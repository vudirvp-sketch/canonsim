"""The mechanical cap guard (doc-3's recurrence fix, iter-176).

Law: AGENTS.md §6 (the cap table) + §5 (KI one-liners) + the restored
STATUS Next-step protocol (one rolling DONE block, iter-175). Lint =
CI, never taste (the L1 law applied to the state layer): every check
is a COUNT over a documented shape — no judgment calls. The doc-3 row
named this the recurrence fix the iter-140/151 GC passes lacked: the
caps are now executable, so the bloat cannot silently regrow between
owner housekeeping calls.

What is counted (the AGENTS §6 table, mechanically):

  STATUS.md    FAQ <= 20 entries, each entry <= 3 lines (the one-liner
               + owner-link form; essays are the failure mode);
               Active KIs <= 15, each <= 2 lines; Next step carries
               <= 1 rolling "iter-N DONE" block.
  worklog.md   <= 10 entries; each entry 3..5 lines (what/why/files).
  docs/TASKS.md  the iteration-ledger tail <= 10 one-liners; no
               "### iter-N" detailed-history headings anywhere (the
               three ledgars stay dead — "### bg-N" under Track B is
               that track's live one-liner form, allowed).
  docs/DECISIONS.md  <= 30 rows (compound-ID family rows count as 1).
  docs/**/*.md <= 600 lines unless in the ALLOWLIST below — the
               over-cap allowlist is documented HERE (the single
               place), each entry with its §6.1 rationale pointer.

Missing state docs are loud (a violation, never a crash); unreadable
shapes degrade to a violation line, not an exception. Read-only; zero
engine imports (pure stdlib, periphery D-046). Exit 0 = clean, 1 = the
violation list on stdout, one per line.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

#: The AGENTS §6 docs cap, with the standing over-cap allowlist — the
#: §6.1 substance holds (cruft passes done, measured substance kept);
#: the rationale records live where cited. A file leaves this table
#: only by a real cruft pass that brings it under the cap.
DOC_CAP = 600
ALLOWLIST: dict[str, str] = {
    "docs/TECH_NOTES.md":
        "the measured-substance record (§3.1–§3.3, §8–§15) — the §6.1 "
        "standing over-cap state, worklog iter-171/173",
    "docs/blueprint/phases.md":
        "the research archive per its own law (D-185) — §6's compact "
        "blocks the declared owner of the intake records",
    "docs/worldbuild/ANCHOR_REGION.md":
        "the authored unit's rungs/tables are substance (the iter-165 "
        "rationale — no cruft found in the pass)",
    "docs/BRIEF_SPEC.md":
        "the eight-block pipeline + budgets + render-format contract — "
        "substance-filtered spec (§2–§7)",
    "docs/ref/paradox_scripting.md":
        "the per-source deep dive's verdict tables and footgun catalog "
        "(§6.1 substance; 605 lines — the five over the cap are the "
        "verdict block's own sentences)",
    "docs/TEST_PLAN.md":
        "the verification stack (T0–T8 + M1–M5 + the gate protocol + "
        "§8/§8.5/§9) — substance-dense at the ceiling; the intake-34 "
        "empty-ablation line pushed the full stack over (cruft pass "
        "run: no filler found)",
    "docs/REDOT_ENGINE_INDEX.md":
        "the Redot engine reference index (iter-225, D-207) — the "
        "version firewall + the routing map for every engine/API/UI/"
        "networking/performance/export touch on the Redot surface; "
        "dense substance (the link catalog + the class routing + the "
        "networking/remote patterns + the proof checklists); the §6.1 "
        "cruft pass done at admission (the external changelog cut, the "
        "seams reconciled to the landed wb surface) — worklog iter-225 "
        "the record",
    "docs/worldbuild/WORLD_TESTS.md":
        "the W5 probe-run records are measured substance (the instrument "
        "protocols + the classified blind-reader results) — the §6.1 "
        "pointer passes done iter-191/192 (the form/gate/isolation "
        "restatements compressed to WORLD_WORKPLAN pointers), worklog "
        "iter-192 the record",
}

FAQ_MAX_ENTRIES = 20
FAQ_MAX_LINES = 3
KI_MAX = 15
KI_MAX_LINES = 2
DONE_BLOCK_MAX = 1
WORKLOG_MAX_ENTRIES = 10
WORKLOG_MIN_LINES = 3
WORKLOG_MAX_LINES = 5
LEDGER_MAX = 10
DECISIONS_MAX = 30

_ENTRY_RE = re.compile(r"^iter-\d+ · \d{4}-\d{2}-\d{2} · ")
_KI_RE = re.compile(r"^- KI#\d+")
_DONE_BLOCK_RE = re.compile(r"^\*\*iter-\d+ DONE")
_LEDGER_LINE_RE = re.compile(r"^- iter-\d+ · ")
_HISTORY_HEADING_RE = re.compile(r"^### iter-\d+ ")
_DECISION_ROW_RE = re.compile(r"^\| D-")


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


def _bullet_blocks(body: str, bullet_re: re.Pattern[str]) -> list[list[str]]:
    """Bullet blocks: a bullet line plus its indented continuation
    lines (blank lines separate blocks; `>` notes and plain prose are
    skipped)."""
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in body.splitlines():
        if bullet_re.match(line):
            current = [line]
            blocks.append(current)
        elif current is not None and line.startswith((" ", "\t")) and line.strip():
            current.append(line)
        elif line.strip():
            current = None
    return blocks


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
        return ["STATUS.md: missing (the state doc must exist)"]
    faq = _section(text, "FAQ / Pitfalls")
    if faq is None:
        out.append("STATUS.md: no '## FAQ / Pitfalls' section")
    else:
        blocks = _bullet_blocks(faq, re.compile(r"^- "))
        if len(blocks) > FAQ_MAX_ENTRIES:
            out.append(f"STATUS.md: {len(blocks)} FAQ entries (cap {FAQ_MAX_ENTRIES})")
        for block in blocks:
            if len(block) > FAQ_MAX_LINES:
                head = " ".join(block[0].split())[:60]
                out.append(
                    f"STATUS.md: FAQ entry over {FAQ_MAX_LINES} lines "
                    f"({len(block)}): {head}…"
                )
    kis = _section(text, "Active KIs")
    if kis is None:
        out.append("STATUS.md: no '## Active KIs' section")
    else:
        blocks = _bullet_blocks(kis, _KI_RE)
        if len(blocks) > KI_MAX:
            out.append(f"STATUS.md: {len(blocks)} active KIs (cap {KI_MAX})")
        for block in blocks:
            if len(block) > KI_MAX_LINES:
                out.append(
                    f"STATUS.md: KI over {KI_MAX_LINES} lines "
                    f"({len(block)}): {block[0][:60]}…"
                )
    step = _section(text, "Next step")
    if step is None:
        out.append("STATUS.md: no '## Next step' section")
    else:
        done_blocks = [ln for ln in step.splitlines() if _DONE_BLOCK_RE.match(ln)]
        if len(done_blocks) > DONE_BLOCK_MAX:
            out.append(
                f"STATUS.md: {len(done_blocks)} DONE blocks in Next step "
                f"(the rolling-block protocol: max {DONE_BLOCK_MAX})"
            )
    return out


def _worklog_checks(repo: Path) -> list[str]:
    out: list[str] = []
    text = _read(repo, "worklog.md")
    if text is None:
        return ["worklog.md: missing (the state doc must exist)"]
    entries: list[list[str]] = []
    for line in text.splitlines():
        if _ENTRY_RE.match(line):
            entries.append([])
        if not entries:
            continue
        if line.strip() and not line.startswith(("---", "#", ">")):
            entries[-1].append(line)
    if len(entries) > WORKLOG_MAX_ENTRIES:
        out.append(f"worklog.md: {len(entries)} entries (cap {WORKLOG_MAX_ENTRIES})")
    for entry in entries:
        n = len(entry)
        if not WORKLOG_MIN_LINES <= n <= WORKLOG_MAX_LINES:
            out.append(
                f"worklog.md: entry {entry[0][:40]}… is {n} lines "
                f"(the entry law: {WORKLOG_MIN_LINES}–{WORKLOG_MAX_LINES})"
            )
    return out


def _tasks_checks(repo: Path) -> list[str]:
    out: list[str] = []
    text = _read(repo, "docs/TASKS.md")
    if text is None:
        return ["docs/TASKS.md: missing (the state doc must exist)"]
    ledger = _section(text, "Iteration ledger", level="###")
    if ledger is None:
        out.append("docs/TASKS.md: no '### Iteration ledger' section")
    else:
        lines = [ln for ln in ledger.splitlines() if _LEDGER_LINE_RE.match(ln)]
        if len(lines) > LEDGER_MAX:
            out.append(
                f"docs/TASKS.md: the ledger tail is {len(lines)} one-liners "
                f"(cap {LEDGER_MAX}; older lines live in git)"
            )
    for line in text.splitlines():
        if _HISTORY_HEADING_RE.match(line):
            out.append(
                f"docs/TASKS.md: detailed history heading present "
                f"('{line[:60]}…') — done-detail lives in git + worklog "
                f"+ the owning docs (the header law)"
            )
    return out


def _decisions_checks(repo: Path) -> list[str]:
    text = _read(repo, "docs/DECISIONS.md")
    if text is None:
        return ["docs/DECISIONS.md: missing (the state doc must exist)"]
    rows = [ln for ln in text.splitlines() if _DECISION_ROW_RE.match(ln)]
    if len(rows) > DECISIONS_MAX:
        return [
            f"docs/DECISIONS.md: {len(rows)} rows (cap {DECISIONS_MAX}; "
            f"collapse fires on the owner's call, D-034/D-185)"
        ]
    return []


def _docs_cap_checks(repo: Path) -> list[str]:
    out: list[str] = []
    docs = repo / "docs"
    if not docs.is_dir():
        return ["docs/: missing"]
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(repo).as_posix()
        try:
            n = len(path.read_text(encoding="utf-8").splitlines())
        except OSError:
            out.append(f"{rel}: unreadable")
            continue
        if rel in ALLOWLIST:
            continue
        if n > DOC_CAP:
            out.append(
                f"{rel}: {n} lines (cap {DOC_CAP}; a §6.1 cruft pass first — "
                f"if substance remains, the file joins the guard's allowlist "
                f"with a rationale)"
            )
    return out


def violations(repo: Path) -> list[str]:
    """Every cap breach, one line each. Pure function of the repo tree."""
    out: list[str] = []
    out.extend(_status_checks(repo))
    out.extend(_worklog_checks(repo))
    out.extend(_tasks_checks(repo))
    out.extend(_decisions_checks(repo))
    out.extend(_docs_cap_checks(repo))
    return out


def main(argv: list[str] | None = None) -> int:
    repo = Path(argv[0]) if argv else REPO
    found = violations(repo)
    for line in found:
        print(f"docguard: {line}")
    if found:
        print(f"docguard: {len(found)} violation(s) — AGENTS §6 / the doc-3 guard")
        return 1
    print("docguard: clean (AGENTS §6 caps + the doc-3 state-layer shapes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
