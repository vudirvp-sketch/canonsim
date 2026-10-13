"""iter-381 acceptance — the rolling-set index (the iter-362 class
applied to the urgency family's per-spec filter walk): per-LOCATION
buckets of ``(spec_position, spec)`` pairs over the present,
positioned, uncaught NPCs — `urgency_rolls`'s own answers, pre-folded
on the commit path, read by the scans and the beat walk for the BOUND
objects only (the identity gate).

The laws here pin the EQUALITY the index is built on — the predicate
stays the semantic owner (D-024); the buckets must answer exactly
what the predicate answers at birth, after any committed sequence of
verdict edges (the exactness law: every verdict mover — position,
caught — rides a committed event, and the fold re-derives the
entity's membership from the live state, so the answer is exact under
ANY in-event change order), across a resume, at the scan/walk function
level (the draw-order law — the counter words ride the iteration
order), and only for the bound objects.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.fold import Projection, apply_event, initial_projection
from core.log import EventRecord, StateChange
from core.loop import Simulator
from core.pack import load_pack
from core.rng import RngBank
from core.urgencies import (
    RollIndex,
    urgency_intents,
    urgency_rolls,
    urgency_scan,
    urgency_specs,
)

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

# the scope forms the twin laws sweep: the one-scene None, every
# single location of the tavern world, and the multi-location warm-ring
# form
_SCOPES: tuple[tuple[str, ...] | None, ...] = (
    None,
    ("loc_tavern",),
    ("loc_backyard",),
    ("loc_cellar",),
    ("loc_tavern", "loc_backyard"),
    ("loc_backyard", "loc_tavern"),  # the order-insensitivity law
    ("loc_tavern", "loc_cellar", "loc_backyard"),
)


def _change(entity: str, prop: str, from_: Any, to_: Any) -> StateChange:
    return StateChange(entity=entity, prop=prop, from_=from_, to_=to_)


def _record(
    changes: tuple[StateChange, ...], n: int, tick: int | None = None
) -> EventRecord:
    return EventRecord(
        id=f"ev_{n:04d}", t=n if tick is None else tick, type="test_event",
        actor="pc_01", cause=None, outcome={}, knowledge=(),
        state_changes=changes, hooks=(), importance="low", provenance={},
        target=None,
    )


def _expected(
    specs: Any, projection: Projection, locations: Any
) -> list[tuple[int, Any]]:
    """The predicate's own answers, in the filter form's iteration
    order (the pack order) — the twins' reference."""
    return [
        (idx, spec)
        for idx, spec in enumerate(specs)
        if urgency_rolls(spec, projection, locations)
    ]


def _assert_twins(
    specs: Any, projection: Projection, index: RollIndex, where: str
) -> None:
    """The full twin sweep: the index's rolling vs the predicate, over
    every scope form — the answers (spec set AND order) must be
    equal."""
    for scope in _SCOPES:
        served = list(index.rolling(scope))
        assert served == _expected(specs, projection, scope), (
            f"{where}: rolling twin broke at scope={scope}: "
            f"index={served} predicate={_expected(specs, projection, scope)}"
        )


# -- the birth law (KI#16: the whole projection, seeds included) ----------------


def test_birth_equals_the_filter_on_every_committed_pack() -> None:
    """`from_projection` births exactly the predicate's answers — every
    present, uncaught NPC's specs land in its position's bucket, in
    the filter form's own iteration order, on every committed pack and
    every scope form."""
    for name in _PACK_DIRS:
        pack = load_pack(REPO / "content" / name)
        specs = urgency_specs(pack)
        if not specs:
            continue  # a pack without urgency entries births empty buckets
        projection = initial_projection(pack.entities)
        index = RollIndex.from_projection(specs, projection)
        assert index.serves(projection, specs), name
        _assert_twins(specs, projection, index, f"birth:{name}")
        # the multi-spec npc (two entries, two streams): both land
        for npc, idxs in index._spec_idxs.items():
            if len(idxs) > 1:
                for scope in _SCOPES:
                    served = [i for i, _ in index.rolling(scope)]
                    assert all(
                        idx in served
                        for idx in idxs
                        if urgency_rolls(specs[idx], projection, scope)
                    ), (name, npc, scope)


def test_birth_skips_the_caught_and_reads_the_seeds() -> None:
    """The teeth of the birth law: a hand-seeded projection places the
    uncaught specs at their seeded positions and skips the caught
    (the whole-projection law — a birth from the pack's declaration
    list alone would be blind to the seeded state, KI#16)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    specs = urgency_specs(pack)
    projection: Projection = {
        "npc_guard_01": {"position": "loc_tavern"},
        "npc_guard_02": {"position": "loc_backyard", "crime_status": "caught"},
        "npc_maid_01": {"position": "loc_cellar"},
    }
    index = RollIndex.from_projection(specs, projection)
    # guard_01's look_around lands; guard_02's TWO specs are vetoed;
    # maid_01's wait lands at the cellar
    assert list(index.rolling(None)) == _expected(specs, projection, None)
    assert [i for i, _ in index.rolling(("loc_backyard",))] == []
    assert [s.intent_kind for _, s in index.rolling(("loc_tavern",))] == [
        "look_around"
    ]
    assert [s.intent_kind for _, s in index.rolling(("loc_cellar",))] == [
        "wait"
    ]


# -- the fold twin: after every verdict edge, index == predicate ----------------


def test_the_fold_twin_agrees_after_every_verdict_edge() -> None:
    """THE equality law. A scripted sequence exercising every edge the
    commit-path fold meets — applied to a real projection through
    `apply_event`, the fold called per change in the `_commit` order
    (after the apply) — after EACH step the index answers what the
    predicate answers on the folded projection:

    - a POSITION move (the bucket hop — the old bucket must lose the
      specs);
    - a move BACK (the return hop);
    - a same-position change (the no-op edge);
    - the CAUGHT veto (BOTH of a multi-spec NPC's entries leave) and
      its release (both return);
    - a non-caught crime_status change (suspected — membership
      unchanged);
    - a POSITION + CAUGHT pair in ONE event, BOTH orders (the live
      read is the final state — the re-derivation is order-immune);
    - TWO position changes in one event (the intermediate placement
      cleaned by the second fold call);
    - caught -> free -> caught in one event (the double flip);
    - a position CLEARED to None (the None bucket — still rolling in
      the one-scene scope, filtered from every located scope)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    specs = urgency_specs(pack)
    projection = initial_projection(pack.entities)
    index = RollIndex.from_projection(specs, projection)
    # (changes, tick) — from_ always the live value (the seeded
    # initials: the drunks at the tavern, guards on rotation posts)
    script: list[tuple[tuple[StateChange, ...], int]] = [
        ((_change("npc_guard_01", "position", "loc_tavern", "loc_backyard"),), 10),
        ((_change("npc_guard_01", "position", "loc_backyard", "loc_tavern"),), 20),
        ((_change("npc_guard_01", "position", "loc_tavern", "loc_tavern"),), 30),
        ((_change("npc_guard_02", "crime_status", None, "caught"),), 40),
        ((_change("npc_guard_02", "crime_status", "caught", "free"),), 50),
        ((_change("npc_maid_01", "crime_status", None, "suspected"),), 60),
        # position + caught in one event, position first
        ((
            _change("npc_drunk_01", "position", "loc_tavern", "loc_cellar"),
            _change("npc_drunk_01", "crime_status", None, "caught"),
        ), 70),
        # caught + position in one event, caught first
        ((
            _change("npc_maid_01", "crime_status", "suspected", "caught"),
            _change("npc_maid_01", "position", "loc_tavern", "loc_backyard"),
        ), 80),
        # two position changes in one event
        ((
            _change("npc_guard_01", "position", "loc_tavern", "loc_backyard"),
            _change("npc_guard_01", "position", "loc_backyard", "loc_cellar"),
        ), 90),
        # the release + the double flip back to caught in one event
        ((
            _change("npc_drunk_01", "crime_status", "caught", "free"),
            _change("npc_drunk_01", "crime_status", "free", "caught"),
        ), 100),
        # a position cleared to None — the drunk RELEASED first (the
        # caught never roll: the probe below needs a rolling drunk)
        ((_change("npc_drunk_01", "crime_status", "caught", "free"),), 110),
        ((_change("npc_drunk_01", "position", "loc_cellar", None),), 120),
    ]
    for n, (changes, tick) in enumerate(script, start=1):
        record = _record(changes, n, tick=tick)
        apply_event(projection, record)
        for change in changes:  # the _commit order: the apply, then the fold
            index.apply_change(change.entity, change.prop)
        _assert_twins(
            specs, projection, index,
            f"script line {n} ({changes[0].entity}.{changes[0].prop})",
        )
    # the None-position law: the drunk still rolls in the one-scene
    # scope, never in a located one
    assert any(
        spec.npc == "npc_drunk_01" for _, spec in index.rolling(None)
    )
    assert not any(
        spec.npc == "npc_drunk_01" for _, spec in index.rolling(("loc_tavern",))
    )


def test_the_fold_ignores_non_verdict_props_and_foreign_entities() -> None:
    """Only `position` and `crime_status` move a verdict; a status
    axis change on a spec NPC and ANY change on a non-spec entity are
    no-ops (the fold returns before touching a bucket)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    specs = urgency_specs(pack)
    projection = initial_projection(pack.entities)
    index = RollIndex.from_projection(specs, projection)
    before = list(index.rolling(None))
    for entity, prop in (
        ("npc_guard_01", "status.fatigue"),
        ("pc_01", "position"),  # not a spec npc
        ("loc_tavern", "flags.any"),  # a location, never a spec npc
    ):
        index.apply_change(entity, prop)
    assert list(index.rolling(None)) == before


# -- the function-level twins (the scan and the walk) ---------------------------


def test_the_scan_twin_at_the_function_level() -> None:
    """`urgency_scan` with the index == the scan without it, on every
    scope form: the streams dict, the first_fire offset — the answers
    AND the dict insertion order (the collective walk's word sequence
    rides it)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    specs = urgency_specs(pack)
    projection = initial_projection(pack.entities)
    index = RollIndex.from_projection(specs, projection)
    bank = RngBank(42)
    for scope in _SCOPES:
        walked = urgency_scan(
            pack, projection, bank, locations=scope, specs=specs, limit=50
        )
        served = urgency_scan(
            pack, projection, bank, locations=scope, specs=specs, limit=50,
            roll_index=index,
        )
        assert walked == served, f"scan twin broke at scope={scope}"
        # the dict ORDER too — the collective walk reads insertion order
        assert list(walked[0]) == list(served[0]), (
            f"scan stream order broke at scope={scope}"
        )


def test_the_walk_twin_and_the_draw_order_law() -> None:
    """`urgency_intents` with the index == the walk without it, on two
    fresh same-seed banks: the intents AND the bank fingerprints equal
    — the per-beat draw sequence (each entry's own stream, the counter
    words) is identical, the canon-order law (the pack order is the
    bucket order)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    specs = urgency_specs(pack)
    projection = initial_projection(pack.entities)
    index = RollIndex.from_projection(specs, projection)
    for scope in _SCOPES:
        bank_a = RngBank(42)
        bank_b = RngBank(42)
        walked = urgency_intents(
            pack, projection, bank_a, locations=scope, specs=specs
        )
        served = urgency_intents(
            pack, projection, bank_b, locations=scope, specs=specs,
            roll_index=index,
        )
        assert walked == served, f"walk twin broke at scope={scope}"
        # the per-stream counter positions too — the draw sequence
        # (each entry's own stream) is the canon-order law's own read
        # (never-assured streams sit at 0 — the counter table's own
        # law, .get the honest read)
        for spec in specs:
            assert bank_a._counts.get(spec.stream, 0) == bank_b._counts.get(
                spec.stream, 0
            ), (
                f"the draw sequence diverged at scope={scope} on "
                f"{spec.stream} — the canon-order law"
            )
        assert bank_a.fingerprint == bank_b.fingerprint


# -- the identity gate (bound: the buckets; foreign: the predicate) --------------


def test_the_identity_gate_foreign_objects_keep_the_predicate() -> None:
    """The scans' index branch serves ONLY the exact bound objects: a
    foreign projection — even a content-near copy — or a fresh parse
    of the specs (a different tuple object) gets the PREDICATE. The
    gate is observable through the walk: the bound buckets hold the
    tavern set, the foreign copy holds a different set; passing the
    index alongside the copy must answer the COPY (the predicate
    answered, never the stale buckets)."""
    pack = load_pack(REPO / "content" / "tavern_pack")
    specs = urgency_specs(pack)
    bound = initial_projection(pack.entities)
    index = RollIndex.from_projection(specs, bound)
    assert index.serves(bound, specs)
    assert not index.serves(bound, None)
    assert not index.serves(bound, urgency_specs(pack))  # a fresh tuple
    foreign: Projection = {
        entity: dict(props) for entity, props in bound.items()
    }
    for npc in pack.entities["npcs"]:
        foreign[npc["id"]]["position"] = "loc_cellar"  # the moved copy
    assert not index.serves(foreign, specs)
    # the observable: the walk on the foreign projection answers the
    # foreign view (the cellar), never the bound buckets
    bank_a = RngBank(7)
    bank_b = RngBank(7)
    walked = urgency_intents(
        pack, foreign, bank_a, locations=("loc_cellar",), specs=specs
    )
    served = urgency_intents(
        pack, foreign, bank_b, locations=("loc_cellar",), specs=specs,
        roll_index=index,
    )
    assert walked == served  # the predicate answered both
    assert walked, "the foreign cellar view rolls — the gate test's teeth"


# -- the real-log twin (the end-to-end equality on committed machinery) --------


def _province_steps() -> list[dict[str, Any]]:
    """The province walk: PC moves + waits that cross beats — the
    autonomous move urgencies fire (the p=100 mover), position
    changes fold through `apply_change` live, the watch and market
    machinery commits. The strongest production path for a fold that
    must track REAL movement."""
    return [
        {"intent": "move", "target": "loc_weirstair"},
        {"intent": "wait", "ticks": 30},
        {"intent": "move", "target": "loc_riverroad"},
        {"intent": "wait", "ticks": 15},
        {"intent": "move", "target": "loc_keep"},
        {"intent": "move", "target": "loc_malby"},
        {"intent": "wait", "ticks": 600},
    ]


def _assert_live_index_agrees_with_a_fresh_birth(sim: Simulator, where: str) -> None:
    """The live (fold-maintained) buckets answer what a FRESH birth
    scan answers on the same projection — the fold and the scan are
    two roads to the same buckets (every committed event since
    construction rode the fold)."""
    fresh = RollIndex.from_projection(sim._urgency_specs, sim.projection)
    for scope in (None, ("loc_malby",), ("loc_keep",), ("loc_weirstair",)):
        assert list(sim._roll_index.rolling(scope)) == list(
            fresh.rolling(scope)
        ), f"{where}: live buckets diverged from a fresh birth (scope={scope})"


def test_the_real_log_twin_law(tmp_path: Path) -> None:
    """After a real province run — autonomous moves folding through
    the commit path, beats, the market and watch machinery — the
    Simulator's live index answers what the predicate answers on the
    Simulator's own projection (the production path the index exists
    for), and what a fresh birth scan answers (the fold == the
    scan)."""
    pack = load_pack(REPO / "content" / "province_pack")
    sim = Simulator(pack, 42, tmp_path / "run.jsonl", SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(_province_steps()[:4])
    _assert_twins(
        sim._urgency_specs, sim.projection, sim._roll_index, "mid-run"
    )
    _assert_live_index_agrees_with_a_fresh_birth(sim, "mid-run")
    sim.run_steps(_province_steps()[4:])
    sim.close()
    _assert_twins(
        sim._urgency_specs, sim.projection, sim._roll_index, "drain"
    )
    _assert_live_index_agrees_with_a_fresh_birth(sim, "drain")


def test_the_resume_law(tmp_path: Path) -> None:
    """The resume door re-births the buckets from the restored
    projection (the resume-invisible law): a resumed session's index
    answers what a fresh birth answers and what the predicate answers
    — the bucket path survives the process boundary exactly like an
    uninterrupted run's, and keeps twin through further play."""
    from core.cursor import cursor_path, load_cursor, save_cursor

    pack = load_pack(REPO / "content" / "province_pack")
    log = tmp_path / "split.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(_province_steps()[:4])
    cursor = sim.export_cursor(director_enabled=True)
    sim.close()
    save_cursor(cursor_path(log), cursor)
    sim2 = Simulator.resume(
        pack, log, SCHEMA, load_cursor(cursor_path(log))
    )
    # the re-birth is bound to the restored live objects
    assert sim2._roll_index.serves(sim2.projection, sim2._urgency_specs)
    _assert_live_index_agrees_with_a_fresh_birth(sim2, "resumed")
    _assert_twins(
        sim2._urgency_specs, sim2.projection, sim2._roll_index, "resumed"
    )
    sim2.run_steps(_province_steps()[4:])
    sim2.close()
    _assert_twins(
        sim2._urgency_specs, sim2.projection, sim2._roll_index,
        "resumed-drain",
    )
    _assert_live_index_agrees_with_a_fresh_birth(sim2, "resumed-drain")
