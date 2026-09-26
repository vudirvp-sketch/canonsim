"""temp-1 — the temporal contracts landed (A2 + B2/B3; B1 deferred).

The owner's 2026-09-26 contract pick over the fork card in
`docs/blueprint/phases.md` §6 (D-236): (a) **A2 crossing-family
equivalence** — the wait-slicing contract pins ONLY the measured
crossing-committed invariance, never full slice equivalence; (b) **B2
deferred-realize stays the runtime semantics** (the beat-minted
autonomous intent's door may land far after its beat) while **B3**
records the semantic origin (`provenance.assignment_tick`) separately
from the canonical realization time `event.t`; **B1 generate-at-T is
DEFERRED** — an owner-gated future scheduler decision, never touched
here.

A2's declared scope (`R_crossing`, tavern): the crossing-committed
families — `status_decayed` (the beat's decay pass), `watch_change` /
`knowledge_transfer` / `expectation_violation` (the rotation machinery:
the post swap, the briefing, the expectation checks) — committed INLINE
at the crossing tick. The door-committed families (everything resolving
through the intent door — player steps and autonomous urgency / faction
/ director intents, the whole OCC / opposed-check / completion chain)
are FREE to diverge between `[wait N]` and `[N x wait 1]`: the
entry_tick enqueue law (the `_run_beat` docstring) plus the per-event
ambient hook minting (iter-53/KI#15) make door outcomes legitimately
slicing-dependent, so the absence of full equivalence is NOT an A2
violation. One measured honesty note rides the free surface: a crossing
event whose PAYLOAD reads the knowledge fold (a rotation briefing's
`count`) can reflect door divergence at seed 1001 — family counts stay
invariant, payloads do not (measured iter-260, the A2 card's own
boundary).

The pinned divergences (the seed-125 coerce flip, the seed-1001
document-check cascade) are the B3 no-runtime-change guard the owner's
§15 names: if a future change makes them disappear, a silent scheduler
semantics change happened — this file goes red, never green-by-accident.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.fold import fold, initial_projection
from core.log import EventRecord, read_log
from core.loop import RunResult, Simulator, load_playscript
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
TAVERN = load_pack(REPO / "content" / "tavern_pack")
PROVINCE = load_pack(REPO / "content" / "province_pack")
DAY1 = load_playscript(REPO / "tests" / "playscripts" / "day1_full.json")
CALENDAR = load_playscript(REPO / "tests" / "playscripts" / "province_calendar.json")

#: A2's declared crossing scope (the `R_crossing` relation, tavern):
#: the crossing-committed event families — committed inline at the
#: crossing tick by the beat / rotation machinery, never through the
#: intent door. Everything else (the door families) is free.
CROSSING_FAMILIES: tuple[str, ...] = (
    "status_decayed",
    "watch_change",
    "knowledge_transfer",
    "expectation_violation",
)
#: The measured surface at HEAD (iter-260, D-236): per seed, per family,
#: the day1_full event count — IDENTICAL in both arms (the 8/8 invariant
#: the temp-1 card measured, now the contract). Re-pin only together
#: with a legitimate tavern-pack or engine change that explains it.
EXPECTED_CROSSING_COUNTS: dict[int, dict[str, int]] = {
    125: {"status_decayed": 11, "watch_change": 2, "knowledge_transfer": 2,
          "expectation_violation": 1},
    42: {"status_decayed": 11, "watch_change": 2, "knowledge_transfer": 2,
         "expectation_violation": 1},
    7: {"status_decayed": 11, "watch_change": 2, "knowledge_transfer": 2,
        "expectation_violation": 1},
    1001: {"status_decayed": 11, "watch_change": 2, "knowledge_transfer": 2,
           "expectation_violation": 0},
}
#: The A/B seeds (the card's own four).
SEEDS: tuple[int, ...] = (125, 42, 7, 1001)
#: The measured day1_full fingerprints (the substantive draw count): the
#: ONLY fingerprint divergence in the 8 pairs is seed 1001's cascade
#: (16 span vs 17 sliced — the document-check arm draws one more check).
EXPECTED_FINGERPRINTS: dict[int, tuple[int, int]] = {
    125: (13, 13), 42: (6, 6), 7: (6, 6), 1001: (16, 17),
}


def _run(
    pack: Any, seed: int, steps: list[dict[str, Any]], name: str, path: Path
) -> tuple[list[EventRecord], RunResult]:
    """One deterministic run; returns (events, result)."""
    script = {"name": name, "seed": seed, "pack": pack.name_version, "steps": steps}
    sim = Simulator(pack, seed, path, SCHEMA, commit="0000000")
    result = sim.run_playscript(script)
    sim.close()
    _header, events = read_log(path, SCHEMA)
    return events, result


def _sliced(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The slicing transform: every `wait N` step becomes N `wait 1`
    steps — the card's minimal-pair form, player steps untouched."""
    out: list[dict[str, Any]] = []
    for step in steps:
        if step.get("intent") == "wait":
            out.extend({"intent": "wait", "ticks": 1} for _ in range(step["ticks"]))
        else:
            out.append(step)
    return out


def _counts(events: list[EventRecord]) -> dict[str, int]:
    """Per-type event counts (the family view)."""
    out: dict[str, int] = {}
    for event in events:
        out[event.type] = out.get(event.type, 0) + 1
    return out


def _is_autonomous(event: EventRecord) -> bool:
    """Whether the event resolves an AUTONOMOUS intent (urgency / faction
    / director) — the B3 field's exact scope."""
    return str(event.provenance.get("cause_intent", "")).startswith(
        ("urgency_", "faction_", "director_")
    )


#: The A/B run view: events (canonical records) + the run result.
ArmView = tuple[list[EventRecord], RunResult]


@pytest.fixture(scope="module")
def day1_arms(tmp_path_factory: pytest.TempPathFactory) -> dict[tuple[int, str], ArmView]:
    """The day1_full A/B pairs, all four seeds: (seed, arm) ->
    (events, result); arm in {"span", "sliced"} — [wait 720] vs
    [720 x wait 1] inside the full walkthrough script."""
    arms: dict[tuple[int, str], ArmView] = {}
    for seed in SEEDS:
        span, r_span = _run(
            TAVERN, seed, list(DAY1["steps"]), f"temp1_d1_{seed}_span",
            tmp_path_factory.mktemp(f"d1_{seed}") / "span.jsonl",
        )
        sliced, r_sliced = _run(
            TAVERN, seed, _sliced(DAY1["steps"]), f"temp1_d1_{seed}_sliced",
            tmp_path_factory.mktemp(f"d1s_{seed}") / "sliced.jsonl",
        )
        arms[(seed, "span")] = (span, r_span)
        arms[(seed, "sliced")] = (sliced, r_sliced)
    return arms


@pytest.fixture(scope="module")
def minimal_arms(tmp_path_factory: pytest.TempPathFactory) -> dict[tuple[int, str], ArmView]:
    """The minimal pair, all four seeds: [wait 720] vs [720 x wait 1]
    alone (the card's minimal-pair A/B — the projection-level contract
    surface with no door traffic of its own)."""
    arms: dict[tuple[int, str], ArmView] = {}
    for seed in SEEDS:
        span, r_span = _run(
            TAVERN, seed, [{"intent": "wait", "ticks": 720}],
            f"temp1_min_{seed}_span",
            tmp_path_factory.mktemp(f"min_{seed}") / "span.jsonl",
        )
        sliced, r_sliced = _run(
            TAVERN, seed, [{"intent": "wait", "ticks": 1} for _ in range(720)],
            f"temp1_min_{seed}_sliced",
            tmp_path_factory.mktemp(f"mins_{seed}") / "sliced.jsonl",
        )
        arms[(seed, "span")] = (span, r_span)
        arms[(seed, "sliced")] = (sliced, r_sliced)
    return arms


@pytest.fixture(scope="module")
def calendar_run(tmp_path_factory: pytest.TempPathFactory) -> ArmView:
    """The province_calendar witness (province pack, seed 42, one
    519000-tick wait): the B2 clustering + B3 two-times corpus."""
    return _run(
        PROVINCE, 42, list(CALENDAR["steps"]), "temp1_cal",
        tmp_path_factory.mktemp("cal") / "cal.jsonl",
    )


# -- A2: the crossing-family slicing contract --------------------------------


@pytest.mark.parametrize("seed", SEEDS)
def test_a2_crossing_families_are_slicing_invariant(
    day1_arms: dict[tuple[int, str], ArmView],
    seed: int,
) -> None:
    """THE A2 contract line: for the declared crossing families,
    `crossing semantics([wait 720]) == crossing semantics([720 x
    wait 1])` — the measured per-family counts are IDENTICAL across the
    arms, at every declared seed, and equal the recorded surface. The
    door families are NOT asserted (the next tests pin their freedom)."""
    span, _ = day1_arms[(seed, "span")]
    sliced, _ = day1_arms[(seed, "sliced")]
    span_counts = _counts(span)
    sliced_counts = _counts(sliced)
    expected = EXPECTED_CROSSING_COUNTS[seed]
    for family in CROSSING_FAMILIES:
        assert span_counts.get(family, 0) == expected[family], (
            f"seed {seed}: the span arm's {family} count "
            f"{span_counts.get(family, 0)} != the recorded surface "
            f"{expected[family]} — the crossing family moved, the A2 "
            f"contract's measured surface changed (re-pin only with the "
            f"explaining change, D-236)"
        )
        assert sliced_counts.get(family, 0) == expected[family], (
            f"seed {seed}: the sliced arm's {family} count "
            f"{sliced_counts.get(family, 0)} != the span arm's "
            f"{span_counts.get(family, 0)} — AN A2 VIOLATION: the "
            f"crossing-committed family diverged under wait slicing"
        )


@pytest.mark.parametrize("seed", SEEDS)
def test_a2_minimal_pair_projection_and_fingerprint_invariant(
    minimal_arms: dict[tuple[int, str], ArmView],
    seed: int,
) -> None:
    """The minimal pair's contract (the card's measured form): identical
    final projection, identical RNG fingerprint, and the ONLY per-type
    delta is the wait events' own count (1 vs 720) — the slicing
    transform's own bookkeeping, never a semantic family."""
    span, r_span = minimal_arms[(seed, "span")]
    sliced, r_sliced = minimal_arms[(seed, "sliced")]
    span_proj = fold(span, initial_projection(TAVERN.entities))
    sliced_proj = fold(sliced, initial_projection(TAVERN.entities))
    assert span_proj == sliced_proj, (
        f"seed {seed}: the minimal pair's final projections diverged — "
        f"the projection-level slicing contract broke"
    )
    assert r_span.fingerprint == r_sliced.fingerprint, (
        f"seed {seed}: the minimal pair's fingerprints diverged "
        f"({r_span.fingerprint} != {r_sliced.fingerprint}) — latent RNG "
        f"drift between the arms (RNG-1)"
    )
    delta = {
        type_: (count_a, count_b)
        for type_ in set(_counts(span)) | set(_counts(sliced))
        if (count_a := _counts(span).get(type_, 0))
        != (count_b := _counts(sliced).get(type_, 0))
    }
    assert delta == {"wait": (1, 720)}, (
        f"seed {seed}: the minimal pair's type delta is {delta}, not the "
        f"wait bookkeeping alone — a semantic family moved"
    )


@pytest.mark.parametrize("seed", SEEDS)
def test_a2_day1_door_deltas_stay_within_the_declared_free_surface(
    day1_arms: dict[tuple[int, str], ArmView],
    seed: int,
) -> None:
    """The honest boundary of A2: the door families are FREE to diverge
    (the entry_tick law + the ambient minting), and the day1_full deltas
    stay inside that freedom — the non-wait deltas touch only
    door-resolved events, never a crossing family (the family counts are
    the previous test's; here the delta SURFACE itself is bounded)."""
    span, _ = day1_arms[(seed, "span")]
    sliced, _ = day1_arms[(seed, "sliced")]
    span_counts = _counts(span)
    sliced_counts = _counts(sliced)
    delta_types = {
        type_
        for type_ in set(span_counts) | set(sliced_counts)
        if span_counts.get(type_, 0) != sliced_counts.get(type_, 0)
    }
    crossing_delta = delta_types & set(CROSSING_FAMILIES)
    assert not crossing_delta, (
        f"seed {seed}: the crossing families {crossing_delta} appear in "
        f"the day1_full type delta — AN A2 VIOLATION (the door families "
        f"are free, the crossing families are not)"
    )


def test_a2_door_freedom_seed125_the_coerce_flip(
    day1_arms: dict[tuple[int, str], ArmView],
) -> None:
    """The known divergence, PINNED (the owner's §15 guard): seed 125 —
    the beat-720 urgency coerce intent has the SAME semantic origin in
    both arms (`assignment_tick` 720) but divergent realization: the
    span arm's door lands at t=732 after the leverage card expired
    t=729 → `intent_rejected`; the sliced arm's door lands at t=720
    with the card live → `coerce` at t=723. A door divergence that
    DISAPPEARS would mean a silent runtime-semantics change — this pin
    is the loud detector."""
    span, _ = day1_arms[(125, "span")]
    sliced, _ = day1_arms[(125, "sliced")]
    span_rejects = [
        e for e in span
        if e.type == "intent_rejected" and _is_autonomous(e)
    ]
    span_coerces = [e for e in span if e.type == "coerce"]
    sliced_coerces = [e for e in sliced if e.type == "coerce"]
    assert len(span_rejects) == 1, (
        "seed 125 span: expected exactly one autonomous rejection "
        "(the beat-720 coerce attempt at the door t=732)"
    )
    rejected = span_rejects[0]
    assert rejected.provenance["cause_intent"].startswith("urgency_")
    assert rejected.provenance["assignment_tick"] == 720
    assert rejected.t == 732
    assert not span_coerces, "seed 125 span: the coerce must NOT fire (the card expired)"
    assert len(sliced_coerces) == 1, (
        "seed 125 sliced: expected the coerce to fire (the door lands with the card live)"
    )
    coerced = sliced_coerces[0]
    assert coerced.provenance["cause_intent"].startswith("urgency_")
    assert coerced.provenance["assignment_tick"] == 720, (
        "the SAME semantic origin as the span arm's rejected attempt — "
        "the fork made checkable in provenance"
    )
    assert coerced.t == 723


def test_a2_door_freedom_seed1001_the_cascade(
    day1_arms: dict[tuple[int, str], ArmView],
) -> None:
    """The second known divergence, PINNED: seed 1001 — the
    document-check flip (the span arm's `document_check_failed` vs the
    sliced arm's accepted `document_check` with the arrest chain), and
    the ONLY fingerprint divergence in the 8 pairs (16 vs 17 — the
    accepted check draws one more opposed check)."""
    span, r_span = day1_arms[(1001, "span")]
    sliced, r_sliced = day1_arms[(1001, "sliced")]
    assert any(e.type == "document_check_failed" for e in span)
    assert not any(e.type == "document_check" for e in span)
    assert any(e.type == "document_check" for e in sliced)
    assert any(e.type == "arrest_attempt" for e in sliced), (
        "the sliced arm's accepted check cascades into the arrest chain"
    )
    assert r_span.fingerprint == 16 and r_sliced.fingerprint == 17, (
        f"the measured cascade fingerprints moved "
        f"({r_span.fingerprint}/{r_sliced.fingerprint} != 16/17) — "
        f"re-pin with the explaining change"
    )


@pytest.mark.parametrize("seed", (42, 7))
def test_a2_door_families_agree_on_seeds_42_and_7(
    day1_arms: dict[tuple[int, str], ArmView],
    seed: int,
) -> None:
    """The honest bound of the measured divergence: at seeds 42 and 7
    the door families HAPPEN to agree — the only type delta is the wait
    bookkeeping (player waits plus, at seed 7, the door-resolved urgency
    idles present in BOTH arms). The divergence is seed-dependent, never
    a universal mechanism (the card's own caution)."""
    span, _ = day1_arms[(seed, "span")]
    sliced, _ = day1_arms[(seed, "sliced")]
    span_counts = _counts(span)
    sliced_counts = _counts(sliced)
    delta = {
        type_: (span_counts.get(type_, 0), sliced_counts.get(type_, 0))
        for type_ in set(span_counts) | set(sliced_counts)
        if span_counts.get(type_, 0) != sliced_counts.get(type_, 0)
    }
    assert set(delta) == {"wait"}, (
        f"seed {seed}: the door families no longer agree ({delta}) — "
        f"either a new divergence arrived (re-measure, the card's "
        f"one-seed caution) or runtime semantics changed"
    )


# -- B2 unchanged + B3 provenance: the two-times contract ---------------------


def test_b3_autonomous_events_carry_their_assignment_tick(
    calendar_run: ArmView,
) -> None:
    """B3's field discipline over the clustering corpus: EVERY
    autonomous-resolved event (accepted or rejected) carries
    `assignment_tick` with `assignment_tick <= event.t` (the origin
    never postdates the realization); every non-autonomous event (player
    steps, world crossings) NEVER carries it — a playscript step's
    assignment IS its enqueue tick, no key needed."""
    events, _ = calendar_run
    autonomous = [e for e in events if _is_autonomous(e)]
    assert autonomous, "the corpus must exercise autonomous intents (the empty-ablation law)"
    for event in autonomous:
        assert "assignment_tick" in event.provenance, (
            f"{event.id} ({event.type}, {event.provenance.get('cause_intent')}) "
            f"resolves an autonomous intent but carries no assignment_tick"
        )
        assert event.provenance["assignment_tick"] <= event.t, (
            f"{event.id}: assignment_tick {event.provenance['assignment_tick']} "
            f"postdates the realization tick {event.t}"
        )
    for event in events:
        if not _is_autonomous(event):
            assert "assignment_tick" not in event.provenance, (
                f"{event.id} ({event.type}) is not autonomous but carries "
                f"assignment_tick — the field's scope is the autonomous door"
            )


def test_b2_b3_the_two_times_separate_under_a_long_wait(
    calendar_run: ArmView,
) -> None:
    """The B2 witness UNCHANGED (the clustering is still total) with the
    B3 separation now observable: all 265 talks realize in the last five
    ticks [520069, 520073] — the world resumes only at the wait's
    landing — while their semantic origins span the whole year
    [1800, 516600], a deferral latency of up to ~518k ticks. `event.t`
    stays the canonical realization time (the card's law: B3 records,
    never re-times)."""
    events, result = calendar_run
    assert result.event_count == 2288, (
        f"the corpus shape moved ({result.event_count} != 2288 events) — "
        f"the §16 witness numbers changed, re-pin with the explaining change"
    )
    talks = [e for e in events if e.type == "talk"]
    assert len(talks) == 265
    talk_ticks = [e.t for e in talks]
    assert min(talk_ticks) == 520069 and max(talk_ticks) == 520073, (
        "the B2 clustering moved — the talks no longer pile into the "
        "last five ticks (a runtime-semantics change, not a provenance one)"
    )
    origins = [e.provenance["assignment_tick"] for e in talks]
    assert min(origins) == 1800 and max(origins) == 516600, (
        "the assignment range moved — re-pin with the explaining change"
    )
    max_latency = max(e.t - e.provenance["assignment_tick"] for e in talks)
    assert max_latency == 518269, (
        f"the max deferral latency moved ({max_latency} != 518269)"
    )


def test_b3_rejections_carry_both_times(
    day1_arms: dict[tuple[int, str], ArmView],
) -> None:
    """A rejected autonomous attempt is still a minted-and-doomed fact:
    the seed-125 span rejection carries BOTH times (origin 720,
    realization 732) — the OCC window that killed it lived between
    them, which is exactly the causal chain the two-times record makes
    inspectable."""
    span, _ = day1_arms[(125, "span")]
    rejected = next(
        e for e in span
        if e.type == "intent_rejected" and _is_autonomous(e)
    )
    assert rejected.provenance["assignment_tick"] == 720
    assert rejected.t == 732
    assert rejected.t - rejected.provenance["assignment_tick"] == 12, (
        "the card-expiry window (the leverage card lived to 729, the "
        "door landed at 732) — the 12-tick gap is the observable OCC miss"
    )


def test_b3_player_intents_never_carry_the_field(
    minimal_arms: dict[tuple[int, str], ArmView],
) -> None:
    """The player-side scope pin: across every minimal-pair arm (1442
    wait events per sliced run), no event resolving a PLAYER intent
    (the `intent_*` ids) ever carries `assignment_tick` — the field is
    the autonomous door's own, and a playscript step's assignment IS
    its enqueue tick. (The arms DO carry autonomous events — a director
    ramble fires mid-wait — which the discipline below leaves to the
    autonomous scope.)"""
    for (_seed, _arm), (events, _result) in minimal_arms.items():
        for event in events:
            cause_intent = str(event.provenance.get("cause_intent", ""))
            if cause_intent.startswith("intent_"):
                assert "assignment_tick" not in event.provenance, (
                    f"{event.id} resolves the player intent "
                    f"{cause_intent} but carries assignment_tick"
                )
