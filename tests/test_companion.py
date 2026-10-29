"""companion-1 + tune-3 — the companion arming, the first committed NPC
movement source (iter-157, the owner's «довести до ума сам генератор»
call: the standing queue's only build-ready generator row — the two rows
arm together or not at all).

The claim packet (TEST_PLAN §9):

- Claim: NPC movement armed as PURE PACK DATA (zero core change) makes
  the adjacent-shout beat live — a traveling knower one leg out on his
  own errand hears the alarm through the walls, and the knowledge
  carries onward to the player; the companion role (follow-duty, mode B
  voice, pair axes, arrival snapshots) lands over the existing doors.
- Lens(es): the changed-next-decision unit (WHO simulates changes — the
  census flip); the boundary lens (the no-teleport law: every companion
  leg an ordinary intent through the door).
- Prism: tune-3's own deciding probe — ONE CRAFTED TWIN with a traveling
  knower (the province data with the runner carrying his own lamp at
  load, the item's own note; the road's watched take is a near-designed
  impossibility — the best-of-observers perception beats the sleight at
  every measured seed) + the committed escort script.
- Oracle: the event log scans — the movement provenance (cause_intent
  urgency_*), the alarm_adjacent record (heard, vague), the panic
  echo's fear write, the telling's accepted fact, the arrival
  snapshots, the pole's ride.
- Falsifier: no shouting_near record on the traveler (the adjacency
  dead — the arming fails); a companion leg outside the door; the
  same-seed fork shifting other packs' fixtures.
- Expected evidence: the hop (urgency-provenanced move), the shout
  (vague, heard, on the MOVER — the travelers hold the static arm),
  the echo (+10 fear on the mover), the telling (the shout carried to
  the player, accepted), the snapshots, the pole's position contract.
- Observed evidence: CONFIRMED at the measured band (seed 61 the full
  loop; the probe scan the shout arm robust across the whole derived
  price range 600-825 — the W1=360/W2=900 waits ride every terrain
  draw).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the twin's fire arm is test-crafted — the
  committed smoke carries the hop alone; the alarm's ignition in a
  committed RUN waits for an authored fire script, the vocabulary now
  live).

The scene-LOD law shapes the design (depth-3, D-125): under the armed
macro clock only the ACTIVE scene rolls per-beat, so the road-leg beat
fires CO-LOCATED and the hop leaves the scene — the warm ring waits for
the reader. The companion's legs beyond the hop ride the mode B door
(the paired actor steps): the no-teleport law's letter — no hidden
"PC moved => companion follows" sync, lag a legal world state.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import Pack, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"
ESCORT = load_playscript(REPO / "tests" / "playscripts" / "province_companion.json")

DELLAN = "npc_secondhand_01"
POLE = "punt_pole_01"
SHOUT = "shouting_near_loc_weirstair"

#: The twin's fire scenario steps (tune-3's deciding probe): the walk to
#: the stair, the two waits (the first carries the beat that fires the
#: hop — W1=360 reaches the first beat strictly after the landing at ANY
#: derived price; the second outlasts the hop's own leg — the arson
#: lands with the second hand ADJACENT, one leg out on the road), the
#: boathouse arson, the reunion walk, the road-talk.
TWIN_STEPS: tuple[dict, ...] = (
    {"intent": "move", "target": "loc_weirstair"},
    {"intent": "wait", "ticks": 360},
    {"intent": "wait", "ticks": 900},
    {"intent": "arson", "target": "loc_weirstair"},
    {"intent": "move", "target": "loc_riverroad"},
    {"intent": "talk", "target": DELLAN},
)
TWIN_SEED = 61  # the full loop lands: the shout heard, the telling accepted


def _run(tmp_path: Path, name: str, script: dict) -> list:
    pack = load_pack(PACK_DIR)
    sim = Simulator(pack, script["seed"], tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    _header, events = read_log(tmp_path / name, SCHEMA)
    return events


def _twin_pack() -> Pack:
    """The crafted twin (tune-3's own probe shape): the province data
    with the runner carrying his own lamp at load — the item's note says
    whose it is; the road's watched take cannot pass at any measured
    seed, so the twin arms the fire source the honest way (load state,
    not a check-engineering hack)."""
    pack = load_pack(PACK_DIR)
    data = copy.deepcopy(dict(pack.data))
    entities = data["entities.json"]
    lamp = next(i for i in entities["items"] if i["id"] == "tallow_lamp_01")
    lamp["carrier"] = "pc_01"
    runner = next(n for n in entities["npcs"] if n["id"] == "pc_01")
    runner["carries"] = ["tallow_lamp_01"]
    return Pack(data=data)


def _run_twin(tmp_path: Path, name: str, seed: int = TWIN_SEED) -> list:
    sim = Simulator(_twin_pack(), seed, tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": list(TWIN_STEPS),
    })
    _header, events = read_log(tmp_path / name, SCHEMA)
    return events


# -- the census flip (tune-3's own gap closed) --------------------------------


def test_the_urgency_census_reads_a_move_kind() -> None:
    """The HEAD census: a committed pack arms an NPC movement source at
    last — the iter-150 revalidation read no move/travel intent kind in
    any committed pack, and alarm_adjacent rode declared-but-dormant in
    four packs. The second hand's road-leg beat is the first; the probe
    below decides the adjacent-shout half."""
    pack = load_pack(PACK_DIR)
    entries = pack.rules["urgencies"]["entries"]
    moves = [e for e in entries if e["intent"]["kind"] == "move"]
    assert len(moves) == 1, moves
    entry = moves[0]
    assert entry["npc"] == DELLAN
    assert entry["intent"]["target"] == "loc_riverroad"
    # the gate: the artery one leg away (silent at the errand's own end —
    # a location is never its own exit)
    assert entry["requires"] == [
        {"noun": "target", "test": "adjacent_to", "with": "actor"}
    ]
    # AP-8: the flaw key consumes the spine's flaw
    spine = next(npc["spine"] for npc in pack.entities["npcs"] if npc["id"] == DELLAN)
    assert entry["flaw"] == spine["flaw"]


def test_the_companion_carries_the_pole() -> None:
    """KI#87's fix: the weirkeeper's note cited a punt-pole item the
    items never carried — the family's last tool commits with the
    household's second hand (the pole is two-handed work), the carrier
    binding bidirectional (the entities lint's own law). The pair axes
    (companion-1's own surface): kin trust with the toll-taker, a
    working acquaintance with the runner."""
    pack = load_pack(PACK_DIR)
    pole = next(i for i in pack.entities["items"] if i["id"] == POLE)
    dellan = next(n for n in pack.entities["npcs"] if n["id"] == DELLAN)
    assert pole["carrier"] == DELLAN
    assert pole["position"] == dellan["position"] == "loc_weirstair"
    assert POLE in dellan["carries"]
    pairs = {p["with"]: p for p in dellan["pair_relations"]}
    assert pairs["npc_weirkeeper_01"]["trust"] == 80
    assert pairs["pc_01"]["trust"] == 45
    assert pairs["pc_01"]["suspicion"] == 0


# -- the escort (the committed pack, the mode B door) -------------------------


def test_the_road_leg_beat_fires_through_the_door(tmp_path: Path) -> None:
    """The movement source is autonomous AND through the door: the hop's
    event carries the urgency provenance, the state changes are the
    movement resolver's own (the position + the carried pole — KI#46's
    position contract on the first AUTONOMOUS mover)."""
    events = _run(tmp_path, "escort.jsonl", ESCORT)
    hops = [
        e for e in events
        if e.type == "move" and e.actor == DELLAN
        and e.provenance.get("cause_intent", "").startswith("urgency_")
    ]
    assert len(hops) == 1, "the road-leg beat fires exactly once"
    hop = hops[0]
    assert hop.target == "loc_riverroad"
    changes = {(c.entity, c.prop, c.from_, c.to_) for c in hop.state_changes}
    assert changes == {
        (DELLAN, "position", "loc_weirstair", "loc_riverroad"),
        (POLE, "position", "loc_weirstair", "loc_riverroad"),
    }
    # the beat-carry duplicates die at the door as honest no-ops
    # (attempts are facts): the mid-travel stale position re-passes the
    # gate until the landing commits — the designed noise, bounded
    rejects = [
        e for e in events
        if e.type == "intent_rejected" and e.actor == DELLAN
        and e.provenance.get("cause_intent", "").startswith("urgency_")
    ]
    assert len(rejects) == 1, "the carry noise is bounded (one duplicate)"


def test_the_arrival_snapshots_and_presence_reverification(tmp_path: Path) -> None:
    """companion-1's arrival-snapshot surface, live on the autonomous
    mover: the PRE-move projection resolves the movement sightings (the
    origin's observers see the departure, the destination's the arrival)
    and the mover himself re-verifies presence — one {present}_present
    record per entity at the landing site (st-1's expansion), refreshed
    again at the reunion."""
    events = _run(tmp_path, "escort.jsonl", ESCORT)
    hop = next(
        e for e in events
        if e.type == "move" and e.actor == DELLAN
        and e.provenance.get("cause_intent", "").startswith("urgency_")
    )
    records = {(r.who, r.knows) for r in hop.knowledge}
    # the origin: the runner and the toll-taker see him leave
    assert ("pc_01", "npc_secondhand_01_left_toward_loc_riverroad") in records
    assert ("npc_weirkeeper_01", "npc_secondhand_01_left_toward_loc_riverroad") in records
    # the destination: the road traffic sees him arrive
    for watcher in ("npc_drover_01", "npc_peddler_01", "npc_carrier_01"):
        assert (watcher, "npc_secondhand_01_arrived") in records
    # the mover's own snapshot: presence re-verified at the landing
    dellan_knows = {r.knows for r in hop.knowledge if r.who == DELLAN}
    assert dellan_knows == {
        "npc_drover_01_present", "npc_peddler_01_present",
        "npc_carrier_01_present", "tallow_lamp_01_present",
    }
    # the reunion: the runner's arrival snapshot names the companion
    reunion = next(
        e for e in events
        if e.type == "move" and e.actor == "pc_01" and e.target == "loc_riverroad"
    )
    assert (DELLAN, "pc_01_arrived") in {(r.who, r.knows) for r in reunion.knowledge}
    runner_sees = {r.knows for r in reunion.knowledge if r.who == "pc_01"}
    assert f"{DELLAN}_present" in runner_sees
    assert f"{POLE}_present" in runner_sees


def test_the_mode_b_voice_and_the_paired_leg(tmp_path: Path) -> None:
    """companion-1's voice and escort halves: the actor step (mode B's
    reply door) commits the companion's OWN talk — the event's actor IS
    the second hand, the conversation records render both ways — and the
    paired move is his own intent through the door, priced by the same
    travel law (the no-teleport pairing: one leg each, lag legal)."""
    events = _run(tmp_path, "escort.jsonl", ESCORT)
    voiced = [
        e for e in events
        if e.type == "talk" and e.actor == DELLAN
        and e.provenance.get("cause_intent", "").startswith("intent_")
    ]
    assert len(voiced) == 1, "the mode B actor step voiced the companion once"
    voice = voiced[0]
    assert voice.target == "pc_01"
    records = {(r.who, r.knows) for r in voice.knowledge}
    assert (DELLAN, "conversation_with_pc_01") in records
    assert ("pc_01", f"conversation_with_{DELLAN}") in records
    # the paired leg: the companion's own move to the keep
    paired = [
        e for e in events
        if e.type == "move" and e.actor == DELLAN
        and not e.provenance.get("cause_intent", "").startswith("urgency_")
    ]
    assert len(paired) == 1
    leg = paired[0]
    assert leg.target == "loc_keep"
    assert (POLE, "position", "loc_riverroad", "loc_keep") in {
        (c.entity, c.prop, c.from_, c.to_) for c in leg.state_changes
    }
    # the departure sighting: the companion watched the runner leave
    assert (DELLAN, "pc_01_left_toward_loc_keep") in {
        (r.who, r.knows)
        for e in events if e.type == "move" for r in e.knowledge
    }


def test_the_escort_is_deterministic(tmp_path: Path) -> None:
    """The twin of T1's law at the companion's own band: same seed +
    script + environment, byte-identical logs."""
    first = _run(tmp_path, "a.jsonl", ESCORT)
    second = _run(tmp_path, "b.jsonl", ESCORT)
    assert first == second


# -- the deciding probe (tune-3: one crafted twin with a traveling knower) ----


def test_the_traveling_knower_hears_the_shout(tmp_path: Path) -> None:
    """tune-3's deciding probe, CONFIRMED: the alarm's adjacent arm
    reaches the MOVER — the second hand, one leg out on his own errand,
    hears the stair's shout through the walls (channel heard, fidelity
    vague — a shout carries through walls; the record's first
    committed-pack instance on the movement-driven arm). The static arm
    (the road traffic, placed by worldgen) holds the same record — the
    probe's distinction is the MOVER: he was NOT there at load, his own
    beat walked him into the adjacency."""
    events = _run_twin(tmp_path, "twin.jsonl")
    alarm = next(e for e in events if e.type == "alarm_raised")
    assert alarm.target == "loc_weirstair"
    records = {(r.who, r.knows, r.channel, r.fidelity) for r in alarm.knowledge}
    # the traveling knower: the movement-driven adjacent hearer
    assert (DELLAN, SHOUT, "heard", "vague") in records
    # the static arm: the worldgen-placed road traffic hears it too
    for watcher in ("npc_drover_01", "npc_peddler_01", "npc_carrier_01"):
        assert (watcher, SHOUT, "heard", "vague") in records
    # the occupants' own record is the exact shout (the toll-taker)
    assert ("npc_weirkeeper_01", "fire_alarm_in_loc_weirstair", "heard", "exact") in records
    # the knower was NOT an occupant: no exact alarm record for him
    assert not any(r.who == DELLAN and r.knows == "fire_alarm_in_loc_weirstair"
                   for r in alarm.knowledge)


def test_the_panic_echo_reaches_the_adjacent_hearer(tmp_path: Path) -> None:
    """The through-the-walls law (content-2/D-077) live on the
    movement-driven arm: everyone who HEARD the shout — the adjacent
    hearers included — grows more afraid (+10, the contagion half, a
    quarter of the occupant spike)."""
    events = _run_twin(tmp_path, "twin.jsonl")
    ripple = next(e for e in events if e.type == "panic_ripple")
    fear = {c.entity: (c.from_, c.to_) for c in ripple.state_changes}
    assert fear[DELLAN] == (0, 10)
    for watcher in ("npc_drover_01", "npc_peddler_01", "npc_carrier_01"):
        assert fear[watcher] == (0, 10)
    # the occupant's compound: the spike (+40) then the echo (+10)
    assert fear["npc_weirkeeper_01"] == (40, 50)


def test_the_telling_carries_the_shout_to_the_player(tmp_path: Path) -> None:
    """The loop's last leg: the road-talk's telling picks the shout as
    the knower's most salient novel fact (importance_then_recency — the
    alarm is story-critical) and the runner ACCEPTS it: the player learns
    the crossing shouted at his fire through the companion alone (he
    holds no alarm record of his own beyond the shout he heard standing
    in it — the exact occupant arm excluded the cause actor)."""
    events = _run_twin(tmp_path, "twin.jsonl")
    told = [
        e for e in events
        if e.type == "rumor_told" and e.actor == DELLAN and e.target == "pc_01"
    ]
    assert len(told) == 1
    telling = told[0]
    assert telling.outcome["knows"] == SHOUT
    assert telling.outcome["accepted"] is True
    assert telling.outcome["fidelity"] == "vague"
    # the knowledge record landed on the player (told, one step down)
    assert ("pc_01", SHOUT, "told", "vague") in {
        (r.who, r.knows, r.channel, r.fidelity) for r in telling.knowledge
    }


def test_the_twin_is_deterministic(tmp_path: Path) -> None:
    """The twin holds T1's law too: byte-identical at the fixed seed."""
    first = _run_twin(tmp_path, "a.jsonl")
    second = _run_twin(tmp_path, "b.jsonl")
    assert first == second
