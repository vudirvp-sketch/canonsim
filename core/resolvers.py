"""The ActionResolver registry (phase0 §2, D-031): pack data references
resolvers by name; each resolver is a generic mechanic — no domain words
(INV-3, enforced by the stoplist test). One iteration = the 12 actions of
`MVP_SCOPE.md` §7.

A resolver runs at completion time (checks have already been rolled by
`core/intent.py`); it reads the projection, draws nothing except explicit
ignition rolls, and returns a `Resolution`: which event type to emit (the
success/failure types are pack data), the outcome payload, knowledge
records (audiences + slot templates from the pack), state changes, hooks,
and world-reaction ignitions the loop executes afterwards. Resolvers are
pure: the loop owns the writer and the queue (INV-1).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Callable, Final

from core.intent import (
    CheckResult,
    IntentData,
    Resolution,
    RunnerError,
    find_flagged_accessible,
    find_flagged_carried,
    location_of,
    resolve_knowledge,
)
from core.log import StateChange
from core.rng import RngBank
from core.transitions import Ignition

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle with pack.py
    from core.pack import Pack

__all__ = ["REGISTRY", "ResolverFn"]

ResolverFn = Callable[
    ["Pack", Mapping[str, Mapping[str, Any]], "RngBank", "IntentData",
     Mapping[str, Any], "CheckResult | None", int],
    "Resolution",
]

Projection = Mapping[str, Mapping[str, Any]]


def _ctx(intent: IntentData, projection: Projection) -> dict[str, Any]:
    return {
        "actor": intent.actor,
        "target": intent.target,
        "location": projection[intent.actor]["position"],
    }


def _branch(check: CheckResult | None, action: Mapping[str, Any]) -> str:
    """success | failure | failure_total (the margin split is steal's; any
    action with a failure_total template gets it for free)."""
    if check is None or check.passed:
        return "success"
    if check.total_failure and "failure_total" in action["knowledge"]:
        return "failure_total"
    return "failure"


def _knowledge(
    action: Mapping[str, Any],
    branch: str,
    pack: Pack,
    projection: Projection,
    intent: IntentData,
    tick: int,
) -> tuple[Any, ...]:
    templates = action["knowledge"].get(branch, [])
    return resolve_knowledge(templates, pack, projection, _ctx(intent, projection), tick)


def _check_outcome(check: CheckResult | None) -> dict[str, Any]:
    if check is None:
        return {}
    return {
        "passed": check.passed,
        "margin": check.margin,
        "attacker_total": check.attacker_total,
        "defender_total": check.defender_total,
        "defender_id": check.defender_id,
        "total_failure": check.total_failure,
    }


def _move_changes(
    pack: Pack, projection: Projection, actor: str, destination: str
) -> tuple[StateChange, ...]:
    """The actor's position delta plus every carried item's (items travel
    with their carrier)."""
    current = projection[actor]["position"]
    changes = [StateChange(entity=actor, prop="position", from_=current, to_=destination)]
    for item in pack.entities["items"]:
        if projection[item["id"]].get("carrier") == actor:
            changes.append(
                StateChange(
                    entity=item["id"], prop="position",
                    from_=current, to_=destination,
                )
            )
    return tuple(changes)


def _hooks(action: Mapping[str, Any], branch: str) -> tuple[str, ...]:
    key = "failure" if branch == "failure_total" else branch
    return tuple(action.get("hooks", {}).get(key, ()))


# -- the twelve ---------------------------------------------------------------


def _observe(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """look_around: the actor learns a scene snapshot of the location."""
    location = projection[intent.actor]["position"]
    return Resolution(
        event_type=action["events"]["success"],
        outcome={"location": location},
        knowledge=_knowledge(action, "success", pack, projection, intent, tick),
    )


def _inspect(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """examine: exact details on a passed perception check, vague on failure."""
    branch = _branch(check, action)
    return Resolution(
        event_type=action["events"][branch],
        outcome={"check": _check_outcome(check)},
        knowledge=_knowledge(action, branch, pack, projection, intent, tick),
    )


def _movement(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """move: adjacency was a precondition; carry the items along."""
    if intent.target is None:
        raise RunnerError("move requires a target location")
    return Resolution(
        event_type=action["events"]["success"],
        outcome={},
        state_changes=_move_changes(pack, projection, intent.actor, intent.target),
    )


def _converse(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """talk: both parties remember the conversation (or the rebuff)."""
    branch = _branch(check, action)
    return Resolution(
        event_type=action["events"][branch],
        outcome={"check": _check_outcome(check)},
        knowledge=_knowledge(action, branch, pack, projection, intent, tick),
    )


def _wait(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """wait: time passes, nothing else (the world moves via passes)."""
    return Resolution(event_type=action["events"]["success"], outcome={})


def _pickup(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """take: an uncarried present item changes carrier; a failed stealth
    check is noticed (records for everyone watching)."""
    if intent.target is None:
        raise RunnerError("take requires a target item")
    branch = _branch(check, action)
    if branch == "success":
        changes = (
            StateChange(
                entity=intent.target, prop="carrier",
                from_=None, to_=intent.actor,
            ),
        )
        return Resolution(
            event_type=action["events"]["success"],
            outcome={"check": _check_outcome(check)},
            state_changes=changes,
        )
    return Resolution(
        event_type=action["events"]["failure"],
        outcome={"check": _check_outcome(check)},
        knowledge=_knowledge(action, branch, pack, projection, intent, tick),
        hooks=_hooks(action, branch),
    )


def _drop(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """drop_break: release the item, break it if breakable (noise), and
    roll the pack ignition chance when a fire source lands at a spot."""
    if intent.target is None:
        raise RunnerError("drop_break requires a target item")
    item = pack.entity(intent.target)
    location = projection[intent.actor]["position"]
    changes = [
        StateChange(
            entity=intent.target, prop="carrier",
            from_=intent.actor, to_=None,
        )
    ]
    broken = bool(item.get("breakable"))
    if broken:
        changes.append(
            StateChange(entity=intent.target, prop="condition", from_=None, to_="broken")
        )

    ignitions: tuple[Ignition, ...] = ()
    config = action.get("ignition")
    near = intent.fields.get("near")
    if config is not None and near is not None:
        layer_cfg = pack.rules["transitions"][config["layer"]]
        spots = pack.entity(location).get(layer_cfg["spot_field"], [])
        if near not in spots:
            raise RunnerError(
                f"drop_break 'near' must be a {location!r} spot of the pack, "
                f"got {near!r} (spots: {spots})"
            )
        flammable = pack.entity(location).get("flammability")
        if (
            item.get(config["item_flag"])
            and flammable in layer_cfg["ignition"]["requires_flammability"]
            and bank.random() <= layer_cfg["ignition"]["chance_on_drop_break"]
        ):
            ignitions = (Ignition(layer=config["layer"], location=location, spot=near),)

    return Resolution(
        event_type=action["events"]["success"],
        outcome={"broken": broken},
        knowledge=_knowledge(action, "success", pack, projection, intent, tick),
        state_changes=tuple(changes),
        ignitions=ignitions,
    )


def _use_item(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """use: apply the item's pack `use_effect` (a status delta) on success."""
    branch = _branch(check, action)
    changes: tuple[StateChange, ...] = ()
    if branch == "success" and intent.target is not None:
        effect = pack.entity(intent.target)["use_effect"]
        prop = f"status.{effect['status']}"
        current = projection[intent.actor].get(prop, 0)
        scale_max = pack.rules["relations"]["scale"][1]
        changes = (
            StateChange(
                entity=intent.actor, prop=prop, from_=current,
                to_=max(0, min(scale_max, current + effect["delta"])),
            ),
        )
    return Resolution(
        event_type=action["events"][branch],
        outcome={"check": _check_outcome(check)},
        knowledge=_knowledge(action, branch, pack, projection, intent, tick),
        state_changes=changes,
    )


def _stealth_take(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """steal: lift the target's flagged item unseen — or produce the
    ev_0007 record family (target saw, others heard; total failure adds
    everyone's sighting) with the document-check hooks seeded."""
    if intent.target is None:
        raise RunnerError("steal requires a target npc")
    flag = next(
        cond["flag"] for cond in action["requires"] if cond["test"] == "carries_flagged"
    )
    branch = _branch(check, action)
    if branch == "success":
        item = find_flagged_carried(pack, projection, intent.target, flag)
        if item is None:
            # Unreachable by construction: the OCC re-check rejects a broken
            # precondition before the resolver runs. Loud, not silent.
            raise RunnerError(
                f"steal target {intent.target} carries no flagged item at completion"
            )
        return Resolution(
            event_type=action["events"]["success"],
            outcome={"check": _check_outcome(check), "stolen": item},
            state_changes=(
                StateChange(
                    entity=item, prop="carrier",
                    from_=intent.target, to_=intent.actor,
                ),
            ),
        )
    return Resolution(
        event_type=action["events"]["failure"],
        outcome={"check": _check_outcome(check)},
        knowledge=_knowledge(action, branch, pack, projection, intent, tick),
        hooks=_hooks(action, branch),
    )


def _divert(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """distract: on success the target's attention turns (a perception
    modifier via the pack skill table); on failure the target ignores."""
    if intent.target is None:
        raise RunnerError("distract requires a target npc")
    branch = _branch(check, action)
    changes: tuple[StateChange, ...] = ()
    if branch == "success":
        changes = (
            StateChange(
                entity=intent.target, prop="status.attention",
                from_=projection[intent.target].get("status.attention"),
                to_="distracted",
            ),
        )
    return Resolution(
        event_type=action["events"][branch],
        outcome={"check": _check_outcome(check)},
        knowledge=_knowledge(action, branch, pack, projection, intent, tick),
        state_changes=changes,
    )


def _ignite_action(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """The ignite resolver: the actor's own location burns — the source
    item is reachable (precondition), the first unburning spot ignites
    (T5 at the front door, T4 in the chain that follows)."""
    config = action["ignition"]
    layer_cfg = pack.rules["transitions"][config["layer"]]
    actor_location = location_of(pack, projection, intent.actor)
    source = find_flagged_accessible(
        pack, projection, intent.actor, config["item_flag"]
    )
    spots = pack.entity(actor_location).get(layer_cfg["spot_field"], [])
    spot = next(
        (s for s in spots if projection[actor_location].get(f"{config['layer']}.{s}")
         != "burning"),
        None,
    )
    ignitions = (
        (Ignition(layer=config["layer"], location=actor_location, spot=spot),)
        if spot is not None
        else ()
    )
    return Resolution(
        event_type=action["events"]["success"],
        outcome={"source": source, "spot": spot},
        knowledge=_knowledge(action, "success", pack, projection, intent, tick),
        ignitions=ignitions,
    )


def _flee(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """flee: opposed evasion vs the best pursuit present; success moves
    the actor (items along), failure leaves them caught in place."""
    if intent.target is None:
        raise RunnerError("flee requires a target location")
    branch = _branch(check, action)
    if branch == "success":
        return Resolution(
            event_type=action["events"]["success"],
            outcome={"check": _check_outcome(check)},
            knowledge=_knowledge(action, "success", pack, projection, intent, tick),
            state_changes=_move_changes(pack, projection, intent.actor, intent.target),
        )
    return Resolution(
        event_type=action["events"]["failure"],
        outcome={"check": _check_outcome(check)},
        knowledge=_knowledge(action, branch, pack, projection, intent, tick),
    )


REGISTRY: Final[dict[str, ResolverFn]] = {
    "observe": _observe,
    "inspect": _inspect,
    "movement": _movement,
    "converse": _converse,
    "wait": _wait,
    "pickup": _pickup,
    "drop": _drop,
    "use_item": _use_item,
    "stealth_take": _stealth_take,
    "divert": _divert,
    "ignite": _ignite_action,
    "flee": _flee,
}
