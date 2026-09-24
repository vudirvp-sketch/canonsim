"""The ONE-command Workbench launcher (wb-9, the owner's 2026-09-25
«чтобы пользователь открыл воркбенч, зашел и загрузил модель» call).

What this script is: the operator's single entry point that starts
the WHOLE live stack — the Python gateway (`scripts/workbench_app.py`,
the MANAGED composition root: llama-server spawns on the first
model.load, the launch settings persist, the models manager fetches
GGUF files) and, when a Redot executable is resolvable, the frontend
(`workbench/presentation/redot/` — the shell dials the gateway on
loopback). One command, two processes, one honest shutdown:

```text
workbench_launch.py ──spawn──> workbench_app.py (the gateway; its
        │                        stdout watched for the bind line)
        └──after bind──> redot --path workbench/presentation/redot
either exits or Ctrl+C ──> the other stops (the gateway gets the
                           console-appropriate stop signal FIRST —
                           its own graceful path stops the managed
                           llama-server too, §25's bounded form)
```

Why the stdout line-watch instead of a health probe: the gateway
prints its bind URL only AFTER `transport.start()` returned — the
line IS the readiness evidence, observed without this launcher ever
opening a socket (scripts/ stays network-free; the app's own probe
surfaces ride their sanctioned modules).

The runtime bootstrap (§16): `workbench/runtime/models/` and
`workbench/runtime/llama.cpp/` are created when missing — the
operator's drop folders (GGUF files into models/, a llama.cpp
release folder into llama.cpp/ — the gateway's discovery scan finds
llama-server.exe in it).

Usage (the owner's forms):

    python scripts/workbench_launch.py
    python scripts/workbench_launch.py --redot-exe C:/Redot/Redot.exe
    REDOT_EXE=C:/Redot/Redot.exe python scripts/workbench_launch.py
    python scripts/workbench_launch.py -- --port 9000   # gateway args

    # no Redot executable resolvable: the gateway still serves and
    # the honest note tells the operator how to open the frontend
    # by hand (never a fake "launched").
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GATEWAY_SCRIPT = REPO / "scripts" / "workbench_app.py"
REDOT_PROJECT = REPO / "workbench" / "presentation" / "redot"

#: The gateway's bind-line marker — the readiness evidence this
#: launcher watches for (workbench_app.main's own print, emitted only
#: after the transport is bound and serving).
BIND_MARKER = "loopback gateway http://"

#: The gateway's boot budget (a cold Python start + the composition;
#: a slow disk deserves the margin — the failure names its own cause).
GATEWAY_BOOT_TIMEOUT_S = 90.0

#: The gateway's graceful-stop budget: the stop signal first (the
#: gateway's own handlers run the bounded graceful path — the managed
#: llama-server included), then the hard fallback.
GATEWAY_STOP_GRACE_S = 15.0

#: The Redot teardown budget (the engine's own quit path).
REDOT_STOP_GRACE_S = 5.0


class LaunchError(RuntimeError):
    """The launcher's loud failure (never a silent partial start)."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "the CanonSim Workbench one-command launcher: the gateway "
            "(managed llama.cpp) + the Redot frontend together"
        )
    )
    parser.add_argument(
        "--redot-exe",
        default=None,
        help="the Redot executable (default: the REDOT_EXE environment "
        "variable; without either, the gateway serves alone and the "
        "note tells you how to open the frontend by hand)",
    )
    parser.add_argument(
        "--no-redot",
        action="store_true",
        help="start the gateway only (the explicit form of no executable)",
    )
    known, gateway_args = parser.parse_known_args(argv)
    known.gateway_args = [str(a) for a in gateway_args]
    return known


def bootstrap_runtime_layout(repo: Path = REPO) -> list[Path]:
    """§16's startup/recovery half: create the runtime drop folders
    when missing (`runtime/models/` + `runtime/llama.cpp/` — both
    gitignored). Returns the folders CREATED (the honest evidence —
    an already-present folder is not re-created, never reported)."""
    created: list[Path] = []
    for role in ("models", "llama.cpp"):
        folder = repo / "workbench" / "runtime" / role
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            created.append(folder)
    return created


def resolve_redot_exe(cli_value: str | None) -> str | None:
    """The frontend's executable: the CLI argument, then the REDOT_EXE
    environment variable (the visual_proof.py convention — one name,
    one meaning across the repo's tooling), then None (the honest
    gateway-only form)."""
    if cli_value is not None and cli_value.strip():
        return cli_value.strip()
    from_env = os.environ.get("REDOT_EXE", "").strip()
    if from_env:
        return from_env
    return None


def _spawn_gateway(gateway_args: list[str]) -> subprocess.Popen:
    """The gateway child: its own process group (Windows: the console's
    Ctrl+C does NOT race our controlled stop — we send CTRL_BREAK
    ourselves; the gateway's handler runs the graceful path), stdout +
    stderr merged into the watched pipe (line-buffered text)."""
    command = [sys.executable, str(GATEWAY_SCRIPT), *gateway_args]
    kwargs: dict[str, int] = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    return subprocess.Popen(
        command,
        cwd=str(REPO),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        buffering=1,
        **kwargs,
    )


def _stop_process(
    process: subprocess.Popen, grace_s: float, *, break_signal: int
) -> None:
    """The honest two-step stop: the graceful signal (CTRL_BREAK on
    Windows / SIGINT on POSIX — the child's own handlers), the grace
    deadline, then the hard kill. Never a guessed exit code."""
    if process.poll() is not None:
        return
    try:
        os.kill(process.pid, break_signal)
    except OSError:
        process.terminate()
    try:
        process.wait(timeout=grace_s)
        return
    except subprocess.TimeoutExpired:
        pass
    process.kill()
    try:
        process.wait(timeout=grace_s)
    except subprocess.TimeoutExpired:
        pass


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    for folder in bootstrap_runtime_layout():
        print(f"workbench_launch: created {folder}")
    redot_exe = None if args.no_redot else resolve_redot_exe(args.redot_exe)
    gateway = _spawn_gateway(args.gateway_args)
    redot: subprocess.Popen | None = None
    try:
        bound = threading.Event()
        stream_closed = threading.Event()

        def _pump() -> None:
            assert gateway.stdout is not None
            for raw_line in gateway.stdout:
                line = raw_line.rstrip("\n")
                print(f"[gateway] {line}")
                if BIND_MARKER in line:
                    bound.set()
            stream_closed.set()

        pump = threading.Thread(target=_pump, daemon=True)
        pump.start()
        deadline = time.monotonic() + GATEWAY_BOOT_TIMEOUT_S
        while (
            not bound.is_set()
            and not stream_closed.is_set()
            and time.monotonic() < deadline
        ):
            time.sleep(0.1)
        if not bound.is_set():
            # the gateway died or never bound — the honest loud exit
            # (its forwarded output above names the cause).
            if gateway.poll() is None:
                _stop_process(
                    gateway, 5.0, break_signal=signal.SIGINT
                )
            detail = (
                f"exit code {gateway.returncode}"
                if gateway.returncode is not None
                else f"no bind line within {GATEWAY_BOOT_TIMEOUT_S:.0f}s"
            )
            print(
                "workbench_launch: the gateway failed to serve "
                f"({detail}) — its output above names the cause",
                file=sys.stderr,
            )
            return 2

        if redot_exe is None:
            print(
                "workbench_launch: the gateway is LIVE — no Redot "
                "executable (pass --redot-exe or set REDOT_EXE); open "
                "the frontend by hand:"
            )
            print(f'  <redot> --path "{REDOT_PROJECT}"')
        else:
            print(
                f"workbench_launch: launching the frontend ({redot_exe})"
            )
            redot = subprocess.Popen(
                [redot_exe, "--path", str(REDOT_PROJECT)], cwd=str(REPO)
            )
        # The wait loop: whoever exits first ends the session — the
        # other child gets the honest stop (the gateway FIRST, so the
        # managed llama-server rides its own graceful path).
        while True:
            if redot is not None and redot.poll() is not None:
                print(
                    "workbench_launch: the frontend closed — stopping "
                    "the gateway (the managed llama-server rides the "
                    "graceful stop)"
                )
                break
            if gateway.poll() is not None:
                print(
                    "workbench_launch: the gateway exited — stopping the "
                    "frontend (the shell would show 'gateway unreachable')"
                )
                break
            time.sleep(0.2)
        return 0
    except KeyboardInterrupt:
        print(
            "workbench_launch: Ctrl+C — the graceful stop (the managed "
            "llama-server rides the gateway's own shutdown path)"
        )
        return 0
    finally:
        break_signal = (
            signal.CTRL_BREAK_EVENT  # type: ignore[attr-defined]
            if os.name == "nt"
            else signal.SIGINT
        )
        if gateway.poll() is None:
            _stop_process(
                gateway, GATEWAY_STOP_GRACE_S, break_signal=break_signal
            )
            print("workbench_launch: the gateway stopped")
        if redot is not None and redot.poll() is None:
            _stop_process(
                redot, REDOT_STOP_GRACE_S, break_signal=signal.SIGINT
            )
            print("workbench_launch: the frontend stopped")


if __name__ == "__main__":
    raise SystemExit(main())
