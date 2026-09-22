"""charcoalpaper — the charcoal debt's STANDING STATE (iter-189, the
owner's W5-decomposition call, finding 2: the standing debt is an
UPSTREAM WORLD GAP, never a renderer issue — debt-1 gave the accounts
+ the flows, campaccount the arithmetic, freightvol the volume; this
row closes the standing state that stayed authored): the paper
SIXTEEN as canonical residue state over the res-1 substrate, pure pack
data, zero core (the KI#87 precedent class), NO generic economy
subsystem — one specific debt brought to its full lifecycle.

The row's named elements: the OUTSTANDING PRINCIPAL as live account
state (a third kind `paper`, stocked on the master — the stock's
entity IS the seat: the debt rides whoever masters the burn); the
HOLDER/CARRIER/SEAT bindings (the guild's chest the coin's destination
at the fall; the tally-stick the badge on the same hand; the secret
the counter-record); the lifecycle doors through the account
resolver's player-scaled arm — the province pack's FIRST arming:
`reckon_paper` (the FALL, the covered-fund gate), `render_fund` (the
COLLECTION, the geography gate at the chest), `pass_the_seat` (the
SUCCESSION, the receiving-stock gate). The unlapseable reading is
arithmetic now: the accounts never decay, so once named, stays named
until a canon event moves the stock.

The claim packet (TEST_PLAN §9):

- Claim: the charcoal debt's standing is canonical residue state —
  the outstanding visible in the projection beside its fund, the
  flows never amortizing it, and each lifecycle transition (fall,
  collection, succession) a lawful canon event with exact shapes.
- Lens(es): the residue-lifecycle lens (each rung's removal changes
  reachable futures — the frozen-force counterfactual the door's own
  removal); the boundary lens (the renegotiation and the tally's
  handing-over stay un-armed, recorded as residues, never smuggled).
- Prism: the committed-pack census; the crafted short-cadence twin
  (macro 480) walking the fund's climb to the fifth reckoning; the
  crafted successor pack (the seat's receiving end declared); the
  committed band's soft-refusal arms.
- Oracle: the event log scans (the verb events' outcome/state_changes/
  knowledge shapes, the cause chain), the projection reads, the tale
  render, the golden corpus bytes.
- Falsifier: a flow touching the paper (amortization smuggled in);
  the fall firing against an uncovered fund; the succession landing
  on a stockless target (a loud crash, not a soft refusal); the
  golden T1 bytes shifting; the tale losing the fall's line.
- Expected evidence: the census pins; the twin's paper unchanged at
  16 through the crossings while the fund climbs 3→18; the fall
  refused at 15, landing at 18 (paper 16→0, the market's witnesses
  holding the_paper_fell); the collection walking 16 coin to the
  chest (the fund 2, the chest 76); the succession walking the paper
  to the successor while the tally-stick stays (the recognition's
  un-armed half); the corpus byte-identical.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  twin + the crafted successor).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded in the economy
  notes: the renegotiation — the guild's re-pricing, the factor
  gateless, no committed surface; the tally's handing-over — the
  crews' recognition, no committed surface; the over-payment state —
  the reversed door order, lawful, never scripted; the re-weigh's
  SALE — the heap's bloom drain, still un-armed, the withhold's own
  future row).
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
TALLY = "camp_tally_01"
MARKET = "npc_marketmistress_01"
SUCCESSOR = "npc_burnhand_01"  # the crafted twin's receiving seat
PAPER = 16  # the starved winter's stores — the outstanding principal
FALL_EVENT = "account_consumed"
WALK_EVENT = "account_transferred"


# -- the helpers ----------------------------------------------------------------


def _twin(tmp_path: Path, name: str) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the sub-year
    law (market 40, fair 120, seasons 120) — the fund's climb to the
    fifth reckoning measured in minutes, not megaticks."""
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


def _successor_pack(tmp_path: Path, name: str) -> Path:
    """The crafted successor twin: the committed pack plus ONE receiving
    seat — a burnhand at the crofts declaring a paper stock of zero
    (the door's receiving end; the crews' recognition has no committed
    surface, so the test mints the successor the way a future row
    would)."""
    target = _twin(tmp_path, name)
    entities = json.loads(
        (target / "entities.json").read_text(encoding="utf-8")
    )
    entities["npcs"].append({
        "id": SUCCESSOR,
        "name": "the burnhand",
        "role": "the crews' own at the stacks",
        "position": CROFTS,
        "status": {"fatigue": 20, "intoxication": 0, "fear": 0, "injury": 0},
        "relations": {"reputation": 50, "trust": 50, "fear": 0},
        "pair_relations": [{"with": MASTER, "trust": 40}],
        "knowledge": [],
        "mood": "steady",
        "goal": "keep the count honest at the stacks",
        "accounts": {"paper": 0},
        "notes": (
            "the crafted receiving seat (charcoalpaper's test twin — the "
            "successor the camp would hold at the burn: the crews' "
            "recognition minted as pack data for the succession's proof, "
            "never a committed entity; the pair relation the recognition's "
            "own proxy — the master's trusted hand)"
        ),
    })
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


# -- the census (the standing state as pack data) --------------------------------


def test_the_armed_census() -> None:
    """The row's named elements as committed pack data: the third
    account kind (paper — the outstanding's own measure), the master's
    standing stock beside the fund (the debt's two numbers at one
    read), the three lifecycle doors (the account resolver's
    player-scaled arm armed for the first time in this pack), the two
    verb lines, the story-critical listing (the lifecycle's beats are
    the tale's), the budget's honest re-declare."""
    pack = load_pack(PACK_DIR)
    economy = pack.rules["economy"]
    assert economy["accounts"] == ["coin", "bloom", "paper"]
    # no flow touches the paper — the no-amortization law is structural
    assert not [f for f in economy["flows"] if f["kind"] == "paper"]
    master = next(n for n in pack.entities["npcs"] if n["id"] == MASTER)
    assert master["accounts"] == {"coin": 3, "paper": PAPER}
    actions = {a["intent"]: a for a in pack.data["actions.json"]["actions"]}
    fall = actions["reckon_paper"]
    assert fall["resolver"] == "account"
    assert fall["account"] == {"verb": "consume", "kind": "paper",
                               "amount": PAPER}
    assert fall["events"] == {"success": FALL_EVENT}
    assert fall["requires"] == [
        {"noun": "actor", "test": "account_at_least", "kind": "paper",
         "value": PAPER},
        {"noun": "actor", "test": "account_at_least", "kind": "coin",
         "value": PAPER},  # the covered-fund gate — the fall's own law
    ]
    walk = actions["render_fund"]
    assert walk["account"] == {"verb": "transfer", "kind": "coin",
                               "amount": PAPER}
    assert walk["events"] == {"success": WALK_EVENT}
    tests = [(c["noun"], c["test"], c.get("kind"), c.get("value"))
             for c in walk["requires"]]
    assert ("target", "field_in", None, None) in [
        (n, t, None, None) for n, t, _, _ in tests
    ]  # the chest pinned
    assert ("actor", "account_at_least", "coin", PAPER) in tests
    seat = actions["pass_the_seat"]
    assert seat["account"] == {"verb": "transfer", "kind": "paper",
                               "amount": PAPER}
    seat_tests = [(c["noun"], c["test"], c.get("kind"), c.get("value"))
                  for c in seat["requires"]]
    assert ("actor", "account_at_least", "paper", PAPER) in seat_tests
    assert ("target", "account_at_least", "paper", 0) in seat_tests
    # the verb lines + the story listing + the budget's re-declare
    assert pack.templates["events"][WALK_EVENT] == (
        "{actor} passes {amount} {kind} to {target}."
    )
    assert pack.templates["events"][FALL_EVENT] == (
        "{actor} is rid of {amount} {kind}."
    )
    for event_type in (WALK_EVENT, FALL_EVENT):
        assert event_type in pack.rules["importance"]["story_critical_events"]
    assert pack.rules["budget"]["templates"]["max"] == 70


def test_the_standing_state_and_its_bindings() -> None:
    """The seat's three surfaces at one read: the paper stock (the
    outstanding, the stock's entity the seat), the tally-stick (the
    badge, carried by the same hand), the secret (the counter-record,
    registered over the same man) — and the fund climbing beside the
    paper (the fall's own gate reading live state)."""
    pack = load_pack(PACK_DIR)
    from core.fold import initial_projection

    projection = initial_projection(pack.entities)
    assert projection[MASTER]["account.paper"] == PAPER
    assert projection[MASTER]["account.coin"] == 3
    assert projection[CROFTS]["account.bloom"] == 4  # freightvol's heap
    master = next(n for n in pack.entities["npcs"] if n["id"] == MASTER)
    assert master["carries"] == [TALLY]
    assert pack.rules["secrets"]["tokens"]["the_camps_word"] == {
        "subject": MASTER, "type": "debt", "expires_ticks": 129600,
    }
    # the holder's home: the chest's coin — the fall's destination
    assert projection[CHEST]["account.coin"] == 40


# -- the no-amortization law + the covered-fund gate ------------------------------


def test_the_flows_never_amortize_the_paper(tmp_path: Path) -> None:
    """The standing service is the paper's WEIGHT, never its fall: four
    crossings climb the fund 3→15 while the paper stands UNCHANGED at
    16 — the flows are coin and bloom, never paper (the structural
    census made live state), and at the fourth reckoning the fund does
    not yet cover the paper (15 < 16: the fifth is the crossing)."""
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "armed.jsonl", 42,
        # the wait's horizon overruns to the next beat boundary —
        # 1600 lands the fourth crossing (t=1920) and no more
        [{"intent": "wait", "ticks": 1600}],
    )
    assert not [e for e in events if e.type in (FALL_EVENT, WALK_EVENT)]
    assert sim.projection[MASTER]["account.coin"] == 15  # 3 + 3x4
    assert sim.projection[MASTER]["account.paper"] == PAPER
    sim.close()


def test_the_fall_requires_the_covered_fund(tmp_path: Path) -> None:
    """The soft door at the committed band: the fund 3 does not cover
    the paper 16 — the reckoning is REFUSED softly (the attempt a
    fact, intent_rejected), the paper standing, the heap untouched."""
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "early"), tmp_path, "early.jsonl", 42,
        [{"intent": "reckon_paper", "actor": MASTER},
         {"intent": "wait", "ticks": 10}],
    )
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "reckon_paper"
    ]
    assert len(rejected) == 1
    assert sim.projection[MASTER]["account.paper"] == PAPER
    assert sim.projection[MASTER]["account.coin"] == 3
    sim.close()


# -- the reckoning: the fall, then the collection ---------------------------------


def test_the_reckoning_at_the_fifth_crossing(tmp_path: Path) -> None:
    """The clearance walked once through the canon door: the master at
    the beam when the fifth reckoning covers the paper (fund 18) — the
    FALL (account_consumed: the paper 16→0, the covered-fund gate
    passed, the market's witnesses holding the_paper_fell), then the
    COLLECTION (account_transferred: 16 coin master→chest, the fund 2,
    the chest 76), the walk's cause chained to the fall, and the tale
    carrying both lines."""
    steps = [
        # the master walks to the beam's town (the honest geography:
        # the fund renders at the chest) — the crossings fire en route
        {"intent": "move", "actor": MASTER, "target": "loc_keep"},
        {"intent": "move", "actor": MASTER, "target": CHEST},
        # past the fifth crossing (t=2400): the fund 3 + 3x5 = 18
        {"intent": "wait", "ticks": 1700},
        # the fall, then the collection — the scene's lawful order
        {"intent": "reckon_paper", "actor": MASTER},
        {"intent": "render_fund", "actor": MASTER, "target": CHEST},
        {"intent": "wait", "ticks": 10},
    ]
    events, pack, sim = _run_pack(
        _twin(tmp_path, "reckoning"), tmp_path, "reckoning.jsonl", 42, steps
    )
    falls = [e for e in events if e.type == FALL_EVENT]
    walks = [e for e in events if e.type == WALK_EVENT]
    assert len(falls) == 1 and len(walks) == 1
    fall, walk = falls[0], walks[0]
    # the fall's shapes: the master's paper consumed, the gate passed
    # (the outcome carries the resolver's check dict + the loop's
    # duration stamp beside the verb's own keys)
    assert fall.actor == MASTER and fall.target is None
    assert fall.outcome["kind"] == "paper"
    assert fall.outcome["amount"] == PAPER
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in fall.state_changes] == [
        (MASTER, "account.paper", PAPER, 0),
    ]
    # the market's witnesses hold the fall — the vale's word
    knowers = {r.who for r in fall.knowledge}
    assert MARKET in knowers
    assert all(r.knows == "the_paper_fell" for r in fall.knowledge)
    # the collection's shapes: 16 coin to the chest, the cause the fall
    assert walk.actor == MASTER and walk.target == CHEST
    assert walk.outcome["kind"] == "coin"
    assert walk.outcome["amount"] == PAPER
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in walk.state_changes] == [
        (MASTER, "account.coin", 18, 2),
        (CHEST, "account.coin", 60, 76),
    ]
    assert walk.cause == fall.id  # the chronological chain
    # the terminus: the paper fallen, the fund spent, the chest paid
    assert sim.projection[MASTER]["account.paper"] == 0
    assert sim.projection[MASTER]["account.coin"] == 2
    assert sim.projection[CHEST]["account.coin"] == 76
    sim.close()
    # the tale carries the reckoning's two lines — rs-2 (iter-191): the
    # fall's line carries the account-kind gloss (the debt's frame, the
    # W5 rendering fix's own surface); the coin line stays dry (the
    # unglossed kind's fallback law)
    tale = render_chronicle(events, pack, seed=42)
    assert (
        "Garrick is rid of 16 paper owed to the guild's chest at Malby "
        "since the starved winter." in tale
    )
    assert "Garrick passes 16 coin to Malby, the market town." in tale


# -- the succession: the seat, never the blood ------------------------------------


def test_the_succession_walks_the_paper_to_the_seat(tmp_path: Path) -> None:
    """The transfer door walked once: the paper walks to the successor
    (the receiving stock declared — the seat's own receiving end), the
    tally-stick STAYS with the old master (the recognition's un-armed
    half — the badge follows the camp's word, never the door), the
    successor holding the fall's own gate now (paper 16 on the new
    seat), and the stockless target refused SOFTLY (the value-0
    existence gate, the KI#15 family's door shape)."""
    steps = [
        # a stockless target first: the market mistress declares no paper
        {"intent": "pass_the_seat", "actor": MASTER, "target": MARKET},
        # the handing-over at the stacks: the successor present
        {"intent": "pass_the_seat", "actor": MASTER, "target": SUCCESSOR},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _successor_pack(tmp_path, "seat"), tmp_path, "seat.jsonl", 42, steps
    )
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "pass_the_seat"
    ]
    assert len(rejected) == 1  # the stockless target, refused softly
    passes = [e for e in events if e.type == WALK_EVENT
              and e.outcome.get("kind") == "paper"]
    assert len(passes) == 1
    seat = passes[0]
    assert seat.actor == MASTER and seat.target == SUCCESSOR
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in seat.state_changes] == [
        (MASTER, "account.paper", PAPER, 0),
        (SUCCESSOR, "account.paper", 0, PAPER),
    ]
    assert any(r.knows == "the_seat_passed" for r in seat.knowledge)
    # the terminus: the debt rides the new seat, the badge stays
    assert sim.projection[MASTER]["account.paper"] == 0
    assert sim.projection[SUCCESSOR]["account.paper"] == PAPER
    assert sim.projection[MASTER].get("carrier") is None or (
        sim.projection[TALLY].get("carrier") == MASTER
    )
    assert sim.projection[TALLY]["carrier"] == MASTER  # the un-armed half
    sim.close()


# -- the corpus laws --------------------------------------------------------------


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the doors never fire in the day-scale
    corpus scripts and the paper stock seeds silently (the projection's
    own floor, never an event) — the golden T1 fixture regenerates
    byte-identically under the armed pack."""
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
    standing state's run byte-identical."""
    steps = [{"intent": "wait", "ticks": 2000}]
    for name in ("det_a", "det_b"):
        _run_pack(
            _twin(tmp_path, name), tmp_path, f"{name}.jsonl", 42, steps
        )
    assert (tmp_path / "det_a.jsonl").read_bytes() == (
        tmp_path / "det_b.jsonl").read_bytes()
