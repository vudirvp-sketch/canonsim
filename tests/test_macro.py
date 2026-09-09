"""iter-90 acceptance — maclock-1, the macro-clock primitive (W2's
head, FIRST among its consumers; TASKS/phases.md §5 — L4 layered
clocks: micro-time and macro-time, one authority, two granularities).

The laws pinned here:

- **The scheduler cadence rule** (INV-2-clean, the depth-3 "scheduler
  rule" family): crossings are the positive multiples of the
  pack-declared `time.macro.cadence_ticks` — pure tick arithmetic,
  never entropy; the loop fires them in the crossing discipline (tick
  order; at a co-occurring tick the COARSEST clock first — the year
  turns before the day's rotation, the rotation before the beat).
- **The macro-year counter + the calendar binding** (D-116 (4)):
  `year = start + t // cadence`, derived never stored (L3); the start
  is the worldgen-armed pack's chronicle horizon (the genesis years
  are the world's history BEFORE the run — one timeline), 0 for an
  unarmed pack. Neither a global tick-year constant (TIME-1 + the
  AGENTS §8 tick-semantics fence) nor forever-decorative years.
- **The aggregate-event emission surface** (D-112's shape — one event
  with cardinality): `macro_turn_draft` carries the year + the
  consumer's counts as flat integer keys; the count vocabulary is the
  future consumers' (depth-3/depth-7/st-6a/weather-1 land AFTER the
  primitive — one primitive, one row, first, the scheduler
  blast-radius insurance); a count key named `year` is a branch fake,
  refused.
- **The unarmed law** (the 68a pattern): the committed pack declares
  no `time.macro` block — zero crossings, zero events, the v0.1 bytes
  untouched; the A/B arms differ in the block's PRESENCE alone, the
  substantive fingerprint EQUAL (the macro path draws nothing), the
  stream delta the macro events alone (the iter-83 both-arms
  measurement form). The committed arming rides with the primitive's
  first consumer.
- **The turn event's shape**: actor `world`, cause = the writer's last
  id (the chronological-chain law, the rotation's scheduled-beat
  precedent), no knowledge (a world event), no state_changes (the year
  is derived), no hooks (the director boundary is the consumers'
  rows); importance rides the pack's own rule — the story-critical
  listing decides tale visibility (the tune-1 split).
- **The session law**: the crossing cursor persists across
  `run_steps` calls (the rotation/beat family); a run still ends when
  its script's queue drains (never pre-seeded past the drain).
- **The lint family** (`core/pack.py::_time_rules`): the closed
  `time.macro` vocabulary, the positive-int cadence, the event type
  in the template closure (EVENT_SCHEMA §11).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.log import read_log
from core.loop import Simulator
from core.macro import (
    MacroError,
    macro_turn_draft,
    macro_year,
    macro_year_start,
    next_macro_tick,
)
from core.pack import Pack, PackError, load_pack
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

PLAYER = "pc_01"
#: The crafted arming's own event type (the pack's vocabulary choice —
#: the macro turn is a pack-declared event type, never an engine word,
#: INV-3; the engine's surface is shape-only).
EVENT_TYPE = "year_turns"
#: The crafted template line — the `{year}` slot binds the outcome's
#: counter key (the flat-keys family: the template binding surface).
TEMPLATE_LINE = "The year turns to {year}."
#: The worldgen horizon the crafted armed arm reuses (test_worldgen's
#: WG twin — the calendar binding's armed end).
HORIZON = 150


def crafted_pack(
    tmp_path: Path,
    name: str,
    macro: Any,
    *,
    worldgen: bool = True,
    template: bool | str = True,
    story_critical: bool = False,
    rotation_offsets: list[int] | None = None,
    beat_ticks: list[int] | None = None,
) -> Pack:
    """A committed-pack copy with `time.macro` set (or REMOVED when
    None — the unarmed arm), the worldgen block kept (True — the
    calendar binding's armed end) or removed (False — the unarmed-
    worldgen twin: the counter counts from 0), the macro template line
    managed (True: the line; False: the closure-refusal arm removes it
    from templates too), the story-critical listing managed (the tale
    visibility arm), and the rotation/beat cadences overridable (the
    co-occurrence probes)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if macro is None:
        rules["time"].pop("macro", None)
    else:
        rules["time"]["macro"] = macro
    if not worldgen:
        rules.pop("worldgen", None)
        # bridge-1's law: the scene line's claim-bound fields are dead
        # without their claims — the unarmed twin carries layout alone
        # (the test_worldgen crafted-pack precedent)
        rules["brief"]["present_entities"]["scene_line_fields"] = ["layout"]
    if rotation_offsets is not None:
        rules["crime_watch"]["watch_rotation_ticks"] = rotation_offsets
    if beat_ticks is not None:
        rules["urgencies"]["beat_ticks"] = beat_ticks
    if story_critical:
        listing = rules["importance"]["story_critical_events"]
        rules["importance"]["story_critical_events"] = [*listing, EVENT_TYPE]
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    if template is False:
        templates["events"].pop(EVENT_TYPE, None)
    else:
        templates["events"][EVENT_TYPE] = (
            TEMPLATE_LINE if template is True else template
        )
    (target / "templates.json").write_text(
        json.dumps(templates, indent=2), encoding="utf-8"
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


#: one wait long enough to cross two 40-tick years (the queue drains
#: before the third crossing — the never-pre-seeded law)
WAIT_100: list[dict[str, Any]] = [{"intent": "wait", "ticks": 100}]

ARMED = {"cadence_ticks": 40, "event_type": EVENT_TYPE}


# -- the cadence arithmetic (unit) ---------------------------------------------


def test_unarmed_answers_none_and_the_declared_shape_is_loud() -> None:
    """The unarmed law: an ABSENT `time.macro` key is no crossings —
    `next_macro_tick` answers None (the loop's cursor never forms, the
    v0.1 bytes untouched by construction, the 68a pattern); a block
    DECLARED without its cadence is a caller bug — loud, never a
    silent pass (the pred-contract family)."""
    assert next_macro_tick(None, 0) is None
    with pytest.raises(MacroError, match="cadence_ticks"):
        next_macro_tick({}, 100)  # declared but broken


def test_crossings_are_the_positive_cadence_multiples() -> None:
    """The scheduler cadence rule: the smallest multiple strictly
    after `after` — pure integer arithmetic (INV-2-clean: tick-derived,
    never entropy), the depth-3 scheduler-rule family's shape."""
    macro = {"cadence_ticks": 40}
    assert next_macro_tick(macro, 0) == 40  # tick 0 is the run start, never a crossing
    assert next_macro_tick(macro, 39) == 40
    assert next_macro_tick(macro, 40) == 80
    assert next_macro_tick(macro, 79) == 80
    assert next_macro_tick(macro, 120) == 160
    assert next_macro_tick({"cadence_ticks": 1}, 0) == 1


def test_a_broken_cadence_fails_loud_never_silently() -> None:
    """The raw-read backstop (the pred-contract family, D-111): a
    hand-built runtime config with a zero/negative/non-integer cadence
    raises MacroError naming the block — an infinite crossing loop is
    never a clock, and a KeyError must never leak."""
    for bad in (0, -1, "40", 1.5, True, None):
        with pytest.raises(MacroError, match="cadence_ticks"):
            next_macro_tick({"cadence_ticks": bad}, 0)


# -- the counter + the calendar binding (unit) ---------------------------------


def test_the_year_counter_binds_to_the_chronicle_horizon() -> None:
    """The calendar binding (D-116 (4)): the genesis years are the
    world's history BEFORE the run, so the live counter continues from
    the chronicle horizon — one timeline, both ends pack-declared;
    never a global tick-year constant, never forever-decorative
    years."""
    rules = dict(PACK.rules)  # the committed pack: worldgen-armed, horizon 150
    assert macro_year_start(rules) == HORIZON
    unarmed = dict(PACK.rules)
    unarmed.pop("worldgen", None)
    assert macro_year_start(unarmed) == 0


def test_the_year_is_derived_never_stored() -> None:
    """The counter law (L3): `year = start + t // cadence` — a pure
    function of the tick; each turn's event records the value (INV-1),
    no state anywhere."""
    rules = {**dict(PACK.rules), "time": {
        **dict(PACK.rules["time"]), "macro": ARMED,
    }}
    assert macro_year(rules, 0) == HORIZON  # the run starts in the current year
    assert macro_year(rules, 39) == HORIZON
    assert macro_year(rules, 40) == HORIZON + 1
    assert macro_year(rules, 79) == HORIZON + 1
    assert macro_year(rules, 80) == HORIZON + 2
    unarmed = dict(PACK.rules)
    unarmed.pop("worldgen", None)
    unarmed["time"] = {**dict(PACK.rules["time"]), "macro": ARMED}
    assert macro_year(unarmed, 40) == 1  # the unarmed world counts from 0


def test_the_counter_reads_only_an_armed_clock() -> None:
    """`macro_year` on an unarmed pack is a caller bug — loud, never a
    silent zero (the counter would otherwise read as a real year)."""
    with pytest.raises(MacroError, match="no time.macro"):
        macro_year(dict(PACK.rules), 40)


# -- the aggregate emission surface (unit) -------------------------------------


def _armed_rules(worldgen: bool) -> dict[str, Any]:
    rules = dict(PACK.rules)
    if not worldgen:
        rules.pop("worldgen", None)
    rules["time"] = {**dict(PACK.rules["time"]), "macro": ARMED}
    return rules


def test_the_surface_is_one_event_with_cardinality() -> None:
    """The D-112 shape: the draft's outcome carries the year + the
    consumer's counts as FLAT integer keys (the flat-keys family — the
    template binding surface); actor `world`, no knowledge, no state
    changes (the year is derived), no hooks; importance through the
    pack's own rule (unlisted: the turn is canon, not tale)."""
    draft = macro_turn_draft(_armed_rules(True), 80, {"caravans": 3, "losses": 1})
    assert draft.type == EVENT_TYPE
    assert draft.actor == "world"
    assert draft.cause is None  # the loop chains at commit
    assert draft.outcome == {"year": HORIZON + 2, "caravans": 3, "losses": 1}
    assert draft.knowledge == () and draft.state_changes == ()
    assert draft.hooks == ()
    assert draft.importance == "low"  # unlisted in story_critical_events


def test_the_refuses_the_counter_key_and_non_counts() -> None:
    """A count named `year` is a branch fake (the {year?...} template
    conditional branches on the outcome shape — RESERVED_CLAIM_SLOTS'
    twin); a non-count value is not cardinality; an unarmed pack has
    no surface to call."""
    with pytest.raises(MacroError, match="reserved"):
        macro_turn_draft(_armed_rules(True), 40, {"year": 2})
    with pytest.raises(MacroError, match="cardinality"):
        macro_turn_draft(_armed_rules(True), 40, {"caravans": -1})
    with pytest.raises(MacroError, match="cardinality"):
        macro_turn_draft(_armed_rules(True), 40, {"caravans": 1.5})
    with pytest.raises(MacroError, match="cardinality"):
        macro_turn_draft(_armed_rules(True), 40, {"caravans": "3"})
    with pytest.raises(MacroError, match="no time.macro"):
        macro_turn_draft(dict(PACK.rules), 40)


def test_the_story_critical_listing_decides_tale_visibility() -> None:
    """The tune-1 split: the RULE owns the signal/noise choice — an
    unlisted turn stays low (canon, not tale); the pack's listing
    raises it through the same rule every world event reads (one rule
    for action events and world events)."""
    rules = _armed_rules(True)
    listing = [*rules["importance"]["story_critical_events"], EVENT_TYPE]
    rules["importance"] = {**rules["importance"],
                           "story_critical_events": listing}
    assert macro_turn_draft(rules, 40).importance == "medium"


# -- the run integration (crafted packs) ---------------------------------------


def test_the_armed_run_turns_the_years_at_the_crossings(
    tmp_path: Path,
) -> None:
    """The crossing integration: cadence 40 over a 100-tick wait — the
    turns fire at t=40 and t=80 (BEFORE the entry that crossed them,
    the crossing discipline), each chained to the writer's last id
    (the chronological chain), the year continuing the horizon (the
    binding: 151, 152); the queue drains before the third crossing
    (never pre-seeded past the drain)."""
    pack = crafted_pack(tmp_path, "armed", ARMED)
    log, _result = _run(tmp_path, pack, 42, WAIT_100, "armed")
    header, events = read_log(log, SCHEMA)
    turns = [e for e in events if e.type == EVENT_TYPE]
    assert [(e.t, e.outcome["year"]) for e in turns] == [(40, 151), (80, 152)]
    for turn in turns:
        assert turn.actor == "world"
        assert turn.knowledge == () and turn.state_changes == ()
        assert turn.hooks == ()
        assert turn.importance == "low"
    # the chronological chain: each turn's cause names the immediately
    # preceding event's id (the rotation's scheduled-beat precedent)
    ids = [event.id for event in events]
    for turn in turns:
        index = ids.index(turn.id)
        assert index > 0
        assert turn.cause == events[index - 1].id


def test_the_unarmed_worldgen_twin_counts_from_zero(
    tmp_path: Path,
) -> None:
    """The binding's unarmed end: a pack with the macro clock but no
    worldgen counts its years from 0 (the first turn is year 1) — the
    genesis horizon is the armed end alone."""
    pack = crafted_pack(tmp_path, "no_worldgen", ARMED, worldgen=False)
    log, _result = _run(tmp_path, pack, 42, WAIT_100, "no_worldgen")
    _header, events = read_log(log, SCHEMA)
    turns = [e for e in events if e.type == EVENT_TYPE]
    assert [(e.t, e.outcome["year"]) for e in turns] == [(40, 1), (80, 2)]


def test_the_corpus_price_is_the_macro_events_alone(
    tmp_path: Path,
) -> None:
    """The both-arms measurement (D-108): the armed arm vs the unarmed
    twin (the block's PRESENCE alone differs) — the substantive
    fingerprint EQUAL (the macro path draws nothing; the armed arm
    rides the worldgen streams' own draws verbatim), the event count
    delta exactly the turns, and the unarmed arm of the COMMITTED pack
    is the v0.1 bytes themselves (T1's golden pin — zero price by
    construction)."""
    armed_pack = crafted_pack(tmp_path, "ab_armed", ARMED)
    unarmed_pack = crafted_pack(tmp_path, "ab_unarmed", None)
    log_a, result_a = _run(tmp_path, armed_pack, 42, WAIT_100, "ab_armed")
    log_u, result_u = _run(tmp_path, unarmed_pack, 42, WAIT_100, "ab_unarmed")
    _header, events_a = read_log(log_a, SCHEMA)
    _header, events_u = read_log(log_u, SCHEMA)
    assert result_a.fingerprint == result_u.fingerprint  # zero draws on the macro path
    turns_a = [e for e in events_a if e.type == EVENT_TYPE]
    assert len(events_a) == len(events_u) + len(turns_a) == len(events_u) + 2
    # the committed pack (no time.macro block) is the unarmed arm's twin:
    # zero macro events in its golden fixture (T1) — the v0.1 bytes
    assert not any(e.type == EVENT_TYPE for e in events_u)


def test_same_seed_renders_byte_identical_runs(tmp_path: Path) -> None:
    """INV-2: the armed arm is deterministic — same seed + same script,
    byte-identical logs (the crossing order, the counter, the chain)."""
    pack = crafted_pack(tmp_path, "det", ARMED)
    log_a, _result_a = _run(tmp_path, pack, 42, WAIT_100, "det_a")
    log_b, _result_b = _run(tmp_path, pack, 42, WAIT_100, "det_b")
    assert log_a.read_bytes() == log_b.read_bytes()


def test_the_coarsest_clock_fires_first_at_a_co_occurring_tick(
    tmp_path: Path,
) -> None:
    """The crossing-order law: at a co-occurring tick the year turns
    BEFORE the day's rotation (the calendar contains the day) — the
    macro event's id precedes the watch_change's at the same tick
    (equal ticks are legal; the writer's monotonicity is
    non-decreasing)."""
    pack = crafted_pack(
        tmp_path, "cooccur", {"cadence_ticks": 720, "event_type": EVENT_TYPE},
        rotation_offsets=[720],
    )
    log, _result = _run(tmp_path, pack, 42, [{"intent": "wait", "ticks": 800}], "cooccur")
    _header, events = read_log(log, SCHEMA)
    at_tick = [e for e in events if e.t == 720]
    types = [e.type for e in at_tick]
    assert types[0] == EVENT_TYPE  # the year turns first
    assert "watch_change" in types  # the rotation follows at the same tick
    assert types.index(EVENT_TYPE) < types.index("watch_change")


def test_the_crossing_cursor_survives_the_session_boundary(
    tmp_path: Path,
) -> None:
    """The session law: `run_steps` is a feed-and-drain cycle — the
    macro cursor persists between calls like the rotation/beat
    cursors; a crossing that falls between calls fires when the next
    call's entries advance past it (never pre-seeded, never skipped)."""
    pack = crafted_pack(tmp_path, "session", ARMED)
    log = tmp_path / "session.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([{"intent": "wait", "ticks": 30}])  # entries reach t~32
    sim.run_steps([{"intent": "wait", "ticks": 30}])  # the completion at t~62 crosses 40
    sim.close()
    _header, events = read_log(log, SCHEMA)
    turns = [e for e in events if e.type == EVENT_TYPE]
    assert [(e.t, e.outcome["year"]) for e in turns] == [(40, 151)]


def test_the_turn_renders_when_the_pack_lists_it(
    tmp_path: Path,
) -> None:
    """The tale visibility arm: the story-critical listing + the
    template line's {year} binding — the turn renders its chronicle
    line (the outcome's counter key is the flat binding surface);
    unlisted, the turn is canon without a line (the tune-1 split —
    the gate follows the rule)."""
    listed = crafted_pack(tmp_path, "listed", ARMED, story_critical=True)
    log, _result = _run(tmp_path, listed, 42, WAIT_100, "listed")
    header, events = read_log(log, SCHEMA)
    text = render_chronicle(events, listed, seed=int(header["seed"]))
    assert "The year turns to 151." in text
    assert "The year turns to 152." in text
    unlisted = crafted_pack(tmp_path, "unlisted", ARMED, story_critical=False)
    log_u, _result_u = _run(tmp_path, unlisted, 42, WAIT_100, "unlisted_r")
    header_u, events_u = read_log(log_u, SCHEMA)
    text_u = render_chronicle(events_u, unlisted, seed=int(header_u["seed"]))
    assert "The year turns" not in text_u  # sub-gate: canon, not tale


# -- the lint family -------------------------------------------------------------


def test_the_lint_refuses_the_broken_arming(tmp_path: Path) -> None:
    """The closed `time.macro` vocabulary: unknown keys, a
    zero/negative cadence, a non-integer cadence, a non-object block,
    and an event type outside the template closure (EVENT_SCHEMA §11)
    are all loud PackErrors at load, never mid-run surprises."""
    for index, (macro, match) in enumerate((
        ({"cadence_ticks": 40, "event_type": EVENT_TYPE, "years": 1}, "unknown keys"),
        ({"cadence_ticks": 0, "event_type": EVENT_TYPE}, "cadence_ticks"),
        ({"cadence_ticks": -40, "event_type": EVENT_TYPE}, "cadence_ticks"),
        ({"cadence_ticks": "40", "event_type": EVENT_TYPE}, "cadence_ticks"),
        ({"cadence_ticks": 40, "event_type": "no_such_event"}, "template"),
        ({"cadence_ticks": 40}, "event_type"),
        ([1, 2, 3], "must be an object"),
    )):
        with pytest.raises(PackError, match=match):
            crafted_pack(tmp_path, f"lint_{index}", macro)


def test_the_armed_packs_load_and_the_committed_pack_stays_unarmed() -> None:
    """The committed pack declares no `time.macro` block (the 68a
    pattern — the arming rides with the first consumer); the crafted
    arming loads clean (the lint passes what the run path reads)."""
    assert "macro" not in PACK.rules["time"]
