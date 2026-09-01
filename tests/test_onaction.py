"""iter-42 acceptance — the on_action dispatch layer (drama-3, phase 3,
D-071; DIRECTOR_SPEC §3c the contract owner, core/onaction.py the
mechanics): the Paradox on_action table adapted — event X commits →
content reacts, as pack data.

The laws pinned here:

- **Append-not-overwrite composition**: every entry of the keyed list
  dispatches; a second declaration never replaces the first; the
  hardcoded system reactions (suspicion / arrest / telling) keep
  running before the pack's entries — the donor's "vanilla first,
  custom appended" law, never a replace.
- **The explicit ctx scope**: the `witnesses` selector reads the
  triggering event's OWN knowledge records (deduped, event order) —
  the named use case "every NPC who witnessed X"; the gate is the
  quantified predicate, a per-entity prop read with the CANDIDATE as
  the argument (no entity field in the spec, no implicit `this`).
- **The alarm shape**: one event per entry, one clamped numeric delta
  per passing candidate (relations.scale — the one numeric scale); an
  empty gated scope emits NOTHING (a world answer, not an event); no
  knowledge and no hooks on the reaction event — the cascade
  terminates (the one-hop lint: no table key may name a reaction event
  the table itself emits).
- **The lazy-group discipline** (KI#13): each entry's draft reads the
  projection as left by the previously committed entries.
- **The gate law**: the pack's own declaration is the gate (INV-3) —
  a pack without the `on_action` block runs the v0.1 reaction
  behavior, byte-identically.

The pack's own entry is DORMANT vocabulary, the iter-38 climax-flag
pattern: `document_check` → `crowd_wary` (every witness of the public
check grows warier) — no action emits document_check yet, so the entry
never fires on any committed run or live session; it fires the moment
the document_check action lands (DIRECTOR_SPEC §11, the owner's
content call). The live path (an alarm-keyed variant — the panic echo)
was probed at iter-42 and reverted: it fires on the phase-1 corpus's
distraction-fire beats, and the corpus's beat anchors are committed
fixtures (§8) — the tests below exercise the live machinery through
linted pack variants instead (the iter-36 mutated-pack pattern).
"""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

import pytest

from core.fold import fold, initial_projection
from core.log import EventRecord, KnowledgeRecord, read_log
from core.onaction import on_action_drafts
from core.pack import PackError, load_pack
from core.transitions import WORLD

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))


def projection() -> dict[str, dict[str, Any]]:
    return initial_projection(PACK.entities)


def _record(
    knowledge: tuple[KnowledgeRecord, ...] = (),
    event_id: str = "ev_0001",
    t: int = 10,
    event_type: str = "document_check",
    actor: str = "npc_guard_01",
    target: str | None = "pc_01",
    outcome: dict[str, Any] | None = None,
) -> EventRecord:
    """A minimal committed record carrying the given knowledge records
    (the witnesses the scope reads)."""
    return EventRecord(
        id=event_id, t=t, type=event_type, actor=actor, cause=None,
        outcome=outcome if outcome is not None else {"location": "loc_tavern"},
        knowledge=knowledge,
        state_changes=(), hooks=(), importance="medium", provenance={},
        target=target,
    )


def _knower(who: str, at: int = 10) -> KnowledgeRecord:
    return KnowledgeRecord(who=who, channel="saw", fidelity="exact",
                           knows="some_token", at=at)


def _pack_with(mutate_rules: Any) -> Any:
    """The tavern pack with `rules.json` mutated, loaded through a temp
    dir and re-linted (the `_mutated_pack` pattern; the pure-function
    tests have no tmp_path, so the dir is scoped here)."""
    rules = json.loads((REPO / "content" / "tavern_pack" / "rules.json")
                       .read_text(encoding="utf-8"))
    mutate_rules(rules)
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "pack"
        shutil.copytree(REPO / "content" / "tavern_pack", target)
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2), encoding="utf-8"
        )
        return load_pack(target)


def _mutated_pack(tmp_path: Path, mutate_rules: Any) -> Any:
    """The same mutation through the suite's tmp_path (the lint tests
    and the live-path variants)."""
    target = tmp_path / "mutated_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    mutate_rules(rules)
    (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                       encoding="utf-8")
    return load_pack(target)


def _rekeyed(entry: dict[str, Any], event_type: str) -> dict[str, Any]:
    """A copy of the live entry, re-keyed (the shape is legal on any
    knowledge-carrying event type — the key is the pack's choice)."""
    return dict(entry, notes=f"re-keyed probe on {event_type}")


def _alarm_pack_rules(rules: dict[str, Any]) -> None:
    """Move the dormant crowd-witness entry onto `alarm_raised` (the
    panic-echo probe: the alarm's witnesses — everyone who heard the
    shout, the PC included — grow warier)."""
    rules["on_action"]["alarm_raised"] = [
        _rekeyed(rules["on_action"]["document_check"][0], "alarm_raised")
    ]
    rules["on_action"].pop("document_check")


def _gate_pack(gate: dict[str, Any]) -> Any:
    """The dormant entry with a per-entity gate bolted on (the drama-1
    gate grammar — a legal mutation the lint accepts)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["on_action"]["document_check"][0]["gate"] = [gate]
    return _pack_with(mutate)


def _keyed_pack(event_type: str) -> Any:
    """The dormant entry re-keyed onto `event_type` (the entry's shape
    is legal on any knowledge-carrying event type)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["on_action"] = {
            event_type: rules["on_action"]["document_check"][:1],
            "notes": rules["on_action"]["notes"],
        }
    return _pack_with(mutate)


# -- the dispatch laws (pure core/onaction.py) -------------------------------


def test_the_witnesses_scope_reads_the_records_deduped() -> None:
    """The scope is the event's OWN knowledge records — deduped by first
    occurrence, in event order (construction order, INV-2): the same
    knower learning two tokens of one event reacts once, in the
    record's own order (never sorted, never set order)."""
    state = projection()
    record = _record(
        knowledge=(
            _knower("npc_drunk_01"), _knower("npc_maid_01"),
            _knower("npc_drunk_01"),  # a second token — reacts once
            _knower("npc_guard_01"),
        )
    )
    (draft,) = on_action_drafts(PACK, state, record)
    assert [change.entity for change in draft.state_changes] == [
        "npc_drunk_01", "npc_maid_01", "npc_guard_01",
    ]


def test_the_delta_is_clamped_and_zero_effect_is_dropped() -> None:
    """One clamped numeric delta per passing candidate (relations.scale —
    the one numeric scale, the alarm precedent); a candidate at the
    scale's edge whose clamped delta is zero is dropped (the KI#13 no-op
    discipline — no zero-change rows in canon)."""
    state = projection()
    state["npc_guard_01"]["relations.suspicion"] = 98  # +5 clamps to 100
    state["npc_barkeep_01"]["relations.suspicion"] = 100  # clamps: no-op
    state["npc_drunk_01"]["relations.suspicion"] = 40
    record = _record(knowledge=(
        _knower("npc_guard_01"), _knower("npc_barkeep_01"),
        _knower("npc_drunk_01"),
    ))
    (draft,) = on_action_drafts(PACK, state, record)
    assert [(c.entity, c.from_, c.to_) for c in draft.state_changes] == [
        ("npc_guard_01", 98, 100), ("npc_drunk_01", 40, 45),
    ]


def test_a_candidate_without_a_numeric_home_is_dropped() -> None:
    """A candidate whose declared prop is missing or non-numeric is
    dropped silently — the world answers (the suspicion law: the
    player, ambient groups have no suspicion home); a bool is never a
    number (the predicates.py guard)."""
    state = projection()
    state["npc_guard_01"]["relations.suspicion"] = 40
    state["npc_maid_01"].pop("relations.suspicion")  # missing home
    state["npc_drunk_01"]["relations.suspicion"] = True  # a flag, not a count
    record = _record(knowledge=(
        _knower("npc_guard_01"), _knower("npc_maid_01"),
        _knower("npc_drunk_01"), _knower("pc_01"),  # the PC: no home either
    ))
    (draft,) = on_action_drafts(PACK, state, record)
    assert [c.entity for c in draft.state_changes] == ["npc_guard_01"]


def test_an_empty_scope_emits_nothing() -> None:
    """No witnesses (or nobody passing the gate) → no event at all —
    the alarm precedent: a world answer, never an empty canon event."""
    state = projection()
    assert list(on_action_drafts(PACK, state, _record())) == []
    record = _record(knowledge=(
        _knower("npc_guard_01"), _knower("npc_maid_01"),
    ))
    gated = _gate_pack({"prop": "relations.suspicion", "comparator": "at_least",
                        "value": 9999})
    assert list(on_action_drafts(gated, state, record)) == []


def test_the_gate_is_the_quantified_predicate() -> None:
    """The per-entity gate: each condition {prop, comparator, value}
    evaluates with the CANDIDATE as the explicit argument — the entity
    is not in the spec (no implicit this). The comparison semantics are
    predicates.py's: a missing prop answers False under at_least and
    equals, True under not_equals; a bool never equals a number."""
    state = projection()
    state["npc_guard_01"]["relations.suspicion"] = 30
    state["npc_maid_01"]["relations.suspicion"] = 10
    record = _record(knowledge=(
        _knower("npc_guard_01"), _knower("npc_maid_01"),
    ))
    gated = _gate_pack({"prop": "relations.suspicion",
                        "comparator": "at_least", "value": 20})
    (draft,) = on_action_drafts(gated, state, record)
    assert [c.entity for c in draft.state_changes] == ["npc_guard_01"]
    equals = _gate_pack({"prop": "relations.suspicion",
                         "comparator": "equals", "value": 10})
    (draft,) = on_action_drafts(equals, state, record)
    assert [c.entity for c in draft.state_changes] == ["npc_maid_01"]
    not_equals = _gate_pack({"prop": "relations.suspicion",
                             "comparator": "not_equals", "value": 10})
    (draft,) = on_action_drafts(not_equals, state, record)
    assert [c.entity for c in draft.state_changes] == ["npc_guard_01"]
    # a missing prop answers honestly: False under at_least
    stripped = projection()
    stripped["npc_guard_01"].pop("relations.suspicion")
    missing = _gate_pack({"prop": "relations.suspicion",
                          "comparator": "at_least", "value": 0})
    assert list(on_action_drafts(missing, stripped, _record(
        knowledge=(_knower("npc_guard_01"),)
    ))) == []
    # a bool never equals the number 1 even where the value is True
    bool_state = projection()
    bool_state["npc_guard_01"]["relations.suspicion"] = True
    bools = _gate_pack({"prop": "relations.suspicion",
                        "comparator": "equals", "value": 1})
    assert list(on_action_drafts(bools, bool_state, _record(
        knowledge=(_knower("npc_guard_01"),)
    ))) == []


def test_the_reaction_event_shape_is_the_alarm_shape() -> None:
    """One event per entry: t = the source's tick, cause chained by the
    loop (draft carries None — the loop-side pin below), actor/target
    from the closed source-resolution vocabulary, the outcome carrying
    the source location and the reacting set, NO knowledge and NO
    hooks of its own — the cascade terminates by construction,
    importance by the pack rule."""
    state = projection()
    state["npc_guard_01"]["relations.suspicion"] = 20
    state["npc_maid_01"]["relations.suspicion"] = 10
    record = _record(knowledge=(
        _knower("npc_guard_01"), _knower("npc_maid_01"),
    ), event_id="ev_0005", t=10, actor="npc_guard_01", target="pc_01")
    (draft,) = on_action_drafts(PACK, state, record)
    assert draft.t == 10
    assert draft.type == "crowd_wary"
    assert draft.cause is None
    assert draft.actor == WORLD  # the default: a world-level reaction
    assert draft.target == "pc_01"  # source_target: the checked stranger
    assert draft.outcome["location"] == "loc_tavern"
    assert draft.outcome["reacting"] == ("npc_guard_01", "npc_maid_01")
    assert draft.knowledge == ()
    assert draft.hooks == ()
    assert draft.importance == "medium"  # entities touched + story-critical
    # the location falls back to the source actor's position when the
    # source outcome carries none (the chronicle's own fallback law)
    fallback = _record(knowledge=(_knower("npc_guard_01"),),
                       event_type="drop_break", actor="pc_01",
                       target=None, outcome={})
    (draft,) = on_action_drafts(_keyed_pack("drop_break"), state, fallback)
    assert draft.outcome["location"] == "loc_street"  # pc_01 stands there


def test_the_actor_target_resolution_vocabulary(tmp_path: Path) -> None:
    """The closed one-hop vocabulary: actor/target resolve to the world
    or the source event's own actor/target — defaults actor=world,
    target=source_target; the override replaces the default."""
    state = projection()
    record = _record(knowledge=(_knower("npc_guard_01"),),
                     event_type="drop_break", actor="pc_01",
                     target="npc_barkeep_01")
    pack = _mutated_pack(tmp_path, lambda rules: rules["on_action"].
                         __setitem__("drop_break", [
                             dict(rules["on_action"]["document_check"][0],
                                  actor="source_actor")
                         ]))
    (draft,) = on_action_drafts(pack, state, record)
    assert draft.actor == "pc_01"  # source_actor override
    assert draft.target == "npc_barkeep_01"  # source_target default


# -- the live path through the Simulator (linted pack variants) --------------


def _sim(pack: Any, log: Path, seed: int = 125) -> Any:
    from core.loop import Simulator

    return Simulator(pack, seed, log, SCHEMA, commit="0000000")


_CROWD_STEPS: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "take", "target": "oil_lamp_01"},
    {"intent": "drop_break", "target": "oil_lamp_01", "near": "bar"},
    {"intent": "wait", "ticks": 30},
]


def test_the_crowded_room_ignition_fires_the_reaction_live(
    tmp_path: Path,
) -> None:
    """The live machinery through the real Simulator + commit door (the
    alarm-keyed linted variant — the iter-36 mutated-pack pattern): an
    occupied ignition raises the alarm → the entry dispatches — every
    witness of the alarm with a numeric home gains the clamped delta,
    cause-chained to the alarm. The PC (no suspicion home) is dropped
    by the world-answer law; the reaction carries no knowledge and no
    hooks, so no further system reaction fires on it — the cascade
    terminates (one hop)."""
    pack = _mutated_pack(tmp_path, _alarm_pack_rules)
    log = tmp_path / "crowd.jsonl"
    sim = _sim(pack, log)
    sim.run_playscript({"name": "crowd", "seed": 125,
                        "pack": pack.name_version, "steps": _CROWD_STEPS})
    events = read_log(log, SCHEMA)[1]
    alarm = next(e for e in events if e.type == "alarm_raised")
    reactions = [e for e in events if e.type == "crowd_wary"]
    assert len(reactions) == 1
    reaction = reactions[0]
    assert reaction.cause == alarm.id  # chained to the alarm, the door's law
    knowers = {k.who for k in alarm.knowledge}
    # the NPCs with a suspicion home react; the PC is dropped (no home)
    assert {c.entity for c in reaction.state_changes} == knowers - {"pc_01"}
    for change in reaction.state_changes:  # the clamped delta lands
        assert change.to_ == change.from_ + 5
    state = fold(events, initial_projection(pack.entities))
    for who in knowers - {"pc_01"}:
        assert state[who]["relations.suspicion"] >= 5
    # nothing dispatched on the reaction itself (no knowledge, no hooks,
    # the one-hop lint) — the events after it are the fire's own cascade
    after = events[events.index(reaction) + 1:]
    assert all(e.type != "crowd_wary" for e in after)


def test_entries_append_and_the_lazy_group_discipline(tmp_path: Path) -> None:
    """Two entries on one key BOTH fire, in declaration order, and the
    second reads the projection as left by the first commit (KI#13:
    never a stale world) — append-not-overwrite through the real
    commit door."""
    def mutate(rules: dict[str, Any]) -> None:
        _alarm_pack_rules(rules)
        rules["on_action"]["alarm_raised"].append(
            _rekeyed(rules["on_action"]["alarm_raised"][0], "alarm_raised")
        )  # a second identical echo: same prop, same delta
    pack = _mutated_pack(tmp_path, mutate)
    log = tmp_path / "append.jsonl"
    sim = _sim(pack, log)
    sim.run_playscript({"name": "append", "seed": 125,
                        "pack": pack.name_version, "steps": _CROWD_STEPS})
    events = read_log(log, SCHEMA)[1]
    reactions = [e for e in events if e.type == "crowd_wary"]
    assert len(reactions) == 2  # both entries dispatched, in order
    assert reactions[0].cause == reactions[1].cause  # both chained to the alarm
    first = {c.entity: (c.from_, c.to_) for c in reactions[0].state_changes}
    second = {c.entity: (c.from_, c.to_) for c in reactions[1].state_changes}
    assert set(first) == set(second)
    for entity, (_, first_to) in first.items():
        # the lazy-group law: entry 2's from_ is entry 1's to_
        assert second[entity][0] == first_to


def test_an_empty_room_ignition_never_dispatches(tmp_path: Path) -> None:
    """The inertness mechanism on the committed runs: an ignition with
    no occupants raises no alarm (the alarm precedent) — no event for
    the entry to key on, no reaction, no log delta."""
    log = tmp_path / "empty.jsonl"
    sim = _sim(PACK, log)
    steps = [
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "take", "target": "oil_lamp_01"},
    ]
    sim.run_playscript({"name": "empty", "seed": 125,
                        "pack": PACK.name_version, "steps": steps})
    events = read_log(log, SCHEMA)[1]
    assert all(e.type != "alarm_raised" for e in events)
    assert all(e.type != "crowd_wary" for e in events)


def test_a_pack_without_the_block_runs_the_v01_reactions(
    tmp_path: Path,
) -> None:
    """The pack's own declaration is the gate (INV-3): dropping the
    on_action block changes NOTHING on a run that fires no entry — the
    logs are byte-identical (the v0.1 reaction behavior)."""
    stripped = _mutated_pack(tmp_path, lambda rules: rules.pop("on_action"))
    log_committed = tmp_path / "committed.jsonl"
    log_stripped = tmp_path / "stripped.jsonl"
    from core.loop import load_playscript

    script = load_playscript(REPO / "tests" / "playscripts" / "day1_full.json")
    _sim(PACK, log_committed, script["seed"]).run_playscript(script)
    _sim(stripped, log_stripped, script["seed"]).run_playscript(script)
    assert log_committed.read_bytes() == log_stripped.read_bytes()


# -- the lint (load-time shape — core/pack.py::_on_action) -------------------


def _lint_error(tmp_path: Path, mutate: Any) -> str:
    with pytest.raises(PackError) as excinfo:
        _mutated_pack(tmp_path, mutate)
    return str(excinfo.value)


def test_lint_rejects_an_unknown_key(tmp_path: Path) -> None:
    error = _lint_error(tmp_path, lambda rules: rules["on_action"][
        "document_check"
    ][0].__setitem__("scop", "witnesses"))
    assert "unknown entry keys ['scop']" in error


def test_lint_rejects_an_unknown_scope(tmp_path: Path) -> None:
    error = _lint_error(tmp_path, lambda rules: rules["on_action"][
        "document_check"
    ][0].__setitem__("scope", "bystanders"))
    assert "scope must be one of ['witnesses']" in error


def test_lint_rejects_a_non_list_table_value(tmp_path: Path) -> None:
    error = _lint_error(tmp_path, lambda rules: rules["on_action"].
                        __setitem__("document_check", rules["on_action"][
                            "document_check"
                        ][0]))
    assert "must be a non-empty list" in error


def test_lint_rejects_a_typo_key(tmp_path: Path) -> None:
    error = _lint_error(tmp_path, lambda rules: rules["on_action"].
                        __setitem__("document_checkk", rules["on_action"].pop(
                            "document_check"
                        )))
    assert "the key must name a template event type" in error


def test_lint_rejects_an_unknown_reaction_event(tmp_path: Path) -> None:
    error = _lint_error(tmp_path, lambda rules: rules["on_action"][
        "document_check"
    ][0].__setitem__("event", "crowd_waryy"))
    assert "event must name a template event type" in error


def test_lint_rejects_a_zero_delta(tmp_path: Path) -> None:
    error = _lint_error(tmp_path, lambda rules: rules["on_action"][
        "document_check"
    ][0]["state"].__setitem__("add", 0))
    assert "state.add must be a non-zero integer" in error


def test_lint_rejects_an_extra_state_key(tmp_path: Path) -> None:
    error = _lint_error(tmp_path, lambda rules: rules["on_action"][
        "document_check"
    ][0]["state"].__setitem__("clamp", True))
    assert "state must be an object with exactly" in error


def test_lint_rejects_a_malformed_gate(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["on_action"]["document_check"][0]["gate"] = [
            {"prop": "relations.suspicion", "comparator": "at_least",
             "value": 20, "of": "npc_guard_01"}
        ]
    error = _lint_error(tmp_path, mutate)
    assert "gate[0]: must be an object with exactly" in error


def test_lint_rejects_an_unknown_gate_comparator(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["on_action"]["document_check"][0]["gate"] = [
            {"prop": "relations.suspicion", "comparator": "around",
             "value": 20}
        ]
    error = _lint_error(tmp_path, mutate)
    assert "comparator must be one of" in error


def test_lint_rejects_unknown_prop_paths(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["on_action"]["document_check"][0]["state"]["prop"] = \
            "relations.dread"
    error = _lint_error(tmp_path, mutate)
    assert "does not name a relations axis" in error


def test_lint_rejects_an_unknown_actor_keyword(tmp_path: Path) -> None:
    error = _lint_error(tmp_path, lambda rules: rules["on_action"][
        "document_check"
    ][0].__setitem__("actor", "source_location"))
    assert "actor must be one of" in error


def test_lint_rejects_a_second_order_reaction(tmp_path: Path) -> None:
    """The one-hop law: an entry keyed on a reaction event type the
    table itself emits — second-order reactions have no v0.1 semantics,
    the cascade must terminate by construction, so the declaration is
    a load-time error (loud, never a silent infinite loop)."""
    def mutate(rules: dict[str, Any]) -> None:
        entry = dict(rules["on_action"]["document_check"][0])
        rules["on_action"]["crowd_wary"] = [entry]
    error = _lint_error(tmp_path, mutate)
    assert "second-order reaction declared" in error


def test_lint_accepts_a_table_without_the_block(tmp_path: Path) -> None:
    """The block is optional — a pack without it lints and runs (the
    gate law pinned byte-side above)."""
    pack = _mutated_pack(tmp_path, lambda rules: rules.pop("on_action"))
    assert "on_action" not in pack.rules
