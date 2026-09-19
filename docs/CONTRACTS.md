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

## 1. roads-1 — LANDED (iter-145, D-178)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-145 + D-178 + worklog
> iter-145 own the landing record — the pass
> (`core/worldgen.py::_pass_roads`), the one shared read
> (`core/roads.py::exits`), the lint, the §9 claim-packet evidence.
> The contract's own pinned decisions, verbatim, in git history at
> the iter-144 commit.

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
