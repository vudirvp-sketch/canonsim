# CanonSim Workbench — observatory.gd (obs-1, the P1 vertical UX slice).
#
# FRONTEND_UIUX_LAW §25's P1 + §50/§51: the Observatory's vertical slice —
# the interaction grammar validated BEFORE full analytical backend
# coverage exists. This is the responsibility-split seed (LAW §18: the
# observatory axis leaves shell.gd's composition at birth, wiring its own
# surface; the shell only hosts it).
#
# What this slice IS: the workspace grammar's REGIONS made visible and
# honest — the semantic breadcrumb, the context identity strip, the World
# Question contract (its DRAFT lifecycle state), ONE primary read-only
# view (the event table shape + the honest empty semantics), the
# inspector region, and the evidence ladder — every region EMPTY in the
# truthful sense (no session, no runs, no claims), nothing fabricated.
#
# What this slice is NOT: a dashboard (§21 — no metric grids, no charts
# without a question); a fake data showcase; a second semantic authority
# (INVARIANT 1/2: the canonical backend owns every truth; the slice shows
# its honest absence); a dispatch surface (no query is ever SENT — the
# read-only form, the DRAFT lifecycle's own law).
#
# Composition law (VISUAL_SYSTEM_UI §1): SURFACE / CONTAINER / CONTENT —
# containers exist because they establish semantic grouping, never a
# rounded box per datum; every colour/size/stylebox arrives by TOKEN name
# through the injected theme (the single source, §10); every user-facing
# string rides the injected _tr boundary (LAW §17, from birth).
extends VBoxContainer


const OBSERVATORY_VERSION := "canon_observatory@0.1"

# The evidence ladder's rungs (LAW §12 — the reusable component's own
# vocabulary; the statuses render as text, never color-only).
const EVIDENCE_RUNGS := ["read", "branch", "state", "divergence", "persistence"]

var _t: Theme
var _tr_call: Callable
var _context_strip: HBoxContainer
var _question_fields: Dictionary = {}
var _ladder_rows: Dictionary = {}
var _inspector_note: Label
var _primary_note: Label


func compose(theme: Theme, translator: Callable) -> void:
        # The shell injects the theme (the token single-source) and its own
        # _tr Callable (the boundary stays ONE — this file never opens the
        # catalog directly, it speaks through the shell's resolver).
        _t = theme
        _tr_call = translator
        add_theme_constant_override("separation", _k("space_m"))
        add_child(_build_header())
        add_child(_build_breadcrumb())
        add_child(_build_context_strip())
        add_child(_build_question_contract())
        add_child(_build_workspace())
        add_child(_build_evidence_ladder())


func _tr(key: String) -> String:
        if _tr_call.is_valid():
                return String(_tr_call.call(key))
        return key  # the honest fallback, the same law as the shell's own


func _c(token: String) -> Color:
        return _t.get_color(token, "Workbench")


func _k(token: String) -> int:
        return _t.get_constant(token, "Workbench")


func _s(token: String) -> StyleBox:
        return _t.get_stylebox(token, "Workbench")


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
        # The semantic navigation root (LAW §17: the breadcrumb carries
        # MEANING, never "Screen 1 > Screen 2" — the root is the analytical
        # context itself).
        var row := HBoxContainer.new()
        row.add_theme_constant_override("separation", _k("space_xs"))
        var root_label := Label.new()
        root_label.text = _tr("obs.breadcrumb.root")
        root_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
        root_label.add_theme_color_override("font_color", _c("text_muted"))
        row.add_child(root_label)
        var hint := Label.new()
        hint.text = _tr("obs.breadcrumb.hint")
        hint.add_theme_font_size_override("font_size", _k("font_size_caption"))
        hint.add_theme_color_override("font_color", _c("text_muted"))
        hint.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        hint.clip_text = true
        row.add_child(hint)
        return row


func _build_context_strip() -> Control:
        # The context identity strip (LAW §42): pack · run · seed · tick
        # window · observation profile · result revision — the COMPACT form;
        # every value honest ("no session") until a run actually exists.
        # Progressive disclosure: the strip is one line now; the expandable
        # detail opens when there is detail to show.
        var strip := PanelContainer.new()
        strip.add_theme_stylebox_override("panel", _s("chip"))
        _context_strip = HBoxContainer.new()
        _context_strip.add_theme_constant_override("separation", _k("space_l"))
        strip.add_child(_context_strip)
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
                _context_strip.add_child(pair)
        return strip


func _build_question_contract() -> Control:
        # The World Question contract (LAW §51.1): QUESTION · CLASS · TARGET ·
        # SCOPE — the read-only DRAFT display. No dispatch exists in the slice
        # (the query lifecycle's DRAFT state is the truth: nothing was asked,
        # nothing is running, nothing is claimed).
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
        # INSPECTOR — one representation holds primary attention (the event
        # table shape); the inspector answers selection. Read-only, bounded
        # (§20: no unbounded Control population — the empty view instantiates
        # zero rows).
        var split := HSplitContainer.new()
        split.split_offset = 640
        split.size_flags_vertical = Control.SIZE_EXPAND_FILL
        split.add_child(_build_primary_view())
        split.add_child(_build_inspector())
        return split


func _build_primary_view() -> Control:
        # ONE primary representation (LAW §5.1: exactly one holds primary
        # visual attention — the event table; timeline/compare/graph come
        # later, never simultaneously). The empty semantics are DISTINCT
        # (LAW §16): NO DATA — no run loaded, never "no match"/"no evidence".
        var box := VBoxContainer.new()
        box.add_theme_constant_override("separation", _k("space_xs"))
        box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        var head := Label.new()
        head.text = _tr("obs.primary.title")
        head.add_theme_font_size_override("font_size", _k("font_size_body"))
        head.add_theme_color_override("font_color", _c("text_primary"))
        box.add_child(head)
        var columns := HBoxContainer.new()
        columns.add_theme_constant_override("separation", _k("space_l"))
        # The grammar's own column vocabulary: TICK · EVENT · KIND ·
        # AUTHORITY — the authority axis rides the table itself (LAW §14:
        # the CANONICAL/OBSERVED/DERIVED/UNKNOWN dimension is visible in the
        # representation, never collapsed).
        for column in ["tick", "event", "kind", "authority"]:
                var col_label := Label.new()
                col_label.text = _tr("obs.column." + column)
                col_label.add_theme_font_size_override("font_size", _k("font_size_caption"))
                col_label.add_theme_color_override("font_color", _c("text_muted"))
                col_label.size_flags_horizontal = (
                        Control.SIZE_EXPAND_FILL if column == "event" else Control.SIZE_FILL
                )
                columns.add_child(col_label)
        box.add_child(columns)
        var rule := ColorRect.new()
        rule.color = _c("border_subtle")
        rule.custom_minimum_size = Vector2(0, 1)
        box.add_child(rule)
        var empty := CenterContainer.new()
        empty.size_flags_vertical = Control.SIZE_EXPAND_FILL
        empty.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        var empty_col := VBoxContainer.new()
        empty_col.add_theme_constant_override("separation", _k("space_xs"))
        var empty_title := Label.new()
        empty_title.text = _tr("obs.empty.no_data")
        empty_title.add_theme_font_size_override("font_size", _k("font_size_body"))
        empty_title.add_theme_color_override("font_color", _c("text_secondary"))
        empty_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        empty_col.add_child(empty_title)
        _primary_note = Label.new()
        _primary_note.text = _tr("obs.empty.no_data_note")
        _primary_note.add_theme_font_size_override("font_size", _k("font_size_caption"))
        _primary_note.add_theme_color_override("font_color", _c("text_muted"))
        _primary_note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        _primary_note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        empty_col.add_child(_primary_note)
        empty.add_child(empty_col)
        box.add_child(empty)
        return box


func _build_inspector() -> Control:
        # The INSPECTOR region (LAW §5.1): selection details — identity,
        # state, relations, provenance. Empty honestly: nothing is selected
        # because nothing can be selected yet (the primary view holds no
        # rows — a fabricated selection would violate the truthfulness law).
        var box := VBoxContainer.new()
        box.add_theme_constant_override("separation", _k("space_xs"))
        box.custom_minimum_size = Vector2(360, 0)
        var head := Label.new()
        head.text = _tr("obs.inspector.title")
        head.add_theme_font_size_override("font_size", _k("font_size_body"))
        head.add_theme_color_override("font_color", _c("text_primary"))
        box.add_child(head)
        var rule := ColorRect.new()
        rule.color = _c("border_subtle")
        rule.custom_minimum_size = Vector2(0, 1)
        box.add_child(rule)
        _inspector_note = Label.new()
        _inspector_note.text = _tr("obs.inspector.nothing_selected")
        _inspector_note.add_theme_font_size_override("font_size", _k("font_size_secondary"))
        _inspector_note.add_theme_color_override("font_color", _c("text_secondary"))
        _inspector_note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        _inspector_note.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        box.add_child(_inspector_note)
        var spring := Control.new()
        spring.size_flags_vertical = Control.SIZE_EXPAND_FILL
        box.add_child(spring)
        return box


func _build_evidence_ladder() -> Control:
        # The evidence ladder as a UI primitive (LAW §12): READ → BRANCH →
        # STATE → DIVERGENCE → PERSISTENCE. Every rung shows its UNKNOWN
        # status as TEXT (§13: never color-only) — no claim is under
        # inspection, so no rung is confirmed; the "?" is the truth.
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
        return card
