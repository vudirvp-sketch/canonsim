"""The chronicle renderer (CHRON-1, `docs/blueprint/phase0.md` §5):
the tale as a pure function of the log.

Every render entry point constructs its own `Engine` on a fresh
`RngBank(seed)` — the seed comes from the log header, so the same log
always renders to the same bytes (T1 covers the chronicle), regardless
of call order or process. The renderer WRITES NOTHING to the log (INV-1
— a render pass that emits canon events is the named violation) and
draws only from the cosmetic stream (INV-2 / RNG-1; the engine assures
it). Within one `render_chronicle` pass the pools advance line by line,
so appending events to a log keeps the rendered prefix identical.

Importance gate (`MVP_SCOPE.md` §9 owns the rule): the pack's
`tale_gate.min_importance` decides which events earn a chronicle line;
day headers group the survivors. The chronicle stays dry — T7 runs on
exactly this output. Per-entity history views (the DF artifact-anchor
free win) are UNGATED: `state <entity>` shows the full mention history,
because a query view is not a tale.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

from core.clock import Clock
from core.economy import (
    ACCOUNT_GLOSS_BLOCK,
    ACCOUNT_PREFIX,
    VERB_EVENT_TYPES,
    is_account_prop,
)
from core.fold import Projection, fold, initial_projection
from core.log import IMPORTANCE_ORDER as _IMPORTANCE_ORDER
from core.log import EventRecord, read_log
from core.pack import Pack
from core.rng import RngBank
from core.transitions import WORLD
from render.tracery import Engine, Grammar

__all__ = [
    "RenderError",
    "chronicle_from_log",
    "compile_glosses",
    "gloss_account_kind",
    "gloss_knows",
    "render_chronicle",
    "render_entity_view",
    "render_scene_card",
    "replay_report",
]

_POSITION_PROP: Final = "position"
_NAME_PROP: Final = "name"

#: The templates.json block that owns the account-kind glosses (rs-2,
#: the reader-surface boundary over the W5 rendering failure): a mapping
#: from the account KIND to its reader prose — a noun phrase headed by
#: the kind word, authored to sit in both the verb lines' `{kind}` slot
#: ("16 paper owed to ...") and the state line's apposition
#: (`account.paper: 16 — ...`). The boundary law is rs-1's own: the pack
#: owns the words, the renderer owns the mapping — a kind with no table
#: entry renders dry and honest (the foreign-log fallback). The block
#: name's single owner: `core/economy.py` (the lint
#: `core/packlint/economy.py` reads it there; this module imports it —
#: never a second constant).
GLOSS_BLOCK: Final = "knows"

_GLOSS_SLOT: Final = re.compile(r"\{([a-z_]+)\}")

#: The account verbs' event types — the ONE family whose outcome `kind`
#: names an account kind (the worldgen memory line's `kind` is the
#: collection name, never an account; the mapping scopes to the verbs
#: so the two never collide). `core/economy.py` owns the spelling.
_ACCOUNT_VERB_EVENTS: Final[frozenset[str]] = frozenset(VERB_EVENT_TYPES.values())


class RenderError(RuntimeError):
    """A render-side contract failure (unknown entity, malformed log)."""


def display_name(pack: Pack, entity_id: str | None) -> str:
    """The prose name of an entity id; `world` is a mechanic, not pack data."""
    if entity_id is None:
        return ""
    if entity_id == WORLD:
        return "the world"
    record = pack.entity(entity_id)
    if record is None:
        return entity_id  # an id from a foreign log — dry and honest
    return str(record.get("name", entity_id))


class _Positions:
    """A running position + born-name map while iterating events (the
    renderer's own lightweight fold — enough to resolve `{location}` at
    each event's tick and the name-1 born names (`name` state changes,
    the condensation's births) without re-folding the whole projection
    per line)."""

    def __init__(self, pack: Pack) -> None:
        self._where: dict[str, str] = {}
        self._names: dict[str, str] = {}
        for category in ("npcs", "ambient_entities", "items"):
            for record in pack.entities[category]:
                self._where[record["id"]] = record["position"]
        # depth-6: the group entities' anchors (optional category — the
        # 68a pattern; a group ACTS through the door, and its events
        # render the anchor as {location} like any actor's)
        for record in pack.entities.get("groups", ()):
            self._where[record["id"]] = record["position"]

    def apply(self, event: EventRecord) -> None:
        for change in event.state_changes:
            if change.prop == _POSITION_PROP:
                self._where[change.entity] = change.to_
            elif change.prop == _NAME_PROP:
                self._names[change.entity] = str(change.to_)

    def location_of(self, entity_id: str) -> str:
        return self._where.get(entity_id, "")

    def born_name(self, entity_id: str) -> str | None:
        """The event-born name (name-1), or None — the fold outranks
        the pack record (canon is the answer; an authored name has no
        birth event, an unborn generated name answers None and the
        caller falls to the pack/id)."""
        return self._names.get(entity_id)

    def display(self, pack: Pack, entity_id: str | None) -> str:
        """The fold-aware display name: the born name first (canon),
        else the pack's authored `name`, else the dry id."""
        if entity_id is None:
            return ""
        born = self.born_name(entity_id)
        if born is not None:
            return born
        return display_name(pack, entity_id)


def _event_context(
    event: EventRecord,
    pack: Pack,
    positions: _Positions,
    glosses: Sequence[tuple[tuple[str, ...], tuple[str, ...], str]] = (),
) -> dict[str, Any]:
    """The slot vocabulary for one event line: derived slots first, then
    the outcome payload (entity ids mapped to display names, booleans
    kept raw for `{cond?...|...}` conditionals). The `knows` slot rides
    the gloss boundary (rs-1): a told machine token maps to the pack's
    reader prose before any template sees it — both the outcome's own
    `knows` (the telling path) and the first knowledge record's (the
    witness path) — one boundary, every consumer."""
    outcome = dict(event.outcome)
    first_record = event.knowledge[0] if event.knowledge else None
    target_name = positions.display(pack, event.target) if event.target else ""
    location_id = outcome.get("location") or positions.location_of(event.actor)
    knows = outcome.get(
        "knows", first_record.knows if first_record else ""
    )
    context: dict[str, Any] = {
        "t": event.t,
        "event_type": event.type,
        "actor": positions.display(pack, event.actor),
        "target": target_name,
        "target_location": target_name,
        "location": display_name(pack, location_id) if location_id else "",
        "action_label": outcome.get("action", event.type),
        "knows": gloss_knows(glosses, pack, positions, knows),
        "fidelity": outcome.get(
            "fidelity", first_record.fidelity if first_record else ""
        ),
        "axes": ", ".join(outcome.get("axes", ())),
    }
    # rs-2 (the account-kind gloss boundary): the account verbs' `kind`
    # slot maps through the pack's table BEFORE the generic outcome
    # loop can land the raw word — the kind's meaning rides every
    # account line (the tale + the entity view's history, one boundary,
    # every consumer, rs-1's own shape). Scoped to the verb family so
    # the worldgen memory line's `kind` (the collection name) never
    # enters the table's key space; an unglossed kind renders dry.
    if event.type in _ACCOUNT_VERB_EVENTS:
        kind = outcome.get("kind")
        if isinstance(kind, str):
            context["kind"] = gloss_account_kind(pack.templates, kind)
    # The promotion door (iter-11, D-054): a texture-path take carries the
    # mediator-resolved reference in its outcome and NO canon target — the
    # take templates branch on {target} and render the promoted slot noun.
    texture = outcome.get("texture")
    if isinstance(texture, Mapping) and isinstance(texture.get("slot"), str):
        context["texture_slot"] = texture["slot"]
    for key, value in outcome.items():
        if key not in context:
            context[key] = _display_if_entity(pack, positions, value)
    return context


def _display_if_entity(
    pack: Pack, positions: _Positions, value: Any
) -> Any:
    """Map a value to its display name when it IS a pack entity id
    (name-1, KI#84: fold-first — the running fold's born name
    outranks the pack record on EVERY id-valued reference, the
    outcome slots included, not just the derived actor/target; the
    collision law keeps the drawn-name≠id mapping unambiguous)."""
    if (
        isinstance(value, str)
        and value != WORLD
        and pack.entity(value) is not None
    ):
        return positions.display(pack, value)
    return value


def compile_glosses(
    templates: Mapping[str, Any],
) -> tuple[tuple[tuple[str, ...], tuple[str, ...], str], ...]:
    """The knows-gloss table compiled to matchable form (rs-1): each
    entry becomes (anchors, slots, gloss) — the literal anchors between
    the pattern's slots, the slot names in order, and the reader prose.
    A slot-free pattern compiles to a single exact-match anchor. The
    table's own declaration order is the match order (deterministic,
    INV-2's spirit — the pack's own priority)."""
    table = templates.get(GLOSS_BLOCK, {})
    if not isinstance(table, Mapping):
        return ()
    compiled: list[tuple[tuple[str, ...], tuple[str, ...], str]] = []
    for pattern, gloss in table.items():
        if not isinstance(pattern, str) or not isinstance(gloss, str):
            continue  # a malformed row is inert data, never a crash
        parts = _GLOSS_SLOT.split(pattern)
        anchors = tuple(parts[0::2])
        slots = tuple(parts[1::2])
        compiled.append((anchors, slots, gloss))
    return tuple(compiled)


def _match_gloss(
    anchors: tuple[str, ...], slots: tuple[str, ...], token: str
) -> tuple[str, ...] | None:
    """Decompose `token` against one compiled pattern: the anchors must
    appear in order (the first a prefix, the last a suffix when
    non-empty) and the between-anchor segments are the slot values.
    First-occurrence matching per inner anchor, left to right —
    deterministic. An empty slot value or a missing anchor is no match;
    adjacent slots (an empty inner anchor) cannot resolve and never
    match (no mint site declares them)."""
    if not slots:
        return () if token == anchors[0] else None
    if any(anchor == "" for anchor in anchors[1:-1]):
        return None  # adjacent slots — unresolvable by construction
    rest = token
    if anchors[0]:
        if not rest.startswith(anchors[0]):
            return None
        rest = rest[len(anchors[0]):]
    values: list[str] = []
    for anchor in anchors[1:-1]:
        index = rest.find(anchor)
        if index < 0:
            return None
        values.append(rest[:index])
        rest = rest[index + len(anchor):]
    last = anchors[-1]
    if last:
        if not rest.endswith(last):
            return None
        final = rest[: len(rest) - len(last)]
    else:
        final = rest
    values.append(final)
    if any(value == "" for value in values):
        return None
    return tuple(values)


def _expand_gloss(gloss: str, context: Mapping[str, str]) -> str:
    """Fill the gloss's `{slot}` markers from the matched values — the
    pattern-side twin of the matcher, one closure per call (never a
    loop-bound lambda — B023's own law)."""
    return _GLOSS_SLOT.sub(
        lambda match: str(context.get(match.group(1), match.group(0))),
        gloss,
    )


def gloss_knows(
    glosses: Sequence[tuple[tuple[str, ...], tuple[str, ...], str]],
    pack: Pack,
    positions: _Positions,
    token: Any,
) -> Any:
    """The told-fact boundary (rs-1): map one knowledge token to its
    reader prose through the pack's gloss table — the slot values
    re-displayed fold-first (`_display_if_entity`: an entity id becomes
    its display name, a non-entity value like a texture noun stays
    raw). A token with no matching entry returns UNCHANGED — the dry
    honest fallback for foreign logs and unglossed literals, never an
    error mid-render."""
    if not isinstance(token, str) or not token:
        return token
    for anchors, slots, gloss in glosses:
        values = _match_gloss(anchors, slots, token)
        if values is None:
            continue
        context = {
            slot: str(_display_if_entity(pack, positions, value))
            for slot, value in zip(slots, values, strict=True)
        }
        return _expand_gloss(gloss, context)
    return token


def gloss_account_kind(templates: Mapping[str, Any], kind: str) -> str:
    """The account-kind boundary (rs-2, the W5 rendering fix's first
    half): one account kind mapped to its reader prose through the
    pack's `account_kinds` table — the kind's MEANING (the W5 first
    run's finding: "16 paper owed" was indistinguishable from "16
    paper held" because the kind's meaning rendered nowhere). A kind
    with no entry returns UNCHANGED — the dry honest fallback (an
    unglossed kind's bare word IS its meaning; a foreign log's kinds
    are not the renderer's to invent), `gloss_knows`'s own family law.
    A malformed row (a non-string or empty value) is inert data here —
    the load-time lint owns the refusal."""
    table = templates.get(ACCOUNT_GLOSS_BLOCK)
    if not isinstance(table, Mapping):
        return kind
    gloss = table.get(kind)
    if not isinstance(gloss, str) or not gloss:
        return kind
    return gloss


def _born_or_pack(
    projection: Projection, pack: Pack, entity_id: str
) -> str:
    """The fold-aware display name over a full projection (the scene
    card + the entity view — name-1's read surface: the born name
    first (canon outranks the pack record), else the authored `name`,
    else the dry id — the unborn generated name renders honestly as
    its id)."""
    born = projection.get(entity_id, {}).get(_NAME_PROP)
    if born is not None:
        return str(born)
    return display_name(pack, entity_id)


def render_chronicle(
    events: Sequence[EventRecord], pack: Pack, seed: int
) -> str:
    """Day-grouped tale lines for the gated events, in log order."""
    clock = Clock.from_rules(dict(pack.rules["time"]))
    grammar = Grammar(pack.templates)
    engine = Engine(grammar, RngBank(seed))
    gate = _IMPORTANCE_ORDER.index(grammar.tale_gate)
    glosses = compile_glosses(pack.templates)
    lines: list[str] = []
    positions = _Positions(pack)
    last_day: int | None = None
    for event in events:
        positions.apply(event)
        if _IMPORTANCE_ORDER.index(event.importance) < gate:
            continue
        day = clock.day_of(event.t)
        if day != last_day:
            header = engine.expand_symbol(
                "day_header",
                {"day": day + 1, "phase": clock.phase_of(event.t)},
            )
            lines.append(header)
            last_day = day
        lines.append(
            engine.expand_symbol(
                _line_symbol(grammar, event.type),
                _event_context(event, pack, positions, glosses),
            )
        )
    return "\n".join(lines) + ("\n" if lines else "")


def render_scene_card(projection: Projection, pack: Pack, seed: int) -> str:
    """Where the player stands and who else is there (pack order)."""
    player = pack.player_id()
    location = projection[player][_POSITION_PROP]
    present = [
        _born_or_pack(projection, pack, record["id"])
        for category in ("npcs", "ambient_entities")
        for record in pack.entities[category]
        if record["id"] != player
        and projection.get(record["id"], {}).get(_POSITION_PROP) == location
    ]
    context = {
        "location_name": display_name(pack, location),
        "present_names": ", ".join(present) if present else "no one",
    }
    engine = Engine(Grammar(pack.templates), RngBank(seed))
    return engine.expand_symbol("scene_card", context)


def _mentions(event: EventRecord, entity_id: str) -> bool:
    if event.actor == entity_id or event.target == entity_id:
        return True
    if any(change.entity == entity_id for change in event.state_changes):
        return True
    return any(record.who == entity_id for record in event.knowledge)


def render_entity_view(
    events: Sequence[EventRecord],
    projection: Projection,
    pack: Pack,
    entity_id: str,
    seed: int,
) -> str:
    """Per-entity history (ungated) + current state — the `state` command."""
    if entity_id not in projection and pack.entity(entity_id) is None:
        raise RenderError(f"unknown entity {entity_id!r}")
    grammar = Grammar(pack.templates)
    engine = Engine(grammar, RngBank(seed))
    glosses = compile_glosses(pack.templates)
    positions = _Positions(pack)
    lines: list[str] = [
        f"{_born_or_pack(projection, pack, entity_id)} ({entity_id})"
    ]
    lines.extend(_state_lines(projection, projection.get(entity_id, {}), pack))
    lines.append("history:")
    wrote = False
    for event in events:
        positions.apply(event)
        if not _mentions(event, entity_id):
            continue
        wrote = True
        lines.append(
            f"[t {event.t}] "
            + engine.expand_symbol(
                _line_symbol(grammar, event.type),
                _event_context(event, pack, positions, glosses),
            )
        )
    if not wrote:
        lines.append("  (no events mention this entity)")
    return "\n".join(lines) + "\n"


def _state_lines(
    projection: Projection, props: Mapping[str, Any], pack: Pack
) -> list[str]:
    """The entity's current projection state, dry and prop-path-labeled.
    name-1 (KI#84): the `carrier:` line is an npc-reference surface —
    the carrier's display resolves fold-first (the born name outranks
    the pack record); `at:` stays the authored location surface —
    locations take no name births. rs-2: an account prop whose kind
    carries a pack gloss renders the level + the kind's meaning — the
    standing debt reads as owed, never as inventory (the W5 first
    run's own finding); an unglossed kind keeps the dry line (the
    fallback law, `gloss_account_kind`'s own)."""
    lines: list[str] = []
    for prop, value in props.items():
        if prop == _POSITION_PROP:
            lines.append(f"  at: {display_name(pack, value)}")
        elif prop == "carrier":
            carrier = (
                _born_or_pack(projection, pack, value)
                if value is not None else ""
            )
            lines.append(f"  carrier: {carrier or '—'}")
        elif is_account_prop(prop) and isinstance(value, int) \
                and not isinstance(value, bool):
            kind = prop[len(ACCOUNT_PREFIX):]
            gloss = gloss_account_kind(pack.templates, kind)
            meaning = f" — {gloss}" if gloss != kind else ""
            lines.append(f"  {prop}: {value}{meaning}")
        elif isinstance(value, bool):
            lines.append(f"  {prop}: {'yes' if value else 'no'}")
        else:
            lines.append(f"  {prop}: {value}")
    return lines


def _line_symbol(grammar: Grammar, event_type: str) -> str:
    """`event.<type>` when the grammar knows it, else the fallback line."""
    symbol = f"event.{event_type}"
    return symbol if symbol in grammar else "fallback"


def chronicle_from_log(log_path: Path, pack: Pack, schema: Mapping[str, Any]) -> str:
    """Read a log and render its chronicle (the seed comes from the
    header — the same log always renders the same bytes)."""
    header, events = read_log(log_path, schema)
    return render_chronicle(events, pack, seed=int(header["seed"]))


def replay_report(
    log_path: Path, pack: Pack, schema: Mapping[str, Any]
) -> tuple[str, int]:
    """The `replay` command: validate the log (T0), fold it (T2), report.

    Returns (report text, event count); the fold raising is the point —
    a log that disagrees with its own projection fails loudly here.
    """
    header, events = read_log(log_path, schema)
    state = fold(events, initial_projection(pack.entities))
    irreversibles = sum(
        1 for event in events for change in event.state_changes if change.irreversible
    )
    last_tick = events[-1].t if events else 0
    text = (
        f"{log_path}: {len(events)} events, ticks 0..{last_tick}, "
        f"seed {header['seed']}, pack {header['pack']}\n"
        f"fold OK — {len(state)} entities rebuilt, "
        f"{irreversibles} irreversible change(s) (T2)"
    )
    return text, len(events)
