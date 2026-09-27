"""grudgesurface — rs-9, the runner's grudge discovery surface (iter-267,
the W5 owner disposition's first row — the standing order's first surface:
ADD DISCOVERY SURFACE, the runner's grudge, "the minimal causal surface
only: standing → the remembered incident → why the grudge exists, never
the biography"; the live band's iter-208 datum the tipping evidence).

THE MEASURED GAP (WORLD_TESTS §9's W5 entry, the iter-208 record): the
human reader noticed the runner's standing hold over Garrick — the tale's
leverage line ("the factor's runner now holds something over Garrick") —
but its REASONS and CONSEQUENCES carried nowhere: the hold's content (the
camp's word) is a MACHINE TOKEN that rendered on no reader surface, and
the causal arc the canon holds (the guild factor's shave two seasons
back → the starved winter → the withhold as the camp's answer → the
audit's tally read → the hold) never transferred to the reader. The rs-1
disposition had named this exact boundary — "the read-hinge secrets
render dry as-is by design; their rendering quality is the probe's
boundary to name, never a preemptive renderer feature" — and the owner's
2026-09-27 disposition opened the row (TASKS' iter-266 record).

THE FIX (the rs family's ninth member, the account/flow gloss boundary's
own shape): the hold's line carries the pack-authored causal row —
ONE table row (templates.json::knows, the_camps_word → the reader
prose: the standing, the incident, the why) + ONE line arm (the
leverage line's conditional tail "{secret? — {secret}}", the banking
lines' "{flow? — {flow}}" tail's own shape) + the boundary extension
(render/chronicle.py: the outcome's `secret` key rides the KNOWS
boundary — rs-1's law, one table, every consumer: the telling path,
the witness path, now the hold path). Zero canon change (the token is
the canon, the gloss is read-side), zero core semantics, the LOG
untouched by construction.

The claim packet (TEST_PLAN §9):

- Claim: the grudge's standing renders its story READ-SIDE — the
  leverage line's tail carries the minimal causal row (the hold's
  content → the shave's incident → the withhold's why) whenever the
  pack authors the secret's gloss; every unglossed secret renders the
  DRY standing unchanged (the machine token never reaching the
  reader), the committed corpora included; the row rides the SAME
  boundary as the telling path (one table, every consumer).
- Problem: the iter-208 discovery-path residue — a standing that
  renders while its story does not (the reader cannot assemble WHY
  the runner holds what he holds or WHERE it came from).
- Lens(es): the reader-surface boundary (the tale's hold line); the
  changed-next-decision unit (the reader holding the tale now assembles
  the grudge's cause chain in one line — the count the proof, the
  shave the origin, the withhold the answer); the boundary's
  every-consumer law (a rumor carrying the word renders the same row).
- Prism: the renderer-level unit (hand-built leverage events: a
  glossed secret, an unglossed secret, no secret); the live re-weigh
  lever chain (seed 42, the day arm and the night arm — the partial
  fidelity's hold the same word); the committed grim fixture (the
  unglossed law over a real corpus: its leverage event's secret
  carries no gloss row); the byte-regen (the province smoke).
- Oracle: the rendered tale text (the row's cells present on the
  glossed line; the dry line for the unglossed; no raw token
  substring; the fixture bytes equal).
- Falsifier: the raw token on the reader surface; the dry standing
  for the glossed hold; the grim fixture's line gaining a tail; the
  province fixture's bytes changing; the twin byte-shifting.
- Expected evidence: the lever chain's tale line carrying the row's
  three cells; the grim fixture's dry line; the byte-identical
  regen; the byte-identical twin.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  day and night arms, the grim fixture, the smoke regen, the twin).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the honest residues: the row is the CAUSAL
  surface only — the temporal placement is the NEXT row's own
  material, the shave's dated-memory surface, the standing order's
  second row; the other three read-hinge secrets stay unglossed —
  each its own row's call on the owner's voice, never a silent
  scope creep; the surface is the TALE's line — the brief's
  recalled-facts token stays dry, the brief's own law).
"""

from __future__ import annotations

import json
from pathlib import Path

from core.log import EventRecord, read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from render.chronicle import chronicle_from_log, render_chronicle

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

PC = "pc_01"
MASTER = "npc_smelter_01"
TALLY = "camp_tally_01"
WORD = "the_camps_word"

#: The row's three cells as substring anchors — the standing (the hold's
#: content), the remembered incident (the shave, the starved winter),
#: the why (the withhold, the bloom off the weighbeam since).
_ROW_CELLS = (
    "the camp's word",
    "the honest count cut in the tally",
    "the guild factor shaved the camp's weight two seasons back",
    "the camp starved that winter",
    "the bloom has sat off the weighbeam since",
)

#: The re-weigh lever chain (tallyread's own DAY_CHAIN + the corner):
#: the walk up-country, the night out, the morning read, the hold
#: spent at the crofts — the grudge surface's own walk.
LEVER_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": "loc_crofts"},
    {"intent": "wait", "ticks": 400},
    {"intent": "read_tally", "target": TALLY},
    {"intent": "coerce", "target": MASTER},
)
#: The night twin: the walk itself lands at night, the read stepping
#: the word down to partial — the hold the same word, learned darker.
NIGHT_CHAIN: tuple[dict, ...] = (
    {"intent": "move", "target": "loc_keep"},
    {"intent": "move", "target": "loc_crofts"},
    {"intent": "read_tally", "target": TALLY},
)
SEED = 42


def _run(tmp_path: Path, name: str, steps: tuple[dict, ...]) -> str:
    """One chain over the committed pack, the tale rendered from its
    own log — the reader's own surface, the same (log, pack) → the
    same bytes (the read-side twin law)."""
    pack = load_pack(PACK_DIR)
    log = tmp_path / name
    sim = Simulator(pack, SEED, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": SEED, "pack": "province_pack@0.1",
        "steps": [dict(step) for step in steps],
    })
    sim.close()
    return chronicle_from_log(log, pack, SCHEMA)


def _hold_event(secret: str | None, t: int = 100) -> EventRecord:
    """One medium-importance leverage mint carrying the secret — the
    hold's own event shape (the live mint's outcome keys)."""
    outcome: dict = {
        "type": "debt", "fidelity": "exact", "expires_at": t + 129600,
    }
    if secret is not None:
        outcome["secret"] = secret
    return EventRecord(
        id=f"ev_{t:04d}", t=t, type="leverage_gained", actor=PC,
        target=MASTER, cause=None, outcome=outcome,
        knowledge=(), state_changes=(), hooks=(), importance="medium",
        provenance={"seed": SEED},
    )


# -- the census (the authored surface as pack data) ------------------------------


def test_the_pack_authors_the_row() -> None:
    """The surface's pack half: ONE knows row (the secret token → the
    causal-row prose) + the line's conditional tail — the words live in
    the pack, the boundary in the renderer (rs-1's own law: the pack
    owns the words, the renderer owns the mapping)."""
    pack = load_pack(PACK_DIR)
    row = pack.templates["knows"].get(WORD)
    assert isinstance(row, str) and row.strip()
    for cell in _ROW_CELLS:
        assert cell in row, f"the row lost a causal cell: {cell!r}"
    line = pack.templates["events"]["leverage_gained"]
    assert line == "{actor} now holds something over {target}{secret? — {secret}}."


# -- the live chain (the surface over the re-weigh's own walk) --------------------


def test_the_hold_line_carries_the_causal_row(tmp_path: Path) -> None:
    """The changed-next-decision unit, live: the reader holding the
    re-weigh tale assembles the grudge's story in one line — the
    standing (the hold's content: the camp's word, the honest count),
    the remembered incident (the guild factor's shave, two seasons
    back, the starved winter), the why (the withhold: the bloom off
    the weighbeam since) — the iter-208 residue's transfer landed."""
    tale = _run(tmp_path, "lever.jsonl", LEVER_CHAIN)
    hold = [ln for ln in tale.splitlines() if "holds something over" in ln]
    assert len(hold) == 1
    line = hold[0]
    assert line.startswith("the factor's runner now holds something over Garrick — ")
    for cell in _ROW_CELLS:
        assert cell in line, f"the tale's hold line lost a cell: {cell!r}"
    # the consequences ride their own lines (the corner + the pair the
    # brief's own surface): the standing's row, never the biography
    assert "the factor's runner leans on Garrick — the hold is spent." in tale


def test_the_night_arm_carries_the_same_row(tmp_path: Path) -> None:
    """The partial-fidelity hold the same word: the walk lands at
    night, the read mints the word PARTIAL (half the notches legible)
    — the cluster records how well, the STORY unchanged (the row is
    the token's meaning, not the knower's acuity)."""
    tale = _run(tmp_path, "night.jsonl", NIGHT_CHAIN)
    hold = [ln for ln in tale.splitlines() if "holds something over" in ln]
    assert len(hold) == 1
    for cell in _ROW_CELLS:
        assert cell in hold[0]


def test_the_twin_renders_byte_identical(tmp_path: Path) -> None:
    """The read-side determinism law: the same (log, pack) renders the
    same tale bytes — the gloss is a pure mapping, never a draw."""
    first = _run(tmp_path, "twin_a.jsonl", LEVER_CHAIN)
    second = _run(tmp_path, "twin_b.jsonl", LEVER_CHAIN)
    assert first == second


# -- the boundary law (one table, every consumer; the dry fallback) ---------------


def test_the_unglossed_secret_renders_the_dry_standing() -> None:
    """The unglossed law (the flow family's own fallback): a secret
    with no table row pre-seeds EMPTY — the raw machine token never
    reaches the reader, the line renders the dry standing exactly as
    it always did. The renderer never invents a foreign log's story."""
    pack = load_pack(PACK_DIR)
    events = [_hold_event("a_secret_with_no_row")]
    tale = render_chronicle(events, pack, seed=SEED)
    assert tale.splitlines() == [
        "— Day 1, Morning —",
        "the factor's runner now holds something over Garrick.",
    ]
    assert "a_secret_with_no_row" not in tale


def test_the_secretless_hold_renders_the_dry_standing() -> None:
    """The absent-secret arm: an outcome with no secret key (a foreign
    emitter's shape) renders the dry line — the tail's conditional
    reads the pre-seeded slot, never the outcome's raw payload."""
    pack = load_pack(PACK_DIR)
    tale = render_chronicle([_hold_event(None)], pack, seed=SEED)
    lines = tale.splitlines()
    assert "the factor's runner now holds something over Garrick." in lines


def test_the_row_rides_the_telling_path_too() -> None:
    """rs-1's every-consumer law: the SAME row glosses the token
    wherever it rides — a rumor carrying the camp's word renders the
    causal prose in the telling line (one boundary, one table, every
    consumer: the telling path, the witness path, the hold path)."""
    pack = load_pack(PACK_DIR)
    rumor = EventRecord(
        id="ev_0200", t=200, type="rumor_told", actor=PC,
        target="npc_marketmistress_01", cause=None,
        outcome={"accepted": True, "score": 60, "knows": WORD,
                 "fidelity": "partial"},
        knowledge=(), state_changes=(), hooks=(), importance="medium",
        provenance={"seed": SEED},
    )
    tale = render_chronicle([rumor], pack, seed=SEED)
    assert "the factor's runner tells Maren: " in tale
    for cell in _ROW_CELLS:
        assert cell in tale
    assert WORD not in tale  # the token itself never survives the boundary


# -- the corpus laws (the committed corpora's price) ------------------------------


def test_the_grim_fixture_renders_the_dry_standing() -> None:
    """The unglossed law over a COMMITTED corpus: the grim fixture's
    leverage event (its secret carrying no province row — and its own
    pack's table none either) renders the dry line with no tail, and
    the spend event's outcome (the same key family) renders its own
    line untouched — the committed tales' price zero."""
    pack = load_pack(REPO / "content" / "grim_pack")
    tale = chronicle_from_log(
        REPO / "tests" / "fixtures" / "grim_smoke_seed42.jsonl", pack, SCHEMA
    )
    hold = [ln for ln in tale.splitlines() if "holds something over" in ln]
    assert hold == ["the player now holds something over the serving maid."]
    assert "scraps_pawned_by_maid" not in tale
    assert "corners the serving maid — the hold is spent, and both know it." in tale


def test_the_log_bytes_are_untouched_by_the_row(tmp_path: Path) -> None:
    """The zero-corpus-price law (the template family's own): the row
    and the line arm are read-side only — the committed smoke fixture
    regenerates BYTE-IDENTICAL under the glossed pack (the tokens are
    canon, the table is not; the runtime bytes never see a template)."""
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
    _header, events = read_log(log, SCHEMA)
    assert not [e for e in events if e.type == "leverage_gained"]
