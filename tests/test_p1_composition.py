"""P1-1 — the Province integrated composition witness (iter-261, the
owner's «prove composition» call over the parked intake-40 P1 set:
phases.md §6's routing — P1-1 behind the owner's explicit call, P1-10
temp-1's half (b) test arm).

The witness: ONE run (province_pack@0.1, seed 2,
`tests/playscripts/province_composition.json` — the factor's runner
takes the lamp, burns the keep's hearth, walks to Malby, fails to lift
the duty sergeant's pay tin, waits, burns the market's stall row, then
idles through the year at Malby) walking the interacting causal chains
END-TO-END over the committed substrate — zero new content, existing
verbs only:

- **the crime family** (Loop A's mechanism family, the anti-double-count
  ruling): the failed steal → the witnessed knowledge mint → the
  leverage clusters (the sergeant's and the market mistress's) → the
  suspicion axis (25+10, PC `suspect`) → the WATCH ROTATION's briefing
  spreading the sergeant's whole stack to the relief (the corporal, who
  never co-located with any of the PC's acts) → the institutional
  `document_check` (the sergeant's own urgency_0001, the levy bending)
  → the waybill crossing the arrest bar (75) while co-located → the
  arrest attempt → `caught`, irreversible — plus the relief hook's own
  check (the director's `possible_manifest_check_relief` arm at t=4680).
- **Loop A (fire → institutional response), the guild arm**: the market
  arson → `fire_started` → `alarm_raised` (the mistress's fear 0→40)
  → `panic_ripple` (+10 through the walls) → `guild_councils` through
  the front door (actor = the group id, `faction_0000`).
- **Loop B (feud residue → present politics)**: the keep fire wakes
  Garrick (grievance 30→50, the numeric-home law), the market fire
  wakes Wilmot (35→55) → both elders past the bar → the deadband opens
  → `wergeld_vigil` (faction_0001) — and the grievance's decay-0 law
  holds it a YEAR: the vigil re-fires at t=525335 off the residue
  minted at t=606/3453 (the persistence→future-option oracle).
- **Loop C (season → weather → social signal)**: the year turns the
  whole calendar — 36 markets, 12 fairs, the four seasons in cycle
  order, one year turn (151), the seasonal weather ride (3 rolls, the
  no-op roll suppressed once; the thaw's roll draws storm).
- **the macro economy (Loop E/H's armed flow half)**: the year turn
  sources the four account flows (the toll nets, the guild collects,
  the bloom nets, the withhold banks).
- **Loop D + the ambient band**: the road condenses at the first beat
  (the born names), the watch rotates 730 times with 5 briefings, the
  mistress talks 287 times (urgency_0004, the trust gate), the crowd
  wares 7 times, 22 rumors walk.

The honest gaps (classified per the §14 law, never "a scheduler
problem"): the GARRISON arm (fear → `garrison_patrols`) and the storm
MURMUR (weather → hook → the mistress's ramble) do not fire on this
seed's windows — both are COMMITTED-proven at their own witnesses
(`tests/test_triangle.py` seed 139; `tests/test_weather.py` the
storm-seeds-the-director's-buffer family) — a witness-window
limitation, never a missing mechanic. The scene LOD (depth-3) scopes
the beat machinery to the active zone (the warm ring at the macro
crossings): the weirstair/crofts NPCs never roll on this route —
structural, by design.

The oracles are RELATIONS (the §12 law — no giant golden world log):
cause exists → consequence exists; residue persists → future option
changes; assignment → the semantic origin stays observable; realization
→ the canonical event stays deterministic (the byte-identical twin).
The measured surface (counts, ticks, latencies) is pinned as numbers —
re-pin only together with the explaining change.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.fold import fold, initial_projection
from core.log import EventRecord, read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PROVINCE = load_pack(REPO / "content" / "province_pack")
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "province_composition.json")

#: The measured surface at HEAD (iter-261): the run's own numbers.
#: Re-pin only together with a legitimate pack or engine change that
#: explains the move.
EVENT_COUNT: int = 2371
AUTONOMOUS_RESOLUTIONS: int = 383  # 382 accepted + 1 rejected
TALK_COUNT: int = 287
VIGIL_COUNT: int = 4


def _is_autonomous(event: EventRecord) -> bool:
    """Whether the event resolves an AUTONOMOUS intent (B3's scope)."""
    return str(event.provenance.get("cause_intent", "")).startswith(
        ("urgency_", "faction_", "director_")
    )


@pytest.fixture(scope="module")
def witness(tmp_path_factory: pytest.TempPathFactory) -> tuple[list[EventRecord], Any]:
    """The composition run, once per module: (events, run result)."""
    log = tmp_path_factory.mktemp("p1") / "composition.jsonl"
    sim = Simulator(PROVINCE, SCRIPT["seed"], log, SCHEMA, commit="0000000")
    result = sim.run_playscript(SCRIPT)
    sim.close()
    _header, events = read_log(log, SCHEMA)
    return events, result


def _of(events: list[EventRecord], *types: str) -> list[EventRecord]:
    return [e for e in events if e.type in types]


def _changes(event: EventRecord) -> dict[tuple[str, str], tuple[Any, Any]]:
    return {(c.entity, c.prop): (c.from_, c.to_) for c in event.state_changes}


# -- chain 1: the crime family end-to-end -------------------------------------


def test_the_theft_failure_mints_knowledge_leverage_and_suspicion(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The chain's first leg: the failed steal of the sergeant's pay tin
    is a FACT (a `pickpocket_failed` event, cause-chained), and the
    world answers on three subsystems at once — the witnessed knowledge
    mint (`figure_reaching_for_tin`, the sergeant AND the mistress),
    the leverage economy (a cluster over the PC for each novel knower),
    and the crime axis (suspicion +25 / noise +10, the PC `suspect`:
    the status flips at the declared 25 bar)."""
    events, _ = witness
    steal = _of(events, "pickpocket_failed")
    assert len(steal) == 1 and steal[0].actor == "pc_01"
    assert steal[0].target == "npc_sergeant_01"
    minted = _of(events, "leverage_gained")
    holders = {e.actor: e.t for e in minted}
    assert set(holders) == {
        "npc_sergeant_01", "npc_marketmistress_01", "npc_corporal_01",
    }, (
        "the theft sighting must mint a cluster for each NOVEL knower: "
        "the two co-located witnesses at the theft tick, the relief at "
        "the briefing tick (the transfer's own mint)"
    )
    assert holders["npc_corporal_01"] > holders["npc_sergeant_01"]
    suspicion = [
        e for e in _of(events, "suspicion_changed")
        if e.actor == "npc_sergeant_01" and e.t == steal[0].t
    ]
    by_source = {e.outcome["source"]: e.outcome["to"] for e in suspicion}
    assert by_source["witnessed_steal_failure"] == 55  # 30 (the arson) + 25
    assert by_source["heard_noise"] == 65  # +10 the stalls' noise
    status = next(
        e for e in _of(events, "suspicion_changed")
        if ("pc_01", "crime_status") in _changes(e)
    )
    assert _changes(status)[("pc_01", "crime_status")][1] == "suspect"


def test_the_watch_rotation_briefing_spreads_the_whole_stack(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The institution's memory: the rotation's `knowledge_transfer`
    (the sergeant briefing his relief) carries the ENTIRE suspicion
    stack to the corporal — witnessed arson (30), the theft sighting
    (25), the noise (10) — in one tick, from one cause event. The
    corporal never co-locates with any of the PC's acts: his suspicion
    is purely institutional, the briefing is its only source."""
    events, _ = witness
    briefing = next(
        e for e in _of(events, "knowledge_transfer")
        if e.actor == "npc_sergeant_01" and e.target == "npc_corporal_01"
    )
    spread = [
        e for e in _of(events, "suspicion_changed")
        if e.actor == "npc_corporal_01" and e.cause == briefing.id
    ]
    by_source = {e.outcome["source"]: e.outcome["to"] for e in spread}
    assert by_source == {
        "witnessed_arson": 30,
        "witnessed_steal_failure": 55,
        "heard_noise": 65,
    }, "the briefing must carry the whole stack in one cause-chained tick"


def test_the_institutional_check_consumes_the_suspicion_and_arrests(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The chain's closing leg: the sergeant's own urgency
    (`document_check`, urgency_0001 — the levy bending for whoever
    feeds it) realizes as an accepted check, the waybill knowledge
    crosses the arrest bar (75) WHILE co-located, the arrest attempt
    follows in the same tick, and the resolution writes the terminal
    `caught` status — irreversible (a later re-arrest is idempotent,
    the KI#13 discipline). The relief hook's own check arm fires too
    (the director's manifest hook at t=4680) — two arms, one door."""
    events, _ = witness
    checks = _of(events, "document_check")
    assert checks and all(c.actor == "npc_sergeant_01" for c in checks)
    assert checks[0].provenance["cause_intent"] == "urgency_0001"
    assert checks[0].provenance["assignment_tick"] < checks[0].t
    waybill = [
        e for e in _of(events, "suspicion_changed")
        if e.outcome.get("source") == "waybill_unsatisfactory"
        and e.actor == "npc_sergeant_01"
    ]
    assert waybill and waybill[0].outcome["to"] >= 75, (
        "the waybill leg must cross the arrest bar (75) on the sergeant"
    )
    attempt = _of(events, "arrest_attempt")
    assert len(attempt) == 1 and attempt[0].actor == "npc_sergeant_01"
    assert attempt[0].t == waybill[0].t, "the attempt rides the crossing tick"
    resolved = _of(events, "arrest_resolved")
    assert len(resolved) == 1
    assert _changes(resolved[0])[("pc_01", "crime_status")] == (
        "suspect", "caught",
    )
    relief_waybill = [
        e for e in _of(events, "suspicion_changed")
        if e.outcome.get("source") == "waybill_unsatisfactory"
        and e.actor == "npc_corporal_01"
    ]
    assert relief_waybill, "the relief hook's own check arm must fire"


# -- chain 2: the fire loops (A's guild arm + B's vigil) ----------------------


def test_the_keep_fire_wakes_one_elder_and_spikes_the_watch(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The keep road: the arson ignites the hearth, the alarm spikes
    the co-located sergeant's fear (0→40, the garrison's own trained
    bar), the panic ripples through the walls (+10), and the grief
    wakes GARRICK alone (30→50, the numeric-home law — the crofts hear
    the keep). The burned-out residue is irreversible."""
    events, _ = witness
    fire = _of(events, "fire_started")
    assert {f.target for f in fire} == {"loc_keep", "loc_malby"}
    keep_alarm = next(a for a in _of(events, "alarm_raised") if a.target == "loc_keep")
    assert ("npc_sergeant_01", "status.fear") in _changes(keep_alarm)
    grief = _of(events, "grief_wakes")
    by_target = {g.target: _changes(g) for g in grief}
    assert by_target["loc_keep"] == {("npc_smelter_01", "status.grievance"): (30, 50)}
    assert by_target["loc_malby"] == {("npc_steward_01", "status.grievance"): (35, 55)}
    burnouts = _of(events, "location_burned_out")
    assert {b.target for b in burnouts} == {"loc_keep", "loc_malby"}
    assert all(
        _changes(b)[(b.target, "destroyed")] == (None, True) for b in burnouts
    )


def test_the_market_fire_tips_the_guild(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """Loop A's guild arm through the door: the market alarm spikes the
    mistress past the guild's fear bar (30), and the GUILD COUNCILS as
    the group entity (`faction_0000`, D-112's one-id law) — the
    autonomous collective riding the same intent door as everything
    else."""
    events, _ = witness
    councils = _of(events, "guild_councils")
    assert len(councils) == 1
    assert councils[0].actor == "grp_river_guild"
    assert councils[0].provenance["cause_intent"] == "faction_0000"
    assert councils[0].provenance["assignment_tick"] < councils[0].t


def test_both_fires_open_the_families_deadband(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """Loop B's consummation: BOTH elders grieve past the bar (the
    fraction reads 100, the deadband opens) and the OLD FAMILIES hold
    the wergeld vigil — the faction's autonomous act, twice-armed by
    the two fires' residues."""
    events, _ = witness
    vigils = _of(events, "wergeld_vigil")
    assert len(vigils) == VIGIL_COUNT
    assert all(v.actor == "grp_old_families" for v in vigils)
    assert all(
        v.provenance["cause_intent"] == "faction_0001" for v in vigils
    )


# -- chain 3: the calendar year (Loop C) + the macro economy -------------------


def test_the_year_turns_the_whole_calendar_with_the_ride(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The composed year (the F3 form over this run): 36 market days,
    12 fairs, the four seasons in cycle order at days 90/180/270/360,
    one year turn (151 — the chronicle binding), the seasonal weather
    ride (3 rolls — the long-light's no-op roll suppresses its event;
    the thaw's roll draws STORM). The co-occurrence at the rise: the
    season crossing FIRST, then its weather roll, then the market —
    the coarsest-first discipline."""
    events, _ = witness
    assert len(_of(events, "market_opens")) == 36
    assert len(_of(events, "fair_opens")) == 12
    seasons = [e for e in events if e.outcome.get("calendar") == "seasons"]
    assert [e.outcome["phase"] for e in seasons] == [
        "high_water", "long_light", "first_frost", "thaw",
    ]
    assert [e.outcome["day"] for e in seasons] == [90, 180, 270, 360]
    year = _of(events, "year_turns")
    assert len(year) == 1 and year[0].outcome["year"] == 151
    rides = _of(events, "weather_turns")
    assert [r.outcome["weather"] for r in rides] == [
        "overcast", "clear", "storm",
    ]
    at_90 = [e.type for e in events if e.t == 129600]
    assert at_90[:3] == ["high_water_rises", "weather_turns", "fair_opens"]


def test_the_macro_year_feeds_the_account_flows(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """Loop E/H's armed flow half rides the macro crossing: the year
    turn sources the four declared account flows (the toll nets, the
    guild collects, the bloom nets, the withhold banks) — the debt-1
    substrate answering the calendar's own clock, one tick, four
    flows."""
    events, _ = witness
    sourced = _of(events, "account_sourced")
    flows = {e.outcome["flow"] for e in sourced}
    assert flows == {
        "the_toll_nets", "the_guild_collects",
        "the_bloom_nets", "the_withhold_banks",
    }
    assert all(e.t == _of(events, "year_turns")[0].t for e in sourced)


# -- chain 4: the ambient band (Loop D + the urgencies) ------------------------


def test_the_road_condenses_at_the_first_beat(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """Loop D: the road traffic condenses at the FIRST beat (the
    load-state origin law — the PC walks into a materialized world),
    the three members' names born on their own streams, the group's
    condensed flag the canon birth."""
    events, _ = witness
    muster = _of(events, "road_musters")
    assert len(muster) == 1 and muster[0].actor == "grp_road_traffic"
    changes = _changes(muster[0])
    assert changes[("grp_road_traffic", "condensed")] == (None, True)
    born = [c for c in muster[0].state_changes if c.prop == "name"]
    assert len(born) == 3, "the three travelers' names must be born"


def test_the_world_stays_causally_loud_through_the_year(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The declared-pressure oracle (§13's first candidate): through
    the 519000-tick idle the world is NEVER causally silent — the
    mistress's trust-gated talk urgency alone realizes 287 times, the
    watch rotates 730 times with 5 briefings, 22 rumors walk, and the
    run's total shape is the measured 2371 events. The urgency families
    that stay silent on this route are the LOD's structural scoping
    (the weirstair/crofts NPCs never enter the ticking zones), never
    spurious silence."""
    events, result = witness
    assert result.event_count == EVENT_COUNT
    talks = _of(events, "talk")
    assert len(talks) == TALK_COUNT
    assert all(t.actor == "npc_marketmistress_01" for t in talks)
    assert all(
        t.provenance["cause_intent"] == "urgency_0004" for t in talks
    )
    assert len(_of(events, "watch_change")) == 730
    assert len(_of(events, "knowledge_transfer")) == 5
    assert len(_of(events, "rumor_told")) == 22


# -- the persistence oracles (§12's relations) ---------------------------------


def test_persistent_residue_feeds_a_future_faction_event(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """THE persistence→future-option relation: the elders' grievance
    (decay 0 — a man-price once named stays named) minted by the two
    fires at t=606/3453 feeds a faction event A FULL YEAR LATER — the
    vigil at t=525335 rides the same residue, the living memory the
    circuit's own state."""
    events, _ = witness
    vigils = sorted(_of(events, "wergeld_vigil"), key=lambda e: e.t)
    first, last = vigils[0], vigils[-1]
    assert last.t - first.t > 518000, (
        "the last vigil must ride the year-old residue, not a fresh spike"
    )
    grief_ticks = [e.t for e in _of(events, "grief_wakes")]
    assert last.t - max(grief_ticks) > 518000


def test_the_final_projection_carries_the_persistent_deltas(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The end-state relations: the caught status persists (irreversible),
    both burned locations stay destroyed, the elders' grievance holds
    (50/55 — decay 0), and the watchers' suspicion stacks persist at
    100/90 — the run's residues survive the whole year of churn (the
    long-wait oracle: waiting never erases a declared persistent
    consequence)."""
    events, _ = witness
    projection = fold(events, initial_projection(PROVINCE.entities))
    assert projection["pc_01"]["crime_status"] == "caught"
    assert projection["loc_keep"]["destroyed"] is True
    assert projection["loc_malby"]["destroyed"] is True
    assert projection["npc_smelter_01"]["status.grievance"] == 50
    assert projection["npc_steward_01"]["status.grievance"] == 55
    assert projection["npc_sergeant_01"]["pair.pc_01.suspicion"] == 100
    assert projection["npc_corporal_01"]["pair.pc_01.suspicion"] == 90


# -- the timing oracles (P1-10, temp-1's half (b) over THIS witness) -----------


def test_every_autonomous_resolution_carries_both_times(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The B3 discipline over the composition corpus: EVERY autonomous
    resolution (accepted and rejected alike) carries `assignment_tick`
    with origin ≤ realization; the measured surface is 383 resolutions
    — and no player or world event ever carries the field (the field
    is the autonomous door's own)."""
    events, _ = witness
    autonomous = [e for e in events if _is_autonomous(e)]
    assert len(autonomous) == AUTONOMOUS_RESOLUTIONS
    for event in autonomous:
        assert "assignment_tick" in event.provenance
        assert event.provenance["assignment_tick"] <= event.t
    for event in events:
        if not _is_autonomous(event):
            assert "assignment_tick" not in event.provenance


def test_the_deferral_latency_surface(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The two-times surface over the integrated run: every autonomous
    resolution is deferred (min latency 7 — the door+duration floor,
    never zero), the max is the year-scale 518861, and the talks' real
    origins span the whole year [1800, 523440] while their realizations
    pile into the landing windows — the B2 clustering, now measured on
    a composition run, not just the stress witness."""
    events, _ = witness
    latencies = [
        e.t - e.provenance["assignment_tick"]
        for e in events if _is_autonomous(e)
    ]
    assert min(latencies) == 7
    assert max(latencies) == 518861
    talks = _of(events, "talk")
    origins = [t.provenance["assignment_tick"] for t in talks]
    assert (min(origins), max(origins)) == (1800, 523440)


def test_the_occ_miss_is_a_recorded_fact(
    witness: tuple[list[EventRecord], Any],
) -> None:
    """The material H1 instance on this corpus: the ONE autonomous
    rejection — a director release (the manifest-check family) minted
    at the beat t=2520 whose door landed at t=3449, 929 ticks later —
    the deferral window is where the precondition broke (the duty
    rotation moved the sergeant off-stage). The rejection carries BOTH
    times: a minted-and-doomed fact, exactly the OCC miss the two-times
    record makes inspectable."""
    events, _ = witness
    rejected = [
        e for e in _of(events, "intent_rejected") if _is_autonomous(e)
    ]
    assert len(rejected) == 1
    miss = rejected[0]
    assert miss.provenance["cause_intent"] == "director_0001"
    assert miss.provenance["assignment_tick"] == 2520
    assert miss.t == 3449
    assert miss.t - miss.provenance["assignment_tick"] == 929


# -- the determinism + scope pins ----------------------------------------------


def test_the_twin_run_is_byte_identical(tmp_path: Path) -> None:
    """INV-2 over the integrated run: the twin run is byte-identical on
    the same environment (T1's form — a determinism pin, never a
    committed golden snapshot; the oracles above are the relations)."""
    twin = tmp_path / "twin.jsonl"
    sim = Simulator(PROVINCE, SCRIPT["seed"], twin, SCHEMA, commit="0000000")
    sim.run_playscript(SCRIPT)
    sim.close()
    primary = tmp_path / "primary.jsonl"
    sim = Simulator(PROVINCE, SCRIPT["seed"], primary, SCHEMA, commit="0000000")
    sim.run_playscript(SCRIPT)
    sim.close()
    assert twin.read_bytes() == primary.read_bytes()
