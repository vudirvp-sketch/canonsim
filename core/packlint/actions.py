"""The action/template lint: the intent contract, the knowledge and
texture blocks, the balance/status_effects shapes, the template closure
(the D-175 split's actions family)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.intent import (
    ECHO_TEST,
    EDGE_TICKS,
    LEVERAGE_TEST,
    PRECONDITION_TESTS,
    REJECTION_EVENT,
    TRAIT_TEST,
)
from core.packlint.helpers import _NOUNS, _SLOT, _SNAKE_CASE, PackError, _require
from core.packlint.shared import knowledge_entry, lint_echo_cond, lint_trait_cond
from core.resolvers import REGISTRY


class ActionsLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

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
                knowledge_entry(self._data, intent, record, tuple(block["requires"]))
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
            resolver = action.get("resolver")
            _require(
                isinstance(resolver, str) and resolver in REGISTRY,
                f"action {intent}: resolver {resolver!r} is not in the registry "
                f"(known: {sorted(REGISTRY)})",
            )
            ticks = action["ticks"]
            if isinstance(ticks, Mapping):
                _require(
                    isinstance(ticks.get("min"), int) and isinstance(ticks.get("max"), int)
                    and ticks["min"] <= ticks["max"],
                    f"action {intent}: ticks range malformed: {ticks}",
                )
            else:
                # st-6a (D-116 (5)): "edge" is the fourth legal value —
                # the duration is the TRAVEL EDGE PRICE (resolve time,
                # the loop's accept-door branch on EDGE_TICKS). Only
                # the movement resolver may carry it (the travel action
                # IS the movement twin with an edge price; an
                # edge-priced check action is a future row's own
                # mechanic, never this one's — the status_effects
                # family law: the block/mode is legal only on its
                # consuming resolver).
                _require(
                    isinstance(ticks, int) or ticks in ("N", EDGE_TICKS),
                    f"action {intent}: ticks must be int, {{min,max}}, 'N' "
                    f"or 'edge', got {ticks!r}",
                )
                if ticks == EDGE_TICKS:
                    _require(
                        resolver == "movement",
                        f"action {intent}: ticks 'edge' is the movement "
                        f"family's price mode (the travel action, the "
                        f"movement twin) — resolver {resolver!r} would "
                        f"need its own row's mechanic",
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
                    lint_echo_cond(self._data, cond, f"action {intent}")
                # beliefwire (iter-67): the trait gate's token must name
                # a declared belief — a token the fold never mints is a
                # dead gate, refused at load (the echo axis family)
                if cond.get("test") == TRAIT_TEST:
                    lint_trait_cond(self._data, cond, f"action {intent}")
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
                    knowledge_entry(self._data, 
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
