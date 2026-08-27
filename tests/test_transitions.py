"""Unit tests for the generic transition engine (core/transitions.py):
ignition plans (alarm with occupants, none without), the spot-prefix
discipline, spread rolls against a twin bank, follow-up idempotence, and
the re-ignition no-op. The e2e fire chain lives in test_actions.py.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.fold import initial_projection
from core.pack import load_pack
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
    import pytest

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
    import pytest

    with pytest.raises(ValueError, match="unknown follow-up kind"):
        follow_up_draft(PACK, projection(), 5, "fire", "loc_tavern",
                        "flood", "ev_0000")
