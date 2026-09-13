"""T1-province — determinism for the province pack (world-2 L2, slice 1,
iter-118: the skeleton — the generated surface at province scale, the
settlements on the travel lattice, the spine records, the AP crosswalk's
first committed consumer).

Same seed + same playscript + same environment = byte-identical logs,
measured against the committed golden fixture
(`tests/fixtures/province_smoke_seed42.jsonl`) — the tavern T1's shape
(`tests/test_t1_determinism.py`), re-run over the THIRD pack at the
L2 scale: a pack that is data-only over a 324-site generated surface
proves the universal-core claim at province scale (zero engine edits,
the module contract D-142).

The travel-loop pins (the L2 scale claims): the move completions land
exactly at accept-t + the st-6a DERIVED price (`core/travel.py` —
integer math over the genesis-frozen WorldModel, draw-free: the
fingerprint stays 0), the watch rotations fire MID-TRAVEL (D-038 —
the long legs carry the institution's beats), and the knowledge
transfer lands strictly INSIDE a leg (the road T1's measured instance
re-produced at province scale: the duty sergeant briefing his relief
from the market post, t=3240 inside the Malby → Thornmill leg).

The L2 spine pins (the AP crosswalk's first committed consumer,
D-148/D-152): the province's NPCs carry spine records whose every
flaw is consumed by an urgency entry — the pack-ci crosswalk's first
non-crafted instance.
"""

from __future__ import annotations

import json
from pathlib import Path

from core.loop import Simulator, load_playscript
from core.pack import load_pack
from core.travel import travel_ticks

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
GOLDEN = REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "province_smoke.json")
PACK_DIR = REPO / "content" / "province_pack"

#: The route the smoke script walks (origin -> destination per move
#: step): the artery's five legs — the hill gate road, the garrison
#: road, the town road, the manor road — prices read from the travel
#: law over the 324-site lattice.
LEGS: tuple[tuple[str, str], ...] = (
    ("loc_riverroad", "loc_weirstair"),
    ("loc_weirstair", "loc_riverroad"),
    ("loc_riverroad", "loc_keep"),
    ("loc_keep", "loc_malby"),
    ("loc_malby", "loc_thornmill"),
)
#: The waits between the legs (the script's own data): leg index ->
#: the wait ticks that follow it (after the weir leg, after the road
#: leg, and the market-business wait before the manor leg).
WAITS: dict[int, int] = {0: 30, 1: 15, 3: 600}


def run(tmp_path: Path, name: str) -> tuple[bytes, int]:
    pack = load_pack(PACK_DIR)
    sim = Simulator(pack, SCRIPT["seed"], tmp_path / name, SCHEMA, commit="0000000")
    result = sim.run_playscript(SCRIPT)
    return (tmp_path / name).read_bytes(), result.fingerprint


def _events(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if "schema_version" not in line
    ]


def test_two_runs_are_byte_identical(tmp_path: Path) -> None:
    first, fp1 = run(tmp_path, "a.jsonl")
    second, fp2 = run(tmp_path, "b.jsonl")
    assert first == second
    assert fp1 == fp2


def test_fresh_run_matches_committed_golden(tmp_path: Path) -> None:
    fresh, fingerprint = run(tmp_path, "fresh.jsonl")
    assert fresh == GOLDEN.read_bytes()
    # edge-priced moves draw nothing (the price is a pure integer
    # function of pack data + the genesis-frozen model, INV-2-clean by
    # construction) and this script runs no opposed check — the
    # substantive stream is never drawn.
    assert fingerprint == 0


# -- the fixture-regeneration guard (TEST_PLAN.md §1.1, the tavern twin) --


def _current_schema_version() -> str:
    schema_id = SCHEMA.get("$id", "")
    assert "/" in schema_id, (
        f"schema $id must look like 'canonsim/event/<ver>', got {schema_id!r}"
    )
    return schema_id.rsplit("/", 1)[-1]


def test_committed_fixture_schema_version_matches_current_schema() -> None:
    header_line = GOLDEN.read_text(encoding="utf-8").splitlines()[0]
    header = json.loads(header_line)
    assert header["schema_version"] == _current_schema_version()


def test_fresh_regeneration_byte_diff_against_committed(tmp_path: Path) -> None:
    fresh, _ = run(tmp_path, "regen.jsonl")
    committed = GOLDEN.read_bytes()
    assert fresh == committed, (
        "province fixture regeneration diverged from the committed fixture — "
        "a behavior change altered emitted bytes; regenerate the fixture "
        "(TEST_PLAN.md §3) and commit it with the code change"
    )


def test_different_seed_diverges(tmp_path: Path) -> None:
    other = dict(SCRIPT, seed=43)
    sim = Simulator(
        load_pack(PACK_DIR), 43, tmp_path / "other.jsonl", SCHEMA,
        commit="0000000",
    )
    sim.run_playscript(other)
    assert (tmp_path / "other.jsonl").read_bytes() != GOLDEN.read_bytes()


# -- the travel-loop pins (the L2 scale claims) ------------------------------


def test_derived_prices_pin_the_route(tmp_path: Path) -> None:
    """Every move completion lands exactly at accept-t + travel_ticks:
    the derived price IS the artery's law — the province walks in
    hours-to-a-day (705/705/660/405/345 over the lattice), where the
    road walked in minutes. The expected clock is rebuilt from the
    travel law + the script's own waits — a price change without a
    fixture regen fails BOTH here and the regen guard; this test
    names why."""
    pack = load_pack(PACK_DIR)
    sim = Simulator(
        pack, SCRIPT["seed"], tmp_path / "prices.jsonl", SCHEMA,
        commit="0000000",
    )
    sim.run_playscript(SCRIPT)
    prices = [
        travel_ticks(pack.rules, sim.world, origin, destination)
        for origin, destination in LEGS
    ]
    # the province scale: the artery's own weight — the heaviest leg
    # near twice the road's longest (360), the whole walk more than
    # twice the road's loop (the map's 9x growth made mechanical)
    assert max(prices) > 600, prices
    assert sum(prices) > 2800, prices
    # the expected completion clock: step 1 accepts at t=0; each later
    # step accepts when the previous one completed (run_playscript
    # drains the queue between steps).
    clock = 0
    expected: list[tuple[int, str]] = []
    for index, (_origin, destination) in enumerate(LEGS):
        clock += prices[index]
        expected.append((clock, destination))
        if index in WAITS:
            clock += WAITS[index]
    moves = [
        (event["t"], event["target"])
        for event in _events(tmp_path / "prices.jsonl")
        if event["type"] == "move"
    ]
    assert moves == expected


def test_encounters_fire_mid_travel(tmp_path: Path) -> None:
    """D-038 at province scale: rotations, briefings and the beat axis
    land strictly INSIDE the long legs' tick windows — the artery's
    institutions ride the route. The measured instance: the watch
    change + the knowledge transfer (Osgar briefing Ferra, the duty
    sergeant's arrival record passing to the relief) at t=3240,
    inside the Malby -> Thornmill leg (3120 -> 3465)."""
    pack = load_pack(PACK_DIR)
    sim = Simulator(
        pack, SCRIPT["seed"], tmp_path / "mid.jsonl", SCHEMA, commit="0000000"
    )
    sim.run_playscript(SCRIPT)
    events = _events(tmp_path / "mid.jsonl")
    legs = [
        (event["t"], event["target"])
        for event in events
        if event["type"] == "move"
    ]
    assert len(legs) == len(LEGS)
    windows: list[tuple[int, int]] = []
    accept = 0
    for index, (complete_t, _destination) in enumerate(legs):
        windows.append((accept, complete_t))
        accept = complete_t
        if index in WAITS:
            accept += WAITS[index]
    mid_travel = [
        event
        for event in events
        if event["type"] != "move"
        and any(start < event["t"] < end for start, end in windows)
    ]
    assert mid_travel, (
        "no encounter fired mid-travel — the travel loop degenerated "
        "into teleportation (D-038's crossings must ride the queue in "
        "tick order)"
    )
    kinds = {event["type"] for event in mid_travel}
    assert "watch_change" in kinds or "knowledge_transfer" in kinds
    # the measured transfer: strictly inside the LAST leg — the duty
    # sergeant's briefing to the relief, the road T1's own instance
    # re-produced at the province's scale
    transfers = [
        event
        for event in events
        if event["type"] == "knowledge_transfer"
    ]
    assert transfers, "the knowledge transfer never fired — the duty record never passed"
    last_start, last_end = windows[-1]
    assert any(
        last_start < event["t"] < last_end for event in transfers
    ), "the briefing must land mid-travel (the artery's institution riding the route)"


def test_the_genesis_renders_the_province_scale() -> None:
    """The world_formed line carries the L2 skeleton's own shape: the
    324-site band (the 200-600 row, phases.md §6), the six armed claim
    slots (the settlements' grounds), and the chronicle's history
    lines open the tale (the feud/quarrel collections, 150 years)."""
    pack = load_pack(PACK_DIR)
    genesis = pack.rules["worldgen"]
    sites = (genesis["map"]["extent"] // genesis["map"]["spacing"]) ** 2
    assert 200 <= sites <= 600, sites
    assert sites == 324, sites
    claims = {
        claim["location"]: claim["slot"]
        for claim in genesis["claims"]
    }
    assert len(claims) == 6, claims
    # the claim slots the world_formed template binds (its formed arm)
    events = _events(GOLDEN)
    formed = [
        e for e in events
        if e["type"] == "world_history" and e["outcome"]["kind"] == "world_formed"
    ]
    assert len(formed) == 1
    outcome = formed[0]["outcome"]
    assert outcome["sites"] == 324
    assert outcome["years"] == 150
    assert {claim["slot"] for claim in outcome["claims"]} == {
        "weir_water", "road_ground", "keep_height", "bank_ground",
        "croft_hills", "mill_bank",
    }
    # the history lines: events_max - 1 = 4 remembered beats
    history = [
        e for e in events
        if e["type"] == "world_history" and "year" in e["outcome"]
    ]
    assert len(history) == 4


# -- the AP crosswalk's first committed consumer (D-148/D-152) ----------------


def test_spine_records_live_and_consumed() -> None:
    """The province is the first committed pack to carry spine records
    (PACK_SPEC §6, AP-9): five NPCs declare the want/need tension with
    a flaw rooted in a cause, and every flaw is consumed by an urgency
    entry's flaw key (AP-8) — the crosswalk's first non-crafted
    instance, the row the lint (iter-117) was built for."""
    pack = load_pack(PACK_DIR)
    spines = {
        npc["id"]: npc["spine"]
        for npc in pack.entities["npcs"]
        if "spine" in npc
    }
    assert len(spines) == 5, spines
    flaws = {spine["flaw"] for spine in spines.values()}
    consumed = {
        entry["flaw"]
        for entry in pack.rules["urgencies"]["entries"]
        if "flaw" in entry
    }
    assert flaws == consumed, (
        f"the declared flaws and the consumed flaws disagree: "
        f"{flaws ^ consumed}"
    )
    # every flaw-consuming entry belongs to the spine's own NPC
    by_npc = {npc: spine["flaw"] for npc, spine in spines.items()}
    for entry in pack.rules["urgencies"]["entries"]:
        if "flaw" in entry:
            assert by_npc[entry["npc"]] == entry["flaw"], entry


def test_the_budget_block_declares_the_skeleton_shape() -> None:
    """AP-1's first committed consumer: the budget block bounds the
    skeleton slice's own shape (7 npcs, 5 items, 6 hooks, 46 template
    families) — the pack's honesty about its scale, growth inside the
    bounds or a deliberate re-declare."""
    pack = load_pack(PACK_DIR)
    budget = pack.rules["budget"]
    assert budget["npcs"]["min"] <= len(pack.entities["npcs"]) <= budget["npcs"]["max"]
    assert budget["items"]["min"] <= len(pack.entities["items"]) <= budget["items"]["max"]
    hooks = len(pack.rules["director"]["hooks"])
    assert budget["hooks"]["min"] <= hooks <= budget["hooks"]["max"]
    templates = len(pack.templates["events"])
    assert budget["templates"]["min"] <= templates <= budget["templates"]["max"]
