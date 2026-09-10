"""iter-67 acceptance + the iter-70 arming — beliefwire and
beliefwire-2 (the v0.2 refinement family, D-095/D-103/TASKS: the
`trait_held` leaf, the traits channel, the counter-family fold — and
the pack arming: the first LIVE consumer + the counter content).

The laws pinned here:

- **The gate law (never a multiplier)**: `trait_held` answers pass/fail
  and touches no roll, no score, no weight. The roll stays the urgency's
  own stream (engine-2, D-079); the belief filters AFTER the roll — a
  held belief cannot fire a 0-probability entry, and a hit roll cannot
  fire without the belief.
- **The channel law (the iter-45 family)**: the fold is read as DATA at
  the caller's own tick — the beat gate at the beat tick, the door at
  the entry tick, the OCC re-check at the completion tick; the read is
  lazy at the door (an ungated action pays nothing) and the loop's
  `trait_held` joins `WINDOWED_TESTS` (the unconditional completion
  re-check; `occ_breaking_cause` never attributes a fold move to an
  event the log does not hold).
- **The counter-family law**: `counters` — exoneration tokens at the
  SAME breadth bar block the crystallization; records are never dropped
  (INV-1), so the fold answers honestly per read — a belief held at
  tick T can be absent at T' > T when counter records born in between
  reach the bar (the de-crystallization path). Counter records never
  ride `sources`; `expand_trait` is unchanged.
- **The lint laws**: the `token` param must name a declared belief (a
  dead gate is refused at load — the echo axis family); the counters
  vocabulary carries every family law (mintable, no duplicates,
  one-sided membership, can reach the bar) plus the family/counters
  disjointness inside one belief. Removing the belief content prunes
  the consumer with it (the KI#77 pruning chain — a crafted variant
  that strips the traits block must strip the trait-gated entry too,
  or the dead gate refuses at load).
- **The arming law (beliefwire-2, iter-70)**: the committed pack's
  first LIVE consumer — the relief guard's trait-gated scan, live on
  the canonical seed-125 day1 geometry (the rotation's transfer IS the
  belief's conduit: the pair crystallizes at the 360 handover). The
  price, measured both arms and paid in the landing: +3 look_around
  events on seed 125 — the ONLY seed of the day1 ten where the pair
  crystallizes (9/10 byte-identical; the seed-33 panic corpus and
  theft_and_arson untouched — no theft chain, no belief, the gate
  stays honestly silent); the seed-93 narrator family re-distilled
  (the fixed-point runner, the iter-50 idempotency law). The guard_01
  re-gate shape stays pinned as the REFUSED alternative (the seed-33
  panic scan would die — iter-67's record).

Live-fire on CRAFTED packs (the iter-46 crafted-pack family): the
canonical seed-125 day1 geometry — the failed pickpocket (the room
sees, the noise mints), the clean second steal (the purse gone), the
360 expectation (the inference), the crystallization AT the first beat.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from core.fold import initial_projection
from core.intent import IntentData, first_failing, occ_breaking_cause
from core.knowledge import KnowledgeView
from core.log import EventRecord, LoggedKnowledgeRecord, read_log
from core.loop import Simulator
from core.pack import PackError, load_pack
from core.rng import RngBank
from core.traits import Trait, crystallized_traits, expand_trait
from core.urgencies import urgency_intents

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
DAY1 = json.loads((REPO / "tests" / "playscripts" / "day1_full.json").read_text())

GUARD, RELIEF, MAID = "npc_guard_01", "npc_guard_02", "npc_maid_01"
FAMILY = ("figure_reaching_for_purse", "noise_by_the_bar", "purse_missing")
BELIEF = "paranoid_about_thieves"
# the committed counter trio (beliefwire-2, iter-70): the arson sighting
# + the fled sighting + the papers verdict, at the committed threshold 3
COUNTERS = ("figure_starting_fire", "figure_fled_the_room",
            "papers_unsatisfactory")

# the crafted two-token family (threshold 2): the noise at the failed
# pickpocket (t~9) + purse_missing at the 360 expectation — the same
# crystallization timing as the committed three-token family
CRAFTED_FAMILY = ("noise_by_the_bar", "purse_missing")
# the crafted counter pair (threshold 2): the arson sighting + the fled
# sighting — both now COMMITTED mintables (the fled line is iter-70's),
# the crafted pair just trims the trio to the two-arson half
CRAFTED_COUNTERS = ("figure_starting_fire", "figure_fled_the_room")


def _rec(who: str, knows: str, at: int, source: str) -> LoggedKnowledgeRecord:
    return LoggedKnowledgeRecord(
        who=who, channel="saw", fidelity="exact", knows=knows, at=at, source=source,
    )


def _ev(
    eid: str, t: int, knowledge: tuple[LoggedKnowledgeRecord, ...]
) -> EventRecord:
    return EventRecord(
        id=eid, t=t, type="wait", actor="pc_01", cause=None, outcome={},
        knowledge=knowledge, state_changes=(), hooks=(),
        importance="low", provenance={"seed": 125}, target=None,
    )


def crafted_pack(
    tmp_path: Path,
    name: str,
    *,
    mutate_rules: Any = lambda rules: None,
    mutate_actions: Any = lambda actions: None,
    v01: bool = False,
) -> Any:
    """A committed-pack copy with the on-duty guard's look_around urgency
    re-gated from the echo dread bar to the trait gate (the crafted
    consumer — the iter-67 REFUSED shape, kept here as the crafted
    probe geometry), plus caller mutations. The (npc, kind) pair keeps
    its slot — the roll stream name is unchanged, the draws stay put.
    The committed relief-guard trait entry (iter-70's consumer) is
    STRIPPED: one crafted run, one consumer — the crafted tests measure
    the re-gate geometry alone."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if v01:
        # the v0.1 one-scene twin: the macro clock AND its paired
        # weather block dropped together (the pairing law) — the beat
        # machinery full-world (weather-1's arming re-pin)
        rules["time"].pop("macro", None)
        rules.pop("weather", None)
    rules["urgencies"]["entries"] = [
        e for e in rules["urgencies"]["entries"]
        if not any(
            c.get("test") == "trait_held" for c in e.get("requires", ())
        )
    ]
    entry = next(
        e for e in rules["urgencies"]["entries"] if e["npc"] == GUARD
    )
    entry["requires"] = [
        {"noun": "actor", "test": "trait_held", "token": BELIEF},
    ]
    entry["notes"] = (
        "probe entry — the belief-gated watcher: the scan rides the "
        "crystallized belief, never the residue (beliefwire, iter-67)"
    )
    mutate_rules(rules)
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
    mutate_actions(actions)
    (target / "actions.json").write_text(
        json.dumps(actions, indent=2), encoding="utf-8"
    )
    return load_pack(target)


def run(
    tmp_path: Path, pack: Any, seed: int, steps: list[dict[str, Any]], name: str
) -> list[EventRecord]:
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    sim.close()
    _header, events = read_log(log, SCHEMA)
    return events


# -- the counter-family fold --------------------------------------------------


def test_the_counter_block_blocks_at_the_same_bar() -> None:
    """The breadth law's exoneration side: the SAME threshold that
    crystallizes a belief blocks it when the held distinct counter
    tokens reach the bar — below the bar, the belief folds exactly as
    v0.1 did (the counter-case is not there yet). And the undeclared
    side is invisible: a rules view WITHOUT the counters key folds the
    belief over the SAME records — the counter tokens are just unread
    (INV-3's declaration gate, both sides; the committed pack declared
    the trio at iter-70, so the v0.1 arm is the crafted no-counters
    twin)."""
    rules = json.loads((REPO / "content" / "tavern_pack" / "rules.json").read_text())
    rules["traits"]["beliefs"][BELIEF]["counters"] = [
        "figure_starting_fire",
        "figure_fled_the_room",
        "papers_unsatisfactory",
    ]
    pack = _pack_with_rules(rules)
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, FAMILY[0], 1, "a"),)))
    view.add(_ev("b", 2, (_rec(GUARD, FAMILY[1], 2, "b"),)))
    view.add(_ev("c", 3, (_rec(GUARD, FAMILY[2], 3, "c"),)))
    # two counter records — below the threshold-3 bar: the belief holds
    view.add(_ev("d", 4, (_rec(GUARD, "figure_starting_fire", 4, "d"),)))
    view.add(_ev("e", 5, (_rec(GUARD, "figure_fled_the_room", 5, "e"),)))
    held = crystallized_traits(pack, view, 5)
    assert len(held) == 1 and held[0].token == BELIEF
    # the third distinct counter crosses the bar — the belief is blocked
    view.add(_ev("f", 6, (_rec(GUARD, "papers_unsatisfactory", 6, "f"),)))
    assert crystallized_traits(pack, view, 6) == ()
    # the v0.1 twin never read the counters: the same records fold the
    # belief (the undeclared side invisible — the committed trio, just
    # as the committed pack did before iter-70)
    v01 = json.loads((REPO / "content" / "tavern_pack" / "rules.json").read_text())
    del v01["traits"]["beliefs"][BELIEF]["counters"]
    assert len(crystallized_traits(_pack_with_rules(v01), view, 6)) == 1


def _pack_with_rules(rules: dict[str, Any]) -> Any:
    """An in-memory pack view over a mutated rules table (the fold reads
    only `pack.rules` — the crafted-view tests stay filesystem-free,
    no pack lint re-run: the mutations here are fold shapes the load
    lint would demand `counters` reachability for; the lint laws get
    their own crafted_pack tests below)."""
    return SimpleNamespace(rules=rules)


def test_the_decrystallization_arc_is_at_tick_honest() -> None:
    """The de-crystallization path, live in one view: the belief held at
    tick T, counter records born in (T, T'] push the held distinct
    counters to the bar, and the read at T' answers honestly — no
    belief. The counter side obeys the same at_tick gate as the family:
    a counter record born after the read tick contributes nothing (the
    honest read-model law, both sides)."""
    rules = json.loads((REPO / "content" / "tavern_pack" / "rules.json").read_text())
    rules["traits"]["threshold"] = 2
    rules["traits"]["beliefs"][BELIEF]["family"] = list(CRAFTED_FAMILY)
    rules["traits"]["beliefs"][BELIEF]["counters"] = list(CRAFTED_COUNTERS)
    pack = _pack_with_rules(rules)
    view = KnowledgeView()
    view.add(_ev("a", 10, (_rec(GUARD, CRAFTED_FAMILY[0], 10, "a"),)))
    view.add(_ev("b", 20, (_rec(GUARD, CRAFTED_FAMILY[1], 20, "b"),)))
    # crystallized at 20; the counters arrive later
    view.add(_ev("c", 30, (_rec(GUARD, CRAFTED_COUNTERS[0], 30, "c"),)))
    view.add(_ev("d", 40, (_rec(GUARD, CRAFTED_COUNTERS[1], 40, "d"),)))
    assert crystallized_traits(pack, view, 25) == (
        Trait(who=GUARD, token=BELIEF, sources=("a", "b")),
    )
    # both counters born by 40 — the read at 40 blocks; at 39 the second
    # counter is not yet there (below the bar) — the belief still holds
    assert crystallized_traits(pack, view, 39) == (
        Trait(who=GUARD, token=BELIEF, sources=("a", "b")),
    )
    assert crystallized_traits(pack, view, 40) == ()


def test_counter_records_never_ride_sources_or_expansion() -> None:
    """Provenance is the family's evidence — the counter-block is a
    guard, not a contribution: `sources` carries only the family
    records' event ids, and `expand_trait` expands to the family
    records only (the expansion law, unchanged by the counter side)."""
    rules = json.loads((REPO / "content" / "tavern_pack" / "rules.json").read_text())
    rules["traits"]["threshold"] = 2
    rules["traits"]["beliefs"][BELIEF]["family"] = list(CRAFTED_FAMILY)
    rules["traits"]["beliefs"][BELIEF]["counters"] = list(CRAFTED_COUNTERS)
    pack = _pack_with_rules(rules)
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, CRAFTED_FAMILY[0], 1, "a"),)))
    view.add(_ev("b", 2, (_rec(GUARD, CRAFTED_FAMILY[1], 2, "b"),)))
    view.add(_ev("c", 3, (_rec(GUARD, CRAFTED_COUNTERS[0], 3, "c"),)))
    trait = crystallized_traits(pack, view, 3)[0]
    assert trait.sources == ("a", "b")
    records = expand_trait(pack, view, trait)
    assert [r.knows for r in records] == list(CRAFTED_FAMILY)


def test_below_the_counter_bar_folds_as_v01_did() -> None:
    """INV-3's declaration gate on the counter side, iter-70's reading:
    the committed pack declares the trio, but a knower BELOW the bar
    folds exactly as v0.1 did — one counter token is not a counter-case,
    the belief crystallizes over the family alone; the no-counters twin
    answers identically (the block's absence still byte-identical, the
    v0.1 law held)."""
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, FAMILY[0], 1, "a"),)))
    view.add(_ev("b", 2, (_rec(GUARD, FAMILY[1], 2, "b"),)))
    view.add(_ev("c", 3, (_rec(GUARD, FAMILY[2], 3, "c"),)))
    # one would-be counter — below the threshold-3 bar: unread
    view.add(_ev("d", 4, (_rec(GUARD, COUNTERS[0], 4, "d"),)))
    expected = (Trait(who=GUARD, token=BELIEF, sources=("a", "b", "c")),)
    assert crystallized_traits(PACK, view, 4) == expected
    rules = json.loads((REPO / "content" / "tavern_pack" / "rules.json").read_text())
    del rules["traits"]["beliefs"][BELIEF]["counters"]
    assert crystallized_traits(_pack_with_rules(rules), view, 4) == expected


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda r: r["traits"]["beliefs"][BELIEF].update(
                counters=["figure_starting_fire", "figure_starting_fire"]
            ),
            "duplicate tokens",
        ),
        (
            lambda r: r["traits"]["beliefs"][BELIEF].update(counters=[]),
            "non-empty list",
        ),
        (
            lambda r: r["traits"]["beliefs"][BELIEF].update(
                counters=[FAMILY[0], "figure_starting_fire"]
            ),
            "overlaps the family",
        ),
        (
            lambda r: r["traits"]["beliefs"][BELIEF].update(
                counters=["nobody_mints_this"]
            ),
            "not mintable",
        ),
        (
            lambda r: r["traits"]["beliefs"][BELIEF].update(
                counters=["figure_starting_fire"]
            ),
            "never reach threshold",
        ),
    ],
)
def test_the_counter_lint_laws(
    tmp_path: Path, mutate: Any, message: str
) -> None:
    """The KI#15 family on the counter side: every authoring smell that
    would declare dead vocabulary or double-count evidence is refused
    at load — the closed-vocabulary law the secrets/echo/traits lints
    set."""
    with pytest.raises(PackError, match=message):
        crafted_pack(tmp_path, "lint", mutate_rules=mutate)


# -- the leaf (the door's closed test set) ------------------------------------


def _guard_intent() -> IntentData:
    return IntentData(
        id="probe_01", kind="look_around", actor=GUARD, target=None, fields={},
        based_on_event_seq=0,
    )


def test_the_trait_held_test_reads_the_fold() -> None:
    """The leaf: no traits supplied — nobody holds any belief, the door
    rejects with `actor.trait_held`; the held pair passes; a different
    token fails (the fold answers the declared vocabulary only)."""
    requires = [{"noun": "actor", "test": "trait_held", "token": BELIEF}]
    state = {"position": "loc_tavern"}
    projection = {GUARD: state}
    intent = _guard_intent()
    assert first_failing(PACK, projection, intent, requires) == (
        "actor.trait_held"
    )
    traits = (Trait(who=GUARD, token=BELIEF, sources=("a",)),)
    assert first_failing(
        PACK, projection, intent, requires, traits=traits
    ) is None
    other = (Trait(who=RELIEF, token=BELIEF, sources=("a",)),)
    assert first_failing(PACK, projection, intent, requires, traits=other) == (
        "actor.trait_held"
    )
    unknown = [{"noun": "actor", "test": "trait_held", "token": "no_such_belief"}]
    assert first_failing(PACK, projection, intent, unknown, traits=traits) == (
        "actor.trait_held"
    )


def test_the_gate_is_never_a_multiplier(tmp_path: Path) -> None:
    """D-095's own law, behavioral: the belief only filters AFTER the
    roll. A 0-probability entry never emits — held belief or not (the
    belief cannot make the world roll a hit); a 100-probability entry
    with no belief never emits (the roll hit, the world said no); with
    the belief it emits (the roll and the gate both said yes)."""
    pack = crafted_pack(tmp_path, "multiplier")
    state = initial_projection(pack.entities)
    traits = (Trait(who=GUARD, token=BELIEF, sources=("a",)),)
    for seed in range(20):
        bank = RngBank(seed)
        assert not any(
            i.actor == GUARD for i in urgency_intents(pack, state, bank)
        )  # no belief supplied — silent on every seed
    for seed in range(20):
        bank = RngBank(seed)
        emitted = urgency_intents(pack, state, bank, traits=traits)
        assert [i.actor for i in emitted if i.actor == GUARD] == [GUARD]


def test_the_trait_cond_lint_refuses_undeclared_tokens(
    tmp_path: Path,
) -> None:
    """The echo-axis family on the trait side: a `trait_held` require
    naming a token the block never declares is dead vocabulary, refused
    at load — on an urgency entry and on an action alike; a pack with
    no traits block carrying the gate is the same refusal."""
    with pytest.raises(PackError, match="declared traits.beliefs belief"):
        crafted_pack(
            tmp_path, "cond_urgency",
            mutate_rules=lambda r: r["urgencies"]["entries"][-1].update(
                requires=[{"noun": "actor", "test": "trait_held",
                           "token": "no_such_belief"}],
            ),
        )
    with pytest.raises(PackError, match="declared traits.beliefs belief"):

        def gate_look(actions: dict[str, Any]) -> None:
            look = next(
                a for a in actions["actions"] if a["intent"] == "look_around"
            )
            look["requires"] = [
                {"noun": "actor", "test": "trait_held", "token": "no_such_belief"},
            ]

        crafted_pack(tmp_path, "cond_action", mutate_actions=gate_look)
    with pytest.raises(PackError, match="declared traits.beliefs belief"):

        def strip_and_gate(rules: dict[str, Any]) -> None:
            del rules["traits"]

        crafted_pack(tmp_path, "cond_noblock", mutate_rules=strip_and_gate)


def test_the_window_test_never_attributes_a_breaking_event(
    tmp_path: Path,
) -> None:
    """The windowed-family law, the trait twin (the iter-45/46
    generalization): a fold move is never attributed to an event — the
    OCC attribution excludes the whole family, so a trait-gated
    intent's de-crystallization chains to the last committed event,
    never falsely to the first event after the proposal."""

    def gate_look(actions: dict[str, Any]) -> None:
        look = next(a for a in actions["actions"] if a["intent"] == "look_around")
        look["requires"] = [
            {"noun": "actor", "test": "trait_held", "token": BELIEF},
        ]

    gated = crafted_pack(tmp_path, "window", mutate_actions=gate_look)
    state = initial_projection(gated.entities)
    intent = _guard_intent()
    events = [
        EventRecord(
            id=f"ev_{i:04d}", t=5 + i, type="probe_event", actor="world",
            target=None, cause=None, outcome={}, knowledge=(),
            state_changes=(), hooks=(), importance="low", provenance={},
        )
        for i in range(3)
    ]
    assert occ_breaking_cause(gated, list(events), 0, intent, state) is None


# -- the live channel (e2e — the committed consumer, the seed-125 day1 geometry) --


def test_the_channel_fires_only_when_the_belief_is_held(
    tmp_path: Path,
) -> None:
    """The live proof on the canonical geometry, COMMITTED since iter-70:
    the relief guard's trait-gated scan — the rotation's transfer hands
    the whole theft chain to the relief at the 360 handover (the belief
    crystallizes for BOTH guards there — the on-duty one from his own
    records, the incoming one from the briefing), and from that beat on
    the scan fires. Exactly three times (the beats 360/720/1080, the
    queue-tick attribution lands them on the popped entries' ticks),
    all at or after the crystallization beat — and the beat gate stays
    SILENT, never a rejection event (the world's noise floor; the
    barkeep's look_around is the director's release, not the gate's
    business). This IS the beliefwire-2 arming price, live: +3
    look_around events on the canonical seed-125 run."""
    events = run(tmp_path, PACK, DAY1["seed"], DAY1["steps"], "channel.jsonl")
    scans = [
        e for e in events
        if e.type == "look_around" and e.actor == RELIEF
    ]
    # weather-1's arming price, re-pinned: the 1456 scan (the off-duty
    # relief at the guardroom) rode the warm ring — held for crossings
    # no day-scale run reaches. The ACTIVE-scene pair at 733 stays (the
    # relief held the tavern post at the beat-720 roll)
    assert [(e.t, e.outcome["location"]) for e in scans] == [
        (733, "loc_tavern"), (733, "loc_tavern"),
    ]
    # the crystallization evidence the gate read (the fold at the beats)
    view = KnowledgeView.from_events(events)
    for beat in (360, 720, 1080):
        traits = crystallized_traits(PACK, view, beat)
        assert any(t.who == RELIEF and t.token == BELIEF for t in traits)
        assert any(t.who == GUARD and t.token == BELIEF for t in traits)
    # the silent-skip law: a beat-gate failure never becomes a rejection
    assert not any(
        e.type == "intent_rejected" and e.outcome.get("action") == "look_around"
        for e in events
    )
    # the honest quiet seeds: where the theft chain never completes, the
    # gate never passes — the entry stays silent, the run byte-clean
    for seed in (7, 120):  # the quiet arm (steals succeed, no failure)
        quiet = run(tmp_path, PACK, seed, DAY1["steps"], f"quiet_{seed}.jsonl")
        assert not any(
            e.type == "look_around" and e.actor == RELIEF for e in quiet
        )


def test_the_counter_block_decrystallizes_between_accept_and_completion(
    tmp_path: Path,
) -> None:
    """The window law's trait twin, live: the action carries the gate
    (the door and the OCC re-validate what the ACTION declares) with a
    long duration. The beat-360 roll enqueues, the door accepts (the
    belief crystallized at the 360 expectation), the first scan commits
    — then the watch transfer at 1080 carries both counter tokens to
    the off-duty guard (the in-room witnesses saw the fire; the
    rotation's briefing hands it over — the counter conduit), the
    belief de-crystallizes, and the beat-720 intent still in flight
    completes into the UNCONDITIONAL re-read: the rejection keeps
    `projection_moved` with the failed test `actor.trait_held` and the
    cause chained to the LAST committed canon (never an event the log
    does not hold). The beat-1080 gate re-reads the fold and stays
    silent — the de-crystallized world stops scanning."""

    def mutate_rules(rules: dict[str, Any]) -> None:
        rules["traits"]["threshold"] = 2
        rules["traits"]["beliefs"][BELIEF]["family"] = list(CRAFTED_FAMILY)
        rules["traits"]["beliefs"][BELIEF]["counters"] = list(CRAFTED_COUNTERS)

    def lengthen_and_gate(actions: dict[str, Any]) -> None:
        look = next(a for a in actions["actions"] if a["intent"] == "look_around")
        look["ticks"] = 400
        look["requires"] = [
            {"noun": "actor", "test": "trait_held", "token": BELIEF},
        ]

    # the v0.1 one-scene twin: the crafted window mechanics need the
    # guard's beat rolls — under the armed LOD his 360-roll slot sits in
    # the rotation-emptied room (the warm ring holds it for crossings);
    # the window law itself is zone-free and pins on the one-scene world
    pack = crafted_pack(
        tmp_path, "decrystallize",
        mutate_rules=mutate_rules, mutate_actions=lengthen_and_gate,
        v01=True,
    )
    script = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "take", "target": "oil_lamp_01"},
        {"intent": "steal", "target": GUARD, "method": "distraction"},
        {"intent": "steal", "target": GUARD, "method": "distraction"},
        {"intent": "wait", "ticks": 400},
        {"intent": "arson", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 400},
        {"intent": "wait", "ticks": 400},
    ]
    events = run(tmp_path, pack, DAY1["seed"], script, "decrystallize.jsonl")
    # the first scan commits (the belief held from 360 to the transfer)
    scans = [
        e for e in events
        if e.type == "look_around" and e.actor == GUARD
    ]
    assert len(scans) == 1 and scans[0].t < 1080
    # the in-flight beat-720 intent completes into the de-crystallized
    # fold — the window close, not a door refusal
    rejection = next(
        e for e in events
        if e.type == "intent_rejected" and e.outcome.get("action") == "look_around"
    )
    assert rejection.outcome["reason"] == "projection_moved"
    assert rejection.outcome["failed_test"] == "actor.trait_held"
    assert rejection.cause is not None  # the last committed canon
    # the counter evidence: both tokens in the guard's records by the
    # transfer (the beat-1080 gate's own read — the silent world; both
    # minted by the committed arson action since iter-70, the crafted
    # fled-line append retired)
    view = KnowledgeView.from_events(events)
    learned = {r.knows for r in view.records_of(GUARD)}
    assert set(CRAFTED_COUNTERS) <= learned
    # exactly one rejection ever: the beat-1080 gate stayed SILENT (the
    # beat-gate failure is the noise floor, never an event)
    assert sum(
        1 for e in events
        if e.type == "intent_rejected" and e.outcome.get("action") == "look_around"
    ) == 1
    assert not crystallized_traits(
        pack, view, events[-1].t
    ) or not any(
        t.who == GUARD for t in crystallized_traits(pack, view, events[-1].t)
    )


# -- the arming price (the both-arms pin, iter-70) -----------------------------


def _disarm_twin(tmp_path: Path) -> Any:
    """The v0.1 twin: the committed pack with the whole beliefwire-2
    content stripped — the trait-gated entry, the counters key, the
    arson fled line (the pair moves with its minting site; the belief
    family and the traits block stay — iter-67's shape)."""
    twin = tmp_path / "twin"
    shutil.copytree(REPO / "content" / "tavern_pack", twin)
    rules = json.loads((twin / "rules.json").read_text(encoding="utf-8"))
    rules["urgencies"]["entries"] = [
        e for e in rules["urgencies"]["entries"]
        if not any(
            c.get("test") == "trait_held" for c in e.get("requires", ())
        )
    ]
    rules["traits"]["beliefs"][BELIEF].pop("counters", None)
    (twin / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    actions = json.loads((twin / "actions.json").read_text(encoding="utf-8"))
    arson = next(a for a in actions["actions"] if a["intent"] == "arson")
    arson["knowledge"]["success"] = [
        k for k in arson["knowledge"]["success"]
        if k["knows"] != "figure_fled_the_room"
    ]
    (twin / "actions.json").write_text(
        json.dumps(actions, indent=2), encoding="utf-8"
    )
    return load_pack(twin)


def test_the_arming_price_is_three_scans_on_one_seed(
    tmp_path: Path,
) -> None:
    """The both-arms A/B, the arming law's price pin (beliefwire-2,
    iter-70): the armed committed pack vs the v0.1 disarm twin —
    day1_full seeds 120..129, byte-identical on every seed EXCEPT 125,
    where the pair crystallizes (the failed pickpocket, the clean
    second steal, the 360 expectation — the only seed of the ten with
    the whole chain) and the scan fires exactly three times: the
    entire landing's day1 footprint. The price the iter-67 measurement
    projected, confirmed by bytes; the rest of the corpus price (the
    seed-93 narrator family's id shifts) is the mediator corpus's own
    re-distill, not a day1 byte."""
    twin = _disarm_twin(tmp_path)
    for seed in range(120, 130):
        bytes_of: dict[str, bytes] = {}
        for label, p in (("twin", twin), ("armed", PACK)):
            log = tmp_path / f"ab_{label}_{seed}.jsonl"
            script = dict(DAY1)
            script["seed"] = seed
            sim = Simulator(p, seed, log, SCHEMA, commit="0000000")
            sim.run_playscript(script)
            sim.close()
            bytes_of[label] = log.read_bytes()
        if seed == 125:
            assert bytes_of["twin"] != bytes_of["armed"]
            armed_lines = bytes_of["armed"].decode().splitlines()
            scans = [
                ln for ln in armed_lines
                if '"type": "look_around"' in ln
                and '"npc_guard_02"' in ln
                and '"cause_intent": "urgency_' in ln
            ]
            # weather-1's arming price: two, not three — the 1456 scan
            # (the off-duty relief at the guardroom) rode the warm ring,
            # held for crossings no day-scale run reaches
            assert len(scans) == 2
        else:
            assert bytes_of["twin"] == bytes_of["armed"], f"seed {seed} diverged"


# -- the declarations (the committed rows, iter-70) ----------------------------


def test_the_declarations() -> None:
    """The landed content set, pack rows: exactly ONE trait-gated
    urgency consumer (the relief guard's scan, p=100, the compulsion
    idiom — the iter-51 jittery-watcher law); the committed counters
    trio (the exoneration side, three mintable tokens at the threshold
    bar); the arson action's fled line beside the fire sighting (one
    event, both halves — the counter mint)."""
    rules = json.loads(
        (REPO / "content" / "tavern_pack" / "rules.json").read_text(
            encoding="utf-8"
        )
    )
    drivers = [
        entry for entry in rules["urgencies"]["entries"]
        if any(cond.get("test") == "trait_held"
               for cond in entry.get("requires", ()))
    ]
    assert len(drivers) == 1
    driver = drivers[0]
    assert driver["npc"] == "npc_guard_02"
    assert driver["probability_per_beat"] == 100
    assert driver["intent"] == {"kind": "look_around"}
    assert driver["requires"] == [
        {"noun": "actor", "test": "trait_held", "token": BELIEF},
    ]
    belief = rules["traits"]["beliefs"][BELIEF]
    assert belief["counters"] == list(COUNTERS)
    actions = json.loads(
        (REPO / "content" / "tavern_pack" / "actions.json").read_text(
            encoding="utf-8"
        )
    )
    arson = next(a for a in actions["actions"] if a["intent"] == "arson")
    assert [
        (k["knows"], k["who"], k["channel"], k["fidelity"])
        for k in arson["knowledge"]["success"]
    ] == [
        ("figure_starting_fire", "same_location", "saw", "partial"),
        ("figure_fled_the_room", "same_location", "saw", "partial"),
    ]
    # no ACTION carries trait_held — the action side stays
    # consumer-free (its window law pinned on crafted copies)
    for action in actions["actions"]:
        assert not any(
            cond.get("test") == "trait_held"
            for cond in action.get("requires", ())
        )
