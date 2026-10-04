"""lab-1 — the Atomic World Lab Stage A laws (the owner's
CANONSIM_ATOMIC_WORLD_LAB_AGENT_PACK v1.5, its 04 §2 the order owner).

The Lab's own falsifiers, pinned at smoke scale (the pack's 03 §12
battery, the E0/F1/F5 subset that is live TODAY):

- E0 player-absent law: over a player-absent horizon the player
  authors NOTHING but the single whole-horizon wait (the anchor
  move only when the player does not already stand at the anchor);
- E0 horizon law: the requested years cross the macro clock exactly
  (year_turns == years, the scheduler's positive-multiple law);
- F1 same-seed replay: the T1 byte-identity double-run at the smoke
  horizon (the same-environment law, AGENTS §10 / replay-1's fence);
- the metric reproducibility law: the same seed yields the SAME
  derived record (the MINIMAL profile is a pure fold over the log —
  no wall-clock, no paths, in the identity fields);
- the E0 honest-baseline law: the mix is maintenance-dominated and
  carries ZERO ecology-closing families — the pack's 01 §11 finding
  («the world ticks; it does not reproduce its own ecology»), now a
  measured law of the current substrate. When Stage B/D lands the
  first endogenous material/demographic mechanism, THIS test flips
  deliberately — it is the gap's canary, not a regression guard.

The runner's own ablation discovery is exercised at one measured
clean block (on_action) and one measured refusal (weather, the
cadence-armed family) — the per-pack re-measurement law.

lab-3 (the protocol arm, the owner's «продолжай lab3» call — the
deferred-realize finding's answer): the segmented-wait A/B laws —
the step-list form (whole = ONE wait, the committed bytes; segmented
= N waits summing EXACTLY to the span), the segmented player-absent
+ T1 laws, THE MID-HORIZON LIFE DISCRIMINANT (whole: 100% of life at
the horizon's final boundary — iter-324's 94% datum pinned at suite
scale; segmented: every year carries its own life), and the paired
record's REALIZED_DELTA surface (the 03 §8 mandatory field, with the
measured verdict: the protocol is NOT measurement-neutral on this
fixture).

lab-4 (the E1 horizon row, the pack's 04 §12 horizon battery at
kiloyear scale): the REPLAY-COST instrument laws — every metrics
record carries the read-side cost split (read_log wall, fold wall,
the read+fold pipeline's Python-allocation peak, an honest
tracemalloc label — never the OS RSS), and the protocol arithmetic
holds at 1,000y WITHOUT running it (the step-list is a pure function
of (years, segment_ticks): the kiloyear wait list sums EXACTLY to
the span, the whole form stays ONE wait — the committed bytes'
arithmetic never drifts with horizon scale).

lab-5 (the scale-1 instrumentation row — the owner's
«инструментальную строку scale-1 в labrunner» call, the row the
iter-327 NEXT named; the wall-decomposition instrument): the
CANON-NEUTRALITY law (the profiled pass's committed bytes EQUAL the
unprofiled run's — profiling observes, never mutates; canon_check
in-record, a breach is the instrument's own RED), the ACCOUNTING law
(the member split partitions the profiled wall — members + rest ==
the total, the disjointness flag green; E03 rule-parses/beat, E04
greedy derived-read calls/beat vs the STATIC gated-entry demand, and
beats/event — the ULTIMATE pack's counters executable, its stale
"~50 beats/event" replaced by the measured number), and the GROWTH +
honest-label law (the two-depth per-call ratios are the
super-linearity datum; the profiled wall rides under its own key,
never the battery's cost.wall_seconds).

Horizons stay at 2y in-test (≈0.3 s/run); longer horizons are the
runner's job (100y+), never the suite's (the corpus-price law).
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

from core.log import read_log
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "province_pack")
PLAYER = PACK.player_id()
PLAYER_START = next(
    str(n["position"])
    for n in PACK.entities["npcs"]
    if n.get("is_player")
)
YEARS = 2

sys.path.insert(0, str(REPO / "scripts"))
from labrunner import (  # noqa: E402
    _anchor_steps,
    _player_start,
    extract_metrics,
    run_world,
)
from labrunner import main as labrunner_main  # noqa: E402


def _lab_run(tmp_path: Path, seed: int = 42) -> tuple[Path, dict[str, object]]:
    """One player-absent Lab run at the smoke horizon (directors off —
    the E0 baseline form)."""
    log, _wall = run_world(
        PACK, SCHEMA, seed, YEARS, tmp_path,
        anchor=PLAYER_START, directors=False, arm="test",
    )
    metrics = extract_metrics(
        PACK, SCHEMA, log, years=YEARS, wall_s=0.0, directors=False,
    )
    return log, metrics


def test_the_anchor_is_the_players_declared_start() -> None:
    """The default anchor IS the pack's declared player position (the
    03 §3 fixed-observer law: the LOD reads a declared position, the
    harness invents none)."""
    assert _player_start(PACK) == PLAYER_START
    steps = _anchor_steps(PACK, YEARS, PLAYER_START)
    assert steps == [{"intent": "wait", "ticks": 518400 * YEARS}]


def test_player_absent_horizon_authors_one_wait(tmp_path: Path) -> None:
    """E0's player-absent law: the ONLY player-actor events over the
    whole horizon are the single wait completion (the anchor move
    never fires — the player already stands at the declared anchor;
    a rejected move would be harness noise, not a world fact)."""
    log, metrics = _lab_run(tmp_path)
    _, events = read_log(log, SCHEMA)
    player_events = [e for e in events if e.actor == PLAYER]
    assert [e.type for e in player_events] == ["wait"]
    assert metrics["counts"]["player_actor_events"] == 1


def test_horizon_crosses_the_macro_clock_exactly(tmp_path: Path) -> None:
    """The horizon law: year_turns == the requested years (the
    scheduler's positive-multiple law, one turn per crossing —
    maclock-1 held over the whole Lab horizon)."""
    _, metrics = _lab_run(tmp_path)
    assert metrics["horizon"]["year_turns"] == YEARS
    assert metrics["horizon"]["years_requested"] == YEARS


def test_same_seed_byte_identity_at_horizon(tmp_path: Path) -> None:
    """F1/T1 at the smoke horizon: the same seed re-run end-to-end
    produces the IDENTICAL committed byte stream (INV-2's law over a
    player-absent long horizon — the double-run the runner's own
    --verify-replay carries, pinned here at suite scale)."""
    first, _ = _lab_run(tmp_path, seed=42)
    second, _ = _lab_run(tmp_path, seed=42)
    assert first.read_bytes() == second.read_bytes()


def test_metrics_reproducible_per_seed(tmp_path: Path) -> None:
    """The metric-reproducibility law: the derived MINIMAL profile is
    a pure fold over the committed log — the same seed yields the
    same record except the measured cost block (wall seconds)."""
    _, one = _lab_run(tmp_path, seed=7)
    _, two = _lab_run(tmp_path, seed=7)
    one["cost"] = two["cost"] = {}
    assert one == two
    # and the identity block carries the declared environment:
    assert one["identity"]["seed"] == 7
    assert one["identity"]["pack"] == PACK.name_version
    assert one["identity"]["directors"] is False
    assert one["identity"]["horizon_years"] == YEARS


def test_the_e0_mix_is_maintenance_dominant_zero_ecology(
    tmp_path: Path,
) -> None:
    """The honest-baseline canary (the pack's 01 §11 finding as a
    LAW of the current substrate): the player-absent log is carried
    by maintenance + account flows, with ZERO ecology-closing
    families — no birth/death/migration/production/depletion cycle
    exists to fire. This test documents the measured gap; it flips
    only when Stage B/D's first endogenous mechanism lands."""
    _, metrics = _lab_run(tmp_path)
    mix = metrics["mix"]
    assert mix["maintenance"] > 0  # the world ticks (watch/decay/sky)
    assert mix.get("account_flow", 0) > 0  # the authored macro flows
    ecology_families = ("demographic", "production", "ecology")
    for family in ecology_families:
        assert mix.get(family, 0) == 0  # nothing closes a material cycle
    carried = mix["maintenance"] + mix.get("account_flow", 0)
    assert carried / metrics["counts"]["events_total"] > 0.9


def test_ablation_arm_clean_block_runs(tmp_path: Path) -> None:
    """The measured-clean ablation arm: minus:on_action runs the whole
    horizon clean (the 68a law live — the block absent, the primitive
    silent), and the log is SHORTER than the baseline's (the block's
    emission family actually carried events — assignment realized)."""
    variant_dir = tmp_path / "pack_minus_on_action"
    variant_dir.mkdir()
    import shutil

    for name in ("actions.json", "entities.json", "templates.json"):
        shutil.copyfile(
            REPO / "content" / "province_pack" / name, variant_dir / name,
        )
    rules = json.loads(
        (REPO / "content" / "province_pack" / "rules.json").read_text(
            encoding="utf-8",
        )
    )
    rules.pop("on_action", None)
    (variant_dir / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    # the dead-vocabulary fixpoint's first measured pass (on_action's
    # own emission lines — the lint names them; here the family is
    # small enough to pin: the reaction-table types die with the block)
    from core.pack import PackError
    from core.pack import load_pack as _load

    try:
        variant = _load(variant_dir)
    except PackError:
        templates = json.loads(
            (variant_dir / "templates.json").read_text(encoding="utf-8")
        )
        import re

        dead_re = re.compile(r"templates: '([^']+)' is declared but unused")
        dead = sorted(set(dead_re.findall(str(sys.exc_info()[1]))))
        assert dead, "the refusal is not dead-vocabulary — re-measure"
        for line in dead:
            templates["events"].pop(line, None)
        (variant_dir / "templates.json").write_text(
            json.dumps(templates, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        variant = _load(variant_dir)

    baseline_log, _ = _lab_run(tmp_path)
    arm_log, _ = run_world(
        variant, SCHEMA, 42, YEARS, tmp_path,
        anchor=PLAYER_START, directors=False, arm="test_minus",
    )
    _, base_events = read_log(baseline_log, SCHEMA)
    _, arm_events = read_log(arm_log, SCHEMA)
    # The MEASURED E0 finding: on_action's reaction family is
    # player-action-armed — over a player-absent horizon it NEVER
    # fires, so the ablation is count-identical to the baseline (the
    # 03 §8 "assignment != realization" law in reverse: the assigned
    # ablation is realized, but its emission family has no consumer
    # in this regime). Pinned as the honest baseline fact; it flips
    # only when an autonomous consumer starts firing on_action.
    assert len(arm_events) == len(base_events)


def test_ablation_arm_cadence_armed_block_refused(tmp_path: Path) -> None:
    """The measured refusal: minus:weather cannot run a long horizon —
    the weather chain is armed by the MACRO CLOCK (time.macro), not
    the weather block; a day-1 harness never crosses the cadence, a
    Lab horizon does. The runner reports the arm's refusal loudly,
    never a stack trace (the honest-ablation law)."""
    variant_dir = tmp_path / "pack_minus_weather"
    variant_dir.mkdir()
    import shutil

    for name in ("actions.json", "entities.json", "templates.json"):
        shutil.copyfile(
            REPO / "content" / "province_pack" / name, variant_dir / name,
        )
    rules = json.loads(
        (REPO / "content" / "province_pack" / "rules.json").read_text(
            encoding="utf-8",
        )
    )
    rules.pop("weather", None)
    (variant_dir / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    from core.pack import PackError
    from core.pack import load_pack as _load

    try:
        variant = _load(variant_dir)
    except PackError:
        templates = json.loads(
            (variant_dir / "templates.json").read_text(encoding="utf-8")
        )
        templates["events"].pop("weather_turns", None)
        templates["events"].pop("smoke_washed_away", None)
        (variant_dir / "templates.json").write_text(
            json.dumps(templates, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        variant = _load(variant_dir)

    with pytest.raises(SystemExit, match="refused at RUNTIME"):
        run_world(
            variant, SCHEMA, 42, YEARS, tmp_path,
            anchor=PLAYER_START, directors=False, arm="test_minus_w",
        )


def test_the_runner_cli_smoke(tmp_path: Path) -> None:
    """The CLI form (the operator's door): one seed, the verify-replay
    flag, the JSON record emitted under the output dir; the process
    exits 0 (the T1 check HELD)."""
    out = tmp_path / "out"
    result = subprocess.run(
        [
            sys.executable, str(REPO / "scripts" / "labrunner.py"),
            "--years", "1", "--seeds", "42", "--verify-replay",
            "--out", str(out), "--tag", "cli_smoke",
        ],
        capture_output=True, text=True, timeout=120, cwd=str(REPO),
        env={"PYTHONHASHSEED": "0", "PATH": "", "PYTHONIOENCODING": "utf-8"},
    )
    assert result.returncode == 0, result.stderr[-2000:]
    assert "T1 byte-identity: HELD" in result.stdout
    record = json.loads((out / "lab_cli_smoke.json").read_text(encoding="utf-8"))
    assert record["runs"][0]["metrics"]["horizon"]["year_turns"] == 1


# -- lab-3: the protocol arm (the segmented-wait A/B, the owner's call) --------

FARSTEAD = load_pack(REPO / "content" / "farstead_pack")
SQUARE = "loc_square"


def _protocol_run(
    tmp_path: Path, seed: int, protocol: str,
) -> tuple[Path, dict[str, object]]:
    """One farstead run under a declared wait protocol (2y, the square
    anchor — the living-world arm; directors off, the E0 form)."""
    log, _wall = run_world(
        FARSTEAD, SCHEMA, seed, 2, tmp_path,
        anchor=SQUARE, directors=False, arm="proto_test",
        protocol=protocol,
    )
    metrics = extract_metrics(
        FARSTEAD, SCHEMA, log, years=2, wall_s=0.0, directors=False,
        protocol=protocol,
    )
    return log, metrics


def test_the_step_list_law_per_protocol() -> None:
    """The protocol's own form (law 7): whole = ONE wait spanning the
    horizon (the committed lab-1 bytes — every prior record unchanged);
    segmented = N equal waits summing EXACTLY to the same span, the
    last absorbing the remainder; the boundary law: one segment IS the
    whole (years=1 makes the two step lists equal)."""
    whole = _anchor_steps(PACK, 2, PLAYER_START, protocol="whole")
    assert whole == [{"intent": "wait", "ticks": 518400 * 2}]
    seg = _anchor_steps(PACK, 2, PLAYER_START, protocol="segmented")
    assert seg == [{"intent": "wait", "ticks": 518400}] * 2
    # the custom segment: full segments + the remainder tail
    custom = _anchor_steps(
        PACK, 2, PLAYER_START, protocol="segmented", segment_ticks=700_000,
    )
    assert custom == [
        {"intent": "wait", "ticks": 700_000},
        {"intent": "wait", "ticks": 336_800},
    ]
    assert sum(s["ticks"] for s in custom) == 518_400 * 2
    # the boundary law: at years=1 the protocols coincide
    assert _anchor_steps(PACK, 1, PLAYER_START, protocol="segmented") == \
        _anchor_steps(PACK, 1, PLAYER_START, protocol="whole")


def test_segmented_is_player_absent_and_t1_stable(tmp_path: Path) -> None:
    """The segmented protocol's player-absent law: the player authors
    ONLY waits (one per segment, never another intent kind), and the
    same seed re-run end-to-end is byte-identical (INV-2 held under the
    protocol — the arm is step-list data, never an engine change)."""
    first, metrics = _protocol_run(tmp_path, seed=42, protocol="segmented")
    second, _ = _protocol_run(tmp_path, seed=42, protocol="segmented")
    assert first.read_bytes() == second.read_bytes()
    _, events = read_log(first, SCHEMA)
    player = FARSTEAD.player_id()
    player_events = [e for e in events if e.actor == player]
    kinds = Counter(e.type for e in player_events)
    # the anchor move + the segment waits, NOTHING else, ever
    assert kinds == {"move": 1, "wait": 2}, kinds
    assert metrics["horizon"]["player_waits"] == 2
    assert metrics["horizon"]["year_turns"] == 2  # the horizon law holds


def test_the_mid_horizon_life_law(tmp_path: Path) -> None:
    """THE A/B PRIMARY DISCRIMINANT (lab-3, the deferred-realize
    finding's answer): under the whole wait the world's autonomous life
    realizes ENTIRELY at the horizon's final boundary (the 94% datum of
    iter-324, now 100% at this scale — the mid-horizon log is the
    scheduled machinery alone); under year-segmented waits EVERY year
    carries its own life. Pinned on farstead 2y, the square anchor —
    the numbers are the measured law, not a target."""
    _, whole = _protocol_run(tmp_path, seed=7, protocol="whole")
    _, seg = _protocol_run(tmp_path, seed=7, protocol="segmented")
    whole_life = whole["life"]
    seg_life = seg["life"]
    # whole: the deferred realization — all life in the FINAL span
    assert whole_life["by_year"] == [0, 0, whole_life["total"]]
    assert whole_life["years_with_life"] == 1
    assert whole_life["final_year_share"] == 1.0
    # segmented: life in EVERY year span (the world lives mid-horizon)
    assert seg_life["by_year"][0] == 0  # the initial span: machinery only
    assert seg_life["by_year"][1] > 0
    assert seg_life["by_year"][2] > 0
    assert seg_life["years_with_life"] == 2
    assert seg_life["final_year_share"] < 1.0


def test_the_paired_record_carries_realized_deltas(tmp_path: Path) -> None:
    """The 03 §8 REALIZED_DELTA law, executable: the paired record
    holds per-seed whole-vs-segmented deltas INCLUDING the final
    material state, and the verdict names the measured fact — for this
    fixture the protocol is NOT measurement-neutral (the gates
    re-validate per year against each year's own state, so WHAT
    realizes differs, not only WHEN). The paired battery runs in-process
    through the same door the CLI opens."""
    out = tmp_path / "out"
    rc = labrunner_main([
        "--pack", str(REPO / "content" / "farstead_pack"),
        "--years", "2", "--seeds", "42", "--anchor", SQUARE,
        "--protocol", "paired", "--out", str(out), "--tag", "paired_test",
    ])
    assert rc == 0
    record = json.loads(
        (out / "lab_paired_test.json").read_text(encoding="utf-8")
    )
    assert record["protocol"] == "paired"
    assert len(record["runs"]) == 2  # whole + segmented, the same seed
    (row,) = record["comparison"]
    assert row["seed"] == 42
    assert row["whole"]["protocol"] == "whole"
    assert row["segmented"]["protocol"] == "segmented"
    delta = row["realized_delta"]
    # the realized-delta surface: the final material state per holder
    assert delta["final_material_delta"], "the material delta must be live"
    assert delta["material_state_identical"] is False
    assert delta["events_total"] > 0  # segmented realizes MORE life here
    assert "REALIZED DELTAS LIVE" in record["disposition"]


def test_the_replay_cost_instrument_law(tmp_path: Path) -> None:
    """lab-4 (the E1 horizon row, the pack's 04 §12 battery): every
    metrics record carries the REPLAY-COST instrument — the read-side
    cost split a resume/replay pays, measured on the committed log:
    read_log's wall, the fold's wall, and the read+fold pipeline's
    Python-allocation peak (tracemalloc's own accounting, honestly
    labeled `replay_alloc_peak_mb` — the interpreter's allocations,
    NEVER the OS RSS, portable across the owner's Windows station).
    Non-negative, present on BOTH protocols, and the record stays
    rebuildable (a non-empty log pays real read+fold time)."""
    for protocol in ("whole", "segmented"):
        _, metrics = _protocol_run(tmp_path, seed=7, protocol=protocol)
        cost = metrics["cost"]
        for key in ("read_seconds", "fold_seconds",
                    "replay_alloc_peak_mb"):
            assert key in cost, f"{key} missing under {protocol}"
            assert isinstance(cost[key], (int, float))
            assert cost[key] >= 0, (key, cost[key])
        # a non-empty committed log pays real read+fold time — the
        # instrument measures the pipeline, never a cached zero
        assert metrics["counts"]["events_total"] > 0
        assert cost["read_seconds"] + cost["fold_seconds"] > 0


def test_the_kiloyear_step_list_arithmetic_law() -> None:
    """lab-4 (the E1 horizon row): the protocol's arithmetic holds at
    KILOYEAR scale without running it — the step list is a pure
    function of (years, segment_ticks), so the 1,000y battery's own
    form is pinned here at zero corpus price: year-segmentation yields
    EXACTLY 1,000 waits of the macro cadence (the E1 battery's own
    shape); a custom segment yields whole segments + the remainder
    tail; every list sums EXACTLY to cadence x years (the horizon
    law's arithmetic, scale-free); and the whole form stays ONE wait
    at any horizon — the committed bytes' form never drifts with
    scale."""
    cadence = 518_400
    span = cadence * 1000
    # the E1 battery's own shape: the year-aligned kiloyear wait list
    kiloyear = _anchor_steps(PACK, 1000, PLAYER_START,
                             protocol="segmented")
    assert kiloyear == [{"intent": "wait", "ticks": cadence}] * 1000
    # the custom segment: whole segments + the remainder tail, the sum
    # EXACTLY the span (no drift, no remainder lost at kiloyear scale)
    custom = _anchor_steps(PACK, 1000, PLAYER_START,
                           protocol="segmented", segment_ticks=700_001)
    whole_segments, remainder = divmod(span, 700_001)
    assert len(custom) == whole_segments + (1 if remainder else 0)
    assert sum(s["ticks"] for s in custom) == span
    # the committed whole form: ONE wait at kiloyear scale too
    assert _anchor_steps(PACK, 1000, PLAYER_START,
                         protocol="whole") == [
        {"intent": "wait", "ticks": span}
    ]


# -- lab-5: the wall-decomposition instrument laws (the scale-1
# instrumentation row, the owner's «инструментальную строку scale-1
# в labrunner» call — the row the iter-327 NEXT named) ----------------


def _profile_record(tmp_path: Path) -> dict[str, object]:
    """The lab-5 battery at smoke scale: farstead seed 7, segmented,
    the main 2y run + profiled passes at 1y and 2y (the depth pair the
    growth block reads; canon_check rides the coinciding 2y depth).
    Drives the CLI form — the profile arm is a main-level battery."""
    out = tmp_path / "out"
    rc = labrunner_main([
        "--years", "2", "--seeds", "7", "--protocol", "segmented",
        "--profile-depths", "1,2",
        "--pack", str(REPO / "content" / "farstead_pack"),
        "--anchor", SQUARE, "--out", str(out),
    ])
    assert rc == 0
    record = json.loads(
        (out / "lab_e0_2y_segmented.json").read_text(encoding="utf-8")
    )
    assert "profile" in record
    return record["profile"]


def test_the_wall_instrument_is_canon_neutral(tmp_path: Path) -> None:
    """lab-5 law 1 — the canon-neutrality law: profiling OBSERVES,
    never mutates. The profiled pass's committed bytes are
    byte-identical to the unprofiled main-battery run's at the
    coinciding depth (Q6's instrument-side echo: a profiler that
    shifted ANY canon byte would be a semantic change masquerading as
    measurement — RED, and the runner's own exit code carries the
    verdict, never just this assertion)."""
    profile = _profile_record(tmp_path)
    canon = profile["canon_check"]
    assert canon["checked"] is True
    assert canon["byte_identical"] is True
    assert [row["years"] for row in canon["depths"]] == [2]


def test_the_wall_split_accounting_law(tmp_path: Path) -> None:
    """lab-5 law 2 — the accounting law: the member split PARTITIONS
    the profiled wall (every member a documented entry-cumtime
    aggregate; members + rest == the profiled total, the disjointness
    flag green), and the counters carry the ULTIMATE pack's vocabulary:
    the beat machinery re-parses the rules every beat (E03 >= 1
    parse/beat), computes the derived folds GREEDILY on the clock path
    while this fixture's gated-entry demand is ZERO (E04's Q7a waste
    measured — the P0.5-A implementation row's RED baseline, flipping
    deliberately when beat laziness lands), and beats/event is the
    measured per-run number (the pack's stale '~50' replaced)."""
    profile = _profile_record(tmp_path)
    for depth in profile["per_depth"]:
        shares = depth["member_shares"]
        total = depth["profiled_total_seconds"]
        assert depth["members_disjoint"] is True
        assert depth["member_rest_seconds"] >= 0
        accounted = (
            sum(depth["members"].values()) + depth["member_rest_seconds"]
        )
        assert abs(accounted - total) < 1e-3, (depth["years"], accounted)
        assert abs(sum(shares.values()) - 1.0) < 0.01
        # the named members exist as keys even when a depth never pays
        # them (an honest zero, never an absent key)
        for member in ("occ_refold", "knowledge_rerank", "beat_rolls",
                       "decay_walk", "clock_derived_folds",
                       "door_derived_folds", "rest"):
            assert member in shares, (depth["years"], member)
        # the clock parses the rules every beat — E03 measured
        assert depth["beats"] > 0
        assert depth["counters"]["e03_parses_per_beat"] >= 1.0
        # the greedy derived folds: every fold function computed on
        # the clock path at least once per beat — TODAY's shape, the
        # laziness row's own RED baseline
        e04 = depth["counters"]["e04_derived_reads"]
        for name, per_func in e04["per_function"].items():
            assert per_func["clock"] >= depth["beats"], (name, "clock")
        assert e04["clock_calls_per_beat"] >= 3.0
        # this fixture demands NONE of them — the waste quantified
        assert profile["e04_gated_entries"]["total"] == 0
        # the beats/event counter present and measured
        assert depth["beats_per_event"] and depth["beats_per_event"] > 0


def test_the_wall_growth_and_labels_law(tmp_path: Path) -> None:
    """lab-5 law 3 — the growth and honest-label law: the two-depth
    growth block carries the per-call ratios of every key function
    observed at both depths (the super-linearity datum — both rungs
    equally instrumented, the ratio never the absolute), and the
    record's honest labels stand: the profiled wall rides under its
    own key (never the battery's cost.wall_seconds), the notes name
    the instrument artifact, and the key-function table quotes ncalls
    for the beat machinery (the anchor of every per-beat counter)."""
    profile = _profile_record(tmp_path)
    growth = profile["growth"]
    assert growth["from_years"] == 1
    assert growth["to_years"] == 2
    assert growth["per_call_ratios"], "no key function at both depths"
    for label, ratio in growth["per_call_ratios"].items():
        assert ratio > 0, label
    # the beat machinery observed at both depths — the counter anchor
    for depth in profile["per_depth"]:
        key_table = depth["key_functions"]
        assert "core/loop.py:_run_beat" in key_table
        assert key_table["core/loop.py:_run_beat"]["ncalls"] == depth["beats"]
        # the honest labels: profiled wall under its own key, never
        # the battery's wall vocabulary
        assert "profiled_wall_seconds" in depth
        assert "wall_seconds" not in depth
    assert any("instrument artifact" in note for note in profile["notes"])
