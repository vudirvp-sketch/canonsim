# sqlite-vec · `REFERENCES.md` §6 + §14 · MIT OR Apache-2.0 (dual) · phase 4 (retrieval candidates — local-first vector index)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is **dual-licensed: `MIT OR
> Apache-2.0`** (catalog said "verify" — verified 2026-08-26 from
> the repo `LICENSE-MIT` file header: "Copyright (c) 2024 Alex
> Garcia" + `LICENSE-APACHE` file present; the `sqlite-dist.toml`
> manifest declares `license = "MIT OR Apache-2.0"`). Since MIT is
> one of the two offered licenses, canonsim may take it under plain
> MIT terms (no patent retaliation clause to worry about for a
> stdlib simulation project). Catalog §6 row read "sqlite-vec
> (asg017) | verify | vector search inside SQLite for static-lore
> RAG (phase 4; §14)" — `verify` status now resolved to "MIT OR
> Apache-2.0 (dual)"; index §2 row had "MIT" — standing pre-flip
> check (KI#6-class pitfall) caught the dual-vs-MIT drift in the
> same §2 edit that flips ref-11-c todo→done with the corrected
> "MIT OR Apache-2.0 (dual)" annotation. **Critical phase-0 intake
> rule:** sqlite-vec is a C `.so`/`.dll`/`.dylib` loadable
> extension — **does NOT ship with Python's stdlib `sqlite3` module**
> (macOS system Python even lacks `enable_load_extension` entirely).
> Phase 0 cannot rely on it; phase 4 treats it as opt-in: the
> retriever probes `db.enable_load_extension(True)` + `sqlite_vec.
> load(db)` inside a `try/except`; if unavailable, it silently
> degrades to pure-Python brute-force `cosine_sim()` over the same
> embeddings cached in SQLite. Reference repo: `asg017/sqlite-vec`
> (pre-v1, breaking changes expected per the README IMPORTANT
> banner).

**What it is.** `sqlite-vec` is a single-file, dependency-free
**loadable SQLite extension written in pure C** that adds a
`vec0` virtual-table module plus a suite of SQL scalar functions
for storing, querying, and compressing `float32` / `int8` / `bit`
vectors inside an ordinary SQLite database — i.e. "FTS5, but for
embeddings." The extension is the canonical local-first vector
index — no qdrant server, no lancedb extra dep, just a SQLite
loadable extension. For phase 4 retrieval, sqlite-vec is the
canonical local-first vector store; the `vec0` shape (`CREATE
VIRTUAL TABLE … MATCH … ORDER BY distance LIMIT k`) mirrors FTS5
(`docs/ref/sqlite_fts5.md`) — same ergonomics for keyword and
vector search, both in the same SQLite database file.

**Concrete mechanics.**

All names below are pulled from `sqlite-vec.c` (registration block
at lines 10660–10711) and the API docs. SQLite function names are
case-insensitive, but the canonical casing the source registers
is given.

- **`vec0` virtual-table module** — registered at `sqlite-vec.c:
  10688` as `{"vec0", &vec0Module, NULL, NULL}` via
  `sqlite3_create_module_v2`. The DDL shape is `CREATE VIRTUAL
  TABLE <name> USING vec0(<col> <type>[N] [pk] [partition key]
  [distance_metric=L2|cosine], <other_col> <type>[M], +<aux_col>
  <type>, ...)`. Real example from the README: `create virtual
  table vec_examples using vec0(sample_embedding float[8]);`.
  Lifted into the canonical "vector index over facts" pattern
  for `core/storage.py` — `CREATE VIRTUAL TABLE lore_vec USING
  vec0(embedding float[D], +fact_text text, scenario_id integer
  partition key)` gives canonsim's phase-4 retrieval layer the
  same ergonomics as its FTS5 keyword index: `WHERE embedding
  MATCH :q ORDER BY distance LIMIT k`. The auxiliary `+fact_text`
  column means retrieval returns the fact payload with no JOIN —
  same single-table pattern as the `events` JSONL fold. The
  `scenario_id integer partition key` column maps cleanly onto
  canonsim's phase-0 tavern scope (one partition per scenario;
  pre-filters kNN to in-scope facts).
- **`rowid` PK + MATCH kNN query** — every `vec0` table has an
  implicit `rowid`. The kNN pattern (from `site/features/knn.md`):
  `select rowid, distance from vec_examples where
  sample_embedding match '[0.89, 0.54, ...]' order by distance
  limit 2;`. The `k` constraint (`and k = 10`) is the pre-3.41
  form; `LIMIT k` works on SQLite ≥ 3.41. The C source validates
  this at `sqlite-vec.c:6101`: "A LIMIT or 'k = ?' constraint
  is required on vec0 knn queries." The `k` value is consumed as
  a hidden column at `sqlite-vec.c:7701` (`i64 k =
  sqlite3_value_int64(argv[k_idx]);`). The pattern: **the
  canonical kNN-over-vectors SQL idiom — `WHERE <col> MATCH
  :query_vec ORDER BY distance LIMIT k`** — same shape as FTS5's
  `WHERE <col> MATCH :query ORDER BY rank`. Lifted into the
  retrieval query DSL alongside FTS5.
- **`vec_distance_cosine(a, b)`** — registered at `sqlite-vec.c:
  10665` (`{"vec_distance_cosine", vec_distance_cosine, 2, ...}`);
  the C impl is `static void vec_distance_cosine(...)` at line
  1423. Computes cosine *distance* (not similarity; `1 - cos`)
  between two float32 or int8 vectors. **Note:** the canonical
  SQL name is `vec_distance_cosine`, **not** `vec_distance_cos`.
  Lifted as the canonical similarity metric — for static-lore
  RAG. Cosine is the right default for normalized embedding
  models; sqlite-vec defaults to L2 but exposes `distance_metric=
  cosine` as a per-column DDL knob (parsed at `sqlite-vec.c:
  3066`, stored on `VectorColumnDefinition.distance_metric` at
  line 2688).
- **`vec_distance_L2(a, b)` / `vec_distance_L1(a, b)` /
  `vec_distance_hamming(a, b)`** — registered at lines 10662–
  10664 (`vec_distance_l2`, `vec_distance_l1`,
  `vec_distance_hamming`). L2 = Euclidean (float32/int8);
  Hamming = bit-vectors only. The `vec0` default distance
  metric is L2; cosine is opt-in per-column via `distance_metric
  =cosine` in the DDL. Lifted as the distance-metric choice rule
  — cosine for normalized embeddings (the canonsim default); L2
  for non-normalized; Hamming for binary-quantized vectors.
- **`vec_f32(v)` / `vec_int8(v)` / `vec_bit(v)` constructors**
  — registered at lines 10673–10675; return a BLOB with a
  `sqlite3_result_subtype` of `223` (float32), `225` (int8), or
  `224` (bit) — see `#define SQLITE_VEC_ELEMENT_TYPE_FLOAT32 =
  223 + 0` etc. at lines 78–80. This **subtype byte** is how
  sqlite-vec tags vector type on an otherwise-undifferentiated
  BLOB. `vec_f32('[.1,.2,.3,4]') → X'CDCCCC3D...'`. The pattern:
  **vectors over the wire are just `struct.pack`-ed `float32`
  BLOBs** — `bindings/python/extra_init.py` ships a 4-line
  pure-Python `struct.pack("%sf" % len(v), *v)` serializer. This
  is the exact pattern canonsim's fallback needs: vectors are
  just `struct.pack`-ed `float32` BLOBs, no extension required
  to *produce* them.
- **`vec_to_json(v)` (and the inverse JSON-array parsing)** —
  registered at line 10668; `static void vec_to_json(...)` at
  line 1965. Renders a vector BLOB as a JSON array string; the
  constructors accept JSON input the other way. JSON input is
  tagged with `#define JSON_SUBTYPE 74` (line 865). So
  `vec_to_json(vec_int8(X'AABBCCDD')) → '[-86,-69,-52,-35]'`.
  Lifted as the vector-serialization contract — vectors go over
  the wire as JSON arrays; the BLOB form is for storage + compute.
- **`vec_quantize_binary(v)` / `vec_quantize_int8(v, 'unit')`**
  — registered at lines 10676–10677. `vec_quantize_binary` (line
  1618) reduces each float element to a single bit (1 = positive,
  0 = negative), packing 8 dims per byte → **32× storage
  reduction** for float32. Used to build a coarse index that's
  re-scored against full vectors (`site/guides/binary-quant.md`
  shows the two-pass `coarse_matches` CTE pattern with
  `vec_distance_L2` rescore). *(The scalar-quant doc shows a
  future overloaded `vec_quantize('float16'|'int8'|'bit', v)`
  form, but it is **not** registered in the current `0.1.10-
  alpha.4` C source — only `vec_quantize_binary` and
  `vec_quantize_int8` exist today.)* Lifted as the compression
  fallback before reaching for an ANN index: build a coarse
  `bit[D]` column alongside the `float[D]` column, kNN-filter
  on the bit index at high k, then re-rank the survivors with
  `vec_distance_L2`. This is the canonsim "scale-up without
  adding a server" ladder rung.
- **`vec_slice(v, start, end)` + `vec_normalize(v)`** — the
  **matryoshka embeddings** primitives. `vec_slice` (line 1849,
  registered line 10671) extracts dims `[start, end)` from a
  vector; `vec_normalize` (line 2015, registered line 10672)
  L2-normalizes a float32 vector. The matryoshka pattern (from
  `site/guides/matryoshka.md`): `select vec_normalize(vec_slice
  (title_embeddings, 0, 256)) as title_embeddings_256d from
  vec_articles;`. Train at 1024-d, store/query at 256-d → ~4×
  index shrink with minimal quality loss on matryoshka-trained
  models (`mxbai-embed-large-v1`, `nomic-embed-text-v1.5`,
  `text-embedding-3-large`). Lifted as the matryoshka pattern
  — train embeddings at high dim (e.g. 1024), store at 256 →
  ~4× smaller lore index for the tavern scenario's static-fact
  corpus, with minimal recall loss. This is the compression
  strategy canonsim adopts *if/when* the fact store grows past
  the brute-force-comfortable threshold.
- **`vec0` shadow tables** — declared on the `vec0_vtab` struct
  (`sqlite-vec.c:3528–3576`): `_rowids` (`shadowRowidsName`),
  `_chunks` (`shadowChunksName`), per-vector `_vector_chunks00`
  (`shadowVectorChunksNames`), per-vector `_rescore_chunks00` /
  `_rescore_vectors00`, and per-metadata `_metadatachunks00`.
  The vec0 module also supports **partition-key columns**
  (`Vec0PartitionColumnDefinition`, struct at line 2697 —
  internally shards the index) and **auxiliary columns**
  (`+`-prefixed, `Vec0AuxiliaryColumnDefinition` at line 2703 —
  stored in a separate table, not in kNN `WHERE`, no JOIN needed
  for SELECT). Max 16 metadata + 16 auxiliary + 4 partition
  keys. The pattern: **shadow-table separation as an architectural
  metaphor, not a literal copy** — sqlite-vec keeps vector
  payloads in `_chunks`/`_vector_chunks00` shadow tables separate
  from the `_rowids` PK table so the heavy BLOBs don't bloat the
  rowid index. canonsim adapts this by storing event-log-derived
  fact embeddings in a **separate `fact_embeddings(fact_id,
  embedding BLOB)` table** alongside the main `facts` table —
  same separation-of-PK-from-payload discipline, expressed as
  ordinary (non-virtual) SQLite tables so it works without the
  extension loaded.
- **`vec_each(v)` table function** — registered at line 10689
  (`{"vec_each", &vec_eachModule, ...}`) via the `sqlite3_module
  vec_eachModule` struct at line 3365. Returns one row per
  vector element (`rowid`, `value`) — useful for inspection and
  arithmetic joins. Mirrors FTS5's `fts5vocab` pattern of "SQL-
  callable introspection over the indexed data." Lifted as the
  introspection escape hatch (parallel to `fts5vocab` for
  keyword search).
- **`vec_version()` / `vec_debug()`** — registered at lines
  10641 / 10647; runtime introspection (`vec_debug()` returns
  version + build flags + commit). Useful for the canonsim "is
  the extension actually loaded?" probe.
- **Loadable-extension entrypoint + Python `sqlite_vec.load
  (db)`** — the C extension is loaded into the SQLite runtime
  via `sqlite3_load_extension` (Python: `db.enable_load_exten-
  sion(True); sqlite_vec.load(db); db.enable_load_extension
  (False)` — `examples/simple-python/demo.py:13–16`). The CLI
  flag for the `sqlite3` shell is `.load ./vec0` (README sample,
  line 64). **Crucially, this is NOT in Python's stdlib** —
  `sqlite-vec` ships as a `.so`/`.dll`/`.dylib` downloaded from
  GitHub Releases (or `pip install sqlite-vec` which bundles
  the precompiled binary). The macOS system Python **lacks
  `enable_load_extension` entirely** (`site/using/python.md`
  documents the `AttributeError: 'sqlite3.Connection' object
  has no attribute 'enable_load_extension'` failure — Homebrew
  Python is the documented workaround). Lifted as the intake
  contract: conditional loadable extension, NOT a phase-0
  runtime dependency (D-012 compliance).
- **`serialize_float32()` / `serialize_int8()` Python helpers**
  — `bindings/python/extra_init.py` ships a 4-line pure-Python
  `struct.pack("%sf" % len(v), *v)` serializer. This is the
  *exact* pattern canonsim's fallback needs: vectors over the
  wire are just `struct.pack`-ed `float32` BLOBs, no extension
  required to *produce* them. Lifted into `core/storage.py`
  pure-Python fallback — same BLOB format, same
  `cosine_sim(a: bytes, b: bytes) -> float` signature as
  `vec_distance_cosine`.

**What we take.**

- The `vec0` virtual-table shape as the canonical "vector index
  over facts" pattern — a single `CREATE VIRTUAL TABLE lore_vec
  USING vec0(embedding float[D], +fact_text text, scenario_id
  integer partition key)` gives canonsim's phase-4 retrieval
  layer the same ergonomics as its FTS5 keyword index: `WHERE
  embedding MATCH :q ORDER BY distance LIMIT k`. The auxiliary
  `+fact_text` column means retrieval returns the fact payload
  with no JOIN — same single-table pattern as the `events`
  JSONL fold. The `scenario_id integer partition key` column
  maps cleanly onto canonsim's phase-0 tavern scope (one
  partition per scenario; pre-filters kNN to in-scope facts).
- The `vec_distance_cosine(a, b)` as the canonical similarity
  metric for static-lore RAG. Cosine is the right default for
  normalized embedding models; sqlite-vec defaults to L2 but
  exposes `distance_metric=cosine` as a per-column DDL knob —
  canonsim lifts both the metric choice and the "per-column
  configurable distance" idea.
- The matryoshka pattern (`vec_slice` + `vec_normalize`) — train
  embeddings at high dim (e.g. 1024), store at 256 → ~4×
  smaller lore index for the tavern scenario's static-fact
  corpus, with minimal recall loss. This is the compression
  strategy canonsim adopts *if/when* the fact store grows past
  the brute-force-comfortable threshold.
- The `vec_quantize_binary` + rescore two-pass pattern as the
  canonical compression fallback before reaching for an ANN
  index: build a coarse `bit[D]` column alongside the
  `float[D]` column, kNN-filter on the bit index at high k, then
  re-rank the survivors with `vec_distance_L2`. This is the
  canonsim "scale-up without adding a server" ladder rung.

**What we adapt.**

- Conditional loadable extension, NOT a phase-0 runtime
  dependency (D-012 compliance). sqlite-vec is a C `.so`/`.dll`/
  `.dylib` that does **not** ship with Python's stdlib `sqlite3`.
  canonsim's `SQLiteIndex` rebuilder probes
  `db.enable_load_extension(True)` + `sqlite_vec.load(db)` inside
  a `try/except (AttributeError, sqlite3.OperationalError)`; if
  unavailable (macOS system Python, restricted envs, CI without
  the binary), the retriever silently degrades to pure-Python
  brute-force and `vec_version()` is never called. The pattern
  is intake-as-pattern, not intake-as-dep.
- Pure-Python `cosine_sim()` fallback lifted from
  `vec_distance_cosine`'s contract. Same signature shape
  `cosine_sim(a: bytes, b: bytes) -> float` returning a distance
  (`1 - dot/(|a|·|b|)`), operating on the same `struct.pack("%sf",
  ...)` BLOB format that `bindings/python/extra_init.py` documents.
  The vec0 *shape* (`CREATE VIRTUAL TABLE … MATCH … ORDER BY
  distance LIMIT k`) is preserved as a SQL view over a plain
  `facts(rowid, embedding BLOB, ...)` table — the `WHERE
  embedding MATCH` clause becomes a Python-side scan that yields
  the same `(rowid, distance)` tuple stream.
- `vec0` shadow-table separation as an architectural metaphor,
  not a literal copy. sqlite-vec keeps vector payloads in
  `_chunks`/`_vector_chunks00` shadow tables separate from the
  `_rowids` PK table so the heavy BLOBs don't bloat the rowid
  index. canonsim adapts this by storing event-log-derived fact
  embeddings in a **separate `fact_embeddings(fact_id, embedding
  BLOB)` table** alongside the main `facts` table — same
  separation-of-PK-from-payload discipline, expressed as ordinary
  (non-virtual) SQLite tables so it works without the extension
  loaded.

**What inspires us.**

- Vectors are just another typed column on the same SQLite index
  — sqlite-vec treats embeddings as a first-class column type on a
  virtual table in the same database that holds the FTS5 keyword
  index; there is no separate vector server, no second process,
  no second storage format. This validates canonsim's INV-1 stance
  (SQLite is a rebuildable index over the JSONL log) extending to
  the RAG layer: the embedding column is just another rebuildable
  projection of the same event log.
- Loadable extension keeps the runtime minimal — if you don't load
  it, the runtime is still stdlib-only. The `.load`-at-startup model
  is the canonical expression of canonsim's "pattern at intake, dep
  only at opt-in" rule. The binary is a capability, not a
  dependency.

**Strengths.**

- Local-first — no qdrant/lancedb server. The same SQLite database
  file that holds the event-log index, the FTS5 keyword index, and
  the metadata tables also holds the `vec0` vector index. One
  file, one process, one backup. Aligns perfectly with canonsim's
  "single random.Random(seed), single SQLite index" runtime.
- Pure-C, zero-dependency, runs anywhere SQLite runs (Linux/
  macOS/Windows/WASM/Raspberry Pi) — the README's "anywhere" claim
  is borne out by the single-file `sqlite-vec.c` + `sqlite-vec.h`
  amalgamation (`sqlite-dist.toml` declares `amalgamation =
  {include=["sqlite-vec.c", "sqlite-vec.h"]}`). No BLAS, no
  OpenMP, no native deps.
- `vec0` shape mirrors FTS5 — same `CREATE VIRTUAL TABLE ...
  USING <mod>(...)` DDL, same `WHERE <col> MATCH :query ORDER BY
  distance LIMIT k` kNN idiom, same shadow-table separation.
  canonsim gets keyword search and vector search with one mental
  model.
- Matryoshka + binary-quantization built in — `vec_slice`/
  `vec_normalize` and `vec_quantize_binary` + the two-pass rescore
  CTE pattern give canonsim a clean storage-compression ladder
  (float32 → 256-d slice → bit-quantized) *before* needing an ANN
  index.
- Partition-key columns map directly onto canonsim's per-scenario
  scoping (`scenario_id integer partition key`) — the index is
  physically sharded so kNN never scans facts from other scenarios.

**Weaknesses.**

- C extension — not in Python stdlib; D-012 forbids it as a
  default runtime dependency. Must be installed (`pip install
  sqlite-vec` bundles a precompiled binary) and loaded at runtime
  via `enable_load_extension`, which is **disabled on macOS
  system Python** entirely (`AttributeError: 'sqlite3.Connection'
  object has no attribute 'enable_load_extension'`). Phase 0
  cannot rely on it; phase 4 must treat it as opt-in.
- Brute-force only for the core `vec0` path. The README and
  `site/guides/binary-quant.md` both state sqlite-vec is *"brute-
  force only and meant to run on small devices."* (IVF and DiskANN
  modules exist in separate `sqlite-vec-ivf.c` / `sqlite-vec-
  diskann.c` files but are gated/experimental.) For very large
  corpora (≫10⁵ facts), qdrant or lancedb would be needed —
  canonsim's tavern-scale static lore is fine, but a multi-
  scenario cumulative store eventually outgrows it.
- Pure-Python fallback is O(N·D) per query. Without the
  extension loaded, canonsim's brute-force `cosine_sim` over a
  `facts` table scans every row × every dim. Viable for the
  phase-0 tavern's small N (hundreds to low thousands of facts);
  becomes painful past ~10⁴ facts at 768-d.
- Pre-v1, breaking changes expected (README `> [!IMPORTANT]
  _sqlite-vec is a pre-v1, so expect breaking changes!_`). The
  API surface (`vec_distance_cosine`, `vec_quantize`, the `k =`
  vs `LIMIT` duality) is still moving — canonsim should pin a
  specific version and treat the SQL contract as the stable
  interface, not the C ABI.
- No approximate search in the stable path + no native HNSW/IVF
  in the default build. The `vec0` module's `enum Vec0IndexType`
  admits IVF/Diskann (`struct Vec0IvfConfig ivf; struct
  Vec0DiskannConfig diskann;` at lines 2693–2694) but these live
  in separate C files and are not the default; depending on them
  couples canonsim to the unstable experimental surface.

**Verdict.** Phase-4 retrieval-candidate reference — the local-
first vector-index candidate; the canonical `vec0` shape and
`vec_distance_cosine` metric are lifted as the intake pattern,
but the C extension itself is an optional, conditionally-loaded
capability; phase-0 canonsim stays stdlib-only with a pure-Python
brute-force `cosine_sim()` fallback over the same SQLite-stored
embeddings. Dual `MIT OR Apache-2.0` license (verified 2026-08-
26 from the repo `LICENSE-MIT` + `LICENSE-APACHE` files +
`sqlite-dist.toml` manifest; catalog "verify" status resolved —
KI#6-class drift pre-flip caught: index §2 said "MIT" vs the
verified dual `MIT OR Apache-2.0`; index fixed in the same §2
edit that flips ref-11-c todo→done). The "vectors are just
another typed column on the same SQLite index" lesson is the
inspiration: the embedding column is just another rebuildable
projection of the same event log (INV-1 extends to the RAG
layer). The "loadable extension keeps the runtime minimal — if
you don't load it, the runtime is still stdlib-only" lesson
shapes canonsim's "pattern at intake, dep only at opt-in" rule.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
