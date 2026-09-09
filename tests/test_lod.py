"""iter-91 acceptance — depth-3, the scene LOD (three zones; phases.md
§5, the STATUS queue's W2 consumer head — the macro clock's FIRST
consumer, D-124's surface called at the crossing).

The laws pinned here:

- **The zone partition** (`core/lod.py::scene_zones`): a pure function
  of the pack's exits graph + the PC's live position — ACTIVE (the
  PC's location, per-beat), WARM (its exits, the pack's own order),
  COLD (the rest, declaration order). INV-2: construction order,
  never a set; loud on an unreadable fold (the pred-contract family).
- **The one-gate law**: the LOD engages exactly when the macro clock
  is ARMED (`time.macro` declared — the warm cadence IS the macro
  cadence, `core/macro.py`'s arithmetic, one clock with the calendar,
  never a second declaration). The unarmed law is the one-scene
  world: the whole simulation per-beat, the v0.1 bytes (zero corpus
  price by construction — the 68a pattern; the committed pack's
  arming rides with the macro clock's first consumer, weather-1).
- **The warm ring** ticks at the MACRO CROSSINGS: drift + goal rolls
  (the beat machinery minus the director — the story layer stays
  global: pack-authored hooks, budget-bounded, never ambient life);
  the drift chains AFTER the turn (the consumer rides the clock's own
  event), the rolls enqueue at the entry tick (the never-regress law).
- **The cold background rides the turn alone**: its NPC census under
  `cold_npcs` on the macro turn's outcome (the D-112 cardinality
  shape — counts for populations, events for notables; L3 derived,
  INV-1 recorded, never stored). The cold NPCs never tick.
- **The A/B both-arms price** (D-108, the iter-90 pin re-measured):
  the unarmed twin is the committed pack's bytes themselves; the
  armed arm's delta is the macro family alone (the turns + the warm
  ring's events, its rolls on the isolated urgency streams).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from core.fold import initial_projection
from core.lod import LodError, npc_population, scene_zones
from core.log import read_log
from core.loop import Simulator
from core.macro import macro_turn_draft
from core.pack import Pack, load_pack
from core.rng import RngBank, urgency_stream_name
from core.states import decay_drafts
from core.urgencies import urgency_intents
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

PLAYER = "pc_01"
EVENT_TYPE = "year_turns"
TEMPLATE_LINE = "The year turns to {year}, {cold_npcs} souls beyond the ring."
ARMED = {"cadence_ticks": 40, "event_type": EVENT_TYPE}
WAIT_100: list[dict[str, Any]] = [{"intent": "wait", "ticks": 100}]


def crafted_pack(
    tmp_path: Path,
    name: str,
    macro: Any,
    *,
    template: str | None = None,
    self_exit: bool = False,
) -> Pack:
    """A committed-pack copy with `time.macro` set (or REMOVED when
    None — the unarmed arm), the macro template line managed (the
    census-binding arm), and the entities graph editable (the
    self-exit probe — a legal symmetric self-edge, never a ring
    member)."""
    target = tmp_path / name
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if macro is None:
        rules["time"].pop("macro", None)
    else:
        rules["time"]["macro"] = macro
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    templates = json.loads((target / "templates.json").read_text(encoding="utf-8"))
    if template is None:
        templates["events"].pop(EVENT_TYPE, None)
    else:
        templates["events"][EVENT_TYPE] = template
    (target / "templates.json").write_text(
        json.dumps(templates, indent=2), encoding="utf-8"
    )
    if self_exit:
        entities = json.loads((target / "entities.json").read_text(encoding="utf-8"))
        # the market's record: the street's self-edge joins its own exits
        for loc in entities["locations"]:
            if loc["id"] == "loc_street":
                loc["exits"].append("loc_street")  # self-symmetric: legal
        (target / "entities.json").write_text(
            json.dumps(entities, indent=2), encoding="utf-8"
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


def _projection(pack: Pack, player_at: str | None) -> dict[str, dict[str, Any]]:
    """The initial projection with the PC optionally repositioned (the
    zone family's unit arm — the fold view the loop reads live)."""
    state = dict(initial_projection(pack.entities))
    if player_at is not None:
        props = dict(state[PLAYER])
        props["position"] = player_at
        state[PLAYER] = props
    return state


# -- the zone partition (unit) -------------------------------------------------


def test_the_zones_partition_by_the_pc_position() -> None:
    """The committed pack's initial fold: the PC stands at the street —
    ACTIVE the street, WARM its exits in the pack's own order, COLD
    the remaining locations in declaration order (INV-2: construction
    order, never a set). The street's ring covers the whole five-room
    world: the cold background is empty."""
    zones = scene_zones(PACK, _projection(PACK, None))
    assert zones.active == "loc_street"
    assert zones.warm == (
        "loc_tavern", "loc_backyard", "loc_guardroom", "loc_market",
    )
    assert zones.cold == ()


def test_the_zones_follow_the_pc() -> None:
    """The partition is a live fold view: the PC at the tavern — the
    ring is the tavern's own exits, the cold background the guardroom
    and the market (declaration order)."""
    zones = scene_zones(PACK, _projection(PACK, "loc_tavern"))
    assert zones.active == "loc_tavern"
    assert zones.warm == ("loc_street", "loc_backyard")
    assert zones.cold == ("loc_guardroom", "loc_market")


def test_the_partition_is_loud_on_an_unreadable_fold() -> None:
    """The pred-contract family (D-111): a player absent from the fold,
    or standing at an undeclared location, is a LOUD LodError — never
    a KeyError, never a silent pass."""
    with pytest.raises(LodError, match="absent from the projection"):
        scene_zones(PACK, {})
    with pytest.raises(LodError, match="not a declared location"):
        scene_zones(PACK, _projection(PACK, "loc_nope"))


def test_the_census_counts_npcs_alone() -> None:
    """The cold census: kind-`npc` entities only — the ambient group
    positioned in the cold zone is a knowledge-holder population, not
    a ticking soul (the LOD silences nothing of theirs); items are
    not souls either."""
    state = _projection(PACK, "loc_tavern")
    zones = scene_zones(PACK, state)
    assert zones.cold == ("loc_guardroom", "loc_market")
    assert npc_population(PACK, state, zones.cold) == 1  # the relief guard
    assert npc_population(PACK, state, zones.warm) == 0  # empty rooms
    # the room's own four + the PC (an npc positioned there — a soul too)
    assert npc_population(PACK, state, (zones.active,)) == 5


def test_the_self_exit_never_joins_the_ring(tmp_path: Path) -> None:
    """A self-exit is a legal symmetric edge but never a ring member:
    the active location is filtered from its own warm tuple (the
    belt-and-braces law — the zone is a partition, the active scene
    ticks per-beat once)."""
    pack = crafted_pack(tmp_path, "selfexit", None, self_exit=True)
    zones = scene_zones(pack, _projection(pack, None))
    assert zones.active == "loc_street"
    assert "loc_street" not in zones.warm
    assert len(zones.warm) == len(set(zones.warm))  # duplicates filtered


# -- the LOD filters (unit) ----------------------------------------------------


def test_the_decay_filter_scopes_the_walk() -> None:
    """The one-scene law vs the zone scoping: `locations=None` decays
    every NPC (the unarmed default, the v0.1 behavior); a zone tuple
    decays only the NPCs positioned there. The drift law itself is
    interval-proportional — the scoped walk computes the SAME deltas
    for the zone's members, never a second scoring path (L13)."""
    state = _projection(PACK, None)
    every = decay_drafts(PACK, state, {}, 40)
    room = decay_drafts(PACK, state, {}, 40, locations=("loc_tavern",))
    assert {d.target for d in every} == {
        PLAYER, "npc_guard_01", "npc_guard_02",
        "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    }
    assert {d.target for d in room} == {
        "npc_guard_01", "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    }
    # the same deltas for the shared members: the filter cuts, never rescores
    by_target = {d.target: d for d in room}
    for draft in every:
        if draft.target in by_target:
            assert draft.state_changes == by_target[draft.target].state_changes


def test_the_urgency_filter_scopes_the_rolls() -> None:
    """The entry walk cuts BEFORE the roll: `locations=None` rolls
    every pack-declared entry (the one-scene law); a zone tuple rolls
    only the entries whose NPC stands there — the drunk's stream
    never even registers (the family streams are draw-driven: an
    un-rolled entry leaves no stream behind), while the relief
    guard's two entries roll once each (the roll CADENCE is the LOD's
    cost; the odds stay the pack's number — fewer rolls, never
    different odds, L13)."""
    state = _projection(PACK, None)
    bank_all = RngBank(42)
    urgency_intents(PACK, state, bank_all)
    bank_zone = RngBank(42)
    urgency_intents(PACK, state, bank_zone, locations=("loc_guardroom",))
    assert bank_all.count(urgency_stream_name("npc_drunk_01", "coerce")) == 1
    assert bank_zone.count(urgency_stream_name("npc_guard_02", "wait")) == 1
    assert bank_zone.count(urgency_stream_name("npc_guard_02", "look_around")) == 1
    # the excluded entry's stream never drew — the registry is draw-driven
    with pytest.raises(KeyError):
        bank_zone.count(urgency_stream_name("npc_drunk_01", "coerce"))


def test_the_census_key_rides_the_surface_shape() -> None:
    """The D-112 surface accepts the census key (a flat non-negative
    integer beside `year` — the cardinality family); the outcome
    carries both, the template binding surface intact."""
    rules = {**dict(PACK.rules), "time": {
        **dict(PACK.rules["time"]), "macro": ARMED,
    }}
    draft = macro_turn_draft(rules, 40, {"cold_npcs": 2})
    assert draft.outcome == {"year": 151, "cold_npcs": 2}


# -- the run integration (crafted packs) ---------------------------------------


def test_the_armed_ring_ticks_at_the_crossings(tmp_path: Path) -> None:
    """The scheduler rule: cadence 40 over a 100-tick wait — the turns
    at t=40/80, each carrying the census; the WARM NPCs drift at the
    crossing tick chained AFTER the turn (the consumer rides the
    clock's own event); the ACTIVE scene's PCs never drift in the
    window (no beat fires — the active zone keeps the beats); the
    queue drains before the third crossing (never pre-seeded)."""
    pack = crafted_pack(tmp_path, "ring", ARMED, template=TEMPLATE_LINE)
    log, _result = _run(tmp_path, pack, 42, WAIT_100, "ring")
    _header, events = read_log(log, SCHEMA)
    turns = [e for e in events if e.type == EVENT_TYPE]
    assert [e.t for e in turns] == [40, 80]
    drift = [e for e in events if e.type == "status_decayed"]
    assert [e.t for e in drift] == [40] * 5 + [80] * 5  # five warm souls x 2
    assert {e.target for e in drift} == {
        "npc_guard_01", "npc_guard_02",
        "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    }
    assert PLAYER not in {e.target for e in drift}  # the active scene: beats only
    # the drunk's one event carries both axes (the per-NPC change set)
    drunk = next(e for e in drift if e.target == "npc_drunk_01")
    axes = sorted(c.prop for c in drunk.state_changes)
    assert axes == ["status.fatigue", "status.intoxication"]
    # the consumer rides the clock's own event: the FIRST drift at each
    # crossing chains to the turn, the family chains forward within it
    ids = {e.id: e for e in events}
    for tick in (40, 80):
        at_crossing = [e for e in drift if e.t == tick]
        assert at_crossing[0].cause == next(
            e.id for e in turns if e.t == tick
        )
        for event in at_crossing[1:]:
            assert ids[event.cause].t == tick  # the chain stays in the crossing
            assert ids[event.cause].type == "status_decayed"


def test_the_active_zone_ticks_per_beat_the_warm_at_the_crossings(
    tmp_path: Path,
) -> None:
    """The LOD split at a beat distance: cadence 1440 (one year per
    day — the realistic arming), a 1500-tick wait. The beats at
    360/720/1080 decay the ACTIVE scene's PCs alone (the PC at the
    street); the warm souls drift ONCE at the crossing t=1440, the
    full-interval delta (the interval-proportional law — the coarser
    sampling lands the same linear drift, floored per event)."""
    pack = crafted_pack(
        tmp_path, "split", {"cadence_ticks": 1440, "event_type": EVENT_TYPE},
        template=TEMPLATE_LINE,
    )
    log, _result = _run(
        tmp_path, pack, 42, [{"intent": "wait", "ticks": 1500}], "split",
    )
    _header, events = read_log(log, SCHEMA)
    turns = [e for e in events if e.type == EVENT_TYPE]
    assert [e.t for e in turns] == [1440]
    assert turns[0].outcome["cold_npcs"] == 0
    drift = [e for e in events if e.type == "status_decayed"]
    # the PC (active) decays at the three beats, 10 fatigue each
    pc_drift = [e for e in drift if e.target == PLAYER]
    assert [e.t for e in pc_drift] == [360, 720, 1080]
    # the warm souls drift once, at the crossing alone, 40 apiece
    warm_drift = [e for e in drift if e.target != PLAYER]
    assert {e.t for e in warm_drift} == {1440}
    assert {e.target for e in warm_drift} == {
        "npc_guard_01", "npc_guard_02",
        "npc_barkeep_01", "npc_drunk_01", "npc_maid_01",
    }
    fatigue = next(
        c for e in warm_drift if e.target == "npc_barkeep_01"
        for c in e.state_changes if c.prop == "status.fatigue"
    )
    assert fatigue.to_ == 50  # 10 + (1440 * 10) // 360 — the full interval


def test_the_cold_zone_is_silent_and_rides_the_turn_alone(
    tmp_path: Path,
) -> None:
    """The third zone: the PC moves to the tavern, then waits — the
    relief guard's room and the market fall COLD. The guard never
    drifts (its fatigue would move at a warm crossing; cold it stays
    put), the census rides the turn alone (1 soul — the ambient
    crowd never counts), and the room's own four keep the beats (none
    fire in the window — the active zone is per-beat, never
    crossing-fed)."""
    pack = crafted_pack(tmp_path, "cold", ARMED, template=TEMPLATE_LINE)
    steps = [{"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log, _result = _run(tmp_path, pack, 42, steps, "cold")
    _header, events = read_log(log, SCHEMA)
    turns = [e for e in events if e.type == EVENT_TYPE]
    assert len(turns) >= 1
    for turn in turns:
        assert turn.outcome["cold_npcs"] == 1  # the relief guard alone
    drift = [e for e in events if e.type == "status_decayed"]
    assert drift == []  # no beat in the window; the ring holds the empty rooms
    # the guard is SILENT: no event in the whole log targets it
    assert not any(e.target == "npc_guard_02" for e in events)


def test_the_census_follows_the_pc_across_the_move(tmp_path: Path) -> None:
    """The zones are a LIVE fold view: the turn before the move counts
    an empty cold background (the street's ring covers the world);
    after the move the ring is the tavern's own exits and the census
    reads the two-room cold background (the relief guard — the L3
    derivation recomputed at each crossing, never stored)."""
    pack = crafted_pack(tmp_path, "shift", ARMED, template=TEMPLATE_LINE)
    steps = [
        {"intent": "wait", "ticks": 50},       # the crossing at t=40: cold 0
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 50},       # the crossing at t=80: cold 1
    ]
    log, _result = _run(tmp_path, pack, 42, steps, "shift")
    _header, events = read_log(log, SCHEMA)
    turns = [e for e in events if e.type == EVENT_TYPE]
    assert [(e.t, e.outcome["cold_npcs"]) for e in turns] == [(40, 0), (80, 1)]


def test_the_unarmed_twin_is_the_committed_bytes(tmp_path: Path) -> None:
    """The one-scene law (the 68a pattern): the crafted pack WITHOUT
    `time.macro` runs the committed corpus scripts BYTE-IDENTICALLY to
    the committed pack itself — the LOD's presence in the code costs
    an unarmed pack nothing (the T1 golden + every corpus fixture
    untouched — zero re-pins, the v0.1 bytes)."""
    for script in ("plumbing_smoke", "day1_full"):
        playscript = json.loads(
            (REPO / "tests" / "playscripts" / f"{script}.json").read_text(
                encoding="utf-8"
            )
        )
        _log_c, _r_c = _run(tmp_path, PACK, 42, playscript["steps"], f"c_{script}")
        unarmed = crafted_pack(tmp_path, f"u_{script}", None)
        _log_u, _r_u = _run(
            tmp_path, unarmed, 42, playscript["steps"], f"u_{script}",
        )
        assert _log_c.read_bytes() == _log_u.read_bytes()


def test_the_armed_run_is_deterministic(tmp_path: Path) -> None:
    """INV-2: the armed arm is deterministic — same seed + same script,
    byte-identical logs (the crossing order, the census, the ring)."""
    pack = crafted_pack(tmp_path, "det", ARMED, template=TEMPLATE_LINE)
    log_a, _r_a = _run(tmp_path, pack, 42, WAIT_100, "det_a")
    log_b, _r_b = _run(tmp_path, pack, 42, WAIT_100, "det_b")
    assert log_a.read_bytes() == log_b.read_bytes()


def test_the_macro_family_fires_before_the_beat_at_a_co_occurring_tick(
    tmp_path: Path,
) -> None:
    """The co-occurrence order at a crossing+beat tick (t=360, cadence
    360): the year turns FIRST (the coarsest clock), the warm ring's
    drift follows chained to the turn, THEN the beat's active-scene
    decay (the PC) — the calendar contains the day, the day contains
    the beat, and the ring rides the calendar's own slot."""
    pack = crafted_pack(
        tmp_path, "cooccur", {"cadence_ticks": 360, "event_type": EVENT_TYPE},
        template=TEMPLATE_LINE,
    )
    log, _result = _run(
        tmp_path, pack, 42, [{"intent": "wait", "ticks": 400}], "cooccur",
    )
    _header, events = read_log(log, SCHEMA)
    at_tick = [e for e in events if e.t == 360]
    types = [e.type for e in at_tick]
    assert types[0] == EVENT_TYPE  # the year turns first
    # the warm ring's drift follows, before the beat's active decay
    assert types[1] == "status_decayed"
    assert at_tick[1].cause == at_tick[0].id  # chained to the turn
    pc_drift = next(e for e in at_tick if e.target == PLAYER)
    assert types.index("status_decayed") < at_tick.index(pc_drift)


def test_the_census_binds_through_the_template(tmp_path: Path) -> None:
    """The tale arm: the story-critical listing + the template's
    {cold_npcs} binding — the census renders its chronicle line (the
    flat-keys family: the outcome key is the binding surface); the
    zone's souls ride the turn's own prose, the counts-for-populations
    law made visible."""
    rules_path = tmp_path / "listed"
    shutil.copytree(REPO / "content" / "tavern_pack", rules_path)
    rules = json.loads((rules_path / "rules.json").read_text(encoding="utf-8"))
    rules["time"]["macro"] = ARMED
    rules["importance"]["story_critical_events"] = [
        *rules["importance"]["story_critical_events"], EVENT_TYPE,
    ]
    (rules_path / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    templates = json.loads(
        (rules_path / "templates.json").read_text(encoding="utf-8")
    )
    templates["events"][EVENT_TYPE] = TEMPLATE_LINE
    (rules_path / "templates.json").write_text(
        json.dumps(templates, indent=2), encoding="utf-8"
    )
    pack = load_pack(rules_path)
    steps = [{"intent": "move", "target": "loc_tavern"}, *WAIT_100]
    log, _result = _run(tmp_path, pack, 42, steps, "listed")
    header, events = read_log(log, SCHEMA)
    text = render_chronicle(events, pack, seed=int(header["seed"]))
    assert "The year turns to 151, 1 souls beyond the ring." in text
