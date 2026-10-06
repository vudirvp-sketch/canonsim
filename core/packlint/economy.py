"""The economy block lint (res-1, `docs/CONTRACTS.md` §2): the
account-kind vocabulary, the flow declarations, the price formulas.
Two phases under the `_Lint` orchestrator's pinned order (KI#77):

- `_economy` — EARLY, before `_entities`: the block's own shape
  (rules.json + templates.json alone — no entity or action reads, so a
  crafted variant with a malformed economy block hits THIS clean
  PackError, never a KeyError downstream). The entity `accounts`
  cross-check and the account-action lint read the vocabulary this
  phase validates.
- `_economy_cross` — LATE, after `_weather`: the flow-endpoint
  cross-checks (from/to must name declared entities that declare the
  account) — reading entity records only after `_entities` validated
  them (the worldgen lint's own late-phase law).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from core.economy import (
    ACCOUNT_GLOSS_BLOCK,
    FLOW_GLOSS_BLOCK,
    VERB_EVENT_TYPES,
)
from core.packlint.helpers import _SNAKE_CASE, PackError, _is_int, _require

#: The economy block's closed key vocabulary (the engine-side mirror
#: `core/economy.py` reads; this lint is the authority).
ECONOMY_KEYS: Final = ("accounts", "flows", "recipes", "prices", "notes")

#: The flow declaration's closed key set, per verb: `id`, `verb`,
#: `kind`, `amount`, the optional `every` cadence, and the endpoint
#: keys — `to` for a source, `from` + `to` for a transfer, `from` for
#: a consume.
_VERB_KEYS: Final[Mapping[str, tuple[str, ...]]] = {
    "source": ("id", "verb", "kind", "to", "amount"),
    "transfer": ("id", "verb", "kind", "from", "to", "amount"),
    "consume": ("id", "verb", "kind", "from", "amount"),
}


class EconomyLint:
    """The domain lint (loaded pack data in, PackError out)."""

    def __init__(self, data: dict[str, Mapping[str, Any]]) -> None:
        self._data = data

    def _economy(self) -> None:
        """The block's own shape, EARLY (see the module docstring for
        the order law). The unarmed law: an ABSENT block is zero
        accounts, zero flows, zero prices — no cross-lint fires, the
        committed packs' bytes untouched (the 68a pattern)."""
        rules = self._data["rules.json"]
        economy = rules.get("economy")
        if economy is None:
            # rs-2: a gloss table without the economy block is ALL dead
            # data (every key names an undeclared kind) — refused here,
            # the early phase's clean PackError (never a silent skip)
            self._gloss_table(vocabulary=frozenset())
            # rs-4: the flow-gloss table's own dead-data law — every key
            # names a flow that cannot exist without the block
            self._flow_gloss_table(flow_ids=frozenset())
            return
        where = "economy"
        _require(
            isinstance(economy, Mapping),
            f"{where} must be an object (the closed vocabulary: "
            "accounts | flows | prices | notes)",
        )
        unknown = sorted(set(economy) - set(ECONOMY_KEYS))
        if unknown:
            raise PackError(
                f"{where}: unknown keys {unknown} (the closed vocabulary: "
                "accounts | flows | prices | notes)"
            )
        self._accounts_vocabulary(economy)
        self._gloss_table(vocabulary=frozenset(economy["accounts"]))
        self._flows(economy)
        self._recipes(economy)
        self._flow_gloss_table(
            flow_ids=frozenset(
                flow["id"] for flow in economy.get("flows", ())
                if isinstance(flow, Mapping)
            )
        )
        self._prices(economy)

    def _gloss_table(self, *, vocabulary: frozenset[str]) -> None:
        """The account-kind gloss table (rs-2, the reader-surface
        boundary's pack half): `templates.json::account_kinds`, kind ->
        reader prose — the kind's MEANING, rendered by the renderer at
        the verb lines' `{kind}` slot and the state line's apposition.
        OPTIONAL (the dry fallback law — an unglossed kind renders its
        bare word, `gloss_account_kind`'s own family); when present:
        an object whose keys sit in the economy.accounts vocabulary (a
        gloss for an undeclared kind is dead data, the vacuity law)
        and whose values are non-empty strings (both surfaces render
        the prose VERBATIM — a noun phrase headed by the kind word,
        authored to sit in "16 {kind}" slots)."""
        table = self._data["templates.json"].get(ACCOUNT_GLOSS_BLOCK)
        if table is None:
            return  # the dry fallback law (the unarmed twin)
        where = f"templates.json::{ACCOUNT_GLOSS_BLOCK}"
        _require(
            isinstance(table, Mapping),
            f"{where} must be an object (account kind -> reader prose)",
        )
        for kind, gloss in table.items():
            _require(
                kind in vocabulary,
                f"{where}: the kind {kind!r} is not in the economy.accounts "
                "vocabulary — a gloss for an undeclared kind is dead data "
                "(the vacuity law)",
            )
            _require(
                isinstance(gloss, str) and bool(gloss.strip()),
                f"{where}: the {kind!r} gloss must be a non-empty string — "
                "the reader surfaces render it verbatim (the verb lines' "
                "{kind} slot and the state line's apposition)",
            )

    def _flow_gloss_table(self, *, flow_ids: frozenset[str]) -> None:
        """The flow-gloss table (rs-4, the covering residue's rendering
        half — the reader-surface boundary's pack half):
        `templates.json::flow_glosses`, economy flow id -> reader prose —
        the flow's MEANING, rendered by the renderer at the banking
        lines' `{flow? — {flow}}` tail (the tale + the entity view's
        history, one boundary). OPTIONAL (the dry fallback law — an
        unglossed flow renders NOTHING: the raw id is a machine token,
        never the reader's surface); when present: an object whose keys
        sit in the declared flow ids (a gloss for an undeclared flow is
        dead data, the vacuity law — rs-2's own shape one granularity
        deeper) and whose values are non-empty strings (the surface
        renders the prose VERBATIM — an authored phrase, the em-dash
        tail's own slot)."""
        table = self._data["templates.json"].get(FLOW_GLOSS_BLOCK)
        if table is None:
            return  # the dry fallback law (the unarmed twin)
        where = f"templates.json::{FLOW_GLOSS_BLOCK}"
        _require(
            isinstance(table, Mapping),
            f"{where} must be an object (economy flow id -> reader prose)",
        )
        for flow_id, gloss in table.items():
            _require(
                flow_id in flow_ids,
                f"{where}: the flow {flow_id!r} is not a declared "
                "economy.flows id — a gloss for an undeclared flow is "
                "dead data (the vacuity law)",
            )
            _require(
                isinstance(gloss, str) and bool(gloss.strip()),
                f"{where}: the {flow_id!r} gloss must be a non-empty "
                "string — the banking lines render it verbatim (the "
                "year's-reckoning tail)",
            )

    def _accounts_vocabulary(self, economy: Mapping[str, Any]) -> None:
        """The account-kind vocabulary (`economy.accounts`): the list
        of pack-declared kind names — WHICH accounts exist is pack data
        (the `states` axes' own law: pack names, engine mechanics).
        Required when the block exists (an economy without a vocabulary
        is a block that names nothing); every kind snake_case and
        unique."""
        accounts = economy.get("accounts")
        where = "economy.accounts"
        _require(
            isinstance(accounts, list) and bool(accounts),
            f"{where} must be a non-empty list of account kind names "
            "(WHICH accounts exist is the block's own declaration — the "
            "states axes' law)",
        )
        assert isinstance(accounts, list)  # the require above
        seen: set[str] = set()
        for kind in accounts:
            _require(
                isinstance(kind, str) and bool(_SNAKE_CASE.match(kind)),
                f"{where}: account kind {kind!r} is not snake_case",
            )
            _require(
                kind not in seen,
                f"{where}: duplicate account kind {kind!r}",
            )
            seen.add(kind)

    def _flows(self, economy: Mapping[str, Any]) -> None:
        """The flow declarations (`economy.flows`): the recurring
        aggregate movements on the maclock cadence. The pairing law: a
        pack declaring flows declares `time.macro` (the flows ride the
        clock; presence here, the shape `_time_rules` owns). Each flow:
        the closed per-verb key set, the verb in the closed vocabulary,
        the kind in the accounts vocabulary, the amount a positive
        integer (a zero amount is dead data — the vacuity law), the
        optional `every` a positive integer (the cadence divisor, the
        scheduler rule family), ids unique and snake_case, and the
        VERB'S EVENT TYPE in the template closure (EVENT_SCHEMA §11 —
        the armed pack pays its own corpus price, the arming law)."""
        flows = economy.get("flows", ())
        where = "economy.flows"
        _require(isinstance(flows, list), f"{where} must be a list")
        templates = self._data["templates.json"]["events"]
        time_rules = self._data["rules.json"].get("time", {})
        macro = (
            time_rules.get("macro")
            if isinstance(time_rules, Mapping)
            else None
        )
        seen_ids: set[str] = set()
        seen_caps: set[tuple[str, str]] = set()
        for flow in flows:
            _require(
                isinstance(flow, Mapping),
                f"{where}: every entry must be an object (a notes string "
                "inside a list is not a declaration)",
            )
            verb = flow.get("verb")
            _require(
                verb in _VERB_KEYS,
                f"{where}.{flow.get('id')!r}: verb {verb!r} is not in the "
                f"closed vocabulary {sorted(_VERB_KEYS)}",
            )
            where_flow = f"{where}.{flow['id']!r}"
            keys = _VERB_KEYS[verb]
            unknown = sorted(set(flow) - set(keys) - {"every", "capacity"})
            _require(
                not unknown,
                f"{where_flow}: unknown keys {unknown} (the closed "
                f"vocabulary for a {verb} flow: {list(keys)} + the "
                "optional every)",
            )
            _require(
                isinstance(flow.get("id"), str)
                and bool(_SNAKE_CASE.match(flow["id"])),
                f"{where_flow}: id must be a snake_case string",
            )
            _require(
                flow["id"] not in seen_ids,
                f"{where_flow}: duplicate flow id",
            )
            seen_ids.add(flow["id"])
            _require(
                flow.get("kind") in economy["accounts"],
                f"{where_flow}: kind {flow.get('kind')!r} is not in the "
                "economy.accounts vocabulary",
            )
            _require(
                _is_int(flow.get("amount")) and flow["amount"] >= 1,
                f"{where_flow}: amount must be an integer >= 1 (a zero "
                "amount is dead data — the vacuity law)",
            )
            if "every" in flow:
                _require(
                    _is_int(flow.get("every")) and flow["every"] >= 1,
                    f"{where_flow}: every must be an integer >= 1 (the "
                    "macro-turn divisor — tick-derived arithmetic, never "
                    "entropy)",
                )
            # stageb-1, B4 — the bounded source: a SOURCE flow may
            # declare `capacity` per its (to, kind) stock; the mint is
            # min(declared, capacity - stock), silence at full. One cap
            # per stock — a second capped flow into the same (to, kind)
            # is an ambiguous bound, refused (one owner per fact).
            if "capacity" in flow:
                _require(
                    verb == "source",
                    f"{where_flow}: only a source flow declares capacity "
                    "(the mint-side bound, CONTRACTS §12 B4 — transfers "
                    "and consumes ride the underflow floor alone)",
                )
                _require(
                    _is_int(flow.get("capacity")) and flow["capacity"] >= 1,
                    f"{where_flow}: capacity must be an integer >= 1 (a "
                    "zero cap is dead data — the vacuity law)",
                )
                stock = (flow["to"], flow["kind"])
                _require(
                    stock not in seen_caps,
                    f"{where_flow}: another capped flow already bounds "
                    f"{flow['to']!r}.{flow['kind']!r} — one capacity per "
                    "stock (one owner per fact, the D-024 law)",
                )
                seen_caps.add(stock)
            for endpoint in ("from", "to"):
                if endpoint in keys:
                    _require(
                        isinstance(flow.get(endpoint), str)
                        and bool(flow[endpoint].strip()),
                        f"{where_flow}: {endpoint} must be a non-empty "
                        "entity id",
                    )
            _require(
                verb != "transfer" or flow["from"] != flow["to"],
                f"{where_flow}: a transfer's from and to are the same "
                "entity — a self-transfer is a no-op loop, dead data",
            )
            event_type = VERB_EVENT_TYPES[verb]
            _require(
                event_type in templates,
                f"{where_flow}: the {verb} event {event_type!r} is not in "
                "the template vocabulary (EVENT_SCHEMA §11 — the armed "
                "pack carries the verb's chronicle line, the corpus price "
                "of arming)",
            )
            _require(
                isinstance(macro, Mapping),
                f"{where_flow}: the flows ride the macro clock — the "
                "rules declare no time.macro block (the pairing law: a "
                "pack declaring economy.flows declares the clock)",
            )

    def _recipes(self, economy: Mapping[str, Any]) -> None:
        """The recipe declarations (stageb-1, CONTRACTS §12 B2 — the
        material cycle's transformation edge): `economy.recipes`, the
        flow declaration's own shape family. Each recipe: the closed
        key set id/inputs/outputs, a snake_case unique id, non-empty
        input and output leg lists, each leg the closed holder/kind/
        amount shape with the kind in the accounts vocabulary and the
        amount a positive integer. The EXPLICIT-id holders' entity
        cross-check rides the LATE phase (`_economy_cross` — the
        flow-endpoint law's own shape); noun holders (actor/target)
        resolve through the binding intent at runtime and ride the
        action lint's per-leg solvency law."""
        recipes = economy.get("recipes")
        if recipes is None:
            return  # no recipes — the unarmed law (the 68a pattern)
        where = "economy.recipes"
        _require(isinstance(recipes, list), f"{where} must be a list")
        seen: set[str] = set()
        for recipe in recipes:
            _require(
                isinstance(recipe, Mapping),
                f"{where}: every entry must be an object (id | inputs | "
                "outputs)",
            )
            where_recipe = f"{where}.{recipe.get('id')!r}"
            unknown = sorted(set(recipe) - {"id", "inputs", "outputs"})
            _require(
                not unknown,
                f"{where_recipe}: unknown keys {unknown} (the closed "
                "vocabulary: id | inputs | outputs)",
            )
            _require(
                isinstance(recipe.get("id"), str)
                and bool(_SNAKE_CASE.match(recipe["id"])),
                f"{where_recipe}: id must be a snake_case string",
            )
            _require(
                recipe["id"] not in seen,
                f"{where_recipe}: duplicate recipe id",
            )
            seen.add(recipe["id"])
            for side in ("inputs", "outputs"):
                legs = recipe.get(side)
                _require(
                    isinstance(legs, list) and bool(legs),
                    f"{where_recipe}.{side} must be a non-empty list of "
                    f"leg objects (a recipe with no {side} is dead data — "
                    "the vacuity law)",
                )
                for index, leg in enumerate(legs):
                    leg_where = f"{where_recipe}.{side}[{index}]"
                    _require(
                        isinstance(leg, Mapping),
                        f"{leg_where} must be an object (holder | kind | "
                        "amount)",
                    )
                    leg_unknown = sorted(set(leg) - {"holder", "kind", "amount"})
                    _require(
                        not leg_unknown,
                        f"{leg_where}: unknown keys {leg_unknown} (the "
                        "closed vocabulary: holder | kind | amount)",
                    )
                    holder = leg.get("holder")
                    _require(
                        isinstance(holder, str) and bool(holder.strip()),
                        f"{leg_where}.holder must be a non-empty entity id "
                        "or the noun actor/target",
                    )
                    _require(
                        leg.get("kind") in economy["accounts"],
                        f"{leg_where}.kind {leg.get('kind')!r} is not in "
                        "the economy.accounts vocabulary",
                    )
                    _require(
                        _is_int(leg.get("amount")) and leg["amount"] >= 1,
                        f"{leg_where}.amount must be an integer >= 1 (a "
                        "zero amount is dead data — the vacuity law)",
                    )

    def _prices(self, economy: Mapping[str, Any]) -> None:
        """The price formulas (`economy.prices`): per account kind, the
        integer weights of the derived read-side price `base +
        per_unit * level` (the travel law — add/multiply only; the PACK
        owns the direction, a negative per_unit prices scarcity). The
        base is non-negative (a negative base prices nothing); a
        per_unit of any sign is legal policy. Every priced kind must be
        declared vocabulary (a formula for a nonexistent account is
        dead data)."""
        prices = economy.get("prices")
        if prices is None:
            return  # prices are optional (the read side's own arming)
        where = "economy.prices"
        _require(isinstance(prices, Mapping), f"{where} must be an object")
        for kind, formula in prices.items():
            _require(
                kind in economy["accounts"],
                f"{where}.{kind}: the kind is not in the economy.accounts "
                "vocabulary (a formula for a nonexistent account is dead "
                "data)",
            )
            _require(
                isinstance(formula, Mapping),
                f"{where}.{kind} must be an object (base | per_unit)",
            )
            unknown = sorted(set(formula) - {"base", "per_unit"})
            _require(
                not unknown,
                f"{where}.{kind}: unknown keys {unknown} (the closed "
                "vocabulary: base | per_unit)",
            )
            _require(
                _is_int(formula.get("base")) and formula["base"] >= 0,
                f"{where}.{kind}.base must be an integer >= 0",
            )
            _require(
                _is_int(formula.get("per_unit")),
                f"{where}.{kind}.per_unit must be an integer (the sign is "
                "the pack's own direction policy — a negative per_unit "
                "prices scarcity: the price falls as the stock grows)",
            )

    def _economy_cross(self) -> None:
        """The flow-endpoint cross-checks, LATE (after `_entities`
        validated the records — the worldgen lint's own phase law):
        every flow endpoint must name a DECLARED entity that DECLARES
        an account of the flow's kind — a flow into an undeclared stock
        is a pack bug, never a materialization (the pairing law's
        entity half; the runtime backstop is `_level_or_loud`)."""
        rules = self._data["rules.json"]
        economy = rules.get("economy")
        if not isinstance(economy, Mapping):
            return
        entities = self._data["entities.json"]
        declared: dict[str, set[str]] = {}
        for category in (
            "locations", "npcs", "ambient_entities", "items", "groups",
        ):
            for record in entities.get(category, ()):
                accounts = record.get("accounts")
                if isinstance(accounts, Mapping):
                    declared[record["id"]] = set(accounts)
        for flow in economy.get("flows", ()):
            if not isinstance(flow, Mapping):
                continue
            kind = flow.get("kind")
            for endpoint in ("from", "to"):
                if endpoint not in flow:
                    continue
                entity_id = flow[endpoint]
                holds = declared.get(entity_id)
                _require(
                    holds is not None,
                    f"economy.flows.{flow.get('id')!r}: {endpoint} "
                    f"{entity_id!r} is not a declared entity",
                )
                assert holds is not None  # the require above
                _require(
                    kind in holds,
                    f"economy.flows.{flow.get('id')!r}: {endpoint} "
                    f"{entity_id!r} declares no account of kind "
                    f"{kind!r} — a flow into an undeclared stock is a "
                    "pack bug, never a materialization (the pairing "
                    "law's entity half)",
                )
        # stageb-1, B2 — the recipe legs' entity half: every EXPLICIT
        # holder must name a declared entity declaring the leg's kind
        # (the flow-endpoint law's own shape; noun holders resolve
        # through the binding intent and ride the action lint's
        # per-leg solvency law instead)
        for recipe in economy.get("recipes", ()):
            if not isinstance(recipe, Mapping):
                continue
            for side in ("inputs", "outputs"):
                for leg in recipe.get(side, ()):
                    if not isinstance(leg, Mapping):
                        continue
                    holder = leg.get("holder")
                    if holder in ("actor", "target") or not isinstance(holder, str):
                        continue
                    holds = declared.get(holder)
                    _require(
                        holds is not None,
                        f"economy.recipes.{recipe.get('id')!r}.{side}: "
                        f"holder {holder!r} is not a declared entity",
                    )
                    assert holds is not None  # the require above
                    _require(
                        leg.get("kind") in holds,
                        f"economy.recipes.{recipe.get('id')!r}.{side}: "
                        f"holder {holder!r} declares no account of kind "
                        f"{leg.get('kind')!r} — a recipe into an "
                        "undeclared stock is a pack bug, never a "
                        "materialization (the pairing law's entity half)",
                    )
