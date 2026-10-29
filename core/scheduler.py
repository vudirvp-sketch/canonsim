"""The system-pass scheduler (SCHED-1, `docs/blueprint/phase0.md` §2):
systems declare `reads`/`writes` as pack data (rules.json `systems`); the
builder topologically sorts the **per-tick** subset on read/write
intersections, honours explicit `before`/`after` hints, and raises
`ScheduleAmbiguityError` naming the offending pair when two systems write
the same component without an explicit order between them — a build-time
failure, never a runtime race (the Bevy/entt organizer discipline).

Only `per_tick: true` systems enter the schedule; the rest are event-driven
(watch change, director releases) and merely carry their annotations. The
loop runs the schedule when tick boundaries pass, band SYSTEM_PASS, one
sub-order slot per DAG position.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

__all__ = ["ScheduleAmbiguityError", "SystemDecl", "build"]


class ScheduleAmbiguityError(RuntimeError):
    """Two per-tick systems write the same component with no explicit order."""


@dataclass(frozen=True, slots=True)
class SystemDecl:
    """One system's scheduling annotation (pack data, rules.json systems)."""

    name: str
    reads: tuple[str, ...]
    writes: tuple[str, ...]
    per_tick: bool
    before: tuple[str, ...] = ()
    after: tuple[str, ...] = ()


def decls_from_rules(rules: Mapping[str, Any]) -> dict[str, SystemDecl]:
    """Parse the pack's `systems` section (load order: sorted by name)."""
    raw = rules.get("systems", {})
    decls: dict[str, SystemDecl] = {}
    for name in sorted(raw):
        entry = raw[name]
        if not isinstance(entry, Mapping):
            continue  # section meta (notes)
        decls[name] = SystemDecl(
            name=name,
            reads=tuple(entry.get("reads", ())),
            writes=tuple(entry.get("writes", ())),
            per_tick=bool(entry.get("per_tick", False)),
            before=tuple(entry.get("before", ())),
            after=tuple(entry.get("after", ())),
        )
    return decls


def _hint_edges(decls: Mapping[str, SystemDecl]) -> set[tuple[str, str]]:
    """Explicit a-before-b edges from before/after hints."""
    edges: set[tuple[str, str]] = set()
    for decl in decls.values():
        for other in decl.before:
            edges.add((decl.name, other))
        for other in decl.after:
            edges.add((other, decl.name))
    return edges


def build(decls: Mapping[str, SystemDecl]) -> tuple[SystemDecl, ...]:
    """The per-tick execution order. Raises on ambiguity (write-write with
    no explicit order) and on cycles; deterministic (sorted tie-breaks)."""
    scheduled = {
        name: decl for name, decl in sorted(decls.items()) if decl.per_tick
    }
    for decl in scheduled.values():
        for referenced in (*decl.before, *decl.after):
            if referenced not in decls:
                raise ScheduleAmbiguityError(
                    f"system {decl.name!r} orders against unknown system {referenced!r}"
                )

    hint_edges = _hint_edges(scheduled)
    # writer -> reader edges (a writes what b reads: a runs first)
    for a in scheduled.values():
        for b in scheduled.values():
            if a.name != b.name and set(a.writes) & set(b.reads):
                hint_edges.add((a.name, b.name))

    for a in scheduled.values():
        for b in scheduled.values():
            if a.name >= b.name:
                continue
            shared = set(a.writes) & set(b.writes)
            if not shared:
                continue
            ordered = (a.name, b.name) in hint_edges or (b.name, a.name) in hint_edges
            if not ordered:
                raise ScheduleAmbiguityError(
                    f"{a.name!r} and {b.name!r} both write {sorted(shared)} "
                    f"with no explicit before/after between them"
                )

    order: list[SystemDecl] = []
    remaining = dict(scheduled)
    while remaining:
        ready = [
            name
            for name in remaining
            if not any(
                (other, name) in hint_edges
                for other in remaining
                if other != name
            )
        ]
        if not ready:
            raise ScheduleAmbiguityError(
                f"cycle in the per-tick schedule: {sorted(remaining)}"
            )
        for name in sorted(ready):  # deterministic
            order.append(remaining.pop(name))
    return tuple(order)
