"""iter-106 acceptance — the resume door (`--resume <log>`, D-139):
**resume is invisible to the log.** A session interrupted at a clean
drain boundary and resumed with the same remaining steps produces
byte-identical bytes to the uninterrupted run — interruption is not an
input, only steps are (T1 extended across process boundaries; pinned
here at every split point, directors on and off).

The cursor (`core/cursor.py`) carries the run's entropy position —
the silent draws no fold can recover (urgency misses, weather
self-rolls, faction goal failures); the checkpoint fast-path
(`core/checkpoint.py`'s first RUNTIME consumer, fed by the operator's
`scripts/checkpoint.py` artifacts) restores the projection as snapshot
+ tail. Loud refusals: a missing or stale cursor, a foreign pack, an
env-pin mismatch, present-but-wrong checkpoints.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

import pytest

from cli.main import main
from core.checkpoint import (
    CheckpointIndex,
    save_checkpoint,
    write_index,
)
from core.cursor import CursorError, cursor_path, load_cursor, save_cursor
from core.director import Director, policy_from_rules
from core.log import read_log
from core.loop import RunnerError, Simulator
from core.pack import load_pack
from core.rng import RngBank, RngError, urgency_stream_name

REPO = Path(__file__).resolve().parents[1]
TAVERN_DIR = REPO / "content" / "tavern_pack"
PACK = load_pack(TAVERN_DIR)
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

# move + steal seeds suspicion and director hooks; wait 760 crosses two
# beats and a watch rotation — the silent urgency/faction/weather draws
# (the entropy no fold recovers) fire across the split; the armed
# worldgen pack exercises the generate_world re-derivation at resume.
STEPS: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "wait", "ticks": 760},
    {"intent": "move", "target": "loc_backyard"},
]


def _uninterrupted(tmp_path: Path, *, directors: bool = True) -> bytes:
    """The counterfactual: the same steps fed in one process, one log."""
    log = tmp_path / "whole.jsonl"
    sim = Simulator(PACK, 42, log, SCHEMA, commit="0000000",
                    director_enabled=directors)
    sim.run_playscript({
        "name": "whole", "seed": 42, "pack": PACK.name_version,
        "steps": [dict(step) for step in STEPS],
    })
    return log.read_bytes()


def _resumed(tmp_path: Path, split: int, *, directors: bool = True) -> bytes:
    """The interrupted twin: steps[:split], close, cursor, resume, rest."""
    log = tmp_path / f"split_{split}.jsonl"
    sim = Simulator(PACK, 42, log, SCHEMA, commit="0000000",
                    director_enabled=directors)
    sim.open()
    if split:
        sim.run_steps([dict(step) for step in STEPS[:split]])
    cursor = sim.export_cursor(director_enabled=directors)
    sim.close()
    save_cursor(cursor_path(log), cursor)
    sim2 = Simulator.resume(PACK, log, SCHEMA, load_cursor(cursor_path(log)))
    sim2.run_steps([dict(step) for step in STEPS[split:]])
    sim2.close()
    return log.read_bytes()


# -- the law: resume is invisible to the log -----------------------------------


@pytest.mark.parametrize("split", [0, 1, 2, 3])
def test_resume_is_invisible_to_the_log(tmp_path: Path, split: int) -> None:
    """The law itself (D-139): byte-identical to the uninterrupted run
    at every split point — split 0 resumes right after open (the
    genesis events + the rebuilt WorldModel), split 2 runs the whole
    beat/rotation cadence in the RESUMED process (the silent draws the
    cursor exists for)."""
    assert _resumed(tmp_path, split) == _uninterrupted(tmp_path)


@pytest.mark.parametrize("split", [1, 3])
def test_resume_restores_the_director_policy(tmp_path: Path, split: int) -> None:
    """The cursor carries the live policy flag: a directors-off run
    resumed is byte-identical to the uninterrupted directors-off run
    (the T8 baseline arm survives the process boundary)."""
    assert (
        _resumed(tmp_path, split, directors=False)
        == _uninterrupted(tmp_path, directors=False)
    )


def test_export_cursor_refuses_mid_drain(tmp_path: Path) -> None:
    """The drain-boundary law has teeth: a queue holding pending entries
    (simulated by pushing one directly) refuses the export loudly."""
    sim = Simulator(PACK, 42, tmp_path / "run.jsonl", SCHEMA, commit="0000000")
    sim._queue.push(tick=99, sub_order=300, actor_id="pc_01",
                    kind="completion", payload=None)
    with pytest.raises(RunnerError):
        sim.export_cursor(director_enabled=True)


# -- the cursor artifact -------------------------------------------------------


def test_cursor_envelope_is_closed(tmp_path: Path) -> None:
    """Save and load both enforce the exact key set — a field that must
    not appear cannot appear (the header's own law)."""
    with pytest.raises(CursorError):
        save_cursor(tmp_path / "c.json", {"seed": 1})  # missing keys: loud
    hand = tmp_path / "hand.json"
    hand.write_text('{"bogus": 1}\n', encoding="utf-8")
    with pytest.raises(CursorError):
        load_cursor(hand)


def test_rng_export_restore_roundtrip() -> None:
    """The bank's positions carry: after restore, a fresh bank's next
    draws match the original's (the entropy state, not the seed, is
    what the cursor preserves)."""
    bank = RngBank(42)
    bank.randint(1, 100)
    bank.random()
    with bank.assure(urgency_stream_name("npc_probe", "coerce")):
        bank.randint(1, 100)  # one urgency-family draw (a silent roll)
    payload = bank.export_state()

    twin = RngBank(42)
    twin.restore_state(payload)
    assert twin.count("substantive") == 2  # the counts carried too
    assert twin.randint(1, 100) == bank.randint(1, 100)
    with bank.assure(urgency_stream_name("npc_probe", "coerce")):
        bank_next = bank.randint(1, 100)
    with twin.assure(urgency_stream_name("npc_probe", "coerce")):
        twin_next = twin.randint(1, 100)
    assert twin_next == bank_next  # same stream, same position: the next draw
    # the worldgen family never exports (genesis-scoped, re-derived)
    assert all(not name.startswith("worldgen:") for name in payload["streams"])


def test_rng_restore_refuses_worldgen_streams() -> None:
    """A cursor claiming worldgen positions is refused loudly — those
    streams re-derive at resume; restoring them would drift silently."""
    bank = RngBank(42)
    payload = bank.export_state()
    smuggled = {
        "streams": dict(payload["streams"], **{"worldgen:height": [3, [0], None]}),
        "counts": dict(payload["counts"], **{"worldgen:height": 0}),
    }
    with pytest.raises(RngError):
        bank.restore_state(smuggled)


def test_director_restore_refuses_drift() -> None:
    """The run marks validate against the pack's own declarations: a
    pacing shape the pack does not declare, and release indices the
    rebuilt buffer cannot hold, are loud (a stale or foreign cursor)."""
    director = Director(pack=PACK, policy=policy_from_rules(PACK.rules, True))
    state = director.export_run_state()
    with pytest.raises(ValueError):  # pacing dropped: pack declares one
        director.restore_run_state(dict(state, pacing=None))
    with pytest.raises(ValueError):  # index beyond the (empty) buffer
        director.restore_run_state(dict(state, released=[99]))
    with pytest.raises(ValueError):  # unknown clock band
        director.restore_run_state(dict(
            state, pacing={"state": "LOUD", "beats_in_state": 1},
        ))


# -- the CLI surface ------------------------------------------------------------


def feed(monkeypatch: pytest.MonkeyPatch, commands: list[str]) -> None:
    answers = iter(commands)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))


def test_session_resume_flag_continues_the_log(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`--resume` through the real session loop: the cursor is pinned
    after every command, the resumed session appends in place, and the
    final log is byte-identical to the one-shot session with the same
    commands (the CLI-level law)."""
    whole_logs = tmp_path / "whole"
    feed(monkeypatch, ["look", "wait 30", "wait 30", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(whole_logs)]) == 0
    whole = sorted(whole_logs.glob("run_42_*.jsonl"))[0].read_bytes()

    part_logs = tmp_path / "part"
    feed(monkeypatch, ["look", "wait 30", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(part_logs)]) == 0
    log = sorted(part_logs.glob("run_42_*.jsonl"))[0]
    assert cursor_path(log).is_file()  # pinned at the drain
    feed(monkeypatch, ["wait 30", "quit"])
    assert main(["--resume", str(log), "--logs-dir", str(part_logs)]) == 0
    out = capsys.readouterr().out
    assert "resumed seed 42" in out
    assert log.read_bytes() == whole


def test_session_resume_without_cursor_refuses_loud(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A log without its cursor refuses loudly (exit 1, stderr names the
    artifact) — the entropy position is not rebuildable from the log,
    and a silent fresh-stream resume would be save-scumming."""
    logs = tmp_path / "logs"
    feed(monkeypatch, ["wait 3", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(logs)]) == 0
    capsys.readouterr()
    log = sorted(logs.glob("run_42_*.jsonl"))[0]
    before = log.read_bytes()
    cursor_path(log).unlink()  # the operator deleted it
    feed(monkeypatch, ["wait 3", "quit"])
    assert main(["--resume", str(log), "--logs-dir", str(logs)]) == 1
    assert "cursor" in capsys.readouterr().err
    assert log.read_bytes() == before  # untouched: nothing appended


def test_session_resume_stale_cursor_refuses_loud(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A cursor the log outgrew refuses loudly: event_count + the prefix
    digest bind the pin to the exact bytes (a mid-drain crash or a
    rolled-back cursor is a lie about entropy, never a guess)."""
    logs = tmp_path / "logs"
    feed(monkeypatch, ["wait 3", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(logs)]) == 0
    log = sorted(logs.glob("run_42_*.jsonl"))[0]
    stale = cursor_path(log).read_bytes()  # the early pin
    feed(monkeypatch, ["wait 30", "quit"])  # resume + continue: log grows
    assert main(["--resume", str(log), "--logs-dir", str(logs)]) == 0
    capsys.readouterr()
    cursor_path(log).write_bytes(stale)  # roll the pin back
    feed(monkeypatch, ["wait 3", "quit"])
    assert main(["--resume", str(log), "--logs-dir", str(logs)]) == 1
    assert "stale cursor" in capsys.readouterr().err


def test_session_resume_wrong_pack_refuses_loud(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A version-bumped pack twin refuses: the initial projection (and
    the whole fold) would be a lie — the checkpoint index's own law,
    applied at the resume door."""
    pack2 = tmp_path / "pack2"
    shutil.copytree(TAVERN_DIR, pack2)
    rules = json.loads((pack2 / "rules.json").read_text(encoding="utf-8"))
    rules["meta"]["version"] = "0.2"
    (pack2 / "rules.json").write_text(json.dumps(rules), encoding="utf-8")

    logs = tmp_path / "logs"
    feed(monkeypatch, ["wait 3", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(logs)]) == 0
    capsys.readouterr()
    log = sorted(logs.glob("run_42_*.jsonl"))[0]
    feed(monkeypatch, ["wait 3", "quit"])
    assert main(["--resume", str(log), "--pack", str(pack2),
                 "--logs-dir", str(logs)]) == 1
    assert "pack" in capsys.readouterr().err


def test_session_resume_env_pin_refuses_loud(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A log written under a different Python refuses at the writer's
    own door: the byte-identical guarantee is same-environment only
    (T1's law, the header's env pin)."""
    logs = tmp_path / "logs"
    feed(monkeypatch, ["wait 3", "quit"])
    assert main(["--seed", "42", "--logs-dir", str(logs)]) == 0
    capsys.readouterr()
    log = sorted(logs.glob("run_42_*.jsonl"))[0]
    lines = log.read_text(encoding="utf-8").splitlines()
    header = json.loads(lines[0])
    header["python"] = "9.9.9"
    lines[0] = json.dumps(header)
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    feed(monkeypatch, ["wait 3", "quit"])
    assert main(["--resume", str(log), "--logs-dir", str(logs)]) == 1
    assert "env pin" in capsys.readouterr().err


def test_resume_flag_with_a_subcommand_is_an_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    """--resume is a session flag: pairing it with a batch subcommand
    refuses loudly instead of being silently ignored."""
    assert main(["--resume", str(tmp_path / "log.jsonl"), "chronicle",
                 str(tmp_path / "x.jsonl")]) == 1
    assert "session flag" in capsys.readouterr().err


# -- the checkpoint fast-path ---------------------------------------------------


def _operator_checkpoints(log: Path, out_dir: Path) -> None:
    """The operator's artifacts, exactly as `scripts/checkpoint.py`
    builds them: verified snapshots + the anchored index."""
    sys.path.insert(0, str(REPO / "scripts"))
    try:
        import checkpoint as checkpoint_cli  # type: ignore[import-not-found]  # noqa: E402
        header, events = read_log(log, SCHEMA)
        checkpoints = checkpoint_cli.build_checkpoints(
            PACK, header, events, offsets=[0, 1]
        )
        records = [
            save_checkpoint(cp, out_dir, checkpoint_cli.prefix_digest(log, cp.offset))
            for cp in checkpoints
        ]
        write_index(
            CheckpointIndex(log=log.name, pack=PACK.name_version,
                            records=tuple(records)),
            out_dir,
        )
    finally:
        sys.path.remove(str(REPO / "scripts"))


def test_resume_via_checkpoints_fast_path(tmp_path: Path) -> None:
    """The checkpoint module's first runtime consumer: with the
    operator's artifacts present, the projection restores as snapshot +
    tail replay — and the resumed log is still byte-identical to the
    uninterrupted run (fold path and checkpoint path answer the same
    state, the re-fold law)."""
    log = tmp_path / "cp.jsonl"
    sim = Simulator(PACK, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([dict(step) for step in STEPS[:2]])
    cursor = sim.export_cursor(director_enabled=True)
    sim.close()
    save_cursor(cursor_path(log), cursor)
    out_dir = tmp_path / "checkpoints" / log.stem
    _operator_checkpoints(log, out_dir)

    sim2 = Simulator.resume(PACK, log, SCHEMA, load_cursor(cursor_path(log)),
                            checkpoints_dir=out_dir)
    sim2.run_steps([dict(step) for step in STEPS[2:]])
    sim2.close()
    assert log.read_bytes() == _uninterrupted(tmp_path)


def test_resume_corrupt_checkpoint_refuses_loud(tmp_path: Path) -> None:
    """Present-but-wrong is loud (the anchors have teeth): a flipped
    byte in the latest artifact fails the sha256 anchor at load."""
    log = tmp_path / "cp.jsonl"
    sim = Simulator(PACK, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([dict(step) for step in STEPS[:2]])
    cursor = sim.export_cursor(director_enabled=True)
    sim.close()
    save_cursor(cursor_path(log), cursor)
    out_dir = tmp_path / "checkpoints" / log.stem
    _operator_checkpoints(log, out_dir)
    artifact = out_dir / "checkpoint_000001.json"  # the latest record's
    artifact.write_bytes(artifact.read_bytes()[:-2] + b"} ")  # one byte bent

    from core.checkpoint import CheckpointError

    with pytest.raises(CheckpointError):
        Simulator.resume(PACK, log, SCHEMA, load_cursor(cursor_path(log)),
                         checkpoints_dir=out_dir)
