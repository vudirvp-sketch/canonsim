"""account-ceiling — the `account_at_most` precondition (substrate-1 B, iter-410).

The wall, as measured by the maintenance unit (iter-405): the closed
precondition set carried FLOORS only (`account_at_least` — a spend's
solvency), so a ladder's HEAD had no instrument. The guild's stair wears
+2 a year up to a cap of 8, and the restoration rides wear-clearing
alone: "the head stays the keeper's door" — authorial discipline, never a
gate. The same shape blocks every declared bounded window (a vessel that
must be empty before it is filled, a store that must be below a ceiling
to accept a delivery).

This witness measures the new instrument: the ceiling twin of the floor
gate, the same account prop compared DOWNWARD, with the floor family's
whole contract (declared kind, non-negative value, the noun/holder naming
law) and the OCC attribution twin.

The claim packet (`docs/TEST_PLAN.md` §9):

- Claim: `account_at_most` joins the closed set as the floor's exact
  twin — it passes at or under the declared value, fails above it and on
  a missing stock, refuses its dead shapes at load, and attributes its
  read pair to the OCC index like every account gate, while the canonical
  corpus stays byte-identical (zero pack byte).
- Lens(es): the evaluator unit (the door's own verdict at a known
  projection) + the boundary lens (the load-time refusals).
- Prism: the committed province pack (real entities/stocks) for the
  evaluator; a crafted twin (the same pack, ONE gate prepended to
  `render_toll`) for the door + the lint shapes.
- Oracle: `first_failing`'s own answer; the log's `intent_rejected`
  records; `PackError` messages.
- Falsifier: a ceiling that passes above its value, a silent pass on an
  undeclared stock, a load that accepts an unglued shape, a missing OCC
  pair, or any movement of the committed corpus.
- Epistemic class: FACT at the measured band.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.fold import initial_projection
from core.intent import (
    ACCOUNT_CEILING_TEST,
    OCC_READ_PAIRS,
    PRECONDITION_TESTS,
    IntentData,
    first_failing,
    precondition_read_pairs,
)
from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack
from core.packlint.helpers import PackError

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"
KETTA = "npc_weirkeeper_01"
MALBY = "loc_malby"
DOOR = "render_toll"
REJECTION = "intent_rejected"


def _intent(kind: str, target: str | None = None) -> IntentData:
    return IntentData(
        id="intent_0000", kind=kind, actor=KETTA, target=target, fields={}
    )


def _twin(tmp_path: Path, name: str, gate: dict[str, Any]) -> Path:
    """The committed province pack with ONE ceiling gate PREPENDED to the
    `render_toll` door's requires — zero bytes of the real pack change
    (the twin is a copy, the door's own shape untouched otherwise)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
    for action in actions["actions"]:
        if action["intent"] == DOOR:
            action["requires"] = [gate, *action["requires"]]
            break
    else:  # pragma: no cover — the committed pack always carries the door
        raise AssertionError(f"{DOOR} not declared")
    (target / "actions.json").write_text(
        json.dumps(actions, indent=2), encoding="utf-8"
    )
    return target


def _rejections(pack_dir: Path, tmp_path: Path, name: str) -> list:
    pack = load_pack(pack_dir)
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": 42, "pack": "province_pack@0.1",
        "steps": [{"actor": KETTA, "intent": DOOR, "target": MALBY}],
    })
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events


# -- (1) the closed set and its attribution twin --------------------------------


def test_the_closed_set_gained_the_ceiling_and_its_read_pair() -> None:
    """The vocabulary law (INTENT_SCHEMA §3, the OCC completeness law):
    the name is in the closed test set, it has an attribution handler,
    and the handler declares EXACTLY the floor's pair — one stock, one
    prop, one declaration."""
    assert ACCOUNT_CEILING_TEST == "account_at_most"
    assert ACCOUNT_CEILING_TEST in PRECONDITION_TESTS
    assert ACCOUNT_CEILING_TEST in OCC_READ_PAIRS

    pack = load_pack(PACK_DIR)
    probe = _intent(DOOR, MALBY)
    floor = [{"noun": "actor", "test": "account_at_least",
              "kind": "coin", "value": 2}]
    ceiling = [{"noun": "actor", "test": "account_at_most",
                "kind": "coin", "value": 2}]
    assert precondition_read_pairs(pack, probe, floor) == precondition_read_pairs(
        pack, probe, ceiling
    )
    assert precondition_read_pairs(pack, probe, ceiling) == frozenset(
        {(KETTA, "account.coin")}
    )


# -- (2) the evaluator compares downward ----------------------------------------


def test_the_evaluator_compares_downward_and_fails_a_missing_stock() -> None:
    """The door's verdict at a known projection: coin 3 passes a ceiling
    of 3 and of 4, fails a ceiling of 2 (the exact boundary — `at_most`
    is inclusive, the floor's own symmetry); the holder form reads the
    same prop; an entity that declares nothing of the kind FAILS (a
    silent pass would let a dead gate arm an action)."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    assert projection[KETTA]["account.coin"] == 2
    projection[KETTA]["account.coin"] = 3
    probe = _intent(DOOR, MALBY)

    def gate(value: int, **extra: Any) -> list[dict[str, Any]]:
        return [{"noun": "actor", "test": ACCOUNT_CEILING_TEST,
                 "kind": "coin", "value": value, **extra}]

    assert first_failing(pack, projection, probe, gate(3)) is None
    assert first_failing(pack, projection, probe, gate(4)) is None
    assert first_failing(pack, projection, probe, gate(2)) == (
        "actor.account_at_most"
    )
    # the holder form names the entity directly (the floor's own law)
    assert first_failing(
        pack, projection, probe,
        [{"holder": KETTA, "test": ACCOUNT_CEILING_TEST,
          "kind": "coin", "value": 3}],
    ) is None
    # a missing stock is the honest False, never a silent pass
    assert first_failing(
        pack, projection, probe,
        [{"holder": "loc_malby", "test": ACCOUNT_CEILING_TEST,
          "kind": "step", "value": 99}],
    ) == "loc_malby.account_at_most"


# -- (3) the door + the log -----------------------------------------------------


def test_the_door_refuses_over_the_ceiling_softly(tmp_path: Path) -> None:
    """At coin 2 a ceiling of 1 refuses the walk BEFORE the door's own
    floor (the gate is prepended): the attempt is a fact in the log
    (`intent_rejected`, `failed_test` naming the ceiling) and the account
    never moves — no `account_transferred` event, the stock untouched."""
    pack_dir = _twin(tmp_path, "over", {
        "noun": "actor", "test": ACCOUNT_CEILING_TEST,
        "kind": "coin", "value": 1,
    })
    events = _rejections(pack_dir, tmp_path, "over")
    rejected = [e for e in events if e.type == REJECTION]
    assert [e.outcome["failed_test"] for e in rejected] == ["actor.account_at_most"]
    assert not [e for e in events if e.type == "account_transferred"]
    assert all(
        ch.prop != "account.coin"
        for e in events for ch in e.state_changes if ch.entity == KETTA
    )


def test_under_the_ceiling_the_door_moves_on(tmp_path: Path) -> None:
    """The control arm: the same door with a ceiling of 2 PASSES (coin
    2 ≤ 2) and the walk stops at ONE OF ITS OWN later gates — the
    rejection, if any, never names the ceiling. The gate is a filter,
    not a second door."""
    pack_dir = _twin(tmp_path, "under", {
        "noun": "actor", "test": ACCOUNT_CEILING_TEST,
        "kind": "coin", "value": 2,
    })
    events = _rejections(pack_dir, tmp_path, "under")
    rejected = [e for e in events if e.type == REJECTION]
    assert rejected, "the walk must stop somewhere (the door is walked)"
    assert all(
        e.outcome["failed_test"] != "actor.account_at_most" for e in rejected
    )


# -- (4) the load-time contract -------------------------------------------------


def test_the_lint_refuses_the_dead_shapes(tmp_path: Path) -> None:
    """The pack-facing contract, refused at load (never a KeyError
    mid-run, never a silently always-False gate): an undeclared kind, a
    negative value, both naming forms, an undeclared holder, and a
    holder that declares no stock of the kind."""
    cases: list[tuple[dict[str, Any], str]] = [
        ({"noun": "actor", "test": ACCOUNT_CEILING_TEST,
          "kind": "mooncoin", "value": 1},
         "requires 'kind' naming a declared economy.accounts kind"),
        ({"noun": "actor", "test": ACCOUNT_CEILING_TEST,
          "kind": "coin", "value": -1},
         "value must be a non-negative integer"),
        ({"noun": "actor", "holder": KETTA, "test": ACCOUNT_CEILING_TEST,
          "kind": "coin", "value": 1},
         "carries both 'noun' and 'holder'"),
        ({"holder": "loc_nowhere", "test": ACCOUNT_CEILING_TEST,
          "kind": "coin", "value": 1},
         "holder 'loc_nowhere' is not a declared entity"),
        ({"holder": KETTA, "test": ACCOUNT_CEILING_TEST,
          "kind": "paper", "value": 1},
         "declares no account of kind 'paper'"),
    ]
    for position, (gate, message) in enumerate(cases):
        pack_dir = _twin(tmp_path, f"dead{position}", gate)
        with pytest.raises(PackError, match=message.replace("(", r"\(")):
            load_pack(pack_dir)
