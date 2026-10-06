"""marketlegs — the §6.5 embodiment legs (iter-264, the owner's
«продолжай работы по embodiment-ногам §6.5» call over iter-263's
carrier-or-surface verdict: the J-rows' reader legs landed as PURE
PACK DATA over the existing primitives — zero core change, the
KI#87/campaccount precedent class):

- **The mourns hook** (the state→behavior reader): the director hook
  `market_mourns` — Maren's grief for the burned stalls, the FOURTH
  murmur of the D-082 family and the FIRST state-gated one. The prop
  trigger reads `loc_malby.destroyed`; the seed rides the wait
  action's hooks (the murmur family's own site — the ignite resolver
  mints no action hooks, iter-263's §D boundary). THE INTENT PICK
  re-authored iter-274 (the owner's execution order opening the
  move-release row): the MOVE release — the keeper of the weighbeam
  LEAVES the ashes for the keep (her need was the market's paper, the
  son's bond covered by the stalls — the fire took the coverage with
  the stalls, the beam has no keeper where the stall row is ash; the
  watch's post the widow's own road). The ramble was iter-264's
  authored pick (grief made audible, the wilmot_grief_ramble rhyme);
  the departure is the grief answering with feet — the market's
  social function dying with its carrier, the measured price HONESTLY
  PAID (iter-263's I3a prediction, re-measured on the committed form
  in the composition witness: the talks collapse to 2, the rumors to
  2, the council pile-up 1→208 off the cold-frozen fear — the B2
  catch-up semantics through the faction door, the known one-tick
  pile shape).
- **The option gate** (the trigger-only law): a triggered hook stays
  quiet-path eligible by construction, and a weight-0 ambient hook
  would mourn a STANDING market — the drama-2 option layer carries
  the SAME prop read as its availability gate, so the only world
  where the hook releases on ANY path (causal, climax or quiet) is
  the world where the trigger already fires. The hook-level trigger
  keeps the release causal (D-005); the option gate closes the pacing
  doors behind it.
- **The trade door** (the state→economy reader): `trade_at_market` —
  an account verb whose `spot_available` gate reads the SAME fire
  layer the arson door reads: the commerce closes with the stalls BY
  CONSTRUCTION (a burned-out Malby refuses the trade softly at the
  door — attempts are facts), and the spots stay in the burning state
  through the burnout, so the closure never reopens. Unarmed by
  doctrine (no urgency entry, no faction door — the census's
  UNREALIZED band until a witness exercises it, THIS file's witness).
- **The knowledge legs** (the institutions' epistemic half): the
  council/vigil acts' authored knowledge blocks — the public act's
  honest residue is KNOWLEDGE, never a boolean flag (iter-263's
  measured law): the co-located hear partial, the adjacent vague; the
  world answers through the acquisition gate (the smoke of the still
  burning market degrades the council's co-located records to vague).
- **The purse**: pc_01's coin six — the trade door's walking stock
  (the buyer's purse, the guild's chest the receiving end).

The claim packet (TEST_PLAN §9):

- Claim: the market's READER legs land as pure pack data — the
  director reads the burnout (the mourns departure, the carrier
  leaving the ashes with her staff), the door gates the commerce on
  the fire layer,
  the institutions' acts mint their witnesses' records, and the
  watch-briefing carries the trade's token (the institutional
  memory consumer) — zero core, zero new primitives.
- Lens(es): the changed-next-decision unit (who simulates
  differently — a burned market now ANSWERS: the mistress departs
  for the keep, the buyers' door refuses, the towns hold the barring
  and the blood price as records); the boundary lens (the trigger-only
  law — the option gate; the unarmed trade — the parse grammar's
  own verb, never an autonomous driver).
- Prism: the committed-pack census (the hook, the blocks, the gates,
  the purse); the minimal integrated witness below (all four legs,
  one route); the no-leak arm (a standing market never mourns).
- Oracle: the event-log scans (the account transfers, the rejection's
  failed_test, the move's carried staff, the knowledge records'
  holders/fidelity, the briefing's token), the projection reads, the
  byte-identical twin.
- Falsifier: a Maren departure before the burnout (the quiet-path
  leak — the option gate broken); the trade accepted after the burnout
  (the fire layer's irreversibility broken); the council/vigil
  events carrying no records (the KI#103 family's dead data); the
  purse minting stock from nothing (the underflow gate bypassed).
- Expected evidence: the oracles below over the seed-2 minimal
  witness; the composition witness's re-pinned surface (its own
  file); the province golden's 3-line delta (the wait tags), pinned
  by the T1 regen guard.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.fold import fold, initial_projection
from core.log import EventRecord, read_log
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

#: the embodiment unit's own cast
MAREN = "npc_marketmistress_01"
CHEST = "loc_malby"
CROWD = "npc_malby_crowd_01"
SERGEANT = "npc_sergeant_01"
CORPORAL = "npc_corporal_01"
STEWARD = "npc_steward_01"

#: the minimal witness route: the runner takes the lamp, burns the
#: keep's hearth (one elder woken), walks to Malby, BUYS at the stalls
#: (the trade leg, accepted), burns the stall row (the other elder
#: woken; the burnout 120 ticks on), waits (the seed + the beats),
#: tries to buy again (the trade leg, rejected — the ashes), then
#: walks to Thornmill and waits through the vigil window (the old
#: families' faction anchors there — the scene LOD's active zone).
STEPS: list[dict[str, Any]] = [
    {"intent": "take", "target": "tallow_lamp_01"},
    {"intent": "move", "target": "loc_keep"},
    {"intent": "arson", "target": "loc_keep"},
    {"intent": "move", "target": CHEST},
    {"intent": "trade_at_market", "target": CHEST},
    {"intent": "arson", "target": CHEST},
    {"intent": "wait", "ticks": 1440},
    {"intent": "trade_at_market", "target": CHEST},
    {"intent": "move", "target": "loc_thornmill"},
    {"intent": "wait", "ticks": 1440},
]


def _run(
    tmp_path: Path, name: str, steps: list[dict[str, Any]], seed: int = 2,
) -> tuple[list[EventRecord], Any]:
    pack = load_pack(PACK_DIR)
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    result = sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": steps,
    })
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, result


#: The witness seed (the epoch's rolls — rng-1's corpus price; the
#: pre-epoch seed 2's lamp take failed at the boundary).
WITNESS_SEED: int = 229


@pytest.fixture(scope="module")
def witness(tmp_path_factory: pytest.TempPathFactory) -> list[EventRecord]:
    """The minimal legs run, once per module."""
    events, _result = _run(
        tmp_path_factory.mktemp("marketlegs"), "witness.jsonl", STEPS,
        seed=WITNESS_SEED,
    )
    return events


def _of(events: list[EventRecord], *types: str) -> list[EventRecord]:
    return [e for e in events if e.type in types]


def _changes(event: EventRecord) -> dict[tuple[str, str], tuple[Any, Any]]:
    return {(c.entity, c.prop): (c.from_, c.to_) for c in event.state_changes}


def _records(event: EventRecord) -> dict[str, tuple[str, str]]:
    """The knowledge records as holder -> (token, fidelity)."""
    return {k.who: (k.knows, k.fidelity) for k in event.knowledge}


# -- the census (the legs as committed pack data) ------------------------------


def test_the_embodiment_census() -> None:
    """The legs as pack data: the hook (weight 0, ambient, once, the
    prop trigger + the option gate reading the same burnout), the wait
    seeding, the two knowledge blocks, the trade verb's gate stack,
    the purse, the budget inside its declared bounds."""
    pack = load_pack(PACK_DIR)
    hooks = pack.rules["director"]["hooks"]
    # the budget: the mourns grows the hooks to eight, inside the
    # declared 5-9 (no re-declare owed)
    assert 5 <= len(hooks) <= 9 and len(hooks) == 8
    mourns = hooks["market_mourns"]
    assert mourns["weight"] == 0 and mourns["first_time_only"] is True
    assert mourns["channel"] == "ambient"
    assert mourns["target_npc"] == MAREN
    # iter-274: the intent pick re-authored — the departure (the owner's
    # move-release row), the ramble's replacement
    assert mourns["intent"] == {"kind": "move", "target": "loc_keep"}
    prop = {
        "kind": "prop", "of": CHEST, "path": "destroyed",
        "comparator": "equals", "value": True,
    }
    assert mourns["trigger"] == prop
    # the trigger-only law: the option gate carries the SAME read, so
    # no pacing path (quiet or climax) can release an unburned mourns
    assert [o["trigger"] for o in mourns["options"]] == [prop]
    # the seed: the murmur family's own site
    wait = pack.action("wait")
    assert wait["hooks"]["success"] == ["wilmot_grief_ramble", "market_mourns"]
    # the knowledge legs: the public acts' honest residue
    council = pack.action("council")
    assert council["knowledge"]["success"] == [
        {"who": "same_location", "except": ["actor"],
         "channel": "heard", "fidelity": "partial",
         "knows": "the_guild_bars_the_stalls"},
        {"who": "adjacent_locations",
         "channel": "heard", "fidelity": "vague",
         "knows": "the_guild_bars_the_stalls"},
    ]
    vigil = pack.action("hold_vigil")
    assert vigil["knowledge"]["success"] == [
        {"who": "same_location", "except": ["actor"],
         "channel": "heard", "fidelity": "partial",
         "knows": "the_blood_price_spoken"},
        {"who": "adjacent_locations",
         "channel": "heard", "fidelity": "vague",
         "knows": "the_blood_price_spoken"},
    ]
    # the trade door: the gate stack over the fire layer
    trade = pack.action("trade_at_market")
    assert trade["account"] == {"verb": "transfer", "kind": "coin", "amount": 2}
    tests = [(c["noun"], c["test"]) for c in trade["requires"]]
    assert tests == [
        ("target", "kind"), ("target", "field_in"), ("target", "same_location"),
        ("target", "spot_available"), ("actor", "account_at_least"),
        ("target", "account_at_least"),
    ]
    spot = next(c for c in trade["requires"] if c["test"] == "spot_available")
    assert spot["layer"] == "fire"
    # the purse: the walking stock the solvency gate reads
    pc = next(n for n in pack.entities["npcs"] if n["id"] == "pc_01")
    assert pc["accounts"] == {"coin": 6}


def test_the_unarmed_trade_rides_no_driver() -> None:
    """The doctrine's own unarmed law: no urgency entry, no faction
    door names the trade verb — the census's UNREALIZED band is the
    honest state (the player's parse verb, realized by witnesses, not
    by the world's own drivers)."""
    pack = load_pack(PACK_DIR)
    for entry in pack.rules["urgencies"]["entries"]:
        assert entry["intent"]["kind"] != "trade_at_market"
    for entry in pack.rules["factions"]["entries"]:
        assert entry["intent"]["kind"] != "trade_at_market"


# -- the no-leak arm (the trigger-only law) ------------------------------------


def test_a_standing_market_never_mourns(tmp_path: Path) -> None:
    """The falsifier's own witness: an idle year with the hook seeded
    (the wait carries the tag) and the market standing — the ambient
    quiet gate is OPEN (weight-0 channel, entropy 0) and the clock
    idles, so WITHOUT the option gate the mourns would release here.
    The option gate must hold: no Maren ramble, no materialized
    residue — the standing market never mourns."""
    events, _result = _run(tmp_path, "idle.jsonl", [
        {"intent": "wait", "ticks": 720},
    ])
    assert not [e for e in events if e.type == "ramble" and e.actor == MAREN]
    projection = fold(events, initial_projection(load_pack(PACK_DIR).entities))
    assert "under_stall_row" not in projection[CHEST]
    assert projection[CHEST].get("destroyed") is not True


# -- the trade leg (the state→economy door) ------------------------------------


def test_the_trade_door_opens_at_the_stalls(
    witness: list[EventRecord],
) -> None:
    """The accepted purchase: the runner's coin walks to the chest at
    the weighbeam (render_fund's own shape — the account verb over the
    same door), and the market's own people see the beat: the
    co-located watchers (the duty corporal at the post — the rotation
    moved the sergeant to his rest — the mistress, the queue) each
    hold the saw-partial record."""
    events = witness
    trades = _of(events, "account_transferred")
    assert len(trades) == 1 and trades[0].actor == "pc_01"
    changes = _changes(trades[0])
    assert changes[("pc_01", "account.coin")] == (6, 4)
    assert changes[(CHEST, "account.coin")] == (40, 42)
    assert _records(trades[0]) == {
        CORPORAL: ("coin_changed_hands_at_loc_malby", "partial"),
        MAREN: ("coin_changed_hands_at_loc_malby", "partial"),
        CROWD: ("coin_changed_hands_at_loc_malby", "partial"),
    }


def test_the_trade_door_closes_with_the_stalls(
    witness: list[EventRecord],
) -> None:
    """The burned market refuses the commerce SOFTLY at the door —
    attempts are facts: the rejection names the failed gate
    (target.spot_available — the fire layer's own read, the same
    grammar the arson door keys on), and it lands AFTER the burnout
    (the closure is the burnout's, never a scripted beat)."""
    events = witness
    burnouts = _of(events, "location_burned_out")
    assert {b.target for b in burnouts} == {"loc_keep", CHEST}
    rejected = [
        e for e in _of(events, "intent_rejected")
        if e.outcome.get("action") == "trade_at_market"
    ]
    assert len(rejected) == 1
    assert rejected[0].outcome["reason"] == "precondition"
    assert rejected[0].outcome["failed_test"] == "target.spot_available"
    market_burnout = next(b for b in burnouts if b.target == CHEST)
    assert rejected[0].t > market_burnout.t


# -- the mourns leg (the state→behavior door) ----------------------------------


def test_the_mourns_release_reads_the_ashes(
    witness: list[EventRecord],
) -> None:
    """The reader the burnout lacked, iter-274's re-authored pick: the
    mistress's DEPARTURE, released by the director after the seed
    finds the ashes — the MOVE release (the keeper leaves the ashes
    for the keep, the grief answering with feet), the tally staff
    riding with her (the carried-item contract, iter-263's measured
    shape reproduced on the committed form), and the ramble GONE (the
    release replaced, never doubled — first_time_only's own law). The
    scene's residue — the dropped tally under the stall row — still
    materializes: the observe family's LAZY canon birth on the
    market's own stream, the sergeant's post-burnout scan drawing it
    first in this witness (t=1153, three ticks past the burnout) —
    the ramble's own draw is gone, the stream's birth remains
    (INV-2: the draw is the stream's, never the observer's)."""
    events = witness
    market_burnout = next(
        b for b in _of(events, "location_burned_out") if b.target == CHEST
    )
    # the departure: one move, director-caused, after the burnout
    mourns = [
        e for e in _of(events, "move") if e.actor == MAREN
        and e.provenance["cause_intent"].startswith("director_")
    ]
    assert len(mourns) == 1, "one mourns per run (first_time_only)"
    departure = mourns[0]
    assert departure.t == 3297 and departure.t > market_burnout.t  # the epoch's rolls
    assert departure.target == "loc_keep"
    assert _changes(departure) == {
        (MAREN, "position"): (CHEST, "loc_keep"),
        ("tally_staff_01", "position"): (CHEST, "loc_keep"),
    }
    # the ramble replaced, never doubled
    assert not [e for e in _of(events, "ramble") if e.actor == MAREN]
    # the scene's residue: the lazy birth still lands on the stream
    projection = fold(events, initial_projection(load_pack(PACK_DIR).entities))
    assert projection[CHEST]["under_stall_row"] == "dropped_tally"
    assert projection[CHEST]["destroyed"] is True


# -- the knowledge legs (the institutions' epistemic half) ----------------------


def test_the_council_mints_the_barring(
    witness: list[EventRecord],
) -> None:
    """The guild's public act leaves its residue as KNOWLEDGE: the
    co-located hold the barring record — degraded to VAGUE by the
    acquisition gate (the still-burning market's smoke — the world's
    own answer, not the authored fidelity), the adjacent towns (the
    duty post's rotation pair, the manor) hold it dimly. The boolean
    'barred stalls' flag is inexpressible and unneeded: the record IS
    the state."""
    events = witness
    councils = _of(events, "guild_councils")
    assert len(councils) == 1 and councils[0].actor == "grp_river_guild"
    assert councils[0].provenance["cause_intent"] == "faction_0000"
    records = _records(councils[0])
    assert set(records) == {
        "pc_01", CORPORAL, MAREN, CROWD, SERGEANT, STEWARD,
    }
    assert all(
        token == "the_guild_bars_the_stalls" and fidelity == "vague"
        for token, fidelity in records.values()
    ), "the smoke gate degrades the co-located partials; the adjacent are vague_only"


def test_the_vigil_mints_the_blood_price(
    witness: list[EventRecord],
) -> None:
    """The families' public act likewise: Thornmill hears the blood
    price spoken (partial — the runner stands there, the steward
    beside him), Malby through the market walls (vague). iter-274's
    departure footprint ON the hearer sets (the epoch's rolls — rng-1's
    corpus price): the first vigil (t=3299, two ticks past Maren's
    move) mints WITHOUT her — she is at the keep now, not through the
    market walls — and with the CORPORAL on the post (the rotation's
    window moved with the cascade); the later pair (t=4379) carries
    the SERGEANT back (the rotation's own rhythm). The residue is the
    ACT's, minted per event at the hearers' live positions, never
    once per run."""
    events = witness
    vigils = _of(events, "wergeld_vigil")
    assert len(vigils) == 3  # the deadband's landing pile at this window
    assert all(v.actor == "grp_old_families" for v in vigils)
    assert all(
        v.provenance["cause_intent"] == "faction_0001" for v in vigils
    )
    first = {
        "pc_01": ("the_blood_price_spoken", "partial"),
        STEWARD: ("the_blood_price_spoken", "partial"),
        CORPORAL: ("the_blood_price_spoken", "vague"),
        CROWD: ("the_blood_price_spoken", "vague"),
    }
    later = {
        "pc_01": ("the_blood_price_spoken", "partial"),
        STEWARD: ("the_blood_price_spoken", "partial"),
        SERGEANT: ("the_blood_price_spoken", "vague"),
        CROWD: ("the_blood_price_spoken", "vague"),
    }
    by_tick = {}
    for vigil in vigils:
        by_tick.setdefault(vigil.t, []).append(vigil)
    assert _records(by_tick[3299][0]) == first  # the departure's own window
    for vigil in by_tick[4379]:
        assert _records(vigil) == later


def test_the_briefing_carries_the_trade_token(
    witness: list[EventRecord],
) -> None:
    """The institutional memory consumer measured in iter-263's I2
    arm, re-measured here for the TRADE's own token: the rotation's
    briefing carries the duty corporal's stack — the coin-changed-
    hands record among the fire family — to the sergeant (one fidelity
    step down, the D-006 briefing law). The chest's commerce is now
    the watch's institutional knowledge: who bought, on the record."""
    events = witness
    transfer = next(
        e for e in _of(events, "knowledge_transfer")
        if e.actor == CORPORAL and e.target == SERGEANT
    )
    records = _records(transfer)
    assert records.get(SERGEANT) is not None
    know = {k.knows: k.fidelity for k in transfer.knowledge}
    assert know["coin_changed_hands_at_loc_malby"] == "vague"


# -- the determinism pin --------------------------------------------------------


def test_the_twin_run_is_byte_identical(tmp_path: Path) -> None:
    """INV-2 over the legs witness: the twin run is byte-identical on
    the same environment (T1's form — a determinism pin, never a
    committed golden)."""
    logs = []
    for name in ("twin_a.jsonl", "twin_b.jsonl"):
        log = tmp_path / name
        pack = load_pack(PACK_DIR)
        sim = Simulator(pack, 2, log, SCHEMA, commit="0000000")
        sim.run_playscript({
            "name": name, "seed": 2, "pack": "province_pack@0.1",
            "steps": STEPS,
        })
        sim.close()
        logs.append(log.read_bytes())
    assert logs[0] == logs[1]
