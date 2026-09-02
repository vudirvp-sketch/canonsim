"""iter-4 acceptance — the goal/urge ticker (P2b, D-021): NPC goals →
occasional autonomous action through the same queue, same tick
discipline. Small-formula dynamics: a probability roll per beat, an
intent template, optional preconditions. World acts without the PC by
construction — M5 (non-PC event share) becomes non-trivially non-zero
at director-off (T8).

Through-the-door discipline (D-037): urgencies never write canon
directly. They produce IntentData the loop enqueues; the front door
validates each one like a playscript step.

iter-49 (content-4, D-078): the drunkard's entry is the coerce driver
now — the roll is the same draw, the leverage gate decides emission
(his idle wait is gone with it; the maid and the relief guard carry
the plain ungated rolls).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.fold import initial_projection
from core.leverage import LeverageFact
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, load_pack
from core.rng import RngBank
from core.urgencies import urgency_intents

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")

TAVERN = [{"intent": "move", "target": "loc_tavern"}]


def make_sim(tmp_path: Path, seed: int, name: str = "run.jsonl",
             pack: Pack = PACK) -> Simulator:
    return Simulator(pack, seed, tmp_path / name, SCHEMA, commit="0000000")


def script(steps: list[dict[str, Any]], seed: int) -> dict[str, Any]:
    return {"name": "test", "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}


def by_type(events: list[Any], event_type: str) -> list[Any]:
    return [e for e in events if e.type == event_type]


# -- the urgency rolls (small-formula dynamics) ------------------------------


def _live_fact() -> LeverageFact:
    """The drunkard's live cluster over the player (the gate's passport)."""
    return LeverageFact(
        holder="npc_drunk_01", subject="pc_01",
        secret="figure_reaching_for_purse", type="blackmail",
        expires_at=10_000, source="ev_0001",
    )


def test_urgency_roll_hits_and_misses_deterministically() -> None:
    """The probability roll draws from the substantive stream (canon
    rolls). Same seed = same sequence of hits/misses — measured through
    the drunkard's leverage-gated entry (content-4): with a live fact
    the hits vary by seed; without one the SAME rolls stay silent (the
    gate filters, the dice are unchanged)."""
    projection = initial_projection(PACK.entities)
    projection["pc_01"]["position"] = "loc_tavern"
    facts = (_live_fact(),)
    hits_per_seed = []
    for seed in range(20):
        bank = RngBank(seed)
        hits = sum(
            1 for _ in range(10)
            for intent in urgency_intents(PACK, projection, bank, facts=facts)
            if intent.actor == "npc_drunk_01"
        )
        hits_per_seed.append(hits)
    # across 20 seeds, at least one seed has a hit (the probability is 40%)
    assert any(h > 0 for h in hits_per_seed)
    # and at least one seed has a miss (the probability is 60% miss)
    assert any(h < 10 for h in hits_per_seed)
    # the gate: the same seeds' rolls, no live fact — always silent
    for seed in range(20):
        bank = RngBank(seed)
        silent = urgency_intents(PACK, projection, bank, facts=())
        assert not any(i.actor == "npc_drunk_01" for i in silent)


def test_urgency_skips_actors_absent_from_projection() -> None:
    """An NPC removed from the projection (arrested, fled) is skipped —
    the world doesn't roll for the dead."""
    projection = initial_projection(PACK.entities)
    del projection["npc_drunk_01"]
    bank = RngBank(42)
    intents = urgency_intents(PACK, projection, bank)
    assert all(i.actor != "npc_drunk_01" for i in intents)


def test_urgency_skips_caught_actors() -> None:
    projection = initial_projection(PACK.entities)
    projection["pc_01"]["crime_status"] = "caught"  # PC has the field by convention
    # urgencies target NPCs not the PC; but the same check applies to NPCs
    projection["npc_drunk_01"]["crime_status"] = "caught"
    bank = RngBank(42)
    intents = urgency_intents(PACK, projection, bank)
    assert all(i.actor != "npc_drunk_01" for i in intents)


def test_urgency_intent_carries_pack_template_target_and_fields() -> None:
    """The IntentData the urgency builds mirrors the pack's intent spec:
    kind, target (None when not declared), fields. The drunkard's
    template is the coerce driver's (content-4 — the leverage gate
    decides emission, never the template); the maid's is the plain
    wait."""
    projection = initial_projection(PACK.entities)
    projection["pc_01"]["position"] = "loc_tavern"
    facts = (_live_fact(),)
    for seed in range(50):
        bank = RngBank(seed)
        intents = urgency_intents(PACK, projection, bank, facts=facts)
        drunk_intents = [i for i in intents if i.actor == "npc_drunk_01"]
        if drunk_intents:
            intent = drunk_intents[0]
            assert intent.kind == "coerce"
            assert intent.target == "pc_01"
            assert intent.fields == {}
            assert intent.id.startswith("urgency_")
            break
    else:
        raise AssertionError("no seed produced a drunkard urgency hit in 50 tries")
    for seed in range(50):
        bank = RngBank(seed)
        intents = urgency_intents(PACK, projection, bank)
        maid_intents = [i for i in intents if i.actor == "npc_maid_01"]
        if maid_intents:
            assert maid_intents[0].kind == "wait"
            assert maid_intents[0].target is None
            assert maid_intents[0].fields == {"ticks": 1}
            return
    raise AssertionError("no seed produced a maid urgency hit in 50 tries")


def test_urgency_precondition_failure_silently_skips() -> None:
    """A roll that hits but whose preconditions fail stays silent — the
    NPC tried, the world said no. No rejection event (that's the director
    path's discipline); the world's noise floor absorbs it."""
    projection = initial_projection(PACK.entities)
    # the relief guard's urgency requires a flagged_accessible fire source
    # in the actor's location. The guardroom has no fire source initially.
    bank = RngBank(42)
    intents = urgency_intents(PACK, projection, bank)
    # the relief guard (npc_guard_02) at the guardroom has no fire source
    # accessible — the precondition fails, no intent emitted for him
    guard02_intents = [i for i in intents if i.actor == "npc_guard_02"]
    assert guard02_intents == []


# -- the world acts without the PC (T8 prerequisite: ≥1 autonomous chain) -----


def test_urgencies_fire_when_player_waits_long_enough(tmp_path: Path) -> None:
    """A wait longer than the beat cycle produces urgency events. The
    director is OFF (director_enabled=False) to isolate the urgency
    contribution to M5 (non-PC event share). Seed 1: the maid's roll
    hits at a crossed beat — the drunkard's own roll gates on leverage
    and stays silent without a cluster (content-4)."""
    sim = make_sim(tmp_path, seed=1, name="run.jsonl")
    sim.run_playscript(script([{"intent": "wait", "ticks": 1100}], 1))
    _, events = read_log(tmp_path / "run.jsonl", SCHEMA)
    # at least one non-PC actor appears in the event log (the urgency
    # fired the maid, at a crossed beat)
    non_pc_actors = {e.actor for e in events if e.actor != "pc_01" and e.actor != "world"}
    assert non_pc_actors  # the world acted without the PC


def test_urgency_intent_goes_through_the_front_door(tmp_path: Path) -> None:
    """Urgency intents run the same PROPOSED → ACCEPTED | REJECTED
    pipeline as playscript intents — a rejected urgency is a no-op
    intent_rejected event (the world noticed the attempt)."""
    sim = make_sim(tmp_path, seed=1, name="run.jsonl")
    sim.run_playscript(script([{"intent": "wait", "ticks": 1100}], 1))
    _, events = read_log(tmp_path / "run.jsonl", SCHEMA)
    # at least one non-PC event has cause_intent starting with 'urgency_'
    autonomous = [
        e for e in events
        if e.provenance.get("cause_intent", "").startswith("urgency_")
    ]
    # the wait crosses the first beat; some autonomy fired (M5 ≥ 1)
    assert autonomous


def test_urgency_completion_never_advances_the_playscript(tmp_path: Path) -> None:
    """KI#17 regression: only the PLAYER's step lifecycle feeds the next
    playscript step. An autonomous (urgency / director) intent ending
    mid-step must not propose the next step early — the script's ordered
    steps contract (MVP_SCOPE §13) holds. Probed seed 2: the maid's
    urgency fires while step 2 (a 50-tick wait) is in flight."""
    sim = make_sim(tmp_path, seed=2, name="run.jsonl")
    sim.run_playscript(script([
        {"intent": "wait", "ticks": 700},
        {"intent": "wait", "ticks": 50},
        {"intent": "move", "target": "loc_tavern"},
    ], 2))
    _, events = read_log(tmp_path / "run.jsonl", SCHEMA)
    # an autonomous intent DID fire during the run (the hazard is live)
    assert any(
        e.provenance.get("cause_intent", "").startswith("urgency_") for e in events
    )
    # the player's own events commit strictly in script order: the move
    # (step 3) never precedes the 50-tick wait's event (step 2)
    player_events = [
        e for e in events
        if e.provenance.get("cause_intent", "").startswith("intent_")
    ]
    order = [e.provenance["cause_intent"] for e in player_events]
    assert order == [f"intent_{i:04d}" for i in range(len(order))]
    ticks = [e.t for e in player_events]
    assert ticks == sorted(ticks)
    # and no player step's event lands before its predecessor's
    for earlier, later in zip(player_events, player_events[1:], strict=False):
        assert later.t >= earlier.t
