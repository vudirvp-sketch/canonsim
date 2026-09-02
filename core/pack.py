"""Pack loader (PACK-1): fixed 4-file directory, `sorted()` load order
(INV-2), load-then-resolve — name-based references are checked only after
all files load (no forward declarations). The phase-0 minimum lint fails
loudly at load, before any simulation: orphan references (exits, positions,
carriers, carries), closed-enum membership, phase coverage of the day,
pack meta consistency — and, from iter-2, the intent-contract cross-refs:
resolver keys against the registry, precondition tests against the closed
set, action event types against the template vocabulary, check kinds
against `rules.checks`, knowledge audiences/channels/fidelity/slots
against their closed sets, transition layers against the template
vocabulary, the system-pass DAG (an ambiguity fails at load —
`core/scheduler.py`), and — from drama-3 — the on_action reaction
table (closed key sets, the scope/gate/event/state vocabularies, the
one-hop law). `"_"` commentary fields are ignored wherever
references are collected. Full pack JSON-Schemas are a phase-6 rung
(`docs/BLUEPRINT.md` PACK-1); the event-contract enums the pack mirrors
are cross-checked by `tests/test_smoke.py` against the schema.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from core.clock import Clock
from core.director import ARC_KEYS, CHANNEL_INPUTS
from core.echo import ECHO_BLOCK_KEYS, ECHO_TOKEN_KEYS
from core.intent import (
    AUDIENCES,
    ECHO_TEST,
    KNOWLEDGE_SLOTS,
    LEVERAGE_TEST,
    PRECONDITION_TESTS,
    PRESENT_SITES,
    REJECTION_EVENT,
)
from core.leverage import SECRETS_BLOCK_KEYS, TOKEN_KEYS
from core.onaction import (
    ACTOR_TARGET_KEYS,
    ENTRY_KEYS,
    GATE_KEYS,
    SCOPES,
    STATE_KEYS,
)
from core.predicates import COMPARATORS, COMPOUND_KEYS, LEAF_KINDS
from core.resolvers import REGISTRY
from core.scheduler import ScheduleAmbiguityError, build, decls_from_rules

__all__ = [
    "BRIEF_BLOCK_IDS",
    "PACK_FILE_NAMES",
    "Pack",
    "PackError",
    "load_pack",
]

PACK_FILE_NAMES: Final = ("actions.json", "entities.json", "rules.json", "templates.json")

# The brief pipeline's closed block vocabulary (BRIEF_SPEC §3). Mechanic
# words, not setting nouns (INV-3); owned here so the lint and the
# assembler (`brief/assembler.py`) share one source of truth.
# `present_entities` sits after scene_texture (st-1: the entity-card block
# — canon-projection structure closes the quiet-beat hole; it outranks
# texture in the eviction order, BRIEF_SPEC §5.2).
BRIEF_BLOCK_IDS: Final = (
    "directives",
    "scene_delta",
    "scene_texture",
    "present_entities",
    "recalled_facts",
    "scheduled_lore",
    "voice_exemplars",
    "active_options",
)

_SNAKE_CASE: Final = re.compile(r"^[a-z][a-z0-9_]*$")
_SLOT: Final = re.compile(r"\{([a-z_]+)\}")
_EXCEPT_TOKENS: Final = ("actor", "target", "cause_actor")
_NOUNS: Final = ("actor", "target", "texture")


class PackError(RuntimeError):
    """Load-time lint failure — the pack never reaches the simulation."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PackError(message)


def _ids(records: list[Mapping[str, Any]]) -> set[str]:
    return {record["id"] for record in records}


def _is_int(value: Any) -> bool:
    """A JSON integer (bool excluded — a flag is never a count)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: Any) -> bool:
    """A JSON number (int or float, bool excluded)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


OPTION_KEYS: Final = ("trigger", "weight", "intent", "notes")
"""The closed option-block vocabulary (drama-2): the availability gate,
the ai_chance-style weight, the payload override, and prose notes —
an unknown key is a shape error, never a silent ignore (a typo'd
`triger` would read as an always-available option)."""


def _lint_weight_spec(
    weight_spec: Any,
    where: str,
    npc_ids: set[str],
    location_ids: set[str],
    relation_axes: set[str],
    entity_ids: set[str],
) -> None:
    """The shared weight lint (drama-1's hook-weight block, extracted
    for drama-2's option weights): a flat non-negative int (the v0.1
    form) or the weight_multiplier object {base, modifiers} — base
    int >= 0, each modifier EXACTLY one of add (int >= 0) | factor
    (number >= 0) plus a `when` predicate (the evaluator applies them
    in declaration order; a factor of 0 legally zeroes). The message
    prefix is `{where}: weight...` so both call sites read cleanly."""
    if isinstance(weight_spec, Mapping):
        _require(
            _is_int(weight_spec.get("base")) and weight_spec["base"] >= 0,
            f"{where}: weight.base must be a non-negative integer",
        )
        modifiers = weight_spec.get("modifiers", ())
        _require(
            isinstance(modifiers, list),
            f"{where}: weight.modifiers must be a list",
        )
        for index, modifier in enumerate(modifiers):
            mwhere = f"{where}.weight.modifiers[{index}]"
            _require(
                isinstance(modifier, Mapping),
                f"{mwhere}: must be an object",
            )
            has_add = "add" in modifier
            has_factor = "factor" in modifier
            _require(
                has_add != has_factor,
                f"{mwhere}: exactly one of add|factor is required "
                "(the donor's shape — never both)",
            )
            if has_add:
                _require(
                    _is_int(modifier["add"]) and modifier["add"] >= 0,
                    f"{mwhere}: add must be a non-negative integer",
                )
            else:
                _require(
                    _is_number(modifier["factor"])
                    and modifier["factor"] >= 0,
                    f"{mwhere}: factor must be a non-negative number",
                )
            when = modifier.get("when")
            error = _predicate_error(
                when, f"{mwhere}.when", npc_ids, location_ids,
                relation_axes, entity_ids,
            )
            _require(
                error is None,
                error or "unreachable",
            )
    else:
        _require(
            _is_int(weight_spec) and weight_spec >= 0,
            f"{where}: weight must be a non-negative integer or a "
            "weight_multiplier object",
        )


def _predicate_error(
    spec: Any,
    where: str,
    npc_ids: set[str],
    location_ids: set[str],
    relation_axes: set[str],
    entity_ids: set[str],
) -> str | None:
    """Validate one drama-1 predicate spec (core/predicates.py owns the
    grammar; this is the load-time shape gate — the evaluator's loud
    ValueError is the runtime backstop, never the first line of defense).
    Returns the error message or None when the spec is valid. Recursive;
    `where` carries the pack path for the message (e.g.
    `director.hooks['x'].trigger.all[0]`)."""
    if isinstance(spec, list):
        if not spec:  # L1: an empty AND is dead vocabulary
            return f"{where}: an empty predicate list is dead vocabulary"
        for index, item in enumerate(spec):
            error = _predicate_error(
                item, f"{where}[{index}]", npc_ids, location_ids,
                relation_axes, entity_ids,
            )
            if error:
                return error
        return None
    if not isinstance(spec, Mapping) or not spec:
        return f"{where}: predicate must be a non-empty object or a list"
    compounds = [key for key in COMPOUND_KEYS if key in spec]
    if compounds:
        if len(spec) != 1:
            return (
                f"{where}: a compound carries extra keys {sorted(spec)} "
                f"beside {compounds[0]!r}"
            )
        inner = spec[compounds[0]]
        if compounds[0] == "not":
            return _predicate_error(
                inner, f"{where}.not", npc_ids, location_ids,
                relation_axes, entity_ids,
            )
        if not isinstance(inner, list) or not inner:  # L1: dead vocabulary
            return f"{where}.{compounds[0]}: must be a non-empty list"
        for index, item in enumerate(inner):
            error = _predicate_error(
                item, f"{where}.{compounds[0]}[{index}]", npc_ids,
                location_ids, relation_axes, entity_ids,
            )
            if error:
                return error
        return None
    kind = spec.get("kind")
    if kind not in LEAF_KINDS:
        return f"{where}: kind must be one of {list(LEAF_KINDS)}, got {kind!r}"
    if kind == "time":
        if not _is_int(spec.get("tick")) or spec["tick"] < 0:
            return f"{where}: time predicate needs a non-negative integer tick"
    elif kind == "place":
        if spec.get("target_npc") not in npc_ids:
            return f"{where}: place predicate target_npc must name an npc"
        if spec.get("location") not in location_ids:
            return f"{where}: place predicate location must name a location"
    elif kind == "threshold":
        if spec.get("target_npc") not in npc_ids:
            return f"{where}: threshold predicate target_npc must name an npc"
        if spec.get("axis") not in relation_axes:
            return f"{where}: threshold predicate axis must be a relations axis"
        if spec.get("comparator") not in ("at_least", "at_most"):
            return f"{where}: threshold comparator must be at_least|at_most"
        if not _is_int(spec.get("value")):
            return f"{where}: threshold value must be an integer"
    else:  # prop — the generalized projection read (drama-1)
        if spec.get("of") not in entity_ids:
            return f"{where}: prop predicate 'of' must name an entity"
        if not isinstance(spec.get("path"), str) or not spec["path"]:
            return f"{where}: prop predicate 'path' must be a non-empty string"
        if spec.get("comparator") not in COMPARATORS:
            return (
                f"{where}: prop comparator must be one of {list(COMPARATORS)}"
            )
        if spec.get("comparator") in ("at_least", "at_most") and not _is_int(
            spec.get("value")
        ):
            return f"{where}: prop {spec['comparator']} needs an integer value"
        if "value" not in spec:
            return f"{where}: prop predicate needs a value"
    return None


class _Lint:
    """Phase-0 minimum lint: one pass over the loaded pack data."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def run(self) -> None:
        self._meta()
        self._entities()
        self._actions()
        self._templates()
        self._time_rules()
        self._systems()
        self._transitions()
        self._knowledge_rules()
        self._crime_watch()
        self._expectations()
        self._urgencies()
        self._director()
        self._on_action()
        self._secrets()
        self._echo()
        self._states_rules()
        self._importance_rules()
        self._brief()

    def _meta(self) -> None:
        names = {name: d["meta"]["pack"] for name, d in self._data.items()}
        versions = {name: d["meta"]["version"] for name, d in self._data.items()}
        _require(
            len(set(names.values())) == 1 and len(set(versions.values())) == 1,
            f"pack meta disagrees across files: {names} / {versions}",
        )

    def _entities(self) -> None:
        entities = self._data["entities.json"]
        rules = self._data["rules.json"]
        locations = entities["locations"]
        npcs = entities["npcs"]
        ambients = entities["ambient_entities"]
        items = entities["items"]

        all_ids = _ids(locations) | _ids(npcs) | _ids(ambients) | _ids(items)
        total = sum(map(len, (locations, npcs, ambients, items)))
        _require(len(all_ids) == total, "entity ids are not unique across categories")

        location_ids = _ids(locations)
        by_location = {loc["id"]: loc for loc in locations}
        for loc in locations:
            for exit_id in loc["exits"]:
                _require(exit_id in location_ids, f"location {loc['id']}: orphan exit {exit_id}")
                _require(
                    loc["id"] in by_location[exit_id]["exits"],
                    f"exit graph asymmetric: {loc['id']} -> {exit_id}",
                )

        status_axes = set(rules["states"])
        relation_axes = set(rules["relations"]["axes"])
        relation_scale = rules["relations"]["scale"]
        crime_status_values = set(rules["crime_watch"].get("status_values", ()))
        item_ids = _ids(items)
        npc_ids = _ids(npcs)
        for npc in npcs:
            _require(npc["position"] in location_ids, f"npc {npc['id']}: unknown position")
            for carried in npc.get("carries", []):
                _require(carried in item_ids, f"npc {npc['id']}: carries unknown item {carried}")
            unknown_status = set(npc.get("status", {})) - status_axes
            _require(not unknown_status, f"npc {npc['id']}: unknown status axes {unknown_status}")
            unknown_axes = set(npc.get("relations", {})) - relation_axes
            _require(not unknown_axes, f"npc {npc['id']}: unknown relation axes {unknown_axes}")
            if "crime_status" in npc:
                _require(
                    npc["crime_status"] in crime_status_values,
                    f"npc {npc['id']}: crime_status {npc['crime_status']!r} not in "
                    f"crime_watch.status_values {sorted(crime_status_values)}",
                )
            for pair in npc.get("pair_relations", ()):  # P2a: sparse pair map
                pair_with = pair.get("with")
                _require(
                    isinstance(pair_with, str) and pair_with in npc_ids
                    and pair_with != npc["id"],
                    f"npc {npc['id']}: pair_relations 'with' must name another "
                    f"npc, got {pair_with!r}",
                )
                _require(
                    len(pair) >= 2,
                    f"npc {npc['id']}: pair_relations entry carries no axes",
                )
                for axis, value in pair.items():
                    if axis == "with":
                        continue
                    _require(
                        axis in relation_axes,
                        f"npc {npc['id']}: unknown pair axis {axis!r}",
                    )
                    _require(
                        isinstance(value, int) and not isinstance(value, bool)
                        and relation_scale[0] <= value <= relation_scale[1],
                        f"npc {npc['id']}: pair axis {axis!r} must be an integer "
                        f"inside {relation_scale}, got {value!r}",
                    )

        players = [npc["id"] for npc in npcs if npc.get("is_player", False)]
        _require(len(players) == 1, f"exactly one is_player npc required, got {players}")

        for ambient in ambients:
            _require(
                ambient["position"] in location_ids,
                f"ambient {ambient['id']}: unknown position",
            )

        for item in items:
            _require(item["position"] in location_ids, f"item {item['id']}: unknown position")
            effect = item.get("use_effect")
            if effect is not None:
                _require(
                    isinstance(effect, Mapping)
                    and effect.get("status") in status_axes
                    and isinstance(effect.get("delta"), int)
                    and not isinstance(effect.get("delta"), bool),
                    f"item {item['id']}: use_effect must name a rules.states "
                    f"axis and an integer delta, got {effect!r}",
                )
            carrier = item.get("carrier")
            if carrier is not None:
                _require(carrier in npc_ids, f"item {item['id']}: unknown carrier {carrier}")
                owner = next(npc for npc in npcs if npc["id"] == carrier)
                _require(
                    item["id"] in owner.get("carries", []),
                    f"item {item['id']}: carrier {carrier} does not carry it",
                )
        for npc in npcs:
            for carried in npc.get("carries", []):
                item = next(i for i in items if i["id"] == carried)
                _require(
                    item.get("carrier") == npc["id"],
                    f"npc {npc['id']} carries {carried} but the item names "
                    f"{item.get('carrier')!r}",
                )

    # -- actions (the intent contract cross-refs) -----------------------------

    def _knowledge_entry(
        self, action_intent: str, record: Mapping[str, Any],
        requires: tuple[Mapping[str, Any], ...] = (),
    ) -> None:
        knowledge = self._data["rules.json"]["knowledge"]
        where = f"action {action_intent!r} knowledge"
        _require(record["who"] in AUDIENCES, f"{where}: unknown audience {record['who']!r}")
        _require(
            record["channel"] in knowledge["channels"],
            f"{where}: unknown channel {record['channel']!r}",
        )
        _require(
            record["fidelity"] in knowledge["fidelity_chain"],
            f"{where}: unknown fidelity {record['fidelity']!r}",
        )
        if record["who"] == "destination_location":
            # resolves against the target location: the action must pin the
            # target's kind to location (movement sighting audiences)
            _require(
                any(
                    cond.get("noun") == "target"
                    and cond.get("test") == "kind"
                    and cond.get("is") == "location"
                    for cond in requires
                ),
                f"{where}: audience 'destination_location' requires a "
                f"target-kind-location precondition",
            )
        if "present_at" in record:
            # The per-present-target expansion (st-1, INTENT_SCHEMA §7): the
            # audience stays `actor` (KI#43's law — this is a `knows`
            # expansion, NOT an audience kind), the site is a closed set,
            # and the {present} slot must actually be used — a site without
            # the slot would emit N identical records.
            _require(
                record["who"] == "actor",
                f"{where}: a 'present_at' expansion requires who == 'actor' "
                f"(the audience stays actor — INTENT_SCHEMA §7)",
            )
            _require(
                record["present_at"] in PRESENT_SITES,
                f"{where}: unknown present_at site {record['present_at']!r} "
                f"(must be one of {list(PRESENT_SITES)})",
            )
            _require(
                not record.get("except"),
                f"{where}: 'except' has no meaning on a 'present_at' "
                f"expansion (the audience is the actor alone)",
            )
            _require(
                "present" in _SLOT.findall(record["knows"]),
                f"{where}: 'present_at' declared but the knows template "
                f"{record['knows']!r} lacks the {{present}} slot",
            )
            if record["present_at"] == "destination_location":
                _require(
                    any(
                        cond.get("noun") == "target"
                        and cond.get("test") == "kind"
                        and cond.get("is") == "location"
                        for cond in requires
                    ),
                    f"{where}: 'present_at=destination_location' requires a "
                    f"target-kind-location precondition",
                )
        elif "present" in _SLOT.findall(record["knows"]):
            # the mirror: the {present} slot has no semantics without a
            # site — the closed-slot lint alone would pass it
            _require(
                False,
                f"{where}: the {{present}} slot requires a 'present_at' "
                f"expansion site on the record",
            )
        for token in record.get("except", ()):
            _require(
                token in _EXCEPT_TOKENS,
                f"{where}: unknown except token {token!r}",
            )
        for slot in _SLOT.findall(record["knows"]):
            _require(
                slot in KNOWLEDGE_SLOTS,
                f"{where}: unknown slot {{{slot}}} in {record['knows']!r}",
            )

    def _texture_block(self, intent: str, action: Mapping[str, Any]) -> None:
        """The optional texture block (iter-11, blueprint §1 promotion): the
        pack declares THIS action texture-capable; its `requires` replace
        the canon ones for intents carrying a resolved texture reference,
        its `knowledge` templates render with the texture context (no canon
        target on that path — the {target} slot is forbidden here)."""
        block = action.get("texture")
        if block is None:
            return
        where = f"action {intent!r} texture"
        _require(isinstance(block, Mapping), f"{where}: must be an object")
        _require(
            "texture" in action.get("fields", ()),
            f"{where}: the action must declare 'texture' in its fields",
        )
        _require(
            isinstance(block.get("requires"), list),
            f"{where}: requires must be a list",
        )
        # The texture path carries no canon target: a target-sourced check
        # would roll against a None defender (a silent nonsense check, not
        # a crash) — the check must oppose the actor or the environment.
        checks = self._data["rules.json"]["checks"]
        check = action.get("check")
        if check is not None and checks["kinds"][check["kind"]].get(
            "defender_source"
        ) == "target":
            _require(
                False,
                f"{where}: check kind {check['kind']!r} defends from the target — "
                f"the texture path has none (use best_in_location or environment)",
            )
        for cond in block["requires"]:
            _require(
                cond.get("test") in PRECONDITION_TESTS,
                f"{where}: unknown precondition test {cond.get('test')!r}",
            )
            for param in ("noun", "with", "who"):
                if param in cond:
                    _require(
                        cond[param] in _NOUNS,
                        f"{where}: precondition {param} {cond[param]!r} "
                        f"must be one of {list(_NOUNS)}",
                    )
        for branch, records in block.get("knowledge", {}).items():
            _require(
                branch in ("success", "failure", "failure_total"),
                f"{where}: unknown knowledge branch {branch!r}",
            )
            if branch == "failure_total":
                # _branch decides failure_total from the CANON knowledge
                # block — without it the texture branch is dead pack data.
                _require(
                    "failure_total" in action.get("knowledge", {}),
                    f"{where}: declares a failure_total branch but the canon "
                    f"knowledge block does not — _branch can never reach it",
                )
            for record in records:
                self._knowledge_entry(intent, record, tuple(block["requires"]))
                _require(
                    "target" not in _SLOT.findall(record["knows"]),
                    f"{where}: knowledge branch {branch!r} uses the {{target}} "
                    f"slot — the texture path has no canon target "
                    f"(use {{{{texture_slot}}}})",
                )

    def _actions(self) -> None:
        actions = self._data["actions.json"]["actions"]
        templates = self._data["templates.json"]["events"]
        checks = self._data["rules.json"]["checks"]
        intents = [action["intent"] for action in actions]
        _require(len(intents) == len(set(intents)), "action intents are not unique")
        for action in actions:
            intent = action["intent"]
            _require(
                bool(_SNAKE_CASE.match(intent)),
                f"action intent {intent!r} is not snake_case",
            )
            ticks = action["ticks"]
            if isinstance(ticks, Mapping):
                _require(
                    isinstance(ticks.get("min"), int) and isinstance(ticks.get("max"), int)
                    and ticks["min"] <= ticks["max"],
                    f"action {intent}: ticks range malformed: {ticks}",
                )
            else:
                _require(
                    isinstance(ticks, int) or ticks == "N",
                    f"action {intent}: ticks must be int, {{min,max}} or 'N'",
                )
            resolver = action.get("resolver")
            _require(
                isinstance(resolver, str) and resolver in REGISTRY,
                f"action {intent}: resolver {resolver!r} is not in the registry "
                f"(known: {sorted(REGISTRY)})",
            )
            for branch in ("success", "failure", "failure_total"):
                event_type = action.get("events", {}).get(branch)
                if event_type is not None:
                    _require(
                        event_type in templates,
                        f"action {intent}: {branch} event {event_type!r} is not in "
                        f"the template vocabulary (EVENT_SCHEMA §11)",
                    )
            check = action.get("check")
            if check is not None:
                _require(
                    check["kind"] in checks["kinds"],
                    f"action {intent}: unknown check kind {check['kind']!r}",
                )
                _require(
                    isinstance(check.get("difficulty"), int),
                    f"action {intent}: check difficulty must be an integer",
                )
            for cond in action.get("requires", ()):
                _require(
                    cond.get("test") in PRECONDITION_TESTS,
                    f"action {intent}: unknown precondition test {cond.get('test')!r}",
                )
                # iter-45 (social-1b): the leverage test's `who` is
                # mandatory — a missing key would KeyError mid-run at the
                # door (the carried_by family, refused at load instead).
                if cond.get("test") == LEVERAGE_TEST:
                    _require(
                        cond.get("who") in _NOUNS,
                        f"action {intent}: precondition leverage_over requires "
                        f"'who' (the entity the noun holds leverage over)",
                    )
                # iter-46 (social-2): the echo gate's axis/value must
                # name the declared vocabulary — a dead gate is refused
                # at load (the leverage `who` family)
                if cond.get("test") == ECHO_TEST:
                    self._lint_echo_cond(cond, f"action {intent}")
                # pack-2 (iter-29): the spot_available test's layer param
                # must name a declared transition layer — a typo would
                # KeyError mid-run (the KI#15 dead-data family, refused
                # at load instead).
                if cond.get("test") == "spot_available":
                    _require(
                        cond.get("layer") in self._data["rules.json"].get(
                            "transitions", {}
                        ),
                        f"action {intent}: precondition layer "
                        f"{cond.get('layer')!r} is not a declared transition "
                        f"layer",
                    )
                for param in ("noun", "with", "who"):
                    if param in cond:
                        _require(
                            cond[param] in _NOUNS,
                            f"action {intent}: precondition {param} {cond[param]!r} "
                            f"must be one of {list(_NOUNS)}",
                        )
            for fields_value in action.get("fields", ()):
                _require(
                    isinstance(fields_value, str),
                    f"action {intent}: fields must be strings",
                )
            # events/knowledge branch consistency (KI#15): a resolver can
            # index events[success] always, events[failure] when the action
            # carries a check, events[failure_total] when knowledge
            # declares that branch — a missing key would crash at
            # completion instead of failing at load.
            events = action.get("events", {})
            _require("success" in events, f"action {intent}: events.success is required")
            if action.get("check") is not None:
                _require(
                    "failure" in events,
                    f"action {intent}: has a check but no events.failure",
                )
            if "failure_total" in action.get("knowledge", {}):
                _require(
                    "failure_total" in events,
                    f"action {intent}: knowledge declares failure_total but "
                    f"events does not — events['failure_total'] would crash "
                    f"at completion",
                )
            for branch, records in action.get("knowledge", {}).items():
                _require(
                    branch in ("success", "failure", "failure_total"),
                    f"action {intent}: unknown knowledge branch {branch!r}",
                )
                for record in records:
                    self._knowledge_entry(
                        intent, record, tuple(action.get("requires", ()))
                    )
                    # The mirror of the texture-block {target} ban: the CANON
                    # context carries no texture slot (only a texture-path
                    # intent does) — the template would KeyError mid-run.
                    _require(
                        "texture_slot" not in _SLOT.findall(record["knows"]),
                        f"action {intent}: knowledge branch {branch!r} uses the "
                        f"{{texture_slot}} slot — only a texture block may "
                        f"(the canon context has no texture reference)",
                    )
            self._texture_block(intent, action)
            for branch, tags in action.get("hooks", {}).items():
                _require(
                    branch in ("success", "failure"),
                    f"action {intent}: unknown hooks branch {branch!r}",
                )
                for tag in tags:
                    _require(isinstance(tag, str), f"action {intent}: hook tags are strings")
            ignition = action.get("ignition")
            if ignition is not None:
                _require(
                    ignition.get("layer") in self._data["rules.json"]["transitions"],
                    f"action {intent}: ignition layer {ignition.get('layer')!r} unknown",
                )
                _require(
                    isinstance(ignition.get("item_flag"), str),
                    f"action {intent}: ignition item_flag must be a string",
                )
            self._status_effects(intent, action)
            self._balance(intent, action)

    def _balance(self, intent: str, action: Mapping[str, Any]) -> None:
        """The optional balance block (iter-45, social-1b): the pack
        declares what a spent leverage cluster BUYS — subject-directed
        pair-axis shifts ({axis, delta}) the `coerce` resolver applies
        toward the actor. The status_effects precedent owns the shape:
        the block lives beside its action, only its resolver consumes
        it, axes must be real relations axes, deltas non-zero integers
        (an undeclared axis or a zero delta is dead data — KI#15 family:
        refuse at load, never a silent no-op at completion)."""
        balance = action.get("balance")
        if balance is None:
            return
        where = f"action {intent!r} balance"
        _require(
            action.get("resolver") == "coerce",
            f"{where}: only the 'coerce' resolver consumes the block "
            f"(this action resolves via {action.get('resolver')!r})",
        )
        _require(
            isinstance(balance, list) and balance,
            f"{where}: must be a non-empty list",
        )
        axes = set(self._data["rules.json"].get("relations", {}).get("axes", ()))
        for effect in balance:
            _require(isinstance(effect, Mapping), f"{where}: entries must be objects")
            unknown = sorted(set(effect) - {"axis", "delta"})
            if unknown:
                raise PackError(
                    f"{where}: unknown keys {unknown} (the closed "
                    "vocabulary: axis | delta)"
                )
            axis = effect.get("axis")
            _require(
                isinstance(axis, str) and axis in axes,
                f"{where}: unknown pair axis {axis!r} (not a relations axis)",
            )
            delta = effect.get("delta")
            _require(
                isinstance(delta, int) and not isinstance(delta, bool) and delta != 0,
                f"{where}: axis {axis!r} delta must be a non-zero integer",
            )

    def _status_effects(self, intent: str, action: Mapping[str, Any]) -> None:
        """The optional status-effects block (tune-1, KI#4): the pack
        declares the actor's status deltas the `recuperate` resolver
        applies. The axes must be real `rules.states` axes (an undeclared
        axis is dead data — the resolver would write a prop nothing
        reads); the block on any other resolver is dead data the same way
        (KI#15 family: refuse at load, never crash or silently no-op at
        completion)."""
        effects = action.get("status_effects")
        if effects is None:
            return
        where = f"action {intent!r} status_effects"
        _require(
            action.get("resolver") == "recuperate",
            f"{where}: only the 'recuperate' resolver consumes the block "
            f"(this action resolves via {action.get('resolver')!r})",
        )
        _require(isinstance(effects, list) and effects, f"{where}: must be a "
                 f"non-empty list")
        states = self._data["rules.json"].get("states", {})
        for effect in effects:
            _require(isinstance(effect, Mapping), f"{where}: entries must be objects")
            axis = effect.get("status")
            _require(
                isinstance(axis, str) and axis in states,
                f"{where}: unknown status axis {axis!r} (not a rules.states axis)",
            )
            delta = effect.get("delta")
            _require(
                isinstance(delta, int) and not isinstance(delta, bool) and delta != 0,
                f"{where}: status {axis!r} delta must be a non-zero integer",
            )

    def _templates(self) -> None:
        templates = self._data["templates.json"]
        _require("fallback" in templates, "templates: missing fallback line")
        _require(
            REJECTION_EVENT in templates["events"],
            f"templates: the {REJECTION_EVENT!r} line is mandatory (the front door "
            f"emits it — INTENT_SCHEMA §3)",
        )
        for event_type in templates["events"]:
            _require(
                bool(_SNAKE_CASE.match(event_type)),
                f"template event type {event_type!r} is not snake_case",
            )

    def _time_rules(self) -> None:
        time_rules = self._data["rules.json"]["time"]
        try:
            Clock.from_rules(time_rules)
        except ValueError as exc:
            raise PackError(f"time rules invalid: {exc}") from exc

    # -- systems (the scheduler DAG) -------------------------------------------

    def _systems(self) -> None:
        rules = self._data["rules.json"]
        decls = decls_from_rules(rules)
        for decl in decls.values():
            for referenced in (*decl.before, *decl.after):
                _require(
                    referenced in decls,
                    f"system {decl.name!r}: orders against unknown system {referenced!r}",
                )
        try:
            build(decls)
        except ScheduleAmbiguityError as exc:
            raise PackError(f"system schedule invalid: {exc}") from exc

    # -- transitions (the pack-declared layers) ---------------------------------

    def _transitions(self) -> None:
        rules = self._data["rules.json"]
        transitions = rules.get("transitions", {})
        templates = self._data["templates.json"]["events"]
        systems = rules.get("systems", {})
        for layer, config in transitions.items():
            if not isinstance(config, Mapping) or "events" not in config:
                continue  # the section's own meta entries
            where = f"transition layer {layer!r}"
            _require(
                config.get("system") in systems
                and systems[config["system"]].get("per_tick") is True,
                f"{where}: system {config.get('system')!r} must be a per-tick system",
            )
            _require(
                isinstance(config.get("spot_field"), str),
                f"{where}: spot_field must be a string",
            )
            for key in ("spot_state", "halt_flag"):
                _require(
                    isinstance(config.get(key), str) and config[key].strip(),
                    f"{where}: {key} must be a non-empty string",
                )
            for key, event_type in config["events"].items():
                _require(
                    event_type in templates,
                    f"{where}: {key} event {event_type!r} is not in the template "
                    f"vocabulary (EVENT_SCHEMA §11)",
                )
            ignition = config.get("ignition", {})
            _require(
                isinstance(ignition.get("chance_on_drop_break"), (int, float))
                and 0 <= ignition["chance_on_drop_break"] <= 1,
                f"{where}: chance_on_drop_break must be a probability",
            )
            for key in ("spread",):
                _require(
                    isinstance(config[key].get("chance_per_tick"), (int, float))
                    and 0 <= config[key]["chance_per_tick"] <= 1,
                    f"{where}: {key} chance must be a probability",
                )
            # D-057: the follow-up vocabulary (kinds, flags, values) is layer
            # data — every kind joins a declared event AND knowledge entry.
            follow_ups = config.get("follow_ups")
            _require(
                isinstance(follow_ups, list) and follow_ups,
                f"{where}: follow_ups must be a non-empty list",
            )
            kinds: set[str] = set()
            for spec in follow_ups:
                _require(
                    isinstance(spec, Mapping),
                    f"{where}.follow_ups: entries must be objects",
                )
                kind = spec.get("kind")
                where_fu = f"{where}.follow_ups[{kind!r}]"
                _require(
                    isinstance(kind, str) and kind.strip() and kind not in kinds,
                    f"{where_fu}: kind must be a unique non-empty string",
                )
                kinds.add(kind)
                _require(
                    kind in config["events"],
                    f"{where_fu}: no {kind!r} event declared",
                )
                _require(
                    kind in config.get("knowledge", {}),
                    f"{where_fu}: no {kind!r} knowledge entry declared",
                )
                after = spec.get("after_ticks")
                _require(
                    isinstance(after, int)
                    and not isinstance(after, bool)
                    and after >= 0,
                    f"{where_fu}: after_ticks must be a non-negative integer",
                )
                _require(
                    isinstance(spec.get("flag"), str) and spec["flag"].strip(),
                    f"{where_fu}: flag must be a non-empty string",
                )
                _require(
                    "value" in spec,
                    f"{where_fu}: value is required",
                )
                _require(
                    isinstance(spec.get("irreversible"), bool),
                    f"{where_fu}: irreversible must be a boolean",
                )
                blocked = spec.get("blocked_by")
                _require(
                    isinstance(blocked, list)
                    and all(isinstance(flag, str) and flag.strip() for flag in blocked),
                    f"{where_fu}: blocked_by must be a list of non-empty strings",
                )
            for key, record in config.get("knowledge", {}).items():
                self._knowledge_entry(f"{layer}.{key}", record)

    # -- knowledge rules (telling + acceptance, iter-3) ------------------------

    def _knowledge_rules(self) -> None:
        rules = self._data["rules.json"]
        knowledge = rules.get("knowledge", {})
        templates = self._data["templates.json"]["events"]
        relation_axes = set(rules["relations"]["axes"])
        status_axes = set(rules["states"])
        _require(
            knowledge.get("salience") in ("importance_then_recency",),
            f"knowledge.salience must be one of ['importance_then_recency'], "
            f"got {knowledge.get('salience')!r}",
        )
        acceptance = knowledge.get("rumor_acceptance", {})
        _require(
            acceptance.get("trust_axis") in relation_axes,
            f"knowledge.rumor_acceptance.trust_axis {acceptance.get('trust_axis')!r} "
            f"is not a relations axis",
        )
        _require(
            acceptance.get("teller_penalty_axis") in status_axes,
            f"knowledge.rumor_acceptance.teller_penalty_axis "
            f"{acceptance.get('teller_penalty_axis')!r} is not a status axis",
        )
        telling = knowledge.get("telling")
        if telling is not None:
            for key in ("on_event", "event"):
                _require(
                    telling.get(key) in templates,
                    f"knowledge.telling.{key} {telling.get(key)!r} is not in the "
                    f"template vocabulary",
                )
            for key in ("teller", "listener"):
                _require(
                    telling.get(key) in ("actor", "target"),
                    f"knowledge.telling.{key} must be 'actor' or 'target'",
                )
            _require(
                isinstance(telling.get("facts"), int)
                and not isinstance(telling.get("facts"), bool)
                and telling["facts"] >= 1,
                "knowledge.telling.facts must be a positive integer",
            )

    # -- crime_watch (the reacting system, iter-3) ------------------------------

    def _crime_watch(self) -> None:
        rules = self._data["rules.json"]
        crime = rules.get("crime_watch", {})
        if not crime:
            return
        templates = self._data["templates.json"]["events"]
        entities = self._data["entities.json"]
        location_ids = _ids(entities["locations"])
        npc_ids = _ids(entities["npcs"])
        relation_axes = set(rules["relations"]["axes"])
        _require(
            crime.get("suspicion_axis") in relation_axes,
            f"crime_watch.suspicion_axis {crime.get('suspicion_axis')!r} is not "
            f"a relations axis",
        )
        for key in ("reaction_event",):
            _require(
                crime.get(key) in templates,
                f"crime_watch.{key} {crime.get(key)!r} is not in the template "
                f"vocabulary",
            )
        _require(
            crime.get("status_suspect_value") in crime.get("status_values", ()),
            "crime_watch.status_suspect_value must be one of status_values",
        )
        sources = crime.get("suspicion_sources", {})
        for token, source in crime.get("suspicion_from_knowledge", {}).items():
            _require(
                source in sources,
                f"crime_watch.suspicion_from_knowledge[{token!r}]: unknown "
                f"suspicion source {source!r}",
            )
        arrest = crime.get("arrest", {})
        _require(
            arrest.get("event") in templates,
            f"crime_watch.arrest.event {arrest.get('event')!r} is not in the "
            f"template vocabulary",
        )
        # iter-4: arrest resolution fields (evasion_vs_pursuit → arrest_resolved)
        _require(
            arrest.get("resolution_event") in templates,
            f"crime_watch.arrest.resolution_event {arrest.get('resolution_event')!r} "
            f"is not in the template vocabulary",
        )
        _require(
            arrest.get("resolution_check") in rules["checks"]["kinds"],
            f"crime_watch.arrest.resolution_check "
            f"{arrest.get('resolution_check')!r} is not a checks.kinds entry",
        )
        _require(
            arrest.get("caught_value") in crime.get("status_values", ()),
            f"crime_watch.arrest.caught_value {arrest.get('caught_value')!r} "
            f"is not in crime_watch.status_values",
        )
        ticks = crime.get("watch_rotation_ticks", [])
        _require(
            all(
                isinstance(t, int) and not isinstance(t, bool)
                and 0 <= t < rules["time"]["ticks_per_day"]
                for t in ticks
            ),
            "crime_watch.watch_rotation_ticks must be intraday tick offsets",
        )
        if not ticks:
            return
        rotation = crime.get("rotation", {})
        for key in ("duty_post", "rest_post"):
            _require(
                rotation.get(key) in location_ids,
                f"crime_watch.rotation.{key} {rotation.get(key)!r} is not a location",
            )
        participants = rotation.get("participants", [])
        _require(
            len(participants) >= 2
            and len(set(participants)) == len(participants)
            and all(p in npc_ids for p in participants),
            f"crime_watch.rotation.participants must be >= 2 distinct npcs, "
            f"got {participants!r}",
        )
        for key in ("watch_event", "transfer_event"):
            _require(
                rotation.get(key) in templates,
                f"crime_watch.rotation.{key} {rotation.get(key)!r} is not in "
                f"the template vocabulary",
            )

    # -- expectations (P2d, iter-3) ----------------------------------------------

    def _expectations(self) -> None:
        rules = self._data["rules.json"]
        config = rules.get("expectations")
        if config is None:
            return
        templates = self._data["templates.json"]["events"]
        entities = self._data["entities.json"]
        location_ids = _ids(entities["locations"])
        npc_ids = _ids(entities["npcs"])
        item_ids = _ids(entities["items"])
        _require(
            config.get("event") in templates,
            f"expectations.event {config.get('event')!r} is not in the template "
            f"vocabulary",
        )
        _require(
            config.get("check_at") in ("watch_rotation",),
            f"expectations.check_at must be 'watch_rotation', got "
            f"{config.get('check_at')!r}",
        )
        items_by_id = {item["id"]: item for item in entities["items"]}
        for rule in config.get("rules", ()):
            where = f"expectation rule {rule.get('knows')!r}"
            _require(rule.get("npc") in npc_ids, f"{where}: unknown npc")
            _require(rule.get("item") in item_ids, f"{where}: unknown item")
            modes = [key for key in ("carried_by", "at_location") if key in rule]
            _require(
                len(modes) == 1,
                f"{where}: exactly one of carried_by / at_location is required",
            )
            if "carried_by" in rule:
                _require(rule["carried_by"] in npc_ids, f"{where}: unknown carrier npc")
            if "at_location" in rule:
                _require(
                    rule["at_location"] in location_ids, f"{where}: unknown location"
                )
            _require(
                isinstance(rule.get("knows"), str) and rule["knows"],
                f"{where}: knows must be a non-empty string",
            )
            # a rule must hold on the initial pack state: a violation without
            # a mover would have no event to chain its cause to (P2d)
            item = items_by_id[rule["item"]]
            holds = (
                item.get("carrier") == rule["carried_by"]
                if "carried_by" in rule
                else item["position"] == rule["at_location"]
            )
            _require(
                holds,
                f"{where}: violated by the initial pack state — expectation "
                f"rules must hold at t=0",
            )

    # -- states rules (decay rates + reset_on_rotation, iter-4a) -------------

    def _states_rules(self) -> None:
        rules = self._data["rules.json"]
        states = rules.get("states", {})
        for axis, config in states.items():
            if not isinstance(config, Mapping):
                continue  # the section's notes field
            where = f"states.{axis}"
            for rate_key in ("gain_per_360_ticks_awake", "decay_per_360_ticks",
                             "auto_decay"):
                if rate_key in config:
                    _require(
                        isinstance(config[rate_key], int)
                        and not isinstance(config[rate_key], bool)
                        and config[rate_key] >= 0,
                        f"{where}.{rate_key} must be a non-negative integer",
                    )
            if "reset_on_rotation" in config:
                _require(
                    isinstance(config["reset_on_rotation"], bool),
                    f"{where}.reset_on_rotation must be a boolean",
                )

    # -- the importance rule (tune-1: the story-critical hook) -----------------

    def _importance_rules(self) -> None:
        """MVP_SCOPE §9 owns the rule's shape; the pack owns the numbers.
        The story-critical vocabulary must live in the template vocabulary
        (EVENT_SCHEMA §11) — a typo would silently never match, the
        dead-pack-data failure the lint family guards against (KI#15).
        Every score key must be an int (the rule computes in ints, never
        floats)."""
        rules = self._data["rules.json"]
        section = rules.get("importance")
        if section is None:
            return  # the engine reads the section unconditionally at the
        # first event; a pack without it fails there — nothing more to lint
        where = "importance"
        templates = self._data["templates.json"]["events"]
        for key in ("score", "thresholds"):
            _require(isinstance(section.get(key), Mapping),
                     f"{where}.{key} must be an object")
        story_critical = section.get("story_critical_events", ())
        _require(isinstance(story_critical, list),
                 f"{where}.story_critical_events must be a list")
        for event_type in story_critical:
            _require(
                event_type in templates,
                f"{where}.story_critical_events: {event_type!r} is not in the "
                f"template vocabulary — a typo here never matches any event",
            )
        for key, value in section["score"].items():
            _require(
                isinstance(value, int) and not isinstance(value, bool),
                f"{where}.score.{key} must be an integer",
            )
        thresholds = section["thresholds"]
        for key in ("medium", "high"):
            _require(
                isinstance(thresholds.get(key), int)
                and not isinstance(thresholds[key], bool)
                and thresholds[key] > 0,
                f"{where}.thresholds.{key} must be a positive integer",
            )
        _require(
            thresholds["medium"] <= thresholds["high"],
            f"{where}.thresholds: medium must not exceed high",
        )

    # -- urgencies (P2b, iter-4) -----------------------------------------------

    def _urgencies(self) -> None:
        rules = self._data["rules.json"]
        config = rules.get("urgencies")
        if config is None:
            return
        entities = self._data["entities.json"]
        npc_ids = _ids(entities["npcs"])
        actions = {a["intent"]: a for a in self._data["actions.json"]["actions"]}
        ticks_per_day = rules["time"]["ticks_per_day"]
        _require(
            isinstance(config.get("beat_ticks"), list)
            and all(
                isinstance(t, int) and not isinstance(t, bool)
                and 0 <= t < ticks_per_day
                for t in config["beat_ticks"]
            ),
            "urgencies.beat_ticks must be intraday tick offsets",
        )
        for entry in config.get("entries", ()):
            where = f"urgencies.entries[{entry.get('npc')!r}]"
            _require(entry.get("npc") in npc_ids, f"{where}: unknown npc")
            _require(
                isinstance(entry.get("probability_per_beat"), int)
                and not isinstance(entry.get("probability_per_beat"), bool)
                and 0 <= entry["probability_per_beat"] <= 100,
                f"{where}: probability_per_beat must be 0..100",
            )
            intent = entry.get("intent", {})
            _require(
                isinstance(intent, Mapping)
                and intent.get("kind") in actions,
                f"{where}: intent.kind must name a pack action",
            )
            for key in ("target", "fields"):
                if key in intent:
                    if key == "target" and not isinstance(intent[key], str):
                        raise PackError(
                            f"{where}: intent.target must be a string, "
                            f"got {intent.get('target')!r}"
                        )
                    if key == "fields" and not isinstance(intent[key], Mapping):
                        raise PackError(
                            f"{where}: intent.fields must be a mapping, "
                            f"got {intent.get('fields')!r}"
                        )
            for cond in entry.get("requires", ()):
                _require(
                    cond.get("test") in PRECONDITION_TESTS,
                    f"{where}: unknown precondition test {cond.get('test')!r}",
                )
                if cond.get("test") == ECHO_TEST:
                    self._lint_echo_cond(cond, where)
                for param in ("noun", "with", "who"):
                    if param in cond:
                        _require(
                            cond[param] in _NOUNS,
                            f"{where}: precondition {param} {cond[param]!r} "
                            f"must be one of {list(_NOUNS)}",
                        )

    # -- director (iter-4: consequence buffer + triggers + stagnation) --------

    def _director(self) -> None:
        rules = self._data["rules.json"]
        config = rules.get("director")
        if config is None:
            return
        entities = self._data["entities.json"]
        npc_ids = _ids(entities["npcs"])
        location_ids = _ids(entities["locations"])
        entity_ids = (
            location_ids | npc_ids | _ids(entities["ambient_entities"])
            | _ids(entities["items"])
        )
        relation_axes = set(rules["relations"]["axes"])
        actions = {a["intent"]: a for a in self._data["actions.json"]["actions"]}
        for trigger_kind in config.get("triggers", ()):
            _require(
                trigger_kind in LEAF_KINDS,
                f"director.triggers: unknown kind {trigger_kind!r}",
            )
        stagnation = config.get("stagnation", {})
        _require(
            isinstance(stagnation.get("entropy_floor"), int)
            and not isinstance(stagnation.get("entropy_floor"), bool)
            and stagnation["entropy_floor"] >= 0,
            "director.stagnation.entropy_floor must be a non-negative integer",
        )
        _require(
            isinstance(stagnation.get("per_npc_cooldown_beats"), int)
            and not isinstance(stagnation.get("per_npc_cooldown_beats"), bool)
            and stagnation["per_npc_cooldown_beats"] >= 1,
            "director.stagnation.per_npc_cooldown_beats must be >= 1",
        )
        # iter-36 (DIR-1): the pacing clock's pack contract — peak floor
        # strictly above the stagnation floor (the loud band must not
        # overlap the quiet one), positive minimum durations (anti-flap).
        # iter-38 (DIR-3): the climax layer — the L4D2 three-intensity
        # rule's third threshold, strictly above the peak floor (a
        # climax_floor inside the peak band would swallow the layering).
        pacing = config.get("pacing")
        if pacing is not None:
            _require(
                isinstance(pacing, Mapping),
                "director.pacing must be an object",
            )
            for key in ("peak_floor", "min_peak_beats", "min_rest_beats"):
                _require(
                    isinstance(pacing.get(key), int)
                    and not isinstance(pacing.get(key), bool)
                    and pacing[key] >= 1,
                    f"director.pacing.{key} must be a positive integer",
                )
            _require(
                int(pacing["peak_floor"]) > int(stagnation["entropy_floor"]),
                "director.pacing.peak_floor must sit strictly above "
                "director.stagnation.entropy_floor (the PEAK band is the "
                "loud world, the STAGNATION band the quiet one)",
            )
            climax_floor = pacing.get("climax_floor")
            if climax_floor is not None:
                _require(
                    isinstance(climax_floor, int)
                    and not isinstance(climax_floor, bool)
                    and climax_floor > int(pacing["peak_floor"]),
                    "director.pacing.climax_floor must be an integer "
                    "strictly above director.pacing.peak_floor (the "
                    "climax layer is the third, above the peak — the "
                    "L4D2 layering law)",
                )
        # iter-39 (DIR-4): the multi-channel contract — `director.channels`
        # declares the pacing dimensions (a per-channel quiet floor + the
        # closed input vocabulary CHANNEL_INPUTS, owned by core.director).
        # A hook's channel tag, when present, must name a declared channel
        # when the block exists (a typo check); without the block the tag is
        # inert dormant vocabulary — the climax-flag-without-layer law.
        channels = config.get("channels")
        channel_names: set[str] = set()
        if channels is not None:
            _require(
                isinstance(channels, Mapping),
                "director.channels must be an object",
            )
            for name, spec in channels.items():
                where = f"director.channels[{name!r}]"
                _require(
                    isinstance(spec, Mapping),
                    f"{where}: must be an object",
                )
                _require(
                    isinstance(spec.get("entropy_floor"), int)
                    and not isinstance(spec.get("entropy_floor"), bool)
                    and spec["entropy_floor"] >= 0,
                    f"{where}: entropy_floor must be a non-negative integer",
                )
                inputs = spec.get("inputs", ())
                _require(
                    isinstance(inputs, list)
                    and all(item in CHANNEL_INPUTS for item in inputs),
                    f"{where}: inputs must list channel inputs "
                    f"({' | '.join(CHANNEL_INPUTS)})",
                )
                channel_names.add(str(name))
        for tag, spec in config.get("hooks", {}).items():
            where = f"director.hooks[{tag!r}]"
            # drama-1 (iter-40): the hook weight — flat int or the
            # weight_multiplier object (the shared lint, extracted for
            # drama-2's option weights: `_lint_weight_spec`)
            _lint_weight_spec(
                spec.get("weight"), where, npc_ids, location_ids,
                relation_axes, entity_ids,
            )
            # drama-1: the Wesnoth fire-only-once release policy — boolean
            _require(
                "first_time_only" not in spec
                or isinstance(spec.get("first_time_only"), bool),
                f"{where}: first_time_only must be a boolean",
            )
            # iter-38 (DIR-3): the boss-beat flag — a boolean; a climax
            # hook without a climax_floor layer is legal (explicit-trigger
            # only — the nopacing harness variant is exactly that pack)
            _require(
                "climax" not in spec or isinstance(spec.get("climax"), bool),
                f"{where}: climax must be a boolean",
            )
            # iter-39 (DIR-4): the hook's pacing dimension — a string;
            # with the channels block present it must name a declared
            # channel (a typo check), without the block it is inert
            # dormant vocabulary
            hook_channel = spec.get("channel")
            if channel_names:
                _require(
                    isinstance(hook_channel, str)
                    and hook_channel in channel_names,
                    f"{where}: channel must name a declared "
                    "director.channels entry",
                )
            else:
                _require(
                    hook_channel is None or isinstance(hook_channel, str),
                    f"{where}: channel must be a string",
                )
            _require(
                isinstance(spec.get("release_threshold"), int)
                and not isinstance(spec.get("release_threshold"), bool)
                and spec["release_threshold"] >= 0,
                f"{where}: release_threshold must be a non-negative integer",
            )
            _require(
                spec.get("target_npc") in npc_ids,
                f"{where}: target_npc must name an npc",
            )
            intent = spec.get("intent", {})
            _require(
                isinstance(intent, Mapping)
                and intent.get("kind") in actions,
                f"{where}: intent.kind must name a pack action",
            )
            # iter-43 (D-072): the hook-level payload now carries targets
            # (the document-check pair names the pack's player) — the
            # target lint mirrors the option payload's (the iter-41 note
            # closed its own gap: new vocabulary, its lint complete from
            # day one).
            if "target" in intent:
                _require(
                    intent.get("target") is None or intent.get("target") in entity_ids,
                    f"{where}: intent.target must be null or name an entity",
                )
            trigger = spec.get("trigger")
            if trigger is not None:
                # drama-1 (iter-40): the full predicate grammar — the
                # v0.1 leaf kinds unchanged, plus compound all/any/not
                # forms, the implicit-AND list root, and the generalized
                # `prop` leaf (core/predicates.py owns the vocabulary)
                error = _predicate_error(
                    trigger, f"{where}.trigger", npc_ids, location_ids,
                    relation_axes, entity_ids,
                )
                _require(
                    error is None,
                    error or "unreachable",
                )
            # drama-2 (iter-41): the option layer — each block an
            # availability gate (the drama-1 predicate grammar) + an
            # ai_chance-style weight (the shared weight lint) + a
            # payload override (kind names an action, fields an
            # object, target null or an entity — the option block is
            # new vocabulary, its lint complete from day one; the
            # hook-level intent lint stays kind-only, the pre-existing
            # laxness is not this iteration's scope)
            options = spec.get("options")
            if options is not None:
                _require(
                    isinstance(options, list) and len(options) > 0,
                    f"{where}: options must be a non-empty list",
                )
                for index, option in enumerate(options):
                    owhere = f"{where}.options[{index}]"
                    _require(
                        isinstance(option, Mapping),
                        f"{owhere}: must be an object",
                    )
                    unknown = sorted(set(option) - set(OPTION_KEYS))
                    _require(
                        not unknown,
                        f"{owhere}: unknown option keys {unknown} "
                        f"(the closed vocabulary: {' | '.join(OPTION_KEYS)})",
                    )
                    _require(
                        "notes" not in option
                        or isinstance(option.get("notes"), str),
                        f"{owhere}: notes must be a string",
                    )
                    option_trigger = option.get("trigger")
                    if option_trigger is not None:
                        error = _predicate_error(
                            option_trigger, f"{owhere}.trigger", npc_ids,
                            location_ids, relation_axes, entity_ids,
                        )
                        _require(
                            error is None,
                            error or "unreachable",
                        )
                    if "weight" in option:
                        _lint_weight_spec(
                            option["weight"], owhere, npc_ids,
                            location_ids, relation_axes, entity_ids,
                        )
                    option_intent = option.get("intent")
                    if option_intent is not None:
                        _require(
                            isinstance(option_intent, Mapping),
                            f"{owhere}: intent must be an object",
                        )
                        if "kind" in option_intent:
                            _require(
                                option_intent.get("kind") in actions,
                                f"{owhere}: intent.kind must name a pack action",
                            )
                        if "fields" in option_intent:
                            _require(
                                isinstance(option_intent.get("fields"), Mapping),
                                f"{owhere}: intent.fields must be an object",
                            )
                        if "target" in option_intent:
                            _require(
                                option_intent.get("target") is None
                                or option_intent.get("target") in entity_ids,
                                f"{owhere}: intent.target must be null or "
                                "name an entity",
                            )
        # iter-47 (arc-1, P3c): the arc contract — `director.arcs`
        # declares the release chains (the DF event_collections /
        # Paradox event-chain precedent). Membership is one-sided —
        # the members list IS the declaration (a hook spec carries no
        # arc key; the single owner of the fact, D-024); every member
        # must name a declared hook tag and no tag may ride two arcs
        # (ambiguous order). The gap floor is >= 2: the one-per-beat
        # budget already enforces a one-beat spacing, so a 1 declares
        # nothing — dead vocabulary, refused at load (the empty-
        # compound law's family).
        arcs = config.get("arcs")
        if arcs is not None:
            _require(
                isinstance(arcs, Mapping),
                "director.arcs must be an object keyed by arc name",
            )
            hook_tags = set(config.get("hooks", {}))
            member_arc: dict[str, str] = {}
            for name, spec in arcs.items():
                where = f"director.arcs[{name!r}]"
                _require(
                    isinstance(spec, Mapping),
                    f"{where}: must be an object",
                )
                unknown = sorted(set(spec) - set(ARC_KEYS))
                _require(
                    not unknown,
                    f"{where}: unknown arc keys {unknown} "
                    f"(the closed vocabulary: {' | '.join(ARC_KEYS)})",
                )
                members = spec.get("members")
                _require(
                    isinstance(members, list)
                    and len(members) >= 2
                    and all(isinstance(member, str) for member in members),
                    f"{where}: members must be a list of at least two "
                    "tags (a chain has a successor — a one-member arc "
                    "is dead vocabulary)",
                )
                _require(
                    len(set(members)) == len(members),
                    f"{where}: members must be unique (a doubled tag "
                    "chains to itself)",
                )
                for member in members:
                    _require(
                        member in hook_tags,
                        f"{where}: member {member!r} must name a "
                        "declared director.hooks tag",
                    )
                    _require(
                        member not in member_arc,
                        # the message formats eagerly — .get() keeps the
                        # first-sight member out of the KeyError path
                        f"{where}: member {member!r} already belongs to "
                        f"arc {member_arc.get(member, '')!r} (a tag in two "
                        "arcs has ambiguous order)",
                    )
                    member_arc[member] = str(name)
                _require(
                    isinstance(spec.get("min_gap_beats"), int)
                    and not isinstance(spec.get("min_gap_beats"), bool)
                    and spec["min_gap_beats"] >= 2,
                    f"{where}: min_gap_beats must be an integer >= 2 "
                    "(the 1-per-beat budget already enforces 1 — a "
                    "smaller gap is dead vocabulary)",
                )
                _require(
                    "notes" not in spec or isinstance(spec.get("notes"), str),
                    f"{where}: notes must be a string",
                )

    # -- on_action (drama-3, iter-42: the pack's reaction table) ---------------

    def _on_action(self) -> None:
        """The on_action dispatch contract (DIRECTOR_SPEC §3c the owner;
        core/onaction.py owns the vocabulary constants). The block is
        OPTIONAL — a pack without it runs the v0.1 reaction behavior,
        byte-identically (the pack's own declaration is the gate, INV-3)."""
        rules = self._data["rules.json"]
        config = rules.get("on_action")
        if config is None:
            return
        templates = self._data["templates.json"]["events"]
        status_axes = set(rules["states"])
        relation_axes = set(rules["relations"]["axes"])
        _require(
            isinstance(config, Mapping) and config,
            "on_action must be a non-empty object keyed by event type",
        )
        if "notes" in config:
            _require(
                isinstance(config["notes"], str),
                "on_action.notes must be a string (prose — never a table key)",
            )
        emitted: set[str] = set()  # the reaction event types (the one-hop law)
        for event_type, entries in config.items():
            if event_type == "notes":  # prose commentary, not a table key
                continue
            where = f"on_action[{event_type!r}]"
            # the key must name a declared event type — a typo'd key is
            # silent dead vocabulary otherwise (the closed-set law)
            _require(
                event_type in templates,
                f"{where}: the key must name a template event type",
            )
            # the append law: the value is a LIST — every entry dispatches,
            # a second declaration never replaces the first
            _require(
                isinstance(entries, list) and entries,
                f"{where}: must be a non-empty list of reaction entries "
                "(the append composition — one entry, not a bare object)",
            )
            for index, entry in enumerate(entries):
                error = self._on_action_entry(
                    entry, f"{where}[{index}]", templates,
                    status_axes, relation_axes,
                )
                if error is not None:
                    raise PackError(error)
                emitted.add(entry["event"])
        # the one-hop law: an on_action reaction event never dispatches
        # further on_action reactions — no table key may name a reaction
        # event type the table itself emits (second-order reactions have
        # no v0.1 semantics; the cascade terminates by construction)
        overlap = sorted((set(config) - {"notes"}) & emitted)
        _require(
            not overlap,
            f"on_action: second-order reaction declared — the table keys "
            f"{overlap} are reaction event types it emits itself (v0.1 "
            "dispatches one hop; DIRECTOR_SPEC §3c)",
        )

    def _on_action_entry(
        self,
        entry: Any,
        where: str,
        templates: Mapping[str, Any],
        status_axes: set[str],
        relation_axes: set[str],
    ) -> str | None:
        """Validate one reaction entry; returns the error message or None
        (the `_predicate_error` pattern). The closed key set comes from
        core/onaction.py — the single vocabulary owner."""
        if not isinstance(entry, Mapping):
            return f"{where}: must be an object"
        unknown = sorted(set(entry) - set(ENTRY_KEYS))
        if unknown:
            return (
                f"{where}: unknown entry keys {unknown} (the closed "
                f"vocabulary: {' | '.join(ENTRY_KEYS)})"
            )
        if entry.get("scope") not in SCOPES:
            return (
                f"{where}: scope must be one of {list(SCOPES)} — the entity-set "
                "selector (the explicit ctx argument, never an implicit this)"
            )
        if entry.get("event") not in templates:
            return f"{where}: event must name a template event type"
        state = entry.get("state")
        if not isinstance(state, Mapping) or sorted(state) != sorted(STATE_KEYS):
            return (
                f"{where}: state must be an object with exactly "
                f"{list(STATE_KEYS)} — the scoped state change"
            )
        prop = state.get("prop")
        if not isinstance(prop, str) or not prop:
            return f"{where}: state.prop must be a non-empty string"
        error = self._prop_path_error(prop, f"{where}.state.prop",
                                       status_axes, relation_axes)
        if error is not None:
            return error
        if not _is_int(state.get("add")) or state["add"] == 0:
            return (
                f"{where}: state.add must be a non-zero integer (a zero delta "
                "is dead vocabulary, L1)"
            )
        gate = entry.get("gate")
        if gate is not None:
            if not isinstance(gate, list) or not gate:
                return (
                    f"{where}: gate must be a non-empty list of per-entity "
                    "conditions (an empty gate is dead vocabulary, L1)"
                )
            for gindex, condition in enumerate(gate):
                gwhere = f"{where}.gate[{gindex}]"
                if not isinstance(condition, Mapping) or sorted(condition) != sorted(
                    GATE_KEYS
                ):
                    return (
                        f"{gwhere}: must be an object with exactly "
                        f"{list(GATE_KEYS)} — the quantified predicate's "
                        "per-entity read (the candidate is the argument, "
                        "the spec carries no entity field)"
                    )
                cprop = condition.get("prop")
                if not isinstance(cprop, str) or not cprop:
                    return f"{gwhere}: prop must be a non-empty string"
                error = self._prop_path_error(
                    cprop, f"{gwhere}.prop", status_axes, relation_axes
                )
                if error is not None:
                    return error
                if condition.get("comparator") not in COMPARATORS:
                    return (
                        f"{gwhere}: comparator must be one of "
                        f"{list(COMPARATORS)} (the predicates.py vocabulary)"
                    )
                if condition.get("comparator") in ("at_least", "at_most") and not _is_int(
                    condition.get("value")
                ):
                    return f"{gwhere}: {condition['comparator']} needs an integer value"
                if "value" not in condition:
                    return f"{gwhere}: the condition needs a value"
        for key in ("actor", "target"):
            if key in entry and entry[key] not in ACTOR_TARGET_KEYS:
                return (
                    f"{where}.{key} must be one of {list(ACTOR_TARGET_KEYS)} "
                    "(the source-event resolution vocabulary)"
                )
        if "notes" in entry and not isinstance(entry.get("notes"), str):
            return f"{where}: notes must be a string"
        return None

    # -- secrets & leverage (social-1, P3a — the fact-cluster registry) -----

    def _secrets(self) -> None:
        """The secrets registry contract (`core/leverage.py` owns the
        vocabulary constants; `phases.md` §3 P3a the architecture row).
        The block is OPTIONAL — a pack without it runs the v0.1 reaction
        behavior, byte-identically (the pack's own declaration is the
        gate, INV-3)."""
        rules = self._data["rules.json"]
        config = rules.get("secrets")
        if config is None:
            return
        templates = self._data["templates.json"]["events"]
        npc_ids = {npc["id"] for npc in self._data["entities.json"]["npcs"]}
        if not isinstance(config, Mapping):
            raise PackError("secrets must be an object")
        unknown = sorted(set(config) - set(SECRETS_BLOCK_KEYS))
        if unknown:
            raise PackError(
                f"secrets: unknown keys {unknown} (the closed vocabulary: "
                f"{' | '.join(SECRETS_BLOCK_KEYS)})"
            )
        event_type = config.get("event")
        _require(
            isinstance(event_type, str) and event_type in templates,
            f"secrets.event {event_type!r} is not in the template vocabulary "
            "(EVENT_SCHEMA §11 — the fact event renders in the chronicle)",
        )
        # iter-45 (social-1b): the spend door. The event type must render,
        # must be PRODUCED by a declared action, and every action that
        # produces it must gate on the leverage test — the loop's spend
        # stamping reads the live fold that very test guarantees at
        # completion (an ungated spend would reach the stamping with an
        # empty fold and crash mid-run — the KI#15 family, refused at
        # load instead).
        spend_type = config.get("spend_event")
        if spend_type is not None:
            _require(
                isinstance(spend_type, str) and spend_type in templates,
                f"secrets.spend_event {spend_type!r} is not in the template "
                "vocabulary (EVENT_SCHEMA §11 — the spend renders in the "
                "chronicle)",
            )
            spenders = [
                action for action in self._data["actions.json"]["actions"]
                if action.get("events", {}).get("success") == spend_type
            ]
            _require(
                spenders,
                f"secrets.spend_event {spend_type!r} is no action's success "
                "event — the spend door is dead vocabulary",
            )
            for action in spenders:
                intent = action.get("intent")
                _require(
                    any(
                        cond.get("test") == LEVERAGE_TEST
                        for cond in action.get("requires", ())
                    ),
                    f"action {intent!r} spends leverage (its success event is "
                    f"secrets.spend_event) but carries no leverage_over "
                    "precondition — the door would not guarantee a live "
                    "cluster at completion",
                )
        if "notes" in config:
            _require(
                isinstance(config["notes"], str),
                "secrets.notes must be a string (prose — never a table key)",
            )
        tokens = config.get("tokens")
        _require(
            isinstance(tokens, Mapping) and tokens,
            "secrets.tokens must be a non-empty object keyed by knowledge "
            "token",
        )
        mintable = self._literal_knows_tokens()
        for token, spec in tokens.items():
            where = f"secrets.tokens[{token!r}]"
            # a token nobody can ever learn is dead vocabulary — the token
            # must be minted by a declared knowledge template (the closed-set
            # law; templated tokens are ineligible by construction: a
            # secret's subject must be a fixed entity, a templated token's
            # subject varies with the world)
            _require(
                token in mintable,
                f"{where}: no declared knowledge template mints this token "
                "(the literal `knows` vocabulary: actions / expectations / "
                "transition layers)",
            )
            _require(
                isinstance(spec, Mapping),
                f"{where}: must be an object",
            )
            unknown_token = sorted(set(spec) - set(TOKEN_KEYS))
            if unknown_token:
                raise PackError(
                    f"{where}: unknown keys {unknown_token} (the closed "
                    f"vocabulary: {' | '.join(TOKEN_KEYS)})"
                )
            _require(
                spec.get("subject") in npc_ids,
                f"{where}: subject must be an npc id — the cluster targets "
                "a social actor",
            )
            _require(
                isinstance(spec.get("type"), str) and spec["type"].strip(),
                f"{where}: type must be a non-empty string (the donor's "
                "add_hook type — v0.1 vocabulary, no consumer yet)",
            )
            _require(
                _is_int(spec.get("expires_ticks")) and spec["expires_ticks"] > 0,
                f"{where}: expires_ticks must be a positive integer (the "
                "donor's days — the read-side liveness window)",
            )

    def _echo(self) -> None:
        """The psychological echo contract (`core/echo.py` owns the
        vocabulary constants; `phases.md` §3 P3e the architecture row).
        The block is OPTIONAL — a pack without it folds no residue and
        runs the v0.1 behavior, byte-identically (the pack's own
        declaration is the gate, INV-3). Declaring the table costs
        nothing at runtime until a consumer reads it (the iter-45
        laziness law: the fold runs only for intents whose preconditions
        carry the echo test)."""
        rules = self._data["rules.json"]
        config = rules.get("echo")
        if config is None:
            return
        if not isinstance(config, Mapping):
            raise PackError("echo must be an object")
        unknown = sorted(set(config) - set(ECHO_BLOCK_KEYS))
        if unknown:
            raise PackError(
                f"echo: unknown keys {unknown} (the closed vocabulary: "
                f"{' | '.join(ECHO_BLOCK_KEYS)})"
            )
        # the scale: [lo, hi] — the per-axis sums clamp to it
        scale = config.get("scale")
        _require(
            isinstance(scale, list)
            and len(scale) == 2
            and all(_is_int(bound) for bound in scale)
            and scale[0] < scale[1],
            "echo.scale must be [lo, hi] integers with lo < hi "
            "(the residue clamp bounds)",
        )
        # the fidelity percents: closed against the pack's own fidelity
        # chain — a chain member without a percent would KeyError at the
        # fold (the KI#15 family, refused at load instead)
        chain = rules["knowledge"]["fidelity_chain"]
        percents = config.get("fidelity_weight")
        _require(
            isinstance(percents, Mapping)
            and sorted(percents) == sorted(chain)
            and all(
                _is_int(percents[step]) and 0 < percents[step] <= 100
                for step in percents
            ),
            f"echo.fidelity_weight must map every fidelity chain member "
            f"({list(chain)}) to a percent in 1..100 — a missing step "
            "would KeyError at the fold",
        )
        if "notes" in config:
            _require(
                isinstance(config["notes"], str),
                "echo.notes must be a string (prose — never a table key)",
            )
        tokens = config.get("tokens")
        _require(
            isinstance(tokens, Mapping) and tokens,
            "echo.tokens must be a non-empty object keyed by knowledge "
            "token",
        )
        mintable = self._literal_knows_tokens()
        for token, spec in tokens.items():
            where = f"echo.tokens[{token!r}]"
            # the secrets lint's law: a token nobody can ever learn is
            # dead vocabulary — the residue must ride a declared
            # knowledge template
            _require(
                token in mintable,
                f"{where}: no declared knowledge template mints this "
                "token (the literal `knows` vocabulary: actions / "
                "expectations / transition layers)",
            )
            _require(isinstance(spec, Mapping), f"{where}: must be an object")
            unknown_token = sorted(set(spec) - set(ECHO_TOKEN_KEYS))
            if unknown_token:
                raise PackError(
                    f"{where}: unknown keys {unknown_token} (the closed "
                    f"vocabulary: {' | '.join(ECHO_TOKEN_KEYS)})"
                )
            _require(
                _is_int(spec.get("fades_ticks")) and spec["fades_ticks"] > 0,
                f"{where}: fades_ticks must be a positive integer (the "
                "residue's lifetime — dead at the boundary tick itself)",
            )
            axes = spec.get("axes")
            _require(
                isinstance(axes, Mapping)
                and axes
                and all(
                    _is_int(weight) and weight != 0 for weight in axes.values()
                ),
                f"{where}: axes must be a non-empty object of non-zero "
                "integer valence weights (valence has a sign; zero is "
                "dead vocabulary)",
            )

    def _lint_echo_cond(self, cond: Mapping[str, Any], where: str) -> None:
        """The echo_at_least precondition contract, shared by the action
        and urgency `requires` lints: `axis` must name a declared echo
        axis and `value` must sit strictly above the scale floor and at
        or below the ceiling — outside those bounds the gate can never
        pass (score clamps into the scale) or never fails (always above
        the floor), dead vocabulary either way, refused at load."""
        echo_cfg = self._data["rules.json"].get("echo")
        axes: set[str] = set()
        if isinstance(echo_cfg, Mapping):
            for spec in echo_cfg.get("tokens", {}).values():
                if isinstance(spec, Mapping):
                    axes.update(spec.get("axes", ()))
        _require(
            bool(axes) and cond.get("axis") in axes,
            f"{where}: precondition echo_at_least requires 'axis' naming "
            "a declared echo axis (the fold scores only the declared "
            "vocabulary — anything else is dead data)",
        )
        lo, hi = echo_cfg["scale"]
        _require(
            _is_int(cond.get("value")) and lo < cond["value"] <= hi,
            f"{where}: precondition echo_at_least value must be an "
            f"integer in {lo + 1}..{hi} (the score clamps to the scale — "
            "outside it the gate is dead vocabulary)",
        )

    def _literal_knows_tokens(self) -> set[str]:
        """Every knowledge token the pack can mint as a literal string:
        the `knows` values declared without slot braces across the three
        birth sites — action knowledge templates (all branches + the
        texture path), expectation rules, and transition-layer knowledge
        entries. The reaction systems (telling, crime) only transfer
        existing tokens, so this IS the birth vocabulary; templated
        values (containing `{`) are excluded — a secret's subject is a
        fixed entity, and a templated token's subject varies with the
        world."""
        tokens: set[str] = set()

        def _take(entry: Any) -> None:
            knows = entry.get("knows") if isinstance(entry, Mapping) else None
            if isinstance(knows, str) and "{" not in knows:
                tokens.add(knows)

        for action in self._data["actions.json"]["actions"]:
            knowledge = action.get("knowledge", {})
            if isinstance(knowledge, Mapping):
                for branch in knowledge.values():
                    if isinstance(branch, list):
                        for entry in branch:
                            _take(entry)
            texture = action.get("texture", {})
            if isinstance(texture, Mapping):
                for branch in texture.get("knowledge", {}).values():
                    if isinstance(branch, list):
                        for entry in branch:
                            _take(entry)
        rules = self._data["rules.json"]
        for rule in rules.get("expectations", {}).get("rules", ()):
            if isinstance(rule, Mapping):
                _take(rule)
        for config in rules.get("transitions", {}).values():
            if isinstance(config, Mapping):
                for entry in config.get("knowledge", {}).values():
                    _take(entry)
        return tokens

    def _prop_path_error(
        self,
        prop: str,
        where: str,
        status_axes: set[str],
        relation_axes: set[str],
    ) -> str | None:
        """The prop-path known-prefix gate: a `relations.X` path must name
        a declared axis, a `status.X` path must name a declared status
        axis — everything else is the open projection vocabulary (layer
        flags, spot props). The runtime drops candidates without a
        numeric home on the path (the suspicion law); this gate catches
        the pack-author typo before it becomes a silent no-op."""
        if prop.startswith("relations."):
            axis = prop[len("relations."):]
            if axis not in relation_axes:
                return f"{where}: {prop!r} does not name a relations axis"
        if prop.startswith("status."):
            axis = prop[len("status."):]
            if axis not in status_axes:
                return f"{where}: {prop!r} does not name a status axis"
        return None

    # -- brief (iter-8: the phase-1 assembler contract, BRIEF_SPEC §6) --------

    def _brief(self) -> None:
        config = self._data["rules.json"].get("brief")
        if config is None:
            raise PackError(
                "rules.json: the brief section is required (phase-1 contract, "
                "BRIEF_SPEC §6)"
            )
        where = "rules.json::brief"
        blocks = config.get("blocks")
        _require(isinstance(blocks, Mapping), f"{where}: 'blocks' must be an object")
        _require(
            set(blocks) == set(BRIEF_BLOCK_IDS),
            f"{where}: blocks must be exactly {list(BRIEF_BLOCK_IDS)}, "
            f"got {sorted(blocks)}",
        )
        for block_id, budget in blocks.items():
            _require(
                isinstance(budget, Mapping),
                f"{where}.blocks[{block_id!r}]: budget must be an object",
            )
            for key in ("soft", "hard"):
                value = budget.get(key)
                _require(
                    isinstance(value, int) and not isinstance(value, bool) and value > 0,
                    f"{where}.blocks[{block_id!r}]: {key} must be a positive integer",
                )
            _require(
                budget["soft"] <= budget["hard"],
                f"{where}.blocks[{block_id!r}]: soft must be <= hard",
            )
        total = config.get("total_hard")
        _require(
            isinstance(total, int) and not isinstance(total, bool) and total > 0,
            f"{where}: total_hard must be a positive integer",
        )
        directives = config.get("directives")
        _require(
            isinstance(directives, list)
            and directives
            and all(isinstance(line, str) and line.strip() for line in directives),
            f"{where}: directives must be a non-empty list of non-empty strings",
        )
        # Never-dropped data must fit by construction (BRIEF_SPEC §6):
        # the fill law never applies to directives, so their own hard
        # budget is the only ceiling they have.
        directives_tokens = sum(len(line.split()) for line in directives)
        _require(
            directives_tokens <= blocks["directives"]["hard"],
            f"{where}: directives ({directives_tokens} tokens) exceed their own "
            f"hard budget {blocks['directives']['hard']}",
        )
        lore = config.get("lore")
        _require(isinstance(lore, list), f"{where}: lore must be a list")
        seen_ids: set[str] = set()
        for entry in lore:
            _require(isinstance(entry, Mapping), f"{where}.lore: entries must be objects")
            entry_id = entry.get("id")
            _require(
                isinstance(entry_id, str) and entry_id.strip() and entry_id not in seen_ids,
                f"{where}.lore: ids must be unique non-empty strings, got {entry_id!r}",
            )
            seen_ids.add(entry_id)
            where_entry = f"{where}.lore[{entry_id!r}]"
            _require(
                isinstance(entry.get("text"), str) and entry["text"].strip(),
                f"{where_entry}: text must be a non-empty string",
            )
            for key in ("from_beat", "to_beat"):
                value = entry.get(key)
                _require(
                    isinstance(value, int) and not isinstance(value, bool) and value >= 0,
                    f"{where_entry}: {key} must be a non-negative integer",
                )
            _require(
                entry["from_beat"] < entry["to_beat"],
                f"{where_entry}: from_beat must be < to_beat",
            )
        exemplars = config.get("voice_exemplars")
        _require(
            isinstance(exemplars, list)
            and all(isinstance(line, str) and line.strip() for line in exemplars),
            f"{where}: voice_exemplars must be a list of non-empty strings",
        )
        recalled = config.get("recalled_facts")
        _require(
            isinstance(recalled, Mapping),
            f"{where}: recalled_facts must be an object",
        )
        for key in ("recency_weight", "importance_weight"):
            value = recalled.get(key)
            _require(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and value >= 0,
                f"{where}.recalled_facts: {key} must be a non-negative number",
            )
        max_items = recalled.get("max_items")
        _require(
            isinstance(max_items, int) and not isinstance(max_items, bool) and max_items >= 1,
            f"{where}.recalled_facts: max_items must be an integer >= 1",
        )
        # iter-10: the 7th block's ranking caps + the unique-slot flag set
        # (BRIEF_SPEC §3.3/§6 — the scene-texture window law, D-049).
        texture = config.get("scene_texture")
        _require(isinstance(texture, Mapping), f"{where}: scene_texture must be an object")
        for key in ("max_items", "tombstone_max_items"):
            value = texture.get(key)
            _require(
                isinstance(value, int) and not isinstance(value, bool) and value >= 1,
                f"{where}.scene_texture: {key} must be an integer >= 1",
            )
        unique_slots = texture.get("unique_slots")
        _require(
            isinstance(unique_slots, list)
            and all(
                isinstance(slot, str) and slot.strip() and slot not in unique_slots[: index]
                for index, slot in enumerate(unique_slots)
            ),
            f"{where}.scene_texture: unique_slots must be unique non-empty strings",
        )
        # st-1: the 8th block's ranking caps + the observable-marker table
        # (BRIEF_SPEC §3.8/§6 — the entity-card block). Marker names are
        # pack vocabulary (INV-3); the axis must be a known status axis of
        # the pack's states section.
        present = config.get("present_entities")
        _require(
            isinstance(present, Mapping),
            f"{where}: present_entities must be an object",
        )
        for key in ("max_entities", "max_pairs"):
            value = present.get(key)
            _require(
                isinstance(value, int) and not isinstance(value, bool) and value >= 1,
                f"{where}.present_entities: {key} must be an integer >= 1",
            )
        markers = present.get("card_markers")
        _require(
            isinstance(markers, list),
            f"{where}.present_entities: card_markers must be a list",
        )
        state_axes = set(self._data["rules.json"].get("states", {})) - {"notes"}
        relation_axes = set(self._data["rules.json"].get("relations", {}).get(
            "axes", ()
        ))
        for marker in markers:
            _require(
                isinstance(marker, Mapping),
                f"{where}.present_entities.card_markers: entries must be objects",
            )
            where_marker = (
                f"{where}.present_entities.card_markers[{marker.get('prop')!r}]"
            )
            # tune-2 (D-060): prop-path keyed, two row kinds. The closed
            # prefix set keeps the table honest — a typo'd prop is dead
            # data (the marker silently never renders), the KI#15 family.
            prop = marker.get("prop")
            _require(isinstance(prop, str) and prop.strip(),
                     f"{where_marker}: prop must be a non-empty string")
            if prop.startswith("status."):
                _require(
                    prop[len("status."):] in state_axes,
                    f"{where_marker}: status axis "
                    f"{prop[len('status.'):]!r} is not one of the pack's "
                    f"states axes {sorted(state_axes)}",
                )
            elif prop.startswith("relations."):
                _require(
                    prop[len("relations."):] in relation_axes,
                    f"{where_marker}: relations axis "
                    f"{prop[len('relations.'):]!r} is not one of the pack's "
                    f"relations axes {sorted(relation_axes)}",
                )
            else:
                _require(
                    prop == "crime_status",
                    f"{where_marker}: prop must be status.<axis>, "
                    f"relations.<axis>, or crime_status (the closed marker "
                    f"surface; grow it only with a real need, L13)",
                )
            has_min, has_value = "min" in marker, "value" in marker
            _require(
                has_min != has_value,
                f"{where_marker}: exactly one of min (threshold row) or "
                f"value (value row) is required",
            )
            if has_min:
                threshold = marker["min"]
                _require(
                    isinstance(threshold, int)
                    and not isinstance(threshold, bool) and threshold >= 0,
                    f"{where_marker}: min must be a non-negative integer",
                )
            else:
                _require(
                    isinstance(marker["value"], str) and marker["value"].strip(),
                    f"{where_marker}: value must be a non-empty string",
                )
            _require(
                isinstance(marker.get("marker"), str) and marker["marker"].strip(),
                f"{where_marker}: marker must be a non-empty string",
            )
        # iter-20/D-057: pack-declared location fields the scene line
        # renders canon-from-birth (the st-6 layout answer — no projection
        # seeding; canon_slot already guards pack-modeled fields).
        scene_fields = present.get("scene_line_fields")
        _require(
            isinstance(scene_fields, list)
            and all(
                isinstance(field, str) and field.strip() for field in scene_fields
            ),
            f"{where}.present_entities: scene_line_fields must be a list of "
            f"non-empty strings",
        )
        _require(
            len(set(scene_fields)) == len(scene_fields),
            f"{where}.present_entities: scene_line_fields must be unique",
        )
        location_fields = {
            key
            for location in self._data["entities.json"]["locations"]
            for key in location
        }
        _require(
            all(field in location_fields for field in scene_fields),
            f"{where}.present_entities: scene_line_fields must reference "
            f"location fields of the pack",
        )


@dataclass(frozen=True, slots=True)
class Pack:
    """Loaded, linted pack: the setting as read-only data (INV-3)."""

    data: Mapping[str, Mapping[str, Any]]

    @property
    def name(self) -> str:
        return self.data["entities.json"]["meta"]["pack"]

    @property
    def version(self) -> str:
        return self.data["entities.json"]["meta"]["version"]

    @property
    def name_version(self) -> str:
        return f"{self.name}@{self.version}"

    @property
    def entities(self) -> Mapping[str, Any]:
        return self.data["entities.json"]

    @property
    def rules(self) -> Mapping[str, Any]:
        return self.data["rules.json"]

    @property
    def templates(self) -> Mapping[str, Any]:
        return self.data["templates.json"]

    def entity(self, entity_id: str) -> Mapping[str, Any] | None:
        """The pack record for an entity id, or None (any category)."""
        for category in ("locations", "npcs", "ambient_entities", "items"):
            for record in self.entities[category]:
                if record["id"] == entity_id:
                    return record
        return None

    def kind_of(self, entity_id: str) -> str | None:
        """The entity category: location | npc | ambient | item, or None."""
        for category, kind in (
            ("locations", "location"),
            ("npcs", "npc"),
            ("ambient_entities", "ambient"),
            ("items", "item"),
        ):
            for record in self.entities[category]:
                if record["id"] == entity_id:
                    return kind
        return None

    def action(self, intent: str) -> Mapping[str, Any] | None:
        """The action record for an intent type, or None."""
        for action in self.data["actions.json"]["actions"]:
            if action["intent"] == intent:
                return action
        return None

    def event_types(self) -> frozenset[str]:
        """The pack's closed event-type vocabulary (templates own it in
        phase 0 — every type the slice can produce has a chronicle line)."""
        return frozenset(self.templates["events"])

    def player_id(self) -> str:
        """The single is_player entity id."""
        for npc in self.entities["npcs"]:
            if npc.get("is_player", False):
                return npc["id"]
        raise PackError("no is_player npc in pack")


def load_pack(pack_dir: Path) -> Pack:
    """Load the fixed 4-file pack directory and run the minimum lint."""
    present = {path.name for path in pack_dir.glob("*.json")}
    _require(
        present == set(PACK_FILE_NAMES),
        f"{pack_dir}: expected exactly {list(PACK_FILE_NAMES)}, found {sorted(present)}",
    )
    data: dict[str, Mapping[str, Any]] = {}
    for name in sorted(PACK_FILE_NAMES):  # INV-2: sorted() load order
        with (pack_dir / name).open(encoding="utf-8") as fh:
            data[name] = json.load(fh)
    _Lint(data).run()
    return Pack(data=data)
