"""obs-2's claim packet (FRONTEND_UIUX_LAW §25's P1 continuation —
TEST_PLAN §9's form over the Observatory read-side seam).

Claim: the Observatory's two READ operations serve BOUNDED, honest
projections of the canonical JSONL log (INV-1's append-only truth —
the same read-side edge wb-1's scene_build established):

- `observatory.runs` — the discovery scan: the sorted listing, the
  parsed header per run, the honest NO DATA for a missing root, and
  the DEGRADED entry (header=None + the observed error) for a corrupt
  first line — never a failed whole listing, never a silent skip
  (LAW §16's distinct empty semantics);
- `observatory.read` — the bounded window: the validated header, the
  after-cursor pagination over event ids (the semantic identity, LAW
  §6.2 — never a row index), the closed limit (default 50, cap 200 —
  the boundedness law's declared ceiling), the row projection's
  authority axis (CANONICAL — INV-1's truth rendered, never guessed),
  and the loud DOMAIN_REJECTED for every NOT_SENT domain violation
  (unknown run, stale cursor, corrupt log, path traversal, unknown
  argument, duplicate ids).

Lens: determinism + boundary purity — the same read answers the
identical document twice (no wall-clock, no mtime — content truths
only); the closed argument sets reject unknown members; the wire
shape is pure JSON. Prism: the real fixture log (the plumbing smoke
run — a genuine product of the canonical writer), never a
hand-crafted near-miss.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from workbench.api.contract import RequestEnvelope
from workbench.api.gateway import Gateway
from workbench.application.clock import AppClock
from workbench.application.operations.composition import (
    CompositionError,
    compose_workbench_operations,
)
from workbench.observatory_read import (
    DEFAULT_WINDOW,
    MAX_WINDOW,
    READ_PROFILE,
)

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
FIXTURE_LOG = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"


def _compose(runs_root: Path) -> Gateway:
    gateway = Gateway()
    compose_workbench_operations(
        gateway,
        runs_root.parent / "models-absent",
        AppClock(),
        observatory_runs_root=runs_root,
        observatory_schema=SCHEMA,
    )
    return gateway


def _runs(gateway: Gateway) -> dict[str, Any]:
    response = gateway.dispatch(
        RequestEnvelope(operation="observatory.runs", arguments={})
    )
    assert response.status == "OK", response.to_mapping()
    return dict(response.result)


def _read(
    gateway: Gateway,
    run: str,
    after: str = "",
    limit: int | None = None,
) -> dict[str, Any]:
    arguments: dict[str, Any] = {"run": run}
    if after:
        arguments["after"] = after
    if limit is not None:
        arguments["limit"] = limit
    response = gateway.dispatch(
        RequestEnvelope(operation="observatory.read", arguments=arguments)
    )
    assert response.status == "OK", response.to_mapping()
    return dict(response.result)


def _rejected(
    gateway: Gateway,
    operation: str,
    arguments: dict[str, Any],
    needle: str,
) -> None:
    response = gateway.dispatch(
        RequestEnvelope(operation=operation, arguments=arguments)
    )
    assert response.status == "REJECTED", response.to_mapping()
    assert response.rejection == "DOMAIN_REJECTED"
    assert needle in str(response.result), response.to_mapping()


@pytest.fixture()
def runs_root(tmp_path: Path) -> Path:
    root = tmp_path / "logs"
    root.mkdir()
    shutil.copy(FIXTURE_LOG, root / "run_42_0.jsonl")
    return root


# -- observatory.runs: the discovery scan --------------------------------


def test_runs_listing_sorted_with_parsed_headers(runs_root: Path) -> None:
    shutil.copy(FIXTURE_LOG, runs_root / "run_42_1.jsonl")
    (runs_root / "run_7_0.jsonl").write_text(
        FIXTURE_LOG.read_text(encoding="utf-8").replace('"seed": 42', '"seed": 7'),
        encoding="utf-8",
    )
    result = _runs(_compose(runs_root))
    assert [run["name"] for run in result["runs"]] == [
        "run_42_0",
        "run_42_1",
        "run_7_0",
    ]
    entry = result["runs"][0]
    assert entry["header"] == {
        "seed": 42,
        "pack": "tavern_pack@0.1",
        # derived from the schema $id (D-010) — the hand-crafted 0.2 went
        # stale at the v0.3 bump (iter-260); test_render's precedent: the
        # expectation derives, never hard-codes the version
        "schema_version": SCHEMA["$id"].rsplit("/", 1)[-1],
    }
    assert entry["error"] is None
    assert entry["size_bytes"] > 0


def test_runs_missing_root_is_honest_no_data(tmp_path: Path) -> None:
    result = _runs(_compose(tmp_path / "never-created"))
    assert result["runs"] == []
    assert result["runs_root"] == "never-created"


def test_runs_corrupt_first_line_degrades_not_fails(runs_root: Path) -> None:
    (runs_root / "run_bad_0.jsonl").write_text(
        "not json at all\n", encoding="utf-8"
    )
    (runs_root / "run_empty_0.jsonl").write_text("", encoding="utf-8")
    result = _runs(_compose(runs_root))
    by_name = {run["name"]: run for run in result["runs"]}
    assert by_name["run_bad_0"]["header"] is None
    assert "not JSON" in str(by_name["run_bad_0"]["error"])
    assert by_name["run_empty_0"]["header"] is None
    assert by_name["run_empty_0"]["error"] == "empty first line"
    # The healthy run still lists — one corrupt log never fails the scan.
    assert by_name["run_42_0"]["header"] is not None


def test_runs_takes_no_arguments(runs_root: Path) -> None:
    _rejected(
        _compose(runs_root), "observatory.runs", {"run": "run_42_0"}, "no arguments"
    )


# -- observatory.read: the bounded window ---------------------------------


def test_read_first_window_shape_and_authority(runs_root: Path) -> None:
    document = _read(_compose(runs_root), "run_42_0")
    total = document["total_events"]
    assert total == 11  # the plumbing fixture: 12 lines - the header
    assert document["run"] == "run_42_0"
    assert document["profile"] == READ_PROFILE == "CANON_VIEW"
    assert document["authority"] == "CANONICAL"
    assert document["header"]["seed"] == 42
    assert document["header"]["pack"] == "tavern_pack@0.1"
    window = document["window"]
    assert window["after"] == ""
    assert window["limit"] == DEFAULT_WINDOW
    assert window["next_after"] is None  # 11 events < the 50 default
    first = window["events"][0]
    assert first["id"] == "ev_0000"
    assert first["t"] == 0
    assert first["type"] == "world_history"
    assert first["actor"] == "world"
    assert first["authority"] == "CANONICAL"
    assert first["kind"] == "world_formed"
    assert isinstance(first["state_changes"], list)
    assert first["knowledge_count"] == 0
    assert first["provenance"]["seed"] == 42
    # A later event carries the declared cause + importance axis.
    with_cause = window["events"][1]
    assert with_cause["cause"] == "ev_0000"
    assert with_cause["importance"] in {"low", "medium", "high"}


def test_read_pagination_cursor_and_end(runs_root: Path) -> None:
    gateway = _compose(runs_root)
    page = _read(gateway, "run_42_0", limit=5)
    assert [row["id"] for row in page["window"]["events"]] == [
        f"ev_000{i}" for i in range(5)
    ]
    assert page["window"]["next_after"] == "ev_0004"
    page = _read(gateway, "run_42_0", after="ev_0004", limit=5)
    assert [row["id"] for row in page["window"]["events"]] == [
        f"ev_000{i}" for i in range(5, 10)
    ]
    assert page["window"]["next_after"] == "ev_0009"
    last = _read(gateway, "run_42_0", after="ev_0009", limit=5)
    assert [row["id"] for row in last["window"]["events"]] == ["ev_0010"]
    assert last["window"]["next_after"] is None  # the run's end, honestly


def test_read_limit_closed_set_and_cap(runs_root: Path) -> None:
    gateway = _compose(runs_root)
    assert _read(gateway, "run_42_0", limit=1)["window"]["limit"] == 1
    capped = _read(gateway, "run_42_0", limit=10_000)
    assert capped["window"]["limit"] == MAX_WINDOW == 200
    _rejected(
        gateway,
        "observatory.read",
        {"run": "run_42_0", "limit": 0},
        "positive int",
    )
    _rejected(
        gateway,
        "observatory.read",
        {"run": "run_42_0", "limit": True},
        "positive int",
    )


def test_read_unknown_argument_rejected(runs_root: Path) -> None:
    _rejected(
        _compose(runs_root),
        "observatory.read",
        {"run": "run_42_0", "cursor": "ev_0000"},
        "closed set",
    )


def test_read_unknown_run_is_no_match(runs_root: Path) -> None:
    _rejected(
        _compose(runs_root),
        "observatory.read",
        {"run": "run_999_9"},
        "NO MATCH",
    )


def test_read_stale_cursor_rejected(runs_root: Path) -> None:
    _rejected(
        _compose(runs_root),
        "observatory.read",
        {"run": "run_42_0", "after": "ev_9999"},
        "stale cursor",
    )


def test_read_traversal_and_bad_stems_rejected(runs_root: Path) -> None:
    gateway = _compose(runs_root)
    for bad in ("../fixtures/plumbing_smoke_seed42", "..", "a/b", "a.b", ".hidden"):
        _rejected(gateway, "observatory.read", {"run": bad}, "run stem")


def test_read_corrupt_event_line_loud(runs_root: Path) -> None:
    lines = FIXTURE_LOG.read_text(encoding="utf-8").splitlines()
    lines[3] = '{"id": "broken", "garbage": true}'
    (runs_root / "run_broken_0.jsonl").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    _rejected(
        _compose(runs_root),
        "observatory.read",
        {"run": "run_broken_0"},
        "failed validation",
    )


def test_read_duplicate_ids_refused(runs_root: Path) -> None:
    lines = FIXTURE_LOG.read_text(encoding="utf-8").splitlines()
    dup = json.loads(lines[2])
    dup["id"] = "ev_0000"  # collide with the first event
    lines.append(json.dumps(dup))
    (runs_root / "run_dup_0.jsonl").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    _rejected(
        _compose(runs_root),
        "observatory.read",
        {"run": "run_dup_0"},
        "duplicate event id",
    )


def test_read_header_only_run_is_distinct_no_events(runs_root: Path) -> None:
    header_line = FIXTURE_LOG.read_text(encoding="utf-8").splitlines()[0]
    (runs_root / "run_head_0.jsonl").write_text(
        header_line + "\n", encoding="utf-8"
    )
    document = _read(_compose(runs_root), "run_head_0")
    assert document["total_events"] == 0
    assert document["window"]["events"] == []
    assert document["window"]["next_after"] is None


def test_read_is_deterministic(runs_root: Path) -> None:
    gateway = _compose(runs_root)
    first = _read(gateway, "run_42_0", limit=5)
    second = _read(gateway, "run_42_0", limit=5)
    assert first == second  # no clock, no mtime — content truths only


# -- the composition wiring ----------------------------------------------


def test_composition_wires_the_observatory_family(runs_root: Path) -> None:
    gateway = _compose(runs_root)
    names = gateway.operation_names
    assert "observatory.runs" in names
    assert "observatory.read" in names


def test_composition_half_wired_refuses_loud(tmp_path: Path) -> None:
    with pytest.raises(CompositionError, match="half-wired"):
        compose_workbench_operations(
            Gateway(),
            tmp_path / "models",
            AppClock(),
            observatory_runs_root=tmp_path / "logs",
        )
    with pytest.raises(CompositionError, match="half-wired"):
        compose_workbench_operations(
            Gateway(),
            tmp_path / "models",
            AppClock(),
            observatory_schema=SCHEMA,
        )
