"""floworder — the crossing's declaration order is a LOAD-TIME law
(substrate-1 A's guard, iter-413).

`substrate-1` A made the crossing a SEQUENCE: `flow_drafts` reads each
level at its own yield, so a drain declared AFTER its mint sees the minted
stock, and a drain declared BEFORE it sees the pre-mint one. That is the
right engine law, and it created a new authoring hazard: a misordered
graph is not a wrong number but a crash at the first crossing — the
`_commit` floor refuses a negative stock LOUD (`would write -3`), and the
author learns about it by running the world, not by loading the pack.

This witness measures the guard: `core/packlint/economy.py::_flow_order`
simulates the first `max(every)` crossings from the pack's seed levels in
declaration order and refuses the load at the first negative level. The
check is exact for each flow's first due turn and conservative afterwards
(the `_commit` floor stays the runtime net).

The claim packet (`docs/TEST_PLAN.md` §9):

- Claim: a pack whose declared flow order drains a stock before the flow
  that feeds it fails to LOAD (one PackError naming the flow, the stock
  and the turn), while an order that mints first loads; a drain that is
  not due until a later crossing is judged on ITS first due turn, never
  on a crossing it does not ride.
- Lens(es): the boundary unit (load-time refusal vs the run that used to
  crash); the declaration-order unit (which crossing the graph is judged
  on).
- Prism: copies of the committed province pack with the larder pair
  reordered; the committed pack itself as the control.
- Oracle: `PackError` at `load_pack`, the message naming flow + stock.
- Falsifier: a misordered pack that loads; a correctly ordered pack that
  is refused; a not-yet-due drain judged early.
- Epistemic class: FACT at the measured band.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.pack import load_pack
from core.packlint.helpers import PackError

REPO = Path(__file__).resolve().parents[1]
PACK_DIR = REPO / "content" / "province_pack"
KETTA = "npc_weirkeeper_01"

GARDEN = {
    "id": "the_garden_yields", "verb": "source", "kind": "stores",
    "to": KETTA, "amount": 3, "every": 1, "capacity": 4,
}
HEARTH = {
    "id": "the_hearth_eats", "verb": "consume", "kind": "stores",
    "from": KETTA, "amount": 2, "every": 1,
}


def _twin(tmp_path: Path, name: str, flows: list[dict[str, Any]]) -> Path:
    """The committed province pack with the economy flow list REPLACED by
    the graph under test (the other blocks untouched — the load must fail
    in THIS lint, not in a neighbour)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    rules["economy"]["flows"] = flows
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    glosses = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    glosses.pop("flow_glosses", None)  # the replaced graph's ids are the law
    (target / "templates.json").write_text(
        json.dumps(glosses, indent=2), encoding="utf-8"
    )
    return target


# -- (1) the committed graph loads ---------------------------------------------


def test_the_committed_graph_loads() -> None:
    """The control: the larder's own order (mint, then drain) is what the
    committed pack declares — the guard never fires on it."""
    pack = load_pack(PACK_DIR)
    ids = [flow["id"] for flow in pack.rules["economy"]["flows"]]
    assert ids.index("the_garden_yields") < ids.index("the_hearth_eats")


# -- (2) the misordered graph is refused AT LOAD --------------------------------


def test_a_drain_before_its_mint_is_a_load_time_refusal(tmp_path: Path) -> None:
    """The hazard substrate-1 A created, caught where the author is: the
    hearth declared before the garden on a larder that opens empty drives
    `account.stores` to −2 at the first crossing. The load refuses, naming
    the flow, the stock and the turn — never a run that dies at `_commit`."""
    twin = _twin(tmp_path, "misordered", [HEARTH, GARDEN])
    with pytest.raises(PackError, match="declaration order drives"):
        load_pack(twin)
    with pytest.raises(PackError, match="the_hearth_eats"):
        load_pack(twin)
    with pytest.raises(PackError, match=r"npc_weirkeeper_01\.account\.stores"):
        load_pack(twin)


# -- (3) judged on the flow's FIRST due turn ------------------------------------


def test_a_drain_not_due_at_the_first_crossing_is_judged_on_its_own_turn(
    tmp_path: Path,
) -> None:
    """The `every` divisor decides WHICH crossing a flow rides: a drain
    on `every: 2` does not fire at turn 1. The guard must judge it at
    turn 2 (its first due turn) — where the pair is declared correctly
    (mint first) it loads; where it is declared before the mint it is
    refused, with the turn named."""
    slower_garden = {**GARDEN, "every": 2}
    slower_hearth = {**HEARTH, "every": 2}
    ok = _twin(tmp_path, "ok_pair", [slower_garden, slower_hearth])
    pack = load_pack(ok)
    assert any(
        flow["id"] == "the_hearth_eats"
        for flow in pack.rules["economy"]["flows"]
    )
    wrong = _twin(tmp_path, "wrong_pair", [slower_hearth, slower_garden])
    with pytest.raises(PackError, match="crossing turn 2"):
        load_pack(wrong)
