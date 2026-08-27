"""The scheduler DAG (SCHED-1, `core/scheduler.py`): topological order over
read/write intersections, explicit before/after hints, and the build-time
ambiguity error — two per-tick systems writing the same component with no
explicit order fail at load, never as a runtime race (phase0 §2). The
negative tests are the point: a deliberately conflicting pair must fail.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.pack import load_pack
from core.scheduler import (
    ScheduleAmbiguityError,
    SystemDecl,
    build,
    decls_from_rules,
)

REPO = Path(__file__).resolve().parents[1]


def decl(name: str, *, reads: tuple[str, ...] = (), writes: tuple[str, ...] = (),
         per_tick: bool = True, before: tuple[str, ...] = (),
         after: tuple[str, ...] = ()) -> SystemDecl:
    return SystemDecl(name=name, reads=reads, writes=writes, per_tick=per_tick,
                      before=before, after=after)


def test_writer_runs_before_reader() -> None:
    order = build({
        "reader": decl("reader", reads=("x",)),
        "writer": decl("writer", writes=("x",)),
    })
    assert [d.name for d in order] == ["writer", "reader"]


def test_explicit_hints_order_and_ordering_is_deterministic() -> None:
    # b before a (hint); c is unordered — Kahn pops the sorted ready set,
    # so c lands between the ordered pair. Deterministic either way.
    order = build({
        "a": decl("a", writes=("x",), after=("b",)),
        "b": decl("b", writes=("x",)),
        "c": decl("c"),
    })
    assert [d.name for d in order] == ["b", "c", "a"]
    assert build({
        "a": decl("a", writes=("x",), after=("b",)),
        "b": decl("b", writes=("x",)),
        "c": decl("c"),
    }) == build({
        "c": decl("c"),
        "b": decl("b", writes=("x",)),
        "a": decl("a", writes=("x",), after=("b",)),
    })


def test_non_per_tick_systems_never_enter_the_schedule() -> None:
    order = build({
        "event_driven": decl("event_driven", writes=("x",), per_tick=False),
        "tick": decl("tick", writes=("x",)),
    })
    assert [d.name for d in order] == ["tick"]


def test_write_write_ambiguity_names_the_pair() -> None:
    with pytest.raises(ScheduleAmbiguityError, match="'left' and 'right' both write"):
        build({
            "left": decl("left", writes=("x",)),
            "right": decl("right", writes=("x",)),
        })


def test_ambiguity_resolved_by_hint() -> None:
    order = build({
        "left": decl("left", writes=("x",), before=("right",)),
        "right": decl("right", writes=("x",)),
    })
    assert [d.name for d in order] == ["left", "right"]


def test_cycle_is_loud() -> None:
    with pytest.raises(ScheduleAmbiguityError, match="cycle"):
        build({
            "a": decl("a", writes=("x",), after=("b",)),
            "b": decl("b", writes=("y",), after=("a",)),
        })


def test_ordering_against_unknown_system_is_loud() -> None:
    with pytest.raises(ScheduleAmbiguityError, match="unknown system"):
        build({"a": decl("a", after=("ghost",))})


def test_real_pack_builds_fire_only() -> None:
    pack = load_pack(REPO / "content" / "tavern_pack")
    decls = decls_from_rules(pack.rules)
    assert set(decls) == {
        "time", "position_visibility", "relations", "knowledge",
        "states", "fire", "crime_watch", "director",
    }
    order = build(decls)
    assert [d.name for d in order] == ["fire"]  # the only per-tick system in iter-2


def test_decls_from_rules_skips_section_meta() -> None:
    pack = load_pack(REPO / "content" / "tavern_pack")
    decls = decls_from_rules({"systems": dict(pack.rules["systems"]),
                               "notes": "not a system"})
    assert "notes" not in decls
