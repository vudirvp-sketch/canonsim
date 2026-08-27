"""iter-3 acceptance — the crime-and-watch system (phase0 §3): NPC memory
driving behavior. The ev_0007 shape lands on the reacting system (suspicion
0→25 together with the crime-status flip), knowers react only to their OWN
novel records (EPIST-1), the watch rotation swaps the posts and the briefing
spreads knowledge with one-step decay (D-006), crossing the arrest threshold
co-located with the suspect emits the attempt, and a rotation landing
mid-action is the natural intent-OCC trigger (KI#12).

Seeds are probed to be deterministic (T1 discipline); thresholds below 75
run through crafted pack copies (the established mechanism-proof pattern —
balance tuning belongs to the iter-6 harness).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.crime import next_rotation_tick
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")

TAVERN = [{"intent": "move", "target": "loc_tavern"}]


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


def tuned_pack(tmp_path: Path, mutate: Any) -> Pack:
    """A pack copy with tuned crime_watch numbers (mechanism proof)."""
    target = tmp_path / "tuned_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text())
    mutate(rules["crime_watch"])
    (target / "rules.json").write_text(json.dumps(rules))
    return load_pack(target)


# -- the ev_0007 shape on the reacting system ----------------------------------


def test_steal_failure_reactions_match_ev_0007(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 1, TAVERN + [  # seed 1: partial failure
        {"intent": "steal", "target": "npc_guard_01"},
    ])
    failed = by_type(events, "pickpocket_failed")[0]
    reactions = by_type(events, "suspicion_changed")
    # one reaction per knower, all cause-chained to the failed attempt
    assert {e.actor for e in reactions} == {
        "npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    }
    assert all(e.cause == failed.id for e in reactions)
    # the watcher saw (partial): +25 AND the status flip on the same event
    guard = next(e for e in reactions if e.actor == "npc_guard_01")
    assert guard.outcome == {
        "token": "figure_reaching_for_purse", "source": "witnessed_steal_failure",
        "delta": 25, "from": 0, "to": 25,
    }
    assert guard.state_changes == (
        guard.state_changes[0].__class__(  # same shape, explicit below
            entity="npc_guard_01", prop="relations.suspicion", from_=0, to_=25),
        guard.state_changes[0].__class__(
            entity="pc_01", prop="crime_status", from_="unknown", to_="suspect"),
    )
    # everyone else heard (vague): +10 each, no status change of their own
    others = [e for e in reactions if e.actor != "npc_guard_01"]
    assert all(e.outcome["delta"] == 10 for e in others)
    assert all(len(e.state_changes) == 1 for e in others)
    # the flip happened exactly once; reactions carry no knowledge of their own
    assert sim.projection["pc_01"]["crime_status"] == "suspect"
    assert all(e.knowledge == () for e in reactions)
    # characters know different things and react differently (the AC)
    assert sim.projection["npc_guard_01"]["relations.suspicion"] == 25
    assert sim.projection["npc_barkeep_01"]["relations.suspicion"] == 10


def test_repeated_evidence_never_re_escalates(tmp_path: Path) -> None:
    # crafted copy: steal difficulty 90 (both attempts fail) and a huge
    # failure_margin (both failures partial — identical record families, the
    # total-failure branch would legitimately produce NOVEL tokens for the
    # other onlookers: saw where they had only heard)
    target = tmp_path / "novelty_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text())
    rules["checks"]["failure_margin"] = 100
    rules["crime_watch"]["arrest"]["requires_suspicion"] = 99
    (target / "rules.json").write_text(json.dumps(rules))
    actions = json.loads((target / "actions.json").read_text())
    for action in actions["actions"]:
        if action["intent"] == "steal":
            action["check"]["difficulty"] = 90
    (target / "actions.json").write_text(json.dumps(actions))
    novelty = load_pack(target)

    events, sim = run(tmp_path, 1, TAVERN + [
        {"intent": "steal", "target": "npc_guard_01"},
        {"intent": "steal", "target": "npc_guard_01"},
    ], pack=novelty)
    # two partial failures, same tokens: only the FIRST acquisition reacts
    assert len(by_type(events, "pickpocket_failed")) == 2
    assert len(by_type(events, "suspicion_changed")) == 4  # from attempt one only
    assert sim.projection["npc_guard_01"]["relations.suspicion"] == 25
    assert sim.projection["npc_barkeep_01"]["relations.suspicion"] == 10


def test_player_knowledge_moves_no_suspicion(tmp_path: Path) -> None:
    # the player hears his own crime retold (telling reaction): the player has
    # no suspicion axis — nothing reacts (EPIST-1: own state + own knowledge)
    events, _ = run(tmp_path, 1, TAVERN + [
        {"intent": "steal", "target": "npc_guard_01"},
        {"intent": "talk", "target": "npc_guard_01"},
    ])
    telling = by_type(events, "rumor_told")[0]
    assert telling.knowledge[0].who == "pc_01"
    assert not by_type(events, "arrest_attempt")
    assert len(by_type(events, "suspicion_changed")) == 4  # unchanged by the telling


# -- arrest: memory driving behavior ---------------------------------------------


def test_arrest_attempt_on_threshold_crossing_co_located(tmp_path: Path) -> None:
    pack = tuned_pack(tmp_path, lambda cw: cw["arrest"].__setitem__(
        "requires_suspicion", 20))  # the failed steal's +25 crosses it
    events, sim = run(tmp_path, 1, TAVERN + [
        {"intent": "steal", "target": "npc_guard_01"},
    ], pack=pack)
    arrest = by_type(events, "arrest_attempt")
    assert len(arrest) == 1
    guard_reaction = next(e for e in by_type(events, "suspicion_changed")
                          if e.actor == "npc_guard_01")
    assert arrest[0].actor == "npc_guard_01" and arrest[0].target == "pc_01"
    # cause-chained to THIS watcher's suspicion event — not to the theft
    assert arrest[0].cause == guard_reaction.id
    assert arrest[0].outcome == {"suspicion": 25, "threshold": 20}
    assert arrest[0].state_changes == ()  # the attempt is a fact
    # iter-4: the arrest_resolved event follows immediately (the same
    # commit-door cascade), drawing evasion_vs_pursuit. With seed 1 the
    # pursuit holds: the suspect is caught (crime_status → caught, T4).
    resolution = by_type(events, "arrest_resolved")
    assert len(resolution) == 1
    assert resolution[0].actor == "npc_guard_01" and resolution[0].target == "pc_01"
    assert resolution[0].cause == arrest[0].id
    assert resolution[0].outcome["caught"] is True
    assert sim.projection["pc_01"]["crime_status"] == "caught"


def test_no_arrest_when_the_suspect_is_elsewhere(tmp_path: Path) -> None:
    pack = tuned_pack(tmp_path, lambda cw: cw["arrest"].__setitem__(
        "requires_suspicion", 20))
    # seed 42: the theft succeeds silently; the expectation violation at the
    # rotation crosses 20 — but the player is in the backyard, the watcher
    # at the guard room: no attempt
    events, _ = run(tmp_path, 42, TAVERN + [
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "wait", "ticks": 400},
    ], pack=pack)
    assert len(by_type(events, "expectation_violation")) == 1
    assert not by_type(events, "arrest_attempt")


# -- watch rotation + the briefing (D-006) ---------------------------------------


def test_rotation_swaps_posts_and_briefs_the_relief(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 1, TAVERN + [
        {"intent": "steal", "target": "npc_guard_01"},
        {"intent": "wait", "ticks": 400},  # crosses tick 360
    ])
    watch = by_type(events, "watch_change")
    assert len(watch) == 1
    assert watch[0].actor == "world"
    assert watch[0].outcome == {"outgoing": "npc_guard_01", "incoming": "npc_guard_02"}
    assert sim.projection["npc_guard_01"]["position"] == "loc_guardroom"
    assert sim.projection["npc_guard_02"]["position"] == "loc_tavern"
    # the briefing: everything the outgoing holder knew passes, told,
    # one fidelity step down (saw/partial → told/vague), deduped
    transfer = by_type(events, "knowledge_transfer")
    assert len(transfer) == 1
    assert transfer[0].actor == "npc_guard_01" and transfer[0].target == "npc_guard_02"
    assert transfer[0].cause == watch[0].id
    passed = {(r.knows, r.channel, r.fidelity) for r in transfer[0].knowledge}
    assert ("figure_reaching_for_purse", "told", "vague") in passed
    assert ("pc_01_arrived", "told", "vague") in passed
    # the relief reacts to what he was told: +25, cause-chained to the briefing
    relief = next(e for e in by_type(events, "suspicion_changed")
                  if e.actor == "npc_guard_02")
    assert relief.outcome["delta"] == 25 and relief.cause == transfer[0].id
    assert sim.projection["npc_guard_02"]["relations.suspicion"] == 25
    # the second rotation (tick 1080, crossed by nothing here) never ran
    assert len(by_type(events, "watch_change")) == 1


def test_second_rotation_swaps_back_without_a_transfer(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 1, [
        {"intent": "wait", "ticks": 1100},  # crosses 360 AND 1080
    ])
    assert len(by_type(events, "watch_change")) == 2
    # back at the original posts: the pair rotated and rotated back
    assert sim.projection["npc_guard_01"]["position"] == "loc_tavern"
    assert sim.projection["npc_guard_02"]["position"] == "loc_guardroom"
    # nothing to brief the second time: both hold the same (empty) memory
    assert not by_type(events, "knowledge_transfer")


def test_rotation_tick_arithmetic_repeats_daily() -> None:
    rules = dict(PACK.rules)
    assert next_rotation_tick(rules, 1440, 0) == 360
    assert next_rotation_tick(rules, 1440, 360) == 1080
    assert next_rotation_tick(rules, 1440, 1080) == 1440 + 360  # day 1
    assert next_rotation_tick(rules, 1440, 1500) == 1440 + 360


def test_no_rotation_before_the_first_offset(tmp_path: Path) -> None:
    events, _ = run(tmp_path, 1, [{"intent": "wait", "ticks": 300}])
    assert len(events) == 1 and not by_type(events, "watch_change")


# -- intent OCC: the natural e2e trigger (KI#12) ----------------------------------


def test_rotation_mid_action_rejects_the_intent_with_the_breaking_cause(
    tmp_path: Path,
) -> None:
    # the move draws 2..4 ticks: proposal lands at 357..359, completion at
    # 360..362 — the rotation at 360 breaks same_location in between, for
    # every possible draw (no seed fragility)
    events, sim = run(tmp_path, 42, TAVERN + [
        {"intent": "wait", "ticks": 355},
        {"intent": "steal", "target": "npc_guard_01"},
    ])
    watch = by_type(events, "watch_change")[0]
    rejection = by_type(events, "intent_rejected")[0]
    assert rejection.outcome == {
        "action": "steal", "reason": "projection_moved",
        "failed_test": "target.same_location",
    }
    # the cause is the event whose application broke the precondition
    assert rejection.cause == watch.id
    # the world did not change: the purse stayed, no crime reaction fired
    assert sim.projection["purse_01"]["carrier"] == "npc_guard_01"
    assert not by_type(events, "suspicion_changed")
    assert rejection.state_changes == () and rejection.knowledge == ()
