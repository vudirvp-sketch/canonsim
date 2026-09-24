"""wb-10's claim packet — the LOCAL model import (the `model.import`
work kind in `workbench/application/operations/models.py`, the owner's
2026-09-25 «просто открывающийся проводник и выбор уже скаченных
локальных моделей» call).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE ADMISSION GATES: run.start on model.import rejects BEFORE the
   run exists (NOT_SENT) — the non-array paths, the empty array, the
   relative path, the missing file, the directory-as-path, the occupied
   destination name, the `.part` residue, the duplicate names in one
   call, the unknown argument.
2. THE END-TO-END IMPORT: run.start → the run.get poll → COMPLETED —
   the LOCAL bytes landing in the models root byte-identical (the
   independent sha256 oracle), the run's result naming the file, and
   model.list discovering the file afterwards WITH the `models_root`
   field (the frontend's open-folder answer).
3. THE MULTI-FILE FORM: one run lands several files (the folder-picker
   arm's shape), the result naming each.
4. THE KIND'S OWN CHECKPOINT CONTRACT (direct work-level, the
   deterministic form over the duck-typed context): the progress
   payload's closed shape (logical_name/file_index/file_count/
   copied_bytes/total_bytes), the cooperative cancellation mid-copy
   (the checkpoint's own carrier propagates, the `.part` cleaned, no
   final file), and the partial multi-file truth (an interrupted run
   leaves the ALREADY-LANDED files in place).
5. THE COMPOSITION DEFAULT: the kind wires into the default map
   WITHOUT any fetcher (local I/O, no injection — INV-4 untouched).
"""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from workbench.api.contract import RequestEnvelope  # noqa: E402
from workbench.api.gateway import Gateway  # noqa: E402
from workbench.application.clock import AppClock  # noqa: E402
from workbench.application.operations.composition import (  # noqa: E402
    compose_workbench_operations,
)
from workbench.application.operations.execution import (  # noqa: E402
    WorkCancelled,
)
from workbench.application.operations.models import (  # noqa: E402
    IMPORT_DEFAULT_DEADLINE_SECONDS,
    ModelRegistry,
    model_import_kind,
)


def _compose(models_root: Path):
    gateway = Gateway()
    operations = compose_workbench_operations(
        gateway, models_root, AppClock()
    )
    return gateway, operations


def _direct_session(gateway: Gateway) -> str:
    response = gateway.dispatch(
        RequestEnvelope(
            operation="session.create",
            arguments={},
            client_request_id="wb10-import-session",
        )
    )
    assert response.status == "OK", response.to_mapping()
    return str(response.result["session_id"])


def _start_run(gateway: Gateway, session: str, paths: object, key: str):
    return gateway.dispatch(
        RequestEnvelope(
            operation="run.start",
            arguments={
                "work": "model.import",
                "arguments": {"paths": paths},
            },
            session_id=session,
            client_request_id=key,
        )
    )


def _await_run(gateway: Gateway, session: str, execution: str) -> dict:
    for _ in range(300):
        reply = gateway.dispatch(
            RequestEnvelope(
                operation="run.get",
                arguments={"execution_id": execution},
                session_id=session,
            )
        )
        assert reply.status == "OK", reply.to_mapping()
        result = reply.result
        if result["terminal"]:
            return dict(result)
        time.sleep(0.02)
    raise AssertionError("the import run never reached terminal")


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    hasher.update(path.read_bytes())
    return hasher.hexdigest()


# --------------------------------------------------- the admission gates


def test_the_admission_gates_reject_before_the_run_exists(
    tmp_path: Path,
) -> None:
    models = tmp_path / "models"
    models.mkdir()
    (models / "taken.gguf").write_bytes(b"here")
    (models / "inflight.gguf.part").write_bytes(b"partial")
    outside = tmp_path / "outside.gguf"
    outside.write_bytes(b"a local model")
    residue_source = tmp_path / "inflight.gguf"
    residue_source.write_bytes(b"the in-flight source")
    gone = tmp_path / "gone.gguf"
    gateway, _operations = _compose(models)
    session = _direct_session(gateway)
    cases = [
        ({"paths": "not-an-array"}, "non-empty array"),
        ({"paths": []}, "non-empty array"),
        ({"paths": [str(gone)]}, "not an existing regular file"),
        ({"paths": [str(tmp_path)]}, "not an existing regular file"),
        ({"paths": ["relative.gguf"]}, "is relative"),
        ({"paths": [str(outside), str(gone)]}, "not an existing"),
        ({"paths": [str(outside), str(outside)]}, "appears twice"),
        ({"paths": [str(models / "taken.gguf")]}, "already exists"),
        ({"paths": [str(residue_source)]}, ".part exists"),
        ({"paths": [str(outside)], "extra": 1}, "closed set"),
    ]
    for index, (arguments, fragment) in enumerate(cases):
        reply = gateway.dispatch(
            RequestEnvelope(
                operation="run.start",
                arguments={"work": "model.import", "arguments": arguments},
                session_id=session,
                client_request_id=f"wb10-gate-{index}",
            )
        )
        assert reply.status != "OK", (arguments, reply.to_mapping())
        assert reply.rejection == "DOMAIN_REJECTED", arguments
        reason = str(reply.result.get("reason"))
        assert fragment in reason, (fragment, reason)


def test_the_import_kind_deadline_is_minutes_class() -> None:
    """The kind's own §12 material input: a multi-GB LOCAL copy is
    minutes-class on a slow disk — the same 3600s band as the fetch."""
    assert IMPORT_DEFAULT_DEADLINE_SECONDS == 3600.0


def test_the_composition_wires_the_import_kind_without_a_fetcher(
    tmp_path: Path,
) -> None:
    """Local I/O needs NO injection (INV-4 untouched): the default
    composition carries model.import even with no fetcher."""
    _gateway, operations = _compose(tmp_path / "models")
    assert "model.import" in operations.work_kinds


# --------------------------------------------- the end-to-end import


def test_the_end_to_end_import_lands_the_bytes(tmp_path: Path) -> None:
    """THE wb-10 import claim: run.start model.import → the run.get
    poll → COMPLETED — the LOCAL bytes landing byte-identical (the
    independent sha256 oracle), the run's result naming the file, and
    discovery seeing it afterwards WITH the models_root field."""
    models = tmp_path / "models"
    models.mkdir()
    source = tmp_path / "downloads" / "local-model.Q4_K_M.gguf"
    source.parent.mkdir()
    payload = b"THE-LOCAL-MODEL-BYTES" * 1024
    source.write_bytes(payload)
    gateway, _operations = _compose(models)
    session = _direct_session(gateway)
    started = _start_run(gateway, session, [str(source)], "wb10-import-1")
    assert started.status == "OK", started.to_mapping()
    execution = str(started.result["execution_id"])
    terminal = _await_run(gateway, session, execution)
    assert terminal["state"] == "COMPLETED", terminal
    landed = models / "local-model.Q4_K_M.gguf"
    assert landed.is_file()
    assert _sha256(landed) == _sha256(source)
    run_result = terminal["result"]
    assert run_result["count"] == 1
    assert run_result["imported"][0]["logical_name"] == (
        "local-model.Q4_K_M.gguf"
    )
    assert run_result["imported"][0]["size_bytes"] == len(payload)
    # no residue: the .part never survives a successful landing
    assert not (models / "local-model.Q4_K_M.gguf.part").exists()
    # discovery sees it — and names the ROOT (the open-folder answer)
    listed = gateway.dispatch(
        RequestEnvelope(operation="model.list", arguments={})
    )
    assert listed.status == "OK", listed.to_mapping()
    assert listed.result["models_root"] == str(models)
    names = {
        entry["logical_name"] for entry in listed.result["models"]
    }
    assert "local-model.Q4_K_M.gguf" in names


def test_the_multi_file_form_lands_each(tmp_path: Path) -> None:
    """One run lands SEVERAL files (the folder-picker arm's shape) —
    each named in the result, each byte-identical."""
    models = tmp_path / "models"
    models.mkdir()
    sources: list[Path] = []
    for index in range(3):
        source = tmp_path / f"model-{index}.gguf"
        source.write_bytes(f"BYTES-{index}".encode() * (index + 1) * 512)
        sources.append(source)
    gateway, _operations = _compose(models)
    session = _direct_session(gateway)
    started = _start_run(
        gateway, session, [str(p) for p in sources], "wb10-import-multi"
    )
    assert started.status == "OK", started.to_mapping()
    terminal = _await_run(
        gateway, session, str(started.result["execution_id"])
    )
    assert terminal["state"] == "COMPLETED", terminal
    run_result = terminal["result"]
    assert run_result["count"] == 3
    for source in sources:
        assert (models / source.name).is_file()
        assert _sha256(models / source.name) == _sha256(source)


# ------------------------------- the kind's own checkpoint contract


class _RecordingContext:
    """The deterministic duck-typed context (the work callable's own
    contract — check/progress, nothing more): records every progress
    payload, cancels cooperatively at the Nth checkpoint (the §12
    carrier raised BY the checkpoint; the registry's own mapping to
    CANCELED is the wb-5/wb-9 packets' claim, not re-proven here)."""

    def __init__(self, cancel_at: int | None = None) -> None:
        self.progress_payloads: list[dict] = []
        self.checks = 0
        self._cancel_at = cancel_at

    def progress(self, payload: dict) -> None:
        self.progress_payloads.append(dict(payload))

    def check(self) -> None:
        self.checks += 1
        if self._cancel_at is not None and self.checks >= self._cancel_at:
            raise WorkCancelled("the cooperative cancel")


def test_the_progress_payload_is_the_closed_shape(tmp_path: Path) -> None:
    models = tmp_path / "models"
    models.mkdir()
    source = tmp_path / "one.gguf"
    payload = b"x" * 100
    source.write_bytes(payload)
    registry = ModelRegistry(models)
    kind = model_import_kind(registry, chunk_bytes=32)
    holder = _RecordingContext()
    result = kind.work(holder, {"paths": f'["{source}"]'})
    assert result["count"] == 1
    assert holder.progress_payloads, "the progress must ride the chunks"
    last = holder.progress_payloads[-1]
    assert last == {
        "logical_name": "one.gguf",
        "file_index": 0,
        "file_count": 1,
        "copied_bytes": 100,
        "total_bytes": 100,
    }
    assert holder.checks > 1, "a checkpoint per chunk, cooperative"
    assert (models / "one.gguf").read_bytes() == payload


def test_the_mid_copy_cancellation_cleans_the_part(
    tmp_path: Path,
) -> None:
    """The §12.3 truth at the kind's own boundary: the checkpoint's
    carrier propagates (never swallowed), the `.part` is cleaned, and
    NO final file lands."""
    models = tmp_path / "models"
    models.mkdir()
    source = tmp_path / "big.gguf"
    source.write_bytes(b"y" * 4096)
    registry = ModelRegistry(models)
    kind = model_import_kind(registry, chunk_bytes=64)
    holder = _RecordingContext(cancel_at=3)
    with pytest.raises(WorkCancelled):
        kind.work(holder, {"paths": f'["{source}"]'})
    assert not (models / "big.gguf").exists()
    assert not (models / "big.gguf.part").exists()


def test_the_interrupted_multi_file_run_keeps_the_landed(
    tmp_path: Path,
) -> None:
    """The honest partial arrival: cancelling during the SECOND file
    leaves the FIRST landed (a real file the next discovery scan
    sees) — never a silent rollback, never a fake completion."""
    models = tmp_path / "models"
    models.mkdir()
    first = tmp_path / "first.gguf"
    second = tmp_path / "second.gguf"
    first.write_bytes(b"a" * 256)
    second.write_bytes(b"b" * 4096)
    registry = ModelRegistry(models)
    kind = model_import_kind(registry, chunk_bytes=64)
    # let the first file complete (256/64 = 4 chunks); cancel deep
    # inside the second
    holder = _RecordingContext(cancel_at=4 + 5)
    with pytest.raises(WorkCancelled):
        kind.work(holder, {"paths": f'["{first}", "{second}"]'})
    assert (models / "first.gguf").read_bytes() == b"a" * 256
    assert not (models / "second.gguf").exists()
    assert not (models / "second.gguf.part").exists()
