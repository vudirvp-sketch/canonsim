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
- `ref-N` Reference deep dives — one file per source under `docs/ref/`, per
  the plan in `docs/REFERENCES_DEEP.md` §1 (the plan table) and the index
  in §2 (which filenames to create). Solo iterations for sources with ≥3
  subsystems worth deep coverage; 2–3 sources per iter for the rest. Pick
  in order; skip if a phase hasn't shipped yet. Sequence:
  - `ref-3` (solo) Paradox event scripting (CK3 + EU4 + Stellaris) — full
    grammar: trigger, weight, mtth, effect, option, scope. → done
    (iter-0l): `docs/ref/paradox_scripting.md`; 605 lines, 5 over cap
    per AGENTS §6.1 (three games × trigger/MTTH/weight/effect/scope/
    on_action subsystems with real field names + ~150+ on_action IDs).
  - `ref-4` (batch) RimWorld + L4D Director + Alien: Isolation — pacing /
    storyteller trio; phase-3 director ref. → done (iter-0m):
    `docs/ref/rimworld.md` (253 — Defs taxonomy, IncidentDef field
    triad, storyteller trio, threat-points scalar, TaleDef chronicle
    layer, QuestDef signals+parts arc, Randy from-nothing anti-pattern
    naming D-005), `docs/ref/l4d_director.md` (245 — multi-channel
    Horde/S.I./Music family, intensity ratchet, peak/rest two-state
    clock with floors, spawn budget = 1 per beat, player-cardinal
    survival bias as named negative reference against `VISION.md` §6),
    `docs/ref/alien_isolation.md` (296 — two-AI actor vs director split,
    Pressure scalar with cap-and-floor transitions, encounter windows
    with `MinGapBetweenEncounters` floor, three-axis anxiety
    perceived/actual/unknown, offscreen presence in vents,
    objective-broadcast matching Intent/Event, "Director learns the
    player" as named anti-pattern against `VISION.md` §6 player-blind
    canon law). All three proprietary §10 sources — design-notes only
    per `REFERENCES.md` §0.5; patterns not content per §0.7 (D-015).
  - `ref-5` (batch) Wesnoth WML + Endless Sky mission DSL + ink + tracery —
    event / narrative grammar family. → done (iter-0n):
    `docs/ref/wesnoth_wml.md` (244 — `[event]`/`[filter]`/action triad
    as reactive atom, `first_time_only`/`id`/
    `delayed_variable_substitution` orthogonal save-compat fields,
    per-noun `[filter]` family with real field names, ~30 action
    verbs, macro preprocessor, Lua escape hatch since 1.7 as
    precedent for our `cli/`/`brief/` split, closed `name` enum
    lifted into `actions.json` `action_type`, `sighted` event as
    perception-as-first-class-event-source), `docs/ref/endless_sky_dsl.md`
    (228 — mission lifecycle `to: offer`/`accept`/`complete`/`fail`/
    `defer` as state-machine shape for our `Intent`, smallest condition
    language in the family — no MTTH/scopes/weights/on_action IDs,
    flat `effect` mini-language, `phrase` one-symbol grammar
    [simpler-than-tracery precedent], `event` block separate from
    `mission` as cleanest public precedent for player-independent
    background events = our `seeded_hooks`, `npc` `personality`
    flags lifted into `entities.json` `traits`), `docs/ref/ink.md`
    (212 — knot/stitch/divert/gather graph shape lifted into our
    `Brief` sketch phase 1+, `LIST` multivalued flags lifted into
    entity `state`, `+` vs `*` choice persistence lifted into
    `Intent` `accept_policy`, `#` tags lifted into `Brief`
    `metadata`, three sequence flavours `cycle`/`sequence`/
    `shuffle` as determinism hazard [INV-2 fix], `KnotName?`
    visited-check as precedent for `seen` knowledge channel,
    snapshot-save amnesia anti-pattern as INV-1 fix), `docs/ref/tracery.md`
    (217 — JSON grammar shape lifted verbatim into `templates.json`,
    save/restore stack `[symbol:value#]`/`[symbol:#]` lifted
    into `render/` `stack[pop]` for cross-clause agreement,
    modifier pattern `#symbol.modifier#` with built-ins
    `a`/`capitalize`/`s`/`ed`/`er` + registration hook lifted
    into `templates.json` modifiers, "pure function from
    (grammar, RNG state) → string" pattern = our `render/` shape,
    ~200-line runtime scale as precedent that useful procedural
    text generation is a small algorithm not a framework). All
    four open-licensed per `REFERENCES.md` §0.4 — pattern lifting
    permitted, port the shape not the syntax per §0.7 (D-015).
    KI#6 opened and closed in this iter: §2 of `REFERENCES_DEEP.md`
    had license drift for ref-5-b ("CC-BY-SA" vs catalog
    "GPL-3.0 code; mixed assets") and ref-5-d ("CC0" vs catalog
    "Apache-2.0"); both fixed in the same §2 edit.
  - `ref-6` (batch) Brogue + DCSS + KeeperRL — roguelike emergence +
    micro-sim. → done (iter-0o): `docs/ref/brogue.md` (326 — two-stream
    RNG `RNG_SUBSTANTIVE`/`RNG_COSMETIC` with `brogueAssert`
    scope guards, 36-byte no-wall-clock recording header
    [version/seed/turn/level/length], `promoteTile` per-layer
    state-transition primitive with flag-gated trigger sources
    [`TM_IS_FLAMMABLE`/`TM_PROMOTES_ON_ELECTRICITY`/
    `TM_IS_WIRED`/`promoteChance`], multi-pass environment
    tick with read→write→cleanup pass separation, layered
    `pmap[x][y].layers[layer]` cell-stack, `updateVolumetricMedia`
    stochastic gas diffusion with `rand_range(0, numSpaces - 1) <
    (sum % numSpaces)` stochastic rounding, `paintLight` additive
    RGB over `getFOVMask`, `randomNumbersGenerated` audit counter,
    the "small alphabet deep composition" lesson [fire/gas/water/
    light ~5 rules → emergent chains], explicitly negative on
    in-memory `pmap` state model [INV-1 amnesia] + `time(NULL)`
    seed fallback [we never loosen INV-2]),
    `docs/ref/dcss.md` (360 — multi-stream RNG `rng_type` enum
    [`GAMEPLAY`/`UI`/`SYSTEM_SPECIFIC`/`LEVELGEN`+per-branch,
    NUM_RNGS = LEVELGEN + NUM_BRANCHES], RAII `rng::generator`
    for stream switching, PCG generator, `ASSERT_stable` scope
    guard [snapshot+assert no consumption on exit], `peek_uint32/
    64` non-advancing reads, `defer_rand` infinite lazy tree
    [functional randomness — same path always same value],
    energy-based turn scheduler [`speed_increment`/
    `BASELINE_DELAY=10`/`div_rand_round` stochastic rounding],
    `dgn_event_dispatcher` positional event system [`DET_*`
    bitflags + per-position listeners + vetoable], `.des` vault
    grammar [`NAME`/`TAGS`/`DEPTH`/`CHANCE`/`SUBST`/`FTILE` +
    Lua `: ... :` escape hatch], 15-year-codebase-scales
    discipline precedent, explicitly negative on in-memory
    monster struct state [INV-1 amnesia] + Lua-in-vaults escape
    [INV-4 stricter] + no knowledge records + no director),
    `docs/ref/keeperrl.md` (444 — continuous-time queue
    [`map<ExtendedTime, Queue>` with `players`/`nonPlayers`
    deques, `orderMap` per-queue-position tiebreaker,
    `extraTurn` flag for haste], `Model::tick` per-tick update
    order [creatures → levels → collectives → territory →
    external], `Collective::tick` 11-step subsystem update
    [border/rebellion/guard/minion-promotions/danger-cache/
    control/zones/task-map/constructions/dancing/warnings],
    `getRebellionProbability` small-formula social dynamics
    [12-line prisoner/fighter ratio formula],
    `ExternalEnemies` 500-wave pre-computed planner
    [`firstAttackDelay=1800`/`attackInterval=1200`/
    `attackVariation=450`, dispatched by `popNextWave(local
    Time)` small-if], `GameEvent` X-macro 24-event closed
    variant, `cereal` binary serialisation, data-driven
    content DSL [`data_free/game_config/*.txt` with `inherit`],
    `Fire` minimal optional-state machine, single-instance
    `extern RandomGen Random`, explicitly negative on
    single-stream RNG [no two-stream discipline] + binary
    save [INV-1 JSONL is inverse] + no knowledge records +
    custom DSL with no schema [D-023 fix]). All three open-
    licensed per `REFERENCES.md` §2 — pattern lifting
    permitted, port the shape not the syntax per §0.7
    (D-015). Licenses verified against catalog §2 (AGPL for
    Brogue CE, GPL-2.0+ for DCSS, GPL-2.0 for KeeperRL) —
    no KI#6-style drift this iteration.
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
- iter-0k · 2026-08-26 · owner-requested REFERENCES_DEEP split (D-026):
  deep-dive content moved from single-file `docs/REFERENCES_DEEP.md`
  into `docs/ref/<source>.md` per-ref files (5 created: `neighborly.md`,
  `mesa.md`, `df_legends_xml.md`, `df_worldgen.md`, `cdda_data_json.md`,
  101–244 lines each). `REFERENCES_DEEP.md` rewritten as index (133
  lines): header + §0 format template + §1 iteration plan + §2 NEW index
  table (one row per ref). D-026 supersedes D-024 single-file wording;
  three-place anti-drift policy unchanged. AGENT_NAVIGATION §1 + §3
  updated. Doc-loop exception (tenth docs iter).
- iter-0l · 2026-08-26 · owner-requested ref-3 solo deep dive:
  `docs/ref/paradox_scripting.md` (605 lines, 5 over cap per §6.1
  substance — three games × trigger/MTTH/weight/effect/scope/on_action
  subsystems with real field names + ~150+ on_action IDs). §2 of
  `REFERENCES_DEEP.md` flips ref-3 todo → done. AGENT_NAVIGATION §1
  adds `paradox_scripting.md` to the `docs/ref/` list. Doc-loop
  exception (eleventh docs iter, D-022).
- iter-0m · 2026-08-26 · owner-requested ref-4 3-batch deep dive:
  `docs/ref/rimworld.md` (253), `docs/ref/l4d_director.md` (245),
  `docs/ref/alien_isolation.md` (296) — three proprietary §10
  pacing/director references (RimWorld Defs+Storyteller, L4D
  intensity ratchet + multi-channel, Alien two-AI split + three-axis
  anxiety). All three under cap by construction (closed-source forces
  field-shape-from-talks only). §2 of `REFERENCES_DEEP.md` flips
  ref-4-a/b/c todo → done. AGENT_NAVIGATION §1 adds three new files
  to `docs/ref/` list. Doc-loop exception (twelfth docs iter, D-022).
- iter-0n · 2026-08-26 · owner-requested ref-5 4-batch deep dive:
  `docs/ref/wesnoth_wml.md` (244), `docs/ref/endless_sky_dsl.md` (228),
  `docs/ref/ink.md` (212), `docs/ref/tracery.md` (217) — four
  open-licensed event/narrative grammar family references (Wesnoth
  WML event/filter/action triad + Lua escape valve, Endless Sky
  mission lifecycle + flat effect mini-language, ink knot/stitch/
  divert/gather graph + LIST multivalued flags, tracery JSON grammar
  + save/restore stack + 200-line runtime precedent). All four under
  cap by construction (pattern-not-content rule §0.7 keeps each
  file to mechanics layer only). §2 of `REFERENCES_DEEP.md` flips
  ref-5-a/b/c/d todo → done + fixes license drift for ref-5-b
  and ref-5-d (KI#6 closed in-iter). AGENT_NAVIGATION §1 adds
  four new files to `docs/ref/` list. Doc-loop exception (thirteenth
  docs iter, D-022).
- iter-0o · 2026-08-26 · owner-requested ref-6 3-batch deep dive:
  `docs/ref/brogue.md` (326), `docs/ref/dcss.md` (360),
  `docs/ref/keeperrl.md` (444) — three open-licensed roguelike
  emergence + micro-sim references (Brogue CE two-stream RNG
  + 36-byte no-wall-clock recording header + `promoteTile` +
  multi-pass environment tick, DCSS multi-stream RNG +
  `ASSERT_stable` + energy-based turn scheduler + `dgn_event_
  dispatcher` + `.des` vault grammar, KeeperRL continuous-time
  queue + `Model::tick` per-tick update order +
  `getRebellionProbability` small-formula social dynamics +
  `ExternalEnemies` 500-wave pre-computed planner +
  `GameEvent` X-macro variant). All three under cap by
  construction (pattern-not-content rule §0.7 + the shape-lift
  keeps each file to mechanics layer only). §2 of
  `REFERENCES_DEEP.md` flips ref-6-a/b/c todo → done +
  richer one-line verdicts. AGENT_NAVIGATION §1 adds three
  new files to `docs/ref/` list. Licenses verified against
  catalog §2 — no KI#6-style drift this iteration. Doc-loop
  exception (fourteenth docs iter, D-022).
