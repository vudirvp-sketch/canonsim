"""The play interface (`MVP_SCOPE.md` §12 owns the command list;
`docs/blueprint/phase0.md` §5): the "editor" layer of the four-layer
split — Python orchestration ON TOP of the JSONL log, never in the
canon path (the Wesnoth escape-valve precedent).

Batch subcommands (one process, one job):

    python -m cli play <playscript.json> [--seed N] [--directors on|off]
    python -m cli chronicle <log.jsonl>
    python -m cli state <entity> <log.jsonl>
    python -m cli replay <log.jsonl>

Interactive session (no subcommand) — `look` and `wait` are two of the
12 actions driven as single-step intents through the same front door as
playscript steps; `play` loads a script into the live session; `narrate`
drives the mediator beat cycle over an EXTERNAL narrator (the
agent-in-the-loop door, D-055 — the repo stays LLM-free):

    look · wait N · play <script> · narrate [<reply.json> | dry] ·
    chronicle · state <entity> · replay <log> · directors on|off ·
    seed [<n>] · help · quit

The session is one opened Simulator (`core/loop.py`): every command
feeds steps through `run_steps` and the world moves only through the
queue it seeds — the log is one continuous deterministic run. The
renderer is a pure function of the log (CHRON-1); `chronicle` re-renders
from the log file, so re-running a command on a longer log keeps every
earlier line identical.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from cli.mediator import BeatResult, Mediator, MediatorError
from core.director import policy_from_rules
from core.fold import fold, initial_projection
from core.log import LogError, next_log_path, read_log
from core.loop import RunnerError, Simulator, load_playscript
from core.pack import Pack, PackError, load_pack
from render.chronicle import (
    RenderError,
    chronicle_from_log,
    render_entity_view,
    render_scene_card,
    replay_report,
)
from render.tracery import GrammarError

REPO = Path(__file__).resolve().parents[1]
PACK_DIR = REPO / "content" / "tavern_pack"
SCHEMA_PATH = REPO / "schemas" / "event.schema.json"
LOGS_DIR = REPO / "logs"
OUTPUT_DIR = REPO / "output"

_SESSION_HELP = """commands:
  look              take in the scene (the look_around action)
  wait N            wait N ticks (the world moves: beats, rotations)
  play <script>     run a playscript's steps in this session
  narrate           emit the narrator call (output/mediator/call_NNNN.md)
  narrate <reply>   apply a narrator reply JSON {prose, texture_delta?,
                    proposal?} — the beat cycle runs
  narrate dry       close the beat without a narrator (template prose)
  chronicle         print the tale so far (re-rendered from the log)
  state <entity>    full history + current state of one entity
  replay <log>      validate + fold another log (T2), report
  directors on|off  toggle the director's releases (buffer keeps seeding)
  seed [<n>]        show the seed / restart the session with seed n
  help              this list
  quit              end the session (the log stays)"""


def _commit_id() -> str:
    """Short HEAD hash for the log header provenance; `unknown` offline."""
    try:
        return subprocess.run(  # noqa: S603 — fixed argv, no user input
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
            capture_output=True, text=True, timeout=5, check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def _load() -> tuple[Pack, dict]:
    pack = load_pack(PACK_DIR)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return pack, schema


def _session_log(pack: Pack, schema: dict, log_path: Path) -> str:
    """The chronicle rendered from the session log so far."""
    return chronicle_from_log(log_path, pack, schema)


class Session:
    """One interactive run: an opened Simulator fed step-by-step.

    The seed is bound at open (the log header is fixed); `seed <n>`
    closes the current log and starts a fresh run — committed logs are
    never edited (INV-5), a restart is a new log file.
    """

    def __init__(
        self,
        pack: Pack,
        schema: dict,
        seed: int,
        logs_dir: Path,
        director_enabled: bool,
    ) -> None:
        self._pack = pack
        self._schema = schema
        self._logs_dir = logs_dir
        self._directors_on = director_enabled
        self._shown_lines = 0  # chronicle lines already printed
        self._mediator: Mediator | None = None
        self._start(seed)

    def _start(self, seed: int) -> None:
        self._logs_dir.mkdir(parents=True, exist_ok=True)
        self._seed = seed
        self._log_path = next_log_path(self._logs_dir, seed)
        self._sim = Simulator(
            self._pack, seed, self._log_path, self._schema,
            commit=_commit_id(), director_enabled=self._directors_on,
        )
        self._sim.open()
        self._shown_lines = 0
        self._mediator = None  # the ledger dies with its session (D-049)

    @property
    def seed(self) -> int:
        return self._seed

    @property
    def log_path(self) -> Path:
        return self._log_path

    def close(self) -> None:
        self._sim.close()

    # -- command dispatch ----------------------------------------------------

    def execute(self, line: str) -> None:
        """Run one session command; user errors print, the session lives."""
        parts = line.split()
        command, args = parts[0].lower(), parts[1:]
        try:
            handler = {
                "help": self._cmd_help,
                "look": self._cmd_look,
                "wait": self._cmd_wait,
                "play": self._cmd_play,
                "chronicle": self._cmd_chronicle,
                "state": self._cmd_state,
                "replay": self._cmd_replay,
                "directors": self._cmd_directors,
                "seed": self._cmd_seed,
                "narrate": self._cmd_narrate,
            }[command]
        except KeyError:
            print(f"unknown command {command!r} — try 'help'")
            return
        try:
            handler(args)
        except (
            RunnerError, LogError, RenderError, GrammarError,
            MediatorError, ValueError,
        ) as exc:
            print(f"error: {exc}")
        except FileNotFoundError as exc:
            print(f"error: {exc}")

    def _cmd_help(self, args: list[str]) -> None:
        print(_SESSION_HELP)

    def _cmd_look(self, args: list[str]) -> None:
        self._run_steps([{"intent": "look_around"}])

    def _cmd_wait(self, args: list[str]) -> None:
        if len(args) != 1 or not args[0].isdigit():
            print("usage: wait N (N = tick count)")
            return
        self._run_steps([{"intent": "wait", "ticks": int(args[0])}])

    def _cmd_play(self, args: list[str]) -> None:
        if len(args) != 1:
            print("usage: play <playscript.json>")
            return
        script = load_playscript(Path(args[0]))
        if script["seed"] != self._seed:
            print(
                f"error: playscript seed {script['seed']} != session seed "
                f"{self._seed} (a session's seed is fixed at open — "
                f"'seed <n>' starts a new run)"
            )
            return
        if script["pack"] != self._pack.name_version:
            print(
                f"error: playscript pack {script['pack']!r} != loaded "
                f"{self._pack.name_version!r}"
            )
            return
        self._run_steps(list(script["steps"]))

    def _cmd_chronicle(self, args: list[str]) -> None:
        text = _session_log(self._pack, self._schema, self._log_path)
        self._shown_lines = len(text.splitlines())
        print(text, end="")

    def _cmd_state(self, args: list[str]) -> None:
        if len(args) != 1:
            print("usage: state <entity_id>")
            return
        _, events = read_log(self._log_path, self._schema)
        projection = fold(events, initial_projection(self._pack.entities))
        print(
            render_entity_view(
                events, projection, self._pack, args[0], seed=self._seed
            ),
            end="",
        )

    def _cmd_replay(self, args: list[str]) -> None:
        if len(args) != 1:
            print("usage: replay <log.jsonl>")
            return
        report, _ = replay_report(Path(args[0]), self._pack, self._schema)
        print(report)

    def _cmd_directors(self, args: list[str]) -> None:
        if args not in (["on"], ["off"]):
            print("usage: directors on|off")
            return
        self._directors_on = args[0] == "on"
        self._sim.director.policy = policy_from_rules(
            self._pack.rules, self._directors_on
        )
        print(
            f"director releases {'ON' if self._directors_on else 'OFF'} "
            f"(the buffer keeps seeding — D-005 hygiene)"
        )

    def _cmd_seed(self, args: list[str]) -> None:
        if not args:
            print(f"session seed: {self._seed} (log: {self._log_path})")
            return
        if len(args) != 1 or not args[0].lstrip("-").isdigit():
            print("usage: seed [<n>]")
            return
        new_seed = int(args[0])
        self._sim.close()
        self._start(new_seed)
        print(f"new run: seed {new_seed}, log {self._log_path}")

    # -- the mediator beat cycle (agent-in-the-loop, D-055) -------------------

    def _mediator_or_start(self) -> Mediator:
        if self._mediator is None:
            self._mediator = Mediator(
                self._sim, self._pack, self._schema, self._log_path,
                OUTPUT_DIR / "mediator",
            )
        return self._mediator

    def _cmd_narrate(self, args: list[str]) -> None:
        mediator = self._mediator_or_start()
        try:
            if not args:
                path = mediator.emit_call()
                reply = path.with_name(
                    path.stem.replace("call", "reply") + ".json"
                )
                print(f"[narrator call: {path}]")
                print(
                    f"[write a JSON reply {{prose, texture_delta?, proposal?}} "
                    f"at {reply}, then: narrate {reply}]"
                )
            elif args == ["dry"]:
                self._print_beat(mediator.dry_close())
            elif len(args) == 1:
                self._print_beat(mediator.apply_reply(Path(args[0])))
            else:
                print("usage: narrate [<reply.json> | dry]")
        finally:
            self._shown_lines = mediator.shown_lines

    @staticmethod
    def _print_beat(result: BeatResult) -> None:
        if result.status == "accepted":
            print(result.prose)
            return
        if result.status == "regen":
            print(
                f"[refused — regen {result.regens_used}/{result.max_regens}; "
                f"next call: {result.call_path}]"
            )
            for note in result.notes:
                print(f"  {note}")
            return
        print(result.prose)
        print(
            f"[dry beat — the L12 floor; regens used "
            f"{result.regens_used}/{result.max_regens}]"
        )

    # -- the world-touching path ---------------------------------------------

    def _run_steps(self, steps: list[dict]) -> None:
        """Feed steps, then show the fresh chronicle tail + scene card."""
        self._sim.run_steps(steps)
        text = _session_log(self._pack, self._schema, self._log_path)
        lines = text.splitlines()
        for line in lines[self._shown_lines :]:
            print(line)
        self._shown_lines = len(lines)
        header, events = read_log(self._log_path, self._schema)
        projection = fold(events, initial_projection(self._pack.entities))
        print(render_scene_card(projection, self._pack, seed=self._seed))


# -- batch subcommands -------------------------------------------------------


def cmd_play(args: argparse.Namespace) -> int:
    """Run a playscript end-to-end; print the chronicle + final scene."""
    pack, schema = _load()
    script = load_playscript(Path(args.script))
    if args.seed is not None:
        script = dict(script, seed=args.seed)
    logs_dir = Path(args.logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = next_log_path(logs_dir, script["seed"])
    sim = Simulator(
        pack, script["seed"], log_path, schema, commit=_commit_id(),
        director_enabled=args.directors != "off",
    )
    result = sim.run_playscript(script)
    text = chronicle_from_log(log_path, pack, schema)
    print(text, end="")
    _, events = read_log(log_path, schema)
    projection = fold(events, initial_projection(pack.entities))
    print(render_scene_card(projection, pack, seed=script["seed"]))
    print(f"[log: {log_path} | {result.event_count} events, tick {result.last_tick}]")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"chronicle_{log_path.stem}.txt"
    out_path.write_text(text, encoding="utf-8")
    print(f"[chronicle saved: {out_path}]")
    return 0


def cmd_chronicle(args: argparse.Namespace) -> int:
    """Render a log's chronicle (the seed comes from the log header)."""
    pack, schema = _load()
    print(chronicle_from_log(Path(args.log), pack, schema), end="")
    return 0


def cmd_state(args: argparse.Namespace) -> int:
    """One entity's full history + current state from a log."""
    pack, schema = _load()
    header, events = read_log(Path(args.log), schema)
    projection = fold(events, initial_projection(pack.entities))
    print(
        render_entity_view(
            events, projection, pack, args.entity, seed=int(header["seed"])
        ),
        end="",
    )
    return 0


def cmd_replay(args: argparse.Namespace) -> int:
    """Validate + fold a log (T0/T2 in one pass); report."""
    pack, schema = _load()
    report, _ = replay_report(Path(args.log), pack, schema)
    print(report)
    return 0


def run_session(args: argparse.Namespace) -> int:
    """The interactive session loop."""
    pack, schema = _load()
    session = Session(
        pack, schema, args.seed, Path(args.logs_dir), args.directors != "off"
    )
    print(
        f"canonsim — {pack.name_version} | seed {session.seed} | "
        f"log {session.log_path}\n"
        f"(the world moves when you act or wait — 'help' lists commands)"
    )
    try:
        while True:
            try:
                line = input("tick> ").strip()
            except EOFError:
                break
            if not line:
                continue
            if line.lower() in ("quit", "exit"):
                break
            session.execute(line)
    except KeyboardInterrupt:
        print()
    finally:
        session.close()
    print(f"[session log: {session.log_path}]")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="canonsim",
        description="TavernSim v0 — deterministic simulation, no LLM "
        "(simulator produces facts; the chronicle reads them from the log)",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="seed for the interactive session (default: 42)",
    )
    parser.add_argument(
        "--directors", choices=("on", "off"), default="on",
        help="director releases for the interactive session (default: on)",
    )
    parser.add_argument(
        "--logs-dir", default=str(LOGS_DIR),
        help="where run logs are written (default: the repo's logs/)",
    )
    sub = parser.add_subparsers(dest="command")

    play = sub.add_parser("play", help="run a playscript end-to-end")
    play.add_argument("script", type=Path, help="playscript .json path")
    play.add_argument("--seed", type=int, default=None,
                      help="override the script's seed")
    play.add_argument("--directors", choices=("on", "off"), default="on",
                      help="director releases (default: on)")
    play.add_argument("--logs-dir", default=str(LOGS_DIR))
    play.add_argument("--out-dir", default=str(OUTPUT_DIR))

    chronicle = sub.add_parser("chronicle", help="render a log's chronicle")
    chronicle.add_argument("log", type=Path)

    state = sub.add_parser("state", help="one entity's history + state")
    state.add_argument("entity", help="entity id (e.g. purse_01, npc_guard_01)")
    state.add_argument("log", type=Path)

    replay = sub.add_parser("replay", help="validate + fold a log (T2)")
    replay.add_argument("log", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry: subcommand dispatch, interactive session by default."""
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "play":
            return cmd_play(args)
        if args.command == "chronicle":
            return cmd_chronicle(args)
        if args.command == "state":
            return cmd_state(args)
        if args.command == "replay":
            return cmd_replay(args)
        return run_session(args)
    except (
        RunnerError, PackError, LogError, RenderError, GrammarError,
        MediatorError, ValueError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
