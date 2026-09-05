"""Architecture fitness test (D-031, `docs/blueprint/phase0.md` §1).

The invariants made executable with stdlib `ast` only — zero new dev deps:
(a) import boundary — `core/` imports nothing from `sim/`/`render/`/`cli/`/
    `brief/` (kernel independence);
(b) RNG monopoly — a bare `import random` exists only in `core/rng.py` (L5);
(c) network ban — no `socket`/`urllib`/`http` imports in ANY track-A
    package dir, `scripts/` included (INV-4 executable; widened iter-6a,
    D-046 — the iter-6 `scripts/` dir had silently escaped this check);
(d) print discipline — `print()` lives only in the operator entry points
    (`cli/` and `scripts/` — CLI-class tools, MVP_SCOPE §18 "CLI excepted",
    D-046); engine code logs instead;
(e) coverage closure — every top-level code dir must be in PACKAGE_DIRS
    (a new dir joins in the same iteration it lands, D-046).

Trivially green on a healthy tree, loud on the first violation.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

PACKAGE_DIRS = ("core", "sim", "render", "brief", "cli", "scripts")
NETWORK_MODULES = frozenset({"socket", "urllib", "http", "requests"})
_OPERATOR_ENTRY_DIRS = frozenset({"cli", "scripts"})


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


def test_network_ban_in_track_a_packages() -> None:
    """INV-4 executable across every track-A package dir (D-046): no
    network module import anywhere in core/sim/render/brief/cli/scripts.
    """
    for path in package_files():
        roots = import_roots(parse(path))
        hits = roots & NETWORK_MODULES
        assert not hits, f"{path}: network import(s) {sorted(hits)} violate INV-4"


def _guarded_probe_imports(tree: ast.Module) -> set[int]:
    """Ids of import nodes inside a Try that catches ImportError — the
    optional-probe law (D-088's sqlite_vec precedent: a third-party root
    is legal in the runtime ONLY as a guarded probe with a fallback)."""
    guarded: set[int] = set()

    def catches_import_error(handler: ast.ExceptHandler) -> bool:
        exc = handler.type
        if exc is None:
            return True
        names = exc.elts if isinstance(exc, ast.Tuple) else [exc]
        return any(
            isinstance(n, ast.Name) and n.id in ("ImportError", "ModuleNotFoundError")
            for n in names
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Try) and any(map(catches_import_error, node.handlers)):
            for inner in ast.walk(node):
                if isinstance(inner, (ast.Import, ast.ImportFrom)):
                    guarded.add(id(inner))
    return guarded


def test_runtime_imports_stdlib_only() -> None:
    """D-012 executable (leg-4, D-093): the runtime import graph
    (core/sim/render/brief/cli — the packages the simulation loads) may
    import ONLY stdlib, local top-level packages, and guarded optional
    probes (try/except ImportError, the sqlite_vec law). A hard
    third-party root — duckdb today, anything else tomorrow — fails
    loudly here. `scripts/` is the offline operator graph (the chronicler
    lives there, never in the runtime) and is exempt by design (D-046)."""
    import sys

    runtime_dirs = ("core", "sim", "render", "brief", "cli")
    local = set(runtime_dirs) | {"scripts", "content"}
    for name in runtime_dirs:
        for path in sorted((REPO / name).rglob("*.py")):
            tree = parse(path)
            guarded = _guarded_probe_imports(tree)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)) and id(node) not in guarded:
                    roots = (
                        {alias.name.split(".")[0] for alias in node.names}
                        if isinstance(node, ast.Import)
                        else (
                            {node.module.split(".")[0]}
                            if node.module and node.level == 0
                            else set()
                        )
                    )
                    foreign = {
                        root
                        for root in roots
                        if root not in sys.stdlib_module_names and root not in local
                    }
                    assert not foreign, (
                        f"{path}: third-party import(s) {sorted(foreign)} in the "
                        f"runtime graph — D-012 (core is stdlib-only; offline "
                        f"deps live in scripts/ and the [chronicler] extra; "
                        f"optional probes must be ImportError-guarded)"
                    )


def test_print_only_in_operator_entry_points() -> None:
    """MVP_SCOPE §18 "CLI excepted" = CLI-class tools: `cli/` and the
    argparse harness in `scripts/` (D-046). Engine code logs instead."""
    for path in package_files():
        if path.relative_to(REPO).parts[0] in _OPERATOR_ENTRY_DIRS:
            continue
        tree = parse(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id != "print", (
                    f"{path}: print() outside the operator entry points "
                    f"(MVP_SCOPE §18)"
                )


def test_package_dirs_cover_every_top_level_code_dir() -> None:
    """Coverage closure (D-046): every top-level directory holding
    committed .py files must appear in PACKAGE_DIRS — a new code dir that
    skips the fitness test silently escapes the executable invariants
    (the iter-6 `scripts/` gap this test closes)."""
    code_dirs = {
        path.parent.name for path in REPO.glob("*/*.py")
    } - {"tests"}
    assert code_dirs == set(PACKAGE_DIRS), (
        f"top-level code dirs {sorted(code_dirs)} != PACKAGE_DIRS "
        f"{sorted(PACKAGE_DIRS)} — add the new dir to the fitness test in "
        f"the same iteration it lands (D-046)"
    )
