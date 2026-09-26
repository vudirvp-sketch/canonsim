"""Architecture fitness test (D-031, `docs/blueprint/phase0.md` §1).

The invariants made executable with stdlib `ast` only — zero new dev deps:
(a) import boundary — `core/` imports nothing from `sim/`/`render/`/`cli/`/
    `brief/` (kernel independence);
(b) RNG monopoly — a bare `import random` exists only in `core/rng.py` (L5);
(c) network ban — no `socket`/`urllib`/`http`/`requests` imports in ANY
    track-A package dir outside the THREE sanctioned modules — the
    OUTBOUND engine adapter `cli/engine.py` (INV-4's form since
    engine-1's landing, iter-177/D-193), the INBOUND Workbench
    gateway binding `workbench/api/transport.py` (wb-4's owner-gated
    exception, iter-219/D-201: one module per direction, the app
    spec §4.1), and the OUTBOUND model-assets fetch
    `workbench/platform/model_fetch.py` (wb-9's owner-gated
    exception, iter-226/D-208: HTTP GET downloads ONLY — the
    owner's «подтянуть модель откуда угодно» call; before the
    landings the ban covered every dir — iter-6a's D-046 widening);
(d) print discipline — `print()` lives only in the operator entry points
    (`cli/` and `scripts/` — CLI-class tools, MVP_SCOPE §18 "CLI excepted",
    D-046); engine code logs instead;
(e) coverage closure — every top-level code dir must be in PACKAGE_DIRS
    (a new dir joins in the same iteration it lands, D-046);
(f) no hidden effect (SSI-N001, ssi-3/D-223) — the wall-clock and
    entropy import roots (`time`, `datetime`, `secrets`, `uuid`) are
    banned across the canonical kernel (core/sim/render/brief/cli):
    the effect families a local-looking module must never hide;
    INV-2's static surface widened from the bare `random` monopoly
    (L5) to the full hidden-effect set — the entropy authority stays
    `core/rng.py`, the app layer (workbench/) sits outside the
    determinism envelope (TEST_PLAN §8.4);
(g) admission closure (SSI-N002, ssi-3/D-223) — every top-level code
    dir in PACKAGE_DIRS carries its owner row in
    `docs/AGENT_NAVIGATION.md` §1: a new mechanism landing without
    its documented owner/purpose is an unadmitted primitive (AGENTS
    §2.8: named consumer, owner, minimal intervention, verification
    — the coverage-closure law's own sibling at the documentation
    edge);
(h) the canonical read seam (Phase 5/ssi-6, D-228) — `workbench/`
    imports core/ EXACTLY THROUGH `workbench/canonical_read.py`, the
    narrow read API (INV-4's sanctioned-module pattern applied to the
    core-read boundary: the ONE module whose reads the topology map
    hard-pins); a core import anywhere else in the workbench app
    layer — a second edge, a write arm, a fresh deep dependency —
    goes RED here.

Trivially green on a healthy tree, loud on the first violation.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

PACKAGE_DIRS = ("core", "sim", "render", "brief", "cli", "scripts", "workbench")
NETWORK_MODULES = frozenset({"socket", "urllib", "http", "requests"})
#: SSI-N001's hidden-effect roots (ssi-3/D-223): wall-clock (time,
#: datetime) and entropy (secrets, uuid) — the families the canonical
#: kernel admits ZERO members of (INV-2's "no wall-clock anywhere
#: (including the log header)"; `random` stays L5's own monopoly
#: below). Any use requires an import; the root-level ban is the
#: complete static surface.
HIDDEN_EFFECT_ROOTS = frozenset({"time", "datetime", "secrets", "uuid"})
#: The canonical determinism envelope's dirs (SSI-N001's scope — the
#: kernel graph; workbench/ is the app layer, outside the envelope
#: per TEST_PLAN §8.4, and scripts/ is the offline operator graph).
CANONICAL_KERNEL_DIRS = ("core", "sim", "render", "brief", "cli")
#: INV-4's sanctioned network surface: exactly three modules, one
#: per direction-and-asset (the app spec §4.1 + D-208) — the OUTBOUND
#: engine adapter (D-192/D-193), the INBOUND gateway binding (D-201,
#: wb-4's owner-gated exception — loopback-only), and the OUTBOUND
#: model-assets fetch (D-208, wb-9's owner-gated exception — HTTP GET
#: downloads only, the owner's «подтянуть модель откуда угодно»
#: call). A network import anywhere else — a second engine file, an
#: engine client in core/brief, a stray probe in scripts, a socket in
#: the gateway's semantic core — fails the ban below.
NETWORK_EXCEPTIONS = frozenset(
    {
        REPO / "cli" / "engine.py",
        REPO / "workbench" / "api" / "transport.py",
        REPO / "workbench" / "platform" / "model_fetch.py",
    }
)
#: The canonical read seam (Phase 5/ssi-6, D-228): the ONE workbench
#: module that may import core/ — the narrow read API every other
#: workbench module reaches CanonSim's read products through (the
#: pure re-export shell over read_log/validate_header/EventRecord/
#: LogError/fold/initial_projection/present_in_order/load_pack/
#: PackError/stable_hash; its reads ride the topology map's watchlist
#: — the surface grows deliberately, never silently). The periphery
#: (scripts/ — the offline operator graph, render/ — the chronicle
#: read-side) keeps its direct core imports by design (D-046, the
#: map's §0 scope law); this pin bounds the WORKBENCH app layer only.
CORE_READ_SEAM = REPO / "workbench" / "canonical_read.py"
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


def test_network_ban_outside_the_sanctioned_modules() -> None:
    """INV-4 executable across every track-A package dir (D-046,
    engine-1's lift D-193, wb-4's gateway exception D-201, wb-9's
    model-fetch exception D-208): the network surface is EXACTLY
    THREE modules, one per direction-and-asset (the app spec §4.1
    + D-208) — the explicit adapter `cli/engine.py` (outbound engine
    wire), the loopback gateway binding
    `workbench/api/transport.py` (inbound), and the model-assets
    fetch `workbench/platform/model_fetch.py` (outbound downloads,
    the owner's «подтянуть модель откуда угодно» call). No network
    import anywhere else in core/sim/render/brief/cli/scripts/
    workbench.
    """
    for path in package_files():
        if path in NETWORK_EXCEPTIONS:
            continue
        roots = import_roots(parse(path))
        hits = roots & NETWORK_MODULES
        assert not hits, (
            f"{path}: network import(s) {sorted(hits)} outside the three "
            f"sanctioned modules (INV-4 — the surface is cli/engine.py "
            f"+ workbench/api/transport.py + workbench/platform/"
            f"model_fetch.py, one per direction-and-asset)"
        )


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
    (the iter-6 `scripts/` gap this test closes). KI#102 (iter-259): the
    glob walks the FILESYSTEM while the law names COMMITTED files — a
    session's gitignored `scratch/` interventions (D-197) turned the test
    red in any sandbox that used them (green in CI, red at the desk —
    KI#93's inverse). The exclusion set now names the ignored dir family
    explicitly, keeping the closure law environment-independent."""
    code_dirs = {
        path.parent.name for path in REPO.glob("*/*.py")
    } - {"tests", "scratch"}  # never-committed dirs: the intervention root
    assert code_dirs == set(PACKAGE_DIRS), (
        f"top-level code dirs {sorted(code_dirs)} != PACKAGE_DIRS "
        f"{sorted(PACKAGE_DIRS)} — add the new dir to the fitness test in "
        f"the same iteration it lands (D-046)"
    )


def test_no_hidden_effect_wall_clock_or_entropy_in_the_kernel() -> None:
    """SSI-N001 executable (ssi-3/D-223): the wall-clock and entropy
    import roots — time, datetime, secrets, uuid — never appear in the
    canonical kernel (core/sim/render/brief/cli). INV-2's static
    surface was the bare `random` monopoly (L5, the test above); the
    SSI admission widens it to the full hidden-effect set: a module
    that looks local must not hide a timing or entropy effect behind
    an import. The entropy authority stays `core/rng.py` (the RngBank,
    D-028); file IO stays INV-1's privilege separation (core/log.py
    the one canon-write path — a JOB, never a hidden effect); the app
    layer (workbench/) legitimately holds deadlines and process
    timing OUTSIDE the determinism envelope (TEST_PLAN §8.4)."""
    for name in CANONICAL_KERNEL_DIRS:
        for path in sorted((REPO / name).rglob("*.py")):
            roots = import_roots(parse(path))
            hits = roots & HIDDEN_EFFECT_ROOTS
            assert not hits, (
                f"{path}: hidden-effect import(s) {sorted(hits)} in the "
                f"canonical kernel — wall-clock/entropy effects a "
                f"local-looking module must never hide (SSI-N001, INV-2; "
                f"the entropy authority is core/rng.py's RngBank)"
            )


def test_admission_closure_every_package_dir_is_documented_in_nav() -> None:
    """SSI-N002 executable (ssi-3/D-223): every top-level code dir
    (PACKAGE_DIRS — the coverage-closure set) carries its row in
    docs/AGENT_NAVIGATION.md §1, the documented owner map. A new
    mechanism (dir) landing without its owner/purpose row is an
    unadmitted primitive — AGENTS §2.8's admission law (a named
    consumer, a demonstrated problem, an owner, a minimal
    intervention, a verification) leaves a paper trail, and NAV §1 is
    where it lands. The sibling of the coverage-closure test above at
    the documentation edge: the tree knows the dir, the map must know
    it too. (The sim/ row landed with this test — the admission-
    completion fix, not a waiver.)"""
    nav = (REPO / "docs" / "AGENT_NAVIGATION.md").read_text(encoding="utf-8")
    for name in PACKAGE_DIRS:
        assert f"| `{name}/`" in nav, (
            f"docs/AGENT_NAVIGATION.md §1: no owner row for `{name}/` — a "
            f"top-level code dir without its documented owner/purpose is "
            f"an unadmitted primitive (SSI-N002, AGENTS §2.8; the row "
            f"joins in the same iteration the dir lands)"
        )


def test_core_reads_only_through_the_canonical_seam() -> None:
    """The canonical read seam executable (Phase 5/ssi-6, D-228):
    `workbench/` imports core/ EXACTLY THROUGH
    `workbench/canonical_read.py` — INV-4's sanctioned-module pattern
    («exactly N modules», one per boundary) applied to the core-read
    boundary. The three read-side consumers the map names
    (scene_build.py, observatory_read.py, scene_ir.py) and every
    future workbench module reach the canonical read products
    (read_log, the fold, the pack load, stable_hash) through the seam
    — a direct core import anywhere else in the workbench app layer
    fails here: a second edge is an unaudited dependency on the
    engine's internals, exactly what the phase exists to close. The
    seam's OWN surface is drift-pinned by scripts/topology.py
    --check (it rides the map's watchlist); this test bounds the
    consumers, that pin bounds the seam."""
    seam_on_disk = CORE_READ_SEAM.is_file()
    for path in sorted((REPO / "workbench").rglob("*.py")):
        if path == CORE_READ_SEAM:
            continue
        roots = import_roots(parse(path))
        assert "core" not in roots, (
            f"{path}: core import(s) outside the canonical read seam — "
            f"workbench/ reaches core/ EXACTLY THROUGH "
            f"workbench/canonical_read.py (Phase 5/ssi-6, D-228; INV-4's "
            f"sanctioned-module pattern at the core-read boundary; a new "
            f"read need joins the seam's surface, never a second edge)"
        )
    assert seam_on_disk, (
        f"{CORE_READ_SEAM}: the canonical read seam itself is missing — "
        "the one sanctioned core-import module (Phase 5/ssi-6, D-228) "
        "must exist for the pin above to bound anything"
    )
