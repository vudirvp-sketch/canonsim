"""wb-7's claim packet — the live chat circuit's Python half (the
composition-root launcher `scripts/workbench_app.py`).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE WIRING LAW: `build_app` composes the full live stack — the
   gateway, the wb-5 operations, the wb-6 backend port injected at the
   composition root (chat.send/model.load/model.unload registered),
   and the loopback transport — WITHOUT starting anything (start/stop
   stay the caller's).
2. THE HONEST NO-BACKEND FORM: `--no-backend` composes without the
   port — the three backend operations stay UNREGISTERED (the
   admission law's honest form; nothing fakes a chat).
3. THE LOUD ARGUMENTS: a missing models dir is a loud AppError (never
   a silent empty serve); the defaults are the documented constants.
4. THE LIVE ROUNDTRIP: the composed app serves POST /op over real
   loopback HTTP — session.create + app.status over the wire.
5. THE END-TO-END CIRCUIT: chat.send over HTTP against the LIVE stub
   llama-server (the app's backend port dialling it) observed to its
   truthful terminal COMPLETED with the stub's scripted reply — the
   exact circuit the Redot shell drives (identity-then-poll).

No Redot binary is needed here (the Redot half's committed-file
contract rides test_shell_contract.py; its gated proof rides
test_shell_proof.py).
"""

from __future__ import annotations

import json
import sys
import threading
import urllib.request
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tests"))
sys.path.insert(0, str(REPO / "scripts"))

from test_engine import _StubLlamaServer  # noqa: E402 — the shared stub
from workbench_app import (  # noqa: E402 — the launcher under test
    DEFAULT_BACKEND_ENDPOINT,
    DEFAULT_HOST,
    DEFAULT_MODELS_DIR,
    DEFAULT_PORT,
    AppError,
    build_app,
    parse_args,
)

_MESSAGES = [{"role": "user", "content": "hello from the live circuit"}]


def _write_model(models_dir: Path, name: str = "stub.gguf") -> None:
    models_dir.mkdir(parents=True, exist_ok=True)
    (models_dir / name).write_bytes(b"the stub model bytes")


def _over_http(url: str, document: dict[str, object]) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        data=json.dumps(document).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as handle:
        return dict(json.loads(handle.read().decode("utf-8")))


def _await_terminal(
    url: str, session: str, execution_id: str, tries: int = 200
) -> dict[str, object]:
    """The honest caller's poll (§8 identity-then-poll — the Redot
    shell's own form; the live-events row delivers streaming later)."""
    for _ in range(tries):
        document = _over_http(
            url,
            {
                "operation": "run.get",
                "arguments": {"execution_id": execution_id},
                "session_id": session,
            },
        )
        result = document.get("result")
        assert isinstance(result, dict)
        if result.get("terminal"):
            return dict(result)
        threading.Event().wait(0.02)
    raise AssertionError("the execution never reached terminal")


# ------------------------------------------------------- the wiring law


def test_build_app_wires_the_full_live_stack(tmp_path: Path) -> None:
    models = tmp_path / "models"
    _write_model(models)
    gateway, operations, transport, backend, args = build_app(
        ["--models-dir", str(models)]
    )
    names = set(gateway.operation_names)
    # The wb-5 families + the wb-6 backend trio + the wb-4 session seed.
    assert {"run.start", "run.get", "run.cancel",
            "model.list", "model.inspect"} <= names
    assert {"chat.send", "model.load", "model.unload"} <= names
    assert {"session.create", "session.get", "app.status"} <= names
    assert backend is not None
    assert args.backend_endpoint == DEFAULT_BACKEND_ENDPOINT
    assert transport is not None
    assert operations is not None


def test_the_backend_port_is_injected_never_imported() -> None:
    """INV-4's two-surface form holds at the launcher: the operations
    package never imports cli.engine (the architecture test owns the
    ban; this pins the launcher's side of the seam — the port arrives
    as an injected object, the physical owner referenced only here)."""
    import workbench.application.operations.backend as backend_module

    assert not hasattr(backend_module, "LlamaServerClient")
    source = Path(backend_module.__file__).read_text(encoding="utf-8")
    assert "cli.engine" not in source


def test_no_backend_honest_form(tmp_path: Path) -> None:
    models = tmp_path / "models"
    _write_model(models)
    gateway, _operations, transport, backend, _args = build_app(
        ["--models-dir", str(models), "--no-backend"]
    )
    names = set(gateway.operation_names)
    assert "chat.send" not in names, (
        "the admission law: no backend port injected, no chat.send "
        "registered — never a fake"
    )
    assert "model.load" not in names and "model.unload" not in names
    assert {"run.start", "model.list", "app.status"} <= names
    assert backend is None
    assert transport is not None


def test_missing_models_dir_is_loud(tmp_path: Path) -> None:
    with pytest.raises(AppError, match="does not exist"):
        build_app(["--models-dir", str(tmp_path / "nowhere")])
    with pytest.raises(AppError, match="does not exist"):
        build_app(["--no-backend", "--models-dir", str(tmp_path / "nowhere")])


def test_the_documented_defaults() -> None:
    args = parse_args([])
    assert args.host == DEFAULT_HOST == "127.0.0.1"
    assert args.port == DEFAULT_PORT == 8765
    assert args.backend_endpoint == DEFAULT_BACKEND_ENDPOINT
    assert Path(args.models_dir) == DEFAULT_MODELS_DIR
    assert not args.no_backend
    args = parse_args(["--no-backend", "--port", "9000", "--host", "::1"])
    assert args.no_backend and args.port == 9000 and args.host == "::1"


# ---------------------------------------------------- the live roundtrip


def test_the_served_app_answers_over_loopback_http(tmp_path: Path) -> None:
    models = tmp_path / "models"
    _write_model(models)
    gateway, _operations, transport, _backend, _args = build_app(
        ["--models-dir", str(models), "--no-backend", "--port", "0"]
    )
    transport.start()
    try:
        assert transport.url.startswith("http://127.0.0.1:")
        created = _over_http(
            transport.url,
            {
                "operation": "session.create",
                "arguments": {},
                "client_request_id": "wb7-roundtrip",
            },
        )
        assert created["status"] == "OK", created
        status = _over_http(
            transport.url, {"operation": "app.status", "arguments": {}}
        )
        assert status["status"] == "OK", status
        assert status["result"]["operations"] is not None
    finally:
        transport.stop()


def test_chat_circuit_end_to_end_over_http(tmp_path: Path) -> None:
    """THE wb-7 claim: chat.send over the served app against the LIVE
    stub llama-server, observed to its truthful terminal COMPLETED —
    the exact circuit the Redot shell drives (identity-then-poll over
    POST /op, the §19.1 REQUESTED→…→OBSERVED walk)."""
    models = tmp_path / "models"
    _write_model(models)
    stub = _StubLlamaServer(
        models / "stub.gguf", replies=[("the live reply", "stop")]
    )
    stub.start()
    try:
        gateway, _operations, transport, backend, _args = build_app(
            [
                "--models-dir", str(models),
                "--backend-endpoint", stub.url,
                "--port", "0",
            ]
        )
        assert backend is not None
        transport.start()
        try:
            created = _over_http(
                transport.url,
                {
                    "operation": "session.create",
                    "arguments": {},
                    "client_request_id": "wb7-chat",
                },
            )
            session = created["result"]["session_id"]
            dispatched = _over_http(
                transport.url,
                {
                    "operation": "chat.send",
                    "arguments": {"messages": _MESSAGES},
                    "session_id": session,
                    "client_request_id": "wb7-chat-send-1",
                },
            )
            assert dispatched["status"] == "OK", dispatched
            execution = dispatched["result"]["execution_id"]
            assert dispatched["result"]["work"] == "chat.completion"
            terminal = _await_terminal(transport.url, session, execution)
            assert terminal["state"] == "COMPLETED", terminal
            assert terminal["result"]["content"] == "the live reply"
            assert terminal["result"]["finish_reason"] == "stop"
            backend_note = terminal["result"]["backend"]
            assert backend_note["model"].endswith("stub.gguf")
            assert backend_note["build"] == "b11064-a894dae93"
        finally:
            transport.stop()
    finally:
        stub.stop()


def test_unreachable_backend_closes_the_run_failed(tmp_path: Path) -> None:
    """The honest down-backend form: the app still serves; the chat
    run closes FAILED with the observed cause (never a hang, never a
    fake) — the launcher's own documented contract."""
    models = tmp_path / "models"
    _write_model(models)
    # A loopback port with nothing listening: bind then close to pick
    # a guaranteed-free port.
    import socket

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        dead_port = probe.getsockname()[1]
    gateway, _operations, transport, backend, _args = build_app(
        [
            "--models-dir", str(models),
            "--backend-endpoint", f"http://127.0.0.1:{dead_port}",
            "--port", "0",
        ]
    )
    assert backend is not None
    transport.start()
    try:
        assert backend.health() is False  # the evidence-not-gate probe
        created = _over_http(
            transport.url,
            {
                "operation": "session.create",
                "arguments": {},
                "client_request_id": "wb7-dead",
            },
        )
        session = created["result"]["session_id"]
        dispatched = _over_http(
            transport.url,
            {
                "operation": "chat.send",
                "arguments": {"messages": _MESSAGES},
                "session_id": session,
                "client_request_id": "wb7-dead-send-1",
            },
        )
        execution = dispatched["result"]["execution_id"]
        terminal = _await_terminal(transport.url, session, execution)
        assert terminal["state"] == "FAILED", terminal
        assert terminal["failure_type"] is not None
    finally:
        transport.stop()
