"""The action/template lint: the intent contract, the knowledge and
texture blocks, the balance/status_effects shapes, the template closure
(the D-175 split's actions family)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.economy import VERB_EVENT_TYPES
from core.intent import (
    ACCOUNT_TEST,
    ECHO_TEST,
    EDGE_TICKS,
    LEVERAGE_TEST,
    PRECONDITION_TESTS,
    REJECTION_EVENT,
    TRAIT_TEST,
    needs_target,
)
from core.packlint.helpers import _NOUNS, _SLOT, _SNAKE_CASE, PackError, _is_int, _require
from core.packlint.shared import (
    knowledge_entry,
    lint_account_cond,
    lint_direct_keys,
    lint_echo_cond,
    lint_trait_cond,
)
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
            lint_direct_keys(cond, where)
            if cond.get("test") == ECHO_TEST:
                lint_echo_cond(self._data, cond, where)
            if cond.get("test") == TRAIT_TEST:
                lint_trait_cond(self._data, cond, where)
            if cond.get("test") == ACCOUNT_TEST:
                lint_account_cond(self._data, cond, where)
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
        # iter-200 (the rename-safety closure, the iter-198 T3 measured
        # failure — TECH_NOTES §17): the declared hook tags the branches
        # below check membership against. The read is guarded (the KI#77
        # order law: _director validates the block LATER, so a malformed
        # director config must read here as no declarations, never a
        # crash — the worldgen/weather precedents read the table only
        # after _director has run).
        director_cfg = self._data["rules.json"].get("director")
        hook_table = director_cfg.get("hooks", {}) if isinstance(director_cfg, Mapping) else {}
        declared_hooks = set(hook_table) if isinstance(hook_table, Mapping) else set()
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
                # KI#88's second arm (closed iter-169): a target-sourced
                # defender builds its total from the intent's target — the
                # door demands one only when a precondition references
                # the noun (needs_target, the door's own predicate). A
                # targetless intent would reach the check and roll
                # against the base skill (the silent nonsense roll);
                # refuse at load what the assert would refuse mid-run.
                # The texture-block row is the stricter twin: the texture
                # path replaces the canon requires and carries no target
                # at all, so it refuses the combination outright.
                if checks["kinds"][check["kind"]].get(
                    "defender_source"
                ) == "target":
                    _require(
                        needs_target(action),
                        f"action {intent}: check kind {check['kind']!r} "
                        "defends from the target — the action must pin "
                        "the intent's target with a target-noun "
                        "precondition (the door demands a target only "
                        "then; without the pin a targetless intent would "
                        "roll against the base skill, KI#88)",
                    )
            for cond in action.get("requires", ()):
                _require(
                    cond.get("test") in PRECONDITION_TESTS,
                    f"action {intent}: unknown precondition test {cond.get('test')!r}",
                )
                # KI#89 (closed iter-169): the directly-indexed key rows —
                # the five record-reading tests subscript their named
                # parameters, so a missing key is refused HERE, at load
                # (the iter-45 leverage `who` family's shared twin).
                lint_direct_keys(cond, f"action {intent}")
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
                # res-1 (the economy substrate): the account gate's kind
                # must name a declared economy account — a kind outside
                # the vocabulary is a dead gate (the echo axis family)
                if cond.get("test") == ACCOUNT_TEST:
                    lint_account_cond(self._data, cond, f"action {intent}")
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
                    # iter-200: the seeding side of the rename-safety law —
                    # a tag naming no declared hook is a silent no-op at
                    # runtime (director.seed's None branch skips it), so a
                    # rename that misses a seeding site kills the deferred
                    # consequence invisibly. The worldgen and weather lints
                    # already refuse their own hook references; the
                    # actions' branches were the last unchecked surface.
                    _require(
                        tag in declared_hooks,
                        f"action {intent}: hooks[{branch!r}] tag {tag!r} is not "
                        "a declared director.hooks entry (the runtime ignores "
                        "unknown tags — the seeded consequence never fires; "
                        "declare the hook in director.hooks first)",
                    )
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
            self._account_block(intent, action)


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


    def _account_block(self, intent: str, action: Mapping[str, Any]) -> None:
        """The optional account block (res-1, the economy substrate):
        the action-declared verb/kind/amount the `account` resolver
        executes — the player-scaled arm of the three verbs through the
        canon door. The status_effects/balance precedent owns the shape
        law: the block lives beside its action, only its resolver
        consumes it. TWO cross-checks beyond the shape: the pack's
        `events.success` must RESTATE the verb's engine constant (the
        emitted type is the engine's — the build's naming pass; the
        restatement is the load-time cross-check, and the template
        closure above then covers the verb's line, the arming corpus
        price), and a transfer/consume must declare the
        `account_at_least` solvency gate on the actor for the same
        kind with value >= amount (the underflow floor's soft arm, D3:
        without the gate an insolvent attempt reaches the resolver and
        crashes loud at the commit gate mid-run — the KI#15 family,
        refuse at load what would crash at completion)."""
        block = action.get("account")
        if block is None:
            return
        where = f"action {intent!r} account"
        _require(
            action.get("resolver") == "account",
            f"{where}: only the 'account' resolver consumes the block "
            f"(this action resolves via {action.get('resolver')!r})",
        )
        _require(
            isinstance(block, Mapping),
            f"{where}: must be an object (verb | kind | amount)",
        )
        verb = block.get("verb")
        _require(
            verb in VERB_EVENT_TYPES,
            f"{where}.verb {verb!r} is not in the closed vocabulary "
            f"{sorted(VERB_EVENT_TYPES)}",
        )
        unknown = sorted(set(block) - {"verb", "kind", "amount"})
        if unknown:
            raise PackError(
                f"{where}: unknown keys {unknown} (the closed vocabulary: "
                "verb | kind | amount — a source mints to the actor and a "
                "transfer lands on the intent target by construction)"
            )
        economy = self._data["rules.json"].get("economy")
        vocabulary = (
            economy.get("accounts") if isinstance(economy, Mapping) else None
        )
        _require(
            isinstance(vocabulary, list) and block.get("kind") in vocabulary,
            f"{where}.kind {block.get('kind')!r} is not in the "
            "economy.accounts vocabulary (the substrate moves only "
            "declared stocks — the pairing law)",
        )
        _require(
            _is_int(block.get("amount")) and block["amount"] >= 1,
            f"{where}.amount must be an integer >= 1 (a zero amount is "
            "dead data — the vacuity law)",
        )
        _require(
            action.get("events", {}).get("success") == VERB_EVENT_TYPES[verb],
            f"{where}: events.success must restate the {verb} verb's "
            f"engine constant {VERB_EVENT_TYPES[verb]!r} (the emitted "
            "type is the engine's, the naming pass; the restatement is "
            "the cross-check and carries the template closure)",
        )
        if verb in ("transfer", "consume"):
            gate = next(
                (
                    cond for cond in action.get("requires", ())
                    if isinstance(cond, Mapping)
                    and cond.get("test") == ACCOUNT_TEST
                    and cond.get("noun") == "actor"
                    and cond.get("kind") == block["kind"]
                ),
                None,
            )
            _require(
                gate is not None,
                f"{where}: the {verb} declares no account_at_least "
                f"solvency gate on the actor for kind {block['kind']!r} — "
                "an ungated spend would underflow at the commit gate "
                "(author the precondition: the door rejects insolvent "
                "attempts softly, attempts are facts)",
            )
            assert gate is not None  # the require above
            _require(
                _is_int(gate.get("value")) and gate["value"] >= block["amount"],
                f"{where}: the solvency gate's value must cover the "
                f"amount (>= {block['amount']}) — a lower gate passes "
                "insolvent attempts to the commit gate's loud refusal",
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
