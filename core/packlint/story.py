"""The story-layer lints: the director hooks and options, on_action
reactions, secrets, echo, traits (the D-175 split's story family)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from core.director import ARC_KEYS, CHANNEL_INPUTS
from core.echo import ECHO_BLOCK_KEYS, ECHO_TOKEN_KEYS
from core.intent import LEVERAGE_TEST
from core.leverage import SECRETS_BLOCK_KEYS, TOKEN_KEYS
from core.onaction import ACTOR_TARGET_KEYS, ENTRY_KEYS, GATE_KEYS, SCOPES, STATE_KEYS
from core.packlint.helpers import (
    PackError,
    _ids,
    _is_int,
    _lint_weight_spec,
    _predicate_error,
    _require,
)
from core.packlint.shared import literal_knows_tokens
from core.predicates import COMPARATORS, LEAF_KINDS
from core.traits import TRAIT_BELIEF_KEYS, TRAIT_BLOCK_KEYS

OPTION_KEYS: Final = ("trigger", "weight", "intent", "notes")
"""The closed option-block vocabulary (drama-2): the availability gate,
the ai_chance-style weight, the payload override, and prose notes —
an unknown key is a shape error, never a silent ignore (a typo'd
`triger` would read as an always-available option)."""


class StoryLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

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
                if condition.get("value") is None:
                    return (
                        f"{gwhere}: the condition's value must not be null — "
                        "absence is the world's answer (False, "
                        "DIRECTOR_SPEC §3), never a pack value"
                    )
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
        assert isinstance(tokens, Mapping)  # the require above
        mintable = literal_knows_tokens(self._data)
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
        assert isinstance(tokens, Mapping)  # the require above
        mintable = literal_knows_tokens(self._data)
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


    def _traits(self) -> None:
        """The trait crystallization contract (`core/traits.py` owns the
        vocabulary constants; `phases.md` §4 P3f the architecture row —
        the LEGEND_SPEC sketch's trait half, landed iter-55; the
        counter-family is beliefwire, iter-67). The block is OPTIONAL —
        a pack without it folds no beliefs and runs the v0.1 behavior,
        byte-identically (the pack's own declaration is the gate, INV-3).
        Declaring the table costs nothing at runtime until a consumer
        reads it (the iter-45 laziness law — the fold's readers are the
        brief's derived-trait read, leg-2, and the loop's traits channel
        behind a `trait_held` require, beliefwire; neither computes
        unasked)."""
        rules = self._data["rules.json"]
        config = rules.get("traits")
        if config is None:
            return
        if not isinstance(config, Mapping):
            raise PackError("traits must be an object")
        unknown = sorted(set(config) - set(TRAIT_BLOCK_KEYS))
        if unknown:
            raise PackError(
                f"traits: unknown keys {unknown} (the closed vocabulary: "
                f"{' | '.join(TRAIT_BLOCK_KEYS)})"
            )
        # the threshold: the family size that crystallizes a belief —
        # one record is a fact, not a belief (the crystallization floor)
        threshold = config.get("threshold")
        _require(
            _is_int(threshold) and threshold >= 2,
            "traits.threshold must be an integer >= 2 (a single record "
            "is a fact, not a crystallized belief — the LEGEND_SPEC floor)",
        )
        assert _is_int(threshold)  # the require above
        if "notes" in config:
            _require(
                isinstance(config["notes"], str),
                "traits.notes must be a string (prose — never a table key)",
            )
        beliefs = config.get("beliefs")
        _require(
            isinstance(beliefs, Mapping) and beliefs,
            "traits.beliefs must be a non-empty object keyed by belief "
            "token",
        )
        assert isinstance(beliefs, Mapping)  # the require above
        mintable = literal_knows_tokens(self._data)
        seen_members: dict[str, str] = {}  # token -> owning belief
        for belief, spec in beliefs.items():
            where = f"traits.beliefs[{belief!r}]"
            # the vocabulary-hygiene check: a belief token colliding
            # with a mintable knowledge token would put one string in
            # two vocabularies the brief reads (holds vs trait lookups)
            _require(
                belief not in mintable,
                f"{where}: the belief token is also a mintable knowledge "
                "token (one string, two vocabularies — rename the belief)",
            )
            _require(isinstance(spec, Mapping), f"{where}: must be an object")
            unknown_belief = sorted(set(spec) - set(TRAIT_BELIEF_KEYS))
            if unknown_belief:
                raise PackError(
                    f"{where}: unknown keys {unknown_belief} (the closed "
                    f"vocabulary: {' | '.join(TRAIT_BELIEF_KEYS)})"
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
                "double-counts one piece of evidence — dead data)",
            )
            for token in family:
                # the secrets/echo lint's law: a token nobody can ever
                # learn is dead vocabulary — the belief must ride a
                # declared knowledge template
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
                    f"belief {owner!r} (the one-sided membership law — a "
                    "token feeds exactly one belief)",
                )
                seen_members[token] = belief
            _require(
                len(family) >= threshold,
                f"{where}: family of {len(family)} token(s) can never "
                f"reach threshold {threshold} — dead vocabulary, refused "
                "at load (grow the family or lower the threshold)",
            )
            # beliefwire (iter-67): the counter-family — exoneration
            # tokens at the SAME breadth bar block the crystallization.
            # Every family law applies verbatim (mintable, no duplicates,
            # can reach the bar, one-sided membership) plus the family/
            # counters disjointness inside one belief (a token that is
            # both evidence and counter-evidence feeds the belief both
            # ways — author error, refused loudly).
            counters = spec.get("counters")
            if counters is not None:
                _require(
                    isinstance(counters, list) and counters,
                    f"{where}: counters must be a non-empty list of "
                    "knowledge tokens (an empty list is dead data)",
                )
                _require(
                    all(isinstance(token, str) for token in counters),
                    f"{where}: counters entries must be strings",
                )
                _require(
                    len(set(counters)) == len(counters),
                    f"{where}: counters contains duplicate tokens (a "
                    "duplicate double-counts one piece of evidence — "
                    "dead data)",
                )
                overlap = sorted(set(counters) & set(family))
                _require(
                    not overlap,
                    f"{where}: counters overlaps the family at {overlap} "
                    "(a token that is both evidence and counter-evidence "
                    "feeds the belief both ways — split the vocabularies)",
                )
                for token in counters:
                    _require(
                        token in mintable,
                        f"{where}: counters token {token!r} is not "
                        "mintable (no declared knowledge template mints "
                        "it — the literal `knows` vocabulary)",
                    )
                    owner = seen_members.get(token)
                    _require(
                        owner is None,
                        f"{where}: counters token {token!r} already "
                        f"belongs to belief {owner!r} (the one-sided "
                        "membership law — a token feeds exactly one "
                        "belief, either side)",
                    )
                    seen_members[token] = belief
                _require(
                    len(counters) >= threshold,
                    f"{where}: counters of {len(counters)} token(s) can "
                    f"never reach threshold {threshold} — the block can "
                    "never fire, dead vocabulary, refused at load (grow "
                    "the counters or lower the threshold)",
                )
            if "notes" in spec:
                _require(
                    isinstance(spec["notes"], str),
                    f"{where}: notes must be a string (prose)",
                )
