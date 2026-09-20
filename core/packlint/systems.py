"""The mechanical rule-block lints: time, systems, transitions, crime
watch, expectations, states, importance, drift, reflection (the D-175
split's systems family)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.clock import Clock
from core.knowledge import DRIFT_SPEC_KEYS
from core.packlint.helpers import PackError, _ids, _is_int, _require
from core.packlint.shared import knowledge_entry, literal_knows_tokens
from core.reflection import REFLECTION_BLOCK_KEYS, REFLECTION_INSIGHT_KEYS
from core.scheduler import ScheduleAmbiguityError, build, decls_from_rules


class SystemsLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _time_rules(self) -> None:
        time_rules = self._data["rules.json"]["time"]
        try:
            Clock.from_rules(time_rules)
        except ValueError as exc:
            raise PackError(f"time rules invalid: {exc}") from exc
        # maclock-1 (L4): the macro sub-block — the second granularity's
        # own declaration. OPTIONAL (the unarmed law: an absent block is
        # zero crossings, zero events, the v0.1 bytes untouched — the
        # 68a pattern; the committed pack's arming rides with the
        # primitive's first consumer). Closed vocabulary, positive-int
        # cadence, the event type in the template closure (EVENT_SCHEMA
        # §11 — the macro turn is a pack-declared event type, never an
        # engine word, INV-3).
        macro = time_rules.get("macro")
        if macro is not None:
            where = "time.macro"
            _require(isinstance(macro, Mapping), f"{where} must be an object")
            unknown = sorted(set(macro) - {"cadence_ticks", "event_type"})
            if unknown:
                raise PackError(
                    f"{where}: unknown keys {unknown} (the closed "
                    "vocabulary: cadence_ticks | event_type)"
                )
            _require(
                _is_int(macro.get("cadence_ticks"))
                and macro["cadence_ticks"] >= 1,
                f"{where}.cadence_ticks must be an integer >= 1 (zero or "
                "negative is an infinite crossing loop, never a clock)",
            )
            templates = self._data["templates.json"]["events"]
            event_type = macro.get("event_type")
            _require(
                isinstance(event_type, str) and event_type in templates,
                f"{where}.event_type {event_type!r} is not in the template "
                "vocabulary (EVENT_SCHEMA §11 — closed per pack)",
            )

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
            assert isinstance(follow_ups, list)  # the require above
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
                knowledge_entry(self._data, f"{layer}.{key}", record)

    # -- knowledge rules (telling + acceptance, iter-3) ------------------------


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
        flat_shape = targeted_shape = False
        for token, spec in crime.get("suspicion_from_knowledge", {}).items():
            if isinstance(spec, str):  # v0.1: token -> source (the player implicit)
                flat_shape = True
                _require(
                    spec in sources,
                    f"crime_watch.suspicion_from_knowledge[{token!r}]: unknown "
                    f"suspicion source {spec!r}",
                )
                continue
            # per-target (suspectaxis, iter-69): token -> {source, figure}
            targeted_shape = True
            _require(
                isinstance(spec, dict),
                f"crime_watch.suspicion_from_knowledge[{token!r}]: a string "
                f"(flat) or an object (per-target) — got {type(spec).__name__}",
            )
            _require(
                spec.get("source") in sources,
                f"crime_watch.suspicion_from_knowledge[{token!r}].source: "
                f"unknown suspicion source {spec.get('source')!r}",
            )
            figure = spec.get("figure")
            _require(
                figure in npc_ids,
                f"crime_watch.suspicion_from_knowledge[{token!r}].figure "
                f"{figure!r} is not an npc",
            )
        _require(
            not (flat_shape and targeted_shape),
            "crime_watch.suspicion_from_knowledge mixes the flat v0.1 shape "
            "and the per-target shape — one mode per pack",
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


    def _drift(self) -> None:
        """The rumor-drift contract (rumordrift, A2''/D-095; the v0.2
        refinement family's third segment, iter-68a — mechanics only,
        the pack arming is 68b). The block is OPTIONAL and lives INSIDE
        `rules.json::knowledge` (the rumor path's config home, beside
        `telling` and `rumor_acceptance`): `knowledge.drift` maps family
        id → spec. A pack without it drifts nothing and runs the v0.1
        bytes, byte-identically (the pack's own declaration is the
        arming, INV-3; `core/knowledge.py::drift_families` the reader).
        Family ids name the drift streams (`drift:<family>`, D-095:
        isolation is law) — map keys, injective by construction."""
        rules = self._data["rules.json"]
        config = rules.get("knowledge", {}).get("drift")
        if config is None:
            return
        _require(
            isinstance(config, Mapping) and config,
            "knowledge.drift must be a non-empty object keyed by family "
            "id (an empty block is dead data — omit it for v0.1 bytes)",
        )
        mintable = literal_knows_tokens(self._data)
        chain = rules["knowledge"]["fidelity_chain"]
        seen_tokens: dict[str, str] = {}  # token -> owning family
        for family, spec in config.items():
            where = f"knowledge.drift[{family!r}]"
            _require(
                isinstance(family, str) and family,
                f"{where}: family ids must be non-empty strings (they "
                "name the drift stream `drift:<family>`)",
            )
            _require(isinstance(spec, Mapping), f"{where}: must be an object")
            unknown = sorted(set(spec) - set(DRIFT_SPEC_KEYS))
            if unknown:
                raise PackError(
                    f"{where}: unknown keys {unknown} (the closed "
                    f"vocabulary: {' | '.join(DRIFT_SPEC_KEYS)})"
                )
            tokens = spec.get("tokens")
            _require(
                isinstance(tokens, list)
                and len(tokens) >= 2
                and all(isinstance(token, str) for token in tokens),
                f"{where}: tokens must be a list of >= 2 knowledge tokens "
                "(a one-token orbit can never drift — dead vocabulary)",
            )
            _require(
                len(set(tokens)) == len(tokens),
                f"{where}: tokens contains duplicates (a duplicate orbit "
                "member is dead data)",
            )
            for token in tokens:
                # the secrets/echo/traits lint's law: a token nobody can
                # ever learn is dead vocabulary — a drift orbit must ride
                # declared knowledge templates (the telling path only
                # transfers what the world minted)
                _require(
                    token in mintable,
                    f"{where}: orbit token {token!r} is not mintable (no "
                    "declared knowledge template mints it — the literal "
                    "`knows` vocabulary)",
                )
                owner = seen_tokens.get(token)
                _require(
                    owner is None,
                    f"{where}: orbit token {token!r} already belongs to "
                    f"family {owner!r} (the one-sided membership law — a "
                    "token drifts in exactly one family, else the stream "
                    "isolation law breaks: two families' rolls would "
                    "couple over one token)",
                )
                seen_tokens[token] = family
            # the ladder: closed against the pack's own fidelity chain —
            # the echo.fidelity_weight law (a chain member without a
            # chance would KeyError at the roll, refused at load instead)
            ladder = spec.get("ladder")
            _require(
                isinstance(ladder, Mapping)
                and sorted(ladder) == sorted(chain)
                and all(
                    _is_int(chance) and 0 <= chance <= 100
                    for chance in ladder.values()
                ),
                f"{where}: ladder must map every fidelity chain member "
                f"({list(chain)}) to a d100 chance in 0..100 — the drift "
                "rolls at the RECEIVED fidelity (a missing step would "
                "KeyError at the roll)",
            )
            if "notes" in spec:
                _require(
                    isinstance(spec["notes"], str),
                    f"{where}: notes must be a string (prose)",
                )


    def _reflection(self) -> None:
        """The reflection & compaction contract (`core/reflection.py`
        owns the vocabulary constants; `phases.md` §4 the reflection
        paragraph — the LEGEND_SPEC compression half, landed iter-57).
        The block is OPTIONAL — a pack without it mints no reflection
        events and runs the v0.1 behavior, byte-identically (the
        pack's own declaration is the gate, INV-3; the committed v0.1
        pack carries no block — the TASKS arming row owns the
        corpus price)."""
        rules = self._data["rules.json"]
        config = rules.get("reflection")
        if config is None:
            return
        templates = self._data["templates.json"]["events"]
        if not isinstance(config, Mapping):
            raise PackError("reflection must be an object")
        unknown = sorted(set(config) - set(REFLECTION_BLOCK_KEYS))
        if unknown:
            raise PackError(
                f"reflection: unknown keys {unknown} (the closed "
                f"vocabulary: {' | '.join(REFLECTION_BLOCK_KEYS)})"
            )
        event_type = config.get("event")
        _require(
            isinstance(event_type, str) and event_type in templates,
            f"reflection.event {event_type!r} is not in the template "
            "vocabulary (EVENT_SCHEMA §11 — the reflection renders in the "
            "chronicle)",
        )
        # the threshold: the recurrence count that compacts — a first
        # occurrence is an event, not a pattern (the compaction floor,
        # the traits threshold's twin)
        threshold = config.get("threshold")
        _require(
            _is_int(threshold) and threshold >= 2,
            "reflection.threshold must be an integer >= 2 (a single "
            "record is an occurrence, not a recurrence — the LEGEND_SPEC "
            "floor)",
        )
        if "notes" in config:
            _require(
                isinstance(config["notes"], str),
                "reflection.notes must be a string (prose — never a table "
                "key)",
            )
        insights = config.get("reflections")
        _require(
            isinstance(insights, Mapping) and insights,
            "reflection.reflections must be a non-empty object keyed by "
            "insight token",
        )
        assert isinstance(insights, Mapping)  # the require above
        mintable = literal_knows_tokens(self._data)
        seen_members: dict[str, str] = {}  # token -> owning insight
        for insight, spec in insights.items():
            where = f"reflection.reflections[{insight!r}]"
            # the vocabulary-hygiene check (the traits law): an insight
            # token colliding with a mintable knowledge token puts one
            # string in two vocabularies — the template mint would hold
            # it and the never-re-reflect gate would block the fold's
            # own mint forever
            _require(
                insight not in mintable,
                f"{where}: the insight token is also a mintable knowledge "
                "token (one string, two vocabularies — rename the insight)",
            )
            _require(isinstance(spec, Mapping), f"{where}: must be an object")
            unknown_insight = sorted(set(spec) - set(REFLECTION_INSIGHT_KEYS))
            if unknown_insight:
                raise PackError(
                    f"{where}: unknown keys {unknown_insight} (the closed "
                    f"vocabulary: {' | '.join(REFLECTION_INSIGHT_KEYS)})"
                )
            family = spec.get("family")
            _require(
                isinstance(family, list) and family,
                f"{where}: family must be a non-empty list of knowledge "
                "tokens",
            )
            _require(
                all(isinstance(token, str) for token in family),
                f"{where}: family entries must be strings",
            )
            _require(
                len(set(family)) == len(family),
                f"{where}: family contains duplicate tokens (a duplicate "
                "double-counts one recurrence — dead data)",
            )
            for token in family:
                # the secrets/echo/traits lint's law: a token nobody can
                # ever learn is dead vocabulary — the recurrence must
                # ride a declared knowledge template
                _require(
                    token in mintable,
                    f"{where}: family token {token!r} is not mintable "
                    "(no declared knowledge template mints it — the "
                    "literal `knows` vocabulary)",
                )
                owner = seen_members.get(token)
                _require(
                    owner is None,
                    f"{where}: family token {token!r} already belongs to "
                    f"insight {owner!r} (the one-sided membership law — a "
                    "token feeds exactly one reflection)",
                )
                seen_members[token] = insight
            if "notes" in spec:
                _require(
                    isinstance(spec["notes"], str),
                    f"{where}: notes must be a string (prose)",
                )
