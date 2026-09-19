"""pack-4 acceptance — the pressure-city pack (iter-149, D-182): the
displacement law as pure pack vocabulary on the untouched engine (the
T1 slice: one district, one boiler, one gauge, three factions, one
Cooling-Debt chain — zero core change).

The row's minimal test set, in order:
(1) the closed cycle — res-1's second consumer: the crafted twin's
    short macro cadence fires the three flows (the fire eats coal, the
    gauge climbs, the grid bleeds pressure — the SPATIAL half: the
    cost moves through the cycle's nodes, the arithmetic pinned); the
    feed's transfer conserves (the cart -5 / the store +5) and the
    empty cart's attempt is a logged soft rejection (attempts are
    facts, D3's front-door arm); the derived price reads the declared
    scarcity direction (base 30, per_unit -1 — the D-119 binding).
(2) the Cooling-Debt chain — the TEMPORAL half: each hard burn shocks
    the FIRST unshocked seam in pack order (the deterministic
    ratchet), the spot flags irreversible; the knocking at +600 and
    the collection at +4320 fire as the delayed public follow-ups, the
    second seed of each silenced by the idempotence law (KI#13's
    family); NOTHING ever writes a seam back (the never-regress law).
(3) the world's replies — the MORAL half: the scream's dread (+5 on
    the hearers, the burner included), the feed's warmth (-2, the
    feeder included), the collection's cold (+10 on the district); and
    the SPIRAL's close: the burst's cold tips the tenants' ratio, the
    watch pleads, the widow feeds (the emergent loop, never scripted).
(4) the objective-function triangle — depth-6: the crafted twins push
    the member axes past the bars and the goals fire through the front
    door (the stokers' group burn — actor = the group, the ignite
    through D-112's one-id law, the seams saturating and the goal
    going silent on the spent machine); the bench's convening and the
    keeper's echo-gated ration answer the knocking (the antagonist
    pair's divergence over the same system); below the bar never fires
    (the deadband).
(5) the read surface — the ONE meter: the scene line renders the LIVE
    gauge at the firehole (integer truth below, one rendered line
    above) and NOTHING renders the debt (the thermometer minus: no
    marker, no scene field, no template ever names a seam count).
(6) T1 — the same-seed twin byte-identical, the committed golden
    fixture pinned, a different seed diverges (the tavern T1's exact
    shape over the FIFTH pack — the universality claim's corpus half).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from brief.assembler import assemble_brief, render_brief
from core.economy import price_of
from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import Pack, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
PACK_DIR = REPO / "content" / "pressure_pack"
PACK = load_pack(PACK_DIR)
GOLDEN = REPO / "tests" / "fixtures" / "pressure_smoke_seed42.jsonl"
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "pressure_smoke.json")

PLAYER = "pc_01"
BOILER = "loc_boilerhouse"
GROUP_STOKERS = "grp_stokers"
KEEPER = "npc_regulator_02"
WIDOW = "npc_tenant_01"


# -- the harness ---------------------------------------------------------------


def pressure_twin(
    tmp_path: Path, name: str, patch: dict[str, Any]
) -> Pack:
    """A committed-pressure copy with a JSON patch applied (the crafted-
    twin pattern, the packci family): `patch` maps a file name to the
    REPLACEMENT value for that file's top-level key (a dict patches the
    key deep, a list replaces it wholesale)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    for file_name, repl in patch.items():
        data = json.loads((target / file_name).read_text(encoding="utf-8"))
        for key, value in repl.items():
            if isinstance(value, dict) and isinstance(data.get(key), dict):
                data[key].update(value)
            else:
                data[key] = value
        (target / file_name).write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )
    return load_pack(target)


def _move_pc(position: str) -> dict[str, Any]:
    """An entities.json patch that parks the player at `position`."""
    entities = json.loads((PACK_DIR / "entities.json").read_text(encoding="utf-8"))
    for npc in entities["npcs"]:
        if npc["id"] == PLAYER:
            npc["position"] = position
    return {"entities.json": {"npcs": entities["npcs"]}}


def _seed_axes(axes: dict[str, int], members: tuple[str, ...]) -> dict[str, Any]:
    """An entities.json patch that reseeds the given status axes on the
    given members (the ratio's crafted initial condition)."""
    entities = json.loads((PACK_DIR / "entities.json").read_text(encoding="utf-8"))
    for npc in entities["npcs"]:
        if npc["id"] in members:
            npc["status"].update(axes)
    return {"entities.json": {"npcs": entities["npcs"]}}


def _merge_npc_patch(*patches: dict[str, Any]) -> dict[str, Any]:
    """Merge two entities.json npc-list patches (the later seeds win on
    a shared npc's re-seeded axes; the positions compose — each patch
    carries the FULL list, so the merge re-applies them in order)."""
    npcs = json.loads((PACK_DIR / "entities.json").read_text(encoding="utf-8"))["npcs"]
    for patch in patches:
        by_id = {npc["id"]: npc for npc in patch["entities.json"]["npcs"]}
        for npc in npcs:
            if npc["id"] in by_id:
                npc.update(by_id[npc["id"]])
    return {"entities.json": {"npcs": npcs}}


def run(
    tmp_path: Path, pack: Pack, steps: list[dict[str, Any]],
    name: str, seed: int = 42,
) -> list[Any]:
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "pressure_pack@0.1", "steps": steps}
    )
    _, events = read_log(log, SCHEMA)
    return events


def by_type(events: list[Any], *types: str) -> list[Any]:
    return [event for event in events if event.type in types]


def prop(events: list[Any], entity: str, prop_name: str) -> Any:
    """The last state_change value written to a prop (the folded read)."""
    value = None
    for event in events:
        for change in event.state_changes:
            if change.entity == entity and change.prop == prop_name:
                value = change.to_
    return value


# -- (1) the closed cycle -------------------------------------------------------


def test_the_two_flow_arms_fire_on_a_short_cadence(tmp_path: Path) -> None:
    """The SPATIAL half: the crafted twin's macro year at one beat fires
    the closed cycle's two aggregate flows — the fire eats three coal
    from the store and the gauge holds its net degree (the FOLDED
    cycle: the gross climb six less the grid's draw five — the cost
    moving through the cycle's nodes, the arithmetic exact; the co-due
    same-account limit that forced the fold is discovered and recorded
    in the economy block's own notes, never patched in-core)."""
    twin = pressure_twin(
        tmp_path, "short_year",
        {"rules.json": {"time": {"macro": {
            "cadence_ticks": 360, "event_type": "year_turns",
        }}}},
    )
    events = run(
        tmp_path, twin, [{"intent": "wait", "ticks": 400}], "flows"
    )
    flows = {
        event.outcome.get("flow"): event
        for event in by_type(events, "account_sourced", "account_consumed")
    }
    assert set(flows) == {"the_fire_eats", "the_gauge_holds"}
    # the fire eats three coal from the store: 8 -> 5
    eat = [c for c in flows["the_fire_eats"].state_changes][0]
    assert (eat.entity, eat.prop, eat.from_, eat.to_) == (
        BOILER, "account.coal", 8, 5
    )
    # the gauge's net hold: the gross climb six less the draw five
    hold = [c for c in flows["the_gauge_holds"].state_changes][0]
    assert (hold.entity, hold.prop, hold.from_, hold.to_) == (
        BOILER, "account.pressure", 40, 41
    )
    # the macro turn's own event opened the crossing (the pairing law)
    assert by_type(events, "year_turns")


def test_the_feed_conserves_and_the_empty_cart_rejects_softly(
    tmp_path: Path,
) -> None:
    """The player-scaled arm: the haul mints five coal to the cart, the
    feed moves them into the store (conservation exact), and a second
    feed from the empty cart is a logged SOFT rejection — attempts are
    facts, the underflow floor's front-door arm (D3), never a negative
    stock."""
    events = run(
        tmp_path, PACK,
        [
            {"intent": "haul_coal", "target": "loc_coalyard"},
            {"intent": "feed_the_fire", "target": BOILER},
            {"intent": "feed_the_fire", "target": BOILER},
        ],
        "feed",
    )
    haul = by_type(events, "account_sourced")
    assert len(haul) == 1  # the cart: 0 -> 5
    feeds = by_type(events, "account_transferred")
    assert len(feeds) == 1  # the store: 8 -> 13, the cart: 5 -> 0
    for change in feeds[0].state_changes:
        if change.entity == PLAYER:
            assert (change.prop, change.from_, change.to_) == ("account.coal", 5, 0)
        else:
            assert (change.entity, change.prop, change.from_, change.to_) == (
                BOILER, "account.coal", 8, 13
            )
    rejected = by_type(events, "intent_rejected")
    assert len(rejected) == 1
    assert rejected[0].outcome["failed_test"] == "actor.account_at_least"
    assert rejected[0].outcome["action"] == "feed_the_fire"


def test_the_derived_price_reads_the_scarcity_direction() -> None:
    """The D-119 binding paid (grim's identity read superseded): base 30,
    per_unit -1 — the yard's asking for the next scuttle falls as the
    firehole's store grows (the scarcity DIRECTION, a derived read,
    never stored, never a transaction)."""
    assert price_of(PACK.rules, "coal", 0) == 30
    assert price_of(PACK.rules, "coal", 8) == 22
    assert price_of(PACK.rules, "coal", 18) == 12


# -- (2) the Cooling-Debt chain -------------------------------------------------


def test_each_burn_shocks_the_first_whole_seam_in_pack_order() -> None:
    """The ratchet: the golden run's two burns shocked the FIRST
    UNSHOCKED seam each time, in the pack's declaration order — the
    deterministic, draw-free selection (never a roll, never a skip)."""
    seams = [
        change
        for event in by_type(load_golden(), "seam_shocked")
        for change in event.state_changes
    ]
    assert [change.prop for change in seams] == [
        "thermal_shock.main_riser", "thermal_shock.east_joint",
    ]
    assert all(change.from_ is None and change.to_ == "shocked" for change in seams)
    assert all(change.irreversible for change in seams)


def test_the_knocking_and_the_collection_fire_on_schedule_and_idempotently() -> None:
    """The delayed public follow-ups: the knocking at +600 and the
    collection at +4320 after the FIRST burn; the second burn's seeds
    of both are SILENCED by the fired flags (the idempotence law —
    the first knock says the line, the first burst ends the decade)."""
    events = load_golden()
    knocks = by_type(events, "pipes_knock")
    collections = by_type(events, "debt_collects")
    burns = by_type(events, "boiler_run_hard")
    assert [event.t for event in burns] == [7, 34]
    assert len(knocks) == 1 and knocks[0].t == 7 + 600  # not 34 + 600
    assert len(collections) == 1 and collections[0].t == 7 + 4320
    # the follow-up flags are irreversible counter-events on the location
    for change in knocks[0].state_changes + collections[0].state_changes:
        assert change.entity == BOILER and change.irreversible


def test_nothing_ever_writes_a_seam_back() -> None:
    """The never-regress law, pinned on the committed corpus: every
    seam write in the golden log is a BIRTH (None -> shocked); no event
    anywhere reverts, decrements, or re-writes a shocked seam — the
    debt is monotonic by construction, not by vigilance."""
    events = load_golden()
    seam_writes = [
        (event.type, change)
        for event in events
        for change in event.state_changes
        if change.prop.startswith("thermal_shock.")
    ]
    assert seam_writes  # the debt grew in the committed run
    for _, change in seam_writes:
        assert change.from_ is None and change.to_ == "shocked"


# -- (3) the world's replies + the spiral ---------------------------------------


def test_the_scream_the_warmth_and_the_cold_replies() -> None:
    """The moral half (consequence-rendered, never scored): the scream
    leaves five dread on everyone who heard it (the BURNER included —
    the moral cost lands on the hand that chose it); a fed fire warms
    the feeder and the wall-hearers two degrees; the burst collects
    ten cold from the whole district."""
    events = load_golden()
    # the scream (t=7): pc 10->15, both stokers +5
    first_dread = by_type(events, "dread_rises")[0]
    shifted = {(c.entity, c.from_, c.to_) for c in first_dread.state_changes}
    assert (PLAYER, 10, 15) in shifted
    assert ("npc_stoker_01", 20, 25) in shifted
    assert ("npc_stoker_02", 15, 20) in shifted
    # the feed (t=27): the feeder and the stokers through the wall -2
    warmth = by_type(events, "warmth_felt")[0]
    warmed = {(c.entity, c.from_, c.to_) for c in warmth.state_changes}
    assert (PLAYER, 20, 18) in warmed  # the feeder feels his own fire
    assert ("npc_stoker_01", 35, 33) in warmed  # through the shared wall
    # the burst (t=4327): the district +10
    cold = by_type(events, "the_cold_collects")[0]
    collected = {(c.entity, c.from_, c.to_) for c in cold.state_changes}
    assert (WIDOW, 40, 50) in collected
    assert ("npc_regulator_01", 15, 25) in collected


def test_the_spiral_closes_the_burst_tips_the_watch_and_the_widow_feeds() -> None:
    """The emergent loop, end to end on the committed run: burst ->
    the district's cold +10 -> the tenants' ratio past the bar -> the
    watch pleads -> the widow spends the scuttle -> the warmth reply.
    Every link is the world's own machinery; none of it is scripted."""
    events = load_golden()
    burst = by_type(events, "debt_collects")[0]
    cold = by_type(events, "the_cold_collects")[0]
    pleas = by_type(events, "the_watch_pleads")
    feeds = [
        event
        for event in by_type(events, "account_transferred")
        if event.actor == WIDOW
    ]
    assert burst.t <= cold.t < pleas[0].t < feeds[0].t  # the cold reply
    # is the burst's own cause-chained reaction (same tick, chained id)
    # the widow's scuttle: 6 -> 1 (five coal, the hoard's one feed)
    for change in feeds[0].state_changes:
        if change.entity == WIDOW:
            assert (change.prop, change.from_, change.to_) == ("account.coal", 6, 1)
    # the burst's cold tipped the ratio: the tenants were past the
    # trigger before the plea fired (the crafted arithmetic)
    assert prop(events, WIDOW, "status.cold") == 48  # 50 - 2 (her own feed)


# -- (4) the objective-function triangle ----------------------------------------


def test_the_stokers_burn_through_the_front_door_and_saturate(
    tmp_path: Path,
) -> None:
    """The fire arm (minimum immediate cold): the crafted twin parks the
    player at the firehole (the beats' faction walk reads the active
    zone) and the circle's own ratio — the members' cold seeds, past
    the bar at open — drives the GROUP's stoke_hard through the front
    door (actor = the group, D-112's one-id law) until every seam is
    shocked and the goal goes silent on the spent machine."""
    twin = pressure_twin(tmp_path, "at_firehole", _move_pc(BOILER))
    events = run(
        tmp_path, twin, [{"intent": "wait", "ticks": 3600}], "circle"
    )
    group_burns = [
        event
        for event in by_type(events, "boiler_run_hard")
        if event.actor == GROUP_STOKERS
    ]
    assert group_burns  # the group burned, through the same door
    seams = {
        change.prop
        for event in by_type(events, "seam_shocked")
        for change in event.state_changes
    }
    assert seams == {  # the machine's whole capacity, spent by the circle
        "thermal_shock.main_riser",
        "thermal_shock.east_joint",
        "thermal_shock.crown_seam",
    }
    # the saturation: no burn AFTER the last seam (the goal's
    # spot_available pre-gate holds the spent machine silent)
    last_seam_tick = max(
        event.t for event in by_type(events, "seam_shocked")
    )
    assert all(event.t <= last_seam_tick for event in group_burns)


def test_the_bench_convenes_and_the_keeper_rations_on_the_knock(
    tmp_path: Path,
) -> None:
    """The ledger arm (minimum 20-year systemic damage): the crafted run
    burns once and parks the reader at the registry; the knocking
    (+10 dread through the shared walls) crosses BOTH keepers' bar —
    the bench convenes (the public order, the ratio's own voice) and
    the keeper's echo-gated ration releases four coal from the reserve
    (the knocking's residue the gate, the grim guard's precedent). The
    antagonist pair's divergence: the SAME system, the OTHER answer."""
    twin = pressure_twin(tmp_path, "bench_twin", _move_pc(BOILER))
    events = run(
        tmp_path, twin,
        [
            {"intent": "stoke_hard", "target": BOILER},
            {"intent": "move", "target": "loc_registry"},
            {"intent": "wait", "ticks": 3600},
        ],
        "bench",
        seed=43,
    )
    assert by_type(events, "pipes_knock")
    convenes = by_type(events, "the_bench_convenes")
    assert convenes and all(event.actor == "grp_regulators" for event in convenes)
    rations = [
        event
        for event in by_type(events, "account_transferred")
        if event.actor == KEEPER
    ]
    assert rations  # the measured release: four coal, never five
    for ration in rations:
        assert ration.outcome["amount"] == 4
        for change in ration.state_changes:
            if change.entity == KEEPER:
                assert change.prop == "account.coal"  # the reserve drains


def test_the_deadband_holds_below_the_bar(tmp_path: Path) -> None:
    """The vacuity law's quiet half: the crafted twin seeds the circle's
    cold BELOW the trigger AND parks the player at the firehole (the
    beats' walks roll — the draws consumed, the bar zero) — the goal
    never fires across a full day of beats (the deadband, churn-free
    by construction)."""
    twin = pressure_twin(
        tmp_path, "quiet_circle",
        {
            "entities.json": {
                "npcs": _merge_npc_patch(
                    _move_pc(BOILER), _seed_axes(
                        {"cold": 10}, ("npc_stoker_01", "npc_stoker_02")
                    )
                )["entities.json"]["npcs"],
            }
        },
    )
    events = run(
        tmp_path, twin, [{"intent": "wait", "ticks": 1500}], "deadband"
    )
    assert not by_type(events, "boiler_run_hard")


# -- (5) the read surface --------------------------------------------------------


def test_the_gauge_renders_one_live_line_and_no_meter_renders_the_debt() -> None:
    """The ONE meter (REFERENCES §10's DD/FP law): the firehole's scene
    line carries the LIVE pressure stock (integer truth below, one
    rendered line above) — and the thermometer minus holds: no marker,
    no scene field, no brief line anywhere names a seam, the debt, or
    a count of either; the debt renders only as its consequences."""
    events = load_golden()
    # at the firehole (after the move + the look): the gauge's line
    brief = render_brief(assemble_brief(events[:2], PACK))
    scene_lines = [
        line for line in brief.splitlines() if line.startswith("- scene")
    ]
    assert any(
        "account.pressure=40" in line and BOILER in line
        for line in scene_lines
    )
    # the thermometer minus: the whole rendered brief never speaks a
    # seam, a spot flag, or any prop of the debt's stock — the word may
    # ride the district's own prose (the lore and the voice carry the
    # metaphor), but no METER ever renders it (no prop, no number)
    for line in brief.splitlines():
        assert "seam" not in line and "thermal" not in line
        assert "shocked" not in line and "pipes_knock" not in line
    # the marker table: the felt axes only — no debt marker exists
    markers = PACK.rules["brief"]["present_entities"]["card_markers"]
    assert {spec["prop"] for spec in markers} == {"status.cold", "status.dread"}


# -- (6) T1 — determinism over the fifth pack ------------------------------------


def test_two_runs_are_byte_identical(tmp_path: Path) -> None:
    first = tmp_path / "a.jsonl"
    second = tmp_path / "b.jsonl"
    for name in (first, second):
        sim = Simulator(PACK, SCRIPT["seed"], name, SCHEMA, commit="0000000")
        sim.run_playscript(SCRIPT)
    assert first.read_bytes() == second.read_bytes()


def test_fresh_run_matches_committed_golden(tmp_path: Path) -> None:
    fresh = tmp_path / "fresh.jsonl"
    sim = Simulator(PACK, SCRIPT["seed"], fresh, SCHEMA, commit="0000000")
    result = sim.run_playscript(SCRIPT)
    assert fresh.read_bytes() == GOLDEN.read_bytes()
    assert result.fingerprint == 15  # the talk checks the run takes


def test_different_seed_diverges(tmp_path: Path) -> None:
    other = tmp_path / "other.jsonl"
    sim = Simulator(PACK, 43, other, SCHEMA, commit="0000000")
    sim.run_playscript(dict(SCRIPT, seed=43))
    assert other.read_bytes() != GOLDEN.read_bytes()


def test_committed_fixture_schema_version_matches_current_schema() -> None:
    header_line = GOLDEN.read_text(encoding="utf-8").splitlines()[0]
    header = json.loads(header_line)
    schema_id = SCHEMA.get("$id", "")
    assert header["schema_version"] == schema_id.rsplit("/", 1)[-1]


# -- helpers ---------------------------------------------------------------------


def load_golden() -> list[Any]:
    """The committed golden corpus (read once per call, assertion-safe)."""
    _, events = read_log(GOLDEN, SCHEMA)
    return events
