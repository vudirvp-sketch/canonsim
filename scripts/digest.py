"""The repo digest (iter-108, the risk-synthesis §6 rider — the one
confirmed real gap: no generated human-readable summary of the three
state-owning docs).

The DERIVED-ONLY law: every line the digest prints is quoted+truncated
source text, or a count of source rows — never a computed metric, never
restated state, never advice. STATUS.md / docs/TASKS.md /
docs/DECISIONS.md stay the single owners; the digest is a viewport, not
a second source of truth. If a line here drifts from a doc, the doc
wins and this parser is the bug (the drift pin lives in
tests/test_digest.py).

Robustness follows the doctor's law: an unparsable shape prints itself
as (unparsed) instead of crashing — the digest never guesses past the
data. A missing doc is loud (exit 1); a malformed one is honest. No
wall-clock anywhere: the date shown is STATUS.md's own Date line (INV-2's
hygiene extended to derived artifacts, the scaffold's precedent).
Read-only: writes nothing, owns nothing. Zero engine imports — not even
`core` (pure stdlib file parsing; the chronicler's no-core decoupling
was its mode-F special case, this is the general case).

Periphery (D-046): reads docs, prints, never touches the engine.

Usage:
    python -m scripts.digest                 # the one-pager
    python -m scripts.digest --decisions 12  # a deeper decisions tail
    python -m scripts.digest <repo>          # a fork's docs
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

#: Extraction widths — one page stays one page (the caps are the law's
#: mechanical half; every cut carries an ellipsis so the reader knows).
_HEADLINE = 80  # a decision row's bold headline
_LEAD = 180  # the next-step bold lead
_LINE = 92  # any single quoted line
_ELLIPSIS = "…"

_ITERATION_RE = re.compile(r"^Iteration: (\S+)")
_TAG_RE = re.compile(r"`([^`]+)`")
_PHASE_RE = re.compile(r"^Phase: (\d+ [^(]*\([^)]*\))\s*—\s*([A-Z]+)")
_TESTS_RE = re.compile(r"^(\d+ passed[^\n,]*), ruff clean")
_DATE_RE = re.compile(r"^Date: (\d{4}-\d{2}-\d{2})")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)
_KI_RE = re.compile(r"^- (KI#\d+.*)")
_ROW_RE = re.compile(r"^- `([a-z0-9-]+)` ")
_TODO_HEADING_RE = re.compile(r"^### ((?:iter|bg)-\d+) ·.*— todo")
_DONE_HEADING_RE = re.compile(r"^### ((?:iter|bg)-\d+) · (.*?)(?: — done| — LANDED)")
#: The decision row: id(s), date, the decision cell up to the Why
#: column — bold optional (the pre-collapse rows predate the ** law);
#: compound ids join by `/` and by `..` ranges, dates may carry a
#: `..` range tail (D-084..D-093 family merges — the iter-176 fix:
#: the range forms never counted before, 25 of 30 rows).
_DECISION_RE = re.compile(
    r"^\| ((?:D-\d+)(?:(?:/|\.\.)D-\d+)*) \| "
    r"(\d{4}-\d{2}-\d{2}(?:\.\.[\d-]+)?) \| (.*?) \|"
)
_ITEM_RE = re.compile(r"^(\d+)\. (.*)")
#: The TASKS iteration-ledger one-liner (the doc-3 shape): the ledger
#: is the landings source now that the detailed history sections are
#: dead (git owns them); the title cuts at the first parenthetical or
#: colon, the heading form below stays for older/mini shapes.
_LEDGER_RE = re.compile(r"^- ((?:iter|bg)-\d+) · \d{4}-\d{2}-\d{2} · (.*?)(?: \(|:|$)")


def _unparsed() -> str:
    """The honest miss: a shape the parser does not recognize."""
    return "(unparsed)"


def _trunc(text: str, width: int) -> str:
    """The hard cut for quoted sentences (leads, items, KI lines): the
    words are the doc's own — cut only at the width, at a word
    boundary, never at a boundary the digest would be choosing. The
    ellipsis marks it."""
    text = text.strip()
    if len(text) <= width:
        return text
    cut = text[: width - 1].rsplit(" ", 1)[0]
    return cut.rstrip(" —,;") + _ELLIPSIS


def _cut(text: str, width: int) -> str:
    """Truncate at a natural boundary when one lands inside the width
    (a `:` or an em-dash clause — the decision rows' headline rhythm),
    else the hard cut. Never silently: the ellipsis marks every cut."""
    text = text.strip()
    for marker in (":", " — "):
        at = text.find(marker)
        if 0 < at <= width:
            return text[:at].rstrip(" —")
    return _trunc(text, width)


def _section(text: str, heading: str) -> str | None:
    """The section body: from `## <heading>` to the next `## ` or EOF.
    None when the heading is absent — the caller decides what that
    means (a missing section is a fact, not a crash)."""
    start = None
    for i, line in enumerate(text.splitlines()):
        if re.match(rf"^## {re.escape(heading)}\s*$", line):
            start = i + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for line in text.splitlines()[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def _status_fields(text: str) -> dict[str, str]:
    """The header block's five anchored fields (everything before the
    first `## ` heading — the re-pin shape every iteration follows)."""
    header = text.split("\n## ", 1)[0]
    fields: dict[str, str] = {}
    lines = header.splitlines()

    def first(pattern: re.Pattern[str]) -> str:
        for line in lines:
            m = pattern.match(line)
            if m:
                return m.group(1)
        return _unparsed()

    fields["iteration"] = first(_ITERATION_RE)
    tag = _TAG_RE.search(lines[0]) if lines else None
    fields["tag"] = tag.group(1) if tag else _unparsed()
    phase = _PHASE_RE.match(
        next((src for src in lines if src.startswith("Phase:")), ""))
    fields["phase"] = phase.group(1) if phase else _unparsed()
    fields["state"] = phase.group(2) if phase else _unparsed()
    fields["tests"] = first(_TESTS_RE)
    fields["date"] = first(_DATE_RE)
    return fields


def _next_step(text: str, items: int) -> list[str]:
    """The next step in STATUS.md's own words: the bold lead, then the
    first line of each numbered item — quoted, de-markdowned, cut."""
    body = _section(text, "Next step")
    if body is None:
        return ["(no Next step section)"]
    lead = _BOLD_RE.search(body)
    out: list[str] = []
    if lead:
        collapsed = " ".join(lead.group(1).split()).replace("**", "")
        out.append(_trunc(collapsed, _LEAD))
    else:
        plain = [src for src in body.splitlines() if src.strip()]
        out.extend(_trunc(src.strip(), _LINE) for src in plain[: items + 2])
    count = 0
    for line in body.splitlines():
        m = _ITEM_RE.match(line)
        if m and count < items:
            count += 1
            out.append(f"{m.group(1)}. {_trunc(m.group(2).replace('**', ''), _LINE)}")
    return out


def _active_kis(text: str) -> str:
    """The open-KI census: lines shaped `- KI#N · ...` (the AGENTS §5
    open shape). Deletion notes and '(None ...)' summaries carry no
    match — none active is a derived verdict, not an assumption."""
    body = _section(text, "Active KIs")
    if body is None:
        return "(no Active KIs section)"
    kis = [m.group(1).strip() for m in map(_KI_RE.match, body.splitlines()) if m]
    if not kis:
        return "none active"
    shown = ", ".join(_trunc(k, 60) for k in kis[:15])
    return f"{len(kis)}: {shown}" + (" (+more)" if len(kis) > 15 else "")


def _open_rows(text: str) -> list[str]:
    """The todo census over TASKS.md: dash-rows whose id + following
    line carry `todo` (rows wrap; the flag often lands on line two),
    plus bg/iter headings flagged todo. A census, not an order —
    TASKS owns composition, never order (STATUS.md FAQ's law)."""
    lines = text.splitlines()
    ids: list[str] = []
    for i, line in enumerate(lines):
        m = _ROW_RE.match(line)
        if m:
            window = line + " " + (lines[i + 1] if i + 1 < len(lines) else "")
            if "todo" in window:
                ids.append(m.group(1))
                continue
        h = _TODO_HEADING_RE.match(line)
        if h:
            ids.append(h.group(1))
    return ids


def _landings(text: str, count: int) -> list[str]:
    """The main track's recent done work, ordered by the iteration ids'
    own numbering: the iteration-ledger one-liners (the doc-3 shape —
    TASKS' history sections are dead, the tail carries the record) and
    the legacy `### iter-N — done` headings (the mini-repo fixture
    keeps that shape). `iter-N` is the repo's own clock; `bg-N` is a
    different sequence, not ranked against `iter-N`."""
    done: dict[int, str] = {}
    for m in map(_DONE_HEADING_RE.match, text.splitlines()):
        if m and m.group(1).startswith("iter-"):
            done[int(m.group(1)[5:])] = _trunc(m.group(2), 40)
    for m in map(_LEDGER_RE.match, text.splitlines()):
        if m and m.group(1).startswith("iter-"):
            done[int(m.group(1)[5:])] = _trunc(m.group(2), 40)
    return [f"iter-{n} {done[n]}" for n in sorted(done, reverse=True)[:count]]


def _decisions_tail(text: str, count: int) -> tuple[list[str], int]:
    """The last N decision rows as `D-xxx · date · headline` (the file
    is append-only chronological; the tail IS the recent state)."""
    rows = [
        (m.group(1), m.group(2), m.group(3))
        for m in map(_DECISION_RE.match, text.splitlines())
        if m
    ]
    tail = [f"{d} · {t} · {_cut(b.replace('**', ''), _HEADLINE)}" for d, t, b in rows[-count:]]
    return tail, len(rows)


def render(repo: Path, *, decisions: int = 8, items: int = 4) -> str:
    """Assemble the one-pager. Pure function of the three docs — same
    docs, same bytes (the determinism pin's contract)."""
    status = (repo / "STATUS.md").read_text(encoding="utf-8")
    tasks = (repo / "docs" / "TASKS.md").read_text(encoding="utf-8")
    decisions_text = (repo / "docs" / "DECISIONS.md").read_text(encoding="utf-8")

    head = _status_fields(status)
    step = _next_step(status, items)
    open_ids = _open_rows(tasks)
    landed = _landings(tasks, 4)
    tail, total = _decisions_tail(decisions_text, decisions)

    out: list[str] = [
        "canonsim — the digest (derived from STATUS.md · docs/TASKS.md · "
        "docs/DECISIONS.md — never a second source of truth)",
        f"iteration: {head['iteration']} ({head['tag']}) · {head['date']}",
        f"phase:     {head['phase']} — {head['state']}",
        f"tests:     {head['tests']}",
        f"KIs:       {_active_kis(status)}",
        f"next step: {step[0]}",
    ]
    out.extend(f"  {line}" for line in step[1:])
    if open_ids:
        shown = ", ".join(open_ids[:12])
        more = f" (+{len(open_ids) - 12} more)" if len(open_ids) > 12 else ""
        out.append(f"backlog:   {len(open_ids)} todo-flagged rows: {shown}{more}")
    else:
        out.append("backlog:   no todo-flagged rows")
    out.append("landings:  " + (" · ".join(landed) if landed else "(none)"))
    out.append(f"decisions: last {len(tail)} of {total} rows (docs/DECISIONS.md)")
    out.extend(f"  {row}" for row in tail)
    return "\n".join(out)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="digest",
        description="The derived one-pager over STATUS/TASKS/DECISIONS: "
                    "iteration, phase, test line, next step, KI census, "
                    "backlog shape, the decisions tail. Read-only; the "
                    "docs stay the single source of truth",
    )
    parser.add_argument("repo", type=Path, nargs="?", default=REPO,
                        help="the repo root (default: this repo)")
    parser.add_argument("--decisions", type=int, default=8,
                        help="how many decision rows to tail (default: 8)")
    args = parser.parse_args(argv)

    try:
        page = render(args.repo, decisions=max(1, args.decisions))
    except OSError as exc:
        print(f"error: cannot read the state docs under {args.repo}: {exc}",
              file=sys.stderr)
        return 1
    print(page)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
