"""Phase-0 balance harness (KI#4 close, `docs/TEST_PLAN.md` §6).

Runs the gate playscript (or a variant) N times across sampled seeds,
folds each log through `core/metrics.py`, and emits a distribution
table for: `suspicion` peak per NPC, `fire_spread` spot count at
burnout, M1–M5, the emergent-chain count, and the eventless
beat-stretch distribution (DIR-2, phase 3 — the exit criterion's
measurement). Validates that the `rules.json` thresholds are tuned,
not guessed (D-019 — directionality first, numbers from data).

The pacing A/B (DIR-2): `--pacing on` runs the committed pack as-is;
`--pacing off` runs the same pack minus `director.pacing` — a pack
without the block runs the v0.1 minimal pair (the pack's own
declaration is the gate, INV-3) — materialized once per invocation
under the gitignored output dir and linted on load. Both arms keep the
director enabled (the question is what the CLOCK changes; the
director-off baseline stays `--directors off`).

Output: `output/balance_<N>.txt` (gitignored runtime artifact — never
committed; the harness itself is committed, the runs are reproducible
from the seed range).

Usage:
    python -m scripts.balance_harness --runs 1000 --seed-base 100
    python -m scripts.balance_harness --runs 50 --directors off
    python -m scripts.balance_harness --runs 100 --script \
        tests/playscripts/day1_full.json
    python -m scripts.balance_harness --runs 200 --directors on \
        --pacing off  # the DIR-2 A/B's clock-off arm
"""

from __future__ import annotations

import argparse
import json
import shutil
import statistics
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

# Allow `python scripts/balance_harness.py` and `python -m scripts.balance_harness`
REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from core.fold import fold, initial_projection  # noqa: E402
from core.log import read_log  # noqa: E402
from core.loop import Simulator, load_playscript  # noqa: E402
from core.metrics import (  # noqa: E402
    MetricReport,
    eventless_beat_stretches,
    metrics_report,
)
from core.pack import Pack, load_pack  # noqa: E402
from render.tracery import Grammar  # noqa: E402

DEFAULT_SCRIPT = REPO / "tests" / "playscripts" / "day1_full.json"
DEFAULT_OUT = REPO / "output"
PACK_DIR = REPO / "content" / "tavern_pack"


def _load() -> tuple[Pack, dict[str, Any], dict[str, Any]]:
    pack = load_pack(PACK_DIR)
    schema = json.loads(
        (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
    )
    script = load_playscript(DEFAULT_SCRIPT)
    return pack, schema, script


def _nopacing_pack(out_dir: Path) -> Pack:
    """The clock-off arm's pack: the committed pack minus `director.pacing`
    (a pack without the block runs the v0.1 minimal pair — the pack's own
declaration is the gate, INV-3). Materialized once per invocation under
the gitignored output dir; `load_pack` runs the full lint on it."""
    variant_dir = out_dir / "pack_nopacing"
    variant_dir.mkdir(parents=True, exist_ok=True)
    for name in sorted(p.name for p in PACK_DIR.glob("*.json")):
        source = PACK_DIR / name
        if name == "rules.json":
            rules = json.loads(source.read_text(encoding="utf-8"))
            rules["director"].pop("pacing", None)
            (variant_dir / name).write_text(
                json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        else:
            shutil.copyfile(source, variant_dir / name)
    return load_pack(variant_dir)


def _suspicion_peaks(
    events: Sequence[Any], projection: dict[str, dict[str, Any]]
) -> dict[str, int]:
    """Peak suspicion per NPC across the run (max value seen, not just
    final — a guard who escalated then de-escalated still peaked)."""
    peaks: dict[str, int] = {}
    # init from projection (0 default per the pack)
    for npc_id in projection:
        if "relations.suspicion" in projection[npc_id]:
            peaks[npc_id] = int(projection[npc_id]["relations.suspicion"])
    # walk every state_change on the suspicion axis
    for event in events:
        for change in event.state_changes:
            if change.prop == "relations.suspicion":
                current = peaks.get(change.entity, 0)
                peaks[change.entity] = max(current, int(change.to_))
    return peaks


def _fire_destroyed_locations(
    events: Sequence[Any], projection: dict[str, dict[str, Any]]
) -> int:
    """Count of locations whose `destroyed` prop is True at run end (T4
    irreversibility evidence — a burned location stays burned; fire has
    no counter-event). The `fire.<spot>` props are the burning lifecycle
    (None → 'burning', irreversible); the location's `destroyed = True`
    is the canonical 'this place is gone' marker."""
    count = 0
    for _entity_id, props in projection.items():
        if props.get("destroyed") is True:
            count += 1
    return count


def _run_one(
    pack: Pack, schema: dict[str, Any], script: dict[str, Any],
    seed: int, directors: bool, pacing: bool, gate: str, out_dir: Path,
) -> tuple[MetricReport, dict[str, int], int, list[int]]:
    """One balance run: simulate → fold → metrics + peaks + burned spots
    + the eventless beat-stretch lengths (DIR-2, gate-read from the pack's
    own tale gate — the same gate the chronicle renders by)."""
    arm = f"{'on' if directors else 'off'}" + ("" if pacing else "_nopacing")
    log = out_dir / f"balance_{seed}_{arm}.jsonl"
    if log.exists():
        log.unlink()
    sim = Simulator(
        pack, seed, log, schema, commit="0000000",
        director_enabled=directors,
    )
    sim.run_playscript(dict(script, seed=seed))
    _, events = read_log(log, schema)
    projection = fold(events, initial_projection(pack.entities))
    report = metrics_report(
        pack.rules, events, projection,
        player_id=pack.player_id(), director_on=directors,
    )
    peaks = _suspicion_peaks(events, projection)
    burned = _fire_destroyed_locations(events, projection)
    stretches = eventless_beat_stretches(pack.rules, events, gate=gate)
    return report, peaks, burned, stretches


def _aggregate(reports: list[MetricReport],
               peaks_list: list[dict[str, int]],
               burned_list: list[int],
               stretch_lists: list[list[int]]) -> dict[str, Any]:
    """Aggregate per-metric stats across N runs."""
    def _stats(values: list[float]) -> dict[str, float]:
        return {
            "min": min(values),
            "p50": statistics.median(values),
            "mean": statistics.mean(values),
            "max": max(values),
        }
    out: dict[str, Any] = {
        "runs": len(reports),
        "events": _stats([r.events for r in reports]),
        "M1": _stats([r.m1_cross_system_share for r in reports]),
        "M3_mean": _stats([r.m3_mean for r in reports]),
        "M3_median": _stats([r.m3_median for r in reports]),
        "M4_repetition": _stats([r.m4_repetition_rate for r in reports]),
        "M4_distinct_knows": _stats([r.m4_distinct_knows_share for r in reports]),
        "M5": _stats([r.m5_non_pc_share for r in reports]),
        "emergent_chains": _stats([float(r.emergent_chains) for r in reports]),
        "destroyed_locations": _stats([float(b) for b in burned_list]),
        "eventless_max_stretch": _stats(
            [float(max(s)) if s else 0.0 for s in stretch_lists]
        ),
        "runs_with_stretches": sum(1 for s in stretch_lists if s),
    }
    histogram: dict[int, int] = {}
    for stretches in stretch_lists:
        for length in stretches:
            histogram[length] = histogram.get(length, 0) + 1
    out["stretch_histogram"] = dict(sorted(histogram.items()))
    # suspicion peaks: aggregate per NPC
    npc_ids = {npc for peaks in peaks_list for npc in peaks}
    peak_stats: dict[str, dict[str, float]] = {}
    for npc in sorted(npc_ids):
        vals = [peaks.get(npc, 0) for peaks in peaks_list]
        peak_stats[npc] = _stats([float(v) for v in vals])
    out["suspicion_peaks"] = peak_stats
    return out


def _render_table(stats: dict[str, Any], *, gate: str, pacing: bool) -> str:
    """ASCII table of the aggregated stats (one block, worklog-friendly)."""
    lines: list[str] = []
    arm = "clock on" if pacing else "clock off (v0.1 minimal pair)"
    lines.append(f"balance harness — {stats['runs']} runs — pacing: {arm}")
    lines.append("-" * 60)
    lines.append(f"{'metric':<22}{'min':>10}{'p50':>10}{'mean':>10}{'max':>10}")
    for key in (
        "events", "M1", "M3_mean", "M3_median",
        "M4_repetition", "M4_distinct_knows", "M5",
        "emergent_chains", "destroyed_locations",
        "eventless_max_stretch",
    ):
        s = stats[key]
        lines.append(
            f"{key:<22}{s['min']:>10.2f}{s['p50']:>10.2f}"
            f"{s['mean']:>10.2f}{s['max']:>10.2f}"
        )
    lines.append("-" * 60)
    lines.append(
        f"eventless beat-stretches (gate={gate}): "
        f"{stats['runs_with_stretches']}/{stats['runs']} runs quiet at least once"
    )
    histogram = stats["stretch_histogram"]
    if histogram:
        cells = "  ".join(f"{length}:{count}" for length, count in histogram.items())
        lines.append(f"stretch histogram (length:count) — {cells}")
    else:
        lines.append("stretch histogram (length:count) — none: every window had a scene event")
    lines.append("-" * 60)
    lines.append("suspicion peaks per NPC:")
    lines.append(f"{'npc':<22}{'min':>10}{'p50':>10}{'mean':>10}{'max':>10}")
    for npc, s in stats["suspicion_peaks"].items():
        lines.append(
            f"{npc:<22}{s['min']:>10.0f}{s['p50']:>10.0f}"
            f"{s['mean']:>10.0f}{s['max']:>10.0f}"
        )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="balance_harness",
        description="1000-sim distribution harness for KI#4 (phase-0 gate) "
                    "+ the DIR-2 pacing A/B (phase 3)",
    )
    parser.add_argument("--runs", type=int, default=1000,
                        help="number of seed-varied runs (default: 1000)")
    parser.add_argument("--seed-base", type=int, default=100,
                        help="first seed (default: 100; runs use 100..100+N-1)")
    parser.add_argument("--directors", choices=("on", "off"), default="off",
                        help="director policy (default: off — the T8 baseline)")
    parser.add_argument("--pacing", choices=("on", "off"), default="on",
                        help="the pacing clock arm (default: on — the committed "
                             "pack; 'off' runs the pack minus director.pacing, "
                             "the v0.1 minimal pair — requires --directors on)")
    parser.add_argument("--script", type=Path, default=DEFAULT_SCRIPT,
                        help="playscript path (default: day1_full.json)")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT,
                        help="output directory (default: the repo's output/)")
    args = parser.parse_args(argv)

    directors = args.directors == "on"
    pacing = args.pacing == "on"
    if not pacing and not directors:
        parser.error(
            "--pacing off requires --directors on: a disabled director never "
            "consults the clock (the arm would measure nothing — the "
            "director-off baseline is --directors off --pacing on)"
        )

    pack, schema, default_script = _load()
    script = (
        load_playscript(args.script) if args.script != DEFAULT_SCRIPT
        else default_script
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if not pacing:
        pack = _nopacing_pack(args.out_dir)
    # the gate the chronicle renders by (the same reader, the same default —
    # the metric's scene definition IS the tale's)
    gate = Grammar(pack.templates).tale_gate

    reports: list[MetricReport] = []
    peaks_list: list[dict[str, int]] = []
    burned_list: list[int] = []
    stretch_lists: list[list[int]] = []
    for offset in range(args.runs):
        seed = args.seed_base + offset
        report, peaks, burned, stretches = _run_one(
            pack, schema, script, seed, directors, pacing, gate, args.out_dir,
        )
        reports.append(report)
        peaks_list.append(peaks)
        burned_list.append(burned)
        stretch_lists.append(stretches)

    stats = _aggregate(reports, peaks_list, burned_list, stretch_lists)
    table = _render_table(stats, gate=gate, pacing=pacing)
    suffix = "" if pacing else "_nopacing"
    out_path = args.out_dir / (
        f"balance_{args.runs}_seed{args.seed_base}_{args.directors}{suffix}.txt"
    )
    out_path.write_text(table, encoding="utf-8")
    print(table)
    print(f"[balance table saved: {out_path}]")
    if directors and pacing:
        print(
            "[DIR-2 A/B: re-run with --pacing off for the clock-off arm "
            "(same seed range) — the exit criterion's measurement]"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
