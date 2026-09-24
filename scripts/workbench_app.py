"""The Workbench composition root + loopback serve (wb-7, the live
chat circuit's Python half — the app spec §22's CLI/batch delivery
surface over the application operations; wb-8, the MANAGED backend
half — the app spec §11.1's spawn/observe/graceful-stop machinery,
the owner's «llama.cpp тоже запускаться при загрузке модели» call).

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
     -> llama-server (ATTACHED: the operator's process, D-192's D1
                        MANAGED: spawned HERE on the first model.load,
                        §11.1's prepare→validate→ready form)
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
- ATTACHED (the default): the operator owns llama-server's lifecycle;
  a down backend is the honest FAILED close, never an implicit spawn.
- MANAGED (`--managed`): the launcher owns the process (§11.1's
  MANAGED half, platform/llama_process.py's mechanics) — the FIRST
  model.load spawns llama-server with the honest default flag set
  (the station's own: -ngl 999, -c 8192, -fa on, --jinja, --no-webui,
  loopback bind, -a <logical_name>) and observes readiness through
  the engine adapter's own health() probe; Ctrl+C stops the gateway
  AND the server (bounded graceful: TERM → deadline → kill, the
  observed exit code reported). The flags ride --llama-server-exe /
  --llama-ctx / --llama-ngl / --llama-args (the operator's override
  surface); a busy/owned port is the loud observed failure, never a
  silent fallback (no port shopping — §16's explicit-path law).

Usage (the owner's live forms):

    python scripts/workbench_app.py \
        --models-dir /path/to/gguf-dir \
        --backend-endpoint http://127.0.0.1:8080

    python scripts/workbench_app.py --managed \
        --llama-server-exe D:/llama.cpp/llama-server.exe \
        --models-dir /path/to/gguf-dir

    # defaults: 127.0.0.1:8765 + http://127.0.0.1:8080 +
    # <repo>/workbench/runtime/models (gitignored runtime data)
"""

from __future__ import annotations

import argparse
import signal
import sys
import time
from pathlib import Path
from typing import Any

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
from workbench.platform.llama_process import (  # noqa: E402
    DEFAULT_CONTEXT,
    DEFAULT_GPU_LAYERS,
    LlamaProcessError,
    LlamaServerProcess,
    build_server_command,
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

#: The MANAGED readiness budget (§11.1 PROBING → READY): a Q4_K_M
#: body's spawn+load on the station lands well inside this; the
#: timeout is the observed failure's own vocabulary, never a hang.
MANAGED_READY_TIMEOUT_S = 300.0

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
        f"(default {DEFAULT_BACKEND_ENDPOINT}); in --managed form the "
        "spawned server is expected on THIS endpoint's port",
    )
    parser.add_argument(
        "--no-backend",
        action="store_true",
        help="compose WITHOUT the backend port: chat.send/model.load/"
        "model.unload stay unregistered (the honest admission law)",
    )
    parser.add_argument(
        "--managed",
        action="store_true",
        help="§11.1's MANAGED form: llama-server is spawned on the first "
        "model.load and stopped at shutdown (the lifecycle policy owned "
        "here, the OS mechanics in workbench/platform/llama_process.py)",
    )
    parser.add_argument(
        "--llama-server-exe",
        default="llama-server",
        help="the llama-server executable path for --managed (the owner's "
        "station: D:/llama.cpp/llama-server.exe; default: the PATH lookup)",
    )
    parser.add_argument(
        "--llama-ctx",
        type=int,
        default=DEFAULT_CONTEXT,
        help=f"the spawned server's context window (default {DEFAULT_CONTEXT})",
    )
    parser.add_argument(
        "--llama-ngl",
        type=int,
        default=DEFAULT_GPU_LAYERS,
        help="the spawned server's GPU layer count (default "
        f"{DEFAULT_GPU_LAYERS} — all layers; 0 = CPU)",
    )
    parser.add_argument(
        "--llama-args",
        default="",
        help="extra llama-server flags verbatim (space-separated, the "
        "operator's override surface — quoted as one argument)",
    )
    return parser.parse_args(argv)


class _ManagedBackend:
    """The MANAGED BackendPort face (§11.1 over wb-6's port shape):
    the SAME four members the operations already call —
    props/chat/load_model/unload_model — with the process policy
    folded in at the physical boundary:

    - a HEALTHY server is used as-is (delegation — the ATTACHED
      behaviour unchanged);
    - model.load on a DOWN server spawns llama-server with `-m` for
      the very model the caller named (prepare → validate → ready),
      so the load's observed outcome IS the spawn's honest truth;
    - unload of the SPAWNED model stops the process (the server
      exists for that one model — §11.1's bounded graceful stop);
      any other model ref delegates to POST /models/unload;
    - Ctrl+C (the launcher's stop path) always stops the process we
      spawned — ATTACHED servers are never terminated by us (§25).

    The HTTP itself stays the engine adapter's (cli/engine.py — the
    ONE outbound surface); this wrapper only decides WHEN a process
    must exist and owns its lifetime. It never touches the gateway,
    the operations, or the wire shapes."""

    def __init__(
        self,
        *,
        client: LlamaServerClient,
        exe: str,
        host: str,
        port: int,
        context: int,
        gpu_layers: int,
        extra_args: list[str],
        ready_timeout_s: float = MANAGED_READY_TIMEOUT_S,
    ) -> None:
        self._client = client
        self._exe = exe
        self._host = host
        self._port = port
        self._context = context
        self._gpu_layers = gpu_layers
        self._extra_args = extra_args
        self._ready_timeout_s = ready_timeout_s
        self._process: LlamaServerProcess | None = None
        self._spawned_alias: str | None = None
        self.last_spawn_command: list[str] = []

    # -- the port face (wb-6's shape, duck-typed by the operations) --

    def props(self) -> dict[str, Any]:
        return self._client.props()

    def chat(
        self,
        messages: Any,
        *,
        grammar: str | None = None,
        temperature: float = 0.8,
        max_tokens: int = 512,
    ) -> tuple[str, str]:
        return self._client.chat(
            messages,
            grammar=grammar,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def load_model(
        self, model_path: str, alias: str | None = None
    ) -> dict[str, Any]:
        if self._client.health():
            return self._client.load_model(model_path, alias=alias)
        return self._spawn_for(model_path, alias)

    def unload_model(self, model_ref: str) -> dict[str, Any]:
        if (
            self._process is not None
            and self._spawned_alias is not None
            and model_ref == self._spawned_alias
        ):
            code = self._process.stop(grace_s=10.0)
            self._process = None
            self._spawned_alias = None
            return {
                "success": True,
                "managed": "stopped",
                "exit_code": code,
            }
        return self._client.unload_model(model_ref)

    # -- the lifecycle policy (§11.1: the composition root's own) ----

    def _spawn_for(
        self, model_path: str, alias: str | None
    ) -> dict[str, Any]:
        """prepare (the command with the honest defaults) → validate
        (the spawn itself, loud) → ready (the adapter's own health
        probe, the observed truth — never a fabricated readiness)."""
        command = build_server_command(
            self._exe,
            model_path,
            host=self._host,
            port=self._port,
            alias=alias,
            context=self._context,
            gpu_layers=self._gpu_layers,
            extra_args=self._extra_args,
        )
        self.last_spawn_command = list(command)
        process = LlamaServerProcess(command)
        try:
            process.start()  # loud on a missing/failed executable
        except LlamaProcessError as exc:
            # The D1 mapping at the managed boundary: a spawn that cannot
            # happen IS an unavailable backend (the model rests at
            # SELECTED — a deliberate re-load stays legal, §12.1's sibling).
            raise _managed_error("unavailable", str(exc)) from exc
        self._process = process
        self._spawned_alias = alias
        ready = process.wait_ready(
            self._client.health, timeout_s=self._ready_timeout_s
        )
        if not ready:
            tail = process.stderr_tail()
            code = process.exit_code()
            process.stop(grace_s=2.0)
            self._process = None
            self._spawned_alias = None
            if code is not None:
                raise _managed_error(
                    "unavailable",
                    f"the managed llama-server exited with code {code} "
                    f"before readiness — stderr tail: {tail or '(empty)'}",
                )
            raise _managed_error(
                "unavailable",
                f"the managed llama-server did not become ready within "
                f"{self._ready_timeout_s:.0f}s — stderr tail: "
                f"{tail or '(empty)'} (is the port free? does the model "
                "fit the GPU budget?)",
            )
        return {
            "success": True,
            "managed": "started",
            "command": " ".join(command),
        }

    def stop(self) -> int | None:
        """The shutdown path's own half (§25): stop ONLY the process
        we spawned, the observed exit code returned."""
        if self._process is None:
            return None
        code = self._process.stop(grace_s=10.0)
        self._process = None
        self._spawned_alias = None
        return code

    def managed_line(self) -> str:
        """The startup evidence line's managed half (§18: the
        effective backend state, never hidden)."""
        if self._process is not None:
            return (
                f"managed llama-server LIVE on port {self._port} — "
                f"alias {self._spawned_alias!r}"
            )
        return (
            f"managed llama-server ABSENT — it spawns on the first "
            f"model.load (exe {self._exe!r}, -ngl {self._gpu_layers}, "
            f"-c {self._context})"
        )


class _ManagedError(RuntimeError):
    """The managed spawn's honest failure (the D1 vocabulary's
    'unavailable' cause — the outcome never fabricated)."""

    def __init__(self, cause: str, detail: str) -> None:
        super().__init__(f"[{cause}] {detail}")
        self.cause = cause


def _managed_error(cause: str, detail: str) -> _ManagedError:
    return _ManagedError(cause, detail)


def _backend_port_from(args: argparse.Namespace) -> object | None:
    """The composition's backend resolution: None (--no-backend),
    the plain ATTACHED client (the default), or the MANAGED wrapper
    (§11.1's policy half — the client inside stays the ONE outbound
    surface; the wrapper adds process decisions only)."""
    if args.no_backend:
        return None
    client = LlamaServerClient(
        EngineConfig(endpoint=args.backend_endpoint)
    )
    if not args.managed:
        return client
    host, port = _host_port(args.backend_endpoint)
    extra = [part for part in args.llama_args.split() if part]
    return _ManagedBackend(
        client=client,
        exe=args.llama_server_exe,
        host=host,
        port=port,
        context=args.llama_ctx,
        gpu_layers=args.llama_ngl,
        extra_args=extra,
    )


def _host_port(endpoint: str) -> tuple[str, int]:
    """The endpoint's host:port (the managed spawn must land on the
    endpoint the port already dials — one name, one place; a malformed
    endpoint is the launcher's loud argument error)."""
    raw = endpoint.rstrip("/")
    if raw.startswith("http://"):
        raw = raw[len("http://"):]
    elif raw.startswith("https://"):
        raise AppError(
            f"--managed: the endpoint {endpoint!r} is https — the managed "
            "spawn speaks plain loopback http (app §4's exposure law)"
        )
    host, separator, port_text = raw.rpartition(":")
    if not separator or not host or not port_text.isdigit():
        raise AppError(
            f"--managed: the endpoint {endpoint!r} does not parse as "
            "host:port — the spawned server must land on the port the "
            "BackendPort dials"
        )
    return host, int(port_text)


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
    try:
        backend = _backend_port_from(args)
    except LlamaProcessError as exc:
        raise AppError(f"the managed backend refused: {exc}") from exc
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
        if args.managed:
            print(_managed_line(backend))
    print("Ctrl+C to stop.")
    while not stopped[0]:
        time.sleep(_STOP_POLL_S)
    transport.stop()
    if args.managed and backend is not None:
        code = backend.stop()  # type: ignore[attr-defined]
        print(f"managed llama-server stopped (exit code {code})")
    return 0


def _managed_line(backend: object) -> str:
    return backend.managed_line()  # type: ignore[attr-defined]


if __name__ == "__main__":
    raise SystemExit(main())
