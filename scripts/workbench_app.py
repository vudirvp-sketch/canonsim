"""The Workbench composition root + loopback serve (wb-7, the live
chat circuit's Python half — the app spec §22's CLI/batch delivery
surface over the application operations).

What this script is: the ONE launcher that assembles the live
Workbench — the inbound gateway (wb-4), the application operations
(wb-5), and the llama.cpp backend port (wb-6, `cli/engine.py`'s
LlamaServerClient injected, never imported by the operations — INV-4's
two-surface form holds; this file is the composition root, the only
place the two sanctioned surfaces meet) — and serves the loopback HTTP
binding the frontend talks to:

```text
Redot shell (POST /op)  ->  LoopbackHttpTransport  ->  Gateway
     -> chat.send / run.get / run.cancel / model.*  ->  BackendPort
     -> llama-server (the operator's long-lived process, D-192's D1)
```

The frontend NEVER talks to llama.cpp directly (frontend §47's G8 —
the frontend cannot bypass the application boundary); llama.cpp is
reached only through the engine adapter, and the shell reaches it
only through the gateway.

Honest forms:

- `--no-backend` composes WITHOUT the port: chat.send/model.load/
  model.unload are simply not registered (the admission law's honest
  form) and the frontend shows "not connected" — never a fake.
- A configured-but-down backend endpoint still starts: health is
  probed once at startup as EVIDENCE (never a gate), and chat runs
  close FAILED with the observed cause — the honest surface.
- The backend process is NOT managed here (§11.1's MANAGED half is
  its own row): the operator owns llama-server's lifecycle.

Usage (the owner's live form):

    python scripts/workbench_app.py \
        --models-dir /path/to/gguf-dir \
        --backend-endpoint http://127.0.0.1:8080

    # defaults: 127.0.0.1:8765 + http://127.0.0.1:8080 +
    # <repo>/workbench/runtime/models (gitignored runtime data)
"""

from __future__ import annotations

import argparse
import signal
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

if str(REPO) not in sys.path:  # the scripts/ pattern (visual_proof.py)
    sys.path.insert(0, str(REPO))

from cli.engine import EngineConfig, LlamaServerClient  # noqa: E402
from workbench.api.gateway import Gateway  # noqa: E402
from workbench.api.transport import LoopbackHttpTransport  # noqa: E402
from workbench.application.clock import AppClock  # noqa: E402
from workbench.application.operations.composition import (  # noqa: E402
    CompositionError,
    compose_workbench_operations,
)

#: The loopback serve defaults (the frontend's committed project
#: setting matches: workbench/presentation/redot/project.godot —
#: canonism_workbench/gateway/url).
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765

#: The operator's llama-server endpoint default (llama.cpp's own
#: default port; EngineConfig's DEFAULT_ENDPOINT sibling).
DEFAULT_BACKEND_ENDPOINT = "http://127.0.0.1:8080"

#: The default MODELS_ASSETS root (§16's path role, gitignored —
#: the operator drops GGUF files there; model discovery scans it).
DEFAULT_MODELS_DIR = REPO / "workbench" / "runtime" / "models"

_STOP_POLL_S = 0.2


class AppError(RuntimeError):
    """The launcher's loud failure (a bad argument or a malformed
    composition — never a silent empty serve)."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="the CanonSim Workbench composition root + loopback serve"
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"the loopback bind host (default {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"the loopback bind port (default {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--models-dir",
        default=str(DEFAULT_MODELS_DIR),
        help="the MODELS_ASSETS root — GGUF discovery (§16/§20); "
        "default <repo>/workbench/runtime/models",
    )
    parser.add_argument(
        "--backend-endpoint",
        default=DEFAULT_BACKEND_ENDPOINT,
        help="the llama-server endpoint the BackendPort dials "
        f"(default {DEFAULT_BACKEND_ENDPOINT})",
    )
    parser.add_argument(
        "--no-backend",
        action="store_true",
        help="compose WITHOUT the backend port: chat.send/model.load/"
        "model.unload stay unregistered (the honest admission law)",
    )
    return parser.parse_args(argv)


def build_app(
    argv: list[str] | None = None,
) -> tuple[Gateway, object, LoopbackHttpTransport, object | None, argparse.Namespace]:
    """Construct → validate → wire (§6.1's composition form): the
    gateway, the operations over it, the backend port when configured
    (the handle returned for the startup evidence line — the
    operations themselves never see the physical owner), and the
    loopback transport — NOTHING started (start/stop stay the
    caller's: the test surface composes without serving)."""
    args = parse_args(argv)
    models_dir = Path(args.models_dir).expanduser().resolve()
    if not models_dir.exists():
        raise AppError(
            f"models dir {str(models_dir)!r} does not exist — create it "
            "and drop the GGUF files there (§16's MODELS_ASSETS role), "
            "or pass --models-dir"
        )
    backend: object | None = None
    if not args.no_backend:
        backend = LlamaServerClient(
            EngineConfig(endpoint=args.backend_endpoint)
        )
    gateway = Gateway()
    try:
        operations = compose_workbench_operations(
            gateway, models_dir, AppClock(), backend=backend
        )
    except CompositionError as exc:
        raise AppError(f"the composition refused: {exc}") from exc
    transport = LoopbackHttpTransport(
        gateway, host=args.host, port=args.port
    )
    return gateway, operations, transport, backend, args


def _backend_line(backend: object, endpoint: str) -> str:
    """The startup evidence line (§18: never hide effective backend
    state): one health probe — evidence, never a gate."""
    reachable = backend.health()  # type: ignore[attr-defined]
    if reachable:
        return f"backend llama.cpp {endpoint} — REACHABLE"
    return (
        f"backend llama.cpp {endpoint} — NOT REACHABLE (the app still "
        "serves; chat runs will close FAILED with the observed cause)"
    )


def main(argv: list[str] | None = None) -> int:
    try:
        gateway, _operations, transport, backend, args = build_app(argv)
    except AppError as exc:
        print(f"workbench_app: {exc}", file=sys.stderr)
        return 2
    stopped = [False]

    def _stop(_signum: int, _frame: object) -> None:
        stopped[0] = True

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, _stop)
    transport.start()
    print(f"CanonSim Workbench — loopback gateway {transport.url}")
    print(f"operations: {', '.join(gateway.operation_names)}")
    if backend is None:
        print(
            "backend: NONE (--no-backend — chat.send/model.load/"
            "model.unload unregistered, the honest admission law)"
        )
    else:
        print(_backend_line(backend, args.backend_endpoint))
    print("Ctrl+C to stop.")
    while not stopped[0]:
        time.sleep(_STOP_POLL_S)
    transport.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
