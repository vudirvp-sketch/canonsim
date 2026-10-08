"""settlement — the §6.4 SALE landed through the GENERALIZED account
transaction (iter-273, the owner's synthesis decision over the
iter-271 fork: never the price-door-with-residue (a), never the heap's
re-seating (b — rejected by the record), never a location-side drain
verb (c); the fork dissolved by extending the generic substrate's
grammar, not by a per-case door): the FOURTH verb `settle` — a
multi-leg transaction over EXPLICIT owners through the same canon
door, the initiator no longer implicitly the owner of every resource
consumed.

The row's named elements: the account block's LEGS form (each leg its
own from/to/kind/amount — the nouns actor/target or explicit entity
ids declaring the stock, the flow-endpoint law's own shape); the
per-leg solvency gates (the account_at_least HOLDER form for explicit
ids, the noun vocabulary closed); ONE atomic `account_settled` event
per transaction (one net state change per touched account); the §6.4
arming `sell_bloom` — the withhold's release: one load walked to the
beam's receiving stock for three coin the load banked at the crofts'
own ledger (the rs-10 anchor's site, the heap never re-seated).

The claim packet (TEST_PLAN §9):

- Claim: the actor-side grammar wall was a genuine substrate limit
  (measured below — the closed verbs' from-side is always the intent
  actor and actors are npcs only, so a location's stock could never be
  a from-side), and the settle verb removes that CLASS of limit — the
  same mechanism expressing the sale, the buyer-initiated purchase and
  every future toll/wage/withdrawal shape, with no second transaction
  engine (the intent door, the resolver registry, the commit gate and
  the fold all unchanged in shape).
- Lens(es): the grammar lens (the wall measured, then the same
  transaction the wall refused, landed); the class lens (the crafted
  buyer's purchase — the owner's own example — over the same verb);
  the boundary lens (the lint's closed vocabularies, the corpus's
  zero price).
- Prism: the committed-pack census; the crafted short-cadence twin
  (macro 480) walking the master to the beam; the pre-positioned
  refusal twins; the crafted wall probe (a transfer door over the
  heap); the crafted buyer's door.
- Oracle: the event log scans (the settle event's legs/state_changes/
  knowledge shapes), the projection reads, the tale render, the
  golden corpus bytes.
- Falsifier: the heap drained by any closed-verb door (the wall
  unmeasured); the settle event split across events (atomicity lost);
  a leg landing on an undeclared stock; an ungated leg reaching the
  commit gate; the golden T1 bytes shifting; the tale losing the
  settle line.
- Expected evidence: the census pins; the wall probe refused at the
  ACTOR gate while the heap stands; the sale's ONE event with four
  net changes and the beam's witnesses; the compounding heap
  6→5→4→3 with the ledger climbing 0→3→6→9; the soft refusals naming
  the holders; the buyer's purchase one atomic event; the corpus
  byte-identical.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  twin + the crafted arms).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded in the economy
  notes: the withdrawal from the camp's ledger to the master's fund a
  future row's own door; the price stays authored — three the load,
  never a derived formula).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.intent import RunnerError
from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

MASTER = "npc_smelter_01"
PC = "pc_01"
CHEST = "loc_malby"
CROFTS = "loc_crofts"
MARKET = "npc_marketmistress_01"
CROWD = "npc_malby_crowd_01"
LOAD = 1    # one load per fire — the compounding law
PRICE = 3   # three coin the load — the gross nine's own arithmetic
SETTLE_EVENT = "account_settled"


# -- the helpers ----------------------------------------------------------------


def _twin(tmp_path: Path, name: str, mutate=None) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the sub-year
    law (market 40, fair 120, seasons 120) — the withhold's release
    measured in minutes, not megaticks. `mutate`, when given, receives
    the four-file data dict BEFORE the write+load (the crafted arms'
    injection point)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    data = {
        fname: json.loads((target / f"{fname}.json").read_text(encoding="utf-8"))
        for fname in ("actions", "entities", "rules", "templates")
    }

    def _shrink(data: dict) -> None:
        rules = data["rules"]
        rules["time"]["macro"]["cadence_ticks"] = 480
        calendar = rules["time"]["calendar"]
        calendar["market_days"]["every_ticks"] = 40
        calendar["fairs"]["every_ticks"] = 120
        calendar["seasons"]["every_ticks"] = 120

    _shrink(data)
    if mutate is not None:
        mutate(data)
    for fname, payload in data.items():
        (target / f"{fname}.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
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


def _to_beam(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The master's walk to the beam (the honest geography: the sale at
    the beam, the render_fund form)."""
    return [
        {"intent": "move", "actor": MASTER, "target": "loc_keep"},
        {"intent": "move", "actor": MASTER, "target": CHEST},
        *steps,
    ]


# -- the grammar wall, measured (the discriminating test) -------------------------


def test_the_grammar_wall_was_real() -> None:
    """The cheapest discriminating test the owner's decision demanded,
    run and pinned: the iter-271 fork's wall is a SUBSTRATE limit, not
    a pack-authoring one. Three measured facts. (1) The actor grammar:
    a playscript step's actor must be a pack NPC — a location can never
    initiate (the loud refusal). (2) The closed verbs' census: every
    committed account door that can DECREASE a stock does so only from
    the intent actor — the single-stock block carries no endpoint keys
    at all (the from-side IS the actor by construction). (3) The
    behavioral probe: a crafted transfer door over the heap is refused
    at the ACTOR's own gate while the heap stands full — the location's
    stock unreachable by the closed set. Only the settle door (the
    legs form) names a location as a from-side."""
    pack = load_pack(PACK_DIR)
    account_doors = [
        a for a in pack.data["actions.json"]["actions"]
        if "account" in a
    ]
    settle_doors = []
    for door in account_doors:
        block = door["account"]
        if block.get("verb") == "settle":
            settle_doors.append(door)
            continue
        # the closed single-stock form: verb | kind | amount — NO
        # endpoint keys, the from-side implicitly the intent actor
        assert sorted(block) == ["amount", "kind", "verb"]
    assert len(settle_doors) == 1  # sell_bloom — the §6.4 arming
    legs = settle_doors[0]["account"]["legs"]
    assert any(
        leg["from"] == CROFTS for leg in legs
    )  # the ONLY from-side a location owns


def test_the_location_actor_is_refused_loud() -> None:
    """The wall's first leg: the playscript grammar pins actors to pack
    NPCs — a location can never initiate, so a location's stock can
    never be a transfer's from-side (the loud RunnerError, never a
    silent no-op)."""
    pack = load_pack(PACK_DIR)
    log = Path("/tmp/settlement_actor_refused.jsonl")
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    with pytest.raises(RunnerError, match="must be a pack npc id"):
        sim.run_playscript({
            "name": "wall", "seed": 42, "pack": "province_pack@0.1",
            "steps": [
                {"intent": "give_coin", "actor": CROFTS, "target": MASTER},
            ],
        })
    sim.close()


def test_the_closed_verb_cannot_drain_the_heap(tmp_path: Path) -> None:
    """The wall's behavioral leg: a crafted transfer door over the heap
    (the closed set's only multi-holder verb) is refused SOFTLY at the
    ACTOR's own solvency gate — the master holds no bloom, the heap
    sits at his feet full, and the transfer's from-side is the actor by
    construction. The wall measured; the settle door in the same twin
    then drains the same heap (the contrast IS the discrimination)."""

    def _wall_probe(data: dict) -> None:
        data["actions"]["actions"].append({
            "intent": "haul_bloom",
            "label": "haul a load off the heap",
            "resolver": "account",
            "ticks": 2,
            "check": None,
            "on_failure": None,
            "events": {"success": "account_transferred"},
            "requires": [
                {"noun": "actor", "test": "account_at_least",
                 "kind": "bloom", "value": 1},
            ],
            "fields": [],
            "account": {"verb": "transfer", "kind": "bloom", "amount": 1},
            "knowledge": {"success": [], "failure": []},
            "hooks": {"success": [], "failure": []},
            "notes": (
                "the crafted wall probe: the transfer's from-side is the "
                "actor by construction — the heap's holder a location"
            ),
        })

    steps = [
        {"intent": "haul_bloom", "actor": MASTER, "target": CROFTS},
        {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "wall", _wall_probe), tmp_path, "wall.jsonl", 42,
        _to_beam(steps),
    )
    # the transfer: refused softly at the ACTOR gate — the master holds
    # no bloom, the heap unreachable by the closed verb
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "haul_bloom"
    ]
    assert len(rejected) == 1
    assert rejected[0].outcome["failed_test"] == "actor.account_at_least"
    assert sim.projection[MASTER].get("account.bloom") is None
    # the settle: the same heap, the same twin — drained lawfully
    # (the sale's own change: the heap 10→9 — the post-sale crossings
    # bank the margin further, the final level the flows' own law;
    # ki114-1-impl: the heap banked two more crossings — every step
    # now feeds at the post-drain clock, the F1/F4 +4 translation)
    sales = [e for e in events if e.type == SETTLE_EVENT]
    assert len(sales) == 1
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in sales[0].state_changes][0] == (
        CROFTS, "account.bloom", 10, 9,
    )
    sim.close()


# -- the census (the arming as pack data) ------------------------------------------


def test_the_armed_census() -> None:
    """The row's named elements as committed pack data: the settle door
    (the two legs — the load walked, the price banked), the geography
    gate (the render_fund form: the beam's town, the master present),
    the two HOLDER gates (the heap's own, the chest's own), the
    knowledge row (the withhold's release public), the knows gloss,
    the settle template line, the story-critical listing, the two
    receiving stocks, the budget's honest re-declare — and UNARMED by
    doctrine (no urgency entry, no hook: the autonomous runtime never
    fires it, the corpus price zero)."""
    pack = load_pack(PACK_DIR)
    actions = {a["intent"]: a for a in pack.data["actions.json"]["actions"]}
    sale = actions["sell_bloom"]
    assert sale["resolver"] == "account"
    assert sale["account"] == {
        "verb": "settle",
        "legs": [
            {"from": CROFTS, "to": CHEST, "kind": "bloom", "amount": LOAD},
            {"from": CHEST, "to": CROFTS, "kind": "coin", "amount": PRICE},
        ],
    }
    assert sale["events"] == {"success": SETTLE_EVENT}
    gates = [
        (c.get("noun"), c.get("holder"), c["test"], c.get("kind"),
         c.get("value"))
        for c in sale["requires"]
    ]
    # the geography gate — the render_fund form (the sale at the beam)
    assert any(
        noun == "target" and test == "field_in"
        for noun, _h, test, _k, _v in gates
    )
    assert any(
        noun == "target" and test == "same_location"
        for noun, _h, test, _k, _v in gates
    )
    # the two HOLDER gates — the heap's own and the chest's own
    assert (None, CROFTS, "account_at_least", "bloom", LOAD) in gates
    assert (None, CHEST, "account_at_least", "coin", PRICE) in gates
    # the knowledge row: the withhold's release public to the witnesses
    block = sale["knowledge"]["success"]
    assert block == [{
        "who": "same_location", "except": ["actor"], "channel": "saw",
        "fidelity": "exact", "knows": "the_bloom_sold",
    }]
    # the knows gloss — the sale's own causal row
    assert pack.templates["knows"]["the_bloom_sold"] == (
        "the withhold sold at the beam — the bloom held back since the "
        "shave finally walked to the weighbeam, the price banked at the "
        "crofts where the tally's notches record it"
    )
    # the settle line + the story listing + the budget's re-declare
    assert pack.templates["events"][SETTLE_EVENT] == (
        "{actor} settles at {target}: {leg_0_amount} {leg_0_kind} for "
        "{leg_1_amount} {leg_1_kind}."
    )
    assert SETTLE_EVENT in pack.rules["importance"]["story_critical_events"]
    assert pack.rules["budget"]["templates"]["max"] == 80
    # the two receiving stocks: the beam's end + the camp's ledger
    crofts = next(
        loc for loc in pack.entities["locations"] if loc["id"] == CROFTS
    )
    malby = next(
        loc for loc in pack.entities["locations"] if loc["id"] == CHEST
    )
    assert crofts["accounts"] == {"bloom": 4, "coin": 0}
    assert malby["accounts"] == {"coin": 40, "bloom": 0}
    # UNARMED by doctrine: no urgency entry names the door, no hook
    # seeds it — the autonomous runtime never fires it
    urgencies = json.dumps(pack.rules.get("urgencies", {}))
    assert "sell_bloom" not in urgencies
    assert not sale["hooks"]["success"]


# -- the sale: one atomic event -----------------------------------------------------


def test_the_sale_walked_once(tmp_path: Path) -> None:
    """The re-weigh's sale walked once through the canon door: the
    master at the beam after the walk (the crossings en route — the
    heap banked 4→10, the chest 40→52; ki114-1-impl: every step feeds
    at the post-drain clock, two more crossings banked en route than
    the mid-drain feed caught, the F1/F4 +4 translation), ONE atomic
    account_settled event carrying BOTH legs and FOUR net state
    changes (the heap 10→9, the beam's receiving stock 0→1, the chest
    52→49, the camp's ledger 0→3), the beam's witnesses (the keeper of
    the weighbeam among them) learning the_bloom_sold exact, and the
    tale carrying the settle line with the bloom gloss riding the leg
    slot (rs-2's boundary, the legs' own form)."""
    steps = _to_beam([
        {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
        {"intent": "wait", "ticks": 10},
    ])
    events, pack, sim = _run_pack(
        _twin(tmp_path, "sale"), tmp_path, "sale.jsonl", 42, steps
    )
    sales = [e for e in events if e.type == SETTLE_EVENT]
    assert len(sales) == 1
    sale = sales[0]
    assert sale.actor == MASTER and sale.target == CHEST
    # the outcome's legs: the RESOLVED parties (the sale's own shape)
    assert sale.outcome["legs"] == [
        {"from": CROFTS, "to": CHEST, "kind": "bloom", "amount": LOAD},
        {"from": CHEST, "to": CROFTS, "kind": "coin", "amount": PRICE},
    ]
    # the conservation oracle's settle arm: every leg's amount matches
    # its from-side loss and to-side gain — one net change per account
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in sale.state_changes] == [
        (CROFTS, "account.bloom", 10, 9),
        (CHEST, "account.bloom", 0, 1),
        (CHEST, "account.coin", 52, 49),
        (CROFTS, "account.coin", 0, 3),
    ]
    # the beam's witnesses: the keeper of the weighbeam among them, all
    # exact, all the one token
    knowers = {r.who for r in sale.knowledge}
    assert MARKET in knowers and CROWD in knowers
    assert all(r.knows == "the_bloom_sold" for r in sale.knowledge)
    assert all(r.fidelity == "exact" for r in sale.knowledge)
    # the terminus: the ledger banked, the heap thinned, the beam fed
    assert sim.projection[CROFTS]["account.coin"] == 3
    assert sim.projection[CHEST]["account.bloom"] == 1
    sim.close()
    # the tale carries the settle line — the withhold's meaning riding
    # the leg slot through the kind gloss (rs-2's boundary)
    tale = render_chronicle(events, pack, seed=42)
    assert (
        "Garrick settles at Malby, the market town: 1 bloom kept off "
        "the weighbeam since the guild factor shaved the camp's weight "
        "two seasons back and the camp starved that winter — the "
        "withhold's own ledger for 3 coin." in tale
    )


def test_the_drain_compounds(tmp_path: Path) -> None:
    """The withhold's release is the world's own compounding, never a
    clock: three fires walk three loads (the heap 10→9→8→7, each sale
    its own event), the ledger climbing 0→3→6→9 — the drain repeated
    while the heap stands and the chest covers, the squeeze's own law
    (the amounts authored, the repetition the player's or the world's
    own arithmetic)."""
    steps = _to_beam([
        {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
        {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
        {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
        {"intent": "wait", "ticks": 10},
    ])
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "compound"), tmp_path, "compound.jsonl", 42, steps
    )
    sales = [e for e in events if e.type == SETTLE_EVENT]
    assert len(sales) == 3
    heaps = [
        (sale.state_changes[0].from_, sale.state_changes[0].to_)
        for sale in sales
    ]
    assert heaps == [(10, 9), (9, 8), (8, 7)]  # the heap's own chain
    ledgers = [
        next(c for c in sale.state_changes if c.entity == CROFTS
             and c.prop == "account.coin")
        for sale in sales
    ]
    assert [(c.from_, c.to_) for c in ledgers] == [(0, 3), (3, 6), (6, 9)]
    sim.close()


# -- the soft refusals (the per-leg gates) -------------------------------------------


def _prepositioned(stock: str, kind: str, level: int):
    """The refusal twin's mutation: the master pre-positioned at the
    beam (no crossings before the sale — the flows cannot refill the
    gate under test) and the named stock's genesis level crafted."""
    def _mutate(data: dict) -> None:
        for loc in data["entities"]["locations"]:
            if loc["id"] == stock:
                loc["accounts"][kind] = level
        for npc in data["entities"]["npcs"]:
            if npc["id"] == MASTER:
                npc["position"] = CHEST
    return _mutate


def test_the_empty_heap_is_refused_softly(tmp_path: Path) -> None:
    """The heap's own gate: an empty heap (bloom 0 at the genesis, the
    master at the beam before any crossing) refuses the sale SOFTLY —
    the attempt a fact (intent_rejected), the failed test naming the
    HOLDER, no state write, the ledger untouched."""
    steps = [
        {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "empty", _prepositioned(CROFTS, "bloom", 0)),
        tmp_path, "empty.jsonl", 42, steps,
    )
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "sell_bloom"
    ]
    assert len(rejected) == 1
    assert rejected[0].outcome["failed_test"] == "loc_crofts.account_at_least"
    assert sim.projection[CROFTS]["account.bloom"] == 0
    assert sim.projection[CROFTS]["account.coin"] == 0
    sim.close()


def test_the_thin_chest_is_refused_softly(tmp_path: Path) -> None:
    """The chest's own gate: a chest that cannot cover the price (coin
    2 < 3) refuses the sale SOFTLY — the failed test naming the CHEST's
    holder, the heap and the ledger both untouched (the transaction
    atomic: no partial landing)."""
    steps = [
        {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "thin", _prepositioned(CHEST, "coin", 2)),
        tmp_path, "thin.jsonl", 42, steps,
    )
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "sell_bloom"
    ]
    assert len(rejected) == 1
    assert rejected[0].outcome["failed_test"] == "loc_malby.account_at_least"
    assert sim.projection[CHEST]["account.coin"] == 2
    assert sim.projection[CROFTS]["account.bloom"] == 4
    assert sim.projection[CROFTS]["account.coin"] == 0
    sim.close()


# -- the class pin (the owner's example, the same mechanism) --------------------------


def test_the_buyers_purchase_one_atomic_event(tmp_path: Path) -> None:
    """The class law pinned with the owner's own example: the
    buyer-initiated purchase — the buyer pays coin, the crofts
    surrender bloom, the buyer receives bloom, the crofts receive coin
    — over the SAME settle verb, inexpressible over the closed set (a
    two-legged exchange with the coin FROM the actor and the bloom from
    a location). The crafted door carries the full grammar in one
    block: the noun-ref legs (from/to 'actor'), the explicit-id legs,
    the noun-form gate AND the holder gate. One atomic event, four net
    changes, the resolved legs naming the parties."""

    def _buyers_door(data: dict) -> None:
        for npc in data["entities"]["npcs"]:
            if npc["id"] == PC:
                npc["accounts"]["bloom"] = 0  # the buyer's receiving stock
        data["actions"]["actions"].append({
            "intent": "buy_bloom",
            "label": "buy a load off the heap",
            "resolver": "account",
            "ticks": 2,
            "check": None,
            "on_failure": None,
            "events": {"success": SETTLE_EVENT},
            "requires": [
                {"noun": "target", "test": "kind", "is": "location"},
                {"noun": "target", "test": "field_in", "field": "id",
                 "values": [CROFTS]},
                {"noun": "target", "test": "same_location", "with": "actor"},
                {"noun": "actor", "test": "account_at_least",
                 "kind": "coin", "value": PRICE},
                {"test": "account_at_least", "holder": CROFTS,
                 "kind": "bloom", "value": LOAD},
            ],
            "fields": [],
            "account": {
                "verb": "settle",
                "legs": [
                    {"from": "actor", "to": CROFTS,
                     "kind": "coin", "amount": PRICE},
                    {"from": CROFTS, "to": "actor",
                     "kind": "bloom", "amount": LOAD},
                ],
            },
            "knowledge": {"success": [], "failure": []},
            "hooks": {"success": [], "failure": []},
            "notes": (
                "the crafted genericity probe: the buyer-initiated "
                "purchase — coin from the ACTOR (the noun ref), bloom "
                "from the location to the actor, one atomic event"
            ),
        })

    steps = [
        {"intent": "move", "target": "loc_keep"},
        {"intent": "move", "target": CROFTS},
        {"intent": "buy_bloom", "target": CROFTS},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "buyer", _buyers_door), tmp_path, "buyer.jsonl",
        42, steps,
    )
    sales = [e for e in events if e.type == SETTLE_EVENT]
    assert len(sales) == 1
    sale = sales[0]
    assert sale.actor == PC and sale.target == CROFTS
    # the noun refs RESOLVED through the intent — the legs name parties
    assert sale.outcome["legs"] == [
        {"from": PC, "to": CROFTS, "kind": "coin", "amount": PRICE},
        {"from": CROFTS, "to": PC, "kind": "bloom", "amount": LOAD},
    ]
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in sale.state_changes] == [
        (PC, "account.coin", 6, 3),
        (CROFTS, "account.coin", 0, 3),
        (CROFTS, "account.bloom", 10, 9),
        (PC, "account.bloom", 0, 1),
    ]
    sim.close()


# -- the corpus laws ------------------------------------------------------------------


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the door never fires in the day-scale
    corpus scripts and the two receiving stocks seed silently (the
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
    sale's run byte-identical."""
    steps = _to_beam([
        {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
        {"intent": "wait", "ticks": 10},
    ])
    for name in ("det_a", "det_b"):
        _run_pack(
            _twin(tmp_path, name), tmp_path, f"{name}.jsonl", 42, steps
        )
    assert (tmp_path / "det_a.jsonl").read_bytes() == (
        tmp_path / "det_b.jsonl").read_bytes()
