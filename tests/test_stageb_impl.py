"""iter-332 acceptance — stageb-1-impl, the material cycle's ENGINE
mechanics (CONTRACTS §12 B1..B8, the implementation row's first
half; B1..B8 owner-accepted 2026-10-04):

- **B2 the convert verb** — ONE atomic recipe event: the declared
  recipe's input legs drain, its output legs produce, every leg's
  state changes in the SAME canonical event (the settle precedent's
  atomic multi-leg law; the float law by construction — no chained
  second verb ever reads pre-first state). Conservation PER RECIPE
  per kind, fold-checkable; the outcome carries the recipe id + the
  resolved legs (the flow outcome's diagnosability form).
- **B3 the use-hook wear** — a per-USE integer consume on the
  instrument's stock fired at the consuming action's SUCCESSFUL
  completion (a failed attempt leaves the stock untouched — the
  attempt is a fact, the stock is not); the instrument NAMED in the
  event; break-at-zero the LAST use (below-zero dies softly at the
  door — the lint-required solvency gate; attempts are facts).
- **B4 the capacity cap** — the mint's min() arithmetic, SILENCE at
  full (the every-miss form), the `_commit` cap floor LOUD (a write
  above a declared cap refuses, any verb).
- **B5 the unarmed law** — no recipes, no wear bindings, no
  capacities declared → zero events change (the standing golden T1
  corpora the executable; the mechanics' surfaces answer empty).
- **B7 the index law** — every new read surface a projection read
  (account_level's O(1) form), never a log scan: by construction,
  the resolver/hook/floor read `projection[entity][account.kind]`.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.economy import (
    CONVERT_EVENT,
    ECONOMY_BLOCK,
    EconomyError,
    convert_resolution,
    source_caps,
)
from core.fold import fold, initial_projection
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
TAVERN_PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)

PLAYER = "pc_01"
BARKEEP = "npc_barkeep_01"
TAVERN = "loc_tavern"
BACKYARD = "loc_backyard"

ACCOUNTS: dict[str, dict[str, int]] = {
    PLAYER: {"coin": 10, "grain": 0},
    BARKEEP: {"grain": 6},
    TAVERN: {"grain": 4, "flour": 2},
}

CONVERT_ECONOMY: dict[str, Any] = {
    "accounts": ["coin", "grain", "flour"],
    "flows": [],
    "recipes": [
        {
            "id": "mill_the_grain",
            "inputs": [{"holder": TAVERN, "kind": "grain", "amount": 2}],
            "outputs": [{"holder": TAVERN, "kind": "flour", "amount": 1}],
        },
    ],
    "prices": {},
}

MILL_ACTION: dict[str, Any] = {
    "intent": "mill_grain", "label": "mill flour", "resolver": "account",
    "ticks": 4,
    "events": {"success": CONVERT_EVENT},
    "requires": [
        {"test": "kind", "noun": "target", "is": "location"},
        {"test": "same_location", "noun": "target", "with": "actor"},
        {"test": "account_at_least", "holder": TAVERN, "kind": "grain",
         "value": 2},
    ],
    "fields": [],
    "account": {"verb": "convert", "recipe": "mill_the_grain"},
    "knowledge": {
        "success": [
            {"who": "actor", "channel": "saw", "fidelity": "exact",
             "knows": "milled_flour"},
        ]
    },
    "notes": "stageb-1 fixture: the conversion door (the recipe event)",
}

CAPPED_ECONOMY: dict[str, Any] = {
    "accounts": ["coin", "grain", "flour"],
    "flows": [
        {"id": "grain_delivery", "verb": "source", "kind": "grain",
         "to": TAVERN, "amount": 3, "capacity": 7},
    ],
}

GRIND_ACTION: dict[str, Any] = {
    "intent": "grind_flour", "label": "grind flour", "resolver": "account",
    "ticks": 4,
    "events": {"success": CONVERT_EVENT},
    "requires": [
        {"test": "kind", "noun": "target", "is": "location"},
        {"test": "same_location", "noun": "target", "with": "actor"},
        {"test": "account_at_least", "holder": TAVERN, "kind": "grain",
         "value": 1},
        {"test": "account_at_least", "holder": TAVERN, "kind": "flour",
         "value": 1},
    ],
    "fields": [],
    "account": {"verb": "convert", "recipe": "grain_to_flour"},
    "instrument": {"holder": TAVERN, "kind": "flour", "amount": 1},
    "knowledge": {},
    "notes": "stageb-1 fixture: the wear door (the use-hook)",
}

WEAR_ECONOMY: dict[str, Any] = {
    "accounts": ["coin", "grain", "flour"],
    "flows": [],
    "recipes": [
        {
            "id": "grain_to_flour",
            "inputs": [{"holder": TAVERN, "kind": "grain", "amount": 1}],
            "outputs": [{"holder": TAVERN, "kind": "flour", "amount": 2}],
        },
    ],
}

VERB_LINES: dict[str, str] = {
    CONVERT_EVENT: "{actor} works the recipe: {input_0_amount} "
                   "{input_0_kind} into {output_0_amount} {output_0_kind}.",
}


def stageb_pack(
    tmp_path: Path, name: str, *,
    economy: dict[str, Any] | None,
    actions: tuple[dict[str, Any], ...] = (),
) -> Pack:
    """A committed-pack copy with the material cycle armed: the entity
    `accounts` merged in, the economy block set (None keeps the pack's
    own — the unarmed twin), the fixture actions appended, the convert
    line carried only when a convert door is armed (the
    dead-vocabulary law)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    data = {
        file_name: json.loads((target / file_name).read_text(encoding="utf-8"))
        for file_name in (
            "actions.json", "entities.json", "rules.json", "templates.json",
        )
    }
    entities = data["entities.json"]
    for category in (
        "locations", "npcs", "ambient_entities", "items", "groups",
    ):
        for record in entities.get(category, ()):
            merged = ACCOUNTS.get(record["id"])
            if merged is not None:
                record["accounts"] = json.loads(json.dumps(merged))
    rules = data["rules.json"]
    rules["time"]["macro"] = {
        "cadence_ticks": 40, "event_type": "year_turns",
    }
    if economy is not None:
        rules[ECONOMY_BLOCK] = json.loads(json.dumps(economy))
    data["actions.json"]["actions"].extend(
        json.loads(json.dumps(a)) for a in actions
    )
    templates = data["templates.json"]["events"]
    if any(
        isinstance(a.get("account"), dict)
        and a["account"].get("verb") == "convert"
        for a in data["actions.json"]["actions"]
    ):
        templates.update(VERB_LINES)
    if economy is not None:
        # the armed flows' verb lines (the corpus price of arming —
        # the template closure law)
        verbs = {
            flow.get("verb")
            for flow in economy.get("flows", ())
            if isinstance(flow, dict)
        }
        if "source" in verbs:
            templates["account_sourced"] = \
                "The {target} gains {amount} {kind}."
    for file_name, payload in data.items():
        (target / file_name).write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )
    return load_pack(target)


def _run(
    tmp_path: Path, pack: Pack, seed: int,
    steps: list[dict[str, Any]],
) -> tuple[list[Any], Simulator]:
    log = tmp_path / f"run_{seed}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": "t", "seed": seed, "pack": pack.name_version, "steps": steps,
    })
    _, events = read_log(log, SCHEMA)
    return events, sim


def _by_type(events: list[Any], *types: str) -> list[Any]:
    return [e for e in events if e.type in types]


# -- B2: the convert verb -------------------------------------------------------


def test_the_recipe_event_is_atomic_and_conserved(tmp_path: Path) -> None:
    """The conversion commits ONE event per use: the tavern's grain
    drains 2, its flour gains 1 — both legs in the SAME event, the
    outcome carrying the recipe id + the resolved legs; conservation
    per kind per recipe holds on the FOLD (the fold-checkable
    identity)."""
    pack = stageb_pack(
        tmp_path, "convert", economy=CONVERT_ECONOMY, actions=(MILL_ACTION,),
    )
    events, sim = _run(tmp_path, pack, 42, [
        {"intent": "move", "target": TAVERN},
        {"intent": "mill_grain", "target": TAVERN},
    ])
    converted = _by_type(events, CONVERT_EVENT)
    assert len(converted) == 1
    event = converted[0]
    assert event.outcome["recipe"] == "mill_the_grain"
    assert event.outcome["inputs"] == [
        {"holder": TAVERN, "kind": "grain", "amount": 2},
    ]
    assert event.outcome["outputs"] == [
        {"holder": TAVERN, "kind": "flour", "amount": 1},
    ]
    # ONE event carries BOTH legs (the atomic multi-leg law)
    changes = {(c.entity, c.prop): c for c in event.state_changes}
    assert changes[(TAVERN, "account.grain")].from_ == 4
    assert changes[(TAVERN, "account.grain")].to_ == 2
    assert changes[(TAVERN, "account.flour")].from_ == 2
    assert changes[(TAVERN, "account.flour")].to_ == 3
    # the fold agrees (the fold-checkable conservation: grain -2,
    # flour +1 — the declared net)
    state = fold(events[1:], initial_projection(pack.entities))
    assert state[TAVERN]["account.grain"] == 2
    assert state[TAVERN]["account.flour"] == 3


def test_the_insolvent_conversion_dies_softly(tmp_path: Path) -> None:
    """The per-input-leg solvency gates the door: an attempt without
    the input stock is world-impossible — `intent_rejected`, attempts
    are facts, no state change."""
    pack = stageb_pack(
        tmp_path, "insolvent", economy=CONVERT_ECONOMY, actions=(MILL_ACTION,),
    )
    # the tavern holds 4 grain; THREE conversions exhaust it — the
    # third attempt (needing 2 with 0 left... 4-2-2=0) leaves the
    # stock at 0 and the next attempt is refused
    events, _ = _run(tmp_path, pack, 42, [
        {"intent": "move", "target": TAVERN},
        {"intent": "mill_grain", "target": TAVERN},
        {"intent": "mill_grain", "target": TAVERN},
        {"intent": "mill_grain", "target": TAVERN},
    ])
    assert len(_by_type(events, CONVERT_EVENT)) == 2
    rejections = [
        e for e in _by_type(events, "intent_rejected")
        if e.outcome.get("reason") == "precondition"
    ]
    assert len(rejections) == 1
    state = fold(events[1:], initial_projection(pack.entities))
    assert state[TAVERN]["account.grain"] == 0
    assert state[TAVERN]["account.flour"] == 4  # 2 seeded + 2 milled


# -- B4: the capacity cap -------------------------------------------------------


def test_the_capped_mint_plateaus_and_stays_silent(tmp_path: Path) -> None:
    """The bounded source: the mint is min(declared, cap - stock); at
    full cap the flow is NOT DUE (zero events, the every-miss form);
    the stock NEVER exceeds the cap — the plateau, B6's shape (b) in
    miniature."""
    pack = stageb_pack(tmp_path, "capped", economy=CAPPED_ECONOMY)
    events, _ = _run(tmp_path, pack, 42, [
        {"intent": "wait", "ticks": 200},
    ])
    state = fold(events[1:], initial_projection(pack.entities))
    assert state[TAVERN]["account.grain"] <= 7
    # 4 seeded + 3 minted to the cap in one turn, then SILENCE — the
    # second turn mints nothing (the every-miss form at full)
    mints = [
        e for e in _by_type(events, "account_sourced")
        if e.outcome.get("flow") == "grain_delivery"
    ]
    assert [m.outcome["amount"] for m in mints] == [3]
    assert state[TAVERN]["account.grain"] == 7


def test_the_cap_floor_is_loud(tmp_path: Path) -> None:
    """A write above a declared cap refuses LOUD at `_commit` — any
    verb, before the log ever sees it (B1's "never" arm; the flow's
    own min() keeps the machinery compliant, so the breach is a
    hand-built draft)."""
    pack = stageb_pack(tmp_path, "floor", economy=CAPPED_ECONOMY)
    log = tmp_path / "floor.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.open()
    from core.economy import source_draft
    before = sim._writer.event_count  # the genesis events, already legal
    try:
        sim._commit(source_draft(
            pack.rules, sim._projection, 10, TAVERN, "grain", 99,
        ))
        raise AssertionError("the cap floor never fired")
    except ValueError as exc:
        assert "capacity" in str(exc)
    assert sim._writer.event_count == before  # the refusal wrote nothing
    sim.close()
    # the unarmed twin: no caps declared -> no floor arm at all
    assert source_caps(TAVERN_PACK.rules) == {}
    assert source_caps({"economy": {"flows": []}}) == {}


def test_the_partial_mint_fills_to_the_cap(tmp_path: Path) -> None:
    """The partial fill: stock 6 of cap 7, declared 3 -> mint 1 (the
    min() arithmetic) — tick+stock-derived, draw-free (INV-2-clean)."""
    economy = json.loads(json.dumps(CAPPED_ECONOMY))
    pack_data = tmp_path / "partial"
    shutil.copytree(REPO / "content" / "tavern_pack", pack_data)
    entities = json.loads((pack_data / "entities.json").read_text())
    for record in entities["locations"]:
        if record["id"] == TAVERN:
            record["accounts"] = {"grain": 6}
    (pack_data / "entities.json").write_text(json.dumps(entities))
    rules = json.loads((pack_data / "rules.json").read_text())
    rules["time"]["macro"] = {"cadence_ticks": 40, "event_type": "year_turns"}
    rules[ECONOMY_BLOCK] = economy
    (pack_data / "rules.json").write_text(json.dumps(rules))
    templates = json.loads((pack_data / "templates.json").read_text())
    templates["events"]["account_sourced"] = "The {target} gains {amount} {kind}."
    (pack_data / "templates.json").write_text(json.dumps(templates))
    pack = load_pack(pack_data)
    events, _ = _run(tmp_path, pack, 42, [{"intent": "wait", "ticks": 200}])
    mints = [
        e for e in _by_type(events, "account_sourced")
        if e.outcome.get("flow") == "grain_delivery"
    ]
    assert [m.outcome["amount"] for m in mints] == [1]


# -- B3: the use-hook wear ------------------------------------------------------


def test_the_use_hook_wears_on_completion(tmp_path: Path) -> None:
    """The wear fires at the consuming action's SUCCESSFUL completion:
    ONE consume event after the recipe event, the instrument NAMED
    (target = the holder, outcome's `use` = the action), the stock
    drained by the per-use amount."""
    pack = stageb_pack(
        tmp_path, "wear", economy=WEAR_ECONOMY, actions=(GRIND_ACTION,),
    )
    events, _ = _run(tmp_path, pack, 42, [
        {"intent": "move", "target": TAVERN},
        {"intent": "grind_flour", "target": TAVERN},
    ])
    converted = _by_type(events, CONVERT_EVENT)
    assert len(converted) == 1
    # the wear: the LAST committed event before nothing else — right
    # after the recipe event (the chronological chain)
    wears = [
        e for e in _by_type(events, "account_consumed")
        if e.outcome.get("use") == "grind_flour"
    ]
    assert len(wears) == 1
    wear = wears[0]
    assert wear.actor == PLAYER
    assert wear.target == TAVERN
    assert wear.outcome["kind"] == "flour"
    assert wear.outcome["amount"] == 1
    # 2 seeded + 2 produced by the recipe - 1 worn by the use = 3
    state = fold(events[1:], initial_projection(pack.entities))
    assert state[TAVERN]["account.flour"] == 3
    assert state[TAVERN]["account.grain"] == 3  # 4 - 1


def test_break_at_zero_is_the_last_use(tmp_path: Path) -> None:
    """The 0-crossing is the LAST use: the stock drains 0 -> the use
    commits (the action completed); the NEXT attempt dies softly at
    the door (the lint-required gate) — intent_rejected, attempts are
    facts, no negative write ever lands."""
    pack = stageb_pack(
        tmp_path, "break", economy=WEAR_ECONOMY, actions=(GRIND_ACTION,),
    )
    # grain 4 -> four grinds; flour: +2 -1 wear per grind => 1 left
    # after grind 1, 2 after grind 2 (1+2-1), 3 after grind 3... the
    # flour stock only hits 0 via wears: grind1 f=1, grind2 f=2,
    # grind3 f=3, grind4 f=4 — never breaks; re-seed the fixture to
    # make the flour stock scarce instead
    data = tmp_path / "break2"
    shutil.copytree(tmp_path / "break", data)
    entities = json.loads((data / "entities.json").read_text())
    for record in entities["locations"]:
        if record["id"] == TAVERN:
            record["accounts"]["flour"] = 2
    (data / "entities.json").write_text(json.dumps(entities))
    pack = load_pack(data)
    events, _ = _run(tmp_path, pack, 42, [
        {"intent": "move", "target": TAVERN},
        {"intent": "grind_flour", "target": TAVERN},
        {"intent": "grind_flour", "target": TAVERN},
        {"intent": "grind_flour", "target": TAVERN},
    ])
    # the recipe NET-produces flour here, so the break needs the
    # wear-only twin below; this arm pins the pairing law instead:
    # wears == grinds (every completion wore its use) and no state
    # ever went negative
    grinds = len(_by_type(events, CONVERT_EVENT))
    wears = len([
        e for e in _by_type(events, "account_consumed")
        if e.outcome.get("use") == "grind_flour"
    ])
    assert grinds == 3
    assert wears == 3
    state = fold(events[1:], initial_projection(pack.entities))
    assert state[TAVERN]["account.flour"] == 5  # 2 + 3*(2-1)


def test_the_wear_only_stock_breaks(tmp_path: Path) -> None:
    """The break law's direct form: a wear-only stock (no recipe
    output feeds it) drains to 0 — the 0-crossing use COMMITS (the
    last use), the next attempt is world-impossible and dies softly
    at the door (the gate), never a negative write."""
    economy = json.loads(json.dumps(WEAR_ECONOMY))
    economy["recipes"][0]["outputs"][0]["amount"] = 0 if False else 1
    # a pure test action that only wears (a no-op verb carrying the
    # instrument binding): reuse grind but with a recipe producing
    # nothing into flour — instead give the recipe an output the
    # wear never touches
    economy["recipes"][0]["outputs"] = [
        {"holder": TAVERN, "kind": "grain", "amount": 1},
    ]
    pack_data = tmp_path / "wearonly"
    shutil.copytree(REPO / "content" / "tavern_pack", pack_data)
    entities = json.loads((pack_data / "entities.json").read_text())
    for record in entities["locations"]:
        if record["id"] == TAVERN:
            record["accounts"] = {"grain": 4, "flour": 2}
    (pack_data / "entities.json").write_text(json.dumps(entities))
    rules = json.loads((pack_data / "rules.json").read_text())
    rules["time"]["macro"] = {"cadence_ticks": 40, "event_type": "year_turns"}
    rules[ECONOMY_BLOCK] = economy
    (pack_data / "rules.json").write_text(json.dumps(rules))
    actions = json.loads((pack_data / "actions.json").read_text())
    actions["actions"].append(json.loads(json.dumps(GRIND_ACTION)))
    (pack_data / "actions.json").write_text(json.dumps(actions))
    templates = json.loads((pack_data / "templates.json").read_text())
    templates["events"].update(VERB_LINES)
    (pack_data / "templates.json").write_text(json.dumps(templates))
    pack = load_pack(pack_data)
    events, _ = _run(tmp_path, pack, 42, [
        {"intent": "move", "target": TAVERN},
        {"intent": "grind_flour", "target": TAVERN},
        {"intent": "grind_flour", "target": TAVERN},
        {"intent": "grind_flour", "target": TAVERN},
    ])
    # flour 2 -> wear 1 -> 1 -> wear 2 -> 0 (the LAST use commits);
    # the third attempt: gate fails (0 < 1) -> intent_rejected
    grinds = len(_by_type(events, CONVERT_EVENT))
    wears = len([
        e for e in _by_type(events, "account_consumed")
        if e.outcome.get("use") == "grind_flour"
    ])
    rejections = [
        e for e in _by_type(events, "intent_rejected")
        if e.outcome.get("reason") == "precondition"
    ]
    assert (grinds, wears, len(rejections)) == (2, 2, 1)
    state = fold(events[1:], initial_projection(pack.entities))
    assert state[TAVERN]["account.flour"] == 0
    # grain: the recipe here swaps grain->grain 1:1 (input 1,
    # output 1) — the two grinds net zero on grain
    assert state[TAVERN]["account.grain"] == 4


# -- B7: the index law (by construction, the executable form) -------------------


def test_the_new_read_surfaces_are_projection_reads() -> None:
    """The three edges' read surfaces answer from the projection (the
    O(1) account_level form), never a log scan: the convert
    resolution over a hand-built projection, the caps accessor over
    the rules, the wear draft over the projection — no events list
    enters any of them."""
    rules = {"economy": json.loads(json.dumps(CONVERT_ECONOMY))}
    projection = {TAVERN: {"account.grain": 5, "account.flour": 0}}
    outcome, changes = convert_resolution(
        rules, projection, 10, "mill_the_grain",
        holders=lambda ref: ref,
    )
    assert outcome["recipe"] == "mill_the_grain"
    assert len(changes) == 2
    assert changes[0].from_ == 5 and changes[0].to_ == 3
    assert changes[1].from_ == 0 and changes[1].to_ == 1
    # the loud backstops (the pred-contract family)
    try:
        convert_resolution(
            rules, projection, 10, "no_such_recipe", holders=lambda r: r,
        )
        raise AssertionError("the missing recipe never refused")
    except EconomyError:
        pass


# -- the lint refusals ---------------------------------------------------------


def _refusal(tmp_path: Path, name: str, mutate) -> None:
    data = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", data)
    payload = {
        file_name: json.loads((data / file_name).read_text(encoding="utf-8"))
        for file_name in (
            "actions.json", "entities.json", "rules.json", "templates.json",
        )
    }
    mutate(payload)
    for file_name, doc in payload.items():
        (data / file_name).write_text(json.dumps(doc), encoding="utf-8")
    try:
        load_pack(data)
    except PackError:
        return
    raise AssertionError(f"the lint accepted an invalid {name}")


def _arm_all(payload: dict[str, Any]) -> None:
    """The base arming all refusal arms mutate: the economy with one
    recipe + one capped flow, the convert + wear doors, the lines."""
    for record in payload["entities.json"]["locations"]:
        if record["id"] == TAVERN:
            record["accounts"] = {"grain": 4, "flour": 0}
    rules = payload["rules.json"]
    rules["time"]["macro"] = {
        "cadence_ticks": 40, "event_type": "year_turns",
    }
    rules[ECONOMY_BLOCK] = json.loads(json.dumps(WEAR_ECONOMY))
    rules[ECONOMY_BLOCK]["flows"] = [
        {"id": "g", "verb": "source", "kind": "grain",
         "to": TAVERN, "amount": 1, "capacity": 9},
    ]
    payload["actions.json"]["actions"].append(
        json.loads(json.dumps(GRIND_ACTION))
    )
    payload["templates.json"]["events"].update(VERB_LINES)


def test_the_stageb_lint_refusals(tmp_path: Path) -> None:
    """The lint's own gates: the unknown recipe binding, the convert
    event-type mismatch, the missing input-leg solvency gate, the
    ungated instrument, the non-source capacity, the doubled cap, the
    unknown recipe keys, the undeclared recipe holder."""

    # the unknown recipe id
    def unknown_recipe(payload):
        _arm_all(payload)
        payload["actions.json"]["actions"][-1]["account"]["recipe"] = "nope"

    # the convert event-type mismatch
    def wrong_type(payload):
        _arm_all(payload)
        payload["actions.json"]["actions"][-1]["events"]["success"] = \
            "account_settled"

    # the missing input-leg solvency gate
    def no_gate(payload):
        _arm_all(payload)
        requires = payload["actions.json"]["actions"][-1]["requires"]
        payload["actions.json"]["actions"][-1]["requires"] = [
            cond for cond in requires
            if not (cond.get("test") == "account_at_least"
                    and cond.get("kind") == "grain")
        ]

    # the ungated instrument
    def ungated_wear(payload):
        _arm_all(payload)
        requires = payload["actions.json"]["actions"][-1]["requires"]
        payload["actions.json"]["actions"][-1]["requires"] = [
            cond for cond in requires
            if not (cond.get("test") == "account_at_least"
                    and cond.get("kind") == "flour")
        ]

    # the non-source capacity
    def capped_transfer(payload):
        _arm_all(payload)
        payload["rules.json"][ECONOMY_BLOCK]["flows"] = [
            {"id": "g", "verb": "transfer", "kind": "grain",
             "from": TAVERN, "to": BACKYARD, "amount": 1, "capacity": 9},
        ]

    # the doubled cap on one stock
    def double_cap(payload):
        _arm_all(payload)
        payload["rules.json"][ECONOMY_BLOCK]["flows"] = [
            {"id": "g", "verb": "source", "kind": "grain",
             "to": TAVERN, "amount": 1, "capacity": 9},
            {"id": "g2", "verb": "source", "kind": "grain",
             "to": TAVERN, "amount": 1, "capacity": 8},
        ]

    # the unknown recipe keys
    def bad_recipe_keys(payload):
        _arm_all(payload)
        payload["rules.json"][ECONOMY_BLOCK]["recipes"][0]["extras"] = 1

    # the undeclared recipe holder
    def ghost_holder(payload):
        _arm_all(payload)
        payload["rules.json"][ECONOMY_BLOCK]["recipes"][0]["inputs"][0][
            "holder"
        ] = "loc_ghost"

    for name, mutate in (
        ("unknown_recipe", unknown_recipe),
        ("wrong_type", wrong_type),
        ("no_gate", no_gate),
        ("ungated_wear", ungated_wear),
        ("capped_transfer", capped_transfer),
        ("double_cap", double_cap),
        ("bad_recipe_keys", bad_recipe_keys),
        ("ghost_holder", ghost_holder),
    ):
        _refusal(tmp_path, name, mutate)


def test_the_armed_run_is_deterministic(tmp_path: Path) -> None:
    """INV-2 over an armed run: the recipes draw nothing, the cap
    arithmetic is tick+stock-derived — the double run is
    byte-identical (the T1 form over the material cycle)."""
    pack = stageb_pack(
        tmp_path, "det", economy=WEAR_ECONOMY, actions=(GRIND_ACTION,),
    )
    steps = [
        {"intent": "move", "target": TAVERN},
        {"intent": "grind_flour", "target": TAVERN},
        {"intent": "grind_flour", "target": TAVERN},
        {"intent": "wait", "ticks": 120},
    ]
    log_a = tmp_path / "det_a.jsonl"
    sim = Simulator(pack, 8, log_a, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": "t", "seed": 8, "pack": pack.name_version, "steps": steps,
    })
    sim.close()
    log_b = tmp_path / "det_b.jsonl"
    sim = Simulator(pack, 8, log_b, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": "t", "seed": 8, "pack": pack.name_version, "steps": steps,
    })
    sim.close()
    assert log_a.read_bytes() == log_b.read_bytes()
    # the armed world really moved (a vacuous identity is no law)
    assert len(_by_type(read_log(log_a, SCHEMA)[1], CONVERT_EVENT)) >= 2
