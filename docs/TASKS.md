# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2. Done-detail lives in git
> history + `worklog.md` + the owning docs — never restated here (KI#7
> cleanup, iter-0v). Day-tags removed per D-029 (calendar dropped); the
> build sequence is iteration-counted (`MVP_SCOPE.md` §17).

## Track A — main (simulator, no LLM)

### iter-6 · gate — todo (next)

- Full T1–T8 (T1 with the fixture-regeneration guard —
  `docs/blueprint/phase0.md` §6); director-off A/B on identical seed +
  playscript; M1–M5 metric report (thresholds set from baseline); manual
  playtest; phase-0 verdict in `worklog.md`.
- **M3 causal chain length** (D-019, P1b): mean/median depth of the `cause`
  chain per event, from the log alone.
- **M4 novelty/repetition** (D-019, P1c): rate of repeated (type, actor)
  bigrams; share of distinct `knows` tokens. RimWorld's repetitive-tale
  problem, measured.
- **M5 non-PC event share** (D-019, P1d): events with actor ≠ player /
  all events. "World not player-centered" (Kenshi/RimWorld lesson) made
  measurable at the director-off gate.
- AC: exit criteria `MVP_SCOPE.md` §16 all hold — or kill-criteria documented
  honestly.

## Track B — background (evenings, foreign canon)

### bg-1 · DF export pipeline — todo

- DF Classic (free) + DFHack `exportlegends info` → 2–3 worlds → XML → SQLite
  parser. Watch for: HEX errors after fortress play (export from clean legends
  mode), hundreds of MB per large world, translated-name layers.
- AC: parser loads a world into SQLite; pitfalls recorded in
  `docs/TECH_NOTES.md` §3.

### bg-2 · event taxonomy — todo

- 100–300 interesting events across ~16 types (birth, death, murder, theft,
  betrayal, artifact creation, site destruction, war, journey, captivity,
  escape, founding, item loss, madness, transformation, catastrophe); per
  event: participants, place, cause, witness, long-term consequence,
  expressibility in our ontology → `docs/TAXONOMY.md`.
- AC: ≥100 entries. Honest note baked in: causality is *reconstructed* from
  `event_collections` + role fields, not parsed.

### bg-3 · briefer spike — todo

- Mini-briefer "tell battle X from figure Y's POV, knowing only Y's own
  records" + reverse validation (invented-facts count, regeneration count) +
  retrieval stress test (tens of MB of XML).
- AC: harness runs; numbers in `docs/TECH_NOTES.md`. Expectation to keep
  honest: DF canon is macro-dense and micro-empty — this validates briefer
  *mechanics*, not micro-event interestingness (measure that on our own dry
  chronicle).

### bg-4 · cost notes — todo

- Park et al. 2023 + "Generative Agent Simulations of 1,000 People" (2024)
  figures → `docs/TECH_NOTES.md` cost section.

## Infra backlog (pick by need)

- `ci-1` GitHub Actions: pytest + ruff on push (`PYTHONHASHSEED=0`, pinned
  Python).
- `qa-1` mypy --strict on `core/` (owner-approval-gated: dev tooling is
  capped at pytest + ruff — AGENTS §8/§10; D-031 parks the candidate here.
  The type-discipline values are law from iter-1 via
  `docs/blueprint/phase0.md` §1; the tool is optional).
- `perf-1` 10k-tick timing profile (target: seconds, not minutes).
- `balance-1` 1000-headless-sim distribution harness: playscript runner with
  sampled intents (seed-varied) → distribution plots of `suspicion` and
  `fire_spread` over ticks. Validates that `rules.json` thresholds are tuned,
  not guessed. Uses T1-determinism, no new infra. Prerequisite for iter-6
  M-baseline (KI#4).
- `doc-1` VISION freeze review after the phase-0 verdict.
- `doc-2` REFERENCES.md license/URL re-verification, quarterly (alongside the
  TECH_NOTES review).
- `pack-1` Grim tavern pack candidate (post-gate; `PACK_SPEC.md` trigger —
  phase 6 or a 2nd setting): the romance/intimacy/coercion line as **pure
  pack data** — relation axes (`attraction`/`intimacy`/`loyalty`), status
  axes (`shame`/`anger`), a flirt→proposition action ladder,
  `consented`/`coerced` crafted knowledge records (D-008 pattern), seeded
  consequence hooks (jealousy, exposure, regret), dark templates, item
  extensions. Darkness levers per D-030; zero core change (axis-blind core;
  event vocabulary per pack, EVENT_SCHEMA §11). Distillation source:
  D-030 + the PACK_SPEC sketch row. Blocked until: phase-0 gate passed.
- `pack-2` Arson-on-ashes guard (iter-2a audit note): arson on a
  fully-burning or destroyed location currently logs a no-ignition
  success (spot=None, world unchanged). Candidate fix = a pack
  precondition (e.g. an `unburning_spot`/`not_destroyed` test in the
  closed set) when a precondition slot is next needed — most naturally
  iter-3+, once crime reactions make arson attempts meaningful facts.
- `ref-N` Reference deep dives — the plan table and the per-file index live
  in `docs/REFERENCES_DEEP.md` §1/§2 (single owner). All ref-1..ref-13 items
  are done — status one-liners:
  - ref-1 DF worldgen — done (iter-0i) → `docs/ref/df_worldgen.md`
  - ref-2 C:DDA data/json — done (iter-0j) → `docs/ref/cdda_data_json.md`
  - ref-3 Paradox scripting — done (iter-0l) → `docs/ref/paradox_scripting.md`
  - ref-4 RimWorld + L4D + Alien — done (iter-0m) → `docs/ref/{rimworld,l4d_director,alien_isolation}.md`
  - ref-5 Wesnoth + Endless Sky + ink + tracery — done (iter-0n) → `docs/ref/{wesnoth_wml,endless_sky_dsl,ink,tracery}.md`
  - ref-6 Brogue + DCSS + KeeperRL — done (iter-0o) → `docs/ref/{brogue,dcss,keeperrl}.md`
  - ref-7 Generative Agents + ai-town + letta — done (iter-0p) → `docs/ref/{generative_agents,ai_town,letta}.md`
  - ref-8 Azgaar + Natural Earth + GeoNames — done (iter-0q) → `docs/ref/{azgaar_fmg,natural_earth,geonames}.md`
  - ref-9 libtcod + rot.js + Red Blob — done (iter-0q) → `docs/ref/{libtcod,rot_js,red_blob_games}.md`
  - ref-10 entt + Bevy + EventStore — done (iter-0r) → `docs/ref/{entt,bevy,eventstore}.md`
  - ref-11 SQLite FTS5 + DuckDB + sqlite-vec — done (iter-0r) → `docs/ref/{sqlite_fts5,duckdb,sqlite_vec}.md`
  - ref-12 Universe Audit Protocol — done (iter-0s) → `docs/ref/uap_audit.md`
  - ref-13 Live Character Guide — done (iter-0t) → `docs/ref/live_char_guide.md`
- Candidates (owner-request only — D-022 law: no doc pass without a fresh
  owner request; both are synthesis-only today, cited via
  `CORE_DESIGN_RESEARCH.md` §2 and marked as such in the blueprint donor
  stacks):
  - `ref-14` The Sims — proprietary; patterns-from-papers only (D-015).
  - `ref-15` Prom Week — academic paper + GDC talk; no code repo.

## Done

- iter-5 · 2026-08-28 · chronicle & CLI: deterministic tracery engine
  (ShufflePool no-immediate-repeat, modifiers, save/restore, ink
  conditionals — cosmetic stream only) + the chronicle as a pure
  function of the log (day headers, importance gate as pack data,
  scene card, ungated per-entity views) + CLI (batch
  play/chronicle/state/replay + interactive session: look, wait N,
  directors on|off, seed); loop factored open/run_steps/close — a
  session equals the batch run byte-for-byte; templates completed into
  the grammar (KI#21); 264 tests green, fixture byte-identical.
- iter-4a · 2026-08-28 · owner-requested code audit of iter-3/4: probes
  (60-seed sweep × director on/off, T1/T2, crafted records — 124 runs
  clean); KI#17 autonomous completions never advance the playscript;
  KI#18 caught→suspect downgrade guarded by the status_values
  progression; KI#19 reset_on_rotation implemented (rotation_resets +
  per-axis decay baseline); KI#20 dead pack keys removed; D-041;
  225 tests green, fixture byte-identical.
- iter-4 · 2026-08-28 · director + goal ticker: consequence buffer +
  triggers (time / place / threshold) + narrative entropy (P2e:
  sum of seeded-hook weights + global suspicion + visible threats,
  observable state only — L6) + stagnation release (lowest-threshold
  hook wins) + director on/off switch; P2b goal ticker (D-021, NPC
  probability rolls through the intent door — M5 non-PC share
  non-trivially non-zero by construction); states decay passes
  deferred from iter-3 (fatigue/intoxication/fear proportional to
  elapsed ticks, injury never decays — T4); arrest resolution
  (evasion_vs_pursuit → arrest_resolved, `crime_status → caught`
  irreversible); D-038/D-039/D-040 recorded; DIRECTOR_SPEC.md written
  (trigger fired). 219 tests green, golden fixture byte-identical.
- iter-3 · 2026-08-28 · knowledge, relations, expectations: derived
  KnowledgeView + telling reaction (P2c, salience + acceptance), crime
  reactions (ev_0007 shape on the reacting system; novelty rule), watch
  rotation + briefing spread (D-006), P2a pair map, P2d expectation
  violations (cause-chained to the axis-specific mover), movement
  sightings, natural OCC e2e trigger; KI#3/KI#12 closed; T3 suite; fixture
  regenerated. 187 tests green.
- iter-2a · 2026-08-28 · owner-requested code audit of iter-1/2: 4 KIs
  found+fixed (drop desync + `_commit` pre-write gate D-035;
  next_log_path truncation; pack-lint gaps; parallel spread passes →
  per-layer singleton + shared causes D-036), repeat smoke/burnout
  silent, KI#11 deleted; 155 tests green, baselines byte-identical.
- iter-2 · 2026-08-28 · actions: the 12 resolvers + registry, pack-driven
  preconditions/checks/knowledge templates, intent OCC + lifecycle
  (INTENT_SCHEMA.md), scheduler DAG, generic transition engine (fire
  chain), INV-3 stoplist; steal/arson/talk = facts with records; T5
  partial (rejections are logged no-ops). 148 tests green.
- iter-1 · 2026-08-28 · core plumbing: RngBank, clock, queue, JSONL log +
  header, fold/projection, pack loader + lint, playscript runner; T0/T1
  minimal + architecture fitness; KI#10/KI#5 closed, D-032..D-034 recorded.
- iter-0 · 2026-08-25 · docs & tooling bootstrap.
- iter-0b · 2026-08-25 · docs review + external source catalog (`docs/REFERENCES.md`).
- iter-0c · 2026-08-25 · REFERENCES rev v2 merge (D-017) + `content/tavern_pack/` v0.1 drafted.
- iter-0d · 2026-08-25 · infra restore: `.gitignore`, package skeleton, smoke tests (KI#1/KI#2).
- iter-0e · 2026-08-25 · `docs/CORE_DESIGN_RESEARCH.md` (synthesis, depth equation, P1–P3, Q1–Q4).
- iter-0f · 2026-08-25 · manifesto absorption (D-018): BRIEF/VALIDATION sketch clauses, P3e psychological_echo, STATUS FAQ git-ls-files pitfall.
- iter-0g · 2026-08-25 · research pass: Q1–Q3 absorbed (D-019..D-021); KI#3–KI#5 opened.
- iter-0h · 2026-08-26 · `docs/REFERENCES_DEEP.md` + D-024 anti-drift policy; ref batch 1 (Neighborly, Mesa, DF Legends XML).
- iter-0i · 2026-08-26 · ref-1 DF worldgen solo dive.
- iter-0j · 2026-08-26 · ref-2 C:DDA solo dive + cap policy rewrite (D-025).
- iter-0k · 2026-08-26 · per-ref split into `docs/ref/` (D-026).
- iter-0l · 2026-08-26 · ref-3 Paradox scripting solo dive.
- iter-0m · 2026-08-26 · ref-4 pacing trio dive (RimWorld, L4D, Alien).
- iter-0n · 2026-08-26 · ref-5 event/narrative grammar family dive.
- iter-0o · 2026-08-26 · ref-6 roguelike emergence trio dive (Brogue, DCSS, KeeperRL).
- iter-0p · 2026-08-26 · ref-7 LLM-agent precedents dive (GA, ai-town, letta).
- iter-0q · 2026-08-26 · ref-8 + ref-9 six-file batch (worldgen data + grid math).
- iter-0r · 2026-08-26 · ref-10 + ref-11 six-file batch (ECS/event-sourcing + storage).
- iter-0s · 2026-08-27 · ref-12 UAP webapp dive (rubric + 7-hole crosswalk).
- iter-0t · 2026-08-27 · ref-13 live-char-guide dive (SPINE/Price/AP lint).
- iter-0u · 2026-08-27 · references distillation: `docs/BLUEPRINT.md` + `docs/blueprint/{phase0,phases}.md` (D-027 — 12-resolution ledger + laws + build index).
- iter-0v · 2026-08-27 · owner-requested audit patches: INV-2 rewritten per D-028 (RngBank law wording; TASKS/TECH_NOTES/MVP_SCOPE synced); 18 audit resolutions landed as blueprint sub-clauses (DAG language, intent OCC + lifecycle, price precursor, eviction contract, retrieval precedence, reflection provenance, copy-from cycle contract, ShufflePool, prune_window, director rejection + per-run scope, T1 fixture guard, phase-0 pack lint, event-vocabulary-per-pack); KI#8 opened/closed; KI#7 resolved (worklog trimmed to cap, TASKS done-collapsed).
- iter-0w · 2026-08-27 · owner-requested post-reference concept realignment: D-029 — digestion complete, skeleton (phases 0–6, 3 layers, INV-1..5) confirmed, blueprint = the mechanics owner; KI#9 calendar/lifecycle drift fixed (sprint calendar dropped → iteration-counted, CORE_DESIGN_RESEARCH absorbed, ROADMAP §2 blueprint pointer, README Status refreshed).
- iter-0x · 2026-08-27 · owner-requested reference-influence traceability audit: verdict "load-bearing" recorded in STATUS (4-place chain verified — docs/ref/ → synthesis → blueprint → TASKS/SPECS clauses; ledger-term spot-greps all land); FAQ gains the ref-graveyard grep diagnostic; no code.
- iter-0y · 2026-08-27 · owner-requested content-principles pass: D-030 (darkness = architecture, not content scripts; phase-0 pack unchanged; grim line = post-gate `pack-1`); PACK_SPEC sketch + TASKS synced; KI#7/KI#8 deleted (closed >2 iterations); no code.
- iter-0z · 2026-08-27 · owner-requested quality round: D-031 — INVARIANT-CORE v3 + Elegant Solutions absorbed surgically (D-018 pattern): L13/L14 laws (BLUEPRINT §2), phase0 §1 type discipline + fitness test + fail-fast, §2 ActionResolver registry, §6 negative tests, AGENTS §4 INV-1 privilege line + §9 quality bullet, stack freeze through phase 2, mypy parked as owner-gated `qa-1`, TECH_NOTES §7 log-as-stream, REFERENCES §15 principle donors; KI#9 deleted; no code.
