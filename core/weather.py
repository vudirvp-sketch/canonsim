"""The ambient weather family (weather-1, `phases.md` §5 — TASKS'
"ambient weather + canon erosion"; D-116 (7): "an ambient family over
the existing doors — no physics engine"):

- THE CADENCE: the family rides the macro clock (`core/macro.py`'s,
  maclock-1/D-124 — one clock, one cadence, never a second declaration).
  At each macro crossing, AFTER the turn, the weather chain rolls its
  next state and — when it CHANGES — commits ONE event through the canon
  door, chained to the turn (the drift's precedent: the consumer rides
  the clock's own event). The event carries NO knowledge (the ambient
  law — a world event, the macro turn's own shape) and NO state_changes
  (L3: the current weather is the fold over weather events — the last
  event's state, the pack's `initial` before the first; derive, never
  store).
- THE CHAIN: pack-declared states with per-state transition weights
  (a Markov chain in data — the weather persists through self-weights,
  no TTL, no turn counters, no decay timers, D-049's fence held). The
  draw rides the family's own `weather:chain` stream (the D-079 law's
  seventh member — singleton: one weather per world; arming or
  re-tuning the block shifts neither a canon check draw nor any other
  family's rolls, and the substantive fingerprint never sees a weather
  draw). A roll that lands on the CURRENT state suppresses the event
  (the idempotence discipline, KI#13's family — no no-op lines in the
  canon; the draw still advances the stream, INV-2 untouched).
- THE SEEDED CONSEQUENCES (TIME-1): the change event carries the new
  state's pack-declared hook tags — the director's buffer seeds them at
  commit time through the existing door (D-005; the ambient channel's
  quiet gate the release path, the idle-murmur pattern, D-082).
- THE EROSION (the fire follow-ups' shape): promoted canon objects erode
  via `state_changes` in SEEDED follow-ups — the change event seeds one
  queue entry per pack-declared erosion rule at `t + after_ticks`; the
  entry's commit scans the fold for entities holding the rule's `from`
  value on the target `prop` and emits ONE event per eroded entity (an
  explicit counter-event is the legal revert of a held flag,
  EVENT_SCHEMA §4). Idempotent on state (KI#13): an entity no longer
  holding `from` is skipped, never a duplicate, never a no-op line.
  Erosion targets are the transition layers' follow-up flags (the
  promoted canon objects the TASKS row names — the lint's closure law).

The unarmed law (the 68a pattern): an absent `weather` block is zero
events, zero draws, zero seeds — the macro clock may run without the
family; the family may never run without the clock (the pairing law,
`core/pack.py::_weather` owns the load-time contract).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from core.intent import pack_importance
from core.log import EventDraft, StateChange
from core.rng import RngBank, weather_stream_name
from core.transitions import WORLD

__all__ = [
    "EROSION_KEYS",
    "STATE_KEYS",
    "WEATHER_BLOCK",
    "WEATHER_KEYS",
    "ErosionSpec",
    "WeatherError",
    "current_weather",
    "erosion_drafts",
    "erosion_specs",
    "weather_turn_draft",
]

#: The rules.json block this module reads (`core/pack.py::_weather` owns
#: the load-time shape lint). Absent -> the unarmed family (the macro
#: clock may run without weather; the lint refuses the other direction).
WEATHER_BLOCK: Final = "weather"

#: The closed vocabulary of the weather block (the lint owns the
#: load-time contract; this is the engine-side mirror the docs cite —
#: one owner per shape, the lint the authority). `notes` is the pack's
#: commentary convention (an optional string — every committed block
#: carries its author note).
WEATHER_KEYS: Final = ("event_type", "initial", "states", "notes")

#: The closed vocabulary of one state's declaration.
STATE_KEYS: Final = ("weights", "hooks", "erosion")

#: The closed vocabulary of one erosion rule (the SEEDED follow-up's
#: pack data — the transition layers' follow_ups shape, the ambient
#: family's own target vocabulary).
EROSION_KEYS: Final = (
    "event_type", "after_ticks", "prop", "from", "to", "irreversible",
)


class WeatherError(ValueError):
    """A weather-family contract failure (raw-read surfaces fail loud,
    never with a KeyError — the pred-contract family law, D-111)."""


@dataclass(frozen=True, slots=True)
class ErosionSpec:
    """A SEEDED erosion follow-up: emit the rule's event type at
    `at_tick` (the layer FollowUpSpec twin — the ambient
    family's own queue identity is the rule's event type, unique per
    block by lint)."""

    event_type: str
    at_tick: int


def _weather(rules: Mapping[str, Any]) -> Mapping[str, Any]:
    """The weather block, validated loud (the runtime backstop: the lint
    owns the load-time contract; a hand-built runtime config that skips
    it fails here with the block named)."""
    weather = rules.get(WEATHER_BLOCK)
    if not isinstance(weather, Mapping):
        raise WeatherError(
            f"the weather family reads an armed {WEATHER_BLOCK!r} block — "
            "the rules declare none (the pack lint refuses a weather "
            "block without the macro clock; this call is the runtime "
            "backstop for hand-built configs)"
        )
    return weather


def current_weather(
    rules: Mapping[str, Any], events: Sequence[Any]
) -> str:
    """The fold read (L3): the last weather event's state, else the
    pack's declared `initial` (the run opens under the pack's sky —
    deterministic, no draw at start; the first crossing rolls the
    chain). The events walk backwards — the newest weather event wins."""
    initial = _weather(rules)["initial"]
    event_type = _weather(rules)["event_type"]
    for event in reversed(events):
        if event.type == event_type:
            state = event.outcome.get("weather")
            if isinstance(state, str):
                return state
    return str(initial)


def _draw_state(
    bank: RngBank, weights: Mapping[str, int]
) -> str:
    """One weighted pick from the chain's own stream (INV-2: the sorted
    key walk — construction order is a set-iteration hazard, `sorted()`
    is the law; the walk compares `draw * total` against the running
    sum, no division anywhere)."""
    with bank.assure(weather_stream_name()):
        draw = bank.random()
    total = sum(weights[key] for key in sorted(weights))
    threshold = draw * total
    acc = 0.0
    for key in sorted(weights):
        acc += weights[key]
        if threshold < acc:
            return key
    # unreachable: the last cumulative equals `total` and draw < 1
    return sorted(weights)[-1]


def weather_turn_draft(
    rules: Mapping[str, Any],
    bank: RngBank,
    tick: int,
    prev: str,
) -> EventDraft | None:
    """The ambient family's one event for the macro crossing at `tick`:
    roll the chain from `prev`; a roll that lands on `prev` again is
    the idempotence law — None, no event, no seeds (the draw still
    advanced the family's own stream). A change commits ONE event:
    actor `world`, cause chained by the loop to the turn, the new state
    under the outcome's flat `weather` key (the template binding
    surface), the new state's hook tags (the director's seeded
    consequences, TIME-1 SEEDED), no knowledge (the ambient law), no
    state_changes (the weather state is fold-derived, L3); importance
    rides the pack's own rule (the story-critical listing decides —
    the tune-1 split)."""
    weather = _weather(rules)
    states = weather["states"]
    if prev not in states:
        raise WeatherError(
            f"the weather chain rolled from {prev!r} — a state the "
            "block does not declare (the lint guarantees the fold "
            "reads a declared state; this is the runtime backstop)"
        )
    spec = states[prev]
    weights = spec.get("weights", {})
    if not isinstance(weights, Mapping) or not weights:
        raise WeatherError(
            f"weather.states[{prev!r}].weights must be a non-empty "
            "object (the chain must be able to move — the lint owns "
            "the load-time contract; this is the runtime backstop)"
        )
    state = _draw_state(bank, weights)
    if state == prev:
        return None  # the idempotence law: no no-op line in the canon
    hooks = tuple(states[state].get("hooks", ()))
    return EventDraft(
        t=tick,
        type=str(weather["event_type"]),
        actor=WORLD,
        target=None,
        cause=None,  # the loop chains to the turn (the drift precedent)
        outcome={"weather": state},
        knowledge=(),
        state_changes=(),
        hooks=hooks,
        importance=pack_importance(
            rules, {WORLD}, irreversible=0, hooks=len(hooks),
            event_type=str(weather["event_type"]),
        ),
        provenance={},  # the loop stamps seed at commit (the family law)
    )


def erosion_specs(
    rules: Mapping[str, Any], state: str
) -> tuple[ErosionSpec, ...]:
    """The state's SEEDED erosion follow-ups (the fire follow-ups' shape:
    the queue entries the loop pushes at the change event's own tick +
    `after_ticks`). The rule set is read at seed time; the erosion
    itself reads the fold at FIRE time — the state the world holds then
    is the truth, never the state it held at seed time."""
    weather = _weather(rules)
    states = weather["states"]
    if state not in states:
        raise WeatherError(
            f"erosion_specs read the state {state!r} — a state the "
            "block does not declare"
        )
    return tuple(
        ErosionSpec(
            event_type=str(rule["event_type"]),
            at_tick=int(rule["after_ticks"]),
        )
        for rule in states[state].get("erosion", ())
    )


def erosion_drafts(
    rules: Mapping[str, Any],
    projection: Mapping[str, Mapping[str, Any]],
    tick: int,
    event_type: str,
    cause_id: str,
) -> tuple[EventDraft, ...]:
    """The erosion follow-up's commit drafts (fired at the entry's tick
    by the loop): find the rule by its event type (unique per block by
    lint — the queue identity), scan the fold for entities holding the
    rule's `from` value on the target `prop`, and emit ONE event per
    eroded entity in sorted id order (INV-2: construction order never
    iterates a set). No matches -> no events (the idempotence law —
    the story was already told, or never began). Each draft: actor
    `world`, target the eroded entity, cause the seeding weather
    event, the state_changes carrying the explicit revert
    (EVENT_SCHEMA §4 — a held flag's legal counter-event), no
    knowledge (the ambient law), importance through the pack's rule."""
    weather = _weather(rules)
    for state, spec in sorted(weather["states"].items()):
        for rule in spec.get("erosion", ()):
            if str(rule["event_type"]) == event_type:
                return _erosion_for(
                    rules, projection, tick, str(state), rule, cause_id,
                )
    raise WeatherError(
        f"the weather erosion rule {event_type!r} is not declared by "
        "any state (the queue identity is the rule's event type, "
        "unique per block by lint — this call is the runtime backstop)"
    )


def _erosion_for(
    rules: Mapping[str, Any],
    projection: Mapping[str, Mapping[str, Any]],
    tick: int,
    state: str,
    rule: Mapping[str, Any],
    cause_id: str,
) -> tuple[EventDraft, ...]:
    """One rule's drafts: the fold scan over every entity's props in
    sorted id order; an entity no longer holding `from` is skipped (the
    idempotence law), the projection's own value rides `from_` (the
    commit gate's D-035 contract)."""
    prop = str(rule["prop"])
    from_value = rule["from"]
    to_value = rule["to"]
    irreversible = bool(rule.get("irreversible", False))
    event_type = str(rule["event_type"])
    drafts: list[EventDraft] = []
    for entity_id in sorted(projection):
        props = projection[entity_id]
        if props.get(prop) != from_value:
            continue
        change = StateChange(
            entity=entity_id,
            prop=prop,
            from_=props[prop],
            to_=to_value,
            irreversible=irreversible,
        )
        drafts.append(
            EventDraft(
                t=tick,
                type=event_type,
                actor=WORLD,
                target=entity_id,
                cause=cause_id,
                outcome={"weather": state, "location": entity_id},
                knowledge=(),
                state_changes=(change,),
                importance=pack_importance(
                    rules, {WORLD, entity_id},
                    irreversible=1 if irreversible else 0,
                    hooks=0,
                    event_type=event_type,
                ),
                provenance={},  # the loop stamps seed at commit
            )
        )
    return tuple(drafts)
