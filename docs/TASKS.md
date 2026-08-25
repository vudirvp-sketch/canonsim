# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2.

## Track A — main (simulator, no LLM)

### iter-1 · core plumbing (sprint days 3–4) — todo

- Seed → single `random.Random(seed)` instance; integer clock; `heapq` queue
  keyed `(tick, sub_order, actor_id)`; JSONL append-only writer with header
  (no wall-clock); playscript runner (seed + ordered intents);
  pack loader for the drafted `content/tavern_pack/` v0.1 (entities from
  `MVP_SCOPE.md` §4 — that table is the source of truth; pack data landed in
  iter-0c).
- Tests: T0 schema validation (the EVENT_SCHEMA example is a fixture; the log
  header shape per EVENT_SCHEMA §1 is validated as a separate fixture), minimal
  T1 (two runs byte-identical), smoke boot.
- AC: world creates from seed; an event writes; a playscript plays end-to-end;
  `pytest -q` green.

### iter-2 · actions (days 5–6) — todo

- The 12 actions with checks/outcomes/durations (`MVP_SCOPE.md` §7);
  pack-driven preconditions; event emission for each; INV-3 grep stoplist
  test.
- AC: steal / arson / talk = facts in the log with knowledge records;
  impossible stays impossible (T5 partial).

### iter-3 · knowledge + relations + expectations (days 7–8) — todo

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

### iter-4 · director + goal ticker (days 9–10) — todo

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

### iter-5 · chronicle & CLI (days 11–12) — todo

- Template chronicle from the log; scene card; CLI: `play`, `look`, `wait`,
  `chronicle`, `state`, `replay`, `directors on|off`, `seed`.
- AC: playable and readable without LLM.

### iter-6 · gate (days 13–14) — todo

- Full T1–T8; director-off A/B on identical seed + playscript; M1–M5
  metric report (thresholds set from baseline); manual playtest; phase-0
  verdict in `worklog.md`.
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
- `ref-N` Reference deep dives — one batch per iteration, owned by
  `docs/REFERENCES_DEEP.md` §1 (the plan table). Solo iterations for sources
  with ≥3 subsystems worth deep coverage; 2–3 per iter for the rest. Pick in
  order; skip if a phase hasn't shipped yet. Sequence:
  - `ref-3` (solo) Paradox event scripting (CK3 + EU4 + Stellaris) — full
    grammar: trigger, weight, mtth, effect, option, scope.
  - `ref-4` (batch) RimWorld + L4D Director + Alien: Isolation — pacing /
    storyteller trio; phase-3 director ref.
  - `ref-5` (batch) Wesnoth WML + Endless Sky mission DSL + ink + tracery —
    event / narrative grammar family.
  - `ref-6` (batch) Brogue + DCSS + KeeperRL — roguelike emergence +
    micro-sim.
  - `ref-7` (batch) Stanford Generative Agents + ai-town + letta — LLM-agent
    precedents (mostly negative; overlaps bg-4).
  - `ref-8` (batch) Azgaar FMG + Natural Earth + GeoNames — worldgen data
    donors; phase 5.
  - `ref-9` (batch) libtcod + rot.js + Red Blob Games — FOV / pathfinding /
    grid math; pattern only (D-012).
  - `ref-10` (batch) entt + Bevy + EventStore — ECS scheduling + event-
    sourcing stream/projection patterns.
  - `ref-11` (batch) SQLite FTS5 + DuckDB + sqlite-vec — storage layer
    candidates; depends on phase-4 retrieval decision.

## Done

- iter-0 · 2026-08-25 · docs & tooling bootstrap (this pack).
- iter-0b · 2026-08-25 · owner-requested docs review: error fixes + external
  source catalog (`docs/REFERENCES.md`).
- iter-0c · 2026-08-25 · owner-requested rev v2 merge: REFERENCES §14
  layer/priority map, D-017, TECH_NOTES §6; `content/tavern_pack/` v0.1
  drafted (entities, actions, rules, templates).
- iter-0d · 2026-08-25 · owner-requested infra restore: `.gitignore` + package
  skeleton + pack/schema smoke tests; pyproject package-discovery fix (KI#1,
  KI#2 closed).
- iter-0e · 2026-08-25 · owner-requested core-design research:
  `docs/CORE_DESIGN_RESEARCH.md` (reference synthesis, depth equation, gaps
  P1–P3, open questions Q1–Q4 for the owner).
- iter-0g · 2026-08-26 · owner-requested research pass (Q1–Q3 yes, Q4 no):
  Q1–Q3 absorbed as D-019..D-021; KI#3 expectation_violation, KI#4 balance
  harness, KI#5 runtime-vs-fold logged; §2 of CORE_DESIGN_RESEARCH deepened
  (Mesa, Neighborly, Red Blob, Game Programming Patterns); P1e/P2d/P2e/P3f
  new proposals; SPECS_BACKLOG sketches extended (DIRECTOR/LEGEND/BRIEF);
  MVP_SCOPE §4.2/§10/§15 updated. Doc-loop alarm exception (sixth docs iter).
- iter-0h · 2026-08-26 · owner-requested references deep dive: new
  `docs/REFERENCES_DEEP.md` (400 lines) — format template + iteration plan
  + first batch (Neighborly, Mesa, DF Legends XML export schema); D-024
  three-place anti-drift policy (catalog ↔ synthesis ↔ deep dives); TASKS
  gets `ref-N` backlog items (ref-1..ref-11); AGENT_NAVIGATION §1 + §3
  updated; STATUS FAQ gets three-places-three-jobs pitfall. Doc-loop alarm
  exception (seventh docs iter, D-022).
- iter-0i · 2026-08-26 · owner-requested ref-1 solo deep dive: §3 in
  `docs/REFERENCES_DEEP.md` (DF worldgen + history layer); §2 trimmed to
  fit 400 cap (substance lost — restored in iter-0j). Doc-loop exception.
- iter-0j · 2026-08-26 · owner-requested ref-2 + cap policy rewrite: §4
  in `docs/REFERENCES_DEEP.md` (C:DDA `data/json/` schema); §2 restored
  from iter-0i over-trim; AGENTS §6 rewritten with §6.1 substance-vs-
  cruft criteria (D-025) — 400-line hard wall replaced by 600 ceiling +
  substance filter; file now 737 lines (substance-justified). Doc-loop
  exception (ninth docs iter).
