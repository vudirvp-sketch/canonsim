"""iter-43 acceptance — the document_check action (the crime ladder's
public rung, D-072): the deferred consequence becomes a real resolution.
The whole boss beat is PACK DATA over the standing machinery — the
inspect resolver (a checked interaction producing knowledge, no state
change of its own), the crime reactions on the verdict token
(papers_unsatisfactory → +25 → the arrest attempt + resolution), the
on_action crowd reaction on the check's own witnesses (crowd_wary, the
first live dispatch of the drama-3 entry), and the two watcher hooks
with option-gated confrontation (the deferred-release law: the release
waits for the world where the door will accept).

Seeds are probed to be deterministic (T1 discipline): seed 19 — the
band opens (double-steal failure → 55) AND the verdict lands (the
scrutiny wins) → the full ladder to the irreversible caught state;
seed 93 — the band opens, the stranger talks the check down → no
escalation, the crowd layer only; seed 2 — the band never opens (the
second steal succeeds) but the entropy sits at the climax layer → the
boss releases through the DIR-3 climax path (the L4D2 three-intensity
rule live); seed 125 (day1_full) — Doren's half waits all run (his
post emptied the beat his band opened) and the door never sees a
world-impossible attempt.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")

# the corpus session-10 shape: enter, fail two steals (Doren's band),
# wait through the rotation beat — the briefing opens the relief's band
DOUBLE_STEAL_WAIT: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "wait", "ticks": 400},
]


def run(tmp_path: Path, seed: int,
        steps: list[dict[str, Any]]) -> tuple[list[Any], Simulator]:
    name = f"run_{seed}.jsonl"
    sim = Simulator(PACK, seed, tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": "doccheck", "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    _, events = read_log(tmp_path / name, SCHEMA)
    return events, sim


def by_type(events: list[Any], event_type: str) -> list[Any]:
    return [e for e in events if e.type == event_type]


def all_checks(events: list[Any]) -> list[Any]:
    """Both branch types — the demand is one event family (the house
    pattern: take/take_failed, flee/flee_caught)."""
    return by_type(events, "document_check") + by_type(
        events, "document_check_failed"
    )


def suspicion_before(events: list[Any], event_id: str, npc: str) -> int:
    """The npc's suspicion as left by the events strictly before the
    given event (the pre-check world the release read)."""
    value = 0
    for e in events:
        if e.id == event_id:
            return value
        for change in e.state_changes:
            if change.entity == npc and change.prop == "relations.suspicion":
                value = int(change.to_)
    return value


# -- the full ladder: verdict → escalation → arrest → caught ------------------


def test_the_ladder_fires_the_full_boss_beat(tmp_path: Path) -> None:
    """Seed 19: the relief's check lands the damning verdict — the
    ladder runs end to end. The verdict token escalates the WATCHER who
    holds it (EPIST-1: +25 on the knower, never on the room), the
    crossing emits the arrest attempt cause-chained to the suspicion
    event, the resolution draws evasion vs pursuit and catches the
    suspect (the irreversible T4 flip), and the crowd reaction lands
    on the check's own witnesses (the room +5; the checked stranger is
    dropped — no suspicion home, the suspicion law)."""
    events, sim = run(tmp_path, 19, DOUBLE_STEAL_WAIT)
    (check,) = by_type(events, "document_check")
    # the release rides the intent door: the relief guard's intent
    assert str(check.provenance["cause_intent"]) == "director_0000"
    assert check.actor == "npc_guard_02" and check.target == "pc_01"
    # the damning verdict: the actor's scrutiny beat the target's composure
    assert check.outcome["check"]["passed"] is True
    assert check.outcome["check"]["defender_id"] == "pc_01"
    # the verdict is knowledge: the actor holds it exactly; the room
    # (and the target) hold the un-mapped sighting token
    tokens = {(k.who, k.knows, k.fidelity) for k in check.knowledge}
    assert ("npc_guard_02", "papers_unsatisfactory", "exact") in tokens
    assert ("npc_barkeep_01", "papers_demanded_of_pc_01", "partial") in tokens
    # the escalation rides the crime reaction, not the resolver
    guard_reaction = next(
        e for e in by_type(events, "suspicion_changed")
        if e.actor == "npc_guard_02" and e.cause == check.id
    )
    assert guard_reaction.outcome["token"] == "papers_unsatisfactory"
    assert guard_reaction.outcome["delta"] == 25
    # the arrest attempt is chained to the watcher's own suspicion event
    (attempt,) = by_type(events, "arrest_attempt")
    assert attempt.actor == "npc_guard_02" and attempt.target == "pc_01"
    assert attempt.cause == guard_reaction.id
    # the resolution: caught, irreversible (T4) — the boss beat's end
    (resolved,) = by_type(events, "arrest_resolved")
    assert resolved.outcome["caught"] is True
    assert sim.projection["pc_01"]["crime_status"] == "caught"
    # the crowd reaction: the check's own witnesses, the room only
    (crowd,) = by_type(events, "crowd_wary")
    assert crowd.cause == check.id
    assert {c.entity for c in crowd.state_changes} == {
        "npc_guard_02", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    }
    for change in crowd.state_changes:  # the clamped +5 lands
        assert change.to_ == change.from_ + 5
    # the crowd's wariness never re-triggers the arrest machinery (the
    # token-keyed crime system owns the ladder, not the crowd layer)
    assert len(by_type(events, "arrest_attempt")) == 1


def test_the_talked_down_verdict_escalates_nothing(tmp_path: Path) -> None:
    """Seed 93: the stranger's composure beats the scrutiny — the
    talked-down branch commits its own event type (the house pattern:
    the demand happened, the answer satisfied), no verdict token, no
    escalation, no arrest; the crowd layer still lands (a public
    challenge unsettles the room either way). The first_time_only
    burn means the check never re-rolls within the run."""
    events, sim = run(tmp_path, 93, DOUBLE_STEAL_WAIT)
    (check,) = all_checks(events)
    assert check.type == "document_check_failed"  # the talked-down branch
    assert check.outcome["check"]["passed"] is False
    # the actor holds no verdict record on the talked-down branch
    assert not any(
        k.who == "npc_guard_02" for k in check.knowledge
    )
    # nothing escalated: no token reaction chained to the check
    assert not [
        e for e in by_type(events, "suspicion_changed") if e.cause == check.id
    ]
    assert by_type(events, "arrest_attempt") == []
    assert sim.projection["pc_01"]["crime_status"] == "suspect"
    # the crowd layer still fired (the entry keys BOTH branch types)
    (crowd,) = by_type(events, "crowd_wary")
    assert crowd.cause == check.id
    # exactly one check per run (the Wesnoth burn law, per watcher)
    assert len(all_checks(events)) == 1


# -- the release's world gating (the deferred-release law) ---------------------


def test_the_relief_releases_at_the_rotation_doren_waits(tmp_path: Path) -> None:
    """The canonical day1_full run (seed 125, the T8 gate script): the
    seeded watcher's half NEVER releases — Doren rotates off the post
    the beat his band opens, and the option gate (his post + the
    stranger present) stays closed for the rest of the run; the
    relief's half fires right after the briefing. The deferred-release
    law: the door never sees a world-impossible director attempt
    (zero intent_rejected events with a director cause)."""
    from core.loop import load_playscript

    script = load_playscript(REPO / "tests" / "playscripts" / "day1_full.json")
    name = "day1_full.jsonl"
    sim = Simulator(PACK, script["seed"], tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _, events = read_log(tmp_path / name, SCHEMA)
    checks = all_checks(events)
    assert len(checks) == 1
    assert checks[0].actor == "npc_guard_02"  # the institution's half
    assert str(checks[0].provenance["cause_intent"]) == "director_0000"
    rejected = [
        e for e in by_type(events, "intent_rejected")
        if str(e.provenance.get("cause_intent", "")).startswith("director_")
    ]
    assert rejected == []  # the gate closed beats the door rejecting


def test_the_climax_path_releases_when_the_band_never_opens(
    tmp_path: Path,
) -> None:
    """Seed 2: the second steal SUCCEEDS — the band stays shut (the
    watchers sit at 45, below 50) — but the day's tension sits at the
    climax layer (suspicion + unreleased hooks ≥ 75 at the first
    beat), so the boss releases through the DIR-3 path: the L4D2
    three-intensity rule live. The release marks PEAK_CLIMAX (the one
    boss beat) and the verdict escalates the watcher below the arrest
    threshold (no arrest: the boss without the band is one rung
    short)."""
    events, sim = run(tmp_path, 2, DOUBLE_STEAL_WAIT)
    (check,) = all_checks(events)
    assert check.type == "document_check"  # the damning branch
    # the band never opened: the pre-check suspicion is below the
    # trigger value — only the climax path could have released
    assert suspicion_before(events, check.id, "npc_guard_02") < 50
    assert sim.director.pacing is not None
    assert sim.director.pacing.state == "PEAK_CLIMAX"
    # the verdict landed but stopped one rung short of the arrest
    (guard_reaction,) = [
        e for e in by_type(events, "suspicion_changed") if e.cause == check.id
    ]
    assert guard_reaction.outcome["to"] == 70  # 45 + the verdict's 25
    assert by_type(events, "arrest_attempt") == []


def test_the_pack_declares_the_watcher_pair() -> None:
    """The institutional consequence is TWO hooks — one per watch
    participant — each with the plain threshold trigger (its own
    watcher's band, the causal condition), the option-gated
    confrontation (the world the door will accept), the climax flag
    (the boss path consults the same gate — a closed boss does not
    mark PEAK_CLIMAX), the first_time_only burn (one check per
    watcher), and the real action payload (the stub wait is gone)."""
    hooks = PACK.rules["director"]["hooks"]
    for tag, watcher in (
        ("possible_document_check", "npc_guard_01"),
        ("possible_document_check_relief", "npc_guard_02"),
    ):
        spec = hooks[tag]
        assert spec["target_npc"] == watcher
        assert spec["intent"] == {"kind": "document_check", "target": "pc_01"}
        assert spec["trigger"]["kind"] == "threshold"
        assert spec["trigger"]["target_npc"] == watcher
        assert spec["climax"] is True
        assert spec["first_time_only"] is True
        (gate,) = spec["options"]
        assert {leaf["kind"] for leaf in gate["trigger"]} == {"place", "prop"}
    # the steal failure registers both halves (the institutional seed)
    steal = next(
        a for a in PACK.data["actions.json"]["actions"]
        if a["intent"] == "steal"
    )
    assert set(steal["hooks"]["failure"]) == {
        "guard_suspicious_of_pc", "possible_document_check",
        "possible_document_check_relief",
    }
    # the verdict token is the only crime-mapped check knowledge
    mapping = PACK.rules["crime_watch"]["suspicion_from_knowledge"]
    assert mapping["papers_unsatisfactory"] == "papers_unsatisfactory"
    assert PACK.rules["crime_watch"]["suspicion_sources"]["papers_unsatisfactory"] == 25


# -- the action's own door (generic actor — the front door is one door) --------


def test_the_door_rejects_a_check_across_locations(tmp_path: Path) -> None:
    """A world-impossible intent is a soft rejection (a no-op fact,
    never an exception): demanding papers from another room fails the
    co-location precondition — the action is actor-generic (the door
    validates the world, not who asks)."""
    events, _ = run(tmp_path, 42, [
        {"intent": "document_check", "target": "npc_guard_01"},
    ])
    (rejected,) = by_type(events, "intent_rejected")
    assert rejected.outcome["action"] == "document_check"
    assert rejected.outcome["failed_test"] == "target.same_location"
    assert all_checks(events) == []


def test_a_co_located_actor_checks_documents(tmp_path: Path) -> None:
    """The generic-actor pin: the door accepts any co-located actor —
    the stranger demanding papers of the watcher is mechanically legal
    (the world answers the check honestly; the roles are content)."""
    events, sim = run(tmp_path, 42, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "document_check", "target": "npc_guard_01"},
    ])
    (check,) = all_checks(events)
    assert check.actor == "pc_01" and check.target == "npc_guard_01"
    # the roles are content: the stranger's scrutiny rolled against the
    # watcher's composure, the knowledge landed on the same shapes
    assert check.knowledge  # the room witnessed whoever demanded
    assert by_type(events, "intent_rejected") == []
    # no crime-mapped token rode the room's sighting: nobody escalated,
    # the stranger is still unknown to the watch's paperwork
    assert sim.projection["pc_01"]["crime_status"] == "unknown"
    assert not [
        e for e in by_type(events, "suspicion_changed")
        if e.cause == check.id
    ]


# -- the chronicle line (T7: the tale reads without ornaments) -----------------


def test_the_boss_beat_reads_as_a_story(tmp_path: Path) -> None:
    """The day-19 chronicle renders the whole ladder in order: the
    demand, the verdict line (the conditional template), the crowd, the
    watcher's escalation, the arrest, the catch."""
    from render.chronicle import chronicle_from_log

    events, _ = run(tmp_path, 19, DOUBLE_STEAL_WAIT)
    log = tmp_path / "run_19.jsonl"
    text = chronicle_from_log(log, PACK, SCHEMA)
    for line in (
        "the relief guard demands papers from the player — the papers do not satisfy.",
        "The room watches the player closely.",
        "the relief guard moves to arrest the player.",
        "is caught — the pursuit holds.",
    ):
        assert line in text, f"missing chronicle line: {line!r}"


def test_the_talked_down_line_renders(tmp_path: Path) -> None:
    """The failure branch's verdict line — the same demand event, the
    other conditional arm."""
    from render.chronicle import chronicle_from_log

    events, _ = run(tmp_path, 93, DOUBLE_STEAL_WAIT)
    log = tmp_path / "run_93.jsonl"
    text = chronicle_from_log(log, PACK, SCHEMA)
    assert (
        "the relief guard demands papers from the player — the answer satisfies."
        in text
    )
    assert "the papers do not satisfy" not in text
