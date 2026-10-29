"""The dispatch log's laws (iter-402, diaglog-1 — WORKBENCH_APP_LAW
§21's redaction floor, the smallest honest increment the iter-400 audit
named: today there is NO logging at all).

The laws, each falsifiable on its own:

1. THE ONE-RECORD LAW: every `POST /op` emits exactly ONE record, and
   its `operation_id` is the ResponseDocument's own identity — the log
   is an index over dispatches, not a second truth.
2. THE REDACTION LAW: the record carries identity fields only
   (operation/status/rejection/error_type/elapsed); request bodies,
   headers, tokens and credentials never enter it — a secret-looking
   argument in the request must not appear in the file.
3. THE BOUNDED LAW: the rotation ceilings are real — the live file
   never exceeds the declared `max_bytes` and the kept-file count is
   `backups` (an unbounded append is the failure this prevents).
4. THE IDEMPOTENT-CONFIG LAW: a second configuration replaces the
   handlers this module installed (no duplicated lines, no foreign
   handler touched) — the launcher and a test can both configure.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any

import pytest

from workbench.api.dispatch_log import (
    configure_dispatch_log,
    disable_dispatch_log,
    record_dispatch,
)
from workbench.api.gateway import Gateway
from workbench.api.transport import LoopbackHttpTransport
from workbench.application.clock import AppClock


@pytest.fixture(autouse=True)
def _restore_the_silent_default() -> "Any":
    """The logger is process-global by design; every test here leaves
    it unconfigured so the rest of the suite stays silent."""
    try:
        yield
    finally:
        disable_dispatch_log()


def _post(url: str, document: Any) -> tuple[int, dict[str, Any]]:
    request = urllib.request.Request(
        url,
        data=json.dumps(document).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as opened:
        return opened.status, json.loads(opened.read())


def test_one_record_per_dispatch_with_identity_fields_only(
    tmp_path: Path,
) -> None:
    """Law 1 + 2: one line per dispatch, the response's own
    operation_id, no request payload anywhere in the file."""
    log_path = tmp_path / "logs" / "gateway.log"
    configure_dispatch_log(log_path)
    gateway = Gateway(clock=AppClock())
    transport = LoopbackHttpTransport(gateway).start()
    try:
        status, answered = _post(transport.url, {"operation": "app.status"})
        assert status == 200
        assert answered["status"] == "OK"
        rejected_status, rejected = _post(
            transport.url,
            {
                "operation": "no.such",
                "arguments": {"note": "sk-do-not-log"},
            },
        )
        assert rejected_status == 200
        assert rejected["status"] == "REJECTED"
    finally:
        transport.stop()

    lines = [
        json.loads(line)
        for line in log_path.read_text(encoding="utf-8").splitlines()
    ]
    assert len(lines) == 2, lines
    first, second = lines
    assert first["operation"] == "app.status"
    assert first["operation_id"] == answered["operation_id"]
    assert first["status"] == "OK"
    assert first["rejection"] is None
    assert first["error_type"] is None
    assert isinstance(first["elapsed_ms"], float)
    assert first["elapsed_ms"] >= 0
    assert second["operation"] == "no.such"
    assert second["status"] == "REJECTED"
    assert second["rejection"] == "DOMAIN_REJECTED"
    assert "sk-do-not-log" not in log_path.read_text(encoding="utf-8")


def test_the_rotation_ceilings_are_real(tmp_path: Path) -> None:
    """Law 3: the live file stays within max_bytes and the kept-file
    count is the declared backups — never an unbounded append."""
    log_path = tmp_path / "gateway.log"
    configure_dispatch_log(log_path, max_bytes=512, backups=1)
    for index in range(60):
        record_dispatch(
            operation=f"probe.{index}",
            operation_id=f"id-{index}",
            status="OK",
            rejection=None,
            error_type=None,
            elapsed_ms=1.0,
        )
    kept = sorted(tmp_path.glob("gateway.log*"))
    assert len(kept) == 2, kept  # the live file + exactly one backup
    for one in kept:
        assert one.stat().st_size <= 512, (one, one.stat().st_size)


def test_a_second_configuration_replaces_its_own_handlers(
    tmp_path: Path,
) -> None:
    """Law 4: configuring twice does not duplicate lines (the module's
    own handler set is replaced; a foreign handler stays untouched)."""
    first = tmp_path / "first.log"
    second = tmp_path / "second.log"
    configure_dispatch_log(first)
    configure_dispatch_log(second)
    record_dispatch(
        operation="app.status",
        operation_id="once",
        status="OK",
        rejection=None,
        error_type=None,
        elapsed_ms=0.5,
    )
    assert first.exists() is False or first.read_text(encoding="utf-8") == ""
    assert len(second.read_text(encoding="utf-8").splitlines()) == 1


def test_an_invalid_ceiling_refuses_loudly() -> None:
    """The boundedness law at construction: a zero cap or zero backups
    is a loud error, never a silently unbounded handler."""
    with pytest.raises(ValueError):
        configure_dispatch_log(Path("unused.log"), max_bytes=0)
    with pytest.raises(ValueError):
        configure_dispatch_log(Path("unused.log"), backups=0)
