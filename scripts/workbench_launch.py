r"""The ZERO-COMMAND Workbench launcher (wb-9; wb-10, the owner's
2026-09-25 fix list — «редот у меня такой …\\Redot_v26.2-stable_
windows_win64, redot.windows.editor.x86_64.exe, где найти redot.exe
и как его подключить?» + «пользователь не должен вводить команды
чтобы запустить или скачать что-либо!»).

What this script is: the operator's single entry point that starts
the WHOLE live stack — the Python gateway (`scripts/workbench_app.py`,
the MANAGED composition root: llama-server spawns on the first
model.load, the launch settings persist, the models manager imports
local GGUF files or fetches by URL) and the Redot frontend
(`workbench/presentation/redot/` — the shell dials the gateway on
loopback). One command, two processes, one honest shutdown:

```text
workbench_launch.py ──spawn──> workbench_app.py (the gateway; its
        │                        stdout watched for the bind line)
        └──after bind──> redot --path workbench/presentation/redot
                       -- --gateway-url <the observed bind URL>
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
also what the Redot child receives as `--gateway-url` — the shell
dials the gateway the launcher actually started (never a divergent
committed default when `-- --port` moves the bind).

The Redot executable resolution (wb-10 — the owner's exact layout:
a Redot RELEASE FOLDER on the Desktop, `redot.windows.editor.x86_
64.exe` inside — «где найти redot.exe и как его подключить?»):

```text
1. --redot-exe <path>            an .exe OR a release FOLDER
                                  (the folder is scanned for the
                                  engine executable — root level,
                                  then one folder deep, sorted)
2. workbench/runtime/launcher.json   the persisted pick (the first
                                  run's folder-picker answer)
3. REDOT_EXE                      the env convention (exe or folder)
4. the common-roots auto-scan     Desktop / OneDrive Desktop /
                                  LOCALAPPDATA\Programs / Program
                                  Files — any *Redot* folder
5. the interactive folder picker  a native directory dialog (tk),
                                  ONCE — the pick persists
6. --no-redot                     the honest gateway-only form
```

The runtime bootstrap (§16): `workbench/runtime/models/` and
`workbench/runtime/llama.cpp/` are created when missing — the
operator's drop folders (GGUF files into models/, a llama.cpp
release folder into llama.cpp/ — the gateway's discovery scan finds
llama-server.exe in it).

Usage (the owner's forms — the FIRST one is the zero-command form:

    Workbench.bat                        (double-click; repo root)
    Workbench Setup.bat                  (re-pick the Redot folder)

    python scripts/workbench_launch.py   (run from the repo ROOT —
                                          inside scripts/ the path
                                          doubles: scripts/scripts/…)
    python scripts/workbench_launch.py --redot-exe "C:/…/Redot_v26.2-stable_windows_win64"
    REDOT_EXE=C:/Redot/Redot.exe python scripts/workbench_launch.py
    python scripts/workbench_launch.py -- --port 9000   # gateway args
    python scripts/workbench_launch.py --no-redot       # gateway only

    # no Redot executable resolvable AND no picker answer: the
    # gateway still serves and the honest note tells the operator
    # how to open the frontend by hand (never a fake "launched").
"""

from __future__ import annotations

import argparse
import json
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

#: The launcher's own persisted settings (§16's USER_CONFIG role —
#: the FIRST picker answer survives restarts; gitignored with the
#: whole workbench/runtime/ tree). ONE field today: redot_exe.
LAUNCHER_SETTINGS_PATH = REPO / "workbench" / "runtime" / "launcher.json"

#: The engine executable names a Redot release folder carries, in
#: preference order (the owner's build: redot.windows.editor.x86_64.
#: exe — the Windows console-less editor binary; the .console.
#: variant, the 32-bit build, and the POSIX builds follow).
REDOT_EXE_NAMES: tuple[str, ...] = (
    "redot.windows.editor.x86_64.exe",
    "redot.console.windows.editor.x86_64.exe",
    "redot.windows.editor.x86_32.exe",
    "redot.exe",
    "redot_linux.x86_64",
    "redot.x86_64",
)

#: The common roots the auto-scan walks for a Redot release folder
#: (the owner's real layout: OneDrive Desktop; the plain Desktop and
#: the program-install roots follow). Missing roots are skipped.
COMMON_ROOT_CANDIDATES: tuple[str, ...] = (
    "Desktop",
    "OneDrive/Desktop",
    "OneDrive/Рабочий стол",
    "AppData/Local/Programs",
    "AppData/Local",
    "Program Files",
    "Program Files (x86)",
)

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
            "the CanonSim Workbench zero-command launcher: the gateway "
            "(managed llama.cpp) + the Redot frontend together — "
            "Workbench.bat is the double-click form"
        )
    )
    parser.add_argument(
        "--redot-exe",
        default=None,
        help="the Redot executable OR its release folder (scanned for "
        "the engine .exe); default: the persisted pick, then REDOT_EXE, "
        "then the Desktop/Programs auto-scan, then the folder picker",
    )
    parser.add_argument(
        "--pick-redot",
        action="store_true",
        help="force the Redot folder picker (the Setup form — the pick "
        "persists in workbench/runtime/launcher.json)",
    )
    parser.add_argument(
        "--no-redot",
        action="store_true",
        help="start the gateway only (the explicit form of no executable)",
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


# ------------------------------------------------- the launcher settings


def load_launcher_settings(path: Path = LAUNCHER_SETTINGS_PATH) -> dict[str, str]:
    """The persisted pick ({} when absent). A corrupt file is LOUD on
    the console but never a brick — the launcher continues to the
    resolution chain and re-persists on the next successful pick."""
    if not path.is_file():
        return {}
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(
            f"workbench_launch: the launcher settings {path} are "
            f"unreadable ({exc}) — continuing with the resolution chain"
        )
        return {}
    if not isinstance(document, dict):
        print(
            f"workbench_launch: the launcher settings {path} are not a "
            "JSON object — continuing with the resolution chain"
        )
        return {}
    return {
        str(key): str(value) for key, value in document.items()
    }


def save_launcher_settings(
    redot_exe: str, path: Path = LAUNCHER_SETTINGS_PATH
) -> None:
    """Persist the pick atomically (the settings.py pattern: write the
    temporary file, os.replace into place — a killed save never
    leaves a half-written launcher.json)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps({"redot_exe": redot_exe}, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


# ----------------------------------------------- the Redot exe resolution


def redot_exe_in_folder(folder: Path) -> Path | None:
    """The engine executable inside a Redot RELEASE FOLDER: the known
    names at the root first (the preference order), then any other
    `redot*` executable at the root, then the same walk ONE folder
    deep (a release unpacked into a nested folder). One deterministic
    order — sorted children, first hit wins, never a glob race."""
    if not folder.is_dir():
        return None

    def _hit(candidate: Path) -> bool:
        if not candidate.is_file():
            return False
        name = candidate.name.lower()
        if not name.startswith("redot"):
            return False
        if os.name == "nt":
            return name.endswith(".exe")
        return os.access(candidate, os.X_OK)

    for name in REDOT_EXE_NAMES:
        candidate = folder / name
        if _hit(candidate):
            return candidate
    root_hits = sorted(
        (child for child in folder.iterdir() if _hit(child)),
        key=lambda p: p.name,
    )
    if root_hits:
        return root_hits[0]
    for child in sorted(folder.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        for name in REDOT_EXE_NAMES:
            candidate = child / name
            if _hit(candidate):
                return candidate
        nested_hits = sorted(
            (grandchild for grandchild in child.iterdir() if _hit(grandchild)),
            key=lambda p: p.name,
        )
        if nested_hits:
            return nested_hits[0]
    return None


def resolve_redot_path(value: str, *, strict: bool = False) -> str | None:
    """One explicit value (the CLI argument, the persisted pick, or
    the env variable): an .exe passes VERBATIM (the operator's
    explicit hand is never second-guessed — a broken path is the
    spawn's own loud error); a FOLDER is scanned for the engine
    executable; anything else is None (the honest skip, never a
    guess).

    `strict` (the --redot-exe CLI form and the REDOT_EXE env — both
    the operator's EXPLICIT hand, set at invocation time): a value
    that is neither a file nor a folder ALSO passes verbatim — the
    spawn itself reports the broken path (workbench_app's
    resolve_llama_exe law, one name one meaning). The persisted pick
    (saved once, the folder may move) SKIPS a stale path and falls
    through the chain — a moved Redot folder recovers by the scan or
    the picker, never a dead launcher."""
    text = value.strip().strip('"')
    if not text:
        return None
    path = Path(text).expanduser()
    if path.is_file():
        return str(path)
    if path.is_dir():
        found = redot_exe_in_folder(path)
        if found is not None:
            return str(found)
        print(
            f"workbench_launch: the folder {text!r} carries no Redot "
            "executable (scanned the root and one folder deep) — "
            "continuing the resolution chain"
        )
        return None
    if strict:
        return text
    # a non-existent non-strict value (a stale persisted pick / env):
    # surfaced loudly, skipped — the chain recovers, never a dead launcher
    print(
        f"workbench_launch: {text!r} is neither a file nor a folder — "
        "continuing the resolution chain"
    )
    return None


def common_scan_roots(home: Path | None = None) -> list[Path]:
    """The deterministic auto-scan roots: the home directory's common
    candidate children (missing ones skipped — an absent root is not
    an error, it is simply no Redot there)."""
    base = home if home is not None else Path.home()
    roots: list[Path] = []
    for relative in COMMON_ROOT_CANDIDATES:
        candidate = (base / relative).resolve()
        if candidate.is_dir():
            roots.append(candidate)
    return roots


def auto_discover_redot(roots: list[Path] | None = None) -> str | None:
    """The unattended fallback: walk the common roots for a folder
    whose name mentions Redot (case-insensitive), scan it for the
    engine executable — the owner's actual layout (a
    `Redot_v26.2-stable_windows_win64` folder on the Desktop) lands
    here with zero configuration. First hit in the sorted order wins."""
    scan_roots = common_scan_roots() if roots is None else roots
    for root in scan_roots:
        try:
            children = sorted(root.iterdir(), key=lambda p: p.name)
        except OSError:
            continue
        for child in children:
            if not child.is_dir() or "redot" not in child.name.lower():
                continue
            found = redot_exe_in_folder(child)
            if found is not None:
                return str(found)
    return None


def _prompt_pick_redot_folder() -> str | None:
    """The interactive fallback (the owner's «просто открывающийся
    проводник»): a NATIVE directory picker over tkinter, shown when
    nothing else resolved. The pick PERSISTS (launcher.json) — the
    operator answers once, ever. A headless/absent-tk environment
    returns None (the honest note follows, never a crash)."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception as exc:  # no display, no tkinter — the honest skip
        print(
            "workbench_launch: no interactive picker available "
            f"({exc}) — pass --redot-exe or set REDOT_EXE"
        )
        return None
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory(
            title=(
                "Where is Redot? Pick the Redot folder "
                "(the one with redot.windows.editor.x86_64.exe)"
            ),
            mustexist=True,
        )
        root.destroy()
    except Exception as exc:
        print(
            f"workbench_launch: the folder picker failed ({exc}) — "
            "pass --redot-exe or set REDOT_EXE"
        )
        return None
    if not folder:
        return None  # cancelled — the honest note follows
    found = redot_exe_in_folder(Path(folder))
    if found is None:
        print(
            f"workbench_launch: the picked folder {folder!r} carries no "
            "Redot executable — nothing persisted"
        )
        return None
    return str(found)


def resolve_redot_exe(
    cli_value: str | None,
    persisted: str = "",
    env_value: str | None = None,
    *,
    pick: bool = False,
) -> tuple[str | None, str]:
    """The whole resolution chain (§ the module docstring's ladder).
    Returns (the executable path or None, the origin note — the
    honest evidence line the console prints). `pick` forces the
    interactive folder picker FIRST (the Setup form). `env_value`
    left at None reads the REDOT_EXE environment variable NOW (the
    visual_proof.py convention's one name, one meaning — an explicit
    argument wins for the tests)."""
    if pick:
        picked = _prompt_pick_redot_folder()
        if picked is not None:
            save_launcher_settings(picked)
            return picked, "the fresh folder pick"
        print(
            "workbench_launch: no Redot picked — falling through the "
            "resolution chain"
        )
    if env_value is None:
        env_value = os.environ.get("REDOT_EXE")
    for label, value, strict in (
        ("the --redot-exe argument", cli_value, True),
        (
            "the persisted pick (workbench/runtime/launcher.json)",
            persisted,
            False,
        ),
        ("the REDOT_EXE environment variable", env_value, True),
    ):
        if value is None or not str(value).strip():
            continue
        resolved = resolve_redot_path(str(value), strict=strict)
        if resolved is not None:
            return resolved, label
    discovered = auto_discover_redot()
    if discovered is not None:
        return discovered, "the common-roots auto-scan (a Redot folder found)"
    return None, "no resolution"


# ------------------------------------------------------- child processes


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
        bufsize=1,
        **kwargs,
    )


def _gateway_url_from_bind_line(line: str) -> str | None:
    """The OBSERVED bind URL out of the gateway's own bind line — the
    address the Redot child is told to dial (never a divergent
    committed default when -- --port moved the bind). The marker
    already carries the scheme: the remainder IS host:port."""
    marker_at = line.find(BIND_MARKER)
    if marker_at < 0:
        return None
    rest = line[marker_at + len(BIND_MARKER):].strip()
    tokens = rest.split()
    if not tokens:
        return None
    host_port = tokens[0].rstrip("/")
    if not host_port:
        return None
    return "http://" + host_port


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
    settings = load_launcher_settings()
    redot_exe = None
    redot_origin = "the --no-redot form"
    if not args.no_redot:
        redot_exe, redot_origin = resolve_redot_exe(
            args.redot_exe,
            settings.get("redot_exe", ""),
            pick=args.pick_redot,
        )
    if redot_exe is not None:
        print(f"workbench_launch: the frontend executable — {redot_exe}")
        print(f"workbench_launch: resolved through {redot_origin}")
    gateway = _spawn_gateway(args.gateway_args)
    redot: subprocess.Popen | None = None
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
        if redot_exe is None:
            print(
                "workbench_launch: the gateway is LIVE — no Redot "
                "executable resolved: run Workbench Setup.bat (or pass "
                "--redot-exe <folder-or-exe>, or set REDOT_EXE); the "
                "frontend can also be opened by hand:"
            )
            print(f'  <redot> --path "{REDOT_PROJECT}"')
        else:
            command = [redot_exe, "--path", str(REDOT_PROJECT)]
            if gateway_url:
                command += ["--", "--gateway-url", gateway_url]
                print(
                    "workbench_launch: launching the frontend "
                    f"({redot_exe}) against {gateway_url}"
                )
            else:
                print(
                    f"workbench_launch: launching the frontend ({redot_exe})"
                )
            redot = subprocess.Popen(command, cwd=str(REPO))
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
