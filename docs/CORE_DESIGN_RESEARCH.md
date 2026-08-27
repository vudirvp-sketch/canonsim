# CORE_DESIGN_RESEARCH.md — Depth-First Core: Reference Synthesis

> Research notes (owner-requested, iter-0e), NOT a spec. Per
> `docs/SPECS_BACKLOG.md`, specs are born from experiments; this file distills
> external references (`docs/REFERENCES.md` catalog + widely documented design
> patterns) into design guidance for the core, written before iter-1 code.
> **Status: absorbed (D-029, iter-0w; P2c accepted via D-033, iter-1)** — every
> P1/P2 item is enacted into `docs/DECISIONS.md` / `docs/TASKS.md` / the blueprint (P1a → phase0 §1;
> P1b–d → D-019; P1e → D-023/KI#5; P2a → D-020; P2b → D-021; P2d → KI#3;
> P2e → DIRECTOR_SPEC sketch); no owner-pending
> candidates remain; §3's synthesis table is superseded by the
> blueprint ledger (`docs/BLUEPRINT.md` §1) — retained as research record.
> Retired at the phase-0 gate review (`doc-1`) alongside the VISION freeze.
> Nothing here changes phase-0 law (`docs/MVP_SCOPE.md` §2). Cap 600 lines
> (D-025).

## 0. The goal function (owner's intent, formalized)

The owner's requirement in one sentence: **deep, connected stories where
details matter — not "much content, puddle-deep" — with diversity as the
second-order concern.** Formalized as testable properties:

| Property | Testable form |
|---|---|
| Depth | an early detail changes a late outcome (Chekhov's gun fires) |
| Connectivity | events link via `cause`, relations and knowledge — not sequence |
| Details matter | removing one early event changes the ending |
| Diversity | same ontology, different seeds/packs → different stories |
| Foundation | the ontology generalizes (core admission test, `VISION.md` §5) |

The design risk this file guards against: **volume without connectivity**.
Breadth is O(authored content); depth is O(intersections between primitives).
Adding depth means adding intersections, not adding content.

## 1. Method

1. Take the sources cataloged in `docs/REFERENCES.md` (§1–§10) plus widely
   documented patterns (marked `†`, intake queue in §7).
2. For each source: the depth primitive it proves, and the failure mode it
   is known for.
3. Audit the phase-0 design against those primitives (§4); record gaps (§6).
4. Convert gaps into decision-ready proposals with cost/phase tags (§6).

## 2. Reference synthesis: what each source teaches

| Source (catalog §) | Depth primitive (proven) | Failure mode to neutralize | Lands where |
|---|---|---|---|
| DF Legends (§1, §10) | epistemology schema; artifact anchors; LOD — history ticks on populations + notables | micro-empty (no gossip layer); dry prose; causality *reconstructed*, not recorded | knowledge records (phase 0); `cause` recorded not inferred (`EVENT_SCHEMA.md` §2); ambient crowd entity; bg-2 taxonomy |
| DF worldgen (§10) | abstract history: notables get events, populations get statistics | full-detail-everywhere cost explosion | entity LOD ladder (P3d, phase 5) |
| RimWorld (§10) | content-as-data (Defs); tale extraction from a log | storyteller invents threats from nothing; repetitive tales | D-005 consequence planner; `templates.json`; M4 novelty metric (P1c) |
| Kenshi (§10) | faction sim without plot; world indifferent to the player | no epistemology — nobody *knows* anything | phase 5 factions; our knowledge layer is the fix |
| L4D Director (§10) | tension curve, peaks and rests | player-centric pacing; content-free beats | phase 3 pacing ON TOP of the seeded buffer |
| Alien: Isolation (§10) | dual AI: macro director + micro agents | — | phase 3 director/agent split |
| CK3 / Paradox scripting (§1, §10) | secrets & leverage as first-class facts; relation axes; event grammar (trigger/weight/mtth/effect) | mechanical prose; scripted feel; content bloat | D-006/D-007/D-008 groundwork; phase 3 grammar; phase 4 secrets (P3a) |
| The Sims `†` | social-network gossip propagation | episodic amnesia; no irreversibility | phase 0 rumor transfer (already: `EVENT_SCHEMA.md` §3) |
| Prom Week `†` | social physics: relations gate which actions are *available* | tiny hand-authored action space | the intersection matrix (`MVP_SCOPE.md` §6) is the generalization |
| Wildermyth `†` | character arcs; legacy across campaigns; panel retelling | finite authored content | phase 3 arcs; scene cards (iter-5) |
| King of Dragon Pass `†` | state-gated scenes; reactive advisors | finite authored content | triggers (phase 0); phase 3 scene grammar |
| Stanford Generative Agents (§5) | memory stream / reflection / planning | cost: thousands of USD per 2-day demo; canonless | negative precedent (bg-4 pins the figures) |
| AI Town (§2) | — | runtime LLM agents: cost + drift | negative precedent (`ROADMAP.md` §4) |
| Brogue (§2) | environmental emergence from ~5 rules | no social/epistemic layer | fire/smoke chain (phase 0); "small alphabet, deep composition" |
| C:DDA (§1) | content-as-JSON at scale | — | phase 3 |
| GearHead (§2) | story-fragment random generation | — | arc-fragment precedent (phase 3) |
| ink / tracery (§4) | generative text skins | surface variety without depth | `render/` (iter-5); phase 6 skins |
| Gaffer on Games (§8) | determinism discipline | — | INV-2; `TECH_NOTES.md` §4 |
| Mesa (§2) | Python ABM pattern: Model + Scheduler + Agent — our tick queue is the scheduler, agents are stateful folds | pure ABM is episodic amnesia without an event log (The Sims problem); Mesa's `step()` is state-mutating, not event-emitting | iter-1 tick loop is Mesa-style; the JSONL log + `state_changes` is the amnesia fix |
| Neighborly (§2) | agent-based settlement: emergent narrative from agent goals + interactions; closest existing cousin | weak epistemology — agents act but don't accumulate structured knowledge; no `known_by`, no fidelity | phase 5 settlement cousin; our `knowledge` records are the missing layer |
| Red Blob Games (§8) | deterministic algorithmic foundations: A*, FOV, hex/grid math, polygon maps | pure geometry, no narrative; algorithms without an ontology produce puddles | phase 5 worldgen foundations; phase 0 = none (zero-external-code law) |
| Game Programming Patterns (§8) | pattern vocabulary: Event Queue, Component, Command, State, Observer | patterns without invariants rot; vocabulary alone ships nothing | iter-1 core plumbing uses Event Queue + State; INV-1..INV-5 are the binding constraints that keep patterns honest |
| UAP webapp (§9) | countable-criteria world audit: rubrics with thresholds over evidence; code decides, not the LLM (their §0.6) | LLM-as-judge scoring (X/52 = unseeded opinion); regex-over-markdown handoff; free-form output | external validation of M1-M5 + gate reviews; 7-hole test crosswalk; phase-1 harness prompt shapes; phase-6 pack lint (`docs/ref/uap_audit.md`) |
| Live Character Guide (§9) | character-card methodology: SPINE causal chain of observable units + Trigger→Action→Price anchors where Price = immediate, physical, same-scene observable cost; "every element must produce an observable action" | prompt-compensation machinery (token budgets, PP/format locks, Script Tax); false memory + fatigue emulation as canon breaks; single-character focus — no epistemology, no NPC↔NPC knowledge | pack-data character depth (spine-shaped records, price markers, stress modifier tables) + phase-6 lint vocabulary (AP crosswalk) + phase-1 brief injection grammar (voice isolation, recency hierarchy, lorebook depth/probability/cooldown/sticky/range) (`docs/ref/live_char_guide.md`) |

`†` Not in `REFERENCES.md` yet — §7 intake queue, D-016 procedure at the
quarterly `doc-2` review.

## 3. The composition principle (why the architecture is the blend)

No single reference has epistemology + causality + data-driven content +
pacing + arcs at once. The architecture takes each strength and pairs it
with another source's fix:

| Weakness | Neutralized by |
|---|---|
| DF: micro-empty, dry prose | micro-dense slice (`MVP_SCOPE.md` §3) + LLM narrator later (canon/voice split) |
| RimWorld: threats from nothing | D-005: consequences seeded at event time |
| CK3: mechanical prose | template chronicle now; LLM renderer in phase 1 |
| Wildermyth / KoDP: finite authored content | simulation substrate + packs |
| L4D: content-free pacing | consequences are the only pacing fuel |
| Generative Agents: cost, canonless | the world ticks outside the model (`VISION.md` §1) |
| The Sims: amnesia | event-sourced memory: state = fold(log) |
| Brogue: no social layer | 8 systems × intersection matrix |
| Lorebooks: no time, no causality | ticks + `cause` + knowledge records |
| Mesa: pure ABM = episodic amnesia | event log + `state_changes` = the amnesia fix (The Sims lesson, ported to Python) |
| Neighborly: weak epistemology | our `knowledge` layer (records + `known_by` + fidelity) is the missing epistemic substrate |

The pattern: **depth comes from pairing each generative axis with an
epistemic or causal ledger.** That is exactly what event sourcing gives us —
the log is the ledger.

## 4. Depth equation (mechanical decomposition)

Story depth factors multiplicatively — any factor at zero collapses depth:

| Factor | Mechanical form | Phase-0 home | If missing |
|---|---|---|---|
| Causality | `cause` chain on every event | `EVENT_SCHEMA.md` §2 | "one thing, then another" |
| Consequence | every event narrows the possibility space: `state_changes` + `hooks` | `EVENT_SCHEMA.md` §4–§5 | events without consequences (kill criterion) |
| Memory | knowledge records + relations + world state persist | `MVP_SCOPE.md` §10 | NPC amnesia; details stop mattering |
| Asymmetry | who-knows-what differs per actor | T3 blind-NPC | no dramatic irony, no investigation |
| Irreversibility | `irreversible` state changes | T4 | stakes collapse |
| Salience | importance rule; the chronicle surfaces what matters | `MVP_SCOPE.md` §9, §12 | puddle: volume without focus |
| Diversity | small alphabet × deep composition; seeds/packs recombine | pack data | repetitive runs |

Free win already in the design: **per-entity history views**. fold(log)
filtered by entity = the full history of `purse_01` or of Doren — DF's
artifact anchors without extra machinery. The chronicle and the future
briefer should expose this query from day one.

## 5. Phase-0 audit (already depth-first — links only)

The ontology already encodes most depth-first principles; confirmation map:

- Intersection matrix as a first-class design artifact — `MVP_SCOPE.md` §6.
- Far hooks (10–50 turns) first-class — `EVENT_SCHEMA.md` §5.
- Epistemology as data; fidelity decay; lies as crafted records —
  `MVP_SCOPE.md` §10, `EVENT_SCHEMA.md` §3.
- Director = consequence planner; director-off A/B mandatory —
  `MVP_SCOPE.md` §11, D-005.
- Importance computed, never by feel — `MVP_SCOPE.md` §9.
- Causal-density checklist per event — `MVP_SCOPE.md` §15.
- Metrics from the log, not by feel (M1, M2) — `MVP_SCOPE.md` §15.

**Research conclusion: the phase-0 risk is not the ontology. It is (a)
execution details that silently destroy depth (§6 P1), and (b) three small
gaps (§6 P2).**

## 6. Gaps and proposals

### P1 — zero/low-cost, iter-1-compatible (recommend: adopt now)

- **P1a Cause-chain integrity in the writer.** Gap-free ids (already law),
  non-null `cause` except run-start events, one RNG stream, header written
  before the first event. The log is the depth-measurement instrument; dirty
  chains poison every later metric and every "why did this happen" query.
- **P1b M3 — causal chain length.** Mean/median depth of the `cause` chain
  per event, computable from the log alone. (absorbed → D-019, iter-0g;
  added to `MVP_SCOPE.md` §15 at the iter-6 gate: baseline first,
  thresholds from measurement, same protocol as M1/M2.)
- **P1c M4 — novelty/repetition.** Rate of repeated (type, actor) bigrams;
  share of distinct `knows` tokens. RimWorld's repetitive-tale problem,
  measured instead of felt. (absorbed → D-019, iter-0g.)
- **P1d M5 — non-PC event share.** Events with actor ≠ player / all events.
  Makes "world not player-centered" (Kenshi/RimWorld lesson) measurable at
  the director-off gate (T8). (absorbed → D-019, iter-0g.)
- **P1e Runtime state vs test fold.** The `fold(log) = state` rule (INV-1,
  `EVENT_SCHEMA.md` §1) is the **truth-test** (T2) and the SQLite rebuild
  path. Runtime must use an **incremental projection** —
  `state_new = state_old.apply(event)` per event as it is emitted, with the
  SQLite index kept in lockstep. Using `fold(log)` on the runtime hot path
  is O(N) per query and O(N²) on a running system; the ambiguity is silent
  and bites only at scale. Recorded as D-023, KI#5; clarify in
  `EVENT_SCHEMA.md` §1 next time it is touched. No new proposal — a
  clarification of an existing invariant, not a feature.

### P2 — phase-0/1 candidates (small, real additions — owner decision)

- **P2a NPC↔NPC relations.** Today relations exist only (npc → pc)
  (`MVP_SCOPE.md` §4.2), yet rumor acceptance already weighs trust
  (`content/tavern_pack/rules.json`) — teller↔listener trust has no data
  home. Sparse pair-keyed relation map; no event-schema break (relations are
  state, not event fields). Payoff: guard coordination, non-PC story lines,
  richer rumor dynamics. (absorbed → D-020, iter-0g; folded into iter-3.)
- **P2b Minimal goal/urge ticker.** `goal` is inert data today; the world
  only reacts to the PC. Minimal version: goal → occasional autonomous
  action (drunkard seeks ale, maid roams, guard patrols) through the same
  queue, same tick discipline. (absorbed → D-021, iter-0g; minimal in
  iter-3/4 so the gate can measure aliveness; full LLM planning — never,
  not a Generative Agents clone, `VISION.md` §6 held.)
- **P2c Detail callbacks in talk.** "Old events surface later" is a victory
  condition (`MVP_SCOPE.md` §1): talk topic selection = most salient known
  fact of the teller. Cheap; makes knowledge *used*, not just stored.
  (absorbed → D-033, iter-1; slated for iter-3.)
- **P2d expectation_violation.** NPC reacts only to records *present* in
  `knowledge` today — they cannot notice that the purse is gone, or that
  the expected guard is missing. Yet investigation mechanics
  (suspicion-from-absence) require exactly that. The elegant fix uses
  **no new schema field**: a behaviour rule in `rules.json` generates
  per-NPC expectations from schedule + position (e.g., "guard expects
  `purse_01` on the bar at watch start"); the perception system compares
  expected vs observed; on mismatch, it emits an ordinary knowledge
  record with `channel: "inferred"` and a `knows` token like
  `purse_missing_from_bar`, cause-chained to the theft event. Expectations
  are behaviour functions, not state; the record uses the existing
  `inferred` channel. This is the only legitimate trigger for
  suspicion-from-absence — a guard cannot arrest on "purse not seen", but
  can on `inferred: purse_missing_from_bar` cause-chained to `ev_0007`.
  Slated for iter-3 (KI#3); no schema bump.
- **P2e Narrative entropy for the stagnation detector.** The current
  `release_after_ticks_without_visible_event: 90` (`rules.json` director)
  is a flat timer. A more honest trigger: release the lowest-threshold
  seeded hook when **narrative entropy** drops below a threshold, where
  entropy = sum(weights of seeded hooks) + global suspicion + visible
  physical threats. Crucially, entropy is computed only from **seeded
  hooks + visible state** — never invents new threats (D-005 preserved).
  This refines the stagnation_detector from "boredom timer" to "tension
  floor sensor". Lands in `DIRECTOR_SPEC` (iter-4); replaces the flat
  timer, does not add a new system.

### P3 — later-phase records (no action now)

- **P3a** Secrets/leverage as access-controlled fact clusters (phase 4;
  D-008 lies groundwork). CK3 lesson: a secret is depth gunpowder —
  asymmetry with stakes attached.
- **P3b** Faction goals + macro LOD ladder (phase 5; DF/Azgaar).
- **P3c** Arcs & tension shaping (phase 3; L4D/Alien — pacing layered over
  the seeded buffer, never replacing it).
- **P3d** Entity LOD ladder: ambient → statistical → full simulation (the
  crowd entity is the seed of this ladder).
- **P3e** psychological_echo. NPC behavior carries the emotional residue of
  past events: a guard who saw a fire is jittery next morning; a maid who
  witnessed a theft watches the suspect's hands. Implemented as a per-NPC
  `echo_state` derived from `knowledge.records` + `state_changes` + ticks
  since learned, fed as an input to behavior selection — not new data, a
  behavior modifier computed from the existing log. Phase 3+; depends on
  the goal/urge ticker (P2b) to act on the echo, and on per-entity history
  views (§4 free win) for the source signal. Prevents "events that
  happened but no longer matter" — the depth-equation Memory factor made
  observable in NPC behavior, not just in the chronicle.
- **P3f** Trait crystallization. Three or more related `knowledge.records`
  collapse into a discrete belief token (e.g., `paranoid_about_thieves`
  after a guard witnesses 3+ theft-related events). Traits are **derived
  state** — a fold over a subset of the log — never stored as primary
  data (INV-1 preserved); on demand they expand back to their source
  records for the brief. Lands in `LEGEND_SPEC` (phase 4); prevents
  long-running NPCs from accumulating unbounded records in working memory
  while keeping the log the only truth. Differs from P3e: P3e is a
  per-NPC valence (continuous, behavior-modifying), P3f is a discrete
  semantic belief (token-level, brief-substituting). Together they close
  the Memory factor of the depth equation at phase 3+ — P3e makes
  memory *felt*, P3f makes memory *compressible*.

## 7. Reference intake candidates (owner queue for `doc-2`)

`†` Prom Week (social physics) · `†` Wildermyth (arcs/legacy) · `†` King of
Dragon Pass / Six Ages (state-gated scenes) · `†` The Sims (gossip) · `†`
academic lineage: TALE-SPIN (Meehan 1977), UNIVERSE (Lebowitz 1984), Façade
(Mateas & Stern) — character-centric emergent narrative planning. Procedure:
D-016 (exact-name verification; proprietary sources stay pattern-only).
None enters the catalog before verification.

## 8. Owner decisions (iter-0g, 2026-08-26)

- **Q1 → yes (D-019).** M3/M4/M5 flip from proposals to accepted iter-6
  metric baseline. P1b–P1d enacted.
- **Q2 → yes (D-020).** NPC↔NPC relations flip from proposal to accepted
  iter-3 scope. P2a enacted.
- **Q3 → yes (D-021).** Minimal goal/urge ticker flips from proposal to
  accepted iter-3/4 scope. P2b enacted (minimal in phase 0; full LLM
  planning — never, `VISION.md` §6 held).
- **Q4 → no, one more research pass (D-022).** This iteration is that
  pass. iter-1 is the next functional step. Doc-loop alarm fires (sixth
  docs iteration in a row); owner-requested exception applies.

New proposals from the iter-0g audit (no owner decision yet): P1e (KI#5
runtime-vs-fold clarification), P2d (KI#3 expectation_violation, slated
for iter-3), P2e (entropy refinement for iter-4 director), P3f (trait
crystallization for phase 4 LEGEND_SPEC). P2c is accepted for iter-3
(D-033).

Open questions blocking iter-1: none.
