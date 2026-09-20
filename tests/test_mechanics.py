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

mech-2 (iter-163) — the §9 claim packet (TEST_PLAN §9's form):
Claim: the CLI's DEFAULTS respect the reading agent's attention budget
without dropping facts silently, and the two riders — the one-event read
(intake-21) and the systems-graph export (intake-22) — are honest
projections. Problem: the unqualified `trace`/`matrix` printed O(events)
walls (measured at iter-163's HEAD: 175/277 trace lines on the canonical
runs, 300+ matrix lines on the grown packs — the row's "past a screen"
conditional now FACT). Lenses: boundary/boundedness (the defaults),
attribution/explainability (the postmortem), independent re-derivation
(the recounts). Prism: the canonical day1_full run + the pack's own
declarations. Oracle: the window policy caps ONLY the unqualified default
and the note names the expansion flags; the postmortem's chain/children
counts and the DAG's edge counts equal independent recounts of the log's
cause links and rules.json::systems. Falsifier: any default exceeding the
budget with no truncation line; any count disagreeing with its recount.
Expected evidence: the pins below. Epistemic class: measured on the
canonical substrate. Disposition: CONFIRMED at iter-163; pack growth
re-tests through the same pins.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Mapping

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
    # weather-1's arming price, re-pinned: the warm ring's beat events
    # left the day (the check's id shifted with them, the verdict with
    # the draw sequence); the sweep is the day's last event
    assert "[t=734] ev_0043 document_check_failed" in out
    assert "director_0000 -> possible_document_check_relief" in out
    tail = mechanics.render_trace(
        PACK, events, source="day1", seed=125, tick_from=1447
    )
    assert "[t=1456] ev_0055 look_around" in tail
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


# -- mech-2: the attention budget (caps core) -------------------------------


def test_trace_default_window_policy(tmp_path: Path) -> None:
    """The cap law: an unqualified trace defaults to the last
    DEFAULT_TRACE_WINDOW_TICKS ticks with a note naming the expansion
    flags; every explicit flag is answered in full; a short run cuts
    nothing and says nothing (the note never lies)."""
    events = _run_day1(tmp_path)
    last = events[-1].t
    lo, hi, note = mechanics.trace_window(events)
    assert lo == last - mechanics.DEFAULT_TRACE_WINDOW_TICKS + 1
    assert hi == last
    assert note is not None and "--ticks 0:" in note and "--tail N" in note
    short = events[:3]
    assert mechanics.trace_window(short) == (None, None, None)
    assert mechanics.trace_window(events, ticks="0:") == (0, None, None)
    assert mechanics.trace_window(events, tail=10) == (last - 9, last, None)
    for kwargs in (
        {"entity": "pc_01"}, {"hook": "possible_document_check"},
        {"event_type": "wait"},
    ):
        assert mechanics.trace_window(events, **kwargs) == (None, None, None)


def test_trace_default_view_fits_the_budget(tmp_path: Path) -> None:
    """The capped default renders under a screen and ends with the note
    (the anti-silent-drop tail line — the operator always sees how to
    widen)."""
    events = _run_day1(tmp_path)
    lo, hi, note = mechanics.trace_window(events)
    out = mechanics.render_trace(
        PACK, events, source="day1", seed=125,
        tick_from=lo, tick_to=hi, window_note=note,
    )
    assert len(out.splitlines()) < 60  # a screen proxy (measured: 28)
    assert out.rstrip().endswith("or --entity/--hook/--event to narrow")


def test_matrix_compact_default_full_by_flag() -> None:
    """The bounded default: the queryable name spaces (the vocabulary the
    four narrow flags accept), the folds, the unindexed law line, the
    query note; the wiring itself stays behind --full / narrow queries."""
    compact = mechanics.render_matrix(PACK, full_inventory=False)
    assert "compact — the default view" in compact
    assert "hooks (" in compact and "possible_document_check" in compact
    assert "tokens (" in compact and "figure_reaching_for_purse" in compact
    assert "unindexed rules blocks" in compact  # the future-layer law stays
    assert "--full (the whole inventory)" in compact
    assert "-- hooks (director.hooks) --" not in compact
    full = mechanics.render_matrix(PACK)  # full_inventory defaults True
    assert "-- hooks (director.hooks) --" in full
    assert "hook possible_document_check" in full


# -- mech-2: the single-event postmortem (intake-21) -------------------------


def _recount_descendants(events: list, event_id: str) -> tuple[int, int]:
    """The independent oracle: direct + total descendants recounted by a
    DFS over the log's own cause links (a path the renderer does not
    share — TEST_PLAN §9's re-derivation law)."""
    kids: dict[str, list[str]] = {}
    for e in events:
        if e.cause is not None:
            kids.setdefault(e.cause, []).append(e.id)
    seen: set[str] = set()
    frontier = list(kids.get(event_id, ()))
    while frontier:
        nid = frontier.pop()
        if nid in seen:
            continue
        seen.add(nid)
        frontier.extend(kids.get(nid, ()))
    return len(kids.get(event_id, ())), len(seen)


def test_why_event_postmortem_matches_recount(tmp_path: Path) -> None:
    """The one-event read: ev_0007 (the theft) — the backward chain, the
    knowledge join (the minted tokens' crime/echo/traits wiring), and the
    cascade counts all equal independent recounts of the log's cause
    links; the truncation line names the walk-back query."""
    events = _run_day1(tmp_path)
    out = mechanics.render_why_event(PACK, events, event_id="ev_0007")
    by_id = {e.id: e for e in events}
    chain_len = 0
    cursor = by_id["ev_0007"].cause
    while cursor is not None:
        chain_len += 1
        cursor = by_id[cursor].cause
    assert f"cause chain  {chain_len} link(s) back to ev_0000" in out
    direct, total = _recount_descendants(events, "ev_0007")
    assert f"{direct} direct · {total} descendant(s) total" in out
    assert "crime witnessed_steal_failure +25" in out
    assert "traits paranoid_about_thieves" in out
    # the cap names its cut only when it cut: ev_0007's chain (6 links)
    # is shorter than the detail cap, so no chain-truncation line appears;
    # ev_0043's (26 links) hides 18 and names the walk-back query.
    assert "earlier links" not in out
    late = mechanics.render_why_event(PACK, events, event_id="ev_0043")
    chain_late = []
    cursor = by_id["ev_0043"].cause
    while cursor is not None:
        chain_late.append(cursor)
        cursor = by_id[cursor].cause
    hidden = len(chain_late) - mechanics.CHAIN_DETAIL_LINKS
    assert hidden > 0  # the pin's own precondition
    walk_back = chain_late[mechanics.CHAIN_DETAIL_LINKS - 1]
    assert f"(+{hidden} earlier links; walk back with why --event {walk_back})" in late


def test_why_event_edges_unknown_and_run_start(tmp_path: Path) -> None:
    """The honest edges: an unknown id refuses; the run-start carries no
    chain and the whole run descends from it (the writer's cause law)."""
    events = _run_day1(tmp_path)
    unknown = mechanics.render_why_event(PACK, events, event_id="ev_9999")
    assert "no such event id" in unknown
    root = mechanics.render_why_event(PACK, events, event_id="ev_0000")
    assert "the run-start event (cause null)" in root
    assert f"{len(events) - 1} descendant(s) total" in root


# -- mech-2: the systems graph export (intake-22) ----------------------------


def test_dag_is_the_systems_projection() -> None:
    """The viz export: a Mermaid projection of rules.json::systems whose
    read/write edge counts equal an independent recount of the pack's own
    declarations; the per_tick marker and the after-hint render; the
    projection law names itself (never a second truth)."""
    raw = {
        k: v for k, v in PACK.rules.get("systems", {}).items()
        if isinstance(v, Mapping)
    }
    reads = sum(len(v.get("reads", ())) for v in raw.values())
    writes = sum(len(v.get("writes", ())) for v in raw.values())
    out = mechanics.render_dag(PACK)
    assert out.startswith("%% MERMAID flowchart")
    assert "flowchart LR" in out
    assert out.count(" -.-> ns_") == reads
    assert out.count(" --> ns_") == writes
    assert 'sys_fire["fire"]:::per_tick' in out
    assert "sys_relations ==>|before| sys_crime_watch" in out
    assert "never truth" in out


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
    # weather-1's arming price: the warm ring's beat events left the
    # day — the base arm carries 56 (was 61), the +distract arm 57
    assert "arm A (base)     : 56 events" in out
    assert "arm B (modified) : 57 events" in out
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
