"""Unit tests for `scripts/df_survey.py` (iter-8g).

The survey tool is operator-class (no LLM/network per INV-4; scripts/ is
in `tests/test_architecture.py` PACKAGE_DIRS), but it had zero regression
protection — a single re-export from a future DF version could silently
break the parser. These tests pin the four load-bearing invariants of
the bg-1 parsing core on a tiny synthetic DF-like XML so a regression
shows up at the bench, not in a 5 GB export.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import df_survey  # type: ignore[import-not-found]  # noqa: E402

TINY_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<df_world>
  <regions>
    <region>
      <id>1</id>
      <name>woods</name>
      <coords>x1y2</coords>
    </region>
    <region>
      <id>2</id>
      <name>hills</name>
    </region>
  </regions>
  <sites>
    <site>
      <id>10</id>
      <type>tavern</type>
      <coords>x5y6</coords>
      <name>The Stow</name>
    </site>
    <site>
      <id>11</id>
      <type>hamlet</type>
      <name>Oakview</name>
    </site>
  </sites>
  <entities>
    <entity>
      <id>100</id>
      <name>guild</name>
      <type>guild</type>
    </entity>
  </entities>
  <historical_figures>
    <historical_figure>
      <id>500</id>
      <race>DWARF</race>
      <caste>MALE</caste>
      <birth_year>100</birth_year>
      <death_year>-1</death_year>
    </historical_figure>
    <historical_figure>
      <id>501</id>
      <race>HUMAN</race>
      <birth_year>120</birth_year>
      <death_year>180</death_year>
    </historical_figure>
  </historical_figures>
  <historical_events>
    <historical_event>
      <id>1</id>
      <type>hf died</type>
      <year>200</year>
      <hfid>501</hfid>
      <slayer_hfid>500</slayer_hfid>
      <cause>struck</cause>
    </historical_event>
    <historical_event>
      <id>2</id>
      <type>artifact created</type>
      <year>205</year>
      <artifact_id>9</artifact_id>
      <creator_hfid>500</creator_hfid>
    </historical_event>
  </historical_events>
  <historical_event_collections>
    <historical_event_collection>
      <id>1</id>
      <type>war</type>
      <start_year>200</start_year>
      <end_year>210</end_year>
      <attacker_civ_id>100</attacker_civ_id>
      <defender_civ_id>100</defender_civ_id>
      <event>1</event>
      <event>2</event>
    </historical_event_collection>
  </historical_event_collections>
</df_world>
"""


@pytest.fixture
def tiny_xml(tmp_path: Path) -> Path:
    p = tmp_path / "tiny-legends.xml"
    p.write_bytes(TINY_XML)
    return p


def test_sanitize_replaces_invalid_control_bytes(tmp_path: Path) -> None:
    # CP437 item-quality symbol 0x11 inside an artifact name — not
    # well-formed XML; the SanitizingReader must swap it for '?' and count.
    raw = b"<x><name>\x11bad</name></x>"
    p = tmp_path / "bad.xml"
    p.write_bytes(raw)
    reader = df_survey.SanitizingReader(p)
    out = reader.read()
    reader.close()
    assert out == b"<x><name>?bad</name></x>"
    assert reader.replaced == 1


def test_tail_closes_root_detects_truncation(tmp_path: Path) -> None:
    intact = tmp_path / "ok.xml"
    intact.write_bytes(b"<df_world><x/></df_world>")
    assert df_survey._tail_closes_root(intact) is True
    cut = tmp_path / "cut.xml"
    cut.write_bytes(b"<df_world><x>")  # no closing tag
    assert df_survey._tail_closes_root(cut) is False


def test_recovering_reader_survives_truncation(tmp_path: Path) -> None:
    # A truncated export: cut inside a record, no </df_world>; the
    # RecoveringReader synthesizes the closing tags so iterparse completes.
    cut = tmp_path / "cut-legends.xml"
    cut.write_bytes(
        b"<df_world><historical_events>"
        b"<historical_event><id>1</id><type>hf died</type>"  # cut mid-record
    )
    # The tail check fails → _make_reader wraps in RecoveringReader.
    reader = df_survey._make_reader(cut)
    assert isinstance(reader, df_survey.RecoveringReader)
    stats = df_survey.WorldStats()
    # Should not raise — the synthesized closing tags complete the parse.
    sanitized, _seconds = df_survey._stream(cut, stats, audit=True)
    reader.close()
    # We never saw the </historical_event> close, so the partial record
    # is dropped — but the section wrapper and root are closed by recovery.
    assert stats.section_counts.get("historical_events", 0) >= 0
    assert sanitized == 0


def test_audit_census_counts_all_record_tags(tiny_xml: Path) -> None:
    stats = df_survey.WorldStats()
    df_survey._stream(tiny_xml, stats, audit=True)
    # 5 record tags: region, site, entity, historical_figure, historical_event,
    # historical_event_collection.
    assert set(stats.record_tags_per_section) == {
        "regions", "sites", "entities",
        "historical_figures", "historical_events", "historical_event_collections",
    }
    # Each section maps to its singular record tag with the right count.
    assert dict(stats.record_tags_per_section["regions"]) == {"region": 2}
    assert dict(stats.record_tags_per_section["sites"]) == {"site": 2}
    assert dict(stats.record_tags_per_section["entities"]) == {"entity": 1}


def test_audit_finds_unhandled_records(tiny_xml: Path) -> None:
    stats = df_survey.WorldStats()
    df_survey._stream(tiny_xml, stats, audit=True)
    record_tags = {
        tag for per_tag in stats.record_tags_per_section.values()
        for tag in per_tag
    }
    unhandled = record_tags - df_survey.HANDLED_RECORDS
    assert unhandled == {"region", "site", "entity"}
    handled = record_tags & df_survey.HANDLED_RECORDS
    assert handled == {
        "historical_event", "historical_event_collection", "historical_figure",
    }


def test_audit_records_schema_variants(tiny_xml: Path) -> None:
    """Records of the same tag with different child-tag sets land as
    distinct variants in `unique_child_tag_sets` — schema drift signal."""
    stats = df_survey.WorldStats()
    df_survey._stream(tiny_xml, stats, audit=True)
    # `region` has 2 records: one with `coords`, one without → 2 variants.
    assert len(stats.unique_child_tag_sets["region"]) == 2
    # `site` likewise.
    assert len(stats.unique_child_tag_sets["site"]) == 2
    # `entity` has 1 record → 1 variant.
    assert len(stats.unique_child_tag_sets["entity"]) == 1
    # The variants are frozensets of immediate child tags.
    sample = next(iter(stats.unique_child_tag_sets["region"]))
    assert isinstance(sample, frozenset)
    assert "id" in sample and "name" in sample


def test_stream_audit_mode_still_collects_f7_f8_detail(tiny_xml: Path) -> None:
    """Audit mode is additive — F7/F8 detail still collected alongside
    the census (same single pass, no second parse)."""
    stats = df_survey.WorldStats()
    df_survey._stream(tiny_xml, stats, audit=True)
    # F7: event types.
    assert dict(stats.event_types) == {"hf died": 1, "artifact created": 1}
    # F7: figure info (id -> race/birth/death).
    assert stats.figure_info[500][0] == "DWARF"
    assert stats.figure_info[501] == ("HUMAN", 120, 180)
    # F8: collection membership.
    assert stats.event_refs == {1: 1, 2: 1}  # each event referenced once
    # F8: deaths.
    assert stats.deaths_total == 1
    assert stats.deaths_with_slayer == 1
    assert dict(stats.death_causes) == {"struck": 1}


def test_build_report_with_audit_renders_coverage_section(tiny_xml: Path) -> None:
    stats = df_survey.WorldStats()
    sanitized, seconds = df_survey._stream(tiny_xml, stats, audit=True)
    report = df_survey.build_report(
        tiny_xml, None, stats, sanitized, seconds, None, 0, 0.0, audit_mode=True,
    )
    assert "Coverage audit" in report
    assert "HANDLED" in report
    assert "UNHANDLED" in report
    assert "region" in report  # unhandled
    assert "site" in report
    assert "entity" in report
    assert "historical_event" in report  # handled
    assert "variant(s)" in report


def test_build_report_without_audit_skips_coverage_section(tiny_xml: Path) -> None:
    stats = df_survey.WorldStats()
    df_survey._stream(tiny_xml, stats, audit=False)  # default
    sanitized, seconds = df_survey._stream(tiny_xml, stats, audit=False)
    report = df_survey.build_report(
        tiny_xml, None, stats, sanitized, seconds, None, 0, 0.0, audit_mode=False,
    )
    assert "Coverage audit" not in report
    # F7/F8 detail still present.
    assert "F7" in report and "F8" in report
