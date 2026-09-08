"""iter-81 acceptance — depth-5, the ordered worldgen passes (phase 5's
build-column headline, TASKS/phases.md §5 — the Azgaar + Red Blob donor
discipline: ordered focused passes, integer geometry, per-pass streams).
Mechanics only (iter-81, the depth-1/2/4 pattern): the committed pack is
UNARMED (no `worldgen` block — the 68a pattern), so the unarmed arm of
every A/B pin below is the committed pack itself; the armed arm is the
crafted twin (the block + the `world_history` template line).

The laws pinned here:

- **The stream law (the D-079 family's fourth member)**:
  `worldgen:<pass>`, content-addressed via
  `core/rng.py::worldgen_stream_name` (injective — the pass names are
  the closed, ":"-free `PASS_ORDER` vocabulary); lazily registered;
  per-seed derived; the closed-set tripwire survives for non-family
  names; the ONE legal nesting is inside the assured substantive run
  scope (a worldgen stream may shadow `substantive`, never the
  reverse).
- **The unarmed law**: a pack without the block answers `(None, ())`
  BEFORE any stream touch — zero registrations, zero draws, zero
  events; the committed run is v0.1 byte-identical (the corpus price
  zero by construction, the depth-2 precedent).
- **The integer discipline (the Azgaar float-drift refusal)**: every
  model value is a Python int, in its declared bounds — a float
  anywhere in the model is a bug of the highest severity.
- **The pass laws**: determinism (same seed → same model), the lattice
  count, the relax discipline, the closed biome vocabulary + the
  coastal rule, the watershed flow/rivers, the capitals/regions
  growth, the chronicle cap and ordering.
- **The claim gate (`detail_claim`'s first legal caller)**: commit on
  an empty log; `no_op` skipped (the idempotent duplicate);
  `slot_conflict` refused with the cause chain — the world-forming
  event carries ONLY the committed claims, the refused list rides the
  outcome (never-empty keys only when non-empty — the drifted_from
  law).
- **The genesis integration**: the world forms at open time, BEFORE
  any player step; the first genesis event is the run-start (cause
  null); events chain; the PC's first event chains to the LAST
  genesis event; the director's buffer holds the genesis hooks; the
  claims live in the projection and replay through the fold (INV-1);
  history carries NO knowledge records (the DF discipline: history is
  canon-dense, epistemology-empty); the isolation law — the armed
  arm's substantive fingerprint equals the unarmed arm's (the worldgen
  streams never move a canon draw); same seed → byte-identical logs.
- **The lint family** (`core/pack.py::_worldgen`): the closed
  vocabulary at every level, the range laws, the template closure, the
  declared-hook law, the claim double-claim laws (modeled slot /
  scene_detail overlap / duplicate pair / site bounds).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.detail import COMMIT, NO_OP, SLOT_CONFLICT
from core.fold import fold, initial_projection
from core.intent import pack_importance
from core.log import EventRecord, StateChange, read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack
from core.rng import (
    COSMETIC,
    SUBSTANTIVE,
    RngBank,
    RngError,
    worldgen_stream_name,
)
from core.worldgen import (
    BIOMES,
    FIELD_MAX,
    HISTORY_KINDS,
    PASS_ORDER,
    WORLDGEN_BLOCK,
    WorldgenError,
    generate_world,
    genesis,
    resolve_claims,
)

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

PLAYER = "pc_01"
EVENT_TYPE = "world_history"
TEMPLATE_LINE = "{actor}: the world remembers ({kind}, year {year})."

#: The armed twin's block — bands calibrated so seed 42 spans the whole
#: biome vocabulary (ocean + coast included, the coastal rule live).
WG: dict[str, Any] = {
    "map": {
        "extent": 48,
        "spacing": 8,
        "jitter": 3,
        "relax_rounds": 1,
        "height_octaves": 3,
        "moisture_octaves": 2,
    },
    "biomes": {
        "height_bands": [4000, 5000, 7000],
        "moisture_bands": [2500, 5000, 7500],
    },
    "watershed": {"neighbors": 4, "river_flow": 6},
    "states": {"capitals": 3},
    "chronicle": {
        "years": 150,
        "events_max": 5,
        "event_type": EVENT_TYPE,
        "hooks": ["barkeep_wary_sweep", "ambient_drunkard_ramble"],
    },
    "claims": [
        {"location": "loc_tavern", "slot": "terrain", "field": "biome", "site": 0},
        {"location": "loc_tavern", "slot": "world_region", "field": "region", "site": 0},
        {"location": "loc_street", "slot": "near_river", "field": "river", "site": 1},
    ],
}

CLAIM_SLOTS = ("terrain", "world_region", "near_river")


def crafted_pack(
    tmp_path: Path, name: str, worldgen: Any, *, template: bool = True
) -> Pack:
    """A committed-pack copy with the `worldgen` block set (or REMOVED
    when None — the v0.1 twin) and the `world_history` template line
    added (the lint's template closure: the genesis event type is pack
    vocabulary, EVENT_SCHEMA §11)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if worldgen is None:
        rules.pop(WORLDGEN_BLOCK, None)
    else:
        rules[WORLDGEN_BLOCK] = worldgen
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    if template:
        templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
        templates["events"][EVENT_TYPE] = TEMPLATE_LINE
        (target / "templates.json").write_text(
            json.dumps(templates, indent=2), encoding="utf-8"
        )
    return load_pack(target)


def _rules_with(worldgen: Any) -> dict[str, Any]:
    rules = dict(PACK.rules)
    if worldgen is None:
        rules.pop(WORLDGEN_BLOCK, None)
    else:
        rules[WORLDGEN_BLOCK] = worldgen
    return rules


def _record(event_id: str, changes: tuple[StateChange, ...]) -> EventRecord:
    return EventRecord(
        id=event_id, t=0, type="look_around", actor=PLAYER, cause=None,
        outcome={}, knowledge=(), state_changes=changes, hooks=(),
        importance="low", provenance={"seed": 42}, target=None,
    )


def _run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]], name: str,
) -> tuple[Path, Simulator]:
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    sim.close()
    return log, sim


# -- the stream law (unit) -----------------------------------------------------


def test_the_name_grammar_is_content_addressed() -> None:
    """`worldgen_stream_name` is the single owner of the naming grammar
    `worldgen:<pass>` — injective over the closed PASS_ORDER
    vocabulary, whose members are ":"-free (the re-raise guard's law:
    stream-name injectivity holds by construction)."""
    assert worldgen_stream_name("sites") == "worldgen:sites"
    names = [worldgen_stream_name(pass_name) for pass_name in PASS_ORDER]
    assert len(set(names)) == len(names)  # injective
    assert all(":" not in pass_name for pass_name in PASS_ORDER)


def test_the_stream_registers_lazily_and_derives_per_seed() -> None:
    """The family registers on first use, derives per (seed, name) —
    the standard stream law (INV-2) — and a worldgen-LOOKING non-family
    name stays loud (the closed-set tripwire)."""
    stream = worldgen_stream_name("sites")
    bank = RngBank(42)
    assert bank.peek(stream) != bank.peek(SUBSTANTIVE)
    assert bank.peek(stream) != bank.peek(COSMETIC)
    assert RngBank(42).peek(stream) == RngBank(42).peek(stream)
    assert RngBank(42).peek(stream) != RngBank(43).peek(stream)
    with pytest.raises(RngError, match="unknown stream"):
        bank.peek("worldgen-sites")  # outside the family (the separator)


def test_the_family_nests_inside_the_substantive_scope() -> None:
    """The one legal nesting: a worldgen-family stream may shadow the
    assured substantive run scope (the pass draws are canon-relevant
    but stream-isolated); the reverse nesting is a bug, not a
    feature."""
    stream = worldgen_stream_name("height")
    bank = RngBank(42)
    with bank.assure(SUBSTANTIVE):
        bank.randint(1, 6)  # a canon check draws
        with bank.assure(stream):
            assert bank.active == stream
            bank.randint(1, 100)
        assert bank.active == SUBSTANTIVE
        bank.randint(1, 6)
    with bank.assure(stream):
        with pytest.raises(RngError, match="cannot assure"):
            with bank.assure(SUBSTANTIVE):
                pass


# -- the unarmed law ------------------------------------------------------------


def test_the_unarmed_law_answers_nothing_before_any_stream_touch() -> None:
    """A pack without the block answers `(None, ())` BEFORE any stream
    is touched: no lazy registration (count on a worldgen stream is a
    KeyError — the stream never existed), zero draws, fingerprint
    zero."""
    bank = RngBank(42)
    model, drafts = genesis(bank, PACK.rules, [], 42)
    assert model is None and drafts == ()
    for pass_name in PASS_ORDER:
        with pytest.raises(KeyError):
            bank.count(worldgen_stream_name(pass_name))
    assert bank.fingerprint == 0


def test_the_committed_run_stays_v01(tmp_path: Path) -> None:
    """The committed pack (unarmed) runs the v0.1 shape: no genesis
    events (a wait script answers exactly its own event), `world` is
    None — the corpus price zero by construction."""
    log, sim = _run(tmp_path, PACK, 42, [{"intent": "wait", "ticks": 5}], "v01")
    _header, events = read_log(log, SCHEMA)
    assert len(events) == 1 and events[0].actor == PLAYER
    assert sim.world is None


# -- the pass laws (determinism + shape + the integer discipline) ----------------


def test_same_seed_same_world_different_seed_different_world() -> None:
    assert generate_world(RngBank(42), WG) == generate_world(RngBank(42), WG)
    assert generate_world(RngBank(42), WG) != generate_world(RngBank(43), WG)


def test_the_geometry_is_integer_only_and_in_bounds() -> None:
    """The Azgaar float-drift refusal made executable: every model
    value is an int inside its declared bounds — a float anywhere in
    the model (sites, height, moisture, flow, rivers, capitals) is a
    discipline violation, the highest-severity bug class."""
    for seed in (42, 7, 125, 93):
        model = generate_world(RngBank(seed), WG)
        for x, y in model.sites:
            assert isinstance(x, int) and isinstance(y, int)
            assert 0 <= x < model.extent and 0 <= y < model.extent
        for value in model.height:
            assert isinstance(value, int) and 0 <= value <= FIELD_MAX
        for value in model.moisture:
            assert isinstance(value, int) and 0 <= value <= FIELD_MAX
        for value in model.flow:
            assert isinstance(value, int) and value >= 1
        assert all(isinstance(site, int) for site in model.rivers)
        assert all(isinstance(site, int) for site in model.capitals)


def test_the_lattice_count_and_the_relax_discipline() -> None:
    """The sites pass answers (extent // spacing)^2 sites; one relax
    round moves them (the Lloyd discipline) but never out of
    bounds."""
    no_relax = {**WG, "map": {**WG["map"], "relax_rounds": 0}}
    relaxed = generate_world(RngBank(42), WG)
    raw = generate_world(RngBank(42), no_relax)
    assert len(relaxed.sites) == len(raw.sites) == (48 // 8) ** 2
    assert relaxed.sites != raw.sites  # the round moved sites
    assert all(
        0 <= x < 48 and 0 <= y < 48 for x, y in relaxed.sites
    )


def test_the_biome_vocabulary_is_closed_and_the_coast_law_holds() -> None:
    """Every biome is a member of the closed vocabulary; the coastal
    rule is structural: a coast site is always height-band-1 with an
    ocean site among its k nearest (the calibrated bands exercise both
    on seed 42)."""
    model = generate_world(RngBank(42), WG)
    assert set(model.biomes) <= set(BIOMES)
    assert "ocean" in model.biomes and "coast" in model.biomes  # the rule is live
    bands = WG["biomes"]["height_bands"]

    def band(height: int) -> int:
        for index, edge in enumerate(bands):
            if height < edge:
                return index
        return len(bands)

    ocean_sites = [i for i, b in enumerate(model.biomes) if b == "ocean"]
    for i, biome in enumerate(model.biomes):
        if biome != "coast":
            continue
        assert band(model.height[i]) == 1
        x, y = model.sites[i]
        distances = sorted(
            (x - sx) ** 2 + (y - sy) ** 2
            for j, (sx, sy) in enumerate(model.sites)
            if j in ocean_sites
        )
        assert distances[: WG["watershed"]["neighbors"]]  # an ocean neighbor exists


def test_the_watershed_flow_and_river_law() -> None:
    model = generate_world(RngBank(42), WG)
    threshold = WG["watershed"]["river_flow"]
    assert all(flow >= 1 for flow in model.flow)
    assert model.rivers == frozenset(
        i for i, flow in enumerate(model.flow) if flow >= threshold
    )


def test_the_states_law_capitals_and_nearest_region() -> None:
    model = generate_world(RngBank(42), WG)
    capitals = sorted(model.capitals)
    assert len(capitals) == WG["states"]["capitals"]
    assert set(model.regions) <= {f"region_{i:02d}" for i in range(len(capitals))}
    for i, (x, y) in enumerate(model.sites):
        owner = min(
            range(len(capitals)),
            key=lambda r: (
                (x - model.sites[capitals[r]][0]) ** 2
                + (y - model.sites[capitals[r]][1]) ** 2,
                r,
            ),
        )
        assert model.regions[i] == f"region_{owner:02d}"


def test_the_chronicle_is_capped_ordered_and_closed() -> None:
    """The genesis answers events_max events: world_formed + the
    history draws, years ascending inside [1, years], kinds from the
    closed vocabulary, hooks from the declared tags, all at t=0 with
    the world actor and NO knowledge records (the DF discipline)."""
    model, drafts = genesis(RngBank(42), _rules_with(WG), [], 42)
    assert model is not None and len(drafts) == WG["chronicle"]["events_max"]
    assert drafts[0].outcome["kind"] == "world_formed"
    years = [draft.outcome["year"] for draft in drafts[1:]]
    assert years == sorted(years)
    assert all(1 <= year <= WG["chronicle"]["years"] for year in years)
    for draft in drafts:
        assert draft.t == 0 and draft.actor == "world"
        assert draft.type == EVENT_TYPE
        assert draft.knowledge == ()
        assert draft.provenance == {"seed": 42, "worldgen": True}
    for draft in drafts[1:]:
        assert draft.outcome["kind"] in HISTORY_KINDS
        assert draft.hooks[0] in WG["chronicle"]["hooks"]
        assert len(draft.hooks) == 1
    assert not drafts[0].hooks  # the world's shape is facts, not consequences


def test_the_importance_rides_the_pack_rule() -> None:
    """One rule for action events and world events: the genesis
    importance is `pack_importance`'s answer over the same inputs —
    never a second scoring path."""
    rules = _rules_with(WG)
    model, drafts = genesis(RngBank(42), rules, [], 42)
    assert model is not None
    formed, *history = drafts
    assert formed.importance == pack_importance(
        rules, {"loc_tavern", "loc_street"}, 0, 0, EVENT_TYPE
    )
    for draft in history:
        assert draft.importance == pack_importance(
            rules, set(), 0, len(draft.hooks), EVENT_TYPE
        )


# -- the claim gate (the first legal caller) ------------------------------------


def test_the_first_legal_caller_commits_on_an_empty_log() -> None:
    """The genesis is `detail_claim`'s first legal caller: an empty log
    answers commit for every claim — the claimer is the first
    committer, the values are the model's own reads."""
    model = generate_world(RngBank(42), WG)
    claims = resolve_claims([], model, WG["claims"])
    assert [claim.outcome for claim in claims] == [COMMIT] * len(WG["claims"])
    assert all(claim.cause is None for claim in claims)
    assert claims[0].value == model.biomes[0]
    assert claims[1].value == model.regions[0]
    assert claims[2].value == (1 in model.rivers)


def test_the_gate_answers_no_op_and_conflict_with_the_cause_chain() -> None:
    """The verdict family the future lazy door will live on: canon
    holding the SAME value answers the idempotent no_op (skipped, not
    written); canon holding a DIFFERENT value refuses with the winning
    event's id as the cause — the world-forming event carries only the
    committed claims, the refused list rides the outcome."""
    model = generate_world(RngBank(42), WG)
    events = [
        _record(
            "ev_0002",
            (StateChange("loc_tavern", "terrain", None, model.biomes[0]),),
        ),
        _record(
            "ev_0005",
            (StateChange("loc_tavern", "world_region", None, "region_XX"),),
        ),
    ]
    claims = resolve_claims(events, model, WG["claims"])
    by_slot = {claim.slot: claim for claim in claims}
    assert by_slot["terrain"].outcome == NO_OP  # canon holds the same value
    refused = by_slot["world_region"]
    assert refused.outcome == SLOT_CONFLICT and refused.cause == "ev_0005"
    assert by_slot["near_river"].outcome == COMMIT

    _model, drafts = genesis(RngBank(42), _rules_with(WG), events, 42)
    formed = drafts[0]
    # only the committed claim writes; the no_op is skipped, the
    # conflict refused
    assert [(c.entity, c.prop, c.from_, c.to_) for c in formed.state_changes] == [
        ("loc_street", "near_river", None, 1 in model.rivers)
    ]
    assert formed.outcome["claims"] == [
        {"slot": "near_river", "value": 1 in model.rivers}
    ]
    assert formed.outcome["refused"] == [
        {"slot": "world_region", "cause": "ev_0005"}
    ]


def test_a_claims_free_genesis_omits_the_outcome_keys() -> None:
    """The drifted_from law: `claims` and `refused` ride the outcome
    only when non-empty — a claims-free genesis (map + history alone)
    writes a lean world_formed outcome."""
    config = {**WG, "claims": []}
    model, drafts = genesis(RngBank(42), _rules_with(config), [], 42)
    assert model is not None
    assert "claims" not in drafts[0].outcome
    assert "refused" not in drafts[0].outcome
    assert drafts[0].state_changes == ()


# -- the genesis integration (the armed crafted twin) ---------------------------


def test_the_genesis_commits_before_the_first_step_and_seeds_the_buffer(
    tmp_path: Path,
) -> None:
    """The PC walks into a running world: open() forms the world, the
    claims live in the projection, the director's buffer holds the
    genesis hooks — all BEFORE any player step; the first genesis
    event is the run's run-start (cause null), the chain is linear,
    and the PC's first event chains to the LAST genesis event."""
    armed = crafted_pack(tmp_path, "armed", WG)
    log = tmp_path / "genesis.jsonl"
    sim = Simulator(armed, 42, log, SCHEMA, commit="0000000")
    sim.open()
    try:
        assert sim.world is not None and len(sim.world.sites) == 36
        buffer = [(hook.tag, hook.seeded_by_event) for hook in sim.director.hooks]
        assert buffer  # the pre-PC history seeded the director's buffer
        assert all(
            tag in WG["chronicle"]["hooks"] for tag, _ in buffer
        )
        genesis_hook_ids = {event_id for _, event_id in buffer}
        header, events = read_log(log, SCHEMA)
        assert len(events) == WG["chronicle"]["events_max"]
        assert events[0].id == "ev_0000" and events[0].cause is None
        for previous, event in zip(events, events[1:], strict=False):
            assert event.cause == previous.id
        assert {event.id for event in events[1:]} == genesis_hook_ids
        # the claims are canon: the projection holds them, the fold
        # replays them (INV-1 — state = fold(log))
        model = sim.world
        assert sim.projection["loc_tavern"]["terrain"] == model.biomes[0]
        assert sim.projection["loc_tavern"]["world_region"] == model.regions[0]
        assert sim.projection["loc_street"]["near_river"] == (1 in model.rivers)
        replayed = fold(events, initial_projection(armed.entities))
        assert replayed["loc_tavern"]["terrain"] == model.biomes[0]
        assert replayed["loc_street"]["near_river"] == (1 in model.rivers)
        # the PC's first event chains to the LAST genesis event
        sim.run_steps([{"intent": "wait", "ticks": 5}])
        _header, after = read_log(log, SCHEMA)
        assert after[-1].actor == PLAYER and after[-1].cause == events[-1].id
    finally:
        sim.close()


def test_the_armed_run_is_byte_identical_across_runs(tmp_path: Path) -> None:
    """Determinism end-to-end: same seed, same pack, same script →
    identical log bytes (the T1 discipline, armed arm)."""
    armed = crafted_pack(tmp_path, "armed", WG)
    first, _ = _run(tmp_path, armed, 42, [{"intent": "wait", "ticks": 5}], "a")
    second, _ = _run(tmp_path, armed, 42, [{"intent": "wait", "ticks": 5}], "b")
    assert first.read_bytes() == second.read_bytes()


def test_the_isolation_law_the_canon_fingerprint_never_moves(
    tmp_path: Path,
) -> None:
    """The family law at pass granularity, measured: the armed arm's
    substantive fingerprint equals the unarmed arm's for the same
    script — the worldgen streams never move a canon draw (the corpus
    price of arming is the genesis events alone)."""
    unarmed = crafted_pack(tmp_path, "unarmed", None)
    armed = crafted_pack(tmp_path, "armed", WG)
    steps = [{"intent": "wait", "ticks": 5}]
    _log_a, sim_a = _run(tmp_path, unarmed, 42, steps, "iso_a")
    _log_b, sim_b = _run(tmp_path, armed, 42, steps, "iso_b")
    assert sim_a._bank.fingerprint == sim_b._bank.fingerprint


def test_the_genesis_events_carry_no_knowledge(tmp_path: Path) -> None:
    """The DF discipline (bg-2's measured finding: DF history is
    canon-dense, epistemology-empty): the pre-PC history carries no
    knowledge records — the world has a past nobody knows; the PC (and
    the telling path) learn the present, never the deep history."""
    log, _ = _run(tmp_path, crafted_pack(tmp_path, "armed", WG), 42, [], "silent")
    _header, events = read_log(log, SCHEMA)
    assert all(event.knowledge == () for event in events)


# -- the runtime backstop (D-111 — the loud raw-read family) ---------------------


def test_the_runtime_backstop_is_loud_on_hand_built_configs() -> None:
    """A hand-built config missing a block, a bad claim field, or an
    out-of-range site raises WorldgenError naming the offender —
    KeyError/IndexError never leak (the pred-contract family law)."""
    bank = RngBank(42)
    with pytest.raises(WorldgenError, match="missing the 'states' block"):
        genesis(bank, _rules_with({k: v for k, v in WG.items() if k != "states"}), [], 42)
    model = generate_world(RngBank(42), WG)
    with pytest.raises(WorldgenError, match="closed set"):
        model.claim_value("biomes", 0)
    with pytest.raises(WorldgenError, match="outside 0"):
        model.claim_value("biome", len(model.sites))


# -- the lint family (`core/pack.py::_worldgen`) ---------------------------------


_LINT_SEQ = 0


def _lint_error(tmp_path: Path, worldgen: Any) -> str:
    """One crafted variant per call (unique dir names — several probes
    share a tmp_path)."""
    global _LINT_SEQ
    _LINT_SEQ += 1
    with pytest.raises(PackError) as excinfo:
        crafted_pack(tmp_path, f"lint_{_LINT_SEQ}", worldgen)
    return str(excinfo.value)


def test_the_lint_accepts_the_canonical_arming(tmp_path: Path) -> None:
    assert crafted_pack(tmp_path, "ok", WG).rules[WORLDGEN_BLOCK] == WG


def test_the_lint_refuses_unknown_keys_at_every_level(tmp_path: Path) -> None:
    assert "unknown keys" in _lint_error(tmp_path, {**WG, "terrain": 1})
    assert "unknown keys" in _lint_error(
        tmp_path, {**WG, "map": {**WG["map"], "scale": 2}}
    )
    assert "unknown keys" in _lint_error(
        tmp_path, {**WG, "chronicle": {**WG["chronicle"], "notes": "x"}}
    )
    assert "unknown keys" in _lint_error(
        tmp_path, {**WG, "claims": [{"location": "loc_tavern", "slot": "s",
                                      "field": "biome", "site": 0, "weight": 1}]}
    )


def test_the_lint_refuses_range_and_shape_violations(tmp_path: Path) -> None:
    cases: list[tuple[dict[str, Any], str]] = [
        ({**WG, "map": {**WG["map"], "extent": 8}}, "extent must exceed spacing"),
        ({**WG, "map": {**WG["map"], "jitter": 4}}, "jitter collapses the lattice"),
        ({**WG, "map": {**WG["map"], "height_octaves": 0}}, "height_octaves"),
        ({**WG, "map": {**WG["map"], "relax_rounds": 9}}, "relax_rounds"),
        ({**WG, "biomes": {**WG["biomes"], "height_bands": [5000, 4000, 7000]}},
         "strictly ascending"),
        ({**WG, "biomes": {**WG["biomes"], "moisture_bands": [100, 200]}},
         "three integer band edges"),
        ({**WG, "watershed": {**WG["watershed"], "neighbors": 1}}, "neighbors"),
        ({**WG, "watershed": {**WG["watershed"], "river_flow": 1}}, "river_flow"),
        ({**WG, "states": {**WG["states"], "capitals": 0}}, "capitals"),
        ({**WG, "states": {**WG["states"], "capitals": 999}}, "capitals"),
        ({**WG, "chronicle": {**WG["chronicle"], "events_max": 0}}, "events_max"),
        ({**WG, "chronicle": {**WG["chronicle"], "years": 0}}, "years"),
    ]
    for worldgen, needle in cases:
        assert needle in _lint_error(tmp_path, worldgen)


def test_the_lint_refuses_an_undeclared_event_type_or_hooks(tmp_path: Path) -> None:
    """The genesis event type is pack vocabulary (EVENT_SCHEMA §11);
    the chronicle hooks must be DECLARED director hooks — a genesis
    hook the director does not know would never release."""
    with pytest.raises(PackError, match="template vocabulary"):
        crafted_pack(tmp_path, "bad_type", WG, template=False)
    bad_hooks = {**WG, "chronicle": {**WG["chronicle"], "hooks": ["no_such_hook"]}}
    assert "undeclared director" in _lint_error(tmp_path, bad_hooks)


def test_the_lint_refuses_the_claim_double_claim_family(tmp_path: Path) -> None:
    modeled = {**WG, "claims": [
        {"location": "loc_tavern", "slot": "layout", "field": "biome", "site": 0}
    ]}
    assert "modeled by the location entity" in _lint_error(tmp_path, modeled)
    overlap = {**WG, "claims": [
        {"location": "loc_tavern", "slot": "under_bench", "field": "biome", "site": 0}
    ]}
    assert "scene_detail" in _lint_error(tmp_path, overlap)
    bad_field = {**WG, "claims": [
        {"location": "loc_tavern", "slot": "terrain", "field": "weather", "site": 0}
    ]}
    assert "closed set" in _lint_error(tmp_path, bad_field)
    bad_site = {**WG, "claims": [
        {"location": "loc_tavern", "slot": "terrain", "field": "biome", "site": 99}
    ]}
    assert "0..35" in _lint_error(tmp_path, bad_site)
    duplicate = {**WG, "claims": WG["claims"] + [
        {"location": "loc_tavern", "slot": "terrain", "field": "height", "site": 1}
    ]}
    assert "claimed twice" in _lint_error(tmp_path, duplicate)
    unknown_location = {**WG, "claims": [
        {"location": "loc_nowhere", "slot": "terrain", "field": "biome", "site": 0}
    ]}
    assert "unknown location id" in _lint_error(tmp_path, unknown_location)
    empty_claims = {**WG, "claims": []}
    assert "dead data" in _lint_error(tmp_path, empty_claims)
