"""iter-3 acceptance — the knowledge system (phase0 §3):

- T3 blind-NPC: no record → cannot know, cannot say; the view is the
  derived memory (L3) and rebuilds from the log (the T2 truth-test).
- Movement sightings: origin observers see the departure, destination
  observers the arrival (records on the movement events, pack templates).
- Transfer (D-007): one fidelity step down, channel told; the telling
  reaction (P2c) shares the teller's most salient NOVEL fact — importance
  before recency, the triggering conversation's own records excluded.
- Acceptance: base + trust weight − teller penalty (pack numbers); a
  rejected telling is a fact with no records.
- Expectations (P2d, KI#3): a violated rule emits an inferred record
  cause-chained to the event that moved the item on the violated axis;
  repeated rotations never duplicate a noticed violation; at_location
  rules need the watcher on site.

Seeds are probed to be deterministic (T1 discipline).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.knowledge import KnowledgeView, trust_toward
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")


def make_sim(tmp_path: Path, seed: int, name: str = "run.jsonl",
             pack: Pack = PACK) -> Simulator:
    return Simulator(pack, seed, tmp_path / name, SCHEMA, commit="0000000")


def script(steps: list[dict[str, Any]], seed: int) -> dict[str, Any]:
    return {"name": "test", "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}


def run(tmp_path: Path, seed: int, steps: list[dict[str, Any]],
        pack: Pack = PACK, name: str = "run.jsonl") -> tuple[list[Any], Simulator]:
    sim = make_sim(tmp_path, seed, name, pack)
    sim.run_playscript(script(steps, seed))
    _, events = read_log(tmp_path / name, SCHEMA)
    return events, sim


def by_type(events: list[Any], event_type: str) -> list[Any]:
    return [e for e in events if e.type == event_type]


# -- movement sightings ---------------------------------------------------------


def test_move_records_sightings_at_both_ends(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 42, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "move", "target": "loc_backyard"},
    ])
    first, second = by_type(events, "move")
    # destination observers saw the arrival (the player was never a knower)
    arrived = {r.who for r in first.knowledge if r.knows == "pc_01_arrived"}
    assert arrived == {"npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01"}
    assert all(r.channel == "saw" and r.fidelity == "partial" for r in first.knowledge)
    # origin observers saw the departure toward the backyard
    left = {r.who for r in second.knowledge if r.knows == "pc_01_left_toward_loc_backyard"}
    assert left == {"npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01"}
    # nobody was in the backyard to see the arrival
    assert not any(r.knows == "pc_01_arrived" for r in second.knowledge)


def test_flee_records_arrival_sighting_at_the_destination(tmp_path: Path) -> None:
    events, _ = run(tmp_path, 42, [
        {"intent": "flee", "target": "loc_market"},
    ])
    flee = by_type(events, "flee")[0]
    arrived = {r.who: r.knows for r in flee.knowledge}
    # the street was empty; the market crowd saw the runner burst in
    assert arrived == {"npc_market_crowd_01": "pc_01_arrived_fleeing"}


# -- T3: blind NPC ------------------------------------------------------------


def test_blind_npc_holds_nothing_and_cannot_say(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 42, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01"},  # seed 42: silent success
    ])
    # the relief watcher was in the guard room the whole time: nothing seen,
    # nothing heard, nobody told him — and no rotation ran before tick 360
    assert sim.knowledge.records_of("npc_guard_02") == ()
    assert not by_type(events, "knowledge_transfer")
    assert not by_type(events, "rumor_told")


def test_blind_npc_tells_nothing_on_talk(tmp_path: Path) -> None:
    # co-location implies the movement sighting: the relief watcher sees the
    # player walk in — and that arrival record is ALL he ever gets. The tavern
    # scene (theft, noise) stays strictly with its own witnesses (T3).
    events, sim = run(tmp_path, 42, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01"},  # seed 42: silent success
        {"intent": "move", "target": "loc_street"},
        {"intent": "move", "target": "loc_guardroom"},
        {"intent": "talk", "target": "npc_guard_02"},
    ])
    guard_records = [r.knows for r in sim.knowledge.records_of("npc_guard_02")]
    # blind to the tavern scene: only his own arrival sighting + this talk
    assert guard_records == ["pc_01_arrived", "conversation_with_pc_01"]
    for telling in by_type(events, "rumor_told"):
        assert telling.actor == "npc_guard_02"
        # a knower of nothing but the arrival can say nothing but the arrival
        assert telling.outcome["knows"] == "pc_01_arrived"
        for record in telling.knowledge:
            assert record.knows == "pc_01_arrived"


def test_crowd_only_knows_what_it_witnessed(tmp_path: Path) -> None:
    _, sim = run(tmp_path, 42, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "move", "target": "loc_street"},
        {"intent": "move", "target": "loc_market"},
    ])
    crowd = [
        (r.knows, r.channel, r.fidelity)
        for r in sim.knowledge.records_of("npc_market_crowd_01")
    ]
    # the crowd saw exactly one thing: the arrival. No theft, no tavern noise.
    assert crowd == [("pc_01_arrived", "saw", "partial")]


# -- the telling reaction (P2c) + transfer decay (D-007) ------------------------


def test_talk_shares_salient_fact_decayed_and_told(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 1, [  # seed 1: the steal fails (guard saw, partial)
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01"},
        {"intent": "talk", "target": "npc_guard_01"},
    ])
    talk = by_type(events, "talk")[0]
    telling = by_type(events, "rumor_told")
    assert len(telling) == 1
    assert telling[0].actor == "npc_guard_01" and telling[0].target == "pc_01"
    assert telling[0].cause == talk.id
    assert telling[0].outcome["knows"] == "figure_reaching_for_purse"
    # salience: the medium-importance crime record beats the low arrival record
    # decay: the guard's saw/partial passes told/vague (one step down, D-007)
    player = [(r.knows, r.channel, r.fidelity)
              for r in sim.knowledge.records_of("pc_01")]
    assert ("figure_reaching_for_purse", "told", "vague") in player
    # the guard still holds his own record — telling copies, never moves
    assert ("figure_reaching_for_purse", "saw", "partial") in [
        (r.knows, r.channel, r.fidelity)
        for r in sim.knowledge.records_of("npc_guard_01")
    ]


def test_second_talk_never_re_shares_the_same_fact(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 1, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01"},
        {"intent": "talk", "target": "npc_guard_01"},
        {"intent": "talk", "target": "npc_guard_01"},
    ])
    tellings = by_type(events, "rumor_told")
    shared = [e.outcome["knows"] for e in tellings]
    # the crime fact passes once; the next talk shares only the next salient
    # novel record — the first conversation itself (low importance, newest) —
    # a listener never re-learns a token they already hold
    assert shared.count("figure_reaching_for_purse") == 1
    assert len(tellings) == 2 and shared[1] == "conversation_with_pc_01"
    player_tokens = [r.knows for r in sim.knowledge.records_of("pc_01")]
    assert player_tokens.count("figure_reaching_for_purse") == 1


def test_rejected_telling_is_a_fact_without_records(tmp_path: Path) -> None:
    target = tmp_path / "deaf_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text())
    rules["knowledge"]["rumor_acceptance"]["base"] = -100  # never accepted
    (target / "rules.json").write_text(json.dumps(rules))
    deaf = load_pack(target)

    events, sim = run(tmp_path, 1, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01"},
        {"intent": "talk", "target": "npc_guard_01"},
    ], pack=deaf)
    telling = by_type(events, "rumor_told")
    assert len(telling) == 1
    assert telling[0].outcome["accepted"] is False
    assert telling[0].knowledge == ()  # nothing passed — the listener learns nothing
    assert not any(r.knows == "figure_reaching_for_purse"
                   for r in sim.knowledge.records_of("pc_01"))


# -- trust lookup (P2a pair map; the Influence Boundary holds) ------------------


def test_trust_reads_pair_map_then_player_axis_then_neutral(tmp_path: Path) -> None:
    sim = make_sim(tmp_path, 42, name="trust.jsonl")
    sim.run_playscript(script([{"intent": "wait", "ticks": 1}], 42))
    projection = sim.projection
    # pair map (P2a): the watchers trust each other, seeded from the pack
    assert projection["npc_guard_01"]["pair.npc_guard_02.trust"] == 75
    assert trust_toward(PACK, projection, "npc_guard_02", "npc_guard_01", "trust") == 75
    # toward-the-player axis (v0.1 semantics)
    assert trust_toward(PACK, projection, "npc_barkeep_01", "pc_01", "trust") == 50
    # the player has no pair map and no relations: neutral
    assert trust_toward(PACK, projection, "pc_01", "npc_barkeep_01", "trust") == 50


# -- expectations (P2d, KI#3) ----------------------------------------------------


def test_silent_theft_noticed_as_expectation_violation(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 42, [  # seed 42: the steal succeeds unseen
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "wait", "ticks": 400},  # crosses the watch rotation
    ])
    steal = by_type(events, "steal")[0]
    move = by_type(events, "move")[-1]
    violations = by_type(events, "expectation_violation")
    assert len(violations) == 1
    assert violations[0].actor == "npc_guard_01"
    assert violations[0].target == "purse_01"
    # cause-chained to the CARRIER mover (the theft), not the later position move
    assert violations[0].cause == steal.id and violations[0].cause != move.id
    record = violations[0].knowledge[0]
    assert (record.who, record.channel, record.fidelity, record.knows) == (
        "npc_guard_01", "inferred", "exact", "purse_missing"
    )
    # the violation feeds the crime reaction (suspicion 0→20) and spreads
    # to the relief watcher through the briefing (dedup: told once, partial)
    assert sim.projection["npc_guard_01"]["relations.suspicion"] == 20
    assert sim.projection["npc_guard_02"]["relations.suspicion"] == 20
    transfer = by_type(events, "knowledge_transfer")[0]
    spread = [r for r in transfer.knowledge if r.knows == "purse_missing"]
    assert spread[0].channel == "told" and spread[0].fidelity == "partial"
    # under the status threshold: no flip — suspicion-from-absence is legal,
    # arrest-on-absence stays impossible without the threshold
    assert sim.projection["pc_01"]["crime_status"] == "unknown"


def test_repeated_rotations_never_duplicate_the_violation(tmp_path: Path) -> None:
    events, _ = run(tmp_path, 42, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "wait", "ticks": 1100},  # crosses BOTH rotations (360 and 1080)
    ])
    assert len(by_type(events, "watch_change")) == 2
    assert len(by_type(events, "expectation_violation")) == 1
    # the second briefing finds nothing new: every token is already held
    assert len(by_type(events, "knowledge_transfer")) == 1


def test_at_location_expectation_needs_the_watcher_on_site(tmp_path: Path) -> None:
    target = tmp_path / "site_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    entities = json.loads((target / "entities.json").read_text())
    rules = json.loads((target / "rules.json").read_text())
    # move the rope into the tavern so the rules hold at t=0 (lint demands it)
    for item in entities["items"]:
        if item["id"] == "rope_01":
            item["position"] = "loc_tavern"
    (target / "entities.json").write_text(json.dumps(entities))
    rules["expectations"]["rules"] = [
        # the maid is on site at the tavern: she notices the rope leaving
        {"npc": "npc_maid_01", "item": "rope_01", "at_location": "loc_tavern",
         "knows": "rope_gone_from_tavern"},
        # the second watcher is at the guard room when the checks run (the
        # rotation moved him off the duty post): the same absence stays unseen
        {"npc": "npc_guard_01", "item": "rope_01", "at_location": "loc_tavern",
         "knows": "rope_gone_seen_by_absentee"},
    ]
    (target / "rules.json").write_text(json.dumps(rules))
    site_pack = load_pack(target)

    events, sim = run(tmp_path, 13, [  # seed 13: the take succeeds unnoticed
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "take", "target": "rope_01"},
        {"intent": "move", "target": "loc_street"},
        {"intent": "wait", "ticks": 400},
    ], pack=site_pack)
    violations = by_type(events, "expectation_violation")
    assert len(violations) == 1
    assert violations[0].actor == "npc_maid_01"
    # cause = the move that changed the rope's POSITION (not the take that
    # changed its carrier — the at_location axis watches position)
    moves = by_type(events, "move")
    assert violations[0].cause == moves[-1].id
    assert sim.projection["rope_01"]["position"] == "loc_street"


# -- the derived view rebuilds from the log (T2 for knowledge) -------------------


def test_knowledge_view_rebuilds_from_the_log(tmp_path: Path) -> None:
    _, sim = run(tmp_path, 42, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "wait", "ticks": 400},
    ])
    _, events = read_log(tmp_path / "run.jsonl", SCHEMA)
    rebuilt = KnowledgeView.from_events(events)
    assert sim.knowledge.knowers() == rebuilt.knowers()
    for who in rebuilt.knowers():
        assert sim.knowledge.records_of(who) == rebuilt.records_of(who)
