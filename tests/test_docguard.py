"""The state-layer shape guard's suite (`scripts/docguard.py`; retrimmed for
the DSH-local law 2026-10-24); ssi-2 (D-222/D-223) — the SSI control-plane
shape families.

The laws this suite pins: (1) LINT = CI, NEVER TASTE — every check is a
shape or a resolvability fact, never a volume judgement (the old caps are
RETIRED law, AGENTS.md §11); (2) the crafted mini-repo carries a known
breach for every surviving family, each producing its own violation line;
(3) the drift pin — the real repo's state docs are clean at HEAD, so a future
edit that breaks a shape fails HERE; (4) the SSI families: the overlay's
block matrix / rule subset / phase ladder lint exactly their breaches, and an
R3+ decision row still carries its PCC record.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import docguard  # type: ignore[import-not-found]  # noqa: E402

MINI_STATUS = """\
# STATUS.md — the current state (crafted guard fixture)

**Phase.** 3 (Director) — CLOSED (crafted phases).
**Base.** crafted.
**Verification state.** 42 passed + 1 skipped, ruff clean (crafted).

## Active KIs

- KI#12 · the crafted open KI · 2026-01-01

## Next

1. The crafted next step.
"""

MINI_WORKLOG = """\
<!-- FROZEN 2026-10-24 (AGENTS.md §6.2): the sandbox-era memory. New entries are
     NOT written here; git log owns the per-change record. -->
---
iter-9 · 2026-01-02 · mini — the crafted frozen entry
"""

MINI_TASKS = """\
# TASKS

## Track A — main

- `world-9` · the crafted parked row —
  todo, owner-gated (crafted)

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
    (tmp_path / "docs" / "TECH_NOTES.md").write_text(
        "## 18. Operational pitfalls\n\n- crafted trap\n", encoding="utf-8"
    )
    iterations = tmp_path / "docs" / "iterations"
    iterations.mkdir()
    (iterations / "iter-9-mini-report.md").write_text("# crafted\n", encoding="utf-8")
    (iterations / "00_INDEX.md").write_text(
        "| 9 | `mini` | [iter-9-mini-report.md](iter-9-mini-report.md) | crafted report |\n",
        encoding="utf-8",
    )
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





def test_tasks_history_headings(tmp_path: Path) -> None:
    root = _mini(tmp_path)
    text = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
    history = "### iter-7 · crafted — done\n\nThe crafted detailed section."
    (root / "docs" / "TASKS.md").write_text(
        text + "\n" + history + "\n", encoding="utf-8"
    )
    found = docguard.violations(root)
    assert any("detailed history heading" in v for v in found)



def test_decisions_section_form_carries_the_pcc_duty(tmp_path: Path) -> None:
    """The iter-310 lesson survives the cap's retirement: a post-table
    ## D- section IS an entry, and an R3+ tag in the section form carries
    the same six-field PCC duty as an index row (SSI-N017)."""
    root = _mini(tmp_path)
    _rewrite(
        root,
        'docs/DECISIONS.md',
        '| D-002 | 2026-01-02 | the crafted second row | why | so |',
        '| D-002 | 2026-01-02 | the crafted second row | why | so |\n\n'
        '## D-003 -- the crafted (R3) section entry\n\nThe crafted body.',
    )
    assert any('R3+ row lacks the PCC fields' in v for v in docguard.violations(root))
    _rewrite(
        root,
        'docs/DECISIONS.md',
        '## D-003 -- the crafted (R3) section entry',
        '## D-003 -- the crafted (R3) section entry [PCC: intent= crafted; '
        'invariants= crafted; delta= crafted; verification= crafted; '
        'provenance= crafted; runtime= crafted]',
    )
    found = docguard.violations(root)
    assert not any('PCC fields' in v for v in found)


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
    """The shape pin at HEAD: the STATUS sections, the worklog banner, the
    TASKS headings, the D-ID resolvability, the report index and the SSI
    control-plane shapes — a state-doc edit that breaks a shape fails HERE
    (the iter-140/151 lesson: both GC passes lacked exactly this executable
    check)."""
    assert docguard.violations(REPO) == []


# -- the published tree (no state layer: degrade, never invent) -----------


def test_state_layer_absent_is_skipped_never_red(tmp_path: Path) -> None:
    """A checkout without `AGENTS.md` is the published tree: it carries no
    state docs, and every state-layer family degrades to SKIPPED — naming a
    missing STATUS.md there would fail CI on a clean clone."""
    (tmp_path / "docs").mkdir()
    assert docguard.violations(tmp_path) == []
    assert docguard.main([str(tmp_path)]) == 0


def test_state_layer_claimed_but_incomplete_stays_loud(tmp_path: Path) -> None:
    """`AGENTS.md` claims the state layer, so with the law file present the
    loud behaviour stands: a deleted state doc cannot hide behind the
    published-tree skip."""
    (tmp_path / "AGENTS.md").write_text("# law\n\nR3 PCC\n", encoding="utf-8")
    found = docguard.violations(tmp_path)
    assert any("STATUS.md: missing" in v for v in found)
    assert any("docs/TASKS.md: missing" in v for v in found)
