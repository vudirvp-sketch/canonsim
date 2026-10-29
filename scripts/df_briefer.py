"""DF briefer spike (bg-3 — `docs/TASKS.md` Track B, bg-3-briefer-spike).

The mini-briefer + reverse-validation harness over the SQLite sink
(`scripts/df_import.py`, D-051/D-063). It ports the repo's LLM-boundary
pattern (D-055: the repo side is LLM-free; the operator is the external
narrator over files under `output/`, gitignored) to foreign canon:

    "tell battle X from figure Y's POV, knowing only Y's own records"

- **The POV brief** (`call`): dry structured tokens assembled from the
  sink — the assignment frame (battle X's curator facts: name, span,
  place, scale — explicitly labeled NOT the subject's knowledge), the
  subject card, the subject's in-window records (the `event_participant`
  prefix scan — Y's own records; plus-companion fields merged, main
  precedence), and the nearest records outside the window (context,
  bounded). A pure function of (DB, figure, collection, params): no RNG,
  no wall-clock in the document. Boundedness is BRIEF_SPEC's law: a
  ranking cap with a loud `[truncated: ...]` marker, never a silent drop.
- **The epistemic model** (the honest reading of "Y's own records"):
  Y's closure = its participant-index events; figures = Y plus the
  hfid-shaped co-participants of those events; sites = the sites those
  events reference. DF has no epistemology events (TAXONOMY §4.1) — the
  participant index IS this spike's knowledge model. Known measured blind
  spot (TAXONOMY §4.2): reputation events key figures as hfid1/hfid2 and
  lift zero participant rows — reputation context is invisible to the
  closure, by law, not by accident.
- **Reverse validation** (`apply`): the reply document
  `{anchor, prose, claims}` is gated loudly (malformed → `BrieferError`,
  nothing validated, never a repair); each structured claim gets exactly
  one closed-vocabulary verdict:

      supported      — checks out against the subject's records
      contradicted   — within the subject's reach, the stated value
                       differs (evidence: the actual value)
      beyond_records — exists in the sink, OUTSIDE the closure (the POV
                       privacy violation this spike counts as invented)
      unknown_event / unknown_figure / unknown_site — not in the sink

  The invented-facts count = every non-supported claim. Prose is NEVER
  parsed (the structural neutralization law: facts ride structured
  claims only). Figure-name claims match ANY recorded name variant
  (the EAV can hold more than one; race/caste/birth/death are typed).
- **The regen ladder** (VALIDATION_SPEC §7 ported, ≤2): a refused reply
  emits the regen call — same brief, refusal notes riding the protocol
  section (D-049's note geometry); budget exhaustion renders the DRY
  floor: the subject's own in-window records as template lines (the L12
  ladder's floor analog). `regen_count` is a first-class metric, never
  absorbed silently.
- **The retrieval stress test** (`stress`): a deterministic figure spread
  (quantiles over the mention-count distribution) — per figure: prefix-
  scan latency, brief-assembly latency, brief size, truncation flag; plus
  a double-build byte-compare (the content-determinism probe, the
  profile_harness law). Counts and sizes are facts; timings are
  environment-specific (perf-1's labeling law).

Usage:
    python scripts/df_briefer.py <db> cases [--count N] [--min-events N]
    python scripts/df_briefer.py <db> call --figure N [--collection M]
                                         [--max-records K] [--context K]
    python scripts/df_briefer.py <db> apply --call <path> --reply <path>
    python scripts/df_briefer.py <db> stress [--picks N] [--max-records K]

Call/reply/dry files live under `output/df_briefer/` (gitignored runtime
artifacts; the call counter derives from the files on disk — the session
state IS the file set).
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import df_taxonomy  # _Atlas (name resolution) + _ref + _spread — the bg-2 recipe, reused

REPO = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO / "output" / "df_briefer"

MAX_REGENS = 2  # VALIDATION_SPEC §7's ceiling, ported verbatim
CLAIM_FIGURE_PROPS = frozenset({"name", "race", "caste", "birth_year", "death_year"})
SUPPORTED = "supported"
NON_SUPPORTED = frozenset({
    "contradicted", "beyond_records",
    "unknown_event", "unknown_figure", "unknown_site",
})

# Salient event fields render before the alphabetical tail (readability
# only — determinism holds either way: salience list, then sorted rest).
_SALIENT = (
    "cause", "state", "mood", "outcome", "successful", "old_race", "new_race",
    "theft_method", "item_type", "mat", "method", "action", "victim", "eater",
    "race", "crime", "prison_months", "return",
)
_MAX_EVENT_FIELDS = 14
_MAX_VALUE_CHARS = 60
_HFID_KEYS = frozenset({"histfig", "hist_figure_id"})
_SITE_KEYS = frozenset({"site", "moved_to_site_id", "feature_layer_id"})
_PLACE_KEYS = frozenset({
    "site_id", "site", "moved_to_site_id", "subregion_id", "feature_layer_id",
})


class BrieferError(Exception):
    """A malformed reply document — loud, never a repair (the shape gate)."""


# ---------------------------------------------------------------------------
# The epistemic closure (the subject's measured reach)


@dataclass(frozen=True)
class Closure:
    """Y's own records, as the sink's participant index sees them."""

    hfid: int
    records: tuple[tuple[int, int], ...]      # (event_id, year), ordered
    events: frozenset[int]
    figures: frozenset[int]                   # Y + hfid-shaped co-participants
    sites: frozenset[int]                     # sites referenced by Y's records

    @property
    def total_records(self) -> int:
        return len(self.records)


def _records_query(conn: sqlite3.Connection, hfid: int) -> list[tuple[int, int]]:
    """The participant-index prefix scan (bg-2's 4 ms measured path)."""
    return conn.execute(
        "SELECT e.id, e.year FROM events e JOIN event_participant p"
        " ON p.event_id = e.id WHERE p.hfid = ? ORDER BY e.year, e.id",
        (hfid,),
    ).fetchall()


def _ref_values(
    conn: sqlite3.Connection, table: str, event_ids: list[int],
    keys: tuple[str, ...],
) -> set[int]:
    """Distinct integer refs under the given field keys over Y's events
    (both EAVs use event_id as the leading PK column — prefix scans)."""
    out: set[int] = set()
    marks = ",".join("?" * len(event_ids)) if event_ids else ""
    if not marks:
        return out
    key_marks = ",".join("?" * len(keys))
    for (value,) in conn.execute(
        f"SELECT DISTINCT f.value FROM {table} f WHERE f.event_id IN ({marks})"  # noqa: S608
        f" AND f.key IN ({key_marks})",
        (*event_ids, *keys),
    ):
        ref = df_taxonomy._ref(value)
        if ref is not None:
            out.add(ref)
    return out


def subject_closure(conn: sqlite3.Connection, hfid: int) -> Closure:
    """Y's closure: events from the participant index; figures from every
    hfid-shaped key (the sink's lift rule, hfid1/hfid2 excluded by law);
    sites from the site-bearing keys."""
    records = _records_query(conn, hfid)
    event_ids = [event_id for event_id, _ in records]
    figures: set[int] = {hfid}
    sites: set[int] = set()
    for table in ("event_fields", "event_plus_fields"):
        figures |= _ref_values(
            conn, table, event_ids,
            tuple(k for k in _field_keys(conn, table) if _is_hfid_key(k)),
        )
        sites |= _ref_values(
            conn, table, event_ids, ("site_id", "site", "moved_to_site_id"),
        )
    return Closure(
        hfid=hfid,
        records=tuple(records),
        events=frozenset(event_ids),
        figures=frozenset(figures),
        sites=frozenset(sites),
    )


def _field_keys(conn: sqlite3.Connection, table: str) -> list[str]:
    return [
        row[0] for row in conn.execute(
            f"SELECT DISTINCT key FROM {table}"  # noqa: S608
        )
    ]


def _is_hfid_key(key: str) -> bool:
    return key.endswith("hfid") or key in _HFID_KEYS


# ---------------------------------------------------------------------------
# The POV brief


@dataclass
class Brief:
    """The assembled brief plus the pieces the dry floor re-renders."""

    hfid: int
    col_id: int | None
    text: str
    anchor: int
    record_lines: list[str] = field(default_factory=list)
    window: tuple[int, int] | None = None
    in_window: int = 0
    truncated: int = 0


def _clip(value: str) -> str:
    return value if len(value) <= _MAX_VALUE_CHARS else value[:_MAX_VALUE_CHARS] + "..."


def _display_key(key: str) -> str:
    for suffix in ("_hfid", "_enid", "_entity_id", "_id"):
        if key.endswith(suffix) and len(key) > len(suffix):
            return key[: -len(suffix)]
    return key


def _render_value(atlas: df_taxonomy._Atlas, key: str, value: str) -> str:
    """Resolve a field value: ids to names, DF presence flags to 'yes'."""
    if value == "":
        return "yes"  # the DF empty-element presence flag (bg-2's law)
    ref = df_taxonomy._ref(value)
    if ref is None:
        return _clip(value)
    if _is_hfid_key(key):
        return atlas.figure(ref)
    if key in _SITE_KEYS or key == "site_id" or key.endswith("_site"):
        return atlas.site(ref)
    if key.endswith("enid") or key.endswith("_entity_id") or key == "civ_id":
        return atlas.entity(ref)
    if key == "artifact_id":
        return atlas.artifact(ref)
    if key in ("subregion_id", "region_id"):
        return atlas.region(ref)
    return _clip(value)


def _event_place(
    atlas: df_taxonomy._Atlas, main: dict[str, str], plus: dict[str, str],
) -> str:
    for key in ("site_id", "site", "moved_to_site_id"):
        ref = df_taxonomy._ref((main.get(key) or plus.get(key)))
        if ref is not None:
            return atlas.site(ref)
    ref = df_taxonomy._ref(main.get("subregion_id"))
    if ref is not None:
        return atlas.region(ref)
    ref = df_taxonomy._ref(main.get("feature_layer_id"))
    if ref is not None:
        return f"feature layer {ref}"
    return "no place recorded"


def _event_fields(
    conn: sqlite3.Connection, event_id: int,
) -> tuple[dict[str, str], dict[str, str]]:
    """Single-value view of both EAVs (main + plus), main precedence."""
    main = df_taxonomy._event_fields(conn, "event_fields", event_id)
    plus = (
        df_taxonomy._event_fields(conn, "event_plus_fields", event_id)
        if df_taxonomy._has_plus(conn)
        else {}
    )
    plus = {k: v for k, v in plus.items() if k not in main}
    return main, plus


def render_event_line(
    conn: sqlite3.Connection, atlas: df_taxonomy._Atlas, event_id: int,
) -> str:
    """One dry record line: `- [y122] 'hf died' ev 34117 · cause: struck;
    victim: ...; slayer: ... · at tradedblocked [s1121]`."""
    row = conn.execute(
        "SELECT type, year FROM events WHERE id = ?", (event_id,)
    ).fetchone()
    if row is None:
        return f"- ev {event_id} (not in the events table)"
    event_type, year = row
    main, plus = _event_fields(conn, event_id)
    merged: dict[str, str] = {**plus, **main}
    place = _event_place(atlas, main, plus)
    ordered = [k for k in _SALIENT if k in merged]
    ordered += sorted(k for k in merged if k not in _SALIENT)
    # Collision-aware display keys: main 'woundee_hfid' and plus 'woundee'
    # both strip to 'woundee' — on collision both render their raw key
    # (dry tokens stay unambiguous; redundancy is the export's own).
    base = {k: _display_key(k) for k in ordered if k not in _PLACE_KEYS}
    counts = Counter(base.values())
    parts: list[str] = []
    for key in ordered[:_MAX_EVENT_FIELDS]:
        if key in _PLACE_KEYS:
            continue  # the trailing place carries these
        shown_key = base[key] if counts[base[key]] == 1 else key
        parts.append(f"{shown_key}: {_render_value(atlas, key, merged[key])}")
    if len(ordered) > _MAX_EVENT_FIELDS:
        parts.append(f"(+{len(ordered) - _MAX_EVENT_FIELDS} more fields)")
    body = "; ".join(parts) if parts else "no detail fields"
    return f"- [y{year}] '{event_type}' ev {event_id} · {body} · at {place}"


def _figure_card(
    conn: sqlite3.Connection, atlas: df_taxonomy._Atlas, hfid: int,
) -> list[str]:
    row = conn.execute(
        "SELECT race, birth_year, death_year FROM figures WHERE id = ?", (hfid,)
    ).fetchone()
    if row is None:
        return [f"- hf {hfid} (no figure record)"]
    race, birth, death = row
    span = f"born y{birth}" + (
        f" · died y{death}" if death != -1 else " · alive at export"
    )
    return [f"- {atlas.figure(hfid)} · {span}"]


def _collection_topic(
    conn: sqlite3.Connection, atlas: df_taxonomy._Atlas, col_id: int,
) -> tuple[list[str], tuple[int, int]]:
    """The assignment frame — curator facts, explicitly NOT the subject's
    knowledge (the assignment tells WHAT to tell, not the facts)."""
    row = conn.execute(
        "SELECT type, start_year, end_year FROM collections WHERE id = ?",
        (col_id,),
    ).fetchone()
    if row is None:
        return [f"- col {col_id} (no collection record)"], (0, 0)
    col_type, start, end = row
    fields: dict[str, list[str]] = {}
    for key, value in conn.execute(
        "SELECT key, value FROM collection_fields WHERE collection_id = ?",
        (col_id,),
    ):
        fields.setdefault(key, []).append(value)
    span = (
        f"y{start}-ongoing" if end == -1
        else f"y{start}-{end}" if end != start else f"y{start}"
    )
    members = conn.execute(
        "SELECT COUNT(*) FROM event_membership WHERE collection_id = ?",
        (col_id,),
    ).fetchone()[0]
    nested = conn.execute(
        "SELECT COUNT(*) FROM collection_parent WHERE parent_id = ?",
        (col_id,),
    ).fetchone()[0]
    name = (fields.get("name") or ["?"])[0]
    site = df_taxonomy._ref((fields.get("site_id") or [""])[0])
    lines = [
        f"- tell {col_type} '{name}' (col {col_id}, {span}) from the subject's"
        " point of view",
        f"- curator facts (NOT the subject's knowledge): place"
        f" {atlas.site(site) if site is not None else 'none recorded'}"
        f" · {members} direct member events · {nested} nested collections",
    ]
    outcome = (fields.get("outcome") or [None])[0]
    if outcome:
        lines.append(f"- recorded outcome: {outcome}")
    for side in ("attacking", "defending"):
        leaders = fields.get(f"{side}_hfid") or []
        if leaders:
            refs = sorted({df_taxonomy._ref(v) for v in leaders} - {None})
            shown = ", ".join(atlas.figure(r) for r in refs[:3])
            more = f" (+{len(refs) - 3} more)" if len(refs) > 3 else ""
            lines.append(f"- {side} side: {len(refs)} named figures: {shown}{more}")
    parent = df_taxonomy._ref((fields.get("war_eventcol") or [""])[0])
    if parent is not None:
        lines.append(f"- parent war: col {parent}")
    return lines, (start, end if end != -1 else start)


def _context_records(
    records: list[tuple[int, int]], window: tuple[int, int], limit: int,
) -> list[int]:
    """The nearest records OUTSIDE the window, half before, half after."""
    before = [e for e, y in records if y < window[0]][-(limit // 2):]
    after = [e for e, y in records if y > window[1]][: limit - len(before)]
    return before + after


def build_pov_brief(
    conn: sqlite3.Connection,
    atlas: df_taxonomy._Atlas,
    hfid: int,
    col_id: int | None = None,
    *,
    max_records: int = 60,
    context: int = 8,
    notes: tuple[str, ...] = (),
    regens: int = 0,
) -> Brief:
    """Assemble the POV brief — a pure function of (DB, ids, params)."""
    closure = subject_closure(conn, hfid)
    if not closure.records:
        raise BrieferError(
            f"figure {hfid} has zero participant-index records — nothing to tell"
        )
    out: list[str] = [f"# POV brief — {atlas.figure(hfid)}"]
    out.append("")
    out.append("## assignment")
    if col_id is not None:
        topic, window = _collection_topic(conn, atlas, col_id)
        out.extend(topic)
    else:
        years = [y for _, y in closure.records]
        window = (min(years), max(years))
        out.append("- tell the subject's full recorded timeline (no topic"
                   " collection given)")
    out.append(f"- window: y{window[0]}-y{window[1]}")
    out.append("")
    out.append("## subject_card")
    out.extend(_figure_card(conn, atlas, hfid))
    out.append(f"- total records: {closure.total_records} (participant index;"
               " hfid1/hfid2-keyed events are invisible to it)")
    out.append("")
    out.append("## pov_records")
    in_window = [e for e, y in closure.records if window[0] <= y <= window[1]]
    grouped = {
        e for e in in_window
        if conn.execute(
            "SELECT 1 FROM event_membership WHERE event_id = ? AND"
            " collection_id = ? LIMIT 1", (e, col_id or -1),
        ).fetchone()
    } if col_id is not None else set()
    shown = in_window[:max_records]
    record_lines = [
        render_event_line(conn, atlas, e) for e in shown
    ]
    out.extend(record_lines)
    out.append(
        f"- (the subject's in-window records: {len(in_window)}"
        + (
            f", of which the curator grouped {len(grouped)} into the topic"
            if col_id is not None
            else ""
        )
        + ")"
    )
    truncated = len(in_window) - len(shown)
    if truncated > 0:
        out.append(f"- [truncated: {len(shown)} of {len(in_window)} shown"
                   " — beyond-cap items render nothing, never a silent drop]")
    out.append("")
    out.append("## context_records")
    if col_id is None:
        out.append("- (none — the window spans the whole recorded timeline)")
    else:
        ctx = _context_records(list(closure.records), window, context)
        if ctx:
            out.extend(render_event_line(conn, atlas, e) for e in ctx)
        else:
            out.append("- (none — the window spans the subject's recorded life)")
    out.append("")
    out.append("## briefer_protocol")
    out.append(f"figure: {hfid}")
    out.append(f"collection: {col_id if col_id is not None else 'none'}")
    out.append(f"anchor: {closure.total_records}")
    out.append(f"regen: {regens}/{MAX_REGENS}")
    for note in notes:
        out.append(f"- {note}")
    out.append("")
    out.append("## reply_contract")
    out.append(_REPLY_CONTRACT)
    return Brief(
        hfid=hfid, col_id=col_id, text="\n".join(out) + "\n",
        anchor=closure.total_records, record_lines=record_lines,
        window=window, in_window=len(in_window), truncated=truncated,
    )


_REPLY_CONTRACT = """Reply with ONE JSON document (write it as reply_<NNNN>.json
next to this call, then `apply --call ... --reply ...`):
{"anchor": <int, copy from briefer_protocol>,
 "prose": "<the narrative — free text, NEVER parsed or validated>",
 "claims": [<claim>, ...]}
Each claim is exactly one of:
 {"event": <int ev id>, "type"?: "<the event's type>"}
 {"figure": <int hf id>, "prop": "name|race|caste|birth_year|death_year", "value": "<str>"}
 {"site": <int site id>, "value": "<the site's name>"}
Verdicts: supported | contradicted | beyond_records | unknown_event |
unknown_figure | unknown_site. Any non-supported claim refuses the whole
reply (regen <= 2, refusal notes ride the next call; exhaustion renders
the dry floor — the subject's own records as template lines)."""


# ---------------------------------------------------------------------------
# Reverse validation


@dataclass(frozen=True)
class Verdict:
    index: int
    claim: str
    verdict: str
    evidence: str


def _figure_prop(
    conn: sqlite3.Connection, hfid: int, prop: str,
) -> str | tuple[str, ...]:
    if prop == "name":
        values = [
            row[0] for row in conn.execute(
                "SELECT value FROM figure_fields WHERE figure_id = ? AND key = 'name'"
                " ORDER BY value", (hfid,),
            )
        ]
        return tuple(values) if values else ""
    row = conn.execute(
        f"SELECT {prop} FROM figures WHERE id = ?", (hfid,)  # noqa: S608
    ).fetchone()
    if row is None:
        return ""
    return str(row[0])


def validate_reply(
    conn: sqlite3.Connection,
    atlas: df_taxonomy._Atlas,
    closure: Closure,
    reply: Any,
    anchor: int,
) -> list[Verdict]:
    """The shape gate (loud) + one closed-vocabulary verdict per claim."""
    if not isinstance(reply, dict):
        raise BrieferError("the reply must be a JSON object")
    reply_anchor = reply.get("anchor")
    if not isinstance(reply_anchor, int) or isinstance(reply_anchor, bool):
        raise BrieferError("'anchor' must be an integer")
    if reply_anchor != anchor:
        raise BrieferError(
            f"anchor mismatch: reply {reply_anchor} != call {anchor}"
            " (the world is frozen — a mismatch is an operator error)"
        )
    prose = reply.get("prose")
    if not isinstance(prose, str) or not prose.strip():
        raise BrieferError("'prose' must be a non-empty string")
    claims = reply.get("claims")
    if not isinstance(claims, list):
        raise BrieferError("'claims' must be a list")

    verdicts: list[Verdict] = []
    for index, claim in enumerate(claims):
        verdicts.append(_verdict_of(conn, atlas, closure, index, claim))
    return verdicts


def _verdict_of(
    conn: sqlite3.Connection,
    atlas: df_taxonomy._Atlas,
    closure: Closure,
    index: int,
    claim: Any,
) -> Verdict:
    if not isinstance(claim, dict):
        raise BrieferError(f"claim {index} must be an object")
    keys = set(claim)
    if "event" in keys:
        if keys - {"event", "type", "says"}:
            raise BrieferError(f"claim {index}: unknown keys {sorted(keys)}")
        event_id = claim["event"]
        if not isinstance(event_id, int) or isinstance(event_id, bool):
            raise BrieferError(f"claim {index}: 'event' must be an integer")
        desc = f"event {event_id}" + (
            f" ({claim['type']})" if "type" in claim else ""
        )
        row = conn.execute(
            "SELECT type, year FROM events WHERE id = ?", (event_id,)
        ).fetchone()
        if event_id in closure.events:
            if row is None:  # defensive: index says member, table disagrees
                raise BrieferError(
                    f"claim {index}: event {event_id} in the index, not in events"
                )
            if "type" in claim and claim["type"] != row[0]:
                return Verdict(index, desc, "contradicted",
                               f"actual type '{row[0]}' (y{row[1]})")
            return Verdict(index, desc, SUPPORTED,
                           f"[y{row[1]}] '{row[0]}' ev {event_id}")
        if row is not None:
            return Verdict(
                index, desc, "beyond_records",
                f"'{row[0]}' y{row[1]} exists in the log, but the subject has"
                " no record of it",
            )
        return Verdict(index, desc, "unknown_event",
                       "no such event id in the sink")
    if "figure" in keys:
        if keys - {"figure", "prop", "value", "says"}:
            raise BrieferError(f"claim {index}: unknown keys {sorted(keys)}")
        hfid, prop, value = claim.get("figure"), claim.get("prop"), claim.get("value")
        if not isinstance(hfid, int) or isinstance(hfid, bool):
            raise BrieferError(f"claim {index}: 'figure' must be an integer")
        if prop not in CLAIM_FIGURE_PROPS:
            raise BrieferError(
                f"claim {index}: 'prop' must be one of"
                f" {sorted(CLAIM_FIGURE_PROPS)}"
            )
        if not isinstance(value, str):
            raise BrieferError(f"claim {index}: 'value' must be a string")
        desc = f"figure {hfid} {prop} = {value!r}"
        actual = _figure_prop(conn, hfid, prop)
        known = hfid == closure.hfid or hfid in closure.figures
        exists = conn.execute(
            "SELECT 1 FROM figures WHERE id = ?", (hfid,)
        ).fetchone() is not None
        if known:
            if isinstance(actual, tuple):
                ok = value in actual
                evidence = f"recorded names: {', '.join(actual) or 'none'}"
            else:
                ok = value == actual
                evidence = f"actual {prop}: {actual}"
            return Verdict(
                index, desc, SUPPORTED if ok else "contradicted", evidence
            )
        if exists:
            return Verdict(
                index, desc, "beyond_records",
                f"{atlas.figure(hfid)} exists in the sink, outside the"
                " subject's closure",
            )
        return Verdict(index, desc, "unknown_figure", "no such figure id")
    if "site" in keys:
        if keys - {"site", "value", "says"}:
            raise BrieferError(f"claim {index}: unknown keys {sorted(keys)}")
        site_id, value = claim.get("site"), claim.get("value")
        if not isinstance(site_id, int) or isinstance(site_id, bool):
            raise BrieferError(f"claim {index}: 'site' must be an integer")
        if not isinstance(value, str):
            raise BrieferError(f"claim {index}: 'value' must be a string")
        desc = f"site {site_id} = {value!r}"
        name = _site_name(conn, site_id)
        if site_id in closure.sites:
            return Verdict(
                index, desc,
                SUPPORTED if value == name else "contradicted",
                f"actual name: {name}",
            )
        if name is not None:
            return Verdict(
                index, desc, "beyond_records",
                f"site '{name}' exists in the sink, outside the closure",
            )
        return Verdict(index, desc, "unknown_site", "no such site id")
    raise BrieferError(
        f"claim {index}: must carry exactly one of event|figure|site"
    )


def _site_name(conn: sqlite3.Connection, site_id: int) -> str | None:
    row = conn.execute(
        "SELECT data FROM records WHERE record_tag = 'site' AND id = ?",
        (site_id,),
    ).fetchone()
    if row is None:
        return None
    try:
        payload = json.loads(row[0])
    except ValueError:
        return None
    raw = payload.get("name") or [""]
    return str(raw[0]) if isinstance(raw, list) and raw else None


def render_dry(brief: Brief) -> str:
    """The dry floor — the beat renders its own record lines (L12 analog)."""
    out = [
        "# dry floor — regen budget exhausted",
        f"# subject: hf {brief.hfid}"
        + (f" · topic: col {brief.col_id}" if brief.col_id is not None else ""),
        "",
    ]
    out.extend(brief.record_lines)
    if brief.truncated > 0:
        out.append(
            f"# ({brief.in_window} in-window records; {brief.truncated}"
            " beyond the cap — not rendered)"
        )
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# The session files (call / reply / dry) — the D-055 pattern over files


@dataclass(frozen=True)
class CallState:
    hfid: int
    col_id: int | None
    anchor: int
    regens: int
    notes: tuple[str, ...]


def parse_call(text: str) -> CallState:
    """Machine-read the briefer_protocol section of a call file."""
    if "## briefer_protocol" not in text:
        raise BrieferError("no briefer_protocol section in the call file")
    section = text.split("## briefer_protocol", 1)[1].split("\n## ", 1)[0]
    state: dict[str, str] = {}
    notes: list[str] = []
    for line in section.splitlines():
        for key in ("figure", "collection", "anchor", "regen"):
            marker = f"{key}: "
            if line.startswith(marker):
                state[key] = line[len(marker):].strip()
        if line.startswith("- "):
            notes.append(line[2:])
    if "figure" not in state or "anchor" not in state or "regen" not in state:
        raise BrieferError(f"malformed briefer_protocol: {state}")
    regens = int(state["regen"].split("/")[0])
    return CallState(
        hfid=int(state["figure"]),
        col_id=None if state.get("collection") == "none"
        else int(state["collection"]),
        anchor=int(state["anchor"]),
        regens=regens,
        notes=tuple(notes),
    )


def next_seq(out_dir: Path) -> int:
    """The session state IS the file set: the next free call number."""
    out_dir.mkdir(parents=True, exist_ok=True)
    highest = -1
    for path in out_dir.glob("call_*.md"):
        digits = path.stem.removeprefix("call_")
        if digits.isdigit():
            highest = max(highest, int(digits))
    return highest + 1


def emit_call(
    conn: sqlite3.Connection, atlas: df_taxonomy._Atlas, out_dir: Path,
    hfid: int, col_id: int | None, *,
    max_records: int, context: int,
    notes: tuple[str, ...] = (), regens: int = 0,
) -> tuple[Path, Brief]:
    seq = next_seq(out_dir)
    brief = build_pov_brief(
        conn, atlas, hfid, col_id, max_records=max_records, context=context,
        notes=notes, regens=regens,
    )
    path = out_dir / f"call_{seq:04d}.md"
    path.write_text(brief.text, encoding="utf-8")
    return path, brief


def apply_reply(
    conn: sqlite3.Connection, atlas: df_taxonomy._Atlas,
    call_path: Path, reply_path: Path, out_dir: Path, *,
    max_records: int, context: int,
) -> int:
    """Validate a reply against its call; drive the regen ladder."""
    state = parse_call(call_path.read_text(encoding="utf-8"))
    try:
        reply = json.loads(reply_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise BrieferError(f"reply is not valid JSON: {exc}") from exc
    closure = subject_closure(conn, state.hfid)
    verdicts = validate_reply(conn, atlas, closure, reply, state.anchor)
    accepted = all(v.verdict == SUPPORTED for v in verdicts)
    invented = sum(1 for v in verdicts if v.verdict in NON_SUPPORTED)

    print(f"call {call_path.name} · reply {reply_path.name}")
    print(f"claims: {len(verdicts)} · invented (non-supported): {invented}")
    for v in verdicts:
        print(f"  [{v.verdict}] claim {v.index} ({v.claim}) — {v.evidence}")

    if accepted:
        prose = reply["prose"]
        print(f"ACCEPTED · prose {len(prose)} chars (never parsed)")
        return 0

    refusal = [
        f"refused claim {v.index} ({v.claim}): {v.verdict} ({v.evidence})"
        for v in verdicts if v.verdict in NON_SUPPORTED
    ]
    if state.regens < MAX_REGENS:
        path, _ = emit_call(
            conn, atlas, out_dir, state.hfid, state.col_id,
            max_records=max_records, context=context,
            notes=tuple(refusal), regens=state.regens + 1,
        )
        print(f"REFUSED — regen call emitted: {path}")
        return 1
    seq = next_seq(out_dir)
    dry_path = out_dir / f"dry_{seq:04d}.md"
    brief = build_pov_brief(
        conn, atlas, state.hfid, state.col_id,
        max_records=max_records, context=context,
    )
    dry_path.write_text(render_dry(brief), encoding="utf-8")
    print(f"EXHAUSTED (regens {state.regens}/{MAX_REGENS}) — dry floor:"
          f" {dry_path}")
    return 2


# ---------------------------------------------------------------------------
# Case listing + the retrieval stress test


def list_cases(
    conn: sqlite3.Connection, atlas: df_taxonomy._Atlas,
    count: int = 8, min_events: int = 10,
) -> str:
    """Deterministic case list: battles/beast attacks by member count,
    one median-reach POV candidate each (quantile spread, no RNG)."""
    rows = conn.execute(
        "SELECT c.id, c.type, c.start_year, c.end_year,"
        " (SELECT COUNT(*) FROM event_membership m WHERE m.collection_id = c.id)"
        " FROM collections c WHERE c.type IN ('battle', 'beast attack')"
        " ORDER BY 5 DESC, c.id"
    ).fetchall()
    rows = [r for r in rows if r[4] >= min_events]
    picks = [rows[i] for i in df_taxonomy._spread(len(rows), count)]
    out = ["# bg-3 case list — pick (figure, battle) pairs for live sessions",
           f"{len(rows)} collections with >= {min_events} member events;"
           f" quantile spread by member count, {len(picks)} shown"]
    for col_id, col_type, start, end, members in picks:
        name_row = conn.execute(
            "SELECT value FROM collection_fields WHERE collection_id = ?"
            " AND key = 'name'", (col_id,),
        ).fetchone()
        name = name_row[0] if name_row else "?"
        totals = {
            hfid: (in_battle, total)
            for hfid, in_battle, total in conn.execute(
                "SELECT p.hfid, COUNT(*),"
                " (SELECT COUNT(*) FROM event_participant p2"
                "  WHERE p2.hfid = p.hfid)"
                " FROM event_participant p"
                " JOIN event_membership m ON m.event_id = p.event_id"
                " WHERE m.collection_id = ? GROUP BY p.hfid", (col_id,),
            )
        }
        # richest in-battle participant: the figure who lived the battle most
        pov = max(totals, key=lambda h: (totals[h][0], totals[h][1], h)) if totals else None
        pov_desc = (
            f"hf {pov} ({totals[pov][0]} in-battle records,"
            f" {totals[pov][1]} total)" if pov is not None else "none (no figure participants)"
        )
        span = f"y{start}-{end}" if end != start else f"y{start}"
        out.append(
            f"- col {col_id} · {col_type} '{name}' · {span} · {members} member"
            f" events · {len(totals)} participants · POV candidate: {pov_desc}"
        )
    return "\n".join(out) + "\n"


def _pct(values: list[float], pct: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    index = min(len(ordered) - 1, round(pct / 100 * (len(ordered) - 1)))
    return ordered[index]


def run_stress(
    db_path: Path, atlas: df_taxonomy._Atlas, picks: int = 64,
    max_records: int = 60,
) -> tuple[str, dict[str, Any]]:
    """The retrieval stress test: scan/build latency + brief size over a
    deterministic figure spread; double-build byte-compare probe."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = None
    counts = [
        (hfid, total)
        for hfid, total in conn.execute(
            "SELECT hfid, COUNT(*) FROM event_participant GROUP BY hfid"
            " ORDER BY COUNT(*) DESC, hfid"
        )
    ]
    selected = [counts[i] for i in df_taxonomy._spread(len(counts), picks)]
    stats: dict[str, list[float]] = {"scan_ms": [], "build_ms": [], "bytes": []}
    truncated = 0
    determinism_pass = True
    for hfid, _total in selected:
        t0 = time.perf_counter()
        records = _records_query(conn, hfid)
        t1 = time.perf_counter()
        brief = build_pov_brief(conn, atlas, hfid, None, max_records=max_records)
        t2 = time.perf_counter()
        again = build_pov_brief(
            conn, atlas, hfid, None, max_records=max_records
        )
        if again.text != brief.text:
            determinism_pass = False
        stats["scan_ms"].append((t1 - t0) * 1000)
        stats["build_ms"].append((t2 - t1) * 1000)
        stats["bytes"].append(len(brief.text.encode("utf-8")))
        truncated += 1 if brief.truncated > 0 else 0
        del records
    events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    figures = conn.execute("SELECT COUNT(*) FROM figures").fetchone()[0]
    mentions = [total for _, total in counts]
    report = [
        f"# bg-3 retrieval stress — {db_path.stem}",
        f"events {events:,} · figures {figures:,} · indexed participants"
        f" {len(counts):,} · db {db_path.stat().st_size / 1e6:.0f} MB",
        f"records/figure: p50 {_pct(mentions, 50):.0f} · p90 {_pct(mentions, 90):.0f}"
        f" · p99 {_pct(mentions, 99):.0f} · max {max(mentions):,}",
        f"figure spread: {len(selected)} of {len(counts)} (quantiles over the"
        f" mention distribution); brief cap {max_records} records",
        f"content determinism (double-build byte-compare):"
        f" {'PASS' if determinism_pass else 'FAIL'}",
        "",
        "timings (environment-specific, perf-1's labeling law; single thread):",
    ]
    for key, unit in (("scan_ms", "ms"), ("build_ms", "ms"), ("bytes", "B")):
        vals = stats[key]
        report.append(
            f"  {key}: p50 {_pct(vals, 50):.1f} {unit} · p90 {_pct(vals, 90):.1f}"
            f" · p99 {_pct(vals, 99):.1f} · max {max(vals):.1f}"
        )
    report.append(
        f"  briefs truncated at the cap: {truncated}/{len(selected)}"
        " (the loud marker; never a silent drop)"
    )
    conn.close()
    summary = {
        "picks": len(selected), "truncated": truncated,
        "determinism": "PASS" if determinism_pass else "FAIL",
        "scan_p99_ms": _pct(stats["scan_ms"], 99),
        "build_p99_ms": _pct(stats["build_ms"], 99),
        "bytes_p99": _pct(stats["bytes"], 99),
    }
    return "\n".join(report) + "\n", summary


# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("db", type=Path, help="sink DB (output/df_world_<stem>.sqlite3)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_cases = sub.add_parser("cases", help="list (figure, battle) case candidates")
    p_cases.add_argument("--count", type=int, default=8)
    p_cases.add_argument("--min-events", type=int, default=10)

    p_call = sub.add_parser("call", help="emit the next POV brief call file")
    p_call.add_argument("--figure", type=int, required=True)
    p_call.add_argument("--collection", type=int, default=None)
    p_call.add_argument("--max-records", type=int, default=60)
    p_call.add_argument("--context", type=int, default=8)
    p_call.add_argument("--out", type=Path, default=DEFAULT_OUT)

    p_apply = sub.add_parser("apply", help="validate a reply; drive the regen ladder")
    p_apply.add_argument("--call", type=Path, required=True)
    p_apply.add_argument("--reply", type=Path, required=True)
    p_apply.add_argument("--max-records", type=int, default=60)
    p_apply.add_argument("--context", type=int, default=8)
    p_apply.add_argument("--out", type=Path, default=DEFAULT_OUT)

    p_stress = sub.add_parser("stress", help="the retrieval stress test")
    p_stress.add_argument("--picks", type=int, default=64)
    p_stress.add_argument("--max-records", type=int, default=60)
    p_stress.add_argument("--out", type=Path, default=DEFAULT_OUT)

    args = parser.parse_args(argv)
    if not args.db.exists():
        print(f"no such sink DB: {args.db}", file=sys.stderr)
        return 1
    conn = sqlite3.connect(args.db)
    atlas = df_taxonomy._Atlas(conn)
    try:
        if args.command == "cases":
            print(list_cases(conn, atlas, count=args.count,
                             min_events=args.min_events), end="")
            return 0
        if args.command == "call":
            path, brief = emit_call(
                conn, atlas, args.out, args.figure, args.collection,
                max_records=args.max_records, context=args.context,
            )
            print(brief.text, end="")
            print(f"\n( call file: {path} )", file=sys.stderr)
            return 0
        if args.command == "apply":
            return apply_reply(
                conn, atlas, args.call, args.reply, args.out,
                max_records=args.max_records, context=args.context,
            )
        if args.command == "stress":
            report, summary = run_stress(
                args.db, atlas, picks=args.picks, max_records=args.max_records,
            )
            args.out.mkdir(parents=True, exist_ok=True)
            # large and medium share the slot stem region2-00500-01-01 —
            # the parent dir (the world label) keeps the reports apart
            stem = args.db.stem.removeprefix("df_world_")
            out_path = args.out / f"stress_{args.db.parent.name}_{stem}.txt"
            out_path.write_text(report, encoding="utf-8")
            print(report, end="")
            print(f"( report file: {out_path} )", file=sys.stderr)
            print(json.dumps(summary), file=sys.stderr)
            return 0
    except BrieferError as exc:
        # the shape gate: loud, nothing validated, never a repair
        print(f"BRIEFER ERROR (shape gate): {exc}", file=sys.stderr)
        return 3
    finally:
        conn.close()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
