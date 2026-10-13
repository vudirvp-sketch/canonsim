"""iter-379 acceptance — the decay landing index (the iter-362 class
applied to the two population-linear decay scans): per-location
min-heaps of ``(next_fire, npc, prop)`` cells over the LIVE pairs, read
by a peek (`next_decay_tick`) and a bounded enumeration (`decay_drafts`)
for the BOUND objects only (the identity gate).

The laws here pin the EQUALITY the index is built on — the walks stay
the semantic owners (D-024); the pool must answer exactly what the
walks answer at birth, after any committed sequence of staleness edges,
across a resume, without a commit (the enumeration-never-consumes law),
and only for the bound objects. The staleness discipline's own
foundation — INV-1: every cause of staleness rides a committed event,
and `_commit` folds every state change — is what law 3 exercises edge
by edge.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.fold import Projection, apply_event, initial_projection
from core.log import EventRecord, StateChange
from core.loop import Simulator
from core.pack import load_pack
from core.states import DecayIndex, decay_axes, decay_drafts, next_decay_tick

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

# probe ticks and scopes the twin laws sweep (craft beats at 360/720 —
# the tavern grid — plus off-grid ticks the landing formula must still
# answer exactly)
_PROBE_TICKS = (0, 1, 35, 36, 71, 72, 359, 360, 719, 720, 1080, 5000)
_SCOPES: tuple[tuple[str, ...] | None, ...] = (
    None,
    ("loc_tavern",),
    ("loc_backyard",),
    ("loc_tavern", "loc_backyard"),
    ("loc_cellar",),
)


def _change(entity: str, prop: str, from_: Any, to_: Any) -> StateChange:
    return StateChange(entity=entity, prop=prop, from_=from_, to_=to_)


def _record(changes: tuple[StateChange, ...], n: int, tick: int | None = None) -> EventRecord:
    return EventRecord(
        id=f"ev_{n:04d}", t=n if tick is None else tick, type="test_event",
        actor="pc_01", cause=None, outcome={}, knowledge=(),
        state_changes=changes, hooks=(), importance="low", provenance={},
        target=None,
    )


def _assert_twins(
    pack: Any,
    projection: Projection,
    last_change: dict[tuple[str, str], int],
    index: DecayIndex,
    axes: Any,
    where: str,
) -> None:
    """The full twin sweep: both walks, index-served vs the walk, over
    every probe tick and scope — the answers (ticks, drafts, draft
    ORDER) must be equal."""
    for tick in _PROBE_TICKS:
        for scope in _SCOPES:
            walked = next_decay_tick(
                pack, projection, last_change, tick, locations=scope, axes=axes
            )
            served = next_decay_tick(
                pack, projection, last_change, tick, locations=scope,
                axes=axes, index=index,
            )
            assert walked == served, (
                f"{where}: next_decay_tick twin broke at tick={tick} "
                f"scope={scope}: walk={walked} index={served}"
            )
            walked_drafts = decay_drafts(
                pack, projection, last_change, tick, locations=scope, axes=axes
            )
            served_drafts = decay_drafts(
                pack, projection, last_change, tick, locations=scope,
                axes=axes, index=index,
            )
            assert walked_drafts == served_drafts, (
                f"{where}: decay_drafts twin broke at tick={tick} "
                f"scope={scope}"
            )


# -- the birth law (KI#16: the whole projection, seeds included) ----------------


def test_birth_pool_equals_the_walks_live_set_on_every_committed_pack() -> None:
    """`from_projection` births exactly the LIVE pairs — every (npc,
    axis) the walks' own filters would consider (present, uncaught,
    valued int-not-bool, unpinned), positioned in per-location heaps
    with ``next_fire = base + elapsed_first``. Observed through the
    widest possible probe: a tick past every axis's first fire answers
    the whole live set, in the pack's own NPC declaration order."""
    for name in _PACK_DIRS:
        pack = load_pack(REPO / "content" / name)
        axes = decay_axes(pack)
        if not axes:
            continue  # a pack without decay axes births an empty pool
        projection = initial_projection(pack.entities)
        last_change: dict[tuple[str, str], int] = {}
        index = DecayIndex.from_projection(
            pack, projection, axes, last_change
        )
        # the walk-derived live set (the walks' own filters, verbatim)
        expected: dict[str, set[str]] = {}
        for npc in pack.entities["npcs"]:
            props = projection.get(npc["id"])
            if props is None:
                continue
            if props.get("crime_status") == "caught":
                continue
            for axis in axes:
                current = props.get(axis.prop)
                if not isinstance(current, int) or isinstance(current, bool):
                    continue
                scale = pack.rules["relations"]["scale"]
                if max(scale[0], min(scale[1], current + axis.sign)) == current:
                    continue  # pinned at the bound
                expected.setdefault(npc["id"], set()).add(axis.prop)
        live = index.firing(10**9, None)
        assert live == tuple(
            (npc, frozenset(props)) for npc, props in expected.items()
        ), name


def test_birth_pool_counts_seeded_values_not_zero() -> None:
    """The teeth of the birth law: a hand-seeded projection with an
    unpinned axis answers through the pool — a birth from zero would be
    blind to the pack's declarations (KI#16). The crafted ids are the
    PACK's own (the walks iterate the pack's npc list — a foreign id is
    invisible to both paths by the same law)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    axes = decay_axes(pack)
    projection: Projection = {
        "npc_guard_01": {"position": "loc_tavern", "status.fatigue": 40},
        "npc_barkeep_01": {"position": "loc_tavern", "status.fatigue": 100},
        "npc_guard_02": {"position": "loc_backyard", "status.intoxication": 0},
    }
    last_change: dict[tuple[str, str], int] = {}
    index = DecayIndex.from_projection(pack, projection, axes, last_change)
    assert index.firing(10**9, None) == (
        ("npc_guard_01", frozenset({"status.fatigue"})),
    )
    # the landing: base 0 + elapsed_first 36 — the seeded value decays
    # from run start, exactly the walk's default
    assert index.next_fire(None) == 36
    assert index.next_fire(("loc_backyard",)) is None  # pinned: never fires


# -- the fold twin: after every staleness edge, index == walks ------------------


def test_the_fold_twin_agrees_after_every_staleness_edge() -> None:
    """THE equality law. A scripted sequence exercising every edge the
    commit-path fold meets — applied to a real projection through
    `apply_event`, `last_change` updated and `apply_change` folded in
    the `_commit` order (the base line first, the fold second) — after
    EACH step the index answers what the walks answer on the folded
    projection:

    - a status BIRTH with `from_ = None`;
    - pinning at the TOP bound (fatigue 100 — the axis's own direction)
      and UNPINNING (the meal-style ease);
    - a BOOL value on a live axis (never counts);
    - a STRING value (never counts);
    - a value CLEARED to None;
    - a POSITION move (the heap hop — the old heap's cells must die);
    - the CAUGHT veto and its release;
    - TWO changes to the same prop at the SAME TICK (the duplicate-cell
      coincidence: equal next_fire, the pool must still answer once);
    - a fear pin at the BOTTOM bound (the decay direction's own pin)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    axes = decay_axes(pack)
    projection = initial_projection(pack.entities)
    last_change: dict[tuple[str, str], int] = {}
    index = DecayIndex.from_projection(
        pack, projection, axes, last_change
    )
    # (entity, prop, from_, to_, tick) — from_ always the live value
    # (the seeded initials: guard_01/barkeep_01 fatigue 10, all else 0)
    script: list[tuple[str, str, Any, Any, int]] = [
        ("npc_guard_01", "status.fatigue", 10, 40, 10),
        ("npc_guard_01", "status.fatigue", 40, 100, 20),  # pinned top
        ("npc_guard_01", "status.fatigue", 100, 60, 30),  # unpinned
        ("npc_barkeep_01", "status.intoxication", 0, 50, 40),
        ("npc_barkeep_01", "status.intoxication", 50, True, 50),  # bool
        ("npc_barkeep_01", "status.intoxication", True, "drunk", 60),  # str
        ("npc_barkeep_01", "status.intoxication", "drunk", 70, 70),
        ("npc_barkeep_01", "status.intoxication", 70, None, 80),  # cleared
        ("npc_barkeep_01", "status.intoxication", None, 65, 90),
        ("npc_guard_02", "status.fear", 0, 25, 100),
        ("npc_guard_02", "status.fear", 25, 0, 110),  # pinned bottom
        ("npc_guard_02", "status.fear", 0, 15, 120),  # unpinned
        ("npc_barkeep_01", "position", "loc_tavern", "loc_backyard", 130),
        ("npc_guard_01", "crime_status", None, "caught", 140),  # the veto
        ("npc_guard_01", "crime_status", "caught", "free", 150),  # released
        ("npc_guard_02", "status.fatigue", 0, 20, 150),  # same-tick pair
        ("npc_guard_02", "status.fatigue", 20, 45, 150),  # the duplicate edge
    ]
    for n, (entity, prop, from_, to_, tick) in enumerate(script, start=1):
        record = _record((_change(entity, prop, from_, to_),), n, tick=tick)
        apply_event(projection, record)
        # the _commit order: the base line first, the fold second
        last_change[(entity, prop)] = record.t
        index.apply_change(entity, prop)
        _assert_twins(
            pack, projection, last_change, index, axes,
            f"script line {n} ({entity}.{prop} {from_!r}->{to_!r} @{tick})",
        )


def test_caught_is_the_total_veto_on_every_axis() -> None:
    """A caught NPC never constrains a landing and never drafts — the
    walk's own filter, mirrored by the pool's veto (the crime_status
    fold re-derives nothing while caught, everything on release)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    axes = decay_axes(pack)
    projection: Projection = {
        "npc_guard_01": {"position": "loc_tavern", "status.fatigue": 40},
    }
    last_change: dict[tuple[str, str], int] = {}
    index = DecayIndex.from_projection(pack, projection, axes, last_change)
    assert index.next_fire(None) == 36
    record = _record((_change("npc_guard_01", "crime_status", None, "caught"),), 1, tick=5)
    apply_event(projection, record)
    last_change[("npc_guard_01", "crime_status")] = 5
    index.apply_change("npc_guard_01", "crime_status")
    assert index.next_fire(None) is None
    assert index.firing(10**9, None) == ()
    _assert_twins(pack, projection, last_change, index, axes, "caught")


# -- the no-commit law (the enumeration never consumes) -------------------------


def test_the_enumeration_never_consumes() -> None:
    """`firing` re-pushes every valid cell it pops: a caller that takes
    the drafts and DROPS them (no commit) leaves the pool exactly as it
    was — the same enumeration again, the same landing, the walks still
    twins (the index never assumes the caller's commit discipline)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    axes = decay_axes(pack)
    projection = initial_projection(pack.entities)
    last_change: dict[tuple[str, str], int] = {}
    index = DecayIndex.from_projection(
        pack, projection, axes, last_change
    )
    before_landing = index.next_fire(None)
    first = index.firing(10**9, None)
    assert first  # the seeded world has live pairs
    # dropped on the floor — no commit, no fold
    assert index.firing(10**9, None) == first
    assert index.next_fire(None) == before_landing
    _assert_twins(pack, projection, last_change, index, axes, "no-commit")
    # and the drafts are re-derivable through the walk form untouched
    assert decay_drafts(pack, projection, last_change, 10**9, axes=axes)


# -- the identity gate (bound: the pool; foreign: the walk) ---------------------


def test_the_identity_gate_foreign_projection_keeps_the_walk() -> None:
    """The walks' index branch serves ONLY the exact bound objects: a
    foreign projection — even a content-near copy — gets the WALK. The
    gate is observable through the drafts: the bound pool is empty (its
    NPC pinned), while the foreign copy holds a live pair; passing the
    index alongside the copy must still draft (the walk answered the
    copy, never the stale pool)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    axes = decay_axes(pack)
    bound: Projection = {
        "npc_guard_01": {"position": "loc_tavern", "status.fatigue": 100},  # pinned
    }
    last_change: dict[tuple[str, str], int] = {}
    index = DecayIndex.from_projection(pack, bound, axes, last_change)
    assert index.firing(10**9, None) == ()
    foreign: Projection = {
        "npc_guard_01": {"position": "loc_tavern", "status.fatigue": 50},
    }
    foreign_lc: dict[tuple[str, str], int] = {}
    assert not index.serves(foreign, foreign_lc, axes)
    served = decay_drafts(
        pack, foreign, foreign_lc, 10**9, axes=axes, index=index
    )
    assert len(served) == 1  # the walk answered the foreign view
    assert served[0].target == "npc_guard_01"
    # the axes-table gate too: a fresh resolution is not the bound table
    assert not index.serves(bound, last_change, decay_axes(pack))
    assert not index.serves(bound, last_change, None)


# -- the real-log twin (the end-to-end equality on committed machinery) --------


def _theft_steps() -> list[dict[str, Any]]:
    """The crime chain that moves the decay-relevant state: a theft
    seeds suspicion through the reaction cascade, the wait crosses
    beats and a watch rotation (decay commits fold through
    `apply_change` the while — rotation resets, drift, the moved
    PC)."""
    return [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "wait", "ticks": 760},
    ]


def _assert_pool_agrees_with_a_fresh_birth(sim: Simulator, where: str) -> None:
    """The live (fold-maintained) pool answers what a FRESH birth scan
    answers on the same projection + last_change — the fold and the
    scan are two roads to the same pool (the strongest production
    equality; every committed event since construction rode the fold)."""
    pack = sim._pack
    fresh = DecayIndex.from_projection(
        pack, sim.projection, sim._decay_axes, sim._last_change
    )
    for scope in (None, ("loc_tavern",), ("loc_backyard",), ("loc_cellar",)):
        assert sim._decay_index.next_fire(scope) == fresh.next_fire(scope), (
            f"{where}: pool landing diverged from a fresh birth "
            f"(scope={scope})"
        )
        assert sim._decay_index.firing(10**9, scope) == fresh.firing(
            10**9, scope
        ), f"{where}: pool live set diverged from a fresh birth"


def test_the_real_log_twin_law(tmp_path: Path) -> None:
    """After a real run — the full reaction cascade, beats, a watch
    rotation with its status resets — the Simulator's live pool answers
    what the walks answer on the Simulator's own projection (the
    production path the index exists for), and what a fresh birth scan
    answers (the fold == the scan)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    sim = Simulator(pack, 42, tmp_path / "run.jsonl", SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(_theft_steps()[:2])
    _assert_twins(
        pack, sim.projection, sim._last_change, sim._decay_index,
        sim._decay_axes, "mid-run",
    )
    _assert_pool_agrees_with_a_fresh_birth(sim, "mid-run")
    sim.run_steps(_theft_steps()[2:])
    sim.close()
    _assert_twins(
        pack, sim.projection, sim._last_change, sim._decay_index,
        sim._decay_axes, "drain",
    )
    _assert_pool_agrees_with_a_fresh_birth(sim, "drain")


def test_the_resume_law(tmp_path: Path) -> None:
    """The resume door re-births the pool from the restored projection
    + the folded last_change (the resume-invisible law): a resumed
    session's pool answers what a fresh birth answers and what the
    walks answer — the O(1) path survives the process boundary exactly
    like an uninterrupted run's, and keeps twin through further
    play."""
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
    # the re-birth is bound to the restored live objects
    assert sim2._decay_index.serves(
        sim2.projection, sim2._last_change, sim2._decay_axes
    )
    _assert_pool_agrees_with_a_fresh_birth(sim2, "resumed")
    _assert_twins(
        pack, sim2.projection, sim2._last_change, sim2._decay_index,
        sim2._decay_axes, "resumed",
    )
    sim2.run_steps(_theft_steps()[2:])
    sim2.close()
    _assert_twins(
        pack, sim2.projection, sim2._last_change, sim2._decay_index,
        sim2._decay_axes, "resumed-drain",
    )
    _assert_pool_agrees_with_a_fresh_birth(sim2, "resumed-drain")
