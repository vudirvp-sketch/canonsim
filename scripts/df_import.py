"""DF Legends XML -> SQLite sink (bg-1 remainder; the bg-1-sqlite-sink pass).

Loads a `*-legends.xml` world export into one SQLite database — the
queryable home for the track-B spikes (bg-2 event taxonomy, bg-3 briefer
stress test). Reuses the validated sanitize+stream parsing core
(`df_survey.py`, iter-8e/8f/8g): byte-level CP437 sanitize, truncation
recovery, `iterparse` with per-record clearing — never DOM.

Schema laws (recipe owner: `docs/TECH_NOTES.md` §3.2; field plan owner:
the coverage matrix in `docs/ref/df_legends_xml.md`):

- HANDLED records (historical_event / _collection / _figure — the survey's
  F7/F8 detail set) get typed core tables plus an EAV field table for
  every other child tag; nested children are deterministic JSON
  (order-preserving, sorted keys). The audit's child-tag sets are the
  field plan.
- `event_participant (hfid, event_id)` lifts every direct child tag
  ending in `hfid` (the survey's context rule) — bg-3's "figure Y's own
  records" query is a PK prefix scan.
- Collection nesting is reconstructed from the parents' `<eventcol>`
  lists (the measured law: the `parent_eventcol` up-edge is almost never
  set); both sources land in `collection_parent`, deduplicated.
- Every other non-noise record (site, entity, artifact, written_content,
  region, underground_region, entity_population, historical_era, … plus
  any future UNDOCUMENTED tag) lands in one generic `records` table as a
  deterministic JSON payload — one code path, no per-tag schema upkeep.
- Design-noise sections (art/dance/musical/poetic forms) are counted and
  skipped (coverage-matrix law); the plus companion is NOT imported —
  selective import, never wholesale; deferred until bg-2/bg-3 need its
  complementary fields (recorded in `meta`).

Truncation policy (owns the KI#34 recovery semantics; D-051): default =
flagged PARTIAL import — the recovered prefix lands in the DB, `meta`
carries `partial=1`, warnings go to stderr; `--strict` aborts before
parsing instead. The record in flight at the cut lands with its parsed
prefix of fields (the recovering reader synthesizes its closing tag —
measured, KI#36; the survey counts it the same way, so sink and survey
counts agree on any export). The DB is always written fresh (existing
file unlinked; rebuildable index, D-003 analog).

Determinism stance (df_design.md quarantine): DB content is a pure
function of the export bytes — parse order, no wall-clock in `meta`, no
randomness; re-importing the same export yields identical rows. No
golden DF fixtures, no cross-DF-version byte-identity claims.

Usage:
    python scripts/df_import.py "dfworlds/<world>" [--out DIR] [--strict]

Output: `output/df_world_<stem>.sqlite3` (gitignored runtime artifact,
rebuildable from the same export). The exports themselves live outside
the repo (`dfworlds/` is gitignored).
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import df_survey  # the validated sanitize+stream parsing core (iter-8e/8f/8g)

REPO = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO / "output"

# Bump on schema change; migration = re-import (the DB is a rebuildable
# index of the export, not a canon artifact — INV-1/INV-5 do not apply).
SINK_VERSION = 1

# Design-noise skips — coverage-matrix law (`docs/ref/df_legends_xml.md`):
# briefer noise, not canon-relevant structure.
NOISE_SECTIONS = frozenset({
    "art_forms", "dance_forms", "musical_forms", "poetic_forms",
})

# Child tags lifted into typed columns / link tables instead of *_fields.
_EVENT_TYPED = frozenset({"id", "type", "year", "seconds72"})
_COLLECTION_TYPED = frozenset({
    "id", "type", "start_year", "end_year", "event", "eventcol", "parent_eventcol",
})
_FIGURE_TYPED = frozenset({"id", "race", "caste", "birth_year", "death_year"})

_FLUSH_EVERY = 4096  # records between batch flushes (the survey's section-clear rhythm)
_PROGRESS_EVERY = 262_144  # records between stderr progress lines

_TABLES = """
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    year INTEGER NOT NULL,
    seconds72 INTEGER NOT NULL
);
CREATE TABLE event_fields (
    event_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    PRIMARY KEY (event_id, key, value)
) WITHOUT ROWID;
CREATE TABLE event_participant (
    hfid INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    PRIMARY KEY (hfid, event_id)
) WITHOUT ROWID;
CREATE TABLE event_membership (
    event_id INTEGER NOT NULL,
    collection_id INTEGER NOT NULL,
    PRIMARY KEY (event_id, collection_id)
) WITHOUT ROWID;
CREATE TABLE collections (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    start_year INTEGER NOT NULL,
    end_year INTEGER NOT NULL
);
CREATE TABLE collection_fields (
    collection_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    PRIMARY KEY (collection_id, key, value)
) WITHOUT ROWID;
CREATE TABLE collection_parent (
    child_id INTEGER NOT NULL,
    parent_id INTEGER NOT NULL,
    PRIMARY KEY (child_id, parent_id)
) WITHOUT ROWID;
CREATE TABLE figures (
    id INTEGER PRIMARY KEY,
    race TEXT NOT NULL,
    caste TEXT NOT NULL,
    birth_year INTEGER NOT NULL,
    death_year INTEGER NOT NULL
);
CREATE TABLE figure_fields (
    figure_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    PRIMARY KEY (figure_id, key, value)
) WITHOUT ROWID;
CREATE TABLE records (
    record_tag TEXT NOT NULL,
    id INTEGER NOT NULL,
    data TEXT NOT NULL
);
"""

# Created after the bulk load — an indexed build is faster than indexed inserts.
_INDEXES = """
CREATE INDEX idx_events_type ON events(type);
CREATE INDEX idx_events_year ON events(year);
CREATE INDEX idx_event_fields_kv ON event_fields(key, value);
CREATE INDEX idx_membership_collection ON event_membership(collection_id);
CREATE INDEX idx_collection_parent_parent ON collection_parent(parent_id);
CREATE INDEX idx_records_tag_id ON records(record_tag, id);
"""


def _ref(text: str | None) -> int | None:
    """Parse an integer id reference; None when absent, unparseable, or -1."""
    if text is None:
        return None
    try:
        value = int(text)
    except ValueError:
        return None
    return value if value != -1 else None


def _nested_value(elem: ET.Element) -> str | list[Any] | dict[str, list[Any]]:
    """Native nested encoding: leaf text, or {tag: [values]} preserving
    repeats and parse order (the generic `records` payload)."""
    if len(elem) == 0:
        return elem.text or ""
    acc: dict[str, list[Any]] = {}
    for sub in elem:
        acc.setdefault(sub.tag, []).append(_nested_value(sub))
    return acc


def _child_value(child: ET.Element) -> str:
    """Deterministic EAV field value: leaf text, or canonical JSON of
    the nested structure (sorted keys; parse order preserved in lists)."""
    if len(child) == 0:
        return child.text or ""
    return json.dumps(_nested_value(child), ensure_ascii=False, sort_keys=True)


def _record_json(elem: ET.Element) -> str:
    """Whole-record deterministic JSON payload for the generic `records`
    table — nested natively so spikes navigate with plain json.loads."""
    acc: dict[str, list[Any]] = {}
    for child in elem:
        acc.setdefault(child.tag, []).append(_nested_value(child))
    return json.dumps(acc, ensure_ascii=False, sort_keys=True)


class _Importer:
    """Streaming record dispatcher: XML elements -> SQLite batch buffers."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self.counts: dict[str, int] = {}
        self._events: list[tuple[int, str, int, int]] = []
        self._event_fields: list[tuple[int, str, str]] = []
        self._participants: list[tuple[int, int]] = []
        self._membership: list[tuple[int, int]] = []
        self._collections: list[tuple[int, str, int, int]] = []
        self._collection_fields: list[tuple[int, str, str]] = []
        self._collection_parent: list[tuple[int, int]] = []
        self._figures: list[tuple[int, str, str, int, int]] = []
        self._figure_fields: list[tuple[int, str, str]] = []
        self._records: list[tuple[str, int, str]] = []

    def _bump(self, key: str) -> None:
        self.counts[key] = self.counts.get(key, 0) + 1

    # -- per-record handlers ------------------------------------------------

    def event(self, elem: ET.Element) -> None:
        event_id = df_survey._int_text(elem, "id")
        if event_id == -1:
            self._bump("malformed:historical_event")
            return
        event_type = elem.findtext("type") or "?"
        year = df_survey._int_text(elem, "year")
        seconds72 = df_survey._int_text(elem, "seconds72")
        self._events.append((event_id, event_type, year, seconds72))
        participants: set[int] = set()
        for child in elem:
            tag = child.tag
            if tag in _EVENT_TYPED:
                continue
            self._event_fields.append((event_id, tag, _child_value(child)))
            if tag.endswith("hfid"):
                hfid = _ref(child.text)
                if hfid is not None:
                    participants.add(hfid)
        self._participants.extend((hfid, event_id) for hfid in participants)

    def collection(self, elem: ET.Element) -> None:
        col_id = df_survey._int_text(elem, "id")
        if col_id == -1:
            self._bump("malformed:historical_event_collection")
            return
        col_type = elem.findtext("type") or "?"
        start_year = df_survey._int_text(elem, "start_year")
        end_year = df_survey._int_text(elem, "end_year")
        self._collections.append((col_id, col_type, start_year, end_year))
        for child in elem:
            tag = child.tag
            if tag == "event":
                ref = _ref(child.text)
                if ref is not None:
                    self._membership.append((ref, col_id))
            elif tag == "eventcol":
                ref = _ref(child.text)
                if ref is not None:
                    self._collection_parent.append((ref, col_id))
            elif tag == "parent_eventcol":
                ref = _ref(child.text)
                if ref is not None:
                    self._collection_parent.append((col_id, ref))
            elif tag in _COLLECTION_TYPED:
                continue
            else:
                self._collection_fields.append((col_id, tag, _child_value(child)))

    def figure(self, elem: ET.Element) -> None:
        figure_id = df_survey._int_text(elem, "id")
        if figure_id == -1:
            self._bump("malformed:historical_figure")
            return
        race = elem.findtext("race") or ""
        caste = elem.findtext("caste") or ""
        birth = df_survey._int_text(elem, "birth_year")
        death = df_survey._int_text(elem, "death_year")
        self._figures.append((figure_id, race, caste, birth, death))
        for child in elem:
            if child.tag in _FIGURE_TYPED:
                continue
            self._figure_fields.append((figure_id, child.tag, _child_value(child)))

    def record(self, tag: str, elem: ET.Element) -> None:
        record_id = df_survey._int_text(elem, "id")
        self._records.append((tag, record_id, _record_json(elem)))
        self._bump(f"records:{tag}")

    def noise(self, section_tag: str) -> None:
        self._bump(f"skipped:{section_tag}")

    # -- batch flushing -----------------------------------------------------

    def flush(self) -> None:
        # INSERT OR IGNORE on the EAV/link tables: identical duplicate
        # (id, key, value) triples are redundant (repeated XML tags), and
        # collection_parent deliberately feeds two sources (the parent's
        # <eventcol> list + the child's parent_eventcol up-edge) that can
        # agree. Distinct values never collide — the typed cores keep
        # plain INSERT so a true duplicate id still fails loud.
        conn = self._conn
        if self._events:
            conn.executemany("INSERT INTO events VALUES (?,?,?,?)", self._events)
            self._events.clear()
        if self._event_fields:
            conn.executemany(
                "INSERT OR IGNORE INTO event_fields VALUES (?,?,?)", self._event_fields
            )
            self._event_fields.clear()
        if self._participants:
            conn.executemany(
                "INSERT OR IGNORE INTO event_participant VALUES (?,?)", self._participants
            )
            self._participants.clear()
        if self._membership:
            conn.executemany(
                "INSERT OR IGNORE INTO event_membership VALUES (?,?)", self._membership
            )
            self._membership.clear()
        if self._collections:
            conn.executemany("INSERT INTO collections VALUES (?,?,?,?)", self._collections)
            self._collections.clear()
        if self._collection_fields:
            conn.executemany(
                "INSERT OR IGNORE INTO collection_fields VALUES (?,?,?)",
                self._collection_fields,
            )
            self._collection_fields.clear()
        if self._collection_parent:
            conn.executemany(
                "INSERT OR IGNORE INTO collection_parent VALUES (?,?)",
                self._collection_parent,
            )
            self._collection_parent.clear()
        if self._figures:
            conn.executemany("INSERT INTO figures VALUES (?,?,?,?,?)", self._figures)
            self._figures.clear()
        if self._figure_fields:
            conn.executemany(
                "INSERT OR IGNORE INTO figure_fields VALUES (?,?,?)", self._figure_fields
            )
            self._figure_fields.clear()
        if self._records:
            conn.executemany("INSERT INTO records VALUES (?,?,?)", self._records)
            self._records.clear()


def import_world(main_path: Path, db_path: Path, *, strict: bool = False) -> dict[str, str]:
    """Import one legends XML into a fresh SQLite DB; return the meta mapping.

    The DB is always rebuilt from scratch (existing file unlinked). Content
    is a pure function of the export bytes — no wall-clock, no randomness.
    """
    if strict and not df_survey._tail_closes_root(main_path):
        raise SystemExit(
            f"ERROR: {main_path.name}: truncated export (no </df_world> at EOF)"
            " and --strict is set — aborting before import; re-export the world"
            " or drop --strict for a flagged partial import"
        )
    if db_path.exists():
        db_path.unlink()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, isolation_level=None)
    # Rebuildable runtime artifact: no journal, no fsync per commit (D-003
    # analog — the DB is an index of the export, never a source of truth).
    conn.execute("PRAGMA journal_mode=OFF")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("PRAGMA cache_size=-65536")  # 64 MB page cache
    conn.executescript(_TABLES)
    conn.execute("BEGIN")

    importer = _Importer(conn)
    reader = df_survey._make_reader(main_path)  # prints PARTIAL warnings itself
    partial = isinstance(reader, df_survey.RecoveringReader)
    started = time.perf_counter()
    records = 0
    depth = 0
    section: ET.Element | None = None
    try:
        for event, elem in ET.iterparse(reader, events=("start", "end")):
            if event == "start":
                depth += 1
                if depth == 2:
                    section = elem
                continue
            if depth == 3:
                if section is not None:
                    if section.tag in NOISE_SECTIONS:
                        importer.noise(section.tag)
                    else:
                        tag = elem.tag
                        if tag == "historical_event":
                            importer.event(elem)
                        elif tag == "historical_event_collection":
                            importer.collection(elem)
                        elif tag == "historical_figure":
                            importer.figure(elem)
                        else:
                            importer.record(tag, elem)
                    records += 1
                elem.clear()
                if records % _FLUSH_EVERY == 0:
                    if section is not None:
                        section.clear()
                    importer.flush()
                    if records % _PROGRESS_EVERY == 0:
                        print(f"  {records:,} records ...", file=sys.stderr)
            depth -= 1
    finally:
        reader.close()

    importer.flush()
    conn.execute("COMMIT")
    conn.executescript(_INDEXES)

    # Row counts read back from the tables — exact, not buffer estimates.
    table_counts = {
        table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in (
            "events", "event_fields", "event_participant", "event_membership",
            "collections", "collection_fields", "collection_parent",
            "figures", "figure_fields", "records",
        )
    }

    meta: dict[str, str] = {
        "sink_version": str(SINK_VERSION),
        "source": main_path.name,
        "source_bytes": str(main_path.stat().st_size),
        "sanitized_bytes": str(reader.replaced),
        "partial": "1" if partial else "0",
        "plus_companion": "skipped",
        "skipped_sections": ",".join(sorted(NOISE_SECTIONS)),
    }
    meta.update({key: str(value) for key, value in table_counts.items()})
    meta.update({key: str(value) for key, value in sorted(importer.counts.items())})
    conn.executemany("INSERT INTO meta VALUES (?,?)", sorted(meta.items()))
    conn.execute("ANALYZE")
    conn.close()
    print(
        f"  {records:,} records -> {db_path.name}"
        f" ({db_path.stat().st_size / 1e6:.0f} MB)"
        f" in {time.perf_counter() - started:.0f}s"
        + ("  [PARTIAL — truncated export]" if partial else ""),
        file=sys.stderr,
    )
    return meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "targets", nargs="+",
        help="legends.xml file(s) or world directory(ies) containing them",
    )
    parser.add_argument(
        "--out", type=Path, default=DEFAULT_OUT,
        help=f"output directory (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="abort on truncated exports instead of a flagged partial import",
    )
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)

    for main_path, plus_path in df_survey.find_worlds(args.targets):
        print(f"importing {main_path} ...", file=sys.stderr)
        if plus_path is not None:
            print(f"  companion {plus_path.name}: skipped (selective import;"
                  " deferred until bg-2/bg-3 need its fields)", file=sys.stderr)
        stem = main_path.name.removesuffix("-legends.xml")
        db_path = args.out / f"df_world_{stem}.sqlite3"
        meta = import_world(main_path, db_path, strict=args.strict)
        shown = (
            "events", "collections", "figures", "event_participant",
            "event_membership", "collection_parent", "records",
        )
        summary = " · ".join(f"{k} {int(v):,}" for k, v in meta.items() if k in shown)
        print(f"  {summary}")
        print(f"  db: {db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
