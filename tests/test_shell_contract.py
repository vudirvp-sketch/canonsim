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


# ------------------------------------------- wb-8: the Models surface


def test_the_models_surface_contract() -> None:
    """wb-8's frontend half: the Models surface is LIVE in the shell
    (the §17 axis moved off the planned list), drives the gateway's
    own operation names, and carries the honest per-call timeout for
    the managed load (minutes-class — §11.1's STARTING→PROBING→READY
    walk) plus the truthful UNKNOWN/refusal notes."""
    text = SHELL_SCRIPT.read_text(encoding="utf-8")
    # The axis went live: models sits in SURFACES, not PLANNED.
    assert 'const SURFACES := ["chat", "models", "settings"]' in text
    planned_line = text.split("PLANNED_SURFACES := ")[1].split("\n")[0]
    assert '"Inference"' in planned_line and '"Simulation"' in planned_line
    assert '"Models"' not in planned_line
    # The circuit's operation surface (the gateway's own names).
    for op in ('"model.list"', '"model.states"', '"model.load"',
               '"model.unload"'):
        assert op in text, f"the Models surface must call {op}"
    # wb-11: the load/unload circuits are RUNS (identity-then-poll) —
    # the per-call 420s/60s budgets died with the synchronous call
    # (the freeze chain's client-side half: the one-request queue can
    # never again wedge behind a minutes-class load).
    assert "MODEL_LOAD_TIMEOUT_S" not in text
    assert "MODEL_UNLOAD_TIMEOUT_S" not in text
    assert '_next_request_id("model-load-get")' in text
    assert '_next_request_id("model-unload-get")' in text
    assert "_on_model_load_get_answered" in text
    assert "_on_model_unload_get_answered" in text
    assert "MODEL_ACTION_STATES" in text
    # The truthful notes (the honest surface, never fakes).
    assert "OUTCOME UNKNOWN" in text
    assert "model.load refused" in text
    assert "model.states refused" in text
    # The FAILED diagnostics note carries the observed cause (§21).
    assert "load FAILED · " in text
    # wb-11: the honest picker/load guards — never a silent return
    # (§18: the effective state is named).
    assert "the models manager needs a live gateway session" in text
    assert "the load action needs a live gateway session" in text
    # wb-11: a failed scan re-arms — the empty list never sticks.
    assert "_models_requested = false" in text
    # The lifecycle states surface by name (D-203's gap shown, not hidden).
    assert '"FAILED"' in text
    assert "_on_model_load_pressed" in text
    assert "_on_model_unload_pressed" in text


def test_the_gateway_client_timeout_surface() -> None:
    """wb-8's client half: the per-call timeout rides the queue's own
    envelope (the property write lands at dispatch time), and the
    default floor stays the committed constant."""
    client = REDOT / "scripts" / "gateway_client.gd"
    text = client.read_text(encoding="utf-8")
    assert "timeout_s: float = DEFAULT_TIMEOUT_S" in text
    assert '"timeout_s": timeout_s' in text
    assert '_http.timeout = float(next.get("timeout_s", DEFAULT_TIMEOUT_S))' in text


def test_the_gdscript_warning_hygiene() -> None:
    """The owner-reported launcher warnings stay fixed: no UNUSED
    parameter (the chat-send answer's tag is _tag) and no SHADOWED
    name (the composer submit's body no longer shadows _text())."""
    text = SHELL_SCRIPT.read_text(encoding="utf-8")
    assert "func _on_chat_send_answered(_tag: String, document: Dictionary)" in text
    assert "func _on_composer_submitted(_body: String)" in text
    assert "func _on_composer_submitted(_text: String)" not in text
    client = REDOT / "scripts" / "gateway_client.gd"
    client_text = client.read_text(encoding="utf-8")
    assert "\t" not in client_text, (
        "the client file stays space-indented (the committed style)"
    )


def test_project_carries_the_gateway_url_setting() -> None:
    """The committed default the live shell falls back to — the same
    loopback URL scripts/workbench_app.py serves on (the launcher's
    DEFAULT_HOST/DEFAULT_PORT)."""
    text = PROJECT.read_text(encoding="utf-8")
    assert "[canonism_workbench]" in text
    assert 'gateway/url="http://127.0.0.1:8765"' in text


# ------------------------------------------- wb-9: the model-flow surface


def test_the_launch_settings_surface_is_real() -> None:
    """wb-9's frontend half: the Settings surface drives the gateway's
    own settings operations (backend.settings / backend.settings.update),
    carries the typed llama.cpp launch fields + the collapsed advanced
    extras + the command preview, and the honest next-spawn note —
    never a fake knob."""
    text = SHELL_SCRIPT.read_text(encoding="utf-8")
    for op in ('"backend.settings"', '"backend.settings.update"'):
        assert op in text, f"the Settings surface must call {op}"
    for marker in (
        "llama.cpp launch (managed)",
        "llama-server executable",
        "Context window (-c)",
        "GPU layers (-ngl)",
        "Flash attention (-fa)",
        "Temperature (--temp)",
        "Top-K (--top-k)",
        "Top-P (--top-p)",
        "Min-P (--min-p)",
        "Repeat penalty (--repeat-penalty)",
        "Extra flags",
        "command_preview",
    ):
        assert marker in text, f"the launch-settings field missing: {marker}"
    # the collapsed advanced surface + the honest note
    assert "_on_advanced_toggled" in text
    assert "a LIVE server keeps its flags until unloaded" in text
    assert "_populate_settings_fields" in text
    assert "backend.settings.update refused" in text


def test_the_model_manager_surface_is_real() -> None:
    """wb-9's Models manager: the fetch circuit rides run.start with
    the model.fetch work kind, polls run.get (the distinct fetch-get
    tag — no collision with the chat poll), cancels through run.cancel,
    and shows the live progress + the honest terminal notes."""
    text = SHELL_SCRIPT.read_text(encoding="utf-8")
    assert '"model.fetch"' in text
    assert '_next_request_id("fetch-start")' in text
    assert '_next_request_id("fetch-get")' in text
    assert '_next_request_id("fetch-cancel")' in text
    assert "_on_fetch_pressed" in text
    assert "_on_fetch_cancel_pressed" in text
    assert "_fetch_progress_note" in text
    assert "downloading" in text
    assert "fetch FAILED" in text
    assert "fetch canceled (the truthful terminal)" in text
    # the manager's hint names the one-command launcher
    assert "workbench_launch.py" in text


# ------------------------------------ wb-10: the local-import surface


def test_the_local_import_surface_is_real() -> None:
    """wb-10's frontend half (the owner's «просто открывающийся
    проводник и выбор уже скаченных локальных моделей» call): the
    NATIVE picker is the Models surface's PRIMARY flow — the OS file
    dialog (multiselect + the .gguf filter) and the OS folder dialog
    over the gateway's model.import work kind, the observed
    models_root driving Open models folder, the import run polled
    with its own tags and cancellable through run.cancel."""
    text = SHELL_SCRIPT.read_text(encoding="utf-8")
    # the native picker: the engine's FileDialog surface, by member
    assert "FileDialog.ACCESS_FILESYSTEM" in text
    assert "FileDialog.FILE_MODE_OPEN_FILES" in text
    assert "FileDialog.FILE_MODE_OPEN_DIR" in text
    assert "use_native_dialog = true" in text
    # the import circuit rides the gateway's own work kind + run family
    assert '"model.import"' in text
    assert '_next_request_id("import-start")' in text
    assert '_next_request_id("import-get")' in text
    assert '_next_request_id("import-cancel")' in text
    assert "_on_import_files_selected" in text
    assert "_on_import_dir_selected" in text
    assert "_on_import_start_answered" in text
    assert "_on_import_get_answered" in text
    assert "_on_import_cancel_pressed" in text
    assert "_import_progress_note" in text
    assert "import FAILED" in text
    assert "import canceled (the truthful terminal)" in text
    # the primary buttons + the folder-open action
    assert "_on_add_local_pressed" in text
    assert "_on_add_folder_pressed" in text
    assert "_on_open_models_folder_pressed" in text
    assert '"Add local models…"' in text
    # the models root arrives from the gateway's own answer, never a guess
    assert '"models_root"' in text
    assert "OS.shell_open" in text
    # the URL fetch demoted to the collapsed advanced row (still real)
    assert "_on_fetch_advanced_toggled" in text
    assert "_fetch_advanced_box.visible = _fetch_advanced_button.button_pressed" in text
    # the poll loop serves both transfer arms
    assert '_next_request_id("import-get"), "run.get"' in text


def test_the_zero_command_entry_is_committed() -> None:
    """wb-10's zero-command law (the owner's «пользователь не должен
    вводить команды чтобы запустить или скачать что-либо!» call): the
    double-click .bat entries live at the repo root, the offline hints
    name Workbench.bat FIRST, and the launcher's own resolution chain
    (the folder form + the persisted pick) is pinned in the committed
    script."""
    launch = REPO / "scripts" / "workbench_launch.py"
    launch_text = launch.read_text(encoding="utf-8")
    assert "bufsize=1" in launch_text, (
        "the gateway child's pipe is line-buffered through Popen's "
        "bufsize (the owner-reported TypeError: 'buffering' is not a "
        "Popen keyword)"
    )
    assert "redot.windows.editor.x86_64.exe" in launch_text, (
        "the owner's actual engine binary name is a known candidate"
    )
    assert "launcher.json" in launch_text
    assert "askdirectory" in launch_text, "the native folder picker"
    for name in ("Workbench.bat", "Workbench Setup.bat"):
        entry = REPO / name
        assert entry.is_file(), f"the double-click entry missing: {name}"
        bat = entry.read_text(encoding="utf-8")
        assert "workbench_launch.py" in bat
        assert "cd /d \"%~dp0\"" in bat
    shell_text = SHELL_SCRIPT.read_text(encoding="utf-8")
    assert "Workbench.bat" in shell_text, (
        "the offline hints name the double-click form first"
    )


def test_the_theme_visual_refresh_landed() -> None:
    """wb-12's token audit (iter-230, the owner's «тема и UI все так же
    убоги» call, VISUAL_SYSTEM_UI §2/§3 the law): the theme@0.3 tokens
    the re-skinned shell reads by name — the single-accent pin (the
    warm-orange family retired WITH its accent_deep token), the busy
    chip (the GENERATING carrier), and the NavButton variation's full
    state set (the rail's quiet controls) exist in the committed theme
    file — a renamed token is a runtime break the suite must catch
    textually (§10's single-source law)."""
    text = THEME.read_text(encoding="utf-8")
    for marker in (
        "Workbench/styles/chip",
        "Workbench/styles/chip_busy",
        "Workbench/styles/card_user",
        "Workbench/colors/accent_soft",
        "Workbench/constants/bar_height = 52",
        "NavButton/styles/normal",
        "NavButton/styles/hover",
        "NavButton/styles/pressed",
        "NavButton/styles/hover_pressed",
        "NavButton/styles/disabled",
        "NavButton/styles/focus",
        "NavButton/colors/font_color",
    ):
        assert marker in text, f"the theme@0.3 token missing: {marker}"
    # The audit's retire: the old warm accent's deep variant has no
    # consumer left — its return is a regression of the one-accent law.
    assert "Workbench/colors/accent_deep" not in text, (
        "accent_deep was retired at wb-12 (no consumer; the ONE accent "
        "family is accent/accent_soft/focus_ring)"
    )
    assert "canon_workbench_theme@0.3" in SHELL_SCRIPT.read_text(
        encoding="utf-8"
    )


# ------------------------------------ iter-230: wb-12 + the chat follow law


def test_the_chat_surface_smooth_follow() -> None:
    """iter-230 (the owner's «в чате при получении сообщений от языковой
    модели => не происходит плавной прокрутки вниз» call): the message
    list's follow law — the smooth TWEEN over the scrollbar's float
    value (never the integer scroll_vertical jump), the layout-settle
    await BEFORE the target is read (the autowrapped labels size late
    — reading max_value too early is the old short-scroll bug), the
    near-bottom gate (a reader scrolled into history is never yanked),
    the follow requested for EVERY role (the user's own message
    included), and the GENERATING state's visible carrier (the busy
    chip + the pulse, §4's not-color-only law)."""
    text = SHELL_SCRIPT.read_text(encoding="utf-8")
    # the smooth tween, not the integer jump
    assert "_scroll_to_bottom_smooth" in text
    assert 'bar, "value", target, SCROLL_TWEEN_S' in text
    assert "scroll_vertical = int(" not in text, (
        "the integer jump is the retired recipe — the tween owns the scroll"
    )
    # the layout-settle await before the target is read
    assert "await get_tree().process_frame" in text
    # the near-bottom gate + the deferred follow
    assert "_near_bottom" in text
    assert "SCROLL_FOLLOW_SLOP_PX" in text
    assert "_request_scroll_follow" in text
    assert "_scroll_follow_deferred.call_deferred(follows)" in text
    # the late-layout guard (one bounded re-settle, never a loop)
    assert "_after_follow_tween" in text
    # the follow is requested for every role — the old assistant-only
    # gate is gone from the card-append path
    append_block = text.split("func _add_message_card")[1].split(
        "func _request_scroll_follow"
    )[0]
    assert 'if role == "assistant":' not in append_block
    # the GENERATING carrier: the busy chip + the pulse, wired into the
    # single busy owner
    assert '_s("chip_busy")' in text
    assert "GENERATING" in text
    assert "_start_busy_pulse" in text
    assert "_stop_busy_pulse" in text
    assert "_busy_row.visible = busy" in text
    # the NavButton variation (the rail's quiet set, values in the
    # theme; KI#94: applied through the theme_type_variation PROPERTY —
    # Redot 26.2 has NO add_theme_type_variation method; the engine's
    # own 2026-09-25 report killed _ready at _build_nav_rail)
    assert 'set_type_variation("NavButton", "Button")' in text
    assert 'theme_type_variation = "NavButton"' in text
    assert "add_theme_type_variation" not in text


# ----------------------------------- iter-224: the literal-concatenation ban


def test_no_adjacent_string_literals_across_lines() -> None:
    """iter-224's regression: GDScript has NO implicit string-literal
    concatenation — wb-8 shipped five notes Python-style (two adjacent
    literals across lines inside parentheses) and the Redot 26.2 parser
    refused the whole file (the owner's 2026-09-25 report, shell.gd
    806/861/868/999/1042). Every committed .gd file keeps each note
    ONE literal per line — pinned textually so the regression fails
    the suite everywhere, not only where the engine binary is."""
    pattern = re.compile(r'"[ \t]*\r?\n[ \t]*"')
    scripts = sorted((REDOT / "scripts").glob("*.gd"))
    assert scripts, "the scripts directory must carry the committed clients"
    for script in scripts:
        text = script.read_text(encoding="utf-8")
        match = pattern.search(text)
        assert match is None, (
            f"{script.name}:{text[: match.start()].count(chr(10)) + 1}: "
            "adjacent string literals across lines — GDScript has no "
            "implicit concatenation (one literal per line, the iter-224 "
            "fix's shape)"
        )
