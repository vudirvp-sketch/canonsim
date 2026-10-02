"""iter-305's claim packet (the SSE stream contract, TEST_PLAN §9's
form).

Claim: the streaming admission's step 2 (FRONTEND_WEB_LAW §5's
order) is established — the §13 one-way event direction has its
explicit gateway contract, BACKEND FIRST:

- the core half (socket-free, G1): `Gateway.subscribe` answers
  §13's dual (REPLAY window + live tail, or RESYNC snapshot + live
  tail) under the SAME coarse lock `_emit` appends under — the
  replay/live boundary gapless by construction (no gap, no
  duplicate); the per-subscriber delivery buffer is bounded with an
  observable overflow terminal (the queued events drain first, then
  the channel closes; the retained stream — the canonical record —
  never drops); `stream_buffer_events <= retention_events` is
  construction law, so a consumer that overflowed ALWAYS reconnects
  into a replay (never a second resync); `close_subscriptions` is
  the bounded-shutdown wake; a disconnect (client or server) never
  implicitly cancels unrelated execution.
- the delivery half (transport, INV-4's sanctioned socket): GET
  /events with `session_id` + `since_sequence` (the SSE
  Last-Event-ID header the standard's fallback cursor), the frame
  vocabulary closed (stream.open / the EVENT_TYPES event frames /
  stream.overflow / stream.close / stream.rejected), the event
  frames' `data` byte-identical to what `session.events` replays
  (the D4 parity law's stream arm), the heartbeat comment cadence,
  the pre-stream 4xx guards (malformed wire input never reaches the
  core; the auth-required refusal — auth material never rides
  URLs), the semantic rejection riding ONE frame at HTTP 200 (the
  §8 delivery/semantics split holds on the stream surface), and the
  bounded `stop()` waking every live writer (the honest stream.close
  frame, not a vanished socket).

Lens: determinism + boundary purity (the closed vocabularies, the
byte parity, no second truth channel — the SSE stream is a DELIVERY
of the same ordered events, never a parallel event source).
Prism: the direct-subscribe vs parsed-SSE-frames parity; the byte
parity against `session.events`; the real-socket frame reads over
http.client; the thread-count observation (one handler thread per
stream, no pools).
"""

from __future__ import annotations

import http.client
import json
import threading
import time
from typing import Any

import pytest

from workbench.api.contract import EVENT_TYPES, canonical_json
from workbench.api.gateway import (
    DEFAULT_STREAM_BUFFER_EVENTS,
    STREAM_CLOSE_REASONS,
    SUBSCRIPTION_MODES,
    SUBSCRIPTION_STATES,
    Gateway,
    GatewayConfig,
    GatewayError,
    StreamClosed,
    StreamEvent,
    StreamOverflow,
    StreamRejection,
    Subscription,
)
from workbench.api.transport import (
    DEFAULT_HEARTBEAT_SECONDS,
    DEFAULT_STREAM_WRITE_SECONDS,
    STREAM_FRAME_TYPES,
    STREAM_ROUTE,
    TransportError,
)


def _gateway(
    config: GatewayConfig | None = None,
) -> Gateway:
    return Gateway(config=config if config is not None else GatewayConfig())


def _create(gateway: Gateway, key: str) -> str:
    response = gateway.dispatch_document(
        {
            "operation": "session.create",
            "client_request_id": key,
            "arguments": {"label": key},
        }
    )
    assert response.status == "OK", response.to_mapping()
    return str(response.result["session_id"])


def _attach(gateway: Gateway, session_id: str, revision: int, key: str) -> None:
    response = gateway.dispatch_document(
        {
            "operation": "session.attach",
            "session_id": session_id,
            "client_request_id": key,
            "expected_revision": revision,
            "arguments": {"label": key},
        }
    )
    assert response.status == "OK", response.to_mapping()


def _events_answer(
    gateway: Gateway, session_id: str, since: int
) -> dict[str, Any]:
    response = gateway.dispatch_document(
        {
            "operation": "session.events",
            "session_id": session_id,
            "arguments": {"since_sequence": since},
        }
    )
    assert response.status == "OK", response.to_mapping()
    return dict(response.result)


# ---------------------------------------------------------- vocabularies


def test_stream_vocabularies_are_closed() -> None:
    """The closed-set law: the subscription modes/states, the framed
    close reasons, and the SSE control frames are each an exact,
    tested membership — a silent member is a bug."""
    assert SUBSCRIPTION_MODES == frozenset({"REPLAY", "RESYNC"})
    assert SUBSCRIPTION_STATES == frozenset({"OPEN", "OVERFLOW", "CLOSED"})
    assert STREAM_CLOSE_REASONS == frozenset({"SHUTDOWN"})
    assert STREAM_FRAME_TYPES == frozenset(
        {"stream.open", "stream.rejected", "stream.overflow", "stream.close"}
    )
    # The event frames ride the contract's own EVENT_TYPES — the
    # stream invents no event vocabulary of its own.
    assert "SESSION_CREATED" in EVENT_TYPES
    assert "OPERATION_EFFECT" in EVENT_TYPES


def test_stream_buffer_ceiling_is_construction_law() -> None:
    """§13/§26: the buffer ceiling is explicit and loud — a
    non-positive value or one beyond retention (the
    overflow-reconnect-always-replays invariant) refuses at
    construction, never a silent clamp."""
    assert DEFAULT_STREAM_BUFFER_EVENTS == 64
    with pytest.raises(GatewayError):
        GatewayConfig(stream_buffer_events=0)
    with pytest.raises(GatewayError):
        GatewayConfig(stream_buffer_events=-1)
    with pytest.raises(GatewayError):
        GatewayConfig(retention_events=8, stream_buffer_events=9)
    # the boundary itself is legal (buffer == retention)
    GatewayConfig(retention_events=8, stream_buffer_events=8)


def test_transport_cadence_params_are_construction_law() -> None:
    """The heartbeat and the write bound are positive numbers, loud
    at construction (a sub-second test heartbeat is the same law as
    the proof runner's ephemeral port)."""
    from workbench.api.transport import LoopbackHttpTransport

    assert DEFAULT_HEARTBEAT_SECONDS == 15.0
    assert DEFAULT_STREAM_WRITE_SECONDS == 30.0
    gateway = _gateway()
    with pytest.raises(TransportError):
        LoopbackHttpTransport(gateway, heartbeat_seconds=0)
    with pytest.raises(TransportError):
        LoopbackHttpTransport(gateway, stream_write_seconds=-1)


# ------------------------------------------------------------ the core


def test_subscribe_validates_arguments_loudly() -> None:
    gateway = _gateway()
    with pytest.raises(GatewayError):
        gateway.subscribe("", 0)
    with pytest.raises(GatewayError):
        gateway.subscribe("nope", -1)
    with pytest.raises(GatewayError):
        gateway.subscribe("nope", True)  # type: ignore[arg-type]
    with pytest.raises(GatewayError):
        gateway.subscribe(None, 0)  # type: ignore[arg-type]


def test_subscribe_rejected_for_unknown_session() -> None:
    """The rejected lane: an unknown session answers the closed §8
    vocabulary — the same verdict a POST `session.events` would
    answer, never a fabricated transport failure."""
    gateway = _gateway()
    answer = gateway.subscribe("no-such-session", 0)
    assert isinstance(answer, StreamRejection)
    assert answer.rejection == "DOMAIN_REJECTED"
    assert "no such session" in answer.reason
    with pytest.raises(GatewayError):
        StreamRejection(rejection="INVENTED", reason="x")
    with pytest.raises(GatewayError):
        StreamRejection(rejection="DOMAIN_REJECTED", reason="")


def test_subscribe_replay_is_the_events_window() -> None:
    """The parity law's core arm: the REPLAY window is EXACTLY the
    window `session.events` replays for the same cursor — the same
    envelopes, the same order."""
    gateway = _gateway()
    session_id = _create(gateway, "parity")
    for revision in range(3):
        _attach(gateway, session_id, revision, f"attach-{revision}")
    for since in (0, 1, 2, 3, 4):
        answer = gateway.subscribe(session_id, since)
        assert isinstance(answer, Subscription)
        assert answer.mode == "REPLAY"
        replayed = [event.to_mapping() for event in answer.replay]
        assert replayed == _events_answer(gateway, session_id, since)["events"]
        assert answer.last_sequence == 4


def test_subscribe_resync_matches_the_events_answer() -> None:
    """The RESYNC arm: the snapshot document is the SAME bounded
    current snapshot `session.events` answers beyond retention."""
    gateway = _gateway(
        GatewayConfig(retention_events=3, stream_buffer_events=1)
    )
    session_id = _create(gateway, "resync")
    for revision in range(4):
        _attach(gateway, session_id, revision, f"attach-{revision}")
    answer = gateway.subscribe(session_id, 0)
    assert isinstance(answer, Subscription)
    assert answer.mode == "RESYNC"
    assert answer.resync_document is not None
    expected = _events_answer(gateway, session_id, 0)
    for key in ("last_sequence", "resync", "retained_from", "snapshot"):
        assert answer.resync_document[key] == expected[key]
    assert answer.resync_document["snapshot"]["revision"] == 4
    assert answer.replay == ()
    answer.close()


def test_replay_live_boundary_is_gapless() -> None:
    """THE core guarantee: subscribe runs under the same coarse lock
    `_emit` appends under — the replay ends at `last_sequence`, the
    live queue starts at `last_sequence + 1`; events dispatched
    after the open arrive live, in order, with no duplicate of the
    replay and no gap."""
    gateway = _gateway()
    session_id = _create(gateway, "gapless")
    _attach(gateway, session_id, 0, "attach-0")
    subscription = gateway.subscribe(session_id, 1)
    assert isinstance(subscription, Subscription)
    assert [event.sequence for event in subscription.replay] == [2]
    for revision in (1, 2):
        _attach(gateway, session_id, revision, f"attach-{revision}")
    seen: list[int] = []
    while True:
        item = subscription.next_item(0.2)
        if item is None:
            break
        assert isinstance(item, StreamEvent)
        seen.append(item.envelope.sequence)
    assert seen == [3, 4]
    subscription.close()


def test_fan_out_reaches_every_subscriber() -> None:
    """The fan-out: two channels on one session each receive the
    same live events (§13's ordered delivery to N consumers)."""
    gateway = _gateway()
    session_id = _create(gateway, "fanout")
    first = gateway.subscribe(session_id, 0)
    second = gateway.subscribe(session_id, 0)
    assert isinstance(first, Subscription) and isinstance(second, Subscription)
    _attach(gateway, session_id, 0, "attach-0")
    for subscription in (first, second):
        item = subscription.next_item(0.5)
        assert isinstance(item, StreamEvent)
        assert item.envelope.sequence == 2
        assert subscription.state() == "OPEN"
        subscription.close()


def test_overflow_drains_then_closes_observably() -> None:
    """§13's bounded buffer: a consumer that falls further behind
    than the ceiling gets its queued events drained IN ORDER, then
    the observable overflow terminal — never a silent drop, and the
    retained stream (the canonical record) is untouched."""
    gateway = _gateway(
        GatewayConfig(retention_events=8, stream_buffer_events=2)
    )
    session_id = _create(gateway, "overflow")
    subscription = gateway.subscribe(session_id, 0)
    assert isinstance(subscription, Subscription)
    # the create event (sequence 1) is replay, not queued; three
    # more events against a ceiling of 2: two queue, one overflows.
    for revision in range(3):
        _attach(gateway, session_id, revision, f"attach-{revision}")
    drained: list[int] = []
    first = subscription.next_item(0.2)
    assert isinstance(first, StreamEvent)
    drained.append(first.envelope.sequence)
    second = subscription.next_item(0.2)
    assert isinstance(second, StreamEvent)
    drained.append(second.envelope.sequence)
    assert drained == [2, 3]
    terminal = subscription.next_item(0.2)
    assert isinstance(terminal, StreamOverflow)
    assert terminal.last_sequence == 4
    assert subscription.state() == "OVERFLOW"
    # the terminal is idempotent; the retained stream is untouched
    assert subscription.next_item(0.2) == terminal
    assert subscription.known_sequence == 4
    events = _events_answer(gateway, session_id, 0)["events"]
    assert [event["sequence"] for event in events] == [1, 2, 3, 4]
    subscription.close()


def test_overflow_reconnect_always_replays() -> None:
    """The construction invariant's payoff: a consumer that
    overflowed reconnects from ITS last received sequence into a
    REPLAY window (the buffer is at most the retention, so the
    cursor is always inside the window) — never a second resync."""
    for buffer_events, retention in ((2, 8), (4, 4)):
        gateway = _gateway(
            GatewayConfig(
                retention_events=retention, stream_buffer_events=buffer_events
            )
        )
        session_id = _create(gateway, f"reconnect-{buffer_events}")
        subscription = gateway.subscribe(session_id, 0)
        assert isinstance(subscription, Subscription)
        last_received = subscription.replay[-1].sequence
        for revision in range(buffer_events + 2):
            _attach(gateway, session_id, revision, f"attach-{revision}")
        while True:
            item = subscription.next_item(0.1)
            if isinstance(item, StreamEvent):
                last_received = item.envelope.sequence
            else:
                assert isinstance(item, StreamOverflow)
                break
        subscription.close()
        reconnected = gateway.subscribe(session_id, last_received)
        assert isinstance(reconnected, Subscription)
        assert reconnected.mode == "REPLAY"
        assert reconnected.replay
        reconnected.close()


def test_close_is_idempotent_and_unregisters() -> None:
    """The consumer-side close: idempotent, unregisters from the
    fan-out (close_subscriptions finds nothing after), the terminal
    is the unframed CLIENT close."""
    gateway = _gateway()
    session_id = _create(gateway, "close")
    subscription = gateway.subscribe(session_id, 0)
    assert isinstance(subscription, Subscription)
    subscription.close()
    subscription.close()  # idempotent
    assert subscription.state() == "CLOSED"
    assert gateway.close_subscriptions() == 0
    terminal = subscription.next_item(0.1)
    assert terminal == StreamClosed("CLIENT")


def test_close_subscriptions_wakes_and_is_idempotent() -> None:
    """The bounded-shutdown surface: a blocked `next_item` returns
    the SHUTDOWN terminal PROMPTLY (the condition wake, not the
    heartbeat bound), the count is honest, the second call is a
    no-op, and the session's own state is untouched (a server stop
    cancels nothing)."""
    gateway = _gateway()
    session_id = _create(gateway, "shutdown")
    subscription = gateway.subscribe(session_id, 0)
    assert isinstance(subscription, Subscription)
    observed: list[Any] = []

    def _blocked_pull() -> None:
        observed.append(subscription.next_item(30.0))

    puller = threading.Thread(target=_blocked_pull, daemon=True)
    puller.start()
    time.sleep(0.05)
    closed = gateway.close_subscriptions()
    puller.join(timeout=2.0)
    assert closed == 1
    assert not puller.is_alive()
    assert observed == [StreamClosed("SHUTDOWN")]
    assert subscription.state() == "CLOSED"
    assert gateway.close_subscriptions() == 0
    # §13: the session stream itself is untouched by the stop
    events = _events_answer(gateway, session_id, 0)["events"]
    assert [event["sequence"] for event in events] == [1]


def test_disconnect_never_cancels_unrelated_execution() -> None:
    """§13's hard law, executable: a consumer channel ends mid-life
    and the session keeps dispatching, emitting, and replaying for
    the NEXT subscriber — the stream is a READ surface."""
    gateway = _gateway()
    session_id = _create(gateway, "disconnect")
    gone = gateway.subscribe(session_id, 0)
    assert isinstance(gone, Subscription)
    gone.close()
    for revision in range(2):
        _attach(gateway, session_id, revision, f"attach-{revision}")
    fresh = gateway.subscribe(session_id, 0)
    assert isinstance(fresh, Subscription)
    assert [event.sequence for event in fresh.replay] == [1, 2, 3]
    fresh.close()


# ------------------------------------------------------ the SSE wire


class _SseClient:
    """A raw http.client SSE reader: real socket, incremental frame
    reads — no mock between the test and the wire."""

    def __init__(
        self,
        transport: Any,
        session_id: str,
        since: int | None = None,
        last_event_id: str | None = None,
        query: str | None = None,
        method: str = "GET",
    ) -> None:
        self._transport = transport
        self._conn = http.client.HTTPConnection(
            "127.0.0.1", transport.port, timeout=5
        )
        path = query if query is not None else f"/events?session_id={session_id}"
        if since is not None:
            path += f"&since_sequence={since}"
        headers = {}
        if last_event_id is not None:
            headers["Last-Event-ID"] = last_event_id
        self._conn.request(method, path, headers=headers)
        self._response = self._conn.getresponse()

    @property
    def status(self) -> int:
        return self._response.status

    @property
    def content_type(self) -> str | None:
        return self._response.headers.get("Content-Type")

    def line(self, timeout: float = 2.0) -> str:
        """One raw line (the SSE wire is line-framed); a deadline
        fails loud — a hung stream is a bug, never a slow test."""
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise AssertionError("the stream never produced the next line")
            self._response.fp.raw._sock.settimeout(remaining)  # type: ignore[attr-defined]
            raw = self._response.readline()
            if raw:
                return raw.decode("utf-8").rstrip("\n")

    def frame(self, timeout: float = 2.0) -> dict[str, str]:
        """One parsed SSE message: the non-comment lines until the
        blank separator — {event, data, id?}."""
        fields: dict[str, str] = {}
        while True:
            text = self.line(timeout)
            if text == "":
                if fields:
                    return fields
                continue  # a heartbeat comment block's separator
            if text.startswith(":"):
                fields.setdefault("comment", text)
                continue
            key, _, value = text.partition(": ")
            fields[key] = value

    def frames(self, count: int, timeout: float = 3.0) -> list[dict[str, str]]:
        return [self.frame(timeout) for _ in range(count)]

    def expect_eof(self, timeout: float = 2.0) -> None:
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            assert remaining > 0, "the stream never closed"
            self._response.fp.raw._sock.settimeout(remaining)  # type: ignore[attr-defined]
            if not self._response.readline():
                return

    def close(self) -> None:
        self._conn.close()


def _transport(
    gateway: Gateway, heartbeat: float = 30.0
) -> Any:
    from workbench.api.transport import LoopbackHttpTransport

    transport = LoopbackHttpTransport(
        gateway, heartbeat_seconds=heartbeat, stream_write_seconds=5.0
    ).start()
    return transport


def test_stream_wire_open_replay_and_parity() -> None:
    """The wire form: 200 + text/event-stream + no-store; ONE
    stream.open frame (the mode document); the replay as id/event/
    data frames whose data bytes are EXACTLY what `session.events`
    replays (the D4 parity law's stream arm); the cursor beyond
    last_sequence answers an empty replay honestly."""
    gateway = _gateway()
    transport = _transport(gateway)
    try:
        session_id = _create(gateway, "wire")
        for revision in range(2):
            _attach(gateway, session_id, revision, f"attach-{revision}")
        client = _SseClient(transport, session_id, since=1)
        assert client.status == 200
        assert client.content_type == "text/event-stream; charset=utf-8"
        open_frame = client.frame()
        assert open_frame["event"] == "stream.open"
        document = json.loads(open_frame["data"])
        assert document["mode"] == "REPLAY"
        assert document["session_id"] == session_id
        assert document["last_sequence"] == 3
        expected = _events_answer(gateway, session_id, 1)["events"]
        frames = client.frames(len(expected))
        for frame, event in zip(frames, expected, strict=True):
            assert frame["event"] == event["event_type"]
            assert frame["id"] == str(event["sequence"])
            assert frame["data"] == canonical_json(event)
        client.close()
        # a cursor beyond the history: the honest empty replay
        beyond = _SseClient(transport, session_id, since=99)
        open_beyond = beyond.frame()
        assert json.loads(open_beyond["data"])["last_sequence"] == 3
        assert beyond.frames(0) == []
        beyond.close()
    finally:
        transport.stop()


def test_stream_live_push_over_the_wire() -> None:
    """The live arm: an event dispatched AFTER the stream opened
    arrives as a pushed frame (no polling, no replay) — the same
    canonical bytes, the id advancing."""
    gateway = _gateway()
    transport = _transport(gateway)
    try:
        session_id = _create(gateway, "live")
        client = _SseClient(transport, session_id, since=0)
        client.frames(2)  # stream.open + the create event
        _attach(gateway, session_id, 0, "attach-0")
        frame = client.frame()
        assert frame["event"] == "SESSION_ATTACHED"
        assert frame["id"] == "2"
        expected = _events_answer(gateway, session_id, 1)["events"][0]
        assert frame["data"] == canonical_json(expected)
        client.close()
    finally:
        transport.stop()


def test_stream_last_event_id_header() -> None:
    """The SSE standard's own reconnect cursor: Last-Event-ID is the
    fallback when the explicit parameter is absent; the explicit
    parameter wins when both ride the request."""
    gateway = _gateway()
    transport = _transport(gateway)
    try:
        session_id = _create(gateway, "last-event-id")
        for revision in range(2):
            _attach(gateway, session_id, revision, f"attach-{revision}")
        header_only = _SseClient(transport, session_id, last_event_id="2")
        header_only.frame()  # stream.open
        replay = header_only.frames(1)
        assert replay[0]["id"] == "3"
        header_only.close()
        explicit = _SseClient(transport, session_id, since=0, last_event_id="2")
        explicit.frame()
        explicit_replay = explicit.frames(3)
        assert [frame["id"] for frame in explicit_replay] == ["1", "2", "3"]
        explicit.close()
        malformed = _SseClient(transport, session_id, last_event_id="abc")
        assert malformed.status == 400
        body = malformed._response.read()  # noqa: SLF001 — the guard's body
        assert json.loads(body)["error"] == "BAD_STREAM_PARAMS"
        malformed.close()
    finally:
        transport.stop()


def test_stream_guards_are_transport_level() -> None:
    """The pre-stream guards answer 4xx JSON and never reach the
    core; the routing matrix holds: GET /op -> 405, POST /events ->
    405, unknown GET -> 404."""
    gateway = _gateway()
    transport = _transport(gateway)
    try:
        cases = [
            ("", 400),  # no session_id at all
            ("session_id=", 400),  # empty value
            ("session_id=x&since_sequence=abc", 400),
            ("session_id=x&since_sequence=-1", 400),
            ("session_id=x&session_id=y", 400),  # duplicated: never first-wins
            ("session_id=no-such&since_sequence=0", 200),  # the semantic lane
        ]
        for query, expected_status in cases:
            client = _SseClient(transport, "", query=f"/events?{query}")
            assert client.status == expected_status, query
            client.close()
        # POST /events is the wrong method for the stream route
        post = _SseClient(transport, "", query="/events", method="POST")
        assert post.status == 405
        post.close()
        # GET /op stays 405; an unknown GET path is 404 (not 405)
        get_op = _SseClient(transport, "", query="/op")
        assert get_op.status == 405
        get_op.close()
        get_unknown = _SseClient(transport, "", query="/nope")
        assert get_unknown.status == 404
        get_unknown.close()
        # the guards never opened a channel
        assert gateway.close_subscriptions() == 0
    finally:
        transport.stop()


def test_stream_semantic_rejection_rides_one_frame() -> None:
    """§8's split on the stream surface: an unknown session is a
    DELIVERED semantic answer — HTTP 200, ONE stream.rejected frame
    with the closed vocabulary's verdict, then the connection
    closes. Never a fabricated 4xx for a core verdict."""
    gateway = _gateway()
    transport = _transport(gateway)
    try:
        client = _SseClient(transport, "no-such-session")
        assert client.status == 200
        assert client.content_type == "text/event-stream; charset=utf-8"
        frame = client.frame()
        assert frame["event"] == "stream.rejected"
        document = json.loads(frame["data"])
        assert document["rejection"] == "DOMAIN_REJECTED"
        assert "no such session" in document["reason"]
        client.expect_eof()
        client.close()
    finally:
        transport.stop()


def test_stream_auth_required_refuses_before_the_core() -> None:
    """The auth law: the stream carries no credential (auth material
    never rides URLs) — an auth-required gateway refuses the stream
    route loudly (403) and never opens a channel."""
    from workbench.api.gateway import GatewayCredential

    gateway = _gateway(
        GatewayConfig(
            auth_required=True,
            credentials=(GatewayCredential(token="s", principal="p"),),
        )
    )
    created = gateway.dispatch_document(
        {
            "operation": "session.create",
            "client_request_id": "authed",
            "auth_token": "s",
        }
    )
    assert created.status == "OK", created.to_mapping()
    session_id = str(created.result["session_id"])
    transport = _transport(gateway)
    try:
        client = _SseClient(transport, session_id)
        assert client.status == 403
        body = json.loads(client._response.read())  # noqa: SLF001
        assert body["error"] == "STREAM_AUTH_REQUIRED"
        client.close()
        assert gateway.close_subscriptions() == 0
    finally:
        transport.stop()


def test_stream_heartbeat_comment_cadence() -> None:
    """The keep-alive: an idle stream emits the SSE comment
    heartbeat on the wired cadence (EventSource ignores comments;
    the wire stays alive)."""
    gateway = _gateway()
    transport = _transport(gateway, heartbeat=0.05)
    try:
        session_id = _create(gateway, "heartbeat")
        client = _SseClient(transport, session_id, since=0)
        client.frames(2)  # stream.open + the create event
        started = time.monotonic()
        beat = client.frame(timeout=1.0)
        assert "comment" in beat
        assert beat["comment"].startswith(": keep-alive")
        assert time.monotonic() - started < 1.0
        client.close()
    finally:
        transport.stop()


def test_stream_stop_is_bounded_and_frames_the_close() -> None:
    """§25's bounded shutdown with LIVE streams: stop() wakes every
    writer through the channel condition (not the heartbeat bound),
    each stream receives its honest stream.close frame and EOF —
    promptly, and the serve-thread join stays bounded."""
    gateway = _gateway()
    transport = _transport(gateway, heartbeat=30.0)
    session_id = _create(gateway, "stop")
    clients = [_SseClient(transport, session_id, since=0) for _ in range(3)]
    for client in clients:
        client.frames(2)  # stream.open + the create event
    stopped = threading.Event()

    def _stop() -> None:
        transport.stop()
        stopped.set()

    stopper = threading.Thread(target=_stop, daemon=True)
    started = time.monotonic()
    stopper.start()
    for client in clients:
        frame = client.frame(timeout=2.0)
        assert frame["event"] == "stream.close"
        document = json.loads(frame["data"])
        assert document["reason"] == "SHUTDOWN"
        assert document["last_sequence"] == 1
        client.expect_eof(timeout=2.0)
        client.close()
    stopper.join(timeout=2.0)
    assert stopped.is_set()
    assert time.monotonic() - started < 2.0


def test_one_handler_thread_per_stream() -> None:
    """The boundedness posture: the writer is the request's own
    handler thread — a stream adds exactly one thread, frames add
    none. A vanished consumer's channel ends BOUNDED, by design: its
    queue fills to the ceiling and the OVERFLOW terminal closes the
    loop (the writes themselves may buffer silently into a
    gracefully-closed socket — no RST ever comes — so the bounded
    buffer, not the write failure, is the reliable end); the
    dispatch surface itself never notices (§13: a disconnect never
    implicitly cancels unrelated execution)."""
    gateway = _gateway(
        GatewayConfig(retention_events=8, stream_buffer_events=2)
    )
    transport = _transport(gateway)
    try:
        before = threading.active_count()
        session_id = _create(gateway, "threads")
        client = _SseClient(transport, session_id, since=0)
        client.frames(2)
        _attach(gateway, session_id, 0, "attach-0")
        client.frame()  # the live push
        during = threading.active_count()
        assert during == before + 1
        # the consumer vanishes; its channel fills (ceiling 2) and
        # the OVERFLOW terminal ends the writer — bounded, observed
        client.close()
        for revision in range(1, 6):
            _attach(gateway, session_id, revision, f"attach-{revision}")
        deadline = time.monotonic() + 2.0
        while threading.active_count() > before and time.monotonic() < deadline:
            time.sleep(0.02)
        assert threading.active_count() == before
        # the session's stream is intact — the disconnect cancelled
        # nothing (§13)
        events = _events_answer(gateway, session_id, 0)["events"]
        assert [event["sequence"] for event in events] == [1, 2, 3, 4, 5, 6, 7]
    finally:
        transport.stop()


def test_stream_route_constant() -> None:
    """The one stream route's name is law (the client adapter row
    binds on it)."""
    assert STREAM_ROUTE == "/events"
