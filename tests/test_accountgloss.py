"""rs-2 — the account-kind gloss boundary (iter-191, the owner's
gate-route call firing STATUS Next step item 1, option (a) — the W5
rendering failure's first half): the account KIND's meaning on the
reader surface, the rs-1 precedent's own shape.

rs-3 (iter-194, the owner's «продолжай работу» continuation call
firing STATUS Next step item 1 — the W5 humor probe's rendering
failure, the rs family's natural third member): the SECOND table
entry, the bloom kind — the withhold's meaning on the reader surface.
The humor probe's finding (iter-192, glm n=2 convergent): the
withhold's MEANING rendered nowhere — the bloom kind carried no gloss
(the dry fallback: the table glossed paper only), the banking lines
read as periodic income, the loads-kept-off-the-beam invisible unless
framed. The fix: ONE table row — the withhold's meaning as reader
prose in the paper gloss's own shape (kind + meaning + origin, the
authored origin the shave — ANCHOR_REGION §6.4's loop H) — the
mechanism itself rs-2's, unchanged: the crofts' state line and the
banking verb lines now carry the meaning. The LOG untouched (zero
corpus price, the same law). The arc's ASSEMBLY stays the covering
residue's own future row (the W5 record's route: the gloss now, the
arc later — the re-run's residues recorded there).

The failure (iter-190's W5 first run, glm n=2 convergent): the reader
did NOT reconstruct the persistent obligation — FAILED at the RENDERING
boundary, the canonical fact PRESENT (both readers saw
`account.paper: 16`), the account kind's meaning rendering NOWHERE:
"16 paper owed" indistinguishable from "16 paper held" (the inventory
reading the symptom), the creditor a location name, the lifecycle doors
two unconnected verb lines. The fix's route (the owner's call, the
natural class): an account-kind gloss on the reader surface — the pack
owns the words (templates.json `account_kinds`: kind -> its reader
prose, a noun phrase headed by the kind word), the renderer owns the
mapping (`render/chronicle.py::gloss_account_kind` at TWO boundaries:
the account verbs' `{kind}` slot in `_event_context` — one boundary,
every consumer: the tale lines + the entity view's history lines — and
the state line's apposition in `_state_lines`). An unglossed kind
renders dry and honest (the foreign-log fallback, rs-1's own family
law); the LOG is untouched — zero corpus price by construction.

The claim packet (TEST_PLAN §9):

- Claim: the account kind's meaning renders on every reader surface
  that asserts it — the state line carries the standing's meaning
  (owed, the creditor, the origin), the account verb lines carry the
  kind's gloss, and no unglossed kind or foreign kind renders prose.
- Problem: the W5 first run's rendering-boundary failure — the
  obligation invisible on the reader surface the probe packaged.
- Lens(es): the boundary lens (the tale + the entity view, the probe's
  own surfaces); the fallback lens (unglossed kinds, foreign logs, the
  table-less packs); the corpus lens (the log bytes, the dry packs'
  renders byte-identical).
- Prism: the renderer-level unit over hand-built account events; the
  committed re-weigh twin (the probe's own chain, seed 42); the
  crafted lint variants (the refusal arms live in test_economy.py).
- Oracle: the rendered texts (the glossed prose present at exactly the
  glossed kinds' surfaces; the dry lines byte-identical to the pre-rs-2
  form); the golden log bytes.
- Falsifier: a glossed kind rendering dry; an unglossed kind rendering
  prose; the fall's line losing its frame; the coin lines shifting
  (the dry control — the bloom lines carry rs-3's gloss by design);
  the smoke fixture's bytes shifting; a dead gloss row passing the
  load.
- Expected evidence: the open record's standing line
  `account.paper: 16 — paper owed to the guild's chest at Malby since
  the starved winter`; the fall line carrying the same gloss; the coin
  lines dry; rs-3: the crofts' heap line and the banking verb lines
  carrying the withhold's gloss (`bloom kept off the weighbeam since
  the shave`).
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  re-weigh twin; rs-3's band: the humor probe's re-run — the mandatory
  bar met, WORLD_TESTS §9's W5 entry).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues: the arc's ASSEMBLY —
  the fund's climb and the covering still render as routine facts,
  the route's second half, each a future row's own design per the W5
  record; the unglossed kinds' rendering quality — coin and the other
  packs' kinds — the dry fallback's own band, never a preemptive
  gloss; the briefs' entity cards carry no account state — the
  model-facing band, PRESENTATION_SPEC's, not this row's surface).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.fold import fold, initial_projection
from core.log import EventRecord, read_log
from core.loop import Simulator
from core.pack import load_pack
from render.chronicle import (
    gloss_account_kind,
    render_chronicle,
    render_entity_view,
)

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

MASTER = "npc_smelter_01"
CHEST = "loc_malby"
CROFTS = "loc_crofts"
PAPER = 16
#: The paper kind's committed gloss (the pack's own words, pinned so a
#: re-wording is a deliberate act, never drift).
PAPER_GLOSS = (
    "paper owed to the guild's chest at Malby since the starved winter"
)
#: The bloom kind's committed gloss (rs-3, iter-194 — the withhold's
#: meaning, pinned the same law: a re-wording is a deliberate act).
BLOOM_GLOSS = "bloom kept off the weighbeam since the shave"


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


def _fall(t: int, kind: str, amount: int) -> EventRecord:
    """One account_consumed event carrying the kind — the renderer-level
    unit's surface (the verb line's `{kind}` slot)."""
    return EventRecord(
        id=f"ev_{t:04d}", t=t, type="account_consumed", actor=MASTER,
        target=None, cause=None,
        outcome={"kind": kind, "amount": amount},
        knowledge=(), state_changes=(), hooks=(), importance="medium",
        provenance={"seed": 42},
    )


# -- the boundary units (the renderer-level arm) ---------------------------------


def test_the_gloss_lookup_shapes() -> None:
    """The mapping's own arithmetic: the table's kind -> its prose; an
    unglossed kind -> the bare kind UNCHANGED (the dry fallback law);
    a table-less pack -> the bare kind; a malformed row inert (the
    lint owns the refusal, the render never crashes mid-line)."""
    pack = load_pack(PACK_DIR)
    assert gloss_account_kind(pack.templates, "paper") == PAPER_GLOSS
    assert gloss_account_kind(pack.templates, "bloom") == BLOOM_GLOSS
    assert gloss_account_kind(pack.templates, "coin") == "coin"
    tavern = load_pack(REPO / "content" / "tavern_pack")
    assert gloss_account_kind(tavern.templates, "coin") == "coin"
    malformed = {"account_kinds": {"paper": "", "coin": 3}}
    assert gloss_account_kind(malformed, "paper") == "paper"
    assert gloss_account_kind(malformed, "coin") == "coin"


def test_the_verb_line_carries_the_gloss() -> None:
    """The account verbs' `{kind}` slot maps through the table — the
    kind's meaning rides the line; every OTHER event family's `kind`
    (the worldgen memory line's collection name) renders raw, the
    scoping law."""
    pack = load_pack(PACK_DIR)
    tale = render_chronicle([_fall(100, "paper", PAPER)], pack, seed=42)
    assert (
        f"Garrick is rid of {PAPER} {PAPER_GLOSS}." in tale
    )
    coin_line = render_chronicle([_fall(100, "coin", 4)], pack, seed=42)
    assert "Garrick is rid of 4 coin." in coin_line
    memory = EventRecord(
        id="ev_0101", t=101, type="world_history", actor="the world",
        target=None, cause=None,
        outcome={"kind": "the feud", "year": 64},
        knowledge=(), state_changes=(), hooks=(), importance="medium",
        provenance={"seed": 42},
    )
    tale = render_chronicle([memory], pack, seed=42)
    assert "the feud" in tale


def test_the_foreign_kind_falls_back_dry() -> None:
    """A foreign log's account kind (no table entry) renders its bare
    word — the renderer never invents a meaning the pack did not
    declare (the foreign-log law, rs-1's own)."""
    pack = load_pack(PACK_DIR)
    tale = render_chronicle([_fall(100, "silver", 5)], pack, seed=42)
    assert "Garrick is rid of 5 silver." in tale


# -- the committed surface (the probe's own chain) -------------------------------


def test_the_standing_renders_its_meaning(tmp_path: Path) -> None:
    """The W5 failure's own surfaces: the OPEN state records (the
    initial projection — the probe's opening records) carry the
    standings' meanings — the debt reads as OWED with its creditor and
    origin, never as inventory; rs-3: the withhold's heap reads as
    iron KEPT OFF the beam, never as stockpiled goods; the unglossed
    fund line stays dry."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    view = render_entity_view([], projection, pack, MASTER, seed=42)
    assert (
        f"  account.paper: {PAPER} — {PAPER_GLOSS}" in view
    )
    assert "  account.coin: 3" in view  # dry — no apposition
    crofts = render_entity_view([], projection, pack, CROFTS, seed=42)
    assert f"  account.bloom: 4 — {BLOOM_GLOSS}" in crofts


def test_the_reweigh_tale_and_records(tmp_path: Path) -> None:
    """The probe's chain over the fixed surface: the fall's line
    carries the debt's frame (the discharge reads as the obligation
    ending, never an exchange); the payment's line stays dry (the coin
    kind unglossed — the creditor connects through the gloss's own
    \"at Malby\"); the close record's zero level beside the owed-gloss
    reads as the obligation discharged; the history's account lines
    carry the same gloss (one boundary, every consumer)."""
    events, pack = _reweigh(_twin(tmp_path, "reweigh"), tmp_path, "reweigh.jsonl")
    tale = render_chronicle(events, pack, seed=42)
    assert f"Garrick is rid of {PAPER} {PAPER_GLOSS}." in tale
    assert "Garrick passes 16 coin to Malby, the market town." in tale
    assert "Garrick comes by 3 coin at the year's reckoning." in tale
    # rs-3: the banking verb lines carry the withhold's meaning — the
    # heap's climb reads as the withhold deepening, never as income
    assert (
        f"the smelt crofts comes by 2 {BLOOM_GLOSS}"
        " at the year's reckoning." in tale
    )
    view = render_entity_view(
        events, fold(events, initial_projection(pack.entities)),
        pack, MASTER, seed=42,
    )
    assert f"  account.paper: 0 — {PAPER_GLOSS}" in view
    assert f"[t 2559] Garrick is rid of {PAPER} {PAPER_GLOSS}." in view
    crofts_view = render_entity_view(
        events, fold(events, initial_projection(pack.entities)),
        pack, CROFTS, seed=42,
    )
    # the withhold's own surface at the close: the heap's level beside
    # its meaning (the probe package's crofts record)
    assert f"  account.bloom: 14 — {BLOOM_GLOSS}" in crofts_view


def test_the_log_bytes_are_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the gloss is read-side only — the
    committed smoke fixture regenerates byte-identically under the
    glossed pack (the kind names are canon, the table is not)."""
    from core.loop import load_playscript

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


def test_the_dry_packs_account_lines_stay_dry() -> None:
    """The corpus law's other arm: the packs WITHOUT a table render
    their account kinds dry — the fallback holds by construction, the
    committed renders byte-stable across the boundary's landing (the
    armed packs' own tale pins carry this in their packets; this census
    pins the law itself over the loaded templates)."""
    for pack_name in ("grim_pack", "pressure_pack"):
        pack = load_pack(REPO / "content" / pack_name)
        assert "account_kinds" not in pack.templates
        for kind in ("coin", "coal", "pressure"):
            if kind in pack.rules.get("economy", {}).get("accounts", ()):
                assert gloss_account_kind(pack.templates, kind) == kind
