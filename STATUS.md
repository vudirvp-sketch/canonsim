# STATUS — canonsim

Iteration: 0t (owner-requested: ref-13 — Live Character Guide deep dive, fresh external source; character-card methodology donor: SPINE/Price/observability → pack lint + brief-layer injection grammar; license clean: MIT, LICENSE file verified) · Phase: 0 — simulator without LLM · Date: 2026-08-27

iter-0t is the **ref-13 solo deep dive** — the owner's own
`live-char-guide`, a fresh external source admitted by the documented
condition (fresh source + explicit owner request — same D-022 logic as
iter-0s). Deliverable: `docs/ref/live_char_guide.md` (+ catalog §9 row,
`REFERENCES_DEEP.md` §1/§2 rows, `CORE_DESIGN_RESEARCH.md` §2 row,
SPECS_BACKLOG BRIEF_SPEC/PACK_SPEC sketch clauses, TASKS ref-13 + iter-0t
lines, this header, worklog entry — 8 files, the same mandated set as
iter-0s).

**What the guide is** (read in full: `docs/canon/` parts 00–10 + 4
appendices, ~4700 lines — the repo's declared single source of truth for
content; `data/character_schema.json` 684): a methodology for building RP
character cards for 12B–32B+ models (SillyTavern-compatible) that treats
the card as a **behavioral engine** — every element must produce an
observable action, never decorate a description. Pipeline: SPINE
(GHOST→LIE→FLAW→NEED→WANT — a causal chain of observable units: concrete
past event → quoted false belief → concrete flawed behavior → blocked true
need → conscious goal compatible with the lie, in tension with the need;
§4.9 consistency checklist = a causality audit) → Behavioral Anchors
(Trigger→Action→Price, where **Price = immediate, physical, same-scene
observable cost**; "will regret it later" is banned as a Price; FLAW-linked
anchors mandatory; one anchor = one atomic T→A→P link) → Embodiment
(State→Body→Sensor→Speech — every state must surface physically before
speech) → Voice Isolation (linguistic voice only in Examples; the model is
a pattern matcher, not a rule executor; influence hierarchy on 12B: recent
chat ~85%, examples ~10%, description 0%) → System Prompt assembly (7 CORE
DIRECTIVES: Show Never Tell / Embodiment First / Spatial & Anatomical Lock
/ Environmental Reactivity / Influence Boundary / Consequence Driven /
Pre-Generation Filter) → 15 anti-patterns (symptom→cause→fix) → countable
diagnostics (6 test scenarios, 6 success metrics, one-change rule, 5+14
pre-deploy checks). OCEAN as validator with a 1–2 extreme-poles budget;
Lorebook as injection scheduling (depth/probability/cooldown/sticky/
range-cascade), not lore storage. Machine-readable mirror:
`character_schema.json` (spine.want/need/flaw required; anchors 3–12 with
trigger/action/price required).

**Why it matters to us** — the load-bearing transfers:
1. **External validation of the observability law, round two.** "Every
   element must produce an observable action" = the causal-density
   checklist / dead-event law (`MVP_SCOPE.md` §15) arriving from the
   prompt side; their AP-2 (anchor without Price) is our "tried to steal —
   failed, the world did not change". After UAP §0.6 this is the second
   independent convergence on "quality must be countable over
   observables" — now at character granularity.
2. **Price = the immediate half of consequence.** D-005 owns the deferred
   half (hooks seeded at event time); the guide adds: a socially
   meaningful behavior must carry a same-scene observable marker — a
   knowledge record or a perceivable state token. Iter-2 pack-rule
   pattern + causal-density checklist wording; no schema change.
3. **Influence Boundary as a candidate iter-2/3 architecture rule.** NPC
   behavior functions read **own state + own knowledge only**; other
   entities' internal states enter exclusively via perception of their
   observable markers (embodiment as the states→observables mapping). The
   guard cannot react to the drunkard's intoxication field — only to
   slurred speech arriving as a `heard` record. Closes system 5 (states)
   into the perception→knowledge chain; sharpens T3/blind-NPC. Adopting it
   as law = owner call at iter-2/3 design time.
4. **Brief-layer law for BRIEF_SPEC (track B, phase 1).** Facts travel as
   structured tokens, never style descriptions; voice lives in template
   exemplars; recency-dominant hierarchy + AN geometry (position 3–5
   messages from the end, 100–200 tokens, every 5–10 messages) +
   lorebook scheduling params (depth/probability/cooldown/sticky/range)
   = the injection-scheduling grammar phase 1 needs.
5. **AP catalog → PACK_SPEC lint vocabulary (phase 6):** want/need tension
   + flaw rootedness (AP-9), flaw→rule connectivity (AP-8), clone-NPC
   check (AP-11), rule atomicity (AP-15), pack budgets (AP-1), rule
   contradiction (AP-13) — converging with the UAP teleology gate.
6. **Test discipline:** 6-scenario battery → playscript design; 6 success
   metrics → log-computable analogs (M4 novelty, state_changes+hooks
   presence, actor discipline); one-change rule = single-factor A/B on
   identical seed (T1/T8) stated as experimental method.

**What we adapt (INV-3-safe routes):** SPINE/OCEAN/stress types as pack
metadata + modifier tables in `rules.json` (spine-shaped entity records
referenced by generic rules — the spine-hooks-in-core-code variant is an
INV-3 violation, rejected); relation drift as a fold over price-bearing
events (Consequence Driven → iter-3/4 candidate pattern); GHOST-Layers
degradation counter → counted-event capability loss (phase 4); their
percentages stay shape, not thresholds (iter-6 baseline law — the guide
itself disclaims them as qualitative markers).

**What we reject** (inversions of our invariants): prompt-compensation
machinery (token budgets, PP=0, format locks, 4K fallbacks, Script Tax —
patch LLM limits phase 0 does not have; track-B shape only); psychometrics
as runtime systems (OCEAN/Enneagram/MBTI stay authoring-side pack data —
INV-3); false memory (unfalsifiable memory injection) and fatigue
emulation (hidden context degradation narrated as trait) — the INV-1/INV-5
inversions; human-judged gates (our law: log-computed M1–M5, humans only
at T7); their single-character focus offers nothing for systems 2/4/6
(epistemology remains DF Legends / Paradox territory).

**License: clean.** MIT LICENSE file present and read in full
(2026-08-27) — unlike UAP, content and patterns are both liftable with
attribution. Recorded in catalog §9 + index §2 + the ref file.

**Doc-loop accounting:** 19th consecutive docs iteration. Exception is the
documented one (fresh external source + explicit owner request — D-022
logic, same as iter-0s). The alarm condition stands: **iter-1 is
unconditionally the next iteration** — no further ref-N, no spec writing,
no doc polish without a fresh owner request.

**iter-0s closing summary** (full detail: git history + worklog entry):
ref-12 UAP solo deep dive delivered (`docs/ref/uap_audit.md`:
countable-criteria rubric donor — external validation of the §15 metric
law; 7-hole → T2/T3/D-005 crosswalk; phase-1 harness prompt + resilience
patterns; pack-lint vocabulary; negative on LLM-as-judge, regex bridges,
free-form canon); license catch stands — no LICENSE file in the UAP repo
(reference only until fixed).

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
- **Doc-loop alarm vs owner-requested research.** Nineteen docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022) — but only under the documented
  condition: a fresh external source + an explicit request. iter-0t is the
  nineteenth docs iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j,
  0k, 0l, 0m, 0n, 0o, 0p, 0q, 0r, 0s, 0t; iter-0d was infra); iter-0s
  (UAP) and iter-0t (live-char-guide) were each admitted under that
  condition. All ref-N backlog items are complete — ref-1 through ref-13
  plus the iter-0h cousins (Neighborly + Mesa + DF Legends XML); no
  further ref-N iterations remain without a fresh external source.
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
  cut); documented in worklog. At iter-0s the STATUS opening block
  was cut to ~307 lines by a cruft pass (iter-0r detail moved to git
  history) and `uap_audit.md` is 212 lines; at iter-0t
  `live_char_guide.md` is 304 lines — both under cap by construction
  (the pattern-not-content rule §0.7 keeps each file to the
  methodology layer only).
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
  iter-0t verified ref-13 (MIT, LICENSE file read in full) against the
  new catalog §9 row — no drift; the check now covers the two
  owner-repo sources (UAP, live-char-guide) as well.
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
layer (FTS5 + sqlite-vec hybrid). The ref-13 deep dive (SPINE observable
units + Trigger→Action→Price immediate observables; voice isolation /
pattern-matcher law + recency-dominant influence hierarchy + lorebook
depth/probability/cooldown/sticky/range scheduling; 15-AP lint vocabulary;
Influence Boundary — NPC behavior reads own state + own knowledge only)
is the precedent for iter-2 outcome observables (price markers), the
iter-3/4 relation-drift-as-price-fold candidate pattern, the phase-1
brief layer (BRIEF_SPEC — facts as structured tokens, style in template
exemplars) and phase-6 pack authoring lint (PACK_SPEC AP crosswalk).
**All ref-N backlog items are now
complete** — ref-1 through ref-13 (ref-12 = UAP, iter-0s; ref-13 = Live
Character Guide, iter-0t), plus the
iter-0h cousins (Neighborly + Mesa + DF Legends XML). The doc-loop alarm
now counts 19 consecutive docs iterations; iter-0s and iter-0t were each
admitted under the documented exception (fresh external source + owner
request). **iter-1 is
unconditionally the next iteration** (functional code, not docs); no
further ref-N iterations, spec writing or doc polish without a fresh owner
request.
