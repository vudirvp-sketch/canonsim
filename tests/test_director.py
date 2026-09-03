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

iter-39 acceptance (phase 3, DIR-4, the L4D multi-channel family —
Horde / S.I. / Music → threat / social / ambient): the quiet path
decomposes per channel. `director.channels` declares the pacing
dimensions (floor + the closed input vocabulary); a hook opts in per
hook (`channel`); the channel senses its own unreleased hooks + the
inputs it binds. The pacing clock stays global (PEAK/REST suppress
every channel — one drama arc); explicit triggers stay ungated; the
budget stays 1 release per beat across all channels; the climax path
ignores channels. A pack without the block runs the v0.1 global-floor
quiet path byte-identically; a channelless hook keeps that global
floor even in a channels pack (the per-hook opt-in mirrors the climax
flag: a tag without the block is dormant vocabulary).

Determinism holds (T1 discipline): the entropy formula reads
observable state only (L6), and the release decisions are deterministic
for a given buffer + projection — no RNG in the director itself. The
clock is derived state the same way: a fold of the per-beat entropy
sequence, never a canon write.

iter-47 acceptance (phase 3, arc-1, P3c — arcs & tension shaping; the
DF event_collections / Paradox event-chain precedent): `director.arcs`
declares named release CHAINS. The ORDER law — a member tag is a
release candidate only while it is its arc's current member (the
chain gates ALL release paths, explicit triggers included: an arc is
pack-declared causality, not pacing). The GAP law — the current
member waits `min_gap_beats` after the previous member's release,
consulted by the quiet and climax paths only (D-005: the world's own
consequences fire mid-gap exactly as they fire mid-rest). The entropy
mirror — instances of PASSED members stop counting (one play per arc
beat, the first_time_only burn law's twin); future members count
normally (a fully-seeded chain reads its whole weight). No committed
hook rides an arc yet — the pack declares no chains (the content row
owns the live driver); the tests exercise the laws via mutated packs
(the iter-36/38/42 pattern).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.director import (
    ARC_KEYS,
    CHANNEL_INPUTS,
    DISABLED,
    ArcConfig,
    ChannelConfig,
    Director,
    DisabledPolicy,
    EnabledPolicy,
    OptionSpec,
    PacingClock,
    PacingConfig,
    SeededHook,
    arcs_from_rules,
    channel_entropies,
    channels_from_rules,
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
    climax: bool = False, channel: str | None = None,
    weight_modifiers: tuple[dict[str, Any], ...] = (),
    first_time_only: bool = False,
    options: tuple[OptionSpec, ...] = (),
) -> SeededHook:
    return SeededHook(
        tag=tag, seeded_by_event="ev_0001", seeded_at_tick=0,
        weight=weight, release_threshold=release_threshold,
        target_npc=target_npc, intent_kind="wait", intent_target=None,
        intent_fields={"ticks": 1}, trigger=trigger, climax=climax,
        channel=channel, weight_modifiers=weight_modifiers,
        first_time_only=first_time_only, options=options,
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
    assert entropy(projection, iter([]), PACK.rules, 0) == 0  # no threats


def test_entropy_sums_hook_weights() -> None:
    projection = initial_projection(PACK.entities)
    hooks = [_seeded_hook(weight=2), _seeded_hook(weight=3)]
    # only the unreleased contribute
    assert entropy(projection, iter(hooks), PACK.rules, 0) == 5


def test_entropy_reads_global_suspicion() -> None:
    projection = initial_projection(PACK.entities)
    projection["npc_guard_01"]["relations.suspicion"] = 25
    projection["npc_guard_02"]["relations.suspicion"] = 10
    assert entropy(projection, iter([]), PACK.rules, 0) == 35


def test_entropy_counts_visible_physical_threats() -> None:
    projection = initial_projection(PACK.entities)
    projection["loc_tavern"]["fire.bar"] = "burning"
    projection["loc_tavern"]["fire.tables"] = "burning"
    assert entropy(projection, iter([]), PACK.rules, 0) == 2


def test_entropy_threat_states_are_pack_data() -> None:
    """D-057: the threat sensor reads the layers' declared spot_state —
    a pack whose layer spreads under a different vocabulary stays
    visible to the director (zero hardcoded state values)."""
    projection = initial_projection(PACK.entities)
    projection["loc_tavern"]["fire.bar"] = "burning"
    rules = json.loads(json.dumps(dict(PACK.data)))
    rules["rules.json"]["transitions"]["fire"]["spot_state"] = "smoldering"
    # the old vocabulary no longer reads as a threat...
    assert entropy(projection, iter([]), rules["rules.json"], 0) == 0
    # ...the declared one does
    projection["loc_tavern"]["fire.tables"] = "smoldering"
    assert entropy(projection, iter([]), rules["rules.json"], 0) == 1


def test_entropy_never_reads_knowledge_records() -> None:
    """L6: entropy is observable state only. A knower's records must
    never feed the director's release decision — the Influence Boundary
    extends from the perceiver (EPIST-1) to the director itself."""
    projection = initial_projection(PACK.entities)
    # stuff a knowledge record into the projection — the director MUST
    # not see it (it lives in the KnowledgeView, not the projection)
    projection["npc_guard_01"]["knowledge.figure_reaching_for_purse"] = True
    assert entropy(projection, iter([]), PACK.rules, 0) == 0


# -- explicit triggers (causal, fire regardless of entropy) -------------------


def test_threshold_trigger_fires_when_suspicion_crosses() -> None:
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director.seed(_record(hooks=("possible_document_check",)))
    projection = initial_projection(PACK.entities)
    # suspicion below the threshold (50): trigger does not fire — even
    # with the confrontation world in place (guard on post, PC present)
    projection["npc_guard_01"]["position"] = "loc_tavern"
    projection["pc_01"]["position"] = "loc_tavern"
    assert director.releases(projection, beat_tick=0) == []
    # suspicion crosses 50 with the confrontation world open: the
    # trigger + the option gate both pass — the real document_check
    # intent releases (iter-43: the stub wait became the action, D-072).
    # entropy_floor=0 means stagnation never releases (entropy can't be
    # negative), only the explicit threshold trigger can release here
    projection["npc_guard_01"]["relations.suspicion"] = 50
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert released[0].kind == "document_check"
    assert released[0].actor == "npc_guard_01"
    assert released[0].target == "pc_01"
    assert released[0].fields == {}


def test_the_confrontation_gate_defers_the_release() -> None:
    """iter-43 (D-072): the option gate is the release's world check —
    the band open without the confrontation (the watcher off the post,
    or the stranger elsewhere) means the hook WAITS: nothing hits the
    door, no budget is consumed (the drama-2 deferred-release law; the
    canonical day1 shape — Doren rotates off the post the beat his
    band opens)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director.seed(_record(hooks=("possible_document_check",)))
    projection = initial_projection(PACK.entities)
    projection["npc_guard_01"]["relations.suspicion"] = 55  # the band
    # the watcher sits at the guardroom (post-rotation), the PC at the
    # tavern: the gate's place leaf fails — the hook waits
    projection["npc_guard_01"]["position"] = "loc_guardroom"
    projection["pc_01"]["position"] = "loc_tavern"
    assert director.releases(projection, beat_tick=0) == []
    # the watcher returns to the post with the stranger present: the
    # gate opens, the release fires
    projection["npc_guard_01"]["position"] = "loc_tavern"
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1 and released[0].kind == "document_check"


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


# -- the multi-channel split (iter-39, DIR-4; the L4D family) -----------------

# pack wiring


def test_pack_declares_the_three_channels() -> None:
    """The tavern pack instantiates the L4D family as three pacing
    dimensions (threat / social / ambient — the names are the pack's
    own); both existing hooks are classified, the ambient channel is
    declared-but-dormant (no hook carries it — the owner's content
    call, the climax-flag precedent)."""
    channels = channels_from_rules(PACK.rules)
    assert channels == {
        "threat": ChannelConfig(entropy_floor=3, inputs=frozenset({"physical_threats"})),
        "social": ChannelConfig(entropy_floor=5, inputs=frozenset({"suspicion"})),
        "ambient": ChannelConfig(entropy_floor=2, inputs=frozenset()),
    }
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    director.seed(_record(hooks=("possible_document_check",), event_id="ev_0002"))
    assert director.hooks[0].channel == "social"
    assert director.hooks[1].channel == "threat"


def test_channel_input_vocabulary_is_closed() -> None:
    """CHANNEL_INPUTS is the two world-sensing P2e terms decomposed per
    channel — the closed vocabulary the pack lint enforces against."""
    assert CHANNEL_INPUTS == ("suspicion", "physical_threats")


def test_channel_entropies_bind_only_the_declared_inputs() -> None:
    """A channel senses its OWN hooks plus the inputs it binds:
    suspicion feeds the social channel only, burning spots the threat
    channel only, the ambient channel senses nothing but its own hooks
    (the noise floor). Channelless hooks count toward the TOTAL only —
    the pacing clock's input, unchanged (P2e invariant)."""
    channels = channels_from_rules(PACK.rules)
    assert channels is not None
    projection = initial_projection(PACK.entities)
    projection["npc_guard_01"]["relations.suspicion"] = 10
    projection["loc_tavern"]["fire.bar"] = "burning"
    hooks = [
        _seeded_hook(channel="social", weight=2),
        _seeded_hook(channel="threat", weight=3),
        _seeded_hook(channel="ambient", weight=1),
        _seeded_hook(weight=2),  # channelless: total only
    ]
    per_channel = channel_entropies(channels, projection, iter(hooks), PACK.rules, 0)
    assert per_channel == {
        "threat": 3 + 1,  # own weights + the burning spot
        "social": 2 + 10,  # own weights + global suspicion
        "ambient": 1,  # own weights only
    }
    assert entropy(projection, iter(hooks), PACK.rules, 0) == 2 + 3 + 1 + 2 + 10 + 1


# the quiet path, per channel


def test_a_quiet_channel_releases_while_another_burns() -> None:
    """THE multi-channel law (DIR-4): the quiet gate is per hook — a
    quiet social channel injects while the threat channel is loud. The
    v0.1 global floor refuses the exact same world (total entropy above
    the floor): the split is the win the single gate cannot express."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="social", weight=2, release_threshold=10,
    ))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="threat", weight=3, release_threshold=5,
        target_npc="npc_guard_02",
    ))
    projection = initial_projection(PACK.entities)
    projection["loc_tavern"]["fire.bar"] = "burning"
    # threat = 3 + 1 spot = 4 >= floor 3 (loud); social = 2 + 0 = 2 < 5
    # (quiet); TOTAL 6 >= the v0.1 floor 5 — the channels pack releases
    # the social hook anyway; the clock reads 6 < 25 = RAMP, permitted
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert released[0].actor == "npc_guard_01"


def test_a_quiet_channel_stays_silent_under_the_v01_floor(
    tmp_path: Path,
) -> None:
    """The same world under a pack WITHOUT the channels block: one
    global floor gates everything — total 6 >= 5, no release (the v0.1
    behavior the channels-less pack keeps, byte-identically)."""
    pack = _mutated_pack(tmp_path, lambda rules: rules["director"].pop("channels"))
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(weight=2, release_threshold=10))  # type: ignore[attr-defined]
    director._hooks.append(_seeded_hook(weight=3, release_threshold=5, target_npc="npc_guard_02"))  # type: ignore[attr-defined]
    projection = initial_projection(pack.entities)
    projection["loc_tavern"]["fire.bar"] = "burning"
    assert director.releases(projection, beat_tick=0) == []


def test_no_release_when_every_declared_channel_is_loud() -> None:
    """Both channels above their own floors: no quiet release — the
    multi-channel split never lowers the bar the v0.1 floor set for
    actually-quiet worlds, it only decomposes the question."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="social", weight=2, release_threshold=10,
    ))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="threat", weight=3, release_threshold=5,
        target_npc="npc_guard_02",
    ))
    projection = initial_projection(PACK.entities)
    projection["npc_guard_01"]["relations.suspicion"] = 10  # social 12 >= 5
    projection["loc_tavern"]["fire.bar"] = "burning"  # threat 4 >= 3
    assert director.releases(projection, beat_tick=0) == []


def test_the_real_document_check_never_releases_quietly() -> None:
    """The pack's own numbers: the document-check's weight (3) meets its
    threat channel floor (3) — the quiet path self-blocks. An escalation
    never spawns because the world is boring: it fires causally (its
    suspicion-50 trigger) or via the climax path when the flag lands
    (§11, the owner's content call). The social vigil (2 < 5) still
    quietly releases — the small hooks own the quiet path."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    director.seed(_record(hooks=("possible_document_check",), event_id="ev_0002"))
    projection = initial_projection(PACK.entities)
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert director.hooks[0].tag == "guard_suspicious_of_pc"
    # the document-check stays pending — its channel is not quiet
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director2.seed(_record(hooks=("possible_document_check",)))
    assert director2.releases(projection, beat_tick=0) == []


def test_the_clock_gate_is_global_across_channels() -> None:
    """The pacing clock reads TOTAL entropy — one drama arc for every
    channel: a PEAK suppresses even a channel whose own dimension is
    quiet (the world is loud; the director does not add — any channel)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="threat", weight=25, release_threshold=5,
        target_npc="npc_guard_02",
    ))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="social", weight=2, release_threshold=10,
    ))
    projection = initial_projection(PACK.entities)
    director.next_beat()
    # total 27 >= peak_floor 25 -> PEAK; social entropy 2 < 5 is quiet
    assert director.releases(projection, beat_tick=0) == []
    assert director.pacing is not None and director.pacing.state == "PEAK"


def test_explicit_triggers_ignore_the_channel_gates() -> None:
    """D-005: causality is not pacing and not channeling — a threat
    hook's explicit time trigger fires while the threat channel itself
    is loud (the channels gate only the quiet path)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="threat", weight=3, release_threshold=5,
        trigger={"kind": "time", "tick": 0},
    ))
    projection = initial_projection(PACK.entities)
    projection["loc_tavern"]["fire.bar"] = "burning"  # threat loud
    assert len(director.releases(projection, beat_tick=0)) == 1


def test_channelless_hook_keeps_the_global_floor_in_a_channels_pack() -> None:
    """The per-hook opt-in (the climax-flag pattern): a channelless hook
    in a channels pack rides the v0.1 global floor — the mixed mode is
    legal; so is a tag naming no declared channel (dormant vocabulary,
    impossible via lint, defensive here)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(weight=2, release_threshold=10))  # type: ignore[attr-defined]
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="ghost", weight=2, release_threshold=11, target_npc="npc_guard_02",
    ))
    projection = initial_projection(PACK.entities)
    # total 4 < the global floor 5: both channelless-path hooks release
    # through the global gate, the lowest threshold first (budget 1)
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert released[0].actor == "npc_guard_01"  # threshold 10 < 11
    # total 5 >= the floor: the global gate closes for both
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director2._hooks.append(_seeded_hook(weight=5, release_threshold=10))  # type: ignore[attr-defined]
    assert director2.releases(projection, beat_tick=0) == []


def test_channels_share_the_one_release_budget() -> None:
    """The budget is 1 release per beat across ALL channels (L4D's
    spawn budget is per side, not per director); the pick stays the
    global lowest-threshold tiebreak — the ambient hook (5) beats the
    social hook (10) across the channel split."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="social", weight=2, release_threshold=10,
    ))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="ambient", weight=1, release_threshold=5,
        target_npc="npc_maid_01",
    ))
    projection = initial_projection(PACK.entities)
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert released[0].actor == "npc_maid_01"


def test_disabled_policy_blocks_every_channel() -> None:
    """T8 A/B: a disabled director never releases — every channel's
    quiet gate included (DisabledPolicy.permit_quiet is False); the
    buffer still seeds."""
    director = Director(pack=PACK, policy=DISABLED)
    director._hooks.append(_seeded_hook(channel="social", weight=2, release_threshold=10))  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    assert director.releases(projection, beat_tick=0) == []


def test_the_climax_path_ignores_the_channels() -> None:
    """The boss gate reads TOTAL entropy (the third layer) — channels
    do not touch the climax path: a climax-flagged threat hook releases
    at the end of a peak exactly as in the channels-less iter-38 shape,
    PEAK_CLIMAX and all."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        channel="threat", weight=80, release_threshold=5, climax=True,
    ))
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert len(director.releases(projection, beat_tick=0)) == 1
    assert director.pacing == PacingClock(state="PEAK_CLIMAX", beats_in_state=1)


def test_channel_tag_without_the_block_is_dormant_vocabulary(
    tmp_path: Path,
) -> None:
    """The mirror of the climax-flag-without-layer law: a pack whose
    hooks carry channel tags but declare no channels block lints clean
    and runs the v0.1 global-floor quiet path — the tag is inert data
    (a second pack may declare the block and activate it, zero engine
    changes)."""
    pack = _mutated_pack(tmp_path, lambda rules: rules["director"].pop("channels"))
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    assert director.hooks[0].channel == "social"  # the tag survives, inert
    projection = initial_projection(pack.entities)
    # the global floor gates: total 2 < 5 -> release (v0.1 behavior)
    assert len(director.releases(projection, beat_tick=0)) == 1


# pack lint (the multi-channel contract)


def test_channels_lint_rejects_unknown_input(tmp_path: Path) -> None:
    """The input vocabulary is closed (CHANNEL_INPUTS): a channel
    binding an input the engine does not sense fails the load loudly —
    dead pack data never reaches the simulation (the KI#15 family)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["channels"]["social"]["inputs"] = ["suspicion", "gossip"]

    with pytest.raises(PackError, match="inputs"):
        _mutated_pack(tmp_path, mutate)


def test_channels_lint_rejects_negative_floor(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["channels"]["threat"]["entropy_floor"] = -1

    with pytest.raises(PackError, match="entropy_floor"):
        _mutated_pack(tmp_path, mutate)


def test_channels_lint_rejects_undeclared_hook_channel(tmp_path: Path) -> None:
    """With the channels block present, a hook's channel tag must name
    a declared channel — the typo fails at load, not silently at
    runtime (where it would fall back to the global floor)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["hooks"]["guard_suspicious_of_pc"]["channel"] = "menace"

    with pytest.raises(PackError, match="declared director.channels"):
        _mutated_pack(tmp_path, mutate)


def test_channels_lint_rejects_non_string_channel(tmp_path: Path) -> None:
    """Without the channels block the tag is inert — but it must still
    be a string when present (the field's type is dataclass-typed
    `str | None`; a non-string tag would lie about its own type)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"].pop("channels")
        rules["director"]["hooks"]["guard_suspicious_of_pc"]["channel"] = 5

    with pytest.raises(PackError, match="channel must be a string"):
        _mutated_pack(tmp_path, mutate)


# -- helpers -----------------------------------------------------------------


# -- drama-1 (iter-40: the event grammar's predicate + weight layer) ----------


def test_seed_reads_the_multiplier_shape() -> None:
    """The pack's own vigil hook declares the weight_multiplier object +
    first_time_only: seed() flattens to (base, modifier tail) and the
    burn flag — the buffer stores data, the effective weight is
    computed per evaluation (L3: never a stored projection). The flat
    document-check weight stays the v0.1 form."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    vigil = director.hooks[0]
    assert vigil.weight == 2
    assert len(vigil.weight_modifiers) == 1
    assert vigil.weight_modifiers[0]["add"] == 2
    assert vigil.first_time_only is True
    director.seed(_record(hooks=("possible_document_check",), event_id="ev_0002"))
    check = director.hooks[1]
    assert check.weight == 3
    assert check.weight_modifiers == ()
    # iter-43: the document-check pair burns after its one release
    # (the Wesnoth fire-only-once law — a talked-down verdict never
    # re-rolls); the flat weight stays the v0.1 form
    assert check.first_time_only is True


def test_entropy_reads_the_pack_escalation() -> None:
    """The pack's own modifier: the vigil doubles its tension once the
    watcher's suspicion reaches the document-check band (50). The
    suspicion axis itself sums into entropy — at 49 the total is
    2 + 49, at 50 it jumps to 4 + 50 (the escalation a flat weight
    cannot express)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    hook = director.hooks[0]
    projection = initial_projection(PACK.entities)
    projection["npc_guard_01"]["relations.suspicion"] = 49
    assert entropy(projection, iter([hook]), PACK.rules, 0) == 2 + 49
    projection["npc_guard_01"]["relations.suspicion"] = 50
    assert entropy(projection, iter([hook]), PACK.rules, 0) == 4 + 50


def test_entropy_weight_modifier_reads_any_predicate() -> None:
    """A modifier's `when` may read any leaf — here a prop (fatigue, an
    axis entropy never sums) and a time leaf (the beat_tick threading:
    the tension can ripen with the clock)."""
    fatigue_hook = _seeded_hook(
        weight_modifiers=({"add": 2, "when": {
            "kind": "prop", "of": "npc_guard_01", "path": "status.fatigue",
            "comparator": "at_least", "value": 30,
        }},),
    )
    time_hook = _seeded_hook(
        weight_modifiers=({"factor": 2.0, "when": {"kind": "time", "tick": 100}},),
    )
    projection = initial_projection(PACK.entities)
    projection["npc_guard_01"]["status.fatigue"] = 29
    assert entropy(projection, iter([fatigue_hook]), PACK.rules, 0) == 2
    projection["npc_guard_01"]["status.fatigue"] = 30
    assert entropy(projection, iter([fatigue_hook]), PACK.rules, 0) == 4
    assert entropy(projection, iter([time_hook]), PACK.rules, 99) == 2
    assert entropy(projection, iter([time_hook]), PACK.rules, 100) == 4


def test_weight_modifiers_apply_in_order_and_truncate() -> None:
    """add runs before a later factor (declaration order), factors
    truncate toward zero (weights are non-negative — floor), and a
    factor of 0 legally zeroes the tension (a hook may go quiet
    without seeding a new fact)."""
    composed = _seeded_hook(
        weight=2,
        weight_modifiers=(
            {"add": 3, "when": {"kind": "time", "tick": 0}},
            {"factor": 0.5, "when": {"kind": "time", "tick": 0}},
        ),
    )
    zeroed = _seeded_hook(
        weight_modifiers=({"factor": 0, "when": {"kind": "time", "tick": 0}},),
    )
    truncated = _seeded_hook(
        weight=3,
        weight_modifiers=({"factor": 0.5, "when": {"kind": "time", "tick": 0}},),
    )
    projection = initial_projection(PACK.entities)
    hooks = iter([composed, zeroed, truncated])
    # (2 + 3) * 0.5 = 2.5 -> 2; 2 * 0 = 0; 3 * 0.5 = 1.5 -> 1
    assert entropy(projection, hooks, PACK.rules, 0) == 2 + 0 + 1


def test_first_time_only_burns_the_tag() -> None:
    """The Wesnoth fire-only-once law: once any instance of a
    first_time_only tag releases, the tag burns for the run — the
    remaining instance never releases AND stops counting toward
    entropy (un-dischargeable tension is noise). The beat-3
    differential proves the filter: un-burned, the second instance
    (weight 2, threshold 5, cooldown expired) would release there."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    first = _seeded_hook(
        tag="guard_suspicious_of_pc", weight=2, release_threshold=5,
        first_time_only=True,
    )
    second = _seeded_hook(
        tag="guard_suspicious_of_pc", weight=2, release_threshold=5,
        first_time_only=True,
    )
    other = _seeded_hook(
        tag="possible_document_check", target_npc="npc_drunk_01",
        weight=1, release_threshold=20,
    )
    director._hooks.extend([first, second, other])  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # beat 1: entropy 5 < floor 10; lowest threshold (5) wins, oldest
    # first — the first vigil releases and burns the tag
    director.next_beat()
    assert len(director.releases(projection, beat_tick=0)) == 1
    # beat 2: the burned instance is filtered; the other tag is free
    # (its npc never had a release) and releases on the quiet path
    director.next_beat()
    released = director.releases(projection, beat_tick=360)
    assert len(released) == 1
    # beat 3: only the burned instance remains — filtered from the
    # buffer view, so entropy reads 0 and nothing releases
    director.next_beat()
    assert director.releases(projection, beat_tick=720) == []


def test_repeatable_tag_releases_every_instance() -> None:
    """Without first_time_only the v0.1 law holds: every seeded
    instance is its own consequence — the second failure's vigil
    releases on its own beat (after the per-NPC cooldown clears)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    director._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(weight=2, release_threshold=5),
        _seeded_hook(weight=2, release_threshold=5),
    ])
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert len(director.releases(projection, beat_tick=0)) == 1
    director.next_beat()
    # beat 2: the cooldown (2 beats on npc_guard_01) still holds
    assert director.releases(projection, beat_tick=360) == []
    director.next_beat()
    assert len(director.releases(projection, beat_tick=720)) == 1


def test_compound_trigger_needs_every_leg() -> None:
    """A compound trigger composes leaves: the hook releases only when
    every leg holds (the Paradox implicit-AND root, as a hook
    trigger)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    hook = _seeded_hook(
        trigger={"all": [
            {"kind": "threshold", "target_npc": "npc_guard_01",
             "axis": "suspicion", "comparator": "at_least", "value": 25},
            {"kind": "place", "target_npc": "npc_guard_01",
             "location": "loc_tavern"},
        ]},
    )
    director._hooks.append(hook)  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    # the guard is at the tavern but suspicion is 0: the threshold leg fails
    assert director.releases(projection, beat_tick=0) == []
    projection["npc_guard_01"]["relations.suspicion"] = 25
    assert len(director.releases(projection, beat_tick=0)) == 1


# pack lint (the drama-1 grammar contract)


def test_weight_lint_rejects_modifier_with_both_add_and_factor(
    tmp_path: Path,
) -> None:
    """The donor's modifier shape is exactly one of add|factor — both
    in one modifier is a shape error, never an evaluation-order
    guess."""
    def mutate(rules: dict[str, Any]) -> None:
        modifier = rules["director"]["hooks"]["guard_suspicious_of_pc"][
            "weight"]["modifiers"][0]
        modifier["factor"] = 0.5

    with pytest.raises(PackError, match="exactly one of add\\|factor"):
        _mutated_pack(tmp_path, mutate)


def test_weight_lint_rejects_malformed_when_predicate(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        modifier = rules["director"]["hooks"]["guard_suspicious_of_pc"][
            "weight"]["modifiers"][0]
        modifier["when"] = {"kind": "vibes", "target_npc": "npc_guard_01"}

    with pytest.raises(PackError, match="kind must be"):
        _mutated_pack(tmp_path, mutate)


def test_trigger_lint_rejects_unknown_predicate_kind(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["hooks"]["possible_document_check"]["trigger"] = {
            "kind": "omen", "target_npc": "npc_guard_01",
        }

    with pytest.raises(PackError, match="kind must be"):
        _mutated_pack(tmp_path, mutate)


def test_trigger_lint_rejects_prop_with_unknown_entity(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["hooks"]["possible_document_check"]["trigger"] = {
            "kind": "prop", "of": "npc_ghost", "path": "status.fear",
            "comparator": "at_least", "value": 10,
        }

    with pytest.raises(PackError, match="'of' must name an entity"):
        _mutated_pack(tmp_path, mutate)


def test_trigger_lint_rejects_empty_compound_as_dead_vocabulary(
    tmp_path: Path,
) -> None:
    """L1: an empty all/any is dead vocabulary (vacuous semantics are
    the evaluator's honesty, not a license for empty pack data)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["hooks"]["possible_document_check"]["trigger"] = {
            "all": [],
        }

    with pytest.raises(PackError, match="non-empty list"):
        _mutated_pack(tmp_path, mutate)


def test_first_time_only_lint_rejects_non_boolean(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["hooks"]["guard_suspicious_of_pc"][
            "first_time_only"
        ] = "yes"

    with pytest.raises(PackError, match="first_time_only must be a boolean"):
        _mutated_pack(tmp_path, mutate)



# -- drama-2 (iter-41: the event grammar's option layer) ----------------------


def _option(
    *, weight: Any = 1, trigger: dict[str, Any] | None = None,
    weight_modifiers: tuple[dict[str, Any], ...] = (),
    intent: dict[str, Any] | None = None,
) -> OptionSpec:
    """A manual option spec (the mirrored `_seeded_hook` helper)."""
    return OptionSpec(
        trigger=trigger, weight=int(weight) if isinstance(weight, int) else weight,
        weight_modifiers=weight_modifiers, intent=intent,
    )


def test_a_hook_without_options_runs_the_v01_payload() -> None:
    """The pure-addition law: an option-less hook releases the exact
    base payload — the implicit base option carries it unchanged, the
    release id sequence starts at director_0000. Since iter-43 every
    pack hook declares options (the vigil's pair, the document-check
    pair's confrontation gates), so the law is pinned through a
    synthetic option-less hook — the mechanism, not a pack instance.
    The T1/T8/corpus byte-identity is the suite-level pin of the same
    law."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director._hooks.append(_seeded_hook(  # type: ignore[attr-defined]
        tag="hookless_v01", target_npc="npc_guard_01",
        trigger={"kind": "threshold", "target_npc": "npc_guard_01",
                 "axis": "suspicion", "value": 0, "comparator": "at_least"},
    ))
    projection = initial_projection(PACK.entities)
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    intent = released[0]
    assert intent.id == "director_0000"
    assert intent.kind == "wait"
    assert intent.actor == "npc_guard_01"
    assert intent.target is None
    assert intent.fields == {"ticks": 1}


def test_seed_flattens_the_vigil_option_specs() -> None:
    """The pack's own vigil hook declares the glance/stare pair: seed()
    flattens both options — the glance's flat 1, the stare's multiplier
    (base 1 + the escalation tail), the fields-only payload overrides.
    The document-check pair (iter-43) declares the confrontation gates:
    one option each, the compound implicit-AND root, the default
    weight, no payload override — the base payload rides."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    vigil = director.hooks[0]
    assert len(vigil.options) == 2
    glance, stare = vigil.options
    assert glance.weight == 1 and glance.weight_modifiers == ()
    assert glance.trigger is None
    assert glance.intent == {"fields": {"ticks": 1}}
    assert stare.weight == 1
    assert len(stare.weight_modifiers) == 1
    assert stare.weight_modifiers[0]["add"] == 2
    assert stare.intent == {"fields": {"ticks": 2}}
    director.seed(_record(hooks=("possible_document_check",), event_id="ev_0002"))
    (gate,) = director.hooks[1].options
    assert gate.weight == 1 and gate.weight_modifiers == ()
    assert gate.intent is None  # no override: the base payload rides
    assert isinstance(gate.trigger, list) and len(gate.trigger) == 2
    assert {leaf["kind"] for leaf in gate.trigger} == {"place", "prop"}


def test_the_pack_vigil_releases_the_glance_below_the_band() -> None:
    """The pack's own pair, live through the real quiet path: at
    suspicion 0 both options weigh 1 — the tie breaks by declaration
    order, the glance (the v0.1 payload) wins. The release burns the
    first_time_only tag; a later beat releases nothing."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    director.seed(_record(hooks=("guard_suspicious_of_pc",)))
    projection = initial_projection(PACK.entities)
    director.next_beat()
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert released[0].kind == "wait"
    assert released[0].fields == {"ticks": 1}
    director.next_beat()
    assert director.releases(projection, beat_tick=360) == []


def test_option_weights_decide_the_pick() -> None:
    """The ai_chance law, deterministic: the heaviest effective weight
    wins; a tie keeps the earlier declaration. The choice is a pure
    function of the world — never a draw."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    heavy = _seeded_hook(
        trigger={"kind": "time", "tick": 0},
        options=(
            _option(weight=1, intent={"fields": {"ticks": 1}}),
            _option(weight=3, intent={"fields": {"ticks": 2}}),
        ),
    )
    tie = _seeded_hook(
        trigger={"kind": "time", "tick": 0},
        options=(
            _option(intent={"fields": {"ticks": 5}}),
            _option(intent={"fields": {"ticks": 6}}),
        ),
    )
    projection = initial_projection(PACK.entities)
    director._hooks.append(heavy)  # type: ignore[attr-defined]
    released = director.releases(projection, beat_tick=0)
    assert released[0].fields == {"ticks": 2}  # the heavier option
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director2._hooks.append(tie)  # type: ignore[attr-defined]
    released = director2.releases(projection, beat_tick=0)
    assert released[0].fields == {"ticks": 5}  # the first declared


def test_option_weight_modifiers_read_the_world() -> None:
    """The pack's own escalation shape, on the pick: below the band the
    glance wins the tie; in the band the stare's escalated weight (1+2)
    beats the glance's flat 1 — the release CHOICE hardens with the
    world exactly as the hook's tension does (two layers, one band)."""
    glance = _option(weight=1, intent={"fields": {"ticks": 1}})
    stare = _option(
        weight_modifiers=(
            {"add": 2, "when": {
                "kind": "threshold", "target_npc": "npc_guard_01",
                "axis": "suspicion", "comparator": "at_least", "value": 50,
            }},
        ),
        intent={"fields": {"ticks": 2}},
    )
    projection = initial_projection(PACK.entities)
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(trigger={"kind": "time", "tick": 0}, options=(glance, stare))
    )
    released = director.releases(projection, beat_tick=0)
    assert released[0].fields == {"ticks": 1}  # suspicion 0: the tie -> glance
    projection["npc_guard_01"]["relations.suspicion"] = 50
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director2._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(trigger={"kind": "time", "tick": 0}, options=(glance, stare))
    )
    released = director2.releases(projection, beat_tick=0)
    assert released[0].fields == {"ticks": 2}  # in the band: the stare


def test_option_availability_gate_defers_the_release() -> None:
    """The deferred-release law: a hook whose options are ALL gated off
    cannot release that beat — nothing hits the door (the id sequence
    proves no intent was built), and the hook stays in the buffer until
    a world where an option opens. The trigger re-fires next beat."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(
            trigger={"kind": "time", "tick": 0},
            options=(
                _option(
                    trigger={"kind": "time", "tick": 100},
                    intent={"fields": {"ticks": 2}},
                ),
            ),
        )
    )
    projection = initial_projection(PACK.entities)
    # the hook's own trigger fires at tick 0, but the option's gate
    # opens only at tick 100: no release, nothing spent
    assert director.releases(projection, beat_tick=50) == []
    released = director.releases(projection, beat_tick=100)
    assert len(released) == 1
    assert released[0].id == "director_0000"  # the budget was never spent
    assert released[0].fields == {"ticks": 2}


def test_zero_weight_options_are_never_picked() -> None:
    """The Stellaris factor-0 zero-out: an available option weighing a
    zero effective weight is never picked — and a hook whose every
    option zeroes out cannot release at all (the hook may go quiet
    without seeding a new fact)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(
            trigger={"kind": "time", "tick": 0},
            options=(
                _option(
                    weight_modifiers=({"factor": 0, "when": {"kind": "time", "tick": 0}},),
                    intent={"fields": {"ticks": 1}},
                ),
                _option(weight=2, intent={"fields": {"ticks": 2}}),
            ),
        )
    )
    projection = initial_projection(PACK.entities)
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert released[0].fields == {"ticks": 2}  # the zeroed option skipped
    all_zero = _seeded_hook(
        trigger={"kind": "time", "tick": 0},
        options=(
            _option(weight=0, intent={"fields": {"ticks": 1}}),
            _option(
                weight_modifiers=({"factor": 0, "when": {"kind": "time", "tick": 0}},),
                intent={"fields": {"ticks": 2}},
            ),
        ),
    )
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director2._hooks.append(all_zero)  # type: ignore[attr-defined]
    assert director2.releases(projection, beat_tick=0) == []


def test_an_option_intent_overrides_the_base_payload() -> None:
    """The whole-key merge: each declared key of the option's intent
    block (kind / target / fields) wholly replaces the base payload's;
    an undeclared key inherits. An option without an intent block
    carries the base payload unchanged."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(
            trigger={"kind": "time", "tick": 0},
            options=(
                _option(intent={
                    "kind": "talk", "target": "npc_barkeep_01",
                    "fields": {"topic": "the_missing_purse"},
                }),
            ),
        )
    )
    projection = initial_projection(PACK.entities)
    released = director.releases(projection, beat_tick=0)
    assert released[0].kind == "talk"
    assert released[0].target == "npc_barkeep_01"
    assert released[0].fields == {"topic": "the_missing_purse"}
    # partial override: kind only — target and fields inherit the base
    director2 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director2._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(
            trigger={"kind": "time", "tick": 0},
            options=(_option(intent={"kind": "wait"}),),
        )
    )
    released = director2.releases(projection, beat_tick=0)
    assert released[0].kind == "wait"
    assert released[0].target is None
    assert released[0].fields == {"ticks": 1}
    # no intent block at all: the base payload, wholly
    director3 = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=0))
    director3._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(trigger={"kind": "time", "tick": 0}, options=(_option(),))
    )
    released = director3.releases(projection, beat_tick=0)
    assert released[0].kind == "wait"
    assert released[0].fields == {"ticks": 1}


def test_options_do_not_touch_entropy() -> None:
    """One owner per number: the HOOK's effective weight is the tension
    (drama-1's law); the option weights are choice-local and never feed
    entropy — a hook with heavyweight options contributes exactly its
    own effective weight."""
    projection = initial_projection(PACK.entities)
    flat = _seeded_hook(weight=2)
    loaded = _seeded_hook(
        weight=2,
        options=(
            _option(weight=9, intent={"fields": {"ticks": 9}}),
            _option(weight=5),
        ),
    )
    assert entropy(projection, iter([flat]), PACK.rules, 0) == (
        entropy(projection, iter([loaded]), PACK.rules, 0)
    )


def test_the_climax_path_resolves_the_option_choice() -> None:
    """The boss path composes with the option layer: the release
    carries the chosen option's payload and marks the beat PEAK_CLIMAX.
    A boss whose options are all closed does not release — and does not
    mark the beat (the state stays PEAK; the closed boss is not a
    spent boss)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    director._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(
            weight=80, release_threshold=5, climax=True,
            options=(
                _option(weight=1, intent={"fields": {"ticks": 1}}),
                _option(weight=2, intent={"fields": {"ticks": 3}}),
            ),
        )
    )
    projection = initial_projection(PACK.entities)
    director.next_beat()
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert released[0].fields == {"ticks": 3}
    assert director.pacing == PacingClock(state="PEAK_CLIMAX", beats_in_state=1)
    closed = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=5))
    closed._hooks.append(  # type: ignore[attr-defined]
        _seeded_hook(
            weight=80, release_threshold=5, climax=True,
            options=(_option(trigger={"kind": "time", "tick": 9999}),),
        )
    )
    closed.next_beat()
    assert closed.releases(projection, beat_tick=0) == []
    assert closed.pacing == PacingClock(state="PEAK", beats_in_state=1)


def test_first_time_only_burns_through_the_option_pick() -> None:
    """The burn law is orthogonal to the choice: whichever option wins,
    the release burns a first_time_only tag — the second instance
    never releases (its own options cannot reopen a burned tag)."""
    director = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    options = (
        _option(weight=2, intent={"fields": {"ticks": 2}}),
        _option(intent={"fields": {"ticks": 1}}),
    )
    director._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(
            weight=2, release_threshold=5, first_time_only=True,
            options=options,
        ),
        _seeded_hook(
            weight=2, release_threshold=5, first_time_only=True,
            options=options,
        ),
    ])
    projection = initial_projection(PACK.entities)
    director.next_beat()
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1
    assert released[0].fields == {"ticks": 2}  # the heavier option won
    # beat 2: the burned tag filters the second instance — entropy
    # reads 0, nothing releases
    director.next_beat()
    director.next_beat()
    assert director.releases(projection, beat_tick=720) == []


# pack lint (the drama-2 option contract)


def test_options_lint_rejects_an_empty_list(tmp_path: Path) -> None:
    """L1: an empty options list is dead vocabulary — the closed-hook
    law is for worlds that change, not for pack authors who never
    declared a choice."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["hooks"]["guard_suspicious_of_pc"]["options"] = []

    with pytest.raises(PackError, match="options must be a non-empty list"):
        _mutated_pack(tmp_path, mutate)


def test_options_lint_rejects_unknown_option_key(tmp_path: Path) -> None:
    """A typo'd key is a shape error, never a silent ignore — `triger`
    would read as an always-available option (the drift the closed
    vocabulary exists to catch)."""
    def mutate(rules: dict[str, Any]) -> None:
        option = rules["director"]["hooks"]["guard_suspicious_of_pc"]["options"][0]
        option["triger"] = {"kind": "time", "tick": 0}

    with pytest.raises(PackError, match="unknown option keys"):
        _mutated_pack(tmp_path, mutate)


def test_option_trigger_lint_rejects_unknown_predicate_kind(
    tmp_path: Path,
) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        option = rules["director"]["hooks"]["guard_suspicious_of_pc"]["options"][0]
        option["trigger"] = {"kind": "omen", "target_npc": "npc_guard_01"}

    with pytest.raises(PackError, match="kind must be"):
        _mutated_pack(tmp_path, mutate)


def test_option_weight_lint_rejects_both_add_and_factor(
    tmp_path: Path,
) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        option = rules["director"]["hooks"]["guard_suspicious_of_pc"]["options"][1]
        modifier = option["weight"]["modifiers"][0]
        modifier["factor"] = 0.5

    with pytest.raises(PackError, match="exactly one of add\\|factor"):
        _mutated_pack(tmp_path, mutate)


def test_option_intent_lint_rejects_unknown_action(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        option = rules["director"]["hooks"]["guard_suspicious_of_pc"]["options"][0]
        option["intent"] = {"kind": "omen"}

    with pytest.raises(PackError, match="intent.kind must name a pack action"):
        _mutated_pack(tmp_path, mutate)


def test_option_intent_lint_rejects_non_object_fields(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        option = rules["director"]["hooks"]["guard_suspicious_of_pc"]["options"][0]
        option["intent"] = {"fields": "one tick please"}

    with pytest.raises(PackError, match="intent.fields must be an object"):
        _mutated_pack(tmp_path, mutate)


def test_option_intent_lint_rejects_unknown_target(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        option = rules["director"]["hooks"]["guard_suspicious_of_pc"]["options"][0]
        option["intent"] = {"target": "npc_ghost"}

    with pytest.raises(PackError, match="intent.target must be null or name an entity"):
        _mutated_pack(tmp_path, mutate)


# -- arc-1 acceptance (iter-47, P3c — release chains + tension shaping) ----


def _arc_pack(
    tmp_path: Path,
    gap: int = 3,
    members: tuple[str, ...] = (
        "possible_document_check", "possible_document_check_relief",
    ),
) -> Any:
    """The tavern pack plus one declared arc over the watcher pair (the
    test's own members/gap), re-linted — the mutated-pack pattern."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {
            "papers": {
                "members": list(members),
                "min_gap_beats": gap,
                "notes": "the test's chain",
            }
        }

    return _mutated_pack(tmp_path, mutate)


def test_the_committed_pack_declares_the_aftermath_arc() -> None:
    """The live-declaration pin (the iter-51 dormancy flip, content-6's
    landing): the aftermath chain is LIVE in the committed content set —
    the relief's check first (the one hook that releases on any committed
    run — the order law never holds the corpus pin), the barkeep's sweep
    second, gap 2 (the march's spacing: beat 720 refused, beat 1080 the
    room's own — the gap law load-bearing, DIRECTOR_SPEC §3d/D-081)."""
    assert arcs_from_rules(PACK.rules) == {
        "aftermath": ArcConfig(
            members=("possible_document_check_relief", "barkeep_wary_sweep"),
            min_gap_beats=2,
        )
    }


def test_arcs_from_rules_reads_the_declared_chains(tmp_path: Path) -> None:
    """The single arcs read: the members tuple and the gap floor,
flattened at load exactly like the pacing and channel configs. The
closed key set is pinned beside it (the lint's vocabulary, one owner)."""
    assert ARC_KEYS == ("members", "min_gap_beats", "notes")
    pack = _arc_pack(tmp_path, gap=4)
    assert arcs_from_rules(pack.rules) == {
        "papers": ArcConfig(
            members=("possible_document_check", "possible_document_check_relief"),
            min_gap_beats=4,
        )
    }


def test_an_empty_arcs_block_is_legal_and_inert(tmp_path: Path) -> None:
    """`director.arcs: {}` declares no chains — the same release behavior
    as an absent block (the v0.1 tiebreak decides, the lowest threshold
    first). An empty block is not dead vocabulary the way a one-member
    arc is: it declares nothing at all."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {}

    pack = _mutated_pack(tmp_path, mutate)
    assert arcs_from_rules(pack.rules) == {}
    director = Director(pack=pack, policy=EnabledPolicy(entropy_floor=10))
    director._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=2, release_threshold=5,
        ),
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=3, release_threshold=1,
        ),
    ])
    projection = initial_projection(pack.entities)
    director.next_beat()
    released = director.releases(projection, beat_tick=0)
    # v0.1: both eligible, the tiebreak picks the lowest threshold (the
    # relief twin, threshold 1) — no chain holds anything
    assert len(released) == 1 and released[0].actor == "npc_guard_02"


def test_the_order_law_reorders_the_quiet_path(tmp_path: Path) -> None:
    """The ORDER law bites against the v0.1 tiebreak: the relief twin
holds the LOWER threshold (it would win the un-chained pick), but the
chain's first member releases first — the successor is not a candidate
until its predecessor's beat is spent. The un-chained arm (the
committed pack, same hooks) releases the twin first — the differential
that proves the reordering is the arc's, not the world's."""
    hooks = [
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=2, release_threshold=5,
        ),
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=3, release_threshold=1,
        ),
    ]
    chained = Director(
        pack=_arc_pack(tmp_path), policy=EnabledPolicy(entropy_floor=10),
    )
    chained._hooks.extend(hooks)  # type: ignore[attr-defined]
    projection = initial_projection(PACK.entities)
    chained.next_beat()
    released = chained.releases(projection, beat_tick=0)
    assert len(released) == 1 and released[0].actor == "npc_guard_01"
    plain = Director(pack=PACK, policy=EnabledPolicy(entropy_floor=10))
    plain._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=2, release_threshold=5,
        ),
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=3, release_threshold=1,
        ),
    ])
    plain.next_beat()
    released = plain.releases(initial_projection(PACK.entities), beat_tick=0)
    assert len(released) == 1 and released[0].actor == "npc_guard_02"


def test_the_order_law_holds_explicit_triggers(
    tmp_path: Path,
) -> None:
    """The chain is causality, not pacing: a non-current member's FIRING
trigger is held (beat 1 — nothing releases, though the twin's time
trigger fires and the quiet path is closed); the predecessor's own
trigger releases it (beat 2); the successor then releases through its
still-firing trigger IMMEDIATELY (beat 3) — the gap law does not gate
the explicit path (D-005: causality is not pacing, the mid-rest law's
twin)."""
    director = Director(
        pack=_arc_pack(tmp_path, gap=3), policy=EnabledPolicy(entropy_floor=5),
    )
    director._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=2, release_threshold=5,
            trigger={"kind": "time", "tick": 1},
        ),
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=3, release_threshold=1,
            trigger={"kind": "time", "tick": 0},
        ),
    ])
    projection = initial_projection(PACK.entities)
    director.next_beat()
    # the twin's trigger fires but the chain holds it; the quiet path is
    # closed (entropy 5 >= floor 5) — nothing releases
    assert director.releases(projection, beat_tick=0) == []
    director.next_beat()
    released = director.releases(projection, beat_tick=360)
    assert len(released) == 1 and released[0].actor == "npc_guard_01"
    director.next_beat()
    # gap 3 would hold the twin until beat 4 on the quiet path — the
    # explicit path does not consult it
    released = director.releases(projection, beat_tick=720)
    assert len(released) == 1 and released[0].actor == "npc_guard_02"


def test_the_gap_law_spaces_the_quiet_path(tmp_path: Path) -> None:
    """The tension-shaping half: the chain's beats march. After the first
member releases (beat 1), the successor is held while
`beat_count - last_release < min_gap_beats` (beats 2-3) and releases
the beat the gap opens (beat 4 — a three-beat spacing at gap 3)."""
    director = Director(
        pack=_arc_pack(tmp_path, gap=3), policy=EnabledPolicy(entropy_floor=10),
    )
    director._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=2, release_threshold=5,
        ),
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=3, release_threshold=1,
        ),
    ])
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert len(director.releases(projection, beat_tick=0)) == 1  # member 1
    director.next_beat()
    assert director.releases(projection, beat_tick=360) == []  # gap 1/3
    director.next_beat()
    assert director.releases(projection, beat_tick=720) == []  # gap 2/3
    director.next_beat()
    released = director.releases(projection, beat_tick=1080)  # gap open
    assert len(released) == 1 and released[0].actor == "npc_guard_02"


def test_future_members_count_toward_entropy(tmp_path: Path) -> None:
    """The buffer's meaning is unchanged by the chain: a fully-seeded
arc reads its whole weight. The successor (weight 25) alone holds the
clock in PEAK after the first member's explicit release — if future
members were excluded from entropy the world would read quiet (the
rest band), and the assert would fail. The first member releases
explicitly mid-PEAK — the D-005 ungated-explicit pin riding along."""
    director = Director(
        pack=_arc_pack(tmp_path, gap=2), policy=EnabledPolicy(entropy_floor=0),
    )
    director._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=5, release_threshold=5,
            trigger={"kind": "time", "tick": 0},
        ),
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=25, release_threshold=1,
        ),
    ])
    projection = initial_projection(PACK.entities)
    director.next_beat()
    released = director.releases(projection, beat_tick=0)
    assert len(released) == 1  # the explicit path, mid-PEAK (ungated)
    director.next_beat()
    assert director.releases(projection, beat_tick=360) == []  # never quiet
    assert director.pacing is not None
    assert director.pacing.state == "PEAK"  # the successor's 25 holds it
    director.next_beat()
    director.releases(projection, beat_tick=720)
    assert director.pacing.state == "PEAK"


def test_passed_instances_stop_counting_toward_entropy(
    tmp_path: Path,
) -> None:
    """The burn law's twin: a member whose turn came and went drops its
remaining instances from entropy. The counterfactual is arithmetic —
the second instance of the first member (weight 5) still counting
would read entropy 14 >= the floor 10 and the un-chained hook (weight
4, threshold 50) would never release; excluded, entropy reads 9 < 10
and the quiet path opens for it on beat 2 (the successor itself is
gap-held)."""
    director = Director(
        pack=_arc_pack(tmp_path, gap=3), policy=EnabledPolicy(entropy_floor=10),
    )
    first = _seeded_hook(
        tag="possible_document_check", target_npc="npc_guard_01",
        weight=5, release_threshold=5, trigger={"kind": "time", "tick": 0},
    )
    director._hooks.extend([  # type: ignore[attr-defined]
        first,
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=5, release_threshold=5,
        ),  # the spent instance — passed the moment the first releases
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=5, release_threshold=1,
        ),
        _seeded_hook(
            tag="guard_suspicious_of_pc", target_npc="npc_drunk_01",
            weight=4, release_threshold=50,
        ),  # un-chained: the quiet path's probe
    ])
    projection = initial_projection(PACK.entities)
    director.next_beat()
    assert len(director.releases(projection, beat_tick=0)) == 1  # member 1
    director.next_beat()
    # entropy 9 (5 successor + 4 probe; the spent instance excluded) <
    # 10 — the quiet path opens; the successor is gap-held, the probe
    # is not chained and releases (the lowest releasable candidate)
    released = director.releases(projection, beat_tick=360)
    assert len(released) == 1 and released[0].actor == "npc_drunk_01"


def test_one_play_per_arc_beat(tmp_path: Path) -> None:
    """A spent member's later instances never release: the cursor moved,
they are passed facts (the coerce one-secret-one-play twin). The
sequence pins exactly two releases — the first member's first
instance, then the successor after the gap — and nothing after the
chain completes (beat 5: the leftover instance would release if the
filter leaked; entropy reads 0, the quiet path is open, it does not)."""
    director = Director(
        pack=_arc_pack(tmp_path, gap=3), policy=EnabledPolicy(entropy_floor=10),
    )
    director._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=5, release_threshold=5, trigger={"kind": "time", "tick": 0},
        ),
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=5, release_threshold=5,
        ),
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=5, release_threshold=5,
        ),
    ])
    projection = initial_projection(PACK.entities)
    order: list[str] = []
    director.next_beat()
    order.extend(
        i.actor for i in director.releases(projection, beat_tick=0)
    )
    for tick in (360, 720, 1080, 1440, 1800):
        director.next_beat()
        order.extend(
            i.actor for i in director.releases(projection, beat_tick=tick)
        )
    assert order == ["npc_guard_01", "npc_guard_02"]


def test_the_climax_path_respects_the_chain(tmp_path: Path) -> None:
    """The boss gate composes with both chain laws: a climax-flagged
SUCCESSOR is held while its predecessor is unreleased (beat 1 — the
climax gate is open, entropy at the third layer, and nothing releases);
the predecessor's explicit trigger fires first (beat 2 — explicit
beats the boss path, and a non-climax release never marks
PEAK_CLIMAX); the successor then waits the gap INSIDE the peak (beat
3 — the clock is back in PEAK, the gate re-opens, the gap holds) and
releases when it opens (beat 4), marking the boss beat."""
    director = Director(
        pack=_arc_pack(tmp_path, gap=3), policy=EnabledPolicy(entropy_floor=5),
    )
    director._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=2, release_threshold=5,
            trigger={"kind": "time", "tick": 1},
        ),
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=80, release_threshold=1, climax=True,
        ),
    ])
    projection = initial_projection(PACK.entities)
    director.next_beat()
    # the climax gate is open (entropy 82 >= 75, PEAK held its minimum)
    # but the flagged successor is not the chain's current member
    assert director.releases(projection, beat_tick=0) == []
    director.next_beat()
    released = director.releases(projection, beat_tick=360)
    assert len(released) == 1 and released[0].actor == "npc_guard_01"
    assert director.pacing is not None
    assert director.pacing.state == "PEAK"  # not marked: not a boss release
    director.next_beat()
    assert director.releases(projection, beat_tick=720) == []  # gap 1/3
    director.next_beat()
    assert director.releases(projection, beat_tick=1080) == []  # gap 2/3
    director.next_beat()
    released = director.releases(projection, beat_tick=1440)
    assert len(released) == 1 and released[0].actor == "npc_guard_02"
    assert director.pacing.state == "PEAK_CLIMAX"  # the boss beat


def test_director_off_suppresses_the_chain(tmp_path: Path) -> None:
    """The T8 baseline holds under chaining: a disabled director never
releases — the chain never advances, no member ever spends its beat."""
    director = Director(pack=_arc_pack(tmp_path), policy=DisabledPolicy())
    director._hooks.extend([  # type: ignore[attr-defined]
        _seeded_hook(
            tag="possible_document_check", target_npc="npc_guard_01",
            weight=2, release_threshold=5,
            trigger={"kind": "time", "tick": 0},
        ),
        _seeded_hook(
            tag="possible_document_check_relief", target_npc="npc_guard_02",
            weight=3, release_threshold=1,
        ),
    ])
    projection = initial_projection(PACK.entities)
    for tick in (0, 360, 720, 1080):
        director.next_beat()
        assert director.releases(projection, beat_tick=tick) == []


# pack lint (the arc-1 chain contract)


def test_arc_lint_rejects_unknown_member_tag(tmp_path: Path) -> None:
    """A typo'd member is silent dead vocabulary — the chain would wait
forever on a tag that never seeds."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {
            "papers": {
                "members": ["possible_document_check", "possible_document"],
                "min_gap_beats": 2,
            }
        }

    with pytest.raises(PackError, match="must name a declared director.hooks tag"):
        _mutated_pack(tmp_path, mutate)


def test_arc_lint_rejects_a_one_member_arc(tmp_path: Path) -> None:
    """L1: a chain of one has no successor — the order law and the gap
law are both vacuous on it (dead vocabulary, refused at load)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {
            "papers": {
                "members": ["possible_document_check"],
                "min_gap_beats": 2,
            }
        }

    with pytest.raises(PackError, match="at least two tags"):
        _mutated_pack(tmp_path, mutate)


def test_arc_lint_rejects_a_doubled_member(tmp_path: Path) -> None:
    """A tag chained to itself has no order semantics — the successor
and the predecessor are the same release."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {
            "papers": {
                "members": [
                    "possible_document_check", "possible_document_check",
                ],
                "min_gap_beats": 2,
            }
        }

    with pytest.raises(PackError, match="members must be unique"):
        _mutated_pack(tmp_path, mutate)


def test_arc_lint_rejects_a_tag_in_two_arcs(tmp_path: Path) -> None:
    """Two chains claiming one tag have ambiguous order — which chain's
cursor governs its candidacy is a question load refuses to answer."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {
            "papers": {
                "members": [
                    "possible_document_check", "possible_document_check_relief",
                ],
                "min_gap_beats": 2,
            },
            "papers_again": {
                "members": [
                    "possible_document_check", "guard_suspicious_of_pc",
                ],
                "min_gap_beats": 2,
            },
        }

    with pytest.raises(PackError, match="already belongs to arc"):
        _mutated_pack(tmp_path, mutate)


def test_arc_lint_rejects_gap_below_the_budget(tmp_path: Path) -> None:
    """min_gap_beats 1 is the 1-per-beat budget's own law — declaring it
buys nothing (dead vocabulary, the empty-compound family)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {
            "papers": {
                "members": [
                    "possible_document_check", "possible_document_check_relief",
                ],
                "min_gap_beats": 1,
            }
        }

    with pytest.raises(PackError, match="min_gap_beats must be an integer >= 2"):
        _mutated_pack(tmp_path, mutate)


def test_arc_lint_rejects_non_integer_gap(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {
            "papers": {
                "members": [
                    "possible_document_check", "possible_document_check_relief",
                ],
                "min_gap_beats": "two",
            }
        }

    with pytest.raises(PackError, match="min_gap_beats must be an integer >= 2"):
        _mutated_pack(tmp_path, mutate)


def test_arc_lint_rejects_unknown_arc_key(tmp_path: Path) -> None:
    """A typo'd key is a shape error, never a silent ignore — `memebers`
would read as an unvalidated extra (the option-block precedent)."""
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {
            "papers": {
                "members": [
                    "possible_document_check", "possible_document_check_relief",
                ],
                "min_gap_beats": 2,
                "memebers": [],
            }
        }

    with pytest.raises(PackError, match="unknown arc keys"):
        _mutated_pack(tmp_path, mutate)


def test_arc_lint_rejects_non_string_notes(tmp_path: Path) -> None:
    def mutate(rules: dict[str, Any]) -> None:
        rules["director"]["arcs"] = {
            "papers": {
                "members": [
                    "possible_document_check", "possible_document_check_relief",
                ],
                "min_gap_beats": 2,
                "notes": 3,
            }
        }

    with pytest.raises(PackError, match="notes must be a string"):
        _mutated_pack(tmp_path, mutate)
