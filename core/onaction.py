"""The on_action dispatch layer (drama-3, phase 3; phases.md §3 — the
Paradox on_action table adapted per L10: event X commits → content
reacts, as pack data). `docs/DIRECTOR_SPEC.md` §3c owns the contract;
the donor mechanics live in `docs/ref/paradox_scripting.md`.

What the donor gave, minus its footguns: the on_action table keys
reactions to committed event types; every entry of the keyed list
dispatches (**append-not-overwrite** — a second declaration never
replaces the first, and the hardcoded system reactions keep running
before the pack's entries, the donor's "vanilla first, custom
appended" composition). The reaction scope is an EXPLICIT context
argument, never an implicit `this`: the v0.1 selector `witnesses`
reads the triggering event's own knowledge records (the named use
case — "every NPC who witnessed X"), and the gate conditions are
per-entity prop reads evaluated with the CANDIDATE as the argument
(no entity field in the spec, no scope magic). MTTH stays excluded
(TIME-1): the reaction is immediate and cause-chained; nothing
schedules.

The reaction body is a scoped state-change event (the alarm shape,
phase0 §3): one event per entry, one clamped numeric delta per
passing candidate, committed through the same door as every canon
event (D-037 — the loop chains the cause and stamps the seed). The
draft carries NO knowledge and NO hooks of its own: the existing
system reactions skip a knowledge-less event, deferred consequences
ride the actions' own hooks (D-005), and pack lint rejects any table
key that an entry emits (the one-hop law) — the cascade terminates
by construction.

Pure per INV-2: a function of (pack data, projection, record) with
no RNG, no clock, no stored choice; the generator is lazy on purpose
(each entry's draft reads the projection as left by the previously
committed entries — the KI#13 discipline, never a stale world)."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING, Any, Final

from core.intent import pack_importance
from core.log import EventDraft, StateChange
from core.predicates import COMPARATORS
from core.transitions import WORLD

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.log import EventRecord
    from core.pack import Pack

__all__ = [
    "ACTOR_TARGET_KEYS",
    "ENTRY_KEYS",
    "GATE_KEYS",
    "SCOPES",
    "STATE_KEYS",
    "on_action_drafts",
]

SCOPES: Final = ("witnesses",)
"""The closed entity-set selector vocabulary (drama-3 v0.1). `witnesses`
= every knower named in the triggering event's own knowledge records,
deduped, in event order (the Paradox event scope minus the implicit-
`this` footgun — the entity set is read from the record, never
inherited). New selectors land with their first consumer."""

ACTOR_TARGET_KEYS: Final = ("world", "source_actor", "source_target")
"""The closed actor/target resolution vocabulary: the reaction event's
actor and target resolve from the SOURCE event (one hop, never a
`fromfrom` chain) or to the world-event actor. Defaults: actor
`world`, target `source_target`."""

ENTRY_KEYS: Final = ("scope", "gate", "event", "state", "actor", "target", "notes")
"""The closed reaction-entry key set (an unknown key is a lint error,
never a silent ignore)."""

GATE_KEYS: Final = ("prop", "comparator", "value")
"""The closed per-entity gate condition key set: the quantified
predicate — evaluated with the candidate entity as the explicit
context argument, so the spec carries no entity field at all."""

STATE_KEYS: Final = ("prop", "add")
"""The closed state-change key set: the prop path and a non-zero
numeric delta, clamped to the pack's `relations.scale` (the alarm
precedent — the one numeric scale)."""


def on_action_drafts(
    pack: "Pack",
    projection: "Projection",
    record: "EventRecord",
) -> Iterator[EventDraft]:
    """Yield the pack's on_action reaction drafts for one committed
    record, one per dispatching entry (lazy: each draft reads the
    projection as left by the previously committed ones — the loop
    commits between yields). Entries are append-composed: every entry
    of the keyed list dispatches independently. A pack without an
    `on_action` block yields nothing (the v0.1 behavior,
    byte-identical — the pack's own declaration is the gate, INV-3)."""
    config = pack.rules.get("on_action", {})
    entries = config.get(record.type)
    if not entries:
        return
    for entry in entries:
        scope = entry.get("scope")
        if scope not in SCOPES:
            raise ValueError(f"unknown on_action scope {scope!r}")
        draft = _reaction_draft(pack, projection, record, entry)
        if draft is not None:
            yield draft


def _reaction_draft(
    pack: "Pack",
    projection: "Projection",
    record: "EventRecord",
    entry: Mapping[str, Any],
) -> EventDraft | None:
    """Build one entry's reaction draft: the scope's entity set, gated
    per entity, each passing candidate with a numeric home on the
    declared prop gains the clamped delta — ONE event (the alarm
    shape). None when nobody reacts (the alarm precedent: no
    occupants, no alarm — an empty scope is a world answer, not an
    event)."""
    candidates = _witnesses(record)
    gate = entry.get("gate", ())
    prop = entry["state"]["prop"]
    add = int(entry["state"]["add"])
    scale = pack.rules["relations"]["scale"]
    changes: list[StateChange] = []
    reacting: list[str] = []
    for who in candidates:
        if not _gate_passes(gate, projection, who):
            continue
        props = projection.get(who)
        current = props.get(prop) if props else None
        if not isinstance(current, int) or isinstance(current, bool):
            continue  # no numeric home — the world answers (the suspicion law)
        new = max(int(scale[0]), min(int(scale[1]), current + add))
        if new == current:
            continue  # the KI#13 discipline: no no-op deltas in canon
        changes.append(
            StateChange(entity=who, prop=prop, from_=current, to_=new)
        )
        reacting.append(who)
    if not changes:
        return None
    actor = _resolve(entry.get("actor", "world"), record)
    target = _resolve(entry.get("target", "source_target"), record)
    entities = set(reacting) | {WORLD}
    if target is not None:
        entities.add(target)
    return EventDraft(
        t=record.t,
        type=entry["event"],
        actor=actor,
        target=target,
        cause=None,  # chained to the triggering event by the loop
        outcome={
            "location": _source_location(record, projection),
            "reacting": tuple(reacting),
        },
        knowledge=(),  # v0.1: no knowledge of its own — cascades terminate
        state_changes=tuple(changes),
        hooks=(),  # deferred consequences ride the actions' own hooks (D-005)
        importance=pack_importance(
            pack.rules, entities, irreversible=0, hooks=0,
            event_type=entry["event"],
        ),
        provenance={},  # the loop stamps the seed at commit
    )


def _witnesses(record: "EventRecord") -> list[str]:
    """The `witnesses` scope: every knower of the triggering event, in
    the record's own order, deduped by first occurrence (construction
    order — INV-2's legal iteration; the same knower learning two
    tokens of one event reacts once)."""
    seen: set[str] = set()
    candidates: list[str] = []
    for knowledge in record.knowledge:
        who = knowledge.who
        if who not in seen:
            seen.add(who)
            candidates.append(who)
    return candidates


def _gate_passes(
    gate: Any,
    projection: "Projection",
    who: str,
) -> bool:
    """The quantified predicate: every condition must pass for the
    candidate (implicit-AND, the Paradox limit block). The entity is
    an explicit ARGUMENT — the spec carries only the prop read, so
    there is no implicit `this` to misread. The comparison semantics
    are `core/predicates.py`'s own (the single owner): a missing prop
    answers False under the ordering comparators and `equals`, True
    under `not_equals`; a bool never equals a number."""
    for condition in gate:
        props = projection.get(who)
        actual = props.get(condition["prop"]) if props else None
        expected = condition["value"]
        comparator = condition["comparator"]
        if comparator not in COMPARATORS:
            raise ValueError(f"unknown gate comparator {comparator!r}")
        if comparator == "equals":
            if not _same_kind(actual, expected) or actual != expected:
                return False
        elif comparator == "not_equals":
            if _same_kind(actual, expected) and actual == expected:
                return False
        else:
            if not isinstance(actual, int) or isinstance(actual, bool):
                return False
            if comparator == "at_least" and actual < expected:
                return False
            if comparator == "at_most" and actual > expected:
                return False
    return True


def _same_kind(left: Any, right: Any) -> bool:
    """The predicates.py bool/int law (linked owner: `core/predicates.py::
    _same_kind`): a flag must not equal a count."""
    return isinstance(left, bool) == isinstance(right, bool)


def _resolve(keyword: str, record: "EventRecord") -> str | None:
    """Resolve an actor/target keyword against the source event (one
    hop — the donor's this/from chain collapsed to a closed
    vocabulary). `source_target` may honestly resolve to None (the
    source event carried no target)."""
    if keyword == "world":
        return WORLD
    if keyword == "source_actor":
        return record.actor
    return record.target


def _source_location(
    record: "EventRecord", projection: "Projection"
) -> str | None:
    """Where the reaction happens for the renderer: the source event's
    own `location` outcome field when it carries one, else the source
    actor's position (the chronicle's own fallback law, applied at
    draft time so the event is self-describing in the log)."""
    location = record.outcome.get("location")
    if isinstance(location, str):
        return location
    props = projection.get(record.actor)
    position = props.get("position") if props else None
    return position if isinstance(position, str) else None
