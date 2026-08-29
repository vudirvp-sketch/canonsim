"""INV-3 made executable: the grep stoplist test (from iter-2, AGENTS §4).

Scope (the interpretation this test enforces): **setting** nouns — the
invariant's named examples ('guard', 'purse', 'tavern') and the rest of
the tavern_pack vocabulary — must never appear in `core/`, `sim/` or
`brief/` code (the ENGINE — `brief/` is the mediator circuit,
engine-side since iter-8: pure functions of (log, ledger, pack)).
Matching is **segment-based**: a word delimited by non-alphanumerics, so
both standalone prose words (`guard`) and compound identifiers
(`npc_guard_01`, `loc_guardroom`) trip it, while English derivations
('guards', 'guarded') and mechanic vocabulary (take, move, fire, stealth —
the generic action names of MVP_SCOPE §7) stay legal. Pack data
(`content/`) is where the setting lives — the stoplist never greps it, and
the second test keeps the list tied to the pack's actual vocabulary so it
cannot rot.

Periphery scope note (iter-6a audit, D-046): `render/`, `cli/` and
`scripts/` are OUTSIDE the stoplist by design — they legitimately carry
pack path strings (`content/tavern_pack`), CLI help-text examples and
docstring prose; INV-3's substance is the ENGINE (`core/` + `sim/` +
`brief/` — the scope grew with the mediator circuit at iter-10a, KI#38)
hardcoding setting data (a second pack must require zero engine changes —
the renderer is template-driven, the CLI takes the pack dir as config).
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Setting nouns of tavern_pack: the invariant's named examples plus entity
# display names and location/item vocabulary (kept in sync with the pack
# by the self-check below).
STOPLIST: tuple[str, ...] = (
    "guard", "purse", "tavern", "doren", "drunkard", "barkeep", "maid",
    "lamp", "ale", "mug", "club", "rope", "market", "street", "backyard",
    "guardroom", "crowd", "woodpile", "hearth", "arson",
)


def _segment_pattern(word: str) -> re.Pattern[str]:
    """The word as a full segment: delimited by non-alphanumerics on both
    sides (word boundaries AND snake_case compound segments)."""
    return re.compile(rf"(?<![a-zA-Z0-9]){re.escape(word)}(?![a-zA-Z0-9])",
                      re.IGNORECASE)


def source_files() -> list[Path]:
    files: list[Path] = []
    for package in ("core", "sim", "brief"):
        files.extend(sorted((REPO / package).rglob("*.py")))
    assert files, "no sources found — the stoplist test must see core/, sim/ and brief/"
    return files


def test_no_setting_words_in_engine_code() -> None:
    patterns = [(word, _segment_pattern(word)) for word in STOPLIST]
    violations: list[str] = []
    for path in source_files():
        text = path.read_text(encoding="utf-8")
        for word, pattern in patterns:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                violations.append(f"{path.name}:{line}: {word}")
    assert not violations, (
        f"INV-3 violations (setting words in code): {violations}"
    )


def test_stoplist_words_actually_belong_to_the_pack() -> None:
    """The stoplist must track the pack's setting vocabulary, not rot: every
    word occurs in the pack data as a full segment (ids included)."""
    pack_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((REPO / "content" / "tavern_pack").glob("*.json"))
    )
    missing = [
        word for word in STOPLIST
        if not _segment_pattern(word).search(pack_text)
    ]
    assert not missing, f"stoplist words absent from the pack data: {missing}"
