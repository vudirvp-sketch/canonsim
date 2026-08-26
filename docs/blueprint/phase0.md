# blueprint/phase0.md — Phase-0 Build Blueprint (iter-1..iter-6)

> The combined donor design for TavernSim v0, contradiction-free. Entry
> point + resolution ledger: [`docs/BLUEPRINT.md`](../BLUEPRINT.md) (row IDs
> like RNG-1 cited here). Contracts: `MVP_SCOPE.md` (scope), `EVENT_SCHEMA.md`
> (event fields) — this file never restates their fields, it sequences their
> donors. Per-source evidence: `docs/ref/<source>.md`, linked per row.

## 1. iter-1 · core plumbing (seed, rng, clock, queue, log, fold, packs)

**Combined design.**

- `core/rng.py` — the RngBank (RNG-1). One constructor argument (the master
  seed); named streams derived deterministically:
  `stream(name) = random.Random(stable_hash(f"{seed}:{name}"))` with
  `stable_hash(s) = int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],
  "big")` — sha256-based, environment-independent (stream derivation never
  relies on `PYTHONHASHSEED`; INV-2 per D-028) —
  `substantive` (canon) and `cosmetic` (render-only) are the two phase-0
  streams. Guards lifted from the donors: an `assure(name)` context manager
  (Brogue `assureCosmeticRNG`) that swaps and restores the active stream —
  canon-emitting code paths run under `assure('substantive')`, render paths
  under `assure('cosmetic')`; an `audit()` context manager (DCSS
  `ASSERT_stable`) asserting zero draws on a chosen stream inside the scope
  (the test guard — T5 wraps perception checks in it); `peek()` non-advancing
  reads for tests; per-stream draw counters — the substantive counter is the
  replay fingerprint T1 compares. A draw from the wrong stream is a bug of
  INV-2 severity; the guards make it loud instead of silent. **Lint rule
  (substantive by definition):** any draw whose value lands in an event's
  `outcome`/`state_changes`/`knowledge` is substantive — a cosmetic draw on a
  canon path fires the `assure` guard with Brogue's
  `brogueAssert(rogue.RNG == RNG_SUBSTANTIVE)` loudness.
- `core/clock.py` — integer tick from 0; day-phase boundaries and
  ticks-per-action are pack rule data (`rules.json`), never constants in
  code (INV-3). One tick ≈ 12 in-world minutes; a full day ≈ 1440 ticks
  (`MVP_SCOPE.md` §8 owns the numbers).
- `core/queue.py` — one `heapq` (SCHED-1). Entry key `(tick, sub_order,
  actor_id)` plus a monotonic `seq` as the never-compared-before last
  tiebreak so payloads are never ordered. `sub_order` bands, as constants:
  system passes (fixed per-tick order, band 0–99) < player intents (100s) <
  NPC reactions (200s) < scheduled completions (300s). Within a band,
  `actor_id` orders. KeeperRL's players-before-nonplayers deque discipline
  collapses into the band numbers; rot.js's bare `_time` key is the named
  collision hazard the 3-tuple fixes.
- `core/ids.py` — gap-free event ids `ev_0000…` and actor handles with
  `(id, generation)` packing (entt `entt_traits`) so a recycled handle is
  distinguishable in the queue key.
- `core/log.py` — append-only JSONL writer. Header line first (Brogue's
  36-byte no-wall-clock recording header is the shape; our fields per
  `EVENT_SCHEMA.md` §1), then one event per line. Cause-chain integrity at
  write time (P1a): non-null `cause` except run-start events, `cause` must
  reference an existing id, header flushed before the first event. The log
  writer is the only code allowed to produce canon (INV-1 enforcement
  point).
- `core/fold.py` — two paths, one truth (STATE-1, D-023, KI#5):
  `fold(log) → state` is the T2 truth-test; runtime keeps an incremental
  projection `state_new = apply(state_old, event)` updated as events are
  emitted, with SQLite kept in lockstep — the projection checkpoint is
  `MAX(event_seq)` in the index (EventStore persistent-subscription
  collapse: the index *is* the checkpoint). Never fold at startup on the
  hot path.
- `core/pack.py` — loader (PACK-1). `sorted()` over the pack directory
  (INV-2; C:DDA's BFS load order is needed only when inheritance arrives —
  phase 6), per-category files, JSON-Schema validation at load, closed
  enums checked, `"_"` commentary fields ignored, name-based references
  resolved after all files load (load-then-resolve; no forward declarations).
  **Phase-0 minimum lint (~50 lines stdlib, fails loudly at load, before any
  simulation):** orphan-reference check — a behavior rule referencing a
  trigger, an effect referencing an item, a template referencing an event
  type: the target must exist (closed per pack); closed-enum check on every
  enumerated field. Full UAP/live-char AP lint is phase 6, never earlier.
- `core/loop.py` + playscript runner — the tick driver (KeeperRL
  `Model::update` shape): pop the next entry; while the entry's tick passes
  integer boundaries, run the per-tick system passes first (fixed order,
  each a band-0 queue entry or an explicit ordered list), then execute the
  popped entry: checks, RngBank draws, event emission, completions/hooks
  enqueued at their trigger ticks. Playscript = seed + ordered intents
  (`MVP_SCOPE.md` §13 owns the format).

**Donor stack.**

| Donor | Contributes | Evidence |
|---|---|---|
| rot.js | `EventQueue` min-heap primitive | `docs/ref/rot_js.md` |
| KeeperRL | continuous-time queue; players-first; `Model::tick` fixed subsystem order; wave precompute → hooks | `docs/ref/keeperrl.md` |
| DCSS | N-stream RNG; `ASSERT_stable`; `peek`; `div_rand_round` stochastic rounding | `docs/ref/dcss.md` |
| Brogue | two-stream discipline; no-wall-clock recording header; audit counter; multi-pass tick | `docs/ref/brogue.md` |
| Mesa | Model/Scheduler/Agent vocabulary; single-RNG; amnesia anti-pattern named | `docs/ref/mesa.md` |
| EventStore | `$all` global stream; OCC constants; checkpoint-as-index | `docs/ref/eventstore.md` |
| entt | id+version packing; sparse+packed projection layout (STATE-1) | `docs/ref/entt.md` |
| Bevy | double-buffer → tick boundary; build-time ambiguity check | `docs/ref/bevy.md` |
| Azgaar | four-layer split: data / generators / editors(`cli`) / renderer | `docs/ref/azgaar_fmg.md` |
| C:DDA | per-category file split; load discipline | `docs/ref/cdda_data_json.md` |

**Watch-outs (named negatives).** No wall-clock anywhere, including
diagnostics (D-004; Brogue's `time(NULL)` seed fallback is the one looseness
we do not port — seed 0 means seed 0). No unsorted iteration over dicts or
files (`PYTHONHASHSEED=0` + `sorted()`; ai-town's insertion-order iteration
is the named hazard). No `fold(log)` on the runtime path (KI#5). No floats
in the canon path — ticks, counters, seeds are integers (Azgaar's
float-drift across engines is the named cause).

## 2. iter-2 · actions (the 12, checks, outcomes, price)

**Combined design.**

- **Intent → Event boundary** (ai-town discriminated union + EventStore
  OCC): an Intent is a *proposal* — `type`, `target`, `method`, risk
  fields per `SPECS_BACKLOG.md` INTENT_SCHEMA sketch. The front-door
  validates preconditions against the projection; only then does the
  resolver emit the event. Rejected intents are recorded as no-op events
  with a cause chain (the world noticed the attempt — or did not, per
  perception), never silently dropped.
  **Intent OCC (`based_on_event_seq`):** every Intent carries the
  projection's `event_seq` it was proposed against; on apply, if
  `MAX(event_seq) > based_on_event_seq` **and** the precondition is broken
  in the new projection — reject with a cause chain to the event that broke
  it; a no-op event is recorded either way. The same OCC semantics the
  phase-1 validator uses — one mechanism, two scales.
  **Intent lifecycle (Endless Sky 7-state reduced):**
  `PROPOSED → ACCEPTED (SCHEDULED completion entry enqueued) | REJECTED
  (no-op event with cause)`; "accepted but pending" = the SCHEDULED
  completion entry in the queue; a precondition broken before the
  completion tick → a SEEDED fail-trigger emits `mission_failed` with a
  cause chain to the original accept event. The full offer/accept/decline/
  complete/fail/defer/visit state machine is a phase-3 refinement (P3c).
- **Scheduler DAG (SCHED-1, lands iter-2):** the annotation language —
  every system dataclass declares `reads: tuple[str, ...]` and
  `writes: tuple[str, ...]` as data loaded from JSON packs (entt
  discipline — Python has no const, so the access spec is content, not
  signature); optional `before: tuple[str, ...]` / `after: tuple[str, ...]`
  hints (the Bevy `.before()`/`.after()` analogue) for explicit ordering.
  `core/scheduler.py::build()` topologically sorts on read/write
  intersection; two systems both writing the same component without an
  explicit `before`/`after` between them → `ScheduleAmbiguityError` naming
  the offending pair — a unit test with a deliberately conflicting pair
  fails at build time, before any test run. "Fails loudly" = an exception
  at DAG build, never a runtime race.
- **Preconditions as data** (Wesnoth `[filter]` family → JSON): a
  per-noun structured filter map (`Dict[str, list]`), never a string
  expression language (L10 — the Wesnoth `filter_condition`
  Lisp-in-disguise and Paradox scope-spaghetti are the named
  anti-patterns). Endless Sky's infix condition language is the minimal
  donor; we take the *fields*, not the syntax.
- **The 12 actions** (`MVP_SCOPE.md` §7 owns the table): each is pack data
  — checks with modifier tables, duration → SCHEDULED completion entry,
  outcome payloads. Checks draw from the substantive stream only.
- **Price markers** (EPIST-1, live-char): every socially meaningful
  outcome payload carries same-scene observable markers — the knowledge
  records and perceivable state tokens witnesses can perceive — alongside
  `state_changes` and `hooks` (L8 pairing). "Tried to steal — failed, the
  world did not change" is dead by L1; the fix is the partial-sighting
  records the walkthrough already specifies. **Precursor contract:** at
  iter-2 a Price marker is the tuple `(perceivee_id, marker_type,
  fidelity_hint, cause_event_id)` — a partial-sighting precursor; iter-3
  generalizes it into the full `KnowledgeRecord` schema (channels ×
  fidelity). The migration is an additive schema_version bump plus a
  `_correction` event family rewriting partial-sighting records as full
  knowledge records (INV-5: append, never edit).
- **Effect family = one transition primitive + flag-gated triggers**
  (Brogue `promoteTile`): fire exposure, flammability flags, stochastic
  promotion ticks — all one mechanism with per-layer trigger sources, in
  `rules.json`. Fire-vs-extinguisher priority comparison (Brogue
  `exposeTileToFire`) is the whole fire-vs-water model — no physics layer.
- **Relations gate availability** (Prom Week): an action's precondition
  may reference relation axes — "talk" needs a minimal trust floor —
  wiring system 3 into the action layer before iter-3 formalizes the map.
- **INV-3 stoplist test** lands here: grep for domain words in `core/` +
  `sim/` fails CI.

**Donor stack.** Prom Week (social physics — synthesis-only: academic
  paper + GDC talk, no code repo; no deep dive planned, per
  `CORE_DESIGN_RESEARCH.md` §2) · live-char (Trigger→Action→Price;
  observability law L1) · Brogue
  (`promoteTile`, extinguishing priority, stochastic promotion) · C:DDA (flat
  effect vocabulary; itemgroup `collection`/`distribution` for placement) ·
  Paradox (`weight_multiplier = base + modifier{add|factor|trigger}` for
  context-sensitive option weighting — as JSON, not script) · Endless Sky
  (mission lifecycle `to: offer/accept/complete/fail/defer` → intent
  `accept_if/complete_if/fail_if`) · ink (`+` persistent vs `*` single-shot
  → `accept_policy`) · ai-town (Intent discriminated union).

**Watch-outs.** No mid-action cancellation in v0 — a cancelled action is a
new event (`MVP_SCOPE.md` §8). No free-text parsing (phase-2 gate). Every
dice roll keyed through the RngBank (L5) — a bare `random.` import in
`sim/` is a stoplist-class bug.

## 3. iter-3 · knowledge, relations, expectations

**Combined design.**

- **Knowledge records** (`EVENT_SCHEMA.md` §3 owns fields): channels
  `saw/heard/told/inferred` × fidelity `exact/partial/vague`. The record
  shape is Generative Agents' memory stream one-to-one (append-only,
  per-knower rows) — with the channel axis they lacked. Rumor = transfer
  event with one-step fidelity decay (D-007); lies = crafted records
  (D-008). Blind-NPC (T3): no record → cannot know, cannot say.
- **Expectations** (P2d, closes KI#3): `rules.json` behaviour rules
  generate per-NPC expected observations from schedule + position ("guard
  expects `purse_01` on the bar at watch start"); perception compares
  expected vs observed; mismatch emits an ordinary `inferred`-channel
  record cause-chained to the originating event
  (`purse_missing_from_bar` → `ev_0007`). The only legal route to
  suspicion-from-absence — an absence is knowable only as a violated
  expectation, never as "not seen".
- **Relations** (P2a, D-020): sparse pair-keyed map, canonical key the
  sorted id tuple (Neighborly `RelationshipTracker`; C:DDA
  `factions.json` relations; CK3 axes — three independent validations).
  Relation values are **derived state** (L3): `relation_changed` events
  fold into the projection; delta tables per interaction type are pack
  data. Teller↔listener trust already weighs rumor acceptance in the
  drafted `rules.json` — now it has a data home.
- **Influence Boundary online** (EPIST-1): NPC behavior functions read
  own state + own knowledge only; the guard reacts to
  `heard: slurred_speech`, never to the drunkard's intoxication field.
  Embodiment is pack data: which status flags surface as which perceivable
  markers at which fidelity. This closes system 5 into the
  perception→knowledge chain and makes "who can be wrong" computable per
  observer. *(Adopted by this blueprint as the default design; the owner
  may veto at the iter-3 design gate — it was flagged owner-call in
  STATUS iter-0t.)*
- **Ambient crowd** (`npc_market_crowd_01`): passive knowledge-holder —
  the seed of the LOD ladder (LOD-1), not a simulated individual.
- **Detail callbacks** (P2c, owner-pending): talk topic selection = most
  salient known fact of the teller — knowledge *used*, not just stored.

**Donor stack.** The Sims (gossip propagation — synthesis-only:
proprietary, patterns-from-papers per D-015; no deep dive possible, per
`CORE_DESIGN_RESEARCH.md` §2) · Prom
Week (relations gate actions — synthesis-only, as above) · Neighborly
(pair-keyed map shape) · C:DDA (pair-keyed faction booleans) · CK3/Paradox
(relation axes; secrets arrive phase 3+) · DF Legends (`hf_reputation_change`
→ reputation-as-event; epistemology schema) · Generative Agents (memory
stream; retrieval shape reserved for phase 4) · live-char (Influence
Boundary; embodiment) · Wesnoth (`sighted` — perception as first-class
event source) · Mesa (amnesia anti-pattern the log fixes).

**Watch-outs.** `known_by` is derived, never stored (L3). No group
reputation (D-006) — spread between guards is transfer events at watch
change. Fidelity decays one step per transfer, never more — distortion
from source incompleteness, not a rumor system.

## 4. iter-4 · director + goal ticker

**Combined design.**

- **Consequence buffer** (D-005, the law): hooks + triggers (time / place /
  threshold) are seeded **at event time** into the buffer. The director
  only ever *releases already-seeded material* — a complication out of
  nowhere is a bug (RimWorld Randy is the named anti-pattern). KeeperRL's
  `ExternalEnemies` is the clean precedent: schedules precomputed, a small
  dispatcher releases them.
- **Narrative entropy** (P2e, `SPECS_BACKLOG.md` DIRECTOR_SPEC sketch owns
  the formula): sum of seeded-hook weights + global suspicion + visible
  physical threats — computed from **observable state only** (L6). The
  stagnation detector releases the lowest-threshold seeded hook when
  entropy drops below threshold — a tension floor sensor, not a boredom
  timer. Replaces the flat `release_after_ticks_without_visible_event`
  timer in the drafted `rules.json`.
- **Pacing clock** (DIR-1): states RAMP / PEAK / REST / STAGNATION with
  minimum durations — two cooldown clocks (`TimeSincePeak`,
  `TimeSinceRest`, L4D) rather than one timer; release budget = 1 hook per
  beat (L4D spawn-budget logic, budget 1); encounter windows with a
  `MinGapBetweenEncounters` floor (Alien). Layered thresholds (L4D2
  three-intensity rule) and a `PEAK_CLIMAX` state for high-severity hooks
  are phase-3 refinements, recorded not built.
- **Multi-channel policies** (L4D family): a `DirectorPolicy` interface —
  `should_release(hook, observable_state) → bool` and escalation factors
  — with channels (threat / social / ambient) as pack-configured
  instances, not one god function. RimWorld's storytellers are three
  policies over the same content; our director-on/off switch (T8) is the
  minimal policy pair.
- **Objective broadcast** (Alien): releasing a hook enqueues an **Intent**
  for an NPC through the normal queue — the director never moves actors,
  changes state, or bypasses the Intent→Event front-door. Director-off =
  the buffer still exists (hooks seed), nothing releases; A/B measures the
  delta (T8).
  **Rejection policy:** a rejected director Intent consumes the release
  budget (1 per beat — the director never spams); after a rejection the
  target NPC gets a per-NPC cooldown of N beats (pack data — the
  `MinGapBetweenEncounters` analogue applied to targeting); the entropy
  sensor stops targeting dead actors (observable projection). STAGNATION
  stays a purely entropy-driven state — targeting failures never fake it.
  **Per-run scope:** director adaptation state is per-run — INV-1
  (`state = fold(log)`, the log is per-run) forbids cross-run persistence
  of director observations; the seeded-hook buffer reseeds from the master
  seed every run. Director *policies* (RAMP/PEAK/REST/STAGNATION parameters,
  weight tables, cooldowns) are pack data — constant across runs with the
  same pack. "Director learns the player" (Alien) stays the named
  anti-pattern (L6).
- **Goal/urge ticker** (P2b, D-021): NPC goals → occasional autonomous
  actions (the drunkard seeks ale, the maid roams, the guard patrols)
  through the same queue and tick discipline — M5 non-PC share becomes
  non-trivially non-zero by construction. Small-formula dynamics
  (KeeperRL rebellion): goal-driven behavior is a few numeric formulas
  over knowledge and state, not a planner. Full LLM planning — never
  (`VISION.md` §6; Generative Agents is the cost anti-precedent).

**Donor stack.** RimWorld (named anti-pattern; `IncidentDef` field shape:
weight + category + cooldown as hook data; tale layer) · L4D (intensity
ratchet; peak/rest clock; budget; two clocks; multi-channel) · Alien
(two-AI split; pressure cap-and-floor transitions; objective broadcast;
encounter windows; named negative: player-learning) · KeeperRL (wave
precompute; per-tick roll `SAMPLED` timing; small-formula social dynamics)
· Paradox (`immediate`/`option`/`after` three-phase lifecycle → seed /
choose / apply) · Endless Sky (`event` block = player-independent
background events) · Generative Agents (re-plan-on-violation for hook
chains, engine-free).

**Watch-outs.** Entropy reads observables only — never knowledge records,
never PC internals (L6). The director is causality-preserving by
construction; if T8 shows all emergent chains are director injections, the
core is dead — that is the test working, not a bug to paper over.

## 5. iter-5 · chronicle & CLI

**Combined design.**

- **Event vs tale split** (RimWorld `TaleDef`): the chronicle line is a
  derived prose-ready record — created when the event fires, attached to
  the participating entities, pruned per cause-chain window (the
  `maxThreads` analogue applied to causal chains, not type buckets — a
  deliberate departure from RimWorld's per-taleType buckets, recorded as
  such; a pack rule `prune_window: Dict[event_type, int]` may return for
  multi-scenario chronicles in phase 5+, an option recorded here, not
  built). Canon stays in the JSONL; the tale is a fold (L3).
- **`render/` = deterministic tracery** (CHRON-1): `templates.json` as the
  JSON symbol table (symbol → alternatives, nested `#symbol#` expansion,
  dot-notation hierarchies, modifiers `.a`/`.capitalize`/…, save/restore
  stack for pronoun/article agreement). Every pick comes from the
  **cosmetic stream** (RNG-1) or `sorted()` order — the grammar is
  tracery's, the engine is ~200 lines of stdlib, and T1 covers the
  chronicle too (byte-identical). ink's conditional text
  (`{condition: text|else}`) rides the same engine; ink's `shuffle`
  semantics (random pick **without immediate repeat**) is preserved via a
  per-symbol `ShufflePool` state machine — candidates =
  `sorted(alternatives)` minus `last_pick`; if more than one candidate
  remains, tie-break by a seeded draw from the cosmetic stream; a single
  remaining candidate is taken as-is; `last_pick` advances after every
  expansion. ~20 lines of stdlib: ink's no-immediate-repeat semantics and
  tracery's determinism both hold; the pool state lives in the render pass
  and never touches canon. Endless Sky `phrase` (one symbol → list) is the
  minimal rung for name variety.
- **Importance gates surfacing** (`MVP_SCOPE.md` §9 owns the rule): the
  pack rule (entities touched + irreversibility + far hooks → low/medium/
  high) decides which events get tale lines at all; day headers group
  them. The chronicle stays dry — readability test T7 runs on exactly
  this output, ornaments would invalidate it.
- **Per-entity history views** — the free win (DF artifact anchors):
  `fold(log)` filtered by entity = full history of `purse_01` or Doren.
  `state <entity>` CLI command exposes it from day one; the phase-1
  briefer inherits the same query.
- **CLI** (`MVP_SCOPE.md` §12 owns the command list): `cli/` is the
  "editor" layer of the four-layer split (Azgaar); it is also the script
  escape valve (Wesnoth Lua precedent) — Python orchestration *on top of*
  the JSONL log, never in the canon path. `replay <log>` exercises T2;
  `directors on|off` exercises T8; no `print()` outside `cli/`.

**Donor stack.** tracery (grammar; stack; 200-line scale) · ink (knot/
stitch addressing reserved for the phase-1 brief graph; conditional text;
`+`/`*` persistence already consumed at iter-2) · Endless Sky (`phrase`) ·
RimWorld (tale vs event; pruning window) · DF Legends (chronicle LOD;
per-entity views) · Wesnoth (escape-valve precedent) · Azgaar (renderer
never mutates world data).

**Watch-outs.** The renderer writes nothing to the log — a render pass
that emits canon events is an INV-1 violation. Cosmetic stream only
(RNG-1): a substantive draw inside `render/` desyncs nothing today and
everything the day a render cache is added.

## 6. iter-6 · gate (tests, metrics, verdict)

**Combined design — the verification stack (TEST-1).**

| Test | Donor technique folded in |
|---|---|
| T0 schema | every log line validates; the doc example is the fixture (D-010) |
| T1 determinism | two runs byte-identical **+ RngBank fingerprint equality** (Brogue audit counter) **+ known-good seed catalogs** diffed against committed outputs (Brogue `test/seed_catalogs/`). **Fixture-regeneration guard (runs inside pytest, no CI change):** T1 executes twice — (1) byte-identity against committed fixtures; (2) a fresh regeneration into a tmp dir diffed against the committed fixtures; a divergence with unchanged `schema_version` = fail. A schema change makes "regenerate fixtures" a mandatory iteration step + a migration note in `EVENT_SCHEMA.md` |
| T2 replay | `fold(log) == state`; SQLite dropped and rebuilt, equality again (EventStore projection equivalence; `rebuild` as the INV-1 mechanism) |
| T3 blind-NPC | zero knowledge leaks on the suite; UAP motivation-hole crosswalk designs the cases |
| T4 irreversibility | `irreversible` state changes never revert without counter-events (fire has none) |
| T5 impossible | teleport / sourceless arson / absent items / knowing the unseen — plus `ASSERT_stable` guards proving perception checks draw no stray RNG |
| T6 smoke | 1000 ticks, no exceptions |
| T7 readability | human retells the chronicle (manual gate — the only human judgment in the stack) |
| T8 director-off | A/B on identical seed + playscript, **single-factor** (live-char one-change rule); ≥3 emergent chains without the director |

- **Metrics M1–M5** (`MVP_SCOPE.md` §15 owns definitions): computed by
  folding the log, never collected by feel (Mesa `DataCollector` is the
  shape, inverted). Thresholds set from the measured baseline at the gate
  review (D-019) — directionality first, numbers from data.
- **Causal-density checklist** per event (L1): what changed · who learned
  what at what fidelity · who can be wrong · who can lie · what became
  irreversible · what future conflict was seeded · usable 10–50 turns
  later · **what did witnesses perceive of the price paid** (the live-char
  addition).
- **balance-1 harness** (KI#4): 1000 headless sims, seed-varied sampled
  intents → distribution plots of `suspicion` / `fire_spread` over ticks —
  validates that `rules.json` thresholds are tuned, not guessed. Uses T1
  determinism; no new infra.
- **Gate protocol** per `ROADMAP.md` §5; verdict in `worklog.md` +
  `STATUS.md`; kill-criteria hit stops feature work until the ontology is
  fixed — honestly reported, never averaged away.

**Watch-outs.** No LLM anywhere near the gate (INV-4 — the phase-0 gate
must pass first). A boring four-room scenario is not a verdict on the
core (`MVP_SCOPE.md` §1) — expressiveness and combinatorial depth are.

---

← Up: [`docs/BLUEPRINT.md`](../BLUEPRINT.md) · next part:
[`docs/blueprint/phases.md`](phases.md).
