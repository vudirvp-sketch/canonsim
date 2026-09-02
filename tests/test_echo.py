"""iter-46 acceptance — the psychological echo (social-2, phase 3;
TASKS.md's social-2 row: "psychological echo (P3e); phases.md §3 — NPC
behavior modifiers derived from own knowledge records + ticks since
learned; the emotional residue is per-NPC valence, never player-adapted
(L6)").

The laws pinned here:

- **The read-model law (INV-1)**: the echo writes NOTHING — no events,
  no knowledge, no hooks, no state, no templates, no metrics. A pure
  fold over the knowledge view: token valence decaying linearly with
  ticks since learned, scaled by the record's fidelity, summed per
  axis, clamped to the pack scale. The residue becomes visible only
  through the behavior it gates.
- **The door law**: `echo_at_least` — the P2b behavior gate. The scores
  arrive as duck-typed data read AT THE CALLER'S OWN TICK (the door at
  the entry tick, the urgency gate at the beat, the OCC re-check at
  completion); a missing pair IS zero (the honest answer, never an
  error).
- **The window law (the iter-45 generalization)**: the OCC re-check is
  UNCONDITIONAL for intents whose ACTION carries the echo test — the
  residue decays by time, so the gate can close between accept and
  completion with no event committed; the rejection keeps
  `projection_moved` and never attributes a breaking event the log
  does not hold (the WINDOWED_TESTS family).
- **The L6 fence**: per-NPC valence over the NPC's own records, never
  player-adapted, never an entropy input — the director is untouched
  by construction (DIRECTOR_SPEC §4).
- **The dormancy law (the iter-38/42/45 pattern)**: the committed pack
  declares the valence table but NO action or urgency carries
  `echo_at_least` — the fold runs for no intent, the corpus staying
  green is the byte-identity proof; the live-fire tests run on crafted
  pack copies (the hard_pack precedent; the live driver is content-5's
  call).

Seeds probed to be deterministic (T1): seed 93 — the total steal
failure (the room sees; the drunk's partial sighting at t=5) + the
beat-driven driver.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.echo import EchoScore, echo_scores
from core.fold import initial_projection
from core.intent import IntentData, first_failing, occ_breaking_cause
from core.knowledge import KnowledgeView
from core.log import EventRecord, LoggedKnowledgeRecord, read_log
from core.loop import Simulator
from core.pack import PackError, load_pack
from core.rng import RngBank
from core.urgencies import urgency_intents

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

# the corpus session-10 shape (the iter-44/45 precedent): enter, fail the
# steal (the room sees and mints), wait through the rotation beat
ROOM_FAILURE_WAIT: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "wait", "ticks": 400},
]
# the fade arm: one more wait reaches the 720 beat (the residue is 0 by
# then — the second roll must stay silent)
FADE_SCRIPT: list[dict[str, Any]] = ROOM_FAILURE_WAIT + [
    {"intent": "wait", "ticks": 400},
]

# the tuned probe token (the hard_pack pattern): dread 100, fades 720 —
# the drunk's partial sighting at t=5 scores 25 at the beat-360 read,
# 22 at the door tick 405, dead at the completion tick 805
PROBE_TOKEN: dict[str, Any] = {"fades_ticks": 720, "axes": {"dread": 100}}
PROBE_DRIVER: dict[str, Any] = {
    "npc": "npc_drunk_01",
    "probability_per_beat": 100,
    "intent": {"kind": "look_around"},
    "requires": [
        {"noun": "actor", "test": "echo_at_least", "axis": "dread", "value": 20},
    ],
    "notes": "probe entry — the jittery drunkard watches the room while the "
             "residue holds",
}


def run(tmp_path: Path, pack: Any, seed: int, steps: list[dict[str, Any]],
        name: str) -> tuple[list[Any], Simulator]:
    sim = Simulator(pack, seed, tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    sim.close()
    _header, events = read_log(tmp_path / name, SCHEMA)
    return events, sim


def tuned_pack(tmp_path: Path, *, mutate_rules: Any = None,
               mutate_actions: Any = None) -> Any:
    """A pack copy plus the tuned token and the echo-gated driver (the
    hard_pack pattern): mechanism proof on a crafted copy, the committed
    driver stays content-5's call."""
    target = tmp_path / "pack_tuned"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["echo"]["tokens"]["figure_reaching_for_purse"] = PROBE_TOKEN
    rules["urgencies"]["entries"].append(PROBE_DRIVER)
    if mutate_rules is not None:
        mutate_rules(rules)
    (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                       encoding="utf-8")
    if mutate_actions is not None:
        actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
        mutate_actions(actions)
        (target / "actions.json").write_text(json.dumps(actions, indent=2),
                                            encoding="utf-8")
    return load_pack(target)


def _record(who: str, fidelity: str, knows: str, at: int,
            source: str = "ev_0001") -> LoggedKnowledgeRecord:
    return LoggedKnowledgeRecord(
        who=who, channel="saw", fidelity=fidelity, knows=knows, at=at,
        source=source,
    )


def _view(*rows: LoggedKnowledgeRecord) -> KnowledgeView:
    """A view over synthetic events carrying exactly these records (the
    unit-fold harness — `from_events` is the T2 rebuild path)."""
    events = []
    for index, row in enumerate(rows):
        event_id = row.source if row.source != "ev_0001" else f"ev_{index:04d}"
        events.append(EventRecord(
            id=event_id, t=row.at, type="probe_event", actor="world",
            target=None, cause=None, outcome={},
            knowledge=(row,), state_changes=(), hooks=(),
            importance="low", provenance={},
        ))
    return KnowledgeView.from_events(events)


def _echo_pack(tmp_path: Path, token: dict[str, Any]) -> Any:
    """A pack copy with one crafted token over the theft sighting (the
    formula units' harness — clean fades/weight numbers)."""
    target = tmp_path / "pack_unit"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["echo"]["tokens"]["figure_reaching_for_purse"] = token
    (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                       encoding="utf-8")
    return load_pack(target)


# -- the fold (unit) ---------------------------------------------------------------


def test_full_weight_at_birth_decaying_linearly(tmp_path: Path) -> None:
    """Weight 40, fades 100, exact: age 0 -> 40, age 25 -> 30, age 50
    -> 20 — integer arithmetic, floored; dead AT the boundary tick (the
    leverage expiry law's twin)."""
    pack = _echo_pack(tmp_path, {"fades_ticks": 100, "axes": {"dread": 40}})
    row = _record("npc_drunk_01", "exact", "figure_reaching_for_purse", 0)
    view = _view(row)

    def dread(at: int) -> int:
        scores = echo_scores(pack, view, at)
        return next(s.score for s in scores if s.axis == "dread")

    assert dread(0) == 40
    assert dread(25) == 30
    assert dread(50) == 20
    # the floored tail reads as zero — the pair is ABSENT (the honest
    # answer); dead at the boundary tick itself (the expiry twin)
    assert echo_scores(pack, view, 99) == ()
    assert echo_scores(pack, view, 100) == ()


def test_fidelity_scales_the_residue(tmp_path: Path) -> None:
    """The same sighting at three fidelities: exact 40, partial 20,
    vague 10 — a vague telling carries a quarter of the seeing (the
    knowledge model's core axis composing with the valence table)."""
    pack = _echo_pack(tmp_path, {"fades_ticks": 100, "axes": {"dread": 40}})
    for fidelity, expected in (("exact", 40), ("partial", 20), ("vague", 10)):
        view = _view(_record("npc_drunk_01", fidelity,
                             "figure_reaching_for_purse", 0))
        scores = echo_scores(pack, view, 0)
        assert next(s.score for s in scores if s.axis == "dread") == expected


def test_a_renewed_token_sums_its_records(tmp_path: Path) -> None:
    """Heard twice, felt twice: two records of one token both contribute
    — the residue RENEWS on re-learning (the telling's conferral law)."""
    pack = _echo_pack(tmp_path, {"fades_ticks": 100, "axes": {"dread": 40}})
    view = _view(
        _record("npc_drunk_01", "exact", "figure_reaching_for_purse", 0),
        _record("npc_drunk_01", "exact", "figure_reaching_for_purse", 50,
                source="ev_0009"),
    )
    # ages 60 and 10: 40*40//100 + 40*90//100 = 16 + 36 = 52
    scores = echo_scores(pack, view, 60)
    assert next(s.score for s in scores if s.axis == "dread") == 52


def test_the_sum_clamps_to_the_scale(tmp_path: Path) -> None:
    """Three fresh sightings overshoot the ceiling — the score clamps to
    the pack scale (100), never above."""
    pack = _echo_pack(tmp_path, {"fades_ticks": 100, "axes": {"dread": 40}})
    view = _view(*(
        _record("npc_drunk_01", "exact", "figure_reaching_for_purse", 0,
                source=f"ev_{i:04d}")
        for i in range(3)
    ))
    scores = echo_scores(pack, view, 0)
    assert next(s.score for s in scores if s.axis == "dread") == 100


def test_undeclared_tokens_and_axes_score_nothing(tmp_path: Path) -> None:
    """A token outside the table, an axis the token does not declare —
    both invisible to the fold (the closed vocabulary, INV-3)."""
    pack = _echo_pack(tmp_path, {"fades_ticks": 100, "axes": {"dread": 40}})
    view = _view(
        _record("npc_drunk_01", "exact", "papers_unsatisfactory", 0),
        _record("npc_maid_01", "exact", "figure_reaching_for_purse", 0,
                source="ev_0002"),
    )
    assert echo_scores(pack, view, 0) == (
        EchoScore(who="npc_maid_01", axis="dread", score=40),
    )


def test_zero_scores_are_absent_from_the_tuple(tmp_path: None = None) -> None:
    """A missing pair IS zero — the world's honest answer, never an
    error: the tuple carries only non-zero residue."""
    assert echo_scores(PACK, KnowledgeView(), 0) == ()


def test_records_born_after_the_read_tick_do_not_count(
        tmp_path: Path) -> None:
    """The read model at tick T: a record born later contributes nothing
    (the fold's age guard — honest for any caller, unreachable inside
    the loop where evaluation ticks never precede commits)."""
    pack = _echo_pack(tmp_path, {"fades_ticks": 100, "axes": {"dread": 40}})
    view = _view(_record("npc_drunk_01", "exact",
                         "figure_reaching_for_purse", 50))
    assert echo_scores(pack, view, 40) == ()  # not yet born
    assert echo_scores(pack, view, 50) == (  # alive from its own tick
        EchoScore(who="npc_drunk_01", axis="dread", score=40),
    )


def test_the_tuple_order_is_deterministic(tmp_path: Path) -> None:
    """Knowers in first-acquisition order, axes in token-declaration
    order — the fold's tuple is a stable function of (pack, view, tick)
    (INV-2)."""
    pack = _echo_pack(tmp_path, {"fades_ticks": 100,
                                  "axes": {"wariness": 10, "dread": 20}})
    view = _view(
        _record("npc_maid_01", "exact", "figure_reaching_for_purse", 0),
        _record("npc_drunk_01", "exact", "figure_reaching_for_purse", 0,
                source="ev_0002"),
    )
    assert echo_scores(pack, view, 0) == (
        EchoScore(who="npc_maid_01", axis="wariness", score=10),
        EchoScore(who="npc_maid_01", axis="dread", score=20),
        EchoScore(who="npc_drunk_01", axis="wariness", score=10),
        EchoScore(who="npc_drunk_01", axis="dread", score=20),
    )


def test_a_pack_without_the_block_folds_empty(tmp_path: Path) -> None:
    """The declaration is the gate (INV-3): a pack without the `echo`
    block folds to the empty tuple no matter what the view holds."""
    target = tmp_path / "pack_plain"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    del rules["echo"]
    (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                       encoding="utf-8")
    pack = load_pack(target)
    view = _view(_record("npc_drunk_01", "exact",
                         "figure_reaching_for_purse", 0))
    assert echo_scores(pack, view, 0) == ()


# -- the door (unit) ---------------------------------------------------------------


def _echo_intent(actor: str = "npc_drunk_01") -> IntentData:
    return IntentData(
        id="intent_0000", kind="look_around", actor=actor, target=None,
        fields={},
    )


def test_the_echo_test_reads_the_scores() -> None:
    """The door's echo test: `actor.echo_at_least` passes iff some score
    pairs the actor with the axis at or above the value; no scores — no
    residue — the door rejects (the world said no)."""
    state = initial_projection(PACK.entities)
    requires = [
        {"noun": "actor", "test": "echo_at_least", "axis": "dread", "value": 20},
    ]
    intent = _echo_intent()
    assert first_failing(PACK, state, intent, requires, echoes=()) == (
        "actor.echo_at_least"
    )
    echoes = (EchoScore(who="npc_drunk_01", axis="dread", score=25),)
    assert first_failing(PACK, state, intent, requires, echoes=echoes) is None
    # a wrong entity or axis never transfers; a score below the bar fails
    stranger = _echo_intent(actor="npc_maid_01")
    assert first_failing(PACK, state, stranger, requires, echoes=echoes) == (
        "actor.echo_at_least"
    )
    weak = (EchoScore(who="npc_drunk_01", axis="dread", score=19),)
    assert first_failing(PACK, state, intent, requires, echoes=weak) == (
        "actor.echo_at_least"
    )


def test_the_urgency_gate_is_silent_without_residue(tmp_path: Path) -> None:
    """The beat gate (the P2b consumer): an echo-gated urgency rolls,
    sees no residue, and stays SILENT (the world's noise floor — no
    rejection event); the same roll with a passing score enqueues it."""
    pack = tuned_pack(tmp_path)
    state = initial_projection(pack.entities)
    state["npc_drunk_01"]["position"] = "loc_tavern"
    silent = urgency_intents(pack, state, RngBank(7), echoes=())
    assert not any(i.kind == "look_around" for i in silent)
    armed = urgency_intents(
        pack, state, RngBank(7),
        echoes=(EchoScore(who="npc_drunk_01", axis="dread", score=25),),
    )
    looks = [i for i in armed if i.kind == "look_around"]
    assert len(looks) == 1 and looks[0].actor == "npc_drunk_01"


def test_the_window_test_never_attributes_a_breaking_event(
        tmp_path: Path) -> None:
    """A window precondition cannot be broken BY an event: the OCC
    attribution excludes the whole tick-windowed family — an echo-gated
    intent's window close chains to the last committed event, never
    falsely to the first event after the proposal (the iter-45 law,
    generalized)."""
    def gate_look_around(actions: dict[str, Any]) -> None:
        look = next(a for a in actions["actions"]
                    if a["intent"] == "look_around")
        look["requires"] = [
            {"noun": "actor", "test": "echo_at_least", "axis": "dread",
             "value": 20},
        ]

    gated = tuned_pack(tmp_path / "gated", mutate_actions=gate_look_around)
    state = initial_projection(gated.entities)
    intent = _echo_intent()
    events = [
        EventRecord(
            id=f"ev_{i:04d}", t=5 + i, type="probe_event", actor="world",
            target=None, cause=None, outcome={}, knowledge=(),
            state_changes=(), hooks=(), importance="low", provenance={},
        )
        for i in range(3)
    ]
    assert occ_breaking_cause(gated, list(events), 0, intent, state) is None


# -- the live path (e2e, crafted pack — the dormancy law) ----------------------------


def test_the_residue_drives_the_behavior(tmp_path: Path) -> None:
    """Seed 93: the room's theft failure leaves the drunk's sighting
    (partial, t=5); the tuned token (dread 100, fades 720) scores 25 at
    the beat-360 read — the driver fires ONCE (the look_around at the
    entry tick 406); the beat-720 read is 0 (the residue faded) and the
    roll stays SILENT — "events that happened but no longer matter"
    (P3e's headline law, live)."""
    pack = tuned_pack(tmp_path)
    events, sim = run(tmp_path, pack, 93, FADE_SCRIPT, "driver.jsonl")
    looks = [e for e in events if e.type == "look_around"]
    assert [e.t for e in looks] == [406]
    assert looks[0].actor == "npc_drunk_01"
    # the beat gates at 360 / 720: 25 then 0 (the fade, measured)
    assert next(
        s.score for s in echo_scores(pack, sim.knowledge, 360)
        if s.who == "npc_drunk_01" and s.axis == "dread"
    ) == 25
    assert not any(
        s.who == "npc_drunk_01" for s in echo_scores(pack, sim.knowledge, 720)
    )
    # the silent-skip law: the gate failure never becomes a rejection
    assert not any(
        e.type == "intent_rejected" and e.outcome.get("action") == "look_around"
        for e in events
    )


def test_the_committed_valence_table_reads_real_residue(tmp_path: Path) -> None:
    """The committed numbers on the committed pack: the drunk's partial
    sighting at t=5 under the declared valence (dread 25 / wariness 35,
    fades 720, partial 50%) reads dread 6 / wariness 8 at the beat-360
    tick — the table is live-readable even while dormant (no consumer
    gates on it)."""
    events, sim = run(tmp_path, PACK, 93, ROOM_FAILURE_WAIT, "plain.jsonl")
    assert not any(e.type == "look_around" for e in events)
    scores = {
        (s.who, s.axis): s.score
        for s in echo_scores(PACK, sim.knowledge, 360)
    }
    assert scores[("npc_drunk_01", "dread")] == 6
    assert scores[("npc_drunk_01", "wariness")] == 8


def test_the_window_closes_between_accept_and_completion(tmp_path: Path) -> None:
    """The tick-window law (the iter-45 generalization): the ACTION
    carries the echo test (the coerce lint's shape — the door and the
    OCC re-validate what the action declares) with a long duration; the
    door accepts at t=405 (the drunk's residue 22 at his own tick), the
    completion at t=805 re-reads the fold UNCONDITIONALLY — the residue
    is dead, the rejection keeps `projection_moved` with the cause
    chained to the LAST committed canon (never an event the log does
    not hold), and no look_around event commits."""
    def gate_and_lengthen(actions: dict[str, Any]) -> None:
        look = next(a for a in actions["actions"]
                    if a["intent"] == "look_around")
        look["ticks"] = 400
        look["requires"] = [
            {"noun": "actor", "test": "echo_at_least", "axis": "dread",
             "value": 20},
        ]

    pack = tuned_pack(tmp_path / "window", mutate_actions=gate_and_lengthen)
    events, sim = run(tmp_path, pack, 93, ROOM_FAILURE_WAIT, "window.jsonl")
    assert not any(e.type == "look_around" for e in events)
    rejection = next(
        e for e in events
        if e.type == "intent_rejected" and e.outcome.get("action") == "look_around"
    )
    assert rejection.outcome["reason"] == "projection_moved"
    assert rejection.outcome["failed_test"] == "actor.echo_at_least"
    assert rejection.cause is not None  # the last committed canon
    # the two reads that decided it (the window law's evidence)
    assert next(
        s.score for s in echo_scores(pack, sim.knowledge, 405)
        if s.who == "npc_drunk_01"
    ) == 22
    assert not any(
        s.who == "npc_drunk_01" for s in echo_scores(pack, sim.knowledge, 805)
    )


def test_the_declared_table_costs_nothing_at_runtime(tmp_path: Path) -> None:
    """The INV-3 gate law: the committed pack (echo block declared) and
    a copy WITHOUT the block produce byte-identical logs on the same
    seed — the fold runs only for intents that ask for it, and none do
    (the dormancy proof at the byte level)."""
    target = tmp_path / "pack_plain"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    del rules["echo"]
    (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                       encoding="utf-8")
    plain = load_pack(target)
    run(tmp_path, PACK, 93, ROOM_FAILURE_WAIT, "with.jsonl")
    run(tmp_path, plain, 93, ROOM_FAILURE_WAIT, "without.jsonl")
    assert (tmp_path / "with.jsonl").read_bytes() == (
        tmp_path / "without.jsonl").read_bytes()


def test_the_declarations() -> None:
    """The pack rows: the closed block keys, the fidelity percents over
    the pack's own chain, the four declared tokens — and NO consumer
    anywhere (no action, no urgency carries echo_at_least — the
    dormancy law); papers_unsatisfactory stays undeclared (the iter-44
    institutional call)."""
    rules = json.loads(
        (REPO / "content" / "tavern_pack" / "rules.json").read_text(
            encoding="utf-8")
    )
    echo = rules["echo"]
    assert set(echo) == {"scale", "fidelity_weight", "tokens", "notes"}
    assert echo["scale"] == [0, 100]
    assert sorted(echo["fidelity_weight"]) == sorted(
        rules["knowledge"]["fidelity_chain"]
    )
    assert set(echo["tokens"]) == {
        "figure_reaching_for_purse", "figure_starting_fire",
        "purse_missing", "noise_by_the_bar",
    }
    actions = json.loads(
        (REPO / "content" / "tavern_pack" / "actions.json").read_text(
            encoding="utf-8")
    )
    for action in actions["actions"]:
        assert not any(
            cond.get("test") == "echo_at_least"
            for cond in action.get("requires", ())
        )
    for entry in rules["urgencies"]["entries"]:
        assert not any(
            cond.get("test") == "echo_at_least"
            for cond in entry.get("requires", ())
        )


# -- the pack lint ------------------------------------------------------------------


def _lint_error(tmp_path: Path, mutate: Any) -> str:
    target = tmp_path / "pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    mutate(rules)
    (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                       encoding="utf-8")
    try:
        load_pack(target)
    except PackError as exc:
        return str(exc)
    raise AssertionError("the mutated pack must fail the lint")


def test_lint_the_block_keys_are_closed(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["echo"]["nudge"] = True

    assert "unknown keys ['nudge']" in _lint_error(tmp_path, mutate)


def test_lint_the_scale_bounds(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["echo"]["scale"] = [100, 0]

    assert "echo.scale must be" in _lint_error(tmp_path, mutate)


def test_lint_fidelity_weight_must_cover_the_chain(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        del rules["echo"]["fidelity_weight"]["vague"]

    assert "fidelity_weight must map" in _lint_error(tmp_path, mutate)


def test_lint_fidelity_percent_bounds(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["echo"]["fidelity_weight"]["vague"] = 0

    assert "fidelity_weight must map" in _lint_error(tmp_path, mutate)


def test_lint_a_dead_token_is_refused(tmp_path: Path) -> None:
    """The secrets lint's law: a token no declared template can mint is
    dead vocabulary — a typo'd residue token would silently never fire."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["echo"]["tokens"]["purse_mising"] = (
            rules["echo"]["tokens"].pop("purse_missing")
        )

    assert "no declared knowledge template mints this token" in _lint_error(
        tmp_path, mutate
    )


def test_lint_the_token_keys_are_closed(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["echo"]["tokens"]["purse_missing"]["nudge"] = 1

    assert "unknown keys ['nudge']" in _lint_error(tmp_path, mutate)


def test_lint_fades_ticks_must_be_positive(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["echo"]["tokens"]["purse_missing"]["fades_ticks"] = 0

    assert "fades_ticks must be a positive integer" in _lint_error(
        tmp_path, mutate
    )


def test_lint_a_zero_weight_axis_is_dead_vocabulary(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["echo"]["tokens"]["purse_missing"]["axes"] = {"wariness": 0}

    assert "non-zero integer valence weights" in _lint_error(tmp_path, mutate)


def test_lint_the_echo_cond_axis_must_be_declared(tmp_path: Path) -> None:
    """A gate naming an undeclared axis can never pass — dead data,
    refused at load (the leverage `who` family)."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["urgencies"]["entries"].append({
            "npc": "npc_drunk_01", "probability_per_beat": 100,
            "intent": {"kind": "wait", "fields": {"ticks": 1}},
            "requires": [
                {"noun": "actor", "test": "echo_at_least", "axis": "unease",
                 "value": 10},
            ],
        })

    assert "requires 'axis' naming a declared echo axis" in _lint_error(
        tmp_path, mutate
    )


def test_lint_the_echo_cond_value_bounds(tmp_path: Path) -> None:
    """A value at or below the scale floor always passes (a gate that
    never gates); above the ceiling it never does — dead vocabulary
    both ways, refused at load."""

    def mutate_floor(rules: dict[str, Any]) -> None:
        rules["urgencies"]["entries"].append({
            "npc": "npc_drunk_01", "probability_per_beat": 100,
            "intent": {"kind": "wait", "fields": {"ticks": 1}},
            "requires": [
                {"noun": "actor", "test": "echo_at_least", "axis": "dread",
                 "value": 0},
            ],
        })

    def mutate_ceiling(rules: dict[str, Any]) -> None:
        rules["urgencies"]["entries"].append({
            "npc": "npc_drunk_01", "probability_per_beat": 100,
            "intent": {"kind": "wait", "fields": {"ticks": 1}},
            "requires": [
                {"noun": "actor", "test": "echo_at_least", "axis": "dread",
                 "value": 101},
            ],
        })

    assert "value must be an integer in 1..100" in _lint_error(
        tmp_path, mutate_floor
    )
    assert "value must be an integer in 1..100" in _lint_error(
        tmp_path / "ceil", mutate_ceiling
    )


def test_lint_the_echo_test_requires_the_block(tmp_path: Path) -> None:
    """An echo-gated entry in a pack without the echo block: the fold
    scores nothing, the gate can never pass — refused at load."""

    def mutate(rules: dict[str, Any]) -> None:
        del rules["echo"]
        rules["urgencies"]["entries"].append({
            "npc": "npc_drunk_01", "probability_per_beat": 100,
            "intent": {"kind": "wait", "fields": {"ticks": 1}},
            "requires": [
                {"noun": "actor", "test": "echo_at_least", "axis": "dread",
                 "value": 10},
            ],
        })

    assert "requires 'axis' naming a declared echo axis" in _lint_error(
        tmp_path, mutate
    )


def test_lint_the_action_gate_is_checked_too(tmp_path: Path) -> None:
    """The actions side of the cross-lint: an action require naming an
    undeclared axis is refused exactly as the urgency side is."""
    target = tmp_path / "pack_action"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
    look = next(a for a in actions["actions"] if a["intent"] == "look_around")
    look["requires"] = [
        {"noun": "actor", "test": "echo_at_least", "axis": "jitters",
         "value": 10},
    ]
    (target / "actions.json").write_text(json.dumps(actions, indent=2),
                                         encoding="utf-8")
    with pytest.raises(PackError, match="naming a declared echo axis"):
        load_pack(target)
