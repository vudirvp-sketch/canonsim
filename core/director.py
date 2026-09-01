"""The director (phase0 §4, MVP_SCOPE §11, D-005, DIRECTOR_SPEC): a
consequence planner that NEVER improvises. A hook seeded at event time
sits in a per-run buffer until its trigger fires (time / place /
threshold) or the stagnation detector releases the lowest-threshold
hook when narrative entropy drops below the pack's floor.

Phase 3 (DIR-1, the L4D peak/rest donor): the pacing clock — a
per-run four-state machine (RAMP / PEAK / REST / STAGNATION) over
narrative entropy, advanced once per beat. REST is the post-climax
breathing room the flat v0.1 detector lacked: the stagnation path
releases only OUTSIDE PEAK/REST, so the world is not re-injected the
beat after a climax. Explicit triggers never consult the clock —
causality is not pacing (D-005). A pack without `director.pacing`
runs the v0.1 minimal pair, byte-identically.

Phase 3 (DIR-3, iter-38 — the L4D2 three-intensity rule + the boss-beat
rule): layered thresholds — an optional third entropy layer
`director.pacing.climax_floor`, strictly above the peak floor (pack
lint), and the climax release path. A climax-flagged hook (pack data
`director.hooks[tag].climax`) releases at the END of a peak — the clock
in PEAK having held `min_peak_beats`, entropy at the third layer — and
never from the quiet path (a boss does not spawn because the world is
boring). The release marks the beat PEAK_CLIMAX (one beat — the boss
beat itself); the next transition is REST (boss beat + reset). The
pack's declaration is the gate (INV-3): a pack without `climax_floor`
runs the iter-36 two-layer clock, byte-identically, and a climax-flagged
hook without the layer is explicit-trigger-only.

Phase 3 (DIR-4, iter-39 — the L4D multi-channel family): the quiet
path decomposes per channel. `director.channels` (pack data) declares
named pacing dimensions — each its own entropy floor plus the
observable inputs it senses (the closed vocabulary {suspicion,
physical_threats}; the channel's own unreleased hook weights always
feed it). A hook opts in per hook (`director.hooks[tag].channel`):
the quiet gate asks the hook's OWN channel — a quiet social channel
can inject while the threat channel burns (the multi-channel win the
single global floor cannot express). The pacing clock stays global
(one drama arc over TOTAL entropy — PEAK/REST suppress every
channel); explicit triggers stay ungated (D-005); the budget stays 1
release per beat across all channels; the climax path ignores
channels (the boss gate reads total entropy). A pack without
`director.channels` runs the v0.1 global-floor quiet path,
byte-identically; a channelless hook keeps that global floor even in
a channels pack (the per-hook opt-in mirrors the climax flag — a tag
without the block is dormant vocabulary).

Releases ride the intent door (phase0 §4 "Objective broadcast", D-037):
a released hook produces an IntentData the loop enqueues through the
normal queue, validated by the same front door as a playscript step.
The director never moves actors, changes state, or bypasses the
Intent→Event front-door. Director-off = the buffer still seeds (D-005
hygiene), nothing releases (T8 A/B baseline — the world's emergent
chains come from urgencies + reactions + rotations, not director
injections).

Per-run scope (D-005): the buffer is per-run (folded from the log);
policies are pack data (constant across runs with the same pack). The
director never learns the player (Alien named negative — director
adaptation state is per-run, never persisted). The pacing clock is
derived state the same way: a deterministic fold of the per-beat
entropy sequence, itself a function of the log (INV-2 — same log, same
clock, same releases; it writes nothing).

Narrative entropy (P2e): sum of seeded-hook weights + global suspicion
+ visible physical threats — observable state only (L6, never
knowledge records, never PC internals). Replaces the flat
`release_after_ticks_without_visible_event` timer of the v0.1 draft.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Final, Protocol

from core.ids import sequence_id
from core.intent import IntentData

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.log import EventRecord
    from core.pack import Pack

__all__ = [
    "DISABLED",
    "CHANNEL_INPUTS",
    "ChannelConfig",
    "Director",
    "DirectorPolicy",
    "EnabledPolicy",
    "DisabledPolicy",
    "PacingClock",
    "PacingConfig",
    "SeededHook",
    "channel_entropies",
    "channels_from_rules",
    "entropy",
    "pacing_from_rules",
    "policy_from_rules",
]

HOOK_PREFIX: Final = "director"


@dataclass(frozen=True, slots=True)
class SeededHook:
    """One consequence seeded at event time (D-005). The event wrote a
    hook tag and the pack's `director.hooks` config declared what to do
    about it. A hook with no explicit trigger is stagnation-only — it
    releases only when entropy drops below the floor (the
    lowest-threshold one wins, phase0 §4) — UNLESS it carries the
    climax flag (DIR-3): a boss hook never releases from the quiet
    path; its door is the climax layer (or an explicit trigger).
    Immutable; the Director tracks release state via a separate index
    set, not by mutating the record (the frozen-ness documents INV-5:
    a seeded hook is a fact)."""

    tag: str
    seeded_by_event: str
    seeded_at_tick: int
    weight: int
    release_threshold: int
    target_npc: str
    intent_kind: str
    intent_target: str | None
    intent_fields: Mapping[str, Any]
    trigger: Mapping[str, Any] | None  # {"kind": "time"|"place"|"threshold", ...}
    climax: bool = False  # DIR-3: the boss-beat flag (pack data)
    channel: str | None = None  # DIR-4: the pacing dimension (pack data)


class DirectorPolicy(Protocol):
    """The release gate (phase0 §4 "Multi-channel policies"): the
    director asks the policy whether a release is permitted at this
    beat. The minimal pair (Enabled / Disabled) covers T8's A/B
    baseline. The quiet question split per release path at phase 3:
    `permit_climax` (DIR-3 — the boss fires at HIGH entropy where the
    stagnation path fires at LOW; one boolean cannot serve both
    honestly) and `permit_quiet` (DIR-4 — each channel owns its floor;
    the global floor cannot serve three pacing dimensions honestly).
    The pacing clock is Director-side state, not a policy (iter-36);
    the channel table likewise lives on the Director — the policy only
    answers."""

    def permit_release(
        self,
        explicit_trigger_fires: bool,
        current_entropy: int,
    ) -> bool: ...

    def permit_quiet(
        self, channel: ChannelConfig, channel_entropy: int
    ) -> bool: ...

    def permit_climax(self) -> bool: ...


@dataclass(frozen=True, slots=True)
class EnabledPolicy:
    """Default: explicit triggers always release (causal); stagnation
    releases the lowest-threshold hook when entropy < floor; the climax
    path is permitted whenever the pacing gates pass (the clock state
    and the layered threshold decided — the policy only switches the
    director on or off)."""

    entropy_floor: int

    def permit_release(
        self, explicit_trigger_fires: bool, current_entropy: int
    ) -> bool:
        if explicit_trigger_fires:
            return True
        return current_entropy < self.entropy_floor

    def permit_quiet(
        self, channel: ChannelConfig, channel_entropy: int
    ) -> bool:
        """DIR-4: the per-channel quiet question — the channel's entropy
        against the channel's own floor (each pacing dimension owns its
        quiet gate; one global floor cannot serve three honestly)."""
        return channel_entropy < channel.entropy_floor

    def permit_climax(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class DisabledPolicy:
    """T8 A/B baseline: no releases ever — the boss and every channel
    included. The buffer still seeds — D-005 hygiene holds (a
    complication from nowhere is still a bug); A/B measures the delta
    the director's releases make."""

    def permit_release(
        self, explicit_trigger_fires: bool, current_entropy: int
    ) -> bool:
        return False

    def permit_quiet(
        self, channel: ChannelConfig, channel_entropy: int
    ) -> bool:
        return False

    def permit_climax(self) -> bool:
        return False


DISABLED: Final = DisabledPolicy()


def policy_from_rules(rules: Mapping[str, Any], enabled: bool) -> DirectorPolicy:
    """The pack-configured policy (the single owner of the entropy-floor
    read — the loop and the CLI `directors on|off` toggle both come here)."""
    if not enabled:
        return DISABLED
    return EnabledPolicy(
        entropy_floor=int(rules["director"]["stagnation"]["entropy_floor"])
    )


# -- the release channels (DIR-4, phase 3; the L4D multi-channel family) ------


CHANNEL_INPUTS: Final = ("suspicion", "physical_threats")
"""The closed vocabulary of observable P2e terms a channel may bind
(`director.channels.<name>.inputs`): the entropy formula's two
world-sensing terms, decomposed per dimension. The channel's own
unreleased hook weights always feed it — that input is not listable."""


@dataclass(frozen=True, slots=True)
class ChannelConfig:
    """DIR-4 pack data (`director.channels.<name>`): one pacing
    dimension — the L4D family (Horde / S.I. / Music; the names are the
    pack's own — this pack instantiates threat / social / ambient).
    `entropy_floor` is the channel's quiet gate (the stagnation
    detector's per-channel floor); `inputs` binds the observable terms
    the channel senses (a subset of CHANNEL_INPUTS). A channel never
    senses another channel's hooks — the split is the point: a quiet
    social channel can inject while the threat channel burns."""

    entropy_floor: int
    inputs: frozenset[str]


def channels_from_rules(
    rules: Mapping[str, Any],
) -> Mapping[str, ChannelConfig] | None:
    """The pack's channel declarations (`director.channels`), beside
    `pacing_from_rules` (the single channels read). None when the pack
    declares no channels — the v0.1 global-floor quiet path,
    byte-identical (the pack's own declaration is the gate, INV-3).
    The channel NAMES are free-form pack data; only the input
    vocabulary is closed (CHANNEL_INPUTS)."""
    channels = rules.get("director", {}).get("channels")
    if channels is None:
        return None
    return {
        str(name): ChannelConfig(
            entropy_floor=int(spec["entropy_floor"]),
            inputs=frozenset(spec.get("inputs", ())),
        )
        for name, spec in channels.items()
    }


# -- the pacing clock (DIR-1, phase 3; the L4D peak/rest donor) ----------------


@dataclass(frozen=True, slots=True)
class PacingConfig:
    """DIR-1 pack data (`director.pacing` + the stagnation floor): the
    pacing clock's thresholds and minimum durations. `peak_floor` sits
    strictly above the stagnation `entropy_floor` (pack lint) — the
    band between them is normal tension (RAMP); below the floor the
    clock reads STAGNATION (the detector's own band). `min_peak_beats`
    / `min_rest_beats` are the L4D `PeakDuration` / `RestMinDuration`
    anti-flap floors (a spike is a peak, a peak is followed by a rest —
    neither may flap on a one-beat entropy dip).

    `climax_floor` (DIR-3, iter-38) is the optional third threshold
    layer — the L4D2 three-intensity rule (a Boss threshold gates a
    Peak threshold gates a Calm threshold). It sits strictly above
    `peak_floor` (pack lint); `None` means the pack declares two layers
    and runs the iter-36 clock, byte-identically."""

    entropy_floor: int
    peak_floor: int
    min_peak_beats: int
    min_rest_beats: int
    climax_floor: int | None = None


@dataclass(frozen=True, slots=True)
class PacingClock:
    """The per-run pacing state over narrative entropy (DIR-1; the L4D
    `TimeSincePeak` / `TimeSinceRest` two-clock shape IS this state
    machine — REST's `beats_in_state` is time-since-peak, PEAK's is
    time-since-rest-ended). `beats_in_state` counts the beats held
    INCLUDING the entering beat. Functional by design: `transition`
    returns a new clock, the Director holds the current one — a
    deterministic fold of the per-beat entropy sequence (INV-2).

    States: RAMP (normal tension) · PEAK (entropy at or above the peak
    floor — the world is loud, the director does not add) · REST
    (post-peak breathing room, holds `min_rest_beats`) · STAGNATION
    (entropy below the stagnation floor — the quiet the detector
    exists to break). Only PEAK and REST suppress releases; the
    RAMP/STAGNATION split is the observable band name (the policy's
    floor remains the release authority — one owner per law).

    PEAK_CLIMAX (DIR-3) is the boss beat itself — one beat, entered
    ONLY by a climax release (never by entropy alone: the state marks
    the placement of a high-severity hook, not an intensity band),
    exited to REST unconditionally (boss beat + reset; a still-loud
    world breaks the rest on the transition after, per the re-spike
    law)."""

    state: str = "RAMP"
    beats_in_state: int = 0

    def transition(self, entropy_value: int, config: PacingConfig) -> "PacingClock":
        """One beat's deterministic transition. PEAK holds its minimum
        even through an entropy dip (hysteresis); REST is broken early
        only by the world re-spiking (entropy back at the peak floor) —
        the director never ends its own rest with a release. The boss
        beat (PEAK_CLIMAX) ends the peak: the reset is the rest."""
        if self.state == "PEAK_CLIMAX":
            return PacingClock("REST", 1)  # boss beat + reset: breathe
        if self.state == "PEAK":
            if (
                entropy_value < config.peak_floor
                and self.beats_in_state >= config.min_peak_beats
            ):
                return PacingClock("REST", 1)  # the peak is over: breathe
            return PacingClock("PEAK", self.beats_in_state + 1)
        if self.state == "REST":
            if entropy_value >= config.peak_floor:
                return PacingClock("PEAK", 1)  # the world re-spiked: rest over
            if self.beats_in_state >= config.min_rest_beats:
                return _quiet_band(entropy_value, config)
            return PacingClock("REST", self.beats_in_state + 1)
        # RAMP / STAGNATION — no minimum (the flat band; the policy's
        # floor, not the clock, is the release authority here)
        if entropy_value >= config.peak_floor:
            return PacingClock("PEAK", 1)
        return _quiet_band(entropy_value, config)


def _quiet_band(entropy_value: int, config: PacingConfig) -> PacingClock:
    """The quiet-band split: below the stagnation floor the clock reads
    STAGNATION, at or above it RAMP. Observable naming only — both
    states leave the release decision to the policy."""
    if entropy_value < config.entropy_floor:
        return PacingClock("STAGNATION", 1)
    return PacingClock("RAMP", 1)


def pacing_from_rules(rules: Mapping[str, Any]) -> PacingConfig | None:
    """The pack's pacing declaration (`director.pacing`), beside
    `policy_from_rules` (the single pacing read). None when the pack
    declares no pacing — the v0.1 minimal pair, release behavior
    byte-identical (the pack's own declaration is the gate, INV-3).
    A pacing block without `climax_floor` declares the two-layer
    iter-36 clock (climax_floor None — the climax path is off)."""
    pacing = rules.get("director", {}).get("pacing")
    if pacing is None:
        return None
    stagnation = rules["director"]["stagnation"]
    return PacingConfig(
        entropy_floor=int(stagnation["entropy_floor"]),
        peak_floor=int(pacing["peak_floor"]),
        min_peak_beats=int(pacing["min_peak_beats"]),
        min_rest_beats=int(pacing["min_rest_beats"]),
        climax_floor=(
            int(pacing["climax_floor"]) if "climax_floor" in pacing else None
        ),
    )


# -- entropy (P2e: observable state only, never knowledge records) ------------


def _threat_states(rules: Mapping[str, Mapping[str, Any]]) -> frozenset[str]:
    """The active-state values of every declared transition layer — the
    value a `<layer>.<spot>` prop holds while the layer spreads (pack
    data, D-057; the director never hardcodes a layer vocabulary)."""
    return frozenset(
        str(config["spot_state"])
        for config in rules.get("transitions", {}).values()
        if isinstance(config, Mapping) and "spot_state" in config
    )


def _visible_physical_threats(
    projection: Mapping[str, Mapping[str, Any]], states: frozenset[str]
) -> int:
    """Count of spreading transition spots across all locations (one per
    `<layer>.<spot>` prop holding a layer's active-state value)."""
    threats = 0
    for props in projection.values():
        for prop, value in props.items():
            if "." not in prop:
                continue
            if value in states:
                threats += 1
    return threats


def _global_suspicion(projection: Mapping[str, Mapping[str, Any]]) -> int:
    """Sum of the `relations.suspicion` axis across NPCs that have one
    (the player and ambient groups lack it — by convention, never
    raised). The aggregate tension the director senses."""
    total = 0
    for props in projection.values():
        value = props.get("relations.suspicion")
        if isinstance(value, int) and not isinstance(value, bool):
            total += value
    return total


def entropy(
    projection: Mapping[str, Mapping[str, Any]],
    unreleased: Iterator[SeededHook],
    rules: Mapping[str, Mapping[str, Any]],
) -> int:
    """P2e: sum of seeded-hook weights + global suspicion + visible
    physical threats — observable state only (L6). Computed from the
    projection, the buffer, and the pack's transition declarations,
    never from knowledge records or PC internals. The stagnation
    detector releases when this drops below the pack's floor."""
    weights = sum(hook.weight for hook in unreleased)
    return (
        weights
        + _global_suspicion(projection)
        + _visible_physical_threats(projection, _threat_states(rules))
    )


def channel_entropies(
    channels: Mapping[str, ChannelConfig],
    projection: Mapping[str, Mapping[str, Any]],
    unreleased: Iterator[SeededHook],
    rules: Mapping[str, Mapping[str, Any]],
) -> dict[str, int]:
    """DIR-4: the per-channel entropy map. Each declared channel senses
    its OWN unreleased hook weights (always) plus the inputs it binds
    (CHANNEL_INPUTS — the P2e world-sensing terms, decomposed per
    dimension). Hooks in no declared channel count toward the TOTAL
    only (the pacing clock's input, unchanged). Deterministic: the
    channels iterate sorted(), the buffer in construction order
    (INV-2)."""
    suspicion = _global_suspicion(projection)
    threats = _visible_physical_threats(projection, _threat_states(rules))
    totals = {name: 0 for name in sorted(channels)}
    for hook in unreleased:
        if hook.channel in totals:
            totals[hook.channel] += hook.weight
    for name in sorted(channels):
        inputs = channels[name].inputs
        if "suspicion" in inputs:
            totals[name] += suspicion
        if "physical_threats" in inputs:
            totals[name] += threats
    return totals


# -- triggers (time / place / threshold — causal, not stagnation) -------------


def _trigger_fires(
    trigger: Mapping[str, Any] | None,
    projection: Mapping[str, Mapping[str, Any]],
    beat_tick: int,
) -> bool:
    """A hook's explicit trigger (time / place / threshold). A hook with
    `trigger is None` is stagnation-only — its trigger never fires on
    its own; it relies on the stagnation detector. Otherwise:
    - `time`: fires when `beat_tick >= trigger.tick`
    - `place`: fires when the `target_npc` is at `trigger.location`
    - `threshold`: fires when the target_npc's relations axis meets
      the comparison (`at_least` / `at_most`)
    """
    if trigger is None:
        return False
    kind = trigger["kind"]
    if kind == "time":
        return beat_tick >= int(trigger["tick"])
    if kind == "place":
        npc = trigger["target_npc"]
        return projection.get(npc, {}).get("position") == trigger["location"]
    if kind == "threshold":
        npc = trigger["target_npc"]
        prop = f"relations.{trigger['axis']}"
        value = projection.get(npc, {}).get(prop)
        if not isinstance(value, int) or isinstance(value, bool):
            return False
        if trigger["comparator"] == "at_least":
            return value >= int(trigger["value"])
        if trigger["comparator"] == "at_most":
            return value <= int(trigger["value"])
        raise ValueError(f"unknown threshold comparator {trigger['comparator']!r}")
    raise ValueError(f"unknown trigger kind {kind!r}")


# -- the director -----------------------------------------------------------


@dataclass
class Director:
    """The per-run consequence planner. Holds the seeded-hook buffer and
    the release budget; the loop calls `seed` at commit time and
    `releases` at each beat tick. A release produces an IntentData the
    loop enqueues — the director never writes canon itself (D-037).
    Since iter-36 it also holds the per-run pacing clock (DIR-1) when
    the pack declares one; since iter-39 the channel table (DIR-4) —
    pack data, constant across runs, like the policies."""

    pack: "Pack"
    policy: DirectorPolicy
    beat_count: int = 0
    _hooks: list[SeededHook] = field(default_factory=list)
    _released: set[int] = field(default_factory=set)
    _release_seq: int = 0
    _npc_last_release_beat: dict[str, int] = field(default_factory=dict)
    _pacing_config: PacingConfig | None = field(default=None, init=False, repr=False)
    _pacing: PacingClock | None = field(default=None, init=False, repr=False)
    _pacing_beat: int = field(default=-1, init=False, repr=False)
    _channels: Mapping[str, ChannelConfig] | None = field(
        default=None, init=False, repr=False
    )

    def __post_init__(self) -> None:
        self._pacing_config = pacing_from_rules(self.pack.rules)
        if self._pacing_config is not None:
            self._pacing = PacingClock()
        self._channels = channels_from_rules(self.pack.rules)

    @property
    def hooks(self) -> tuple[SeededHook, ...]:
        return tuple(self._hooks)

    @property
    def pacing(self) -> PacingClock | None:
        """The per-run pacing clock (None when the pack declares no
        pacing — the v0.1 minimal pair)."""
        return self._pacing

    def next_beat(self) -> int:
        """Advance the beat counter; returns the new beat index."""
        self.beat_count += 1
        return self.beat_count

    def seed(self, event: "EventRecord") -> None:
        """Absorb an event's hooks into the buffer (D-005: a complication
        is seeded at event time, never invented later). Tags the pack
        does not declare are silently ignored — a hook without a
        release intent is just a tag, not a deferred consequence."""
        config = self.pack.rules.get("director", {})
        hook_specs = config.get("hooks", {})
        for tag in event.hooks:
            spec = hook_specs.get(tag)
            if spec is None:
                continue
            self._hooks.append(
                SeededHook(
                    tag=tag,
                    seeded_by_event=event.id,
                    seeded_at_tick=event.t,
                    weight=int(spec["weight"]),
                    release_threshold=int(spec["release_threshold"]),
                    target_npc=spec["target_npc"],
                    intent_kind=spec["intent"]["kind"],
                    intent_target=spec["intent"].get("target"),
                    intent_fields=dict(spec["intent"].get("fields", {})),
                    trigger=spec.get("trigger"),
                    climax=bool(spec.get("climax", False)),
                    channel=spec.get("channel"),
                )
            )

    def releases(
        self,
        projection: "Projection",
        beat_tick: int,
    ) -> list[IntentData]:
        """One beat's worth of releases (phase0 §4): explicit triggers
        fire causally first; the climax path (DIR-3) checks the boss
        gate; then the quiet path — per channel since iter-39 (DIR-4):
        each hook's own channel floor gates it when the pack declares
        channels and the hook carries a channel; the v0.1 global floor
        otherwise. Budget: 1 release per beat (the director never
        spams, across ALL channels — the pick stays the global
        lowest-threshold tiebreak). A rejected director Intent consumes
        the budget (per-NPC cooldown follows — recorded, the front door
        does the rejecting). Dead actors (no projection entry /
        `crime_status == caught`) are never targeted.

        Reads observable state only (L6): the projection and the
        seeded-hook buffer — never knowledge records, never PC
        internals (the entropy law, phases.md/DIRECTOR_SPEC §5). The
        pacing clock (DIR-1) advances once per beat BEFORE the gates
        read it; PEAK/REST suppress the quiet path — every channel
        (the clock reads TOTAL entropy: one drama arc), explicit
        triggers stay ungated (D-005 — causality is not pacing).
        """
        unreleased = list(self._unreleased())
        # Entropy is invariant across this call — nothing mutates the
        # buffer, the release set, or the projection before an immediate
        # return — so it is computed once and reused for every policy
        # check (the eager per-hook recomputation was pure waste under a
        # rejecting policy: k+1 identical evaluations per beat). Computed
        # even on an empty buffer: the pacing clock models the world's
        # drama (a burning room is a PEAK with the buffer drained), and
        # entropy is its only input.
        current_entropy = entropy(
            projection, iter(h for _, h in unreleased), self.pack.rules
        )
        self._advance_pacing(current_entropy)
        if not unreleased:
            return []
        # 1) explicit triggers — causal, fire regardless of entropy
        for idx, hook in unreleased:
            if not _trigger_fires(hook.trigger, projection, beat_tick):
                continue
            if self._on_cooldown(hook.target_npc):
                continue
            if not self._target_alive(projection, hook.target_npc):
                continue
            if not self.policy.permit_release(
                explicit_trigger_fires=True,
                current_entropy=current_entropy,
            ):
                continue
            self._mark_released(idx, hook.target_npc)
            return [self._intent(hook)]
        # 2) climax release (DIR-3, the L4D2 three-intensity rule + the
        # boss-beat rule): a climax-flagged hook releases at the END of a
        # peak — the clock in PEAK having held `min_peak_beats` (the
        # placement law: boss beats end peaks, never start them), entropy
        # at the third layer (`climax_floor`, strictly above the peak
        # floor — pack lint). The release marks the beat PEAK_CLIMAX (one
        # beat); the next transition is REST — the post-climax breathing
        # room the clock already defines. The pack's declaration is the
        # gate (INV-3): no `climax_floor`, no climax path — and a
        # climax-flagged hook never falls through to the quiet path.
        if self._climax_gate(current_entropy):
            candidates = [
                (idx, hook) for idx, hook in unreleased
                if hook.climax
                and not self._on_cooldown(hook.target_npc)
                and self._target_alive(projection, hook.target_npc)
            ]
            if candidates:
                candidates.sort(
                    key=lambda ih: (ih[1].release_threshold, ih[1].seeded_at_tick)
                )
                idx, hook = candidates[0]
                self._mark_released(idx, hook.target_npc)
                assert self._pacing is not None  # the gate passed: pacing exists
                self._pacing = PacingClock("PEAK_CLIMAX", 1)  # the boss beat
                return [self._intent(hook)]
        # 3) the quiet path (the stagnation family). DIR-4 (iter-39 —
        # the L4D multi-channel family): the quiet gate is per hook. A
        # hook carrying a channel the pack declares asks its OWN
        # channel's floor against that channel's entropy — a quiet
        # channel can inject while another burns (the multi-channel win
        # the single global floor cannot express); every other hook
        # keeps the v0.1 global-floor question (the per-hook opt-in
        # mirrors the climax flag: a tag without the block is dormant
        # vocabulary). The clock gate stays global (PEAK/REST suppress
        # every channel); the pick stays the global lowest-threshold
        # tiebreak — the budget is one release per beat, all channels.
        global_quiet = self.policy.permit_release(
            explicit_trigger_fires=False, current_entropy=current_entropy
        )
        if self._channels is None and not global_quiet:
            return []
        if self._pacing is not None and self._pacing.state not in (
            "RAMP", "STAGNATION"
        ):
            return []
        per_channel = (
            channel_entropies(
                self._channels, projection,
                iter(hook for _, hook in unreleased), self.pack.rules,
            )
            if self._channels is not None
            else None
        )
        candidates = [
            (idx, hook) for idx, hook in unreleased
            if not hook.climax  # the boss never spawns because the world is boring
            and not self._on_cooldown(hook.target_npc)
            and self._target_alive(projection, hook.target_npc)
            and self._quiet_gate(hook, per_channel, global_quiet)
        ]
        if not candidates:
            return []
        # lowest release_threshold wins; ties break by seeding order
        # (oldest first — far hooks deserve priority, MVP_SCOPE §5)
        candidates.sort(key=lambda ih: (ih[1].release_threshold, ih[1].seeded_at_tick))
        idx, hook = candidates[0]
        self._mark_released(idx, hook.target_npc)
        return [self._intent(hook)]

    # -- helpers (private) ---------------------------------------------------

    def _quiet_gate(
        self,
        hook: SeededHook,
        per_channel: Mapping[str, int] | None,
        global_quiet: bool,
    ) -> bool:
        """The per-hook quiet gate (DIR-4): the hook's own channel floor
        when it carries a channel the pack declares; the v0.1 global
        answer otherwise (channelless, the tag names no declared
        channel — dormant vocabulary, the climax-flag-without-layer
        law — or the pack declares no channels). The global question is
        asked once in `releases`, never per hook."""
        if (
            per_channel is not None
            and hook.channel is not None
            and hook.channel in per_channel
        ):
            assert self._channels is not None  # per_channel set: channels declared
            return self.policy.permit_quiet(
                self._channels[hook.channel], per_channel[hook.channel]
            )
        return global_quiet

    def _climax_gate(self, current_entropy: int) -> bool:
        """The layered-threshold release gate (DIR-3): the pack declares
        the third layer AND the clock is at a peak's end (PEAK having
        held its minimum) AND entropy sits at the climax layer AND the
        policy permits the boss path. Note the clock's PEAK_CLIMAX
        state does not re-open this gate (state != PEAK) — no double
        boss; a PEAK entry beat below `min_peak_beats` is the peak's
        start, not its end (the L4D placement law)."""
        if self._pacing_config is None or self._pacing is None:
            return False
        if self._pacing_config.climax_floor is None:
            return False
        if self._pacing.state != "PEAK":
            return False
        if self._pacing.beats_in_state < self._pacing_config.min_peak_beats:
            return False
        if current_entropy < self._pacing_config.climax_floor:
            return False
        return self.policy.permit_climax()

    def _advance_pacing(self, current_entropy: int) -> None:
        """One beat's clock transition — guarded so a repeated
        `releases()` call inside one beat never double-advances (the
        loop calls once per beat; unit tests probe repeatedly)."""
        if self._pacing is None or self._pacing_config is None:
            return
        if self._pacing_beat == self.beat_count:
            return
        self._pacing_beat = self.beat_count
        self._pacing = self._pacing.transition(current_entropy, self._pacing_config)

    def _unreleased(self) -> Iterator[tuple[int, SeededHook]]:
        for idx, hook in enumerate(self._hooks):
            if idx not in self._released:
                yield idx, hook

    def _mark_released(self, idx: int, npc: str) -> None:
        self._released.add(idx)
        self._npc_last_release_beat[npc] = self.beat_count

    def _on_cooldown(self, npc: str) -> bool:
        """Per-NPC cooldown after a release (the MinGapBetweenEncounters
        analogue). The pack declares the cooldown length in beats."""
        last = self._npc_last_release_beat.get(npc)
        if last is None:
            return False
        cooldown = int(self.pack.rules["director"]["stagnation"].get(
            "per_npc_cooldown_beats", 1
        ))
        return self.beat_count - last < cooldown

    @staticmethod
    def _target_alive(projection: "Projection", npc: str) -> bool:
        """The entropy sensor stops targeting dead actors: an NPC removed
        from the projection or marked caught is never targeted again."""
        if npc not in projection:
            return False
        return projection[npc].get("crime_status") != "caught"

    def _intent(self, hook: SeededHook) -> IntentData:
        """Build the IntentData the loop will enqueue (the director never
        writes canon — it broadcasts an objective through the door)."""
        intent_id = sequence_id(HOOK_PREFIX, self._release_seq)
        self._release_seq += 1
        return IntentData(
            id=intent_id,
            kind=hook.intent_kind,
            actor=hook.target_npc,
            target=hook.intent_target,
            fields=hook.intent_fields,
            based_on_event_seq=0,  # the loop stamps the current count at enqueue
        )
