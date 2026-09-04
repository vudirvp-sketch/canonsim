"""iter-55 acceptance — trait crystallization (leg-1, phase 4;
TASKS.md's leg-1 row: "phases.md §4 P3f — the LEGEND_SPEC sketch's trait
half: 3+ related knowledge records collapse into a discrete belief
token; traits are derived state, never stored as primary data").

The laws pinned here:

- **The read-model law (INV-1)**: the fold writes NOTHING — no events,
  no knowledge, no hooks, no state, no templates, no metrics. A pure
  fold over the knowledge view: a knower holding at least `threshold`
  DISTINCT tokens of a declared family crystallizes the belief,
  carrying the contributing records' source event ids as provenance
  (the expansion law — the trait expands back to source records for
  the brief; the source is always queryable, the belief a derived
  view, never a replacement).
- **The breadth law**: distinct tokens against the threshold —
  repetition is the echo's business (renewal), not crystallization.
- **The stability law**: no decay term — records are never dropped
  (INV-1), so the evidence holds while the log holds; `at_tick` gates
  CONTRIBUTION (the honest read-model law shared with the echo), never
  the belief's persistence.
- **The dormancy law, post leg-2**: the CANON loop never imports
  `core.traits` (the write side stays untouched — the day1_full
  10-seed A/B is byte-identical through the landing, iter-55 and
  iter-56); the fold's first consumer is the brief's read-side lens
  (leg-2, `brief/assembler.py::_recalled_fact_lines` — BRIEF_SPEC
  §3.5), which reads the fold as DATA and writes nothing.
- **The L6 fence**: a belief is per-NPC derived state over the NPC's
  own records — never player-adapted, never an entropy input; the
  director is untouched by construction (DIRECTOR_SPEC §4).
- **The lint laws**: closed vocabularies, threshold >= 2 (one record
  is a fact, not a belief), family >= threshold (dead vocabulary
  refused), family tokens mintable, one-sided membership (a token
  feeds exactly one belief), the belief token never collides with a
  mintable knowledge token.

Live-fire on the COMMITTED pack (the canonical day1_full, seed 125):
the guard pair crystallizes `paranoid_about_thieves` — guard_01 the
eyewitness (sighting + inference, two source events), guard_02 the
hearsay knower (the watch transfer minted all three tokens in one
event — provenance length 1); the room's other witnesses hold two
tokens and honestly stay uncrystallized. The mechanism-isolation
tests below craft events directly (the iter-46 crafted-pack family).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.knowledge import KnowledgeView
from core.log import EventRecord, LoggedKnowledgeRecord, read_log
from core.loop import Simulator
from core.pack import PackError, load_pack
from core.traits import Trait, crystallized_traits, expand_trait

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
DAY1 = json.loads((REPO / "tests" / "playscripts" / "day1_full.json").read_text())

# the committed block's own vocabulary (the live-fire pins read it)
FAMILY = ("figure_reaching_for_purse", "noise_by_the_bar", "purse_missing")
GUARD, RELIEF, MAID = "npc_guard_01", "npc_guard_02", "npc_maid_01"


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


def tuned_pack(tmp_path: Path, mutate: Any) -> Any:
    """A committed-pack copy with the `traits` block replaced by
    `mutate(rules)` (the hard_pack pattern): the crafted-block tests
    stay isolated from the committed live set."""
    target = tmp_path / "pack_traits"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    mutate(rules)
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return load_pack(target)


def run_day1(tmp_path: Path) -> tuple[list[EventRecord], KnowledgeView]:
    log = tmp_path / "day1_traits.jsonl"
    sim = Simulator(PACK, DAY1["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(DAY1)
    sim.close()
    _header, events = read_log(log, SCHEMA)
    return events, KnowledgeView.from_events(events)


# -- the read model -----------------------------------------------------


def test_the_fold_is_pure_and_idempotent(tmp_path: Path) -> None:
    """INV-1's read-model proof: the fold mutates nothing (the view's
    rows identical before/after) and two reads agree exactly (INV-2 —
    construction order only, no randomness anywhere in the fold)."""
    events, view = run_day1(tmp_path)
    before = {who: view.records_of(who) for who in view.knowers()}
    first = crystallized_traits(PACK, view, events[-1].t)
    second = crystallized_traits(PACK, view, events[-1].t)
    after = {who: view.records_of(who) for who in view.knowers()}
    assert first == second
    assert before == after


def test_no_block_folds_empty(tmp_path: Path) -> None:
    """The INV-3 gate: a pack without the block folds the empty tuple —
    the v0.1 behavior, byte-identical (the pack's own declaration is
    the gate)."""

    def strip(rules: dict[str, Any]) -> None:
        del rules["traits"]

    pack = tuned_pack(tmp_path, strip)
    events, view = run_day1(tmp_path)
    assert crystallized_traits(pack, view, events[-1].t) == ()


# -- the mechanics (crafted events over the committed block) ------------


def test_the_threshold_law(tmp_path: Path) -> None:
    """Two of three family tokens: no belief. The third lands: the
    belief crystallizes — breadth counted at the read, not promised."""
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, FAMILY[0], 1, "a"),)))
    view.add(_ev("b", 2, (_rec(GUARD, FAMILY[1], 2, "b"),)))
    t_two = 2
    assert crystallized_traits(PACK, view, t_two) == ()
    view.add(_ev("c", 3, (_rec(GUARD, FAMILY[2], 3, "c"),)))
    traits = crystallized_traits(PACK, view, 3)
    assert traits == (Trait(who=GUARD, token="paranoid_about_thieves",
                            sources=("a", "b", "c")),)


def test_breadth_not_repetition(tmp_path: Path) -> None:
    """Three records of ONE token do not crystallize (threshold 3,
    distinct tokens 1 — repetition is the echo's renewal, never
    crystallization); two more DISTINCT tokens do."""
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, FAMILY[0], 1, "a"),)))
    view.add(_ev("b", 2, (_rec(GUARD, FAMILY[0], 2, "b"),)))
    view.add(_ev("c", 3, (_rec(GUARD, FAMILY[0], 3, "c"),)))
    assert crystallized_traits(PACK, view, 3) == ()
    view.add(_ev("d", 4, (_rec(GUARD, FAMILY[1], 4, "d"),)))
    view.add(_ev("e", 5, (_rec(GUARD, FAMILY[2], 5, "e"),)))
    traits = crystallized_traits(PACK, view, 5)
    assert len(traits) == 1
    # the duplicate token's records all ride the provenance — evidence
    # is evidence; the COUNT is what stays distinct-only
    assert traits[0].sources == ("a", "b", "c", "d", "e")


def test_at_tick_gates_contribution(tmp_path: Path) -> None:
    """The honest read-model law: a record born after `at_tick`
    contributes nothing — the belief is absent at the earlier read and
    present at the crossing tick (read as DATA at the caller's own
    tick, the window law shared with the echo)."""
    view = KnowledgeView()
    view.add(_ev("a", 10, (_rec(GUARD, FAMILY[0], 10, "a"),)))
    view.add(_ev("b", 20, (_rec(GUARD, FAMILY[1], 20, "b"),)))
    view.add(_ev("c", 30, (_rec(GUARD, FAMILY[2], 30, "c"),)))
    assert crystallized_traits(PACK, view, 29) == ()
    assert crystallized_traits(PACK, view, 30) == (
        Trait(who=GUARD, token="paranoid_about_thieves", sources=("a", "b", "c")),
    )


def test_provenance_dedupes_event_ids(tmp_path: Path) -> None:
    """One event minting two family records is ONE source event —
    provenance is event ids, deduped first-seen, acquisition order (the
    hearsay shape: the day1 relief guard's whole belief from one
    transfer event)."""
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, FAMILY[0], 1, "a"),
                          _rec(GUARD, FAMILY[1], 1, "a"))))
    view.add(_ev("b", 2, (_rec(GUARD, FAMILY[2], 2, "b"),)))
    traits = crystallized_traits(PACK, view, 2)
    assert traits[0].sources == ("a", "b")


def test_blind_knower_stays_blind(tmp_path: Path) -> None:
    """A knower outside the family (one unrelated token) folds nothing
    — T3's honesty at the trait layer: no record, no belief."""
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(MAID, "pc_01_arrived", 1, "a"),)))
    assert crystallized_traits(PACK, view, 1) == ()


def test_declaration_and_acquisition_order(tmp_path: Path) -> None:
    """INV-2: beliefs in declaration order, knowers in first-acquisition
    order — construction order only, stable across reads."""

    def two_beliefs(rules: dict[str, Any]) -> None:
        rules["traits"] = {
            "threshold": 2,
            "beliefs": {
                "first_belief": {
                    "family": [FAMILY[0], FAMILY[1]],
                },
                "second_belief": {
                    "family": ["figure_starting_fire", "papers_unsatisfactory"],
                },
            },
        }

    pack = tuned_pack(tmp_path, two_beliefs)
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, FAMILY[0], 1, "a"),)))
    view.add(_ev("b", 2, (_rec(MAID, "figure_starting_fire", 2, "b"),)))
    view.add(_ev("c", 3, (_rec(GUARD, FAMILY[1], 3, "c"),)))
    view.add(_ev("d", 4, (_rec(MAID, "papers_unsatisfactory", 4, "d"),)))
    traits = crystallized_traits(pack, view, 4)
    assert [(t.who, t.token) for t in traits] == [
        (GUARD, "first_belief"),  # guard acquired first
        (MAID, "second_belief"),
    ]


# -- live-fire on the committed pack -------------------------------------


def test_the_canonical_crystallization(tmp_path: Path) -> None:
    """The live pin (measured at the landing, day1_full seed 125): the
    guard pair crystallizes paranoid_about_thieves — the eyewitness
    (guard_01: sighting + inference, two source events) and the hearsay
    knower (guard_02: the transfer minted all three tokens in one
    event); the room's other witnesses hold two tokens and stay
    uncrystallized; every source id resolves to a real log event."""
    events, view = run_day1(tmp_path)
    traits = crystallized_traits(PACK, view, events[-1].t)
    by_who = {t.who: t for t in traits}
    assert set(by_who) == {GUARD, RELIEF}
    assert by_who[GUARD].token == "paranoid_about_thieves"
    assert len(by_who[GUARD].sources) == 2  # the sighting + the inference
    assert len(by_who[RELIEF].sources) == 1  # the one-event hearsay shape
    ids = {event.id for event in events}
    assert all(s in ids for t in traits for s in t.sources)


# -- the expansion law (leg-2's demand side) -----------------------------


def test_expand_trait_returns_the_family_records() -> None:
    """The expansion law: the trait expands back to its source records —
    EVERY family record the knower holds in acquisition order, evidence
    is evidence (not just the threshold-crossing subset); the non-family
    record stays out."""
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, FAMILY[0], 1, "a"),)))
    view.add(_ev("b", 2, (_rec(GUARD, "pc_01_arrived", 2, "b"),)))
    view.add(_ev("c", 3, (_rec(GUARD, FAMILY[1], 3, "c"),)))
    view.add(_ev("d", 4, (_rec(GUARD, FAMILY[2], 4, "d"),)))
    trait = Trait(who=GUARD, token="paranoid_about_thieves",
                  sources=("a", "c", "d"))
    assert [r.knows for r in expand_trait(PACK, view, trait)] == [
        FAMILY[0], FAMILY[1], FAMILY[2],
    ]


def test_expand_trait_unknown_token_folds_empty() -> None:
    """A trait whose belief the pack no longer declares (crafted views —
    packs are never edited under a live log) expands to the honest empty
    answer, never an error."""
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, FAMILY[0], 1, "a"),)))
    ghost = Trait(who=GUARD, token="no_such_belief", sources=("a",))
    assert expand_trait(PACK, view, ghost) == ()


def test_expansion_purity() -> None:
    """The expansion is a read like the fold: two reads agree, the view's
    rows are untouched (INV-1 by construction)."""
    view = KnowledgeView()
    view.add(_ev("a", 1, (_rec(GUARD, FAMILY[0], 1, "a"),)))
    view.add(_ev("b", 2, (_rec(GUARD, FAMILY[1], 2, "b"),)))
    view.add(_ev("c", 3, (_rec(GUARD, FAMILY[2], 3, "c"),)))
    trait = crystallized_traits(PACK, view, 3)[0]
    before = {who: view.records_of(who) for who in view.knowers()}
    first = expand_trait(PACK, view, trait)
    second = expand_trait(PACK, view, trait)
    after = {who: view.records_of(who) for who in view.knowers()}
    assert first == second
    assert before == after


def test_the_canonical_expansion(tmp_path: Path) -> None:
    """The live pin: guard_01's crystallized belief expands back to its
    full family evidence — the sighting, the noise, the inferred
    absence — while the log holds them untouched (the expansion law on
    the canonical run)."""
    events, view = run_day1(tmp_path)
    traits = crystallized_traits(PACK, view, events[-1].t)
    guard_trait = next(t for t in traits if t.who == GUARD)
    records = expand_trait(PACK, view, guard_trait)
    assert sorted(r.knows for r in records) == sorted(FAMILY)
    assert {r.source for r in records} == set(guard_trait.sources)


# -- the pack lint --------------------------------------------------------


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda r: r["traits"].__setitem__("threshold", 1),
            "integer >= 2",
        ),
        (
            lambda r: r["traits"].__setitem__("threshold", 4),
            "can never reach threshold",
        ),
        (
            lambda r: r["traits"]["beliefs"]["paranoid_about_thieves"]["family"]
            .append("no_such_token"),
            "not mintable",
        ),
        (
            lambda r: r["traits"]["beliefs"].__setitem__(
                "twin_belief",
                {"family": [FAMILY[0], "figure_starting_fire"]},
            ),
            "already belongs to belief",
        ),
        (
            lambda r: r["traits"]["beliefs"].__setitem__(
                "purse_missing",
                {"family": ["figure_starting_fire", "papers_unsatisfactory"]},
            ),
            "two vocabularies",
        ),
        (
            lambda r: r["traits"].__setitem__("unknown_key", 1),
            "unknown keys",
        ),
        (
            lambda r: r["traits"]["beliefs"]["paranoid_about_thieves"]
            .__setitem__("unknown_key", 1),
            "unknown keys",
        ),
        (
            lambda r: r["traits"]["beliefs"]["paranoid_about_thieves"]["family"]
            .append(FAMILY[0]),
            "duplicate tokens",
        ),
        (
            lambda r: r.__setitem__("traits", [1, 2]),
            "must be an object",
        ),
    ],
)
def test_the_lint_refuses_dead_vocabulary(
    tmp_path: Path, mutate: Any, message: str
) -> None:
    """The KI#15 family, load-time: every authoring smell that would
    KeyErrors mid-run or declare dead vocabulary is refused at load —
    the closed-vocabulary law the secrets/echo lints set."""
    with pytest.raises(PackError, match=message):
        tuned_pack(tmp_path, mutate)
