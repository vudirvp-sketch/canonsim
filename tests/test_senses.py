"""iter-378 acceptance — the director's senses index (the iter-362
class applied to the P2e world-sensing terms): the commit-path fold of
global suspicion + visible physical threats, read O(1) per beat for the
BOUND projection (the `director_global_passes` wall member's answer).

The laws here pin the EQUALITY the index is built on — the scans stay
the semantic owners (D-024); the fold must answer exactly what they
answer at birth, after any committed sequence, across a resume, and
only for the bound object (the identity gate — every foreign
projection keeps the scans, the KI#16 law unchanged for the fallback
path). KI#16's own constraint is pinned too: the fold is born from the
pack-seeded INITIAL projection and tracks every committed event, never
the hook-seeding ones.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.director import (
    Director,
    EnabledPolicy,
    SensesIndex,
    _global_suspicion,
    _threat_states,
    _visible_physical_threats,
)
from core.fold import Projection, apply_event, initial_projection
from core.log import EventRecord
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

# The six committed packs — the birth law's corpus (the iter-362
# index-vs-linear law's own set).
_PACK_DIRS = (
    "tavern_pack", "province_pack", "farstead_pack",
    "grim_pack", "pressure_pack", "road_pack",
)


def _scans(projection: Projection, states: frozenset[str]) -> tuple[int, int]:
    """The semantic owners' answer, as a pair."""
    return (
        _global_suspicion(projection),
        _visible_physical_threats(projection, states),
    )


def _change(
    entity: str, prop: str, from_: Any, to_: Any
) -> Any:
    from core.log import StateChange

    return StateChange(entity=entity, prop=prop, from_=from_, to_=to_)


def _record(changes: tuple[Any, ...], n: int) -> EventRecord:
    return EventRecord(
        id=f"ev_{n:04d}", t=n, type="test_event", actor="pc_01", cause=None,
        outcome={}, knowledge=(), state_changes=changes, hooks=(),
        importance="low", provenance={}, target=None,
    )


# -- the birth law (KI#16: the whole projection, seeds included) ----------------


def test_birth_scan_equals_the_scans_on_every_committed_pack() -> None:
    """`from_projection` answers what the scans answer on every
    committed pack's seeded initial projection — the fold's basis is
    the WHOLE projection (KI#16), so a pack that seeded suspicion or a
    burning spot at birth would be sensed exactly like an event-written
    one (the current six seed neither; the law holds for any that
    does)."""
    for name in _PACK_DIRS:
        pack = load_pack(REPO / "content" / name)
        projection = initial_projection(pack.entities)
        states = _threat_states(pack.rules)
        index = SensesIndex.from_projection(projection, states)
        assert (index.suspicion, index.threats) == _scans(projection, states), (
            name
        )


def test_birth_scan_counts_seeded_values_not_zero() -> None:
    """The teeth of the birth law: a hand-seeded projection carrying a
    pack-style suspicion axis and a spreading spot reads NON-zero
    through the index — a fold born from zero would be blind to the
    pack's declarations (the KI#16 regression this law exists to
    catch)."""
    projection: Projection = {
        "npc_a": {"relations.suspicion": 7},
        "npc_b": {"pair.npc_a.suspicion": 3, "position": "loc_x"},
        "loc_x": {"fire.bar": "burning", "flags_ok": "burning"},
    }
    states = frozenset({"burning"})
    index = SensesIndex.from_projection(projection, states)
    # 7 + 3 on the axis; ONE threat (the dotted fire.bar — the undotted
    # flags_ok never counts, the scan's own `.` gate)
    assert (index.suspicion, index.threats) == (10, 1)
    assert (index.suspicion, index.threats) == _scans(projection, states)


# -- the fold twin: after every committed event, index == scans -----------------


def test_the_fold_twin_agrees_after_every_event() -> None:
    """THE equality law. A scripted sequence exercising every edge the
    fold meets — applied to a real projection through `apply_event`
    (the commit door's own net) and fed to a Director through `seed`
    (the index's own door) — after EACH event the index answers what
    fresh scans answer on the folded projection:

    - int suspicion in BOTH homes (the flat and the pair record);
    - a BOOL in a suspicion home (never counts — the int-not-bool
      discipline, both directions of the delta);
    - a STRING in a suspicion home (never counts);
    - a dotted prop entering and leaving the threat states;
    - an UNdotted prop holding a threat-state value (never a threat);
    - a prop BIRTH with `from_ = None` (contributes nothing on the
      from-side: None is neither an int nor a state);
    - a prop cleared to None (the to-side symmetric);
    - TWO changes to the same prop inside ONE event (the progressive
      semantics: the second `from_` is the first's `to_`)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    states = _threat_states(pack.rules) | frozenset({"burning"})
    projection = initial_projection(pack.entities)
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=5))
    director.bind(projection)
    # the sequence: (entity, prop, from_, to_) — from_ always the live
    # value (the apply_event contract)
    script: list[tuple[str, str, Any, Any]] = [
        ("npc_guard_01", "relations.suspicion", None, 25),  # birth (unseeded home)
        ("npc_guard_02", "relations.suspicion", None, 10),
        ("npc_guard_01", "relations.suspicion", 25, True),  # -> bool
        ("npc_guard_01", "relations.suspicion", True, "watching"),  # str
        ("npc_guard_01", "relations.suspicion", "watching", 12),  # back to int
        ("npc_guard_02", "pair.pc_01.suspicion", 0, 4),  # the seeded pair home
        ("npc_guard_02", "pair.pc_01.suspicion", 4, 0),
        ("loc_tavern", "fire.bar", None, "burning"),  # threat birth
        ("loc_tavern", "fire.tables", None, "burning"),
        ("loc_tavern", "fire.bar", "burning", "smoldering"),  # leaves the states
        ("loc_tavern", "fire.tables", "burning", None),  # cleared
        ("loc_tavern", "flags_ok", None, "burning"),  # UNdotted — never a threat
        ("npc_barkeep_01", "relations.scale", None, 3),  # dotted, non-threat, non-axis
    ]
    for n, (entity, prop, from_, to_) in enumerate(script, start=1):
        record = _record((_change(entity, prop, from_, to_),), n)
        apply_event(projection, record)
        director.seed(record)
        assert (
            director._senses.suspicion,
            director._senses.threats,
        ) == _scans(projection, states), f"diverged at script line {n}"


def test_repeated_same_prop_changes_inside_one_event() -> None:
    """The progressive semantics: one event may write the same prop
    twice (change N checked against the state as left by 0..N-1) — the
    fold applies BOTH deltas in order, exactly as `apply_event` applies
    both writes."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    states = _threat_states(pack.rules)
    projection = initial_projection(pack.entities)
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=5))
    director.bind(projection)
    record = _record(
        (
            _change("npc_guard_01", "relations.suspicion", None, 30),
            _change("npc_guard_01", "relations.suspicion", 30, 5),
            _change("loc_tavern", "fire.bar", None, "burning"),
        ),
        1,
    )
    apply_event(projection, record)
    director.seed(record)
    assert (
        director._senses.suspicion,
        director._senses.threats,
    ) == _scans(projection, states)


# -- the identity gate (bound: the index; foreign: the scans) -------------------


def test_the_identity_gate_bound_reads_the_fold_foreign_reads_the_scan() -> None:
    """`releases` reads the fold ONLY for the exact object `bind`
    stamped; any other projection — even a content-equal copy — gets
    the whole-projection scans. Observable through the quiet gate: a
    bound projection whose suspicion the fold raised sits ABOVE the
    floor (no quiet release), while a foreign copy without the raise
    sits below it (the quiet release fires — the scan answered the
    foreign view, never the stale fold)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=5))
    bound: Projection = initial_projection(pack.entities)
    director.bind(bound)
    # seed the hook (the buffer) and raise the axis on the BOUND object
    hook_event = EventRecord(
        id="ev_0001", t=0, type="test_event", actor="pc_01", cause=None,
        outcome={}, knowledge=(), state_changes=(), hooks=("guard_suspicious_of_pc",),
        importance="low", provenance={}, target=None,
    )
    director.seed(hook_event)
    # a raise the index tracks — sized to sit ABOVE the quiet floor (5)
    # but BELOW the pacing peak floor (25), so the probe isolates the
    # quiet gate from the clock (RAMP stays RAMP on both sides)
    raise_event = _record(
        (_change("npc_guard_01", "relations.suspicion", None, 10),), 2
    )
    apply_event(bound, raise_event)
    director.seed(raise_event)
    assert director._senses.suspicion == 10
    # the BOUND object: entropy 10 + hook base 2 = 12 sits above the
    # floor 5 — the quiet path stays closed
    assert director.releases(bound, beat_tick=0) == []
    # the FOREIGN copy: same content minus the raise — the scan reads
    # ITS projection (suspicion 0), the quiet gate opens, the hook
    # releases (the fallback law: the director senses the projection it
    # was handed, never the fold)
    foreign: Projection = initial_projection(pack.entities)
    foreign["npc_guard_01"]["relations.suspicion"] = None
    released = director.releases(foreign, beat_tick=0)
    assert len(released) == 1


# -- the real-log twin (the end-to-end equality on committed machinery) --------


def _theft_steps() -> list[dict[str, Any]]:
    """The crime chain that moves both sensed axes: a theft seeds
    suspicion through the reaction cascade, the wait crosses beats and
    a rotation (decay/urgency commits fold through `seed` the
    while)."""
    return [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "wait", "ticks": 760},
    ]


def test_the_real_log_twin_law(tmp_path: Path) -> None:
    """After a real run — the full reaction cascade, beats, a watch
    rotation — the Director's fold answers what fresh scans answer on
    the Simulator's own live projection (the production path the index
    exists for: every committed event folded in apply order)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    sim = Simulator(pack, 42, tmp_path / "run.jsonl", SCHEMA, commit="0000000")
    sim.open()
    states = _threat_states(pack.rules)
    sim.run_steps(_theft_steps()[:2])
    # mid-run probe: the fold already tracks the cascade's writes
    assert (
        sim._director._senses.suspicion,
        sim._director._senses.threats,
    ) == _scans(sim.projection, states)
    sim.run_steps(_theft_steps()[2:])
    sim.close()
    assert (
        sim._director._senses.suspicion,
        sim._director._senses.threats,
    ) == _scans(sim.projection, states)


def test_the_resume_law(tmp_path: Path) -> None:
    """The resume door re-anchors the fold on the restored projection
    (the bind's honest flush after the replay pass): a resumed
    session's director answers what fresh scans answer on the resumed
    Simulator's projection — the O(1) path survives the process
    boundary exactly like an uninterrupted run's."""
    from core.cursor import cursor_path, load_cursor, save_cursor

    pack = load_pack(REPO / "content" / "tavern_pack")
    log = tmp_path / "split.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(_theft_steps()[:2])
    cursor = sim.export_cursor(director_enabled=True)
    sim.close()
    save_cursor(cursor_path(log), cursor)
    sim2 = Simulator.resume(
        pack, log, SCHEMA, load_cursor(cursor_path(log))
    )
    states = _threat_states(pack.rules)
    assert (
        sim2._director._senses.suspicion,
        sim2._director._senses.threats,
    ) == _scans(sim2.projection, states)
    # and the bound object IS the restored live projection (the O(1)
    # path armed for the resumed session's beats)
    assert sim2._director._bound is sim2.projection
    sim2.run_steps(_theft_steps()[2:])
    sim2.close()
    assert (
        sim2._director._senses.suspicion,
        sim2._director._senses.threats,
    ) == _scans(sim2.projection, states)
