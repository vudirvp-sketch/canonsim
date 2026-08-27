"""The intent contract (INTENT_SCHEMA.md is the doc owner): an Intent is a
*proposal*, never an event (phase0 §2). This module owns the generic
machinery the front door runs:

- loud shape validation (author errors raise; the world can never be blamed
  for a malformed playscript step) vs soft precondition evaluation
  (a well-formed but world-impossible intent is REJECTED with a no-op
  event, never silently dropped, never an exception);
- the closed precondition test set — structured filters, no string
  expression language (L10); the pack references tests by name (INV-3);
- opposed checks: skill base + status modifiers + die, from `rules.json`
  `checks` — every number is pack data;
- intent OCC (`based_on_event_seq`): cause attribution for the event that
  broke a precondition between proposal and completion;
- knowledge-record resolution: audience placeholders + slot templates are
  pack data; the resolver of record is `core/resolvers.py`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.fold import Projection, fold
from core.log import EventRecord, KnowledgeRecord, StateChange
from core.rng import RngBank

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle with pack.py
    from core.pack import Pack

__all__ = [
    "AUDIENCES",
    "CheckResult",
    "IntentData",
    "KNOWLEDGE_SLOTS",
    "PRECONDITION_TESTS",
    "REJECTION_EVENT",
    "Resolution",
    "RunnerError",
    "action_duration",
    "first_failing",
    "find_flagged_accessible",
    "find_flagged_carried",
    "knowers_at",
    "location_of",
    "occ_breaking_cause",
    "pack_importance",
    "resolve_knowledge",
    "run_check",
    "skill_total",
    "validate_shape",
]

REJECTION_EVENT: Final = "intent_rejected"  # pack vocabulary (lint-checked)


class RunnerError(RuntimeError):
    """Run-time violation: unknown intent, malformed step, broken contract."""


@dataclass(frozen=True, slots=True)
class IntentData:
    """One playscript intent: a proposal, not yet an event (INTENT_SCHEMA §2)."""

    id: str
    kind: str
    actor: str
    target: str | None
    fields: Mapping[str, Any]
    based_on_event_seq: int = 0


@dataclass(frozen=True, slots=True)
class CheckResult:
    """One opposed check resolution (INTENT_SCHEMA §5). `margin` is the
    defender's lead (>= 0 on failure); `total_failure` marks the margin
    band `rules.checks.failure_margin` and above."""

    passed: bool
    margin: int
    attacker_total: int
    defender_total: int
    defender_id: str | None
    total_failure: bool = False


@dataclass(frozen=True, slots=True)
class Resolution:
    """A resolver's decision at completion: which event to emit and what
    the world looks like afterwards. `ignitions` are world reactions the
    loop executes after the primary event (transition layers)."""

    event_type: str
    outcome: Mapping[str, Any]
    knowledge: tuple[KnowledgeRecord, ...] = ()
    state_changes: tuple[StateChange, ...] = ()
    hooks: tuple[str, ...] = ()
    ignitions: tuple[Any, ...] = ()  # transition.Ignition (type-avoided: no cycle)


# -- shape validation (loud) -------------------------------------------------


def validate_shape(action: Mapping[str, Any], intent: IntentData) -> None:
    """Author errors are loud: unknown fields, missing target where the
    preconditions need one. World impossibility is NOT checked here."""
    allowed = set(action.get("fields", ()))
    extras = set(intent.fields) - allowed
    if extras:
        raise RunnerError(
            f"{intent.kind} takes no step fields {sorted(extras)}; "
            f"allowed: {sorted(allowed)}"
        )
    needs_target = any(
        value == "target" for cond in action.get("requires", ()) for value in cond.values()
    )
    if needs_target and intent.target is None:
        raise RunnerError(f"{intent.kind} requires a target")


def action_duration(
    action: Mapping[str, Any], bank: RngBank, intent: IntentData
) -> int:
    """Duration at accept time: fixed int, a drawn range, or the caller's
    'ticks' field for the 'N' actions (MVP_SCOPE §7)."""
    ticks = action["ticks"]
    if isinstance(ticks, Mapping):
        return bank.randint(ticks["min"], ticks["max"])
    if isinstance(ticks, int):
        return ticks
    value = intent.fields.get("ticks")  # ticks == "N"
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise RunnerError(
            f"{intent.kind} requires a positive integer 'ticks' step field, got {value!r}"
        )
    return value


# -- preconditions (soft; the closed test set, INV-3) ------------------------


class _Ctx:
    """Evaluation context: pack + projection + the intent's nouns."""

    def __init__(self, pack: Pack, projection: Projection, intent: IntentData) -> None:
        self.pack = pack
        self.projection = projection
        self.intent = intent

    def entity(self, noun: str) -> str:
        if noun == "actor":
            return self.intent.actor
        if noun == "target":
            if self.intent.target is None:
                raise RunnerError(f"precondition references {noun!r} without a target")
            return self.intent.target
        raise RunnerError(f"unknown noun {noun!r} (actor | target)")


def location_of(pack: Pack, projection: Projection, entity_id: str) -> str:
    """The location an entity is at; a location is at itself."""
    if pack.kind_of(entity_id) == "location":
        return entity_id
    return projection[entity_id]["position"]


def _test_kind(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    return ctx.pack.kind_of(ctx.entity(cond["noun"])) == cond["is"]


def _test_same_location(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    left = location_of(ctx.pack, ctx.projection, ctx.entity(cond["noun"]))
    right = location_of(ctx.pack, ctx.projection, ctx.entity(cond["with"]))
    return left == right


def _test_adjacent_to(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    noun_location = location_of(ctx.pack, ctx.projection, ctx.entity(cond["noun"]))
    base = location_of(ctx.pack, ctx.projection, ctx.entity(cond["with"]))
    return noun_location in ctx.pack.entity(base)["exits"]


def _test_location_of(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    noun = ctx.entity(cond["noun"])
    return ctx.pack.kind_of(noun) == "location" and noun == location_of(
        ctx.pack, ctx.projection, ctx.entity(cond["with"])
    )


def _test_flag(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    record = ctx.pack.entity(ctx.entity(cond["noun"]))
    return bool(record.get(cond["flag"]))


def _test_field_in(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    record = ctx.pack.entity(ctx.entity(cond["noun"]))
    return record.get(cond["field"]) in cond["values"]


def _test_field_nonempty(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    record = ctx.pack.entity(ctx.entity(cond["noun"]))
    value = record.get(cond["field"])
    return isinstance(value, list) and len(value) > 0


def _test_carries_flagged(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    return (
        find_flagged_carried(
            ctx.pack, ctx.projection, ctx.entity(cond["noun"]), cond["flag"]
        )
        is not None
    )


def _test_flagged_accessible(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    return (
        find_flagged_accessible(
            ctx.pack, ctx.projection, ctx.entity(cond["noun"]), cond["flag"]
        )
        is not None
    )


def _test_relation_at_least(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    value = ctx.projection[ctx.entity(cond["noun"])].get(f"relations.{cond['axis']}")
    return isinstance(value, int) and value >= cond["value"]


def _test_carried_by(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    item = ctx.entity(cond["noun"])
    return ctx.projection[item].get("carrier") == ctx.entity(cond["who"])


def _test_uncarried(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    return ctx.projection[ctx.entity(cond["noun"])].get("carrier") is None


def _test_has_field(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    return cond["field"] in ctx.pack.entity(ctx.entity(cond["noun"]))


PRECONDITION_TESTS: Final[Mapping[str, Any]] = {
    "kind": _test_kind,
    "same_location": _test_same_location,
    "adjacent_to": _test_adjacent_to,
    "location_of": _test_location_of,
    "flag": _test_flag,
    "field_in": _test_field_in,
    "field_nonempty": _test_field_nonempty,
    "carries_flagged": _test_carries_flagged,
    "flagged_accessible": _test_flagged_accessible,
    "relation_at_least": _test_relation_at_least,
    "carried_by": _test_carried_by,
    "uncarried": _test_uncarried,
    "has_field": _test_has_field,
}


def first_failing(
    pack: Pack,
    projection: Projection,
    intent: IntentData,
    preconditions: list[Mapping[str, Any]],
) -> str | None:
    """The first failing condition as '<noun>.<test>', or None when the
    intent is executable. Soft: callers record a no-op rejection event."""
    ctx = _Ctx(pack, projection, intent)
    for cond in preconditions:
        test = PRECONDITION_TESTS.get(cond["test"])
        if test is None:
            raise RunnerError(f"unknown precondition test {cond['test']!r}")
        if not test(ctx, cond):
            return f"{cond['noun']}.{cond['test']}"
    return None


# -- flagged-item lookups (shared by preconditions and resolvers) -------------


def find_flagged_carried(
    pack: Pack, projection: Projection, holder: str, flag: str
) -> str | None:
    """The first item (pack order) carried by `holder` whose pack record
    carries `flag` — the steal target lookup."""
    for item in pack.entities["items"]:
        if projection[item["id"]].get("carrier") == holder and item.get(flag):
            return item["id"]
    return None


def find_flagged_accessible(
    pack: Pack, projection: Projection, entity_id: str, flag: str
) -> str | None:
    """The first flagged item the entity carries or that lies in its
    location — the fire-source availability lookup."""
    location = location_of(pack, projection, entity_id)
    for item in pack.entities["items"]:
        if not item.get(flag):
            continue
        if projection[item["id"]].get("carrier") == entity_id:
            return item["id"]
        if projection[item["id"]]["position"] == location:
            return item["id"]
    return None


# -- opposed checks (every number is pack data) -------------------------------


def _modifier_value(mod: Mapping[str, Any], value: Any) -> int:
    """One status-modifier entry (rules.checks.skills.<skill>.status_modifiers):
    per_10_points | flat (nonzero numeric) | flat_at_least+flat | flat_when+flat."""
    if "per_10_points" in mod and isinstance(value, (int, float)):
        return (value // 10) * mod["per_10_points"]
    if "flat_when" in mod:
        return mod["flat"] if value == mod["flat_when"] else 0
    if "flat_at_least" in mod and isinstance(value, (int, float)):
        return mod["flat"] if value >= mod["flat_at_least"] else 0
    if "flat" in mod and isinstance(value, (int, float)) and value != 0:
        return mod["flat"]
    return 0


def skill_total(
    pack: Pack, projection: Projection, entity_id: str, skill: str
) -> int:
    """Skill base plus status modifiers — system 5 feeding checks (EPIST-1:
    modifiers ride the perceiver's own status, never another entity's)."""
    checks = pack.rules["checks"]
    config = checks["skills"][skill]
    total: int = config["base"]
    for axis, mod in sorted(config.get("status_modifiers", {}).items()):
        value = projection.get(entity_id, {}).get(f"status.{axis}")
        if value is not None:
            total += _modifier_value(mod, value)
    return total


def _best_in_location(
    pack: Pack, projection: Projection, actor: str, skill: str
) -> str | None:
    """The strongest opposing entity (npc or ambient group, never an item)
    at the actor's location, excluding the actor; ties break by pack order."""
    location = projection[actor]["position"]
    best_id: str | None = None
    best_total = -1
    for group in ("npcs", "ambient_entities"):
        for record in pack.entities[group]:
            entity_id = record["id"]
            if entity_id == actor or projection[entity_id]["position"] != location:
                continue
            total = skill_total(pack, projection, entity_id, skill)
            if total > best_total:
                best_id, best_total = entity_id, total
    return best_id


def run_check(
    pack: Pack,
    projection: Projection,
    bank: RngBank,
    intent: IntentData,
    action: Mapping[str, Any],
) -> CheckResult | None:
    """Resolve the action's opposed check; None = no check (or no opposing
    entity — automatic). Draws come from the active (substantive) stream."""
    spec = action.get("check")
    if spec is None:
        return None
    checks = pack.rules["checks"]
    kind = checks["kinds"][spec["kind"]]
    die: int = checks["die"]
    margin_rule: int = checks["failure_margin"]

    attacker = skill_total(pack, projection, intent.actor, kind["attack"])
    attacker_total = attacker + bank.randint(1, die)

    defender_id: str | None = None
    defender = int(spec["difficulty"])
    source = kind["defender_source"]
    if source == "target":
        defender_id = intent.target
        defender = skill_total(pack, projection, defender_id, kind["defend"])
    elif source == "best_in_location":
        defender_id = _best_in_location(
            pack, projection, intent.actor, kind["defend"]
        )
        if defender_id is None:
            return None  # nobody to oppose — the attempt is unopposed
        defender = skill_total(pack, projection, defender_id, kind["defend"])
    elif source != "environment":
        raise RunnerError(f"unknown defender_source {source!r}")

    defender_total = defender + bank.randint(1, die)
    method = intent.fields.get("method")
    if method is not None:
        if method not in checks["methods"]:
            raise RunnerError(f"unknown method {method!r} (rules.checks.methods)")
        defender_total += checks["methods"][method]["defender_modifier"]

    passed = attacker_total > defender_total  # tie -> defender (pack rule)
    margin = defender_total - attacker_total
    return CheckResult(
        passed=passed,
        margin=margin,
        attacker_total=attacker_total,
        defender_total=defender_total,
        defender_id=defender_id,
        total_failure=not passed and margin >= margin_rule,
    )


# -- intent OCC (based_on_event_seq, phase0 §2) --------------------------------


def occ_breaking_cause(
    pack: Pack,
    events: list[EventRecord],
    based_on_event_seq: int,
    intent: IntentData,
    initial: Projection,
) -> str | None:
    """The event id whose application first broke a precondition after the
    intent was proposed; None when nothing broke it. Folds forward from the
    initial projection (test-path machinery reused for attribution only)."""
    action = pack.action(intent.kind)
    preconditions = list(action.get("requires", ())) if action else []
    for idx in range(based_on_event_seq, len(events)):
        state = fold(events[: idx + 1], initial)
        if first_failing(pack, state, intent, preconditions) is not None:
            return events[idx].id
    return None


# -- the pack importance rule (MVP_SCOPE §9 — never by feel) -------------------


def pack_importance(
    rules: Mapping[str, Any],
    entities: set[str],
    irreversible: int,
    hooks: int,
) -> str:
    """Score = entities-touched + irreversibility + hooks, mapped through
    the pack's thresholds. One rule for action events and world events."""
    score_rule = rules["importance"]["score"]
    thresholds = rules["importance"]["thresholds"]
    score = 0
    if len(entities) >= 2:
        score += score_rule["entities_touched_at_least_2"]
    score += score_rule["irreversible_state_change"] * (1 if irreversible else 0)
    score += score_rule["per_far_hook"] * hooks
    if score >= thresholds["high"]:
        return "high"
    if score >= thresholds["medium"]:
        return "medium"
    return "low"


# -- knowledge-record resolution (audiences + slot templates) ------------------

AUDIENCES: Final = (
    "actor",
    "target",
    "same_location",
    "adjacent_locations",
    "destination_location",  # movement sightings at the arrival end (iter-3)
)
KNOWLEDGE_SLOTS: Final = ("actor", "target", "location", "cause_actor")


def knowers_at(pack: Pack, projection: Projection, location: str) -> list[str]:
    """Knowledge-holders at a location: npcs and ambient groups (pack order);
    items never know."""
    knowers: list[str] = []
    for group in ("npcs", "ambient_entities"):
        for record in pack.entities[group]:
            if projection[record["id"]]["position"] == location:
                knowers.append(record["id"])
    return knowers


def resolve_knowledge(
    records: list[Mapping[str, Any]],
    pack: Pack,
    projection: Projection,
    ctx: Mapping[str, Any],
    tick: int,
) -> tuple[KnowledgeRecord, ...]:
    """Turn pack knowledge templates into records: audience placeholders
    resolve to entity ids, `knows` slots fill from `ctx` (a missing slot
    fails loudly — the pack lint pre-checks the closed slot set)."""
    resolved: list[KnowledgeRecord] = []
    for record in records:
        audience = record["who"]
        if audience == "actor":
            who_ids = [ctx["actor"]]
        elif audience == "target":
            who_ids = [ctx["target"]]
        elif audience == "same_location":
            who_ids = knowers_at(pack, projection, ctx["location"])
        elif audience == "adjacent_locations":
            who_ids = []
            exits = pack.entity(ctx["location"])["exits"]
            for adjacent in exits:  # pack exit order — deterministic
                who_ids.extend(knowers_at(pack, projection, adjacent))
        elif audience == "destination_location":
            destination = ctx["target"]
            if pack.kind_of(destination) != "location":
                raise RunnerError(
                    f"knowledge audience 'destination_location' resolves against a "
                    f"location target, got {destination!r}"
                )
            who_ids = knowers_at(pack, projection, destination)
        else:
            raise RunnerError(f"unknown knowledge audience {audience!r}")
        knows = record["knows"].format_map(ctx)
        except_ids = {
            ctx[token]
            for token in record.get("except", ())  # actor | target | cause_actor
            if ctx.get(token) is not None
        }
        for who in who_ids:
            if who in except_ids:
                continue
            resolved.append(
                KnowledgeRecord(
                    who=who,
                    channel=record["channel"],
                    fidelity=record["fidelity"],
                    knows=knows,
                    at=tick,
                )
            )
    return tuple(resolved)
