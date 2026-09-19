"""The cross-block admission lints (pack-ci, D-152): the teleology gate
and the live-char crosswalk — the packlint tail, running after every
block lint (the D-175 split's admission family)."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from core.intent import REJECTION_EVENT
from core.packlint.helpers import PackError, _require
from core.resolvers import STATE_MUTATING
from core.states import DECAY_EVENT


class AdmissionLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _teleology(self) -> None:
        """pack-ci (iter-117): the PACK_SPEC §5 admission rows — dead
        action types, orphan entities, empty intersection-matrix rows,
        declared-but-unused templates. The UAP audit's gate as
        deterministic lint: every declared thing must be able to produce
        an observable consequence, or it is dead content."""
        rules = self._data["rules.json"]
        entities = self._data["entities.json"]
        actions = self._data["actions.json"]["actions"]
        templates = self._data["templates.json"]["events"]
        # -- §5 row 1: dead action types --------------------------------
        # an action is dead iff NONE of its declared effect surfaces is
        # armed AND no on_action reaction awaits its event types AND no
        # system_of_type row reacts to them AND its resolver is not an
        # intrinsic state mutator (core/resolvers.py::STATE_MUTATING —
        # those events carry state changes by construction)
        on_action_types = {
            event_type for event_type in (rules.get("on_action") or {})
            if event_type != "notes"
            and isinstance((rules.get("on_action") or {})[event_type], list)
        }
        system_of_type = (rules.get("metrics") or {}).get("system_of_type") or {}
        for action in actions:
            intent = action["intent"]
            alive = (
                bool(action.get("status_effects"))
                or bool(action.get("balance"))
                or bool(action.get("ignition"))
                or any(
                    records
                    for records in (action.get("knowledge") or {}).values()
                )
                or any(
                    records
                    for records in (
                        (action.get("texture") or {}).get("knowledge", {})
                    ).values()
                )
                or any(action.get("hooks", {}).values())
                or action.get("resolver") in STATE_MUTATING
            )
            if not alive:
                for event_type in (action.get("events") or {}).values():
                    if isinstance(event_type, str) and (
                        event_type in on_action_types
                        or system_of_type.get(event_type)
                    ):
                        alive = True
                        break
            _require(
                alive,
                f"action {intent}: dead action type — the events carry no "
                f"state change, no knowledge, no seed and no on_action "
                f"reaction (PACK_SPEC §5; resolver {action.get('resolver')!r} "
                f"is not a state mutator)",
            )
        # -- §5 row 2: orphan entities ----------------------------------
        references = self._reference_strings()
        edged = self._edged_locations()
        audiences = self._dynamic_audience_declared()
        read_flags = self._read_item_flags(actions)
        for category, kind in (
            ("locations", "location"),
            ("npcs", "npc"),
            ("ambient_entities", "ambient"),
            ("items", "item"),
        ):
            for record in entities.get(category, ()):
                entity_id = record["id"]
                if entity_id in references:
                    continue
                touched = False
                if kind == "location":
                    touched = entity_id in edged
                elif kind in ("npc", "ambient"):
                    # knowers: reachable through any positional audience
                    # declared anywhere in the grammar, from an edged
                    # position (the reference walk missed them by name)
                    touched = audiences and record.get("position") in edged
                else:  # items: the target grammar can address them
                    touched = self._item_grammar_reachable(record, edged, read_flags)
                _require(
                    touched,
                    f"entity {entity_id}: orphan — no event, position read "
                    f"or template ever touches it (PACK_SPEC §5; the "
                    f"reference graph, the exits edges, the audiences and "
                    f"the target grammar all miss a {kind})",
                )
        # -- §5 row 3: empty intersection-matrix rows --------------------
        # the matrix's exercised pairs are the urgency entries; the row
        # check reads the wider authored-surface inventory — an NPC with
        # an all-empty row is never deliberately exercised (the player is
        # exempt: the walkthrough's own actor, MVP_SCOPE §3)
        exercised = self._exercised_npcs()
        for npc in entities["npcs"]:
            if npc.get("is_player"):
                continue
            _require(
                npc["id"] in exercised,
                f"npc {npc['id']}: the intersection-matrix row is empty — "
                f"no urgency entry, watch slot, expectation, hook target, "
                f"pair relation or carrier binding exercises them "
                f"(PACK_SPEC §5)",
            )
        # -- §5 row 4: declared-but-unused templates ---------------------
        witnesses = self._emission_witnesses()
        for event_type in sorted(templates):
            _require(
                event_type in witnesses,
                f"templates: {event_type!r} is declared but unused — no "
                f"emission site, core constant or story-critical listing "
                f"renders it (PACK_SPEC §5; dead vocabulary)",
            )

    # -- pack-ci (iter-117): the live-char crosswalk (PACK_SPEC §6) --------


    def _live_char(self) -> None:
        """pack-ci (iter-117): the PACK_SPEC §6 rows — the AP crosswalk
        (AP-1 budgets, AP-8 flaw consumption, AP-9 spine shape [in
        _entities], AP-11 clone pairs, AP-13 contradictory reactions,
        AP-15 predicate atomicity) and the price-marker lint (AP-2's
        design-time half). The AP-9/1/8 rows are conditional on their
        optional data (the 68a pattern — world-2 L2 the first consumer,
        D-148); AP-11/13/15 and the price markers read the standing
        blocks and are always live."""
        rules = self._data["rules.json"]
        entities = self._data["entities.json"]
        actions = self._data["actions.json"]["actions"]
        # -- AP-1: pack size budgets -------------------------------------
        # optional metadata block: {npcs, items, hooks, templates}, each
        # {min, max} — counts within declared bounds, or the pack has
        # outgrown (or underfilled) its own declared shape
        budget = rules.get("budget")
        if budget is not None:
            where = "budget"
            _require(
                isinstance(budget, Mapping),
                f"{where}: must be an object (npcs | items | hooks | templates)",
            )
            unknown = sorted(set(budget) - {"npcs", "items", "hooks", "templates", "notes"})
            _require(
                not unknown,
                f"{where}: unknown keys {unknown} (the closed vocabulary: "
                "npcs | items | hooks | templates | notes)",
            )
            counts = {
                "npcs": len(entities.get("npcs", ())),
                "items": len(entities.get("items", ())),
                "hooks": len((rules.get("director") or {}).get("hooks", {})),
                "templates": len(self._data["templates.json"].get("events", {})),
            }
            for key, count in counts.items():
                bounds = budget.get(key)
                if bounds is None:
                    continue
                _require(
                    isinstance(bounds, Mapping),
                    f"{where}.{key}: must be an object (min | max)",
                )
                _require(
                    sorted(set(bounds)) == ["max", "min"],
                    f"{where}.{key}: exactly min and max are required "
                    f"(the declared bounds), got {sorted(bounds)}",
                )
                low, high = bounds["min"], bounds["max"]
                _require(
                    isinstance(low, int) and not isinstance(low, bool) and low >= 0
                    and isinstance(high, int) and not isinstance(high, bool)
                    and low <= high,
                    f"{where}.{key}: min and max must be integers, "
                    f"0 <= min <= max (got {low!r}, {high!r})",
                )
                _require(
                    low <= count <= high,
                    f"{where}.{key}: count {count} is outside the declared "
                    f"bounds [{low}, {high}] (AP-1: the pack has outgrown "
                    f"or underfilled its own budget)",
                )
        # -- AP-8: every spine flaw consumed by a behavior rule -----------
        # the consuming surface today is the urgency entry's optional
        # `flaw` key (the owner's own rule); hook-weight modifiers,
        # on_action reactions and prohibitions join on their own triggers
        spines: dict[str, str] = {}
        for npc in entities["npcs"]:
            spine = npc.get("spine")
            if isinstance(spine, Mapping) and isinstance(spine.get("flaw"), str):
                spines[npc["id"]] = spine["flaw"]
        consumed: set[str] = set()
        unknown_flaws: list[str] = []
        for entry in (rules.get("urgencies") or {}).get("entries", ()):
            if not isinstance(entry, Mapping) or not isinstance(entry.get("flaw"), str):
                continue
            flaw = entry["flaw"]
            if flaw not in spines.values():
                unknown_flaws.append(flaw)
            consumed.add(flaw)
        # the PROHIBITION surface (iter-119, world-2 L2 slice 2 — the
        # cultures block's law entries): a prohibition's `flaw` joins
        # the consumed set (AP-8's "prohibitions join on their own
        # triggers" — the province is the trigger's first consumer);
        # the shape and the member binding are _cultures' own, this
        # walker owns the union — a flaw consumed by the culture's law
        # alone (no urgency entry) is anchored, never GHOST
        for culture in (rules.get("cultures") or {}).values():
            if not isinstance(culture, Mapping):
                continue
            for entry in culture.get("prohibitions", ()):
                if not isinstance(entry, Mapping) or not isinstance(entry.get("flaw"), str):
                    continue
                consumed.add(entry["flaw"])
        if unknown_flaws:
            raise PackError(
                f"urgencies: flaw {unknown_flaws[0]!r} names no declared "
                f"spine flaw (AP-8: the consuming rule must reference a "
                f"real flaw token — dead vocabulary otherwise)"
            )
        for npc_id, flaw in sorted(spines.items()):
            _require(
                flaw in consumed,
                f"npc {npc_id}: spine flaw {flaw!r} is unconsumed — no "
                f"urgency entry carries it (AP-8: GHOST without anchors is "
                f"dead pack data)",
            )
        # -- AP-11: no clone NPCs sharing trigger→action pairs ------------
        # two LIVE entries (probability > 0 — a 0-weight slot is a stream
        # placeholder that never fires, not a behavior) from different
        # NPCs with identical (intent, requires) pairs are clones — the
        # design-time twin of M4 novelty
        pairs: dict[tuple[Any, Any], str] = {}
        for entry in (rules.get("urgencies") or {}).get("entries", ()):
            if not isinstance(entry, Mapping):
                continue
            probability = entry.get("probability_per_beat")
            if (
                not isinstance(probability, int)
                or isinstance(probability, bool)
                or probability <= 0
            ):
                continue
            key = (
                json.dumps(entry.get("intent", {}), sort_keys=True),
                json.dumps(entry.get("requires", ()), sort_keys=True),
            )
            other = pairs.get(key)
            if other is not None and other != entry.get("npc"):
                _require(
                    False,
                    f"urgencies: clone NPCs — {other!r} and {entry.get('npc')!r} "
                    f"share the trigger→action pair {entry.get('intent', {}).get('kind')!r} "
                    f"(AP-11: the design-time twin of M4 novelty)",
                )
            pairs[key] = entry.get("npc")
        # -- AP-13: no contradictory on_action rules ----------------------
        # two ungated reactions to the same event type asserting the same
        # prop in opposite directions cancel out — a design error the
        # gate vocabulary exists to separate
        for event_type, entries in (rules.get("on_action") or {}).items():
            if event_type == "notes" or not isinstance(entries, list):
                continue
            signs: dict[str, int] = {}
            for entry in entries:
                if not isinstance(entry, Mapping) or "gate" in entry:
                    continue
                state = entry.get("state") or {}
                prop, add = state.get("prop"), state.get("add")
                if not isinstance(prop, str) or not isinstance(add, int) or isinstance(add, bool):
                    continue
                sign = 1 if add > 0 else -1 if add < 0 else 0
                if sign and prop in signs and signs[prop] != sign:
                    _require(
                        False,
                        f"on_action[{event_type!r}]: contradictory rules — "
                        f"two ungated reactions assert {prop!r} in opposite "
                        f"directions (AP-13: separate them with a gate)",
                    )
                if sign:
                    signs[prop] = sign
        # -- AP-15: predicate atomicity ----------------------------------
        # a compound's members must be leaves — nested compounds are the
        # conditional chains the crosswalk refuses; split them instead
        # (checked inside _predicate_error, the single walker every
        # predicate site already routes through — triggers, weight
        # modifiers, options; the law lives there so no site misses it)
        # -- the price-marker lint (AP-2's design-time half) --------------
        # a branch whose hooks seed non-ambient deferred consequences
        # must carry an immediate observable on that branch: a knowledge
        # record, or a declared state token (status_effects / balance /
        # ignition) — or the behavior is socially invisible
        hook_table = (rules.get("director") or {}).get("hooks") or {}
        for action in actions:
            for branch, tags in (action.get("hooks") or {}).items():
                if not tags:
                    continue
                consequential = any(
                    isinstance(hook_table.get(tag), Mapping)
                    and hook_table[tag].get("channel") != "ambient"
                    for tag in tags
                    if isinstance(tag, str)
                )
                if not consequential:
                    continue
                immediate = bool(
                    (action.get("knowledge") or {}).get(branch)
                ) or bool(
                    action.get("status_effects") or action.get("balance")
                    or action.get("ignition")
                )
                _require(
                    immediate,
                    f"action {action['intent']}: the {branch} hooks seed "
                    f"deferred consequences with no immediate price marker — "
                    f"no knowledge record and no declared state token rides "
                    f"the branch (AP-2: a socially meaningful behavior must "
                    f"be observable in-scene, or it is socially invisible)",
                )


    def _reference_strings(self) -> set[str]:
        """Every string the pack's DATA declares — dict keys and values
        across actions/rules/templates, plus the entity records' own
        cross-references — prose excluded (notes and `_` commentary,
        PACK_SPEC §2: prose rides beside data, never inside it). The
        orphan-entity check reads this as the static reference graph;
        keys matter because entity ids ride as keys too (scene_detail's
        locations, brief actors, on_action's event types)."""
        collected: set[str] = set()

        def walk(node: Any) -> None:
            if isinstance(node, Mapping):
                for key, value in node.items():
                    if key == "notes" or (isinstance(key, str) and key.startswith("_")):
                        continue
                    if isinstance(key, str):
                        collected.add(key)
                    walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)
            elif isinstance(node, str):
                collected.add(node)

        walk(self._data["actions.json"])
        walk(self._data["rules.json"])
        walk(self._data["templates.json"])
        entities = self._data["entities.json"]
        for category in (
            "locations", "npcs", "ambient_entities", "items", "groups",
        ):
            for record in entities.get(category, ()):
                for field, value in record.items():
                    if field in ("id", "name", "notes") or field.startswith("_"):
                        continue
                    if isinstance(value, str):
                        collected.add(value)
                    elif isinstance(value, (list, Mapping)):
                        walk(value)
        return collected


    def _edged_locations(self) -> set[str]:
        """Locations carrying at least one exits edge (undirected) — the
        position-read half of the orphan law: an edged location is walked
        by the movement grammar, an isolated one is reachable by nothing
        short of name references."""
        edged: set[str] = set()
        for location in self._data["entities.json"]["locations"]:
            if location.get("exits"):
                edged.add(location["id"])
                edged.update(exit_id for exit_id in location["exits"] if isinstance(exit_id, str))
        return edged


    def _dynamic_audience_declared(self) -> bool:
        """Whether any action declares a positional knowledge audience
        (same_location / adjacent_locations / destination_location) —
        the grammar can then reach any knower at any edged location."""
        for action in self._data["actions.json"]["actions"]:
            for records in (action.get("knowledge") or {}).values():
                for record in records:
                    if isinstance(record, Mapping) and record.get("who") in (
                        "same_location", "adjacent_locations", "destination_location",
                    ):
                        return True
            for records in (action.get("texture") or {}).get("knowledge", {}).values():
                for record in records:
                    if isinstance(record, Mapping) and record.get("who") in (
                        "same_location", "adjacent_locations", "destination_location",
                    ):
                        return True
        return False


    def _item_grammar_reachable(
        self, item: Mapping[str, Any], edged: set[str],
        read_flags: frozenset[str],
    ) -> bool:
        """Whether the event grammar can ever target this item: some
        action's target-noun precondition conjunction passes for it,
        OR one of the item's declared truthy flags is read by an
        actor-side precondition (flagged_accessible — the actor carries
        such an item) or an ignition config (item_flag — the fire
        source). The item-applicable target tests: kind (category),
        same_location (an edged position, or carried — co-located with
        the carrier), uncarried / carries_flagged / field_in /
        field_nonempty / has_field (read against the item's own data).
        carried_by passes for any carried item (droppable by its
        holder). Tests foreign to items pass generously — the check's
        teeth are the items NOTHING can address."""
        if any(item.get(flag) for flag in read_flags):
            return True
        carried = item.get("carrier") is not None
        for action in self._data["actions.json"]["actions"]:
            target_tests = [
                cond for cond in action.get("requires", ())
                if isinstance(cond, Mapping) and cond.get("noun") == "target"
            ]
            if not target_tests:
                continue
            if all(self._item_passes(item, cond, edged, carried) for cond in target_tests):
                return True
        return False

    @staticmethod


    def _read_item_flags(actions: list[Mapping[str, Any]]) -> frozenset[str]:
        """The item-flag names the grammar reads off CARRIED items: the
        actor-side `flagged_accessible` preconditions and the ignition
        configs' `item_flag` — the fire-source read, the ignition
        chain's own declaration."""
        read: set[str] = set()
        for action in actions:
            ignition = action.get("ignition") or {}
            if isinstance(ignition, Mapping) and isinstance(ignition.get("item_flag"), str):
                read.add(ignition["item_flag"])
            for cond in action.get("requires", ()):
                if (
                    isinstance(cond, Mapping)
                    and cond.get("test") == "flagged_accessible"
                    and isinstance(cond.get("flag"), str)
                ):
                    read.add(cond["flag"])
        return frozenset(read)

    @staticmethod


    def _item_passes(
        item: Mapping[str, Any], cond: Mapping[str, Any],
        edged: set[str], carried: bool,
    ) -> bool:
        test = cond.get("test")
        if test == "kind":
            return cond.get("is") == "item"
        if test == "same_location":
            return carried or item.get("position") in edged
        if test == "uncarried":
            return not carried
        if test == "carried_by":
            return carried
        if test == "carries_flagged":
            return bool(item.get(cond.get("flag")))
        if test == "field_in":
            return cond.get("field") in item and item.get(cond.get("field")) in (
                cond.get("values") or ()
            )
        if test == "field_nonempty":
            value = item.get(cond.get("field"))
            return isinstance(value, (list, str, tuple)) and len(value) > 0
        if test == "has_field":
            return cond.get("field") in item
        return True


    def _exercised_npcs(self) -> set[str]:
        """The NPCs the setting deliberately exercises — the non-empty
        rows of the intersection matrix (PACK_SPEC §5's third row). The
        authored surfaces: urgency entries (the NPC × action pairs
        themselves), crime_watch rotation participants, expectations
        rules, director hook targets, group memberships, pair relations
        (both sides), and carrier/carries bindings. An NPC whose row is
        empty is dead design space — reachable by the dynamic grammar
        (the orphan check passes them) but never deliberately wired."""
        rules = self._data["rules.json"]
        entities = self._data["entities.json"]
        exercised: set[str] = set()
        for entry in (rules.get("urgencies") or {}).get("entries", ()):
            if isinstance(entry, Mapping) and isinstance(entry.get("npc"), str):
                exercised.add(entry["npc"])
        rotation = (rules.get("crime_watch") or {}).get("rotation") or {}
        for participant in rotation.get("participants", ()):
            if isinstance(participant, str):
                exercised.add(participant)
        for rule in (rules.get("expectations") or {}).get("rules", ()):
            if isinstance(rule, Mapping) and isinstance(rule.get("npc"), str):
                exercised.add(rule["npc"])
        for hook in (rules.get("director") or {}).get("hooks", {}).values():
            if isinstance(hook, Mapping) and isinstance(hook.get("target_npc"), str):
                exercised.add(hook["target_npc"])
        for npc in entities["npcs"]:
            for pair in npc.get("pair_relations", ()):
                if isinstance(pair, Mapping) and isinstance(pair.get("with"), str):
                    exercised.add(npc["id"])
                    exercised.add(pair["with"])
            for carried in npc.get("carries", ()):
                if isinstance(carried, str):
                    exercised.add(npc["id"])
        for item in entities["items"]:
            if isinstance(item.get("carrier"), str):
                exercised.add(item["carrier"])
        for group in entities.get("groups", ()):
            for member in group.get("members", ()):
                if isinstance(member, str):
                    exercised.add(member)
        return exercised


    def _emission_witnesses(self) -> set[str]:
        """Every event type the pack's grammar declares as an emission,
        plus the two core-constant witnesses and the authored-intent
        list. The declared-but-unused check (§5's fourth row) reads this:
        a template entry matching NO witness is dead vocabulary. The
        emission sites are exactly the fields the per-block lints
        validate against the template closure (the forward direction,
        EVENT_SCHEMA §11) — this is the reverse walk over the same
        closed set; a new emission site that misses here fails the
        committed packs loudly (the drift-contract family: the closure
        is pinned by the packs that pass it)."""
        rules = self._data["rules.json"]
        used: set[str] = set()
        # actions' branch events (the texture twin rides the action's
        # own event types — no separate emission site)
        for action in self._data["actions.json"]["actions"]:
            for branch in ("success", "failure", "failure_total"):
                event_type = (action.get("events") or {}).get(branch)
                if isinstance(event_type, str):
                    used.add(event_type)
        # on_action: the reacted-to keys and each reaction's event
        for event_type, entries in (rules.get("on_action") or {}).items():
            if event_type == "notes" or not isinstance(entries, list):
                continue
            used.add(event_type)
            for entry in entries:
                if isinstance(entry, Mapping) and isinstance(entry.get("event"), str):
                    used.add(entry["event"])
        # transition layers (started/spread/smoke/alarm/burnout)
        for layer in (rules.get("transitions") or {}).values():
            if isinstance(layer, Mapping):
                for event_type in (layer.get("events") or {}).values():
                    if isinstance(event_type, str):
                        used.add(event_type)
        # crime_watch: the reaction, the rotation pair, the arrest pair
        crime = rules.get("crime_watch") or {}
        rotation = crime.get("rotation") or {}
        arrest = crime.get("arrest") or {}
        for event_type in (
            crime.get("reaction_event"),
            rotation.get("watch_event"),
            rotation.get("transfer_event"),
            arrest.get("event"),
            arrest.get("resolution_event"),
        ):
            if isinstance(event_type, str):
                used.add(event_type)
        # expectations, telling, secrets, reflection, macro, weather,
        # worldgen chronicle — the single-event blocks
        telling = (rules.get("knowledge") or {}).get("telling") or {}
        macro = (rules.get("time") or {}).get("macro") or {}
        chronicle = (rules.get("worldgen") or {}).get("chronicle") or {}
        for event_type in (
            (rules.get("expectations") or {}).get("event"),
            telling.get("on_event"),
            telling.get("event"),
            (rules.get("secrets") or {}).get("event"),
            (rules.get("secrets") or {}).get("spend_event"),
            (rules.get("reflection") or {}).get("event"),
            macro.get("event_type"),
            (rules.get("weather") or {}).get("event_type"),
            chronicle.get("event_type"),
        ):
            if isinstance(event_type, str):
                used.add(event_type)
        # the calendar entries (the sub-year cadences, the calendar
        # slice) — the crossing events are emission sites exactly as
        # the macro turn's own: a plain entry's own type, every cycle
        # pair's phase type
        for entry in ((rules.get("time") or {}).get("calendar") or {}).values():
            if not isinstance(entry, Mapping):
                continue
            if isinstance(entry.get("event_type"), str):
                used.add(entry["event_type"])
            for pair in entry.get("cycle") or ():
                if isinstance(pair, Mapping) and isinstance(
                    pair.get("event_type"), str
                ):
                    used.add(pair["event_type"])
        # weather erosion rows
        for state in ((rules.get("weather") or {}).get("states") or {}).values():
            if not isinstance(state, Mapping):
                continue
            for erosion in state.get("erosion", ()):
                if isinstance(erosion, Mapping) and isinstance(
                    erosion.get("event_type"), str
                ):
                    used.add(erosion["event_type"])
        # group tiers (depth-7)
        for group in self._data["entities.json"].get("groups", ()):
            for tier_key in ("macro_event", "condense_event"):
                if isinstance(group.get(tier_key), str):
                    used.add(group[tier_key])
        # the core-constant witnesses: the front door's rejection line is
        # mandatory everywhere (_templates); the decay line is owed iff
        # any states axis declares a drift rate (the decay pass emits it)
        used.add(REJECTION_EVENT)
        states = rules.get("states") or {}
        if any(
            isinstance(axis, Mapping)
            and ("decay_per_360_ticks" in axis or "gain_per_360_ticks_awake" in axis)
            for axis in states.values()
        ):
            used.add(DECAY_EVENT)
        # the authored-intent witness: the story-critical list is the
        # pack's own declaration that an event type carries the tale —
        # a template listed there is deliberately kept vocabulary (the
        # 68a twin's dormant lines), never dead-by-accident
        for event_type in (rules.get("importance") or {}).get(
            "story_critical_events", ()
        ):
            if isinstance(event_type, str):
                used.add(event_type)
        return used
