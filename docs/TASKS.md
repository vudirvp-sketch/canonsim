# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2. Done-detail lives in git
> history + `worklog.md` + the owning docs — never restated here (KI#7
> cleanup, iter-0v). Day-tags removed per D-029 (calendar dropped); the
> build sequence is iteration-counted (`MVP_SCOPE.md` §17).

## Track A — main (simulator, no LLM)

### iter-1 · core plumbing — todo

- Seed → RngBank (RNG-1, INV-2 per D-028): one master seed; named streams
  deterministically derived (`stable_hash(f"{seed}:{stream}")`, sha256-based)
  — `substantive` + `cosmetic` in phase 0; integer clock; `heapq` queue
  keyed `(tick, sub_order, actor_id)`; JSONL append-only writer with header
  (no wall-clock); playscript runner (seed + ordered intents); pack loader
  with the phase-0 minimum lint (orphan refs, closed enums) for the drafted
  `content/tavern_pack/` v0.1 (entities from `MVP_SCOPE.md` §4 — that table
  is the source of truth; pack data landed in iter-0c).
- Tests: T0 schema validation (the EVENT_SCHEMA example is a fixture; the log
  header shape per EVENT_SCHEMA §1 is validated as a separate fixture), minimal
  T1 (two runs byte-identical), smoke boot.
- AC: world creates from seed; an event writes; a playscript plays end-to-end;
  `pytest -q` green.

### iter-2 · actions — todo

- The 12 actions with checks/outcomes/durations (`MVP_SCOPE.md` §7);
  pack-driven preconditions; event emission for each; INTENT_SCHEMA (with
  `based_on_event_seq` OCC — `docs/blueprint/phase0.md` §2); scheduler DAG
  with `reads`/`writes` annotations; INV-3 grep stoplist test.
- AC: steal / arson / talk = facts in the log with knowledge records;
  impossible stays impossible (T5 partial).

### iter-3 · knowledge + relations + expectations — todo

- Knowledge records; transfer with fidelity decay; suspicion / relations
  updates; watch-change transfer; NPC memory driving behavior (guards act on
  suspicion thresholds).
- **P2a NPC↔NPC relations** (D-020): sparse pair-keyed relation map — rumor
  acceptance already weighs trust, trust now has a data home; enables guard
  coordination and non-PC story lines.
- **P2d expectation_violation** (KI#3): behaviour rules in `rules.json`
  generate per-NPC expectations from schedule + position; perception
  compares expected vs observed; mismatch emits an `inferred`-channel
  knowledge record (e.g., `purse_missing_from_bar`). No schema change —
  uses the existing `inferred` channel. Suspicion-from-absence now has a
  legitimate trigger.
- AC: characters know different things and react differently; NPCs notice
  absences they had reason to expect; T3 blind-NPC passes.

### iter-4 · director + goal ticker — todo

- Consequence buffer seeded at event time; triggers (time / place /
  threshold); stagnation detector releases; director on/off switch.
- **P2b minimal goal/urge ticker** (D-021): goal → occasional autonomous
  action (drunkard seeks ale, maid roams, guard patrols) through the same
  queue, same tick discipline. Full LLM planning — never (`VISION.md` §6).
- **P2e narrative entropy** for the stagnation detector (proposal, not yet
  owner-decided): release the lowest-threshold seeded hook when entropy
  (sum of seeded-hook weights + global suspicion + visible physical
  threats) drops below threshold — not on a flat timer. Entropy computed
  only from seeded hooks + visible state, never invents new threats
  (D-005 preserved). See DIRECTOR_SPEC sketch in `docs/SPECS_BACKLOG.md`.
- AC: seeded hooks fire causally; no "from nothing" complications; world
  acts without the PC; T4 irreversibility passes; T8 director-off shows
  ≥3 emergent chains.

### iter-5 · chronicle & CLI — todo

- Template chronicle from the log (deterministic tracery engine + ink
  `shuffle` ShufflePool — `docs/blueprint/phase0.md` §5); scene card; CLI:
  `play`, `look`, `wait`, `chronicle`, `state`, `replay`,
  `directors on|off`, `seed`.
- AC: playable and readable without LLM.

### iter-6 · gate — todo

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

## Infra backlog (post-sprint, pick by need)

- `ci-1` GitHub Actions: pytest + ruff on push (`PYTHONHASHSEED=0`, pinned
  Python).
- `perf-1` 10k-tick timing profile (target: seconds, not minutes).
- `balance-1` 1000-headless-sim distribution harness: playscript runner with
  sampled intents (seed-varied) → distribution plots of `suspicion` and
  `fire_spread` over ticks. Validates that `rules.json` thresholds are tuned,
  not guessed. Uses T1-determinism, no new infra. Prerequisite for iter-6
  M-baseline (KI#4).
- `doc-1` VISION freeze review after the phase-0 verdict.
- `doc-2` REFERENCES.md license/URL re-verification, quarterly (alongside the
  TECH_NOTES review).
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

- iter-0 · 2026-08-25 · docs & tooling bootstrap.
- iter-0b · 2026-08-25 · docs review + external source catalog (`docs/REFERENCES.md`).
- iter-0c · 2026-08-25 · REFERENCES rev v2 merge (D-017) + `content/tavern_pack/` v0.1 drafted.
- iter-0d · 2026-08-25 · infra restore: `.gitignore`, package skeleton, smoke tests (KI#1/KI#2).
- iter-0e · 2026-08-25 · `docs/CORE_DESIGN_RESEARCH.md` (synthesis, depth equation, P1–P3, Q1–Q4).
- iter-0g · 2026-08-26 · research pass: Q1–Q3 absorbed (D-019..D-021); KI#3–KI#5 opened.
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
