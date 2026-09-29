r"""The ZERO-COMMAND Workbench launcher (wb-9; wb-10, the owner's
2026-09-25 zero-command law — «пользователь не должен вводить команды
чтобы запустить или скачать что-либо!»; re-pointed to the web client
at iter-290/D-245 — the owner's «удаляй redot» call deleted the
frozen Redot tree with the launcher's old frontend child; the web
dev server is the frontend half now).

What this script is: the operator's single entry point that starts
the WHOLE live stack — the Python gateway (`scripts/workbench_app.py`,
the MANAGED composition root: llama-server spawns on the first
model.load, the launch settings persist, the models manager imports
local GGUF files or fetches by URL) and the WEB frontend
(`frontend/` — React + TS + Vite, frontend-1/D-244; the browser
client stays same-origin to the Vite dev server, which forwards
`/gateway/*` to the loopback gateway). One command, two processes,
one honest shutdown:

```text
workbench_launch.py ──spawn──> workbench_app.py (the gateway; its
        │                        stdout watched for the bind line)
        └──after bind──> npm run dev  (cwd frontend/; the child env
                          carries GATEWAY_TARGET = the OBSERVED
                          bind URL — the Vite proxy target; Vite
                          prints its own Local: URL and --open
                          raises the browser)
either exits or Ctrl+C ──> the other stops (the gateway gets the
                           console-appropriate stop signal FIRST —
                           its own graceful path stops the managed
                           llama-server too, §25's bounded form)
```

Why the stdout line-watch instead of a health probe: the gateway
prints its bind URL only AFTER `transport.start()` returned — the
line IS the readiness evidence, observed without this launcher ever
opening a socket (scripts/ stays network-free; the app's own probe
surfaces ride their sanctioned modules). The OBSERVED bind URL is
also what the web child receives as `GATEWAY_TARGET` — the Vite
dev proxy dials the gateway the launcher actually started (never a
divergent committed default when `-- --port` moves the bind).

The web child law (D-245):

```text
1. resolve_npm()          npm over PATH (shutil.which — the
                          explicit extension on Windows, never a
                          shell); absent → the honest note, the
                          gateway still serves
2. node_modules missing   `npm install` runs FIRST (the owner's
                          zero-command law — never a manual step)
3. GATEWAY_TARGET         the observed bind URL forwarded to the
                          child env (the Vite proxy target)
4. --no-frontend          the honest gateway-only form (the test/
                          operator escape)
5. the group stop         the web child runs in its OWN session on
                          POSIX — the teardown signals the whole
                          tree (npm's sh→vite grandchildren die
                          with it, never orphaned); Windows rides
                          the console's own Ctrl+C group
```

The runtime bootstrap (§16): `workbench/runtime/models/` and
`workbench/runtime/llama.cpp/` are created when missing — the
operator's drop folders (GGUF files into models/, a llama.cpp
release folder into llama.cpp/ — the gateway's discovery scan finds
llama-server.exe in it).

Usage (the owner's forms — the FIRST one is the zero-command form:

    Workbench.bat                        (double-click; repo root)
    python scripts/workbench_launch.py   (run from the repo ROOT —
                                          inside scripts/ the path
                                          doubles: scripts/scripts/…)
    python scripts/workbench_launch.py -- --port 9000   # gateway args
    python scripts/workbench_launch.py --no-frontend    # gateway only

    # npm not on PATH AND not installable: the gateway still serves
    # and the honest note tells the operator how to open the
    # frontend by hand (never a fake "launched").
"""

from __future__ import annotations

import argparse
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GATEWAY_SCRIPT = REPO / "scripts" / "workbench_app.py"
FRONTEND_DIR = REPO / "frontend"

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

#: The web child's first-run install budget (`npm install` over a
#: cold cache on a slow link; a failure past it is loud, never a
#: silent hang — the gateway keeps serving, the note tells the
#: operator the manual form).
NPM_INSTALL_TIMEOUT_S = 900.0

#: The web child's teardown budget (Vite's own SIGINT path).
FRONTEND_STOP_GRACE_S = 5.0


class LaunchError(RuntimeError):
    """The launcher's loud failure (never a silent partial start)."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "the CanonSim Workbench zero-command launcher: the gateway "
            "(managed llama.cpp) + the web frontend (React + TS + Vite) "
            "together — Workbench.bat is the double-click form"
        )
    )
    parser.add_argument(
        "--no-frontend",
        action="store_true",
        help="start the gateway only (the explicit no-web-child form)",
    )
    known, gateway_args = parser.parse_known_args(argv)
    # The argparse "--" separator is OURS (the operator's
    # `-- --port 9000` form) — strip it before the child sees it:
    # workbench_app's parser has no positional args, a bare "--" is
    # its own loud refusal (the latent wb-9 bug, fixed with wb-10).
    if gateway_args and gateway_args[0] == "--":
        gateway_args = gateway_args[1:]
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


# ----------------------------------------------- the web child (D-245)


def resolve_npm() -> str | None:
    """The web child's executable: npm over PATH (`shutil.which` —
    on Windows this yields the explicit `npm.cmd`, which CreateProcess
    spawns without a shell; on POSIX the npm runner itself). One
    resolution point, no hardcoded paths, no second site — the
    CONTRACTS §5 D1 pattern (an external toolchain resolved ONE
    way). Absent → None (the honest note follows, never a guess)."""
    return shutil.which("npm")


def needs_install(frontend_dir: Path = FRONTEND_DIR) -> bool:
    """The first-run check: `frontend/node_modules` absent means the
    dependency tree must be installed before the dev server can run
    (the zero-command law — the launcher runs `npm install` itself,
    the operator never types it)."""
    return not (frontend_dir / "node_modules").is_dir()


def frontend_env(
    base: dict[str, str] | None = None, gateway_url: str = ""
) -> dict[str, str]:
    """The web child's environment: the OBSERVED bind URL forwarded
    as `GATEWAY_TARGET` (frontend/vite.config.ts's proxy target —
    the dev server dials the gateway the launcher actually started,
    never a divergent committed default when `-- --port` moved the
    bind). An empty URL (no parseable bind line) forwards NOTHING —
    Vite's own committed default target stands."""
    env = dict(os.environ if base is None else base)
    if gateway_url:
        env["GATEWAY_TARGET"] = gateway_url
    return env


# ------------------------------------------------------- child processes


def _spawn_gateway(gateway_args: list[str]) -> subprocess.Popen:
    """The gateway child: its own process group (Windows: the console's
    Ctrl+C does NOT race our controlled stop — we send CTRL_BREAK
    ourselves; the gateway's handler runs the graceful path), stdout +
    stderr merged into the watched pipe (line-buffered text) — and the
    child itself runs `-u`, so its bind line STREAMS through the pipe
    whatever the host environment (KI#93: `bufsize=1` only paces OUR
    reads; the child's writes were block-buffered without the host's
    PYTHONUNBUFFERED — CI and the owner's machines do not set it)."""
    command = [sys.executable, "-u", str(GATEWAY_SCRIPT), *gateway_args]
    kwargs: dict[str, int] = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    return subprocess.Popen(
        command,
        cwd=str(REPO),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        **kwargs,
    )


def _gateway_url_from_bind_line(line: str) -> str | None:
    """The OBSERVED bind ROOT out of the gateway's own bind line — the
    address the web child's proxy target is told to dial (never a
    divergent committed default when -- --port moved the bind). The
    marker already carries the scheme; the banner's URL is the
    transport's full ENDPOINT (``transport.url`` — the ``/op`` route
    included, the wb-4 shape), while the Vite proxy expects the ROOT
    and appends the route itself — so the forwarded value strips any
    path: scheme://host:port, never the endpoint (KI#98: the iter-227
    forward shipped ``http://host:port/op`` and every shell request
    landed on ``/op/op`` — 404, the dead session, the disabled
    picker)."""
    marker_at = line.find(BIND_MARKER)
    if marker_at < 0:
        return None
    rest = line[marker_at + len(BIND_MARKER):].strip()
    tokens = rest.split()
    if not tokens:
        return None
    first = tokens[0]
    route_at = first.find("/")
    if route_at >= 0:
        first = first[:route_at]
    host_port = first.rstrip("/")
    if not host_port:
        return None
    return "http://" + host_port


def _spawn_frontend(npm: str, gateway_url: str) -> subprocess.Popen:
    """The web child: `npm run dev --open` in frontend/, its OWN
    session on POSIX (a `killpg`-addressable tree — a bare
    SIGINT-to-npm would orphan npm's sh→vite grandchildren; Windows
    rides the console's own Ctrl+C group instead), the OBSERVED bind
    URL forwarded as GATEWAY_TARGET (the Vite proxy target — the
    dev server dials the gateway the launcher actually started)."""
    kwargs: dict[str, bool] = {}
    if os.name != "nt":
        kwargs["start_new_session"] = True
    return subprocess.Popen(
        [npm, "run", "dev", "--", "--open"],
        cwd=str(FRONTEND_DIR),
        env=frontend_env(gateway_url=gateway_url),
        **kwargs,
    )


def _signal_process(process: subprocess.Popen, sig: int) -> None:
    """Group-aware signal: a POSIX session leader takes its whole
    tree (the web child's grandchildren die with it); everyone else
    the pid itself (the gateway child shares the launcher's group —
    killpg refuses, the direct kill stands)."""
    if os.name != "nt" and hasattr(os, "killpg"):
        try:
            os.killpg(process.pid, sig)
            return
        except OSError:
            pass
    try:
        os.kill(process.pid, sig)
    except OSError:
        process.terminate()


def _hard_kill(process: subprocess.Popen) -> None:
    """The hard fallback — group-aware on POSIX (the whole tree),
    the process itself elsewhere."""
    if os.name != "nt" and hasattr(os, "killpg"):
        try:
            os.killpg(process.pid, signal.SIGKILL)
            return
        except OSError:
            pass
    process.kill()


def _stop_process(
    process: subprocess.Popen, grace_s: float, *, break_signal: int
) -> None:
    """The honest two-step stop: the graceful signal (CTRL_BREAK on
    Windows / SIGINT on POSIX — the child's own handlers), the grace
    deadline, then the hard kill. Never a guessed exit code."""
    if process.poll() is not None:
        return
    _signal_process(process, break_signal)
    try:
        process.wait(timeout=grace_s)
        return
    except subprocess.TimeoutExpired:
        pass
    _hard_kill(process)
    try:
        process.wait(timeout=grace_s)
    except subprocess.TimeoutExpired:
        pass


def _the_no_npm_note() -> None:
    """The honest note when npm is not resolvable: the gateway still
    serves; the operator gets the exact manual form (never a fake
    "launched") — install Node.js once, then the zero-command form
    works again."""
    print(
        "workbench_launch: the gateway is LIVE — npm was not found on "
        "PATH: install Node.js LTS from https://nodejs.org (the "
        "external toolchain, one resolution point), then run me "
        "again; the frontend can also be opened by hand:"
    )
    print("  cd frontend")
    print("  npm install")
    print("  npm run dev")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    # KI#93: the supervisor's own stream must be line-buffered when
    # piped — the boot report and the forwarded gateway lines are the
    # test's and the owner's contract; PYTHONUNBUFFERED is not set on
    # CI/owner machines, so a block-buffered stdout here starves any
    # reader until exit (never rely on the host's buffering mood).
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    for folder in bootstrap_runtime_layout():
        print(f"workbench_launch: created {folder}")
    npm = None if args.no_frontend else resolve_npm()
    if npm is not None:
        print(f"workbench_launch: the web child — {npm}")
        if needs_install():
            print(
                "workbench_launch: frontend/node_modules missing — "
                "running npm install first (the zero-command law; "
                "this can take a few minutes on a cold cache)"
            )
            try:
                installed = subprocess.run(
                    [npm, "install"],
                    cwd=str(FRONTEND_DIR),
                    timeout=NPM_INSTALL_TIMEOUT_S,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                installed = None
                print(
                    "workbench_launch: npm install failed "
                    f"({exc}) — the gateway keeps serving, the "
                    "note below tells the manual form"
                )
            if installed is not None and installed.returncode != 0:
                print(
                    "workbench_launch: npm install exited "
                    f"{installed.returncode} — the gateway keeps "
                    "serving, the note below tells the manual form"
                )
                npm = None
            elif installed is None:
                npm = None
    gateway = _spawn_gateway(args.gateway_args)
    frontend: subprocess.Popen | None = None
    try:
        bound = threading.Event()
        bound_url: list[str] = []
        stream_closed = threading.Event()

        def _pump() -> None:
            assert gateway.stdout is not None
            for raw_line in gateway.stdout:
                line = raw_line.rstrip("\n")
                print(f"[gateway] {line}")
                if BIND_MARKER in line:
                    url = _gateway_url_from_bind_line(line)
                    if url is not None:
                        bound_url.append(url)
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

        gateway_url = bound_url[0] if bound_url else ""
        if npm is None:
            if args.no_frontend:
                print(
                    "workbench_launch: the gateway is LIVE — the "
                    "web child skipped (--no-frontend, the explicit "
                    "gateway-only form)"
                )
            else:
                _the_no_npm_note()
        else:
            if gateway_url:
                print(
                    "workbench_launch: launching the web frontend "
                    f"({npm}) with GATEWAY_TARGET={gateway_url}"
                )
            else:
                print(
                    f"workbench_launch: launching the web frontend ({npm})"
                )
            try:
                frontend = _spawn_frontend(npm, gateway_url)
            except OSError as exc:
                print(
                    "workbench_launch: the web child failed to start "
                    f"({exc}) — the gateway keeps serving, the "
                    "manual form:"
                )
                _the_no_npm_note()
                frontend = None
        # The wait loop: whoever exits first ends the session — the
        # other child gets the honest stop (the gateway FIRST, so the
        # managed llama-server rides its own graceful path).
        while True:
            if frontend is not None and frontend.poll() is not None:
                print(
                    "workbench_launch: the web frontend closed — stopping "
                    "the gateway (the managed llama-server rides the "
                    "graceful stop)"
                )
                break
            if gateway.poll() is not None:
                print(
                    "workbench_launch: the gateway exited — stopping the "
                    "web frontend (the browser would show a dead proxy)"
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
        if frontend is not None and frontend.poll() is None:
            _stop_process(
                frontend, FRONTEND_STOP_GRACE_S, break_signal=signal.SIGINT
            )
            print("workbench_launch: the web frontend stopped")


if __name__ == "__main__":
    raise SystemExit(main())
