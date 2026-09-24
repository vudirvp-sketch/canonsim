"""wb-1's Redot-half claim packet (CONTRACTS §5, TEST_PLAN §9's form).

Claim: the pinned external Redot 26.2 LTS binary, driven over the
repository project, composes the Visual Scene IR into the placeholder
scene and captures a screenshot + metadata artifact — reproducibly:
two consecutive runs in the same environment produce byte-identical
PNG and IR artifacts (the CONTRACTS §5 D4 falsifier).

Lens: determinism + artifact honesty (identity fields carried).
Prism: the double-run byte-diff over the tavern fixture.

Skip law (D6, the duckdb/D-093 pattern): without REDOT_EXE the packet
skips cleanly — CI stays engine-free, the owner/sandbox runs set
REDOT_EXE to the external toolchain binary.
"""

from __future__ import annotations

import json
import os
import struct
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TAVERN_LOG = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
TAVERN_PACK = REPO / "content" / "tavern_pack"

REDOT_EXE = os.environ.get("REDOT_EXE", "").strip()

pytestmark = pytest.mark.skipif(
    not REDOT_EXE,
    reason="REDOT_EXE not set — the Redot 26.2 LTS binary is an external "
    "toolchain (CONTRACTS §5 D1); set REDOT_EXE=<path> to run this packet",
)


def _png_size(path: Path) -> tuple[int, int]:
    """Parse the IHDR (stdlib only — no imaging dependency, D-012)."""
    raw = path.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    assert raw[12:16] == b"IHDR", "first chunk is not IHDR"
    width, height = struct.unpack(">II", raw[16:24])
    return int(width), int(height)


@pytest.fixture(scope="module")
def proof_runs(tmp_path_factory: pytest.TempPathFactory) -> list[dict[str, Path]]:
    """Two independent proof runs (fresh IR build + Redot run each)."""
    if not REDOT_EXE:
        pytest.skip("REDOT_EXE not set")
    from scripts.visual_proof import main as proof_main

    runs: list[dict[str, Path]] = []
    for index in range(2):
        out_dir = tmp_path_factory.mktemp(f"wb_proof_{index}")
        code = proof_main(
            [
                "--log",
                str(TAVERN_LOG),
                "--pack",
                str(TAVERN_PACK),
                "--location",
                "loc_tavern",
                "--out",
                str(out_dir),
            ]
        )
        assert code == 0
        runs.append(
            {
                "ir": out_dir / "ir.json",
                "png": out_dir / "proof.png",
                "meta": out_dir / "meta.json",
            }
        )
    return runs


def test_artifacts_exist_and_are_wellformed(proof_runs: list[dict[str, Path]]) -> None:
    first = proof_runs[0]
    for key in ("ir", "png", "meta"):
        assert first[key].is_file(), f"artifact {key} missing"

    meta = json.loads(first["meta"].read_text(encoding="utf-8"))
    for key in (
        "scene_identity",
        "scene_ir_schema_identity",
        "semantic_input_identity",
        "composition_seed",
        "composition_policy_version",
        "asset_manifest_identity",
        "source_revision",
        "engine_version",
        "instances",
    ):
        assert meta.get(key), f"metadata field {key} missing/empty"
    # The pinned engine line (the brief's baseline; a different binary
    # refuses loudly rather than masquerading as the pinned one).
    assert meta["engine_version"].startswith("26.2"), meta["engine_version"]
    assert meta["scene_ir_schema_identity"] == "canon_scene_ir@0.1"
    assert "seed=42" in meta["source_revision"]
    assert meta["instances"]["actors"] >= 1 and meta["instances"]["props"] >= 1

    # The scene identity must match the IR's (composition integrity).
    ir = json.loads(first["ir"].read_text(encoding="utf-8"))
    assert meta["scene_identity"] == ir["scene_identity"]

    assert _png_size(first["png"]) == (1280, 720), "PNG is not the IR coordinate space"


def test_double_run_is_byte_identical(proof_runs: list[dict[str, Path]]) -> None:
    first, second = proof_runs
    assert first["ir"].read_bytes() == second["ir"].read_bytes(), "IR differs"
    assert first["png"].read_bytes() == second["png"].read_bytes(), (
        "screenshot differs between two runs in the same environment "
        "(the CONTRACTS §5 D4 falsifier fired)"
    )
