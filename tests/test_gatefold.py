"""iter-382 acceptance — the gate fold: `ScanGateMemo`'s commit-path
twin (the standing order's key-build row, iter-375's honest
remainder). The memo's key comparison moved from the read side to the
write side: the fold watches the declared read pairs on the commit
path (``apply_change`` — the ``apply_event`` twin, popped from
``_commit``), pops every confirmed probe a write could invalidate (the
pop law), and the scans serve the stored verdict in O(1) instead of
rebuilding the key per stretch.

THE SERVE LAW is the equality the laws here falsify: the fold's fast
path serves EXACTLY the verdict the key-compare path would — never
more — under the three O(1) gates (identity: the bound projection
object; declared: the spec's own (probe, pairs) content; stamp: the
memo entry object the fold validated). The laws pin the equality at
birth and after every edge class (the fold twin), at the scan function
level (fresh == memo == memo+fold, the answers AND the dict order),
through the contamination surfaces (a replaced entry, a flushed table,
a foreign projection, a crafted colliding spec), over the faction twin
(crafted pack), on a real log (the province walk — position pairs
folding live), and across a resume (the re-birth law).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.fold import Projection, apply_event, initial_projection
from core.intent import ScanGateFold, ScanGateMemo  # noqa: F401 (laws)
from core.log import EventRecord, StateChange
from core.loop import Simulator
from core.pack import load_pack
from core.rng import RngBank
from core.urgencies import urgency_scan, urgency_specs

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

# The six committed packs — the corpus the serve law sweeps.
_PACK_DIRS = (
    "tavern_pack", "province_pack", "farstead_pack",
    "grim_pack", "pressure_pack", "road_pack",
)

# the scope forms the function-level twins sweep
_SCOPES: tuple[tuple[str, ...] | None, ...] = (
    None,
    ("loc_tavern",),
    ("loc_backyard",),
    ("loc_tavern", "loc_backyard"),
)


def _moved_value(current: Any) -> Any:
    """A type-preserving mutation for the batteries: same type as the
    live value, never equal to it (the key must see the move)."""
    if isinstance(current, str):
        return f"{current}_moved"
    if isinstance(current, bool):
        return not current
    if isinstance(current, int):
        return current + 1000
    if isinstance(current, list):
        return [*current, "moved"]
    return "moved"


def _copy_of(projection: Any) -> Any:
    return {entity: dict(props) for entity, props in projection.items()}


def _fold_of(pack: Any, projection: Projection) -> ScanGateFold:
    """The loop's own birth form over both families."""
    from core.factions import faction_specs

    return ScanGateFold.from_specs(
        (
            (spec.probe.id, spec.pairs)
            for spec in (
                *urgency_specs(pack), *faction_specs(pack)
            )
        ),
        projection,
    )


def _armed(pack: Any, projection: Projection) -> tuple[
    Any, ScanGateMemo, ScanGateFold, RngBank,
]:
    """The loop's own triple over a pack: specs, a bound memo, the
    fold, and the bank the scan arms share."""
    specs = urgency_specs(pack)
    memo = ScanGateMemo(pack, None)
    fold = _fold_of(pack, projection)
    bank = RngBank(7)
    return specs, memo, fold, bank


# -- the birth law (the declared map + the readers inversion) -------------------


def test_birth_declares_the_union_and_inverts_the_readers() -> None:
    """`from_specs` builds exactly the two birth tables: the declared
    map (probe -> its pairs — the content gate's own table) over every
    memoizable spec of BOTH families, and the readers inversion (pair
    -> exactly the probes declaring it). The pairs-None specs (ungated
    or windowed) never enter; an ungated pack births the empty fold
    (the 68a pattern)."""
    from core.factions import faction_specs

    for name in _PACK_DIRS:
        pack = load_pack(REPO / "content" / name)
        projection = initial_projection(pack.entities)
        fold = _fold_of(pack, projection)
        declared = {
            spec.probe.id: spec.pairs
            for spec in (
                *urgency_specs(pack), *faction_specs(pack)
            )
            if spec.pairs is not None
        }
        assert fold._declared == declared, name
        readers: dict[tuple[str, str], list[str]] = {}
        for probe_id, pairs in declared.items():
            for pair in pairs:
                readers.setdefault(pair, []).append(probe_id)
        assert fold._readers == readers, name
        assert fold.serves(projection), name
        # the windowed/ungated fence: a pairs-None spec is nowhere
        for spec in (*urgency_specs(pack), *faction_specs(pack)):
            if spec.pairs is None:
                assert spec.probe.id not in fold._declared, (
                    name, spec.probe.id,
                )


# -- the serve law (the head oracle: fresh == memo == memo+fold) ---------------


def test_the_fold_serves_exactly_the_key_compare_path() -> None:
    """THE equality law, at the scan function level, on every
    committed pack with gated specs and every scope form: the
    memo+fold scan answers EXACTLY the fresh scan (no memo) AND the
    memo-only scan — the answers, the first_fire, AND the streams dict
    insertion order (the collective walk's word sequence rides it).
    Repeated passes pin the warm path (the cold first pass evaluates
    fresh; the warm passes serve)."""
    for name in _PACK_DIRS:
        pack = load_pack(REPO / "content" / name)
        specs = urgency_specs(pack)
        if not any(spec.pairs is not None for spec in specs):
            continue  # the ungated packs ride the other laws
        projection = initial_projection(pack.entities)
        _s, memo, fold, bank = _armed(pack, projection)
        for scope in _SCOPES:
            fresh = urgency_scan(
                pack, projection, bank, locations=scope, specs=specs,
                limit=400,
            )
            memoized = urgency_scan(
                pack, projection, bank, locations=scope, specs=specs,
                limit=400, gate_memo=memo,
            )
            folded = urgency_scan(
                pack, projection, bank, locations=scope, specs=specs,
                limit=400, gate_memo=memo, gate_fold=fold,
            )
            assert fresh == memoized == folded, (name, scope)
            assert list(fresh[0]) == list(folded[0]), (name, scope)
        # the warm fold actually SERVES (the fast path is live, not a
        # fallthrough to the key compare on every call), and every
        # confirmed record carries the spec's OWN declared pairs
        assert fold._confirmed, name
        by_id = {spec.probe.id: spec for spec in specs}
        for probe_id, record in fold._confirmed.items():
            assert record[0] == by_id[probe_id].pairs, (name, probe_id)


def test_the_mutation_battery_inside_and_outside() -> None:
    """The twin-agreement battery over the BOUND projection (the
    honest production path: apply_event + the fold in the _commit
    order): mutations OUTSIDE every declared pair never move the
    folded answers and never pop (the confirmed set holds); mutations
    INSIDE a declared pair pop exactly the reading probes and the
    next scan re-derives (the answers move exactly when the fresh
    evaluation moves)."""
    pack = load_pack(REPO / "content" / "farstead_pack")
    specs = urgency_specs(pack)
    projection = initial_projection(pack.entities)
    _s, memo, fold, bank = _armed(pack, projection)
    read_pairs = {pair for spec in specs for pair in spec.pairs or ()}

    def folded() -> Any:
        return urgency_scan(
            pack, projection, bank, specs=specs, limit=400,
            gate_memo=memo, gate_fold=fold,
        )

    def fresh() -> Any:
        return urgency_scan(pack, projection, bank, specs=specs, limit=400)

    def commit(
        entity: str, prop: str, from_: Any, to_: Any, n: int
    ) -> None:
        record = EventRecord(
            id=f"ev_{n:04d}", t=10 + n, type="test_event", actor="pc_01",
            cause=None, outcome={}, knowledge=(), hooks=(),
            importance="low", provenance={}, target=None,
            state_changes=(
                StateChange(entity=entity, prop=prop, from_=from_, to_=to_),
            ),
        )
        apply_event(projection, record)  # apply, then fold (_commit)
        fold.apply_change(entity, prop)

    assert folded() == fresh()
    warm = dict(fold._confirmed)
    # OUTSIDE: a non-declared pair's write pops nothing, answers hold
    outside = sorted(
        (entity, prop)
        for entity, props in projection.items()
        for prop in props
        if (entity, prop) not in read_pairs
    )
    assert outside
    for n, (entity, prop) in enumerate(outside[:5]):
        current = projection[entity][prop]
        commit(entity, prop, current, _moved_value(current), n)
        assert folded() == fresh(), (entity, prop)
    assert fold._confirmed == warm  # no pop fired

    # INSIDE: every declared pair the battery reaches pops its
    # readers and re-derives — the equality holds after each
    for n, (entity, prop) in enumerate(sorted(read_pairs)[:8]):
        current = projection[entity].get(prop)
        commit(entity, prop, current, _moved_value(current), 100 + n)
        assert folded() == fresh(), (entity, prop)
    # the flip-back on a declared pair (the conservative pop's cost:
    # one wasted build, never a wrong answer — the key compare
    # re-hits the restored values and the fold re-confirms)
    entity, prop = sorted(read_pairs)[0]
    moved = projection[entity][prop]
    base = _moved_value(moved)  # flip to a fresh value, then back
    commit(entity, prop, moved, base, 200)
    assert folded() == fresh()
    commit(entity, prop, base, moved, 201)
    assert folded() == fresh()
    assert fold._confirmed  # re-confirmed after the flip-back


# -- the fold twin after every edge class (the scripted battery) ----------------


def _record(changes: tuple[StateChange, ...], n: int) -> EventRecord:
    return EventRecord(
        id=f"ev_{n:04d}", t=n, type="test_event", actor="pc_01",
        cause=None, outcome={}, knowledge=(), hooks=(),
        importance="low", provenance={}, target=None,
        state_changes=changes,
    )


def test_the_fold_twin_after_every_edge() -> None:
    """A scripted sequence driving the BOUND projection through every
    edge the commit-path fold meets — applied via `apply_event`, the
    fold called per change in the `_commit` order — after EACH step
    the memo+fold scan answers EXACTLY the fresh scan:

    - a declared-pair write (the pop + the re-derivation);
    - a NON-declared write (no pop, the answers hold);
    - a write landing on the SAME value (the no-op edge — the pop
      fires, the key compare re-hits, one wasted build);
    - the flip-back (value restored — the same law, served again);
    - a POSITION move on a gated spec's NPC (province's own form);
    - two declared-pair writes in ONE event (both folds, both pops);
    - a declared pair on an entity whose prop was ABSENT (the None
      read becomes a value — the absence cache law's write side)."""
    pack = load_pack(REPO / "content" / "farstead_pack")
    specs = urgency_specs(pack)
    projection = initial_projection(pack.entities)
    _s, memo, fold, bank = _armed(pack, projection)
    read_pairs = sorted({p for spec in specs for p in spec.pairs or ()})
    entity, prop = read_pairs[0]
    other_e, other_p = read_pairs[1] if len(read_pairs) > 1 else (entity, prop)
    base = projection[entity].get(prop)

    def twins(where: str) -> None:
        fresh = urgency_scan(
            pack, projection, bank, specs=specs, limit=400
        )
        folded = urgency_scan(
            pack, projection, bank, specs=specs, limit=400,
            gate_memo=memo, gate_fold=fold,
        )
        assert fresh == folded, where
        assert list(fresh[0]) == list(folded[0]), where

    def step(changes: tuple[StateChange, ...], where: str) -> None:
        record = _record(changes, step.n)
        apply_event(projection, record)
        for change in changes:  # the _commit order: apply, then fold
            fold.apply_change(change.entity, change.prop)
        twins(where)
        step.n += 1

    step.n = 1
    step((StateChange(entity, prop, base, _moved_value(base)),), "the move")
    step(
        (StateChange("loc_square", "flags.any", None, "x"),),
        "a non-declared write (no pop)",
    )
    step(
        (StateChange(entity, prop, _moved_value(base), _moved_value(base)),),
        "the same-value write (the no-op edge)",
    )
    step((StateChange(entity, prop, _moved_value(base), base),), "the flip-back")
    step((
        StateChange(entity, prop, base, _moved_value(base)),
        StateChange(other_e, other_p,
                    projection[other_e].get(other_p),
                    _moved_value(projection[other_e].get(other_p))),
    ), "two declared writes in one event")

    # the ABSENCE edge (the None-read write side, driven at the
    # fold's own level): a fold declared over a pair the seed never
    # carried pops on the write that CREATES it — the fold tracks
    # change times, never values, so an absent pair is no special
    # case (iter-375's honest-absence law, the write-side twin)
    absent_prop = f"{prop}_absent_edge"
    absent_fold = ScanGateFold.from_specs(
        (("probe_absent", ((entity, absent_prop),)),), projection,
    )
    absent_fold.confirm(
        "probe_absent", ((entity, absent_prop),), object()
    )
    assert absent_fold.confirmed(
        "probe_absent", ((entity, absent_prop),),
        next(iter(absent_fold._confirmed.values()))[1],
    )
    absent_fold.apply_change(entity, absent_prop)  # the creation write
    assert "probe_absent" not in absent_fold._confirmed  # popped


# -- the contamination surfaces (the three gates' teeth) -----------------------


def test_the_stamp_gate_a_replaced_entry_is_never_served() -> None:
    """The stamp law's falsifier: after a confirmed pass, a colliding
    store under the same probe id (a foreign key — the pathological
    caller that overwrites the memo entry) must NOT be served by the
    fold — the entry object moved, the identity compare fails, the
    key-compare path runs, and the scan's answer equals the fresh
    evaluation. The memo's own flush (bind) answers the same way (no
    live entry -> the None guard -> the slow path)."""
    pack = load_pack(REPO / "content" / "farstead_pack")
    specs = urgency_specs(pack)
    projection = initial_projection(pack.entities)
    _s, memo, fold, bank = _armed(pack, projection)

    def folded() -> Any:
        return urgency_scan(
            pack, projection, bank, specs=specs, limit=400,
            gate_memo=memo, gate_fold=fold,
        )

    def fresh() -> Any:
        return urgency_scan(pack, projection, bank, specs=specs, limit=400)

    assert folded() == fresh()
    assert fold._confirmed
    # the contamination: overwrite a real probe's entry with a
    # FOREIGN key + verdict (the crafted-caller simulation)
    probe_id = next(iter(fold._confirmed))
    memo.store(probe_id, ("crafted",), False)
    assert folded() == fresh()  # the stamp gate refused the replacement
    # the flush surface: a foreign (pack, world) bind empties the
    # table — the answer()-None guard falls to the key compare
    memo.bind(pack, object())  # identity only — never dereferenced
    assert folded() == fresh()
    # and the fold re-fills: a pass after the flush confirms again
    assert folded() == fresh()
    assert fold._confirmed


def test_the_identity_gate_and_the_purity_law() -> None:
    """The identity gate: a foreign projection (even a content-near
    copy) is never served — the scan answers through the key compare
    (the memo's own law, the fold must not corrupt it). The PURITY
    law: a fresh parse of the specs (specs=None — the scan re-parses
    inside) IS served — the parse is content-identical, the declared
    gate matches content, not object identity."""
    pack = load_pack(REPO / "content" / "farstead_pack")
    specs = urgency_specs(pack)
    projection = initial_projection(pack.entities)
    _s, memo, fold, bank = _armed(pack, projection)
    foreign = _copy_of(projection)
    for _entity, props in foreign.items():
        if "position" in props:
            props["position"] = "loc_square_moved"
    assert fold.serves(projection)
    assert not fold.serves(foreign)
    # the foreign scan: memo + fold passed, the predicate + the key
    # compare answer (never the fold's bound state)
    fresh = urgency_scan(
        pack, foreign, bank, specs=specs, limit=400
    )
    served = urgency_scan(
        pack, foreign, bank, specs=specs, limit=400,
        gate_memo=memo, gate_fold=fold,
    )
    assert fresh == served
    # the purity law: the fresh parse (specs=None) is served — the
    # fold's declared gate matches CONTENT
    parsed = urgency_scan(
        pack, projection, bank, limit=400, gate_memo=memo, gate_fold=fold,
    )
    assert parsed == urgency_scan(
        pack, projection, bank, specs=specs, limit=400,
        gate_memo=memo, gate_fold=fold,
    )


def test_the_declared_gate_a_crafted_colliding_spec_never_confirms() -> None:
    """The declared gate's falsifier: a crafted spec with a REAL
    probe's id but DIFFERENT pairs (the colliding-caller simulation)
    never confirms — its stores stay the key-compare path's problem,
    never the fast path's. The real spec's next pass re-derives and
    re-confirms its OWN entry."""
    pack = load_pack(REPO / "content" / "farstead_pack")
    specs = urgency_specs(pack)
    projection = initial_projection(pack.entities)
    _s, memo, fold, bank = _armed(pack, projection)
    real = next(s for s in specs if s.pairs is not None)
    # the crafted twin: same id, different pairs (a pair NO real spec
    # declares — the mutation the crafted caller would key on)
    crafted_pairs = (("loc_workshop", "position"),)
    assert crafted_pairs != real.pairs
    assert crafted_pairs[0] not in fold._readers
    # confirm() refuses the crafted content (the declared gate)
    fold.confirm(real.probe.id, crafted_pairs, object())
    assert not fold.confirmed(real.probe.id, crafted_pairs, object())
    # ...and confirmed() refuses it even against a recorded real entry
    entry = memo.entry_at(real.probe.id)
    fold.confirm(real.probe.id, real.pairs, entry)
    assert fold.confirmed(real.probe.id, real.pairs, entry)
    assert not fold.confirmed(real.probe.id, crafted_pairs, entry)


# -- the faction twin (the crafted gated pack) ---------------------------------


def test_the_faction_twin_on_the_crafted_pack(tmp_path: Path) -> None:
    """The family's other arm: the crafted gated faction pack (the
    iter-375 faction law's own fixture) — the fold serves the faction
    scan exactly as the key compare would, over the inside/outside
    mutations (the group walks to the guard — a declared pair moved)."""
    import sys

    tests_dir = str(REPO / "tests")
    if tests_dir not in sys.path:
        sys.path.insert(0, tests_dir)
    from test_factions import ARMED_ENTRY, MEMBERS, crafted_pack  # noqa: E402

    from core.factions import faction_scan, faction_specs  # noqa: E402

    gated_entry = {
        **ARMED_ENTRY,
        "intent": {"kind": "muster", "target": "npc_guard_01"},
        "requires": [
            {"noun": "actor", "test": "same_location", "with": "target"},
        ],
    }
    _dir, pack = crafted_pack(
        tmp_path, "gate_fold", entries=[gated_entry], fears=(80, 70),
    )
    specs = faction_specs(pack)
    spec = next(s for s in specs if s.pairs is not None)
    projection = initial_projection(pack.entities)
    memo = ScanGateMemo(pack, None)
    fold = ScanGateFold.from_specs(
        ((s.probe.id, s.pairs) for s in specs), projection,
    )
    bank = RngBank(7)

    def fresh(proj: Any) -> Any:
        return faction_scan(pack, proj, bank, specs=specs, limit=400)

    def folded(proj: Any) -> Any:
        return faction_scan(
            pack, proj, bank, specs=specs, limit=400,
            gate_memo=memo, gate_fold=fold,
        )

    assert folded(projection) == fresh(projection)
    assert fold._confirmed  # the faction arm actually serves
    # the INSIDE mutation: the group walks to the guard
    moved = _copy_of(projection)
    moved[spec.group]["position"] = moved[MEMBERS[0]]["position"]
    # (a copy is foreign — the key-compare answers; the bound pop is
    # driven through apply_change on the bound object below)
    assert folded(moved) == fresh(moved)
    # the bound-side pop: the same move on the BOUND projection
    record = _record(
        (StateChange(
            spec.group, "position",
            projection[spec.group].get("position"),
            moved[spec.group]["position"],
        ),),
        1,
    )
    apply_event(projection, record)
    fold.apply_change(spec.group, "position")
    assert folded(projection) == fresh(projection)
    assert fold._confirmed  # re-confirmed after the re-derivation


# -- the real-log twin (the province walk — position pairs folding live) -------


def _province_steps() -> list[dict[str, Any]]:
    return [
        {"intent": "move", "target": "loc_weirstair"},
        {"intent": "wait", "ticks": 30},
        {"intent": "move", "target": "loc_riverroad"},
        {"intent": "wait", "ticks": 15},
        {"intent": "move", "target": "loc_keep"},
        {"intent": "move", "target": "loc_malby"},
        {"intent": "wait", "ticks": 600},
    ]


def test_the_real_log_twin(tmp_path: Path) -> None:
    """After a real province run — autonomous moves folding through
    the commit path (province's declared pairs are POSITION pairs: the
    p=100 walker pops the readers live), beats, the market and watch
    machinery — the Simulator's live fold answers what a fresh
    evaluation answers on the Simulator's own projection (the
    production path the fold exists for), mid-run and at the drain."""
    pack = load_pack(REPO / "content" / "province_pack")
    sim = Simulator(
        pack, 42, tmp_path / "run.jsonl", SCHEMA, commit="0000000"
    )
    sim.open()
    specs = sim._urgency_specs
    memo, fold = sim._gate_memo, sim._gate_fold

    def twins(where: str) -> None:
        for scope in (None, ("loc_malby",), ("loc_weirstair",)):
            fresh = urgency_scan(
                pack, sim.projection, sim._bank,
                locations=scope, specs=specs, limit=50,
            )
            folded = urgency_scan(
                pack, sim.projection, sim._bank,
                locations=scope, specs=specs, limit=50,
                gate_memo=memo, gate_fold=fold,
            )
            assert fresh == folded, (where, scope)
            assert list(fresh[0]) == list(folded[0]), (where, scope)

    sim.run_steps(_province_steps()[:4])
    assert fold.serves(sim.projection)
    twins("mid-run")
    sim.run_steps(_province_steps()[4:])
    sim.close()
    twins("drain")
    # the live fold actually served along the way (the province's
    # gated specs confirmed at least once after the moves)
    assert fold._confirmed


def test_the_resume_law(tmp_path: Path) -> None:
    """The resume door re-births the fold on the restored projection
    (the resume-invisible law): the re-born fold serves the restored
    object, a post-resume scan equals the fresh evaluation, and the
    twin holds through further play (the cold memo re-fills on the
    first pass, exactly like an uninterrupted run's)."""
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
    assert sim2._gate_fold.serves(sim2.projection)  # the re-birth
    specs = sim2._urgency_specs

    def twins(where: str) -> None:
        fresh = urgency_scan(
            pack, sim2.projection, sim2._bank, specs=specs, limit=50
        )
        folded = urgency_scan(
            pack, sim2.projection, sim2._bank, specs=specs, limit=50,
            gate_memo=sim2._gate_memo, gate_fold=sim2._gate_fold,
        )
        assert fresh == folded, where

    twins("resumed")
    sim2.run_steps(_province_steps()[4:])
    sim2.close()
    twins("resumed-drain")
