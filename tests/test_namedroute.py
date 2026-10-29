"""namedroute — the W7 station's named-boundary rendering route
(iter-286, the owner's «точечный и быстрый (read-side only)» call over
iter-284/285's boundary (a): the refusal's institutional cause as a
rendering row — the station's fourth row, the W7 reading band's own
honest boundary routed read-side).

THE NAMED BOUNDARY (WORLD_TESTS §9's W7 entries, the iter-284/285
records — three independent readings across two reader classes, BOTH
declaring the same limit unprompted): the dead door's refusal renders
«tries to coerce — impossible here», and the INSTITUTIONAL CAUSE — the
registry as the leverage authority, the difference between «no lever
minted» and «a coerce ban» — sat beyond the readable surface: the two
mechanisms were indistinguishable from the material (iter-285's own
sharpening: the coerce verb present in BOTH vocabularies — the block
at the intent level, never the grammar level).

THE FIX (rs-13, the gloss-boundary family's thirteenth member — the
rs-2/rs-4 recorded precedents' own shape, zero canon, zero gate, zero
machinery, the LOG untouched by construction): a pack table
`templates.json::rejection_boundaries` — GATE name -> the reader prose
naming the refusing authority — glossed at ONE boundary
(`render/chronicle.py::gloss_rejection_boundary`, the failed_test's
gate segment; unglossed answers EMPTY, the flow-gloss family's
fallback law — the raw machine token never reaching the reader) and
landed as the `boundary` slot BEFORE the generic outcome loop (the
rs-2/rs-4 precedence); the pack's `intent_rejected` line carries the
rs-12-form conditional tail `{boundary? — {boundary}}` — every
consumer (the tale's gated line, the entity view's ungated record)
reads the one slot through the one template, rs-1's one-boundary law.
The load-time lint owns the refusal (the vacuity law: a gloss for a
gate this pack's door can never refuse at is dead data — the armed
`requires` union the vocabulary).

The claim packet (TEST_PLAN §9):

- Claim: the refusal's institutional cause is now READABLE — the
  no-word twin's runner record renders «tries to coerce — impossible
  here — no minted word to lean on», the committed package's runner
  record renders the hold minted and spent («now holds something over
  Garrick … / leans on Garrick — the hold is spent») — the Q5 boundary
  closed at the readable surface: the two mechanisms discriminate by
  PROSE, not by event census alone. Every unchanged surface stays
  byte-stable: the unglossed gates render the standing line, the tale
  gate UNTOUCHED (the refusal never enters the tale — the records
  surface carries the boundary), the unarmed packs load and render
  unchanged (the table optional), the committed corpora byte-identical
  (the templates never enter the log).
- Problem: the named honest boundary of the W7 reading band — a
  rendering miss never proving a substrate lack (the discrimination
  law); the repair a rendering surface, never prose edits, never a
  gate, never machinery (the station's law held).
- Lens(es): the reader-surface boundary (the entity view's ungated
  record — the surface the W7 readers actually read); the
  every-consumer law (one table, one slot, one template); the
  vacuity lint (the armed-gate vocabulary).
- Prism: the C/D pair (the committed JOURNEY against its no-word
  twin — test_negative's own arms, cited, never re-derived); the
  golden corpus's unglossed rejection (the standing line); the lint's
  crafted refusals; the byte-regen (the province smoke).
- Oracle: the rendered text itself (the boundary tail on the D
  record, the hold/spend lines on the C record), the event censuses
  (leverage_gained/coerce/rejections), the load-time PackError, the
  golden fixture bytes.
- Falsifier: the boundary tail on an unglossed gate; the refusal line
  INSIDE the tale (the gate raised); the C record carrying the refusal
  (the lever present — the boundary glossing a live door); the D
  record rendering the hold (the registry not the authority); a dead
  boundary row loading; the unarmed twin failing to load; the golden
  fixture's bytes changing.
- Expected evidence: the D record's tailed refusal, the C record's
  hold-and-spend pair, the golden corpus's standing move-refusal line,
  the two PackErrors, the byte-identical smoke regen.
- Observed evidence: CONFIRMED at the measured band (seed 42, the
  JOURNEY chain's own form).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the reading band's re-measure over the
  surfaced boundary is a future owner call, never this row's scope;
  the disappearance-battery extension to the remaining majors is
  answered NO by the same call — the meso units' drivers already pass
  the anchor's disable test, ANCHOR_REGION §5's own record; the row
  stays available for a NEW major's own arm, never as a re-measure).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

import pytest

from core.fold import fold, initial_projection
from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import PackError, load_pack
from render.chronicle import (
    gloss_rejection_boundary,
    render_chronicle,
    render_entity_view,
)

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"
GOLDEN = REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"

PC = "pc_01"                         # the factor's runner — the coercer
MASTER = "npc_smelter_01"            # Garrick — the word's subject
TALLY = "camp_tally_01"              # the count cut in wood — the read hinge
WORD = "the_camps_word"              # the hidden fact — the registry's third key
KEEP = "loc_keep"
CROFTS = "loc_crofts"

#: The journey chain (test_negative's JOURNEY form — cited, never
#: re-derived): the walk, the night waited out, the tally read (the
#: word's minting path), then the coercion attempt at the master.
JOURNEY: dict[str, Any] = {
    "name": "journey", "seed": 42, "pack": "province_pack@0.1",
    "steps": [
        {"intent": "move", "target": KEEP},
        {"intent": "move", "target": CROFTS},
        {"intent": "wait", "ticks": 400},
        {"intent": "read_tally", "target": TALLY},
        {"intent": "coerce", "target": MASTER},
        {"intent": "wait", "ticks": 10},
    ],
}

D_REFUSAL = "tries to coerce — impossible here — no minted word to lean on."
C_HOLD = "now holds something over Garrick"
C_SPENT = "leans on Garrick — the hold is spent."


# -- the twins (test_negative's divergence-probe form, cited) ----------------------


def _twin(
    tmp_path: Path, name: str, mutate: Callable[[dict[str, Any]], None],
) -> Path:
    """The committed pack with ONE difference — the same probe form the
    battery's own arms ride (never the committed pack itself)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    data = {
        fname: json.loads((target / f"{fname}.json").read_text(encoding="utf-8"))
        for fname in ("actions", "entities", "rules", "templates")
    }
    mutate(data)
    for fname, payload in data.items():
        (target / f"{fname}.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return target


def _no_word(data: dict[str, Any]) -> None:
    """The registry's third key removed (test_negative's own arm): the
    hidden fact unregistered — the read's knowledge write stays."""
    del data["rules"]["secrets"]["tokens"][WORD]


def _run_view(
    pack_dir: Path, tmp_path: Path, name: str,
) -> tuple[list, str, str]:
    """One JOURNEY run + the runner's record + the tale (the seed from
    the script — the same log renders the same bytes)."""
    pack = load_pack(pack_dir)
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, JOURNEY["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(JOURNEY)
    sim.close()
    _, events = read_log(log, SCHEMA)
    projection = fold(events, initial_projection(pack.entities))
    return (
        events,
        render_entity_view(events, projection, pack, PC, JOURNEY["seed"]),
        render_chronicle(events, pack, seed=JOURNEY["seed"]),
    )


# -- THE ROUTE: the named boundary renders, the dead doors discriminate -------------


def test_the_named_boundary_renders_on_the_records_surface(tmp_path: Path) -> None:
    """The route's own row: the no-word twin's runner record carries the
    refusal WITH the institutional cause — «no minted word to lean on»,
    the registry named as the leverage authority in the pack's own
    register (the coerce family's lean/hold vocabulary). The raw
    failed_test token never reaches the reader; the boundary is the
    pack's authored prose at the one gloss boundary."""
    twin = _twin(tmp_path, "no_word", _no_word)
    _, view, _ = _run_view(twin, tmp_path, "dworld")
    assert D_REFUSAL in view
    assert "actor.leverage_over" not in view  # the machine token never leaks


def test_the_dead_doors_discriminate_by_prose(tmp_path: Path) -> None:
    """The Q5 boundary closed at the readable surface: the SAME journey
    over the committed package (C — the word registered) mints the hold
    and spends it; over the no-word twin (D — the registry's key gone)
    the door refuses WITH its institutional cause. The two mechanisms —
    «no lever minted» against «a coerce ban» — were indistinguishable
    from the material at the W7 reading band; the named boundary makes
    the discrimination a PROSE fact, not a census fact alone."""
    events_c, view_c, _ = _run_view(PACK_DIR, tmp_path, "cworld")
    twin = _twin(tmp_path, "no_word", _no_word)
    events_d, view_d, _ = _run_view(twin, tmp_path, "dworld2")

    assert sum(1 for e in events_c if e.type == "leverage_gained") == 1
    assert sum(1 for e in events_c if e.type == "coerce") == 1
    assert C_HOLD in view_c and C_SPENT in view_c
    assert "impossible here" not in view_c          # the door live, no refusal

    assert not [e for e in events_d if e.type == "leverage_gained"]
    assert not [e for e in events_d if e.type == "coerce"]
    assert D_REFUSAL in view_d
    assert C_HOLD not in view_d and C_SPENT not in view_d


def test_the_unglossed_gates_render_the_standing_line() -> None:
    """The dry fallback law over the committed corpus: the golden smoke
    log's own rejection (a move refused at target.adjacent_to — a
    GEOGRAPHIC cause, never an institutional one) renders the standing
    line UNCHANGED — no tail, the bytes the pre-route renderer wrote.
    The unglossed/absent-table forms answer EMPTY at the boundary
    (the flow-gloss family's fallback: the raw token never lands)."""
    pack = load_pack(PACK_DIR)
    _, events = read_log(GOLDEN, SCHEMA)
    projection = fold(events, initial_projection(pack.entities))
    view = render_entity_view(events, projection, pack, "npc_secondhand_01", 42)
    assert "tries to move — impossible here." in view
    assert "no minted word" not in view
    # the boundary function's own fallbacks (the foreign-log law)
    assert gloss_rejection_boundary({}, "actor.leverage_over") == ""
    assert gloss_rejection_boundary(
        {"rejection_boundaries": {}}, "actor.leverage_over"
    ) == ""
    assert gloss_rejection_boundary(pack.templates, None) == ""
    assert gloss_rejection_boundary(pack.templates, "actor.leverage_over") == (
        "no minted word to lean on"
    )


def test_the_tale_gate_stays_the_boundary_rides_the_records(
    tmp_path: Path,
) -> None:
    """The station's law held: no gate raised. The refusal is low-importance
    canon (a no-op attempt) and the province tale gate stays medium — the
    boundary NEVER enters the tale; it rides the RECORDS surface (the
    ungated per-entity history, the surface the W7 kit's readers actually
    read). The same template serves both consumers: a pack that ever gates
    rejections into its tale gets the boundary through the one slot."""
    twin = _twin(tmp_path, "no_word", _no_word)
    _, view, tale = _run_view(twin, tmp_path, "dworld3")
    assert "impossible here" not in tale
    assert D_REFUSAL in view
    pack = load_pack(PACK_DIR)
    assert pack.templates["tale_gate"] == {"min_importance": "medium"}


# -- THE LINT: the vacuity law at the door -----------------------------------------


def test_the_lint_refuses_dead_boundary_data(tmp_path: Path) -> None:
    """The table's load-time floor (the rs-2/rs-4 family law): a gloss
    for a gate this pack's door can never refuse at is dead data — the
    engine-known-but-never-armed gate (trait_held — the province arms
    no belief gate) and the outright unknown gate both refuse; a
    non-string or empty gloss refuses (the line renders it verbatim).
    The well-formed table loads — and the UNARMED twin (the table
    removed) loads too: the block is optional, the standing refusal
    line the fallback (the other packs' bytes untouched)."""
    def _dead_gate(data: dict[str, Any]) -> None:
        data["templates"]["rejection_boundaries"] = {
            "trait_held": "no belief to lean on",
        }

    def _unknown_gate(data: dict[str, Any]) -> None:
        data["templates"]["rejection_boundaries"] = {
            "no_such_gate": "no such authority",
        }

    def _empty_gloss(data: dict[str, Any]) -> None:
        data["templates"]["rejection_boundaries"] = {"leverage_over": "  "}

    def _non_string(data: dict[str, Any]) -> None:
        data["templates"]["rejection_boundaries"] = {"leverage_over": 42}

    def _unarmed(data: dict[str, Any]) -> None:
        del data["templates"]["rejection_boundaries"]

    for name, mutate in (
        ("dead_gate", _dead_gate),
        ("unknown_gate", _unknown_gate),
        ("empty_gloss", _empty_gloss),
        ("non_string", _non_string),
    ):
        twin = _twin(tmp_path, f"lint_{name}", mutate)
        with pytest.raises(PackError):
            load_pack(twin)

    unarmed = _twin(tmp_path, "unarmed", _unarmed)
    load_pack(unarmed)  # the optional law: the table absent, loads
    # the unarmed + no-word twin: the boundary table gone with the
    # registry key — the refusal renders the STANDING line (the dry
    # fallback), never the authored cause
    twin = _twin(tmp_path, "no_word_unarmed", lambda d: (_no_word(d), _unarmed(d)))
    _, view, _ = _run_view(twin, tmp_path, "dworld_unarmed")
    assert "tries to coerce — impossible here." in view
    assert "no minted word" not in view


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the route is read-side only — the
    gloss, the slot and the template tail never enter the log; the
    golden T1 fixture regenerates byte-identical."""
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_smoke.json"
    )
    log = tmp_path / "smoke.jsonl"
    sim = Simulator(load_pack(PACK_DIR), script["seed"], log, SCHEMA,
                    commit="0000000")
    sim.run_playscript(script)
    sim.close()
    assert log.read_bytes() == GOLDEN.read_bytes()
