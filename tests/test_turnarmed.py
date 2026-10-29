"""iter-429 acceptance — the FIRST armed turn in a committed pack (D-281).

The claim these laws pin: `content/province_pack` now DECLARES a role turn,
authored on the role (never on a person), and its carrier is an authored
profile — so the row survives every born-origin ablation (the reason the
born-carrier form was refused by measurement, iter-428 §2.2).

- without the residue the row is silent (no event, the world unchanged);
- below the bar it stays silent (`dread` 49 of 100);
- AT the bar it is pending — and the draft it makes is exactly ONE canon
  event: `role_turned`, the smelter as its actor, the `archetype` prop
  rewritten `the_smelter_master -> the_road_wanderer`, from the pack's own
  template vocabulary;
- the bar is 50 and the barn sighting mints `dread` 60, so the row is
  reachable from the pack's own echo table, not from a hand-placed number
  (the vocabulary check the moving lint gap names: `docs/TASKS.md`).

Rides the COMMITTED pack and never writes: the witness is the parse and the
draft, no playthrough (the corpus price of the arming is measured in
`docs/iterations/iter-429-armed-turn-report.md` §4).
"""

from __future__ import annotations

import json
from pathlib import Path

from core.echo import EchoScore
from core.fold import initial_projection
from core.pack import load_pack
from core.turning import turning_drafts, turning_pending, turning_specs

REPO = Path(__file__).resolve().parents[1]
PACK_DIR = REPO / "content" / "province_pack"
SMELTER = "npc_smelter_01"
FROM_ROLE = "the_smelter_master"
TO_ROLE = "the_road_wanderer"
EVENT = "role_turned"
BAR = 50


def _pack():
    return load_pack(PACK_DIR)


def _echo(score: int) -> list[EchoScore]:
    return [EchoScore(who=SMELTER, axis="dread", score=score)]


def test_the_pack_declares_the_row_on_the_role_not_on_a_person() -> None:
    """The row names two archetypes and one closed condition; no npc id
    appears in it (one row per ROLE — a person is armed by carrying it)."""
    pack = _pack()
    psyche = pack.rules["psyche"]
    rows = psyche["turnings"]
    assert len(rows) == 1
    row = rows[0]
    assert (row["from"], row["to"]) == (FROM_ROLE, TO_ROLE)
    assert row["when"] == [
        {"noun": "actor", "test": "echo_at_least", "axis": "dread", "value": BAR}
    ]
    assert psyche["turning_event"] == EVENT
    assert EVENT in pack.templates["events"]


def test_the_bar_is_reachable_from_the_packs_own_echo_table() -> None:
    """A condition the world can never satisfy is dead data. The row reads
    `dread`; the pack's own residue registry mints `dread` 60 on the barn
    sighting and 25 on the tin, so the bar 50 sits INSIDE the declared
    scale and a real sighting crosses it."""
    pack = _pack()
    tokens = pack.rules["echo"]["tokens"]
    dreads = {
        token: row["axes"]["dread"]
        for token, row in tokens.items()
        if isinstance(row, dict) and "dread" in row.get("axes", {})
    }
    assert max(dreads.values()) >= BAR, dreads


def test_the_probe_id_names_the_declared_pair() -> None:
    """turnids-1 (iter-437): the committed row's probe id is the (carrier,
    declaration) triple — the pack's own names, never an ordinal, so a row
    inserted earlier can never rename this probe (the `probeids-1` law)."""
    pack = _pack()
    specs = turning_specs(pack)
    assert len(specs) == 1
    spec = specs[0]
    assert (spec.npc, spec.from_role, spec.to_role) == (
        SMELTER, FROM_ROLE, TO_ROLE,
    )
    assert spec.probe.id == f"turn_{SMELTER}_{FROM_ROLE}_{TO_ROLE}"


def test_silent_without_the_residue_and_pending_at_the_bar() -> None:
    pack = _pack()
    projection = initial_projection(pack.entities)
    assert turning_pending(pack, projection) is False
    assert turning_pending(pack, projection, echoes=_echo(BAR - 1)) is False
    assert turning_pending(pack, projection, echoes=_echo(BAR)) is True


def test_the_turn_is_one_canon_event_rewriting_the_role_prop() -> None:
    pack = _pack()
    projection = initial_projection(pack.entities)
    drafts = turning_drafts(
        pack,
        projection,
        echoes=_echo(60),
        cause="ev_0001",
        tick=1200,
    )
    assert len(drafts) == 1
    draft = drafts[0]
    payload = json.loads(
        json.dumps(
            {
                "type": draft.type,
                "actor": draft.actor,
                "target": draft.target,
                "outcome": draft.outcome,
            }
        )
    )
    assert payload == {
        "type": EVENT,
        "actor": SMELTER,
        "target": None,
        "outcome": {"from": FROM_ROLE, "to": TO_ROLE},
    }
    assert len(draft.state_changes) == 1
    change = draft.state_changes[0]
    assert (change.entity, change.prop, change.to_) == (
        SMELTER,
        "archetype",
        TO_ROLE,
    )
