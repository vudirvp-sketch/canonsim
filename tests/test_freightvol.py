"""freightvol — the camp's freight volume (iter-187, the owner's
embodiment-options call over the world track's standing frames: the
camp's two remaining gaps — the account, the freight's volume — each
its own row; the account landed iter-186, this row the second): the
withhold's VOLUME SURFACE armed in the province pack as PURE PACK DATA
over the res-1 substrate (ANCHOR_REGION §6.4's second named gap: "the
road's road_counts aggregate carries the road's cardinality, never the
camp's bloom — the withhold's volume effect has no committed surface"),
zero core change (the KI#87 precedent class).

The one seed: the crofts' HEAP — a second account kind (`bloom`) on
loc_crofts, the withheld margin's own ledger (four loads at the
genesis: two seasons of the standing withhold, the shave's aftermath
priced in held loads) — plus the withhold's margin flow
(`the_withhold_banks`, +2 each macro year: the linger beat's ANNUAL
AGGREGATE, the marginal yield held back while the price stays fallen,
banked at the crofts where the tally's notches record it). The tally's
PRESENT COUNT now has a committed ledger (iter-185's boundary held:
the read mints the WORD, never the PRESENT — the PRESENT lives here,
as account state); the heap's level is the artery's thinning made
legible (E⇄H's material edge: two loads a year of the toll's own
freight kept off the artery while the heap climbs).

The claim packet (TEST_PLAN §9):

- Claim: the withhold's volume effect is one pack-data arming — the
  held margin as live account state climbing beside the coin funds
  (the burn's rhythm five loads: the honest sale three walking to the
  beam — the gross nine, campaccount's own arming — plus the withheld
  two banked), the coupled liabilities' material edge legible as
  numbers (the heap's level the crossing's toll-starvation), zero
  core.
- Lens(es): the changed-next-decision unit (who simulates differently
  — the reader of the year's tale sees the fourth reckoning line, the
  artery's loss beside the debts' service; the designer reads the
  heap's climb against the sale's margin); the boundary lens (the
  drain door deliberately UNARMED — the heap climbs monotonically in
  the committed band, the withhold deepening, §6.4's own
  transformation rung; the re-weigh's sale rides the account
  resolver's player-scaled verbs, debt-1's standing residue; no price
  formula for bloom — the beam's price is the shave's own authored
  tilt, never a derived function of the heap).
- Prism: the committed-pack census; the committed YEAR run (the
  calendar experiment — the real cadence, the tale render); the
  crafted short-cadence twin (macro 480 / market 40 / fair 120 /
  seasons 120) with its complete-ablation twin (the block AND all
  four entity stocks go together); the action census (no account
  verb armed in the pack — the drain door's absence pinned).
- Oracle: the event log scans (the flow outcome, the state_changes'
  from_/to_, the chain to the year turn), the projection reads, the
  tale render, the fingerprint + the both-arms (t, type) strip
  compare.
- Falsifier: the heap's climb touching a coin fund (the kinds
  crossing — the accounts' separation broken); a flow event drawing a
  canon stream (the fingerprint shifting — INV-2 broken); the
  co-due desync (a second flow onto the crofts' bloom); the golden
  T1 bytes shifting (a corpus price); the tale losing the fourth
  reckoning line.
- Expected evidence: the census pins; the year run's FOURTH account
  event at t=518400 chained after the coin flows to the year turn,
  the tale carrying the four reckoning lines under the Day 360
  header; the twin's heap climbing exactly (4→6→8→10 over the first
  three crossings) with the coin funds' climb unchanged; the
  fingerprint EQUAL to the ablated twin, the stripped (t, type)
  lists equal; the T1 golden byte-identical.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  year run + the twin).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded in the economy
  notes: the flow carries the STANDING withhold's margin — the
  price's recovery (an authored future season) would end the banking,
  the flow vocabulary having no conditional cadence; the heap's drain
  un-armed (the player-scaled door, debt-1's standing residue — a
  future row's own call); the read mints the WORD, the ledger carries
  the PRESENT — the two surfaces never conflated).
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
CROFTS = "loc_crofts"
SOURCE_EVENT = "account_sourced"
MARGIN = 2  # the withheld loads a year — the linger beat's aggregate

#: The first three crossings of the crafted twin (macro 480): the
#: heap's expected climb — the withhold deepening, two loads a year
#: banked while the price stays fallen.
EXPECTED_HEAP: tuple[tuple[int, str, str, int, int], ...] = (
    (480, "the_withhold_banks", CROFTS, 4, 6),
    (960, "the_withhold_banks", CROFTS, 6, 8),
    (1440, "the_withhold_banks", CROFTS, 8, 10),
)


# -- the helpers ----------------------------------------------------------------


def _twin(
    tmp_path: Path, name: str, *, armed: bool = True
) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the sub-year
    law (market 40, fair 120, seasons 120 — every entry < the year). The
    ablated twin is the COMPLETE ablation: the economy block, the entity
    stocks, the account-block actions AND the account-kind gloss table
    go together (entity accounts, account actions or a gloss table
    without the block are dead data, the lint's own refusal; the doors
    widened at charcoalpaper, iter-189; the table rs-2, iter-191)."""
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
        templates = json.loads(
            (target / "templates.json").read_text(encoding="utf-8")
        )
        # rs-2 (iter-191): the account-kind gloss table rides the
        # economy block — the COMPLETE ablation drops the read-side
        # half with the rest (a table without the block is all dead
        # data, the lint's own refusal)
        templates.pop("account_kinds", None)
        (target / "templates.json").write_text(
            json.dumps(templates, indent=2), encoding="utf-8"
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
    """The row's named elements as committed pack data: the second
    account kind (bloom — the withheld loads, the heap's own measure),
    the crofts' stock (four loads: two seasons of the standing
    withhold), the fourth flow (the margin — the linger beat's annual
    aggregate), the source template REUSED again (the same reckoning
    line shape — the zero-template price held), the drain door
    deliberately UNARMED (no action carries an account block — the
    re-weigh's sale a future row's own call, debt-1's standing
    residue)."""
    pack = load_pack(PACK_DIR)
    economy = pack.rules["economy"]
    # iter-189 (charcoalpaper) widens the vocabulary again (paper — the
    # outstanding's own kind, the standing state's row)
    assert economy["accounts"] == ["coin", "bloom", "paper"]
    assert [(f["id"], f["verb"], f["kind"], f["to"], f["amount"],
             f["every"]) for f in economy["flows"]
            if f["kind"] == "bloom"] == [
        ("the_withhold_banks", "source", "bloom", CROFTS, MARGIN, 1),
    ]
    crofts = next(
        loc for loc in pack.entities["locations"] if loc["id"] == CROFTS
    )
    assert crofts["accounts"] == {"bloom": 4}
    # the DRAIN door still un-armed — no player-scaled verb moves the
    # bloom heap (the paper's lifecycle doors exist since iter-189,
    # charcoalpaper — but the re-weigh's SALE, the held loads walked to
    # the beam, remains a future row's own call: the withhold's drain)
    assert not [
        a for a in pack.data["actions.json"]["actions"]
        if "account" in a and a["account"]["kind"] == "bloom"
    ]
    # the template reused, the story listing already carries the verb
    assert pack.templates["events"][SOURCE_EVENT] == (
        "{target} comes by {amount} {kind} at the year's reckoning."
    )
    assert SOURCE_EVENT in pack.rules["importance"]["story_critical_events"]


# -- the committed year band (the real cadence) ----------------------------------


def test_the_withhold_banks_at_the_years_reckoning(tmp_path: Path) -> None:
    """The committed year run: the year crossing fires the turn, then
    the four flows chained to it in declaration order — the withhold's
    margin FOURTH (after the three coin flows), the shapes exact (actor
    WORLD, the target the crofts, the outcome carrying the flow id +
    kind + amount, the state_changes the heap's climb 4→6, no
    knowledge, no hooks, importance medium), the chain's root the year
    turn (the consumer-rides-the-clock law)."""
    events, _pack = _run_script(
        tmp_path, "year.jsonl", 42,
        REPO / "tests" / "playscripts" / "province_calendar.json",
    )
    flows = [e for e in events if e.type == SOURCE_EVENT]
    assert len(flows) == 4
    assert [(e.outcome["flow"], e.target) for e in flows] == [
        ("the_toll_nets", KETTA),
        ("the_guild_collects", CHEST),
        ("the_bloom_nets", MASTER),
        ("the_withhold_banks", CROFTS),
    ]
    margin = flows[3]
    assert margin.t == 518400  # the first macro crossing
    assert margin.actor == "world"
    assert margin.knowledge == () and margin.hooks == ()
    assert margin.importance == "medium"
    assert margin.outcome == {
        "flow": "the_withhold_banks", "kind": "bloom", "amount": MARGIN,
    }
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in margin.state_changes] == [
        (CROFTS, "account.bloom", 4, 6),
    ]
    # the chain: the margin walks back through the coin flows to the
    # year turn (the chronological-chain law)
    by_id = {e.id: e for e in events}
    cause = margin.cause
    while cause is not None and by_id[cause].type != "year_turns":
        cause = by_id[cause].cause
    assert cause is not None, "the turn must be the chain root"


def test_the_tale_carries_the_fourth_reckoning(tmp_path: Path) -> None:
    """The changed-next-decision unit, rendered: the year's tale carries
    the FOUR reckoning lines under the Day 360 header — the vale's year
    in four lines (the crossing's net, the chest's take, the camp's
    net, the heap's margin), the withhold's volume visible at the same
    turn as the debts it starves: the artery's loss beside the papers'
    service."""
    events, pack = _run_script(
        tmp_path, "year.jsonl", 42,
        REPO / "tests" / "playscripts" / "province_calendar.json",
    )
    tale = render_chronicle(events, pack, seed=42)
    assert "Ketta comes by 2 coin at the year's reckoning." in tale
    assert "Garrick comes by 3 coin at the year's reckoning." in tale
    assert "the smelt crofts comes by 2 bloom at the year's reckoning." in (
        tale
    )


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the margin flow rides the macro year
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


# -- the crafted twin (the withhold's ledger at a short band) ---------------------


def test_the_twin_climbs_the_heap(tmp_path: Path) -> None:
    """The twin walks the first three crossings: the heap climbs
    exactly (the withhold deepening — two loads a year banked), the
    coin funds' climb UNCHANGED beside it (the sold three still
    walking: the camp's honest surplus untouched by the margin's
    banking — the kinds separate, the accounts separate, no co-due by
    construction)."""
    events, _ = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "armed.jsonl", 42,
        [{"intent": "wait", "ticks": 1500}],
    )
    assert [
        (e.t, e.outcome["flow"], e.state_changes[0].entity,
         e.state_changes[0].from_, e.state_changes[0].to_)
        for e in events if e.type == SOURCE_EVENT
        and e.outcome["flow"] == "the_withhold_banks"
    ][:3] == list(EXPECTED_HEAP)
    # the coin funds' climb unchanged — the kinds never cross
    coin = [
        (e.outcome["flow"], e.state_changes[0].entity,
         e.state_changes[0].from_, e.state_changes[0].to_)
        for e in events if e.type == SOURCE_EVENT
        and e.outcome["kind"] == "coin"
    ][:6]
    assert coin == [
        ("the_toll_nets", KETTA, 2, 4),
        ("the_guild_collects", CHEST, 40, 44),
        ("the_bloom_nets", MASTER, 3, 6),
        ("the_toll_nets", KETTA, 4, 6),
        ("the_guild_collects", CHEST, 44, 48),
        ("the_bloom_nets", MASTER, 6, 9),
    ]


def test_the_heaps_level_is_the_arterys_thinning(tmp_path: Path) -> None:
    """The changed-next-decision unit, as numbers: after the twin's
    four crossings the projection holds the heap at TWELVE — the
    withhold's own arithmetic (four loads held at the genesis plus two
    a year: twelve loads of the toll's own freight kept off the artery
    since the shave), the four accounts of the vale's year legible at
    one read (two debts' funds, the chest's take, the heap's margin —
    the coupled liabilities E⇄H as live state, the heap's level the
    crossing's toll-starvation)."""
    pack = load_pack(_twin(tmp_path, "armed"))
    sim = Simulator(pack, 42, tmp_path / "legible.jsonl", SCHEMA,
                    commit="0000000")
    sim.run_playscript({
        "name": "legible", "seed": 42, "pack": "province_pack@0.1",
        "steps": [{"intent": "wait", "ticks": 1500}],
    })
    assert sim.projection[CROFTS]["account.bloom"] == 12  # 4 + 2x4
    assert sim.projection[MASTER]["account.coin"] == 15  # 3 + 3x4
    assert sim.projection[KETTA]["account.coin"] == 10  # 2 + 2x4
    assert sim.projection[CHEST]["account.coin"] == 56  # 40 + 4x4
    # the heap's margin never touches the coin funds — the kinds' law
    assert sim.projection[CROFTS].get("account.coin") is None
    assert sim.projection[MASTER].get("account.bloom") is None
    sim.close()


def test_the_fingerprint_never_sees_the_economy(tmp_path: Path) -> None:
    """INV-2's both-arms proof (the iter-83 measurement form): the
    armed twin against the COMPLETE ablated twin (the block and all
    four stocks ablated together) — the fingerprints EQUAL (the flows
    draw nothing, pure stock reads) and the event lists identical
    outside the account events (the delta is the economy alone)."""
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
