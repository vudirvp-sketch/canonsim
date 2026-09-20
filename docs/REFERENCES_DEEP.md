# REFERENCES_DEEP.md — Index & Format Template for Per-Reference Deep Dives

> Companion to `docs/REFERENCES.md` (catalog); the cross-reference
> synthesis lives in `docs/BLUEPRINT.md` (D-027). Where the
> catalog says "Mesa — Python ABM framework", the per-ref files in
> `docs/ref/` say **what Mesa actually does, mechanically, and what we
> take / adapt / reject / inspire from**.
>
> This file is the **index** + the **format template** + the **iteration
> plan**. The concrete deep dives live in `docs/ref/<source>.md` — one
> file per source (D-026). The single-file arrangement (D-024) did not
> scale: at iter-0j the file was 737 lines and ref-3..ref-11 would push
> it to ~3000. Per-ref files keep each source under the 600 cap
> (AGENTS §6) by construction — no substance exceptions needed.
>
> Anti-drift (AGENTS §3, `AGENT_NAVIGATION.md` §3): the catalog stays
> the source for **license / URL / phase gating / intake rules** — never
> restated in `docs/ref/`. `docs/BLUEPRINT.md` (the ledger + the
> cross-cutting laws) owns the cross-reference synthesis — never
> restated in `docs/ref/`. Per-ref files are the **concrete mechanics**
> layer: named systems, real data structures, pseudo-code where it earns
> its keep, honest strengths and weaknesses, a per-source verdict.
> Review quarterly alongside the `doc-2` license re-verification.
>
> Phase law (`ROADMAP.md` §4, `MVP_SCOPE.md` §2) still owns when a source
> is *consulted*. Reading design notes early is allowed; vendoring early
> is scope creep. Nothing here lifts the phase-0 zero-external-code gate
> (D-012, D-015, D-022).
>
> The applied synthesis over these deep dives — cross-reference resolutions
> and donor combinations per build component — lives in `docs/BLUEPRINT.md`
> (D-027). This index stays the owner of the iteration plan + format.

## 0. Format (every per-ref file follows this template)

```
# <source> · <catalog §> · <license> · <phase/track>

> Per-reference deep dive. Format template: this file §0. Iteration
> plan: this file §1. Anti-drift (D-026): catalog/license/URL/phase
> gating in `docs/REFERENCES.md`; one-line
> the cross-reference synthesis in `docs/BLUEPRINT.md`; concrete mechanics
> here. License
> filter and "patterns not content" rule: `REFERENCES.md` §0.7 (D-015).

**What it is.** One sentence: what the project IS, mechanically.
**Concrete mechanics.** Named systems, real data structures, a snippet
  where it earns its keep. Not a feature list — the parts that matter.
**What we take.** Specific, named — a class, a pattern, an algorithm.
**What we adapt.** Specific, named — and *how* we change it.
**What inspires us.** The design lesson (one clause, not a paragraph).
**Strengths.** Concrete virtues we cannot get cheaper elsewhere.
**Weaknesses.** Concrete defects — the source's failure
  modes, expanded here.
**Verdict.** One line: what role this source plays in our work.

[body]

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
```

If an entry would not fill every field honestly, the source is too thin
for a deep dive — leave it in the catalog only.

## 1. Iteration plan (which references get a solo iter, which batch)

A reference is **huge** (solo iter) if it has ≥3 distinct subsystems each
worth deep coverage, or if a real reading pass takes a full evening. A
reference is **batchable** (2–3 per iter) if its lessons fit one focused
session. This plan lives in `docs/TASKS.md` (infra backlog, `ref-N`); the
size verdict is recorded here so a future agent picks items in order
without re-judging.

| ID | References | Solo / Batch | Rationale |
|---|---|---|---|
| iter-0h | Neighborly + Mesa + DF Legends XML (export schema only) | 3-batch | framework setup + the three cousins |
| ref-1 | DF worldgen + history layer (the half not covered in iter-0h) | solo | 5+ subsystems: history ticks, populations vs notables LOD, age/civ dynamics, artifact anchors, reputation as event |
| ref-2 | C:DDA `data/json/` schema | solo | the reference for content-as-JSON at scale — items, monsters, recipes, missions, factions; CC-BY-SA lets us lift |
| ref-3 | Paradox event scripting (CK3 + EU4 + Stellaris) | solo | three wikis, complex grammar (trigger / weight / mtth / effect / option / scope); phase-3 design backbone |
| ref-4 | RimWorld + L4D Director + Alien: Isolation | 3-batch | pacing/storyteller trio; all closed; design-notes only; phase-3 director ref |
| ref-5 | Wesnoth WML + Endless Sky mission DSL + ink + tracery | 4-batch | event/narrative grammar family; same conceptual shape |
| ref-6 | Brogue + DCSS + KeeperRL | 3-batch | roguelike emergence + micro-sim; environmental sim from few rules |
| ref-7 | Stanford Generative Agents + ai-town + letta | 3-batch | LLM-agent precedents — mostly negative; bg-4 cost notes overlap |
| ref-8 | Azgaar FMG + Natural Earth + GeoNames | 3-batch | worldgen data donors; phase-5 |
| ref-9 | libtcod + rot.js + Red Blob Games | 3-batch | FOV / pathfinding / grid math — pattern only (D-012) |
| ref-10 | entt + Bevy + EventStore | 3-batch | ECS scheduling + event-sourcing stream/projection patterns |
| ref-11 | SQLite FTS5 + DuckDB + sqlite-vec | 3-batch | storage layer candidates; depends on phase-4 retrieval decision |
| ref-12 | Universe Audit Protocol webapp (owner's own) | solo (owner-requested, fresh external source) | LLM world-concept audit: one domain, one focused session; rubric discipline + harness patterns + license catch |
| ref-13 | Live Character Guide (owner's own) | solo (owner-requested, fresh external source) | character-card methodology: SPINE/Price/observability → pack lint + brief-layer injection grammar; license clean (MIT) |
| ref-16 | agent-memory-atlas (neoneye) | solo (owner-requested, fresh external source; absorbed inside iter-8a — the D-022 exception, no solo iteration) | 151-system memory survey: 7 marks + 22 patterns → phase-1 scene ledger (D-048) + phase-4 memory checklist; license clean (MIT, GitHub API 2026-08-28) |
| ref-17 | DF designed experience (the player-facing half not covered by iter-0h-c / ref-1) | solo (owner-requested research pass — the D-022 exception, iter-8d) | enchantment pillars P1–P6 + flaw taxonomy F1–F10 (missing layers, not wrong simulation) + successor trade-off matrix feed bg-1 hardening, phase-3 director posture, phase-5 LOD; every flaw maps to an existing mechanism or recorded phase |
| ref-18 | X4 + Stellaris economy + Distant Worlds | 3-batch (landed iter-109 — the phase-6 opening call, the TASKS res-1 row's owed dives: `docs/ref/x4.md` + `stellaris_economy.md` + `distant_worlds.md`) | the economy trio: agent supply chains + cascading failures / abstract trade value + piracy risk / private-vs-state sector — res-1's design backbone (phase 6) |
| ref-19 | CK3 (pillars/tags/name pools) + the Azgaar name pools | 2-batch (landed iter-96, D-131 — just-in-time at name-1's row, the D-116 plan) | the name generator's phonotactic profiles + the culture-as-pillar data shape — name-1's design backbone (phase 5) |
| ref-20 | EVE + Path of Exile + Albion + Shadows of Doubt (+ Kenshi's economy loop) | 4-batch (+1 riding: landed iter-109 — the same opening call: `eve_online.md` + `path_of_exile.md` + `albion_online.md` + `shadows_of_doubt.md` + `kenshi.md`) | economy-as-social-contract + physical tracing: sinks, friction, information asymmetry, risk premiums — res-1's lesson set + the theft family's confirmation (phase 6) |

A "batch" iteration produces one file per source — the batching is a
scheduling concept (which sources to read in the same evening), not a
file-grouping rule. A solo iteration produces one file. Either way the
scope is 2 files touched (one new `docs/ref/<source>.md` + this index
to flip status), well within the 3–5 soft limit (AGENTS §2.3).

## 2. Index of per-ref files

| ID | Source | File | License | Phase / Track | One-line verdict | Status |
|---|---|---|---|---|---|---|
| iter-0h-a | Neighborly | `docs/ref/neighborly.md` | MIT | phase 5 (cousin); iter-3 (P2a pattern source) | pair-keyed relationship map shape; P2a precedent | done |
| iter-0h-b | Mesa | `docs/ref/mesa.md` | Apache-2.0 | phase 0 (architectural pattern) | Python ABM reference; single-RNG discipline; amnesia anti-pattern | done |
| iter-0h-c | DF Legends XML | `docs/ref/df_legends_xml.md` | proprietary (export only) | bg-1..bg-4 (track B) | event-id + tick schema; `event_collections`; reputation-as-event | done |
| ref-1 | DF worldgen + history layer | `docs/ref/df_worldgen.md` | proprietary (read exported data only) | bg-1..bg-4 (track B); phase 5 LOD | history ticks abstractly; populations vs notables LOD ladder | done |
| ref-2 | C:DDA `data/json/` schema | `docs/ref/cdda_data_json.md` | CC-BY-SA 3.0 | phase 3 (content-pack reference) | content-as-JSON at scale; per-category file split; pair-keyed `relations` | done |
| ref-3 | Paradox event scripting | `docs/ref/paradox_scripting.md` | (closed wikis) | phase 3 (event grammar) | trigger / weight / mtth / effect / option / scope backbone | done |
| ref-4-a | RimWorld | `docs/ref/rimworld.md` | closed | phase 3 (director ref) | Defs taxonomy + IncidentDef field shape + storyteller trio (D-005 anti-pattern named) | done |
| ref-4-b | L4D Director | `docs/ref/l4d_director.md` | closed | phase 3 (director ref) | intensity ratchet + peak/rest clock + multi-channel family | done |
| ref-4-c | Alien: Isolation | `docs/ref/alien_isolation.md` | closed | phase 3 (director ref) | two-AI split (actor vs director) + pressure-scalar cap-and-floor + encounter-window floor + three-axis anxiety (perceived/actual/unknown) | done |
| ref-5-a | Wesnoth WML | `docs/ref/wesnoth_wml.md` | GPL-2.0+ | phase 3 (event grammar family) | `[event]`/`[filter]`/action triad + `first_time_only`/`id`/`delayed_variable_substitution` orthogonal fields + Lua escape-valve precedent (`cli/`/`… — detail: the ref file | done |
| ref-5-b | Endless Sky mission DSL | `docs/ref/endless_sky_dsl.md` | GPL-3.0 code; mixed assets | phase 3 (event grammar family) | mission lifecycle (offer/accept/complete/fail/defer) + flat `effect` mini-language + `phrase` one-symbol grammar + `event` block as background-even… — detail: the ref file | done |
| ref-5-c | ink | `docs/ref/ink.md` | MIT | phase 3 (event grammar family) | knot/stitch/divert/gather graph shape (`Brief` sketch inherits) + `LIST` multivalued flags (`entity.state` inherits) + `+`/`*` choice persistence (… — detail: the ref file | done |
| ref-5-d | tracery | `docs/ref/tracery.md` | Apache-2.0 | phase 3 (event grammar family) | JSON grammar shape (`templates.json` inherits) + save/restore stack (`render/` `stack[pop]` inherits) + modifier pattern (`templates.json` modifier… — detail: the ref file | done |
| ref-6-a | Brogue | `docs/ref/brogue.md` | AGPL | phase 5 (roguelike emergence) | two-stream RNG discipline (`RNG_SUBSTANTIVE`/`RNG_COSMETIC` with `brogueAssert` scope guards) + 36-byte no-wall-clock recording header (version/see… — detail: the ref file | done |
| ref-6-b | DCSS | `docs/ref/dcss.md` | GPL | phase 5 (roguelike emergence) | multi-stream RNG (`rng_type` enum: `GAMEPLAY`/`UI`/`SYSTEM_SPECIFIC`/`LEVELGEN`+per-branch, RAII `rng::generator` for stream switching) + PCG gener… — detail: the ref file | done |
| ref-6-c | KeeperRL | `docs/ref/keeperrl.md` | GPL | phase 5 (roguelike emergence) | continuous-time queue (`map<ExtendedTime, Queue>` with `players`/`nonPlayers` deques, `orderMap` per-queue-position tiebreaker, `extraTurn` flag fo… — detail: the ref file | done |
| ref-7-a | Stanford Generative Agents | `docs/ref/generative_agents.md` | Apache-2.0 (repo) + paper | bg-4 (cost notes) / phase 4 (memory patterns) | memory stream shape (one-to-one with our per-NPC knowledge records) + retrieval function `recency + importance + relevance` top-k (lifted into `cor… — detail: the ref file | done |
| ref-7-b | ai-town | `docs/ref/ai_town.md` | MIT | bg-4 (cost notes) / negative reference | Convex reactive database + `engine.ts` per-tick LLM call + `agentStep` action-grammar discriminated-union (`MoveAction`/`SayAction`/`WaitAction`, l… — detail: the ref file | done |
| ref-7-c | letta (ex-MemGPT) | `docs/ref/letta.md` | Apache-2.0 | bg-4 (cost notes) / phase 4 (memory patterns) | block manager context-window partition [`system`/`persona`/`human`/`tools`/`scratchpad`/`fifo_queue` blocks with per-block token budget, lifted int… — detail: the ref file | done |
| ref-8-a | Azgaar FMG | `docs/ref/azgaar_fmg.md` | MIT | phase 5 (worldgen donors) | four-layer architecture (world data/generators/editors/renderers — INV-1 inherits the split: canon log = world data — detail: the ref file | done |
| ref-8-b | Natural Earth | `docs/ref/natural_earth.md` | public domain | phase 5 (worldgen donors) | three-scale LOD ladder (1:10m / 1:50m / 1:110m — same theme at three LODs, consumer picks scale — detail: the ref file | done |
| ref-8-c | GeoNames | `docs/ref/geonames.md` | CC-BY 4.0 | phase 5 (worldgen donors) | 9-class / 684-code feature-class enum (verified 2026-08-26 against live `download.geonames.org/export/dump/featureCodes_en.txt` dump — `readme.txt`… — detail: the ref file | done |
| ref-9-a | libtcod | `docs/ref/libtcod.md` | BSD-3-Clause | phase 5 (grid math, pattern only) | FOV algorithm closed enum (14 algorithms: `FOV_BASIC`/`FOV_DIAMOND`/`FOV_SHADOW`/`FOV_PERMISSIVE_0`/`1`/`2`/`3`/`4`/`5`/`6`/`7`/`8`/`FOV_RESTRICTIV… — detail: the ref file | done |
| ref-9-b | rot.js | `docs/ref/rot_js.md` | BSD-3-Clause | phase 5 (grid math, pattern only) | `EventQueue` min-heap core (`_time` + `_events` MinHeap<T> + `getTime()`/`clear()` — detail: the ref file | done |
| ref-9-c | Red Blob Games | `docs/ref/red_blob_games.md` | CC-BY (treat as) | phase 5 (grid math, pattern only) | hex grid coordinate algebra (offset odd-r/even-r/odd-q/even-q + axial (q, r) + cube (x, y, z with x+y+z=0) + doubled — detail: the ref file |Δx|, |Δy|, |Δz|)` + line drawing via cube-coord sampling + rounding + range walking the cube coordinate ring + rotation by 60° in cube coords + FOV/line-of-sight via hex-grid line drawing + pixel-to-hex conversion for pointy-top + flat-top orientations with fractional hex intermediate; the canonical write-up that every hex-grid library (libtcod + rot.js + hexlib + reffy) implements; deferred to phase-5+ spatial layer if hex-based, phase-0 tavern is a fixed pack-authored location graph (no grid)) + A* pseudo-code (open set + closed set + g cost-from-start + h heuristic estimate-to-goal + f = g + h + pick lowest f + expand neighbors + update g and parent; BFS/Dijkstra/A* family framing with different h choices (0 for BFS, exact for Dijkstra, estimated for A*); heuristic functions Manhattan/Euclidean/Chebyshev/Octile by movement rules; priority queue binary heap + tiebreaking prefer higher g toward goal; the most-cited A* tutorial in game dev; lifted into `core/resolvers.py` iter-2 — libtcod + rot.js implementations are concrete instances of this algorithm) + polygon map generation pipeline (Voronoi diagram from N random points via d3-delaunay/delaunator + Lloyd's relaxation 1-2 iterations for uniform distribution + Perlin noise elevation with radial gradient for island shape + watershed downhill tracing for rivers + Whittaker biome diagram elevation × moisture → biome type + noisy edges for hand-drawn look via `/maps/noisy-edges/`; the canonical Voronoi+noise worldgen — Azgaar FMG `azgaar_fmg.md` implements the same algorithm with additional passes states/cultures/religions; deferred to phase-5+ worldgen) + relational grid abstraction (faces/edges/corners with typed relations — a face has edges, each edge has 2 corners, each corner has 3 edges; same relational shape for square/hex/triangle grids, different geometries; grid as graph of parts with relations; deferred to phase-5+ spatial layer's per-part query interface) + circle drawing algorithms (midpoint circle + Andreev for AoE effects + circular rooms; lifted into `core/transitions.py` iter-2 fire_spread AoE queries) + distance-to-any single-source Dijkstra + all-pairs Floyd-Warshall pre-compute (choice: Dijkstra for one-off paths, Floyd-Warshall for pre-computed small maps; lifted into `core/resolvers.py`); explicitly negative on no explicit license statement (site has no license on article pages — verified 2026-08-26 by inspecting `/grids/hexagons/` + `/pathfinding/a-star/introduction.html` + `/about`; CSS comment 'CSS Copyright 2007-2026 by Amit J. Patel' is for stylesheet not content; Amit Patel explicitly requests attribution in academic contexts per `/blog/`; convention adopted here = treat as CC-BY 4.0, re-evaluate if stance changes) + HTML5 canvas demos (lift formulas + pseudo-code only, not interactivity) + d3-delaunay/delaunator dependency for Voronoi (port to Python stdlib — Python's `geometry` + `math` modules suffice for small N) + not a code repository (formulas in prose + diagrams, no `git clone` to inspect) + hex grid not directly relevant to phase-0 (defer to phase-5+ if we go hex) + polygon map generation not directly relevant to phase-0 (defer to phase-5+ worldgen); the site is the canonical write-up layer above the libtcod + rot.js implementations — algorithm shapes here are the source of truth that implementations are concrete instances of; 'BFS/Dijkstra/A* are a family with different heuristics' lesson shapes the `core/resolvers.py` config-time choice of algorithm; 'worldgen is composition of focused passes' lesson (Voronoi → relax → elevation → watershed → biomes → noisy edges) is the same lesson as Azgaar FMG and 'small alphabet deep composition' lesson from `brogue.md`; interactive HTML5 canvas demos lesson (algorithm write-ups benefit from interactivity) shapes phase-5+ frontend explorability goal | done |
| ref-10-a | entt | `docs/ref/entt.md` | MIT | phase 5 (ECS patterns) | C++ ECS sparse-set blueprint — `basic_sparse_set` dual-array (`sparse` page-ptr + `packed` entity) + `deletion_policy` swap_and_pop/in_place/swap_o… — detail: the ref file | done |
| ref-10-b | Bevy | `docs/ref/bevy.md` | MIT OR Apache-2.0 (dual) | phase 5 (ECS patterns) | Rust ECS + scheduler — detail: the ref file | done |
| ref-10-c | EventStore | `docs/ref/eventstore.md` | BSD-3-Clause (≤23.x); ESLv2/Kurrent-License-v1 from 24.10 — pattern only | phase 5 (event-sourcing) | canonical event-sourcing mechanics — `EventRecord` (EventId Guid + EventType string + Data + Metadata byte[] + EventStreamId + EventNumber + LogPos… — detail: the ref file | done |
| ref-11-a | SQLite FTS5 | `docs/ref/sqlite_fts5.md` | public domain | phase 4 (retrieval candidates) | zero-dependency keyword search in stdlib SQLite — `CREATE VIRTUAL TABLE <name> USING fts5(<col1>, <col2>, ...)` schema (implicit `rowid` PK, no typ… — detail: the ref file |1|2 + `categories` + `tokenchars`/`separators`; `ascii`; `porter` wrapper applying Porter stemmer over another tokenizer; `trigram` for substring matching; custom via `fts5_api` struct out of scope) + `bm25(<table>[, w0, w1, ...])` (lower = better, `k1=1.2`, `b=0.75`, per-column positional weights) + `highlight(<table>, colIdx, before, after)` + `snippet(<table>, colIdx, before, after, ellipsis, maxTokens≤64)` + query operators (`AND`/`OR`/`NOT` precedence `NOT`>`AND`>`OR`; `NEAR(p1 p2 [, N=10])` proximity; `*` prefix token; `^` initial-token anchor; `+` phrase concat; `col:` / `{c1 c2}:` column filters) + `INSERT INTO ft(ft, ...) VALUES(...)` lifecycle (`rebuild` full reindex, `optimize` merge-all, `merge ±N` incremental, `automerge`/`crisismerge`/`usermerge`/`deletemerge` thresholds, `delete`/`delete-all`, `integrity-check`, `rank` set-default) + `fts5vocab` introspection virtual table (`row`/`col`/`instance`) + 5 shadow tables (`%_data`/`%_idx`/`%_config`/`%_docsize`/`%_content` — never accessed directly) + segment b-trees (immutable, leveled, newer-wins) + content-table variants (plain/contentless/contentless-delete/external-content); lifted into `core/retrieval.py` (the `facts` FTS5 virtual table — D-003 canon index; queries go through MATCH) + `scripts/chronicle.py` (the offline chronicler) + `brief/assembler.py` (bm25 positional column weights as the zero-dep baseline ranker — subject/title weighted above body) + `render/` (highlight for span wrapping + snippet for auto-excerpt) + unicode61 default for multilingual content packs (café/Café/CAFÉ match by default) + NEAR for proximity queries (theft NEAR/3 arson — find facts where these words appear within 3 tokens) + `rebuild` command as the INV-1 mechanism (schema/tokenizer change = drop+recreate+replay — the expected path); explicitly negative on keyword-only (need sqlite-vec for semantic) + ranking customization is bm25 + custom C function only (recency×authority×BM25 blend needs Python reranker) + tokenizer fixed at CREATE TABLE (switch forces full rebuild — INV-1-expected path but plan at design time) + segment b-trees accumulate under write-heavy loads (batch inserts + optimize once at end, not per event) + `delete` on contentless tables brittle (prefer plain tables + full rebuild); 'BM25 is the canonical keyword-relevance baseline — anything semantic compares against it' lesson + 'inverted index as a fold-of-the-log projection' lesson (FTS5's `rebuild` is the proof INV-1's log=truth/SQLite=index split has a first-class supported refresh path) shape phase-4 retrieval; public domain (verified 2026-08-26 from sqlite.org/copyright.html — ships inside Python's sqlite3 stdlib module, D-012-compliant by construction) — zero friction at intake | done |
| ref-11-b | DuckDB | `docs/ref/duckdb.md` | MIT | phase 4 (offline analytics — NOT runtime; D-012) | in-process columnar OLAP engine — `DuckDB` class (in-memory `nullptr` or persistent path — detail: the ref file | done |
| ref-11-c | sqlite-vec | `docs/ref/sqlite_vec.md` | MIT OR Apache-2.0 (dual) | phase 4 (retrieval candidates — local-first vector index) | local-first vector index in SQLite — `vec0` virtual-table module (`CREATE VIRTUAL TABLE <name> USING vec0(<col> <type>[N] [pk] [partition key] [dis… — detail: the ref file |cosine], <other_col>, +<aux_col>)` — same shape as FTS5) + implicit `rowid` + MATCH kNN (`WHERE <col> MATCH :query_vec ORDER BY distance LIMIT k`, or pre-3.41 `and k = N`) + `vec_distance_cosine(a, b)` (canonical name, not `vec_distance_cos`; cosine distance = `1 - cos`) + `vec_distance_L2`/`vec_distance_L1`/`vec_distance_hamming` (L2 default; cosine opt-in per-column via `distance_metric=cosine`) + `vec_f32`/`vec_int8`/`vec_bit` constructors (subtype byte tagging — 223/225/224 on otherwise-undifferentiated BLOB) + `vec_to_json(v)` (BLOB → JSON array serialization; JSON input via `JSON_SUBTYPE = 74`) + `vec_quantize_binary(v)` (32× storage reduction, 8 dims/byte) + `vec_quantize_int8(v, 'unit')` + `vec_slice(v, start, end)` + `vec_normalize(v)` (matryoshka embeddings — train at 1024-d, store/query at 256-d → ~4× index shrink) + `vec0` shadow tables (`_rowids` + `_chunks` + per-vector `_vector_chunks00` + `_rescore_chunks00`/`_rescore_vectors00` + per-metadata `_metadatachunks00`) + partition-key columns + auxiliary columns (`+`-prefixed, no JOIN needed for SELECT, max 16 metadata + 16 auxiliary + 4 partition keys) + `vec_each(v)` TVF (per-element inspection — mirrors FTS5's fts5vocab) + `vec_version()`/`vec_debug()` runtime introspection + loadable-extension entrypoint via `sqlite3_load_extension` (Python: `db.enable_load_extension(True); sqlite_vec.load(db); db.enable_load_extension(False)`; macOS system Python lacks `enable_load_extension` entirely) + pure-Python `struct.pack("%sf" % len(v), *v)` serializer helper; lifted into the canonical "vector index over facts" pattern for `core/retrieval.py` (the vec probe/scan/floor chain, iter-59; `CREATE VIRTUAL TABLE lore_vec USING vec0(embedding float[D], +fact_text text, scenario_id integer partition key)` — same ergonomics as FTS5 keyword index, same single-table pattern, partition-key column maps onto phase-0 tavern scoping) + `vec_distance_cosine` as the canonical similarity metric + matryoshka compression strategy if fact store grows past brute-force threshold + binary-quant two-pass pattern (coarse bit[D] kNN filter then L2 rescore — the scale-up-without-server ladder rung); explicitly negative on C extension not in Python stdlib (D-012 fix: conditional loadable extension at phase 4 — phase 0 stays stdlib-only with pure-Python `cosine_sim()` brute-force fallback over the same BLOB format) + pure-Python fallback O(N·D) (viable for phase-0 small N < 10⁴ facts, painful past 10⁴ at 768-d) + pre-v1 with breaking changes expected (pin a version, treat SQL contract as the stable interface not C ABI) + no approximate search in stable path (HNSW/IVF/DiskANN live in separate experimental C files, not the default — at very large corpora qdrant/lancedb would be needed); 'vectors are just another typed column on the same SQLite index' lesson (no separate vector server — embedding column is just another rebuildable projection of the event log, INV-1 extends to RAG layer) + 'loadable extension keeps the runtime minimal — if you don't load it, the runtime is still stdlib-only' lesson (pattern at intake, dep only at opt-in) shape phase-4 retrieval; catalog "verify" license status RESOLVED to dual `MIT OR Apache-2.0` (verified 2026-08-26 from repo LICENSE-MIT + LICENSE-APACHE + sqlite-dist.toml manifest) — license drift KI#6-class (index "MIT" vs verified dual) caught pre-flip in the same §2 edit that flips ref-11-c todo→done with the corrected "MIT OR Apache-2.0 (dual)" annotation | done |
| ref-12 | Universe Audit Protocol webapp (UAP) | `docs/ref/uap_audit.md` | README claims MIT; no LICENSE file (checked 2026-08-27 — reference only) | track B (phase-1 harness) / phase 6 (pack CI) | countable-criteria rubric donor (external validation of M1-M5 + gate reviews) + 7-hole test crosswalk + free-tier resilience patterns — detail: the ref file | done |
| ref-13 | Live Character Guide | `docs/ref/live_char_guide.md` | MIT | track A (iter-2+ observability discipline) + track B (phase-1 brief layer) / phase 6 (pack authoring lint) | character-depth donor: Price/observability + AP→lint vocabulary + brief injection grammar (voice isolation, recency hierarchy, lorebook scheduling) — detail: the ref file | done |
| ref-16 | agent-memory-atlas | `docs/ref/agent_memory_atlas.md` | MIT | track B (phase-1 scene ledger, D-048) + phase 4 (memory patterns) | meta-survey donor: trust states / rejected-value tombstone / scope-as-key / hysteresis→pinning / evidence-before-belief → the scene ledger — detail: the ref file | done |
| ref-17 | DF designed experience | `docs/ref/df_design.md` | proprietary (design patterns only) | phases 1–5 cross-cutting (salience/director/LOD) + bg-1..bg-4 context | enchantment pillars P1–P6 — detail: the ref file | done |
| ref-18-a | X4: Foundations | `docs/ref/x4.md` | proprietary (design notes only) | phase 6 / track A (res-1) | res-1's dependency-graph backbone: the pack-declared recipe graph, stock variables, derived spreads — scarcity as a mechanical cascade, never a scr… — detail: the ref file | done (iter-109) |
| ref-18-b | Stellaris economy | `docs/ref/stellaris_economy.md` | proprietary (design notes only) | phase 6 / track A (res-1) | res-1's aggregate-edge donor: flow-as-number, threat-as-edge-state, consequences-as-declared-penalties — the abstraction half of the scarcity cycle… — detail: the ref file | done (iter-109) |
| ref-18-c | Distant Worlds: Universe | `docs/ref/distant_worlds.md` | proprietary (design notes only) | phase 6 / track A (res-1) | res-1's boundary donor: the declaration/emergence split, the tax-base coupling, constraint-based economy play reading as statecraft — the Dune row'… — detail: the ref file | done (iter-109) |
| ref-19-a | Crusader Kings III (name pools + the culture-as-pillar shape) | `docs/ref/ck3.md` | proprietary (wiki docs CC-BY-SA) | phase 5 (name-1) + phase 6 (cultures, D-116 (12)) | the DATA-SHAPE donor: the culture-keyed pool map (one name vocabulary per culture, the culture id the pack's own vocabulary — the profile IS the to… — detail: the ref file | done | done (iter-96) |
| ref-19-b | Azgaar F-M-G (the name pools) | `docs/ref/azgaar_names.md` | MIT | phase 5 (name-1) | the GENERATOR donor: the nameBase shape — positional syllable-component pools (onsets/nuclei/codas, the empty fragment for vowel initials + open sy… — detail: the ref file | done | done (iter-96) |
| ref-20-a | EVE Online | `docs/ref/eve_online.md` | proprietary (design notes only) | phase 6 / track A (res-1) | res-1's sink + friction + asymmetry donor: the closed-loop law (absolute sinks pump demand), the spread-as-derived read, the rumor-moves-markets co… — detail: the ref file | done (iter-109) |
| ref-20-b | Path of Exile | `docs/ref/path_of_exile.md` | proprietary (design notes only) | phase 6 / track A (res-1 — the social-economy note) | the social-economy note's donor: spend-consumes, value-follows-function, devaluation-on-publication — the sink's grammar (a resource that leaves wh… — detail: the ref file | done (iter-109) |
| ref-20-c | Albion Online | `docs/ref/albion_online.md` | proprietary (design notes only) | phase 6 / track A (res-1) | res-1's risk-premium donor: spread-from-threat, the fear/stagnation social loop, reward-gated-by-danger geography — the river-artery province's eco… — detail: the ref file | done (iter-109) |
| ref-20-d | Shadows of Doubt | `docs/ref/shadows_of_doubt.md` | proprietary (design notes only) | phase 6 / track A (res-1 — the theft family's confirmation) | the theft family's confirmation donor: position + owner + knowers as one read surface — the landed state_changes + known_by + presence already impl… — detail: the ref file | done (iter-109) |
| ref-20-e | Kenshi (the economy loop) | `docs/ref/kenshi.md` | proprietary (design notes only) | phase 6 / track A (res-1 / world-2) | res-1's loop donor + world-2's crime-pressure law: stockpile → faction read → action — the desperation economy binding X4's cascade to a human-read… — detail: the ref file | done (iter-109) |

Status flips to `done` when the per-ref file exists and passes
`pytest -q` + `ruff check .` clean (no test depends on the deep-dive
files; the gate is just that the iteration closes cleanly).

When a future ref-N iteration adds new files to `docs/ref/`, **append to
this table in the same iteration** — same-edit rule, AGENTS §3.
