"""iter-5 acceptance — the CLI (`MVP_SCOPE.md` §12 owns the command
list): batch `play` / `chronicle` / `state` / `replay` plus the
interactive session (`look`, `wait N`, `directors on|off`, `seed`).

The session is one opened Simulator fed through `run_steps` — the same
front door as a playscript, one continuous deterministic log. The
`directors on|off` wiring is iter-5's deliverable (the T8 A/B RUN
itself lands at iter-6); here it is proven live: a script that seeds
and releases a hook produces a director intent with the flag on and
none with it off, same seed, same steps.

iter-105 (cli-pack): the `--pack` flag — every pack-loading command
and the session take it; the tavern default runs byte-identically
(explicit flag = no-flag run), a bad path refuses loudly before any
world opens. The stoplist docstring's "the CLI takes the pack dir as
config" claim is TRUE from here.
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
TAVERN_DIR = REPO / "content" / "tavern_pack"
PACK = load_pack(TAVERN_DIR)
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
    # steps[:2] = move + steal: the story-critical events render at the
    # tune-1 medium gate (a move-only script now prints an empty chronicle
    # — nothing tale-worthy happened, honestly).
    script = write_script(tmp_path, dict(AB_SCRIPT, steps=AB_SCRIPT["steps"][:2]))
    logs, out = tmp_path / "logs", tmp_path / "out"
    code = main(["play", str(script), "--logs-dir", str(logs), "--out-dir", str(out)])
    assert code == 0
    captured = capsys.readouterr().out
    assert "— Day 1, Morning —" in captured
    assert "the player's hand drifts toward Doren's purse" in captured
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


# -- the --pack flag (iter-105, cli-pack) ---------------------------------------


def test_pack_flag_tavern_default_is_byte_identical(tmp_path: Path) -> None:
    """`--pack` naming the committed tavern pack equals the no-flag run
    byte-for-byte: the flag is periphery plumbing, the tavern default IS
    the flag's default — zero canon price, no fixture regen."""
    script = write_script(tmp_path, dict(AB_SCRIPT, steps=AB_SCRIPT["steps"][:2]))
    logs, out = tmp_path / "logs", tmp_path / "out"
    assert main(["play", str(script),
                 "--logs-dir", str(logs), "--out-dir", str(out)]) == 0
    assert main(["play", str(script), "--pack", str(TAVERN_DIR),
                 "--logs-dir", str(logs), "--out-dir", str(out)]) == 0
    first, second = sorted(logs.glob("run_32_*.jsonl"))
    assert first.read_bytes() == second.read_bytes()


def test_pack_flag_bad_path_refuses_loud(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A bad --pack path refuses loudly BEFORE any world opens — batch,
    session, and the flag named BEFORE the subcommand (the subparser's
    SUPPRESS does not clobber the top-level value) all exit 1 naming the
    path; no log file is born."""
    script = write_script(
        tmp_path, dict(AB_SCRIPT, steps=[{"intent": "wait", "ticks": 3}])
    )
    bad = tmp_path / "no_such_pack"
    assert main(["play", str(script), "--pack", str(bad),
                 "--logs-dir", str(tmp_path), "--out-dir", str(tmp_path)]) == 1
    err = capsys.readouterr().err
    assert "pack dir not found" in err and str(bad) in err
    assert not list(tmp_path.glob("run_*.jsonl"))  # nothing opened

    assert main(["--pack", str(bad), "play", str(script),
                 "--logs-dir", str(tmp_path), "--out-dir", str(tmp_path)]) == 1
    assert "pack dir not found" in capsys.readouterr().err

    assert main(["--pack", str(bad), "--seed", "42",
                 "--logs-dir", str(tmp_path / "logs")]) == 1
    assert "pack dir not found" in capsys.readouterr().err


def test_pack_flag_on_the_read_side_subcommands(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The read-side subcommands take the flag too: `chronicle --pack`
    renders exactly the renderer's output, `state --pack` answers — and
    a directory that exists but is NOT a pack still refuses loudly
    (load_pack's own lint, the same exit 1)."""
    script = write_script(tmp_path, AB_SCRIPT)
    logs = tmp_path / "logs"
    main(["play", str(script), "--logs-dir", str(logs),
          "--out-dir", str(tmp_path)])
    capsys.readouterr()
    log = sorted(logs.glob("run_32_*.jsonl"))[0]

    assert main(["chronicle", str(log), "--pack", str(TAVERN_DIR)]) == 0
    from render.chronicle import chronicle_from_log

    assert capsys.readouterr().out == chronicle_from_log(log, PACK, SCHEMA)
    assert main(["state", "npc_guard_01", str(log), "--pack", str(TAVERN_DIR)]) == 0
    assert "Doren (npc_guard_01)" in capsys.readouterr().out
    assert main(["replay", str(log), "--pack", str(tmp_path)]) == 1
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
    # tune-1: look/wait are world texture — below the tale gate, so the
    # delta print stays silent (no chronicle lines); the SCENE CARD is the
    # command's observable answer, and the session mechanics still run.
    assert "the street in front of the tavern: no one" in out  # scene card
    assert "the player waits." not in out  # gated noise, not rendered
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
    # A story-bearing script (session seed 42): the clean steal is
    # story-critical (tune-1), so its line renders in BOTH the post-play
    # delta print and the full `chronicle` — the prefix-stability law the
    # waits used to pin before the gate rose.
    story = write_script(tmp_path, {
        "name": "session_story", "seed": 42, "pack": "tavern_pack@0.1",
        "steps": [
            {"intent": "move", "target": "loc_tavern"},
            {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        ],
    })
    feed(monkeypatch, ["directors off", f"play {story}", "chronicle", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    out = capsys.readouterr().out
    assert "director releases OFF" in out
    assert out.count("the player lifts the purse unseen.") == 2  # delta + full


def test_session_play_with_wrong_seed_is_an_error_not_a_crash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    script = write_script(tmp_path, dict(AB_SCRIPT, seed=999))
    feed(monkeypatch, [f"play {script}", "look", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    out = capsys.readouterr().out
    assert "error: playscript seed 999 != session seed 42" in out
    # the session survives the error: the next command still answers
    # (its scene card — the wait line itself is below the tune-1 gate)
    assert "the street in front of the tavern: no one" in out


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


# -- the mediator beat cycle (iter-12, agent-in-the-loop) ------------------------


def test_session_narrate_emits_and_applies_a_reply(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The narrator door drives one full beat: `narrate` emits the call
    (brief + protocol), `narrate <reply>` runs the cycle — a reply with
    supported claims is accepted and its verdict summary prints (KI#44);
    a malformed one degrades (regen), never crashes."""
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    reply = tmp_path / "mediator" / "reply_0000.json"
    reply.parent.mkdir(parents=True)
    reply.write_text(json.dumps({
        "prose": "The common room was warm.",
        "proposal": {
            "expected_event_seq": 1,
            "claims": [{"kind": "state", "entity": "pc_01",
                        "prop": "position", "value": "loc_street"}],
        },
    }), "utf-8")
    bad = tmp_path / "mediator" / "reply_0001.json"
    bad.write_text(json.dumps({"prose": "x", "bogus": 1}), "utf-8")
    feed(monkeypatch, [
        "look",
        "narrate", f"narrate {reply}",
        "narrate", f"narrate {bad}", "narrate dry",
        "quit",
    ])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    out = capsys.readouterr().out
    call = tmp_path / "mediator" / "call_0000.md"
    assert call.exists() and "## narrator_protocol" in call.read_text("utf-8")
    assert "The common room was warm." in out  # the accepted prose
    assert "BEAT claims: 1 supported" in out  # KI#44: the verdict summary
    assert "refused — regen 1/2" in out  # malformed → the ladder, no crash
    assert "[dry beat — the L12 floor" in out


def test_session_narrate_without_a_beat_is_an_error_not_a_crash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("cli.main.OUTPUT_DIR", tmp_path)
    feed(monkeypatch, [f"narrate {tmp_path / 'nope.json'}", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(tmp_path / "logs")]) == 0
    assert "no open narrator beat" in capsys.readouterr().out

