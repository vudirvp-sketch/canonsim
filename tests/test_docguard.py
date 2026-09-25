"""iter-176 (doc-3) — the mechanical cap guard suite
(`scripts/docguard.py`, the recurrence fix the iter-140/151 GC passes
lacked); ssi-2 (D-222/D-223) — the SSI control-plane shape families.

The laws this suite pins: (1) LINT = CI, NEVER TASTE — every check is
a count over a documented shape (AGENTS §6 + the restored Next-step
one-rolling-block protocol + the SSI overlay's own tables); (2) the
crafted mini-repo carries known breaches for every family, each
producing exactly the family's violation line; (3) the allowlist is
part of the guard's own text — an allowlisted path over the cap stays
clean, a non-allowlisted one trips; (4) the DRIFT PIN — the real
repo's state docs parse clean at HEAD (a future edit that breaches a
cap fails HERE, in the same iteration, the test_digest family's
shape); (5) the SSI families (ssi-2/D-222 + D-223): the overlay's
block matrix / rule subset / phase ladder lint exactly their
breaches — a skipped block, an out-of-vocabulary state, an implicit
waive, a drifted instrument, a silently-open phase, an evidence bar
without trajectory terms, an R3+ DECISIONS row without its PCC
record, a deleted AGENTS §2.9 ladder.
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

MINI_AGENTS = """\
# AGENTS — the crafted mini law

2. Iteration protocol: the crafted protocol.
9. Risk ladder (crafted ssi row): R0–R2 the standing protocol; R3+
   self-declares the class and carries the PCC record.
"""

#: The crafted overlay — every table complete and in-vocabulary, the
#: instruments (tests/mini_arch.py, scripts/mini_lint.py) created by
#: _mini() so the existence law holds; each breach test below breaks
#: exactly one shape.
MINI_OVERLAY = """\
# SSI_OVERLAY — the crafted mini-repo overlay

## The block matrix

| Block | Q | Mechanism | State | Evidence |
|---|---|---|---|---|
| A | crafted | crafted | VERIFIED | crafted |
| B | crafted | crafted | OPEN | crafted |
| C | crafted | crafted | PARTIAL | crafted |
| D | crafted | none | NOT_APPLICABLE | reason= crafted |
| E | crafted | crafted | VERIFIED | crafted |
| F | crafted | crafted | VERIFIED | crafted |
| G | crafted | crafted | VERIFIED | crafted |
| H | crafted | crafted | VERIFIED | crafted |
| I | crafted | crafted | PARTIAL | crafted |
| J | crafted | crafted | VERIFIED | crafted |
| K | crafted | crafted | VERIFIED | crafted |
| L | crafted | crafted | PARTIAL | crafted |

## The rule subset

| Rule | Name | Instrument | State | Findings |
|---|---|---|---|---|
| SSI-N001 | crafted | tests/mini_arch.py | VERIFIED | crafted |
| SSI-N002 | crafted | tests/mini_arch.py | VERIFIED | crafted |
| SSI-N006 | crafted | scripts/mini_lint.py | VERIFIED | crafted |
| SSI-N007 | crafted | scripts/mini_lint.py | VERIFIED | crafted |
| SSI-N010 | crafted | scripts/mini_lint.py | VERIFIED | crafted |
| SSI-N017 | crafted | scripts/mini_lint.py | VERIFIED | crafted |
| SSI-N018 | crafted | scripts/mini_lint.py | OPEN | crafted |
| SSI-N020 | crafted | scripts/mini_lint.py | OPEN | crafted |

## The phase ladder

| Phase | Track | Scope | Gate | Evidence bar |
|---|---|---|---|---|
| 0 | ssi-1 | crafted | CLOSED iter-9 | crafted |
| 1 | ssi-2 | crafted | CLOSED iter-9 | crafted |
| 2 | ssi-3 | crafted | owner-gated | co-change crafted |
| 3 | ssi-4 | crafted | owner-gated | crafted |
| 4 | ssi-5 | crafted | owner-gated | trajectory crafted |
| 5 | ssi-6 | crafted | owner-gated | crafted |
| 6 | ssi-7 | crafted | owner-gated | crafted |
| 7 | ssi-8 | crafted | owner-gated | crafted |
"""


def _mini(tmp_path: Path) -> Path:
    (tmp_path / "STATUS.md").write_text(MINI_STATUS, encoding="utf-8")
    (tmp_path / "worklog.md").write_text(MINI_WORKLOG, encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(MINI_AGENTS, encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "TASKS.md").write_text(MINI_TASKS, encoding="utf-8")
    (tmp_path / "docs" / "DECISIONS.md").write_text(MINI_DECISIONS, encoding="utf-8")
    overlay_dir = tmp_path / "docs" / "ssi"
    overlay_dir.mkdir()
    (overlay_dir / "SSI_OVERLAY.md").write_text(MINI_OVERLAY, encoding="utf-8")
    (tmp_path / "tests").mkdir(exist_ok=True)
    (tmp_path / "tests" / "mini_arch.py").write_text("# crafted\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir(exist_ok=True)
    (tmp_path / "scripts" / "mini_lint.py").write_text("# crafted\n", encoding="utf-8")
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
    # the ssi-2 families: the control plane's absence is loud too
    assert any("SSI_OVERLAY.md: missing" in v for v in found)
    assert any("AGENTS.md: missing" in v for v in found)


# -- the SSI control-plane families (ssi-2, D-222/D-223) ------------------


def test_ssi_overlay_missing_is_loud(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    (root / "docs" / "ssi" / "SSI_OVERLAY.md").unlink()
    found = docguard.violations(root)
    assert any(
        "SSI_OVERLAY.md: missing" in v and "control-plane" in v for v in found
    )


def test_ssi_block_matrix_skip_and_state_vocabulary(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    # a skipped block (E removed) — SSI-N006
    _rewrite(root, docguard.SSI_OVERLAY, "| E | crafted | crafted | VERIFIED | crafted |\n", "")
    # an out-of-vocabulary state (D's NOT_APPLICABLE → DONE) — SSI-N007
    _rewrite(
        root,
        docguard.SSI_OVERLAY,
        "| D | crafted | none | NOT_APPLICABLE | reason= crafted |",
        "| D | crafted | none | DONE | reason= crafted |",
    )
    found = docguard.violations(root)
    assert any("missing ['E']" in v and "SSI-N006" in v for v in found)
    assert any("'D' state 'DONE'" in v and "SSI-N007" in v for v in found)


def test_ssi_implicit_waive_and_reasonless_skip(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    # a WAIVED row without owner=/reason=/expiry= — the explicit-waive law
    _rewrite(
        root,
        docguard.SSI_OVERLAY,
        "| B | crafted | crafted | OPEN | crafted |",
        "| B | crafted | crafted | WAIVED | crafted |",
    )
    # a NOT_APPLICABLE row without reason= — the explicit-skip law
    _rewrite(
        root,
        docguard.SSI_OVERLAY,
        "| D | crafted | none | NOT_APPLICABLE | reason= crafted |",
        "| D | crafted | none | NOT_APPLICABLE | crafted |",
    )
    found = docguard.violations(root)
    assert any("'B' WAIVED without" in v and "owner=" in v for v in found)
    assert any("'D' NOT_APPLICABLE without reason=" in v for v in found)


def test_ssi_rule_subset_and_instrument_drift(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    # a rule dropped from the declared subset + an instrument that
    # left the tree — SSI-N010: no drift between claims and reality
    _rewrite(
        root,
        docguard.SSI_OVERLAY,
        "| SSI-N020 | crafted | scripts/mini_lint.py | OPEN | crafted |\n",
        "",
    )
    _rewrite(
        root,
        docguard.SSI_OVERLAY,
        "| SSI-N001 | crafted | tests/mini_arch.py | VERIFIED | crafted |",
        "| SSI-N001 | crafted | tests/gone_arch.py | VERIFIED | crafted |",
    )
    found = docguard.violations(root)
    assert any("rule subset" in v and "declared eight" in v for v in found)
    assert any(
        "claims instrument tests/gone_arch.py" in v and "SSI-N010" in v
        for v in found
    )


def test_ssi_phase_gate_and_evidence_bar(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    # a silently-open phase (3's gate loses owner-gated) + an evidence
    # bar reduced to a snapshot (2 loses co-change/trajectory) — N018
    _rewrite(
        root,
        docguard.SSI_OVERLAY,
        "| 3 | ssi-4 | crafted | owner-gated | crafted |",
        "| 3 | ssi-4 | crafted | todo | crafted |",
    )
    _rewrite(
        root,
        docguard.SSI_OVERLAY,
        "| 2 | ssi-3 | crafted | owner-gated | co-change crafted |",
        "| 2 | ssi-3 | crafted | owner-gated | 1714 lines today |",
    )
    found = docguard.violations(root)
    assert any("phase 3 neither CLOSED nor owner-gated" in v for v in found)
    assert any("phase 2's evidence bar lacks" in v and "SSI-N018" in v for v in found)


def test_ssi_pcc_fields_on_risk_tagged_rows(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    # an R3+ row carrying the class tag but not the record — N017
    _rewrite(
        root,
        "docs/DECISIONS.md",
        "| D-002 | 2026-01-02 | the crafted second row | why | so |",
        "| D-002 | 2026-01-02 | the crafted (R3) row without its record | why | so |",
    )
    found = docguard.violations(root)
    assert any("R3+ row lacks the PCC fields" in v and "SSI-N017" in v for v in found)
    # the same row WITH the six markers stays clean
    _rewrite(
        root,
        "docs/DECISIONS.md",
        "the crafted (R3) row without its record | why | so |",
        "the crafted (R3) row | why | (R3) [PCC: intent= crafted; "
        "invariants= crafted; delta= crafted; verification= crafted; "
        "provenance= crafted; runtime= crafted] |",
    )
    assert docguard.violations(root) == []


def test_ssi_ladder_absence_breaks_the_pin(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    ladder = (
        "9. Risk ladder (crafted ssi row): R0–R2 the standing protocol; "
        "R3+\n   self-declares the class and carries the PCC record.\n"
    )
    _rewrite(root, "AGENTS.md", ladder, "9. Crafted law without the ladder.\n")
    found = docguard.violations(root)
    assert any("risk ladder" in v and "ssi-2/D-222" in v for v in found)


# -- the drift pin (the real repo: the recurrence fix's teeth) ------------


def test_guard_clean_on_the_real_repo() -> None:
    """The caps hold at HEAD: AGENTS §6's counts, the FAQ one-liner law,
    the worklog entry law, the TASKS ledger tail, the DECISIONS cap,
    and the docs cap with its allowlist — the bloat cannot silently
    regrow between owner housekeeping calls (the iter-140/151 lesson:
    both GC passes lacked exactly this executable check)."""
    assert docguard.violations(REPO) == []
