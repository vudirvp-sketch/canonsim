"""campaccount — the camp's account (iter-186, the owner's
embodiment-options call over the world track's standing frames: the
camp's two remaining gaps — the account, the freight's volume — each
its own row, STATUS Next step's own routing): the charcoal debt's
arithmetic armed in the province pack as PURE PACK DATA over the res-1
substrate (the debt-1 residue class's newest row — ANCHOR_REGION
§6.4's crisis probe named the gap: "no committed account state —
debt-1 armed the crossing's only"), zero core change (the KI#87
precedent class, iter-157/161/162/185).

The arming (the row's three named elements):

- THE ACCOUNT — the master's THIN STOCK (npc_smelter_01, coin 3: the
  camp's unspent year, the withhold's own savings — the debt fund's
  climb toward the charcoal paper, the seat's own purse riding the
  paper's named holder);
- THE BLOOM'S NET FLOW — `the_bloom_nets`, the net +3 on the master
  each macro year (the weighing season's reckoning: the bloom walked
  to the beam at the year's turn nets the camp three);
- THE FOLD — the gross bloom sale NINE splits as the camp's net THREE
  and the charcoal row's standing service SIX; the service folded
  away by the CHEST'S ONE-FLOW LAW (a second every-year source into
  loc_malby's coin would co-due with the_guild_collects at every
  crossing, the D-182 fold's own constraint one level deeper) — the
  service mints no stock, the notes the arithmetic's only mirror.

The claim packet (TEST_PLAN §9):

- Claim: the charcoal debt's arithmetic is one pack-data arming — ONE
  SALE, TWO CLAIMS as live account state (the guild's claim double
  the camp's, the same two-to-one the toll's gross carries at the
  crossing: the tilted beam's justice uniform, the estrangement's
  arithmetic engine), the paper SIXTEEN (the starved winter's stores,
  twice the household's eight) with NO amortization path (the service
  the paper's weight, never its fall — the debt outlives the man
  unless the strong honest season outruns it), zero core, the fold
  respecting the one-flow-per-account law by construction.
- Lens(es): the changed-next-decision unit (who simulates differently
  — the reader of the year's tale sees the camp's reckoning beside
  the crossing's, the vale's year in three lines; the designer reads
  the fund's climb against the authored paper); the boundary lens
  (zero core — the service's live-stock absence the honest residue,
  the chest's climb stays the toll's take alone; the paper's fall a
  DISCRETE event beyond the flows, debt-1's own residue law).
- Prism: the committed-pack census; the committed YEAR run (the
  calendar experiment — the real cadence, the tale render); the
  crafted short-cadence twin (macro 480 / market 40 / fair 120 /
  seasons 120 — the sub-year law held) with its complete-ablation
  twin (the block AND all three entity stocks go together).
- Oracle: the event log scans (the flow outcomes, the state_changes'
  from_/to_, the chain to the year turn), the projection reads, the
  tale render, the fingerprint + the both-arms (t, type) strip
  compare.
- Falsifier: the chest's climb shifting (the service minting a second
  stock — the fold broken); a flow event drawing a canon stream (the
  fingerprint shifting — INV-2 broken); the co-due desync (a second
  chest-ward flow — the D-182 crash); the golden T1 bytes shifting (a
  corpus price); the tale losing the reckoning lines.
- Expected evidence: the census pins; the year run's three account
  events at t=518400 chained after the year turn (the camp's third in
  declaration order), the tale carrying the three reckoning lines
  under the Day 360 header; the twin's levels climbing exactly (2→4→6
  / 40→44→48 / 3→6→9 over the first crossings), the fingerprint
  EQUAL to the ablated twin, the stripped (t, type) lists equal; the
  T1 golden byte-identical.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  year run + the twin).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded in the economy
  notes: the standing service mints no stock — the chest's one-flow
  law; the paper's fall and the strong season's lump are discrete
  events beyond the flows; no player-scaled door armed in this row —
  the debt-1 residue class's own standing residue; the freight's
  volume surface stays owner-routed, the next row's own call).
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
CHEST = "loc_malby"
MASTER = "npc_smelter_01"
SOURCE_EVENT = "account_sourced"
PAPER = 16  # the charcoal row — the starved winter's stores (authored)

#: The first three crossings of the crafted twin (macro 480): the
#: three flows' expected climb — the crossing's net, the chest's take,
#: the camp's net, ONE SALE TWO CLAIMS at both doors of the vale.
EXPECTED_CLIMB: tuple[tuple[int, str, str, int, int], ...] = (
    (480, "the_toll_nets", KETTA, 2, 4),
    (480, "the_guild_collects", CHEST, 40, 44),
    (480, "the_bloom_nets", MASTER, 3, 6),
    (960, "the_toll_nets", KETTA, 4, 6),
    (960, "the_guild_collects", CHEST, 44, 48),
    (960, "the_bloom_nets", MASTER, 6, 9),
    (1440, "the_toll_nets", KETTA, 6, 8),
    (1440, "the_guild_collects", CHEST, 48, 52),
    (1440, "the_bloom_nets", MASTER, 9, 12),
)


# -- the helpers ----------------------------------------------------------------


def _twin(
    tmp_path: Path, name: str, *, armed: bool = True
) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the sub-year
    law (market 40, fair 120, seasons 120 — every entry < the year). The
    ablated twin is the COMPLETE ablation: the economy block, the entity
    stocks AND the account-block actions go together (entity accounts or
    account actions without the block are dead data, the lint's own
    refusal; the doors widened at charcoalpaper, iter-189)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["time"]["macro"]["cadence_ticks"] = 480
    calendar = rules["time"]["calendar"]
    calendar["market_days"]["every_ticks"] = 40
    calendar["fairs"]["every_ticks"] = 120
    calendar["seasons"]["every_ticks"] = 120
    if not armed:
        del rules["economy"]
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    if not armed:
        entities = json.loads(
            (target / "entities.json").read_text(encoding="utf-8")
        )
        for category in ("locations", "npcs"):
            for record in entities[category]:
                record.pop("accounts", None)
        (target / "entities.json").write_text(
            json.dumps(entities, indent=2), encoding="utf-8"
        )
        actions = json.loads(
            (target / "actions.json").read_text(encoding="utf-8")
        )
        actions["actions"] = [
            a for a in actions["actions"] if "account" not in a
        ]
        (target / "actions.json").write_text(
            json.dumps(actions, indent=2), encoding="utf-8"
        )
    return target


def _run_pack(
    pack_dir: Path, tmp_path: Path, name: str, seed: int,
    steps: list[dict[str, Any]],
) -> tuple[list, Any]:
    pack = load_pack(pack_dir)
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    result = sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": steps,
    })
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, result


def _run_script(
    tmp_path: Path, name: str, seed: int, script_path: Path
) -> tuple[list, Any]:
    pack = load_pack(PACK_DIR)
    script = load_playscript(script_path)
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, pack


# -- the census (the arming as pack data) ---------------------------------------


def test_the_armed_census() -> None:
    """The row's named elements as committed pack data: the master's
    thin stock (the debt fund's seat — the paper's named holder, the
    tally's carrier, the account riding the same seat), the third flow
    (the bloom's net — the weighing season's reckoning), the source
    template REUSED (the camp's reckoning rides the crossing's own
    line shape — the zero-template-price arming), the story listing
    already carrying the verb (tune-1's law, debt-1's own listing)."""
    pack = load_pack(PACK_DIR)
    economy = pack.rules["economy"]
    # iter-189 (charcoalpaper) widens the vocabulary again (paper — the
    # outstanding's own kind, the standing state's row — tests/
    # test_charcoalpaper.py the row's own packet)
    assert economy["accounts"] == ["coin", "bloom", "paper"]
    assert [(f["id"], f["verb"], f["to"], f["amount"], f["every"])
            for f in economy["flows"]
            if f["kind"] == "coin"] == [
        ("the_toll_nets", "source", KETTA, 2, 1),
        ("the_guild_collects", "source", CHEST, 4, 1),
        ("the_bloom_nets", "source", MASTER, 3, 1),
    ]
    master = next(n for n in pack.entities["npcs"] if n["id"] == MASTER)
    # iter-189 (charcoalpaper) adds the paper stock beside the fund —
    # the outstanding and its climb one read (the fall's own gate)
    assert master["accounts"] == {"coin": 3, "paper": 16}
    # the seat's own reading: the account rides the paper's named holder
    assert "camp_tally_01" in master["carries"]
    # the template reused — no new line shape, the zero-template price
    assert pack.templates["events"][SOURCE_EVENT] == (
        "{target} comes by {amount} {kind} at the year's reckoning."
    )
    assert SOURCE_EVENT in pack.rules["importance"]["story_critical_events"]


# -- the committed year band (the real cadence) ----------------------------------


def test_the_bloom_nets_at_the_years_reckoning(tmp_path: Path) -> None:
    """The committed year run (the calendar experiment's own script):
    the year crossing fires the turn, then the three coin flows chained
    to it in declaration order — the camp's third, the shapes exact
    (actor WORLD, the target the master, the outcome carrying the flow
    id + kind + amount, the state_changes the fund's climb 3→6, no
    knowledge, no hooks, importance medium — the story listing), the
    chain's root the year turn (the consumer-rides-the-clock law);
    iter-187 (freightvol) adds the withhold's bloom flow at the same
    crossing — the coin flows filtered to their own kind here (the
    heap's walk lives in its own packet)."""
    events, _pack = _run_script(
        tmp_path, "year.jsonl", 42,
        REPO / "tests" / "playscripts" / "province_calendar.json",
    )
    flows = [e for e in events if e.type == SOURCE_EVENT
             and e.outcome["kind"] == "coin"]
    assert len(flows) == 3
    assert all(e.t == 518400 for e in flows)  # the first macro crossing
    assert [(e.outcome["flow"], e.target) for e in flows] == [
        ("the_toll_nets", KETTA),
        ("the_guild_collects", CHEST),
        ("the_bloom_nets", MASTER),
    ]
    camp = flows[2]
    assert camp.actor == "world"
    assert camp.knowledge == () and camp.hooks == ()
    assert camp.importance == "medium"
    assert camp.outcome["kind"] == "coin" and camp.outcome["amount"] == 3
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in camp.state_changes] == [
        (MASTER, "account.coin", 3, 6),
    ]
    # the chain: the camp's flow walks back through the crossing's to
    # the year turn (the chronological-chain law)
    by_id = {e.id: e for e in events}
    cause = camp.cause
    while cause is not None and by_id[cause].type != "year_turns":
        cause = by_id[cause].cause
    assert cause is not None, "the turn must be the chain root"


def test_the_service_mints_no_stock_the_fold_holds(tmp_path: Path) -> None:
    """The chest's one-flow law, live: the charcoal row's standing
    service SIX a year mints NO stock — the chest's climb stays the
    toll's take alone (40→44, never 40→50), the service folded away
    with the notes its only mirror. The camp's fund climbs by its net
    three ALONE — the gross sale nine never a live state (the same
    honesty debt-1's fold carried: the gross six is the notes' own
    arithmetic, never an event). iter-187 (freightvol) adds the
    withhold's bloom flow at the same crossing — exactly ONE chest
    write among all the year's flows stays the fold's own proof (the
    coin claims' entity set unchanged by the heap's arrival)."""
    events, _pack = _run_script(
        tmp_path, "year.jsonl", 42,
        REPO / "tests" / "playscripts" / "province_calendar.json",
    )
    flows = [e for e in events if e.type == SOURCE_EVENT]
    by_flow = {e.outcome["flow"]: e for e in flows}
    assert by_flow["the_guild_collects"].state_changes[0].to_ == 44
    assert by_flow["the_bloom_nets"].state_changes[0].to_ == 6
    # exactly ONE chest write among all the year's flows — the service
    # never a second chest-ward write, the fold by construction
    chest_writes = [e for e in flows
                    if any(c.entity == CHEST for c in e.state_changes)]
    assert len(chest_writes) == 1
    coin_kinds = [e for e in flows if e.outcome["kind"] == "coin"]
    assert {c.entity for f in coin_kinds for c in f.state_changes} == {
        KETTA, CHEST, MASTER,
    }


def test_the_tale_carries_the_camps_reckoning(tmp_path: Path) -> None:
    """The changed-next-decision unit, rendered: the year's tale
    carries the THREE reckoning lines under the Day 360 header — the
    vale's year in three lines (the crossing's net, the chest's take,
    the camp's net), the coupled liabilities visible at one turn: two
    debts, one guild, one reckoning."""
    events, pack = _run_script(
        tmp_path, "year.jsonl", 42,
        REPO / "tests" / "playscripts" / "province_calendar.json",
    )
    tale = render_chronicle(events, pack, seed=42)
    assert "Ketta comes by 2 coin at the year's reckoning." in tale
    assert (
        "Malby, the market town comes by 4 coin at the year's reckoning."
        in tale
    )
    assert "Garrick comes by 3 coin at the year's reckoning." in tale


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the camp's flow rides the macro year
    (518400), beyond every day-scale corpus script's horizon by
    construction — the golden T1 fixture's own bytes the proof (the
    smoke run regenerates byte-identically under the armed pack)."""
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


# -- the crafted twin (the arithmetic at a short band) ---------------------------


def test_the_twin_climbs_the_three_funds(tmp_path: Path) -> None:
    """The twin walks the first three crossings: the three COIN levels
    climb exactly, the events in declaration order (the crossing's net,
    the chest's take, the camp's net — one reckoning, three claims),
    the accounts independent (three coin flows, three coin accounts, no
    co-due by construction — the one-flow-per-account law held at the
    camp's own arming; iter-187's bloom flow rides beside on its own
    account, filtered to the coin kind here — the heap's walk in its
    own packet)."""
    events, _ = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "armed.jsonl", 42,
        [{"intent": "wait", "ticks": 1500}],
    )
    assert [
        (e.t, e.outcome["flow"], e.state_changes[0].entity,
         e.state_changes[0].from_, e.state_changes[0].to_)
        for e in events if e.type == SOURCE_EVENT
        and e.outcome["kind"] == "coin"
    ][:9] == list(EXPECTED_CLIMB)


def test_the_fund_climbs_toward_the_paper(tmp_path: Path) -> None:
    """The camp's arithmetic, as numbers: after the twin's four
    crossings the projection holds the master's fund at fifteen — one
    reckoning short of the paper sixteen (the fifth crossing crosses
    it), the crossing's own climbs unchanged beside it (Ketta's punt
    fund, the chest's take — the three funds of the vale's two debts,
    each climbing at its own door). The paper's fall itself stays a
    discrete event beyond the flows (debt-1's residue law — the fund
    is the CAPACITY, never the clearance)."""
    pack = load_pack(_twin(tmp_path, "armed"))
    sim = Simulator(pack, 42, tmp_path / "legible.jsonl", SCHEMA,
                    commit="0000000")
    sim.run_playscript({
        "name": "legible", "seed": 42, "pack": "province_pack@0.1",
        "steps": [{"intent": "wait", "ticks": 1500}],
    })
    assert sim.projection[MASTER]["account.coin"] == 15  # 3 + 3x4
    assert sim.projection[KETTA]["account.coin"] == 10  # 2 + 2x4
    assert sim.projection[CHEST]["account.coin"] == 56  # 40 + 4x4
    assert 15 < PAPER <= 15 + 3  # the fifth reckoning crosses the row
    sim.close()


def test_the_fingerprint_never_sees_the_economy(tmp_path: Path) -> None:
    """INV-2's both-arms proof (the iter-83 measurement form): the
    armed twin against the COMPLETE ablated twin (the block and all
    three stocks ablated together) — the fingerprints EQUAL (the
    flows draw nothing, pure stock reads) and the event lists
    identical outside the account events (the delta is the economy
    alone)."""
    armed_events, armed = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "a.jsonl", 42,
        [{"intent": "wait", "ticks": 1500}],
    )
    ablated_events, ablated = _run_pack(
        _twin(tmp_path, "ablated", armed=False), tmp_path, "u.jsonl", 42,
        [{"intent": "wait", "ticks": 1500}],
    )
    assert armed.fingerprint == ablated.fingerprint
    strip = lambda es: [  # noqa: E731
        (e.t, e.type) for e in es if e.type != SOURCE_EVENT
    ]
    assert strip(armed_events) == strip(ablated_events)


def test_the_twin_is_deterministic(tmp_path: Path) -> None:
    """The T1 law at the twin's own band: same seed + steps +
    environment, byte-identical logs."""
    for name in ("det_a", "det_b"):
        _run_pack(
            _twin(tmp_path, name), tmp_path, f"{name}.jsonl", 42,
            [{"intent": "wait", "ticks": 1500}],
        )
    assert (tmp_path / "det_a.jsonl").read_bytes() == (
        tmp_path / "det_b.jsonl").read_bytes()
