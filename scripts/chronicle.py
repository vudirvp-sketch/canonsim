"""Mode F offline chronicler (leg-4, phase 4, D-093; `docs/TASKS.md`).

The offline analytics half of the knowledge layer — a DuckDB pipeline over
the committed JSONL log, NEVER in the runtime import graph (D-012): this
module imports no `core/`/`sim/`/`brief/` code and nothing in the runtime
imports it; it speaks only the published log-file contract
(`docs/EVENT_SCHEMA.md` §1–§2). The log is truth (INV-1); the chronicler
is convenience — every artifact here is derived and rebuildable.

Pipeline (the donor pattern set, `docs/ref/duckdb.md` "what we take"):

1. **Intake** — `read_ndjson_auto()` over the JSONL: the file IS the table
   (no-ETL). The run-header line unions into a NULL `id` and drops via
   `WHERE id IS NOT NULL` (measured: 55/55 events on day1 seed 123).
2. **Count gate** — every log line minus the header must appear as a row:
   DuckDB's row count is checked against a raw line count BEFORE any
   artifact is written. A silent drop is an integrity failure, never a
   partial archive (exit 1, nothing written).
3. **`events.parquet`** — the cold columnar archive: one row per event,
   the canonical field order (EVENT_SCHEMA §2), `ORDER BY id`.
4. **`state_diffs.parquet`** — per-actor state deltas: `state_changes`
   unnested, `LAG(to) OVER (PARTITION BY entity, prop ORDER BY t, id)` —
   the window-diff law; `continuous` is NULL on a state's first change
   (no previous), then `from == previous to` (the fold-consistency read).
5. **`chronicle.sqlite`** — the summary that flows back toward the
   runtime's stdlib reader (the "summary SQLite IS stdlib" adaptation):
   `facts_summary` (per actor), `state_current` (per entity+prop fold
   snapshot), `type_histogram`, `knowledge_summary` (per knower, by
   channel), `chronicle_meta` (the artifact's own identity).
6. **Write ladder** (probe + fallback, the L12 law): `SET
   autoinstall_known_extensions=false` closes the network door by
   construction; if the sqlite_scanner extension is locally available the
   summary is written through `ATTACH ... (TYPE SQLITE)` (the lifted
   pattern); otherwise through stdlib `sqlite3` (the never-breaks floor).
   Both paths are byte-deterministic per environment; the manifest and
   `chronicle_meta` record which one ran (`write_mode`).
7. **`manifest.json`** — content-derived audit record (log sha256, event
   count, the header's seed/schema_version/python/commit/pack, duckdb
   version, write mode, per-artifact sha256+rows). No wall-clock, no
   absolute paths: same log bytes + same environment = same manifest
   bytes (INV-2's spirit, offline).

Determinism: every query ends in explicit `ORDER BY`; parquet and sqlite
writes are byte-identical across runs in the same environment (measured).
Offline compaction (scavenge with tombstones) is NOT here — it is the
`scav-1` backlog row, phases.md §4's later half.

Usage:
    python scripts/chronicle.py logs/run_123_0.jsonl
    python -m scripts.chronicle logs/run_123_0.jsonl --min-events 100000
    python scripts/chronicle.py logs/run_123_0.jsonl --sqlite-via stdlib
Output: `output/chronicle/<log_stem>/` (gitignored runtime artifacts,
reproducible from the log at any time).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import duckdb

# Allow `python scripts/chronicle.py` and `python -m scripts.chronicle`
REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

#: The event line's canonical field order (EVENT_SCHEMA.md §2). The intake
#: projects these, in this order — absent fields (a log where no event
#: carries `target`, a header-only log) become typed NULLs, so every
#: downstream query and the archive schema are uniform: always 12 columns.
EVENT_FIELDS: tuple[str, ...] = (
    "id", "t", "type", "actor", "target", "cause", "outcome", "knowledge",
    "state_changes", "hooks", "importance", "provenance",
)

#: The typed-NULL substitution per canonical field (used only when the
#: field is absent from the file's union schema). Nested shapes follow
#: EVENT_SCHEMA.md §3–§4; scalar values stay JSON/VARCHAR-typed — the
#: downstream SQL casts on read, so detected and substituted types agree.
_FIELD_TYPES: dict[str, str] = {
    "id": "VARCHAR",
    "t": "BIGINT",
    "type": "VARCHAR",
    "actor": "VARCHAR",
    "target": "VARCHAR",
    "cause": "VARCHAR",
    "outcome": "JSON",
    "knowledge": 'STRUCT("who" VARCHAR, channel VARCHAR, fidelity VARCHAR, '
                 'knows VARCHAR, "at" BIGINT, "source" VARCHAR)[]',
    "state_changes": 'STRUCT(entity VARCHAR, prop VARCHAR, "from" JSON, '
                     '"to" JSON, irreversible BOOLEAN)[]',
    "hooks": "VARCHAR[]",
    "importance": "VARCHAR",
    "provenance": "JSON",
}

#: The run-header keys the manifest echoes (EVENT_SCHEMA.md §1).
_HEADER_KEYS: tuple[str, ...] = (
    "schema_version", "seed", "python", "commit", "pack",
)

#: The summary write paths: auto (attach when locally available, else the
#: stdlib floor), attach (forced, requires a local sqlite_scanner), stdlib.
SQLITE_VIA: tuple[str, ...] = ("auto", "attach", "stdlib")

_Meta = list[tuple[str, str]]

# -- the rollup SQL (single source; both write paths consume these) ----------
# Every query ends ORDER BY — determinism (the row order is the table order).


_SUMMARIES: tuple[tuple[str, str], ...] = (
    (
        "facts_summary",
        """
        SELECT actor,
               count(*) AS event_count,
               min(t) AS first_tick,
               max(t) AS last_tick,
               coalesce(sum(len(state_changes)), 0) AS state_changes,
               coalesce(sum(len(knowledge)), 0) AS knowledge_out
        FROM events GROUP BY actor ORDER BY actor
        """,
    ),
    (
        "state_current",
        """
        WITH flat AS (
            SELECT event_id, t, sc.entity AS entity, sc.prop AS prop,
                   CAST(sc.to AS VARCHAR) AS value
            FROM state_events
        ), ranked AS (
            SELECT entity, prop, value, event_id, t,
                   row_number() OVER (
                       PARTITION BY entity, prop ORDER BY t DESC, event_id DESC
                   ) AS rn,
                   count(*) OVER (PARTITION BY entity, prop) AS n_changes
            FROM flat
        )
        SELECT entity, prop, value, event_id AS last_event_id,
               t AS last_tick, n_changes
        FROM ranked WHERE rn = 1 ORDER BY entity, prop
        """,
    ),
    (
        "type_histogram",
        "SELECT type, count(*) AS n FROM events GROUP BY type ORDER BY type",
    ),
    (
        "knowledge_summary",
        """
        WITH ev AS (
            SELECT UNNEST(knowledge) AS k
            FROM events WHERE len(knowledge) > 0
        )
        SELECT k.who AS who,
               count(*) AS total,
               count(*) FILTER (k.channel = 'saw') AS saw,
               count(*) FILTER (k.channel = 'heard') AS heard,
               count(*) FILTER (k.channel = 'told') AS told,
               count(*) FILTER (k.channel = 'inferred') AS inferred
        FROM ev GROUP BY k.who ORDER BY k.who
        """,
    ),
)

#: duckdb column type -> sqlite column type (the stdlib write path).
_SQLITE_TYPES: dict[str, str] = {
    "VARCHAR": "TEXT",
    "BIGINT": "INTEGER",
    "INTEGER": "INTEGER",
    "BOOLEAN": "INTEGER",
}


class ChronicleError(RuntimeError):
    """Chronicler integrity failure (count gate, header shape, write path)."""


# -- small file helpers (no core imports: the offline graph stays decoupled) --


def sha256_file(path: Path) -> str:
    """Streamed file digest (never loads the log whole — token hygiene)."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_lines(path: Path) -> int:
    """Line count without parsing (token hygiene: never load the log)."""
    n = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            n += chunk.count(b"\n")
    return n


def read_header(path: Path) -> dict[str, Any]:
    """Line 1 only — the run header (EVENT_SCHEMA.md §1 shape)."""
    with path.open(encoding="utf-8") as fh:
        first = fh.readline()
    if not first.strip():
        raise ChronicleError(f"{path}: empty log (no header line)")
    data = json.loads(first)
    if data.get("header") is not True:
        raise ChronicleError(f"{path}: line 1 is not a run header (header != true)")
    missing = [k for k in _HEADER_KEYS if k not in data]
    if missing:
        raise ChronicleError(f"{path}: run header missing keys {missing}")
    return {k: data[k] for k in _HEADER_KEYS}


# -- the pipeline -------------------------------------------------------------


def _connect() -> duckdb.DuckDBPyConnection:
    """One in-memory handle; the network door closed by construction."""
    con = duckdb.connect()
    # The ref's offline law (duckdb.md "weaknesses"): INSTALL fetches from
    # the extension repository — the chronicler never phones home, even by
    # accident. Locally available extensions still load (autoload stays on).
    con.execute("SET autoinstall_known_extensions=false")
    return con


def _sqlite_scanner_available(con: duckdb.DuckDBPyConnection) -> bool:
    """True when sqlite_scanner is locally installed or loaded — the probe
    that decides the ATTACH rung without ever triggering a download."""
    row = con.execute(
        "SELECT installed OR loaded FROM duckdb_extensions() "
        "WHERE extension_name = 'sqlite_scanner'"
    ).fetchone()
    return bool(row and row[0])


def _write_sqlite_attach(
    con: duckdb.DuckDBPyConnection, path: Path, meta: _Meta
) -> None:
    """The lifted pattern: ATTACH a sqlite file, CTAS each summary into it."""
    con.execute(f"ATTACH '{path}' AS chrono (TYPE SQLITE)")
    try:
        for table, sql in _SUMMARIES:
            con.execute(f"CREATE TABLE chrono.{table} AS {sql}")
        _write_meta_attach(con, meta)
    finally:
        con.execute("DETACH chrono")


def _write_meta_attach(con: duckdb.DuckDBPyConnection, meta: _Meta) -> None:
    con.execute('CREATE TABLE chrono.chronicle_meta ("key" VARCHAR, "value" VARCHAR)')
    con.executemany('INSERT INTO chrono.chronicle_meta VALUES (?, ?)', meta)


def _write_sqlite_stdlib(
    con: duckdb.DuckDBPyConnection, path: Path, meta: _Meta
) -> None:
    """The floor: fetch each summary, write through stdlib sqlite3."""
    cx = sqlite3.connect(path)
    try:
        with cx:  # transaction: commits or rolls back as one
            for table, sql in _SUMMARIES:
                cur = con.execute(sql)
                cols = [d[0] for d in cur.description]
                types = [_sqlite_type(str(d[1])) for d in cur.description]
                rows = [tuple(r) for r in cur.fetchall()]
                decl = ", ".join(f'"{c}" {t}' for c, t in zip(cols, types, strict=True))
                marks = ", ".join("?" * len(cols))
                cx.execute(f'CREATE TABLE "{table}" ({decl})')
                cx.executemany(f'INSERT INTO "{table}" VALUES ({marks})', rows)
            cx.execute('CREATE TABLE "chronicle_meta" ("key" TEXT, "value" TEXT)')
            cx.executemany('INSERT INTO "chronicle_meta" VALUES (?, ?)', meta)
    finally:
        cx.close()  # finalized bytes before any digest reads the file


def _sqlite_type(duck_type: str) -> str:
    base = duck_type.split("(")[0].upper()
    return _SQLITE_TYPES.get(base, "TEXT")


def _resolve_write_mode(
    con: duckdb.DuckDBPyConnection, via: str
) -> str:
    """Probe + ladder (L12): attach when locally available, else stdlib."""
    if via == "stdlib":
        return "stdlib"
    available = _sqlite_scanner_available(con)
    if via == "attach" and not available:
        raise ChronicleError(
            "--sqlite-via attach: sqlite_scanner not locally available "
            "(autoinstall is off by design); use 'auto' or 'stdlib'"
        )
    return "attach" if available else "stdlib"


def run_chronicler(
    log: Path,
    out_dir: Path | None = None,
    *,
    min_events: int = 0,
    sqlite_via: str = "auto",
) -> dict[str, Any] | None:
    """Run the mode-F pipeline over one log; return the manifest dict.

    Returns None when the scale gate (min_events) suppresses the run.
    Raises ChronicleError on any integrity failure (nothing is written).
    """
    if sqlite_via not in SQLITE_VIA:
        raise ChronicleError(f"sqlite_via must be one of {SQLITE_VIA}")
    if not log.is_file():
        raise ChronicleError(f"{log}: no such log file")
    header = read_header(log)
    n_lines = count_lines(log)

    if n_lines - 1 < min_events:
        print(
            f"scale gate: {n_lines - 1} events < --min-events {min_events}; "
            f"the runtime sqlite index answers everything below threshold "
            f"(the ~100k guidance, docs/ref/duckdb.md)"
        )
        return None

    stem = log.name.rsplit(".", 1)[0]
    target = out_dir if out_dir is not None else REPO / "output" / "chronicle" / stem
    target.mkdir(parents=True, exist_ok=True)

    con = _connect()
    try:
        # -- intake: the file IS the table (the header line drops by id) ----
        columns = {
            c[0]
            for c in con.execute(
                f"DESCRIBE SELECT * FROM read_ndjson_auto('{log}', ignore_errors=true)"
            ).fetchall()
        }
        # Every event line carries `id` — its absence from the union schema
        # means no event line survived the intake (a header-only log, or all
        # lines dropped): the typed-NULL skeleton over zero rows.
        row_filter = "id IS NOT NULL" if "id" in columns else "false"
        projection = ", ".join(
            f'"{f}"' if f in columns else f'CAST(NULL AS {_FIELD_TYPES[f]}) AS "{f}"'
            for f in EVENT_FIELDS
        )
        con.execute(
            f"CREATE TEMP VIEW events AS SELECT {projection} FROM "
            f"read_ndjson_auto('{log}', ignore_errors=true) WHERE {row_filter}"
        )
        n_events = con.execute("SELECT count(*) FROM events").fetchone()[0]
        if n_events != n_lines - 1:
            raise ChronicleError(
                f"count gate: {n_lines - 1} log lines but {n_events} rows "
                f"served — events were silently dropped (integrity failure, "
                f"nothing written)"
            )

        # -- events.parquet: the canonical 12-column archive, ORDER BY id ---
        ordered = ", ".join(f'"{f}"' for f in EVENT_FIELDS)
        events_parquet = target / "events.parquet"
        con.execute(
            f"COPY (SELECT {ordered} FROM events ORDER BY id) "
            f"TO '{events_parquet}' (FORMAT PARQUET)"
        )

        # -- state_diffs.parquet: the LAG/LEAD window-diff law --------------
        con.execute(
            "CREATE TEMP VIEW state_events AS "
            "SELECT id AS event_id, t, actor, type, UNNEST(state_changes) AS sc "
            "FROM events WHERE len(state_changes) > 0"
        )
        n_diffs = con.execute("SELECT count(*) FROM state_events").fetchone()[0]
        diffs_parquet = target / "state_diffs.parquet"
        con.execute(
            f"""
            COPY (
                SELECT event_id, t, actor, type,
                       sc.entity AS entity, sc.prop AS prop,
                       CAST(sc['from'] AS VARCHAR) AS from_value,
                       CAST(sc.to AS VARCHAR) AS to_value,
                       sc.irreversible AS irreversible,
                       LAG(CAST(sc.to AS VARCHAR)) OVER (
                           PARTITION BY sc.entity, sc.prop ORDER BY t, event_id
                       ) AS prev_to,
                       CAST(sc['from'] AS VARCHAR) = LAG(CAST(sc.to AS VARCHAR)) OVER (
                           PARTITION BY sc.entity, sc.prop ORDER BY t, event_id
                       ) AS continuous
                FROM state_events
                ORDER BY sc.entity, sc.prop, t, event_id
            ) TO '{diffs_parquet}' (FORMAT PARQUET)
            """
        )

        # -- chronicle.sqlite: the write ladder ------------------------------
        sqlite_path = target / "chronicle.sqlite"
        if sqlite_path.exists():
            sqlite_path.unlink()
        # The meta row order is construction order in BOTH paths (the
        # degraded run rewrites the same list, never reorders it).
        base_meta: _Meta = [
            ("log", log.name),
            ("log_sha256", sha256_file(log)),
            ("n_events", str(n_events)),
            ("duckdb_version", str(duckdb.__version__)),
        ] + [(k, str(header[k])) for k in _HEADER_KEYS]
        mode = _resolve_write_mode(con, sqlite_via)
        meta = base_meta + [("write_mode", mode)]
        if mode == "attach":
            try:
                _write_sqlite_attach(con, sqlite_path, meta)
            except duckdb.Error:
                # The L12 degrade law: a failed attach rung falls to the
                # stdlib floor — the chronicler never breaks.
                mode = "stdlib"
                if sqlite_path.exists():
                    sqlite_path.unlink()
                meta = base_meta + [("write_mode", mode)]
                _write_sqlite_stdlib(con, sqlite_path, meta)
        else:
            _write_sqlite_stdlib(con, sqlite_path, meta)

        # -- manifest: content-derived, no wall-clock, no abs paths ----------
        manifest: dict[str, Any] = {
            "log": log.name,
            "log_sha256": sha256_file(log),
            "n_lines": n_lines,
            "n_events": int(n_events),
            **{k: header[k] for k in _HEADER_KEYS},
            "duckdb_version": str(duckdb.__version__),
            "write_mode": mode,
            "artifacts": {
                events_parquet.name: {
                    "rows": int(n_events),
                    "sha256": sha256_file(events_parquet),
                },
                diffs_parquet.name: {
                    "rows": int(n_diffs),
                    "sha256": sha256_file(diffs_parquet),
                },
                sqlite_path.name: {"sha256": sha256_file(sqlite_path)},
            },
        }
        (target / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        _report(manifest, target)
        return manifest
    finally:
        con.close()


def _report(manifest: dict[str, Any], target: Path) -> None:
    print(f"chronicle: {manifest['log']} ({manifest['n_events']} events)")
    for name, info in manifest["artifacts"].items():
        print(f"  {target / name}  rows={info.get('rows', '-')}  sha={info['sha256'][:16]}")
    print(f"  write_mode={manifest['write_mode']}  duckdb={manifest['duckdb_version']}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="chronicle",
        description="Mode F offline chronicler: DuckDB rollups + parquet archive "
        "+ summary sqlite over one JSONL run log (never in the runtime graph).",
    )
    parser.add_argument("log", type=Path, help="path to a run log (.jsonl)")
    parser.add_argument(
        "--out", type=Path, default=None,
        help="output directory (default: output/chronicle/<log_stem>/)",
    )
    parser.add_argument(
        "--min-events", type=int, default=0,
        help="scale gate: skip runs below this event count (the ~100k "
        "guidance, docs/ref/duckdb.md; default 0 = always run)",
    )
    parser.add_argument(
        "--sqlite-via", choices=SQLITE_VIA, default="auto",
        help="summary write path: auto (attach if locally available, else "
        "stdlib), attach, or stdlib",
    )
    args = parser.parse_args(argv)
    try:
        run_chronicler(args.log, args.out, min_events=args.min_events, sqlite_via=args.sqlite_via)
    except ChronicleError as exc:
        print(f"chronicle: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
