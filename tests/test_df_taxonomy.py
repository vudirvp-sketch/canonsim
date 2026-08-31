"""Unit tests for `scripts/df_taxonomy.py` (bg-2 event taxonomy).

Pins the load-bearing survey behavior on a tiny synthetic DF-like world
(the `tests/test_df_import.py` pattern): plan selection over the sink DB,
plus-field dependency (theft detail), the witness blind-spot query
(reputation events key figures as hfid1/hfid2 — invisible to the
participant index, found through the EAV), presence-flag rendering,
the birth gap row, the collection plans (war/beast attack), content
determinism, and v1-sink degradation (plus-dependent plans yield zero
candidates instead of crashing).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

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
  <artifacts>
    <artifact><id>900</id><name>Hammer</name><site_id>10</site_id></artifact>
  </artifacts>
  <historical_figures>
    <historical_figure>
      <id>500</id><race>DWARF</race><caste>MALE</caste>
      <birth_year>100</birth_year><death_year>-1</death_year><name>Urist</name>
    </historical_figure>
    <historical_figure>
      <id>501</id><race>HUMAN</race><caste>MALE</caste>
      <birth_year>120</birth_year><death_year>180</death_year><name>Gob</name>
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
      <circumstance_id>2</circumstance_id>
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
  </historical_events>
  <historical_event_collections>
    <historical_event_collection>
      <id>1</id><type>war</type><start_year>200</start_year><end_year>210</end_year>
      <name>The Tiny War</name><aggressor_ent_id>100</aggressor_ent_id>
      <defender_ent_id>101</defender_ent_id>
      <event>1</event>
    </historical_event_collection>
    <historical_event_collection>
      <id>2</id><type>beast attack</type><start_year>215</start_year>
      <end_year>215</end_year><site_id>10</site_id><defending_enid>100</defending_enid>
      <event>3</event><event>5</event>
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
      <victim>-1</victim><race>goose</race><eater>500</eater><site>10</site>
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


def test_report_renders_entries_and_plus_detail(tiny_db: Path) -> None:
    report, summary = df_taxonomy.build_report(tiny_db, per_type=4)
    # Murder: roles resolve to names; the war grouping is reconstructed.
    assert "victim: Gob [hf 501, HUMAN]" in report
    assert "slayer: Urist [hf 500, DWARF]" in report
    assert "war col 1 'The Tiny War'" in report
    # Theft detail lives only in the plus companion and renders from it.
    assert "thief: Gob [hf 501, HUMAN]" in report
    assert "item: gold cup" in report
    assert "method: theft" in report
    assert "beast attack col 2" in report
    # Presence flag: an empty <return/> element renders as a yes.
    assert "return: yes" in report
    # The witness column finds the reputation link through hfid1/hfid2
    # even though those events carry no participant-index rows.
    assert "nearest 'hfs formed reputation relationship' ev 4 y202" in report
    assert "participants: (0,)" not in report  # sanity: no raw tuples leak
    assert summary["targets"] == 16
    # 13 event plans + 2 collection plans; the tiny world feeds five of them.
    assert summary["entries"] == 5


def test_birth_gap_is_measured(tiny_db: Path) -> None:
    report, _ = df_taxonomy.build_report(tiny_db, per_type=2)
    assert "GAP: no DF event type records births" in report
    assert "2 figures carry birth_year (100 .. 120)" in report


def test_war_and_beast_collection_entries(tiny_db: Path) -> None:
    report, _ = df_taxonomy.build_report(tiny_db, per_type=2)
    assert "name: 'The Tiny War' · aggressor guild [entity 100] vs defender kingdom" in report
    assert "no squad-deaths recorded" in report
    assert "beast: Urist [hf 500, DWARF]" in report
    assert "1 'creature devoured'" in report
    assert "no recorded death (alive or orphan)" in report


def test_report_is_deterministic(tiny_db: Path) -> None:
    first, _ = df_taxonomy.build_report(tiny_db, per_type=4)
    second, _ = df_taxonomy.build_report(tiny_db, per_type=4)
    assert first == second


def test_v1_sink_degrades_loudly_not_loudly_crashing(tmp_path: Path) -> None:
    main = tmp_path / "tiny-legends.xml"
    main.write_bytes(TINY_XML)
    db = tmp_path / "v1.sqlite3"
    df_import.import_world(main, db)  # no companion -> v1, no plus table
    report, summary = df_taxonomy.build_report(db, per_type=4)
    assert "WARNING: event_plus_fields missing (v1 sink)" in report
    assert "DEGRADED (v1 sink — plus fields absent)" in report
    assert "theft — DF 'item stolen' (0 candidates)" in report
    # the non-plus plans still render: murder, journey, war, catastrophe
    assert summary["entries"] == 4


def test_spread_is_bounded_and_deterministic() -> None:
    assert df_taxonomy._spread(0, 4) == []
    assert df_taxonomy._spread(3, 4) == [0, 1, 2]
    picks = df_taxonomy._spread(100, 8)
    assert len(picks) == 8
    assert picks[0] == 0 and picks[-1] == 99
    assert picks == sorted(set(picks))
    assert df_taxonomy._spread(100, 8) == picks
