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
| ref-1 | DF worldgen + history layer (the half not covered here) | solo | 5+ subsystems: history ticks, populations vs notables LOD, age/civ dynamics, artifact anchors, reputation as event |
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
