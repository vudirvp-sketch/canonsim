"""mech-1 acceptance — the mechanics introspection CLI (iter-84, D-118).

The shadow-replay exactness pin is the core guarantee: `shadow_replay`
drives the REAL Director over a log's events and beats, and INV-2 makes
its decisions equal the runtime's own. The pin: the shadow's release ids
must equal the log's director-intent events (provenance.cause_intent with
the director prefix) on the canonical day1_full run — plus the STATUS
pins (the relief's check commits at t=734; the sweep at t=1456 is the
day's last event). The static half pins the wiring matrix and the
future-layer fallback: an unknown rules block must LOAD (lint passes) and
appear in the unindexed listing — a new layer is visible the iteration it
lands, never a rewrite.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import mechanics  # type: ignore[import-not-found]  # noqa: E402

from core.log import read_log  # noqa: E402
from core.loop import Simulator, load_playscript  # noqa: E402
from core.pack import load_pack  # noqa: E402

PACK_DIR = REPO / "content" / "tavern_pack"
PACK = load_pack(PACK_DIR)
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
DAY1 = REPO / "tests" / "playscripts" / "day1_full.json"


def _run_day1(tmp_path: Path) -> list:
    """The canonical run in an isolated gitignored-style tmp dir."""
    log = tmp_path / "day1.jsonl"
    sim = Simulator(PACK, 125, log, SCHEMA, commit="0000000")
    sim.run_playscript(load_playscript(DAY1))
    _, events = read_log(log, SCHEMA)
    return list(events)


# -- the static half ----------------------------------------------------------


def test_matrix_hook_declaration() -> None:
    """One hook's full wiring: trigger, gates, payload, seeders, arc."""
    out = mechanics.render_matrix(PACK, hook="possible_document_check")
    assert "hook possible_document_check" in out
    assert "pair.pc_01.suspicion >= 50" in out  # the band's single owner
    assert "channel threat" in out
    assert "first_time_only" in out
    assert "document_check -> pc_01 by npc_guard_01" in out
    assert "steal.failure" in out  # seeded by the theft's failure hooks list


def test_matrix_event_wiring() -> None:
    """One event type's consumers: producers, crime mapping, hook seeds."""
    out = mechanics.render_matrix(PACK, event="pickpocket_failed")
    assert "produced_by  steal.failure" in out
    assert (
        "figure_reaching_for_purse -> witnessed_steal_failure +25" in out
    )
    assert "possible_document_check_relief" in out
    assert "guard_suspicious_of_pc" in out


def test_matrix_token_and_prop_queries() -> None:
    """The reverse queries: a token's owners and a prop's readers."""
    token = mechanics.render_matrix(PACK, token="figure_reaching_for_purse")
    assert "source witnessed_steal_failure" in token
    assert "fades_ticks" in token  # the echo valence table
    prop = mechanics.render_matrix(PACK, prop="pair.pc_01.suspicion")
    assert "hook possible_document_check (trigger/gate/modifier)" in prop
    assert "on_action document_check (state)" in prop


def test_matrix_unknown_block_is_listed_not_rejected(tmp_path: Path) -> None:
    """The future-layer law: a new top-level rules block loads (the pack
    lint passes) and appears in the unindexed listing — visible the
    iteration it lands; a shape rule joins later, never a rewrite.
    depth-6 note: this test's placeholder WAS `factions` — the block
    became real (the closed vocabulary landed with it), so the probe
    moved to the next still-unknown name, exactly the law's own
    lifecycle."""
    variant_dir = tmp_path / "pack_variant"
    variant_dir.mkdir()
    for name in ("actions.json", "entities.json", "templates.json"):
        shutil.copyfile(PACK_DIR / name, variant_dir / name)
    rules = json.loads((PACK_DIR / "rules.json").read_text(encoding="utf-8"))
    rules["guilds"] = {"houses": {"house_01": {"honor": 5}}}
    (variant_dir / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    variant = load_pack(variant_dir)  # the full lint runs on load
    out = mechanics.render_matrix(variant, event="pickpocket_failed")
    assert "guilds (1 keys)" in out
    assert "steal.failure" in out  # the known wiring still resolves


# -- the dynamic half ---------------------------------------------------------


def test_beat_grid_matches_pack_offsets() -> None:
    """The grid derivation: intraday beat_ticks repeated daily, fired up
    to the last event tick (day1_full ends at t=1456 -> 3 beats)."""
    assert mechanics.beat_grid(PACK.rules, 1456) == [360, 720, 1080]
    assert mechanics.beat_grid(PACK.rules, 700) == [360]
    assert mechanics.beat_grid(PACK.rules, 0) == []


def test_shadow_releases_equal_the_log(tmp_path: Path) -> None:
    """THE exactness pin: the shadow's release ids == the log's own
    director-intent events on the canonical run (INV-2: replaying the
    real pipeline reproduces the runtime's decisions)."""
    events = _run_day1(tmp_path)
    replay = mechanics.shadow_replay(PACK, events)
    shadow_ids = sorted(
        line.intent_id for beat in replay.beats for line in beat.releases
    )
    log_ids = sorted(
        str(event.provenance["cause_intent"])
        for event in events
        if str(event.provenance.get("cause_intent", "")).startswith("director_")
    )
    assert shadow_ids == log_ids == ["director_0000", "director_0001"]


def test_trace_pins_the_canonical_run(tmp_path: Path) -> None:
    """The STATUS pins render: the relief's check commits at t=734; the
    sweep is the day's last event at t=1456; the release lines name the
    hooks and the log events carry the director attribution."""
    events = _run_day1(tmp_path)
    out = mechanics.render_trace(
        PACK, events, source="day1", seed=125, tick_from=700
    )
    assert "[t=734] ev_0044 document_check_failed" in out
    assert "director_0000 -> possible_document_check_relief" in out
    tail = mechanics.render_trace(
        PACK, events, source="day1", seed=125, tick_from=1447
    )
    assert "[t=1456] ev_0060 look_around" in tail
    assert "barkeep_wary_sweep" in tail
    hook_view = mechanics.render_trace(
        PACK, events, source="day1", seed=125, hook="possible_document_check_relief"
    )
    assert "seeded 1 (ev_0007@t=9)" in hook_view
    assert "released at beat(s) 360" in hook_view


def test_why_explains_blocked_and_released(tmp_path: Path) -> None:
    """The postmortem: at t=700 the watcher's check is ARMED but its
    option gate is CLOSED (the deferred-release law); the relief's half
    released at beat t=360."""
    events = _run_day1(tmp_path)
    blocked = mechanics.render_why(
        PACK, events, tag="possible_document_check", at_tick=700
    )
    assert "-> ARMED" in blocked
    assert "-> CLOSED" in blocked
    assert "released    NO" in blocked
    released = mechanics.render_why(
        PACK, events, tag="possible_document_check_relief"
    )
    assert "released    YES" in released
    assert "beat t=360" in released


def test_why_unknown_tag_fails_loudly(tmp_path: Path) -> None:
    """A tag the pack does not declare: the honest answer, no guessing."""
    events = _run_day1(tmp_path)
    out = mechanics.render_why(PACK, events, tag="no_such_hook")
    assert "no such hook" in out


# -- blast --------------------------------------------------------------------


def test_blast_reports_the_insert_delta(tmp_path: Path) -> None:
    """The two-arm A/B: same seed, one inserted step, honest deltas —
    event delta, projection delta, fingerprint divergence (the RNG
    price), and both arms' shapes."""
    script = load_playscript(DAY1)
    step = {"intent": "distract", "target": "npc_guard_01"}
    out = mechanics.run_blast(
        PACK, SCHEMA, script, step, 3, tmp_path / "blast"
    )
    assert "arm A (base)     : 61 events" in out
    assert "arm B (modified) : 62 events" in out
    assert "+distract x1" in out
    assert "npc_guard_01.status.attention: None -> 'distracted'" in out
    assert "DIVERGED" in out
    assert (tmp_path / "blast" / "blast_day1_full_a.jsonl").exists()
    assert (tmp_path / "blast" / "blast_day1_full_b.jsonl").exists()


def test_blast_without_step_runs_identical_arms(tmp_path: Path) -> None:
    """No inserted step: the arms are the same script — equal
    fingerprints, no deltas (the instrument's null control)."""
    script = load_playscript(DAY1)
    out = mechanics.run_blast(PACK, SCHEMA, script, None, None, tmp_path / "blast0")
    assert "EQUAL (no RNG divergence)" in out
    assert "event delta      none" in out
