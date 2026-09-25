"""wb-10's claim packet — the zero-command launcher
(`scripts/workbench_launch.py`, the owner's 2026-09-25 fix list:
«редот у меня такой …\\Redot_v26.2-stable_windows_win64 … где найти
redot.exe и как его подключить?» + the reported TypeError + the
zero-command law).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE SPAWN ITSELF: the REAL launcher process starts the REAL
   gateway child, observes the bind line, and shuts both down on
   Ctrl+C — the owner-reported `Popen.__init__() got an unexpected
   keyword argument 'buffering'` crash is pinned dead forever (the
   spawn refuses before any bind without `bufsize`).
2. THE FOLDER RESOLUTION: a Redot RELEASE FOLDER resolves to the
   engine executable inside it (the owner's exact layout:
   Redot_v26.2-stable_windows_win64/ with
   redot.windows.editor.x86_64.exe) — root level AND one folder deep,
   the known names in preference order, the sorted-glob fallback.
3. THE CHAIN: the explicit forms pass verbatim (strict — the spawn's
   own loud error); the persisted pick falls through when stale.
4. THE AUTO-SCAN: a Redot folder on the Desktop-shaped roots is found
   with zero configuration (the owner's actual machine layout).
5. THE PERSISTED PICK: launcher.json saves atomically and loads back;
   a corrupt file is loud on the console but never a brick.
6. THE BIND-URL PARSE: the gateway's own bind line yields the URL the
   Redot child is told to dial (never a divergent default).
"""

from __future__ import annotations

import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from workbench_launch import (  # noqa: E402
    _gateway_url_from_bind_line,
    auto_discover_redot,
    common_scan_roots,
    load_launcher_settings,
    parse_args,
    redot_exe_in_folder,
    resolve_redot_path,
    save_launcher_settings,
)


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def _fake_release(root: Path, name: str = "Redot_v26.2-stable_windows_win64"):
    """The owner's actual layout: a Redot release folder on a desktop,
    the engine executable at its root (the exact binary name)."""
    folder = root / name
    folder.mkdir(parents=True)
    engine = folder / "redot.windows.editor.x86_64.exe"
    engine.write_bytes(b"#!/bin/sh\nexit 0\n")
    engine.chmod(0o755)
    return folder, engine


# ----------------------------------------------- 1. the spawn itself


def test_the_real_launcher_spawns_and_stops_the_gateway() -> None:
    """THE owner-reported crash, pinned dead: the launcher's gateway
    child (Popen with the line-buffered pipe) must CONSTRUCT and reach
    the bind line — `buffering` (not a Popen keyword) refused the
    spawn before anything served. Then SIGINT stops the session.
    KI#93: the whole chain must stream WITHOUT the host's
    PYTHONUNBUFFERED (CI and the owner's machines never set it — the
    sandbox's global PYTHONUNBUFFERED=1 masked three red CI
    iterations), so this spawn strips it: the launcher owns the
    buffering itself (the gateway child rides `-u`, the supervisor
    line-buffers its own stdout)."""
    port = _free_port()
    process = subprocess.Popen(
        [
            sys.executable,
            str(REPO / "scripts" / "workbench_launch.py"),
            "--no-redot",
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
            "no Redot executable resolved" in line for line in lines
        ), "the honest no-redot note (never a fake 'launched')"
        process.send_signal(signal.SIGINT)
        process.wait(timeout=30.0)
        assert process.returncode == 0, "\n".join(lines[-20:])
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=10.0)


# --------------------------------------- 2. the folder resolution


def test_a_release_folder_resolves_the_engine_executable(
    tmp_path: Path,
) -> None:
    """The owner's exact form: --redot-exe <the release FOLDER> finds
    redot.windows.editor.x86_64.exe inside it — never 'where is
    redot.exe?' again."""
    folder, engine = _fake_release(tmp_path)
    assert redot_exe_in_folder(folder) == engine
    assert resolve_redot_path(str(folder)) == str(engine)


def test_a_nested_release_folder_resolves_one_level_deep(
    tmp_path: Path,
) -> None:
    """A release unpacked into a subfolder (one level deep) resolves
    too — the deterministic sorted walk."""
    outer = tmp_path / "Redot_v26.2-stable_windows_win64"
    outer.mkdir()
    nested = outer / "unpacked"
    nested.mkdir()
    engine = nested / "redot.windows.editor.x86_64.exe"
    engine.write_bytes(b"engine")
    engine.chmod(0o755)
    assert redot_exe_in_folder(outer) == engine


def test_the_known_name_wins_over_the_sorted_glob(tmp_path: Path) -> None:
    """The preference order: the known engine names beat any other
    redot* executable the folder happens to carry."""
    folder = tmp_path / "Redot_folder"
    folder.mkdir()
    other = folder / "aaa-redot-tool.exe"
    other.write_bytes(b"tool")
    other.chmod(0o755)
    engine = folder / "redot.windows.editor.x86_64.exe"
    engine.write_bytes(b"engine")
    engine.chmod(0o755)
    assert redot_exe_in_folder(folder) == engine


def test_an_empty_folder_resolves_none(tmp_path: Path) -> None:
    """A folder with no Redot executable is the honest skip (loud on
    the console), never a guess."""
    empty = tmp_path / "empty"
    empty.mkdir()
    assert redot_exe_in_folder(empty) is None
    assert resolve_redot_path(str(empty)) is None


def test_the_strict_and_recovery_forms(tmp_path: Path) -> None:
    """An explicit .exe passes verbatim; the STRICT form (the CLI
    argument) passes a nonexistent path verbatim too (the spawn's own
    loud error); the non-strict form (the persisted pick) skips it."""
    engine = tmp_path / "redot.windows.editor.x86_64.exe"
    engine.write_bytes(b"engine")
    engine.chmod(0o755)
    assert resolve_redot_path(str(engine)) == str(engine)
    assert resolve_redot_path(
        "C:/nowhere/Redot.exe", strict=True
    ) == "C:/nowhere/Redot.exe"
    assert resolve_redot_path("C:/nowhere/Redot.exe") is None


# ------------------------------------------------- 3. the auto-scan


def test_the_auto_scan_finds_a_desktop_redot(tmp_path: Path) -> None:
    """The owner's machine layout, zero configuration: a Redot release
    folder inside a Desktop-shaped root is discovered; non-Redot
    folders and missing roots are skipped."""
    desktop = tmp_path / "Desktop"
    desktop.mkdir()
    _folder, engine = _fake_release(desktop)
    (desktop / "SomethingElse").mkdir()
    assert auto_discover_redot([desktop]) == str(engine)
    empty_root = tmp_path / "Other"
    empty_root.mkdir()
    assert auto_discover_redot([empty_root]) is None


def test_the_common_roots_skip_missing_children(tmp_path: Path) -> None:
    (tmp_path / "Desktop").mkdir()
    roots = common_scan_roots(tmp_path)
    assert roots == [tmp_path / "Desktop"]


# ------------------------------------------ 4. the persisted pick


def test_the_persisted_pick_roundtrips(tmp_path: Path) -> None:
    path = tmp_path / "launcher.json"
    save_launcher_settings("D:/Tools/Redot/redot.exe", path)
    assert load_launcher_settings(path) == {
        "redot_exe": "D:/Tools/Redot/redot.exe"
    }
    # the atomic write leaves no .tmp residue
    assert not path.with_suffix(".json.tmp").exists()


def test_a_corrupt_pick_is_loud_but_never_a_brick(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "launcher.json"
    path.write_text("{not json", encoding="utf-8")
    assert load_launcher_settings(path) == {}
    assert "unreadable" in capsys.readouterr().out
    path.write_text(json.dumps(["a", "list"]), encoding="utf-8")
    assert load_launcher_settings(path) == {}
    assert "not a JSON object" in capsys.readouterr().out


# ------------------------------------------ 5. the bind-line parse


def test_the_bind_line_yields_the_gateway_url() -> None:
    assert _gateway_url_from_bind_line(
        "CanonSim Workbench — loopback gateway http://127.0.0.1:8765"
    ) == "http://127.0.0.1:8765"
    assert _gateway_url_from_bind_line(
        "CanonSim Workbench — loopback gateway http://127.0.0.1:9000/"
    ) == "http://127.0.0.1:9000"
    assert _gateway_url_from_bind_line("anything else") is None


# ------------------------------------------------- 6. the CLI forms


def test_the_pick_redot_flag_parses() -> None:
    args = parse_args(["--pick-redot"])
    assert args.pick_redot is True
    assert args.no_redot is False
    quiet = parse_args(["--no-redot"])
    assert quiet.no_redot is True and quiet.pick_redot is False
