"""Unit tests for `scripts/df_import.py` (bg-1 SQLite sink).

Pins the load-bearing sink invariants on a tiny synthetic DF-like XML
(the `tests/test_df_survey.py` pattern): typed core + EAV extraction,
the participant index, collection-membership/parent links, the generic
records path (incl. id-less records and noise skips), the truncation
policy (flagged partial default, --strict abort), and content
determinism (same export bytes -> identical rows).
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import df_import  # type: ignore[import-not-found]  # noqa: E402

TINY_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<df_world>
  <regions>
    <region><id>1</id><name>woods</name></region>
  </regions>
  <sites>
    <site>
      <id>10</id>
      <type>tavern</type>
      <name>The Stow</name>
      <coords>x5y6</coords>
      <structures>
        <structure><local_id>0</local_id><type>market</type></structure>
      </structures>
    </site>
  </sites>
  <entities>
    <entity><id>100</id><name>guild</name><type>guild</type></entity>
  </entities>
  <artifacts>
    <artifact><id>900</id><name>Hammer</name><site_id>10</site_id></artifact>
  </artifacts>
  <historical_eras>
    <historical_era><name>Age of Myth</name><start_year>0</start_year></historical_era>
  </historical_eras>
  <dance_forms>
    <dance_form><id>700</id><description>a dance</description></dance_form>
  </dance_forms>
  <historical_figures>
    <historical_figure>
      <id>500</id>
      <race>DWARF</race>
      <caste>MALE</caste>
      <birth_year>100</birth_year>
      <death_year>-1</death_year>
      <name><name_string>Urist</name_string></name>
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
      <seconds72>-1</seconds72>
      <hfid>501</hfid>
      <slayer_hfid>500</slayer_hfid>
      <cause>struck</cause>
      <site_id>10</site_id>
    </historical_event>
    <historical_event>
      <id>2</id>
      <type>artifact created</type>
      <year>205</year>
      <seconds72>1000</seconds72>
      <artifact_id>900</artifact_id>
      <creator_hfid>500</creator_hfid>
      <hfid>500</hfid>
      <hfid>500</hfid>
      <party><member_hfid>501</member_hfid></party>
    </historical_event>
    <historical_event>
      <id>3</id>
      <type>trade</type>
      <year>206</year>
      <hfid>-1</hfid>
      <hfid>garbage</hfid>
    </historical_event>
  </historical_events>
  <historical_event_collections>
    <historical_event_collection>
      <id>1</id>
      <type>war</type>
      <start_year>200</start_year>
      <end_year>210</end_year>
      <attacker_civ_id>100</attacker_civ_id>
      <event>1</event>
      <event>2</event>
      <eventcol>2</eventcol>
    </historical_event_collection>
    <historical_event_collection>
      <id>2</id>
      <type>battle</type>
      <start_year>201</start_year>
      <end_year>201</end_year>
      <parent_eventcol>1</parent_eventcol>
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


def _rows(db_path: Path, sql: str) -> list[tuple]:
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute(sql).fetchall()
    finally:
        conn.close()


@pytest.fixture
def tiny_db(tiny_xml: Path, tmp_path: Path) -> Path:
    db = tmp_path / "tiny.sqlite3"
    df_import.import_world(tiny_xml, db)
    return db


def test_typed_cores_and_eav_fields(tiny_db: Path) -> None:
    # Typed event core; type/year/seconds72 never duplicated into EAV.
    assert _rows(tiny_db, "SELECT * FROM events ORDER BY id") == [
        (1, "hf died", 200, -1),
        (2, "artifact created", 205, 1000),
        (3, "trade", 206, -1),
    ]
    # EAV: every non-typed child tag, nested children as canonical JSON.
    fields = dict(_rows(
        tiny_db, "SELECT key, value FROM event_fields WHERE event_id = 1",
    ))
    assert fields["cause"] == "struck"
    assert fields["site_id"] == "10"
    nested = dict(_rows(
        tiny_db, "SELECT key, value FROM event_fields WHERE event_id = 2",
    ))["party"]
    assert nested == json.dumps({"member_hfid": ["501"]}, sort_keys=True)
    # Repeated identical tags collapse on the EAV primary key.
    assert _rows(
        tiny_db, "SELECT COUNT(*) FROM event_fields WHERE event_id = 2 AND key = 'hfid'",
    ) == [(1,)]


def test_participant_index_lifts_direct_hfid_tags_only(tiny_db: Path) -> None:
    # Direct children ending in 'hfid' (hfid, slayer_hfid, creator_hfid);
    # -1 and unparseable values excluded; identical repeats deduplicated;
    # nested <party><member_hfid> stays in event_fields, not participants.
    assert _rows(tiny_db, "SELECT * FROM event_participant ORDER BY hfid, event_id") == [
        (500, 1), (500, 2), (501, 1),
    ]


def test_collection_membership_and_parent_links(tiny_db: Path) -> None:
    # Membership from the parents' <event> children — multi-parent events
    # survive (event 2 sits in both collections).
    assert _rows(tiny_db, "SELECT * FROM event_membership ORDER BY 1, 2") == [
        (1, 1), (2, 1), (2, 2),
    ]
    # Parent links from BOTH sources, deduplicated: the parent's
    # <eventcol> child list and the child's parent_eventcol up-edge.
    assert _rows(tiny_db, "SELECT * FROM collection_parent") == [(2, 1)]
    assert _rows(tiny_db, "SELECT * FROM collections ORDER BY id") == [
        (1, "war", 200, 210), (2, "battle", 201, 201),
    ]


def test_figures_typed_and_nested_name_json(tiny_db: Path) -> None:
    assert _rows(tiny_db, "SELECT * FROM figures ORDER BY id") == [
        (500, "DWARF", "MALE", 100, -1),
        (501, "HUMAN", "", 120, 180),
    ]
    name = _rows(tiny_db, "SELECT value FROM figure_fields WHERE key = 'name'")
    assert name == [(json.dumps({"name_string": ["Urist"]}, sort_keys=True),)]


def test_generic_records_path(tiny_db: Path) -> None:
    # Non-noise UNHANDLED records land as JSON payloads; id-less records
    # (historical_era) carry -1; noise sections are counted, not stored.
    tags = dict(_rows(
        tiny_db, "SELECT record_tag, COUNT(*) FROM records GROUP BY record_tag",
    ))
    assert tags == {
        "region": 1, "site": 1, "entity": 1, "artifact": 1, "historical_era": 1,
    }
    site = _rows(
        tiny_db, "SELECT data FROM records WHERE record_tag = 'site' AND id = 10",
    )[0][0]
    payload = json.loads(site)
    assert payload["name"] == ["The Stow"]
    assert payload["structures"][0]["structure"][0]["local_id"] == ["0"]
    era = _rows(tiny_db, "SELECT id, data FROM records WHERE record_tag = 'historical_era'")
    assert era[0][0] == -1
    assert json.loads(era[0][1])["name"] == ["Age of Myth"]


def test_meta_records_policy_and_counts(tiny_db: Path) -> None:
    meta = dict(_rows(tiny_db, "SELECT key, value FROM meta"))
    assert meta["sink_version"] == str(df_import.SINK_VERSION)
    assert meta["source"] == "tiny-legends.xml"
    assert meta["partial"] == "0"
    assert meta["plus_companion"] == "skipped"
    assert "dance_forms" in meta["skipped_sections"]
    assert meta["events"] == "3"
    assert meta["collections"] == "2"
    assert meta["figures"] == "2"
    assert meta["records"] == "5"
    assert meta["skipped:dance_forms"] == "1"
    assert meta["sanitized_bytes"] == "0"


def test_truncated_default_is_flagged_partial(tmp_path: Path) -> None:
    cut = tmp_path / "cut-legends.xml"
    cut.write_bytes(
        b"<df_world><historical_events>"
        b"<historical_event><id>1</id><type>hf died</type><year>9</year>"
        b"<hfid>7</hfid>"  # cut mid-record after a participant field
    )
    db = tmp_path / "cut.sqlite3"
    meta = df_import.import_world(cut, db)
    # The in-flight record lands with its parsed prefix of fields (KI#36
    # measured behavior — the recovering reader closes it); the whole DB
    # is flagged partial.
    assert meta["partial"] == "1"
    assert meta["events"] == "1"
    assert _rows(db, "SELECT id, type, year FROM events") == [(1, "hf died", 9)]
    assert _rows(db, "SELECT * FROM event_participant") == [(7, 1)]


def test_strict_aborts_before_import(tmp_path: Path) -> None:
    cut = tmp_path / "cut-legends.xml"
    cut.write_bytes(b"<df_world><historical_events><historical_event><id>1</id>")
    db = tmp_path / "cut.sqlite3"
    with pytest.raises(SystemExit, match="--strict"):
        df_import.import_world(cut, db, strict=True)
    # Nothing was written.
    assert not db.exists()


def test_reimport_is_content_deterministic(tiny_xml: Path, tmp_path: Path) -> None:
    """Same export bytes -> identical rows in every table (the df_design
    determinism quarantine: content-level, no wall-clock in meta)."""
    db_a = tmp_path / "a.sqlite3"
    db_b = tmp_path / "b.sqlite3"
    df_import.import_world(tiny_xml, db_a)
    df_import.import_world(tiny_xml, db_b)
    tables = (
        "meta", "events", "event_fields", "event_participant", "event_membership",
        "collections", "collection_fields", "collection_parent",
        "figures", "figure_fields", "records",
    )
    for table in tables:
        sql = f"SELECT * FROM {table} ORDER BY 1, 2"
        assert _rows(db_a, sql) == _rows(db_b, sql), f"table {table} diverged"


def test_bg3_figure_records_query(tiny_db: Path) -> None:
    """The consumer query bg-3 names ("figure Y's own records") is a
    participant-index prefix scan joined against the typed core."""
    rows = _rows(
        tiny_db,
        "SELECT e.id, e.type, e.year FROM event_participant p"
        " JOIN events e ON e.id = p.event_id"
        " WHERE p.hfid = 500 ORDER BY e.id",
    )
    assert rows == [(1, "hf died", 200), (2, "artifact created", 205)]


def test_fresh_rebuild_unlinks_existing_db(tiny_xml: Path, tmp_path: Path) -> None:
    """The DB is a rebuildable index: importing over an existing file
    starts fresh instead of appending (D-003 analog)."""
    db = tmp_path / "rebuild.sqlite3"
    df_import.import_world(tiny_xml, db)
    df_import.import_world(tiny_xml, db)
    assert _rows(db, "SELECT COUNT(*) FROM events") == [(3,)]
