# CORE_DESIGN_RESEARCH.md — Depth-First Core: Reference Synthesis

> Research notes (owner-requested, iter-0e), NOT a spec. Per
> `docs/SPECS_BACKLOG.md`, specs are born from experiments; this file distills
> external references (`docs/REFERENCES.md` catalog + widely documented design
> patterns) into design guidance for the core, written before iter-1 code.
> Lifecycle: when the owner accepts a proposal, it moves to `docs/TASKS.md` /
> `docs/DECISIONS.md` and its line here flips to `absorbed → D-0XX`. Nothing
> here changes phase-0 law (`docs/MVP_SCOPE.md` §2). Cap 400 lines; review at
> the phase-0 gate alongside `doc-1`.

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
  per event, computable from the log alone. Propose adding to
  `MVP_SCOPE.md` §15 at the iter-6 gate: baseline first, thresholds from
  measurement (same protocol as M1/M2).
- **P1c M4 — novelty/repetition.** Rate of repeated (type, actor) bigrams;
  share of distinct `knows` tokens. RimWorld's repetitive-tale problem,
  measured instead of felt.
- **P1d M5 — non-PC event share.** Events with actor ≠ player / all events.
  Makes "world not player-centered" (Kenshi/RimWorld lesson) measurable at
  the director-off gate (T8).

### P2 — phase-0/1 candidates (small, real additions — owner decision)

- **P2a NPC↔NPC relations.** Today relations exist only (npc → pc)
  (`MVP_SCOPE.md` §4.2), yet rumor acceptance already weighs trust
  (`content/tavern_pack/rules.json`) — teller↔listener trust has no data
  home. Sparse pair-keyed relation map; no event-schema break (relations are
  state, not event fields). Payoff: guard coordination, non-PC story lines,
  richer rumor dynamics. Recommend: fold into iter-3.
- **P2b Minimal goal/urge ticker.** `goal` is inert data today; the world
  only reacts to the PC. Minimal version: goal → occasional autonomous
  action (drunkard seeks ale, maid roams, guard patrols) through the same
  queue, same tick discipline. Recommend: minimal in phase 0 (iter-3/4) so
  the gate can measure aliveness; full LLM planning — never (not a
  Generative Agents clone; `VISION.md` §6).
- **P2c Detail callbacks in talk.** "Old events surface later" is a victory
  condition (`MVP_SCOPE.md` §1): talk topic selection = most salient known
  fact of the teller. Cheap; makes knowledge *used*, not just stored.
  Candidate for iter-3.

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

## 7. Reference intake candidates (owner queue for `doc-2`)

`†` Prom Week (social physics) · `†` Wildermyth (arcs/legacy) · `†` King of
Dragon Pass / Six Ages (state-gated scenes) · `†` The Sims (gossip) · `†`
academic lineage: TALE-SPIN (Meehan 1977), UNIVERSE (Lebowitz 1984), Façade
(Mateas & Stern) — character-centric emergent narrative planning. Procedure:
D-016 (exact-name verification; proprietary sources stay pattern-only).
None enters the catalog before verification.

## 8. Open questions for the owner

- **Q1** Adopt M3/M4/M5 (P1b–P1d) into the iter-6 metric set? (recommend: yes)
- **Q2** NPC↔NPC relations in iter-3 (P2a)? (recommend: yes)
- **Q3** Minimal goal/urge ticker in phase 0 (P2b)? (recommend: minimal yes)
- **Q4** Proceed to iter-1 now, or one more research pass first?
