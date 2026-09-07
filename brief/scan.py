"""The invented-entity prose floor (iter-66, D-095 — the v0.2 refinement
family's first landing; contract owner `docs/VALIDATION_SPEC.md` §2.1)
plus the lowercase assertion surface (iter-72, prosefloor-2 — D-104;
D-096's routing: the detection half only).

The response document's `prose` field is the boundary's one free-text
surface: never parsed, never repaired, never treated as instructions
(VALIDATION_SPEC §2 — injection carries nothing actionable). It gets
exactly ONE structural check, the closed-world twin of the claim-side
`unknown_entity` verdict: **a capitalized token in unambiguous
proper-noun position must be a word of a declared entity's display
name.**

Three laws hold the floor's design:

- **Existence, not visibility.** The manifest is the PACK's declared
  names (`name_manifest`) — the whole closed world, not the current
  call's entity cards. A name may be legally narrated off-stage (the
  named thing walked out of the scene mid-session; the world still
  holds it — the brief shows who is present, the floor asks what
  exists); knowledge-state is the leak suite's job (all four layers),
  never this floor's. The floor answers one question only: does the
  named thing exist at all.
- **The detection surface is the unambiguous position.** English
  mandates a capital at every sentence start, so a capitalized token
  there carries no name signal; a capital in NON-initial position is a
  proper noun (or the pronoun "I"). Sentence-initial detection would
  need an English common-word dictionary — out of scope by the
  stdlib-only law, and a heuristic word list would trade the provable
  FP=0 for speculative recall; bg-7 measures the live gap before any
  extension is considered (the surface-section decision rides it).
- **A gate, not a repair.** Violations are `REFUSED prose <name>
  (invented_entity)` lines — the same dry protocol shape as every
  refusal family, riding the next call and the existing regen budget
  (VALIDATION_SPEC §7; exhaustion falls to the L12 ladder, never a
  crash, never a silent drop).

The lowercase twin (iter-72, D-104): the position law is blind to
lowercase relation/attribute assertions ("the thief's brother", "a
gift"), so the module exports the DETECTION surface for exactly that
half — a measurement instrument for bg-8's weaker-engine arm, never a
gate:

- **The surface is the unambiguous assertion slot.** Two shapes: the
  determiner-headed copular predicate (a BE-form or the 's contraction,
  up to two lowercase interveners — "was the landlord's brother",
  "he's no fool", "is no longer a suspect"; the contraction path also
  surfaces the relation object in "the miller's trust in the landlord"
  shapes) and the possessive tail ("the miller's uncle", the plural
  "the watchmen's rest"; the intensifiers own/very are skipped to the
  real tail). Bare adjectival predicates ("was drunk", "were soaked in
  oil") are EXCLUDED by declared law — telling a tone adjective from
  an attribute claim needs semantics, the same class as the
  sentence-initial exemption; the weaker-engine arm measures that gap.
  Capitalized tokens stay out (the name floor's position law owns
  them). The closed classes (copulas, determiners, intensifiers) are
  English function words only — mechanics, never domain words (INV-3).
- **A measurement, never a gate.** No refusal, no regen spend, no
  boundary wiring (D-096: the refusal ladder is NOT the work; a future
  ladder may only ride the weaker-engine arm's measured numbers). The
  split is the consumer's set arithmetic: a surface token the world's
  `modeled_vocabulary` holds is grounded, one it does not is the
  unmodeled half. The committed corpus's own split is pinned in
  `tests/test_scan.py` (the single owner of the calibration numbers).
- **The manifest reads the pack's own fields.** `modeled_vocabulary`:
  every declared display-name word (the name manifest), every entity
  record's `role` words, the NPC `mood` words, and the relation/state
  axis names — one source per fact (INV-3). Trait and knowledge tokens
  (snake_case ids) and enum values (crime_status, the flammability
  scale) are not English attribute words and stay out.

Pure function of (prose, manifest): regex only, no RNG, no I/O, no
wall-clock; the manifest is derived once per session from the immutable
pack (INV-2/INV-3 — the mechanics live here, the names stay pack data).
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Final

from core.pack import Pack

__all__ = [
    "INVENTED_ENTITY",
    "PROSE_STOPWORDS",
    "invented_names",
    "modeled_vocabulary",
    "name_manifest",
    "prose_refusal_lines",
    "relation_attribute_tokens",
]

#: The refusal reason (VALIDATION_SPEC §2.1 — the closed REASONS style,
#: the prose twin of the claim side's `unknown_entity`).
INVENTED_ENTITY: Final = "invented_entity"

#: English function words that are capitalized MID-sentence (the closed
#: class: the first-person pronoun). Everything else mid-sentence-capital
#: is a proper noun by position.
PROSE_STOPWORDS: Final = frozenset({"I"})

#: The entity categories whose records declare display names (the whole
#: closed world — the pack's cast, not any per-beat visibility set).
_NAME_CATEGORIES: Final = ("locations", "npcs", "ambient_entities", "items")

# Sentence boundaries: terminal punctuation (with closing quotes /
# brackets), an opening quote (dialogue restarts the capital law), or a
# line break. Commas, colons and dashes are deliberately NOT boundaries —
# a capital after one is still mid-sentence, still a name signal.
_SENTENCE_START: Final = re.compile(r"[.!?…]+[\"')\]]*\s+|[\(\"'\[]+\s*|\n+")

_WORD: Final = re.compile(r"[A-Za-z]+")

#: The closed determiner class — one source for the copular head
#: position (S1) and the possessive tail block (S2). English function
#: words only (INV-3: mechanics, never domain words); the emphatic
#: negation "no" included ("he's no fool").
_DETERMINERS: Final = (
    "a", "an", "the", "no", "this", "that", "these", "those",
    "his", "her", "their", "its", "my", "your", "our",
)
_DET: Final = "|".join(_DETERMINERS)

#: The assertion token shape: a lowercase word, hyphen compounds taken
#: whole ("off-duty"). Capitalized tokens are the name floor's domain.
_ASSERTION_TOKEN: Final = r"([a-z]+(?:-[a-z]+)*)"

# S1 — the copular predicate head: a BE-form or the 's contraction, up
# to two lowercase interveners (negation/adverb: "is no longer a"),
# then the determiner's head position. A question-form capital on the
# copula ("Was the wagon a gift?") is a declared miss.
_COPULAR_HEAD: Final = re.compile(
    r"(?:\b(?:is|was|are|were|am|be|been|being)\b|\b[A-Za-z]+'s)\s+"
    rf"(?:[a-z]+\s+){{0,2}}(?:{_DET})\s+{_ASSERTION_TOKEN}"
)

# S2 — the possessive tail: the relation word after "'s"/"s'". A
# determiner tail is the 's-copula (S1's shape — blocked); the two
# intensifiers (own/very) are skipped to the real tail.
_POSSESSIVE_TAIL: Final = re.compile(
    rf"\b[A-Za-z]+(?:'s|s')\s+(?:(?:own|very)\s+)?(?!(?:{_DET})\b)"
    rf"{_ASSERTION_TOKEN}"
)


def name_manifest(pack: Pack) -> frozenset[str]:
    """The closed world's name vocabulary: every word of every declared
    entity record's display `name` (the same pack fields the brief's
    entity cards render — one source, read directly, never restated).
    Ids, roles and the pack meta display are not names and stay out."""
    words: set[str] = set()
    for category in _NAME_CATEGORIES:
        for record in pack.entities[category]:
            words.update(_WORD.findall(str(record["name"])))
    return frozenset(words)


def invented_names(prose: str, manifest: frozenset[str]) -> tuple[str, ...]:
    """The prose's invented-entity violations: capitalized tokens in
    non-sentence-initial position whose form is neither a declared name
    (exact, case-preserved — possessives strip to the stem) nor a
    `PROSE_STOPWORDS` member. Sorted and deduplicated (INV-2: the
    iteration order is part of the contract). Same (prose, manifest)
    → same tuple, any process."""
    starts = {0}
    for boundary in _SENTENCE_START.finditer(prose):
        starts.add(boundary.end())
    found = {
        match.group(0)
        for match in _WORD.finditer(prose)
        if match.start() not in starts
        and match.group(0)[0].isupper()
        and match.group(0) not in manifest
        and match.group(0) not in PROSE_STOPWORDS
    }
    return tuple(sorted(found))


def prose_refusal_lines(violations: Sequence[str]) -> tuple[str, ...]:
    """The refusal family's dry lines (the ledger's `REFUSED <item>
    (<reason>)` shape, one per unique name): they ride the next call's
    protocol section through the existing regen machinery — the operator
    sees exactly which names the world does not hold."""
    return tuple(
        f"REFUSED prose {name} ({INVENTED_ENTITY})" for name in violations
    )


def modeled_vocabulary(pack: Pack) -> frozenset[str]:
    """The closed world's declared English words — the grounded half of
    the lowercase assertion split: every display-name word (the name
    manifest — one source, reused), every entity record's `role` words,
    the NPC `mood` words, and the relation/state axis names (the rules'
    own fields, read directly). Trait and knowledge tokens (snake_case
    ids) and enum values (crime_status, the flammability scale) are not
    English attribute words and stay out. Same pack → same frozenset,
    any process (INV-2/INV-3: mechanics here, words in pack data)."""
    words = set(name_manifest(pack))
    for category in _NAME_CATEGORIES:
        for record in pack.entities[category]:
            role = str(record.get("role", "")).replace("'s", " ")
            words.update(_WORD.findall(role))
    for record in pack.entities["npcs"]:
        words.update(_WORD.findall(str(record.get("mood", ""))))
    words.update(str(axis) for axis in pack.rules["relations"]["axes"])
    words.update(
        str(axis) for axis in pack.rules.get("states", {}) if axis != "notes"
    )
    return frozenset(words)


def relation_attribute_tokens(prose: str) -> tuple[str, ...]:
    """The lowercase assertion surface: tokens in the two unambiguous
    assertion slots (the determiner-headed copular predicate, the
    possessive tail — the module docstring's declared boundaries),
    sorted and deduplicated (INV-2: same prose → same tuple, any
    process). A measurement export, never a gate: the consumer splits
    it against `modeled_vocabulary` (grounded / unmodeled); no refusal,
    no regen spend, no boundary wiring (D-096 — the weaker-engine arm
    measures first)."""
    found = {match.group(1) for match in _COPULAR_HEAD.finditer(prose)}
    found.update(match.group(1) for match in _POSSESSIVE_TAIL.finditer(prose))
    return tuple(sorted(found))
