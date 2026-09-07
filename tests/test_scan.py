"""iter-66 acceptance — the invented-entity prose floor (`brief/scan.py`;
contract owner `docs/VALIDATION_SPEC.md` §2.1, decision D-095 — the v0.2
refinement family's first landing) + iter-72 — the lowercase assertion
surface (prosefloor-2, D-104: the detection half D-096 routed — the
measurement export for bg-8's weaker-engine arm; no gate, no wiring).

The iter-66 suite pins the three laws the module declares: the closed-world
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

The iter-72 suite pins the surface's declared boundaries (the two
assertion slots, the adjectival exclusion, the contraction path) and
the corpus calibration baseline — the single owner of the split
numbers (D-024): the exact surface tuple, the exact grounded subset,
and the honest headline that clean operator narration already rides
mostly unmodeled assertion tokens (the number that says no refusal
ladder may be built on this surface without bg-8's numbers).
"""

from __future__ import annotations

import json
from pathlib import Path

from brief.scan import (
    INVENTED_ENTITY,
    invented_names,
    modeled_vocabulary,
    name_manifest,
    prose_refusal_lines,
    relation_attribute_tokens,
)
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
MANIFEST = name_manifest(PACK)
VOCAB = modeled_vocabulary(PACK)

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


# -- iter-72: the lowercase assertion surface (prosefloor-2, D-104) ---------------

#: The committed corpus's calibration baseline — pinned exact, the single
#: owner of the split numbers (D-024): every lowercase token the two
#: assertion slots surface over all 129 corpus prose strings, and the
#: subset the pack's modeled vocabulary holds.
_CORPUS_SURFACE: tuple[str, ...] = (
    "absence", "alone", "arithmetic", "arm", "attempt", "attention",
    "barkeep", "belt", "birth", "black", "calm", "candlelight", "coat",
    "cost", "cup", "door", "dry", "ear", "echo", "end", "expectation",
    "eye", "eyes", "face", "fact", "far", "fear", "fire", "first",
    "flailing", "gaze", "good", "greeting", "guard", "hand", "head",
    "held", "inch", "lamp", "ledger", "like", "mind", "mistake",
    "morning", "mug", "new", "night", "noise", "old", "on", "one",
    "own", "panic", "paperwork", "pointing", "private", "purse", "rag",
    "record", "refusal", "ruin", "same", "scolding", "shadows", "shell",
    "small", "square", "stool", "story", "strange", "street", "thought",
    "tray", "trust", "voice", "wall", "warm", "watch", "window", "wrist",
    "yard",
)
_CORPUS_GROUNDED: tuple[str, ...] = (
    "attention", "barkeep", "door", "fear", "fire", "guard", "lamp",
    "mug", "on", "purse", "square", "street", "trust", "watch",
)


def test_vocabulary_is_the_packs_declared_words() -> None:
    """The grounded half's manifest reads the pack's own fields — display
    names, role words, moods, the relation/state axes — one source per
    fact (INV-3), the name manifest reused (never restated). Ids,
    snake_case tokens and enum values are not English attribute words
    and stay out."""
    assert {"Doren", "barkeep", "purse"} <= VOCAB  # display-name words
    assert {"thief", "owner", "witness"} <= VOCAB  # role words
    assert {"wary", "tired", "merry"} <= VOCAB  # the NPC moods
    assert {"trust", "suspicion", "fatigue", "attention"} <= VOCAB  # axes
    assert MANIFEST <= VOCAB  # the name manifest is the reused subset
    assert "npc_guard_01" not in VOCAB  # ids are not words
    assert "unknown" not in VOCAB  # crime_status enum
    assert "exact" not in VOCAB  # the fidelity ladder (epistemic render)


def test_vocabulary_is_deterministic() -> None:
    assert modeled_vocabulary(PACK) == VOCAB


def test_surface_catches_the_copular_kind_claim() -> None:
    """S1: the determiner-headed copular predicate — the category/identify
    assertion ("the purse was a gift")."""
    assert relation_attribute_tokens("The purse was a gift.") == ("gift",)


def test_surface_catches_the_relation_confabulation() -> None:
    """The designed probe: a kinship relation the world does not hold
    (brother), an unmodeled attribute (gift) and the possessor's
    grounded kind word (thief — pc_01's own role) — the split's three
    outcomes in one sentence. Recall arm for the instrument; the FP arm
    is the corpus pin below."""
    tokens = relation_attribute_tokens(
        "The barkeep was the thief's brother, and the purse was a gift."
    )
    assert tokens == ("brother", "gift", "thief")
    assert [token for token in tokens if token in VOCAB] == ["thief"]


def test_surface_the_s_contraction() -> None:
    """The copula slot admits the 's contraction — "he's no fool" is the
    emphatic-negation kind claim."""
    assert relation_attribute_tokens("He's no fool tonight.") == ("fool",)


def test_surface_negation_interveners() -> None:
    """Up to two lowercase interveners ride between copula and determiner
    ("is no longer a") — the greedy run resolves to the determiner, not
    the negation."""
    assert relation_attribute_tokens("She is no longer a guest.") == ("guest",)


def test_surface_possessive_tail_and_plural() -> None:
    """S2: the relation word after "'s" — singular and plural possessive
    alike."""
    assert relation_attribute_tokens("The maid's uncle nodded.") == ("uncle",)
    assert relation_attribute_tokens(
        "The guards' rest ended at dawn."
    ) == ("rest",)


def test_surface_intensifier_skips_to_the_real_tail() -> None:
    """The two intensifiers (own/very) are skipped so the real relation
    word surfaces, not the intensifier."""
    assert relation_attribute_tokens(
        "The crowd's own panic carried them."
    ) == ("panic",)
    assert relation_attribute_tokens(
        "The lamp's very glow was steady."
    ) == ("glow",)


def test_surface_relation_objects_via_the_contraction_path() -> None:
    """The declared feature: "X's trust in the barkeep" surfaces the
    relation's object noun too (the contraction path reads X's as a
    copula over the intervening relation words) — the full relation,
    measured honestly."""
    assert relation_attribute_tokens(
        "The maid's trust in the barkeep held fast."
    ) == ("barkeep", "trust")


def test_surface_determiner_tail_is_the_copula_not_possessive() -> None:
    """A determiner after 's is the contraction, never a possessive tail
    — the S2 block hands the shape to S1."""
    assert relation_attribute_tokens("He's a thief.") == ("thief",)


def test_surface_bare_adjectival_is_excluded_by_law() -> None:
    """The declared boundary: a bare adjective after the copula carries
    no unambiguous claim signal — tone-vs-claim needs semantics (the
    sentence-initial exemption's class). The weaker-engine arm measures
    that gap; this surface never guesses."""
    assert relation_attribute_tokens("The beams were soaked in oil.") == ()
    assert relation_attribute_tokens("The room was quiet.") == ()
    assert relation_attribute_tokens("The purse was silver.") == ()


def test_surface_capitalized_tokens_stay_out() -> None:
    """Lowercase only — a capitalized predicate head is already visible
    to the name floor's position law (no double policing)."""
    assert relation_attribute_tokens("The guard was the Landlord.") == ()


def test_surface_dedupes_sorted_deterministic() -> None:
    """INV-2: unique tokens, sorted — the tuple is the contract, any
    process."""
    assert relation_attribute_tokens(
        "The maid's uncle spoke; the maid's uncle left. He's no bard, "
        "and the club was the barkeep's."
    ) == ("bard", "barkeep", "uncle")


def test_surface_quotes_do_not_block() -> None:
    """No capital law is involved — quoted speech carries the same
    assertion slots (contrast the name floor's quote boundaries)."""
    assert relation_attribute_tokens(
        '"The maid\'s uncle," she said. "He\'s no fool."'
    ) == ("fool", "uncle")


def test_corpus_surface_pinned_both_arms() -> None:
    """The Layer-1 calibration baseline — this test is the single owner
    of the split numbers (D-024; a corpus regen re-measures here, the
    iter-48 discipline). The honest headline: clean operator narration
    already rides mostly unmodeled assertion tokens (67 of 81 unique —
    body parts, narration nouns), which is precisely why the refusal
    ladder is not the work (D-096) and any future ladder may only ride
    the weaker-engine arm's numbers. The grounded arm: the corpus's own
    axis assertions — the possessive forms it actually writes ("the
    serving maid's trust", "a guard's attention", "the drunkard's
    fear") — land grounded, the split working as designed."""
    surface: set[str] = set()
    hits = 0
    strings = 0
    for case in _CORPUS["cases"]:
        for beat in case["beats"]:
            prose = beat["reply"].get("prose")
            if not isinstance(prose, str):
                continue
            strings += 1
            tokens = relation_attribute_tokens(prose)
            hits += len(tokens)
            surface.update(tokens)
    assert (strings, hits, len(surface)) == (129, 133, 81)
    assert tuple(sorted(surface)) == _CORPUS_SURFACE
    grounded = tuple(sorted(token for token in surface if token in VOCAB))
    assert grounded == _CORPUS_GROUNDED
    assert len(grounded) == 14 and len(surface) - len(grounded) == 67
    assert {"trust", "fear", "attention"} <= set(grounded)  # the axis pin
