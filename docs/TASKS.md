# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2. Done-detail lives in git
> history + `worklog.md` + the owning docs — never restated here (KI#7
> cleanup, iter-0v). Day-tags removed per D-029 (calendar dropped); the
> build sequence is iteration-counted (`MVP_SCOPE.md` §17).

## Track A — main (simulator, no LLM)

> Phase 0 closed (gate PASS, iter-6; audit-clean iter-6a). Phase 1
> (narrator over the log) is open — architecture owner:
> `docs/blueprint/phases.md` §1; spec triggers fire at phase-1 start
> (`docs/SPECS_BACKLOG.md`). INV-4 holds until the narrator-boundary
> iteration explicitly opens it (AGENTS §8 owner checkpoint).

### iter-7 · phase-1 intake — done

DECISIONS collapsed 46→30 per D-034 (ID-preserving family merges);
TASKS.md regained the "what next" ownership (the phase-1 plan lived
only in STATUS "Next step" — drift); intake audit fixes KI#25/26/27.
Detail: `worklog.md` iter-7 + `STATUS.md`.

### iter-8 · BRIEF_SPEC + brief assembler — done

`docs/BRIEF_SPEC.md` written (trigger fired; six-block pipeline, two-level
budgets, eviction contract, voice-isolation law, just-in-time deferrals);
`brief/assembler.py` — the deterministic assembler as pure functions of the
log; `rules.json::brief` pack contract + `core/pack.py` lint. Detail:
`worklog.md` iter-8 + `docs/BRIEF_SPEC.md`.

### iter-9+ · phase-1 continuation — todo (sequenced after iter-8)

- `VALIDATION_SPEC.md` trigger fires (fact transaction, ExpectedVersion
  OCC, ≤2 regens, INSUFFICIENT_DATA default) + the validator's LLM-free
  half (proposal shaping, stale-version rejection, golden-set plumbing).
- The scene-ledger LLM-free half (D-048, mechanism
  `docs/blueprint/phases.md` §1): `brief/ledger.py` (entry shape,
  discrete lifecycle, laundering refusal, contradiction retirement) +
  the `scene_texture` 7th brief block reading it + fixture-shaped
  narrator deltas under `tests/fixtures/` + pack lint (block budget).
  Sequenced after VALIDATION_SPEC's LLM-free half — the delta grammar
  informs the fixture shapes. BRIEF_SPEC §9 deferral flips to written.
- The narrator LLM boundary itself is a separate owner-gated iteration
  (AGENTS §8; local inference per `docs/TECH_NOTES.md` §1 — degradation
  ladder L12 from day one); it now also carries the scene-ledger live
  wiring: the structural texture delta in the narrator call, the
  texture↔canon precedence checks, the laundering-refusal flags, and
  the texture noun-test in the pack `requires` closed set.

### Phase-1 tuning backlog (post-assembler, owner-gated)

- `tune-1` rest action as pack data (player fatigue is monotonic over
  long waits — KI#4/balance observation) + the D-045(b) importance-rule
  knob (hooks on story-critical events, NOT `tale_gate`); both refresh
  the 1000-sim baseline when tuned.

### iter-6 · gate — done (phase-0 verdict: PASS)

Phase-0 gate closed; full evidence in `worklog.md` iter-6 + the
`docs/TEST_PLAN.md` spec. Track A was feature-frozen at phase-0 scope;
phase 1 (narrator over the log) opened per `docs/ROADMAP.md` §2.

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
- `balance-1` 1000-headless-sim distribution harness — DONE iter-6:
  `scripts/balance_harness.py` runs the gate playscript 1000× across
  seeds 100–1099 (director off), folds each log through
  `core/metrics.py`, emits a distribution table for M1–M5 +
  emergent_chains + suspicion peaks per NPC + destroyed-locations.
  Baseline (1000 seeds): M5 p50=0.77, emergent_chains p50=20, M3_mean
  p50=13.81, M1 p50=0.24 — full table at
  `output/balance_1000_seed100_off.txt` (gitignored runtime artifact;
  reproducible). KI#4 closed.
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

- iter-8a · 2026-08-28 · scene-ledger design pass (owner-requested
  continuity question: long scenes lose narrator-invented texture —
  the brief is a pure function of the log and free texture had no
  home): `docs/ref/agent_memory_atlas.md` written (the owner-supplied
  151-system memory survey distilled: 7 marks, 22 patterns, per-pattern
  take/adapt/reject for canonsim; MIT verified via GitHub API); the
  scene ledger designed into `docs/blueprint/phases.md` §1 (D-048:
  session-scoped append-only mediator-owned ledger; discrete states;
  canon outranks texture; promotion only through the intent door;
  laundering refusal; no TTL; dies with the session); spec triggers
  synced (SPECS_BACKLOG VALIDATION_SPEC row + BRIEF_SPEC §9 deferral);
  TASKS sequencing added. Docs-only — the D-022 owner-request exception
  (no doc-loop: iter-8 was code-heavy). 329 tests green, ruff clean,
  fixture byte-identical.
- iter-8 · 2026-08-28 · BRIEF_SPEC + brief assembler: `docs/BRIEF_SPEC.md`
  (trigger fired at phase-1 start — six-block pipeline, two-level budgets
  soft-fill/hard-ceiling, whole-block eviction with `[truncated:N]`
  markers and the never-drop-directives law, voice-isolation L2, §9
  just-in-time deferrals incl. the max_items ranking-cap distinction);
  `brief/assembler.py` — the deterministic assembler, pure functions of
  the log, zero RNG (byte-identity on the golden fixture across calls,
  PYTHONHASHSEED-independent); `rules.json::brief` pack contract
  (budgets + directives/lore/exemplars text) + `core/pack.py::_brief`
  lint (BRIEF_BLOCK_IDS closed enum). D-047 recorded. 329 tests green
  (+30), ruff clean, golden fixture byte-identical.
- iter-7 · 2026-08-28 · phase-1 intake (owner-requested retrospective +
  plan reorganization): DECISIONS collapsed 46→30 per D-034
  (ID-preserving family merges, 55KB→20KB); TASKS.md regained the
  what-next ownership (phase-1 sequence: iter-8 BRIEF_SPEC + brief
  assembler, iter-9+ validator, tune-1 rest/importance knobs); intake
  audit fixes: KI#25 stale `_enqueue_autonomous` docstring (beat-tick
  vs entry-tick), KI#26 dead-parameter family (`Director.releases`
  knowledge, `briefing_draft` projection, `urgency_intents` beat_tick,
  `_axis_deltas` pack — L14, the KI#24 family), KI#27 README drift
  (298→299, "systems land iter-2"), KI#28 residual false §9 citation in
  AGENT_NAVIGATION (the KI#23 family). KI#21 deleted (closed >2 iters).
  299 tests green, fixture byte-identical, ruff clean.
- iter-6a · 2026-08-28 · owner-requested code audit of iter-5/6: every
  gate claim reproduced (298 green, the 1000-sim baseline EXACTLY, T8
  OFF = 26 chains, PYTHONHASHSEED-independent chronicle); 3 KIs fixed —
  KI#22 TEST_PLAN/test-docstring drift (seed 32→125, 24→26 chains, M2
  formula, §6 filename), KI#23 scripts/ outside the executable
  invariants + the false "AGENTS §9" citation (D-046; PACKAGE_DIRS +=
  scripts + closure test + CLI-class print exemption), KI#24 dead
  fold_events removed; KI#17–20 deleted (closed >2 iters); FAQ 24→20.
  299 tests green, ruff clean, fixture byte-identical.
- iter-6 · 2026-08-28 · phase-0 gate: `docs/TEST_PLAN.md` spec (T0–T8 +
  M1–M5 + gate protocol + UAP crosswalk); `core/metrics.py` (M1–M5 +
  emergent-chain count as pure functions of the log); T1 fixture-
  regeneration guard; T8 single-factor A/B (≥3 emergent chains OFF,
  director_0000 fires ON); `scripts/balance_harness.py` (KI#4 close,
  1000-sim distribution); `tests/playscripts/day1_full.json` (gate
  playscript, seed 125). Verdict PASS — all `MVP_SCOPE.md` §16 exit
  criteria met, no kill-criteria hit. 298 tests green, fixture
  byte-identical, ruff clean.
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
