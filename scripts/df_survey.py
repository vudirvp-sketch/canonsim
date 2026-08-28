"""DF Legends XML empirical survey (iter-8e; owner-requested F7/F8 verification).

Streams one or more `*-legends.xml` exports (plus the sibling
`*-legends_plus.xml` for a structural scan) and measures what `docs/ref/
df_design.md` F7 (macro-dense, micro-empty) and F8 (causality as
archaeology) claim about the corpus:

- scale: section -> record counts, file sizes, companion sections;
- F7: event-type distribution classified into 7 categories (the table
  below is the classification owner), top-N concentration, events-per-year
  histogram, events-per-figure participation + concentration;
- F8: collection-reference counts per event (the 2+ refs share = the
  `candidate_causes` rate for bg-2), orphan share (no collection ref, no
  figure-role field, no cause), `hf died` slayer/cause breakdown,
  collection nesting.

`--audit` (iter-8g): coverage census instead of measured F7/F8 detail.
For every top-level section: per-record-tag counts + the set of all
unique child-tag sets per record tag (DF records are uniform within a
type, so this set is small — typically 1-3 variants; >3 = schema drift
signal). HANDLED records (historical_event / _collection / _figure —
F7/F8 detail above) are marked, UNHANDLED records (site, entity, artifact,
written_content, region, landmass, mountain_peak, river, creature_raw,
entity_population, dance/musical/poetic form, …) are listed with their
unique child-tag sets so bg-1's SQLite sink can plan field extraction
without re-parsing the export. The audit replaces head/middle/tail
positional sampling: it is strictly more information (every structural
variant is captured, not just three positions) and is bounded by record
uniformity.

Parsing law (bg-1 hardening, `docs/ref/df_design.md` "What we adapt"):
stream with `iterparse` + element `clear()` + periodic section `clear()`
(never DOM), sanitize XML-invalid control bytes at the byte level (the DF
exporter writes raw CP437 quality symbols into artifact names — measured:
12–24 bytes per world), no network. Truncated exports (the exporter can die
mid-write, losing `</df_world>`; measured on a 2.9 GB export) are caught
by a tail check and recovered best-effort: the missing closing tags are
synthesized at EOF so the parse completes, with loud PARTIAL warnings.
This script is the parsing core bg-1's SQLite loader is expected to reuse
(truncation survival since iter-8f).

Track law: pure stdlib counting — no RNG, no network, no LLM (INV-4);
report content is deterministic (sorted tables); the trailing
"environment" block (wall time, peak RSS) is informational only.

Usage:
    python scripts/df_survey.py "/path/region1-00250-01-01-legends.xml"
    python scripts/df_survey.py --audit "/path/region1-00250-01-01-legends.xml"
    python scripts/df_survey.py /path/dfworlds/

Output: `output/df_survey_<stem>.txt` (gitignored runtime artifact,
reproducible from the same export) + a stdout summary. The exports
themselves live outside the repo (`dfworlds/` is gitignored).
"""

from __future__ import annotations

import argparse
import collections
import os
import re
import resource
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import BinaryIO

REPO = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO / "output"

# --- F7 classification (the single owner of the category assignment). ---
# Keys are the literal `<type>` strings of the exports (display style with
# spaces — NOT snake_case; KI#33). Covers the type vocabulary measured
# across the owner's exports — the count lives in `docs/TECH_NOTES.md`
# §3.1 (single owner); an unknown type lands in UNCLASSIFIED and is
# reported loudly so the table can be extended (KI#35: "site tribute
# forced" was the first such extension).
CATEGORY_MICRO = "micro (street/personal life)"
CATEGORIES = (
    "bookkeeping",
    "war-geopolitics",
    "personal-violence",
    CATEGORY_MICRO,
    "occasion-ritual",
    "artifact-culture",
    "arcane",
)

TYPE_CATEGORY: dict[str, str] = {
    # bookkeeping: state/job/link/identity churn + org & site lifecycle
    "change hf state": "bookkeeping",
    "change hf job": "bookkeeping",
    "change hf body state": "bookkeeping",
    "add hf entity link": "bookkeeping",
    "remove hf entity link": "bookkeeping",
    "add hf hf link": "bookkeeping",
    "remove hf hf link": "bookkeeping",
    "add hf site link": "bookkeeping",
    "remove hf site link": "bookkeeping",
    "create entity position": "bookkeeping",
    "add hf entity honor": "bookkeeping",
    "entity law": "bookkeeping",
    "building profile acquired": "bookkeeping",
    "modified building": "bookkeeping",
    "replaced structure": "bookkeeping",
    "entity relocate": "bookkeeping",
    "entity equipment purchase": "bookkeeping",
    "regionpop incorporated into entity": "bookkeeping",
    "entity created": "bookkeeping",
    "created site": "bookkeeping",
    "created structure": "bookkeeping",
    "created world construction": "bookkeeping",
    "new site leader": "bookkeeping",
    "entity incorporated": "bookkeeping",
    "entity dissolved": "bookkeeping",
    "entity alliance formed": "bookkeeping",
    "entity primary criminals": "bookkeeping",
    "hf recruited unit type for entity": "bookkeeping",
    "hf travel": "bookkeeping",
    # war-geopolitics: macro conflict, conquest, diplomacy
    "field battle": "war-geopolitics",
    "attacked site": "war-geopolitics",
    "plundered site": "war-geopolitics",
    "site taken over": "war-geopolitics",
    "destroyed site": "war-geopolitics",
    "razed structure": "war-geopolitics",
    "entity persecuted": "war-geopolitics",
    "entity overthrown": "war-geopolitics",
    "peace accepted": "war-geopolitics",
    "peace rejected": "war-geopolitics",
    "site dispute": "war-geopolitics",
    "site tribute forced": "war-geopolitics",
    "reclaim site": "war-geopolitics",
    "hf attacked site": "war-geopolitics",
    "hf destroyed site": "war-geopolitics",
    "entity breach feature layer": "war-geopolitics",
    "holy city declaration": "war-geopolitics",
    # personal-violence: single-figure-scale harm (notable biography)
    "hf died": "personal-violence",
    "hf wounded": "personal-violence",
    "hf simple battle event": "personal-violence",
    "creature devoured": "personal-violence",
    "body abused": "personal-violence",
    "hf abducted": "personal-violence",
    "hf performed horrible experiments": "personal-violence",
    "hf disturbed structure": "personal-violence",
    # micro: relations, reputation, intrigue, secrets, economy, transgression
    "hfs formed reputation relationship": CATEGORY_MICRO,
    "hf relationship denied": CATEGORY_MICRO,
    "hf reunion": CATEGORY_MICRO,
    "hfs formed intrigue relationship": CATEGORY_MICRO,
    "failed intrigue corruption": CATEGORY_MICRO,
    "failed frame attempt": CATEGORY_MICRO,
    "hf confronted": CATEGORY_MICRO,
    "hf interrogated": CATEGORY_MICRO,
    "hf convicted": CATEGORY_MICRO,
    "hf gains secret goal": CATEGORY_MICRO,
    "assume identity": CATEGORY_MICRO,
    "hf profaned structure": CATEGORY_MICRO,
    "sabotage": CATEGORY_MICRO,
    "hf enslaved": CATEGORY_MICRO,
    "hf ransomed": CATEGORY_MICRO,
    "trade": CATEGORY_MICRO,
    "gamble": CATEGORY_MICRO,
    "agreement formed": CATEGORY_MICRO,
    "hf equipment purchase": CATEGORY_MICRO,
    "hf new pet": CATEGORY_MICRO,
    # occasion-ritual: community events
    "performance": "occasion-ritual",
    "ceremony": "occasion-ritual",
    "procession": "occasion-ritual",
    "competition": "occasion-ritual",
    "hf preach": "occasion-ritual",
    "hf prayed inside structure": "occasion-ritual",
    # artifact-culture: artifacts, books, forms, knowledge
    "artifact created": "artifact-culture",
    "artifact stored": "artifact-culture",
    "item stolen": "artifact-culture",
    "artifact lost": "artifact-culture",
    "artifact given": "artifact-culture",
    "artifact claim formed": "artifact-culture",
    "artifact destroyed": "artifact-culture",
    "artifact copied": "artifact-culture",
    "artifact found": "artifact-culture",
    "artifact recovered": "artifact-culture",
    "artifact possessed": "artifact-culture",
    "hf viewed artifact": "artifact-culture",
    "written content composed": "artifact-culture",
    "musical form created": "artifact-culture",
    "poetic form created": "artifact-culture",
    "dance form created": "artifact-culture",
    "knowledge discovered": "artifact-culture",
    # arcane: supernatural transformations and secrets
    "hf does interaction": "arcane",
    "changed creature type": "arcane",
    "hf revived": "arcane",
    "hf learns secret": "arcane",
}

_UNKNOWN = "UNCLASSIFIED"

# Records the survey extracts detail from (F7/F8); everything else on
# depth=3 is counted + structurally fingerprinted by `--audit` only.
HANDLED_RECORDS = frozenset({
    "historical_event",
    "historical_event_collection",
    "historical_figure",
})


def _sanitize_table() -> bytes:
    """256-byte translation table: XML-invalid control bytes -> '?'."""
    return bytes(
        0x3F if (b < 0x09 or b in (0x0B, 0x0C) or 0x0E <= b < 0x20) else b
        for b in range(256)
    )


class SanitizingReader:
    """Byte-level file wrapper stripping XML-invalid control bytes.

    The DF exporter writes raw CP437 bytes (item-quality symbols 0x10/0x11)
    inside artifact `<name_string>` elements, which makes the file not
    well-formed XML (measured: 24 invalid bytes per world, 12 artifacts).
    Invalid bytes are replaced with `?` and counted. Byte-level filtering
    is safe: CP437 is single-byte and UTF-8 continuation bytes are >= 0x80.
    """

    _TABLE = _sanitize_table()
    _CLEAN = bytes(range(256))

    def __init__(self, path: Path) -> None:
        self._f: BinaryIO = open(path, "rb")  # noqa: SIM115
        self.replaced = 0

    def read(self, size: int = -1) -> bytes:
        data = self._f.read(size)
        if not data:
            return data
        clean = data.translate(self._TABLE)
        if clean != data:
            self.replaced += sum(1 for a, b in zip(data, clean, strict=True) if a != b)
        return clean

    def close(self) -> None:
        self._f.close()


def _tail_closes_root(path: Path, sniff: int = 4096) -> bool:
    """True when the file tail carries `</df_world>` (intact export)."""
    with open(path, "rb") as fh:
        size = fh.seek(0, os.SEEK_END)
        fh.seek(max(0, size - sniff))
        return fh.read().rstrip().endswith(b"</df_world>")


class _TagStack:
    """Streaming open-element tracker over sanitized bytes (best-effort).

    DF output carries no comments/CDATA and no `>` inside attribute values,
    so a flat tag scan mirrors the element nesting; a scanner artifact could
    only shift the synthesized closing tags — it never touches intact-export
    numbers, because recovery runs only on files that failed the tail check.
    """

    _TAG = re.compile(
        rb"<(/?)([A-Za-z_:][\w.:-]*)((?:\"[^\"]*\"|'[^']*'|[^>\"'])*?)(/?)>"
    )

    def __init__(self) -> None:
        self._stack: list[bytes] = []
        self._carry = b""

    def feed(self, data: bytes) -> None:
        buf = self._carry + data
        pos = 0
        for m in self._TAG.finditer(buf):
            name = m.group(2)
            if m.group(1):  # </tag>
                if name in self._stack:
                    while self._stack[-1] != name:
                        self._stack.pop()
                    self._stack.pop()
            elif not m.group(4):  # <tag> — not self-closing
                self._stack.append(name)
            pos = m.end()
        rest = buf[pos:]
        rest = rest[rest.rfind(b">") + 1:]  # drop text; keep a partial tag
        lt = rest.find(b"<")
        self._carry = rest[lt:] if lt != -1 else b""

    def closing_bytes(self) -> bytes:
        """Closing tags for the still-open elements, innermost first."""
        return b"".join(b"</" + name + b">" for name in reversed(self._stack))

    def depth(self) -> int:
        return len(self._stack)

    def innermost(self) -> bytes:
        return self._stack[-1] if self._stack else b""


class RecoveringReader:
    """SanitizingReader wrapper that survives truncated DF exports (KI#34).

    The DF exporter can die mid-write (measured: a 2.9 GB export ends inside
    a battle collection, no `</df_world>`; the archive CRC was intact, so
    the cut happened at export time). A raw iterparse then aborts with
    ParseError at EOF. This wrapper tracks the open-element stack while
    streaming and synthesizes the missing closing tags at EOF so the parse
    completes; everything after the cut was never written, so the counted
    prefix stays honest — but every number from such a file is PARTIAL,
    and the stderr warnings say so.
    """

    def __init__(self, inner: SanitizingReader, name: str) -> None:
        self._inner = inner
        self._name = name
        self._tags = _TagStack()
        self._pending = b""
        self._recovered = False

    @property
    def replaced(self) -> int:
        return self._inner.replaced

    def read(self, size: int = -1) -> bytes:
        if self._pending:
            out = self._pending[:size] if size > 0 else self._pending
            self._pending = self._pending[len(out):]
            return out
        data = self._inner.read(size)
        if data:
            self._tags.feed(data)
            return data
        if self._recovered:
            return b""
        self._recovered = True
        closers = self._tags.closing_bytes()
        if closers:
            print(
                f"WARNING: {self._name}: export cut inside"
                f" <{self._tags.innermost().decode()}> — synthesized"
                f" {self._tags.depth()} closing tag(s); everything after"
                " the cut is lost; counts are PARTIAL",
                file=sys.stderr,
            )
        if size > 0:
            out, self._pending = closers[:size], closers[size:]
            return out
        return closers

    def close(self) -> None:
        self._inner.close()


def _make_reader(path: Path) -> SanitizingReader | RecoveringReader:
    """SanitizingReader; wrapped for truncation recovery when the tail check fails."""
    reader = SanitizingReader(path)
    if _tail_closes_root(path):
        return reader
    print(
        f"WARNING: {path.name}: truncated export (no </df_world> at EOF)"
        " — best-effort recovery by synthesizing closing tags; ALL counts"
        " from this file are PARTIAL",
        file=sys.stderr,
    )
    return RecoveringReader(reader, path.name)


def _int_text(elem: ET.Element, tag: str) -> int:
    value = elem.findtext(tag)
    if value is None:
        return -1
    try:
        return int(value)
    except ValueError:
        return -1


def _percentiles(values: list[int], points: tuple[float, ...]) -> list[int]:
    """Percentile ranks of an ascending-sorted list (nearest-rank)."""
    if not values:
        return [-1] * len(points)
    out: list[int] = []
    n = len(values)
    for p in points:
        idx = min(n - 1, max(0, round(p / 100 * n) - 1))
        out.append(values[idx])
    return out


class WorldStats:
    """Accumulators for one world export (all maps are deterministic)."""

    def __init__(self) -> None:
        self.section_counts: collections.Counter[str] = collections.Counter()
        self.event_types: collections.Counter[str] = collections.Counter()
        self.year_counts: collections.Counter[int] = collections.Counter()
        # event_id -> type_code * 2 + context_flag (context = any *_hfid
        # role field or a `cause` child); one dict serves both the F8
        # ambiguity-by-type join and the orphan count.
        self.event_meta: dict[int, int] = {}
        self.event_refs: dict[int, int] = {}
        self.collection_types: collections.Counter[str] = collections.Counter()
        self.collection_parent_field = 0  # collections with parent_eventcol set
        self.collection_root_count = 0  # collections with parent_eventcol == -1
        self.eventcol_child_links = 0  # total <eventcol> child references
        self.eventcol_refs: dict[int, int] = {}  # subcollection id -> #parents
        self.events_per_collection: list[int] = []
        self.figure_mentions: collections.Counter[int] = collections.Counter()
        self.figure_info: dict[int, tuple[str, int, int]] = {}
        self.figure_dead = 0
        self.deaths_total = 0
        self.deaths_with_slayer = 0
        self.death_causes: collections.Counter[str] = collections.Counter()
        self.type_codes: dict[str, int] = {}
        # Coverage census (iter-8g `--audit`): per-section per-record-tag
        # counts + every unique child-tag set per record tag (bounded by
        # DF record uniformity — typically 1-3 variants). Empty when the
        # audit flag is off (the F7/F8 detail pass does not collect this).
        self.record_tags_per_section: dict[str, collections.Counter[str]] = {}
        self.unique_child_tag_sets: dict[str, set[frozenset[str]]] = {}

    def type_code(self, event_type: str) -> int:
        code = self.type_codes.get(event_type)
        if code is None:
            code = len(self.type_codes)
            self.type_codes[event_type] = code
        return code


def _process_event(elem: ET.Element, stats: WorldStats) -> None:
    event_id = _int_text(elem, "id")
    event_type = elem.findtext("type") or "?NONE?"
    stats.event_types[event_type] += 1
    year = _int_text(elem, "year")
    stats.year_counts[year] += 1
    context = False
    hfids: set[int] = set()
    for child in elem:
        tag = child.tag
        text = child.text or ""
        if tag.endswith("hfid"):
            try:
                value = int(text)
            except ValueError:
                continue
            if value != -1:
                context = True
                hfids.add(value)
        elif tag == "cause":
            context = True
            if event_type == "hf died":
                stats.death_causes[text] += 1
    if event_type == "hf died":
        stats.deaths_total += 1
        if _int_text(elem, "slayer_hfid") != -1:
            stats.deaths_with_slayer += 1
    stats.figure_mentions.update(hfids)
    stats.event_meta[event_id] = stats.type_code(event_type) * 2 + (1 if context else 0)


def _process_collection(elem: ET.Element, stats: WorldStats) -> None:
    col_type = elem.findtext("type") or "?NONE?"
    stats.collection_types[col_type] += 1
    if _int_text(elem, "parent_eventcol") != -1:
        stats.collection_parent_field += 1
    else:
        stats.collection_root_count += 1
    child_events = 0
    for child in elem:
        if child.tag == "event":
            try:
                event_id = int(child.text or "-1")
            except ValueError:
                continue
            if event_id != -1:
                stats.event_refs[event_id] = stats.event_refs.get(event_id, 0) + 1
                child_events += 1
        elif child.tag == "eventcol":
            try:
                col_id = int(child.text or "-1")
            except ValueError:
                continue
            if col_id != -1:
                stats.eventcol_refs[col_id] = stats.eventcol_refs.get(col_id, 0) + 1
                stats.eventcol_child_links += 1
    stats.events_per_collection.append(child_events)


def _process_figure(elem: ET.Element, stats: WorldStats) -> None:
    figure_id = _int_text(elem, "id")
    race = elem.findtext("race") or "?"
    birth = _int_text(elem, "birth_year")
    death = _int_text(elem, "death_year")
    stats.figure_info[figure_id] = (race, birth, death)
    if death != -1:
        stats.figure_dead += 1


def _stream(path: Path, stats: WorldStats, audit: bool = False) -> tuple[int, float]:
    """One streaming pass over a legends XML; returns (sanitized, seconds).

    Memory law: `elem.clear()` per record + `section.clear()` every 4096
    records — a naive non-clearing parse of the medium world OOMs a 4 GB
    machine (measured, iter-8e).

    When `audit` is set, also collect the coverage census (per-section
    per-record-tag counts + every unique child-tag set per record tag)
    — a small fixed overhead: the per-record frozenset of immediate
    child tags is bounded by record uniformity (typically 1-3 variants
    per record tag, even across 10^5+ records).
    """
    reader = _make_reader(path)
    started = time.perf_counter()
    depth = 0
    section: ET.Element | None = None
    records = 0
    try:
        for event, elem in ET.iterparse(reader, events=("start", "end")):
            if event == "start":
                depth += 1
                if depth == 2:
                    section = elem
                continue
            if depth == 3:
                if section is not None:
                    stats.section_counts[section.tag] += 1
                    if audit:
                        _census_record(section.tag, elem, stats)
                    tag = elem.tag
                    if tag == "historical_event":
                        _process_event(elem, stats)
                    elif tag == "historical_event_collection":
                        _process_collection(elem, stats)
                    elif tag == "historical_figure":
                        _process_figure(elem, stats)
                    records += 1
                elem.clear()
                if records % 4096 == 0 and section is not None:
                    section.clear()
            depth -= 1
    finally:
        reader.close()
    return reader.replaced, time.perf_counter() - started


def _census_record(section_tag: str, elem: ET.Element, stats: WorldStats) -> None:
    """Coverage census contribution from one depth-3 record.

    Records the immediate child tag set (a structural fingerprint) for
    the record's tag — not the field values, only the shape. DF records
    of the same type are uniform, so `unique_child_tag_sets[tag]` stays
    small (1-3 elements typically); growth past 3 is a drift signal.
    """
    record_tag = elem.tag
    counter = stats.record_tags_per_section.get(section_tag)
    if counter is None:
        counter = collections.Counter()
        stats.record_tags_per_section[section_tag] = counter
    counter[record_tag] += 1
    child_set = frozenset(child.tag for child in elem)
    variants = stats.unique_child_tag_sets.get(record_tag)
    if variants is None:
        variants = set()
        stats.unique_child_tag_sets[record_tag] = variants
    variants.add(child_set)


def _stream_structure(path: Path) -> tuple[collections.Counter[str], int, float]:
    """Light pass for a companion `*-legends_plus.xml`: section counts only."""
    counts: collections.Counter[str] = collections.Counter()
    reader = _make_reader(path)
    started = time.perf_counter()
    depth = 0
    section: ET.Element | None = None
    records = 0
    try:
        for event, elem in ET.iterparse(reader, events=("start", "end")):
            if event == "start":
                depth += 1
                if depth == 2:
                    section = elem
                continue
            if depth == 3:
                if section is not None:
                    counts[section.tag] += 1
                    records += 1
                elem.clear()
                if records % 4096 == 0 and section is not None:
                    section.clear()
            depth -= 1
    finally:
        reader.close()
    return counts, reader.replaced, time.perf_counter() - started


def _fmt_pct(part: int, whole: int) -> str:
    return f"{(100.0 * part / whole):5.2f}%" if whole else "  n/a "


def _render_audit_section(add, stats: WorldStats) -> None:
    """Coverage census (iter-8g `--audit`).

    Lists every record tag seen on depth=3, marks HANDLED (the F7/F8
    detail records) vs UNHANDLED (everything else — site, entity,
    artifact, written_content, region, landmass, mountain_peak, river,
    creature_raw, entity_population, dance/musical/poetic form, …), and
    prints every unique child-tag set per record tag so bg-1's SQLite
    sink can plan field extraction without re-parsing the export.
    """
    add("== 1b. Coverage audit (record tags on depth=3) ==")
    record_totals: collections.Counter[str] = collections.Counter()
    for per_tag in stats.record_tags_per_section.values():
        for record_tag, count in per_tag.items():
            record_totals[record_tag] += count
    handled_count = sum(c for t, c in record_totals.items() if t in HANDLED_RECORDS)
    unhandled_count = sum(c for t, c in record_totals.items() if t not in HANDLED_RECORDS)
    add(f"  records: {len(record_totals)} distinct tags"
        f" · {record_totals.total():,} total"
        f" · HANDLED {handled_count:,} ({_fmt_pct(handled_count, record_totals.total())})"
        f" · UNHANDLED {unhandled_count:,} ({_fmt_pct(unhandled_count, record_totals.total())})")
    add("  per-section record-tag census (section -> [tag:count, ...]):")
    for section_tag in sorted(stats.record_tags_per_section):
        per_tag = stats.record_tags_per_section[section_tag]
        parts = [f"{tag}:{c:,}" for tag, c in per_tag.most_common()]
        add(f"  {section_tag} -> {{{', '.join(parts)}}}")
    add("  unique child-tag sets per record tag (variants = schema stability signal; >3 = drift):")
    for record_tag in sorted(record_totals):
        variants = stats.unique_child_tag_sets.get(record_tag, set())
        marker = "HANDLED" if record_tag in HANDLED_RECORDS else "UNHANDLED"
        n_records = record_totals[record_tag]
        n_variants = len(variants)
        add(f"  [{marker}] {record_tag} ({n_records:,} records, {n_variants} variant(s))")
        for variant in sorted(variants, key=lambda s: sorted(s)):
            tags = ", ".join(sorted(variant)) or "(no children)"
            add(f"      {{ {tags} }}")


def build_report(
    path: Path,
    plus_path: Path | None,
    stats: WorldStats,
    sanitized: int,
    seconds: float,
    plus_counts: collections.Counter[str] | None,
    plus_sanitized: int,
    plus_seconds: float,
    audit_mode: bool = False,
) -> str:
    lines: list[str] = []
    add = lines.append
    total_events = sum(stats.event_types.values())
    total_collections = sum(stats.collection_types.values())
    total_figures = len(stats.figure_info)

    add(f"DF Legends XML survey — {path.name}")
    add(f"file size: {path.stat().st_size / 1e6:.1f} MB"
        + (f" (plus companion: {plus_path.name}, {plus_path.stat().st_size / 1e6:.1f} MB)"
           if plus_path else ""))
    add(f"sanitized invalid XML bytes: {sanitized}"
        + (f" (plus: {plus_sanitized})" if plus_path else ""))
    add("")

    add("== 1. Scale (section -> records) ==")
    for section, count in sorted(stats.section_counts.items()):
        add(f"  {count:>9,}  {section}")
    if plus_counts:
        add("  companion (*-legends_plus.xml) sections:")
        for section, count in sorted(plus_counts.items()):
            add(f"  {count:>9,}  {section}   [plus]")
    add("")

    if audit_mode and stats.record_tags_per_section:
        _render_audit_section(add, stats)
        add("")

    add(f"== 2. F7 — event type distribution ({len(stats.event_types)} types,"
        f" {total_events:,} events) ==")
    category_counts: collections.Counter[str] = collections.Counter()
    for event_type, count in stats.event_types.items():
        category_counts[TYPE_CATEGORY.get(event_type, _UNKNOWN)] += count
    for category in list(CATEGORIES) + ([_UNKNOWN] if category_counts.get(_UNKNOWN) else []):
        count = category_counts.get(category, 0)
        if count:
            add(f"  {_fmt_pct(count, total_events)}  {count:>9,}  {category}")
    add("  top 15 types:")
    for event_type, count in stats.event_types.most_common(15):
        category = TYPE_CATEGORY.get(event_type, _UNKNOWN)
        add(f"  {_fmt_pct(count, total_events)}  {count:>9,}  {event_type}  [{category}]")
    top5 = sum(c for _, c in stats.event_types.most_common(5))
    add(f"  top-5 type concentration: {_fmt_pct(top5, total_events)}")
    if category_counts.get(_UNKNOWN):
        add("  UNCLASSIFIED types (extend TYPE_CATEGORY):")
        for event_type in sorted(stats.event_types):
            if event_type not in TYPE_CATEGORY:
                add(f"    {stats.event_types[event_type]:>9,}  {event_type}")
    add("")

    years = sorted(y for y in stats.year_counts if y >= 0)
    if years:
        first, last = years[0], years[-1]
        span = last - first + 1
        mean_year = total_events / span
        last_decade = sum(stats.year_counts[y] for y in range(last - 9, last + 1))
        peak_year, peak_count = max(
            sorted(stats.year_counts.items()), key=lambda kv: kv[1]
        )
        add(f"== 3. F7/F6 — events per year (year {first}..{last}) ==")
        add(f"  mean/year {mean_year:,.0f} · peak year {peak_year} ({peak_count:,} events)"
            f" · last-10y mean {last_decade / 10:,.0f}")
        add("  histogram (year:count) every 25y: "
            + " ".join(f"{y}:{stats.year_counts[y]:,}"
                       for y in range(first, last + 1, max(1, span // 20))))
    add("")

    add(f"== 4. F7 — events per figure ({total_figures:,} figures,"
        f" {stats.figure_dead:,} dead at export) ==")
    mentioned = len(stats.figure_mentions)
    add(f"  figures referenced by >=1 event: {mentioned:,} ({_fmt_pct(mentioned, total_figures)})"
        f" · never-referenced: {total_figures - mentioned:,}")
    counts_sorted = sorted(stats.figure_mentions.values())
    if counts_sorted:
        p50, p90, p99, pmax = _percentiles(counts_sorted, (50, 90, 99, 100))
        total_mentions = sum(counts_sorted)
        top1pct_n = max(1, len(counts_sorted) // 100)
        top1pct_share = sum(counts_sorted[-top1pct_n:]) / total_mentions
        add(f"  mentions per referenced figure: p50 {p50} · p90 {p90} · p99 {p99}"
            f" · max {pmax} · mean {total_mentions / len(counts_sorted):.1f}")
        add(f"  top-1% concentration: {top1pct_share * 100:.1f}% of all mentions"
            f" ({total_mentions:,})")
        add("  top 10 most-mentioned figures (id · race · b..d years · mentions):")
        for figure_id, mentions in stats.figure_mentions.most_common(10):
            race, birth, death = stats.figure_info.get(figure_id, ("?", -1, -1))
            add(f"    {figure_id:>7} · {race:<12} · {birth}..{death} · {mentions:,}")
    add("")

    add("== 5. F8 — causality reachability via event_collections ==")
    referenced = len(stats.event_refs)
    multi = sum(1 for n in stats.event_refs.values() if n >= 2)
    three = sum(1 for n in stats.event_refs.values() if n >= 3)
    add(f"  events referenced by >=1 collection:"
        f" {referenced:,} ({_fmt_pct(referenced, total_events)})")
    add(f"  events referenced by >=2 collections (ambiguous parentage,"
        f" bg-2 candidate_causes rate): {multi:,} ({_fmt_pct(multi, total_events)})")
    add(f"  events referenced by >=3 collections: {three:,} ({_fmt_pct(three, total_events)})")
    orphans = 0
    for _event_id, meta in stats.event_meta.items():
        if _event_id not in stats.event_refs and meta % 2 == 0:
            orphans += 1
    add(f"  orphan events (no collection ref, no *_hfid role, no cause):"
        f" {orphans:,} ({_fmt_pct(orphans, total_events)})")
    add(f"  hf died: {stats.deaths_total:,} · slayer recorded:"
        f" {stats.deaths_with_slayer:,} ({_fmt_pct(stats.deaths_with_slayer, stats.deaths_total)})")
    add("  hf died cause enum:")
    for cause, count in stats.death_causes.most_common():
        add(f"    {_fmt_pct(count, stats.deaths_total)}  {count:>9,}  {cause}")
    if multi:
        add("  ambiguity (>=2 direct refs) by event type, top 10:")
        ambiguous_by_type: collections.Counter[str] = collections.Counter()
        type_by_code = {code: name for name, code in stats.type_codes.items()}
        for event_id, refs in stats.event_refs.items():
            if refs >= 2:
                meta = stats.event_meta.get(event_id)
                if meta is not None:
                    ambiguous_by_type[type_by_code[meta // 2]] += 1
        for event_type, count in ambiguous_by_type.most_common(10):
            add(f"    {count:>9,}  {event_type}")
    else:
        add("  direct event -> collection references are unique in this export"
            " (no event lists 2+ parent collections)")
    multi_parent = sum(1 for n in stats.eventcol_refs.values() if n >= 2)
    max_parents = max(stats.eventcol_refs.values(), default=0)
    add(f"  collections: {total_collections:,} · parent_eventcol set:"
        f" {stats.collection_parent_field:,} · roots {stats.collection_root_count:,}"
        f" · eventcol child links {stats.eventcol_child_links:,}")
    add(f"  subcollections referenced by >=2 parents (many-to-many where it"
        f" actually lives): {multi_parent:,} ({_fmt_pct(multi_parent, total_collections)})"
        f" · max parents {max_parents}")
    if stats.events_per_collection:
        epc = sorted(stats.events_per_collection)
        p50, p90, pmax = _percentiles(epc, (50, 90, 100))
        add(f"  direct events per collection: p50 {p50} · p90 {p90} · max {pmax}")
    add("")

    add("== 6. Full event type table ==")
    for event_type, count in sorted(
        stats.event_types.items(), key=lambda kv: (-kv[1], kv[0])
    ):
        category = TYPE_CATEGORY.get(event_type, _UNKNOWN)
        add(f"  {count:>9,}  {event_type}  [{category}]")
    add("")

    add("== environment (informational — not deterministic) ==")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    add(f"  parse wall time: {seconds:.1f}s"
        + (f" (+ {plus_seconds:.1f}s companion)" if plus_path else "")
        + f" · peak RSS: {rss:.0f} MB")
    return "\n".join(lines)


def find_worlds(args_paths: list[str]) -> list[tuple[Path, Path | None]]:
    """Resolve each CLI target to (legends.xml, legends_plus.xml|None)."""
    worlds: list[tuple[Path, Path | None]] = []
    for target in args_paths:
        p = Path(target)
        if p.is_dir():
            mains = sorted(p.glob("*-legends.xml"))
            if not mains:
                raise SystemExit(f"no *-legends.xml under {p}")
            for main in mains:
                plus = main.with_name(main.name.replace("-legends.xml", "-legends_plus.xml"))
                worlds.append((main, plus if plus.exists() else None))
        elif p.is_file():
            plus = p.with_name(p.name.replace("-legends.xml", "-legends_plus.xml"))
            worlds.append((p, plus if plus.exists() else None))
        else:
            raise SystemExit(f"not found: {p}")
    return worlds


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "targets", nargs="+",
        help="legends.xml file(s) or world directory(ies) containing them",
    )
    parser.add_argument(
        "--out", type=Path, default=DEFAULT_OUT,
        help=f"report directory (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--audit", action="store_true",
        help="coverage census: per-section per-record-tag counts + every "
             "unique child-tag set per record tag (iter-8g). Replaces "
             "head/middle/tail positional sampling — strictly more info, "
             "bounded by record uniformity. Use before a bg-1 SQLite sink "
             "to plan field extraction without re-parsing.",
    )
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)

    for main_path, plus_path in find_worlds(args.targets):
        print(f"surveying {main_path} ...", file=sys.stderr)
        stats = WorldStats()
        sanitized, seconds = _stream(main_path, stats, audit=args.audit)
        plus_counts: collections.Counter[str] | None = None
        plus_sanitized = 0
        plus_seconds = 0.0
        if plus_path is not None:
            print(f"  companion {plus_path.name} ...", file=sys.stderr)
            plus_counts, plus_sanitized, plus_seconds = _stream_structure(plus_path)
        report = build_report(
            main_path, plus_path, stats, sanitized, seconds,
            plus_counts, plus_sanitized, plus_seconds,
            audit_mode=args.audit,
        )
        stem = main_path.name.removesuffix("-legends.xml")
        out_path = args.out / f"df_survey_{stem}.txt"
        out_path.write_text(report + "\n", encoding="utf-8")

        total_events = sum(stats.event_types.values())
        referenced = len(stats.event_refs)
        multi = sum(1 for n in stats.event_refs.values() if n >= 2)
        micro = sum(
            c for t, c in stats.event_types.items()
            if TYPE_CATEGORY.get(t) == CATEGORY_MICRO
        )
        print(f"  {total_events:,} events · {len(stats.event_types)} types ·"
              f" {sum(stats.collection_types.values()):,} collections ·"
              f" {len(stats.figure_info):,} figures")
        if args.audit:
            record_total = sum(
                c for per_tag in stats.record_tags_per_section.values()
                for c in per_tag.values()
            )
            handled = sum(
                c for per_tag in stats.record_tags_per_section.values()
                for t, c in per_tag.items() if t in HANDLED_RECORDS
            )
            unhandled_tags = {
                t for per_tag in stats.record_tags_per_section.values()
                for t in per_tag if t not in HANDLED_RECORDS
            }
            print(f"  coverage: {len(unhandled_tags)} UNHANDLED record tags"
                  f" · HANDLED {handled:,} / {record_total:,}"
                  f" ({_fmt_pct(handled, record_total)})")
        else:
            print(f"  micro (street/personal) share: {_fmt_pct(micro, total_events)}"
                  f" · collection-referenced: {_fmt_pct(referenced, total_events)}"
                  f" · ambiguous (2+ refs): {_fmt_pct(multi, total_events)}")
        print(f"  report: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
