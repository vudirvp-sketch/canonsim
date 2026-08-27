"""iter-5 acceptance — the CLI (`MVP_SCOPE.md` §12 owns the command
list): batch `play` / `chronicle` / `state` / `replay` plus the
interactive session (`look`, `wait N`, `directors on|off`, `seed`).

The session is one opened Simulator fed through `run_steps` — the same
front door as a playscript, one continuous deterministic log. The
`directors on|off` wiring is iter-5's deliverable (the T8 A/B RUN
itself lands at iter-6); here it is proven live: a script that seeds
and releases a hook produces a director intent with the flag on and
none with it off, same seed, same steps.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from cli.main import main
from core.log import read_log
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

# seed 32 + two failed steals stack Doren's suspicion past the
# document-check trigger: the director releases ON-run only (probed)
AB_SCRIPT: dict[str, Any] = {
    "name": "director_ab",
    "seed": 32,
    "pack": "tavern_pack@0.1",
    "steps": [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "wait", "ticks": 760},
    ],
}


def write_script(tmp_path: Path, script: dict[str, Any]) -> Path:
    path = tmp_path / f"{script['name']}.json"
    path.write_text(json.dumps(script), encoding="utf-8")
    return path


def director_intents(log_path: Path) -> list[str]:
    _, events = read_log(log_path, SCHEMA)
    return [
        str(e.provenance["cause_intent"])
        for e in events
        if str(e.provenance.get("cause_intent", "")).startswith("director_")
    ]


# -- batch subcommands ---------------------------------------------------------


def test_play_prints_chronicle_scene_and_writes_files(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = write_script(tmp_path, dict(AB_SCRIPT, steps=AB_SCRIPT["steps"][:1]))
    logs, out = tmp_path / "logs", tmp_path / "out"
    code = main(["play", str(script), "--logs-dir", str(logs), "--out-dir", str(out)])
    assert code == 0
    captured = capsys.readouterr().out
    assert "— Day 1, Morning —" in captured
    assert "the player heads to Three Barrels tavern." in captured
    assert "Three Barrels tavern:" in captured  # the scene card
    assert "[log:" in captured
    log_files = list(logs.glob("run_32_*.jsonl"))
    assert len(log_files) == 1
    assert list(out.glob("chronicle_run_32_*.txt"))  # the chronicle file


def test_play_directors_flag_wires_the_release_gate(tmp_path: Path) -> None:
    """`--directors on|off` is the T8 switch: same seed + steps, the
    hook releases only when the director is on (buffer seeds either way)."""
    script = write_script(tmp_path, AB_SCRIPT)
    logs = tmp_path / "logs"
    assert main([
        "play", str(script), "--directors", "on",
        "--logs-dir", str(logs), "--out-dir", str(tmp_path / "out"),
    ]) == 0
    assert main([
        "play", str(script), "--directors", "off",
        "--logs-dir", str(logs), "--out-dir", str(tmp_path / "out"),
    ]) == 0
    on_log, off_log = sorted(logs.glob("run_32_*.jsonl"))
    assert director_intents(on_log) == ["director_0000"]
    assert director_intents(off_log) == []
    assert on_log.read_bytes() != off_log.read_bytes()


def test_play_seed_override(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    script = write_script(tmp_path, dict(AB_SCRIPT, steps=[{"intent": "wait", "ticks": 3}]))
    logs = tmp_path / "logs"
    assert main(["play", str(script), "--seed", "77",
                 "--logs-dir", str(logs), "--out-dir", str(tmp_path)]) == 0
    assert list(logs.glob("run_77_*.jsonl"))  # the override named the log


def test_play_missing_script_fails_loud(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["play", str(tmp_path / "nope.json"),
                 "--logs-dir", str(tmp_path), "--out-dir", str(tmp_path)]) == 1
    assert "error" in capsys.readouterr().err


def test_chronicle_command_matches_the_renderer(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = write_script(tmp_path, AB_SCRIPT)
    logs = tmp_path / "logs"
    main(["play", str(script), "--logs-dir", str(logs),
          "--out-dir", str(tmp_path)])
    capsys.readouterr()
    log = sorted(logs.glob("run_32_*.jsonl"))[0]
    assert main(["chronicle", str(log)]) == 0
    from render.chronicle import chronicle_from_log

    assert capsys.readouterr().out == chronicle_from_log(log, PACK, SCHEMA)


def test_state_command_prints_entity_history(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = write_script(tmp_path, AB_SCRIPT)
    logs = tmp_path / "logs"
    main(["play", str(script), "--logs-dir", str(logs),
          "--out-dir", str(tmp_path)])
    capsys.readouterr()
    log = sorted(logs.glob("run_32_*.jsonl"))[0]
    assert main(["state", "npc_guard_01", str(log)]) == 0
    out = capsys.readouterr().out
    assert out.startswith("Doren (npc_guard_01)")
    assert "history:" in out
    assert "grows warier of the player" in out


def test_replay_command_reports_the_fold(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = write_script(tmp_path, AB_SCRIPT)
    logs = tmp_path / "logs"
    main(["play", str(script), "--logs-dir", str(logs),
          "--out-dir", str(tmp_path)])
    capsys.readouterr()
    log = sorted(logs.glob("run_32_*.jsonl"))[0]
    assert main(["replay", str(log)]) == 0
    out = capsys.readouterr().out
    assert "events" in out and "fold OK" in out


def test_replay_command_rejects_a_desynced_log(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = write_script(tmp_path, AB_SCRIPT)
    logs = tmp_path / "logs"
    main(["play", str(script), "--logs-dir", str(logs),
          "--out-dir", str(tmp_path)])
    log = sorted(logs.glob("run_32_*.jsonl"))[0]
    lines = log.read_text(encoding="utf-8").splitlines()
    event = json.loads(lines[1])
    event["state_changes"] = [{  # a delta the projection cannot replay
        "entity": "pc_01", "prop": "position",
        "from": "loc_moon", "to": "loc_tavern", "irreversible": False,
    }]
    lines[1] = json.dumps(event)
    broken = tmp_path / "broken.jsonl"
    broken.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert main(["replay", str(broken)]) == 1
    assert "error" in capsys.readouterr().err


# -- the interactive session ----------------------------------------------------


def feed(monkeypatch: pytest.MonkeyPatch, commands: list[str]) -> None:
    answers = iter(commands)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))


def test_session_look_wait_seed_quit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    feed(monkeypatch, ["look", "wait 30", "seed", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    out = capsys.readouterr().out
    assert "— Day 1, Morning —" in out
    assert "the player takes in the street in front of the tavern." in out
    assert "the player waits." in out
    assert "the street in front of the tavern: no one" in out  # scene card
    assert "session seed: 42" in out
    assert list((tmp_path / "logs").glob("run_42_*.jsonl"))


def test_session_seed_restarts_a_new_log(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    feed(monkeypatch, ["wait 3", "seed 7", "wait 3", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    logs = tmp_path / "logs"
    assert list(logs.glob("run_42_*.jsonl"))
    assert list(logs.glob("run_7_*.jsonl"))  # a restart is a NEW log (INV-5)
    out = capsys.readouterr().out
    assert "new run: seed 7" in out


def test_session_directors_toggle_and_chronicle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    feed(monkeypatch, ["directors off", "wait 3", "chronicle", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    out = capsys.readouterr().out
    assert "director releases OFF" in out
    assert out.count("the player waits.") == 2  # delta print + full chronicle


def test_session_play_with_wrong_seed_is_an_error_not_a_crash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    script = write_script(tmp_path, dict(AB_SCRIPT, seed=999))
    feed(monkeypatch, [f"play {script}", "wait 3", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    out = capsys.readouterr().out
    assert "error: playscript seed 999 != session seed 42" in out
    assert "the player waits." in out  # the session survives the error


def test_session_unknown_command_suggests_help(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    feed(monkeypatch, ["dance", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    assert "unknown command 'dance'" in capsys.readouterr().out


def test_session_equals_batch_log_bytes(tmp_path: Path) -> None:
    """The session's step-by-step feed and a batch run of the same steps
    produce byte-identical logs (T1 extends to session mode)."""
    from core.loop import Simulator

    steps = [{"intent": "move", "target": "loc_tavern"},
             {"intent": "wait", "ticks": 30},
             {"intent": "move", "target": "loc_backyard"}]
    script = {"name": "s", "seed": 42, "pack": "tavern_pack@0.1", "steps": steps}
    batch_log = tmp_path / "batch.jsonl"
    sim = Simulator(PACK, 42, batch_log, SCHEMA, commit="0000000")
    sim.run_playscript(script)

    session_log = tmp_path / "session.jsonl"
    sim2 = Simulator(PACK, 42, session_log, SCHEMA, commit="0000000")
    sim2.open()
    for step in steps:
        sim2.run_steps([step])
    sim2.close()
    assert batch_log.read_bytes() == session_log.read_bytes()
