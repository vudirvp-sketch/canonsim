"""The managed-backend contract tests' stand-in server (wb-8).

A standalone HTTP server that PARSES the same flag surface the
platform emits (the inf-2 semantic command: -m/--host/--port/-a/
-ngl/-c/-fa/--jinja/--no-webui + the full semantic flag set as
extras) and serves the llama-server surface the engine adapter
dials: /health, /props, /v1/chat/completions, /models/load,
/models/unload. It exists so the spawn tests prove the REAL process
mechanics (spawn → probe → ready → graceful stop) without a
llama.cpp binary — the wire shapes stay the stub contract's own
(tests/test_engine.py's _StubLlamaServer), and this file is TEST
tooling: never imported by the application, never scanned by the
architecture ban (tests/ is not a package dir).

inf-2 note: the parse is a TOKEN SCAN, never argparse — the full
semantic command carries short flags argparse would cluster-mangle
(`-mg 0` parsed as `-m g`, eating the model path); the real
llama.cpp arg parser does exact matching, the stub mirrors THAT
law, and the receipt records the tokens the spawn actually carried.

Run shape (the tests spawn it through the command lead
`[sys.executable, __file__]`):

    python tests/_managed_fake_server.py -m <model> --host 127.0.0.1 \
        --port <port> -a <alias> -ngl 999 -c 8192 -fa on --jinja --no-webui
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

RECEIPT_FILE = "managed_fake_server_receipt.json"


def _value_of(tokens: list[str], flag: str, default: str) -> str:
    """The token following an EXACT flag match (the stub's own exact
    matching — no abbreviations, no clusters)."""
    if flag in tokens:
        index = tokens.index(flag)
        if index + 1 < len(tokens):
            return tokens[index + 1]
    return default


def main(argv: list[str] | None = None) -> int:
    tokens = list(sys.argv[1:] if argv is None else argv)
    received = {
        "model": _value_of(tokens, "-m", ""),
        "host": _value_of(tokens, "--host", "127.0.0.1"),
        "port": int(_value_of(tokens, "--port", "0")),
        "alias": _value_of(tokens, "-a", ""),
        "ngl": _value_of(tokens, "-ngl", "999"),
        "ctx": _value_of(tokens, "-c", "8192"),
        "fa": _value_of(tokens, "-fa", "on"),
        "jinja": "--jinja" in tokens,
        "no_webui": "--no-webui" in tokens,
        # inf-2 — the semantic receipt's own pins (the spawn tests
        # assert the compiled values reached the process boundary)
        "samplers": _value_of(tokens, "--samplers", ""),
        "temp": _value_of(tokens, "--temp", ""),
        "seed": _value_of(tokens, "-s", ""),
    }
    # The flag receipt rides stdout line 1 (the test reads it from the
    # spawn's captured pipe... the process stays alive, so the receipt
    # rides /props instead — printed here only for a debug eyeball).
    print(json.dumps(received), flush=True)

    class Handler(BaseHTTPRequestHandler):
        def _json(self, document: dict[str, object]) -> None:
            body = json.dumps(document).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802 — http.server's name
            if self.path == "/health":
                self._json({"status": "ok"})
            elif self.path == "/props":
                self._json({
                    "role": "server",
                    "model_path": received["model"],
                    "build_info": "fake-managed-b1",
                    "alias": received["alias"],
                })
            else:
                self.send_error(404)

        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", 0))
            payload = self.rfile.read(length) if length else b"{}"
            if self.path in ("/models/load", "/models/unload"):
                self._json({"success": True, "path": self.path})
            elif self.path == "/v1/chat/completions":
                json.loads(payload)  # shape-checked, content scripted
                self._json({
                    "choices": [{
                        "message": {"role": "assistant", "content": "managed"},
                        "finish_reason": "stop",
                    }],
                })
            else:
                self.send_error(404)

        def log_message(self, format: str, *args: object) -> None:
            pass  # silence the stand-in's stderr

    server = ThreadingHTTPServer(
        (received["host"], received["port"]), Handler
    )
    server.serve_forever(poll_interval=0.1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
