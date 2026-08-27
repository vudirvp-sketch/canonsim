"""Two paths, one truth (STATE-1, D-023, KI#5): the runtime keeps an
incremental projection `state_new = apply(state_old, event)` updated as
events are emitted; `fold(log)` rebuilds the same state for T2 replay.
Never fold on the startup hot path — fold is the truth-test, not the
runtime store. Projection shape: `{entity_id: {prop_path: value}}`, seeded
from pack entity data (`initial_projection`); `apply_event` enforces each
`state_change.from` against the current value, so a log that disagrees with
its own projection fails loudly (INV-1 made executable).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from core.log import EventRecord

__all__ = ["Projection", "apply_event", "fold", "initial_projection"]

Projection = dict[str, dict[str, Any]]


def initial_projection(entities: Mapping[str, Any]) -> Projection:
    """Flatten pack entity state into the projection.

    Locations are registered prop-less (state changes may target them);
    position for every positioned entity (npcs, ambient groups, items);
    `status.*` and `relations.*` for npcs — the props iter-2+ events will
    carry `from` values for. Iteration follows pack list order
    (construction order — INV-2).
    """
    state: Projection = {}

    def _put(entity_id: str, prop: str, value: Any) -> None:
        state.setdefault(entity_id, {})[prop] = value

    for loc in entities.get("locations", []):
        state[loc["id"]] = {}  # registered so state_changes can target it
    for npc in entities.get("npcs", []):
        _put(npc["id"], "position", npc["position"])
        for key, value in npc.get("status", {}).items():
            _put(npc["id"], f"status.{key}", value)
        for key, value in npc.get("relations", {}).items():
            _put(npc["id"], f"relations.{key}", value)
    for ambient in entities.get("ambient_entities", []):
        _put(ambient["id"], "position", ambient["position"])
    for item in entities.get("items", []):
        _put(item["id"], "position", item["position"])
        _put(item["id"], "carrier", item.get("carrier"))
    return state


def apply_event(state: Projection, event: EventRecord) -> Projection:
    """Apply one event's `state_changes` in place; fail loudly on desync."""
    for change in event.state_changes:
        props = state.get(change.entity)
        if props is None:
            raise ValueError(
                f"{event.id}: state_change touches unknown entity {change.entity!r}"
            )
        current = props.get(change.prop)
        if change.from_ != current:
            raise ValueError(
                f"{event.id}: {change.entity}.{change.prop} expected from "
                f"{change.from_!r} but projection holds {current!r}"
            )
        props[change.prop] = change.to_
    return state


def fold(events: Iterable[EventRecord], initial: Projection) -> Projection:
    """Rebuild state from a log (T2 truth-test; never the runtime path)."""
    state: Projection = {entity: dict(props) for entity, props in initial.items()}
    for event in events:
        apply_event(state, event)
    return state
