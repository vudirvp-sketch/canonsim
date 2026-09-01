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

Phase 3 (drama-1, iter-40 — the Paradox event grammar's predicate +
weight layer; phases.md §3 owns the design): triggers are now JSON
predicate specs over the projection (`core/predicates.py` owns the
grammar — the three v0.1 leaf kinds plus compound `all`/`any`/`not`
forms, an implicit-AND list root, the generalized `prop` leaf). The
hook weight gains the `weight_multiplier` shape (base +
modifiers{add|factor, when} — context-sensitive tension: the entropy
sensor reads the EFFECTIVE weight per beat, a pure function of the
projection). `first_time_only` (the Wesnoth fire-only-once law) is a
release policy: once any instance of the tag releases, the tag burns
for the run — burned instances stay facts in the buffer but stop
counting toward entropy (tension that can never discharge is noise,
not tension). A pack with flat int weights and no first_time_only
runs the v0.1 shapes, byte-identically (the pack's own declaration is
the gate, INV-3).

Phase 3 (drama-2, iter-41 — the Paradox event grammar's option layer;
phases.md §3 owns the design): a hook may declare `options` — each an
availability gate (a drama-1 predicate spec) + an ai_chance-style weight
(the weight_multiplier shape) + an intent payload override. At release
the director CHOOSES: gated-off options are unavailable, zero effective
weights are never picked (the Stellaris factor-0 zero-out), the heaviest
wins, ties break by declaration order — a PURE function of (pack data,
projection, beat_tick), no RNG (every director decision stays RNG-free;
the cross-run variety the donor's weighted draw provides comes from
world state — the modifiers read the projection). When every option is
closed the hook cannot release that beat: nothing hits the door, no
budget is consumed — the hook waits for a world where an option opens.
The chosen option's payload overrides the base whole-key (Paradox
options are complete alternative effect branches, not patches). A hook
without options runs the v0.1 release path byte-identically.

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
from core.predicates import evaluate

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
    "OptionSpec",
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
    a seeded hook is a fact).

    `weight` is the BASE tension (the v0.1 flat int; the drama-1
    `weight_multiplier` pack shape resolves to base + modifiers at
    seed time). `weight_modifiers` are the drama-1 multiplier tail:
    each `{add: N | factor: N, when: <predicate>}` applies in
    declaration order when its predicate passes — the entropy sensor
    reads the EFFECTIVE weight (`_resolve_weight`), never the bare
    base. `first_time_only` burns the tag after its first release
    (the remaining instances stay facts but never release and never
    count toward entropy again)."""

    tag: str
    seeded_by_event: str
    seeded_at_tick: int
    weight: int
    release_threshold: int
    target_npc: str
    intent_kind: str
    intent_target: str | None
    intent_fields: Mapping[str, Any]
    trigger: Mapping[str, Any] | None  # a drama-1 predicate spec (core/predicates.py)
    climax: bool = False  # DIR-3: the boss-beat flag (pack data)
    channel: str | None = None  # DIR-4: the pacing dimension (pack data)
    weight_modifiers: tuple[Mapping[str, Any], ...] = ()  # drama-1: the multiplier tail
    first_time_only: bool = False  # drama-1: the Wesnoth fire-only-once release policy
    options: tuple["OptionSpec", ...] = ()  # drama-2: the option layer (see OptionSpec)


@dataclass(frozen=True, slots=True)
class OptionSpec:
    """One declared option of a hook's option layer (drama-2 — the
    Paradox `option` block adapted: an availability gate + an
    ai_chance-style weight + a payload override). Frozen pack data
    flattened at seed time; `_choose_option` computes the pick per
    release — the buffer never stores a choice (L3: a stored pick would
    be a projection inside the buffer).

    `trigger` is the availability gate (a drama-1 predicate spec; None =
    always available). `weight`/`weight_modifiers` are the ai_chance
    shape (a flat base + the modifier tail; an absent pack weight is
    base 1, the donor's default; a zero EFFECTIVE weight is never
    picked — the Stellaris factor-0 zero-out). `intent` is the payload
    override block `{kind?, target?, fields?}`: each declared key
    wholly replaces the hook's base payload key (Paradox options are
    complete alternative effect branches, not patches); None inherits
    the base payload wholly."""

    trigger: Mapping[str, Any] | None
    weight: int
    weight_modifiers: tuple[Mapping[str, Any], ...]
    intent: Mapping[str, Any] | None


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
    beat_tick: int,
) -> int:
    """P2e: sum of seeded-hook EFFECTIVE weights + global suspicion +
    visible physical threats — observable state only (L6). Computed
    from the projection, the buffer, the pack's transition declarations,
    and the beat tick (a drama-1 modifier's `when` predicate may read
    the clock), never from knowledge records or PC internals. The
    stagnation detector releases when this drops below the pack's
    floor."""
    weights = sum(_resolve_weight(hook, projection, beat_tick) for hook in unreleased)
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
    beat_tick: int,
) -> dict[str, int]:
    """DIR-4: the per-channel entropy map. Each declared channel senses
    its OWN unreleased hook weights (always — at their drama-1 effective
    values) plus the inputs it binds (CHANNEL_INPUTS — the P2e
    world-sensing terms, decomposed per dimension). Hooks in no declared
    channel count toward the TOTAL only (the pacing clock's input,
    unchanged). Deterministic: the channels iterate sorted(), the buffer
    in construction order (INV-2)."""
    suspicion = _global_suspicion(projection)
    threats = _visible_physical_threats(projection, _threat_states(rules))
    totals = {name: 0 for name in sorted(channels)}
    for hook in unreleased:
        if hook.channel in totals:
            totals[hook.channel] += _resolve_weight(hook, projection, beat_tick)
    for name in sorted(channels):
        inputs = channels[name].inputs
        if "suspicion" in inputs:
            totals[name] += suspicion
        if "physical_threats" in inputs:
            totals[name] += threats
    return totals


def _resolve_weight(
    hook: SeededHook,
    projection: Mapping[str, Mapping[str, Any]],
    beat_tick: int,
) -> int:
    """The hook's EFFECTIVE tension (drama-1): the base weight, then
    each modifier in declaration order — `{add: N}` adds, `{factor: N}`
    multiplies and truncates toward zero (deterministic; weights are
    non-negative by lint so truncation is floor). Only passing
    modifiers apply; a factor of 0 legally zeroes the weight (the
    Stellaris zero-out shape — a hook may go quiet without seeding a
    new fact). Pure (INV-2): same hook + same projection + same tick =
    the same number, in any process."""
    return _effective_weight(
        hook.weight, hook.weight_modifiers, projection, beat_tick
    )


def _effective_weight(
    weight: int,
    modifiers: tuple[Mapping[str, Any], ...],
    projection: Mapping[str, Mapping[str, Any]],
    beat_tick: int,
) -> int:
    """The shared effective-tension fold (drama-1's `_resolve_weight`
    body, extracted for drama-2's option weights): base, then each
    modifier in declaration order when its `when` predicate passes —
    `add` sums, `factor` multiplies and truncates toward zero; a factor
    of 0 legally zeroes. Pure (INV-2)."""
    for modifier in modifiers:
        if not evaluate(modifier["when"], projection, beat_tick):
            continue
        if "add" in modifier:
            weight += int(modifier["add"])
        else:
            weight = int(weight * float(modifier["factor"]))
    return weight


# -- the option layer (drama-2, phase 3; phases.md §3 — the Paradox  ----------
# -- option mechanics adapted) ------------------------------------------------


_BASE_OPTION: Final = OptionSpec(
    trigger=None, weight=1, weight_modifiers=(), intent=None
)
"""The implicit option every option-less hook carries: the base
payload, always pickable. `_choose_option` answers this for a hook
with no declared options — never None — so the v0.1 release path is
byte-identical (the option layer is pure addition, INV-3's
declaration-is-the-gate law)."""


def _choose_option(
    hook: SeededHook,
    projection: Mapping[str, Mapping[str, Any]],
    beat_tick: int,
) -> OptionSpec | None:
    """The option whose payload a release of `hook` carries (drama-2 —
    the Paradox option mechanics adapted: availability gates +
    ai_chance-style weighting, a PURE pick). None means the hook cannot
    release this beat: every declared option is gated off or zeroed
    out — the deferred-release law (the hook waits for a world where an
    option opens; nothing hits the door, no budget is consumed).

    The pick: an option's availability gate (`trigger`, a drama-1
    predicate spec) must pass; a zero EFFECTIVE weight is never picked
    (the Stellaris factor-0 zero-out); the heaviest effective weight
    wins, ties break by declaration order (first declared). No RNG —
    the choice is a pure function of (pack data, projection,
    beat_tick): every director decision stays RNG-free (the release
    pick, the threshold tiebreak), and the cross-run variety the
    donor's weighted DRAW provides comes here from world state (the
    modifiers read the projection — different runs, different
    winners)."""
    if not hook.options:
        return _BASE_OPTION
    best: OptionSpec | None = None
    best_weight = 0
    for option in hook.options:  # declaration order (INV-2)
        if option.trigger is not None and not evaluate(
            option.trigger, projection, beat_tick
        ):
            continue  # the availability gate is closed
        weight = _effective_weight(
            option.weight, option.weight_modifiers, projection, beat_tick
        )
        if weight <= 0:
            continue  # zeroed out — never picked
        if weight > best_weight:  # strict: ties keep the earlier declaration
            best = option
            best_weight = weight
    return best


def _option_specs(raw: Any) -> tuple[OptionSpec, ...]:
    """Flatten the pack's option blocks (drama-2) into buffer data: each
    weight resolves via `_weight_spec` (flat int = base, no tail; the
    multiplier object flattens to base + modifier list; an ABSENT
    weight is base 1, the ai_chance default), the availability gate and
    the payload override block pass through as linted data. The buffer
    stores data; `_choose_option` computes the pick per release, never
    stored (L3 — a stored choice would be a projection inside the
    buffer)."""
    if raw is None:
        return ()
    specs: list[OptionSpec] = []
    for option in raw:
        base, modifiers = _weight_spec(option.get("weight", 1))
        specs.append(
            OptionSpec(
                trigger=option.get("trigger"),
                weight=base,
                weight_modifiers=modifiers,
                intent=option.get("intent"),
            )
        )
    return tuple(specs)


# -- triggers (time / place / threshold — causal, not stagnation) -------------


def _trigger_fires(
    trigger: Mapping[str, Any] | None,
    projection: Mapping[str, Mapping[str, Any]],
    beat_tick: int,
) -> bool:
    """A hook's explicit trigger. A hook with `trigger is None` is
    stagnation-only — its trigger never fires on its own; it relies on
    the stagnation detector. Otherwise the spec is a drama-1 predicate
    (core/predicates.py owns the grammar: the three v0.1 leaf kinds —
    time / place / threshold — evaluate byte-identically to the pre-
    drama-1 shapes, and compound `all`/`any`/`not` forms are legal pack
    data since this iteration).
    """
    return trigger is not None and evaluate(trigger, projection, beat_tick)


def _weight_spec(spec: Any) -> tuple[int, tuple[Mapping[str, Any], ...]]:
    """Resolve the pack's hook weight (drama-1): a flat non-negative
    int is the v0.1 form (base, no tail); the multiplier object
    `{base, modifiers}` flattens to (base, tuple(modifiers)) — the
    buffer stores the data, `_resolve_weight` computes the effective
    value per evaluation (a stored effective weight would be a
    projection inside the buffer — L3's drift hazard). Pack lint owns
    the shape validation; this resolver only trusts what the lint
    passed."""
    if isinstance(spec, int) and not isinstance(spec, bool):
        return spec, ()
    return int(spec["base"]), tuple(spec.get("modifiers", ()))


# -- the director -----------------------------------------------------------


@dataclass
class Director:
    """The per-run consequence planner. Holds the seeded-hook buffer and
    the release budget; the loop calls `seed` at commit time and
    `releases` at each beat tick. A release produces an IntentData the
    loop enqueues — the director never writes canon itself (D-037).
    Since iter-36 it also holds the per-run pacing clock (DIR-1) when
    the pack declares one; since iter-39 the channel table (DIR-4) —
    pack data, constant across runs, like the policies. Since iter-40
    it holds the drama-1 burn set (`first_time_only` tags whose one
    release already happened — per-run, folded state like the buffer).
    Since iter-41 the option layer rides the release path: every
    release resolves its option choice first (`_choose_option` — pure,
    never stored)."""

    pack: "Pack"
    policy: DirectorPolicy
    beat_count: int = 0
    _hooks: list[SeededHook] = field(default_factory=list)
    _released: set[int] = field(default_factory=set)
    _burned_tags: set[str] = field(default_factory=set)  # drama-1 first_time_only
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
        release intent is just a tag, not a deferred consequence. The
        drama-1 weight spec resolves here (flat int = base, no tail;
        the multiplier object flattens to base + modifier list — the
        buffer stores data, the effective weight is computed per
        evaluation, never stored). The drama-2 option blocks flatten
        the same way (`_option_specs` — the choice is computed per
        release, never stored)."""
        config = self.pack.rules.get("director", {})
        hook_specs = config.get("hooks", {})
        for tag in event.hooks:
            spec = hook_specs.get(tag)
            if spec is None:
                continue
            base, modifiers = _weight_spec(spec["weight"])
            self._hooks.append(
                SeededHook(
                    tag=tag,
                    seeded_by_event=event.id,
                    seeded_at_tick=event.t,
                    weight=base,
                    release_threshold=int(spec["release_threshold"]),
                    target_npc=spec["target_npc"],
                    intent_kind=spec["intent"]["kind"],
                    intent_target=spec["intent"].get("target"),
                    intent_fields=dict(spec["intent"].get("fields", {})),
                    trigger=spec.get("trigger"),
                    climax=bool(spec.get("climax", False)),
                    channel=spec.get("channel"),
                    weight_modifiers=modifiers,
                    first_time_only=bool(spec.get("first_time_only", False)),
                    options=_option_specs(spec.get("options")),
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

        drama-2 (iter-41): every release resolves its option choice
        first — a hook whose options are ALL gated off or zeroed out
        cannot release this beat (nothing hits the door, no budget is
        consumed; the hook waits for a world where an option opens),
        and the chosen option's payload overrides the base whole-key.
        A hook without options runs the v0.1 path byte-identically.

        Reads observable state only (L6): the projection and the
        seeded-hook buffer — never knowledge records, never PC
        internals (the entropy law, phases.md/DIRECTOR_SPEC §5). The
        pacing clock (DIR-1) advances once per beat BEFORE the gates
        read it; PEAK/REST suppress the quiet path — every channel
        (the clock reads TOTAL entropy: one drama arc), explicit
        triggers stay ungated (D-005 — causality is not pacing).
        """
        unreleased = [
            (idx, hook) for idx, hook in self._unreleased()
            if hook.tag not in self._burned_tags  # drama-1: a burned tag
            # never releases again and never counts toward entropy — its
            # remaining instances are facts (INV-5) but not tension.
        ]
        # Entropy is invariant across this call — nothing mutates the
        # buffer, the release set, or the projection before an immediate
        # return — so it is computed once and reused for every policy
        # check (the eager per-hook recomputation was pure waste under a
        # rejecting policy: k+1 identical evaluations per beat). Computed
        # even on an empty buffer: the pacing clock models the world's
        # drama (a burning room is a PEAK with the buffer drained), and
        # entropy is its only input.
        current_entropy = entropy(
            projection, iter(h for _, h in unreleased), self.pack.rules, beat_tick
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
            option = _choose_option(hook, projection, beat_tick)
            if option is None:
                # drama-2: every option is gated off or zeroed out — the
                # hook cannot release this beat; the next hook in line
                # gets its chance (nothing hit the door, no budget spent)
                continue
            self._mark_released(idx, hook)
            return [self._intent(hook, option)]
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
                # drama-2: a hook whose options are all closed is not a
                # candidate — the walk takes the first releasable pick
                for idx, hook in candidates:
                    option = _choose_option(hook, projection, beat_tick)
                    if option is None:
                        continue
                    self._mark_released(idx, hook)
                    assert self._pacing is not None  # the gate passed: pacing exists
                    self._pacing = PacingClock("PEAK_CLIMAX", 1)  # the boss beat
                    return [self._intent(hook, option)]
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
                iter(hook for _, hook in unreleased), self.pack.rules, beat_tick,
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
        # (oldest first — far hooks deserve priority, MVP_SCOPE §5).
        # drama-2: a hook whose options are all closed is not a candidate
        # — the walk takes the first releasable pick in tiebreak order.
        candidates.sort(key=lambda ih: (ih[1].release_threshold, ih[1].seeded_at_tick))
        for idx, hook in candidates:
            option = _choose_option(hook, projection, beat_tick)
            if option is None:
                continue
            self._mark_released(idx, hook)
            return [self._intent(hook, option)]
        return []

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

    def _mark_released(self, idx: int, hook: SeededHook) -> None:
        self._released.add(idx)
        self._npc_last_release_beat[hook.target_npc] = self.beat_count
        if hook.first_time_only:
            # drama-1: the Wesnoth fire-only-once law — the tag burns for
            # the run; its remaining instances stop counting (releases()
            # filters them) and never release.
            self._burned_tags.add(hook.tag)

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

    def _intent(self, hook: SeededHook, option: OptionSpec) -> IntentData:
        """Build the IntentData the loop will enqueue (the director never
        writes canon — it broadcasts an objective through the door). The
        drama-2 payload merge: the chosen option's intent block overrides
        the hook's base payload WHOLE-KEY (kind / target / fields each
        wholly replaced when declared — Paradox options are complete
        alternative effect branches, not patches); an option without an
        intent block (and the implicit base option of an option-less
        hook) carries the base payload unchanged."""
        kind = hook.intent_kind
        target = hook.intent_target
        fields = dict(hook.intent_fields)
        if option.intent is not None:
            override = option.intent
            if "kind" in override:
                kind = override["kind"]
            if "target" in override:
                target = override["target"]
            if "fields" in override:
                fields = dict(override["fields"])
        intent_id = sequence_id(HOOK_PREFIX, self._release_seq)
        self._release_seq += 1
        return IntentData(
            id=intent_id,
            kind=kind,
            actor=hook.target_npc,
            target=target,
            fields=fields,
            based_on_event_seq=0,  # the loop stamps the current count at enqueue
        )
