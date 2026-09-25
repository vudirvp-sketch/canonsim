"""wb-7's claim packet — the live chat circuit's Python half (the
composition-root launcher `scripts/workbench_app.py`); wb-9's
launcher-side claims (the managed default, the settings family, the
exe resolution, the models-dir bootstrap).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE WIRING LAW: `build_app` composes the full live stack — the
   gateway, the wb-5 operations, the wb-6 backend port injected at the
   composition root (chat.send/model.load/model.unload registered),
   the wb-9 fetcher + settings family, and the loopback transport —
   WITHOUT starting anything (start/stop stay the caller's).
2. THE HONEST NO-BACKEND FORM: `--no-backend` composes without the
   port — the backend operations stay UNREGISTERED (the admission
   law's honest form; nothing fakes a chat). The settings family
   rides the same law (no port, no backend.settings).
3. THE MANAGED DEFAULT (wb-9): the plain form composes the
   _ManagedBackend wrapper (the owner's «llama.cpp тоже запускаться
   при загрузке модели» as THE default); `--attached` restores the
   observe-only client.
4. THE LOUD ARGUMENTS: a missing CUSTOM models dir is a loud AppError
   (never a silent empty serve); the DEFAULT models dir bootstraps
   itself (§16's recovery-by-creation); the https/malformed endpoint
   refuses.
5. THE SETTINGS FAMILY (wb-9): backend.settings answers the effective
   document + the command preview; backend.settings.update validates,
   persists atomically, and rejects the out-of-range/unknown loud;
   chat.send's absent temperature resolves from the store (§19.1's
   BASE layer — the caller's explicit value still wins).
6. THE EXE RESOLUTION (wb-9): the CLI override > the persisted
   preference > the runtime/llama.cpp scan > the PATH fallback.
7. THE LIVE ROUNDTRIP + THE END-TO-END CIRCUIT: the composed app
   serves POST /op over real loopback HTTP — session.create +
   app.status over the wire; chat.send against the LIVE stub
   llama-server observed to its truthful terminal COMPLETED.

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
    _ManagedBackend,
    build_app,
    parse_args,
    resolve_llama_exe,
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


def _settings_path(tmp_path: Path) -> Path:
    """The isolated USER_CONFIG path (the tests never touch the
    checkout's own runtime root)."""
    return tmp_path / "settings.json"


# ------------------------------------------------------- the wiring law


def test_build_app_wires_the_full_live_stack(tmp_path: Path) -> None:
    models = tmp_path / "models"
    _write_model(models)
    gateway, operations, transport, backend, args = build_app(
        ["--models-dir", str(models), "--settings-path", str(_settings_path(tmp_path))]
    )
    names = set(gateway.operation_names)
    # The wb-5 families + the wb-6 backend trio + the wb-9 fetch kind
    # + the settings family + the wb-4 session seed.
    assert {"run.start", "run.get", "run.cancel",
            "model.list", "model.inspect"} <= names
    assert {"chat.send", "model.load", "model.unload"} <= names
    assert {"model.states", "backend.settings",
            "backend.settings.update"} <= names
    assert {"session.create", "session.get", "app.status"} <= names
    assert "model.fetch" in operations.work_kinds
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
    gateway, operations, _transport, backend, _args = build_app(
        ["--models-dir", str(models), "--no-backend",
         "--settings-path", str(_settings_path(tmp_path))]
    )
    names = set(gateway.operation_names)
    assert "chat.send" not in names, (
        "the admission law: no backend port injected, no chat.send "
        "registered — never a fake"
    )
    assert "model.load" not in names and "model.unload" not in names
    assert "backend.settings" not in names and (
        "backend.settings.update" not in names
    ), "the settings family rides the same admission law (no port, no consumer)"
    assert {"run.start", "model.list", "app.status"} <= names
    assert "model.fetch" in operations.work_kinds  # the fetcher is port-free
    assert backend is None


def test_missing_custom_models_dir_is_loud(tmp_path: Path) -> None:
    with pytest.raises(AppError, match="does not exist"):
        build_app(["--models-dir", str(tmp_path / "nowhere")])
    with pytest.raises(AppError, match="does not exist"):
        build_app(["--no-backend", "--models-dir", str(tmp_path / "nowhere")])


def test_the_default_models_dir_bootstraps_itself() -> None:
    """wb-9's frictionless open: the DEFAULT MODELS_ASSETS root is
    created when missing (§16's recovery-by-creation — the gitignored
    runtime root, never a loud dead end on a fresh clone)."""
    assert DEFAULT_MODELS_DIR.is_absolute()
    DEFAULT_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    gateway, _operations, _transport, _backend, _args = build_app(
        ["--settings-path", str(DEFAULT_MODELS_DIR.parent / "settings.json")]
    )
    assert DEFAULT_MODELS_DIR.is_dir()
    assert "model.list" in gateway.operation_names


def test_the_documented_defaults() -> None:
    args = parse_args([])
    assert args.host == DEFAULT_HOST == "127.0.0.1"
    assert args.port == DEFAULT_PORT == 8765
    assert args.backend_endpoint == DEFAULT_BACKEND_ENDPOINT
    assert Path(args.models_dir) == DEFAULT_MODELS_DIR
    assert not args.no_backend
    assert not args.attached  # MANAGED is the default ownership form
    assert args.llama_server_exe is None  # the settings/scan resolution
    assert args.llama_ctx is None and args.llama_ngl is None
    args = parse_args(["--no-backend", "--port", "9000", "--host", "::1"])
    assert args.no_backend and args.port == 9000 and args.host == "::1"
    attached = parse_args(["--attached"])
    assert attached.attached and not attached.no_backend


# ------------------------------------------- wb-9: the managed default


def test_the_managed_default_composes_the_wrapper(tmp_path: Path) -> None:
    models = tmp_path / "models"
    _write_model(models)
    _gateway, _operations, _transport, backend, _args = build_app(
        ["--models-dir", str(models), "--port", "0",
         "--settings-path", str(_settings_path(tmp_path))]
    )
    assert isinstance(backend, _ManagedBackend)
    assert backend.is_live() is False
    assert backend.managed_line().startswith("managed llama-server ABSENT")


def test_attached_restores_the_observe_only_client(tmp_path: Path) -> None:
    models = tmp_path / "models"
    _write_model(models)
    _gateway, _operations, _transport, backend, _args = build_app(
        ["--models-dir", str(models), "--attached", "--port", "0",
         "--settings-path", str(_settings_path(tmp_path))]
    )
    assert not isinstance(backend, _ManagedBackend)


def test_the_managed_endpoint_must_parse(tmp_path: Path) -> None:
    models = tmp_path / "models"
    _write_model(models)
    with pytest.raises(AppError, match="host:port"):
        build_app(
            ["--models-dir", str(models),
             "--backend-endpoint", "http://127.0.0.1",
             "--settings-path", str(_settings_path(tmp_path))]
        )
    with pytest.raises(AppError, match="https"):
        build_app(
            ["--models-dir", str(models),
             "--backend-endpoint", "https://127.0.0.1:8080",
             "--settings-path", str(_settings_path(tmp_path))]
        )


# ------------------------------------------- wb-9: the exe resolution


def test_the_exe_resolution_order(tmp_path: Path) -> None:
    home = tmp_path / "llama.cpp"
    release = home / "llama-b1234-bin-win-cuda-x64"
    release.mkdir(parents=True)
    exe = release / "llama-server.exe"
    exe.write_bytes(b"stub")
    # 1. the explicit preference wins verbatim
    assert resolve_llama_exe("D:/llama.cpp/llama-server.exe", home) == (
        "D:/llama.cpp/llama-server.exe"
    )
    # 2. the empty preference falls to the scan (deterministic: the
    # root level first, then the sorted subfolders)
    assert resolve_llama_exe("", home) == str(exe)
    # 3. no home, no PATH hit → the bare name (the spawn's own loud error)
    empty_home = tmp_path / "empty"
    empty_home.mkdir()
    assert resolve_llama_exe("", empty_home) == "llama-server"


def test_the_launch_params_merge_cli_over_settings(tmp_path: Path) -> None:
    """The EFFECTIVE provider: the CLI overrides win per-field over
    the store's CURRENT values (read at spawn time — a UI update
    applies at the next spawn)."""
    sys.path.insert(0, str(REPO))
    from workbench_app import _make_launch_params

    from workbench.application.inference import InferenceStore
    from workbench.application.settings import SettingsStore

    settings_path = _settings_path(tmp_path)
    store = SettingsStore(settings_path)
    inference = InferenceStore(tmp_path / "inference.json")
    inference.update(
        {"context": 4096, "gpu_layers": 24, "temperature": 0.25}
    )
    cli = parse_args(["--llama-ctx", "2048"])
    provider = _make_launch_params(store, inference, cli)
    params = provider()
    assert params["context"] == 2048  # the CLI override
    assert params["gpu_layers"] == 24  # the profile's value
    assert params["temperature"] == 0.25
    assert params["flash_attention"] == "on"
    assert params["exe"] == "llama-server"  # the bare PATH default
    # inf-1: the compiled semantic surface rides the provider (the
    # chain, the seed, the fit, the KV pair)
    assert params["samplers"] == [
        "penalties", "top_k", "top_p", "min_p", "temperature"
    ]
    assert params["seed"] == -1
    assert params["fit"] == "on"
    assert params["cache_type_k"] == "f16"
    # the profile's update applies at the NEXT provider read (the
    # Inference surface's own next-spawn law)
    inference.update({"gpu_layers": 40})
    assert provider()["gpu_layers"] == 40


# ------------------------------------------- wb-9: the one-command launcher


def test_the_launcher_bootstrap_creates_the_runtime_layout(
    tmp_path: Path,
) -> None:
    from workbench_launch import bootstrap_runtime_layout

    created = bootstrap_runtime_layout(tmp_path)
    assert created == [
        tmp_path / "workbench" / "runtime" / "models",
        tmp_path / "workbench" / "runtime" / "llama.cpp",
    ]
    # idempotent: an already-present folder is not re-created/reported
    assert bootstrap_runtime_layout(tmp_path) == []


def test_the_launcher_resolves_the_redot_exe(monkeypatch: pytest.MonkeyPatch) -> None:
    """wb-10's resolution chain (the tuple contract: the executable +
    the origin note). The auto-scan is pinned to an empty root list —
    the environment's own Desktop must never leak into the claim."""
    import os

    import workbench_launch
    from workbench_launch import resolve_redot_exe

    monkeypatch.setattr(workbench_launch, "auto_discover_redot", lambda: None)
    try:
        os.environ.pop("REDOT_EXE", None)
        assert resolve_redot_exe(None) == (None, "no resolution")
        assert resolve_redot_exe("  ") == (None, "no resolution")
        # the CLI form is strict: verbatim even when the path is
        # absent — the spawn's own loud error, never second-guessed
        resolved, origin = resolve_redot_exe("C:/Redot/Redot.exe")
        assert resolved == "C:/Redot/Redot.exe"
        assert origin == "the --redot-exe argument"
        os.environ["REDOT_EXE"] = "C:/env/Redot.exe"
        resolved, origin = resolve_redot_exe(None)
        assert resolved == "C:/env/Redot.exe"
        assert origin == "the REDOT_EXE environment variable"
        resolved, origin = resolve_redot_exe("C:/cli/Redot.exe")
        assert resolved == "C:/cli/Redot.exe"
        assert origin == "the --redot-exe argument"
        # a stale non-strict value (the persisted pick) falls through
        os.environ.pop("REDOT_EXE", None)
        monkeypatch.setattr(
            workbench_launch, "auto_discover_redot", lambda: "D:/found/redot.exe"
        )
        resolved, origin = resolve_redot_exe(None, persisted="gone/redot.exe")
        assert resolved == "D:/found/redot.exe"
        assert "auto-scan" in origin
    finally:
        os.environ.pop("REDOT_EXE", None)


def test_the_launcher_passes_the_gateway_args_through() -> None:
    from workbench_launch import parse_args as parse_launch_args

    args = parse_launch_args(["--port", "9000"])
    assert args.gateway_args == ["--port", "9000"]
    assert args.no_redot is False
    quiet = parse_launch_args(["--no-redot"])
    assert quiet.no_redot is True and quiet.gateway_args == []
    # the "--" separator is OURS: stripped before the child's own
    # parser sees it (the latent wb-9 bug — a bare "--" was the
    # gateway's own loud argparse refusal, wb-10's fix)
    passthrough = parse_launch_args(["--", "--port", "9001"])
    assert passthrough.gateway_args == ["--port", "9001"]


# ------------------------------------------- wb-9: the settings family


def test_backend_settings_read_and_update_over_http(tmp_path: Path) -> None:
    """THE wb-9 settings claim after inf-1's split: the READ answers
    the DEPLOYMENT document + the compiled command preview (the
    semantic surface's own preview); the UPDATE validates, persists,
    and serves the new deployment state — all over the served
    loopback HTTP (the exact circuit the Redot Settings surface
    drives). The inference family rides the same circuit: the READ
    answers the resolved controls + the chain, the UPDATE walks the
    resolver's effective state."""
    models = tmp_path / "models"
    _write_model(models)
    settings_path = _settings_path(tmp_path)
    inference_path = tmp_path / "inference.json"
    gateway, _operations, transport, _backend, _args = build_app(
        ["--models-dir", str(models), "--port", "0",
         "--settings-path", str(settings_path),
         "--inference-path", str(inference_path)]
    )
    transport.start()
    try:
        session = _over_http(
            transport.url,
            {"operation": "session.create", "arguments": {},
             "client_request_id": "wb9-settings"},
        )["result"]["session_id"]
        read = _over_http(
            transport.url,
            {"operation": "backend.settings", "arguments": {}},
        )
        assert read["status"] == "OK", read
        result = read["result"]
        assert result["settings"]["llama_server_exe"] == ""
        assert result["managed_live"] is False
        assert result["applies"] == "next-spawn"
        assert "<model.gguf>" in result["command_preview"]
        assert "--temp" in result["command_preview"]
        # inf-1: the inference READ over the same circuit — the
        # resolved controls document + the compiled chain
        inference_read = _over_http(
            transport.url,
            {"operation": "inference.read", "arguments": {}},
        )
        assert inference_read["status"] == "OK", inference_read
        controls = {
            c["id"]: c for c in inference_read["result"]["controls"]
        }
        assert controls["sampling.temperature"]["state"] == "EFFECTIVE"
        assert controls["sampling.temperature"]["value"] == 0.8
        assert controls["sampling.seed"]["state"] == "AUTO"
        assert "--samplers" in inference_read["result"]["compiled_preview"]
        # the inference UPDATE: the closed partial over the profile
        inference_updated = _over_http(
            transport.url,
            {
                "operation": "inference.update",
                "arguments": {"temperature": 0.3, "context": 4096},
                "session_id": session,
                "client_request_id": "inf1-update-1",
            },
        )
        assert inference_updated["status"] == "OK", inference_updated
        controls = {
            c["id"]: c for c in inference_updated["result"]["controls"]
        }
        assert controls["model.context"]["value"] == 4096
        assert controls["sampling.temperature"]["value"] == 0.3
        assert "-c 4096" in inference_updated["result"]["compiled_preview"]
        # the DEPLOYMENT update still walks its own store
        updated = _over_http(
            transport.url,
            {
                "operation": "backend.settings.update",
                "arguments": {"no_webui": False},
                "session_id": session,
                "client_request_id": "wb9-update-1",
            },
        )
        assert updated["status"] == "OK", updated
        assert updated["result"]["settings"]["no_webui"] is False
        # the atomic persistence: both files carry their schema + values
        document = json.loads(settings_path.read_text(encoding="utf-8"))
        assert document["schema"] == "canonsim.workbench.settings/2"
        assert document["settings"]["no_webui"] is False
        inference_document = json.loads(inference_path.read_text(encoding="utf-8"))
        assert inference_document["schema"] == (
            "canonsim.workbench.inference/1"
        )
        assert inference_document["profile"]["temperature"] == 0.3
    finally:
        transport.stop()


def test_backend_settings_update_rejects_loud(tmp_path: Path) -> None:
    models = tmp_path / "models"
    _write_model(models)
    gateway, _operations, transport, _backend, _args = build_app(
        ["--models-dir", str(models), "--port", "0",
         "--settings-path", str(_settings_path(tmp_path))]
    )
    transport.start()
    try:
        session = _over_http(
            transport.url,
            {"operation": "session.create", "arguments": {},
             "client_request_id": "wb9-reject"},
        )["result"]["session_id"]
        for bad in (
            {"context": 0},
            {"temperature": 5.0},
            {"flash_attention": "maybe"},
            {"nope": 1},
        ):
            reply = _over_http(
                transport.url,
                {
                    "operation": "backend.settings.update",
                    "arguments": bad,
                    "session_id": session,
                    "client_request_id": "wb9-reject-%s" % sorted(bad)[0],
                },
            )
            assert reply["status"] != "OK", bad
            assert reply.get("rejection") == "DOMAIN_REJECTED"
    finally:
        transport.stop()


def test_chat_temperature_resolves_from_the_settings(tmp_path: Path) -> None:
    """§19.1's BASE layer: chat.send with NO explicit temperature sends
    the store's value; the caller's explicit value still wins."""
    models = tmp_path / "models"
    _write_model(models)
    settings_path = _settings_path(tmp_path)
    inference_path = tmp_path / "inference.json"
    from workbench.application.inference import InferenceStore

    InferenceStore(inference_path).update({"temperature": 0.25})
    stub = _StubLlamaServer(models / "stub.gguf", replies=[("t1", "stop"), ("t2", "stop")])
    stub.start()
    try:
        _gateway, _operations, transport, _backend, _args = build_app(
            ["--models-dir", str(models),
             "--backend-endpoint", stub.url,
             "--port", "0", "--settings-path", str(settings_path),
             "--inference-path", str(inference_path)]
        )
        transport.start()
        try:
            session = _over_http(
                transport.url,
                {"operation": "session.create", "arguments": {},
                 "client_request_id": "wb9-temp"},
            )["result"]["session_id"]
            dispatched = _over_http(
                transport.url,
                {
                    "operation": "chat.send",
                    "arguments": {"messages": _MESSAGES},
                    "session_id": session,
                    "client_request_id": "wb9-temp-send",
                },
            )
            execution = dispatched["result"]["execution_id"]
            terminal = _await_terminal(transport.url, session, execution)
            assert terminal["state"] == "COMPLETED", terminal
            assert stub.requests[-1]["temperature"] == 0.25
            # the explicit value wins (the call-local override layer)
            dispatched = _over_http(
                transport.url,
                {
                    "operation": "chat.send",
                    "arguments": {"messages": _MESSAGES, "temperature": 1.5},
                    "session_id": session,
                    "client_request_id": "wb9-temp-send-2",
                },
            )
            execution = dispatched["result"]["execution_id"]
            _await_terminal(transport.url, session, execution)
            assert stub.requests[-1]["temperature"] == 1.5
        finally:
            transport.stop()
    finally:
        stub.stop()


# ---------------------------------------------------- the live roundtrip


def test_the_served_app_answers_over_loopback_http(tmp_path: Path) -> None:
    models = tmp_path / "models"
    _write_model(models)
    gateway, _operations, transport, _backend, _args = build_app(
        ["--models-dir", str(models), "--no-backend", "--port", "0",
         "--settings-path", str(_settings_path(tmp_path))]
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
    POST /op, the §19.1 REQUESTED→…→OBSERVED walk). The MANAGED
    default (wb-9) delegates to the live stub — the ATTACHED behaviour
    on a healthy server."""
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
                "--settings-path", str(_settings_path(tmp_path)),
            ]
        )
        assert backend is not None
        assert backend.is_live() is False  # the managed wrapper, no spawn
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
            "--settings-path", str(_settings_path(tmp_path)),
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
