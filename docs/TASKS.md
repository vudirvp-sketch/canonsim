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

### iter-18 · validation beats — done (session 5, the arson half)

Session 5, the arson-half session over the cards (seed 20, 10 beats,
29 supported / 4 refused-and-caught / 1 unverifiable, **0 canon
violations**): the fire cascade (fire_started / fire_spread /
smoke_rising / location_burned_out) is in canon regardless of who
stood where; the observable surface splits by location — the
cause-actor never gets `fire_in_<loc>` (rules.json transitions.fire.
knowledge.started `except: cause_actor` — token_absent on the PC's
own ignition knowledge), the same-location PC gets the spread/smoke/
burnout records via saw/exact, an absent NPC's `fire_in_<loc>` claim
is token_absent (different location → no record), no alarm fires in
the canonical solo-arson scenario (no occupants at the fire
location → `fire_alarm_in_<loc>` and the fear markers stay unclaimable),
an unmodeled `fire_intensity` prop reads `insufficient_data` (the
honest-verdict law, UAP), and a canon event is claimable by id+type
even when the PC's brief was silent about it (the validator checks
the log, not the brief's perception). Corpus 41 → 51. Detail:
`worklog.md` iter-18 + `docs/VALIDATION_SPEC.md` §7.1.

### iter-17 · validation beats — done (session 4, crime cascade)

Session 4, the crime-cascade session over the presence machinery (seed
15, 10 beats, 32 supported / 2 refused-and-caught, 5 intents fed, **0
canon violations**): witnesses present with per-witness knowledge
claimable (the noticed reach), the purse carried moving across cards
(guard → player) and riding the flee (KI#46's read-side, pinned), the
blind-witness refusal (heard ≠ saw) and the uninferred `purse_missing`
refusal both caught live; **the suspicion half is invisible through
the brief** — `relations.suspicion` is not a card marker (the marker
lookup is status-prefixed; a suspicion row is not even expressible in
pack data today) and `suspicion_changed` never enters scene_delta →
the `tune-2` backlog row, owner's call. Corpus 32 → 41. Detail:
`worklog.md` iter-17 + `docs/VALIDATION_SPEC.md` §7.1.

### Phase-1 tuning backlog (post-assembler, owner-gated)

- `tune-1` rest action as pack data (player fatigue is monotonic over
  long waits — KI#4/balance observation) + the D-045(b) importance-rule
  knob (hooks on story-critical events, NOT `tale_gate`); both refresh
  the 1000-sim baseline when tuned.
- `tune-2` crime-cascade observability (iter-17 session finding): the
  suspicion axis and the `crime_status` flip are invisible through the
  brief — no card marker (the marker table's axis lookup is
  status-prefixed, so a `relations.suspicion` row is not even
  expressible in pack data) and `suspicion_changed` never enters
  scene_delta. Candidate = a pack marker row for suspicion/crime-status
  + the tiny status-prefix generalization in the card renderer; whether
  the narrator SHOULD see NPC-interior suspicion at all is the owner's
  call (mode-A epistemics vs readable crime tension).

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
- `perf-1` 10k-tick timing profile (target: seconds, not minutes; the
  iter-8h micro-pass landed the six locally-provable asymptotic wins —
  the profile stays the gate for structural work).
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

- iter-15 · 2026-08-30 · presence & entity cards — st-1 landed
  (iter-15-presence, D-056; the owner's session delegation "pick what
  is best"): the 8th brief block `present_entities` (entity cards:
  present set + status markers + visibly-carried items + promoted
  props + directed pair tokens; the scene line keeps canon-born
  texture visible post-promotion) + the write-side twin — the
  actor-held per-present-target `knows` expansion on `move` (the
  arrival snapshot; INTENT_SCHEMA §7, KI#43's grammar). Zero new event
  types; the T1 fixture regenerated (+10 records, the iter-3
  precedent); 2 pair-relation seeds. 502→520 green, ruff clean.
  Detail: worklog iter-15 + `docs/BRIEF_SPEC.md` §3.4 + D-056.

- bg-5 · 2026-08-30 · owner-requested verdict on a pasted external
  integration spec (bg-5-spec-verdict; docs-only, D-022 counter = 3):
  every citation audited against the repo + live-char-guide — no repo
  drift; not integrated as text (renames of the MECW/st-1/st-2
  vocabulary, fatigue emulation re-rejected per ref-13 weakness (4),
  invented AP-16 and ownerless figures); two adoptions land as the
  st-4 Script-Tax and st-2 repetition-promotion backlog amendments.
  Detail: worklog bg-5.

- iter-11c · 2026-08-30 · owner-requested re-check of iter-11b
  (iter-11c-audit; docs-only, D-022): verdict sound — every claim
  reproduced against the code (453 green, ruff clean, byte-identical;
  perception tokens, prop-birth shape, O(N)/beat folds, `records_of`,
  canon-slot check, citations, caps, KI lifecycle); KI#43 precision
  family closed (MECW figure → TECH_NOTES §2 single owner +
  provenance; arrival snapshot → actor-held per-present-target
  `knows` expansion per INTENT_SCHEMA §7/§10; container cycle guard
  += the commit gate, D-035). Resolutions stay owner-verdict-pending.
  Detail: worklog iter-11c + `STATUS.md`.

- iter-11b · 2026-08-30 · roadmap stress-test, re-verified + problems
  4–6 (iter-11b-stress-test-verified; docs-only, D-022): the reported
  but never-landed pass reconstructed (KI#42 — archive expired) and
  re-verified against the code (3 sharpenings: perception emits coarse
  tokens, no snapshot semantics; a D-054 promotion births a prop, not
  a portable entity; write-side LOD was undesigned) + MECW/nuance/
  reasoning resolved (call-budget law, thinking = ephemeral texture,
  transcript-tail contract, mode-B knower parameterization, presence/
  entity cards); landed as blueprint §1/§5/§7 + BRIEF_SPEC §9 (+4
  deferrals, cap held) + GROUP_SPEC sketch + the st-1..st-5 backlog.
  453 green, ruff clean, no code changes. Detail: worklog iter-11b.

- iter-11a · 2026-08-29 · post-iter-11 audit (iter-11a-audit-fix): KI#39
  texture-take chronicle prose (`{target?…|…}` conditional templates +
  the `texture_slot` derived slot — canon lines byte-unchanged), KI#40
  unique-slot claims survive promotion (golden case 17), KI#41 canon-slot
  overlap includes pack-modeled fields; +lint hardening, +texture-path
  OCC attribution test, +doc sync (INTENT_SCHEMA §9, AGENT_NAVIGATION,
  TASKS). 443→453 green, ruff clean, fixtures byte-identical. Detail:
  worklog iter-11a.

- iter-11 · 2026-08-29 · texture promotion door (iter-11-texture-door;
  D-054): the narrator boundary's LLM-free half — the intent door's
  texture path, the `texture_noun` test, real `unique_slots`, the
  laundering + unique_slot golden pins (8/8 refusal reasons). 435→443
  green. Detail: worklog iter-11 + docs/INTENT_SCHEMA.md §3.

- iter-10a · 2026-08-29 · post-iter-9/10 audit sync (iter-10a-audit-sync):
  KI#37 doc-sync family — worklog re-trimmed to the line cap (iter-10
  file count 15→16), AGENT_NAVIGATION/README synced, the golden-coverage
  claim qualified; KI#38 — the INV-3 stoplist test scans `brief/`.
  435 green, ruff clean. Detail: worklog iter-10a.

- iter-10 · 2026-08-29 · scene-ledger LLM-free half (iter-10-scene-ledger;
  D-053): `brief/ledger.py` + the `scene_texture` 7th brief block + the
  BRIEF_SPEC §9 atomic flip + the committed golden delta fixture + pack
  lint. 435 green (was 390; +45). No new KIs. Detail: worklog iter-10.
- bg-1 · 2026-08-29 · DF export pipeline CLOSED (bg-1-sqlite-sink; D-051):
  `scripts/df_import.py` loads a world into SQLite (AC met) over the
  validated survey core — typed cores + EAV + `event_participant` +
  generic JSON records; truncation policy owned (flagged partial default,
  `--strict` abort); cross-validated on the owner's new large world
  (2.38 GB → 898 MB in 174 s; every count reproduces the survey);
  `tests/test_df_import.py` (11 tests). KI#36 fixed (UNDOCUMENTED audit
  marker; matrix gaps `artifact` + `historical_era`). Plus-companion
  import = documented deferral (TECH_NOTES §3.2), not backlog scope.
  Survey half history: iter-8e/8f/8g (git).
- iter-8h · 2026-08-29 · owner-directed derived-index micro-pass (an
  external patch list verified against the code first — every item
  proven semantics-preserving): two derived runtime indexes beside
  their single mutation funnels (`KnowledgeView` `who → token →
  source-ids` in `add` — `holds` O(1), `before_source` preserved;
  Simulator `(entity, prop) → tick` in `_commit` — the decay baseline
  without the per-beat log scan) + four scan eliminations
  (scene-delta window break on tick-monotonicity, `salient()` top-1
  `max`, `occ_breaking_cause` one forward fold from the proposal
  point, director `entropy` once per `releases()`); D-050;
  micro-benchmarks 1.9×–664×; 338→340 green, ruff clean, golden
  fixtures byte-identical. Detail: worklog iter-8h + D-050.
- iter-8g · 2026-08-29 · DF coverage audit (owner-requested: "is anything
  being missed in the giant DF exports?"): `scripts/df_survey.py --audit`
  mode — coverage census (per-section per-record-tag counts + every
  unique child-tag set per record tag, a structural fingerprint bounded
  by DF record uniformity — typically 1-3 variants; >3 = drift signal);
  HANDLED records (F7/F8 detail) marked, UNHANDLED records (site, entity,
  region, artifact, written_content, …) carry their child-tag sets so
  bg-1's SQLite sink can plan field extraction without re-parsing a 5 GB
  export; replaces head/middle/tail positional sampling strictly — every
  variant captured, not three positions; runs in the same single
  streaming pass. First `tests/test_df_survey.py` (9 tests) pins the four
  load-bearing invariants (sanitize, recover, census, audit render) on a
  tiny synthetic DF-like XML. Coverage matrix: `docs/ref/df_legends_xml.md`.
  329→338 green, ruff clean, fixture byte-identical. No new KIs.
- iter-8f · 2026-08-29 · audit-fix after the iter-8e audit (owner-approved
  option A): KI#34 — truncated-export survival in `scripts/df_survey.py`
  (tail check + RecoveringReader closing-tag synthesis at EOF, loud
  PARTIAL warnings; ground-truth validated — the complete 4.95 GB
  re-export of the same small-dense region3-00500 world reproduces the
  recovered prefix counts exactly) + KI#35 — "site tribute forced" →
  war-geopolitics (101st type; vocabulary count re-anchored to
  TECH_NOTES §3.1, third-world numbers added). 329 green, ruff clean.
- iter-8e · 2026-08-28 · DF empirical F7/F8 survey on the owner's two world
  exports (owner-requested, the D-022 exception; closes iter-8d's not-done
  item): `scripts/df_survey.py` (sanitize + stream parsing core for bg-1)
  + measured numbers distilled into `docs/TECH_NOTES.md` §3.1 (single
  owner) + F7/F8 verdict links in `docs/ref/df_design.md` + KI#33
  schema-drift fix in `docs/ref/df_legends_xml.md` (actual `<event>`/
  `<eventcol>` tags, naming duality, single-parent trees — the
  many-to-many claim corrected). 329 green, ruff clean.
- iter-8d · 2026-08-28 · DF designed-experience deep dive (owner-requested
  research pass, the D-022 exception; docs-only — iter-9 stays the code
  iteration; ref-17): `docs/ref/df_design.md` — six enchantment pillars
  (P1–P6), flaw taxonomy F1–F10 with root causes (every flaw is a missing
  layer — salience/pacing/audience-epistemology/LOD/continuity — not wrong
  simulation), successor trade-off matrix (RimWorld/KoDP/SoS/Versu/Rain
  World/SS13/…: each "fix" amputates a pillar), the structural read
  (layer-adding is the canonsim thesis), reader-as-knower symmetry, bg-1
  hardening + bg-2 ambiguity-as-data + bg-3 corpus-division guidance; every
  flaw mapped to an existing mechanism or recorded phase. No new KIs (all
  cross-claims verified against the repo); 329 green, ruff clean.
- iter-8c · 2026-08-28 · owner-requested audit of iter-8a/8b: every
  claim reproduced (329 green, ruff clean, T1 byte-identical; the 8b
  false-alarm verdicts verified against pre-8b git state; atlas MIT
  re-verified). 3 KIs fixed: KI#30 `D-018c` false citation (never
  resolved — the KI#23/#28 family) → D-018 ×4 sites; KI#31 blueprint
  §1 wording debts (stale 8a pinned-eviction remnant vs
  ledger-never-evicts; lifecycle transitions {active, pinned} →
  terminal); KI#32 sync misses (TASKS ref-N + ref-16; BLUEPRINT
  BRIEF-1 atlas donor line). Verdict: no rework of iter-1..8 — the
  7th block lands additively. Docs-only (D-022 exception); 329 green,
  ruff clean, fixture byte-identical.
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
