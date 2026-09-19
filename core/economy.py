"""The economy substrate (res-1, `docs/CONTRACTS.md` §2 — the mechanism
split's core half, D-175 (1)): the ACCOUNT primitive — a named
non-negative INTEGER stock bound to a canon entity id (any kind the pack
declares it on: npc, location, group — the owner-agnostic form; the
level rides `state_changes` as `account.<kind>`, the position family's
own shape) — plus the THREE VERBS through the canon door:

- **source** — declared units enter an account (the world mints);
- **transfer** — units move between two accounts;
- **consume** — units leave to a declared sink.

The event type names are the build's naming pass (INV-3-clean:
account/source/transfer/consume are mechanic words, pinned by the
stoplist self-check). The ECONOMY stays PACK DATA (the row's own law):
the resource graph — which account kinds exist, source/sink/flow
declarations with amounts and cadences, price formulas — lives in
`rules.json::economy` (`core/packlint/economy.py` owns the load-time
shape lint); this module is the engine's mechanic half only.

The arithmetic is INTEGER-ONLY (the travel law, D-116 (5)): add and
multiply, no division anywhere in the substrate; prices are DERIVED
read-side values — pure functions of pack formulas + stock reads (L3:
never stored, never an event). Flows are AGGREGATE macro-events on the
maclock cadence (the D-112 one-event-with-cardinality surface,
`core/macro.py::macro_turn_draft` the precedent): one event per due
flow per crossing, log growth O(declared flows × macrobeats), never
O(members × ticks); the flows draw nothing (INV-2-clean by
construction — the fingerprint never sees an economy event).

The underflow floor (D3, CONTRACTS §2): a transfer/consume that would
drive an account below zero is world-impossible. The player-scaled arm
dies SOFT at the front door (`account_at_least`, the intent
precondition — attempts are facts, `intent_rejected`); the aggregate
arm and every other write path are refused LOUD at the `_commit` gate
(D-035 — the write never lands; `is_account_prop` is the gate's
predicate, `core/loop.py` the single enforcement point). No code path
ever writes a negative stock.

The irreversibility split (D2): event immutability ≠ stock
immutability. A consume event never un-fires (INV-5's log law); a
stock's LEVEL is an ordinary mutable value — `7 → 12` by a source
event is a legal new event, never a "revert". The `irreversible`
state_change flag is NEVER set on stock props (the wrong instrument),
and the decay pass never touches account props (I5 — `core/states.py`
iterates `status.*` axes only; the separation is pinned by test).

The unarmed landing (D4, the 68a pattern): no committed pack declares
the economy block — zero events, the golden T1 fixtures and the corpora
byte-untouched; the first consumer pack arms it and pays its own corpus
price (the template lines for the three verb types).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from core.intent import pack_importance
from core.log import EventDraft, StateChange
from core.transitions import WORLD

__all__ = [
    "ACCOUNT_PREFIX",
    "CONSUME_EVENT",
    "ECONOMY_BLOCK",
    "SOURCE_EVENT",
    "TRANSFER_EVENT",
    "VERB_EVENT_TYPES",
    "EconomyError",
    "account_level",
    "account_prop",
    "consume_draft",
    "flow_drafts",
    "is_account_prop",
    "price_of",
    "source_draft",
    "transfer_draft",
]

#: The rules.json block this module reads (`core/packlint/economy.py`
#: owns the load-time shape lint). Absent -> zero accounts, zero flows,
#: zero prices — the unarmed law (the 68a pattern).
ECONOMY_BLOCK: Final = "economy"

#: The account prop prefix: an account of kind K on entity E lives at
#: `projection[E]["account.K"]` (the `status.`/`relations.` family's
#: own seeding shape — restated inline at the seeding floor
#: `core/fold.py` and the door's read `core/intent.py`, the family
#: precedent; this constant is the writer-side owner).
ACCOUNT_PREFIX: Final = "account."

#: The three verbs' event types — the build's naming pass (INV-3-clean
#: mechanic words; the armed pack's templates carry the lines, the
#: lint's closure family). Actor/target/state_changes per verb:
#: source — actor WORLD, target the account entity, one gain; transfer
#: — actor the from-entity, target the to-entity, one loss + one gain;
#: consume — actor the entity, no target, one loss.
SOURCE_EVENT: Final = "account_sourced"
TRANSFER_EVENT: Final = "account_transferred"
CONSUME_EVENT: Final = "account_consumed"

VERB_EVENT_TYPES: Final[Mapping[str, str]] = {
    "source": SOURCE_EVENT,
    "transfer": TRANSFER_EVENT,
    "consume": CONSUME_EVENT,
}

#: The flow declaration's closed key set (the lint owns the load-time
#: contract; this is the engine-side mirror the docs cite — one owner
#: per shape, the lint the authority).
FLOW_KEYS: Final = ("id", "verb", "kind", "amount", "every", "from", "to")


class EconomyError(ValueError):
    """An economy contract failure (raw-read surfaces fail loud, never
    with a KeyError — the pred-contract family law, D-111)."""


def account_prop(kind: str) -> str:
    """The projection prop an account of `kind` lives at."""
    return f"{ACCOUNT_PREFIX}{kind}"


def is_account_prop(prop: str) -> bool:
    """The `_commit` gate's predicate (D3's loud arm): does this prop
    name an account stock? The floor check — no negative write, ever —
    keys on this (`core/loop.py` the single enforcement point)."""
    return prop.startswith(ACCOUNT_PREFIX)


def account_level(
    projection: Mapping[str, Mapping[str, Any]], entity: str, kind: str
) -> int | None:
    """The current level of an account, or None when the entity
    declares no stock of that kind (a missing account IS an absent
    stock — the door's `account_at_least` reads the same None as a
    failed gate, the honest answer, never an error)."""
    props = projection.get(entity)
    if props is None:
        return None
    level = props.get(account_prop(kind))
    if not isinstance(level, int) or isinstance(level, bool):
        return None
    return level


def _level_or_loud(
    projection: Mapping[str, Mapping[str, Any]], entity: str, kind: str
) -> int:
    """The flow machinery's stock read: the declared level, LOUD when
    the account does not exist (the lint requires every flow endpoint
    to declare its account; this is the runtime backstop for
    hand-built configs — the MacroError family)."""
    level = account_level(projection, entity, kind)
    if level is None:
        raise EconomyError(
            f"the flow endpoint {entity!r} declares no account of kind "
            f"{kind!r} (projection holds no {account_prop(kind)!r} stock) — "
            "the pack lint requires every flow endpoint to declare the "
            "account; a flow into an undeclared stock is a pack bug, "
            "never a materialization"
        )
    return level


def _flow_cadence(rules: Mapping[str, Any]) -> int:
    """The macro cadence the flows ride (the pairing law: a pack
    declaring flows declares `time.macro`; the lint refuses the
    mismatch at load — this is the runtime backstop, loud like
    `_cadence` in `core/macro.py`)."""
    macro = rules.get("time", {}).get("macro") if isinstance(
        rules.get("time"), Mapping
    ) else None
    if not isinstance(macro, Mapping):
        raise EconomyError(
            "the economy's flows ride the macro clock — the rules declare "
            "no time.macro block (the pairing law: a pack declaring "
            "economy.flows declares the clock)"
        )
    cadence = macro.get("cadence_ticks")
    if not isinstance(cadence, int) or isinstance(cadence, bool) or cadence < 1:
        raise EconomyError(
            f"time.macro.cadence_ticks must be an integer >= 1 for the "
            f"economy's flows, got {cadence!r}"
        )
    return cadence


def _flow_outcome(flow: Mapping[str, Any]) -> dict[str, Any]:
    """The flow event's outcome: the flow id (diagnosability — the
    declared graph's own name), the kind, and the amount as the flat
    integer cardinality key (the D-112 shape — the template binding
    surface, `{amount}`/`{kind}`/`{flow}` the bindable slots)."""
    return {
        "flow": flow["id"],
        "kind": flow["kind"],
        "amount": flow["amount"],
    }


def _draft(
    rules: Mapping[str, Any],
    t: int,
    event_type: str,
    actor: str,
    target: str | None,
    outcome: Mapping[str, Any],
    changes: tuple[StateChange, ...],
) -> EventDraft:
    """The shared draft tail: cause None (the loop chains to the
    writer's last id — the chronological-chain law, the rotation's
    scheduled-beat precedent), no knowledge (a world-scale bookkeeping
    event — the macro turn's own law), no hooks (the director boundary
    is the consumers' rows, never the substrate's), `irreversible`
    never set (D2: the flag is the decay family's instrument, wrong
    for stock props), importance the pack's own rule."""
    entities = {actor}
    if target is not None:
        entities.add(target)
    entities.update(change.entity for change in changes)
    return EventDraft(
        t=t,
        type=event_type,
        actor=actor,
        target=target,
        cause=None,
        outcome=dict(outcome),
        knowledge=(),
        state_changes=changes,
        hooks=(),
        importance=pack_importance(
            rules, entities, irreversible=0, hooks=0, event_type=event_type,
        ),
        provenance={},  # the loop stamps seed at commit (the family law)
    )


def source_draft(
    rules: Mapping[str, Any],
    projection: Mapping[str, Mapping[str, Any]],
    t: int,
    entity: str,
    kind: str,
    amount: int,
    flow_id: str | None = None,
) -> EventDraft:
    """The SOURCE verb: `amount` declared units enter the account —
    the world mints (actor WORLD, the target the account's entity; a
    source can never underflow — it only adds)."""
    level = _level_or_loud(projection, entity, kind)
    outcome: dict[str, Any] = {"kind": kind, "amount": amount}
    if flow_id is not None:
        outcome["flow"] = flow_id
    return _draft(
        rules, t, SOURCE_EVENT, WORLD, entity, outcome,
        (
            StateChange(
                entity=entity, prop=account_prop(kind),
                from_=level, to_=level + amount,
            ),
        ),
    )


def transfer_draft(
    rules: Mapping[str, Any],
    projection: Mapping[str, Mapping[str, Any]],
    t: int,
    from_entity: str,
    to_entity: str,
    kind: str,
    amount: int,
    flow_id: str | None = None,
) -> EventDraft:
    """The TRANSFER verb: `amount` units move between two accounts (the
    from-entity is the doer). A from-stock below `amount` is built
    HONESTLY negative here and refused at the `_commit` gate (D3's loud
    arm — the write never lands; the draft is the evidence, the gate
    the law)."""
    from_level = _level_or_loud(projection, from_entity, kind)
    to_level = _level_or_loud(projection, to_entity, kind)
    outcome: dict[str, Any] = {"kind": kind, "amount": amount}
    if flow_id is not None:
        outcome["flow"] = flow_id
    return _draft(
        rules, t, TRANSFER_EVENT, from_entity, to_entity, outcome,
        (
            StateChange(
                entity=from_entity, prop=account_prop(kind),
                from_=from_level, to_=from_level - amount,
            ),
            StateChange(
                entity=to_entity, prop=account_prop(kind),
                from_=to_level, to_=to_level + amount,
            ),
        ),
    )


def consume_draft(
    rules: Mapping[str, Any],
    projection: Mapping[str, Mapping[str, Any]],
    t: int,
    entity: str,
    kind: str,
    amount: int,
    flow_id: str | None = None,
) -> EventDraft:
    """The CONSUME verb: `amount` units leave the account to a declared
    sink (the entity is the doer; the sink is the declaration's own
    semantics — the units leave the modeled world). An under-level
    stock is built honestly negative and refused at the gate (D3)."""
    level = _level_or_loud(projection, entity, kind)
    outcome: dict[str, Any] = {"kind": kind, "amount": amount}
    if flow_id is not None:
        outcome["flow"] = flow_id
    return _draft(
        rules, t, CONSUME_EVENT, entity, None, outcome,
        (
            StateChange(
                entity=entity, prop=account_prop(kind),
                from_=level, to_=level - amount,
            ),
        ),
    )


def flow_drafts(
    rules: Mapping[str, Any],
    projection: Mapping[str, Mapping[str, Any]],
    t: int,
) -> tuple[EventDraft, ...]:
    """The due economy flows at the macro crossing `t` (the D-112
    aggregate surface): each declared flow fires when its `every`
    cadence divides the macro turn — pure tick-derived integer
    arithmetic, the scheduler rule family (INV-2-clean, draw-free).
    One event per due flow per crossing: log growth O(declared flows ×
    macrobeats), never O(members × ticks). An unarmed economy block
    answers () — zero events, the 68a pattern. Declaration order
    (the pack's own flow list order — construction order, INV-2)."""
    economy = rules.get(ECONOMY_BLOCK)
    if not isinstance(economy, Mapping):
        return ()
    flows = economy.get("flows", ())
    if not flows:
        return ()
    cadence = _flow_cadence(rules)
    turn = t // cadence
    drafts: list[EventDraft] = []
    for flow in flows:
        if not isinstance(flow, Mapping):
            continue  # the section's notes entries (the lint's own law)
        every = flow.get("every", 1)
        if turn % every:
            continue  # not this flow's turn (the cadence arithmetic)
        verb = flow["verb"]
        if verb == "source":
            drafts.append(
                source_draft(
                    rules, projection, t, flow["to"], flow["kind"],
                    flow["amount"], flow_id=flow["id"],
                )
            )
        elif verb == "transfer":
            drafts.append(
                transfer_draft(
                    rules, projection, t, flow["from"], flow["to"],
                    flow["kind"], flow["amount"], flow_id=flow["id"],
                )
            )
        else:  # consume — the lint closes the verb vocabulary
            drafts.append(
                consume_draft(
                    rules, projection, t, flow["from"], flow["kind"],
                    flow["amount"], flow_id=flow["id"],
                )
            )
    return tuple(drafts)


def price_of(rules: Mapping[str, Any], kind: str, level: int) -> int:
    """The DERIVED unit price of one `kind` unit at stock `level`
    (L3 — a pure function of the pack formula + the stock read; never
    stored, never an event, never a state change): the pack-declared
    integer weights `base + per_unit * level` — add/multiply only, no
    division (the travel law). The pack owns the DIRECTION (a negative
    `per_unit` prices scarcity: the price falls as the stock grows);
    the engine owns only the arithmetic. Loud when the kind carries no
    declared formula (the pred-contract family)."""
    economy = rules.get(ECONOMY_BLOCK)
    prices = economy.get("prices") if isinstance(economy, Mapping) else None
    formula = prices.get(kind) if isinstance(prices, Mapping) else None
    if not isinstance(formula, Mapping):
        raise EconomyError(
            f"economy.prices declares no formula for account kind "
            f"{kind!r} — the derived price reads a declared formula "
            "(the lint requires one per priced kind; this is the "
            "runtime backstop)"
        )
    base = formula.get("base")
    per_unit = formula.get("per_unit")
    if not isinstance(base, int) or isinstance(base, bool):
        raise EconomyError(
            f"economy.prices.{kind}.base must be an integer, got {base!r}"
        )
    if not isinstance(per_unit, int) or isinstance(per_unit, bool):
        raise EconomyError(
            f"economy.prices.{kind}.per_unit must be an integer, got "
            f"{per_unit!r}"
        )
    return base + per_unit * level
