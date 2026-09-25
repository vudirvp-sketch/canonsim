# CanonSim Workbench — inference.gd (inf-1: the llama.cpp semantic
# inference-control surface — the vertical slice's Redot half).
#
# LLAMA_CPP_INFERENCE_CONTROL_LAW owns the architecture; this surface
# is its UI PROJECTION (the law's §2: the UI representation is never
# the semantic authority — a chip is a semantic runtime control, the
# visual chip is ONE projection of it). The meaning, the validation
# and the effective-state resolution live in
# workbench/application/inference.py; this file only renders the
# resolved document and collects the operator's edits.
#
# What this surface IS: the semantic generation-control WORKSPACE
# (FRONTEND_UIUX_LAW §2's IA — Inference under WORK, SURFACE =
# intent, VIEW = representation). Its regions follow the LAW §3
# grammar: CONTEXT (the profile + the honest next-spawn note), the
# control LIBRARY (the semantic groups — Model/Runtime, Device,
# Memory, Sampling, Chat; progressive disclosure's later rungs grow
# from this set), the SAMPLER CHAIN (the ordered first-class object —
# never a favorites grid), and the compiled preview (the technical
# artifact, collapsed behind the advanced toggle — never the
# authoring language).
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
#     read/update document); local edits never fabricate a state —
#     after Save the fresh resolution renders
#   · the sampler chain is ORDERED (the law's §11): membership +
#     position are first-class (up/down reorder, the enabled
#     checkbox); the order changes the emitted configuration
#   · temperature 0 PRESERVES the other sampler values (the law's
#     §11: the deterministic decoding state never deletes the
#     configuration — the other rows stay visible with their
#     INEFFECTIVE reason)
#   · canonical vocabulary renders VERBATIM (the states, the raw flag
#     names in the tooltips — the not-localized set, strings.gd's own
#     law); every other user-facing string rides _tr
#
# The request surface (the shell owns the transport — zero new
# transport, the LAW's invariant): read_requested / update_requested
# answered through the public feed methods. Proof mode:
# apply_read_document() is the harness's ONLY injection point.
extends VBoxContainer


const INFERENCE_VERSION := "canon_inference@0.1"

# The request surface: the shell dispatches these over the ONE gateway
# client; the answers arrive through feed_read.
signal read_requested()
signal update_requested(payload: Dictionary)

# The gpu_layers composite's forms (the runtime's own literal values;
# 'explicit' enables the count editor — a UI-local mode, never a
# server value).
const GPU_FORMS := ["auto", "all", "explicit"]

# The semantic category order (the law's §16 — the slice's own set;
# the later capability groups grow from this ladder, never a flat
# 100+ flag surface).
const CATEGORY_ORDER := ["model", "device", "memory", "sampling", "chat"]

const KV_TYPES := [
        "f32", "f16", "bf16", "q8_0", "q4_0", "q4_1", "iq4_nl", "q5_0", "q5_1",
]
const FA_FORMS := ["auto", "on", "off"]
const FIT_FORMS := ["on", "off"]
const CHAT_TEMPLATE_FORMS := ["model_default", "generic"]

# The scalar controls this surface edits (the chain is its own region):
# id -> {min, max, step} for value controls; the mode controls carry
# their form lists above (the server's own closed vocabularies).
const VALUE_SPINS := {
        "model.context": {"min": 512.0, "max": 2097152.0, "step": 512.0},
        "sampling.temperature": {"min": 0.0, "max": 2.0, "step": 0.05},
        "sampling.top_k": {"min": 0.0, "max": 10000.0, "step": 1.0},
        "sampling.top_p": {"min": 0.0, "max": 1.0, "step": 0.01},
        "sampling.min_p": {"min": 0.0, "max": 1.0, "step": 0.01},
        "sampling.penalties": {"min": 0.0, "max": 4.0, "step": 0.05},
        "sampling.seed": {"min": -1.0, "max": 2147483647.0, "step": 1.0},
}

var _t: Theme
var _tr_call: Callable
# --- the live state (every rendered value sourced from a feed) ---
var _document: Dictionary = {}
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
var _editors: Dictionary = {}          # id -> {kind, widget(s), reason_label}
var _chain_box: VBoxContainer          # the ordered region
var _chain_rows: Array = []            # [{id, check, box}] in current order
var _chain_state_labels: Dictionary = {}  # id -> Label (the state badge)


func compose(theme: Theme, translator: Callable) -> void:
        _t = theme
        _tr_call = translator
        add_theme_constant_override("separation", _k("space_m"))
        add_child(_build_header())
        add_child(_build_context_strip())
        _scroll = ScrollContainer.new()
        _scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
        _scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
        var column := VBoxContainer.new()
        column.add_theme_constant_override("separation", _k("space_s"))
        column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _scroll.add_child(column)
        add_child(_scroll)
        for category in CATEGORY_ORDER:
                column.add_child(_build_category_group(category))
        column.add_child(_build_save_row())


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
        return card


func _build_category_group(category: String) -> Control:
        var card := PanelContainer.new()
        card.add_theme_stylebox_override("panel", _s("surface"))
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_xs"))
        card.add_child(col)
        var title := Label.new()
        title.text = _tr("inference.category." + category)
        title.add_theme_font_size_override("font_size", _k("font_size_section_title"))
        title.add_theme_color_override("font_color", _c("text_primary"))
        col.add_child(title)
        if category == "sampling":
                col.add_child(_build_chain_region())
        for control in _controls_of_category(category):
                col.add_child(_build_control_row(control))
        if category == "chat":
                # the compiled preview rides the LAST group's tail —
                # the technical artifact, collapsed by default
                col.add_child(_build_advanced_region())
        return card


func _controls_of_category(category: String) -> Array:
        var result: Array = []
        if not (_document.get("controls") is Array):
                return result
        for entry in _document["controls"]:
                if not (entry is Dictionary):
                        continue
                if _text(entry.get("category")) == category and (
                                _text(entry.get("id")) != "sampling.chain"):
                        result.append(entry)
        return result


func _build_chain_region() -> Control:
        var box := VBoxContainer.new()
        box.add_theme_constant_override("separation", _k("space_xs"))
        var caption := Label.new()
        caption.text = _tr("inference.chain.title")
        caption.add_theme_font_size_override("font_size", _k("font_size_body"))
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
        return box


func _build_control_row(control: Dictionary) -> Control:
        var id := _text(control.get("id"))
        var row := VBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_xs"))
        var line := HBoxContainer.new()
        line.add_theme_constant_override("separation", _k("space_m"))
        var name_label := Label.new()
        name_label.text = _text(control.get("name"))
        name_label.add_theme_font_size_override("font_size", _k("font_size_body"))
        name_label.add_theme_color_override("font_color", _c("text_primary"))
        name_label.tooltip_text = _flag_tooltip(control)
        name_label.custom_minimum_size = Vector2(180.0, 0.0)
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
        if _join_reasons(control) != "":
                reason_label.text = _join_reasons(control)
                reason_label.visible = true
        _editors[id] = {
                "state_label": state_label,
                "reason_label": reason_label,
                "editor": editor,
        }
        return row


func _build_editor(control: Dictionary) -> Control:
        var id := _text(control.get("id"))
        if VALUE_SPINS.has(id):
                var spin := SpinBox.new()
                var limits: Dictionary = VALUE_SPINS[id]
                spin.min_value = float(limits["min"])
                spin.max_value = float(limits["max"])
                spin.step = float(limits["step"])
                spin.value = _as_float(control.get("value"))
                spin.alignment = HORIZONTAL_ALIGNMENT_RIGHT
                return spin
        if id == "device.flash_attention":
                return _option(FA_FORMS, _text(control.get("value")))
        if id == "device.fit":
                return _option(FIT_FORMS, _text(control.get("value")))
        if id == "memory.cache_type_k" or id == "memory.cache_type_v":
                return _option(KV_TYPES, _text(control.get("value")))
        if id == "chat.template":
                return _option(CHAT_TEMPLATE_FORMS, _text(control.get("value")))
        if id == "device.gpu_layers":
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
                option.add_item(item)
        var index := forms.find(current)
        option.selected = index if index >= 0 else 0
        return option


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
        if not (_document.get("controls") is Array):
                return
        # The scalar controls: values + the resolved states + reasons.
        for entry in _document["controls"]:
                if not (entry is Dictionary):
                        continue
                var id := _text(entry.get("id"))
                if not _editors.has(id):
                        continue
                _apply_value_to_editor(id, entry.get("value"))
                var editors: Dictionary = _editors[id]
                var state_label: Label = editors["state_label"]
                state_label.text = _text(entry.get("state"))
                state_label.add_theme_color_override(
                        "font_color", _state_color(_text(entry.get("state")))
                )
                var reason_label: Label = editors["reason_label"]
                var reasons := _join_reasons(entry)
                reason_label.text = reasons
                reason_label.visible = reasons != ""
        var preview := _text(document.get("compiled_preview"))
        if preview != "":
                _preview_label.text = preview
        _rebuild_chain_rows()
        _status_label.text = _tr("inference.status.resolved")
        _save_button.disabled = false


func _apply_value_to_editor(id: String, value) -> void:
        if not _editors.has(id):
                return
        var editors: Dictionary = _editors[id]
        var editor = editors.get("editor")
        if id in VALUE_SPINS and editor is SpinBox:
                (editor as SpinBox).value = _as_float(value)
        elif id == "device.flash_attention" and editor is OptionButton:
                _select_option(editor as OptionButton, FA_FORMS, _text(value))
        elif id == "device.fit" and editor is OptionButton:
                _select_option(editor as OptionButton, FIT_FORMS, _text(value))
        elif id == "memory.cache_type_k" and editor is OptionButton:
                _select_option(editor as OptionButton, KV_TYPES, _text(value))
        elif id == "memory.cache_type_v" and editor is OptionButton:
                _select_option(editor as OptionButton, KV_TYPES, _text(value))
        elif id == "chat.template" and editor is OptionButton:
                _select_option(
                        editor as OptionButton, CHAT_TEMPLATE_FORMS, _text(value)
                )
        elif id == "device.gpu_layers":
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


func _rebuild_chain_rows() -> void:
        for child in _chain_box.get_children():
                _chain_box.remove_child(child)
                child.queue_free()
        _chain_rows.clear()
        _chain_state_labels.clear()
        if not (_document.get("sampler_chain") is Array):
                return
        for entry in _document["sampler_chain"]:
                if not (entry is Dictionary):
                        continue
                _chain_box.add_child(_build_chain_row(entry))


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
        _chain_state_labels[id] = state_label
        var up := Button.new()
        up.text = _tr("inference.chain.up")
        up.pressed.connect(_on_chain_move.bind(id, -1))
        row.add_child(up)
        var down := Button.new()
        down.text = _tr("inference.chain.down")
        down.pressed.connect(_on_chain_move.bind(id, 1))
        row.add_child(down)
        _chain_rows.append({"id": id, "check": check, "row": row, "order": order_label})
        return row


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


func _on_save_pressed() -> void:
        update_requested.emit(build_update_payload())


func build_update_payload() -> Dictionary:
        # The closed profile vocabulary (the server's own field set —
        # the whole document, never a partial guess; the store merges
        # and validates, the resolver answers with fresh states).
        var payload: Dictionary = {}
        for id in VALUE_SPINS:
                var entry: Dictionary = _editors.get(id, {})
                var editor = entry.get("editor")
                if editor is SpinBox:
                        payload[_profile_field_of(id)] = int((editor as SpinBox).value)
        payload["temperature"] = _spin_value("sampling.temperature")
        payload["top_p"] = _spin_value("sampling.top_p")
        payload["min_p"] = _spin_value("sampling.min_p")
        payload["repeat_penalty"] = _spin_value("sampling.penalties")
        payload["flash_attention"] = _option_text(
                "device.flash_attention", FA_FORMS
        )
        payload["fit"] = _option_text("device.fit", FIT_FORMS)
        payload["cache_type_k"] = _option_text("memory.cache_type_k", KV_TYPES)
        payload["cache_type_v"] = _option_text("memory.cache_type_v", KV_TYPES)
        payload["chat_template"] = _option_text(
                "chat.template", CHAT_TEMPLATE_FORMS
        )
        # the floats keep their precision (a SpinBox value is float —
        # the ints above are the count controls only)
        payload["context"] = int(_spin_value("model.context"))
        payload["top_k"] = int(_spin_value("sampling.top_k"))
        payload["seed"] = int(_spin_value("sampling.seed"))
        var option_entry: Dictionary = _editors.get("device.gpu_layers.option", {})
        var spin_entry: Dictionary = _editors.get("device.gpu_layers.spin", {})
        if not option_entry.is_empty():
                var option: OptionButton = option_entry["editor"]
                var form: String = GPU_FORMS[option.selected]
                if form == "explicit" and not spin_entry.is_empty():
                        var spin: SpinBox = spin_entry["editor"]
                        payload["gpu_layers"] = int(spin.value)
                else:
                        payload["gpu_layers"] = form
        var chain: Array = []
        for row_entry in _chain_rows:
                var check: CheckBox = row_entry["check"]
                chain.append(
                        {"id": _text(row_entry["id"]), "enabled": check.button_pressed}
                )
        payload["sampler_chain"] = chain
        if _document.get("profile") is Dictionary:
                var profile: Dictionary = _document["profile"]
                payload["name"] = _text(profile.get("name", "Baseline"))
        return payload


func _profile_field_of(control_id: String) -> String:
        # The profile field names (the server vocabulary); the float
        # family overrides below keep their precision.
        if control_id == "sampling.temperature":
                return "temperature"
        if control_id == "sampling.top_p":
                return "top_p"
        if control_id == "sampling.min_p":
                return "min_p"
        if control_id == "sampling.penalties":
                return "repeat_penalty"
        return control_id.split(".", true, 1)[1] if control_id.find(".") >= 0 else control_id


func _spin_value(id: String) -> float:
        var entry: Dictionary = _editors.get(id, {})
        var editor = entry.get("editor")
        if editor is SpinBox:
                return float((editor as SpinBox).value)
        return 0.0


func _option_text(id: String, forms: Array) -> String:
        var entry: Dictionary = _editors.get(id, {})
        var editor = entry.get("editor")
        if editor is OptionButton:
                var option: OptionButton = editor
                if option.selected >= 0 and option.selected < forms.size():
                        return _text(forms[option.selected])
        return _text(forms[0])


# ---------------------------------------------------------------- helpers


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
        # rendering walks _int_text's own form.
        if typeof(value) == TYPE_FLOAT:
                return float(value)
        if typeof(value) == TYPE_INT:
                return float(value)
        return 0.0


func _text(value) -> String:
        if typeof(value) == TYPE_STRING:
                return String(value)
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
