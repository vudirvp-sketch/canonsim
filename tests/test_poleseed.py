"""poleseed — the pole's embodiment seeds (iter-161, the owner's «надо
решить что начали в прошлой итерации» call, item (a)): the crossing
household's carrier completed as a SOCIAL carrier over existing
substrate only — pure pack data, zero core change (the KI#87 precedent
class, iter-157's companion arming).

The two seeds (the W4 working set's own named embodiment options,
`WORLD_WORKPLAN.md` §6 candidate 2; ANCHOR_REGION §6.1's gates line):

- the flood-story RECOGNITION TOKEN — `the_flood_story`, minted by the
  close read of the pole (the `read_pole` hinge, the grim read_ticket
  precedent's second instance) and registered in the secrets table
  over the toll-taker (the debtor): whoever learns the flood story
  holds the lever at the stair;
- the `steal_target` FLAG — the verb-gate boundary's unless-arm
  (`WORLD_AUTHORING.md` §8): the pole liftable unseen from the second
  hand, the player-facing ablation's own gate.

The claim packet (TEST_PLAN §9):

- Claim: the pole's social-recognition half and its player-facing
  ablation are each ONE pack-data seed — the carrier formula's PUBLIC
  RECOGNITION, TRANSFER and RELATIONSHIP CHANGE rungs (kurvitz.md §6)
  embodied with zero core change; the material half was already
  committed (iter-157, test-pinned there).
- Lens(es): the changed-next-decision unit (who simulates differently
  — the reader holds a live cluster over the toll-taker; the thief
  owns the household's tool); the boundary lens (the flag opens
  exactly one gate — take stays uncarried-gated, drop_break stays the
  carrier's own).
- Prism: three deterministic chains on the committed pack (the
  day-read lever chain, the night-read acquisition arm, the theft
  ablation chain) at probed seeds — the reads are check-deterministic
  at every seed (perception 50 vs difficulty 30, both d20: the healthy
  reader never fails); the theft's pass/fail arms ride the opposed
  stealth draw.
- Oracle: the event log scans — the read's record, the leverage mint's
  cluster, the coerce balance, the steal's carrier flip, the road-leg
  hop's state changes.
- Falsifier: no leverage_gained on the read (the token dead); the hop
  still carrying the pole after a successful theft (the ablation a
  lie); the same-seed fork shifting other packs' fixtures.
- Expected evidence: pole_read exact -> leverage_gained (pc over
  Ketta, type debt) -> coerce (trust 25 / fear 75 from neutral); the
  night read partial (the unlit stair, the acquisition arm); steal
  flips the carrier and the next hop walks the second hand pole-less;
  the failed lift mints the sighting and flips nothing.
- Observed evidence: CONFIRMED at the measured band (seed 42 the day
  chain, the night chain and the total-failure arm; seed 2 the lift).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded in the secrets
  notes: the family's own read/telling mints the cluster too — the
  lived knowledge is not event-recorded; dormant, no driver).

The honest pre-existing shape left as found (never patched in a
zero-core slice): the province's secrets block declares no
`spend_event` — the coerce event carries no cluster stamp and the
cluster stays live after a spend (the grim pack's one-spend-door law
is that pack's own declaration); the sighting token
`figure_reaching_for_tin` names the tin family's anchor but rides
every steal failure — the pole's failed lift mints it too (the
template line is item-neutral since iter-161; the token name stays).
"""

from __future__ import annotations

import json
from pathlib import Path

from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

PC = "pc_01"
KETTA = "npc_weirkeeper_01"
DELLAN = "npc_secondhand_01"
POLE = "punt_pole_01"
STORY = "the_flood_story"

#: The lever chain (seed 42, probed: the move lands at t=705, the read
#: check-deterministic): the walk to the stair, the close read, the
#: corner at the toll-taker.
READ_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": "loc_weirstair"},
    {"intent": "read_pole", "target": POLE},
    {"intent": "coerce", "target": KETTA},
)
#: The night twin: the same walk plus the wait to the night phase
#: (t=1080) — the unlit stair's acquisition arm on the read.
NIGHT_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": "loc_weirstair"},
    {"intent": "wait", "ticks": 375},
    {"intent": "read_pole", "target": POLE},
)
#: The theft chain (the ablation): the walk, the lift, the two waits
#: that carry the road-leg beat — seed 2 lifts the pole, seed 42 is
#: the total-failure arm.
THEFT_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": "loc_weirstair"},
    {"intent": "steal", "target": DELLAN},
    {"intent": "wait", "ticks": 360},
    {"intent": "wait", "ticks": 900},
)
SEED_DAY = 42  # the read exact, the lever minted, the corner spent
SEED_NIGHT = 42  # the same clock: the read lands at t=1082, in the night
SEED_LIFT = 2  # the stealth draw passes: the pole lifted unseen
SEED_FAIL = 42  # the total-failure margin: the whole crossing sees


def _run(tmp_path: Path, name: str, seed: int, steps: tuple[dict, ...]) -> list:
    pack = load_pack(PACK_DIR)
    sim = Simulator(pack, seed, tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": [dict(step) for step in steps],
    })
    _header, events = read_log(tmp_path / name, SCHEMA)
    return events


def _action(pack, intent: str) -> dict:
    return next(a for a in pack.data["actions.json"]["actions"]
                if a["intent"] == intent)


# -- the census (the two seeds as pack data) -----------------------------------


def test_the_flag_opens_exactly_one_gate() -> None:
    """The verb-gate boundary (`WORLD_AUTHORING.md` §8): carried ⇒
    untakeable, unstealable UNLESS flagged, breakable only by its
    carrier. The pole now carries the flag — and the flag widens
    exactly one door: steal's carries_flagged. Take keeps its
    uncarried gate (a carried pole is still not pick-up-able),
    drop_break keeps the carrier's own gate."""
    pack = load_pack(PACK_DIR)
    pole = next(i for i in pack.entities["items"] if i["id"] == POLE)
    assert pole["steal_target"] is True
    steal = _action(pack, "steal")
    assert {"noun": "target", "test": "carries_flagged",
            "flag": "steal_target"} in steal["requires"]
    take = _action(pack, "take")
    assert {"noun": "target", "test": "uncarried"} in take["requires"]
    drop = _action(pack, "drop_break")
    assert {"noun": "target", "test": "carried_by", "who": "actor"} in drop["requires"]


def test_the_read_is_pinned_to_the_pole() -> None:
    """The recognition hinge: a pack-specific close read (the grim
    read_ticket shape — the field_in id pin means studying any other
    stave mints nothing), perception-gated, minting the LITERAL token
    on success (the templated-token ineligibility law) and only the
    vague unread marks on failure — a failed read mints no cluster."""
    pack = load_pack(PACK_DIR)
    read = _action(pack, "read_pole")
    assert read["check"] == {"kind": "perception", "difficulty": 30}
    assert read["requires"] == [
        {"noun": "target", "test": "kind", "is": "item"},
        {"noun": "target", "test": "same_location", "with": "actor"},
        {"noun": "target", "test": "field_in", "field": "id",
         "values": [POLE]},
    ]
    assert read["knowledge"]["success"] == [
        {"who": "actor", "channel": "saw", "fidelity": "exact",
         "knows": STORY}
    ]
    assert read["knowledge"]["failure"] == [
        {"who": "actor", "channel": "saw", "fidelity": "vague",
         "knows": "unread_marks_on_the_pole"}
    ]
    # the honest failure surface: the vague token is not a secret
    assert "unread_marks_on_the_pole" not in pack.rules["secrets"]["tokens"]
    # the tale renders both arms (EVENT_SCHEMA §11)
    assert "pole_read" in pack.templates["events"]
    assert "pole_read_failed" in pack.templates["events"]


def test_the_story_is_registered_over_the_toll_taker() -> None:
    """The lever's registration: the flood story is a DEBT-type secret
    whose subject is the toll-taker (the debtor) — distinguished from
    blackmail's witnessed transgression; the expiry one full season
    (129600 — the debt's reckoning unit, the lever living through the
    season's collection)."""
    pack = load_pack(PACK_DIR)
    spec = pack.rules["secrets"]["tokens"][STORY]
    assert spec == {
        "subject": KETTA, "type": "debt", "expires_ticks": 129600,
    }


# -- the lever chain (the recognition -> the mint -> the corner) ---------------


def test_the_read_mints_the_story_and_the_lever(tmp_path: Path) -> None:
    """The social-recognition half, live: the close read mints the
    exact flood story on the reader, and the secrets registry turns it
    into the lever at the stair — one leverage_gained cluster, holder
    the reader, subject the toll-taker, expiry the season's window."""
    events = _run(tmp_path, "read.jsonl", SEED_DAY, READ_CHAIN)
    read = [e for e in events if e.type == "pole_read"]
    assert len(read) == 1
    assert (PC, STORY, "saw", "exact") in {
        (r.who, r.knows, r.channel, r.fidelity) for r in read[0].knowledge
    }
    gained = [e for e in events if e.type == "leverage_gained"]
    assert len(gained) == 1
    cluster = gained[0]
    assert cluster.actor == PC and cluster.target == KETTA
    assert cluster.t == read[0].t  # the mint rides the read's own commit
    assert cluster.outcome == {
        "secret": STORY, "type": "debt", "fidelity": "exact",
        "expires_at": read[0].t + 129600,
    }


def test_the_lever_opens_the_corner_and_shifts_the_pair(tmp_path: Path) -> None:
    """The lever is spendable at the stair: the coerce door reads the
    live cluster and the corner lands — the toll-taker's directed pair
    homes toward the reader break (trust from neutral 50-25) and spike
    (fear 50+25, D-030's break-fast law). The province's standing
    shape: no spend_event declared, so the event carries no cluster
    stamp and the cluster stays live (the grim one-spend-door law is
    that pack's own)."""
    events = _run(tmp_path, "read.jsonl", SEED_DAY, READ_CHAIN)
    corners = [e for e in events if e.type == "coerce"]
    assert len(corners) == 1
    corner = corners[0]
    assert corner.actor == PC and corner.target == KETTA
    assert "cluster" not in corner.outcome  # no spend_event declared
    assert {(c.entity, c.prop, c.from_, c.to_) for c in corner.state_changes} == {
        (KETTA, "pair.pc_01.trust", None, 25),
        (KETTA, "pair.pc_01.fear", None, 75),
    }


def test_the_corner_without_the_read_dies_at_the_door(tmp_path: Path) -> None:
    """The leverage test IS the door (social-1b's law): no story, no
    corner — the attempt is a fact (intent_rejected names the failed
    lever test), never a write."""
    events = _run(tmp_path, "bare.jsonl", SEED_DAY, READ_CHAIN[:1] + (
        {"intent": "coerce", "target": KETTA},
    ))
    assert not [e for e in events if e.type == "coerce"]
    rejections = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "coerce"
    ]
    assert len(rejections) == 1
    assert "leverage_over" in rejections[0].outcome["failed_test"]


def test_the_night_read_steps_the_story_down(tmp_path: Path) -> None:
    """The acquisition arm rides the new verb: the weir stair is
    unlit, and a read in the night phase steps the record down the
    fidelity chain — the flood story learned PARTIAL by dark, half the
    tale legible. The cluster still mints (a partial-knowing holder
    still holds the lever, the cluster recording how well)."""
    events = _run(tmp_path, "night.jsonl", SEED_NIGHT, NIGHT_CHAIN)
    read = next(e for e in events if e.type == "pole_read")
    assert 1080 <= read.t < 1440  # the night phase pinned by the wait
    assert (PC, STORY, "saw", "partial") in {
        (r.who, r.knows, r.channel, r.fidelity) for r in read.knowledge
    }
    cluster = next(e for e in events if e.type == "leverage_gained")
    assert cluster.outcome["fidelity"] == "partial"


# -- the theft chain (the player-facing ablation) ------------------------------


def test_the_lift_flips_the_carrier_binding(tmp_path: Path) -> None:
    """The flagged theft, live: the steal against the second hand
    lifts the pole unseen (the door now passes — pre-flag this step
    died at carries_flagged), the carrier binding flips to the thief,
    and the quiet lift mints no sighting (the unseen arm)."""
    events = _run(tmp_path, "lift.jsonl", SEED_LIFT, THEFT_CHAIN)
    lifts = [e for e in events if e.type == "steal"]
    assert len(lifts) == 1
    lift = lifts[0]
    assert lift.actor == PC and lift.target == DELLAN
    assert lift.outcome["stolen"] == POLE
    assert [(c.entity, c.prop, c.from_, c.to_) for c in lift.state_changes] == [
        (POLE, "carrier", DELLAN, PC)
    ]
    # the quiet arm: a successful lift teaches nobody anything
    assert not any(e.type == "leverage_gained" for e in events)


def test_the_stolen_pole_stops_traveling_with_the_role(tmp_path: Path) -> None:
    """The carrier-availability law's dark half, pinned: after the
    lift the road-leg beat still walks the second hand to the artery —
    but the position contract now binds the pole to the THIEF: the hop
    moves the man alone, the pole stays at the stair, and the second
    hand's arrival snapshot no longer verifies the pole's presence
    (the household's tool availability degraded through ordinary
    movement, never a scripted flag)."""
    events = _run(tmp_path, "lift.jsonl", SEED_LIFT, THEFT_CHAIN)
    hops = [
        e for e in events
        if e.type == "move" and e.actor == DELLAN
        and e.provenance.get("cause_intent", "").startswith("urgency_")
    ]
    assert len(hops) == 1, "the road-leg beat fires after the lift"
    hop = hops[0]
    assert hop.target == "loc_riverroad"
    assert [(c.entity, c.prop, c.from_, c.to_) for c in hop.state_changes] == [
        (DELLAN, "position", "loc_weirstair", "loc_riverroad")
    ]
    assert POLE not in {c.entity for c in hop.state_changes}
    # the arrival snapshot: the pole is absent from his verified world
    dellan_knows = {r.knows for r in hop.knowledge if r.who == DELLAN}
    assert f"{POLE}_present" not in dellan_knows
    # and the pole's own position never left the stair
    position_writes = [
        c for e in events for c in e.state_changes
        if c.entity == POLE and c.prop == "position"
    ]
    assert not position_writes, "the stolen pole never moves again"


def test_the_failed_lift_is_the_fact_family(tmp_path: Path) -> None:
    """The world's answer to the attempt (attempts are facts): the
    total-failure margin means the whole crossing sees the reach — the
    pre-existing sighting family (the tin-named token, the token name
    left as found) mints the watchers' clusters over the thief, and
    the pole never moves: no carrier flip, the second hand still
    armed for the next beat."""
    events = _run(tmp_path, "fail.jsonl", SEED_FAIL, THEFT_CHAIN)
    failed = [e for e in events if e.type == "pickpocket_failed"]
    assert len(failed) == 1
    assert failed[0].outcome["check"]["total_failure"] is True
    assert not failed[0].state_changes  # nothing lifted
    # the witnesses hold the sighting (the target + the room)
    records = {(r.who, r.knows) for r in failed[0].knowledge}
    assert (DELLAN, "figure_reaching_for_tin") in records
    assert (KETTA, "figure_reaching_for_tin") in records
    # and the sighting is leverage over the thief (the tin family's
    # own registration — the pre-existing cascade, now reachable
    # through the pole's theft too)
    holders = {e.actor for e in events if e.type == "leverage_gained"}
    assert holders == {KETTA, DELLAN}
    # the pole stays with its carrier
    assert not [
        c for e in events for c in e.state_changes
        if c.entity == POLE and c.prop == "carrier"
    ]


def test_the_chains_are_deterministic(tmp_path: Path) -> None:
    """The twin of T1's law at the seeds' own band: same seed + script
    + environment, byte-identical logs — both chains."""
    for name, seed, steps in (
        ("read", SEED_DAY, READ_CHAIN),
        ("lift", SEED_LIFT, THEFT_CHAIN),
    ):
        first = _run(tmp_path, f"{name}_a.jsonl", seed, steps)
        second = _run(tmp_path, f"{name}_b.jsonl", seed, steps)
        assert first == second
