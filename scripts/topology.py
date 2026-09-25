"""iter-244 (ssi-3/D-224) — the ownership/topology audit instrument.

The SSI Phase 2 executable (SSI-N018's FULL trajectory audit, the
overlay §2's OPEN row until this landed): derives the machine-readable
map over core/ + workbench/ (owner rows live in
docs/SSI_TOPOLOGY.md — the semantic layer; everything mechanical is
derived HERE, never hand-copied) and the co-change/trajectory evidence
over git history. Two modes:

  --audit [--window N]  derive the live map at HEAD and print it as a
                        JSON document (modules: lines/reads/writes/
                        emits; cochange pairs; watchlist trajectories)
  --check               validate docs/SSI_TOPOLOGY.md against HEAD:
                        the inventory pin (every scope .py has a row,
                        no stale rows), the owner pin (non-empty), and
                        the WATCHLIST topology pin (reads + emits match
                        the derivation exactly — a seam-relevant change
                        without a map update goes RED here)

Laws this rides: N018 (no architecture health from a snapshot — the
recorded figures in the doc are audit-time evidence pinned to
BASE_COMMIT; the live derivation is one command away, never a stale
copy trusted); D-198's admission (the named consumers: ssi-4/ssi-5
split decisions + the owner's go/no-go; the instrument extends the
docguard/test_architecture family — a NEW focused script because the
audit's inputs are code + git history, outside both existing
instruments' charters); INV-2 discipline (sorted iteration everywhere,
stdlib only — no third-party imports, D-012's envelope).

The map's scope: Python modules under core/ and workbench/ (the
strangler targets are all Python; the Redot .gd presentation layer is
out of the map — its law owners are VISUAL_SYSTEM_UI/FRONTEND_UIUX_
LAW, documented in the map's §0). Reads may reference any in-repo
module (sim/, brief/, render/, cli/ included — they carry NAV §1
owners, no map rows of their own).
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
MAP_DOC = REPO / "docs" / "SSI_TOPOLOGY.md"
SCOPE_TOPS = ("core", "workbench")
# The strangler watchlist (the ssi-3 hypotheses + the co-change
# partner) — the ONLY rows whose reads+emits are hard-pinned by
# --check: these files' topology must change DELIBERATELY (a map
# update in the same iteration), never silently.
WATCHLIST = (
    "core/loop.py",
    "core/director.py",
    "core/worldgen.py",
    "core/intent.py",
    "workbench/application/inference.py",
    "core/pack.py",
)
IN_REPO_PREFIXES = ("core", "workbench", "sim", "brief", "render", "cli")
STORE_RE = re.compile(r"^[A-Za-z0-9_./-]+\.(json|jsonl)$")
OP_RE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_.]*$")


def _run_git(args: list[str]) -> str:
    proc = subprocess.run(  # noqa: S603 -- fixed argv, no shell
        ["git", *args], cwd=REPO, capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def base_commit() -> str:
    return _run_git(["rev-parse", "HEAD"]).strip()


def scope_modules() -> list[Path]:
    files: list[Path] = []
    for top in SCOPE_TOPS:
        files.extend(sorted((REPO / top).rglob("*.py")))
    return [f for f in files if "__pycache__" not in f.parts]


def _module_to_paths(module: str) -> list[str]:
    """Map an imported module name to in-repo file path(s)."""
    if module is None:
        return []
    parts = module.split(".")
    if parts[0] not in IN_REPO_PREFIXES:
        return []
    base = "/".join(parts)
    candidates = [f"{base}.py", f"{base}/__init__.py"]
    return [c for c in candidates if (REPO / c).is_file()]


class _Extractor(ast.NodeVisitor):
    """Per-module mechanical facts: imports, draft/push sites, stores, ops."""

    def __init__(self) -> None:
        self.reads: set[str] = set()
        self.drafts: int = 0
        self.pushes: int = 0
        self.stores: set[str] = set()
        self.emit_literals: set[str] = set()
        self.emit_dynamic: bool = False
        self.ops: set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.reads.update(_module_to_paths(alias.name))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level == 0 and node.module:
            self.reads.update(_module_to_paths(node.module))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        name = func.id if isinstance(func, ast.Name) else ""
        attr = func.attr if isinstance(func, ast.Attribute) else ""
        if name == "EventDraft" or attr == "EventDraft":
            self.drafts += 1
            self._take_emit_kw(node, "type")
        elif attr == "push":
            self.pushes += 1
            self._take_emit_kw(node, "kind")
        for kw in node.keywords:
            if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                value = kw.value.value
                if isinstance(value, str) and OP_RE.match(value):
                    self.ops.add(value)
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if OP_RE.match(arg.value) and attr in ("op", "register"):
                    self.ops.add(arg.value)
        self.generic_visit(node)

    def _take_emit_kw(self, node: ast.Call, kwname: str) -> None:
        for kw in node.keywords:
            if kw.arg == kwname:
                if isinstance(kw.value, ast.Constant) and isinstance(
                    kw.value.value, str
                ):
                    self.emit_literals.add(kw.value.value)
                else:
                    self.emit_dynamic = True

    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, str) and STORE_RE.match(node.value):
            self.stores.add(node.value)
        self.generic_visit(node)


def derive_module(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    ex = _Extractor()
    ex.visit(tree)
    rel = path.relative_to(REPO).as_posix()
    return {
        "module": rel,
        "lines": source.count("\n"),
        "reads": sorted(ex.reads),
        "writes": {
            "drafts": ex.drafts,
            "pushes": ex.pushes,
            "stores": sorted(ex.stores),
        },
        "emits": {
            "literals": sorted(ex.emit_literals),
            "dynamic": ex.emit_dynamic,
            "ops": sorted(ex.ops),
        },
    }


def cochange(window: int) -> dict[str, Any]:
    """Pairwise co-change over the last N commits (all repo files)."""
    raw = _run_git(
        ["log", f"-{window}", "--name-only", "--pretty=format:%x00"]
    )
    commits: list[frozenset[str]] = []
    current: list[str] = []
    for line in raw.splitlines():
        if line.startswith("\x00"):
            if current:
                commits.append(frozenset(current))
            current = []
        elif line.strip():
            current.append(line.strip())
    if current:
        commits.append(frozenset(current))
    n = len(commits)
    touches: Counter[str] = Counter()
    pairs: Counter[tuple[str, str]] = Counter()
    for files in commits:
        for f in files:
            touches[f] += 1
        ordered = sorted(files)
        for i, a in enumerate(ordered):
            for b in ordered[i + 1 :]:
                pairs[(a, b)] += 1
    pair_stats = []
    for (a, b), nab in sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0])):
        if nab < 5:
            continue
        na, nb = touches[a], touches[b]
        lift = (n * nab / (na * nb)) if na and nb else 0.0
        jaccard = nab / (na + nb - nab)
        pair_stats.append(
            {
                "pair": [a, b],
                "co": nab,
                "a": na,
                "b": nb,
                "lift": round(lift, 3),
                "jaccard": round(jaccard, 3),
            }
        )
    code_pairs = [
        p
        for p in pair_stats
        if p["pair"][0].endswith(".py") and p["pair"][1].endswith(".py")
    ]
    return {
        "window": window,
        "commits_in_window": n,
        "total_commits": int(_run_git(["rev-list", "--count", "HEAD"]).strip()),
        "top_pairs": pair_stats[:40],
        "top_code_pairs": code_pairs[:25],
        "code_pair_count": len(code_pairs),
        "touches": {f: c for f, c in sorted(touches.items()) if c >= 10},
    }


def trajectory(path: str, window: int) -> dict[str, Any]:
    """Size trajectory for one file over the repo's last N commits:
    HEAD size, window-start size, introduction size, touch counts.

    NOTE: `git log -N -- <path>` limits the OUTPUT list (commits that
    touch the path), NOT the window — the boundary commit must be
    resolved first (`rev-list --max-count=N HEAD`), else the "window"
    silently becomes "the file's own last N touches"."""
    boundary = _run_git(
        ["rev-list", f"--max-count={window}", "HEAD"]
    ).strip().splitlines()[-1]
    head_lines = (REPO / path).read_text(encoding="utf-8").count("\n")
    raw = _run_git(
        ["log", f"{boundary}..HEAD", "--numstat", "--pretty=format:%x00", "--", path]
    )
    added = deleted = 0
    window_touches = 0
    for line in raw.splitlines():
        if line.startswith("\x00"):
            continue
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
            window_touches += 1
            added += int(parts[0])
            deleted += int(parts[1])
    full_raw = _run_git(
        ["log", "--numstat", "--pretty=format:%x00", "--follow", "--", path]
    )
    full_added = full_deleted = 0
    full_touches = 0
    for line in full_raw.splitlines():
        if line.startswith("\x00"):
            continue
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
            full_touches += 1
            full_added += int(parts[0])
            full_deleted += int(parts[1])
    return {
        "file": path,
        "lines_head": head_lines,
        "lines_window_start": head_lines - added + deleted,
        "net_window_growth": added - deleted,
        "lines_introduced": full_added - full_deleted,
        "window_touches": window_touches,
        "full_touches": full_touches,
    }


def run_audit(window: int) -> dict[str, Any]:
    modules = [derive_module(p) for p in scope_modules()]
    return {
        "base_commit": base_commit(),
        "scope": [f"{t}/ (*.py)" for t in SCOPE_TOPS],
        "modules": modules,
        "cochange": cochange(window),
        "trajectories": [trajectory(f, window) for f in WATCHLIST],
    }


# ------------------------------------------------------------ --check


MAP_HEADER = "| module | owner | lines | reads | writes | emits |"


def _parse_map_doc() -> tuple[list[dict[str, str]], list[str]]:
    """Parse the map table rows + the declared watchlist from the doc.

    Only the table whose header is EXACTLY the map header is parsed —
    the doc's other tables (co-change, verdicts) never match, so they
    cannot leak rows into the pin."""
    try:
        text = MAP_DOC.read_text(encoding="utf-8")
    except OSError:
        return [], []
    watchlist: list[str] = []
    rows: list[dict[str, str]] = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("watchlist:"):
            watchlist = [
                w.strip() for w in stripped[len("watchlist:") :].split(",") if w.strip()
            ]
        if stripped == MAP_HEADER:
            in_table = True
            continue
        if in_table and (stripped.startswith("|---") or stripped.startswith("|:--")):
            continue
        if in_table and stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= 6:
                rows.append(
                    {
                        "module": cells[0],
                        "owner": cells[1],
                        "lines": cells[2],
                        "reads": cells[3],
                        "writes": cells[4],
                        "emits": cells[5],
                    }
                )
            else:
                in_table = False
        elif in_table and stripped and not stripped.startswith("|"):
            in_table = False
    return rows, watchlist


def _split_cell(cell: str) -> list[str]:
    if cell in ("—", "-", ""):
        return []
    return [item.strip() for item in cell.split(",") if item.strip()]


def run_check() -> list[str]:
    violations: list[str] = []
    rows, declared_watchlist = _parse_map_doc()
    if not rows:
        return ["map table missing or unparsable in docs/SSI_TOPOLOGY.md"]
    derived = {m["module"]: m for m in (derive_module(p) for p in scope_modules())}
    doc_modules = {r["module"] for r in rows}
    for missing in sorted(derived.keys() - doc_modules):
        violations.append(f"inventory: {missing} on disk, no map row")
    for stale in sorted(doc_modules - derived.keys()):
        violations.append(f"inventory: {stale} in map, not on disk")
    for r in rows:
        if not r["owner"] or r["owner"] in ("—", "TBD", "?"):
            violations.append(f"owner: {r['module']} has no owner")
    watchlist = declared_watchlist or list(WATCHLIST)
    for w in watchlist:
        row = next((r for r in rows if r["module"] == w), None)
        mod = derived.get(w)
        if row is None:
            violations.append(f"watchlist: {w} has no map row")
            continue
        if mod is None:
            violations.append(f"watchlist: {w} not derivable (missing on disk?)")
            continue
        doc_reads = _split_cell(row["reads"])
        if sorted(doc_reads) != mod["reads"]:
            violations.append(
                f"watchlist reads drift: {w} doc={doc_reads} live={mod['reads']}"
            )
        live_literals = set(mod["emits"]["literals"])
        if mod["emits"]["dynamic"]:
            live_literals.add("dyn")
        live_literals.update(mod["emits"]["ops"])
        doc_emits = set(_split_cell(row["emits"]))
        if doc_emits != live_literals:
            violations.append(
                f"watchlist emits drift: {w} doc={sorted(doc_emits)} "
                f"live={sorted(live_literals)}"
            )
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--audit", action="store_true", help="derive + print the live map")
    mode.add_argument(
        "--check", action="store_true", help="validate docs/SSI_TOPOLOGY.md at HEAD"
    )
    parser.add_argument("--window", type=int, default=150, help="co-change window")
    args = parser.parse_args(argv)
    if args.audit:
        json.dump(run_audit(args.window), sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    violations = run_check()
    if violations:
        for v in violations:
            print(f"topology: {v}")
        print(f"topology: {len(violations)} violation(s) — docs/SSI_TOPOLOGY.md "
              "is stale; refresh the rows via `python scripts/topology.py --audit`")
        return 1
    print("topology: clean (inventory + owners + watchlist pins held)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
