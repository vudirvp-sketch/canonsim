"""End-to-end tests of the tick driver + playscript runner (iter-1 AC):
world creates from seed, an event writes, a playscript plays end-to-end.
T2 in its iter-1 form: fold(log) == runtime projection (STATE-1). Negative
tests prove the loud failures: teleport stays impossible (T5 seed), unknown
intents, not-yet-landed action resolvers, malformed steps, script/run
mismatches.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.fold import fold, initial_projection
from core.log import read_log
from core.loop import RunnerError, Simulator, load_playscript
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")


def make_sim(tmp_path: Path, seed: int = 42) -> Simulator:
    return Simulator(PACK, seed, tmp_path / f"run_{seed}.jsonl", SCHEMA, commit="0000000")


def script(steps: list[dict[str, Any]], seed: int = 42) -> dict[str, Any]:
    return {"name": "test", "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}


def test_world_creates_from_seed_and_first_event_writes(tmp_path: Path) -> None:
    sim = make_sim(tmp_path)
    assert sim.projection["pc_01"]["position"] == "loc_street"  # world exists
    result = sim.run_playscript(script([{"intent": "wait", "ticks": 5}]))
    assert result.event_count == 1
    header, events = read_log(tmp_path / "run_42.jsonl", SCHEMA)
    assert header["seed"] == 42
    assert events[0].id == "ev_0000" and events[0].cause is None  # run-start event


def test_playscript_plays_end_to_end(tmp_path: Path) -> None:
    playscript = load_playscript(REPO / "tests" / "playscripts" / "plumbing_smoke.json")
    sim = make_sim(tmp_path)
    result = sim.run_playscript(playscript)
    assert result.event_count == 6
    assert sim.projection["pc_01"]["position"] == "loc_market"  # the walk happened
    _, events = read_log(tmp_path / "run_42.jsonl", SCHEMA)
    # linear cause chain: run-start, then each event chains to its predecessor
    for previous, event in zip(events, events[1:], strict=False):
        assert event.cause == previous.id
    # every provenance names the intent it resolves (§7)
    assert [e.provenance["cause_intent"] for e in events] == [
        f"intent_{i:04d}" for i in range(6)
    ]
    # move events carry the position delta; wait events change nothing
    moves = [e for e in events if e.type == "move"]
    assert all(len(e.state_changes) == 1 for e in moves)
    waits = [e for e in events if e.type == "wait"]
    assert all(e.state_changes == () for e in waits)


def test_t2_fold_equals_runtime_projection(tmp_path: Path) -> None:
    playscript = load_playscript(REPO / "tests" / "playscripts" / "plumbing_smoke.json")
    sim = make_sim(tmp_path)
    sim.run_playscript(playscript)
    _, events = read_log(tmp_path / "run_42.jsonl", SCHEMA)
    rebuilt = fold(events, initial_projection(PACK.entities))
    assert rebuilt == sim.projection  # STATE-1: two paths, one truth


def test_teleport_stays_impossible(tmp_path: Path) -> None:
    sim = make_sim(tmp_path)
    # loc_street is a hub (adjacent to everything); from the tavern only the
    # street and the backyard are reachable — the market is not.
    far = script([
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "move", "target": "loc_market"},
    ])
    with pytest.raises(RunnerError, match="teleport"):
        sim.run_playscript(far)


def test_unknown_intent_is_loud(tmp_path: Path) -> None:
    sim = make_sim(tmp_path)
    with pytest.raises(RunnerError, match="unknown intent"):
        sim.run_playscript(script([{"intent": "fly", "target": "loc_tavern"}]))


def test_check_bearing_actions_land_iter_2(tmp_path: Path) -> None:
    sim = make_sim(tmp_path)
    with pytest.raises(RunnerError, match="iter-2"):
        sim.run_playscript(script([{"intent": "steal", "target": "npc_guard_01"}]))


def test_wait_requires_positive_ticks(tmp_path: Path) -> None:
    sim = make_sim(tmp_path)
    with pytest.raises(RunnerError, match="positive integer"):
        sim.run_playscript(script([{"intent": "wait", "ticks": 0}]))
    sim2 = make_sim(tmp_path)
    with pytest.raises(RunnerError, match="positive integer"):
        sim2.run_playscript(script([{"intent": "wait"}]))


def test_move_rejects_extra_fields_and_missing_target(tmp_path: Path) -> None:
    sim = make_sim(tmp_path)
    with pytest.raises(RunnerError, match="no extra step fields"):
        sim.run_playscript(script([{"intent": "move", "target": "loc_tavern",
                                    "method": "sneaky"}]))
    sim2 = make_sim(tmp_path)
    with pytest.raises(RunnerError, match="requires a target"):
        sim2.run_playscript(script([{"intent": "move"}]))


def test_script_must_match_seed_and_pack(tmp_path: Path) -> None:
    sim = make_sim(tmp_path, seed=7)
    with pytest.raises(RunnerError, match="seed"):
        sim.run_playscript(script([], seed=42))
    sim2 = make_sim(tmp_path)
    wrong_pack = script([])
    wrong_pack["pack"] = "other_pack@9.9"
    with pytest.raises(RunnerError, match="pack"):
        sim2.run_playscript(wrong_pack)


def test_empty_playscript_writes_header_only(tmp_path: Path) -> None:
    sim = make_sim(tmp_path)
    result = sim.run_playscript(script([]))
    assert result.event_count == 0
    lines = (tmp_path / "run_42.jsonl").read_text().splitlines()
    assert len(lines) == 1 and json.loads(lines[0])["header"] is True


def test_event_types_stay_within_pack_vocabulary(tmp_path: Path) -> None:
    sim = make_sim(tmp_path)
    sim.run_playscript(script([{"intent": "move", "target": "loc_tavern"}]))
    _, events = read_log(tmp_path / "run_42.jsonl", SCHEMA)
    assert all(event.type in PACK.event_types() for event in events)
