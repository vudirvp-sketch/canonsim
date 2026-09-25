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
  docs/DECISIONS.md  <= 30 rows (compound-ID family rows count as 1);
               an R3+ row (a `(R3)`/`(R4)`/`(R5)` tag, AGENTS §2.9)
               must carry the six PCC field markers — intent=,
               invariants=, delta=, verification=, provenance=,
               runtime= (SSI-N017 proof-carrying-change, ssi-2/D-222).
  AGENTS.md    the risk ladder must stand (the R0–R5 + PCC markers
               of §2.9 — a deleted ladder goes red, ssi-2/D-222).
  docs/ssi/SSI_OVERLAY.md  the SSI control plane's own shape (the
               ssi-2/D-222 families): the A–L block matrix COMPLETE
               with every state inside the closed vocabulary
               {NOT_APPLICABLE, OPEN, PARTIAL, VERIFIED, WAIVED}
               (SSI-N006 no-silent-skip + SSI-N007 illegal-states-
               unrepresentable); a WAIVED row carries owner=/reason=/
               expiry=, a NOT_APPLICABLE row carries reason= (the
               package's own anti-skipping laws); the declared
               eight-rule subset complete (SSI-N001/002/006/007/010/
               017/018/020, D-223) with every claimed instrument on
               disk (SSI-N010 — no drift between the control plane
               and the tree); the phase ladder 0..7 with every
               non-CLOSED phase explicitly owner-gated, and phases
               2/4 carrying co-change/trajectory evidence (SSI-N018
               — a snapshot is never architecture health).
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
    "docs/FRONTEND_UIUX_LAW.md":
        "the frontend UI/UX law (iter-233, D-214) — the distilled "
        "binding form of the owner's Ultimate Frontend/UI/UX/Visual "
        "Architecture pack over the WHOLE frontend domain (27 law "
        "sections: the interaction grammar + the epistemic grammar + "
        "the accessibility/localization/responsive contracts + the "
        "verification matrix + the invariants); substance-dense at "
        "the ceiling — the §6.1 cruft pass done at admission (three "
        "compression rounds: 632→627; the enum/field/invariant lists "
        "are the substance §6.1 names as never-cut) — worklog "
        "iter-233 the record",
    "docs/WORKBENCH_APP_LAW.md":
        "the Workbench application/runtime architecture law (iter-237, "
        "D-218) — the binding distillation of the external app spec "
        "with the §-numbering preserved 1:1 (the design: every "
        "existing `app §N` citation resolves without edits); the "
        "34-section contract set (the ownership tables + the state "
        "vocabularies + the four lifecycle machines + the dispatch/"
        "failure matrices + the §30/§33 checklists + the LANDED/"
        "CONTRACT markers) is the §6.1 never-cut substance; two "
        "compression rounds done (849→784: prose tightened, absorbed "
        "sections §27/§28/§31 collapsed to pointers) — cutting "
        "further would cut the §-preserving contract load itself — "
        "worklog iter-237 the record",
    "docs/worldbuild/WORLD_TESTS.md":
        "the W5 probe-run records are measured substance (the instrument "
        "protocols + the classified blind-reader results) — the §6.1 "
        "pointer passes done iter-191/192 (the form/gate/isolation "
        "restatements compressed to WORLD_WORKPLAN pointers), worklog "
        "iter-192 the record",
    "docs/ssi/software-semantic-integrity-unified-v3.md":
        "the SSIEC-v3 canonical doctrine — the READ-ONLY reference copy "
        "(ssi-2/D-222): the external package verbatim, never edited "
        "in-repo, the overlay (SSI_OVERLAY.md) the only authored file; "
        "the docs/blueprint/phases.md research-archive precedent (§6.1)",
    "docs/ssi/software-semantic-integrity-unified-v2.md":
        "the prior canonical supplement retained for traceability — the "
        "READ-ONLY reference copy (ssi-2/D-222), the same §6.1 class as "
        "the v3 doctrine file above",
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

# -- the SSI control-plane shapes (ssi-2/D-222, ssi-2/D-223) -------------

#: The overlay home — the ONE authored file over the read-only
#: reference copy (docs/ssi/). Its tables ARE the executable control
#: plane: the shapes below are counts over documented forms, never
#: taste (the module's own law).
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
    """SSI-N017 executable (AGENTS §2.9): a DECISIONS row that
    self-declares R3+ — a `(R3)`/`(R4)`/`(R5)` tag — must carry the
    compact PCC record's six field markers. Green-and-armed: the
    first R3+ row that ships without its proof goes red here."""
    text = _read(repo, "docs/DECISIONS.md")
    if text is None:
        return []
    out: list[str] = []
    for line in text.splitlines():
        if _DECISION_ROW_RE.match(line) and _SSI_RISK_TAG_RE.search(line):
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
        return ["AGENTS.md: missing (the operating law must exist)"]
    if "R3" not in text or "PCC" not in text:
        return [
            "AGENTS.md: the risk ladder (§2.9 — the R0–R5 classes + "
            "the PCC record) is absent (ssi-2/D-222; the overlay and "
            "AGENTS §2.9 drift apart)"
        ]
    return []


def violations(repo: Path) -> list[str]:
    """Every cap breach, one line each. Pure function of the repo tree."""
    out: list[str] = []
    out.extend(_status_checks(repo))
    out.extend(_worklog_checks(repo))
    out.extend(_tasks_checks(repo))
    out.extend(_decisions_checks(repo))
    out.extend(_docs_cap_checks(repo))
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
        print(f"docguard: {len(found)} violation(s) — AGENTS §6 / the doc-3 guard")
        return 1
    print("docguard: clean (AGENTS §6 caps + the doc-3 state-layer shapes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
