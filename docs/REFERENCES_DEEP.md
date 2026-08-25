# REFERENCES_DEEP.md — Per-Reference Deep Dives

> Companion to `docs/REFERENCES.md` (catalog) and `docs/CORE_DESIGN_RESEARCH.md`
> §2 (one-line synthesis). Where the catalog says "Mesa — Python ABM
> framework", this file says **what Mesa actually does, mechanically, and what
> we take / adapt / reject / inspire from**.
>
> Anti-drift (AGENTS §3, `AGENT_NAVIGATION.md` §3): the catalog stays the
> source for **license / URL / phase gating / intake rules** — never
> restated here. `CORE_DESIGN_RESEARCH.md` §2 stays the source for the
> one-line **depth primitive + failure mode** synthesis — never restated
> here. This file is the **concrete mechanics** layer: named systems,
> real data structures, pseudo-code where it earns its keep, honest
> strengths and weaknesses, a per-source verdict. Cap 400 lines
> (`AGENTS.md` §6). Review quarterly alongside the `doc-2` license
> re-verification.
>
> Phase law (`ROADMAP.md` §4, `MVP_SCOPE.md` §2) still owns when a source
> is *consulted*. Reading design notes early is allowed; vendoring early
> is scope creep. Nothing here lifts the phase-0 zero-external-code gate
> (D-012, D-015, D-022).

## 0. Format (every entry follows this template)

```
### <source> · <catalog §> · <license> · <phase/track>

**What it is.** One sentence: what the project IS, mechanically.
**Concrete mechanics.** Named systems, real data structures, a snippet
  where it earns its keep. Not a feature list — the parts that matter.
**What we take.** Specific, named — a class, a pattern, an algorithm.
**What we adapt.** Specific, named — and *how* we change it.
**What inspires us.** The design lesson (one clause, not a paragraph).
**Strengths.** Concrete virtues we cannot get cheaper elsewhere.
**Weaknesses.** Concrete defects — `CORE_DESIGN_RESEARCH.md` §2
  one-liners expanded here.
**Verdict.** One line: what role this source plays in our work.
```

If an entry would not fill every field honestly, the source is too thin for
a deep dive — leave it in the catalog only.

## 1. Iteration plan (which references get a solo iter, which batch)

A reference is **huge** (solo iter) if it has ≥3 distinct subsystems each
worth deep coverage, or if a real reading pass takes a full evening. A
reference is **batchable** (2–3 per iter) if its lessons fit one focused
session. This plan lives in `docs/TASKS.md` (infra backlog, `ref-N`); the
size verdict is recorded here so a future agent picks items in order
without re-judging.

| ID | References | Solo / Batch | Rationale |
|---|---|---|---|
| iter-0h | Neighborly + Mesa + DF Legends XML (export schema only) | 3-batch | framework setup + the three cousins already half-documented in `CORE_DESIGN_RESEARCH.md` §2 |
| ref-1 | DF worldgen + history layer (the half not covered in iter-0h) | solo | 5+ subsystems: history ticks, populations vs notables LOD, age/civ dynamics, artifact anchors, reputation as event |
| ref-2 | C:DDA `data/json/` schema | solo | the reference for content-as-JSON at scale — items, monsters, recipes, missions, factions; CC-BY-SA lets us lift |
| ref-3 | Paradox event scripting (CK3 + EU4 + Stellaris) | solo | three wikis, complex grammar (trigger / weight / mtth / effect / option / scope); phase-3 design backbone |
| ref-4 | RimWorld + L4D Director + Alien: Isolation | 3-batch | pacing/storyteller trio; all closed; design-notes only; phase-3 director ref |
| ref-5 | Wesnoth WML + Endless Sky mission DSL + ink + tracery | 4-batch | event/narrative grammar family; same conceptual shape |
| ref-6 | Brogue + DCSS + KeeperRL | 3-batch | roguelike emergence + micro-sim; environmental sim from few rules |
| ref-7 | Stanford Generative Agents + ai-town + letta | 3-batch | LLM-agent precedents — mostly negative; bg-4 cost notes overlap |
| ref-8 | Azgaar FMG + Natural Earth + GeoNames | 3-batch | worldgen data donors; phase-5 |
| ref-9 | libtcod + rot.js + Red Blob Games | 3-batch | FOV / pathfinding / grid math — pattern only (D-012) |
| ref-10 | entt + Bevy + EventStore | 3-batch | ECS scheduling + event-sourcing stream/projection patterns |
| ref-11 | SQLite FTS5 + DuckDB + sqlite-vec | 3-batch | storage layer candidates; depends on phase-4 retrieval decision |

## 2. iter-0h batch — the three cousins

### Neighborly · `REFERENCES.md` §2 · MIT · phase 5 (cousin); iter-3 (P2a pattern source)

**What it is.** C# agent-based settlement simulation (`ShiJbey/neighborly`,
MIT) — the closest existing cousin to canonsim's phase-5 settlement vision:
NPCs with relationships, jobs, personalities, and routines that produce
emergent narrative summaries.

**Concrete mechanics.**

- ECS-shaped core: `Entity` is an integer id; components (`Position`,
  `Relationship`, `Occupation`, `Personality`, `Mood`, `Health`) are
  struct-bags keyed by entity id; systems (`TimeSystem`, `SocialSystem`,
  `RoutineSystem`, `NarrativeLogSystem`) tick daily.
- `RelationshipTracker` is a **pair-keyed map** `Dictionary<(int, int),
  Relationship>` — key is a sorted tuple of entity ids; value carries
  axes (trust, friendship, romance, familiarity) plus a per-axis weight
  as tiebreaker in social decisions.
- `SocialSystem` iterates entities, asks `RelationshipTracker` for
  candidates (proximity + score above threshold), picks one, emits a
  `SocialInteraction` record (enum: greet, argue, compliment,
  small-talk…); updates relationship axes per type-specific delta tables.
- Narrative is **post-hoc**: `NarrativeLogSystem` runs at day's end,
  reads the day's `SocialInteraction` records, writes prose summaries —
  a *reader* over state, not a participant.

**What we take.**

- The **pair-keyed relationship map** shape — exactly P2a (D-020,
  `CORE_DESIGN_RESEARCH.md` §6): sparse pair-keyed relation map for
  NPC↔NPC relations in iter-3. The **system-per-verb** decomposition
  (`SocialSystem`, `RoutineSystem` as separate ticked scopes) matches
  our `sim/systems/` 8-system layout (`MVP_SCOPE.md` §5).

**What we adapt.**

- **State-mutating → event-emitting tick** (INV-1): Neighborly's
  `SocialSystem` mutates `RelationshipTracker` in place; we emit
  `relation_changed` events, the writer flushes, an incremental projection
  (D-023) updates relations. Event = truth; projection = cache (KI#5).
- **Post-hoc narrative → recorded log + template chronicle** (iter-5):
  we write events during the tick, `render/` assembles the chronicle.
  Replay reconstructs what was *reported* vs what *happened* — Neighborly
  cannot. Relations become derived state (fold over log,
  `EVENT_SCHEMA.md` §1), not a primary store.

**What inspires us.** The "settlement simulates itself without a player"
posture — confirms Kenshi's lesson (`CORE_DESIGN_RESEARCH.md` §3 row 4):
we don't invent the genre, we harden its epistemology.

**Strengths.**

- Readable C# codebase, MIT-licensed — pattern transfer is direct.
- Pair-keyed relations data structure validated ahead of us.
- System-per-verb decomposition maps one-to-one onto our 8-system layout.

**Weaknesses.**

- **Weak epistemology** (`CORE_DESIGN_RESEARCH.md` §2 row "Neighborly"):
  no `known_by`, no fidelity, no rumor-distortion channel. Our `knowledge`
  records (MVP_SCOPE §10, EVENT_SCHEMA §3) fill this gap.
- **State-mutating tick** — the Mesa amnesia pattern (below). Replay
  requires re-running; byte-compare impossible without external RNG logging.
- **No causal chain** — `SocialInteraction` has no `cause`. Our `cause`
  (EVENT_SCHEMA §2, P1a) is the missing ledger.

**Verdict.** Phase-5 settlement cousin. Iter-3 P2a lifts its pair-keyed
map shape. Its epistemology gap is the spec for our knowledge records;
its amnesia is the spec for our event log. Read the repo at iter-3.

### Mesa · `REFERENCES.md` §2 · Apache-2.0 · phase 0 (architectural pattern)

**What it is.** Python agent-based modelling framework (`projectmesa/mesa`,
Apache-2.0) — the reference implementation of the Model / Scheduler /
Agent / DataCollector pattern, and the closest language match to our
stdlib-only core.

**Concrete mechanics.**

- `Model` holds `self.schedule`, `self.random` (a single
  `random.Random(seed)` — same discipline as our INV-2), `self.running`
  flag, `self.current_id` for gap-free agent ids, and a `DataCollector`.
  Subclasses implement `step(self)`.
- `Scheduler` subclasses are pure **ordering policies**:
  `SimpleActivation` (insertion order), `RandomActivation` (shuffled by
  `model.random` each tick), `SimultaneousActivation` (two-phase: step
  into staging buffer, then commit), `StagedActivation` (per-tick stage
  list, all agents run stage 1, then all stage 2).
- Tick loop: `while model.running: model.step(); schedule.step();
  datacollector.collect(model)` — see `mesa/model.py` + `scheduler.py`.

**What we take.**

- **Single-RNG-instance discipline.** Mesa holds one
  `random.Random(seed)` on the Model — exactly our INV-2; Mesa is the
  Python reference that it works. **Model / Scheduler / Agent
  vocabulary.** `core/` ≈ Model; `heapq` queue keyed `(tick, sub_order,
  actor_id)` ≈ Scheduler (stricter policy); `sim/systems/*` ≈
  per-system Agent.step() pieces. DataCollector precedent —
  `agent_reporters` / `model_reporters` ≈ our M1–M5 metrics
  (`CORE_DESIGN_RESEARCH.md` §6 P1b–d, D-019), but computed by folding
  the JSONL log, not by collecting at runtime.

**What we adapt.**

- **`agent.step(model)` → event emission** (INV-1): Mesa's agent decides
  and acts in one call, mutating state directly. Our agent produces an
  `Intent`; the queue decides ordering; the writer flushes; the projection
  applies. Intent = decision unit; Event = state-change unit (Spec-Talk
  boundary, `MVP_SCOPE.md` §7, `EVENT_SCHEMA.md` §1).
- **Scheduler → heapq** (INV-2): we key the queue by `(tick, sub_order,
  actor_id)` so ordering is deterministic without per-tick reshuffling.
  `SimultaneousActivation` two-phase is on file — a future phase may want
  simultaneous-intent resolution; not phase 0.

**What inspires us.** The **framework-not-engine** posture: Mesa is a
library, not an executable — matches our stdlib-only posture (D-012). The
"scheduler = the policy" insight is the same lesson as our queue key:
ordering is the design lever.

**Strengths.**

- Same language as our core (Python) — pattern transfer is one-to-one.
- Apache-2.0, mature, widely taught; many reference models in-repo.
- Single-RNG-instance discipline is literally our INV-2.

**Weaknesses.**

- **Pure ABM = episodic amnesia** (`CORE_DESIGN_RESEARCH.md` §2 row
  "Mesa"): `step()` mutates state; no event log; replay = re-run, not
  fold. Our JSONL log + `state_changes` is the amnesia fix.
- **No causal chain** — `agent.step()` is opaque; the "why" lives in
  agent code. Our `cause` (P1a) records this at the event.
- **No content/code split** (INV-3) — Mesa has no opinion on domain data;
  that's our addition via `content/tavern_pack/`.

**Verdict.** Phase-0 architectural pattern reference. Half positive
(RNG discipline, scheduler-as-policy, framework-not-engine), half
negative (amnesia, no causal chain) — the negative half is the spec for
our event log.

### DF Legends XML · `REFERENCES.md` §1 + §10 · proprietary (export from own install) · bg-1..bg-4 (track B); schema shapes borrow for phase 0

**What it is.** Dwarf Fortress (proprietary) exports a world's history as
XML via the DFHack `exportlegends info` command. The XML contains
populations, sites, regions, figures, entities, artistic forms, structured
events, and nested `event_collections`. It is the **only irreplaceable
external resource** (`ROADMAP.md` §4): a ready canonical event log from a
real world generator. This entry covers the **export schema** half;
`ref-1` (§3 below) covers the worldgen + history layer half.

**Concrete mechanics.**

- **`historical_events`** — flat list of typed events, each with `id`
  (gap-free integer), `year`, `seconds72` (sub-year tick), and
  type-specific fields. Representative types: `hf_died` (`victim_hfid`,
  `slayer_hfid`, `cause` enum, `site_id`); `artifact_created`
  (`artifact_id`, `creator_hfid`, `site_id`); `hf_reputation_change`
  (`hfid`, `rep_hfid`, `reputation_type` enum, `strength` 1–100).
  `historical_event_collections` — nested many-to-many groupings (`id`,
  `type`, `event_ids`, `subcollection_ids`, role fields); types: `war`,
  `battle`, `duel`, `abduction`, `site_taken_over`, `beast_attack`,
  `journey`, `performed_structure`.
- **Causality is NOT a first-class field.** The "why" is reconstructed
  from role fields + `event_collections` grouping (a `war` collection
  groups `battle` collections, which group `hf_died` events). This is
  the **`TECH_NOTES.md` §3** finding: "Causality is reconstructed, not
  parsed — budget inference work, not parsing work."

**What we take.**

- **Event-with-id-and-tick schema shape.** DF: `id` + `year` +
  `seconds72`; ours: gap-free `event_id` + `tick` + `sub_order`
  (`EVENT_SCHEMA.md` §1). `event_collections` grouping precedent: our
  `cause` chain (`EVENT_SCHEMA.md` §2) is stricter (single-parent
  linear vs DF's many-to-many); a future phase may want collection-style
  multi-parent linking for arcs (P3c, `CORE_DESIGN_RESEARCH.md` §6).
  Population vs notables LOD is covered in §3 ref-1; figure-with-
  affiliation-history pattern (model for `LEGEND_SPEC` phase 4) is
  covered in §2 DF `historical_figures` bullet above.

**What we adapt.**

- **Causality from reconstructed → recorded** (P1a, INV-1): DF's
  causality is inferred from `event_collections` + role fields; our
  `cause` is first-class, recorded at event time. bg-2 will measure how
  much DF causality we can lift.
- **Macro-dense/micro-empty → micro-dense slice.** DF events are macro
  (wars, artifacts, births, deaths, abductions); our phase-0 events are
  micro (theft, arson, gossip, watch change). `TECH_NOTES.md` §3: the
  bg track validates briefer *mechanics*, not micro-event interestingness.
- **XML → JSONL** (D-002): the bg-1 pipeline parses XML → SQLite; we
  read rows from there. Our event log is never XML.

**What inspires us.**

- **"History without a player."** DF generates 1000 years before the
  player arrives; the PC walks into a live world. Our phase-0 tavern is
  the analog (seeded hooks in the director, `MVP_SCOPE.md` §11). The
  "history ticks abstractly" LOD principle and the epistemology schema
  (`hf_reputation_change` ↔ our `knowledge` records) are covered in
  §3 ref-1 — see there for the full mechanics.

**Strengths.**

- The only irreplaceable external resource (`ROADMAP.md` §4) — a
  ready canonical event log from a free install. Real-world precedent
  for every primitive we care about: events, figures, entities, sites,
  collections, reputations, affiliations. Structured XML — parseable,
  not a binary blob; schema documented in DFHack source.

**Weaknesses.**

- **Causality is reconstructed, not parsed** (`TECH_NOTES.md` §3) — bg-2
  budgets inference work, not parsing work. We lift the shape, not the
  chains.
- **Macro-dense, micro-empty** (`TECH_NOTES.md` §3) — DF has wars and
  artifact theft, not gossip and pickpocketing. DF's theft events are
  artifact-theft (a hammer stolen from a museum), not street theft.
- **Hundreds of MB per large world; translated-name layers to strip**
  (`TECH_NOTES.md` §3) — a 1000-year world is ~200MB XML; the parser
  must stream, not load DOM.
- **Proprietary.** We read exported data, never DF's code or assets
  (`REFERENCES.md` §10). DFHack is Zlib — pattern only.

**Verdict.** bg-1..bg-4 track. Phase-0 borrows schema shapes (event id
+ tick, role fields, population vs notables). Phase-4 (LEGEND_SPEC)
borrows its epistemology. Phase-5 (depth/worldgen) borrows its LOD
ladder. Nothing here gates phase 0.

## 3. ref-1 — DF worldgen + history layer (solo dive)

### DF worldgen + history layer · `REFERENCES.md` §1 + §10 · proprietary (read exported data only; never code or assets) · bg-1..bg-4 (track B); LOD ladder for phase 5

**What it is.** Dwarf Fortress generates 200–1000+ years of world history
before the player arrives. This entry covers the **worldgen + history
layer** — the other half of DF Legends XML vs the export schema half
(§2 above). Where the export schema entry covers the *format* of exported
history, this entry covers *how DF generates it*: history ticks,
populations vs notables LOD, age/civ dynamics, artifact anchors, reputation
as event.

**Concrete mechanics.**

- **History ticks abstractly.** DF worldgen advances year-by-year, not
  turn-by-turn. Each year: populations get statistical updates
  (births, deaths, migrations as counts); notable figures
  (`historical_figures`) get full event records; sites grow or shrink;
  civilizations expand, contract, go to war, found new sites.
- **Populations vs notables LOD** (central abstraction):
  `entity_populations` = aggregate counts per race per site
  (`{civ_id, race, count, site_ids}` — no individual records);
  `historical_figures` = full per-individual records (name, race, caste,
  birth_year, death_year, affiliation history, kills, reputation).
  Boundary is membership-based: a figure becomes "historical" when it
  does something worth recording. DF keeps ~1000–10000 historical
  figures per 1000-year world; populations are 10–100× larger but
  never simulated individually. Civilizations have lifespans (founding
  → expansion → conflict → decline); wars reduce defender counts
  without simulating each death — the LOD abstraction strikes again.
- **Reputation as event** (cleanest precedent):
  `hf_reputation_change`: `{hfid, rep_hfid, identity_id, region_index,
  reputation_type, strength}`. `entity_reputation_change`: same shape
  for an entity. `reputation_type` enum: "rumors of theft",
  "terrorized", "respected", "feared"… `strength` is 1–100. Reputation
  is **not stored as a state field** — it is the *stream* of these
  events. "Current reputation" = fold over `hf_reputation_change`
  events for a given `hfid` × `rep_hfid` pair.

**What we take.**

- **Populations vs notables LOD ladder** — the boundary (count → record)
  is the same shape as our P3d: ambient → statistical → full simulation.
  Our `npc_market_crowd_01` ambient entity (`MVP_SCOPE.md` §4.2) is the
  seed; DF proves the seed grows. Reputation-as-event (already borrowed
  in §2 export schema entry) — `hf_reputation_change` is the precedent
  for our `knowledge` records (MVP_SCOPE §10, EVENT_SCHEMA §3).

**What we adapt.**

- **Year-by-year tick → second-by-second tick.** DF worldgen advances
  years; our phase-0 tick is sub-minute (`MVP_SCOPE.md` §4.1: 1 tick =
  12 in-world minutes). Phase 5 will need a coarser macro-time tick
  layered over micro-time.
- **Macro-dense / micro-empty → micro-dense slice** (§2 export schema
  entry, `TECH_NOTES.md` §3) + **worldgen monolith → runtime + history**
  (DF runs once and ends; we need both simultaneously — the tavern is
  "live history" the moment the PC walks in). Pre-PC worldgen seeds
  the "running world" the PC arrives into (`MVP_SCOPE.md` §11 director
  hooks). Causality reconstructed → recorded (P1a, INV-1, §2 export
  schema entry) and no determinism contract across builds → INV-2 strict
  (`TECH_NOTES.md` §4) — cross-link, don't restate.

**What inspires us.**

- **"History without a player."** DF generates 1000 years before the
  player arrives; PC walks into a live world. Our phase-0 tavern is
  the analog: events have already been happening; the PC arrives at
  T=0 into a running world (seeded hooks in the director,
  `MVP_SCOPE.md` §11). DF is the proof-of-existence for the "running
  world" posture. Reputation is the *stream* of changes, not a
  number on an entity — aligns with INV-1 and D-007. The LOD
  discipline ("crowd is a count, guard is a record") is in
  "Concrete mechanics" above.

**Strengths.**

- The only existing implementation of "abstract history ticks at scale"
  (1000+ years) producing a usable canonical log.
- LOD discipline concretely demonstrated: populations vs notables is a
  working split with a 20-year track record.
- Reputation-as-event is the cleanest precedent for our `knowledge`
  records (cross-link §2 export schema entry).

**Weaknesses.**

- **Macro-dense, micro-empty** (§2 export schema entry, `TECH_NOTES.md`
  §3): wars and artifact-theft, not gossip and pickpocketing; bg track
  validates briefer *mechanics*, not micro-event interestingness.
- **Population LOD is "one tier"** (counts vs notables); our P3d proposes
  3 tiers (ambient → statistical → full). DF confirms the bottom 2;
  "ambient" tier is our addition (`MVP_SCOPE.md` §4.2).
- **DF worldgen has no "now"**: once play starts, worldgen ends; we need
  runtime + history simultaneously. DF is the negative precedent for
  "history runs only before play".
- **No determinism contract across builds** (`TECH_NOTES.md` §4) +
  **proprietary** (`REFERENCES.md` §10; DFHack is Zlib — pattern only).

**Verdict.** Phase-5 settlement cousin + phase-4 LEGEND_SPEC reference.
Confirms LOD ladder (P3d) and "history without a player"
(`MVP_SCOPE.md` §11). Schema shapes already borrowed in §2; worldgen
mechanics proper wait for phase 5. bg-1..bg-4 track parses the export;
nothing here gates phase 0.
