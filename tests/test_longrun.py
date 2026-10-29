"""iter-99-rev5 — the long-run laws on the COMMITTED pack (the pre-gate
revision's test actualization).

The suite's longest committed-pack runs stop at ~1500 ticks (one day):
the year-scale arming committed at weather-1 (the macro clock at
518400 + the weather chain) has never been live-fired on the committed
scenario at its OWN cadence — the crafted-pack twins squeeze the
cadence, but the committed combination (genesis + macro + weather +
the LOD's one-gate engagement) is what the phase-5 exit review hands
to phase 6. Three pins, each self-comparing (no committed fixture —
zero corpus price by construction):

- the year-scale run: one crossing fires the year turn (the derived
  calendar law) + the weather chain (the structural laws: chained to
  the turn, the closed state vocabulary) + the T2 replay + the T1
  byte-identity double-run on the LONG log;
- the wandering tail: day1_full + a day-2 tail keeps a living floor
  (autonomous events past the scripted storyline) — the steady state
  the exit review characterizes;
- the idle world: beats, rotations and decay fire with the player
  standing still (the world is not player-driven).

Seeds are fixed (42/125/7 — the probe battery's); the assertions pin
laws, not rolls: a pack re-tune re-rolls the weather draw without
breaking anything here (only a real regression or a determinism break
fails the suite).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.log import read_log
from core.loop import Simulator
from core.macro import macro_year
from core.pack import load_pack
from render.chronicle import replay_report

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")
PLAYER = PACK.player_id()

#: day1_full.json steps verbatim (seed 125) — the scripted storyline.
DAY1: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "take", "target": "oil_lamp_01"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "wait", "ticks": 720},
    {"intent": "move", "target": "loc_backyard"},
    {"intent": "drop_break", "target": "oil_lamp_01", "near": "back_wall"},
    {"intent": "wait", "ticks": 720},
]

#: a day-2 wandering tail: rest, return, socials, idle beats.
TAIL: list[dict[str, Any]] = [
    {"intent": "rest"},
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "look_around"},
    {"intent": "talk", "target": "npc_barkeep_01"},
    {"intent": "wait", "ticks": 720},
    {"intent": "look_around"},
    {"intent": "move", "target": "loc_street"},
    {"intent": "look_around"},
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "wait", "ticks": 720},
]


def _run(path: Path, seed: int, steps: list[dict[str, Any]]) -> bytes:
    """One fresh committed-pack run; returns the log bytes (T1 self-compare)."""
    sim = Simulator(PACK, seed, path, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(steps)
    sim.close()
    return path.read_bytes()


def _events(path: Path) -> list[Any]:
    _, events = read_log(path, SCHEMA)
    return events


def test_year_scale_run_crosses_the_macro_clock(tmp_path: Path) -> None:
    """One committed-cadence crossing (seed 42): the wait jumps the clock
    a full year and the crossing fires MID-WAIT (D-038) — the year turn
    carries the derived calendar year and the cold census; the weather
    chain rolls at most once, chained to the turn, inside the closed
    state vocabulary; the long log replays and re-runs byte-identically."""
    cadence = int(PACK.rules["time"]["macro"]["cadence_ticks"])
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": cadence},
        {"intent": "look_around"},
    ]
    log = tmp_path / "year.jsonl"
    first = _run(log, 42, steps)
    events = _events(log)

    years = [e for e in events if e.type == "year_turns"]
    assert len(years) == 1  # exactly one crossing inside the window
    turn = years[0]
    assert turn.t == cadence  # the scheduler law: the positive multiple
    assert turn.outcome["year"] == macro_year(PACK.rules, turn.t)  # derived, L3
    assert isinstance(turn.outcome["cold_npcs"], int)  # the census shape

    weathers = [e for e in events if e.type == "weather_turns"]
    assert len(weathers) <= 1  # one roll per crossing, self-roll suppresses
    states = set(PACK.rules["weather"]["states"])
    for sky in weathers:
        assert sky.t == turn.t
        assert sky.cause == turn.id  # the consumer rides the clock's own event
        assert sky.outcome["weather"] in states  # the closed vocabulary

    report, _ = replay_report(log, PACK, SCHEMA)  # T2 on the long log
    assert "fold OK" in report

    twin = _run(tmp_path / "year_twin.jsonl", 42, steps)  # T1 self-compare
    assert twin == first


def test_wandering_tail_keeps_a_living_floor(tmp_path: Path) -> None:
    """day1_full + a day-2 tail (seed 125): the scripted storyline ends
    (the director's one-shot magazine spent) and the world still moves —
    day 2 owns autonomous events (rotations, decay, urgencies, the
    social mill). The steady state the phase-5 exit review
    characterizes; pinned as a floor, never as counts."""
    log = tmp_path / "tail.jsonl"
    first = _run(log, 125, DAY1 + TAIL)
    events = _events(log)

    day2 = [e for e in events if e.t >= 1440]
    assert day2, "the world went silent after the storyline"
    autonomous = [e for e in day2 if e.actor != PLAYER]
    assert autonomous  # the living floor: rotations, decay, urgencies
    assert any(e.type == "watch_change" for e in autonomous)  # clock-scheduled

    report, _ = replay_report(log, PACK, SCHEMA)
    assert "fold OK" in report

    twin = _run(tmp_path / "tail_twin.jsonl", 125, DAY1 + TAIL)
    assert twin == first


def test_the_idle_world_beats_without_the_player(tmp_path: Path) -> None:
    """A fresh run where the player only arrives and stands still (seed
    7): beats, rotations and decay still commit — the world is not
    player-driven (M5's law at the smallest scale, no harness needed)."""
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 1500},
    ]
    log = tmp_path / "idle.jsonl"
    _run(log, 7, steps)
    events = _events(log)

    autonomous = [e for e in events if e.actor != PLAYER]
    assert any(e.type == "watch_change" for e in autonomous)  # the rotation
    assert any(e.type == "status_decayed" for e in autonomous)  # the decay
