"""iter-330 acceptance — scale-1-impl, the P0.5 pair (the first
byte-identical wall row behind the runtime-promotion gate; CONTRACTS
§9 the law, the rng-1 order's head):

- **P0.5-A (the E04 fix)** — the beat/macro derived folds ride the
  pack's DECLARED gated-entry demand: `_fold_demand`, read once at
  Simulator init from the two spec families' own `requires`, gates
  `_clock_fold_reads`. A pack demanding none (farstead — iter-328's
  measured 5.01 greedy calls/beat vs 0 gated entries) computes ZERO
  of them; a pack demanding them (tavern) computes each ONCE per
  beat/macro tick, shared by the urgency and faction walks (the old
  greedy form paid `live_leverage` and `crystallized_traits` twice
  per beat with provably equal values — no commit between the two
  family calls, so the hoist is value-identical).
- **P0.5-B (the E03 fix)** — the spec families parse ONCE at init
  (`urgency_specs` / `faction_specs`, handed down via `specs=`):
  the per-beat re-parse (2.0 parses/beat, iter-328's counter) is
  gone; the parse is pure, so the memo is byte-identical by
  construction.

The byte-identity law (Q6) is the falsifier: the standing golden T1
corpora (the armed-demand packs) plus the session's cross-version
md5 pair (farstead 2y/10y segmented + province 2y whole, pre-change
references vs post-change logs — equal, recorded in the iter-330
report §B) pin both sides of the demand axis.
"""

from __future__ import annotations

import json
from pathlib import Path

import core.loop as loop_module
from core.factions import faction_specs
from core.loop import Simulator
from core.pack import load_pack
from core.urgencies import urgency_specs

REPO = Path(__file__).resolve().parents[1]
FARSTEAD = load_pack(REPO / "content" / "farstead_pack")
TAVERN = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

#: The windowed-test names (core/intent.py's closed set — the demand
#: vocabulary the fixture asserts read from the families' requires).
LEVERAGE, ECHO, TRAIT = "leverage_over", "echo_at_least", "trait_held"


def _sim(pack, tmp_path: Path, seed: int = 7) -> Simulator:
    log = tmp_path / f"scale1impl_{seed}.jsonl"
    return Simulator(pack, seed, log, SCHEMA, commit="0000000")


def _demand_of(pack) -> frozenset[str]:
    """The fold demand computed the way the loop computes it — over
    both families' requires, intersected with the windowed set (the
    test reads the same memo the clock reads)."""
    specs = (*urgency_specs(pack), *faction_specs(pack))
    return frozenset(
        cond.get("test")
        for spec in specs
        for cond in spec.requires
    ) & {LEVERAGE, ECHO, TRAIT}


def test_the_fold_demand_reads_the_families() -> None:
    """The demand axis itself: farstead declares NO windowed gate
    (the zero-demand side of iter-328's measured pair), tavern
    declares at least one (the armed side) — the two fixtures the
    laziness law runs on."""
    assert _demand_of(FARSTEAD) == frozenset()
    assert _demand_of(TAVERN) != frozenset()


def test_zero_demand_computes_no_clock_folds(tmp_path: Path) -> None:
    """P0.5-A, the zero side: on farstead (zero declared demand) the
    clock path calls NONE of the three derived folds over a real
    multi-beat run — monkeypatched counters over the loop module's
    own bound names, the run otherwise real (the committed log still
    lands; the beat machinery still rolls)."""
    calls = {"leverage": 0, "echo": 0, "traits": 0}
    real = {
        "leverage": loop_module.live_leverage,
        "echo": loop_module.echo_scores,
        "traits": loop_module.crystallized_traits,
    }

    def count(name):
        def wrapper(*args, **kwargs):
            calls[name] += 1
            return real[name](*args, **kwargs)
        return wrapper

    loop_module.live_leverage = count("leverage")
    loop_module.echo_scores = count("echo")
    loop_module.crystallized_traits = count("traits")
    try:
        sim = _sim(FARSTEAD, tmp_path)
        sim.open()
        sim.run_steps([{"intent": "wait", "ticks": 2880}])
        sim.close()
    finally:
        loop_module.live_leverage = real["leverage"]
        loop_module.echo_scores = real["echo"]
        loop_module.crystallized_traits = real["traits"]
    assert sim._writer.event_count > 0  # the world really ran
    assert calls == {"leverage": 0, "echo": 0, "traits": 0}


def test_armed_demand_computes_each_fold_once_per_tick(
    tmp_path: Path,
) -> None:
    """P0.5-A, the armed side + the hoist: on tavern (demand armed)
    every demanded fold is computed by the clock path, and each at
    most once per beat-plus-crossing tick — the old greedy form paid
    live_leverage and crystallized_traits TWICE per beat (once per
    family call); the shared triple halves that without moving a
    byte (the value-identity argument: no commit between the two
    family walks)."""
    assert _demand_of(TAVERN)
    calls = {"leverage": 0, "echo": 0, "traits": 0}
    real = {
        "leverage": loop_module.live_leverage,
        "echo": loop_module.echo_scores,
        "traits": loop_module.crystallized_traits,
    }

    def count(name):
        def wrapper(*args, **kwargs):
            calls[name] += 1
            return real[name](*args, **kwargs)
        return wrapper

    loop_module.live_leverage = count("leverage")
    loop_module.echo_scores = count("echo")
    loop_module.crystallized_traits = count("traits")
    try:
        sim = _sim(TAVERN, tmp_path, seed=42)
        sim.open()
        sim.run_steps([{"intent": "wait", "ticks": 1440}])
        sim.close()
        beats = sim._writer.event_count  # any positive bound suffices
    finally:
        loop_module.live_leverage = real["leverage"]
        loop_module.echo_scores = real["echo"]
        loop_module.crystallized_traits = real["traits"]
    assert beats > 0
    # every demanded fold computed at least once (the demand is live)
    for name in _demand_of(TAVERN):
        key = {
            LEVERAGE: "leverage",
            ECHO: "echo",
            TRAIT: "traits",
        }[name]
        assert calls[key] > 0, name
    # the hoist law: at most ONE clock call per fold per tick — the
    # run's tick span is the wait's ticks plus the run-start tick;
    # doubling (the old per-family recompute) would clear this bar
    # on any multi-beat run
    tick_budget = 1440 + 2
    for key, n in calls.items():
        assert n <= tick_budget, (key, n)


def test_the_specs_memo_parses_once_per_run(
    tmp_path: Path, monkeypatch
) -> None:
    """P0.5-B: the family parses fire at INIT and never again —
    patched counters around the real construction + a multi-beat
    run; the counts stay at their init values (the old form paid
    one urgency + one faction parse per beat — E03's 2.0/beat)."""
    import core.factions as factions_module
    import core.urgencies as urgencies_module

    counts = {"urgency": 0, "faction": 0}
    real_u, real_f = urgencies_module._specs, factions_module._specs

    def count_u(pack):
        counts["urgency"] += 1
        return real_u(pack)

    def count_f(pack):
        counts["faction"] += 1
        return real_f(pack)

    monkeypatch.setattr(urgencies_module, "_specs", count_u)
    monkeypatch.setattr(factions_module, "_specs", count_f)
    sim = _sim(FARSTEAD, tmp_path)
    assert counts == {"urgency": 1, "faction": 1}  # init, once each
    sim.open()
    sim.run_steps([{"intent": "wait", "ticks": 2880}])
    sim.close()
    assert sim._writer.event_count > 0
    assert counts == {"urgency": 1, "faction": 1}  # never re-parsed


# -- iter-331: P1a + P1b (the two quadratic wall members) ----------------------


def _k_event(seq: int, t: int, importance: str, records: list[tuple[str, str]]):
    """One synthetic knowledge-bearing event: `records` as (who, token)
    pairs, all sharing the event's tick and source id (the log's own
    shape — an event's records share its t and source)."""
    from core.log import EventRecord, LoggedKnowledgeRecord

    return EventRecord(
        id=f"ev_{seq:04d}", t=t, type="talk", actor="world", cause=None,
        outcome={}, importance=importance, provenance={}, target=None,
        state_changes=(), hooks=(),
        knowledge=tuple(
            LoggedKnowledgeRecord(
                who=who, channel="saw", fidelity="exact",
                knows=token, at=t, source=f"ev_{seq:04d}",
            )
            for who, token in records
        ),
    )


def _reference_ranked(view, who: str, exclude_source: str | None):
    """The OLD algorithm, kept as the test's oracle: filter then stable
    sort by (importance rank, tick) DESC — the bucket iteration must
    reproduce it EXACTLY (P1b's byte-identity ground)."""
    rows = list(view._rows.get(who, ()))
    if exclude_source is not None:
        rows = [r for r in rows if r.record.source != exclude_source]
    rows.sort(key=lambda r: ({"low": 0, "medium": 1, "high": 2}[r.importance],
                             r.record.at), reverse=True)
    return [r.record for r in rows]


def test_the_bucket_iteration_matches_the_sort(tmp_path: Path) -> None:
    """P1b's order law: over interleaved adds (three ranks, tie ticks,
    multi-record events, re-learned tokens), the rank-bucket iteration
    equals the reference stable sort EXACTLY — with and without an
    excluded source (the tie-run discipline: equal ticks keep arrival
    order, runs emit newest-first, ranks descend)."""
    from core.knowledge import KnowledgeView

    view = KnowledgeView()
    script = [
        (10, "low", [("a", "t1")]),
        (10, "high", [("a", "t2"), ("b", "t3")]),   # a tie tick, two rows
        (20, "high", [("a", "t4")]),
        (20, "medium", [("b", "t5"), ("c", "t6")]),
        (30, "low", [("a", "t1")]),                   # a re-learned token
        (30, "high", [("c", "t7")]),
        (40, "medium", [("a", "t8")]),
        (40, "high", [("b", "t3")]),                  # b re-learns t3
    ]
    for seq, (t, importance, records) in enumerate(script):
        view.add(_k_event(seq, t, importance, records))
    for who in ("a", "b", "c"):
        bucket = list(view._ranked(who, exclude_source=None))
        assert bucket == _reference_ranked(view, who, None), who
        for excluded in ("ev_0001", "ev_0004", "ev_9999"):
            bucket = list(view._ranked(who, exclude_source=excluded))
            assert bucket == _reference_ranked(view, who, excluded), (
                who, excluded,
            )


def test_the_novelty_count_matches_the_walk(tmp_path: Path) -> None:
    """P1b's count law: the (teller, listener) novelty count is EXACTLY
    the number of the teller's rows whose token the listener does not
    hold — zero iff the walk picks nothing (the O(1) short-circuit's
    soundness), positive iff at least one pick exists with no excluded
    source. Late-born knowers included (the birth-initialization law)."""
    from core.knowledge import KnowledgeView, _novel_facts

    view = KnowledgeView()
    script = [
        (10, "high", [("a", "t1"), ("a", "t2")]),
        (10, "medium", [("b", "t3")]),
        (20, "high", [("a", "t3")]),        # a learns b's token
        (30, "low", [("c", "t4")]),         # c born LATE — pre-birth rows
        (40, "high", [("b", "t1")]),        # b learns a's first token
        (50, "medium", [("c", "t1"), ("c", "t2")]),  # c catches up fully
    ]
    for seq, (t, importance, records) in enumerate(script):
        view.add(_k_event(seq, t, importance, records))
    for teller in ("a", "b", "c"):
        for listener in ("a", "b", "c"):
            if teller == listener:
                continue
            unheld = [
                row for row in view._rows.get(teller, ())
                if not view.holds(listener, row.record.knows)
            ]
            count = view._novelty.get(teller, {}).get(listener, 0)
            assert count == len(unheld), (teller, listener, count)
            picks = _novel_facts(
                view, teller, listener, exclude_source="ev_9999", limit=99,
            )
            if count == 0:
                assert picks == [], (teller, listener)
            else:
                assert picks, (teller, listener)


def test_the_occ_snapshot_walk_equals_the_fold(tmp_path: Path) -> None:
    """P1a's equivalence law: a real rejection-heavy run (farstead 10y
    segmented carries ~254 projection_moved rejections, each walking the
    OCC attribution) is byte-identical with the snapshot path DISABLED —
    the loop's start_state stripped, the fold-from-initial restored.
    The cause chains in every rejection event are the oracle."""
    import core.loop as loop_module

    # the Lab protocol's own step list (the anchor move when the
    # player does not stand there — farstead's player starts on the
    # road — then the year-segmented waits; the rejection-heavy arm:
    # the whole protocol's herd dies at the DOOR, projection_moved
    # rides the segmented cadence)
    steps = [
        {"intent": "move", "target": "loc_square"},
        *[{"intent": "wait", "ticks": 518400}] * 10,
    ]
    log_snapshot = tmp_path / "with_snapshot.jsonl"
    sim = Simulator(FARSTEAD, 7, log_snapshot, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(steps)
    sim.close()

    real_occ = loop_module.occ_breaking_cause

    def fold_only(*args, **kwargs):
        kwargs.pop("start_state", None)
        return real_occ(*args, **kwargs)

    loop_module.occ_breaking_cause = fold_only
    try:
        log_fold = tmp_path / "fold_only.jsonl"
        sim = Simulator(FARSTEAD, 7, log_fold, SCHEMA, commit="0000000")
        sim.open()
        sim.run_steps(list(steps))
        sim.close()
    finally:
        loop_module.occ_breaking_cause = real_occ
    assert log_snapshot.read_bytes() == log_fold.read_bytes()
    # the run really exercised the walk (a vacuous equivalence is no
    # law — the rejection count must be material)
    import json as _json
    rejections = sum(
        1 for line in log_snapshot.read_text(encoding="utf-8").splitlines()[1:]
        if _json.loads(line)["type"] == "intent_rejected"
        and _json.loads(line)["outcome"].get("reason") == "projection_moved"
    )
    assert rejections > 50, rejections
