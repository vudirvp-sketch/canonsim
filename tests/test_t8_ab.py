"""iter-6 gate acceptance — T8 director-off A/B (`docs/TEST_PLAN.md` §1,
`MVP_SCOPE.md` §14, `phase0.md` §6).

The full director-off A/B run: same playscript, same seed, single-factor
switch (the live-char one-change rule — only the director flag changes
between runs). The OFF run produces ≥3 emergent chains WITHOUT the
director (the gate kill-criterion); the ON run produces at least one
director-injected event (`director_<N>` cause_intent). The director
buffer seeds in both runs (D-005 hygiene — the OFF run is not "no
director", it is "no releases").

The gate playscript (`tests/playscripts/day1_full.json`, seed 32) is the
phase-0 walkthrough scenario: enter the tavern, fail two steals (Doren's
suspicion crosses the document-check threshold), wait through the
afternoon beat + watch rotation, drop the lamp at the backyard, wait
through the evening beat + the second rotation. The OFF run produces 24
emergent chains — far above the gate minimum (≥3); the ON run fires
`director_0000` (the document check).
"""

from __future__ import annotations

import json
from pathlib import Path

from core.fold import fold, initial_projection
from core.log import read_log
from core.loop import Simulator, load_playscript
from core.metrics import emergent_chains, metrics_report, render_report
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "day1_full.json")
PLAYER = PACK.player_id()


def _run(tmp_path: Path, directors: bool) -> tuple[list, Path]:
    """Run the gate playscript with the director on or off; same seed
    (single-factor A/B), same script, same commit. Returns (events, log)."""
    log = tmp_path / f"gate_{SCRIPT['seed']}_{'on' if directors else 'off'}.jsonl"
    if log.exists():
        log.unlink()
    sim = Simulator(
        PACK, SCRIPT["seed"], log, SCHEMA, commit="0000000",
        director_enabled=directors,
    )
    sim.run_playscript(SCRIPT)
    _, events = read_log(log, SCHEMA)
    return events, log


def _director_intents(events: list) -> list[str]:
    """Events whose `provenance.cause_intent` starts with `director_`."""
    return [
        str(e.provenance["cause_intent"])
        for e in events
        if str(e.provenance.get("cause_intent", "")).startswith("director_")
    ]


# -- T8 single-factor A/B ----------------------------------------------------


def test_ab_runs_share_seed_script_commit_single_factor_switch(
    tmp_path: Path,
) -> None:
    """The single-factor discipline (live-char one-change rule): only
    the director flag differs between runs. The seed, the script, the
    pack, and the commit id are identical — verified by reading both
    headers."""
    on_events, on_log = _run(tmp_path, True)
    off_events, off_log = _run(tmp_path, False)
    on_header = json.loads(on_log.read_text(encoding="utf-8").splitlines()[0])
    off_header = json.loads(off_log.read_text(encoding="utf-8").splitlines()[0])
    # everything except the seed-pin counts (the seed is the same; only
    # the run-id suffix differs by the writer's next_log_path slot)
    for key in ("schema_version", "seed", "python", "commit", "pack"):
        assert on_header[key] == off_header[key], f"header {key} diverged"


def test_on_run_fires_at_least_one_director_release(tmp_path: Path) -> None:
    """The ON run fires at least one director-injected event on the
    gate playscript (the document_check release when Doren's suspicion
    crosses 50 after the two failed steals)."""
    events, _ = _run(tmp_path, True)
    intents = _director_intents(events)
    assert intents, (
        "ON run produced no director releases — the gate scenario's "
        "double-steal should cross the document_check threshold (suspicion "
        "≥ 50) and release director_0000"
    )
    assert intents[0] == "director_0000"


def test_off_run_produces_no_director_releases(tmp_path: Path) -> None:
    """The OFF run produces ZERO director-injected events — the
    director's releases are suppressed (the buffer keeps seeding, D-005
    hygiene — the run is not 'no director', it is 'no releases')."""
    events, _ = _run(tmp_path, False)
    assert _director_intents(events) == []


def test_off_run_meets_gate_threshold_three_emergent_chains(
    tmp_path: Path,
) -> None:
    """The T8 gate kill-criterion: ≥3 emergent chains WITHOUT the
    director. The gate playscript produces 24 by the iter-6 baseline;
    this test pins the gate minimum so a regression that drops emergence
    below the threshold fails loudly. An emergent chain is a maximal
    causal path rooted in a player event with a non-PC, non-director
    tail of length ≥ 2 (`TEST_PLAN.md` §1.2)."""
    events, _ = _run(tmp_path, False)
    chains = emergent_chains(events, PLAYER)
    assert len(chains) >= 3, (
        f"T8 gate failed: only {len(chains)} emergent chains in the OFF "
        f"run (gate minimum is 3); the world is too player-centered — "
        f"investigate urgency / rotation / crime-reaction regressions"
    )


def test_off_run_m5_non_zero(tmp_path: Path) -> None:
    """M5 (non-PC event share) > 0 in the OFF run — the world acts
    without the player by construction (D-021 urgencies + crime
    reactions + watch rotations + fire spread). The Kenshi/RimWorld
    'world not player-centered' lesson, made measurable at the
    director-off gate."""
    events, _ = _run(tmp_path, False)
    projection = fold(events, initial_projection(PACK.entities))
    report = metrics_report(
        PACK.rules, events, projection, player_id=PLAYER, director_on=False,
    )
    assert report.m5_non_pc_share > 0


def test_off_run_m3_mean_at_least_two(tmp_path: Path) -> None:
    """M3 mean ≥ 2 — the kill-criterion anti-pattern: 'one event, then
    another = failure' (MVP_SCOPE §15). The gate scenario's OFF run
    produces causal chains of length ≥ 2 by construction (steal →
    suspicion → watch_change → knowledge_transfer)."""
    events, _ = _run(tmp_path, False)
    projection = fold(events, initial_projection(PACK.entities))
    report = metrics_report(
        PACK.rules, events, projection, player_id=PLAYER, director_on=False,
    )
    assert report.m3_mean >= 2.0


def test_on_off_runs_byte_differ(tmp_path: Path) -> None:
    """The ON and OFF runs are byte-different — the director's release
    leaves a trace in the log (the document_check event + its
    downstream). This is the positive complement to T1: same script +
    same seed, different policy → different canon."""
    _, on_log = _run(tmp_path, True)
    _, off_log = _run(tmp_path, False)
    assert on_log.read_bytes() != off_log.read_bytes()


# -- the metric baseline (the iter-6 verdict evidence) -----------------------


def test_gate_metric_baseline_for_verdict(tmp_path: Path) -> None:
    """The metric baseline that the phase-0 verdict reads against the
    MVP_SCOPE §15 directionality targets. The numbers themselves are
    reported in `worklog.md`; this test pins the directionality:
    M1 non-trivial, M2 non-zero on the ON run, M3 mean ≥ 2, M5 > 0 OFF.

    A failure here is a kill-criterion hit — honestly reported, never
    averaged away (MVP_SCOPE §16).
    """
    on_events, _ = _run(tmp_path, True)
    off_events, _ = _run(tmp_path, False)
    on_proj = fold(on_events, initial_projection(PACK.entities))
    off_proj = fold(off_events, initial_projection(PACK.entities))
    on_report = metrics_report(
        PACK.rules, on_events, on_proj, player_id=PLAYER, director_on=True,
    )
    off_report = metrics_report(
        PACK.rules, off_events, off_proj, player_id=PLAYER, director_on=False,
    )
    # M1 non-trivial and rising across the slice — pin non-zero on both
    assert on_report.m1_cross_system_share > 0
    assert off_report.m1_cross_system_share > 0
    # M2 non-zero on the ON run (a director release happened)
    assert on_report.m2_hooks_fired_ratio > 0
    # M3 mean ≥ 2 (no 'one event, then another' failure)
    assert on_report.m3_mean >= 2.0
    assert off_report.m3_mean >= 2.0
    # M5 non-zero OFF (the world is not player-centered)
    assert off_report.m5_non_pc_share > 0
    # render both for the worklog evidence
    assert "events=" in render_report(on_report, director_on=True)
    assert "events=" in render_report(off_report, director_on=False)
