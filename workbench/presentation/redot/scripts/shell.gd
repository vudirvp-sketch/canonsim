# CanonSim Workbench — the wb-2/wb-7 application shell (frontend §46
# Phase A: custom theme -> Chat -> Settings).

# iter-234 (ux-1 — the P0 minimums row, FRONTEND_UIUX_LAW §25/§17/§15/§16:
# the owner's «начать работать в этом направлении» call over the Ultimate
# Frontend pack): the _tr() LOCALIZATION BOUNDARY lands (strings.gd —
# every user-facing literal rides a key, en+ru catalogs, OS-locale
# resolution with --lang/CANONSIM_LANG overrides, Cyrillic-safe widths)
# + the REDUCED-MOTION setting (the chat follow and the busy pulse gain
# static equivalents — LAW §15's motion contract; UI-local persistence in
# workbench/runtime/ui_state.json, never read or written in proof mode)
# + the VIEWPORT/MIN-SIZE policy (project.godot: min window, stretch
# canvas_items/expand — LAW §16's SMALL..ULTRAWIDE class contract) + the
# FOCUS/KEYBOARD baseline (Esc stops a live generation, Ctrl+. stops from
# anywhere, task-aware focus entry per surface — composer / refresh /
# first field; LAW §15). The KI#97 proof-pin repair rides the same row.

# iter-235 (obs-1 — FRONTEND_UIUX_LAW §25's P1 + §50/§51: the
# Observatory's vertical UX slice, the grammar validated BEFORE full
# analytical backend coverage): the nav rail adopts the §4.1 IA —
# WORK (Chat · Observatory; Simulation/Inference planned) /
# RESOURCES (Models; Prompts/History planned) / SYSTEM (Settings;
# Runs/Diagnostics planned — the LAW's own map, Inference kept,
# nothing silently dropped) + scripts/observatory.gd the
# responsibility-split seed (LAW §18: the axis composes its own
# surface at birth; the shell only hosts it): the breadcrumb, the
# context identity strip (the honest no-session values), the World
# Question contract (the DRAFT lifecycle — nothing asked, nothing
# claimed), ONE primary read-only view (the event table shape, the
# distinct NO DATA semantics), the inspector region, the evidence
# ladder (every rung's unknown status as text) — empty honestly,
# zero fabricated content, zero dispatch, zero new transport.
# iter-232 (KI#95/KI#96 + the OLED re-pin — the owner's 2026-09-25
# «цвет лучше взять темный под oled мониторы, но не синий такой
# убогий» + «проводник опять сломался видимо, я не могу папки
# открыть и модели не показывает языковые» calls): theme@0.4 re-pins
# the VALUES ONLY (the truly neutral near-black ramp over #050505 +
# the ONE teal accent — this script's token reads unchanged); KI#96
# kills the models-scan latch — entering the Models surface re-scans
# EVERY time (§20's routine refresh: the cheap discovery READ,
# model.list + model.states — files dropped into the folder by hand
# appear on the next surface entry, the latched "requested once" flag
# never freezes the list again).
#
# iter-230 (wb-12 + the chat follow mechanism — the owner's «тема и UI
# все так же убоги» + «в чате при получении сообщений от языковой модели
# => не происходит плавной прокрутки вниз» calls): the theme@0.3 token
# audit re-skins every surface through the tokens (this script's reads
# unchanged); the message list gains the FOLLOW LAW — a smooth tween over
# the scrollbar's value (never the integer jump), the target read AFTER a
# frame so the autowrap labels settle first, and a near-bottom gate so a
# reader scrolled up into history is never yanked; the chat's GENERATING
# state gains its visible carrier (the busy chip — a pulsing dot AND a
# text label, §4's not-color-only law); the nav rail moves onto the
# NavButton theme variation (navigation reads as navigation, not as a
# grid of action buttons — every value still lives in the theme).
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

const SHELL_VERSION := "canon_shell@0.8"  # inf-1: the Inference axis went REAL
const THEME_PATH := "res://themes/workbench_theme.tres"
const GATEWAY_CLIENT_SCRIPT := preload("res://scripts/gateway_client.gd")
# obs-1: the Observatory's own surface builder (LAW §18's split seed —
# the responsibility leaves the shell's composition at birth).
const OBSERVATORY_SCRIPT := preload("res://scripts/observatory.gd")
const INFERENCE_SCRIPT := preload("res://scripts/inference.gd")
# ux-1: the single translation boundary (strings.gd — the en/ru catalogs;
# every user-facing string rides a key, the honest fallback returns the
# key itself, never a silently wrong string).
const STRINGS := preload("res://scripts/strings.gd")
const GATEWAY_URL_SETTING := "canonism_workbench/gateway/url"
const GATEWAY_DEFAULT_URL := "http://127.0.0.1:8765"
# obs-1 — the §4.1 IA (LAW: SURFACE = intent, VIEW = representation;
# the rail reads as intent GROUPS, never a flat feature catalog):
# WORK (Chat, Observatory), RESOURCES (Models), SYSTEM (Settings).
const SURFACE_GROUPS := [
        {"caption": "nav.group.work", "keys": ["chat", "observatory", "inference"]},
        {"caption": "nav.group.resources", "keys": ["models"]},
        {"caption": "nav.group.system", "keys": ["settings"]},
]
const SURFACES := ["chat", "observatory", "inference", "models", "settings"]
# The planned axes per group (canonical identity names; the display
# rides _tr("nav.planned.<key>")). The LAW's map adds Runs (SYSTEM) —
# the honest gap made visible; Inference stays WORK-planned (the
# existing axis is never silently dropped, D-198's law).
const PLANNED_SURFACE_GROUPS := [
        {"caption": "nav.group.work", "keys": ["Simulation"]},
        {"caption": "nav.group.resources", "keys": ["Prompts", "History"]},
        {"caption": "nav.group.system", "keys": ["Runs", "Diagnostics"]},
]
const PLANNED_SURFACES := ["Simulation", "Prompts", "History", "Runs", "Diagnostics"]
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
# The chat follow law (iter-230 — the owner's «плавной прокрутки» call):
# the near-bottom window inside which a new message keeps following the
# conversation's tail, and the smooth scroll's duration. A reader farther
# up than the window is reading history — the view never yanks them.
const SCROLL_FOLLOW_SLOP_PX := 96.0
const SCROLL_TWEEN_S := 0.28

# The Settings surface's own state (wb-9): the launch-settings document
# arrives from backend.settings (the gateway's own answer); the preview
# label carries the command the NEXT managed spawn would run.

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
var _scroll_tween: Tween
var _busy_row: HBoxContainer
var _busy_dot: ColorRect
var _busy_label: Label
var _busy_tween: Tween
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
var _observatory: Control  # obs-2: the hosted surface (LAW §18 — the shell owns the seam, the axis owns its regions)
var _inference: Control  # inf-1: the hosted inference surface (the same LAW §18 split — the shell owns the transport, the surface owns its regions)
var _inference_summary: Dictionary = {}  # inf-1: the Chat projection's own cached read (profile name + the effective temperature)
var _models_active_label: Label
var _model_rows: Dictionary = {}
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
var _no_webui_check: CheckBox
var _extra_edit: LineEdit
var _advanced_box: VBoxContainer
var _advanced_button: Button
var _preview_label: Label
var _settings_status_label: Label
var _settings_save_button: Button
# ux-1 — the localization/motion state: the resolved display locale (en/ru)
# and the reduced-motion flag (LAW §15 — every tween/pulse keeps a static
# equivalent; UI-local persistence, never a backend concern).
var _ui_locale := "en"
var _motion_reduced := false
var _reduced_motion_check: CheckBox
# ux-1 — proof mode is pinned: locale "en", motion enabled, ui_state.json
# neither read nor written (the byte-identical capture law, §22).
var _proof_mode := false
var _proof_obs_run := ""  # obs-2: the proof injection's run stem (the meta's own honesty)


func _ready() -> void:
        _t = theme
        _proof_mode = not _parse_proof_args(OS.get_cmdline_user_args()).is_empty()
        # Proof runs are deterministic (§22): the locale resolves from the
        # EXPLICIT sources only (--lang arg > CANONSIM_LANG env > "en") —
        # the OS locale never leaks into a capture; a --lang ru capture is
        # byte-stable the same way the default en one is.
        _ui_locale = _resolve_locale(OS.get_cmdline_user_args(), not _proof_mode)
        if not _proof_mode:
                _load_ui_state()
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
        if paths.has("obs_document"):
                # obs-2's proof injection: the capture renders the LOADED
                # state over a real op-produced document (exit 4 = the
                # injection refused; 2 = a bad surface, 3 = a capture
                # failure — the codes stay distinct).
                if not _apply_obs_document(String(paths["obs_document"])):
                        return
        if paths.has("inference_document"):
                # inf-1's proof injection: the capture renders the
                # RESOLVED state over a real op-produced document (the
                # same exit-code discipline: 4 = the injection refused).
                if not _apply_inference_document(String(paths["inference_document"])):
                        return
        _capture_and_quit.call_deferred(paths)


# --- token access (the theme file is the single source — §10) ---------------


func _tr(key: String) -> String:
        # ux-1 — the single translation boundary (LAW §17): every user-facing
        # string rides a key; a missing key returns the key itself (visible in
        # review, never a silently wrong string).
        return STRINGS.lookup(key, _ui_locale)


func _resolve_locale(args: PackedStringArray, use_os_locale := true) -> String:
        # The resolution order: the --lang user arg, then the CANONSIM_LANG
        # env var, then the OS language (the owner's machine answers "ru"
        # natively); anything unrecognized falls back to "en" — honest,
        # never a crash. Proof mode passes use_os_locale=false: captures
        # resolve from explicit sources only, never the host's locale.
        var i := 0
        while i < args.size() - 1:
                if args[i] == "--lang":
                        var chosen := args[i + 1].to_lower()
                        if chosen in STRINGS.locales():
                                return chosen
                i += 1
        var from_env := OS.get_environment("CANONSIM_LANG").to_lower()
        if from_env in STRINGS.locales():
                return from_env
        if use_os_locale:
                var os_locale := OS.get_locale_language().to_lower()
                if os_locale in STRINGS.locales():
                        return os_locale
        return "en"


func _ui_state_path() -> String:
        # UI-local state lives in the established runtime root
        # (workbench/runtime/ — settings.json/launcher.json's own home,
        # gitignored, never a repo file).
        var base := ProjectSettings.globalize_path("res://")
        return base.get_base_dir().get_base_dir().get_base_dir() + "/workbench/runtime/ui_state.json"


func _load_ui_state() -> void:
        # The honest read: a missing file is the default state (motion on);
        # a corrupt file refuses loud and keeps the default — never a crash,
        # never a silent foreign shape.
        var path := _ui_state_path()
        if not FileAccess.file_exists(path):
                return
        var file := FileAccess.open(path, FileAccess.READ)
        if file == null:
                push_error("shell: ui_state.json unreadable — motion stays enabled")
                return
        var parsed = JSON.parse_string(file.get_as_text())
        file.close()
        if not (parsed is Dictionary):
                push_error("shell: ui_state.json is not an object — motion stays enabled")
                return
        _motion_reduced = bool(parsed.get("motion_reduced", false))


func _save_ui_state() -> void:
        if _proof_mode:
                return  # the capture law: proof never persists UI state
        var path := _ui_state_path()
        DirAccess.make_dir_recursive_absolute(path.get_base_dir())
        var file := FileAccess.open(path, FileAccess.WRITE)
        if file == null:
                push_error("shell: cannot write ui_state.json — the toggle stays session-local")
                return
        file.store_string(JSON.stringify({"motion_reduced": _motion_reduced}, "  ", false))
        file.close()


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
        title.text = _tr("app.title")
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
        _badge_label.text = _tr("app.badge.not_connected")
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
        _surface_nodes["observatory"] = _build_observatory_surface()
        _surface_nodes["models"] = _build_models_surface()
        _surface_nodes["inference"] = _build_inference_surface()
        _surface_nodes["settings"] = _build_settings_surface()
        for key in SURFACES:
                _surface_nodes[key].size_flags_vertical = Control.SIZE_EXPAND_FILL
                content.add_child(_surface_nodes[key])
        return body


func _build_inference_surface() -> Control:
        # inf-1 — the llama.cpp semantic inference-control workspace
        # (LLAMA_CPP_INFERENCE_CONTROL_LAW + FRONTEND_UIUX_LAW §2's IA:
        # Inference under WORK, the deep generation-control home —
        # Settings keeps the deployment half only). The LAW §18 split:
        # the surface composes ITSELF over the injected theme + the
        # shell's _tr Callable; it speaks ONLY through its two request
        # signals (the shell owns the ONE gateway client).
        var surface: Control = INFERENCE_SCRIPT.new()
        surface.compose(_t, Callable(self, "_tr"))
        surface.read_requested.connect(_on_inference_read_requested)
        surface.update_requested.connect(_on_inference_update_requested)
        _inference = surface
        return surface


func _build_observatory_surface() -> Control:
        # obs-1 (LAW §18's split seed): the surface composes ITSELF — the
        # shell injects the theme (the token single-source) and its own
        # _tr resolver (the ONE boundary; the observatory never opens the
        # catalog directly). The shell hosts; the axis owns its regions.
        # obs-2: the hosting wires the TWO request signals (the seam's
        # only form — the observatory never touches the gateway client;
        # the answers arrive through its public feed methods).
        var surface: VBoxContainer = OBSERVATORY_SCRIPT.new()
        surface.compose(_t, Callable(self, "_tr"))
        surface.runs_requested.connect(_on_observatory_runs_requested)
        surface.read_requested.connect(_on_observatory_read_requested)
        _observatory = surface
        return surface


func _build_nav_rail() -> Control:
        var rail := PanelContainer.new()
        rail.add_theme_stylebox_override("panel", _s("surface"))
        rail.custom_minimum_size = Vector2(_k("rail_width"), 0)

        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_s"))
        rail.add_child(col)

        # wb-12: the rail's quiet control set — a Button TYPE VARIATION so the
        # nav reads as navigation, never as a grid of action buttons. Every
        # value (colors, styleboxes, sizes) lives in the theme file under
        # NavButton/* — the token law holds (the code only names the type;
        # KI#94: the Control API is the theme_type_variation PROPERTY —
        # Redot 26.2 exposes no method form for it; the engine's own
        # 2026-09-25 report killed _ready at _build_nav_rail).
        _t.set_type_variation("NavButton", "Button")

        col.add_child(_caption(_tr("nav.group.work")))
        var group := ButtonGroup.new()
        var planned_by_group := {}
        for entry in PLANNED_SURFACE_GROUPS:
                planned_by_group[entry["caption"]] = entry["keys"]
        for entry in SURFACE_GROUPS:
                var group_caption: String = entry["caption"]
                if group_caption != "nav.group.work":
                        col.add_child(_caption(_tr(group_caption)))
                for key in entry["keys"]:
                        # ux-1: the display label rides the boundary (nav.chat /
                        # nav.observatory / nav.models / nav.settings — the
                        # Cyrillic-safe rail); the KEY stays the protocol
                        # identity for switching/meta.
                        var btn := _nav_button(_tr("nav." + key))
                        btn.theme_type_variation = "NavButton"
                        btn.toggle_mode = true
                        btn.button_group = group
                        btn.pressed.connect(_on_surface_selected.bind(key))
                        col.add_child(btn)
                        _nav_buttons[key] = btn
                        if key == "chat":
                                btn.button_pressed = true
                for axis_name in planned_by_group.get(group_caption, []):
                        var later := _nav_button(_tr("nav.planned." + axis_name.to_lower()))
                        later.theme_type_variation = "NavButton"
                        later.disabled = true
                        col.add_child(later)

        var spring := Control.new()
        spring.size_flags_vertical = Control.SIZE_EXPAND_FILL
        col.add_child(spring)

        var version := Label.new()
        version.text = _tr("nav.version") % [SHELL_VERSION, "canon_workbench_theme@0.4"]
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


var _chat_projection_label: Label  # inf-1 — the §21.2 compact projection


func _build_chat_projection_row() -> Control:
        # FRONTEND_UIUX_LAW §21.2 (the AI-interaction contract): the
        # Chat surface carries a COMPACT contextual projection of the
        # inference state (the profile name + the effective
        # temperature) with the link to the Inference workspace — the
        # full control depth lives THERE, Chat never holds its own
        # hidden sampler settings.
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_m"))
        _chat_projection_label = Label.new()
        _chat_projection_label.text = ""
        _chat_projection_label.add_theme_font_size_override(
                "font_size", _k("font_size_caption")
        )
        _chat_projection_label.add_theme_color_override(
                "font_color", _c("text_muted")
        )
        _chat_projection_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _chat_projection_label.clip_text = true
        row.add_child(_chat_projection_label)
        var link := Button.new()
        link.text = _tr("chat.inference.link")
        link.pressed.connect(func() -> void:
                _show_surface("inference")
        )
        row.add_child(link)
        return row


func _build_chat_surface() -> Control:
        var surface := VBoxContainer.new()
        surface.add_theme_constant_override("separation", _k("space_m"))
        surface.add_child(_surface_header(
                _tr("chat.title"),
                _tr("chat.subtitle")
        ))
        surface.add_child(_build_chat_projection_row())

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
        empty_title.text = _tr("chat.empty.title")
        empty_title.add_theme_font_size_override("font_size", _k("font_size_body"))
        empty_title.add_theme_color_override("font_color", _c("text_secondary"))
        empty_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        empty_col.add_child(empty_title)
        _empty_note = Label.new()
        _empty_note.text = _tr("chat.empty.note")
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

        # iter-230: the GENERATING state's visible carrier (§5's matrix
        # state — Chat: EMPTY | ACTIVE | GENERATING). A chip between the
        # list and the composer: the pulsing accent dot AND the text label
        # (§4's not-color-only law — the label is the mandatory half).
        _busy_row = HBoxContainer.new()
        _busy_row.visible = false
        var busy_chip := PanelContainer.new()
        busy_chip.add_theme_stylebox_override("panel", _s("chip_busy"))
        var busy_inner := HBoxContainer.new()
        busy_inner.add_theme_constant_override("separation", _k("space_s"))
        _busy_dot = ColorRect.new()
        _busy_dot.color = _c("accent")
        _busy_dot.custom_minimum_size = Vector2(8, 8)
        _busy_dot.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        _busy_label = Label.new()
        _busy_label.text = _tr("chat.busy.label")
        _busy_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        _busy_label.add_theme_color_override("font_color", _c("accent"))
        busy_inner.add_child(_busy_dot)
        busy_inner.add_child(_busy_label)
        busy_chip.add_child(busy_inner)
        _busy_row.add_child(busy_chip)
        surface.add_child(_busy_row)

        var composer := HBoxContainer.new()
        composer.add_theme_constant_override("separation", _k("space_s"))
        _composer_input = LineEdit.new()
        _composer_input.text = _tr("chat.composer.offline")
        _composer_input.editable = false
        _composer_input.custom_minimum_size = Vector2(0, 40)
        _composer_input.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        composer.add_child(_composer_input)
        _send_button = Button.new()
        _send_button.text = _tr("chat.send")
        # Cyrillic-safe (LAW §17): «Отправить» rides 112px — fixed widths
        # are layout contracts, never English-label accidents.
        _send_button.custom_minimum_size = Vector2(112, 40)
        _send_button.disabled = true
        _send_button.pressed.connect(_on_send_pressed)
        composer.add_child(_send_button)
        _stop_button = Button.new()
        _stop_button.text = _tr("chat.stop")
        _stop_button.tooltip_text = _tr("chat.stop.tooltip")
        _stop_button.custom_minimum_size = Vector2(112, 40)
        _stop_button.disabled = true
        _stop_button.pressed.connect(_on_stop_pressed)
        composer.add_child(_stop_button)
        surface.add_child(composer)
        return surface


func _build_models_surface() -> Control:
        var surface := VBoxContainer.new()
        surface.add_theme_constant_override("separation", _k("space_m"))
        surface.add_child(_surface_header(
                _tr("models.title"),
                _tr("models.subtitle")
        ))

        var toolbar := HBoxContainer.new()
        toolbar.add_theme_constant_override("separation", _k("space_s"))
        _models_refresh_button = Button.new()
        _models_refresh_button.text = _tr("models.refresh")
        _models_refresh_button.disabled = true
        _models_refresh_button.pressed.connect(_on_models_refresh_pressed)
        toolbar.add_child(_models_refresh_button)
        _models_active_label = Label.new()
        _models_active_label.text = _tr("models.active.none")
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
        _add_files_button.text = _tr("models.add_files")
        _add_files_button.tooltip_text = _tr("models.add_files.tooltip")
        _add_files_button.disabled = true
        _add_files_button.pressed.connect(_on_add_local_pressed)
        add_row.add_child(_add_files_button)
        _add_folder_button = Button.new()
        _add_folder_button.text = _tr("models.add_folder")
        _add_folder_button.tooltip_text = _tr("models.add_folder.tooltip")
        _add_folder_button.disabled = true
        _add_folder_button.pressed.connect(_on_add_folder_pressed)
        add_row.add_child(_add_folder_button)
        _open_folder_button = Button.new()
        _open_folder_button.text = _tr("models.open_folder")
        _open_folder_button.tooltip_text = _tr("models.open_folder.tooltip")
        _open_folder_button.disabled = true
        _open_folder_button.pressed.connect(_on_open_models_folder_pressed)
        add_row.add_child(_open_folder_button)
        _import_cancel_button = Button.new()
        _import_cancel_button.text = _tr("common.cancel")
        _import_cancel_button.tooltip_text = _tr("models.import_cancel.tooltip")
        _import_cancel_button.disabled = true
        _import_cancel_button.pressed.connect(_on_import_cancel_pressed)
        add_row.add_child(_import_cancel_button)
        add_col.add_child(add_row)
        _fetch_status_label = Label.new()
        _fetch_status_label.text = _tr("models.manager.offline")
        _fetch_status_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _fetch_status_label.add_theme_color_override("font_color", _c("text_muted"))
        _fetch_status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        _fetch_status_label.clip_text = true
        add_col.add_child(_fetch_status_label)
        _fetch_advanced_button = Button.new()
        _fetch_advanced_button.text = _tr("models.advanced")
        _fetch_advanced_button.toggle_mode = true
        _fetch_advanced_button.pressed.connect(_on_fetch_advanced_toggled)
        add_col.add_child(_fetch_advanced_button)
        _fetch_advanced_box = VBoxContainer.new()
        _fetch_advanced_box.visible = false
        _fetch_advanced_box.add_theme_constant_override("separation", _k("space_xs"))
        var fetch_row := HBoxContainer.new()
        fetch_row.add_theme_constant_override("separation", _k("space_s"))
        _fetch_input = LineEdit.new()
        _fetch_input.placeholder_text = _tr("models.fetch.placeholder")
        _fetch_input.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _fetch_input.editable = false
        fetch_row.add_child(_fetch_input)
        _fetch_button = Button.new()
        _fetch_button.text = _tr("models.fetch")
        _fetch_button.disabled = true
        _fetch_button.pressed.connect(_on_fetch_pressed)
        fetch_row.add_child(_fetch_button)
        _fetch_cancel_button = Button.new()
        _fetch_cancel_button.text = _tr("common.cancel")
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
        empty_title.text = _tr("models.empty.title")
        empty_title.add_theme_font_size_override("font_size", _k("font_size_body"))
        empty_title.add_theme_color_override("font_color", _c("text_secondary"))
        empty_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        empty_col.add_child(empty_title)
        _models_empty_note = Label.new()
        _models_empty_note.text = _tr("models.empty.note")
        _models_empty_note.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _models_empty_note.add_theme_color_override("font_color", _c("text_muted"))
        _models_empty_note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        _models_empty_note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        empty_col.add_child(_models_empty_note)
        empty.add_child(empty_col)
        surface.add_child(empty)
        _models_empty_center = empty

        _models_status_label = Label.new()
        _models_status_label.text = _tr("models.status.idle")
        _models_status_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _models_status_label.add_theme_color_override("font_color", _c("text_muted"))
        _models_status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        surface.add_child(_models_status_label)
        return surface


func _build_settings_surface() -> Control:
        var surface := VBoxContainer.new()
        surface.add_theme_constant_override("separation", _k("space_m"))
        surface.add_child(_surface_header(
                _tr("settings.title"),
                _tr("settings.subtitle")
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

        column.add_child(_setting_row(_tr("settings.theme"), _tr("settings.theme.value")))
        column.add_child(_setting_row(_tr("settings.language"), _tr("settings.language.value")))
        column.add_child(_build_interface_section())
        _settings_gateway_value = _setting_value_label(
                _tr("settings.gateway.offline")
        )
        column.add_child(_setting_row_with_value(_tr("settings.gateway"), _settings_gateway_value))
        _settings_backend_value = _setting_value_label(
                _tr("settings.backend.none")
        )
        column.add_child(_setting_row_with_value(_tr("settings.backend"), _settings_backend_value))
        column.add_child(_launch_settings_section())
        column.add_child(_setting_row(_tr("settings.simulation"), _tr("settings.simulation.value")))
        column.add_child(_setting_row(_tr("settings.keyboard"), _tr("settings.keyboard.value")))
        return surface


func _build_interface_section() -> Control:
        # ux-1 — the Interface row: the reduced-motion setting (LAW §15's
        # motion contract made visible and REVERSIBLE; applied immediately,
        # persisted UI-local in workbench/runtime/ui_state.json — never a
        # backend concern, never a gateway call).
        var card := PanelContainer.new()
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_s"))
        card.add_child(col)
        var title := Label.new()
        title.text = _tr("settings.interface")
        title.add_theme_font_size_override("font_size", _k("font_size_section_title"))
        title.add_theme_color_override("font_color", _c("text_primary"))
        col.add_child(title)
        _reduced_motion_check = CheckBox.new()
        _reduced_motion_check.text = _tr("settings.reduced_motion")
        _reduced_motion_check.button_pressed = _motion_reduced
        _reduced_motion_check.toggled.connect(_on_reduced_motion_toggled)
        col.add_child(_reduced_motion_check)
        return card


func _on_reduced_motion_toggled(pressed: bool) -> void:
        _motion_reduced = pressed
        _save_ui_state()
        if _motion_reduced:
                _stop_busy_pulse()  # the static equivalent: steady dot + label
        elif _busy_row != null and _busy_row.visible:
                _start_busy_pulse()  # re-arm the pulse the reduced mode parked


func _launch_settings_section() -> Control:
        # wb-9 — the REAL llama.cpp launch settings: the typed fields the
        # managed spawn reads (backend.settings over the gateway), the
        # collapsed advanced extras, and the effective command preview.
        var card := PanelContainer.new()
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_s"))
        card.add_child(col)

        var title := Label.new()
        title.text = _tr("settings.launch.title")
        title.add_theme_font_size_override("font_size", _k("font_size_section_title"))
        title.add_theme_color_override("font_color", _c("text_primary"))
        col.add_child(title)
        var note := Label.new()
        note.text = _tr("settings.launch.note")
        note.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        note.add_theme_color_override("font_color", _c("text_secondary"))
        note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        col.add_child(note)

        _llama_exe_edit = LineEdit.new()
        _llama_exe_edit.placeholder_text = _tr("settings.launch.exe.placeholder")
        col.add_child(_input_row(_tr("settings.launch.exe"), _llama_exe_edit))

        _no_webui_check = CheckBox.new()
        _no_webui_check.button_pressed = true
        col.add_child(_input_row(_tr("settings.launch.no_webui"), _no_webui_check))

        # inf-1 — Settings ≠ Inference Control (the law's §1): the
        # semantic generation controls moved to the INFERENCE
        # workspace (context, GPU placement, flash attention, the
        # sampler family, the chain); this section keeps the
        # DEPLOYMENT half + the raw extra_args hatch. The link row
        # carries the split visibly, never a dead editor.
        var inference_link := Button.new()
        inference_link.text = _tr("settings.launch.inference.link")
        inference_link.pressed.connect(func() -> void:
                _show_surface("inference")
        )
        col.add_child(inference_link)

        _advanced_button = Button.new()
        _advanced_button.text = _tr("settings.launch.advanced")
        _advanced_button.toggle_mode = true
        _advanced_button.pressed.connect(_on_advanced_toggled)
        col.add_child(_advanced_button)
        _advanced_box = VBoxContainer.new()
        _advanced_box.visible = false
        _advanced_box.add_theme_constant_override("separation", _k("space_xs"))
        _extra_edit = LineEdit.new()
        _extra_edit.placeholder_text = _tr("settings.launch.extra.placeholder")
        _advanced_box.add_child(_input_row(_tr("settings.launch.extra"), _extra_edit))
        _preview_label = Label.new()
        _preview_label.text = _tr("settings.launch.preview")
        _preview_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _preview_label.add_theme_color_override("font_color", _c("text_muted"))
        _preview_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        _advanced_box.add_child(_preview_label)
        col.add_child(_advanced_box)

        _settings_status_label = Label.new()
        _settings_status_label.text = _tr("settings.status.offline")
        _settings_status_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _settings_status_label.add_theme_color_override("font_color", _c("text_muted"))
        _settings_status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        col.add_child(_settings_status_label)

        _settings_save_button = Button.new()
        _settings_save_button.text = _tr("settings.save")
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
        legend.text = _tr("status.legend")
        legend.add_theme_font_size_override("font_size", _k("font_size_caption"))
        legend.add_theme_color_override("font_color", _c("text_secondary"))
        legend.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        legend.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        legend.clip_text = true
        row.add_child(legend)

        _gateway_state_label = Label.new()
        _gateway_state_label.text = _tr("status.gateway.offline")
        _gateway_state_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _gateway_state_label.add_theme_color_override("font_color", _c("text_muted"))
        _gateway_state_label.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        row.add_child(_gateway_state_label)

        var seam := Label.new()
        seam.text = _tr("status.seam")
        seam.add_theme_font_size_override("font_size", _k("font_size_caption"))
        seam.add_theme_color_override("font_color", _c("status_success"))
        seam.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        row.add_child(seam)

        var engine := Label.new()
        engine.text = _tr("status.engine")
        engine.add_theme_font_size_override("font_size", _k("font_size_caption"))
        engine.add_theme_color_override("font_color", _c("text_muted"))
        engine.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        row.add_child(engine)
        return bar


# --- surface switching -------------------------------------------------------


func _on_surface_selected(key: String) -> void:
        _show_surface(key)


func _unhandled_input(event: InputEvent) -> void:
        # ux-1 — the keyboard baseline (LAW §15): Escape cancels the current
        # transient action (a LIVE generation — the only transient this
        # shell owns so far), Ctrl+. stops it from anywhere. Both are
        # honest no-ops when nothing is generating — never a fake action.
        # Native surfaces (the OS file dialogs) consume their own Esc first.
        if event is InputEventKey and event.pressed and not event.echo:
                var key_event: InputEventKey = event
                var is_escape := key_event.keycode == KEY_ESCAPE
                var is_ctrl_period := (
                        key_event.keycode == KEY_PERIOD
                        and key_event.ctrl_pressed
                )
                if (is_escape or is_ctrl_period) and _active_execution != "":
                        _on_stop_pressed()
                        get_viewport().set_input_as_handled()
                        return
                if is_ctrl_period and _active_execution == "":
                        # Discoverable, never silent: the shortcut is wired
                        # even idle — nothing to stop is a no-op, not an error.
                        get_viewport().set_input_as_handled()


func _show_surface(key: String) -> void:
        _active_surface = key
        for surface_key in SURFACES:
                _surface_nodes[surface_key].visible = surface_key == key
        # KI#96 (iter-232): the scan latch is dead — every entry into the
        # Models surface re-scans (§20's routine refresh; both reads are
        # cheap, and the owner's hand-dropped GGUF files appear without a
        # manual Refresh). The wb-11 re-arm survives as the transport-
        # failure note's own surface (the next entry retries by itself).
        if key == "models" and _client != null:
                _refresh_models()
        if key == "observatory" and _client != null:
                # obs-2 — KI#96's law (no scan latch): every entry into
                # the Observatory re-reads (the runs listing + the
                # loaded window — the live feed's own refresh).
                _observatory.refresh()
        # The active axis owns the pressed state (the button group keeps the
        # exclusivity).
        if _nav_buttons.has(key):
                _nav_buttons[key].button_pressed = true
        # ux-1 — the task-aware focus entry (LAW §15): the surface switch
        # restores MEANINGFUL focus — the composer on Chat, the refresh
        # action on Models, the first launch field on Settings — deferred
        # one frame so the visibility settles; an offline (disabled) entry
        # control leaves focus where it is (the honest no-op).
        _focus_surface_entry.call_deferred(key)


func _focus_surface_entry(key: String) -> void:
        match key:
                "chat":
                        if _composer_input != null and _composer_input.editable:
                                _composer_input.grab_focus()
                "models":
                        if _models_refresh_button != null and not _models_refresh_button.disabled:
                                _models_refresh_button.grab_focus()
                "settings":
                        if _llama_exe_edit != null:
                                _llama_exe_edit.grab_focus()
                "observatory":
                        # obs-2 (LAW §15: Observatory → the query or the
                        # preserved selection): the slice's task-aware
                        # entry is the Refresh action — the surface's
                        # one verb (deferred; an offline/disabled entry
                        # control leaves focus where it is).
                        var obs_entry: Control = _observatory.entry_control()
                        if obs_entry != null and not obs_entry.disabled:
                                obs_entry.grab_focus()
                "inference":
                        # inf-1 (LAW §15): the Inference workspace's
                        # task-aware entry is the Save action (the
                        # surface's primary verb — disabled until a
                        # live read resolves, the honest no-op).
                        if _inference != null:
                                var inf_entry: Control = _inference.entry_control()
                                if inf_entry != null and not inf_entry.disabled:
                                        inf_entry.grab_focus()
                _:
                        pass  # an unknown surface never invents a focus target


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
        _settings_gateway_value.text = _tr("settings.gateway.probing") % _gateway_url
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
        _observatory.note_live()
        if _active_surface == "models":
                _refresh_models()
        if _active_surface == "observatory":
                _observatory.refresh()
        if _active_surface == "inference" and _client != null:
                _request_inference_read()


func _next_request_id(prefix: String) -> String:
        _request_counter += 1
        return "%s-%d" % [prefix, _request_counter]


func _on_operation_answered(tag: String, document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if tag == "app-status":
                if status == "OK":
                        _set_badge(_tr("app.badge.gateway_live"), true)
                        _gateway_state_label.text = _tr("status.gateway.live") % _gateway_url
                        _gateway_state_label.add_theme_color_override(
                                "font_color", _c("status_success")
                        )
                        _settings_gateway_value.text = _tr("settings.gateway.live") % _gateway_url
                        _client.call_operation(
                                "session-create", "session.create", {},
                                "", "wb-shell-session-%d" % OS.get_process_id()
                        )
                else:
                        _note_system(
                                _tr("chat.note.app_refused") % [
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
                                _set_badge(_tr("app.badge.session_live"), true)
                                _empty_note.text = _tr("chat.empty.note_live")
                                _composer_input.text = ""
                                _composer_input.placeholder_text = _tr("chat.composer.placeholder")
                                _composer_input.editable = true
                                _send_button.disabled = false
                                _update_models_enablement()
                                _fetch_input.editable = true
                                _fetch_button.disabled = false
                                _add_files_button.disabled = false
                                _add_folder_button.disabled = false
                                _settings_save_button.disabled = false
                                _request_backend_settings()
                                _request_inference_read()
                else:
                        _note_system(
                                _tr("chat.note.session_refused") % [
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
        if tag == "observatory-runs":
                _on_observatory_runs_answered(document)
                return
        if tag == "observatory-read":
                _on_observatory_read_answered(document)
                return
        if tag == "backend-settings":
                _on_backend_settings_answered(document)
                return
        if tag == "inference-read":
                _on_inference_read_answered(document)
                return
        if tag.begins_with("inference-save-"):
                _on_inference_saved_answered(document)
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
                        _fetch_status_label.text = _tr("chat.note.run_cancel_refused") % [
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
                        _fetch_status_label.text = _tr("chat.note.run_cancel_refused") % [
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
                                _tr("chat.note.run_cancel_refused") % [
                                        _text(document.get("rejection")),
                                        _reason_of(document),
                                ]
                        )
                return
        _note_system(_tr("chat.note.unexpected") % [tag, status])


func _on_chat_send_answered(_tag: String, document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                var result: Dictionary = document.get("result")
                _active_execution = _text(result.get("execution_id"))
                _poll_failures = 0
                _poll_timer.start()
                _set_busy(true)
                _note_system(
                        _tr("chat.note.dispatched") % _short(_active_execution)
                )
                return
        if status == "UNKNOWN":
                _note_system(
                        _tr("chat.note.outcome_unknown") % _reason_of(document)
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
                        _tr("chat.note.get_refused") % [
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
                                _tr("chat.note.finish") % [
                                        _text(run_result.get("finish_reason")),
                                        _backend_note(backend),
                                ]
                        )
                        _observe_backend(backend)
                "FAILED":
                        _note_system(
                                _tr("chat.note.run_failed") % _text(result.get("failure_type"))
                        )
                "CANCELED":
                        _note_system(_tr("chat.note.run_canceled"))
                "FAILED_TO_CANCEL":
                        # §12.3: the late result was recorded; the truth is the
                        # failed cancel. Both are shown, never merged.
                        _note_system(
                                _tr("chat.note.cancel_failed")
                        )
                        _append_message("assistant", _text(run_result.get("content")))
                "UNKNOWN":
                        _note_system(_tr("chat.note.run_unknown"))
                _:
                        _note_system(_tr("chat.note.run_unmodelled") % state)


func _backend_note(backend: Dictionary) -> String:
        if backend.is_empty():
                return _tr("chat.backend.unavailable")
        if _text(backend.get("probe")) == "unavailable":
                return _tr("chat.backend.probe_unavailable")
        var model := _text(backend.get("model"))
        var build := _text(backend.get("build"))
        if model == "":
                model = _tr("chat.backend.unknown_model")
        if build == "":
                build = _tr("chat.backend.unknown_build")
        return "%s · %s" % [model, build]


func _observe_backend(backend: Dictionary) -> void:
        if backend.is_empty():
                _settings_backend_value.text = (
                        _tr("chat.backend.no_identity")
                )
        elif _text(backend.get("probe")) == "unavailable":
                _settings_backend_value.text = (
                        _tr("chat.backend.observed_probe")
                )
        else:
                _settings_backend_value.text = _tr("chat.backend.observed") % _backend_note(backend)


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
                _set_badge(_tr("app.badge.not_connected"), false)
                _gateway_state_label.text = _tr("status.gateway.unreachable") % error
                _empty_note.text = _tr("chat.empty.unreachable") % error
                _settings_gateway_value.text = _tr("settings.gateway.unreachable") % _gateway_url
                return
        if tag == "model-list" or tag == "model-states":
                # wb-11's honest failure note (KI#96's every-entry rescan
                # owns the retry — the next surface entry re-arms by
                # itself, the empty list never sticks silently).
                _models_status_label.text = (
                        _tr("models.status.unreachable") % [tag, error]
                )
                return
        if tag == "observatory-runs" or tag == "observatory-read":
                # obs-2 — the honest transport failure rides the
                # surface's own state box (the position resets; the next
                # entry/Refresh retries by itself).
                _observatory.feed_transport_failure(error)
                return
        if tag == "backend-settings":
                _settings_status_label.text = _tr("settings.status.unreachable") % error
                return
        if tag == "inference-read":
                if _inference != null:
                        _inference.feed_transport_failure(error)
                return
        if tag.begins_with("inference-save-"):
                if _inference != null:
                        _inference.feed_transport_failure(error)
                return
        if tag.begins_with("settings-save-"):
                _settings_status_label.text = _tr("settings.status.save_transport") % error
                return
        if tag.begins_with("fetch-start-"):
                _reset_fetch_controls()
                _fetch_status_label.text = _tr("fetch.status.dispatch_transport") % error
                return
        if tag.begins_with("import-start-"):
                _reset_import_controls()
                _fetch_status_label.text = _tr("fetch.status.import_dispatch_transport") % error
                return
        if tag.begins_with("import-get-"):
                _import_poll_failures += 1
                if _import_poll_failures >= MAX_POLL_FAILURES:
                        _import_execution = ""
                        _reset_import_controls()
                        _fetch_status_label.text = _tr("fetch.status.import_abandoned") % [MAX_POLL_FAILURES, error]
                        _maybe_stop_poll_timer()
                return
        if tag.begins_with("import-cancel-"):
                _fetch_status_label.text = _tr("chat.note.cancel_transport") % error
                return
        if tag.begins_with("fetch-get-"):
                _fetch_poll_failures += 1
                if _fetch_poll_failures >= MAX_POLL_FAILURES:
                        _fetch_execution = ""
                        _reset_fetch_controls()
                        _fetch_status_label.text = _tr("fetch.status.fetch_abandoned") % [MAX_POLL_FAILURES, error]
                        _maybe_stop_poll_timer()
                return
        if tag.begins_with("fetch-cancel-"):
                _fetch_status_label.text = _tr("chat.note.cancel_transport") % error
                return
        # wb-11: the POLL arms first — "model-load-get-N" also begins with
        # "model-load-", the longer prefix owns the match.
        if tag.begins_with("model-load-get-"):
                # The load run's poll transport failures — bounded
                # abandon, the same law as the chat/fetch/import polls.
                _load_poll_failures += 1
                if _load_poll_failures >= MAX_POLL_FAILURES:
                        _load_execution = ""
                        _models_status_label.text = _tr("models.status.load_abandoned") % [MAX_POLL_FAILURES, error]
                        _maybe_stop_poll_timer()
                return
        if tag.begins_with("model-unload-get-"):
                _unload_poll_failures += 1
                if _unload_poll_failures >= MAX_POLL_FAILURES:
                        _unload_execution = ""
                        _models_status_label.text = _tr("models.status.unload_abandoned") % [MAX_POLL_FAILURES, error]
                        _maybe_stop_poll_timer()
                return
        if tag.begins_with("model-load-") or tag.begins_with("model-unload-"):
                # The action never reached the gateway — the row's truth is
                # unchanged (SELECTED/ACTIVE), the button returns honestly.
                _models_status_label.text = _tr("models.status.action_transport") % [tag, error]
                _client.call_operation("model-states", "model.states", {})
                return
        if tag.begins_with("run-get-"):
                _poll_failures += 1
                if _poll_failures >= MAX_POLL_FAILURES:
                        _active_execution = ""
                        _set_busy(false)
                        _maybe_stop_poll_timer()
                        _note_system(
                                _tr("chat.note.poll_abandoned") % [
                                        MAX_POLL_FAILURES, error
                                ]
                        )
                return
        if tag.begins_with("run-cancel-"):
                # The cancel request itself failed to send — the run is still
                # in flight, the poll continues, Stop stays the honest action.
                _note_system(_tr("chat.note.cancel_transport") % error)
                return
        _note_system(_tr("chat.note.transport") % [tag, error])
        _set_busy(false)


# --- the models surface (wb-8 — discovery, load, unload, the truth) ----------


func _on_models_refresh_pressed() -> void:
        _refresh_models()


func _refresh_models() -> void:
        # The honest discovery re-scan (§20): model.list + the lifecycle
        # read (model.states) — both READs, no session needed, no fake.
        # KI#96: called on EVERY surface entry (the latch retired) and on
        # the Refresh action — the routine-refresh form.
        if _client == null:
                return
        _models_status_label.text = _tr("models.status.scanning")
        _client.call_operation("model-list", "model.list", {})
        _client.call_operation("model-states", "model.states", {})


# --- obs-2: the Observatory seam (the shell owns the transport) ----------


func _on_observatory_runs_requested() -> void:
        # The surface's runs_requested signal: the discovery scan over
        # the canonical runs root (READ, no session).
        if _client == null:
                return
        _client.call_operation("observatory-runs", "observatory.runs", {})


func _on_observatory_read_requested(run: String, after: String) -> void:
        # The surface's read_requested signal: the bounded window (the
        # limit stays the OP's own default — the single source of the
        # boundedness law, never a UI-side second ceiling).
        if _client == null:
                return
        var arguments := {"run": run}
        if after != "":
                arguments["after"] = after
        _client.call_operation("observatory-read", "observatory.read", arguments)


func _on_observatory_runs_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                _observatory.feed_runs(document.get("result"))
                return
        _observatory.feed_rejection(_observatory_rejection_text(document))


func _on_observatory_read_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                _observatory.feed_read(document.get("result"))
                return
        _observatory.feed_rejection(_observatory_rejection_text(document))


func _observatory_rejection_text(document: Dictionary) -> String:
        # The refusal's own identity + the observed reason (LAW §21.1:
        # the backend's cause rides verbatim, never a generic error).
        var rejection := _text(document.get("rejection"))
        var reason := _reason_of(document)
        if reason == "":
                return rejection
        return "%s · %s" % [rejection, reason]


func _on_model_list_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status != "OK" or not (document.get("result") is Dictionary):
                _models_status_label.text = _tr("models.status.list_refused") % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                return
        var result: Dictionary = document.get("result")
        var directory_state := _text(result.get("directory_state"))
        if directory_state == "MISSING":
                _models_empty_note.text = _tr("models.status.missing_dir")
        var models: Array = result.get("models", []) if result.get("models") is Array else []
        _models_root = _text(result.get("models_root"))
        if _models_root != "":
                _open_folder_button.disabled = false
        _rebuild_models_list(models)
        if models.is_empty():
                _models_status_label.text = _tr("models.status.none_found") % [directory_state, _models_root]
        else:
                _models_status_label.text = _tr("models.status.discovered") % [
                        models.size(), directory_state
                ]
        # (the states read is already in flight from _refresh_models —
        # the sequential queue keeps the pair honest, no duplicate)


func _on_model_states_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status != "OK" or not (document.get("result") is Dictionary):
                _models_status_label.text = _tr("models.status.states_refused") % [
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
        action.text = _tr("models.action.load")
        action.custom_minimum_size = Vector2(112, 0)  # «Загрузить» — Cyrillic-safe
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
                var observed := _text(states.get(logical_name, "DISCOVERED"))
                _set_model_row_state(logical_name, observed)
        if active != "":
                _models_active_label.text = _tr("models.active.observed") % active
        else:
                _models_active_label.text = _tr("models.active.none")
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
                _models_status_label.text = _tr("models.status.load_needs_live")
                return
        var row: Dictionary = _model_rows.get(logical_name, {})
        if row.is_empty():
                return
        var action: Button = row["action"]
        action.disabled = true
        action.text = _tr("models.action.loading")
        _set_model_row_state(logical_name, "LOADING")
        _models_status_label.text = _tr("models.status.loading") % logical_name
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
                _models_status_label.text = _tr("models.status.unload_needs_live")
                return
        var row: Dictionary = _model_rows.get(logical_name, {})
        if row.is_empty():
                return
        var action: Button = row["action"]
        action.disabled = true
        action.text = _tr("models.action.unloading")
        _set_model_row_state(logical_name, "UNLOADING")
        _models_status_label.text = _tr("models.status.unloading") % logical_name
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
                _models_status_label.text = _tr("models.status.load_unknown") % _reason_of(document)
        else:
                _models_status_label.text = _tr("models.status.load_refused") % [
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
                _models_status_label.text = _tr("models.status.unload_unknown") % _reason_of(document)
        else:
                _models_status_label.text = _tr("models.status.unload_refused") % [
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
                _models_status_label.text = _tr("chat.note.get_refused") % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                _client.call_operation("model-states", "model.states", {})
                _update_models_enablement()
                return
        if not (document.get("result") is Dictionary):
                return
        var result: Dictionary = document.get("result")
        if not bool(result.get("terminal", false)):
                _models_status_label.text = _tr("models.status.loading_walk") % [
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
                        _models_active_label.text = _tr("models.active.observed") % logical_name
                        _models_status_label.text = _tr("models.status.active_ready") % logical_name
                "FAILED":
                        var note := _text(result.get("failure_type"))
                        var cause := _first_diagnostic(result)
                        if cause.length() > MODEL_LOAD_NOTE_MAX_LENGTH:
                                cause = cause.substr(0, MODEL_LOAD_NOTE_MAX_LENGTH) + "…"
                        _models_status_label.text = _tr("models.status.load_failed") % [note, cause]
                "CANCELED":
                        _models_status_label.text = _tr("models.status.load_canceled")
                _:
                        _models_status_label.text = _tr("models.status.load_unmodelled") % run_state
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
                _models_status_label.text = _tr("chat.note.get_refused") % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                _client.call_operation("model-states", "model.states", {})
                _update_models_enablement()
                return
        if not (document.get("result") is Dictionary):
                return
        var result: Dictionary = document.get("result")
        if not bool(result.get("terminal", false)):
                _models_status_label.text = _tr("models.status.unloading_walk") % [
                        _unload_model, _text(result.get("state"))
                ]
                return
        _unload_execution = ""
        var logical_name := _unload_model
        _unload_model = ""
        var run_state := _text(result.get("state"))
        match run_state:
                "COMPLETED":
                        _models_status_label.text = _tr("models.status.evicted") % logical_name
                "FAILED":
                        var cause := _first_diagnostic(result)
                        if cause.length() > MODEL_LOAD_NOTE_MAX_LENGTH:
                                cause = cause.substr(0, MODEL_LOAD_NOTE_MAX_LENGTH) + "…"
                        _models_status_label.text = _tr("models.status.unload_failed") % [
                                _text(result.get("failure_type")), cause
                        ]
                "CANCELED":
                        _models_status_label.text = _tr("models.status.unload_canceled")
                _:
                        _models_status_label.text = _tr("models.status.unload_unmodelled") % run_state
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
                        action.text = _tr("models.action.unload")
                        action.disabled = not _session_live
                        _rebind_action(logical_name, "_on_model_unload_pressed")
                else:
                        action.text = _tr("models.action.load")
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


func _request_inference_read() -> void:
        if _client == null:
                return
        _client.call_operation("inference-read", "inference.read", {})


func _on_inference_read_requested() -> void:
        _request_inference_read()


func _on_inference_update_requested(payload: Dictionary) -> void:
        if not _session_live or _client == null:
                return
        var request_id := _next_request_id("inference-save")
        _client.call_operation(
                request_id, "inference.update", payload,
                _session_id, request_id
        )


func _on_inference_read_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status != "OK" or not (document.get("result") is Dictionary):
                if _inference != null:
                        _inference.feed_rejection(_reason_of(document))
                return
        var result: Dictionary = document.get("result")
        if _inference != null:
                _inference.feed_read(result)
        # the Chat projection's own cache (§21.2: the compact line —
        # the profile name + the effective temperature; Chat links to
        # Inference, never its own hidden sampler surface)
        _inference_summary = {
                "profile": _text(result.get("profile_name")),
                "temperature": _effective_temperature_of(result),
        }
        _apply_chat_projection()


func _effective_temperature_of(result: Dictionary) -> String:
        if not (result.get("controls") is Array):
                return ""
        for entry in result["controls"]:
                if not (entry is Dictionary):
                        continue
                if _text(entry.get("id")) == "sampling.temperature":
                        var value = entry.get("value")
                        if typeof(value) == TYPE_FLOAT:
                                return "%.2f" % float(value)
                        if typeof(value) == TYPE_INT:
                                return str(int(value))
        return ""


func _on_inference_saved_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                var result: Dictionary = document.get("result")
                if _inference != null:
                        _inference.feed_read(result)
                _inference_summary = {
                        "profile": _text(result.get("profile_name")),
                        "temperature": _effective_temperature_of(result),
                }
                _apply_chat_projection()
                return
        if _inference != null:
                _inference.feed_rejection(_reason_of(document))


func _apply_chat_projection() -> void:
        if _chat_projection_label == null:
                return
        if _inference_summary.is_empty():
                _chat_projection_label.text = ""
                return
        _chat_projection_label.text = _tr("chat.inference.projection") % [
                _text(_inference_summary.get("profile", "")),
                _text(_inference_summary.get("temperature", "")),
        ]


func _on_backend_settings_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status != "OK" or not (document.get("result") is Dictionary):
                _settings_status_label.text = _tr("settings.status.settings_refused") % [
                        _text(document.get("rejection")), _reason_of(document)
                ]
                return
        _populate_settings_fields(document.get("result"))


func _populate_settings_fields(result: Dictionary) -> void:
        # inf-1: the DEPLOYMENT half only (the semantic fields moved
        # to the inference profile — Settings ≠ Inference Control).
        var settings: Dictionary = (
                result.get("settings", {}) if result.get("settings") is Dictionary else {}
        )
        if settings.is_empty():
                return
        _llama_exe_edit.text = _text(settings.get("llama_server_exe"))
        _no_webui_check.button_pressed = bool(settings.get("no_webui", true))
        _extra_edit.text = _text(settings.get("extra_args"))
        var preview := _text(result.get("command_preview"))
        if preview != "":
                _preview_label.text = preview
        var suffix := _tr("settings.status.effective_next")
        if bool(result.get("managed_live")):
                suffix = _tr("settings.status.effective_live")
        _settings_status_label.text = _tr("settings.status.effective") % suffix


func _on_settings_save_pressed() -> void:
        if not _session_live or _client == null:
                return
        # inf-1: the DEPLOYMENT document (the closed settings/2 set —
        # the semantic edits ride the Inference surface's own save)
        var document := {
                "llama_server_exe": _llama_exe_edit.text.strip_edges(),
                "no_webui": _no_webui_check.button_pressed,
                "extra_args": _extra_edit.text.strip_edges(),
        }
        _settings_status_label.text = _tr("settings.status.saving")
        var request_id := _next_request_id("settings-save")
        _client.call_operation(
                request_id, "backend.settings.update", document,
                _session_id, request_id
        )


func _on_settings_saved_answered(document: Dictionary) -> void:
        var status := _text(document.get("status"))
        if status == "OK" and document.get("result") is Dictionary:
                _populate_settings_fields(document.get("result"))
                _settings_status_label.text = _tr("settings.status.saved")
                return
        if status == "UNKNOWN":
                _settings_status_label.text = _tr("settings.status.save_unknown") % _reason_of(document)
                return
        _settings_status_label.text = _tr("settings.status.save_refused") % [
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
                _fetch_status_label.text = _tr("fetch.status.url_first")
                return
        _fetch_button.disabled = true
        _fetch_cancel_button.disabled = false
        _fetch_status_label.text = _tr("fetch.status.dispatching")
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
                _fetch_status_label.text = _tr("fetch.status.fetching")
                _poll_timer.start()
                return
        _reset_fetch_controls()
        if status == "UNKNOWN":
                _fetch_status_label.text = _tr("fetch.status.outcome_unknown") % _reason_of(document)
                return
        _fetch_status_label.text = _tr("fetch.status.refused") % [
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
                _fetch_status_label.text = _tr("chat.note.get_refused") % [
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
                        _fetch_status_label.text = _tr("fetch.status.fetched") % [
                                _text(run_result.get("logical_name")),
                                _format_size(int(run_result.get("size_bytes", 0)))
                        ]
                        _refresh_models()
                "FAILED":
                        _fetch_status_label.text = _tr("fetch.status.failed") % _first_diagnostic(result)
                "CANCELED":
                        _fetch_status_label.text = _tr("fetch.status.canceled")
                _:
                        _fetch_status_label.text = _tr("fetch.status.unmodelled") % state


func _fetch_progress_note(progress: Dictionary) -> String:
        var name_value := _text(progress.get("logical_name"))
        var downloaded := int(progress.get("downloaded_bytes", 0))
        var total_value = progress.get("total_bytes")
        if total_value == null:
                return _tr("fetch.progress.unknown_total") % [
                        name_value, _format_size(downloaded)
                ]
        var total := int(total_value)
        if total > 0:
                var percent := int(float(downloaded) * 100.0 / float(total))
                return _tr("fetch.progress.percent") % [
                        name_value, percent,
                        _format_size(downloaded), _format_size(total)
                ]
        return _tr("fetch.progress.plain") % [name_value, _format_size(downloaded)]


func _first_diagnostic(result: Dictionary) -> String:
        var diagnostics: Array = (
                result.get("diagnostics", []) if result.get("diagnostics") is Array else []
        )
        if diagnostics.is_empty():
                return _tr("fetch.progress.no_diagnostics")
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
        # ux-1: the filters ride the boundary too — the OS dialog's own
        # display strings (the registry accepts any plain file; the filter
        # is a convenience, never a gate — wb-10's law unchanged).
        dialog.filters = PackedStringArray([
                _tr("models.dialog.gguf"), _tr("models.dialog.all"),
        ])
        dialog.files_selected.connect(_on_import_files_selected)
        dialog.dir_selected.connect(_on_import_dir_selected)
        add_child(dialog)
        return dialog


func _on_add_local_pressed() -> void:
        if not _session_live or _client == null:
                # wb-11: never a silent return — the note names the state
                # (§18: the effective state is never hidden; the owner's
                # «проводник не открывается» silence call).
                _fetch_status_label.text = _tr("models.needs_live")
                return
        if _import_execution != "" or _fetch_execution != "":
                _fetch_status_label.text = _tr("models.one_transfer")
                return
        _import_dialog.file_mode = FileDialog.FILE_MODE_OPEN_FILES
        _import_dialog.popup_centered()


func _on_add_folder_pressed() -> void:
        if not _session_live or _client == null:
                _fetch_status_label.text = _tr("models.needs_live")
                return
        if _import_execution != "" or _fetch_execution != "":
                _fetch_status_label.text = _tr("models.one_transfer")
                return
        _import_dialog.file_mode = FileDialog.FILE_MODE_OPEN_DIR
        _import_dialog.popup_centered()


func _on_open_models_folder_pressed() -> void:
        # The gateway's OWN models_root answer (never a local guess);
        # the OS file manager opens AT it — drop-by-hand stays a real
        # alternative to the picker.
        if _models_root == "":
                _fetch_status_label.text = _tr("fetch.status.folder_pending")
                return
        var err := OS.shell_open(_models_root)
        if err != OK:
                _fetch_status_label.text = _tr("fetch.status.open_failed") % [_models_root, err]


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
                _fetch_status_label.text = _tr("fetch.status.no_gguf") % directory
                return
        _dispatch_import(path_list)


func _dispatch_import(path_list: Array) -> void:
        _add_files_button.disabled = true
        _add_folder_button.disabled = true
        _fetch_button.disabled = true
        _import_cancel_button.disabled = false
        _fetch_status_label.text = _tr("fetch.status.importing_count") % path_list.size()
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
                _fetch_status_label.text = _tr("fetch.status.importing")
                _poll_timer.start()
                return
        _reset_import_controls()
        if status == "UNKNOWN":
                _fetch_status_label.text = _tr("fetch.status.import_unknown") % _reason_of(document)
                return
        _fetch_status_label.text = _tr("fetch.status.import_refused") % [
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
                _fetch_status_label.text = _tr("chat.note.get_refused") % [
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
                        _fetch_status_label.text = _tr("fetch.status.imported") % imported.size()
                        _refresh_models()
                "FAILED":
                        _fetch_status_label.text = _tr("fetch.status.import_failed") % _first_diagnostic(result)
                "CANCELED":
                        _fetch_status_label.text = _tr("fetch.status.import_canceled")
                _:
                        _fetch_status_label.text = _tr("fetch.status.import_unmodelled") % state


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
                return _tr("import.progress.percent") % [
                        name_value, file_index, file_count, percent,
                        _format_size(copied), _format_size(total)
                ]
        return _tr("import.progress.plain") % [
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
        # iter-230: the GENERATING state's carrier — the busy chip rides the
        # same single busy owner (§5's matrix state, §4 label+color+position).
        _busy_row.visible = busy
        if busy:
                _start_busy_pulse()
        else:
                _stop_busy_pulse()


func _start_busy_pulse() -> void:
        # ux-1 — the reduced-motion static equivalent (LAW §15): no loop
        # tween; the busy chip's steady dot AND text label carry the state
        # (§4's not-color-only law already made the label mandatory).
        if _motion_reduced:
                _busy_dot.modulate.a = 1.0
                return
        if _busy_tween != null and _busy_tween.is_valid():
                return
        _busy_tween = create_tween()
        _busy_tween.set_loops()
        _busy_tween.tween_property(_busy_dot, "modulate:a", 0.35, 0.55)
        _busy_tween.tween_property(_busy_dot, "modulate:a", 1.0, 0.55)


func _stop_busy_pulse() -> void:
        if _busy_tween != null and _busy_tween.is_valid():
                _busy_tween.kill()
        _busy_tween = null
        _busy_dot.modulate.a = 1.0


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
                                _tr("chat.note.trimmed") % MAX_MESSAGES
                        ))
        _add_message_card(role, content)


func _note_system(note: String) -> void:
        _append_message("system", note)


func _add_message_card(role: String, content: String) -> void:
        _empty_center.visible = false
        _messages_scroll.visible = true
        _messages_box.add_child(_message_card(role, content))
        _request_scroll_follow()


func _request_scroll_follow() -> void:
        # iter-230 — the follow law (the owner's «не происходит плавной
        # прокрутки вниз» call): the follow decision is made BEFORE the new
        # card's height lands (was the reader at the tail?), the scroll runs
        # deferred so the layout pass completes first — never the integer
        # jump, never a yank of a reader deep in history.
        var follows := _near_bottom()
        _scroll_follow_deferred.call_deferred(follows)


func _near_bottom() -> bool:
        var bar := _messages_scroll.get_v_scroll_bar()
        return bar.value >= (bar.max_value - bar.page) - SCROLL_FOLLOW_SLOP_PX


func _scroll_follow_deferred(follows: bool) -> void:
        if not follows:
                return
        _scroll_to_bottom_smooth()


func _scroll_to_bottom_smooth() -> void:
        # The smooth bottom: one frame of layout settle (the autowrapped
        # labels size late — reading the bar's max too early is the old
        # short-scroll bug), then a cubic-out tween over the scrollbar's
        # float value. The late-layout guard re-settles once if a long
        # message grew the content after the target was read.
        # ux-1 — the reduced-motion static equivalent (LAW §15): the settle
        # frame stays (layout correctness, not motion); the jump is direct,
        # never animated.
        await get_tree().process_frame
        if not is_inside_tree():
                return
        var bar := _messages_scroll.get_v_scroll_bar()
        var target := bar.max_value
        if target <= bar.page:
                return  # the list fits — nothing to follow
        if _scroll_tween != null and _scroll_tween.is_valid():
                _scroll_tween.kill()
        if _motion_reduced:
                bar.value = target
                return
        _scroll_tween = create_tween()
        _scroll_tween.tween_property(bar, "value", target, SCROLL_TWEEN_S).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
        _scroll_tween.tween_callback(_after_follow_tween.bind(target))


func _after_follow_tween(target: float) -> void:
        # The bounded re-settle: if the content grew past the tweened target
        # (a card settling late), ONE more smooth pass — never a loop.
        var bar := _messages_scroll.get_v_scroll_bar()
        if bar.max_value > target + 1.0:
                _scroll_to_bottom_smooth()


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
        # ux-1: the role caption rides the boundary (chat.role.user /
        # chat.role.assistant); the role TOKEN stays the protocol identity
        # for styling — never displayed raw.
        role_label.text = _tr("chat.role." + role)
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
                        "--inference-document":
                                # inf-1's runtime-proof injection (the
                                # obs-2 pattern): a REAL op-produced
                                # inference.read result document — the
                                # capture proves the resolved rendering
                                # through the same feed path (proof args
                                # only, never a second data path).
                                out["inference_document"] = args[i + 1]
                        "--obs-document":
                                # obs-2's runtime-proof injection (LAW §43):
                                # a REAL op-produced read document — the
                                # capture proves the loaded rendering
                                # through the same feed path the gateway
                                # serves (never a second data path in the
                                # interactive form — proof args only).
                                out["obs_document"] = args[i + 1]
                i += 1
        if out.has("png") and out.has("meta"):
                return out
        return {}


func _apply_obs_document(path: String) -> bool:
        # The proof harness's ONLY injection (LAW §43: the runtime proof
        # renders a REAL op-produced document through the same feed path
        # the gateway serves). The document comes from the actual
        # observatory.read over a fixture log — the capture proves the
        # LOADED rendering (the context strip, the rows, the selected
        # inspector, the scoped ladder) without a network. False = the
        # injection refused (the caller quits 4 — the codes stay
        # distinct: 2 surface, 3 capture, 4 injection).
        var file := FileAccess.open(path, FileAccess.READ)
        if file == null:
                push_error("shell: cannot read --obs-document %s" % path)
                get_tree().quit(4)
                return false
        # Redot 26.2's JSON law: parse_string is the static form (parse
        # is an instance method since 4.3's JSON rework — the engine
        # index's version firewall, D-207).
        var parsed_result = JSON.parse_string(file.get_as_text())
        if parsed_result == null or not (parsed_result is Dictionary):
                push_error("shell: --obs-document %s is not a JSON object" % path)
                get_tree().quit(4)
                return false
        var document: Dictionary = parsed_result
        _proof_obs_run = String(document.get("run", ""))
        _observatory.apply_read_document(document, true)
        return true


func _apply_inference_document(path: String) -> bool:
        # inf-1's proof injection (the obs-2 pattern, verbatim): the
        # document comes from the actual inference.read over the real
        # gateway — the capture proves the resolved rendering (the
        # context strip, the control rows + states, the ordered chain,
        # the compiled preview) without a network. False = refused
        # (the caller quits 4 — the codes stay distinct).
        var file := FileAccess.open(path, FileAccess.READ)
        if file == null:
                push_error("shell: cannot read --inference-document %s" % path)
                get_tree().quit(4)
                return false
        var parsed_result = JSON.parse_string(file.get_as_text())
        if parsed_result == null or not (parsed_result is Dictionary):
                push_error(
                        "shell: --inference-document %s is not a JSON object" % path
                )
                get_tree().quit(4)
                return false
        var document: Dictionary = parsed_result
        if _inference != null:
                _inference.apply_read_document(document)
        # the Chat projection rides the same document (the §21.2 law)
        _inference_summary = {
                "profile": _text(document.get("profile_name")),
                "temperature": _effective_temperature_of(document),
        }
        _apply_chat_projection()
        return true


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
                "observatory_run": _proof_obs_run,
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
