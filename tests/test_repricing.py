"""repricing — the paper's RENEGOTIATION (iter-271, the §6.4 fill row's
first landing: FACTOR NEGOTIATION + the honest residues SALE and TAG
TRANSFER, the W5 disposition iter-266's fill-list front row): the
guild's re-pricing of the charcoal paper armed as live arithmetic over
the account resolver's player-scaled arm — pure pack data, zero core,
the charcoalpaper precedent family's fourth door.

The row's named elements: the SQUEEZE (the source verb minting two
paper onto the seat — the withheld margin's own number, the coupled
liabilities' answer: the camp holds two loads off the beam, the guild
prices two paper onto the debt); the STANDING-TERMS GATE (paper at
least sixteen on the actor — the renegotiation only against the
standing debt, a fallen paper having no terms to re-price); the
RECEIVING-STOCK GATE (the target declaring a paper stock, the
pass_the_seat form); the KNOWLEDGE (the re-priced terms public — the
witnesses learning the_paper_repriced, the squeeze legible in the
same breath as the debt it lands on). The factor stays gateless as an
ENTITY (the beat rides the seat's acceptance-door, the guild's agency
carried by the terms themselves — the honest boundary, recorded).

The row's honest residues (the fork recorded for the owner, never
smuggled): the re-weigh's SALE — the heap's drain — hits the account
resolver's ACTOR-SIDE grammar wall (the transfer's from-side is
always the intent actor; the heap's ledger stocks loc_crofts, a
location, and a location can only ever be a TO-side — the drain door
cannot be authored as pure pack data over the closed verb set); the
TAG TRANSFER (the tally-stick's handing-over) rides the existing
drop+take pair mechanically (the carrier-availability law's own
family — the drop lays the badge down uncarried, the take re-carries
it) with the crews' recognition mint still no committed surface
(iter-185's law unchanged).

The claim packet (TEST_PLAN §9):

- Claim: the renegotiation is live account arithmetic — the squeeze a
  lawful canon event with exact shapes, gated by the standing terms,
  public to the witnesses, the debt compounding by design.
- Lens(es): the residue-lifecycle lens (the re-pricing rung between
  the standing residue and the cleared/inheritable futures); the
  boundary lens (the sale's grammar wall + the tag's verb-gate
  boundary recorded as residues, never smuggled doors).
- Prism: the committed-pack census; the crafted short-cadence twin
  (macro 480); the crafted fallen-world twin (the paper at zero);
  the committed band's soft-refusal arms; the golden corpus.
- Oracle: the event log scans (the verb event's outcome/
  state_changes/knowledge shapes), the projection reads, the tale
  render, the golden corpus bytes.
- Falsifier: the squeeze firing without the standing terms; a
  stockless target crashing loud (never refusing softly); the golden
  T1 bytes shifting; the tale losing the squeeze's line.
- Expected evidence: the census pins; the twin's paper climbing
  16→18→20 across two squeezes with the witnesses holding
  the_paper_repriced; the fallen world refused softly; the stockless
  target refused softly; the corpus byte-identical.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  twin + the crafted fallen world).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded in the action
  notes + ANCHOR_REGION §6.4: the sale's actor-side grammar wall —
  the owner's fork between the price-door-with-residue, the heap's
  re-seating, and a location-side drain verb; the tag's recognition
  mint — a future row's own call).
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

MASTER = "npc_smelter_01"
CHEST = "loc_malby"
CROFTS = "loc_crofts"
MARKET = "npc_marketmistress_01"
PAPER = 16  # the starved winter's stores — the standing terms
MARGIN = 2  # the withheld margin's own number — the squeeze's size
SOURCE_EVENT = "account_sourced"


# -- the helpers ----------------------------------------------------------------


def _twin(tmp_path: Path, name: str) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the sub-year
    law (market 40, fair 120, seasons 120) — the charcoalpaper test's
    own shape, the fund's climb measured in minutes, not megaticks."""
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


def _fallen_world(tmp_path: Path, name: str) -> Path:
    """The crafted fallen-world twin: the committed twin with the
    master's paper at ZERO — the world after the fall, no standing
    terms left to re-price (the door's own law measured at its
    refused edge)."""
    target = _twin(tmp_path, name)
    entities = json.loads(
        (target / "entities.json").read_text(encoding="utf-8")
    )
    master = next(n for n in entities["npcs"] if n["id"] == MASTER)
    master["accounts"] = {"coin": master["accounts"]["coin"], "paper": 0}
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8"
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


# -- the census (the arming as pack data) ---------------------------------------


def test_the_armed_census() -> None:
    """The row's named elements as committed pack data: the fourth
    account door (the renegotiation — the source verb, the squeeze's
    own size the withheld margin's number), the standing-terms gate on
    the actor, the receiving-stock gate on the target (the
    pass_the_seat form), the knowledge row (the re-priced terms
    public), the knows gloss — and UNARMED by doctrine (no urgency
    entry, no faction door: the census's UNREALIZED band until a
    witness exercises it)."""
    pack = load_pack(PACK_DIR)
    actions = {a["intent"]: a for a in pack.data["actions.json"]["actions"]}
    squeeze = actions["reprice_paper"]
    assert squeeze["resolver"] == "account"
    assert squeeze["account"] == {"verb": "source", "kind": "paper",
                                  "amount": MARGIN}
    assert squeeze["events"] == {"success": SOURCE_EVENT}
    tests = [(c["noun"], c["test"], c.get("kind"), c.get("value"))
             for c in squeeze["requires"]]
    # the standing-terms gate — the renegotiation only against the
    # standing sixteen (a fallen paper has no terms to re-price)
    assert ("actor", "account_at_least", "paper", PAPER) in tests
    # the receiving-stock gate — the target declares a paper stock
    assert ("target", "account_at_least", "paper", 0) in tests
    assert ("target", "kind", None, None) in [
        (n, t, None, None) for n, t, _, _ in tests
    ]
    # the knowledge row: the witnesses learn the re-priced terms
    block = squeeze["knowledge"]["success"]
    assert len(block) == 1
    assert block[0]["who"] == "same_location"
    assert block[0]["except"] == ["actor"]
    assert block[0]["knows"] == "the_paper_repriced"
    # the knows gloss rides rs-1's one table (the squeeze's own prose —
    # iter-281: re-authored as the account line's KNOWS TAIL, the W6
    # gap (b) routing: the guild's agency + the answer-to-withhold +
    # the standing terms + the climb, one row every consumer)
    assert pack.templates["knows"]["the_paper_repriced"] == (
        "the guild's squeeze answering the withhold: the loads kept off "
        "the weighbeam priced onto the standing terms, the debt climbing "
        "while the bloom stays unweighed"
    )
    # the source event is already story-critical (tune-1's law — the
    # reckoning is a story beat of this pack; the squeeze's line rides
    # the same listing, no importance change owed)
    assert SOURCE_EVENT in pack.rules["importance"]["story_critical_events"]
    # UNARMED by doctrine: no urgency entry names the door, no hook
    # seeds it — the autonomous runtime never fires it
    urgencies = json.dumps(pack.rules.get("urgencies", {}))
    assert "reprice_paper" not in urgencies
    hooks_blob = json.dumps(pack.rules.get("director", {}))
    assert "reprice_paper" not in hooks_blob


# -- the squeeze: the terms re-priced on the seat --------------------------------


def test_the_squeeze_lands_on_the_standing_terms(tmp_path: Path) -> None:
    """The renegotiation walked once through the canon door: the master
    at the beam's town with the standing terms — the SQUEEZE
    (account_sourced: the paper 16→18, the outcome carrying the verb's
    own keys, the market's witnesses holding the_paper_repriced), the
    debt compounding on the repeat (18→20 — the coupled liabilities'
    own escalation, unchecked by design), and the tale carrying the
    squeeze's line with the kind's own gloss (the debt's frame, the
    starved winter's anchor riding the growth)."""
    steps = [
        # the master walks to the beam's town (the tale's own staging;
        # the door's law is the standing terms, the geography staging)
        {"intent": "move", "actor": MASTER, "target": "loc_keep"},
        {"intent": "move", "actor": MASTER, "target": CHEST},
        # the squeeze, then the repeat — the compounding measured
        {"intent": "reprice_paper", "actor": MASTER, "target": MASTER},
        {"intent": "reprice_paper", "actor": MASTER, "target": MASTER},
        {"intent": "wait", "ticks": 10},
    ]
    events, pack, sim = _run_pack(
        _twin(tmp_path, "squeeze"), tmp_path, "squeeze.jsonl", 42, steps
    )
    squeezes = [e for e in events if e.type == SOURCE_EVENT
                and e.outcome.get("kind") == "paper"]
    assert len(squeezes) == 2
    first, second = squeezes
    # the source's shapes: the master's paper minted, the verb's keys
    for e in (first, second):
        assert e.actor == MASTER and e.target == MASTER
        assert e.outcome["kind"] == "paper"
        assert e.outcome["amount"] == MARGIN
        assert all(r.knows == "the_paper_repriced" for r in e.knowledge)
        knowers = {r.who for r in e.knowledge}
        assert MARKET in knowers  # the market's own people at the beam
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in first.state_changes] == [
        (MASTER, "account.paper", PAPER, PAPER + MARGIN),
    ]
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in second.state_changes] == [
        (MASTER, "account.paper", PAPER + MARGIN, PAPER + 2 * MARGIN),
    ]
    # the compounding terminus: the terms re-priced twice, the fund
    # untouched by the squeeze itself (the crossings en route climb
    # the fund at their own law — the squeeze prices paper, never coin)
    crossings = [
        e for e in events if e.type == SOURCE_EVENT
        and e.outcome.get("flow") == "the_bloom_nets"
    ]
    assert sim.projection[MASTER]["account.paper"] == PAPER + 2 * MARGIN
    assert sim.projection[MASTER]["account.coin"] == 3 + 3 * len(crossings)
    sim.close()
    # the tale carries the squeeze's line — the kind's own gloss riding
    # the growth (the starved winter's anchor on the climbed debt), and
    # iter-281 (the W6 gap (b) routing): the KNOWS TAIL — the event's
    # own witnessed row riding the same line through rs-1's boundary,
    # the guild's agency and the standing terms in the reader's material
    tale = render_chronicle(events, pack, seed=42)
    assert (
        "Garrick comes by 2 paper owed to the guild's chest at Malby "
        "since the starved winter at the year's reckoning — the guild's "
        "squeeze answering the withhold: the loads kept off the weighbeam "
        "priced onto the standing terms, the debt climbing while the "
        "bloom stays unweighed." in tale
    )


# -- the standing-terms gate + the receiving-stock gate ---------------------------


def test_the_fallen_world_refuses_softly(tmp_path: Path) -> None:
    """The door's own law at its refused edge: the paper at ZERO (the
    world after the fall) has no terms to re-price — the squeeze is
    REFUSED softly (the attempt a fact, intent_rejected), the paper
    standing at zero, nothing minted."""
    steps = [
        {"intent": "reprice_paper", "actor": MASTER, "target": MASTER},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _fallen_world(tmp_path, "fallen"), tmp_path, "fallen.jsonl", 42,
        steps,
    )
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "reprice_paper"
    ]
    assert len(rejected) == 1
    assert not [
        e for e in events if e.type == SOURCE_EVENT
        and e.outcome.get("kind") == "paper"
    ]
    assert sim.projection[MASTER]["account.paper"] == 0
    sim.close()


def test_the_stockless_target_refuses_softly(tmp_path: Path) -> None:
    """The receiving-stock gate (the pass_the_seat form): the market
    mistress declares no paper stock — the re-pricing aimed at her is
    REFUSED softly (the value-0 existence gate, the KI#15 family's
    door shape), the master's terms untouched."""
    steps = [
        {"intent": "reprice_paper", "actor": MASTER, "target": MARKET},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "stockless"), tmp_path, "stockless.jsonl", 42,
        steps,
    )
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "reprice_paper"
    ]
    assert len(rejected) == 1
    assert sim.projection[MASTER]["account.paper"] == PAPER
    sim.close()


# -- the corpus laws --------------------------------------------------------------


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the door never fires in the day-scale
    corpus scripts (unarmed by doctrine — no urgency entry, no hook)
    — the golden T1 fixture regenerates byte-identically under the
    armed pack."""
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
    squeeze's run byte-identical."""
    steps = [
        {"intent": "move", "actor": MASTER, "target": "loc_keep"},
        {"intent": "move", "actor": MASTER, "target": CHEST},
        {"intent": "reprice_paper", "actor": MASTER, "target": MASTER},
        {"intent": "wait", "ticks": 10},
    ]
    for name in ("det_a", "det_b"):
        _run_pack(
            _twin(tmp_path, name), tmp_path, f"{name}.jsonl", 42, steps
        )
    assert (tmp_path / "det_a.jsonl").read_bytes() == (
        tmp_path / "det_b.jsonl").read_bytes()
