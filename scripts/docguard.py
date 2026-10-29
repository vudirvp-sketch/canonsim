"""The state-layer shape guard (doc-3's recurrence fix, iter-176; retrimmed
for the DSH-local law, 2026-10-24).

Law: AGENTS.md §6.1–§6.2 (one owner per fact; state docs are indexes) + §4
(the risk ladder and its PCC record). Lint = CI, never taste: every check is a
shape or a resolvability fact, never a judgment call.

What it checks now (the volume caps of the sandbox era are RETIRED — AGENTS.md
§11; they forced the deletion of state an agent needs):

  STATUS.md    exists; '## Active KIs' present;
               '## Next' present (the actions a successor starts from);
               the operational traps still live in docs/TECH_NOTES.md §18
               (they must not be lost with the old FAQ section).
  worklog.md   exists and carries its FROZEN banner (new entries are not
               written there: git log owns the per-change record).
  docs/TASKS.md  no "### iter-N" detailed-history headings (done-detail
               lives in git + docs/iterations).
  docs/DECISIONS.md  the index exists and, together with
               docs/decisions/*.md, resolves every D-ID cited in STATUS.md,
               docs/TASKS.md, docs/AGENT_NAVIGATION.md, README.md, AGENTS.md.
  docs/iterations/00_INDEX.md  every report listed, every listed report on
               disk (an unlisted report is invisible; a listed ghost is a
               dangling link).
  AGENTS.md    the risk ladder stands (R0–R5 + the PCC markers of §4) and an
               R3+ decision row carries the six PCC field markers
               (SSI-N017 proof-carrying-change).
  docs/ssi/SSI_OVERLAY.md  the SSI control plane's own shape: the A–L block
               matrix complete with every state inside the closed vocabulary
               {NOT_APPLICABLE, OPEN, PARTIAL, VERIFIED, WAIVED}, the declared
               rule subset with its instruments on disk, the phase ladder
               owner-gated, N018's evidence bar on phases 2/4.

The state layer is a LOCAL overlay, and `AGENTS.md` is its claim: a checkout
that carries the law file is checked strictly (a missing state doc stays a
violation), while a checkout without it — the published clone — skips every
state-layer family instead of naming files it is not supposed to have. The
skip is printed, never silent. Unreadable shapes degrade to a violation line,
not an exception. Read-only; zero engine imports (pure stdlib, periphery
D-046). Exit 0 = clean, 1 = the violation list on stdout, one per line.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _strict(repo: Path) -> bool:
    """Is the state layer claimed in this checkout? `AGENTS.md` is the claim
    (the file the harness loads as law): a tree without it is the published
    tree, which carries no state docs by design."""
    return (repo / "AGENTS.md").exists()

#: The state-layer shapes (AGENTS.md §6.1–§6.2). These are FORM and
#: RESOLVABILITY checks — never volume budgets: the caps were retired with the
#: sandbox era (§11), and deleting a fact to fit a line count is the crutch the
#: law forbids.

_HISTORY_HEADING_RE = re.compile(r"^### iter-\d+ ")
_DECISION_ROW_RE = re.compile(r"^\| D-")
_DECISION_SECTION_RE = re.compile(r"^#{2,3} D-")
_D_ID_RE = re.compile(r"D-\d+")
_ITERATION_LISTED_RE = re.compile(r"\((iter-\d+-[^)]+\.md)\)")



SSI_OVERLAY = "docs/ssi/SSI_OVERLAY.md"
#: The SSI block index (00_INDEX.md's A–L) — completeness is the
#: no-silent-skip law (SSI-N006): a missing block row is a skipped
#: block.
SSI_BLOCKS = "ABCDEFGHIJKL"
#: manifest.yaml's own closed state vocabulary — a state string
#: outside it is an invalid state encoded only as convention
#: (SSI-N007).
SSI_BLOCK_STATES = frozenset(
    {"NOT_APPLICABLE", "OPEN", "PARTIAL", "VERIFIED", "WAIVED"}
)
#: D-223's declared executable subset — the owner's chosen eight
#: (never all twenty; the other twelve stay reference-only).
SSI_RULES = frozenset(f"SSI-N{n:03d}" for n in (1, 2, 6, 7, 10, 17, 18, 20))
#: The compact PCC record's six field markers (AGENTS §2.9 — the
#: DECISIONS-row form of templates/proof-carrying-change.md).
SSI_PCC_FIELDS = (
    "intent=",
    "invariants=",
    "delta=",
    "verification=",
    "provenance=",
    "runtime=",
)
#: An R3+ row's self-declared class tag (AGENTS §2.9's ladder).
_SSI_RISK_TAG_RE = re.compile(r"\(R[345]\)")
#: The explicit-waive law (the package README: "WAIVED is never
#: implicit; it requires owner + reason + expiry").
SSI_WAIVE_FIELDS = ("owner=", "reason=", "expiry=")
#: A repo-rooted instrument path (the rule table's Instrument column
#: grammar: at least one directory component + a file extension).
_SSI_INSTRUMENT_RE = re.compile(
    r"(?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]+\.(?:py|md|yaml|json)"
)
#: The phase ladder (the owner's ssi plan, TASKS ssi-1..ssi-8).
SSI_PHASES = "01234567"
#: SSI-N018's evidence family — the trajectory terms a Phase 2/4
#: row's evidence bar must name (a snapshot alone is never health).
SSI_EVIDENCE_TERMS = ("co-change", "trajectory")
_SSI_BLOCK_ROW_RE = re.compile(r"^\| [A-L] \|")
_SSI_RULE_ROW_RE = re.compile(r"^\| SSI-N\d{3} \|")
_SSI_PHASE_ROW_RE = re.compile(r"^\| [0-7] \|")


def _section(text: str, heading: str, level: str = "##") -> str | None:
    """The section body: from `<level> <heading>` (a prefix match — the
    heading line may continue with a parenthetical) to the next heading
    at the same or higher level, or EOF; None when the heading is
    absent."""
    marker = f"{level} {heading}"
    start = None
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(marker):
            start = i + 1
            break
    if start is None:
        return None
    depth = len(level)
    body: list[str] = []
    for line in lines[start:]:
        if line.startswith("#"):
            m = re.match(r"^(#+) ", line)
            if m and len(m.group(1)) <= depth:
                break
        body.append(line)
    return "\n".join(body)


def _read(repo: Path, rel: str) -> str | None:
    path = repo / rel
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _status_checks(repo: Path) -> list[str]:
    out: list[str] = []
    text = _read(repo, "STATUS.md")
    if text is None:
        if not _strict(repo):
            return []
        return ["STATUS.md: missing (the state doc must exist)"]
    if _section(text, "Active KIs") is None:
        out.append("STATUS.md: no '## Active KIs' section")
    if _section(text, "Next") is None:
        out.append(
            "STATUS.md: no '## Next' section (the actions a successor starts from)"
        )
    tech = _read(repo, "docs/TECH_NOTES.md") or ""
    if "## 18. Operational pitfalls" not in tech:
        out.append(
            "docs/TECH_NOTES.md: §18 (the operational traps moved out of STATUS) "
            "is absent — STATUS would be the only copy"
        )
    return out


def _worklog_checks(repo: Path) -> list[str]:
    """The file is frozen (AGENTS.md §6.2): it exists for its citations and
    must say so, because the next agent would otherwise write into it."""
    text = _read(repo, "worklog.md")
    if text is None:
        if not _strict(repo):
            return []
        return ["worklog.md: missing (docs cite it — delete only via a citation sweep)"]
    head = "\n".join(text.splitlines()[:12])
    if "FROZEN 2026-10-24" not in head:
        return [
            "worklog.md: the FROZEN banner is absent — new entries must not be "
            "written here (git log owns the per-change record)"
        ]
    return []


def _tasks_checks(repo: Path) -> list[str]:
    out: list[str] = []
    text = _read(repo, "docs/TASKS.md")
    if text is None:
        if not _strict(repo):
            return []
        return ["docs/TASKS.md: missing (the state doc must exist)"]
    for line in text.splitlines():
        if _HISTORY_HEADING_RE.match(line):
            out.append(
                f"docs/TASKS.md: detailed history heading present "
                f"('{line[:60]}…') — done-detail lives in git + docs/iterations"
            )
    return out


def _decisions_checks(repo: Path) -> list[str]:
    """The decision index must resolve every D-ID the agent-facing docs cite,
    and the R3+ PCC shape is pinned where it is read (AGENTS.md §4)."""
    out: list[str] = []
    index = _read(repo, "docs/DECISIONS.md")
    if index is None:
        if not _strict(repo):
            return []
        return ["docs/DECISIONS.md: missing (the decision index must exist)"]
    corpus = index
    decisions_dir = repo / "docs" / "decisions"
    if decisions_dir.is_dir():
        for path in sorted(decisions_dir.glob("*.md")):
            corpus += "\n" + (_read(repo, path.relative_to(repo).as_posix()) or "")
    known = set(_D_ID_RE.findall(corpus))
    for rel in ("STATUS.md", "docs/TASKS.md", "docs/AGENT_NAVIGATION.md", "README.md", "AGENTS.md"):
        cited = _read(repo, rel)
        if cited is None:
            continue
        for lineno, line in enumerate(cited.splitlines(), 1):
            for d in _D_ID_RE.findall(line):
                if d not in known:
                    out.append(
                        f"{rel}:{lineno}: {d} does not resolve in "
                        f"docs/DECISIONS.md + docs/decisions/"
                    )
    return out


def _iterations_checks(repo: Path) -> list[str]:
    """The report index is the archive's only entry point: a report the index
    omits is invisible, and a listed report that is gone is a dangling link."""
    out: list[str] = []
    index = _read(repo, "docs/iterations/00_INDEX.md")
    if index is None:
        if not _strict(repo):
            return []
        return ["docs/iterations/00_INDEX.md: missing (the report index must exist)"]
    listed = set(_ITERATION_LISTED_RE.findall(index))
    actual = {p.name for p in (repo / "docs" / "iterations").glob("iter-*.md")}
    for name in sorted(actual - listed):
        out.append(f"docs/iterations/{name}: a report the index does not list")
    for name in sorted(listed - actual):
        out.append(f"docs/iterations/00_INDEX.md: lists {name}, which does not exist")
    return out


# -- the SSI control-plane shapes (ssi-2/D-222, ssi-2/D-223) -------------


def _cells(row: str) -> list[str]:
    """A markdown table row's cells, stripped (the overlay's tables
    never carry a literal `|` inside a cell — the row grammar the
    checks below count over)."""
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def _ssi_overlay_checks(repo: Path) -> list[str]:
    """The control plane's own shape — the overlay IS executable:
    SSI-N006 (the block matrix complete, every skip explicit),
    SSI-N007 (the closed state vocabulary), D-223's declared
    eight-rule subset with its instruments on disk (SSI-N010), the
    phase ladder owner-gated beyond CLOSED with N018's evidence bar
    on phases 2/4. A missing overlay is loud, never a silent skip."""
    out: list[str] = []
    text = _read(repo, SSI_OVERLAY)
    if text is None:
        if not _strict(repo):
            return []
        return [
            f"{SSI_OVERLAY}: missing (the SSI control-plane overlay — "
            "ssi-2/D-222; the block matrix, the rule subset, and the "
            "phase ladder all lint here)"
        ]
    lines = text.splitlines()
    block_rows = [ln for ln in lines if _SSI_BLOCK_ROW_RE.match(ln)]
    rule_rows = [ln for ln in lines if _SSI_RULE_ROW_RE.match(ln)]
    phase_rows = [ln for ln in lines if _SSI_PHASE_ROW_RE.match(ln)]
    blocks = [_cells(r)[0] for r in block_rows if _cells(r)]
    if sorted(blocks) != sorted(SSI_BLOCKS):
        missing = sorted(set(SSI_BLOCKS) - set(blocks))
        dupes = sorted({b for b in blocks if blocks.count(b) > 1})
        out.append(
            f"{SSI_OVERLAY}: block matrix {sorted(blocks)} != A–L "
            f"(missing {missing or []}, duplicated {dupes or []} — "
            "SSI-N006: no silent block skip)"
        )
    rules = {_cells(r)[0] for r in rule_rows if _cells(r)}
    if rules != SSI_RULES:
        out.append(
            f"{SSI_OVERLAY}: rule subset {sorted(rules)} != D-223's "
            f"declared eight {sorted(SSI_RULES)}"
        )
    phases = [_cells(r)[0] for r in phase_rows if _cells(r)]
    if sorted(phases) != sorted(SSI_PHASES):
        out.append(
            f"{SSI_OVERLAY}: phase ladder {phases} != 0..7 (the "
            "owner's ssi phase plan, TASKS ssi-1..ssi-8)"
        )
    for row in block_rows + rule_rows:
        cells = _cells(row)
        if len(cells) < 4:
            continue
        state = cells[3]
        if state not in SSI_BLOCK_STATES:
            out.append(
                f"{SSI_OVERLAY}: '{cells[0]}' state {state!r} outside "
                "the closed vocabulary "
                f"{sorted(SSI_BLOCK_STATES)} (SSI-N007)"
            )
    for row in block_rows + rule_rows:
        cells = _cells(row)
        if len(cells) < 5:
            continue
        evidence = cells[4]
        if cells[3] == "WAIVED":
            lacking = [f for f in SSI_WAIVE_FIELDS if f not in evidence]
            if lacking:
                out.append(
                    f"{SSI_OVERLAY}: '{cells[0]}' WAIVED without "
                    f"{lacking} (the explicit-waive law — never implicit)"
                )
        if cells[3] == "NOT_APPLICABLE" and "reason=" not in evidence:
            out.append(
                f"{SSI_OVERLAY}: '{cells[0]}' NOT_APPLICABLE without "
                "reason= (the explicit-skip law)"
            )
    for row in rule_rows:
        cells = _cells(row)
        if len(cells) < 3:
            continue
        for token in _SSI_INSTRUMENT_RE.findall(cells[2]):
            if not (repo / token).exists():
                out.append(
                    f"{SSI_OVERLAY}: '{cells[0]}' claims instrument "
                    f"{token} — not on disk (SSI-N010: no drift between "
                    "the control plane and the tree)"
                )
    for row in phase_rows:
        cells = _cells(row)
        if len(cells) < 5:
            continue
        phase, gate, evidence = cells[0], cells[3], cells[4]
        if "CLOSED" not in gate and "owner-gated" not in gate:
            out.append(
                f"{SSI_OVERLAY}: phase {phase} neither CLOSED nor "
                "owner-gated (a silently-open phase)"
            )
        if phase in ("2", "4") and not any(t in evidence for t in SSI_EVIDENCE_TERMS):
            out.append(
                f"{SSI_OVERLAY}: phase {phase}'s evidence bar lacks "
                f"{SSI_EVIDENCE_TERMS} (SSI-N018 — a line-count "
                "snapshot is never architecture health)"
            )
    return out


def _ssi_pcc_checks(repo: Path) -> list[str]:
    """SSI-N017 executable (AGENTS §2.9): a DECISIONS entry that
    self-declares R3+ — a `(R3)`/`(R4)`/`(R5)` tag, in the table-row
    OR the post-table section form — must carry the compact PCC
    record's six field markers. Green-and-armed: the first R3+ entry
    that ships without its proof goes red here."""
    text = _read(repo, "docs/DECISIONS.md")
    if text is None:
        return []
    out: list[str] = []
    for line in text.splitlines():
        is_entry = _DECISION_ROW_RE.match(line) or _DECISION_SECTION_RE.match(
            line
        )
        if is_entry and _SSI_RISK_TAG_RE.search(line):
            lacking = [f for f in SSI_PCC_FIELDS if f not in line]
            if lacking:
                out.append(
                    "docs/DECISIONS.md: an R3+ row lacks the PCC fields "
                    f"{lacking} (SSI-N017 proof-carrying-change, "
                    "AGENTS §2.9 — the row carries the class tag but "
                    "not the record)"
                )
    return out


def _agents_ladder_checks(repo: Path) -> list[str]:
    """The risk ladder drift pin (ssi-2/D-222): AGENTS §2.9 stands —
    the R3 ladder + the PCC record markers. A deleted ladder makes
    every overlay citation of §2.9 a dangling law; the pin holds the
    two documents together (the heading-presence family's own form)."""
    text = _read(repo, "AGENTS.md")
    if text is None:
        # No law file — no claimed state layer: the published tree.
        return []
    if "R3" not in text or "PCC" not in text:
        return [
            "AGENTS.md: the risk ladder (§4 — the R0–R5 classes + "
            "the PCC record) is absent (ssi-2/D-222; the overlay and "
            "AGENTS §2.9 drift apart)"
        ]
    return []


def violations(repo: Path) -> list[str]:
    """Every state-layer violation, one line each. Pure function of the tree."""
    out: list[str] = []
    out.extend(_status_checks(repo))
    out.extend(_worklog_checks(repo))
    out.extend(_tasks_checks(repo))
    out.extend(_decisions_checks(repo))
    out.extend(_iterations_checks(repo))
    out.extend(_ssi_overlay_checks(repo))
    out.extend(_ssi_pcc_checks(repo))
    out.extend(_agents_ladder_checks(repo))
    return out


def main(argv: list[str] | None = None) -> int:
    repo = Path(argv[0]) if argv else REPO
    found = violations(repo)
    for line in found:
        print(f"docguard: {line}")
    if found:
        print(f"docguard: {len(found)} violation(s) — the state-layer shapes (AGENTS.md §6)")
        return 1
    if _strict(repo):
        print("docguard: clean (the state-layer shapes of AGENTS.md §6)")
    else:
        print(
            "docguard: clean (published tree — the state layer is a local "
            "overlay, absent here: 0 state shapes checked)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
