"""The intent contract (INTENT_SCHEMA.md is the doc owner): an Intent is a
*proposal*, never an event (phase0 §2). This module owns the generic
machinery the front door runs:

- loud shape validation (author errors raise; the world can never be blamed
  for a malformed playscript step) vs soft precondition evaluation
  (a well-formed but world-impossible intent is REJECTED with a no-op
  event, never silently dropped, never an exception);
- the closed precondition test set — structured filters, no string
  expression language (L10); the pack references tests by name (INV-3);
  the texture path: a texture-capable action's `texture` block replaces the
  canon `requires` for intents carrying a resolved texture reference (the
  grammar/vocabulary split, D-049 — the pack owns WHICH actions are
  texture-capable; the ledger owns which nouns are addressable, and that
  lives outside core: core stays ledger-blind, the Intent carries the
  resolved slot as data);
- opposed checks: skill base + status modifiers + die, from `rules.json`
  `checks` — every number is pack data;
- intent OCC (`based_on_event_seq`): cause attribution for the event that
  broke a precondition between proposal and completion;
- knowledge-record resolution: audience placeholders + slot templates are
  pack data; the resolver of record is `core/resolvers.py`; the
  per-present-target expansion (st-1): an actor-held template with a
  `present_at` site expands to one record per entity present there —
  the arrival snapshot's write side (blueprint §5).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.fold import Projection, apply_event, fold, present_in_order
from core.log import EventRecord, KnowledgeRecord, StateChange
from core.rng import RngBank

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle with pack.py
    from core.pack import Pack

__all__ = [
    "AUDIENCES",
    "CheckResult",
    "ECHO_TEST",
    "IntentData",
    "KNOWLEDGE_SLOTS",
    "LEVERAGE_TEST",
    "PRECONDITION_TESTS",
    "REJECTION_EVENT",
    "Resolution",
    "RunnerError",
    "TEXTURE_FIELD",
    "TEXTURE_SCOPES",
    "WINDOWED_TESTS",
    "action_duration",
    "first_failing",
    "find_flagged_accessible",
    "find_flagged_carried",
    "knowers_at",
    "location_of",
    "occ_breaking_cause",
    "pack_importance",
    "requires_for",
    "resolve_knowledge",
    "run_check",
    "skill_total",
    "texture_reference",
    "texture_scope_target",
    "validate_shape",
]

REJECTION_EVENT: Final = "intent_rejected"  # pack vocabulary (lint-checked)

#: The intent door's first leverage test (social-1b, iter-45): the actor
#: holds live leverage over `who`. The name is this module's vocabulary
#: (the closed test set's owner); `core/leverage.py` reads it for the
#: spend machinery — the import direction stays one-way (leverage →
#: intent), so the facts themselves are duck-typed below.
LEVERAGE_TEST: Final = "leverage_over"

#: The intent door's echo test (social-2, iter-46): the noun entity's
#: psychological residue on `axis` is at least `value` — the P2b
#: behavior gate over the per-NPC valence fold. Same discipline as the
#: leverage test: the scores arrive as duck-typed data
#: (`core.echo.echo_scores` read at the caller's own tick); this module
#: never imports `core.echo` (the import direction stays one-way).
ECHO_TEST: Final = "echo_at_least"

#: The tick-windowed precondition family — tests whose truth is driven
#: by TIME, not by event application (the leverage liveness window,
#: the echo decay). Two laws ride this name: the OCC re-check runs
#: UNCONDITIONAL for intents carrying one (the window can move between
#: accept and completion with no event committed), and
#: `occ_breaking_cause` excludes them (a window close never attributes
#: a breaking event the log does not hold).
WINDOWED_TESTS: Final = (LEVERAGE_TEST, ECHO_TEST)

#: The intent field carrying a resolved texture reference (INTENT_SCHEMA §2;
#: blueprint §1 D-049: the mediator resolves noun -> live entry BEFORE the
#: door, so the Intent carries the resolved slot as data and core never
#: sees the ledger).
TEXTURE_FIELD: Final = "texture"
#: The texture-reference scope prefixes — the same pair the ledger's
#: `split_scope` owns (brief/ledger.py); restated here only as the intent
#: field's shape contract (core may not import brief — D-031).
TEXTURE_SCOPES: Final = ("scene:", "entity:")


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


def _carries_texture(intent: IntentData) -> bool:
    return TEXTURE_FIELD in intent.fields


def texture_reference(intent: IntentData) -> Mapping[str, Any]:
    """The resolved texture reference from the intent's `texture` field:
    `{entry, scope, slot, value}` — the mediator's noun-resolution output.

    Loud on a malformed reference (the emitter is the mediator or a
    playscript author, and author bugs crash): every key a non-empty
    string, the scope one of the two ledger prefixes. Returns the mapping
    as-is when well-formed; core NEVER checks ledger liveness — the
    withdrawal mirror (VALIDATION_SPEC §8) owns that, mediator-side.
    """
    value = intent.fields.get(TEXTURE_FIELD)
    if not isinstance(value, Mapping):
        raise RunnerError(
            f"{intent.kind}: field 'texture' must be the mediator's resolved "
            f"reference object, got {value!r}"
        )
    missing = {"entry", "scope", "slot", "value"} - set(value)
    if missing:
        raise RunnerError(
            f"{intent.kind}: texture reference missing keys {sorted(missing)}"
        )
    for key in ("entry", "scope", "slot", "value"):
        if not isinstance(value[key], str) or not value[key].strip():
            raise RunnerError(
                f"{intent.kind}: texture reference {key} must be a non-empty "
                f"string, got {value[key]!r}"
            )
    if not value["scope"].startswith(TEXTURE_SCOPES):
        raise RunnerError(
            f"{intent.kind}: texture scope must be 'scene:<id>' or 'entity:<id>', "
            f"got {value['scope']!r}"
        )
    if not value["scope"].split(":", 1)[1].strip():
        raise RunnerError(
            f"{intent.kind}: texture scope target is empty in {value['scope']!r}"
        )
    return value


def texture_scope_target(pack: Pack, intent: IntentData) -> str:
    """The canon entity id a texture-referencing intent acts on: the scope
    target (a location for scene scope, any other entity for entity scope).
    Loud when the target is not a known pack entity — the promotion's canon
    birth lands ON this entity, so it must exist."""
    reference = texture_reference(intent)
    target = str(reference["scope"]).split(":", 1)[1]
    if pack.kind_of(target) is None:
        raise RunnerError(
            f"{intent.kind}: texture scope target {target!r} is not a known entity"
        )
    return target


def requires_for(
    action: Mapping[str, Any], intent: IntentData
) -> list[Mapping[str, Any]]:
    """The precondition list this intent evaluates against: the action's
    `texture` block when the intent carries a resolved texture reference
    and the action declares itself texture-capable; the canon `requires`
    otherwise (blueprint §1 — the PACK owns which actions are texture-
    capable; validate_shape guarantees the pair is consistent)."""
    if _carries_texture(intent) and action.get("texture") is not None:
        return list(action["texture"].get("requires", ()))
    return list(action.get("requires", ()))


def validate_shape(action: Mapping[str, Any], intent: IntentData) -> None:
    """Author errors are loud: unknown fields, missing target where the
    preconditions need one, a texture reference on a non-texture action or
    a malformed one on a texture-capable action. World impossibility is
    NOT checked here."""
    allowed = set(action.get("fields", ()))
    extras = set(intent.fields) - allowed
    if extras:
        raise RunnerError(
            f"{intent.kind} takes no step fields {sorted(extras)}; "
            f"allowed: {sorted(allowed)}"
        )
    if _carries_texture(intent):
        if action.get("texture") is None:
            raise RunnerError(
                f"{intent.kind} is not texture-capable (no pack 'texture' block)"
            )
        texture_reference(intent)  # loud shape gate
        if intent.target is not None:
            raise RunnerError(
                f"{intent.kind}: the texture path carries the resolved reference, "
                f"not a target (got target {intent.target!r}) — an intent is one "
                f"path, never both"
            )
        return  # the texture block's requires reference no canon target
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
    """Evaluation context: pack + projection + the intent's nouns + the
    live leverage facts (iter-45) and echo scores (iter-46). Both are
    the caller's reads of the derived folds AT THE CALLER'S OWN TICK —
    the door at the entry tick, the urgency gate at the beat, the OCC
    re-check at completion: a tick-windowed precondition must be re-read
    at every evaluation, never cached. Both duck-typed (holder/subject
    and who/axis/score attributes) — core.intent never imports
    core.leverage or core.echo (the import direction is one-way; the
    owning modules own the fact types)."""

    def __init__(
        self,
        pack: Pack,
        projection: Projection,
        intent: IntentData,
        facts: Sequence[Any] = (),
        echoes: Sequence[Any] = (),
    ) -> None:
        self.pack = pack
        self.projection = projection
        self.intent = intent
        self.facts = facts
        self.echoes = echoes

    def entity(self, noun: str) -> str:
        if noun == "actor":
            return self.intent.actor
        if noun == "target":
            if self.intent.target is None:
                raise RunnerError(f"precondition references {noun!r} without a target")
            return self.intent.target
        if noun == "texture":
            # The texture noun resolves to the reference's scope target —
            # the canon entity the promotion lands on (blueprint §1).
            return texture_scope_target(self.pack, self.intent)
        raise RunnerError(f"unknown noun {noun!r} (actor | target | texture)")


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


def _test_texture_noun(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    """The texture-noun test (INTENT_SCHEMA §3): the intent carries a
    well-formed resolved reference whose scope target is a known entity.
    Ledger liveness is deliberately NOT tested — core is ledger-blind; the
    mediator resolved the noun against live entries and the withdrawal
    mirror owns mid-flight retirement (VALIDATION_SPEC §8)."""
    texture_scope_target(ctx.pack, ctx.intent)  # loud on malformed/unknown
    return True


def _test_leverage_over(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    """The intent door's first leverage test (social-1b, iter-45): the
    noun entity holds live leverage over `who` — some fact in the
    caller-supplied fold pairs them. The facts arrive as data (the
    caller's `live_leverage` read at its own tick); with no facts the
    test fails — nobody holds leverage over anyone, the door rejects.
    The pack lint requires the `who` param (a missing key would KeyError
    mid-run — the KI#15 family)."""
    return any(
        fact.holder == ctx.entity(cond["noun"])
        and fact.subject == ctx.entity(cond["who"])
        for fact in ctx.facts
    )


def _test_echo_at_least(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    """The intent door's echo test (social-2, iter-46): the noun entity's
    residue on `axis` is at least `value` — a score in the
    caller-supplied fold (read at the caller's own tick). With no
    scores the test fails — a silent world carries no residue, the
    behavior does not fire (the honest answer, never an error: a
    missing pair IS zero). The pack lint requires `axis` declared in
    the echo table and `value` within the scale (dead vocabulary is
    refused at load — the KI#15 family)."""
    return any(
        score.who == ctx.entity(cond["noun"])
        and score.axis == cond["axis"]
        and score.score >= cond["value"]
        for score in ctx.echoes
    )


def _test_spot_available(ctx: _Ctx, cond: Mapping[str, Any]) -> bool:
    """pack-2 (iter-29, D-061): the noun (a location) holds at least one
    spot of the pack-declared transition layer that is NOT in the layer's
    `spot_state` — the exact condition the ignite resolver keys on when
    it picks its spot, so the door check and the resolver agree by
    construction. Igniting a destroyed or fully-burning location is a
    door rejection, never a no-ignition success that pretends the world
    changed. The layer's vocabulary (`spot_field`, `spot_state`) is pack
    data — core stays layer-blind (INV-3)."""
    layer_cfg = ctx.pack.rules["transitions"][cond["layer"]]
    location = ctx.entity(cond["noun"])
    spots = ctx.pack.entity(location).get(layer_cfg["spot_field"], [])
    props = ctx.projection[location]
    prefix = f"{cond['layer']}."
    return any(
        props.get(f"{prefix}{spot}") != layer_cfg["spot_state"] for spot in spots
    )


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
    "texture_noun": _test_texture_noun,
    "spot_available": _test_spot_available,
    "leverage_over": _test_leverage_over,
    "echo_at_least": _test_echo_at_least,
}


def first_failing(
    pack: Pack,
    projection: Projection,
    intent: IntentData,
    preconditions: list[Mapping[str, Any]],
    facts: Sequence[Any] = (),
    echoes: Sequence[Any] = (),
) -> str | None:
    """The first failing condition as '<noun>.<test>', or None when the
    intent is executable. Soft: callers record a no-op rejection event.
    The caller passes the list from `requires_for` — canon or texture per
    the intent's path — and, when the list carries a tick-windowed test
    (`WINDOWED_TESTS`), the matching fold read at the caller's own tick
    (the leverage facts and/or the echo scores — the window law: a
    tick-driven precondition is never evaluated on stale reads)."""
    ctx = _Ctx(pack, projection, intent, facts, echoes)
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
    intent was proposed; None when nothing broke it. One forward fold from
    the proposal point (test-path machinery reused for attribution only):
    `fold` is a strict left fold over `apply_event`, so folding the prefix
    once and then applying one event at a time visits exactly the states
    the per-index refold used to rebuild — at O(events), not O(w·events)."""
    action = pack.action(intent.kind)
    preconditions = requires_for(action, intent) if action else []
    # Window preconditions (the tick-windowed family: the leverage
    # liveness window, the echo decay) never attribute a breaking
    # EVENT: their failure is tick-driven (the window closes by time,
    # not by an application). They are excluded from the attribution
    # fold — a window-close rejection chains to the last committed
    # event (the caller's fallback), never falsely to the first event
    # after the proposal (iter-45, social-1b; generalized to the family
    # at iter-46, social-2).
    attributable = [
        cond for cond in preconditions if cond.get("test") not in WINDOWED_TESTS
    ]
    state = fold(events[:based_on_event_seq], initial)
    for idx in range(based_on_event_seq, len(events)):
        apply_event(state, events[idx])
        if first_failing(pack, state, intent, attributable) is not None:
            return events[idx].id
    return None


# -- the pack importance rule (MVP_SCOPE §9 — never by feel) -------------------


def pack_importance(
    rules: Mapping[str, Any],
    entities: set[str],
    irreversible: int,
    hooks: int,
    event_type: str,
) -> str:
    """Score = entities-touched + irreversibility + far hooks + the
    story-critical hook, mapped through the pack's thresholds. One rule
    for action events and world events. The story-critical hook (tune-1,
    D-045(b)/D-059): event types the pack lists in
    `importance.story_critical_events` score their bonus — the rule, not
    the tale gate, owns the signal/noise split (a gate raise alone would
    cut story events the dumb rule scores low: a clean steal, a watch
    change)."""
    score_rule = rules["importance"]["score"]
    thresholds = rules["importance"]["thresholds"]
    score = 0
    if len(entities) >= 2:
        score += score_rule["entities_touched_at_least_2"]
    score += score_rule["irreversible_state_change"] * (1 if irreversible else 0)
    score += score_rule["per_far_hook"] * hooks
    if event_type in rules["importance"].get("story_critical_events", ()):
        score += score_rule["story_critical_event"]
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
KNOWLEDGE_SLOTS: Final = (
    "actor", "target", "location", "cause_actor",
    "texture_slot",  # the promoted texture's slot (iter-11; INTENT_SCHEMA §10
    # — additive slots are pack/code growth, no bump)
    "present",  # one present target per expansion record (st-1; only legal
    # with a `present_at` site — the pack lint pins the pairing)
)
# Where a per-present-target expansion may look (st-1, INTENT_SCHEMA §7):
# the actor's own location (completion time, pre-change) or the action's
# destination location. Pack data picks; core stays generic.
PRESENT_SITES: Final = ("location", "destination_location")


def knowers_at(pack: Pack, projection: Projection, location: str) -> list[str]:
    """Knowledge-holders at a location: npcs and ambient groups (pack order);
    items never know."""
    knowers: list[str] = []
    for group in ("npcs", "ambient_entities"):
        for record in pack.entities[group]:
            if projection[record["id"]]["position"] == location:
                knowers.append(record["id"])
    return knowers


def _expansion_site(
    record: Mapping[str, Any], pack: Pack, ctx: Mapping[str, Any]
) -> str:
    """The location a per-present-target expansion iterates (st-1,
    INTENT_SCHEMA §7): `destination_location` resolves against the
    action's target (location-kind, same law as the audience — the pack
    lint pre-checks the precondition), `location` against the actor's
    own position at completion time, pre-change."""
    site = record["present_at"]
    if site == "destination_location":
        destination = ctx["target"]
        if pack.kind_of(destination) != "location":
            raise RunnerError(
                f"knowledge expansion 'present_at=destination_location' resolves "
                f"against a location target, got {destination!r}"
            )
        return str(destination)
    return str(ctx["location"])


def resolve_knowledge(
    records: list[Mapping[str, Any]],
    pack: Pack,
    projection: Projection,
    ctx: Mapping[str, Any],
    tick: int,
) -> tuple[KnowledgeRecord, ...]:
    """Turn pack knowledge templates into records: audience placeholders
    resolve to entity ids, `knows` slots fill from `ctx` (a missing slot
    fails loudly — the pack lint pre-checks the closed slot set). A
    template with a `present_at` site takes the per-present-target
    expansion branch instead: the audience stays `actor`, and the
    template emits ONE record per entity present at the site (pack
    declaration order, the actor itself excluded) — the arrival
    snapshot's write side (blueprint §5; st-1)."""
    resolved: list[KnowledgeRecord] = []
    for record in records:
        if "present_at" in record:
            site = _expansion_site(record, pack, ctx)
            template_ctx = dict(ctx)
            for target_id in present_in_order(pack, projection, site):
                if target_id == ctx["actor"]:
                    continue  # the arriver knows their own presence
                template_ctx["present"] = target_id
                resolved.append(
                    KnowledgeRecord(
                        who=ctx["actor"],
                        channel=record["channel"],
                        fidelity=record["fidelity"],
                        knows=record["knows"].format_map(template_ctx),
                        at=tick,
                    )
                )
            continue
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
