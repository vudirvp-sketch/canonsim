# CanonSim Workbench — inference.gd (inf-2: the llama.cpp semantic
# inference-control WORKSPACE — the full chip library's Redot
# projection).
#
# LLAMA_CPP_INFERENCE_CONTROL_LAW owns the architecture; this surface
# is its UI PROJECTION (the law's §2: the UI representation is never
# the semantic authority — a chip is a semantic runtime control, the
# visual chip is ONE projection of it). The meaning, the validation
# and the effective-state resolution live in
# workbench/application/inference.py; this file only renders the
# resolved document and collects the operator's edits.
#
# What this surface IS (the law's §15 workspace): the CONTEXT strip
# (the profile + the honest next-spawn note + the §30 PRESETS row
# with its transparent diff preview), the SEARCH field, the PINNED
# strip (the §14 workspace state — quick-access chips, one click
# reveals the control), the CONTEXT-AWARE LIBRARY (the semantic
# categories, COLLAPSIBLE — progressive disclosure: the six
# general-chat categories open, the rest one click away, an advanced
# toggle for the expert rung, search over name/flag/category), the
# SAMPLER CHAIN (the ordered first-class object — all 9 reviewed
# members, never a favorites grid), and the compiled preview (the
# technical artifact, collapsed behind the advanced toggle — never
# the authoring language).
#
# inf-2's own repair over inf-1: the control rows are DATA-DRIVEN
# (the read document's own kind/forms/limits metadata builds the
# editors — the UI never re-encodes the vocabulary; a new control
# lands by the server's document alone) and they BUILD ON THE READ
# (inf-1 composed the categories before the first read — the live
# flow rendered empty groups, the proof-only flow hid it).
#
# Honesty laws that govern every line below:
#   · zero fabricated state — every state badge renders the RESOLVED
#     document's own vocabulary (EFFECTIVE / AUTO / INACTIVE /
#     INEFFECTIVE + the reason text; the law's §8: configured-but-
#     ineffective controls stay VISIBLE with their reason, never
#     hidden or deleted)
#   · AUTO is a real state (the law's §10): 'auto' renders as AUTO,
#     an explicit value as its number, disabled-by-value as INACTIVE —
#     the three never collapse
#   · the resolved states shown are the SERVER's answer (the last
#     read's truth — an edited field is a REQUEST, never a truth; the
#     badge stays stale-honest until the next read)
#   · a preset applies as a TRANSPARENT diff (the §14 law: preview
#     every field it would change, the chips stay editable after the
#     apply — never an opaque mode)
#   · the unsaved edits SURVIVE a refresh (the carried editor values
#     law — a re-read rebuilds the rows with the operator's in-flight
#     values re-applied; the one exception: the read that answers OUR
#     OWN save, where the document IS the new truth)
extends VBoxContainer


const INFERENCE_VERSION := "canon_inference@0.2"

# The request surface: the shell dispatches these over the ONE gateway
# client; the answers arrive through feed_read.
signal read_requested()
signal update_requested(payload: Dictionary)

# The gpu_layers composite's forms (the runtime's own literal values;
# 'explicit' enables the count editor — a UI-local mode, never a
# server value).
const GPU_FORMS := ["auto", "all", "explicit"]

# The general-chat default visibility (the chip spec §17's own list):
# the six categories a new workspace opens with; every other family
# stays one disclosure click away (never a flat 85-control wall).
const DEFAULT_OPEN_CATEGORIES := [
        "model", "device", "memory", "moe", "sampling", "chat",
]

# The bool controls' display forms (the on/off pair).
const BOOL_FORMS := ["on", "off"]

var _t: Theme
var _tr_call: Callable
# --- the live state (every rendered value sourced from a feed) ---
var _document: Dictionary = {}
var _built := false                     # the rows exist (the first read built them)
var _suppress_carry_once := false       # the next feed IS our own save's answer
var _pinned_ids: Array = []             # the workspace's pinned control ids
# --- widget refs ---
var _profile_label: Label
var _applies_label: Label
var _preview_label: Label
var _status_label: Label
var _save_button: Button
var _refresh_button: Button
var _advanced_button: Button
var _advanced_box: VBoxContainer
var _scroll: ScrollContainer
var _library_column: VBoxContainer
var _search_edit: LineEdit
var _advanced_check: CheckButton
var _preset_option: OptionButton
var _preset_preview_button: Button
var _preset_apply_button: Button
var _preset_diff_label: Label
var _pinned_flow: HFlowContainer
var _editors: Dictionary = {}           # id -> {editor, kind, value_type, field}
var _rows: Dictionary = {}              # id -> {row, state_label, reason_label, category}
var _category_sections: Dictionary = {}  # category -> {body, header, count}
var _category_open: Dictionary = {}     # category -> bool (survives rebuilds)
var _chain_box: VBoxContainer           # the ordered region
var _chain_rows: Array = []             # [{id, check, row, order_label}] in current order


func compose(theme: Theme, translator: Callable) -> void:
        _t = theme
        _tr_call = translator
        add_theme_constant_override("separation", _k("space_m"))
        add_child(_build_header())
        add_child(_build_context_strip())
        add_child(_build_tools_row())
        add_child(_build_pinned_strip())
        _scroll = ScrollContainer.new()
        _scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
        _scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
        _library_column = VBoxContainer.new()
        _library_column.add_theme_constant_override("separation", _k("space_s"))
        _library_column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _scroll.add_child(_library_column)
        add_child(_scroll)
        add_child(_build_save_row())


func refresh() -> void:
        read_requested.emit()


func feed_read(document: Dictionary) -> void:
        if not (document is Dictionary) or document.is_empty():
                return
        _document = document
        _populate_from_document(document)


func feed_rejection(reason: String) -> void:
        _status_label.text = _tr("inference.status.refused") % reason


func feed_transport_failure(error: String) -> void:
        _status_label.text = _tr("inference.status.transport") % error


func apply_read_document(document: Dictionary) -> void:
        # The proof harness's ONLY injection point (the runtime proof
        # renders a REAL op-produced document through the same feed
        # path the gateway serves; the interactive path always rides
        # the gateway, never a file read).
        feed_read(document)


func entry_control() -> Control:
        # The task-aware focus entry (ux-1's law): the primary action.
        return _save_button


func note_live() -> void:
        # The live-circuit note (the shell wires the transport late —
        # the surface stays honest-empty until the first read).
        _status_label.text = _tr("inference.status.probing")


# ------------------------------------------------------------ composition


func _build_header() -> Control:
        var header := VBoxContainer.new()
        header.add_theme_constant_override("separation", _k("space_xs"))
        var title := Label.new()
        title.text = _tr("inference.title")
        title.add_theme_font_size_override("font_size", _k("font_size_page_title"))
        title.add_theme_color_override("font_color", _c("text_primary"))
        header.add_child(title)
        var subtitle := Label.new()
        subtitle.text = _tr("inference.subtitle")
        subtitle.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        subtitle.add_theme_color_override("font_color", _c("text_secondary"))
        subtitle.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        header.add_child(subtitle)
        return header


func _build_context_strip() -> Control:
        var card := PanelContainer.new()
        card.add_theme_stylebox_override("panel", _s("surface"))
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_xs"))
        card.add_child(col)
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_m"))
        _profile_label = Label.new()
        _profile_label.text = _tr("inference.context.offline")
        _profile_label.add_theme_font_size_override("font_size", _k("font_size_body"))
        _profile_label.add_theme_color_override("font_color", _c("text_primary"))
        _profile_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        row.add_child(_profile_label)
        _refresh_button = Button.new()
        _refresh_button.text = _tr("inference.refresh")
        _refresh_button.pressed.connect(refresh)
        row.add_child(_refresh_button)
        col.add_child(row)
        _applies_label = Label.new()
        _applies_label.text = _tr("inference.context.applies_next")
        _applies_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _applies_label.add_theme_color_override("font_color", _c("text_muted"))
        _applies_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        col.add_child(_applies_label)
        col.add_child(_build_preset_row())
        _preset_diff_label = Label.new()
        _preset_diff_label.text = ""
        _preset_diff_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _preset_diff_label.add_theme_color_override("font_color", _c("text_secondary"))
        _preset_diff_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        _preset_diff_label.visible = false
        col.add_child(_preset_diff_label)
        return card


func _build_preset_row() -> Control:
        # The §30 presets (the law's §14): a named STARTING POINT,
        # applied as a TRANSPARENT diff (the preview below lists every
        # field it would change; the chips stay editable after the
        # apply — never an opaque "mode").
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_s"))
        var caption := Label.new()
        caption.text = _tr("inference.preset.caption")
        caption.add_theme_font_size_override("font_size", _k("font_size_body"))
        caption.add_theme_color_override("font_color", _c("text_secondary"))
        row.add_child(caption)
        _preset_option = OptionButton.new()
        _preset_option.custom_minimum_size = Vector2(180.0, 0.0)
        _preset_option.item_selected.connect(_on_preset_selected)
        row.add_child(_preset_option)
        _preset_preview_button = Button.new()
        _preset_preview_button.text = _tr("inference.preset.preview")
        _preset_preview_button.disabled = true
        _preset_preview_button.pressed.connect(_on_preset_preview)
        row.add_child(_preset_preview_button)
        _preset_apply_button = Button.new()
        _preset_apply_button.text = _tr("inference.preset.apply")
        _preset_apply_button.disabled = true
        _preset_apply_button.pressed.connect(_on_preset_apply)
        row.add_child(_preset_apply_button)
        return row


func _build_tools_row() -> Control:
        # The workspace tools: the SEARCH field (name / raw flag /
        # category — the chip spec §32's own match families) + the
        # ADVANCED rung (the expert controls stay hidden until asked).
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_s"))
        _search_edit = LineEdit.new()
        _search_edit.placeholder_text = _tr("inference.search.placeholder")
        _search_edit.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _search_edit.text_changed.connect(_on_search_changed)
        row.add_child(_search_edit)
        _advanced_check = CheckButton.new()
        _advanced_check.text = _tr("inference.search.advanced")
        _advanced_check.toggled.connect(_on_advanced_controls_toggled)
        row.add_child(_advanced_check)
        return row


func _build_pinned_strip() -> Control:
        # The §14 workspace state: the PINNED quick-access chips (the
        # ordering policy's first rung — an explicit personal pin, a
        # DIFFERENT concern from the ACTIVE state; a pinned chip is a
        # one-click REVEAL of its control, never a second editor).
        var card := PanelContainer.new()
        card.add_theme_stylebox_override("panel", _s("surface"))
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_xs"))
        card.add_child(col)
        var caption := Label.new()
        caption.text = _tr("inference.pinned.caption")
        caption.add_theme_font_size_override("font_size", _k("font_size_caption"))
        caption.add_theme_color_override("font_color", _c("text_muted"))
        col.add_child(caption)
        _pinned_flow = HFlowContainer.new()
        _pinned_flow.add_theme_constant_override("separation", _k("space_xs"))
        col.add_child(_pinned_flow)
        return card


func _build_save_row() -> Control:
        var box := HBoxContainer.new()
        box.add_theme_constant_override("separation", _k("space_m"))
        _status_label = Label.new()
        _status_label.text = _tr("inference.status.offline")
        _status_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _status_label.add_theme_color_override("font_color", _c("text_muted"))
        _status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        _status_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        box.add_child(_status_label)
        _save_button = Button.new()
        _save_button.text = _tr("inference.save")
        _save_button.disabled = true
        _save_button.pressed.connect(_on_save_pressed)
        box.add_child(_save_button)
        return box


func _on_advanced_toggled() -> void:
        _advanced_box.visible = _advanced_button.button_pressed


# ------------------------------------------------------ the library build


func _rebuild_library() -> void:
        # The data-driven rebuild (inf-2's repair: inf-1 composed the
        # categories BEFORE the first read — the live flow rendered
        # empty groups). The read document's own controls array builds
        # the sections; the carried editor values law re-applies the
        # operator's in-flight edits afterwards.
        var carried := _carry_editor_values()
        for child in _library_column.get_children():
                _library_column.remove_child(child)
                child.queue_free()
        _editors.clear()
        _rows.clear()
        _category_sections.clear()
        _chain_rows.clear()
        if not (_document.get("controls") is Array):
                return
        var controls_by_category := {}
        for entry in _document["controls"]:
                if not (entry is Dictionary):
                        continue
                var category := _text(entry.get("category"))
                if not controls_by_category.has(category):
                        controls_by_category[category] = []
                controls_by_category[category].append(entry)
        var order: Array = _document.get("categories", [])
        var category_ids := []
        for category_entry in order:
                if category_entry is Dictionary:
                        category_ids.append(_text(category_entry.get("id")))
        for category in controls_by_category.keys():
                if not (category in category_ids):
                        category_ids.append(category)
        for category in category_ids:
                var entries: Array = controls_by_category.get(category, [])
                if entries.is_empty():
                        continue
                _library_column.add_child(
                        _build_category_section(category, entries)
                )
                if category == "sampling":
                        _library_column.add_child(_build_chain_region())
        _library_column.add_child(_build_advanced_region())
        _rebuild_chain_rows()
        _reapply_carried_values(carried)
        _apply_search_filter()


func _build_category_section(category: String, entries: Array) -> Control:
        var card := PanelContainer.new()
        card.add_theme_stylebox_override("panel", _s("surface"))
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_xs"))
        card.add_child(col)
        var header := HBoxContainer.new()
        header.add_theme_constant_override("separation", _k("space_s"))
        var open: bool = _category_open.get(
                category, category in DEFAULT_OPEN_CATEGORIES
        )
        var toggle := Button.new()
        toggle.text = "▾" if open else "▸"
        toggle.tooltip_text = _tr("inference.category.toggle.tooltip")
        toggle.pressed.connect(_on_category_toggled.bind(category, toggle))
        header.add_child(toggle)
        var title := Label.new()
        title.text = _category_title(category)
        title.add_theme_font_size_override("font_size", _k("font_size_section_title"))
        title.add_theme_color_override("font_color", _c("text_primary"))
        title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        header.add_child(title)
        var count := Label.new()
        count.text = _tr("inference.category.count") % entries.size()
        count.add_theme_font_size_override("font_size", _k("font_size_caption"))
        count.add_theme_color_override("font_color", _c("text_muted"))
        header.add_child(count)
        col.add_child(header)
        var body := VBoxContainer.new()
        body.add_theme_constant_override("separation", _k("space_xs"))
        body.visible = open
        col.add_child(body)
        for entry in entries:
                body.add_child(_build_control_row(entry))
        _category_sections[category] = {"body": body, "header": header}
        return card


func _on_category_toggled(category: String, toggle: Button) -> void:
        # The disclosure state is WORKSPACE state (it survives
        # rebuilds — the operator's own library shape).
        var section: Dictionary = _category_sections.get(category, {})
        if section.is_empty():
                return
        var body: VBoxContainer = section["body"]
        body.visible = not body.visible
        _category_open[category] = body.visible
        toggle.text = "▾" if body.visible else "▸"


func _build_control_row(control: Dictionary) -> Control:
        var id := _text(control.get("id"))
        var row := VBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_xs"))
        var line := HBoxContainer.new()
        line.add_theme_constant_override("separation", _k("space_m"))
        var pin := Button.new()
        pin.flat = true
        pin.text = "★" if id in _pinned_ids else "☆"
        pin.tooltip_text = _tr("inference.pin.tooltip")
        pin.pressed.connect(_on_pin_toggled.bind(id))
        line.add_child(pin)
        var name_label := Label.new()
        name_label.text = _text(control.get("name"))
        name_label.add_theme_font_size_override("font_size", _k("font_size_body"))
        name_label.add_theme_color_override("font_color", _c("text_primary"))
        name_label.tooltip_text = _flag_tooltip(control)
        name_label.custom_minimum_size = Vector2(190.0, 0.0)
        name_label.clip_text = true
        line.add_child(name_label)
        var editor := _build_editor(control)
        if editor != null:
                editor.size_flags_horizontal = Control.SIZE_EXPAND_FILL
                line.add_child(editor)
        var state_label := Label.new()
        state_label.text = _text(control.get("state"))
        state_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        state_label.add_theme_color_override(
                "font_color", _state_color(_text(control.get("state")))
        )
        state_label.custom_minimum_size = Vector2(110.0, 0.0)
        state_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
        state_label.tooltip_text = _join_reasons(control)
        line.add_child(state_label)
        row.add_child(line)
        var reason_label := Label.new()
        reason_label.text = ""
        reason_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        reason_label.add_theme_color_override("font_color", _c("text_muted"))
        reason_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        reason_label.visible = false
        row.add_child(reason_label)
        var reasons := _join_reasons(control)
        if reasons != "":
                reason_label.text = reasons
                reason_label.visible = true
        var category := _text(control.get("category"))
        _editors[id] = {
                "editor": editor,
                "value_type": _text(control.get("value_type")),
                "field": _text(control.get("field")),
                "forms": control.get("forms", []),
        }
        _rows[id] = {
                "row": row, "state_label": state_label,
                "reason_label": reason_label, "category": category,
                "advanced": bool(control.get("advanced", false)),
                "name": _text(control.get("name")),
                "flag": _text(control.get("flag")),
        }
        return row


func _build_editor(control: Dictionary) -> Control:
        # The DATA-DRIVEN factory (inf-2's core repair): the read
        # document's own kind/forms/limits metadata builds the editor
        # — the UI never re-encodes the vocabulary. A new control
        # lands by the server's document alone.
        var id := _text(control.get("id"))
        var value_type := _text(control.get("value_type"))
        if value_type == "int" or value_type == "float":
                var spin := SpinBox.new()
                var min_value = control.get("minimum")
                var max_value = control.get("maximum")
                spin.min_value = _as_float(min_value) if min_value != null else 0.0
                spin.max_value = (
                        _as_float(max_value)
                        if max_value != null
                        else 1000000.0
                )
                spin.step = _as_float(control.get("step", 1.0))
                spin.value = _as_float(control.get("value"))
                spin.alignment = HORIZONTAL_ALIGNMENT_RIGHT
                if value_type == "int":
                        spin.step = max(1.0, floor(spin.step))
                        spin.value = float(int(_as_float(control.get("value"))))
                return spin
        if value_type == "bool":
                return _option(
                        BOOL_FORMS, _bool_text(bool(control.get("value")))
                )
        if value_type == "enum":
                var forms: Array = control.get("forms", [])
                return _option(forms, _text(control.get("value")))
        if value_type == "text":
                var edit := LineEdit.new()
                var text := _text(control.get("value"))
                edit.text = text
                edit.placeholder_text = _tr("inference.text.placeholder")
                return edit
        if value_type == "gpu_layers":
                return _build_gpu_layers_editor(control)
        return null


func _build_gpu_layers_editor(control: Dictionary) -> Control:
        # The AUTO/ALL/explicit composite (the runtime's own literal
        # forms + the count editor; 'explicit' is a UI-local mode).
        var box := HBoxContainer.new()
        box.add_theme_constant_override("separation", _k("space_s"))
        var value = control.get("value")
        var form := "explicit"
        if typeof(value) == TYPE_STRING:
                form = _text(value)
        var option := OptionButton.new()
        for item in GPU_FORMS:
                option.add_item(item)
        option.selected = GPU_FORMS.find(form) if GPU_FORMS.find(form) >= 0 else 2
        var spin := SpinBox.new()
        spin.min_value = 0.0
        spin.max_value = 999.0
        spin.step = 1.0
        spin.value = _as_float(value) if typeof(value) != TYPE_STRING else 999.0
        spin.alignment = HORIZONTAL_ALIGNMENT_RIGHT
        spin.editable = form == "explicit"
        option.item_selected.connect(func(_index: int) -> void:
                spin.editable = GPU_FORMS[option.selected] == "explicit"
        )
        box.add_child(option)
        box.add_child(spin)
        _editors["device.gpu_layers.option"] = {"editor": option}
        _editors["device.gpu_layers.spin"] = {"editor": spin}
        return box


func _option(forms: Array, current: String) -> OptionButton:
        var option := OptionButton.new()
        for item in forms:
                option.add_item(_text(item))
        var index := forms.find(current)
        option.selected = index if index >= 0 else 0
        return option


func _build_chain_region() -> Control:
        var card := PanelContainer.new()
        card.add_theme_stylebox_override("panel", _s("surface"))
        var box := VBoxContainer.new()
        box.add_theme_constant_override("separation", _k("space_xs"))
        card.add_child(box)
        var caption := Label.new()
        caption.text = _tr("inference.chain.title")
        caption.add_theme_font_size_override("font_size", _k("font_size_section_title"))
        caption.add_theme_color_override("font_color", _c("text_primary"))
        box.add_child(caption)
        var note := Label.new()
        note.text = _tr("inference.chain.note")
        note.add_theme_font_size_override("font_size", _k("font_size_caption"))
        note.add_theme_color_override("font_color", _c("text_muted"))
        note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        box.add_child(note)
        _chain_box = VBoxContainer.new()
        _chain_box.add_theme_constant_override("separation", _k("space_xs"))
        box.add_child(_chain_box)
        return card


func _build_chain_row(entry: Dictionary) -> Control:
        var id := _text(entry.get("id"))
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_s"))
        var order_label := Label.new()
        order_label.text = str(int(_as_float(entry.get("order"))) + 1) + "."
        order_label.add_theme_font_size_override("font_size", _k("font_size_body"))
        order_label.add_theme_color_override("font_color", _c("text_muted"))
        order_label.custom_minimum_size = Vector2(24.0, 0.0)
        row.add_child(order_label)
        var check := CheckBox.new()
        check.button_pressed = bool(entry.get("enabled", true))
        check.tooltip_text = _tr("inference.chain.enabled.tooltip")
        row.add_child(check)
        var name_label := Label.new()
        name_label.text = _text(entry.get("name"))
        name_label.add_theme_font_size_override("font_size", _k("font_size_body"))
        name_label.add_theme_color_override("font_color", _c("text_primary"))
        name_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        name_label.clip_text = true
        row.add_child(name_label)
        var value_label := Label.new()
        value_label.text = _value_text_of_chain_item(entry)
        value_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        value_label.add_theme_color_override("font_color", _c("text_secondary"))
        value_label.custom_minimum_size = Vector2(64.0, 0.0)
        value_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
        row.add_child(value_label)
        var state_label := Label.new()
        state_label.text = _text(entry.get("state"))
        state_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        state_label.add_theme_color_override(
                "font_color", _state_color(_text(entry.get("state")))
        )
        state_label.custom_minimum_size = Vector2(110.0, 0.0)
        state_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
        state_label.tooltip_text = _join_reasons(entry)
        row.add_child(state_label)
        var up := Button.new()
        up.text = "↑"
        up.tooltip_text = _tr("inference.chain.up")
        up.pressed.connect(_on_chain_move.bind(id, -1))
        row.add_child(up)
        var down := Button.new()
        down.text = "↓"
        down.tooltip_text = _tr("inference.chain.down")
        down.pressed.connect(_on_chain_move.bind(id, 1))
        row.add_child(down)
        _chain_rows.append(
                {"id": id, "check": check, "row": row, "order": order_label}
        )
        return row


func _build_advanced_region() -> Control:
        var box := VBoxContainer.new()
        box.add_theme_constant_override("separation", _k("space_xs"))
        _advanced_button = Button.new()
        _advanced_button.text = _tr("inference.advanced")
        _advanced_button.toggle_mode = true
        _advanced_button.pressed.connect(_on_advanced_toggled)
        box.add_child(_advanced_button)
        _advanced_box = VBoxContainer.new()
        _advanced_box.visible = false
        _advanced_box.add_theme_constant_override("separation", _k("space_xs"))
        var caption := Label.new()
        caption.text = _tr("inference.compiled.caption")
        caption.add_theme_font_size_override("font_size", _k("font_size_caption"))
        caption.add_theme_color_override("font_color", _c("text_muted"))
        caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        _advanced_box.add_child(caption)
        _preview_label = Label.new()
        _preview_label.text = ""
        _preview_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _preview_label.add_theme_color_override("font_color", _c("text_secondary"))
        _preview_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        _advanced_box.add_child(_preview_label)
        box.add_child(_advanced_box)
        return box


# ------------------------------------------------------------- population


func _populate_from_document(document: Dictionary) -> void:
        var profile: Dictionary = (
                document.get("profile", {})
                if document.get("profile") is Dictionary else {}
        )
        _profile_label.text = _tr("inference.context.profile") % _text(
                profile.get("name", "")
        )
        if bool(document.get("managed_live")):
                _applies_label.text = _tr("inference.context.applies_live")
        else:
                _applies_label.text = _tr("inference.context.applies_next")
        _pinned_ids = []
        if document.get("pinned") is Array:
                for entry in document["pinned"]:
                        _pinned_ids.append(_text(entry))
        _rebuild_library()
        _populate_presets(document)
        _rebuild_pinned_strip()
        var preview := _text(document.get("compiled_preview"))
        if preview != "":
                _preview_label.text = preview
        _status_label.text = _tr("inference.status.resolved")
        _save_button.disabled = false


func _populate_presets(document: Dictionary) -> void:
        _preset_option.clear()
        _preset_option.add_item(_tr("inference.preset.none"))
        if document.get("presets") is Array:
                for entry in document["presets"]:
                        if not (entry is Dictionary):
                                continue
                        _preset_option.add_item(_text(entry.get("name")))
        _preset_option.selected = 0
        _preset_preview_button.disabled = true
        _preset_apply_button.disabled = true
        _preset_diff_label.visible = false
        _preset_diff_label.text = ""


func _rebuild_pinned_strip() -> void:
        for child in _pinned_flow.get_children():
                _pinned_flow.remove_child(child)
                child.queue_free()
        if _pinned_ids.is_empty():
                var empty := Label.new()
                empty.text = _tr("inference.pinned.empty")
                empty.add_theme_font_size_override(
                        "font_size", _k("font_size_caption")
                )
                empty.add_theme_color_override("font_color", _c("text_muted"))
                _pinned_flow.add_child(empty)
                return
        for id in _pinned_ids:
                var row: Dictionary = _rows.get(id, {})
                if row.is_empty():
                        continue
                var chip := Button.new()
                chip.text = _pinned_chip_text(id, row)
                chip.tooltip_text = _tr("inference.pinned.chip.tooltip")
                chip.pressed.connect(_reveal_control.bind(id))
                _pinned_flow.add_child(chip)


func _pinned_chip_text(id: String, row: Dictionary) -> String:
        # The compact projection: the NAME · the live editor value ·
        # the last-read state (the chip spec §15's own inline form —
        # a quick-access glance, the edit stays in the library row).
        var state: Label = row.get("state_label", null)
        var state_text := ""
        if state != null:
                state_text = state.text
        var value := _value_text_of_editor(id)
        var name_text: String = row.get("name", id)
        if value == "":
                return "%s · %s" % [name_text, state_text]
        return "%s: %s · %s" % [name_text, value, state_text]


func _reveal_control(id: String) -> void:
        # One click: the control's category opens (the disclosure
        # honored), the advanced rung shows it if needed, and the
        # scroll lands on its row — the quick-access law.
        var row: Dictionary = _rows.get(id, {})
        if row.is_empty():
                return
        var category: String = row.get("category", "")
        if category in _category_sections:
                var section: Dictionary = _category_sections[category]
                var body: VBoxContainer = section["body"]
                if not body.visible:
                        body.visible = true
                        _category_open[category] = true
        if bool(row.get("advanced", false)) and not _advanced_check.button_pressed:
                _advanced_check.set_pressed_no_signal(true)
                _apply_advanced_visibility()
        var control_row: Control = row.get("row", null)
        if control_row == null:
                return
        var row_rect := control_row.get_global_rect()
        var scroll_rect := _scroll.get_global_rect()
        var target := int(
                _scroll.scroll_vertical + row_rect.position.y
                - scroll_rect.position.y - 8.0
        )
        _scroll.scroll_vertical = clamp(target, 0, 1000000000)


func _carry_editor_values() -> Dictionary:
        # The carried editor values law: a re-read rebuilds the rows
        # with the operator's IN-FLIGHT edits re-applied (the server's
        # read answers the SAVED profile; an edited field is a REQUEST
        # — never dropped by a refresh). The exception: the read that
        # answers OUR OWN save (the document IS the new truth).
        if _suppress_carry_once:
                _suppress_carry_once = false
                return {}
        var carried := {}
        for id in _editors.keys():
                var value = _raw_editor_value(id)
                if value != null:
                        carried[id] = value
        return carried


func _reapply_carried_values(carried: Dictionary) -> void:
        for id in carried.keys():
                if not _rows.has(id):
                        continue
                _apply_value_to_editor(id, carried[id])


# ----------------------------------------------------------- the search row


func _on_search_changed(text: String) -> void:
        _apply_search_filter()


func _apply_search_filter() -> void:
        # The §32 match families: the human name, the raw CLI name,
        # the category (the technical identifier too — substring,
        # case-insensitive). Non-matching rows hide; empty sections
        # hide; the pinned strip and the chain stay (the workspace's
        # own objects). A search MATCH is an explicit ask — it shows
        # the advanced rows too; the cleared search restores the
        # advanced rung and the disclosure states.
        var query := _search_edit.text.strip_edges().to_lower()
        var searching := query != ""
        for id in _rows.keys():
                var row: Dictionary = _rows[id]
                var control_row: Control = row.get("row", null)
                if control_row == null:
                        continue
                if not searching:
                        control_row.visible = true
                        continue
                var haystack := _row_haystack(id, row)
                control_row.visible = haystack.find(query) >= 0
        for category in _category_sections.keys():
                var section: Dictionary = _category_sections[category]
                var body: VBoxContainer = section["body"]
                var card: Control = body.get_parent().get_parent()
                if not searching:
                        card.visible = true
                        body.visible = _category_open.get(
                                category, category in DEFAULT_OPEN_CATEGORIES
                        )
                        continue
                var any_visible := false
                for child in body.get_children():
                        if child.visible:
                                any_visible = true
                                break
                card.visible = any_visible
                if any_visible:
                        body.visible = true
        if not searching:
                _apply_advanced_visibility()


func _row_haystack(id: String, row: Dictionary) -> String:
        var name_text: String = row.get("name", "")
        var flag_text: String = row.get("flag", "")
        var category: String = row.get("category", "")
        var joined := "%s %s %s %s" % [name_text, flag_text, category, id]
        return joined.to_lower()


func _on_advanced_controls_toggled(pressed: bool) -> void:
        _apply_advanced_visibility()


func _apply_advanced_visibility() -> void:
        # The progressive-disclosure rung: the expert controls stay
        # hidden until the operator asks (the §15 law — never a flat
        # 85-control wall, never hidden FOREVER).
        var show_advanced := _advanced_check.button_pressed
        for id in _rows.keys():
                var row: Dictionary = _rows[id]
                if not bool(row.get("advanced", false)):
                        continue
                var control_row: Control = row.get("row", null)
                if control_row == null:
                        continue
                control_row.visible = show_advanced
        # the search filter narrows further (the two compose)
        if _search_edit.text.strip_edges() != "":
                _apply_search_filter()


# --------------------------------------------------------------- the pins


func _on_pin_toggled(id: String) -> void:
        # The workspace's OWN save path (independent of the profile
        # values): the pin list persists immediately through the
        # update surface; the answer's feed rebuilds with the pins.
        if id in _pinned_ids:
                _pinned_ids.erase(id)
        else:
                _pinned_ids.append(id)
        _suppress_carry_once = true
        update_requested.emit({"pinned": _pinned_ids.duplicate()})


# -------------------------------------------------------------- the presets


func _on_preset_selected(_index: int) -> void:
        _preset_preview_button.disabled = _preset_option.selected == 0
        _preset_apply_button.disabled = true
        _preset_diff_label.visible = false


func _selected_preset() -> Dictionary:
        if _preset_option.selected <= 0:
                return {}
        if not (_document.get("presets") is Array):
                return {}
        var index := _preset_option.selected - 1
        if index >= _document["presets"].size():
                return {}
        var entry = _document["presets"][index]
        if not (entry is Dictionary):
                return {}
        return entry


func _preset_diff_lines(preset: Dictionary) -> Array:
        # The TRANSPARENT diff (the §14 law): every field the preset
        # would change, old value -> new value — previewed BEFORE the
        # apply, the chips stay editable after it.
        var lines: Array = []
        var profile: Dictionary = (
                _document.get("profile", {})
                if _document.get("profile") is Dictionary else {}
        )
        var values: Dictionary = preset.get("values", {})
        var names_by_field := {}
        for control in _document.get("controls", []):
                if not (control is Dictionary):
                        continue
                names_by_field[_text(control.get("field"))] = _text(
                        control.get("name")
                )
        for field in values.keys():
                var current = profile.get(field, null)
                var incoming = values[field]
                if str(current) == str(incoming):
                        continue
                var name_text: String = names_by_field.get(field, field)
                lines.append(
                        "%s: %s -> %s"
                        % [name_text, _value_text(current), _value_text(incoming)]
                )
        return lines


func _on_preset_preview() -> void:
        var preset := _selected_preset()
        if preset.is_empty():
                return
        var lines := _preset_diff_lines(preset)
        _preset_diff_label.visible = true
        if lines.is_empty():
                _preset_diff_label.text = _tr("inference.preset.diff.empty")
        else:
                _preset_diff_label.text = _tr("inference.preset.diff") % " · ".join(
                        PackedStringArray(lines)
                )
        _preset_apply_button.disabled = false


func _on_preset_apply() -> void:
        # The apply is a PLAIN update payload (the store validates;
        # the values land editable — never an opaque mode). The
        # diff stays visible until the next selection.
        var preset := _selected_preset()
        if preset.is_empty():
                return
        var values: Dictionary = preset.get("values", {})
        _suppress_carry_once = true
        update_requested.emit(values.duplicate())


# --------------------------------------------------------------- the chain


func _rebuild_chain_rows() -> void:
        for child in _chain_box.get_children():
                _chain_box.remove_child(child)
                child.queue_free()
        _chain_rows.clear()
        if not (_document.get("sampler_chain") is Array):
                return
        for entry in _document["sampler_chain"]:
                if not (entry is Dictionary):
                        continue
                _chain_box.add_child(_build_chain_row(entry))


func _on_chain_move(id: String, delta: int) -> void:
        # The ORDER is first-class: the move re-orders the emitted
        # chain (the law's §11 — an actual order change changes the
        # emitted configuration; never a cosmetic sort).
        var index := -1
        for i in range(_chain_rows.size()):
                if _text(_chain_rows[i]["id"]) == id:
                        index = i
                        break
        var target := index + delta
        if index < 0 or target < 0 or target >= _chain_rows.size():
                return
        var moved: Dictionary = _chain_rows[index]
        _chain_rows[index] = _chain_rows[target]
        _chain_rows[target] = moved
        for i in range(_chain_rows.size()):
                _chain_box.move_child(_chain_rows[i]["row"], i)
                (_chain_rows[i]["order"] as Label).text = str(i + 1) + "."


# ----------------------------------------------------------- the save path


func _on_save_pressed() -> void:
        _suppress_carry_once = true
        update_requested.emit(build_update_payload())


func build_update_payload() -> Dictionary:
        # The closed profile vocabulary (the server's own field set —
        # the whole document, never a partial guess; the store merges
        # and validates, the resolver answers with fresh states). The
        # pins are NOT part of this payload (their own save path).
        var payload: Dictionary = {}
        if _document.get("profile") is Dictionary:
                var profile: Dictionary = _document["profile"]
                payload["name"] = _text(profile.get("name", "Baseline"))
        for id in _rows.keys():
                var value = _raw_editor_value(id)
                if value == null:
                        continue
                var editors: Dictionary = _editors.get(id, {})
                var field: String = editors.get("field", "")
                if field != "":
                        payload[field] = value
        var chain: Array = []
        for row_entry in _chain_rows:
                var check: CheckBox = row_entry["check"]
                chain.append(
                        {"id": _text(row_entry["id"]), "enabled": check.button_pressed}
                )
        if not chain.is_empty():
                payload["sampler_chain"] = chain
        return payload


func _raw_editor_value(id: String):
        # The editor's CURRENT value in the SERVER's own wire type
        # (int controls read as int, floats as float, the rest as
        # their literal forms) — the request surface's honest shape.
        var entry: Dictionary = _editors.get(id, {})
        var editor = entry.get("editor")
        var value_type: String = entry.get("value_type", "")
        if value_type == "int":
                if editor is SpinBox:
                        return int((editor as SpinBox).value)
                return null
        if value_type == "float":
                if editor is SpinBox:
                        return float((editor as SpinBox).value)
                return null
        if value_type == "bool":
                if editor is OptionButton:
                        return _option_text_of(editor as OptionButton, BOOL_FORMS) == "on"
                return null
        if value_type == "enum":
                if editor is OptionButton:
                        var option: OptionButton = editor
                        var forms: Array = entry.get("forms", [])
                        if option.selected >= 0 and option.selected < forms.size():
                                return _text(forms[option.selected])
                return null
        if value_type == "text":
                if editor is LineEdit:
                        return (editor as LineEdit).text
                return null
        if value_type == "gpu_layers":
                return _gpu_layers_value()
        return null


func _gpu_layers_value():
        var option_entry: Dictionary = _editors.get("device.gpu_layers.option", {})
        var spin_entry: Dictionary = _editors.get("device.gpu_layers.spin", {})
        if option_entry.is_empty() or spin_entry.is_empty():
                return null
        var option: OptionButton = option_entry["editor"]
        var spin: SpinBox = spin_entry["editor"]
        var form: String = GPU_FORMS[option.selected]
        if form == "explicit":
                return int(spin.value)
        return form


func _value_text_of_editor(id: String) -> String:
        var value = _raw_editor_value(id)
        return _value_text(value)


func _value_text(value) -> String:
        if value == null:
                return ""
        if typeof(value) == TYPE_BOOL:
                return "on" if value else "off"
        if typeof(value) == TYPE_FLOAT and float(value) == int(value):
                return str(int(value))
        if typeof(value) == TYPE_FLOAT:
                return _trim_float(float(value))
        return _text(value)


func _apply_value_to_editor(id: String, value) -> void:
        if not _editors.has(id):
                return
        var editors: Dictionary = _editors[id]
        var editor = editors.get("editor")
        var value_type: String = editors.get("value_type", "")
        if value_type == "int" and editor is SpinBox:
                (editor as SpinBox).value = float(int(_as_float(value)))
        elif value_type == "float" and editor is SpinBox:
                (editor as SpinBox).value = _as_float(value)
        elif value_type == "bool" and editor is OptionButton:
                _select_option(
                        editor as OptionButton, BOOL_FORMS, _bool_text(bool(value))
                )
        elif value_type == "enum" and editor is OptionButton:
                var forms: Array = editors.get("forms", [])
                _select_option(editor as OptionButton, forms, _text(value))
        elif value_type == "text" and editor is LineEdit:
                (editor as LineEdit).text = _text(value)
        elif value_type == "gpu_layers":
                _apply_gpu_layers_value(value)


func _apply_gpu_layers_value(value) -> void:
        var option_entry: Dictionary = _editors.get("device.gpu_layers.option", {})
        var spin_entry: Dictionary = _editors.get("device.gpu_layers.spin", {})
        if option_entry.is_empty() or spin_entry.is_empty():
                return
        var option: OptionButton = option_entry["editor"]
        var spin: SpinBox = spin_entry["editor"]
        if typeof(value) == TYPE_STRING:
                var index := GPU_FORMS.find(_text(value))
                option.selected = index if index >= 0 else 0
                spin.editable = false
        else:
                option.selected = GPU_FORMS.find("explicit")
                spin.value = _as_float(value)
                spin.editable = true


func _select_option(option: OptionButton, forms: Array, current: String) -> void:
        var index := forms.find(current)
        option.selected = index if index >= 0 else 0


func _option_text_of(option: OptionButton, forms: Array) -> String:
        if option.selected >= 0 and option.selected < forms.size():
                return _text(forms[option.selected])
        return _text(forms[0])


# ---------------------------------------------------------------- helpers


func _category_title(category: String) -> String:
        var key := "inference.category." + category
        var title := _tr(key)
        if title == key:
                return category
        return title


func _value_text_of_chain_item(entry: Dictionary) -> String:
        var value = entry.get("value")
        if typeof(value) == TYPE_FLOAT and float(value) == int(value):
                return str(int(value))
        if typeof(value) == TYPE_FLOAT:
                return _trim_float(float(value))
        return _text(value)


func _trim_float(value: float) -> String:
        var text := "%.2f" % value
        return text.trim_suffix("0").trim_suffix(".")


func _flag_tooltip(control: Dictionary) -> String:
        # The raw mapping renders in the tooltip (the law's §1: the
        # CLI syntax is technical detail, never the primary identity).
        return _text(control.get("flag")) + " " + _text(control.get("value_doc"))


func _join_reasons(entry: Dictionary) -> String:
        var reasons = entry.get("reasons")
        if not (reasons is Array) or reasons.is_empty():
                return ""
        var parts: PackedStringArray = []
        for reason in reasons:
                parts.append(_text(reason))
        return " · ".join(parts)


func _state_color(state: String) -> Color:
        # The badge color is a SECONDARY channel (VISUAL_SYSTEM_UI §4:
        # the state text itself is the primary carrier — never
        # color-only).
        if state == "EFFECTIVE":
                return _c("status_success")
        if state == "AUTO":
                return _c("accent")
        if state == "INEFFECTIVE" or state == "INACTIVE":
                return _c("text_muted")
        return _c("text_secondary")


func _as_float(value) -> float:
        # JSON numbers parse as FLOATS (the obs-2 lesson); the int
        # rendering walks _value_text's own form.
        if typeof(value) == TYPE_FLOAT:
                return float(value)
        if typeof(value) == TYPE_INT:
                return float(value)
        return 0.0


func _bool_text(value: bool) -> String:
        return "on" if value else "off"


func _text(value) -> String:
        if typeof(value) == TYPE_STRING:
                return String(value)
        if typeof(value) == TYPE_INT:
                return str(int(value))
        if typeof(value) == TYPE_FLOAT:
                return _value_text(value)
        if typeof(value) == TYPE_BOOL:
                return _bool_text(value)
        return ""


func _tr(key: String) -> String:
        # The single translation boundary (the injected shell resolver —
        # the observatory's own law): a missing key returns the key
        # itself (visible in review, never a silently wrong string).
        if _tr_call.is_valid():
                return String(_tr_call.call(key))
        return key  # the honest fallback, the same law as the shell's own


func _c(token: String) -> Color:
        return _t.get_color(token, "Workbench")


func _k(token: String) -> int:
        return int(_t.get_constant(token, "Workbench"))


func _s(token: String) -> StyleBox:
        return _t.get_stylebox(token, "Workbench")
