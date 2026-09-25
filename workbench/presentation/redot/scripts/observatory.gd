# CanonSim Workbench — observatory.gd (obs-1 the slice, obs-2 the live feed).
#
# FRONTEND_UIUX_LAW §25's P1 ladder: obs-1 made the workspace grammar's
# REGIONS visible and honest (every region empty in the truthful sense);
# obs-2 feeds them — the live run over the READ-side seam
# (observatory.runs / observatory.read, the bounded read model over the
# canonical JSONL log) + the SELECTION MODEL's first consumer (LAW §6:
# select event E → the inspector opens E → the evidence view scopes to
# E → the breadcrumb carries the semantic path).
#
# What this surface IS: a projection instrument (LAW §0 — never a
# second authority, never a second transport). The shell owns the
# gateway seam; this surface owns its own composition (LAW §18 — it
# composes ITSELF over the injected theme + the shell's _tr Callable)
# and speaks ONLY through two request signals (runs_requested /
# read_requested) answered through the public feed methods.
#
# Honesty laws that govern every line below:
#   · zero fabricated content — every value rendered came from a read
#     document (INVARIANT 1/2; the empty states are DISTINCT, LAW §16:
#     probing ≠ NO RUNS ≠ NO EVENTS ≠ READ REFUSED ≠ transport failure)
#   · the selection is the semantic identity (the event id, LAW §6.2 —
#     never a row index), stable across re-reads while the id stays in
#     the window (LAW §6.1)
#   · the evidence ladder's rungs never overclaim (LAW §12: a cause_id
#     alone never implies a causal conclusion — only the READ rung is
#     "confirmed" under a selection; the rest stay "?" with their
#     honest no-verified-claim note)
#   · boundedness (LAW §39): the window rides the op's own default page
#     (50 rows, capped 200 server-side); the surface never requests
#     past the end (next_after null disables Later)
#   · canonical identifiers render VERBATIM (run stems, event ids, pack
#     ids, CANON_VIEW, CANONICAL — the not-localized set, strings.gd's
#     own law); every other user-facing string rides _tr
#
# Proof mode: `apply_read_document()` is the harness's ONLY injection
# point (LAW §43 — the runtime proof renders a REAL op-produced
# document through the same feed path the gateway serves; the
# interactive path ALWAYS rides the gateway, never a file read).
extends VBoxContainer


const OBSERVATORY_VERSION := "canon_observatory@0.2"

# The evidence ladder's rungs (LAW §12 — the statuses render as text,
# never color-only).
const EVIDENCE_RUNGS := ["read", "branch", "state", "divergence", "persistence"]

# The request surface: the shell dispatches these over the ONE gateway
# client (the seam's owner); the answers arrive through feed_runs /
# feed_read. Zero new transport (the LAW's invariant).
signal runs_requested()
signal read_requested(run: String, after: String)

# Column geometry (obs-1's precedent: raw widths until the P2 token
# expansion row gives them token names).
const COLUMN_TICK_WIDTH := 64
const COLUMN_KIND_WIDTH := 208
const COLUMN_AUTHORITY_WIDTH := 120
const PICKER_MIN_WIDTH := 220

var _t: Theme
var _tr_call: Callable
# --- the live state (every value sourced from a feed document) ---
var _run_entries: Array = []
var _current_run := ""
var _cursor_stack: PackedStringArray = []  # page cursors; [0] is "" (the head)
var _page_sizes: Array[int] = []  # rows per page, parallel to _cursor_stack
var _window: Dictionary = {}
var _selected_id := ""
var _read_pending := false
# --- widget refs ---
var _breadcrumb_label: Label
var _run_picker: OptionButton
var _refresh_button: Button
var _context_values: Dictionary = {}
var _question_fields: Dictionary = {}
var _page_status: Label
var _earlier_button: Button
var _later_button: Button
var _columns_row: Control
var _state_title: Label
var _state_note: Label
var _state_box: CenterContainer
var _rows_scroll: ScrollContainer
var _rows_box: VBoxContainer
var _inspector_title: Label
var _inspector_body: VBoxContainer
var _ladder_rows: Dictionary = {}
var _ladder_notes: Dictionary = {}


func compose(theme: Theme, translator: Callable) -> void:
        # The shell injects the theme (the token single-source) and its own
        # _tr Callable (the boundary stays ONE — this file never opens the
        # catalog directly, it speaks through the shell's resolver).
        _t = theme
        _tr_call = translator
        _cursor_stack = [""]
        _page_sizes = [0]
        add_theme_constant_override("separation", _k("space_m"))
        add_child(_build_header())
        add_child(_build_breadcrumb())
        add_child(_build_toolbar())
        add_child(_build_context_strip())
        add_child(_build_question_contract())
        add_child(_build_workspace())
        add_child(_build_evidence_ladder())


# --- the public seam (the shell's hosting surface) ------------------------


func refresh() -> void:
        # The entry action (surface entry + the Refresh button — KI#96's
        # law: no scan latch, every entry re-reads). Emits the requests;
        # the shell owns the dispatch.
        runs_requested.emit()
        if _current_run != "" and not _read_pending:
                read_requested.emit(_current_run, _after_cursor())


func feed_runs(document: Dictionary) -> void:
        # The observatory.runs answer: the runs listing. The picker
        # refreshes; the auto-load fires only when nothing is loaded (the
        # selection stability law — a loaded run never jumps on a
        # re-list).
        _run_entries = document.get("runs", [])
        _rebuild_picker()
        if _current_run == "" and not _run_entries.is_empty():
                var first_readable := _first_readable_index()
                _current_run = _entry_name(first_readable)
                _pick_in_picker(first_readable)
                _reset_position()
                _read_pending = true
                _update_action_enablement()
                read_requested.emit(_current_run, "")
        elif _current_run == "" and _run_entries.is_empty():
                _show_state("obs.empty.no_runs", "obs.empty.no_runs_note")
        elif _read_pending:
                _show_state("obs.state.probing", "obs.state.probing_note")


func feed_read(document: Dictionary) -> void:
        # The observatory.read answer: the bounded window. The context
        # strip, the rows, the pagination and the selection restore all
        # ride the ONE document.
        _read_pending = false
        _window = document
        _apply_context_strip()
        _rebuild_rows()
        _update_pagination()
        _update_action_enablement()
        _restore_selection()
        _update_breadcrumb()


func feed_rejection(reason: String) -> void:
        # A DOMAIN_REJECTED read (unknown run, stale cursor, corrupt
        # log): the honest failure — nothing fabricated, the position
        # resets to the head (LAW §21.1's recovery: the next Refresh
        # re-reads; never a stuck loop).
        _read_pending = false
        _window = {}
        _selected_id = ""
        _reset_position()
        _reset_context_strip()
        _show_state("obs.read.rejected", "obs.read.rejected_note", [reason])
        _clear_inspector()
        _clear_ladder_scoping()
        _update_pagination()
        _update_action_enablement()
        _update_breadcrumb()


func feed_transport_failure(error: String) -> void:
        # The transport's own failure (the gateway unreachable): the same
        # honest reset — the read never happened, so no window exists.
        feed_rejection(_tr("obs.read.transport") % error)


func apply_read_document(document: Dictionary, select_first_row := false) -> void:
        # The PROOF harness's injection (LAW §43): render a REAL
        # op-produced document through the same path the gateway serves.
        # The interactive path never reads files — this method exists so
        # the capture proves the loaded rendering without a network.
        _current_run = String(document.get("run", ""))
        _run_entries = [{"name": _current_run}]
        _rebuild_picker()
        _pick_in_picker(0)
        _reset_position()
        feed_read(document)
        if select_first_row and not _rows_box.get_children().is_empty():
                var first := _rows_box.get_children()[0]
                if first is Button:
                        _select_row(first, first.get_meta("row", {}))


func entry_control() -> Control:
        # The task-aware focus entry (LAW §15): the surface's primary
        # action — the Refresh (the slice's one verb).
        return _refresh_button


func note_live() -> void:
        # The shell's live-circuit note (wb-7's law): the gateway
        # answers — the entry action becomes reachable (the proof /
        # static form keeps it honestly disabled: no feed exists).
        _update_action_enablement()


# --- token + translation access (the shell's single sources) --------------


func _tr(key: String) -> String:
        if _tr_call.is_valid():
                return String(_tr_call.call(key))
        return key  # the honest fallback, the same law as the shell's own


func _int_text(value) -> String:
        # Redot 26.2's JSON law (the engine index's version firewall):
        # parse_string yields FLOATS for every number — the canonical
        # ints (seed, tick, counts) render as ints, never "42.0".
        if value is float:
                var as_int := int(value)
                if float(as_int) == value:
                        return str(as_int)
        return str(value)


func _c(token: String) -> Color:
        return _t.get_color(token, "Workbench")


func _k(token: String) -> int:
        return _t.get_constant(token, "Workbench")


func _s(token: String) -> StyleBox:
        return _t.get_stylebox(token, "Workbench")


# --- the regions (LAW §5.1) ------------------------------------------------


func _build_header() -> Control:
        var header := VBoxContainer.new()
        header.add_theme_constant_override("separation", _k("space_xs"))
        var head := Label.new()
        head.text = _tr("obs.title")
        head.add_theme_font_size_override("font_size", _k("font_size_section_title"))
        head.add_theme_color_override("font_color", _c("text_primary"))
        header.add_child(head)
        var sub := Label.new()
        sub.text = _tr("obs.subtitle")
        sub.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        sub.add_theme_color_override("font_color", _c("text_secondary"))
        sub.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        header.add_child(sub)
        return header


func _build_breadcrumb() -> Control:
        # The semantic navigation path (LAW §17: MEANING, never
        # "Screen 1 > Screen 2" — Observatory → run → the selected
        # event, each step a semantic identity, verbatim).
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_xs"))
        _breadcrumb_label = Label.new()
        _breadcrumb_label.text = _tr("obs.breadcrumb.root")
        _breadcrumb_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _breadcrumb_label.add_theme_color_override("font_color", _c("text_muted"))
        _breadcrumb_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _breadcrumb_label.clip_text = true
        row.add_child(_breadcrumb_label)
        return row


func _build_toolbar() -> Control:
        # The run picker + the refresh (the slice's one verb pair). The
        # picker is a NATIVE control (LAW §49: native where it reduces
        # friction); run stems render verbatim.
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_s"))
        var label := Label.new()
        label.text = _tr("obs.runs.label")
        label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        label.add_theme_color_override("font_color", _c("text_muted"))
        row.add_child(label)
        _run_picker = OptionButton.new()
        _run_picker.custom_minimum_size = Vector2(PICKER_MIN_WIDTH, 0)
        _run_picker.item_selected.connect(_on_run_picked)
        _run_picker.disabled = true  # no runs answered yet — the honest state
        row.add_child(_run_picker)
        _refresh_button = Button.new()
        _refresh_button.text = _tr("obs.runs.refresh")
        _refresh_button.disabled = true  # no gateway feed yet (proof/static form)
        _refresh_button.pressed.connect(refresh)
        row.add_child(_refresh_button)
        return row


func _build_context_strip() -> Control:
        # The context identity strip (LAW §42): pack · run · seed · tick
        # window · observation profile · result revision — the COMPACT
        # form; every value honest until a read answers. The canonical
        # identifiers (pack id, run stem, seed, CANON_VIEW) render
        # verbatim once loaded.
        var strip := PanelContainer.new()
        strip.add_theme_stylebox_override("panel", _s("chip"))
        var hbox := HBoxContainer.new()
        hbox.add_theme_constant_override("separation", _k("space_l"))
        strip.add_child(hbox)
        for axis in ["pack", "run", "seed", "tick", "profile", "revision"]:
                var pair := VBoxContainer.new()
                pair.add_theme_constant_override("separation", 0)
                var key_label := Label.new()
                key_label.text = _tr("obs.context." + axis)
                key_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
                key_label.add_theme_color_override("font_color", _c("text_muted"))
                pair.add_child(key_label)
                var value_label := Label.new()
                value_label.text = _tr("obs.context.no_session")
                value_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
                value_label.add_theme_color_override("font_color", _c("text_secondary"))
                pair.add_child(value_label)
                hbox.add_child(pair)
                _context_values[axis] = value_label
        return strip


func _build_question_contract() -> Control:
        # The World Question contract (LAW §51.1): QUESTION · CLASS ·
        # TARGET · SCOPE — the read-only DRAFT display. No dispatch
        # exists in the slice (the query lifecycle's DRAFT state is the
        # truth: nothing was asked, nothing is running, nothing is
        # claimed). The question EDITING form is a later row.
        var card := PanelContainer.new()
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_s"))
        card.add_child(col)
        var title_row := HBoxContainer.new()
        title_row.add_theme_constant_override("separation", _k("space_s"))
        var title := Label.new()
        title.text = _tr("obs.question.title")
        title.add_theme_font_size_override("font_size", _k("font_size_body"))
        title.add_theme_color_override("font_color", _c("text_primary"))
        title_row.add_child(title)
        var draft_chip := PanelContainer.new()
        draft_chip.add_theme_stylebox_override("panel", _s("chip"))
        var chip_row := HBoxContainer.new()
        chip_row.add_theme_constant_override("separation", _k("space_xs"))
        var chip_label := Label.new()
        chip_label.text = _tr("obs.lifecycle.draft")
        chip_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        chip_label.add_theme_color_override("font_color", _c("text_secondary"))
        chip_row.add_child(chip_label)
        draft_chip.add_child(chip_row)
        draft_chip.size_flags_vertical = Control.SIZE_SHRINK_CENTER
        title_row.add_child(draft_chip)
        var spring := Control.new()
        spring.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        title_row.add_child(spring)
        col.add_child(title_row)
        var fields := GridContainer.new()
        fields.columns = 2
        fields.add_theme_constant_override("h_separation", _k("space_l"))
        fields.add_theme_constant_override("v_separation", _k("space_xs"))
        for axis in ["question", "class", "target", "scope"]:
                var key_label := Label.new()
                key_label.text = _tr("obs.question." + axis)
                key_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
                key_label.add_theme_color_override("font_color", _c("text_muted"))
                fields.add_child(key_label)
                var value_label := Label.new()
                value_label.text = _tr("obs.question.not_set")
                value_label.add_theme_font_size_override("font_size", _k("font_size_body"))
                value_label.add_theme_color_override("font_color", _c("text_secondary"))
                value_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
                value_label.clip_text = true
                fields.add_child(value_label)
                _question_fields[axis] = value_label
        col.add_child(fields)
        return card


func _build_workspace() -> Control:
        # The workspace regions (LAW §5.1): the PRIMARY VIEW and the
        # INSPECTOR — one representation holds primary attention (the
        # event table); the inspector answers selection.
        var split := HSplitContainer.new()
        split.split_offset = 640
        split.size_flags_vertical = Control.SIZE_EXPAND_FILL
        split.add_child(_build_primary_view())
        split.add_child(_build_inspector())
        return split


func _build_primary_view() -> Control:
        # ONE primary representation (LAW §5.1): the event table. The
        # empty semantics are DISTINCT (LAW §16) and ride the state box:
        # probing / NO RUNS / NO EVENTS / READ REFUSED — never one
        # generic empty card.
        var box := VBoxContainer.new()
        box.add_theme_constant_override("separation", _k("space_xs"))
        box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        var head_row := HBoxContainer.new()
        head_row.add_theme_constant_override("separation", _k("space_s"))
        var head := Label.new()
        head.text = _tr("obs.primary.title")
        head.add_theme_font_size_override("font_size", _k("font_size_body"))
        head.add_theme_color_override("font_color", _c("text_primary"))
        head_row.add_child(head)
        var spring := Control.new()
        spring.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        head_row.add_child(spring)
        _earlier_button = Button.new()
        _earlier_button.text = _tr("obs.page.earlier")
        _earlier_button.disabled = true
        _earlier_button.pressed.connect(_on_earlier_pressed)
        head_row.add_child(_earlier_button)
        _page_status = Label.new()
        _page_status.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _page_status.add_theme_color_override("font_color", _c("text_muted"))
        head_row.add_child(_page_status)
        _later_button = Button.new()
        _later_button.text = _tr("obs.page.later")
        _later_button.disabled = true
        _later_button.pressed.connect(_on_later_pressed)
        head_row.add_child(_later_button)
        box.add_child(head_row)
        _columns_row = _build_columns_row()
        box.add_child(_columns_row)
        var rule := ColorRect.new()
        rule.color = _c("border_subtle")
        rule.custom_minimum_size = Vector2(0, 1)
        box.add_child(rule)
        # The state box (the distinct empties) and the rows (the loaded
        # window) share the space; exactly one is visible.
        _state_box = CenterContainer.new()
        _state_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
        _state_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        var state_col := VBoxContainer.new()
        state_col.add_theme_constant_override("separation", _k("space_xs"))
        _state_title = Label.new()
        _state_title.add_theme_font_size_override("font_size", _k("font_size_body"))
        _state_title.add_theme_color_override("font_color", _c("text_secondary"))
        _state_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        state_col.add_child(_state_title)
        _state_note = Label.new()
        _state_note.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _state_note.add_theme_color_override("font_color", _c("text_muted"))
        _state_note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        _state_note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        state_col.add_child(_state_note)
        _state_box.add_child(state_col)
        box.add_child(_state_box)
        _rows_scroll = ScrollContainer.new()
        _rows_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
        _rows_scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _rows_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
        _rows_box = VBoxContainer.new()
        _rows_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _rows_box.add_theme_constant_override("separation", _k("space_xs"))
        _rows_scroll.add_child(_rows_box)
        _rows_scroll.visible = false
        box.add_child(_rows_scroll)
        _show_state("obs.state.probing", "obs.state.probing_note")
        return box


func _build_columns_row() -> Control:
        # The grammar's own column vocabulary: TICK · EVENT · KIND ·
        # AUTHORITY — the authority axis rides the table itself (LAW
        # §14: the CANONICAL/OBSERVED/DERIVED/UNKNOWN dimension is
        # visible in the representation, never collapsed).
        var columns := HBoxContainer.new()
        columns.add_theme_constant_override("separation", _k("space_l"))
        for column in ["tick", "event", "kind", "authority"]:
                var col_label := Label.new()
                col_label.text = _tr("obs.column." + column)
                col_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
                col_label.add_theme_color_override("font_color", _c("text_muted"))
                if column == "tick":
                        col_label.custom_minimum_size = Vector2(COLUMN_TICK_WIDTH, 0)
                elif column == "kind":
                        col_label.custom_minimum_size = Vector2(COLUMN_KIND_WIDTH, 0)
                elif column == "authority":
                        col_label.custom_minimum_size = Vector2(COLUMN_AUTHORITY_WIDTH, 0)
                else:
                        col_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
                columns.add_child(col_label)
        return columns


func _build_inspector() -> Control:
        # The INSPECTOR region (LAW §5.1): selection details — identity,
        # relations, provenance. Empty honestly until a selection exists
        # (the selection model's first consumer, LAW §6). The body rides
        # a ScrollContainer (LAW §39's boundedness: a long event's
        # changes scroll, never clip the panel's edges).
        var box := VBoxContainer.new()
        box.add_theme_constant_override("separation", _k("space_xs"))
        box.custom_minimum_size = Vector2(360, 0)
        _inspector_title = Label.new()
        _inspector_title.text = _tr("obs.inspector.title")
        _inspector_title.add_theme_font_size_override("font_size", _k("font_size_body"))
        _inspector_title.add_theme_color_override("font_color", _c("text_primary"))
        box.add_child(_inspector_title)
        var rule := ColorRect.new()
        rule.color = _c("border_subtle")
        rule.custom_minimum_size = Vector2(0, 1)
        box.add_child(rule)
        var scroll := ScrollContainer.new()
        scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
        scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
        _inspector_body = VBoxContainer.new()
        _inspector_body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _inspector_body.add_theme_constant_override("separation", _k("space_s"))
        scroll.add_child(_inspector_body)
        box.add_child(scroll)
        _clear_inspector()
        return box


func _build_evidence_ladder() -> Control:
        # The evidence ladder as a UI primitive (LAW §12): READ → BRANCH
        # → STATE → DIVERGENCE → PERSISTENCE. Without a selection every
        # rung shows its UNKNOWN as TEXT (§13: never color-only); with a
        # selection only the READ rung is "confirmed" (the record was
        # read from the canonical log) — the rest keep their honest
        # no-verified-claim note (a cause_id alone never confirms).
        var card := PanelContainer.new()
        var col := VBoxContainer.new()
        col.add_theme_constant_override("separation", _k("space_xs"))
        card.add_child(col)
        var head := Label.new()
        head.text = _tr("obs.evidence.title")
        head.add_theme_font_size_override("font_size", _k("font_size_body"))
        head.add_theme_color_override("font_color", _c("text_primary"))
        col.add_child(head)
        for rung in EVIDENCE_RUNGS:
                var row := HBoxContainer.new()
                row.add_theme_constant_override("separation", _k("space_s"))
                var rung_label := Label.new()
                rung_label.text = _tr("obs.evidence." + rung)
                rung_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
                rung_label.add_theme_color_override("font_color", _c("text_secondary"))
                rung_label.custom_minimum_size = Vector2(160, 0)
                row.add_child(rung_label)
                var status := Label.new()
                status.text = _tr("obs.evidence.unknown")
                status.add_theme_font_size_override("font_size", _k("font_size_secondary"))
                status.add_theme_color_override("font_color", _c("text_muted"))
                status.custom_minimum_size = Vector2(120, 0)
                row.add_child(status)
                var note := Label.new()
                note.text = _tr("obs.evidence.no_claim")
                note.add_theme_font_size_override("font_size", _k("font_size_caption"))
                note.add_theme_color_override("font_color", _c("text_muted"))
                note.size_flags_horizontal = Control.SIZE_EXPAND_FILL
                note.clip_text = true
                row.add_child(note)
                col.add_child(row)
                _ladder_rows[rung] = status
                _ladder_notes[rung] = note
        return card


# --- the feeds' rendering (every value from a document) --------------------


func _rebuild_picker() -> void:
        # The picker mirrors the listing (run stems verbatim; a corrupt
        # header renders the honest unreadable suffix — the degraded
        # entry stays selectable so its read failure is observable).
        _run_picker.clear()
        for entry in _run_entries:
                var name := _entry_name_of(entry)
                var label := name
                if entry is Dictionary and entry.get("error") != null:
                        label = _tr("obs.runs.corrupt") % name
                _run_picker.add_item(label)
                _run_picker.set_item_metadata(_run_picker.item_count - 1, name)
        _run_picker.disabled = _run_entries.is_empty()


func _first_readable_index() -> int:
        # The deterministic auto-load choice: the FIRST run (sorted by
        # the listing) whose header parsed — a corrupt log is never the
        # silent default, but it stays pickable.
        for index in range(_run_entries.size()):
                var entry = _run_entries[index]
                if entry is Dictionary and entry.get("header") != null:
                        return index
        return 0


func _entry_name(index: int) -> String:
        if index >= 0 and index < _run_entries.size():
                return _entry_name_of(_run_entries[index])
        return ""


func _entry_name_of(entry) -> String:
        if entry is Dictionary:
                return String(entry.get("name", ""))
        return ""


func _pick_in_picker(index: int) -> void:
        if index >= 0 and index < _run_picker.item_count:
                _run_picker.selected = index


func _apply_context_strip() -> void:
        # The context identity (LAW §42) from the read document — the
        # canonical identifiers verbatim, the tick window and revision
        # from the window's own truths.
        if _window.is_empty():
                _reset_context_strip()
                return
        var header: Dictionary = _window.get("header", {})
        _context_values["pack"].text = String(header.get("pack", "—"))
        _context_values["run"].text = String(_window.get("run", "—"))
        _context_values["seed"].text = _int_text(header.get("seed", "—"))
        var events: Array = _window.get("window", {}).get("events", [])
        if events.is_empty():
                _context_values["tick"].text = _tr("obs.context.empty_axis")
        else:
                var min_tick := int(events[0].get("t", 0))
                var max_tick := min_tick
                for row in events:
                        var tick := int(row.get("t", 0))
                        min_tick = mini(min_tick, tick)
                        max_tick = maxi(max_tick, tick)
                _context_values["tick"].text = _tr("obs.context.tick_range") % [min_tick, max_tick]
        _context_values["profile"].text = String(_window.get("profile", ""))
        _context_values["revision"].text = _tr("obs.context.revision_format") % int(_window.get("total_events", 0))


func _reset_context_strip() -> void:
        for axis in _context_values:
                _context_values[axis].text = _tr("obs.context.no_session")


func _rebuild_rows() -> void:
        # The bounded window's rows (LAW §39: at most the op's page —
        # never an unbounded Control population). The row is a NATIVE
        # Button (keyboard-reachable, focus-visible — LAW §15/§32)
        # carrying the column labels; the selection restyles it.
        for child in _rows_box.get_children():
                child.queue_free()
        var window: Dictionary = _window.get("window", {})
        var events: Array = window.get("events", [])
        if events.is_empty():
                _rows_scroll.visible = false
                _columns_row.visible = false
                _show_state("obs.empty.no_events", "obs.empty.no_events_note")
                return
        _state_box.visible = false
        _columns_row.visible = true
        _rows_scroll.visible = true
        for row in events:
                _rows_box.add_child(_event_row(row))


func _event_row(row: Dictionary) -> Button:
        var button := Button.new()
        button.text = ""
        button.alignment = HORIZONTAL_ALIGNMENT_LEFT
        button.focus_mode = Control.FOCUS_ALL
        button.tooltip_text = "%s · %s · %s" % [
                String(row.get("id", "")),
                String(row.get("kind", "")),
                _tr("obs.inspector.tick") + " " + _int_text(row.get("t", "")),
        ]
        var columns := HBoxContainer.new()
        columns.set_anchors_preset(Control.PRESET_FULL_RECT)
        columns.offset_left = _k("space_m")
        columns.offset_right = -_k("space_m")
        columns.mouse_filter = Control.MOUSE_FILTER_IGNORE
        columns.add_theme_constant_override("separation", _k("space_l"))
        columns.add_child(_cell(_int_text(row.get("t", "")), COLUMN_TICK_WIDTH, "text_muted"))
        var event_cell := _cell(String(row.get("id", "")), 0, "text_primary")
        event_cell.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        columns.add_child(event_cell)
        columns.add_child(_cell(String(row.get("kind", "")), COLUMN_KIND_WIDTH, "text_secondary"))
        var authority_cell := _cell(String(row.get("authority", "")), COLUMN_AUTHORITY_WIDTH, "authority_canonical")
        columns.add_child(authority_cell)
        button.add_child(columns)
        button.pressed.connect(_on_row_pressed.bind(button, row))
        button.set_meta("row", row)
        return button


func _cell(text: String, min_width: int, color_token: String) -> Label:
        var label := Label.new()
        label.text = text
        label.mouse_filter = Control.MOUSE_FILTER_IGNORE
        label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        label.add_theme_color_override("font_color", _c(color_token))
        if min_width > 0:
                label.custom_minimum_size = Vector2(min_width, 0)
        label.clip_text = true
        label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
        return label


# --- the selection model (LAW §6 — the first consumer) ---------------------


func _on_row_pressed(button: Button, row: Dictionary) -> void:
        _select_row(button, row)


func _select_row(button: Button, row: Dictionary) -> void:
        # The selection is the semantic identity (the event id), carried
        # on the button's metadata — never a row index (LAW §6.2). The
        # inspector opens the event; the evidence view scopes to it
        # (LAW §6.1); the breadcrumb carries the semantic path (§17).
        _selected_id = String(row.get("id", ""))
        for child in _rows_box.get_children():
                if child is Button:
                        _style_row_as(child, child == button)
        _show_inspector(row)
        _scope_ladder(row)
        _update_breadcrumb()


func _style_row_as(button: Button, selected: bool) -> void:
        # The selected row's background arrives by TOKEN (the chip
        # stylebox — the single source); the unselected row is the
        # theme's own flat Button (its hover/pressed/focus states).
        if selected:
                button.flat = false
                button.add_theme_stylebox_override("normal", _s("chip"))
                button.add_theme_stylebox_override("hover", _s("chip"))
                button.add_theme_stylebox_override("pressed", _s("chip"))
                button.add_theme_stylebox_override("hover_pressed", _s("chip"))
        else:
                button.flat = true
                button.remove_theme_stylebox_override("normal")
                button.remove_theme_stylebox_override("hover")
                button.remove_theme_stylebox_override("pressed")
                button.remove_theme_stylebox_override("hover_pressed")


func _restore_selection() -> void:
        # LAW §6.1: the selection stays stable across re-reads while
        # the identity stays in the window — re-selected by ID, never
        # by position; an id that left the window clears honestly.
        if _selected_id == "":
                _clear_inspector()
                _clear_ladder_scoping()
                return
        for child in _rows_box.get_children():
                if child is Button:
                        var row: Dictionary = child.get_meta("row", {})
                        if String(row.get("id", "")) == _selected_id:
                                _style_row_as(child, true)
                                _show_inspector(row)
                                _scope_ladder(row)
                                return
        _selected_id = ""
        _clear_inspector()
        _clear_ladder_scoping()


func _show_inspector(row: Dictionary) -> void:
        # The selection's details (LAW §5.1): identity · the declared
        # relation · the recorded state changes (as DATA, never as
        # causal claims) · provenance. Canonical identifiers verbatim.
        for child in _inspector_body.get_children():
                child.queue_free()
        _inspector_title.text = _tr("obs.inspector.selected_title") % String(row.get("id", ""))
        var grid := GridContainer.new()
        grid.columns = 2
        grid.add_theme_constant_override("h_separation", _k("space_l"))
        grid.add_theme_constant_override("v_separation", _k("space_xs"))
        _inspector_pair(grid, "obs.inspector.id", String(row.get("id", "")))
        _inspector_pair(grid, "obs.inspector.tick", _int_text(row.get("t", "")))
        _inspector_pair(grid, "obs.inspector.type", String(row.get("type", "")))
        _inspector_pair(grid, "obs.inspector.actor", String(row.get("actor", "")))
        _inspector_pair(grid, "obs.inspector.kind", String(row.get("kind", "")))
        _inspector_pair(grid, "obs.inspector.importance", String(row.get("importance", "")))
        _inspector_pair(grid, "obs.inspector.authority", String(row.get("authority", "")))
        _inspector_body.add_child(grid)
        # JSON null is a PRESENT key with a null value — get()'s default
        # never fires (a root event's cause is null, never missing);
        # String(null) is a runtime error, so the null arm is explicit.
        var cause_value = row.get("cause", "")
        var cause := "" if cause_value == null else String(cause_value)
        if cause == "":
                _inspector_line("obs.inspector.cause", _tr("obs.inspector.cause_none"))
        else:
                _inspector_line("obs.inspector.cause", cause)
        var changes: Array = row.get("state_changes", [])
        if changes.is_empty():
                _inspector_line("obs.inspector.state_changes", _tr("obs.inspector.state_changes_none"))
        else:
                _inspector_line("obs.inspector.state_changes", " ")
                for change in changes:
                        var line := Label.new()
                        line.text = _tr("obs.inspector.state_change") % [
                                String(change.get("entity", "")),
                                String(change.get("prop", "")),
                                _value_text(change.get("from", null)),
                                _value_text(change.get("to", null)),
                        ]
                        line.add_theme_font_size_override("font_size", _k("font_size_secondary"))
                        line.add_theme_color_override("font_color", _c("text_secondary"))
                        line.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
                        line.size_flags_horizontal = Control.SIZE_EXPAND_FILL
                        _inspector_body.add_child(line)
        _inspector_line(
                "obs.inspector.knowledge", _int_text(row.get("knowledge_count", 0))
        )
        var provenance := JSON.stringify(_normalize_numbers(row.get("provenance", {})))
        _inspector_line("obs.inspector.provenance", provenance)


func _normalize_numbers(value):
        # The JSON float law's read-side arm: integer-valued floats
        # normalize back to the canonical int form BEFORE serialization
        # (the provenance renders verbatim — {"seed":42}, never 42.0).
        if value is float:
                var as_int := int(value)
                return as_int if float(as_int) == value else value
        if value is Dictionary:
                var out := {}
                for key in value:
                        out[key] = _normalize_numbers(value[key])
                return out
        if value is Array:
                var list := []
                for item in value:
                        list.append(_normalize_numbers(item))
                return list
        return value


func _value_text(value) -> String:
        # The state changes' from/to ride verbatim — a float-parsed int
        # normalizes back to its canonical int form (the JSON float law).
        if value == null:
                return "null"
        return _int_text(value)


func _inspector_pair(grid: GridContainer, key: String, value: String) -> void:
        var key_label := Label.new()
        key_label.text = _tr(key)
        key_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        key_label.add_theme_color_override("font_color", _c("text_muted"))
        grid.add_child(key_label)
        var value_label := Label.new()
        value_label.text = value
        value_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        value_label.add_theme_color_override("font_color", _c("text_secondary"))
        # The value column must EXPAND (clip_text alone yields a zero-min
        # column — the values render at width 0 and vanish; the question
        # contract's own form is the reference).
        value_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        value_label.clip_text = true
        grid.add_child(value_label)


func _inspector_line(key: String, value: String) -> void:
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_s"))
        var key_label := Label.new()
        key_label.text = _tr(key)
        key_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        key_label.add_theme_color_override("font_color", _c("text_muted"))
        key_label.custom_minimum_size = Vector2(160, 0)
        row.add_child(key_label)
        var value_label := Label.new()
        value_label.text = value
        value_label.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        value_label.add_theme_color_override("font_color", _c("text_secondary"))
        value_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        value_label.clip_text = true
        row.add_child(value_label)
        _inspector_body.add_child(row)


func _clear_inspector() -> void:
        _inspector_title.text = _tr("obs.inspector.title")
        for child in _inspector_body.get_children():
                child.queue_free()
        var note := Label.new()
        note.text = _tr("obs.inspector.nothing_selected")
        note.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        note.add_theme_color_override("font_color", _c("text_secondary"))
        note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        note.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        _inspector_body.add_child(note)


func _scope_ladder(row: Dictionary) -> void:
        # LAW §6.1's "the evidence view scopes to E": only the READ rung
        # is confirmed (the record was read from the canonical log —
        # that is what happened); BRANCH/STATE/DIVERGENCE/PERSISTENCE
        # keep "?" (no analysis layer exists — LAW §12: the declared
        # cause never confirms the branch rung by itself).
        var rung: Label = _ladder_rows["read"]
        rung.text = _tr("obs.evidence.confirmed")
        rung.add_theme_color_override("font_color", _c("status_success"))
        var note: Label = _ladder_notes["read"]
        note.text = _tr("obs.evidence.scope_note") % [
                String(_window.get("run", "")),
                String(row.get("id", "")),
        ]
        for other in ["branch", "state", "divergence", "persistence"]:
                var other_note: Label = _ladder_notes[other]
                other_note.text = _tr("obs.evidence.no_verified_claim")


func _clear_ladder_scoping() -> void:
        for rung in EVIDENCE_RUNGS:
                var status: Label = _ladder_rows[rung]
                status.text = _tr("obs.evidence.unknown")
                status.add_theme_color_override("font_color", _c("text_muted"))
                var note: Label = _ladder_notes[rung]
                note.text = _tr("obs.evidence.no_claim")


# --- pagination (the bounded window's navigation) --------------------------


func _after_cursor() -> String:
        return _cursor_stack[_cursor_stack.size() - 1]


func _reset_position() -> void:
        _cursor_stack = [""]
        _page_sizes = [0]


func _page_start_index() -> int:
        # The absolute index of the window's first row: the sum of the
        # prior pages' sizes (the cursor stack's own bookkeeping — the
        # document carries totals, not positions).
        var start := 0
        for size in _page_sizes.slice(0, _page_sizes.size() - 1):
                start += size
        return start


func _update_pagination() -> void:
        if _window.is_empty():
                _page_status.text = ""
                _earlier_button.disabled = true
                _later_button.disabled = true
                return
        var window: Dictionary = _window.get("window", {})
        var events: Array = window.get("events", [])
        var total := int(_window.get("total_events", 0))
        if events.is_empty():
                _page_status.text = _tr("obs.page.status_empty")
        else:
                var start := _page_start_index()
                _page_status.text = _tr("obs.page.status") % [
                        start + 1,
                        start + events.size(),
                        total,
                ]
        _earlier_button.disabled = _cursor_stack.size() <= 1
        _later_button.disabled = window.get("next_after", null) == null


func _update_action_enablement() -> void:
        # The in-flight guard: one read at a time (the honest pending
        # state — a second dispatch could answer out of order).
        var busy := _read_pending
        _refresh_button.disabled = busy
        _run_picker.disabled = busy or _run_entries.is_empty()
        _earlier_button.disabled = busy or _cursor_stack.size() <= 1
        if not busy and not _window.is_empty():
                var window: Dictionary = _window.get("window", {})
                _later_button.disabled = window.get("next_after", null) == null
        elif busy:
                _later_button.disabled = true


func _on_earlier_pressed() -> void:
        if _cursor_stack.size() <= 1 or _read_pending:
                return
        _cursor_stack.remove_at(_cursor_stack.size() - 1)
        _page_sizes.remove_at(_page_sizes.size() - 1)
        _read_pending = true
        _update_action_enablement()
        read_requested.emit(_current_run, _after_cursor())


func _on_later_pressed() -> void:
        if _window.is_empty() or _read_pending:
                return
        var next_after = _window.get("window", {}).get("next_after", null)
        if next_after == null:
                return
        _cursor_stack.append(String(next_after))
        _page_sizes.append(0)
        _read_pending = true
        _update_action_enablement()
        read_requested.emit(_current_run, String(next_after))


func _on_run_picked(index: int) -> void:
        # The run switch: a new semantic context — the position resets
        # to the head, the selection clears (the identity left the
        # scope, LAW §6.1's honest branch).
        var name := String(_run_picker.get_item_metadata(index))
        if name == _current_run or name == "" or _read_pending:
                return
        _current_run = name
        _selected_id = ""
        _window = {}
        _reset_position()
        _reset_context_strip()
        _clear_inspector()
        _clear_ladder_scoping()
        _read_pending = true
        _update_action_enablement()
        _update_breadcrumb()
        read_requested.emit(_current_run, "")


# --- the state box + breadcrumb -------------------------------------------


func _show_state(title_key: String, note_key: String, args: Array = []) -> void:
        # The DISTINCT empties (LAW §16): the state box replaces the
        # rows; each state carries its own title + note, never one
        # generic empty card.
        _state_box.visible = true
        _rows_scroll.visible = false
        _columns_row.visible = false
        if args.is_empty():
                _state_title.text = _tr(title_key)
        else:
                _state_title.text = _tr(title_key) % args
        _state_note.text = _tr(note_key)


func _update_breadcrumb() -> void:
        # The semantic path (LAW §17): Observatory → run → the selected
        # event — each step a semantic identity, canonical verbatim.
        var path := _tr("obs.breadcrumb.root")
        if _current_run != "":
                path += " → " + _current_run
                if _selected_id != "":
                        var kind := ""
                        for child in _rows_box.get_children():
                                if child is Button:
                                        var row: Dictionary = child.get_meta("row", {})
                                        if String(row.get("id", "")) == _selected_id:
                                                kind = String(row.get("kind", ""))
                                                break
                        if kind != "":
                                path += " → %s · %s" % [_selected_id, kind]
                        else:
                                path += " → " + _selected_id
        else:
                path += " → " + _tr("obs.breadcrumb.hint")
        _breadcrumb_label.text = path
