"""iter-57 acceptance — reflection & memory compaction (leg-3, phase 4;
TASKS.md's leg-3 row: "phases.md §4 — reflection provenance
`list[event_id]`, the source outranks the reflection's recency on
contradiction, the `stale` flag, reflection-on-recurrence never
`summarize_messages_in_place`; LEGEND_SPEC.md written just-in-time at
this row"). The contract owner is `docs/LEGEND_SPEC.md`.

The laws pinned here:

- **The compaction law (INV-1/INV-5)**: reflection-on-recurrence — a
  knower whose held records of a declared family reach the block's
  `threshold` (REPEATS, not distinct tokens — breadth is the traits'
  business) mints ONE reflection EVENT through the canon door; the
  originals are never dropped and never edited. letta's
  `summarize_messages_in_place` is the named anti-pattern: nothing is
  ever rewritten in place.
- **The provenance law**: the reflection event's `outcome.provenance`
  is the `list[event_id]` of the source records it summarizes; the
  source is always queryable (the expansion law), the reflection a
  derived view, never a replacement.
- **The never-re-reflect law**: one mint per (knower, insight) per
  run — the insight token is held knowledge from its mint on, and
  records are never dropped, so the gate holds forever.
- **The stale law (read side)**: a reflection whose provenance no
  longer resolves is flagged and excluded from retrieval. In the
  runtime log this is impossible by construction (INV-1); the flag
  exists for derived stores after offline scavenge (leg-4) and the
  retrieval consumer (retr-1) must consult it.
- **The L6 fence**: the reflection draft carries NO hooks and NO
  state changes — the director buffer is untouched, entropy never
  reads a knowledge-derived entry; the cascade terminates by
  construction.
- **The dormancy law**: the committed v0.1 pack carries no
  `reflection` block — the run is byte-identical through the landing
  (the 10-seed day1_full A/B, seeds 120..129); the TASKS arming row
  owns the corpus price (the measured recurrence: seeds 123/128).
- **The lint laws**: closed vocabularies, threshold >= 2 (a first
  occurrence is an event, not a recurrence), the event type renders,
  family tokens mintable and one-sided, the insight token never
  collides with the mintable knowledge vocabulary.

Live-fire on the CRAFTED pack (the iter-46 crafted-block family): the
committed pack has no block, so every live-fire test copies the pack
and declares one — the probe insight `sneak_at_work_here` over the
`figure_reaching_for_purse` family, the measured day1_full seed-123
recurrence (the PC retries the theft; the room's other witnesses hold
the sighting once and honestly stay unreflected).
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
from core.reflection import (
    expand_reflection,
    reflection_drafts,
    stale_reflections,
)

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
DAY1 = json.loads((REPO / "tests" / "playscripts" / "day1_full.json").read_text())

# the crafted block's own vocabulary (the live-fire pins read it)
INSIGHT = "sneak_at_work_here"
FAMILY = ("figure_reaching_for_purse",)
GUARD = "npc_guard_01"
REFLECTION_EVENT = "reflection_had"


def _rec(who: str, knows: str, at: int, source: str) -> LoggedKnowledgeRecord:
    return LoggedKnowledgeRecord(
        who=who, channel="saw", fidelity="partial", knows=knows, at=at, source=source,
    )


def _ev(
    eid: str,
    t: int,
    knowledge: tuple[LoggedKnowledgeRecord, ...],
    etype: str = "wait",
) -> EventRecord:
    return EventRecord(
        id=eid, t=t, type=etype, actor="pc_01", cause=None, outcome={},
        knowledge=knowledge, state_changes=(), hooks=(),
        importance="low", provenance={"seed": 123}, target=None,
    )


def crafted_pack(tmp_path: Path, mutate: Any = None) -> Any:
    """A committed-pack copy with the probe `reflection` block declared
    (the hard_pack pattern); `mutate(rules)` edits the block before the
    load — the lint family's one door. Idempotent on the target dir
    (the fixed probe paths reuse it across tests)."""
    target = tmp_path / "pack_reflection"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    templates["events"][REFLECTION_EVENT] = (
        "{actor} had seen it before, and named it: {knows}"
    )
    rules["reflection"] = {
        "event": REFLECTION_EVENT,
        "threshold": 2,
        "reflections": {
            INSIGHT: {
                "family": list(FAMILY),
                "notes": "the probe insight: a repeated sighting compacts",
            },
        },
        "notes": "probe block — the committed pack stays block-less",
    }
    if mutate is not None:
        mutate(rules)
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    (target / "templates.json").write_text(
        json.dumps(templates, indent=2), encoding="utf-8"
    )
    return load_pack(target)


def run_crafted(tmp_path: Path, seed: int = 123) -> list[EventRecord]:
    log = tmp_path / f"day1_reflection_{seed}.jsonl"
    script = dict(DAY1)
    script["seed"] = seed
    sim = Simulator(crafted_pack(tmp_path), seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _header, events = read_log(log, SCHEMA)
    return events


# -- the mint ------------------------------------------------------------


def test_no_block_yields_nothing_and_the_run_is_v0_1(tmp_path: Path) -> None:
    """The dormancy law: the committed pack declares no block, so the
    mint yields nothing, the log holds no reflection events, and the
    read side folds empty — the byte-identical v0.1 behavior (the
    10-seed A/B witness measured at the landing)."""
    log = tmp_path / "day1_v01.jsonl"
    script = dict(DAY1)
    script["seed"] = 125
    sim = Simulator(PACK, 125, log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _header, events = read_log(log, SCHEMA)
    view = KnowledgeView.from_events(events)
    assert "reflection" not in PACK.rules
    drafts = list(
        reflection_drafts(PACK, view, events[1])
    )
    assert drafts == []
    assert stale_reflections(PACK, events) == frozenset()


def test_the_mint_fires_at_the_threshold_crossing(tmp_path: Path) -> None:
    """The compaction law, live: the PC's second theft attempt (the
    measured seed-123 recurrence) mints exactly ONE reflection event at
    the second sighting's tick, cause-chained to the triggering event,
    committed through the canon door."""
    events = run_crafted(tmp_path)
    minted = [e for e in events if e.type == REFLECTION_EVENT]
    assert len(minted) == 1
    event = minted[0]
    assert event.actor == GUARD
    assert event.cause == "ev_0015"  # the second pickpocket attempt
    assert event.t == 12  # the second sighting's tick — the crossing
    # the cascade terminates: the reflection event's own reaction pass
    # mints nothing (no recursion — exactly one event in the log)
    assert sum(1 for e in events if e.type == REFLECTION_EVENT) == 1


def test_provenance_is_the_source_event_id_list(tmp_path: Path) -> None:
    """The provenance law: `outcome.provenance` is the list of source
    event ids the reflection summarizes — every id resolves to an event
    that minted a contributing family record for the reflector."""
    events = run_crafted(tmp_path)
    event = next(e for e in events if e.type == REFLECTION_EVENT)
    provenance = event.outcome["provenance"]
    assert provenance == ["ev_0002", "ev_0015"]
    assert event.outcome["recurrence"] == 2
    by_id = {e.id: e for e in events}
    for source in provenance:
        source_event = by_id[source]
        assert any(
            record.who == GUARD and record.knows in FAMILY
            for record in source_event.knowledge
        )


def test_the_minted_record_is_inferred_exact_knowledge(tmp_path: Path) -> None:
    """The minted entry: one knowledge record for the reflector —
    channel `inferred` (P2d's channel: an inference from one's own
    memory), fidelity `exact` (the reflection states what is held; the
    evidence's quality rides the provenance), `source` stamped by the
    writer as the reflection event's own id."""
    events = run_crafted(tmp_path)
    event = next(e for e in events if e.type == REFLECTION_EVENT)
    assert len(event.knowledge) == 1
    record = event.knowledge[0]
    assert record.who == GUARD
    assert record.channel == "inferred"
    assert record.fidelity == "exact"
    assert record.knows == INSIGHT
    assert record.at == event.t
    assert record.source == event.id


def test_below_threshold_nothing_mints() -> None:
    """The floor: one held record is an occurrence, not a recurrence —
    no draft below the block's threshold (the honest answer, never an
    error)."""
    pack = crafted_pack(Path("/tmp/refl_probe"))
    view = KnowledgeView()
    first = _ev("ev_0001", 5, (_rec(GUARD, FAMILY[0], 5, "ev_0001"),))
    view.add(first)
    assert list(reflection_drafts(pack, view, first)) == []


def test_never_re_reflect_a_third_recurrence() -> None:
    """The never-re-reflect law: the insight is held knowledge from its
    mint on — a THIRD family record changes the expansion's evidence
    but never mints again (one compaction per (knower, insight) per
    run; records are never dropped, INV-1). The direct call follows
    the runtime discipline: the triggering event's records enter the
    view BEFORE the drafts read it (the commit door's own order)."""
    pack = crafted_pack(Path("/tmp/refl_probe2"))
    view = KnowledgeView()
    for eid, t in (("ev_0001", 5), ("ev_0002", 9)):
        view.add(_ev(eid, t, (_rec(GUARD, FAMILY[0], t, eid),)))
    second = _ev("ev_0002", 9, (_rec(GUARD, FAMILY[0], 9, "ev_0002"),))
    drafts = list(reflection_drafts(pack, view, second))
    assert len(drafts) == 1  # the mint at the crossing
    # the mint's record joins the view (the writer stamps its own id)
    view.add(
        _ev(
            "ev_0003", 9,
            (LoggedKnowledgeRecord(
                who=GUARD, channel="inferred", fidelity="exact",
                knows=INSIGHT, at=9, source="ev_0003",
            ),),
        )
    )
    third = _ev("ev_0004", 20, (_rec(GUARD, FAMILY[0], 20, "ev_0004"),))
    view.add(third)
    assert list(reflection_drafts(pack, view, third)) == []


def test_one_reflection_per_knower_per_event() -> None:
    """The within-event dedup: an event minting two family records for
    the same knower (the `seen` guard) yields ONE draft — the leverage
    reaction's own law. The view carries the runtime discipline: the
    triggering event's records are in it before the drafts read."""
    pack = crafted_pack(Path("/tmp/refl_probe3"))
    view = KnowledgeView()
    view.add(_ev("ev_0001", 5, (_rec(GUARD, FAMILY[0], 5, "ev_0001"),)))
    twin = _ev(
        "ev_0002", 9,
        (_rec(GUARD, FAMILY[0], 9, "ev_0002"), _rec(GUARD, FAMILY[0], 9, "ev_0002")),
    )
    view.add(twin)
    drafts = list(reflection_drafts(pack, view, twin))
    assert len(drafts) == 1


def test_ambient_groups_never_reflect(tmp_path: Path) -> None:
    """The knower gate: an ambient group does not reflect in v0.1 —
    the leverage knower law (a crowd holds records, never draws
    conclusions of its own)."""
    pack = crafted_pack(tmp_path)
    view = KnowledgeView()
    crowd = "npc_market_crowd_01"
    for eid, t in (("ev_0001", 5), ("ev_0002", 9)):
        view.add(_ev(eid, t, (_rec(crowd, FAMILY[0], t, eid),)))
    second = _ev("ev_0002", 9, (_rec(crowd, FAMILY[0], 9, "ev_0002"),))
    assert list(reflection_drafts(pack, view, second)) == []


def test_the_insight_is_ordinary_knowledge(tmp_path: Path) -> None:
    """From its mint on, the insight is an ordinary knowledge record:
    held (`view.holds`), present in the knower's memory in acquisition
    order — tellable onward at the telling reaction's own fidelity
    decay, salient in the fold like any record (organic canon, no
    special casing)."""
    events = run_crafted(tmp_path)
    view = KnowledgeView.from_events(events)
    assert view.holds(GUARD, INSIGHT)
    assert any(
        record.knows == INSIGHT for record in view.records_of(GUARD)
    )


def test_the_mint_is_deterministic_and_rng_free(tmp_path: Path) -> None:
    """INV-2: the reflection is an inference, not a stochastic act —
    no acceptance roll (the telling rolls; the reflection does not),
  and the same seed replays byte-identically."""
    first = run_crafted(tmp_path, seed=123)
    log2 = tmp_path / "day1_reflection_123_again.jsonl"
    script = dict(DAY1)
    script["seed"] = 123
    sim = Simulator(crafted_pack(tmp_path / "again"), 123, log2, SCHEMA,
                    commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _header, second = read_log(log2, SCHEMA)
    assert [e.id for e in first] == [e.id for e in second]
    assert [dict(e.outcome) for e in first] == [dict(e.outcome) for e in second]


def test_the_director_is_untouched_l6(tmp_path: Path) -> None:
    """The L6 fence, structural: the reflection event carries NO hooks
    (the director buffer never seeds from it) and NO state changes
    (suspicion never moves) — entropy reads observable state only, and
    a knowledge-derived entry is not observable state."""
    events = run_crafted(tmp_path)
    event = next(e for e in events if e.type == REFLECTION_EVENT)
    assert event.hooks == ()
    assert event.state_changes == ()


# -- the read side -------------------------------------------------------


def test_stale_never_fires_on_a_whole_log(tmp_path: Path) -> None:
    """INV-1's read-side twin: the log never drops originals, so every
    minted provenance id resolves — the stale fold is empty on any
    whole runtime log, by construction."""
    events = run_crafted(tmp_path)
    pack = crafted_pack(tmp_path / "stale_pack")
    assert stale_reflections(pack, events) == frozenset()


def test_stale_fires_after_scavenge(tmp_path: Path) -> None:
    """The stale law's live arm: in a DERIVED store after offline
    scavenge (leg-4's tombstones — the log itself is never edited,
    INV-5), a reflection whose provenance no longer resolves is
    flagged — the screening the retrieval consumer (retr-1) must
    consult before serving the entry."""
    events = run_crafted(tmp_path)
    pack = crafted_pack(tmp_path / "stale_pack2")
    scavenged = [e for e in events if e.id != "ev_0002"]
    assert stale_reflections(pack, scavenged) == frozenset({"ev_0016"})


def test_expansion_returns_every_family_record(tmp_path: Path) -> None:
    """The expansion law (the `expand_trait` twin): every family record
    the reflector holds, in acquisition order — the mint-time
    provenance is the subset; evidence is evidence, a post-mint
    recurrence record expands too."""
    events = run_crafted(tmp_path)
    pack = crafted_pack(tmp_path / "expand_pack")
    view = KnowledgeView.from_events(events)
    event = next(e for e in events if e.type == REFLECTION_EVENT)
    records = expand_reflection(pack, view, event)
    assert [r.knows for r in records] == [FAMILY[0], FAMILY[0]]
    assert [r.source for r in records] == ["ev_0002", "ev_0015"]


def test_expansion_unknown_about_folds_empty(tmp_path: Path) -> None:
    """A reflection whose `about` token the block no longer declares
    expands to the empty tuple — the honest answer, never an error
    (the crafted-view law shared with the traits)."""
    events = run_crafted(tmp_path)
    pack = crafted_pack(tmp_path / "expand_pack2")
    view = KnowledgeView.from_events(events)
    drifted = EventRecord(
        id="ev_9000", t=30, type=REFLECTION_EVENT, actor=GUARD, cause=None,
        outcome={"about": "renamed_insight", "provenance": [], "recurrence": 2},
        knowledge=(), state_changes=(), hooks=(), importance="low",
        provenance={"seed": 123}, target=None,
    )
    assert expand_reflection(pack, view, drifted) == ()


# -- the lint family -----------------------------------------------------


def _lint_case(tmp_path: Path, mutate: Any) -> str:
    with pytest.raises(PackError) as info:
        crafted_pack(tmp_path, mutate)
    return str(info.value)


def test_lint_closed_block_keys(tmp_path: Path) -> None:
    """Unknown keys are a load error, never a silent ignore."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["reflection"]["weight"] = 3

    assert "reflection: unknown keys" in _lint_case(tmp_path, mutate)


def test_lint_threshold_floor(tmp_path: Path) -> None:
    """A threshold of 1 would compact a first occurrence — an event,
    not a recurrence; refused at load."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["reflection"]["threshold"] = 1

    assert "threshold" in _lint_case(tmp_path, mutate)


def test_lint_event_type_must_render(tmp_path: Path) -> None:
    """EVENT_SCHEMA §11: the reflection event renders in the chronicle
    — an undeclared type is dead vocabulary."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["reflection"]["event"] = "daydream_had"

    assert "template vocabulary" in _lint_case(tmp_path, mutate)


def test_lint_family_tokens_must_be_mintable(tmp_path: Path) -> None:
    """A token no declared template can mint is dead vocabulary — the
    recurrence would never fire (the secrets/echo/traits law)."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["reflection"]["reflections"][INSIGHT]["family"] = [
            "token_nobody_mints",
        ]

    assert "not mintable" in _lint_case(tmp_path, mutate)


def test_lint_one_sided_membership(tmp_path: Path) -> None:
    """A family token feeding two insights double-counts one
    recurrence across tables — refused at load."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["reflection"]["reflections"]["second_insight"] = {
            "family": list(FAMILY),
        }

    assert "one-sided membership" in _lint_case(tmp_path, mutate)


def test_lint_insight_token_vocabulary_hygiene(tmp_path: Path) -> None:
    """The traits law: an insight token colliding with a mintable
    knowledge token puts one string in two vocabularies — the template
    mint would hold it and the never-re-reflect gate would block the
    fold's own mint forever."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["reflection"]["reflections"] = {
            FAMILY[0]: {"family": ["noise_by_the_bar"]},
        }

    assert "two vocabularies" in _lint_case(tmp_path, mutate)


def test_lint_duplicate_family_entries(tmp_path: Path) -> None:
    """A duplicate family token double-counts one recurrence — dead
    data, refused at load."""

    def mutate(rules: dict[str, Any]) -> None:
        rules["reflection"]["reflections"][INSIGHT]["family"] = [
            FAMILY[0],
            FAMILY[0],
        ]

    assert "duplicate" in _lint_case(tmp_path, mutate)
