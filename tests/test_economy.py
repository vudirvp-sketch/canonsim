"""iter-146 acceptance — res-1, the economy substrate (CONTRACTS §2,
D-175's mechanism split): the account primitive, the three verbs
through the canon door, the flows on the macro cadence, the derived
prices — landed UNARMED (D4: no committed pack declares the block, the
corpora byte-untouched — pinned by the green T1s and the unarmed test
below).

The laws pinned here (the contract's minimal test set, §2.3):

- **I1/F1 CONSERVATION** — every account's folded balance equals its
  initial level plus the verb events' declared deltas, and NOTHING
  outside the three verbs ever touches an account prop; the oracle is
  an INDEPENDENT re-derivation (a test-side ledger replay over the raw
  event list, never the runtime's own fold — TEST_PLAN §9's oracle
  law), with the per-verb delta shapes verified against the outcomes'
  declared amounts (aggregate AND discrete events both).
- **I3/F2 THE UNDERFLOW FLOOR** — both refusal arms: the soft door
  (a player-scaled spend beyond the stock dies as `intent_rejected`,
  no state write) and the loud gate (an aggregate flow beyond its
  stock raises at `_commit` BEFORE the write — the log never holds a
  negative stock).
- **I5 THE DECAY SEPARATION** — account props never appear in the
  decay pass's axis set; a long-horizon run's stock is unchanged
  without economic events.
- **I4/F-determinism + I6 THE UNARMED LAW** — integer-only arithmetic,
  same seed → byte-identical logs; the committed packs declare no
  economy block (their corpora are the T1 fixtures' own bytes).
- **INV-3** — the stoplist self-check over the new names
  (account/source/transfer/consume are mechanic words, never setting
  nouns).
- **THE PRICE LAW** — prices are derived read-side values: same inputs
  → same value, integer add/multiply only, never stored, never logged.

Plus the lint family (the crafted-variant refusals), the flow cadence
arithmetic (the `every` divisor — the scheduler rule family), the
discrete verbs' event shapes, and the §9 falsifier pins in their
minimal test form: F3 (the player-decision effect — the same-seed fork
where spending early changes the world's later answers) and F4 (the
one-knob ablation — a perturbed flow moves the economy's surface and
leaves every non-economy event byte-identical). The full measured
claim packet runs in the sandbox driver outside the repo (Rule 9).
"""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.economy import (
    ACCOUNT_GLOSS_BLOCK,
    CONSUME_EVENT,
    ECONOMY_BLOCK,
    FLOW_GLOSS_BLOCK,
    SOURCE_EVENT,
    TRANSFER_EVENT,
    VERB_EVENT_TYPES,
    EconomyError,
    account_level,
    account_prop,
    consume_draft,
    flow_drafts,
    is_account_prop,
    price_of,
    source_draft,
    transfer_draft,
)
from core.log import StateChange, event_to_mapping, read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack
from core.states import decay_drafts

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

PLAYER = "pc_01"
BARKEEP = "npc_barkeep_01"
DRUNK = "npc_drunk_01"
TAVERN = "loc_tavern"

#: The crafted arming's account stocks (the entity-declared `accounts`
#: mappings — the seeding under test).
DEFAULT_ACCOUNTS: dict[str, dict[str, int]] = {
    PLAYER: {"coin": 10},
    BARKEEP: {"coin": 5, "grain": 0},
    DRUNK: {"coin": 30},
    TAVERN: {"coin": 0, "grain": 4},
}

#: The crafted economy block: all three verbs on the flow side, the
#: `every: 2` transfer gating alternate turns, one priced kind with a
#: NEGATIVE per_unit (scarcity pricing — the price falls as the stock
#: grows; the pack owns the direction).
DEFAULT_ECONOMY: dict[str, Any] = {
    "accounts": ["coin", "grain"],
    "flows": [
        {"id": "barkeep_tally", "verb": "transfer", "kind": "coin",
         "from": BARKEEP, "to": TAVERN, "amount": 1, "every": 2},
        {"id": "hearth_cost", "verb": "consume", "kind": "coin",
         "from": DRUNK, "amount": 1},
        {"id": "grain_delivery", "verb": "source", "kind": "grain",
         "to": TAVERN, "amount": 2},
    ],
    "prices": {"grain": {"base": 10, "per_unit": -1}},
}

#: The player-scaled transfer action (the discrete arm): the
#: `events.success` restatement is the load-time cross-check; the
#: `account_at_least` gate is the underflow floor's soft arm.
GIVE_ACTION: dict[str, Any] = {
    "intent": "give_coin", "label": "give_coin", "resolver": "account",
    "ticks": 10,
    "events": {"success": TRANSFER_EVENT},
    "requires": [
        {"test": "kind", "noun": "target", "is": "npc"},
        {"test": "account_at_least", "noun": "actor", "kind": "coin",
         "value": 2},
    ],
    "fields": [],
    "account": {"verb": "transfer", "kind": "coin", "amount": 2},
    "knowledge": {
        "success": [
            {"who": "actor", "channel": "saw", "fidelity": "exact",
             "knows": "gave_coin_to_{target}"},
            {"who": "target", "channel": "saw", "fidelity": "exact",
             "knows": "received_coin_from_{actor}"},
        ]
    },
    "notes": "res-1 fixture: the player-scaled transfer",
}

SPEND_ACTION: dict[str, Any] = {
    "intent": "spend_coin", "label": "spend_coin", "resolver": "account",
    "ticks": 5,
    "events": {"success": CONSUME_EVENT},
    "requires": [
        {"test": "account_at_least", "noun": "actor", "kind": "coin",
         "value": 3},
    ],
    "fields": [],
    "account": {"verb": "consume", "kind": "coin", "amount": 3},
    "knowledge": {
        "success": [
            {"who": "actor", "channel": "saw", "fidelity": "exact",
             "knows": "spent_coin"},
        ]
    },
    "notes": "res-1 fixture: the player-scaled consume",
}

FIND_ACTION: dict[str, Any] = {
    "intent": "find_coin", "label": "find_coin", "resolver": "account",
    "ticks": 5,
    "events": {"success": SOURCE_EVENT},
    "requires": [],
    "fields": [],
    "account": {"verb": "source", "kind": "coin", "amount": 4},
    "knowledge": {
        "success": [
            {"who": "actor", "channel": "saw", "fidelity": "exact",
             "knows": "found_coin"},
        ]
    },
    "notes": "res-1 fixture: the player-scaled source (the world mints "
             "to the actor)",
}

VERB_TEMPLATES: dict[str, str] = {
    SOURCE_EVENT: "The {target} gains {amount} {kind}.",
    TRANSFER_EVENT: "{actor} gives {amount} {kind} to {target}.",
    CONSUME_EVENT: "{actor} spends {amount} {kind}.",
}


def economy_pack(
    tmp_path: Path,
    name: str,
    *,
    economy: Any = "default",
    accounts: Any = "default",
    cadence: int = 40,
    extra_actions: tuple[dict[str, Any], ...] = (
        GIVE_ACTION, SPEND_ACTION, FIND_ACTION,
    ),
    verb_lines: bool = True,
    mutate: Any = None,
) -> Pack:
    """A committed-pack copy with the economy armed: `time.macro`'s
    cadence shrunk to cross inside a short wait, the entity `accounts`
    merged in, the economy block set (None removes it — the unarmed
    twin), the three player-scaled account actions appended (empty
    tuple omits them), the verb template lines managed (False removes
    them — the closure-refusal arm). `mutate`, when given, receives
    the whole four-file data dict BEFORE the write+load — the lint
    refusal tests' injection point (a mutation the lint must catch)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    data: dict[str, Any] = {
        file_name: json.loads((target / file_name).read_text(encoding="utf-8"))
        for file_name in (
            "actions.json", "entities.json", "rules.json", "templates.json",
        )
    }
    if accounts == "default":
        accounts = DEFAULT_ACCOUNTS
    if accounts is not None:
        entities = data["entities.json"]
        for category in (
            "locations", "npcs", "ambient_entities", "items", "groups",
        ):
            for record in entities.get(category, ()):
                merged = accounts.get(record["id"])
                if merged is not None:
                    # deep copy: the fixture constants are module-level —
                    # a refusal test's mutation must never poison them
                    record["accounts"] = json.loads(json.dumps(merged))
    rules = data["rules.json"]
    rules["time"]["macro"] = {
        "cadence_ticks": cadence, "event_type": "year_turns",
    }
    if economy == "default":
        rules[ECONOMY_BLOCK] = json.loads(json.dumps(DEFAULT_ECONOMY))
    elif economy is not None:
        rules[ECONOMY_BLOCK] = economy
    if extra_actions:
        data["actions.json"]["actions"].extend(
            json.loads(json.dumps(a)) for a in extra_actions
        )
    templates = data["templates.json"]
    for event_type, line in VERB_TEMPLATES.items():
        if verb_lines:
            templates["events"][event_type] = line
        else:
            templates["events"].pop(event_type, None)
    if mutate is not None:
        mutate(data)
    for file_name, payload in data.items():
        (target / file_name).write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )
    return load_pack(target)


def _run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]], name: str,
) -> tuple[Path, Any]:
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    result = sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    sim.close()
    return log, result


def _events(log: Path) -> list[Any]:
    _, events = read_log(log, SCHEMA)
    return events


def _by_type(events: list[Any], *types: str) -> list[Any]:
    return [event for event in events if event.type in types]


#: one wait long enough to cross three 40-tick macro turns (the queue
#: drains before the fourth crossing — the never-pre-seeded law)
WAIT_130: list[dict[str, Any]] = [{"intent": "wait", "ticks": 130}]


# -- the substrate units -------------------------------------------------------


def test_the_prop_helpers_and_the_seeding() -> None:
    """The account primitive's read surface: `account.<kind>` props
    seeded from the entity `accounts` mappings (the status/relations
    family's own shape), `is_account_prop` the commit gate's
    predicate, `account_level` answering None for an absent stock (a
    missing account IS an absent stock — the honest answer)."""
    assert account_prop("coin") == "account.coin"
    assert is_account_prop("account.coin")
    assert not is_account_prop("status.fatigue")
    assert not is_account_prop("position")
    projection = {
        PLAYER: {account_prop("coin"): 10},
        BARKEEP: {account_prop("grain"): 0},
    }
    assert account_level(projection, PLAYER, "coin") == 10
    assert account_level(projection, BARKEEP, "grain") == 0
    assert account_level(projection, PLAYER, "grain") is None
    assert account_level(projection, TAVERN, "coin") is None
    assert account_level({}, PLAYER, "coin") is None


def test_the_draft_builders_shapes() -> None:
    """The three verbs' emission surfaces: actor/target per verb (source
    — WORLD over the account entity; transfer — the from-entity over
    the to-entity; consume — the entity, no target), the state_changes
    reading the LIVE projection (KI#13 — from never hardcoded), the
    outcome's flat cardinality keys, `irreversible` never set (D2: the
    flag is the decay family's instrument, wrong for stocks), no
    knowledge, no hooks. A missing account is the loud EconomyError
    (the runtime backstop — the lint owns the load-time law)."""
    projection = {
        PLAYER: {account_prop("coin"): 10},
        BARKEEP: {account_prop("coin"): 5},
    }
    source = source_draft(PACK.rules, projection, 40, PLAYER, "coin", 4)
    assert source.type == SOURCE_EVENT
    assert source.actor == "world" and source.target == PLAYER
    assert source.outcome == {"kind": "coin", "amount": 4}
    assert source.state_changes == (
        StateChange(PLAYER, account_prop("coin"), 10, 14),
    )
    assert not source.state_changes[0].irreversible
    transfer = transfer_draft(
        PACK.rules, projection, 40, PLAYER, BARKEEP, "coin", 2
    )
    assert transfer.type == TRANSFER_EVENT
    assert transfer.actor == PLAYER and transfer.target == BARKEEP
    assert transfer.state_changes == (
        StateChange(PLAYER, account_prop("coin"), 10, 8),
        StateChange(BARKEEP, account_prop("coin"), 5, 7),
    )
    consume = consume_draft(PACK.rules, projection, 40, PLAYER, "coin", 2)
    assert consume.type == CONSUME_EVENT
    assert consume.actor == PLAYER and consume.target is None
    assert consume.state_changes == (
        StateChange(PLAYER, account_prop("coin"), 10, 8),
    )
    for draft in (source, transfer, consume):
        assert draft.knowledge == () and draft.hooks == ()
    with pytest.raises(EconomyError, match="declares no account"):
        source_draft(PACK.rules, projection, 40, TAVERN, "coin", 1)


def test_the_flow_cadence_arithmetic_and_the_backstops() -> None:
    """The `every` divisor: a flow fires on the macro turns its
    cadence divides — pure tick-derived integer arithmetic (the
    scheduler rule family, INV-2-clean). The unarmed law: no economy
    block answers (). The pairing backstops: flows without a macro
    clock, and a broken cadence, fail loud (the MacroError family —
    never a KeyError)."""
    rules = dict(PACK.rules)
    rules["time"] = {**dict(PACK.rules["time"]),
                     "macro": {"cadence_ticks": 40, "event_type": "year_turns"}}
    rules[ECONOMY_BLOCK] = json.loads(json.dumps(DEFAULT_ECONOMY))
    projection = {
        BARKEEP: {account_prop("coin"): 50},
        DRUNK: {account_prop("coin"): 50},
        TAVERN: {account_prop("coin"): 0, account_prop("grain"): 4},
    }
    # turn 1 (t=40): the every=2 transfer is NOT due; consume + source are
    due = flow_drafts(rules, projection, 40)
    assert [draft.outcome["flow"] for draft in due] == [
        "hearth_cost", "grain_delivery",
    ]
    # turn 2 (t=80): all three due — declaration order (INV-2)
    due = flow_drafts(rules, projection, 80)
    assert [draft.outcome["flow"] for draft in due] == [
        "barkeep_tally", "hearth_cost", "grain_delivery",
    ]
    # turn 3 (t=120): the transfer skips again
    due = flow_drafts(rules, projection, 120)
    assert [draft.outcome["flow"] for draft in due] == [
        "hearth_cost", "grain_delivery",
    ]
    # the unarmed law
    unarmed = dict(rules)
    unarmed.pop(ECONOMY_BLOCK)
    assert flow_drafts(unarmed, projection, 40) == ()
    # the pairing backstop: flows declared, clock removed
    clockless = dict(rules)
    clockless["time"] = {
        **dict(rules["time"]),
        "macro": None,
    }
    with pytest.raises(EconomyError, match="time.macro"):
        flow_drafts(clockless, projection, 40)
    # the cadence backstop: a hand-broken clock is loud
    broken = dict(rules)
    broken["time"] = {
        **dict(rules["time"]),
        "macro": {"cadence_ticks": 0, "event_type": "year_turns"},
    }
    with pytest.raises(EconomyError, match="cadence_ticks"):
        flow_drafts(broken, projection, 40)


def test_the_price_law_purity_and_arithmetic() -> None:
    """Prices are DERIVED read-side values (L3): `base + per_unit *
    level` — integer add/multiply only, no division anywhere (the
    travel law); the pack owns the DIRECTION (a negative per_unit
    prices scarcity). Purity: same inputs → the same value, twice;
    loud EconomyError for a kind without a declared formula (the
    pred-contract family)."""
    rules = dict(PACK.rules)
    rules[ECONOMY_BLOCK] = json.loads(json.dumps(DEFAULT_ECONOMY))
    assert price_of(rules, "grain", 0) == 10
    assert price_of(rules, "grain", 4) == 6
    assert price_of(rules, "grain", 10) == 0
    assert price_of(rules, "grain", 4) == 6  # purity: same inputs, same value
    with pytest.raises(EconomyError, match="declares no formula"):
        price_of(rules, "coin", 0)  # coin carries no formula in the fixture


# -- the unarmed law + INV-3 ---------------------------------------------------


def test_the_committed_packs_land_unarmed() -> None:
    """D4 (the arming law, the 68a pattern): the tavern and the road
    declare no economy block and no entity accounts — their golden T1
    fixtures and corpora byte-untouched (the T1 suites' own green run
    is the byte-identity pin; this test pins the unarmed precondition
    itself). iter-148 (pack-1): the GRIM pack is the armed FIRST
    CONSUMER; iter-149 (pack-4): the PRESSURE pack the second; iter-162
    (debt-1): the PROVINCE the third — the crossing household's flood
    debt (each declaration IS the arming, the corpus price its own: the
    verb template lines; the province's flows ride the macro year,
    beyond its day-scale golden corpus by construction), so the unarmed
    law now reads "every pack before the first consumer", never "every
    pack forever"."""
    for pack_dir in sorted((REPO / "content").iterdir()):
        if not pack_dir.is_dir():
            continue
        if pack_dir.name in (
            "grim_pack", "pressure_pack", "province_pack",  # the armed
        ):  # consumers (the first, the second, the third)
            rules = json.loads(
                (pack_dir / "rules.json").read_text(encoding="utf-8")
            )
            assert ECONOMY_BLOCK in rules  # the arming itself
            continue
        rules = json.loads(
            (pack_dir / "rules.json").read_text(encoding="utf-8")
        )
        assert ECONOMY_BLOCK not in rules, pack_dir.name
        entities = json.loads(
            (pack_dir / "entities.json").read_text(encoding="utf-8")
        )
        for category in (
            "locations", "npcs", "ambient_entities", "items", "groups",
        ):
            for record in entities.get(category, ()):
                assert "accounts" not in record, (
                    f"{pack_dir.name}/{record['id']}"
                )


def test_the_new_names_are_inv3_clean() -> None:
    """INV-3's stoplist self-check over the build's naming pass: the
    substrate's mechanic vocabulary (account, source, transfer,
    consume, economy, flow, price and the event-type spellings) must
    never collide with a pack's setting nouns — the engine words stay
    legal precisely because no stoplist word matches them as a
    segment."""
    stoplist_path = Path(__file__).resolve().parent / "test_inv3_stoplist.py"
    spec = importlib.util.spec_from_file_location(
        "test_inv3_stoplist_under_economy", stoplist_path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    words = (
        "account", "source", "transfer", "consume", "economy", "flow",
        "price", "stock", "verb", "amount",
        "account_sourced", "account_transferred", "account_consumed",
        "account_at_least",
    )
    banned = module._segment_pattern
    collisions = [
        (word, stop)
        for word in words
        for stop in (
            *module.STOPLIST, *module.ROAD_STOPLIST, *module.PROVINCE_STOPLIST,
        )
        if banned(stop).search(word)
    ]
    assert not collisions, (
        f"the substrate's mechanic vocabulary collides with setting "
        f"nouns: {collisions}"
    )


# -- the lint family (crafted-variant refusals) --------------------------------


def _refusal(tmp_path: Path, name: str, mutate) -> None:
    """Craft an armed variant with the mutation applied to the raw
    four-file data BEFORE the load, expect the clean PackError (never
    a KeyError/AttributeError from a later lint — the KI#77 order
    law)."""
    with pytest.raises(PackError):
        economy_pack(tmp_path, name, mutate=mutate)


def test_the_economy_lint_refusals(tmp_path: Path) -> None:
    """The block's closed vocabulary and shapes: unknown block keys,
    an empty vocabulary, a dead flow kind, a zero amount, a zero
    cadence divisor, a verb typo, a duplicate id, a self-transfer, the
    missing verb template line (the closure law), flows without the
    macro clock (the pairing law)."""
    def bad_block(data: dict) -> None:
        data["rules.json"][ECONOMY_BLOCK]["sinks"] = []

    def bad_vocabulary(data: dict) -> None:
        data["rules.json"][ECONOMY_BLOCK]["accounts"] = []

    def bad_kind(data: dict) -> None:
        data["rules.json"][ECONOMY_BLOCK]["flows"][0]["kind"] = "silver"

    def bad_amount(data: dict) -> None:
        data["rules.json"][ECONOMY_BLOCK]["flows"][0]["amount"] = 0

    def bad_every(data: dict) -> None:
        data["rules.json"][ECONOMY_BLOCK]["flows"][0]["every"] = 0

    def bad_verb(data: dict) -> None:
        data["rules.json"][ECONOMY_BLOCK]["flows"][0]["verb"] = "mint"

    def bad_duplicate_id(data: dict) -> None:
        flows = data["rules.json"][ECONOMY_BLOCK]["flows"]
        flows[1]["id"] = flows[0]["id"]

    def bad_self_transfer(data: dict) -> None:
        flow = data["rules.json"][ECONOMY_BLOCK]["flows"][0]
        flow["verb"] = "transfer"
        flow["to"] = flow["from"]

    def bad_closure(data: dict) -> None:
        data["templates.json"]["events"].pop(SOURCE_EVENT)

    def bad_pairing(data: dict) -> None:
        data["rules.json"]["time"].pop("macro")
        data["rules.json"].pop("weather")  # the family binds to the clock

    # rs-2 (iter-191): the account-kind gloss table's own refusals —
    # a dead row (an undeclared kind), a non-string gloss, a
    # non-object table, and the table without the economy block (all
    # dead data by the same vacuity law)
    def bad_gloss_kind(data: dict) -> None:
        data["templates.json"][ACCOUNT_GLOSS_BLOCK] = {"silver": "owed"}

    def bad_gloss_value(data: dict) -> None:
        data["templates.json"][ACCOUNT_GLOSS_BLOCK] = {"coin": 3}

    def bad_gloss_shape(data: dict) -> None:
        data["templates.json"][ACCOUNT_GLOSS_BLOCK] = ["coin"]

    def bad_gloss_without_block(data: dict) -> None:
        data["templates.json"][ACCOUNT_GLOSS_BLOCK] = {"coin": "owed"}
        data["rules.json"].pop(ECONOMY_BLOCK)

    # rs-4 (iter-199): the flow-gloss table's own refusals — a dead row
    # (a gloss for an undeclared flow id), a non-string gloss, a
    # non-object table, and the table without the economy block (the
    # same vacuity law, one granularity deeper than rs-2's)
    def bad_flow_gloss_id(data: dict) -> None:
        data["templates.json"][FLOW_GLOSS_BLOCK] = {
            "the_dead_flow": "owed",
        }

    def bad_flow_gloss_value(data: dict) -> None:
        data["templates.json"][FLOW_GLOSS_BLOCK] = {
            "barkeep_tally": 3,
        }

    def bad_flow_gloss_shape(data: dict) -> None:
        data["templates.json"][FLOW_GLOSS_BLOCK] = ["barkeep_tally"]

    def bad_flow_gloss_without_block(data: dict) -> None:
        data["templates.json"][FLOW_GLOSS_BLOCK] = {
            "barkeep_tally": "owed",
        }
        data["rules.json"].pop(ECONOMY_BLOCK)

    for mutate in (
        bad_block, bad_vocabulary, bad_kind, bad_amount, bad_every,
        bad_verb, bad_duplicate_id, bad_self_transfer, bad_closure,
        bad_pairing, bad_gloss_kind, bad_gloss_value, bad_gloss_shape,
        bad_gloss_without_block, bad_flow_gloss_id, bad_flow_gloss_value,
        bad_flow_gloss_shape, bad_flow_gloss_without_block,
    ):
        _refusal(tmp_path, f"eco_{mutate.__name__}", mutate)


def test_the_entity_and_cross_lint_refusals(tmp_path: Path) -> None:
    """The pairing law's entity half: entity accounts without the
    economy block are dead data (refused); a flow endpoint that is not
    a declared entity, or an entity that declares no account of the
    flow's kind, is refused by the LATE cross phase (a flow into an
    undeclared stock is a pack bug, never a materialization)."""
    def accounts_without_block(data: dict) -> None:
        data["rules.json"].pop(ECONOMY_BLOCK)

    def bad_endpoint(data: dict) -> None:
        data["rules.json"][ECONOMY_BLOCK]["flows"][2]["to"] = "loc_nowhere"

    def undeclared_stock(data: dict) -> None:
        # the drunk declares no grain account; the source targets it
        flow = data["rules.json"][ECONOMY_BLOCK]["flows"][2]
        flow["kind"] = "grain"
        flow["to"] = DRUNK

    def bad_level(data: dict) -> None:
        for npc in data["entities.json"]["npcs"]:
            if npc["id"] == BARKEEP:
                npc["accounts"]["coin"] = -1

    def bad_entity_kind(data: dict) -> None:
        for npc in data["entities.json"]["npcs"]:
            if npc["id"] == BARKEEP:
                npc["accounts"] = {"silver": 2}

    for mutate in (
        accounts_without_block, bad_endpoint, undeclared_stock, bad_level,
        bad_entity_kind,
    ):
        _refusal(tmp_path, f"ent_{mutate.__name__}", mutate)


def test_the_account_action_lint_refusals(tmp_path: Path) -> None:
    """The discrete arm's contract: the block only on its resolver, the
    closed verb/kind/amount shapes, the events.success RESTATEMENT of
    the verb constant (the cross-check that carries the template
    closure), and the SOLVENCY GATE — a transfer/consume without an
    actor account_at_least gate covering the amount is refused at load
    (the KI#15 family: what would crash at the commit gate mid-run
    fails here instead)."""
    def _give(data: dict) -> dict:
        return next(
            a for a in data["actions.json"]["actions"]
            if a["intent"] == "give_coin"
        )

    def wrong_resolver(data: dict) -> None:
        _give(data)["resolver"] = "wait"

    def bad_restatement(data: dict) -> None:
        _give(data)["events"]["success"] = "coin_given"

    def no_gate(data: dict) -> None:
        give = _give(data)
        give["requires"] = [give["requires"][0]]  # drops the solvency gate

    def low_gate(data: dict) -> None:
        _give(data)["requires"][1]["value"] = 1  # below the amount 2

    def dead_gate_kind(data: dict) -> None:
        action = next(
            a for a in data["actions.json"]["actions"]
            if a["intent"] == "spend_coin"
        )
        action["requires"][0]["kind"] = "silver"

    for mutate in (
        wrong_resolver, bad_restatement, no_gate, low_gate, dead_gate_kind,
    ):
        _refusal(tmp_path, f"act_{mutate.__name__}", mutate)


# -- the run laws (the crafted armed pack) --------------------------------------


def test_the_flow_events_fire_at_the_crossings(tmp_path: Path) -> None:
    """The aggregate arm end-to-end: one event per due flow per macro
    crossing, chained after the turn (the consumer-rides-the-clock
    law), the `every: 2` transfer gating alternate turns, the outcome
    carrying the flow id + kind + amount (the D-112 cardinality
    surface), actor WORLD on a source and the from-entity on a
    transfer/consume, no knowledge, no hooks, importance the pack's
    own rule."""
    log, _ = _run(
        tmp_path, economy_pack(tmp_path, "flows"), 42, WAIT_130, "flows"
    )
    events = _events(log)
    sources = _by_type(events, SOURCE_EVENT)
    transfers = _by_type(events, TRANSFER_EVENT)
    consumes = _by_type(events, CONSUME_EVENT)
    # three crossings (t=40, 80, 120): source + consume every turn,
    # the transfer only on even turns
    assert [event.t for event in sources] == [40, 80, 120]
    assert [event.t for event in consumes] == [40, 80, 120]
    assert [event.t for event in transfers] == [80]
    assert all(event.actor == "world" for event in sources)
    assert all(event.target == TAVERN for event in sources)
    assert all(event.actor == DRUNK for event in consumes)
    assert transfers[0].actor == BARKEEP and transfers[0].target == TAVERN
    assert all(event.knowledge == () and event.hooks == () for event in sources)
    assert sources[0].outcome == {
        "flow": "grain_delivery", "kind": "grain", "amount": 2,
    }
    # the chronological-chain law: each flow chains to the writer's
    # last id at its commit — the declaration order (hearth_cost
    # before grain_delivery), and the turn reachable through the
    # backward cause walk (the weather roll rides between)
    by_id = {event.id: event for event in events}
    assert sources[0].cause == consumes[0].id
    cause = sources[0].cause
    while cause is not None and by_id[cause].type != "year_turns":
        cause = by_id[cause].cause
    assert cause is not None, "the turn must be the crossing's chain root"
    assert by_id[cause].t == 40


def test_the_conservation_oracle(tmp_path: Path) -> None:
    """F1, the independent re-derivation: a test-side ledger replay
    over the raw event list — never the runtime's own fold. Every
    account delta belongs to a verb event; every verb event's deltas
    match its outcome's declared amount (source +amount on one, consume
    −amount on one, transfer −amount/+amount on the pair); every level
    stays >= 0 at every fold point; the replayed balances equal BOTH
    the runtime projection AND the initial levels plus the verb events'
    net effect (aggregate and discrete events both)."""
    pack = economy_pack(tmp_path, "oracle")
    steps = [
        {"intent": "give_coin", "target": BARKEEP},
        {"intent": "wait", "ticks": 130},
    ]
    log = _run(tmp_path, pack, 42, steps, "oracle")[0]
    events = _events(log)
    verb_types = set(VERB_EVENT_TYPES.values())
    balances = {
        entity: dict(levels)
        for entity, levels in DEFAULT_ACCOUNTS.items()
    }
    for event in events:
        account_changes = [
            change for change in event.state_changes
            if is_account_prop(change.prop)
        ]
        if not account_changes:
            continue
        assert event.type in verb_types, (
            f"{event.id}: a non-verb event touches {account_changes[0].prop}"
        )
        amount = event.outcome["amount"]
        kind = event.outcome["kind"]
        if event.type == SOURCE_EVENT:
            assert len(account_changes) == 1
            change = account_changes[0]
            assert change.to_ - change.from_ == amount
        elif event.type == CONSUME_EVENT:
            assert len(account_changes) == 1
            change = account_changes[0]
            assert change.from_ - change.to_ == amount
        else:  # transfer
            assert len(account_changes) == 2
            for change in account_changes:
                assert change.prop == account_prop(kind)
                assert abs(change.to_ - change.from_) == amount
        for change in account_changes:
            kind_name = change.prop.split(".", 1)[1]
            assert change.from_ == balances[change.entity][kind_name], (
                f"{event.id}: the replay diverges from its own ledger at "
                f"{change.entity}.{change.prop}"
            )
            balances[change.entity][kind_name] = change.to_
            assert change.to_ >= 0
    # the replay equals the runtime's own fold (two paths, one truth)
    projection = {}
    log2 = tmp_path / "oracle2.jsonl"
    sim = Simulator(pack, 42, log2, SCHEMA, commit="0000000")
    sim.open()
    try:
        sim.run_steps(steps)
        projection = {
            entity: dict(props) for entity, props in sim.projection.items()
        }
    finally:
        sim.close()
    for entity, levels in balances.items():
        for kind_name, level in levels.items():
            assert projection[entity][account_prop(kind_name)] == level, (
                f"{entity}.{kind_name}: the replay and the fold disagree"
            )
    # the conservation identity, re-derived from the OUTCOMES alone:
    # initial + net verb effect (source in, consume out, transfer
    # across) — nothing appears or disappears outside the verbs
    net = {
        entity: dict(levels) for entity, levels in DEFAULT_ACCOUNTS.items()
    }
    for event in events:
        if event.type not in verb_types:
            continue
        amount = event.outcome["amount"]
        kind = event.outcome["kind"]
        if event.type == SOURCE_EVENT:
            net[event.target][kind] += amount
        elif event.type == CONSUME_EVENT:
            net[event.actor][kind] -= amount
        else:
            net[event.actor][kind] -= amount
            net[event.target][kind] += amount
    assert net == balances


def test_the_underflow_soft_door(tmp_path: Path) -> None:
    """F2's soft arm (D3): a player-scaled spend beyond the stock dies
    at the front door — `intent_rejected` (attempts are facts), NO
    state write, the stock unchanged. pc holds 10 coin; the give (2)
    and spend (3) arms drain it to 5, then 2 — a further give (2) is
    solvent, a further spend (3) is not: the door answers with the
    rejection and the ledger never moves."""
    steps = [
        {"intent": "give_coin", "target": BARKEEP},   # 10 -> 8
        {"intent": "spend_coin"},                      # 8 -> 5
        {"intent": "give_coin", "target": BARKEEP},   # 5 -> 3
        {"intent": "spend_coin"},                      # 3 -> 0
        {"intent": "spend_coin"},                      # 0: refused softly
        {"intent": "wait", "ticks": 10},
    ]
    log, _ = _run(
        tmp_path, economy_pack(tmp_path, "soft"), 42, steps, "soft"
    )
    events = _events(log)
    rejections = [
        event for event in events if event.type == "intent_rejected"
        and event.outcome.get("action") == "spend_coin"
    ]
    assert len(rejections) == 1
    assert rejections[0].outcome["reason"] == "precondition"
    assert "account_at_least" in rejections[0].outcome["failed_test"]
    spends = [
        event for event in _by_type(events, CONSUME_EVENT)
        if event.actor == PLAYER
    ]
    assert len(spends) == 2  # the first two landed; the third never wrote
    assert _final_levels(events, PLAYER)["coin"] == 0


def test_the_underflow_loud_gate(tmp_path: Path) -> None:
    """F2's loud arm (D3): an aggregate flow beyond its stock fails
    LOUD at the `_commit` gate — the write never lands. The crafted
    consume flow (amount 5) against the drunk's 3-coin stock: the run
    raises at the first crossing, and the log holds no negative stock
    and no underflowing verb event (the committed prefix is clean —
    the append-only truth never received the disagreeing draft)."""
    economy = json.loads(json.dumps(DEFAULT_ECONOMY))
    economy["flows"][1]["amount"] = 5  # hearth_cost: 5 > the drunk's 3
    accounts = json.loads(json.dumps(DEFAULT_ACCOUNTS))
    accounts[DRUNK] = {"coin": 3}
    pack = economy_pack(
        tmp_path, "loud", economy=economy, accounts=accounts
    )
    log = tmp_path / "loud.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    with pytest.raises(ValueError, match="never goes below zero"):
        sim.run_playscript({
            "name": "loud", "seed": 42, "pack": "tavern_pack@0.1",
            "steps": WAIT_130,
        })
    sim.close()
    events = _events(log)
    # the drunk's underflowing consume never landed; every committed
    # account write is a non-negative stock
    for event in events:
        for change in event.state_changes:
            if is_account_prop(change.prop):
                assert change.to_ >= 0, event.id
    assert _by_type(events, CONSUME_EVENT) == []


def test_the_decay_separation(tmp_path: Path) -> None:
    """I5 (D2): the decay pass never touches account props — a stock
    prop is not a decay axis. The long-horizon run crosses beats (the
    decay events fire) and macro turns (the flows fire) while the
    tavern's grain — the flow-targeted stock — moves ONLY by its
    source events; the structural half pins the pass itself: no draft
    it can produce ever names an account prop."""
    log, _ = _run(
        tmp_path, economy_pack(tmp_path, "decay"), 42,
        [{"intent": "wait", "ticks": 400}], "decay",
    )
    events = _events(log)
    assert _by_type(events, "status_decayed"), "the fixture must decay"
    grain_writes = [
        (event, change)
        for event in events
        for change in event.state_changes
        if change.prop == account_prop("grain")
    ]
    # every grain write is the source flow (2/turn; the wait ends at
    # t=400 and the crossing at 400 fires before the completion, so
    # the turns 40..400 inclusive are TEN)
    assert all(event.type == SOURCE_EVENT for event, _ in grain_writes)
    assert _final_levels(events, TAVERN)["grain"] == 4 + 2 * 10
    # the structural half: the pass itself, over a projection holding
    # account props, never emits one
    projection = {
        BARKEEP: {
            "position": TAVERN, "status.fatigue": 10,
            account_prop("coin"): 5,
        },
    }
    drafts = decay_drafts(
        PACK, projection,
        {(BARKEEP, "status.fatigue"): 0}, 360,
    )
    assert drafts  # the fixture does decay...
    for draft in drafts:
        for change in draft.state_changes:
            assert not is_account_prop(change.prop)


def test_armed_determinism_and_price_never_logged(tmp_path: Path) -> None:
    """I4 + the price law's log half: same pack, same seed, same script
    → byte-identical logs (integer determinism, the T1 form over the
    armed variant); and the derived price appears NOWHERE in the log —
    no outcome carries a price key, no state change stores one (the
    amounts are spends, the prices are reads)."""
    pack = economy_pack(tmp_path, "det")
    steps = [
        {"intent": "give_coin", "target": BARKEEP},
        {"intent": "wait", "ticks": 130},
    ]
    log_a, _ = _run(tmp_path, pack, 42, steps, "det_a")
    log_b, _ = _run(tmp_path, pack, 42, steps, "det_b")
    assert log_a.read_bytes() == log_b.read_bytes()
    for event in _events(log_a):
        assert "price" not in event.outcome, event.id
        for change in event.state_changes:
            assert "price" not in change.prop


def test_the_discrete_verbs_end_to_end(tmp_path: Path) -> None:
    """The player-scaled arm's three verbs through the canon door: the
    transfer (both state changes, both knowledge records), the consume
    (one loss), the source (one gain, actor the player — the world
    mints to the actor on their action); the importance rides the
    pack's own rule; the cause chains to the writer's last id."""
    steps = [
        {"intent": "give_coin", "target": BARKEEP},
        {"intent": "spend_coin"},
        {"intent": "find_coin"},
        {"intent": "wait", "ticks": 10},
    ]
    log, _ = _run(
        tmp_path, economy_pack(tmp_path, "discrete"), 42, steps, "discrete"
    )
    events = _events(log)
    transfer = _by_type(events, TRANSFER_EVENT)[0]
    assert transfer.actor == PLAYER and transfer.target == BARKEEP
    assert transfer.state_changes == (
        StateChange(PLAYER, account_prop("coin"), 10, 8),
        StateChange(BARKEEP, account_prop("coin"), 5, 7),
    )
    knows = {record.who: record.knows for record in transfer.knowledge}
    assert knows == {
        PLAYER: "gave_coin_to_npc_barkeep_01",
        BARKEEP: "received_coin_from_pc_01",
    }
    consume = _by_type(events, CONSUME_EVENT)[0]
    assert consume.actor == PLAYER and consume.target is None
    assert consume.state_changes == (
        StateChange(PLAYER, account_prop("coin"), 8, 5),
    )
    source = _by_type(events, SOURCE_EVENT)
    discrete = [event for event in source if event.actor == PLAYER]
    assert discrete, "the find action's source event must land"
    assert discrete[0].state_changes == (
        StateChange(PLAYER, account_prop("coin"), 5, 9),
    )
    assert _final_levels(events, PLAYER)["coin"] == 9


# -- the §9 falsifier pins (the minimal test forms) -----------------------------


def test_f3_the_player_decision_effect(tmp_path: Path) -> None:
    """F3 (the priced-option question, intake-27's counting form): the
    same-seed fork where the player's spend options change the world's
    later answers — arm A spends 8 of 10 coin early; both arms then
    attempt the same 4-coin spend. A's door answer is the soft
    rejection (2 left); B's is the accept (10 held). Identical packs,
    identical seeds, measurably different worlds — the option is a
    decision, not decoration."""
    pack = economy_pack(tmp_path, "f3")
    spend4 = json.loads(json.dumps(SPEND_ACTION))
    spend4["intent"] = "spend_four"
    spend4["account"]["amount"] = 4
    spend4["requires"][0]["value"] = 4
    spend4["events"]["success"] = CONSUME_EVENT
    pack.data["actions.json"]["actions"].append(spend4)
    # arm A: drain 8 first (four gives of 2), then attempt the 4-spend
    steps_a = [
        {"intent": "give_coin", "target": BARKEEP},
        {"intent": "give_coin", "target": BARKEEP},
        {"intent": "give_coin", "target": BARKEEP},
        {"intent": "give_coin", "target": BARKEEP},
        {"intent": "spend_four"},
        {"intent": "wait", "ticks": 10},
    ]
    # arm B: the 4-spend first
    steps_b = [
        {"intent": "spend_four"},
        {"intent": "wait", "ticks": 10},
    ]
    log_a, _ = _run(tmp_path, pack, 42, steps_a, "f3_a")
    log_b, _ = _run(tmp_path, pack, 42, steps_b, "f3_b")
    events_a, events_b = _events(log_a), _events(log_b)
    rejected_a = [
        event for event in events_a
        if event.type == "intent_rejected"
        and event.outcome.get("action") == "spend_four"
    ]
    rejected_b = [
        event for event in events_b
        if event.type == "intent_rejected"
        and event.outcome.get("action") == "spend_four"
    ]
    assert len(rejected_a) == 1 and len(rejected_b) == 0
    assert _final_levels(events_a, PLAYER)["coin"] == 2
    assert _final_levels(events_b, PLAYER)["coin"] == 6


def test_f4_the_one_knob_ablation(tmp_path: Path) -> None:
    """F4 (the one-knob ablation): ONE declared flow knob perturbed
    (the source's amount 2 → 3) — the economy's surface moves (the
    grain levels +1 per turn) and NO unrelated event is perturbed:
    with the verb events stripped, the two same-seed logs are
    byte-identical (the flows draw nothing, so the streams never see
    the knob — the fingerprint's own law)."""
    economy_b = json.loads(json.dumps(DEFAULT_ECONOMY))
    economy_b["flows"][2]["amount"] = 3  # grain_delivery: 2 -> 3
    pack_a = economy_pack(tmp_path, "f4a")
    pack_b = economy_pack(tmp_path, "f4b", economy=economy_b)
    log_a, _ = _run(tmp_path, pack_a, 42, WAIT_130, "f4_a")
    log_b, _ = _run(tmp_path, pack_b, 42, WAIT_130, "f4_b")
    events_a, events_b = _events(log_a), _events(log_b)
    assert _final_levels(events_a, TAVERN)["grain"] == 4 + 2 * 3
    assert _final_levels(events_b, TAVERN)["grain"] == 4 + 3 * 3
    # the unrelated runs: strip the verb events, compare the rest
    verb_types = set(VERB_EVENT_TYPES.values())
    rest_a = [
        event_to_mapping(event) for event in events_a
        if event.type not in verb_types
    ]
    rest_b = [
        event_to_mapping(event) for event in events_b
        if event.type not in verb_types
    ]
    assert rest_a == rest_b


# -- helpers --------------------------------------------------------------------


def _final_levels(events: list[Any], entity: str) -> dict[str, int]:
    """The entity's account levels as folded from the event list (the
    test's own replay — never the runtime's projection)."""
    levels: dict[str, int] = dict(DEFAULT_ACCOUNTS[entity])
    for event in events:
        for change in event.state_changes:
            if change.entity == entity and is_account_prop(change.prop):
                levels[change.prop.split(".", 1)[1]] = change.to_
    return levels
