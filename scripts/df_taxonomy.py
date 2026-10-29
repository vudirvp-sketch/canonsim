"""DF event taxonomy survey (bg-2 — the bg-2-event-taxonomy task).

Selects a deterministic spread of "interesting" events per target type
(the 16 of `docs/TASKS.md` bg-2: birth, death, murder, theft, betrayal,
artifact creation, site destruction, war, journey, captivity, escape,
founding, item loss, madness, transformation, catastrophe) from a sink
DB (`scripts/df_import.py`, D-051) and reconstructs, per entry, what
`docs/TAXONOMY.md` distills: participants, place, cause, witness,
long-term consequence. Selection is a fixed quantile spread over the
id-ascending candidate list — pure function of the DB content, no RNG,
no wall-clock in the report (the stderr timing line is informational
only; the survey's track law).

Honest notes baked in (the bg-2 law):

- **Causality is reconstructed, not parsed** — from role fields
  (slayer, snatcher, corruptor, changer) and `event_collections`
  grouping, never from a through-going cause field. The report renders
  the reconstruction, labeled as such.
- **Witnesses do not exist as data.** DF events carry no witness field;
  the report counts the nearest `hfs formed reputation relationship`
  event involving the entry's figures within +/-10 years (the
  epistemology mapping of `docs/ref/df_legends_xml.md`) — "none
  recorded" is the honest default, and it is the norm.
- **War casualties are lower bounds** — identical repeated
  `attacking_squad_deaths`/`defending_squad_deaths` values collapse in
  the EAV dedup (the D-051 law); distinct sums only.
- **birth is a gap** — no DF event type records births; the figure
  table's `birth_year` is the only source (rendered as the measured
  gap row, zero entries).
- Theft detail (thief, item, method) and beast-attack victims live
  ONLY in the plus companion — requires `sink_version >= 2` (the bg-2
  plus pass); on a v1 DB those plans degrade to zero candidates with a
  loud stderr warning.

Usage:
    python scripts/df_taxonomy.py output/df_world_<stem>.sqlite3 [--per-type N]

Output: `output/df_taxonomy_<stem>.txt` (gitignored runtime artifact,
reproducible from the same DB) + a stdout summary.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO / "output"

REP_TYPE = "hfs formed reputation relationship"
_FOLLOW_FACT_KEYS = (
    "cause", "crime", "mood", "new_race", "state", "theft_method",
    "successful", "action", "prison_months", "return",
)


def _ref(text: str | None) -> int | None:
    """Integer id reference; None when absent, unparseable, or -1."""
    if text is None:
        return None
    try:
        value = int(text)
    except ValueError:
        return None
    return value if value != -1 else None


@dataclass
class TypePlan:
    """One DF source feeding one bg-2 target type (event plans)."""

    target: str
    df_type: str
    where: str = ""              # extra SQL over events e (AND-joined)
    params: tuple[Any, ...] = ()
    roles: tuple[tuple[str, str], ...] = ()   # (EAV key, role label)
    plus_roles: tuple[tuple[str, str], ...] = ()  # (plus EAV key, label)
    place_keys: tuple[str, ...] = ("site_id",)
    follow: str = "participants"  # 'participants' | 'artifact' | 'site'
    note: str = ""
    candidates_label: str = ""


@dataclass
class CollectionPlan:
    """A collection-typed source (war, journey groupings, beast attacks)."""

    target: str
    col_type: str
    note: str = ""
    beast: bool = False  # catastrophe: lift the eater from a devoured member


_PLANS: tuple[TypePlan, ...] = (
    TypePlan(
        target="death", df_type="hf died",
        where=(
            "EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'cause' AND f.value IN ('old age', 'struck', 'shot'))"
            " AND EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'site_id' AND f.value != '-1')"
        ),
        roles=(("hfid", "victim"), ("slayer_hfid", "slayer"), ("cause", "cause")),
        note="non-murder deaths; 'hf died' carries victim/slayer/cause/site",
    ),
    TypePlan(
        target="murder", df_type="hf died",
        where=(
            "EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'cause' AND f.value = 'murdered')"
            " AND EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'slayer_hfid' AND f.value != '-1')"
            " AND EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'site_id' AND f.value != '-1')"
        ),
        roles=(("hfid", "victim"), ("slayer_hfid", "slayer"), ("cause", "cause")),
        note="cause 'murdered' with a named slayer",
    ),
    TypePlan(
        target="theft", df_type="item stolen",
        where=(
            "EXISTS (SELECT 1 FROM event_plus_fields p WHERE p.event_id = e.id"
            " AND p.key = 'histfig' AND p.value != '-1')"
        ),
        roles=(),
        plus_roles=(
            ("histfig", "thief"), ("mat", "item"), ("item_type", "item kind"),
            ("theft_method", "method"),
        ),
        place_keys=("site",),
        note="detail (thief/item/method) lives only in the plus companion",
    ),
    TypePlan(
        target="betrayal", df_type="hfs formed intrigue relationship",
        roles=(
            ("corruptor_hfid", "corruptor"), ("target_hfid", "target"),
            ("method", "method"), ("action", "action"), ("successful", "outcome"),
        ),
        note=("betrayal is RECONSTRUCTED: the intrigue family (corruptor/"
              "target/seen-as); 'assume identity' is the identity-betrayal flavor"),
    ),
    TypePlan(
        target="artifact creation", df_type="artifact created",
        where=(
            "EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'hist_figure_id' AND f.value != '-1')"
            " AND EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'site_id' AND f.value != '-1')"
        ),
        roles=(("hist_figure_id", "creator"), ("artifact_id", "artifact")),
        follow="artifact",
        note="follow-up = the artifact's next recorded custody event",
    ),
    TypePlan(
        target="site destruction", df_type="destroyed site",
        roles=(("attacker_civ_id", "attacker"), ("defender_civ_id", "defender")),
        follow="site",
        note="'hf destroyed site'/'razed structure' are the sibling flavors",
    ),
    TypePlan(
        target="journey", df_type="hf travel",
        where=(
            "EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'site_id' AND f.value != '-1')"
        ),
        roles=(("group_hfid", "traveler"), ("return", "return")),
        note="journey collections group these; 'return' marks round trips",
    ),
    TypePlan(
        target="captivity", df_type="hf abducted",
        where=(
            "EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'site_id' AND f.value != '-1')"
        ),
        roles=(("target_hfid", "victim"), ("snatcher_hfid", "snatcher")),
        note="'hf enslaved'/'hf ransomed' are the downstream fates",
    ),
    TypePlan(
        target="escape", df_type="hf ransomed",
        roles=(
            ("ransomed_hfid", "captive"), ("ransomer_hfid", "ransomer"),
            ("payer_hfid", "payer"), ("payer_entity_id", "payer entity"),
            ("moved_to_site_id", "moved to"),
        ),
        note=("no bare escape event type exists — ransoms are the recorded"
              " captivity exit; 'flight' (change-hf-state reason) is the flee flavor"),
    ),
    TypePlan(
        target="founding", df_type="created site",
        where=(
            "EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'builder_hfid' AND f.value != '-1')"
        ),
        roles=(("civ_id", "civ"), ("builder_hfid", "builder")),
        follow="site",
        note="'entity created'/'created structure' are the sibling flavors",
    ),
    TypePlan(
        target="item loss", df_type="artifact lost",
        where=(
            "EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'artifact_id' AND f.value != '-1')"
        ),
        roles=(("artifact_id", "artifact"),),
        follow="artifact",
        note="'artifact destroyed'/'artifact given' are the sibling flavors",
    ),
    TypePlan(
        target="madness", df_type="change hf state",
        where=(
            "EXISTS (SELECT 1 FROM event_fields f WHERE f.event_id = e.id"
            " AND f.key = 'mood')"
        ),
        roles=(("hfid", "figure"), ("mood", "mood"), ("state", "state")),
        note="moods: fey/secretive/possessed/insane/melancholy/macabre/berserk/fell",
    ),
    TypePlan(
        target="transformation", df_type="changed creature type",
        roles=(
            ("changee_hfid", "changee"), ("changer_hfid", "changer"),
            ("old_race", "from"), ("new_race", "to"),
        ),
        note="forced goblinkidnapping conversions ride this type (abductees)",
    ),
)

_COLLECTION_PLANS: tuple[CollectionPlan, ...] = (
    CollectionPlan(
        target="war", col_type="war",
        note="war collections nest battle collections; casualty sums are lower bounds",
    ),
    CollectionPlan(
        target="catastrophe", col_type="beast attack", beast=True,
        note="beast attacks group devour/theft/died events; eater from the plus pass",
    ),
)

# Targets with no DF event source at all — rendered as measured gaps.
_GAP_TARGETS = ("birth",)


class _Atlas:
    """Name resolution over the sink (figures, sites, entities, regions,
    artifacts); ids without a record render as bare ids."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._figure = self._names_from_fields(conn)
        self._figure_race = {
            row[0]: row[1] for row in conn.execute("SELECT id, race FROM figures")
        }
        self._record = {}
        for tag in ("site", "entity", "region", "artifact"):
            self._record[tag] = self._names_from_records(conn, tag)

    @staticmethod
    def _names_from_fields(conn: sqlite3.Connection) -> dict[int, str]:
        return {
            int(fid): value
            for fid, value in conn.execute(
                "SELECT figure_id, value FROM figure_fields WHERE key = 'name'"
            )
        }

    @staticmethod
    def _names_from_records(conn: sqlite3.Connection, tag: str) -> dict[int, str]:
        names: dict[int, str] = {}
        for rid, data in conn.execute(
            "SELECT id, data FROM records WHERE record_tag = ?", (tag,)
        ):
            try:
                payload = json.loads(data)
            except ValueError:
                continue
            raw = payload.get("name") or [""]
            if isinstance(raw, list) and raw:
                names[int(rid)] = str(raw[0])
        return names

    def figure(self, hfid: int | None) -> str:
        if hfid is None:
            return "?"
        name = self._figure.get(hfid)
        if name is None:
            return f"hf {hfid}"
        race = self._figure_race.get(hfid, "")
        return f"{name} [hf {hfid}{', ' + race if race else ''}]"

    def _tagged(self, tag: str, ident: int | None, label: str) -> str:
        if ident is None:
            return "?"
        name = self._record[tag].get(ident)
        return f"{name or label} [{label} {ident}]" if name else f"{label} {ident}"

    def site(self, ident: int | None) -> str:
        return self._tagged("site", ident, "site")

    def entity(self, ident: int | None) -> str:
        return self._tagged("entity", ident, "entity")

    def region(self, ident: int | None) -> str:
        return self._tagged("region", ident, "region")

    def artifact(self, ident: int | None) -> str:
        return self._tagged("artifact", ident, "artifact")


@dataclass
class _Entry:
    lines: list[str] = field(default_factory=list)
    hfids: tuple[int, ...] = ()
    summary: dict[str, str] = field(default_factory=dict)


def _spread(count: int, n: int) -> list[int]:
    """Deterministic quantile indices into an id-ascending list."""
    if count <= 0:
        return []
    if count <= n:
        return list(range(count))
    step = (count - 1) / (n - 1)
    return sorted({min(count - 1, round(i * step)) for i in range(n)})


def _event_fields(
    conn: sqlite3.Connection, table: str, event_id: int
) -> dict[str, str]:
    """Single-value view: alphabetically-first value per key (the EAV may
    hold repeated keys; identical values already collapsed at import)."""
    return {
        key: value
        for key, value in conn.execute(
            f"SELECT key, value FROM {table} WHERE event_id = ?"
            " ORDER BY key, value",  # noqa: S608 — table from a fixed literal
            (event_id,),
        )
    }


def _place(atlas: _Atlas, main: dict[str, str], plus: dict[str, str]) -> str:
    for key in ("site_id", "site"):
        ident = _ref(main.get(key) or plus.get(key))
        if ident is not None:
            return atlas.site(ident)
    ident = _ref(main.get("subregion_id"))
    if ident is not None:
        return atlas.region(ident)
    ident = _ref(main.get("feature_layer_id"))
    if ident is not None:
        return f"feature layer {ident}"
    return "no place recorded"


def _collection_of(
    conn: sqlite3.Connection, atlas: _Atlas, event_id: int
) -> str:
    rows = conn.execute(
        "SELECT c.id, c.type, c.start_year, c.end_year FROM event_membership m"
        " JOIN collections c ON c.id = m.collection_id WHERE m.event_id = ?"
        " ORDER BY c.id",
        (event_id,),
    ).fetchall()
    parts = []
    for col_id, col_type, start_year, end_year in rows:
        extras = dict(conn.execute(
            "SELECT key, value FROM collection_fields WHERE collection_id = ?"
            " AND key IN ('name', 'attacking_enid', 'defending_enid')",
            (col_id,),
        ))
        detail = ""
        if extras.get("name"):
            detail = f" {extras['name']!r}"
        elif "attacking_enid" in extras or "defending_enid" in extras:
            key = "attacking_enid" if "attacking_enid" in extras else "defending_enid"
            detail = f" [{key} {atlas.entity(_ref(extras[key]))}]"
        span = f"y{start_year}-y{end_year}" if end_year != start_year else f"y{start_year}"
        parts.append(f"{col_type} col {col_id}{detail} {span}")
    return "; ".join(parts) if parts else "no grouping recorded"


def _witness(conn: sqlite3.Connection, hfids: tuple[int, ...], year: int) -> str:
    """Nearest reputation-relationship link involving the entry's figures
    within +/-10 years — the closest DF analog of a witness record.

    Queries the EAV directly: reputation events key their figures as
    hfid1/hfid2, which the participant lift rule (tags ending in 'hfid')
    does not match — a measured blind spot of the sink index, noted in
    `docs/TAXONOMY.md`.
    """
    if not hfids:
        return "n/a (no figure participants)"
    marks = ",".join("?" * len(hfids))
    rows = conn.execute(
        f"SELECT DISTINCT e.id, e.year FROM events e"
        f" JOIN event_fields f ON f.event_id = e.id"
        f" AND f.key IN ('hfid1', 'hfid2') WHERE e.type = ? AND f.value IN ({marks})"
        " AND e.year BETWEEN ? AND ? ORDER BY ABS(e.year - ?), e.id LIMIT 2",
        (REP_TYPE, *(str(h) for h in hfids), year - 10, year + 10, year),
    ).fetchall()
    if not rows:
        return "none recorded (no witness field exists in DF events)"
    nearest = rows[0]
    return f"nearest {REP_TYPE!r} ev {nearest[0]} y{nearest[1]}"


def _followups(
    conn: sqlite3.Connection,
    atlas: _Atlas,
    entry: _Entry,
    *,
    exclude_id: int,
    year: int,
    mode: str,
    main: dict[str, str],
    plus: dict[str, str],
) -> list[str]:
    """The next recorded facts involving the entry's subject — the honest
    'long-term consequence': what the log actually shows later, no more."""
    rendered: list[str] = []
    rows: list[tuple] = []
    if mode == "participants" and entry.hfids:
        marks = ",".join("?" * len(entry.hfids))
        rows = conn.execute(
            f"SELECT DISTINCT e.id, e.type, e.year FROM events e"
            f" JOIN event_participant p ON p.event_id = e.id"
            f" WHERE p.hfid IN ({marks}) AND e.id != ? AND e.year >= ?"
            " ORDER BY e.year, e.id LIMIT 2",
            (*entry.hfids, exclude_id, year),
        ).fetchall()
    elif mode == "artifact":
        artifact_id = _ref(main.get("artifact_id"))
        if artifact_id is not None:
            rows = conn.execute(
                "SELECT e.id, e.type, e.year FROM events e JOIN event_fields f"
                " ON f.event_id = e.id WHERE f.key = 'artifact_id' AND f.value = ?"
                " AND e.id != ? AND e.year >= ? ORDER BY e.year, e.id LIMIT 2",
                (str(artifact_id), exclude_id, year),
            ).fetchall()
    elif mode == "site":
        site_id = _ref(main.get("site_id")) or _ref(plus.get("site"))
        if site_id is not None:
            rows = conn.execute(
                "SELECT e.id, e.type, e.year FROM events e JOIN event_fields f"
                " ON f.event_id = e.id WHERE f.key = 'site_id' AND f.value = ?"
                " AND e.id != ? AND e.year > ? ORDER BY e.year, e.id LIMIT 2",
                (str(site_id), exclude_id, year),
            ).fetchall()
    for event_id, event_type, event_year in rows:
        facts = _event_fields(conn, "event_fields", event_id)
        detail = ""
        for key in _FOLLOW_FACT_KEYS:
            value = facts.get(key)
            if value is not None and value != "-1" and value.strip():
                detail = f" ({key} {value})"
                break
        rendered.append(f"y{event_year} '{event_type}'{detail} ev {event_id}")
    return rendered or ["none within the log (terminal or orphaned)"]


_ENTITY_ROLE_KEYS = frozenset({"attacker_civ_id", "defender_civ_id", "civ_id", "payer_entity_id"})
_SITE_ROLE_KEYS = frozenset({"moved_to_site_id"})
_ARTIFACT_ROLE_KEYS = frozenset({"artifact_id"})


def _role_render(
    plan: TypePlan, atlas: _Atlas, main: dict[str, str], plus: dict[str, str]
) -> tuple[str, tuple[int, ...]]:
    """Render the plan's role fields: ids resolve to names, figures are
    also collected as participants for the witness/consequence queries."""
    parts: list[str] = []
    hfids: list[int] = []
    for key, label in plan.roles + plan.plus_roles:
        source = main if (key, label) in plan.roles else plus
        raw = source.get(key)
        if raw is None or raw == "-1":
            continue
        if raw == "":
            # DF presence flag: an empty element means true (return/successful).
            parts.append(f"{label}: yes")
            continue
        ident = _ref(raw)
        if key in _ENTITY_ROLE_KEYS and ident is not None:
            parts.append(f"{label}: {atlas.entity(ident)}")
        elif key in _SITE_ROLE_KEYS and ident is not None:
            parts.append(f"{label}: {atlas.site(ident)}")
        elif key in _ARTIFACT_ROLE_KEYS and ident is not None:
            parts.append(f"{label}: {atlas.artifact(ident)}")
        elif ident is not None and (
            key.endswith("hfid") or key in ("hist_figure_id", "histfig")
        ):
            parts.append(f"{label}: {atlas.figure(ident)}")
            hfids.append(ident)
        else:
            parts.append(f"{label}: {raw}")
    return "; ".join(parts) or "no named participants", tuple(sorted(set(hfids)))


def _render_event_entry(
    conn: sqlite3.Connection,
    atlas: _Atlas,
    plan: TypePlan,
    event_id: int,
    picked: int,
    index: int,
) -> _Entry:
    row = conn.execute(
        "SELECT id, type, year, seconds72 FROM events WHERE id = ?", (event_id,)
    ).fetchone()
    event_type, year = row[1], row[2]
    main = _event_fields(conn, "event_fields", event_id)
    plus = _event_fields(conn, "event_plus_fields", event_id) if _has_plus(conn) else {}
    entry = _Entry()
    roles, hfids = _role_render(plan, atlas, main, plus)
    entry.hfids = hfids
    entry.lines = [
        f"entry {index + 1}/{picked} · event {event_id} · '{event_type}' · year {year}",
        f"    participants: {roles}",
        f"    place: {_place(atlas, main, plus)}",
        f"    cause (reconstructed): {_collection_of(conn, atlas, event_id)}"
        f"{'; roles above' if roles != 'no named participants' else ''}",
        f"    witness: {_witness(conn, hfids, year)}",
        "    consequence: "
        + "; ".join(
            _followups(
                conn, atlas, entry, exclude_id=event_id, year=year,
                mode=plan.follow, main=main, plus=plus,
            )
        ),
    ]
    entry.summary = {"event": str(event_id), "year": str(year)}
    return entry


def _has_plus(conn: sqlite3.Connection) -> bool:
    """True when the import actually ingested a companion: the table itself
    is always created (sink v2 schema) — the meta flag is the honest source
    (a companion with zero events still records 'imported')."""
    row = conn.execute(
        "SELECT value FROM meta WHERE key = 'plus_companion'"
    ).fetchone()
    return bool(row and row[0] == "imported")


def _render_collection_entry(
    conn: sqlite3.Connection, atlas: _Atlas, plan: CollectionPlan,
    col_id: int, picked: int, index: int,
) -> _Entry:
    row = conn.execute(
        "SELECT id, type, start_year, end_year FROM collections WHERE id = ?",
        (col_id,),
    ).fetchone()
    _, col_type, start_year, end_year = row
    fields = {
        key: value
        for key, value in conn.execute(
            "SELECT key, value FROM collection_fields WHERE collection_id = ?"
            " ORDER BY key, value",
            (col_id,),
        )
    }
    children = conn.execute(
        "SELECT COUNT(*) FROM collection_parent WHERE parent_id = ?", (col_id,)
    ).fetchone()[0]
    members = conn.execute(
        "SELECT e.id, e.type, e.year FROM event_membership m JOIN events e"
        " ON e.id = m.event_id WHERE m.collection_id = ? ORDER BY e.year, e.id",
        (col_id,),
    ).fetchall()
    entry = _Entry()
    hfids: list[int] = []
    span = (
        f"years {start_year}-ongoing" if end_year == -1
        else f"years {start_year}-{end_year}" if end_year != start_year
        else f"year {start_year}"
    )
    site_id = _ref(fields.get("site_id"))
    place = (
        atlas.site(site_id) if site_id is not None
        else "no single place (theater-level collection)"
    )
    lines = [
        f"entry {index + 1}/{picked} · collection {col_id} · '{col_type}' · {span}",
        f"    place: {place}",
    ]
    if plan.col_type == "war":
        name = fields.get("name", "?")
        aggressor = atlas.entity(_ref(fields.get("aggressor_ent_id")))
        defender = atlas.entity(_ref(fields.get("defender_ent_id")))
        deaths = [
            int(row[0])
            for row in conn.execute(
                "SELECT cf.value FROM collection_fields cf"
                " JOIN collection_parent cp ON cp.child_id = cf.collection_id"
                " WHERE cp.parent_id = ? AND cf.key IN"
                " ('attacking_squad_deaths', 'defending_squad_deaths')",
                (col_id,),
            )
            if row[0].lstrip("-").isdigit()
        ]
        lines.insert(1, f"    name: {name!r} · aggressor {aggressor} vs defender {defender}")
        if deaths:
            lines.append(
                f"    scale: {children} nested battles · {len(members)} direct member"
                f" events · casualty sum >= {sum(deaths)} (distinct-values lower bound)"
            )
        else:
            lines.append(
                f"    scale: {children} nested battles · {len(members)} direct member"
                " events · no squad-deaths recorded"
            )
    else:  # beast attack
        kinds: dict[str, int] = {}
        beast_hfid: int | None = None
        for member_id, member_type, _ in members:
            kinds[member_type] = kinds.get(member_type, 0) + 1
            if beast_hfid is None and member_type == "creature devoured" and _has_plus(conn):
                eater = _ref(_event_fields(conn, "event_plus_fields", member_id).get("eater"))
                if eater is not None:
                    beast_hfid = eater
        defender = atlas.entity(_ref(fields.get("defending_enid")))
        lines.insert(1, f"    defender: {defender}")
        lines.append(
            "    members: "
            + (", ".join(f"{count} '{kind}'" for kind, count in sorted(kinds.items()))
               or "no direct events")
        )
        if beast_hfid is not None:
            hfids = [beast_hfid]
            lines.append(f"    beast: {atlas.figure(beast_hfid)}")
    entry.hfids = tuple(hfids)
    if plan.beast and hfids:
        fate = conn.execute(
            "SELECT e.id, e.type, e.year, f.value FROM events e"
            " JOIN event_participant p ON p.event_id = e.id"
            " JOIN event_fields f ON f.event_id = e.id AND f.key = 'cause'"
            " WHERE e.type = 'hf died' AND p.hfid = ? AND e.year >= ?"
            " ORDER BY e.year, e.id LIMIT 1",
            (hfids[0], end_year),
        ).fetchone()
        if fate:
            lines.append(
                f"    consequence (beast's fate): y{fate[2]} '{fate[1]}'"
                f" (cause {fate[3]}) ev {fate[0]}"
            )
        else:
            lines.append("    consequence (beast's fate): no recorded death (alive or orphan)")
    entry.lines = lines
    entry.summary = {"collection": str(col_id)}
    return entry


def _target_gap_note(target: str, conn: sqlite3.Connection) -> list[str]:
    if target == "birth":
        stats = conn.execute(
            "SELECT COUNT(*), MIN(birth_year), MAX(birth_year) FROM figures"
        ).fetchone()
        return [
            "target: birth — GAP: no DF event type records births.",
            f"    measured: {stats[0]:,} figures carry birth_year "
            f"({stats[1]} .. {stats[2]}) — derivable, never evented.",
            "    ontology: our schema would carry it as an event (actor=world,"
            " state_changes) — DF is the poorer side here.",
        ]
    return []


def build_report(db_path: Path, per_type: int = 8) -> tuple[str, dict[str, Any]]:
    """Build the full taxonomy report text; returns (report, summary)."""
    conn = sqlite3.connect(db_path)
    try:
        sink_version = int(
            conn.execute(
                "SELECT value FROM meta WHERE key = 'sink_version'"
            ).fetchone()[0]
        )
        plus_missing = not _has_plus(conn)
        atlas = _Atlas(conn)
        out: list[str] = [
            f"# DF event taxonomy survey — {db_path.stem}",
            f"source: {dict(conn.execute('SELECT key, value FROM meta'))['source']}"
            f" · sink_version {sink_version} · per-type {per_type}",
            "selection: fixed quantile spread over the id-ascending candidate"
            " list — deterministic, reproducible from the same DB.",
        ]
        if plus_missing:
            out.append(
                "WARNING: event_plus_fields missing (v1 sink) — theft/catastrophe"
                " plans degrade; re-import with the plus companion."
            )
        summary: dict[str, Any] = {"entries": 0, "targets": 0, "gaps": []}
        for target in _GAP_TARGETS:
            out.append("")
            out.append("=" * 72)
            out.extend(_target_gap_note(target, conn))
            summary["targets"] += 1
        for plan in _PLANS:
            where = f" WHERE e.type = ?{(' AND ' + plan.where) if plan.where else ''}"
            if plus_missing and "event_plus_fields" in where:
                ids: list[int] = []  # plus-dependent filter cannot run on a v1 sink
            else:
                ids = [
                    row[0]
                    for row in conn.execute(
                        f"SELECT e.id FROM events e{where} ORDER BY e.id",  # noqa: S608
                        (plan.df_type, *plan.params),
                    )
                ]
            out.append("")
            out.append("=" * 72)
            label = f", {plan.candidates_label}" if plan.candidates_label else ""
            out.append(
                f"target: {plan.target} — DF '{plan.df_type}'"
                f" ({len(ids):,} candidates{label})"
            )
            if plan.note:
                out.append(f"note: {plan.note}")
            if plus_missing and plan.plus_roles:
                out.append("DEGRADED (v1 sink — plus fields absent)")
            picks = [ids[i] for i in _spread(len(ids), per_type)]
            for index, event_id in enumerate(picks):
                entry = _render_event_entry(
                    conn, atlas, plan, event_id, len(picks), index
                )
                out.extend(entry.lines)
                summary["entries"] += 1
            if not picks:
                out.append("    (no candidates after filters)")
            else:
                shape = sorted(
                    _event_fields(conn, "event_fields", picks[0])
                    | _event_fields(conn, "event_plus_fields", picks[0])
                )
                out.append(f"event field shape: {', '.join(shape)}")
            summary["targets"] += 1
        for plan in _COLLECTION_PLANS:
            ids = [
                row[0]
                for row in conn.execute(
                    "SELECT id FROM collections WHERE type = ? ORDER BY id",
                    (plan.col_type,),
                )
            ]
            out.append("")
            out.append("=" * 72)
            out.append(
                f"target: {plan.target} — collection '{plan.col_type}'"
                f" ({len(ids):,} candidates)"
            )
            if plan.note:
                out.append(f"note: {plan.note}")
            picked = [ids[i] for i in _spread(len(ids), per_type)]
            for index, col_id in enumerate(picked):
                entry = _render_collection_entry(
                    conn, atlas, plan, col_id, len(picked), index
                )
                out.extend(entry.lines)
                summary["entries"] += 1
            summary["targets"] += 1
        out.append("")
        out.append("=" * 72)
        out.append(
            f"total: {summary['entries']} entries across {summary['targets']} targets"
            f" (birth gap: figure birth_year only)"
        )
        return "\n".join(out) + "\n", summary
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("db", type=Path, help="sink DB (output/df_world_<stem>.sqlite3)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--per-type", type=int, default=8)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    report, summary = build_report(args.db, per_type=args.per_type)
    out_path = args.out / f"df_taxonomy_{args.db.stem.removeprefix('df_world_')}.txt"
    out_path.write_text(report, encoding="utf-8")
    print(f"  {summary['entries']} entries across {summary['targets']} targets"
          f" -> {out_path.name} in {time.perf_counter() - started:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
