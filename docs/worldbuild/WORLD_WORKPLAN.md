# Worldbuilding Workplan

**Status:** active.

This is the operational owner for the world track. It does not replace the
repository's engineering backlog. Engine work follows repository law; world work
uses the active worldbuilding surface and only asks for engine changes when an
actual authored need is demonstrated.

## 1. Completed consolidation

### W0 — Foundation reconciliation

**DONE.** Hard/working/mystery/deferred/rejected were separated and duplicate
canon surfaces were removed from the active reading path.

### W1 — World kernel

**DONE.** The durable world identity and load-bearing laws now live in
`WORLD_KERNEL.md`.

### Resonance consolidation

**DONE.** v0.2 mechanism + v0.3 torture tests now have one owner:
`RESONANCE.md`.

### Domain consolidation

**DONE.** Life/personhood, peoples, and culture/civilization now each have one
owner instead of overlapping foundation documents.

## 2. Current stage — Anchor Region

### Status: ACTIVE / PARTIALLY DEMONSTRATED

The current repository's Sarrow Vale province is the strongest concrete
implementation witness. The broader worldbuilding goal is not closed yet because
the meso and human-meaning layers are still thinner than the mechanical layer —
the first meso unit is authored (`ANCHOR_REGION.md` §6.1, iter-155) and embodied
at the single-NPC + companion band (the second hand and the pole, iter-157);
the debt's flow and further meso units are not yet embodied. The causal mesh is
audited — five independent loops, four committed (W3 done, iter-156,
`ANCHOR_REGION.md` §5).

The active deliverable is `ANCHOR_REGION.md`.

## 3. Immediate work

### A1 — Anchor Causal Map — DONE (iter-155)

The first pass existed in `ANCHOR_REGION.md`; the unsupported links deepened
through the crossing household: the Trade/Institutions/Actors/Culture/History/
Knowledge/Weather/Read-side rows answered at the authored band (§4's map);
Geography and Resource stay open (§4). The chain walked once end-to-end (§6.1).

### A2 — Meso unit — DONE (iter-155)

One ordinary meso unit authored: the crossing household (the weir stair's ferry
family — `ANCHOR_REGION.md` §6.1), connecting macro pressure (the seasonal rise,
the guild-held flood debt) to ordinary life through durable constraints (the
debt, the shelter law's edge), choices (the high_water rate, the purse-read
bend, the pole-or-road question) and consequences (the debt standing, the
reputation residue, the inherited pole). The unit's pack embodiment landed at
the companion band (iter-157: the second hand walks the artery, the pole
committed, KI#87 closed); the debt's economy flow stays the open engineering-side
question (the separate-track law).

### A3 — Meaning test — DONE (iter-155)

One concrete human-life slice run over the existing region — the high-water
double toll (`ANCHOR_REGION.md` §7.1): the same mechanical event through four
positions (the toll-taker, the hill carrier, the auditor, the guild), each with
a bounded map. Four of the five meaning probes answered at the authored band;
the Thornmill family obligation stays open. The next frontier is W4 (§6).

## 4. Next research only if needed

### Ancient Network

The source corpus identifies four unresolved upstream questions:

- network architecture;
- hydrological/climate engineering;
- migration and demographic redistribution;
- ancient political structure.

Do not open a new giant foundation document. Use a bounded research task only if
the current anchor exposes a contradiction that cannot be explained without one
of these pieces.

### Resonance edge cases

Do not add new powers. Extend the Resonance model only when an anchor or later
region requires a capability not already bounded by `RESONANCE.md`.

## 5. W3 — Causal mesh — DONE (iter-156)

The audit's two laws: the **disable test** (remove one loop's unique driver;
the others must still run) and the **shared-stage rule** (two circuits sharing
driver AND mediator are one mechanism counted once). Result: five loops pass —
fire → institutional response, feud residue → present politics, season →
weather → social signal, route → condensation → culture (all four COMMITTED,
per-loop tests green) + the credit loop (AUTHORED — `ANCHOR_REGION.md` §6.1's
unit; the debt's flow not economy-armed). The anti-double-count ruling applied
once: the theft → suspicion → document-check → arrest circuit is the fire
loop's mechanism family on another verb — counted in A, never a sixth loop.
Four named interlock edges: the alarm wakes both fear and grief (A⇄B), the
rain erases the smoke (C→A), the condensation materializes the feud's carrier
(B⇄D), the rise prices the toll (C⇄E). The mesh's map and verdict live in
`ANCHOR_REGION.md` §5; the test record in `WORLD_TESTS.md` §9. The next
frontier is W4 (§6).

## 6. W4 — Meso expansion

Only after the causal mesh is stable, add a small number of additional meso units:

- families;
- workshops;
- guild substructures;
- schools;
- markets;
- local legal/religious institutions;
- crews/caravans.

Each addition must create a new causal coupling, not just more names.

### The W4 working set (intake-31, D-189 — the operator-armed frontier)

The meso additions above are authored through the operator set
(`WORLD_AUTHORING.md` §5/§7/§8/§19 — the function-loss probe, the meso assembly
probe, the residue lifecycle trace, the natural-pattern transfer rule) and
verified through the probe forms (`WORLD_TESTS.md` §3 — the biography crisis
probe, the humor generator). The operators exist to find the coupling, not to
add volume; the source mechanics live in `docs/ref/kurvitz.md` (ref-21).

**The bounded experiment — RUN (iter-160, w4exp1): CONFIRMED at the split
band, the transfer KEPT.** The crossing household walked once through the
full stack on existing substrate only (the evidence record: `WORLD_TESTS.md`
§9; the household's authored residue: `ANCHOR_REGION.md` §6.1's lifecycle
table):

`flood / debt → function lost or constrained → replacement carrier / institution → heterogeneous household roles → biography crisis → residue lifecycle → one perturbation / ablation → reachable-state difference`.

Decision rule (the standing law, D-189 — the applied verdict below):

- a new causal capability from existing primitives → keep the mechanism as an
  authoring/test pattern;
- a repeatedly exposed substrate limitation → record it and route to the
  engineering side (a TASKS standing row on the owner's call, never from this
  track);
- richer prose or more names only → reject the transfer as decorative
  complexity.

Applied (iter-160):

- kept as authoring/test patterns — the carrier-availability law + the
  verb-gate boundary (`WORLD_AUTHORING.md` §8) and the carrier-ablation
  probe (`WORLD_TESTS.md` §7): a new causal capability composed from
  existing primitives (the movement beat + the carried-item position
  contract make the household's tool availability a lawful world state —
  test-pinned, `tests/test_companion.py`);
- the one repeatedly exposed substrate limitation (the debt's arithmetic —
  no account state; the third recorded exposure: A2's residue, Loop E's
  band, this run) stays owner-routed per the separate-track law; the
  lifecycle proved explanatory without the economy arm (one coin, two
  claims — the debt cleared vs the punt bought back);
- zero decorative residue — nothing added, nothing renamed; every tested
  transition's removal changes reachable futures (the perturbation test
  passed per transition).

Two first-exposure findings recorded, not routed (the crisis probe's honest
residue): the vigil never wakes for the stair (the elders out of earshot —
the crossing is not a feud location) and the reputation axis has no runtime
writer (D-006's own record; the breach response rides the knowledge/rumor
stack).

**Candidates (PROPOSAL — hypotheses, not canon; each carries its falsifier):**

1. **The flood debt as a lifecycle.** Does the debt become materially more
   explanatory when its holder, transfer/renegotiation, partial repayment,
   inheritance, and social interpretation are explicitly traced? Do not build
   an economy system first — test the lifecycle on existing substrate.
   TESTED (iter-160): the trace passes the perturbation test at the authored
   band (`ANCHOR_REGION.md` §6.1's table); the economy arm stays the
   owner-routed question.
2. **One social carrier.** The punt pole (committed, iter-157), the waybill, or
   the toll record: material function + social meaning + holder + recognized
   claim + transfer = a new meso coupling? The carrier must alter at least one
   relationship, obligation, or future option, or it is decoration.
   TESTED (iter-160) for the pole: the material half passes at the committed
   band (the position-modulation causal, test-pinned); the social-recognition
   half and the player-facing ablation are each one pack-data seed away (the
   recognition token, the `steal_target` flag — the owner's embodiment call,
   the KI#87 precedent class).
3. **A practitioner water-governance node.** Scarce resource → recurring
   allocation conflict → practitioner rule → immediate enforcement →
   legitimacy/resentment → memory (the irrigation-tribunal MECHANISM, never the
   institution; the real-world donor is documented in the source research —
   UNESCO, irrigators' tribunals of the Spanish Mediterranean coast). Survives
   only if it performs a function the guild's paper and the crossing's custom
   do not — the function-loss probe is the arbiter; the guild council must not
   be duplicated.
4. **A constructed kinship edge.** Care/bodily relation → socially recognized
   kin edge → obligation → inheritance/protection/exclusion (the milk-kinship
   MECHANISM, never the practice; the documented donor is the Hindu Kush
   foster-relations research). A future-region donor unless a concrete Sarrow
   need appears — the shelter law's fed-through-winter strangers are the native
   generator candidate. The edge must be expensive (priced by the residue
   lifecycle) or it inflates into noise.

## 7. W5 — Human tests

Run:

- biography;
- humor;
- heartbreak.

Use existing region state wherever possible.

## 8. W6 — Genre tests

Use the same region and pressure network to test:

`adventure / mystery / politics / relationship drama / tragedy / comedy / biography`.

A failed genre test should identify the missing world substrate rather than
trigger immediate plot writing.

## 9. W7 — Negative / compression tests

For any new major capability, regime or institution:

`why possible? why not universal? what does it replace? what does it make harder? who profits? who resists? who remembers? what if it disappears?`

Then run the compression test and remove or merge decorative material.

## 10. W8 — Integration readiness

The world track is ready for a broader implementation handoff when:

1. the anchor has an authored causal substrate;
2. at least one meso unit is demonstrated;
3. major content can be represented by existing pack primitives or a named,
   justified capability gap;
4. at least one ordinary event reaches a persistent human-scale consequence;
5. knowledge asymmetry is explicit;
6. world-specific material remains outside engine core ontology;
7. the tests distinguish what is proven from what remains hypothetical.

## 11. Expansion rule

The next region should be selected because it introduces a **new civilizational
coupling**, not because the map has room or the setting lacks a biome.

A suggested long-term sequence remains:

`riverine human-scale region → mountain/industrial regime → maritime regime → deepwater regime → necropolis/continuity regime → sky/closed-tech regime → cosmic layer only if earned`.

This sequence is a routing heuristic, not canon and not an owner order.

## 12. Explicitly deferred

Do not start these merely to make the setting feel larger:

- full atlas;
- encyclopedic species list;
- definitive religion catalogue;
- exhaustive language bible;
- continent-scale cosmology;
- FTL society design;
- dozens of new fundamental Resonance effects;
- production-ready world pack before the anchor/meso proof.

## 13. Exit principle

> **First prove one living region. Then scale the world.**

The quality gate is not "how much has been described?" It is:

> **How many different human histories can honestly emerge from the same causal substrate?**
