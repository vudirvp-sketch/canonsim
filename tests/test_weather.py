"""iter-98 acceptance — weather-1, the ambient weather family + canon
erosion (the STATUS queue's live row after st-6a; TASKS "ambient
weather + canon erosion"; D-116 (7): an ambient family over the existing
doors, no physics engine; phases.md §5 the architecture owner).

The laws pinned here:

- **The cadence law**: the family rides the macro clock's crossings —
  one chain roll per crossing, AFTER the turn, the change event chained
  to the turn (the drift's precedent: the consumer rides the clock's
  own event). The pairing law (one direction): a weather block without
  `time.macro` is dead data, refused at load; the clock may run
  weatherless.
- **The chain law**: pack-declared states with per-state weights (the
  Markov chain in data — self-weights keep weather sticky; NO TTL, no
  turn counters, no decay timers, D-049's fence). The draw rides the
  isolated `weather:chain` stream (the D-079 family's seventh member,
  singleton) — the substantive fingerprint never sees a weather roll.
  A roll that lands on the CURRENT state suppresses the event (the
  idempotence law, KI#13's family) while still advancing the stream.
- **The fold law (L3)**: the current weather is the last weather
  event's outcome key, the pack's `initial` before the first — derived,
  never stored; the event carries no state_changes.
- **The ambient law**: no knowledge on the weather event (a world
  event, the macro turn's shape — the sky is ambient context, not a
  per-entity fact; the blind-NPC rule never applies to the sky).
- **The seeded consequences (TIME-1 SEEDED)**: the change event carries
  the new state's hook tags — the director's buffer seeds them at
  commit through the existing door (D-005); the storm's murmur rides
  the ambient channel's quiet gate (the D-082 pattern verbatim).
- **The erosion law (the arson family's shape)**: SEEDED follow-ups
  carrying `state_changes` — the change event seeds one queue entry per
  pack-declared rule at the crossing tick + `after_ticks`; the drafts
  read the fold at FIRE time (idempotent: an entity no longer holding
  `from` is skipped); an explicit counter-event is the legal revert of
  a held flag (EVENT_SCHEMA §4). The never-regress law: a crossing that
  fires late (a batch before a far entry) seeds no earlier than the
  world's resumed tick.
- **The corpus price**: the committed macro ARMING (weather-1's row,
  the primitive's first consumer) — the cadence 518400 (a full year of
  the pack's own day) sits beyond every corpus script's horizon: the
  T1 golden + day1_theft byte-identical, the price the LOD's one-gate
  engagement alone on day1_full (depth-3's designed price, paid here —
  the warm ring's beat events move to the crossings, the fingerprint
  equal). The weather block itself adds ZERO corpus events (no
  crossing, no roll — the unarmed family's twin is byte-identical to
  the macro-armed bytes).
- **The lint family** (`core/pack.py::_weather`): the closed
  vocabulary, the pairing + identity laws, the weights' closure, the
  hooks' registry closure, the erosion rules' shapes (the queue
  identity unique, the prop a transition follow-up flag, from != to),
  and the reachability law (every state reachable from `initial`).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.log import read_log
from core.loop import Simulator
from core.pack import Pack, PackError, load_pack
from core.rng import RngBank, weather_stream_name
from core.weather import (
    ErosionSpec,
    WeatherError,
    current_weather,
    erosion_drafts,
    erosion_specs,
    weather_turn_draft,
)
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

PLAYER = "pc_01"
#: The crafted arming's own event type (the pack's vocabulary choice —
#: the weather event is a pack-declared event type, never an engine
#: word, INV-3; the engine's surface is shape-only).
WEATHER_EVENT = "weather_turns"
YEAR_EVENT = "year_turns"
#: The crafted macro cadence (the corpus scripts never reach a year at
#: the committed 518400; the crafted twin squeezes years into a run).
ARMED = {"cadence_ticks": 40, "event_type": YEAR_EVENT}
WAIT_100: list[dict[str, Any]] = [{"intent": "wait", "ticks": 100}]
#: The fire-chain script (day1_theft's own shape — the erosion needs a
#: smoky location to wash).
FIRE_STEPS: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "steal", "target": "npc_guard_01", "method": "distraction"},
    {"intent": "take", "target": "oil_lamp_01"},
    {"intent": "move", "target": "loc_backyard"},
    {"intent": "drop_break", "target": "oil_lamp_01", "near": "back_wall"},
    {"intent": "wait", "ticks": 200},
]


def crafted_pack(
    tmp_path: Path,
    name: str,
    *,
    macro: Any = "armed",
    weather: Any = "keep",
    patch_weather: Any = None,
    story_critical: list[str] | None = None,
) -> Pack:
    """A committed-pack copy with the macro clock and the weather block
    managed (`"armed"` = the crafted short cadence 40, the default for
    the integration probes; `"committed"` = the pack's own year-scale
    518400 block kept verbatim, the corpus tests' arm; None = BOTH
    blocks removed — the pairing law binds them at load; a dict = the
    macro block replaced) plus an optional weather surgery callable
    (the chain-bias and lint probes mutate the parsed block)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if macro == "armed":
        rules["time"]["macro"] = ARMED
    elif macro is None:
        rules["time"].pop("macro", None)
        rules.pop("weather", None)  # the pairing law: no clock, no family
    elif macro != "committed":
        rules["time"]["macro"] = macro
    if weather != "keep":
        if weather is None:
            rules.pop("weather", None)
        else:
            rules["weather"] = weather
    if patch_weather is not None:
        patch_weather(rules["weather"])
    if story_critical is not None:
        rules["importance"]["story_critical_events"] = story_critical
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
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


# -- the fold law + the chain law (unit) ----------------------------------------


def test_the_fold_reads_the_pack_initial_before_the_first_event() -> None:
    """L3: the current weather is the last weather event's outcome key;
    before any event, the pack's declared `initial` (the run opens
    under the pack's sky — deterministic, no draw at start)."""
    rules = dict(PACK.rules)
    assert current_weather(rules, []) == "clear"
    class _Evt:  # a minimal duck: the fold reads type + outcome alone
        def __init__(self, type_: str, weather: str) -> None:
            self.type, self.outcome = type_, {"weather": weather}
    events = [_Evt("move", "x"), _Evt(WEATHER_EVENT, "storm"),
              _Evt("move", "x")]
    assert current_weather(rules, events) == "storm"  # the newest wins


def test_the_no_op_roll_suppresses_the_event_and_advances_the_stream() -> None:
    """The idempotence law: a roll that lands on the current state is
    None — no no-op line in the canon (KI#13's family) — while the draw
    STILL advanced the family's own stream (INV-2: the stream's state
    moves, determinism untouched)."""
    rules = {**dict(PACK.rules), "time": {
        **dict(PACK.rules["time"]), "macro": ARMED,
    }}
    sticky = {**dict(rules["weather"]), "states": {
        "clear": {"weights": {"clear": 1}},  # the self-only chain: stuck
        "overcast": {"weights": {"clear": 1}},
        "rain": {"weights": {"clear": 1}},
        "storm": {"weights": {"clear": 1}},
    }}
    rules["weather"] = sticky
    bank = RngBank(42)
    bank.peek(weather_stream_name())  # registers the family stream lazily
    before = bank.count(weather_stream_name())
    assert weather_turn_draft(rules, bank, 40, "clear") is None
    assert bank.count(weather_stream_name()) == before + 1


def test_the_raw_read_backstops_fail_loud() -> None:
    """The pred-contract family (D-111): a hand-built runtime config
    that skips the lint fails loudly — no block, a broken chain source,
    empty weights — never a KeyError, never a silent pass."""
    unarmed = dict(PACK.rules)
    unarmed.pop("weather", None)
    with pytest.raises(WeatherError, match="armed"):
        weather_turn_draft(unarmed, RngBank(42), 40, "clear")
    with pytest.raises(WeatherError, match="declare"):
        weather_turn_draft(dict(PACK.rules), RngBank(42), 40, "hail")
    with pytest.raises(WeatherError, match="declare"):
        erosion_specs(dict(PACK.rules), "hail")
    with pytest.raises(WeatherError, match="armed"):
        erosion_specs(unarmed, "rain")


def test_the_chain_walk_is_sorted_and_division_free() -> None:
    """The weighted pick over the sorted keys (INV-2: never set
    iteration); the same seed walks the same chain (the stream is the
    chain's own — deterministic, isolated)."""
    rules = dict(PACK.rules)
    states = {
        "clear": {"weights": {"clear": 1, "rain": 3}},  # rain 3 of 4
        "overcast": {"weights": {"clear": 1}},
        "rain": {"weights": {"clear": 1}},
        "storm": {"weights": {"clear": 1}},
    }
    rules["weather"] = {**dict(rules["weather"]), "states": states}
    drawn = [
        weather_turn_draft(rules, RngBank(7), 40, "clear")
        for _ in range(12)
    ]
    assert all(d is not None and d.outcome["weather"] == "rain" for d in drawn)
    assert all(d.type == WEATHER_EVENT and d.actor == "world" for d in drawn)
    assert all(d.knowledge == () and d.state_changes == () for d in drawn)


def test_the_storm_carries_the_seeded_consequences() -> None:
    """TIME-1 SEEDED: the change event carries the new state's hook
    tags (the director's buffer seeds them at commit — D-005); the
    importance feeds the rule's far-hook term."""
    rules = dict(PACK.rules)
    storm = {
        **dict(rules["weather"]),
        "states": {
            "clear": {"weights": {"storm": 1}},
            "overcast": {"weights": {"clear": 1}},
            "rain": {"weights": {"clear": 1}},
            "storm": {"weights": {"clear": 1}},
        },
    }
    rules["weather"] = storm
    draft = weather_turn_draft(rules, RngBank(42), 40, "clear")
    assert draft is not None
    assert draft.hooks == ()  # the storm state's own hooks
    rules["weather"] = {**dict(storm), "states": {
        **dict(storm["states"]),
        "storm": {"weights": {"clear": 1}, "hooks": ["storm_drunk_murmur"]},
    }}
    draft = weather_turn_draft(rules, RngBank(42), 40, "clear")
    assert draft is not None
    assert draft.hooks == ("storm_drunk_murmur",)
    assert draft.outcome == {"weather": "storm"}
    assert draft.importance == "low"  # unlisted + one far hook: the rule's own


# -- the erosion drafts (unit) ----------------------------------------------------


def _projection_with_smoke() -> dict[str, dict[str, Any]]:
    from core.fold import initial_projection
    projection = initial_projection(PACK.entities)
    projection["loc_backyard"]["smoke"] = True
    projection["loc_tavern"]["smoke"] = True
    return projection


def test_the_erosion_scans_the_fold_in_sorted_order() -> None:
    """One draft per entity holding `from` on the target prop, sorted
    id order (INV-2: construction order never iterates a set); the
    change carries the explicit revert (EVENT_SCHEMA §4) with the
    fold's own current value as `from_` (the D-035 commit contract)."""
    projection = _projection_with_smoke()
    drafts = erosion_drafts(
        dict(PACK.rules), projection, 70, "smoke_washed_away", "ev_0042"
    )
    assert [d.target for d in drafts] == ["loc_backyard", "loc_tavern"]
    for draft in drafts:
        assert draft.type == "smoke_washed_away"
        assert draft.actor == "world"
        assert draft.cause == "ev_0042"
        assert draft.knowledge == ()
        assert draft.outcome == {"weather": "rain", "location": draft.target}
    assert all(
        [(c.entity, c.prop, c.from_, c.to_, c.irreversible)
         for c in d.state_changes]
        == [(d.target, "smoke", True, False, False)]
        for d in drafts
    )


def test_the_erosion_is_idempotent_on_state() -> None:
    """The fold at fire time is the truth: an entity no longer holding
    `from` is skipped (the story was already told, or never began) —
    the KI#13 discipline, no no-op lines, no duplicates."""
    projection = _projection_with_smoke()
    projection["loc_backyard"]["smoke"] = False  # already washed
    drafts = erosion_drafts(
        dict(PACK.rules), projection, 70, "smoke_washed_away", "ev_0042"
    )
    assert [d.target for d in drafts] == ["loc_tavern"]
    clean = _projection_with_smoke()
    clean["loc_backyard"].pop("smoke")
    clean["loc_tavern"].pop("smoke")
    assert erosion_drafts(
        dict(PACK.rules), clean, 70, "smoke_washed_away", "ev_0042"
    ) == ()


def test_the_erosion_rule_lookup_is_loud_on_an_unknown_identity() -> None:
    """The queue identity is the rule's event type (unique per block by
    lint); a payload naming an unknown one is a caller bug — loud,
    never an empty pass (a silent no-op would hide the queue's own
    desync)."""
    with pytest.raises(WeatherError, match="not declared"):
        erosion_drafts(
            dict(PACK.rules), _projection_with_smoke(), 70,
            "no_such_erosion", "ev_0042",
        )


def test_the_erosion_specs_read_the_state_rules() -> None:
    """The SEEDED follow-up specs (the arson family's FollowUpSpec
    twin): the state's rules as queue entries at +after_ticks."""
    assert erosion_specs(dict(PACK.rules), "rain") == (
        ErosionSpec(event_type="smoke_washed_away", at_tick=30),
    )
    assert erosion_specs(dict(PACK.rules), "clear") == ()
    assert erosion_specs(dict(PACK.rules), "storm") == ()


# -- the run integration (crafted packs) -------------------------------------------


def test_the_armed_run_turns_the_weather_at_the_crossings(
    tmp_path: Path,
) -> None:
    """The cadence law: one chain roll per crossing, the change event
    chained to the turn (the drift's precedent), the suppression law
    skipping the no-op rolls; the fold's current weather drives the
    next roll (L3 — no stored state anywhere)."""
    pack = crafted_pack(tmp_path, "armed")
    log, _result = _run(tmp_path, pack, 42, WAIT_100, "armed")
    _header, events = read_log(log, SCHEMA)
    turns = [e for e in events if e.type == YEAR_EVENT]
    skies = [e for e in events if e.type == WEATHER_EVENT]
    assert len(turns) == 2  # t=40, t=80 (the queue drains before the third)
    assert len(skies) <= 2  # the suppression law: only the changes
    ids = [event.id for event in events]
    for sky in skies:
        index = ids.index(sky.id)
        assert index > 0
        assert sky.cause == events[index - 1].id  # chained to the turn
        assert sky.t in (40, 80)
        assert sky.actor == "world" and sky.target is None
        assert sky.outcome["weather"] in {"clear", "overcast", "rain", "storm"}


def test_the_armed_run_is_deterministic(tmp_path: Path) -> None:
    """INV-2: same seed + same script — byte-identical logs (the chain
    rolls, the crossings, the erosion, the order)."""
    pack = crafted_pack(tmp_path, "det")
    log_a, _ra = _run(tmp_path, pack, 42, WAIT_100, "det_a")
    log_b, _rb = _run(tmp_path, pack, 42, WAIT_100, "det_b")
    assert log_a.read_bytes() == log_b.read_bytes()


def test_the_weather_draws_never_touch_the_substantive_fingerprint(
    tmp_path: Path,
) -> None:
    """The isolation law (the D-079 family's seventh member): the chain
    rolls on `weather:chain` alone — the both-arms fingerprint EQUAL
    (the armed weather vs the weather-less twin over the SAME armed
    macro clock; the stream delta the weather events alone)."""
    armed = crafted_pack(tmp_path, "iso_armed")
    bare = crafted_pack(tmp_path, "iso_bare", weather=None)
    log_a, result_a = _run(tmp_path, armed, 42, WAIT_100, "iso_a")
    log_b, result_b = _run(tmp_path, bare, 42, WAIT_100, "iso_b")
    assert result_a.fingerprint == result_b.fingerprint
    _header, events_a = read_log(log_a, SCHEMA)
    _header, events_b = read_log(log_b, SCHEMA)
    skies_a = [e for e in events_a if e.type == WEATHER_EVENT]
    assert not any(e.type == WEATHER_EVENT for e in events_b)
    assert len(events_a) == len(events_b) + len(skies_a)


def test_the_rain_washes_the_smoke_from_the_burned_location(
    tmp_path: Path,
) -> None:
    """The erosion integration (the arson family's shape over the
    ambient family's rule): the fire seeds the smoke; the rain's change
    event seeds the wash; the wash commits the explicit revert
    (smoke True -> False) on every holding location, cause-chained to
    the weather event; the fold replays it (T2's shape — fold(log) ==
    the runtime projection)."""
    def bias_rain(weather: dict[str, Any]) -> None:
        # the clear sky rolls rain early — the wash deterministically
        # lands inside the run (all states stay reachable)
        weather["states"]["clear"]["weights"] = {
            "rain": 10, "overcast": 1, "clear": 1,
        }

    pack = crafted_pack(tmp_path, "wash", patch_weather=bias_rain)
    log, _result = _run(tmp_path, pack, 8, FIRE_STEPS, "wash")
    _header, events = read_log(log, SCHEMA)
    washes = [e for e in events if e.type == "smoke_washed_away"]
    assert washes  # the rain came and the wash fired
    skies = [e for e in events if e.type == WEATHER_EVENT]
    rain = next(e for e in skies if e.outcome["weather"] == "rain")
    for wash in washes:
        assert wash.cause == rain.id  # the SEEDED chain: the sky's own event
        assert wash.t >= rain.t + 30  # the deferral, never before the seed
        change = wash.state_changes[0]
        assert (change.entity, change.prop, change.from_, change.to_) == (
            wash.target, "smoke", True, False,
        )
    # T2: the fold replays the projection with the wash included
    from core.fold import fold, initial_projection
    sim = Simulator(pack, 8, tmp_path / "wash2.jsonl", SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": "wash", "seed": 8, "pack": "tavern_pack@0.1", "steps": FIRE_STEPS}
    )
    _header2, events2 = read_log(tmp_path / "wash2.jsonl", SCHEMA)
    rebuilt = fold(events2, initial_projection(pack.entities))
    assert rebuilt == sim.projection
    assert sim.projection["loc_backyard"]["smoke"] is False
    sim.close()


def test_the_wash_never_regresses_behind_the_clock(tmp_path: Path) -> None:
    """The never-regress law: a crossing that fires LATE (the batch of
    missed crossings before a far entry) seeds its follow-up no earlier
    than the world's resumed tick — the deferral bends, the order never
    breaks (the clock-regression crash is the refused world)."""
    pack = crafted_pack(tmp_path, "regress")
    # the far entry: one long wait jumps the clock past several
    # crossings at once — the batch fires them, the wash seeds late
    log, _result = _run(tmp_path, pack, 8, FIRE_STEPS, "regress")
    _header, events = read_log(log, SCHEMA)
    skies = [e for e in events if e.type == WEATHER_EVENT]
    washes = [e for e in events if e.type == "smoke_washed_away"]
    for wash in washes:
        for sky in skies:
            if sky.id == wash.cause:
                assert wash.t >= sky.t  # never behind its own seed
    ticks = [e.t for e in events]
    assert ticks == sorted(ticks)  # the writer's monotonicity held


def test_the_storm_seeds_the_directors_buffer(
    tmp_path: Path,
) -> None:
    """The seeded consequences (TIME-1): the storm's change event
    carries the hook tag; the director's buffer holds it after the
    crossing (D-005 — seeded at commit time, the release the ambient
    channel's quiet gate at a later beat)."""
    def pin_storm(weather: dict[str, Any]) -> None:
        # the first roll lands on storm; the ring keeps every state
        # reachable (the reachability law) while the storm dominates
        weather["states"]["clear"]["weights"] = {"storm": 10, "clear": 1}
        weather["states"]["storm"]["weights"] = {"overcast": 1}
        weather["states"]["overcast"]["weights"] = {"rain": 1}
        weather["states"]["rain"]["weights"] = {"storm": 10, "rain": 1}

    stormy = crafted_pack(tmp_path, "stormy", patch_weather=pin_storm)
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 380},  # the crossing at 40 + the beat at 360
    ]
    log, _result = _run(tmp_path, stormy, 42, steps, "stormy")
    _header, events = read_log(log, SCHEMA)
    storm = next(e for e in events if e.type == WEATHER_EVENT)
    assert storm.hooks == ("storm_drunk_murmur",)
    rambles = [
        e for e in events
        if e.type == "ramble"
        and str(e.provenance.get("cause_intent", "")).startswith("director_")
    ]
    assert rambles  # the quiet gate released the storm murmur at the beat
    assert all(
        r.t > storm.t for r in rambles
    )  # the release follows the seeding, never precedes it


def test_the_crossing_cursor_survives_the_session_boundary(
    tmp_path: Path,
) -> None:
    """The session law: `run_steps` is a feed-and-drain cycle — the
    weather state (the fold) and the macro cursor persist between
    calls; a crossing between calls fires when the next call's entries
    advance past it."""
    pack = crafted_pack(tmp_path, "session")
    log = tmp_path / "session.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([{"intent": "wait", "ticks": 30}])
    sim.run_steps([{"intent": "wait", "ticks": 30}])  # crosses t=40
    sim.close()
    _header, events = read_log(log, SCHEMA)
    assert any(e.t == 40 and e.type == YEAR_EVENT for e in events)
    skies = [e for e in events if e.type == WEATHER_EVENT]
    assert len(skies) <= 1  # at most one change inside the window


def test_the_tale_gate_follows_the_story_critical_listing(
    tmp_path: Path,
) -> None:
    """The tune-1 split: unlisted, the weather event is canon without a
    line (low importance); listed, the chronicle renders the {weather}
    slot (the flat-keys family — the outcome key is the binding
    surface)."""
    listed = crafted_pack(
        tmp_path, "listed",
        story_critical=[
            *PACK.rules["importance"]["story_critical_events"], WEATHER_EVENT,
        ],
    )
    log, _result = _run(tmp_path, listed, 42, WAIT_100, "listed")
    header, events = read_log(log, SCHEMA)
    text = render_chronicle(events, listed, seed=int(header["seed"]))
    skies = [e for e in events if e.type == WEATHER_EVENT]
    for sky in skies:
        assert f"The weather turns: {sky.outcome['weather']}." in text
    unlisted = crafted_pack(tmp_path, "unlisted")
    log_u, _result_u = _run(tmp_path, unlisted, 42, WAIT_100, "unlisted_r")
    header_u, events_u = read_log(log_u, SCHEMA)
    text_u = render_chronicle(events_u, unlisted, seed=int(header_u["seed"]))
    assert "The weather turns" not in text_u  # canon, not tale


# -- the corpus price (the committed arming) --------------------------------------


def test_the_committed_arming_keeps_the_short_corpus_bytes(
    tmp_path: Path,
) -> None:
    """The committed cadence 518400 (a full year) sits beyond every
    corpus script's horizon: plumbing_smoke + day1_theft run
    byte-identically to the unarmed-macro twin (the T1 golden and the
    day1 fixture untouched — zero macro events, zero weather rolls,
    zero LOD scoping before the first beat)."""
    unarmed = crafted_pack(tmp_path, "unarmed", macro=None)
    for script in ("plumbing_smoke", "day1_theft_and_arson"):
        playscript = json.loads(
            (REPO / "tests" / "playscripts" / f"{script}.json").read_text(
                encoding="utf-8"
            )
        )
        _log_c, _r_c = _run(
            tmp_path, PACK, playscript["seed"], playscript["steps"], f"c_{script}"
        )
        _log_u, _r_u = _run(
            tmp_path, unarmed, playscript["seed"], playscript["steps"], f"u_{script}"
        )
        assert _log_c.read_bytes() == _log_u.read_bytes()


def test_the_committed_macro_price_is_the_lod_delta_on_day1_full(
    tmp_path: Path,
) -> None:
    """The one-gate law's designed price, paid at the arming: the armed
    committed pack vs the macro-less twin over day1_full — the warm
    ring's beat events move to the crossings (never reached on a
    day-scale run: the status_decayed and urgency-scan counts drop),
    the substantive fingerprint EQUAL (the LOD's rolls ride the
    isolated urgency streams, the weather never draws — no crossing),
    the delta the warm-ring family alone. The T1 golden (t <= 58, no
    beats) is byte-identical — the v0.1 pin."""
    unarmed = crafted_pack(tmp_path, "price", macro=None)
    script = json.loads(
        (REPO / "tests" / "playscripts" / "day1_full.json").read_text(
            encoding="utf-8"
        )
    )
    _log_c, result_c = _run(
        tmp_path, PACK, script["seed"], script["steps"], "price_c"
    )
    _log_u, result_u = _run(
        tmp_path, unarmed, script["seed"], script["steps"], "price_u"
    )
    assert result_c.fingerprint == result_u.fingerprint
    _header, events_c = read_log(_log_c, SCHEMA)
    _header, events_u = read_log(_log_u, SCHEMA)
    # the warm ring's beat events vanish (they wait for the crossings):
    assert len(events_c) < len(events_u)
    assert not any(e.type in (YEAR_EVENT, WEATHER_EVENT) for e in events_c)


def test_the_weather_block_adds_zero_corpus_events(
    tmp_path: Path,
) -> None:
    """The weather family's own corpus price: the committed pack vs the
    weather-less twin (the SAME committed year-scale macro clock) —
    byte-identical on every corpus script (no crossing inside any
    horizon, no roll, no event, no seed; the block's presence costs the
    corpus nothing — the 68a pattern's twin at family granularity)."""
    bare = crafted_pack(tmp_path, "bare", macro="committed", weather=None)
    for script in ("plumbing_smoke", "day1_theft_and_arson", "day1_full"):
        playscript = json.loads(
            (REPO / "tests" / "playscripts" / f"{script}.json").read_text(
                encoding="utf-8"
            )
        )
        _log_c, _r_c = _run(
            tmp_path, PACK, playscript["seed"], playscript["steps"], f"w_c_{script}"
        )
        _log_b, _r_b = _run(
            tmp_path, bare, playscript["seed"], playscript["steps"], f"w_b_{script}"
        )
        assert _log_c.read_bytes() == _log_b.read_bytes(), script


# -- the lint family ----------------------------------------------------------------


def test_the_lint_refuses_the_broken_arming(tmp_path: Path) -> None:
    """The closed-vocabulary family: unknown block keys, a non-object
    block, the pairing law (weather without the macro clock), the
    identity law (the weather event type is the macro turn's own), an
    undeclared initial, empty states, the weights' closure + sign, the
    hooks' registry closure, the erosion shapes (the queue identity
    unique, the template closure, the prop closure, from == to,
    after_ticks), and the reachability law — all loud PackErrors at
    load, never mid-run surprises."""
    base = json.loads(
        (REPO / "content" / "tavern_pack" / "rules.json").read_text(
            encoding="utf-8"
        )
    )

    def probe(name: str, mutate: Any, match: str) -> None:
        rules = json.loads(json.dumps(base))
        rules["time"]["macro"] = {"cadence_ticks": 40, "event_type": YEAR_EVENT}
        mutate(rules)
        target = tmp_path / f"lint_{name}"
        shutil.copytree(REPO / "content" / "tavern_pack", target)
        (target / "rules.json").write_text(
            json.dumps(rules, indent=2), encoding="utf-8"
        )
        with pytest.raises(PackError, match=match):
            load_pack(target)

    probe("extra_key", lambda r: r["weather"].update({"seasons": []}), "unknown keys")
    probe("not_object", lambda r: r.update({"weather": [1]}), "must be an object")
    probe(
        "pairing", lambda r: r["time"].pop("macro"), "declare time.macro"
    )
    probe(
        "identity",
        lambda r: r["weather"].update({"event_type": "year_turns"}),
        "macro turn's own event type",
    )
    probe("initial", lambda r: r["weather"].update({"initial": "hail"}), "initial")
    probe("no_states", lambda r: r["weather"].update({"states": {}}), "non-empty")
    probe(
        "state_keys",
        lambda r: r["weather"]["states"]["clear"].update({"climate": 1}),
        "unknown keys",
    )
    probe(
        "weight_target",
        lambda r: r["weather"]["states"]["clear"]["weights"].update({"hail": 1}),
        "not a declared state",
    )
    probe(
        "weight_zero",
        lambda r: r["weather"]["states"]["clear"]["weights"].update({"clear": 0}),
        "integer >= 1",
    )
    probe(
        "weight_empty",
        lambda r: r["weather"]["states"]["clear"].update({"weights": {}}),
        "non-empty object",
    )
    probe(
        "hook_tag",
        lambda r: r["weather"]["states"]["storm"].update(
            {"hooks": ["no_such_hook"]}
        ),
        "director.hooks entry",
    )
    probe(
        "erosion_keys",
        lambda r: r["weather"]["states"]["rain"]["erosion"][0].update(
            {"chance": 0.5}
        ),
        "unknown keys",
    )
    probe(
        "erosion_template",
        lambda r: r["weather"]["states"]["rain"]["erosion"][0].update(
            {"event_type": "no_such_event"}
        ),
        "template vocabulary",
    )
    probe(
        "erosion_identity",
        lambda r: r["weather"]["states"]["storm"].update(
            {"erosion": [{"event_type": "smoke_washed_away", "after_ticks": 5,
                          "prop": "smoke", "from": True, "to": False}]}
        ),
        "queue identity",
    )
    probe(
        "erosion_after",
        lambda r: r["weather"]["states"]["rain"]["erosion"][0].update(
            {"after_ticks": 0}
        ),
        "after_ticks",
    )
    probe(
        "erosion_prop",
        lambda r: r["weather"]["states"]["rain"]["erosion"][0].update(
            {"prop": "status.fear"}
        ),
        "follow-up flag",
    )
    probe(
        "erosion_noop",
        lambda r: r["weather"]["states"]["rain"]["erosion"][0].update(
            {"to": True}
        ),
        "from and to",
    )
    probe(
        "erosion_irreversible",
        lambda r: r["weather"]["states"]["rain"]["erosion"][0].update(
            {"irreversible": "yes"}
        ),
        "irreversible",
    )
    probe(
        "unreachable",
        lambda r: r["weather"]["states"]["clear"].update(
            {"weights": {"clear": 1}}
        ),
        "unreachable",
    )


def test_the_committed_declarations_are_the_armed_shape() -> None:
    """The committed pack's own landing: the macro clock ARMED (the
    year-scale cadence — 360 days of the pack's own day, the calendar
    binding continuing the genesis horizon), the weather block's four
    states all reachable, the storm's hook declared in the director's
    registry (the closure), and the three template lines present (the
    tale arms render through them)."""
    macro = PACK.rules["time"]["macro"]
    assert macro == {"cadence_ticks": 518400, "event_type": "year_turns"}
    weather = PACK.rules["weather"]
    assert weather["event_type"] == "weather_turns"
    assert weather["initial"] == "clear"
    assert set(weather["states"]) == {"clear", "overcast", "rain", "storm"}
    assert "storm_drunk_murmur" in PACK.rules["director"]["hooks"]
    for line in ("year_turns", "weather_turns", "smoke_washed_away"):
        assert line in PACK.templates["events"]
