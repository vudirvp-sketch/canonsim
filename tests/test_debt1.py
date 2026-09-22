"""debt-1 — the crossing household's flood debt economy arm (iter-162,
the owner's iter-161 routing call, the debt-1 standing row): the debt's
arithmetic armed in the province pack as PURE PACK DATA over the res-1
substrate (CONTRACTS §2, D-179) — the THIRD consumer arming (the grim
tavern the first, iter-148; the pressure city the second, iter-149),
zero core change (the KI#87 precedent class, iter-157/161).

The arming (the row's three named elements):

- THE ACCOUNTS — the toll-taker's THIN SURPLUS (npc_weirkeeper_01,
  coin 2: the household's unspent year, itself the punt fund's climb
  toward the authored twelve — Dellan's claim on the same coin) and
  the guild's CHEST at the weighbeam (loc_malby, coin 40 — the grim
  till's location form; the GROUP entity takes no stock, the entity
  lint's closed group vocabulary carrying no accounts key — the
  substrate finding recorded in the block's notes, never patched in a
  zero-core slice);
- THE TOLL-SURPLUS FLOW — `the_toll_nets`, the net source +2 on the
  toll-taker each macro year;
- THE GUILD'S COLLECTION — `the_guild_collects`, the take +4 into the
  chest each macro year.

THE FOLD IS THE ENGINE'S OWN LAW (pack-4's discovered precedent,
D-182's recorded residue — the row's own named constraint): the
toll-surplus flow and the guild's collection would be CO-DUE on the
toll-taker's coin at every year crossing (flow_drafts builds every
draft against the crossing's single snapshot — the second flow's
from_ desyncs at the _commit gate, loud), so the year's arithmetic is
FOLDED: the gross toll six splits as the net two plus the take four,
both flows SOURCES, the transfer's household-side half folded away.

The claim packet (TEST_PLAN §9):

- Claim: the debt's arithmetic (the accounts, the toll-surplus flow,
  the guild's collection) is one pack-data arming — ONE COIN, TWO
  CLAIMS as live account state (the guild's claim outweighing the
  family's two-to-one), zero core, the fold respecting the co-due
  limit by construction.
- Lens(es): the changed-next-decision unit (who simulates differently
  — the reader of the year's tale sees the reckoning; the designer
  reads the surplus's climb against the authored punt); the boundary
  lens (zero core — the substrate's own laws unbroken: the fold, the
  sources' unreachable underflow, the draw-free flows).
- Prism: the committed-pack census; the committed YEAR run (the
  calendar experiment — the real cadence, the tale render); the
  crafted short-cadence twin (macro 480 / market 40 / fair 120 /
  seasons 120 — the sub-year law held) with its unarmed twin (the
  complete ablation: the block AND the entity stocks).
- Oracle: the event log scans (the flow outcomes, the state_changes'
  from_/to_, the chain to the year turn), the projection reads, the
  tale render, the fingerprint + the both-arms (t, type) strip
  compare, the T1 golden byte-identity.
- Falsifier: a flow event drawing a canon stream (the fingerprint
  shifting — INV-2 broken); the co-due desync (the second flow's
  from_ stale — the D-182 crash); the golden T1 bytes shifting (a
  corpus price); the calendar experiment's own laws breaking at the
  year crossing.
- Expected evidence: the census pins; the year run's two account
  events at t=518400 chained after the year turn, importance medium
  (the story listing), the tale carrying the reckoning lines under
  the Day 360 header; the twin's levels climbing exactly (2→4→6→8 /
  40→44→48→52 over the first crossings), the fingerprint EQUAL to the
  unarmed twin, the stripped (t, type) lists equal; the T1 golden
  byte-identical.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  year run + the twin; the probe battery's own runs).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues recorded in the block's
  notes: the flow vocabulary has no terminus and no amortization —
  the paper's fall, the clearance lump and the punt's purchase are
  discrete events beyond the flows, no player-scaled door armed in
  this row; the group-stock lint gap).
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
GUILD = "grp_river_guild"
SOURCE_EVENT = "account_sourced"

#: the first four crossings of the crafted twin (macro 480): the
#: levels' expected climb — the household's net two against the
#: guild's take four, ONE COIN TWO CLAIMS as account state.
EXPECTED_CLIMB: tuple[tuple[int, str, str, int, int], ...] = (
    (480, "the_toll_nets", KETTA, 2, 4),
    (480, "the_guild_collects", CHEST, 40, 44),
    (960, "the_toll_nets", KETTA, 4, 6),
    (960, "the_guild_collects", CHEST, 44, 48),
    (1440, "the_toll_nets", KETTA, 6, 8),
    (1440, "the_guild_collects", CHEST, 48, 52),
)


# -- the helpers ----------------------------------------------------------------


def _twin(
    tmp_path: Path, name: str, *, armed: bool = True
) -> Path:
    """The crafted short-cadence twin: the committed pack with the macro
    year shrunk to 480 ticks and the calendar scaled inside the sub-year
    law (market 40, fair 120, seasons 120 — every entry < the year). The
    unarmed twin is the COMPLETE ablation: the economy block, the
    entity stocks, the account-block actions AND the account-kind
    gloss table go together (the pairing law's halves — entity accounts or account actions
    without the block are dead data, the lint's own refusal; the doors
    widened at charcoalpaper, iter-189)."""
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
        # data, the lint's own refusal); rs-4 (iter-199): the
        # flow-gloss table rides the same law
        templates.pop("account_kinds", None)
        templates.pop("flow_glosses", None)
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
    """The row's three named elements as committed pack data: the
    accounts (the toll-taker's thin surplus, the chest at the
    weighbeam — the grim till's location form, the group taking no
    stock), the two flows (both SOURCES, the fold), the verb line in
    the template vocabulary (the arming's corpus price), the story
    listing (the reckoning a story beat of this pack). iter-186
    (campaccount) adds the camp's own third flow beside these — the
    crossing's census here keeps its two (the camp's claims live in
    tests/test_campaccount.py, the row's own packet)."""
    pack = load_pack(PACK_DIR)
    economy = pack.rules["economy"]
    # iter-187 (freightvol) widens the kind vocabulary (bloom joins),
    # iter-189 (charcoalpaper) again (paper — the outstanding's own
    # kind) — the crossing's coin claims still pinned by their own kind
    assert economy["accounts"] == ["coin", "bloom", "paper"]
    assert [(f["id"], f["verb"], f["to"], f["amount"], f["every"])
            for f in economy["flows"]
            if f["id"] in ("the_toll_nets", "the_guild_collects")] == [
        ("the_toll_nets", "source", KETTA, 2, 1),
        ("the_guild_collects", "source", CHEST, 4, 1),
    ]
    ketta = next(n for n in pack.entities["npcs"] if n["id"] == KETTA)
    assert ketta["accounts"] == {"coin": 2}
    malby = next(
        loc for loc in pack.entities["locations"] if loc["id"] == CHEST
    )
    assert malby["accounts"] == {"coin": 40}
    guild = next(g for g in pack.entities["groups"] if g["id"] == GUILD)
    assert "accounts" not in guild  # the group-stock lint gap, recorded
    # the verb line (the lint's closure law) + the story listing;
    # rs-4 (iter-199): the verb line gains the flow-gloss tail — the
    # banking lines carry their flows' meanings (the conditional stays
    # dry for unglossed flows and door-minted events)
    assert pack.templates["events"][SOURCE_EVENT] == (
        "{target} comes by {amount} {kind} at the year's reckoning"
        "{flow? — {flow}}."
    )
    assert SOURCE_EVENT in pack.rules["importance"]["story_critical_events"]


def test_the_budget_redeclares_the_template_ceiling() -> None:
    """AP-1's own law: growth inside the bounds or an honest re-declare
    — the verb line grows the template families past the declared 60,
    and the budget carries the re-declared ceiling with its note (65 at
    debt-1; 70 at charcoalpaper, iter-189 — the lifecycle doors' two
    verb lines)."""
    pack = load_pack(PACK_DIR)
    budget = pack.rules["budget"]["templates"]
    assert budget["min"] <= len(pack.templates["events"]) <= budget["max"]
    assert budget["max"] == 70


# -- the committed year band (the real cadence) ----------------------------------


def test_the_flows_fire_at_the_years_reckoning(tmp_path: Path) -> None:
    """The committed year run (the calendar experiment's own script):
    the year crossing fires the turn, then the two flows chained to it
    (the consumer-rides-the-clock law), the shapes exact — actor WORLD,
    the target the account's entity, the outcome carrying the flow id +
    kind + amount (the D-112 cardinality surface), the state_changes
    the levels' climb, no knowledge, no hooks, importance medium (the
    story listing — the reckoning renders). iter-186 (campaccount)
    adds the camp's third flow at the same crossing — the crossing's
    two pinned here by their own ids (the camp's walk lives in its own
    packet)."""
    events, _pack = _run_script(
        tmp_path, "year.jsonl", 42,
        REPO / "tests" / "playscripts" / "province_calendar.json",
    )
    flows = [e for e in events if e.type == SOURCE_EVENT
             and e.outcome["flow"] in ("the_toll_nets",
                                       "the_guild_collects")]
    assert len(flows) == 2
    assert all(e.t == 518400 for e in flows)  # the first macro crossing
    assert [(e.outcome["flow"], e.target) for e in flows] == [
        ("the_toll_nets", KETTA), ("the_guild_collects", CHEST),
    ]
    for flow in flows:
        assert flow.actor == "world"
        assert flow.knowledge == () and flow.hooks == ()
        assert flow.importance == "medium"
        assert flow.outcome["kind"] == "coin"
    assert [(c.entity, c.prop, c.from_, c.to_)
            for f in flows for c in f.state_changes] == [
        (KETTA, "account.coin", 2, 4),
        (CHEST, "account.coin", 40, 44),
    ]
    # the chain: each flow's cause walks back to the year turn
    by_id = {e.id: e for e in events}
    for flow in flows:
        cause = flow.cause
        while cause is not None and by_id[cause].type != "year_turns":
            cause = by_id[cause].cause
        assert cause is not None, "the turn must be the chain root"


def test_the_reckoning_renders_in_the_tale(tmp_path: Path) -> None:
    """The meaning rung: the story listing's payoff — the year's tale
    carries the reckoning lines under the Day 360 header (the debt's
    weight visible at the year's turn, where the weather stays canon
    without a line — the ambient family's own law, the committed form
    held)."""
    events, pack = _run_script(
        tmp_path, "year.jsonl", 42,
        REPO / "tests" / "playscripts" / "province_calendar.json",
    )
    tale = render_chronicle(events, pack, seed=42)
    # rs-4 (iter-199): the reckoning lines carry their flows' meanings
    # — the crossing's fund and the chest's service, never bare income
    assert (
        "Ketta comes by 2 coin at the year's reckoning — the toll's net"
        " surplus, the punt fund climbing toward the punt's twelve." in tale
    )
    assert (
        "Malby, the market town comes by 4 coin at the year's reckoning —"
        " the guild's standing take, the flood paper's service at the chest."
        in tale
    )
    # the ambient family stays canon without a line (the committed form)
    assert "The weather turns" not in tale


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the flows ride the macro year
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


def test_the_fold_holds_the_co_due_limit(tmp_path: Path) -> None:
    """D-182's named constraint, answered by construction: the
    toll-surplus flow and the guild's collection NEVER share an account
    (both sources — the fold), so no crossing desyncs at the commit
    gate. The twin walks the first three crossings: the levels climb
    exactly, the events in declaration order, the take outweighing the
    net two-to-one — ONE COIN, TWO CLAIMS as live account state.
    iter-186's camp flow rides the same crossings on its own account —
    the crossing's two filtered to their own ids here (the camp's climb
    pinned in tests/test_campaccount.py)."""
    events, _ = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "armed.jsonl", 42,
        [{"intent": "wait", "ticks": 1500}],
    )
    assert [
        (e.t, e.outcome["flow"], e.state_changes[0].entity,
         e.state_changes[0].from_, e.state_changes[0].to_)
        for e in events if e.type == SOURCE_EVENT
        and e.outcome["flow"] in ("the_toll_nets", "the_guild_collects")
    ][:6] == list(EXPECTED_CLIMB)


def test_the_households_arithmetic_is_legible(tmp_path: Path) -> None:
    """The changed-next-decision unit, as numbers: after the twin's
    crossings the projection holds the household's surplus climbing
    two a year (the punt fund's arc — the authored twelve six thin
    years out) against the chest's four (the paper's standing service,
    the authored twenty five honest years if amortized — the block's
    notes the arithmetic's only mirror)."""
    pack = load_pack(_twin(tmp_path, "armed"))
    sim = Simulator(pack, 42, tmp_path / "legible.jsonl", SCHEMA,
                    commit="0000000")
    sim.run_playscript({
        "name": "legible", "seed": 42, "pack": "province_pack@0.1",
        "steps": [{"intent": "wait", "ticks": 1500}],
    })
    assert sim.projection[KETTA]["account.coin"] == 10  # 2 + 2x4
    assert sim.projection[CHEST]["account.coin"] == 56  # 40 + 4x4
    sim.close()


def test_the_fingerprint_never_sees_the_economy(tmp_path: Path) -> None:
    """INV-2's both-arms proof (the iter-83 measurement form): the
    armed twin against the COMPLETE unarmed twin (the block and the
    stocks ablated together) — the fingerprints EQUAL (the flows draw
    nothing, pure stock reads) and the event lists identical outside
    the account events (the delta is the economy alone)."""
    armed_events, armed = _run_pack(
        _twin(tmp_path, "armed"), tmp_path, "a.jsonl", 42,
        [{"intent": "wait", "ticks": 1500}],
    )
    unarmed_events, unarmed = _run_pack(
        _twin(tmp_path, "unarmed", armed=False), tmp_path, "u.jsonl", 42,
        [{"intent": "wait", "ticks": 1500}],
    )
    assert armed.fingerprint == unarmed.fingerprint
    strip = lambda es: [  # noqa: E731
        (e.t, e.type) for e in es if e.type != SOURCE_EVENT
    ]
    assert strip(armed_events) == strip(unarmed_events)


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
