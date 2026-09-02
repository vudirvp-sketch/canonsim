"""iter-44 acceptance — the secrets & leverage fact clusters (social-1,
phase 3, P3a; phases.md §3 — the CK3 `add_hook` precedent: secrets and
leverage as first-class facts, a hook IS an event with target, type,
expiry tick, cause; core/leverage.py the mechanics, `rules.json::secrets`
the registry).

The laws pinned here:

- **The birth law**: a committed event's knowledge records ride the
  reaction cascade; a record whose token the pack declares, held by a
  NOVEL knower, mints one `leverage_gained` fact event per (knower,
  token) pair — actor = holder, target = subject, the cause chained to
  the event that taught them, the acquisition fidelity riding the
  cluster.
- **The novelty law**: a knower who already holds the token never
  re-mints (the crime reaction's own law — the second steal failure in
  view of the same room mints nothing).
- **Told secrets confer leverage**: the transfer event's records are
  knowledge like any other — the watch briefing's transfer mints the
  relief watcher's cluster (the institution's knowledge becomes the
  institution's leverage).
- **The holder guards**: kind npc (an ambient group is not a social
  actor), holder != subject.
- **The cascade law**: the cluster carries no knowledge, no hooks, no
  state changes — the social fact, not the epistemic one; the reaction
  systems skip it by construction (the one-hop law's sibling).
- **The expiry law**: liveness is a read-side window (INV-1 — the fact
  is immutable, its expiry is a fold): live iff `at_tick < expires_at`,
  dead at the boundary tick.
- **The gate law** (INV-3): a pack without the `secrets` block mints
  nothing — byte-identical to v0.1 on any run without births; on runs
  with births the leverage events are the ONLY divergence.

Seeds are probed to be deterministic (T1 discipline): seed 93 — the
total steal failure (the whole room sees) + the rotation briefing
transfers the token to the relief; seed 19 — two failures against the
same mark, one mint round (the novelty law live).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.knowledge import KnowledgeView
from core.leverage import leverage_drafts, live_leverage
from core.log import (
    EventRecord,
    KnowledgeRecord,
    LoggedKnowledgeRecord,
    read_log,
)
from core.loop import Simulator
from core.pack import PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

# the corpus session-10 shape: enter, fail the steal (the room sees),
# wait through the rotation beat (the briefing transfers the token)
ROOM_FAILURE_WAIT: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "wait", "ticks": 400},
]


def run(tmp_path: Path, seed: int,
        steps: list[dict[str, Any]]) -> list[Any]:
    name = f"run_{seed}.jsonl"
    sim = Simulator(PACK, seed, tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": "leverage", "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    _header, events = read_log(tmp_path / name, SCHEMA)
    return events


def stripped_pack(tmp_path: Path) -> Any:
    """The same pack minus the `secrets` block (the A/B off arm — the
    pack's own declaration is the gate, INV-3)."""
    target = tmp_path / "pack_nosecrets"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    del rules["secrets"]
    (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                       encoding="utf-8")
    return load_pack(target)


def _record(
    knowledge: tuple[KnowledgeRecord, ...] = (),
    event_id: str = "ev_0001",
    t: int = 10,
    event_type: str = "pickpocket_failed",
) -> EventRecord:
    """A minimal committed record carrying the given knowledge records."""
    return EventRecord(
        id=event_id, t=t, type=event_type, actor="pc_01", cause=None,
        outcome={"location": "loc_tavern"}, knowledge=knowledge,
        state_changes=(), hooks=(), importance="medium", provenance={},
        target="npc_guard_01",
    )


def _secret_record(who: str, fidelity: str = "partial") -> KnowledgeRecord:
    return KnowledgeRecord(
        who=who, channel="saw", fidelity=fidelity,  # type: ignore[arg-type]
        knows="figure_reaching_for_purse", at=10,
    )


# -- the unit laws ---------------------------------------------------------------


def test_a_novel_knower_mints_one_cluster() -> None:
    """The fact-cluster shape: actor = holder, target = subject, the
    acquisition fidelity and the expiry window riding the outcome, the
    cause chained by the loop (None here — the drafts are pre-door)."""
    view = KnowledgeView()
    record = _record((_secret_record("npc_guard_01"),))
    drafts = list(leverage_drafts(PACK, view, record))
    assert len(drafts) == 1
    draft = drafts[0]
    assert draft.type == "leverage_gained"
    assert draft.actor == "npc_guard_01"
    assert draft.target == "pc_01"
    assert draft.cause is None  # the loop chains it to the source event
    assert draft.outcome == {
        "secret": "figure_reaching_for_purse",
        "type": "blackmail",
        "fidelity": "partial",
        "expires_at": 10 + 720,
    }
    assert draft.importance == "medium"  # story-critical + two entities


def test_the_cascade_terminates_by_construction() -> None:
    """The cluster carries no knowledge, no hooks, no state changes — the
    social fact, not the epistemic one: the reaction systems (crime,
    telling, on_action) skip it by construction."""
    view = KnowledgeView()
    record = _record((_secret_record("npc_barkeep_01"),))
    for draft in leverage_drafts(PACK, view, record):
        assert draft.knowledge == ()
        assert draft.hooks == ()
        assert draft.state_changes == ()


def test_the_novelty_law_skips_a_known_token() -> None:
    """A knower who already holds the token never re-mints — the crime
    reaction's own novelty law, `before_source` semantics."""
    view = KnowledgeView()
    earlier = EventRecord(
        id="ev_0000", t=5, type="pickpocket_failed", actor="pc_01", cause=None,
        outcome={},
        knowledge=(
            LoggedKnowledgeRecord(
                who="npc_guard_01", channel="saw", fidelity="partial",
                knows="figure_reaching_for_purse", at=5, source="ev_0000",
            ),
        ),
        state_changes=(), hooks=(), importance="medium", provenance={},
        target="npc_guard_01",
    )
    view.add(earlier)
    record = _record((_secret_record("npc_guard_01"),))
    assert list(leverage_drafts(PACK, view, record)) == []


def test_the_holder_guards() -> None:
    """An ambient group is not a social actor (kind npc only); nobody
    holds leverage over themselves (the subject as knower)."""
    view = KnowledgeView()
    record = _record((
        _secret_record("npc_market_crowd_01"),  # ambient: no cluster
        _secret_record("pc_01"),  # the subject: no self-leverage
    ))
    assert list(leverage_drafts(PACK, view, record)) == []


def test_one_cluster_per_knower_token_per_event() -> None:
    """Two records of the same (knower, token) in one event — one
    cluster (the pair is the fact, not the record)."""
    view = KnowledgeView()
    record = _record((
        _secret_record("npc_drunk_01", "partial"),
        _secret_record("npc_drunk_01", "vague"),
    ))
    drafts = list(leverage_drafts(PACK, view, record))
    assert len(drafts) == 1
    assert drafts[0].outcome["fidelity"] == "partial"  # event order wins


def test_an_undeclared_token_mints_nothing() -> None:
    """Only pack-declared tokens are secrets — the registry is the gate
    (INV-3; the noise token about nobody is crowd memory, not leverage)."""
    view = KnowledgeView()
    record = _record((
        KnowledgeRecord(who="npc_barkeep_01", channel="heard",
                        fidelity="vague", knows="noise_by_the_bar", at=10),
    ))
    assert list(leverage_drafts(PACK, view, record)) == []


def test_a_pack_without_the_block_yields_nothing() -> None:
    """The INV-3 gate: a pack without the `secrets` block runs the v0.1
    reaction behavior — no drafts, no fold facts (byte-identity's unit
    half)."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        pack = stripped_pack(Path(tmp))
        view = KnowledgeView()
        record = _record((_secret_record("npc_guard_01"),))
        assert list(leverage_drafts(pack, view, record)) == []
        assert live_leverage(pack, [record], 10) == ()


# -- the live path (e2e) ---------------------------------------------------------


def test_the_failed_steal_mints_the_room_live(tmp_path: Path) -> None:
    """Seed 93: the total failure teaches the token to the whole room —
    every witnessing npc mints a cluster over the player, cause-chained
    to the pickpocket event, the fidelity riding the acquisition (the
    relief's cluster lands later, at the rotation — its own test)."""
    events = run(tmp_path, 93, ROOM_FAILURE_WAIT)
    clusters = [e for e in events if e.type == "leverage_gained"]
    pickpocket = next(e for e in events if e.type == "pickpocket_failed")
    room = [e for e in clusters if e.cause == pickpocket.id]
    assert len(room) == 4  # Doren, the barkeep, the drunkard, the maid
    assert {e.actor for e in room} == {
        "npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    }
    for cluster in room:
        assert cluster.target == "pc_01"
        assert cluster.outcome["secret"] == "figure_reaching_for_purse"
        assert cluster.outcome["expires_at"] == pickpocket.t + 720
        assert cluster.outcome["fidelity"] == "partial"
        assert cluster.provenance == {"seed": 93}


def test_the_briefing_transfer_mints_the_relief(tmp_path: Path) -> None:
    """The told secret: the rotation briefing transfers the token to the
    relief watcher — the institution's knowledge becomes the
    institution's leverage (the transfer event's records are knowledge
    like any other)."""
    events = run(tmp_path, 93, ROOM_FAILURE_WAIT)
    clusters = [e for e in events if e.type == "leverage_gained"]
    transfer = next(e for e in events if e.type == "knowledge_transfer")
    relief = [e for e in clusters if e.actor == "npc_guard_02"]
    assert len(relief) == 1
    assert relief[0].cause == transfer.id  # chained to the teaching event
    assert relief[0].outcome["fidelity"] == "vague"  # two decay steps down
    assert relief[0].outcome["expires_at"] == transfer.t + 720


def test_the_second_failure_never_re_mints(tmp_path: Path) -> None:
    """Seed 19: two steal failures against the same mark in view of the
    same room — ONE mint round (the novelty law live: the second event's
    knowers already hold the token)."""
    events = run(tmp_path, 19, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
        {"intent": "wait", "ticks": 400},
    ])
    failures = [e for e in events if e.type == "pickpocket_failed"]
    assert len(failures) == 2
    room_mints = [
        e for e in events if e.type == "leverage_gained" and e.t < 300
    ]
    assert len(room_mints) == 4  # the first failure only
    assert {e.cause for e in room_mints} == {failures[0].id}


def test_live_leverage_expires_at_the_boundary(tmp_path: Path) -> None:
    """The read-side fold: live strictly before the expiry tick, dead AT
    it (the boundary is exclusive) — the room's window closes first, the
    relief's (minted at the rotation, 360) outlives it."""
    events = run(tmp_path, 93, ROOM_FAILURE_WAIT)
    clusters = [e for e in events if e.type == "leverage_gained"]
    room_expiry = max(
        int(e.outcome["expires_at"]) for e in clusters if e.t < 300
    )
    relief_expiry = max(
        int(e.outcome["expires_at"]) for e in clusters if e.t >= 300
    )
    assert live_leverage(PACK, events, room_expiry - 1)  # all five live
    assert len(live_leverage(PACK, events, room_expiry - 1)) == 5
    # AT the room's boundary: the room dies, the relief survives
    surviving = live_leverage(PACK, events, room_expiry)
    assert [f.holder for f in surviving] == ["npc_guard_02"]
    assert live_leverage(PACK, events, relief_expiry) == ()  # all dead
    first = live_leverage(PACK, events, clusters[0].t)[0]
    assert first.holder == "npc_guard_01"
    assert first.subject == "pc_01"
    assert first.type == "blackmail"
    assert first.source == clusters[0].id


def test_the_chronicle_renders_the_cluster_line(tmp_path: Path) -> None:
    """T7: the fact earns its tale line — the room's first cluster reads
    in the chronicle (story-critical → medium → above the tale gate)."""
    from render.chronicle import chronicle_from_log

    run(tmp_path, 93, ROOM_FAILURE_WAIT)
    text = chronicle_from_log(tmp_path / "run_93.jsonl", PACK, SCHEMA)
    assert "Doren now holds something over the player." in text
    assert "the barkeep now holds something over the player." in text
    assert "the serving maid now holds something over the player." in text


# -- the A/B (the INV-3 gate, live) ----------------------------------------------


def test_no_births_no_divergence_byte_identical(tmp_path: Path) -> None:
    """A run without secret births (the smoke script: movement only) is
    byte-identical with and without the `secrets` block."""
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 30},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "wait", "ticks": 15},
    ]
    with_secrets = tmp_path / "with.jsonl"
    stripped = tmp_path / "without.jsonl"
    Simulator(PACK, 42, with_secrets, SCHEMA, commit="0000000").run_playscript(
        {"name": "ab", "seed": 42, "pack": "tavern_pack@0.1", "steps": steps}
    )
    Simulator(stripped_pack(tmp_path / "arm"), 42, stripped, SCHEMA,
              commit="0000000").run_playscript(
        {"name": "ab", "seed": 42, "pack": "tavern_pack@0.1", "steps": steps}
    )
    assert with_secrets.read_bytes() == stripped.read_bytes()


def test_births_are_the_only_divergence(tmp_path: Path) -> None:
    """On a birth run the divergence is EXACTLY the leverage events:
    filtering them out of the committed arm's log reproduces the
    stripped arm's stream event-for-event (ids, types, ticks, actors —
    the inserted facts shift nothing else)."""
    steps = ROOM_FAILURE_WAIT
    with_log = tmp_path / "with.jsonl"
    without_log = tmp_path / "without.jsonl"
    Simulator(PACK, 93, with_log, SCHEMA, commit="0000000").run_playscript(
        {"name": "ab", "seed": 93, "pack": "tavern_pack@0.1", "steps": steps}
    )
    Simulator(stripped_pack(tmp_path / "arm"), 93, without_log, SCHEMA,
              commit="0000000").run_playscript(
        {"name": "ab", "seed": 93, "pack": "tavern_pack@0.1", "steps": steps}
    )
    _h, with_events = read_log(with_log, SCHEMA)
    _h, without_events = read_log(without_log, SCHEMA)
    remainder = [e for e in with_events if e.type != "leverage_gained"]
    assert len(remainder) == len(without_events)
    for new, old in zip(remainder, without_events, strict=True):
        assert (new.type, new.t, new.actor, new.target) == (
            old.type, old.t, old.actor, old.target
        )
    assert any(e.type == "leverage_gained" for e in with_events)


# -- the pack lint ----------------------------------------------------------------


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


def test_lint_unknown_block_key(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["deadline"] = 1
    assert "unknown keys ['deadline']" in _lint_error(tmp_path, mutate)


def test_lint_the_event_must_be_a_template_type(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["event"] = "leverage_won"
    assert "not in the template vocabulary" in _lint_error(tmp_path, mutate)


def test_lint_a_typoed_token_is_dead_vocabulary(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["tokens"] = {
            "figure_reaching_for_the_purse": {
                "subject": "pc_01", "type": "blackmail", "expires_ticks": 720,
            }
        }
    assert "no declared knowledge template mints this token" in _lint_error(
        tmp_path, mutate
    )


def test_lint_a_templated_token_is_ineligible(tmp_path: Path) -> None:
    """Templated tokens can never be secrets: the subject of a secret is
    a fixed entity, a templated token's subject varies with the world."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["tokens"] = {
            "{actor}_reaching_for_{target}": {
                "subject": "pc_01", "type": "blackmail", "expires_ticks": 720,
            }
        }
    assert "no declared knowledge template mints this token" in _lint_error(
        tmp_path, mutate
    )


def test_lint_the_subject_must_be_an_npc(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["tokens"]["figure_reaching_for_purse"]["subject"] = (
            "oil_lamp_01"
        )
    assert "subject must be an npc id" in _lint_error(tmp_path, mutate)


def test_lint_the_type_must_be_non_empty(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["tokens"]["figure_reaching_for_purse"]["type"] = " "
    assert "type must be a non-empty string" in _lint_error(tmp_path, mutate)


def test_lint_the_expiry_must_be_positive(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["tokens"]["figure_reaching_for_purse"][
            "expires_ticks"
        ] = 0
    assert "expires_ticks must be a positive integer" in _lint_error(
        tmp_path, mutate
    )


def test_lint_unknown_token_keys(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["tokens"]["figure_reaching_for_purse"]["spend"] = True
    assert "unknown keys ['spend']" in _lint_error(tmp_path, mutate)


def test_lint_the_token_table_must_not_be_empty(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["tokens"] = {}
    assert "non-empty object" in _lint_error(tmp_path, mutate)


def test_lint_notes_must_be_prose(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["notes"] = {"key": "value"}
    assert "notes must be a string" in _lint_error(tmp_path, mutate)
