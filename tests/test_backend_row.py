"""wb-6 acceptance — the backend row (the owner's «подключи llama.cpp»
call, app §32 step 7; CONTRACTS §5's wb-6; the modules
`workbench/application/operations/backend.py` + the composition's
backend wiring + the engine adapter's model-management half).

The claim packet (TEST_PLAN §9's classes — the claimed EFFECT checked,
not merely that tests happened):

- **the port conformance** (§4.1/§29): the REAL adapter
  (`cli/engine.py`'s LlamaServerClient) satisfies the BackendPort
  structurally AND behaviorally — over the loopback stub server, the
  same client the station runs (INV-4 untouched: the physical surface
  stays the one module; the workbench imports it NEVER — the
  operations receive the port at the composition root);
- **chat.send** (§8/§19.1/§12): the §19.1 layer walk (REQUESTED →
  ACCEPTED — the closed argument surface, the ranges, the defaults;
  EFFECTIVE — the §10 freeze observable from admission; OBSERVED —
  content + finish_reason + the backend identity, the failed props
  probe the honest "unavailable" note); identity-then-poll (§8: the
  execution_id returns immediately); the backend failure closing the
  run FAILED with the cause named; the truthful cancellation trio —
  CANCELED (the entry checkpoint observed it), FAILED_TO_CANCEL (the
  late result recorded, never a completion), the deadline's
  DeadlineExceeded terminal;
- **model.load / model.unload** (§20/§11): the observed-outcome walk
  (ACTIVE on success; FAILED on the backend's observed refusal — the
  terminal gap rejected loudly, D-203; SELECTED rest on the UNKNOWN
  outcome, the re-load legal; EVICTED on unload, the re-selection
  path EVICTED → SELECTED); the §20 entry gate (discovery first); the
  unload failure leaving ACTIVE (the still-loaded truth);
- **the admission law's honest form**: with no port injected the
  three operations stay UNREGISTERED (machinery without a consumer
  is forbidden — wb-5's law, continued);
- **the composition**: the malformed-port CompositionError (§6.1's
  validate step), the full registration closure, the direct-vs-HTTP
  parity (the wb-4/wb-5 proof pattern over the new surface), the
  byte-deterministic pair, and the cross-PYTHONHASHSEED subprocess
  pair over the chat execution identity.
"""

from __future__ import annotations

import json
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

import pytest

from cli.engine import EngineConfig, LlamaServerClient
from workbench.api.gateway import Gateway
from workbench.api.transport import LoopbackHttpTransport
from workbench.application.clock import AppClock
from workbench.application.operations import backend as backend_module
from workbench.application.operations.backend import (
    CHAT_DEFAULT_MAX_TOKENS,
    CHAT_DEFAULT_TEMPERATURE,
    BackendPort,
    ModelLoadStates,
)
from workbench.application.operations.composition import (
    CompositionError,
    compose_workbench_operations,
)

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tests"))
from test_engine import _StubLlamaServer  # noqa: E402 — the shared stub

_MESSAGES = [{"role": "user", "content": "Rain on the shutters?"}]


# ------------------------------------------------------------ the doubles


class _PortDouble:
    """The in-memory port double: the scripted replies + the recorded
    calls + the optional gate (a threading.Event the chat call waits
    on — the cancellation/deadline trio's blocking arm)."""

    def __init__(
        self,
        *,
        content: str = "Rain started, patient and unhurried.",
        finish: str = "stop",
        chat_error: Exception | None = None,
        props_error: Exception | None = None,
        props: dict[str, Any] | None = None,
        gate: threading.Event | None = None,
        props_gate: threading.Event | None = None,
        load_error: Exception | None = None,
        unload_error: Exception | None = None,
        load_reply: dict[str, Any] | None = None,
    ) -> None:
        self.content = content
        self.finish = finish
        self.chat_error = chat_error
        self.props_error = props_error
        self._props_doc = props if props is not None else {
            "model_path": "/models/stub.gguf",
            "build_info": "b11064-test",
        }
        self.gate = gate
        self.props_gate = props_gate
        self.load_error = load_error
        self.unload_error = unload_error
        self.load_reply = load_reply or {"success": True}
        self.chat_calls: list[dict[str, Any]] = []
        self.load_calls: list[tuple[str, str | None]] = []
        self.unload_calls: list[str] = []
        self.props_calls = 0

    def props(self) -> dict[str, Any]:
        self.props_calls += 1
        if self.props_gate is not None:
            self.props_gate.wait(timeout=10)
        if self.props_error is not None:
            raise self.props_error
        return dict(self._props_doc)

    def chat(
        self,
        messages,
        *,
        grammar=None,
        temperature=CHAT_DEFAULT_TEMPERATURE,
        max_tokens=CHAT_DEFAULT_MAX_TOKENS,
    ):
        self.chat_calls.append({
            "messages": [dict(m) for m in messages],
            "grammar": grammar,
            "temperature": temperature,
            "max_tokens": max_tokens,
        })
        if self.gate is not None:
            self.gate.wait(timeout=10)
        if self.chat_error is not None:
            raise self.chat_error
        return self.content, self.finish

    def load_model(self, model_path, alias=None):
        self.load_calls.append((model_path, alias))
        if self.load_error is not None:
            raise self.load_error
        return dict(self.load_reply)

    def unload_model(self, model_ref):
        self.unload_calls.append(model_ref)
        if self.unload_error is not None:
            raise self.unload_error
        return {"success": True}


class _EngineError(Exception):
    """The adapter-failure double (the port's duck-typed `cause`)."""

    def __init__(self, cause: str, detail: str = "stub") -> None:
        super().__init__(f"[{cause}] {detail}")
        self.cause = cause


def _compose_with_backend(
    tmp_path: Path, port: object
) -> tuple[Gateway, str]:
    gateway = Gateway()
    compose_workbench_operations(
        gateway, tmp_path / "models", AppClock(), backend=port
    )
    session = gateway.dispatch_document({
        "operation": "session.create",
        "arguments": {},
        "client_request_id": "compose-session",
    })
    token = str(session.result["session_id"])
    return gateway, token


def _dispatch(
    gateway: Gateway,
    token: str,
    operation: str,
    arguments: dict[str, Any],
    request_id: str | None = None,
) -> dict[str, Any]:
    document: dict[str, Any] = {
        "operation": operation,
        "arguments": arguments,
        "session_id": token,
    }
    if request_id is not None:
        document["client_request_id"] = request_id
    return gateway.dispatch_document(document)


def _await_terminal(
    gateway: Gateway, token: str, execution_id: str, tries: int = 200
) -> dict[str, Any]:
    """Poll run.get to terminal (the honest caller's form — the
    live-events row delivers streaming later)."""
    for _ in range(tries):
        doc = _dispatch(
            gateway, token, "run.get", {"execution_id": execution_id}
        )
        assert doc.result is not None
        if doc.result["terminal"]:
            return dict(doc.result)
        threading.Event().wait(0.02)
    raise AssertionError("the execution never reached terminal")


def _write_model(tmp_path: Path, name: str = "stub.gguf") -> None:
    models = tmp_path / "models"
    models.mkdir(parents=True, exist_ok=True)
    (models / name).write_bytes(b"the stub model bytes")


def _discover(gateway: Gateway) -> None:
    """The §20 entry gate: discovery first (model.list — the registry
    populates its entries; the load/unload family rides on top)."""
    response = gateway.dispatch_document({
        "operation": "model.list", "arguments": {},
    })
    assert response.status == "OK", response.to_mapping()


# ------------------------------------------------- the port conformance


def test_the_real_adapter_satisfies_the_port(tmp_path: Path) -> None:
    """§4.1/§29: the physical owner (LlamaServerClient) satisfies the
    typed port — structurally (runtime-checkable) and behaviorally
    over the loopback stub (the same client shape the station runs;
    the workbench imports it HERE only — tests were never the runtime
    graph, the INV-4 law)."""
    model = tmp_path / "stub.gguf"
    model.write_bytes(b"the stub model bytes")
    server = _StubLlamaServer(model)
    server.start()
    try:
        client = LlamaServerClient(EngineConfig(endpoint=server.url))
        assert isinstance(client, BackendPort)
        assert client.props()["model_path"] == str(model)
        server.replies.append("ok")
        assert client.chat(
            _MESSAGES, temperature=0.8, max_tokens=32
        ) == ("ok", "stop")
        assert client.load_model(str(model), alias="stub") == {
            "success": True
        }
        assert client.unload_model("stub") == {"success": True}
    finally:
        server.stop()


# ----------------------------------------------------------- chat.send


def test_chat_send_identity_then_observed(tmp_path: Path) -> None:
    """§8 + §19.1: the execution identity returns immediately; the
    OBSERVED document carries content + finish_reason + the backend
    identity; the §10 freeze is observable from admission (the
    messages + the resolved params — the before-side-effects proof
    surface)."""
    _write_model(tmp_path)
    port = _PortDouble()
    gateway, token = _compose_with_backend(tmp_path, port)
    response = _dispatch(
        gateway,
        token,
        "chat.send",
        {"messages": _MESSAGES, "temperature": 0.4, "max_tokens": 77},
        request_id="chat-1",
    )
    result = dict(response.result or {})
    assert result["work"] == "chat.completion"
    assert response.status == "OK"
    run = _await_terminal(gateway, token, str(result["execution_id"]))
    assert run["state"] == "COMPLETED"
    assert run["result"]["content"] == port.content
    assert run["result"]["finish_reason"] == "stop"
    assert run["result"]["backend"] == {
        "model": "/models/stub.gguf",
        "build": "b11064-test",
    }
    # the ACCEPTED layer reached the port verbatim (EFFECTIVE)
    assert port.chat_calls == [{
        "messages": _MESSAGES,
        "grammar": None,
        "temperature": 0.4,
        "max_tokens": 77,
    }]
    # the §10 freeze — the frozen inputs name the request identity
    frozen = dict((k, v) for k, v in run["frozen_inputs"])
    assert frozen["max_tokens"] == "77"
    assert json.loads(frozen["messages"]) == _MESSAGES


def test_chat_send_defaults_and_validation(tmp_path: Path) -> None:
    """The REQUESTED→ACCEPTED layer: the defaults resolve (0.8 / 512);
    the closed argument set, the roles, the ranges — DOMAIN_REJECTED,
    never a clamp."""
    _write_model(tmp_path)
    port = _PortDouble()
    gateway, token = _compose_with_backend(tmp_path, port)
    response = _dispatch(
        gateway, token, "chat.send", {"messages": _MESSAGES},
        request_id="chat-d",
    )
    _await_terminal(gateway, token, str(response.result["execution_id"]))
    call = port.chat_calls[0]
    assert call["temperature"] == CHAT_DEFAULT_TEMPERATURE
    assert call["max_tokens"] == CHAT_DEFAULT_MAX_TOKENS
    assert call["grammar"] is None
    bad_cases = [
        {"messages": []},
        {"messages": "hello"},
        {"messages": [{"role": "user"}]},
        {"messages": [{"role": "tool", "content": "x"}]},
        {"messages": [{"role": "user", "content": ""}]},
        {"messages": [{"role": "user", "content": "x"}], "top_k": 4},
        {"messages": _MESSAGES, "temperature": 3.0},
        {"messages": _MESSAGES, "temperature": "high"},
        {"messages": _MESSAGES, "max_tokens": 0},
        {"messages": _MESSAGES, "max_tokens": 10**9},
    ]
    for index, arguments in enumerate(bad_cases):
        response = _dispatch(
            gateway, token, "chat.send", arguments,
            request_id=f"bad-{index}",
        )
        assert response.status == "REJECTED", arguments
        assert response.rejection == "DOMAIN_REJECTED"


def test_chat_send_backend_failure_closes_the_run(
    tmp_path: Path,
) -> None:
    """The backend's failure is the RUN's failure (§29's matrix rows:
    unavailable/malformed) — the dispatch itself succeeded (the
    identity returned), the truth lands in run.get with the failure
    type named; never a fabricated completion."""
    _write_model(tmp_path)
    port = _PortDouble(
        chat_error=_EngineError("unavailable", "down after the ladder")
    )
    gateway, token = _compose_with_backend(tmp_path, port)
    response = _dispatch(
        gateway, token, "chat.send", {"messages": _MESSAGES},
        request_id="chat-f",
    )
    run = _await_terminal(
        gateway, token, str(response.result["execution_id"])
    )
    assert run["state"] == "FAILED"
    assert run["failure_type"] == "_EngineError"
    assert run["result"] is None


def test_chat_send_failed_props_probe_never_kills_the_chat(
    tmp_path: Path,
) -> None:
    """The identity probe is evidence, not a gate: a failed props
    probe lands the honest "unavailable" note and the chat still
    completes (readiness ≠ identity evidence; never a fabricated
    identity, never a silent skip)."""
    _write_model(tmp_path)
    port = _PortDouble(props_error=_EngineError("unavailable", "props"))
    gateway, token = _compose_with_backend(tmp_path, port)
    response = _dispatch(
        gateway, token, "chat.send", {"messages": _MESSAGES},
        request_id="chat-p",
    )
    run = _await_terminal(
        gateway, token, str(response.result["execution_id"])
    )
    assert run["state"] == "COMPLETED"
    assert run["result"]["backend"]["probe"] == "unavailable"
    assert run["result"]["content"] == port.content


def test_chat_send_cancellation_truth(tmp_path: Path) -> None:
    """§12.3's trio, the chat form: CANCELED when a checkpoint
    observes the request (the props probe blocked, the post-probe
    checkpoint fires on release); FAILED_TO_CANCEL with the result
    RECORDED when the single blocking call lands after the request
    (the late result — never a completion, never a fabricated
    cancellation)."""
    _write_model(tmp_path)
    # arm 1: the request lands between the checkpoints — the
    # post-probe checkpoint observes it and aborts
    props_gate = threading.Event()
    port = _PortDouble(props_gate=props_gate)
    gateway, token = _compose_with_backend(tmp_path, port)
    response = _dispatch(
        gateway, token, "chat.send", {"messages": _MESSAGES},
        request_id="chat-c1",
    )
    execution_id = str(response.result["execution_id"])
    _await_in_flight(lambda: port.props_calls >= 1)
    cancel = _dispatch(
        gateway, token, "run.cancel", {"execution_id": execution_id},
        request_id="cancel-1",
    )
    assert cancel.result["cancellation"] == "CANCEL_REQUESTED"
    props_gate.set()  # release the probe — the checkpoint fires next
    run = _await_terminal(gateway, token, execution_id)
    assert run["state"] == "CANCELED"

    # arm 2: the request lands while the port call is in flight (past
    # every checkpoint — the gate is inside the port call itself)
    gate2 = threading.Event()
    port2 = _PortDouble(gate=gate2)
    gateway2, token2 = _compose_with_backend(tmp_path, port2)
    response2 = _dispatch(
        gateway2, token2, "chat.send", {"messages": _MESSAGES},
        request_id="chat-c2",
    )
    execution2 = str(response2.result["execution_id"])
    _await_in_flight(lambda: bool(port2.chat_calls))
    cancel2 = _dispatch(
        gateway2, token2, "run.cancel", {"execution_id": execution2},
        request_id="cancel-2",
    )
    assert cancel2.result["cancellation"] == "CANCEL_REQUESTED"
    gate2.set()
    run2 = _await_terminal(gateway2, token2, execution2)
    assert run2["state"] == "FAILED_TO_CANCEL"
    assert run2["result"]["content"] == port2.content  # recorded


def _await_in_flight(predicate, tries: int = 200) -> None:
    """Wait until the predicate holds (the in-flight proof — the
    port call is genuinely inside the double before the cancel)."""
    for _ in range(tries):
        if predicate():
            return
        threading.Event().wait(0.02)
    raise AssertionError("the port call never went in flight")


def test_chat_send_deadline_terminal(tmp_path: Path) -> None:
    """§12's absolute deadline: the caller's explicit tiny deadline
    crosses while the props probe is blocked — the post-probe
    checkpoint's DeadlineExceeded is a terminal FAILED, no hidden
    retry loop (§29's matrix row)."""
    _write_model(tmp_path)
    props_gate = threading.Event()
    port = _PortDouble(props_gate=props_gate)
    gateway, token = _compose_with_backend(tmp_path, port)
    response = _dispatch(
        gateway,
        token,
        "chat.send",
        {"messages": _MESSAGES, "deadline_seconds": 0.05},
        request_id="chat-dl",
    )
    execution_id = str(response.result["execution_id"])
    _await_in_flight(lambda: port.props_calls >= 1)
    threading.Event().wait(0.15)  # let the tiny deadline pass
    props_gate.set()
    run = _await_terminal(gateway, token, execution_id)
    assert run["state"] == "FAILED"
    assert run["failure_type"] == "DeadlineExceeded"


def test_chat_send_is_session_owned(tmp_path: Path) -> None:
    """The execution belongs to the dispatching session (the registry's
    session-ownership law): another session's run.get is rejected."""
    _write_model(tmp_path)
    gateway, token = _compose_with_backend(tmp_path, _PortDouble())
    other = str(
        gateway.dispatch_document({
            "operation": "session.create", "arguments": {},
            "client_request_id": "other-session",
        }).result["session_id"]
    )
    response = _dispatch(
        gateway, token, "chat.send", {"messages": _MESSAGES},
        request_id="chat-s",
    )
    execution_id = str(response.result["execution_id"])
    document = {
        "operation": "run.get",
        "arguments": {"execution_id": execution_id},
        "session_id": other,
    }
    reply = gateway.dispatch_document(document)
    assert reply.status == "REJECTED"
    assert reply.rejection == "DOMAIN_REJECTED"


def test_chat_effects_in_ordered_stream(tmp_path: Path) -> None:
    """§13: the dispatch-time effect lands the session's ordered
    stream (CHAT_DISPATCHED, the execution identity carried)."""
    _write_model(tmp_path)
    gateway, token = _compose_with_backend(tmp_path, _PortDouble())
    response = _dispatch(
        gateway, token, "chat.send", {"messages": _MESSAGES},
        request_id="chat-e",
    )
    assert response.status == "OK"
    events = _dispatch(gateway, token, "session.events", {})
    kinds = [
        (e["event_type"], e["payload"].get("effect"))
        for e in events.result["events"]
    ]
    assert ("OPERATION_EFFECT", "CHAT_DISPATCHED") in kinds
    assert kinds.count(("OPERATION_EFFECT", "CHAT_DISPATCHED")) == 1


# ------------------------------------------------------ model.load/unload


def test_model_load_walk_to_active(tmp_path: Path) -> None:
    """§20's chain over the Model ladder: discovery gate → select →
    the observed reply → ACTIVE; the alias = the logical_name; the
    effect lands the stream."""
    _write_model(tmp_path)
    port = _PortDouble()
    gateway, token = _compose_with_backend(tmp_path, port)
    gateway.dispatch_document({
        "operation": "model.list", "arguments": {},
    })  # discovery first — the §20 entry gate
    response = _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="load-1",
    )
    result = dict(response.result or {})
    assert result["state"] == "ACTIVE"
    assert result["logical_name"] == "stub.gguf"
    assert port.load_calls == [
        (str(tmp_path / "models" / "stub.gguf"), "stub.gguf")
    ]
    events = _dispatch(gateway, token, "session.events", {})
    assert any(
        e["payload"].get("effect") == "MODEL_LOADED"
        for e in events.result["events"]
    )


def test_model_load_requires_discovery(tmp_path: Path) -> None:
    """The §20 entry gate: an undiscovered name is DOMAIN_REJECTED
    (model.list first — the registry's own law, never a raw path)."""
    _write_model(tmp_path)
    gateway, token = _compose_with_backend(tmp_path, _PortDouble())
    response = _dispatch(
        gateway, token, "model.load", {"logical_name": "ghost.gguf"},
        request_id="load-g",
    )
    assert response.status == "REJECTED"
    assert "not discovered" in str(response.result)


def test_model_load_already_active_rejected(tmp_path: Path) -> None:
    """The replacement path is a later row: loading an ACTIVE model
    rejects (unload first)."""
    _write_model(tmp_path)
    gateway, token = _compose_with_backend(tmp_path, _PortDouble())
    _discover(gateway)
    for name in ("load-a1", "load-a2"):
        _dispatch(
            gateway, token, "model.load", {"logical_name": "stub.gguf"},
            request_id=name,
        )
    response = _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="load-a3",
    )
    assert response.rejection == "DOMAIN_REJECTED"
    assert "already ACTIVE" in str(response.result)


def test_model_load_observed_failure_is_terminal_failed(
    tmp_path: Path,
) -> None:
    """The backend's observed refusal (http/malformed) walks
    SELECTED → LOADING → FAILED; the re-load rejects loudly — the
    ladder's FAILED is terminal (the recorded gap, D-203) — and the
    gateway outcome is SENT_OUTCOME_UNKNOWN (the call was sent)."""
    _write_model(tmp_path)
    port = _PortDouble(load_error=_EngineError("http", "500"))
    gateway, token = _compose_with_backend(tmp_path, port)
    _discover(gateway)
    response = _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="load-f1",
    )
    assert response.status == "UNKNOWN"
    assert response.rejection == "SENT_OUTCOME_UNKNOWN"
    retry = _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="load-f2",
    )
    assert retry.rejection == "DOMAIN_REJECTED"
    assert "FAILED" in str(retry.result)


def test_model_load_unknown_outcome_rests_selected(
    tmp_path: Path,
) -> None:
    """§12.1's sibling at the model layer: an "unavailable" outcome is
    UNKNOWN, not failed — the state rests SELECTED and the re-load is
    LEGAL (the retry path the caller owns)."""
    _write_model(tmp_path)
    port = _PortDouble(load_error=_EngineError("unavailable", "down"))
    gateway, token = _compose_with_backend(tmp_path, port)
    _discover(gateway)
    response = _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="load-u1",
    )
    assert response.rejection == "SENT_OUTCOME_UNKNOWN"
    # the backend returns — the re-load succeeds
    port.load_error = None
    retry = _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="load-u2",
    )
    assert retry.result["state"] == "ACTIVE"


def test_model_load_success_false_reply_is_observed_refusal(
    tmp_path: Path,
) -> None:
    """The backend answered HTTP 200 with success:false — the observed
    refusal (the stub pins the shape; build-sensitive): FAILED, never
    a silent pass."""
    _write_model(tmp_path)
    port = _PortDouble(load_reply={"success": False, "error": "oom"})
    gateway, token = _compose_with_backend(tmp_path, port)
    _discover(gateway)
    response = _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="load-sf",
    )
    assert response.rejection == "DOMAIN_REJECTED"
    assert "refused" in str(response.result)


def test_model_unload_walk_and_reselection(tmp_path: Path) -> None:
    """ACTIVE → EVICTED on the observed reply; the re-selection path
    (EVICTED → SELECTED — the ladder's own return) makes the second
    load legal; the unload rides the alias."""
    _write_model(tmp_path)
    port = _PortDouble()
    gateway, token = _compose_with_backend(tmp_path, port)
    _discover(gateway)
    _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="ul-1",
    )
    response = _dispatch(
        gateway, token, "model.unload", {"logical_name": "stub.gguf"},
        request_id="ul-2",
    )
    assert response.result["state"] == "EVICTED"
    assert port.unload_calls == ["stub.gguf"]
    # the re-selection: EVICTED → SELECTED → ... → ACTIVE
    again = _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="ul-3",
    )
    assert again.result["state"] == "ACTIVE"


def test_model_unload_failure_leaves_active(tmp_path: Path) -> None:
    """The unload failure performs NO walk — the model's observed
    truth is still ACTIVE (the next unload is legal; the reply is the
    evidence, never a fabricated eviction)."""
    _write_model(tmp_path)
    port = _PortDouble(unload_error=_EngineError("http", "500"))
    gateway, token = _compose_with_backend(tmp_path, port)
    _discover(gateway)
    _dispatch(
        gateway, token, "model.load", {"logical_name": "stub.gguf"},
        request_id="ulf-1",
    )
    response = _dispatch(
        gateway, token, "model.unload", {"logical_name": "stub.gguf"},
        request_id="ulf-2",
    )
    assert response.rejection == "SENT_OUTCOME_UNKNOWN"
    port.unload_error = None
    retry = _dispatch(
        gateway, token, "model.unload", {"logical_name": "stub.gguf"},
        request_id="ulf-3",
    )
    assert retry.result["state"] == "EVICTED"


def test_model_unload_requires_active(tmp_path: Path) -> None:
    """Nothing active to unload: a never-loaded name is rejected with
    the truthful state named."""
    _write_model(tmp_path)
    gateway, token = _compose_with_backend(tmp_path, _PortDouble())
    _discover(gateway)
    response = _dispatch(
        gateway, token, "model.unload", {"logical_name": "stub.gguf"},
        request_id="ulx-1",
    )
    assert response.rejection == "DOMAIN_REJECTED"
    assert "not ACTIVE" in str(response.result)


def test_load_states_document_view(tmp_path: Path) -> None:
    """The tracker's read view: the per-model states + the active
    slot (the diagnostic surface — the registered consumer is a later
    row, the admission law)."""
    loads = ModelLoadStates()
    assert loads.document() == {"states": {}, "active": None}
    loads.select("a.gguf")
    loads.settle_load_success("a.gguf")
    assert loads.document() == {
        "states": {"a.gguf": "ACTIVE"},
        "active": "a.gguf",
    }
    loads.settle_unload_success("a.gguf")
    assert loads.document() == {"states": {"a.gguf": "EVICTED"},
                                "active": None}


def test_load_states_invalid_walk_loud() -> None:
    """The tracker never bypasses its own gate: the wrong-state walk
    raises (the handler's pre-check bypassed = a composition bug,
    loud by design; the transition table's own loudness is
    lifecycles' tested law)."""
    loads = ModelLoadStates()
    loads.select("a.gguf")
    with pytest.raises(Exception, match="not 'ACTIVE'"):
        loads.settle_unload_success("a.gguf")  # SELECTED, not ACTIVE


# ------------------------------------------------------- the composition


def test_no_backend_no_registration(tmp_path: Path) -> None:
    """The admission law's honest form (wb-5's law, continued): with
    no port injected the three backend operations stay UNREGISTERED —
    machinery without a consumer is forbidden."""
    gateway = Gateway()
    ops = compose_workbench_operations(
        gateway, tmp_path / "models", AppClock()
    )
    assert "chat.send" not in gateway.operation_names
    assert "model.load" not in gateway.operation_names
    assert "model.unload" not in gateway.operation_names
    assert ops.model_loads is None


def test_backend_registration_closure(tmp_path: Path) -> None:
    """The full composition closure: the wb-5 five + the wb-6 three +
    wb-8's model.states read + the wb-4 builtins — one name, one
    owner."""
    _write_model(tmp_path)
    gateway = Gateway()
    ops = compose_workbench_operations(
        gateway, tmp_path / "models", AppClock(), backend=_PortDouble()
    )
    expected = {
        "run.start", "run.get", "run.cancel",
        "model.list", "model.inspect",
        "chat.send", "model.load", "model.unload",
        "model.states",
        "session.create", "session.get", "session.attach",
        "session.detach", "session.events", "app.status",
    }
    assert set(gateway.operation_names) == expected
    assert ops.model_loads is not None


def test_malformed_port_is_composition_error(tmp_path: Path) -> None:
    """§6.1's validate step: a port missing members is the loud
    CompositionError at construction, never a mid-dispatch
    AttributeError."""
    gateway = Gateway()

    class _HalfPort:
        def props(self):  # pragma: no cover — never called
            return {}

    with pytest.raises(CompositionError, match="does not satisfy"):
        compose_workbench_operations(
            gateway, tmp_path / "models", AppClock(), backend=_HalfPort()
        )


def test_require_backend_port_vocabulary() -> None:
    with pytest.raises(
        backend_module.BackendPortError, match="'props' is missing"
    ):
        backend_module.require_backend_port(object())


# ------------------------------------------------- parity + determinism


def test_http_parity_over_the_backend_surface(tmp_path: Path) -> None:
    """The wb-4/wb-5 proof pattern over the new surface: the same
    dispatch core serves the direct call and the HTTP binding — the
    backend operations byte-identical both ways (chat.send +
    model.load as the proofs)."""
    import urllib.request

    _write_model(tmp_path)
    gateway, token = _compose_with_backend(tmp_path, _PortDouble())
    _discover(gateway)
    transport = LoopbackHttpTransport(gateway).start()
    try:
        def over_http(document: dict[str, Any]) -> dict[str, Any]:
            request = urllib.request.Request(
                transport.url,
                data=json.dumps(document).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=10) as handle:
                return json.loads(handle.read().decode("utf-8"))

        direct = _dispatch(
            gateway, token, "chat.send", {"messages": _MESSAGES},
            request_id="parity-1",
        )
        http_document = over_http({
            "operation": "chat.send",
            "arguments": {"messages": _MESSAGES},
            "session_id": token,
            "client_request_id": "parity-1-http",
        })
        assert direct.status == http_document["status"] == "OK"
        assert (
            direct.result["work"]
            == http_document["result"]["work"]
            == "chat.completion"
        )
        load_direct = _dispatch(
            gateway, token, "model.load",
            {"logical_name": "stub.gguf"},
            request_id="parity-2",
        )
        # the load walk is one-shot per activation — unload before the
        # HTTP arm loads the same model again (the parity is over the
        # operation semantics, not a duplicated state walk)
        _dispatch(
            gateway, token, "model.unload", {"logical_name": "stub.gguf"},
            request_id="parity-2-unload",
        )
        load_http = over_http({
            "operation": "model.load",
            "arguments": {"logical_name": "stub.gguf"},
            "session_id": token,
            "client_request_id": "parity-2-http",
        })
        assert load_direct.result["state"] == "ACTIVE"
        assert load_http["result"]["state"] == "ACTIVE"
        assert (
            load_direct.result["logical_name"]
            == load_http["result"]["logical_name"]
        )
    finally:
        transport.stop()


def test_chat_execution_identity_byte_deterministic(
    tmp_path: Path,
) -> None:
    """D4, the chat form (the wb-5 pattern): the same inputs under
    the same fixed clock -> the byte-identical chat.send response and
    the byte-identical closed artifact (two fresh compositions; the
    deadline readings are runtime observations — the fixed clock
    holds them identical, the artifact is clock-free by law)."""
    outputs: list[tuple[str, str]] = []
    for _ in range(2):
        _write_model(tmp_path)
        clock = AppClock(monotonic=lambda: 100.0, utc=lambda: 0.0)
        gateway = Gateway(clock=clock)
        compose_workbench_operations(
            gateway, tmp_path / "models", clock, backend=_PortDouble()
        )
        session = gateway.dispatch_document({
            "operation": "session.create", "arguments": {},
            "client_request_id": "the-same-session-key",
        })
        token = str(session.result["session_id"])
        response = _dispatch(
            gateway, token, "chat.send", {"messages": _MESSAGES},
            request_id="determinism",
        )
        run = _await_terminal(
            gateway, token, str(response.result["execution_id"])
        )
        outputs.append(
            (
                json.dumps(
                    response.to_mapping(),
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                json.dumps(
                    run["artifact"],
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            )
        )
    assert outputs[0][0] == outputs[1][0]
    assert outputs[0][1] == outputs[1][1]


def test_chat_identity_cross_pythonhashseed(tmp_path: Path) -> None:
    """The cross-seed pair (the wb-5 packet's own law): the chat
    execution identity is PYTHONHASHSEED-invariant — a subprocess
    under a different seed derives the same identity over the same
    request (the digest derivation is sort-order-closed)."""
    _write_model(tmp_path)
    script = (
        "import json,sys\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, r'" + str(REPO) + "')\n"
        "from workbench.api.gateway import Gateway\n"
        "from workbench.application.clock import AppClock\n"
        "from workbench.application.operations.composition import"
        " compose_workbench_operations\n"
        "class P:\n"
        "    def props(self):\n"
        "        return {'model_path': '/models/stub.gguf',"
        " 'build_info': 'b11064-test'}\n"
        "    def chat(self, m, *, grammar=None, temperature=0.8,"
        " max_tokens=512):\n"
        "        return 'ok', 'stop'\n"
        "    def load_model(self, p, alias=None):\n"
        "        return {'success': True}\n"
        "    def unload_model(self, r):\n"
        "        return {'success': True}\n"
        "g = Gateway()\n"
        "compose_workbench_operations(g,"
        f" Path(r'{tmp_path / 'models'}'), AppClock(), backend=P())\n"
        "s = g.dispatch_document({'operation': 'session.create',"
        " 'arguments': {}, 'client_request_id': 'seed-session'})"
        ".result['session_id']\n"
        "r = g.dispatch_document({'operation': 'chat.send',"
        " 'arguments': {'messages': [{'role': 'user', 'content': 'x'}]},"
        " 'session_id': s, 'client_request_id': 'seed-pair'})\n"
        "print(json.dumps(dict(r.result)))\n"
    )
    outputs = []
    for seed in ("0", "12345"):
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            check=True,
            env={"PYTHONHASHSEED": seed, "PATH": "/usr/bin:/bin"},
        )
        outputs.append(result.stdout)
    assert outputs[0] == outputs[1]
    identity = json.loads(outputs[0])["execution_id"]
    assert len(identity) == 64  # the sha256 content digest form


def test_backend_module_import_closure() -> None:
    """The envelope law, executable: backend.py imports NO cli/, no
    engine, no network (INV-4's two-surface form untouched — the port
    is the seam, the physical wiring the application-entry rows')."""
    import ast

    source = (
        REPO
        / "workbench"
        / "application"
        / "operations"
        / "backend.py"
    ).read_text(encoding="utf-8")
    roots: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    banned = {"cli", "urllib", "http", "socket", "requests", "core"}
    assert roots & banned == set(), roots & banned
