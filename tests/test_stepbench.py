"""stepbench — the §6.2 fill row (iter-275, the owner's 2026-09-27
execution order's fourth row: PRESENT / HATCH / NOTCH — the fill-list's
last embodiment row, placed last by iter-266's own risk note: two risk
layers, the highest chance of prematurely hitting a substrate gap):
the step bench's three missing links brought to live state through the
EXISTING account substrate (the iter-273 family), the gaps honestly
recorded, never routed.

The row's named elements:

- **PRESENT, LANDED**: the FIFTH kind `step` — the standing head as
  live account state, stocked on the keeper (the timbers' setting in
  the pool's hand, seeded three the working head) + the door
  `set_the_timbers` (the TIGHTENING alone armed: consume, the
  solvency gate step >= three — the FLOOR LAW in the gate's own
  arithmetic: the tightening only from the working head, the first
  rung the drought's own, never the hand's; the loosening stays
  authored — the price's recovery an authored future season, the
  freightvol law's own shape; the fourth rung never a setting, the
  rise's own committed text).
- **NOTCH, LANDED (the honest half)**: the SIXTH kind `notch` — the
  dry years' sequence in wood, stocked on the beam's hand (the tally
  staff's carrier, seeded zero — the count opens at the canonical
  present, the past sequence authored in the gloss) + the door
  `cut_the_notch` (the reckoning at the weighing day: source, the
  acceptance form the reprice precedent's own shape). THE HONEST GAP:
  the notch's lawful condition — the DRY BAND standing — is a
  TWO-SIDED band condition the closed gate vocabulary cannot express
  (account_at_least reads floors, never ceilings, never exact
  values); the band law stays authored, the gap a named candidate for
  the I0 witness's substrate-limitation inventory.
- **HATCH, HELD AS PROSE** (the verb-gate boundary, iter-266's own
  law, WORLD_AUTHORING §8): the wattle's thrower-open form — "who
  throws it, the users' own law executed at the water" — has no
  single holder, and a wattle stock would need a thrower-side stock
  on every user: the over-authoring the boundary refuses. The hatch
  stays prose; the breach's social half already lives (the run's
  claim riding the beam's talk, the committed rumor channel).

The claim packet (TEST_PLAN §9):

- Claim: the bench's PRESENT and NOTCH land as live account state
  through the existing player-scaled arm — the standing step a
  readable, gated, lawful stock with the floor law expressed in the
  gate's own arithmetic; the notch a climbing count with the weighing
  day's own record — while the two honest boundaries (the two-sided
  band condition, the thrower-open wattle) are MEASURED and recorded,
  never routed around.
- Lens(es): the carrier lens (the reading at the stair mints the LAW,
  the keeper's stock carries the PRESENT — the two surfaces meeting
  at the reader); the boundary lens (the at-least-only gate
  vocabulary; the no-single-holder wattle).
- Prism: the committed-pack census; the crafted short-cadence twin
  (macro 480) walking the tightening and the notch; the floor's
  refusal arm; the gap arm (the notch cut at the working head).
- Oracle: the event log scans (the verb events' shapes, the knowledge
  rows), the projection reads, the tale render, the golden corpus
  bytes.
- Falsifier: the tightening landing below the second rung (the floor
  law broken); the notch door reading the band (the gap denied); a
  hatch/wattle verb armed (the boundary broken); the golden T1 bytes
  shifting; the tale losing the timbers' line.
- Expected evidence: the census pins; the tightening 3→2 with the
  second hand the witness; the floor refused softly at the low band;
  the notch 0→1 with the market's witnesses; the notch FIRING at the
  working head (the gap measured, the band law prose); the corpus
  byte-identical.
- Observed evidence: CONFIRMED at the measured band (seed 42).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest boundaries recorded in the
  economy notes: the loosening a future season's row; the band
  condition the I0 inventory's named candidate; the wattle prose by
  law).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

KEEPER = "npc_weirkeeper_01"     # Ketta — the pool's hand
SECOND = "npc_secondhand_01"     # Dellan — the living line at the stair
BEAM = "npc_marketmistress_01"   # Maren — the run's hand, the staff's carrier
STAIR = "loc_weirstair"
CROWD = "npc_malby_crowd_01"
SERGEANT = "npc_sergeant_01"
WORKING_HEAD = 3                 # the long_light default — the seeded rung
CONSUME_EVENT = "account_consumed"
SOURCE_EVENT = "account_sourced"


# -- the helpers ----------------------------------------------------------------


def _twin(tmp_path: Path, name: str) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the sub-year
    law (market 40, fair 120, seasons 120)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["time"]["macro"]["cadence_ticks"] = 480
    calendar = rules["time"]["calendar"]
    calendar["market_days"]["every_ticks"] = 40
    calendar["fairs"]["every_ticks"] = 120
    calendar["seasons"]["every_ticks"] = 120
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    return target


def _run_pack(
    pack_dir: Path, tmp_path: Path, name: str, seed: int,
    steps: list[dict[str, Any]],
) -> tuple[list, Any, Simulator]:
    pack = load_pack(pack_dir)
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": steps,
    })
    _, events = read_log(log, SCHEMA)
    return events, pack, sim


# -- the census (the arming as pack data) ------------------------------------------


def test_the_armed_census() -> None:
    """The row's named elements as committed pack data: the two kinds
    (the vocabulary now six), the keeper's standing stock (the working
    head seeded), the beam's count stock (the count opening at zero),
    the two doors (the tightening's floor gate; the notch's acceptance
    form), the kind glosses + the knows rows, UNARMED by doctrine, and
    the HATCH honestly absent — no wattle verb, no hatch stock (the
    verb-gate boundary held)."""
    pack = load_pack(PACK_DIR)
    economy = pack.rules["economy"]
    # iter-275 (stepbench): the fifth and sixth kinds — the bench's own
    assert economy["accounts"] == [
        "coin", "bloom", "paper", "floodpaper", "step", "notch",
    ]
    # no flow touches the step or the notch — the no-amortization law's
    # own family (the re-setting a practitioner's act, the reckoning the
    # beam's — never a clock)
    assert not [f for f in economy["flows"] if f["kind"] in ("step", "notch")]
    keeper = next(n for n in pack.entities["npcs"] if n["id"] == KEEPER)
    assert keeper["accounts"] == {
        "coin": 2, "floodpaper": 20, "step": WORKING_HEAD,
    }
    beam = next(n for n in pack.entities["npcs"] if n["id"] == BEAM)
    assert beam["accounts"] == {"notch": 0}
    actions = {a["intent"]: a for a in pack.data["actions.json"]["actions"]}
    tighten = actions["set_the_timbers"]
    assert tighten["account"] == {"verb": "consume", "kind": "step",
                                  "amount": 1}
    assert tighten["events"] == {"success": CONSUME_EVENT}
    tests = [
        (c.get("noun"), c["test"], c.get("kind"), c.get("value"))
        for c in tighten["requires"]
    ]
    # the geography honest (the timbers at the water — the setting at
    # the stair) and THE FLOOR LAW: the gate step >= 3 — the tightening
    # only FROM the working head, the first rung the drought's own
    assert ("actor", "account_at_least", "step", WORKING_HEAD) in tests
    assert ("target", "same_location", None, None) in [
        (n, t, None, None) for n, t, _, _ in tests
    ]
    notch = actions["cut_the_notch"]
    assert notch["account"] == {"verb": "source", "kind": "notch",
                                "amount": 1}
    assert notch["events"] == {"success": SOURCE_EVENT}
    # the acceptance form (the reprice precedent): the target the beam's
    # own hand, the identity the discipline; NO band gate — the honest
    # gap (the two-sided condition inexpressible, the law prose)
    notch_tests = [
        (c.get("noun"), c["test"], c.get("kind"), c.get("value"))
        for c in notch["requires"]
    ]
    assert ("target", "field_in", None, None) in [
        (n, t, None, None) for n, t, _, _ in notch_tests
    ]
    assert not [
        t for _n, t, k, _v in notch_tests
        if t == "account_at_least" and k == "step"
    ]  # the gap: no step-reading gate exists
    # the knowledge rows: the standing re-made public, the count public
    assert tighten["knowledge"]["success"] == [{
        "who": "same_location", "except": ["actor"], "channel": "saw",
        "fidelity": "exact", "knows": "the_timbers_set",
    }]
    assert notch["knowledge"]["success"] == [{
        "who": "same_location", "except": ["actor"], "channel": "saw",
        "fidelity": "exact", "knows": "the_dry_year_notched",
    }]
    # the kind glosses — headed by the kind word (the lint's own law)
    assert pack.templates["account_kinds"]["step"] == (
        "step at the weir stair — the standing head named by the stair's "
        "wet step, the timbers' setting in the keeper's hand (three the "
        "working head, two the low band's standing, one the drought floor "
        "the drought's own)"
    )
    assert pack.templates["account_kinds"]["notch"] == (
        "notch on the tally staff — the dry years' sequence in wood, the "
        "beam's reckoning cut at the weighing day"
    )
    assert pack.templates["knows"]["the_timbers_set"] == (
        "the timbers set to the low band at the weir stair — the pool "
        "held for the crossing, the race at its trickle, the run light: "
        "the standing quarrel made arithmetic, the second step's own "
        "argument"
    )
    assert pack.templates["knows"]["the_dry_year_notched"] == (
        "the count climbing, the beam's memory of the thin season, the "
        "grounding year weighed light"
    )
    # UNARMED by doctrine: no urgency entry names either door
    urgencies = json.dumps(pack.rules.get("urgencies", {}))
    assert "set_the_timbers" not in urgencies
    assert "cut_the_notch" not in urgencies
    # THE HATCH honestly absent: no wattle verb, no hatch stock (the
    # verb-gate boundary held — the thrower-open form has no holder)
    assert not [
        a for a in pack.data["actions.json"]["actions"]
        if "hatch" in a["intent"] or "wattle" in a["intent"]
    ]
    assert "hatch" not in economy["accounts"]
    assert "wattle" not in economy["accounts"]


# -- the PRESENT leg: the tightening + the floor law --------------------------------


def test_the_tightening_lands_the_low_band(tmp_path: Path) -> None:
    """The re-setting walked once: the keeper at the stair consumes the
    working head down to the low band (3→2), the living line the
    witness (the second hand at the weirstair learning the_timbers_set
    exact), the tale carrying the timbers' line with the kind's own
    gloss — the standing quarrel made arithmetic on the reader's
    surface."""
    steps = [
        {"intent": "set_the_timbers", "actor": KEEPER, "target": STAIR},
        {"intent": "wait", "ticks": 10},
    ]
    events, pack, sim = _run_pack(
        _twin(tmp_path, "tighten"), tmp_path, "tighten.jsonl", 42, steps
    )
    settings = [
        e for e in events if e.type == CONSUME_EVENT
        and e.outcome.get("kind") == "step"
    ]
    assert len(settings) == 1
    setting = settings[0]
    assert setting.actor == KEEPER and setting.target == STAIR
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in setting.state_changes] == [
        (KEEPER, "account.step", WORKING_HEAD, WORKING_HEAD - 1),
    ]
    # the living line the witness — the inheritance's own learner
    knowers = {r.who for r in setting.knowledge}
    assert SECOND in knowers
    assert all(r.knows == "the_timbers_set" for r in setting.knowledge)
    assert sim.projection[KEEPER]["account.step"] == WORKING_HEAD - 1
    sim.close()
    tale = render_chronicle(events, pack, seed=42)
    assert (
        "Ketta is rid of 1 step at the weir stair — the standing head "
        "named by the stair's wet step, the timbers' setting in the "
        "keeper's hand (three the working head, two the low band's "
        "standing, one the drought floor the drought's own)." in tale
    )


def test_the_floor_law_refuses_below_the_low_band(tmp_path: Path) -> None:
    """The FLOOR LAW in the gate's own arithmetic: at the low band (2)
    the tightening is refused SOFTLY (the gate step >= 3 fails — the
    attempt a fact, intent_rejected, the stock untouched) — the first
    rung the drought's own, never the hand's ('never set but by a
    drought the vale survives, and never unnotched')."""
    steps = [
        {"intent": "set_the_timbers", "actor": KEEPER, "target": STAIR},
        {"intent": "set_the_timbers", "actor": KEEPER, "target": STAIR},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "floor"), tmp_path, "floor.jsonl", 42, steps
    )
    settings = [
        e for e in events if e.type == CONSUME_EVENT
        and e.outcome.get("kind") == "step"
    ]
    assert len(settings) == 1  # the first lands 3→2
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "set_the_timbers"
    ]
    assert len(rejected) == 1  # the second refused softly at the floor
    assert rejected[0].outcome["failed_test"] == "actor.account_at_least"
    assert sim.projection[KEEPER]["account.step"] == WORKING_HEAD - 1
    sim.close()


# -- the NOTCH leg: the reckoning + the honest gap -----------------------------------


def test_the_notch_cut_at_the_weighing_day(tmp_path: Path) -> None:
    """The beam's reckoning walked once: the mistress accepts her own
    count (the reprice precedent's identity form — the actor and the
    target one hand), the tally staff's notch climbing 0→1, the
    market's witnesses learning the_dry_year_notched exact, the tale
    carrying the reckoning's line with the kind's own gloss."""
    steps = [
        {"intent": "cut_the_notch", "actor": BEAM, "target": BEAM},
        {"intent": "wait", "ticks": 10},
    ]
    events, pack, sim = _run_pack(
        _twin(tmp_path, "notch"), tmp_path, "notch.jsonl", 42, steps
    )
    cuts = [
        e for e in events if e.type == SOURCE_EVENT
        and e.outcome.get("kind") == "notch"
    ]
    assert len(cuts) == 1
    cut = cuts[0]
    assert cut.actor == BEAM and cut.target == BEAM
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in cut.state_changes] == [
        (BEAM, "account.notch", 0, 1),
    ]
    knowers = {r.who for r in cut.knowledge}
    assert CROWD in knowers and SERGEANT in knowers
    assert all(r.knows == "the_dry_year_notched" for r in cut.knowledge)
    assert sim.projection[BEAM]["account.notch"] == 1
    sim.close()
    tale = render_chronicle(events, pack, seed=42)
    # iter-281 (the W6 gap (b) routing's family consequence): the notch
    # line gains the KNOWS TAIL — the witnessed row riding the account
    # line through rs-1's boundary; the gloss re-authored to COMPLEMENT
    # the kind's own gloss (what the notching DOES, never a restatement)
    assert (
        "Maren comes by 1 notch on the tally staff — the dry years' "
        "sequence in wood, the beam's reckoning cut at the weighing day "
        "at the year's reckoning — the count climbing, the beam's memory "
        "of the thin season, the grounding year weighed light." in tale
    )


def test_the_band_gap_measured(tmp_path: Path) -> None:
    """The row's honest gap, MEASURED never denied: the notch's lawful
    condition — the dry band standing (the second step) — cannot ride
    the door (the closed gate vocabulary reads floors, never ceilings,
    never exact values); the witness drives the notch cut at the
    WORKING HEAD (the step still three) and the door FIRES — the band
    law stays prose, the first missing causal leg of the §6.2 row, a
    named candidate for the I0 witness's substrate-limitation
    inventory."""
    steps = [
        # the notch cut with the timbers STILL at the working head —
        # the lawful world would refuse (a dry year needs the low band)
        {"intent": "cut_the_notch", "actor": BEAM, "target": BEAM},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "gap"), tmp_path, "gap.jsonl", 42, steps
    )
    cuts = [
        e for e in events if e.type == SOURCE_EVENT
        and e.outcome.get("kind") == "notch"
    ]
    # the door FIRES at the working head — the gap measured: the gate
    # vocabulary cannot express the two-sided band condition
    assert len(cuts) == 1
    assert sim.projection[KEEPER]["account.step"] == WORKING_HEAD
    assert sim.projection[BEAM]["account.notch"] == 1
    sim.close()


# -- the corpus laws ------------------------------------------------------------------


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: neither door ever fires in the
    day-scale corpus scripts and both stocks seed silently (the
    projection's own floor, never an event) — the golden T1 fixture
    regenerates byte-identically under the armed pack."""
    golden = (
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
    ).read_bytes()
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_smoke.json"
    )
    pack = load_pack(PACK_DIR)
    log = tmp_path / "smoke.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    assert log.read_bytes() == golden


def test_the_twin_is_deterministic(tmp_path: Path) -> None:
    """The T1 law at the row's own band: same seed + steps + pack, the
    bench's run byte-identical."""
    steps = [
        {"intent": "set_the_timbers", "actor": KEEPER, "target": STAIR},
        {"intent": "cut_the_notch", "actor": BEAM, "target": BEAM},
        {"intent": "wait", "ticks": 10},
    ]
    for name in ("det_a", "det_b"):
        _run_pack(
            _twin(tmp_path, name), tmp_path, f"{name}.jsonl", 42, steps
        )
    assert (tmp_path / "det_a.jsonl").read_bytes() == (
        tmp_path / "det_b.jsonl").read_bytes()
