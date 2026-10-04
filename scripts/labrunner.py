"""The Atomic World Lab batch runner (lab-1, Stage A of the owner's
CANONSIM_ATOMIC_WORLD_LAB_AGENT_PACK v1.5 — its 04 §2 the order owner;
the pack's README the discipline source).

THE LAB LAWS (the pack's non-negotiables, made executable here):

1. NO SECOND RUNTIME. The Lab drives the real Simulator and reads the
   committed log only — one log, one fold, one canon. Metrics are
   derived read-side aggregates over `core.log.read_log` output; the
   runner never emits, reorders, or patches events (INV-1, and the
   pack's "no second event store/truth/RNG/scheduler/resolver").
2. PLAYER-ABSENT MEANS NO PLAYER-AUTHORED INPUT (the pack's 01 §3 /
   03 §3): one anchor move to a declared location, then ONE wait that
   spans the whole horizon. No other player intent ever fires. The
   scene LOD still reads the player position — that is exactly why
   the anchor is FIXED and declared, never wandered (until an
   observer-independence probe exists, the pack's 03 §3 fence).
3. DIRECTORS OFF BY DEFAULT: the E0 baseline isolates the world's own
   cadence machinery from the director's story pressure (the pack
   01 §11 probe form; `--directors on` exists for the paired arm).
4. MINIMAL OBSERVATION PROFILE (the pack's 09 §5): run identity, seed,
   tick range, event/state counts, wall time, per-type invocation
   aggregates. No per-event telemetry, no viewer dependency; the run
   stays valid without the record.
5. THE EXPERIMENT-CONTRACT RECORD (the pack's 03 §8, the E0 subset —
   assignment vs realized kept apart): QUESTION, IDENTITY, ARMS, RUNS,
   METRICS, DISPOSITION — one JSON artifact under the gitignored
   output dir, rebuildable from (seed, pack, horizon).
6. T1 BYTE-IDENTITY DOUBLE-RUN (`--verify-replay`, the pack's F1):
   same seed + same declared environment -> the two log byte streams
   equal. The same-environment law only — cross-environment claims
   route to `scripts/semantic_diff.py`, never here (replay-1's fence).

The ablation arm (`--arm minus:<block>`) materializes the pack minus
one optional rules block under the gitignored output dir — the 68a law
(the balance_harness precedent: an absent optional block is the
primitive silent; `load_pack` lints the variant before any run). The
removable set is RE-MEASURED per pack and horizon, never inherited —
the balance harness's tavern day-1 set does NOT transfer to long
horizons. Measured for province_pack at 1y+ (lab-1, seed 42):

    RUN CLEAN:      on_action, reflection, secrets, factions
    LINT-REFUSED:   urgencies (spine-flaw law), expectations
                    (unmintable belief token), traits (trait_held
                    requires declared beliefs)
    RUNTIME-REFUSED: weather (the chain is CADENCE-ARMED by the macro
                    clock — the day-1 harness never crossed it; a
                    long-horizon run does), crime_watch (a missing-
                    block KeyError — a runtime-backstop gap, recorded
                    as the arm's finding, never patched here)

Usage:
    python scripts/labrunner.py --years 10 --seeds 42
    python scripts/labrunner.py --years 100 --seeds 42,7,93,125
    python scripts/labrunner.py --years 10 --seeds 42 --verify-replay
    python scripts/labrunner.py --years 10 --seeds 42,8 \
        --arm minus:on_action
    python scripts/labrunner.py --years 10 --seeds 42 --directors on

Output: `output/lab_<tag>.json` + a stdout summary (the gitignored
runtime artifact family — the harness is committed, the runs are
reproducible from seed + pack + horizon).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

# Allow `python scripts/labrunner.py` and `python -m scripts.labrunner`
REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from core.fold import fold, initial_projection  # noqa: E402
from core.log import read_log  # noqa: E402
from core.loop import Simulator  # noqa: E402
from core.pack import Pack, PackError, load_pack  # noqa: E402

DEFAULT_PACK = REPO / "content" / "province_pack"
DEFAULT_OUT = REPO / "output"

#: The pack's smoke seed set (03 §6 — a smoke set, never a statistical
#: guarantee; replication grows when observed variance requires it).
SMOKE_SEEDS: Final = (7, 42, 93, 125)

#: The run tag's date-free form: the artifact identity is (seed, pack,
#: horizon, arm) — no wall-clock anywhere in the record (INV-2's read-side
#: echo: the record is rebuildable, so it carries no timestamps either;
#: wall SECONDS ride per-run as measured cost, never as identity).


def _load(pack_dir: Path) -> tuple[Pack, dict[str, Any]]:
    pack = load_pack(pack_dir)
    schema = json.loads(
        (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
    )
    return pack, schema


def _cadence(pack: Pack) -> int:
    """The macro clock's year cadence (ticks per year, pack-declared)."""
    return int(pack.rules["time"]["macro"]["cadence_ticks"])


def _player_start(pack: Pack) -> str:
    """The player's declared initial position (the anchor the LOD
    reads; the pack entities own the fact)."""
    player = next(
        (n for n in pack.entities["npcs"] if n.get("is_player")), None,
    )
    if player is None or not player.get("position"):
        raise SystemExit("the pack declares no player position — pin an "
                         "anchor explicitly with --anchor")
    return str(player["position"])


def _anchor_steps(pack: Pack, years: int, anchor: str) -> list[dict[str, Any]]:
    """The PLAYER-ABSENT step list (law 2): a declared anchor move ONLY
    when the player does not already stand there (a rejected move is
    harness noise, not a world fact), then ONE whole-horizon wait. The
    crossings fire mid-wait (D-038's law); the player authors nothing
    else, ever."""
    if pack.kind_of(anchor) != "location":
        known = [rec["id"] for rec in pack.entities["locations"]]
        raise SystemExit(f"anchor {anchor!r} is not a location; known: {known}")
    steps: list[dict[str, Any]] = []
    if anchor != _player_start(pack):
        steps.append({"intent": "move", "target": anchor})
    steps.append({"intent": "wait", "ticks": _cadence(pack) * years})
    return steps


def run_world(
    pack: Pack,
    schema: dict[str, Any],
    seed: int,
    years: int,
    out_dir: Path,
    *,
    anchor: str,
    directors: bool,
    arm: str,
) -> tuple[Path, float]:
    """One Lab run: the real Simulator, player-absent steps, the
    committed log under the gitignored output dir. Returns (log path,
    wall seconds). The log file is per-(seed, arm) so a replication
    never collides with a prior run's bytes.

    A runtime refusal inside the arm (the substrate's own loud
    backstops — the cadence-armed families, the missing-block
    KeyErrors) is reported as the ARM's finding, never a stack trace:
    the ablation set is measured per pack+horizon, not inherited."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # the filename-safe arm form (the owner-side checkout is Windows —
    # a ':' from 'minus:<block>' is an INVALID path char there; the
    # arm's own name stays untouched in the record)
    arm_fs = arm.replace(":", "_").replace("/", "_")
    log = out_dir / f"lab_{seed}_{arm_fs}.jsonl"
    if log.exists():
        log.unlink()
    sim = Simulator(
        pack, seed, log, schema, commit="0000000",
        director_enabled=directors,
    )
    sim.open()
    try:
        t0 = time.perf_counter()
        sim.run_steps(_anchor_steps(pack, years, anchor))
        wall = time.perf_counter() - t0
    except Exception as exc:  # noqa: BLE001 -- the arm's honest verdict:
        # the block is not cleanly removable at this horizon; the
        # substrate's own backstop names the reason.
        sim.close()
        log.unlink(missing_ok=True)
        raise SystemExit(
            f"arm {arm!r} refused at RUNTIME over {years}y: "
            f"{type(exc).__name__}: {exc} — the block is not cleanly "
            f"removable for long-horizon runs on this pack (a measured "
            f"finding, not a defect to patch here)"
        ) from exc
    sim.close()
    return log, wall


#: The event families the E0 baseline classifies (the pack's 06 §11 —
#: semantic vs maintenance vs derived; the family map is read-side
#: vocabulary over the pack's own closed type set, never new canon).
_MAINTENANCE_TYPES: Final = (
    "watch_change", "market_opens", "status_decayed", "weather_turns",
    "year_turns", "smoke_washed_away",
)
_ACCOUNT_PREFIX: Final = "account_"


def _family(event_type: str, outcome: Mapping[str, Any]) -> str:
    """The E0 event-mix family (the pack's 06 §11 interpretation rule:
    first determine WHICH events are maintenance, which semantic)."""
    if event_type.startswith(_ACCOUNT_PREFIX):
        return "account_flow"  # the authored macro flows (economy cadence)
    if event_type in _MAINTENANCE_TYPES:
        return "maintenance"
    if event_type in ("intent_rejected",):
        return "gate"  # an attempted door refused (a fact, not ecology)
    if "outcome" in outcome or event_type.endswith(("_done", "_changes")):
        return "action"  # an actor's realized action (move/take/...)
    return "other"


def extract_metrics(
    pack: Pack,
    schema: dict[str, Any],
    log: Path,
    *,
    years: int,
    wall_s: float,
    directors: bool,
) -> dict[str, Any]:
    """The MINIMAL observation profile (law 4) over one committed log:
    identity, horizon, event counts/mix, autonomous share, projection
    size, cost. Derived read-side only — rebuilding the fold is the
    check, never a second truth."""
    header, events = read_log(log, schema)
    player = pack.player_id()
    projection = fold(events, initial_projection(pack.entities))
    by_type: Counter[str] = Counter(e.type for e in events)
    # The player-authored law check: the anchor's own move + wait
    # completion are the ONLY player-actor events allowed in E0.
    player_events = [e for e in events if e.actor == player]
    actors = {e.actor for e in events}
    autonomous = sum(1 for e in events if e.actor != player)
    mix: Counter[str] = Counter()
    for event in events:
        mix[_family(event.type, event.outcome)] += 1
    final_tick = events[-1].t if events else 0
    return {
        "identity": {
            "seed": int(header["seed"]),
            "pack": str(header["pack"]),
            "schema_version": str(header["schema_version"]),
            "commit": str(header["commit"]),
            "python": str(header["python"]),
            "directors": directors,
            "horizon_years": years,
        },
        "horizon": {
            "final_tick": final_tick,
            "years_requested": years,
            "year_turns": by_type.get("year_turns", 0),
        },
        "counts": {
            "events_total": len(events),
            "events_per_year": round(len(events) / years, 1) if years else 0,
            "unique_event_types": len(by_type),
            "unique_actors": len(actors),
            "autonomous_events": autonomous,
            "autonomous_share": round(autonomous / len(events), 3) if events else 0.0,
            "player_actor_events": len(player_events),
        },
        "mix": dict(sorted(mix.items())),
        "by_type_top": dict(sorted(by_type.items(), key=lambda kv: -kv[1])[:12]),
        # lab-2: the economy verbs' exact counts (the full Counter read,
        # never the top-12 cutoff — a pack whose material loop rides the
        # account family gets its production vocabulary quoted whole)
        "account_verbs": {
            verb: by_type[verb] for verb in (
                "account_sourced", "account_transferred",
                "account_consumed", "account_settled",
            ) if by_type[verb]
        },
        "state": {
            "projection_entities": len(projection),
            "declared_locations": len(pack.entities["locations"]),
            "declared_npcs": len(pack.entities["npcs"]),
            "declared_items": len(pack.entities["items"]),
            "declared_groups": len(pack.entities["groups"]),
        },
        "cost": {
            "wall_seconds": round(wall_s, 2),
            "log_bytes": log.stat().st_size,
        },
    }


#: The E0 QUESTION (the pack's 03 §1 primary question, first battery):
#: what actually changes over the horizon with no player authorship?
_E0_QUESTION: Final = (
    "E0 baseline: what actually changes in the committed world over the "
    "declared horizon with no player-authored input and no director "
    "pressure — which event families carry the log, and is there any "
    "endogenous material/demographic closure? (The pack's 03 §13 minimal "
    "success criteria: repeated cycle + persistent consequence + "
    "downstream consumer — 'activity-only' is a failure for ecology "
    "claims.)"
)


def _disposition(metrics: dict[str, Any]) -> str:
    """The E0 honest read (the pack's FACT/INFERENCE discipline): the
    measured mix either shows ecology-carrying families or it does
    not — never a graded 'mostly working'."""
    mix = metrics["mix"]
    ecology = mix.get("action", 0) + mix.get("other", 0)
    maintenance = mix.get("maintenance", 0) + mix.get("account_flow", 0)
    demographic = sum(
        count for family, count in mix.items()
        if family in ("demographic", "production", "ecology")
    )
    parts = [
        f"FACT: {metrics['counts']['events_total']} events over "
        f"{metrics['identity']['horizon_years']}y, "
        f"{metrics['counts']['autonomous_share']:.0%} autonomous; "
        f"maintenance+account_flow = {maintenance}, action+other = {ecology}."
    ]
    if demographic == 0:
        parts.append(
            "FACT: zero endogenous demographic/production/ecology events — "
            "the world ticks (cadence, weather, decay, flows); it does not "
            "reproduce its own material/social population ecology (the "
            "pack's 01 §11 finding, now measured per-run)."
        )
    else:
        parts.append(f"MEASURED: {demographic} ecology-carrying events — "
                     "classify and trace before any claim.")
    # lab-2: the account verbs are the ECONOMY substrate's own event
    # family — for a pack whose material loop rides them (the Lab's
    # synthetic fixtures) they ARE the production vocabulary; for a
    # pack whose flows are authored ambience (the province's toll nets)
    # they are maintenance. The runner never sniffs which — it quotes
    # the counts and leaves the classification to the pack's economy
    # semantics (the report's own job, never a per-pack branch here).
    verbs = metrics.get("account_verbs", {})
    if verbs:
        parts.append(
            "MEASURED: account-verb events "
            + ", ".join(f"{v}={n}" for v, n in sorted(verbs.items()))
            + " — the pack's material vocabulary; classify per its "
              "economy semantics before any ecology claim."
        )
    parts.append(
        "DISPOSITION: baseline recorded; no promotion claim rides E0 "
        "(assignment != realization; the pack's 06 §15 gate)."
    )
    return " ".join(parts)


def _variant_pack(
    out_dir: Path, pack_dir: Path, block: str,
) -> Pack:
    """The ablation arm's pack (law: the 68a form — the committed pack
    minus ONE optional rules block, materialized under the gitignored
    output dir, full lint on load; a variant the lint refuses never
    runs). Block-scoped by the same measured-not-guessed law as the
    balance harness: interlocked blocks (systems, time, economy...)
    are refused here, never attempted. See the module docstring for
    the MEASURED per-block verdicts on province_pack.

    The dead-template fixpoint: a dropped block's emission vocabulary
    dies with it (PACK_SPEC §5), and the LINT NAMES the dead lines —
    so the materializer iterates (drop block -> lint -> strip the
    named dead lines -> lint again) until clean, bounded. The lint is
    the measurement instrument; no per-block dead-line map is guessed
    or inherited from another pack's family table."""
    REFUSED = {
        "systems", "time", "economy", "checks", "states", "transitions",
        "knowledge", "importance", "metrics", "worldgen", "meta",
        "position_visibility", "brief", "budget", "relations", "retrieval",
        "scene_detail", "travel", "cultures", "names", "echo",
    }
    if block in REFUSED:
        raise SystemExit(
            f"minus:{block} refused — the block is interlocked/required; "
            f"the removable optional set per-pack: urgencies, weather, "
            f"on_action, reflection, secrets, factions, director, "
            f"crime_watch, expectations, traits"
        )
    variant_dir = out_dir / f"pack_minus_{block}"
    variant_dir.mkdir(parents=True, exist_ok=True)
    for name in sorted(p.name for p in pack_dir.glob("*.json")):
        source = pack_dir / name
        if name == "rules.json":
            rules = json.loads(source.read_text(encoding="utf-8"))
            rules.pop(block, None)
            (variant_dir / name).write_text(
                json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        else:
            shutil.copyfile(source, variant_dir / name)
    # The dead-vocabulary fixpoint (bounded; each pass strips only the
    # lines the lint itself declared dead — measured, never guessed).
    dead_re = re.compile(r"templates: '([^']+)' is declared but unused")
    for _ in range(32):
        try:
            return load_pack(variant_dir)
        except PackError as exc:
            dead = sorted(set(dead_re.findall(str(exc))))
            if not dead:
                shutil.rmtree(variant_dir, ignore_errors=True)
                raise SystemExit(
                    f"minus:{block} refused by the pack lint: {exc}"
                ) from exc
            templates_path = variant_dir / "templates.json"
            templates = json.loads(templates_path.read_text(encoding="utf-8"))
            for line in dead:
                templates["events"].pop(line, None)
            templates_path.write_text(
                json.dumps(templates, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
    shutil.rmtree(variant_dir, ignore_errors=True)
    raise SystemExit(
        f"minus:{block} refused — the dead-vocabulary fixpoint did not "
        f"converge in 32 passes; the block is not cleanly removable"
    )


def _render_summary(record: dict[str, Any]) -> str:
    """The stdout summary: the E0 table (one line per run) + the
    disposition — the report format the agent reads first."""
    lines = [
        f"Atomic World Lab — E0 baseline ({record['tag']})",
        f"question: {_E0_QUESTION}",
        f"pack: {record['pack_dir']}",
    ]
    for run in record["runs"]:
        m = run["metrics"]
        lines.append(
            f"  seed {m['identity']['seed']:>4} | "
            f"{m['counts']['events_total']:>6} events | "
            f"{m['counts']['autonomous_share']:>6.1%} auto | "
            f"mix {m['mix']} | {m['cost']['wall_seconds']}s"
        )
    if record.get("replay_check"):
        rc = record["replay_check"]
        lines.append(
            f"  T1 byte-identity: "
            f"{'HELD' if rc['byte_identical'] else 'BROKEN'} "
            f"({rc['first_bytes']} vs {rc['second_bytes']} bytes)"
        )
    lines.append(f"disposition: {record['disposition']}")
    lines.append(f"record: {record['record_path']}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The Atomic World Lab batch runner (Stage A, lab-1).",
    )
    parser.add_argument("--pack", default=str(DEFAULT_PACK),
                        help="the pack directory (default: province_pack)")
    parser.add_argument("--years", type=int, default=10,
                        help="horizon in years (default: 10)")
    parser.add_argument("--seeds", default="42",
                        help="comma-separated seed set (default: 42; the "
                             "smoke set: 7,42,93,125)")
    parser.add_argument("--anchor", default=None,
                        help="the fixed player-anchor location id "
                             "(default: the pack's first declared location)")
    parser.add_argument("--directors", choices=("off", "on"), default="off",
                        help="the director pressure arm (default: off — "
                             "the player-absent E0 baseline)")
    parser.add_argument("--arm", default="baseline",
                        help="'baseline' or 'minus:<rules-block>' — the "
                             "ablation arm (one optional block dropped)")
    parser.add_argument("--verify-replay", action="store_true",
                        help="the F1/T1 double-run: same seed, byte-identity")
    parser.add_argument("--out", default=str(DEFAULT_OUT),
                        help="the output root (gitignored runtime space)")
    parser.add_argument("--tag", default=None,
                        help="the record tag (default: e0_<years>y)")
    args = parser.parse_args(argv)

    pack_dir = Path(args.pack).resolve()
    out_dir = Path(args.out).resolve()
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    directors = args.directors == "on"
    tag = args.tag or f"e0_{args.years}y"
    years = max(1, args.years)

    # The arm resolution: baseline uses the committed pack as-is; the
    # ablation arm materializes the variant once, then every seed runs
    # the SAME variant (the arm is a pack property, never per-seed).
    if args.arm == "baseline":
        pack, schema = _load(pack_dir)
    elif args.arm.startswith("minus:"):
        block = args.arm.split(":", 1)[1]
        pack = _variant_pack(out_dir, pack_dir, block)
        schema = json.loads(
            (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
        )
    else:
        raise SystemExit(f"unknown arm: {args.arm!r}")

    anchor = args.anchor or _player_start(pack)

    runs: list[dict[str, Any]] = []
    for seed in seeds:
        log, wall = run_world(
            pack, schema, seed, years, out_dir,
            anchor=anchor, directors=directors, arm=args.arm,
        )
        metrics = extract_metrics(
            pack, schema, log, years=years, wall_s=wall, directors=directors,
        )
        runs.append({
            "seed": seed,
            "arm": args.arm,
            "anchor": anchor,
            "log": str(log),
            "metrics": metrics,
        })

    record: dict[str, Any] = {
        "question": _E0_QUESTION,
        "tag": tag,
        "pack_dir": str(pack_dir),
        "arm": args.arm,
        "anchor": anchor,
        "runs": runs,
        "disposition": _disposition(runs[0]["metrics"]) if runs else "no runs",
    }

    # The F1/T1 falsifier (law 6): one seed re-run end-to-end; the two
    # committed byte streams must be EQUAL (the same-environment law).
    if args.verify_replay and seeds:
        probe_seed = seeds[0]
        first = Path(runs[0]["log"]).read_bytes()
        log2, _ = run_world(
            pack, schema, probe_seed, years, out_dir,
            anchor=anchor, directors=directors, arm=f"{args.arm}_twin",
        )
        second = log2.read_bytes()
        log2.unlink()
        record["replay_check"] = {
            "seed": probe_seed,
            "byte_identical": first == second,
            "first_bytes": len(first),
            "second_bytes": len(second),
        }
        if first != second:
            record["disposition"] += " T1 BROKEN — the determinism law failed."

    record_path = out_dir / f"lab_{tag}.json"
    record["record_path"] = str(record_path)
    record_path.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(_render_summary(record))
    return 0 if record.get("replay_check", {}).get("byte_identical", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
