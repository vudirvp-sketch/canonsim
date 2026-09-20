# Game-design practitioner talks corpus · REFERENCES.md §10 · proprietary (public talks/essays — pattern only) · presentation-1 consult + world-track donor material (D-191)

> Per-reference deep dive. Format template: this file §0. Iteration
> plan: this file §1. Anti-drift (D-026): catalog/license/phase gating
> in `docs/REFERENCES.md`; the cross-reference synthesis in
> `docs/BLUEPRINT.md`; concrete mechanics here. License
> filter and "patterns not content" rule: `REFERENCES.md` §0.7 (D-015).
> Scope fence: this file records the SOURCE layer (the owner's
> consolidated five-source knowledge base, auto-subtitle transcripts —
> names/numbers carry the source's own `(?)` marks, never re-verified
> here); the repo-facing residue was verified against HEAD at
> intake-33 (iter-166, D-191). The original full corpus lives outside
> the repo (the convenience-copy law).

**What it is.** Five practitioner sources on game DESIGN (not
worldbuilding, not narrative theory — the balance/psychology/
strategy-decision/procgen craft): S1 Josh Sawyer (Obsidian) on
attribute tuning in Pillars of Eternity; S2 Sid Meier on the
psychology of game design; S3 a Stardock video essay on the
micromanagement term; S4 Soren Johnson's Old World postmortem; S5
Herbert Wolverson on procedural map generation.

**Concrete mechanics** (per source, the transferable residue only).

**S1 — Sawyer, attribute tuning.** The viable↔optimal band narrowed so
no concept is unplayable (viable) while min-maxing stays possible;
the neutral point (10 = no bonus; below = penalty) because loss
aversion makes a −3% read roughly twice as large as +3%; base +
modifiers shown in UI, never a naked total; naming as signal (Might
≠ Strength tells the reader "this is different"); items grant bonuses
under stacking-max, so external knowledge buys marginal advantage,
never free points. Verdict: the numbers half is a PERCEPTION donor
(the card below); the balance half confirms the pack lint's dead-data
refusal + D-019 (thresholds from measurement, never guesses).

**S2 — Meier, player psychology.** The Unholy Alliance (the player is
the star; suspension of disbelief; respect the player's time; tonal
consistency); expectation thresholds (~3:1 odds read as "should win";
the absolute difference, not the ratio, can dominate); the invisible
roll breeds paranoia — an implausible outcome from an unseen RNG is
read as cheating; every failure must carry its cause and an avoidance
path; surprises belong outside the fundamentals; the Covert Action
rule (one center of gravity per game); the imagination economy
(render the caravan, not the seven dancing bears); listen for the
motive, never the proposed solution. The source's own anti-streak
fix BENDS the dice — that half does not transfer (INV-2; the honesty
law): the invariant is *perceived fairness*, and CanonSim can only
buy it at the render layer, never the roll layer.

**S3 — Battle Mode (Stardock), the micromanagement term.**
Micromanagement = excessive fiddling for small gains (NOT "many
units"); term drift → meme → studios solve a nonexistent problem by
gutting depth; the valid complaint is friction from *insignificant*
management. All three halves already repo law: term precision =
D-024 + the worldbuild terminology fence; insignificant-management
friction = the brief's fill law (the dropped count — nothing drops
silently) + mech-2's attention budget; verify-the-complaint-first =
D-175's measurement-before-mechanism. Confirmation only, the
thinnest source.

**S4 — Johnson, Old World postmortem.** The richest donor.
Interesting decision = trade-off + irreversibility + information
horizon; automation of a subsystem = red flag for that subsystem's
design; undo works BECAUSE combat is deterministic; infinite
tooltips as the turn-based standard; known-denominator design (the
fixed City Sites count grounds Victory Points — no exploitable
sliding target); the open market with buy ≈ 2× sell (conversion
lossy by construction — producing beats arbitraging); stockpiles as
one homogeneous shape so any pair can be exchanged through one
mechanism; 3000+ loosely coupled events (trigger + requirements +
effects, valid under many world states) written by many authors with
zero coordination; events-offer instead of table-negotiation (the
probing interface was the cursed design); AI without cheats, beats
the player on points only, gets no events — asymmetry as honesty;
characters die ⇒ forces change (the ECS cure: buildings and
technologies never die, people do — mortality is the anti-stagnation
engine).

**S5 — Wolverson, procedural map generation.** Direct and verify
randomness (generate toward a shape, then algorithmically check
reachability/solvability); the Dijkstra-map design applications:
cut the unreachable, safe-start near the desired zone, hide value at
the LEAST accessible point, the Hot Path (content placed along the
path between start and goal — rooms on the path live, off-path
rooms pruned or deferred), the locked-door/key guarantee (the key
flood-fill-proven to sit before its lock — solvability by
construction); combinations of techniques + prefabs (several, never
all) so the map tells a story.

**What we take.** THREE compact adoptions + ONE consult card:

1. **The outcome-perception laws card** (S1+S2+S4, parked behind the
   owner gate with presentation-1 — the third card joining the
   intake-30 visual card and the intake-32 Vantiel card; the
   falsifier: at the presentation-1 write, each layer either changes
   the narrator document's shape or dissolves as already-satisfied):

   1. TRUTH never bends — outcomes are decided by the simulator
      (INV-2, VISION §5); the perception work lives entirely at the
      render layer. (Neutralizes the source's dice-bending.)
   2. Every FAILURE carries cause + avoidance path in the render —
      the intent_rejected fact + L7 cause chains exist; the narrator
      must surface them, never render a naked "no". (S2's core law.)
   3. Odds read as expectation bands, never naked percentages on big
      numbers (S1: two-digit numbers + percentages read poorly); a
      low-probability outcome on a fundamental is rendered WITH its
      unlikeliness, or it reads as betrayal. (S2's paranoia law.)
   4. TRANSPARENCY is opt-in and bounded — base + modifiers for
      those who ask, through the expansion flags, nothing dropped
      silently (mech-2's law applied to the model-facing surface).
   5. Outcomes stay legible through RESIDUE — what changed, who
      remembers, who benefits (the world track's carrier discipline
      is the story-shaped answer to "what did the roll mean").
   6. STAKES stay irreversible — no outcome-bending, no engine-level
      undo; undo/branch questions are presentation-1's, fenced.

2. **The anti-arbitrage spread** (S4, the Resource open question's
   donor material — ANCHOR_REGION's "how does scarcity become a
   measured price/flow cycle?"): exchange between stocks is lossy by
   construction (the spread rides pack-authored transfer pairs over
   the account substrate — the mechanism, never the 2× number); if
   conversion were lossless, authored scarcity would dissolve into
   arbitrage. Falsifier (the water's own function-loss arbiter): if
   removing the spread changes nothing reachable, it is decoration.

3. **The turnover question** (S4's ECS cure → WORLD_AUTHORING §5):
   every authored force names what carries its function when the
   holder dies or leaves — the function-loss probe aimed at holder
   turnover, the world's anti-freeze law. Consumers: the camp's meso
   half (the charcoal debt's succession), W5's biography arc.
   Falsifier: the probe's own perturbation test.

4. **The Hot-Path placement pair** (S5, parked beside the intake-27
   topology-aware hook distribution proposal — its natural pair):
   rank placement by distance-from-artery; defer or prune the
   off-path; the key provably before its lock. Consumer: the
   pressure pack's road-traffic rider (the depth-7 condensation)
   when that row convenes. Falsifier: the ranking must change what
   is placed where, versus the junction/through/dead-end classes
   alone.

**What we adapt.** The weak-coupling authoring law (S4): an event
unit that is valid under many world states composes with every other
unit without author coordination — content grows without complexity
growth (P15's own shape). Rides pack-3's authoring material (the
next authored pack's event families), never a new mechanism — the
Paradox grammar row + D-005 own the grammar. The
homogeneous-stock exchange affordance (S4): because every value is
an account (res-1), any-to-any exchange offers are one transfer pair
away — a pack-design affordance, already expressible, never a
second subsystem.

**What inspires us.** The corpus is the strongest
outcome-perception donor the intake family has seen: every prior
GDC family (D-156 emergent storytelling, D-173 level design) is
about what the SYSTEM generates; this one is about how the outcome
READS — the one layer CanonSim owns the truth half of (determinism,
cause chains) but has never specced the framing half of.

**Strengths.** Practitioner-tested mechanisms with their failure
modes attached (the beta-tuning reversals in S1, the my-bad
catalogue in S2, the rejected 99-of-100 variants in S4); the
K-table — the corpus's own cross-source contradiction map (typed
disagreements + applicability conditions) — is a synthesis
discipline worth imitating in future intake one-pass records; every
principle arrives with the numbers that broke it.

**Weaknesses.** Transcript rot (auto-subtitles; names/numbers
unreliable — the corpus's own §N marks them, binding: no number from
this file may ride a spec); CRPG/4X player-psychology frame — the
"player" is an optimization-prone adversary with save/load rights,
which maps only partially onto a reader in an authored world; the
dice-bending fixes assume a hidden RNG, the exact opposite of
INV-2's inspectable log.

**Verdict.** PARTIALLY CONFIRMED (intake-33, D-191): a perception +
economy-craft donor, never a systems donor — one consult card (the
outcome-perception laws, parked with presentation-1), two compact
world-track adoptions (the spread's mechanism-form; the turnover
question), two parked placement/authoring notes (the Hot-Path pair;
the weak-coupling law), and the largest single batch of
cross-domain confirmations since intake-27 (INV-2/T2 = the
strongest anti-save-scum form; the one-id door = AI-without-cheats;
mechanics.py = infinite tooltips; the fill law + mech-2 =
automation-as-red-flag inverted for observability; MST-connectivity
= direct-and-verify's superior own form; the brief's blocks =
Covert Action's center of gravity). The do-not-import list is
binding: no dice-bending of any form; no 3:1/2×/N-levels numbers as
law (threshold leakage — the laws transfer, the constants do not);
no tech-deck, order-system, or no-counterattack mechanics (no
substrate, no consumer); no difficulty-level taxonomy; no Voronoi/
two-layer-noise worldgen additions (saturated by ref-8/ref-9 + the
LOD ladder); no K-table taxonomy as repo law (the per-finding
verdict discipline already owns it).

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
