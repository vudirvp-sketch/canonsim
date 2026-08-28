# DF designed experience · `REFERENCES.md` §10 · proprietary (design patterns only) · phases 1–5 cross-cutting (salience/director/LOD) + bg-1..bg-4 context

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015). Anecdotes are community canon (player reports,
> succession LPs) — cited as design evidence, not verified history.

**What it is.** The third DF entry, and the only one about the game as
a *designed experience*: not the export schema (`df_legends_xml.md`),
not the worldgen layer (`df_worldgen.md`), but why the game has
captivated players for two decades, where it breaks for them, and what
each successor traded away to "fix" it. Born from the owner's research
question (2026-08-28, the D-022 fresh-request exception): survey DF's
internal flaws — narrative, depth, coherence; explicitly NOT
UI/graphics — and design better instead of copying blindly. Context:
in development since 2002 (public since 2006), principally Tarn Adams
with brother Zach; the 2022 Steam release replaced the interface, not
the simulation.

**Concrete mechanics.**

### The enchantment pillars (what we multiply)

- **P1 Radical specificity.** Tissue/organ/nerve modeling per
  creature; preferences, dreams, moods, grudges per dwarf. A dwarf
  loses a leg, survives, and grieves that he can no longer dance.
  Specificity is why retold DF stories never read as generic — the
  detail is load-bearing.
- **P2 History before the player.** The world arrives pre-aged
  (`df_worldgen.md`): geography, civilizations, gods, heroes the
  player never witnessed but can excavate. Memory the player did not
  pay for.
- **P3 Emergence from collision.** No authored plots; stories are
  collisions of independent systems (cats × spilled ale × grooming;
  a butterfly × a mechanism × an elephant siege — the Boatmurdered
  retelling). Players retroactively reconstruct causality —
  `VISION.md` §3 ("he lost his leg *because* we skimped on medics")
  is the DF experience stated as doctrine.
- **P4 The world as a canonical record.** Legends mode IS an event
  log with an export format — the direct ancestor of our JSONL canon
  (schema borrow: `df_legends_xml.md`).
- **P5 Simulation honesty.** No dramaturgic fudging; the engine never
  softens an outcome for the story's sake. "Losing is fun" is an
  irreversibility-as-content posture, not marketing.
- **P6 Prose outsourced to the audience.** ASCII pushes all rendering
  into the player's head; the "graphics engine" is the community's
  retelling. Proof that a symbolic interface suffices *if the facts
  are specific* — we replace the delivery channel, not the facts
  (`VISION.md` §1).

### The flaw taxonomy (root causes, not symptoms)

Each flaw names the missing layer; the "naive fix" names the pillar it
would amputate. The owner's constraint holds: UI/graphics out of scope.

- **F1 No salience layer — "death by a thousand cats."** Cascades from
  dozens of intersecting mechanics surface as undifferentiated spam:
  the player learns the cats died, never *why* in one legible telling.
  Root cause: no model of what matters to the reader — every event
  delivers at the same priority; relevance is computed in the player's
  head, if at all. The cat cascade is *good content*; the failure is
  delivery. Naive fix (curb the simulation, patch out interactions)
  amputates P3/P5. Fix shape: a salience layer above an honest sim —
  importance gate + assembled vignettes.
- **F2 No pacing layer — "the roulette."** A megabeast arrives by dice
  and ends the fortress with no setup, no foreshadowing, no third act.
  Stories need arcs; honest variance provides neither. Naive fixes:
  scripted arcs (amputates P3) or rigged dice (amputates P5 — the
  RimWorld storyteller escalation, our named anti-pattern, D-005).
  Fix shape: pacing *over* the honest sim — release latent seeded
  consequences when the story starves (DIR-1), never spawn from
  nothing.
- **F3 No audience epistemology — "the silence of the fortress."**
  Famine is announced by a corpse; jobs vanish silently when a worker
  flees. Not a UI problem: the simulator has no knowledge model of its
  *audience* — it knows everything and tells nothing. Note the
  symmetry: fortress-mode NPCs are equally blind (no runtime
  epistemology). Fix shape: treat the reader as a knower with a
  channel — gated chronicle lines, O(relevance) briefs; the same
  discipline our knowledge records impose on NPCs (`EVENT_SCHEMA.md`
  §3).
- **F4 Fidelity cliffs — "the fragile world."** One constructed pillar
  holds up a mountain; fluids are approximations; units path through
  each other. Full fidelity where it is fun (organs), corner-cuts
  where the designers bet nobody looks — and players always find the
  seams. Fix shape: honest abstraction boundaries — what is not
  simulated is a *documented* non-goal (`MVP_SCOPE.md` §2), and the
  render layer is licensed to invent exactly inside that documented
  gap (`VISION.md` §5 importance dial; the scene ledger D-048 keeps
  texture from laundering into canon).
- **F5 Monolithic fidelity — "the technical ceiling."** Everything is
  simulated at full detail, always; late fortresses crawl on strong
  hardware (single core). DF's own worldgen proves the cure — history
  ticks abstractly over populations + notables (`df_worldgen.md`) —
  but fortress mode ignores its own lesson. Fix shape: the LOD ladder
  (LOD-1 / P3d).
- **F6 History without a present — "no now."** The deep generator
  stops at play start; the v0.40 "world activation" (2014) keeps only
  coarse history running (armies, succession) at a fraction of
  worldgen density. Worldgen and runtime are different programs with
  different clocks. Fix shape: one log, continuous time (INV-1);
  micro/macro clocks layered later (`docs/blueprint/phases.md` §5).
- **F7 Macro-dense, micro-empty.** Legends records wars and artifact
  theft; no gossip, no street theft (`TECH_NOTES.md` §3) — the exact
  inverse of fortress-mode density, and the briefer's
  distribution-mismatch trap (the bg-3 honest note). *Measured
  (iter-8e, `TECH_NOTES.md` §3.1): confirmed with a refinement —
  bookkeeping 52–57%, micro 7.7–8.8% and it is notable-to-notable
  intrigue, not street texture.*
- **F8 Causality as archaeology.** Causes are reconstructed from
  `event_collections` + role fields, never recorded (`TECH_NOTES.md`
  §3; L7 names the anti-pattern). *Measured (iter-8e): only 19–24% of
  events sit in any collection, the groupings are strict single-parent
  trees, and 39–58% of deaths carry no slayer — the archaeology is
  sparser than assumed (`TECH_NOTES.md` §3.1).*
- **F9 Primitive epistemology.** Reputation is a 1–100 strength scalar
  (`hf_reputation_change`) — no channel, no fidelity; runtime rumors
  exist (adventure mode) but export poorly. DF cannot answer "who
  knows what, through whom, how faithfully" — the exact question
  `EVENT_SCHEMA.md` §3 answers.
- **F10 The static anchor.** The colony is nailed to one site;
  relocation is effectively impossible, and the wider world stays a
  backdrop the fortress cannot enter. F5's corollary: full-fidelity
  sites are too expensive to be mobile or plural. Fix shape: LOD
  makes plural sites affordable — the phase-5 site graph /
  running-world posture (`docs/blueprint/phases.md` §5).

### The successor matrix (what each "fix" cost)

The market proof of the structural read below: no successor kept all
six pillars. One-liners; the cited refs own the mechanics.

- **RimWorld** (`rimworld.md`) — attacks F1/F2/F3/F5 with readable
  feedback, storyteller pacing curves, tuned threat points, solid
  performance. Price: the world is a backdrop (P2 thin), pawns are
  shallow vs dwarves (P1 reduced), saves are snapshots (the amnesia
  anti-pattern), and the storyteller *rigs* variance (D-005) instead
  of explaining it.
- **Gnomoria** — interface legibility. Price: fewer intersecting
  systems (P3), and the project went quiet after its 2016 1.0 — the
  one-dev lifespan risk DF itself barely escaped.
- **Songs of Syx** — F5 at city scale: thousands of concurrent agents,
  the majority simulated in a simplified/batched state. Price:
  figure-depth (no per-organ specificity). Existence proof that the
  statistical tier of P3d holds at 10k+ scale.
- **KeeperRL** (`keeperrl.md`) — F2 via a focused war/progression
  loop. Price: a narrower intersection surface (P3 breadth).
- **Going Medieval** — the RimWorld shape, smaller. Price: the same
  trade plus a smaller world memory; confirms the family plateaus
  below DF depth.
- **Caves of Qud** — F3/F6 legibility of history: procedural history
  is injected into the present as explorable texture (sultan-era
  ruins, relics that name the dead) — the player excavates P2
  directly. Price: an RPG — history is setting, not a running
  simulation.
- **King of Dragon Pass / Six Ages** (`CORE_DESIGN_RESEARCH.md` §2
  row) — F1/F3 by construction: hundreds of hand-authored,
  state-gated scenes fire off the clan simulation; the selection
  layer IS the product. Price: finite authored content; the sim
  underneath is shallow — DF's trade inverted.
- **Wildermyth** (§2 row) — procedural characters through authored
  beats; scars and retirement persist as legacy. Price: the beat
  library is finite; the sim is thin.
- **Versu** (Evans & Short 2013) — the published sim/prose split:
  social practices as declarative data, text rendered from the same
  facts (Richard Evans: The Sims 3 AI lead). The closest ancestor of
  "simulator produces facts, LLM produces prose" (`VISION.md` §1).
  Price: small scope, discontinued, no persistent canon — the
  log-as-truth half is ours.
- **Prom Week** (McCoy et al. 2013; candidate ref-15) — social
  physics: ~20 social exchanges with numeric preconditions; relations
  gate which actions are available. Price: a tiny action space — our
  intersection matrix (`MVP_SCOPE.md` §6) is the generalization.
- **The Sims 3** (candidate ref-14; D-015 patterns-only) — F9
  partially: witnessed acts propagate as gossip/reputation through
  the social graph (Late Night, 2010); story progression advances
  off-screen households. Price: episodic amnesia — snapshots, not a
  log (the Mesa/Sims amnesia row, `rimworld.md` weakness).
- **Rain World** — the F2 counter-proof: variance stays high but
  reads as *fair* because every creature visibly runs its own ecology
  (needs, food chains, territory). Fairness = legibility, not low
  variance. Price: no drama manager at all and a difficulty ceiling
  that excludes most audiences (a posture `VISION.md` §8 rejects for
  us).
- **SpaceStation 13** — F1's extreme case: deep systems × human crew
  produce chaos; the chronicle is *external* — communities retell
  rounds after the fact. Proof that audiences will narrate for free
  when the facts are specific: the strongest external validation of
  "the log stores canon; prose is derivative" (`VISION.md` §1).
- **Cataclysm: DDA** (`cdda_data_json.md`) — DF-adjacent depth at
  content scale; the same late-game monolithic-fidelity trap (F5),
  plus the content-as-JSON standard we already borrow.

### The structural read (the thesis)

Every successor that "solved" DF amputated a pillar to do it: RimWorld
traded depth for readability, King of Dragon Pass traded simulation
for authored selection, Songs of Syx traded figure-depth for scale,
Rain World traded audience reach for honesty. The flaws are not wrong
simulation — they are **missing layers**: salience (F1/F3), pacing
(F2), audience epistemology (F3), LOD (F5/F10), continuity (F6).
Adding layers over an honest simulation is precisely the canonsim
thesis: the canon log stays DF-honest; the missing layers arrive as
read-side machinery (importance gate → brief → narrator) and
planning-side machinery (the director over the seeded buffer), with
the LOD ladder underneath. No prior project has the full stack — the
pieces exist (Versu's split, KoDP's selection, L4D's pacing, DF's
canon); the composition is the novelty, and `BLUEPRINT.md` §1 is that
composition. This is the elegant middle: multiply DF's pillars and
RimWorld's readability at once, because they live on different layers.

**What we take.**

- **The pillar-vs-layer checklist.** Any design debate resolves
  against P1–P6 (multiply pillars) before F1–F10 (patch flaws), and a
  flaw fix must be a layer, never a sim amputation. E.g. the D-045(b)
  importance-rule knob is F1 work on the delivery layer, never P5
  work on the engine.
- **"Losing is fun" as data.** Irreversibility
  (`state_changes.irreversible`, T4) + consequence pairing (L8) make
  tragedy *retellable*; the salience layer (the F1 fix) makes it also
  *readable*. Tragedy with a legible cause chain is content; tragedy
  without one is the F2 complaint.
- **Reader-as-knower symmetry.** The chronicle and the brief apply
  the NPC knowledge discipline to the audience: the importance gate
  is what the reader is "told", the brief's O(relevance) law
  (`VISION.md` §5) is F3's cure. Recorded as a design-consistency
  law; zero new machinery.
- **The cats test (a T7 lens).** An emergent cascade must be
  retellable from the log alone — T7 ("chronicle readable and
  retold by a human") sharpened to cascade granularity. A
  test-design lens, not a new test.
- **The Rain World law.** Never fix F2 by rigging the sim; fix it by
  explaining the world (narrator legibility) plus pacing releases
  (director). Confirms D-005 and the phase-3 refinement posture
  (`docs/blueprint/phases.md` §3).
- **Songs of Syx's batched-agent proof** for the statistical tier of
  P3d (a phase-5 design note: dormancy is affordable at 10k+ scale).

**What we adapt.**

- **bg-1 pipeline hardening** (beyond the `TECH_NOTES.md` §3
  pitfalls): stream the parse (`xml.etree.ElementTree.iterparse` +
  element `clear()` — never DOM); import selectively (skip art/dance/
  musical/poetic forms — briefer noise); normalize names (canonical
  name + translation as alias — the translated-name layer becomes
  data, not garbage); determinism quarantine (`df_version` +
  `dfhack_version` + `export_mode` recorded in meta; mismatch →
  reject, never repair; no golden DF fixtures committed —
  cross-version reproducibility is not a DF property, so exports stay
  gitignored runtime artifacts). Community XML viewers (Legends
  Browser et al.) prove the format parses at scale — pattern only,
  not cataloged.
- **bg-2 ambiguity as data.** An event whose causality cannot be
  grounded records `cause: null` + `candidate_causes` inside `outcome`
  — legal today (type-specific payload fields are pack data,
  `EVENT_SCHEMA.md` §11); trains briefer/validator on incomplete
  causality, realistic for phase-4 retrieval. Measured grounding
  (iter-8e, `TECH_NOTES.md` §3.1): the original trigger (2+
  collections referencing one event) fires never in real exports —
  direct refs are unique and collections are single-parent trees;
  ground `candidate_causes` instead on absent role fields (no slayer
  on 39–58% of deaths) and on the ~77–81% of events outside any
  grouping. Canon-level multi-parent grouping stays deferred (P3c —
  now our own design idea, not a DF-export property, per
  `df_legends_xml.md`).
- **bg-3 corpus division of labor.** DF canon serves macro-scale
  retrieval stress (measured iter-8e: 0.32–2.3 GB per world,
  4.5×10^5–1.2×10^6 events — an order above the old 10^4–10^5
  estimate; `TECH_NOTES.md` §3.1); micro-event interestingness is
  measured on our own chronicle (the bg-3 honest note). Synthetic
  micro-events injected from DF macro-events were considered and
  rejected: they contaminate the one thing DF canon is *for* (scale
  realism) and duplicate what our own log already provides
  (micro-density). Two corpora, two jobs — no synthesis.
- **F4 discipline for the narrator.** The non-goals list
  (`MVP_SCOPE.md` §2) doubles as the texture license boundary: the
  pack documents what is not simulated, the importance dial licenses
  invention exactly there, the scene ledger (D-048/D-049) bounds it,
  and the validator catches prose that asserts state the sim never
  wrote.

**What inspires us.** The enchantment equation: **specificity ×
honesty × surprise, delivered through the audience's imagination.**
DF proves the three multipliers compound; its delivery channel
(symbolic interface + the player's head + community retelling) does
not reach our audience. `VISION.md` §3's closing line — "Simulation
without rendering is unreadable; rendering without simulation is
unaccountable" — is the DF lesson stated as architecture: we keep the
simulation, replace the delivery (brief → narrator → validator), and
make canonical what DF only offers as an export mode.

**Strengths.**

- Two decades of proof that emergent depth outlives authored content;
  the community story corpus (Boatmurdered, the cats) is permanent
  marketing — the stories ARE the product, the property the owner's
  goal function encodes (`CORE_DESIGN_RESEARCH.md` §0: depth and
  connectivity, never volume).
- Legends export exists at all — the only irreplaceable external
  resource (`ROADMAP.md` §4).
- "Losing is fun" — the founding precedent for
  irreversibility-as-content (T4, L8).

**Weaknesses.** (one-liners; the §F rows above are the owners — this
expands the `CORE_DESIGN_RESEARCH.md` §2 row "micro-empty; dry prose;
causality reconstructed")

- F1 no salience layer; F2 no pacing layer; F3 no audience
  epistemology; F4 fidelity cliffs; F5 monolithic fidelity (FPS
  death); F6 frozen worldgen; F7 macro-dense/micro-empty; F8
  reconstructed causality; F9 scalar reputation; F10 the static
  anchor. Each is a missing layer, not a wrong mechanism.

**Verdict.** DF is the existence proof for the thesis and the caution
tale for delivery: copy the honesty (P5), the specificity-through-data
(P1 → pack), the canonical record (P4 → log); never the delivery
stack, never the monolithic fidelity, never the frozen history. Every
flaw already has an answer in the architecture or a recorded phase:

| Flaw | canonsim answer | Owner |
|---|---|---|
| F1 salience | importance rule (pack data) + `tale_gate` + brief recall ranking | `EVENT_SCHEMA.md` §6, `docs/BRIEF_SPEC.md` |
| F2 pacing | director = consequence planner + narrative entropy floor; phase-3 refinements | `docs/DIRECTOR_SPEC.md`, `docs/blueprint/phases.md` §3 |
| F3 audience epistemics | reader-as-knower: gated chronicle + O(relevance) brief | `VISION.md` §5, `docs/BRIEF_SPEC.md` |
| F4 fidelity cliffs | documented non-goals + INV-4 + validator + scene ledger | `MVP_SCOPE.md` §2, D-048/D-049 |
| F5 monolithic fidelity | the LOD ladder | LOD-1 / P3d, `docs/blueprint/phases.md` §5 |
| F6 no "now" | one continuous log; layered clocks | INV-1, `docs/ref/df_worldgen.md` |
| F7 micro-empty | the micro-dense slice + the bg-3 honest note | `MVP_SCOPE.md`, `docs/TASKS.md` bg-3 |
| F8 reconstructed cause | first-class `cause` at write time | L7, `EVENT_SCHEMA.md` §2 |
| F9 scalar reputation | knowledge records: channel + fidelity + decay | `EVENT_SCHEMA.md` §3, D-006/D-007/D-008 |
| F10 static anchor | plural affordable sites at phase 5 | `docs/blueprint/phases.md` §5 |

Nothing here gates phase 1. The doc feeds bg-1 hardening (pipeline
guidance), bg-2 (ambiguity-as-data), the phase-3 director posture, the
phase-5 LOD design, and the phase-1 narrator-legibility posture
(reader-as-knower).

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
