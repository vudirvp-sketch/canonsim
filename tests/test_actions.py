"""End-to-end tests of the 12 actions through the Simulator — the iter-2
acceptance criteria: steal / arson / talk are facts in the log with
knowledge records, and impossible stays impossible (T5 partial).

Branch coverage uses seeds probed to be deterministic (T1 discipline: same
seed + pack + code = same log). The v0.1 pack numbers make low-difficulty
environment checks auto-succeed for an unmodified actor — the failure
branches of talk/examine/use/distract are exercised through a crafted pack
copy with raised difficulties (mechanism proof; balance is the iter-6
harness's territory).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.fold import fold, initial_projection
from core.log import StateChange, read_log
from core.loop import Simulator, load_playscript
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


def hard_pack(tmp_path: Path, difficulties: dict[str, int]) -> Pack:
    """A pack copy with raised check difficulties — the failure branches."""
    target = tmp_path / "hard_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    actions = json.loads((target / "actions.json").read_text())
    for action in actions["actions"]:
        if action["intent"] in difficulties and action["check"] is not None:
            action["check"]["difficulty"] = difficulties[action["intent"]]
    (target / "actions.json").write_text(json.dumps(actions))
    return load_pack(target)


TAVERN_STEPS = [{"intent": "move", "target": "loc_tavern"}]


# -- the AC trio: steal / arson / talk ------------------------------------------


def test_steal_success_transfers_the_item(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    ])
    steal = events[-1]
    assert steal.type == "steal" and steal.outcome["stolen"] == "purse_01"
    assert sim.projection["purse_01"]["carrier"] == "pc_01"  # the lift happened
    assert steal.knowledge == ()  # unseen: no records for others
    assert steal.provenance["cause_intent"].startswith("intent_")


def test_steal_partial_failure_records_ev_0007_family(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 1, TAVERN_STEPS + [
        {"intent": "steal", "target": "npc_guard_01"},
    ])
    failed = next(e for e in events if e.type == "pickpocket_failed")
    assert failed.outcome["check"]["passed"] is False
    assert not failed.outcome["check"]["total_failure"]
    assert sim.projection["purse_01"]["carrier"] == "npc_guard_01"  # nothing moved
    saw = {r.who for r in failed.knowledge if r.knows == "figure_reaching_for_purse"}
    heard = {r.who for r in failed.knowledge if r.knows == "noise_by_the_bar"}
    # the target saw (partial); the other tavern occupants heard (vague) — ev_0007
    assert saw == {"npc_guard_01"}
    assert heard == {"npc_barkeep_01", "npc_drunk_01", "npc_maid_01"}
    by_channel = {(r.who, r.channel, r.fidelity) for r in failed.knowledge}
    assert ("npc_guard_01", "saw", "partial") in by_channel
    assert ("npc_barkeep_01", "heard", "vague") in by_channel
    # iter-43: the steal failure registers the institutional consequence
    # — both watcher halves (D-072: the seeded watcher's + the relief's);
    # iter-52: + the room's latent wariness (the arc driver's seed, the
    # aftermath chain's second member, content-6/D-081 — appended last)
    assert set(failed.hooks) == {
        "guard_suspicious_of_pc",
        "possible_document_check",
        "possible_document_check_relief",
        "barkeep_wary_sweep",
    }
    # tune-1: pickpocket_failed is story-critical (raw 1+2 hooks) + hook 2
    # = 5 -> high; it was "medium" before the story-critical score term.
    assert failed.importance == "high"


def test_steal_total_failure_everyone_saw(tmp_path: Path) -> None:
    events, _ = run(tmp_path, 2, TAVERN_STEPS + [
        {"intent": "steal", "target": "npc_guard_01"},
    ])
    failed = next(e for e in events if e.type == "pickpocket_failed")
    assert failed.outcome["check"]["total_failure"] is True
    saw = {r.who for r in failed.knowledge if r.knows == "figure_reaching_for_purse"}
    assert saw == {"npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01"}


def test_talk_both_parties_remember(tmp_path: Path) -> None:
    events, _ = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "talk", "target": "npc_barkeep_01"},
    ])
    talk = next(e for e in events if e.type == "talk")
    assert talk.type == "talk"
    records = {(r.who, r.knows) for r in talk.knowledge}
    assert records == {
        ("pc_01", "conversation_with_npc_barkeep_01"),
        ("npc_barkeep_01", "conversation_with_pc_01"),
    }
    assert all(r.channel == "told" and r.fidelity == "exact" for r in talk.knowledge)
    # iter-3: the telling reaction follows — the barkeep shares his most
    # salient fact (the sighting record born on the move)
    telling = [e for e in events if e.type == "rumor_told"]
    assert len(telling) == 1
    assert telling[0].actor == "npc_barkeep_01" and telling[0].target == "pc_01"
    assert telling[0].cause == talk.id


def test_talk_rebuffed_branch(tmp_path: Path) -> None:
    pack = hard_pack(tmp_path, {"talk": 90})
    events, _ = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "talk", "target": "npc_barkeep_01"},
    ], pack=pack, name="rebuff.jsonl")
    rebuff = events[-1]
    assert rebuff.type == "talk_rebuffed"
    assert rebuff.outcome["check"]["passed"] is False
    assert [(r.who, r.knows) for r in rebuff.knowledge] == [
        ("pc_01", "rebuffed_by_npc_barkeep_01")
    ]


def test_arson_chain_alarm_and_burnout(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "arson", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 200},
    ], name="arson.jsonl")
    by_type = {e.type: e for e in events}
    arson, started = by_type["arson"], by_type["fire_started"]
    # witnesses saw the figure starting the fire (the price marker, L8)
    assert {r.who for r in arson.knowledge} == {
        "npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    }
    assert all(r.channel == "saw" and r.fidelity == "partial"
               and r.knows == "figure_starting_fire" for r in arson.knowledge)
    # the fire itself: irreversible burning state, cause-chained to the action
    assert started.cause == arson.id
    assert started.actor == "world"
    spot_change = started.state_changes[0]
    assert spot_change.prop == "fire.bar" and spot_change.irreversible
    # alarm: fear spikes on the occupants, everyone hears
    alarm = by_type["alarm_raised"]
    assert alarm.cause == started.id
    assert {c.entity for c in alarm.state_changes} == {
        "npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    }
    assert all(c.prop == "status.fear" and c.to_ == 40 for c in alarm.state_changes)
    # the folded fear: the direct spike (40) + the panic echo (+10, the
    # through-the-walls contagion — content-2, D-077) = 50
    assert sim.projection["npc_guard_01"]["status.fear"] == 50
    heard = {r.who for r in alarm.knowledge}
    assert heard == {"pc_01", "npc_guard_01", "npc_barkeep_01",
                     "npc_drunk_01", "npc_maid_01"}
    # SEEDED follow-ups: smoke at +10, burnout at +120 (ignition tick 6)
    assert by_type["smoke_rising"].t == started.t + 10
    burnout = by_type["location_burned_out"]
    assert burnout.t == started.t + 120
    assert burnout.cause == started.id
    destroyed = burnout.state_changes[0]
    assert destroyed.prop == "destroyed" and destroyed.irreversible
    assert sim.projection["loc_tavern"]["destroyed"] is True  # T4: it stays burned
    assert sim.projection["loc_tavern"]["smoke"] is True


# -- the rest of the twelve --------------------------------------------------------


def test_look_around_scene_snapshot(tmp_path: Path) -> None:
    events, _ = run(tmp_path, 42, TAVERN_STEPS + [{"intent": "look_around"}])
    look = events[-1]
    assert look.type == "look_around"
    assert [(r.who, r.channel, r.fidelity, r.knows) for r in look.knowledge] == [
        ("pc_01", "saw", "exact", "scene_loc_tavern")
    ]


def test_examine_exact_and_vague_branches(tmp_path: Path) -> None:
    events, _ = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "examine", "target": "purse_01"},
    ])
    assert events[-1].type == "examine"
    assert events[-1].knowledge[0].knows == "details_purse_01"
    assert events[-1].knowledge[0].fidelity == "exact"
    pack = hard_pack(tmp_path, {"examine": 90})
    events, _ = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "examine", "target": "purse_01"},
    ], pack=pack, name="vague.jsonl")
    assert events[-1].type == "examine_failed"
    assert events[-1].knowledge[0].knows == "vague_details_purse_01"
    assert events[-1].knowledge[0].fidelity == "vague"


def test_take_success_and_noticed_failure(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 13, TAVERN_STEPS + [
        {"intent": "take", "target": "oil_lamp_01"},
    ], name="take13.jsonl")
    take = events[-1]
    assert take.type == "take"
    assert sim.projection["oil_lamp_01"]["carrier"] == "pc_01"
    assert take.knowledge == ()  # unnoticed
    # the observers catch the reach on a failed stealth roll
    events, sim = run(tmp_path, 3, TAVERN_STEPS + [
        {"intent": "take", "target": "oil_lamp_01"},
    ], name="take3.jsonl")
    failed = events[-1]
    assert failed.type == "take_failed"
    assert sim.projection["oil_lamp_01"]["carrier"] is None
    saw = {r.who for r in failed.knowledge if r.knows == "pc_01_reaching_for_oil_lamp_01"}
    assert saw == {"npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01"}


def test_use_applies_item_effect(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 13, TAVERN_STEPS + [
        {"intent": "take", "target": "ale_mug_01"},
        {"intent": "use", "target": "ale_mug_01"},
    ], name="use.jsonl")
    use = events[-1]
    assert use.type == "use"
    assert use.state_changes[0].entity == "pc_01"
    assert use.state_changes[0].prop == "status.intoxication"
    assert use.state_changes[0].from_ == 0 and use.state_changes[0].to_ == 20
    assert sim.projection["pc_01"]["status.intoxication"] == 20
    saw = {r.who for r in use.knowledge if r.knows == "pc_01_used_ale_mug_01"}
    assert saw == {"npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01"}


def test_use_failed_branch(tmp_path: Path) -> None:
    pack = hard_pack(tmp_path, {"use": 90})
    events, sim = run(tmp_path, 13, TAVERN_STEPS + [
        {"intent": "take", "target": "ale_mug_01"},
        {"intent": "use", "target": "ale_mug_01"},
    ], pack=pack, name="usefailed.jsonl")
    assert events[-1].type == "use_failed"
    assert events[-1].state_changes == ()
    assert sim.projection["pc_01"]["status.intoxication"] == 0  # no effect


def test_drop_break_noise_and_ignition(tmp_path: Path) -> None:
    # dropping a non-fire-source item: noise, no ignition
    events, sim = run(tmp_path, 13, TAVERN_STEPS + [
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "drop_break", "target": "purse_01"},
    ], name="drop_purse.jsonl")
    drop = events[-1]
    assert drop.type == "drop_break"
    assert drop.outcome["broken"] is False  # the purse is not breakable
    assert sim.projection["purse_01"]["carrier"] is None
    heard = {r.who for r in drop.knowledge}
    assert "npc_guard_01" in heard  # same-location noise
    assert not any(e.type == "fire_started" for e in events)


def test_drop_break_unknown_spot_is_loud(tmp_path: Path) -> None:
    sim = make_sim(tmp_path, 13, "spot.jsonl")
    import pytest

    from core.loop import RunnerError

    with pytest.raises(RunnerError, match="must be a .* spot"):
        sim.run_playscript(script(TAVERN_STEPS + [
            {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
            {"intent": "drop_break", "target": "purse_01", "near": "roof"},
        ], 13))


def test_distract_turns_attention(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "distract", "target": "npc_drunk_01"},
    ])
    distract = events[-1]
    assert distract.type == "distract"
    assert sim.projection["npc_drunk_01"]["status.attention"] == "distracted"
    assert [(r.who, r.knows) for r in distract.knowledge] == [
        ("npc_drunk_01", "antics_by_pc_01")
    ]
    pack = hard_pack(tmp_path, {"distract": 90})
    events, sim = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "distract", "target": "npc_drunk_01"},
    ], pack=pack, name="ignored.jsonl")
    assert events[-1].type == "distract_ignored"
    assert "status.attention" not in sim.projection["npc_drunk_01"]


def test_flee_caught_and_escape(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "flee", "target": "loc_street"},
    ], name="caught.jsonl")
    caught = events[-1]
    assert caught.type == "flee_caught"
    assert sim.projection["pc_01"]["position"] == "loc_tavern"  # caught in place
    assert (caught.knowledge[0].who, caught.knowledge[0].fidelity) == (
        "npc_guard_01", "exact"
    )
    events, sim = run(tmp_path, 3, TAVERN_STEPS + [
        {"intent": "flee", "target": "loc_street"},
    ], name="escape.jsonl")
    flee = events[-1]
    assert flee.type == "flee"
    assert sim.projection["pc_01"]["position"] == "loc_street"
    assert flee.knowledge[0].knows == "pc_01_fled_toward_loc_street"


def test_flee_unopposed_when_alone(tmp_path: Path) -> None:
    # the street starts empty: no pursuit check at all, the exit is free
    events, sim = run(tmp_path, 42, [{"intent": "flee", "target": "loc_market"}],
                      name="free.jsonl")
    assert events[-1].type == "flee"
    assert events[-1].outcome["check"] == {}  # no check ran
    assert sim.projection["pc_01"]["position"] == "loc_market"


# -- impossible stays impossible (T5 partial) ---------------------------------------


def test_rejections_are_noops_and_the_script_continues(tmp_path: Path) -> None:
    events, sim = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "steal", "target": "npc_barkeep_01"},  # carries nothing stealable
        {"intent": "take", "target": "purse_01"},        # carried by the guard
        {"intent": "use", "target": "ale_mug_01"},        # lies uncarried
    ], name="reject.jsonl")
    rejections = [e for e in events if e.type == "intent_rejected"]
    assert [r.outcome["failed_test"] for r in rejections] == [
        "target.carries_flagged", "target.uncarried", "target.carried_by",
    ]
    assert all(r.outcome["reason"] == "precondition" for r in rejections)
    assert all(r.state_changes == () and r.knowledge == () and r.hooks == ()
               for r in rejections)
    assert all(r.importance == "low" for r in rejections)
    assert all(r.provenance["cause_intent"].startswith("intent_") for r in rejections)
    # nothing changed in the world; the script ran to the end
    assert sim.projection["pc_01"]["position"] == "loc_tavern"
    assert sim.projection["purse_01"]["carrier"] == "npc_guard_01"
    assert not any(e.type.startswith("fire") for e in events)


def test_arson_rejected_without_a_fire_source(tmp_path: Path) -> None:
    # the pc in the street holds nothing that burns and the street has no spots
    events, sim = run(tmp_path, 42, [{"intent": "arson", "target": "loc_street"}],
                      name="no_source.jsonl")
    assert [e.type for e in events] == ["intent_rejected"]
    assert events[0].outcome["failed_test"] == "target.field_in"
    assert not sim.projection["loc_street"]


def test_take_of_a_carried_item_is_rejected_not_steal(tmp_path: Path) -> None:
    # taking what someone carries is steal's job — the front door says no
    events, sim = run(tmp_path, 42, TAVERN_STEPS + [
        {"intent": "take", "target": "purse_01"},
    ], name="carried.jsonl")
    assert events[-1].type == "intent_rejected"
    assert events[-1].outcome["failed_test"] == "target.uncarried"
    assert sim.projection["purse_01"]["carrier"] == "npc_guard_01"


# -- the walkthrough fixture + determinism -------------------------------------------


def test_day1_theft_and_arson_fixture(tmp_path: Path) -> None:
    playscript = load_playscript(
        REPO / "tests" / "playscripts" / "day1_theft_and_arson.json"
    )
    sim = make_sim(tmp_path, playscript["seed"], "day1.jsonl")
    sim.run_playscript(playscript)
    _, events = read_log(tmp_path / "day1.jsonl", SCHEMA)
    types = [e.type for e in events]
    assert types == [
        "move", "steal", "take", "move", "drop_break", "fire_started",
        "fire_spread", "smoke_rising", "location_burned_out", "wait",
    ]
    # cause-chain integrity: every event chains to a written predecessor
    ids = {e.id for e in events}
    assert events[0].cause is None
    assert all(e.cause in ids for e in events[1:])
    # the fire chain: ignition chained to the drop, burnout irreversible
    started = next(e for e in events if e.type == "fire_started")
    drop = next(e for e in events if e.type == "drop_break")
    assert started.cause == drop.id
    burnout = next(e for e in events if e.type == "location_burned_out")
    assert burnout.t == started.t + 120
    assert sim.projection["loc_backyard"]["destroyed"] is True
    # the stolen purse travelled with the player
    assert sim.projection["purse_01"]["carrier"] == "pc_01"
    assert sim.projection["purse_01"]["position"] == "loc_backyard"
    # T2: fold(log) == runtime projection (STATE-1) with the fire chain in
    rebuilt = fold(events, initial_projection(PACK.entities))
    assert rebuilt == sim.projection


def test_day1_is_byte_identical_on_rerun(tmp_path: Path) -> None:
    playscript = load_playscript(
        REPO / "tests" / "playscripts" / "day1_theft_and_arson.json"
    )
    first = make_sim(tmp_path, playscript["seed"], "a.jsonl")
    result_a = first.run_playscript(playscript)
    second = make_sim(tmp_path, playscript["seed"], "b.jsonl")
    result_b = second.run_playscript(playscript)
    assert (tmp_path / "a.jsonl").read_bytes() == (tmp_path / "b.jsonl").read_bytes()
    assert result_a.fingerprint == result_b.fingerprint


def test_all_emitted_types_stay_in_pack_vocabulary(tmp_path: Path) -> None:
    playscript = load_playscript(
        REPO / "tests" / "playscripts" / "day1_theft_and_arson.json"
    )
    sim = make_sim(tmp_path, playscript["seed"], "vocab.jsonl")
    sim.run_playscript(playscript)
    _, events = read_log(tmp_path / "vocab.jsonl", SCHEMA)
    assert all(event.type in PACK.event_types() for event in events)


# -- iter-2a audit regressions (KI#13/KI#15/KI#16) -----------------------------


def test_double_drop_break_of_a_broken_item_is_idempotent(tmp_path: Path) -> None:
    # seed 34: both stealth takes succeed. The retake-and-redrop of the
    # broken mug must not desync the projection (KI#13): the second drop
    # releases the carrier and keeps the noise, but carries no second
    # condition change.
    events, sim = run(tmp_path, 34, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "take", "target": "ale_mug_01"},
        {"intent": "drop_break", "target": "ale_mug_01"},
        {"intent": "take", "target": "ale_mug_01"},
        {"intent": "drop_break", "target": "ale_mug_01"},
    ], name="twice.jsonl")
    drops = [e for e in events if e.type == "drop_break"]
    assert len(drops) == 2
    assert drops[0].state_changes[1].prop == "condition"
    assert all(c.prop != "condition" for c in drops[1].state_changes)
    assert drops[1].outcome["broken"] is True  # still breakable — still noisy
    assert sim.projection["ale_mug_01"]["condition"] == "broken"
    assert sim.projection["ale_mug_01"]["carrier"] is None


def test_two_staggered_fires_share_one_pass_and_keep_the_cause_chain(
    tmp_path: Path,
) -> None:
    # seed 19 (the KI#16 reproducer): the tavern fire's spread pass is live
    # when the backyard lamp drops. One pass must roll both locations with a
    # cause for every spread — no parallel pass, no cause=None crash.
    events, sim = run(tmp_path, 19, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "arson", "target": "loc_tavern"},
        {"intent": "take", "target": "oil_lamp_01"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "drop_break", "target": "oil_lamp_01", "near": "woodpile"},
        {"intent": "wait", "ticks": 60},
    ], name="twofires.jsonl")
    ids = {e.id for e in events}
    spreads = [e for e in events if e.type == "fire_spread"]
    assert spreads  # the run reaches the spread phase without dying
    assert all(e.cause in ids for e in spreads)  # every spread chains
    # one fire_started per location, one burnout line per location
    started = [e for e in events if e.type == "fire_started"]
    assert {e.target for e in started} == {"loc_tavern", "loc_backyard"}
    burnouts = [e for e in events if e.type == "location_burned_out"]
    assert {e.target for e in burnouts} == {"loc_tavern", "loc_backyard"}
    smokes = [e for e in events if e.type == "smoke_rising"]
    assert {e.target for e in smokes} == {"loc_tavern", "loc_backyard"}
    assert sim.projection["loc_tavern"]["destroyed"] is True
    assert sim.projection["loc_backyard"]["destroyed"] is True
    # T2 still holds with two interleaved fires
    rebuilt = fold(events, initial_projection(PACK.entities))
    assert rebuilt == sim.projection


def test_resolver_desync_fails_before_the_log_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A resolver bug (a from_ value the projection contradicts) must fail
    # at the _commit gate, BEFORE the write — the append-only log never
    # receives a desynced event (KI#13, D-035).
    from core import resolvers

    def buggy(
        pack: Pack, projection: Any, bank: Any, intent: Any, action: Any,
        check: Any, tick: int,
    ) -> Any:
        return resolvers.Resolution(
            event_type=action["events"]["success"],
            outcome={},
            state_changes=(
                resolvers.StateChange(
                    entity="pc_01", prop="position",
                    from_="loc_moon", to_="loc_mars",
                ),
            ),
        )

    monkeypatch.setitem(resolvers.REGISTRY, "wait", buggy)
    sim = make_sim(tmp_path, 42, "desync.jsonl")
    with pytest.raises(ValueError, match="projection holds"):
        sim.run_playscript(script([{"intent": "wait", "ticks": 1}], 42))
    lines = (tmp_path / "desync.jsonl").read_text().splitlines()
    assert len(lines) == 1  # header only — the bad draft never landed


def test_steal_without_carries_flagged_precondition_is_loud(
    tmp_path: Path,
) -> None:
    # A pack that drops the precondition the resolver keys on fails with a
    # named contract error, never a bare StopIteration (KI#15).
    target = tmp_path / "noflag_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    actions = json.loads((target / "actions.json").read_text())
    steal = next(a for a in actions["actions"] if a["intent"] == "steal")
    steal["requires"] = [c for c in steal["requires"]
                         if c["test"] != "carries_flagged"]
    (target / "actions.json").write_text(json.dumps(actions))
    pack = load_pack(target)
    sim = make_sim(tmp_path, 1, "noflag.jsonl", pack=pack)
    with pytest.raises(RuntimeError, match="carries_flagged precondition"):
        sim.run_playscript(script([
            {"intent": "move", "target": "loc_tavern"},
            {"intent": "steal", "target": "npc_guard_01"},
        ], 1), )


# -- the texture promotion path (iter-11: blueprint §1 — the door half) ------------


_CANDLES_REF = {
    "entry": "tex_0000", "scope": "scene:loc_tavern",
    "slot": "candles", "value": "lit",
}


def test_texture_take_success_is_the_canon_birth(tmp_path: Path) -> None:
    """A take on a resolved texture reference: the committed event IS the
    promotion — the scope target gains the slot as a canon prop, the
    outcome carries the reference, knowledge rides the texture templates.
    Probed seed: the opposed stealth check passes for pc_01."""
    events, sim = run(tmp_path, 4, TAVERN_STEPS + [
        {"intent": "take", "texture": dict(_CANDLES_REF)},
    ])
    take = events[-1]
    assert take.type == "take"
    assert take.outcome["texture"]["entry"] == "tex_0000"
    assert take.state_changes == (
        StateChange("loc_tavern", "candles", None, "lit"),
    )
    assert sim.projection["loc_tavern"]["candles"] == "lit"  # canon birth
    assert any(r.knows == "pc_01_holds_the_candles" for r in take.knowledge)
    assert take.provenance["cause_intent"].startswith("intent_")


def test_texture_take_failure_promotes_nothing(tmp_path: Path) -> None:
    """The stealth check fails (a hard pack): the failure event commits
    with the reference in the outcome but NO canon birth — a failed attempt
    does not kill the texture (blueprint §1)."""
    pack = hard_pack(tmp_path, {"take": 90})
    events, sim = run(tmp_path, 7, TAVERN_STEPS + [
        {"intent": "take", "texture": dict(_CANDLES_REF)},
    ], pack=pack, name="hard.jsonl")
    take = events[-1]
    assert take.type == "take_failed"
    assert take.outcome["texture"]["entry"] == "tex_0000"
    assert take.state_changes == ()
    assert "candles" not in sim.projection["loc_tavern"]  # no canon birth
    assert any(r.knows == "pc_01_fumbled_the_candles" for r in take.knowledge)


def test_texture_take_elsewhere_is_a_soft_rejection(tmp_path: Path) -> None:
    """Scene-scoped texture at another location: well-formed but
    world-impossible — an intent_rejected no-op fact, never a crash."""
    events, sim = run(tmp_path, 5, TAVERN_STEPS + [
        {"intent": "take", "texture": dict(_CANDLES_REF, scope="scene:loc_backyard")},
    ])
    rejected = events[-1]
    assert rejected.type == "intent_rejected"
    assert rejected.outcome["failed_test"] == "texture.same_location"
    assert "candles" not in sim.projection["loc_tavern"]


# -- rest (tune-1, iter-27: the fatigue counter-play, KI#4) ---------------------


def test_rest_reduces_fatigue_gained_by_long_waits(tmp_path: Path) -> None:
    """KI#4's balance observation was monotonic player fatigue: long waits
    climb the axis with no counter-play in v0.1. The rest action (pack data
    over the recuperate resolver) is the answer — the delta reads CURRENT
    projection values and clamps to the scale (KI#13: from_ never lies)."""
    events, sim = run(tmp_path, 5, TAVERN_STEPS + [
        {"intent": "wait", "ticks": 730},  # ~20 fatigue across two beats
        {"intent": "rest"},
    ])
    assert sim.projection["pc_01"]["status.fatigue"] == 0  # 20 - 30 -> clamp
    rest = next(e for e in events if e.type == "rest")
    assert [(c.prop, c.from_, c.to_) for c in rest.state_changes] == [
        ("status.fatigue", 20, 0)
    ]
    # routine recovery is not a tale beat (tune-1: the gate reads the rule)
    assert rest.importance == "low"
    # the fold agrees with the runtime projection (T2 shape, INV-1)
    state = fold(events, initial_projection(PACK.entities))
    assert state["pc_01"]["status.fatigue"] == 0


def test_rest_at_zero_fatigue_is_a_legal_quiet_beat(tmp_path: Path) -> None:
    """Resting fresh: no state change, no desynced write — the event still
    commits (time passed, the world moved) exactly like the decay pass's
    zero-delta skip."""
    events, sim = run(tmp_path, 6, [{"intent": "rest"}])
    rest = events[-1]
    assert rest.type == "rest"
    assert rest.state_changes == ()
    assert sim.projection["pc_01"]["status.fatigue"] == 0


# -- pack-2 (iter-29, D-061): the arson-on-ashes door check ---------------------


def test_arson_on_a_destroyed_location_is_rejected(tmp_path: Path) -> None:
    """pack-2, the iter-2a audit note + iter-24's live probe: arson on a
    fully-burning or destroyed location used to log a no-ignition success
    (spot=None, world unchanged) — a success that pretended. The
    spot_available door check rejects the attempt as a no-op fact with
    failed_test target.spot_available (the fourth door-outcome axis:
    no unburning spot, beside not co-located / no flagged target /
    no fuel)."""
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "take", "target": "oil_lamp_01"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "drop_break", "target": "oil_lamp_01", "near": "back_wall"},
        {"intent": "wait", "ticks": 300},  # the cascade burns out the yard
        {"intent": "arson", "target": "loc_backyard"},
    ]
    events, sim = run(tmp_path, 4, steps)  # seed 4: the take succeeds
    assert sim.projection["loc_backyard"]["destroyed"] is True
    rejected = events[-1]
    assert rejected.type == "intent_rejected"
    assert rejected.outcome["failed_test"] == "target.spot_available"
    # the world did not change: no new fire events after the burnout
    fire_types = {"fire_started", "fire_spread", "smoke_rising",
                  "location_burned_out"}
    assert not any(e.type in fire_types for e in events[events.index(rejected):])


def test_arson_on_a_fresh_location_still_ignites(tmp_path: Path) -> None:
    """The happy path is unchanged: a fresh flammable location with an
    unburning spot passes the new door check and the chain follows (T5's
    impossible-half and the possible-half stay honest)."""
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "take", "target": "oil_lamp_01"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "arson", "target": "loc_backyard"},
    ]
    events, sim = run(tmp_path, 4, steps)
    assert any(e.type == "arson" for e in events)
    assert any(e.type == "fire_started" for e in events)
    rejected = [e for e in events if e.type == "intent_rejected"]
    assert not rejected
