"""iter-108 — the digest suite (the risk-synthesis §6 rider:
`scripts/digest.py`, the derived one-pager over the three state-owning
docs).

The laws this suite pins: (1) DERIVED-ONLY — the digest renders the
docs' own words (the crafted mini-repo carries known text; every
rendered line is a quote or a count of it); (2) never a second source
of truth — no computed metrics, no restated state; (3) DETERMINISM —
same docs, same bytes, and no wall-clock in the source at all (the
scaffold's INV-2-hygiene precedent, pinned as a source scan); (4) the
doctor's law — an unparsable shape degrades to (unparsed), a missing
doc is loud (exit 1), neither crashes; (5) the DRIFT PIN — the real
repo's docs must parse cleanly (a future header reshape that breaks
the digest fails HERE, in the same iteration, the test_drift family's
shape); value pins are for the mini-repo only — the digest of iter-109
must not fail iter-108's test.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import digest  # type: ignore[import-not-found]  # noqa: E402

MINI_STATUS = """\
Iteration: iter-9 (`iter-9-mini` — the crafted digest fixture) ·
Phase: 3 (Director) — CLOSED (crafted phases) ·
42 passed +1 skipped, ruff clean (crafted) ·
Date: 2026-01-02 ·
Scope: the crafted fixture only.

## Invariants

- crafted

## Active KIs

- KI#12 · the crafted open KI · 2026-01-01

## Next step

**iter-9 DONE: the crafted landing — the fixture's own words.** Nothing
pinned.

1. **The opening call** — crafted item one.
2. Crafted item two.
"""

MINI_TASKS = """\
# TASKS

## Track A — main

- `world-9` · the crafted parked row —
  todo, owner-gated (crafted)

### iter-9 · mini — done

The crafted landing.

### iter-8 · older — done

## Track B — background

### bg-2 · crafted probe — done (2026-01-01)

### bg-6 · crafted audit — todo (owner-deferred)
"""

MINI_DECISIONS = """\
# DECISIONS

| ID | Date | Decision | Why | Consequence |
|---|---|---|---|---|
| D-001 | 2026-01-01 | **The crafted first law: the colon cut** | why | so |
| D-002 | 2026-01-02 | **The crafted second law — the em-dash cut** | why | so |
"""


def _mini(tmp_path: Path) -> Path:
    (tmp_path / "STATUS.md").write_text(MINI_STATUS, encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "TASKS.md").write_text(MINI_TASKS, encoding="utf-8")
    (tmp_path / "docs" / "DECISIONS.md").write_text(MINI_DECISIONS, encoding="utf-8")
    return tmp_path


# -- the rendered shape (the crafted mini-repo: value pins allowed) ----


def test_digest_renders_the_mini_repo(tmp_path: Path) -> None:
    """Every section renders, and every value is the fixture's own
    text: the header's five fields, the bold lead + the numbered items,
    the KI census, the todo census (wrapped row + todo heading), the
    landings ordered by iteration id, the decisions tail with both cut
    laws."""
    out = digest.render(_mini(tmp_path))
    assert out.startswith("canonsim — the digest")
    assert "iteration: iter-9 (iter-9-mini) · 2026-01-02" in out
    assert "phase:     3 (Director) — CLOSED" in out
    assert "tests:     42 passed +1 skipped" in out
    assert "KIs:       1: KI#12 · the crafted open KI" in out
    assert "next step: iter-9 DONE: the crafted landing" in out
    assert "  1. The opening call — crafted item one." in out
    assert "  2. Crafted item two." in out
    assert "backlog:   2 todo-flagged rows: world-9, bg-6" in out
    assert "landings:  iter-9 mini · iter-8 older" in out
    assert "decisions: last 2 of 2 rows" in out
    assert "  D-001 · 2026-01-01 · The crafted first law" in out
    assert "  D-002 · 2026-01-02 · The crafted second law" in out


def test_digest_decisions_limit(tmp_path: Path) -> None:
    """--decisions tails the file: the limit is honored, the census
    still counts every row."""
    out = digest.render(_mini(tmp_path), decisions=1)
    assert "decisions: last 1 of 2 rows" in out
    assert "D-002" in out
    assert "D-001 ·" not in out


def test_digest_no_kis_means_none_active(tmp_path: Path) -> None:
    """An Active KIs section with no `- KI#N` lines is 'none active' —
    a derived verdict over the deletion notes, not an assumption."""
    root = _mini(tmp_path)
    text = (root / "STATUS.md").read_text(encoding="utf-8")
    (root / "STATUS.md").write_text(
        text.replace("- KI#12 · the crafted open KI · 2026-01-01",
                     "- (KI#11 deleted per AGENTS §5 — closed iter-7)"),
        encoding="utf-8",
    )
    assert "KIs:       none active" in digest.render(root)


# -- the laws ------------------------------------------------------------


def test_digest_deterministic_no_wall_clock(tmp_path: Path) -> None:
    """Same docs, same bytes — and the source never imports a clock:
    the date shown is STATUS.md's own Date line (the scaffold's INV-2
    hygiene extended to derived artifacts, pinned as a source scan)."""
    root = _mini(tmp_path)
    assert digest.render(root) == digest.render(root)
    source = Path(digest.__file__).read_text(encoding="utf-8")
    assert "datetime" not in source
    assert "time.time" not in source


def test_digest_degrades_never_crashes(tmp_path: Path) -> None:
    """The doctor's law: garbage docs render with (unparsed) markers
    and empty censuses — the digest never guesses past the data, and
    never raises on text it does not understand."""
    (tmp_path / "STATUS.md").write_text("random\ntext\nno anchors\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "TASKS.md").write_text("", encoding="utf-8")
    (tmp_path / "docs" / "DECISIONS.md").write_text("| broken table\n", encoding="utf-8")
    out = digest.render(tmp_path)
    assert "(unparsed)" in out
    assert "backlog:   no todo-flagged rows" in out
    assert "landings:  (none)" in out
    assert "decisions: last 0 of 0 rows" in out


def test_digest_missing_doc_is_loud(tmp_path: Path, capsys: object) -> None:
    """A repo without the state docs is a usage error, not a blank
    page: exit 1, the offending path on stderr."""
    empty = tmp_path / "empty"
    empty.mkdir()
    code = digest.main([str(empty)])
    assert code == 1
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert "STATUS.md" in captured.err


# -- the drift pin (the real repo: shape pins only, never values) ------


def test_digest_parses_the_real_repo_cleanly() -> None:
    """The contract with the docs' shapes: every header field parses
    (no (unparsed) markers), every listed decision row carries a D-id,
    and the iteration/phase/test lines keep their anchored shapes. A
    future doc reshape that breaks the digest fails HERE — the fix
    lands in the same iteration (the test_drift family's law)."""
    out = digest.render(REPO)
    assert "(unparsed)" not in out
    assert "(no " not in out
    assert "iteration: iter-" in out
    assert "phase:     " in out
    assert "tests:     " in out
    assert "KIs:       " in out
    assert "next step: " in out
    assert "decisions: last 8 of " in out
    for line in out.splitlines():
        if line.startswith("  D-"):
            assert line[2:].split(" ·")[0].startswith("D-")


def test_digest_cut_prefers_natural_boundaries() -> None:
    """The headline cut: a colon or em-dash clause inside the width
    wins; beyond it, a hard cut that always carries the ellipsis."""
    assert digest._cut("The crafted first law: the colon cut", 80) == (
        "The crafted first law"
    )
    assert digest._cut("The crafted second law — the em-dash cut", 80) == (
        "The crafted second law"
    )
    long = "x" * 100
    cut = digest._cut(long, 80)
    assert len(cut) <= 80
    assert cut.endswith(digest._ELLIPSIS)
    assert digest._cut("short", 80) == "short"
