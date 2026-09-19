"""The entity-graph lint: pack meta agreement, the entity categories,
the exits graph's symmetry and orphan law, the birth flags (the D-175
split's entities family)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.packlint.helpers import _ids, _require


class EntitiesLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

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
        # depth-6 (D-112's "one id, all tiers"): the GROUP category —
        # OPTIONAL (the 68a pattern: the committed pack declares no
        # groups, zero factions, the v0.1 bytes untouched; a group is a
        # pack entity acting through the intent door, never a body in
        # a scene — presence views never list it).
        groups = entities.get("groups", ())

        all_ids = (
            _ids(locations) | _ids(npcs) | _ids(ambients) | _ids(items)
            | _ids(groups)
        )
        total = sum(map(len, (locations, npcs, ambients, items, groups)))
        _require(len(all_ids) == total, "entity ids are not unique across categories")

        location_ids = _ids(locations)
        by_location = {loc["id"]: loc for loc in locations}
        for loc in locations:
            # KI#83 (the KI#82 family, the pred-contract law): a MISSING
            # `exits` key died with a raw KeyError — the missing-field
            # loop names the location, never the host's exception.
            _require(
                isinstance(loc.get("exits"), list),
                f"location {loc['id']}: missing or non-list exits",
            )
            for exit_id in loc["exits"]:
                _require(exit_id in location_ids, f"location {loc['id']}: orphan exit {exit_id}")
                _require(
                    loc["id"] in by_location[exit_id]["exits"],
                    f"exit graph asymmetric: {loc['id']} -> {exit_id}",
                )
            # depth-1b (iter-74): pack-declared birth flags seed the
            # projection as raw site props (core/fold.py) — the closed
            # shape the acquisition gate's when_flag/unless_flag read.
            flags = loc.get("flags")
            if flags is not None:
                _require(
                    isinstance(flags, Mapping),
                    f"location {loc['id']}: flags must be an object "
                    "(pack-declared site props)",
                )
                for key, value in flags.items():
                    _require(
                        isinstance(key, str) and key.strip(),
                        f"location {loc['id']}: flag names must be "
                        "non-empty strings",
                    )
                    _require(
                        isinstance(value, (str, int, bool)),
                        f"location {loc['id']}: flag {key!r} must be a "
                        "scalar (str | int | bool) — comparable values "
                        "only, never nested objects",
                    )

        status_axes = set(rules["states"])
        relation_axes = set(rules["relations"]["axes"])
        relation_scale = rules["relations"]["scale"]
        crime_status_values = set(rules["crime_watch"].get("status_values", ()))
        item_ids = _ids(items)
        npc_ids = _ids(npcs)
        # depth-6: the group record's contract — an anchor on the exits
        # graph (a vertex, the spatial model's law) and a static
        # member list over declared npcs (the pack's initial
        # condition). depth-7: the tier vocabulary — the optional
        # macro-tick aggregate + condensation event types (both in
        # the template closure, EVENT_SCHEMA §11; both refused on a
        # memberless group — the dead-data law, a population of
        # nobody never carries a count and never births).
        group_templates = self._data["templates.json"]["events"]
        for group in groups:
            where = f"group {group['id']}"
            _require(
                group.get("position") in location_ids,
                f"{where}: unknown position {group.get('position')!r}",
            )
            members = group.get("members")
            _require(
                isinstance(members, list),
                f"{where}: members must be a list (the membership's "
                "explicit initial condition, possibly empty)",
            )
            seen_members: set[str] = set()
            for member in members:
                _require(
                    member in npc_ids,
                    f"{where}: member {member!r} is not a declared npc",
                )
                _require(
                    member not in seen_members,
                    f"{where}: duplicate member {member!r}",
                )
                seen_members.add(member)
            if "name" in group:
                _require(
                    isinstance(group["name"], str),
                    f"{where}: name must be a string",
                )
            for tier_key in ("macro_event", "condense_event"):
                event_type = group.get(tier_key)
                if event_type is None:
                    continue  # the per-group unarmed law (the 68a pattern)
                _require(
                    isinstance(event_type, str)
                    and event_type in group_templates,
                    f"{where}: {tier_key} {event_type!r} is not in the "
                    "template vocabulary (EVENT_SCHEMA §11 — the tier "
                    "events are pack-declared)",
                )
                _require(
                    bool(members),
                    f"{where}: {tier_key} on a memberless group is dead "
                    "data — the population tier needs a membership (the "
                    "vacuity law, the threshold-100 family)",
                )
            unknown = sorted(
                set(group)
                - {
                    "id", "name", "position", "members",
                    "macro_event", "condense_event", "notes",
                }
            )
            _require(
                not unknown,
                f"{where}: unknown keys {unknown} (the closed "
                "vocabulary: id | name | position | members | "
                "macro_event | condense_event | notes)",
            )
        for npc in npcs:
            _require(npc["position"] in location_ids, f"npc {npc['id']}: unknown position")
            # pack-ci (iter-117, PACK_SPEC §6 AP-9): the SPINE record —
            # want/need tension + flaw rooted in a cause. OPTIONAL (the
            # 68a pattern: absent = the check silent; world-2 L2 is the
            # crosswalk's first consumer per D-148). All-or-nothing: a
            # half-declared spine is a broken spine, refused here — the
            # consumption cross-check (AP-8) lives in _live_char.
            spine = npc.get("spine")
            if spine is not None:
                where = f"npc {npc['id']}: spine"
                _require(
                    isinstance(spine, Mapping),
                    f"{where} must be an object (want | need | flaw | cause)",
                )
                unknown = sorted(set(spine) - {"want", "need", "flaw", "cause", "notes"})
                _require(
                    not unknown,
                    f"{where}: unknown keys {unknown} (the closed vocabulary: "
                    "want | need | flaw | cause | notes)",
                )
                for field in ("want", "need", "flaw", "cause"):
                    _require(
                        isinstance(spine.get(field), str)
                        and bool(spine[field].strip()),
                        f"{where}.{field} is required and must be a non-empty "
                        f"string (AP-9: the want/need tension and the flaw "
                        f"rooted in a cause are the four load-bearing fields)",
                    )
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
