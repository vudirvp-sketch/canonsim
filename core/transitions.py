"""The generic transition engine (phase0 §2, Brogue `promoteTile` donor):
one mechanism — flag-gated ignition, stochastic per-tick promotion, SEEDED
follow-ups — driven entirely by pack-declared layers (`rules.json`
`transitions`). Core code carries no layer names and no domain words
(INV-3): the fire chain is data, the engine is mechanics.

The engine is pure: it returns event drafts and plans; `core/loop.py` owns
the writer and the queue (the only canon-write path, INV-1), chains
`cause`, and stamps `provenance.seed` at append time. State layout on the
location: `<layer>.<spot>` = "burning" (irreversible), plus `smoke` /
`destroyed` flags. Spread rolls draw from the substantive stream — they
change canon.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from core.intent import knowers_at, pack_importance, resolve_knowledge
from core.log import EventDraft, StateChange
from core.rng import RngBank

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle with pack.py
    from core.pack import Pack

__all__ = [
    "FollowUpSpec",
    "Ignition",
    "IgnitionPlan",
    "SpreadResult",
    "follow_up_draft",
    "ignite",
    "spread_tick",
]

WORLD: str = "world"  # EVENT_SCHEMA §2: the actor for world-events


@dataclass(frozen=True, slots=True)
class Ignition:
    """A world reaction a resolver requests: start `layer` at one spot of
    a location (carried on `Resolution.ignitions`)."""

    layer: str
    location: str
    spot: str


@dataclass(frozen=True, slots=True)
class FollowUpSpec:
    """A SEEDED follow-up: emit the layer's `kind` event at `at_tick`."""

    kind: str  # "smoke" | "burnout"
    at_tick: int


@dataclass(frozen=True, slots=True)
class IgnitionPlan:
    """What an ignition produces: the started event (+ alarm when others
    are present, fear spikes per pack rule), smoke/burnout follow-up
    seeds, and whether the spread pass starts."""

    drafts: tuple[EventDraft, ...]
    follow_ups: tuple[FollowUpSpec, ...]
    seed_pass: bool


@dataclass(frozen=True, slots=True)
class SpreadResult:
    """One spread pass tick: new spread events and whether the pass
    continues (unburning spots remain somewhere)."""

    drafts: tuple[EventDraft, ...]
    continue_pass: bool


def _layer(pack: Pack, layer: str) -> Mapping[str, Any]:
    transitions = pack.rules.get("transitions", {})
    if layer not in transitions:
        raise ValueError(f"unknown transition layer {layer!r}")
    return transitions[layer]


def _spots(pack: Pack, layer_cfg: Mapping[str, Any], location: str) -> list[str]:
    return list(pack.entity(location).get(layer_cfg["spot_field"], ()))


def _burning_spots(
    projection: Mapping[str, Mapping[str, Any]], layer: str, location: str
) -> list[str]:
    """Burning spot NAMES (the layer prefix stripped from the prop path)."""
    props = projection[location]
    prefix = f"{layer}."
    return [
        prop[len(prefix):]
        for prop in sorted(props)
        if prop.startswith(prefix) and props[prop] == "burning"
    ]


def _importance(
    pack: Pack,
    location: str,
    state_changes: tuple[StateChange, ...],
) -> str:
    return pack_importance(
        pack.rules,
        entities={WORLD, location} | {change.entity for change in state_changes},
        irreversible=sum(1 for change in state_changes if change.irreversible),
        hooks=0,
    )


def ignite(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
    tick: int,
    ignition: Ignition,
    cause_actor: str,
) -> IgnitionPlan:
    """Plan the ignition of one spot: the started event (irreversible),
    the alarm when other entities are present, smoke/burnout seeds, and
    the spread pass. Re-igniting an already-burning spot is a no-op plan."""
    layer_cfg = _layer(pack, ignition.layer)
    location = ignition.location
    spot = ignition.spot
    if spot not in _spots(pack, layer_cfg, location):
        raise ValueError(f"spot {spot!r} is not a {location!r} spot of the pack")
    if spot in _burning_spots(projection, ignition.layer, location):
        return IgnitionPlan(drafts=(), follow_ups=(), seed_pass=False)

    knowledge_cfg = layer_cfg["knowledge"]
    ctx = {"location": location, "cause_actor": cause_actor}
    started_knowledge = resolve_knowledge(
        [knowledge_cfg["started"]], pack, projection, ctx, tick
    )
    spot_change = StateChange(
        entity=location,
        prop=f"{ignition.layer}.{spot}",
        from_=None,
        to_="burning",
        irreversible=True,
    )
    started = EventDraft(
        t=tick,
        type=layer_cfg["events"]["started"],
        actor=WORLD,
        target=location,
        cause=None,  # chained to the causing action event by the loop
        outcome={"location": location, "spot": spot},
        knowledge=started_knowledge,
        state_changes=(spot_change,),
        importance=_importance(pack, location, (spot_change,)),
        provenance={},  # seed stamped by the loop at append time
    )

    drafts: list[EventDraft] = [started]
    fear_spike = layer_cfg["alarm"]["fear_spike"]
    occupants = [who for who in knowers_at(pack, projection, location)
                 if who != cause_actor]
    if layer_cfg["alarm"]["when_occupants_present"] and occupants:
        alarm_knowledge = resolve_knowledge(
            [knowledge_cfg["alarm"], knowledge_cfg["alarm_adjacent"]],
            pack, projection, ctx, tick,
        )
        scale_max = pack.rules["relations"]["scale"][1]
        fear_changes = tuple(
            StateChange(
                entity=who,
                prop="status.fear",
                from_=projection[who].get("status.fear", 0),
                to_=min(scale_max, projection[who].get("status.fear", 0) + fear_spike),
            )
            for who in occupants
        )
        alarm = EventDraft(
            t=tick,
            type=layer_cfg["events"]["alarm"],
            actor=WORLD,
            target=location,
            cause=None,  # chained to the started event by the loop
            outcome={"location": location, "raised_by": occupants[0]},
            knowledge=alarm_knowledge,
            state_changes=fear_changes,
            importance=pack_importance(
                pack.rules,
                entities={WORLD, location} | set(occupants),
                irreversible=0,
                hooks=0,
            ),
            provenance={},
        )
        drafts.append(alarm)

    follow_ups = (
        FollowUpSpec("smoke", tick + layer_cfg["smoke"]["after_ticks"]),
        FollowUpSpec("burnout", tick + layer_cfg["burnout"]["after_ticks"]),
    )
    return IgnitionPlan(
        drafts=tuple(drafts), follow_ups=follow_ups, seed_pass=True
    )


def spread_tick(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
    bank: RngBank,
    tick: int,
    layer: str,
    causes: Mapping[str, str],
) -> SpreadResult:
    """One pass tick: for every burning, not-destroyed location, roll each
    unburning spot (pack order) against the pack chance; emit one spread
    event per ignition, cause-chained to the location's last fire event
    (`causes`, maintained by the loop)."""
    layer_cfg = _layer(pack, layer)
    knowledge_cfg = layer_cfg["knowledge"]
    chance = layer_cfg["spread"]["chance_per_tick"]
    drafts: list[EventDraft] = []
    continue_pass = False

    burning_locations = sorted(
        entity_id
        for entity_id, props in projection.items()
        if any(
            prop.startswith(f"{layer}.") and value == "burning"
            for prop, value in props.items()
        )
    )
    for location in burning_locations:
        if projection[location].get("destroyed"):
            continue
        burning = set(_burning_spots(projection, layer, location))
        unburning = [
            spot for spot in _spots(pack, layer_cfg, location) if spot not in burning
        ]
        if unburning:
            continue_pass = True
        for spot in unburning:
            if bank.random() > chance:
                continue
            spread_knowledge = resolve_knowledge(
                [knowledge_cfg["spread"]], pack, projection,
                {"location": location, "cause_actor": None}, tick,
            )
            spot_change = StateChange(
                entity=location, prop=f"{layer}.{spot}",
                from_=None, to_="burning", irreversible=True,
            )
            drafts.append(
                EventDraft(
                    t=tick,
                    type=layer_cfg["events"]["spread"],
                    actor=WORLD,
                    target=location,
                    cause=causes.get(location),
                    outcome={"location": location, "spot": spot},
                    knowledge=spread_knowledge,
                    state_changes=(spot_change,),
                    importance=_importance(pack, location, (spot_change,)),
                    provenance={},
                )
            )
    return SpreadResult(drafts=tuple(drafts), continue_pass=continue_pass)


def follow_up_draft(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
    tick: int,
    layer: str,
    location: str,
    kind: str,
    cause_id: str,
) -> EventDraft | None:
    """The smoke / burnout event for a burning location (SEEDED at
    ignition time). Idempotent on state: a flag already set means this
    story was already told — None, no duplicate event, no duplicate
    chronicle line. None likewise when the burnout pre-empted a pending
    smoke. A second ignition of the same location seeds a second
    follow-up pair; the first to fire says the line, the rest stay
    silent (KI#13 discipline: no no-op duplicates in the canon)."""
    layer_cfg = _layer(pack, layer)
    knowledge_cfg = layer_cfg["knowledge"]
    ctx = {"location": location, "cause_actor": None}

    if kind == "smoke":
        if projection[location].get("destroyed"):
            return None  # the burnout already told this story
        if projection[location].get("smoke") is True:
            return None  # the smoke already told this story
        knowledge = resolve_knowledge(
            [knowledge_cfg["smoke"]], pack, projection, ctx, tick
        )
        changes = (
            StateChange(entity=location, prop="smoke", from_=None, to_=True),
        )
    elif kind == "burnout":
        if projection[location].get("destroyed") is True:
            return None  # the burnout already told this story
        knowledge = resolve_knowledge(
            [knowledge_cfg["burnout"]], pack, projection, ctx, tick
        )
        changes = (
            StateChange(
                entity=location, prop="destroyed",
                from_=None, to_=True, irreversible=True,
            ),
        )
    else:
        raise ValueError(f"unknown follow-up kind {kind!r}")

    return EventDraft(
        t=tick,
        type=layer_cfg["events"][kind],
        actor=WORLD,
        target=location,
        cause=cause_id,
        outcome={"location": location},
        knowledge=knowledge,
        state_changes=changes,
        importance=_importance(pack, location, changes),
        provenance={},
    )
