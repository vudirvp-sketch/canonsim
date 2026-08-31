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

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

from core.clock import Clock
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
    "render_chronicle",
    "render_entity_view",
    "render_scene_card",
    "replay_report",
]

_POSITION_PROP: Final = "position"


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
    """A running position map while iterating events (the renderer's own
    lightweight fold — enough to resolve `{location}` at each event's
    tick without re-folding the whole projection per line)."""

    def __init__(self, pack: Pack) -> None:
        self._where: dict[str, str] = {}
        for category in ("npcs", "ambient_entities", "items"):
            for record in pack.entities[category]:
                self._where[record["id"]] = record["position"]

    def apply(self, event: EventRecord) -> None:
        for change in event.state_changes:
            if change.prop == _POSITION_PROP:
                self._where[change.entity] = change.to_

    def location_of(self, entity_id: str) -> str:
        return self._where.get(entity_id, "")


def _event_context(
    event: EventRecord, pack: Pack, positions: _Positions
) -> dict[str, Any]:
    """The slot vocabulary for one event line: derived slots first, then
    the outcome payload (entity ids mapped to display names, booleans
    kept raw for `{cond?...|...}` conditionals)."""
    outcome = dict(event.outcome)
    first_record = event.knowledge[0] if event.knowledge else None
    target_name = display_name(pack, event.target) if event.target else ""
    location_id = outcome.get("location") or positions.location_of(event.actor)
    context: dict[str, Any] = {
        "t": event.t,
        "event_type": event.type,
        "actor": display_name(pack, event.actor),
        "target": target_name,
        "target_location": target_name,
        "location": display_name(pack, location_id) if location_id else "",
        "action_label": outcome.get("action", event.type),
        "knows": outcome.get(
            "knows", first_record.knows if first_record else ""
        ),
        "fidelity": outcome.get(
            "fidelity", first_record.fidelity if first_record else ""
        ),
        "axes": ", ".join(outcome.get("axes", ())),
    }
    # The promotion door (iter-11, D-054): a texture-path take carries the
    # mediator-resolved reference in its outcome and NO canon target — the
    # take templates branch on {target} and render the promoted slot noun.
    texture = outcome.get("texture")
    if isinstance(texture, Mapping) and isinstance(texture.get("slot"), str):
        context["texture_slot"] = texture["slot"]
    for key, value in outcome.items():
        if key not in context:
            context[key] = _display_if_entity(pack, value)
    return context


def _display_if_entity(pack: Pack, value: Any) -> Any:
    """Map a value to its display name when it IS a pack entity id."""
    if (
        isinstance(value, str)
        and value != WORLD
        and pack.entity(value) is not None
    ):
        return display_name(pack, value)
    return value


def render_chronicle(
    events: Sequence[EventRecord], pack: Pack, seed: int
) -> str:
    """Day-grouped tale lines for the gated events, in log order."""
    clock = Clock.from_rules(dict(pack.rules["time"]))
    grammar = Grammar(pack.templates)
    engine = Engine(grammar, RngBank(seed))
    gate = _IMPORTANCE_ORDER.index(grammar.tale_gate)
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
                _event_context(event, pack, positions),
            )
        )
    return "\n".join(lines) + ("\n" if lines else "")


def render_scene_card(projection: Projection, pack: Pack, seed: int) -> str:
    """Where the player stands and who else is there (pack order)."""
    player = pack.player_id()
    location = projection[player][_POSITION_PROP]
    present = [
        display_name(pack, record["id"])
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
    positions = _Positions(pack)
    lines: list[str] = [f"{display_name(pack, entity_id)} ({entity_id})"]
    lines.extend(_state_lines(projection.get(entity_id, {}), pack))
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
                _event_context(event, pack, positions),
            )
        )
    if not wrote:
        lines.append("  (no events mention this entity)")
    return "\n".join(lines) + "\n"


def _state_lines(props: Mapping[str, Any], pack: Pack) -> list[str]:
    """The entity's current projection state, dry and prop-path-labeled."""
    lines: list[str] = []
    for prop, value in props.items():
        if prop == _POSITION_PROP:
            lines.append(f"  at: {display_name(pack, value)}")
        elif prop == "carrier":
            lines.append(f"  carrier: {display_name(pack, value) or '—'}")
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
