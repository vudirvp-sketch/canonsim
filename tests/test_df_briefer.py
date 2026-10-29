"""Unit tests for `scripts/df_briefer.py` (bg-3 briefer spike).

Pins the load-bearing spike behavior on a tiny synthetic DF-like world
(the `tests/test_df_import.py` / `test_df_taxonomy.py` pattern): the POV
brief (assignment frame vs the subject's records, plus-field merge with
main precedence, the loud truncation marker), the epistemic closure (the
participant-index law — reputation events keyed hfid1/hfid2 are invisible
by design, the measured blind spot), the closed verdict vocabulary
(supported / contradicted / beyond_records / unknown_*), the shape gate
(malformed replies raise BrieferError, never a repair), the regen ladder
(refusal -> regen call with notes -> accept; exhaustion -> the dry floor),
the deterministic case listing, the stress smoke (double-build
byte-compare), and content determinism throughout.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import df_briefer  # type: ignore[import-not-found]  # noqa: E402
import df_import  # type: ignore[import-not-found]  # noqa: E402
import df_taxonomy  # type: ignore[import-not-found]  # noqa: E402

TINY_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<df_world>
  <sites>
    <site><id>10</id><type>tavern</type><name>The Stow</name></site>
  </sites>
  <entities>
    <entity><id>100</id><name>guild</name></entity>
    <entity><id>101</id><name>kingdom</name></entity>
  </entities>
  <historical_figures>
    <historical_figure>
      <id>500</id><race>DWARF</race><caste>MALE</caste>
      <birth_year>100</birth_year><death_year>-1</death_year><name>Urist</name>
    </historical_figure>
    <historical_figure>
      <id>501</id><race>HUMAN</race><caste>MALE</caste>
      <birth_year>120</birth_year><death_year>180</death_year><name>Gob</name>
    </historical_figure>
    <historical_figure>
      <id>502</id><race>ELF</race><caste>FEMALE</caste>
      <birth_year>150</birth_year><death_year>-1</death_year><name>Nia</name>
    </historical_figure>
  </historical_figures>
  <historical_events>
    <historical_event>
      <id>1</id><type>hf died</type><year>200</year><seconds72>-1</seconds72>
      <hfid>501</hfid><slayer_hfid>500</slayer_hfid>
      <cause>murdered</cause><site_id>10</site_id>
    </historical_event>
    <historical_event>
      <id>2</id><type>hf travel</type><year>205</year><seconds72>-1</seconds72>
      <group_hfid>500</group_hfid><site_id>10</site_id><return/>
    </historical_event>
    <historical_event>
      <id>3</id><type>item stolen</type><year>210</year><seconds72>-1</seconds72>
      <circumstance>historical event collection</circumstance>
      <circumstance_id>1</circumstance_id>
    </historical_event>
    <historical_event>
      <id>4</id><type>hfs formed reputation relationship</type>
      <year>202</year><seconds72>-1</seconds72>
      <hfid1>500</hfid1><hfid2>501</hfid2><site_id>10</site_id>
    </historical_event>
    <historical_event>
      <id>5</id><type>creature devoured</type><year>215</year>
      <seconds72>-1</seconds72><site_id>10</site_id>
    </historical_event>
    <historical_event>
      <id>6</id><type>field battle</type><year>200</year><seconds72>-1</seconds72>
      <attacker_civ_id>100</attacker_civ_id><defender_civ_id>101</defender_civ_id>
    </historical_event>
  </historical_events>
  <historical_event_collections>
    <historical_event_collection>
      <id>1</id><type>battle</type><start_year>200</start_year><end_year>215</end_year>
      <name>The Tiny Onslaught</name><site_id>10</site_id>
      <war_eventcol>2</war_eventcol><outcome>attacker won</outcome>
      <event>1</event><event>2</event><event>5</event><event>6</event>
    </historical_event_collection>
    <historical_event_collection>
      <id>2</id><type>war</type><start_year>200</start_year><end_year>215</end_year>
      <name>The Tiny War</name><aggressor_ent_id>100</aggressor_ent_id>
      <defender_ent_id>101</defender_ent_id>
      <eventcol>1</eventcol>
    </historical_event_collection>
  </historical_event_collections>
</df_world>
"""

TINY_PLUS_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<df_world>
  <historical_events>
    <historical_event>
      <id>3</id><type>item_stolen</type><year>210</year><seconds72>-1</seconds72>
      <item_type>cup</item_type><mat>gold cup</mat><histfig>501</histfig>
      <site>10</site><theft_method>theft</theft_method>
    </historical_event>
    <historical_event>
      <id>5</id><type>creature_devoured</type><year>215</year>
      <victim>-1</victim><race>goose</race><eater>502</eater><site>10</site>
    </historical_event>
  </historical_events>
</df_world>
"""


@pytest.fixture
def tiny_db(tmp_path: Path) -> Path:
    main = tmp_path / "tiny-legends.xml"
    plus = tmp_path / "tiny-legends_plus.xml"
    main.write_bytes(TINY_XML)
    plus.write_bytes(TINY_PLUS_XML)
    db = tmp_path / "tiny.sqlite3"
    df_import.import_world(main, db, plus)
    return db


@pytest.fixture
def conn_atlas(tiny_db: Path):
    import sqlite3

    conn = sqlite3.connect(tiny_db)
    atlas = df_taxonomy._Atlas(conn)
    yield conn, atlas
    conn.close()


def _reply(anchor: int, claims: list[dict], prose: str = "telling") -> dict:
    return {"anchor": anchor, "prose": prose, "claims": claims}


# -- the POV brief ----------------------------------------------------------


def test_pov_brief_renders_assignment_card_and_records(conn_atlas) -> None:
    conn, atlas = conn_atlas
    brief = df_briefer.build_pov_brief(conn, atlas, 500, 1)
    text = brief.text
    # the assignment frame carries curator facts, labeled NOT knowledge
    assert "tell battle 'The Tiny Onslaught' (col 1, y200-215)" in text
    assert "curator facts (NOT the subject's knowledge): place The Stow [site 10]" in text
    assert "4 direct member events · 0 nested collections" in text
    assert "recorded outcome: attacker won" in text
    assert "parent war: col 2" in text
    # the subject card
    assert "Urist [hf 500, DWARF] · born y100 · alive at export" in text
    assert "total records: 2 (participant index" in text
    # the POV records: Y's in-window events only, roles resolved
    assert "'hf died' ev 1" in text
    assert "hfid: Gob [hf 501, HUMAN]; slayer: Urist [hf 500, DWARF]" in text
    assert "'hf travel' ev 2" in text
    # the reputation event (hfid1/hfid2) and the participant-less member
    # events never enter the POV records — the closure law
    assert "ev 4" not in text
    assert "ev 5" not in text
    assert "ev 6" not in text
    assert "(the subject's in-window records: 2, of which the curator grouped 2" in text
    assert "regen: 0/2" in text
    assert brief.anchor == 2 and brief.window == (200, 215)


def test_pov_brief_caps_with_loud_marker(conn_atlas) -> None:
    conn, atlas = conn_atlas
    brief = df_briefer.build_pov_brief(conn, atlas, 500, 1, max_records=1)
    assert brief.truncated == 1
    assert "[truncated: 1 of 2 shown" in brief.text
    assert "never a silent drop" in brief.text


def test_plus_fields_merge_with_main_precedence(conn_atlas) -> None:
    conn, atlas = conn_atlas
    line = df_briefer.render_event_line(conn, atlas, 3)
    # theft detail lives only in the plus companion and renders from it
    assert "mat: gold cup" in line
    assert "theft_method: theft" in line
    assert "at The Stow [site 10]" in line  # the plus site resolves the place


def test_zero_record_figure_raises(conn_atlas) -> None:
    conn, atlas = conn_atlas
    with pytest.raises(df_briefer.BrieferError, match="zero participant-index"):
        df_briefer.build_pov_brief(conn, atlas, 502, 1)


def test_brief_is_deterministic(conn_atlas) -> None:
    conn, atlas = conn_atlas
    first = df_briefer.build_pov_brief(conn, atlas, 500, 1)
    second = df_briefer.build_pov_brief(conn, atlas, 500, 1)
    assert first.text == second.text


# -- the epistemic closure --------------------------------------------------


def test_closure_blind_spot_reputation_events(conn_atlas) -> None:
    conn, _ = conn_atlas
    closure = df_briefer.subject_closure(conn, 500)
    # the participant-index law: ev 4 keys its figures hfid1/hfid2 — the
    # tags do not end in 'hfid', so no rows lift (TAXONOMY §4.2)
    assert closure.events == {1, 2}
    assert closure.figures == {500, 501}
    assert closure.sites == {10}
    assert closure.total_records == 2


# -- reverse validation -----------------------------------------------------


def test_verdicts_supported_and_contradicted(conn_atlas) -> None:
    conn, atlas = conn_atlas
    closure = df_briefer.subject_closure(conn, 500)
    reply = _reply(2, [
        {"event": 1, "type": "hf died"},
        {"figure": 500, "prop": "race", "value": "DWARF"},
        {"figure": 501, "prop": "race", "value": "HUMAN"},
        {"figure": 501, "prop": "name", "value": "Gob"},
        {"figure": 500, "prop": "birth_year", "value": "100"},
        {"site": 10, "value": "The Stow"},
        {"event": 1, "type": "hf travel"},
        {"figure": 501, "prop": "race", "value": "ELF"},
    ])
    verdicts = df_briefer.validate_reply(conn, atlas, closure, reply, anchor=2)
    assert [v.verdict for v in verdicts[:6]] == ["supported"] * 6
    assert verdicts[6].verdict == "contradicted"
    assert "actual type 'hf died'" in verdicts[6].evidence
    assert verdicts[7].verdict == "contradicted"
    assert "actual race: HUMAN" in verdicts[7].evidence


def test_verdicts_beyond_records_and_unknown(conn_atlas) -> None:
    conn, atlas = conn_atlas
    closure = df_briefer.subject_closure(conn, 500)
    reply = _reply(2, [
        {"event": 5, "type": "creature devoured"},   # in the log, not Y's
        {"figure": 502, "prop": "race", "value": "ELF"},  # exists, outside closure
        {"event": 999},                              # not in the sink at all
        {"figure": 999, "prop": "race", "value": "ELF"},
        {"site": 999, "value": "nowhere"},
    ])
    verdicts = df_briefer.validate_reply(conn, atlas, closure, reply, anchor=2)
    assert [v.verdict for v in verdicts] == [
        "beyond_records", "beyond_records",
        "unknown_event", "unknown_figure", "unknown_site",
    ]
    assert "the subject has no record of it" in verdicts[0].evidence
    assert "outside the subject's closure" in verdicts[1].evidence


@pytest.mark.parametrize("bad", [
    {"anchor": 1, "prose": "x", "claims": []},            # anchor mismatch
    {"anchor": 2, "claims": []},                          # prose missing
    {"anchor": 2, "prose": "  ", "claims": []},           # prose empty
    {"anchor": 2, "prose": "x"},                          # claims missing
    {"anchor": 2, "prose": "x", "claims": {}},            # claims not a list
    {"anchor": "2", "prose": "x", "claims": []},          # anchor not an int
    {"anchor": 2, "prose": "x", "claims": ["nope"]},      # claim not an object
    {"anchor": 2, "prose": "x", "claims": [{"event": 1, "what": "?"}]},
    {"anchor": 2, "prose": "x", "claims": [{"figure": 500, "prop": "job"}]},
    {"anchor": 2, "prose": "x", "claims": [{"figure": 500, "prop": "race"}]},
    {"anchor": 2, "prose": "x", "claims": [{"foo": 1}]},  # no known kind
])
def test_shape_gate_is_loud(conn_atlas, bad: dict) -> None:
    conn, atlas = conn_atlas
    closure = df_briefer.subject_closure(conn, 500)
    with pytest.raises(df_briefer.BrieferError):
        df_briefer.validate_reply(conn, atlas, closure, bad, anchor=2)


# -- the regen ladder -------------------------------------------------------


def test_refusal_emits_regen_call_then_accepts(conn_atlas, tmp_path: Path) -> None:
    conn, atlas = conn_atlas
    out = tmp_path / "session"
    call_path, brief = df_briefer.emit_call(
        conn, atlas, out, 500, 1, max_records=60, context=8
    )
    assert call_path.name == "call_0000.md"
    # the leaky draft: ev 5 exists in the log but outside the records
    leaky = tmp_path / "reply_0000.json"
    leaky.write_text(json.dumps(_reply(brief.anchor, [
        {"event": 5, "type": "creature devoured"},
        {"event": 1, "type": "hf died"},
    ])), encoding="utf-8")
    code = df_briefer.apply_reply(conn, atlas, call_path, leaky, out,
                                  max_records=60, context=8)
    assert code == 1  # REFUSED
    regen = out / "call_0001.md"
    state = df_briefer.parse_call(regen.read_text(encoding="utf-8"))
    assert state.regens == 1 and state.hfid == 500 and state.col_id == 1
    assert any("refused claim 0" in n for n in state.notes)
    assert "beyond_records" in "\n".join(state.notes)
    # the corrected draft passes through the regen call
    fixed = tmp_path / "reply_0001.json"
    fixed.write_text(json.dumps(_reply(state.anchor, [
        {"event": 1, "type": "hf died"},
        {"figure": 501, "prop": "race", "value": "HUMAN"},
    ])), encoding="utf-8")
    code = df_briefer.apply_reply(conn, atlas, regen, fixed, out,
                                  max_records=60, context=8)
    assert code == 0  # ACCEPTED


def test_exhaustion_renders_dry_floor(conn_atlas, tmp_path: Path) -> None:
    conn, atlas = conn_atlas
    out = tmp_path / "session"
    call_path, brief = df_briefer.emit_call(
        conn, atlas, out, 500, 1, max_records=60, context=8
    )
    leaky = _reply(brief.anchor, [{"event": 5}])
    code = 2  # sentinel: must end exhausted
    for step in range(3):
        reply_path = tmp_path / f"bad_{step}.json"
        reply_path.write_text(json.dumps(leaky), encoding="utf-8")
        code = df_briefer.apply_reply(conn, atlas, call_path, reply_path, out,
                                      max_records=60, context=8)
        if code == 2:
            break
        call_path = out / f"call_{step + 1:04d}.md"  # the auto-emitted regen
    assert code == 2  # EXHAUSTED after regens 0, 1, 2
    dry = (out / "dry_0003.md")
    assert dry.exists()
    dry_text = dry.read_text(encoding="utf-8")
    assert "dry floor — regen budget exhausted" in dry_text
    assert "subject: hf 500 · topic: col 1" in dry_text
    assert "'hf died' ev 1" in dry_text  # the beat renders its own records


def test_parse_call_roundtrip(conn_atlas, tmp_path: Path) -> None:
    conn, atlas = conn_atlas
    out = tmp_path / "session"
    call_path, _ = df_briefer.emit_call(
        conn, atlas, out, 500, 1, max_records=60, context=8
    )
    state = df_briefer.parse_call(call_path.read_text(encoding="utf-8"))
    assert state == df_briefer.CallState(
        hfid=500, col_id=1, anchor=2, regens=0, notes=()
    )


# -- case listing + the stress smoke ----------------------------------------


def test_case_listing_picks_riches_pov(conn_atlas) -> None:
    conn, atlas = conn_atlas
    listing = df_briefer.list_cases(conn, atlas, count=4, min_events=1)
    assert "battle 'The Tiny Onslaught'" in listing
    assert "POV candidate: hf 500 (2 in-battle records, 2 total)" in listing


def test_stress_smoke_runs_and_is_deterministic(
    conn_atlas, tiny_db: Path
) -> None:
    conn, atlas = conn_atlas
    report, summary = df_briefer.run_stress(tiny_db, atlas, picks=4)
    assert "content determinism (double-build byte-compare): PASS" in report
    assert summary["determinism"] == "PASS"
    assert summary["picks"] == 2  # only figures 500 and 501 have records
    assert "records/figure: p50 1 · p90 2" in report  # mentions [2, 1]
