# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2. Done-detail lives in git
> history + `worklog.md` + the owning docs — never restated here (KI#7
> cleanup, iter-0v). Day-tags removed per D-029 (calendar dropped); the
> build sequence is iteration-counted (`MVP_SCOPE.md` §17).

## Track A — main (simulator, no LLM)

> Phase 0 closed (gate PASS, iter-6; audit-clean iter-6a). Phase 1 closed
> (gate PASS, iter-26, D-058; the polish menu tune-1/tune-2/pack-2 landed
> iter-27–29). Phase 2 closed (gate PASS, iter-35, D-064 — 35/35 boundary
> validity over 51 combined utterances, 0 honest misfires; the parse corpus
> 10 cases + the full §5 protocol re-run, M1/M2 identical to iter-26).
> Phase 3 (Director) CLOSED — gate PASS iter-54, D-083 (the D-083 row owns
> the phase-3 landing ledger). Phase 4 (Knowledge & scene) OPENED iter-55
> (the owner's "start phase 4" session call; the backlog below is drafted
> from `docs/blueprint/phases.md` §4 — the phase's architecture owner).
> Architecture owner: `docs/blueprint/phases.md` §4; exit criterion
> "0 leaks on the blind-NPC suite" (ROADMAP §2 — the T3 family,
> `docs/TEST_PLAN.md` §1, extends to the phase-4 surfaces).

### Phase-4 backlog (opened iter-55)

- `leg-1` · trait crystallization (P3f) — **done (iter-55, D-084)**:
  `core/traits.py` — the belief-token fold (a knower holding
  `threshold` DISTINCT tokens of a declared family crystallizes the
  belief, the source event ids riding as provenance); the read-model
  laws + the lint's closed vocabulary; DORMANT until leg-2 (the
  iter-47 arc precedent — the 10-seed A/B byte-identical). Detail:
  D-084 + tests/test_traits.py.
- `leg-2` · the brief's derived-trait read (leg-1's first consumer) —
  **done (iter-56, D-085)**: `brief/assembler.py::_recalled_fact_lines`
  reads the fold — belief lines lead the recalled_facts block (provenance
  ids inline, the expansion law's demand handle), the family records
  render nothing raw; `core/traits.py::expand_trait` the demand side.
  Zero-regen landing (the PC holds no family token on any committed
  corpus; the 10-seed A/B byte-identical). Detail: D-085 +
  BRIEF_SPEC §3.5 + tests/test_brief.py.
- `leg-3` · reflection & memory compaction — **done (iter-57, D-086)**:
  `core/reflection.py` — reflection-on-recurrence mints the
  higher-level entry as an EVENT through the canon door (originals
  never dropped, INV-1; never `summarize_messages_in_place`),
  `outcome.provenance` the `list[event_id]` demand handle, the
  never-re-reflect law, `stale_reflections` (the read-side flag,
  derived stores after scavenge) + `expand_reflection` the expansion
  law's demand side; `rules.json::reflection` linted, DORMANT in the
  committed pack (the 10-seed A/B byte-identical, zero corpus
  regen); LEGEND_SPEC.md written just-in-time at this row. Detail:
  D-086 + LEGEND_SPEC + tests/test_reflection.py.
- `leg-3b` · the tavern reflection set (arming the v0.1 pack block) —
  **done (iter-58, D-087)**: the measured recurrence (day1_full seeds
  123/128 — the retried theft) arms the insight pair
  `sneak_at_work_here`/`figure_reaching_for_purse` (the watcher's
  conclusion) + `trouble_by_the_bar`/`noise_by_the_bar` (the room's);
  `conclusion_drawn` story-critical, renders in the tale; the corpus
  price measured ZERO (the narrator corpus 105, the parse corpus 10,
  the T1 golden — untouched; 8/10 day1 seeds byte-identical) — the
  iter-52 zero-regen landing. Detail: D-087 + LEGEND_SPEC §7 +
  tests/test_reflection.py.
- `retr-1` · the retrieval ladder (STORE-1): SQLite FTS5 `bm25()` the
  zero-dep default, the sqlite-vec probe + fallback chain
  (vec → pure-Python cosine → FTS5-only, never an empty result), the
  deterministic re-ranker `α·recency + β·authority + γ·bm25 + δ·cosine`
  (coefficients as pack data); hard boundary: dynamic world state =
  SQL + `known_by`, never vectors.
- `scene-1` · the scene manager + mode B (one NPC per call — the
  chorus is a queue, not a convention; the per-NPC brief's leak
  surface).
- `leg-4` · mode F offline chronicler (DuckDB `read_ndjson_auto()`
  over the JSONL, per-actor state diffs, parquet rollups, ATTACH back
  into SQLite — never in the runtime import graph, D-012).
- `blind-1` · the blind-NPC leak suite extended to the phase-4
  surfaces (the exit criterion's instrument — the dir-2 precedent:
  mode B + retrieval outputs under T3's zero-leak law).

> Phase 3 (Director) landing ledger, condensed: the pacing stack
> iter-36..39 (D-065..D-068), the event grammar iter-40..42
> (D-069/D-070/D-071 — predicate/weight, options, on_action), the
> social stack iter-44..46 (D-073/D-074/D-075 — secrets, leverage,
> the echo), the arcs iter-47 (D-076), the content column
> iter-43/48/49/51/52/53 (D-072/D-077/D-078/D-080/D-081/D-082 —
> every layer and declared channel dimension live); the build column
> completed at iter-53, the gate PASS at iter-54. Architecture owner:
> `docs/blueprint/phases.md` §3; runtime contract owner:
> `docs/DIRECTOR_SPEC.md`; exit criterion "a scene without an event
> < N beats" (ROADMAP §2). Detail: the D-083 compound row + worklog.

### Phase-3 director backlog (opened iter-36)

- `dir-1` · pacing clock — **done (iter-36, D-065)**: the per-run
  RAMP/PEAK/REST/STAGNATION clock over narrative entropy; `director.pacing`
  pack data + lint; clock-gated stagnation releases; explicit triggers
  ungated (D-005). Detail: the D-065/D-066/D-067/D-068 compound row +
  DIRECTOR_SPEC §5 + TEST_PLAN §6.
- `dir-2` · the eventless-stretch instrument — **done (iter-37, D-066)**:
  `core.metrics.eventless_beat_stretches` (the exit criterion's
  measurement) + the harness `--pacing on|off` A/B; measured 1000 seeds:
  max stretch 1, both arms byte-identical (the all-PEAK law). Detail:
  TEST_PLAN §6.
- `dir-3` · layered thresholds + `PEAK_CLIMAX` — **done (iter-38, D-067)**:
  the third entropy layer `climax_floor` (75 = 3× the peak floor) + the
  climax release path (boss beats END peaks, the option gate consulted, a
  closed boss never burns) + the one-beat PEAK_CLIMAX state. Detail:
  DIRECTOR_SPEC §5.
- `dir-4` · multi-channel policies — **done (iter-39, D-068)**:
  `director.channels` (threat/social/ambient, the L4D family) +
  `SeededHook.channel` + the per-hook quiet gate (`permit_quiet`); the
  clock/budget/climax/explicit triggers stay global on purpose. Detail:
  DIRECTOR_SPEC §5.
- `drama-1` · the event grammar, predicate + weight layer — **done
  (iter-40, D-069)**: trigger predicates as JSON (`core/predicates.py`:
  leaves + compounds + the prop leaf), the `weight_multiplier`, the
  `first_time_only` burn; MTTH stays the named anti-pattern. Detail:
  DIRECTOR_SPEC §3/§3a.
- `drama-2` · the grammar's option layer — **done (iter-41, D-070)**:
  option blocks with availability gates + ai_chance-style weighting (a
  pure deterministic pick), payload overrides whole-key; the
  immediate/option/after lifecycle maps onto seed/choose/apply. Detail:
  DIRECTOR_SPEC §3b.
- `drama-3` · the on_action dispatch layer — **done (iter-42, D-071)**:
  the pack table keyed by committed event type, appended after the
  hardcoded reactions (append-not-overwrite), the witnesses scope + the
  quantified gate + the alarm-shaped state change; one-hop lint. Detail:
  DIRECTOR_SPEC §3c.
- `content-1` · the document_check content set — **done (iter-43, D-072)**:
  the 14th action over the inspect resolver (the verdict token → the
  standing arrest machinery), the climax flag live on the watcher pair,
  the crowd reaction, the 4-case corpus regen. Zero engine edits. Detail:
  the D-072/... compound row + TEST_PLAN §6.
- `social-1` · secrets & leverage as fact clusters — **done (iter-44,
  D-073)**: `core/leverage.py` + `rules.json::secrets` (the CK3 add_hook
  precedent): a novel knower mints a `leverage_gained` fact event; expiry
  a read-side fold; ONE live token; the 9-case corpus regen paid. Detail:
  the social-stack compound row.
- `social-1b` · the leverage use — the coerce door — **done (iter-45,
  D-074)**: the 15th action over the coerce resolver: `leverage_over`
  (the door's first fold-reading precondition), the spend a NEW event
  naming the cluster (one secret buys one play), the unconditional
  tick-window OCC re-check, the balance as pack data. Detail: the
  social-stack compound row.
- `social-2` · psychological echo (P3e) — **done (iter-46, D-075)**:
  `core/echo.py` — the residue as a pure read-side fold (per-NPC
  valence, linear decay, fidelity-scaled; writes nothing, feeds no
  entropy — L6) + the `echo_at_least` behavior gate. Detail: the
  content-column compound row.
- `arc-1` · arcs & tension shaping (P3c) — **done (iter-47, D-076)**:
  `director.arcs` pack chains — the ORDER law + the GAP law + the
  entropy mirror (the burn law's twin) + the one-sided membership lint;
  dormant until content-6. Detail: the D-076/D-081 compound row.
- `content-2` · the alarm panic echo — **done (iter-48, D-077)**: the
  through-the-walls law as one on_action entry (panic_ripple, witnesses
  +10 fear), story-critical with its own line, zero engine edits; the
  7-case corpus re-distill paid. Detail: the content-column compound row.
- `content-4` · the coerce driver — **done (iter-49, D-078)**: the
  drunkard's urgency entry re-armed by the REPLACEMENT law (the draw
  count holds, the corpus ladders hold); 4 seed-93 cases see the spend;
  the corpus regen via the fixed-point runner. Detail: the social-stack
  compound row + the STATUS regen FAQ.
- `content-5` · the echo driver — **done (iter-51, D-080)**: the
  jittery-watcher beat (the guard's `look_around` over `echo_at_least
  dread >= 15`, p=100 the compulsion semantics); the wariness arm
  measured and refused; the corpus ZERO broken pins + the deliberate
  pins. Detail: the content-column compound row.
- `content-6` · the arc driver — **done (iter-52, D-081)**: the
  aftermath chain `[the relief's check, the barkeep's wary sweep]` gap 2
  — the gap law LOAD-BEARING (the unchained sweep would land before the
  check: a causality lie); the closing beat riding the climax path; zero
  corpus re-distill. Detail: the D-076/D-081 compound row.
- `content-3` · the ambient driver — **done (iter-53, D-082)**: the
  drunkard's ramble, the room's murmur (the L4D Music analog) — the 16th
  action + the weight-0 ambient hook (the channel's own quiet gate its
  only road), seeded on the wait action's hooks (the resolver-sparse
  minting gap closed); day1 birth-record-only, the quiet march pinned.
  Detail: the content-column compound row + TEST_PLAN §6.
### iter-54 · phase-3 gate — done (verdict: PASS, D-083)

Full ROADMAP §5 protocol re-run: the corpus 105 + parse corpus green
(973 tests, ruff clean); the seed-125 pair ON M1=0.509 / M2=0.333 /
OFF T8 26 chains ≥ 3; the stretch table max 1 (both pacing arms + the
quiet-walk stage — the D-066 question answered); T7 reads as a story.
The doc debts paid: DECISIONS 48→30, FAQ 23→20, TASKS 854→510,
DIRECTOR_SPEC 641→593, phases.md kept over per §6.1 (the worklog
records why). Phase 4 unlocked — opens on the owner's call. Detail:
worklog iter-54 + D-083.

### Phase-2 parser backlog

- `parse-2` (owner-gated) disambiguation buttons + multi-intent
  utterances — deferred with a frontend consumer / live-session
  evidence (PARSER_SPEC §7).
- `engine-1` (owner-gated) the runtime inference engine decision
  (llama.cpp + GBNF; TECH_NOTES §1) — unlocked by the phase-1 gate,
  waits on the owner; the dev-time external parser carried phase 2 to
  its gate PASS (iter-35) and carries mode C until then.

### iter-26 · phase-1 gate — done (verdict: PASS, D-058)

Full ROADMAP §5 protocol re-run: 109 live beats / 0 canon violations /
corpus 105 green; DECISIONS collapsed 41→30; `doc-1` closed clean;
phase 2 unlocked. Detail: worklog iter-26 + `docs/DECISIONS.md` D-058.

### Phase-1 tuning backlog (post-assembler, owner-gated)

- `tune-3` alarm-adjacent reachability (iter-21 session finding):
  `transitions.fire.knowledge.alarm_adjacent` (`shouting_near_<loc>`)
  is structurally unreachable in v0.1 — the token needs a knower
  adjacent to the fire location at ignition, but NPC placement is
  static (the rotation is a direct duty↔rest swap, playscript steps
  are player-only, urgencies are all waits), so the street/backyard
  are never occupied when the fire starts; the same-location half
  (alarm + fear spike) fires fine and is corpus-pinned. Session 8
  (iter-23) pinned the same family live on the §3 rumor leg: the
  market crowd holds no `figure_at_back_door_last_night` — the
  drunkard never leaves the tavern (the refusal is corpus-pinned,
  the boundary probed, not forced). Owner's
  call: a v0.2 pack NPC-movement source (e.g. a transit route
  through the street), leave as declared-but-dormant layer
  vocabulary (a second pack may exercise it), or phase-5 spatial
  material.

(tune-1 done iter-27, tune-2 done iter-28 — see Done.)

### Stress-test backlog (iter-11b resolutions; owner-gated)

- `st-2` identity persistence: pack `identity_slots` window tier +
  per-scope quotas (read-path) + the identity promotion door (pack
  grammar beyond `take`, the D-054 machine; blueprint §1). Optional
  second trigger (bg-5): repetition-counted promotion — N repeats of
  a priced pattern via a counted fold (the ref-13 GHOST-layers
  counter pattern); owner's call: alongside or instead of the
  pack-grammar door.
- `st-3` groups & simulation LOD: one id across tiers, aggregate
  macro-clock events with cardinality, condensation on crossing
  (GROUP_SPEC trigger = phase 5 or owner request; blueprint §5).
- `st-4` the call budget (head + brief + tail + thinking + output ≤
  MECW target) + the transcript-tail contract + thinking-as-ephemeral-
  texture (the narrator-boundary iteration; blueprint §1) + the Script
  Tax clause (bg-5): non-Latin tail/prose costs ≈1.5–2× tokens on
  32K-vocab local models (guide part_07a §7A.5; ref-13) — the
  whitespace proxy under-charges Cyrillic; budget per script at the
  mediator, never in core.
- `st-5` containers: the `in` relation + entity-birth promotion
  (with `st-3`, phase 5; blueprint §7).

### Spatial backlog (owner analyses 2026-08-30, audited iter-19; owner-gated)

- `st-6` spatial vocabulary — `travel` + `layout` (the narrator's
  revisit-stability question: scene-scoped texture dies on
  `scene_close` by design, D-049, so important architecture must be
  canon from birth). (a) **`travel` as a separate action, NOT
  weighted `move`** — move semantics, `adjacent_to`, and the T1
  golden fixtures stay untouched; duration = pack-precomputed edge
  cost (per edge or edge×mode — no runtime division in the
  resolver); mechanically legal today (`t + duration`, MVP_SCOPE §8;
  the clock jumps ahead so day-scale durations are queue-cheap;
  beats/rotations still fire mid-travel in tick order, D-038); macro
  clocks (L4) enter only when regions/worldgen arrive. (b)
  **`layout` — LANDED iter-20 (D-057/KI#48)**: a top-level pack
  field on every location rendered canon-from-birth on the scene
  line via `brief.present_entities.scene_line_fields` — no
  `initial_projection` seeding (the iter-19 claim that the gateway's
  canon_slot reads top-level pack fields only was WRONG: the check
  reads both prop sources, and a pack field was already guarded —
  the `exits` precedent, KI#41); the validator adjudicates claims on
  it; mutable decor stays texture (the existing door). Remaining
  gates for (a): the phase-5 spatial layer or an owner request —
  geometry donors are phase-5-gated (ROADMAP §4) and track A is
  feature-frozen.

### iter-6 · gate — done (phase-0 verdict: PASS)

Phase-0 gate closed; full evidence in `worklog.md` iter-6 + the
`docs/TEST_PLAN.md` spec. Track A was feature-frozen at phase-0 scope;
phase 1 (narrator over the log) opened per `docs/ROADMAP.md` §2.

## Track B — background (evenings, foreign canon)

### bg-2 · event taxonomy — DONE (bg-2-event-taxonomy)

- Done one-liner: `docs/TAXONOMY.md` (120 entries across the 16 target
  types; AC ≥100 MET) + `scripts/df_taxonomy.py` (the quantile-spread
  survey over the sink DB) + the sink v2 plus pass
  (`scripts/df_import.py` — D-051's deferral fired: theft/beast detail
  is companion-only, D-063). Measured findings + the bg-3 consumer
  caveats: TAXONOMY §4/§5; recipe: TECH_NOTES §3.2.

### bg-3 · briefer spike — DONE (bg-3-briefer-spike)

- Done one-liner: `scripts/df_briefer.py` — the POV mini-briefer (the
  participant-index prefix scan as the knowledge model; the assignment
  frame kept apart from the subject's records) + the closed-vocabulary
  reverse-validation gate (`supported | contradicted | beyond_records |
  unknown_*`; prose never parsed; the ≤2-regen ladder with the dry
  floor) + the retrieval stress harness (double-build byte-compare).
  Live session: 4 TAXONOMY §5-anchored cases, 31 claims — 19 supported
  / 12 deliberate-probe non-supported, 0 honest misfires; 1 regen
  recovery, 1 exhaustion. Numbers (brief p50 ≈ 2.9 KB on GB-scale
  exports; scan p99 ≤ 0.2 ms; 3 worlds, determinism PASS): TECH_NOTES
  §3.3; regression `tests/test_df_briefer.py`. The F7 honest
  expectation held — mechanics validated, not micro-event
  interestingness.

### bg-6 · SoW integration audit — todo (owner-deferred)

- Read-only pass over `github.com/jofizcd/Soul-of-Waifu` (registered
  2026-08-30 at the owner's request; the owner defers integration "until
  unavoidable"): extension points for a separate simulation chat mode
  (a new mode vs. invasive edits), where llama.cpp sits, what the
  frontend must NOT own (the dumb-terminal contract, VISION §10).
  Output: a TECH_NOTES section + the `SOW_INTEGRATION_SPEC` sketch.
  Unlocked by the phase-1 gate (D-058); owner-deferred "until
  unavoidable" (D-055). Never blocks track A.

## Infra backlog (pick by need)

- `engine-2` · the urgency-roll stream split — **done (iter-50,
  D-079)**: the owner's "quality over speed" fork call. Per-entry
  streams `urgency:<npc>:<kind>` (content-addressed, pack-linted
  unique, lazily registered, the assure nesting law reworked for the
  family); the single shared stream was measured and refused (the
  entries couple by draw position). Add-safety 10/10 day1_full
  byte-identical on the iter-49 refused scenario; the one-time flip
  paid (0/10, 2 corpus cases + 1 parse pin + 2 seed re-probes).
- `ci-1` GitHub Actions: pytest + ruff on push (`PYTHONHASHSEED=0`, pinned
  Python).
- `qa-1` mypy --strict on `core/` (owner-approval-gated: dev tooling is
  capped at pytest + ruff — AGENTS §8/§10; D-031 parks the candidate here.
  The type-discipline values are law from iter-1 via
  `docs/blueprint/phase0.md` §1; the tool is optional).
- `perf-1` 10k-tick timing profile — DONE iter-30
  (iter-30-perf1-profile): `scripts/profile_harness.py` (story phase +
  grid-aligned waits to the target; clean + cProfile double-run with a
  byte-compare probe — held at 10k ticks). 10k ticks ≈ 0.01–0.02 s
  write-side (~9.8k events/s), read side ≈ 0.017 s; cost is
  event-linear, schema validation dominates the per-event write cost;
  target met with ~3 orders of margin — no structural work warranted at
  v0.1 scale. Numbers owner: `docs/TECH_NOTES.md` §8.
- `balance-1` 1000-headless-sim distribution harness — DONE iter-6:
  `scripts/balance_harness.py` runs the gate playscript 1000× across
  seeds 100–1099 (director off), folds each log through
  `core/metrics.py`, emits a distribution table for M1–M5 +
  emergent_chains + suspicion peaks per NPC + destroyed-locations.
  Baseline (1000 seeds): M5 p50=0.77, emergent_chains p50=20, M3_mean
  p50=13.81, M1 p50=0.24 — full table at
  `output/balance_1000_seed100_off.txt` (gitignored runtime artifact;
  reproducible). KI#4 closed.
- `doc-1` VISION freeze review after the phase-0 verdict — DONE
  iter-26 (the phase-1 gate's doc-actualization sweep): the frozen text
  verified against phase-1 reality — the 3-layer shape, the call-budget
  law, the honest limits all hold; no changes, the freeze stands.
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
- `pack-2` Arson-on-ashes guard (iter-2a audit note) — DONE iter-29
  (D-061): the `spot_available` door check (the closed precondition
  set's 15th test, layer-param lint-checked) — arson on a destroyed or
  fully-burning location is an `intent_rejected` no-op with
  `failed_test target.spot_available`, never the no-ignition success
  that pretended the world changed; the door-outcome vocabulary's
  fourth axis. The seed-41 corpus probe flipped with it (renamed
  `arson_on_a_destroyed_yard_is_door_rejected`).
- `pack-3` Sci-Fi setting candidate (owner sketches, 2026-08-30 chat;
  parked, not scheduled): frontier station / ark fleet / lawless
  asteroid belt / derelict megastructure. The sketches map
  mechanic-for-mechanic onto what already exists — watch rotations →
  station shifts, spreading rumors → leaks & paranoia, arson →
  sabotage / hull breach, theft → cargo/data theft, status markers →
  drunk/weary/afraid analogues per setting, pair axes + factions, watch
  change knowledge transfer → shift handover. Zero core change by
  design (INV-3's substance: a second pack must require zero ENGINE
  changes); blocked until the 2nd-setting gate (phase 6, same trigger
  as `pack-1`, ROADMAP §6).
- `ref-N` Reference deep dives — the plan table and the per-file index live
  in `docs/REFERENCES_DEEP.md` §1/§2 (single owner). All ref-1..ref-13
  items are done — status one-liners below; ref-16 (agent-memory-atlas,
  owner-supplied) was absorbed inside iter-8a, no solo iteration
  (`docs/ref/agent_memory_atlas.md`):
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
  - ref-17 DF designed experience (the player-facing half; owner-requested
    research pass, D-022 exception) — done (iter-8d) →
    `docs/ref/df_design.md`
- Candidates (owner-request only — D-022 law: no doc pass without a fresh
  owner request; both are synthesis-only today, cited via
  `CORE_DESIGN_RESEARCH.md` §2 and marked as such in the blueprint donor
  stacks):
  - `ref-14` The Sims — proprietary; patterns-from-papers only (D-015).
  - `ref-15` Prom Week — academic paper + GDC talk; no code repo.

## Done

- iter-40 · 2026-09-01 · drama-1 event grammar, predicate + weight layer — detail: worklog + the owning docs (D-row where named).

- iter-39 · 2026-09-01 · dir-4 multi-channel policies — detail: worklog + the owning docs (D-row where named).

- iter-35 · 2026-09-01 · phase-2 gate — detail: worklog + the owning docs (D-row where named).

- iter-34 · 2026-09-01 · owner-requested planning-layer audit — detail: worklog + the owning docs (D-row where named).

- iter-33 · 2026-09-01 · parse-1 batch 2 — detail: worklog + the owning docs (D-row where named).

- iter-32 · 2026-09-01 · parse-1 validation beats — detail: worklog + the owning docs (D-row where named).

- iter-31 · 2026-09-01 · phase-2 parser door — detail: worklog + the owning docs (D-row where named).

- bg-4 · 2026-08-31 · cost notes — detail: worklog + the owning docs (D-row where named).

- iter-30 · 2026-08-31 · perf-1 — the 10k-tick timing profile — detail: worklog + the owning docs (D-row where named).

- iter-29 · 2026-08-31 · pack-2 — the arson-on-ashes door check — detail: worklog + the owning docs (D-row where named).

- iter-28 · 2026-08-31 · tune-2 — the crime cascade renders on the — detail: worklog + the owning docs (D-row where named).

- iter-27 · 2026-08-31 · tune-1 — the rest action + the story-critical — detail: worklog + the owning docs (D-row where named).

- iter-25 · 2026-08-31 · validation beats — session 10, the — detail: worklog + the owning docs (D-row where named).

- iter-24 · 2026-08-31 · validation beats — session 9, the day-2 — detail: worklog + the owning docs (D-row where named).

- iter-23 · 2026-08-31 · validation beats — session 8, the — detail: worklog + the owning docs (D-row where named).

- iter-22 · 2026-08-31 · validation beats — session 7, the theft half — detail: worklog + the owning docs (D-row where named).

- iter-21 · 2026-08-31 · validation beats — session 6, the alarm — detail: worklog + the owning docs (D-row where named).

- iter-20 · 2026-08-30 · universality pass — the transition-layer and — detail: worklog + the owning docs (D-row where named).

- iter-19 · 2026-08-30 · owner-requested audit of two pasted spatial — detail: worklog + the owning docs (D-row where named).

- iter-18 · 2026-08-30 · validation beats — session 5, the arson half — detail: worklog + the owning docs (D-row where named).

- iter-17 · 2026-08-30 · validation beats — session 4, crime cascade — detail: worklog + the owning docs (D-row where named).

- iter-16 · 2026-08-30 · validation beats — session 3 — detail: worklog + the owning docs (D-row where named).

- iter-15 · 2026-08-30 · presence & entity cards — st-1 landed — detail: worklog + the owning docs (D-row where named).

- iter-14 · 2026-08-30 · validation beats — session 2 — detail: worklog + the owning docs (D-row where named).

- iter-13 · 2026-08-30 · validation beats — session 1 — detail: worklog + the owning docs (D-row where named).

- iter-12 · 2026-08-30 · the mediator session loop — detail: worklog + the owning docs (D-row where named).

- bg-5 · 2026-08-30 · owner-requested verdict on a pasted external integration spec — detail: worklog + the owning docs (D-row where named).

- iter-11c · 2026-08-30 · owner-requested re-check of iter-11b — detail: worklog + the owning docs (D-row where named).

- iter-11b · 2026-08-30 · roadmap stress-test re-verified + problems 4–6 — detail: worklog + the owning docs (D-row where named).

- iter-11a · 2026-08-29 · post-iter-11 audit — detail: worklog + the owning docs (D-row where named).

- iter-11 · 2026-08-29 · texture promotion door — detail: worklog + the owning docs (D-row where named).

- iter-10a · 2026-08-29 · post-iter-9/10 audit sync — detail: worklog + the owning docs (D-row where named).

- iter-10 · 2026-08-29 · scene-ledger LLM-free half — detail: worklog + the owning docs (D-row where named).

- bg-1 · 2026-08-29 · DF export pipeline CLOSED — detail: worklog + the owning docs (D-row where named).

- iter-8h · 2026-08-29 · owner-directed derived-index micro-pass — detail: worklog + the owning docs (D-row where named).

- iter-8g · 2026-08-29 · DF coverage audit — detail: worklog + the owning docs (D-row where named).

- iter-8f · 2026-08-29 · audit-fix after iter-8e — detail: worklog + the owning docs (D-row where named).

- iter-8e · 2026-08-28 · DF empirical F7/F8 survey on the owner's two world exports — detail: worklog + the owning docs (D-row where named).

- iter-8d · 2026-08-28 · DF designed-experience deep dive — detail: worklog + the owning docs (D-row where named).

- iter-8c · 2026-08-28 · owner-requested audit of iter-8a/8b: every claim reproduced; KI#30 — detail: worklog + the owning docs (D-row where named).

- iter-8a · 2026-08-28 · scene-ledger design pass — detail: worklog + the owning docs (D-row where named).

- iter-8 · 2026-08-28 · BRIEF_SPEC + brief assembler — detail: worklog + the owning docs (D-row where named).

- iter-7 · 2026-08-28 · phase-1 intake — detail: worklog + the owning docs (D-row where named).

- iter-6a · 2026-08-28 · owner-requested code audit of iter-5/6: every gate claim reproduced — detail: worklog + the owning docs (D-row where named).

- iter-6 · 2026-08-28 · phase-0 gate — detail: worklog + the owning docs (D-row where named).

- iter-5 · 2026-08-28 · chronicle & CLI — detail: worklog + the owning docs (D-row where named).

- iter-4a · 2026-08-28 · owner-requested code audit of iter-3/4 — detail: worklog + the owning docs (D-row where named).

- iter-4 · 2026-08-28 · director + goal ticker — detail: worklog + the owning docs (D-row where named).

- iter-3 · 2026-08-28 · knowledge, relations, expectations — detail: worklog + the owning docs (D-row where named).

- iter-2a · 2026-08-28 · owner-requested code audit of iter-1/2: KI#13–16 fixed — detail: worklog + the owning docs (D-row where named).

- iter-2 · 2026-08-28 · actions — detail: worklog + the owning docs (D-row where named).

- iter-1 · 2026-08-28 · core plumbing — detail: worklog + the owning docs (D-row where named).

- iter-0 · 2026-08-25 · docs & tooling bootstrap. — detail: worklog + the owning docs (D-row where named).

- iter-0b · 2026-08-25 · docs review + external source catalog — detail: worklog + the owning docs (D-row where named).

- iter-0c · 2026-08-25 · REFERENCES rev v2 merge — detail: worklog + the owning docs (D-row where named).

- iter-0d · 2026-08-25 · infra restore: `.gitignore`, package skeleton, smoke tests — detail: worklog + the owning docs (D-row where named).

- iter-0e · 2026-08-25 · `docs/CORE_DESIGN_RESEARCH.md` — detail: worklog + the owning docs (D-row where named).

- iter-0f · 2026-08-25 · manifesto absorption — detail: worklog + the owning docs (D-row where named).

- iter-0g · 2026-08-25 · research pass: Q1–Q3 absorbed — detail: worklog + the owning docs (D-row where named).

- iter-0h · 2026-08-26 · `docs/REFERENCES_DEEP.md` + D-024 anti-drift policy; ref batch 1 — detail: worklog + the owning docs (D-row where named).

- iter-0i · 2026-08-26 · ref-1 DF worldgen solo dive. — detail: worklog + the owning docs (D-row where named).

- iter-0j · 2026-08-26 · ref-2 C:DDA solo dive + cap policy rewrite — detail: worklog + the owning docs (D-row where named).

- iter-0k · 2026-08-26 · per-ref split into `docs/ref/` — detail: worklog + the owning docs (D-row where named).

- iter-0l · 2026-08-26 · ref-3 Paradox scripting solo dive. — detail: worklog + the owning docs (D-row where named).

- iter-0m · 2026-08-26 · ref-4 pacing trio dive — detail: worklog + the owning docs (D-row where named).

- iter-0n · 2026-08-26 · ref-5 event/narrative grammar family dive. — detail: worklog + the owning docs (D-row where named).

- iter-0o · 2026-08-26 · ref-6 roguelike emergence trio dive — detail: worklog + the owning docs (D-row where named).

- iter-0p · 2026-08-26 · ref-7 LLM-agent precedents dive — detail: worklog + the owning docs (D-row where named).

- iter-0q · 2026-08-26 · ref-8 + ref-9 six-file batch — detail: worklog + the owning docs (D-row where named).

- iter-0r · 2026-08-26 · ref-10 + ref-11 six-file batch — detail: worklog + the owning docs (D-row where named).

- iter-0s · 2026-08-27 · ref-12 UAP webapp dive — detail: worklog + the owning docs (D-row where named).

- iter-0t · 2026-08-27 · ref-13 live-char-guide dive — detail: worklog + the owning docs (D-row where named).

- iter-0u · 2026-08-27 · references distillation: `docs/BLUEPRINT.md` + `docs/blueprint/{phase0,phases}.md` — detail: worklog + the owning docs (D-row where named).

- iter-0v · 2026-08-27 · owner-requested audit patches: INV-2 rewritten per D-028 — detail: worklog + the owning docs (D-row where named).

- iter-0w · 2026-08-27 · owner-requested post-reference concept realignment: D-029 — digestion complete, skeleton — detail: worklog + the owning docs (D-row where named).

- iter-0x · 2026-08-27 · owner-requested reference-influence traceability audit: verdict "load-bearing" recorded in STATUS — detail: worklog + the owning docs (D-row where named).

- iter-0y · 2026-08-27 · owner-requested content-principles pass: D-030 — detail: worklog + the owning docs (D-row where named).

- iter-0z · 2026-08-27 · owner-requested quality round: D-031 — INVARIANT-CORE v3 + Elegant Solutions absorbed surgically — detail: worklog + the owning docs (D-row where named).
