"""iter-244 (ssi-3/D-224) — the topology drift-pin suite
(`scripts/topology.py --check`, the map's executable half).

The laws this suite pins (the docguard/test_architecture family's
shape, extended to the topology map): (1) the DRIFT PIN — the real
repo's map parses clean at HEAD (a future edit that adds a scope
module, drops a row, blanks an owner, or silently changes a watchlist
module's imports/emits fails HERE, in the same iteration);
(2) LINT = CI, NEVER TASTE — every violation is a named mechanical
delta between docs/SSI_TOPOLOGY.md and the ast/git derivation, never
a judgment; (3) the crafted breaches each produce exactly their
family's violation line (the tmp-doc harness: the mutated map is
compared against the REAL repo's derivation, so the delta is the
crafted breach and nothing else); (4) a missing/unparsable map is
LOUD, never a vacuous pass (N006's no-silent-skip law, the map's
form).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import topology  # type: ignore[import-not-found]  # noqa: E402

MAP_TEXT = (REPO / "docs" / "SSI_TOPOLOGY.md").read_text(encoding="utf-8")


def _write_mutated(tmp_path: Path, old: str, new: str) -> Path:
    assert old in MAP_TEXT, f"fixture anchor missing: {old[:60]!r}"
    mutated = MAP_TEXT.replace(old, new, 1)
    path = tmp_path / "SSI_TOPOLOGY.md"
    path.write_text(mutated, encoding="utf-8")
    return path


def test_map_check_clean_on_the_real_repo() -> None:
    """The drift pin: the committed map matches the HEAD derivation."""
    assert topology.run_check() == []


def test_missing_map_doc_is_loud(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(topology, "MAP_DOC", tmp_path / "absent.md")
    violations = topology.run_check()
    assert any("map table missing" in v for v in violations)


def test_dropped_row_is_loud(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        topology,
        "MAP_DOC",
        _write_mutated(
            tmp_path,
            "| core/clock.py | the tick clock (engine) | 92 | — | — | — |",
            "",
        ),
    )
    violations = topology.run_check()
    assert any(
        v == "inventory: core/clock.py on disk, no map row" for v in violations
    )


def test_stale_row_is_loud(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        topology,
        "MAP_DOC",
        _write_mutated(
            tmp_path,
            "| core/clock.py | the tick clock (engine) | 92 | — | — | — |",
            "| core/clock.py | the tick clock (engine) | 92 | — | — | — |"
            "\n| core/ghost.py | a stale row | 10 | — | — | — |",
        ),
    )
    violations = topology.run_check()
    assert any(
        v == "inventory: core/ghost.py in map, not on disk" for v in violations
    )


def test_ownerless_row_is_loud(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        topology,
        "MAP_DOC",
        _write_mutated(
            tmp_path,
            "| core/echo.py | the echo fold (knowledge stack, L6) | 130 |",
            "| core/echo.py | — | 130 |",
        ),
    )
    violations = topology.run_check()
    assert any(v == "owner: core/echo.py has no owner" for v in violations)


def test_watchlist_reads_drift_is_loud(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        topology,
        "MAP_DOC",
        _write_mutated(
            tmp_path,
            "| core/director.py | the beat decision module (DIRECTOR_SPEC) "
            "— ssi-5 target | 1419 | core/fold.py, core/ids.py, "
            "core/intent.py, core/log.py, core/pack.py, "
            "core/predicates.py | — | — |",
            "| core/director.py | the beat decision module (DIRECTOR_SPEC) "
            "— ssi-5 target | 1419 | core/fold.py | — | — |",
        ),
    )
    violations = topology.run_check()
    assert any(
        v.startswith("watchlist reads drift: core/director.py") for v in violations
    )


def test_watchlist_emits_drift_is_loud(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        topology,
        "MAP_DOC",
        _write_mutated(
            tmp_path,
            "| workbench/application/inference.py | the inference-control "
            "semantic core (LLAMA_CPP_INFERENCE_CONTROL_LAW, D-219/D-220) "
            "— ssi-4's target | 2511 | workbench/api/gateway.py | — | "
            "inference.read, inference.update |",
            "| workbench/application/inference.py | the inference-control "
            "semantic core (LLAMA_CPP_INFERENCE_CONTROL_LAW, D-219/D-220) "
            "— ssi-4's target | 2511 | workbench/api/gateway.py | — | "
            "inference.read |",
        ),
    )
    violations = topology.run_check()
    assert any(
        v.startswith("watchlist emits drift: workbench/application/inference.py")
        for v in violations
    )
