"""Phase-0 balance harness (KI#4 close, `docs/TEST_PLAN.md` §6).

Runs the gate playscript (or a variant) N times across sampled seeds,
folds each log through `core/metrics.py`, and emits a distribution
table for: `suspicion` peak per NPC, `fire_spread` spot count at
burnout, M1–M5, and the emergent-chain count. Validates that the
`rules.json` thresholds are tuned, not guessed (D-019 — directionality
first, numbers from data).

Output: `output/balance_<N>.txt` (gitignored runtime artifact — never
committed; the harness itself is committed, the runs are reproducible
from the seed range).

Usage:
    python -m scripts.balance_harness --runs 1000 --seed-base 100
    python -m scripts.balance_harness --runs 50 --directors off
    python -m scripts.balance_harness --runs 100 --script \
        tests/playscripts/day1_full.json
"""

from __future__ import annotations

import argparse
import json
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
from core.metrics import MetricReport, metrics_report  # noqa: E402
from core.pack import load_pack  # noqa: E402

DEFAULT_SCRIPT = REPO / "tests" / "playscripts" / "day1_full.json"
DEFAULT_OUT = REPO / "output"


def _load() -> tuple[Any, dict[str, Any], dict[str, Any]]:
    pack = load_pack(REPO / "content" / "tavern_pack")
    schema = json.loads(
        (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
    )
    script = load_playscript(DEFAULT_SCRIPT)
    return pack, schema, script


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
    pack: Any, schema: dict[str, Any], script: dict[str, Any],
    seed: int, directors: bool, out_dir: Path,
) -> tuple[MetricReport, dict[str, int], int]:
    """One balance run: simulate → fold → metrics + peaks + burned spots."""
    log = out_dir / f"balance_{seed}_{'on' if directors else 'off'}.jsonl"
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
    return report, peaks, burned


def _aggregate(reports: list[MetricReport],
               peaks_list: list[dict[str, int]],
               burned_list: list[int]) -> dict[str, Any]:
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
    }
    # suspicion peaks: aggregate per NPC
    npc_ids = {npc for peaks in peaks_list for npc in peaks}
    peak_stats: dict[str, dict[str, float]] = {}
    for npc in sorted(npc_ids):
        vals = [peaks.get(npc, 0) for peaks in peaks_list]
        peak_stats[npc] = _stats([float(v) for v in vals])
    out["suspicion_peaks"] = peak_stats
    return out


def _render_table(stats: dict[str, Any]) -> str:
    """ASCII table of the aggregated stats (one block, worklog-friendly)."""
    lines: list[str] = []
    lines.append(f"balance harness — {stats['runs']} runs")
    lines.append("-" * 60)
    lines.append(f"{'metric':<22}{'min':>10}{'p50':>10}{'mean':>10}{'max':>10}")
    for key in (
        "events", "M1", "M3_mean", "M3_median",
        "M4_repetition", "M4_distinct_knows", "M5",
        "emergent_chains", "destroyed_locations",
    ):
        s = stats[key]
        lines.append(
            f"{key:<22}{s['min']:>10.2f}{s['p50']:>10.2f}"
            f"{s['mean']:>10.2f}{s['max']:>10.2f}"
        )
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
        description="1000-sim distribution harness for KI#4 (phase-0 gate)",
    )
    parser.add_argument("--runs", type=int, default=1000,
                        help="number of seed-varied runs (default: 1000)")
    parser.add_argument("--seed-base", type=int, default=100,
                        help="first seed (default: 100; runs use 100..100+N-1)")
    parser.add_argument("--directors", choices=("on", "off"), default="off",
                        help="director policy (default: off — the T8 baseline)")
    parser.add_argument("--script", type=Path, default=DEFAULT_SCRIPT,
                        help="playscript path (default: day1_full.json)")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT,
                        help="output directory (default: the repo's output/)")
    args = parser.parse_args(argv)

    pack, schema, default_script = _load()
    script = (
        load_playscript(args.script) if args.script != DEFAULT_SCRIPT
        else default_script
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)

    directors = args.directors == "on"
    reports: list[MetricReport] = []
    peaks_list: list[dict[str, int]] = []
    burned_list: list[int] = []
    for offset in range(args.runs):
        seed = args.seed_base + offset
        report, peaks, burned = _run_one(
            pack, schema, script, seed, directors, args.out_dir,
        )
        reports.append(report)
        peaks_list.append(peaks)
        burned_list.append(burned)

    stats = _aggregate(reports, peaks_list, burned_list)
    table = _render_table(stats)
    out_path = args.out_dir / f"balance_{args.runs}_seed{args.seed_base}_{args.directors}.txt"
    out_path.write_text(table, encoding="utf-8")
    print(table)
    print(f"[balance table saved: {out_path}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
