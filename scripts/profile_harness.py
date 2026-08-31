"""perf-1: the long-tick timing profile (`docs/TECH_NOTES.md` §8 owns the numbers).

One session per invocation: the gate playscript's steps (the story beats —
crime chains, transitions), then chunked `wait` steps to the tick target
(the long-run load — rotations, beats, decay/urgency passes, director).
The write side is timed per phase; the read side (read_log → fold →
metrics → chronicle) is timed separately after close. Each invocation
runs the session TWICE — once clean (the headline wall-clock numbers),
once under cProfile (the hot-spot table) — and byte-compares the two
logs: a free T1-style determinism probe at the tick target, far past the
smoke fixture's horizon.

Timing is wall-clock BY DESIGN: a measurement harness is operator
tooling, not canon (INV-2 bans wall-clock in the log; the
`balance_harness` precedent). Output:
`output/perf_<ticks>_seed<seed>_<on|off>.txt` — gitignored runtime
artifact; the harness is committed, the distilled numbers live in
TECH_NOTES §8. The profile is the gate for anything structural
(`docs/TASKS.md` perf-1).

Usage:
    PYTHONHASHSEED=0 python -m scripts.profile_harness --ticks 10000
    PYTHONHASHSEED=0 python -m scripts.profile_harness --ticks 10000 \
        --directors on
"""

from __future__ import annotations

import argparse
import cProfile
import json
import pstats
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

# Allow `python scripts/profile_harness.py` and `python -m scripts.profile_harness`
REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from core.fold import fold, initial_projection  # noqa: E402
from core.log import read_log  # noqa: E402
from core.loop import Simulator, load_playscript  # noqa: E402
from core.metrics import metrics_report  # noqa: E402
from core.pack import load_pack  # noqa: E402
from render.chronicle import chronicle_from_log  # noqa: E402

DEFAULT_SCRIPT = REPO / "tests" / "playscripts" / "day1_full.json"
DEFAULT_OUT = REPO / "output"
WAIT_CHUNK = 360  # one watch per wait step — grid-aligned, session-shaped
ENGINE_DIRS = ("core", "brief", "render")
HOTSPOT_ROWS = 12


def _session(
    pack: Any,
    schema: dict[str, Any],
    script: dict[str, Any],
    seed: int,
    directors: bool,
    ticks_target: int,
    log_path: Path,
    profiler: cProfile.Profile | None,
) -> dict[str, Any]:
    """One write-side session, timed per phase. Returns phase timings.

    The story phase replays the playscript's own steps; the long-run phase
    feeds grid-aligned wait steps until the clock reaches the tick target.
    Wall-clock here is harness measurement, never a canon input.
    """
    if script["seed"] != seed:
        raise ValueError(
            f"playscript seed {script['seed']} != --seed {seed} "
            f"(run_playscript parity: loud, not silent)"
        )
    if script["pack"] != pack.name_version:
        raise ValueError(
            f"playscript pack {script['pack']!r} != loaded pack "
            f"{pack.name_version!r}"
        )
    if log_path.exists():
        log_path.unlink()
    sim = Simulator(
        pack, seed, log_path, schema, commit="perf0000",
        director_enabled=directors,
    )
    timings: dict[str, Any] = {}
    sim.open()
    try:
        if profiler is not None:
            profiler.enable()
        t0 = time.perf_counter()
        result = sim.run_steps(list(script["steps"]))
        timings["story_wall_s"] = time.perf_counter() - t0
        timings["story_end_tick"] = result.last_tick
        waits = 0
        t1 = time.perf_counter()
        while result.last_tick < ticks_target:
            result = sim.run_steps(
                [{"intent": "wait", "ticks": WAIT_CHUNK}]
            )
            waits += 1
        timings["long_run_wall_s"] = time.perf_counter() - t1
        timings["waits"] = waits
        timings["end_tick"] = result.last_tick
        timings["events"] = result.event_count
        if profiler is not None:
            profiler.disable()
    finally:
        sim.close()
    return timings


def _read_side(
    pack: Any,
    schema: dict[str, Any],
    log_path: Path,
    directors: bool,
) -> dict[str, Any]:
    """Time the read-side stack over the finished log (pure functions)."""
    out: dict[str, Any] = {}
    t0 = time.perf_counter()
    _header, events = read_log(log_path, schema)
    out["read_log_s"] = time.perf_counter() - t0
    t1 = time.perf_counter()
    projection = fold(events, initial_projection(pack.entities))
    out["fold_s"] = time.perf_counter() - t1
    t2 = time.perf_counter()
    metrics_report(
        pack.rules, events, projection,
        player_id=pack.player_id(), director_on=directors,
    )
    out["metrics_s"] = time.perf_counter() - t2
    t3 = time.perf_counter()
    chronicle_from_log(log_path, pack, schema)
    out["chronicle_s"] = time.perf_counter() - t3
    out["read_total_s"] = time.perf_counter() - t0
    out["events"] = len(events)
    return out


def _hotspots(profiler: cProfile.Profile) -> list[dict[str, Any]]:
    """Top engine-side functions by cumulative time (the triage table)."""
    stats = pstats.Stats(profiler).stats
    rows: list[tuple[float, int, str, str]] = []
    for (filename, _lineno, funcname), (
        _cc, nc, _tt, ct, _callers
    ) in stats.items():
        if not any(f"/{d}/" in filename for d in ENGINE_DIRS):
            continue
        rows.append((ct, nc, funcname, Path(filename).name))
    rows.sort(key=lambda r: (-r[0], r[2]))
    return [
        {"cum_s": round(ct, 4), "calls": nc, "func": func, "file": fname}
        for ct, nc, func, fname in rows[:HOTSPOT_ROWS]
    ]


def run_profile(
    pack: Any,
    schema: dict[str, Any],
    script: dict[str, Any],
    seed: int,
    ticks_target: int,
    directors: bool,
    out_dir: Path,
) -> dict[str, Any]:
    """Full profile: clean run + profiled run + byte-compare + read side."""
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"perf{ticks_target}_seed{seed}_{'on' if directors else 'off'}"
    log_a = out_dir / f"{tag}_run1.jsonl"
    log_b = out_dir / f"{tag}_run2.jsonl"
    clean = _session(
        pack, schema, script, seed, directors, ticks_target, log_a, None
    )
    profiler = cProfile.Profile()
    profiled = _session(
        pack, schema, script, seed, directors, ticks_target, log_b, profiler
    )
    byte_identical = log_a.read_bytes() == log_b.read_bytes()
    read = _read_side(pack, schema, log_a, directors)
    hotspots = _hotspots(profiler)
    write_total = clean["story_wall_s"] + clean["long_run_wall_s"]
    return {
        "tag": tag,
        "ticks_target": ticks_target,
        "seed": seed,
        "directors": directors,
        "wait_chunk": WAIT_CHUNK,
        "end_tick": clean["end_tick"],
        "events": clean["events"],
        "story": clean,
        "profiled_story_s": profiled["story_wall_s"],
        "profiled_long_run_s": profiled["long_run_wall_s"],
        "write_total_s": round(write_total, 3),
        "events_per_sec": round(clean["events"] / write_total, 1),
        "ticks_per_sec": round(clean["end_tick"] / write_total, 1),
        "read": read,
        "log_bytes": log_a.stat().st_size,
        "byte_identical_runs": byte_identical,
        "hotspots": hotspots,
    }


def _render_report(report: dict[str, Any]) -> str:
    """ASCII report block (worklog/TECH_NOTES-friendly)."""
    lines: list[str] = []
    lines.append(f"profile {report['tag']} — wait chunk {report['wait_chunk']}")
    lines.append("-" * 64)
    lines.append(
        f"end tick {report['end_tick']} · events {report['events']} · "
        f"log {report['log_bytes'] / 1024:.1f} KiB"
    )
    lines.append(
        f"write side: story {report['story']['story_wall_s']:.2f}s + "
        f"long run {report['story']['long_run_wall_s']:.2f}s "
        f"({report['story']['waits']} waits) = "
        f"{report['write_total_s']:.2f}s"
    )
    lines.append(
        f"  -> {report['ticks_per_sec']:.0f} ticks/s · "
        f"{report['events_per_sec']:.0f} events/s"
    )
    read = report["read"]
    lines.append(
        f"read side: read_log {read['read_log_s']:.3f}s · fold "
        f"{read['fold_s']:.3f}s · metrics {read['metrics_s']:.3f}s · "
        f"chronicle {read['chronicle_s']:.3f}s = {read['read_total_s']:.3f}s"
    )
    lines.append(
        f"under cProfile: story {report['profiled_story_s']:.2f}s + long "
        f"run {report['profiled_long_run_s']:.2f}s "
        f"(hot-spot table only, never the headline)"
    )
    lines.append(
        f"byte-identical clean vs profiled runs: "
        f"{report['byte_identical_runs']}"
    )
    lines.append("-" * 64)
    lines.append(f"engine hot spots (cumulative, top {HOTSPOT_ROWS}):")
    for i, row in enumerate(report["hotspots"], start=1):
        lines.append(
            f"  {i:>2}. {row['cum_s']:>8.3f}s  {row['calls']:>9,d}x  "
            f"{row['func']}  [{row['file']}]"
        )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="profile_harness",
        description="perf-1: long-tick timing profile (TECH_NOTES §8)",
    )
    parser.add_argument("--ticks", type=int, default=10000,
                        help="tick target (default: 10000)")
    parser.add_argument("--seed", type=int, default=125,
                        help="seed (default: 125 — the day1_full seed)")
    parser.add_argument("--directors", choices=("on", "off"), default="off",
                        help="director policy (default: off — T8 baseline)")
    parser.add_argument("--script", type=Path, default=DEFAULT_SCRIPT,
                        help="story-phase playscript (default: day1_full)")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT,
                        help="output directory (default: the repo's output/)")
    args = parser.parse_args(argv)

    pack = load_pack(REPO / "content" / "tavern_pack")
    schema = json.loads(
        (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
    )
    script = load_playscript(args.script)
    report = run_profile(
        pack, schema, script, args.seed, args.ticks,
        args.directors == "on", args.out_dir,
    )
    table = _render_report(report)
    out_path = args.out_dir / f"{report['tag']}.txt"
    out_path.write_text(table, encoding="utf-8")
    print(table)
    print(f"[profile saved: {out_path}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
