"""iter-66 acceptance — the invented-entity prose floor (`brief/scan.py`;
contract owner `docs/VALIDATION_SPEC.md` §2.1, decision D-095 — the v0.2
refinement family's first landing).

The suite pins the three laws the module declares: the closed-world
manifest (existence, never visibility — a name may be narrated
off-stage), the detection surface (the unambiguous proper-noun position:
mid-sentence capitalized; sentence-initial capitals are grammar, exempt
by law), and the refusal family's shape (the `REFUSED <item> (<reason>)`
protocol, sorted + deduplicated — INV-2). The both-arms corpus pin
(iter-52 pattern): every prose string of the 105-case narrator corpus
scans clean against the committed pack's manifest (FP=0), and the one
designed confabulation probe (`regen_exhaustion_falls_dry` beat 2 —
"a night watchman named Aldric") is caught (recall). The live wiring
lives in `tests/test_mediator.py` (the floor rides the existing regen
ladder through `apply_reply`).
"""

from __future__ import annotations

import json
from pathlib import Path

from brief.scan import (
    INVENTED_ENTITY,
    invented_names,
    name_manifest,
    prose_refusal_lines,
)
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
MANIFEST = name_manifest(PACK)

_CORPUS = json.loads(
    (REPO / "tests" / "fixtures" / "narrator_beats.json").read_text(
        encoding="utf-8"
    )
)


# -- the manifest: the closed world's names --------------------------------------


def test_manifest_is_the_packs_declared_names() -> None:
    """The manifest reads the entity records' display names directly —
    the same fields the brief's entity cards render, one source (INV-3:
    mechanics here, names in pack data). The proper names arrive whole;
    role phrases arrive lowercase and harmless; ids, roles and the pack
    meta display are not names and stay out."""
    assert "Doren" in MANIFEST  # npc_guard_01 — the one proper name
    assert {"Three", "Barrels", "tavern"} <= MANIFEST  # loc_tavern
    assert {"barkeep", "drunkard", "purse", "lamp"} <= MANIFEST
    assert "npc_guard_01" not in MANIFEST  # ids are not names
    assert "TavernSim" not in MANIFEST  # the pack meta display stays out
    assert "Aldric" not in MANIFEST  # the world holds no watchman Aldric


def test_manifest_is_deterministic() -> None:
    assert name_manifest(PACK) == MANIFEST


# -- the detection surface (the position laws) -----------------------------------


def test_floor_flags_mid_sentence_capitalized_unknowns() -> None:
    """The unambiguous position: a capital after a non-boundary is a
    proper noun — the narrator invented it, the document refuses."""
    assert invented_names(
        "The guard watched Marlowe closely.", MANIFEST
    ) == ("Marlowe",)


def test_floor_allows_declared_names_off_stage() -> None:
    """Existence, not visibility: the rotation beat's exact shape — the
    guard is gone from the room (not on any card), the world still
    holds him; the location name rides mid-sentence too. Knowledge-state
    is the leak suite's job, never this floor's."""
    assert invented_names(
        "Doren was gone from the room, walked off to the guard room; "
        "all that stood in the ashes of the Three Barrels was the relief.",
        MANIFEST,
    ) == ()


def test_floor_sentence_initial_is_exempt_by_law() -> None:
    """The declared boundary: English mandates the capital at a sentence
    start, so the position carries no name signal — a single-mention
    sentence-initial unknown passes (bg-7 measures the live gap; any
    extension is gated on those numbers, never on a heuristic word
    list)."""
    assert invented_names("Marlowe poured the ale and left.", MANIFEST) == ()


def test_floor_catches_the_second_sighting() -> None:
    """The common live pattern: a confabulated name usually recurs — any
    mid-sentence occurrence catches it even when the first mention was
    sentence-initial."""
    assert invented_names(
        "Marlowe poured the ale. The guard watched Marlowe leave.", MANIFEST
    ) == ("Marlowe",)


def test_floor_possessives_strip_to_the_stem() -> None:
    assert invented_names(
        "It was Doren's purse, not Marlowe's.", MANIFEST
    ) == ("Marlowe",)


def test_floor_quotes_restart_the_capital_law() -> None:
    """Dialogue: an opening quote is a sentence boundary — quoted
    sentence starts are exempt; a name inside or after quoted speech is
    still mid-sentence and must be declared."""
    assert invented_names(
        '"Nothing now," said Doren. "Watch yourself." The barkeep sighed.',
        MANIFEST,
    ) == ()


def test_floor_the_english_capital_pronoun() -> None:
    assert invented_names("He said I was wrong.", MANIFEST) == ()


def test_floor_dedupes_sorted_deterministic() -> None:
    """INV-2: unique violations, sorted — the tuple is a contract, the
    regen note lines are reproducible in any process."""
    assert invented_names(
        "Marlowe saw Bodkin first. Bodkin had seen Marlowe too, and told "
        "Cheswick everything.",
        MANIFEST,
    ) == ("Bodkin", "Cheswick", "Marlowe")


def test_floor_line_breaks_are_boundaries() -> None:
    """A line start is a sentence start (multi-line prose): the capital
    there is grammar, exempt."""
    assert invented_names(
        "The room held its breath.\nMarlowe leaned on the bar.", MANIFEST
    ) == ()


def test_floor_commas_and_dashes_are_not_boundaries() -> None:
    """A capital after a comma, colon or dash is still mid-sentence —
    still a name signal (deliberately: the teeth stay on the
    unambiguous side only, never on punctuation style)."""
    assert invented_names(
        "Two strangers — Marlowe, and another: Bodkin.", MANIFEST
    ) == ("Bodkin", "Marlowe")


# -- the refusal family -----------------------------------------------------------


def test_refusal_lines_match_the_protocol_shape() -> None:
    assert prose_refusal_lines(("Marlowe",)) == (
        f"REFUSED prose Marlowe ({INVENTED_ENTITY})",
    )


def test_reason_is_the_closed_vocabulary() -> None:
    assert INVENTED_ENTITY == "invented_entity"


# -- the both-arms corpus pin (iter-52 pattern) -----------------------------------


def test_corpus_prose_fp_zero_and_the_designed_probe_caught() -> None:
    """FP arm: every prose string of the 105-case narrator corpus scans
    clean against the committed pack's manifest — the floor never
    refuses a beat the corpus pins (the corpus replay through the REAL
    mediator cycle is `test_mediator.py::test_phase1_regression_set`;
    this pin is the direct scan, both arms measured). Recall arm: the
    one designed confabulation probe — beat 2 of
    `regen_exhaustion_falls_dry`, "a night watchman named Aldric" — is
    caught; its case outcome is unchanged (the refusal rides the same
    regen ladder the contradicted claim did, the exhaustion falls dry
    either way)."""
    flagged: list[tuple[str, int, tuple[str, ...]]] = []
    for case in _CORPUS["cases"]:
        for beat_index, beat in enumerate(case["beats"]):
            prose = beat["reply"].get("prose")
            if not isinstance(prose, str):
                continue
            violations = invented_names(prose, MANIFEST)
            if violations:
                flagged.append((case["name"], beat_index, violations))
    assert flagged == [("regen_exhaustion_falls_dry", 2, ("Aldric",))]
