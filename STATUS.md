# STATUS — canonsim

Iteration: 6 (`iter-6-gate`) · Phase: 0 — simulator without LLM ·
Date: 2026-08-28 · **Phase-0 gate: PASS** (deferred: bg-1..bg-4, pack-1,
`doc-1` VISION review — all explicitly post-gate per `ROADMAP.md` §2).

The gate iteration (`docs/blueprint/phase0.md` §6, `TEST_PLAN.md`,
`MVP_SCOPE.md` §16): `docs/TEST_PLAN.md` — the trigger-fired spec
(T0–T8 formalization + M1–M5 definitions + the gate protocol + the
UAP 7-hole crosswalk + the §3 schema-bump migration procedure).
`core/metrics.py` — M1–M5 + the emergent-chain count as PURE
FUNCTIONS of `(events, projection)` (Mesa `DataCollector` inverted:
the simulator emits, the metric reads; the simulator never knows a
metric exists — L3 derive-never-store). System classification is pack
data (`rules.json::metrics.system_of_type` — INV-3: system names are
MVP_SCOPE §5 mechanic words, not setting nouns). `tests/test_metrics.py`
— 24 unit tests covering M1–M5 + the emergent-chain walk (the
director-injected link breaks the chain; the world-actor-only root
excludes the chain; the player-seeded world fire IS emergent).
`tests/test_t1_determinism.py` extended with the iter-6 fixture-
regeneration guard (TEST_PLAN §1.1): two new tests pin (a) the
committed fixture's header `schema_version` equals the current
`schemas/event.schema.json` `$id` version, and (b) a fresh regeneration
into tmp diffed byte-by-byte against the committed fixture. A schema
bump without a fixture regen fails here loudly. `tests/playscripts/
day1_full.json` — the T8 gate playscript (seed 125: take → 2 steals
→ wait 720 → move backyard → drop_break → wait 720). `tests/test_t8_ab.py`
— single-factor A/B (only the director flag changes), ≥3 emergent
chains OFF (baseline 26), director_0000 fires ON, M5 non-zero OFF,
M3 mean ≥2 both runs. `scripts/balance_harness.py` — KI#4 close: the
1000-sim distribution harness (`scripts/` per AGENTS §9); outputs a
metrics + suspicion-peaks + destroyed-locations table to
`output/balance_<N>_seed<S>_<on|off>.txt` (gitignored runtime
artifact; reproducible from the seed range). 298 tests green (+34),
ruff clean, golden fixture byte-identical.

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index; the log writer is the
  only canon-write path (D-031).
- INV-2 Determinism: single point of randomness control — one master seed;
  named streams derived via the RngBank (`stable_hash` = sha256-based);
  no wall-clock; `sorted()` iteration; fixed `PYTHONHASHSEED`; queue key
  `(tick, sub_order, actor_id)`; cosmetic draws never desync canon replay
  (D-028 — the law text itself now carries this; AGENTS.md is the single
  reading owner).
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#4 · balance harness — CLOSED iter-6: `scripts/balance_harness.py`
  runs the gate playscript 1000× across seeds 100–1099 (director off),
  folds each log through `core/metrics.py`, emits a distribution table for
  M1–M5 + emergent_chains + suspicion peaks per NPC + destroyed-locations.
  Baseline numbers (the iter-6 verdict evidence, full table in
  `output/balance_1000_seed100_off.txt`): M5 p50=0.77 (world not
  player-centered — strong pass); emergent_chains p50=20 (gate ≥3
  easily met); M3_mean p50=13.81 (depth ≥2 kill-criterion met); M1
  p50=0.24 (non-trivial). The three iter-2/4/5 observations now have
  numbers: (a) v0.1 environment checks CAN auto-succeed at low difficulty
  (the take-after-steal failure on seed 32 is the counterexample); (b)
  non-PC share is 73–83% across 1000 seeds (formally M5); (c) player
  fatigue IS monotonic (no rest action — pack data issue, not a code
  bug; first rest-action candidate lands in iter-7+ as `pack-2`-style
  pack data, NOT a core change).
- KI#21 · draft templates drifted from the shipped event contract
  (iter-5 found+fixed) — CLOSED iter-5: `suspicion_changed` had
  actor/target inverted (the iter-3 reaction events carry actor=watcher,
  target=suspect; the iter-0c draft assumed the opposite); the fallback
  line used `[` as decoration — a collision with tracery's `[key:value]`
  save syntax (now `(t {t})`); the steal line named the victim, not the
  stolen object (`{stolen}` = outcome.stolen). Fixed as pack data while
  completing the templates; no renderer existed before iter-5, so no
  output ever showed the wrong lines.
- KI#17 · autonomous intents advanced the playscript (iter-4a found+fixed)
  — CLOSED iter-4a: `_feed_next` fired after ANY intent rejection or
  completion, including urgency/director NPC entries (an iter-1 assumption
  — only the player had intents — that iter-4's queue-riding autonomy
  silently broke; step 3 committed before step 2's event, seeds 1/2/3/7/11).
  Fix: the feed gates on `entry.actor_id == player_id` (D-041). Invisible
  to the suite: loop e2e runs the 58-tick no-beat fixture; urgency tests
  use single-step scripts — the runner×autonomy interaction was untested.
- KI#18 · crime-status flip could downgrade caught → suspect (iter-4a
  found+fixed) — CLOSED iter-4a: the flip guard was `status != suspect`, so
  after an (irreversible, T4) `caught`, a LATER watcher's novel crime token
  crossing `status_suspect_at` flipped the suspect back to `suspect`. Fix:
  the flip checks the pack's ordered `status_values` progression
  (`_at_or_past`); suspicion itself still moves — only the flip is guarded.
- KI#19 · `states.reset_on_rotation` declared but not implemented
  (iter-4a found+fixed) — CLOSED iter-4a: rules.json flagged fatigue
  `reset_on_rotation: true` and states.py's docstring promised the reset,
  but no code read the key (doc↔repo drift, §3). Fix: `rotation_resets`
  resets flagged axes to 0 for the watch participants on the watch_change
  event, and the decay baseline is per-axis last-change-by-any-committer
  (a rotation-fresh NPC no longer gains fatigue for pre-reset ticks).
  Semantics choice: BOTH participants reset (fatigue is gain-only — an
  incoming-only reset would peg the outgoing's fatigue at the ceiling
  across days); owner may veto (D-041).
- KI#20 · dead pack keys with no reader (iter-4a found+fixed) — CLOSED
  iter-4a: `crime_watch.document_check` (the v0.1 flat-timer remnant the
  director replaced), `relations.suspicion_thresholds.document_check_at`
  (mirrored the director hook's trigger value), `states.fear.spike_on_alarm`
  (duplicated `transitions.fire.alarm.fear_spike`). All three removed — the
  number keeps its single live owner (D-024); the smoke escalation-order
  assertion re-pointed at `director.hooks.possible_document_check.trigger`.
  No runtime behavior change (nothing read the dead keys).

## FAQ / Pitfalls

- **Crossings fire in tick order, not by type (iter-4 law, D-038).**
  Rotations (iter-3) and beats (iter-4: decay / urgencies / director
  release) all ride the clock-crossing discipline — but they interleave
  by tick, not as "all rotations first then all beats". A beat at T=720
  between rotations at T=360 and T=1080 fires BETWEEN them, not after
  both. The log writer's tick-monotonicity invariant forbids out-of-order
  commits; the loop's crossing logic is `min(candidates)` per iteration,
  picking whichever rotation-or-beat is soonest. The same rule applies
  to any future clock-crossing system (per-tick states passes if they
  arrive, decay sub-passes, etc.).
- **Autonomous intents enqueue at entry.tick, not beat_tick (iter-4
  law, D-039) — and they NEVER advance the playscript (iter-4a law,
  KI#17).** The beat fires retroactively (T=beat_tick) when the
  loop is processing an entry at T=entry.tick > beat_tick. The entry
  was already popped; the queue discipline forbids enqueuing at a tick
  the clock has already passed (regression). Urgency and director
  intents thus enqueue at `entry.tick` with sub_order=NPC_REACTION —
  conceptually "after the beat, at the moment the world resumes
  moving". Decay events commit directly at `beat_tick` (their canonical
  tick in the log); they don't go through the queue. And the runner
  feeds the NEXT playscript step only on the PLAYER's own step endings
  — an autonomous intent's completion or door rejection must never
  `_feed_next` (the KI#17 bug: step 3 proposed while step 2 was still
  in flight).
- **Director releases ride the intent door, not the canon door (D-037,
  phase0 §4 "Objective broadcast").** A released hook produces an
  IntentData (id `director_<N>`) enqueued band NPC_REACTION; the front
  door validates preconditions, runs OCC, rolls checks, and emits the
  event through the resolver. A rejected director intent emits an
  `intent_rejected` no-op event with `cause_intent = "director_..."`.
  The director never moves actors, changes state, or bypasses the
  Intent→Event front-door — the world's logic is one mechanism, not
  two. Same door for urgencies (id `urgency_<N>`).
- **Reactions dispatch from the commit door; novelty is per (knower,
  token) (iter-3 law, D-037).** `Simulator._commit` feeds the knowledge
  index and runs `_react` (crime → arrest resolution → telling) for
  EVERY committed event — no call site can forget a reaction, and
  cascades terminate because reaction events carry no records beyond
  what legitimately spreads. Suspicion reacts only to tokens the
  knower did not already hold — repeated identical evidence never
  re-escalates; escalation is the pack's token vocabulary. The arrest
  resolution rides the same door — the attempt is a fact, the
  resolution is its completion, dispatched immediately after the
  arrest_attempt event commits. Scheduled beats (rotations,
  urgencies, director) chain cause = last written event; reactions
  chain cause = the trigger; expectation violations chain cause = the
  axis-specific mover (carrier vs position).
- **System passes scan the whole projection, not the events that seeded
  them (KI#16 lesson).** `spread_tick` rolls every burning location with
  unburning spots — including fires ignited after the pass started. Any
  per-layer bookkeeping (cause maps, "already told" flags) must therefore
  be global to the layer and mergeable by new ignitions, never a frozen
  snapshot carried in the queue payload. Same rule for every per-tick
  system iter-3+ adds (knowledge, relations, states passes). The iter-4
  states decay pass follows the same rule: it scans ALL npcs, not just
  the ones who fired events since the last beat — and its per-axis
  baseline is the tick of the LAST event that changed that axis (any
  committer: decay beat, use effect, rotation reset), so a mid-beat
  reset is respected (KI#19: a rotation-fresh NPC gains no fatigue
  for pre-reset ticks).
- **Hardcoded `from_` is a desync waiting to happen (KI#13 lesson).** A
  resolver that hardcodes a `from_` value instead of reading the
  projection breaks the moment a legal sequence moves that prop before
  the resolver runs. Two disciplines: read current values from the
  projection (the `_divert`/`_use_item` pattern) and make repeat effects
  idempotent (the `follow_up_draft` None pattern). The `_commit` gate
  (D-035) makes the failure loud BEFORE the write — the log never holds
  a desynced event — but the resolver should not rely on the net. The
  iter-4 arrest resolution reads `crime_status` from the projection for
  the `from_` value (not hardcoded "suspect" — a future pack could
  extend the status enum).
- **INV-3's stoplist scope (iter-2 interpretation, test-owned).** The
  stoplist (`tests/test_inv3_stoplist.py`) bans **setting** nouns — the
  invariant's named examples plus entity names and location/item
  vocabulary — matched as code segments (`guard`, `npc_guard_01`,
  `loc_guardroom` all trip; English derivations like 'guards' do not).
  Mechanic words (take, move, talk, fire, stealth — MVP_SCOPE §7's own
  vocabulary) stay legal; pack data is never grepped. The word list is
  tied to the pack by a self-check, so it cannot rot silently. iter-4
  note: generic status axis names (`fatigue`, `intoxication`, `fear`,
  `injury`) are mechanic words, NOT setting nouns — they appear in
  code and in the pack's `rules.states` alike.
- **The loud/soft front-door line.** Malformed playscript steps (unknown
  fields, missing targets, bad spot names, unknown methods) raise
  `RunnerError` — author bugs crash. Well-formed but world-impossible
  intents emit `intent_rejected` no-op events — character attempts are
  facts. Moving a check from one side to the other is a contract change,
  not a refactor (INTENT_SCHEMA §9). Director and urgency intents go
  through the same door — a director intent that fails preconditions
  emits an `intent_rejected` event (the budget is consumed); an urgency
  that fails preconditions stays silent (no event — the world's noise
  floor absorbs it; the urgency is autonomous, not director-driven).
- **The golden T1 fixture is env-pinned.** The log header records the
  Python version (`AGENTS.md` §10 — same-environment determinism only), so
  `tests/fixtures/plumbing_smoke_seed42.jsonl` byte-compares only on the
  Python it was generated on. On an interpreter bump the byte-compare
  fails **by design**: regenerate (Simulator, seed 42, commit `"0000000"`,
  playscript `tests/playscripts/plumbing_smoke.json`) and commit the new
  fixture together with the env change. The same procedure applies to a
  deliberate behavior change that alters emitted bytes — iter-4 kept
  the fixture byte-identical (the 58-tick plumbing_smoke scenario
  crosses no beat — no decay, no urgency, no director release), which
  is the regression proof that the iter-4 director rewiring changed no
  iter-1..3 canon for the baseline scenario.
- **A ref citing a spec section it never contained is drift, not history.**
  The pre-D-028 FAQ rule protects *real* historical wording — verify with
  `git log -S "<phrase>" -- <file>` before calling something history.
  iter-0aa example: `df_worldgen.md` cited "MVP_SCOPE §4.1: 1 tick = 12
  in-world minutes" — §4.1 is the locations table and never owned time
  numbers; the fabricated figure leaked into `phase0.md` §1 and contradicted
  MVP_SCOPE §8's own arithmetic (1440 ticks/day). Diagnostic: any
  cross-doc numeric claim is re-derived from its claimed owner before it
  enters a prescriptive doc.
- **Where the code-quality bar lives (D-031).** Law: `AGENTS.md` §4
  (invariants + the canon-write privilege line) + §9 (DoD: conventions per
  `MVP_SCOPE.md` §18 — type hints, no `print()` outside `cli/` — and the
  L13/L14 elegance laws). Constitution: `docs/BLUEPRINT.md` §2 — L13
  (abstraction cost gate, Rule-of-Three tiers, 4-branch registry threshold)
  and L14 (elegance standard + review checklist). Build clauses:
  `docs/blueprint/phase0.md` §1 (type discipline, fail-fast, the
  architecture fitness test), §2 (ActionResolver registry), §6 (tests
  document the invariants; negative tests prove them). Executable:
  `tests/test_architecture.py` (iter-1) + the stoplist test (iter-2).
  Rationale: D-031; sources: `docs/REFERENCES.md` §15. The two owner texts
  are absorbed, not filed — no `docs/ARCHITECTURE.md` /
  `TYPE_DISCIPLINE.md` / `TESTING_PHILOSOPHY.md` will be created (the
  D-018 pattern); a new canonical layer is the named anti-pattern.
- **GitHub upload / git hygiene (the KI#1 family).** "Add files via
  upload" on GitHub drops `.gitignore` and every dir without tracked
  files; after any upload, verify `.gitignore` exists. And
  `git status --short` shows changes *vs HEAD*, not what is *in HEAD* —
  a file in the working directory may not be committed at all. After
  any structural change, run `git ls-files <path>` to confirm what is
  actually tracked (the diagnostic for KI#1-class losses and "the file
  exists but tests can't find it" surprises).
- **Content/tone questions → D-030 + the `PACK_SPEC.md` sketch row.** The
  start pack for phase 0 is `tavern_pack` v0.1 as scoped (`MVP_SCOPE.md`
  §4–§7 own the counts); tone is data asymmetry inside the existing systems,
  not new systems. Growing the pack or writing a pack spec before its
  trigger = scope creep (AGENTS §2.4; SPECS_BACKLOG header rule). Grim/romance
  material accumulates in the sketch row + `pack-1` (TASKS infra backlog)
  until the PACK_SPEC trigger fires (phase 6 / a 2nd setting).
- **Doc-loop alarm vs owner-requested research.** Twenty-six docs iterations
  in a row would normally force a stop (AGENTS §2.5). Owner-requested passes
  are the explicit exception (D-022) — the documented condition is a fresh
  owner request. iter-0aa was the twenty-sixth (and last); iter-1..5 are
  code — the alarm does not fire on code iterations.
- **Four places, four jobs (D-027).** `docs/REFERENCES.md` catalogs sources
  (license, URL, phase gating); `docs/CORE_DESIGN_RESEARCH.md` §2 carries
  the one-line synthesis per source; `docs/ref/<source>.md` carries the
  concrete mechanics; `docs/BLUEPRINT.md` + `docs/blueprint/` carry the
  cross-reference resolutions and donor combinations per build component.
  Drift rule: link, never restate; cite ledger row IDs (e.g. "per RNG-1")
  instead of re-deriving a resolution.
- **Copy-vs-owner drift is evidence, not prescription.** Pre-D-028 RNG
  wording ("one `random.Random(seed)` instance") quoted in `docs/ref/*`
  is HISTORICAL — it documents what the donor comparison was made
  against; the reading owner of INV-2 is `AGENTS.md` §4 (D-028). Same
  pattern for licenses: the `REFERENCES_DEEP.md` §2 index is NOT the
  source of truth — `REFERENCES.md` (the catalog) is; before flipping
  any ref-N row todo→done, verify the license column against the
  catalog. Verify with `git log -S "<phrase>"` before "fixing" what
  looks like history (KI#6 pattern).
- **Substance over line count (D-025) + per-ref split (D-026).** The cap is
  600 with the §6.1 substance filter as the real law — filler is cut
  always; named systems, real field lists, type enumerations, per-source
  verdicts are never cut to fit.
- **"Ref graveyard" check (iter-0x audit method).** To verify the reference
  corpus still influences the plans (not just exists as a folder), grep a
  sample of ledger terms across the planning docs — ShufflePool,
  ASSERT_stable, Influence Boundary, promoteTile, bm25, copy-from — over
  `docs/BLUEPRINT.md` + `docs/blueprint/` + `docs/TASKS.md` +
  `docs/SPECS_BACKLOG.md`: every term must land in at least one planning
  doc; the concrete mechanics stay owned by `docs/ref/` by design (link,
  never restate — D-027). Verified iter-0x; re-run at the phase-0 gate
  review.
- **The render pass is a pure function of the log (iter-5 law, CHRON-1).**
  Every render entry point (chronicle / scene card / entity view) builds
  a fresh `RngBank` seeded from the LOG HEADER's seed plus fresh
  `ShufflePool`s — the same log renders the same bytes in any process,
  any call order, any `PYTHONHASHSEED` (verified). Within one chronicle
  pass the pools advance line by line, so a growing log keeps its
  rendered prefix identical — the session delta-print contract rides on
  this. Templates own the words: `[` is tracery save syntax
  (`[key:value]`), literal brackets in template text are impossible by
  law (ticks in prose use `(t N)`); the renderer writes nothing to the
  log (INV-1) and draws only cosmetic (RNG-1, audit-tested).
- **A session is one opened Simulator; the world moves only through the
  queue it seeds (iter-5 law).** `core/loop.py`'s public doors:
  `open()` writes the header once; `run_steps()` is a self-contained
  feed-and-drain cycle, callable repeatedly (the CLI pattern);
  `close()` ends the run. A step-by-step session and a batch run of
  the same steps produce byte-identical logs (tested). The seed binds
  at open — `seed <n>` restarts into a NEW log (INV-5); `directors
  on|off` swaps the live policy (`policy_from_rules` owns the
  entropy-floor read). Between commands the clock stands still:
  beats/rotations fire on crossings during entry processing, exactly
  as in batch.
- **The metric is a pure function of the log (iter-6 law, M1–M5).**
  `core/metrics.py` reads `(events, projection)`; the simulator
  emits, the metric reads, the simulator never knows a metric exists
  (L3 derive-never-store — Mesa `DataCollector` inverted). M1
  cross-system share reads the pack's `metrics.system_of_type` table
  + the state-change prop-prefix map (mechanic vocabulary, FAQ note
  in INV-3 — system names are MVP_SCOPE §5 mechanic words). M2
  released-to-seeded ratio on the ON run; the OFF run is 0 by
  construction (D-005 hygiene — the OFF run is "no releases", not
  "no director"). M3 walks `cause` links to null; depth is the chain
  length. M4 counts repeated `(type, actor)` bigrams + distinct
  `knows` token share (RimWorld's repetitive-tale problem,
  measured). M5 non-PC event share on the OFF run. The emergent-chain
  count walks `cause` links back to a player event through a non-PC,
  non-director tail of length ≥ 2 — a director-injected link breaks
  the walk (the director is causally upstream; this is not emergent),
  a world-actor-only root (no player upstream) excludes the chain,
  a player-seeded world fire IS emergent (the player dropped the
  lamp; the world ignited it).
- **The fixture-regeneration guard is the iter-6 T1 discipline
  (TEST_PLAN §1.1).** Two tests pin the contract: (a) the committed
  fixture's header `schema_version` equals the current
  `schemas/event.schema.json` `$id` version — a schema bump without a
  fixture regen fails here loudly; (b) a fresh run regenerates the
  fixture into tmp, diffed byte-by-byte against the committed file —
  a behavior change that altered emitted bytes fails here. The §3
  migration procedure (regenerate fixtures + commit them with the
  schema change in the SAME iteration + a migration note in
  `EVENT_SCHEMA.md` §8) is forced, never punted. A breaking schema
  change without fixture regen is the loud failure the guard is
  designed to catch — the alternative is silent drift between the
  schema, the committed fixtures, and the runtime.
- **The T8 single-factor A/B (iter-6 law, live-char one-change rule).**
  The gate runs the same playscript (`tests/playscripts/day1_full.json`,
  seed 125) with only the director flag changed between runs: ON
  fires `director_0000` (the document-check release when Doren's
  suspicion crosses 50 via the inference at watch rotation), OFF
  fires zero director releases but seeds the same hooks (D-005
  hygiene — the OFF run is "no releases", not "no director"). The
  OFF run produces ≥3 emergent chains (baseline 26); the gate
  minimum is 3 (a regression that drops emergence below the
  threshold fails loudly — investigate urgency / rotation /
  crime-reaction regressions). The ON and OFF logs are byte-different
  (the director's release leaves a trace — the positive complement
  to T1: same script + same seed, different policy → different
  canon).
- **The balance harness is a script, not a test (iter-6 law, KI#4
  close).** `scripts/balance_harness.py` (committed; `output/*.txt`
  gitignored runtime artifact, reproducible from the seed range):
  runs the gate playscript 1000× across seeds 100–1099 (director
  off — the T8 baseline), folds each log through `core/metrics.py`,
  emits a distribution table for M1–M5 + emergent_chains + suspicion
  peaks per NPC + destroyed-locations. The kill-criteria in
  `MVP_SCOPE.md` §16 ("Events without consequences", "Knowledge does
  not affect behavior", "The director produces noise instead of
  causal complications") are operationalized as M3 mean ≥ 2, M1
  non-trivial, M2 non-zero — directionality first (D-019), numbers
  from data. The harness is NOT in pytest because a 1000-sim sweep
  would dominate the suite's runtime; the gate playscript's
  `tests/test_t8_ab.py` runs the SINGLE seed (125) and asserts the
  gate minimum (≥3 emergent chains).

## Next step

**Phase-0 gate: PASS** (verdict in `worklog.md` iter-6 entry). The
simulator produces facts; the chronicle reads them from the log; the
world acts without the player; old events surface later via the
reaction cascade + watch rotation; losses are permanent (the backyard
stays destroyed). Track A is feature-frozen at phase-0 scope.

**Track B (background) is now unblocked** for parallel LLM-circuit
spikes on foreign canon: `bg-1` (DF export pipeline), `bg-2` (event
taxonomy), `bg-3` (briefer spike), `bg-4` (cost notes). None of
these block track A — they exercise the briefer/validator/renderer
on Dwarf Fortress Legends XML so the phase-1 narrator arrives with
real data, not speculation.

**Phase 1 (narrator over the log)** is the next track-A work; the
phase-0 gate must pass first (`ROADMAP.md` §2 — it has). The
pre-trigger `BRIEF_SPEC.md` / `VALIDATION_SPEC.md` sketches in
`SPECS_BACKLOG.md` are the design surface; they fire AT phase 1
start, not before (`SPECS_BACKLOG.md` header rule). The
`PACK_SPEC.md` trigger stays at phase 6 / 2nd setting (`pack-1` in
the infra backlog is the grim/romance tavern pack candidate).

Post-gate housekeeping deferred to the phase-1 intake (none block
phase 0): `doc-1` VISION freeze review; the rest-action candidate
(`pack-2`-style pack data); `qa-1` mypy (owner-gated; dev tooling is
capped at pytest + ruff per AGENTS §8/§10, D-031); `ci-1` GitHub
Actions; `perf-1` 10k-tick timing profile.
