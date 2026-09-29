"""iter-290's claim packet — the zero-command launcher re-pointed to
the web client (`scripts/workbench_launch.py`, the owner's 2026-09-29
«удаляй redot» call; D-245 deleted the frozen Redot tree WITH the
launcher's old frontend half).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE SPAWN ITSELF: the REAL launcher process starts the REAL
   gateway child, observes the bind line, reports the honest
   gateway-only note under `--no-frontend`, and shuts down on
   Ctrl+C (the wb-10 owner-reported `Popen.__init__() got an
   unexpected keyword argument 'buffering'` crash stays dead —
   KI#93's no-host-PYTHONUNBUFFERED law included).
2. THE NPM RESOLUTION: npm resolves over PATH; an empty PATH is
   the honest None — never a guess, never a shell.
3. THE INSTALL CHECK: `frontend/node_modules` present/absent
   decides the first-run `npm install` step.
4. THE GATEWAY_TARGET FORWARD: the web child's env carries the
   OBSERVED bind URL (the Vite proxy target — never a divergent
   committed default); an empty URL forwards nothing and Vite's own
   committed default target stands.
5. THE BIND-URL PARSE: the gateway's own bind line yields the ROOT
   the proxy expects (never the /op endpoint — KI#98's doubled-route
   death), and the REAL gateway's root actually serves POST /op.
6. THE CLI FORMS: `--no-frontend` parses; the bare `--` separator
   is stripped before the gateway child's parser sees it.
"""

from __future__ import annotations

import json
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from workbench_launch import (  # noqa: E402
    _gateway_url_from_bind_line,
    frontend_env,
    needs_install,
    parse_args,
    resolve_npm,
)


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


# ----------------------------------------------- 1. the spawn itself


def test_the_real_launcher_spawns_and_stops_the_gateway() -> None:
    """The owner-reported crash, pinned dead: the launcher's gateway
    child (Popen with the line-buffered pipe) must CONSTRUCT and reach
    the bind line — `buffering` (not a Popen keyword) refused the
    spawn before anything served. Then SIGINT stops the session.
    KI#93: the whole chain must stream WITHOUT the host's
    PYTHONUNBUFFERED (CI and the owner's machines never set it —
    the sandbox's global PYTHONUNBUFFERED=1 masked three red CI
    iterations), so this spawn strips it: the launcher owns the
    buffering itself (the gateway child rides `-u`, the supervisor
    line-buffers its own stdout)."""
    port = _free_port()
    process = subprocess.Popen(
        [
            sys.executable,
            str(REPO / "scripts" / "workbench_launch.py"),
            "--no-frontend",
            "--",
            "--no-backend",
            "--port",
            str(port),
        ],
        cwd=str(REPO),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env={
            key: value
            for key, value in os.environ.items()
            if key != "PYTHONUNBUFFERED"
        },
    )
    lines: list[str] = []
    deadline = time.monotonic() + 90.0
    try:
        assert process.stdout is not None
        while time.monotonic() < deadline:
            line = process.stdout.readline()
            if not line:
                break
            lines.append(line.rstrip("\n"))
            if "gateway is LIVE" in line:
                break
        else:
            raise AssertionError(
                "the launcher never reported the live gateway:\n"
                + "\n".join(lines[-20:])
            )
        assert any("loopback gateway http://127.0.0.1:" in line for line in lines), (
            "the bind line must ride the forwarded gateway output"
        )
        assert any(
            "the web child skipped (--no-frontend" in line for line in lines
        ), "the honest gateway-only note (never a fake 'launched')"
        process.send_signal(signal.SIGINT)
        process.wait(timeout=30.0)
        assert process.returncode == 0, "\n".join(lines[-20:])
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=10.0)


# ------------------------------------ 2. the npm resolution (D-245)


def test_npm_resolves_over_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """npm is found over the operator's PATH — the one resolution
    point (the CONTRACTS §5 D1 pattern; never a hardcoded path)."""
    npm = resolve_npm()
    if npm is None:  # a CI image without node: the honest skip
        return
    assert Path(npm).is_absolute() and Path(npm).exists()


def test_an_empty_path_is_the_honest_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No npm on PATH is the honest None — the launcher then prints
    the manual note and keeps serving the gateway; never a guess,
    never a shell fallback."""
    monkeypatch.setenv("PATH", "")
    assert resolve_npm() is None


def test_a_missing_node_modules_means_install(tmp_path: Path) -> None:
    """The first-run check: an absent dependency tree installs before
    the dev server runs (the zero-command law — the operator never
    types `npm install`)."""
    assert needs_install(tmp_path) is True
    (tmp_path / "node_modules").mkdir()
    assert needs_install(tmp_path) is False


# --------------------------------- 3. the GATEWAY_TARGET forward


def test_the_child_env_carries_the_observed_url() -> None:
    """The OBSERVED bind URL is the Vite proxy target — the web
    child dials the gateway the launcher actually started (never a
    divergent committed default when `-- --port` moves the bind)."""
    env = frontend_env({"PATH": "/bin"}, "http://127.0.0.1:9000")
    assert env == {"PATH": "/bin", "GATEWAY_TARGET": "http://127.0.0.1:9000"}


def test_an_unparsed_bind_forwards_nothing() -> None:
    """An empty URL (no parseable bind line) forwards NO variable —
    Vite's own committed default target stands; the launcher never
    invents a URL."""
    env = frontend_env({"PATH": "/bin"}, "")
    assert env == {"PATH": "/bin"}


# ------------------------------------------ 4. the bind-line parse


def test_the_bind_line_yields_the_gateway_url() -> None:
    # KI#98: the REAL banner carries the transport's full ENDPOINT
    # (transport.url — the /op route included, the wb-4 shape); the
    # forwarded value is the ROOT the Vite proxy targets — never the
    # endpoint.
    assert _gateway_url_from_bind_line(
        "CanonSim Workbench — loopback gateway http://127.0.0.1:8765/op"
    ) == "http://127.0.0.1:8765"
    assert _gateway_url_from_bind_line(
        "CanonSim Workbench — loopback gateway http://127.0.0.1:8765"
    ) == "http://127.0.0.1:8765"
    assert _gateway_url_from_bind_line(
        "CanonSim Workbench — loopback gateway http://127.0.0.1:9000/"
    ) == "http://127.0.0.1:9000"
    assert _gateway_url_from_bind_line("anything else") is None


def test_the_forwarded_root_serves_the_clients_route() -> None:
    """KI#98's end-to-end pin: the REAL gateway process's own bind
    line (the banner workbench_app prints — transport.url, route
    INCLUDED), parsed by the launcher's parse, must SERVE the route
    the clients dial (the Vite proxy forwards to the root; the web
    client's gateway adapter appends its own route). The iter-227
    forward shipped the endpoint as the base and every request
    landed on /op/op — HTTP 404, app.status dead. This pin kills the
    whole class: banner shape, route, or parse drift all go RED
    here."""
    port = _free_port()
    process = subprocess.Popen(
        [
            sys.executable,
            "-u",
            str(REPO / "scripts" / "workbench_app.py"),
            "--no-backend",
            "--port",
            str(port),
        ],
        cwd=str(REPO),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env={
            key: value
            for key, value in os.environ.items()
            if key != "PYTHONUNBUFFERED"
        },
    )
    banner = ""
    deadline = time.monotonic() + 60.0
    try:
        assert process.stdout is not None
        while time.monotonic() < deadline:
            line = process.stdout.readline()
            if not line:
                break
            if "loopback gateway http://" in line:
                banner = line.rstrip("\n")
                break
        assert banner, "the gateway never printed its bind line"
        root = _gateway_url_from_bind_line(banner)
        assert root is not None, f"the parse refused the real banner: {banner!r}"
        assert not root.endswith("/op"), (
            "the forwarded value is the ROOT — a route inside it "
            "doubles under the client's own /op append"
        )
        request = urllib.request.Request(
            root + "/op",
            data=json.dumps(
                {"operation": "app.status", "arguments": {}}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=10) as handle:
            document = json.loads(handle.read().decode("utf-8"))
        assert document.get("status") == "OK", document
    finally:
        process.send_signal(signal.SIGINT)
        try:
            process.wait(timeout=15.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10.0)


# ------------------------------------------------- 5. the CLI forms


def test_the_no_frontend_flag_parses() -> None:
    args = parse_args(["--no-frontend"])
    assert args.no_frontend is True
    assert args.gateway_args == []


def test_the_bare_separator_is_stripped_for_the_gateway() -> None:
    """The operator's `-- --port 9000` form: the separator is OURS —
    workbench_app's parser has no positional args, a bare "--" is
    its own loud refusal (the latent wb-9 bug, fixed with wb-10)."""
    args = parse_args(["--", "--port", "9000"])
    assert args.gateway_args == ["--port", "9000"]
    assert args.no_frontend is False
