"""The loopback HTTP binding (wb-4, the app spec §§4.1/8/22 — the
family's fourth row).

This is INV-4's second sanctioned network module (D-201) — the ONE
inbound Workbench surface, and the ONLY socket in `workbench/`. The
semantic API lives in the socket-free dispatch core
(`workbench/api/gateway.py`); this module is pure delivery (§8:
"HTTP/SSE/WebSocket are delivery mechanisms"):

```text
client JSON body -> RequestEnvelope -> Gateway.dispatch_document
                 -> ResponseDocument -> canonical JSON body
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
- The body ceiling is explicit (§26's boundedness at the edge):
  `MAX_BODY_BYTES`; a larger body is refused before reading.
- The response body is the canonical byte form (sorted keys, fixed
  separators — the D4 discipline; the parity proof byte-compares
  direct vs HTTP).
- `observed_at` and every identity field come from the core's wired
  clock — the transport itself adds NO time, NO identity, NO state.

Shutdown is explicit and bounded (§25's minimal form):
`stop()` -> `shutdown()` (the serve loop exits) -> `server_close()`
(the socket releases) -> a bounded join. Idempotent; `start()`
likewise. The handler silences `BaseHTTPRequestHandler`'s stderr
logging (§21: observation is the diagnostics surface's own row,
never stray prints).
"""

from __future__ import annotations

import http.server
import json
import threading
from collections.abc import Mapping

from workbench.api.gateway import Gateway

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


class TransportError(ValueError):
    """A transport construction violation — LOUD, before any bind
    (the exposure law's binding half, G3)."""


class _GatewayHTTPServer(http.server.ThreadingHTTPServer):
    """The threaded server carrying the gateway (daemon threads: a
    transport never blocks process exit; §25 owns the graceful
    policy)."""

    daemon_threads = True

    def __init__(
        self,
        address: tuple[str, int],
        handler: type[http.server.BaseHTTPRequestHandler],
        gateway: Gateway,
    ) -> None:
        super().__init__(address, handler)
        self.gateway = gateway


class _Handler(http.server.BaseHTTPRequestHandler):
    """The delivery translator: bytes <-> the core's documents. Adds
    no state, no time, no identity (the parity law's transport half)."""

    server: _GatewayHTTPServer

    def do_POST(self) -> None:  # noqa: N802 — the http.server API
        if self.path != ROUTE:
            self._send_json(404, {"error": "NOT_FOUND", "path": self.path})
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
        self._send_json(405, {"error": "METHOD_NOT_ALLOWED"})

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
    the dispatch core.

    `port=0` binds an ephemeral port (the proof runner's form);
    `start()` is idempotent and returns self; `stop()` shuts the
    serve loop down, releases the socket, joins the thread (bounded),
    and is idempotent. No lifecycle beyond start/stop — backend/
    application lifecycles are §11/§32 step 2 rows, never the
    transport's.
    """

    def __init__(
        self,
        gateway: Gateway,
        host: str = "127.0.0.1",
        port: int = 0,
    ) -> None:
        if host not in LOOPBACK_HOSTS:
            raise TransportError(
                f"host {host!r}: the shipped binding is LOOPBACK ONLY "
                "(G3 — a non-loopback bind is a future row's own "
                "contract; the exposure law holds at construction)"
            )
        self._gateway = gateway
        self._host = host
        self._requested_port = port
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

    def start(self) -> LoopbackHttpTransport:
        """Bind + serve (idempotent). The bind failure (port in use)
        propagates loudly — never a hidden retry loop."""
        if self._server is not None:
            return self
        self._server = _GatewayHTTPServer(
            (self._host, self._requested_port), _Handler, self._gateway
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
        (idempotent; §25's minimal shutdown form)."""
        server = self._server
        thread = self._thread
        if server is None:
            return
        self._server = None
        self._thread = None
        server.shutdown()
        server.server_close()
        if thread is not None:
            thread.join(timeout=5.0)
