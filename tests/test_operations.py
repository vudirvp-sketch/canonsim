"""wb-5's claim packet (CONTRACTS §5's wb-5 row, TEST_PLAN §9's form).

Claim: the minimal application operations (app §32 step 5) are
established over the registered surface — the §11 lifecycle
vocabularies closed with invalid-transition loudness, the §12
absolute-deadline/cancellation machinery executable, the run family
(`run.start/get/cancel`) landing the §10 artifact freeze BEFORE side
effects with §12.3's truthful cancellation, the model family's
discovery half (`model.list/inspect`) over the §16 MODELS_ASSETS
role with the §9 identity laws, and the §6.1 composition root the
single wiring owner — one real work kind (`model.digest`, §20's
computed-when-needed arm) making the execution substrate machinery
in use, not machinery awaiting a demo.

Lens: determinism + boundary purity (the closed vocabularies, the
clock never in identity, the artifact byte-stable, DOMAIN_REJECTED
for every NOT_SENT domain violation — never a §12.1 outcome).
Prism: the independent sha256 re-derivation (the digest work's
oracle); the same-input byte-diff rebuild; the cross-PYTHONHASHSEED
subprocess pair; the AST import-edge scan over the package.
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

import pytest

from workbench.api.contract import RequestEnvelope, ResponseDocument
from workbench.api.gateway import (
    Gateway,
    GatewayError,
    OperationRejected,
    OperationSpec,
)
from workbench.api.transport import LoopbackHttpTransport
from workbench.application.clock import AppClock
from workbench.application.operations import composition
from workbench.application.operations.composition import (
    WorkbenchOperations,
    WorkKind,
    compose_workbench_operations,
)
from workbench.application.operations.execution import (
    CancellationToken,
    DeadlineExceeded,
    ExecutionRegistry,
    ExecutionRegistryConfig,
    OperationDeadline,
    RegistryError,
    WorkCancelled,
    WorkContext,
)
from workbench.application.operations.lifecycles import (
    APPLICATION_STATES,
    BACKEND_STATES,
    EXECUTION_STATES,
    INITIAL_STATES,
    LIFECYCLE_DOMAINS,
    LIFECYCLE_STATES,
    MODEL_STATES,
    TERMINAL_STATES,
    LifecycleError,
    is_terminal,
    legal_transitions,
    states,
    transition,
)
from workbench.application.operations.models import (
    DEFAULT_CHUNK_BYTES,
    DISCOVERY_STATE,
    ModelRegistry,
    ModelRegistryError,
)

REPO = Path(__file__).resolve().parents[1]


class _StepClock:
    """The deterministic clock double (wb-3/wb-4's pattern): both
    domains step only when the test moves them."""

    def __init__(self) -> None:
        self._mono = 100.0
        self._utc = 1000.0

    def monotonic(self) -> float:
        return self._mono

    def utc(self) -> float:
        return self._utc

    def step(self, seconds: float) -> None:
        self._mono += seconds
        self._utc += seconds


def _fixed_clock() -> tuple[AppClock, _StepClock]:
    step = _StepClock()
    return AppClock(monotonic=step.monotonic, utc=step.utc), step


def _compose(
    tmp_path: Path,
    clock: AppClock | None = None,
    work_kinds: dict[str, WorkKind] | None = None,
    registry_config: ExecutionRegistryConfig | None = None,
) -> tuple[Gateway, WorkbenchOperations]:
    """The smaller-composition pattern (§6.1's own law): a fresh
    gateway + the workbench operations over a tmp MODELS_ASSETS
    root."""
    if clock is None:
        clock, _ = _fixed_clock()
    gateway = Gateway(clock=clock)
    root = tmp_path / "models"
    root.mkdir(parents=True, exist_ok=True)
    ops = compose_workbench_operations(
        gateway,
        root,
        clock,
        work_kinds=work_kinds,
        registry_config=registry_config,
    )
    return gateway, ops


def _session(gateway: Gateway, key: str = "session-key-1") -> str:
    response = gateway.dispatch(
        RequestEnvelope(
            operation="session.create",
            arguments={},
            client_request_id=key,
        )
    )
    assert response.status == "OK", response.to_mapping()
    return str(response.result["session_id"])


def _run_start(
    gateway: Gateway,
    session_id: str,
    key: str,
    work: str,
    arguments: dict[str, Any],
    deadline_seconds: float | None = None,
) -> ResponseDocument:
    payload: dict[str, Any] = {"work": work, "arguments": arguments}
    if deadline_seconds is not None:
        payload["deadline_seconds"] = deadline_seconds
    return gateway.dispatch(
        RequestEnvelope(
            operation="run.start",
            arguments=payload,
            client_request_id=key,
            session_id=session_id,
        )
    )


def _run_get(
    gateway: Gateway, session_id: str, execution_id: str
) -> ResponseDocument:
    return gateway.dispatch(
        RequestEnvelope(
            operation="run.get",
            arguments={"execution_id": execution_id},
            session_id=session_id,
        )
    )


def _run_cancel(
    gateway: Gateway, session_id: str, execution_id: str, key: str
) -> ResponseDocument:
    return gateway.dispatch(
        RequestEnvelope(
            operation="run.cancel",
            arguments={"execution_id": execution_id},
            client_request_id=key,
            session_id=session_id,
        )
    )


def _ok(response: ResponseDocument) -> None:
    assert response.status == "OK", response.to_mapping()


class _Gate:
    """A controllable work body: loops on the §12 checkpoint until
    the test releases it — the cancellation/deadline races made
    deterministic from the test side."""

    def __init__(self) -> None:
        self._release = threading.Event()

    def release(self) -> None:
        self._release.set()

    def __call__(self, context: WorkContext) -> dict[str, object]:
        while not self._release.is_set():
            context.check()
            self._release.wait(timeout=0.02)
        context.check()
        return {"done": True}


def _probe_kind(name: str, body: Any) -> WorkKind:
    """A test work kind: no arguments of its own, the body called
    with the WorkContext (the §6.1 smaller composition)."""
    return WorkKind(
        name=name,
        description="the packet's probe kind",
        validate_arguments=lambda arguments: {},
        work=lambda context, inputs: body(context),
    )


# ------------------------------------------------------------ lifecycles


def test_lifecycle_vocabulary_closures() -> None:
    """§11's four machines, the exact membership (a silent member is
    a bug; a missing member is a bug)."""
    assert APPLICATION_STATES == frozenset(
        {"STARTING", "READY", "DEGRADED", "STOPPING", "STOPPED", "FAILED_SHUTDOWN"}
    )
    assert BACKEND_STATES == frozenset(
        {
            "ABSENT",
            "STARTING",
            "PROBING",
            "READY",
            "BUSY",
            "STOPPING",
            "STOPPED",
            "FAILED",
            "RECOVERING",
        }
    )
    assert MODEL_STATES == frozenset(
        {
            "DISCOVERED",
            "VALIDATED",
            "SELECTED",
            "LOADING",
            "LOADED",
            "ACTIVE",
            "UNLOADING",
            "EVICTED",
            "FAILED",
        }
    )
    assert EXECUTION_STATES == frozenset(
        {
            "ADMITTED",
            "STARTING",
            "RUNNING",
            "COMPLETING",
            "COMPLETED",
            "FAILED",
            "CANCEL_REQUESTED",
            "CANCELED",
            "FAILED_TO_CANCEL",
            "UNKNOWN",
        }
    )
    assert LIFECYCLE_DOMAINS == frozenset(LIFECYCLE_STATES)
    for domain in LIFECYCLE_DOMAINS:
        assert INITIAL_STATES[domain] in states(domain)


def test_lifecycle_ladder_walks() -> None:
    """Every ladder walks its spec'd chain legally — including the
    failure/cancellation branches and the re-selection loop."""
    # Application: the healthy walk + §25's FAILED_SHUTDOWN terminal.
    current = "STARTING"
    for target in ("READY", "DEGRADED", "READY", "STOPPING", "STOPPED"):
        current = transition("APPLICATION", current, target)
    assert current == "STOPPED"
    current = "STARTING"
    for target in ("READY", "STOPPING", "FAILED_SHUTDOWN"):
        current = transition("APPLICATION", current, target)
    assert current == "FAILED_SHUTDOWN"
    # Backend: the healthy walk, the failure branch, the recovery.
    current = "ABSENT"
    healthy = ("STARTING", "PROBING", "READY", "BUSY", "READY", "STOPPING", "STOPPED")
    for target in healthy:
        current = transition("BACKEND", current, target)
    assert current == "STOPPED"
    current = "ABSENT"
    for target in ("STARTING", "FAILED", "RECOVERING", "READY"):
        current = transition("BACKEND", current, target)
    assert current == "READY"
    # Model: the full ladder, the re-selection after eviction, FAILED.
    current = "DISCOVERED"
    ladder = ("VALIDATED", "SELECTED", "LOADING", "LOADED", "ACTIVE", "UNLOADING", "EVICTED")
    for target in ladder:
        current = transition("MODEL", current, target)
    assert current == "EVICTED"
    current = transition("MODEL", current, "SELECTED")
    assert current == "SELECTED"
    assert transition("MODEL", "VALIDATED", "FAILED") == "FAILED"
    # Execution: completion, failure, and the three cancellation ends.
    current = "ADMITTED"
    for target in ("STARTING", "RUNNING", "COMPLETING", "COMPLETED"):
        current = transition("EXECUTION", current, target)
    assert current == "COMPLETED"
    assert transition("EXECUTION", "RUNNING", "FAILED") == "FAILED"
    for terminal in ("CANCELED", "FAILED_TO_CANCEL", "UNKNOWN", "FAILED"):
        assert (
            transition("EXECUTION", "CANCEL_REQUESTED", terminal) == terminal
        )
    # §25's process-loss marks (the mark_unknown producers).
    assert transition("EXECUTION", "RUNNING", "UNKNOWN") == "UNKNOWN"
    assert transition("EXECUTION", "STARTING", "UNKNOWN") == "UNKNOWN"
    # A queued admission may be cancelled before it starts.
    assert (
        transition("EXECUTION", "ADMITTED", "CANCEL_REQUESTED")
        == "CANCEL_REQUESTED"
    )


def test_lifecycle_terminal_states() -> None:
    """Terminal = the empty successor set, per domain (the §11
    closure the artifact's status rides)."""
    assert TERMINAL_STATES["APPLICATION"] == frozenset(
        {"STOPPED", "FAILED_SHUTDOWN"}
    )
    assert TERMINAL_STATES["BACKEND"] == frozenset({"STOPPED"})
    assert TERMINAL_STATES["MODEL"] == frozenset({"FAILED"})
    assert TERMINAL_STATES["EXECUTION"] == frozenset(
        {"COMPLETED", "FAILED", "CANCELED", "FAILED_TO_CANCEL", "UNKNOWN"}
    )
    for domain in LIFECYCLE_DOMAINS:
        for state in states(domain):
            assert is_terminal(domain, state) == (
                legal_transitions(domain, state) == frozenset()
            )


def test_lifecycle_invalid_transitions_loud() -> None:
    """The falsifiers: every illegal move (including same-state and
    moves out of terminals) raises LifecycleError naming the legal
    set — never a silent no-op."""
    falsifiers = [
        ("EXECUTION", "COMPLETED", "RUNNING"),
        ("EXECUTION", "CANCELED", "RUNNING"),
        ("EXECUTION", "ADMITTED", "COMPLETED"),
        ("EXECUTION", "RUNNING", "RUNNING"),
        ("EXECUTION", "COMPLETING", "CANCEL_REQUESTED"),
        ("APPLICATION", "STOPPED", "READY"),
        ("APPLICATION", "STARTING", "DEGRADED"),
        ("BACKEND", "ABSENT", "READY"),
        ("BACKEND", "STOPPED", "STARTING"),
        ("MODEL", "DISCOVERED", "ACTIVE"),
        ("MODEL", "FAILED", "SELECTED"),
        ("MODEL", "LOADED", "UNLOADING"),
    ]
    for domain, current, target in falsifiers:
        with pytest.raises(LifecycleError, match="illegal transition"):
            transition(domain, current, target)


def test_lifecycle_unknown_domain_and_state_loud() -> None:
    with pytest.raises(LifecycleError, match="unknown lifecycle domain"):
        states("NOT_A_DOMAIN")
    with pytest.raises(LifecycleError, match="unknown state"):
        legal_transitions("EXECUTION", "NOT_A_STATE")
    with pytest.raises(LifecycleError, match="unknown state"):
        transition("MODEL", "NOT_A_STATE", "VALIDATED")


# ------------------------------------------------- deadline + cancellation


def test_operation_deadline_budget_arithmetic() -> None:
    """§12: one absolute deadline — remaining is the only view."""
    deadline = OperationDeadline(
        operation_id="op", started_monotonic=100.0, deadline_monotonic=160.0
    )
    assert deadline.remaining(100.0) == 60.0
    assert deadline.remaining(130.0) == 30.0
    assert deadline.remaining(160.0) == 0.0
    assert deadline.remaining(200.0) == -40.0  # the overrun stays visible
    assert not deadline.exceeded(159.9)
    assert deadline.exceeded(160.0)
    assert deadline.exceeded(200.0)


def test_operation_deadline_requires_positive_budget() -> None:
    with pytest.raises(RegistryError, match="positive budget"):
        OperationDeadline("op", 100.0, 100.0)
    with pytest.raises(RegistryError, match="positive budget"):
        OperationDeadline("op", 100.0, 99.0)
    with pytest.raises(RegistryError, match="empty operation_id"):
        OperationDeadline("", 100.0, 160.0)


def test_work_context_check_cancellation() -> None:
    clock, _ = _fixed_clock()
    deadline = OperationDeadline("op", 100.0, 160.0)
    token = CancellationToken()
    context = WorkContext(
        execution_id="exec", deadline=deadline, clock=clock, cancellation=token
    )
    assert not context.cancellation_requested()
    assert context.remaining_budget() == 60.0
    context.check()  # no-op while neither flag is set
    token.request()
    assert context.cancellation_requested()
    with pytest.raises(WorkCancelled, match="checkpoint observed"):
        context.check()


def test_work_context_check_deadline() -> None:
    clock, step = _fixed_clock()
    deadline = OperationDeadline("op", 100.0, 160.0)
    context = WorkContext(
        execution_id="exec",
        deadline=deadline,
        clock=clock,
        cancellation=CancellationToken(),
    )
    step.step(59.0)
    context.check()
    step.step(1.0)
    with pytest.raises(DeadlineExceeded, match="absolute deadline"):
        context.check()


def test_registry_config_ceilings_loud() -> None:
    with pytest.raises(RegistryError, match="max_deadline_seconds"):
        ExecutionRegistryConfig(default_deadline_seconds=120.0, max_deadline_seconds=60.0)
    with pytest.raises(RegistryError, match="positive number"):
        ExecutionRegistryConfig(default_deadline_seconds=0)


def test_registry_admit_freezes_inputs_before_work(tmp_path: Path) -> None:
    """§10's core falsifier: the frozen inputs exist on the record
    BEFORE the work runs — the work itself observes them (the
    before-side-effects proof, from inside the work)."""
    clock, _ = _fixed_clock()
    registry = ExecutionRegistry(clock)
    seen: dict[str, object] = {}

    def body(context: WorkContext) -> dict[str, object]:
        document = registry.document(context.execution_id, "session-1")
        seen["frozen_at_work_start"] = document["frozen_inputs"]
        seen["state_at_work_start"] = document["state"]
        return {"observed": True}

    execution_id = registry.admit(
        operation_id="op-1",
        session_id="session-1",
        work_kind="probe",
        frozen_inputs={"work": "probe", "x": "1"},
        deadline_seconds=30.0,
    )
    document = registry.document(execution_id, "session-1")
    assert document["frozen_inputs"] == [["work", "probe"], ["x", "1"]]
    assert document["state"] == "ADMITTED"
    assert document["artifact"] is None  # not closed pre-terminal
    registry.launch(execution_id, body)
    assert registry.wait(execution_id, timeout=5.0)
    document = registry.document(execution_id, "session-1")
    assert document["state"] == "COMPLETED"
    assert seen["state_at_work_start"] == "RUNNING"
    assert seen["frozen_at_work_start"] == [["work", "probe"], ["x", "1"]]
    # the artifact closed with the terminal status + the SAME freeze
    artifact = document["artifact"]
    assert artifact is not None
    assert artifact["status"] == "COMPLETED"
    assert artifact["frozen_inputs"] == [["work", "probe"], ["x", "1"]]


def test_registry_duplicate_admission_loud(tmp_path: Path) -> None:
    clock, _ = _fixed_clock()
    registry = ExecutionRegistry(clock)
    registry.admit(
        operation_id="op-1",
        session_id="s",
        work_kind="probe",
        frozen_inputs={"work": "probe"},
        deadline_seconds=30.0,
    )
    with pytest.raises(RegistryError, match="already admitted"):
        registry.admit(
            operation_id="op-1",
            session_id="s",
            work_kind="probe",
            frozen_inputs={"work": "probe"},
            deadline_seconds=30.0,
        )


def test_registry_deadline_ceiling_enforced(tmp_path: Path) -> None:
    clock, _ = _fixed_clock()
    registry = ExecutionRegistry(clock)
    with pytest.raises(RegistryError, match="exceeds the ceiling"):
        registry.resolve_deadline_seconds(7200.0)
    assert registry.resolve_deadline_seconds(None) == 60.0
    assert registry.resolve_deadline_seconds(30) == 30.0


# --------------------------------------------- the run family (via gateway)


def test_run_start_happy_path_completes(tmp_path: Path) -> None:
    """The one real work kind end to end: the §20 digest run — the
    result is the independent sha256 (the oracle), the artifact
    closes with the terminal status, the registry records the strong
    identity (the run's effect)."""
    gateway, ops = _compose(tmp_path)
    session_id = _session(gateway)
    payload = b"the quick brown fox jumps over the lazy dog" * 100
    (tmp_path / "models" / "fixture.gguf").write_bytes(payload)
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    response = _run_start(
        gateway, session_id, "key-1", "model.digest", {"logical_name": "fixture.gguf"}
    )
    _ok(response)
    execution_id = str(response.result["execution_id"])
    assert ops.executions.wait(execution_id, timeout=5.0)
    document = _run_get(gateway, session_id, execution_id)
    _ok(document)
    result = document.result["result"]
    assert result is not None
    assert result["content_digest"] == hashlib.sha256(payload).hexdigest()
    assert result["chunks"] == 1  # 4.5 KB < one 1 MiB chunk
    assert result["size_bytes"] == len(payload)
    assert result["logical_name"] == "fixture.gguf"
    # the artifact closes at terminal with the §11 closure member
    artifact = document.result["artifact"]
    assert artifact is not None
    assert artifact["status"] == "COMPLETED"
    # the effect: the registry now knows the strong identity
    listing = gateway.dispatch(
        RequestEnvelope(operation="model.list", arguments={})
    )
    _ok(listing)
    entry = next(
        m for m in listing.result["models"] if m["logical_name"] == "fixture.gguf"
    )
    assert entry["content_digest"] == hashlib.sha256(payload).hexdigest()


def test_run_start_returns_identity_immediately(tmp_path: Path) -> None:
    """§8: long-running work returns identity immediately — the
    response carries the execution_id while the work is still
    mid-flight; the live state is run.get's."""
    clock, _ = _fixed_clock()
    gate = _Gate()
    gateway, ops = _compose(tmp_path, clock, {"probe.block": _probe_kind("probe.block", gate)})
    session_id = _session(gateway)
    response = _run_start(
        gateway, session_id, "key-1", "probe.block", {}
    )
    _ok(response)
    execution_id = str(response.result["execution_id"])
    document = _run_get(gateway, session_id, execution_id)
    _ok(document)
    assert document.result["state"] in ("STARTING", "RUNNING")
    assert document.result["terminal"] is False
    assert document.result["artifact"] is None
    gate.release()
    assert ops.executions.wait(execution_id, timeout=5.0)
    document = _run_get(gateway, session_id, execution_id)
    assert document.result["state"] == "COMPLETED"
    assert document.result["terminal"] is True
    assert document.result["result"] == {"done": True}


def test_run_cancel_truthful_midflight(tmp_path: Path) -> None:
    """§12.3: the cancellation request is accepted (CANCEL_REQUESTED)
    and the work's next checkpoint observes it — CANCELED, the result
    absent, the artifact closed with the cancellation truth."""
    clock, _ = _fixed_clock()
    gate = _Gate()
    gateway, ops = _compose(tmp_path, clock, {"probe.block": _probe_kind("probe.block", gate)})
    session_id = _session(gateway)
    response = _run_start(gateway, session_id, "key-1", "probe.block", {})
    execution_id = str(response.result["execution_id"])
    cancel = _run_cancel(gateway, session_id, execution_id, "cancel-key-1")
    _ok(cancel)
    assert cancel.result["cancellation"] == "CANCEL_REQUESTED"
    assert ops.executions.wait(execution_id, timeout=5.0)
    document = _run_get(gateway, session_id, execution_id)
    assert document.result["state"] == "CANCELED"
    assert document.result["result"] is None
    artifact = document.result["artifact"]
    assert artifact is not None
    assert artifact["status"] == "CANCELED"
    assert artifact["diagnostics"] == [
        "the checkpoint observed the cancellation request"
    ]


def test_run_cancel_after_terminal_failed_to_cancel(tmp_path: Path) -> None:
    """§12.3's other half: a cancel on a completed execution is
    FAILED_TO_CANCEL — never a fabricated cancellation."""
    gateway, ops = _compose(tmp_path)
    session_id = _session(gateway)
    (tmp_path / "models" / "small.gguf").write_bytes(b"payload")
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    response = _run_start(
        gateway, session_id, "key-1", "model.digest", {"logical_name": "small.gguf"}
    )
    execution_id = str(response.result["execution_id"])
    assert ops.executions.wait(execution_id, timeout=5.0)
    cancel = _run_cancel(gateway, session_id, execution_id, "cancel-key-1")
    _ok(cancel)
    assert cancel.result["cancellation"] == "FAILED_TO_CANCEL"
    document = _run_get(gateway, session_id, execution_id)
    assert document.result["state"] == "COMPLETED"  # unchanged — truthful


def test_run_cancel_idempotent_on_canceled(tmp_path: Path) -> None:
    """A re-request on an already-canceled record returns CANCELED —
    the idempotent truth, not a second state move."""
    clock, _ = _fixed_clock()
    gate = _Gate()
    gateway, ops = _compose(tmp_path, clock, {"probe.block": _probe_kind("probe.block", gate)})
    session_id = _session(gateway)
    response = _run_start(gateway, session_id, "key-1", "probe.block", {})
    execution_id = str(response.result["execution_id"])
    first = _run_cancel(gateway, session_id, execution_id, "cancel-key-1")
    assert first.result["cancellation"] == "CANCEL_REQUESTED"
    assert ops.executions.wait(execution_id, timeout=5.0)
    second = _run_cancel(gateway, session_id, execution_id, "cancel-key-2")
    _ok(second)
    assert second.result["cancellation"] == "CANCELED"


def test_run_work_failure_recorded(tmp_path: Path) -> None:
    """A raising work lands FAILED with the failure type named — the
    artifact closes with it (the §29 matrix's honest terminal)."""
    def body(context: WorkContext) -> dict[str, object]:
        raise ValueError("the probe's deliberate failure")

    gateway, ops = _compose(tmp_path, None, {"probe.fail": _probe_kind("probe.fail", body)})
    session_id = _session(gateway)
    response = _run_start(gateway, session_id, "key-1", "probe.fail", {})
    _ok(response)  # the dispatch succeeded — the WORK failed later
    execution_id = str(response.result["execution_id"])
    assert ops.executions.wait(execution_id, timeout=5.0)
    document = _run_get(gateway, session_id, execution_id)
    assert document.result["state"] == "FAILED"
    assert document.result["failure_type"] == "ValueError"
    artifact = document.result["artifact"]
    assert artifact is not None
    assert artifact["status"] == "FAILED"
    # wb-9: the diagnostic carries the failure's own message too (the
    # fetch row's honest-cause law — bounded, never the whole traceback).
    assert artifact["diagnostics"][0].startswith("the work raised ValueError")
    assert "the probe's deliberate failure" in artifact["diagnostics"][0]


def test_run_deadline_exceeded_failed(tmp_path: Path) -> None:
    """§12's absolute deadline: the checkpoint observes the overrun —
    FAILED, the diagnostics naming it (terminal, never a hidden
    retry loop)."""
    real_clock = AppClock()  # the real monotonic — the deadline must actually pass
    gate = _Gate()
    gateway, ops = _compose(
        tmp_path, real_clock, {"probe.block": _probe_kind("probe.block", gate)}
    )
    session_id = _session(gateway)
    response = _run_start(
        gateway,
        session_id,
        "key-1",
        "probe.block",
        {},
        deadline_seconds=0.05,
    )
    _ok(response)
    execution_id = str(response.result["execution_id"])
    assert ops.executions.wait(execution_id, timeout=5.0)
    document = _run_get(gateway, session_id, execution_id)
    assert document.result["state"] == "FAILED"
    assert document.result["failure_type"] == "DeadlineExceeded"
    artifact = document.result["artifact"]
    assert artifact is not None
    assert any("deadline exceeded" in d for d in artifact["diagnostics"])
    gate.release()  # release the gate's loop resource


def test_run_deadline_argument_falsifiers(tmp_path: Path) -> None:
    """§26 boundedness: a deadline beyond the ceiling is rejected,
    never clamped; the argument contract is closed."""
    gateway, _ = _compose(tmp_path)
    session_id = _session(gateway)
    (tmp_path / "models" / "x.gguf").write_bytes(b"x")
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    base = {"work": "model.digest", "arguments": {"logical_name": "x.gguf"}}
    cases: list[tuple[dict[str, Any], str]] = [
        ({**base, "deadline_seconds": 7200.0}, "ceiling"),
        ({**base, "deadline_seconds": 0}, "positive"),
        ({**base, "deadline_seconds": -1.0}, "positive"),
        ({**base, "deadline_seconds": True}, "positive"),
        ({**base, "deadline_seconds": "60"}, "positive"),
    ]
    for payload, pattern in cases:
        response = gateway.dispatch(
            RequestEnvelope(
                operation="run.start",
                arguments=payload,
                client_request_id=f"key-{pattern}-{payload['deadline_seconds']}",
                session_id=session_id,
            )
        )
        assert response.status == "REJECTED", response.to_mapping()
        assert response.rejection == "DOMAIN_REJECTED"


def test_run_start_domain_falsifiers(tmp_path: Path) -> None:
    """The NOT_SENT domain rejections: unknown work kind, malformed
    arguments, unknown keys — every one DOMAIN_REJECTED (never a
    §12.1 dispatch outcome), nothing admitted."""
    gateway, ops = _compose(tmp_path)
    session_id = _session(gateway)
    cases: list[dict[str, Any]] = [
        {"work": "not.a.kind", "arguments": {}},
        {"work": "", "arguments": {}},
        {"work": 123, "arguments": {}},
        {"work": "model.digest"},  # missing arguments -> default {} -> missing logical_name
        {"work": "model.digest", "arguments": {"logical_name": 123}},
        {"work": "model.digest", "arguments": {"logical_name": "x.gguf", "extra": 1}},
        {"work": "model.digest", "arguments": []},
        {"work": "model.digest", "arguments": {"logical_name": "never-discovered.gguf"}},
        {"work": "model.digest", "arguments": {}, "unknown_key": True},
    ]
    for index, payload in enumerate(cases):
        response = gateway.dispatch(
            RequestEnvelope(
                operation="run.start",
                arguments=payload,
                client_request_id=f"bad-key-{index}",
                session_id=session_id,
            )
        )
        assert response.status == "REJECTED", (index, response.to_mapping())
        assert response.rejection == "DOMAIN_REJECTED"
    assert ops.executions.execution_ids == ()  # nothing admitted


def test_run_start_idempotent_replay(tmp_path: Path) -> None:
    """The §12.2 law over the run family: the same key replays the
    recorded outcome verbatim (one effect — one execution), the
    conflicting reuse is DUPLICATE_REQUEST."""
    gateway, ops = _compose(tmp_path)
    session_id = _session(gateway)
    (tmp_path / "models" / "a.gguf").write_bytes(b"aaa")
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    first = _run_start(
        gateway, session_id, "key-1", "model.digest", {"logical_name": "a.gguf"}
    )
    _ok(first)
    execution_id = str(first.result["execution_id"])
    assert ops.executions.wait(execution_id, timeout=5.0)
    replay = _run_start(
        gateway, session_id, "key-1", "model.digest", {"logical_name": "a.gguf"}
    )
    _ok(replay)
    assert replay.duplicate is True
    assert replay.result == first.result
    assert ops.executions.execution_ids == (execution_id,)
    conflict = _run_start(
        gateway, session_id, "key-1", "model.digest", {"logical_name": "other.gguf"}
    )
    assert conflict.status == "REJECTED"
    assert conflict.rejection == "DUPLICATE_REQUEST"


def test_run_get_ownership_and_missing(tmp_path: Path) -> None:
    """The session-ownership law: an execution is visible only to its
    session; a missing identity is DOMAIN_REJECTED."""
    gateway, ops = _compose(tmp_path)
    session_id = _session(gateway, "session-key-1")
    other_session = _session(gateway, "session-key-2")
    (tmp_path / "models" / "a.gguf").write_bytes(b"aaa")
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    response = _run_start(
        gateway, session_id, "key-1", "model.digest", {"logical_name": "a.gguf"}
    )
    execution_id = str(response.result["execution_id"])
    assert ops.executions.wait(execution_id, timeout=5.0)
    foreign = _run_get(gateway, other_session, execution_id)
    assert foreign.status == "REJECTED"
    assert foreign.rejection == "DOMAIN_REJECTED"
    assert "another session" in foreign.to_mapping()["result"]["reason"]
    missing = _run_get(gateway, session_id, "no-such-execution")
    assert missing.status == "REJECTED"
    assert missing.rejection == "DOMAIN_REJECTED"


def test_run_events_in_ordered_stream(tmp_path: Path) -> None:
    """§13: the dispatch-time effects land in the session's ordered
    stream as OPERATION_EFFECT events — RUN_STARTED at run.start,
    CANCEL_REQUESTED at run.cancel, sequences strictly increasing."""
    clock, _ = _fixed_clock()
    gate = _Gate()
    gateway, _ops = _compose(
        tmp_path, clock, {"probe.block": _probe_kind("probe.block", gate)}
    )
    session_id = _session(gateway)
    response = _run_start(gateway, session_id, "key-1", "probe.block", {})
    execution_id = str(response.result["execution_id"])
    _run_cancel(gateway, session_id, execution_id, "cancel-key-1")
    events = gateway.dispatch(
        RequestEnvelope(
            operation="session.events",
            arguments={},
            session_id=session_id,
        )
    )
    _ok(events)
    stream = events.result["events"]
    kinds = [(e["event_type"], e["payload"].get("effect")) for e in stream]
    assert kinds == [
        ("SESSION_CREATED", None),
        ("OPERATION_EFFECT", "RUN_STARTED"),
        ("OPERATION_EFFECT", "CANCEL_REQUESTED"),
    ]
    run_started = stream[1]
    assert run_started["payload"]["execution_id"] == execution_id
    assert run_started["payload"]["work"] == "probe.block"
    cancel_requested = stream[2]
    assert cancel_requested["payload"]["cancellation"] == "CANCEL_REQUESTED"
    sequences = [e["sequence"] for e in stream]
    assert sequences == sorted(sequences)
    gate.release()


def test_run_sent_outcome_unknown_on_spawn_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The §12.1 integration on the new surface: a mutating handler
    raising AFTER admission (the worker spawn failing) maps
    SENT_OUTCOME_UNKNOWN — recorded, the blind retry blocked — while
    the registry's own record says FAILED (each layer truthful at its
    own layer)."""
    clock, _ = _fixed_clock()

    def broken_thread(*args: object, **kwargs: object) -> threading.Thread:
        raise RuntimeError("no thread for you")

    monkeypatch.setattr(
        "workbench.application.operations.execution.threading.Thread",
        broken_thread,
    )
    gateway, ops = _compose(tmp_path, clock)
    session_id = _session(gateway)
    (tmp_path / "models" / "a.gguf").write_bytes(b"aaa")
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    response = _run_start(
        gateway, session_id, "key-1", "model.digest", {"logical_name": "a.gguf"}
    )
    assert response.status == "UNKNOWN", response.to_mapping()
    assert response.rejection == "SENT_OUTCOME_UNKNOWN"
    assert response.to_mapping()["result"]["error_type"] == "RuntimeError"
    # the retry with the same key replays the recorded UNKNOWN outcome
    replay = _run_start(
        gateway, session_id, "key-1", "model.digest", {"logical_name": "a.gguf"}
    )
    assert replay.status == "UNKNOWN"
    assert replay.duplicate is True
    # the registry's truth: the execution FAILED (the walk happened
    # before the re-raise)
    (execution_id,) = ops.executions.execution_ids
    document = _run_get(gateway, session_id, execution_id)
    assert document.result["state"] == "FAILED"
    assert document.result["terminal"] is True


# ------------------------------------------- the model family (discovery)


def test_model_list_discovery(tmp_path: Path) -> None:
    gateway, _ = _compose(tmp_path)
    (tmp_path / "models" / "beta.gguf").write_bytes(b"bb")
    (tmp_path / "models" / "alpha.gguf").write_bytes(b"aaaa")
    (tmp_path / "models" / "notes.txt").write_bytes(b"not a model")  # any file is discovered
    response = gateway.dispatch(
        RequestEnvelope(operation="model.list", arguments={})
    )
    _ok(response)
    assert response.result["directory_state"] == "OK"
    names = [m["logical_name"] for m in response.result["models"]]
    assert names == ["alpha.gguf", "beta.gguf", "notes.txt"]  # sorted
    entry = response.result["models"][0]
    assert entry["size_bytes"] == 4
    assert entry["state"] == DISCOVERY_STATE
    assert entry["content_digest"] is None  # not yet computed
    assert entry["location"].endswith("alpha.gguf")
    assert isinstance(entry["mtime_ns"], int)


def test_model_list_missing_directory_truthful(tmp_path: Path) -> None:
    """A missing MODELS_ASSETS slot is a truthful MISSING + empty
    list (the §16 vocabulary surfaced, never an error, never a
    fabricated model)."""
    gateway = Gateway()
    compose_workbench_operations(
        gateway, tmp_path / "not-created", AppClock()
    )
    response = gateway.dispatch(
        RequestEnvelope(operation="model.list", arguments={})
    )
    _ok(response)
    assert response.result == {
        "directory_state": "MISSING",
        "models": [],
        "models_root": str(tmp_path / "not-created"),
    }


def test_model_list_corrupt_slot_loud(tmp_path: Path) -> None:
    """The §16 shallow CORRUPT form (a file where the directory
    should be) is a LOUD DOMAIN_REJECTED, never a silent empty."""
    corrupt = tmp_path / "models"
    corrupt.parent.mkdir(parents=True, exist_ok=True)
    corrupt.write_bytes(b"i am a file, not a directory")
    gateway = Gateway()
    compose_workbench_operations(gateway, corrupt, AppClock())
    response = gateway.dispatch(
        RequestEnvelope(operation="model.list", arguments={})
    )
    assert response.status == "REJECTED"
    assert response.rejection == "DOMAIN_REJECTED"
    assert "CORRUPT" in response.to_mapping()["result"]["reason"]


def test_model_list_takes_no_arguments(tmp_path: Path) -> None:
    gateway, _ = _compose(tmp_path)
    response = gateway.dispatch(
        RequestEnvelope(operation="model.list", arguments={"refresh": True})
    )
    assert response.status == "REJECTED"
    assert response.rejection == "DOMAIN_REJECTED"


def test_model_inspect_strong_identity(tmp_path: Path) -> None:
    """The §9 correctness identity: the fresh sha256 of the bytes —
    the independent oracle."""
    gateway, _ = _compose(tmp_path)
    payload = b"model-bytes" * 64
    (tmp_path / "models" / "m.gguf").write_bytes(payload)
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    response = gateway.dispatch(
        RequestEnvelope(
            operation="model.inspect",
            arguments={"logical_name": "m.gguf"},
        )
    )
    _ok(response)
    assert response.result["content_digest"] == hashlib.sha256(payload).hexdigest()
    assert response.result["state"] == DISCOVERY_STATE
    assert response.result["size_bytes"] == len(payload)


def test_model_identity_laws(tmp_path: Path) -> None:
    """§9: same bytes -> the same identity (stability); same path +
    new bytes -> a NEW content identity (never silently reused)."""
    gateway, _ = _compose(tmp_path)
    target = tmp_path / "models" / "m.gguf"
    target.write_bytes(b"version-one")
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    first = gateway.dispatch(
        RequestEnvelope(
            operation="model.inspect", arguments={"logical_name": "m.gguf"}
        )
    )
    again = gateway.dispatch(
        RequestEnvelope(
            operation="model.inspect", arguments={"logical_name": "m.gguf"}
        )
    )
    assert first.result["content_digest"] == again.result["content_digest"]
    target.write_bytes(b"version-two-bytes")
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    third = gateway.dispatch(
        RequestEnvelope(
            operation="model.inspect", arguments={"logical_name": "m.gguf"}
        )
    )
    assert third.result["content_digest"] != first.result["content_digest"]
    assert third.result["content_digest"] == hashlib.sha256(
        b"version-two-bytes"
    ).hexdigest()


def test_model_inspect_undiscovered_and_paths(tmp_path: Path) -> None:
    gateway, _ = _compose(tmp_path)
    (tmp_path / "models" / "m.gguf").write_bytes(b"x")
    for name in ("m.gguf", "../escape", "sub/dir", ".", "..", ""):
        response = gateway.dispatch(
            RequestEnvelope(
                operation="model.inspect",
                arguments={"logical_name": name} if name else {},
            )
        )
        assert response.status == "REJECTED", (name, response.to_mapping())
        assert response.rejection == "DOMAIN_REJECTED"


def test_model_registry_relative_root_loud(tmp_path: Path) -> None:
    with pytest.raises(ModelRegistryError, match="relative"):
        ModelRegistry(Path("relative/models"))
    with pytest.raises(ModelRegistryError, match="pathlib.Path"):
        ModelRegistry("not-a-path")  # type: ignore[arg-type]


def test_model_digest_run_chunked(tmp_path: Path) -> None:
    """The §20 long-running arm over a multi-chunk file: the chunk
    count is the ceiling division (the checkpoint cadence), the
    strong identity lands in the registry (the run's effect)."""
    gateway, ops = _compose(tmp_path)
    payload = b"0123456789abcdef" * (DEFAULT_CHUNK_BYTES // 16 * 2 + 3)
    (tmp_path / "models" / "big.gguf").write_bytes(payload)
    gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
    response = _run_start(
        gateway, _session(gateway), "key-1", "model.digest",
        {"logical_name": "big.gguf"},
    )
    _ok(response)
    execution_id = str(response.result["execution_id"])
    assert ops.executions.wait(execution_id, timeout=30.0)
    document = _run_get(gateway, _session(gateway), execution_id)
    result = document.result["result"]
    expected_chunks = -(-len(payload) // DEFAULT_CHUNK_BYTES)
    assert result["chunks"] == expected_chunks
    assert result["content_digest"] == hashlib.sha256(payload).hexdigest()
    listing = gateway.dispatch(
        RequestEnvelope(operation="model.list", arguments={})
    )
    entry = next(
        m for m in listing.result["models"] if m["logical_name"] == "big.gguf"
    )
    assert entry["content_digest"] == result["content_digest"]


# ------------------------------------------------------- composition root


def test_composition_registers_five_operations(tmp_path: Path) -> None:
    gateway, ops = _compose(tmp_path)
    expected = {
        "run.start",
        "run.get",
        "run.cancel",
        "model.list",
        "model.inspect",
        # the wb-4 builtins stay
        "session.create",
        "session.get",
        "session.attach",
        "session.detach",
        "session.events",
        "app.status",
    }
    assert set(gateway.operation_names) == expected
    assert ops.work_kinds == ("model.digest", "model.import")


def test_composition_duplicate_loud(tmp_path: Path) -> None:
    """§6.1/one-name-one-owner: composing twice on one gateway is the
    gateway's own loud error, never a silent override."""
    gateway, _ = _compose(tmp_path)
    with pytest.raises(GatewayError, match="already registered"):
        compose_workbench_operations(
            gateway, tmp_path / "models", AppClock()
        )


def test_composition_empty_work_kinds_loud(tmp_path: Path) -> None:
    gateway = Gateway()
    with pytest.raises(composition.CompositionError, match="at least one work kind"):
        compose_workbench_operations(
            gateway, tmp_path / "models", AppClock(), work_kinds={}
        )


def test_work_kind_contract_loud() -> None:
    # wb-9: WorkKind lives in execution.py (the run family's own module
    # — the fetch factory constructs kinds without a circular import);
    # its loudness is the registry's own error family, re-exported
    # through the composition's historical name.
    from workbench.application.operations.execution import RegistryError

    with pytest.raises(RegistryError, match="non-empty name"):
        WorkKind(
            name="   ",
            description="",
            validate_arguments=lambda a: {},
            work=lambda c, i: {},
        )
    with pytest.raises(RegistryError, match="callable"):
        WorkKind(
            name="ok",
            description="",
            validate_arguments=None,  # type: ignore[arg-type]
            work=lambda c, i: {},
        )
    with pytest.raises(RegistryError, match="default_deadline_seconds"):
        WorkKind(
            name="ok",
            description="",
            validate_arguments=lambda a: {},
            work=lambda c, i: {},
            default_deadline_seconds=-1.0,
        )


# --------------------------------------------- the wb-5 gateway surface


def test_operation_rejected_enforces_vocabulary() -> None:
    """The public carrier: a member of the closed set passes; an
    invented member is a construction bug (GatewayError, loud)."""
    rejection = OperationRejected("DOMAIN_REJECTED", "the reason")
    assert rejection.rejection == "DOMAIN_REJECTED"
    assert rejection.reason == "the reason"
    with pytest.raises(GatewayError, match="closed rejection set"):
        OperationRejected("NOT_A_MEMBER", "the reason")


def test_operation_rejected_rides_the_pipeline(tmp_path: Path) -> None:
    """A registered handler's OperationRejected maps to the
    REJECTED/DOMAIN_REJECTED response — NOT_SENT, never a §12.1
    outcome — including through the public carrier."""
    gateway = Gateway()
    seen: dict[str, Any] = {}

    def handler(context: Any) -> dict[str, object]:
        seen["effects"] = context.effects
        raise OperationRejected("DOMAIN_REJECTED", "the handler's own reason")

    gateway.register(
        OperationSpec(name="probe.reject", kind="READ", handler=handler)
    )
    response = gateway.dispatch(
        RequestEnvelope(operation="probe.reject", arguments={})
    )
    assert response.status == "REJECTED"
    assert response.rejection == "DOMAIN_REJECTED"
    assert response.to_mapping()["result"]["reason"] == "the handler's own reason"
    assert seen["effects"] is None  # not session-scoped: no stream


def test_effects_surface_session_scoped_only(tmp_path: Path) -> None:
    """The effects surface exists exactly for session-scoped
    operations; a probe MUTATION's two effects land as two ordered
    OPERATION_EFFECT events."""
    gateway, _ = _compose(tmp_path)
    session_id = _session(gateway)
    seen: dict[str, Any] = {}

    def handler(context: Any) -> dict[str, object]:
        seen["effects"] = context.effects
        assert context.effects is not None
        context.effects.effect({"effect": "ONE", "n": 1})
        context.effects.effect({"effect": "TWO", "n": 2})
        return {"emitted": 2}

    gateway.register(
        OperationSpec(
            name="probe.emit",
            kind="MUTATION",
            handler=handler,
            session_scoped=True,
        )
    )
    response = gateway.dispatch(
        RequestEnvelope(
            operation="probe.emit",
            arguments={},
            client_request_id="emit-key-1",
            session_id=session_id,
        )
    )
    _ok(response)
    assert seen["effects"] is not None
    events = gateway.dispatch(
        RequestEnvelope(
            operation="session.events", arguments={}, session_id=session_id
        )
    )
    stream = events.result["events"]
    assert [e["payload"]["effect"] for e in stream[1:]] == ["ONE", "TWO"]
    assert stream[1]["event_type"] == "OPERATION_EFFECT"
    assert stream[1]["operation_id"] == response.operation_id


def test_http_parity_for_registered_operations(tmp_path: Path) -> None:
    """§30/§22: the same dispatch core serves the direct call and the
    HTTP binding — the registered operations byte-identical both
    ways (model.list as the proof; the wb-4 parity law extended over
    the wb-5 surface)."""
    import urllib.request

    gateway, _ = _compose(tmp_path)
    (tmp_path / "models" / "m.gguf").write_bytes(b"parity")
    transport = LoopbackHttpTransport(gateway).start()
    try:
        request = urllib.request.Request(
            transport.url,
            data=json.dumps(
                {
                    "operation": "model.list",
                    "arguments": {},
                    # a keyed READ: the operation identity is stable
                    # across dispatches (the unkeyed form is per-
                    # dispatch by design — the counter identity)
                    "client_request_id": "parity-read-key",
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=10) as handle:
            http_document = json.loads(handle.read().decode("utf-8"))
    finally:
        transport.stop()
    direct = gateway.dispatch(
        RequestEnvelope(
            operation="model.list",
            arguments={},
            client_request_id="parity-read-key",
        )
    )
    assert http_document == direct.to_mapping()


# ----------------------------------------------------------- determinism


def test_run_response_and_artifact_byte_deterministic(tmp_path: Path) -> None:
    """D4: the same inputs -> the byte-identical run.start response
    and the byte-identical closed artifact (two fresh compositions,
    the same fixed clock)."""
    outputs: list[tuple[str, str]] = []
    for index in range(2):
        root = tmp_path / f"case{index}" / "models"
        root.mkdir(parents=True)
        (root / "m.gguf").write_bytes(b"deterministic-payload")
        clock, _ = _fixed_clock()
        gateway = Gateway(clock=clock)
        ops = compose_workbench_operations(gateway, root, clock)
        gateway.dispatch(RequestEnvelope(operation="model.list", arguments={}))
        session_id = _session(gateway, "the-same-session-key")
        response = _run_start(
            gateway, session_id, "the-same-key", "model.digest",
            {"logical_name": "m.gguf"},
        )
        _ok(response)
        execution_id = str(response.result["execution_id"])
        assert ops.executions.wait(execution_id, timeout=5.0)
        document = _run_get(gateway, session_id, execution_id)
        outputs.append(
            (
                json.dumps(
                    response.to_mapping(),
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                json.dumps(
                    document.to_mapping()["result"]["artifact"],
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            )
        )
    assert outputs[0][0] == outputs[1][0]
    assert outputs[0][1] == outputs[1][1]


def test_cross_pythonhashseed_pair(tmp_path: Path) -> None:
    """The D4 read-side discipline, subprocess form: the composed
    documents (discovery + inspect + a digest run's response and
    artifact) are byte-identical under PYTHONHASHSEED=0 and
    PYTHONHASHSEED=1."""
    root = tmp_path / "seedmodels"
    root.mkdir()
    (root / "m.gguf").write_bytes(b"cross-seed-payload")
    code = "\n".join(
        [
            "import json, pathlib, sys",
            "sys.path.insert(0, {!r})".format(str(REPO)),
            "from workbench.api.gateway import Gateway",
            "from workbench.api.contract import RequestEnvelope",
            "from workbench.application.clock import AppClock",
            "from workbench.application.operations.composition import (",
            "    compose_workbench_operations,",
            ")",
            "clock = AppClock(monotonic=lambda: 100.0, utc=lambda: 1000.0)",
            "gateway = Gateway(clock=clock)",
            "root = pathlib.Path({!r})".format(str(root)),
            "ops = compose_workbench_operations(gateway, root, clock)",
            "def dispatch(envelope):",
            "    return gateway.dispatch(envelope).to_mapping()",
            "session = dispatch(RequestEnvelope(",
            "    operation='session.create', arguments={},",
            "    client_request_id='seed-key'))",
            "listing = dispatch(RequestEnvelope(",
            "    operation='model.list', arguments={}))",
            "started = dispatch(RequestEnvelope(",
            "    operation='run.start',",
            "    arguments={'work': 'model.digest',",
            "               'arguments': {'logical_name': 'm.gguf'}},",
            "    client_request_id='run-key',",
            "    session_id=session['result']['session_id']))",
            "execution_id = started['result']['execution_id']",
            "assert ops.executions.wait(execution_id, 10.0)",
            "run = dispatch(RequestEnvelope(",
            "    operation='run.get', arguments={'execution_id': execution_id},",
            "    session_id=session['result']['session_id']))",
            "documents = [session, listing, started, run]",
            "print(json.dumps(documents, sort_keys=True,",
            "                 separators=(',', ':')))",
        ]
    )
    outputs = []
    for seed in ("0", "1"):
        env = {"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": seed}
        completed = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            env=env,
            timeout=120,
            check=True,
        )
        outputs.append(completed.stdout)
    assert outputs[0] == outputs[1]


def test_operations_import_closure() -> None:
    """The dependency direction (§6/§24): the operations package
    imports stdlib + workbench.application.* only — except
    `composition` (the wiring owner) and `backend` (the backend row's
    port + operations), which additionally import the gateway
    registration surface. No core/, no cli/, no engine (the app side
    stays CanonSim-free until the seam row; INV-4's two-surface form
    untouched — the port is injected, never imported)."""
    allowed = {
        "workbench",
        "workbench.application",
        "workbench.application.operations",
        "workbench.application.operations.backend",
        "workbench.application.operations.execution",
        "workbench.application.operations.models",
        "workbench.application.operations.lifecycles",
        "workbench.application.settings",
        # inf-1: the semantic inference-control layer (the profile
        # store + the resolver + the family's registration — the
        # composition wires it exactly like the settings family).
        "workbench.application.inference",
        "workbench.application.artifact",
        "workbench.application.clock",
        "workbench.application.identity",
        "workbench.application.operations.composition",
        "workbench.application.operations.observatory",
        # obs-2's seam module (the read model over core.log — the
        # CanonSim edge lives THERE, workbench-root beside
        # scene_build.py; the operations package reaches the log only
        # through it, never importing core itself).
        "workbench.observatory_read",
        "workbench.api.gateway",
    }
    for module_path in sorted(
        (REPO / "workbench" / "application" / "operations").glob("*.py")
    ):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                root_package = name.split(".")[0]
                if root_package in ("__future__",):
                    continue
                if root_package in sys.stdlib_module_names:
                    continue
                assert name in allowed, (
                    f"{module_path.name}: import {name!r} outside the "
                    "operations dependency envelope"
                )
