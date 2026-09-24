"""wb-1's Python-half claim packet (CONTRACTS §5, TEST_PLAN §9's form).

Claim: the Visual Scene IR is a deterministic, renderer-neutral,
typed read-side projection of a committed log — same (log, pack,
location) → byte-identical JSON; the semantic statuses survive intact;
the identity closure changes when the semantic input changes.

Lens: determinism + boundary purity (status laws, identity closure).
Prism: same-input rebuild byte-diff; a truncated-log perturbation
(the identity discriminant); a cross-PYTHONHASHSEED subprocess pair
(sha256 stability, INV-2's read-side discipline — stronger than the
suite's fixed-seed default).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from core.log import LogError
from workbench.scene_build import build_scene
from workbench.scene_ir import (
    STATUSES,
    Instance,
    SceneIRError,
    instance_from_mapping,
)

REPO = Path(__file__).resolve().parents[1]
TAVERN_LOG = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
TAVERN_PACK = REPO / "content" / "tavern_pack"
PROVINCE_LOG = REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
PROVINCE_PACK = REPO / "content" / "province_pack"

FIXTURES = [
    (TAVERN_LOG, TAVERN_PACK, "loc_tavern"),
    (PROVINCE_LOG, PROVINCE_PACK, None),
]


def _build(log: Path, pack: Path, location: str | None) -> str:
    return build_scene(log, pack, location).to_json()


def test_rebuild_is_byte_identical() -> None:
    for log, pack, location in FIXTURES:
        first = _build(log, pack, location)
        second = _build(log, pack, location)
        assert first == second, f"{log.name}: IR not byte-identical on rebuild"


def test_identity_closure_present_and_sensitive() -> None:
    scene = build_scene(TAVERN_LOG, TAVERN_PACK, "loc_tavern")
    mapping = json.loads(scene.to_json())
    for key in (
        "scene_identity",
        "scene_ir_schema_identity",
        "semantic_input_identity",
        "source_revision",
        "composition_seed",
        "asset_manifest_identity",
        "composition_policy_version",
    ):
        assert mapping[key], f"identity field {key} missing/empty"
    assert mapping["scene_ir_schema_identity"] == "canon_scene_ir@0.1"
    assert "seed=42" in mapping["source_revision"]

    # The identity discriminant: a shorter log is a different semantic
    # input — identity must move (never silently reuse, CONTRACTS §5).
    lines = TAVERN_LOG.read_text(encoding="utf-8").splitlines()
    short = REPO / "tests" / "fixtures" / "_wb_short.jsonl"
    short.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
    try:
        shorter = build_scene(short, TAVERN_PACK, "loc_tavern")
        assert shorter.semantic_input_identity != scene.semantic_input_identity
        assert shorter.scene_identity != scene.scene_identity
    finally:
        short.unlink()


def test_statuses_survive_intact() -> None:
    for log, pack, location in FIXTURES:
        mapping = json.loads(_build(log, pack, location))
        instances = [*mapping["actors"], *mapping["props"]]
        assert instances, f"{log.name}: no instances to check"
        for inst in instances:
            assert inst["semantic_status"] in STATUSES
            assert inst["semantic_status"] == "CANONICAL"  # fold-known presence
            assert inst["provenance"], "entity provenance missing"
        assert mapping["background"]["semantic_status"] == "VISUAL"
        assert mapping["overlays"][0]["semantic_status"] == "DERIVED"
        # No silent UNKNOWN→ABSENT / HIDDEN→ABSENT: absent entities are
        # simply not instances (never emitted with a collapsed status).
        emitted = {inst["provenance"] for inst in instances}
        assert "" not in emitted and None not in emitted


def test_instance_roundtrip_strict() -> None:
    inst = Instance(
        asset_id="actor.silhouette",
        position=(123.5, 45.25),
        layer="actors",
        semantic_status="CANONICAL",
        provenance="npc_x",
    )
    assert instance_from_mapping(inst.to_mapping()) == inst

    drifted = dict(inst.to_mapping())
    drifted["node_path"] = "res://evil.tscn"  # renderer-type leak attempt
    with pytest.raises(SceneIRError):
        instance_from_mapping(drifted)


def test_closed_enums_reject_loudly() -> None:
    with pytest.raises(SceneIRError):
        Instance(
            asset_id="x",
            position=(0.0, 0.0),
            layer="actors",
            semantic_status="ABSENT",  # the forbidden collapse vocabulary
        )
    with pytest.raises(SceneIRError):
        Instance(
            asset_id="x",
            position=(0.0, 0.0),
            layer="SceneTree",  # renderer layer leak
            semantic_status="CANONICAL",
        )


def test_location_moves_the_composition() -> None:
    tavern = build_scene(TAVERN_LOG, TAVERN_PACK, "loc_tavern")
    street = build_scene(TAVERN_LOG, TAVERN_PACK, "loc_street")
    assert tavern.composition_seed != street.composition_seed
    assert tavern.scene_identity != street.scene_identity
    empty = build_scene(TAVERN_LOG, TAVERN_PACK, "loc_backyard")
    assert empty.actors or empty.props  # rope_01 lives there


def test_cross_hash_seed_subprocess_stability() -> None:
    """sha256 + sorted serialization: the IR bytes do not depend on
    PYTHONHASHSEED (the strongest honest determinism claim — the read
    side never rides dict-order luck)."""
    code = (
        "import sys; sys.path.insert(0, '.')\n"
        "from pathlib import Path\n"
        "from workbench.scene_build import build_scene\n"
        "scene = build_scene(Path('tests/fixtures/plumbing_smoke_seed42.jsonl'),"
        " Path('content/tavern_pack'), 'loc_tavern')\n"
        "sys.stdout.write(scene.to_json())\n"
    )
    outputs = []
    for seed_value in ("0", "1"):
        env = {**os.environ, "PYTHONHASHSEED": seed_value, "PYTHONPATH": str(REPO)}
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            cwd=REPO,
            env=env,
            check=True,
        )
        outputs.append(result.stdout)
    assert outputs[0] == outputs[1]


def test_malformed_log_fails_loudly() -> None:
    bad = REPO / "tests" / "fixtures" / "_wb_bad.jsonl"
    bad.write_text('{"header": true}\n', encoding="utf-8")
    try:
        with pytest.raises(LogError):
            build_scene(bad, TAVERN_PACK, "loc_tavern")
    finally:
        bad.unlink()
