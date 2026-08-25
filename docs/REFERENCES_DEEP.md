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
MIT) — the closest existing cousin to canonsim's phase-5 settlement
vision: NPCs with relationships, jobs, personalities, and routines that
produce emergent narrative summaries.

**Concrete mechanics.**

- ECS-shaped core: an `Entity` is an integer id; components (`Position`,
  `Relationship`, `Occupation`, `Personality`, `Mood`, `Health`) are
  struct-bags keyed by entity id; systems (`TimeSystem`, `SocialSystem`,
  `RoutineSystem`, `NarrativeLogSystem`) tick on a daily cadence.
- `RelationshipTracker` is a **pair-keyed map**:
  `Dictionary<(int, int), Relationship>` where the key is a sorted tuple
  of entity ids and the value carries axes (trust, friendship, romance,
  familiarity) plus a per-axis weight used as a tiebreaker in social
  decisions.
- The social step: a `SocialSystem` iterates entities, asks
  `RelationshipTracker` for candidates (filter by proximity +
  relationship score above threshold), picks one, and emits a
  `SocialInteraction` record (enum: greet, argue, compliment,
  small-talk, …). The interaction updates the relationship axes per
  type-specific delta tables.
- Narrative is **post-hoc**: a `NarrativeLogSystem` runs at day's end,
  reads the day's `SocialInteraction` records, writes prose summaries.
  The narrative layer is a *reader* over state, not a participant.

**What we take.**

- The **pair-keyed relationship map** shape — `Dictionary<(int, int), …>`
  with a sorted tuple as canonical key. This is exactly P2a (D-020,
  `CORE_DESIGN_RESEARCH.md` §6): "sparse pair-keyed relation map" for
  NPC↔NPC relations in iter-3. Neighborly confirms the data structure.
- The "system-per-verb" decomposition — `SocialSystem`, `RoutineSystem`
  as separate ticked scopes. Our `sim/systems/` 8-system layout
  (`MVP_SCOPE.md` §5) is the same discipline; Neighborly proves "social"
  deserves its own system, not a method on `NPC`.

**What we adapt.**

- **State-mutating tick → event-emitting tick** (INV-1). Neighborly's
  `SocialSystem` mutates `RelationshipTracker` in place during the step;
  we emit a `rumor_heard` / `relation_changed` event into the queue, the
  writer flushes it to JSONL, and an incremental projection updates
  relations. The event is the truth; the projection is a cache
  (D-023, KI#5).
- **Post-hoc narrative → recorded log + template chronicle** (iter-5).
  Neighborly writes prose summaries at day's end and stores them as
  primary artifacts; we write events during the tick and let
  `render/` assemble the chronicle from the JSONL. Replay reconstructs
  what was *reported* vs what *happened* — Neighborly cannot.
- **Relationship matrix → relations-as-derived-state.** Neighborly
  stores `RelationshipTracker` as primary state; we derive relations
  from `relation_changed` events (fold over the log, `EVENT_SCHEMA.md`
  §1). INV-1 preserved; relations are a view, not a store.

**What inspires us.** The "settlement simulates itself without a player"
posture — confirms Kenshi's lesson (`CORE_DESIGN_RESEARCH.md` §3 row 4)
that the world must run for its own sake, not for the PC. Neighborly is
the proof-of-existence that agent goals + interactions produce emergent
narrative *at all* — we don't invent the genre, we harden its epistemology.

**Strengths.**

- Readable C# codebase, MIT-licensed — pattern transfer is direct.
- Solves the pair-keyed relations problem ahead of us; the data
  structure choice is validated.
- The system-per-verb decomposition matches our 8-system layout, so the
  architectural mapping is one-to-one.

**Weaknesses.**

- Weak epistemology (`CORE_DESIGN_RESEARCH.md` §2 row "Neighborly"):
  agents act but don't accumulate structured knowledge — no `known_by`,
  no fidelity, no rumor-distortion channel. This is the gap our
  `knowledge` records (MVP_SCOPE §10, EVENT_SCHEMA §3) are designed to
  fill; Neighborly confirms it is a real gap, not our invention.
- State-mutating tick — the Mesa anti-pattern (see below). Replay
  requires re-running; we cannot byte-compare a Neighborly run without
  recording every RNG draw externally.
- No causal chain — `SocialInteraction` records have no `cause`; the
  "why" lives in agent code, not the log. Our `cause` (EVENT_SCHEMA §2,
  P1a) is the missing ledger.
- Narrative is post-hoc summary, not a recorded log — summaries drift;
  replay cannot detect when the narrator lied.

**Verdict.** Phase-5 settlement cousin. Iter-3 P2a lifts its pair-keyed
map shape. Its epistemology gap is the spec for our knowledge records;
its amnesia is the spec for our event log. Read the repo at iter-3.

### Mesa · `REFERENCES.md` §2 · Apache-2.0 · phase 0 (architectural pattern)

**What it is.** Python agent-based modelling framework
(`projectmesa/mesa`, Apache-2.0) — the reference implementation of the
Model / Scheduler / Agent / DataCollector pattern, and the closest
language match to our stdlib-only core.

**Concrete mechanics.**

- `Model` class — holds `self.schedule`, `self.random` (a single
  `random.Random(seed)` instance — same discipline as our INV-2),
  `self.running` flag, `self.current_id` counter for gap-free agent ids,
  and a `DataCollector`. Subclasses implement `step(self)`.
- `Agent` base — `unique_id`, `model` backreference, `pos` (optional,
  for spatial models), `step(self)` (the agent's per-tick action).
- `Scheduler` subclasses are pure **ordering policies**:
  - `SimpleActivation` — insertion order.
  - `RandomActivation` — shuffled by `model.random` each tick.
  - `SimultaneousActivation` — two-phase: all agents `step()` into a
    staging buffer, then all commits.
  - `StagedActivation` — per-tick stage list (`["talk", "move", "eat"]`),
    all agents run stage 1, then all stage 2.
- `DataCollector` — `agent_reporters` and `model_reporters` dicts of
  `name → callable(agent|model)`; `collect(model)` runs every step and
  stores per-step frames; `get_model_vars_dataframe()` / `get_agent_vars_dataframe()`
  return pandas frames.
- The tick loop, in pseudo-code (from `mesa/model.py` + `scheduler.py`):

  ```python
  while model.running:
      model.step()                # user code: schedule.step() + bookkeeping
      schedule.step()             # for agent in order: agent.step(model)
      datacollector.collect(model)
  ```

**What we take.**

- **Single-RNG-instance discipline.** Mesa holds one `random.Random(seed)`
  on the Model and passes it everywhere an agent needs entropy. This is
  exactly our INV-2; Mesa is the Python reference that the pattern works.
- **Model / Scheduler / Agent vocabulary.** Our `core/` ≈ Model
  (clock + rng + queue + writer); our `heapq` queue keyed
  `(tick, sub_order, actor_id)` ≈ Scheduler (with a stricter ordering
  policy); our `sim/systems/*` ≈ per-system Agent.step() pieces.
- **DataCollector precedent.** Mesa's `agent_reporters` /
  `model_reporters` is the same idea as our M1–M5 metrics
  (`CORE_DESIGN_RESEARCH.md` §6 P1b–d, D-019): computed from the run,
  not by feel. We compute M1–M5 by folding the JSONL log, not by
  collecting at runtime — but the *notion* of "named, callable,
  replay-derived" metrics is Mesa's.

**What we adapt.**

- **`agent.step(model)` → event emission** (INV-1). Mesa's agent decides
  and acts in one call, mutating state directly. Our agent produces an
  `Intent` (or none); the queue decides ordering; the writer flushes;
  the projection applies. The Intent is the unit of decision; the Event
  is the unit of state-change; they are not the same object (this is
  the Spec-Talk boundary — see `MVP_SCOPE.md` §7, `EVENT_SCHEMA.md` §1).
- **Scheduler → heapq** (INV-2). Mesa's `RandomActivation` reshuffles
  every tick; we key the queue by `(tick, sub_order, actor_id)` so
  ordering is deterministic without per-tick reshuffling. Mesa's
  `SimultaneousActivation` two-phase step is on file — a future phase may
  want simultaneous-intent resolution; not phase 0.
- **`DataCollector` → log-derived metrics** (D-023). Mesa collects at
  runtime into per-step frames; we fold the JSONL log to compute M1–M5.
  Same output shape, opposite path; the DataCollector pattern is reserved
  for the T2 test path (and `balance-1` 1000-sim harness, TASKS infra).

**What inspires us.** The **framework-not-engine** posture: Mesa is a
library, not an executable — agents and models are user code; Mesa
provides the tick loop, RNG, scheduler, and collectors. This matches
our stdlib-only posture (D-012) — we are not a game, we are a
simulation core. The "scheduler = the policy" insight
(`SimultaneousActivation` vs `RandomActivation` vs `StagedActivation`)
is the same lesson as our queue key: ordering is the design lever.

**Strengths.**

- Same language as our core (Python) — pattern transfer is one-to-one.
- Apache-2.0, mature, widely taught; many reference models in-repo.
- Single-RNG-instance discipline is literally our INV-2 — Mesa proves it.

**Weaknesses.**

- **Pure ABM = episodic amnesia** (Mesa / Sims problem,
  `CORE_DESIGN_RESEARCH.md` §2 row "Mesa"). `step()` mutates state; no
  event log; replay = re-run, not fold. Our JSONL log + `state_changes`
  is the amnesia fix — the lesson ported from The Sims via Mesa.
- No causal chain — `agent.step()` is opaque; the "why" lives in agent
  code, not the framework. Our `cause` (P1a) records this at the event.
- No content/code split (INV-3) — Mesa has no opinion on domain data;
  that's our addition via `content/tavern_pack/`.
- No determinism-by-construction — Mesa's `RandomActivation` is
  deterministic *given the seed*, but the contract is "replay the same
  run", not "byte-compare two runs from the same seed + same Python
  version". Our INV-2 + T1 byte-identical test is stricter.

**Verdict.** Phase-0 architectural pattern reference. The closest
language-level precedent for our tick loop. Half positive (RNG
discipline, scheduler-as-policy, framework-not-engine), half negative
(amnesia, no causal chain) — the negative half is exactly the spec for
our event log.

### DF Legends XML · `REFERENCES.md` §1 + §10 · proprietary (export from own install) · bg-1..bg-4 (track B); schema shapes borrow for phase 0

**What it is.** Dwarf Fortress (proprietary) exports a world's history
as XML via the DFHack `exportlegends info` command. The XML contains
populations, sites, regions, figures, entities, artistic forms, structured
events, and nested `event_collections`. It is the **only irreplaceable
external resource** (`ROADMAP.md` §4): a ready canonical event log from a
real world generator. This entry covers the **export schema** half;
`ref-1` (above) will cover the worldgen + history layer half.

**Concrete mechanics.**

- Top-level XML elements (verified against DFHack docs, current DF
  Classic): `regions`, `underground_regions`, `sites`, `landmasses`,
  `mountain_peaks`, `rivers`, `creature_collections`, `historical_figures`,
  `entities`, `entity_populations`, `art_forms`, `dance_forms`,
  `musical_forms`, `poetic_forms`, `written_contents`, `historical_events`,
  `historical_event_collections`.
- **`historical_events`** — flat list of typed events, each with `id`
  (gap-free integer), `year`, `seconds72` (sub-year tick), and
  type-specific fields. Common types:
  - `hf_died` (figure died) — `victim_hfid`, `slayer_hfid`,
    `slayer_race`, `slayer_caste`, `cause` (enum: murdered, old age,
    shot, …), `site_id`.
  - `hf_attacked_site` — `attacker_civ_id`, `site_id`, `defender_civ_id`.
  - `artifact_created` — `artifact_id`, `creator_hfid`, `site_id`.
  - `created_site` / `destroyed_site` — `site_id`, `civ_id`, `builder_hfid`.
  - `hf_reputation_change` — `hfid`, `rep_hfid` (the figure whose
    reputation changed), `identity_id`, `region_index`, `reputation_type`
    (enum: rumors of theft, terrorized, …), `strength` (1–100).
  - `entity_reputation_change` — like the above but for an entity.
- **`historical_event_collections`** — nested groupings; each has `id`,
  `type`, `start_year`, `end_year`, `event_ids` (children), `subcollection_ids`
  (recursive children), and role fields (attacker, defender, winner, loser,
  killer, abductor). Types: `war`, `battle`, `duel`, `abduction`,
  `site_taken_over`, `beast_attack`, `journey`, `performed_structure` (a
  dance or music performance).
- **`historical_figures`** — entry per notable: `name` (with translated
  variant layers), `race`, `caste`, `birth_year`, `death_year`,
  `entity_id`, `site_link`, `ent_pop_id`, `reputation` (nested list of
  reputation entries), `honor`, `kills` list (figure ids), `affiliation`
  history (entity_id + role + start_year + end_year).
- **Causality is NOT a first-class field.** Events have participants,
  place, year; the "why" is reconstructed from role fields (killer,
  abductor, attacker) and from `event_collections` grouping (a `war`
  collection groups `battle` collections, which group `hf_died` events).
  This is the **TECH_NOTES.md §3** finding: "Causality is reconstructed,
  not parsed — budget inference work, not parsing work."

**What we take.**

- **Event-with-id-and-tick schema shape.** Every DF event has `id`
  (gap-free integer), `year`, `seconds72`. Our event schema
  (`EVENT_SCHEMA.md` §1) follows: gap-free `event_id`, `tick`,
  `sub_order` — same idea, deterministic naming, sub-tick precision.
- **`event_collections` as the precedent for grouping.** Our `cause`
  chain (`EVENT_SCHEMA.md` §2) does similar work in a stricter way:
  an event points at its parent via `cause` (single-parent linear
  chain). DF's collections are **many-to-many** (a battle belongs to a
  war AND can be referenced by a journey); our `cause` is single-parent.
  DF is more expressive here — a future phase may want collection-style
  multi-parent linking for arcs (P3c, `CORE_DESIGN_RESEARCH.md` §6).
- **Figure-with-affiliation-history pattern.** Our `entity` records
  (knowledge records, `known_by`, etc.) will need the same "track who
  was where when" structure for any non-trivial timeline. DF's
  `affiliation` history (entity_id + role + start + end) is the model
  for `LEGEND_SPEC` (phase 4).
- **Population vs notables LOD.** DF keeps `entity_populations` as
  aggregate counts and `historical_figures` as full records — exactly
  the LOD ladder (`CORE_DESIGN_RESEARCH.md` §2 row "DF worldgen", §6
  P3d). Our `npc_market_crowd_01` ambient entity (`MVP_SCOPE.md` §4.2)
  is the seed of this same ladder.

**What we adapt.**

- **Causality from reconstructed → recorded** (P1a, INV-1). DF's
  causality is inferred from `event_collections` + role fields; our
  `cause` is first-class, recorded at event time. bg-2 will measure
  how much DF causality we can lift into our `cause` chain.
- **Macro-dense/micro-empty → micro-dense slice.** DF events are macro
  (wars, artifacts, births, deaths, abductions); our phase-0 events
  are micro (theft, arson, gossip, watch change). `TECH_NOTES.md` §3:
  the bg track validates briefer mechanics, NOT micro-event
  interestingness — that stays on our own dry chronicle.
- **XML → JSONL** (D-002). DF speaks XML; we speak JSONL. The bg-1
  pipeline parses XML → SQLite; from there we read rows. Our event
  log is never XML.

**What inspires us.**

- **"History ticks abstractly."** DF worldgen advances the clock year by
  year; populations get statistics, notables get events — the LOD
  principle (`CORE_DESIGN_RESEARCH.md` §2 row "DF worldgen") confirmed
  at the source; our `entity LOD ladder` (P3d, phase 5) follows.
- **"History without a player."** DF generates 1000 years before the
  player arrives; the player walks into a live world. Our phase-0
  tavern is the analog: events have already been happening; the PC
  arrives at T=0 into a running world (seeded hooks in the director —
  `MVP_SCOPE.md` §11).
- **Epistemology schema.** DF's `hf_reputation_change` /
  `entity_reputation_change` are the closest precedent for our
  `knowledge records` (MVP_SCOPE §10, EVENT_SCHEMA §3). DF tracks
  who-reputed-what-where; we track who-knows-what-with-what-fidelity.
  Mapping: `rep_hfid` ↔ `known_by`, `reputation_type` ↔ `knows`
  token, `strength` ↔ `fidelity`.

**Strengths.**

- The only irreplaceable external resource (`ROADMAP.md` §4) — a ready
  canonical event log, exportable from a free install.
- Real-world precedent for every primitive we care about: events,
  figures, entities, sites, collections, reputations, affiliations.
- Structured XML — parseable, not a binary blob; schema documented in
  DFHack source.

**Weaknesses.**

- **Causality is reconstructed, not parsed** (`TECH_NOTES.md` §3) —
  bg-2 budgets inference work, not parsing work. We lift the shape,
  not the chains.
- **Macro-dense, micro-empty** (`TECH_NOTES.md` §3) — DF has wars and
  artifact theft, not gossip and pickpocketing. DF's theft events
  are artifact-theft (a hammer stolen from a museum), not street theft.
  This is why the bg track validates mechanics, not interestingness.
- **HEX errors after fortress play** (`TECH_NOTES.md` §3) — must export
  from a clean legends-mode save; the bug is on DFHack's side.
- **Hundreds of MB per large world; translated-name layers to strip**
  (`TECH_NOTES.md` §3). A 1000-year world is ~200MB XML; the parser must
  stream, not load DOM.
- **Proprietary.** We read exported data, never DF's code or assets
  (`REFERENCES.md` §10). DFHack is Zlib — pattern only; its parser is
  a reference, not a donor.

**Verdict.** bg-1..bg-4 track. Phase-0 borrows schema shapes (event
  id + tick, role fields, population vs notables). Phase-4 (LEGEND_SPEC)
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

## 4. ref-2 — C:DDA `data/json/` schema (solo dive)

### Cataclysm: Dark Days Ahead · `REFERENCES.md` §1 · CC-BY-SA 3.0 · phase 3 (content-pack reference)

**What it is.** Post-apocalyptic survival roguelike
(`CleverRaven/Cataclysm-DDA`, CC-BY-SA 3.0). The reference implementation
of "content-as-JSON at scale": ~111 top-level entries in `data/json/` (a
mix of standalone `.json` files and category subdirs), thousands of
objects, the engine a generic JSON interpreter. The closest existing
precedent for our `content/tavern_pack/` at phase 0 and the model for what
phase-3 content packs must scale to.

**Concrete mechanics.**

- **Top-level layout** (`data/json/` — 111 entries at the time of
  writing): a mix of standalone files (`materials.json`, `skills.json`,
  `traps.json`, `monster_factions.json`, `vitamin.json` …) and category
  subdirs (`items/`, `monsters/`, `recipes/`, `itemgroups/`, `npcs/`,
  `mutations/`, `overmap/`, `mapgen/`, `vehicles/`, `vehicleparts/`,
  `proficiencies/` …). `LOADING_ORDER.md` documents the discipline: a
  **breadth-first search** over the tree, so `data/json/X.json` is loaded
  before `data/json/subdir/X.json`. Dependency-respecting: skills load
  before professions, professions before scenarios.
- **Item schema** (`data/json/items/*.json`, `type: "ITEM"`): `id`
  (string, unique), `name` (object with `str` / `str_sp` / `str_pl` keys
  — localization-aware, no bare strings), `description` (same shape, with
  optional `"//~": "NO_I18N"` marker for non-translatable), `symbol`
  (single ASCII char) + `color` (named: `"white"`, `"red"`,
  `"dark_gray"` …), `material` (list of refs into `materials.json`),
  `weight` / `volume` (strings with units: `"350 g"`, `"467 ml"`,
  `"1 L"`), `price` (string: `"0 cent"`, `"150 USD"`), `stackable`
  (bool), `flags` (flat enum list: `PSEUDO`, `PERPETUAL`,
  `WATER_PROOF` … — no inheritance tree, appendable, no schema break on
  adding new flags).
- **Monster schema** (`data/json/monsters/*.json`, `type: "MONSTER"`):
  `abstract` (string — for inheritance; abstract monsters don't spawn,
  others `copy-from` them), `name`/`description` (localization-aware
  objects), `default_faction` (ref into `monster_factions.json`),
  `categories` (`WILDLIFE` etc.) and `species` (`BIRD`, `FISH` …) — two
  orthogonal classification axes, `volume`/`weight`/`hp`/`speed` (units
  or ints), `aggression` (signed int; `-99` = docile, `+99` =
  immediately hostile), `morale` (signed — flees below threshold),
  `melee_dice` + `melee_dice_sides` + `melee_damage` (list of
  `{damage_type, amount}`), `dodge`, `material` (drop-table reference),
  `harvest` (id into `harvest.json`), `weakpoint_sets` (anatomy), and
  `families` (proficiency references — what the player learns from
  dissecting the monster).
- **Recipe schema** (`data/json/recipes/*.json`, `type: "recipe"`):
  `result` (item id produced), `activity_level` (enum: `LIGHT_EXERCISE`,
  `MODERATE_EXERCISE` … — feeds the player fitness system),
  `category` + `subcategory` (`CC_*` / `CSC_*_NESTED` — hierarchical),
  `skill_used` + `difficulty` (skill id + int level), `skills_required`
  (paired list `[[skill_id, level], …]`), `time` (string with units:
  `"25 m"`, `"2 h"`), `reversible` (bool — can be deconstructed),
  `decomp_learn` (skill level granted on deconstruction — bonus learning
  from disassembly), `book_learn` (paired `[[book_id, level_required],
  …]` — recipe gated by a book the player has read), `using` (paired
  `[["tool_qualities_id", charge_count], …]` — tool charge costs),
  `qualities` (list of `{id, level}` — tool qualities required, e.g.
  `{id: "SCREW", level: 1}`), `components` (list of alternatives —
  paired lists, each `[item_id, count]`, alternatives = any-of).
- **Itemgroup schema** (`data/json/itemgroups/*.json`, `type:
  "item_group"`): `subtype` (`"collection"` = spawn-all |
  `"distribution"` = pick-N), `entries` (list of `{item, count, prob,
  variant}`), `prob` is `0–100`, `count` is a range `[min, max]`.
  **Nested `collection` entries** for "one of these sets" — a sub-list
  inside an entry. This is the abstraction for loot tables / tavern
  inventory / NPC starting gear.
- **Mission schema** (`data/json/npcs/missiondef.json`, `type:
  "mission_definition"`): `id`, `name`, `goal` (enum: `MGOAL_GO_TO_TYPE`,
  `MGOAL_CONDITION`, `MGOAL_FIND_ITEM`, `MGOAL_KILL_NPC` …),
  `goal_condition` (JSON-predicate like `{u_has_item: "inhaler"}` —
  evaluated against the player's state), `difficulty` (int), `value`
  (reward in cents), `urgent` (bool), `start` (object with an `effect`
  array and an `assign_mission_target` shape — what happens when the
  mission is issued), `origins` (enum list: `ORIGIN_SECONDARY`,
  `ORIGIN_OPENER_NPC`, `ORIGIN_ANY_NPC` — who can offer it), `deadline`
  (string pair like `["2 days", "3 days"]` — duration range sampled at
  issue time), `dialogue` (object with `describe` / `offer` / `accepted`
  / `rejected` / `advice` / `inquire` / `success` / `success_lie` /
  `failure` — full conversation template inline).
- **NPC faction schema** (`data/json/npcs/factions.json`, `type:
  "faction"`): `id`, `name`, `likes_u`/`respects_u` (signed int — same
  shape as our `relations` map axes), `known_by_u` (bool), `size` /
  `power` (numerical attributes — `power` is the faction's effective
  strength), `consumes_food` / `wealth` (economy flags), `relations`
  (nested map keyed by **other-faction-id**, with booleans: `kill on
  sight`, `watch your back`, `share my stuff`, `guard your stuff`, `lets
  you in`, `defends your space`, `knows your voice` — pair-keyed with
  boolean attributes), `mon_faction` (ref into
  `monster_factions.json`), `epilogues` (state-gated epilogue blocks
  with `power_min` / `power_max` thresholds and `dynamic` cross-faction
  predicates — the precedent for our director triggers in phase 3).
- **Monster faction schema** (`data/json/monster_factions.json`, `type:
  "MONSTER_FACTION"`): `name`, `base_faction` (inheritance — attitude
  chain), `friendly` / `neutral` / `hostile` (lists of faction names),
  `by_mood` (mood-dependent override — faction attitude changes with
  monster mood). **Pair-keyed map** of monster-vs-monster relations —
  same shape as NPC factions and as Neighborly's `RelationshipTracker`
  (§2).
- **Inline author commentary convention**: every C:DDA JSON file uses
  `"//": "..."` (and `"//2": "..."`, `"//~": "NO_I18N"` as a
  non-translatable marker) as inline documentation for humans. Our
  `content/tavern_pack/` uses `"_"` for the same job — minor cosmetic
  divergence, same pattern.

**What we take.**

- The **per-category file split** (items/ split into `ammo/`, `armor/`,
  `gun/` …) — scales to thousands of objects without merge conflicts.
  Our `content/tavern_pack/` already does this (`entities.json`,
  `actions.json`, `rules.json`, `templates.json`); C:DDA proves the
  discipline scales to ~111 categories.
- The **string-with-units convention** (`"350 g"`, `"25 m"`,
  `"0 cent"`) — human-readable, parseable, no magic numbers. Validates
  the content/code split (INV-3) at scale: ~111 files, thousands of
  objects, zero domain words in engine code.
- The **`abstract` + `copy-from` inheritance** for monsters — base
  archetypes that don't spawn but are referenced. C:DDA proves the
  pattern works for content with hundreds of variants of the same
  archetype (e.g. `mon_bird_flying_base` → many specific bird
  species). Useful precedent if `content/tavern_pack/` grows NPC
  archetypes in a later phase.
- The **`relations` map shape** in `factions.json` — pair-keyed by
  other-faction-id with boolean attributes (`kill on sight`, `watch
  your back`, `share my stuff` …). This is **exactly the same shape** as
  Neighborly's pair-keyed `RelationshipTracker` (§2 above) and aligns
  with our P2a (D-020) sparse pair-keyed relation map for iter-3. C:DDA
  is the second independent validation of the data structure.
- The **`subtype: "collection" | "distribution"`** abstraction for
  itemgroups — exactly the loot-table / tavern-inventory primitive we
  need for `content/tavern_pack/` placement and starter inventory.
  Nested `collection` entries (one-of-these-sets) are non-trivial and
  on file.
- The **`//` field as inline author commentary** — `//`, `//2`, `//~`
  markers in every JSON file. Our pack uses `"_"` (per
  `content/tavern_pack/`); the convention is identical, the field name
  differs.

**What we adapt.**

- **Inline `dialogue` block → separate `templates.json`**: C:DDA
  inlines the full conversation (`describe`/`offer`/`accepted`/
  `rejected`/`advice`/`inquire`/`success`/`success_lie`/`failure`) in the
  `mission_definition` object — `missiondef.json` is 55k+ lines;
  cross-referencing by id impossible; localization is bolted on via
  `//~` markers. For phase 0 we keep templates in
  `content/tavern_pack/templates.json` and reference by id; for phase 1
  the LLM-renderer generates from the event log directly (canon/voice
  split, `VISION.md` §1).
- **Deadline as duration pair → event-time computation**: C:DDA's
  `deadline: ["2 days", "3 days"]` is a duration range sampled at
  mission-issue. We compute deadline as `issue_tick +
  sampled_duration` (INV-2: sampled via the seeded `random.Random(seed)`
  instance), store as event field, never as wall-clock (D-004,
  `TECH_NOTES.md` §4).
- **String-with-units everywhere → pack data only, not code**: C:DDA
  parses strings like `"350 g"` at load time. For phase 0 we keep
  numbers as JSON numbers (grams, milliliters, ticks), not strings; the
  renderer formats them at output. C:DDA's convention is content-author
  convenience; ours is determinism (no parse-step ambiguity, no unit
  drift across builds — `TECH_NOTES.md` §4).
- **BFS-tree load order → `sorted()` discipline**: C:DDA's BFS-tree
  load discipline is required because of `abstract` + `copy-from`
  inheritance (base monster must exist before child) and cross-file
  references. Our load order is `sorted()` per INV-2 — pack files have no
  inheritance, only references, and references are name-based
  (resolve-after-load). Simpler discipline, same outcome.
- **CC-BY-SA license → lift patterns, not text**: CC-BY-SA is viral —
  if we lift text wholesale, our pack must also be CC-BY-SA. We lift the
  schema *shapes* (the abstractions are general), not the prose, not
  the enum values, not the field names tied to C:DDA's vocabulary. Per
  §0.7 of `REFERENCES.md` and D-015.

**What inspires us.** The **"content as data, code as engine"** posture
at scale. C:DDA is the existence proof that an entire game can be
authored as JSON content with the engine as a generic interpreter — 111
top-level data files, thousands of objects, zero code changes for new
content. Our `content/tavern_pack/` is a phase-0 micro-version of the same
discipline; C:DDA proves it grows.

**Strengths.**

- The reference implementation of content-as-JSON at scale. 111
  top-level entries, thousands of objects, CC-BY-SA, mature (15+ years
  of public development).
- Per-category file split (items/ split into `ammo/`, `armor/`, `gun/`
  etc.) — scales to thousands of objects without merge conflicts.
- String-with-units convention — every quantity carries its unit, no
  magic numbers, no "what does 350 mean?" hunting.
- The `abstract` + `copy-from` inheritance pattern for monsters — base
  archetypes that don't spawn but are referenced.
- The `relations` map shape in `factions.json` — pair-keyed with
  boolean attributes. Same shape as our P2a (D-020) sparse pair-keyed
  relation map; second independent validation after Neighborly (§2).
- The `epilogues` block — state-gated, with `power_min`/`power_max`
  thresholds and `dynamic` cross-faction predicates. Direct precedent
  for our director triggers in phase 3 (D-005 consequence planner).
- The `//` field as inline author commentary — documentation lives next
  to the data, not in a separate README.

**Weaknesses.**

- **No event log / no event sourcing** (`CORE_DESIGN_RESEARCH.md` §2
  row "C:DDA"): C:DDA is state-mutating at runtime; the save file is a
  snapshot, not a fold-replayable log. Same amnesia as Mesa (§2). Our
  JSONL log + `state_changes` (INV-1) is the fix.
- **Inline `dialogue` blocks bloat mission definitions**: the full
  conversation template is inlined in the `mission_definition` object —
  `missiondef.json` is 55k+ lines; cross-referencing by id impossible;
  localization is bolted on via `//~` markers. We split templates from
  definitions (MVP_SCOPE §9, `templates.json`).
- **No causal chain**: missions reference `goal` (an enum) and
  `goal_condition` (a JSON-predicate), but there is no `cause` field —
  the "why did this mission get offered now" lives in the engine C++
  code, not the data. Our `cause` (`EVENT_SCHEMA.md` §2, P1a) is the
  missing ledger.
- **CC-BY-SA viral** — if we lift text, we inherit the license. We lift
  patterns only (D-015, `REFERENCES.md` §0.7); the license rule forces
  the "patterns not content" stance rather than treating it as optional.
- **No determinism contract** — engine uses wall-clock for many
  systems; save files are not byte-reproducible across builds. Our
  INV-2 is the discipline C:DDA lacks; we cannot lift C:DDA's runtime
  patterns, only its data-shape patterns.

**Verdict.** Phase-3 content-pack reference. The proof-of-existence that
the content/code split (INV-3) scales to thousands of objects across ~111
category files. We lift patterns (schema shapes, per-category file split,
string-with-units convention, `abstract`+inherit, pair-keyed `relations`
map, state-gated `epilogues`) — never text, never enum values, never
field names tied to C:DDA's vocabulary. CC-BY-SA forces the "patterns not
content" rule. Read the repo at iter-2 / iter-3 (when actions and the
content loader land). Nothing here gates phase 0.
