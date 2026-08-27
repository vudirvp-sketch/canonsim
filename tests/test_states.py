"""iter-4 acceptance — the states decay pass (MVP_SCOPE §5 system 5,
deferred from iter-3): fatigue/intoxication/fear decay per the pack's
`rules.states` rates at clock-crossing beats. Every state delta is an
event through the commit door (INV-1) — the pass returns drafts, the
loop commits them. Injury has `auto_decay: 0` (never decays; only a
counter-event can change it — T4 holds).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.fold import initial_projection
from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack
from core.states import DECAY_EVENT, decay_drafts

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")


def by_type(events: list[Any], event_type: str) -> list[Any]:
    return [e for e in events if e.type == event_type]


def test_decay_pass_emits_no_drafts_at_zero_elapsed() -> None:
    """A decay pass at the same tick as the last decay event produces
    no drafts — the elapsed time is zero, no axis moves."""
    projection = initial_projection(PACK.entities)
    drafts = decay_drafts(PACK, projection, events=[], beat_tick=0)
    assert drafts == ()


def test_decay_pass_emits_drafts_after_six_in_world_hours() -> None:
    """At tick 360 (6 in-world hours), fatigue +10 (gain_per_360_ticks_awake
    = 10); intoxication -10 (decay_per_360_ticks = 10); fear 0 (no fear
    to decay on the NPCs at t=0 — all start at 0); injury 0 (auto_decay
    is 0 — the sentinel that says 'never decay')."""
    projection = initial_projection(PACK.entities)
    drafts = decay_drafts(PACK, projection, events=[], beat_tick=360)
    # the drunkard has intoxication 50; the barkeep and Doren have fatigue 10;
    # the maid has fatigue 20. Each NPC with a non-zero delta gets a draft.
    assert drafts  # at least one
    # all drafts are status_decayed
    assert all(d.type == DECAY_EVENT for d in drafts)
    # check the drunkard's intoxication decayed by 10
    drunk = next(d for d in drafts if d.target == "npc_drunk_01")
    intox = next(c for c in drunk.state_changes if c.prop == "status.intoxication")
    assert intox.from_ == 50 and intox.to_ == 40


def test_decay_pass_uses_last_decay_event_as_baseline() -> None:
    """Proportional deltas: a 720-tick beat after a 360-tick decay event
    applies only 360 ticks of decay (not 720)."""
    projection = initial_projection(PACK.entities)
    # first decay at 360: drunkard intoxication 50 -> 40
    first = decay_drafts(PACK, projection, events=[], beat_tick=360)
    first_drunk = next(d for d in first if d.target == "npc_drunk_01")
    first_intox = next(c for c in first_drunk.state_changes if c.prop == "status.intoxication")
    assert first_intox.to_ == 40
    # apply the first decay to the projection
    for change in first_drunk.state_changes:
        projection[first_drunk.target][change.prop] = change.to_
    # build a synthetic EventRecord to feed as the "last decay"
    from core.log import EventRecord
    last_decay_event = EventRecord(
        id="ev_0001", t=360, type=DECAY_EVENT, actor="world",
        target="npc_drunk_01", cause=None, outcome={}, knowledge=(),
        state_changes=first_drunk.state_changes, hooks=(), importance="low",
        provenance={},
    )
    # second decay at 720 (another 360 ticks): 40 -> 30
    second = decay_drafts(PACK, projection, events=[last_decay_event], beat_tick=720)
    second_drunk = next(d for d in second if d.target == "npc_drunk_01")
    second_intox = next(c for c in second_drunk.state_changes if c.prop == "status.intoxication")
    assert second_intox.from_ == 40 and second_intox.to_ == 30


def test_injury_never_decays() -> None:
    """Injury has auto_decay=0 (the pack's signal it only changes via a
    counter-event). T4 holds — an injury is permanent."""
    projection = initial_projection(PACK.entities)
    projection["npc_guard_01"]["status.injury"] = 50  # injured
    drafts = decay_drafts(PACK, projection, events=[], beat_tick=360)
    guard = next((d for d in drafts if d.target == "npc_guard_01"), None)
    if guard is not None:
        # if the guard has a draft, it should NOT touch injury
        assert all(c.prop != "status.injury" for c in guard.state_changes)


def test_decay_pass_skips_caught_npcs() -> None:
    """The caught do not tire — a dead-or-captured NPC has no decay."""
    projection = initial_projection(PACK.entities)
    projection["npc_drunk_01"]["crime_status"] = "caught"
    drafts = decay_drafts(PACK, projection, events=[], beat_tick=360)
    # no draft for the drunkard (caught)
    assert all(d.target != "npc_drunk_01" for d in drafts)


def test_decay_clamps_to_relations_scale() -> None:
    """The drunkard's intoxication can't drop below 0 — the pack's
    relation scale [0, 100] is the floor/ceiling for status too."""
    projection = initial_projection(PACK.entities)
    projection["npc_drunk_01"]["status.intoxication"] = 5  # near floor
    drafts = decay_drafts(PACK, projection, events=[], beat_tick=360)
    drunk = next((d for d in drafts if d.target == "npc_drunk_01"), None)
    if drunk is not None:
        intox = next(c for c in drunk.state_changes if c.prop == "status.intoxication")
        assert intox.to_ == 0  # clamped, not negative


def test_decay_pass_fires_at_clock_boundary_in_run(tmp_path: Path) -> None:
    """End-to-end: a wait that crosses the first beat (tick 360) produces
    at least one status_decayed event in the log."""
    sim = Simulator(PACK, 42, tmp_path / "run.jsonl", SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": "test", "seed": 42, "pack": "tavern_pack@0.1",
        "steps": [{"intent": "wait", "ticks": 400}],
    })
    _, events = read_log(tmp_path / "run.jsonl", SCHEMA)
    decay = by_type(events, DECAY_EVENT)
    assert decay  # the beat at tick 360 fired the decay pass


def test_decay_pass_silent_in_short_plumbing_smoke_run(tmp_path: Path) -> None:
    """The golden-fixture scenario (58 ticks) does not cross a beat —
    no status_decayed events. The fixture stays byte-identical."""
    sim = Simulator(PACK, 42, tmp_path / "run.jsonl", SCHEMA, commit="0000000")
    from core.loop import load_playscript
    sim.run_playscript(load_playscript(
        REPO / "tests" / "playscripts" / "plumbing_smoke.json"
    ))
    _, events = read_log(tmp_path / "run.jsonl", SCHEMA)
    assert not by_type(events, DECAY_EVENT)
