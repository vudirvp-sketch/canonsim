# CONTRACTS.md — Pre-Implementation Contracts

> What this file is: the compact pre-implementation contracts for the
> contract-write rows (intake-29/D-175's closing proposal, written
> iter-144/D-177 under the owner's delegation). A contract pins what a
> row's build must satisfy BEFORE it starts: the decisions the row
> leaves open (each grounded in standing code or law), the invariant
> set, the falsifier (TEST_PLAN §9's claim-packet form), the minimal
> test set. What it is NOT: the row's spec — the spec fires
> just-in-time at the row's start, FROM experiment results
> (SPECS_BACKLOG's header law); the contract is the boundary, the spec
> the implementation's own words. Ownership never moves: TASKS owns
> WHAT/WHEN (the ORDER owner decides), the row keeps its acceptance
> criteria, this file owns the pre-implementation HOW-boundary. When a
> row's build lands, its spec absorbs its contract by reference (never
> restated, D-024) and the section here collapses to a one-line
> pointer. Cap-law: `docs/*.md` ≤600 lines, substance-filtered
> (AGENTS §6.1).

## 1. roads-1 — the topology contract (the generated-exits pass)

Row: `docs/TASKS.md` `roads-1` (mode G must EMIT exits for generated
worlds). Starting material: the intake-29 sharpening (D-175 (2)) plus
the iter-104 read-path resolution the row already carries.

### 1.1 The pinned decisions

**D1 — the NODE question: the graph spans CLAIMED LOCATIONS only.**
The node set = the locations carrying at least one `worldgen.claims`
entry; unclaimed lattice sites are never graph nodes. Grounding:
every named consumer reads location-to-location edges — the warm ring
(`core/lod.py::scene_zones` reads the active location's `exits`), the
intent door's move validation (targets are location ids), the travel
edge lookup — and the derived price (`core/travel.py::travel_ticks`)
prices an edge only when BOTH endpoints are claimed locations (D-122's
map-graph coherence: an edge-local price needs edge-local sites). A
pass over all sites would emit edges no consumer can read: on a
200–600-site lattice with 3–6 claims, k-nearest over all sites mostly
hits unclaimed sites (the audit's measured fact), and an unclaimed
endpoint maps to nothing through the claims. Node geometry = the
location's claimed site SET (a location may hold several claims —
`core/travel.py::_claimed_sites` the precedent read); the distance
between two nodes = the MINIMAL Chebyshev cross-pair lattice distance
(`core/worldgen.py::lattice_distance`) — one metric, two readers (the
price reads the cheapest cross-pair for COST, the topology for
LENGTH).

**D2 — the algorithm NAMED: an MST backbone plus a bounded-degree
nearest overlay (the union graph), pack-parameterized.** The bare
"MST/k-nearest" wording is retired (a tree and a bounded-degree graph
are different behavioral surfaces). The combination carries the
fence's three questions (D-174), answered here:

- *Mechanism-of-advantage decomposition:* the MST (Kruskal over the
  claimed-node set, weight = D1's metric, tie-breaking per invariant
  I5) earns CONNECTIVITY — the one property it guarantees by
  construction; the nearest overlay (each node's k nearest nodes,
  k pack-declared, edges not already in the tree) earns ROUTE CHOICE
  (competing priced edges — a travel decision, not a pathfinding
  feature) and RING DEPTH (who simulates at macro cadence). Neither
  plus is carried without its named earner.
- *Combination price:* edge count n−1 plus up to n·k/2 deduplicated —
  longer exits lists (the brief/render surface) and larger warm rings
  exist ONLY because of the union; the determinism surface doubles
  (two tie-breaking disciplines to pin).
- *Frankenstein test:* operationalized as the build's own kill arm
  (§1.3 F5): overlay on vs off on the same world; if the measured
  LOD/autonomy/travel-decision surface shows no difference beyond
  edge count, the overlay is REJECTED for the committed pack (k=0)
  and the tree stands — the fence's reject arm pinned BEFORE the
  build, never after.
- k is PACK DATA in the new `worldgen.roads` sub-block (the
  `worldgen.watershed.neighbors` precedent: a pass's shape parameter
  is declared, not engine-constant); k=0 is legal (the tree-only
  world — the province's authored artery IS a tree). The sub-block's
  closed vocabulary is the build's lint edit; `core/pack.py` grows,
  so the pack.py-split rider rule (D-175) rides this row's build if
  it is the first pack.py-growing row to start (roads-1 is the
  readiness head).

**D3 — the read path (iter-104's law, unchanged by this contract):**
ONE shared read `exits(location)` — the authored record wins when
declared (the pack wins), else the pass-derived edges; the graph
lives on the WorldModel (L11: derived, rebuildable, never truth — a
pure function of the header seed + pack); NO canon births (INV-1
untouched: seed-dependent derived data stays out of the log; the
`world_formed` outcome block stays as-is). The consumers re-point
through the one read.

### 1.2 The invariant set (asserted at emit — the pass's own law)

- I1 CONNECTED: exactly one component over the claimed nodes.
- I2 NO SELF-LOOP; SYMMETRIC (an undirected edge lands in both
  endpoints' derived exits lists).
- I3 BOUNDED DEGREE: at most (n−1) backbone edges plus k overlay
  edges per node; asserted at emit (the authored precedents run
  degree 1–4: road max 4, province max 3).
- I4 PATHOLOGICAL-EDGE BOUND: every edge ≤ `worldgen.place.max_edge_span`
  lattice steps (place-1's law RELOCATED into the pass, asserted at
  emit where the data is born — relocated, never weakened). CONFLICT
  RULE: if the claimed set cannot be connected within the declared
  span, the pass fails LOUD (`WorldgenError`, the pred-contract
  family D-111) — connectivity is never bought by breaking the span;
  the pack author fixes placements or raises the span. Authored
  packs keep the load-time lint unchanged.
- I5 DETERMINISTIC TIE-BREAKING + EDGE ORDER (INV-2): candidate edges
  ordered by (weight, site-index pair, location-id pair); each
  location's derived exits list renders in that order (the warm tuple
  follows the exits list's own order — `core/lod.py`).
- I6 CYCLE POLICY: cycles are LEGAL and are the overlay's purpose
  (the road pack's authored triangle is the precedent shape); the
  backbone alone is acyclic; no multi-edges.

### 1.3 The falsifier + the minimal test set (TEST_PLAN §9, build-time)

**F — the claim packet.** Claim: "the generated topology is a
behavioral mechanic, not a pathfinding feature." Lens: the
changed-next-decision unit (the §9 depth family). Prism: the
same-seed fork (same world, k=0 vs k=2) plus the one-knob perturb.
Oracle: MEASURED differences in WHO simulates (the warm-ring
composition per active location across a run), the travel decision
surface (competing priced routes offered at the door), and route
metrics — never route existence alone. Falsifier: no measurable
LOD/autonomy difference between the arms → the overlay's mechanism
claim REJECTED (D2's kill arm). Scenario: the province geometry (324
sites, 6 claims, span 4) at the smoke seed, the corpus playscripts'
fork family. Counterexamples: the star topology (one hub, degree
n−1 — legal, the bound holds), the two-cluster span violation (the
loud failure, I4).

The tests: (1) the topology invariants I1–I6 at emit over the
committed province block and a fixture pack with k>0 — every
invariant an assertion, the loud span failure its own case; (2)
determinism: same seed + pack → the identical derived graph (the
WorldModel rebuild law); (3) the pack-wins override: an authored
`exits` record never reads the pass; (4) zero corpus price: the
golden T1 byte-compare and the corpus pins unchanged (no canon
births); (5) the claim packet F run — the build's own evidence,
recorded in the row's TASKS detail at landing.

## 2. res-1 — the substrate contract (the resource/economy layer)

Row: `docs/TASKS.md` `res-1` (the closed scarcity cycle). Starting
material: the intake-29 sharpening (D-175 (1)) — the mechanism split,
the irreversibility split, the verification form.

### 2.1 The pinned decisions

**D1 — the MECHANISM SPLIT (PACK_SPEC §1's WHAT/HOW test): the
quantity substrate is a new WHAT in core, NAMED.** The audit's fact
pattern holds: no quantity primitive exists (the resolver registry
`core/resolvers.py::REGISTRY` is a closed mechanic vocabulary; items
are discrete `{position, carrier}` records; statuses are per-NPC
decay axes; the population cardinality is a derived unborn-count; the
macro surface emits aggregate outcomes, never declarative stock
deltas) — a pack-only implementation would grow the hidden mechanism
the row itself forbids ("never a second economy engine"). The
substrate's minimal domain-blind shape:

- **account** — a named non-negative INTEGER stock bound to a canon
  entity id (any kind the pack declares it on: npc, location, group
  — the owner-agnostic form); the account KIND is pack-declared
  vocabulary (the `states` axes' own law: pack names, engine
  mechanics); the level rides `state_changes` (the existing channel —
  `{entity, prop, from, to}` with integer from/to, the position
  family's own shape).
- **three event verbs through the canon door** — source (declared
  units enter an account), transfer (units move between two
  accounts), consume (units leave to a declared sink); the exact type
  names are the build's naming pass, INV-3-clean by the stoplist
  self-check (account/source/transfer/consume are mechanic words).
- **integer-only arithmetic** (the travel law): add/multiply only, no
  division anywhere in the substrate; prices are DERIVED read-side
  values (pure functions of pack formulas + stock reads, L3 — never
  stored, never an event).
- **flows as aggregate macro-events** on the maclock cadence ride the
  D-112 one-event-with-cardinality surface (`core/macro.py::
  macro_turn_draft` the precedent) — log growth O(declared flows ×
  macrobeats), never O(members × ticks).
- **the economy stays PACK DATA** (the row's own law): the resource
  graph — which accounts exist, source/sink declarations, flow
  amounts and cadences, thresholds, price formulas, faction coupling
  — lives in a new rules block; the lint grows its shape checks (the
  pack.py-split rider rule rides whichever pack.py-growing row starts
  first — roads-1 is the readiness head).

**D2 — the IRREVERSIBILITY SPLIT: event immutability ≠ stock
immutability.** A consume event never un-fires (INV-5's log law); a
stock's LEVEL is an ordinary mutable value — `7 → 12` by a source
event is a legal new event, never a "revert". The `irreversible`
state_change flag (EVENT_SCHEMA: "never reverts without an explicit
counter-event" — the decay family's spontaneous-reversion law) is
NEVER set on stock props: the wrong instrument. A stock prop is not
a decay axis either — the decay pass never touches account props.

**D3 — the underflow floor: refused, never a negative write.** A
transfer/consume that would drive an account below zero is
world-impossible: a player-scaled attempt dies soft at the front door
(`intent_rejected` — attempts are facts, the loud/soft line); an
aggregate flow that would underflow fails LOUD at the commit gate
(D-035 — the write never lands). No code path ever writes a negative
stock.

**D4 — the arming law (the 68a pattern): the substrate lands
UNARMED.** No committed pack declares the economy block at landing →
zero events, the golden T1 fixtures and the corpora byte-untouched;
the first consumer pack (the pack-1/pack-4 family or world-2's own
row — the ORDER owner's call) arms it and pays its own corpus price.

### 2.2 The invariant set

- I1 all stock changes through the canon door: the three verbs are
  the ONLY write path (INV-1; the log writer's privilege separation,
  D-031); every level change rides a `state_changes` entry.
- I2 CONSERVATION: every account's folded balance == Σ sources −
  Σ consumes ± net transfers; nothing appears or disappears outside
  declared sources/sinks (the oracle below is its test form).
- I3 the non-negative floor (D3).
- I4 integer-only, prices derived (D1).
- I5 the decay separation (D2): account props never appear in the
  decay pass's axis set.
- I6 the unarmed landing (D4): zero events on the committed packs.

### 2.3 The falsifier + the minimal test set (TEST_PLAN §9, build-time)

The row's "four proofs" = §9's rows instantiated. **F1 conservation
oracle** — computed by INDEPENDENT re-derivation (a test-side ledger
replay over the raw event list, never the runtime's own fold — §9's
oracle law). **F2 the no-negative floor** — every account ≥ 0 at
every fold point; both refusal arms pinned. **F3 the
player-decision-effect arm** — the priced-option question (intake-27)
the counting form: remove the player's spend/consume options (a
`--systems-minus`-style arm) → the world's answers measurably differ.
**F4 the one-knob ablation** — one declared source/sink/flow knob
perturbed → the expected surface moves and no unrelated run perturbed
(the same-seed fork the follow-up).

The tests: (1) the conservation oracle over a fixture pack's economy
log (aggregate and discrete events both); (2) the underflow refusals
— the soft door (`intent_rejected`, no state write) and the loud
gate (the aggregate case); (3) the decay separation (a long-horizon
run's stock unchanged without economic events); (4) integer
determinism + the unarmed law: the committed packs' corpora
byte-identical at landing; (5) INV-3: the stoplist self-check over
the new names; (6) price derivation purity: same inputs → same
derived price bytes, never stored, never logged.

## 3. since-1 — the baseline contract (the re-encounter delta)

Row: `docs/TASKS.md` `since-1` (the per-entity line family on the
brief's entity cards, BRIEF_SPEC §3.4's extension). Starting
material: the intake-29 sharpening (D-175 (3)) plus the row's own
content families (status-axis deltas, position/membership transfers,
relation flips, the knower's heard records).

### 3.1 The pinned decisions

**D1 — the baseline sense NAMED: LAST PHYSICAL CO-PRESENCE (the
per-entity encounter epoch).** "The last co-presence tick" gains its
standing definition: a per-(reader, entity) ENCOUNTER EPOCH — an
epoch opens when the two become co-present (either one's arrival at
the other's location; presence per `core/fold.py::present_entities`
— position at the shared location, or the carried-item closure), and
closes when the co-presence breaks (either moves away; a dropped item
at the reader's feet stays co-present, a carried-off item breaks).
The delta window = [end-of-previous-epoch, start-of-current-epoch):
what changed while apart. The other four senses are distinct and
rejected with cause:

- *last scene* (`brief/ledger.py::scenes` — the PC-location interval,
  identity `(location_id, ordinal)`): the scene is the reader's
  interval, not the pair's — the reader can leave and return while
  the entity stays; a new scene opens without any encounter ending.
- *last brief observation*: perception-side and lossy — budget
  eviction (the `[truncated:N]` law) can drop an entity's line
  without any meeting; never a timeline authority.
- *last known fact*: epistemic, not physical — a rumor heard about
  the entity would reset the baseline with no meeting (the D-008
  belief half is CONTENT for the delta, never its window).
- *last entity re-entry*: one-directional — the epoch must also open
  when the READER arrives at the entity's location.

**D2 — the surface separation (explicit):** `scene_delta` = "what do
I perceive now" (the beat window, BRIEF_SPEC §3.2); since-1 = "what
changed in this entity since we last met" — a DIFFERENT block, never
merged; the lines ride the entity cards' family (BRIEF_SPEC §3.4's
extension per the row; the exact slot is the build's BRIEF_SPEC
edit). The block budgets follow the standing family (soft/hard caps
+ the `[truncated:N]` marker — never a silent drop).

**D3 — the blind-NPC inheritance (TEST_PLAN §1.3):** the delta lines
carry only what the READER could perceive: the comparison basis at
the epoch boundaries is the reader's perceived surface (present-set
membership, observable props, heard records), never raw state — a
change the reader never saw stays silent (an unperceived change
during co-presence is not re-surfaced later: the reader never knew
the before-state). The knower parameterization follows the retrieval
index's own law (`core/retrieval.py` — the `knower` boundary); a
non-PC reader is a legal future consumer, the world-2 condensing
travelers the row's named first.

**D4 — the pack owns the line vocabulary** (the row's own law): the
delta's line shapes are pack template data; the fold supplies the
structured deltas, the pack renders them.

### 3.2 The invariant set

- I1 ZERO canon writes: the epochs are a pure fold of position events
  (the `scenes()` shape — read-side view state, never logged; the
  row's own law); zero streams (INV-2 — no RNG anywhere in the fold).
- I2 the surface separation (D2): a distinct block, never merged into
  `scene_delta`.
- I3 the blind-NPC inheritance (D3).
- I4 determinism: same log → identical delta bytes (the read-side
  purity law; construction order everywhere).

### 3.3 The falsifier + the minimal test set (TEST_PLAN §9, build-time)

**F — the claim packet.** Claim: "the re-encounter line changes the
reader's next decision" (the row's own consumer: world-2's condensing
travelers). Lens: the changed-next-decision unit. Prism: the
same-seed fork with the block on/off (a `--systems-minus`-style arm)
over a condensation-heavy corpus run. Oracle: the reader's subsequent
intents/answers measurably differ with the block on; the block's own
bytes deterministic. Falsifier: no decision difference in the fork →
the line is decorative for the corpus — REJECTED as a standing block
(the pack's authoring problem, not the fold's).

The tests: (1) the epoch fold — a fixture log's meet/part/remeet
sequences → the boundaries exactly at the co-presence interval
edges, both arrival directions opening epochs (independent
re-derivation: hand-computed boundaries vs the fold); (2) the window
content — apart-window changes surface, during-co-presence changes
do not (scene_delta's own territory), unperceived changes stay
silent; (3) the surface separation — the block renders apart from
scene_delta, the budget family applies; (4) zero canon writes + zero
corpus price — the fold is pure, no new event types, the committed
corpora byte-untouched at landing; (5) the multi-reader
parameterization — the knower boundary honored (an NPC reader's
delta differs from the PC's on the same log).
