"""wb-2's Redot-half claim packet (CONTRACTS §5, TEST_PLAN §9's form).

Claim: the wb-2 application shell (scenes/shell.tscn + the semantic-token
theme themes/workbench_theme.tres + the code-built composition in
scripts/shell.gd) composes under the pinned external Redot 26.2 LTS binary
and captures a screenshot + metadata artifact — reproducibly: two
consecutive runs in the same environment produce byte-identical PNGs (the
CONTRACTS §5 D4 falsifier, extended from the seam to the shell). The
per-surface capture (--surface settings) proves the second placeholder
surface composes with the same artifact honesty.

Lens: determinism + artifact honesty (the shell/theme identities carried).
Prism: the double-run byte-diff over the shell scene (default surface).

Skip law (D6, the duckdb/D-093 pattern): without REDOT_EXE the packet
skips cleanly — CI stays engine-free, the owner/sandbox runs set
REDOT_EXE to the external toolchain binary.
"""

from __future__ import annotations

import json
import os
import struct
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
REDOT = REPO / "workbench" / "presentation" / "redot"

REDOT_EXE = os.environ.get("REDOT_EXE", "").strip()

pytestmark = pytest.mark.skipif(
    not REDOT_EXE,
    reason="REDOT_EXE not set — the Redot 26.2 LTS binary is an external "
    "toolchain (CONTRACTS §5 D1); set REDOT_EXE=<path> to run this packet",
)


def _png_size(path: Path) -> tuple[int, int]:
    """Parse the IHDR (stdlib only — no imaging dependency, D-012)."""
    raw = path.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    assert raw[12:16] == b"IHDR", "first chunk is not IHDR"
    width, height = struct.unpack(">II", raw[16:24])
    return int(width), int(height)


def _run_shell_proof(out_dir: Path, surface: str | None = None) -> dict[str, Path]:
    """One shell-proof run through the operator runner (fresh out dir)."""
    if not REDOT_EXE:
        pytest.skip("REDOT_EXE not set")
    from scripts.visual_proof import main as proof_main

    argv = ["--shell", "--out", str(out_dir)]
    if surface:
        argv += ["--surface", surface]
    assert proof_main(argv) == 0
    name = f"shell_{surface}" if surface and surface != "chat" else "shell"
    meta_name = f"{name}_meta.json" if surface and surface != "chat" else "shell_meta.json"
    return {"png": out_dir / f"{name}.png", "meta": out_dir / meta_name}


@pytest.fixture(scope="module")
def shell_runs(tmp_path_factory: pytest.TempPathFactory) -> list[dict[str, Path]]:
    """Two independent shell-proof runs (default surface)."""
    return [
        _run_shell_proof(tmp_path_factory.mktemp(f"wb_shell_{index}")) for index in range(2)
    ]


@pytest.fixture(scope="module")
def settings_run(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """One per-surface capture (the second placeholder surface)."""
    return _run_shell_proof(tmp_path_factory.mktemp("wb_shell_settings"), surface="settings")


def test_artifacts_exist_and_are_wellformed(shell_runs: list[dict[str, Path]]) -> None:
    first = shell_runs[0]
    for key in ("png", "meta"):
        assert first[key].is_file(), f"artifact {key} missing"

    meta = json.loads(first["meta"].read_text(encoding="utf-8"))
    for key in (
        "engine_version",
        "shell_version",
        "theme_identity",
        "active_surface",
        "surfaces",
        "planned_surfaces",
        "window_size",
    ):
        assert meta.get(key), f"metadata field {key} missing/empty"

    # The pinned engine line (a different binary refuses loudly, never
    # masquerades as the pinned one — the same law as the seam packet).
    assert meta["engine_version"].startswith("26.2"), meta["engine_version"]
    # KI#97 (iter-234): the pin had drifted to canon_shell@0.1 while the
    # packet was REDOT_EXE-gated-silent through wb-8/wb-9 — pins track the
    # LIVE shell, never a remembered one. iter-235: @0.6 (the Observatory).
    assert meta["shell_version"] == "canon_shell@0.6"
    # The theme identity is the committed theme file's sha256 (64 hex).
    theme_sha = meta["theme_identity"]
    assert len(theme_sha) == 64 and all(c in "0123456789abcdef" for c in theme_sha)
    import hashlib

    committed = (REDOT / "themes" / "workbench_theme.tres").read_bytes()
    assert theme_sha == hashlib.sha256(committed).hexdigest(), (
        "theme_identity does not match the committed theme file"
    )

    # The §17 surface inventory (obs-1: the IA gained the Observatory —
    # WORK/RESOURCES/SYSTEM; the planned list re-pointed per LAW §4.1,
    # Runs added, Inference kept, nothing silently dropped).
    assert meta["surfaces"] == ["chat", "observatory", "models", "settings"]
    assert meta["planned_surfaces"] == [
        "Simulation", "Inference", "Prompts", "History", "Runs", "Diagnostics",
    ]
    assert meta["active_surface"] == "chat"
    # ux-1: the base window stays 1440x900 (the min-size/stretch policy rides
    # project.godot — canvas_items/expand; the proof capture is the base run).
    assert meta["window_size"] == [1440, 900]
    assert _png_size(first["png"]) == (1440, 900), "PNG is not the window space"


def test_double_run_is_byte_identical(shell_runs: list[dict[str, Path]]) -> None:
    first, second = shell_runs
    assert first["png"].read_bytes() == second["png"].read_bytes(), (
        "the shell screenshot differs between two runs in the same environment "
        "(the CONTRACTS §5 D4 falsifier, extended to the shell — it fired)"
    )
    meta_a = json.loads(first["meta"].read_text(encoding="utf-8"))
    meta_b = json.loads(second["meta"].read_text(encoding="utf-8"))
    assert meta_a["theme_identity"] == meta_b["theme_identity"]


def test_settings_surface_capture(settings_run: dict[str, Path]) -> None:
    """The second placeholder surface composes with the same honesty."""
    assert settings_run["png"].is_file() and settings_run["meta"].is_file()
    meta = json.loads(settings_run["meta"].read_text(encoding="utf-8"))
    assert meta["active_surface"] == "settings"
    assert meta["surfaces"] == ["chat", "observatory", "models", "settings"]
    assert meta["shell_version"] == "canon_shell@0.6"
    assert _png_size(settings_run["png"]) == (1440, 900)
    # The two surfaces must not render identically (the switch is real).
    default_run_png = None  # resolved lazily: the module fixture order is not ours
    for candidate in settings_run["png"].parent.parent.glob("wb_shell_*/shell.png"):
        default_run_png = candidate
        break
    assert default_run_png is not None, "the default-surface capture not found"
    assert default_run_png.read_bytes() != settings_run["png"].read_bytes(), (
        "the settings capture is byte-identical to the chat capture — "
        "the surface switch did not change the composition"
    )


@pytest.fixture(scope="module")
def observatory_run(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """obs-1: the Observatory slice's deterministic capture."""
    return _run_shell_proof(
        tmp_path_factory.mktemp("wb_shell_observatory"), surface="observatory"
    )


def test_observatory_surface_capture(observatory_run: dict[str, Path]) -> None:
    """obs-1 (FRONTEND_UIUX_LAW §50/§51): the vertical UX slice composes
    under the pinned engine — the workspace grammar's regions rendered
    (breadcrumb, context strip, the World Question contract, the
    primary view's honest NO DATA, the inspector, the evidence ladder),
    deterministically (the surface's own capture, never identical to
    another surface — the regions are the composition)."""
    assert observatory_run["png"].is_file() and observatory_run["meta"].is_file()
    meta = json.loads(observatory_run["meta"].read_text(encoding="utf-8"))
    assert meta["active_surface"] == "observatory"
    assert meta["surfaces"] == ["chat", "observatory", "models", "settings"]
    assert meta["shell_version"] == "canon_shell@0.6"
    assert _png_size(observatory_run["png"]) == (1440, 900)
    # The slice's composition is its own — never a byte-copy of another
    # surface (the grammar changed the canvas, not just the header).
    settings_png = None
    for candidate in observatory_run["png"].parent.parent.glob(
        "wb_shell_settings*/shell_settings.png"
    ):
        settings_png = candidate
        break
    assert settings_png is not None, "the settings capture not found for the diff"
    assert observatory_run["png"].read_bytes() != settings_png.read_bytes(), (
        "the observatory capture is byte-identical to the settings capture — "
        "the slice did not change the composition"
    )
