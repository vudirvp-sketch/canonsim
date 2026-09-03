"""iter-45 acceptance — the leverage use, the coerce door (social-1b,
phase 3; TASKS.md's social-1b row: "an action that SPENDS a live fact
cluster... the pre-condition reads `live_leverage` (the intent door's
first leverage test); the balance... is pack data. The fact cluster's
first runtime consumer").

The laws pinned here:

- **The spend law (INV-1)**: the spend is a NEW EVENT naming the spent
  cluster's id in `outcome.cluster` — never a mutation. The fold kills
  the cluster at the spend's tick (the holder cannot milk one secret
  twice); expiry keeps working beside it.
- **The door law**: `actor.leverage_over` reads the live fold AT THE
  CALLER'S OWN TICK (the door at the entry tick, the urgency gate at
  the beat, the OCC re-check at completion — a tick-windowed
  precondition is never evaluated on stale facts).
- **The window law**: the OCC re-check runs UNCONDITIONAL for
  leverage-carrying intents — the window can close between accept and
  completion with no event committed (the projection is event-driven,
  the window is tick-driven); the rejection rides the standing
  `projection_moved` reason and never attributes a breaking event the
  log does not contain.
- **The balance law**: what a spent cluster buys is pack data —
  subject-directed pair-axis shifts toward the holder, an absent axis
  materialized from the pack's neutral, clamped to the scale, a
  clamped-to-unchanged delta a legal quiet beat (the rest discipline).
- **The quiet law**: the spend carries no knowledge, no hooks — the
  corner is private; the reaction cascade terminates exactly as the
  mint's does.
- **The driver law (content-4, iter-49, D-078)**: the committed pack
  CARRIES the driver — the drunkard's urgency entry re-armed as the
  coerce carrier (the replacement law: the slot and weight stay, the
  per-beat draw count with them — the corpus's check ladders hold; an
  ADDED entry would shift every later check draw). The live-fire tests
  run on the COMMITTED content; the crafted-copy pattern survives only
  for the shrunk-expiry window probe (a pack copy mutating nothing but
  the cluster's lifetime).

Seeds probed to be deterministic (T1): seed 93 — the total steal
failure (the room mints) + the beat-driven drunkard coercion (the
committed p-40 roll hits at the beat; his own cluster expires unspent
on seeds where the roll misses).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.fold import initial_projection
from core.intent import IntentData, first_failing, occ_breaking_cause
from core.leverage import LeverageFact, live_leverage, spendable_leverage
from core.log import EventRecord, read_log
from core.loop import Simulator
from core.pack import PackError, load_pack
from core.resolvers import REGISTRY
from core.rng import RngBank
from core.urgencies import urgency_intents

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

# the corpus session-10 shape (the iter-44 precedent): enter, fail the
# steal (the room sees and mints), wait through the rotation beat
ROOM_FAILURE_WAIT: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "wait", "ticks": 400},
]


def run(tmp_path: Path, pack: Any, seed: int, steps: list[dict[str, Any]],
        name: str) -> tuple[list[Any], Simulator]:
    sim = Simulator(pack, seed, tmp_path / name, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    _header, events = read_log(tmp_path / name, SCHEMA)
    return events, sim


def shrunk_pack(tmp_path: Path, expires_ticks: int) -> Any:
    """A pack copy with ONLY the theft secret's lifetime shrunk (the
    window probe's one knob — the committed driver stays as landed; the
    iter-45 armed_pack append pattern died with content-4: the committed
    entry IS the driver now, and appending a second drunkard entry would
    contaminate the roll table)."""
    target = tmp_path / "pack_shrunk"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["secrets"]["tokens"]["figure_reaching_for_purse"][
        "expires_ticks"
    ] = expires_ticks
    (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                       encoding="utf-8")
    return load_pack(target)


def _fact(holder: str, subject: str, source: str = "ev_0010",
          expires_at: int = 730) -> LeverageFact:
    return LeverageFact(
        holder=holder, subject=subject, secret="figure_reaching_for_purse",
        type="blackmail", expires_at=expires_at, source=source,
    )


def _coerce_intent(actor: str = "pc_01", target: str | None = "npc_drunk_01") -> IntentData:
    return IntentData(
        id="intent_0000", kind="coerce", actor=actor, target=target, fields={}
    )


def _gain(event_id: str = "ev_0010", t: int = 10, actor: str = "npc_drunk_01",
          expires_at: int | None = None) -> EventRecord:
    return EventRecord(
        id=event_id, t=t, type="leverage_gained", actor=actor, target="pc_01",
        cause=None,
        outcome={
            "secret": "figure_reaching_for_purse", "type": "blackmail",
            "fidelity": "partial",
            "expires_at": t + 720 if expires_at is None else expires_at,
        },
        knowledge=(), state_changes=(), hooks=(), importance="medium",
        provenance={},
    )


def _spend(event_id: str = "ev_0020", t: int = 100,
           cluster: str = "ev_0010") -> EventRecord:
    return EventRecord(
        id=event_id, t=t, type="coerce", actor="npc_drunk_01", target="pc_01",
        cause=None,
        outcome={"cluster": cluster, "secret": "figure_reaching_for_purse",
                 "type": "blackmail"},
        knowledge=(), state_changes=(), hooks=(), importance="medium",
        provenance={},
    )


# -- the fold's spent law (unit) ------------------------------------------------


def test_the_spend_kills_the_cluster_at_its_tick() -> None:
    """Live the tick before the spend, dead AT it — the twin of the expiry
    boundary law (iter-44): one secret buys one play, the fold decides."""
    events = [_gain(), _spend()]
    assert len(live_leverage(PACK, events, 99)) == 1  # before the spend
    assert live_leverage(PACK, events, 100) == ()  # AT the spend tick
    assert live_leverage(PACK, events, 500) == ()  # and forever after


def test_expiry_still_kills_without_a_spend() -> None:
    """The spend joins expiry, never replaces it: an unspent cluster dies
    at its own boundary tick exactly as before (iter-44's law intact)."""
    events = [_gain(expires_at=730)]
    assert len(live_leverage(PACK, events, 729)) == 1
    assert live_leverage(PACK, events, 730) == ()


def test_a_foreign_cluster_reference_is_ignored() -> None:
    """A spend naming an id no gain carries is inert data — the fold never
    crashes on log noise (defensive read, the folded set is id-keyed)."""
    events = [_gain(), _spend(cluster="ev_9999")]
    assert len(live_leverage(PACK, events, 150)) == 1


def test_a_pack_without_a_spend_event_never_spends() -> None:
    """The `secrets` block without `spend_event`: clusters live to expiry
    no matter what coerce-shaped events walk the log — the declaration is
    the gate (INV-3)."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "pack_nospend"
        shutil.copytree(REPO / "content" / "tavern_pack", target)
        rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
        del rules["secrets"]["spend_event"]
        (target / "rules.json").write_text(json.dumps(rules, indent=2),
                                           encoding="utf-8")
        pack = load_pack(target)
        events = [_gain(), _spend()]
        assert len(live_leverage(pack, events, 150)) == 1  # the spend is dead data


def test_spendable_leverage_picks_log_order_and_is_loud() -> None:
    """The picker: the FIRST live fact for the pair (log order —
    deterministic); an empty fold is a loud contract break, never a
    silent no-op (the KI#15 family)."""
    first = _fact("npc_drunk_01", "pc_01", source="ev_0010")
    second = _fact("npc_drunk_01", "pc_01", source="ev_0011")
    picked = spendable_leverage((first, second), "npc_drunk_01", "pc_01")
    assert picked is first
    assert spendable_leverage((second,), "npc_drunk_01", "pc_01") is second
    with pytest.raises(Exception, match="no live leverage"):
        spendable_leverage((), "npc_drunk_01", "pc_01")
    with pytest.raises(Exception, match="no live leverage"):
        spendable_leverage((_fact("npc_maid_01", "pc_01"),), "npc_drunk_01", "pc_01")


# -- the door (unit) ------------------------------------------------------------


def test_the_leverage_test_reads_the_facts() -> None:
    """The intent door's first leverage test: `actor.leverage_over` passes
    iff some live fact pairs the actor over `who`; no facts — no leverage
    — the door rejects (the world said no)."""
    action = PACK.action("coerce")
    assert action is not None
    state = initial_projection(PACK.entities)
    state["pc_01"]["position"] = "loc_tavern"  # co-located with the drunkard
    intent = _coerce_intent()
    requires = list(action["requires"])
    # the player holds nothing over the drunkard (the subject is the player)
    assert first_failing(PACK, state, intent, requires, facts=()) == (
        "actor.leverage_over"
    )
    # the drunkard holds the live fact over the player
    drunk = _coerce_intent(actor="npc_drunk_01", target="pc_01")
    facts = (_fact("npc_drunk_01", "pc_01"),)
    assert first_failing(PACK, state, drunk, requires, facts=facts) is None
    # a fact over one subject never transfers to another pair
    stranger = _coerce_intent(actor="npc_barkeep_01", target="npc_maid_01")
    assert first_failing(PACK, state, stranger, requires, facts=facts) == (
        "actor.leverage_over"
    )


def test_the_window_test_never_attributes_a_breaking_event() -> None:
    """A window precondition cannot be broken BY an event: the OCC
    attribution excludes it — a window close chains to the last
    committed event (the caller's fallback), never falsely to the first
    event after the proposal."""
    action = PACK.action("coerce")
    assert action is not None
    state = initial_projection(PACK.entities)
    state["pc_01"]["position"] = "loc_tavern"  # co-located from the start
    drunk = _coerce_intent(actor="npc_drunk_01", target="pc_01")
    # two unrelated events after the proposal point — nothing breaks
    events = [_gain(event_id="ev_0000", t=5), _spend(event_id="ev_0001", t=9)]
    cause = occ_breaking_cause(PACK, list(events), 0, drunk, state)
    assert cause is None


# -- the resolver (unit) ----------------------------------------------------------


def test_the_balance_lands_on_the_subject_pair_axes() -> None:
    """The pack's buy: the subject's directed pair axes toward the holder
    shift from the NEUTRAL (an absent axis materializes at neutral+delta
    — the trust_toward read law, made a write); no check, the event type
    is the action's own success."""
    action = PACK.action("coerce")
    assert action is not None
    state = initial_projection(PACK.entities)
    drunk = _coerce_intent(actor="npc_drunk_01", target="pc_01")
    resolution = REGISTRY["coerce"](
        PACK, state, RngBank(42), drunk, action, None, 10
    )
    assert resolution.event_type == "coerce"
    assert resolution.outcome == {}  # the loop stamps the cluster half
    assert resolution.knowledge == ()  # the corner is quiet
    assert [(c.entity, c.prop, c.from_, c.to_) for c in resolution.state_changes] == [
        ("pc_01", "pair.npc_drunk_01.trust", None, 25),
        ("pc_01", "pair.npc_drunk_01.fear", None, 75),
    ]


def test_the_balance_accumulates_and_clamps() -> None:
    """An existing pair axis accumulates from its CURRENT value (KI#13:
    `from` is read, never hardcoded); the scale clamps; a
    clamped-to-unchanged delta is a legal quiet beat (no StateChange —
    the rest/decay discipline)."""
    action = PACK.action("coerce")
    assert action is not None
    state = initial_projection(PACK.entities)
    state["pc_01"]["pair.npc_drunk_01.trust"] = 20
    state["pc_01"]["pair.npc_drunk_01.fear"] = 90
    drunk = _coerce_intent(actor="npc_drunk_01", target="pc_01")
    resolution = REGISTRY["coerce"](
        PACK, state, RngBank(42), drunk, action, None, 10
    )
    changes = {(c.prop): (c.from_, c.to_) for c in resolution.state_changes}
    assert changes == {
        "pair.npc_drunk_01.trust": (20, 0),  # 20 - 25 clamps to the floor
        "pair.npc_drunk_01.fear": (90, 100),  # 90 + 25 clamps to the ceiling
    }
    # at the clamped ends nothing moves — the quiet beat
    state["pc_01"]["pair.npc_drunk_01.trust"] = 0
    state["pc_01"]["pair.npc_drunk_01.fear"] = 100
    quiet = REGISTRY["coerce"](PACK, state, RngBank(42), drunk, action, None, 10)
    assert quiet.state_changes == ()


def test_a_targetless_coerce_is_loud() -> None:
    action = PACK.action("coerce")
    assert action is not None
    state = initial_projection(PACK.entities)
    with pytest.raises(Exception, match="requires a target"):
        REGISTRY["coerce"](PACK, state, RngBank(42), _coerce_intent(target=None),
                           action, None, 10)


# -- the urgency gate (unit) ------------------------------------------------------


def test_the_urgency_gate_is_silent_without_facts() -> None:
    """The beat gate on the COMMITTED driver (content-4): the drunkard's
    roll hits, sees no live fact, and stays SILENT (the world's noise
    floor — no rejection event); the same roll with a live fact enqueues
    the coerce. RngBank(4)'s first urgency-stream draw is a hit
    (21 <= 40, re-probed at engine-2 — the rolls left the substantive
    stream), so the gate — not the dice — is the only filter here."""
    state = initial_projection(PACK.entities)
    state["npc_drunk_01"]["position"] = "loc_tavern"
    state["pc_01"]["position"] = "loc_tavern"
    silent = urgency_intents(PACK, state, RngBank(4), facts=())
    assert not any(i.kind == "coerce" for i in silent)
    armed = urgency_intents(
        PACK, state, RngBank(4), facts=(_fact("npc_drunk_01", "pc_01"),)
    )
    coerces = [i for i in armed if i.kind == "coerce"]
    assert len(coerces) == 1
    assert coerces[0].actor == "npc_drunk_01" and coerces[0].target == "pc_01"


# -- the live path (e2e, the committed content — the driver law) ------------------


def test_the_drunkard_spends_his_cluster(tmp_path: Path) -> None:
    """Seed 93 on the COMMITTED content (content-4): the room failure
    mints the drunkard's cluster; the beat's urgency enqueues the coerce;
    the door accepts (the fold is live); completion commits the spend —
    outcome.cluster names HIS cluster (the log names the fact it
    consumed), the balance lands as the subject's pair axes, importance
    medium (story-critical + two entities), the cascade quiet (no
    knowledge, no hooks)."""
    events, sim = run(tmp_path, PACK, 93, ROOM_FAILURE_WAIT, "spend.jsonl")
    coerces = [e for e in events if e.type == "coerce"]
    assert len(coerces) == 1
    spend = coerces[0]
    clusters = [e for e in events if e.type == "leverage_gained"]
    drunk_cluster = next(e for e in clusters if e.actor == "npc_drunk_01")
    assert spend.actor == "npc_drunk_01" and spend.target == "pc_01"
    assert spend.outcome["cluster"] == drunk_cluster.id
    assert spend.outcome["secret"] == "figure_reaching_for_purse"
    assert spend.outcome["type"] == "blackmail"
    assert spend.knowledge == () and spend.hooks == ()
    assert spend.importance == "medium"
    assert sim.projection["pc_01"]["pair.npc_drunk_01.trust"] == 25
    assert sim.projection["pc_01"]["pair.npc_drunk_01.fear"] == 75
    # the fold: the drunk's cluster is dead, the room's still live
    facts = live_leverage(PACK, events, spend.t + 1)
    assert "npc_drunk_01" not in {f.holder for f in facts}
    assert {f.holder for f in facts} == {
        "npc_guard_01", "npc_guard_02", "npc_barkeep_01", "npc_maid_01",
    }


def test_one_secret_buys_one_play(tmp_path: Path) -> None:
    """The committed driver across three further beats: the drunk's
    cluster is spent at the first coercion, every later roll's gate sees
    a dead fold, no second coerce, no rejection noise — the world's
    noise floor (the urgency law; the door-rejection path is the expiry
    window, pinned next)."""
    steps = ROOM_FAILURE_WAIT + [
        {"intent": "wait", "ticks": 400},
        {"intent": "wait", "ticks": 800},
    ]
    events, _sim = run(tmp_path, PACK, 93, steps, "twice.jsonl")
    assert len([e for e in events if e.type == "coerce"]) == 1
    rejections = [
        e for e in events if e.type == "intent_rejected"
        and e.outcome.get("failed_test") == "actor.leverage_over"
    ]
    assert rejections == []  # silent, never a rejection event


def test_the_door_rejects_the_leverageless_coerce(tmp_path: Path) -> None:
    """A player step coercing without holding any cluster is a plain door
    rejection — the intent door's first leverage test live on the
    committed content (the driver gates the drunkard's beat rolls; the
    player's own attempts meet the door directly)."""
    events, _sim = run(tmp_path, PACK, 93, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "coerce", "target": "npc_drunk_01"},
    ], "reject.jsonl")
    rejection = next(e for e in events if e.type == "intent_rejected")
    assert rejection.outcome == {
        "action": "coerce", "reason": "precondition",
        "failed_test": "actor.leverage_over",
    }


def test_the_window_closes_between_accept_and_completion(tmp_path: Path) -> None:
    """The tick-window law: the OCC re-check is UNCONDITIONAL for
    leverage-carrying intents — the window closes mid-flight with no
    event committed between accept and completion, the completion
    rejects (reason projection_moved — the derived liveness moved, never
    a breaking event the log does not hold), the cause chains to the
    last committed canon. Two-pass pin (the probe discipline): read the
    accept tick, shrink the window, re-run. The committed p-40 driver
    fires on seed 93 (probed) — the shrunk copy mutates nothing but the
    cluster's lifetime."""
    events, _sim = run(tmp_path, PACK, 93, ROOM_FAILURE_WAIT, "pass1.jsonl")
    first = next(e for e in events if e.type == "coerce")
    accept = first.t - 3  # the coerce duration
    mint = min(
        e.t for e in events
        if e.type == "leverage_gained" and e.actor == "npc_drunk_01"
    )
    window = accept - mint + 2  # dies at accept+2, completion at accept+3

    shrunk = shrunk_pack(tmp_path / "shrink", window)
    events2, _sim2 = run(tmp_path, shrunk, 93, ROOM_FAILURE_WAIT, "pass2.jsonl")
    assert not any(e.type == "coerce" for e in events2)
    rejection = next(
        e for e in events2
        if e.type == "intent_rejected" and e.outcome.get("action") == "coerce"
    )
    assert rejection.outcome["reason"] == "projection_moved"
    assert rejection.outcome["failed_test"] == "actor.leverage_over"
    assert rejection.cause is not None  # the last committed canon


def test_the_chronicle_renders_the_spend_line(tmp_path: Path) -> None:
    """T7: the spend earns its tale line — story-critical, medium, above
    the gate, the actor's display name in the house's dry voice."""
    from render.chronicle import chronicle_from_log

    run(tmp_path, PACK, 93, ROOM_FAILURE_WAIT, "tale.jsonl")
    text = chronicle_from_log(tmp_path / "tale.jsonl", PACK, SCHEMA)
    assert "the drunkard leans on the player — the hold is spent." in text


def test_the_declarations() -> None:
    """The pack rows: the spend event declared, the action's success
    event matches, the tale line present, the story-critical hook and
    the metrics row in place (the rule owns the signal/noise split),
    and the driver's entry carries the coerce template (content-4 — the
    committed content set is live)."""
    rules = json.loads(
        (REPO / "content" / "tavern_pack" / "rules.json").read_text(encoding="utf-8")
    )
    assert rules["secrets"]["spend_event"] == "coerce"
    assert "coerce" in rules["importance"]["story_critical_events"]
    assert rules["metrics"]["system_of_type"]["coerce"] == ["relations"]
    drunk = next(
        e for e in rules["urgencies"]["entries"]
        if e["npc"] == "npc_drunk_01"
    )
    assert drunk["intent"] == {"kind": "coerce", "target": "pc_01"}
    assert drunk["probability_per_beat"] == 40
    assert {c["test"] for c in drunk["requires"]} == {
        "same_location", "leverage_over",
    }
    templates = json.loads(
        (REPO / "content" / "tavern_pack" / "templates.json").read_text(encoding="utf-8")
    )
    assert templates["events"]["coerce"]


def test_the_corpus_pins_the_spend_and_the_pair_axes() -> None:
    """The re-distill (the iter-48 pattern, D-078): the corpus's
    outgoing_guard case carries the landing's own claims — the spend
    event claimable by id and the subject's pair axes at the coerce's
    buy (trust 25 / fear 75) — and the silent_second case's tail is the
    spend itself (the last event type re-pinned crowd_wary -> coerce:
    the drunkard's card lands inside the final door batch). The corpus
    test replays these through the real cycle; this pin guards the
    fixture against a silent rollback of the content landing."""
    corpus = json.loads(
        (REPO / "tests" / "fixtures" / "narrator_beats.json").read_text(
            encoding="utf-8"
        )
    )
    outgoing = next(
        c for c in corpus["cases"]
        if c["name"] == "outgoing_guard_blind_to_the_distraction_fire"
    )
    claims = outgoing["beats"][0]["reply"]["proposal"]["claims"]
    coerce_claims = [c for c in claims if c.get("type") == "coerce"]
    assert len(coerce_claims) == 1
    assert coerce_claims[0]["event_id"] == "ev_0031"
    pair = {
        c["prop"]: c["value"] for c in claims
        if c.get("entity") == "pc_01" and c.get("prop", "").startswith(
            "pair.npc_drunk_01"
        )
    }
    assert pair == {
        "pair.npc_drunk_01.trust": 25,
        "pair.npc_drunk_01.fear": 75,
    }
    silent = next(
        c for c in corpus["cases"]
        if c["name"] == "silent_second_steal_waits_out_the_watch"
    )
    assert silent["expect"]["last_event_type"] == "coerce"


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


def _lint_action_error(tmp_path: Path, mutate: Any) -> str:
    target = tmp_path / "pack_action"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
    mutate(actions)
    (target / "actions.json").write_text(json.dumps(actions, indent=2),
                                         encoding="utf-8")
    try:
        load_pack(target)
    except PackError as exc:
        return str(exc)
    raise AssertionError("the mutated action set must fail the lint")


def _coerce_action(actions: dict[str, Any]) -> dict[str, Any]:
    return next(a for a in actions["actions"] if a["intent"] == "coerce")


def test_lint_the_spend_event_must_be_a_template_type(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["spend_event"] = "shakedown"
    assert "not in the template vocabulary" in _lint_error(tmp_path, mutate)


def test_lint_the_spend_event_needs_a_producer(tmp_path: Path) -> None:
    """A spend event no action produces is dead vocabulary — fire_started
    renders (a template type) but belongs to the transition system, not
    to any action's success branch."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["secrets"]["spend_event"] = "fire_started"

    assert "is no action's success event" in _lint_error(tmp_path, mutate)


def test_lint_the_spender_must_gate_on_leverage(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        pass

    def mutate_actions(actions: dict[str, Any]) -> None:
        _coerce_action(actions)["requires"] = [
            {"noun": "target", "test": "kind", "is": "npc"},
        ]

    target = tmp_path / "pack_gate"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
    mutate_actions(actions)
    (target / "actions.json").write_text(json.dumps(actions, indent=2),
                                         encoding="utf-8")
    with pytest.raises(PackError, match="leverage_over precondition"):
        load_pack(target)
    _ = mutate  # the rules are untouched — the action side breaks the pair


def test_lint_the_leverage_test_requires_its_who(tmp_path: Path) -> None:
    def mutate_actions(actions: dict[str, Any]) -> None:
        _coerce_action(actions)["requires"] = [
            {"noun": "actor", "test": "leverage_over"},
        ]

    assert "requires 'who'" in _lint_action_error(tmp_path, mutate_actions)


def test_lint_the_balance_block_is_coerce_only(tmp_path: Path) -> None:
    def mutate_actions(actions: dict[str, Any]) -> None:
        _coerce_action(actions)["resolver"] = "converse"

    assert "only the 'coerce' resolver consumes" in _lint_action_error(
        tmp_path, mutate_actions
    )


def test_lint_the_balance_axes_must_be_declared(tmp_path: Path) -> None:
    def mutate_actions(actions: dict[str, Any]) -> None:
        _coerce_action(actions)["balance"] = [{"axis": "dread", "delta": -25}]

    assert "not a relations axis" in _lint_action_error(tmp_path, mutate_actions)


def test_lint_the_balance_delta_must_be_non_zero(tmp_path: Path) -> None:
    def mutate_actions(actions: dict[str, Any]) -> None:
        _coerce_action(actions)["balance"] = [{"axis": "fear", "delta": 0}]

    assert "non-zero integer" in _lint_action_error(tmp_path, mutate_actions)


def test_lint_the_balance_keys_are_closed(tmp_path: Path) -> None:
    def mutate_actions(actions: dict[str, Any]) -> None:
        _coerce_action(actions)["balance"] = [{"axis": "fear", "delta": 5,
                                               "nudge": True}]

    assert "unknown keys ['nudge']" in _lint_action_error(tmp_path, mutate_actions)
