"""Architecture fitness test (D-031, `docs/blueprint/phase0.md` §1).

The invariants made executable with stdlib `ast` only — zero new dev deps:
(a) import boundary — `core/` imports nothing from `sim/`/`render/`/`cli/`/
    `brief/` (kernel independence);
(b) RNG monopoly — a bare `import random` exists only in `core/rng.py` (L5);
(c) network ban — no `socket`/`urllib`/`http` imports in `core/` + `sim/`
    (INV-4 executable, not just review);
(d) no `print()` outside `cli/` (`MVP_SCOPE.md` §18).

Trivially green on a healthy tree, loud on the first violation.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

PACKAGE_DIRS = ("core", "sim", "render", "brief", "cli")
NETWORK_MODULES = frozenset({"socket", "urllib", "http", "requests"})


def package_files() -> list[Path]:
    files: list[Path] = []
    for name in PACKAGE_DIRS:
        files.extend(sorted((REPO / name).rglob("*.py")))
    return files


def import_roots(tree: ast.Module) -> set[str]:
    """Top-level module names of every import statement in the file."""
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0:
            roots.add(node.module.split(".")[0])
    return roots


def parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_import_boundary_core_is_kernel() -> None:
    for path in sorted((REPO / "core").rglob("*.py")):
        roots = import_roots(parse(path))
        leaks = roots & {"sim", "render", "cli", "brief"}
        assert not leaks, f"{path}: core/ must not import periphery modules {sorted(leaks)}"


def test_rng_monopoly_random_only_in_rng_bank() -> None:
    for path in package_files():
        if path == REPO / "core" / "rng.py":
            continue
        roots = import_roots(parse(path))
        assert "random" not in roots, f"{path}: bare random import outside core/rng.py (L5)"


def test_network_ban_in_core_and_sim() -> None:
    for path in package_files():
        if path.parent != REPO / "core" and "sim" not in path.relative_to(REPO).parts:
            continue
        roots = import_roots(parse(path))
        hits = roots & NETWORK_MODULES
        assert not hits, f"{path}: network import(s) {sorted(hits)} violate INV-4"


def test_no_print_outside_cli() -> None:
    for path in package_files():
        if path.relative_to(REPO).parts[0] == "cli":
            continue
        tree = parse(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id != "print", f"{path}: print() outside cli/ (MVP_SCOPE §18)"
