"""content-3 / iter-53 — the ambient channel's live content set (D-082).

DIR-4's declared-but-dormant third dimension gains its live consumer:
the drunkard's ramble — the room's murmur, the L4D Music analog. The
hook carries the `ambient` channel, weight 0 (the inputless noise floor
as declared: the ambient entropy stays exactly 0, so no floor flips
anywhere — the +W gate-flip class dead by construction, the iter-52
law), trigger-less (the ambient quiet gate is its only road),
first_time_only (one murmur per run — the recurring variant is
recorded-not-built, DIRECTOR_SPEC §11).

The seeding side (D-005: seeded at event time, never improvised): idle
time itself — the wait action's success hooks list (the resolver minted
action hooks for the first time at iter-53; the minting was
resolver-sparse, the steal family only — a silent dead-data gap of the
KI#15 family, closed for the wait resolver by its first consumer).

The suite pins: the quiet march (the murmur returns on the first quiet
beat after an idle wait), the room-heard knowledge mint (the occupants
minus the actor — the rotation's absence honored), the chronicle line
(the tale-gated medium importance), the burn, the all-PEAK containment
(day1_full never goes quiet — the D-066 law), the mechanism isolation
(the seeding stripped → no murmur), the RNG containment (the
fingerprint identity), and the declarations.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack
from render.chronicle import render_chronicle

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK = load_pack(REPO / "content" / "tavern_pack")
DAY1 = json.loads((REPO / "tests" / "playscripts" / "day1_full.json").read_text())

TAG = "ambient_drunkard_ramble"

QUIET = {
    "name": "quiet",
    "seed": 42,
    "pack": "tavern_pack@0.1",
    "steps": [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "wait", "ticks": 360},
        {"intent": "wait", "ticks": 360},
        {"intent": "wait", "ticks": 360},
    ],
}


def run_script(
    tmp_path: Path,
    script: dict[str, Any],
    pack: Any = PACK,
    label: str = "run",
    director_enabled: bool = True,
) -> tuple[list[Any], Simulator, Any]:
    """One batch run over the given pack; returns (events, sim, result)."""
    script = dict(script)
    log = tmp_path / f"{label}_{script['seed']}.jsonl"
    if log.exists():
        log.unlink()
    sim = Simulator(
        PACK if pack is None else pack, script["seed"], log, SCHEMA,
        commit="0000000", director_enabled=director_enabled,
    )
    result = sim.run_playscript(script)
    _, events = read_log(log, SCHEMA)
    return events, sim, result


def rambles(events: list[Any]) -> list[Any]:
    """The drunkard's director-released ambient beats."""
    return [
        e for e in events
        if e.type == "ramble"
        and str(e.provenance.get("cause_intent", "")).startswith("director_")
    ]


def _variant_pack(
    tmp_path: Path,
    mutate_rules: Callable[[dict[str, Any]], None],
    mutate_actions: Callable[[dict[str, Any]], None] | None = None,
) -> Any:
    """A copy of the tavern pack with rules.json (and optionally
    actions.json) mutated and re-linted — the suite-local pattern from
    tests/test_arc_driver.py::_variant_pack."""
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


# -- the march: the murmur returns on the first quiet beat ----------------------


def test_the_quiet_march_releases_the_murmur(tmp_path: Path) -> None:
    """A world walked into quiet (the D-066 protocol question, answered
    by the row's own stage): the arrival, then idle time. The first wait
    completes AFTER beat 360 — the tag enters the buffer behind the
    beat it missed (the seeding is the wait event, its own completion
    tick; nothing retro-seeds). Beat 720 is the first quiet window the
    tag can see: STAGNATION (entropy 0 — no suspicion, no fire, no
    other tension), the ambient channel's own floor the only gate left
    (0 < 2). The murmur releases: director_0000, the drunkard's ramble
    at t=725 (the intent enqueued at the beat, 3 ticks of rambling).
    The room hears — the occupants minus the actor, the outgoing guard
    honestly absent (the t=360 rotation moved him to the guardroom).
    Beat 1080 stays silent: the tag burned (first_time_only)."""
    events, sim, _ = run_script(tmp_path, QUIET)
    waits = [e for e in events if e.type == "wait"]
    assert all(TAG in e.hooks for e in waits)
    assert [e.t for e in waits] == [362, 722, 1082]
    (ramble,) = rambles(events)
    assert ramble.id == "ev_0016"
    assert ramble.t == 725
    assert ramble.actor == "npc_drunk_01"
    assert str(ramble.provenance["cause_intent"]) == "director_0000"
    # the murmur rides the door: the observe resolver, the pack's
    # knowledge templates, no check, no state change
    assert ramble.outcome["duration"] == 3
    assert not ramble.state_changes
    assert ramble.importance == "medium"  # story-critical: tale-gated
    assert [(k.who, k.channel, k.fidelity, k.knows) for k in ramble.knowledge] == [
        ("pc_01", "heard", "vague", "rambling_by_npc_drunk_01"),
        ("npc_guard_02", "heard", "vague", "rambling_by_npc_drunk_01"),
        ("npc_barkeep_01", "heard", "vague", "rambling_by_npc_drunk_01"),
        ("npc_maid_01", "heard", "vague", "rambling_by_npc_drunk_01"),
    ]
    # the burn: one murmur per run — beat 1080 stays silent
    assert len(rambles(events)) == 1
    # the beat's release marked nothing: the clock ends the run quiet
    assert sim.director.pacing is not None
    assert sim.director.pacing.state == "STAGNATION"


def test_the_chronicle_line_renders_the_murmur(tmp_path: Path) -> None:
    """The tale carries the murmur: the ramble's own template line, in
    log order between the watch changes (the ambient beat is a real
    chronicle line, not a hidden log event — the story-critical entry
    is what lifts it over the tale gate)."""
    events, _, _ = run_script(tmp_path, QUIET)
    tale = render_chronicle(events, PACK, QUIET["seed"])
    lines = tale.splitlines()
    murmur = [ln for ln in lines if "rambles" in ln]
    assert murmur == ["the drunkard rambles to no one in particular."]
    # in log order: after the day's first watch change, before the second
    assert lines.index(murmur[0]) > lines.index(
        "The watch changes: Doren hands the post to the relief guard."
    )
    assert lines.index(murmur[0]) < lines.index(
        "The watch changes: the relief guard hands the post to Doren."
    )


# -- the containment laws --------------------------------------------------------


def test_directors_off_stays_silent(tmp_path: Path) -> None:
    """The T8-family arm: a disabled director never consults a channel —
    the murmur is a director release, so the OFF run keeps zero rambles
    (the wait events still seed the tag; the buffer just never drains)."""
    events, _, _ = run_script(
        tmp_path, QUIET, label="off", director_enabled=False
    )
    assert rambles(events) == []
    waits = [e for e in events if e.type == "wait"]
    assert all(TAG in e.hooks for e in waits)


def test_day1_full_stays_silent_the_all_peak_law(tmp_path: Path) -> None:
    """The committed stage never gives the murmur a window (the D-066
    finding, now the ambient row's own containment pin): day1_full ends
    in PEAK on every seed — the quiet path is suppressed at every beat
    (seed 125: the loud geometry, suspicion ≥ 100 from the double steal
    failure; the whole ambient footprint on day1_full is the wait
    events' hooks field, the birth record — zero appended events, the
    iter-52 zero-regen shape)."""
    events, _, _ = run_script(tmp_path, DAY1, label="day1")
    assert rambles(events) == []
    assert events[-1].type == "look_around"  # the sweep stays the closer
    assert all(TAG in e.hooks for e in events if e.type == "wait")


def test_the_stripped_seeding_isolates_the_mechanism(tmp_path: Path) -> None:
    """The probe family (the iter-46/51 pattern — mechanism isolation):
    the same pack with the wait action's success hooks emptied (the
    seeding side removed, the hook declaration kept) never releases the
    murmur on the quiet stage — the release is seeded by idle time, not
    by the declaration alone (D-005: a complication from nowhere is a
    bug; without the seed there is no consequence)."""
    def mutate_actions(actions: dict[str, Any]) -> None:
        for item in actions["actions"]:
            if item["intent"] == "wait":
                item["hooks"]["success"] = []

    pack = _variant_pack(tmp_path, lambda rules: None, mutate_actions)
    events, _, _ = run_script(tmp_path, QUIET, pack=pack, label="stripped")
    assert rambles(events) == []
    waits = [e for e in events if e.type == "wait"]
    assert all(e.hooks == () for e in waits)


def test_the_weight_zero_footprint_the_fingerprint_identity(
    tmp_path: Path,
) -> None:
    """The RNG containment (the D-080/D-081 fingerprint pattern): the
    murmur is draw-free end to end — the ambient hook carries no rolls
    (weight 0, no check, the director's quiet-path pick deterministic),
    the ramble action runs no opposed check, the knowledge mint is pure
    audience expansion, and the rotation's transfer of the heard record
    is the deterministic briefing machinery. The committed quiet run
    and the landing-stripped run (the director hook + the seeding tag
    removed — HEAD's shape) draw from identical stream positions: the
    RngBank fingerprints are EQUAL. The log delta is exactly two
    events, both honest downstream of the murmur: the ramble itself
    (t=725, mid-run — the tail ids shift) and the evening guard's
    knowledge_transfer at the t=1080 rotation — the heard record
    crossing the watch change (the world's own ripple: the briefing
    mentions the drunkard's rambling; a guard with nothing novel
    briefs nothing, the stripped arm's shape)."""
    def mutate_rules(rules: dict[str, Any]) -> None:
        rules["director"]["hooks"].pop(TAG)

    def mutate_actions(actions: dict[str, Any]) -> None:
        for item in actions["actions"]:
            if item["intent"] == "wait":
                item["hooks"]["success"] = []

    stripped = _variant_pack(tmp_path, mutate_rules, mutate_actions)
    live_events, _, live_result = run_script(
        tmp_path, QUIET, pack=PACK, label="live"
    )
    stripped_events, _, stripped_result = run_script(
        tmp_path, QUIET, pack=stripped, label="fp"
    )
    assert live_result.fingerprint == stripped_result.fingerprint
    # the pre-murmur prefix is identical; the murmur lands mid-run
    assert [e.id for e in live_events[:16]] == [e.id for e in stripped_events[:16]]
    murmur = live_events[16]
    assert murmur.type == "ramble" and murmur.t == 725
    # the tail is content-identical except ONE extra event: the heard
    # record crossing the watch change (guard_02's briefing)
    live_tail = [(e.t, e.type, e.actor) for e in live_events[17:]]
    stripped_tail = [(e.t, e.type, e.actor) for e in stripped_events[16:]]
    assert live_tail[:1] == stripped_tail[:1]  # the watch change
    assert live_tail[1] == (1080, "knowledge_transfer", "npc_guard_02")
    assert live_tail[2:] == stripped_tail[1:]
    assert len(live_events) == len(stripped_events) + 2


# -- the declarations -------------------------------------------------------------


def test_the_driver_declarations_are_live() -> None:
    """The landed content set: the ambient hook's shape (channel ambient
    — the declared dimension carried at last; weight 0 — the inputless
    noise floor keeps the ambient entropy exactly 0, no floor can flip;
    trigger-less — the quiet path is its only road; first_time_only —
    one murmur per run; the drunkard — the room's own noise source) and
    the seeding side: the wait action's success hooks list carries the
    tag (idle time is the murmur's seed). The ramble action: the 16th,
    over the observe resolver, the room-heard knowledge template, its
    own event type (the chronicle line's carrier), story-critical (the
    tale gate's lift)."""
    spec = PACK.rules["director"]["hooks"][TAG]
    assert spec.get("trigger") is None
    assert spec.get("climax") is None
    assert spec["channel"] == "ambient"
    assert spec["weight"] == 0
    assert spec["first_time_only"] is True
    assert spec["target_npc"] == "npc_drunk_01"
    assert spec["intent"] == {"kind": "ramble"}
    assert spec["release_threshold"] == 10
    wait = next(
        a for a in PACK.data["actions.json"]["actions"]
        if a["intent"] == "wait"
    )
    assert wait["hooks"]["success"] == [TAG]
    assert wait["hooks"]["failure"] == []
    ramble = next(
        a for a in PACK.data["actions.json"]["actions"]
        if a["intent"] == "ramble"
    )
    assert ramble["resolver"] == "observe"
    assert ramble["ticks"] == 3
    assert ramble["check"] is None
    assert ramble["events"] == {"success": "ramble"}
    assert ramble["hooks"] == {"success": [], "failure": []}
    assert ramble["knowledge"]["success"] == [
        {
            "who": "same_location",
            "except": ["actor"],
            "channel": "heard",
            "fidelity": "vague",
            "knows": "rambling_by_{actor}",
        }
    ]
    assert "ramble" in PACK.rules["importance"]["story_critical_events"]
    assert PACK.templates["events"]["ramble"] == (
        "{actor} rambles to no one in particular."
    )
