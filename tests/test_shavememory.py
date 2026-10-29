"""shavememory — rs-10, the shave's temporal surface (iter-268, the W5
owner disposition's ADD TEMPORAL SURFACE row — the standing order's
second surface: "the dated-memory row, the chain earlier season →
hunger winter → the event → present consequence, currently read as
present unfairness with the temporal anchor lost — the arc's
assembly's remaining half, the iter-201/202 measured open row; the
residue ladder's own EVENT → RESIDUE → CARRIER → HOLDER rungs,
WORLD_AUTHORING §8, requiring the transition between historical
states").

THE MEASURED GAP (WORLD_TESTS §9's W5 entry, the iter-201/202
records): the shave's TEMPORAL placement never assembled — the shave
read as the year's present injustice or a vague background, never the
two-seasons-back living memory with the starved winter between.
Reading 2 conflated the shave with the present weighing ("the guild
'comes to the smelt crofts'"); reading 1's own uncertainty note: "the
exact nature of the dispute ... remains uncertain". The canonical
facts were PRESENT since rs-3/5 (the shave named, the direction
correct) — what rendered nowhere was the DATE: the withhold's banking
line carried "since the guild factor shaved the camp's weight" with no
anchor, and the winter lived only inside the paper gloss's "since the
starved winter", unconnected to the shave.

THE FIX (the rs family's tenth member, the rs-5 precedent's own form —
the SAME table row re-authored, the mechanism unchanged): the bloom
kind gloss now carries the DATED MEMORY — the spine's own full
sentence plus its date (entities.json: "the guild factor shaved the
weight two seasons back and the camp starved") and the ledger tail
("the withhold's own ledger", freightvol's own concept — the heap as
the withhold's record, and the NOUN the banking template's fixed "at
the year's reckoning" attaches to, keeping the starvation clause clear
of the reckoning phrase). The chain on one line: earlier season (the
shave, dated) → hunger winter (the camp starved that winter) → the
withhold since → the present ledger. Zero code, zero canon change, the
LOG untouched, zero corpus price (the iter-265 template law: a template
changes no runtime byte).

The claim packet (TEST_PLAN §9):

- Claim: the withhold's own line (the banking line, the state
  apposition, the entity view's history — one boundary, every
  consumer) carries the dated chain — the shave DATED "two seasons
  back", the starvation winter named BETWEEN the shave and the present
  practice, the withhold's ledger the present consequence; the paper
  gloss's "since the starved winter" now anchors to the SAME winter
  through the shared name, the arc assembling ACROSS the tale's own
  lines.
- Problem: the iter-201/202 measured open row — the temporal anchor
  lost, the shave read as present unfairness (never the living
  memory), the arc's assembly broken at its first transition.
- Lens(es): the dated-memory lens (the shave's temporal position on
  the reader surface); the arc-assembly lens (the winter shared
  between the two kind glosses); the regression lens (rs-5's
  direction, rs-6's answer frame, rs-2's paper gloss — all unchanged);
  the misparse lens (the starvation clause never landing at the
  reckoning).
- Prism: the renderer-level unit over the pack row (the census); the
  sparse twin (the re-weigh chain, seed 42 — the probe's own
  instrument); the calendar year run (the freightvol witness's own
  chain); the committed fixtures (the golden bytes).
- Oracle: the rendered texts (the dated chain's cells present on the
  glossed lines; the regression rows verbatim; the misparse adjacency
  absent; the coin lines unchanged); the golden log bytes.
- Falsifier: the date or the winter missing from the glossed lines;
  rs-5's direction clause altered; rs-6's flow gloss changed; the
  paper gloss changed; the starvation clause adjacent to the reckoning
  phrase ("that winter at the year's reckoning" — the misparse the
  ledger tail exists to kill); the coin lines shifting; the smoke
  fixture's bytes changing; the twin byte-shifting.
- Expected evidence: the withhold's banking line carrying "two
  seasons back and the camp starved that winter — the withhold's own
  ledger at the year's reckoning"; the crofts' state apposition the
  same row; the paper gloss unchanged; the smoke fixture
  byte-identical.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  sparse twin, the calendar run, the fixtures, the twin) + the probe's
  re-run (WORLD_TESTS §9's W5 entry — the glm blind reading n=2
  convergent: the shave placed BEFORE the tale's events, the winter
  between, the withhold since).
- Epistemic class: measured, deterministic per seed (the probe reading:
  the LLM band, its own caveat).
- Disposition: CONFIRMED (the honest boundaries: the row dates the
  MEMORY as the camp tells it — the authored constant, never a runtime
  clock read; the debt's BIRTH (the winter's borrowing) stays on the
  paper's own line — the two surfaces chain through the shared winter's
  name, never one bloated row; the brief's recalled-facts token stays
  dry, the brief's own law; the live human band open — the standing
  order's next row reads both surfaces together).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.fold import fold, initial_projection
from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from render.chronicle import render_chronicle, render_entity_view

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

MASTER = "npc_smelter_01"
CHEST = "loc_malby"
CROFTS = "loc_crofts"
SOURCE_EVENT = "account_sourced"

#: The dated-memory row's committed gloss (rs-10, iter-268 — the spine's
#: own sentence plus its date, the ledger tail; pinned so a re-wording is
#: a deliberate act, never drift — the family's own pinning law).
DATED_GLOSS = (
    "bloom kept off the weighbeam since the guild factor shaved"
    " the camp's weight two seasons back and the camp starved that"
    " winter — the withhold's own ledger"
)
#: The regression rows (must not move): rs-2's paper gloss, rs-6's
#: withhold flow gloss.
PAPER_GLOSS = (
    "paper owed to the guild's chest at Malby since the starved winter"
)
WITHHOLD_FLOW_GLOSS = (
    "the camp's answer to a tilted beam: unweighable at it, the paper"
    " still paid"
)
#: The dated chain's cells as substring anchors: the earlier season (the
#: shave's date), the hunger winter (the starvation), the event (the
#: shave — rs-5's direction phrase verbatim), the present consequence
#: (the withhold's ledger).
_ROW_CELLS = (
    "since the guild factor shaved the camp's weight",  # rs-5, verbatim
    "two seasons back",                                  # the date
    "and the camp starved that winter",                  # the hunger winter
    "the withhold's own ledger",                         # the present tail
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


# -- the census (the authored surface as pack data) ------------------------------


def test_the_pack_authors_the_dated_row() -> None:
    """The surface's pack half: ONE kind row re-authored (the rs-5
    precedent's own form — the mechanism unchanged, the words live in
    the pack) — the dated chain's every cell present, the spine's own
    sentence carried, and the regression rows untouched beside it."""
    pack = load_pack(PACK_DIR)
    row = pack.templates["account_kinds"]["bloom"]
    assert row == DATED_GLOSS
    for cell in _ROW_CELLS:
        assert cell in row, f"the row lost a dated-memory cell: {cell!r}"
    # the regression rows verbatim (rs-2's paper, rs-6's withhold flow)
    assert (
        pack.templates["account_kinds"]["paper"] == PAPER_GLOSS
    )
    assert (
        pack.templates["flow_glosses"]["the_withhold_banks"]
        == WITHHOLD_FLOW_GLOSS
    )
    # the spine's own committed sentence is the row's source of record
    entities = json.loads(
        (PACK_DIR / "entities.json").read_text(encoding="utf-8")
    )
    causes = [
        str(n.get("spine", {}).get("cause", ""))
        for n in entities["npcs"]
        if isinstance(n, dict)
    ]
    assert any(
        "shaved the weight two seasons back and the camp starved" in c
        for c in causes
    )


# -- the live chain (the surfaces the probe's readers read) -----------------------


def test_the_banking_line_carries_the_dated_chain(tmp_path: Path) -> None:
    """The changed-next-decision unit, live: the reader holding the
    re-weigh tale reads the withhold's own line AS a dated memory — the
    shave two seasons back, the starved winter between, the withhold's
    ledger the present consequence — the temporal anchor the iter-201/202
    readers lost, restored on the line they actually read."""
    events, pack = _reweigh(_twin(tmp_path, "reweigh"), tmp_path, "reweigh.jsonl")
    tale = render_chronicle(events, pack, seed=42)
    line = (
        f"the smelt crofts comes by 2 {DATED_GLOSS}"
        f" at the year's reckoning — {WITHHOLD_FLOW_GLOSS}."
    )
    assert tale.count(line) == 6  # every crossing — the anchor throughout
    # (ki114-1-impl: six crossings now — the stretched span's boundary
    # count, every step feeding at the post-drain clock; the dated
    # chain's shape intact)
    # the coin lines unchanged (the regression: the flows' meanings)
    assert (
        "Garrick comes by 3 coin at the year's reckoning — the honest"
        " year's surplus, the debt fund climbing toward the paper sixteen."
        in tale
    )


def test_the_state_record_carries_the_dated_chain(tmp_path: Path) -> None:
    """The same row on the probe package's OTHER surface (one boundary,
    every consumer — rs-2's own law): the crofts' close record carries
    the heap's level beside the dated apposition, and the entity view's
    history lines carry the same banking lines with their dates."""
    events, pack = _reweigh(_twin(tmp_path, "reweigh"), tmp_path, "reweigh.jsonl")
    state = fold(events, initial_projection(pack.entities))
    view = render_entity_view(events, state, pack, CROFTS, seed=42)
    assert f"  account.bloom: 16 — {DATED_GLOSS}" in view
    assert f"[t 480] the smelt crofts comes by 2 {DATED_GLOSS}" in view


def test_the_arc_assembles_across_the_tales_lines(tmp_path: Path) -> None:
    """The reader-path unit (the disposition's own chain): the withhold's
    line dates the shave and names the winter; the paper's line anchors
    the debt to the SAME winter's name; the fund's line carries the climb
    toward the paper — the arc earlier season → hunger winter → the
    event's residue → present consequence assembled from the tale's own
    lines, no single surface required to carry it all."""
    events, pack = _reweigh(
        _twin(tmp_path, "reweigh"), tmp_path, "reweigh.jsonl"
    )
    tale = render_chronicle(events, pack, seed=42)
    # the winter's name shared by both kind glosses (the chaining anchor)
    assert "the camp starved that winter" in tale
    assert "since the starved winter" in tale
    # the withhold's line: the dated chain whole
    assert (
        f"the smelt crofts comes by 2 {DATED_GLOSS}"
        f" at the year's reckoning — {WITHHOLD_FLOW_GLOSS}." in tale
    )
    # the paper's line: the debt's discharge beside its own winter anchor
    assert f"Garrick is rid of 16 {PAPER_GLOSS}." in tale


def test_the_starvation_never_lands_at_the_reckoning(tmp_path: Path) -> None:
    """The misparse falsifier: the banking template's fixed \"at the
    year's reckoning\" follows the {kind} slot — a gloss ending in a time
    phrase would weld the starvation to the reckoning (\"the camp starved
    that winter at the year's reckoning\"). The ledger tail exists to
    kill exactly that adjacency; its absence is the failure."""
    events, pack = _reweigh(_twin(tmp_path, "reweigh"), tmp_path, "reweigh.jsonl")
    tale = render_chronicle(events, pack, seed=42)
    assert "that winter at the year's reckoning" not in tale
    assert "starved that winter — the withhold's own ledger at the year's" in tale


# -- the corpus laws (the committed corpora's price) ------------------------------


def test_the_log_bytes_are_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law (the template family's own, iter-265):
    the row is read-side only — the committed smoke fixture regenerates
    BYTE-IDENTICAL under the re-authored pack (the kind names are canon,
    the table is not; the runtime bytes never see a gloss)."""
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


def test_the_twin_renders_byte_identical(tmp_path: Path) -> None:
    """The read-side determinism law: the same (log, pack) renders the
    same tale bytes — the dated row is a pure mapping, never a draw."""
    first, pack = _reweigh(_twin(tmp_path, "a"), tmp_path, "a.jsonl")
    second, same_pack = _reweigh(_twin(tmp_path, "b"), tmp_path, "b.jsonl")
    assert render_chronicle(first, pack, seed=42) == render_chronicle(
        second, same_pack, seed=42
    )


def test_the_dry_packs_and_foreign_kinds_stay_dry() -> None:
    """The fallback laws (rs-1's own family): a foreign kind renders
    its bare word; the packs without a table render their account kinds
    dry — the boundary never invents a dated memory the pack did not
    author, a foreign log's included."""
    from render.chronicle import gloss_account_kind

    pack = load_pack(PACK_DIR)
    assert gloss_account_kind(pack.templates, "iron") == "iron"
    for pack_name in ("grim_pack", "pressure_pack"):
        other = load_pack(REPO / "content" / pack_name)
        assert "account_kinds" not in other.templates
        for kind in ("coin", "coal", "pressure", "bloom"):
            assert gloss_account_kind(other.templates, kind) == kind
