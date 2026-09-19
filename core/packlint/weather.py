"""The weather block lint (weather-1's seasonal family — the D-175
split's weather family)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.packlint.helpers import PackError, _is_int
from core.weather import EROSION_KEYS as WEATHER_EROSION_KEYS
from core.weather import SEASONAL_KEYS as WEATHER_SEASONAL_KEYS
from core.weather import STATE_KEYS as WEATHER_STATE_KEYS
from core.weather import WEATHER_BLOCK, WEATHER_KEYS


class WeatherLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _weather(self) -> None:
        """The ambient weather family's pack half (weather-1; runs LAST —
        the block reads the macro clock (`_time_rules`), the template
        closure, the director hook table, and the transition layers'
        follow-up flags, all validated before it).

        THE PAIRING LAW (one direction): the family rides the macro
        clock's cadence — a weather block without `time.macro` is dead
        data (no crossing ever fires the chain). The other direction is
        legal: the clock may run weatherless (maclock-1's own row —
        consumers are optional, the primitive never demands them).

        THE IDENTITY LAW: the family's event type differs from the macro
        turn's — the fold scans by event type, a shared type would mix
        the year's counter with the sky's state (two families, two
        identities).

        THE CLOSED VOCABULARY: `event_type` (in the template closure,
        EVENT_SCHEMA §11), `initial` (a declared state — the pack's sky
        at run start, deterministic, never a draw), `states` (the
        chain's vocabulary). Every state: non-empty `weights` (keys ⊆
        the declared states, positive ints — the Markov chain in data,
        no TTL, no turn counters, D-049's fence), optional `hooks`
        (tags ⊆ the director registry — the seeded consequences), and
        optional `erosion` rules.

        THE EROSION RULES (the fire follow-ups' shape): the `event_type`
        is the queue identity — UNIQUE across the block (two rules
        sharing one type would share one queue actor id), in the
        template closure; `after_ticks` >= 1 (the erosion is a deferred
        consequence, never same-tick); `prop` must be a transition
        layer's follow-up flag (the closure law — the family erodes
        promoted canon objects, the flags the layers mint); `from` !=
        `to` (a no-op rule is dead data — the vacuity family);
        `irreversible` an optional boolean.

        THE REACHABILITY LAW (the vacuity family at chain granularity,
        the depth-5b precedent): every declared state must be reachable
        from `initial` over the weights graph — a state the chain can
        never roll is dead data, refused."""
        rules = self._data["rules.json"]
        weather = rules.get(WEATHER_BLOCK)
        if weather is None:
            return  # the unarmed law: no block, no family, zero draws
        where = f"rules.json {WEATHER_BLOCK}"
        if not isinstance(weather, Mapping):
            raise PackError(f"{where}: must be an object")
        macro = rules.get("time", {}).get("macro")
        if macro is None:
            raise PackError(
                f"{where}: the ambient family rides the macro clock's "
                "cadence — declare time.macro (a weather block without "
                "the clock is dead data: no crossing ever fires the "
                "chain; the pairing law — the other direction is legal, "
                "the clock may run weatherless)"
            )
        unknown = sorted(set(weather) - set(WEATHER_KEYS))
        if unknown:
            raise PackError(
                f"{where}: unknown keys {unknown} (the closed "
                f"vocabulary: {' | '.join(WEATHER_KEYS)})"
            )
        if "notes" in weather and not isinstance(weather["notes"], str):
            raise PackError(f"{where}.notes must be a string")
        templates = self._data["templates.json"]["events"]
        event_type = weather.get("event_type")
        if not (
            isinstance(event_type, str) and event_type in templates
        ):
            raise PackError(
                f"{where}.event_type {event_type!r} is not in the "
                "template vocabulary (EVENT_SCHEMA §11 — closed per "
                "pack)"
            )
        if event_type == macro.get("event_type"):
            raise PackError(
                f"{where}.event_type {event_type!r} is the macro turn's "
                "own event type — two families, two identities (the "
                "fold scans by event type; a shared type would mix the "
                "year's counter with the sky's state)"
            )
        states = weather.get("states")
        if not (isinstance(states, Mapping) and states):
            raise PackError(
                f"{where}.states must be a non-empty object (the "
                "chain's vocabulary — an empty chain has no sky to "
                "turn)"
            )
        initial = weather.get("initial")
        if not (isinstance(initial, str) and initial in states):
            raise PackError(
                f"{where}.initial {initial!r} must name a declared "
                "state (the pack's sky at run start — deterministic, "
                "never a draw)"
            )
        hook_table = rules.get("director", {}).get("hooks", {})
        transition_flags = self._transition_flags()
        erosion_event_types: set[str] = set()
        for state, spec in states.items():
            state_where = f"{where}.states[{state!r}]"
            if not isinstance(spec, Mapping):
                raise PackError(f"{state_where}: must be an object")
            unknown = sorted(set(spec) - set(WEATHER_STATE_KEYS))
            if unknown:
                raise PackError(
                    f"{state_where}: unknown keys {unknown} (the "
                    f"closed vocabulary: {' | '.join(WEATHER_STATE_KEYS)})"
                )
            weights = spec.get("weights")
            if not (isinstance(weights, Mapping) and weights):
                raise PackError(
                    f"{state_where}.weights must be a non-empty object "
                    "(the chain must be able to move — a weightless "
                    "state is a dead end the draw cannot walk)"
                )
            for target, weight in weights.items():
                if target not in states:
                    raise PackError(
                        f"{state_where}.weights: {target!r} is not a "
                        "declared state (the chain's vocabulary is "
                        "closed)"
                    )
                if not (_is_int(weight) and weight >= 1):
                    raise PackError(
                        f"{state_where}.weights[{target!r}] must be an "
                        f"integer >= 1, got {weight!r} (zero or "
                        "negative is not a weight — omit the key "
                        "instead)"
                    )
            hooks = spec.get("hooks", [])
            if not isinstance(hooks, list):
                raise PackError(
                    f"{state_where}.hooks must be a list of director "
                    "hook tags (the seeded consequences ride the "
                    "director's own registry)"
                )
            for tag in hooks:
                if not (isinstance(tag, str) and tag in hook_table):
                    raise PackError(
                        f"{state_where}.hooks: {tag!r} is not a "
                        "declared director.hooks entry (the closure "
                        "law — the consequences release through the "
                        "registry the director already reads)"
                    )
            erosion = spec.get("erosion", [])
            if not isinstance(erosion, list):
                raise PackError(
                    f"{state_where}.erosion must be a list of rules "
                    "(the fire follow-ups' shape: one SEEDED follow-up "
                    "per rule)"
                )
            for rule in erosion:
                if not isinstance(rule, Mapping):
                    raise PackError(
                        f"{state_where}.erosion: each rule must be an "
                        "object"
                    )
                rule_where = (
                    f"{state_where}.erosion[{rule.get('event_type')!r}]"
                )
                unknown = sorted(set(rule) - set(WEATHER_EROSION_KEYS))
                if unknown:
                    raise PackError(
                        f"{rule_where}: unknown keys {unknown} (the "
                        f"closed vocabulary: {' | '.join(WEATHER_EROSION_KEYS)})"
                    )
                rule_event = rule.get("event_type")
                if not (
                    isinstance(rule_event, str) and rule_event in templates
                ):
                    raise PackError(
                        f"{rule_where}.event_type {rule_event!r} is not "
                        "in the template vocabulary (EVENT_SCHEMA §11 — "
                        "closed per pack)"
                    )
                if rule_event in erosion_event_types:
                    raise PackError(
                        f"{rule_where}: the event type is the erosion "
                        "rule's queue identity — another rule already "
                        "declares it (one rule per event type; the "
                        "queue's actor id is the rule's own)"
                    )
                erosion_event_types.add(rule_event)
                if not (
                    _is_int(rule.get("after_ticks"))
                    and rule["after_ticks"] >= 1
                ):
                    raise PackError(
                        f"{rule_where}.after_ticks must be an integer "
                        ">= 1, got {rule.get('after_ticks')!r} (the "
                        "erosion is a deferred consequence, never "
                        "same-tick)"
                    )
                prop = rule.get("prop")
                if not (isinstance(prop, str) and prop in transition_flags):
                    raise PackError(
                        f"{rule_where}.prop {prop!r} is not a "
                        "transition layer's follow-up flag (the "
                        "erosion family erodes PROMOTED canon objects — "
                        "the flags the layers mint, the closure law; "
                        "anything else the fold holds is another "
                        "family's own, never the weather's)"
                    )
                if not ("from" in rule and "to" in rule
                        and rule["from"] != rule["to"]):
                    raise PackError(
                        f"{rule_where}: from and to must be present and "
                        "differ (a no-op rule is dead data — the "
                        "vacuity family)"
                    )
                if ("irreversible" in rule
                        and not isinstance(rule["irreversible"], bool)):
                    raise PackError(
                        f"{rule_where}.irreversible must be a boolean"
                    )
        # the reachability law: BFS from `initial` over the weights
        # graph; sorted expansion (INV-2's construction-order discipline)
        seen = {initial}
        frontier = [initial]
        while frontier:
            state = frontier.pop()
            for target in sorted(states[state].get("weights", {})):
                if target not in seen:
                    seen.add(target)
                    frontier.append(target)
        unreachable = sorted(set(states) - seen)
        if unreachable:
            raise PackError(
                f"{where}.states: {unreachable} unreachable from the "
                f"initial state {initial!r} over the weights graph — a "
                "state the chain can never roll is dead data (the "
                "reachability law, the depth-5b precedent)"
            )
        # -- the seasonal layer (the calendar slice) ---------------------
        # `ride` names a DECLARED, CYCLED time.calendar entry: the
        # chain's rolls move to that sub-year clock's crossings (the
        # reference, never a declaration — "one clock, one cadence"),
        # and the phases the weights key on come from that entry's own
        # cycle (an uncycled ride has no phases to bias — dead data,
        # the vacuity family). Each `weights[phase][state]` map is the
        # FULL replacement for that state's roll during that phase:
        # the same shape the base states' own weights lint enforces
        # (non-empty, keys ⊆ the declared states, integers >= 1).
        seasonal = weather.get("seasonal")
        if seasonal is not None:
            seasonal_where = f"{where}.seasonal"
            if not isinstance(seasonal, Mapping):
                raise PackError(
                    f"{seasonal_where}: must be an object (ride | weights | "
                    "notes)"
                )
            unknown = sorted(set(seasonal) - set(WEATHER_SEASONAL_KEYS))
            if unknown:
                raise PackError(
                    f"{seasonal_where}: unknown keys {unknown} (the "
                    f"closed vocabulary: {' | '.join(WEATHER_SEASONAL_KEYS)})"
                )
            if "notes" in seasonal and not isinstance(
                seasonal["notes"], str
            ):
                raise PackError(
                    f"{seasonal_where}.notes must be a string (the pack's "
                    "commentary convention)"
                )
            ride = seasonal.get("ride")
            calendar = rules.get("time", {}).get("calendar") or {}
            ride_entry = calendar.get(ride) if isinstance(ride, str) else None
            if not (
                isinstance(ride, str)
                and isinstance(ride_entry, Mapping)
                and isinstance(ride_entry.get("cycle"), list)
            ):
                raise PackError(
                    f"{seasonal_where}.ride {ride!r} must name a DECLARED "
                    "time.calendar entry carrying a cycle (the binding "
                    "law: the rolls move to that sub-year clock's "
                    "crossings and the phases come from its cycle — an "
                    "uncycled or absent ride is dead data, the vacuity "
                    "family)"
                )
            phases = {
                pair.get("phase")
                for pair in ride_entry["cycle"]
                if isinstance(pair, Mapping)
            }
            phase_weights = seasonal.get("weights")
            if phase_weights is None:
                raise PackError(
                    f"{seasonal_where}.weights must be present — a "
                    "seasonal layer that biases nothing is dead data "
                    "(the vacuity family; move the rolls without the "
                    "bias through the ride alone is not a layer)"
                )
            if not isinstance(phase_weights, Mapping):
                raise PackError(
                    f"{seasonal_where}.weights must be an object keyed by "
                    "the ride's cycle phases, each the per-state weight "
                    "maps"
                )
            for phase, overrides in phase_weights.items():
                phase_where = f"{seasonal_where}.weights[{phase!r}]"
                if phase not in phases:
                    raise PackError(
                        f"{phase_where}: not a phase of the ride's cycle "
                        f"{sorted(phases)} (the binding law)"
                    )
                if not isinstance(overrides, Mapping) or not overrides:
                    raise PackError(
                        f"{phase_where}: must be a non-empty object keyed "
                        "by the current state whose roll it overrides"
                    )
                for state, weights in overrides.items():
                    state_where = f"{phase_where}[{state!r}]"
                    if state not in states:
                        raise PackError(
                            f"{state_where}: not a declared weather "
                            "state (the chain's vocabulary is closed)"
                        )
                    if not (isinstance(weights, Mapping) and weights):
                        raise PackError(
                            f"{state_where}: must be a non-empty weight "
                            "map (the full replacement for that state's "
                            "roll during the phase)"
                        )
                    for target, weight in weights.items():
                        if target not in states:
                            raise PackError(
                                f"{state_where}: {target!r} is not a "
                                "declared state (the chain's vocabulary "
                                "is closed)"
                            )
                        if not (_is_int(weight) and weight >= 1):
                            raise PackError(
                                f"{state_where}[{target!r}] must be an "
                                f"integer >= 1, got {weight!r} (zero or "
                                "negative is not a weight — omit the "
                                "key instead)"
                            )


    def _transition_flags(self) -> set[str]:
        """The flags the transition layers' follow-ups mint — the erosion
        family's target closure (the promoted canon objects the ambient
        family may revert; every other fold value is another family's
        own, never the weather's)."""
        flags: set[str] = set()
        for config in self._data["rules.json"].get("transitions", {}).values():
            if not isinstance(config, Mapping):
                continue  # the block's own meta entries
            for spec in config.get("follow_ups", ()):
                if isinstance(spec, Mapping) and isinstance(spec.get("flag"), str):
                    flags.add(spec["flag"])
        return flags
