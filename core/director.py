"""The director (phase0 §4, MVP_SCOPE §11, D-005, DIRECTOR_SPEC): a
consequence planner that NEVER improvises. A hook seeded at event time
sits in a per-run buffer until its trigger fires (time / place /
threshold) or the stagnation detector releases the lowest-threshold
hook when narrative entropy drops below the pack's floor.

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
adaptation state is per-run, never persisted).

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
    "Director",
    "DirectorPolicy",
    "EnabledPolicy",
    "DisabledPolicy",
    "SeededHook",
    "entropy",
    "policy_from_rules",
]

HOOK_PREFIX: Final = "director"


@dataclass(frozen=True, slots=True)
class SeededHook:
    """One consequence seeded at event time (D-005). The event wrote a
    hook tag and the pack's `director.hooks` config declared what to do
    about it. A hook with no explicit trigger is stagnation-only — it
    releases only when entropy drops below the floor (the
    lowest-threshold one wins, phase0 §4). Immutable; the Director
    tracks release state via a separate index set, not by mutating the
    record (the frozen-ness documents INV-5: a seeded hook is a fact)."""

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


class DirectorPolicy(Protocol):
    """The release gate (phase0 §4 "Multi-channel policies"): the
    director asks the policy whether a release is permitted at this
    beat. The minimal pair (Enabled / Disabled) covers T8's A/B
    baseline; multi-channel (threat / social / ambient) and the
    pacing-clock escalation factors (RAMP / PEAK / REST / STAGNATION)
    are phase-3 refinements, recorded not built."""

    def permit_release(
        self,
        explicit_trigger_fires: bool,
        current_entropy: int,
    ) -> bool: ...


@dataclass(frozen=True, slots=True)
class EnabledPolicy:
    """Default: explicit triggers always release (causal); stagnation
    releases the lowest-threshold hook when entropy < floor."""

    entropy_floor: int

    def permit_release(
        self, explicit_trigger_fires: bool, current_entropy: int
    ) -> bool:
        if explicit_trigger_fires:
            return True
        return current_entropy < self.entropy_floor


@dataclass(frozen=True, slots=True)
class DisabledPolicy:
    """T8 A/B baseline: no releases ever. The buffer still seeds — D-005
    hygiene holds (a complication from nowhere is still a bug); A/B
    measures the delta the director's releases make."""

    def permit_release(
        self, explicit_trigger_fires: bool, current_entropy: int
    ) -> bool:
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
    loop enqueues — the director never writes canon itself (D-037)."""

    pack: "Pack"
    policy: DirectorPolicy
    beat_count: int = 0
    _hooks: list[SeededHook] = field(default_factory=list)
    _released: set[int] = field(default_factory=set)
    _release_seq: int = 0
    _npc_last_release_beat: dict[str, int] = field(default_factory=dict)

    @property
    def hooks(self) -> tuple[SeededHook, ...]:
        return tuple(self._hooks)

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
                )
            )

    def releases(
        self,
        projection: "Projection",
        beat_tick: int,
    ) -> list[IntentData]:
        """One beat's worth of releases (phase0 §4): explicit triggers
        fire causally first; if none fire and the policy permits a
        stagnation release (entropy < floor under EnabledPolicy), the
        stagnation detector releases the lowest-threshold hook. Budget:
        1 release per beat (the director never spams). A rejected
        director Intent consumes the budget (per-NPC cooldown follows —
        recorded, the front door does the rejecting). Dead actors (no
        projection entry / `crime_status == caught`) are never
        targeted.

        Reads observable state only (L6): the projection and the
        seeded-hook buffer — never knowledge records, never PC
        internals (the entropy law, phases.md/DIRECTOR_SPEC §5)."""
        unreleased = list(self._unreleased())
        if not unreleased:
            return []
        # Entropy is invariant across this call — nothing mutates the
        # buffer, the release set, or the projection before an immediate
        # return — so it is computed once and reused for every policy
        # check (the eager per-hook recomputation was pure waste under a
        # rejecting policy: k+1 identical evaluations per beat).
        current_entropy = entropy(
            projection, iter(h for _, h in unreleased), self.pack.rules
        )
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
        # 2) stagnation release — entropy < floor → lowest-threshold hook
        if not self.policy.permit_release(
            explicit_trigger_fires=False, current_entropy=current_entropy
        ):
            return []
        candidates = [
            (idx, hook) for idx, hook in unreleased
            if not self._on_cooldown(hook.target_npc)
            and self._target_alive(projection, hook.target_npc)
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
