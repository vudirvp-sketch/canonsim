"""iter-4 acceptance — the director (phase0 §4, D-005, DIRECTOR_SPEC):
the consequence planner that never improvises. Hooks seeded at event
time sit in a per-run buffer; explicit triggers (time / place /
threshold) fire causally; the stagnation detector releases the
lowest-threshold hook when narrative entropy drops below the pack's
floor. Releases ride the intent door — the director never writes canon
itself (D-037). Director-off keeps the buffer seeding but suppresses
releases (T8 A/B baseline).

iter-36 acceptance (phase 3, DIR-1, the L4D peak/rest donor): the
pacing clock — a per-run RAMP / PEAK / REST / STAGNATION machine over
narrative entropy, advanced once per beat. REST is the post-climax
breathing room the flat v0.1 detector lacked (it re-injected the beat
after a climax); explicit triggers never consult the clock (D-005 —
causality is not pacing); a pack without `director.pacing` runs the
v0.1 minimal pair unchanged.

iter-38 acceptance (phase 3, DIR-3, the L4D2 three-intensity rule +
the boss-beat rule): the climax layer — `director.pacing.climax_floor`,
the third threshold strictly above the peak floor; the `PEAK_CLIMAX`
state (one beat — the boss beat, entered only by a climax release,
exited to REST); the climax release path (a climax-flagged hook at the
END of a peak, entropy at the third layer, never from the quiet path).
No tavern hook carries the flag yet — the pack declares the layer as
dormant vocabulary; the tests exercise the path via manual hooks and
mutated packs (the iter-36 pattern).

Determinism holds (T1 discipline): the entropy formula reads
observable state only (L6), and the release decisions are deterministic
for a given buffer + projection — no RNG in the director itself. The
clock is derived state the same way: a fold of the per-beat entropy
sequence, never a canon write.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.director import (
    DISABLED,
    Director,
    DisabledPolicy,
    EnabledPolicy,
    PacingClock,
    PacingConfig,
    SeededHook,
    entropy,
    pacing_from_rules,
)
from core.fold import initial_projection
from core.log import EventRecord
from core.pack import PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")


def _record(hooks: tuple[str, ...] = (), event_id: str = "ev_0001", t: int = 0) -> EventRecord:
    """A minimal committed event with the given hooks."""
    return EventRecord(
        id=event_id, t=t, type="test_event", actor="pc_01", cause=None,
        outcome={}, knowledge=(), state_changes=(), hooks=hooks,
        importance="low", provenance={}, target=None,
    )


def _seeded_hook(
    *, tag: str = "guard_suspicious_of_pc", target_npc: str = "npc_guard_01",
    weight: int = 2, release_threshold: int = 5, trigger: dict[str, Any] | None = None,
    climax: bool = False,
) -> SeededHook:
    return SeededHook(
        tag=tag, seeded_by_event="ev_0001", seeded_at_tick=0,
        weight=weight, release_threshold=release_threshold,
        target_npc=target_npc, intent_kind="wait", intent_target=None,
        intent_fields={"ticks": 1}, trigger=trigger, climax=climax,
    )


# -- seeding (D-005: hooks seeded at event time, never invented later) --------


def test_seed_absorbs_hooks_the_pack_declares() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=("guard_suspicious_of_pc", "unknown_tag")))
    # the pack-declared hook seeds; the unknown tag is silently ignored
    assert len(director.hooks) == 1
    assert director.hooks[0].tag == "guard_suspicious_of_pc"
    assert director.hooks[0].target_npc == "npc_guard_01"
    assert director.hooks[0].intent_kind == "wait"
    # no tavern hook carries the climax flag (DIR-3: declared-but-dormant
    # layer vocabulary — the flag is a content decision, TASKS records it)
    assert director.hooks[0].climax is False


def test_seed_ignores_events_without_hooks() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=()))
    assert director.hooks == ()


# -- entropy (P2e: observable state only, never knowledge records) ------------


def test_entropy_zero_on_idle_world() -> None:
    projection = initial_projection(PACK.entities)
    assert entropy(projection, iter([]), PACK.rules) == 0  # no threats


def test_entropy_sums_hook_weights() -> None:
    projection = initial_projection(PACK.entities)
    hooks = [_seeded_hook(weight=2), _seeded_hook(weight=3)]
    # only the unreleased contribute
    assert entropy(projection, iter(hooks), PACK.rules) == 5


def test_entropy_reads_global_suspicion() -> None:
    projection = initial_projection(PACK.entities)
    projection["npc_guard_01"]["relations.suspicion"] = 25
    projection["npc_guard_02"]["relations.suspicion"] = 10
    assert entropy(projection, iter([]), PACK.rules) == 35


def test_entropy_counts_visible_physical_threats() -> None:
    projection = initial_projection(PACK.entities)
    projection["loc_tavern"]["fire.bar"] = "burning"
    projection["loc_tavern"]["fire.tables"] = "burning"
    assert entropy(projection, iter([]), PACK.rules) == 2


def test_entropy_threat_states_are_pack_data() -> None:
    """D-057: the threat sensor reads the layers' declared spot_state —
    a pack whose layer spreads under a different vocabulary stays
    visible to the director (zero hardcoded state values)."""
    projection = initial_projection(PACK.entities)
    projection["loc_tavern"]["fire.bar"] = "burning"
    rules = json.loads(json.dumps(dict(PACK.data)))
    rules["rules.json"]["transitions"]["fire"]["spot_state"] = "smoldering"
    # the old vocabulary no longer reads as a threat...
    assert entropy(projection, iter([]), rules["rules.json"]) == 0
    # ...the declared one does
    projection["loc_tavern"]["fire.tables"] = "smoldering"
    assert entropy(projection, iter([]), rules["rules.json"]) == 1


def test_entropy_never_reads_knowledge_records() -> None:
    """L6: entropy is observable state only. A knower's records must
    never feed the director's release decision — the Influence Boundary
    extends from the perceiver (EPIST-1) to the director itself."""
    projection = initial_projection(PACK.entities)
    # stuff a knowledge record into the projection — the director MUST
    # not see it (it lives in the KnowledgeView, not the projection)
    projection["npc_guard_01"]["knowledge.figure_reaching_for_purse"] = True
    assert entropy(projection, iter([]), PACK.rules) == 0


# -- explicit triggers (causal, fire regardless of entropy) -------------------


def test_threshold_trigger_fires_when_suspicion_crosses() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director.seed(_record(hooks=("possible_document_check",)))
    projection = initial_projection(PACK.entities)
    # suspicion below the threshold (50): trigger does not fire
    assert director.releases(projection, beat_tick=0) == []
    # suspicion crosses 50: trigger fires — entropy_floor=0 means
    # stagnation never releases (entropy can't be negative), only the
    # explicit threshold trigger can release here
    projection["npc_guard_01"]["relations.suspicion"] = 50
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert released[0].kind == "wait"
    assert released[0].actor == "npc_guard_01"


def test_time_trigger_fires_after_the_packed_tick() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    # craft a hook with a time trigger at tick 100
    hook = _seeded_hook(
        tag="guard_suspicious_of_pc", release_threshold=0,
        trigger={"kind": "time", "tick": 100},
    )
    director._hooks.append(hook)  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    assert director.releases(projection, beat_tick=50) == []
    released = director.releases(projection, beat_tick=100)
    assert len(released) == 1


def test_place_trigger_fires_when_target_at_location() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    hook = _seeded_hook(
        target_npc="npc_guard_01",
        trigger={"kind": "place", "target_npc": "npc_guard_01", "location": "loc_tavern"},
    )
    director._hooks.append(hook)  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # guard at the tavern: trigger fires
    assert projection["npc_guard_01"]["position"] == "loc_tavern"
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    # move the guard away: trigger stops
    projection["npc_guard_01"]["position"] = "loc_guardroom"
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director2._hooks.append(hook)
    assert director2.releases(projection, beat_tick=0) == []


# -- stagnation release (entropy < floor → lowest-threshold hook wins) --------


def test_stagnation_releases_when_entropy_below_floor() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    # two unreleased hooks; no triggers; no suspicion; no fires.
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        tag="guard_suspicious_of_pc", release_threshold=10, weight=2,
    ))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        tag="possible_document_check", release_threshold=5, weight=3,
    ))
    projection = initial_projection(PACK.entities)
    # entropy = 2 + 3 = 5 < floor 10 → release the lowest-threshold hook
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    # the lowest release_threshold wins (5 < 10)
    assert director.hooks[1].tag == "possible_document_check"


def test_stagnation_silent_when_entropy_above_floor() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    director._hooks.append(_seeded_hook(weight=20, release_threshold=5))  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # entropy = 20 ≥ floor 10 → no stagnation release
    assert director.releases(projection, beat_tick=0) == []


def test_stagnation_skips_released_hooks() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    h1 = _seeded_hook(
        tag="guard_suspicious_of_pc", target_npc="npc_guard_01",
        weight=2, release_threshold=5,
    )
    h2 = _seeded_hook(
        tag="possible_document_check", target_npc="npc_barkeep_01",
        weight=3, release_threshold=10,
    )
    director._hooks.extend([h1, h2])  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # first release: lowest-threshold wins (h1, threshold=5)
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    # mark h1 as released (simulate the actual release path)
    director._released.add(0)  # type: ignore[attr-defined]
    # entropy now = 3 (h2 only) < floor 10 → release h2 (different NPC —
    # no cooldown blocks the barkeep)
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1


# -- director-off (T8 A/B baseline: buffer seeds, nothing releases) -----------


def test_director_off_seeds_but_never_releases() -> None:
    director = Director(pack=PACK, policy=DISABLED)
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    assert len(director.hooks) == 1  # the buffer seeds
    projection = initial_projection(PACK.entities)
    # no triggers fire either — the disabled policy suppresses all releases
    released = director.releases(projection, beat_tick=0)
    assert released == []


def test_disabled_policy_always_returns_false() -> None:
    policy = DisabledPolicy()
    assert policy.permit_release(explicit_trigger_fires=True, current_entropy=0) is False
    assert policy.permit_release(explicit_trigger_fires=False, current_entropy=999) is False


# -- per-NPC cooldown (MinGapBetweenEncounters analogue) ---------------------


def test_per_npc_cooldown_blocks_back_to_back_releases() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    # two hooks targeting the same NPC; no triggers
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        tag="guard_suspicious_of_pc", target_npc="npc_guard_01",
        weight=2, release_threshold=5,
    ))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        tag="guard_wary_vigil", target_npc="npc_guard_01",
        weight=2, release_threshold=6,
    ))
    projection = initial_projection(PACK.entities)
    # beat 1: release h1 (lowest threshold)
    director.next_beat()
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    # beat 2: same NPC is on cooldown (per_npc_cooldown_beats=2) → no release
    director.next_beat()
    assert director.releases(projection, beat_tick=0) == []
    # beat 3: cooldown expired → release h2
    director.next_beat()
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1


# -- dead actors (caught NPCs never targeted) ---------------------------------


def test_caught_target_is_never_targeted() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=999))
    hook = _seeded_hook(
        target_npc="npc_guard_01", release_threshold=0,
        trigger={"kind": "threshold", "target_npc": "npc_guard_01",
                 "axis": "suspicion", "value": 0, "comparator": "at_least"},
    )
    director._hooks.append(hook)  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # the trigger condition (suspicion >= 0) is always met — fires normally
    assert len(director.releases(projection, beat_tick=0)) == 1
    # mark the target as caught: the trigger still matches, but the actor
    # is dead to the director — no release
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=999))
    director2._hooks.append(hook)
    projection["npc_guard_01"]["crime_status"] = "caught"
    assert director2.releases(projection, beat_tick=0) == []


# -- the pacing clock (iter-36, DIR-1; the L4D peak/rest donor) ----------------


def _mutated_pack(tmp_path: Path, mutate_rules: Any) -> Any:
    """A copy of the tavern pack with `rules.json` mutated and re-linted
    (the test_core `_broken_pack` pattern, local to this suite)."""
    target = tmp_path / "mutated_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    mutate_rules(rules)
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return load_pack(target)


# pack wiring


def test_pack_declares_pacing_and_clock_starts_ramp() -> None:
    """The tavern pack declares `director.pacing` (the phase-3 arc's first
    config) — with the climax layer (DIR-3: 75 = 3x peak_floor 25, the
    L4D2 three-intensity ratio); the per-run clock starts in RAMP with
    zero beats held."""
    config = pacing_from_rules(PACK.rules)
    assert config is not None
    assert config == PacingConfig(
        entropy_floor=5, peak_floor=25, min_peak_beats=1, min_rest_beats=1,
        climax_floor=75,
    )
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    assert director.pacing == PacingClock(state="RAMP", beats_in_state=0)


def test_pack_without_pacing_runs_the_v01_minimal_pair(tmp_path: Path) -> None:
    """A pack that drops `director.pacing` gets no clock — the release
    behavior is the v0.1 minimal pair (the pack's own declaration is the
    gate, INV-3; a second pack requires zero engine changes)."""
    pack = _mutated_pack(tmp_path, lambda rules: rules["director"].pop("pacing"))
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=10))
    assert director.pacing is None
    director._hooks.append(_seeded_hook(weight=2, release_threshold=5))  # type: ignore[attr-defined]
    projection = initial_projection(pack.entities)
    # v0.1: entropy 2 < floor 10 → release, no clock gate
    assert len(director.releases(projection, beat_tick=0)) == 1


# the state machine (pure PacingClock.transition)


def test_clock_ramp_to_peak_on_entropy_spike() -> None:
    config = PacingConfig(entropy_floor=5, peak_floor=25, min_peak_beats=1, min_rest_beats=1)
    clock = PacingClock().transition(30, config)
    assert clock == PacingClock(state="PEAK", beats_in_state=1)
    # the quiet band names STAGNATION below the floor, RAMP above it
    assert PacingClock().transition(2, config).state == "STAGNATION"
    assert PacingClock().transition(10, config).state == "RAMP"


def test_clock_peak_holds_minimum_through_an_entropy_dip() -> None:
    """L4D hysteresis: a spike is a peak — a one-beat dip below the peak
    floor does not flap the clock out of PEAK before min_peak_beats."""
    config = PacingConfig(entropy_floor=5, peak_floor=25, min_peak_beats=2, min_rest_beats=1)
    clock = PacingClock().transition(30, config)  # PEAK(1)
    clock = clock.transition(10, config)  # dip, but held only 1 < 2 → stay PEAK
    assert clock == PacingClock(state="PEAK", beats_in_state=2)
    clock = clock.transition(10, config)  # held 2 ≥ 2 → the peak is over
    assert clock.state == "REST"


def test_clock_peak_to_rest_then_quiet_band() -> None:
    """The peak is followed by a rest; the rest holds min_rest_beats, then
    settles by the entropy band (the world re-spiking breaks it early)."""
    config = PacingConfig(entropy_floor=5, peak_floor=25, min_peak_beats=1, min_rest_beats=2)
    clock = PacingClock("PEAK", 3).transition(10, config)  # the peak is over
    assert clock == PacingClock(state="REST", beats_in_state=1)
    clock = clock.transition(10, config)  # rest held only 1 < 2 → breathe on
    assert clock == PacingClock(state="REST", beats_in_state=2)
    clock = clock.transition(2, config)  # held 2 ≥ 2 → below the floor
    assert clock == PacingClock(state="STAGNATION", beats_in_state=1)
    # the world re-spiking breaks the rest early
    resting = PacingClock("REST", 1)
    assert resting.transition(30, config).state == "PEAK"


# the release gate (Director-level, the real PACK's pacing)


def test_rest_suppresses_stagnation_release() -> None:
    """DIR-1's behavioral delta: after a peak, the flat v0.1 detector
    would re-inject the beat the entropy drops below the floor; the
    clock holds REST — the world breathes."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    # weight 30 ≥ peak_floor 25 → the beat-1 entropy spike is a PEAK
    director._hooks.append(_seeded_hook(weight=30, release_threshold=5))  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert director.releases(projection, beat_tick=0) == []  # PEAK: nothing adds
    assert director.pacing is not None and director.pacing.state == "PEAK"
    # the tension drains: the peak ends → REST, and the quiet-world hook
    # the flat detector WOULD release now stays in the buffer
    director._hooks.clear()
    director._hooks.append(_seeded_hook(weight=2, release_threshold=5))  # type: ignore[attr-defined]
    director.next_beat()
    assert director.releases(projection, beat_tick=0) == []  # REST suppresses
    assert director.pacing.state == "REST"


def test_release_resumes_after_the_rest_completes() -> None:
    """The rest is bounded (min_rest_beats): once it completes, the quiet
    band releases again — the exit-criterion family (an eventless
    stretch stays short)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(weight=30, release_threshold=5))  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    director.next_beat()
    director.releases(projection, beat_tick=0)  # PEAK
    director._hooks.clear()
    director._hooks.append(_seeded_hook(weight=2, release_threshold=5))  # type: ignore[attr-defined]
    director.next_beat()
    director.releases(projection, beat_tick=0)  # REST (min_rest_beats = 1)
    director.next_beat()
    # rest held 1 ≥ 1 → STAGNATION (entropy 2 < floor 5) → the detector fires
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert director.pacing is not None and director.pacing.state == "STAGNATION"


def test_explicit_time_trigger_fires_during_rest() -> None:
    """D-005: causality is not pacing — the clock never gates explicit
    triggers; the deferred consequence fires mid-rest."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(weight=30, release_threshold=5))  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    director.next_beat()
    director.releases(projection, beat_tick=0)  # PEAK
    director._hooks.clear()
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        weight=2, release_threshold=5,
        trigger={"kind": "time", "tick": 100},
    ))
    director.next_beat()
    # beat 2: PEAK → REST (entropy 2 < 25, min_peak met); the stagnation
    # path is gated, but the explicit time trigger fires in REST
    released = director.releases(projection, beat_tick=100)
    assert len(released) == 1
    assert director.pacing is not None and director.pacing.state == "REST"


def test_repeated_releases_calls_never_double_advance_the_clock() -> None:
    """The loop calls `releases()` once per beat; the unit-test pattern of
    probing repeatedly inside one beat must not double-advance the clock
    (the `_pacing_beat` guard)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(weight=30, release_threshold=5))  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    director.next_beat()
    director.releases(projection, beat_tick=0)  # RAMP → PEAK
    first = director.pacing
    director.releases(projection, beat_tick=0)  # same beat, same projection
    assert director.pacing == first


# pack lint (the pacing contract)


def test_pacing_lint_rejects_peak_at_or_below_the_stagnation_floor(
    tmp_path: Path,
) -> None:
    """peak_floor must sit strictly above the stagnation entropy floor —
    otherwise the PEAK band would swallow the quiet band the detector
    exists to watch."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["pacing"]["peak_floor"] = 5  # == entropy_floor

    with pytest.raises(PackError, match="strictly above"):
        _mutated_pack(tmp_path, mutate)


def test_pacing_lint_rejects_non_positive_min_durations(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["pacing"]["min_rest_beats"] = 0

    with pytest.raises(PackError, match="min_rest_beats"):
        _mutated_pack(tmp_path, mutate)


# -- the climax layer (iter-38, DIR-3; the L4D2 three-intensity rule) ---------


def test_climax_beat_is_one_beat_then_the_rest() -> None:
    """PEAK_CLIMAX is the boss beat itself — one beat, exited to REST
    unconditionally (boss beat + reset); a still-loud world breaks the
    rest per the existing re-spike law, on the transition after."""
    config = PacingConfig(
        entropy_floor=5, peak_floor=25, min_peak_beats=1, min_rest_beats=1,
        climax_floor=75,
    )
    boss = PacingClock("PEAK_CLIMAX", 1)
    # quiet, ramp-band, peak-band, climax-layer entropy: always the rest
    for entropy_value in (2, 10, 30, 80):
        assert boss.transition(entropy_value, config) == PacingClock("REST", 1)


def test_climax_release_fires_at_the_end_of_a_peak() -> None:
    """The climax path: a boss hook at the climax layer with the clock in
    PEAK having held its minimum — the release IS the boss beat (the
    clock marks PEAK_CLIMAX), and the next beat is the rest."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    # weight 80: entropy 80 >= climax_floor 75 and >= peak_floor 25 — the
    # beat-1 spike is a PEAK holding its minimum (1) — the peak's END
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(weight=80, release_threshold=5, climax=True)
    )
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert len(director.releases(projection, beat_tick=0)) == 1
    assert director.pacing == PacingClock(state="PEAK_CLIMAX", beats_in_state=1)
    # beat 2: the reset is the rest — the world breathes (entropy dropped
    # to 0 with the buffer drained; REST suppresses the quiet path)
    director.next_beat()
    assert director.releases(projection, beat_tick=0) == []
    assert director.pacing is not None and director.pacing.state == "REST"


def test_climax_requires_the_layered_threshold() -> None:
    """The L4D2 three-intensity rule: the boss needs the THIRD layer —
    the peak band alone (entropy >= peak_floor, < climax_floor) never
    releases a climax hook, however long the peak holds."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(weight=30, release_threshold=5, climax=True)
    )
    projection = initial_projection(PACK.entities)
    for _ in range(3):
        director.next_beat()
        assert director.releases(projection, beat_tick=0) == []
    # the clock held PEAK past its minimum — but 30 < 75 (the third layer)
    assert director.pacing is not None and director.pacing.state == "PEAK"


def test_climax_requires_the_peak_minimum(tmp_path: Path) -> None:
    """The boss beat is placed at the END of a peak — the peak must have
    held its anti-flap minimum first (a pack with min_peak_beats=2: the
    entry beat is the peak's start, not its end)."""
    pack = _mutated_pack(
        tmp_path,
        lambda rules: rules["director"]["pacing"].update(min_peak_beats=2),
    )
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(weight=80, release_threshold=5, climax=True)
    )
    projection = initial_projection(pack.entities)
    director.next_beat()
    assert director.releases(projection, beat_tick=0) == []  # PEAK held 1 < 2
    director.next_beat()
    assert len(director.releases(projection, beat_tick=0)) == 1  # held 2 >= 2
    assert director.pacing is not None and director.pacing.state == "PEAK_CLIMAX"


def test_climax_hooks_never_release_from_the_quiet_path() -> None:
    """A boss does not spawn because the world is boring: the climax flag
    excludes the hook from the stagnation path even in STAGNATION — the
    un-flagged twin (test_stagnation_releases_when_entropy_below_floor)
    releases under exactly these conditions."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(weight=2, release_threshold=5, climax=True)
    )
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert director.releases(projection, beat_tick=0) == []
    assert director.pacing is not None and director.pacing.state == "STAGNATION"


def test_explicit_trigger_beats_the_climax_path() -> None:
    """D-005: causality is not pacing — when a climax hook's explicit
    trigger fires at the same beat the climax gate passes, the explicit
    path releases first and the clock does NOT mark PEAK_CLIMAX (the
    day1_full shape: the document-check's threshold trigger at beat 1,
    entropy 220 with the climax layer met — the explicit release wins)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(
            weight=80, release_threshold=5, climax=True,
            trigger={"kind": "time", "tick": 0},
        )
    )
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert len(director.releases(projection, beat_tick=0)) == 1
    # released via the causal path: the clock advanced into PEAK and stays
    assert director.pacing is not None and director.pacing.state == "PEAK"


def test_post_climax_beat_is_inert_to_repeated_calls() -> None:
    """No double boss: after the climax release, a repeated releases()
    call inside the same beat returns nothing and the clock stays
    PEAK_CLIMAX (the advance guard + the state gate — PEAK_CLIMAX does
    not re-open the climax gate, state != PEAK)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(weight=80, release_threshold=5, climax=True)
    )
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert len(director.releases(projection, beat_tick=0)) == 1
    assert director.releases(projection, beat_tick=0) == []
    assert director.pacing == PacingClock(state="PEAK_CLIMAX", beats_in_state=1)


def test_director_off_blocks_the_climax_path() -> None:
    """T8 A/B: a disabled director never releases — the boss included
    (DisabledPolicy.permit_climax is False). The clock still runs: it is
    derived state, not a release path."""
    director = Director(pack=PACK, policy=DISABLED)
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(weight=80, release_threshold=5, climax=True)
    )
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert director.releases(projection, beat_tick=0) == []
    assert director.pacing is not None and director.pacing.state == "PEAK"


def test_climax_flag_without_the_layer_is_explicit_trigger_only(
    tmp_path: Path,
) -> None:
    """A pack that flags climax hooks but declares no climax_floor runs
    the two-layer clock: no climax path, the quiet path still excluded,
    the explicit trigger untouched (the nopacing harness variant is
    exactly this pack — the flag stays meaningful without the layer)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["pacing"].pop("climax_floor")
        hook = rules["director"]["hooks"]["guard_suspicious_of_pc"]
        hook["climax"] = True
        hook["trigger"] = {"kind": "time", "tick": 5}

    pack = _mutated_pack(tmp_path, mutate)
    config = pacing_from_rules(pack.rules)
    assert config is not None and config.climax_floor is None
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=10))
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    assert director.hooks[0].climax is True
    projection = initial_projection(pack.entities)
    director.next_beat()
    # entropy 2 < floor 10: the quiet path would fire — the flag excludes it
    assert director.releases(projection, beat_tick=0) == []
    director.next_beat()
    # beat_tick >= 5: the explicit time trigger fires (causal, ungated)
    assert len(director.releases(projection, beat_tick=100)) == 1


def test_two_layer_pack_keeps_the_iter36_release_behavior(
    tmp_path: Path,
) -> None:
    """The pack's own declaration is the gate (INV-3): dropping only the
    climax layer changes nothing about the two-layer paths — the quiet
    release behaves exactly as the iter-36 clock did."""
    pack = _mutated_pack(
        tmp_path, lambda rules: rules["director"]["pacing"].pop("climax_floor")
    )
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(weight=2, release_threshold=5)
    )
    projection = initial_projection(pack.entities)
    director.next_beat()
    # entropy 2 < floor 5, the clock reads STAGNATION → the detector fires
    assert len(director.releases(projection, beat_tick=0)) == 1


# pack lint (the climax-layer contract)


def test_climax_floor_lint_rejects_at_or_below_the_peak_floor(
    tmp_path: Path,
) -> None:
    """The layering law: climax_floor strictly above peak_floor — a
    climax layer inside the peak band would swallow the layering (the
    L4D2 Boss-threshold-gates-Peak-threshold shape)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["pacing"]["climax_floor"] = 25  # == peak_floor

    with pytest.raises(PackError, match="climax_floor"):
        _mutated_pack(tmp_path, mutate)


def test_climax_flag_lint_rejects_non_boolean(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["hooks"]["guard_suspicious_of_pc"]["climax"] = 1

    with pytest.raises(PackError, match="climax must be a boolean"):
        _mutated_pack(tmp_path, mutate)


# -- helpers -----------------------------------------------------------------
