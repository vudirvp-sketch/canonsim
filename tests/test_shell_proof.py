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


def _run_shell_proof(
    out_dir: Path,
    surface: str | None = None,
    obs_document: Path | None = None,
    inference_document: Path | None = None,
) -> dict[str, Path]:
    """One shell-proof run through the operator runner (fresh out dir)."""
    if not REDOT_EXE:
        pytest.skip("REDOT_EXE not set")
    from scripts.visual_proof import main as proof_main

    argv = ["--shell", "--out", str(out_dir)]
    if surface:
        argv += ["--surface", surface]
    if obs_document is not None:
        argv += ["--obs-document", str(obs_document)]
    if inference_document is not None:
        argv += ["--inference-document", str(inference_document)]
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
    assert meta["shell_version"] == "canon_shell@0.8"
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
    # Runs added; inf-1: Inference went REAL — the planned set keeps
    # the honest remainder).
    assert meta["surfaces"] == [
        "chat", "observatory", "inference", "models", "settings"
    ]
    assert meta["planned_surfaces"] == [
        "Simulation", "Prompts", "History", "Runs", "Diagnostics",
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
    assert meta["surfaces"] == [
        "chat", "observatory", "inference", "models", "settings"
    ]
    assert meta["shell_version"] == "canon_shell@0.8"
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
    assert meta["surfaces"] == [
        "chat", "observatory", "inference", "models", "settings"
    ]
    assert meta["shell_version"] == "canon_shell@0.8"
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


def _obs_read_document(tmp: Path) -> Path:
    """obs-2's proof injection source: the REAL observatory.read result
    over the plumbing fixture (the actual gateway + op — the capture
    renders a genuine op document, never a hand-crafted near-miss)."""
    import shutil

    from workbench.api.contract import RequestEnvelope
    from workbench.api.gateway import Gateway
    from workbench.application.clock import AppClock
    from workbench.application.operations.composition import (
        compose_workbench_operations,
    )

    runs_root = tmp / "logs"
    runs_root.mkdir(parents=True, exist_ok=True)
    shutil.copy(
        REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl",
        runs_root / "run_42_0.jsonl",
    )
    schema = json.loads(
        (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
    )
    gateway = Gateway()
    compose_workbench_operations(
        gateway,
        tmp / "models-absent",
        AppClock(),
        observatory_runs_root=runs_root,
        observatory_schema=schema,
    )
    response = gateway.dispatch(
        RequestEnvelope(
            operation="observatory.read", arguments={"run": "run_42_0"}
        )
    )
    assert response.status == "OK", response.to_mapping()
    document = tmp / "obs_read_document.json"
    document.write_text(
        json.dumps(response.result, indent=2, sort_keys=True), encoding="utf-8"
    )
    return document


@pytest.fixture(scope="module")
def observatory_loaded_runs(
    tmp_path_factory: pytest.TempPathFactory,
) -> list[dict[str, Path]]:
    """obs-2: two independent LOADED captures (the real read document
    injected through the proof harness — LAW §43's runtime form)."""
    document = _obs_read_document(tmp_path_factory.mktemp("wb_obs_doc"))
    return [
        _run_shell_proof(
            tmp_path_factory.mktemp(f"wb_shell_obs_loaded_{index}"),
            surface="observatory",
            obs_document=document,
        )
        for index in range(2)
    ]


def test_observatory_loaded_capture(
    observatory_loaded_runs, observatory_run: dict[str, Path]
) -> None:
    """obs-2 (FRONTEND_UIUX_LAW §25's P1 continuation): the LOADED
    Observatory renders over a real op document — the context strip
    carries the run's identity, the event table holds rows, the
    selection's inspector + the scoped evidence ladder compose —
    deterministically (the double-run byte-diff) and distinctly from
    the empty slice (the feed changed the canvas)."""
    first, second = observatory_loaded_runs
    for run in (first, second):
        assert run["png"].is_file() and run["meta"].is_file()
    meta = json.loads(first["meta"].read_text(encoding="utf-8"))
    assert meta["active_surface"] == "observatory"
    assert meta["observatory_run"] == "run_42_0", (
        "the meta must carry the injected run's stem (the capture's own "
        "honesty — a loaded capture never masquerades as an empty one)"
    )
    assert _png_size(first["png"]) == (1440, 900)
    # The D4 falsifier, loaded form: the same document renders
    # byte-identically across runs.
    assert first["png"].read_bytes() == second["png"].read_bytes(), (
        "the LOADED observatory capture differs between two runs — the "
        "document rendering is not deterministic"
    )
    # The loaded capture is NOT the empty slice (the feed is visible).
    assert first["png"].read_bytes() != observatory_run["png"].read_bytes(), (
        "the LOADED capture is byte-identical to the EMPTY slice — the "
        "feed did not change the composition"
    )


def _inference_read_document(tmp: Path) -> Path:
    """inf-1's proof injection source: the REAL inference.read result
    over the actual gateway + the resolver (the capture renders a
    genuine op document, never a hand-crafted near-miss — the obs-2
    pattern). The document carries the RESOLVED states: the seed's
    AUTO, an ineffective sampler (top_k disabled — the value stays
    configured), the reordered chain, and the compiled preview."""
    from workbench.api.contract import RequestEnvelope
    from workbench.api.gateway import Gateway
    from workbench.application.clock import AppClock
    from workbench.application.inference import InferenceStore
    from workbench.application.operations.composition import (
        compose_workbench_operations,
    )

    inference = InferenceStore(tmp / "inference.json")
    inference.update(
        {
            "name": "Long-form draft",
            "temperature": 0.7,
            "gpu_layers": "auto",
            "cache_type_k": "q8_0",
            "sampler_chain": [
                {"id": "penalties", "enabled": True},
                {"id": "top_p", "enabled": True},
                {"id": "min_p", "enabled": True},
                {"id": "top_k", "enabled": False},
                {"id": "temperature", "enabled": True},
                {"id": "dry", "enabled": True},
                {"id": "top_n_sigma", "enabled": True},
                {"id": "typ_p", "enabled": True},
                {"id": "xtc", "enabled": True},
            ],
        }
    )
    gateway = Gateway()
    compose_workbench_operations(
        gateway,
        tmp / "models-absent",
        AppClock(),
        backend=_NoopPort(),
        inference_store=inference,
    )
    response = gateway.dispatch(
        RequestEnvelope(operation="inference.read", arguments={})
    )
    assert response.status == "OK", response.to_mapping()
    document = tmp / "inference_read_document.json"
    document.write_text(
        json.dumps(response.result, indent=2, sort_keys=True), encoding="utf-8"
    )
    return document


class _NoopPort:
    """The proof document's port stand-in (the read needs a registered
    backend family; the read itself never touches the port)."""

    def props(self) -> dict:
        return {}

    def chat(self, messages, *, grammar=None, temperature=0.8, max_tokens=512):
        return ("", "stop")

    def load_model(self, model_path, alias=None):
        return {}

    def unload_model(self, model_ref):
        return {}


@pytest.fixture(scope="module")
def inference_loaded_runs(
    tmp_path_factory: pytest.TempPathFactory,
) -> list[dict[str, Path]]:
    """Two independent loaded Inference captures (the D4 falsifier)."""
    document = _inference_read_document(
        tmp_path_factory.mktemp("inf_doc")
    )
    return [
        _run_shell_proof(
            tmp_path_factory.mktemp(f"wb_inference_{index}"),
            surface="inference",
            inference_document=document,
        )
        for index in range(2)
    ]


def test_inference_surface_capture(inference_loaded_runs) -> None:
    """inf-1's runtime proof (LLAMA_CPP_INFERENCE_CONTROL_LAW §21): the
    Inference surface renders over a REAL inference.read document —
    the control groups, the state badges (the seed's AUTO, the
    disabled top_k's INEFFECTIVE), the reordered chain, and the
    compiled preview compose deterministically (the double-run
    byte-diff)."""
    first, second = inference_loaded_runs
    for run in (first, second):
        assert run["png"].is_file() and run["meta"].is_file()
    meta = json.loads(first["meta"].read_text(encoding="utf-8"))
    assert meta["active_surface"] == "inference"
    assert "inference" in meta["surfaces"], "the axis is REAL, not planned"
    assert _png_size(first["png"]) == (1440, 900)
    # the D4 falsifier: the same document renders byte-identically
    assert first["png"].read_bytes() == second["png"].read_bytes(), (
        "the LOADED inference capture differs between two runs — the "
        "document rendering is not deterministic"
    )
