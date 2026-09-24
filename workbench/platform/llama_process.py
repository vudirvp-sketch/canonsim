"""The llama-server process mechanics (wb-8, the app spec §11.1's
MANAGED half + §2's "process mechanics | platform/process" row).

The law this module closes: **the operator's «llama.cpp тоже
запускаться при загрузке модели» call** — the workbench may OWN the
llama-server process (MANAGED), not merely observe it (wb-6's
ATTACHED form). Per §11.1 the ownership splits exactly two ways:

```text
application/runtime (the composition root, scripts/workbench_app.py)
        owns LIFECYCLE POLICY — when to spawn, what to load, when to
        stop, the replacement decision (prepare new → validate →
        ready → swap → retire old)
THIS module (platform/process)
        owns OS MECHANICS — spawn, the command line, handle/stdio
        ownership, exit observation, the bounded graceful stop
        (TERM → wait → kill), the readiness wait driven by an
        injected probe
```

The seam discipline (INV-4's spirit, §4.1): this module holds NO
network imports and NO HTTP — readiness is observed by calling a
PROBE the composition root injects (the engine adapter's own
`health()`, cli/engine.py — the one sanctioned outbound surface).
`workbench/` stays engine-agnostic otherwise: nothing here knows the
wire protocol, the model semantics, or the gateway.

The default flag set (the owner's «настройки подтягиваться и самые
нужные флаги» call — the RTX 3080 Ti + 32 GB RAM station's honest
defaults, re-verified 2026-09-25 against the current llama.cpp
server surface):

```text
-m <model path>     the file to load (the discovered GGUF)
--host 127.0.0.1    loopback only (the exposure law, app §4)
--port <port>       the backend port (the composition root's own)
-a <alias>          the model alias (= the logical_name — /props and
                    the API surface name the model by it)
-ngl 999            all layers on the GPU (the 12 GB VRAM station's
                    Q4_K_M-class budget; overridable per launch)
-c 8192             the context window (a chat-honest default;
                    overridable)
-fa on              flash attention (the current builds' on/off/auto
                    form; the CUDA default, pinned explicitly)
--jinja             the model's own chat template (the Gemma-class
                    requirement — without it the server's generic
                    template mangles the turns)
--no-webui          no browser UI on the loopback port (the Redot
                    shell is the only intended client)
```

Build-sensitive like every llama.cpp surface (app §20's law): the
defaults are the CONSERVATIVE admitted set; `extra_args` carries the
operator's own flags verbatim (the honest override — later rows
promote validated knobs into typed config as they earn consumers).
"""

from __future__ import annotations

import subprocess
import time
from collections.abc import Callable, Sequence
from pathlib import Path

__all__ = [
    "DEFAULT_CONTEXT",
    "DEFAULT_FLASH_ATTENTION",
    "DEFAULT_GPU_LAYERS",
    "DEFAULT_HOST",
    "LlamaProcessError",
    "LlamaServerProcess",
    "build_server_command",
]

#: The default GPU layer count — all layers (the single-GPU station's
#: Q4_K_M-class budget; a CPU-fallback station overrides it).
DEFAULT_GPU_LAYERS = 999

#: The default context window — a chat-honest mid size (KV budget on
#: the 12 GB station stays comfortable beside a Q4_K_M body).
DEFAULT_CONTEXT = 8192

#: The default flash-attention form — the current builds' explicit
#: "on" (the CUDA default made explicit, never an assumed "auto").
DEFAULT_FLASH_ATTENTION = "on"

#: The managed server's bind host — loopback only (app §4's exposure
#: law: MANAGED is still never an implicit LAN surface).
DEFAULT_HOST = "127.0.0.1"

_STOP_POLL_S = 0.05


class LlamaProcessError(RuntimeError):
    """A process-mechanics contract violation (LOUD — a spawn on a
    missing executable, a stop of nothing; never a silent no-op)."""


def build_server_command(
    exe: str | Path | Sequence[str],
    model_path: str | Path,
    *,
    host: str = DEFAULT_HOST,
    port: int,
    alias: str | None = None,
    context: int = DEFAULT_CONTEXT,
    gpu_layers: int = DEFAULT_GPU_LAYERS,
    flash_attention: str = DEFAULT_FLASH_ATTENTION,
    jinja: bool = True,
    no_webui: bool = True,
    extra_args: Sequence[str] = (),
) -> list[str]:
    """The honest default command line (§22: the launcher selects
    runtime paths; the flags stay the platform's typed surface). The
    alias rides `-a` so the served model's API identity IS the
    workbench logical_name (§9: one name, one identity).

    `exe` is the command LEAD: one token (the executable path — the
    launcher's CLI form) or a short prefix (an interpreter + script —
    the contract tests' stand-in form; never a shell string)."""
    lead: list[str]
    if isinstance(exe, (str, Path)):
        lead = [str(exe)]
    else:
        lead = [str(part) for part in exe]
        if not lead or not lead[0].strip():
            raise LlamaProcessError(
                "the command lead is empty — the executable path is required"
            )
    if not str(model_path).strip():
        raise LlamaProcessError("the model path is empty")
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise LlamaProcessError(f"port {port!r} must be an int in [1, 65535]")
    if not isinstance(context, int) or context <= 0:
        raise LlamaProcessError(f"context {context!r} must be a positive int")
    if not isinstance(gpu_layers, int) or gpu_layers < 0:
        raise LlamaProcessError(
            f"gpu_layers {gpu_layers!r} must be a non-negative int"
        )
    command: list[str] = [
        *lead,
        "-m", str(model_path),
        "--host", str(host),
        "--port", str(port),
        "-ngl", str(gpu_layers),
        "-c", str(context),
        "-fa", str(flash_attention),
    ]
    if alias is not None and alias.strip():
        command += ["-a", alias.strip()]
    if jinja:
        command.append("--jinja")
    if no_webui:
        command.append("--no-webui")
    command += [str(arg) for arg in extra_args]
    return command


class LlamaServerProcess:
    """One managed llama-server's OS mechanics: spawn (stdout/stderr
    captured for the honest failure note), exit observation, and the
    §11.1 bounded graceful stop — TERM, the grace deadline, then
    kill; the ACTUAL outcome is reported, never assumed.

    The process object holds no policy: it does not decide when to
    start or what to load, and it never probes the network (the
    composition root injects the readiness probe — the engine
    adapter's health(), keeping INV-4's single outbound surface).
    """

    def __init__(
        self, command: Sequence[str], *, cwd: Path | None = None
    ) -> None:
        if not command or not str(command[0]).strip():
            raise LlamaProcessError(
                "the command must lead with the executable path"
            )
        self._command = [str(part) for part in command]
        self._cwd = cwd
        self._process: subprocess.Popen[bytes] | None = None

    @property
    def command(self) -> list[str]:
        """The exact command line (the honest evidence line — the
        launcher prints it; the flags are never a hidden default)."""
        return list(self._command)

    @property
    def running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def start(self) -> None:
        """Spawn (§11.1 STARTING): a loud error on a missing/failed
        executable — the captured stderr tail rides the message, the
        honest cause, never 'it did not work'."""
        if self._process is not None:
            raise LlamaProcessError(
                "the process is already spawned (one process per object — "
                "the replacement path constructs a fresh one, §11.1)"
            )
        try:
            self._process = subprocess.Popen(
                self._command,
                cwd=str(self._cwd) if self._cwd is not None else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except OSError as exc:
            raise LlamaProcessError(
                f"cannot spawn {self._command[0]!r}: {exc} — pass "
                "--llama-server-exe with the actual path (the owner's "
                "station: D:\\llama.cpp\\llama-server.exe)"
            ) from exc

    def wait_ready(
        self,
        probe: Callable[[], bool],
        *,
        timeout_s: float,
        poll_s: float = 0.25,
    ) -> bool:
        """§11.1 PROBING → READY: poll the injected probe until it
        answers True or the deadline passes. A dead process fails the
        wait immediately (the exit code is the honest evidence); a
        timeout returns False — the caller decides the failure's
        vocabulary, this side never fabricates readiness."""
        deadline = time.monotonic() + timeout_s
        while True:
            if not self.running:
                return False
            if probe():
                return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(poll_s)

    def stop(self, *, grace_s: float = 10.0) -> int | None:
        """§11.1's bounded graceful stop: TERM → the grace deadline →
        kill; the returned value is the OBSERVED exit code (None when
        the process was never spawned or already reaped by the OS —
        the truth, never a guessed 0)."""
        process = self._process
        if process is None:
            return None
        if process.poll() is not None:
            return process.returncode
        process.terminate()
        try:
            return process.wait(timeout=max(0.0, grace_s))
        except subprocess.TimeoutExpired:
            process.kill()
            return process.wait()

    def exit_code(self) -> int | None:
        """The observed exit code (None while running — §11.1's exit
        observation half; never a blocking wait)."""
        process = self._process
        if process is None:
            return None
        return process.returncode

    def stderr_tail(self, limit: int = 400) -> str:
        """The captured stderr tail for the honest failure note (the
        spawn/ready failure's observed cause — bounded, never the
        whole log). Best-effort on a running process (a non-blocking
        drain; empty when nothing new was captured)."""
        process = self._process
        if process is None or process.stderr is None:
            return ""
        try:
            import os

            os.set_blocking(process.stderr.fileno(), False)
            chunk = process.stderr.read() or b""
        except (OSError, ValueError):
            return ""
        if not chunk:
            return ""
        text = chunk.decode("utf-8", errors="replace").strip()
        return text[-limit:]
