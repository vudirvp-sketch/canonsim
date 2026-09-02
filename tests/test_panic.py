"""iter-48 acceptance — the alarm panic echo (content-2, D-077): the
§11 recorded-not-landed row lands as live pack content over the standing
drama-3 dispatch. ZERO engine edits — the whole through-the-walls law is
one on_action entry keyed on `alarm_raised` (the panic contagion:
everyone who HEARD the shout grows more afraid), a story-critical event
type with its own chronicle line, and the 7-case corpus re-distill the
landing always implied (the content-1 precedent).

The design's load-bearing choices (DIRECTOR_SPEC §3c): the echo's +10
is the CONTAGION half, deliberately a quarter of the hardcoded +40
direct spike — the occupants compound (40 → 50: the fire seen AND the
panic heard), the distant hearers would start at 10; the scope is
UN-gated (a shout of fire unsettles everyone who heard it — the
alarm's own knowledge resolution already decides who that is, the
adjacent half dormant per the tune-3 static-placement finding); the
cause actor is a witness of his own alarm (hears his own shout, fear
0 → 10 — the honest edge the corpus pins); the reaction carries no
knowledge and no hooks, so the cascade terminates (the one-hop law);
the echo commits at the alarm's own tick, so the fear decay baseline
stays where the alarm set it.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")

# the corpus alarm family's shape (seed 33): enter the busy taproom,
# set the fire with the room occupied — the alarm's witnesses are the
# four occupants plus the arsonist himself (his own shout reaches him)
FIRE_STEPS: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "arson", "target": "loc_tavern"},
    {"intent": "wait", "ticks": 360},
]

OCCUPANTS = ("npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01")
WITNESSES = {"pc_01", *OCCUPANTS}


def run(tmp_path: Path, seed: int,
        steps: list[dict[str, Any]],
        pack: Any = PACK) -> tuple[list[Any], Simulator]:
    name = f"run_{seed}.jsonl"
    sim = Simulator(pack, seed, tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": "panic", "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    _, events = read_log(tmp_path / name, SCHEMA)
    return events, sim


def by_type(events: list[Any], event_type: str) -> list[Any]:
    return [e for e in events if e.type == event_type]


def _stripped_pack(tmp_path: Path) -> Any:
    """The committed pack minus ONLY the alarm entry (the INV-3 gate:
    the pack's own declaration is the gate — the block stays, the
    document_check entries stay)."""
    target = tmp_path / "stripped_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules_path = target / "rules.json"
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    rules["on_action"].pop("alarm_raised")
    rules_path.write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return load_pack(target)


# -- the live dispatch (the committed runs) ------------------------------------


def test_the_echo_fires_with_the_alarm_and_compounds_the_room(tmp_path: Path) -> None:
    """Seed 33, the corpus alarm family: ONE panic event per alarm, at
    the alarm's own tick, cause-chained to it — the alarm shape through
    the real door. The reacting set is the alarm's witnesses WITH a
    numeric fear home: the four occupants (the direct +40 spike already
    landed — the echo compounds 40 → 50, the contagion on top of the
    fire seen) and the cause actor himself (0 → 10 — he hears his own
    shout). The deltas are exactly +10, clamped by the one numeric
    scale."""
    events, sim = run(tmp_path, 33, FIRE_STEPS)
    (alarm,) = by_type(events, "alarm_raised")
    (panic,) = by_type(events, "panic_ripple")
    assert panic.t == alarm.t
    assert panic.cause == alarm.id  # chained through the real commit door
    assert panic.actor == "world" and panic.target == "loc_tavern"
    assert panic.importance == "medium"  # story-critical: the tale gate
    assert {c.entity for c in panic.state_changes} == WITNESSES
    for change in panic.state_changes:
        assert change.prop == "status.fear"
        assert change.to_ == change.from_ + 10  # the contagion delta
    # the occupants compound: spike (0→40) then echo (40→50)
    assert all(
        c.from_ == 40 and c.to_ == 50
        for c in panic.state_changes if c.entity in OCCUPANTS
    )
    # the cause actor: his own shout reaches him (0→10)
    pc = next(c for c in panic.state_changes if c.entity == "pc_01")
    assert pc.from_ == 0 and pc.to_ == 10
    # the alarm's own spike is untouched (the hardcoded layer, ev_0003)
    assert all(c.to_ == 40 for c in alarm.state_changes)
    for who in WITNESSES:
        assert who in panic.outcome["reacting"]


def test_the_reaction_terminates_the_cascade(tmp_path: Path) -> None:
    """The one-hop law through the real door: the panic event carries NO
    knowledge and NO hooks — no system reaction and no on_action entry
    can key on it (the pack's table has no panic_ripple key), so the
    events after it are the fire's own cascade, never a second-order
    reaction."""
    events, _sim = run(tmp_path, 33, FIRE_STEPS)
    (panic,) = by_type(events, "panic_ripple")
    assert panic.knowledge == ()
    assert panic.hooks == ()
    after = events[events.index(panic) + 1:]
    assert all(e.type != "panic_ripple" for e in after)
    assert all(e.type != "crowd_wary" for e in after)
    # the entry is the only alarm-keyed reaction: one echo per alarm
    assert len(by_type(events, "panic_ripple")) == len(
        by_type(events, "alarm_raised")
    )


def test_the_echo_never_resets_the_fear_decay_baseline(tmp_path: Path) -> None:
    """The echo commits at the alarm's own tick, so the decay baseline
    for the fear axis stays where the alarm set it: the beat-360 decay
    pass runs FROM the alarm (354 ticks → −4), the occupants fall
    50 → 46 and the cause actor 10 → 6 — never a re-based double
    decay."""
    events, sim = run(tmp_path, 33, FIRE_STEPS)
    decays = [
        c for e in by_type(events, "status_decayed")
        for c in e.state_changes if c.prop == "status.fear"
    ]
    by_entity = {c.entity: (c.from_, c.to_) for c in decays}
    assert by_entity["npc_guard_01"] == (50, 46)
    assert by_entity["pc_01"] == (10, 6)
    assert sim.projection["npc_guard_01"]["status.fear"] == 46


def test_the_chronicle_line_renders_after_the_shout(tmp_path: Path) -> None:
    """The panic is a tale beat: its own line lands directly after the
    alarm's shout (the day's arc: the shout, the panic through the
    walls, the spreading fire) — the story-critical hook earns the
    line, the static template never draws cosmetic RNG."""
    events, _sim = run(tmp_path, 33, FIRE_STEPS)
    lines = render_chronicle(events, PACK, seed=33).splitlines()
    assert "Someone shouts: fire!" in lines
    panic_line = "Panic ripples through the walls of Three Barrels tavern."
    assert panic_line in lines
    assert lines.index(panic_line) == lines.index("Someone shouts: fire!") + 1


def test_an_empty_room_ignition_never_dispatches(tmp_path: Path) -> None:
    """The alarm precedent carries: an ignition with no occupants raises
    no alarm — no event for the entry to key on, no echo, no log delta.
    The canonical day1_full run (seed 125, the T8 gate script) burns
    the EMPTY backyard: the whole run stays echo-free."""
    from core.loop import load_playscript

    script = load_playscript(REPO / "tests" / "playscripts" / "day1_full.json")
    events, _sim = run(tmp_path, script["seed"], script["steps"])
    assert by_type(events, "alarm_raised") == []
    assert by_type(events, "panic_ripple") == []


def test_the_stripped_entry_runs_byte_identical_on_alarm_free_runs(
    tmp_path: Path,
) -> None:
    """The INV-3 gate: dropping ONLY the alarm entry changes nothing on
    a run that raises no alarm — the logs are byte-identical (the
    pack's own declaration is the gate). The single-steal
    theft-and-arson script keeps the law's stage: its fire never shares
    the room with a witness, so no alarm fires."""
    from core.loop import load_playscript

    stripped = _stripped_pack(tmp_path)
    script = load_playscript(
        REPO / "tests" / "playscripts" / "day1_theft_and_arson.json"
    )
    events_committed, _sim = run(tmp_path, script["seed"], script["steps"])
    assert by_type(events_committed, "alarm_raised") == []  # the stage holds
    log_committed = tmp_path / f"run_{script['seed']}.jsonl"
    log_stripped = tmp_path / "stripped.jsonl"
    sim = Simulator(stripped, script["seed"], log_stripped, SCHEMA,
                    commit="0000000")
    sim.run_playscript(
        {"name": "stripped", "seed": script["seed"], "pack": "tavern_pack@0.1",
         "steps": script["steps"]}
    )
    assert log_committed.read_bytes() == log_stripped.read_bytes()


# -- the pack declarations + the corpus evidence --------------------------------


def test_the_pack_declarations_are_live(tmp_path: Path) -> None:
    """The landed content set: the on_action table carries the alarm
    entry (witnesses scope, the panic event, the fear contagion delta),
    the event type is story-critical (the chronicle line's gate), and
    the template line exists — every declaration the dispatch reads."""
    entry = PACK.rules["on_action"]["alarm_raised"][0]
    assert entry["scope"] == "witnesses"
    assert entry["event"] == "panic_ripple"
    assert entry["state"] == {"prop": "status.fear", "add": 10}
    assert "panic_ripple" in PACK.rules["importance"]["story_critical_events"]
    assert PACK.templates["events"]["panic_ripple"] == (
        "Panic ripples through the walls of {location}."
    )
    # the panic event type is NOT in system_of_type (the crowd_wary
    # precedent: the state changes already classify it to one system —
    # M1 stays untouched by the reaction layer)
    assert "panic_ripple" not in PACK.rules["metrics"]["system_of_type"]


def test_the_corpus_pins_the_echo_and_the_cause_actor(tmp_path: Path) -> None:
    """The 7-case re-distill (the iter-43/44 precedent, D-077): the
    corpus's alarm case carries the echo's own claims — the panic event
    claimable by id and the cause actor's fear at 10 — and the
    occupants' fear claims read 50 (the compounding). The corpus test
    replays these through the real cycle; this pin guards the fixture
    against a silent rollback of the content landing."""
    corpus = json.loads(
        (REPO / "tests" / "fixtures" / "narrator_beats.json").read_text(
            encoding="utf-8"
        )
    )
    case = next(
        c for c in corpus["cases"]
        if c["name"] == "alarm_fires_when_occupants_are_present"
    )
    claims = case["beats"][1]["reply"]["proposal"]["claims"]
    panic_claims = [c for c in claims if c.get("type") == "panic_ripple"]
    assert len(panic_claims) == 1
    assert panic_claims[0]["event_id"] == "ev_0004"
    pc_fear = [
        c for c in claims
        if c.get("entity") == "pc_01" and c.get("prop") == "status.fear"
    ]
    assert pc_fear[0]["value"] == 10  # the cause actor heard his own shout
    occupant_fear = [
        c for c in claims
        if c.get("prop") == "status.fear" and c.get("entity") in OCCUPANTS
    ]
    assert all(c["value"] == 50 for c in occupant_fear)
    assert case["expect"]["notes_contains"] == ["BEAT claims: 14 supported"]
