"""Unit tests for the iter-1 core modules (rng, ids, clock, queue, log,
fold, pack). The invariants these tests document: INV-2 (guards, counters,
sorted/queue order), INV-1 (writer-only canon path, cause-chain integrity,
from-checked projection), INV-3 (lint over pack data).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.clock import Clock, Phase
from core.fold import apply_event, fold, initial_projection
from core.ids import ActorHandle, sequence_id
from core.log import (
    EventDraft,
    EventLogWriter,
    KnowledgeRecord,
    LogError,
    StateChange,
    next_log_path,
    read_log,
    validate_header,
)
from core.pack import PackError, load_pack
from core.queue import NPC_REACTION, PLAYER_INTENT, SCHEDULED, EventQueue
from core.rng import (
    COSMETIC,
    SUBSTANTIVE,
    RngBank,
    RngError,
    urgency_stream_name,
)

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))


# -- RngBank (INV-2 guards, RNG-1) ------------------------------------------


def test_bank_counts_per_stream_and_fingerprint() -> None:
    bank = RngBank(42)
    with bank.assure(SUBSTANTIVE):
        bank.randint(1, 4)
        bank.randint(1, 4)
    with bank.assure(COSMETIC):
        bank.random()
    assert bank.count(SUBSTANTIVE) == 2
    assert bank.count(COSMETIC) == 1
    assert bank.fingerprint == 2


def test_bank_default_active_stream_is_substantive() -> None:
    bank = RngBank(42)
    assert bank.active == SUBSTANTIVE
    bank.randint(1, 2)
    assert bank.count(SUBSTANTIVE) == 1


def test_assure_swaps_and_restores() -> None:
    bank = RngBank(42)
    with bank.assure(COSMETIC):
        assert bank.active == COSMETIC
        bank.random()
    assert bank.active == SUBSTANTIVE
    assert bank.count(COSMETIC) == 1


def test_assure_rejects_nested_foreign_stream() -> None:
    bank = RngBank(42)
    with pytest.raises(RngError, match="cannot assure"):
        with bank.assure(SUBSTANTIVE):
            with bank.assure(COSMETIC):
                pass


def test_assure_urgency_family_nests_inside_substantive_scope() -> None:
    """engine-2 (D-079): an urgency-family stream (per-entry,
    content-addressed `urgency:<npc>:<kind>`) may shadow the assured run
    scope — the per-beat goal rolls are canon-relevant but
    stream-isolated PER ENTRY, so pack urgency growth shifts neither a
    later check draw (the iter-49 measurement flipped 3 corpus ladders
    when the rolls shared the substantive stream) nor another entry's
    rolls. The draws count on the entry's stream; the substantive
    counter — the T1 fingerprint — is untouched; the active stream
    restores on scope exit."""
    entry = urgency_stream_name("npc_maid_01", "wait")
    bank = RngBank(42)
    with bank.assure(SUBSTANTIVE):
        bank.randint(1, 6)  # a check draws
        with bank.assure(entry):
            assert bank.active == entry
            bank.randint(1, 100)
            bank.randint(1, 100)
        assert bank.active == SUBSTANTIVE
        bank.randint(1, 6)  # the checks resume on their own stream
    assert bank.count(entry) == 2
    assert bank.count(SUBSTANTIVE) == 2
    assert bank.fingerprint == 2


def test_assure_rejects_substantive_inside_urgency_scope() -> None:
    """The reverse nesting is a bug, not a feature: a substantive draw
    inside an urgency scope would put canon checks on the wrong stream —
    the family law allows exactly one pairing."""
    bank = RngBank(42)
    with pytest.raises(RngError, match="cannot assure"):
        with bank.assure(urgency_stream_name("npc_maid_01", "wait")):
            with bank.assure(SUBSTANTIVE):
                pass


def test_urgency_streams_register_lazily_and_derive_per_seed() -> None:
    """The per-entry streams register on first use (content-derived,
    never hand-written); the derivation is the standard stream law
    (INV-2): per (seed, name), distinct from substantive and cosmetic,
    reproducible; a typo outside the family stays loud."""
    entry = urgency_stream_name("npc_drunk_01", "coerce")
    bank = RngBank(42)
    assert bank.peek(entry) != bank.peek(SUBSTANTIVE)
    assert bank.peek(entry) != bank.peek(COSMETIC)
    assert RngBank(42).peek(entry) == RngBank(42).peek(entry)
    assert RngBank(42).peek(entry) != RngBank(43).peek(entry)
    with pytest.raises(RngError, match="unknown stream"):
        bank.peek("urgencyy:typo")  # outside the family — the tripwire


def test_urgency_stream_name_is_content_addressed() -> None:
    """The name builder is the single owner of the naming grammar:
    `urgency:<npc>:<kind>` — the pack lint's (npc, kind) uniqueness makes
    it injective, so one entry = one stream."""
    assert urgency_stream_name("npc_maid_01", "wait") == "urgency:npc_maid_01:wait"
    assert urgency_stream_name("a", "b") != urgency_stream_name("a", "c")
    assert urgency_stream_name("a", "b") != urgency_stream_name("b", "a")


def test_audit_passes_without_draws_and_fails_with_them() -> None:
    bank = RngBank(42)
    with bank.audit():
        bank.peek()  # peek never advances — allowed inside audit
    with pytest.raises(RngError, match="inside audit scope"):
        with bank.audit():
            bank.randint(1, 2)


def test_peek_does_not_advance() -> None:
    bank = RngBank(42)
    first = bank.peek()
    assert bank.peek() == first
    bank.random()
    assert bank.peek() != first


def test_unknown_stream_is_loud() -> None:
    bank = RngBank(42)
    with pytest.raises(RngError, match="unknown stream"):
        bank.peek("nope")


# -- ids ---------------------------------------------------------------------


def test_sequence_id_is_zero_padded_and_bounded() -> None:
    assert sequence_id("ev", 0) == "ev_0000"
    assert sequence_id("ev", 7) == "ev_0007"
    assert sequence_id("intent", 12345) == "intent_12345"
    with pytest.raises(ValueError):
        sequence_id("ev", -1)


def test_actor_handle_pack_unpack_roundtrip() -> None:
    handle = ActorHandle(index=17, generation=3)
    assert ActorHandle.unpack(handle.pack()) == handle
    with pytest.raises(ValueError):
        ActorHandle(index=1 << 25, generation=0).pack()


# -- clock (pack-owned phases, INV-3) ----------------------------------------


def test_clock_from_pack_rules() -> None:
    pack = load_pack(REPO / "content" / "tavern_pack")
    clock = Clock.from_rules(dict(pack.rules["time"]))
    assert clock.phase_of(0) == "morning"
    assert clock.phase_of(400) == "afternoon"
    assert clock.phase_of(800) == "evening"
    assert clock.phase_of(1100) == "night"
    assert clock.day_of(1440) == 1


def test_clock_rejects_gaps_and_regession() -> None:
    with pytest.raises(ValueError, match="contiguous"):
        Clock(phases=(Phase("a", 0, 10), Phase("b", 20, 30)), ticks_per_day=30)
    with pytest.raises(ValueError, match="cover"):
        Clock(phases=(Phase("a", 0, 10),), ticks_per_day=30)
    clock = Clock(phases=(Phase("a", 0, 10),), ticks_per_day=10)
    clock.advance_to(5)
    with pytest.raises(ValueError, match="regression"):
        clock.advance_to(4)


# -- queue (SCHED-1) ----------------------------------------------------------


def test_queue_orders_by_tick_then_band_then_actor() -> None:
    queue = EventQueue()
    queue.push(5, SCHEDULED, "npc_b", "completion", None)
    queue.push(3, NPC_REACTION, "npc_a", "intent", None)
    queue.push(3, PLAYER_INTENT, "pc_01", "intent", None)
    queue.push(1, PLAYER_INTENT, "pc_01", "intent", None)
    order = [(e.tick, e.sub_order, e.actor_id) for e in queue]
    assert order == [
        (1, PLAYER_INTENT, "pc_01"),
        (3, PLAYER_INTENT, "pc_01"),
        (3, NPC_REACTION, "npc_a"),
        (5, SCHEDULED, "npc_b"),
    ]


def test_queue_seq_breaks_full_key_ties() -> None:
    queue = EventQueue()
    first = queue.push(2, PLAYER_INTENT, "pc_01", "intent", "first")
    second = queue.push(2, PLAYER_INTENT, "pc_01", "intent", "second")
    assert queue.pop().payload == first.payload
    assert queue.pop().payload == second.payload


def test_queue_negative_tick_and_empty_pop_are_loud() -> None:
    queue = EventQueue()
    with pytest.raises(ValueError):
        queue.push(-1, 0, "x", "intent", None)
    with pytest.raises(IndexError):
        queue.pop()
    assert queue.peek_tick() is None


# -- log writer (INV-1 enforcement point) --------------------------------------


def draft(t: int, cause: str | None, **kwargs: Any) -> EventDraft:
    return EventDraft(t=t, type="wait", actor="pc_01", cause=cause,
                      outcome={"duration": 1}, provenance={"seed": 42}, **kwargs)


def test_writer_rejects_double_header(tmp_path: Path) -> None:
    writer = EventLogWriter(tmp_path / "run.jsonl", SCHEMA)
    writer.write_header(seed=1, commit="x", pack="p@1")
    with pytest.raises(LogError, match="header already written"):
        writer.write_header(seed=1, commit="x", pack="p@1")
    writer.close()


def test_writer_enforces_cause_chain_and_gap_free_ids(tmp_path: Path) -> None:
    log = tmp_path / "run.jsonl"
    writer = EventLogWriter(log, SCHEMA)
    writer.write_header(seed=42, commit="0000000", pack="tavern_pack@0.1")
    first = writer.append(draft(1, cause=None))
    assert first.id == "ev_0000"
    second = writer.append(draft(2, cause=first.id))
    assert second.id == "ev_0001"
    with pytest.raises(LogError, match="cause null"):
        writer.append(draft(3, cause=None))
    with pytest.raises(LogError, match="no written event"):
        writer.append(draft(3, cause="ev_9999"))
    with pytest.raises(LogError, match="tick regression"):
        writer.append(draft(1, cause=second.id))
    writer.close()
    header, events = read_log(log, SCHEMA)
    assert header["seed"] == 42
    assert [e.id for e in events] == ["ev_0000", "ev_0001"]


def test_writer_rejects_first_event_with_cause(tmp_path: Path) -> None:
    writer = EventLogWriter(tmp_path / "bad.jsonl", SCHEMA)
    writer.write_header(seed=1, commit="c", pack="p@0.1")
    with pytest.raises(LogError, match="run-start"):
        writer.append(draft(1, cause="ev_0000"))
    writer.close()


def test_writer_stamps_knowledge_sources(tmp_path: Path) -> None:
    log = tmp_path / "know.jsonl"
    writer = EventLogWriter(log, SCHEMA)
    writer.write_header(seed=42, commit="c", pack="p@0.1")
    record = writer.append(draft(
        1, cause=None,
        knowledge=(KnowledgeRecord(who="npc_1", channel="saw", fidelity="partial",
                                   knows="figure_reaching_for_purse", at=1),),
    ))
    assert record.knowledge[0].source == record.id
    writer.close()
    _, events = read_log(log, SCHEMA)
    line = json.loads(log.read_text().splitlines()[1])
    assert line["knowledge"][0]["source"] == record.id == "ev_0000"


def test_writer_validates_against_schema_at_write_time(tmp_path: Path) -> None:
    writer = EventLogWriter(tmp_path / "bad.jsonl", SCHEMA)
    writer.write_header(seed=42, commit="c", pack="p@0.1")
    with pytest.raises(Exception, match="importance|enum"):
        writer.append(EventDraft(t=1, type="wait", actor="pc_01", cause=None,
                                 outcome={}, importance="huge",  # type: ignore[arg-type]
                                 provenance={"seed": 42}))
    writer.close()


def test_header_contract_rejects_wall_clock_shapes() -> None:
    with pytest.raises(LogError, match="exactly"):
        validate_header({"header": True, "schema_version": "0.1", "seed": 1,
                         "python": "3", "commit": "c", "pack": "p", "ts": 123})
    with pytest.raises(LogError, match="seed"):
        validate_header({"header": True, "schema_version": "0.1", "seed": "42",
                         "python": "3", "commit": "c", "pack": "p"})


# -- fold / projection (STATE-1) -----------------------------------------------


def test_initial_projection_flattens_pack_state() -> None:
    pack = load_pack(REPO / "content" / "tavern_pack")
    state = initial_projection(pack.entities)
    assert state["pc_01"]["position"] == "loc_street"
    assert state["npc_guard_01"]["position"] == "loc_tavern"
    assert state["npc_guard_01"]["relations.suspicion"] == 0
    assert state["npc_drunk_01"]["status.intoxication"] == 50
    assert state["purse_01"]["position"] == "loc_tavern"
    assert state["purse_01"]["carrier"] == "npc_guard_01"  # iter-2: carrier projected
    assert state["oil_lamp_01"]["carrier"] is None
    assert state["loc_tavern"] == {}  # locations: registered, prop-less


def _record(event_id: str, changes: tuple[StateChange, ...]) -> Any:
    from core.log import EventRecord, LoggedKnowledgeRecord

    return EventRecord(
        id=event_id, t=0, type="wait", actor="pc_01", cause=None, outcome={},
        knowledge=(LoggedKnowledgeRecord(who="x", channel="saw", fidelity="exact",
                                          knows="k", at=0, source=event_id),),
        state_changes=changes, hooks=(), importance="low",
        provenance={"seed": 1}, target=None,
    )


def test_apply_event_checks_from_values() -> None:
    state = {"pc_01": {"position": "loc_street"}}
    move = _record("ev_0000", (StateChange("pc_01", "position", "loc_street", "loc_tavern"),))
    apply_event(state, move)
    assert state["pc_01"]["position"] == "loc_tavern"
    stale = _record("ev_0001", (StateChange("pc_01", "position", "loc_street", "loc_x"),))
    with pytest.raises(ValueError, match="expected from"):
        apply_event(state, stale)
    orphan = _record("ev_0002", (StateChange("ghost", "position", "a", "b"),))
    with pytest.raises(ValueError, match="unknown entity"):
        apply_event(state, orphan)


def test_fold_rebuilds_projection() -> None:
    initial = {"pc_01": {"position": "loc_street"}}
    events = [
        _record("ev_0000", (StateChange("pc_01", "position", "loc_street", "loc_tavern"),)),
        _record("ev_0001", (StateChange("pc_01", "position", "loc_tavern", "loc_backyard"),)),
    ]
    assert fold(events, initial) == {"pc_01": {"position": "loc_backyard"}}
    assert initial == {"pc_01": {"position": "loc_street"}}  # fold copies, never mutates


# -- pack loader + minimum lint -------------------------------------------------


def test_load_pack_happy_path() -> None:
    pack = load_pack(REPO / "content" / "tavern_pack")
    assert pack.name_version == "tavern_pack@0.1"
    assert pack.action("move") is not None and pack.action("move")["resolver"] == "movement"
    assert "move" in pack.event_types() and "rumor_told" in pack.event_types()
    assert pack.player_id() == "pc_01"


def _broken_pack(tmp_path: Path, mutate: Any) -> Path:
    import shutil

    target = tmp_path / "broken_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    mutate(target)
    return target


def test_pack_lint_catches_orphan_exit(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        entities = json.loads((target / "entities.json").read_text())
        entities["locations"][0]["exits"].append("loc_nope")
        (target / "entities.json").write_text(json.dumps(entities))

    with pytest.raises(PackError, match="orphan exit"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_carrier_mismatch(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        entities = json.loads((target / "entities.json").read_text())
        entities["npcs"][1]["carries"] = []  # drop the guard's purse
        (target / "entities.json").write_text(json.dumps(entities))

    with pytest.raises(PackError, match="carrier"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_meta_drift(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        actions["meta"]["version"] = "9.9"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="meta"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_phase_gap(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["time"]["phases"][1]["from"] = 400  # gap 360..400
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="time rules"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_duplicate_urgency_pair(tmp_path: Path) -> None:
    """engine-2 (D-079): the (npc, intent.kind) pair addresses the entry's
    roll stream — a duplicate puts two entries on one stream and couples
    their draws; the lint refuses it at load."""

    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        entry = dict(rules["urgencies"]["entries"][1])  # the maid's wait
        rules["urgencies"]["entries"].append(entry)
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="duplicate urgency"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_status_axis(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        entities = json.loads((target / "entities.json").read_text())
        entities["npcs"][0]["status"]["drunkenness"] = 10  # not in rules.states
        (target / "entities.json").write_text(json.dumps(entities))

    with pytest.raises(PackError, match="status axes"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_extra_files(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        (target / "extra.json").write_text("{}")

    with pytest.raises(PackError, match="expected exactly"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- pack lint: the iter-2 intent-contract cross-refs ---------------------------


def test_pack_lint_catches_unknown_resolver_key(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        actions["actions"][0]["resolver"] = "levitate"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="not in the registry"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_precondition_test(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        talk = next(a for a in actions["actions"] if a["intent"] == "talk")
        talk["requires"][0]["test"] = "likes_actor"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="unknown precondition test"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_event_type_outside_vocabulary(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        examine = next(a for a in actions["actions"] if a["intent"] == "examine")
        examine["events"]["success"] = "examine_superbly"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="template vocabulary"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_check_kind(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        examine = next(a for a in actions["actions"] if a["intent"] == "examine")
        examine["check"]["kind"] = "luck"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="unknown check kind"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_knowledge_audience(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        look = next(a for a in actions["actions"] if a["intent"] == "look_around")
        look["knowledge"]["success"][0]["who"] = "everyone"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="unknown audience"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_knowledge_slot(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        look = next(a for a in actions["actions"] if a["intent"] == "look_around")
        look["knowledge"]["success"][0]["knows"] = "scene_{planet}"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="unknown slot"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- the texture-block lint (iter-11 clauses; iter-11a hardening) ----------------


def _take(actions: dict[str, Any]) -> dict[str, Any]:
    return next(a for a in actions["actions"] if a["intent"] == "take")


def test_pack_lint_texture_block_requires_the_field(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        _take(actions)["fields"] = []  # texture block stays, field gone
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="must declare 'texture' in its fields"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_texture_block_forbids_target_defended_checks(tmp_path: Path) -> None:
    """iter-11a: the texture path carries no canon target — a target-sourced
    check would silently roll against a None defender (run_check builds the
    defender from intent.target). Loud at load instead."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        _take(actions)["check"]["kind"] = "stealth_vs_perception"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="defends from the target"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_canon_templates_forbid_the_texture_slot(tmp_path: Path) -> None:
    """iter-11a: the mirror of the texture-block {target} ban — a CANON
    knowledge template has no texture reference in its context, so
    {texture_slot} would KeyError mid-run."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        take = _take(actions)
        take["knowledge"]["failure"][0]["knows"] = "{actor}_fumbled_the_{texture_slot}"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match=r"uses the \{texture_slot\} slot"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_texture_failure_total_needs_canon_branch(tmp_path: Path) -> None:
    """iter-11a: _branch decides failure_total from the CANON knowledge
    block — a texture-only failure_total branch is dead pack data."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        _take(actions)["texture"]["knowledge"]["failure_total"] = [
            {"who": "actor", "channel": "saw", "fidelity": "partial",
             "knows": "{actor}_botched_the_{texture_slot}"}
        ]
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="_branch can never reach it"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_missing_rejection_template(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        templates = json.loads((target / "templates.json").read_text())
        del templates["events"]["intent_rejected"]
        (target / "templates.json").write_text(json.dumps(templates))

    with pytest.raises(PackError, match="intent_rejected"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_ambiguous_per_tick_schedule(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        # two per-tick systems both writing 'status' with no explicit order
        rules["systems"]["states"]["per_tick"] = True
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="both write"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_layer_system_not_per_tick(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["systems"]["fire"]["per_tick"] = False
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="per-tick system"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- iter-2a audit regressions (KI#14/KI#15) ------------------------------------


def test_next_log_path_never_names_an_existing_log(tmp_path: Path) -> None:
    # KI#14: after a middle delete, counting files would return a live log
    # path — and the writer's "w" mode would truncate it. The first free
    # slot wins instead.
    for n in range(3):
        writer = EventLogWriter(tmp_path / f"run_42_{n}.jsonl", SCHEMA)
        writer.write_header(seed=42, commit="c", pack="p@1")
        writer.close()
    (tmp_path / "run_42_1.jsonl").unlink()
    nxt = next_log_path(tmp_path, 42)
    assert nxt.name == "run_42_1.jsonl"  # the freed slot, not run_42_2
    assert not nxt.exists()
    # dense sequence: no gap -> the next index
    (tmp_path / "run_42_1.jsonl").touch()
    assert next_log_path(tmp_path, 42).name == "run_42_3.jsonl"


def test_pack_lint_catches_unknown_use_effect_axis(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        entities = json.loads((target / "entities.json").read_text())
        mug = next(i for i in entities["items"] if i["id"] == "ale_mug_01")
        mug["use_effect"]["status"] = "hiccupiness"  # not a rules.states axis
        (target / "entities.json").write_text(json.dumps(entities))

    with pytest.raises(PackError, match="use_effect"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_knowledge_branch_without_event(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        examine = next(a for a in actions["actions"] if a["intent"] == "examine")
        examine["knowledge"]["failure_total"] = []  # no events.failure_total
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="failure_total"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- pack lint: the iter-3 system cross-refs ------------------------------------


def test_pack_lint_catches_bad_pair_relation_axis(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        entities = json.loads((target / "entities.json").read_text())
        guard = next(n for n in entities["npcs"] if n["id"] == "npc_guard_01")
        guard["pair_relations"][0]["admiration"] = 40  # not a relations axis
        (target / "entities.json").write_text(json.dumps(entities))

    with pytest.raises(PackError, match="pair axis"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_pair_relation_with_self(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        entities = json.loads((target / "entities.json").read_text())
        guard = next(n for n in entities["npcs"] if n["id"] == "npc_guard_01")
        guard["pair_relations"][0]["with"] = "npc_guard_01"
        (target / "entities.json").write_text(json.dumps(entities))

    with pytest.raises(PackError, match="another npc"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_crime_status_value(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        entities = json.loads((target / "entities.json").read_text())
        entities["npcs"][0]["crime_status"] = "wanted"  # not in status_values
        (target / "entities.json").write_text(json.dumps(entities))

    with pytest.raises(PackError, match="crime_status"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_suspicion_source(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["crime_watch"]["suspicion_from_knowledge"]["purse_missing"] = "bad_hunch"
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="unknown suspicion source"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_rotation_post_outside_the_world(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["crime_watch"]["rotation"]["duty_post"] = "loc_nope"
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="duty_post"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_expectation_broken_at_t0(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["expectations"]["rules"][0]["carried_by"] = "npc_barkeep_01"
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="initial pack state"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_expectation_with_both_modes(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["expectations"]["rules"][0]["at_location"] = "loc_tavern"
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="exactly one"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_destination_audience_without_location_target(
    tmp_path: Path,
) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        talk = next(a for a in actions["actions"] if a["intent"] == "talk")
        talk["knowledge"]["success"][0]["who"] = "destination_location"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="target-kind-location"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_telling_event_outside_vocabulary(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["knowledge"]["telling"]["event"] = "gossip_explosion"
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="telling.event"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- the per-present-target expansion lint (st-1, INTENT_SCHEMA §7) --------------


def _move_action(actions: dict[str, Any]) -> dict[str, Any]:
    return next(a for a in actions["actions"] if a["intent"] == "move")


def test_pack_lint_expansion_requires_actor_audience(tmp_path: Path) -> None:
    """KI#43's law: the expansion is a `knows` grammar, NOT an audience
    kind — `who` must stay `actor`."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        _move_action(actions)["knowledge"]["success"][2]["who"] = "same_location"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="requires who == 'actor'"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_unknown_present_at_site(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        _move_action(actions)["knowledge"]["success"][2]["present_at"] = "everywhere"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="unknown present_at site"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_expansion_needs_the_present_slot(tmp_path: Path) -> None:
    """A site without the slot would emit N identical records — refused."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        _move_action(actions)["knowledge"]["success"][2]["knows"] = "a_room"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="lacks the \\{present\\} slot"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_present_slot_needs_a_site(tmp_path: Path) -> None:
    """The mirror: a {present} slot without present_at has no expansion
    semantics — the closed-slot lint alone would pass it, so the pairing
    is enforced explicitly."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        record = _move_action(actions)["knowledge"]["success"][2]
        del record["present_at"]
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="requires a 'present_at'"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_expansion_forbids_except(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        _move_action(actions)["knowledge"]["success"][2]["except"] = ["actor"]
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="'except' has no meaning"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_expansion_site_needs_location_target(tmp_path: Path) -> None:
    """present_at=destination_location needs the target-kind-location
    precondition, exactly like the destination_location audience (drop
    the audience record first so the expansion clause is the one firing)."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        move = _move_action(actions)
        move["requires"] = [
            {"noun": "target", "test": "adjacent_to", "with": "actor"}
        ]
        move["knowledge"]["success"] = [
            record
            for record in move["knowledge"]["success"]
            if record["who"] != "destination_location"
        ]
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="present_at=destination_location' requires"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- pack lint: the tune-1 blocks (importance story-critical + status_effects) --


def test_pack_lint_catches_story_critical_typo(tmp_path: Path) -> None:
    """A story-critical entry outside the template vocabulary never matches
    any event — dead pack data refused at load (the KI#15 family)."""
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["importance"]["story_critical_events"].append("fire_startted")
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="story_critical_events"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_non_integer_importance_score(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["importance"]["score"]["story_critical_event"] = 1.5
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="story_critical_event"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_status_effects_on_wrong_resolver(tmp_path: Path) -> None:
    """status_effects on a non-recuperate action is dead data — the block
    has exactly one consumer; refuse at load, never silently no-op."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        wait = next(a for a in actions["actions"] if a["intent"] == "wait")
        wait["status_effects"] = [{"status": "fatigue", "delta": -30}]
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="recuperate"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_status_effects_unknown_axis(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        rest = next(a for a in actions["actions"] if a["intent"] == "rest")
        rest["status_effects"] = [{"status": "boredom", "delta": -10}]
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="unknown status axis"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_status_effects_zero_delta(tmp_path: Path) -> None:
    """A zero delta is a no-op declared as data — refuse it: dead weight
    with no semantics (the same reason the decay pass skips zero deltas)."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        rest = next(a for a in actions["actions"] if a["intent"] == "rest")
        rest["status_effects"] = [{"status": "fatigue", "delta": 0}]
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="non-zero integer"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- pack lint: the tune-2 card_markers table (D-060) ---------------------------


def test_pack_lint_catches_unknown_marker_relation_axis(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["present_entities"]["card_markers"].append(
            {"prop": "relations.admiration", "min": 1, "marker": "admired"}
        )
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="relations axes"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_marker_row_with_min_and_value(tmp_path: Path) -> None:
    """A row with BOTH min and value has no semantics — the renderer would
    silently pick one; refuse the ambiguity at load."""
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["present_entities"]["card_markers"].append(
            {"prop": "crime_status", "min": 1, "value": "suspect",
             "marker": "suspect"}
        )
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="exactly one of min"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_marker_prop_outside_the_closed_surface(tmp_path: Path) -> None:
    """A marker on an arbitrary prop is dead data today (nothing computes
    it) — the closed surface grows only with a real need (L13)."""
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        rules["brief"]["present_entities"]["card_markers"].append(
            {"prop": "position", "min": 1, "marker": "elsewhere"}
        )
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="closed marker surface"):
        load_pack(_broken_pack(tmp_path, mutate))


# -- pack lint: the pack-2 spot_available layer param (iter-29, D-061) ----------


def test_pack_lint_catches_spot_available_unknown_layer(tmp_path: Path) -> None:
    """A typo'd layer param would KeyError mid-run — refuse it at load
    (the KI#15 dead-data family)."""
    def mutate(target: Path) -> None:
        actions = json.loads((target / "actions.json").read_text())
        arson = next(a for a in actions["actions"] if a["intent"] == "arson")
        for cond in arson["requires"]:
            if cond.get("test") == "spot_available":
                cond["layer"] = "frost"
        (target / "actions.json").write_text(json.dumps(actions))

    with pytest.raises(PackError, match="not a declared transition layer"):
        load_pack(_broken_pack(tmp_path, mutate))
