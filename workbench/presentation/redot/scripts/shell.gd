# CanonSim Workbench — the wb-2/wb-7 application shell (frontend §46
# Phase A: custom theme -> Chat -> Settings).
#
# What this script is: the Workbench's application shell, built FROM CODE on
# the committed semantic-token theme (themes/workbench_theme.tres — every
# colour/size/style arrives by token name, never a raw value: frontend §10).
# The layout is the §17 information architecture: a top bar (identity + the
# backend state badge — §18's "never hide effective backend state"), a nav
# rail with the surface axes (Chat + Settings live at wb-2; the later axes
# present as honestly DISABLED rows, never faked), the content surfaces, and
# a status bar carrying the §16 authority vocabulary (displayed, never
# collapsed). The shell owns presentation-local state only (CONTRACTS §5 D2):
# no canon writes, no invented facts, no second semantic store.
#
# wb-10 — the owner's 2026-09-25 fix list («просто открывающийся проводник
# и выбор уже скаченных локальных моделей» + «интерфейс вверх убожества»):
# the Models surface's PRIMARY flow becomes the NATIVE picker — Add local
# models… (the OS file dialog, multiselect, .gguf filter) and Add folder…
# (the OS folder dialog; the .gguf files inside land through the same run)
# over the gateway's model.import work kind (run.start -> run.get -> the
# refreshed discovery list; Cancel = run.cancel — the honest §12.3 truth).
# Open models folder rides OS.shell_open on the gateway's OWN models_root
# answer (never a local guess). The URL fetch demotes to the collapsed
# advanced row (still fully functional — the manager's download arm). The
# visual pass: the token refresh (theme@0.2 — the warmer surface ramp, the
# chip/card styleboxes) + the message cards' role styling + the taller nav.
#
# wb-9 — the model-flow row (the owner's 2026-09-25 «открыл воркбенч, зашел
# и загрузил модель» + «настройки запуска llama.cpp... сэмплеры всякие»
# calls): the Settings surface goes REAL — the llama.cpp launch settings
# (backend.settings / backend.settings.update over the gateway: the typed
# fields + the collapsed advanced extras + the effective command preview,
# the honest next-spawn note when a server is LIVE) — and the Models
# surface gains the MANAGER: a URL (direct / huggingface.co / the hf:
# shorthand) fetches a GGUF into the models folder as a RUN with live
# progress (run.start model.fetch -> the run.get poll -> the refreshed
# discovery list; Stop = run.cancel). Every value shown is the gateway's
# own answer — never a local guess, never a fake.
#
# wb-8 — the Models surface (frontend §46 Phase A's Models row, the
# owner's «выбирать модель я должно из интерфейса» call): the
# DISCOVERED list over model.list + the per-model Model-lifecycle
# states over model.states (wb-5/wb-6's registered operations — the
# load-state read surface's own consumer), the Load/Unload actions
# over model.load/model.unload (the honest per-call timeout: the
# managed backend's spawn + weight load is minutes-class), and the
# honest notes everywhere — no gateway, no session, no fake. The
# llama.cpp process itself stays behind the gateway (G8): a Load on
# a managed launcher is what spawns llama-server — the frontend
# never sees the process, only the observed outcome.
#
# wb-7 — the live chat circuit: without proof args the shell dials the
# Workbench gateway (scripts/workbench_app.py's loopback POST /op) through
# the typed client (scripts/gateway_client.gd): app.status probe ->
# session.create -> chat.send (the §19.1 walk: the execution identity
# returns immediately) -> run.get polling to the truthful terminal ->
# the message lands. Stop is run.cancel (§18: streaming state visible,
# Stop discoverable). The frontend NEVER dials llama.cpp (frontend §47 G8);
# every observation is honest — transport failures, rejections and run
# failures surface as notes, never as fakes.
#
# Proof mode (--png/--meta) stays the wb-2 DETERMINISTIC form: the shell
# composes WITHOUT the live circuit (no network, no clock in the capture),
# awaits one clean frame, captures the screenshot + writes the proof
# metadata, then exits 0 (the headless/screenshot route — frontend §44).
#
# Invocation (the operator runner scripts/visual_proof.py --shell):
#   <redot> --path <project> res://scenes/shell.tscn -- --png <p> --meta <m>
# Live invocation (the owner's form):
#   <redot> --path <project> -- --gateway-url http://127.0.0.1:8765
#   (or the CANONSIM_GATEWAY_URL env var, or the committed project setting
#   canonism_workbench/gateway/url — that order).
extends Control

const SHELL_VERSION := "canon_shell@0.3"
const THEME_PATH := "res://themes/workbench_theme.tres"
const GATEWAY_CLIENT_SCRIPT := preload("res://scripts/gateway_client.gd")
const GATEWAY_URL_SETTING := "canonism_workbench/gateway/url"
const GATEWAY_DEFAULT_URL := "http://127.0.0.1:8765"
const SURFACES := ["chat", "models", "settings"]
const PLANNED_SURFACES := ["Inference", "Prompts", "History", "Diagnostics", "Simulation"]
const CHAT_ROLES := ["user", "assistant"]
const POLL_INTERVAL_S := 0.3
const MAX_MESSAGES := 500
const MAX_POLL_FAILURES := 10
# The Models surface's loadable resting states (the ladder's own
# vocabulary — MODEL_ACTION_STATES feeds the row's Load enablement).
const MODEL_ACTION_STATES := ["DISCOVERED", "SELECTED", "EVICTED"]
# wb-11 — model.load/unload dispatch as RUNS (the owner's «молча
# висят + транспорт результ 13» call): the dispatch is a fast admit
# (identity-then-poll, the chat.send/import shape) — the minutes-class
# spawn/readiness walk rides run.get on the shared tick, and NO call
# ever wedges the one-request queue behind a long load again (the
# per-call 420s/60s budgets died with the synchronous call).
const MODEL_LOAD_NOTE_MAX_LENGTH := 240
# The model manager's own budgets (wb-9): the fetch run's dispatch is a
# quick admit (identity-then-poll — the run.get reads carry the progress);
# the poll cadence rides the shared POLL_INTERVAL_S tick. The import run
# (wb-10) rides the same shape — one transfer class, two arrival arms.
const FETCH_NOTE_MAX_LENGTH := 240
# The import dialog's filters (wb-10): .gguf first, everything else
# second — the registry accepts any plain file, the filter is a
# convenience, never a gate.
const IMPORT_FILTERS := ["*.gguf ; GGUF model files", "* ; All files"]

# The Settings surface's own state (wb-9): the launch-settings document
# arrives from backend.settings (the gateway's own answer); the preview
# label carries the command the NEXT managed spawn would run.
const FA_FORMS := ["on", "off", "auto"]

var _t: Theme
var _surface_nodes: Dictionary = {}
var _active_surface := "chat"
var _nav_buttons: Dictionary = {}

var _client: Node
var _gateway_url := ""
var _session_id := ""
var _session_live := false
var _request_counter := 0
var _active_execution := ""
var _poll_failures := 0
var _messages: Array[Dictionary] = []
var _trimmed_note_shown := false

var _badge_label: Label
var _badge_dot: ColorRect
var _messages_box: VBoxContainer
var _messages_scroll: ScrollContainer
var _empty_note: Label
var _empty_center: CenterContainer
var _models_empty_center: CenterContainer
var _composer_input: LineEdit
var _send_button: Button
var _stop_button: Button
var _poll_timer: Timer
var _settings_gateway_value: Label
var _settings_backend_value: Label
var _gateway_state_label: Label
var _models_list: VBoxContainer
var _models_scroll: ScrollContainer
var _models_empty_note: Label
var _models_status_label: Label
var _models_refresh_button: Button
var _models_active_label: Label
var _model_rows: Dictionary = {}
var _models_requested := false
# wb-11 — the load/unload run circuits (identity-then-poll).
var _load_execution := ""
var _load_model := ""
var _load_poll_failures := 0
var _unload_execution := ""
var _unload_model := ""
var _unload_poll_failures := 0
# wb-9 — the model manager (the fetch circuit) + the launch settings.
var _fetch_input: LineEdit
var _fetch_button: Button
var _fetch_cancel_button: Button
var _fetch_status_label: Label
var _fetch_execution := ""
var _fetch_poll_failures := 0
# wb-10 — the local-import circuit (the native picker) + its controls.
var _import_dialog: FileDialog
var _add_files_button: Button
var _add_folder_button: Button
var _open_folder_button: Button
var _import_cancel_button: Button
var _fetch_advanced_button: Button
var _fetch_advanced_box: VBoxContainer
var _import_execution := ""
var _import_poll_failures := 0
var _models_root := ""
var _settings_scroll: ScrollContainer
var _llama_exe_edit: LineEdit
var _ctx_spin: SpinBox
var _ngl_spin: SpinBox
var _fa_option: OptionButton
var _jinja_check: CheckBox
var _no_webui_check: CheckBox
var _temp_spin: SpinBox
var _topk_spin: SpinBox
var _topp_spin: SpinBox
var _minp_spin: SpinBox
var _repeat_spin: SpinBox
var _extra_edit: LineEdit
var _advanced_box: VBoxContainer
var _advanced_button: Button
var _preview_label: Label
var _settings_status_label: Label
var _settings_save_button: Button


func _ready() -> void:
        _t = theme
        _build()
        var paths := _parse_proof_args(OS.get_cmdline_user_args())
        if paths.is_empty():
                _start_live_circuit(OS.get_cmdline_user_args())
                return  # interactive launch: the live circuit owns the runtime
        if paths.has("surface"):
                if not (paths["surface"] in SURFACES):
                        push_error("shell: unknown --surface %s (have %s)" % [paths["surface"], ", ".join(SURFACES)])
                        get_tree().quit(2)
                        return
                _show_surface(paths["surface"])
        _capture_and_quit.call_deferred(paths)


# --- token access (the theme file is the single source — §10) ---------------


func _c(token: String) -> Color:
        return _t.get_color(token, "Workbench")


func _k(token: String) -> int:
        return _t.get_constant(token, "Workbench")


func _s(token: String) -> StyleBox:
        return _t.get_stylebox(token, "Workbench")


# --- composition -------------------------------------------------------------


func _build() -> void:
        var floor_rect := ColorRect.new()
        floor_rect.color = _c("background_base")
        floor_rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
        add_child(floor_rect)

        var root := VBoxContainer.new()
        root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
        root.add_theme_constant_override("separation", 0)
        add_child(root)

        root.add_child(_build_top_bar())
        root.add_child(_build_body())
        root.add_child(_build_status_bar())
        _show_surface("chat")


func _build_top_bar() -> Control:
        var bar := PanelContainer.new()
        bar.add_theme_stylebox_override("panel", _s("bar"))
        var row := HBoxContainer.new()
        row.custom_minimum_size = Vector2(0, _k("bar_height"))
        row.add_theme_constant_override("separation", _k("space_m"))
        bar.add_child(row)

        var title := Label.new()
        title.text = "CanonSim Workbench"
        title.add_theme_font_size_override("font_size", _k("font_size_page_title"))
        title.add_theme_color_override("font_color", _c("text_primary"))
        title.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        row.add_child(title)

        var spring := Control.new()
        spring.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        row.add_child(spring)

        var badge := PanelContainer.new()
        badge.add_theme_stylebox_override("panel", _s("chip"))
        var badge_row := HBoxContainer.new()
        badge_row.add_theme_constant_override("separation", _k("space_s"))
        badge.add_child(badge_row)
        _badge_dot = ColorRect.new()
        _badge_dot.color = _c("status_warning")
        _badge_dot.custom_minimum_size = Vector2(8, 8)
        _badge_dot.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        badge_row.add_child(_badge_dot)
        _badge_label = Label.new()
        _badge_label.text = "CANONSIM · NOT CONNECTED"
        _badge_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        _badge_label.add_theme_color_override("font_color", _c("status_warning"))
        badge_row.add_child(_badge_label)
        badge.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        row.add_child(badge)
        return bar


func _build_body() -> Control:
        var body := HBoxContainer.new()
        body.size_flags_vertical = Control.SIZE_EXPAND_FILL
        body.add_theme_constant_override("separation", 0)
        body.add_child(_build_nav_rail())

        var gutter := MarginContainer.new()
        gutter.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        for side in ["left", "right", "top", "bottom"]:
                gutter.add_theme_constant_override("margin_" + side, _k("space_m"))
        var content := PanelContainer.new()
        content.add_theme_stylebox_override("panel", _s("surface"))
        content.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        content.clip_contents = true
        gutter.add_child(content)
        body.add_child(gutter)

        _surface_nodes["chat"] = _build_chat_surface()
        _surface_nodes["models"] = _build_models_surface()
        _surface_nodes["settings"] = _build_settings_surface()
        for key in SURFACES:
                _surface_nodes[key].size_flags_vertical = Control.SIZE_EXPAND_FILL
                content.add_child(_surface_nodes[key])
        return body


func _build_nav_rail() -> Control:
        var rail := PanelContainer.new()
        rail.add_theme_stylebox_override("panel", _s("surface"))
        rail.custom_minimum_size = Vector2(_k("rail_width"), 0)

        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_s"))
        rail.add_child(col)

        col.add_child(_caption("SURFACES"))
        var group := ButtonGroup.new()
        for key in SURFACES:
                var btn := _nav_button(key.capitalize())
                btn.toggle_mode = true
                btn.button_group = group
                btn.pressed.connect(_on_surface_selected.bind(key))
                col.add_child(btn)
                _nav_buttons[key] = btn
                if key == "chat":
                        btn.button_pressed = true

        col.add_child(_caption("PLANNED · LATER WB ROWS"))
        for axis_name in PLANNED_SURFACES:
                var later := _nav_button(axis_name)
                later.disabled = true
                col.add_child(later)

        var spring := Control.new()
        spring.size_flags_vertical = Control.SIZE_EXPAND_FILL
        col.add_child(spring)

        var version := Label.new()
        version.text = "%s · theme %s" % [SHELL_VERSION, "canon_workbench_theme@0.2"]
        version.add_theme_font_size_override("font_size", _k("font_size_caption"))
        version.add_theme_color_override("font_color", _c("text_muted"))
        version.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        col.add_child(version)
        return rail


func _nav_button(label: String) -> Button:
        var btn := Button.new()
        btn.text = label
        btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
        btn.custom_minimum_size = Vector2(0, 40)
        return btn


func _caption(text: String) -> Label:
        var label := Label.new()
        label.text = text
        label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        label.add_theme_color_override("font_color", _c("text_muted"))
        return label


func _surface_header(title: String, subtitle: String) -> Control:
        var header := VBoxContainer.new()
        header.add_theme_constant_override("separation", _k("space_xs"))
        var head := Label.new()
        head.text = title
        head.add_theme_font_size_override("font_size", _k("font_size_section_title"))
        head.add_theme_color_override("font_color", _c("text_primary"))
        header.add_child(head)
        var sub := Label.new()
        sub.text = subtitle
        sub.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        sub.add_theme_color_override("font_color", _c("text_secondary"))
        sub.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        header.add_child(sub)
        return header


func _build_chat_surface() -> Control:
        var surface := VBoxContainer.new()
        surface.add_theme_constant_override("separation", _k("space_m"))
        surface.add_child(_surface_header(
                "Chat",
                "The live circuit: the gateway's chat.send observed to its truthful terminal (wb-7)."
        ))

        var fill := VBoxContainer.new()
        fill.size_flags_vertical = Control.SIZE_EXPAND_FILL
        fill.add_theme_constant_override("separation", 0)

        var empty := CenterContainer.new()
        empty.size_flags_vertical = Control.SIZE_EXPAND_FILL
        empty.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _empty_center = empty
        var empty_col := VBoxContainer.new()
        empty_col.add_theme_constant_override("separation", _k("space_xs"))
        var empty_title := Label.new()
        empty_title.text = "No messages"
        empty_title.add_theme_font_size_override("font_size", _k("font_size_body"))
        empty_title.add_theme_color_override("font_color", _c("text_secondary"))
        empty_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        empty_col.add_child(empty_title)
        _empty_note = Label.new()
        _empty_note.text = "Nothing is fabricated: the backend is not connected."
        _empty_note.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _empty_note.add_theme_color_override("font_color", _c("text_muted"))
        _empty_note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        _empty_note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        empty_col.add_child(_empty_note)
        empty.add_child(empty_col)
        fill.add_child(empty)

        _messages_scroll = ScrollContainer.new()
        _messages_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
        _messages_scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _messages_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
        _messages_scroll.visible = false
        _messages_box = VBoxContainer.new()
        _messages_box.add_theme_constant_override("separation", _k("space_s"))
        _messages_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _messages_scroll.add_child(_messages_box)
        fill.add_child(_messages_scroll)
        surface.add_child(fill)

        var composer := HBoxContainer.new()
        composer.add_theme_constant_override("separation", _k("space_s"))
        _composer_input = LineEdit.new()
        _composer_input.text = "Offline — start Workbench.bat (one double-click), then reopen"
        _composer_input.editable = false
        _composer_input.custom_minimum_size = Vector2(0, 40)
        _composer_input.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        composer.add_child(_composer_input)
        _send_button = Button.new()
        _send_button.text = "Send"
        _send_button.custom_minimum_size = Vector2(96, 40)
        _send_button.disabled = true
        _send_button.pressed.connect(_on_send_pressed)
        composer.add_child(_send_button)
        _stop_button = Button.new()
        _stop_button.text = "Stop"
        _stop_button.custom_minimum_size = Vector2(96, 40)
        _stop_button.disabled = true
        _stop_button.pressed.connect(_on_stop_pressed)
        composer.add_child(_stop_button)
        surface.add_child(composer)
        return surface


func _build_models_surface() -> Control:
        var surface := VBoxContainer.new()
        surface.add_theme_constant_override("separation", _k("space_m"))
        surface.add_child(_surface_header(
                "Models",
                "Discover, fetch, load, switch — the lifecycle states observed, never guessed (wb-8/wb-9)."
        ))

        var toolbar := HBoxContainer.new()
        toolbar.add_theme_constant_override("separation", _k("space_s"))
        _models_refresh_button = Button.new()
        _models_refresh_button.text = "Refresh"
        _models_refresh_button.disabled = true
        _models_refresh_button.pressed.connect(_on_models_refresh_pressed)
        toolbar.add_child(_models_refresh_button)
        _models_active_label = Label.new()
        _models_active_label.text = "active: none observed"
        _models_active_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        _models_active_label.add_theme_color_override("font_color", _c("text_secondary"))
        _models_active_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _models_active_label.clip_text = true
        _models_active_label.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        toolbar.add_child(_models_active_label)
        surface.add_child(toolbar)

        # wb-10 — the model manager, the OWNER'S form: the native picker
        # FIRST (Add local models… / Add folder… — the OS dialogs over
        # model.import), Open models folder on the gateway's own root
        # answer; the URL fetch demotes to the collapsed advanced row
        # (wb-9's download arm, fully functional).
        _import_dialog = _make_import_dialog()
        var add_card := PanelContainer.new()
        var add_col := VBoxContainer.new()
        add_col.add_theme_constant_override("separation", _k("space_s"))
        var add_row := HBoxContainer.new()
        add_row.add_theme_constant_override("separation", _k("space_s"))
        _add_files_button = Button.new()
        _add_files_button.text = "Add local models…"
        _add_files_button.tooltip_text = "Pick GGUF files anywhere on disk — the OS file dialog"
        _add_files_button.disabled = true
        _add_files_button.pressed.connect(_on_add_local_pressed)
        add_row.add_child(_add_files_button)
        _add_folder_button = Button.new()
        _add_folder_button.text = "Add folder…"
        _add_folder_button.tooltip_text = "Pick a folder — every .gguf inside lands as a model"
        _add_folder_button.disabled = true
        _add_folder_button.pressed.connect(_on_add_folder_pressed)
        add_row.add_child(_add_folder_button)
        _open_folder_button = Button.new()
        _open_folder_button.text = "Open models folder"
        _open_folder_button.tooltip_text = "The models directory in the OS file manager"
        _open_folder_button.disabled = true
        _open_folder_button.pressed.connect(_on_open_models_folder_pressed)
        add_row.add_child(_open_folder_button)
        _import_cancel_button = Button.new()
        _import_cancel_button.text = "Cancel"
        _import_cancel_button.tooltip_text = "Cancel the running import (the truthful §12.3 terminal)"
        _import_cancel_button.disabled = true
        _import_cancel_button.pressed.connect(_on_import_cancel_pressed)
        add_row.add_child(_import_cancel_button)
        add_col.add_child(add_row)
        _fetch_status_label = Label.new()
        _fetch_status_label.text = "the manager rides the gateway — start Workbench.bat (double-click) or scripts/workbench_launch.py"
        _fetch_status_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _fetch_status_label.add_theme_color_override("font_color", _c("text_muted"))
        _fetch_status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        _fetch_status_label.clip_text = true
        add_col.add_child(_fetch_status_label)
        _fetch_advanced_button = Button.new()
        _fetch_advanced_button.text = "Download by URL… (advanced)"
        _fetch_advanced_button.toggle_mode = true
        _fetch_advanced_button.pressed.connect(_on_fetch_advanced_toggled)
        add_col.add_child(_fetch_advanced_button)
        _fetch_advanced_box = VBoxContainer.new()
        _fetch_advanced_box.visible = false
        _fetch_advanced_box.add_theme_constant_override("separation", _k("space_xs"))
        var fetch_row := HBoxContainer.new()
        fetch_row.add_theme_constant_override("separation", _k("space_s"))
        _fetch_input = LineEdit.new()
        _fetch_input.placeholder_text = "https://…/model.gguf · hf:repo/file — pull a GGUF from anywhere"
        _fetch_input.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _fetch_input.editable = false
        fetch_row.add_child(_fetch_input)
        _fetch_button = Button.new()
        _fetch_button.text = "Fetch"
        _fetch_button.disabled = true
        _fetch_button.pressed.connect(_on_fetch_pressed)
        fetch_row.add_child(_fetch_button)
        _fetch_cancel_button = Button.new()
        _fetch_cancel_button.text = "Cancel"
        _fetch_cancel_button.disabled = true
        _fetch_cancel_button.pressed.connect(_on_fetch_cancel_pressed)
        fetch_row.add_child(_fetch_cancel_button)
        _fetch_advanced_box.add_child(fetch_row)
        add_col.add_child(_fetch_advanced_box)
        add_card.add_child(add_col)
        surface.add_child(add_card)

        _models_scroll = ScrollContainer.new()
        _models_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
        _models_scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _models_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
        _models_list = VBoxContainer.new()
        _models_list.add_theme_constant_override("separation", _k("space_s"))
        _models_list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _models_scroll.add_child(_models_list)
        _models_scroll.visible = false
        surface.add_child(_models_scroll)

        var empty := CenterContainer.new()
        empty.size_flags_vertical = Control.SIZE_EXPAND_FILL
        empty.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        var empty_col := VBoxContainer.new()
        empty_col.add_theme_constant_override("separation", _k("space_xs"))
        var empty_title := Label.new()
        empty_title.text = "No models discovered"
        empty_title.add_theme_font_size_override("font_size", _k("font_size_body"))
        empty_title.add_theme_color_override("font_color", _c("text_secondary"))
        empty_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        empty_col.add_child(empty_title)
        _models_empty_note = Label.new()
        _models_empty_note.text = "No models yet — click Add local models… and pick GGUF files from your disk (or Add folder…)."
        _models_empty_note.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _models_empty_note.add_theme_color_override("font_color", _c("text_muted"))
        _models_empty_note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        _models_empty_note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        empty_col.add_child(_models_empty_note)
        empty.add_child(empty_col)
        surface.add_child(empty)
        _models_empty_center = empty

        _models_status_label = Label.new()
        _models_status_label.text = "model actions: none yet"
        _models_status_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _models_status_label.add_theme_color_override("font_color", _c("text_muted"))
        _models_status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        surface.add_child(_models_status_label)
        return surface


func _build_settings_surface() -> Control:
        var surface := VBoxContainer.new()
        surface.add_theme_constant_override("separation", _k("space_m"))
        surface.add_child(_surface_header(
                "Settings",
                "Global behaviour and appearance — the effective values, honestly."
        ))
        _settings_scroll = ScrollContainer.new()
        _settings_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
        _settings_scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _settings_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
        var column := VBoxContainer.new()
        column.add_theme_constant_override("separation", _k("space_s"))
        column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _settings_scroll.add_child(column)
        surface.add_child(_settings_scroll)

        column.add_child(_setting_row("Theme", "canon_workbench_theme@0.1 · dark — the only admitted theme"))
        column.add_child(_setting_row("Language", "English · localisation opens on its own wb row"))
        _settings_gateway_value = _setting_value_label(
                "offline — the proof/static form (no gateway dialled)"
        )
        column.add_child(_setting_row_with_value("Gateway", _settings_gateway_value))
        _settings_backend_value = _setting_value_label(
                "none observed yet — llama.cpp rides the gateway (chat.run's backend note)"
        )
        column.add_child(_setting_row_with_value("Backend", _settings_backend_value))
        column.add_child(_launch_settings_section())
        column.add_child(_setting_row("Simulation", "seam proven (wb-1) · the surface opens on its wb row"))
        column.add_child(_setting_row("Keyboard & focus", "tab order + visible focus from the theme tokens"))
        return surface


func _launch_settings_section() -> Control:
        # wb-9 — the REAL llama.cpp launch settings: the typed fields the
        # managed spawn reads (backend.settings over the gateway), the
        # collapsed advanced extras, and the effective command preview.
        var card := PanelContainer.new()
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_s"))
        card.add_child(col)

        var title := Label.new()
        title.text = "llama.cpp launch (managed)"
        title.add_theme_font_size_override("font_size", _k("font_size_section_title"))
        title.add_theme_color_override("font_color", _c("text_primary"))
        col.add_child(title)
        var note := Label.new()
        note.text = "The managed spawn's own flags — saved values apply at the NEXT model.load; a LIVE server keeps its flags until unloaded."
        note.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        note.add_theme_color_override("font_color", _c("text_secondary"))
        note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        col.add_child(note)

        _llama_exe_edit = LineEdit.new()
        _llama_exe_edit.placeholder_text = "auto — workbench/runtime/llama.cpp, then PATH"
        col.add_child(_input_row("llama-server executable", _llama_exe_edit))

        _ctx_spin = _spin_box(512.0, 2097152.0, 512.0, 8192.0)
        col.add_child(_input_row("Context window (-c)", _ctx_spin))
        _ngl_spin = _spin_box(0.0, 999.0, 1.0, 999.0)
        col.add_child(_input_row("GPU layers (-ngl)", _ngl_spin))

        _fa_option = OptionButton.new()
        for form in FA_FORMS:
                _fa_option.add_item(form)
        _fa_option.selected = FA_FORMS.find("on")
        col.add_child(_input_row("Flash attention (-fa)", _fa_option))

        _jinja_check = CheckBox.new()
        _jinja_check.button_pressed = true
        col.add_child(_input_row("Chat template (--jinja)", _jinja_check))
        _no_webui_check = CheckBox.new()
        _no_webui_check.button_pressed = true
        col.add_child(_input_row("No web UI (--no-webui)", _no_webui_check))

        col.add_child(_caption("SAMPLER DEFAULTS"))
        _temp_spin = _spin_box(0.0, 2.0, 0.05, 0.8)
        col.add_child(_input_row("Temperature (--temp)", _temp_spin))
        _topk_spin = _spin_box(0.0, 10000.0, 1.0, 40.0)
        col.add_child(_input_row("Top-K (--top-k)", _topk_spin))
        _topp_spin = _spin_box(0.0, 1.0, 0.01, 0.95)
        col.add_child(_input_row("Top-P (--top-p)", _topp_spin))
        _minp_spin = _spin_box(0.0, 1.0, 0.01, 0.05)
        col.add_child(_input_row("Min-P (--min-p)", _minp_spin))
        _repeat_spin = _spin_box(0.0, 4.0, 0.05, 1.1)
        col.add_child(_input_row("Repeat penalty (--repeat-penalty)", _repeat_spin))

        _advanced_button = Button.new()
        _advanced_button.text = "Advanced — extra flags and the command preview"
        _advanced_button.toggle_mode = true
        _advanced_button.pressed.connect(_on_advanced_toggled)
        col.add_child(_advanced_button)
        _advanced_box = VBoxContainer.new()
        _advanced_box.visible = false
        _advanced_box.add_theme_constant_override("separation", _k("space_xs"))
        _extra_edit = LineEdit.new()
        _extra_edit.placeholder_text = "--threads 8 --mlock — extra llama-server flags, verbatim"
        _advanced_box.add_child(_input_row("Extra flags", _extra_edit))
        _preview_label = Label.new()
        _preview_label.text = "the command the NEXT managed spawn would run — arrives with the gateway's settings document"
        _preview_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _preview_label.add_theme_color_override("font_color", _c("text_muted"))
        _preview_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        _advanced_box.add_child(_preview_label)
        col.add_child(_advanced_box)

        _settings_status_label = Label.new()
        _settings_status_label.text = "the settings ride the gateway — start scripts/workbench_launch.py"
        _settings_status_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _settings_status_label.add_theme_color_override("font_color", _c("text_muted"))
        _settings_status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        col.add_child(_settings_status_label)

        _settings_save_button = Button.new()
        _settings_save_button.text = "Save launch settings"
        _settings_save_button.disabled = true
        _settings_save_button.pressed.connect(_on_settings_save_pressed)
        col.add_child(_settings_save_button)
        return card


func _input_row(key: String, field: Control) -> Control:
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_m"))
        var key_label := Label.new()
        key_label.text = key
        key_label.add_theme_font_size_override("font_size", _k("font_size_body"))
        key_label.add_theme_color_override("font_color", _c("text_primary"))
        row.add_child(key_label)
        field.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        row.add_child(field)
        return row


func _spin_box(min_value: float, max_value: float, step: float, value: float) -> SpinBox:
        var spin := SpinBox.new()
        spin.min_value = min_value
        spin.max_value = max_value
        spin.step = step
        spin.value = value
        spin.alignment = HORIZONTAL_ALIGNMENT_RIGHT
        return spin


func _setting_row(key: String, value: String) -> Control:
        return _setting_row_with_value(key, _setting_value_label(value))


func _setting_row_with_value(key: String, value_label: Label) -> Control:
        var card := PanelContainer.new()
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_m"))
        var key_label := Label.new()
        key_label.text = key
        key_label.add_theme_font_size_override("font_size", _k("font_size_body"))
        key_label.add_theme_color_override("font_color", _c("text_primary"))
        row.add_child(key_label)
        value_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
        value_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        value_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        row.add_child(value_label)
        card.add_child(row)
        return card


func _setting_value_label(value: String) -> Label:
        var label := Label.new()
        label.text = value
        label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        label.add_theme_color_override("font_color", _c("text_secondary"))
        return label


func _build_status_bar() -> Control:
        var bar := PanelContainer.new()
        bar.add_theme_stylebox_override("panel", _s("bar"))
        var row := HBoxContainer.new()
        row.custom_minimum_size = Vector2(0, _k("status_bar_height"))
        row.add_theme_constant_override("separation", _k("space_l"))
        bar.add_child(row)

        var legend := Label.new()
        legend.text = "Statuses CANONICAL · OBSERVED · DERIVED · UNKNOWN · HIDDEN · VISUAL are displayed, never collapsed"
        legend.add_theme_font_size_override("font_size", _k("font_size_caption"))
        legend.add_theme_color_override("font_color", _c("text_secondary"))
        legend.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        legend.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        legend.clip_text = true
        row.add_child(legend)

        _gateway_state_label = Label.new()
        _gateway_state_label.text = "gateway OFFLINE"
        _gateway_state_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _gateway_state_label.add_theme_color_override("font_color", _c("text_muted"))
        _gateway_state_label.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        row.add_child(_gateway_state_label)

        var seam := Label.new()
        seam.text = "seam wb-1 · PROVEN"
        seam.add_theme_font_size_override("font_size", _k("font_size_caption"))
        seam.add_theme_color_override("font_color", _c("status_success"))
        seam.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        row.add_child(seam)

        var engine := Label.new()
        engine.text = "Redot 26.2 LTS"
        engine.add_theme_font_size_override("font_size", _k("font_size_caption"))
        engine.add_theme_color_override("font_color", _c("text_muted"))
        engine.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        row.add_child(engine)
        return bar


# --- surface switching -------------------------------------------------------


func _on_surface_selected(key: String) -> void:
        _show_surface(key)


func _show_surface(key: String) -> void:
        _active_surface = key
        for surface_key in SURFACES:
                _surface_nodes[surface_key].visible = surface_key == key
        if key == "models" and _client != null and not _models_requested:
                _refresh_models()
        # The active axis owns the pressed state (the button group keeps the
        # exclusivity) and the keyboard focus (§13: visible focus, logical order).
        if _nav_buttons.has(key):
                _nav_buttons[key].button_pressed = true
                _nav_buttons[key].grab_focus()


# --- the live circuit (wb-7 — no network in the proof/static form) -----------


func _resolve_gateway_url(args: PackedStringArray) -> String:
        # The resolution order: the --gateway-url user arg, then the
        # CANONSIM_GATEWAY_URL env var, then the committed project setting
        # (canonism_workbench/gateway/url), then the default.
        var i := 0
        while i < args.size() - 1:
                if args[i] == "--gateway-url":
                        return args[i + 1]
                i += 1
        var from_env := OS.get_environment("CANONSIM_GATEWAY_URL")
        if from_env != "":
                return from_env
        return String(
                ProjectSettings.get_setting(GATEWAY_URL_SETTING, GATEWAY_DEFAULT_URL)
        )


func _start_live_circuit(args: PackedStringArray) -> void:
        _gateway_url = _resolve_gateway_url(args)
        _settings_gateway_value.text = "offline — probing %s" % _gateway_url
        _client = GATEWAY_CLIENT_SCRIPT.new()
        _client.configure(_gateway_url)
        _client.operation_answered.connect(_on_operation_answered)
        _client.transport_failed.connect(_on_transport_failed)
        add_child(_client)

        _poll_timer = Timer.new()
        _poll_timer.wait_time = POLL_INTERVAL_S
        _poll_timer.autostart = false
        _poll_timer.timeout.connect(_on_poll_tick)
        add_child(_poll_timer)

        # The §18 law: the effective state is never hidden — the probe is
        # evidence; the badge only upgrades on a LIVE observation.
        _client.call_operation("app-status", "app.status", {})
        _composer_input.text_submitted.connect(_on_composer_submitted)
        _models_refresh_button.disabled = false
        if _active_surface == "models":
                _refresh_models()


func _next_request_id(prefix: String) -> String:
        _request_counter += 1
        return "%s-%d" % [prefix, _request_counter]


func _on_operation_answered(tag: String, document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if tag == "app-status":
                if status == "OK":
                        _set_badge("CANONSIM · GATEWAY LIVE", true)
                        _gateway_state_label.text = "gateway LIVE · %s" % _gateway_url
                        _gateway_state_label.add_theme_color_override(
                                "font_color", _c("status_success")
                        )
                        _settings_gateway_value.text = "LIVE · %s" % _gateway_url
                        _client.call_operation(
                                "session-create", "session.create", {},
                                "", "wb-shell-session-%d" % OS.get_process_id()
                        )
                else:
                        _note_system(
                                "app.status refused: %s %s" % [
                                        _text(document.get("rejection")),
                                        _reason_of(document),
                                ]
                        )
                return
        if tag == "session-create":
                if status == "OK" and document.get("result") is Dictionary:
                        var result: Dictionary = document.get("result")
                        _session_id = _text(result.get("session_id"))
                        _session_live = _session_id != ""
                        if _session_live:
                                _set_badge("CANONSIM · SESSION LIVE", true)
                                _empty_note.text = "Session live over the gateway — nothing fabricated, ever."
                                _composer_input.text = ""
                                _composer_input.placeholder_text = "Message… (Enter to send)"
                                _composer_input.editable = true
                                _send_button.disabled = false
                                _update_models_enablement()
                                _fetch_input.editable = true
                                _fetch_button.disabled = false
                                _add_files_button.disabled = false
                                _add_folder_button.disabled = false
                                _settings_save_button.disabled = false
                                _request_backend_settings()
                else:
                        _note_system(
                                "session.create refused: %s %s" % [
                                        _text(document.get("rejection")),
                                        _reason_of(document),
                                ]
                        )
                return
        if tag == "model-list":
                _on_model_list_answered(document)
                return
        if tag == "model-states":
                _on_model_states_answered(document)
                return
        if tag == "backend-settings":
                _on_backend_settings_answered(document)
                return
        if tag.begins_with("settings-save-"):
                _on_settings_saved_answered(document)
                return
        if tag.begins_with("fetch-start-"):
                _on_fetch_start_answered(document)
                return
        if tag.begins_with("fetch-get-"):
                _on_fetch_get_answered(document)
                return
        if tag.begins_with("fetch-cancel-"):
                if status != "OK":
                        _fetch_status_label.text = "run.cancel refused: %s %s" % [
                                _text(document.get("rejection")), _reason_of(document)
                        ]
                return
        if tag.begins_with("import-start-"):
                _on_import_start_answered(document)
                return
        if tag.begins_with("import-get-"):
                _on_import_get_answered(document)
                return
        if tag.begins_with("import-cancel-"):
                if status != "OK":
                        _fetch_status_label.text = "run.cancel refused: %s %s" % [
                                _text(document.get("rejection")), _reason_of(document)
                        ]
                return
        # wb-11: the load/unload POLL arms first (the longer prefixes own
        # the match — "model-load-get-N" also begins with "model-load-").
        if tag.begins_with("model-load-get-"):
                _on_model_load_get_answered(document)
                return
        if tag.begins_with("model-unload-get-"):
                _on_model_unload_get_answered(document)
                return
        if tag.begins_with("model-load-"):
                _on_model_load_answered(tag.substr(len("model-load-")), document)
                return
        if tag.begins_with("model-unload-"):
                _on_model_unload_answered(tag.substr(len("model-unload-")), document)
                return
        if tag.begins_with("chat-send-"):
                _on_chat_send_answered(tag, document)
                return
        if tag.begins_with("run-get-"):
                _on_run_get_answered(document)
                return
        if tag.begins_with("run-cancel-"):
                # §12.3's truthful cancellation: the request's outcome is its own
                # observation; the run's terminal state lands via the poll.
                if status != "OK":
                        _note_system(
                                "run.cancel refused: %s %s" % [
                                        _text(document.get("rejection")),
                                        _reason_of(document),
                                ]
                        )
                return
        _note_system("unexpected answer for %s (status %s)" % [tag, status])


func _on_chat_send_answered(_tag: String, document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                var result: Dictionary = document.get("result")
                _active_execution = _text(result.get("execution_id"))
                _poll_failures = 0
                _poll_timer.start()
                _set_busy(true)
                _note_system(
                        "chat dispatched (run %s · polling run.get)" % _short(_active_execution)
                )
                return
        if status == "UNKNOWN":
                _note_system(
                        "chat dispatch OUTCOME UNKNOWN (%s) — not blindly retried" % _reason_of(document)
                )
                _set_busy(false)
                return
        _note_system(
                "chat.send refused: %s %s" % [
                        _text(document.get("rejection")),
                        _reason_of(document),
                ]
        )
        _set_busy(false)


func _on_run_get_answered(document: Dictionary) -> void:
        if _active_execution == "":
                return
        var status := _text(document.get("status"))
        if status != "OK":
                # A semantic rejection is terminal for THIS poll loop (a transient
                # transport failure is the _poll_failures arm's own law) — noted
                # once, never spammed.
                _active_execution = ""
                _set_busy(false)
                _maybe_stop_poll_timer()
                _note_system(
                        "run.get refused: %s %s" % [
                                _text(document.get("rejection")),
                                _reason_of(document),
                        ]
                )
                return
        if not (document.get("result") is Dictionary):
                return
        var result: Dictionary = document.get("result")
        if not bool(result.get("terminal", false)):
                return  # still walking (STARTING/RUNNING) — the next tick observes
        _active_execution = ""
        _set_busy(false)
        _maybe_stop_poll_timer()
        var state := _text(result.get("state"))
        var run_result: Dictionary = (
                result.get("result") if result.get("result") is Dictionary else {}
        )
        match state:
                "COMPLETED":
                        _append_message("assistant", _text(run_result.get("content")))
                        var backend: Dictionary = (
                                run_result.get("backend", {}) if run_result.get("backend") is Dictionary else {}
                        )
                        _note_system(
                                "finish %s · backend %s" % [
                                        _text(run_result.get("finish_reason")),
                                        _backend_note(backend),
                                ]
                        )
                        _observe_backend(backend)
                "FAILED":
                        _note_system(
                                "run FAILED · %s" % _text(result.get("failure_type"))
                        )
                "CANCELED":
                        _note_system("run canceled (the truthful terminal)")
                "FAILED_TO_CANCEL":
                        # §12.3: the late result was recorded; the truth is the
                        # failed cancel. Both are shown, never merged.
                        _note_system(
                                "cancel failed — the late result was recorded and shown"
                        )
                        _append_message("assistant", _text(run_result.get("content")))
                "UNKNOWN":
                        _note_system("run OUTCOME UNKNOWN — the observation stands, no blind retry")
                _:
                        _note_system("run terminal state %s (unmodelled — shown, never collapsed)" % state)


func _backend_note(backend: Dictionary) -> String:
        if backend.is_empty():
                return "unavailable (no backend identity in the run result)"
        if _text(backend.get("probe")) == "unavailable":
                return "probe unavailable — the identity not observed (honest note)"
        var model := _text(backend.get("model"))
        var build := _text(backend.get("build"))
        if model == "":
                model = "unknown model"
        if build == "":
                build = "unknown build"
        return "%s · %s" % [model, build]


func _observe_backend(backend: Dictionary) -> void:
        if backend.is_empty():
                _settings_backend_value.text = (
                        "no backend identity in the run result (shown, never guessed)"
                )
        elif _text(backend.get("probe")) == "unavailable":
                _settings_backend_value.text = (
                        "llama.cpp chat OBSERVED · identity probe unavailable (honest)"
                )
        else:
                _settings_backend_value.text = "OBSERVED · %s" % _backend_note(backend)


func _on_poll_tick() -> void:
        if _session_id == "":
                _poll_timer.stop()
                return
        var any_active := false
        if _active_execution != "":
                _client.call_operation(
                        _next_request_id("run-get"), "run.get",
                        {"execution_id": _active_execution}, _session_id
                )
                any_active = true
        if _fetch_execution != "":
                _client.call_operation(
                        _next_request_id("fetch-get"), "run.get",
                        {"execution_id": _fetch_execution}, _session_id
                )
                any_active = true
        if _import_execution != "":
                _client.call_operation(
                        _next_request_id("import-get"), "run.get",
                        {"execution_id": _import_execution}, _session_id
                )
                any_active = true
        if _load_execution != "":
                _client.call_operation(
                        _next_request_id("model-load-get"), "run.get",
                        {"execution_id": _load_execution}, _session_id
                )
                any_active = true
        if _unload_execution != "":
                _client.call_operation(
                        _next_request_id("model-unload-get"), "run.get",
                        {"execution_id": _unload_execution}, _session_id
                )
                any_active = true
        if not any_active:
                _poll_timer.stop()


func _on_transport_failed(tag: String, error: String) -> void:
        if tag == "app-status" or tag == "session-create":
                _set_badge("CANONSIM · NOT CONNECTED", false)
                _gateway_state_label.text = "gateway unreachable (%s)" % error
                _empty_note.text = "Gateway unreachable — start Workbench.bat (one double-click) or scripts/workbench_launch.py (%s)." % error
                _settings_gateway_value.text = "unreachable · %s" % _gateway_url
                return
        if tag == "model-list" or tag == "model-states":
                # wb-11: a failed scan re-arms (the next surface entry
                # retries — the empty list never sticks silently, the
                # owner's «моделей не видно» persistence call).
                _models_requested = false
                _models_status_label.text = (
                        "gateway unreachable on %s (%s) — Retry with Refresh" % [tag, error]
                )
                return
        if tag == "backend-settings":
                _settings_status_label.text = "backend.settings unreachable (%s) — the values stay local until the gateway answers" % error
                return
        if tag.begins_with("settings-save-"):
                _settings_status_label.text = "settings save transport failure (%s) — nothing sent, safe to retry" % error
                return
        if tag.begins_with("fetch-start-"):
                _reset_fetch_controls()
                _fetch_status_label.text = "fetch dispatch transport failure (%s) — nothing sent, safe to retry" % error
                return
        if tag.begins_with("import-start-"):
                _reset_import_controls()
                _fetch_status_label.text = "import dispatch transport failure (%s) — nothing sent, safe to retry" % error
                return
        if tag.begins_with("import-get-"):
                _import_poll_failures += 1
                if _import_poll_failures >= MAX_POLL_FAILURES:
                        _import_execution = ""
                        _reset_import_controls()
                        _fetch_status_label.text = "import poll abandoned after %d transport failures (%s)" % [MAX_POLL_FAILURES, error]
                        _maybe_stop_poll_timer()
                return
        if tag.begins_with("import-cancel-"):
                _fetch_status_label.text = "run.cancel transport failure (%s) — the poll continues" % error
                return
        if tag.begins_with("fetch-get-"):
                _fetch_poll_failures += 1
                if _fetch_poll_failures >= MAX_POLL_FAILURES:
                        _fetch_execution = ""
                        _reset_fetch_controls()
                        _fetch_status_label.text = "fetch poll abandoned after %d transport failures (%s)" % [MAX_POLL_FAILURES, error]
                        _maybe_stop_poll_timer()
                return
        if tag.begins_with("fetch-cancel-"):
                _fetch_status_label.text = "run.cancel transport failure (%s) — the poll continues" % error
                return
        # wb-11: the POLL arms first — "model-load-get-N" also begins with
        # "model-load-", the longer prefix owns the match.
        if tag.begins_with("model-load-get-"):
                # The load run's poll transport failures — bounded
                # abandon, the same law as the chat/fetch/import polls.
                _load_poll_failures += 1
                if _load_poll_failures >= MAX_POLL_FAILURES:
                        _load_execution = ""
                        _models_status_label.text = "load poll abandoned after %d transport failures (%s) — the row rests at its observed truth" % [MAX_POLL_FAILURES, error]
                        _maybe_stop_poll_timer()
                return
        if tag.begins_with("model-unload-get-"):
                _unload_poll_failures += 1
                if _unload_poll_failures >= MAX_POLL_FAILURES:
                        _unload_execution = ""
                        _models_status_label.text = "unload poll abandoned after %d transport failures (%s) — the row rests at its observed truth" % [MAX_POLL_FAILURES, error]
                        _maybe_stop_poll_timer()
                return
        if tag.begins_with("model-load-") or tag.begins_with("model-unload-"):
                # The action never reached the gateway — the row's truth is
                # unchanged (SELECTED/ACTIVE), the button returns honestly.
                _models_status_label.text = "%s transport failure (%s) — the state is NOT changed, the action may be re-issued" % [tag, error]
                _client.call_operation("model-states", "model.states", {})
                return
        if tag.begins_with("run-get-"):
                _poll_failures += 1
                if _poll_failures >= MAX_POLL_FAILURES:
                        _active_execution = ""
                        _set_busy(false)
                        _maybe_stop_poll_timer()
                        _note_system(
                                "poll abandoned after %d transport failures (%s)" % [
                                        MAX_POLL_FAILURES, error
                                ]
                        )
                return
        if tag.begins_with("run-cancel-"):
                # The cancel request itself failed to send — the run is still
                # in flight, the poll continues, Stop stays the honest action.
                _note_system("run.cancel transport failure (%s) — the poll continues" % error)
                return
        _note_system("transport failure on %s (%s)" % [tag, error])
        _set_busy(false)


# --- the models surface (wb-8 — discovery, load, unload, the truth) ----------


func _on_models_refresh_pressed() -> void:
        _refresh_models()


func _refresh_models() -> void:
        # The honest discovery re-scan (§20): model.list + the lifecycle
        # read (model.states) — both READs, no session needed, no fake.
        if _client == null:
                return
        _models_requested = true
        _models_status_label.text = "scanning the models directory…"
        _client.call_operation("model-list", "model.list", {})
        _client.call_operation("model-states", "model.states", {})


func _on_model_list_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status != "OK" or not (document.get("result") is Dictionary):
                _models_status_label.text = "model.list refused: %s %s" % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                return
        var result: Dictionary = document.get("result")
        var directory_state := _text(result.get("directory_state"))
        if directory_state == "MISSING":
                _models_empty_note.text = "The models directory is MISSING — the launcher's runtime/models folder is the default home; fetch or drop GGUF files there."
        var models: Array = result.get("models", []) if result.get("models") is Array else []
        _models_root = _text(result.get("models_root"))
        if _models_root != "":
                _open_folder_button.disabled = false
        _rebuild_models_list(models)
        if models.is_empty():
                _models_status_label.text = "no models discovered (%s) — Add local models… above, or drop GGUF files into %s" % [directory_state, _models_root]
        else:
                _models_status_label.text = "%d model(s) discovered · %s" % [
                        models.size(), directory_state
                ]
        # (the states read is already in flight from _refresh_models —
        # the sequential queue keeps the pair honest, no duplicate)


func _on_model_states_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status != "OK" or not (document.get("result") is Dictionary):
                _models_status_label.text = "model.states refused: %s %s" % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                return
        var result: Dictionary = document.get("result")
        var states: Dictionary = (
                result.get("states", {}) if result.get("states") is Dictionary else {}
        )
        var active := _text(result.get("active"))
        _apply_model_states(states, active)


func _rebuild_models_list(models: Array) -> void:
        for child in _models_list.get_children():
                child.queue_free()
        _model_rows = {}
        for entry in models:
                if not (entry is Dictionary):
                        continue
                var logical_name := _text(entry.get("logical_name"))
                if logical_name == "":
                        continue
                var size_bytes := int(entry.get("size_bytes", 0))
                var row := _model_row_card(logical_name, size_bytes)
                _models_list.add_child(row)
        if _model_rows.is_empty():
                _models_scroll.visible = false
                _models_empty_center.visible = true
        else:
                _models_empty_center.visible = false
                _models_scroll.visible = true
        _update_models_enablement()


func _model_row_card(logical_name: String, size_bytes: int) -> Control:
        var card := PanelContainer.new()
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_m"))
        card.add_child(row)

        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_xs"))
        col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        var name_label := Label.new()
        name_label.text = logical_name
        name_label.add_theme_font_size_override("font_size", _k("font_size_body"))
        name_label.add_theme_color_override("font_color", _c("text_primary"))
        name_label.clip_text = true
        name_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        col.add_child(name_label)
        var size_label := Label.new()
        size_label.text = _format_size(size_bytes)
        size_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        size_label.add_theme_color_override("font_color", _c("text_muted"))
        col.add_child(size_label)
        row.add_child(col)

        var state_row := HBoxContainer.new()
        state_row.add_theme_constant_override("separation", _k("space_s"))
        state_row.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        var state_dot := ColorRect.new()
        state_dot.color = _c("text_muted")
        state_dot.custom_minimum_size = Vector2(8, 8)
        state_dot.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        state_row.add_child(state_dot)
        var state_label := Label.new()
        state_label.text = "DISCOVERED"
        state_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        state_label.add_theme_color_override("font_color", _c("text_secondary"))
        state_row.add_child(state_label)
        row.add_child(state_row)

        var action := Button.new()
        action.text = "Load"
        action.custom_minimum_size = Vector2(96, 0)
        action.disabled = true  # until the session + the states arrive
        row.add_child(action)
        _model_rows[logical_name] = {
                "card": card, "state": state_label, "action": action,
                "size": size_label, "dot": state_dot,
        }
        _rebind_action(logical_name, "_on_model_load_pressed")
        return card


func _apply_model_states(states: Dictionary, active: String) -> void:
        for logical_name in _model_rows:
                var row: Dictionary = _model_rows[logical_name]
                var observed := _text(states.get(logical_name, "DISCOVERED"))
                _set_model_row_state(logical_name, observed)
        if active != "":
                _models_active_label.text = "active: %s" % active
        else:
                _models_active_label.text = "active: none observed"
        _update_models_enablement()


func _set_model_row_state(logical_name: String, state: String) -> void:
        if not _model_rows.has(logical_name):
                return
        var row: Dictionary = _model_rows[logical_name]
        var state_label: Label = row["state"]
        state_label.text = state
        var colour := _c("text_secondary")
        match state:
                "ACTIVE":
                        colour = _c("status_success")
                "FAILED":
                        colour = _c("status_warning")
                "SELECTED":
                        colour = _c("status_warning")
        state_label.add_theme_color_override("font_color", colour)
        var state_dot: ColorRect = row["dot"]
        state_dot.color = colour
        row["observed_state"] = state


func _on_model_load_pressed(logical_name: String) -> void:
        if not _session_live or _client == null:
                # wb-11: never a silent return — §18's law (the effective
                # state is named, the owner is never left guessing).
                _models_status_label.text = "the load action needs a live gateway session — the badge (top right) names the state; start Workbench.bat"
                return
        var row: Dictionary = _model_rows.get(logical_name, {})
        if row.is_empty():
                return
        var action: Button = row["action"]
        action.disabled = true
        action.text = "LOADING…"
        _set_model_row_state(logical_name, "LOADING")
        _models_status_label.text = "loading %s — dispatched as a run (the spawn/readiness walk rides the poll; the app stays live)" % logical_name
        # The dispatch tag carries the logical_name verbatim (the answer's
        # routing key); the idempotency key stays unique per action (G4).
        var tag := "model-load-%s" % logical_name
        var request_id := _next_request_id(tag)
        _client.call_operation(
                tag, "model.load", {"logical_name": logical_name},
                _session_id, request_id
        )


func _on_model_unload_pressed(logical_name: String) -> void:
        if not _session_live or _client == null:
                _models_status_label.text = "the unload action needs a live gateway session — the badge (top right) names the state; start Workbench.bat"
                return
        var row: Dictionary = _model_rows.get(logical_name, {})
        if row.is_empty():
                return
        var action: Button = row["action"]
        action.disabled = true
        action.text = "UNLOADING…"
        _set_model_row_state(logical_name, "UNLOADING")
        _models_status_label.text = "unloading %s — dispatched as a run (the graceful stop rides the poll)" % logical_name
        var tag := "model-unload-%s" % logical_name
        var request_id := _next_request_id(tag)
        _client.call_operation(
                tag, "model.unload", {"logical_name": logical_name},
                _session_id, request_id
        )


func _on_model_load_answered(logical_name: String, document: Dictionary) -> void:
        # wb-11: the DISPATCH answer — the fast admit (identity-then-
        # poll; the minutes-class walk is the run's own, observed below).
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                var result: Dictionary = document.get("result")
                _load_execution = _text(result.get("execution_id"))
                _load_model = logical_name
                _load_poll_failures = 0
                _poll_timer.start()
                return
        if status == "UNKNOWN":
                # §12.1: the dispatch outcome is UNKNOWN (never blindly
                # retried) — the row rests at its observed truth.
                _models_status_label.text = "model.load dispatch OUTCOME UNKNOWN (%s) — the state is NOT changed; Load may be re-issued deliberately" % _reason_of(document)
        else:
                _models_status_label.text = "model.load refused: %s %s" % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
        _client.call_operation("model-states", "model.states", {})
        _update_models_enablement()


func _on_model_unload_answered(logical_name: String, document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                var result: Dictionary = document.get("result")
                _unload_execution = _text(result.get("execution_id"))
                _unload_model = logical_name
                _unload_poll_failures = 0
                _poll_timer.start()
                return
        if status == "UNKNOWN":
                _models_status_label.text = "model.unload dispatch OUTCOME UNKNOWN (%s) — the state is NOT changed; Unload may be re-issued deliberately" % _reason_of(document)
        else:
                _models_status_label.text = "model.unload refused: %s %s" % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
        _client.call_operation("model-states", "model.states", {})
        _update_models_enablement()


func _on_model_load_get_answered(document: Dictionary) -> void:
        # wb-11: the load run's run.get poll — the terminal answer names
        # the row's resting truth AND the observed cause (§21: the FAILED
        # diagnostics carry the reason — never an error_type-only note).
        if _load_execution == "":
                return
        var status := _text(document.get("status"))
        if status != "OK":
                _load_execution = ""
                _maybe_stop_poll_timer()
                _models_status_label.text = "run.get refused: %s %s" % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                _client.call_operation("model-states", "model.states", {})
                _update_models_enablement()
                return
        if not (document.get("result") is Dictionary):
                return
        var result: Dictionary = document.get("result")
        if not bool(result.get("terminal", false)):
                _models_status_label.text = "loading %s — the run is %s (the managed spawn is minutes-class, observed live)" % [
                        _load_model, _text(result.get("state"))
                ]
                return
        _load_execution = ""
        var logical_name := _load_model
        _load_model = ""
        var run_state := _text(result.get("state"))
        match run_state:
                "COMPLETED":
                        _set_model_row_state(logical_name, "ACTIVE")
                        _models_active_label.text = "active: %s" % logical_name
                        _models_status_label.text = "%s ACTIVE — the chat surface is ready" % logical_name
                "FAILED":
                        var note := _text(result.get("failure_type"))
                        var cause := _first_diagnostic(result)
                        if cause.length() > MODEL_LOAD_NOTE_MAX_LENGTH:
                                cause = cause.substr(0, MODEL_LOAD_NOTE_MAX_LENGTH) + "…"
                        _models_status_label.text = "load FAILED · %s — %s" % [note, cause]
                "CANCELED":
                        _models_status_label.text = "load canceled (the truthful terminal)"
                _:
                        _models_status_label.text = "load terminal state %s (unmodelled — shown, never collapsed)" % run_state
        _maybe_stop_poll_timer()
        _client.call_operation("model-states", "model.states", {})
        _update_models_enablement()


func _on_model_unload_get_answered(document: Dictionary) -> void:
        # wb-11: the unload run's poll — the graceful stop's terminal.
        if _unload_execution == "":
                return
        var status := _text(document.get("status"))
        if status != "OK":
                _unload_execution = ""
                _maybe_stop_poll_timer()
                _models_status_label.text = "run.get refused: %s %s" % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                _client.call_operation("model-states", "model.states", {})
                _update_models_enablement()
                return
        if not (document.get("result") is Dictionary):
                return
        var result: Dictionary = document.get("result")
        if not bool(result.get("terminal", false)):
                _models_status_label.text = "unloading %s — the run is %s" % [
                        _unload_model, _text(result.get("state"))
                ]
                return
        _unload_execution = ""
        var logical_name := _unload_model
        _unload_model = ""
        var run_state := _text(result.get("state"))
        match run_state:
                "COMPLETED":
                        _models_status_label.text = "%s EVICTED — Load again to re-select" % logical_name
                "FAILED":
                        var cause := _first_diagnostic(result)
                        if cause.length() > MODEL_LOAD_NOTE_MAX_LENGTH:
                                cause = cause.substr(0, MODEL_LOAD_NOTE_MAX_LENGTH) + "…"
                        _models_status_label.text = "unload FAILED · %s — %s (the observed truth stays ACTIVE)" % [
                                _text(result.get("failure_type")), cause
                        ]
                "CANCELED":
                        _models_status_label.text = "unload canceled (the truthful terminal)"
                _:
                        _models_status_label.text = "unload terminal state %s (unmodelled — shown, never collapsed)" % run_state
        _maybe_stop_poll_timer()
        _client.call_operation("model-states", "model.states", {})
        _update_models_enablement()


func _update_models_enablement() -> void:
        # The honest enablement law: the mutations are session-scoped (§8);
        # ACTIVE rows offer Unload; loadable resting states offer Load;
        # FAILED stays terminal (D-203's ladder gap — shown, never hidden).
        for logical_name in _model_rows:
                var row: Dictionary = _model_rows[logical_name]
                var action: Button = row["action"]
                var state := String(row.get("observed_state", "DISCOVERED"))
                if state == "LOADING" or state == "UNLOADING":
                        continue  # the in-flight action owns the button
                if state == "ACTIVE":
                        action.text = "Unload"
                        action.disabled = not _session_live
                        _rebind_action(logical_name, "_on_model_unload_pressed")
                else:
                        action.text = "Load"
                        var loadable := state in MODEL_ACTION_STATES
                        action.disabled = not _session_live or not loadable
                        _rebind_action(logical_name, "_on_model_load_pressed")


func _rebind_action(logical_name: String, handler_name: String) -> void:
        # One pressed connection at a time — the row's single action button
        # re-targets between Load and Unload as the observed state flips.
        var row: Dictionary = _model_rows[logical_name]
        var action: Button = row["action"]
        var desired := Callable(self, handler_name).bind(logical_name)
        if String(row.get("bound_handler", "")) == handler_name:
                return
        if row.has("bound_handler"):
                var previous: Callable = row["bound_callable"]
                if action.pressed.is_connected(previous):
                        action.pressed.disconnect(previous)
        row["bound_handler"] = handler_name
        row["bound_callable"] = desired
        action.pressed.connect(desired)


func _format_size(size_bytes: int) -> String:
        if size_bytes >= 1024 * 1024 * 1024:
                return "%.1f GB" % (float(size_bytes) / (1024.0 * 1024.0 * 1024.0))
        if size_bytes >= 1024 * 1024:
                return "%.1f MB" % (float(size_bytes) / (1024.0 * 1024.0))
        return "%d B" % size_bytes


# --- the launch-settings surface (wb-9 — the real llama.cpp fields) ----------


func _request_backend_settings() -> void:
        if _client == null:
                return
        _client.call_operation("backend-settings", "backend.settings", {})


func _on_backend_settings_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status != "OK" or not (document.get("result") is Dictionary):
                _settings_status_label.text = "backend.settings refused: %s %s" % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                return
        _populate_settings_fields(document.get("result"))


func _populate_settings_fields(result: Dictionary) -> void:
        var settings: Dictionary = (
                result.get("settings", {}) if result.get("settings") is Dictionary else {}
        )
        if settings.is_empty():
                return
        _llama_exe_edit.text = _text(settings.get("llama_server_exe"))
        _ctx_spin.value = float(settings.get("context", 8192))
        _ngl_spin.value = float(settings.get("gpu_layers", 999))
        var fa_index := FA_FORMS.find(_text(settings.get("flash_attention")))
        _fa_option.selected = fa_index if fa_index >= 0 else 0
        _jinja_check.button_pressed = bool(settings.get("jinja", true))
        _no_webui_check.button_pressed = bool(settings.get("no_webui", true))
        _temp_spin.value = float(settings.get("temperature", 0.8))
        _topk_spin.value = float(settings.get("top_k", 40))
        _topp_spin.value = float(settings.get("top_p", 0.95))
        _minp_spin.value = float(settings.get("min_p", 0.05))
        _repeat_spin.value = float(settings.get("repeat_penalty", 1.1))
        _extra_edit.text = _text(settings.get("extra_args"))
        var preview := _text(result.get("command_preview"))
        if preview != "":
                _preview_label.text = preview
        var suffix := " — effective at the next model.load"
        if bool(result.get("managed_live")):
                suffix = " — a LIVE server keeps its flags until unloaded"
        _settings_status_label.text = "effective values shown%s" % suffix


func _on_settings_save_pressed() -> void:
        if not _session_live or _client == null:
                return
        var document := {
                "llama_server_exe": _llama_exe_edit.text.strip_edges(),
                "context": int(_ctx_spin.value),
                "gpu_layers": int(_ngl_spin.value),
                "flash_attention": FA_FORMS[_fa_option.selected],
                "jinja": _jinja_check.button_pressed,
                "no_webui": _no_webui_check.button_pressed,
                "temperature": float(_temp_spin.value),
                "top_k": int(_topk_spin.value),
                "top_p": float(_topp_spin.value),
                "min_p": float(_minp_spin.value),
                "repeat_penalty": float(_repeat_spin.value),
                "extra_args": _extra_edit.text.strip_edges(),
        }
        _settings_status_label.text = "saving…"
        var request_id := _next_request_id("settings-save")
        _client.call_operation(
                request_id, "backend.settings.update", document,
                _session_id, request_id
        )


func _on_settings_saved_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                _populate_settings_fields(document.get("result"))
                _settings_status_label.text = "saved — the values apply at the next model.load (a LIVE server keeps its flags until unloaded)"
                return
        if status == "UNKNOWN":
                _settings_status_label.text = "settings save OUTCOME UNKNOWN (%s) — not blindly retried" % _reason_of(document)
                return
        _settings_status_label.text = "backend.settings.update refused: %s %s" % [
                _text(document.get("rejection")), _reason_of(document)
        ]


func _on_advanced_toggled() -> void:
        _advanced_box.visible = _advanced_button.button_pressed


# --- the model manager (wb-9 — fetch a GGUF from anywhere) -------------------


func _on_fetch_pressed() -> void:
        if not _session_live or _client == null:
                return
        if _fetch_execution != "":
                return
        var url_value := _fetch_input.text.strip_edges()
        if url_value == "":
                _fetch_status_label.text = "paste a URL first — a direct link, a huggingface.co page, or hf:repo/file"
                return
        _fetch_button.disabled = true
        _fetch_cancel_button.disabled = false
        _fetch_status_label.text = "dispatching the fetch run…"
        var request_id := _next_request_id("fetch-start")
        _client.call_operation(
                request_id, "run.start",
                {"work": "model.fetch", "arguments": {"url": url_value}},
                _session_id, request_id
        )


func _on_fetch_cancel_pressed() -> void:
        if _fetch_execution == "" or _client == null:
                return
        var request_id := _next_request_id("fetch-cancel")
        _client.call_operation(
                request_id, "run.cancel",
                {"execution_id": _fetch_execution}, _session_id, request_id
        )


func _on_fetch_start_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                var result: Dictionary = document.get("result")
                _fetch_execution = _text(result.get("execution_id"))
                _fetch_poll_failures = 0
                _fetch_status_label.text = "fetching — the progress rides the run poll"
                _poll_timer.start()
                return
        _reset_fetch_controls()
        if status == "UNKNOWN":
                _fetch_status_label.text = "fetch dispatch OUTCOME UNKNOWN (%s) — not blindly retried" % _reason_of(document)
                return
        _fetch_status_label.text = "model.fetch refused: %s %s" % [
                _text(document.get("rejection")), _reason_of(document)
        ]


func _on_fetch_get_answered(document: Dictionary) -> void:
        if _fetch_execution == "":
                return
        var status := _text(document.get("status"))
        if status != "OK":
                _fetch_execution = ""
                _reset_fetch_controls()
                _maybe_stop_poll_timer()
                _fetch_status_label.text = "run.get refused: %s %s" % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                return
        if not (document.get("result") is Dictionary):
                return
        var result: Dictionary = document.get("result")
        if not bool(result.get("terminal", false)):
                var progress: Dictionary = (
                        result.get("progress", {}) if result.get("progress") is Dictionary else {}
                )
                _fetch_status_label.text = _fetch_progress_note(progress)
                return
        _fetch_execution = ""
        _reset_fetch_controls()
        _maybe_stop_poll_timer()
        var state := _text(result.get("state"))
        var run_result: Dictionary = (
                result.get("result", {}) if result.get("result") is Dictionary else {}
        )
        match state:
                "COMPLETED":
                        _fetch_status_label.text = "fetched %s (%s) — refreshing the list" % [
                                _text(run_result.get("logical_name")),
                                _format_size(int(run_result.get("size_bytes", 0)))
                        ]
                        _refresh_models()
                "FAILED":
                        _fetch_status_label.text = "fetch FAILED · %s" % _first_diagnostic(result)
                "CANCELED":
                        _fetch_status_label.text = "fetch canceled (the truthful terminal)"
                _:
                        _fetch_status_label.text = "fetch terminal state %s (unmodelled — shown, never collapsed)" % state


func _fetch_progress_note(progress: Dictionary) -> String:
        var name_value := _text(progress.get("logical_name"))
        var downloaded := int(progress.get("downloaded_bytes", 0))
        var total_value = progress.get("total_bytes")
        if total_value == null:
                return "downloading %s — %s (total unknown)" % [
                        name_value, _format_size(downloaded)
                ]
        var total := int(total_value)
        if total > 0:
                var percent := int(float(downloaded) * 100.0 / float(total))
                return "downloading %s — %d%% (%s / %s)" % [
                        name_value, percent,
                        _format_size(downloaded), _format_size(total)
                ]
        return "downloading %s — %s" % [name_value, _format_size(downloaded)]


func _first_diagnostic(result: Dictionary) -> String:
        var diagnostics: Array = (
                result.get("diagnostics", []) if result.get("diagnostics") is Array else []
        )
        if diagnostics.is_empty():
                return "no diagnostics"
        var first := _text(diagnostics[0])
        if first.length() > FETCH_NOTE_MAX_LENGTH:
                first = first.substr(0, FETCH_NOTE_MAX_LENGTH) + "…"
        return first


func _reset_fetch_controls() -> void:
        _fetch_button.disabled = not _session_live
        _fetch_cancel_button.disabled = true


func _maybe_stop_poll_timer() -> void:
        if (
                _active_execution == ""
                and _fetch_execution == ""
                and _import_execution == ""
                and _load_execution == ""
                and _unload_execution == ""
        ):
                _poll_timer.stop()


# --- the local import circuit (wb-10 — the native picker, the owner's
# --- «просто открывающийся проводник и выбор уже скаченных локальных
# --- моделей» call) ------------------------------------------------------------


func _make_import_dialog() -> FileDialog:
        # The NATIVE picker (the OS file/folder dialog — the engine's
        # use_native_dialog; the built-in FileDialog renders where the
        # platform has no native surface, an honest graceful fallback).
        # ACCESS_FILESYSTEM: the models live anywhere on disk (the
        # Desktop downloads included), never inside res://.
        var dialog := FileDialog.new()
        dialog.access = FileDialog.ACCESS_FILESYSTEM
        dialog.use_native_dialog = true
        dialog.filters = PackedStringArray(IMPORT_FILTERS)
        dialog.files_selected.connect(_on_import_files_selected)
        dialog.dir_selected.connect(_on_import_dir_selected)
        add_child(dialog)
        return dialog


func _on_add_local_pressed() -> void:
        if not _session_live or _client == null:
                # wb-11: never a silent return — the note names the state
                # (§18: the effective state is never hidden; the owner's
                # «проводник не открывается» silence call).
                _fetch_status_label.text = "the models manager needs a live gateway session — the badge (top right) names the state; start Workbench.bat"
                return
        if _import_execution != "" or _fetch_execution != "":
                _fetch_status_label.text = "one transfer at a time — wait for the current one to land (or cancel it)"
                return
        _import_dialog.file_mode = FileDialog.FILE_MODE_OPEN_FILES
        _import_dialog.popup_centered()


func _on_add_folder_pressed() -> void:
        if not _session_live or _client == null:
                _fetch_status_label.text = "the models manager needs a live gateway session — the badge (top right) names the state; start Workbench.bat"
                return
        if _import_execution != "" or _fetch_execution != "":
                _fetch_status_label.text = "one transfer at a time — wait for the current one to land (or cancel it)"
                return
        _import_dialog.file_mode = FileDialog.FILE_MODE_OPEN_DIR
        _import_dialog.popup_centered()


func _on_open_models_folder_pressed() -> void:
        # The gateway's OWN models_root answer (never a local guess);
        # the OS file manager opens AT it — drop-by-hand stays a real
        # alternative to the picker.
        if _models_root == "":
                _fetch_status_label.text = "the models folder path arrives with the first models scan — Refresh"
                return
        var err := OS.shell_open(_models_root)
        if err != OK:
                _fetch_status_label.text = "the OS file manager refused to open %s (error %d)" % [_models_root, err]


func _on_import_files_selected(paths: PackedStringArray) -> void:
        if paths.is_empty():
                return
        var path_list: Array = []
        for picked in paths:
                path_list.append(String(picked))
        _dispatch_import(path_list)


func _on_import_dir_selected(directory: String) -> void:
        # The folder arm: enumerate the .gguf files INSIDE (one level,
        # the dialog's own answer) and hand the absolute paths to the
        # same run — presentation-local enumeration, the gateway owns
        # the landing.
        var names := DirAccess.get_files_at(directory)
        var path_list: Array = []
        for file_entry in names:
                var file_name := String(file_entry)
                if file_name.to_lower().ends_with(".gguf"):
                        path_list.append(
                                directory.rstrip("/") + "/" + file_name
                        )
        if path_list.is_empty():
                _fetch_status_label.text = "no .gguf files in %s — pick the folder that holds them" % directory
                return
        _dispatch_import(path_list)


func _dispatch_import(path_list: Array) -> void:
        _add_files_button.disabled = true
        _add_folder_button.disabled = true
        _fetch_button.disabled = true
        _import_cancel_button.disabled = false
        _fetch_status_label.text = "importing %d file(s)…" % path_list.size()
        var request_id := _next_request_id("import-start")
        _client.call_operation(
                request_id, "run.start",
                {"work": "model.import", "arguments": {"paths": path_list}},
                _session_id, request_id
        )


func _on_import_start_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                var result: Dictionary = document.get("result")
                _import_execution = _text(result.get("execution_id"))
                _import_poll_failures = 0
                _fetch_status_label.text = "importing — the progress rides the run poll"
                _poll_timer.start()
                return
        _reset_import_controls()
        if status == "UNKNOWN":
                _fetch_status_label.text = "import dispatch OUTCOME UNKNOWN (%s) — not blindly retried" % _reason_of(document)
                return
        _fetch_status_label.text = "model.import refused: %s %s" % [
                _text(document.get("rejection")), _reason_of(document)
        ]


func _on_import_get_answered(document: Dictionary) -> void:
        if _import_execution == "":
                return
        var status := _text(document.get("status"))
        if status != "OK":
                _import_execution = ""
                _reset_import_controls()
                _maybe_stop_poll_timer()
                _fetch_status_label.text = "run.get refused: %s %s" % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                return
        if not (document.get("result") is Dictionary):
                return
        var result: Dictionary = document.get("result")
        if not bool(result.get("terminal", false)):
                var progress: Dictionary = (
                        result.get("progress", {}) if result.get("progress") is Dictionary else {}
                )
                _fetch_status_label.text = _import_progress_note(progress)
                return
        _import_execution = ""
        _reset_import_controls()
        _maybe_stop_poll_timer()
        var state := _text(result.get("state"))
        var run_result: Dictionary = (
                result.get("result", {}) if result.get("result") is Dictionary else {}
        )
        match state:
                "COMPLETED":
                        var imported: Array = (
                                run_result.get("imported", []) if run_result.get("imported") is Array else []
                        )
                        _fetch_status_label.text = "imported %d model(s) — refreshing the list" % imported.size()
                        _refresh_models()
                "FAILED":
                        _fetch_status_label.text = "import FAILED · %s" % _first_diagnostic(result)
                "CANCELED":
                        _fetch_status_label.text = "import canceled (the truthful terminal)"
                _:
                        _fetch_status_label.text = "import terminal state %s (unmodelled — shown, never collapsed)" % state


func _on_import_cancel_pressed() -> void:
        if _import_execution == "" or _client == null:
                return
        var request_id := _next_request_id("import-cancel")
        _client.call_operation(
                request_id, "run.cancel",
                {"execution_id": _import_execution}, _session_id, request_id
        )


func _import_progress_note(progress: Dictionary) -> String:
        var name_value := _text(progress.get("logical_name"))
        var file_index := int(progress.get("file_index", 0)) + 1
        var file_count := int(progress.get("file_count", 1))
        var copied := int(progress.get("copied_bytes", 0))
        var total := int(progress.get("total_bytes", 0))
        if total > 0:
                var percent := int(float(copied) * 100.0 / float(total))
                return "importing %s (%d/%d) — %d%% (%s / %s)" % [
                        name_value, file_index, file_count, percent,
                        _format_size(copied), _format_size(total)
                ]
        return "importing %s (%d/%d) — %s" % [
                name_value, file_index, file_count, _format_size(copied)
        ]


func _reset_import_controls() -> void:
        _add_files_button.disabled = not _session_live
        _add_folder_button.disabled = not _session_live
        _import_cancel_button.disabled = true
        _reset_fetch_controls()


func _on_fetch_advanced_toggled() -> void:
        _fetch_advanced_box.visible = _fetch_advanced_button.button_pressed


# --- the chat surface's local actions ----------------------------------------


func _on_send_pressed() -> void:
        _send_current()


func _on_composer_submitted(_body: String) -> void:
        _send_current()


func _send_current() -> void:
        if not _session_live or _active_execution != "":
                return
        var text := _composer_input.text.strip_edges()
        if text == "":
                return
        _composer_input.text = ""
        _append_message("user", text)
        var request_id := _next_request_id("chat-send")
        _set_busy(true)  # from the press itself — no double-dispatch window
        _client.call_operation(
                request_id, "chat.send", {"messages": _chat_history()},
                _session_id, request_id
        )


func _on_stop_pressed() -> void:
        if _active_execution == "":
                return
        var request_id := _next_request_id("run-cancel")
        _client.call_operation(
                request_id, "run.cancel", {"execution_id": _active_execution},
                _session_id, request_id
        )


func _chat_history() -> Array[Dictionary]:
        # The chat payload: the user/assistant turns ONLY — the system notes
        # are presentation-local honesty, never fabricated context.
        var history: Array[Dictionary] = []
        for message in _messages:
                if String(message["role"]) in CHAT_ROLES:
                        history.append({"role": message["role"], "content": message["content"]})
        return history


func _set_busy(busy: bool) -> void:
        _send_button.disabled = busy or not _session_live
        _stop_button.disabled = not busy


func _set_badge(text: String, live: bool) -> void:
        _badge_label.text = text
        var colour := _c("status_success") if live else _c("status_warning")
        _badge_label.add_theme_color_override("font_color", colour)
        _badge_dot.color = colour


# --- the message list (bounded presentation, §15/§21) ------------------------


func _append_message(role: String, content: String) -> void:
        _messages.append({"role": role, "content": content})
        while _messages.size() > MAX_MESSAGES:
                _messages.pop_front()
                var first := _messages_box.get_child(0)
                if first != null:
                        first.queue_free()
                if not _trimmed_note_shown:
                        _trimmed_note_shown = true
                        # the one-shot boundedness note (display-only, never chat payload)
                        _messages_box.add_child(_message_card(
                                "system",
                                "display trimmed to the last %d messages (bounded, §15)" % MAX_MESSAGES
                        ))
        _add_message_card(role, content)


func _note_system(note: String) -> void:
        _append_message("system", note)


func _add_message_card(role: String, content: String) -> void:
        _empty_center.visible = false
        _messages_scroll.visible = true
        _messages_box.add_child(_message_card(role, content))
        if role == "assistant":
                _scroll_to_bottom.call_deferred()


func _message_card(role: String, content: String) -> Control:
        # The role styling (wb-10's visual pass): the user's card carries
        # the accent edge (card_user), the assistant's the plain card, a
        # system note is a bare muted line — no card, never noise.
        if role == "system":
                var note := Label.new()
                note.text = content
                note.add_theme_font_size_override("font_size", _k("font_size_caption"))
                note.add_theme_color_override("font_color", _c("text_muted"))
                note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
                note.size_flags_horizontal = Control.SIZE_EXPAND_FILL
                return note
        var card := PanelContainer.new()
        if role == "user":
                card.add_theme_stylebox_override("panel", _s("card_user"))
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_xs"))
        card.add_child(col)
        var role_label := Label.new()
        role_label.text = role.to_upper()
        role_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        var body_label := Label.new()
        body_label.text = content
        body_label.add_theme_font_size_override("font_size", _k("font_size_body"))
        body_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        body_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        match role:
                "user":
                        role_label.add_theme_color_override("font_color", _c("accent"))
                        body_label.add_theme_color_override("font_color", _c("text_primary"))
                "assistant":
                        role_label.add_theme_color_override("font_color", _c("text_secondary"))
                        body_label.add_theme_color_override("font_color", _c("text_primary"))
                _:
                        role_label.add_theme_color_override("font_color", _c("text_muted"))
                        body_label.add_theme_color_override("font_color", _c("text_muted"))
        col.add_child(role_label)
        col.add_child(body_label)
        return card


func _scroll_to_bottom() -> void:
        _messages_scroll.scroll_vertical = int(_messages_scroll.get_v_scroll_bar().max_value)


func _short(value: String) -> String:
        if value.length() <= 12:
                return value
        return value.substr(0, 12) + "…"


func _text(value) -> String:
        # null-safe: JSON nulls arrive as null, never a crash on the cast.
        if value == null:
                return ""
        return str(value)


func _reason_of(document: Dictionary) -> String:
        var result: Dictionary = document.get("result", {}) if document.get("result") is Dictionary else {}
        return _text(result.get("reason"))


# --- proof mode (§44: headless/screenshot is the agent-verification route) --


func _parse_proof_args(args: PackedStringArray) -> Dictionary:
        var out := {}
        var i := 0
        while i < args.size() - 1:
                match args[i]:
                        "--png":
                                out["png"] = args[i + 1]
                        "--meta":
                                out["meta"] = args[i + 1]
                        "--surface":
                                out["surface"] = args[i + 1]
                i += 1
        if out.has("png") and out.has("meta"):
                return out
        return {}


func _capture_and_quit(paths: Dictionary) -> void:
        await RenderingServer.frame_post_draw
        var img := get_viewport().get_texture().get_image()
        var err := img.save_png(paths["png"])
        if err != OK:
                push_error("shell: cannot save PNG %s (error %d)" % [paths["png"], err])
                get_tree().quit(3)
                return
        var meta := {
                "engine_version": Engine.get_version_info().get("string", ""),
                "shell_version": SHELL_VERSION,
                "theme_identity": FileAccess.get_sha256(THEME_PATH),
                "active_surface": _active_surface,
                "surfaces": SURFACES,
                "planned_surfaces": PLANNED_SURFACES,
                "live_circuit": false,
                "window_size": [int(get_viewport().size.x), int(get_viewport().size.y)],
                "png": String(paths["png"]),
        }
        var mf := FileAccess.open(paths["meta"], FileAccess.WRITE)
        if mf == null:
                push_error("shell: cannot write metadata %s" % paths["meta"])
                get_tree().quit(3)
                return
        mf.store_string(JSON.stringify(meta, "  ", false))
        mf.close()
        print("SHELL_PROOF_OK %s" % SHELL_VERSION)
        get_tree().quit(0)
