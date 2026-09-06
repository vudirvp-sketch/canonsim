"""The invented-entity prose floor (iter-66, D-095 — the v0.2 refinement
family's first landing; contract owner `docs/VALIDATION_SPEC.md` §2.1).

The response document's `prose` field is the boundary's one free-text
surface: never parsed, never repaired, never treated as instructions
(VALIDATION_SPEC §2 — injection carries nothing actionable). It gets
exactly ONE structural check, the closed-world twin of the claim-side
`unknown_entity` verdict: **a capitalized token in unambiguous
proper-noun position must be a word of a declared entity's display
name.**

Three laws hold the design:

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
    "name_manifest",
    "prose_refusal_lines",
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
