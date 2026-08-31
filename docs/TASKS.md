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

### iter-12 · the mediator session loop — done (D-055)

The owner's engine verdict (2026-08-30): no SoW, no llama.cpp now —
the dev-time narrator is the external agent over a file contract
(call_<N>.md → reply_<N>.json); the repo stays LLM-free (INV-4
unchanged). Landed: the call/response documents, the beat cycle
(retire→sync→call→reply→delta→intents→promotions), noun resolution
+ withdrawals, the L12 ladder, `narrate` session commands. Detail:
`worklog.md` iter-12 + `docs/VALIDATION_SPEC.md` §7.1 + D-055.

### iter-13 · validation beats — done (session 1)

The first live agent-in-the-loop session through `narrate` (seed 125,
11 beats): **0 canon violations**, every refusal family probed and
caught; KI#44 fixed (accepted-beat verdicts now print as the `BEAT`
summary lines — the phase-1 exit numbers are countable in live play);
the phase-1 regression set committed
(`tests/fixtures/narrator_beats.json` — 16 cases distilled from the
session, replayed through the real mediator cycle). Live evidence for
`st-1`: the brief carries no presence block (the narrator cannot
legally name who is in the room). The exit criterion needs volume:
more sessions across seeds/scenarios, findings extend the corpus.
Detail: `worklog.md` iter-13 + `docs/VALIDATION_SPEC.md` §7.1.

### iter-14 · validation beats — done (session 2)

Session 2 over the theft-and-arson scenario (seed 8, 12 beats, 22 supported
claims, **0 canon violations**): the families session 1 left uncovered were
probed live and all caught — `event_type_mismatch`, `cannot_know`,
`stale_ref` (after a scene close), the full regen-exhaustion ladder (2/2 →
dry, L12), a door-rejected intent (a well-formed world-impossible steal
commits `intent_rejected`), rebased intents, and the delta vocabulary at
the beat level (pin, retire + establish, idempotent no-op). The corpus grew
16 → 25 cases: every validator refusal reason is now pinned at the beat
level. Detail: `worklog.md` iter-14 + `docs/VALIDATION_SPEC.md` §7.1.

### iter-26 · phase-1 gate — done (verdict: PASS, D-058)

The owner's quality-first close ("cleanup, re-verification, doc
actualization before closing the gate — I chase quality, not speed"):
the full ROADMAP §5 protocol re-run on evidence — 610 green + ruff
clean; T1 byte-identity + fixture guard; T8 single-factor A/B (OFF =
26 chains; ON M1=0.417 / M2=0.500); T7 chronicle re-read (the chains
read causally; the decay/wariness repetition is the noise floor —
tale_gate stays the owner-gated tune-1 knob). Exit criterion met with
margin: 109 live beats / 0 canon violations / corpus 105 green; no
kill-criteria hit. DECISIONS collapsed 41→30 per D-034 in the same
iteration (7 family merges, all 58 IDs resolve); D-058 = the verdict;
KI#50 fixed; `doc-1` VISION freeze review closed clean; the pre-mediator
Done entries collapsed to one-liners (AGENTS §6; TASKS 683→477, back
under the cap). Phase 2 (Parser, mode C) may open — the
phase-2-vs-polish call stays the owner's. Detail: worklog iter-26 +
`docs/DECISIONS.md` D-058 + `docs/TEST_PLAN.md` §4.

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

### bg-2 · event taxonomy — todo

- 100–300 interesting events across ~16 types (birth, death, murder, theft,
  betrayal, artifact creation, site destruction, war, journey, captivity,
  escape, founding, item loss, madness, transformation, catastrophe); per
  event: participants, place, cause, witness, long-term consequence,
  expressibility in our ontology → `docs/TAXONOMY.md`.
- AC: ≥100 entries. Honest note baked in: causality is *reconstructed* from
  `event_collections` + role fields, not parsed. Sampling frame sharpened
  (iter-8e): measured type distribution + ambiguity grounding live in
  `docs/TECH_NOTES.md` §3.1 (micro tails, unique collection refs,
  slayer-less deaths). Query home since bg-1 closed: the SQLite sink
  (`scripts/df_import.py` → `output/df_world_<stem>.sqlite3`; recipe
  `docs/TECH_NOTES.md` §3.2) — participant/grouping/name queries run on
  the DB, not by re-parsing XML.

### bg-3 · briefer spike — todo

- Mini-briefer "tell battle X from figure Y's POV, knowing only Y's own
  records" + reverse validation (invented-facts count, regeneration count) +
  retrieval stress test (tens of MB of XML).
- AC: harness runs; numbers in `docs/TECH_NOTES.md`. Expectation to keep
  honest: DF canon is macro-dense and micro-empty — this validates briefer
  *mechanics*, not micro-event interestingness (measure that on our own dry
  chronicle). Y's own records = the `event_participant` index
  (`docs/TECH_NOTES.md` §3.2; 4 ms measured on the large world).

### bg-4 · cost notes — todo

- Park et al. 2023 + "Generative Agent Simulations of 1,000 People" (2024)
  figures → `docs/TECH_NOTES.md` cost section.

### bg-6 · SoW integration audit — todo (owner-deferred)

- Read-only pass over `github.com/jofizcd/Soul-of-Waifu` (registered
  2026-08-30 at the owner's request; the owner defers integration "until
  unavoidable"): extension points for a separate simulation chat mode
  (a new mode vs. invasive edits), where llama.cpp sits, what the
  frontend must NOT own (the dumb-terminal contract, VISION §10).
  Output: a TECH_NOTES section + the `SOW_INTEGRATION_SPEC` sketch.
  Natural slot: just before the phase-1 gate (ROADMAP §6 bans
  SoW-specific work earlier; never blocks track A).

## Infra backlog (pick by need)

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

- iter-30 · 2026-08-31 · perf-1 — the 10k-tick timing profile
  (iter-30-perf1-profile): the harness (story + grid-aligned waits;
  clean + cProfile double-run, byte-compare probe held at 10k ticks);
  10k ticks ≈ 0.01–0.02 s write-side / 0.017 s read-side, event-linear
  cost, schema validation the per-event hot spot; no structural work
  warranted at v0.1 scale. Detail: worklog iter-30 +
  `docs/TECH_NOTES.md` §8.

- iter-29 · 2026-08-31 · pack-2 — the arson-on-ashes door check
  (iter-29-pack2-spot-available): the `spot_available` precondition
  test (the target location holds an unburning spot of the declared
  layer — the same condition the ignite resolver keys on) + the
  arson requires row + the layer-param lint; the seed-41 corpus probe
  flipped to `intent_rejected` (the fourth door-outcome axis); 626→629
  green, ruff clean. Detail: worklog iter-29 + D-061 +
  INTENT_SCHEMA §3.

- iter-28 · 2026-08-31 · tune-2 — the crime cascade renders on the
  cards (iter-28-tune2-card-markers): `status_markers` → the prop-path
  `card_markers` table (threshold rows + value rows, closed marker
  surface, lint-checked); the segment is `markers=`; the pack ships
  `wary` (suspicion ≥ 25, aligned with the suspect flip) +
  `suspect`/`caught` on the player's card; the scene_delta half is
  lawful blindness (blind-NPC — the card is the narrator's surface,
  the delta window the player's); 619→626 green, ruff clean. Detail:
  worklog iter-28 + D-060 + BRIEF_SPEC §3.4/§6.

- iter-27 · 2026-08-31 · tune-1 — the rest action + the story-critical
  importance hook (iter-27-tune1-rest-importance; the owner's
  finish-phase-1 directive): `recuperate` resolver + `status_effects`
  pack block (rest = the KI#4 fatigue counter-play, 13th action);
  `importance.story_critical_events` (+2 hook, lint-closed) with the tale
  gate following low→medium — D-045(b)'s rule-first law; the day1_full
  tale 47 events → 14 lines (decay/wariness noise floor gone, pinned);
  the 1000-sim baseline re-run IDENTICAL; T1 fixture byte-identical;
  610→619 green, ruff clean. Detail: worklog iter-27 + D-059.

- iter-25 · 2026-08-31 · validation beats — session 10, the
  witnessed-steal-then-alarm chain (iter-25-validation-beats-10;
  seed 93, 6 accepted beats + 2 refused-and-caught documents, 34
  supported claims, 5 intents fed, 0 canon violations): sessions 4
  and 6 back to back, the last uncovered combination in the phase-1
  corpus vocabulary — a total-failure steal (everyone saw:
  suspicion 35 room-wide, crime_status suspect at the failure) → a
  silent second steal → the t=360 rotation pushes both guards to 55
  (past the document_check threshold 50) → **the director releases
  `director_0000` live for the first time in a narrate session**
  (the v0.1 stub wait claimable by id+type — a canon event no card
  or brief surfaces) → the arson-as-distraction through the door
  (fire_started + alarm_raised raised_by the relief guard + fear 40
  claimable per NPC; the cause actor hears his own alarm; the
  outgoing guard stays blind to the fire — the transfer bounded by
  what the holder holds) → flee_caught at t=535 (the door batch
  drained the fire cascade first; crime_status stays suspect at
  55 < the arrest threshold 75; the purse stays on the thief's card
  through the catch). Corpus 99→105; 604→610 green, ruff clean;
  live beats 101→109 — the corpus moves to the phase-1 gate review
  (ROADMAP §2). Detail: worklog iter-25 +
  `docs/VALIDATION_SPEC.md` §7.1.

- iter-24 · 2026-08-31 · validation beats — session 9, the day-2
  return under burned-yard knowledge (iter-24-validation-beats-9;
  seed 41, 13 accepted beats + 2 refused-and-caught probes, 39
  supported claims, 0 canon violations) — the entry backfilled at
  iter-25 (the iter-24 commit skipped its TASKS one-liner — the
  iter-22 precedent): the day-1 theft-and-arson chain lands at
  t=1452 (day-2 morning post-second-rotation); the day-1 canon
  events all claimable by id+type under day 2 (canon never closes,
  1440-tick gap); the burned yard's `destroyed` flag
  canon-from-birth state-claimable; the arson-on-a-destroyed-yard
  case is the pack-2 backlog's first live probe (no-ignition
  success — distinct from session 8's spotless-street
  `field_nonempty` failure); the door-outcome vocabulary completes
  its three axes (`target.carries_flagged` — no flagged target);
  the third watch_change hands `purse_missing` to the relief guard
  (transfer_decay_steps=1 under day 2); the tune-2 boundary
  re-pinned under day 2. Corpus 84→99; 589→604 green, ruff clean;
  the phase-1 ≥100-beat exit criterion HIT (86→101 live beats); the
  sandbox narrate-session recipe landed in the STATUS FAQ. Detail:
  worklog iter-24 + `docs/VALIDATION_SPEC.md` §7.1.

- iter-23 · 2026-08-31 · validation beats — session 8, the
  arson-after-theft chain (iter-23-validation-beats-8; seed 85, 12
  beats + 3 refused-and-caught probes, 49 supported claims, 0 canon
  violations): the take → silent steal → drop_break → fire chain
  under a successful-theft context (sessions 4/5/7 tied); both
  prizes on one coat; the departure token claimable at the yard
  arrival; the unseen arson — the rotation hands the crime half
  across the watch change (purse_missing inferred/exact →
  told/partial, the trail + noise tokens, suspicion 20 both guards,
  crime_status unknown post-inference at 20 < 25) while the fire
  half never crosses (guard-side fire tokens all token_absent — the
  transfer bounded by what the holder holds); the arsonist's
  fear-0 calm + the cause-actor blindness refusal (the ignition
  exception from both sides); the flee fed through the door from a
  burned-out yard (unpursued; the purse leaves the fire, the lamp
  stays); the street arson attempt commits `intent_rejected`
  (claimable by id+type — a new door-outcome action kind); the
  maid's autonomous urgency event claimable by id+type; the §3
  market leg pinned unreachable (tune-3 family). Corpus 70→84; the
  batch-boundary lesson in the STATUS FAQ (a distilled case must
  reproduce the live batch structure — the intent beat +
  between-steps vocabulary). 575→589 green, ruff clean. Detail:
  worklog iter-23 + `docs/VALIDATION_SPEC.md` §7.1.

- iter-22 · 2026-08-31 · validation beats — session 7, the theft half
  under the presence machinery (iter-22-validation-beats-7; seed 54,
  11 beats, 24 supported / 1 refused-and-caught, 0 canon
  violations): the pre-steal arrival snapshot; a successful first
  steal moves the purse silently (no suspicion, `crime_status` stays
  `unknown` — the silent vs failed-steal fork, complement to session
  4); the `expectation_violation` event claimable by id+type
  (complement to session 5's fire-event-by-id); post-inference
  `purse_missing` positively claimable for both guards
  (inferred/exact + told/partial — the `transfer_decay_steps=1` law
  live); the suspicion axis state-claimable but card-invisible (the
  `tune-2` boundary re-pinned); the second steal after watch rotation
  returns `intent_rejected` (target moved — distinct from session 4's
  second-steal-success); the stolen purse rides a plain move to the
  backyard (KI#46 in a non-pursuit context); the
  witness-cannot-know-`purse_missing` refusal pins the inference
  boundary. Corpus 59→70; 564→575 green, ruff clean. Detail: worklog
  iter-22 + `docs/VALIDATION_SPEC.md` §7.1.

- iter-21 · 2026-08-31 · validation beats — session 6, the alarm
  cascade (iter-21-validation-beats-6; seed 33, 12 beats + 2
  refused-regen probes, 53 supported / 0 canon violations): the
  complement to session 5's solo-arson — with witnesses present the
  cascade fires (`alarm_raised` + the fear spike 40 + the `afraid`
  card marker; the cause actor hears `fire_alarm_in_<loc>` while
  blind to `fire_in_<loc>`); the §3 watch-change handover live (the
  rotation carries the purse, `knowledge_transfer` hands the fire
  record set — told, one fidelity step down; the briefing moves
  knowledge, not fear). Finding → `tune-3` backlog row
  (`shouting_near_<loc>` structurally unreachable in v0.1). Corpus
  51→59; 556→564 green, ruff clean. Detail: worklog iter-21 +
  `docs/VALIDATION_SPEC.md` §7.1.

- iter-20 · 2026-08-30 · universality pass — the transition-layer and
  scene-line vocabularies become pack data (iter-20-universality;
  KI#48 + D-057): follow-up kinds/flags/values, the spreading
  `spot_state`, the spread `halt_flag`, and the director's threat
  vocabulary moved from core code into `rules.json::transitions`
  (behavior byte-identical — the T1 fixture untouched); `layout`
  landed as a location pack field rendered on the scene line via
  `brief.present_entities.scene_line_fields` (canon-from-birth, no
  seeding); KI#48 records the iter-19 factual error (canon_slot
  reads BOTH prop sources — projection and pack record). Proven by a
  synthetic `rot` layer with a wholly different vocabulary in
  test_transitions.py. 547→556 green, ruff clean. Detail: worklog
  iter-20 + `docs/BRIEF_SPEC.md` §3.4/§6 + D-057.

- iter-19 · 2026-08-30 · owner-requested audit of two pasted spatial
  analyses (iter-19-spatial-audit; docs-only, D-022 exception):
  verdict ~85–95% repo-true (time/space/canon-vs-texture mechanics
  confirmed; the second text's corrections repo-exact); omissions
  found — the ref-9/ref-10 lift-target + grid drift family is wider
  than ref-9-c (KI#47: 9 grid phrases fixed; phantom lift-targets
  stanced in the STATUS FAQ), travel is queue-cheap today (clock
  jump-ahead); the layout claim was corrected by KI#48 at iter-20
  (canon_slot guards pack fields without seeding). Resolution: the
  `st-6` spatial backlog row (travel, phase-5-gated; layout landed
  iter-20). Detail: worklog iter-19 + `STATUS.md`.

- iter-18 · 2026-08-30 · validation beats — session 5, the arson half
  over the cards (iter-18-validation-beats-5): the fire cascade
  (fire_started / fire_spread / smoke_rising / location_burned_out)
  is in canon regardless of who stood where; the observable surface
  splits by location — cause-actor blind to ignition (token_absent on
  `fire_in_<loc>`), absent NPCs cannot perceive fire, no alarm in the
  canonical solo-arson scenario, an unmodeled `fire_intensity` prop
  reads `insufficient_data` (UAP), and a canon event is claimable by
  id+type even when the brief was silent. Corpus 41 → 51; KI#46
  deleted per AGENTS §5. Detail: worklog iter-18 + VALIDATION_SPEC
  §7.1.

- iter-17 · 2026-08-30 · validation beats — session 4, crime cascade
  (iter-17-validation-beats-4): the cascade's observable half reads
  through the cards — witnesses, per-witness knowledge, the purse
  carried across cards and through the flee; the suspicion half is
  invisible through the brief (tune-2 backlog row, owner's call).
  Corpus 32 → 41. Detail: worklog iter-17 + VALIDATION_SPEC §7.1.

- iter-16 · 2026-08-30 · validation beats — session 3 (iter-16-
  validation-beats-3): the st-1 acceptance probes over the iter-15
  presence machinery all hold (quiet-beat room naming, the
  absent-presence refusal, sighting + pair tokens, scene-change card
  follow, the promoted prop, post-rotation cards; seed 7, 7 beats,
  0 canon violations); KI#46 found live and fixed (the rotation left
  carried items behind — `rotation_plan` now rides `movement_changes`).
  Corpus 25 → 32. Detail: worklog iter-16 + VALIDATION_SPEC §7.1.

- iter-15 · 2026-08-30 · presence & entity cards — st-1 landed (iter-15-presence, D-056): the `present_entities` 8th brief block (entity cards) + the write-side arrival-snapshot twin; the T1 fixture regenerated in the same commit. Detail: D-056 + `docs/BRIEF_SPEC.md` §3.4.

- bg-5 · 2026-08-30 · owner-requested verdict on a pasted external integration spec (bg-5-spec-verdict; docs-only): every citation audited, no repo drift; two adoptions land as the st-4 Script-Tax and st-2 repetition-promotion backlog amendments. Detail: git worklog bg-5.

- iter-11c · 2026-08-30 · owner-requested re-check of iter-11b (iter-11c-audit; docs-only): every claim reproduced against the code; KI#43 precision family closed (MECW figure + arrival-snapshot grammar + the commit-gate cycle guard). Detail: git worklog iter-11c.

- iter-11b · 2026-08-30 · roadmap stress-test re-verified + problems 4–6 (iter-11b-stress-test-verified; docs-only): the reported-but-never-landed pass reconstructed (KI#42) and re-verified; MECW/nuance/reasoning resolved as blueprint §1/§5/§7 + BRIEF_SPEC §9 + the st-1..st-5 backlog. Detail: git worklog iter-11b.

- iter-11a · 2026-08-29 · post-iter-11 audit (iter-11a-audit-fix): KI#39 texture-take chronicle prose, KI#40 unique-slot claims survive promotion, KI#41 canon-slot overlap incl. pack-modeled fields; +lint hardening. Detail: git worklog iter-11a.

- iter-11 · 2026-08-29 · texture promotion door (iter-11-texture-door; D-054): the narrator boundary's LLM-free half — the intent door's texture path, the `texture_noun` test, real `unique_slots`, the laundering pins. Detail: D-054 + `docs/INTENT_SCHEMA.md` §2/§3.

- iter-10a · 2026-08-29 · post-iter-9/10 audit sync (iter-10a-audit-sync): KI#37 doc-sync family (worklog re-trim, AGENT_NAVIGATION/README synced) + KI#38 the INV-3 stoplist scans `brief/`. Detail: git worklog iter-10a.

- iter-10 · 2026-08-29 · scene-ledger LLM-free half (iter-10-scene-ledger; D-053): `brief/ledger.py` + the `scene_texture` 7th block + the committed golden delta fixture + pack lint. Detail: D-053 + `docs/BRIEF_SPEC.md` §3.3.
- bg-1 · 2026-08-29 · DF export pipeline CLOSED (bg-1-sqlite-sink; D-051): the SQLite sink (typed cores + EAV + `event_participant` + generic records) over the validated survey core; cross-validated on the owner's 2.38 GB world; KI#36 fixed. Detail: D-051 + `docs/TECH_NOTES.md` §3.2.
- iter-8h · 2026-08-29 · owner-directed derived-index micro-pass (iter-8h; D-050): two derived indexes beside their single mutation funnels + four scan eliminations; golden fixtures byte-identical. Detail: D-050.
- iter-8g · 2026-08-29 · DF coverage audit (owner-requested): `scripts/df_survey.py --audit` — the coverage census + UNDOCUMENTED markers (KI#36's two matrix gaps caught on first run); the first `tests/test_df_survey.py`. Detail: `docs/ref/df_legends_xml.md` + git worklog iter-8g.
- iter-8f · 2026-08-29 · audit-fix after iter-8e (owner-approved): KI#34 truncated-export survival (RecoveringReader, loud PARTIAL) + KI#35 the 101st type vocabulary re-anchor. Detail: git worklog iter-8f.
- iter-8e · 2026-08-28 · DF empirical F7/F8 survey on the owner's two world exports (owner-requested): `scripts/df_survey.py` + measured numbers in TECH_NOTES §3.1; KI#33 schema-drift fix. Detail: `docs/TECH_NOTES.md` §3.1 + git worklog iter-8e.
- iter-8d · 2026-08-28 · DF designed-experience deep dive (owner-requested research pass, ref-17): `docs/ref/df_design.md` — six enchantment pillars, the F1–F10 flaw taxonomy, the successor trade-off matrix, the layer-adding thesis. Detail: `docs/ref/df_design.md`.
- iter-8c · 2026-08-28 · owner-requested audit of iter-8a/8b: every claim reproduced; KI#30 (the D-018c false citation family), KI#31 (blueprint wording debts), KI#32 (sync misses) fixed. Detail: git worklog iter-8c.
- iter-8a · 2026-08-28 · scene-ledger design pass (owner-requested continuity question): `docs/ref/agent_memory_atlas.md` written + the scene ledger designed into blueprint §1 (D-048). Detail: D-048.
- iter-8 · 2026-08-28 · BRIEF_SPEC + brief assembler (iter-8; D-047): the trigger-fired spec + the deterministic assembler (pure functions of the log, zero RNG) + the pack brief contract + lint. Detail: D-047 + `docs/BRIEF_SPEC.md`.
- iter-7 · 2026-08-28 · phase-1 intake (owner-requested retrospective + plan reorganization): DECISIONS collapsed 46→30 per D-034; TASKS regained what-next ownership; KI#25–28 intake fixes. Detail: git worklog iter-7.
- iter-6a · 2026-08-28 · owner-requested code audit of iter-5/6: every gate claim reproduced (the 1000-sim baseline exactly, T8 OFF = 26 chains); KI#22–24 fixed; D-046. Detail: D-046 + git worklog iter-6a.
- iter-6 · 2026-08-28 · phase-0 gate (iter-6-gate): `docs/TEST_PLAN.md` + `core/metrics.py` + the T1 fixture guard + the T8 A/B suite + `scripts/balance_harness.py`; verdict PASS (D-045). Detail: D-045 + `docs/TEST_PLAN.md`.
- iter-5 · 2026-08-28 · chronicle & CLI (iter-5): the deterministic tracery engine (ShufflePool, modifiers, conditionals — cosmetic stream only) + the chronicle as a pure function of the log + the batch/interactive CLI. Detail: git worklog iter-5.
- iter-4a · 2026-08-28 · owner-requested code audit of iter-3/4 (iter-4a): 60-seed sweep × director on/off clean; KI#17–20 fixed; D-041. Detail: D-041 + git worklog iter-4a.
- iter-4 · 2026-08-28 · director + goal ticker (iter-4): the consequence buffer + triggers + narrative entropy + the on/off switch; the P2b goal ticker; states decay passes; arrest resolution. Detail: `docs/DIRECTOR_SPEC.md` + D-038/D-039/D-040.
- iter-3 · 2026-08-28 · knowledge, relations, expectations (iter-3): the derived KnowledgeView + telling reaction + crime reactions + watch rotation + the pair map + expectation violations; D-037. Detail: D-037 + git worklog iter-3.
- iter-2a · 2026-08-28 · owner-requested code audit of iter-1/2: KI#13–16 fixed (the `_commit` pre-write gate D-035, the per-layer spread singleton D-036, pack-lint gaps). Detail: D-035/D-036 rows + git worklog iter-2a.
- iter-2 · 2026-08-28 · actions (iter-2): the 12 resolvers + the registry, pack-driven preconditions/checks/knowledge, intent OCC + lifecycle, the scheduler DAG, the generic transition engine, the INV-3 stoplist. Detail: git worklog iter-2.
- iter-1 · 2026-08-28 · core plumbing (iter-1): RngBank, clock, queue, the JSONL log + header, fold/projection, the pack loader + lint, the playscript runner; T0/T1 minimal + architecture fitness. Detail: git worklog iter-1.
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
