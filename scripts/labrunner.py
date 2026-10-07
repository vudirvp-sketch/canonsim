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
7. THE PROTOCOL ARM (lab-3, the owner's «продолжай lab3» call — the
   deferred-realize finding's answer, iter-324's §E1 candidate): the
   player-authored WAIT PROTOCOL is now a declared arm — `whole` (the
   committed lab-1 law 2 form: ONE whole-horizon wait; the default,
   byte-compatible with every prior record), `segmented` (N equal
   waits summing EXACTLY to the horizon — the world realizes its
   autonomous life year by year instead of at the horizon's final
   tick), `paired` (both, the same seed set — the 03 §8 A/B battery
   with REALIZED_DELTA per seed: event totals, the mid-horizon life
   profile, account verbs, the FINAL material state, wall cost). The
   player still authors NOTHING but null waits (never another intent
   kind) — segmentation changes WHEN the world moves, never WHAT the
   player is. The engine is untouched: the arm is step-list data.
8. THE WALL-DECOMPOSITION INSTRUMENT (lab-5, the scale-1
   instrumentation row — the owner's «инструментальную строку scale-1
   в labrunner» call, the row the iter-327 NEXT named): `--profile-
   depths 10,100` runs the FIRST seed once per depth under cProfile
   and decomposes the profiled wall into NAMED MEMBERS by entry
   cumtime — `occ_refold` (occ_breaking_cause's full-log prefix
   refold per OCC rejection, the iter-327 member 1),
   `knowledge_rerank` (_novel_facts' whole-knowledge re-ranking per
   talk, member 2), `beat_rolls` (urgency/faction rolls),
   `decay_walk` (the NPC x axis walk), and the derived folds
   attributed BY CALLER (`_run_beat`/`_run_macro` = the clock's
   greedy per-beat computation vs `_fold_reads` = the intent door's
   lazy reads) — plus the pack counters the ULTIMATE pack named:
   E03 rule-parses per beat (the `_specs` re-parse), E04 derived-read
   calls per beat (greedy vs lazy vs the STATIC gated-entry demand),
   and beats/event (the pack's stale "~50" replaced by the measured
   number). The instrument is CANON-NEUTRAL by law: the profiled
   pass's committed bytes are byte-identical to the unprofiled run
   of the same (seed, anchor, horizon, arm, protocol) tuple — checked
   in-record (canon_check) whenever a depth coincides with the main
   battery, RED otherwise. Honest labels: the profiled wall is an
   instrument artifact (cProfile overhead), never quoted as wall —
   the member SHARES and the two-depth per-call RATIOS are the
   datums (scale-1's Q5 discipline; the split, never the absolute).

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
    python scripts/labrunner.py --years 2 --seeds 7 --protocol paired \
        --pack content/farstead_pack --anchor loc_square
    python scripts/labrunner.py --years 100 --seeds 7 \
        --protocol segmented --segment-ticks 518400
    python scripts/labrunner.py --years 1000 --seeds 7 \
        --protocol segmented  # the E1 horizon ladder (lab-4)
    python scripts/labrunner.py --years 100 --seeds 7 \
        --protocol segmented --profile-depths 10,100 \
        --pack content/farstead_pack  # the wall decomposition (lab-5)

Output: `output/lab_<tag>.json` + a stdout summary (the gitignored
runtime artifact family — the harness is committed, the runs are
reproducible from seed + pack + horizon).
"""

from __future__ import annotations

import argparse
import cProfile
import json
import pstats
import re
import shutil
import sys
import time
import tracemalloc
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

# Allow `python scripts/labrunner.py` and `python -m scripts.labrunner`
REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from core.factions import _specs as _faction_specs  # noqa: E402
from core.fold import fold, initial_projection  # noqa: E402
from core.intent import (  # noqa: E402
    ECHO_TEST,
    LEVERAGE_TEST,
    TRAIT_TEST,
)
from core.log import read_log  # noqa: E402
from core.loop import Simulator  # noqa: E402
from core.pack import Pack, PackError, load_pack  # noqa: E402
from core.urgencies import _specs as _urgency_specs  # noqa: E402

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


def _anchor_steps(
    pack: Pack,
    years: int,
    anchor: str,
    *,
    protocol: str = "whole",
    segment_ticks: int = 0,
) -> list[dict[str, Any]]:
    """The PLAYER-ABSENT step list (law 2 + law 7): a declared anchor
    move ONLY when the player does not already stand there (a rejected
    move is harness noise, not a world fact), then the wait protocol —
    `whole`: ONE wait spanning the horizon (the committed lab-1 form);
    `segmented`: N equal waits summing EXACTLY to the same span (the
    last absorbs the remainder; `segment_ticks=0` = the pack's macro
    cadence — the year-aligned form). The crossings fire mid-wait
    (D-038's law) identically in both forms; the difference is WHERE
    the beat-born and crossing-born autonomous intents land: the
    entry tick they enqueue at is each wait's own completion, so
    segmentation realizes the world's life year by year instead of at
    the horizon's final tick (the deferred-realize law, made an arm)."""
    if pack.kind_of(anchor) != "location":
        known = [rec["id"] for rec in pack.entities["locations"]]
        raise SystemExit(f"anchor {anchor!r} is not a location; known: {known}")
    steps: list[dict[str, Any]] = []
    if anchor != _player_start(pack):
        steps.append({"intent": "move", "target": anchor})
    span = _cadence(pack) * years
    if protocol == "whole":
        steps.append({"intent": "wait", "ticks": span})
        return steps
    if protocol != "segmented":
        raise SystemExit(f"unknown protocol: {protocol!r}")
    seg = segment_ticks or _cadence(pack)
    if seg <= 0 or seg > span:
        raise SystemExit(
            f"segment {seg!r} out of range for the {span}-tick horizon"
        )
    whole_segments, remainder = divmod(span, seg)
    steps += [{"intent": "wait", "ticks": seg}] * whole_segments
    if remainder:
        steps.append({"intent": "wait", "ticks": remainder})
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
    protocol: str = "whole",
    segment_ticks: int = 0,
    profiler: cProfile.Profile | None = None,
    skip: bool = True,
) -> tuple[Path, float, dict[str, int]]:
    """One Lab run: the real Simulator, player-absent steps, the
    committed log under the gitignored output dir. Returns (log path,
    wall seconds). The log file is per-(seed, anchor, horizon, arm,
    protocol) so a replication never collides with a prior run's bytes
    (KI#112, found twice in one battery session: the anchor pair
    batteries collided first, then the 10y battery overwrote the 100y
    logs — the run identity is the full tuple, never a prefix of it).

    `profiler` (lab-5) wraps ONLY the run_steps window in
    enable/disable — observation, never mutation: the profiled pass's
    committed bytes are byte-identical to the unprofiled run's (the
    canon-neutrality law, checked in-record by canon_check); the wall
    under profiling is an instrument artifact, never quoted as wall.

    `skip` (H9, iter-337): the Simulator's quiet-beat skip arm — the
    off-arm (`skip=False`, the `_noskip` log suffix — a separate
    volume, never an overwrite) is the A/B wall's baseline; the two
    arms' bytes are EQUAL by construction (the skip's own falsifier,
    tests/test_h9.py), so the record's cost.skip block carries the
    honest acceleration labels (stretches / skipped beats / landings)
    and the wall delta IS the datum. Returns (log path, wall seconds,
    the skip's stats).

    A runtime refusal inside the arm (the substrate's own loud
    backstops — the cadence-armed families, the missing-block
    KeyErrors) is reported as the ARM's finding, never a stack trace:
    the ablation set is measured per pack+horizon, not inherited."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # the filename-safe arm form (the owner-side checkout is Windows —
    # a ':' from 'minus:<block>' is an INVALID path char there; the
    # arm's own name stays untouched in the record)
    arm_fs = arm.replace(":", "_").replace("/", "_")
    # the protocol's own log stem (whole keeps the committed lab-1 stem
    # form), plus THE ANCHOR (KI#112: the log identity is per-(seed,
    # anchor, arm, protocol) — the anchor pair batteries collided on
    # one name and the road run silently overwrote the square arm's
    # logs; a different anchor is a different world volume)
    proto_fs = "" if protocol == "whole" else f"_{protocol}"
    skip_fs = "" if skip else "_noskip"
    log = out_dir / (
        f"lab_{seed}_{anchor}_{years}y_{arm_fs}{proto_fs}{skip_fs}.jsonl"
    )
    if log.exists():
        log.unlink()
    sim = Simulator(
        pack, seed, log, schema, commit="0000000",
        director_enabled=directors,
        skip_quiet_beats=skip,
    )
    sim.open()
    wall = 0.0
    try:
        t0 = time.perf_counter()
        try:
            if profiler is not None:
                profiler.enable()
            sim.run_steps(
                _anchor_steps(
                    pack, years, anchor,
                    protocol=protocol, segment_ticks=segment_ticks,
                )
            )
        finally:
            if profiler is not None:
                profiler.disable()
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
    return log, wall, sim.skip_stats


#: The event families the E0 baseline classifies (the pack's 06 §11 —
#: semantic vs maintenance vs derived; the family map is read-side
#: vocabulary over the pack's own closed type set, never new canon).
_MAINTENANCE_TYPES: Final = (
    "watch_change", "market_opens", "status_decayed", "weather_turns",
    "year_turns", "smoke_washed_away",
)
_ACCOUNT_PREFIX: Final = "account_"

#: The SCHEDULED MACHINERY the mid-horizon life profile excludes (lab-3):
#: the clock's own events plus the authored environmental mints — the
#: world ticking is not the world LIVING. Everything else an autonomous
#: actor emits (the hauls' settles, the meals' consumes, the talks, the
#: door's refusals, the replies) is realized life, whatever family the
#: mix map assigns it.
_MACHINERY_TYPES: Final = _MAINTENANCE_TYPES + ("account_sourced",)


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
    protocol: str = "whole",
    segment_ticks: int = 0,
    skip_stats: Mapping[str, int] | None = None,
) -> dict[str, Any]:
    """The MINIMAL observation profile (law 4) over one committed log:
    identity, horizon, event counts/mix, autonomous share, projection
    size, cost — plus lab-3's protocol block: the player's own wait
    count, the MID-HORIZON LIFE profile (autonomous non-machinery
    events per year — the deferred-realize discriminant), and the FINAL
    material state (per-holder account levels — the A/B battery's
    REALIZED_DELTA surface, the pack's 03 §8 mandatory field); plus
    lab-4's REPLAY-COST instrument (the pack's 04 §12 horizon battery:
    work, log size, REPLAY COST, state size, MEMORY — read_log's wall,
    the fold's wall, and the Python-allocation peak of the read+fold
    pipeline via tracemalloc, portable across the owner's Windows
    station; tracemalloc measures the interpreter's own allocations,
    never the OS RSS — labeled honestly, never conflated). Derived
    read-side only — rebuilding the fold is the check, never a second
    truth."""
    tracemalloc.start()
    t_read0 = time.perf_counter()
    header, events = read_log(log, schema)
    read_s = time.perf_counter() - t_read0
    t_fold0 = time.perf_counter()
    player = pack.player_id()
    projection = fold(events, initial_projection(pack.entities))
    fold_s = time.perf_counter() - t_fold0
    _, alloc_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    by_type: Counter[str] = Counter(e.type for e in events)
    # The player-authored law check: the anchor's own move + the
    # protocol's waits are the ONLY player-actor events allowed in E0.
    player_events = [e for e in events if e.actor == player]
    actors = {e.actor for e in events}
    autonomous = sum(1 for e in events if e.actor != player)
    mix: Counter[str] = Counter()
    for event in events:
        mix[_family(event.type, event.outcome)] += 1
    final_tick = events[-1].t if events else 0
    # lab-3: the mid-horizon LIFE profile — autonomous events outside
    # the scheduled machinery, bucketed per macro year (floor t//cadence,
    # clamped to `years`; the list carries years+1 spans: 0..years-1 are
    # the calendar years, span `years` is the horizon's final boundary —
    # the last turn, whose drain under the whole protocol carries the
    # ENTIRE deferred realization and under segmentation only the last
    # year's own life; the contrast IS the measurement).
    cadence = _cadence(pack)
    life_by_year = [0] * (years + 1)
    for event in events:
        if (
            event.actor != player
            and event.type not in _MACHINERY_TYPES
        ):
            life_by_year[min(event.t // cadence, years)] += 1
    life_total = sum(life_by_year)
    # lab-3: the realized material state — every account.* prop in the
    # final projection, per holder per kind (the conservation test's
    # own read surface, quoted as the A/B delta instrument)
    final_accounts: dict[str, dict[str, int]] = {}
    for holder in sorted(projection):
        props = projection[holder]
        kinds = {
            key[len("account."):]: int(value)
            for key, value in sorted(props.items())
            if key.startswith("account.")
        }
        if kinds:
            final_accounts[holder] = kinds
    return {
        "identity": {
            "seed": int(header["seed"]),
            "pack": str(header["pack"]),
            "schema_version": str(header["schema_version"]),
            "commit": str(header["commit"]),
            "python": str(header["python"]),
            "directors": directors,
            "horizon_years": years,
            "protocol": protocol,
            "segment_ticks": (
                segment_ticks or cadence if protocol == "segmented" else None
            ),
        },
        "horizon": {
            "final_tick": final_tick,
            "years_requested": years,
            "year_turns": by_type.get("year_turns", 0),
            "player_waits": sum(
                1 for e in player_events if e.type == "wait"
            ),
        },
        "life": {
            "by_year": life_by_year,
            "total": life_total,
            "years_with_life": sum(1 for c in life_by_year if c),
            "final_year_share": (
                round(life_by_year[-1] / life_total, 3) if life_total else 0.0
            ),
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
        # account family gets its production vocabulary quoted whole;
        # iter-335: account_converted joins the read — the family's fifth
        # verb since stageb-1-impl (B2), the B6 turnover metric's own
        # counter, invisible to the top-12 cutoff on long horizons)
        "account_verbs": {
            verb: by_type[verb] for verb in (
                "account_sourced", "account_transferred",
                "account_consumed", "account_settled",
                "account_converted",
            ) if by_type[verb]
        },
        "final_accounts": final_accounts,
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
            # lab-4 (the E1 horizon row, the pack's 04 §12 battery):
            # the replay-cost instrument — what a resume/replay pays to
            # rebuild the world from the committed bytes, plus the
            # read+fold pipeline's Python-allocation peak (never the OS
            # RSS; a tracemalloc honest label)
            "read_seconds": round(read_s, 3),
            "fold_seconds": round(fold_s, 3),
            "replay_alloc_peak_mb": round(alloc_peak / (1024 * 1024), 1),
            # H9 (iter-337): the quiet-beat skip's honest labels — the
            # acceleration's own counters, read-side bookkeeping over
            # the run (never canon); a refused pack (guards) or the
            # off-arm answers all zeros
            **({"skip": dict(skip_stats)} if skip_stats is not None else {}),
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


#: The lab-3 QUESTION (the protocol A/B battery — iter-324's §E1
#: candidate, the deferred-realize finding's answer row): does the wait
#: protocol change only WHEN the world's autonomous life realizes, or
#: also WHAT realizes — and at what native cost?
_LAB3_QUESTION: Final = (
    "Protocol A/B (paired seeds): under the whole-horizon wait the "
    "world's autonomous intents all land at the horizon's final tick "
    "(the deferred-realize law, iter-324's 94% datum) and their gates "
    "re-validate against the END state; under year-segmented waits the "
    "same rolls realize year by year against each year's own state. "
    "Does the segmentation move life into the horizon's middle, does "
    "it change the realized material outcome (the 03 §8 REALIZED_DELTA "
    "law), and what does it cost? (Assignment != realization; no "
    "promotion claim rides a protocol record — the engine is untouched.)"
)


def _life_compact(metrics: dict[str, Any]) -> str:
    """The one-line mid-horizon life profile (the deferred-realize
    discriminant, quoted per run): how much autonomous life, how many
    year-spans carried it (of the years+1 spans — the last span is the
    horizon's final boundary), and what share landed in that final
    span."""
    life = metrics["life"]
    spans = len(life["by_year"])
    return (
        f"life {life['total']} in {life['years_with_life']}/{spans} spans, "
        f"{life['final_year_share']:.0%} final"
    )


def _paired_summary(metrics: dict[str, Any]) -> dict[str, Any]:
    """The compact per-arm read the A/B comparison quotes (the full
    metrics stay in each run's own record entry)."""
    return {
        "protocol": metrics["identity"]["protocol"],
        "events_total": metrics["counts"]["events_total"],
        "autonomous_events": metrics["counts"]["autonomous_events"],
        "player_waits": metrics["horizon"]["player_waits"],
        "life": {
            "total": metrics["life"]["total"],
            "years_with_life": metrics["life"]["years_with_life"],
            "final_year_share": metrics["life"]["final_year_share"],
        },
        "account_verbs": dict(metrics["account_verbs"]),
        "final_accounts": {
            holder: dict(kinds)
            for holder, kinds in metrics["final_accounts"].items()
        },
        "wall_seconds": metrics["cost"]["wall_seconds"],
    }


def _realized_delta(
    whole: dict[str, Any], segmented: dict[str, Any],
) -> dict[str, Any]:
    """The 03 §8 REALIZED_DELTA instrument (mandatory for every A/B
    record): the paired per-seed difference — event totals, the life
    profile, the account verbs, and the FINAL MATERIAL STATE per holder
    per kind (nonzero deltas only, the surface the verdict reads)."""
    verb_delta = {
        verb: segmented["account_verbs"].get(verb, 0)
        - whole["account_verbs"].get(verb, 0)
        for verb in sorted(
            set(whole["account_verbs"]) | set(segmented["account_verbs"])
        )
        if segmented["account_verbs"].get(verb, 0)
        != whole["account_verbs"].get(verb, 0)
    }
    material: dict[str, dict[str, int]] = {}
    for holder in sorted(
        set(whole["final_accounts"]) | set(segmented["final_accounts"])
    ):
        w = whole["final_accounts"].get(holder, {})
        s = segmented["final_accounts"].get(holder, {})
        for kind in sorted(set(w) | set(s)):
            if s.get(kind, 0) != w.get(kind, 0):
                material.setdefault(holder, {})[kind] = (
                    s.get(kind, 0) - w.get(kind, 0)
                )
    return {
        "events_total": (
            segmented["events_total"] - whole["events_total"]
        ),
        "life_total": (
            segmented["life"]["total"] - whole["life"]["total"]
        ),
        "life_years_with_life": (
            segmented["life"]["years_with_life"]
            - whole["life"]["years_with_life"]
        ),
        "account_verbs": verb_delta,
        "final_material_delta": material,
        "material_state_identical": not material,
        "wall_seconds": (
            round(segmented["wall_seconds"] - whole["wall_seconds"], 2)
        ),
    }


def _protocol_disposition(comparison: list[dict[str, Any]]) -> str:
    """The paired record's honest verdict (the pack's FACT/INFERENCE
    discipline): per-seed whether the protocol moved life into the
    horizon's middle, whether the realized material state changed, and
    the one-line disposition — never a graded 'mostly working'."""
    parts: list[str] = []
    for row in comparison:
        w, s, delta = row["whole"], row["segmented"], row["realized_delta"]
        parts.append(
            f"seed {row['seed']}: whole {w['events_total']} events "
            f"({w['life']['years_with_life']}y live, "
            f"{w['life']['final_year_share']:.0%} final) vs segmented "
            f"{s['events_total']} events ({s['life']['years_with_life']}y live, "
            f"{s['life']['final_year_share']:.0%} final); "
            f"events delta {delta['events_total']:+d}; "
            f"material "
            f"{'IDENTICAL' if delta['material_state_identical'] else 'DELTA LIVE'}."
        )
    any_material = any(
        not row["realized_delta"]["material_state_identical"]
        for row in comparison
    )
    verdict = (
        "REALIZED DELTAS LIVE — the protocol is not measurement-neutral: "
        "segmentation changes WHAT the world realizes, not only WHEN "
        "(the gates re-validate per year against each year's own state)."
        if any_material
        else "TIMING-ONLY — the realized material state is protocol-"
        "invariant; segmentation moved life's clock, not its content."
    )
    parts.append(
        "DISPOSITION: " + verdict
        + " No promotion claim rides the record (the pack's 06 §15 gate; "
        "the engine is untouched — the arm is step-list data)."
    )
    return " ".join(parts)


#: The lab-5 QUESTION (the scale-1 instrumentation row, the row the
#: iter-327 NEXT named — the owner's «инструментальную строку scale-1
#: в labrunner» call): what does the native wall CONSIST of, and which
#: members grow super-linearly with depth at constant state?
_PROFILE_QUESTION: Final = (
    "Wall decomposition (scale-1's named gap, iter-327's in-session "
    "cProfile finding made reproducible): at two depths of the SAME "
    "(seed, pack, anchor, protocol) world, what share of the profiled "
    "wall is each named member — the OCC prefix refold "
    "(occ_breaking_cause), the knowledge re-ranking (_novel_facts), "
    "the beat roll machinery, the decay walk, the derived folds by "
    "caller (the clock's greedy per-beat computation vs the intent "
    "door's lazy reads) — and how do the key functions' per-call "
    "costs GROW between the depths? (E03 rule-parses/beat, E04 "
    "derived-read calls/beat vs the static gated-entry demand, and "
    "beats/event quoted with it — the ULTIMATE pack's counters, "
    "measured per-run. The profiled wall is an instrument artifact: "
    "shares and ratios are the datums, never the absolute; the "
    "profiled bytes must equal the unprofiled run's — canon_check.)"
)

#: The member map (the module's own documented split): each member is
#: the CUMULATIVE time of its ENTRY functions — the entries' call
#: subtrees are disjoint by call-site construction (verified live by
#: the accounting law, tests/test_lab.py: sum(members) <= total), so
#: the split partitions the profiled wall with `rest` the remainder.
#: The map is (module-suffix, function-name) pairs, POSIX/Windows
#: portable (the pstats path is normalized before matching).
_MEMBER_ENTRIES: Final[Mapping[str, tuple[tuple[str, str], ...]]] = {
    # iter-327 member 1: the OCC attribution's full-log prefix refold
    "occ_refold": (("core/intent.py", "occ_breaking_cause"),),
    # iter-327 member 2: the teller's whole-knowledge re-ranking per talk
    "knowledge_rerank": (("core/knowledge.py", "_novel_facts"),),
    # the beat's roll machinery (urgency + faction, both clock callers)
    "beat_rolls": (
        ("core/urgencies.py", "urgency_intents"),
        ("core/factions.py", "faction_intents"),
    ),
    # the NPC x axis decay walk
    "decay_walk": (("core/states.py", "decay_drafts"),),
}

#: The derived folds (E04's surface), attributed BY CALLER: the clock
#: path (_run_beat + _run_macro — the greedy per-beat computation,
#: Q7a's measured gap) vs the intent door (_fold_reads — the lazy
#: iter-45 law: computed only when the precondition list reads it).
_DERIVED_FOLDS: Final = (
    ("core/leverage.py", "live_leverage"),
    ("core/echo.py", "echo_scores"),
    ("core/traits.py", "crystallized_traits"),
)
_CLOCK_CALLERS: Final = (
    ("core/loop.py", "_run_beat"),
    ("core/loop.py", "_run_macro"),
)
_DOOR_CALLERS: Final = (("core/loop.py", "_fold_reads"),)

#: The key-function table (iter-327's §B.4 reproduction): ncalls /
#: tottime / cumtime / per-call µs for every named function the
#: decomposition reads. Absent functions (never called at this depth)
#: are simply not in the table — an honest zero, never a guessed one.
_KEY_FUNCS: Final = (
    ("core/loop.py", "_run_beat"),
    ("core/loop.py", "_run_macro"),
    ("core/states.py", "decay_drafts"),
    ("core/urgencies.py", "urgency_intents"),
    ("core/factions.py", "faction_intents"),
    ("core/urgencies.py", "_specs"),
    ("core/factions.py", "_specs"),
    ("core/leverage.py", "live_leverage"),
    ("core/echo.py", "echo_scores"),
    ("core/traits.py", "crystallized_traits"),
    ("core/intent.py", "occ_breaking_cause"),
    ("core/fold.py", "fold"),
    ("core/fold.py", "apply_event"),
    ("core/knowledge.py", "_novel_facts"),
    ("core/knowledge.py", "_ranked"),
)

#: The three derived-fold tests (core/intent.py's closed set) — E04's
#: demand side reads the pack's own parsers, never a second truth.
_GATED_TESTS: Final = (LEVERAGE_TEST, ECHO_TEST, TRAIT_TEST)

_PROFILE_NOTES: Final = (
    "the profiled wall is an instrument artifact (cProfile overhead "
    "rides every entry) — never quoted as wall; the member shares and "
    "the two-depth per-call ratios are the datums (scale-1's Q5 "
    "discipline: the split, never the absolute)",
    "members are entry-cumtime aggregates over the documented map "
    "(_MEMBER_ENTRIES + _DERIVED_FOLDS by caller); rest = total - "
    "sum(members); the profiled bytes must equal the unprofiled "
    "run's (canon_check — the canon-neutrality law)",
    "E03/E04/beats-event are the ULTIMATE pack's counters made "
    "executable: its stale '~50 beats/event' claim is replaced by "
    "the measured per-run number",
)


def _core_key(stats_key: tuple[str, int, str]) -> tuple[str, str] | None:
    """Normalize a pstats key to (module-suffix, name) when it names a
    core/ function, else None. Path-shape portable (the owner-side
    checkout is Windows): backslashes normalized, the LAST '/core/'
    segment anchors the suffix."""
    path = stats_key[0].replace("\\", "/")
    idx = path.rfind("/core/")
    if idx == -1:
        return None
    return (f"core/{path[idx + len('/core/'):]}", stats_key[2])


def _log_event_count(log: Path) -> int:
    """The committed event count, cheap: line 1 is the header
    (EVENT_SCHEMA.md §1 — one header, one event per line), so the
    events are the remaining lines. A counting read, never a second
    parse (the full record stays read_log's own business)."""
    with log.open("rb") as handle:
        return sum(1 for _ in handle) - 1


def _gated_entry_count(pack: Pack) -> dict[str, int]:
    """E04's demand side (read-side, the pack's OWN parsers — no second
    truth): how many urgency/faction entries actually gate on the three
    derived-fold tests. The greedy clock computation pays for EVERY
    beat regardless; the gap between these two numbers is the Q7a
    waste the P0.5-A implementation row will close."""
    families = (("_urgencies", _urgency_specs(pack)),
                ("_factions", _faction_specs(pack)))
    out: dict[str, int] = {}
    for name, specs in families:
        out[name] = sum(
            1 for spec in specs
            if any(cond.get("test") in _GATED_TESTS for cond in spec.requires)
        )
    out["total"] = out["_urgencies"] + out["_factions"]
    return out


def _aggregate_profile(
    prof: cProfile.Profile, *, events_total: int,
) -> dict[str, Any]:
    """One depth's decomposition: the member split (entry cumtimes +
    caller-attributed derived folds), the key-function table, and the
    E03/E04/beats-event counters. pstats' caller attribution is exact
    (sum of caller ct == callee cum, session-verified) — the clock vs
    door split of the derived folds is measured, never estimated."""
    # (module, name) -> [ncalls, tottime, cumtime, callers-map]; the
    # merge absorbs duplicate line-keys for one function (defensive —
    # the target set has one def each).
    raw: dict[tuple[str, str], list[Any]] = {}
    total = 0.0
    for key, (_cc, nc, tt, ct, callers) in pstats.Stats(prof).stats.items():
        total += tt
        ck = _core_key(key)
        if ck is None:
            continue
        row = raw.setdefault(ck, [0, 0.0, 0.0, {}])
        row[0] += nc
        row[1] += tt
        row[2] += ct
        for caller_key, (_ccc, cnc, _ctt, cct) in callers.items():
            cck = _core_key(caller_key)
            if cck is None:
                continue
            crow = row[3].setdefault(cck, [0, 0.0])
            crow[0] += cnc
            crow[1] += cct

    def nc_of(target: tuple[str, str]) -> int:
        return raw.get(target, [0])[0]

    def ct_of(target: tuple[str, str]) -> float:
        return raw.get(target, [0, 0.0])[2]

    def caller_of(
        target: tuple[str, str], callers: tuple[tuple[str, str], ...],
    ) -> tuple[int, float]:
        row = raw.get(target)
        if row is None:
            return (0, 0.0)
        hits = [row[3][c] for c in callers if c in row[3]]
        return (sum(h[0] for h in hits), sum(h[1] for h in hits))

    members: dict[str, float] = {
        name: sum(ct_of(entry) for entry in entries)
        for name, entries in _MEMBER_ENTRIES.items()
    }
    derived_per_func: dict[str, dict[str, int]] = {}
    clock_calls = door_calls = 0
    clock_ct = door_ct = 0.0
    for func in _DERIVED_FOLDS:
        cnc, cct = caller_of(func, _CLOCK_CALLERS)
        dnc, dct = caller_of(func, _DOOR_CALLERS)
        derived_per_func[func[1]] = {"clock": cnc, "door": dnc}
        clock_calls += cnc
        door_calls += dnc
        clock_ct += cct
        door_ct += dct
    members["clock_derived_folds"] = clock_ct
    members["door_derived_folds"] = door_ct
    members_s = {name: round(value, 4) for name, value in members.items()}
    rest = round(total - sum(members.values()), 4)
    shares = {
        name: round(value / total, 3) if total else 0.0
        for name, value in members.items()
    }
    shares["rest"] = round(rest / total, 3) if total else 0.0

    key_functions: dict[str, dict[str, Any]] = {}
    for func in _KEY_FUNCS:
        row = raw.get(func)
        if row is None:
            continue  # never called at this depth — an honest absence
        key_functions[f"{func[0]}:{func[1]}"] = {
            "ncalls": row[0],
            "tottime_s": round(row[1], 4),
            "cumtime_s": round(row[2], 4),
            "per_call_us": round(row[1] / row[0] * 1e6, 1) if row[0] else 0.0,
        }

    beats = nc_of(("core/loop.py", "_run_beat"))
    parses = (
        nc_of(("core/urgencies.py", "_specs"))
        + nc_of(("core/factions.py", "_specs"))
    )
    return {
        "events_total": events_total,
        "beats": beats,
        "macro_crossings": nc_of(("core/loop.py", "_run_macro")),
        "beats_per_event": (
            round(beats / events_total, 2) if events_total else None
        ),
        "profiled_total_seconds": round(total, 4),
        "members": members_s,
        "member_shares": shares,
        "member_rest_seconds": rest,
        # the accounting law's own flag: overlapping subtrees would
        # push the sum past the total — measured, never assumed
        "members_disjoint": sum(members.values()) <= total + 1e-9,
        "key_functions": key_functions,
        "counters": {
            "e03_rule_parses": parses,
            "e03_parses_per_beat": (
                round(parses / beats, 2) if beats else None
            ),
            "e04_derived_reads": {
                "per_function": derived_per_func,
                "clock_calls_total": clock_calls,
                "clock_calls_per_beat": (
                    round(clock_calls / beats, 2) if beats else None
                ),
                "door_calls_total": door_calls,
            },
        },
    }


def _profile_block(
    pack: Pack,
    schema: dict[str, Any],
    seed: int,
    depths: Sequence[int],
    out_dir: Path,
    *,
    anchor: str,
    directors: bool,
    arm: str,
    protocol: str,
    segment_ticks: int,
    main_runs: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """The lab-5 record block: one profiled pass per depth over the
    FIRST seed (the decomposition's datum is the depth pair, never the
    seed spread — replication rides the main battery), the growth
    ratios between the shallowest and deepest rung, the static E04
    demand, and the canon-neutrality check against the main battery's
    own log whenever a depth coincides (the instrument's own
    falsifier: the profiled bytes MUST equal the unprofiled run's)."""
    per_depth: list[dict[str, Any]] = []
    for depth in depths:
        prof = cProfile.Profile()
        log, prof_wall, _prof_skip = run_world(
            pack, schema, seed, depth, out_dir,
            anchor=anchor, directors=directors, arm=f"{arm}_prof",
            protocol=protocol, segment_ticks=segment_ticks,
            profiler=prof,
        )
        per_depth.append({
            "years": depth,
            "log": str(log),
            "profiled_wall_seconds": round(prof_wall, 2),
            **_aggregate_profile(
                prof, events_total=_log_event_count(log),
            ),
        })

    block: dict[str, Any] = {
        "question": _PROFILE_QUESTION,
        "seed": seed,
        "protocol": protocol,
        "depths": list(depths),
        "e04_gated_entries": _gated_entry_count(pack),
        "per_depth": per_depth,
        "notes": list(_PROFILE_NOTES),
    }

    # the growth block: both depths equally instrumented, so the
    # per-call ratio between them is the super-linearity datum (the
    # iter-327 form: fold x9.51, _novel_facts x9.17 at 10y->100y)
    if len(per_depth) >= 2:
        shallow, deep = per_depth[0], per_depth[-1]
        per_call: dict[str, Any] = {}
        ncalls_ratio: dict[str, Any] = {}
        for label, row in deep["key_functions"].items():
            srow = shallow["key_functions"].get(label)
            if srow is None or srow["per_call_us"] <= 0:
                continue
            per_call[label] = round(row["per_call_us"] / srow["per_call_us"], 2)
            ncalls_ratio[label] = (
                round(row["ncalls"] / srow["ncalls"], 2)
                if srow["ncalls"] else None
            )
        block["growth"] = {
            "from_years": shallow["years"],
            "to_years": deep["years"],
            "per_call_ratios": per_call,
            "ncalls_ratios": ncalls_ratio,
            "member_shares": {
                name: [
                    shallow["member_shares"][name],
                    deep["member_shares"][name],
                ]
                for name in deep["member_shares"]
            },
        }

    # the canon-neutrality law: whenever a profiled depth coincides
    # with a main-battery run of the same (seed, protocol), the two
    # committed byte streams must be EQUAL — profiling observes, never
    # mutates; a breach is the instrument's own RED.
    checks: list[dict[str, Any]] = []
    for depth_row in per_depth:
        match = next(
            (
                run for run in main_runs
                if run["seed"] == seed
                and run["protocol"] == protocol
                and run["metrics"]["identity"]["horizon_years"]
                == depth_row["years"]
            ),
            None,
        )
        if match is None:
            continue
        checks.append({
            "years": depth_row["years"],
            "byte_identical": (
                Path(match["log"]).read_bytes()
                == Path(depth_row["log"]).read_bytes()
            ),
        })
    block["canon_check"] = {
        "checked": bool(checks),
        "byte_identical": (
            all(row["byte_identical"] for row in checks) if checks else None
        ),
        "depths": checks,
    }
    return block


def _profile_disposition(profile: Mapping[str, Any]) -> str:
    """The lab-5 honest read (the pack's FACT/INFERENCE discipline):
    the deepest rung's member shares, the E03/E04/beats-event counters,
    the growth ratios of the hottest per-call costs — and the
    canon-neutrality verdict. Shares and ratios only, never the
    absolute profiled wall."""
    deep = profile["per_depth"][-1]
    shares = deep["member_shares"]
    counters = deep["counters"]
    e04 = counters["e04_derived_reads"]
    parts = [
        "FACT: the {}y profiled wall decomposes into ".format(deep["years"])
        + " + ".join(
            f"{name} {share:.1%}"
            for name, share in sorted(
                shares.items(), key=lambda kv: -kv[1]
            )
        )
        + " (rest included in the list; shares only, never wall).",
        "MEASURED: E03 {} rule-parses/beat; E04 {} greedy derived-read "
        "calls/beat vs {} gated entries (the door's lazy reads: {}); "
        "beats/event {}.".format(
            counters["e03_parses_per_beat"],
            e04["clock_calls_per_beat"],
            profile["e04_gated_entries"]["total"],
            e04["door_calls_total"],
            deep["beats_per_event"],
        ),
    ]
    growth = profile.get("growth")
    if growth:
        hottest = sorted(
            growth["per_call_ratios"].items(),
            key=lambda kv: -kv[1],
        )[:3]
        parts.append(
            "GROWTH {}y->{}y: ".format(
                growth["from_years"], growth["to_years"],
            )
            + ", ".join(f"{name} per-call x{ratio}" for name, ratio in hottest)
            + " (both depths equally instrumented — the ratio is the "
            "super-linearity datum)."
        )
    canon = profile.get("canon_check", {})
    if canon.get("checked"):
        parts.append(
            "CANON-NEUTRALITY {}: the profiled bytes {} the unprofiled "
            "run's at depth(s) {}.".format(
                "HELD" if canon["byte_identical"] else "BROKEN",
                "equal" if canon["byte_identical"] else "DIVERGE from",
                [row["years"] for row in canon["depths"]],
            ),
        )
    parts.append(
        "DISPOSITION: the iter-327 in-session decomposition made "
        "reproducible; no promotion claim rides the record (the "
        "implementation rows stay behind their gates)."
    )
    if canon.get("checked") and not canon["byte_identical"]:
        parts.append("T1-CLASS BREACH — the instrument is RED.")
    return " ".join(parts)


def _render_summary(record: dict[str, Any]) -> str:
    """The stdout summary: the E0 table (one line per run) + the
    paired comparison lines (lab-3) + the disposition — the report
    format the agent reads first."""
    lines = [
        f"Atomic World Lab — {record['tag']}",
        f"question: {record.get('question', _E0_QUESTION)}",
        f"pack: {record['pack_dir']}",
    ]
    for run in record["runs"]:
        m = run["metrics"]
        proto = m["identity"]["protocol"]
        lines.append(
            f"  seed {m['identity']['seed']:>4} {proto:<10} | "
            f"{m['counts']['events_total']:>6} events | "
            f"{m['counts']['autonomous_share']:>6.1%} auto | "
            f"{_life_compact(m)} | {m['cost']['wall_seconds']}s"
        )
    for row in record.get("comparison", []):
        delta = row["realized_delta"]
        lines.append(
            f"  A/B seed {row['seed']:>4}: whole {row['whole']['events_total']}"
            f" vs segmented {row['segmented']['events_total']} events "
            f"({delta['events_total']:+d}) | "
            f"material {'IDENTICAL' if delta['material_state_identical'] else 'DELTA LIVE'}"
        )
    if record.get("replay_check"):
        rc = record["replay_check"]
        lines.append(
            f"  T1 byte-identity: "
            f"{'HELD' if rc['byte_identical'] else 'BROKEN'} "
            f"({rc['first_bytes']} vs {rc['second_bytes']} bytes)"
        )
    profile = record.get("profile")
    if profile:
        for depth_row in profile["per_depth"]:
            shares = depth_row["member_shares"]
            counters = depth_row["counters"]
            lines.append(
                f"  profile {profile['seed']:>4} {depth_row['years']:>4}y | "
                f"occ_refold {shares['occ_refold']:.1%} · "
                f"knowledge {shares['knowledge_rerank']:.1%} · "
                f"rest {shares['rest']:.1%} | "
                f"E03 {counters['e03_parses_per_beat']}/beat · "
                f"E04 {counters['e04_derived_reads']['clock_calls_per_beat']}/beat | "
                f"beats/event {depth_row['beats_per_event']}"
            )
        canon = profile.get("canon_check", {})
        if canon.get("checked"):
            lines.append(
                f"  canon-neutrality: "
                f"{'HELD' if canon['byte_identical'] else 'BROKEN'} "
                f"(profiled == unprofiled bytes at "
                f"{[d['years'] for d in canon['depths']]}y)"
            )
        growth = profile.get("growth")
        if growth:
            hottest = sorted(
                growth["per_call_ratios"].items(), key=lambda kv: -kv[1],
            )[:3]
            lines.append(
                f"  growth {growth['from_years']}y->{growth['to_years']}y: "
                + ", ".join(
                    f"{name} ×{ratio}" for name, ratio in hottest
                )
            )
    lines.append(f"disposition: {record['disposition']}")
    lines.append(f"record: {record['record_path']}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The Atomic World Lab batch runner (Stage A, lab-1; "
                    "the lab-3 protocol A/B arm).",
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
    parser.add_argument("--protocol", choices=("whole", "segmented", "paired"),
                        default="whole",
                        help="the player wait protocol (lab-3): 'whole' — "
                             "ONE whole-horizon wait (the committed lab-1 "
                             "law, the default); 'segmented' — N equal "
                             "waits; 'paired' — both, the A/B battery with "
                             "per-seed REALIZED_DELTA")
    parser.add_argument("--segment-ticks", type=int, default=0,
                        help="the segmented wait length (default: 0 = the "
                             "pack's macro cadence — the year-aligned form)")
    parser.add_argument("--verify-replay", action="store_true",
                        help="the F1/T1 double-run: same seed, byte-identity")
    parser.add_argument("--profile-depths", default="",
                        help="the lab-5 wall-decomposition arm (the scale-1 "
                             "instrumentation row): comma-separated depths, "
                             "e.g. '10,100' — the FIRST seed runs once per "
                             "depth under cProfile; the record gains the "
                             "member split, the E03/E04/beats-event counters, "
                             "the growth ratios, and the canon-neutrality "
                             "check (default: off)")
    parser.add_argument("--skip", choices=("on", "off"), default="on",
                        help="H9 (iter-337): the Simulator's quiet-beat "
                             "skip arm (default: on — the skip is "
                             "byte-identical by construction, the A/B law "
                             "pinned in tests/test_h9.py; 'off' is the "
                             "tick-by-tick baseline, the _noskip log "
                             "suffix — the wall A/B's other arm)")
    parser.add_argument("--out", default=str(DEFAULT_OUT),
                        help="the output root (gitignored runtime space)")
    parser.add_argument("--tag", default=None,
                        help="the record tag (default: e0_<years>y, "
                             "e0_<years>y_segmented, or ab_<years>y)")
    args = parser.parse_args(argv)

    pack_dir = Path(args.pack).resolve()
    out_dir = Path(args.out).resolve()
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    directors = args.directors == "on"
    args.skip = args.skip == "on"
    years = max(1, args.years)
    protocols = ["whole", "segmented"] if args.protocol == "paired" \
        else [args.protocol]
    tag = args.tag or (
        f"ab_{years}y" if args.protocol == "paired"
        else f"e0_{years}y" if args.protocol == "whole"
        else f"e0_{years}y_{args.protocol}"
    )

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
    metrics_by_protocol: dict[int, dict[str, dict[str, Any]]] = {}
    for seed in seeds:
        metrics_by_protocol[seed] = {}
        for proto in protocols:
            log, wall, skip_stats = run_world(
                pack, schema, seed, years, out_dir,
                anchor=anchor, directors=directors, arm=args.arm,
                protocol=proto, segment_ticks=args.segment_ticks,
                skip=args.skip,
            )
            metrics = extract_metrics(
                pack, schema, log, years=years, wall_s=wall,
                directors=directors, protocol=proto,
                segment_ticks=args.segment_ticks,
                skip_stats=skip_stats,
            )
            runs.append({
                "seed": seed,
                "arm": args.arm,
                "anchor": anchor,
                "protocol": proto,
                "log": str(log),
                "metrics": metrics,
            })
            metrics_by_protocol[seed][proto] = metrics

    record: dict[str, Any] = {
        "question": (
            _LAB3_QUESTION if args.protocol == "paired" else _E0_QUESTION
        ),
        "tag": tag,
        "pack_dir": str(pack_dir),
        "arm": args.arm,
        "anchor": anchor,
        "protocol": args.protocol,
        "segment_ticks": (
            args.segment_ticks or _cadence(pack)
            if args.protocol != "whole" else None
        ),
        "runs": runs,
    }

    if args.protocol == "paired":
        comparison = []
        for seed in seeds:
            whole_summary = _paired_summary(metrics_by_protocol[seed]["whole"])
            segmented_summary = _paired_summary(
                metrics_by_protocol[seed]["segmented"]
            )
            comparison.append({
                "seed": seed,
                "whole": whole_summary,
                "segmented": segmented_summary,
                "realized_delta": _realized_delta(
                    whole_summary, segmented_summary,
                ),
            })
        record["comparison"] = comparison
        record["disposition"] = (
            _protocol_disposition(comparison) if comparison else "no runs"
        )
    else:
        record["disposition"] = (
            _disposition(runs[0]["metrics"]) if runs else "no runs"
        )
        if args.protocol == "segmented" and runs:
            record["disposition"] += (
                f" PROTOCOL: segmented ({record['segment_ticks']}-tick "
                f"waits, {runs[0]['metrics']['horizon']['player_waits']} "
                f"player waits) — {_life_compact(runs[0]['metrics'])}."
            )

    # The F1/T1 falsifier (law 6): one seed re-run end-to-end; the two
    # committed byte streams must be EQUAL (the same-environment law).
    # The twin runs under the record's FIRST protocol — the paired
    # battery's T1 rides the whole arm (its bytes are the committed
    # form's), a segmented run's T1 rides the segmented arm itself.
    if args.verify_replay and seeds:
        probe_seed = seeds[0]
        probe_proto = protocols[0]
        first = Path(runs[0]["log"]).read_bytes()
        log2, _, _ = run_world(
            pack, schema, probe_seed, years, out_dir,
            anchor=anchor, directors=directors, arm=f"{args.arm}_twin",
            protocol=probe_proto, segment_ticks=args.segment_ticks,
            skip=args.skip,
        )
        second = log2.read_bytes()
        log2.unlink()
        record["replay_check"] = {
            "seed": probe_seed,
            "protocol": probe_proto,
            "byte_identical": first == second,
            "first_bytes": len(first),
            "second_bytes": len(second),
        }
        if first != second:
            record["disposition"] += " T1 BROKEN — the determinism law failed."

    # The lab-5 wall-decomposition arm (law 8): the FIRST seed, one
    # profiled pass per declared depth, the same (anchor, directors,
    # arm, protocol, segment) as the main battery. The block carries
    # its own falsifier — canon_check, the profiled-vs-unprofiled
    # byte identity whenever a depth coincides with the battery.
    profile_depths = sorted({
        int(d) for d in args.profile_depths.split(",") if d.strip()
    })
    if args.profile_depths and (not profile_depths or min(profile_depths) < 1):
        raise SystemExit(
            f"--profile-depths must be comma-separated positive years, "
            f"got {args.profile_depths!r}"
        )
    if profile_depths and seeds:
        record["profile"] = _profile_block(
            pack, schema, seeds[0], profile_depths, out_dir,
            anchor=anchor, directors=directors, arm=args.arm,
            protocol=protocols[0], segment_ticks=args.segment_ticks,
            main_runs=runs,
        )
        record["disposition"] += " " + _profile_disposition(record["profile"])

    record_path = out_dir / f"lab_{tag}.json"
    record["record_path"] = str(record_path)
    record_path.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(_render_summary(record))
    return 0 if (
        record.get("replay_check", {}).get("byte_identical", True)
        and record.get("profile", {}).get("canon_check", {}).get(
            "byte_identical", True,
        )
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
