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

mech-2 (iter-196) — the §9 claim packet for the impact surface (the
agent-edit loop's tool, intake-37's named consumer): Claim: `impact
--path/--ref` gives the static blast radius of an ARBITRARY pack path —
derived readers (runtime + load-time lint, minimal witnesses),
exact-name cross references, and the indexed-matrix pointers — with zero
runtime change. Problem: the matrix indexed only the hook/event/token/prop
quadruple; the other ~19 rules blocks were listed generically (intake-37's
measured gap — value edits there pass lint + goldens when the path is
uncovered). Lenses: boundary/boundedness (the caps + their named cuts),
independent re-derivation (the reader names + the reference recounts).
Prism: the canonical tavern pack + a variant pack's fresh block. Oracle:
the reader set names the real consuming modules with witness lines that
exist in the source (director/weather/travel/knowledge — the
constant-declared blocks included); the reverse query's counts and sites
equal an independent recount walk. Falsifier: any named reader whose
source line does not access the block; any site count disagreeing with
the recount; any silently-dropped listing. Expected evidence: the pins
below. Epistemic class: measured on the canonical substrate. Disposition:
CONFIRMED at iter-196; source growth re-tests through the same pins.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Mapping

import pytest

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


# -- mech-2: the impact surface (iter-196) ------------------------------------


def test_block_access_sites_derive_from_source() -> None:
    """The reader index is DERIVED, never a hand table: the literal form
    (`rules.get("director")`), the `*_BLOCK` constant form (weather,
    travel, worldgen), and the chained literal form (`knowledge.drift`)
    all resolve; every witness line exists in the named source file; the
    packlint family classifies as load-time lint."""
    sites = mechanics.block_access_sites()
    chains = {(s.file, s.chain) for s in sites}
    assert ("core/director.py", ("director",)) in chains
    assert ("core/weather.py", ("weather",)) in chains
    assert ("core/travel.py", ("travel",)) in chains
    assert ("core/travel.py", ("worldgen", "map", "spacing")) in chains
    assert ("core/knowledge.py", ("knowledge", "drift")) in chains
    assert not any(s.file.startswith("scripts/") for s in sites)
    for site in sites:
        if site.file == "core/director.py" and site.chain == ("director",):
            source = (REPO / "core" / "director.py").read_text(
                encoding="utf-8"
            ).splitlines()
            assert "rules" in source[site.line - 1]
            break
    else:
        raise AssertionError("director site not found")


def test_impact_path_readers_and_pointers() -> None:
    """The forward query on the indexed hotspot: the hook path resolves,
    the runtime readers carry minimal witnesses, the load-time lint names
    the admission surface, the cross references give the rename-safety
    set, and the indexed pointer defers to matrix (D-024 — never
    restating the quadruple's wiring)."""
    out = mechanics.render_impact(
        PACK, path="director.hooks.possible_document_check"
    )
    assert out.startswith("== IMPACT tavern_pack@0.1")
    assert "resolves     rules.director.hooks.possible_document_check" in out
    assert "core/director.py:" in out
    assert "[reads director]" in out
    assert "load-time lint: core/packlint/" in out
    assert "refs         'possible_document_check' — 2 exact-name site(s)" in out
    assert "actions.steal.hooks.failure.1 [member]" in out
    assert "rules.director.hooks.possible_document_check [key]" in out
    assert "matrix --hook possible_document_check" in out
    assert "read-only after load" in out


def test_impact_unindexed_block_value() -> None:
    """The measured gap's own case: a value path in an UNINDEXED block
    (knowledge.drift) still gets its reader witness at literal precision —
    the extension beyond the hook/event/token/prop quadruple — and no
    indexed pointer is claimed for a name the pack does not declare."""
    out = mechanics.render_impact(PACK, path="knowledge.drift")
    assert "core/knowledge.py:" in out
    assert "[reads knowledge.drift]" in out
    assert "dict, 1 key(s): figure_deeds" in out
    assert "indexed" not in out
    assert "derived, never truth" in out


def test_impact_unknown_block_no_runtime_reader(tmp_path: Path) -> None:
    """The future-layer law extended to impact: a fresh block LOADS (the
    pack lint passes) and impact reports it honestly — no runtime reader,
    never a rejection; the reader surface is visible the iteration a
    consumer lands."""
    variant_dir = tmp_path / "pack_variant"
    variant_dir.mkdir()
    for name in ("actions.json", "entities.json", "templates.json"):
        shutil.copyfile(PACK_DIR / name, variant_dir / name)
    rules = json.loads((PACK_DIR / "rules.json").read_text(encoding="utf-8"))
    rules["guilds"] = {"houses": {"house_01": {"honor": 5}}}
    (variant_dir / "rules.json").write_text(
        json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    variant = load_pack(variant_dir)
    out = mechanics.render_impact(variant, path="guilds.houses.house_01.honor")
    assert "resolves     rules.guilds.houses.house_01.honor — 5" in out
    assert "runtime: none" in out
    assert "honor" in out  # the reference section still answers


def _recount_reference_sites(data: Mapping, name: str) -> list[tuple[str, str]]:
    """The independent oracle: recount (display path, role) by a walk the
    renderer does not share — stringly path building over the serialized
    JSON, one entry per exact-name key/member/value site. The actions.json
    top-level list collapses into its namespace (the display grammar)."""
    found: list[tuple[str, str]] = []

    def visit(node: object, path: str, top: bool = False) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                collapse = top and str(key) == path
                child = path if collapse else f"{path}.{key}"
                if not collapse and str(key) == name:
                    found.append((child, "key"))
                visit(value, child)
        elif isinstance(node, list):
            for index, item in enumerate(node):
                if isinstance(item, str):
                    if item == name:
                        found.append((f"{path}.{index}", "member"))
                else:
                    label = next(
                        (str(item[k]) for k in ("id", "intent", "npc", "name")
                         if isinstance(item, dict) and k in item),
                        str(index),
                    )
                    visit(item, f"{path}.{label}")
        elif isinstance(node, str) and node == name:
            found.append((path, "value"))

    for file_name in ("actions.json", "entities.json", "rules.json",
                      "templates.json"):
        visit(data[file_name], file_name.removesuffix(".json"), top=True)
    return found


def test_impact_reverse_query_matches_recount() -> None:
    """The reverse query's sites equal an independent recount (TEST_PLAN
    §9's re-derivation law) on the canonical token; the role line defers
    to matrix --token (the quadruple's single owner)."""
    name = "figure_reaching_for_purse"
    expected = _recount_reference_sites(PACK.data, name)
    assert len(expected) == 8  # the hand-verified recount (2 files)
    out = mechanics.render_impact(PACK, ref=name)
    assert "knowledge token (matrix --token figure_reaching_for_purse)" in out
    assert "sites        8 exact-name reference(s) across 2 file(s)" in out
    for path, role in expected:
        assert f"{path} [{role}]" in out


def test_impact_reverse_query_role_and_cap() -> None:
    """The honest classification: an entity id names its role; a prose key
    (`notes`, str-valued inside on_action) is NOT an event type; a common
    name's listing caps at IMPACT_REFS_CAP with the cut named and --full
    named as the expansion flag (D-148's law)."""
    entity = mechanics.render_impact(PACK, ref="npc_guard_01")
    assert "entity id (npc)" in entity
    assert "rules.director.hooks.possible_document_check.target_npc [value]" in entity
    common = mechanics.render_impact(PACK, ref="notes")
    assert "event type" not in common
    assert f"(+{90 - mechanics.IMPACT_REFS_CAP} more — impact --full)" in common
    whole = mechanics.render_impact(PACK, ref="notes", full=True)
    assert "+" not in whole.split("sites")[1].split("note")[0].replace("(+", "")
    assert whole.count("[key]") == 90


def test_impact_path_miss_fails_loudly() -> None:
    """A path that does not resolve: the honest refusal naming the deepest
    resolved position and the available keys — never a guess."""
    with pytest.raises(SystemExit) as raised:
        mechanics.render_impact(PACK, path="weather.rotation")
    assert "does not resolve at rules.weather" in str(raised.value)
    assert "event_type" in str(raised.value)


def test_impact_cli_dispatch(capsys: pytest.CaptureFixture[str]) -> None:
    """The argparse wiring: the subcommand dispatches and prints (the
    operator surface — stdout only, INV-5 never touched)."""
    code = mechanics.main(["impact", "--ref", "figure_reaching_for_purse"])
    assert code == 0
    assert "8 exact-name reference(s)" in capsys.readouterr().out


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


# -- census (cov-1, iter-258) --------------------------------------------------

CORPUS = REPO / "tests" / "playscripts"


def test_census_pins_the_committed_corpus_coverage() -> None:
    """The census's coverage line over the committed corpus: the tavern
    pack's 16 actions pin to 10 realized (6 authored by the four tavern
    scripts + 4 autonomous-only) with the 6-action mutation-escape
    surface named (intake-37's measured lesson — the paths no golden
    binds); 0 consumerless (the admission lint's dead-action law agrees
    with the forward walk)."""
    out = mechanics.render_census(PACK, CORPUS, "tavern_pack")
    assert "== CENSUS tavern_pack · 16 actions" in out
    assert "(4 script(s))" in out
    assert (
        "coverage: 10 realized (6 authored · 4 autonomous-only) · "
        "6 UNREALIZED · 24 event types · 0 consumerless"
    ) in out
    unrealized = out.split("not coverage):", 1)[1]
    for intent in ("examine", "talk", "use", "distract", "arson", "flee"):
        assert intent in unrealized, f"{intent} missing from the escape surface"
    assert "move" not in unrealized


def test_census_action_block_is_the_forward_walk() -> None:
    """One action's full block: declaration → the parser verb (the t=0
    grammar derivation: steal is target-required with the closed method
    enum; drop_break's near enum is position-bound at t=0) → the realized
    legs (steal authored on the three theft scripts, never autonomous;
    wait both) → the canonical events → the per-event consumers."""
    out = mechanics.render_census(
        PACK, CORPUS, "tavern_pack", action="steal"
    )
    assert "resolver     stealth_take · ticks 3" in out
    assert "target-required · fields: method(closed)" in out
    assert "authored     day1_full, day1_theft_and_arson, exp0_week" in out
    assert "autonomous   -" in out
    assert "events       steal / pickpocket_failed" in out
    assert "pickpocket_failed        systems crime_watch, knowledge, relations" in out
    wait = mechanics.render_census(PACK, CORPUS, "tavern_pack", action="wait")
    assert "ticks(positive_int)" in wait
    assert "urgency:npc_maid_01, urgency:npc_guard_02" in wait
    assert "hook:guard_suspicious_of_pc" in wait
    drop = mechanics.render_census(
        PACK, CORPUS, "tavern_pack", action="drop_break"
    )
    assert "near(EMPTY (position-bound))" in drop


def test_census_consumers_agree_with_the_matrix() -> None:
    """The consumers leg is the matrix's own reverse derivation (same
    source, same numbers): the census block's per-event lines match the
    matrix --event view's counts for the same event type."""
    census = mechanics.render_census(
        PACK, CORPUS, "tavern_pack", action="steal"
    )
    matrix = mechanics.render_matrix(PACK, event="pickpocket_failed")
    assert "crime tokens 2" in census
    assert "hook seeds 4" in census
    assert "crime" in matrix and "seeds" in matrix
    # the matrix's crime line lists the two tokens the census counts
    crime_line = next(
        line for line in matrix.splitlines() if line.startswith("  crime")
    )
    assert crime_line.count("->") == 2


def test_census_corpus_is_pack_scoped() -> None:
    """The realized leg counts only THIS pack's scripts: talk is authored
    on the province corpus (province_companion) while unrealized on the
    tavern corpus — a province witness never covers a tavern path."""
    province = load_pack(REPO / "content" / "province_pack")
    out = mechanics.render_census(province, CORPUS, "province_pack")
    assert "talk" not in out.split("not coverage):", 1)[1]
    tavern = mechanics.render_census(PACK, CORPUS, "tavern_pack")
    assert "talk" in tavern.split("not coverage):", 1)[1]


def test_census_is_regenerable() -> None:
    """Derived, rebuildable, never truth: two derivations over the same
    pack + corpus are byte-identical (INV-2's periphery discipline)."""
    first = mechanics.render_census(PACK, CORPUS, "tavern_pack")
    second = mechanics.render_census(PACK, CORPUS, "tavern_pack")
    assert first == second
    full = mechanics.render_census(PACK, CORPUS, "tavern_pack", full_inventory=True)
    assert full.count("\naction ") == 16  # every action blocks in --full


def test_census_unknown_action_fails_loud() -> None:
    """A named action absent from the pack is a loud exit, never a silent
    empty report (SSI-N006's family)."""
    with pytest.raises(SystemExit):
        mechanics.render_census(PACK, CORPUS, "tavern_pack", action="nope")


def test_census_cli_dispatch(capsys: pytest.CaptureFixture[str]) -> None:
    """The CLI subcommand lands the same report the render API returns."""
    assert mechanics.main(["census"]) == 0
    out = capsys.readouterr().out
    assert "== CENSUS tavern_pack · 16 actions" in out
    assert mechanics.main(["census", "--action", "wait"]) == 0
    assert "action wait" in capsys.readouterr().out
