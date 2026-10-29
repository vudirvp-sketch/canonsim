"""meaning2 — the SECOND meaning slice: the re-weigh's sale, the meaning
distribution's substrate measured at the deterministic band (iter-395, the
world track's W8-era content row — the owner's standing delegation «бери
что логичнее начать сейчас»: the audit's #1 named gap, the meaning layer
thinner than the mechanical, deepened by the second measured slice; the
event the NEWEST committed mechanics carry — the withhold's release, the
coupled liabilities' own beat, iter-273's settlement).

The slice's authored half lives in `ANCHOR_REGION.md` §7.2 — the same
mechanical event (ONE load of the withhold's heap walked to the beam),
FIVE bounded position-maps: the seat (the word spent for the debt's
standing), the beam (the count public at last), the guild's chest (the
debt serviceable, the interest's arithmetic), the crossing (the freight
returning, the misreading intact), the road (the near half witnesses, the
far half wordless until the rumor rides). This witness owns the
DISTRIBUTION'S SUBSTRATE — the half the deterministic band can measure
(the first slice's own honest remainder: «the distribution is not yet
measured» — the boundary oracle closes the deterministic half of that
gap; the live reading band stays open, the §7.1 form's own class):

- the MINT'S BOUNDARY: the sale's knowledge records land on EXACTLY the
  same_location witnesses at the beam — the market mistress (the beam's
  own hand), the Malby crowd, the watch sergeant ON DUTY at the market
  post (the 1080 rotation's own arithmetic — the duty post at Malby);
- the ABSENT MAPS: the actor exempt (the master's knowing his own
  authorship — no record minted, the reprice/settle convention); the
  keeper NEVER learns the release in this band (the crossing's map:
  knows the toll's thinning, never its cause); the far road, the crofts'
  winter kin, the steward — no records; the whole-log KnowledgeView
  holding the token on exactly the witness set (no ambient spread — the
  rumor channel its own door, never a leak);
- the ACCOUNTS' DIVERGENCE: the sale's own writes touch exactly the
  four legs (the heap, the beam's receiving stock, the chest, the camp's
  ledger) — the master's paper UNTOUCHED (the debt's standing: the sale
  banks the fund, never pays the paper — «the count prices trust, never
  coin», the §6.4 boundary held executable); the crossing's accounts
  never written by the sale (the coupling bites the artery, never the
  knowing — E⇄H's material edge);
- INV-2: the twin's double-run byte-identical (the family's own form).

The claim packet (TEST_PLAN §9):

- Claim: the second meaning slice's distribution rides the canonical
  knowledge boundary — after the sale, the five positions hold
  materially different states (accounts only / knowledge + stock /
  neither), each bounded exactly as the §7.2 maps claim, zero leakage
  across the boundary, zero pack change, zero core.
- Lens(es): the meaning-distribution lens (the same event, five maps,
  the positions' states diverging in KIND — the distribution's substrate
  measured, n=2 for the frontier's claim); the boundary lens (the
  token's holders exactly the witnesses; the absent maps executable);
  the economy lens (the paper untouched — the sale's own meaning half).
- Prism: the crafted short-cadence twin (macro 480 — the settlement
  family's own form, the master walked to the beam, seed 42).
- Oracle: the event's knowledge records, the whole-log KnowledgeView,
  the state_changes' entity set, the projection's account reads.
- Falsifier: a fourth knower minted by the sale (the boundary broken);
  the token reaching the keeper or the far road in the band (a leak);
  the paper or the keeper's accounts written by the sale's legs (the
  meaning inverted — the sale paying the debt or taxing the crossing);
  the twin's bytes diverging (INV-2).
- Expected evidence: knowers == {market mistress, crowd, duty sergeant};
  holders == knowers; paper 16 through the sale; the keeper absent from
  the sale's writes; the T1 self-compare green.
- Observed evidence: CONFIRMED at the measured band (seed 42, the twin
  of `tests/test_settlement.py`'s own form — the mechanics cited, never
  re-pinned: the door's legs the settlement witness's own rows).
- Epistemic class: measured, deterministic per seed.
- Disposition: the deterministic half CONFIRMED; the authored band
  PARTIALLY CONFIRMED (the §7.1 form's own class — the live reading
  band the slice's open half, the owner's future row).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.knowledge import KnowledgeView
from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

MASTER = "npc_smelter_01"        # the seat — the sale's initiating hand
KEEPER = "npc_weirkeeper_01"     # the crossing — the toll's own hand
MARKET = "npc_marketmistress_01" # the beam — the tally's carrier
CROWD = "npc_malby_crowd_01"     # the road's near half — the witnesses
SERGEANT = "npc_sergeant_01"     # the watch — on duty at the market post
SECONDHAND = "npc_secondhand_01" # the heir — the far road in this band
STEWARD = "npc_steward_01"       # Thornmill — the claim's own hand
WINTERKIN = "npc_winterkin_01"   # the crofts' guest — the care's edge
PC = "pc_01"
CHEST = "loc_malby"
CROFTS = "loc_crofts"
STAIR = "loc_weirstair"
TOKEN = "the_bloom_sold"
SETTLE_EVENT = "account_settled"

#: the beam's witness set — the sale's same_location knowers at the twin's
#: own arithmetic (the 1080 rotation returning the sergeant to the duty
#: post at Malby; the master's walk crossing three macro years, the heap
#: banked 4→10, the chest 40→52 — the settlement witness's own numbers).
WITNESSES = {MARKET, CROWD, SERGEANT}

#: every position the slice's maps bound — the absent set measured against.
ABSENT = {MASTER, KEEPER, SECONDHAND, STEWARD, WINTERKIN, PC}


# -- the twin (the settlement family's own form) -----------------------------------


def _twin(tmp_path: Path, name: str) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the sub-year
    law (market 40, fair 120, seasons 120) — `tests/test_settlement.py`'s
    own helper, repeated here because the family's tests stay
    self-contained (one claim packet, one file)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["time"]["macro"]["cadence_ticks"] = 480
    calendar = rules["time"]["calendar"]
    calendar["market_days"]["every_ticks"] = 40
    calendar["fairs"]["every_ticks"] = 120
    calendar["seasons"]["every_ticks"] = 120
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target


def _run(pack_dir: Path, tmp_path: Path, log_name: str, seed: int,
         steps: list[dict[str, Any]]) -> tuple[list, Simulator]:
    pack = load_pack(pack_dir)
    log = tmp_path / log_name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": log_name, "seed": seed, "pack": "province_pack@0.1",
        "steps": steps,
    })
    _, events = read_log(log, SCHEMA)
    return events, sim


#: the slice's event: the master walks one load of the withhold's heap to
#: the beam (the honest geography — crofts → keep → Malby), the sale fires
#: once, a short wait drains the beat.
SALE_STEPS = [
    {"intent": "move", "actor": MASTER, "target": "loc_keep"},
    {"intent": "move", "actor": MASTER, "target": CHEST},
    {"intent": "sell_bloom", "actor": MASTER, "target": CHEST},
    {"intent": "wait", "ticks": 10},
]


# -- the mint's boundary ------------------------------------------------------------


def test_the_mints_boundary_is_the_witness_set(tmp_path: Path) -> None:
    """The distribution's first leg: the sale's knowledge records land on
    EXACTLY the beam's same_location witnesses — the market mistress (the
    beam's own hand, the tally's carrier), the Malby crowd (the road's
    near half), and the watch sergeant ON DUTY at the market post (the
    1080 rotation's own arithmetic — the duty post at Malby, the watch's
    map: the sale lawful commerce, the writ never the river's iron). The
    master exempt — the authorship convention (the reprice/settle
    family's own form): the initiating hand needs no witness to its own
    act; his knowing rides his accounts, never a record."""
    events, sim = _run(
        _twin(tmp_path, "mint"), tmp_path, "mint.jsonl", 42, SALE_STEPS
    )
    sales = [e for e in events if e.type == SETTLE_EVENT]
    assert len(sales) == 1  # the slice's one event
    sale = sales[0]
    knowers = {r.who for r in sale.knowledge}
    assert knowers == WITNESSES  # EXACTLY the beam's three — no fourth mint
    assert all(r.knows == TOKEN for r in sale.knowledge)
    assert all(r.fidelity == "exact" for r in sale.knowledge)
    # the master's exemption: the authorship convention, not an omission
    assert MASTER not in knowers
    # the absent maps: no record rides past the boundary
    assert not (knowers & ABSENT)
    # the sergeant is the DUTY watch — the rotation's own arithmetic
    rotations = [e for e in events if e.type == "watch_change"]
    assert rotations, "the twin's rotations fired (the duty post's law)"
    assert rotations[-1].outcome["incoming"] == SERGEANT
    assert sim.projection[SERGEANT]["position"] == CHEST
    sim.close()


def test_the_absent_maps_stay_wordless(tmp_path: Path) -> None:
    """The distribution's second leg: the whole-log KnowledgeView holds
    the token on EXACTLY the witness set — the boundary holds through the
    band, no ambient spread (the rumor channel its own door, never a
    leak). The keeper NEVER learns the release: the crossing's map —
    knows the toll's thinning, never its cause — executable as the
    absence (the coupling's misreading preserved by the boundary itself:
    each half reading the other the favored one, the sale's fact never
    the stair's). The far road, the heir, the steward, the winter kin,
    the player — all wordless in this band."""
    events, _sim = _run(
        _twin(tmp_path, "absent"), tmp_path, "absent.jsonl", 42, SALE_STEPS
    )
    view = KnowledgeView.from_events(events)
    holders = {w for w in view.knowers() if view.holds(w, TOKEN)}
    assert holders == WITNESSES  # the boundary law: no fifth holder ever
    # the keeper's bounded map, executable: wordless at the stair
    assert not view.holds(KEEPER, TOKEN)
    assert not view.holds(SECONDHAND, TOKEN)  # the heir on the far road
    assert not view.holds(STEWARD, TOKEN)     # Thornmill's own grief
    assert not view.holds(WINTERKIN, TOKEN)   # the crofts' guest
    assert not view.holds(PC, TOKEN)          # the stranger never at the beam
    # the sale's witnesses hold it — the beam's own crowd
    for witness in WITNESSES:
        assert view.holds(witness, TOKEN)


# -- the accounts' divergence --------------------------------------------------------


def test_the_paper_stands_through_the_sale(tmp_path: Path) -> None:
    """The seat's map, executable half: the sale banks the FUND, never
    pays the paper — the master's paper sixteen UNTOUCHED through the
    sale (the debt's standing: «the count prices trust, never coin», the
    §6.4 boundary — the paper's fall its own door, the strong honest
    season's own law), the camp's ledger holding the banked three (the
    fund toward the paper, the tally's notches its record), and the
    master's own thin stock NEVER the price's terminus — the seat's
    discipline: banked where the tally's notches record it, never the
    master's purse."""
    events, sim = _run(
        _twin(tmp_path, "paper"), tmp_path, "paper.jsonl", 42, SALE_STEPS
    )
    sales = [e for e in events if e.type == SETTLE_EVENT]
    assert len(sales) == 1
    sale = sales[0]
    # the debt's standing: no leg of the sale touches the paper
    assert all(c.prop != "account.paper" for c in sale.state_changes)
    assert sim.projection[MASTER]["account.paper"] == 16
    # the fund banked at the camp's ledger — the tally's own site
    assert sim.projection[CROFTS]["account.coin"] == 3
    # the master's purse is the net flow's own mint, never the price's
    # terminus (the_bloom_nets banks to the SEAT at the year crossings;
    # the sale's coin leg lands on the CAMP's ledger)
    coin_leg = next(
        c for c in sale.state_changes
        if c.entity == CROFTS and c.prop == "account.coin"
    )
    assert (coin_leg.from_, coin_leg.to_) == (0, 3)
    assert MASTER not in {c.entity for c in sale.state_changes}
    sim.close()


def test_the_crossing_is_never_written_by_the_sale(tmp_path: Path) -> None:
    """The crossing's map, executable half: the coupling bites the ARTERY,
    never the knowing — the sale's own writes touch exactly the two
    holders the legs name (the crofts and the chest); the keeper's
    accounts are never among them (her coin's climb the toll flow's own
    mint at the year crossings, the artery's freight carried by the
    heap's level — the withhold released means the loads walking, the
    toll's own freight returning, E⇄H's material edge). The misreading's
    material: the crossing's ledger and the crossing's knowledge BOTH
    untouched by the sale — the thinning's cause never her question."""
    events, sim = _run(
        _twin(tmp_path, "crossing"), tmp_path, "crossing.jsonl", 42, SALE_STEPS
    )
    sales = [e for e in events if e.type == SETTLE_EVENT]
    assert len(sales) == 1
    sale = sales[0]
    # the sale's writes: exactly the legs' own holders
    written = {(c.entity, c.prop) for c in sale.state_changes}
    assert written == {
        (CROFTS, "account.bloom"),
        (CHEST, "account.bloom"),
        (CHEST, "account.coin"),
        (CROFTS, "account.coin"),
    }
    # the crossing never among them — her accounts the flows' own, never
    # the sale's
    assert KEEPER not in {c.entity for c in sale.state_changes}
    assert STAIR not in {c.entity for c in sale.state_changes}
    # the heap thinned — the artery's freight returning (the release's
    # own arithmetic: the load walked, the beam fed)
    heap = next(
        c for c in sale.state_changes
        if c.entity == CROFTS and c.prop == "account.bloom"
    )
    assert heap.to_ == heap.from_ - 1
    assert sim.projection[CHEST]["account.bloom"] == 1
    sim.close()


# -- INV-2 (the family's own closing arm) --------------------------------------------


def test_the_twin_is_deterministic(tmp_path: Path) -> None:
    """The twin's T1 self-compare: the same script twice, byte-identical —
    the distribution's substrate is canon, not chance (the boundary's law
    holds at every replay of the same seed)."""
    pack_dir = _twin(tmp_path, "det")
    first_log = tmp_path / "det_a.jsonl"
    _run(pack_dir, tmp_path, "det_a.jsonl", 42, SALE_STEPS)
    second_log = tmp_path / "det_b.jsonl"
    _run(pack_dir, tmp_path, "det_b.jsonl", 42, SALE_STEPS)
    assert first_log.read_bytes() == second_log.read_bytes()
