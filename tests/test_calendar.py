"""iter-136 acceptance — world-2 L2 slice 4, the calendar (maclock-1's
middle granularities, L4's layered clocks grown to three tiers; TASKS
world-2's wave plan D-153, phases.md §6 — "market days, the fair, the
river's seasonal rise — cadence pack-declared; the seasons ride
weather-1's satisfied gate").

The laws pinned here:

- **The scheduler cadence rule** (INV-2-clean, the macro clock's own
  family): crossings are the positive multiples of the entry's
  `every_ticks` — pure tick arithmetic, never entropy; the loop fires
  them in the crossing discipline (tick order; at a co-occurring tick
  the COARSEST clock first — the year before the season, the season
  before the finer cadence, then the rotation, then the beat; within
  the calendar the order is every_ticks DESC then the entry id —
  deterministic, pinned).
- **The sub-year law**: `every_ticks` is strictly below the macro
  cadence — the year clock owns the year turns (a second year-scale
  clock is a duplicate declaration, never a calendar); the pairing
  law: a calendar without the macro clock is dead data.
- **The cycle law** (the seasons' form): the phases rotate by
  ARITHMETIC (`cycle[k % len]` — the snowmelt comes when it comes,
  never a draw); the run OPENS at cycle[0] (the pack's opening
  season, the weather `initial`'s own law) and the k-th crossing
  carries the k-th phase — the run never sees cycle[0]'s event until
  the wrap; each phase's turn is ITS OWN event type (the tale line,
  never a shared template keyed on a raw id).
- **The turn event's shape**: actor `world`, cause = the previous
  canon id (the chronological-chain law), the outcome carrying the
  entry id, the derived day (the macro `year`'s twin, L3) and the
  phase; no knowledge, no state_changes, no hooks (the director
  boundary is the consumers' rows, never the clock's).
- **The weather's seasonal ride** (the D-030 asymmetric data): the
  chain's rolls move from the macro year's crossings to the RIDE
  entry's crossings — a reference, never a declaration ("one clock,
  one cadence"); the per-phase weight overrides bias the roll (the
  rise's storm bias), the phases absent from the map keep the base
  weights (the long light's slow calm).
- **The unarmed law** (the 68a pattern): an absent `time.calendar`
  block is zero crossings, zero events, the committed bytes untouched
  — the A/B arms differ in the block's PRESENCE alone, the
  substantive fingerprint EQUAL (the calendar path draws nothing), the
  stream delta the calendar events alone (the iter-83 both-arms
  measurement form).
- **The session law + the resume door**: the crossing cursors
  persist across `run_steps` calls; a resumed run is byte-identical
  to the uninterrupted one across a split that straddles crossings
  (the D-139 law — the cursors ride the cursor envelope).
- **The corpus price**: the committed province declares the calendar
  at the real cadences (the market every 14400, the fair 43200, the
  seasons 129600) — beyond every day-scale corpus script's horizon
  by construction (the weather-1 arming's own law), the golden byte
  untouched.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.calendar import (
    CalendarError,
    calendar_order,
    calendar_phase,
    calendar_turn_draft,
    next_calendar_tick,
)
from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack
from core.weather import seasonal_ride

REPO = Path(__file__).resolve().parents[1]
PROVINCE = load_pack(REPO / "content" / "province_pack")
TAVERN_DIR = REPO / "content" / "tavern_pack"
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

#: the crafted arming's own vocabulary (the pack's choice, never an
#: engine word — INV-3): a two-phase season cycle (the run opens at
#: `spring`, the crossings alternate) and a plain weekly cadence
#: half the seasons' period (the co-occurrence probe: every second
#: week crossing shares its tick with a season turn).
CYCLE = [
    {"phase": "spring", "event_type": "spring_turns"},
    {"phase": "storm_season", "event_type": "stormy_turns"},
]
WEEK_EVENT = "week_turns"
SEASON_EVERY = 8
WEEK_EVERY = 4
YEAR_TICKS = 24  # 3 seasons, 6 weeks — the sub-year law's ceiling

#: the seasonal weather layer over the crafted cycle: spring forces
#: rain (the smoke erosion fires at the spring crossings), the storm
#: season forces storm (the murmur hook seeds) — 100% maps make the
#: bias seed-independent, so the pinned sequence is law, not luck.
FORCED = {
    "spring": {
        "clear": {"rain": 10},
        "overcast": {"rain": 10},
        "rain": {"rain": 10},
        "storm": {"rain": 10},
    },
    "storm_season": {
        "clear": {"storm": 10},
        "overcast": {"storm": 10},
        "rain": {"storm": 10},
        "storm": {"storm": 10},
    },
}


def crafted_pack(
    tmp_path: Path,
    name: str,
    calendar: Any,
    *,
    macro: Any = None,
    seasonal: Any = None,
    seasonal_absent: bool = True,
) -> Pack:
    """A committed tavern copy with the calendar family armed at test
    scale (the intake-19 probe pattern): the macro block shrunk to
    YEAR_TICKS (a dict override, the string "remove" drops the block —
    the pairing-law arm), the calendar set (or REMOVED when None — the
    unarmed twin), the seasonal weather layer set (or left absent —
    the default-ride arm rolls at the macro crossings). The crafted
    template lines join the closure; the weather block rides the
    tavern's own (the pairing holds either way)."""
    target = tmp_path / name
    shutil.copytree(TAVERN_DIR, target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if macro == "remove":
        rules["time"].pop("macro", None)
        rules.pop("weather", None)  # the pairing law: no clock, no family
    else:
        rules["time"]["macro"] = macro or {
            "cadence_ticks": YEAR_TICKS, "event_type": "year_turns",
        }
    if calendar is None:
        rules["time"].pop("calendar", None)
    else:
        rules["time"]["calendar"] = calendar
    if seasonal is not None:
        rules["weather"]["seasonal"] = seasonal
    elif "weather" in rules and seasonal_absent:
        rules["weather"].pop("seasonal", None)
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    if calendar is not None:
        templates["events"][WEEK_EVENT] = "A week turns."
        for pair in CYCLE:
            templates["events"][pair["event_type"]] = (
                f"The season turns to {pair['phase']}."
            )
    (target / "templates.json").write_text(
        json.dumps(templates, indent=2), encoding="utf-8"
    )
    return load_pack(target)


def crafted_calendar() -> dict[str, Any]:
    return {
        "seasons": {"every_ticks": SEASON_EVERY, "cycle": CYCLE},
        "weeks": {"every_ticks": WEEK_EVERY, "event_type": WEEK_EVENT},
    }


def _run(
    tmp_path: Path, pack: Pack, seed: int, steps: list[dict[str, Any]], name: str,
) -> tuple[Path, Any]:
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    result = sim.run_playscript(
        {"name": name, "seed": seed, "pack": "tavern_pack@0.1", "steps": steps}
    )
    sim.close()
    return log, result


def _events(records: list, *types: str) -> list:
    return [e for e in records if e.type in types]


WAIT_100: list[dict[str, Any]] = [{"intent": "wait", "ticks": 100}]


# -- the cadence arithmetic (unit) ---------------------------------------------


def test_crossings_are_the_positive_multiples_per_entry() -> None:
    """The scheduler cadence rule, per entry: the smallest multiple
    strictly after `after` — pure integer arithmetic (INV-2-clean),
    the macro clock's own family law."""
    entry = {"every_ticks": SEASON_EVERY}
    assert next_calendar_tick(entry, 0) == SEASON_EVERY
    assert next_calendar_tick(entry, 7) == 8
    assert next_calendar_tick(entry, 8) == 16
    assert next_calendar_tick(entry, 99) == 104
    assert next_calendar_tick({"every_ticks": 1}, 0) == 1


def test_a_broken_period_fails_loud_never_silently() -> None:
    """The raw-read backstop (the pred-contract family, D-111): a
    hand-built config with a zero/negative/non-integer period raises
    CalendarError naming the law — an infinite crossing loop is never
    a clock, and a KeyError must never leak."""
    for bad in (0, -1, "8", 1.5, True, None):
        with pytest.raises(CalendarError, match="every_ticks"):
            next_calendar_tick({"every_ticks": bad}, 0)


def test_the_order_is_coarsest_first_then_id() -> None:
    """The deterministic crossing order: every_ticks DESCENDING (the
    coarsest calendar clock first — the family's own discipline), then
    the entry id (the pinned tiebreak) — a stable total order so a
    co-occurring tick's commits are byte-identical across runs."""
    rules = {"time": {"calendar": {
        "weeks": {"every_ticks": 4},
        "seasons": {"every_ticks": 8},
        "tides": {"every_ticks": 8},
    }}}
    assert calendar_order(rules) == ("seasons", "tides", "weeks")


# -- the phase + the turn draft (unit) -----------------------------------------


def test_the_phase_is_pure_arithmetic_and_the_run_opens_at_cycle_zero() -> None:
    """The cycle law: `cycle[k % len]` — the run OPENS at cycle[0]
    (the pack's opening season, the weather `initial`'s own law), the
    k-th crossing carries the k-th phase; the thaw's event is the
    wrap's own (the province's cycle below), never the run's first
    season turn. Derived, never stored (L3)."""
    rules = {"time": {"calendar": crafted_calendar()}}
    assert calendar_phase(rules, "seasons", 0) == "spring"  # the opening phase
    assert calendar_phase(rules, "seasons", 7) == "spring"  # still cycle[0]
    assert calendar_phase(rules, "seasons", 8) == "storm_season"  # k=1
    assert calendar_phase(rules, "seasons", 15) == "storm_season"
    assert calendar_phase(rules, "seasons", 16) == "spring"  # k=2 wraps
    assert calendar_phase(rules, "weeks", 8) is None  # a plain entry


def test_the_draft_carries_the_entry_the_day_and_the_phase() -> None:
    """The turn event's shape: the outcome carries the entry id, the
    derived day (the macro `year`'s twin, L3) and the phase; a CYCLED
    entry's event type is the CURRENT phase's own (each season's turn
    its own tale line); actor `world`, no knowledge, no
    state_changes, no hooks — the clock family's own event."""
    rules = {"time": {
        "ticks_per_day": 1440, "calendar": crafted_calendar(),
    }, "importance": {"score": {
        "entities_touched_at_least_2": 1, "irreversible_state_change": 2,
        "per_far_hook": 1, "story_critical_event": 2,
    }, "story_critical_events": [], "thresholds": {
        "medium": 2, "high": 4,
    }}}
    draft = calendar_turn_draft(rules, "seasons", 8)
    assert draft.type == CYCLE[1]["event_type"]  # k=1 -> stormy_turns
    assert draft.outcome == {
        "calendar": "seasons", "day": 0, "phase": "storm_season",
    }
    assert draft.actor == "world"
    assert draft.knowledge == () and draft.state_changes == ()
    assert draft.hooks == ()
    week = calendar_turn_draft(rules, "weeks", 12)
    assert week.type == WEEK_EVENT
    assert week.outcome == {"calendar": "weeks", "day": 0}
    with pytest.raises(CalendarError, match="no such entry"):
        calendar_turn_draft(rules, "quarters", 8)


def test_the_province_cycle_is_the_vales_own_four_seasons() -> None:
    """The committed content: three entries at the real cadences —
    the decan market (14400), the month's fair (43200), the 90-day
    seasons over the 360-day year; the cycle [thaw, high_water,
    long_light, first_frost] — the run OPENS in the thaw, the RISE is
    the first crossing (day 90), the wrap's thaw turns with the year
    (day 360 — the year opens with the thaw)."""
    calendar = PROVINCE.rules["time"]["calendar"]
    assert calendar["market_days"] == {
        "every_ticks": 14400, "event_type": "market_opens",
        "notes": calendar["market_days"]["notes"],
    }
    assert calendar["fairs"]["every_ticks"] == 43200
    assert calendar["fairs"]["event_type"] == "fair_opens"
    seasons = calendar["seasons"]
    assert seasons["every_ticks"] == 129600  # 90 days x 1440
    assert [pair["phase"] for pair in seasons["cycle"]] == [
        "thaw", "high_water", "long_light", "first_frost",
    ]
    rules = PROVINCE.rules
    assert calendar_phase(rules, "seasons", 0) == "thaw"  # the opening season
    assert calendar_phase(rules, "seasons", 129600) == "high_water"  # day 90
    assert calendar_phase(rules, "seasons", 259200) == "long_light"
    assert calendar_phase(rules, "seasons", 388800) == "first_frost"
    assert calendar_phase(rules, "seasons", 518400) == "thaw"  # the wrap


# -- the lint family (load-time refusals) ---------------------------------------


def test_the_lint_refuses_the_broken_armings(tmp_path: Path) -> None:
    """The load-time contract (the crafted-directory form, the macro
    family's own precedent): the pairing law (a calendar without the
    macro clock is dead data — the weather block drops with it), the
    sub-year law (a second year-scale clock is a duplicate
    declaration), the identity law (a type colliding with the macro
    turn's, the weather change's, or another calendar entry's), the
    both-or-neither refusal and the cycle law — every one a loud
    PackError at load, never a mid-run surprise."""
    cases: list[tuple[Any, Any, Any, str]] = [
        # the pairing law: the calendar hangs from the head block
        (crafted_calendar(), "remove", None, "pairing law"),
        # the sub-year law: every_ticks strictly below the macro cadence
        ({"weeks": {"every_ticks": 40, "event_type": WEEK_EVENT}},
         None, None, "sub-year law"),
        ({"weeks": {"every_ticks": 518400, "event_type": WEEK_EVENT}},
         None, None, "sub-year law"),
        # the identity law: the macro turn's own type
        ({"weeks": {"every_ticks": 4, "event_type": "year_turns"}},
         None, None, "macro turn's own"),
        # the identity law: the weather change's own type
        ({"weeks": {"every_ticks": 4, "event_type": "weather_turns"}},
         None, None, "weather change's own"),
        # the identity law: one entry, one event type
        ({
            "a": {"every_ticks": 4, "event_type": WEEK_EVENT},
            "b": {"every_ticks": 8, "event_type": WEEK_EVENT},
         }, None, None, "another calendar emission"),
        # the both-or-neither refusal
        ({"both": {
            "every_ticks": 4, "event_type": WEEK_EVENT, "cycle": CYCLE,
         }}, None, None, "exactly one of event_type or cycle"),
        ({"neither": {"every_ticks": 4}}, None, None,
         "exactly one of event_type or cycle"),
        # the cycle law: one phase is a constant, never a cycle
        ({"one": {"every_ticks": 4, "cycle": CYCLE[:1]}}, None, None,
         "at least two phase pairs"),
        # the cycle law: the phases are unique
        ({"twin": {
            "every_ticks": 4, "cycle": [CYCLE[0], dict(CYCLE[0])],
         }}, None, None, "repeats"),
        # the event type outside the template closure
        ({"weeks": {"every_ticks": 4, "event_type": "no_such_event"}},
         None, None, "template"),
    ]
    for index, (calendar, macro, seasonal, match) in enumerate(cases):
        with pytest.raises(PackError, match=match):
            crafted_pack(
                tmp_path, f"lint_{index}", calendar,
                macro=macro, seasonal=seasonal,
            )


def test_the_seasonal_ride_lint_binds_to_a_declared_cycled_entry(
    tmp_path: Path,
) -> None:
    """The binding law: `ride` names a DECLARED calendar entry
    carrying a cycle (the phases come from it — an uncycled or absent
    ride is dead data); the weights key on the ride's own phases and
    the chain's own states (closed vocabularies both); a seasonal
    layer that biases nothing is dead data (the vacuity family)."""
    for index, (seasonal, match) in enumerate((
        # the ride names an uncycled (plain) entry
        ({"ride": "weeks", "weights": {"spring": {}}}, "carrying a cycle"),
        # the ride names an absent entry
        ({"ride": "quarters", "weights": {"spring": {}}}, "carrying a cycle"),
        # a seasonal layer that biases nothing
        ({"ride": "seasons"}, "bias"),
        # a phase outside the ride's cycle
        ({"ride": "seasons", "weights": {
            "autumn": {"clear": {"rain": 10}},
         }}, "not a phase of the ride's cycle"),
        # a state outside the chain's vocabulary
        ({"ride": "seasons", "weights": {
            "spring": {"fog": {"rain": 10}},
         }}, "not a declared weather state"),
        # a target outside the chain's vocabulary
        ({"ride": "seasons", "weights": {
            "spring": {"clear": {"fog": 10}},
         }}, "not a declared state"),
    )):
        with pytest.raises(PackError, match=match):
            crafted_pack(
                tmp_path, f"seasonal_{index}", crafted_calendar(),
                seasonal=seasonal,
            )


# -- the runtime: crossings, order, the seasonal ride ---------------------------


def test_the_crossings_fire_as_canon_in_the_coarsest_first_order(
    tmp_path: Path,
) -> None:
    """The loop wiring: every crossing commits ONE event at its own
    tick; at a co-occurring tick the year turns FIRST, then the
    calendar entries in every_ticks DESC order (the season before the
    week), then the rotation — the crossing discipline extended to
    the middle granularities; the cause chain runs through (the
    chronological-chain law)."""
    pack = crafted_pack(tmp_path, "armed", crafted_calendar())
    log, _ = _run(tmp_path, pack, 7, WAIT_100, "crossings")
    _, events = read_log(log, SCHEMA)
    years = [e for e in events if e.type == "year_turns"]
    weeks = _events(events, WEEK_EVENT)
    seasons = _events(events, "spring_turns", "stormy_turns")
    # the run drains past the wait's own tick (the pushed decay/urgency
    # entries extend the drain — the session law; KI#86's seed-time
    # gate means no DEAD erosion entry chases the clock further); the
    # crossings fired at every multiple up to the drain
    assert [e.t for e in years] == [24, 48, 72, 96]
    assert [e.t for e in weeks] == [4 * k for k in range(1, 26)]
    assert [e.t for e in seasons] == [8 * k for k in range(1, 13)]
    # the phases: the run opens at cycle[0] (the first crossing is
    # cycle[1] — no spring event before the wrap at 16)
    assert [e.outcome["phase"] for e in seasons[:4]] == [
        "storm_season", "spring", "storm_season", "spring",
    ]
    # the co-occurrence at t=24: the year FIRST, then the season (the
    # coarser calendar clock), then the week — the crossing discipline
    # extended to the middle granularities
    at_24 = [e for e in events if e.t == 24]
    assert [e.type for e in at_24 if e.type in (
        "year_turns", "spring_turns", "stormy_turns", WEEK_EVENT,
    )] == ["year_turns", "stormy_turns", WEEK_EVENT]
    # the cause chain: the season's turn chains to the WRITER'S LAST
    # id — the immediately preceding canon event at the co-occurring
    # tick (the chronological-chain law; with the default weather ride
    # the chain runs year -> weather roll -> season -> week)
    season_24 = next(e for e in seasons if e.t == 24)
    index_24 = events.index(season_24)
    assert events[index_24 - 1].id == season_24.cause


def test_the_weather_rides_the_seasons_with_the_phase_bias(
    tmp_path: Path,
) -> None:
    """The seasonal layer (the D-030 asymmetric data): the chain's
    rolls MOVE to the ride entry's crossings (never the macro year's
    — one roll cadence per family), and the phase's weight override
    takes the roll (the forced maps make the bias deterministic: the
    storm season rolls storm, the spring rolls rain); the run's
    opening phase biases nothing (no roll before the first crossing —
    the pack's `initial` sky stands until then)."""
    pack = crafted_pack(
        tmp_path, "seasonal", crafted_calendar(), seasonal={
            "ride": "seasons", "weights": FORCED,
        },
    )
    assert seasonal_ride(pack.rules) == "seasons"
    log, _ = _run(tmp_path, pack, 11, WAIT_100, "ride")
    _, events = read_log(log, SCHEMA)
    weather = _events(events, "weather_turns")
    # the rolls sit ONLY at the season crossings (8, 16, ... — never
    # at the year's own 24/48/... alone): every 8th tick
    assert [e.t for e in weather] == [8 * k for k in range(1, 13)]
    # the phase bias: the first crossing is cycle[1] (storm_season)
    # -> storm, the wrap to spring -> rain, alternating with the cycle
    assert [e.outcome["weather"] for e in weather[:4]] == [
        "storm", "rain", "storm", "rain",
    ]
    # the idempotence law: a forced roll onto the CURRENT state is no
    # event — the alternation never repeats, every roll commits here


def test_the_default_ride_stays_the_macro_year(tmp_path: Path) -> None:
    """The default: a weather block WITHOUT the seasonal layer rolls
    at the macro crossings only (the standing law — the family rides
    the clock family's head block); the calendar crossings do not
    move it."""
    pack = crafted_pack(tmp_path, "default", crafted_calendar())
    assert seasonal_ride(pack.rules) is None
    log, _ = _run(tmp_path, pack, 11, WAIT_100, "default")
    _, events = read_log(log, SCHEMA)
    weather = _events(events, "weather_turns")
    assert [e.t for e in weather] == [24, 48, 72, 96]


def test_the_erosion_seeds_at_the_ride_crossings(tmp_path: Path) -> None:
    """The rain's SEEDED follow-up fires from the RIDE crossings too
    (the never-regress law rides the same entry tick — the extracted
    roll keeps the fire follow-ups' shape whole): a smoke-holding
    fold washes at the spring roll's seeded tick."""
    pack = crafted_pack(
        tmp_path, "erosion", crafted_calendar(), seasonal={
            "ride": "seasons", "weights": FORCED,
        },
    )
    # the tavern's rain erosion: smoke true -> false after 30 ticks
    log, _ = _run(tmp_path, pack, 3, WAIT_100, "erosion")
    _, events = read_log(log, SCHEMA)
    weather = _events(events, "weather_turns")
    washes = _events(events, "smoke_washed_away")
    # no smoke ever held in this run (no fire) — the wash family stays
    # silent (the idempotence law: an entity not holding `from` is
    # skipped, never a duplicate, never a no-op line)
    assert not washes
    assert weather  # the rolls themselves fired at the season crossings


def test_the_session_law_and_the_resume_door_straddle_crossings(
    tmp_path: Path,
) -> None:
    """The cursors persist (the session law) and the resume door is
    invisible to the log across a split that straddles calendar
    crossings (the D-139 law): the interrupted-and-resumed run is
    byte-identical to the uninterrupted one — the cursors ride the
    cursor envelope's new `next_calendar` key, with the never-regress
    check refusing a stale cursor."""
    pack = crafted_pack(
        tmp_path, "resume", crafted_calendar(), seasonal={
            "ride": "seasons", "weights": FORCED,
        },
    )
    steps: list[dict[str, Any]] = [
        {"intent": "wait", "ticks": 20},   # crosses 2 seasons, 5 weeks
        {"intent": "wait", "ticks": 30},   # crosses the year at 24, more
    ]
    whole = tmp_path / "whole.jsonl"
    sim = Simulator(pack, 5, whole, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": "whole", "seed": 5, "pack": "tavern_pack@0.1",
        "steps": [dict(s) for s in steps],
    })
    sim.close()
    split = tmp_path / "split.jsonl"
    sim = Simulator(pack, 5, split, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([dict(s) for s in steps[:1]])
    cursor = sim.export_cursor(director_enabled=True)
    assert set(cursor["next_calendar"]) == {"seasons", "weeks"}
    assert all(v > cursor["tick"] for v in cursor["next_calendar"].values())
    sim.close()
    from core.cursor import cursor_path, load_cursor, save_cursor
    save_cursor(cursor_path(split), cursor)
    resumed = Simulator.resume(
        pack, split, SCHEMA, load_cursor(cursor_path(split)),
    )
    resumed.run_steps([dict(s) for s in steps[1:]])
    resumed.close()
    assert split.read_bytes() == whole.read_bytes()


# -- the composed experiment: the committed year run (the T7 form) ---------------


def test_the_committed_year_run_reads_the_whole_calendar(
    tmp_path: Path,
) -> None:
    """The composed experiment (province_calendar.json, seed 42 — the
    F3 four-read-surfaces form): the factor's runner walks to Malby and
    waits through the year. The counts: 36 market days, 12 fairs, the
    four seasons in cycle order (the run OPENS in the thaw — the first
    crossing is the RISE at day 90, the wrap's thaw turns with the year
    at day 360), one year turn (151 — the chronicle binding: the
    genesis horizon 150 + 1), four weather rolls (the seasonal ride —
    one per season crossing, never the year's own). The
    co-occurrence at day 90: the season's rise FIRST, then its weather
    roll (the consumer rides the clock's own event), then the fair,
    then the market — the coarsest-first discipline over the whole
    family. The D-030 read: the rise's roll draws STORM (the
    storm-heavy override — the world's danger turning with the
    season). The determinism: the twin run byte-identical."""
    from core.loop import load_playscript

    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_calendar.json"
    )
    pack = load_pack(REPO / "content" / "province_pack")
    log = tmp_path / "year.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _, events = read_log(log, SCHEMA)

    def _count(*types: str) -> int:
        return sum(1 for e in events if e.type in types)

    assert _count("market_opens") == 36  # every tenth day of 360
    assert _count("fair_opens") == 12  # every thirtieth
    assert _count("thaw_turns", "high_water_rises",
                  "long_light_turns", "first_frost_turns") == 4
    assert _count("year_turns") == 1
    assert _count("weather_turns") == 4  # the ride: one roll per season

    seasons = [e for e in events if e.outcome.get("calendar") == "seasons"]
    assert [e.outcome["phase"] for e in seasons] == [
        "high_water", "long_light", "first_frost", "thaw",
    ]
    assert [e.outcome["day"] for e in seasons] == [90, 180, 270, 360]
    year = next(e for e in events if e.type == "year_turns")
    assert year.outcome["year"] == 151  # the chronicle horizon 150 + 1

    # the co-occurrence at day 90 — the rise, its weather roll, the
    # fair, the market: the coarsest-first discipline over the family
    at_90 = [e.type for e in events if e.t == 129600]
    assert at_90 == [
        "high_water_rises", "weather_turns", "fair_opens", "market_opens",
    ]
    # the D-030 read: the rise's roll draws the storm
    rise_roll = next(
        e for e in events if e.type == "weather_turns" and e.t == 129600
    )
    assert rise_roll.outcome["weather"] == "storm"

    # the determinism: the twin run byte-identical (INV-2)
    twin = tmp_path / "year_twin.jsonl"
    sim = Simulator(pack, 42, twin, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    assert twin.read_bytes() == log.read_bytes()

    # the T7 read surface: the tale renders the calendar's own lines
    # (the story-critical listing decides — the tune-1 split)
    from render.chronicle import render_chronicle

    tale = render_chronicle(events, pack, seed=42)
    assert "Day 10: the river market opens at Malby" in tale
    assert "Day 30: the month's fair at Malby" in tale
    assert "Day 90: the river rises" in tale
    assert "Day 360: the thaw" in tale
    # the ambient family stays canon without a tale line (the weather
    # turns render nothing — the committed form)
    assert "The weather turns" not in tale


# -- the unarmed law + the corpus price (the both-arms form) ---------------------


def test_the_unarmed_twin_is_byte_identical_the_stream_delta_the_calendar(
    tmp_path: Path,
) -> None:
    """The 68a pattern: the calendar-free twin runs byte-identical
    (the block's PRESENCE is the only delta — the calendar path draws
    NOTHING, INV-2 untouched: the substantive fingerprint EQUAL, the
    stream delta the calendar events alone — the iter-83 both-arms
    measurement form, the macro arming's own precedent)."""
    armed = crafted_pack(tmp_path, "armed2", crafted_calendar())
    unarmed = crafted_pack(tmp_path, "unarmed2", None)
    log_a, _ = _run(tmp_path, armed, 42, WAIT_100, "armed2")
    log_b, _ = _run(tmp_path, unarmed, 42, WAIT_100, "unarmed2")
    _, events_a = read_log(log_a, SCHEMA)
    _, events_b = read_log(log_b, SCHEMA)
    # the unarmed arm: zero calendar events by construction
    assert not _events(
        events_b, WEEK_EVENT, "spring_turns", "stormy_turns",
    )
    # the delta is the calendar events ALONE — every other event
    # identical in tick and type (the ids diverge BY CONSTRUCTION:
    # the calendar events consume the id sequence between them)
    types = {"week_turns", "spring_turns", "stormy_turns"}
    stripped = [
        e for e in events_a
        if e.type not in types
    ]
    assert [(e.t, e.type) for e in stripped] == [
        (e.t, e.type) for e in events_b
    ]


def test_the_committed_calendar_sits_beyond_the_corpus_horizon(
    tmp_path: Path,
) -> None:
    """The corpus price (the weather-1 arming's own law): the
    committed province declares the calendar at the REAL cadences —
    the market at 14400, the fair at 43200, the seasons at 129600 —
    every crossing beyond the day-scale corpus scripts' horizon by
    construction; the smoke run (the golden's own script) sees zero
    calendar events, the golden bytes untouched (test_t1_province's
    byte-identity pin IS this law's committed proof)."""
    calendar = PROVINCE.rules["time"]["calendar"]
    for entry in calendar.values():
        assert entry["every_ticks"] >= 14400  # 10 days at 1440/day
    script = json.loads(
        (REPO / "tests" / "playscripts" / "province_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    horizon = 0
    for step in script["steps"]:
        horizon += int(step.get("ticks", 0)) + 2  # wait ticks + a move/beat
    assert horizon < 14400  # the smoke script never reaches the market day
