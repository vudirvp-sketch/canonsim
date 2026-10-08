"""gaproutes — the W6 station's two double-confirmed RENDERING_GAP
routings (iter-281, the owner's «продолжай работу над задачами класса
мирового трека, делай то, что логичнее и правильнее сейчас сделать, а
не потом» delegated call over iter-280's §F: the two named gaps as
future rows — W7 is "after W6", entering it with the station's own
rows open would violate the station order, iter-279's own argument).

THE MEASURED GAPS (WORLD_TESTS §9's W6 entry, the iter-279/280 records
— three independent readings across two reader classes, BOTH legs
failing at BOTH bands):

(a) THE NIGHT RISK FORM (ADVENTURE A2's night half): the substrate
carries the night arrival at the unlit crofts (the location flags; the
acquisition rule's own phase_in/unless_flag condition; iter-278's
deterministic band measured it deliberately) — the reading form loses
it: the moves are low-importance (the T7 law — no gate raised, the
rejected-knob law) and the `lit` flag rendered nowhere in the
tale/records/briefs.

(b) THE BALANCE-MOVE ASSEMBLY (POLITICS P3): the repricing's causal
row (the guild's squeeze answering the withhold, the terms climbing,
standing) rides the knows gloss — a surface OUTSIDE the kit's form;
the kit carried the delta-form tale line + the bare recalled-facts
token + the records' totals, and the reader never assembled the
standing-terms move (the agency misread once as Garrick's own doing).

THE FIX (the rs family's eleventh and twelfth members, the recorded
precedents' own shapes — zero canon, zero core semantics, the LOG
untouched by construction):

(a) THE NIGHT FORM: two read-side condition namespaces over the
iter-265 law (render/chronicle.py) — the event's own phase as a
per-phase boolean `phase.<id>` (phase_of_tick, the rules-level twin)
and the event site's props as `site.<prop>` (the location fold's
event-scoped view — a GENERIC line conditions on the site it lands
at, no location id named in the template) — plus ONE move-line arm
(templates.json: the `{phase.night?#night_arrival#|.}` tail; the
symbol indirection carries the composed condition — the engine's
conditional partition splits at the first `|`, so the inner
lit/unlit branch rides a SYMBOL, expanded recursively after the
outer choice; the existing machinery, never an engine change).

(b) THE CAUSAL ROW: the account line's KNOWS TAIL —
`{knows? — {knows}}` on account_sourced, the rs-9 `{secret? —
{secret}}` tail's own shape: an account event that mints knowledge
(the reprice door, the notch door) carries its witnessed row on the
line through rs-1's boundary (one table, every consumer); the flow
events carry no knowledge and render dry (the crossings' lines
byte-stable). The two glosses re-authored for the composed line:
the_paper_repriced as the tail (the guild's agency + the withhold +
the standing terms + the climb — the amount already in the line's
head), the_dry_year_notched de-redundantized against its kind gloss
(what the notching DOES, never a restatement).

The claim packet (TEST_PLAN §9):

- Claim: the two reading forms now carry the substrate's own facts —
  the night arrival at an unlit site reads its risk form on the move
  line (the records surface; the tale gate UNTOUCHED, the T7 law
  held), the repricing's line carries the guild's causal row (the
  tale + the records), and every unchanged surface stays
  byte-stable: the day moves plain, the crossings' flow lines dry,
  the committed corpora byte-identical (the templates never enter
  the log).
- Problem: the two double-confirmed RENDERING_GAPs — a reading miss
  never proving a substrate lack (the discrimination law), the
  repair a rendering surface, never prose, never a gate, never
  machinery.
- Lens(es): the reader-surface boundary (the records' move line, the
  account line's tail); the composed-condition authoring (the symbol
  indirection over the raw-truthiness law); the every-consumer law
  (the gloss one table: the tale line, the entity view's history,
  the scene card's display).
- Prism: the mechanism census (the scratch pack's re-voiced wait
  line reading phase.*/site.* — the seed, the advance, the foreign
  tolerance); the journey integration arm (seed 42, the day and
  night arrivals in one history); the lit-night arm (the keep after
  dark — the honest complement); the squeeze arm (the committed
  pack, the master's records); the byte-regen (the province smoke).
- Oracle: the rendered text itself (the branch words on each
  surface), the projection reads, the byte-identical re-render, the
  golden fixture bytes.
- Falsifier: the night prose on a day arrival; the unlit prose on a
  lit site; the move line inside the tale (the gate raised); the
  raw token on the account line; the crossings' lines gaining a
  tail; the golden fixture's bytes changing.
- Expected evidence: the census branches; the journey's records
  carrying both forms; the keep's lit arm; the squeeze's tailed line
  on both surfaces; the byte-identical regen.
- Observed evidence: CONFIRMED at the measured band (seed 42: the
  census, the journey, the lit-night arm, the squeeze, the regen).
- Epistemic class: measured, deterministic per seed.
- Disposition: CONFIRMED (the reading band's re-measure — the blind
  glm n=2 over the regenerated kit — is the iteration's own second
  half, recorded in WORLD_TESTS §9's W6 entry, never in this
  witness; the A3 objective leg's reader-class variance and the
  free-namings divergence stand as recorded, never re-asked).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.fold import fold, initial_projection
from core.log import EventRecord, read_log
from core.loop import Simulator, load_playscript
from core.pack import load_pack
from render.chronicle import render_chronicle, render_entity_view

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

PC = "pc_01"
MASTER = "npc_smelter_01"
KEEP = "loc_keep"
CHEST = "loc_malby"
CROFTS = "loc_crofts"
TALLY = "camp_tally_01"

#: The journey chain (test_tallyread's DAY_CHAIN form — cited, never
#: re-derived): the walk to the keep lands in the afternoon (t=660),
#: the walk to the crofts lands IN THE NIGHT (t=1113, the unlit yards —
#: ki114-1-impl: +3, the F1 feed shift, the move feeding at the drained
#: clock; the night window still held), the night waited out, the
#: tally read by daylight.
JOURNEY: tuple[dict[str, Any], ...] = (
    {"intent": "move", "target": KEEP},
    {"intent": "move", "target": CROFTS},
    {"intent": "wait", "ticks": 400},
    {"intent": "read_tally", "target": TALLY},
)

#: The lit-night arm: the same first edge walked after a long wait —
#: the arrival at the LIT keep inside the night phase (the honest
#: complement: the same conditional, the other branch).
LIT_NIGHT: tuple[dict[str, Any], ...] = (
    {"intent": "wait", "ticks": 700},
    {"intent": "move", "target": KEEP},
    {"intent": "wait", "ticks": 10},
)

#: The squeeze chain (test_genre's SQUEEZE form — cited): the master
#: walks to the beam's town and the terms are re-priced twice on the
#: committed package.
SQUEEZE: tuple[dict[str, Any], ...] = (
    {"intent": "move", "actor": MASTER, "target": KEEP},
    {"intent": "move", "actor": MASTER, "target": CHEST},
    {"intent": "reprice_paper", "actor": MASTER, "target": MASTER},
    {"intent": "reprice_paper", "actor": MASTER, "target": MASTER},
    {"intent": "wait", "ticks": 10},
)

DAY_PLAIN = "[t 660] the factor's runner takes the road to the half-pay keep."
NIGHT_UNLIT = (
    "[t 1113] the factor's runner takes the road to the smelt crofts"
    " — the walk landing after dark, the yards unlit."
)
NIGHT_LIT = (
    "the factor's runner takes the road to the half-pay keep"
    " — arriving after dark, the yards lit."
)
SQUEEZE_TAILED = (
    "Garrick comes by 2 paper owed to the guild's chest at Malby"
    " since the starved winter at the year's reckoning — the guild's"
    " squeeze answering the withhold: the loads kept off the weighbeam"
    " priced onto the standing terms, the debt climbing while the"
    " bloom stays unweighed."
)


def _run(
    tmp_path: Path, name: str, seed: int, steps: tuple[dict[str, Any], ...],
) -> tuple[list[EventRecord], Any, str]:
    """One real run + its projection + its tale (the committed pack)."""
    pack = load_pack(PACK_DIR)
    log = tmp_path / name
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": name, "seed": seed, "pack": "province_pack@0.1",
        "steps": [dict(step) for step in steps],
    })
    sim.close()
    _header, events = read_log(log, SCHEMA)
    projection = fold(events, initial_projection(pack.entities))
    return events, projection, render_chronicle(events, pack, seed=seed)


# -- the mechanism census (a scratch pack through the real load_pack) ---------


def _probe_pack(tmp_path: Path) -> Any:
    """A scratch copy of the province pack through the REAL load_pack
    (the iter-263 instrument's own law: the lint is part of the tool),
    the wait line re-voiced to read the TWO new condition namespaces —
    every phase/site claim readable through the public render surface."""
    pack_dir = tmp_path / "probe_pack"
    pack_dir.mkdir()
    for name in ("entities.json", "rules.json", "actions.json"):
        shutil.copy(PACK_DIR / name, pack_dir / name)
    templates = json.loads(
        (PACK_DIR / "templates.json").read_text(encoding="utf-8")
    )
    templates["events"]["wait"] = (
        "phase:{phase.night?NIGHT|DAY} "
        "site_lit:{site.lit?LIT|DARK} "
        "site_smoke:{site.smoke?SMOKE|CLEAR} "
        "site_coin:{site.account.coin?COIN|EMPTY}"
    )
    (pack_dir / "templates.json").write_text(
        json.dumps(templates, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return load_pack(pack_dir)


def _crafted(
    event_id: str, t: int, location: str | None,
    changes: tuple[Any, ...] = (),
) -> EventRecord:
    """A minimal valid probe event (the re-voiced wait line) — the
    `location` outcome key names the event's site, the fold advances
    on every event (the tale gate reads importance, never the fold)."""
    outcome: dict[str, Any] = {"probe": True}
    if location is not None:
        outcome["location"] = location
    return EventRecord(
        id=event_id, t=t, type="wait", actor="world", cause=None,
        outcome=outcome, knowledge=(), state_changes=changes,
        hooks=(), importance="high", provenance={}, target=None,
    )


def test_the_phase_key_reads_the_events_own_phase(tmp_path: Path) -> None:
    """The per-phase boolean: only the event's OWN phase id lands a
    `phase.<id>` key, True — a night tick reads NIGHT, a morning tick
    DAY (the night key absent, raw-truthiness falsy); the phase ids
    are the pack's declared vocabulary, never a renderer constant."""
    pack = _probe_pack(tmp_path)
    night = render_chronicle([_crafted("e1", 1110, None)], pack, seed=2)
    assert "phase:NIGHT" in night
    morning = render_chronicle([_crafted("e2", 100, None)], pack, seed=2)
    assert "phase:DAY" in morning
    assert "phase:NIGHT" not in morning


def test_the_site_keys_read_the_event_sites_own_state(tmp_path: Path) -> None:
    """The event-scoped site view: the keep (flags: lit) reads LIT;
    the crofts (no declared flags) read DARK with every site.* key
    absent; the chest's seeded account surfaces its own truthiness —
    the same fold iter-265 exposed, scoped to the event's own site."""
    pack = _probe_pack(tmp_path)
    keep = render_chronicle([_crafted("e1", 100, KEEP)], pack, seed=2)
    assert "site_lit:LIT" in keep
    crofts = render_chronicle([_crafted("e2", 100, CROFTS)], pack, seed=2)
    assert "site_lit:DARK" in crofts
    chest = render_chronicle([_crafted("e3", 100, CHEST)], pack, seed=2)
    assert "site_lit:LIT" in chest  # Malby is lit too
    assert "site_coin:COIN" in chest  # the seeded account level


def test_the_site_keys_are_a_reader_never_a_truth_test(
    tmp_path: Path,
) -> None:
    """The tolerance law (iter-265's own): a location write lands in
    the fold at the writing event's own line too (the at-tick
    inclusive law), and an UNKNOWN site answers empty — the
    conditionals read absent-falsy, a foreign log renders dry and
    honest, never a crash."""
    pack = _probe_pack(tmp_path)
    from core.log import StateChange
    fire = _crafted("e1", 100, CROFTS, changes=(
        StateChange(CROFTS, "smoke", False, True),
    ))
    tale = render_chronicle([fire, _crafted("e2", 200, CROFTS)], pack, seed=2)
    assert tale.count("site_smoke:SMOKE") == 2  # the write lands, inclusive
    foreign = render_chronicle(
        [_crafted("e3", 100, "loc_foreign")], pack, seed=2
    )
    assert "site_lit:DARK" in foreign and "site_smoke:CLEAR" in foreign


def test_the_symbol_indirection_composes_the_condition(
    tmp_path: Path,
) -> None:
    """The composed condition's authoring law: the engine's conditional
    partition splits at the FIRST `|`, so the move line's night arm
    rides a SYMBOL (expanded recursively AFTER the outer choice) — the
    inner lit/unlit branch never leaking into the outer partition; the
    committed pack's move template is exactly this shape."""
    pack = load_pack(PACK_DIR)
    template = pack.templates["events"]["move"]
    assert template == (
        "{actor} takes the road to {target_location}"
        "{phase.night?#night_arrival#|.}"
    )
    symbol = pack.templates["symbols"]["night_arrival"]
    assert symbol == (
        "{site.lit? — arriving after dark, the yards lit."
        "| — the walk landing after dark, the yards unlit.}"
    )


# -- the integration arms (one history, both forms) -----------------------------


def test_the_journeys_records_carry_the_night_form(tmp_path: Path) -> None:
    """THE gap (a) witness: the same journey, both arrivals — the
    afternoon arrival at the keep renders PLAIN, the night arrival at
    the unlit crofts renders the walk's own risk form; the reader of
    the records now holds the substrate's own fact (the acquisition
    rule's condition made legible), the falsifier the night prose on
    a day arrival."""
    events, projection, tale = _run(tmp_path, "journey.jsonl", 8, JOURNEY)
    view = render_entity_view(events, projection, load_pack(PACK_DIR), PC, seed=42)
    assert DAY_PLAIN in view
    assert NIGHT_UNLIT in view


def test_the_tale_gate_is_untouched_the_t7_law_held(tmp_path: Path) -> None:
    """The rejected-knob law: the moves stay low-importance — NO move
    line inside the tale (the gate never raised), the night form
    living on the records surface alone; the tale's own lines
    unchanged in kind."""
    _events, _projection, tale = _run(tmp_path, "journey.jsonl", 42, JOURNEY)
    assert "takes the road" not in tale
    assert "the yards unlit" not in tale


def test_the_lit_night_arrival_reads_its_own_arm(tmp_path: Path) -> None:
    """The honest complement: the same edge walked after dark into a
    LIT site — the conditional's other branch; the tale never
    contradicting the projection (the unlit prose on the lit keep
    would be the iter-263 contradiction's own shape)."""
    events, projection, _tale = _run(tmp_path, "litnight.jsonl", 42, LIT_NIGHT)
    move = next(e for e in events if e.type == "move")
    assert 1080 <= move.t < 1440  # the walk lands in the night phase
    view = render_entity_view(
        events, projection, load_pack(PACK_DIR), PC, seed=42
    )
    assert NIGHT_LIT in view
    assert "the yards unlit" not in view


def test_the_squeezes_line_carries_the_causal_row(tmp_path: Path) -> None:
    """THE gap (b) witness: the repricing's line — the tale AND the
    master's records — carries the guild's causal row (the agency +
    the withhold + the standing terms + the climb) through rs-1's
    boundary; the record's own state line carries the terms' final
    standing (the persistence datum); the raw token never surfaces."""
    events, projection, tale = _run(tmp_path, "squeeze.jsonl", 42, SQUEEZE)
    assert tale.count(SQUEEZE_TAILED) == 2  # both squeezes, the climb's steps
    view = render_entity_view(
        events, projection, load_pack(PACK_DIR), MASTER, seed=42
    )
    assert view.count(SQUEEZE_TAILED) == 2
    assert "  account.paper: 20 — paper owed to the guild's chest" in view
    assert "the_paper_repriced" not in tale  # the machine token never leaks


def test_the_render_stays_a_pure_function_of_the_log(
    tmp_path: Path,
) -> None:
    """T1's own law over both surfaces: a fresh render of the same
    events (a fresh fold, a fresh Engine, the same seed) is
    byte-identical — the new namespaces derive from the event's tick
    and the fold alone, stateless per pass."""
    events, _projection, tale = _run(tmp_path, "journey.jsonl", 42, JOURNEY)
    pack = load_pack(PACK_DIR)
    again = render_chronicle(events, pack, seed=42)
    assert again == tale
    assert render_chronicle(events, pack, seed=42) == again


def test_the_golden_corpus_stays_byte_untouched(tmp_path: Path) -> None:
    """The zero-corpus-price law: the templates are read-side only —
    the committed golden T1 fixture regenerates byte-identical over
    the changed pack (the LOG layer never sees a template)."""
    golden = (
        REPO / "tests" / "fixtures" / "province_smoke_seed42.jsonl"
    ).read_bytes()
    script = load_playscript(
        REPO / "tests" / "playscripts" / "province_smoke.json"
    )
    pack = load_pack(PACK_DIR)
    log = tmp_path / "smoke.jsonl"
    sim = Simulator(pack, script["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    assert log.read_bytes() == golden
