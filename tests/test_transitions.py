"""Unit tests for the generic transition engine (core/transitions.py):
ignition plans (alarm with occupants, none without), the spot-prefix
discipline, spread rolls against a twin bank, follow-up idempotence, and
the re-ignition no-op. The e2e fire chain lives in test_actions.py.
iter-20 adds the universality probes: a synthetic layer with a wholly
different vocabulary (spot_state / follow-up kinds / flags / halt) driven
by the same engine — the D-057 proof that a second layer is pack data,
never a code change.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.fold import initial_projection
from core.pack import Pack, PackError, load_pack
from core.rng import RngBank
from core.transitions import Ignition, follow_up_draft, ignite, spread_tick

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")


def projection() -> dict[str, dict[str, Any]]:
    return initial_projection(PACK.entities)


def test_ignite_without_other_occupants_has_no_alarm() -> None:
    state = projection()
    state["pc_01"]["position"] = "loc_backyard"
    plan = ignite(PACK, state, 10, Ignition("fire", "loc_backyard", "woodpile"),
                  "pc_01")
    assert [d.type for d in plan.drafts] == ["fire_started"]
    assert plan.seed_pass is True
    assert [spec.kind for spec in plan.follow_ups] == ["smoke", "burnout"]
    assert plan.follow_ups[0].at_tick == 20  # smoke after 10 ticks
    assert plan.follow_ups[1].at_tick == 130  # burnout after 120
    # nobody else in the backyard: no knowledge records born
    assert plan.drafts[0].knowledge == ()


def test_ignite_with_occupants_plans_the_alarm() -> None:
    state = projection()
    plan = ignite(PACK, state, 10, Ignition("fire", "loc_tavern", "bar"), "pc_01")
    assert [d.type for d in plan.drafts] == ["fire_started", "alarm_raised"]
    alarm = plan.drafts[1]
    assert alarm.state_changes[0].prop == "status.fear"


def test_reigniting_a_burning_spot_is_a_noop_plan() -> None:
    state = projection()
    state["loc_tavern"]["fire.bar"] = "burning"
    plan = ignite(PACK, state, 10, Ignition("fire", "loc_tavern", "bar"), "pc_01")
    assert plan.drafts == () and plan.seed_pass is False


def test_igniting_an_unknown_spot_is_loud() -> None:
    state = projection()

    with pytest.raises(ValueError, match="not a .* spot"):
        ignite(PACK, state, 10, Ignition("fire", "loc_tavern", "roof"), "pc_01")


def test_spread_tick_rolls_each_unburning_spot() -> None:
    state = projection()
    state["loc_tavern"]["fire.bar"] = "burning"
    bank = RngBank(42)
    twin = RngBank(42)
    result = spread_tick(PACK, state, bank, 11, "fire", {"loc_tavern": "ev_0000"})
    # one roll per unburning spot (tables, back_wall — pack order), a draft
    # only for the ignitions
    assert bank.count("substantive") == 2
    assert result.continue_pass is True
    with twin.assure("substantive"):
        rolls = (twin.random(), twin.random())
    ignited = [
        spot
        for spot, roll in zip(("tables", "back_wall"), rolls, strict=True)
        if roll <= 0.15
    ]
    assert [d.outcome["spot"] for d in result.drafts] == ignited
    assert all(d.cause == "ev_0000" for d in result.drafts)


def test_spread_tick_stops_when_nothing_can_spread() -> None:
    state = projection()
    for spot in ("bar", "tables", "back_wall"):
        state["loc_tavern"][f"fire.{spot}"] = "burning"
    result = spread_tick(PACK, state, RngBank(1), 11, "fire",
                         {"loc_tavern": "ev_0000"})
    assert result.drafts == () and result.continue_pass is False


def test_spread_tick_skips_destroyed_locations() -> None:
    state = projection()
    state["loc_tavern"]["fire.bar"] = "burning"
    state["loc_tavern"]["destroyed"] = True
    result = spread_tick(PACK, state, RngBank(1), 11, "fire",
                         {"loc_tavern": "ev_0000"})
    assert result.drafts == () and result.continue_pass is False


def test_follow_up_drafts_are_idempotent_on_state() -> None:
    state = projection()
    state["loc_tavern"]["fire.bar"] = "burning"
    smoke = follow_up_draft(PACK, state, 20, "fire", "loc_tavern", "smoke",
                            "ev_0000")
    assert smoke is not None and smoke.type == "smoke_rising"
    assert smoke.state_changes[0].prop == "smoke"
    # a second smoke follow-up (e.g. a second ignition of the same location)
    # says nothing: no duplicate event, no duplicate chronicle line (KI#13)
    state["loc_tavern"]["smoke"] = True
    smoke_again = follow_up_draft(PACK, state, 30, "fire", "loc_tavern", "smoke",
                                  "ev_0000")
    assert smoke_again is None
    # a second burnout likewise stays silent — the first told the story
    state["loc_tavern"]["destroyed"] = True
    assert follow_up_draft(PACK, state, 140, "fire", "loc_tavern", "burnout",
                           "ev_0000") is None
    # smoke after destruction: nothing left to say
    assert follow_up_draft(PACK, state, 130, "fire", "loc_tavern", "smoke",
                           "ev_0000") is None


def test_follow_up_unknown_kind_is_loud() -> None:
    with pytest.raises(ValueError, match="unknown follow-up kind"):
        follow_up_draft(PACK, projection(), 5, "fire", "loc_tavern",
                        "flood", "ev_0000")


# -- the iter-20 universality probes (D-057) ---------------------------------


def _layered_pack() -> Pack:
    """An in-memory pack with a second, synthetic transition layer whose
    vocabulary shares nothing with fire: spot_state 'infested', halt flag
    'condemned', follow-up kinds 'stench'/'collapse', flags 'foul'/
    'condemned'. Built Pack-direct (lint-free) — these tests pin the
    ENGINE, the lint clauses below pin the loader."""
    data = json.loads(json.dumps(dict(PACK.data)))
    rules = data["rules.json"]
    rules["transitions"]["rot"] = {
        "system": "fire",
        "spot_field": "rot_spots",
        "spot_state": "infested",
        "halt_flag": "condemned",
        "ignition": {"chance_on_drop_break": 0.0},
        "spread": {"chance_per_tick": 0.5, "within": "location"},
        "follow_ups": [
            {"kind": "stench", "after_ticks": 5, "flag": "foul",
             "value": True, "irreversible": False,
             "blocked_by": ["condemned"]},
            {"kind": "collapse", "after_ticks": 50, "flag": "condemned",
             "value": True, "irreversible": True, "blocked_by": []},
        ],
        "alarm": {"when_occupants_present": False, "fear_spike": 0},
        "events": {
            "started": "rot_started", "spread": "rot_spread",
            "stench": "stench_rising", "alarm": "rot_alarm",
            "collapse": "building_collapsed",
        },
        "knowledge": {
            "started": {"who": "same_location", "channel": "saw",
                        "fidelity": "exact", "knows": "rot_in_{location}"},
            "spread": {"who": "same_location", "channel": "saw",
                       "fidelity": "exact",
                       "knows": "rot_spreading_in_{location}"},
            "stench": {"who": "same_location", "channel": "saw",
                       "fidelity": "exact", "knows": "stench_in_{location}"},
            "alarm": {"who": "same_location", "channel": "heard",
                      "fidelity": "exact", "knows": "rot_alarm_in_{location}"},
            "alarm_adjacent": {"who": "adjacent_locations", "channel": "heard",
                               "fidelity": "vague",
                               "knows": "shouting_near_{location}"},
            "collapse": {"who": "same_location", "channel": "saw",
                         "fidelity": "exact", "knows": "{location}_collapsed"},
        },
    }
    for location in data["entities.json"]["locations"]:
        if location["id"] == "loc_backyard":
            location["rot_spots"] = ["crate", "compost"]
    return Pack(data=data)


def test_synthetic_layer_ignites_with_pack_declared_vocabulary() -> None:
    """The engine writes the layer's OWN spot_state and seeds the layer's
    OWN follow-up kinds at the pack-declared ticks — no kind or state
    string exists in core (D-057)."""
    pack = _layered_pack()
    state = initial_projection(pack.entities)
    state["pc_01"]["position"] = "loc_backyard"
    plan = ignite(pack, state, 10, Ignition("rot", "loc_backyard", "crate"),
                  "pc_01")
    assert [draft.type for draft in plan.drafts] == ["rot_started"]
    change = plan.drafts[0].state_changes[0]
    assert change.prop == "rot.crate" and change.to_ == "infested"
    assert [spec.kind for spec in plan.follow_ups] == ["stench", "collapse"]
    assert [spec.at_tick for spec in plan.follow_ups] == [15, 60]


def test_synthetic_layer_follow_ups_are_pack_data() -> None:
    """Flags, values, irreversibility, and preemption are layer data:
    stench sets 'foul' reversibly and is pre-empted by 'condemned';
    collapse sets 'condemned' irreversibly and is idempotent."""
    pack = _layered_pack()
    state = initial_projection(pack.entities)
    state["loc_backyard"]["rot.crate"] = "infested"
    stench = follow_up_draft(pack, state, 15, "rot", "loc_backyard", "stench",
                             "ev_0000")
    assert stench is not None and stench.type == "stench_rising"
    assert stench.state_changes[0].prop == "foul"
    assert stench.state_changes[0].irreversible is False
    state["loc_backyard"]["foul"] = True
    assert follow_up_draft(pack, state, 16, "rot", "loc_backyard", "stench",
                           "ev_0000") is None
    collapse = follow_up_draft(pack, state, 60, "rot", "loc_backyard",
                               "collapse", "ev_0000")
    assert collapse is not None and collapse.type == "building_collapsed"
    assert collapse.state_changes[0].prop == "condemned"
    assert collapse.state_changes[0].irreversible is True
    # the commit applies the draft (drafts never mutate the projection);
    # stench after the collapse stays silent; a second collapse likewise
    state["loc_backyard"]["condemned"] = True
    assert follow_up_draft(pack, state, 61, "rot", "loc_backyard", "stench",
                           "ev_0000") is None
    assert follow_up_draft(pack, state, 61, "rot", "loc_backyard", "collapse",
                           "ev_0000") is None


def test_synthetic_layer_spread_halts_at_the_pack_flag() -> None:
    """Spread rolls against the layer's OWN state vocabulary and halts at
    the layer's OWN halt flag — 'destroyed' means nothing to this layer."""
    pack = _layered_pack()
    state = initial_projection(pack.entities)
    state["loc_backyard"]["rot.crate"] = "infested"
    result = spread_tick(pack, state, RngBank(3), 11, "rot",
                         {"loc_backyard": "ev_0000"})
    assert result.continue_pass is True  # compost still uninfested
    state["loc_backyard"]["condemned"] = True
    result = spread_tick(pack, state, RngBank(3), 12, "rot",
                         {"loc_backyard": "ev_0000"})
    assert result.drafts == () and result.continue_pass is False


def _broken_pack(tmp_path: Path, mutate: Any) -> Path:
    target = tmp_path / "broken_pack"
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    mutate(target)
    return target


def test_pack_lint_catches_follow_up_without_event(tmp_path: Path) -> None:
    """Every follow-up kind joins a declared event AND knowledge entry
    (D-057) — a dangling kind fails at load time."""

    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        fire = rules["transitions"]["fire"]
        fire["follow_ups"][0]["kind"] = "haze"
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="no 'haze' event declared"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_missing_spot_state(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        del rules["transitions"]["fire"]["spot_state"]
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="spot_state must be a non-empty string"):
        load_pack(_broken_pack(tmp_path, mutate))


def test_pack_lint_catches_duplicate_follow_up_kind(tmp_path: Path) -> None:
    def mutate(target: Path) -> None:
        rules = json.loads((target / "rules.json").read_text())
        fire = rules["transitions"]["fire"]
        fire["follow_ups"][1]["kind"] = "smoke"
        (target / "rules.json").write_text(json.dumps(rules))

    with pytest.raises(PackError, match="kind must be a unique non-empty string"):
        load_pack(_broken_pack(tmp_path, mutate))
