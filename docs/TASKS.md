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
    precedents (mostly negative; overlaps bg-4). → done (iter-0p):
    `docs/ref/generative_agents.md` (371 — Park et al. 2023 memory
    stream shape one-to-one with our per-NPC knowledge records +
    retrieval function `recency + importance + relevance` top-k
    [lifted into `brief/recall.py` with stdlib embedder + tick
    delta + event `weight` field] + reflection pattern [INV-1-
    compatible compaction by recurrence — higher-level entries
    are new log entries, not edits] + planning hierarchical
    decomposition with re-plan-on-violation + `Persona`/
    `Scratchpad` JSON split [lifted into `entities.json` +
    `state = fold(log)`] + `agentStep` LLM hot loop [canonical
    LLM-agent architecture] + 25-agent Smallville cost benchmark
    ~$70/2-day for 25 agents [bg-4]; explicitly negative on LLM
    in hot loop [INV-4] + OpenAI network [INV-4 stricter —
    local llama.cpp/Outlines in phase 1+] + non-determinism
    [INV-2 byte-identical impossible] + per-agent scratchpad
    files [INV-1 amnesia — JSONL log + per-actor projection
    is the inverse] + flat memory stream without per-channel
    routing [no `seen`/`told`/`inferred`, KI#3 has no analogue]),
    `docs/ref/ai_town.md` (345 — Convex reactive database +
    `engine.ts` per-tick LLM call + `agentStep` action-grammar
    discriminated-union [`MoveAction`/`SayAction`/`WaitAction`,
    lifted into `templates.json` `action_type` enum] + `archives`
    table compaction-on-overflow + `prompts/` text-file template
    pattern [lifted into `templates.json` shape] + pixi.js
    reactive frontend + GitHub OAuth multi-tenant + `memories`
    table schema [same field shape as our per-NPC knowledge
    records]; explicitly negative on Convex reactive substrate
    [INV-1 + INV-2 inverse — JSONL log + SQLite index is the
    right substrate] + LLM in hot loop [INV-4] + OpenAI/Anthropic/
    OpenRouter network [INV-4 stricter] + reactive frontend
    [`MVP_SCOPE` §2 non-goal — no UI in phase 0] + insertion-order
    agent iteration [INV-2 fix = `sorted()` by ID, queue key
    `(tick, sub_order, actor_id)`]; cost benchmark ~$50/day
    for 25 agents at 1 Hz [bg-4]),
    `docs/ref/letta.md` (353 — block manager context-window
    partition [`system`/`persona`/`human`/`tools`/`scratchpad`/
    `fifo_queue` blocks with per-block token budget, lifted into
    `brief/assembler.py` block layout] + three-tier memory
    hierarchy [core/recall/archival, lifted into canon log +
    per-NPC projection + brief cache — same hierarchy shape,
    different storage substrate] + internal tools
    [`core_memory_append`/`core_memory_replace`/
    `archival_memory_insert`/`conversation_search`/
    `conversation_search_date`] + `summarize_messages_in_place`
    compaction-on-overflow + `LLMClient` abstract base with
    per-provider concrete classes [lifted into
    `brief/llm_client.py` — local llama.cpp/Outlines only]
    + REST + WebSocket agent-as-a-service + OS-memory-hierarchy
    analogy [paper arXiv:2310.08560]; explicitly positive on
    block-manager shape + three-tier hierarchy + pluggable-LLM-
    client interface + `conversation_search_date` tick-range
    retrieval; explicitly negative on LLM in hot loop [INV-4]
    + OpenAI/Anthropic/Google/vLLM network [INV-4 stricter] +
    `core_memory_replace` LLM-mutates-own-memory [INV-5 inverse
    — corrections are new events] + `summarize_messages_in_place`
    drops-originals [INV-1 inverse — reflection-on-recurrence
    from `generative_agents.md` is the canonsim shape] +
    pgvector dependency [D-012 stdlib-only — SQLite + FTS5
    instead] + agent-as-a-service REST/WebSocket [`MVP_SCOPE`
    §2 non-goal] + flat `recall_memory` without per-channel
    routing [KI#3 no analogue]). All three open-licensed per
    `REFERENCES.md` §5 — pattern lifting permitted, port the
    shape not the syntax per §0.7 (D-015). License drift
    pre-flip caught: ref-7-a was listed as "(paper)" in §2
    index, misleading; catalog says Apache-2.0 (the repo);
    fixed in the same §2 edit. No KI#6-class drift this
    iteration.
  - `ref-8` (batch) Azgaar FMG + Natural Earth + GeoNames — worldgen data
    donors; phase 5. → done (iter-0q): `docs/ref/azgaar_fmg.md`
    (280 — four-layer architecture [world data/generators/editors/
    renderers — INV-1 inherits: canon log = world data;
    `sim/systems/` = generators; `cli/` = editors; `render/` =
    renderer] + ordered generator pipeline [30+ side-effecting
    imports in `src/generators/index.ts` documenting dependency
    order: voronoi → heightmap → features → names → lakes →
    river → burgs → biomes → cultures → routes → states →
    zones → religions → labels → added-labels → provinces →
    emblems → ice → ocean → relief → military → markers →
    measurers → goods → production → markets → resample] +
    `State` interface shape [`i`/`name`/`capital`/`culture`/
    `coa`/`neighbors`/`campaigns`/`diplomacy`/`formName`/
    `fullName` — per-entity record with foreign keys + cached
    adjacency + embedded chronology; lifted into `content/packs/
    <pack>/entities.json`] + `Campaign` interface shape [`name`/
    `start`/`end`/`attacker`/`defender` — typed chronology
    event with temporal bounds + actor refs; lifted into
    `EVENT_SCHEMA.md` §2 `tick` + `actor_id` + `cause` chain]
    + diplomacy chronicle [per-state `diplomacy` array on
    designated neutral state[0] — INV-1 fix: global JSONL
    log, not per-state field] + re-entrant pipeline [editors
    as 'interactive generators'; lifted into `Intent` →
    `Event` validation front-door in iter-3+ `cli/`] + `.map`
    save file [seed + state snapshot — INV-1 split: JSONL
    log = replay; SQLite index = snapshot]; explicitly
    negative on side-effecting imports [INV-1 fix: emit
    events, not in-place mutation] + per-state chronicle
    [INV-1 fix: global log] + floating-point Voronoi
    determinism [INV-2 fix: integer ticks + `random.Random
    (seed)`] + catalog row says 'chronology generator' but
    chronology embedded in `states-generator.ts` as
    `generateCampaigns` + `generateDiplomacy` — minor
    catalog↔repo drift, fixed in this per-ref file),
    `docs/ref/natural_earth.md` (250 — three-scale LOD
    ladder [1:10m/1:50m/1:110m; lifted into phase-5 LOD:
    canon log = ground truth; per-NPC projection = mid LOD;
    brief cache = top LOD] + `featurecla` closed-enum-on-
    each-record [every feature carries its type; lifted
    into `entities.json` `entity_type` enum + `EVENT_SCHEMA.md`
    §2 `event_type` enum] + 155-property `ne_110m_admin_0_
    countries` schema [multiple foreign-key systems ISO/
    FIPS/UN/WB/WOE/WIKIDATA + 50 localized-name fields
    `NAME_<lang>` + precomputed display hints `MAPCOLOR7`/
    `8`/`9`/`13` + `POP_EST`/`GDP_MD`/`ECONOMY`/`INCOME_GRP`;
    lifted into `entities.json` closed enum + per-type fields
    (scale trimmed) + `templates.json` localized name sets +
    `render/` display hints on data records] + semantic
    versioning [X.Y.Z with documented major/minor/patch
    boundaries — 'data layout is the API'; lifted into
    `schemas/event.schema.json` `schema_version` + §3
    migration rule] + per-theme file split [one file per
    domain: physical/cultural/populated_places/urban_areas;
    lifted into `content/packs/<pack>/` per-category file
    split]; explicitly negative on 155-property heaviness
    [trim to what simulation uses] + floating-point geometry
    [INV-2 fix: lift metadata only in phase 0, defer
    geometry to phase-5+] + dataset scale [several GB; lift
    shape, not data] + real-world dataset [right shape,
    wrong content — Azgaar FMG + a future fantasy toponym
    source are better fitted]; 'multiple LODs of same data
    should be coherent' lesson [README 'Neatness Counts']
    shapes phase-5 LOD ladder),
    `docs/ref/geonames.md` (345 — 9-class / 684-code
    feature-class enum [verified 2026-08-26 against live
    `featureCodes_en.txt` dump — `readme.txt` says 645,
    stale by 39 codes; classes A/H/L/P/R/S/T/U/V; lifted
    into `entities.json` `entity_type` enum as closed enum
    at top + per-type refinements; 4 types in phase 0 vs
    684 codes in GeoNames] + `geoname` table per-feature
    record shape [`geonameid`/`name`/`asciiname`/
    `alternatenames`/`latitude`/`longitude`/`feature class`/
    `feature code`/`country code`/`cc2`/`admin1-4`/`population`/
    `elevation`/`dem`/`timezone`/`modification date` — flat
    per-feature record with PK + display name + ASCII
    fallback + multilingual alternates + lat/long + typed
    feature + admin hierarchy + population + elevation +
    timezone; lifted into `entities.json` per-entity record
    shape] + admin-hierarchy code chain [admin1 → admin2 →
    admin3 → admin4 + explicit `hierarchy.zip` typed parent/
    child file with type 'ADM'/'related'; implicit hierarchy
    via codes + explicit hierarchy via separate file;
    lifted into `relations.json` P2a pair-keyed relation
    map] + `alternatenames` table [`alternateNameId`/
    `geonameid` FK/`isolanguage` ISO 639 + variants `zh-CN`/
    `post`/`iata`/`icao`/`fr_1793`/`abbr`/`link`/`wkdt`/
    `alternate name`/`isPreferredName`/`isShortName`/
    `isColloquial`/`isHistoric`/`from`/`to` period bounds;
    per-feature multilingual name records with type flags +
    period-of-use bounds; lifted into `templates.json`
    localized name sets + chronicle rename events — a new
    name is a new record with `from` tick] + daily delta
    files [`modifications-<date>.txt` + `deletes-<date>.txt`
    + `alternateNamesModifications-<date>.txt` +
    `alternateNamesDeletes-<date>.txt` — append-only log
    discipline; lifted into INV-1 + INV-5 — the log is
    append-only, every change is a new event, no edits ever]
    + per-country dump + all-countries dump + city-only
    subsets [`cities500/1000/5000/15000.zip` by population
    threshold]; explicitly negative on tab-delimited format
    [INV-3 fix: schema in sidecar, not in code] +
    floating-point lat/long [INV-2 fix: lift metadata only
    in phase 0] + 684-code enum scale [trim to 4 types in
    phase 0; many codes like `S.AIRB` don't apply to
    pre-industrial fantasy] + `readme.txt` stale '645 codes'
    claim [live dump has 684 — documentation lag, dump is
    source of truth; logged here as doc↔repo drift catch]
    + CC-BY 4.0 attribution sidecar mandatory at intake +
    real-world dataset [right shape, wrong content — Azgaar
    FMG is the right content]; 'dataset as append-only log'
    lesson [daily modifications/deletes deltas] shapes INV-1
    + INV-5). All three open-licensed per `REFERENCES.md`
    §1+§2 — pattern lifting permitted, port the shape not
    the syntax per §0.7 (D-015). Licenses verified against
    catalog §1+§2 (MIT for Azgaar FMG, public domain for
    Natural Earth, CC-BY 4.0 for GeoNames) — no KI#6-class
    drift this iteration. Minor catalog↔repo drift: catalog
    §2 row for Azgaar FMG says 'chronology generator' but
    the actual repo at master has chronology embedded in
    `states-generator.ts` (no separate
    `chronology-generator.ts` file); fixed in this per-ref
    file (the catalog row is the short version, the per-ref
    file is the long one). Minor doc↔repo drift: GeoNames
    `readme.txt` says '645 codes' but the live dump has 684
    codes (stale by 39); documented in the per-ref file,
    dump is source of truth.
  - `ref-9` (batch) libtcod + rot.js + Red Blob Games — FOV /
    pathfinding / grid math; pattern only (D-012). → done
    (iter-0q): `docs/ref/libtcod.md` (279 — FOV algorithm
    closed enum [14 algorithms: `FOV_BASIC`/`FOV_DIAMOND`/
    `FOV_SHADOW`/`FOV_PERMISSIVE_0..8`/`FOV_RESTRICTIVE`/
    `FOV_SYMMETRIC_SHADOWCAST` + `NB_FOV_ALGORITHMS` sentinel;
    lifted into `sim/systems/perception.py` iter-3 —
    algorithm choice is config-time, recorded in determinism
    contract] + `TCOD_MapCell` per-tile state [`transparent`
    bool input + `walkable` bool input + `fov` bool output;
    lifted into per-tile visibility projection — canon log
    records 'what is there', perception system projects
    'what can be seen' given viewer position + sight
    radius] + A* + Dijkstra pathfinder interface [graph-
    search with per-tile cost function + priority queue
    using libtcod's `heapq.h` binary heap primitive —
    Python's `heapq` stdlib is the direct equivalent;
    lifted into `sim/systems/movement.py` iter-2 — no
    external dep, D-012] + BSP dungeon generator
    [`TCOD_bsp_t` tree node with `x`/`y`/`w`/`h`/`level`/
    `position`/`[left, right]` children + `TCOD_bsp_split`
    recursive split; deferred to phase-5+ spatial layer,
    phase-0 tavern uses fixed grid] + heightmap pipeline
    [`TCOD_heightmap_t` 2D float array + `add`/`normalize`/
    `add_fbm` Fractal Brownian Motion Perlin/Simplex at
    multiple octaves/`scale_fbm`/`dig`/`kernel_transform`;
    deferred to phase-5+ worldgen, cf. Azgaar FMG
    `heightmap-generator.ts` for same pattern in JS/TS] +
    single-instance seeded Mersenne Twister RNG
    [`TCODRandom`; lifted into `core/rng.py` iter-1 —
    Python's `random.Random(seed)` is Mersenne Twister,
    INV-2 requires one instance, no wall-clock] + per-
    feature file split [one .h/.hpp pair per feature:
    `fov.h`/`path.h`/`bsp.h`/`noise.h`/`heightmap.h`/
    `mersenne.h`/...; lifted into `sim/systems/` per-system
    file layout]; explicitly negative on C/C++ implementation
    [D-012 fix: port shapes to Python stdlib] + breadth-
    irrelevant-to-CLI [`console.h`/`mouse.h`/`image.h`/
    `tileset_*.h`/`renderer_xterm.h` not relevant to a CLI
    simulation; lift only `sim/systems/` + `core/` + `render/`
    parts] + no event sourcing [INV-1 fix: every movement
    is a canon event] + no determinism contract [INV-2 fix:
    one RNG instance, no wall-clock, sorted iteration, queue
    key] + no content/code split [INV-3 fix: algorithm choice
    is config-time, recorded in determinism contract];
    BSD-3-Clause [verified 2026-08-26 against `LICENSE.txt`
    in `libtcod/libtcod` repo] — permissive license, no
    friction at intake; 'permissive license on a reference
    implementation is a gift to the ecosystem' lesson — we
    lift shapes not syntax, no obligation to ship our code
    under same license),
    `docs/ref/rot_js.md` (347 — `EventQueue` min-heap core
    [`_time` + `_events` MinHeap<T> + `getTime()`/`clear()`;
    canonical event-scheduling primitive; lifted into
    `core/queue.py` iter-1 — Python's `heapq` for the heap,
    integer tick for time, queue key `(tick, sub_order,
    actor_id)` is INV-2 fix for tiebreaking simultaneous
    events that rot.js's bare `_time` would collide on] +
    scheduler family [abstract `Scheduler<T>` with `_queue:
    EventQueue<T>` + `_repeat: T[]` + `_current: any` +
    abstract `next()` + 3 concrete subclasses: `Simple`
    round-robin insertion-order + `Speed` speed-based with
    next event at `_time + 1/speed` (classic roguelike turn
    scheduler) + `Action` action-point-based; family of
    schedulers extending one abstract base, each defining a
    turn discipline; lifted into `core/queue.py` discipline
    — queue key IS the discipline, iter-3+ may add speed-
    based variant if P2b minimal goal/urge ticker D-021
    needs it] + FOV family [abstract `FOV` with `compute(x,
    y, R, VisibilityCallback)` + `LightPassesCallback`
    boolean per tile + 3 concrete subclasses: `Discrete
    Shadowcasting` per-octant line-tracing 0/1 visibility +
    `PreciseShadowcasting` fractional visibility 0..1 for
    partial cover + `RecursiveShadowcasting` the 'classic'
    recursive shadowcasting (same family as libtcod's
    `FOV_SHADOW`); closed family extending one abstract
    base, same interface; lifted into `sim/systems/
    perception.py` iter-3 — closed enum at config time,
    interface `compute(viewer_x, viewer_y, radius, callback)`]
    + path family [abstract `Path` with `compute(x1, y1,
    x2, y2, callback)` + 2 concrete subclasses: `AStar` with
    Manhattan heuristic by default + `Dijkstra` for all-
    pairs shortest paths; lifted into `sim/systems/
    movement.py` iter-2] + map family [11 generators
    extending abstract `Map` with `create(callback)`:
    `Arena`/`Cellular`/`Digger`/`DividedMaze`/`Dungeon`/
    `EllerMaze`/`Features`/`IceyMaze`/`Rogue`/`Uniform`;
    deferred to phase-5+ spatial layer] + Alea RNG
    [Baagøe algorithm with `_s0`/`_s1`/`_s2` state + carry
    `_c`, seed expansion via `seed*69069 + 1` LCG; lifted
    into `core/rng.py` iter-1 — Python's `random.Random
    (seed)` Mersenne Twister is the equivalent, INV-2
    requires one instance] + engine game loop wrapper
    [single-threaded loop pulling actors from scheduler,
    calling `actor.act()`, supports async `result.then` for
    browser-side promise-based actions; lifted into
    `core/runner.py` iter-1 — sync loop, no async path in
    phase 0] + per-feature directory + abstract base +
    concrete subclasses shape [`src/scheduler/` + `src/fov/`
    + `src/path/` + `src/map/` with `index.ts` aggregating;
    lifted into `sim/systems/` per-system file layout];
    explicitly negative on TypeScript/JS implementation
    [D-012 fix: port shapes to Python stdlib] + bare
    `_time` queue key [INV-2 fix: 3-tuple `(tick, sub_order,
    actor_id)` queue key for tiebreaking] + browser focus
    [README has `<script>` tag + ES2015 modules + babel+
    rollup bundlers + Node.js with `term` layout backend;
    CLI not relevant, lift only algorithm shapes] + no
    event sourcing [INV-1 fix: every action is a canon
    event, `act()` returns Intent that simulator validates]
    + no determinism contract [INV-2 fix: one RNG instance,
    no wall-clock, sorted iteration, queue key] + no
    content/code split [INV-3 fix] + `setSeed` hack `seed =
    (seed < 1 ? 1/seed : seed)` for fractional seeds [our
    `random.Random(seed)` accepts any hashable, integer
    seed]; 'feature-complete focused toolkit' lesson
    [library 'largely considered feature-complete' per
    README] shapes our `sim/systems/` scope [8 systems in
    phase 0, stops growing after iter-6 phase gate];
    BSD-3-Clause [verified 2026-08-26 from `package.json`
    `license` field in `ondras/rot.js` repo] — no friction
    at intake),
    `docs/ref/red_blob_games.md` (312 — hex grid coordinate
    algebra [offset odd-r/even-r/odd-q/even-q + axial (q, r)
    + cube (x, y, z with x+y+z=0) + doubled; conversions
    offset↔axial↔cube with exact formulas + distance in
    cube coords `max(|Δx|, |Δy|, |Δz|)` + line drawing via
    cube-coord sampling + rounding + range walking the
    cube coordinate ring + rotation by 60° in cube coords +
    FOV/line-of-sight via hex-grid line drawing + pixel-to-
    hex conversion for pointy-top + flat-top orientations
    with fractional hex intermediate; the canonical write-
    up that every hex-grid library (libtcod + rot.js +
    hexlib + reffy) implements; deferred to phase-5+ spatial
    layer if hex-based, phase-0 tavern uses square grid] +
    A* pseudo-code [open set + closed set + g cost-from-
    start + h heuristic estimate-to-goal + f = g + h + pick
    lowest f + expand neighbors + update g and parent;
    BFS/Dijkstra/A* family framing with different h choices
    [0 for BFS, exact for Dijkstra, estimated for A*];
    heuristic functions Manhattan/Euclidean/Chebyshev/
    Octile by movement rules; priority queue binary heap +
    tiebreaking prefer higher g toward goal; the most-cited
    A* tutorial in game dev; lifted into `sim/systems/
    movement.py` iter-2 — libtcod + rot.js implementations
    are concrete instances of this algorithm] + polygon
    map generation pipeline [Voronoi diagram from N
    random points via d3-delaunay/delaunator + Lloyd's
    relaxation 1-2 iterations for uniform distribution +
    Perlin noise elevation with radial gradient for island
    shape + watershed downhill tracing for rivers +
    Whittaker biome diagram elevation × moisture → biome
    type + noisy edges for hand-drawn look; the canonical
    Voronoi+noise worldgen — Azgaar FMG implements the same
    algorithm with additional passes states/cultures/
    religions; deferred to phase-5+ worldgen] + relational
    grid abstraction [faces/edges/corners with typed
    relations — a face has edges, each edge has 2 corners,
    each corner has 3 edges; same relational shape for
    square/hex/triangle grids, different geometries; grid
    as graph of parts with relations; deferred to phase-5+
    spatial layer's per-part query interface] + circle
    drawing algorithms [midpoint circle + Andreev for AoE
    effects + circular rooms; lifted into `sim/systems/`
    iter-2 fire_spread AoE queries] + distance-to-any
    single-source Dijkstra + all-pairs Floyd-Warshall
    pre-compute [choice: Dijkstra for one-off paths,
    Floyd-Warshall for pre-computed small maps; lifted into
    `sim/systems/movement.py`]; explicitly negative on no
    explicit license statement [site has no license on
    article pages — verified 2026-08-26 by inspecting
    `/grids/hexagons/` + `/pathfinding/a-star/introduction.html`
    + `/about`; CSS comment 'CSS Copyright 2007-2026 by Amit
    J. Patel' is for stylesheet not content; Amit Patel
    explicitly requests attribution in academic contexts
    per `/blog/`; convention adopted here = treat as CC-BY
    4.0, re-evaluate if stance changes] + HTML5 canvas
    demos [lift formulas + pseudo-code only, not
    interactivity] + d3-delaunay/delaunator dependency for
    Voronoi [port to Python stdlib — Python's `geometry` +
    `math` modules suffice for small N] + not a code
    repository [formulas in prose + diagrams, no `git clone`
    to inspect] + hex grid not directly relevant to
    phase-0 [defer to phase-5+ if we go hex] + polygon map
    generation not directly relevant to phase-0 [defer to
    phase-5+ worldgen]; the site is the canonical write-up
    layer above the libtcod + rot.js implementations —
    algorithm shapes here are the source of truth that
    implementations are concrete instances of; 'BFS/
    Dijkstra/A* are a family with different heuristics'
    lesson shapes `sim/systems/movement.py` config-time
    choice of algorithm; 'worldgen is composition of
    focused passes' lesson [Voronoi → relax → elevation →
    watershed → biomes → noisy edges] is the same lesson as
    Azgaar FMG and 'small alphabet deep composition' lesson
    from `brogue.md`; interactive HTML5 canvas demos lesson
    [algorithm write-ups benefit from interactivity] shapes
    phase-5+ frontend explorability goal). All three
    open-licensed per `REFERENCES.md` §3+§8 (BSD-3-Clause
    for libtcod + rot.js, treat-as-CC-BY for Red Blob
    Games — catalog §8 has no license column for knowledge-
    base sources; convention adopted here per Amit Patel's
    explicit attribution-request in academic contexts) —
    pattern lifting permitted, port the shape not the
    syntax per §0.7 (D-015). License drift pre-flip caught:
    ref-9-a and ref-9-b were listed as 'BSD' shorthand in
    §2 index, but catalog §3 says 'BSD-3-Clause' explicitly;
    fixed in the same §2 edit that flipped ref-9-a/b/c
    todo→done. ref-9-c Red Blob Games license marked as
    'CC-BY (treat as)' in §2 index — catalog §8 has no
    license column for knowledge-base sources, so this is
    not catalog↔index drift; the convention is documented
    honestly in the per-ref file.
  - `ref-10` (batch) entt + Bevy + EventStore — ECS scheduling + event-
    sourcing stream/projection patterns. → done (iter-0r): `docs/ref/
    entt.md` (359 — MIT; C++ ECS sparse-set blueprint: `basic_sparse_
    set` dual-array + `deletion_policy` swap_and_pop/in_place/swap_only
    + `basic_storage<Type>` paged payload + `basic_view` smallest-pool-
    leads + `basic_group` eagerly maintained intersection [negative:
    invalidates on structural change] + `basic_organizer` task DAG +
    `sigh`/`sink`/`connection` RAII hooks + `basic_sigh_mixin` auto-
    publish + `entt_traits::entity_mask`/`version_mask` id+version
    packing + `meta_type`/`meta_factory` reflection; lifted into
    `core/store.py` + `sim/systems/*.py` View helper + `sim/systems/
    __init__.py` organizer DAG + `core/ids.py` + `content/packs/*.py`
    meta-registration shape; explicitly negative on C++ template-heavy
    API [D-012 fix] + mutable in-place storage [INV-1 fix: events-only
    derived state] + `organizer` signature-inferred ro/rw [INV-3 fix]
    + `group` invalidates [queue discipline sidesteps] + `meta` verbose
    [dataclasses more ergonomic]), `docs/ref/bevy.md` (469 — dual
    `MIT OR Apache-2.0`; Rust ECS + scheduler: `World` struct owning
    `entities` + `storages` [Table columnar + SparseSet triple] +
    `Component` trait with `STORAGE_TYPE` Table/SparseSet + `Resource`
    singleton accessed via `Res`/`ResMut` + `Query<D, F>` with
    `With`/`Without`/`Added`/`Changed` filters + `Schedule` + `SystemSet`
    + `before`/`after`/`chain`/`in_set` + `ambiguous_with` UnGraph
    build-time conflict detection + `Messages<M>` double-buffered ring
    [`messages_a`/`messages_b`/`message_count`/`update()` swap-clear/
    per-reader `MessageCursor.last_message_count`; renamed from
    `Events<T>` in v0.20-dev — pattern unchanged] + `Command`/
    `CommandQueue`/`Commands` deferred mutation + `App` + `Plugin`
    builder + `States` FSM [`State<S>` + `NextState<S>` Unchanged/
    Pending/PendingIfDifferent + `StateTransition` schedule + `OnEnter`/
    `OnExit`] + `Entity` id+generation packs to u64; lifted into
    `core/queue.py` Messages<M> double-buffer [JSONL log = producer
    buffer B; per-tick `update()` swap = tick boundary; per-system
    Local<MessageCursor> = per-system integer-tick cursor] +
    `sim/systems/__init__.py` Schedule+SystemSet+ambiguous_with graph
    + `core/` per-system scratch + `sim/systems/` phase control;
    explicitly negative on Rust-only runtime [D-012 fix: patterns
    only, never vendored] + in-place mutable ResMut<T> [INV-1 fix:
    lift deferred-queue shape not `&mut World` target — `Command::
    apply` becomes "serialize to event JSON, append to log, advance
    tick"] + trait/derive macro type-safety [lifted → Python
    dataclasses + JSON Schema, type-safety degrades to runtime
    checks] + SparseSet/Table cache-line layout [pointless in Python —
    `dict` overhead dominates] + async_executor/multi_threaded [dead
    weight for serial fold]), `docs/ref/eventstore.md` (534 —
    BSD-3-Clause [≤23.x] / ESLv2/Kurrent-License-v1 [24.10+] —
    pattern only; canonical event-sourcing mechanics: `EventRecord`
    [EventId Guid + EventType string + Data + Metadata byte[] +
    EventStreamId + EventNumber + LogPosition + TimeStamp] +
    `ExpectedVersion` OCC constants [`Any = -2`/`NoStream = -1`/
    `Invalid = -3`/`StreamExists = -4`; SDK rebrands to `StreamState`]
    + `SystemNames.SystemStreams` [`$all` global ordered stream +
    `$$<stream>` metastream] + `SystemMetadata` retention knobs
    [`$maxAge`/`$maxCount`/`$tb`/`TruncateBefore`] + `StreamMetadata`
    class + `EventNumber.DeletedStream = long.MaxValue` tombstone
    sentinel + `JintProjectionStateHandler` JS projection engine
    [`emit`/`linkTo`/`linkStreamTo`/`copyTo` globals + `init`/`state`
    fold + `CheckpointTag` restartable] + `PersistentSubscription` +
    `PersistentSubscriptionCheckpointWriter` [checkpoint to
    `$persistentsubscription-<id>-checkpoint` stream with `maxCount=2`]
    + `VNodeState` 16-enum cluster gossip + `Scavenger<TStreamId>`
    Accumulate→Calculate→Chunks→Merge→Index→Clean pipeline restartable
    from `ScavengeCheckpoint` + `ResolvedEvent` [Link $> + Event] +
    `OperationResult.WrongExpectedVersion` rejection +
    `WriteEventsCompleted` post-write `LastEventNumber` +
    `CurrentVersion`; lifted into `core/queue.py` + global JSONL log
    [`$all` — explicit `(tick, sub_order, actor_id)` queue key replaces
    opaque `TFPos`] + `cli/` Intent → Event validation front-door
    [ExpectedVersion OCC — an Intent converts to an Event only after
    the invariant check passes] + `schemas/event.schema.json` [EventRecord
    shape] + runtime log retention policy [StreamMetadata MaxAge/
    MaxCount/TruncateBefore] + INV-5 corrections-as-new-events +
    offline scavenge [tombstone logical deletion + Scavenger physical
    compaction]; explicitly negative on JS projection engine Jint
    [D-012 fix: Python fold functions, "emit" is `yield`] + cluster
    gossip + leader election [irrelevant overhead for single-process
    phase-0 sim] + ESLv2 license friction at 24.10+ [pattern-only
    intake is the only path, but none of the C# code is useful to us
    anyway] + persistent subscriptions [SQLite IS the checkpoint —
    separate stream would be double-bookkeeping] + `$all` TFPos opaque
    ordering [INV-2 fix: explicit domain-meaningful queue key]). All
    three under cap by construction. §2 of `docs/REFERENCES_DEEP.md`
    flips ref-10-a/b/c todo → done + rich one-line verdicts + fixes
    license drift on ref-10-c [index "MIT" → "BSD-3-Clause (≤23.x);
    ESLv2/Kurrent-License-v1 from 24.10 — pattern only" — pre-flip
    caught, KI#6-class pitfall avoided]. AGENT_NAVIGATION §1 adds
    three new files to `docs/ref/` list. Licenses verified against
    catalog §6+§7 — the EventStore license history (BSD-3-Clause at
    ≤23.x, ESLv2 from 24.10, renamed Kurrent-License-v1 in Feb 2025)
    was verified by reading the LICENSE.md commit log on master.
    Doc-loop exception (seventeenth docs iter, D-022).
  - `ref-11` (batch) SQLite FTS5 + DuckDB + sqlite-vec — storage layer
    candidates; depends on phase-4 retrieval decision. → done
    (iter-0r): `docs/ref/sqlite_fts5.md` (368 — public domain;
    zero-dependency keyword search in stdlib SQLite: `CREATE VIRTUAL
    TABLE <name> USING fts5(<col1>, <col2>, ...)` schema + 4 tokenizers
    [`unicode61` default w/ `remove_diacritics` + `categories` +
    `tokenchars`/`separators`; `ascii`; `porter` wrapper applying
    Porter stemmer; `trigram` for substring matching] + `bm25(<table>
    [, w0, w1, ...])` [lower = better, `k1=1.2`, `b=0.75`, per-column
    positional weights] + `highlight()`/`snippet()` + query operators
    [`AND`/`OR`/`NOT` precedence; `NEAR(p1 p2 [, N=10])` proximity;
    `*` prefix token; `^` initial-token anchor; `+` phrase concat;
    `col:` column filters] + `INSERT INTO ft(ft, ...) VALUES(...)`
    lifecycle [`rebuild`/`optimize`/`merge`/`automerge`/`crisismerge`/
    `usermerge`/`deletemerge`/`delete`/`delete-all`/`integrity-check`/
    `rank`/`pgsz`/`secure-delete`/`insttoken`] + `fts5vocab` virtual
    table + 5 shadow tables [`%_data`/`%_idx`/`%_config`/`%_docsize`/
    `%_content` — never accessed directly] + segment b-trees
    [immutable, leveled, newer-wins] + content-table variants
    [plain/contentless/contentless-delete/external-content]; lifted
    into `core/storage.py` [the chronicle `facts` FTS5 virtual table —
    D-003 canon index] + `brief/assembler.py` [bm25 positional
    column weights] + `render/` [highlight + snippet] + unicode61
    default for multilingual content packs + NEAR for proximity
    queries + `rebuild` as the INV-1 mechanism; explicitly negative
    on keyword-only [need sqlite-vec for semantic] + ranking
    customization bm25 + custom C function only [recency×authority×
    BM25 blend needs Python reranker] + tokenizer fixed at CREATE
    TABLE [switch forces full rebuild — INV-1-expected path but
    plan at design time] + segment b-trees accumulate under write-
    heavy loads [batch inserts + optimize once at end] + `delete`
    on contentless tables brittle [prefer plain tables + full
    rebuild]), `docs/ref/duckdb.md` (458 — MIT; in-process columnar
    OLAP engine, OFFLINE not runtime [D-012]: `DuckDB` class +
    `Connection` [Query → MaterializedQueryResult, Prepare →
    PreparedStatement, PendingQuery async] + `STANDARD_VECTOR_SIZE
    = 2048` DataChunk [vector of column-vectors — morsel-driven
    parallelism, chunk IS the morsel] + `PhysicalOperator` family
    keyed by `PhysicalOperatorType` enum [FILTER/PROJECTION/HASH_
    GROUP_BY/PERFECT_HASH_GROUP_BY/PARTITIONED_AGGREGATE/WINDOW/
    HASH_JOIN/ASOF_JOIN/TOP_N/ORDER_BY/TABLE_SCAN/INSERT/BATCH_
    INSERT/COPY_TO_FILE/ATTACH/DETACH/CREATE_SEQUENCE/EXPLAIN_
    ANALYZE] + `read_json_auto()`/`read_ndjson_auto()` TVF [no-ETL
    ingestion — point at the JSONL log and start querying] +
    `CopyFunction("parquet")` [COPY TO + COPY FROM] + `Appender`
    API [`BeginRow`/`EndRow`/`Append<T>`, flush every 204,800 rows]
    + composite types [`STRUCT`/`LIST`/`MAP`/`UNION`/`ARRAY`/`TUPLE`]
    + window functions [`WINDOW_LAG=133`/`WINDOW_LEAD=132`/
    `WINDOW_RANK=120`/`WINDOW_ROW_NUMBER=125` — `LAG(suspicion)
    OVER (PARTITION BY actor_id ORDER BY tick)` is the canonical
    per-actor state-delta pattern] + extension mechanism [`INSTALL`/
    `LOAD`/`AutoLoadExtension`; core `parquet`+`json`+`icu`+`core_
    functions`+`autocomplete` baked in] + `ATTACH` + `CREATE
    SEQUENCE` + `PRAGMA`/`EXPLAIN` + per-column compression
    [`Bitpacking`/`Dictionary`/`FSST`/`ALP`/`ALPRD`/`Chimp128`/
    `Patas`/`Roaring`/`Zstd` — compress-once-scan-many]; lifted
    into the `chronicler` offline pipeline [read JSONL → columnar
    table → aggregate SQL → summary SQLite; the *pattern*, not the
    code] + `read_ndjson_auto` no-ETL ingestion + `COPY TO ...
    (FORMAT PARQUET)` parquet archive output + `Appender` bulk-load
    fallback + `LAG`/`LEAD` per-actor state deltas + `ATTACH` to
    write summary back into runtime SQLite; explicitly negative on
    C++ runtime dependency [D-012 fix: NOT in the runtime path —
    chronicler is `scripts/chronicle.py` outside the runtime module
    graph] + phase-0 log too small [SQLite wins on simplicity below
    ~100k events] + single-writer OLAP model [cannot live-ingest
    during simulation — chronicler runs after tick-batch seal] +
    another tool in the chain [only justified at phase-3+ scale per
    D-022] + extensions fetch from network by default [must bundle
    binaries or rely on auto-loaded core extensions]), `docs/ref/
    sqlite_vec.md` (383 — dual `MIT OR Apache-2.0`; local-first
    vector index in SQLite, conditionally-loaded C extension NOT
    phase-0 runtime dep: `vec0` virtual-table module [`CREATE
    VIRTUAL TABLE <name> USING vec0(<col> <type>[N] [pk] [partition
    key] [distance_metric=L2|cosine], <other_col>, +<aux_col>)` —
    same shape as FTS5] + implicit `rowid` + MATCH kNN [`WHERE
    <col> MATCH :query_vec ORDER BY distance LIMIT k`] +
    `vec_distance_cosine` [canonical name, not `vec_distance_cos`;
    `1 - cos`] + `vec_distance_L2`/`vec_distance_L1`/
    `vec_distance_hamming` [L2 default, cosine opt-in per-column
    via `distance_metric=cosine`] + `vec_f32`/`vec_int8`/`vec_bit`
    constructors [subtype byte tagging 223/225/224] + `vec_to_
    json` + `vec_quantize_binary` [32× storage reduction, 8
    dims/byte] + `vec_quantize_int8(v, 'unit')` + `vec_slice` +
    `vec_normalize` [matryoshka embeddings — train at 1024-d,
    store/query at 256-d → ~4× index shrink] + `vec0` shadow
    tables [`_rowids`/`_chunks`/`_vector_chunks00`/`_rescore_
    chunks00`/`_rescore_vectors00`/`_metadatachunks00`] +
    partition-key columns + auxiliary columns [`+`-prefixed, no
    JOIN for SELECT, max 16 metadata + 16 auxiliary + 4 partition
    keys] + `vec_each(v)` TVF + `vec_version()`/`vec_debug()` +
    loadable-extension entrypoint via `sqlite3_load_extension`
    [Python: `db.enable_load_extension(True); sqlite_vec.load(db);
    db.enable_load_extension(False)`; macOS system Python lacks
    `enable_load_extension` entirely] + pure-Python `struct.pack
    ("%sf" % len(v), *v)` serializer helper; lifted into the
    canonical "vector index over facts" pattern for `core/storage.
    py` + `vec_distance_cosine` as the canonical similarity
    metric + matryoshka compression strategy + binary-quant two-
    pass pattern [coarse bit[D] kNN filter then L2 rescore];
    explicitly negative on C extension not in Python stdlib
    [D-012 fix: conditional loadable extension at phase 4 — phase
    0 stays stdlib-only with pure-Python `cosine_sim()` brute-force
    fallback over the same BLOB format] + pure-Python fallback
    O(N·D) [viable for phase-0 small N < 10⁴ facts, painful past
    10⁴ at 768-d] + pre-v1 with breaking changes expected [pin a
    version, treat SQL contract as the stable interface not C
    ABI] + no approximate search in stable path [HNSW/IVF/DiskANN
    in separate experimental C files, not default]). All three
    under cap by construction. §2 of `docs/REFERENCES_DEEP.md`
    flips ref-11-a/b/c todo → done + rich one-line verdicts +
    fixes license drift on ref-11-c [index "MIT" → "MIT OR
    Apache-2.0 (dual)" — pre-flip caught, KI#6-class pitfall
    avoided; catalog "verify" license status RESOLVED to dual
    `MIT OR Apache-2.0`]. AGENT_NAVIGATION §1 adds three new
    files to `docs/ref/` list. Licenses verified against catalog
    §6+§14 — sqlite-vec's "verify" status in the catalog is now
    resolved to dual `MIT OR Apache-2.0` per `LICENSE-MIT` +
    `LICENSE-APACHE` + `sqlite-dist.toml` manifest. Doc-loop
    exception (seventeenth docs iter, D-022 — same exception as
    ref-10 since both ref-10 and ref-11 are in the same iter-0r
    6-batch).
  - `ref-12` (solo, owner-requested, fresh external source) Universe Audit
    Protocol webapp (the owner's own repo). → done (iter-0s):
    `docs/ref/uap_audit.md` — countable-criteria rubric donor (their §0.6
    "code decides, not the LLM" = external validation of our `MVP_SCOPE.md`
    §15 metric law and the gate-review instrument) + 7-logical-hole taxonomy
    crosswalked onto T2/T3/D-005 (TEST_PLAN sketch) + phase-1 harness prompt
    shapes (role-in-system, criteria-not-labels, staged weaknesses handoff,
    per-stage temperature 0.2/0.45/0.6, free-tier resilience: chunking /
    RPM delay / single retry / partial-text recovery) + three-state
    PASS/FAIL/INSUFFICIENT_DATA honest-default shape for VALIDATION_SPEC
    + pack-admission lint vocabulary for phase 6 (PACK_SPEC sketch);
    negative on LLM-as-judge scoring (X/52 = unseeded opinion, INV-2
    violation), regex-over-markdown bridge (D-018 crutch), free-form canon
    (INV-4 boundary inversion), invented thresholds (our law: thresholds
    from the iter-6 baseline). License catch: README claims MIT, no LICENSE
    file in the repo (checked 2026-08-27) — catalog reads "reference only"
    until the owner adds one; patterns are free regardless. Doc-loop alarm:
    18th consecutive docs iteration — owner-requested exception per the
    documented condition ("no further ref-N iterations unless a fresh
    external source enters the catalog"); **iter-1 is now unconditionally
    the next iteration**.
  - `ref-13` (solo, owner-requested, fresh external source) Live Character
    Guide (the owner's own repo). → done (iter-0t):
    `docs/ref/live_char_guide.md` — character-card methodology donor (SPINE
    GHOST→LIE→FLAW→NEED→WANT causal chain of observable units; anchors
    Trigger→Action→Price where Price = immediate, physical, same-scene
    observable cost; embodiment State→Body→Sensor→Speech; voice isolation +
    pattern-matcher principle + recency-dominant influence hierarchy; 7 CORE
    DIRECTIVES; OCEAN 1–2 extreme-pole budget; 15 anti-patterns
    symptom→cause→fix; countable diagnostics: 6 scenarios, 6 success
    metrics, one-change rule). Load-bearing transfers: (1) "every element
    must produce an observable action" = external validation of the
    causal-density/dead-event law (second convergence after UAP §0.6, now
    at character granularity); (2) Price as the immediate-observable half
    of consequence (D-005 owns the deferred half) — causal-density
    checklist wording + iter-2 pack-rule pattern, no schema change;
    (3) Influence Boundary as candidate iter-2/3 architecture rule (NPC
    behavior reads own state + own knowledge only; other entities' states
    enter via perceived observable markers — closes system 5 into the
    perception→knowledge chain); (4) brief-layer law for BRIEF_SPEC (facts
    as structured tokens, style in template exemplars, AN/lorebook
    injection-scheduling grammar: depth/probability/cooldown/sticky/range);
    (5) AP catalog → PACK_SPEC lint vocabulary; (6) 6-scenario battery →
    playscript suite design. Adapted, not taken raw: SPINE/OCEAN as pack
    metadata + modifier tables (INV-3 — the spine-hooks-in-core-code
    variant is a violation, rejected); relation drift as a fold over
    price-bearing events; GHOST-Layers degradation counter → counted-event
    capability loss. Rejected: prompt-compensation machinery (token
    budgets, PP/format locks — track-B shape only), self-disclaimed
    percentages as thresholds (iter-6 baseline law), psychometrics as
    runtime systems, false memory + fatigue emulation (canon breaks —
    INV-1/INV-5 inversions), human-judged gates (our law: log-computed).
    License: MIT, LICENSE file present (verified 2026-08-27) — content and
    patterns both liftable, unlike UAP. Doc-loop alarm: 19th consecutive
    docs iteration — owner-requested exception per the documented
    condition (fresh external source + explicit request); **iter-1 remains
    unconditionally the next iteration**.

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
- iter-0p · 2026-08-26 · owner-requested ref-7 3-batch deep
  dive: `docs/ref/generative_agents.md` (371),
  `docs/ref/ai_town.md` (345), `docs/ref/letta.md` (353) —
  three open-licensed LLM-agent precedent references (Stanford
  Generative Agents memory stream shape + retrieval function
  + reflection pattern + `Persona`/`Scratchpad` split + cost
  benchmark ~$70/2-day/25 agents, ai-town Convex reactive DB
  + per-tick LLM call + discriminated-union action grammar +
  `prompts/` text-file template + cost ~$50/day/25 agents,
  letta block-manager context-window partition + three-tier
  memory hierarchy [core/recall/archival] + internal memory
  tools + OS-memory-hierarchy analogy). All three under cap
  by construction. §2 of `docs/REFERENCES_DEEP.md` flips
  ref-7-a/b/c todo → done + rich one-line verdicts +
  fixes license drift on ref-7-a ["(paper)" → "Apache-2.0
  (repo) + paper" — pre-flip caught, KI#6-class pitfall
  avoided]. AGENT_NAVIGATION §1 adds three new files to
  `docs/ref/` list. Licenses verified against catalog §5 —
  no KI#6-style drift this iteration. Doc-loop exception
  (fifteenth docs iter, D-022).
- iter-0q · 2026-08-26 · owner-requested ref-8 + ref-9
  6-batch deep dive: `docs/ref/azgaar_fmg.md` (280),
  `docs/ref/natural_earth.md` (250), `docs/ref/geonames.md`
  (345), `docs/ref/libtcod.md` (279), `docs/ref/rot_js.md`
  (347), `docs/ref/red_blob_games.md` (312) — six open-
  licensed worldgen data donor + grid math pattern-only
  references (Azgaar FMG four-layer architecture + ordered
  generator pipeline + `State`/`Campaign` interface shapes,
  Natural Earth three-scale LOD ladder + `featurecla` closed
  enum + 155-property admin-0 schema + semantic versioning,
  GeoNames 9-class/684-code feature enum + `geoname` table
  per-feature record + admin-hierarchy code chain +
  `alternatenames` table + daily delta files, libtcod FOV
  algorithm closed enum + `TCOD_MapCell` per-tile state +
  A*/Dijkstra pathfinder + BSP + heightmap + Mersenne
  Twister RNG + per-feature file split, rot.js `EventQueue`
  min-heap + scheduler family [simple/speed/action] + FOV
  family + path family + 11 map generators + Alea RNG +
  engine game loop, Red Blob Games hex grid coordinate
  algebra + A* pseudo-code + polygon map generation pipeline
  [Voronoi + Lloyd + Perlin + watershed + Whittaker biomes +
  noisy edges] + relational grid abstraction + circle
  drawing + Floyd-Warshall pre-compute). All six under cap
  by construction. §2 of `docs/REFERENCES_DEEP.md` flips
  ref-8-a/b/c + ref-9-a/b/c todo → done + rich one-line
  verdicts + fixes license drift on ref-9-a/b ["BSD" →
  "BSD-3-Clause" — pre-flip caught, KI#6-class pitfall
  avoided] + adds "CC-BY (treat as)" annotation on ref-9-c
  (catalog §8 has no license column for knowledge-base
  sources, convention adopted per Amit Patel's explicit
  attribution-request in academic contexts). AGENT_NAVIGATION
  §1 adds six new files to `docs/ref/` list. Licenses
  verified against catalog §1+§2+§3+§8 — no KI#6-class
  drift this iteration. Minor catalog↔repo drift: catalog
  §2 row for Azgaar FMG says 'chronology generator' but the
  actual repo has chronology embedded in `states-generator.ts`
  (no separate `chronology-generator.ts` file); documented
  honestly in the per-ref file. Minor doc↔repo drift:
  GeoNames `readme.txt` says '645 codes' but the live dump
  has 684 codes (stale by 39); documented honestly in the
  per-ref file. Doc-loop exception (sixteenth docs iter,
  D-022).
- iter-0r · 2026-08-26 · owner-requested ref-10 + ref-11
  6-batch deep dive: `docs/ref/entt.md` (359), `docs/ref/
  bevy.md` (469), `docs/ref/eventstore.md` (534), `docs/ref/
  sqlite_fts5.md` (368), `docs/ref/duckdb.md` (458), `docs/ref/
  sqlite_vec.md` (383) — six open-licensed ECS + event-
  sourcing + storage-layer pattern-only references (entt
  C++ ECS sparse-set blueprint [basic_sparse_set dual-array +
  deletion_policy swap_and_pop/in_place/swap_only + basic_
  storage<Type> paged payload + basic_view smallest-pool-
  leads + basic_group eagerly maintained intersection +
  basic_organizer task DAG + sigh/sink/connection RAII hooks +
  basic_sigh_mixin auto-publish + entt_traits id+version
  packing + meta_type/meta_factory reflection], Bevy Rust
  ECS + scheduler [World + Component trait with STORAGE_TYPE
  Table/SparseSet + Resource singleton + Query<D, F> with
  With/Without/Added/Changed filters + Schedule + SystemSet
  + before/after/chain/in_set + ambiguous_with build-time
  conflict detection + Messages<M> double-buffered ring
  [renamed from Events<T> in v0.20-dev] + Command/CommandQueue/
  Commands deferred mutation + App + Plugin builder + States
  FSM + Entity id+generation], EventStoreDB event-sourcing
  mechanics [EventRecord + ExpectedVersion OCC constants
  Any/NoStream/Invalid/StreamExists + SystemNames.SystemStreams
  $all + SystemMetadata $maxAge/$maxCount/$tb retention knobs +
  StreamMetadata class + EventNumber.DeletedStream tombstone +
  JintProjectionStateHandler JS projection engine +
  PersistentSubscription + PersistentSubscriptionCheck-
  pointWriter + VNodeState 16-enum cluster gossip +
  Scavenger Accumulate→Calculate→Chunks→Merge→Index→Clean +
  ResolvedEvent + OperationResult.WrongExpectedVersion +
  WriteEventsCompleted post-write LastEventNumber], SQLite
  FTS5 [CREATE VIRTUAL TABLE USING fts5 + 4 tokenizers
  unicode61/ascii/porter/trigram + bm25 ranking + highlight
  + snippet + NEAR/* /^ /+ /col: query operators +
  INSERT lifecycle commands rebuild/optimize/merge/automerge
  + fts5vocab virtual table + 5 shadow tables + segment
  b-trees + content-table variants], DuckDB [DuckDB class +
  Connection + STANDARD_VECTOR_SIZE=2048 DataChunk +
  PhysicalOperator family + read_json_auto/read_ndjson_auto
  TVF + CopyFunction("parquet") + Appender API + composite
  types STRUCT/LIST/MAP/UNION/ARRAY/TUPLE + window functions
  WINDOW_LAG/WINDOW_LEAD/WINDOW_RANK/WINDOW_ROW_NUMBER +
  extension mechanism + ATTACH + CREATE SEQUENCE + PRAGMA/
  EXPLAIN + per-column compression Bitpacking/Dictionary/
  FSST/ALP/Chimp128/Patas/Roaring/Zstd], sqlite-vec [vec0
  virtual-table module + MATCH kNN + vec_distance_cosine/
  vec_distance_L2/L1/hamming + vec_f32/vec_int8/vec_bit
  constructors with subtype byte tagging + vec_to_json +
  vec_quantize_binary 32× storage reduction + vec_slice +
  vec_normalize matryoshka embeddings + vec0 shadow tables +
  partition-key + auxiliary columns + vec_each TVF +
  vec_version/vec_debug + loadable-extension entrypoint +
  pure-Python struct.pack serializer helper]). All six under
  cap by construction. §2 of `docs/REFERENCES_DEEP.md` flips
  ref-10-a/b/c + ref-11-a/b/c todo → done + rich one-line
  verdicts + fixes license drift on ref-10-c [index "MIT" →
  "BSD-3-Clause (≤23.x); ESLv2/Kurrent-License-v1 from 24.10
  — pattern only" — pre-flip caught, KI#6-class pitfall
  avoided] + resolves ref-11-c "verify" catalog license
  status to dual "MIT OR Apache-2.0" + fixes the matching
  index drift [index "MIT" → "MIT OR Apache-2.0 (dual)"].
  AGENT_NAVIGATION §1 adds six new files to `docs/ref/`
  list. Licenses verified against catalog §6+§7+§14 —
  EventStore license history (BSD-3-Clause at ≤23.x, ESLv2
  from 24.10, renamed Kurrent-License-v1 in Feb 2025)
  verified by reading the LICENSE.md commit log on master;
  sqlite-vec "verify" status resolved by reading LICENSE-MIT
  + LICENSE-APACHE + sqlite-dist.toml manifest. Doc-loop
  exception (seventeenth docs iter, D-022).
- iter-0s · 2026-08-27 · owner-requested ref-12 solo deep dive (fresh
  external source: universe-audit-protocol-webapp): `docs/ref/uap_audit.md`
  + catalog §9 row + REFERENCES_DEEP §1/§2 rows + CORE_DESIGN_RESEARCH §2
  row + SPECS_BACKLOG TEST_PLAN/PACK_SPEC sketch clauses. License catch:
  README claims MIT, no LICENSE file — reference only. Doc-loop exception
  (eighteenth docs iter); iter-1 unconditional next.
- iter-0t · 2026-08-27 · owner-requested ref-13 solo deep dive (fresh
  external source: live-char-guide): `docs/ref/live_char_guide.md`
  + catalog §9 row + REFERENCES_DEEP §1/§2 rows + CORE_DESIGN_RESEARCH §2
  row + SPECS_BACKLOG BRIEF_SPEC/PACK_SPEC sketch clauses. License clean:
  MIT, LICENSE file verified. Doc-loop exception (nineteenth docs iter);
  iter-1 unconditional next.
- iter-0u · 2026-08-27 · owner-requested references distillation (no new
  external source — the request itself is the trigger, D-022 wording
  satisfied): `docs/BLUEPRINT.md` + `docs/blueprint/phase0.md` +
  `docs/blueprint/phases.md` (D-027 — the resolution ledger: 12
  cross-reference tensions resolved into mechanisms; 12 cross-cutting
  laws; per-iteration donor stacks; phases 1–6 architecture) +
  AGENT_NAVIGATION §1/§2/§3 + REFERENCES_DEEP pointer + STATUS/worklog
  synced; STATUS "Next step" drift folded into the blueprint build index.
  Doc-loop exception (twentieth docs iter); iter-1 unconditional next.
