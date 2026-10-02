"""The loopback HTTP binding (wb-4, the app spec §§4.1/8/22 — the
family's fourth row; iter-305 adds the §13 one-way stream arm).

This is INV-4's second sanctioned network module (D-201) — the ONE
inbound Workbench surface, and the ONLY socket in `workbench/`. The
semantic API lives in the socket-free dispatch core
(`workbench/api/gateway.py`); this module is pure delivery (§8:
"HTTP/SSE/WebSocket are delivery mechanisms"):

```text
client JSON body -> RequestEnvelope -> Gateway.dispatch_document
                 -> ResponseDocument -> canonical JSON body

client GET stream -> Gateway.subscribe -> Subscription (bounded
   live channel) -> SSE frames -> connection close
```

The exposure law's binding half (G3): LOOPBACK HOSTS ONLY —
`127.0.0.1`, `localhost`, `::1` — refused loudly otherwise (a
non-loopback bind is a future row's own contract with auth/transport
of its own; the config-side refusal already guards
`GatewayConfig(exposure=...)`). The wire contract:

- `POST /op` — the envelope document in, the response document out.
  ANY envelope the core processed answers HTTP 200 (semantic
  rejections included — the verdict rides the JSON, §8: delivery and
  semantics separated); transport-level failures (body not JSON,
  oversized, wrong path, wrong method) answer 4xx JSON errors — they
  never reach the core.
- `GET /events` — the §13 one-way stream: `session_id` +
  `since_sequence` (the SSE `Last-Event-ID` header is the standard's
  fallback cursor; the explicit parameter wins). The route mirrors
  the core's `subscribe`: the same dual answer `session.events`
  gives, then the live tail — pushed, never polled. The wire form is
  SSE (`text/event-stream`): one `stream.open` frame (the mode
  document — REPLAY or RESYNC), then one frame per ordered event
  (`id` = the sequence, `event` = the event type, `data` = the SAME
canonical JSON `session.events` replays — the byte parity is the
  contract's proof), `: keep-alive` comment heartbeats, and the
  honest terminals (`stream.overflow`, `stream.close`). A semantic
  rejection (an unknown session) answers HTTP 200 + ONE
  `stream.rejected` frame + close — the verdict rides the stream,
  never a fabricated 4xx. Pre-stream guards (malformed parameters,
  the auth-required refusal — auth material never rides URLs, so
  the authenticated exposures own their own stream contract) stay
  transport-level 4xx JSON.
- The body ceiling is explicit (§26's boundedness at the edge):
  `MAX_BODY_BYTES`; a larger body is refused before reading.
- The response body is the canonical byte form (sorted keys, fixed
  separators — the D4 discipline; the parity proof byte-compares
  direct vs HTTP).
- `observed_at` and every identity field come from the core's wired
  clock — the transport itself adds NO time, NO identity, NO state
  beyond the stream cadence constants (heartbeat, write timeout).

Boundedness of the stream arm (§26): the per-subscriber buffer
lives in the core (its own ceiling, observable overflow); the
writer here is the request's own handler thread (one thread per
  stream, no extra threads); every frame write is bounded by the
  socket write timeout; the heartbeat bounds the loop's wake. A
vanished consumer's channel ends BOUNDED, by design: its queue
fills to the ceiling and the OVERFLOW terminal closes the loop (a
graceful client close sends only FIN — the writes buffer into the
void and no RST ever comes, so the bounded buffer, not the write
failure, is the reliable end; an abrupt reset ends it at the first
failed write) — §13's law either way: a disconnect never
implicitly cancels unrelated execution.

Shutdown is explicit and bounded (§25's minimal form):
`stop()` -> the stopping signal + `close_subscriptions()` (every
live writer wakes on its channel condition, frames its honest
`stream.close`, exits) -> `shutdown()` (the serve loop exits) ->
`server_close()` (the socket releases) -> a bounded join. The
writer threads are daemon handlers (never individually joined — a
stream opened inside the stop race window ends within one
heartbeat). Idempotent; `start()` likewise. The handler silences
`BaseHTTPRequestHandler`'s stderr logging (§21: observation is the
diagnostics surface's own row, never stray prints).
"""

from __future__ import annotations

import http.server
import json
import re
import threading
import urllib.parse
from collections.abc import Mapping

from workbench.api.contract import EventEnvelope, canonical_json
from workbench.api.gateway import (
    STREAM_CLOSE_REASONS,
    Gateway,
    StreamClosed,
    StreamEvent,
    StreamOverflow,
    StreamRejection,
    Subscription,
)

#: The loopback host set (G3 — the shipped binding's whole surface).
LOOPBACK_HOSTS: frozenset[str] = frozenset({"127.0.0.1", "localhost", "::1"})

#: The request-body ceiling (§26: bounded with an explicit ceiling).
MAX_BODY_BYTES = 1 << 20

#: The absolute drain ceiling for refused bodies: a refused request's
#: bytes are drained (so the client reads the 4xx cleanly) only up to
#: this bound — beyond it the connection simply closes (bounded
#: everywhere, §26; no infinite read ever serves an unbounded body).
MAX_DRAIN_BYTES = 8 << 20

#: The one route: POST /op (§8's single dispatch entry).
ROUTE = "/op"

#: The one stream route: GET /events (§13's one-way event direction —
#: the SSE delivery over the SAME ordered stream `session.events`
#: replays by POST).
STREAM_ROUTE = "/events"

#: The keep-alive cadence (seconds) — the writer's wake bound and the
#: idle-connection proof of life (a comment frame; proxies and the
#: client see traffic, EventSource ignores comments).
DEFAULT_HEARTBEAT_SECONDS = 15.0

#: The per-frame write timeout (seconds): a blocked write to a dead
#: or stalled client ends the stream (bounded writes everywhere,
#: §26 — the OS buffers alone are never the bound).
DEFAULT_STREAM_WRITE_SECONDS = 30.0

#: The frame vocabulary — the closed set the stream may emit (the
#: event frames in between ride EVENT_TYPES from the contract).
STREAM_FRAME_TYPES = frozenset(
    {"stream.open", "stream.rejected", "stream.overflow", "stream.close"}
)

#: The non-negative integer form (both the query parameter and the
#: Last-Event-ID header).
_NON_NEG_INT = re.compile(r"^\d+$")


class TransportError(ValueError):
    """A transport construction violation — LOUD, before any bind
    (the exposure law's binding half, G3)."""


class _GatewayHTTPServer(http.server.ThreadingHTTPServer):
    """The threaded server carrying the gateway (daemon threads: a
    transport never blocks process exit; §25 owns the graceful
    policy) + the stream cadence constants and the stopping signal
    (the bounded-shutdown writer wake)."""

    daemon_threads = True

    def __init__(
        self,
        address: tuple[str, int],
        handler: type[http.server.BaseHTTPRequestHandler],
        gateway: Gateway,
        heartbeat_seconds: float,
        stream_write_seconds: float,
    ) -> None:
        super().__init__(address, handler)
        self.gateway = gateway
        self.heartbeat_seconds = heartbeat_seconds
        self.stream_write_seconds = stream_write_seconds
        self.stopping = threading.Event()


class _Handler(http.server.BaseHTTPRequestHandler):
    """The delivery translator: bytes <-> the core's documents. Adds
    no state, no time, no identity (the parity law's transport half).
    The one deliberate exception is the stream loop's OWN lifecycle
    state: it runs inside this request's handler thread (one thread
    per stream — never an extra pool) and adds nothing the request
    does not own."""

    server: _GatewayHTTPServer

    def do_POST(self) -> None:  # noqa: N802 — the http.server API
        path = _path_only(self.path)
        if path == STREAM_ROUTE:
            self._send_json(405, {"error": "METHOD_NOT_ALLOWED"})
            return
        if path != ROUTE:
            self._send_json(404, {"error": "NOT_FOUND", "path": path})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "BAD_CONTENT_LENGTH"})
            return
        if length < 0:
            self._send_json(400, {"error": "BAD_CONTENT_LENGTH"})
            return
        if length > MAX_BODY_BYTES:
            self._drain(length)
            self._send_json(400, {"error": "BODY_TOO_LARGE"})
            return
        body = self.rfile.read(length) if length else b""
        try:
            document = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            self._send_json(400, {"error": "BODY_NOT_JSON"})
            return
        response = self.server.gateway.dispatch_document(document)
        self._send_json(200, response.to_mapping())

    def _drain(self, length: int) -> None:
        """Drain a refused body up to the absolute bound (bounded
        everywhere — beyond MAX_DRAIN_BYTES the connection closes
        with the response, never an unbounded read)."""
        remaining = min(length, MAX_DRAIN_BYTES)
        while remaining > 0:
            chunk = self.rfile.read(min(remaining, 1 << 16))
            if not chunk:
                break
            remaining -= len(chunk)

    def do_GET(self) -> None:  # noqa: N802 — the http.server API
        path, _, query = self.path.partition("?")
        if path == STREAM_ROUTE:
            self._handle_stream(query)
            return
        if path == ROUTE:
            self._send_json(405, {"error": "METHOD_NOT_ALLOWED"})
            return
        self._send_json(404, {"error": "NOT_FOUND", "path": path})

    # ------------------------------------------------------------ stream

    def _handle_stream(self, query: str) -> None:
        """The §13 one-way stream over `Gateway.subscribe`: the
        parameters guard (transport-level 4xx — malformed wire input
        never reaches the core), the auth refusal (the stream carries
        no credential: auth material never rides URLs, so the
        authenticated exposure rows own their own stream contract),
        then the core's dual answer and the live frame loop. The
        handler thread IS the writer — one thread per stream, its
        end is the request's end."""
        gateway = self.server.gateway
        try:
            session_id = _single_query_value(query, "session_id")
        except _MalformedQuery:
            self._send_json(
                400,
                {
                    "error": "BAD_STREAM_PARAMS",
                    "reason": "session_id: exactly one value",
                },
            )
            return
        if session_id is None or session_id == "":
            self._send_json(
                400,
                {
                    "error": "BAD_STREAM_PARAMS",
                    "reason": "session_id: a non-empty query parameter",
                },
            )
            return
        try:
            raw_since = _single_query_value(query, "since_sequence")
        except _MalformedQuery:
            self._send_json(
                400,
                {
                    "error": "BAD_STREAM_PARAMS",
                    "reason": "since_sequence: exactly one value",
                },
            )
            return
        last_event_id = self.headers.get("Last-Event-ID", "").strip()
        if raw_since is not None:
            cursor = raw_since
        elif last_event_id:
            cursor = last_event_id
        else:
            cursor = "0"
        if not _NON_NEG_INT.match(cursor):
            self._send_json(
                400,
                {
                    "error": "BAD_STREAM_PARAMS",
                    "reason": (
                        "since_sequence: a non-negative integer "
                        f"(got {cursor!r})"
                    ),
                },
            )
            return
        if gateway.config.auth_required:
            self._send_json(403, {"error": "STREAM_AUTH_REQUIRED"})
            return
        answer = gateway.subscribe(session_id, int(cursor))
        if isinstance(answer, StreamRejection):
            # The delivery/semantics split (§8) holds on the stream
            # surface too: the core PROCESSED this request — the
            # verdict rides one frame, then the stream ends. Never a
            # fabricated 4xx for a semantic answer.
            self._open_stream()
            self._write_frame(
                "stream.rejected",
                {"reason": answer.reason, "rejection": answer.rejection},
            )
            return
        self._open_stream()
        self._write_frame("stream.open", _open_document(answer))
        for envelope in answer.replay:
            self._write_event(envelope)
        self.connection.settimeout(self.server.stream_write_seconds)
        try:
            while not self.server.stopping.is_set():
                item = answer.next_item(self.server.heartbeat_seconds)
                if item is None:
                    # The heartbeat: a comment frame (EventSource
                    # ignores comments; the wire stays alive).
                    self._write_raw(b": keep-alive\n\n")
                    continue
                if isinstance(item, StreamEvent):
                    self._write_event(item.envelope)
                    continue
                if isinstance(item, StreamOverflow):
                    self._write_frame(
                        "stream.overflow", {"last_sequence": item.last_sequence}
                    )
                    break
                assert isinstance(item, StreamClosed)
                if item.reason in STREAM_CLOSE_REASONS:
                    # The framed server close — e.g. the bounded
                    # shutdown. A CLIENT-side close (the consumer
                    # raced this writer) sends no frame: nobody is
                    # listening; the loop just ends.
                    self._write_frame(
                        "stream.close",
                        {
                            "last_sequence": answer.known_sequence,
                            "reason": item.reason,
                        },
                    )
                break
        except OSError:
            # The consumer is gone (an abrupt reset, a stalled peer,
            # an unreachable connection): the stream and its channel
            # end — nothing else is touched (§13: a disconnect never
            # implicitly cancels unrelated execution). Not an error
            # anywhere; the connection closes with the handler's
            # return. (A GRACEFUL client close sends only FIN — the
            # writes buffer and no error fires; that consumer's
            # channel ends at its own OVERFLOW terminal instead,
            # equally bounded.)
            pass
        finally:
            answer.close()

    def _open_stream(self) -> None:
        """The stream response head. No Content-Length: the body IS
        the stream and ends at the connection close (the handler's
        return) — the read-until-close form; every frame flushes
        immediately (unbuffered writes, one flush per frame)."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def _write_event(self, envelope: EventEnvelope) -> None:
        """One ordered session event as an SSE frame: `id` = the
        sequence (the browser's Last-Event-ID reconnect cursor),
        `event` = the event type, `data` = the SAME canonical JSON
        `session.events` replays (the byte-parity law's stream arm)."""
        body = canonical_json(envelope.to_mapping())
        self._write_raw(
            f"id: {envelope.sequence}\n"
            f"event: {envelope.event_type}\n"
            f"data: {body}\n\n".encode("utf-8")
        )

    def _write_frame(self, event: str, document: Mapping[str, object]) -> None:
        """One control frame (stream.open/rejected/overflow/close):
        no `id` line — a control frame never moves the consumer's
        reconnect cursor."""
        body = json.dumps(document, sort_keys=True, separators=(",", ":"))
        self._write_raw(f"event: {event}\ndata: {body}\n\n".encode("utf-8"))

    def _write_raw(self, payload: bytes) -> None:
        self.wfile.write(payload)
        self.wfile.flush()

    def _send_json(self, code: int, document: Mapping[str, object]) -> None:
        payload = json.dumps(
            document, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        # Silenced: stray stderr is not observation (§21 owns it).
        return


class LoopbackHttpTransport:
    """The one inbound delivery surface: a loopback HTTP binding over
    the dispatch core (`POST /op`) + the §13 one-way stream arm
    (`GET /events`).

    `port=0` binds an ephemeral port (the proof runner's form);
    `heartbeat_seconds` is the stream keep-alive cadence and
    `stream_write_seconds` the per-frame write bound (both
    construction-validated — a test wiring sub-second heartbeats is
    the same law as the proof runner's ephemeral port, never a
    tunable in flight); `start()` is idempotent and returns self;
    `stop()` wakes every live stream writer with the honest
    `stream.close` terminal (bounded), shuts the serve loop down,
    releases the socket, joins the thread (bounded), and is
    idempotent. No lifecycle beyond start/stop — backend/
    application lifecycles are §11/§32 step 2 rows, never the
    transport's.
    """

    def __init__(
        self,
        gateway: Gateway,
        host: str = "127.0.0.1",
        port: int = 0,
        heartbeat_seconds: float = DEFAULT_HEARTBEAT_SECONDS,
        stream_write_seconds: float = DEFAULT_STREAM_WRITE_SECONDS,
    ) -> None:
        if host not in LOOPBACK_HOSTS:
            raise TransportError(
                f"host {host!r}: the shipped binding is LOOPBACK ONLY "
                "(G3 — a non-loopback bind is a future row's own "
                "contract; the exposure law holds at construction)"
            )
        for name, value in (
            ("heartbeat_seconds", heartbeat_seconds),
            ("stream_write_seconds", stream_write_seconds),
        ):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or value <= 0
            ):
                raise TransportError(f"{name}: a positive number")
        self._gateway = gateway
        self._host = host
        self._requested_port = port
        self._heartbeat_seconds = float(heartbeat_seconds)
        self._stream_write_seconds = float(stream_write_seconds)
        self._server: _GatewayHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        """The bound port (the requested one before `start()`)."""
        if self._server is not None:
            return int(self._server.server_address[1])
        return self._requested_port

    @property
    def url(self) -> str:
        return f"http://{self._host}:{self.port}{ROUTE}"

    @property
    def stream_url(self) -> str:
        """The one-way stream route's URL (GET — the SSE delivery)."""
        return f"http://{self._host}:{self.port}{STREAM_ROUTE}"

    def start(self) -> LoopbackHttpTransport:
        """Bind + serve (idempotent). The bind failure (port in use)
        propagates loudly — never a hidden retry loop."""
        if self._server is not None:
            return self
        self._server = _GatewayHTTPServer(
            (self._host, self._requested_port),
            _Handler,
            self._gateway,
            self._heartbeat_seconds,
            self._stream_write_seconds,
        )
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            name="workbench-gateway-transport",
            daemon=True,
        )
        self._thread.start()
        return self

    def stop(self) -> None:
        """Serve-loop stop + socket release + bounded join
        (idempotent; §25's minimal shutdown form). The stream writers
        wake FIRST: `close_subscriptions` hands every live channel
        its SHUTDOWN terminal (the writers frame their honest close
        and exit within their own bounded write); the serve loop and
        the socket follow. The writers are daemon handler threads —
        never individually joined (a stream opened inside the stop
        race window ends within one heartbeat of its own loop)."""
        server = self._server
        thread = self._thread
        if server is None:
            return
        self._server = None
        self._thread = None
        server.stopping.set()
        self._gateway.close_subscriptions()
        server.shutdown()
        server.server_close()
        if thread is not None:
            thread.join(timeout=5.0)


def _path_only(path: str) -> str:
    """The route path (the query string stripped) — the routing
    matrix keys on the path alone."""
    return path.partition("?")[0]


class _MalformedQuery(ValueError):
    """A duplicated query parameter — refused loudly, never a
    first-wins guess."""


def _single_query_value(query: str, name: str) -> str | None:
    """One parameter's single value, or None when absent; a
    duplicated parameter is malformed wire input (never a silent
    first-wins)."""
    params = urllib.parse.parse_qs(query, keep_blank_values=True)
    values = params.get(name)
    if values is None:
        return None
    if len(values) != 1:
        raise _MalformedQuery(name)
    return values[0]


def _open_document(subscription: Subscription) -> dict[str, object]:
    """The `stream.open` frame's document: §13's dual answer — the
    mode, the session identity, the sequence bounds; the RESYNC arm
    merges the SAME snapshot document `session.events` answers."""
    document: dict[str, object] = {
        "last_sequence": subscription.last_sequence,
        "mode": subscription.mode,
        "session_id": subscription.session_id,
    }
    if subscription.resync_document is not None:
        document.update(subscription.resync_document)
    return document
