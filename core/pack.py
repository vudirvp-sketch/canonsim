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
vocabulary, and the system-pass DAG (an ambiguity fails at load —
`core/scheduler.py`). `"_"` commentary fields are ignored wherever
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
from core.intent import (
    AUDIENCES,
    KNOWLEDGE_SLOTS,
    PRECONDITION_TESTS,
    REJECTION_EVENT,
)
from core.resolvers import REGISTRY
from core.scheduler import ScheduleAmbiguityError, build, decls_from_rules

__all__ = ["PACK_FILE_NAMES", "Pack", "PackError", "load_pack"]

PACK_FILE_NAMES: Final = ("actions.json", "entities.json", "rules.json", "templates.json")

_SNAKE_CASE: Final = re.compile(r"^[a-z][a-z0-9_]*$")
_SLOT: Final = re.compile(r"\{([a-z_]+)\}")
_EXCEPT_TOKENS: Final = ("actor", "target", "cause_actor")
_NOUNS: Final = ("actor", "target")


class PackError(RuntimeError):
    """Load-time lint failure — the pack never reaches the simulation."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PackError(message)


def _ids(records: list[Mapping[str, Any]]) -> set[str]:
    return {record["id"] for record in records}


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
            for key in ("smoke", "burnout"):
                _require(
                    isinstance(config[key].get("after_ticks"), int)
                    and config[key]["after_ticks"] >= 0,
                    f"{where}: {key} after_ticks must be a non-negative integer",
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
        relation_axes = set(rules["relations"]["axes"])
        actions = {a["intent"]: a for a in self._data["actions.json"]["actions"]}
        for trigger_kind in config.get("triggers", ()):
            _require(
                trigger_kind in ("time", "place", "threshold"),
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
        for tag, spec in config.get("hooks", {}).items():
            where = f"director.hooks[{tag!r}]"
            _require(
                isinstance(spec.get("weight"), int)
                and not isinstance(spec.get("weight"), bool)
                and spec["weight"] >= 0,
                f"{where}: weight must be a non-negative integer",
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
            trigger = spec.get("trigger")
            if trigger is not None:
                _require(
                    trigger.get("kind") in ("time", "place", "threshold"),
                    f"{where}: trigger.kind must be time|place|threshold",
                )
                if trigger["kind"] == "time":
                    _require(
                        isinstance(trigger.get("tick"), int)
                        and not isinstance(trigger.get("tick"), bool)
                        and trigger["tick"] >= 0,
                        f"{where}: time trigger needs a non-negative tick",
                    )
                elif trigger["kind"] == "place":
                    _require(
                        trigger.get("target_npc") in npc_ids
                        and trigger.get("location") in _ids(entities["locations"]),
                        f"{where}: place trigger needs target_npc + location",
                    )
                elif trigger["kind"] == "threshold":
                    _require(
                        trigger.get("target_npc") in npc_ids
                        and trigger.get("axis") in relation_axes
                        and trigger.get("comparator") in ("at_least", "at_most")
                        and isinstance(trigger.get("value"), int)
                        and not isinstance(trigger.get("value"), bool),
                        f"{where}: threshold trigger needs target_npc + axis + "
                        f"comparator + integer value",
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
