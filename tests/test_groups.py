"""iter-93 acceptance — depth-7, groups & simulation LOD (phases.md §5,
the iter-11b resolutions in the D-112-ratified edition; the STATUS
queue's W2 row after depth-6: the WRITE side of the LOD ladder at
group scale — how off-screen life is represented, how a group becomes
canon when the reader approaches).

The laws pinned here:

- **The population tier** (`core/groups.py::macro_tick_drafts`): a
  group anchored in the COLD zone emits ONE aggregate event per macro
  crossing — actor = the group id (D-112's one id, all tiers), the
  outcome carrying the unborn population's cardinality under
  `population` (the D-112 shape: counts for populations, events for
  notables; log growth O(groups x macrobeats), never O(members x
  ticks)). No knowledge, no state_changes, no hooks — the count is a
  live fold read (L3), and the event draws NOTHING (INV-2-clean by
  construction).
- **The condensation on crossing the warm transition** (D-112 (3) /
  D-116 (9)): a group's anchor entering the WARM ring or the ACTIVE
  scene materializes it — ONE event per group carrying each un-born
  static member's canon birth (`StateChange(member, "member_of",
  None -> group)`, the D-054 promotion shape at group scale: a member
  already holding a value is SKIPPED, never re-birthed) plus the
  group's tombstone marker (`condensed: None -> True`). The
  transition is detected at the zone recomputations — the beats AND
  the crossings, whichever sees the new partition first (the load
  state counts as the origin: a group warm/active at the first
  computation condenses immediately).
- **The tombstone** (the derived store, INV-5 untouched): after the
  condensation the aggregate is realized — `is_condensed` reads the
  marker from the fold and the macro-tick walk stays silent; the
  aggregate events already in the log are never edited.
- **The `member_of` door** (D-020's pair-relation at group scale):
  membership is runtime state — the projection holds no seed for it
  (absence IS None, the D-054 slot shape); the condensation is the
  engine's writer, the fold's `apply_event` validates every
  from-value (a join, a leave, a transfer — INV-1 made executable).
- **The per-group opt-in** (the 68a pattern): a group without
  `macro_event`/`condense_event` is depth-6's intent-door actor alone
  — zero tier machinery, zero events; the committed pack declares no
  groups at all, and a crafted pack carrying the inert vocabulary
  runs the committed corpus scripts BYTE-IDENTICALLY (zero corpus
  price by construction, zero re-pins).
- **The corpus price** (D-108's both-arms law): the armed arm's
  event delta is the tier families ALONE (the condensations + the
  aggregates), the substantive fingerprint EQUAL — the tier events
  are draw-free, so the RngBank never sees them.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

import pytest

from core.fold import fold, initial_projection
from core.groups import (
    MARKER_PROP,
    MEMBER_OF_PROP,
    MEMBERS_KEY,
    POPULATION_KEY,
    condensation_drafts,
    is_condensed,
    macro_tick_drafts,
)
from core.log import StateChange, read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack
from core.rng import RngBank
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

GROUP = "grp_watch"
GROUP_NAME = "the watch"
OTHER = "grp_idle"  # the corpus-price arm's population-only group
OTHER_NAME = "the crowd"
ANCHOR = "loc_guardroom"
MEMBERS = ("npc_guard_01", "npc_guard_02")
OTHER_MEMBERS = ("npc_barkeep_01", "npc_drunk_01")
AGG_EVENT = "watch_counts"
AGG_LINE = "{actor} numbers {population} souls."
COND_EVENT = "watch_musters"
COND_LINE = "{actor} musters {members} strong at {location}."
MACRO_EVENT = "year_turns"
MACRO_LINE = "The year turns to {year}."
CADENCE = 40
WAIT_100: list[dict[str, Any]] = [{"intent": "wait", "ticks": 100}]


def _group_record(
    anchor: str = ANCHOR,
    members: tuple[str, ...] = MEMBERS,
    macro_event: str | None = AGG_EVENT,
    condense_event: str | None = COND_EVENT,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "id": GROUP,
        "name": GROUP_NAME,
        "position": anchor,
        "members": list(members),
        "notes": "the acceptance group (depth-7): the tier vocabulary",
    }
    if macro_event is not None:
        record["macro_event"] = macro_event
    if condense_event is not None:
        record["condense_event"] = condense_event
    return record


def tier_pack(
    tmp_path: Path,
    name: str,
    *,
    groups: list[dict[str, Any]] | None = None,
    macro: Any = False,
) -> tuple[Path, Pack]:
    """A committed-pack copy carrying the depth-7 tier vocabulary (the
    group entity + the template lines; the tier keys are per-group —
    None omits them, the 68a opt-in) plus the optional `time.macro`
    block (False = untouched — the committed pack declares none).
    Returns the pack dir (for post-hoc JSON edits) and the loaded
    pack."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)

    entities = json.loads((target / "entities.json").read_text(encoding="utf-8"))
    entities["groups"] = [_group_record()] if groups is None else groups
    (target / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if macro is not False:
        if macro is None:
            rules["time"].pop("macro", None)
        else:
            rules["time"]["macro"] = macro
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    templates["events"][AGG_EVENT] = AGG_LINE
    templates["events"][COND_EVENT] = COND_LINE
    templates["events"][MACRO_EVENT] = MACRO_LINE
    (target / "templates.json").write_text(
        json.dumps(templates, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target, load_pack(target)


def armed(tmp_path: Path, name: str, **kwargs: Any) -> tuple[Path, Pack]:
    """The deterministic armed arm: the macro clock at cadence 40."""
    kwargs.setdefault("macro", {"cadence_ticks": CADENCE, "event_type": MACRO_EVENT})
    return tier_pack(tmp_path, name, **kwargs)


def _mutated(
    tmp_path: Path, name: str, mutate: Callable[[Path], None], **kwargs: Any
) -> Pack:
    """A crafted pack mutated post-lint-setup (the lint probes)."""
    _base, _pack = tier_pack(tmp_path, f"base_{name}", **kwargs)
    target = tmp_path / name
    shutil.copytree(_base, target)
    mutate(target)
    return load_pack(target)


def _group_mutate(**field: Any) -> Callable[[Path], None]:
    """An entities.json mutator: overwrite one field of the first
    group record (or drop it when the value is DEL)."""
    def mutate(target: Path) -> None:
        entities = json.loads(
            (target / "entities.json").read_text(encoding="utf-8")
        )
        group = entities["groups"][0]
        for key, value in field.items():
            if value is DEL:
                group.pop(key, None)
            else:
                group[key] = value
        (target / "entities.json").write_text(
            json.dumps(entities, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return mutate


DEL = object()


def _run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]], name: str,
) -> tuple[Path, Any]:
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    result = sim.run_playscript(
        {"name": name, "seed": seed, "pack": pack.name_version, "steps": steps}
    )
    sim.close()
    return log, result


def _events(log: Path) -> list[Any]:
    _header, events = read_log(log, SCHEMA)
    return events


def _record(event_id: str, changes: tuple[StateChange, ...]) -> Any:
    """A minimal EventRecord for fold-level door probes (the
    test_core pattern — the state changes are the point)."""
    from core.log import EventRecord

    return EventRecord(
        id=event_id, t=0, type="wait", actor="pc_01", cause=None, outcome={},
        knowledge=(), state_changes=changes, hooks=(), importance="low",
        provenance={"seed": 1}, target=None,
    )


# -- the population tier (the macro-tick aggregates) --------------------------


def test_the_macro_tick_shape(tmp_path: Path) -> None:
    """The D-112 aggregate form: ONE event per cold uncondensed group
    per crossing — actor = the group id (one id, all tiers), the
    outcome ONE flat count under `population`, no knowledge, no state
    changes (L3 — the count is derived), no hooks, the cause left for
    the loop's chronological chain."""
    _dir, pack = tier_pack(tmp_path, "agg_unit")
    projection = initial_projection(pack.entities)
    drafts = macro_tick_drafts(pack, projection, 40, locations=(ANCHOR,))
    assert len(drafts) == 1
    draft = drafts[0]
    assert draft.t == 40
    assert draft.type == AGG_EVENT
    assert draft.actor == GROUP
    assert draft.outcome == {POPULATION_KEY: 2}
    assert draft.cause is None
    assert draft.state_changes == ()
    assert draft.knowledge == ()
    assert draft.hooks == ()
    assert draft.importance == "low"  # a world count — the turn's twin


def test_the_tombstone_gates_the_aggregate(tmp_path: Path) -> None:
    """D-112 (3)'s derived-store tombstone: a condensed group's
    macro-ticks stay silent (the aggregate is realized — INV-5
    untouched, the marker is fold state, never a log edit)."""
    _dir, pack = tier_pack(tmp_path, "tomb_unit")
    projection = initial_projection(pack.entities)
    projection[GROUP][MARKER_PROP] = True
    assert is_condensed(projection, GROUP)
    assert macro_tick_drafts(pack, projection, 40, locations=(ANCHOR,)) == ()


def test_the_zone_filter_scopes_the_aggregate(tmp_path: Path) -> None:
    """The LOD filter: only the caller's zone (the cold background at
    the crossing) ticks — a group anchored elsewhere stays silent."""
    _dir, pack = tier_pack(tmp_path, "zone_unit")
    projection = initial_projection(pack.entities)
    assert macro_tick_drafts(pack, projection, 40, locations=("loc_tavern",)) == ()


def test_the_population_reads_the_live_fold(tmp_path: Path) -> None:
    """L3: the cardinality is a live fold read — a member who joined
    at runtime (`member_of` = the group) left the population; a member
    who transferred to ANOTHER group belongs to neither tier of this
    one; a member who left a runtime membership faded back into it."""
    _dir, pack = tier_pack(tmp_path, "pop_unit")
    projection = initial_projection(pack.entities)
    projection[MEMBERS[0]][MEMBER_OF_PROP] = GROUP
    assert macro_tick_drafts(
        pack, projection, 40, locations=(ANCHOR,)
    )[0].outcome[POPULATION_KEY] == 1
    projection[MEMBERS[1]][MEMBER_OF_PROP] = OTHER  # a transfer out
    assert macro_tick_drafts(
        pack, projection, 40, locations=(ANCHOR,)
    )[0].outcome[POPULATION_KEY] == 0
    projection[MEMBERS[0]][MEMBER_OF_PROP] = None  # a leave: back in
    assert macro_tick_drafts(
        pack, projection, 40, locations=(ANCHOR,)
    )[0].outcome[POPULATION_KEY] == 1  # m0 back, m1 still transferred out


# -- the condensation (the tier transition) ----------------------------------


def test_the_condensation_births_the_members(tmp_path: Path) -> None:
    """The D-054 promotion shape at group scale: ONE event per group
    carrying every un-born member's canon birth (the group's own
    member order — `member_of`: None -> group) plus the tombstone
    marker LAST; the outcome carries the canon membership's size."""
    _dir, pack = tier_pack(tmp_path, "cond_unit")
    projection = initial_projection(pack.entities)
    drafts = condensation_drafts(
        RngBank(42), pack, projection, 40, locations=(ANCHOR,)
    )
    assert len(drafts) == 1
    draft = drafts[0]
    assert draft.type == COND_EVENT
    assert draft.actor == GROUP
    assert draft.outcome == {MEMBERS_KEY: 2}
    assert draft.cause is None
    assert draft.knowledge == ()
    assert draft.state_changes == (
        StateChange(MEMBERS[0], MEMBER_OF_PROP, None, GROUP),
        StateChange(MEMBERS[1], MEMBER_OF_PROP, None, GROUP),
        StateChange(GROUP, MARKER_PROP, None, True),
    )


def test_the_skip_law_never_rebirths(tmp_path: Path) -> None:
    """The D-054 skip law's twin: a member already holding a value is
    SKIPPED — a runtime join counts toward the canon membership
    without a second birth; a member holding ANOTHER group's id
    belongs to neither (not birthed, not counted)."""
    _dir, pack = tier_pack(tmp_path, "skip_unit")
    projection = initial_projection(pack.entities)
    projection[MEMBERS[0]][MEMBER_OF_PROP] = GROUP  # a runtime join
    projection[MEMBERS[1]][MEMBER_OF_PROP] = OTHER  # a transfer out
    drafts = condensation_drafts(
        RngBank(42), pack, projection, 40, locations=(ANCHOR,)
    )
    assert len(drafts) == 1
    draft = drafts[0]
    assert draft.state_changes == (
        StateChange(GROUP, MARKER_PROP, None, True),
    )
    assert draft.outcome == {MEMBERS_KEY: 1}  # the join alone is canon


def test_the_marker_is_write_once(tmp_path: Path) -> None:
    """A condensed group never condenses again (the tier transition
    is one event — the second zone computation sees the marker and
    stays silent)."""
    _dir, pack = tier_pack(tmp_path, "once_unit")
    projection = initial_projection(pack.entities)
    first = condensation_drafts(
        RngBank(42), pack, projection, 40, locations=(ANCHOR,)
    )
    assert len(first) == 1
    for change in first[0].state_changes:  # fold the event (T2 discipline)
        projection[change.entity][change.prop] = change.to_
    assert condensation_drafts(
        RngBank(42), pack, projection, 80, locations=(ANCHOR,)
    ) == ()


def test_the_opt_in_law_per_group(tmp_path: Path) -> None:
    """The 68a pattern per group: without the keys the group is
    depth-6's intent-door actor alone — no macro-tick, no
    condensation, zero tier machinery."""
    _dir, pack = tier_pack(
        tmp_path, "opt_unit", groups=[_group_record(macro_event=None, condense_event=None)]
    )
    projection = initial_projection(pack.entities)
    assert macro_tick_drafts(pack, projection, 40, locations=(ANCHOR,)) == ()
    assert condensation_drafts(
        RngBank(42), pack, projection, 40, locations=(ANCHOR,)
    ) == ()


# -- the member_of door (D-020's pair-relation, fold-validated) ---------------


def test_the_member_of_door_validates_through_the_fold() -> None:
    """The runtime membership door: the fold's apply_event validates
    every from-value — a join (the condensation's own birth shape), a
    leave (the member fades back into the population), a transfer;
    a stale birth fails LOUDLY (INV-1 made executable, the D-054 skip
    law's runtime twin)."""
    from core.fold import apply_event

    state = {
        GROUP: {"position": ANCHOR},
        MEMBERS[0]: {"position": "loc_guardroom"},
    }
    apply_event(
        state, _record("ev_0000", (StateChange(MEMBERS[0], MEMBER_OF_PROP, None, GROUP),))
    )
    assert state[MEMBERS[0]][MEMBER_OF_PROP] == GROUP
    apply_event(
        state, _record("ev_0001", (StateChange(MEMBERS[0], MEMBER_OF_PROP, GROUP, None),))
    )
    assert state[MEMBERS[0]][MEMBER_OF_PROP] is None  # the leave: uncarried
    apply_event(
        state, _record("ev_0002", (StateChange(MEMBERS[0], MEMBER_OF_PROP, None, OTHER),))
    )
    assert state[MEMBERS[0]][MEMBER_OF_PROP] == OTHER
    with pytest.raises(ValueError, match="expected from"):
        apply_event(
            state,
            _record("ev_0003", (StateChange(MEMBERS[0], MEMBER_OF_PROP, None, GROUP),)),
        )


# -- the pack lint ------------------------------------------------------------


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (_group_mutate(macro_event="no_such_line"), "template vocabulary"),
        (_group_mutate(condense_event="no_such_line"), "template vocabulary"),
        (_group_mutate(members=[]), "dead data"),
        (_group_mutate(condense_event=AGG_EVENT, members=[]), "dead data"),
        (_group_mutate(crew=[]), r"macro_event \| condense_event"),
    ],
)
def test_the_tier_keys_lint(
    tmp_path: Path, mutate: Callable[[Path], None], message: str
) -> None:
    """The closed vocabulary + the dead-data law: the tier event
    types must live in the template closure (EVENT_SCHEMA §11), and a
    memberless group's tier keys are refused — a population of nobody
    never carries a count and never births (the vacuity law's lint
    arm, the threshold-100 family)."""
    with pytest.raises(PackError, match=message):
        _mutated(tmp_path, "tier_bad", mutate)


# -- the integration (the loop, the zones, the corpus price) ------------------


def test_the_cold_group_aggregates_at_the_crossings(tmp_path: Path) -> None:
    """The population tier live: with the PC inside the tavern and the
    group anchored at the market (COLD), each crossing emits ONE
    aggregate — the count on the outcome, the cause chained to the
    turn that opened the crossing; no condensation ever (the anchor
    never warms), the members never born (the fold holds no
    `member_of` — the population stays abstract)."""
    _dir, pack = armed(tmp_path, "cold_agg", groups=[_group_record(anchor="loc_market")])
    steps = [{"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log, _result = _run(tmp_path, pack, 42, steps, "cold_agg")
    events = _events(log)
    aggregates = [e for e in events if e.type == AGG_EVENT]
    assert [e.t for e in aggregates] == [40, 80]
    for aggregate in aggregates:
        assert aggregate.actor == GROUP
        assert aggregate.outcome == {POPULATION_KEY: 2}  # the group's own
        turn = next(e for e in events if e.type == MACRO_EVENT and e.t == aggregate.t)
        assert aggregate.cause == turn.id
        assert events.index(aggregate) > events.index(turn)
    assert not any(e.type == COND_EVENT for e in events)
    state = fold(events, initial_projection(pack.entities))
    assert MEMBER_OF_PROP not in state[MEMBERS[0]]
    assert not is_condensed(state, GROUP)


def test_the_warm_group_condenses_at_the_first_crossing(tmp_path: Path) -> None:
    """The tier transition live: the PC at the street (the hub) and
    the group anchored at the guardroom (WARM from load) — the FIRST
    crossing materializes the group (the load state is the origin:
    the PC walks into a materialized world), ONE event with the
    births + the marker, cause-chained to the turn; never a second
    condensation, never an aggregate (the anchor was never cold);
    the fold (T2 rebuild) holds the members' canon `member_of`."""
    _dir, pack = armed(tmp_path, "warm_cond")
    log, _result = _run(tmp_path, pack, 42, WAIT_100, "warm_cond")
    events = _events(log)
    condensations = [e for e in events if e.type == COND_EVENT]
    assert len(condensations) == 1
    condensation = condensations[0]
    assert condensation.t == 40
    assert condensation.actor == GROUP
    assert condensation.outcome == {MEMBERS_KEY: 2}
    turn = next(e for e in events if e.type == MACRO_EVENT and e.t == 40)
    assert condensation.cause == turn.id
    assert events.index(condensation) > events.index(turn)
    assert not any(e.type == AGG_EVENT for e in events)
    state = fold(events, initial_projection(pack.entities))
    assert state[MEMBERS[0]][MEMBER_OF_PROP] == GROUP
    assert state[MEMBERS[1]][MEMBER_OF_PROP] == GROUP
    assert is_condensed(state, GROUP)


def test_the_active_group_condenses_too(tmp_path: Path) -> None:
    """The active arm: a group anchored at the PC's own location (the
    ACTIVE scene) condenses at the same first computation — the warm
    ring and the active scene are one transition family (the reader's
    presence region)."""
    _dir, pack = armed(
        tmp_path, "active_cond", groups=[_group_record(anchor="loc_street")]
    )
    log, _result = _run(tmp_path, pack, 42, WAIT_100, "active_cond")
    events = _events(log)
    assert len([e for e in events if e.type == COND_EVENT]) == 1


def test_the_beat_detects_the_transition_when_the_crossing_is_far(
    tmp_path: Path,
) -> None:
    """The second ride point: the zone recomputation at the BEAT — a
    cadence beyond the beat interval means the beat sees the new
    partition first (the one law, two ride points; the load state is
    the origin here too)."""
    _dir, pack = armed(
        tmp_path, "beat_cond",
        macro={"cadence_ticks": 400, "event_type": MACRO_EVENT},
    )
    log, _result = _run(
        tmp_path, pack, 42, [{"intent": "wait", "ticks": 400}], "beat_cond"
    )
    events = _events(log)
    condensations = [e for e in events if e.type == COND_EVENT]
    assert len(condensations) == 1
    assert condensations[0].t == 360  # the beat, before the crossing at 400
    turns = [e for e in events if e.type == MACRO_EVENT]
    assert [e.t for e in turns] == [400]  # the beat saw the partition FIRST
    assert condensations[0].t < turns[0].t
    assert not any(e.type == AGG_EVENT for e in events)


def test_the_tombstone_gates_the_aggregates_after_condensation(
    tmp_path: Path,
) -> None:
    """The full tier story: the PC starts at the street (the group's
    market anchor WARM — the condensation at the first crossing),
    then steps into the tavern (the anchor COLD again) — the
    macro-ticks stay silent for good (the tombstone), while the
    twin WITHOUT the condense key aggregates freely in the same
    window (the tombstone is the delta)."""
    _dir, pack = armed(
        tmp_path, "tomb_run", groups=[_group_record(anchor="loc_market")]
    )
    steps = [*WAIT_100, {"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log, _result = _run(tmp_path, pack, 42, steps, "tomb_run")
    events = _events(log)
    assert len([e for e in events if e.type == COND_EVENT]) == 1
    assert not any(e.type == AGG_EVENT for e in events)  # gated, for good
    # the contrast arm: never condensed -> the cold window aggregates
    _dir2, pack2 = armed(
        tmp_path, "tomb_contrast",
        groups=[_group_record(anchor="loc_market", condense_event=None)],
    )
    log2, _result2 = _run(tmp_path, pack2, 42, steps, "tomb_contrast")
    events2 = _events(log2)
    assert not any(e.type == COND_EVENT for e in events2)
    assert [e.t for e in events2 if e.type == AGG_EVENT] == [120, 160, 200]


def test_determinism(tmp_path: Path) -> None:
    """INV-2: same seed + same script -> byte-identical logs (the
    births, the counts, the cause chains all fold from the same
    inputs; the tier events draw nothing)."""
    _dir, pack = armed(
        tmp_path, "det", groups=[_group_record(anchor="loc_market")]
    )
    steps = [*WAIT_100, {"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log_a, _a = _run(tmp_path, pack, 42, steps, "det_a")
    log_b, _b = _run(tmp_path, pack, 42, steps, "det_b")
    assert log_a.read_bytes() == log_b.read_bytes()


def test_the_corpus_price_is_the_tier_families_alone(tmp_path: Path) -> None:
    """The both-arms measurement (D-108): the armed arm (two groups —
    one condensing, one population-only) vs the twin with the tier
    keys REMOVED (depth-6's form, everything else identical) — the
    event delta the tier families ALONE (the condensations + the
    aggregates), the substantive fingerprint EQUAL (the tier events
    are draw-free), the shared events' (t, type, actor) sequence
    unchanged (the ids renumber through the interleaving; the cause
    chains stay honest to whatever preceded)."""
    groups = [
        {  # the guardroom group: warm from load -> condenses at t=40
            "id": GROUP, "name": GROUP_NAME, "position": ANCHOR,
            "members": list(MEMBERS), "condense_event": COND_EVENT,
        },
        {  # the market group: cold after the move -> the aggregates
            "id": OTHER, "name": OTHER_NAME, "position": "loc_market",
            "members": list(OTHER_MEMBERS), "macro_event": AGG_EVENT,
        },
    ]
    bare = [
        {key: value for key, value in record.items()
         if key not in ("macro_event", "condense_event")}
        for record in groups
    ]
    _dir_a, pack_a = armed(tmp_path, "price_armed", groups=groups)
    _dir_u, pack_u = armed(tmp_path, "price_unarmed", groups=bare)
    steps = [*WAIT_100, {"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log_a, result_a = _run(tmp_path, pack_a, 42, steps, "price_a")
    log_u, result_u = _run(tmp_path, pack_u, 42, steps, "price_u")
    events_a = _events(log_a)
    events_u = _events(log_u)
    assert result_a.fingerprint == result_u.fingerprint
    condensations = [e for e in events_a if e.type == COND_EVENT]
    aggregates = [e for e in events_a if e.type == AGG_EVENT]
    assert len(condensations) == 1
    assert [e.t for e in aggregates] == [120, 160, 200]
    assert len(events_a) == len(events_u) + len(condensations) + len(aggregates)
    shared = [
        (e.t, e.type, e.actor) for e in events_a
        if e.type not in (COND_EVENT, AGG_EVENT)
    ]
    unarmed = [(e.t, e.type, e.actor) for e in events_u]
    assert shared == unarmed


def test_the_unarmed_twin_is_the_committed_bytes(tmp_path: Path) -> None:
    """The zero-price proof (the 68a pattern): a crafted pack carrying
    the INERT depth-7 vocabulary (the group entity with BOTH tier
    keys, the template lines — no `time.macro` block) runs the
    committed corpus scripts BYTE-IDENTICALLY to the committed pack
    itself (the LOD's one-gate law: no armed clock, no zones, no
    tiers — the v0.1 bytes; zero re-pins)."""
    _dir, inert = tier_pack(tmp_path, "inert")
    for script in ("plumbing_smoke", "day1_full"):
        playscript = json.loads(
            (REPO / "tests" / "playscripts" / f"{script}.json").read_text(
                encoding="utf-8"
            )
        )
        _log_c, _r_c = _run(tmp_path, PACK, 42, playscript["steps"], f"c_{script}")
        _log_u, _r_u = _run(
            tmp_path, inert, 42, playscript["steps"], f"u_{script}",
        )
        assert _log_c.read_bytes() == _log_u.read_bytes()


def test_the_tale_renders_the_tier_lines(tmp_path: Path) -> None:
    """The render arm: the aggregate line binds {population}, the
    condensation line binds {members} + the anchor's {location}; the
    group's display name renders as {actor}; the pack's
    story-critical listing decides the tier events' visibility (the
    tune-1 split — the raw score reads both low)."""
    groups = [
        {
            "id": GROUP, "name": GROUP_NAME, "position": ANCHOR,
            "members": list(MEMBERS), "condense_event": COND_EVENT,
        },
        {
            "id": OTHER, "name": OTHER_NAME, "position": "loc_market",
            "members": list(OTHER_MEMBERS), "macro_event": AGG_EVENT,
        },
    ]
    target, _pack = armed(tmp_path, "render", groups=groups)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["importance"]["story_critical_events"] += [COND_EVENT, AGG_EVENT]
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    pack = load_pack(target)
    steps = [*WAIT_100, {"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log, _result = _run(tmp_path, pack, 42, steps, "render")
    events = _events(log)
    chronicle = render_chronicle(events, pack, 42)
    assert f"{OTHER_NAME} numbers 2 souls." in chronicle
    assert f"{GROUP_NAME} musters 2 strong at the guard room." in chronicle
