"""lab-composite-1, first landing — THE COMPOSITE/METAMORPHIC
BATTERY over the density envelope: boundary surgery made executable
(TEST_PLAN §9.2's vocabulary-only row, its live owner named in the
registry by this same iteration).

THE RELATION the battery falsifies (§9.2's own words): perturb
just-outside vs just-inside a DECLARED dependency boundary — OUTSIDE
CANNOT CHANGE THE RESULT. The declared boundaries are read from the
structures' own declarations, never rebuilt test-side (D-024 — the
manifest law):

  * the GATE FOLD's boundary — the pack's own declared read pairs
    (the memoizable specs' `pairs`, the only boundary that is
    literally pack data; the fold's `_declared` table is checked
    against the specs' own enumeration);
  * the ROLL INDEX's boundary — the verdict movers
    (`position`, `crime_status`);
  * the DECAY INDEX's boundary — the decay-axis props (the pack's
    axis table) + the scope carriers (position/crime_status).

THE WORKLOAD is the density envelope's own axes (the row's law):
three materialized profiles — the density-1 form, the households
(warm-ring) axis, and the cold-volume + relation-web + sampled-family
axes — each a REAL 1y run on the real Simulator (the living world's
own committed events fold the structures through the production
commit path before any surgery).

THE SURGERY rides the exact `_commit` fold-order excerpt for the
verified family — `apply_event`, then per state change:
`_last_change` write → decay fold → roll fold → gate fold
(core/loop.py's own order). The log writer, the OCC attribution
index, the knowledge view, and the reactions are deliberately NOT
driven: those halves are owned by their own laws (test_occidx, the
knowledge suites, the reaction suites) and the surgery is read-side
verification on a drained disposable run — the canon path is never
touched (INV-1).

THE LAWS (each the composite relation at the envelope scale — the
per-edge verdict twins stay owned by test_gatefold/test_rollidx/
test_decayidx; what is NEW here is the cross-structure
discrimination, the cross-unit locality, and the real-run workload):

 1. THE MANIFEST LAW — the surgery boundary enumerates from the
    pack's own structures (the fold's declared table == the specs'
    own pairs, unit-namespaced per the scaffold's law), and the
    surgery classes are non-vacuous (outside-manifest pairs and
    gate-only inside pairs both exist — the battery has teeth).
 2. THE JUST-OUTSIDE LAW — surgeries outside EVERY declared
    boundary move NOTHING: no fold pop, the roll buckets unchanged,
    the decay answers unchanged, the folded scan == the fresh scan
    == the pre-surgery answers (the manifest is NECESSARY).
 3. THE JUST-INSIDE GATE LAW — a declared read pair (gate-only
    class) pops EXACTLY its readers (the `_readers` inversion), the
    folded scan re-derives == fresh, and the roll/decay answers plus
    the OTHER unit's scoped answers are unchanged (the boundary is
    per-structure and unit-local).
 4. THE JUST-INSIDE VERDICT-MOVER LAW — an npc's position move
    re-derives the roll buckets and the decay pairs (live == fresh
    birth, the exactness twins), pops exactly the pair's declared
    readers, and leaves the other unit's buckets unchanged.
 5. THE JUST-INSIDE AXIS-MOVER LAW — an npc's axis-prop change
    re-derives the decay pool (live == fresh birth) while the roll
    buckets hold and the fold pops iff the axis prop is a declared
    pair (the manifest decides, never a hardcode).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NamedTuple

from core.fold import apply_event
from core.log import EventRecord, StateChange
from core.loop import Simulator
from core.pack import load_pack
from core.rng import RngBank
from core.states import DecayIndex, decay_axes
from core.urgencies import RollIndex, urgency_scan
from scripts.densitypack import materialize

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

#: 1y at 360 days x 1440 ticks (the pack's own macro clock)
_ONE_YEAR = 518_400


class _Profile(NamedTuple):
    name: str
    settlements: int
    links: int
    scale: float
    households: int


#: the envelope's own axes (the row's declared workload — never one
#: fixed pack): the density-1 form, the households warm-ring axis,
#: and the cold-volume + relation-web + sampled-family axes together
PROFILES = (
    _Profile("density1", 3, 2, 1.0, 3),
    _Profile("households", 2, 0, 1.0, 6),
    _Profile("cold_r_rho", 4, 4, 0.5, 3),
)

_VERDICT_PROPS = ("position", "crime_status")


def _drained_sim(tmp: Path, profile: _Profile) -> tuple[Simulator, Any]:
    """A REAL 1y run on the materialized profile — the living world's
    own commit path folds the structures before any surgery (the
    composite workload: never the birth projection, never a crafted
    state)."""
    out = tmp / f"pack_{profile.name}"
    materialize(
        out, profile.settlements, profile.links, profile.scale,
        profile.households,
    )
    pack = load_pack(out)
    sim = Simulator(
        pack, 7, tmp / f"run_{profile.name}.jsonl", SCHEMA,
        commit="0000000",
    )
    sim.open()
    sim.run_steps([
        {"intent": "move", "target": "loc_s0_square"},
        {"intent": "wait", "ticks": _ONE_YEAR},
    ])
    sim.close()
    return sim, pack


def _unit_locs(pack: Any, unit: int) -> tuple[str, ...]:
    return tuple(
        sorted(
            e["id"] for e in pack.entities["locations"]
            if e["id"].startswith(f"loc_s{unit}_")
        )
    )


def _unit_npcs(pack: Any, unit: int) -> list[str]:
    return sorted(
        e["id"] for e in pack.entities["npcs"]
        if not e.get("is_player") and f"_s{unit}_" in e["id"]
    )


def _surgery(sim: Simulator, entity: str, prop: str, to_: Any, n: int) -> None:
    """One surgical state change riding the exact `_commit` fold-order
    excerpt for the verified family (loop.py's own sequence): apply,
    `_last_change` write, decay fold, roll fold, gate fold. The
    writer/OCC/knowledge/reaction halves stay out — owned by their
    own laws; the run is drained and disposable."""
    projection = sim.projection
    current = projection[entity][prop]
    record = EventRecord(
        id=f"ev_surgery_{n:04d}", t=sim._events[-1].t + 1 + n,
        type="boundary_surgery", actor="pc_01", cause=None, outcome={},
        knowledge=(), hooks=(), importance="low", provenance={},
        target=None,
        state_changes=(
            StateChange(entity=entity, prop=prop, from_=current, to_=to_),
        ),
    )
    apply_event(projection, record)
    sim._last_change[(entity, prop)] = record.t
    sim._decay_index.apply_change(entity, prop)
    sim._roll_index.apply_change(entity, prop)
    sim._gate_fold.apply_change(entity, prop)


def _moved(current: Any) -> Any:
    """A type-preserving mutation (the test_gatefold form): same type
    as the live value, never equal to it."""
    if isinstance(current, str):
        return f"{current}_moved"
    if isinstance(current, bool):
        return not current
    if isinstance(current, int):
        return current + 1000
    if isinstance(current, list):
        return [*current, "moved"]
    return "moved"


class _Manifest:
    """The declared dependency boundary, enumerated from the
    structures' own declarations (the manifest law's single
    source)"""

    def __init__(self, sim: Simulator, pack: Any) -> None:
        self.specs = sim._urgency_specs
        self.gate_pairs: set[tuple[str, str]] = {
            pair for spec in self.specs for pair in spec.pairs or ()
        }
        # the fold's own declared map == the specs' enumeration
        self.declared: dict[str, tuple[tuple[str, str], ...]] = {
            spec.probe.id: spec.pairs
            for spec in self.specs if spec.pairs is not None
        }
        self.axis_props = {axis.prop for axis in decay_axes(pack)}

    def outside_pairs(self, projection: Any) -> list[tuple[str, str]]:
        return sorted(
            (entity, prop)
            for entity, props in projection.items()
            for prop in props
            if (entity, prop) not in self.gate_pairs
            and prop not in _VERDICT_PROPS
            and prop not in self.axis_props
        )

    def gate_only_pairs(self) -> list[tuple[str, str]]:
        return sorted(
            pair for pair in self.gate_pairs
            if pair[1] not in _VERDICT_PROPS
            and pair[1] not in self.axis_props
        )


def _folded_scan(sim: Simulator, pack: Any, locations: Any = None) -> Any:
    return urgency_scan(
        pack, sim.projection, RngBank(7), locations=locations,
        specs=sim._urgency_specs, limit=400,
        gate_memo=sim._gate_memo, gate_fold=sim._gate_fold,
    )


def _fresh_scan(sim: Simulator, pack: Any, locations: Any = None) -> Any:
    return urgency_scan(
        pack, sim.projection, RngBank(7), locations=locations,
        specs=sim._urgency_specs, limit=400,
    )


def _roll(sim: Simulator, locations: Any = None) -> Any:
    return list(sim._roll_index.rolling(locations))


def _decay_answers(
    sim: Simulator, locations: Any = None
) -> tuple[Any, Any]:
    return (
        sim._decay_index.next_fire(locations),
        sim._decay_index.firing(10**9, locations),
    )


def _fresh_decay(sim: Simulator, pack: Any, locations: Any = None) -> tuple[
    Any, Any
]:
    fresh = DecayIndex.from_projection(
        pack, sim.projection, sim._decay_axes, sim._last_change,
    )
    return (fresh.next_fire(locations), fresh.firing(10**9, locations))


def _fresh_roll(sim: Simulator, locations: Any = None) -> Any:
    fresh = RollIndex.from_projection(sim._urgency_specs, sim.projection)
    return list(fresh.rolling(locations))


# -- 1: the manifest law -------------------------------------------------------

def test_the_manifest_is_the_packs_own_and_the_classes_have_teeth(
    tmp_path: Path,
) -> None:
    for profile in PROFILES:
        sim, pack = _drained_sim(tmp_path / profile.name, profile)
        manifest = _Manifest(sim, pack)
        # the fold's declared map IS the specs' own enumeration
        assert sim._gate_fold._declared == manifest.declared, profile.name
        assert manifest.gate_pairs
        # the scaffold's law: every declared pair is unit-namespaced
        # (or the singular player riding unit 0)
        for entity, _prop in manifest.gate_pairs:
            assert "_s" in entity or entity == "pc_01", (
                profile.name, entity,
            )
        # the surgery classes are non-vacuous (the battery has teeth)
        assert manifest.outside_pairs(sim.projection), profile.name
        assert manifest.gate_only_pairs(), profile.name
        assert manifest.axis_props, profile.name
        # the envelope really varied (the workload is the axes)
        assert len(pack.entities["locations"]) == 7 * profile.settlements


# -- 2: the just-outside law ---------------------------------------------------

def test_outside_cannot_change_the_result(
    tmp_path: Path,
) -> None:
    for profile in PROFILES:
        sim, pack = _drained_sim(tmp_path / profile.name, profile)
        manifest = _Manifest(sim, pack)
        unit1 = _unit_locs(pack, 1)
        # warm the fold (a full-scope scan confirms every probe)
        before_scan = _folded_scan(sim, pack)
        before_scan_u1 = _folded_scan(sim, pack, unit1)
        before_roll = _roll(sim)
        before_roll_u1 = _roll(sim, unit1)
        before_decay = _decay_answers(sim)
        before_decay_u1 = _decay_answers(sim, unit1)
        confirmed = set(sim._gate_fold._confirmed)
        assert confirmed, profile.name

        outside = manifest.outside_pairs(sim.projection)
        # teeth: the sweep crosses units AND the player
        assert any("_s1_" in e for e, _p in outside), profile.name
        assert any(e == "pc_01" for e, _p in outside), profile.name
        for n, (entity, prop) in enumerate(outside[:6]):
            _surgery(sim, entity, prop, _moved(sim.projection[entity][prop]), n)
            # no pop: the manifest is necessary
            assert set(sim._gate_fold._confirmed) == confirmed, (
                profile.name, entity, prop,
            )
            # the derived reads all hold — nothing moved anywhere
            assert _roll(sim) == before_roll, (profile.name, entity, prop)
            assert _roll(sim, unit1) == before_roll_u1
            assert _decay_answers(sim) == before_decay
            assert _decay_answers(sim, unit1) == before_decay_u1
            assert _folded_scan(sim, pack) == before_scan
            assert _folded_scan(sim, pack, unit1) == before_scan_u1
            # the twin: the folded answers == the fresh evaluation
            assert _folded_scan(sim, pack) == _fresh_scan(sim, pack)
            assert _folded_scan(sim, pack, unit1) == _fresh_scan(
                sim, pack, unit1
            )


# -- 3: the just-inside gate law ----------------------------------------------

def test_inside_the_gate_boundary_pops_exactly_its_readers(
    tmp_path: Path,
) -> None:
    for profile in PROFILES:
        sim, pack = _drained_sim(tmp_path / profile.name, profile)
        manifest = _Manifest(sim, pack)
        unit1 = _unit_locs(pack, 1)
        _folded_scan(sim, pack)  # warm: every gated probe confirmed
        confirmed = set(sim._gate_fold._confirmed)
        before_roll = _roll(sim)
        before_roll_u1 = _roll(sim, unit1)
        before_decay_u1 = _decay_answers(sim, unit1)
        before_scan_u1 = _fresh_scan(sim, pack, unit1)

        # a unit-0 declared pair of the gate-only class
        pair = next(
            pair for pair in manifest.gate_only_pairs()
            if "_s0_" in pair[0]
        )
        readers = set(sim._gate_fold._readers[pair])
        assert readers  # the pair is read — the boundary is real
        _surgery(sim, pair[0], pair[1], _moved(sim.projection[pair[0]][pair[1]]), 0)
        # the pop is EXACT: the pair's readers, nobody else
        assert confirmed - set(sim._gate_fold._confirmed) == readers
        # the re-derivation: the folded answers == fresh after the
        # pop (the key compare decides, the stored verdicts never
        # served stale)
        assert _folded_scan(sim, pack) == _fresh_scan(sim, pack)
        # the discrimination: the other structures never declared
        # this dependency — their answers are unchanged
        assert _roll(sim) == before_roll
        assert _roll(sim, unit1) == before_roll_u1
        assert _decay_answers(sim, unit1) == before_decay_u1
        # the locality cross: unit 1's scoped answers are unchanged
        assert _fresh_scan(sim, pack, unit1) == before_scan_u1
        # and the full scope re-confirms (the warm path is live)
        assert set(sim._gate_fold._confirmed) == confirmed


# -- 4: the just-inside verdict-mover law --------------------------------------

def test_inside_the_verdict_movers_rederive_roll_and_decay(
    tmp_path: Path,
) -> None:
    for profile in PROFILES:
        sim, pack = _drained_sim(tmp_path / profile.name, profile)
        unit0, unit1 = _unit_locs(pack, 0), _unit_locs(pack, 1)
        _folded_scan(sim, pack)  # warm
        confirmed = set(sim._gate_fold._confirmed)
        before_roll_u1 = _roll(sim, unit1)
        before_decay_u1 = _decay_answers(sim, unit1)
        before_scan_u1 = _fresh_scan(sim, pack, unit1)

        npc = _unit_npcs(pack, 0)[2]
        current = sim.projection[npc]["position"]
        target = next(loc for loc in unit0 if loc != current)
        # the position pair's declared readers (the p=100 movers
        # declare them; the manifest decides, never a hardcode)
        readers = set(sim._gate_fold._readers.get((npc, "position"), ()))
        _surgery(sim, npc, "position", target, 0)

        # the exactness twins: live == fresh birth (roll + decay)
        assert _roll(sim) == _fresh_roll(sim)
        assert _decay_answers(sim) == _fresh_decay(sim, pack)
        assert _decay_answers(sim, unit0) == _fresh_decay(sim, pack, unit0)
        # the discrimination + locality cross: unit 1 untouched
        assert _roll(sim, unit1) == before_roll_u1
        assert _decay_answers(sim, unit1) == before_decay_u1
        assert _fresh_scan(sim, pack, unit1) == before_scan_u1
        # the fold pops exactly the declared readers of the moved pair
        assert confirmed - set(sim._gate_fold._confirmed) == readers
        # the twin after the re-derivation
        assert _folded_scan(sim, pack) == _fresh_scan(sim, pack)


# -- 5: the just-inside axis-mover law -----------------------------------------

def test_inside_the_axis_movers_rederive_decay_only(
    tmp_path: Path,
) -> None:
    for profile in PROFILES:
        sim, pack = _drained_sim(tmp_path / profile.name, profile)
        manifest = _Manifest(sim, pack)
        unit0, unit1 = _unit_locs(pack, 0), _unit_locs(pack, 1)
        _folded_scan(sim, pack)  # warm
        confirmed = set(sim._gate_fold._confirmed)
        before_roll = _roll(sim)
        before_roll_u0 = _roll(sim, unit0)
        before_scan_u0 = _fresh_scan(sim, pack, unit0)

        # a unit-1 npc's axis prop (the locality cross runs both ways:
        # the surgery unit and the untouched unit swap roles)
        npc = _unit_npcs(pack, 1)[0]
        prop = sorted(manifest.axis_props)[0]
        assert prop in sim.projection[npc]
        current = sim.projection[npc][prop]
        readers = set(sim._gate_fold._readers.get((npc, prop), ()))
        _surgery(sim, npc, prop, current + 500, 0)

        # the decay twin: live == fresh birth (the pair re-derived)
        assert _decay_answers(sim) == _fresh_decay(sim, pack)
        assert _decay_answers(sim, unit1) == _fresh_decay(
            sim, pack, unit1
        )
        # the discrimination: the roll boundary never declared this
        # dependency — the buckets are unchanged
        assert _roll(sim) == before_roll
        assert _roll(sim, unit0) == before_roll_u0
        # the fold pops iff the axis prop is a declared read pair
        # (fatigue is NOT declared in the template — the manifest
        # decides; the discrimination is data-driven)
        assert confirmed - set(sim._gate_fold._confirmed) == readers
        assert _folded_scan(sim, pack) == _fresh_scan(sim, pack)
        # the locality cross: unit 0's scoped answers unchanged
        assert _fresh_scan(sim, pack, unit0) == before_scan_u0
