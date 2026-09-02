"""The ActionResolver registry (phase0 §2, D-031): pack data references
resolvers by name; each resolver is a generic mechanic — no domain words
(INV-3, enforced by the stoplist test). Phase 0 landed the 12 actions of
`MVP_SCOPE.md` §7; the registry grows only with a new MECHANIC (tune-1:
`recuperate` — pack-declared actor status effects, the fatigue
counter-play; iter-45: `coerce` — pack-declared subject-directed pair
shifts, the leverage spend), never for a setting noun.

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
    texture_reference,
    texture_scope_target,
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


def _texture_ctx(
    intent: IntentData, projection: Projection
) -> dict[str, Any]:
    """The knowledge context for a texture-path resolution: no canon
    target (the reference carries the slot instead — the pack lint forbids
    the {target} slot in texture-block templates)."""
    ctx = _ctx(intent, projection)
    ctx["texture_slot"] = texture_reference(intent)["slot"]
    return ctx


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


def _texture_knowledge(
    action: Mapping[str, Any],
    branch: str,
    pack: Pack,
    projection: Projection,
    intent: IntentData,
    tick: int,
) -> tuple[Any, ...]:
    """Texture-path knowledge: the action's `texture.knowledge` templates
    with the texture context (the slot replaces the absent target)."""
    templates = action["texture"]["knowledge"].get(branch, [])
    return resolve_knowledge(
        templates, pack, projection, _texture_ctx(intent, projection), tick
    )


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


def movement_changes(
    pack: Pack, projection: Projection, actor: str, destination: str
) -> tuple[StateChange, ...]:
    """The actor's position delta plus every carried item's (items travel
    with their carrier — the position contract every mover obeys: a
    carried item's position == its carrier's, or the next move's `from_`
    desyncs loudly in `apply_event`). The single owner of the law; the
    watch rotation reuses it (KI#46: the rotation once left carried
    items behind, and the st-1 presence fold surfaced the lie)."""
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


# -- the resolvers --------------------------------------------------------------


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
    """move: adjacency was a precondition; carry the items along. Knowledge
    resolves against the PRE-move projection: origin observers see the
    departure (same_location), destination observers the arrival
    (destination_location) — the movement sighting records (iter-3)."""
    if intent.target is None:
        raise RunnerError("move requires a target location")
    return Resolution(
        event_type=action["events"]["success"],
        outcome={},
        knowledge=_knowledge(action, "success", pack, projection, intent, tick),
        state_changes=movement_changes(pack, projection, intent.actor, intent.target),
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
    check is noticed (records for everyone watching).

    The texture path (iter-11, blueprint §1 promotion): the intent carries
    the mediator-resolved texture reference; on success the committed
    event IS the promotion — the slot's canon birth as a prop on the scope
    target (from_ None: the gateway guarantees canon never modeled it, and
    a mid-flight canon birth would have retired the entry → withdrawal).
    The outcome carries the reference so the mediator can mark_promoted;
    a failed attempt promotes nothing (the entry stays live+pinned)."""
    if "texture" in intent.fields:
        return _pickup_texture(pack, projection, intent, action, check, tick)
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


def _pickup_texture(
    pack: Pack, projection: Projection, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """The promotion resolution: take on a resolved texture reference.

    Canon birth = the scope target gains the slot as a canon prop holding
    the texture's value (apply_event accepts an absent prop from None —
    locations and npcs are registered prop-less). From that moment the
    gateway's canon-slot check outranks any texture on the slot (canon
    always outranks texture, D-049), and the mediator flips the entry to
    `promoted` on observing this event. Fire-chain ignition composition
    (the knocked-over candle) stays with the pack's existing hook/ignition
    consumers of the promoted prop — deliberately not re-implemented here."""
    reference = texture_reference(intent)
    target = texture_scope_target(pack, intent)
    branch = _branch(check, action)
    outcome: dict[str, Any] = {"check": _check_outcome(check), "texture": dict(reference)}
    if branch == "success":
        return Resolution(
            event_type=action["events"]["success"],
            outcome=outcome,
            knowledge=_texture_knowledge(action, "success", pack, projection, intent, tick),
            state_changes=(
                StateChange(
                    entity=target, prop=str(reference["slot"]),
                    from_=None, to_=reference["value"],
                ),
            ),
        )
    return Resolution(
        event_type=action["events"]["failure"],
        outcome=outcome,
        knowledge=_texture_knowledge(action, branch, pack, projection, intent, tick),
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
    # Idempotent (KI#13): an already-broken item re-dropped after a retake
    # carries no second condition change — from_ is never hardcoded against
    # a moved projection. The noise still happens; the break happens once.
    if broken and projection[intent.target].get("condition") != "broken":
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
    try:
        flag = next(
            cond["flag"] for cond in action["requires"]
            if cond["test"] == "carries_flagged"
        )
    except StopIteration:
        # KI#15: pack data dropped the precondition the resolver keys on —
        # a loud contract error, never a bare StopIteration.
        raise RunnerError(
            f"{intent.kind}: the stealth_take resolver requires a "
            f"carries_flagged precondition to find the item"
        ) from None
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
        event_type=action["events"][branch],
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
         != layer_cfg["spot_state"]),
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
            state_changes=movement_changes(pack, projection, intent.actor, intent.target),
        )
    return Resolution(
        event_type=action["events"]["failure"],
        outcome={"check": _check_outcome(check)},
        knowledge=_knowledge(action, branch, pack, projection, intent, tick),
    )


def _recuperate(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """The pack-declared actor status effects (tune-1, KI#4): the action
    carries a `status_effects` list ({status, delta}); each effect reads
    the CURRENT value from the projection (KI#13 — `from` is never
    hardcoded) and clamps to the pack's relation scale. A clamped-to-zero
    delta emits no StateChange (resting at fatigue 0 is a legal quiet
    beat — the same no-op discipline as the decay pass), never a
    desynced write the `_commit` gate would have to refuse."""
    branch = _branch(check, action)
    changes: list[StateChange] = []
    if branch == "success":
        scale = pack.rules["relations"]["scale"]
        for effect in action["status_effects"]:
            prop = f"status.{effect['status']}"
            current = projection[intent.actor].get(prop, 0)
            target = max(scale[0], min(scale[1], current + effect["delta"]))
            if target != current:
                changes.append(
                    StateChange(
                        entity=intent.actor, prop=prop,
                        from_=current, to_=target,
                    )
                )
    return Resolution(
        event_type=action["events"][branch],
        outcome={"check": _check_outcome(check)},
        knowledge=_knowledge(action, branch, pack, projection, intent, tick),
        state_changes=tuple(changes),
    )


def _coerce(
    pack: Pack, projection: Projection, bank: RngBank, intent: IntentData,
    action: Mapping[str, Any], check: CheckResult | None, tick: int,
) -> Resolution:
    """coerce (social-1b, iter-45): spend the live fact cluster over the
    target. The resolver is the BALANCE half only — the pack-declared
    pair-axis shifts landing on the SUBJECT toward the actor ({axis,
    delta}, one directed `pair.<actor>.<axis>` prop each; an absent pair
    axis starts from the pack's neutral — the `trust_toward` read law,
    materialized by the write). The loop stamps the CLUSTER half at
    commit: the event names the spent fact's id in `outcome.cluster`
    (from the live fold — the log's only view of the fact, never a
    resolver-side mutation). A clamped-to-unchanged delta emits no
    StateChange (the rest/decay quiet-beat discipline); `from` is read
    from the projection, never hardcoded (KI#13)."""
    if intent.target is None:
        raise RunnerError("coerce requires a target npc")
    relations = pack.rules["relations"]
    scale = relations["scale"]
    neutral = int(relations["neutral"])
    changes: list[StateChange] = []
    for effect in action["balance"]:
        prop = f"pair.{intent.actor}.{effect['axis']}"
        current = projection[intent.target].get(prop)
        base = neutral if current is None else int(current)
        shifted = max(scale[0], min(scale[1], base + int(effect["delta"])))
        if shifted != current:
            changes.append(
                StateChange(
                    entity=intent.target, prop=prop,
                    from_=current, to_=shifted,
                )
            )
    return Resolution(
        event_type=action["events"]["success"],
        outcome={},  # the loop stamps cluster/secret/type from the live fold
        knowledge=_knowledge(action, "success", pack, projection, intent, tick),
        state_changes=tuple(changes),
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
    "recuperate": _recuperate,
    "coerce": _coerce,
}
