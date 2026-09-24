"""wb-8's claim packet — the MANAGED backend half (the app spec
§11.1's spawn/observe/graceful-stop machinery over the wb-6 port
shape: `workbench/platform/llama_process.py`'s mechanics +
`scripts/workbench_app.py`'s `_ManagedBackend` lifecycle policy).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE HONEST DEFAULT FLAGS: `build_server_command` emits the
   station's typed set (-m/--host/--port/-ngl/-c/-fa on/-a/--jinja/
   --no-webui + the operator's extras verbatim) — nothing hidden,
   nothing invented.
2. THE PROCESS MECHANICS: spawn → the injected readiness probe →
   graceful stop with the OBSERVED exit code; a dead process fails
   the wait immediately; a never-spawned object stops as None.
3. THE LIFECYCLE POLICY: `_ManagedBackend.load_model` on a DOWN
   backend SPAWNS the server for the very model the caller named and
   reports the honest `managed: started` reply; on a LIVE backend it
   DELEGATES (POST /models/load — the ATTACHED behaviour unchanged);
   the spawned model's unload STOPS the process; a foreign unload
   delegates; `stop()` is idempotent and returns the observed code.
4. THE SPAWN-FAILURE TRUTH: an executable that cannot spawn, or a
   server that dies before readiness, surfaces the honest
   'unavailable' cause (the §12.1 sibling — the model rests at
   SELECTED, a deliberate re-load stays legal) with the observed
   stderr tail/exit code in the message.
5. THE LAUNCHER WIRING: `--managed` composes the wrapper as the
   backend port (the same three+one operations registered); the
   argument surface is loud and documented.

The stand-in server (tests/_managed_fake_server.py) is spawned
through the command lead `[sys.executable, script]` — the REAL
process mechanics (no monkey-patching); the wire shapes stay the
stub contract's own. No Redot binary is needed here (the frontend
half's committed-file contract rides test_shell_contract.py).
"""

from __future__ import annotations

import json
import socket
import sys
import time
import urllib.request
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from test_engine import _StubLlamaServer  # noqa: E402 — the shared stub
from workbench_app import (  # noqa: E402 — the launcher under test
    AppError,
    _ManagedBackend,
    build_app,
    parse_args,
)

from workbench.platform.llama_process import (  # noqa: E402
    DEFAULT_CONTEXT,
    DEFAULT_GPU_LAYERS,
    DEFAULT_MIN_P,
    DEFAULT_REPEAT_PENALTY,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_K,
    DEFAULT_TOP_P,
    LlamaProcessError,
    LlamaServerProcess,
    build_server_command,
)

_FAKE_SERVER = Path(__file__).resolve().parent / "_managed_fake_server.py"
_LEAD = [sys.executable, str(_FAKE_SERVER)]


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def _health(url: str) -> bool:
    try:
        with urllib.request.urlopen(url + "/health", timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, OSError):
        return False


# --------------------------------------------- the honest default flags


def test_the_default_flag_set_is_typed_and_visible() -> None:
    command = build_server_command(
        "llama-server.exe", "D:/models/gemma.gguf",
        port=8080, alias="gemma.gguf",
    )
    assert command == [
        "llama-server.exe",
        "-m", "D:/models/gemma.gguf",
        "--host", "127.0.0.1",
        "--port", "8080",
        "-ngl", str(DEFAULT_GPU_LAYERS),
        "-c", str(DEFAULT_CONTEXT),
        "-fa", "on",
        "--temp", repr(DEFAULT_TEMPERATURE),
        "--top-k", str(DEFAULT_TOP_K),
        "--top-p", repr(DEFAULT_TOP_P),
        "--min-p", repr(DEFAULT_MIN_P),
        "--repeat-penalty", repr(DEFAULT_REPEAT_PENALTY),
        "-a", "gemma.gguf",
        "--jinja",
        "--no-webui",
    ]


def test_the_overrides_ride_honestly() -> None:
    command = build_server_command(
        ["python", "wrap.py"], "m.gguf",
        port=9000, alias=None, context=4096, gpu_layers=0,
        flash_attention="off", jinja=False, no_webui=False,
        temperature=0.2, top_k=0, top_p=0.5, min_p=0.1,
        repeat_penalty=1.05,
        extra_args=["--threads", "8", "--mlock"],
    )
    assert command[:3] == ["python", "wrap.py", "-m"]
    assert command[command.index("--port") + 1] == "9000"
    assert command[command.index("-ngl") + 1] == "0"
    assert command[command.index("-c") + 1] == "4096"
    assert command[command.index("-fa") + 1] == "off"
    assert command[command.index("--temp") + 1] == "0.2"
    assert command[command.index("--top-k") + 1] == "0"
    assert command[command.index("--top-p") + 1] == "0.5"
    assert command[command.index("--min-p") + 1] == "0.1"
    assert command[command.index("--repeat-penalty") + 1] == "1.05"
    assert "-a" not in command and "--jinja" not in command
    assert "--no-webui" not in command
    assert command[-3:] == ["--threads", "8", "--mlock"]


def test_the_argument_validation_is_loud() -> None:
    with pytest.raises(LlamaProcessError, match="lead is empty"):
        build_server_command(["", "x"], "m.gguf", port=1)
    with pytest.raises(LlamaProcessError, match="model path is empty"):
        build_server_command("exe", " ", port=1)
    with pytest.raises(LlamaProcessError, match="port"):
        build_server_command("exe", "m.gguf", port=0)
    with pytest.raises(LlamaProcessError, match="port"):
        build_server_command("exe", "m.gguf", port=65536)
    with pytest.raises(LlamaProcessError, match="context"):
        build_server_command("exe", "m.gguf", port=1, context=0)
    with pytest.raises(LlamaProcessError, match="gpu_layers"):
        build_server_command("exe", "m.gguf", port=1, gpu_layers=-1)
    with pytest.raises(LlamaProcessError, match="flash_attention"):
        build_server_command("exe", "m.gguf", port=1, flash_attention="maybe")
    with pytest.raises(LlamaProcessError, match="temperature"):
        build_server_command("exe", "m.gguf", port=1, temperature=2.5)
    with pytest.raises(LlamaProcessError, match="top_k"):
        build_server_command("exe", "m.gguf", port=1, top_k=-1)
    with pytest.raises(LlamaProcessError, match="top_p"):
        build_server_command("exe", "m.gguf", port=1, top_p=1.5)
    with pytest.raises(LlamaProcessError, match="min_p"):
        build_server_command("exe", "m.gguf", port=1, min_p=-0.1)
    with pytest.raises(LlamaProcessError, match="repeat_penalty"):
        build_server_command("exe", "m.gguf", port=1, repeat_penalty=5.0)


# --------------------------------------------- the process mechanics


def test_spawn_probe_ready_stop_the_observed_truth() -> None:
    port = _free_port()
    command = [sys.executable, str(_FAKE_SERVER), "-m", "m.gguf",
               "--host", "127.0.0.1", "--port", str(port)]
    process = LlamaServerProcess(command)
    assert process.command == command
    assert process.exit_code() is None  # never spawned — the honest None
    assert process.stop() is None
    process.start()
    try:
        assert process.running
        url = f"http://127.0.0.1:{port}"
        assert process.wait_ready(lambda: _health(url), timeout_s=15.0)
        with urllib.request.urlopen(url + "/props", timeout=5) as response:
            props = json.loads(response.read().decode("utf-8"))
        assert props["model_path"] == "m.gguf"
    finally:
        code = process.stop(grace_s=10.0)
    # The OBSERVED exit code — a POSIX graceful TERM reports the signal
    # (e.g. -15), a self-exit reports its own code: both are the truth.
    assert code is not None
    assert not process.running


def test_a_dead_process_fails_the_wait_immediately() -> None:
    process = LlamaServerProcess(
        [sys.executable, "-c", "import sys; sys.exit(3)"]
    )
    process.start()
    started = time.monotonic()
    ready = process.wait_ready(lambda: False, timeout_s=30.0)
    assert ready is False
    assert time.monotonic() - started < 10.0  # the dead-exit shortcut
    assert process.exit_code() == 3
    process.stop(grace_s=1.0)


def test_a_failed_spawn_is_loud() -> None:
    process = LlamaServerProcess(["definitely-not-an-executable-xyz"])
    with pytest.raises(LlamaProcessError, match="cannot spawn"):
        process.start()


def test_one_process_per_object() -> None:
    process = LlamaServerProcess(
        [sys.executable, "-c", "import time; time.sleep(30)"]
    )
    process.start()
    try:
        with pytest.raises(LlamaProcessError, match="already spawned"):
            process.start()
    finally:
        process.stop(grace_s=2.0)


# --------------------------------------------- the lifecycle policy


def _managed(
    port: int,
    *,
    client: object | None = None,
    ready_timeout_s: float = 20.0,
    **overrides: object,
) -> _ManagedBackend:
    from cli.engine import EngineConfig, LlamaServerClient

    resolved = (
        client
        if client is not None
        else LlamaServerClient(
            EngineConfig(endpoint=f"http://127.0.0.1:{port}")
        )
    )
    params: dict[str, object] = {
        "exe": _LEAD,
        "context": 4096,
        "gpu_layers": 0,
        "flash_attention": "on",
        "jinja": True,
        "no_webui": True,
        "temperature": 0.8,
        "top_k": 40,
        "top_p": 0.95,
        "min_p": 0.05,
        "repeat_penalty": 1.1,
        "extra_args": [],
    }

    def provider() -> dict[str, object]:
        merged = dict(params)
        merged.update(overrides)
        return merged

    return _ManagedBackend(
        client=resolved,
        launch_params=provider,
        host="127.0.0.1",
        port=port,
        ready_timeout_s=ready_timeout_s,
    )


def test_load_on_a_down_backend_spawns_and_reports_honestly() -> None:
    """THE wb-8 claim: model.load on a down backend is the spawn —
    llama-server comes up WITH the caller's model, readiness observed
    through the engine adapter's own probe, the reply naming the
    honest `managed: started` form."""
    port = _free_port()
    backend = _managed(port)
    reply = backend.load_model("stub-model.gguf", alias="stub-model.gguf")
    try:
        assert reply["success"] is True
        assert reply["managed"] == "started"
        assert "-m" in reply["command"] and "stub-model.gguf" in reply["command"]
        assert "--port" in reply["command"]
        assert backend.managed_line().startswith("managed llama-server LIVE")
        # The spawned server answers the adapter's own surface.
        assert backend.props()["model_path"] == "stub-model.gguf"
        assert backend.props()["build_info"] == "fake-managed-b1"
        content, finish = backend.chat([{"role": "user", "content": "hi"}])
        assert content == "managed" and finish == "stop"
    finally:
        code = backend.stop()
    assert code is not None  # the observed stop outcome (TERM's signal form)
    assert backend.managed_line().startswith("managed llama-server ABSENT")


def test_load_on_a_live_backend_delegates_the_attached_form() -> None:
    port = _free_port()
    stub = _StubLlamaServer(Path("stub.gguf"))
    stub.start()
    try:
        backend = _managed(port, client=_client_at(stub.url))
        reply = backend.load_model("other.gguf", alias="other.gguf")
        assert reply == {"success": True}
        assert stub.model_requests == [
            ("/models/load", {"model": "other.gguf", "alias": "other.gguf"})
        ]
        assert backend.managed_line().startswith("managed llama-server ABSENT")
    finally:
        stub.stop()


def _client_at(url: str) -> object:
    from cli.engine import EngineConfig, LlamaServerClient

    return LlamaServerClient(EngineConfig(endpoint=url))


def test_unload_of_the_spawned_model_stops_the_process() -> None:
    port = _free_port()
    backend = _managed(port)
    backend.load_model("stub-model.gguf", alias="stub-model.gguf")
    assert backend.managed_line().startswith("managed llama-server LIVE")
    reply = backend.unload_model("stub-model.gguf")
    assert reply["success"] is True
    assert reply["managed"] == "stopped"
    assert reply["exit_code"] is not None  # the observed stop outcome
    assert backend.managed_line().startswith("managed llama-server ABSENT")
    assert backend.stop() is None  # idempotent — nothing left to stop


def test_unload_of_a_foreign_ref_delegates() -> None:
    stub = _StubLlamaServer(Path("stub.gguf"))
    stub.start()
    try:
        backend = _managed(_free_port(), client=_client_at(stub.url))
        reply = backend.unload_model("foreign.gguf")
        assert reply == {"success": True}
        assert stub.model_requests == [
            ("/models/unload", {"model": "foreign.gguf"})
        ]
    finally:
        stub.stop()


def test_a_spawn_failure_is_the_honest_unavailable_cause() -> None:
    backend = _managed(_free_port(), exe=["definitely-not-an-exe-xyz"])
    with pytest.raises(Exception) as excinfo:
        backend.load_model("m.gguf", alias="m.gguf")
    assert getattr(excinfo.value, "cause", None) == "unavailable"
    assert backend.managed_line().startswith("managed llama-server ABSENT")


def test_a_never_ready_spawn_is_the_honest_unavailable_cause() -> None:
    """The stand-in server told to die immediately: the readiness wait
    observes the exit and surfaces the honest failure with the code —
    §11.1's PROBING → FAILED, never a fabricated READY."""
    backend = _managed(
        _free_port(),
        exe=[sys.executable, "-c", "import sys; print('boom', file=sys.stderr); sys.exit(7)"],
        ready_timeout_s=5.0,
    )
    with pytest.raises(Exception) as excinfo:
        backend.load_model("m.gguf", alias="m.gguf")
    assert getattr(excinfo.value, "cause", None) == "unavailable"
    assert "7" in str(excinfo.value) or "boom" in str(excinfo.value)


# --------------------------------------------- the launcher wiring


def test_the_managed_default_composes_the_wrapper(tmp_path: Path) -> None:
    models = tmp_path / "models"
    models.mkdir()
    (models / "m.gguf").write_bytes(b"stub")
    gateway, _operations, transport, backend, args = build_app(
        [
            "--models-dir", str(models),
            "--llama-server-exe", "llama-server.exe",
            "--llama-ctx", "4096",
            "--llama-ngl", "24",
            "--llama-args", "--threads 8 --mlock",
            "--port", "0",
            "--settings-path", str(tmp_path / "settings.json"),
        ]
    )
    assert isinstance(backend, _ManagedBackend)
    assert "model.states" in gateway.operation_names
    assert "model.load" in gateway.operation_names
    assert args.llama_ctx == 4096 and args.llama_ngl == 24
    assert args.llama_args == "--threads 8 --mlock"
    assert transport is not None
    assert backend.stop() is None  # nothing spawned — the honest no-op


def test_the_managed_endpoint_must_parse(tmp_path: Path) -> None:
    models = tmp_path / "models"
    models.mkdir()
    (models / "m.gguf").write_bytes(b"stub")
    with pytest.raises(AppError, match="host:port"):
        build_app(
            ["--models-dir", str(models),
             "--backend-endpoint", "http://127.0.0.1",
             "--settings-path", str(tmp_path / "settings.json")]
        )
    with pytest.raises(AppError, match="https"):
        build_app(
            ["--models-dir", str(models),
             "--backend-endpoint", "https://127.0.0.1:8080",
             "--settings-path", str(tmp_path / "settings.json")]
        )


def test_the_documented_managed_defaults() -> None:
    args = parse_args([])
    assert not args.attached and not args.no_backend  # MANAGED default
    assert args.llama_server_exe is None  # the settings/scan resolution
    assert args.llama_ctx is None and args.llama_ngl is None
    assert args.llama_args == ""


def test_no_backend_still_wins_over_managed(tmp_path: Path) -> None:
    """The admission law's precedence: --no-backend composes WITHOUT
    the port even under the managed default — never a wrapper without
    the honest form."""
    models = tmp_path / "models"
    models.mkdir()
    (models / "m.gguf").write_bytes(b"stub")
    gateway, _operations, transport, backend, _args = build_app(
        ["--models-dir", str(models), "--no-backend", "--port", "0",
         "--settings-path", str(tmp_path / "settings.json")]
    )
    assert backend is None
    assert "model.load" not in gateway.operation_names
    assert transport is not None
