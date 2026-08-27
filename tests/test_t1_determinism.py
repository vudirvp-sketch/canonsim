"""T1 — determinism (minimal iter-1 form, MVP_SCOPE §14).

Same seed + same playscript + same environment = byte-identical logs, plus
RngBank fingerprint equality (the substantive draw count, RNG-1). The
committed golden fixture (`tests/fixtures/plumbing_smoke_seed42.jsonl`) is
compared byte-for-byte against a fresh run — a divergence with unchanged
schema_version is a failure. The fixture-regeneration guard (fresh tmp
regeneration diff) lands with the full T1 at iter-6
(`docs/blueprint/phase0.md` §6).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.loop import Simulator, load_playscript
from core.pack import load_pack
from core.rng import RngBank, stable_hash

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
GOLDEN = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "plumbing_smoke.json")


def run(tmp_path: Path, name: str) -> tuple[bytes, int]:
    pack = load_pack(REPO / "content" / "tavern_pack")
    sim = Simulator(pack, SCRIPT["seed"], tmp_path / name, SCHEMA, commit="0000000")
    result = sim.run_playscript(SCRIPT)
    return (tmp_path / name).read_bytes(), result.fingerprint


def test_two_runs_are_byte_identical(tmp_path: Path) -> None:
    first, fp1 = run(tmp_path, "a.jsonl")
    second, fp2 = run(tmp_path, "b.jsonl")
    assert first == second
    assert fp1 == fp2


def test_fresh_run_matches_committed_golden(tmp_path: Path) -> None:
    fresh, fingerprint = run(tmp_path, "fresh.jsonl")
    assert fresh == GOLDEN.read_bytes()
    assert fingerprint == 4  # four drawn move durations in the fixture


def test_different_seed_diverges(tmp_path: Path) -> None:
    pack = load_pack(REPO / "content" / "tavern_pack")
    other = dict(SCRIPT, seed=43)
    sim = Simulator(pack, 43, tmp_path / "other.jsonl", SCHEMA, commit="0000000")
    sim.run_playscript(other)
    assert (tmp_path / "other.jsonl").read_bytes() != GOLDEN.read_bytes()


# -- RngBank stream derivation (environment-independent) --------------------


def test_same_seed_same_streams() -> None:
    left, right = RngBank(42), RngBank(42)
    assert left.peek() == right.peek()
    assert left.peek("cosmetic") == right.peek("cosmetic")


def test_different_seed_different_streams() -> None:
    assert RngBank(42).peek() != RngBank(43).peek()


def test_stream_derivation_matches_stable_hash() -> None:
    import random

    expected = random.Random(stable_hash("42:substantive"))
    assert RngBank(42).peek() == pytest.approx(expected.random())


def test_substantive_and_cosmetic_are_distinct_streams() -> None:
    bank = RngBank(42)
    assert bank.peek() != bank.peek("cosmetic")
