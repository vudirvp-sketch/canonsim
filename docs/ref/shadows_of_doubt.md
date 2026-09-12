# Shadows of Doubt · `REFERENCES.md` §10 · proprietary (design notes only) · phase 6 / track A (res-1 / the theft family's state-surface confirmation)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1 (ref-20, 4-batch + the
> Kenshi economy loop). Anti-drift (D-026): catalog/license/URL/phase
> gating in `docs/REFERENCES.md`; one-line synthesis in
> `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics here. Source is
> proprietary — public dev-logs (ColePow Games / Fireshine) and press
> coverage only. No code, no assets, no 1:1 rewrites (`REFERENCES.md`
> §0.5).

**What it is.** A procedurally generated detective-imm-sim (2023
early access) where **every item physically persists with an owner,
and every citizen has an address, a routine, and a social graph the
case files read** — the closest published thing to "theft with a
state surface".

**Concrete mechanics.**

- **Items as records with location + owner.** Every object in an
  apartment is an entity with a position (in-world, in-container,
  on-person) and an owner id. Moving/stealing an item changes the
  record; the world's response reads the record. The famous
  fingerprint/evidence layer: who-touched-what is queryable state.
- **Citizen records.** Each generated citizen: name, job, address,
  schedule, relationships, and a per-case role slot (killer, victim,
  witness). The mystery is *assigned onto* the simulation, not
  scripted over it — alibis resolve against the routines the sim
  actually ran.
- **The city as one database.** Buildings, rooms, doors, air-ducts,
  phones (with tappable call logs), bulletin boards — all readable
  nodes; the detective work is literally *querying the world state*
  through diegetic interfaces (cameras, eavesdropping, file theft).
- **Evidence decay and noise.** The sim generates red herrings as
  *real* unrelated activity: the database's other rows are the
  misdirection. No scripted decoys — a person who was near the scene
  is near the scene because they live two floors up.

**What we take.** **Theft leaves evidence = the theft/arson family's
state-surface confirmation** (the catalog row's own words): our
`take_failed`/`steal.failure` already mints the knowledge tokens
(`figure_reaching_for_purse`, `noise_by_the_bar`) with witnesses as
knowers — Shadows of Doubt is the proof-of-concept that a theft
*investigation* is a read over (item position change, who knew, who
was present), all three already canon fields for us (position as
event, known_by, presence). The **owner_id law** maps to res-1's
declaration shape: resource nodes carrying claims (whose iron, whose
mill) — ownership as a record the fold reads, disputes as events.

**What we adapt.** Their per-item database is unbounded (every
spoon queryable); ours is the lazy tier — items exist when declared
or when promoted (st-5's entity-birth door, owner-gated), the rest
is scene texture. Routines/schedules exist in our law as rotations +
urgencies (D-021) — the alibi resolves the same way (where was the
NPC when the event fired: the fold answers). The mystery-*generator*
(murder cases) is refused: our consequences are emergent chains (M3)
— but the *investigation surface* (asking around, reading who-knew
what) is the retrieval ladder + since-1's re-encounter delta, both
already built or routed.

**What inspires us.** The database IS the world: every clue the
player ever finds is a query against state that was true anyway —
zero authored clue objects, zero contradictions possible.

**Strengths.** The only published sim where physical persistence and
epistemics share one data model — and its detective layer works
*because* citizens' routines are real (alibi logic is unforgeable by
construction; our INV-1 is the same guarantee at event level).
Procedural citizens with social graphs prove cold-reading a generated
population can be the whole game. Red herrings from real rows is the
honest-noise law: misdirection without deception.

**Weaknesses.** Scale walls: the whole-city database limits city
size, and late-frame performance suffers (our answer: lazy tiers +
condensation — the unborn stay counts, VISION §3; SoD's universe is
small and dense where ours is wide and tiered). The sim's
citizens are socially shallow (name/job/routine, thin opinions) —
no trust dynamics, no rumor propagation; the epistemic layer is
player-only (our known_by + fidelity decay makes NPCs *also*
knowers and liars — the half they lack). Case-generation sometimes
needs patching when the sim produces degenerate setups (a killer
with no reachable witness) — our director's stagnation/buffer owns
that seam instead of patch scripts.

**Verdict.** The **theft family's confirmation donor**: position +
owner + knowers as one read surface — that our landed `state_changes`
+ `known_by` + presence already implement this grammar is the
phase-6 res-1 design's floor; the province's iron claims (owner_id)
and the theft investigations ride the same three fields.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
