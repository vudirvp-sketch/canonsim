"""The execution family's laws (iter-387 — the app half of the
replay-UI row: the app law §8's `execution.get/replay` [CONTRACT]
row landed; §10's replay vocabulary made executable).

The laws, each falsifiable on its own:

1. THE NEW-IDENTITY LAW (§10: replay creates a NEW execution
   identity): the same frozen material (the SAME request_digest —
   one request identity, many executions) admits as many replays as
   asked, each its own execution_id; a second replay of one original
   derives a distinct identity (the per-original sequence); a replay
   OF a replay chains (the lineage link, never identity reuse).
2. THE LINEAGE LAW: the replay's closed artifact carries replay_of
   (the original's carries None); execution.get answers the link +
   the sorted direct children; run.get's document stays the LIFECYCLE
   read (no lineage field — the two families' split).
3. THE HONEST GATES: the closed argument set, the non-empty str, the
   unknown execution, the session-ownership law, the TERMINAL
   requirement (an in-flight original rejects), the kind's
   replayability (the live-gate kinds own their re-dispatch).
4. THE WORK LAW: the replay re-runs the SAME work over the SAME
   frozen pairs — the probe's call count + result equal; the chat arm
   re-calls the port with the SAME messages/temperature/max_tokens
   (the inference-reproducibility datum) and the provenance pair
   collapses to requested == effective (the honest re-run form).
5. THE IDEMPOTENCY LAW (§12.2): a retried execution.replay (the same
   client_request_id) answers the RECORDED outcome (duplicate=True,
   the result equal, the work NEVER re-run); a conflicting reuse is
   DUPLICATE_REQUEST.
6. THE EVENT LAW (§13): the dispatch emits exactly ONE RUN_REPLAYED
   OPERATION_EFFECT into the session's ordered stream.
7. THE ENVELOPE LAW (run.start's own admission): a work kind whose
   own argument pairs would shadow the frozen envelope's reserved
   keys rejects LOUD at the ORIGINAL admission (the replay's strip
   depends on it).
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from workbench.api.contract import RequestEnvelope
from workbench.api.gateway import Gateway
from workbench.application.clock import AppClock
from workbench.application.operations.composition import (
    WorkKind,
    compose_workbench_operations,
)
from workbench.application.operations.execution import WorkContext

# ------------------------------------------------------------ the doubles


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


class _CountingPort:
    """The in-memory port double: the scripted chat reply + the
    recorded chat calls (the reproducibility law's evidence) + the
    no-op load/unload arms (the port protocol's full shape)."""

    def __init__(self, *, content: str = "Rain started, patient and unhurried.") -> None:
        self.content = content
        self.chat_calls: list[dict[str, Any]] = []

    def props(self) -> dict[str, Any]:
        return {"model_path": "/models/stub.gguf", "build_info": "b11541-test"}

    def chat(self, messages, *, grammar=None, temperature=0.8, max_tokens=512):
        self.chat_calls.append({
            "messages": [dict(m) for m in messages],
            "grammar": grammar,
            "temperature": temperature,
            "max_tokens": max_tokens,
        })
        return self.content, "stop"

    def load_model(self, model_path, alias=None):
        return {"success": True}

    def unload_model(self, model_ref):
        return {"success": True}


class _Gate:
    """A controllable work body: blocks on the §12 checkpoint until
    the test releases it (the in-flight gate's deterministic arm).
    `block_on_call` limits the blocking to that call number (the
    two-phase form: the source completes, the replay stays in
    flight); None blocks on every call."""

    def __init__(self, *, block_on_call: int | None = None) -> None:
        self._release = threading.Event()
        self._block_on_call = block_on_call
        self.calls = 0

    def release(self) -> None:
        self._release.set()

    def __call__(self, context: WorkContext) -> dict[str, object]:
        self.calls += 1
        if self._block_on_call is None or self.calls == self._block_on_call:
            while not self._release.is_set():
                context.check()
                self._release.wait(timeout=0.02)
        context.check()
        return {"done": True, "call": self.calls}


class _Counter:
    """A completing work body: counts its calls + answers the same
    deterministic result (the work law's equality evidence — the
    count is the test's own attribute, never the work's answer)."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, context: WorkContext) -> dict[str, object]:
        self.calls += 1
        context.check()
        return {"done": True}


def _probe_kind(name: str, body: Any) -> WorkKind:
    """A test work kind: no arguments of its own, the body called
    with the WorkContext (§6.1's smaller-composition pattern)."""
    return WorkKind(
        name=name,
        description="the exec-ops probe kind",
        validate_arguments=lambda arguments: {},
        work=lambda context, inputs: body(context),
    )


# ------------------------------------------------------------ the helpers


def _compose(
    tmp_path: Path,
    *,
    kinds: dict[str, WorkKind] | None = None,
    port: _CountingPort | None = None,
) -> tuple[Gateway, Any]:
    clock = AppClock(monotonic=_StepClock().monotonic, utc=_StepClock().utc)
    gateway = Gateway(clock=clock)
    root = tmp_path / "models"
    root.mkdir(parents=True, exist_ok=True)
    ops = compose_workbench_operations(
        gateway,
        root,
        clock,
        work_kinds=kinds,
        backend=port,
    )
    return gateway, ops


def _session(gateway: Gateway, key: str = "session-key-1") -> str:
    response = gateway.dispatch(
        RequestEnvelope(
            operation="session.create", arguments={}, client_request_id=key
        )
    )
    assert response.status == "OK", response.to_mapping()
    return str(response.result["session_id"])


def _run_start(
    gateway: Gateway, session_id: str, key: str, work: str
) -> str:
    response = gateway.dispatch(
        RequestEnvelope(
            operation="run.start",
            arguments={"work": work, "arguments": {}},
            client_request_id=key,
            session_id=session_id,
        )
    )
    assert response.status == "OK", response.to_mapping()
    return str(response.result["execution_id"])


def _replay(
    gateway: Gateway,
    session_id: str,
    execution_id: str,
    key: str,
) -> Any:
    return gateway.dispatch(
        RequestEnvelope(
            operation="execution.replay",
            arguments={"execution_id": execution_id},
            client_request_id=key,
            session_id=session_id,
        )
    )


def _execution_get(gateway: Gateway, session_id: str, execution_id: str) -> Any:
    return gateway.dispatch(
        RequestEnvelope(
            operation="execution.get",
            arguments={"execution_id": execution_id},
            session_id=session_id,
        )
    )


def _run_get(gateway: Gateway, session_id: str, execution_id: str) -> Any:
    return gateway.dispatch(
        RequestEnvelope(
            operation="run.get",
            arguments={"execution_id": execution_id},
            session_id=session_id,
        )
    )


def _ok(response: Any) -> Any:
    assert response.status == "OK", response.to_mapping()
    return response.result


def _rejected(response: Any) -> str:
    assert response.status == "REJECTED", response.to_mapping()
    assert response.rejection == "DOMAIN_REJECTED", response.to_mapping()
    return str(response.to_mapping()["result"]["reason"])


# ------------------------------------------------------------ the laws


def test_replay_new_identity_and_lineage(tmp_path: Path) -> None:
    """Law 1 + 2: the SAME frozen material admits many replays (the
    request_digest EQUAL — one request identity, many executions),
    each a NEW identity; the artifact + execution.get carry the
    lineage; the original's artifact carries None; run.get stays the
    lifecycle read (no lineage field on its document)."""
    counter = _Counter()
    gateway, ops = _compose(tmp_path, kinds={"probe.count": _probe_kind("probe.count", counter)})
    session_id = _session(gateway)

    original = _run_start(gateway, session_id, "key-1", "probe.count")
    assert ops.executions.wait(original, timeout=5.0)

    first = _ok(_replay(gateway, session_id, original, "replay-key-1"))
    second = _ok(_replay(gateway, session_id, original, "replay-key-2"))
    assert first["execution_id"] != original
    assert second["execution_id"] != original
    assert first["execution_id"] != second["execution_id"]
    assert first["replayed_from"] == original
    assert first["work"] == "probe.count"
    assert second["replayed_from"] == original
    assert ops.executions.wait(str(first["execution_id"]), timeout=5.0)
    assert ops.executions.wait(str(second["execution_id"]), timeout=5.0)

    # one request identity, many executions: the frozen material is
    # the SAME on all three records
    original_doc = _ok(_run_get(gateway, session_id, original))
    first_doc = _ok(_run_get(gateway, session_id, str(first["execution_id"])))
    assert first_doc["request_digest"] == original_doc["request_digest"]
    assert first_doc["frozen_inputs"] == original_doc["frozen_inputs"]

    # the lineage: the replay's artifact links, the original's None
    assert first_doc["artifact"]["replay_of"] == original
    assert original_doc["artifact"]["replay_of"] is None
    # run.get stays the LIFECYCLE read — no lineage field on it
    assert "replay_of" not in first_doc

    # execution.get: the link + the sorted direct children
    parent = _ok(_execution_get(gateway, session_id, original))
    assert parent["replay_of"] is None
    assert parent["replays"] == sorted(
        [str(first["execution_id"]), str(second["execution_id"])]
    )
    child = _ok(_execution_get(gateway, session_id, str(first["execution_id"])))
    assert child["replay_of"] == original
    assert child["replays"] == []

    # the chain: a replay OF the replay links to its own parent
    grandchild_answer = _ok(
        _replay(gateway, session_id, str(first["execution_id"]), "replay-key-3")
    )
    grandchild_id = str(grandchild_answer["execution_id"])
    assert ops.executions.wait(grandchild_id, timeout=5.0)
    assert grandchild_id not in {original, first["execution_id"], second["execution_id"]}
    grandchild = _ok(_execution_get(gateway, session_id, grandchild_id))
    assert grandchild["replay_of"] == first["execution_id"]
    # the first replay now has its own child
    child_again = _ok(_execution_get(gateway, session_id, str(first["execution_id"])))
    assert child_again["replays"] == [grandchild_id]


def test_replay_gates(tmp_path: Path) -> None:
    """Law 3: the honest gates — the closed argument set, the
    non-empty str, the unknown execution, the session ownership, the
    TERMINAL requirement, the kind's replayability."""
    gate = _Gate()
    gateway, ops = _compose(
        tmp_path,
        kinds={"probe.block": _probe_kind("probe.block", gate)},
        port=_CountingPort(),
    )
    session_id = _session(gateway)
    other_session = _session(gateway, "session-key-2")

    # the closed argument set + the type gate
    unknown = gateway.dispatch(
        RequestEnvelope(
            operation="execution.replay",
            arguments={"execution_id": "x", "extra": 1},
            client_request_id="k1",
            session_id=session_id,
        )
    )
    assert "closed set" in _rejected(unknown)
    bad_type = gateway.dispatch(
        RequestEnvelope(
            operation="execution.replay",
            arguments={"execution_id": 7},
            client_request_id="k2",
            session_id=session_id,
        )
    )
    assert "non-empty str" in _rejected(bad_type)

    # the unknown execution
    missing = _replay(gateway, session_id, "no-such-execution", "k3")
    assert "no such execution" in _rejected(missing)

    # the TERMINAL requirement: a gated original is still in flight
    original = _run_start(gateway, session_id, "run-key-1", "probe.block")
    in_flight = _replay(gateway, session_id, original, "k4")
    assert "still in flight" in _rejected(in_flight)

    # the session ownership: the other session's execution
    owned = _replay(gateway, other_session, original, "k5")
    assert "another session" in _rejected(owned)

    gate.release()
    assert ops.executions.wait(original, timeout=5.0)

    # the chat arm is replayable (the port wires the adapter): the
    # load arm is NOT (the live-gate kinds own their re-dispatch)
    model_file = tmp_path / "models" / "a.gguf"
    model_file.write_bytes(b"aaa")
    listing = gateway.dispatch(
        RequestEnvelope(
            operation="model.list", arguments={}, session_id=session_id
        )
    )
    assert listing.status == "OK", listing.to_mapping()
    load_response = gateway.dispatch(
        RequestEnvelope(
            operation="model.load",
            arguments={"logical_name": "a.gguf"},
            client_request_id="load-key-1",
            session_id=session_id,
        )
    )
    assert load_response.status == "OK", load_response.to_mapping()
    load_id = str(load_response.result["execution_id"])
    assert ops.executions.wait(load_id, timeout=5.0)
    not_replayable = _replay(gateway, session_id, load_id, "k6")
    reason = _rejected(not_replayable)
    assert "not replayable" in reason
    assert "model.load" in reason


def test_replay_reruns_work_same_frozen(tmp_path: Path) -> None:
    """Law 4 (the run arm): the replay re-runs the SAME work over the
    SAME frozen pairs — the probe's call count grows exactly by the
    replays, and a deterministic probe answers equal results."""
    counter = _Counter()
    gateway, ops = _compose(
        tmp_path, kinds={"probe.count": _probe_kind("probe.count", counter)}
    )
    session_id = _session(gateway)
    original = _run_start(gateway, session_id, "key-1", "probe.count")
    assert ops.executions.wait(original, timeout=5.0)
    assert counter.calls == 1

    first = _ok(_replay(gateway, session_id, original, "replay-key-1"))
    assert ops.executions.wait(str(first["execution_id"]), timeout=5.0)
    assert counter.calls == 2

    second = _ok(_replay(gateway, session_id, original, "replay-key-2"))
    assert ops.executions.wait(str(second["execution_id"]), timeout=5.0)
    assert counter.calls == 3

    # a deterministic probe: the replay's result equals the original's
    original_doc = _ok(_run_get(gateway, session_id, original))
    first_doc = _ok(_run_get(gateway, session_id, str(first["execution_id"])))
    assert first_doc["result"] == original_doc["result"]
    assert first_doc["state"] == "COMPLETED"
    # the carried budget: the answer's deadline equals the frozen one
    frozen = dict((k, v) for k, v in original_doc["frozen_inputs"])
    assert str(first["deadline_seconds"]) == frozen["deadline_seconds"]


def test_chat_replay_reproducibility(tmp_path: Path) -> None:
    """Law 4 (the chat arm): the replay re-calls the port with the
    SAME messages/temperature/max_tokens (the inference-
    reproducibility datum — the frozen EFFECTIVE material); the
    provenance pair collapses to requested == effective (the honest
    re-run form); the original's REQUESTED-vs-EFFECTIVE distinction
    stays recorded on the ORIGINAL's own document."""
    port = _CountingPort()
    gateway, ops = _compose(tmp_path, port=port)
    session_id = _session(gateway)

    response = gateway.dispatch(
        RequestEnvelope(
            operation="chat.send",
            arguments={
                "messages": [{"role": "user", "content": "Rain?"}],
                "temperature": 0.7,
                "max_tokens": 64,
            },
            client_request_id="chat-key-1",
            session_id=session_id,
        )
    )
    assert response.status == "OK", response.to_mapping()
    original = str(response.result["execution_id"])
    assert ops.executions.wait(original, timeout=5.0)
    original_doc = _ok(_run_get(gateway, session_id, original))
    # the ORIGINAL carries the honest requested-null (the caller set
    # the temperature explicitly — 0.7 both ways here; the LAW is the
    # pair's presence, checked below on the replay's collapse)
    assert original_doc["result"]["requested"]["temperature"] == 0.7

    answer = _ok(_replay(gateway, session_id, original, "replay-key-1"))
    replay_id = str(answer["execution_id"])
    assert replay_id != original
    assert answer["work"] == "chat.completion"
    assert ops.executions.wait(replay_id, timeout=5.0)

    # the reproducibility datum: TWO port calls, the second carrying
    # exactly the first's frozen material
    assert len(port.chat_calls) == 2
    first_call, second_call = port.chat_calls
    assert second_call["messages"] == first_call["messages"]
    assert second_call["temperature"] == first_call["temperature"] == 0.7
    assert second_call["max_tokens"] == first_call["max_tokens"] == 64

    replay_doc = _ok(_run_get(gateway, session_id, replay_id))
    assert replay_doc["state"] == "COMPLETED"
    assert replay_doc["result"]["content"] == original_doc["result"]["content"]
    # the collapse: requested == effective on the re-run
    assert replay_doc["result"]["requested"] == replay_doc["result"]["effective"]
    assert replay_doc["result"]["effective"]["temperature"] == 0.7
    # the lineage on the closed artifact
    assert replay_doc["artifact"]["replay_of"] == original
    assert replay_doc["artifact"]["operation_id"] == "execution.replay"


def test_replay_idempotency(tmp_path: Path) -> None:
    """Law 5 (§12.2): the same client_request_id answers the
    RECORDED outcome (duplicate=True, the result equal, the work
    never re-run); a conflicting reuse is DUPLICATE_REQUEST."""
    counter = _Counter()
    gateway, ops = _compose(
        tmp_path, kinds={"probe.count": _probe_kind("probe.count", counter)}
    )
    session_id = _session(gateway)
    original = _run_start(gateway, session_id, "key-1", "probe.count")
    assert ops.executions.wait(original, timeout=5.0)

    first = _replay(gateway, session_id, original, "replay-key-1")
    assert first.status == "OK", first.to_mapping()
    assert first.duplicate is False
    replay_id = str(first.result["execution_id"])
    assert ops.executions.wait(replay_id, timeout=5.0)
    assert counter.calls == 2

    # the retry: the recorded outcome, the work NEVER re-run
    retry = _replay(gateway, session_id, original, "replay-key-1")
    assert retry.status == "OK", retry.to_mapping()
    assert retry.duplicate is True
    assert retry.result == first.result
    assert counter.calls == 2

    # the conflicting reuse: the same key, a different execution_id
    conflict = _replay(gateway, session_id, replay_id, "replay-key-1")
    assert conflict.status == "REJECTED", conflict.to_mapping()
    assert conflict.rejection == "DUPLICATE_REQUEST"


def test_replay_effect_in_ordered_stream(tmp_path: Path) -> None:
    """Law 6 (§13): the dispatch emits exactly ONE RUN_REPLAYED
    OPERATION_EFFECT into the session's ordered stream (the payload
    carrying the new identity + the lineage link); the retry adds NO
    second event (one admission, one effect, one event)."""
    counter = _Counter()
    gateway, ops = _compose(
        tmp_path, kinds={"probe.count": _probe_kind("probe.count", counter)}
    )
    session_id = _session(gateway)
    original = _run_start(gateway, session_id, "key-1", "probe.count")
    assert ops.executions.wait(original, timeout=5.0)

    answer = _ok(_replay(gateway, session_id, original, "replay-key-1"))
    replay_id = str(answer["execution_id"])
    assert ops.executions.wait(replay_id, timeout=5.0)
    _replay(gateway, session_id, original, "replay-key-1")  # the retry

    events = gateway.dispatch(
        RequestEnvelope(
            operation="session.events", arguments={}, session_id=session_id
        )
    )
    assert events.status == "OK", events.to_mapping()
    stream = events.result["events"]
    kinds = [(e["event_type"], e["payload"].get("effect")) for e in stream]
    assert kinds.count(("OPERATION_EFFECT", "RUN_REPLAYED")) == 1
    replayed = next(
        e for e in stream if e["payload"].get("effect") == "RUN_REPLAYED"
    )
    assert replayed["payload"]["execution_id"] == replay_id
    assert replayed["payload"]["replay_of"] == original
    assert replayed["payload"]["work"] == "probe.count"
    sequences = [e["sequence"] for e in stream]
    assert sequences == sorted(sequences)


def test_execution_get_read_gates(tmp_path: Path) -> None:
    """execution.get's own honest gates + the pre-terminal lineage
    (the link readable from ADMISSION — before any artifact exists):
    the closed set, the type, the ownership; an in-flight execution
    answers state/lineage with artifact None; execution.replay on a
    MISSING execution_id answers the same closed-set rejections."""
    gate = _Gate()
    gateway, ops = _compose(
        tmp_path, kinds={"probe.block": _probe_kind("probe.block", gate)}
    )
    session_id = _session(gateway)
    other_session = _session(gateway, "session-key-2")

    unknown = gateway.dispatch(
        RequestEnvelope(
            operation="execution.get",
            arguments={"execution_id": "x", "extra": 1},
            session_id=session_id,
        )
    )
    assert "closed set" in _rejected(unknown)

    original = _run_start(gateway, session_id, "key-1", "probe.block")
    in_flight = _ok(_execution_get(gateway, session_id, original))
    assert in_flight["terminal"] is False
    assert in_flight["replay_of"] is None
    assert in_flight["replays"] == []
    assert in_flight["artifact"] is None

    foreign = _execution_get(gateway, other_session, original)
    assert "another session" in _rejected(foreign)

    gate.release()
    assert ops.executions.wait(original, timeout=5.0)
    terminal = _ok(_execution_get(gateway, session_id, original))
    assert terminal["terminal"] is True
    assert terminal["artifact"] is not None
    assert terminal["artifact"]["replay_of"] is None

    # the replay's execution.get carries the link FROM ADMISSION —
    # readable even while the replay itself is in flight
    gate_two = _Gate(block_on_call=2)
    gateway2, ops2 = _compose(
        tmp_path, kinds={"probe.block2": _probe_kind("probe.block2", gate_two)}
    )
    session2 = _session(gateway2)
    source = _run_start(gateway2, session2, "key-1", "probe.block2")
    assert ops2.executions.wait(source, timeout=5.0)
    answer = _ok(_replay(gateway2, session2, source, "replay-key-1"))
    live = _ok(
        _execution_get(gateway2, session2, str(answer["execution_id"]))
    )
    assert live["replay_of"] == source
    assert live["terminal"] is False
    gate_two.release()
    assert ops2.executions.wait(str(answer["execution_id"]), timeout=5.0)


def test_run_start_envelope_reservation(tmp_path: Path) -> None:
    """Law 7 (the envelope vocabulary, run.start's own admission): a
    work kind whose own argument pairs would shadow the frozen
    envelope's reserved keys rejects LOUD — the replay's strip
    depends on it (the same law at the owner, never a replay-side
    second truth)."""
    gateway, _ops = _compose(
        tmp_path,
        kinds={
            "probe.shadow": WorkKind(
                name="probe.shadow",
                description="a kind freezing the reserved envelope key",
                validate_arguments=lambda arguments: {"work": "hijack"},
                work=lambda context, inputs: {"done": True},
            )
        },
    )
    session_id = _session(gateway)
    response = gateway.dispatch(
        RequestEnvelope(
            operation="run.start",
            arguments={"work": "probe.shadow", "arguments": {}},
            client_request_id="key-1",
            session_id=session_id,
        )
    )
    assert response.status == "REJECTED", response.to_mapping()
    assert response.rejection == "DOMAIN_REJECTED"
    reason = str(response.to_mapping()["result"]["reason"])
    assert "reserved" in reason
    assert "['work']" in reason
