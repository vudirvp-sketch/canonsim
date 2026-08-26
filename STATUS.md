# STATUS — canonsim

Iteration: 0s (owner-requested: ref-12 — Universe Audit Protocol webapp deep dive, fresh external source; rubric donor for metrics/harness/pack lint; license catch: README claims MIT, no LICENSE file) · Phase: 0 — simulator without LLM · Date: 2026-08-27

iter-0s is the **ref-12 solo deep dive** — the owner's own
`universe-audit-protocol-webapp` (UAP), a fresh external source admitted by
the documented condition ("no further ref-N iterations unless a fresh
external source enters the catalog"). Deliverable: `docs/ref/uap_audit.md`
(+ catalog §9 row, `REFERENCES_DEEP.md` §1/§2 rows,
`CORE_DESIGN_RESEARCH.md` §2 row, SPECS_BACKLOG TEST_PLAN/PACK_SPEC sketch
clauses, TASKS ref-12 + iter-0s lines, this header, worklog entry).

**What UAP is** (read in full: prompts-v3.ts 1346, pipeline-v3.ts 429,
scoring.ts 204, types-v3.ts 222, context-bridge.ts 254, protocol-data.ts,
patch-tree.ts, error-handler.ts 271, llm-client.ts 1140, vitest ~150 cases):
a no-backend web tool (Next.js 16 static SPA + CORS-proxy Worker → 14 LLM
providers, Zustand/localStorage) auditing fictional-world concepts through a
5-block sequential LLM pipeline (protocol v10.0, Russian prompts, English
JSON keys): 1 Orientation (audit mode conflict/kishō/hybrid; author profile
7-question test gardener/hybrid/architect; 8-element skeleton; 7-question
screening, 4+ NO = stop) · 2 Mechanism L1 (MDA+OT 5-level vitality; 17
vitality criteria, 13/17 alive; N×N connectedness matrix with a verb per
cell, ≥2 bidirectional links; 5×5 faction matrix, 6 liveness criteria, <3 =
decoration; Tarkovsky space-memory; ripple ≥2; three handshakes; economic
arrow 6 questions; "A chtoby chto?" 7-iteration why-chain, break ≤4 =
critical) · 3 Body+Psyche L2+L3 (5-layer character model; price of greatness
on identity not HP; Mary Sue 8-item test; Sanderson magic test; **7 logical
hole types** with quick fixes; Grief Architecture 5 stages × 4
materialization levels — one level = structural hole) · 4 Meta L4 (three
reality layers by removal; Cornelian dilemma 4 criteria; misdirection 4
parameters; narrative debt 4 types; diegetic integrity) · 5 Synthesis
(prioritized fixes; patch decision tree; verdict; X/52). Engineering:
chunked sub-requests (4/2/2/2), RPM-aware delay, single retry + 5 s backoff,
partial-text recovery, per-block temperatures 0.2/0.45/0.45/0.45/0.6,
regex context bridge with three fallback layers, non-blocking JSON-mode
checklist scoring with PASS/FAIL/INSUFFICIENT_DATA + evidence quotes.

**Why it matters to us** — the three load-bearing transfers:
1. **External validation of the metric law.** UAP §0.6 "count-based
   screening — code decides, not the LLM" is the narratology-side twin of
   "metrics computed from the log, not by feel" (`MVP_SCOPE.md` §15); their
   "A chtoby chto?" chain is our `cause` chain (M3), audited in prose
   because authored worlds have no log. Independent convergence on
   "quality gates must be countable over evidence".
2. **7-hole taxonomy → test crosswalk** (TEST_PLAN sketch): motivation → T3
   blind-NPC; memory → T2 replay (INV-1 makes the hole structurally
   impossible); competence → rules-driven behavior; scale → D-005 buffer;
   resources/ideology/time → tick queue + phase-5 factions.
3. **Phase-1 harness patterns** (track B): role-in-system persona, full
   criteria+thresholds embedded in prompts (not labels), staged
   weaknesses handoff (= our brief-as-delta from the other direction),
   per-stage temperature policy, free-tier resilience (chunking/RPM/
   retry/partial recovery), honest-default INSUFFICIENT_DATA verdicts for
   VALIDATION_SPEC fact reports; pack-admission lint vocabulary for phase 6
   (PACK_SPEC sketch: dead event types, orphan entities, empty matrix
   cells, prohibitions as pack metadata + log asserts).

**What we reject** (inversions of our invariants): LLM-as-judge scoring
(X/52 = unseeded opinion of the model that wrote the audit — INV-2
violation; their own §0.6 applied to screening but not scoring);
regex-over-markdown inter-block contract (three fallback layers = the
post-hoc sanitization crutch D-018 rejects); free-form markdown as output
(no machine contract); invented thresholds 0.6/0.9/0.2 from the integration
draft (our law: thresholds from the iter-6 measured baseline); literary
criteria (tragedy-without-villain, cult potential) as anything but pack
metadata / chronicler material — never core law (INV-3).

**License catch (KI#6-class, no KI opened — external repo):** README claims
MIT, **no LICENSE file exists** (checked 2026-08-27). Catalog convention:
"none" = reference only. Patterns are free; code lifting stays blocked
until the owner drops a LICENSE into the UAP repo (one file, unlocks a code
donor in our exact domain). Recorded in catalog §9 + index §2 + the ref
file.

**Doc-loop accounting:** 18th consecutive docs iteration. Exception is the
documented one (fresh external source, owner request — same D-022 logic).
The alarm condition now stands harder than before: **iter-1 is
unconditionally the next iteration** — no further ref-N, no spec writing,
no doc polish without a fresh owner request.

**iter-0r closing summary** (full detail: git history + worklog entry):
ref-10 + ref-11 6-batch (entt 359, bevy 469, eventstore, sqlite_fts 368,
duckdb, sqlite_vec) — ECS scheduling + event-sourcing + storage-layer
pattern-only references; KI#6-class license drift caught pre-flip twice
(EventStore BSD→ESLv2 history, sqlite-vec dual MIT/Apache); KI#3, KI#4,
KI#5 unchanged; no docs outside `docs/ref/` + index touched.

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index.
- INV-2 Determinism: single seeded RNG, no wall-clock, `sorted()` iteration,
  fixed `PYTHONHASHSEED`, queue key `(tick, sub_order, actor_id)`.
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#3 · `expectation_violation` primitive missing — NPC reacts only to presence in `knowledge`, not to absence (purse gone, guard missing). Fix: P2d in `CORE_DESIGN_RESEARCH.md` §6, slated for iter-3.
- KI#4 · balance harness (1000-sim distribution plots of `suspicion` / `fire_spread`) missing — MVP_SCOPE §15 promises an iter-6 baseline but no tool exists. Added as `balance-1` in `docs/TASKS.md` infra backlog.
- KI#5 · runtime state vs test fold not explicitly separated — risk of O(N²) at startup if `fold(log)` is misused as runtime path. D-023 records the rule: runtime = incremental projection; fold = T2 replay only.
- KI#7 · Capped-memory drift (2026-08-27): `worklog.md` entries up to ~880 lines vs the 3–5-line law; `TASKS.md` at 1136 with done entries not one-line-collapsed — trim vs migrate needs an owner call (D-025 covers `docs/*.md` caps only, not these rows).

## FAQ / Pitfalls

- **Zip upload loses dotfiles and empty dirs.** "Add files via upload" on GitHub
  dropped `.gitignore` (and every dir without tracked files). After any future
  upload: verify `.gitignore` exists and `git status --short` shows no runtime
  artifacts (KI#1).
- **Workspace files ≠ tracked files.** `git status --short` shows changes
  *vs HEAD*, not what is *in HEAD* — a file present in your working directory
  may not be committed at all. After any structural change, run
  `git ls-files <path>` (or `git ls-files | head -50`) to confirm what is
  actually tracked. This is the diagnostic for KI#1-class losses and for
  "the file exists but tests can't find it" surprises.
- **Doc-loop alarm vs owner-requested research.** Seventeen docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0r is the seventeenth docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n,
  0o, 0p, 0q, 0r; iter-0d was infra). All ref-N backlog items are now
  complete (ref-1 through ref-11, plus the iter-0h cousins: Neighborly +
  Mesa + DF Legends XML); no further ref-N iterations remain.
- **Substance over line count (D-025) + per-ref split (D-026).** The
  400-line cap was a crutch — iter-0i trimmed real depth (XML element
  lists, event-type enumerations, Mesa pseudo-code, DataCollector
  details) to fit. AGENTS §6 cap is 600, but §6.1 is the real law — filler /
  restatements / linker chains / decorative prose are cut always; named
  systems, real field lists, type enumerations, pseudo-code, per-source
  verdicts are never cut to fit the cap. Over cap after a real cruft pass:
  keep, document in worklog. At iter-0j the single-file
  `docs/REFERENCES_DEEP.md` was 737 lines — 4 deep dives with concrete
  field names and type enumerations justified the breach. At iter-0k the
  same content was split into 5 per-ref files in `docs/ref/` (D-026);
  each is 101–244 lines — under the cap by construction. At iter-0l
  `paradox_scripting.md` is 605 lines — 5 over the cap, justified per
  §6.1 (three games × trigger/MTTH/weight/effect/scope/on_action
  subsystems with real field names and ~150+ on_action IDs). At
  iter-0m three proprietary §10 source files (`rimworld.md` 253,
  `l4d_director.md` 245, `alien_isolation.md` 296) — all under
  cap by construction (the closed-source constraint forces
  field-shape-from-public-talks only, not full enumeration). At
  iter-0n four open-licensed event/narrative grammar family files
  (`wesnoth_wml.md` 244, `endless_sky_dsl.md` 228, `ink.md` 212,
  `tracery.md` 217) — all under cap by construction (the pattern-
  not-content rule §0.7 + the JSON/grammar shape lift keeps each
  file to the mechanics layer only). At iter-0o three open-
  licensed roguelike emergence + micro-sim files
  (`brogue.md` 326, `dcss.md` 360, `keeperrl.md` 444) — all
  under cap by construction (the pattern-not-content rule §0.7
  + the shape-lift keeps each file to the mechanics layer
  only; the larger line counts vs iter-0n reflect the deeper
  RNG/scheduler/queue mechanics these three sources carry —
  the §6.1 substance filter protects the depth). At iter-0p
  three open-licensed LLM-agent precedent files
  (`generative_agents.md` 371, `ai_town.md` 345,
  `letta.md` 353) — all under cap by construction (the
  pattern-not-content rule §0.7 + the shape-lift keeps each
  file to the mechanics layer only; the larger line counts
  vs iter-0n reflect the deeper memory hierarchy + retrieval
  + context-window block manager mechanics these three
  sources carry — the §6.1 substance filter protects the depth). At iter-0q
  six open-licensed worldgen data donor + grid math pattern-only files
  (`azgaar_fmg.md` 280, `natural_earth.md` 250, `geonames.md` 345,
  `libtcod.md` 279, `rot_js.md` 347, `red_blob_games.md` 312) — all
  under cap by construction (the pattern-not-content rule §0.7 + the
  shape-lift keeps each file to the mechanics layer only; the larger
  line counts vs iter-0n reflect the deeper worldgen donor + FOV /
  pathfinding / grid math mechanics these six sources carry — the
  §6.1 substance filter protects the depth). At iter-0r six open-
  licensed ECS + event-sourcing + storage-layer pattern-only files
  (`entt.md` 359, `bevy.md` 469, `eventstore.md` 534, `sqlite_fts5.md`
  368, `duckdb.md` 458, `sqlite_vec.md` 383) — all under cap by
  construction (the pattern-not-content rule §0.7 + the shape-lift
  keeps each file to the mechanics layer only; the larger line counts
  vs iter-0q reflect the deeper ECS sparse-set + scheduler +
  event-sourcing + storage-layer mechanics these six sources carry —
  the §6.1 substance filter protects the depth). The STATUS.md
  opening block at iter-0r is 803 lines (over the 600 cap) —
  substance-justified per §6.1 (named systems + real field names +
  type enumerations + per-source verdicts are all substance, never
  cut); documented in worklog.
- **License drift between catalog and index (KI#6, closed iter-0n; pitfall
  persists).** The `REFERENCES_DEEP.md` §2 index table is **not** the source
  of truth for licenses — `REFERENCES.md` (the catalog) is. The index
  restates the license as a one-line convenience column; if the two
  disagree, the catalog wins. iter-0n found two drifts in §2 (ref-5-b
  "CC-BY-SA" vs catalog "GPL-3.0 code; mixed assets"; ref-5-d "CC0"
  vs catalog "Apache-2.0"); both fixed in the same edit. iter-0o
  verified the three new ref-6 rows (AGPL/GPL/GPL shorthand) against
  catalog §2 (AGPL-3.0 (CE) / GPL-2.0+ / GPL-2.0) — no drift this
  iteration. iter-0p caught one drift on ref-7-a (index said
  "(paper)", misleading — the catalog §5 says Apache-2.0 for the
  `joonspk-research/generative_agents` repo; the paper is the academic
  companion, not the license-bearing artefact); fixed in the same §2
  edit that flipped ref-7-a/b/c todo→done with the corrected
  "Apache-2.0 (repo) + paper" annotation. The diagnostic: before
  flipping any ref-N row todo→done, grep the source row in
  `REFERENCES.md` and verify the license column matches the index
  entry. Same pattern as the catalog ↔ synthesis ↔ deep-dive
  anti-drift rule (D-024/D-026): a fact restated in two places
  drifts; the catalog is the owner. Standing pre-flip check added
  to the iter-0o workflow, exercised again in iter-0p, exercised
  again in iter-0q (ref-9-a + ref-9-b "BSD" shorthand → "BSD-3-Clause"
  to match catalog §3 explicit value; ref-9-c Red Blob Games marked as
  "CC-BY (treat as)" — catalog §8 has no license column for knowledge-
  base sources, so this is not catalog↔index drift; the convention is
  documented honestly in the per-ref file, with Amit Patel's explicit
  attribution-request in academic contexts as the basis). iter-0r
  caught TWO drifts in the same §2 edit that flipped ref-10-a/b/c +
  ref-11-a/b/c todo→done: ref-10-c EventStore index said "MIT" vs
  catalog §6 "BSD-3-Clause (≤23.x); ESLv2 from 24.10 — pattern only"
  — fixed in the same §2 edit with the corrected "BSD-3-Clause (≤23.x);
  ESLv2/Kurrent-License-v1 from 24.10 — pattern only" annotation (the
  license history was verified by reading the LICENSE.md commit log on
  master: BSD-3-Clause at tag oss-v23.10.0, ESLv2 from commit 7c85c2944234
  on 2024-09-27, renamed Kurrent License v1 at commit 88f4ff37532f on
  2025-02-11); ref-11-c sqlite-vec catalog said "verify" (the only
  unresolved license in the catalog) + index said "MIT" — verified by
  reading LICENSE-MIT + LICENSE-APACHE + sqlite-dist.toml manifest as
  dual "MIT OR Apache-2.0"; the catalog "verify" status is now RESOLVED
  to dual "MIT OR Apache-2.0", and the matching index drift (index
  "MIT" vs verified dual) was fixed in the same §2 edit. Both drifts
  are KI#6-class pre-flip catches; the standing pre-flip check is now
  exercised across iter-0o/0p/0q/0r — every ref-N batch iteration.
- **Catalog vs deep dives vs synthesis — three places, three jobs.**
  `docs/REFERENCES.md` is the **catalog** (license, URL, phase gating,
  intake rules). `docs/CORE_DESIGN_RESEARCH.md` §2 is the **synthesis**
  (one-line depth primitive + failure mode per source). Per-source
  **deep dives** live in `docs/ref/<source>.md` (one file per source,
  indexed by `docs/REFERENCES_DEEP.md` §2 — D-026; the single-file
  arrangement from D-024 did not scale). Drift rule (AGENTS §3): never
  restate across these three — link only. A future reference detail
  belongs in a per-ref file under `docs/ref/`, not in the catalog or the
  synthesis table.

## Next step

iter-1 · core plumbing is the next functional step: seed, RNG instance, clock,
event queue, JSONL log with header, playscript runner, pack loader for the
drafted `content/tavern_pack/` v0.1. Acceptance criteria in `docs/TASKS.md`.
Owner's blocking answers to Q1–Q3 are absorbed as D-019..D-021 and flip
P2a/P2b and M3/M4/M5 from proposals to accepted iter-3/iter-4/iter-6 scope.
The ref-6 deep dives (Brogue two-stream RNG, DCSS multi-stream RNG +
energy-based scheduler, KeeperRL continuous-time queue + Collective tick
order) are the direct precedents for iter-1 core plumbing. The ref-7 deep
dives (Generative Agents memory stream + retrieval function + reflection
pattern, ai-town reactive-database anti-pattern, letta block-manager +
three-tier memory hierarchy) are the precedents for the phase-1+ brief
layer (track B only, behind the phase-0 gate). The ref-8 deep dives
(Azgaar FMG four-layer architecture + ordered generator pipeline +
`State`/`Campaign` interface shapes, Natural Earth three-scale LOD
ladder + `featurecla` closed enum + semantic versioning, GeoNames
9-class/684-code feature enum + `geoname` table per-feature record +
admin-hierarchy code chain + `alternatenames` table + daily delta
files) are the precedents for phase-5 worldgen + `entities.json` +
`relations.json` P2a + `templates.json` localized name sets + chronicle
rename events. The ref-9 deep dives (libtcod FOV algorithm closed
enum + `TCOD_MapCell` per-tile state + A*/Dijkstra pathfinder +
heightmap pipeline + Mersenne Twister RNG, rot.js `EventQueue`
min-heap + scheduler family [simple/speed/action] + FOV family +
path family + Alea RNG + engine game loop, Red Blob Games hex grid
coordinate algebra + A* pseudo-code + polygon map generation
pipeline [Voronoi + Lloyd + Perlin + watershed + Whittaker biomes +
noisy edges] + relational grid abstraction + Floyd-Warshall pre-
compute) are the precedents for `core/queue.py` + `core/rng.py` +
`core/runner.py` iter-1 plumbing + `sim/systems/perception.py` +
`sim/systems/movement.py` iter-2/iter-3 systems. The ref-10 deep
dives (entt C++ ECS sparse-set blueprint + `basic_organizer` task
DAG + `sigh`/`sink`/`connection` RAII hooks + `meta_type`/
`meta_factory` reflection, Bevy Rust ECS + scheduler + `Messages<M>`
double-buffered ring [renamed from `Events<T>` in v0.20-dev] +
`Command`/`CommandQueue`/`Commands` deferred mutation + `States`
FSM, EventStoreDB canonical event-sourcing mechanics +
`ExpectedVersion` OCC constants + `SystemNames.SystemStreams`
`$all` + `StreamMetadata` retention knobs + tombstone + `Scavenger`
offline compaction) are the precedents for `core/store.py` +
`core/queue.py` + `cli/` Intent → Event validation front-door +
INV-5 corrections-as-new-events + offline scavenge + `sim/systems/
__init__.py` Schedule + `ambiguous_with` build-time conflict detection
+ `sim/systems/` phase control (States deferred FSM). The ref-11
deep dives (SQLite FTS5 `CREATE VIRTUAL TABLE USING fts5` + `bm25`
+ `highlight`/`snippet` + `NEAR`/`*`/`^`/`+` query operators +
`rebuild` INV-1 mechanism + segment b-trees + `fts5vocab`
introspection + 5 shadow tables, DuckDB `STANDARD_VECTOR_SIZE =
2048` DataChunk + `read_json_auto()`/`read_ndjson_auto()` TVF +
`CopyFunction("parquet")` + `Appender` API + `WINDOW_LAG`/
`WINDOW_LEAD` window functions + per-column compression [offline
chronicler pipeline; NOT runtime — D-012], sqlite-vec `vec0`
virtual-table module + `vec_distance_cosine` + matryoshka
`vec_slice`/`vec_normalize` + `vec_quantize_binary` 32× compression
+ loadable C extension [phase 4 only, conditionally-loaded — phase
0 stays stdlib-only with pure-Python `cosine_sim()` fallback]) are
the precedents for `core/storage.py` SQLite index + `brief/
assembler.py` bm25 ranking + `render/` highlight/snippet + the
offline `chronicler` pipeline (phase-3+ scale) + phase-4 retrieval
layer (FTS5 + sqlite-vec hybrid). **All ref-N backlog items are now
complete** — ref-1 through ref-12 (ref-12 = UAP, iter-0s), plus the
iter-0h cousins (Neighborly + Mesa + DF Legends XML). The doc-loop alarm
now counts 18 consecutive docs iterations; iter-0s was admitted under the
documented exception (fresh external source + owner request). **iter-1 is
unconditionally the next iteration** (functional code, not docs); no
further ref-N iterations, spec writing or doc polish without a fresh owner
request.
