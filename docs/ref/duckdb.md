# DuckDB · `REFERENCES.md` §6 · MIT · phase 4 (offline analytics — NOT runtime; D-012)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is **MIT** (verified 2026-
> 08-26 from the repo `LICENSE` file: "Copyright 2018-2026
> Stichting DuckDB Foundation. Permission is hereby granted, free
> of charge, to any person obtaining a copy of this software … to
> deal in the Software without restriction, including without
> limitation the rights to use, copy, modify, merge, publish,
> distribute, sublicense, and/or sell copies …"). URL: <https://
> github.com/duckdb/duckdb/blob/main/LICENSE>. Catalog §6 row
> reads "DuckDB | MIT | analytics over the log, chronicle
> rebuilds (rev v2: offline 'chronicler' compression)"; index §2
> row had the matching MIT license — no drift this iteration.
> **Critical phase-0 intake rule:** DuckDB is a C++ runtime
> dependency — NOT in Python's stdlib; under D-012 it cannot be in
> the runtime path. The intake is "offline chronicler compression"
> — read JSONL → run SQL analytics → write parquet archive +
> summary SQLite (which IS stdlib). For phase-0 + phase-1, DuckDB
> is not needed at all — the JSONL log is small; the runtime
> SQLite projection is sufficient. DuckDB enters at phase-3+ when
> analytics over 100k+ events become a real workflow (D-022).
> Reference repo: `duckdb/duckdb` (active, C++17, vendor: Stichting
> DuckDB Foundation).

**What it is.** DuckDB is an in-process, columnar, vectorized
OLAP SQL database engine implemented as a C++17 library (no
server, no daemon) — the analytical analogue of SQLite, with
native Parquet/CSV/JSON readers and a morsel-driven parallel
execution engine. The store is the canonical shape for offline
analytics over the JSONL event log: read the log into a columnar
table for offline rollup queries ("per-NPC average suspicion
over time", "fire_spread event histogram"), archive the rolled-up
chronicle to parquet for long-term storage, and pass the summary
back into the runtime SQLite index. The *pattern* (columnar
rollups, no-ETL ingestion, Appender bulk-load, window functions
for state deltas) is what we lift — D-012 — not the C++ runtime.

**Concrete mechanics.**

- **`DuckDB` class** (`src/include/duckdb/main/database.hpp:131`)
  — the database handle; constructor `DuckDB(const char *path =
  nullptr, DBConfig *config = nullptr)`. Passing `nullptr` =
  **in-memory** mode; passing a path = **persistent** mode. Owns
  a `shared_ptr<DatabaseInstance> instance` that aggregates
  `BufferManager`, `DatabaseManager`, `TaskScheduler`,
  `ObjectCache`, `ExtensionManager`, `LogManager`. Static
  helpers: `DuckDB::LibraryVersion()`, `DuckDB::StandardVector-
  Size()`, `DuckDB::Platform()`. The pattern: **one handle owns
  one instance; in-memory or persistent chosen at construction**.
  Lifted as the chronicler entry-point shape — `chronicler =
  duckdb.connect()` for in-memory or `duckdb.connect('chronicle.
  duckdb')` for persistent; the chronicler is a separate process
  (a `scripts/chronicle.py` outside the runtime module graph).
- **`Connection` class** (`src/include/duckdb/main/connection.
  hpp:55`) — the per-client query surface over a `DuckDB`
  instance. Real methods: `Query(const string &)` → returns
  `unique_ptr<MaterializedQueryResult>`; `SendQuery(...)`
  returns a streamable `QueryResult`; `Prepare(...)` →
  `PreparedStatement`; `PendingQuery(...)` for async/
  interruptible execution; `Interrupt()` / `GetQueryProgress
  ()`; relation builders `Table(...)`, `ReadCSV(...)`,
  `ReadParquet(...)`, `TableFunction(...)`. `EnableProfiling
  ()` / `DisableProfiling()` toggle the query profiler; the
  deprecated `EnableQueryVerification()` is a no-op (replaced
  by individual verification routines). The pattern: **one
  connection per client; query via SQL string or prepared
  statement**. Lifted into the chronicler — `con = duckdb.
  connect(); con.execute("SELECT * FROM read_ndjson_auto
  ('log/events.jsonl')")`.
- **Vectorized execution — `STANDARD_VECTOR_SIZE`** (`src/
  include/duckdb/common/vector_size.hpp:16`): `#define
  DEFAULT_STANDARD_VECTOR_SIZE 2048U` — every operator pushes
  data through `DataChunk`s of **2048 rows at a time** (`vector
  <Vector> data` in `DataChunk`, `src/include/duckdb/common/
  types/data_chunk.hpp:44`). Must be a power of two (compile-time
  `#error` check). `DataChunk::Initialize(Allocator&, const
  vector<LogicalType>&, idx_t capacity = STANDARD_VECTOR_SIZE)`
  is the constructor path. This 2048-row chunk is the unit the
  `PipelineExecutor` (`src/parallel/pipeline_executor.cpp:828
  GetData`) pulls through the operator tree — **morsel-driven
  parallelism without using the word "morsel"** (no `Morsel`
  symbol exists in src/; the chunk is the morsel). The pattern:
  **vectorized execution — operators pull `DataChunk`s of 2048
  rows at a time through the operator tree; morsel-driven
  parallelism parallelizes per-chunk**. Lifted as the lesson —
  columnar layout makes "scan all `suspicion` values across 1M
  events" a single sequential pass; SQLite's row-store page
  model makes the same query a full-table scan touching every
  column.
- **`PhysicalOperator` family** (`src/include/duckdb/execution/
  physical_operator.hpp:44`) — base class for the physical
  execution plan; subclasses keyed by `enum class Physical-
  OperatorType` (`src/include/duckdb/common/enums/physical_
  operator_type.hpp:18`). Real members: `FILTER` (32),
  `PROJECTION` (33), `HASH_GROUP_BY` (28), `PERFECT_HASH_GROUP_
  BY` (29), `PARTITIONED_AGGREGATE` (30), `WINDOW` (25),
  `HASH_JOIN` (60), `NESTED_LOOP_JOIN` (59), `CROSS_PRODUCT`
  (61), `PIECEWISE_MERGE_JOIN` (62), `ASOF_JOIN` (67), `TOP_N`
  (24), `ORDER_BY` (20), `TABLE_SCAN` (45), `INSERT` (79),
  `BATCH_INSERT` (80), `COPY_TO_FILE` (34), `BATCH_COPY_TO_
  FILE` (35), `ATTACH`, `DETACH`, `CREATE_SEQUENCE`,
  `EXPLAIN_ANALYZE`. Each operator implements `Execute(...)` /
  `GetData(...)` / `Sink(...)` returning `OperatorResultType`
  / `SourceResultType` / `SinkResultType`. The pattern: **a
  closed family of physical operators keyed by enum, each
  implementing `Execute`/`GetData`/`Sink`** — same family shape
  as `libtcod`/`rot.js`/`entt`/`bevy` operator families; closed
  enum at config time.
- **`read_json_auto()` table-valued function** (`extension/
  json/json_functions/read_json.cpp:384`) — `JSONFunctions::
  GetReadJSONAutoFunction()` creates a `TableFunctionSet` named
  `"read_json_auto"` from a `JSONScanInfo{READ_JSON,
  AUTO_DETECT, AUTO_DETECT, true}`. Sibling functions:
  `"read_json"`, `"read_ndjson"`, `"read_ndjson_auto"`,
  `"read_json_objects"`, `"read_ndjson_objects"`,
  `"read_json_objects_auto"` (all in the same file +
  `read_json_objects.cpp`). The `auto` variant **auto-detects
  schema** from the JSON; NDJSON mode reads newline-delimited
  JSON — the canonical JSONL ingestion path. The pattern:
  **point at the JSONL log file and start querying; no schema,
  no COPY-then-CAST pipeline**. Lifted into the chronicler —
  `SELECT * FROM read_ndjson_auto('log/events.jsonl')` is the
  entire intake step. The *pattern* — that the log file is
  directly queryable as a table — is the inheritance.
- **`COPY TO` parquet via `CopyFunction("parquet")`**
  (`extension/parquet/parquet_extension.cpp:1040`) — parquet
  is registered as a `CopyFunction` named `"parquet"` with
  `copy_to_sink = ParquetWriteSink`, `copy_to_finalize =
  ParquetWriteFinalize`, `execution_mode = ParquetWrite-
  ExecutionMode` (returns `PARALLEL_COPY_TO_FILE` /
  `BATCH_COPY_TO_FILE` / `REGULAR_COPY_TO_FILE` based on
  `preserve_insertion_order` and `supports_batch_index`). The
  same function object carries `copy_from_function` (the
  parquet reader) so `COPY FROM 'x.parquet'` and `COPY (SELECT…)
  TO 'x.parquet'` are both first-class. SQL example: `COPY
  (SELECT actor_id, tick, suspicion FROM events) TO 'archive.
  parquet' (FORMAT PARQUET);`. The pattern: **the canonical
  "archive a rolled-up chronicle to long-term columnar storage"
  pattern** — canonsim's chronicler emits its compressed rollup
  as parquet via this exact mechanism (the parquet extension's
  `copy_to_sink` / `copy_to_finalize` and `BATCH_COPY_TO_FILE`
  execution mode). The *output* of phase-3+ chronicler is
  parquet.
- **`Appender` API** (`src/include/duckdb/main/appender.hpp:30`)
  — high-throughput bulk-insert path bypassing per-row SQL
  parsing. Concrete API: `BaseAppender::BeginRow()` /
  `EndRow()` / template `Append<T>(value)` with explicit
  instantiations for `bool, int8_t … uint64_t, float, double,
  date_t, timestamp_t, string_t, Value, nullptr_t` (lines
  220–261). `Flush()` commits; `Close()` flushes + invalidates.
  Flushes the internal `ColumnDataCollection` every
  `DEFAULT_FLUSH_COUNT = STANDARD_VECTOR_SIZE * 100` (= 204,800
  rows). Three concrete classes: `Appender` (for a real table),
  `QueryAppender` (inserts via a custom query),
  `InternalAppender` (internal system tables). The pattern:
  **the canonical "bulk-load events into DuckDB with maximum
  throughput, bypassing per-row SQL parsing" pattern**. canonsim's
  chronicler, when reading the JSONL log becomes too slow, falls
  back to streaming events through an `Appender` instead of
  `read_json_auto()`. The *batched-row* API shape is the
  inheritance.
- **Composite column types** (`src/include/duckdb/common/
  types.hpp:193` `enum class LogicalTypeId : uint8_t`):
  `STRUCT = 100`, `LIST = 101`, `MAP = 102`, `UNION = 107`,
  `ARRAY = 108`, `TUPLE = 110`. Constructors on `LogicalType`:
  `LogicalType::STRUCT(child_list_t<LogicalType>)`,
  `LogicalType::LIST(const LogicalType &child)`,
  `LogicalType::ARRAY(const LogicalType &child, optional_idx
  index)` (line 456), `LogicalType::MAP(...)`. Storage mirrors
  these as `StructColumnData`, `ListColumnData`,
  `ArrayColumnData` (`src/include/duckdb/storage/table/`). SQL
  surface: `STRUCT(name VARCHAR, value INTEGER)`,
  `LIST(INTEGER)[1,2,3]`, `INTEGER[4]` (fixed-size ARRAY). The
  pattern: **composite column types for nested JSON data** —
  the JSONL event log's nested `data` and `metadata` objects
  map directly to `STRUCT(...)` columns in DuckDB. Lifted as
  the auto-detection contract — `read_json_auto()` infers
  these for us.
- **Window functions** (`src/include/duckdb/common/enums/
  expression_type.hpp:94`): `WINDOW_RANK = 120`,
  `WINDOW_RANK_DENSE = 121`, `WINDOW_NTILE = 122`,
  `WINDOW_PERCENT_RANK = 123`, `WINDOW_ROW_NUMBER = 125`,
  `WINDOW_FIRST_VALUE = 130`, `WINDOW_LAST_VALUE = 131`,
  `WINDOW_LEAD = 132`, `WINDOW_LAG = 133`. Bound in
  `BoundWindowExpression` (`src/include/duckdb/planner/
  expression/bound_window_expression.hpp:21`) with
  `WindowBoundary start` / `WindowBoundary end` (RANGE vs ROWS,
  UNBOUNDED PRECEDING etc.) and `PartitionsAreEquivalent(...)`
  for partition equivalence. Operators: `PhysicalOperatorType::
  WINDOW` (25), `STREAMING_WINDOW` (38). The pattern: **window
  functions (`LAG`/`LEAD` over `tick` partitioned by
  `actor_id`) are the canonical "diff consecutive per-actor
  state" pattern for analytics over the event log** — canonsim's
  chronicler uses this shape (lifted, not copied) to derive
  per-actor state deltas: `LAG(suspicion) OVER (PARTITION BY
  actor_id ORDER BY tick)`.
- **Extension mechanism (`INSTALL` / `LOAD` /
  `AutoLoadExtension`)** (`src/include/duckdb/main/
  extension_helper.hpp:100`): `ExtensionHelper::
  InstallExtension(ClientContext&, extension, options)`,
  `LoadExternalExtension(...)`, `AutoLoadExtension(...)`,
  `TryAutoLoadExtension(...)`, `LoadAllExtensions(DuckDB&)`.
  Built-in core extensions live under `extension/` —
  **`parquet`**, **`json`**, **`icu`** (timezone/collation),
  **`core_functions`**, **`autocomplete`**, **`tpcds`**, plus
  `demo_capi`. SQL: `INSTALL json; LOAD json;`. Extensions can
  be statically linked via `DuckDB::LoadStaticExtension<T>()`
  or `LoadStaticCAPIExtension(name, init_fun)`. Physical
  operator `LOAD` (`PhysicalOperatorType::LOAD`) is the runtime
  form. The pattern: **extensions are loadable plugins; the core
  ships with `parquet` and `json` baked in (relevant for
  canonsim's chronicler — no separate `INSTALL json` needed
  in recent DuckDB)**. Lifted as a negative: extensions fetch
  from DuckDB's extension repository by default
  (`ExtensionHelper::InstallExtension`,
  `ExtensionUrlTemplate`); in an air-gapped or stdlib-purist
  context this is a network dependency — canonsim's chronicler
  must either bundle the extension binaries or rely on auto-
  loaded core extensions.
- **`ATTACH` external databases + `CREATE SEQUENCE`** —
  `PhysicalAttach` (`src/include/duckdb/execution/operator/
  schema/physical_attach.hpp:17`, `PhysicalOperatorType::ATTACH`)
  wires `AttachInfo` (`src/include/duckdb/parser/parsed_data/
  attach_info.hpp:22`) so a second database file (or Postgres/
  SQLite via extensions) can be queried read-only as `att_db.
  tablename`. `CreateSequenceInfo` (`src/include/duckdb/parser/
  parsed_data/create_sequence_info.hpp:32`) +
  `PhysicalCreateSequence` give ANSI `CREATE SEQUENCE` for
  auto-increment keys. The pattern: **a second SQLite file can
  be `ATTACH`-ed and queried alongside the DuckDB instance** —
  the chronicler can `ATTACH 'chronicle.sqlite'` and write the
  summary back into the runtime SQLite index. Lifted as the
  chronicler output path: `ATTACH 'chronicle.sqlite'; INSERT
  INTO chronicle.sqlite.facts_summary SELECT … FROM read_
  ndjson_auto('log/events.jsonl') GROUP BY actor_id;`.
- **`PRAGMA` system + `EXPLAIN`** (`src/function/pragma/
  pragma_functions.cpp:107`): real pragma names registered here
  — `enable_verification` (now deprecated/no-op per the
  comment on line 57 — "PRAGMA enable_verification has been
  deprecated - there is no need to set this anymore"),
  `enable_profiling` / `disable_profiling`,
  `enable_progress_bar` / `disable_progress_bar`,
  `enable_object_cache`, `enable_optimizer` /
  `disable_optimizer`, `force_checkpoint`, `verify_parallelism`
  (force-parallel for testing). The `EXPLAIN` operator is
  `LogicalExplain` (`LOGICAL_EXPLAIN`) and the runtime analyzer
  is `PhysicalExplainAnalyze` (`PhysicalOperatorType::EXPLAIN_
  ANALYZE`) producing a plan tree via `ProfilerPrintFormat`.
  The pattern: **`PRAGMA` + `EXPLAIN` are the diagnostic
  surface**. Lifted as the diagnostic surface for the chronicler
  — `EXPLAIN` shows the plan tree before running expensive
  rollups; `PRAGMA enable_progress_bar` shows progress on multi-
  minute analytics.
- **Columnar storage + compression** (`src/include/duckdb/
  storage/compression/`) — pluggable per-column compression
  algorithms with concrete implementations: `Bitpacking`,
  `Dictionary`, `FSST` (`dict_fsst/`), `ALP` / `ALPRD`,
  `Chimp128`, `Patas`, `Roaring`, `Zstd`. Each has parallel
  `analyze` / `compression` / `decompression` / `scan` /
  `fetch` modules — the canonical "compress once, scan many"
  shape that makes columnar rollups cheap. The pattern:
  **per-column pluggable compression — compress once, scan
  many**. Lifted as the lesson: columnar layout + per-column
  compression makes "scan all `suspicion` values across 1M
  events" a single sequential pass.

**What we take.**

- The columnar OLAP shape as the canonical "offline analytics
  over the log" pattern — DuckDB's `DataChunk` (vector of
  column-vectors, `STANDARD_VECTOR_SIZE = 2048`) + columnar
  `storage/table/` is the shape for "roll up the entire JSONL
  event log in one pass." Under D-022 (phase-3+ scale),
  canonsim's **`chronicler` offline pipeline** borrows this
  shape: read the JSONL log → build a columnar table → run
  aggregate SQL ("per-NPC average suspicion over time",
  "fire_spread event histogram by tick") → emit summary to
  SQLite. The *pattern*, not the code — D-012.
- The `read_json_auto()` / `read_ndjson_auto()` table-valued
  functions (`extension/json/json_functions/read_json.cpp:384,
  388`) as the canonical "no-ETL ingestion" pattern — point the
  table function at the JSONL log file and start querying; no
  schema, no COPY-then-CAST pipeline. canonsim's `chronicler`
  lifts this exact pattern: `SELECT * FROM read_ndjson_auto
  ('log/events.jsonl')` is the entire intake step. The
  *pattern* — that the log file is directly queryable as a
  table — is the inheritance.
- The `COPY TO … (FORMAT PARQUET)` via `CopyFunction("parquet")`
  (`extension/parquet/parquet_extension.cpp:1040`) as the
  canonical "archive a rolled-up chronicle to long-term columnar
  storage" pattern. canonsim's chronicler emits its compressed
  rollup as parquet via this exact mechanism (the parquet
  extension's `copy_to_sink` / `copy_to_finalize` and
  `BATCH_COPY_TO_FILE` execution mode). The *output* of phase-3+
  chronicler is parquet.
- The `Appender` API (`BeginRow`/`EndRow`/`Append<T>`, flush
  every `STANDARD_VECTOR_SIZE * 100` = 204,800 rows)
  (`src/include/duckdb/main/appender.hpp:30`) as the canonical
  "bulk-load events into DuckDB with maximum throughput,
  bypassing per-row SQL parsing" pattern. canonsim's chronicler,
  when reading the JSONL log becomes too slow, falls back to
  streaming events through an `Appender` instead of `read_json_
  auto()`. The *batched-row* API shape is the inheritance.
- The window functions `LAG` / `LEAD` over `tick` partitioned by
  `actor_id` (`WINDOW_LAG = 133`, `WINDOW_LEAD = 132`,
  `BoundWindowExpression`) as the canonical "diff consecutive
  per-actor state" pattern for analytics over the event log.
  canonsim's chronicler uses this shape (lifted, not copied) to
  derive per-actor state deltas: `LAG(suspicion) OVER
  (PARTITION BY actor_id ORDER BY tick)`.
- The `ATTACH` external-database + `CREATE SEQUENCE` pattern
  (`PhysicalOperatorType::ATTACH`, `AttachInfo`) — the chronicler
  can `ATTACH 'chronicle.sqlite'` and write the summary back into
  the runtime SQLite index.

**What we adapt.**

- DuckDB is a C++ runtime dependency → NOT in the canonsim
  runtime path (D-012). Python's stdlib ships `sqlite3`; it
  does NOT ship DuckDB. The canonsim runtime — phase 0 (one
  tavern scenario), phase 1, phase 2 — uses only `sqlite3`
  (the rebuildable index per INV-1) and the JSONL log fold.
  DuckDB cannot be in `import` paths that load during
  simulation. **Adaptation:** the chronicler is an *offline /
  batch / dev-time* tool invoked from a separate `scripts/
  chronicle.py` outside the runtime module graph. The runtime
  never imports `duckdb`.
- The chronicler's intake is "offline compression": JSONL →
  DuckDB (analytical) → parquet archive + summary SQLite
  (runtime-readable). The summary SQLite is the part that flows
  back into the runtime as a fast lookup index; the parquet is
  the cold archive; the DuckDB instance is closed and discarded
  after the rollup. The adaptation: DuckDB is a *build step*
  producing stdlib-compatible artifacts — not a peer of the
  JSONL log or the SQLite index.
- DuckDB enters at phase-3+ (D-022), not phase 0/1. Phase 0
  log is small (<1000 events); the runtime SQLite projection
  suffices for any query canonsim needs at that scale. DuckDB's
  analytical advantage (vectorized scan over millions of rows)
  is wasted below ~100k events. The adaptation is the *scale
  gate*: canonsim keeps a `chronicler` entry point that is a
  no-op until the log crosses a configurable size threshold
  (e.g. 100k events), at which point the offline pipeline
  activates. Below the threshold, the runtime `sqlite3` index
  answers everything.

**What inspires us.**

- The columnar layout is the canonical shape for event-log
  analytics; row-store SQLite is the wrong shape for full-log
  rollups. DuckDB's `DataChunk` (vector of column-vectors) +
  per-column compression (`Bitpacking`/`Dictionary`/`FSST`/`ALP`/
  `Chimp`) makes "scan all `suspicion` values across 1M events"
  a single sequential pass; SQLite's row-store page model makes
  the same query a full-table scan touching every column. The
  lesson: **runtime index = row-store SQLite for point lookups;
  offline analytics = columnar DuckDB for rollups** — and the
  boundary between them is the chronicler.
- "Point at the file and start querying" (`read_json_auto`,
  `SELECT * FROM 'f.parquet'`) is the canonical "no-ETL"
  ingestion pattern — the file *is* the table. This shapes
  canonsim's JSONL log: the log is already queryable without a
  rebuild step, which means the chronicler is *optional*, never
  *required*, for any analytics workflow. The log is truth; the
  chronicler is convenience.

**Strengths.**

- In-process — no server to run. `DuckDB(nullptr)` opens an
  in-memory DB; `DuckDB("file.db")` opens a persistent one. No
  daemon, no port, no service account. The chronicler script can
  `import duckdb; con = duckdb.connect()` and be done.
- Native readers for parquet / csv / json (`read_json_auto`,
  `read_ndjson_auto`, `read_csv_auto`, `read_parquet`).
  canonsim's JSONL log is queryable in one line — `SELECT * FROM
  read_ndjson_auto('log/events.jsonl')` — with no COPY, no schema
  declaration, no ETL.
- Vectorized execution makes full-log rollups ~100× faster than
  SQLite for analytical workloads. `STANDARD_VECTOR_SIZE = 2048`
  chunked `DataChunk`s through `PhysicalOperator::Execute(...)`
  + morsel-driven `PipelineExecutor` parallelism — columnar scan
  + per-column compression (`Bitpacking`/`ALP`/`Chimp`) means a
  1M-event rollup is a handful of sequential column scans, not
  a million row touches.
- MIT license — zero license friction. Compatible with canonsim's
  stdlib-only runtime stance for *offline* use; the chronicler
  tool can `pip install duckdb` without legal review.
- The `Appender` API gives maximum-throughput bulk insert
  (`BeginRow`/`EndRow`/`Append<T>`, flush every 204,800 rows) when
  `read_json_auto` is too slow for very large logs — the
  chronicler's fallback path.
- Window functions (`LAG`/`LEAD`/`RANK`/`ROW_NUMBER` with
  `PARTITION BY` / `ORDER BY`) are first-class
  (`BoundWindowExpression`, `WINDOW_LAG = 133`) — the canonical
  "diff consecutive per-actor state" pattern is a single SQL
  clause, not a Python loop.

**Weaknesses.**

- C++ runtime dependency — not stdlib; under D-012 cannot be in
  the runtime path. `import duckdb` pulls in a multi-MB native
  extension; the canonsim runtime must stay `python -X stdlib-
  only`. DuckDB is therefore confined to the offline `scripts/`
  graph, never `src/canonsim/`.
- Phase 0 log is small (<1000 events); DuckDB's analytical
  advantage is wasted at small scale. Below ~100k events,
  SQLite's `sqlite3` answers every canonsim query in
  milliseconds; DuckDB's startup cost + extension autoload
  cost + larger binary dwarfs the query time. SQLite wins on
  simplicity at phase-0/1.
- Single-writer, not designed for live ingestion during
  simulation. DuckDB's storage model is OLAP: bulk-load then
  scan; concurrent live appends compete with the SQLite runtime
  index for the write lock and would violate canonsim's "JSONL
  is the only write path" invariant (INV-1). The chronicler must
  run *after* a tick batch is sealed, not during.
- Another tool in the chain — only justified when log scale +
  analytical queries pay the operational cost. Adding DuckDB
  means a second binary to install, a second file format
  (parquet) to document, a second failure mode. At phase-0/1/2
  the JSONL + SQLite pair covers everything; DuckDB only earns
  its keep at phase-3+ when "average suspicion per NPC over the
  last 1M ticks" becomes a real workflow (D-022).
- Extensions (`json`, `parquet`) are required for the no-ETL
  ingestion pattern — and `INSTALL`/`LOAD` fetches from DuckDB's
  extension repository by default
  (`ExtensionHelper::InstallExtension`, `ExtensionUrlTemplate`).
  In an air-gapped or stdlib-purist context this is a network
  dependency; canonsim's chronicler must either bundle the
  extension binaries or rely on auto-loaded core extensions
  (`parquet`/`json` are core in recent DuckDB).

**Verdict.** Phase-4 OFFLINE analytics reference (NOT runtime;
D-012) — the chronicler's analytical backend at phase-3+ scale
(≥100k events), used to roll the JSONL log up into columnar
queries and parquet archives. It is **never** in the runtime path
(D-012: stdlib-only runtime; DuckDB is a C++ runtime dep). The
runtime keeps SQLite as the rebuildable index (INV-1); DuckDB
enters only when the log scale + analytical workload justify the
operational cost, and exits by emitting parquet (cold archive) +
summary SQLite (back into the runtime). Pattern-lifted (D-015),
not vendored. MIT license (verified 2026-08-26 from the repo
`LICENSE` file header "Copyright 2018-2026 Stichting DuckDB
Foundation") — zero friction at intake. The "columnar layout is
the canonical shape for event-log analytics; row-store SQLite is
the wrong shape for full-log rollups" lesson is the inspiration:
runtime index = row-store SQLite for point lookups; offline
analytics = columnar DuckDB for rollups; the boundary between
them is the chronicler.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
