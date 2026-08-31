"""iter-6 acceptance — the metrics module (`docs/TEST_PLAN.md` §2,
`MVP_SCOPE.md` §15). M1–M5 + the emergent-chain count as pure functions
of `(events, projection)`. The balance harness (`scripts/balance_harness.py`)
calls these across 1000 seed-varied runs; the T8 A/B test computes M5 on
the OFF run, M2 on the ON run.

The metric is the Mesa `DataCollector` inverted: no per-event hook into
the simulator — the simulator emits, the metric reads, the simulator
never knows a metric exists (L3 — derive-never-store).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.fold import fold, initial_projection
from core.log import EventRecord, LoggedKnowledgeRecord, StateChange
from core.metrics import (
    emergent_chains,
    eventless_beat_stretches,
    m1_cross_system_share,
    m2_hooks_fired_ratio,
    m3_causal_chain_lengths,
    m4_novelty_repetition,
    m5_non_pc_share,
    metrics_report,
    render_report,
    systems_touched,
)
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PLAYER = PACK.player_id()


def _ev(
    eid: str, t: int, etype: str, actor: str, cause: str | None,
    *, target: str | None = None, hooks: tuple[str, ...] = (),
    state_changes: tuple[StateChange, ...] = (),
    knowledge: tuple[LoggedKnowledgeRecord, ...] = (),
    importance: str = "low", cause_intent: str | None = None,
) -> EventRecord:
    prov: dict[str, Any] = {"seed": 42}
    if cause_intent is not None:
        prov["cause_intent"] = cause_intent
    return EventRecord(
        id=eid, t=t, type=etype, actor=actor, cause=cause,
        outcome={}, knowledge=knowledge, state_changes=state_changes,
        hooks=hooks, importance=importance, provenance=prov, target=target,
    )


# -- M1 — cross-system share -------------------------------------------------


def test_m1_zero_when_no_multi_system_events() -> None:
    events = [
        _ev("ev_0000", 0, "wait", "pc_01", None),  # time only
        _ev("ev_0001", 1, "wait", "pc_01", "ev_0000"),
    ]
    assert m1_cross_system_share(PACK.rules, events) == 0.0


def test_m1_one_when_every_event_touches_many_systems() -> None:
    events = [
        _ev(
            "ev_0000", 0, "steal", "pc_01", None,
            state_changes=(
                StateChange("npc_guard_01", "relations.suspicion", 0, 25),
                StateChange("pc_01", "position", "loc_street", "loc_tavern"),
            ),
            knowledge=(
                LoggedKnowledgeRecord(
                    "npc_guard_01", "saw", "partial",
                    "figure_reaching_for_purse", 0, "ev_0000"
                ),
            ),
        ),
    ]
    # steal touches crime_watch + position_visibility + knowledge (per pack);
    # plus the state_changes add relations (suspicion) + position. Multi.
    assert m1_cross_system_share(PACK.rules, events) == 1.0


def test_m1_counted_from_pack_data_only() -> None:
    """An event with no pack classification for its type still counts its
    state_change contributions (the type-side just contributes nothing)."""
    events = [
        _ev(
            "ev_0000", 0, "unknown_type", "pc_01", None,
            state_changes=(
                StateChange("pc_01", "position", "loc_a", "loc_b"),
                StateChange("pc_01", "status.fatigue", 0, 5),
            ),
        ),
    ]
    # position → position_visibility; status.fatigue → states. Multi.
    assert m1_cross_system_share(PACK.rules, events) == 1.0


def test_systems_touched_handles_unknown_props_gracefully() -> None:
    event = _ev(
        "ev_0000", 0, "wait", "pc_01", None,
        state_changes=(StateChange("pc_01", "unknown_prop", "a", "b"),),
    )
    # wait → ["time"]; the unknown prop contributes nothing
    assert systems_touched(PACK.rules, event) == frozenset({"time"})


# -- M2 — deferred hooks fired -----------------------------------------------


def test_m2_zero_when_no_hooks_seeded() -> None:
    events = [_ev("ev_0000", 0, "wait", "pc_01", None, hooks=())]
    assert m2_hooks_fired_ratio(events) == 0.0


def test_m2_zero_when_hooks_seeded_but_none_released() -> None:
    events = [
        _ev("ev_0000", 0, "steal", "pc_01", None, hooks=("guard_suspicious_of_pc",)),
        _ev("ev_0001", 1, "wait", "pc_01", "ev_0000"),
    ]
    assert m2_hooks_fired_ratio(events) == 0.0


def test_m2_one_when_every_seeded_hook_released() -> None:
    events = [
        _ev("ev_0000", 0, "steal", "pc_01", None, hooks=("guard_suspicious_of_pc",)),
        _ev(
            "ev_0001", 100, "document_check", "npc_guard_01", "ev_0000",
            cause_intent="director_0000",
        ),
    ]
    # 1 released / 1 seeded = 1.0
    assert m2_hooks_fired_ratio(events) == 1.0


def test_m2_counts_multi_hook_events_as_multi_seeded() -> None:
    events = [
        _ev(
            "ev_0000", 0, "pickpocket_failed", "pc_01", None,
            hooks=("guard_suspicious_of_pc", "possible_document_check"),
        ),
        _ev(
            "ev_0001", 100, "document_check", "npc_guard_01", "ev_0000",
            cause_intent="director_0000",
        ),
    ]
    # 1 released / 2 seeded (one event seeded 2 hooks) = 0.5
    assert m2_hooks_fired_ratio(events) == 0.5


# -- M3 — causal chain length ------------------------------------------------


def test_m3_zero_depth_for_chain_root() -> None:
    events = [_ev("ev_0000", 0, "wait", "pc_01", None)]
    mean, median = m3_causal_chain_lengths(events)
    assert mean == 0.0 and median == 0.0


def test_m3_linear_chain_depths() -> None:
    events = [
        _ev("ev_0000", 0, "wait", "pc_01", None),
        _ev("ev_0001", 1, "wait", "pc_01", "ev_0000"),
        _ev("ev_0002", 2, "wait", "pc_01", "ev_0001"),
    ]
    mean, median = m3_causal_chain_lengths(events)
    assert mean == 1.0  # (0 + 1 + 2) / 3
    assert median == 1.0


def test_m3_branched_chain_walks_each_path() -> None:
    # ev_0002 and ev_0003 both chain back to ev_0001 → ev_0000
    events = [
        _ev("ev_0000", 0, "wait", "pc_01", None),
        _ev("ev_0001", 1, "wait", "pc_01", "ev_0000"),
        _ev("ev_0002", 2, "wait", "npc_drunk_01", "ev_0001"),
        _ev("ev_0003", 2, "wait", "npc_maid_01", "ev_0001"),
    ]
    mean, median = m3_causal_chain_lengths(events)
    # depths: 0, 1, 2, 2 → mean = 5/4 = 1.25
    assert mean == 1.25
    assert median == 1.5


# -- M4 — novelty / repetition -----------------------------------------------


def test_m4_no_repetition_in_distinct_stream() -> None:
    events = [
        _ev("ev_0000", 0, "move", "pc_01", None),
        _ev("ev_0001", 1, "steal", "pc_01", "ev_0000"),
        _ev("ev_0002", 2, "wait", "pc_01", "ev_0001"),
    ]
    rep, distinct = m4_novelty_repetition(events)
    assert rep == 0.0
    # no knowledge records → distinct_knows_share is 0.0
    assert distinct == 0.0


def test_m4_repetition_rate_counts_repeated_bigrams() -> None:
    # the same (move, pc_01) → (wait, pc_01) bigram twice
    events = [
        _ev("ev_0000", 0, "move", "pc_01", None),
        _ev("ev_0001", 1, "wait", "pc_01", "ev_0000"),
        _ev("ev_0002", 2, "move", "pc_01", "ev_0001"),
        _ev("ev_0003", 3, "wait", "pc_01", "ev_0002"),
    ]
    rep, _ = m4_novelty_repetition(events)
    # 2 distinct bigrams; (move→wait, pc) appears twice → repeated = 1
    # repetition_rate = 1 / 2 = 0.5
    assert rep == 0.5


def test_m4_distinct_knows_share_counts_unique_tokens() -> None:
    kr = [
        LoggedKnowledgeRecord("npc_01", "saw", "partial", "token_a", 0, "ev_0000"),
        LoggedKnowledgeRecord("npc_02", "heard", "vague", "token_a", 0, "ev_0000"),
        LoggedKnowledgeRecord("npc_03", "told", "vague", "token_b", 0, "ev_0001"),
    ]
    events = [
        _ev("ev_0000", 0, "steal", "pc_01", None, knowledge=kr[:2]),
        _ev("ev_0001", 1, "rumor_told", "npc_drunk_01", "ev_0000", knowledge=kr[2:]),
    ]
    _, distinct = m4_novelty_repetition(events)
    # 3 records, 2 distinct tokens → 2/3
    assert distinct == 2 / 3


# -- M5 — non-PC event share -------------------------------------------------


def test_m5_zero_when_only_player_acts() -> None:
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 1, "wait", PLAYER, "ev_0000"),
    ]
    assert m5_non_pc_share(events, PLAYER) == 0.0


def test_m5_one_when_no_player_events() -> None:
    events = [
        _ev("ev_0000", 0, "wait", "npc_drunk_01", None),
        _ev("ev_0001", 1, "wait", "npc_maid_01", "ev_0000"),
    ]
    assert m5_non_pc_share(events, PLAYER) == 1.0


def test_m5_world_actor_counts_as_non_pc() -> None:
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 1, "fire_started", "world", "ev_0000"),
    ]
    assert m5_non_pc_share(events, PLAYER) == 0.5


# -- emergent chains (T8) -----------------------------------------------------


def test_emergent_chain_walks_back_to_player_root() -> None:
    events = [
        _ev("ev_0000", 0, "steal", PLAYER, None),  # player root
        _ev("ev_0001", 1, "suspicion_changed", "npc_guard_01", "ev_0000"),
        _ev("ev_0002", 2, "watch_change", "npc_guard_02", "ev_0001"),
        _ev("ev_0003", 3, "knowledge_transfer", "npc_drunk_01", "ev_0002"),
    ]
    chains = emergent_chains(events, PLAYER)
    # ev_0001 (depth 1) — single link, NOT emergent (needs ≥ 2)
    # ev_0002 (depth 2) — chain [suspicion_changed, steal] len 2 — emergent
    # ev_0003 (depth 3) — chain [kt, watch_change, suspicion_changed] len 3 — emergent
    chain_ids = [c[0] for c in chains]
    assert "ev_0001" not in chain_ids  # too short
    assert "ev_0002" in chain_ids
    assert "ev_0003" in chain_ids
    # check lengths
    for cid, length, types in chains:
        if cid == "ev_0002":
            assert length == 2
            assert types == ["watch_change", "suspicion_changed"]
        if cid == "ev_0003":
            assert length == 3
            assert types == ["knowledge_transfer", "watch_change", "suspicion_changed"]


def test_emergent_chain_excludes_director_injected_links() -> None:
    """A chain whose root cause is a director intent is NOT emergent —
    the director injected the consequence, it didn't emerge from the
    world's systems. (D-005 law, T8 single-factor definition.)"""
    events = [
        _ev("ev_0000", 0, "steal", PLAYER, None),
        _ev("ev_0001", 1, "document_check", "npc_guard_01", "ev_0000",
            cause_intent="director_0000"),
        _ev("ev_0002", 2, "suspicion_changed", "npc_guard_01", "ev_0001"),
    ]
    # ev_0001 is director-injected → excluded as a chain tail
    # ev_0002 chains back to ev_0001 (director) → director-injected
    # link breaks the walk → ev_0002 root = None → not emergent
    assert emergent_chains(events, PLAYER) == []


def test_emergent_chain_excludes_world_actor_only_actors() -> None:
    """A chain whose every link is `world`-actor and never reaches a
    player root is not emergent (no player-seeded consequence)."""
    events = [
        _ev("ev_0000", 0, "fire_started", "world", None),  # no cause — world root
        _ev("ev_0001", 1, "fire_spread", "world", "ev_0000"),
        _ev("ev_0002", 2, "smoke_rising", "world", "ev_0001"),
    ]
    # walk from ev_0002 → ev_0001 → ev_0000 (cause None, actor world)
    # root = None (never reached player) → not emergent
    assert emergent_chains(events, PLAYER) == []


def test_emergent_chain_world_root_after_player_seed_is_emergent() -> None:
    """The player drops a lamp (drop_break); the world ignites
    (fire_started, actor=world); the fire spreads (fire_spread). The
    fire_spread → fire_started → drop_break(pc) chain IS emergent —
    the player seeded the consequence, the world acted on it."""
    events = [
        _ev("ev_0000", 0, "drop_break", PLAYER, None),
        _ev("ev_0001", 1, "fire_started", "world", "ev_0000"),
        _ev("ev_0002", 5, "fire_spread", "world", "ev_0001"),
    ]
    chains = emergent_chains(events, PLAYER)
    # ev_0001: walk → drop_break (pc) → root=pc, len 1 (just fire_started)
    #          → NOT emergent (length 1, needs ≥ 2)
    # ev_0002: walk → fire_started → drop_break (pc) → root=pc, len 2
    #          → emergent
    chain_ids = [c[0] for c in chains]
    assert "ev_0001" not in chain_ids  # too short
    assert "ev_0002" in chain_ids
    for cid, length, types in chains:
        if cid == "ev_0002":
            assert length == 2
            assert types == ["fire_spread", "fire_started"]


# -- the one-shot report -----------------------------------------------------


def test_metrics_report_combines_all_metrics() -> None:
    """The metric report combines all five metrics + the emergent-chain
    count. The fold's pre-write gate (D-035) enforces `from_ == current`,
    so the crafted events here use the actual initial projection values
    (the metrics module does not need the projection to compute M1–M5 —
    they all fold the event stream — but the parameter pins the contract).
    """
    events = [
        _ev("ev_0000", 0, "steal", PLAYER, None,
            hooks=("guard_suspicious_of_pc",),
            state_changes=(
                StateChange("npc_guard_01", "relations.suspicion", 0, 25),
                StateChange("pc_01", "position", "loc_street", "loc_tavern"),
            ),
            knowledge=(
                LoggedKnowledgeRecord(
                    "npc_guard_01", "saw", "partial",
                    "figure_reaching", 0, "ev_0000"
                ),
            ),
        ),
        _ev("ev_0001", 100, "document_check", "npc_guard_01", "ev_0000",
            cause_intent="director_0000"),
    ]
    projection = fold(events, initial_projection(PACK.entities))
    report = metrics_report(
        PACK.rules, events, projection, player_id=PLAYER, director_on=True,
    )
    assert report.events == 2
    # both events touch ≥2 systems: steal (crime_watch + position +
    # knowledge, + state_changes add relations) and document_check
    # (director + crime_watch per pack). M1 = 1.0.
    assert report.m1_cross_system_share == 1.0
    assert report.m2_hooks_fired_ratio == 1.0  # 1 released / 1 seeded
    assert report.m3_mean == 0.5  # (0 + 1) / 2
    assert report.m3_median == 0.5
    assert report.m5_non_pc_share == 0.5  # ev_0001 is non-PC
    assert report.emergent_chains == 0  # ev_0001's root is director → not emergent


def test_render_report_formats_all_fields() -> None:
    events = [_ev("ev_0000", 0, "wait", PLAYER, None)]
    # the metric does not fold (projection is reserved); pass the initial
    projection = initial_projection(PACK.entities)
    report = metrics_report(
        PACK.rules, events, projection, player_id=PLAYER, director_on=False,
    )
    text = render_report(report, director_on=False)
    assert "events=1" in text
    assert "M1=" in text
    assert "M2=" in text and "(off)" in text
    assert "M3 mean=" in text
    assert "M4 rep=" in text
    assert "M5=" in text
    assert "emergent_chains=" in text


# -- the gate playscript end-to-end (M-baseline smoke) -----------------------


def test_day1_full_off_run_meets_t8_thresholds() -> None:
    """The T8 gate playscript's OFF run: ≥3 emergent chains and M5 > 0.
    The full numbers go to `worklog.md`; this test pins the gate minimum
    so a regression that drops emergence below the threshold fails loudly.
    """
    from core.log import read_log
    from core.loop import Simulator, load_playscript

    script = load_playscript(REPO / "tests" / "playscripts" / "day1_full.json")
    log = Path("/tmp/csm_metrics_gate.jsonl")
    if log.exists():
        log.unlink()
    sim = Simulator(
        PACK, script["seed"], log, SCHEMA, commit="0000000",
        director_enabled=False,
    )
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    projection = fold(events, initial_projection(PACK.entities))
    report = metrics_report(
        PACK.rules, events, projection, player_id=PLAYER, director_on=False,
    )
    # the T8 gate: ≥3 emergent chains without the director
    assert report.emergent_chains >= 3
    # M5 non-zero at director-off (Kenshi/RimWorld lesson)
    assert report.m5_non_pc_share > 0
    # M3 mean ≥ 2 (one event, then another = failure)
    assert report.m3_mean >= 2.0


# -- eventless beat-stretches (DIR-2, phase 3 — the exit criterion) -----------


def _rules(offsets: list[int], day: int = 1440) -> dict[str, Any]:
    """A minimal rules dict carrying only what the beat axis reads."""
    return {"time": {"ticks_per_day": day}, "urgencies": {"beat_ticks": offsets}}


def test_eventless_stretches_empty_events() -> None:
    assert eventless_beat_stretches(PACK.rules, [], gate="medium") == []


def test_eventless_stretches_no_beats_declared() -> None:
    """A pack without `urgencies.beat_ticks` fires no beats — no windows,
    no stretches (the degenerate config the loop also allows)."""
    events = [_ev("ev_0000", 0, "wait", PLAYER, None)]
    assert eventless_beat_stretches(_rules([]), events, gate="medium") == []
    assert eventless_beat_stretches(
        {"time": {"ticks_per_day": 1440}}, events, gate="medium"
    ) == []


def test_eventless_stretches_none_when_every_window_has_a_scene_event() -> None:
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 50, "take", PLAYER, "ev_0000", importance="medium"),
        _ev("ev_0002", 150, "take", PLAYER, "ev_0001", importance="medium"),
        _ev("ev_0003", 200, "wait", PLAYER, "ev_0002"),  # the log end
    ]
    assert eventless_beat_stretches(_rules([100, 200]), events, gate="medium") == []


def test_eventless_stretches_counts_consecutive_quiet_windows() -> None:
    """The core semantics: a maximal run of consecutive eventless windows
    is one stretch measured in beats."""
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 50, "take", PLAYER, "ev_0000", importance="medium"),
        _ev("ev_0002", 300, "wait", PLAYER, "ev_0001"),  # log end
    ]
    # windows: (0,100] scene at 50; (100,200] quiet; (200,300] quiet → [2]
    assert eventless_beat_stretches(_rules([100, 200, 300]), events, gate="medium") == [2]


def test_eventless_stretches_two_separate_runs() -> None:
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 100, "take", PLAYER, "ev_0000", importance="medium"),
        _ev("ev_0002", 420, "take", PLAYER, "ev_0001", importance="medium"),
        _ev("ev_0003", 500, "wait", PLAYER, "ev_0002"),  # log end
    ]
    # windows: (0,100] scene; (100,200] quiet → 1; (200,300] quiet → 2;
    # (300,400] quiet → 3; (400,500] scene at 420 → recorded [3]
    assert eventless_beat_stretches(_rules([100, 200, 300, 400, 500]), events, gate="medium") == [3]
    # a later scene event splits the quiet run: stretch recorded mid-walk
    events.append(_ev("ev_0004", 320, "take", PLAYER, "ev_0001", importance="medium"))
    # now (300,400] has the scene at 320 → the run [2] closes, then
    # (400,500] has 420 → no trailing quiet → [2]
    assert eventless_beat_stretches(_rules([100, 200, 300, 400, 500]), events, gate="medium") == [2]


def test_eventless_stretches_only_gate_rank_events_break_the_quiet() -> None:
    """The gate law: low-importance bookkeeping (status decay, texture
    waits) never breaks a stretch — the importance rule owns the
    signal/noise split, the metric follows the tale gate."""
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 50, "status_decayed", "npc_guard_01", "ev_0000"),
        _ev("ev_0002", 120, "wait", PLAYER, "ev_0001"),
        _ev("ev_0003", 200, "wait", PLAYER, "ev_0002"),  # log end
    ]
    assert eventless_beat_stretches(_rules([100, 200]), events, gate="medium") == [2]
    # the same events at gate=low: every window has a scene event → []
    assert eventless_beat_stretches(_rules([100, 200]), events, gate="low") == []


def test_eventless_stretches_event_at_the_beat_tick_belongs_to_that_window() -> None:
    """A rotation fired AT the beat tick is that beat's scene — the
    window is (previous_beat, beat], lower bound exclusive."""
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 100, "watch_change", "npc_guard_01", "ev_0000",
            importance="medium"),
        _ev("ev_0002", 200, "wait", PLAYER, "ev_0001"),  # log end
    ]
    # window (0,100] holds the scene at 100; (100,200] quiet → [1]
    assert eventless_beat_stretches(_rules([100, 200]), events, gate="medium") == [1]


def test_eventless_stretches_day_wrapped_beat_axis() -> None:
    """The beat axis repeats daily: the night gap 1080 → 1800 is one
    window, not three; the day boundary multiplies by ticks_per_day."""
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 400, "arson", PLAYER, "ev_0000", importance="high"),
        _ev("ev_0002", 2000, "wait", PLAYER, "ev_0001"),  # log end
    ]
    # beats: 360, 720, 1080, 1800 (2520 > 2000 excluded)
    # windows: (0,360] quiet=1; (360,720] scene 400; (720,1080] quiet=1;
    # (1080,1800] quiet=2 → [1, 2]; trailing (1800,2000] partial — dropped
    assert eventless_beat_stretches(PACK.rules, events, gate="medium") == [1, 2]


def test_eventless_stretches_trailing_partial_window_dropped() -> None:
    """The run ended before the next beat fired — the trailing partial
    window carries no beat evidence and never counts."""
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 250, "wait", PLAYER, "ev_0000"),  # log end
    ]
    # beats ≤ 250: only 100 (the next beat is 1000); window (0,100] quiet
    # → [1]; the trailing (100,250] partial would have made it 2 — dropped
    assert eventless_beat_stretches(_rules([100], day=1000), events, gate="medium") == [1]


def test_eventless_stretches_tick_zero_offset_fires_at_day_boundaries() -> None:
    """The loop's `_first_beat` law: tick 0 is the run start, never a
    beat; a 0 offset fires at day boundaries from day 1 on."""
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 1600, "wait", PLAYER, "ev_0000"),  # log end
    ]
    # beats: 500 (day 0), 1000 (day 1 offset 0), 1500 (day 1 offset 500) —
    # never tick 0; three quiet windows → [3]
    assert eventless_beat_stretches(_rules([0, 500], day=1000), events, gate="medium") == [3]


def test_eventless_stretches_rejects_unknown_gate() -> None:
    events = [_ev("ev_0000", 0, "wait", PLAYER, None)]
    try:
        eventless_beat_stretches(PACK.rules, events, gate="nonsense")
    except ValueError as exc:
        assert "nonsense" in str(exc)
    else:
        raise AssertionError("unknown gate must fail loudly")


def test_eventless_stretches_log_shorter_than_first_beat() -> None:
    """A run that ends before the first beat fires: no beat axis inside
    the log's span — no windows, no stretches."""
    events = [
        _ev("ev_0000", 0, "wait", PLAYER, None),
        _ev("ev_0001", 100, "wait", PLAYER, "ev_0000"),  # log end
    ]
    assert eventless_beat_stretches(PACK.rules, events, gate="medium") == []


def test_day1_full_stretches_are_short() -> None:
    """The exit-criterion family smoke on the gate playscript: the
    committed day1_full seed keeps every eventless stretch ≤ 1 beat (the
    theft ladder hands off to the fire chain inside one beat)."""
    from core.log import read_log
    from core.loop import Simulator, load_playscript

    script = load_playscript(REPO / "tests" / "playscripts" / "day1_full.json")
    log = Path("/tmp/csm_metrics_dir2.jsonl")
    if log.exists():
        log.unlink()
    sim = Simulator(
        PACK, script["seed"], log, SCHEMA, commit="0000000",
        director_enabled=True,
    )
    sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    stretches = eventless_beat_stretches(PACK.rules, events, gate="medium")
    assert max(stretches, default=0) <= 1
