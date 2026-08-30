"""Unit tests for the intent contract (core/intent.py): shape validation,
the closed precondition test set, opposed checks (skill totals, defender
sources, method modifiers), intent OCC cause attribution, knowledge
audience/slot resolution, and the pack importance rule.

The invariant these tests document: the front door separates author errors
(loud `RunnerError`) from world impossibility (soft rejection data) — and
every number the machinery uses comes from the pack (INV-3).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.fold import fold, initial_projection
from core.intent import (
    IntentData,
    RunnerError,
    action_duration,
    find_flagged_accessible,
    find_flagged_carried,
    first_failing,
    knowers_at,
    location_of,
    occ_breaking_cause,
    pack_importance,
    requires_for,
    resolve_knowledge,
    run_check,
    skill_total,
    texture_reference,
    texture_scope_target,
    validate_shape,
)
from core.log import EventRecord, LoggedKnowledgeRecord, StateChange
from core.pack import load_pack
from core.rng import RngBank

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))


def intent(kind: str, target: str | None = None, **fields: Any) -> IntentData:
    return IntentData(
        id="intent_0000", kind=kind, actor="pc_01", target=target, fields=fields
    )


def projection() -> dict[str, dict[str, Any]]:
    return initial_projection(PACK.entities)


# -- shape validation (loud) ---------------------------------------------------


def test_shape_rejects_unknown_fields() -> None:
    move = PACK.action("move")
    assert move is not None
    with pytest.raises(RunnerError, match="takes no step fields"):
        validate_shape(move, intent("move", "loc_tavern", method="sneaky"))


def test_shape_rejects_missing_target_when_preconditions_need_one() -> None:
    steal = PACK.action("steal")
    assert steal is not None
    with pytest.raises(RunnerError, match="requires a target"):
        validate_shape(steal, intent("steal"))


def test_shape_allows_declared_fields() -> None:
    steal = PACK.action("steal")
    assert steal is not None
    validate_shape(steal, intent("steal", "npc_guard_01", method="distraction"))
    wait = PACK.action("wait")
    assert wait is not None
    validate_shape(wait, intent("wait", ticks=5))


# -- duration -------------------------------------------------------------------


def test_duration_fixed_range_and_n() -> None:
    bank = RngBank(42)
    look = PACK.action("look_around")
    assert look is not None
    assert action_duration(look, bank, intent("look_around")) == 1
    move = PACK.action("move")
    assert move is not None
    assert action_duration(move, bank, intent("move", "loc_tavern")) in range(2, 5)
    wait = PACK.action("wait")
    assert wait is not None
    assert action_duration(wait, bank, intent("wait", ticks=7)) == 7
    with pytest.raises(RunnerError, match="positive integer"):
        action_duration(wait, bank, intent("wait"))


# -- preconditions (the closed test set) ------------------------------------------


def test_preconditions_same_location_and_carries_flagged() -> None:
    steal = PACK.action("steal")
    assert steal is not None
    state = projection()
    # pc starts in the street: the guard is elsewhere
    assert first_failing(PACK, state, intent("steal", "npc_guard_01"),
                         steal["requires"]) == "target.same_location"
    state["pc_01"]["position"] = "loc_tavern"
    assert first_failing(PACK, state, intent("steal", "npc_guard_01"),
                         steal["requires"]) is None
    # the barkeep carries nothing stealable — the club is not a steal target
    assert first_failing(PACK, state, intent("steal", "npc_barkeep_01"),
                         steal["requires"]) == "target.carries_flagged"


def test_preconditions_adjacent_to_and_location_of() -> None:
    move = PACK.action("move")
    assert move is not None
    state = projection()
    # the street is a hub: the market is reachable from there
    assert first_failing(PACK, state, intent("move", "loc_market"),
                         move["requires"]) is None
    # from the tavern, however, the market is not adjacent — teleport stays
    # impossible (T5)
    state["pc_01"]["position"] = "loc_tavern"
    assert first_failing(PACK, state, intent("move", "loc_market"),
                         move["requires"]) == "target.adjacent_to"
    arson = PACK.action("arson")
    assert arson is not None
    # the street is a location but not flammable
    state["pc_01"]["position"] = "loc_street"
    assert first_failing(PACK, state, intent("arson", "loc_street"),
                         arson["requires"]) == "target.field_in"
    state["pc_01"]["position"] = "loc_tavern"
    # no fire source accessible while the lamp lies elsewhere
    state["oil_lamp_01"]["position"] = "loc_market"
    assert first_failing(PACK, state, intent("arson", "loc_tavern"),
                         arson["requires"]) == "actor.flagged_accessible"


def test_preconditions_relation_floor_and_carried() -> None:
    talk = PACK.action("talk")
    assert talk is not None
    state = projection()
    state["pc_01"]["position"] = "loc_tavern"
    # all npcs start at trust 50; the floor is 20
    assert first_failing(PACK, state, intent("talk", "npc_barkeep_01"),
                         talk["requires"]) is None
    state["npc_barkeep_01"]["relations.trust"] = 10
    assert first_failing(PACK, state, intent("talk", "npc_barkeep_01"),
                         talk["requires"]) == "target.relation_at_least"
    use = PACK.action("use")
    assert use is not None
    # the ale lies uncarried in the tavern
    assert first_failing(PACK, state, intent("use", "ale_mug_01"),
                         use["requires"]) == "target.carried_by"
    state["ale_mug_01"]["carrier"] = "pc_01"
    assert first_failing(PACK, state, intent("use", "ale_mug_01"),
                         use["requires"]) is None


def test_flagged_lookups_follow_the_projection() -> None:
    state = projection()
    state["pc_01"]["position"] = "loc_tavern"
    assert find_flagged_carried(PACK, state, "npc_guard_01", "steal_target") == "purse_01"
    assert find_flagged_carried(PACK, state, "npc_barkeep_01", "steal_target") is None
    # the lamp lies in the tavern: accessible to the pc standing there
    assert find_flagged_accessible(PACK, state, "pc_01", "is_fire_source") == "oil_lamp_01"
    state["pc_01"]["position"] = "loc_street"
    assert find_flagged_accessible(PACK, state, "pc_01", "is_fire_source") is None
    # ... unless carried
    state["oil_lamp_01"]["carrier"] = "pc_01"
    assert find_flagged_accessible(PACK, state, "pc_01", "is_fire_source") == "oil_lamp_01"


def test_location_of_resolves_entities_and_locations() -> None:
    state = projection()
    assert location_of(PACK, state, "pc_01") == "loc_street"
    assert location_of(PACK, state, "loc_tavern") == "loc_tavern"


# -- opposed checks -----------------------------------------------------------------


def test_skill_total_applies_status_modifiers() -> None:
    state = projection()
    # the drunkard: intoxication 50 -> -2 per 10 points = -10
    assert skill_total(PACK, state, "npc_drunk_01", "perception") == 40
    # doren: fatigue 10 -> -1
    assert skill_total(PACK, state, "npc_guard_01", "perception") == 49
    state["npc_drunk_01"]["status.fear"] = 60  # flat_at_least 50 -> -10
    assert skill_total(PACK, state, "npc_drunk_01", "perception") == 30
    state["npc_drunk_01"]["status.attention"] = "distracted"  # flat_when -> -15
    assert skill_total(PACK, state, "npc_drunk_01", "perception") == 15
    assert skill_total(PACK, state, "pc_01", "stealth") == 40


def _twin_bank(seed: int) -> RngBank:
    """A fresh bank with identical stream state — predict the dice."""
    return RngBank(seed)


def test_run_check_target_defender_and_method() -> None:
    state = projection()
    state["pc_01"]["position"] = "loc_tavern"
    steal = PACK.action("steal")
    assert steal is not None
    bank = RngBank(42)
    twin = _twin_bank(42)
    with twin.assure("substantive"):
        die_a = twin.randint(1, 20)
        die_d = twin.randint(1, 20)
    check = run_check(PACK, state, bank,
                      intent("steal", "npc_guard_01", method="distraction"), steal)
    assert check is not None
    assert check.defender_id == "npc_guard_01"
    # attacker: stealth 40 + die; defender: perception 49 (fatigue 10) + die,
    # distraction method: -10
    assert check.attacker_total == 40 + die_a
    assert check.defender_total == 49 + die_d - 10
    assert check.passed is (check.attacker_total > check.defender_total)
    assert check.margin == check.defender_total - check.attacker_total


def test_run_check_environment_defender() -> None:
    state = projection()
    examine = PACK.action("examine")
    assert examine is not None
    twin = _twin_bank(7)
    with twin.assure("substantive"):
        die_a = twin.randint(1, 20)
        die_d = twin.randint(1, 20)
    check = run_check(PACK, state, RngBank(7), intent("examine", "purse_01"), examine)
    assert check is not None
    assert check.defender_id is None
    assert check.attacker_total == 50 + die_a
    assert check.defender_total == 30 + die_d


def test_run_check_best_in_location_and_unopposed() -> None:
    state = projection()
    # the pc alone in the street: no opposing entity -> unopposed (None)
    flee = PACK.action("flee")
    assert flee is not None
    check = run_check(PACK, state, RngBank(1), intent("flee", "loc_tavern"), flee)
    assert check is None
    # in the tavern: the best pursuit skill present opposes (the guard, base 45 —
    # status modifiers ride perception only, pursuit is unmodified in v0.1)
    state["pc_01"]["position"] = "loc_tavern"
    bank = RngBank(3)
    twin = _twin_bank(3)
    with twin.assure("substantive"):
        die_a = twin.randint(1, 20)
        die_d = twin.randint(1, 20)
    check = run_check(PACK, state, bank, intent("flee", "loc_street"), flee)
    assert check is not None
    assert check.defender_id == "npc_guard_01"
    assert check.attacker_total == 45 + die_a
    assert check.defender_total == 45 + die_d


def test_run_check_unknown_method_is_loud() -> None:
    state = projection()
    state["pc_01"]["position"] = "loc_tavern"
    steal = PACK.action("steal")
    assert steal is not None
    with pytest.raises(RunnerError, match="unknown method"):
        run_check(PACK, state, RngBank(1),
                  intent("steal", "npc_guard_01", method="bribery"), steal)


def test_run_check_none_without_check() -> None:
    state = projection()
    look = PACK.action("look_around")
    assert look is not None
    assert run_check(PACK, state, RngBank(1), intent("look_around"), look) is None


# -- intent OCC (cause attribution) --------------------------------------------------


def _event(event_id: str, t: int, cause: str | None,
           changes: tuple[StateChange, ...]) -> EventRecord:
    return EventRecord(
        id=event_id, t=t, type="wait", actor="pc_01", cause=cause, outcome={},
        knowledge=(LoggedKnowledgeRecord(who="x", channel="saw", fidelity="exact",
                                         knows="k", at=t, source=event_id),),
        state_changes=changes, hooks=(), importance="low",
        provenance={"seed": 1}, target=None,
    )


def test_occ_finds_the_breaking_event() -> None:
    steal = PACK.action("steal")
    assert steal is not None
    # pc enters the tavern (proposal passes), then the guard walks away —
    # the move event breaks same_location
    events = [
        _event("ev_0000", 0, None,
               (StateChange("pc_01", "position", "loc_street", "loc_tavern"),)),
        _event("ev_0001", 2, "ev_0000",
               (StateChange("npc_guard_01", "position", "loc_tavern", "loc_street"),)),
        _event("ev_0002", 4, "ev_0001", ()),
    ]
    proposed = IntentData(
        id="intent_0001", kind="steal", actor="pc_01", target="npc_guard_01",
        fields={}, based_on_event_seq=1,  # proposed after ev_0000
    )
    state = fold(events, initial_projection(PACK.entities))
    assert first_failing(PACK, state, proposed, steal["requires"]) is not None
    assert occ_breaking_cause(
        PACK, events, 1, proposed, initial_projection(PACK.entities)
    ) == "ev_0001"
    # nothing breaks when the guard stays
    staying = [events[0], _event("ev_0001", 2, "ev_0000", ())]
    assert occ_breaking_cause(
        PACK, staying, 1, proposed, initial_projection(PACK.entities)
    ) is None


# -- knowledge resolution ---------------------------------------------------------


def test_knowledge_audiences_except_and_slots() -> None:
    state = projection()
    state["pc_01"]["position"] = "loc_tavern"
    records = resolve_knowledge(
        [
            {"who": "same_location", "except": ["actor", "target"], "channel": "heard",
             "fidelity": "vague", "knows": "noise_in_{location}"},
            {"who": "adjacent_locations", "channel": "heard", "fidelity": "vague",
             "knows": "noise_in_{location}"},
        ],
        PACK, state,
        {"actor": "pc_01", "target": "npc_guard_01", "location": "loc_tavern"},
        tick=5,
    )
    tavern_others = {"npc_barkeep_01", "npc_drunk_01", "npc_maid_01"}
    heard = {r.who for r in records if r.knows == "noise_in_loc_tavern"}
    # tavern occupants minus actor+target, plus adjacent (street, backyard: empty)
    assert heard == tavern_others
    assert all(r.channel == "heard" and r.fidelity == "vague" and r.at == 5
               for r in records)


def test_knowledge_unknown_audience_is_loud() -> None:
    state = projection()
    with pytest.raises(RunnerError, match="unknown knowledge audience"):
        resolve_knowledge(
            [{"who": "everyone", "channel": "saw", "fidelity": "exact", "knows": "x"}],
            PACK, state, {"actor": "pc_01", "target": None, "location": "loc_street"},
            tick=1,
        )


def test_knowers_at_excludes_items_and_locations() -> None:
    state = projection()
    # four npcs in the tavern, one item (the purse), no ambient
    assert knowers_at(PACK, state, "loc_tavern") == [
        "npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    ]
    assert knowers_at(PACK, state, "loc_market") == ["npc_market_crowd_01"]


# -- the pack importance rule --------------------------------------------------------


def test_pack_importance_mapping() -> None:
    rules = PACK.rules
    noise = "status_decayed"  # never story-critical: the per-beat bookkeeping
    assert pack_importance(rules, {"a"}, 0, 0, noise) == "low"
    assert pack_importance(rules, {"a", "b"}, 0, 0, noise) == "low"  # score 1
    assert pack_importance(rules, {"a", "b"}, 1, 0, noise) == "medium"  # 1 + 2
    assert pack_importance(rules, {"a", "b"}, 1, 1, noise) == "high"  # 1 + 2 + 1
    assert pack_importance(rules, {"a"}, 0, 4, noise) == "high"  # 4 hooks


def test_pack_importance_story_critical_hook() -> None:
    """tune-1 (D-045(b)/D-059): story-critical event types score their pack
    bonus — the rule, not the tale gate, owns the signal/noise split. The
    two halves the T7 noise floor pinned: a clean steal (raw score 1) and
    a watch change climb to medium, while the axis bookkeeping the mid-
    section drowned in stays low even with the same entity count."""
    rules = PACK.rules
    bonus = rules["importance"]["score"]["story_critical_event"]
    assert bonus == 2
    # a clean steal: 2 entities (+1) + story-critical (+2) -> medium
    assert pack_importance(rules, {"pc", "guard"}, 0, 0, "steal") == "medium"
    # the watch handover: same shape, same climb
    assert pack_importance(rules, {"outgoing", "incoming"}, 0, 0, "watch_change") == (
        "medium"
    )
    # the noise floor: identical entity count, no hook -> low
    assert pack_importance(rules, {"world", "npc"}, 0, 0, "status_decayed") == "low"
    assert pack_importance(rules, {"npc", "pc"}, 0, 0, "suspicion_changed") == "low"
    # a world texture beat: move stays low
    assert pack_importance(rules, {"pc", "loc"}, 0, 0, "move") == "low"
    # the fire chain stacks with irreversibility -> high
    assert pack_importance(rules, {"world", "loc"}, 1, 0, "fire_started") == "high"
    # a type outside the list with a big raw score still reads by score alone
    assert pack_importance(rules, {"a", "b"}, 1, 1, "some_other_type") == "high"


# -- the texture path (iter-11: grammar/vocabulary split, blueprint §1 D-049) --------


def _texture_intent(reference: Any) -> IntentData:
    return IntentData(
        id="intent_0000", kind="take", actor="pc_01", target=None,
        fields={"texture": reference}, based_on_event_seq=0,
    )


_CANDLES = {
    "entry": "tex_0000", "scope": "scene:loc_tavern",
    "slot": "candles", "value": "lit",
}
_TAKE_ACTION: Any = PACK.action("take")


def test_texture_reference_shape_gates() -> None:
    good = _texture_intent(_CANDLES)
    assert texture_reference(good) == _CANDLES
    assert texture_scope_target(PACK, good) == "loc_tavern"
    bad_references = (
        "candles",                       # the unresolved noun — the mediator resolves
        {"entry": "tex_0000"},             # missing keys
        {**_CANDLES, "slot": "  "},        # blank slot
        {**_CANDLES, "scope": "zone:loc_tavern"},  # unknown prefix
        {**_CANDLES, "scope": "scene:"},   # empty target
    )
    for reference in bad_references:
        with pytest.raises(RunnerError):
            texture_reference(_texture_intent(reference))


def test_texture_scope_target_must_be_known() -> None:
    unknown = _texture_intent({**_CANDLES, "scope": "scene:loc_nowhere"})
    with pytest.raises(RunnerError, match="not a known entity"):
        texture_scope_target(PACK, unknown)


def test_validate_shape_texture_paths() -> None:
    # the texture path: no canon target needed, the reference is shape-gated
    validate_shape(_TAKE_ACTION, _texture_intent(_CANDLES))
    # an undeclared texture field is loud at the fields gate (steal declares
    # only 'method'); the dedicated non-texture-capable branch fires when an
    # action declares the field but ships no pack texture block
    steal: Any = PACK.action("steal")
    with pytest.raises(RunnerError, match="takes no step fields"):
        validate_shape(steal, _texture_intent(_CANDLES))
    synthetic: Any = {"intent": "take", "fields": ["texture"], "requires": []}
    with pytest.raises(RunnerError, match="not texture-capable"):
        validate_shape(synthetic, _texture_intent(_CANDLES))
    # a malformed reference on the texture-capable action is loud
    with pytest.raises(RunnerError):
        validate_shape(_TAKE_ACTION, _texture_intent("candles"))
    # the canon path is unchanged: take still demands its target
    canon = IntentData(
        id="intent_0001", kind="take", actor="pc_01", target=None,
        fields={}, based_on_event_seq=0,
    )
    with pytest.raises(RunnerError, match="requires a target"):
        validate_shape(_TAKE_ACTION, canon)


def test_requires_for_picks_the_pack_path() -> None:
    texture_requires = requires_for(_TAKE_ACTION, _texture_intent(_CANDLES))
    assert texture_requires == list(_TAKE_ACTION["texture"]["requires"])
    canon = IntentData(
        id="intent_0002", kind="take", actor="pc_01", target="purse_01",
        fields={}, based_on_event_seq=0,
    )
    assert requires_for(_TAKE_ACTION, canon) == list(_TAKE_ACTION["requires"])


def test_texture_path_rejects_a_target_mix() -> None:
    """iter-11a: an intent is ONE path — carrying both the resolved texture
    reference and a canon target is an author error, loud at the shape gate
    (the target would otherwise ride the committed event as silently
    ignored data)."""
    mixed = IntentData(
        id="intent_0003", kind="take", actor="pc_01", target="purse_01",
        fields={"texture": dict(_CANDLES)}, based_on_event_seq=0,
    )
    with pytest.raises(RunnerError, match="not a target"):
        validate_shape(_TAKE_ACTION, mixed)


def test_occ_breaking_cause_on_the_texture_path() -> None:
    """The OCC attribution follows the texture path's preconditions: an
    entity-scoped reference whose scope target walks away between proposal
    and completion breaks texture.same_location, attributed to the move."""
    # pc enters the tavern (the cloak's scope target npc_guard_01 is there)
    events = [
        _event("ev_0000", 0, None,
               (StateChange("pc_01", "position", "loc_street", "loc_tavern"),)),
        _event("ev_0001", 2, "ev_0000",
               (StateChange("npc_guard_01", "position", "loc_tavern", "loc_guardroom"),)),
        _event("ev_0002", 4, "ev_0001", ()),
    ]
    cloak = _texture_intent({
        "entry": "tex_0001", "scope": "entity:npc_guard_01",
        "slot": "cloak", "value": "muddy hem",
    })
    initial = initial_projection(PACK.entities)
    assert occ_breaking_cause(PACK, events, 1, cloak, initial) == "ev_0001"
    # nothing breaks when the guard stays
    staying = [events[0], _event("ev_0001", 2, "ev_0000", ())]
    assert occ_breaking_cause(PACK, staying, 1, cloak, initial) is None


def test_texture_noun_test_and_same_location_through_the_noun() -> None:
    state = fold(
        [EventRecord(
            id="ev_0000", t=2, type="move", actor="pc_01", cause=None,
            outcome={}, knowledge=(), state_changes=(
                StateChange("pc_01", "position", "loc_street", "loc_tavern"),
            ), hooks=(), importance="low", provenance={}, target="loc_tavern",
        )],
        initial_projection(PACK.entities),
    )
    here = _texture_intent(_CANDLES)
    assert first_failing(PACK, state, here, requires_for(_TAKE_ACTION, here)) is None
    # scene-scoped texture at another location: same_location fails softly
    elsewhere = _texture_intent({**_CANDLES, "scope": "scene:loc_backyard"})
    assert first_failing(
        PACK, state, elsewhere, requires_for(_TAKE_ACTION, elsewhere)
    ) == "texture.same_location"
    # entity-scoped texture on a present npc resolves through the noun too
    cloak = _texture_intent({
        "entry": "tex_0001", "scope": "entity:npc_guard_01",
        "slot": "cloak", "value": "muddy hem",
    })
    assert first_failing(PACK, state, cloak, requires_for(_TAKE_ACTION, cloak)) is None
    # ...but an absent entity's texture fails the same_location test
    away = _texture_intent({
        "entry": "tex_0002", "scope": "entity:npc_guard_02",
        "slot": "cloak", "value": "muddy hem",
    })
    assert first_failing(PACK, state, away, requires_for(_TAKE_ACTION, away)) == (
        "texture.same_location"
    )
