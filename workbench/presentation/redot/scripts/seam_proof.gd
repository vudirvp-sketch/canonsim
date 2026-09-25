# CanonSim Workbench — the wb-1 seam proof compositor (CONTRACTS.md §5 D2).
#
# What this script is: the pinned Redot 26.2 LTS presentation half of the
# vertical seam — it loads ONE Visual Scene IR document (renderer-neutral
# JSON, produced by workbench/scene_build.py), composes the placeholder
# scene FROM CODE (no hand-placed instances — the brief's agent-first law),
# captures a screenshot + writes a metadata artifact, then exits with the
# proof's terminal status.
#
# What this script is NOT: a semantic authority. It never mutates canon,
# never owns world state, never invents entities — every drawn instance
# arrives from the IR's actors/props/overlays, the semantic statuses ride
# the provenance labels untouched (CANONICAL/DERIVED/OBSERVED/UNKNOWN/
# HIDDEN/VISUAL are displayed, never collapsed).
#
# Invocation (the operator runner scripts/visual_proof.py owns the details):
#   <redot> --path <project> -- --ir <path.json> --png <path.png> --meta <path.json>
# The args after the engine's own `--` separator are user args
# (OS.get_cmdline_user_args()).
extends Node2D

const CANVAS := Vector2(1280, 720)
const ACTOR_SIZE := Vector2(64, 96)
const PROP_SIZE := Vector2(48, 48)
const LABEL_OFFSET := 22

var _ir: Dictionary = {}


func _ready() -> void:
        # KI#97/ux-1: the harness owns its coordinate space — the window is
        # pinned to the IR's declared canvas (1280x720) and content scaling
        # is disabled for the capture. The project's product stretch policy
        # (canvas_items/expand, project.godot) belongs to the SHELL window;
        # a verification harness never inherits a product resize contract —
        # the PNG stays the IR coordinate space, byte-stable.
        get_window().size = Vector2i(int(CANVAS.x), int(CANVAS.y))
        get_window().content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
        var args := OS.get_cmdline_user_args()
        var paths := _parse_args(args)
        if paths.is_empty():
                push_error("seam_proof: missing --ir/--png/--meta user args")
                get_tree().quit(2)
                return
        var text := _read_file(paths["ir"])
        if text.is_empty():
                push_error("seam_proof: cannot read IR document %s" % paths["ir"])
                get_tree().quit(2)
                return
        var parsed = JSON.parse_string(text)
        if typeof(parsed) != TYPE_DICTIONARY:
                push_error("seam_proof: IR document is not a JSON object")
                get_tree().quit(2)
                return
        _ir = parsed
        _compose()
        _capture_and_quit.call_deferred(paths)


func _parse_args(args: PackedStringArray) -> Dictionary:
        var out := {}
        var i := 0
        while i < args.size() - 1:
                match args[i]:
                        "--ir":
                                out["ir"] = args[i + 1]
                        "--png":
                                out["png"] = args[i + 1]
                        "--meta":
                                out["meta"] = args[i + 1]
                i += 1
        if out.has("ir") and out.has("png") and out.has("meta"):
                return out
        return {}


func _read_file(path: String) -> String:
        var f := FileAccess.open(path, FileAccess.READ)
        if f == null:
                return ""
        return f.get_as_text()


func _compose() -> void:
        # Layer 1: the background + floor band (purely visual, IR-declared).
        var bg_color := Color.from_string(String(_ir.get("background", {}).get("color", "#1c2128")), Color(0.11, 0.13, 0.16))
        var bg := ColorRect.new()
        bg.color = bg_color
        bg.size = CANVAS
        add_child(bg)
        var floor_band: Array = _ir.get("background", {}).get("floor_band", [0.0, 560.0, 1280.0, 160.0])
        var floor_color := Color.from_string(String(_ir.get("background", {}).get("floor_color", "#2d333b")), Color(0.18, 0.2, 0.23))
        var floor := ColorRect.new()
        floor.color = floor_color
        floor.position = Vector2(float(floor_band[0]), float(floor_band[1]))
        floor.size = Vector2(float(floor_band[2]), float(floor_band[3]))
        add_child(floor)

        # Layer 2: the props (IR order preserved — construction order is the law).
        for inst in _ir.get("props", []):
                _draw_instance(inst, PROP_SIZE)
        # Layer 3: the actors.
        for inst in _ir.get("actors", []):
                _draw_instance(inst, ACTOR_SIZE)
        # Layer 4: the overlays (debug/assurance text, IR-declared position).
        for overlay in _ir.get("overlays", []):
                var label := Label.new()
                label.text = String(overlay.get("text", ""))
                label.position = Vector2(float(overlay.get("position", [24.0, 20.0])[0]), float(overlay.get("position", [24.0, 20.0])[1]))
                label.add_theme_font_size_override("font_size", 14)
                label.add_theme_color_override("font_color", Color(0.85, 0.87, 0.9))
                add_child(label)


func _draw_instance(inst: Dictionary, size: Vector2) -> void:
        var color := Color.from_string(String(inst.get("palette_variant", "#d9a066")), Color(0.6, 0.5, 0.4))
        var rect := ColorRect.new()
        rect.color = color
        rect.position = Vector2(float(inst.get("position", [0.0, 0.0])[0]), float(inst.get("position", [0.0, 0.0])[1]))
        rect.size = size * float(inst.get("scale", 1.0))
        add_child(rect)
        # The provenance label: entity id + semantic status — displayed, never collapsed.
        var label := Label.new()
        label.text = "%s · %s" % [String(inst.get("provenance", "?")), String(inst.get("semantic_status", "?"))]
        label.position = Vector2(rect.position.x - 8.0, rect.position.y + rect.size.y + 4.0)
        label.add_theme_font_size_override("font_size", 11)
        label.add_theme_color_override("font_color", Color(0.62, 0.65, 0.7))
        add_child(label)


func _capture_and_quit(paths: Dictionary) -> void:
        await RenderingServer.frame_post_draw
        var img := get_viewport().get_texture().get_image()
        var err := img.save_png(paths["png"])
        if err != OK:
                push_error("seam_proof: cannot save PNG %s (error %d)" % [paths["png"], err])
                get_tree().quit(3)
                return
        var meta := {
                "engine_version": Engine.get_version_info().get("string", ""),
                "scene_identity": String(_ir.get("scene_identity", "")),
                "scene_ir_schema_identity": String(_ir.get("scene_ir_schema_identity", "")),
                "semantic_input_identity": String(_ir.get("semantic_input_identity", "")),
                "composition_seed": int(_ir.get("composition_seed", 0)),
                "composition_policy_version": String(_ir.get("composition_policy_version", "")),
                "asset_manifest_identity": String(_ir.get("asset_manifest_identity", "")),
                "source_revision": String(_ir.get("source_revision", "")),
                "coordinate_space": _ir.get("coordinate_space", [1280, 720]),
                "instances": {
                        "actors": _ir.get("actors", []).size(),
                        "props": _ir.get("props", []).size(),
                },
                "png": String(paths["png"]),
        }
        var mf := FileAccess.open(paths["meta"], FileAccess.WRITE)
        if mf == null:
                push_error("seam_proof: cannot write metadata %s" % paths["meta"])
                get_tree().quit(3)
                return
        mf.store_string(JSON.stringify(meta, "  ", false))
        mf.close()
        print("SEAM_PROOF_OK %s" % String(_ir.get("scene_identity", "")))
        get_tree().quit(0)
