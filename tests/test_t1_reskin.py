"""T1-reskin — determinism for the road pack (world-2 L1, iter-112: the
reskin day, ROADMAP §2's phase-6 exit instrument).

Same seed + same playscript + same environment = byte-identical logs,
measured against the committed golden fixture
(`tests/fixtures/road_smoke_seed42.jsonl`) — the tavern T1's exact
shape (`tests/test_t1_determinism.py`), re-run over the SECOND pack: a
pack that is data-only proves the universal-core claim (zero engine
edits between the two fixtures).

The travel-loop pins (the L1 claim itself): the move completions land
exactly at accept-t + the st-6a DERIVED price (`core/travel.py` —
integer math over the genesis-frozen WorldModel, draw-free: the
fingerprint stays 0), and encounters fire MID-TRAVEL (D-038 — beats,
rotations and knowledge transfers land inside the legs' tick windows).
"""

from __future__ import annotations

import json
from pathlib import Path

from core.loop import Simulator, load_playscript
from core.pack import load_pack
from core.travel import travel_ticks

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
GOLDEN = REPO / "tests" / "fixtures" / "road_smoke_seed42.jsonl"
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "road_smoke.json")
PACK_DIR = REPO / "content" / "road_pack"

#: The route the smoke script walks (origin -> destination per move
#: step): the river road's four legs, prices read from the travel law.
LEGS: tuple[tuple[str, str], ...] = (
    ("loc_street", "loc_tavern"),
    ("loc_tavern", "loc_backyard"),
    ("loc_backyard", "loc_street"),
    ("loc_street", "loc_market"),
)
#: The two waits between the legs (the script's own data).
WAITS: tuple[int, ...] = (30, 15)


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
        "road fixture regeneration diverged from the committed fixture — "
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


# -- the travel-loop pins (world-2 L1's own claims) -------------------------


def test_derived_prices_pin_the_route(tmp_path: Path) -> None:
    """Every move completion lands exactly at accept-t + travel_ticks:
    the derived price IS the route's law. The expected clock is rebuilt
    from the travel law + the script's own waits — a price change
    without a fixture regen fails BOTH here and the regen guard; this
    test names why."""
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
    # the expected completion clock: step 1 accepts at t=0; each later
    # step accepts when the previous one completed (run_playscript
    # drains the queue between steps).
    clock = 0
    expected: list[tuple[int, str]] = []
    for index, (_origin, destination) in enumerate(LEGS):
        clock += prices[index]
        expected.append((clock, destination))
        if index < len(WAITS):
            clock += WAITS[index]
    moves = [
        (event["t"], event["target"])
        for event in _events(tmp_path / "prices.jsonl")
        if event["type"] == "move"
    ]
    assert moves == expected


def test_encounters_fire_mid_travel(tmp_path: Path) -> None:
    """D-038, the loop-change claim: beats/rotations/knowledge transfers
    land strictly INSIDE the travel legs' tick windows — encounters
    ride the route. The measured instance: the watch change + the
    knowledge transfer at t=360, inside the 180 -> 540 leg."""
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
        if index < len(WAITS):
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
