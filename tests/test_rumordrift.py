"""iter-68a/68b acceptance — rumordrift (the v0.2 refinement family's
third segment, A2''/D-095/TASKS: "fidelity-ladder drift profiles,
`drift:<family>` streams — isolation is law, `drifted_from` in outcome,
EVENT_SCHEMA §11 no-bump"). Mechanics (iter-68a) + the committed-pack
ARMING (iter-68b): the pack declares the `figure_deeds` family — the
tavern's two crime sightings drift into each other as rumors spread.

The laws pinned here:

- **The drift law (A2'')**: a told fact whose token rides a pack-declared
  `knowledge.drift` family MAY mutate to a sibling — the family's
  fidelity-ladder profile gives the chance at the RECEIVED fidelity (the
  vaguer the record, the likelier the drift); the roll ALWAYS happens for
  a family member (a gated miss still consumes the draw — the urgency
  law: the draw count never depends on the ladder's numbers); a hit picks
  one uniform OTHER member. The mutation is the medium's, not the
  teller's: the novelty gate tests the token the TELLER holds, so the
  original stays tellable and the mutated token re-learnable (heard
  twice, felt twice — the echo law's twin).
- **The stream law (isolation is law, D-095)**: every drift draw rides
  the family's own `drift:<family>` stream, lazily registered, nested
  inside the run's assured substantive scope — arming a family shifts
  neither a canon check draw (the fingerprint) nor another family's
  rolls. A drift stream inside an assured cosmetic scope still raises;
  a non-family stream name stays loud.
- **The outcome law (§11 no-bump)**: `drifted_from` names the pre-drift
  token — present only when picks[0] actually drifted; a refused telling
  never drifts (nothing transferred, nothing mutated).
- **The verbatim law**: the official watch briefing (crime_watch, D-006)
  never drifts — handovers transfer records verbatim; only the rumor
  path's telling reaction consults the families.
- **The lint laws**: the closed spec vocabulary; the orbit rides mintable
  tokens (dead vocabulary refused at load); no duplicate members; the
  one-sided membership law across families (two families sharing a token
  would couple their rolls over it — refused); >= 2 members; the ladder
  maps EVERY fidelity chain member to a 0..100 chance (a missing step
  would KeyError at the roll).
- **The corpus-price law (the both-arms pins)**: (iter-68a) a twin
  armed with an all-zero-chance family over the very token the rumor
  path tells vs the block-popped v0.1 twin — ten seeds byte-identical,
  the fingerprints identical: the armed family's rolls ride the
  isolated stream and never shift a canon byte (the engine-2
  add-safety pin's drift twin); (iter-68b) the ARMED committed pack vs
  the block-popped twin over the corpus geometries — byte-identical:
  every talk in the committed corpora tells a NON-member token (the
  narrator corpus's seed-15 noise, the parse corpus's arrival
  rumors), so no roll ever fires there — the measured price ZERO.
  The liveness law: a geometry whose teller holds the member token
  rolls — a hit (seed 2) mutates the outcome and the bytes; a miss
  (seed 1) keeps the v0.1 bytes verbatim.

Live-fire on CRAFTED packs (the iter-46 crafted-pack family): the
canonical seed-1 day1 geometry — the failed pickpocket (the guard's
partial sighting), the talk that shares it (told/vague), the rotation
briefing that hands the evidence over (verbatim, never drifted).
Live-fire on the COMMITTED pack (iter-68b): the guard-talk geometry
(seed 2 drifts, seed 1 misses) + the guard-pair traits pin (the
beliefwire-2 same-wave record).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from core.knowledge import drift_families, drifted_knows
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack
from core.rng import (
    COSMETIC,
    SUBSTANTIVE,
    RngBank,
    RngError,
    drift_stream_name,
)

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
DAY1_TALK: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": "npc_guard_01"},
    {"intent": "talk", "target": "npc_guard_01"},
]

GUARD = "npc_guard_01"
SOURCE, SIBLING = "figure_reaching_for_purse", "figure_starting_fire"
THIRD = "noise_by_the_bar"
LADDER_FULL = {"exact": 0, "partial": 0, "vague": 100}
LADDER_ZERO = {"exact": 0, "partial": 0, "vague": 0}


def _spec(
    tokens: list[str], ladder: dict[str, int] | None = None
) -> dict[str, Any]:
    return {"tokens": tokens, "ladder": ladder or LADDER_FULL}


def _duck_pack(
    families: dict[str, Any] | None,
) -> Any:
    """The unit-test pack stub: rules only, the shape `drift_families`
    reads (duck-typed — the module never imports pack.py at runtime)."""
    return SimpleNamespace(
        rules={"knowledge": {"fidelity_chain": ["exact", "partial", "vague"],
                             "drift": families}}
    )


def crafted_pack(
    tmp_path: Path, name: str, families: dict[str, Any] | None = None
) -> Pack:
    """A committed-pack copy with `knowledge.drift` set (or REMOVED when
    None — the v0.1 twin: the committed pack is armed since 68b, so the
    unarmed arm of every A/B pin is this crafted block-popped copy)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if families is None:
        rules["knowledge"].pop("drift", None)
    else:
        rules["knowledge"]["drift"] = families
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return load_pack(target)


def run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]], name: str,
) -> tuple[list[Any], Simulator]:
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events, sim


def by_type(events: list[Any], event_type: str) -> list[Any]:
    return [e for e in events if e.type == event_type]


# -- the mechanics (unit) ------------------------------------------------------


def test_the_index_and_the_empty_block() -> None:
    """`drift_families`: an absent or empty block answers the empty index
    (v0.1 bytes — the pack's own declaration is the arming); a declared
    block indexes every member to its family entry (pack order)."""
    assert drift_families(_duck_pack(None)) == {}
    assert drift_families(_duck_pack({})) == {}
    index = drift_families(_duck_pack({"f": _spec([SOURCE, SIBLING])}))
    assert set(index) == {SOURCE, SIBLING}
    entry = index[SOURCE]
    assert entry.family == "f"
    assert entry.tokens == (SOURCE, SIBLING)
    assert entry.ladder == LADDER_FULL
    # the committed pack is ARMED (68b): the figure_deeds family — the
    # two crime sightings, the monotone ladder (the vaguer, the likelier)
    committed = drift_families(PACK)
    assert set(committed) == {SOURCE, SIBLING}
    armed = committed[SOURCE]
    assert armed.family == "figure_deeds"
    assert armed.ladder == {"exact": 0, "partial": 30, "vague": 50}
    chances = [armed.ladder[run] for run in ("exact", "partial", "vague")]
    assert chances == sorted(chances)


def test_the_ladder_rolls_at_the_received_fidelity() -> None:
    """The chance is the RECEIVED fidelity's ladder entry: the source's
    own fidelity never enters (the mutation rides the degradation —
    phases.md's distorting medium). The same seed, one rung of received
    fidelity apart, answers drift vs no-drift — and a hit costs two
    draws (roll + pick) where a miss costs one."""
    families = drift_families(_duck_pack({"f": _spec([SOURCE, SIBLING])}))
    bank = RngBank(7)
    assert drifted_knows(bank, families, SOURCE, "vague") == SIBLING
    # partial carries chance 0 in LADDER_FULL: the same draw position,
    # a different answer, and the roll still consumed
    bank2 = RngBank(7)
    assert drifted_knows(bank2, families, SOURCE, "partial") == SOURCE
    assert bank.count(drift_stream_name("f")) == 2
    assert bank2.count(drift_stream_name("f")) == 1


def test_a_hit_picks_one_other_member_never_the_source() -> None:
    """The target is one uniform pick among the OTHER members: the source
    never answers itself; every other member is reachable (a 3-member
    orbit over probed seeds)."""
    families = drift_families(_duck_pack({"f": _spec([SOURCE, SIBLING, THIRD])}))
    answers = set()
    for seed in range(60):
        bank = RngBank(seed)
        answer = drifted_knows(bank, families, SIBLING, "vague")
        assert answer in (SOURCE, THIRD)
        answers.add(answer)
    assert answers == {SOURCE, THIRD}


def test_a_non_member_answers_itself_without_a_draw() -> None:
    """A token outside every family never rolls — no draw on any stream
    (the v0.1 path for every un-declared token, the committed pack's
    every token): the fingerprint and the family counter stay at zero."""
    families = drift_families(_duck_pack({"f": _spec([SOURCE, SIBLING])}))
    bank = RngBank(7)
    assert drifted_knows(bank, families, THIRD, "vague") == THIRD
    assert bank.fingerprint == 0


# -- the stream laws (isolation is law, D-095) ---------------------------------


def test_drift_rolls_count_on_the_family_stream_never_the_fingerprint() -> None:
    """Every drift draw advances the family's own counter — the
    substantive fingerprint never sees it (the T1 replay identity holds
    with drift live), and the family stream registers lazily."""
    families = drift_families(_duck_pack({"f": _spec([SOURCE, SIBLING])}))
    bank = RngBank(7)
    with bank.assure(SUBSTANTIVE):
        before = bank.fingerprint
        bank.randint(1, 100)  # the acceptance roll, a canon draw
        drifted_knows(bank, families, SOURCE, "vague")  # roll + pick
    assert bank.count(drift_stream_name("f")) == 2
    assert bank.fingerprint == before + 1


def test_two_families_rolls_never_mix() -> None:
    """Per-family streams: each family's draws advance only its own
    counter — the D-095 isolation law at the bank level (two armed
    families stay decoupled, exactly like two urgency entries: an
    added family never shifts the other's draw positions)."""
    index = drift_families(_duck_pack({
        "f": _spec([SOURCE, SIBLING]), "g": _spec([THIRD, "purse_missing"]),
    }))
    bank = RngBank(9)
    drifted_knows(bank, index, SOURCE, "vague")  # f: roll + pick
    drifted_knows(bank, index, THIRD, "vague")  # g: roll + pick
    assert bank.count(drift_stream_name("f")) == 2
    assert bank.count(drift_stream_name("g")) == 2


def test_a_drift_stream_nests_only_inside_the_substantive_scope() -> None:
    """The engine-2 family law extended: a drift-family stream may shadow
    the assured substantive run scope — and nothing else (a drift stream
    inside an assured cosmetic scope raises; a non-family stream name
    stays loud whatever the scope)."""
    stream = drift_stream_name("f")
    bank = RngBank(7)
    with bank.assure(SUBSTANTIVE):
        with bank.assure(stream):  # the legal nesting
            bank.randint(1, 100)
    with bank.assure(COSMETIC):
        with pytest.raises(RngError, match="cannot assure"):
            with bank.assure(stream):
                pass
    with pytest.raises(RngError, match="unknown stream"):
        with bank.assure("drift-f"):  # a drift-looking non-family name
            pass  # never reached — the typo stays loud


def test_the_same_seed_answers_the_same_drift() -> None:
    """Determinism (INV-2): two banks of the same seed answer identical
    drift sequences over the same (token, fidelity) walk — the streams
    are sha256-derived from seed+name, PYTHONHASHSEED-independent."""
    families = drift_families(_duck_pack({"f": _spec([SOURCE, SIBLING, THIRD])}))
    walk = [(SOURCE, "vague"), (SIBLING, "vague"), (THIRD, "partial")]
    runs = (
        [drifted_knows(RngBank(11), families, token, fidelity)
         for token, fidelity in walk]
        for _ in range(3)
    )
    first = next(runs)
    assert all(other == first for other in runs)


# -- the lint laws -------------------------------------------------------------


def _mutate_drift(
    tmp_path: Path, name: str, families: dict[str, Any]
) -> Path:
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["knowledge"]["drift"] = families
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return target


@pytest.mark.parametrize(
    ("families", "message"),
    [
        ({"f": _spec([SOURCE])}, ">= 2"),  # one-token orbit: dead vocabulary
        ({"f": _spec([SOURCE, SOURCE])}, "duplicates"),
        ({"f": _spec([SOURCE, "aldric_was_here"])}, "not mintable"),
        ({"f": dict(_spec([SOURCE, SIBLING]), weight=1)}, "unknown keys"),
        (
            {"f": _spec([SOURCE, SIBLING], {"exact": 0, "partial": 0})},
            "ladder must map",
        ),  # vague missing: would KeyError at the roll
        (
            {"f": _spec([SOURCE, SIBLING], {"exact": 0, "partial": 0, "vague": 101})},
            "ladder must map",
        ),  # out of bounds
        (
            {
                "f": _spec([SOURCE, SIBLING]),
                "g": _spec([SIBLING, THIRD]),  # SIBLING in two orbits
            },
            "already belongs to family",
        ),
    ],
)
def test_the_lint_refuses_dead_families(
    tmp_path: Path, families: dict[str, Any], message: str
) -> None:
    with pytest.raises(PackError, match=message):
        load_pack(_mutate_drift(tmp_path, "dead", families))


def test_the_lint_refuses_an_empty_block(tmp_path: Path) -> None:
    with pytest.raises(PackError, match="non-empty"):
        load_pack(_mutate_drift(tmp_path, "empty", {}))


def test_a_valid_family_loads(tmp_path: Path) -> None:
    """The 68b arming shape passes the lint: mintable orbit, full ladder,
    prose notes — and `drift_families` reads it back."""
    pack = crafted_pack(tmp_path, "valid", {"f": dict(
        _spec([SOURCE, SIBLING], LADDER_ZERO),
        notes="probe — the figure-deeds orbit, armed at zero chance",
    )})
    assert set(drift_families(pack)) == {SOURCE, SIBLING}


# -- the live-fire laws (crafted packs, the day1 geometry) ---------------------


def test_a_told_fact_drifts_and_the_outcome_names_the_source(
    tmp_path: Path,
) -> None:
    """Seed 1: the failed pickpocket leaves the guard a partial sighting;
    the talk shares it told/vague (D-007) — the family's vague rung is
    100, so the record the player receives carries the SIBLING token,
    and the outcome's `drifted_from` names the pre-drift token (EVENT_
    SCHEMA §11: an outcome payload addition, no bump). The guard's own
    record is untouched — telling copies, the medium mutates."""
    pack = crafted_pack(tmp_path, "armed", {"figure_deeds": _spec(
        [SOURCE, SIBLING], {"exact": 0, "partial": 100, "vague": 100},
    )})
    events, sim = run(tmp_path, pack, 1, DAY1_TALK, "drift.jsonl")
    telling = by_type(events, "rumor_told")[0]
    assert telling.outcome["accepted"] is True
    assert telling.outcome["knows"] == SIBLING
    assert telling.outcome["drifted_from"] == SOURCE
    assert telling.outcome["fidelity"] == "vague"
    player = [
        (r.knows, r.channel, r.fidelity)
        for r in sim.knowledge.records_of("pc_01")
    ]
    assert (SIBLING, "told", "vague") in player
    assert not any(knows == SOURCE for knows, _, _ in player)
    # the teller keeps the true token — the drift never rewrites memory
    guard = [
        (r.knows, r.channel, r.fidelity)
        for r in sim.knowledge.records_of(GUARD)
    ]
    assert (SOURCE, "saw", "partial") in guard


def test_the_novelty_gate_tests_the_teller_token(
    tmp_path: Path,
) -> None:
    """The mutation is the listener's medium, never the teller's model:
    the novelty gate tests the token the TELLER holds — the original
    stays tellable after a drift (the listener holds the sibling, not
    the source), and the re-telling mutates into the same sibling again
    (heard twice — the echo law's twin; the log is honest about both)."""
    pack = crafted_pack(tmp_path, "twice", {"figure_deeds": _spec(
        [SOURCE, SIBLING], {"exact": 0, "partial": 100, "vague": 100},
    )})
    steps = DAY1_TALK + [{"intent": "talk", "target": GUARD}]
    events, sim = run(tmp_path, pack, 1, steps, "twice.jsonl")
    tellings = by_type(events, "rumor_told")
    shared = [e.outcome["knows"] for e in tellings]
    assert shared.count(SOURCE) == 0 and shared[0] == SIBLING
    assert all(e.outcome.get("drifted_from") == SOURCE for e in tellings)
    learned = [
        r.knows for r in sim.knowledge.records_of("pc_01")
    ]
    assert learned.count(SIBLING) == len(tellings)  # re-learned, honestly


def test_a_refused_telling_never_drifts(tmp_path: Path) -> None:
    """A refused telling transfers nothing — nothing mutates: the
    outcome keeps the original token, carries no `drifted_from`, and no
    drift stream is ever registered (the roll is a function of the log's
    acceptances, never of the ladder's numbers)."""
    target = tmp_path / "deaf"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["knowledge"]["rumor_acceptance"]["base"] = -100  # never accepted
    rules["knowledge"]["drift"] = {"figure_deeds": _spec([SOURCE, SIBLING])}
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    deaf = load_pack(target)
    events, _ = run(tmp_path, deaf, 1, DAY1_TALK, "deaf.jsonl")
    telling = by_type(events, "rumor_told")[0]
    assert telling.outcome["accepted"] is False
    assert telling.outcome["knows"] == SOURCE  # the refused fact, verbatim
    assert "drifted_from" not in telling.outcome
    assert telling.knowledge == ()


def test_the_official_briefing_never_drifts(tmp_path: Path) -> None:
    """The verbatim law: the watch rotation's briefing (D-006 handover,
    not a rumor) transfers records as held — an armed family at 100%
    chance over the very tokens it hands over changes nothing (the drift
    consults only the telling reaction's picks; the briefing path has no
    gate). Seed 19: both failed-steal tokens (the sighting, the noise)
    pass verbatim, told one step down."""
    pack = crafted_pack(tmp_path, "verbatim", {"evidence": _spec(
        [SOURCE, SIBLING, THIRD], {"exact": 100, "partial": 100, "vague": 100},
    )})
    events, sim = run(tmp_path, pack, 19, [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "steal", "target": GUARD, "method": "distraction"},
        {"intent": "steal", "target": GUARD, "method": "distraction"},
        {"intent": "move", "target": "loc_backyard"},
        {"intent": "wait", "ticks": 400},  # crosses the rotation (t=360)
    ], "verbatim.jsonl")
    transfers = by_type(events, "knowledge_transfer")
    assert transfers  # the briefing ran
    guard_held = {
        r.knows for r in sim.knowledge.records_of(GUARD)
    }
    for transfer in transfers:
        assert "drifted_from" not in transfer.outcome
        # verbatim: every handed-over token is one the outgoing held —
        # the briefing invents nothing, mutates nothing
        for record in transfer.knowledge:
            assert record.knows in guard_held
            assert record.knows != SIBLING  # the armed orbit never fires here
    # the relief received the guard's family tokens, told one step down
    relief = [
        (r.knows, r.channel, r.fidelity)
        for r in sim.knowledge.records_of("npc_guard_02")
    ]
    assert (SOURCE, "told", "vague") in relief
    assert (THIRD, "told", "vague") in relief


# -- the corpus price (the both-arms pin) --------------------------------------


def test_the_add_safety_pin_armed_zero_chance_family_ten_seeds(
    tmp_path: Path,
) -> None:
    """The engine-2 add-safety pin's drift twin: the v0.1 twin (the
    block popped — the committed pack is armed since 68b, so the
    unarmed arm is crafted) vs a twin armed with an all-zero-chance
    family over the very token the rumor path tells — ten seeds
    byte-identical, the fingerprints identical. The armed family's
    rolls ride the isolated `drift:` stream (they HAPPEN — the ladder
    is zero, not the block absent), never a canon byte: isolation is
    law (D-095)."""
    twin = crafted_pack(tmp_path, "zero", {"figure_deeds": dict(
        _spec([SOURCE, SIBLING], LADDER_ZERO),
        notes="probe — armed at zero chance: the rolls happen, the "
              "mutations never do",
    )})
    unarmed = crafted_pack(tmp_path, "v01", None)
    told = 0
    for seed in range(120, 130):
        bytes_of: dict[str, bytes] = {}
        for label, p in (("twin", twin), ("v01", unarmed)):
            log = tmp_path / f"ab_{label}_{seed}.jsonl"
            sim = Simulator(p, seed, log, SCHEMA, commit="0000000")
            sim.run_playscript(
                {"name": "ab", "seed": seed, "pack": "tavern_pack@0.1",
                 "steps": DAY1_TALK}
            )
            sim.close()
            bytes_of[label] = log.read_bytes()
        assert bytes_of["twin"] == bytes_of["v01"], f"seed {seed} diverged"
        _, events = read_log(tmp_path / f"ab_twin_{seed}.jsonl", SCHEMA)
        told += sum(
            1 for e in events
            if e.type == "rumor_told" and e.outcome.get("accepted")
            and e.outcome["knows"] == SOURCE
        )
    # non-vacuity: the family token really passed the rumor path (the
    # drift stream rolled) in the pinned seeds
    assert told >= 1


# -- the committed arming (68b): the corpus price + the liveness ----------------


SEED15_TALK: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": GUARD, "method": "distraction"},
    {"intent": "steal", "target": GUARD, "method": "distraction"},
    {"intent": "take", "target": "oil_lamp_01"},
    {"intent": "talk", "target": "npc_drunk_01"},
]


def test_the_committed_arming_corpus_price_zero(tmp_path: Path) -> None:
    """The measured price (the both-arms law, 68b): the ARMED committed
    pack vs the block-popped v0.1 twin over the corpus geometries — the
    narrator corpus's seed-15 talk session (the drunk tells the noise, a
    non-member) and the day1_full ten-seed family (no talks at all) —
    byte-identical. Every talk in the committed corpora tells a
    non-member token, so no roll ever fires there: the arming costs the
    corpora nothing; the live corpus stays at its iter-13 fixed point
    (zero re-distill, zero regen)."""
    unarmed = crafted_pack(tmp_path, "v01", None)
    for seed in range(120, 130):
        for name, steps in (
            ("seed15", SEED15_TALK),
            ("day1_full", json.loads(
                (REPO / "tests" / "playscripts" / "day1_full.json")
                .read_text(encoding="utf-8")
            )["steps"]),
        ):
            bytes_of: dict[str, bytes] = {}
            for label, p in (("armed", PACK), ("v01", unarmed)):
                log = tmp_path / f"price_{label}_{name}_{seed}.jsonl"
                sim = Simulator(p, seed, log, SCHEMA, commit="0000000")
                sim.run_playscript(
                    {"name": name, "seed": seed, "pack": "tavern_pack@0.1",
                     "steps": steps}
                )
                sim.close()
                bytes_of[label] = log.read_bytes()
            assert bytes_of["armed"] == bytes_of["v01"], (
                f"{name} seed {seed} diverged"
            )
    # non-vacuity: the seed-15 session really fires a telling (the
    # noise the drunk shares) — an accepted non-member transfer
    log = tmp_path / "vacuity.jsonl"
    sim = Simulator(PACK, 15, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": "v", "seed": 15, "pack": "tavern_pack@0.1",
         "steps": SEED15_TALK}
    )
    sim.close()
    _, events = read_log(log, SCHEMA)
    telling = by_type(events, "rumor_told")[0]
    assert telling.outcome["accepted"] is True
    assert telling.outcome["knows"] == "noise_by_the_bar"
    assert "drifted_from" not in telling.outcome


GUARD_TALK: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": GUARD},
    {"intent": "talk", "target": GUARD},
]


def test_the_committed_family_is_live_a_hit_drifts(tmp_path: Path) -> None:
    """The liveness law (the both-arms second half): a geometry whose
    teller holds the member token ROLLS — seed 2 hits: the outcome's
    knows flips to the sibling, `drifted_from` names the sighting, the
    player's record carries the sibling, the teller keeps the true
    token, and the log bytes DIVERGE from the block-popped twin (the
    armed family is live canon, not declarative dead weight)."""
    unarmed = crafted_pack(tmp_path, "v01", None)
    bytes_of: dict[str, bytes] = {}
    for label, p in (("armed", PACK), ("v01", unarmed)):
        log = tmp_path / f"live_{label}.jsonl"
        sim = Simulator(p, 2, log, SCHEMA, commit="0000000")
        sim.run_playscript(
            {"name": "live", "seed": 2, "pack": "tavern_pack@0.1",
             "steps": GUARD_TALK}
        )
        sim.close()
        bytes_of[label] = log.read_bytes()
    assert bytes_of["armed"] != bytes_of["v01"]  # the hit is a real byte
    events, sim = run(tmp_path, PACK, 2, GUARD_TALK, "hit.jsonl")
    telling = by_type(events, "rumor_told")[0]
    assert telling.outcome["accepted"] is True
    assert telling.outcome["knows"] == SIBLING
    assert telling.outcome["drifted_from"] == SOURCE
    player = [
        (r.knows, r.channel, r.fidelity)
        for r in sim.knowledge.records_of("pc_01")
    ]
    assert (SIBLING, "told", "vague") in player
    assert not any(knows == SOURCE for knows, _, _ in player)
    guard = [
        (r.knows, r.channel, r.fidelity)
        for r in sim.knowledge.records_of(GUARD)
    ]
    assert (SOURCE, "saw", "partial") in guard


def test_a_miss_keeps_the_v0_1_bytes(tmp_path: Path) -> None:
    """The miss law: seed 1's roll misses (the same draw position that
    hit at seed 2) — the outcome keeps the token verbatim, no
    `drifted_from`, and the log bytes match the block-popped v0.1 twin
    exactly: the draw rode the isolated stream and shifted nothing
    (isolation is law, D-095; the miss is the v0.1 path in bytes)."""
    unarmed = crafted_pack(tmp_path, "v01", None)
    bytes_of: dict[str, bytes] = {}
    for label, p in (("armed", PACK), ("v01", unarmed)):
        log = tmp_path / f"miss_{label}.jsonl"
        sim = Simulator(p, 1, log, SCHEMA, commit="0000000")
        sim.run_playscript(
            {"name": "miss", "seed": 1, "pack": "tavern_pack@0.1",
             "steps": GUARD_TALK}
        )
        sim.close()
        bytes_of[label] = log.read_bytes()
    assert bytes_of["armed"] == bytes_of["v01"]
    events, _ = run(tmp_path, PACK, 1, GUARD_TALK, "miss.jsonl")
    telling = by_type(events, "rumor_told")[0]
    assert telling.outcome["accepted"] is True
    assert telling.outcome["knows"] == SOURCE
    assert "drifted_from" not in telling.outcome


def test_the_guard_pair_traits_survive_the_arming(tmp_path: Path) -> None:
    """The beliefwire-2 same-wave record (68b's TASKS row): the drift
    never touches the direct-mint records (the guard's own sighting,
    the inferred absence) nor the verbatim watch briefing — so the
    guard pair's paranoid_about_thieves crystallization on the
    canonical day1_full run is unchanged by the arming: guard_01 the
    two-source eyewitness, guard_02 the one-event hearsay shape. The
    live trait consumer's substrate (the fold's input) is
    byte-identical; the beliefwire-2 arming price stands as measured at
    iter-67."""
    from core.traits import crystallized_traits

    day1 = json.loads(
        (REPO / "tests" / "playscripts" / "day1_full.json")
        .read_text(encoding="utf-8")
    )["steps"]
    log = tmp_path / "traits.jsonl"
    sim = Simulator(PACK, 125, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": "t", "seed": 125, "pack": "tavern_pack@0.1", "steps": day1}
    )
    sim.close()
    _, events = read_log(log, SCHEMA)
    by_who = {
        t.who: t for t in crystallized_traits(PACK, sim.knowledge, events[-1].t)
    }
    assert set(by_who) == {GUARD, "npc_guard_02"}
    assert by_who[GUARD].token == "paranoid_about_thieves"
    assert len(by_who[GUARD].sources) == 2  # the sighting + the inference
    assert len(by_who["npc_guard_02"].sources) == 1  # the one-event hearsay
