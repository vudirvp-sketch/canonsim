# CanonSim Workbench — the wb-2 application shell (frontend §46 Phase A).
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
# What this script is NOT: a chat client or a settings engine. The Chat and
# Settings surfaces are placeholders — their real machinery opens on the
# later wb rows (the gateway is wb-4; the app-operations skeleton wb-3).
#
# Invocation (the operator runner scripts/visual_proof.py --shell):
#   <redot> --path <project> res://scenes/shell.tscn -- --png <p> --meta <m>
# With --png/--meta the shell composes, awaits one clean frame, captures the
# screenshot + writes the proof metadata, then exits 0 (the headless/screenshot
# route — frontend §44). Without user args it simply stays open (interactive).
extends Control

const SHELL_VERSION := "canon_shell@0.1"
const THEME_PATH := "res://themes/workbench_theme.tres"
const SURFACES := ["chat", "settings"]
const PLANNED_SURFACES := ["Models", "Inference", "Prompts", "History", "Diagnostics", "Simulation"]

var _t: Theme
var _surface_nodes: Dictionary = {}
var _active_surface := "chat"
var _nav_buttons: Dictionary = {}


func _ready() -> void:
	_t = theme
	_build()
	var paths := _parse_proof_args(OS.get_cmdline_user_args())
	if paths.is_empty():
		return  # interactive launch: the shell stays open
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
	var badge_row := HBoxContainer.new()
	badge_row.add_theme_constant_override("separation", _k("space_s"))
	badge.add_child(badge_row)
	var dot := ColorRect.new()
	dot.color = _c("status_warning")
	dot.custom_minimum_size = Vector2(8, 8)
	dot.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	badge_row.add_child(dot)
	var badge_label := Label.new()
	badge_label.text = "CANONSIM · NOT CONNECTED"
	badge_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
	badge_label.add_theme_color_override("font_color", _c("status_warning"))
	badge_row.add_child(badge_label)
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
	version.text = "%s · theme %s" % [SHELL_VERSION, "canon_workbench_theme@0.1"]
	version.add_theme_font_size_override("font_size", _k("font_size_caption"))
	version.add_theme_color_override("font_color", _c("text_muted"))
	version.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	col.add_child(version)
	return rail


func _nav_button(label: String) -> Button:
	var btn := Button.new()
	btn.text = label
	btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
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
		"Placeholder surface — the inbound gateway opens on its own wb row (wb-4)."
	))

	var messages := PanelContainer.new()
	messages.size_flags_vertical = Control.SIZE_EXPAND_FILL
	var empty := CenterContainer.new()
	var empty_col := VBoxContainer.new()
	empty_col.add_theme_constant_override("separation", _k("space_xs"))
	var empty_title := Label.new()
	empty_title.text = "No messages"
	empty_title.add_theme_font_size_override("font_size", _k("font_size_body"))
	empty_title.add_theme_color_override("font_color", _c("text_secondary"))
	empty_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	empty_col.add_child(empty_title)
	var empty_note := Label.new()
	empty_note.text = "Nothing is fabricated: the backend is not connected."
	empty_note.add_theme_font_size_override("font_size", _k("font_size_caption"))
	empty_note.add_theme_color_override("font_color", _c("text_muted"))
	empty_note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	empty_col.add_child(empty_note)
	empty.add_child(empty_col)
	messages.add_child(empty)
	surface.add_child(messages)

	var composer := HBoxContainer.new()
	composer.add_theme_constant_override("separation", _k("space_s"))
	var input := LineEdit.new()
	input.text = "Not connected — the gateway opens on wb-4"
	input.editable = false
	input.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	composer.add_child(input)
	var send := Button.new()
	send.text = "Send"
	send.disabled = true
	composer.add_child(send)
	surface.add_child(composer)
	return surface


func _build_settings_surface() -> Control:
	var surface := VBoxContainer.new()
	surface.add_theme_constant_override("separation", _k("space_m"))
	surface.add_child(_surface_header(
		"Settings",
		"Global behaviour and appearance — the effective values, honestly."
	))
	surface.add_child(_setting_row("Theme", "canon_workbench_theme@0.1 · dark — the only admitted theme"))
	surface.add_child(_setting_row("Language", "English · localisation opens on its own wb row"))
	surface.add_child(_setting_row("Backend", "none connected · the inbound gateway opens on wb-4"))
	surface.add_child(_setting_row("Simulation", "seam proven (wb-1) · the surface opens on its wb row"))
	surface.add_child(_setting_row("Keyboard & focus", "tab order + visible focus from the theme tokens"))
	return surface


func _setting_row(key: String, value: String) -> Control:
	var card := PanelContainer.new()
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", _k("space_m"))
	var key_label := Label.new()
	key_label.text = key
	key_label.add_theme_font_size_override("font_size", _k("font_size_body"))
	key_label.add_theme_color_override("font_color", _c("text_primary"))
	row.add_child(key_label)
	var value_label := Label.new()
	value_label.text = value
	value_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
	value_label.add_theme_color_override("font_color", _c("text_secondary"))
	value_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	value_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	value_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(value_label)
	card.add_child(row)
	return card


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
	# The active axis owns the pressed state (the button group keeps the
	# exclusivity) and the keyboard focus (§13: visible focus, logical order).
	if _nav_buttons.has(key):
		_nav_buttons[key].button_pressed = true
		_nav_buttons[key].grab_focus()


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

