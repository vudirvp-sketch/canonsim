"""floodpaper — the crossing household's carrier strengthened
(iter-272, the §6.1 fill row of the W5 disposition iter-266's
fill-list: PAPER DEBT / PUNT BUYOUT / DEBT INHERITANCE — «усилить
carrier: paper representation → holder → inherited obligation →
later settlement; НЕ новый debt-примитив»): the flood debt's
outstanding armed as live account state over the account resolver's
player-scaled arm — pure pack data, zero core, the charcoalpaper
precedent family applied to the crossing.

The row's named elements: the FOURTH account kind `floodpaper` (the
flood winter's own paper — the borrowed punt twelve + the stranded
season's stores eight, the shelter law's cost; its own dated chain
in the kind's gloss, never the camp's starved winter — the two
papers one chest, two winters, the estrangement's own pair); the
STOCK on the toll-taker (the debt's holder-side seat at the
crossing); the RECEIVING stock on the second hand (the inheritance's
existence gate); the four lifecycle doors — `settle_paper` (the
FALL, the covered-fund gate), `render_toll` (the COLLECTION, the
geography gate at the chest), `pass_paper` (the INHERITANCE, the
receiving-stock gate — the drowned generation's open question
answered), `buy_punt` (the PUNT'S PURCHASE, the punt fund's
terminus — the flow vocabulary's no-terminus residue closed); ONE
COIN, TWO CLAIMS made doors (the settlement's twenty and the punt's
twelve drawing on the same thin surplus — the household's own
engine, §6.1's unit, now player-scale).

The honest residues (recorded, never smuggled): the punt's own
item-birth rides the parked entity-birth door (the st-5 family —
the purchase's canonical fact is the coin's walk + the witnesses'
word); the boatyard's purse is the market's location ledger (the
honest no-entity form, a dedicated entity a future row's own call).

The claim packet (TEST_PLAN §9):

- Claim: the crossing's flood debt is live account arithmetic — the
  standing visible in the projection, the flows never amortizing it,
  each lifecycle transition (fall, collection, inheritance, punt) a
  lawful canon event with exact shapes, and the two claims' coupling
  live door law.
- Lens(es): the residue-lifecycle lens (the inheritance rung — the
  TRANSFER rung the iter-160 trace named "the drowned generation's
  open question"); the coupling lens (one coin, two claims).
- Prism: the committed-pack census; the crafted short-cadence twin
  (macro 480) walking the fund's climb; the committed band's
  soft-refusal arms; the golden corpus.
- Oracle: the event log scans (the verb events' outcome/
  state_changes/knowledge shapes), the projection reads, the tale
  render, the golden corpus bytes.
- Falsifier: the fall firing against an uncovered fund; the punt
  spent leaving the fall still landing; the inheritance landing on a
  stockless target crashing loud; the golden T1 bytes shifting; the
  tale losing the fall's line.
- Expected evidence: the census pins; the twin's floodpaper standing
  at 20 through the crossings while the fund climbs; the fall
  refused early, landing when covered (the witnesses holding
  the_floodpaper_fell); the collection walking 20 coin to the chest;
  the punt's purchase walking 12 and the fall then REFUSED (the
  coupling); the inheritance walking the paper to the second hand;
  the corpus byte-identical.
- Observed evidence: CONFIRMED at the measured band (seed 42).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded above).
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

KETTA = "npc_weirkeeper_01"
DELLAN = "npc_secondhand_01"
CHEST = "loc_malby"
STAIR = "loc_weirstair"
MARKET = "npc_marketmistress_01"
POLE = "punt_pole_01"
FLOOD_PAPER = 20  # the borrowed punt twelve + the stranded season's stores eight
PUNT = 12  # the punt's buy-back — Dellan's claim on the same coin
FALL_EVENT = "account_consumed"
WALK_EVENT = "account_transferred"
SOURCE_EVENT = "account_sourced"


# -- the helpers ----------------------------------------------------------------


def _twin(tmp_path: Path, name: str) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the sub-year
    law (market 40, fair 120, seasons 120) — the charcoalpaper test's
    own shape, the toll fund's climb measured in minutes, not
    megaticks."""
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


def _toll_fund(events: list, sim: Simulator) -> int:
    """The toll fund at the run's end: the thin stock + the toll net's
    crossings (the relational read — the doors' own arithmetic never
    depends on the calendar's exact crossing count)."""
    crossings = [
        e for e in events if e.type == SOURCE_EVENT
        and e.outcome.get("flow") == "the_toll_nets"
    ]
    return sim.projection[KETTA]["account.coin"] + 0, len(crossings)


# -- the census (the arming as pack data) ---------------------------------------


def test_the_armed_census() -> None:
    """The row's named elements as committed pack data: the fourth
    account kind (floodpaper — the flood winter's own paper), the
    toll-taker's standing stock (the paper twenty beside the thin
    surplus), the second hand's receiving stock (the inheritance's
    existence gate), the four lifecycle doors (the fall, the
    collection, the inheritance, the punt), the kind's gloss, the
    knows glosses — and UNARMED by doctrine (no urgency entry, no
    hook: the census's UNREALIZED band until a witness exercises
    it)."""
    pack = load_pack(PACK_DIR)
    economy = pack.rules["economy"]
    assert economy["accounts"] == ["coin", "bloom", "paper", "floodpaper",
        "step", "notch"]
    # no flow touches the flood paper — the no-amortization law again
    assert not [f for f in economy["flows"] if f["kind"] == "floodpaper"]
    ketta = next(n for n in pack.entities["npcs"] if n["id"] == KETTA)
    assert ketta["accounts"] == {"coin": 2, "floodpaper": FLOOD_PAPER,
                                 "step": 3}  # iter-275: the timbers' setting
    dellan = next(n for n in pack.entities["npcs"] if n["id"] == DELLAN)
    assert dellan["accounts"] == {"floodpaper": 0}
    actions = {a["intent"]: a for a in pack.data["actions.json"]["actions"]}
    fall = actions["settle_paper"]
    assert fall["account"] == {"verb": "consume", "kind": "floodpaper",
                               "amount": FLOOD_PAPER}
    assert fall["events"] == {"success": FALL_EVENT}
    fall_tests = [(c["noun"], c["test"], c.get("kind"), c.get("value"))
                  for c in fall["requires"]]
    assert ("actor", "account_at_least", "floodpaper", FLOOD_PAPER) in fall_tests
    # the covered-fund gate — the fall's own law (reckon_paper's form)
    assert ("actor", "account_at_least", "coin", FLOOD_PAPER) in fall_tests
    assert fall["knowledge"]["success"][0]["knows"] == "the_floodpaper_fell"
    walk = actions["render_toll"]
    assert walk["account"] == {"verb": "transfer", "kind": "coin",
                               "amount": FLOOD_PAPER}
    walk_tests = [(c["noun"], c["test"], c.get("kind"), c.get("value"))
                  for c in walk["requires"]]
    assert ("target", "field_in", None, None) in [
        (n, t, None, None) for n, t, _, _ in walk_tests
    ]  # the chest pinned
    assert ("actor", "account_at_least", "coin", FLOOD_PAPER) in walk_tests
    assert walk["knowledge"]["success"] == []  # the guild's books need no witness
    inherit = actions["pass_paper"]
    assert inherit["account"] == {"verb": "transfer", "kind": "floodpaper",
                                  "amount": FLOOD_PAPER}
    inherit_tests = [(c["noun"], c["test"], c.get("kind"), c.get("value"))
                     for c in inherit["requires"]]
    assert ("actor", "account_at_least", "floodpaper", FLOOD_PAPER) in inherit_tests
    # the receiving-stock gate — the value-0 existence form
    assert ("target", "account_at_least", "floodpaper", 0) in inherit_tests
    assert inherit["knowledge"]["success"][0]["knows"] == "the_paper_inherited"
    punt = actions["buy_punt"]
    assert punt["account"] == {"verb": "transfer", "kind": "coin",
                               "amount": PUNT}
    punt_tests = [(c["noun"], c["test"], c.get("kind"), c.get("value"))
                  for c in punt["requires"]]
    assert ("actor", "account_at_least", "coin", PUNT) in punt_tests
    assert punt["knowledge"]["success"][0]["knows"] == "the_punt_bought"
    # the kind's own gloss — the flood winter's chain (never the camp's)
    assert pack.templates["account_kinds"]["floodpaper"] == (
        "paper owed to the guild's chest at Malby since the winter after "
        "the flood — the borrowed punt and the stranded season's stores, "
        "the shelter law's cost"
    )
    # UNARMED by doctrine: no urgency entry, no hook
    urgencies = json.dumps(pack.rules.get("urgencies", {}))
    for door in ("settle_paper", "render_toll", "pass_paper", "buy_punt"):
        assert door not in urgencies
    hooks_blob = json.dumps(pack.rules.get("director", {}))
    for door in ("settle_paper", "render_toll", "pass_paper", "buy_punt"):
        assert door not in hooks_blob


def test_the_standing_state_and_its_bindings() -> None:
    """The crossing's seat at one read: the flood paper's stock (the
    outstanding, the toll-taker the holder-side seat), the thin
    surplus beside it (the fund's climb the fall's own gate reads),
    the second hand's receiving stock, and the pole already on the
    same line (the pair: the tool and the obligation one
    inheritance)."""
    pack = load_pack(PACK_DIR)
    from core.fold import initial_projection

    projection = initial_projection(pack.entities)
    assert projection[KETTA]["account.floodpaper"] == FLOOD_PAPER
    assert projection[KETTA]["account.coin"] == 2
    assert projection[DELLAN]["account.floodpaper"] == 0
    assert projection[POLE]["carrier"] == DELLAN
    # the holder's home: the chest's coin — the collection's destination
    assert projection[CHEST]["account.coin"] == 40


# -- the covered-fund gate + the no-amortization law ------------------------------


def test_the_flows_never_amortize_the_flood_paper(tmp_path: Path) -> None:
    """The standing take is the paper's WEIGHT at the chest, never its
    fall: the crossings climb the fund while the flood paper stands
    UNCHANGED at 20 — the flows are coin and bloom, never floodpaper
    (the structural census made live state)."""
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "armed.jsonl", 42,
        # the wait's horizon lands the fourth crossing and no more
        [{"intent": "wait", "ticks": 1600}],
    )
    assert not [e for e in events if e.type in (FALL_EVENT, WALK_EVENT)
                and e.outcome.get("kind") == "floodpaper"]
    _fund, crossings = _toll_fund(events, sim)
    assert crossings == 4
    assert sim.projection[KETTA]["account.coin"] == 2 + 2 * 4
    assert sim.projection[KETTA]["account.floodpaper"] == FLOOD_PAPER
    sim.close()


def test_the_fall_requires_the_covered_fund(tmp_path: Path) -> None:
    """The soft door at the committed band: the fund 2 does not cover
    the paper 20 — the settlement is REFUSED softly (the attempt a
    fact, intent_rejected), the paper standing, the fund
    untouched."""
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "early"), tmp_path, "early.jsonl", 42,
        [{"intent": "settle_paper", "actor": KETTA},
         {"intent": "wait", "ticks": 10}],
    )
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "settle_paper"
    ]
    assert len(rejected) == 1
    assert sim.projection[KETTA]["account.floodpaper"] == FLOOD_PAPER
    assert sim.projection[KETTA]["account.coin"] == 2
    sim.close()


# -- the reckoning: the fall, then the collection ---------------------------------


def test_the_reckoning_when_the_fund_covers(tmp_path: Path) -> None:
    """The clearance walked once through the canon door: the
    toll-taker at the chest's town when the fund covers the paper —
    the FALL (account_consumed: the flood paper 20→0, the covered-fund
    gate passed, the witnesses holding the_floodpaper_fell), then the
    COLLECTION (account_transferred: 20 coin Ketta→chest), the walk's
    cause chained to the fall, and the tale carrying both lines (the
    kind's own gloss riding the fall — the flood winter's chain)."""
    steps = [
        # the toll-taker walks to the chest's town (the honest
        # geography: the fund renders at Malby) — the crossing's own
        # route, three legs (weirstair -> riverroad -> keep -> malby),
        # the crossings en route climbing the fund
        {"intent": "move", "actor": KETTA, "target": "loc_riverroad"},
        {"intent": "move", "actor": KETTA, "target": "loc_keep"},
        {"intent": "move", "actor": KETTA, "target": CHEST},
        # past the ninth crossing (t=4320): the fund 2 + 2x9 = 20
        {"intent": "wait", "ticks": 4400},
        # the fall, then the collection — the scene's lawful order
        {"intent": "settle_paper", "actor": KETTA},
        {"intent": "render_toll", "actor": KETTA, "target": CHEST},
        {"intent": "wait", "ticks": 10},
    ]
    events, pack, sim = _run_pack(
        _twin(tmp_path, "reckoning"), tmp_path, "reckoning.jsonl", 1, steps
    )
    falls = [e for e in events if e.type == FALL_EVENT
             and e.outcome.get("kind") == "floodpaper"]
    walks = [e for e in events if e.type == WALK_EVENT
             and e.outcome.get("kind") == "coin"
             and e.outcome.get("amount") == FLOOD_PAPER]
    assert len(falls) == 1 and len(walks) == 1
    fall, walk = falls[0], walks[0]
    _fund, crossings = _toll_fund(events, sim)
    fund = 2 + 2 * crossings
    assert fund >= FLOOD_PAPER  # the covered-fund gate passed
    # the fall's shapes: the toll-taker's flood paper consumed
    assert fall.actor == KETTA and fall.target is None
    assert fall.outcome["kind"] == "floodpaper"
    assert fall.outcome["amount"] == FLOOD_PAPER
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in fall.state_changes] == [
        (KETTA, "account.floodpaper", FLOOD_PAPER, 0),
    ]
    # the witnesses hold the fall — the crossing's own word
    assert all(r.knows == "the_floodpaper_fell" for r in fall.knowledge)
    knowers = {r.who for r in fall.knowledge}
    assert MARKET in knowers
    # the collection's shapes: 20 coin to the chest, the cause the fall
    assert walk.actor == KETTA and walk.target == CHEST
    assert walk.outcome["kind"] == "coin"
    assert walk.outcome["amount"] == FLOOD_PAPER
    chest_before = sim.projection[CHEST]["account.coin"] - FLOOD_PAPER
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in walk.state_changes] == [
        (KETTA, "account.coin", fund, fund - FLOOD_PAPER),
        (CHEST, "account.coin", chest_before, chest_before + FLOOD_PAPER),
    ]
    assert walk.cause == fall.id  # the chronological chain
    # the terminus: the paper fallen, the fund spent, the chest paid
    assert sim.projection[KETTA]["account.floodpaper"] == 0
    assert sim.projection[KETTA]["account.coin"] == fund - FLOOD_PAPER
    sim.close()
    # the tale carries the reckoning's two lines — the kind's own gloss
    # (the flood winter's chain, never the camp's starved winter)
    tale = render_chronicle(events, pack, seed=42)
    assert (
        "Ketta is rid of 20 paper owed to the guild's chest at Malby "
        "since the winter after the flood" in tale
    )
    assert "Ketta passes 20 coin to Malby, the market town." in tale


# -- ONE COIN, TWO CLAIMS ----------------------------------------------------------


def test_the_coupling_the_punt_first_leaves_the_fall_refused(
    tmp_path: Path,
) -> None:
    """The household's own engine as live door law: the fund climbed to
    fourteen (covering the punt's twelve, not the paper's twenty) —
    the PUNT'S PURCHASE lands (12 coin to Malby's ledger, the
    witnesses holding the_punt_bought), and the settlement is then
    REFUSED softly (the fund 2 no longer covers the paper 20 — ONE
    COIN, TWO CLAIMS, Dellan's need fed first)."""
    steps = [
        {"intent": "move", "actor": KETTA, "target": "loc_riverroad"},
        {"intent": "move", "actor": KETTA, "target": "loc_keep"},
        {"intent": "move", "actor": KETTA, "target": CHEST},
        # past the sixth crossing (t=2880): the fund 2 + 2x6 = 14
        {"intent": "wait", "ticks": 2500},
        {"intent": "buy_punt", "actor": KETTA, "target": CHEST},
        {"intent": "settle_paper", "actor": KETTA},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "coupling"), tmp_path, "coupling.jsonl", 42, steps
    )
    punt = [e for e in events if e.type == WALK_EVENT
            and e.outcome.get("kind") == "coin"
            and e.outcome.get("amount") == PUNT]
    assert len(punt) == 1
    assert punt[0].actor == KETTA and punt[0].target == CHEST
    assert punt[0].outcome["amount"] == PUNT
    assert all(r.knows == "the_punt_bought" for r in punt[0].knowledge)
    _fund, crossings = _toll_fund(events, sim)
    fund = 2 + 2 * crossings
    chest_before = sim.projection[CHEST]["account.coin"] - PUNT
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in punt[0].state_changes] == [
        (KETTA, "account.coin", fund, fund - PUNT),
        (CHEST, "account.coin", chest_before, chest_before + PUNT),
    ]
    # the settlement refused: the fund 2 no longer covers the paper
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "settle_paper"
    ]
    assert len(rejected) == 1
    assert sim.projection[KETTA]["account.floodpaper"] == FLOOD_PAPER
    assert sim.projection[KETTA]["account.coin"] == fund - PUNT
    sim.close()


# -- the inheritance: the line, never the craft ------------------------------------


def test_the_inheritance_walks_the_paper_to_the_line(tmp_path: Path) -> None:
    """The transfer door walked once: the flood paper walks to the
    second hand's declared receiving stock (the drowned generation's
    open question answered — the debt riding the living line), the
    stockless target refused SOFTLY (the value-0 existence gate, the
    KI#15 family's door shape), and the pole already on the same
    hand (the pair complete: the tool and the obligation one
    inheritance)."""
    steps = [
        # a stockless target first: the market mistress declares no
        # flood paper stock
        {"intent": "pass_paper", "actor": KETTA, "target": MARKET},
        # the handing-over at the stair: the second hand present
        {"intent": "pass_paper", "actor": KETTA, "target": DELLAN},
        {"intent": "wait", "ticks": 10},
    ]
    events, _pack, sim = _run_pack(
        _twin(tmp_path, "inherit"), tmp_path, "inherit.jsonl", 42, steps
    )
    rejected = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("action") == "pass_paper"
    ]
    assert len(rejected) == 1  # the stockless target, refused softly
    passes = [e for e in events if e.type == WALK_EVENT
              and e.outcome.get("kind") == "floodpaper"]
    assert len(passes) == 1
    paper = passes[0]
    assert paper.actor == KETTA and paper.target == DELLAN
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in paper.state_changes] == [
        (KETTA, "account.floodpaper", FLOOD_PAPER, 0),
        (DELLAN, "account.floodpaper", 0, FLOOD_PAPER),
    ]
    assert any(r.knows == "the_paper_inherited" for r in paper.knowledge)
    # the terminus: the debt rides the living line, the pole the same
    # hand's already (the pair — the tool and the obligation)
    assert sim.projection[KETTA]["account.floodpaper"] == 0
    assert sim.projection[DELLAN]["account.floodpaper"] == FLOOD_PAPER
    assert sim.projection[POLE]["carrier"] == DELLAN
    sim.close()


# -- the corpus laws --------------------------------------------------------------


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the doors never fire in the day-scale
    corpus scripts and the flood paper's stock seeds silently (the
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
    standing state's run byte-identical."""
    steps = [
        {"intent": "settle_paper", "actor": KETTA},
        {"intent": "wait", "ticks": 2000},
    ]
    for name in ("det_a", "det_b"):
        _run_pack(
            _twin(tmp_path, name), tmp_path, f"{name}.jsonl", 42, steps
        )
    assert (tmp_path / "det_a.jsonl").read_bytes() == (
        tmp_path / "det_b.jsonl").read_bytes()
