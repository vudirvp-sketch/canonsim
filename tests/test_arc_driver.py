"""iter-52 acceptance — the arc driver (content-6, D-081): arc-1's live
content set, the release-chain layer's first LIVE consumer. ZERO engine
edits — the whole driver is pack data: one successor hook (the barkeep's
wary sweep: trigger-less, climax-flagged, weight 0, seeded on the steal
failure, appended last) + the `aftermath` arc over
[possible_document_check_relief, barkeep_wary_sweep] with gap 2.

The design's load-bearing choices (DIRECTOR_SPEC §3d): the relief is
the FIRST member because it is the one hook live on the runs the driver
targets — the survey's measured fact: the relief is the ONLY tag that
releases on any committed run, so the order law never holds the
corpus-pinned release (the D-076 naive watcher-pair chaining refused:
it would park the pinned successor behind a predecessor that never
fires on seed 125). The GAP law is what defers the sweep from beat 720
to beat 1080 — one beat past the check's release — because the
UNCHAINED sweep would land its event BEFORE the check's own event
(t=733 vs t=734, the same-tick NPC_REACTION intent ordering): a second
beat landing before its predecessor is a causality lie in the canon,
and the march is the fix. The sweep is weight 0 so the landing shifts
no entropy floor on any run (the whole +W gate-flip class dead by
construction), and the successor seeds APPENDED LAST so the explicit
scan's buffer order can never steal the relief's budget slot.

Measured footprint (TEST_PLAN §6, iter-52): day1_full 9/10 seeds
byte-identical (the quiet seeds' steals succeed — no failure, no
seeding, no divergence at all); seed 125 gains exactly one event, the
sweep, appended after everything HEAD held; the corpus 105 stays
pin-green untouched (zero re-distill — the first content landing with
none; the 14 theft-failure cases diverge by the seeding event's own
hooks field, the birth record, zero broken pins).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")
DAY1 = load_playscript(REPO / "tests" / "playscripts" / "day1_full.json")

SWEEP_TAG = "barkeep_wary_sweep"


def run_day1(
    tmp_path: Path, pack: Any = PACK, seed: int = DAY1["seed"], label: str = "run"
) -> tuple[list[Any], Simulator, Any]:
    """The gate playscript (seed 125 by default, overridable for the
    quiet-seed arm) over the given pack."""
    script = dict(DAY1)
    script["seed"] = seed
    log = tmp_path / f"day1_{label}_{seed}.jsonl"
    if log.exists():
        log.unlink()
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    result = sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    return events, sim, result


def sweeps(events: list[Any]) -> list[Any]:
    """The barkeep's director-released look_around events."""
    return [
        e for e in events
        if e.type == "look_around" and e.actor == "npc_barkeep_01"
        and str(e.provenance.get("cause_intent", "")).startswith("director_")
    ]


def checks(events: list[Any]) -> list[Any]:
    return [e for e in events if e.type.startswith("document_check")]


def _variant_pack(
    tmp_path: Path,
    mutate_rules: Callable[[dict[str, Any]], None],
    mutate_actions: Callable[[dict[str, Any]], None] | None = None,
) -> Any:
    """A copy of the tavern pack with rules.json (and optionally
    actions.json) mutated and re-linted — the suite-local pattern from
    tests/test_director.py::_mutated_pack, grown the actions knob the
    seeding-side variants need."""
    target = tmp_path / "variant_pack"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    mutate_rules(rules)
    (target / "rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    if mutate_actions is not None:
        actions = json.loads((target / "actions.json").read_text(encoding="utf-8"))
        mutate_actions(actions)
        (target / "actions.json").write_text(
            json.dumps(actions, indent=2), encoding="utf-8"
        )
    return load_pack(target)


# -- the march: two releases, in order, with the gap ----------------------------


def test_the_march_releases_in_order_with_the_gap(tmp_path: Path) -> None:
    """The canonical day1_full run (seed 125, the only live stage): the
    relief's check releases first (the corpus pin untouched — director_0000,
    t=734), the barkeep's sweep second (director_0001) — and the sweep's
    event lands at t=1456, the day's LAST event, AFTER the check and after
    everything HEAD held (the append-only footprint: zero id shifts). The
    arc completes: the cursor sits past its members, and the sweep's
    release marks the day's closing beat (PEAK_CLIMAX — the denouement
    the clock already defines). The knowledge mint is the barkeep's scene
    snapshot: the room, taken stock."""
    events, sim, _ = run_day1(tmp_path)
    (check,) = checks(events)
    (sweep,) = sweeps(events)
    assert str(check.provenance["cause_intent"]) == "director_0000"
    assert check.t == 734 and check.actor == "npc_guard_02"
    assert str(sweep.provenance["cause_intent"]) == "director_0001"
    assert sweep.t == 1456
    # the canon order IS the declared causality: the sweep after the check
    assert sweep.id > check.id
    assert events[-1].id == sweep.id  # the day's last event, nothing after
    # the arc marched: beat 1 (the check) -> beat 3 (the sweep, gap 2 held
    # beat 720) — the cursor now past the chain's end
    assert sim.director._arc_cursor == {"aftermath": 2}  # type: ignore[attr-defined]
    # the sweep's release marked the day's closing beat (the climax path)
    assert sim.director.pacing is not None
    assert sim.director.pacing.state == "PEAK_CLIMAX"
    # the room, taken stock: the barkeep's own scene snapshot, exact
    assert [(k.who, k.knows, k.fidelity) for k in sweep.knowledge] == [
        ("npc_barkeep_01", "scene_loc_tavern", "exact")
    ]
    # the beat is log-visible, not tale-visible (the iter-51 scan
    # precedent: look_around stays below the tale gate — importance low)
    assert sweep.importance == "low"


# -- the gap law live: the load-bearing A/B -------------------------------------


def test_the_stripped_arc_inverts_the_canon_order(tmp_path: Path) -> None:
    """The A/B arm (TEST_PLAN §6): the same pack minus `director.arcs`
    (a linted variant — the pack's own declaration is the gate, INV-3).
    Without the chain the sweep still releases SECOND (director_0001,
    the relief wins beat 360's budget by buffer order) but at beat 720 —
    one beat past the check's release — and both intents ride the SAME
    entry tick (t=732), where the queue's actor_id tiebreak pops the
    barkeep BEFORE the relief guard: the sweep's event lands at t=733,
    BEFORE the check's own event at t=734. A second beat landing before
    its predecessor is a causality lie in the canon — the inversion the
    gap law exists to prevent (the committed run's march is the fix,
    pinned above)."""
    def mutate_rules(rules: dict[str, Any]) -> None:
        rules["director"].pop("arcs")

    pack = _variant_pack(tmp_path, mutate_rules)
    events, _, _ = run_day1(tmp_path, pack=pack)
    (check,) = checks(events)
    (sweep,) = sweeps(events)
    assert str(check.provenance["cause_intent"]) == "director_0000"
    assert str(sweep.provenance["cause_intent"]) == "director_0001"
    # the inversion, live: the sweep's event BEFORE the check's event
    assert sweep.t < check.t
    assert sweep.id < check.id
    # both intents rode the same entry tick; the actor tiebreak decided
    assert sweep.t == 733 and check.t == 734


# -- the order law live: the honest stall ----------------------------------------


def test_the_order_law_stalls_the_sweep_behind_a_dead_predecessor(
    tmp_path: Path,
) -> None:
    """The counterfactual pin (the D-076 e2e shape on the driver's own
    chain): with the relief fully defused — its band unreachable (the
    trigger value 500) AND its confrontation gate pointing where the
    relief never stands (the option place leaf redirected — the climax
    path consults the option gate, so a trigger-only defuse would not
    defuse the boss road) — the predecessor never releases, and the
    order law holds the sweep for the whole run: the successor is a
    candidate ONLY while it is its arc's current member. The sweep
    never fires; the day ends with zero director releases. The stall
    is honest (the world's causality broke the plan; the re-plan
    refinement stays recorded-not-built, DIRECTOR_SPEC §11)."""
    def mutate_rules(rules: dict[str, Any]) -> None:
        relief = rules["director"]["hooks"]["possible_document_check_relief"]
        relief["trigger"]["value"] = 500
        relief["options"][0]["trigger"][0]["location"] = "loc_market"

    pack = _variant_pack(tmp_path, mutate_rules)
    events, sim, _ = run_day1(tmp_path, pack=pack)
    assert sweeps(events) == []
    assert checks(events) == []
    director_events = [
        e for e in events
        if str(e.provenance.get("cause_intent", "")).startswith("director_")
    ]
    assert director_events == []
    # the chain parked at its first member: the cursor never advanced
    # (the lazy `.get` default IS the resting position 0)
    assert sim.director._arc_cursor.get("aftermath", 0) == 0  # type: ignore[attr-defined]


# -- the containment: no draws, no floors, no quiet-seed bytes --------------------


def test_the_sweep_adds_no_draws_the_fingerprint_identity(
    tmp_path: Path,
) -> None:
    """The stream containment (the D-080 fingerprint pattern): the sweep
    is RNG-free end to end — the director's choice draws nothing, the
    look_around action carries no opposed check and a fixed 1-tick
    duration. The committed run and the successor-stripped run (the
    hook + the arc + the seeding tag all removed — HEAD's shape) draw
    from identical stream positions: the RngBank fingerprints are EQUAL,
    and the log grows by exactly one event, appended at the end."""
    def mutate_rules(rules: dict[str, Any]) -> None:
        rules["director"].pop("arcs")
        rules["director"]["hooks"].pop(SWEEP_TAG)

    def mutate_actions(actions: dict[str, Any]) -> None:
        for item in actions["actions"]:
            if item["intent"] == "steal":
                item["hooks"]["failure"].remove(SWEEP_TAG)

    stripped = _variant_pack(tmp_path, mutate_rules, mutate_actions)
    live_events, _, live_result = run_day1(tmp_path, label="live")
    stripped_events, _, stripped_result = run_day1(
        tmp_path, pack=stripped, label="stripped"
    )
    assert live_result.fingerprint == stripped_result.fingerprint
    assert len(live_events) == len(stripped_events) + 1
    # every HEAD event keeps its id: the sweep rides after them all
    assert [e.id for e in live_events[:-1]] == [e.id for e in stripped_events]
    assert live_events[-1].id == "ev_0052"


def test_the_quiet_seeds_stay_byte_identical(tmp_path: Path) -> None:
    """The day1 A/B's quiet arm, pinned on a representative quiet seed
    (7): the steals succeed there — no failure event, no hooks seeded,
    the successor never enters the buffer — so the committed pack and
    the successor-stripped pack produce byte-IDENTICAL logs (not even
    the seeding record diverges). The landing's whole day1 footprint is
    the seed-125 geometry."""
    def mutate_rules(rules: dict[str, Any]) -> None:
        rules["director"].pop("arcs")
        rules["director"]["hooks"].pop(SWEEP_TAG)

    def mutate_actions(actions: dict[str, Any]) -> None:
        for item in actions["actions"]:
            if item["intent"] == "steal":
                item["hooks"]["failure"].remove(SWEEP_TAG)

    stripped = _variant_pack(tmp_path, mutate_rules, mutate_actions)
    live_events, _, _ = run_day1(tmp_path, seed=7, label="live")
    stripped_events, _, _ = run_day1(tmp_path, pack=stripped, seed=7, label="stripped")
    assert [(e.id, e.t, e.type) for e in live_events] == [
        (e.id, e.t, e.type) for e in stripped_events
    ]
    assert sweeps(live_events) == []


# -- the declarations -------------------------------------------------------------


def test_the_driver_declarations_are_live() -> None:
    """The landed content set: the successor hook's shape (trigger-less
    — the climax path is its only road; climax-flagged — the closing
    beat that ends the peak; weight 0 — a closing beat carries no
    tension, the entropy sensor never sees it; first_time_only — one
    reckoning per run) and the seeding side: the steal-failure hooks
    list carries the successor APPENDED LAST (the buffer order can
    never steal the relief's budget slot — the corpus pin's
    belt-and-suspenders)."""
    spec = PACK.rules["director"]["hooks"][SWEEP_TAG]
    assert spec.get("trigger") is None
    assert spec["climax"] is True
    assert spec["first_time_only"] is True
    assert spec["weight"] == 0
    assert spec["target_npc"] == "npc_barkeep_01"
    assert spec["intent"] == {"kind": "look_around"}
    assert spec["channel"] == "social"
    assert spec["release_threshold"] == 10
    steal = next(
        a for a in PACK.data["actions.json"]["actions"]
        if a["intent"] == "steal"
    )
    assert steal["hooks"]["failure"][-1] == SWEEP_TAG
    assert len(steal["hooks"]["failure"]) == 4
