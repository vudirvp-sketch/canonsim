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

from core.economy import VERB_EVENT_TYPES
from core.packlint.helpers import _SNAKE_CASE, PackError, _is_int, _require

#: The economy block's closed key vocabulary (the engine-side mirror
#: `core/economy.py` reads; this lint is the authority).
ECONOMY_KEYS: Final = ("accounts", "flows", "prices", "notes")

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
            return  # the unarmed law
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
        self._flows(economy)
        self._prices(economy)

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
            unknown = sorted(set(flow) - set(keys) - {"every"})
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
                _require(
                    kind in holds,
                    f"economy.flows.{flow.get('id')!r}: {endpoint} "
                    f"{entity_id!r} declares no account of kind "
                    f"{kind!r} — a flow into an undeclared stock is a "
                    "pack bug, never a materialization (the pairing "
                    "law's entity half)",
                )
