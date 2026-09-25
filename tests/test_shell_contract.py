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
STRINGS_SCRIPT = REDOT / "scripts" / "strings.gd"
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
    # The client + the honest default badge (ux-1: the literal lives in the
    # catalog — the boundary's single source; the shell wires it by key).
    assert "gateway_client.gd" in text
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")
    assert '"app.badge.not_connected": "CANONSIM · NOT CONNECTED"' in strings_text
    assert '_tr("app.badge.not_connected")' in text
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
    # The axis went live: models sits in SURFACES, not PLANNED (obs-1:
    # the IA re-pointed the flat list — WORK gains the Observatory).
    assert 'const SURFACES := ["chat", "observatory", "inference", "models", "settings"]' in text
    planned_line = text.split("PLANNED_SURFACES := ")[1].split("\n")[0]
    # inf-1: Inference went REAL (the SURFACES list) — the planned
    # set keeps Simulation and the honest remainder only.
    assert '"Simulation"' in planned_line
    assert '"Inference"' not in planned_line
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
    # The truthful notes (the honest surface, never fakes — ux-1: the
    # literals live in the strings.gd catalog, the wiring by key).
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")
    assert "OUTCOME UNKNOWN" in strings_text
    assert "model.load refused" in strings_text
    assert "model.states refused" in strings_text
    # The FAILED diagnostics note carries the observed cause (§21).
    assert "load FAILED · " in strings_text
    # wb-11: the honest picker/load guards — never a silent return
    # (§18: the effective state is named).
    assert "the models manager needs a live gateway session" in strings_text
    assert "the load action needs a live gateway session" in strings_text
    # KI#96 (iter-232): the scan latch is RETIRED — every entry into the
    # Models surface re-scans (§20's routine refresh; the owner's
    # «проводник опять сломался... модели не показывает» call — the
    # latched "requested once" flag froze the list after one scan and
    # hand-dropped GGUF files never appeared without a manual Refresh).
    assert 'if key == "models" and _client != null:' in text
    assert "_models_requested" not in text, (
        "the models-scan latch was retired at iter-232 — every surface "
        "entry re-scans; a resurrected latch re-freezes the list"
    )
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
    # ux-1: the field labels live in the strings.gd catalog (the boundary's
    # single source); the wiring rides the _tr keys, "command_preview"
    # stays a shell-side document field.
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")
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
        target = text if marker == "command_preview" else strings_text
        assert marker in target, f"the launch-settings field missing: {marker}"
    # the collapsed advanced surface + the honest note
    assert "_on_advanced_toggled" in text
    assert "a LIVE server keeps its flags until unloaded" in strings_text
    assert "_populate_settings_fields" in text
    assert "backend.settings.update refused" in strings_text


def test_the_model_manager_surface_is_real() -> None:
    """wb-9's Models manager: the fetch circuit rides run.start with
    the model.fetch work kind, polls run.get (the distinct fetch-get
    tag — no collision with the chat poll), cancels through run.cancel,
    and shows the live progress + the honest terminal notes."""
    text = SHELL_SCRIPT.read_text(encoding="utf-8")
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")
    assert '"model.fetch"' in text
    assert '_next_request_id("fetch-start")' in text
    assert '_next_request_id("fetch-get")' in text
    assert '_next_request_id("fetch-cancel")' in text
    assert "_on_fetch_pressed" in text
    assert "_on_fetch_cancel_pressed" in text
    assert "_fetch_progress_note" in text
    assert "downloading" in strings_text
    assert "fetch FAILED" in strings_text
    assert "fetch canceled (the truthful terminal)" in strings_text
    # the manager's hint names the one-command launcher (ux-1: catalog)
    assert "workbench_launch.py" in strings_text


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
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")
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
    assert "import FAILED" in strings_text
    assert "import canceled (the truthful terminal)" in strings_text
    # the primary buttons + the folder-open action
    assert "_on_add_local_pressed" in text
    assert "_on_add_folder_pressed" in text
    assert "_on_open_models_folder_pressed" in text
    assert '"Add local models…"' in strings_text
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
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")
    # ux-1: the hint literals live in the catalog; the shell wires them
    # by key (the boundary's own contract).
    assert "Workbench.bat" in strings_text, (
        "the offline hints name the double-click form first"
    )
    assert '_tr("chat.composer.offline")' in shell_text


def test_the_theme_visual_refresh_landed() -> None:
    """wb-12's token audit (iter-230) + iter-232's OLED re-pin (the
    owner's «цвет лучше взять темный под oled мониторы, но не синий
    такой убогий» call, VISUAL_SYSTEM_UI §2/§3 the law): the theme@0.4
    tokens the re-skinned shell reads by name — the single-accent pin
    (the warm-orange family retired WITH its accent_deep token; the
    Catppuccin blue retired with theme@0.4's neutral ramp), the busy
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
        assert marker in text, f"the theme@0.4 token missing: {marker}"
    # The audit's retire: the old warm accent's deep variant has no
    # consumer left — its return is a regression of the one-accent law.
    assert "Workbench/colors/accent_deep" not in text, (
        "accent_deep was retired at wb-12 (no consumer; the ONE accent "
        "family is accent/accent_soft/focus_ring)"
    )
    # iter-232's OLED form: the base sits at the near-black #050505
    # (Color(0.02, 0.02, 0.02, 1) — truly neutral, R=G=B: no blue tint)
    # and the ONE accent is the teal family (not the retired blue).
    assert "Workbench/colors/background_base = Color(0.02, 0.02, 0.02, 1)" in text
    assert "Workbench/colors/accent = Color(0.298, 0.788, 0.651, 1)" in text
    assert "canon_workbench_theme@0.4" in SHELL_SCRIPT.read_text(
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


# ------------------------------------- ux-1: the P0 minimums (FRONTEND_UIUX_LAW §25)


def _catalog_keys(locale_block: str) -> set[str]:
    """Parse a catalog block's keys (`"key": "value",` lines)."""
    keys: set[str] = set()
    for line in locale_block.splitlines():
        match = re.match(r'^\s*"([^"]+)":\s*".*",\s*$', line)
        if match:
            keys.add(match.group(1))
    return keys


def test_the_localization_boundary() -> None:
    """ux-1 (FRONTEND_UIUX_LAW §17): ONE translation boundary — strings.gd
    carries the en/ru catalogs; every user-facing GDScript string rides a
    `_tr()` key; the shell holds no raw display literals; the two catalogs
    stay key-identical (a missing ru key renders the key itself — visible,
    but a contract breach the suite must catch); and the catalog never
    defines `static func tr(` (the Object.tr signature conflict that
    refused the whole shell at parse — this row's own parse lesson)."""
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")
    shell_text = SHELL_SCRIPT.read_text(encoding="utf-8")

    # The catalog's shape: two locale blocks, key-identical, substantive.
    en_block = strings_text.split("const EN := {")[1].split("\n}")[0]
    ru_block = strings_text.split("const RU := {")[1].split("\n}")[0]
    en_keys = _catalog_keys(en_block)
    ru_keys = _catalog_keys(ru_block)
    assert len(en_keys) >= 150, "the catalog is substantive (the full shell)"
    assert en_keys == ru_keys, (
        "the en/ru catalogs drifted — every key must exist in BOTH locales "
        f"(en-only: {sorted(en_keys - ru_keys)}, ru-only: {sorted(ru_keys - en_keys)})"
    )

    # The boundary wiring: the shell preloads the catalog and resolves the
    # locale (arg > env > OS, pinned "en" in proof mode).
    assert 'preload("res://scripts/strings.gd")' in shell_text
    assert "func _tr(key: String) -> String:" in shell_text
    assert "_resolve_locale" in shell_text
    assert '"--lang"' in shell_text and "CANONSIM_LANG" in shell_text
    assert "get_locale_language" in shell_text

    # Every STATIC _tr key the shell references exists in the catalog
    # (comment text is stripped — the code is what the runtime resolves).
    code_only = "\n".join(
        line.split("#", 1)[0] if "#" in line else line
        for line in shell_text.splitlines()
    )
    referenced = set(re.findall(r'_tr\("([^"]+)"\)', code_only))
    assert referenced, "the shell must reference catalog keys"
    missing = referenced - en_keys
    assert not missing, f"shell references unknown catalog keys: {sorted(missing)}"

    # The dynamic composes resolve too: nav.<surface>, nav.planned.<axis>,
    # chat.role.<role> (the runtime key-build families).
    for key in ("nav.chat", "nav.models", "nav.settings", "nav.inference"):
        assert key in en_keys
    for axis in ("Prompts", "History", "Diagnostics", "Simulation"):
        assert f"nav.planned.{axis.lower()}" in en_keys
    for role in ("user", "assistant"):
        assert f"chat.role.{role}" in en_keys

    # The boundary law: NO raw user-facing literals left in the shell —
    # direct string assignments to display surfaces are catalog keys now.
    # Allowed to stay literal BY LAW: the canonical protocol vocabulary
    # (model lifecycle states — the authority words render verbatim, like
    # CANONICAL · OBSERVED · DERIVED in the status bar legend, never
    # re-worded) and format-joins of OBSERVED values ("%s · %s").
    vocabulary_literals = {"DISCOVERED"}
    banned_patterns = [
        (re.compile(r'\.text = "([^"]+)"'), "raw .text literal"),
        (re.compile(r'\.placeholder_text = "[^"]+"'), "raw placeholder literal"),
        (re.compile(r'tooltip_text = "[^"]+"'), "raw tooltip literal"),
        (re.compile(r'_caption\("[^"]+"\)'), "raw _caption literal"),
    ]
    for pattern, label in banned_patterns:
        for match in pattern.finditer(code_only):
            captured = match.group(1) if match.groups() else ""
            assert captured in vocabulary_literals, (
                f"{label} '{match.group(0)}' at offset {match.start()}: the "
                "user-facing string must ride the _tr boundary (LAW §17); "
                "only the canonical protocol vocabulary renders verbatim"
            )

    # The parse lesson pinned: Object.tr's native signature makes
    # `static func tr(` a PARSE ERROR — the catalog's resolver is `lookup`.
    assert "static func lookup(key: String, locale: String) -> String:" in strings_text
    assert "static func tr(" not in strings_text

    # Cyrillic-safe layout: the fixed-width action controls carry the
    # tolerance (112px — «Отправить»/«Загрузить»), never the 96px accident.
    assert "Vector2(112, 40)" in shell_text
    assert "Vector2(112, 0)" in shell_text


def test_the_reduced_motion_contract() -> None:
    """ux-1 (FRONTEND_UIUX_LAW §15): every motion effect keeps a static
    equivalent — the chat follow tween (a direct bar.value jump) and the
    busy pulse (the steady dot + label) — the toggle is visible in the
    Settings Interface section, persisted UI-locally (workbench/runtime/
    ui_state.json), and proof mode never reads or writes it (the
    byte-identical capture law)."""
    shell_text = SHELL_SCRIPT.read_text(encoding="utf-8")
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")

    # The two motion carriers gain their static branches.
    assert "if _motion_reduced:" in shell_text
    follow_block = shell_text.split("func _scroll_to_bottom_smooth")[1].split(
        "func _after_follow_tween"
    )[0]
    assert "bar.value = target" in follow_block, (
        "the reduced follow jumps directly — never an animated scroll"
    )
    pulse_block = shell_text.split("func _start_busy_pulse")[1].split(
        "func _stop_busy_pulse"
    )[0]
    assert "if _motion_reduced:" in pulse_block, (
        "the busy pulse parks behind the flag — the steady chip carries it"
    )

    # The visible, reversible toggle (Settings → Interface).
    assert "_build_interface_section" in shell_text
    assert "_on_reduced_motion_toggled" in shell_text
    assert '"settings.reduced_motion"' in strings_text

    # UI-local persistence: the runtime root's ui_state.json, honest
    # corrupt-refuse, and NEVER touched in proof mode.
    assert "ui_state.json" in shell_text
    assert "_load_ui_state" in shell_text and "_save_ui_state" in shell_text
    save_block = shell_text.split("func _save_ui_state")[1].split("\nfunc ")[0]
    assert "if _proof_mode:" in save_block, (
        "proof never persists UI state (the byte-identical capture law)"
    )


def test_the_viewport_policy() -> None:
    """ux-1 (FRONTEND_UIUX_LAW §16): the fixed 1440x900 baseline gains its
    product contract — the min window floor (1152x700, the SMALL class),
    stretch canvas_items + expand (content scales with the window, extra
    space fills the content region, no critical clipping)."""
    text = PROJECT.read_text(encoding="utf-8")
    for marker in (
        "window/size/viewport_width=1440",
        "window/size/viewport_height=900",
        "window/size/min_width=1152",
        "window/size/min_height=700",
        'window/size/stretch/mode="canvas_items"',
        'window/size/stretch/aspect="expand"',
    ):
        assert marker in text, f"the viewport policy setting missing: {marker}"


def test_the_focus_keyboard_baseline() -> None:
    """ux-1 (FRONTEND_UIUX_LAW §15): the keyboard baseline — Escape cancels
    the live transient (an active generation), Ctrl+. stops it from
    anywhere, both honest no-ops when idle; the surface switch restores
    MEANINGFUL focus (Chat → composer, Models → refresh, Settings → the
    first launch field), deferred one frame so visibility settles."""
    shell_text = SHELL_SCRIPT.read_text(encoding="utf-8")
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")

    # The shortcut contract.
    assert "func _unhandled_input(event: InputEvent) -> void:" in shell_text
    input_block = shell_text.split("func _unhandled_input")[1].split("\nfunc ")[0]
    assert "KEY_ESCAPE" in input_block
    assert "KEY_PERIOD" in input_block and "ctrl_pressed" in input_block
    assert "_on_stop_pressed()" in input_block, (
        "the shortcuts drive the SAME stop action as the button — never a "
        "second cancel path"
    )
    assert "set_input_as_handled" in input_block

    # The task-aware focus entry (deferred so visibility settles).
    assert "_focus_surface_entry.call_deferred(key)" in shell_text
    focus_block = shell_text.split("func _focus_surface_entry")[1].split("\nfunc ")[0]
    assert "_composer_input.grab_focus()" in focus_block
    assert "_models_refresh_button.grab_focus()" in focus_block
    assert "_llama_exe_edit.grab_focus()" in focus_block
    # Offline honesty: a disabled entry control leaves focus untouched.
    assert "_composer_input.editable" in focus_block

    # Discoverability: the Stop button carries the shortcut in its tooltip.
    assert "chat.stop.tooltip" in shell_text
    assert '"chat.stop.tooltip"' in strings_text


# ------------------------------------- obs-1: the Observatory vertical slice


def test_the_observatory_slice_is_real() -> None:
    """obs-1 (FRONTEND_UIUX_LAW §25's P1 + §50/§51): the vertical UX
    slice — the interaction grammar BEFORE full analytical backend
    coverage. The pins hold the slice's own law: the responsibility
    split (observatory.gd composes itself, the shell only hosts), the
    §4.1 IA grouping (WORK/RESOURCES/SYSTEM — never a flat catalog),
    the workspace regions (breadcrumb/context/question/primary view/
    inspector/evidence ladder), the honest empty semantics (NO DATA,
    never a fake), the read-only DRAFT lifecycle (no dispatch), and
    the _tr boundary from birth (INVARIANT: zero user-facing literals
    in observatory.gd)."""
    obs = REDOT / "scripts" / "observatory.gd"
    assert obs.is_file(), "the Observatory's own script (LAW §18's split seed)"
    text = obs.read_text(encoding="utf-8")
    shell_text = SHELL_SCRIPT.read_text(encoding="utf-8")
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")

    # The responsibility split: the surface composes ITSELF through the
    # injected theme + the shell's own _tr Callable (one boundary, the
    # observatory never opens the catalog directly).
    assert 'preload("res://scripts/observatory.gd")' in shell_text
    assert "func compose(theme: Theme, translator: Callable) -> void:" in text
    assert 'Callable(self, "_tr")' in shell_text
    assert "_build_observatory_surface" in shell_text

    # The §4.1 IA: intent groups, not a flat feature catalog.
    assert 'const SURFACE_GROUPS := [' in shell_text
    assert '"keys": ["chat", "observatory", "inference"]' in shell_text
    assert '"keys": ["models"]' in shell_text
    assert '"keys": ["settings"]' in shell_text
    assert '"nav.group.work"' in strings_text
    assert '"nav.group.resources"' in strings_text
    assert '"nav.group.system"' in strings_text
    # The planned axes ride their groups; Runs joined (the LAW's map);
    # inf-1: Inference went REAL (the SURFACES list above) — the
    # planned set keeps the honest remainder, nothing silently dropped.
    planned_line = shell_text.split("PLANNED_SURFACES := ")[1].split("\n")[0]
    for axis in ("Simulation", "Prompts", "History", "Runs", "Diagnostics"):
        assert f'"{axis}"' in planned_line, f"the planned axis missing: {axis}"
    assert '"Inference"' not in planned_line, (
        "Inference is a REAL surface now (inf-1) — never a planned axis"
    )

    # The workspace regions (LAW §5.1) — each region composes.
    for region in (
        "_build_breadcrumb",
        "_build_context_strip",
        "_build_question_contract",
        "_build_workspace",
        "_build_primary_view",
        "_build_inspector",
        "_build_evidence_ladder",
    ):
        assert region in text, f"the workspace region missing: {region}"
    # ONE primary representation + the split workspace (the inspector
    # region rides an HSplitContainer — collapsible, per LAW §5.1).
    assert "HSplitContainer" in text

    # The honest empty semantics (LAW §16): NO DATA is distinct — the
    # note names why, and never collapses to "no match"/"no evidence".
    assert '"obs.empty.no_data"' in strings_text
    assert "no match" in strings_text and "no evidence" in strings_text

    # The context identity strip (LAW §42): the six axes, honest values.
    for axis in ("pack", "run", "seed", "tick", "profile", "revision"):
        assert f'"obs.context.{axis}"' in strings_text
    assert '"obs.context.no_session"' in strings_text

    # The World Question contract (LAW §51.1) + the DRAFT lifecycle.
    for field_name in ("question", "class", "target", "scope"):
        assert f'"obs.question.{field_name}"' in strings_text
    assert '"obs.lifecycle.draft"' in strings_text

    # The evidence ladder (LAW §12): the five rungs, the status as TEXT
    # (never color-only — §13).
    for rung in ("read", "branch", "state", "divergence", "persistence"):
        assert f'"obs.evidence.{rung}"' in strings_text
    assert '"obs.evidence.unknown"' in strings_text

    # The boundary from birth: observatory.gd holds ZERO user-facing
    # literals (the same banned-pattern law as the shell).
    code_only = "\n".join(
        line.split("#", 1)[0] if "#" in line else line
        for line in text.splitlines()
    )
    for pattern in (
        re.compile(r'\.text = "[^"]+"'),
        re.compile(r'_caption\("[^"]+"\)'),
    ):
        assert pattern.search(code_only) is None, (
            "the observatory rides the _tr boundary from birth (LAW §17) — "
            f"raw literal: {pattern.pattern}"
        )
    # Every static _tr key the observatory references exists in the catalog.
    referenced = set(re.findall(r'_tr\("([^"]+)"\)', code_only))
    en_block = strings_text.split("const EN := {")[1].split("\n}")[0]
    en_keys = _catalog_keys(en_block)
    missing = referenced - en_keys
    assert not missing, f"observatory references unknown keys: {sorted(missing)}"

    # No dispatch, no transport, no fabricated state (INVARIANT 1/2 + the
    # read-only slice law): the file never dials anything.
    for banned in ("call_operation", "HTTPRequest", "session.create", "run.start"):
        assert banned not in text, (
            f"the slice is read-only — {banned} is a dispatch surface"
        )




def test_the_observatory_live_feed_is_real() -> None:
    """obs-2 (FRONTEND_UIUX_LAW §25's P1 continuation): the live run
    over the READ-side seam — observatory.runs + observatory.read
    (the bounded read model over the canonical JSONL log, INV-1's own
    truth) + the SELECTION MODEL's first consumer (LAW §6: select
    event E → the inspector opens E → the evidence view scopes to E →
    the breadcrumb carries the semantic path). The pins hold the
    seam's law: the shell owns the transport (the observatory speaks
    ONLY through its two request signals), the boundedness ceiling is
    the OP's own (never a UI-side second limit), the selection is the
    semantic identity (the event id — never a row index), and the
    distinct empty semantics never collapse (probing ≠ NO RUNS ≠ NO
    EVENTS ≠ refused)."""
    obs = REDOT / "scripts" / "observatory.gd"
    text = obs.read_text(encoding="utf-8")
    shell_text = SHELL_SCRIPT.read_text(encoding="utf-8")
    strings_text = STRINGS_SCRIPT.read_text(encoding="utf-8")
    proof_text = (REDOT / "scripts" / "seam_proof.gd").read_text(encoding="utf-8")
    runner_text = (REPO / "scripts" / "visual_proof.py").read_text(encoding="utf-8")

    # The seam's form: the observatory never touches the gateway client —
    # two request signals out, feed methods in (LAW §18's split: the
    # shell owns the seam, the axis owns its regions).
    assert "signal runs_requested()" in text
    assert "signal read_requested(run: String, after: String)" in text
    assert "call_operation" not in text  # the slice never dials; the shell does
    for feed in ("feed_runs", "feed_read", "feed_rejection", "feed_transport_failure"):
        assert f"func {feed}(" in text, f"the feed method missing: {feed}"
    assert "runs_requested.connect(_on_observatory_runs_requested)" in shell_text
    assert "read_requested.connect(_on_observatory_read_requested)" in shell_text
    assert 'call_operation("observatory-runs", "observatory.runs", {})' in shell_text
    assert '"observatory.read"' in shell_text

    # The boundedness law's single ceiling: the shell's read dispatch
    # carries NO limit — the op's own default (50, cap 200) is the one
    # source (workbench/observatory_read.py owns the constants; the UI
    # never re-declares a page size).
    assert "DEFAULT_WINDOW = 50" in (
        REPO / "workbench" / "observatory_read.py"
    ).read_text(encoding="utf-8")
    assert "limit" not in shell_text.split("_on_observatory_read_requested")[1].split(
        "func "
    )[0], "the shell must not re-declare a read limit (the op's default is the law)"

    # The selection model (LAW §6.2): the semantic identity rides the
    # button's metadata — set_meta/get_meta over the event id, never a
    # row index; the restore is by id (§6.1's stability across re-reads).
    assert 'button.set_meta("row", row)' in text
    assert 'child.get_meta("row", {})' in text
    assert "_restore_selection" in text
    assert "get_selected_index" not in text and "get_child(" not in text.split(
        "_restore_selection"
    )[1].split("func ")[0], "the selection restores by ID, never by position"

    # The distinct empty semantics (LAW §16 — never one generic empty):
    # probing (the listing not yet answered) ≠ NO RUNS (the root holds
    # none) ≠ NO EVENTS (the run holds only its header) ≠ refused
    # (the backend's observed cause) — each with its own note.
    for key in (
        "obs.state.probing",
        "obs.state.probing_note",
        "obs.empty.no_runs",
        "obs.empty.no_runs_note",
        "obs.empty.no_events",
        "obs.empty.no_events_note",
        "obs.read.rejected",
        "obs.read.rejected_note",
        "obs.read.transport",
    ):
        assert f'"{key}"' in strings_text, f"the distinct empty key missing: {key}"

    # The evidence ladder's honest scoping (LAW §12): only the READ rung
    # confirms under a selection; the declared cause never confirms
    # BRANCH by itself.
    assert '"obs.evidence.confirmed"' in strings_text
    assert '"obs.evidence.scope_note"' in strings_text
    assert '"obs.evidence.no_verified_claim"' in strings_text
    assert "_scope_ladder" in text and "_clear_ladder_scoping" in text

    # The pagination: the cursor stack over event ids; next_after null
    # disables Later (never a request past the run's end).
    assert '"--obs-document"' not in proof_text  # the seam harness stays untouched
    for pin in ("_cursor_stack", "_page_sizes", "next_after"):
        assert pin in text, f"the pagination primitive missing: {pin}"
    for key in ("obs.page.earlier", "obs.page.later", "obs.page.status"):
        assert f'"{key}"' in strings_text

    # The proof injection (LAW §43's runtime form): --obs-document is
    # PROOF-MODE ONLY (the interactive path always rides the gateway);
    # the shell parses it, applies it through the SAME feed path, and
    # the meta carries the loaded run's stem (a loaded capture never
    # masquerades as an empty one). The engine law rides the code:
    # JSON.parse_string (Redot 26.2 — parse is an instance method).
    assert '"--obs-document"' in shell_text
    assert "JSON.parse_string(" in shell_text
    assert "JSON.parse(" not in shell_text
    assert '"observatory_run": _proof_obs_run' in shell_text
    assert "apply_read_document" in shell_text and "get_tree().quit(4)" in shell_text
    assert '"--obs-document"' in runner_text  # the runner passes it through verbatim

    # The float law's read-side arm: Redot's JSON yields floats for
    # every number — the canonical ints (seed, tick, counts, the
    # provenance) normalize back, never "42.0".
    assert "_int_text" in text and "_normalize_numbers" in text

    # The every-static-key law (the obs-1 contract's own form, rerun over
    # the grown surface).
    code_only = "\n".join(
        line.split("#", 1)[0] if "#" in line else line
        for line in text.splitlines()
    )
    referenced = set(re.findall(r'_tr\("([^"]+)"\)', code_only))
    en_block = strings_text.split("const EN := {")[1].split("\n}")[0]
    missing = referenced - _catalog_keys(en_block)
    assert not missing, f"observatory references unknown keys: {sorted(missing)}"
