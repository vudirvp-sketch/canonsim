"""iter-176 (doc-3) — the mechanical cap guard suite
(`scripts/docguard.py`, the recurrence fix the iter-140/151 GC passes
lacked).

The laws this suite pins: (1) LINT = CI, NEVER TASTE — every check is
a count over a documented shape (AGENTS §6 + the restored Next-step
one-rolling-block protocol); (2) the crafted mini-repo carries known
breaches for every family, each producing exactly the family's
violation line; (3) the allowlist is part of the guard's own text —
an allowlisted path over the cap stays clean, a non-allowlisted one
trips; (4) the DRIFT PIN — the real repo's state docs parse clean at
HEAD (a future edit that breaches a cap fails HERE, in the same
iteration, the test_digest family's shape).
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import docguard  # type: ignore[import-not-found]  # noqa: E402

MINI_STATUS = """\
Iteration: iter-9 (`iter-9-mini` — the crafted guard fixture) ·
Phase: 3 (Director) — CLOSED (crafted phases) ·
42 passed +1 skipped, ruff clean (crafted) ·
Date: 2026-01-02 ·
Scope: the crafted fixture only.

## Invariants

- crafted

## Active KIs

- KI#12 · the crafted open KI · 2026-01-01

## FAQ / Pitfalls

- **Crafted one-liner law** — the crafted owner.

## Next step

**iter-9 DONE: the crafted landing.**

1. The crafted next step.
"""

MINI_WORKLOG = """\
# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry.
---
iter-9 · 2026-01-02 · mini — the crafted entry: what changed and why,
the files touched, the verification line. Crafted to the entry law,
holding the three-line minimum the guard counts.
---
iter-8 · 2026-01-01 · older — the crafted second entry holding the cap
at two, each within the three-to-five line law; the crafted detail
line so the physical line count lands inside the law.
"""

MINI_TASKS = """\
# TASKS

## Track A — main

- `world-9` · the crafted parked row —
  todo, owner-gated (crafted)

### Iteration ledger (one line per iteration; the tail capped by the guard)

- iter-9 · 2026-01-02 · mini — the crafted landing

## Track B — background

### bg-6 · crafted audit — todo (owner-deferred)
"""

MINI_DECISIONS = """\
# DECISIONS

| ID | Date | Decision | Why | Consequence |
|---|---|---|---|---|
| D-001 | 2026-01-01 | the crafted first row | why | so |
| D-002 | 2026-01-02 | the crafted second row | why | so |
"""


def _mini(tmp_path: Path) -> Path:
    (tmp_path / "STATUS.md").write_text(MINI_STATUS, encoding="utf-8")
    (tmp_path / "worklog.md").write_text(MINI_WORKLOG, encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "TASKS.md").write_text(MINI_TASKS, encoding="utf-8")
    (tmp_path / "docs" / "DECISIONS.md").write_text(MINI_DECISIONS, encoding="utf-8")
    return tmp_path


def _rewrite(root: Path, rel: str, old: str, new: str) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture shape drifted: {rel}"
    path.write_text(text.replace(old, new), encoding="utf-8")


# -- the healthy mini-repo ------------------------------------------------


def test_guard_clean_on_the_mini_repo(tmp_path: Path) -> None:
    """Every count inside its cap: zero violations, the exit code 0."""
    assert docguard.violations(_mini(tmp_path)) == []
    assert docguard.main([str(tmp_path)]) == 0


# -- one violation per family (the crafted mini-repo) --------------------


def test_faq_entry_count_and_essay_length(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    essays = "\n".join(
        f"- **Crafted essay {i}** — the crafted long law line one\n"
        "  the crafted long law line two\n"
        "  the crafted long law line three\n"
        "  the crafted long law line four"
        for i in range(21)
    )
    _rewrite(root, "STATUS.md", "- **Crafted one-liner law** — the crafted owner.",
             essays)
    found = docguard.violations(root)
    assert any("21 FAQ entries" in v for v in found)
    assert any("FAQ entry over 3 lines (4)" in v for v in found)
    assert len([v for v in found if "FAQ" in v]) == 22


def test_ki_count_and_length(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    kis = "\n".join(f"- KI#{n} · crafted · 2026-01-01" for n in range(12, 27))
    long_ki = "- KI#99 · crafted long · line one\n  line two\n  line three"
    _rewrite(root, "STATUS.md", "- KI#12 · the crafted open KI · 2026-01-01",
             kis + "\n" + long_ki)
    found = docguard.violations(root)
    assert any("16 active KIs" in v for v in found)
    assert any("KI over 2 lines (3)" in v for v in found)


def test_two_done_blocks_break_the_rolling_protocol(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    _rewrite(root, "STATUS.md", "**iter-9 DONE: the crafted landing.**",
             "**iter-9 DONE: the crafted landing.**\n\n**iter-8 DONE: a stale "
             "block the protocol forbids.**")
    assert any("2 DONE blocks" in v for v in docguard.violations(root))


def test_worklog_entry_count_and_length(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    text = (root / "worklog.md").read_text(encoding="utf-8")
    extra = "\n".join(
        f"---\niter-{n} · 2026-01-01 · filler{n} — the crafted cap breaker"
        for n in range(7, 17)
    )
    (root / "worklog.md").write_text(text + "\n" + extra + "\n", encoding="utf-8")
    found = docguard.violations(root)
    assert any("12 entries" in v for v in found)
    assert all("is 1 lines" in v for v in found if "entry iter-" in v)


def test_tasks_ledger_tail_and_history_headings(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    text = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
    tail = "\n".join(
        f"- iter-{n} · 2026-01-01 · filler{n} — the crafted tail breaker"
        for n in range(8, 18)
    )
    history = "### iter-7 · crafted — done\n\nThe crafted detailed section."
    (root / "docs" / "TASKS.md").write_text(
        text.replace(
            "- iter-9 · 2026-01-02 · mini — the crafted landing",
            "- iter-9 · 2026-01-02 · mini — the crafted landing\n" + tail,
        ) + "\n" + history + "\n",
        encoding="utf-8",
    )
    found = docguard.violations(root)
    assert any("11 one-liners" in v for v in found)
    assert any("detailed history heading" in v for v in found)


def test_decisions_row_cap(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    rows = "\n".join(
        f"| D-{n:03d} | 2026-01-01 | crafted | why | so |" for n in range(3, 33)
    )
    _rewrite(root, "docs/DECISIONS.md",
             "| D-002 | 2026-01-02 | the crafted second row | why | so |",
             "| D-002 | 2026-01-02 | the crafted second row | why | so |\n" + rows)
    assert any("32 rows" in v for v in docguard.violations(root))


def test_docs_cap_and_the_allowlist(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    big = "crafted line\n" * 601
    # a non-allowlisted over-cap doc trips
    (root / "docs" / "BIG.md").write_text(big, encoding="utf-8")
    assert any("docs/BIG.md: 601 lines" in v for v in docguard.violations(root))
    # an allowlisted path over the cap stays clean (the guard's own table)
    (root / "docs" / "TECH_NOTES.md").write_text(big, encoding="utf-8")
    (root / "docs" / "BIG.md").unlink()
    assert docguard.violations(root) == []


def test_missing_state_docs_are_loud(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    found = docguard.violations(empty)
    assert any("STATUS.md: missing" in v for v in found)
    assert any("worklog.md: missing" in v for v in found)
    assert any("TASKS.md: missing" in v for v in found)
    assert any("DECISIONS.md: missing" in v for v in found)
    assert any("docs/: missing" in v for v in found)


# -- the drift pin (the real repo: the recurrence fix's teeth) ------------


def test_guard_clean_on_the_real_repo() -> None:
    """The caps hold at HEAD: AGENTS §6's counts, the FAQ one-liner law,
    the worklog entry law, the TASKS ledger tail, the DECISIONS cap,
    and the docs cap with its allowlist — the bloat cannot silently
    regrow between owner housekeeping calls (the iter-140/151 lesson:
    both GC passes lacked exactly this executable check)."""
    assert docguard.violations(REPO) == []
