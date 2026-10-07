"""occ-1 acceptance — the whole-arm OCC window fix (the STATUS Next
item (1), B7's letter: every read surface index-based, never a log
scan; the row iter-335/336/337's NEXT lines named behind H9):

THE INDEX-BASED WINDOW ATTRIBUTION. The whole protocol's
deferred-realize law holds completions to the horizon's end, so the
OCC attribution window [seq, end) is horizon-long and the per-event
re-check walk was the measured wall (occ_refold, 81.7% of the whole
100y profiled wall, iter-335). The Simulator now maintains a WRITE
INDEX — (entity, prop) -> every committed write's event index, the
`_last_change` pattern's full-history form — and the walk visits
ONLY the window events that write a pair the intent's attributable
tests can read (`precondition_read_pairs`, the twin table in
core/intent.py). The index law: a test's verdict is a function of
its read pairs' values, so no other event can flip it.

THE FALSIFIER IS THE A/B ATTRIBUTION-EQUIVALENCE LAW (this file's
first law): every answer the loop's index path gives equals the
exact full walk's answer over the same call — plus the byte-identity
A/B (the stripped call re-pins the loop-level composition), the
twin-completeness table law, the twin-agreement property over every
committed pack's every action, the resume rebuild, and the unit grid
(break / no-break / break-at-snapshot / repair-then-re-break).
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path
from typing import Any

from core import loop as loop_module
from core.fold import initial_projection
from core.intent import (
    OCC_READ_PAIRS,
    PRECONDITION_TESTS,
    STATIC_TESTS,
    WINDOWED_TESTS,
    IntentData,
    first_failing,
    occ_breaking_cause,
    precondition_read_pairs,
)
from core.log import EventRecord, LoggedKnowledgeRecord, StateChange
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from labrunner import _anchor_steps  # noqa: E402

FARSTEAD = load_pack(REPO / "content" / "farstead_pack")
TAVERN = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

SQUARE = "loc_square"

PACKS = tuple(
    load_pack(REPO / "content" / name)
    for name in (
        "tavern_pack", "province_pack", "farstead_pack",
        "pressure_pack", "road_pack", "grim_pack",
    )
)


def _steps(years: int, protocol: str) -> list[dict[str, object]]:
    """The player-absent step list in the Lab's own law-2 form: the
    anchor move first when the player does not start there (the
    player at loc_road scopes the beats to the road's thin scene —
    the Lab's anchored square is where the living world is; the
    anchor form is the shape the OCC calls actually fire on)."""
    return _anchor_steps(FARSTEAD, years, SQUARE, protocol=protocol)


def _run(
    tmp: Path, name: str, *, seed: int, years: int, protocol: str,
) -> tuple[Simulator, Path]:
    log = tmp / f"occ_{name}.jsonl"
    sim = Simulator(FARSTEAD, seed, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps(_steps(years, protocol))
    sim.close()
    return sim, log


def _write_index(events: list[EventRecord]) -> dict[tuple[str, str], list[int]]:
    """The unit laws' hand-built twin of the Simulator's `_occ_index`."""
    index: dict[tuple[str, str], list[int]] = {}
    for position, event in enumerate(events):
        for change in event.state_changes:
            index.setdefault((change.entity, change.prop), []).append(position)
    return index


# -- law 1: THE A/B ATTRIBUTION-EQUIVALENCE LAW (the row's falsifier) ----------


def test_the_ab_attribution_equivalence_law(tmp_path: Path) -> None:
    """Every attribution the loop's index path makes equals the exact
    full walk's answer over the SAME call (the stripped re-invocation
    — no snapshot shortcut, no index, the pre-occ-1 semantics). Both
    wait protocols: whole (the horizon-long window — the row's own
    shape) and segmented (the living world's short windows). The
    battery is NON-VACUOUS: calls > 0, attributed answers > 0, and on
    the whole arm the index path inspects STRICTLY fewer events than
    the window holds — a green pair with zero calls proves nothing."""
    real_occ = loop_module.occ_breaking_cause
    calls = {"n": 0, "attributed": 0, "windows": 0}

    def spy(
        pack: Any, events: list[EventRecord], seq: int, intent: IntentData,
        initial: Any, world: Any = None, **kwargs: Any,
    ) -> str | None:
        answer = real_occ(
            pack, events, seq, intent, initial, world=world, **kwargs
        )
        full = real_occ(pack, events, seq, intent, initial, world=world)
        assert answer == full, (
            f"the index walk DIVERGED: index={answer!r} full={full!r} "
            f"seq={seq} kind={intent.kind}"
        )
        calls["n"] += 1
        calls["attributed"] += answer is not None
        calls["windows"] += max(0, len(events) - seq)
        return answer

    loop_module.occ_breaking_cause = spy
    try:
        stats_by_arm = {}
        for protocol in ("whole", "segmented"):
            sim, _ = _run(tmp_path, f"eq_{protocol}", seed=7, years=2,
                          protocol=protocol)
            stats_by_arm[protocol] = sim.occ_stats
    finally:
        loop_module.occ_breaking_cause = real_occ
    assert calls["n"] > 0, "the equivalence pair is vacuous — no OCC call fired"
    assert calls["attributed"] > 0, "no attribution was ever made"
    whole = stats_by_arm["whole"]
    assert whole["calls"] > 0 and whole["attributed"] > 0
    assert whole["window"] > whole["inspected"], (
        "the index path never skipped an event on the whole arm — the "
        "acceleration is vacuous (pin a shape where it does)"
    )


def test_the_ab_byte_identity_law(tmp_path: Path) -> None:
    """The loop-level composition: the same (seed, step list) with the
    index ride ARMED and STRIPPED (changes/stats popped — the exact
    pre-occ-1 walk) commits byte-identical logs. The attribution
    answers ride the rejections' cause chains, so equal answers are
    equal bytes — the law re-pins the composition the per-call law
    decomposes."""
    real_occ = loop_module.occ_breaking_cause

    def stripped(*args: Any, **kwargs: Any) -> str | None:
        kwargs.pop("changes", None)
        kwargs.pop("stats", None)
        return real_occ(*args, **kwargs)

    _, log_armed = _run(tmp_path, "bytes_armed", seed=7, years=2,
                        protocol="whole")
    loop_module.occ_breaking_cause = stripped
    try:
        _, log_stripped = _run(tmp_path, "bytes_stripped", seed=7, years=2,
                               protocol="whole")
    finally:
        loop_module.occ_breaking_cause = real_occ
    assert log_armed.read_bytes() == log_stripped.read_bytes(), (
        "the index ride DIVERGED the canon"
    )


# -- law 2: THE TWIN-COMPLETENESS TABLE LAW -------------------------------------


def test_the_read_pair_table_completeness_law() -> None:
    """Every name in the closed test vocabulary is EXACTLY ONE of: a
    table entry (declares its read pairs), a static name (reads no
    projection pair), or a windowed name (never attributed). A new
    test that reads the projection must declare its pairs in
    OCC_READ_PAIRS — never neither, never two."""
    table = set(OCC_READ_PAIRS)
    static = set(STATIC_TESTS)
    windowed = set(WINDOWED_TESTS)
    vocabulary = set(PRECONDITION_TESTS)
    assert table | static | windowed == vocabulary, (
        "a precondition test escapes the read-set twin — declare its "
        "pairs or its staticness"
    )
    assert not (table & static), "a test is both reading and static"
    assert not (table & windowed), "a test is both reading and windowed"
    assert not (static & windowed), "a test is both static and windowed"


# -- law 3: THE TWIN-AGREEMENT PROPERTY LAW -------------------------------------


def _mutate(value: Any, rng: random.Random, pool: list[str]) -> Any:
    """A far value for a non-read pair: the property must survive any
    value the pair could hold (ints drift, strings become other real
    ids, flags flip, lists empty or fill, None becomes a name)."""
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + rng.choice((-999, -1, 1, 999))
    if isinstance(value, str):
        return rng.choice(pool)
    if isinstance(value, list):
        return [] if value else ["zzz"]
    if value is None:
        return rng.choice(pool)
    return value


def _candidate_target(pack: Any) -> str | None:
    """A resolvable target: the property only needs the noun to
    RESOLVE (the verdict may pass or fail — both sides of the pair
    answer through the same resolution)."""
    for group in ("locations", "npcs", "items", "ambient_entities", "groups"):
        records = pack.entities.get(group, ())
        if records:
            return str(records[0]["id"])
    return None


def test_the_twin_agreement_property_law() -> None:
    """The over-approximation itself: for every committed pack's every
    action's every attributable cond, two projections that AGREE on
    the declared read pairs but are mutated everywhere else answer
    `first_failing` identically — the read-set table covers every
    projection read the test family makes (a missed pair would flip a
    verdict under a mutation it forgot to declare)."""
    rng = random.Random(2026)
    for pack in PACKS:
        base = initial_projection(pack.entities)
        pool = [
            str(record["id"])
            for group in ("locations", "npcs", "ambient_entities", "items")
            for record in pack.entities.get(group, ())
        ]
        actor = str(pack.entities["npcs"][0]["id"])
        actions = pack.data["actions.json"]["actions"]
        exercised = 0
        for action in actions:
            cond_lists: list[list[dict[str, Any]]] = []
            needs_target = any(
                value == "target"
                for cond in action.get("requires", ())
                for value in cond.values()
            )
            target = _candidate_target(pack) if needs_target else None
            intent = IntentData(
                id="intent_0000", kind=action["intent"], actor=actor,
                target=target, fields={},
            )
            cond_lists.append(list(action.get("requires", ())))
            texture_block = action.get("texture")
            texture_intent: IntentData | None = None
            if texture_block is not None:
                reference = {
                    "entry": "tex_0000",
                    "scope": f"entity:{actor}",
                    "slot": "slot", "value": "value",
                }
                texture_intent = IntentData(
                    id="intent_0001", kind=action["intent"], actor=actor,
                    target=None, fields={"texture": reference},
                )
                cond_lists.append(list(texture_block.get("requires", ())))
            for position, conds in enumerate(cond_lists):
                attributable = [
                    cond for cond in conds
                    if cond.get("test") not in WINDOWED_TESTS
                    # the canon arm carries no texture reference, so its
                    # conds cannot reference the texture noun; the TEXTURE
                    # arm carries one and resolves it (texture_scope_target)
                    and not (position == 0 and "texture" in cond.values())
                ]
                if not attributable:
                    continue
                the_intent = intent if position == 0 else texture_intent
                assert the_intent is not None
                pairs = precondition_read_pairs(pack, the_intent, attributable)
                exercised += 1
                keys = [
                    (entity, prop)
                    for entity, props in base.items()
                    for prop in props
                    if (entity, prop) not in pairs
                ]
                assert keys, (
                    f"{pack.name}:{action['intent']} — no mutable surface "
                    "outside the read set (the property would be vacuous)"
                )
                for _ in range(12):
                    mutated = {
                        entity: dict(props)
                        for entity, props in base.items()
                    }
                    for entity, prop in rng.sample(keys, k=min(len(keys), 6)):
                        mutated[entity][prop] = _mutate(
                            mutated[entity][prop], rng, pool
                        )
                    assert first_failing(
                        pack, base, the_intent, attributable
                    ) == first_failing(
                        pack, mutated, the_intent, attributable
                    ), (
                        f"{pack.name}:{action['intent']} — a mutation OUTSIDE "
                        f"the declared read set flipped a verdict: the twin "
                        f"table misses a read pair"
                    )
        assert exercised > 0, f"{pack.name}: no attributable conds found"


# -- law 4: THE RESUME REBUILD LAW ----------------------------------------------


def test_the_resume_rebuild_law(tmp_path: Path) -> None:
    """Resume rebuilds the write index from the log — the `_commit`
    form's exact twin (same pairs, same ascending indices) — and the
    RESUMED segment's attribution is byte-transparent: the same
    split-resume form with the index ride ARMED and STRIPPED commits
    byte-identical logs, with the walk non-vacuous through the resume
    boundary (calls > 0 — the rebuilt index is the one doing the
    attributing).

    NOT asserted here: split-vs-uninterrupted byte identity — the
    farstead split-after-a-wait boundary diverges by a PRE-EXISTING
    drain semantics (the resumed segment's clock pins the post-drain
    tick, 16 past the wait's completion; KI#114, found by this law's
    first draft, reproduced with occ-1 fully stripped — never this
    row's surface)."""
    steps = _steps(2, "segmented")  # [anchor move?, wait 1y, wait 1y]
    assert len(steps) == 3, "the farstead anchor move rides first"
    from core.cursor import cursor_path, load_cursor, save_cursor

    def split_resume(name: str) -> tuple[bytes, dict[str, int], Simulator]:
        log = tmp_path / f"resume_{name}.jsonl"
        sim2 = Simulator(FARSTEAD, 7, log, SCHEMA, commit="0000000")
        sim2.open()
        sim2.run_steps([dict(step) for step in steps[:2]])  # type: ignore[arg-type]
        cursor = sim2.export_cursor(director_enabled=False)
        sim2.close()
        save_cursor(cursor_path(log), cursor)
        sim3 = Simulator.resume(
            FARSTEAD, log, SCHEMA, load_cursor(cursor_path(log))
        )
        sim3.run_steps([dict(step) for step in steps[2:]])  # type: ignore[arg-type]
        sim3.close()
        return log.read_bytes(), sim3.occ_stats, sim3

    real_occ = loop_module.occ_breaking_cause

    def stripped(*args: Any, **kwargs: Any) -> str | None:
        kwargs.pop("changes", None)
        kwargs.pop("stats", None)
        return real_occ(*args, **kwargs)

    armed_bytes, armed_stats, armed_sim = split_resume("armed")
    loop_module.occ_breaking_cause = stripped
    try:
        stripped_bytes, _, _ = split_resume("stripped")
    finally:
        loop_module.occ_breaking_cause = real_occ
    assert armed_bytes == stripped_bytes, (
        "the rebuilt index DIVERGED the resumed canon"
    )
    assert armed_stats["calls"] > 0, (
        "the resumed segment never walked — the law is vacuous on this shape"
    )
    # the rebuild itself: the index equals the log's own write history,
    # folded independently here (same pairs, same ascending indices)
    rebuilt: dict[tuple[str, str], list[int]] = {}
    for position, event in enumerate(armed_sim._events):  # noqa: SLF001 -- the law's own read
        for change in event.state_changes:
            rebuilt.setdefault((change.entity, change.prop), []).append(position)
    assert armed_sim._occ_index == rebuilt  # noqa: SLF001 -- the law's own read


# -- law 5: THE UNIT GRID (the walk's own shapes) --------------------------------


def _event(event_id: str, t: int, cause: str | None,
           changes: tuple[StateChange, ...]) -> EventRecord:
    return EventRecord(
        id=event_id, t=t, type="wait", actor="pc_01", cause=cause, outcome={},
        knowledge=(LoggedKnowledgeRecord(who="x", channel="saw",
                                         fidelity="exact", knows="k",
                                         at=t, source=event_id),),
        state_changes=changes, hooks=(), importance="low",
        provenance={"seed": 1}, target=None,
    )


def _both_ways(
    events: list[EventRecord], seq: int, intent: IntentData,
) -> tuple[str | None, str | None]:
    """The A/B pair at unit scale: the index path (hand-built index,
    the fold-from-initial start) vs the exact full walk."""
    initial = initial_projection(TAVERN.entities)
    indexed = occ_breaking_cause(
        TAVERN, events, seq, intent, initial, changes=_write_index(events)
    )
    full = occ_breaking_cause(TAVERN, events, seq, intent, initial)
    return indexed, full


def _steal_intent(seq: int, target: str = "npc_guard_01") -> IntentData:
    return IntentData(
        id="intent_0001", kind="steal", actor="pc_01", target=target,
        fields={}, based_on_event_seq=seq,
    )


def test_the_unit_grid_break_at_a_writer() -> None:
    """(a) The classic: the target walks away mid-window — the move is
    a read-pair writer, the answer is the move, both paths agree."""
    events = [
        _event("ev_0000", 0, None,
               (StateChange("pc_01", "position", "loc_street", "loc_tavern"),)),
        _event("ev_0001", 2, "ev_0000",
               (StateChange("npc_guard_01", "position", "loc_tavern",
                            "loc_street"),)),
        _event("ev_0002", 4, "ev_0001", ()),
    ]
    indexed, full = _both_ways(events, 1, _steal_intent(1))
    assert indexed == full == "ev_0001"


def test_the_unit_grid_no_break() -> None:
    """(b) Nothing breaks (the guard stays): both paths answer None."""
    events = [
        _event("ev_0000", 0, None,
               (StateChange("pc_01", "position", "loc_street", "loc_tavern"),)),
        _event("ev_0001", 2, "ev_0000", ()),
    ]
    indexed, full = _both_ways(events, 1, _steal_intent(1))
    assert indexed is None and full is None


def test_the_unit_grid_break_at_snapshot() -> None:
    """(c) The verdict ALREADY fails at the walk's start and the first
    window event is not a read-pair writer: the full walk answers the
    FIRST window event's id (its check fires after applying it), and
    the shortcut branch answers exactly that — never None."""
    events = [
        # pc walks away from the guard's room before the proposal (the
        # verdict already fails at the window's start: pc at the
        # backyard, the guard at the tavern)
        _event("ev_0000", 0, None,
               (StateChange("pc_01", "position", "loc_street", "loc_backyard"),)),
        # an unrelated mid-window write (the maid's seeded fatigue)
        _event("ev_0001", 2, "ev_0000",
               (StateChange("npc_maid_01", "status.fatigue", 20, 60),)),
        _event("ev_0002", 4, "ev_0001", ()),
    ]
    intent = IntentData(
        id="intent_0002", kind="steal", actor="pc_01",
        target="npc_guard_01", fields={}, based_on_event_seq=1,
    )
    indexed, full = _both_ways(events, 1, intent)
    assert indexed == full == "ev_0001"


def test_the_unit_grid_repair_then_rebreak() -> None:
    """(d) The nastiest shape: the verdict fails at the start, the
    FIRST WINDOW EVENT (a writer AT seq) REPAIRS it, a later writer
    breaks it again — the answer is the LATER writer on both paths
    (the shortcut must not fire when the first window event is itself
    a writer; the repair proves the loop, not the shortcut, ran)."""
    events = [
        # pc walks away from the guard before the proposal (fails at
        # the window's start: pc at the backyard, the guard at the
        # tavern)
        _event("ev_0000", 0, None,
               (StateChange("pc_01", "position", "loc_street", "loc_backyard"),)),
        # the repair AT seq: pc walks INTO the guard's tavern
        _event("ev_0001", 2, "ev_0000",
               (StateChange("pc_01", "position", "loc_backyard", "loc_tavern"),)),
        # a non-writer between the repair and the re-break
        _event("ev_0002", 4, "ev_0001",
               (StateChange("npc_maid_01", "status.fatigue", 20, 60),)),
        # the re-break: pc leaves again — the ANSWER
        _event("ev_0003", 6, "ev_0002",
               (StateChange("pc_01", "position", "loc_tavern", "loc_backyard"),)),
    ]
    intent = IntentData(
        id="intent_0003", kind="steal", actor="pc_01",
        target="npc_guard_01", fields={}, based_on_event_seq=1,
    )
    indexed, full = _both_ways(events, 1, intent)
    assert indexed == full == "ev_0003"


def test_the_unit_grid_empty_window() -> None:
    """(e) An empty window (seq == len(events)) with a failing verdict:
    both paths answer None — the shortcut's out-of-window guard is
    exact, never an IndexError."""
    events = [
        _event("ev_0000", 0, None,
               (StateChange("pc_01", "position", "loc_street", "loc_backyard"),)),
    ]
    intent = IntentData(
        id="intent_0004", kind="steal", actor="pc_01",
        target="npc_guard_01", fields={}, based_on_event_seq=1,
    )
    indexed, full = _both_ways(events, 1, intent)
    assert indexed is None and full is None


def test_the_unit_grid_static_conds_read_nothing() -> None:
    """The static family declares no read pairs: a cond list of only
    static tests answers an EMPTY read set (the walk's shortcut path —
    candidates can never exist, the verdict decides at the start)."""
    intent = IntentData(
        id="intent_0005", kind="steal", actor="pc_01",
        target="npc_guard_01", fields={},
    )
    conds = [
        {"noun": "target", "test": "kind", "is": "npc"},
        {"noun": "target", "test": "has_field", "field": "position"},
    ]
    assert precondition_read_pairs(TAVERN, intent, conds) == frozenset()
