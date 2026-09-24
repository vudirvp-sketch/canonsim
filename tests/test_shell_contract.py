"""wb-2's committed-file contract (non-gated — no engine needed).

The shell's gated proof packet (test_shell_proof.py) needs REDOT_EXE;
this module pins the COMMITTED contract the proof depends on, so a
regression in the project files fails the suite everywhere, not only
where the engine binary is present:

- the app-entry law: the Redot project's main scene IS the shell (the
  wb-1 seam-proof scene is a verification harness, run explicitly by
  scripts/visual_proof.py — never the app's launch form);
- the theme's token namespaces exist in the committed theme file (the
  §10 single-source law: the shell code reads colours/sizes/styleboxes
  by name from `Workbench/*`, so a renamed token is a runtime break the
  suite must catch textually);
- the proof-mode arg contract: the shell script handles --png/--meta
  (the runner's coupling) and the theme path it hashes for identity.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REDOT = REPO / "workbench" / "presentation" / "redot"
PROJECT = REDOT / "project.godot"
THEME = REDOT / "themes" / "workbench_theme.tres"
SHELL_SCRIPT = REDOT / "scripts" / "shell.gd"
SHELL_SCENE = REDOT / "scenes" / "shell.tscn"


def test_main_scene_is_the_shell() -> None:
    text = PROJECT.read_text(encoding="utf-8")
    assert 'run/main_scene="res://scenes/shell.tscn"' in text, (
        "the project's main scene must be the application shell (wb-2's "
        "app-entry law); the seam-proof scene runs explicitly via "
        "scripts/visual_proof.py"
    )
    assert 'renderer/rendering_method="gl_compatibility"' in text


def test_theme_file_carries_the_token_namespaces() -> None:
    text = THEME.read_text(encoding="utf-8")
    # The semantic token namespaces the shell code reads by name.
    for marker in (
        "Workbench/colors/background_base",
        "Workbench/colors/surface_l1",
        "Workbench/colors/surface_l2",
        "Workbench/colors/surface_selected",
        "Workbench/colors/text_primary",
        "Workbench/colors/text_secondary",
        "Workbench/colors/text_muted",
        "Workbench/colors/accent",
        "Workbench/colors/status_success",
        "Workbench/colors/status_warning",
        "Workbench/colors/authority_canonical",
        "Workbench/constants/font_size_page_title",
        "Workbench/constants/font_size_section_title",
        "Workbench/constants/font_size_body",
        "Workbench/constants/font_size_secondary",
        "Workbench/constants/font_size_caption",
        "Workbench/constants/rail_width",
        "Workbench/styles/surface",
        "Workbench/styles/bar",
    ):
        assert marker in text, f"theme token missing: {marker}"
    # The component-state law (§10): the styled types carry their state sets.
    for marker in (
        "Button/styles/normal",
        "Button/styles/hover",
        "Button/styles/pressed",
        "Button/styles/disabled",
        "Button/styles/focus",
        "LineEdit/styles/normal",
        "LineEdit/styles/focus",
        "LineEdit/styles/readonly",
        "PanelContainer/styles/panel",
    ):
        assert marker in text, f"component style missing: {marker}"
    # Every color token is a 4-float Color (the .tres serialisation law).
    assert re.search(r"Workbench/colors/\w+ = Color\(", text)


def test_shell_script_proof_contract() -> None:
    text = SHELL_SCRIPT.read_text(encoding="utf-8")
    assert 'THEME_PATH := "res://themes/workbench_theme.tres"' in text
    assert '"--png":' in text and '"--meta":' in text, (
        "the shell must handle the proof-mode user args (the runner coupling)"
    )
    assert "SHELL_PROOF_OK" in text
    assert "get_sha256" in text, "the theme identity must ride the metadata"
    scene = SHELL_SCENE.read_text(encoding="utf-8")
    assert 'path="res://themes/workbench_theme.tres"' in scene
    assert 'path="res://scripts/shell.gd"' in scene
    assert "anchor_right = 1.0" in scene and "anchor_bottom = 1.0" in scene, (
        "the shell root must be full-rect in the scene file (the app fills "
        "the window — the wb-2 layout lesson)"
    )


# ------------------------------------------- wb-7: the live chat circuit


def test_gateway_client_is_committed_and_contracted() -> None:
    """wb-7's frontend half: the typed POST /op client is a committed
    project file whose contract the shell depends on — the single
    dispatch route, the loopback-only posture (no llama.cpp URL can
    appear in the frontend: frontend §47 G8), and the two signals the
    shell wires."""
    client = REDOT / "scripts" / "gateway_client.gd"
    text = client.read_text(encoding="utf-8")
    assert '"/op"' in text, "the single dispatch route (wb-4's §8 law)"
    assert "signal operation_answered" in text
    assert "signal transport_failed" in text
    assert "JSON.stringify" in text and "JSON.parse_string" in text
    # G8's executable half: the client holds NO endpoint of its own —
    # no absolute URL, no llama.cpp API path, no backend port literal.
    # (The docstring may NAME llama.cpp as the thing never dialled.)
    import re

    assert not re.search(r"https?://", text), (
        "the client must not hardcode an endpoint — the URL is configured"
    )
    assert "8080" not in text, "no backend port literal in the frontend"
    assert "/v1/chat" not in text and "/completions" not in text, (
        "the frontend dials the GATEWAY only, never the llama.cpp API "
        "(frontend §47 G8)"
    )


def test_shell_live_circuit_contract() -> None:
    """wb-7's shell wiring: the live-circuit entry points exist by name
    (the URL resolution order, the session/chat/poll surface, the
    honest NOT CONNECTED default) and the proof mode stays the static
    deterministic form (no live circuit when --png rides)."""
    text = SHELL_SCRIPT.read_text(encoding="utf-8")
    # The URL resolution order (user arg > env > project setting).
    assert '"--gateway-url"' in text
    assert "CANONSIM_GATEWAY_URL" in text
    assert 'canonism_workbench/gateway/url' in text
    # The circuit's operation surface (the gateway's own names).
    for op in ('"app.status"', '"session.create"', '"chat.send"',
               '"run.get"', '"run.cancel"'):
        assert op in text, f"the live circuit must call {op}"
    # The client + the honest default badge.
    assert "gateway_client.gd" in text
    assert "CANONSIM · NOT CONNECTED" in text
    # The deterministic proof mode: the live circuit starts ONLY on
    # the interactive path (paths.is_empty() branch).
    assert "_start_live_circuit" in text
    assert "if paths.is_empty():" in text


def test_project_carries_the_gateway_url_setting() -> None:
    """The committed default the live shell falls back to — the same
    loopback URL scripts/workbench_app.py serves on (the launcher's
    DEFAULT_HOST/DEFAULT_PORT)."""
    text = PROJECT.read_text(encoding="utf-8")
    assert "[canonism_workbench]" in text
    assert 'gateway/url="http://127.0.0.1:8765"' in text
