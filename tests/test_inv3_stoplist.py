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

iter-112 (world-2 L1, the reskin day): the stoplist's **self-check
extension** — the second pack exists, so its nouns join the INV-3 audit
vocabulary (PACK_SPEC §9's own step; the ROAD_STOPLIST below). The
engine-side grep reads BOTH lists; the self-check splits per pack so
each family stays tied to its own data.

iter-118 (world-2 L2, slice 1): the THIRD pack's nouns join the same
law (PROVINCE_STOPLIST below — the original-setting vocabulary; the
province is authored original content, D-130's posture tier, no
CREDITS sidecar). Shared words (market, hearth, lamp, toll) stay in
the older lists; "keep" is deliberately absent — a common English
verb the engine's prose legitimately carries; "garrison" and
"sergeant" carry the watch nouns instead.

Periphery scope note (iter-6a audit, D-046): `render/`, `cli/` and
`scripts/` are OUTSIDE the stoplist by design — they legitimately carry
pack path strings (`content/tavern_pack`), CLI help-text examples and
docstring prose; INV-3's substance is the ENGINE (`core/` + `sim/` +
`brief/` — the scope grew with the mediator circuit at iter-10a, KI#38)
hardcoding setting data (a second pack must require zero engine changes —
the renderer is template-driven, the CLI takes the pack dir as config).

iter-112 (world-2 L1, the reskin day): the stoplist's **self-check
extension** — the second pack exists, so its nouns join the INV-3 audit
vocabulary (PACK_SPEC §9's own step; the ROAD_STOPLIST below). The
engine-side grep reads BOTH lists; the self-check splits per pack so
each family stays tied to its own data.

iter-118 (world-2 L2, slice 1): the THIRD pack's nouns join the same
law (PROVINCE_STOPLIST below — the original-setting vocabulary, no
CREDITS sidecar: the province is authored original content, D-130's
posture tier). Shared words (market, hearth, lamp) stay in the older
lists; this list carries what is DISTINCTIVELY the province's.
"keep" is deliberately absent — a common English verb the engine's
prose legitimately carries; "garrison"/"sergeant" carry the watch
nouns instead.
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

# Setting nouns of road_pack (iter-112, the world-2 L1 reskin): the
# second pack's own vocabulary — the generic-stack nouns (SRD 5.1,
# CC-BY-4.0, content/road_pack/CREDITS.md) plus the authored toponyms.
# Shared tavern words (rope, hearth) stay in the tavern list; this list
# carries what is DISTINCTIVELY the road's.
ROAD_STOPLIST: tuple[str, ...] = (
    "ferry", "quay", "toll", "tollhouse", "inn", "innkeeper", "boatman",
    "lantern", "cudgel", "hawser", "mead", "throng", "jetty", "stockade",
    "timber", "cask", "odo", "ashen", "wayfarer", "gable",
)

# Setting nouns of province_pack (iter-118, world-2 L2 slice 1; grown
# iter-119, the cultures slice): the third pack's own vocabulary — the
# ORIGINAL setting's toponyms, cast names, prop nouns and culture words
# (the Sarrow Vale). Shared road/tavern words (market, hearth, lamp,
# toll) stay in the older lists; this list carries what is
# DISTINCTIVELY the province's. The cultures slice's additions
# (iter-119): the travelers' nouns (drover, peddler) and the hill law
# word (wergeld — the prohibition's own token, riding the carrier's
# goal). "carrier" is deliberately absent — the acquisition family's
# engine word (core/fold.py's item holder, the drift registry's own
# UNCLASSIFIED entry); the id npc_carrier_01 never spells it as a
# free-standing word in code. The triangle slice's additions
# (iter-135): the faction nouns (guild, council, vigil, patrol — the
# goal verbs and their tale lines), the chronicle's third tier
# (exodus), and the feud's own axis (grievance — the wergeld's
# pressure surface). The calendar slice's additions (iter-136): the
# seasons' distinctive nouns (thaw, frost — the cycle phases' own
# words, riding the season tale lines); "market" stays in the older
# tavern list, "fair" and "season" are deliberately absent — common
# English words the engine's prose legitimately carries.
PROVINCE_STOPLIST: tuple[str, ...] = (
    "sarrow", "weir", "malby", "thornmill", "tithe", "crofts", "garrison",
    "sergeant", "corporal", "osgar", "ketta", "ferra", "garrick",
    "wilmot", "tallow", "punt", "tally", "waybill", "tin", "weighbeam",
    "charcoal", "drover", "peddler", "wergeld", "guild", "council",
    "vigil", "patrol", "exodus", "grievance", "thaw", "frost",
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
    patterns = [
        (word, _segment_pattern(word))
        for word in (*STOPLIST, *ROAD_STOPLIST, *PROVINCE_STOPLIST)
    ]
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


def test_road_stoplist_words_actually_belong_to_the_road_pack() -> None:
    """The self-check extension (iter-112): the road stoplist tracks the
    SECOND pack's setting vocabulary — every word occurs in the road
    pack's data as a full segment (ids included)."""
    pack_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((REPO / "content" / "road_pack").glob("*.json"))
    )
    missing = [
        word for word in ROAD_STOPLIST
        if not _segment_pattern(word).search(pack_text)
    ]
    assert not missing, (
        f"road stoplist words absent from the road pack data: {missing}"
    )


def test_province_stoplist_words_actually_belong_to_the_province_pack() -> None:
    """The self-check extension, the third pack (iter-118): the province
    stoplist tracks the L2 pack's setting vocabulary — every word occurs
    in the province pack's data as a full segment (ids included)."""
    pack_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((REPO / "content" / "province_pack").glob("*.json"))
    )
    missing = [
        word for word in PROVINCE_STOPLIST
        if not _segment_pattern(word).search(pack_text)
    ]
    assert not missing, (
        f"province stoplist words absent from the province pack data: "
        f"{missing}"
    )
