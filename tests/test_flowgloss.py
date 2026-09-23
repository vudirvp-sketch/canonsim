"""rs-4 — the economy flow-gloss boundary (iter-199, the owner's
«продолжай работу» continuation call firing STATUS Next step item 1 —
the covering residue's future row, the arc's assembly): the economy
FLOW's meaning on the reader surface, the rs family's fourth member —
rs-1's token-mapping shape (a machine token -> reader prose at ONE
boundary, every consumer), rs-2's pack-table shape one granularity
deeper (the kind table glossed the KIND; this table glosses the FLOW).

The residues this row answers (the probes' measured findings,
WORLD_TESTS §9's W5 entry): the biography re-run's residue — "the
COVERING only partially connected in both readings (the +3 reckonings
read as periodic income)"; the humor re-run's residue — "the fund's
climb, the heap's meaning, the beam's law never joined as one frame".
The boundary classification (the decomposition law): the canonical
facts PRESENT (the flows' arithmetic committed since campaccount), the
kinds' MEANINGS present since rs-2/rs-3, but the flows' RELATIONS
rendering NOWHERE — "coin" is one kind serving four flows (the punt
fund, the chest's service, the camp's fund, the withhold's margin), so
the kind gloss CANNOT carry the covering; the flow is the relation's
own unit (its id rides the minted event's outcome), and its meaning is
authored (the economy notes' own words — "the debt fund's climb toward
the charcoal paper sixteen").

The fix: the pack-declared `templates.json::flow_glosses` table
(economy flow id -> reader prose — the flow's meaning, authored from
the notes' own words, pinned below), the renderer's boundary mapping
(`render/chronicle.py::gloss_flow` at the account verbs' `{flow}` slot
in `_event_context`, landed BEFORE the outcome loop so the raw machine
id never reaches a template), the verb line's conditional tail
(`{flow? — {flow}}` — the take template's own conditional form), and
the load-time lint closure (`core/packlint/economy.py::
_flow_gloss_table`: keys inside the declared flow ids, values
non-empty strings, the table without the economy block refused as dead
data — rs-2's own law one granularity deeper). The unglossed flow
renders NOTHING (the raw id is a machine token, rs-1's law — the
conditional stays dry, the line byte-identical to the pre-rs-4 form);
the doors' events (the fall, the collection) carry no flow and never
did. The LOG untouched (zero corpus price by construction — the gloss
is read-side only).

rs-6 (iter-202, the owner's queue-order call «withhold -> the
heartbreak probe» firing STATUS Next step item 1 — the one-surface
contradiction, the iter-199/201 measured residue): the withhold's
EMPTY SLOT FILLED — `the_withhold_banks` gains its flow gloss, the row
rs-4 deliberately left unglossed ("the meaning already rides the
kind" — the measured ceiling of that reading: the heap read as
commerce / "careful accounting", never as the camp's ANSWER). The
join the table owed the reader (ANCHOR_REGION §6.4's CONSEQUENCE row,
the authored law's own words: "the camp's answer to a tilted beam is
to be unweighable at it"): the beam's law + the ANSWER frame + the
fund's tie ONE surface — the banking line (the withhold's own
enactment) now reads as the camp refusing the guild's tilted weighing
while the paper is still paid. The mechanism UNCHANGED (rs-4's table,
rs-4's mapping); the LOG untouched.

The claim packet (TEST_PLAN §9):

- Claim: the flow-minted banking lines carry their flows' meanings on
  every reader surface that asserts them (the tale lines + the entity
  view's history lines — one boundary), the covering's join rendered
  (the camp's line reads as the fund's climb toward the paper sixteen,
  never as income); rs-6: the withhold's line carries the ANSWER frame
  (the beam's tilt, the camp's posture, the paper still paid — one
  surface); no unglossed flow, no door-minted event, and no
  foreign pack renders a tail; the raw flow id never renders; the
  state lines' apposition stays kind-level (rs-2's law, unchanged).
- Problem: the W5 covering residue — the probes' readers read the +3
  reckonings as periodic income because the flow's relation rendered
  nowhere (the kind gloss's granularity ceiling); rs-6's own half —
  the one-surface contradiction (iter-199/201, glm n=2): the heap
  read as commerce / "careful accounting", never as the camp's ANSWER
  to the tilted beam — the heap's meaning, the fund's climb, and the
  beam's law never joined one surface.
- Lens(es): the boundary lens (the tale + the entity view, the probe
  package's own surfaces); the fallback lens (unglossed flows,
  door-minted events, table-less packs, foreign logs); the corpus lens
  (the log bytes; the unglossed lines byte-identical to the pre-rs-4
  form).
- Prism: the renderer-level unit over hand-built account_sourced
  events (with/without a flow outcome); the committed re-weigh twin
  (the probe's own chain, seed 42); the crafted lint variants (the
  refusal arms live in test_economy.py).
- Oracle: the rendered texts (the tailed lines at exactly the glossed
  flows' surfaces; the dry lines byte-identical); the golden log
  bytes.
- Falsifier: a glossed flow rendering dry; an unglossed flow or a
  door-minted event rendering a tail; the raw flow id reaching the
  reader; a state line gaining a flow apposition; the smoke fixture's
  bytes shifting; a dead flow-gloss row passing the load.
- Expected evidence: the year block's three coin lines carrying their
  tails ("...at the year's reckoning — the toll's net surplus...",
  "...— the guild's standing take...", "...— the honest year's
  surplus, the debt fund climbing toward the paper sixteen"); rs-6:
  the withhold's bloom line carrying its tail beside the kind gloss
  ("...— the camp's answer to a tilted beam: unweighable at it, the
  paper still paid."); the fall's and
  the collection's lines dry.
- Observed evidence: CONFIRMED at the deterministic band (seed 42:
  the calendar year run + the re-weigh twin); the probe's re-run rides
  this iteration's record (WORLD_TESTS §9's W5 entry).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues: the shave -> starvation
  ARC's discovery-path half — the voice exemplar sits in the brief,
  the flow glosses join the arithmetic, the reader's assembly is the
  probe's own measure; the withhold's own joke — the frame's material
  now present, the joke stays the reader's act; the state lines' coin
  apposition stays dry by rs-2's law — a per-ACCOUNT gloss would be a
  new granularity, this row's scope deliberately excludes it).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.fold import fold, initial_projection
from core.log import EventRecord, read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from render.chronicle import gloss_flow, render_chronicle, render_entity_view

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

MASTER = "npc_smelter_01"
CHEST = "loc_malby"
CROFTS = "loc_crofts"
SOURCE_EVENT = "account_sourced"
PAPER = 16

#: The three committed flow glosses (the economy notes' own words,
#: pinned so a re-wording is a deliberate act, never drift — rs-2's
#: own pinning law).
TOLL_GLOSS = (
    "the toll's net surplus, the punt fund climbing toward the punt's twelve"
)
CHEST_GLOSS = (
    "the guild's standing take, the flood paper's service at the chest"
)
NETS_GLOSS = (
    "the honest year's surplus, the debt fund climbing toward the paper sixteen"
)
#: The withhold's flow gloss (rs-6, iter-202 — the one-surface
#: contradiction's join: ANCHOR_REGION §6.4's CONSEQUENCE row, the
#: authored law's own words; pinned the same law, a re-wording is a
#: deliberate act).
WITHHOLD_GLOSS = (
    "the camp's answer to a tilted beam: unweighable at it, the paper"
    " still paid"
)


# -- the helpers ----------------------------------------------------------------


def _twin(tmp_path: Path, name: str) -> Path:
    """The crafted short-cadence twin (charcoalpaper's own form): the
    committed pack with the macro year shrunk to 480 ticks — the
    re-weigh chain measured in minutes, not megaticks."""
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


def _reweigh(pack_dir: Path, tmp_path: Path, name: str) -> tuple[list, Any]:
    """The probe's own chain (iter-190's instrument, the sparse form):
    the tally read -> the walks to Malby -> the fifth crossing covering
    the paper -> the FALL -> the COLLECTION -> the aftermath."""
    pack = load_pack(pack_dir)
    log = tmp_path / name
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": 42, "pack": "province_pack@0.1",
        "steps": [
            {"intent": "read_tally", "actor": MASTER, "target": "camp_tally_01"},
            {"intent": "move", "actor": MASTER, "target": "loc_keep"},
            {"intent": "move", "actor": MASTER, "target": CHEST},
            {"intent": "wait", "ticks": 1700},
            {"intent": "reckon_paper", "actor": MASTER},
            {"intent": "render_fund", "actor": MASTER, "target": CHEST},
            {"intent": "wait", "ticks": 10},
        ],
    })
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, pack


def _source(t: int, flow: str | None, kind: str, amount: int) -> EventRecord:
    """One account_sourced event — the flow-minted shape (outcome
    carrying the flow id) when `flow` is given, the door-minted shape
    (no flow key) when it is not: the renderer-level unit's two arms."""
    outcome: dict[str, Any] = {"kind": kind, "amount": amount}
    if flow is not None:
        outcome["flow"] = flow
    return EventRecord(
        id=f"ev_{t:04d}", t=t, type=SOURCE_EVENT, actor="world",
        target=MASTER, cause=None,
        outcome=outcome,
        knowledge=(), state_changes=(), hooks=(), importance="medium",
        provenance={"seed": 42},
    )


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


# -- the boundary units (the renderer-level arm) ---------------------------------


def test_the_gloss_lookup_shapes() -> None:
    """The mapping's own arithmetic: the table's flow -> its prose; an
    unglossed flow -> EMPTY (never the raw id — the machine-token law,
    rs-1's own family shape one member on); a table-less pack -> EMPTY;
    a malformed row inert (the lint owns the refusal, the render never
    crashes mid-line)."""
    pack = load_pack(PACK_DIR)
    assert gloss_flow(pack.templates, "the_toll_nets") == TOLL_GLOSS
    assert gloss_flow(pack.templates, "the_guild_collects") == CHEST_GLOSS
    assert gloss_flow(pack.templates, "the_bloom_nets") == NETS_GLOSS
    assert (
        gloss_flow(pack.templates, "the_withhold_banks") == WITHHOLD_GLOSS
    )
    tavern = load_pack(REPO / "content" / "tavern_pack")
    assert gloss_flow(tavern.templates, "the_toll_nets") == ""
    malformed = {"flow_glosses": {"the_toll_nets": "", "coin": 3}}
    assert gloss_flow(malformed, "the_toll_nets") == ""
    assert gloss_flow(malformed, "coin") == ""


def test_the_verb_line_carries_the_flow_meaning() -> None:
    """The banking line's conditional tail: the flow-minted event
    carries its flow's meaning; the door-minted event (no flow key)
    renders the DRY line, byte-identical to the pre-rs-4 form; the raw
    flow id NEVER renders (the unglossed flow's line stays dry too —
    the machine token never reaches the reader)."""
    pack = load_pack(PACK_DIR)
    tailed = render_chronicle(
        [_source(100, "the_bloom_nets", "coin", 3)], pack, seed=42
    )
    assert (
        "Garrick comes by 3 coin at the year's reckoning — "
        f"{NETS_GLOSS}." in tailed
    )
    dry = render_chronicle([_source(100, None, "coin", 3)], pack, seed=42)
    assert "Garrick comes by 3 coin at the year's reckoning." in dry
    unglossed = render_chronicle(
        [_source(100, "the_dead_flow", "coin", 3)], pack, seed=42
    )
    assert "the_dead_flow" not in unglossed
    assert "Garrick comes by 3 coin at the year's reckoning." in unglossed


def test_the_foreign_pack_lines_stay_dry() -> None:
    """The other packs' surfaces untouched: the grim pack's own verb
    line carries no flow slot and no table — the line byte-identical
    (the corpus lens: no foreign pack shifts a rendered byte)."""
    grim = load_pack(REPO / "content" / "grim_pack")
    tale = render_chronicle(
        [_source(100, "the_toll_nets", "coin", 1)], grim, seed=42
    )
    assert "comes by 1 coin." in tale
    assert NETS_GLOSS not in tale and TOLL_GLOSS not in tale


# -- the committed surface (the probe's own chain) -------------------------------


def test_the_year_block_carries_the_covering_frame(tmp_path: Path) -> None:
    """The committed year run (the calendar experiment's own script):
    the tale's reckoning lines carry their flows' meanings — the
    covering JOINED (the camp's line reads as the fund's climb toward
    the paper, the chest's as the papers' service, the crossing's as
    the punt fund), rs-6: the withhold's bloom line carries the
    ANSWER frame (the heap never reading as commerce — the beam's tilt,
    the camp's posture, and the paper's payment one surface)."""
    events, pack = _run_script(
        tmp_path, "year.jsonl", 42,
        REPO / "tests" / "playscripts" / "province_calendar.json",
    )
    tale = render_chronicle(events, pack, seed=42)
    assert (
        "Ketta comes by 2 coin at the year's reckoning — "
        f"{TOLL_GLOSS}." in tale
    )
    assert (
        "Malby, the market town comes by 4 coin at the year's reckoning"
        f" — {CHEST_GLOSS}." in tale
    )
    assert (
        "Garrick comes by 3 coin at the year's reckoning — "
        f"{NETS_GLOSS}." in tale
    )
    # rs-6 (iter-202): the withhold's own line carries the join — the
    # kind gloss (the heap's meaning, rs-3/5) + the flow gloss (the
    # beam's tilt, the ANSWER frame, the paper still paid) one surface
    assert (
        "the smelt crofts comes by 2 bloom kept off the weighbeam"
        " since the guild factor shaved the camp's weight"
        f" at the year's reckoning — {WITHHOLD_GLOSS}." in tale
    )


def test_the_reweigh_tale_and_records(tmp_path: Path) -> None:
    """The probe's chain over the fixed surface: every banking line
    through the chain carries its flow's tail (the fund's climb visible
    at all five crossings, the covering joined before the fall); the
    DOORS' lines (the fall, the collection) carry no flow and stay dry;
    the close record's STATE lines keep rs-2's kind apposition only
    (the fund's meaning rides the history lines, never the state
    apposition); the entity view's history carries the same tails (one
    boundary, every consumer)."""
    events, pack = _reweigh(_twin(tmp_path, "reweigh"), tmp_path, "reweigh.jsonl")
    tale = render_chronicle(events, pack, seed=42)
    assert tale.count(
        "Garrick comes by 3 coin at the year's reckoning — "
        f"{NETS_GLOSS}."
    ) == 5  # all five crossings — the climb visible throughout
    assert "Garrick is rid of 16 paper owed to the guild's chest at" in tale
    assert "Garrick passes 16 coin to Malby, the market town." in tale
    view = render_entity_view(
        events, fold(events, initial_projection(pack.entities)),
        pack, MASTER, seed=42,
    )
    assert view.count(
        "Garrick comes by 3 coin at the year's reckoning — "
        f"{NETS_GLOSS}."
    ) == 5
    assert "  account.paper: 0 — paper owed to the guild's chest at" in view
    assert "  account.coin: 2" in view  # dry — rs-2's apposition law held


def test_the_log_bytes_are_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the flow gloss is read-side only —
    the committed smoke fixture regenerates byte-identically under the
    glossed pack (the flow ids are canon, the table is not)."""
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
