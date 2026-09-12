"""iter-107 — the pack authoring tools (the risk-synthesis §1 rider:
`scripts/pack_scaffold.py` + `scripts/pack_doctor.py`, the authoring
loop's first rung and its gate reader).

The loop this suite pins: scaffold (a lint-clean tavern copy, identity
renamed, SCAFFOLD.md the editing map) → edit → doctor (the lint's
fix-hint surface: file + block + rule + hint + doc, the failing
block's data with --trace; the green path prints the health
inventory). A scaffold that does not lint is a bug; a doctor that
crashes on a broken pack is worse than no doctor — the failure paths
here are crafted BROKEN packs (the crafted-twin pattern, the
travel/lint suites' family).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import pack_doctor  # type: ignore[import-not-found]  # noqa: E402
import pack_scaffold  # type: ignore[import-not-found]  # noqa: E402

from core.pack import load_pack  # noqa: E402

PACK_DIR = REPO / "content" / "tavern_pack"


# -- the scaffold --------------------------------------------------------------


def test_scaffold_lints_and_renames_identity(tmp_path: Path) -> None:
    """The scaffold is a COMPLETE lint-clean pack: the four files land,
    the identity anchor is rewritten in every meta block, and
    `load_pack` (the single admission gate) passes on the output."""
    out = tmp_path / "skeleton"
    pack_scaffold.scaffold(out, "harbor_pack")
    pack = load_pack(out)
    assert pack.name_version == "harbor_pack@0.1"
    for name in pack_scaffold.PACK_FILES:
        assert (out / name).is_file()
        text = (out / name).read_text(encoding="utf-8")
        assert '"pack": "harbor_pack"' in text, name
        assert '"pack": "tavern_pack"' not in text, name


def test_scaffold_bytes_deterministic_and_surgical(tmp_path: Path) -> None:
    """Same pack → same scaffold bytes (no wall-clock, INV-2's hygiene
    extended to authoring artifacts); and the rewrite is SURGICAL —
    every byte outside the identity anchor equals the source's."""
    left = tmp_path / "left"
    right = tmp_path / "right"
    pack_scaffold.scaffold(left, "harbor_pack")
    pack_scaffold.scaffold(right, "harbor_pack")
    for name in pack_scaffold.PACK_FILES:
        assert (left / name).read_bytes() == (right / name).read_bytes()
        assert (left / "SCAFFOLD.md").read_bytes() == (right / "SCAFFOLD.md").read_bytes()
        source = (PACK_DIR / name).read_text(encoding="utf-8")
        scaffolded = (left / name).read_text(encoding="utf-8")
        assert scaffolded == source.replace(
            '"pack": "tavern_pack"', '"pack": "harbor_pack"'
        )


def test_scaffold_refuses_non_empty_output(tmp_path: Path) -> None:
    """Never clobbers author work: an existing non-empty dir refuses
    loudly (a ValueError, not an overwrite)."""
    out = tmp_path / "occupied"
    out.mkdir()
    (out / "rules.json").write_text("{}", encoding="utf-8")
    try:
        pack_scaffold.scaffold(out, "x_pack")
    except ValueError as exc:
        assert "refuses to overwrite" in str(exc)
    else:
        raise AssertionError("the scaffold must refuse a non-empty dir")


def test_scaffold_md_maps_the_editing_surfaces(tmp_path: Path) -> None:
    """SCAFFOLD.md is derived from the pack's own data: the noun
    surfaces (the reskin's main lever), the verb labels, the armed and
    absent optional blocks (the 68a inventory), the doctor loop — the
    map an author (human or LLM) edits against."""
    out = tmp_path / "skeleton"
    pack_scaffold.scaffold(out, "harbor_pack")
    text = (out / "SCAFFOLD.md").read_text(encoding="utf-8")
    assert "harbor_pack" in text
    assert "The reskin law" in text
    assert "npcs (6)" in text  # the committed pack's noun inventory
    assert "16 verbs" in text
    assert "armed optional blocks" in text
    assert "pack_doctor" in text  # the loop's gate pointer
    assert "balance_harness" in text  # the self-check instruments


# -- the doctor ----------------------------------------------------------------


def test_doctor_green_path_health_inventory() -> None:
    """The committed pack prints its health: identity, counts, the
    per-tick systems row, the hook table, the beat axis, the armed
    optional blocks — and exits 0."""
    code = pack_doctor.main([str(PACK_DIR)])
    assert code == 0


def test_doctor_refuses_missing_and_malformed_dirs(tmp_path: Path) -> None:
    """A missing dir and a wrong file set refuse loudly before any
    world opens (the same law as the CLI's --pack gate)."""
    assert pack_doctor.main([str(tmp_path / "nowhere")]) == 1
    partial = tmp_path / "partial"
    partial.mkdir()
    (partial / "rules.json").write_text("{}", encoding="utf-8")
    assert pack_doctor.main([str(partial)]) == 1


def test_doctor_diagnoses_a_lint_failure(tmp_path: Path) -> None:
    """A crafted-broken pack (the echo block removed — the urgencies
    precondition family, the KI#77 shape) gets the structured
    diagnosis: file, block, the rule text, the fix-family hint, the
    doc owner — exit 1."""
    broken = tmp_path / "broken"
    broken.mkdir()
    for name in pack_scaffold.PACK_FILES:
        (broken / name).write_text(
            (PACK_DIR / name).read_text(encoding="utf-8"), encoding="utf-8"
        )
    rules = json.loads((broken / "rules.json").read_text(encoding="utf-8"))
    rules.pop("echo", None)
    (broken / "rules.json").write_text(
        json.dumps(rules, indent=2) + "\n", encoding="utf-8"
    )
    import contextlib
    import io

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = pack_doctor.main([str(broken)])
    assert code == 1
    text = buffer.getvalue()
    assert "FAIL rules.json · block: urgencies" in text
    assert "echo_at_least" in text  # the rule text itself
    assert "hint:" in text  # the fix family
    assert "doc:" in text  # the owner pointer
    assert "echo_at_least / trait_held / leverage_over" in text


def test_doctor_trace_dumps_the_offending_block(tmp_path: Path) -> None:
    """--trace adds the failing block's own data (the urgencies block's
    JSON) — the operator patches against the actual bytes, never a
    guess."""
    broken = tmp_path / "broken_trace"
    broken.mkdir()
    for name in pack_scaffold.PACK_FILES:
        (broken / name).write_text(
            (PACK_DIR / name).read_text(encoding="utf-8"), encoding="utf-8"
        )
    rules = json.loads((broken / "rules.json").read_text(encoding="utf-8"))
    rules.pop("echo", None)
    (broken / "rules.json").write_text(
        json.dumps(rules, indent=2) + "\n", encoding="utf-8"
    )
    import contextlib
    import io

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        assert pack_doctor.main([str(broken), "--trace"]) == 1
    text = buffer.getvalue()
    assert "data:" in text
    assert '"beat_ticks"' in text  # the urgencies block's own shape


def test_doctor_locates_the_where_shapes() -> None:
    """The locator parses every lint-message family without crashing:
    the `file::block.path` shape, the bare `block[.path]:` shape, the
    `action <id>:` / `location <id>:` shapes."""
    assert pack_doctor._locate(
        "rules.json::worldgen.chronicle.hooks names undeclared hooks"
    ) == ("rules.json", "worldgen")
    assert pack_doctor._locate(
        "urgencies.entries['npc_guard_01']: precondition echo_at_least ..."
    ) == ("rules.json", "urgencies")
    assert pack_doctor._locate("action arson: precondition layer ...") == (
        "actions.json", "action"
    )
    assert pack_doctor._locate("location loc_tavern: missing exits") == (
        "entities.json", "entities"
    )
    assert pack_doctor._locate("templates: missing fallback line") == (
        "rules.json", "templates"
    )
