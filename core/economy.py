"""The economy substrate (res-1, `docs/CONTRACTS.md` §2 — the mechanism
split's core half, D-175 (1)): the ACCOUNT primitive — a named
non-negative INTEGER stock bound to a canon entity id (any kind the pack
declares it on: npc, location, group — the owner-agnostic form; the
level rides `state_changes` as `account.<kind>`, the position family's
own shape) — plus the FOUR VERBS through the canon door:

- **source** — declared units enter an account (the world mints);
- **transfer** — units move between two accounts;
- **consume** — units leave to a declared sink;
- **settle** — a MULTI-LEG transaction over EXPLICIT owners (iter-273,
  the owner's §6.4 SALE synthesis: the initiator is not implicitly
  the owner of every resource consumed — a location, group or other
  existing holder may own a leg's stock while another actor initiates;
  all legs land as ONE atomic canonical event, the per-leg solvency
  gates the door's own soft arm).

The event type names are the build's naming pass (INV-3-clean:
account/source/transfer/consume/settle are mechanic words, pinned by the
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

from collections.abc import Callable, Mapping
from typing import Any, Final

from core.intent import pack_importance
from core.log import EventDraft, StateChange
from core.transitions import WORLD

__all__ = [
    "ACCOUNT_GLOSS_BLOCK",
    "ACCOUNT_PREFIX",
    "CONSUME_EVENT",
    "CONVERT_EVENT",
    "ECONOMY_BLOCK",
    "LEG_KEYS",
    "RECIPE_KEYS",
    "SETTLE_EVENT",
    "SOURCE_EVENT",
    "TRANSFER_EVENT",
    "VERB_EVENT_TYPES",
    "EconomyError",
    "account_level",
    "account_prop",
    "consume_draft",
    "convert_resolution",
    "flow_drafts",
    "is_account_prop",
    "price_of",
    "recipe_of",
    "source_caps",
    "source_draft",
    "transfer_draft",
    "wear_draft",
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

#: The templates.json block that owns the account-kind glosses (rs-2,
#: the reader-surface boundary over the W5 rendering failure — the
#: W5 first run's finding: the account kind's meaning rendered nowhere,
#: "16 paper owed" indistinguishable from "16 paper held"). A mapping
#: from account KIND to its reader prose; the renderer owns the mapping
#: (`render/chronicle.py::gloss_account_kind` — the verb lines' `{kind}`
#: slot + the state line's apposition), the pack owns the words, and
#: the load-time lint (`core/packlint/economy.py`) owns the shape: keys
#: inside the `economy.accounts` vocabulary, values non-empty strings.
#: An unglossed kind renders dry — the fallback law, rs-1's own family.
#: The constant lives HERE (the engine mechanic vocabulary's single
#: owner) so core, render, and the lint share one spelling — never a
#: second constant (the D-024 anti-drift law).
ACCOUNT_GLOSS_BLOCK: Final = "account_kinds"

#: The flow-gloss block (rs-4, the W5 covering residue's own half): the
#: pack-declared `templates.json::flow_glosses` table — economy flow id ->
#: reader prose, the flow's MEANING (the W5 residues' finding: the +3
#: reckonings read as periodic income because the flow's relation — the
#: fund's climb toward the paper — rendered nowhere; the kind gloss
#: cannot carry it: one kind, many flows, each its own meaning). The
#: load-time lint owns the shape: keys inside the `economy.flows` ids,
#: values non-empty strings, the table without the block refused as dead
#: data. An unglossed flow renders NOTHING at the boundary (the raw id
#: is a machine token, rs-1's own law — never the reader's surface).
#: The constant lives HERE for the same one-spelling reason as above.
FLOW_GLOSS_BLOCK: Final = "flow_glosses"

#: The three single-stock verbs' event types — the build's naming pass
#: (INV-3-clean mechanic words; the armed pack's templates carry the
#: lines, the lint's closure family). Actor/target/state_changes per
#: verb: source — actor WORLD, target the account entity, one gain;
#: transfer — actor the from-entity, target the to-entity, one loss +
#: one gain; consume — actor the entity, no target, one loss.
SOURCE_EVENT: Final = "account_sourced"
TRANSFER_EVENT: Final = "account_transferred"
CONSUME_EVENT: Final = "account_consumed"

#: The settle verb's event type (iter-273, the §6.4 SALE synthesis):
#: ONE atomic canonical event carrying every leg's state changes —
#: actor the INITIATOR (never implicitly any leg's owner), target the
#: intent's own target (may be None — the legs name their parties),
#: the outcome carrying the resolved legs, one net state change per
#: touched account. The same mechanism serves sales, tolls,
#: settlements, withdrawals, wages — any ordinary resource
#: relationship between existing holders (the owner's class law:
#: never a per-case verb).
SETTLE_EVENT: Final = "account_settled"

#: The convert verb's event type (stageb-1, CONTRACTS §12 B2 — the
#: material cycle's transformation edge): ONE atomic RECIPE event —
#: inputs consumed, outputs produced, every leg's state changes in
#: the SAME canonical event (the settle precedent's atomic multi-leg
#: law; the float law respected by construction — no chained second
#: verb ever reads pre-first state). Actor the INITIATOR, target the
#: intent's own target, the outcome carrying the recipe id + the
#: resolved input/output legs (the flow outcome's diagnosability
#: form). Conservation is PER RECIPE, fold-checkable per kind. The
#: type rides the pack-defined snake_case vocabulary — additive, no
#: schema change (EVENT_SCHEMA §2's free-form type; the armed pack's
#: templates carry the line, the lint's closure family).
CONVERT_EVENT: Final = "account_converted"

VERB_EVENT_TYPES: Final[Mapping[str, str]] = {
    "source": SOURCE_EVENT,
    "transfer": TRANSFER_EVENT,
    "consume": CONSUME_EVENT,
    "settle": SETTLE_EVENT,
    "convert": CONVERT_EVENT,
}

#: The flow declaration's closed key set (the lint owns the load-time
#: contract; this is the engine-side mirror the docs cite — one owner
#: per shape, the lint the authority).
FLOW_KEYS: Final = ("id", "verb", "kind", "amount", "every", "from", "to")

#: The settle leg's closed key set (iter-273): `from`/`to` name the
#: leg's owners — the nouns `actor`/`target` resolve through the
#: intent, any other value is an EXPLICIT entity id (the lint's
#: cross-check: a declared entity declaring the leg's kind — the flow
#: endpoint precedent); `kind` an economy.accounts kind; `amount` a
#: positive integer. The lint (`core/packlint/actions.py`) owns the
#: load-time contract; this mirror is the docs' single citation.
LEG_KEYS: Final = ("from", "to", "kind", "amount")

#: The recipe leg's closed key set (stageb-1, CONTRACTS §12 B2):
#: `holder` — the noun `actor`/`target` or an explicit entity id (the
#: settle leg's resolution family); `kind` an economy.accounts kind;
#: `amount` a positive integer. An INPUT leg drains its holder's
#: stock (the per-leg solvency gates the door — the haul's own
#: form); an OUTPUT leg produces into its holder's. The lint
#: (`core/packlint/economy.py`) owns the load-time contract; this
#: mirror is the docs' single citation.
RECIPE_KEYS: Final = ("holder", "kind", "amount")


#: The recipe declaration's closed key set (stageb-1, B2): id,
#: inputs, outputs — the flow declaration's own shape family.
RECIPE_DECL_KEYS: Final = ("id", "inputs", "outputs")


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


def recipe_of(rules: Mapping[str, Any], recipe_id: str) -> Mapping[str, Any]:
    """The declared recipe by id (stageb-1, B2) — LOUD when absent (the
    pred-contract family: the lint pinned the id at load, this is the
    runtime backstop for hand-built configs)."""
    economy = rules.get(ECONOMY_BLOCK)
    recipes = economy.get("recipes") if isinstance(economy, Mapping) else None
    if isinstance(recipes, list):
        for recipe in recipes:
            if (
                isinstance(recipe, Mapping)
                and recipe.get("id") == recipe_id
            ):
                return recipe
    raise EconomyError(
        f"economy.recipes declares no recipe {recipe_id!r} — the convert "
        "verb reads a declared recipe (the lint requires the binding "
        "action to name one; this is the runtime backstop)"
    )


def convert_resolution(
    rules: Mapping[str, Any],
    projection: Mapping[str, Mapping[str, Any]],
    t: int,
    recipe_id: str,
    holders: "Callable[[str], str]",
) -> tuple[dict[str, Any], tuple[StateChange, ...]]:
    """The convert verb's resolution half (stageb-1, B2): the recipe's
    input legs drain, its output legs produce, ONE net state change
    per touched (entity, kind) — the settle aggregation's own law
    (the commit gate's progressive semantics never sees a chained
    intermediate). `holders` resolves each leg's holder reference
    (the settle `_leg_entity` family — nouns through the intent,
    explicit ids as themselves). Returns (outcome, state_changes):
    the outcome carrying the recipe id + the RESOLVED legs (the flow
    outcome's diagnosability form), the changes first-touch in
    construction order (INV-2). The per-input solvency gates the
    DOOR (the lint-required account_at_least preconditions — the
    haul's own form); the reads here are live at completion
    (KI#13's law), an underflow refused LOUD at the commit floor
    (D3 — the same net law as every other write path)."""
    recipe = recipe_of(rules, recipe_id)
    order: list[tuple[str, str]] = []  # first-touch — construction order
    net: dict[tuple[str, str], int] = {}
    resolved_inputs: list[dict[str, Any]] = []
    resolved_outputs: list[dict[str, Any]] = []
    for legs, sign, sink in (
        (recipe.get("inputs", ()), -1, resolved_inputs),
        (recipe.get("outputs", ()), +1, resolved_outputs),
    ):
        for leg in legs:
            holder = holders(leg["holder"])
            leg_kind = leg["kind"]
            if (holder, leg_kind) not in net:
                net[(holder, leg_kind)] = 0
                order.append((holder, leg_kind))
            net[(holder, leg_kind)] += sign * leg["amount"]
            sink.append({
                "holder": holder, "kind": leg_kind,
                "amount": leg["amount"],
            })
    changes: list[StateChange] = []
    for entity, leg_kind in order:
        level = _level_or_loud(projection, entity, leg_kind)
        changes.append(
            StateChange(
                entity=entity, prop=account_prop(leg_kind),
                from_=level, to_=level + net[(entity, leg_kind)],
            )
        )
    outcome: dict[str, Any] = {
        "recipe": recipe_id,
        "inputs": resolved_inputs,
        "outputs": resolved_outputs,
    }
    return outcome, tuple(changes)


def source_caps(
    rules: Mapping[str, Any],
) -> dict[tuple[str, str], int]:
    """The declared source-flow capacities (stageb-1, B4): (to-entity,
    kind) -> cap — the mint-side bound the `_commit` floor enforces
    (a write above a declared cap refused LOUD, any verb — B1's
    "never" arm; the flow's own mint stays compliant by the min()
    arithmetic). The lint refuses two capped flows into one stock
    (one cap owner per (entity, kind)); an unarmed economy answers
    {} — no caps, no floor arm, the 68a pattern."""
    economy = rules.get(ECONOMY_BLOCK)
    if not isinstance(economy, Mapping):
        return {}
    caps: dict[tuple[str, str], int] = {}
    for flow in economy.get("flows", ()):
        if not isinstance(flow, Mapping) or flow.get("verb") != "source":
            continue
        capacity = flow.get("capacity")
        if capacity is not None:
            caps[(flow["to"], flow["kind"])] = int(capacity)
    return caps


def wear_draft(
    rules: Mapping[str, Any],
    projection: Mapping[str, Mapping[str, Any]],
    t: int,
    user: str,
    holder: str,
    kind: str,
    amount: int,
    used_action: str,
) -> EventDraft:
    """The use-hook's wear draft (stageb-1, B3): a per-USE integer
    consume on the instrument's own stock, fired at the consuming
    action's completion — the instrument NAMED in the event (target
    = the stock's holder, outcome's `use` = the action that wore
    it; the flagged_accessible referents' own diagnose form). Break
    at zero: the 0-crossing is the LAST use (the stock reads broken
    — fold-derivable, L3, never a second status axis); a use that
    would drive the stock below zero is world-impossible, refused
    SOFTLY at the door by the lint-required account_at_least
    precondition (attempts are facts). NO wall-clock anywhere (the
    I5 fence holds — decay stays NPC-status-only)."""
    level = _level_or_loud(projection, holder, kind)
    return _draft(
        rules, t, CONSUME_EVENT, user, holder,
        {"kind": kind, "amount": amount, "use": used_action},
        (
            StateChange(
                entity=holder, prop=account_prop(kind),
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
            # stageb-1, B4 — the bounded source: at full cap the flow
            # is NOT DUE (zero events, the every-miss form — the
            # noise law's precedent); the mint is min(declared,
            # capacity - stock) — tick+stock-derived, draw-free
            # (INV-2-clean; the stock is a fold of the log)
            capacity = flow.get("capacity")
            if capacity is not None:
                stock = _level_or_loud(projection, flow["to"], flow["kind"])
                room = int(capacity) - stock
                if room <= 0:
                    continue  # full — silence (the every-miss form)
                amount = min(flow["amount"], room)
            else:
                amount = flow["amount"]
            drafts.append(
                source_draft(
                    rules, projection, t, flow["to"], flow["kind"],
                    amount, flow_id=flow["id"],
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
