"""wb-4's claim packet (CONTRACTS §5's wb-4 contract, TEST_PLAN §9's
form).

Claim: the one inbound Workbench gateway over application operations
is established — one dispatch core (socket-free), one loopback HTTP
binding (INV-4's second sanctioned module, D-201), the §8 rejection
vocabulary closed and enforced where the session-translation seed
exercises it, the idempotency/revision/lease laws executable, the
§12.1 dispatch-outcome mapping honest (a mutating raise after
admission is SENT_OUTCOME_UNKNOWN, never a fabricated failure), the
§13 ordered-event stream with the RESYNC law, and the GUI/CLI/API
parity as a byte-diff between the direct dispatch and the HTTP path.

Lens: determinism + boundary purity (the closed vocabularies, the
recorded-outcome replay, no clock in any identity, the credential
never serialized).
Prism: the same-input byte-diff rebuild; the cross-PYTHONHASHSEED
subprocess pair; the direct-vs-HTTP byte pair; the AST import-edge
scan over the api package.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import pytest

from workbench.api import contract as api_contract
from workbench.api.contract import (
    DISPATCH_OUTCOME_FOR_STATUS,
    DISPATCH_OUTCOMES,
    DISPATCH_STATUSES,
    ENVELOPE_TYPES,
    EVENT_TYPES,
    EXPOSURES,
    GATEWAY_SCHEMA_IDENTITY,
    GatewayContractError,
    RequestEnvelope,
    ResponseDocument,
    canonical_json,
)
from workbench.api.gateway import (
    Gateway,
    GatewayConfig,
    GatewayCredential,
    GatewayError,
    OperationSpec,
)
from workbench.api.transport import (
    LOOPBACK_HOSTS,
    MAX_BODY_BYTES,
    TransportError,
)
from workbench.application.clock import AppClock

REPO = Path(__file__).resolve().parents[1]


class _StepClock:
    """The deterministic clock double (wb-3's pattern): both domains
    step only when the test moves them — no host-clock trust."""

    def __init__(self) -> None:
        self._mono = 100.0
        self._utc = 1000.0

    def monotonic(self) -> float:
        return self._mono

    def utc(self) -> float:
        return self._utc


def _fixed_clock() -> tuple[AppClock, _StepClock]:
    step = _StepClock()
    return AppClock(monotonic=step.monotonic, utc=step.utc), step


def _gateway(
    config: GatewayConfig | None = None, clock: AppClock | None = None
) -> Gateway:
    return Gateway(
        config=config if config is not None else GatewayConfig(),
        clock=clock,
    )


def _create(
    gateway: Gateway, key: str, label: str | None = None
) -> ResponseDocument:
    arguments: dict[str, Any] = {}
    if label is not None:
        arguments["label"] = label
    return gateway.dispatch(
        RequestEnvelope(
            operation="session.create",
            arguments=arguments,
            client_request_id=key,
        )
    )


def _ok(response: ResponseDocument) -> None:
    assert response.status == "OK", response.to_mapping()


# ------------------------------------------------------------ vocabularies


def test_rejection_vocabulary_is_the_closed_minimum() -> None:
    assert api_contract.REJECTIONS == frozenset(
        {
            "AUTH_FAILED",
            "AUTHZ_DENIED",
            "DUPLICATE_REQUEST",
            "STALE_REVISION",
            "LEASE_EXPIRED",
            "DOMAIN_REJECTED",
            "RUNTIME_FAILED",
            "SENT_OUTCOME_UNKNOWN",
        }
    )


def test_exposure_status_outcome_vocabularies_closed() -> None:
    assert EXPOSURES == frozenset({"LOOPBACK", "LAN", "TUNNEL"})
    assert DISPATCH_STATUSES == frozenset({"OK", "REJECTED", "FAILED", "UNKNOWN"})
    assert DISPATCH_OUTCOMES == frozenset(
        {"NOT_SENT", "SENT_AND_TERMINAL", "SENT_OUTCOME_UNKNOWN"}
    )
    # the §12.1 mapping: every status maps onto exactly one outcome;
    # every rejection is NOT_SENT; UNKNOWN is never a blind retry
    assert set(DISPATCH_OUTCOME_FOR_STATUS) == DISPATCH_STATUSES
    assert set(DISPATCH_OUTCOME_FOR_STATUS.values()) == DISPATCH_OUTCOMES
    assert DISPATCH_OUTCOME_FOR_STATUS["REJECTED"] == "NOT_SENT"
    assert DISPATCH_OUTCOME_FOR_STATUS["UNKNOWN"] == "SENT_OUTCOME_UNKNOWN"


def test_event_type_vocabulary_closed() -> None:
    assert EVENT_TYPES == frozenset(
        {
            "SESSION_CREATED",
            "SESSION_ATTACHED",
            "SESSION_DETACHED",
            "OPERATION_EFFECT",
        }
    )


# -------------------------------------------------------------- envelopes


def test_envelope_roundtrip_strict() -> None:
    envelope = RequestEnvelope(
        operation="session.attach",
        arguments={"label": "chat"},
        client_request_id="key-1",
        session_id="abc",
        expected_revision=2,
        lease_token="lease",
    )
    roundtripped = RequestEnvelope.from_mapping(envelope.to_mapping())
    assert roundtripped == envelope
    assert canonical_json(envelope.to_mapping()) == canonical_json(
        roundtripped.to_mapping()
    )
    # the closed document law: unknown keys are loud
    with pytest.raises(GatewayContractError):
        RequestEnvelope.from_mapping(
            {"operation": "app.status", "unexpected": 1}
        )
    with pytest.raises(GatewayContractError):
        RequestEnvelope.from_mapping({"operation": "no-dots"})
    with pytest.raises(GatewayContractError):
        RequestEnvelope.from_mapping({})


    document = ResponseDocument(
        status="OK", operation_id="d" * 64, result={"a": 1}
    )
    assert ResponseDocument.from_mapping(document.to_mapping()) == document
    with pytest.raises(GatewayContractError):
        ResponseDocument.from_mapping(
            {"status": "OK", "operation_id": "x", "rogue": True}
        )
    with pytest.raises(GatewayContractError):
        ResponseDocument(status="WEIRD", operation_id="x")


def test_envelope_arguments_must_be_json_safe() -> None:
    with pytest.raises(GatewayContractError):
        RequestEnvelope(operation="app.status", arguments={"bad": {1, 2}})
    with pytest.raises(GatewayContractError):
        RequestEnvelope(operation="app.status", arguments={"bad": float("nan")})
    with pytest.raises(GatewayContractError):
        RequestEnvelope(
            operation="app.status",
            arguments={"nested": [{"deeper": object()}]},
        )
    with pytest.raises(GatewayContractError):
        RequestEnvelope(operation="app.status", expected_revision=-1)


def test_material_digest_excludes_the_credential() -> None:
    base = RequestEnvelope(
        operation="session.create",
        arguments={"label": "a"},
        client_request_id="k",
        auth_token="secret-one",
    )
    other_credential = RequestEnvelope(
        operation="session.create",
        arguments={"label": "a"},
        client_request_id="k",
        auth_token="secret-two",
    )
    material_changed = RequestEnvelope(
        operation="session.create",
        arguments={"label": "b"},
        client_request_id="k",
        auth_token="secret-one",
    )
    assert base.material_digest() == other_credential.material_digest()
    assert base.material_digest() != material_changed.material_digest()


def test_envelope_roster_covers_the_roundtrip_pair() -> None:
    assert ENVELOPE_TYPES == (
        RequestEnvelope,
        ResponseDocument,
        api_contract.EventEnvelope,
    )


# ------------------------------------------------------------ session seed


def test_session_create_first_effect() -> None:
    clock, _ = _fixed_clock()
    gateway = _gateway(clock=clock)
    response = _create(gateway, "key-create")
    _ok(response)
    session_id = response.result["session_id"]
    assert response.result["revision"] == 0
    assert response.result["event_sequence"] == 1
    events = gateway.dispatch_document(
        {
            "operation": "session.events",
            "session_id": session_id,
            "arguments": {"since_sequence": 0},
        }
    )
    _ok(events)
    assert events.result["last_sequence"] == 1
    (event,) = events.result["events"]
    assert event["event_type"] == "SESSION_CREATED"
    assert event["sequence"] == 1
    # §17: observed_at is the UTC_WALL reading — the injected clock's
    assert event["observed_at"] == 1000.0


def test_unknown_operation_is_domain_rejected() -> None:
    gateway = _gateway()
    response = gateway.dispatch_document({"operation": "no.such"})
    assert response.status == "REJECTED"
    assert response.rejection == "DOMAIN_REJECTED"


def test_mutation_requires_a_client_request_id() -> None:
    gateway = _gateway()
    response = gateway.dispatch_document({"operation": "session.create"})
    assert response.status == "REJECTED"
    assert response.rejection == "DOMAIN_REJECTED"


def test_duplicate_mutation_replays_one_outcome() -> None:
    clock, _ = _fixed_clock()
    gateway = _gateway(clock=clock)
    first = _create(gateway, "key-dup")
    _ok(first)
    session_id = first.result["session_id"]
    second = _create(gateway, "key-dup")
    _ok(second)
    # the §30 row: the same identity replays the ORIGINAL outcome —
    # one effect, one session, the duplicate marker honest
    assert second.result == first.result
    assert second.duplicate is True
    assert first.duplicate is False
    events = gateway.dispatch_document(
        {
            "operation": "session.events",
            "session_id": session_id,
            "arguments": {"since_sequence": 0},
        }
    )
    _ok(events)
    assert len(events.result["events"]) == 1


def test_conflicting_key_reuse_is_duplicate_request() -> None:
    gateway = _gateway()
    _create(gateway, "key-conflict")
    response = _create(gateway, "key-conflict", label="different")
    assert response.status == "REJECTED"
    assert response.rejection == "DUPLICATE_REQUEST"


def test_session_get_document() -> None:
    clock, _ = _fixed_clock()
    gateway = _gateway(clock=clock)
    created = _create(gateway, "key-get")
    session_id = created.result["session_id"]
    read = gateway.dispatch_document(
        {"operation": "session.get", "session_id": session_id}
    )
    _ok(read)
    assert read.result == {
        "attached": False,
        "created_observed_at": 1000.0,
        "event_sequence": 1,
        "revision": 0,
        "session_id": session_id,
    }
    assert read.session_id == session_id
    assert read.revision == 0
    assert read.sequence == 1
    # the closed-argument law
    bad = gateway.dispatch_document(
        {"operation": "session.get", "session_id": session_id,
         "arguments": {"rogue": 1}}
    )
    assert bad.rejection == "DOMAIN_REJECTED"
    missing = gateway.dispatch_document(
        {"operation": "session.get", "session_id": "nope"}
    )
    assert missing.rejection == "DOMAIN_REJECTED"


def test_attach_bumps_revision_and_emits() -> None:
    clock, _ = _fixed_clock()
    gateway = _gateway(clock=clock)
    session_id = _create(gateway, "key-attach").result["session_id"]
    attached = gateway.dispatch_document(
        {
            "operation": "session.attach",
            "client_request_id": "attach-1",
            "session_id": session_id,
            "expected_revision": 0,
            "arguments": {"label": "chat"},
        }
    )
    _ok(attached)
    assert attached.revision == 1
    assert attached.sequence == 2
    assert attached.result["attached"] is True
    assert attached.result["lease_token"]
    events = gateway.dispatch_document(
        {
            "operation": "session.events",
            "session_id": session_id,
            "arguments": {"since_sequence": 1},
        }
    )
    _ok(events)
    (event,) = events.result["events"]
    assert event["event_type"] == "SESSION_ATTACHED"
    assert event["sequence"] == 2
    assert event["payload"] == {"label": "chat", "observed_at": 1000.0}


def test_stale_revision_cannot_mutate() -> None:
    clock, _ = _fixed_clock()
    gateway = _gateway(clock=clock)
    session_id = _create(gateway, "key-stale").result["session_id"]
    first = gateway.dispatch_document(
        {
            "operation": "session.attach",
            "client_request_id": "attach-a",
            "session_id": session_id,
            "expected_revision": 0,
        }
    )
    _ok(first)
    # the stale writer: revision 0 again after the world moved to 1
    stale = gateway.dispatch_document(
        {
            "operation": "session.attach",
            "client_request_id": "attach-b",
            "session_id": session_id,
            "expected_revision": 0,
        }
    )
    assert stale.status == "REJECTED"
    assert stale.rejection == "STALE_REVISION"
    read = gateway.dispatch_document(
        {"operation": "session.get", "session_id": session_id}
    )
    _ok(read)
    assert read.revision == 1  # untouched
    assert read.result["event_sequence"] == 2  # no event for the rejection
    absent = gateway.dispatch_document(
        {
            "operation": "session.attach",
            "client_request_id": "attach-c",
            "session_id": session_id,
        }
    )
    assert absent.rejection == "DOMAIN_REJECTED"


def test_lease_lifecycle_and_expiry() -> None:
    clock, step = _fixed_clock()
    gateway = _gateway(clock=clock)
    session_id = _create(gateway, "key-lease").result["session_id"]
    attached = gateway.dispatch_document(
        {
            "operation": "session.attach",
            "client_request_id": "lease-attach",
            "session_id": session_id,
            "expected_revision": 0,
        }
    )
    _ok(attached)
    lease = attached.result["lease_token"]
    # expiry on the MONOTONIC domain: step past the window
    step._mono += 31.0
    expired = gateway.dispatch_document(
        {
            "operation": "session.detach",
            "client_request_id": "detach-late",
            "session_id": session_id,
            "expected_revision": 1,
            "lease_token": lease,
        }
    )
    assert expired.status == "REJECTED"
    assert expired.rejection == "LEASE_EXPIRED"
    read = gateway.dispatch_document(
        {"operation": "session.get", "session_id": session_id}
    )
    _ok(read)
    assert read.revision == 1  # the expired lease mutated nothing
    # the valid window detaches cleanly
    step._mono -= 31.0
    reattached = gateway.dispatch_document(
        {
            "operation": "session.attach",
            "client_request_id": "lease-reattach",
            "session_id": session_id,
            "expected_revision": 1,
        }
    )
    _ok(reattached)
    detached = gateway.dispatch_document(
        {
            "operation": "session.detach",
            "client_request_id": "detach-now",
            "session_id": session_id,
            "expected_revision": 2,
            "lease_token": reattached.result["lease_token"],
        }
    )
    _ok(detached)
    assert detached.revision == 3


# ----------------------------------------------------------- auth + law


def test_auth_failed_when_required_and_missing_or_wrong() -> None:
    config = GatewayConfig(
        auth_required=True,
        credentials=(GatewayCredential(token="tok", principal="op"),),
    )
    gateway = _gateway(config=config)
    missing = gateway.dispatch_document({"operation": "app.status"})
    assert missing.status == "REJECTED"
    assert missing.rejection == "AUTH_FAILED"
    wrong = gateway.dispatch_document(
        {"operation": "app.status", "auth_token": "not-the-token"}
    )
    assert wrong.rejection == "AUTH_FAILED"


def test_authz_denied_when_operation_out_of_scope() -> None:
    config = GatewayConfig(
        auth_required=True,
        credentials=(
            GatewayCredential(
                token="tok",
                principal="reader",
                allowed_operations=frozenset({"session.get"}),
            ),
        ),
    )
    gateway = _gateway(config=config)
    denied = gateway.dispatch_document(
        {"operation": "app.status", "auth_token": "tok"}
    )
    assert denied.status == "REJECTED"
    assert denied.rejection == "AUTHZ_DENIED"
    allowed = gateway.dispatch_document(
        {"operation": "session.get", "auth_token": "tok",
         "session_id": "any"}
    )
    assert allowed.rejection != "AUTHZ_DENIED"  # authz passed (domain
    # rejection is the session's own)


def test_non_loopback_exposure_refuses_to_start_without_auth() -> None:
    with pytest.raises(GatewayError):
        GatewayConfig(exposure="LAN")
    with pytest.raises(GatewayError):
        GatewayConfig(exposure="TUNNEL")
    with pytest.raises(GatewayError):
        GatewayConfig(auth_required=True)  # no credentials: nothing
        # could ever authenticate
    with_auth = GatewayConfig(
        exposure="LAN",
        auth_required=True,
        credentials=(GatewayCredential(token="t", principal="op"),),
    )
    assert with_auth.exposure == "LAN"


def test_credential_scope_form_is_validated() -> None:
    with pytest.raises(GatewayError):
        GatewayCredential(token="t", principal="p",
                          allowed_operations=frozenset({"nodots"}))


# ---------------------------------------------------- dispatch outcomes


def test_read_failure_maps_runtime_failed() -> None:
    gateway = _gateway()

    def boom(_context: Any) -> dict[str, Any]:
        raise RuntimeError("read exploded")

    gateway.register(
        OperationSpec(name="probe.read", kind="READ", handler=boom)
    )
    response = gateway.dispatch_document({"operation": "probe.read"})
    assert response.status == "FAILED"
    assert response.rejection == "RUNTIME_FAILED"
    assert response.result == {"error_type": "RuntimeError"}
    assert response.dispatch_outcome() == "SENT_AND_TERMINAL"


def test_mutation_failure_maps_sent_outcome_unknown() -> None:
    gateway = _gateway()

    def boom(_context: Any) -> dict[str, Any]:
        raise RuntimeError("mutation exploded mid-flight")

    gateway.register(
        OperationSpec(
            name="probe.mutate",
            kind="MUTATION",
            handler=boom,
        )
    )
    first = gateway.dispatch_document(
        {"operation": "probe.mutate", "client_request_id": "k"}
    )
    assert first.status == "UNKNOWN"
    assert first.rejection == "SENT_OUTCOME_UNKNOWN"
    assert first.dispatch_outcome() == "SENT_OUTCOME_UNKNOWN"
    # the recorded UNKNOWN blocks the blind retry (§12.1): the retry
    # replays the UNKNOWN, never re-attempts
    retry = gateway.dispatch_document(
        {"operation": "probe.mutate", "client_request_id": "k"}
    )
    assert retry.status == "UNKNOWN"
    assert retry.duplicate is True


# ------------------------------------------------------ events + resync


def test_events_replay_ordered_since_sequence() -> None:
    clock, _ = _fixed_clock()
    gateway = _gateway(clock=clock)
    session_id = _create(gateway, "key-events").result["session_id"]
    for revision in range(3):
        attached = gateway.dispatch_document(
            {
                "operation": "session.attach",
                "client_request_id": f"attach-{revision}",
                "session_id": session_id,
                "expected_revision": revision,
            }
        )
        _ok(attached)
    detached = gateway.dispatch_document(
        {
            "operation": "session.detach",
            "client_request_id": "detach-final",
            "session_id": session_id,
            "expected_revision": 3,
            "lease_token": None,
        }
    )
    # the detach without a valid lease: LEASE_EXPIRED (the attach left
    # a live lease; detach requires the token) — the stream's last
    # effect is the third attach
    assert detached.rejection == "LEASE_EXPIRED"
    events = gateway.dispatch_document(
        {
            "operation": "session.events",
            "session_id": session_id,
            "arguments": {"since_sequence": 2},
        }
    )
    _ok(events)
    sequences = [event["sequence"] for event in events.result["events"]]
    assert sequences == [3, 4]
    types = [event["event_type"] for event in events.result["events"]]
    assert types == ["SESSION_ATTACHED", "SESSION_ATTACHED"]
    assert events.result["last_sequence"] == 4


def test_resync_required_beyond_retention() -> None:
    clock, _ = _fixed_clock()
    gateway = _gateway(
        config=GatewayConfig(retention_events=3), clock=clock
    )
    session_id = _create(gateway, "key-resync").result["session_id"]
    for revision in range(4):
        attached = gateway.dispatch_document(
            {
                "operation": "session.attach",
                "client_request_id": f"attach-{revision}",
                "session_id": session_id,
                "expected_revision": revision,
            }
        )
        _ok(attached)
    # five effects, three retained: since 0 is beyond the window
    stale = gateway.dispatch_document(
        {
            "operation": "session.events",
            "session_id": session_id,
            "arguments": {"since_sequence": 0},
        }
    )
    _ok(stale)
    assert stale.result["resync"] == "RESYNC_REQUIRED"
    assert stale.result["retained_from"] == 3
    assert stale.result["snapshot"]["revision"] == 4
    assert stale.result["snapshot"]["event_sequence"] == 5
    # inside the window: the ordered replay continues
    fresh = gateway.dispatch_document(
        {
            "operation": "session.events",
            "session_id": session_id,
            "arguments": {"since_sequence": 3},
        }
    )
    _ok(fresh)
    assert [event["sequence"] for event in fresh.result["events"]] == [4, 5]


def test_app_status_is_construction_stable() -> None:
    gateway = _gateway()
    first = gateway.dispatch_document(
        {"operation": "app.status", "client_request_id": "key-status"}
    )
    _ok(first)
    assert first.result == {
        "service": "canonsim-workbench-gateway",
        "contract": GATEWAY_SCHEMA_IDENTITY,
        "exposure": "LOOPBACK",
        "auth_required": False,
        "operations": [
            "app.status",
            "session.attach",
            "session.create",
            "session.detach",
            "session.events",
            "session.get",
        ],
    }
    # parity precondition: the second dispatch is byte-identical
    # (the keyed request's logical identity is stable, G6)
    second = gateway.dispatch_document(
        {"operation": "app.status", "client_request_id": "key-status"}
    )
    assert canonical_json(first.to_mapping()) == canonical_json(
        second.to_mapping()
    )


# ---------------------------------------------------- registered surface


def test_registered_operations_wire_and_dispatch() -> None:
    gateway = _gateway()
    captured: dict[str, Any] = {}

    def echo(context: Any) -> dict[str, Any]:
        captured["context"] = context
        return {"echo": dict(context.arguments), "seen": context.operation}

    gateway.register(
        OperationSpec(
            name="probe.echo",
            kind="READ",
            handler=echo,
            description="the registration-surface proof",
        )
    )
    response = gateway.dispatch_document(
        {"operation": "probe.echo", "arguments": {"word": "hi"}}
    )
    _ok(response)
    assert response.result == {"echo": {"word": "hi"}, "seen": "probe.echo"}
    context = captured["context"]
    assert context.operation_id == response.operation_id
    assert context.session is None
    # one name, one owner — the duplicate registration is loud
    with pytest.raises(GatewayError):
        gateway.register(
            OperationSpec(name="probe.echo", kind="READ", handler=echo)
        )
    # the guard-flag validation
    with pytest.raises(GatewayError):
        OperationSpec(
            name="probe.bad", kind="READ", handler=echo, requires_lease=True
        )


# ---------------------------------------------------------- determinism


def test_gateway_response_serialization_deterministic() -> None:
    first_clock, _ = _fixed_clock()
    second_clock, _ = _fixed_clock()
    first = _gateway(clock=first_clock)
    second = _gateway(clock=second_clock)
    first_response = _create(first, "key-det")
    second_response = _create(second, "key-det")
    assert canonical_json(first_response.to_mapping()) == canonical_json(
        second_response.to_mapping()
    )
    assert first_response.result["session_id"] == second_response.result[
        "session_id"
    ]


def test_cross_pythonhashseed_pair() -> None:
    """The D4 read-side discipline, subprocess form (wb-3's pattern):
    the response document is byte-identical under PYTHONHASHSEED=0 and
    PYTHONHASHSEED=1 — no dict-order or hash dependence anywhere in
    the identity chain."""
    code = "\n".join(
        [
            "import json, sys",
            "sys.path.insert(0, {!r})".format(str(REPO)),
            "from workbench.api.gateway import Gateway",
            "from workbench.api.contract import RequestEnvelope",
            "from workbench.application.clock import AppClock",
            "clock = AppClock(monotonic=lambda: 100.0, utc=lambda: 1000.0)",
            "gateway = Gateway(clock=clock)",
            "response = gateway.dispatch(RequestEnvelope(",
            "    operation='session.create',",
            "    arguments={'label': 'chat'},",
            "    client_request_id='key-seed',",
            "))",
            "print(json.dumps(response.to_mapping(), sort_keys=True,",
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
            timeout=60,
            check=True,
        )
        outputs.append(completed.stdout)
    assert outputs[0] == outputs[1]


# ------------------------------------------------- transport + parity


def _post(url: str, document: Any) -> tuple[int, dict[str, Any]]:
    body = json.dumps(document).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as opened:
        return opened.status, json.loads(opened.read())


def test_operation_semantics_parity_direct_vs_http() -> None:
    """§30's row / §22: the same dispatch core serves the direct call
    and the HTTP path — byte-identical response documents for the
    same request (the parity proof, G2)."""
    clock, _ = _fixed_clock()
    gateway = _gateway(clock=clock)
    envelope = {
        "operation": "app.status",
        "client_request_id": "key-parity",
    }
    direct = gateway.dispatch_document(envelope)
    transport = None
    try:
        from workbench.api.transport import LoopbackHttpTransport

        transport = LoopbackHttpTransport(gateway).start()
        status, http_document = _post(transport.url, envelope)
        assert status == 200
        direct_bytes = canonical_json(direct.to_mapping())
        http_bytes = canonical_json(http_document)
        assert direct_bytes == http_bytes
    finally:
        if transport is not None:
            transport.stop()


def test_transport_refuses_non_loopback_host() -> None:
    from workbench.api.transport import LoopbackHttpTransport

    gateway = _gateway()
    for host in ("0.0.0.0", "192.168.1.5", "example.org"):
        with pytest.raises(TransportError):
            LoopbackHttpTransport(gateway, host=host)
    assert "localhost" in LOOPBACK_HOSTS


def test_transport_roundtrip_lifecycle() -> None:
    from workbench.api.transport import LoopbackHttpTransport

    clock, _ = _fixed_clock()
    gateway = _gateway(clock=clock)
    transport = LoopbackHttpTransport(gateway).start()
    try:
        assert transport.port != 0
        status, created = _post(
            transport.url,
            {
                "operation": "session.create",
                "client_request_id": "key-http",
                "arguments": {"label": "chat"},
            },
        )
        assert status == 200
        assert created["status"] == "OK"
        session_id = created["result"]["session_id"]
        status, read = _post(
            transport.url,
            {"operation": "session.get", "session_id": session_id},
        )
        assert status == 200
        assert read["status"] == "OK"
        assert read["result"]["revision"] == 0
        # a semantic rejection rides HTTP 200 (delivery succeeded)
        status, rejected = _post(
            transport.url, {"operation": "no.such"}
        )
        assert status == 200
        assert rejected["rejection"] == "DOMAIN_REJECTED"
    finally:
        transport.stop()
    transport.stop()  # idempotent
    transport.start().stop()  # restartable after a clean stop


def test_transport_body_guards() -> None:
    from workbench.api.transport import LoopbackHttpTransport

    gateway = _gateway()
    transport = LoopbackHttpTransport(gateway).start()
    try:
        # not JSON
        request = urllib.request.Request(
            transport.url, data=b"not json", method="POST"
        )
        try:
            urllib.request.urlopen(request, timeout=10)
            raised = False
        except urllib.error.HTTPError as exc:
            raised = exc.code == 400
            body = json.loads(exc.read())
            assert body["error"] == "BODY_NOT_JSON"
        assert raised
        # oversized body
        request = urllib.request.Request(
            transport.url,
            data=b"0" * (MAX_BODY_BYTES + 1),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(request, timeout=10)
            raised = False
        except urllib.error.HTTPError as exc:
            raised = exc.code == 400
            body = json.loads(exc.read())
            assert body["error"] == "BODY_TOO_LARGE"
        assert raised
        # valid JSON but a malformed envelope: the semantic path
        status, document = _post(transport.url, {"operation": "app"})
        assert status == 200
        assert document["rejection"] == "DOMAIN_REJECTED"
        # the wrong path / wrong method
        request = urllib.request.Request(
            transport.url.replace("/op", "/other"), data=b"{}", method="POST"
        )
        try:
            urllib.request.urlopen(request, timeout=10)
            raised = False
        except urllib.error.HTTPError as exc:
            raised = exc.code == 404
        assert raised
        try:
            urllib.request.urlopen(transport.url, timeout=10)
            raised = False
        except urllib.error.HTTPError as exc:
            raised = exc.code == 405
        assert raised
    finally:
        transport.stop()


# ------------------------------------------------------ secrets + edges


def test_credential_never_serializes() -> None:
    config = GatewayConfig(
        auth_required=True,
        credentials=(GatewayCredential(token="tok", principal="op"),),
    )
    clock, _ = _fixed_clock()
    gateway = _gateway(config=config, clock=clock)
    created = gateway.dispatch_document(
        {
            "operation": "session.create",
            "client_request_id": "key-secret",
            "auth_token": "tok",
        }
    )
    _ok(created)
    session_id = created.result["session_id"]
    events = gateway.dispatch_document(
        {
            "operation": "session.events",
            "session_id": session_id,
            "arguments": {"since_sequence": 0},
            "auth_token": "tok",
        }
    )
    _ok(events)
    status = gateway.dispatch_document(
        {"operation": "app.status", "auth_token": "tok"}
    )
    _ok(status)
    serialized = canonical_json(
        {
            "created": created.to_mapping(),
            "events": events.to_mapping(),
            "status": status.to_mapping(),
        }
    )
    assert "tok" not in serialized


# --------------------------------------------------- architecture edges


def _import_roots(path: Path) -> set[str]:
    """Top-level roots AND full dotted module paths (the edge checks
    need both forms: `import workbench.api.transport` and `from
    workbench.api.transport import ...` must both be caught)."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name)
                roots.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module)
            roots.add(node.module.split(".")[0])
    return roots


def test_gateway_core_is_socket_free_and_edge_clean() -> None:
    """G1/G7 executable: the semantic core (__init__/contract/gateway)
    imports no network module and never the transport (transport.py is
    the sanctioned socket — the architecture test pins its
    exclusivity); nothing in the api package imports cli/brief/core
    (the §6.2 forbidden edges — no backend transport, no CanonSim
    internals, no persistence)."""
    api = REPO / "workbench" / "api"
    network = {"socket", "urllib", "http", "requests"}
    forbidden = {"cli", "brief", "core"}
    for path in sorted(api.glob("*.py")):
        roots = _import_roots(path)
        edges = roots & forbidden
        assert not edges, f"{path.name}: forbidden edge {sorted(edges)}"
        if path.name == "transport.py":
            continue
        hits = roots & network
        assert not hits, f"{path.name}: network import {sorted(hits)} (G1)"
        assert "workbench.api.transport" not in roots, (
            f"{path.name}: the semantic core never imports the "
            "transport (the socket stays one module deep)"
        )


def test_api_dependency_envelope_stdlib_only() -> None:
    """G7/§27: workbench/api imports only stdlib + workbench — zero
    third-party roots, agreeing with the application envelope."""
    import sys

    api = REPO / "workbench" / "api"
    for path in sorted(api.glob("*.py")):
        roots = _import_roots(path)
        top_level = {root.split(".")[0] for root in roots}
        foreign = {
            root
            for root in top_level
            if root not in sys.stdlib_module_names and root != "workbench"
        }
        assert not foreign, f"{path.name}: third-party {sorted(foreign)}"


def test_inv4_exception_is_exactly_two_modules() -> None:
    """The D-201 + D-208 pins: the architecture test's sanctioned
    surface is exactly the outbound adapter + the inbound gateway
    binding + the outbound model-assets fetch (wb-9's owner-gated
    exception — one per direction-and-asset)."""
    spec = importlib.util.spec_from_file_location(
        "test_architecture", REPO / "tests" / "test_architecture.py"
    )
    assert spec is not None and spec.loader is not None
    architecture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(architecture)
    assert architecture.NETWORK_EXCEPTIONS == frozenset(
        {
            architecture.REPO / "cli" / "engine.py",
            architecture.REPO / "workbench" / "api" / "transport.py",
            architecture.REPO / "workbench" / "platform" / "model_fetch.py",
        }
    )
