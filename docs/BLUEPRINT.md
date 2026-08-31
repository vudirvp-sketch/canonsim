# BLUEPRINT.md — The Reference Distillation: Resolved Combinations for the Build

> The applied-synthesis layer of the reference system: where the deep dives
> (`docs/ref/`, indexed by `docs/REFERENCES_DEEP.md` §2 — 33 files at
> iter-0u) stop being a library and become a construction plan.
> **Organized by what we build, not by
> source.** This file owns the RESOLUTIONS and COMBINATIONS (new facts,
> created by cross-referencing); every mechanic cited stays owned by its
> per-ref file — linked, never restated. Anti-drift map extended to a fourth
> place: catalog (`REFERENCES.md`) ↔ one-line synthesis
> (`CORE_DESIGN_RESEARCH.md` §2) ↔ deep dives (`docs/ref/`) ↔ **this
> blueprint** (`BLUEPRINT.md` + `docs/blueprint/`).
>
> Law hierarchy is unchanged: `AGENTS.md` §4 invariants beat every donor
> pattern. Where a donor and an invariant conflict, the invariant wins and
> the ledger below records the workaround — that is the entire point of this
> file. Born iter-0u (owner-requested synthesis pass, 2026-08-27).

## 0. Method (how the corpus was digested — and how future refs enter)

The corpus at iter-0u: 33 per-ref deep dives (~10k lines) + the core docs;
grown to 35: the atlas (ref-16, iter-8a — the scene-ledger pattern
source; its donor line is on BRIEF-1 below) and the DF designed-
experience dive (ref-17, iter-8d). The live count's owner:
`docs/REFERENCES_DEEP.md` §2.
Digestion was one full read pass, then a per-component extraction:

1. **Component slice.** For every buildable component (iter-1 plumbing →
   phase-6 packs) collect each ref's verdict rows ("what we take / adapt /
   reject") that target it. The per-ref files are already structured for
   this — no re-reading of sources needed.
2. **Tension detection.** Where two donors disagree (MTTH vs determinism;
   player-stress pacing vs player-blind canon; mutable ECS storage vs
   INV-1), the disagreement is made explicit instead of averaged away.
3. **Resolution.** Each tension resolves into one mechanism that keeps the
   invariant whole and takes the donor's shape — the "workaround" is a
   restatement of the mechanism at the invariant's side of the border.
4. **Sequencing.** Resolutions land in the iteration/phase that first needs
   them; earlier phases never depend on later-phase machinery.

**Maintenance protocol** (a new reference enters the same way): deep dive
lands in `docs/ref/` → its verdicts touch at most a few ledger rows below →
the affected `docs/blueprint/` sections gain a donor-chain line. A new ref
that changes a *resolution* (not just adds a donor) is a rare event — it
requires a worklog note and, if it breaks a prior combination, a
`docs/DECISIONS.md` entry superseding the old one. The blueprint is
maintained **at deep-dive time**, never "later".

**What this file is NOT:** not a spec (specs are born just-in-time from
experiments — `SPECS_BACKLOG.md` owns trigger-gated sketches); not a
restatement of `MVP_SCOPE.md` (the phase-0 contract) or `EVENT_SCHEMA.md`
(the event contract). The blueprint is the layer **between** references and
specs: when a spec is written, it draws its donor decisions from here.

## 1. The resolution ledger (twelve tensions, twelve mechanisms)

| ID | Tension (donor A vs donor B) | Resolution — the one mechanism we build | Lands |
|---|---|---|---|
| RNG-1 | INV-2 "one `random.Random(seed)` instance" (pre-D-028 wording) vs Brogue two-stream / DCSS N-stream discipline | **RngBank**: a single authority in `core/rng.py` holding named streams, each deterministically derived from the master seed: `stream(name) = random.Random(stable_hash(f"{seed}:{name}"))` where `stable_hash(s) = int.from_bytes(hashlib.sha256(s.encode()).digest()[:8], "big")` — sha256-based, environment-independent (stream derivation never relies on `PYTHONHASHSEED`; INV-2 now carries this wording, D-028). `substantive` = canon stream; `cosmetic` = render-only. Cosmetic rolls can never desync canon replay; `audit()` scope guard (DCSS `ASSERT_stable`); draw counter on substantive = replay fingerprint for T1. **Substantive-by-definition lint rule:** any draw whose value lands in an event's `outcome`/`state_changes`/`knowledge` is substantive; canon-emitting paths run under `assure('substantive')`, render paths under `assure('cosmetic')` — a wrong-stream draw is loud, not silent | iter-1 |
| TIME-1 | Paradox MTTH (wall-clock + per-scope RNG) vs KeeperRL per-tick rolls vs Endless Sky condition-availability vs D-005 consequence seeding | **Three tick-anchored timing primitives, nothing else**: SCHEDULED (completion entries enqueued at commit), SEEDED (hooks + triggers recorded at event time — the only source of new complications), SAMPLED (per-tick probability derived from pack `expected_interval_ticks`, rolled by the keyed stream). MTTH is the named anti-pattern; every event grammar rides on top as pack data | iter-1/2, formalized iter-4 |
| STATE-1 | Every game donor mutates state in place (Mesa, C:DDA, RimWorld, entt, Bevy) vs INV-1 `state = fold(log)` | **The projection IS the storage**: entt's sparse+packed layout becomes the layout of the *incremental* projection (D-023); queries are views (smallest-pool-leads); Bevy's double-buffered messages become the tick boundary (log append → projection apply); entt's `sigh` signals become fold handlers. Writes go only through log append — ECS ergonomics without ECS mutation | iter-1/2 |
| SCHED-1 | rot.js min-heap vs KeeperRL `map`-queue + players/nonPlayers deques vs DCSS energy scheduler | **One `heapq`, key `(tick, sub_order, actor_id)`** with a monotonic `seq` as final tiebreak; `sub_order` bands: system passes (fixed order) < player intents < NPC reactions < scheduled completions. Energy model (DCSS `speed_increment`) is deferred until actors have speeds — phase 0 tick is time, not energy. KeeperRL's fixed per-tick subsystem order is enforced, not hoped: systems declare `reads`/`writes` as data, a build-time DAG orders them, ambiguity check (entt organizer + Bevy `ambiguous_with`) fails loudly on conflicts | iter-1, DAG at iter-2 |
| EPIST-1 | Private numeric states (system 5: fatigue/intoxication/fear) vs knowledge-driven behavior (blind-NPC law) | **Influence Boundary** (live-char-guide, adopted): behavior functions read own state + own knowledge only; other entities' internals enter exclusively via perception of observable markers. Embodiment = the states→observables mapping, pack data. Expectation mismatch (P2d) emits `inferred` records — the only legal route to suspicion-from-absence. **Price**: every socially meaningful action carries same-scene observable markers alongside its deferred hooks | iter-2 (price), iter-3 (full) |
| DIR-1 | L4D "measure the player's stress" vs Alien "Director learns the player" vs player-blind canon (`VISION.md` §6) | The director reads **the world's observable surface only**: entropy = seeded-hook weights + global suspicion + visible threats. Pacing clock RAMP/PEAK/REST/STAGNATION with two cooldown clocks and a release budget of 1 per beat; **objective broadcast** — the director enqueues an Intent for an NPC (Alien's directive), never mutates actors directly. Named negatives, each with its donor: from-nothing threats (Randy), player-pattern adaptation (Alien), canon softening (L4D health bias) | iter-4 |
| BRIEF-1 | Generative Agents retrieval vs letta block manager vs D-018 sensory-delta brief vs live-char voice isolation vs lorebook injection vs the atlas texture-lifecycle patterns (trust states, tombstone, scope-as-key — ref-16) | **The block pipeline**: typed blocks with hard token budgets — [directives] [scene delta (sensory emitters, O(perception))] [recalled facts] [scheduled static lore] [voice exemplars near the context end] [active options]; the deferred 7th block `scene_texture` reads the session scene ledger (D-048/D-049 — `phases.md` §1, the canon-vs-texture resolution). Retrieval split: dynamic facts = `known_by` + tick window + event weight (**never vector search** — `VISION.md` §5); static lore = FTS5 keyword first, sqlite-vec optional. Injection scheduling grammar: depth / probability / cooldown / sticky / range-cascade | phase 1 |
| PACK-1 | C:DDA 111-category scale vs phase-0 "no pack system" non-goal vs Wesnoth no-schema pain | **The pack ladder**: phase 0 = fixed directory, 4 JSON files, JSON-Schema-validated, closed enums on every record, `"_"` commentary fields; growth rungs pre-placed — per-category split, `abstract`+`copy-from` inheritance, append-not-overwrite composition, and lint (UAP teleology gate + live-char AP crosswalk) as the phase-6 CI. A pack format without schema validation is the named Wesnoth anti-pattern — never taken | iter-1 (loader), phase 6 (system) |
| CHRON-1 | Canon events vs prose: tracery unseeded RNG / ink snapshot state vs byte-identical chronicle | **Event vs tale split** (RimWorld `TaleDef`): the chronicle entry is a derived, prose-ready record; importance gates what surfaces; per-cause-chain pruning bounds the window. Templates = tracery grammar (JSON symbol table, nested expansion, modifiers, save/restore stack) with **every pick from the cosmetic stream or `sorted()` order** — same grammar, deterministic engine, ~200 lines of stdlib | iter-5 |
| STORE-1 | Log-is-truth vs query speed vs semantic search vs analytics | **The storage ladder**, each rung rebuildable, none authoritative: JSONL log (truth) → SQLite incremental projection (runtime; checkpoint = `MAX(event_seq)`) → FTS5 index (phase-4 keyword; `rebuild` = the INV-1 mechanism) → sqlite-vec (static-lore vectors, conditionally loaded, pure-Python cosine fallback) → DuckDB chronicler + parquet (offline only, never in the runtime import graph). Compaction is offline scavenge with tombstones — corrections are always new events | iter-1 → phase 4 |
| TEST-1 | Per-donor test lore: Brogue seed catalogs, DCSS RNG audits, UAP rubrics, live-char one-change rule | **The verification stack**: T0–T8 core suite; T1 strengthened with the RNG fingerprint and known-good seed catalogs; `ASSERT_stable` guards in tests; single-factor A/B (one change per run) for every comparison; the UAP 7-hole taxonomy as a test-design crosswalk; golden-set comparison for the chronicler. Metrics M1–M5 computed from the log only — never by feel, never LLM-judged | iter-1 → iter-6 |
| LOD-1 | DF "macro-dense, micro-empty" vs our micro-dense slice; DF one-tier populations vs full simulation everywhere | **The LOD ladder**, coherent across scales (`natural_earth.md` "multiple LODs of the same data should be coherent"): canon log = ground truth; per-NPC projection = mid LOD; brief cache = top LOD; phase-5 worldgen adds populations-vs-notables below and ambient crowd above. Worldgen = ordered focused passes over the seed (Azgaar pipeline); history ticks abstractly before the PC arrives — the running world the PC walks into. bg-2 (D-063) measured: DF history is canon-dense, epistemology-empty — no witness/knowledge events in the exports (`docs/TAXONOMY.md` §4); DF donates the legends structure, never the knowing side | phase 4–5 (crowd seed now) |

## 2. The cross-cutting laws (the constitution, distilled)

Each law is the fusion of several donors into one sentence a reviewer can
check a diff against. Invariants (INV-1..5) outrank these; the laws
operationalize the invariants.

- **L1 Observability.** Every element — event, pack rule, trait, hook —
  must produce an observable action or be cut. Three independent
  convergences: causal-density checklist (`MVP_SCOPE.md` §15), UAP §0.6
  count-based screening, live-char "every element must produce an
  observable action". Dead data is a lint error, not a style choice.
- **L2 Canon/voice split.** Facts travel as structured tokens; voice lives
  in templates and exemplars. The brief never *describes* style; the
  chronicle never embellishes canon (`VISION.md` §1; live-char voice
  isolation; Paradox payload-vs-presentation separation).
- **L3 Derive, never store.** State, relations, `known_by`, traits,
  chronicle tales — all folds over the log. Anything stored twice will
  drift; anything derived can be rebuilt, diffed, and trusted
  (`EVENT_SCHEMA.md` §1; Neighborly/letta inversions; P3f).
- **L4 Single time authority.** One integer tick; no wall-clock anywhere,
  log header included. All timing reduces to SCHEDULED / SEEDED / SAMPLED
  (TIME-1). Any new mechanism that wants "later" must express it as one of
  the three.
- **L5 Single randomness authority.** All entropy flows through the
  RngBank; a roll outside it is a bug (RNG-1). The draw count is a
  fingerprint, and fingerprints are compared in tests.
- **L6 Player-blind canon.** NPCs and the director read observables, never
  player internals or player history (DIR-1, EPIST-1). Adaptation to the
  player is prose-layer only (phase-1+ narrator may tune style; canon
  never).
- **L7 Causality is recorded, not reconstructed.** `cause` on every event
  at write time (P1a); DF's reconstructed causality is the named
  anti-pattern. M3 measures the chain; UAP's why-chain audit validates the
  approach from the prose side.
- **L8 Consequence pairing.** Immediate Price (same-scene observable
  markers) + deferred hooks (D-005 buffer). An action with neither is dead
  by L1; an action with only deferred consequence is socially invisible;
  with only immediate, it has no arc.
- **L9 Small alphabet, deep composition.** Depth = O(intersections between
  primitives), not O(content). The intersection matrix
  (`MVP_SCOPE.md` §6) is a first-class artifact; Brogue's five
  environmental rules and Azgaar's pass pipeline are the existence proofs.
  Adding a primitive must add intersections or it is not added.
- **L10 Validated content, not parsed content.** Pack data is JSON +
  JSON-Schema + lint; no string expression languages in packs (INV-3 — an
  evaluator with domain words would live in code). Wesnoth's no-schema
  pain and Paradox's implicit-scope footguns are the named anti-patterns.
- **L11 Everything rebuildable.** SQLite, projections, briefs, chronicles,
  legends: all derived, all droppable. Offline compaction (scavenge)
  never edits committed logs (INV-5).
- **L12 Degradation ladders, never hard dependencies.** LLM → template →
  dry log line; vec → pure-Python cosine; DuckDB → sqlite aggregates. The
  canon path has zero optional dependencies; optionality lives at the
  edges (render, retrieval, analytics).
- **L13 Abstraction cost gate.** An abstraction must name the future change
  it makes cheaper before it enters the diff — no answer means speculative
  complexity (D-031). Rule-of-Three tiers: adapters abstract on demand;
  kernel↔periphery seams are ports from day one (`RngBank`, the log
  writer); helpers extract on the third duplicate, not the first; one
  discriminator with 4+ branches becomes a name→handler registry
  (`docs/blueprint/phase0.md` §2 ActionResolver).
- **L14 Elegance standard.** A solution is accepted when it makes the
  problem look obvious in retrospect; a complex one carries its
  justification in the diff (D-031). Review checklist: fewer moving parts
  than before · one rule instead of N exceptions · parts compose freely ·
  stdlib-only · reads as pseudo-code · the next change is local · same seed
  → same log.

## 3. Build index (what to read before each iteration)

| Before building | Read | Ledger rows in play |
|---|---|---|
| iter-1 core plumbing | `docs/blueprint/phase0.md` §1 + `MVP_SCOPE.md` §8 + `EVENT_SCHEMA.md` §1 | RNG-1, SCHED-1, STATE-1, STORE-1, TEST-1 |
| iter-2 actions | `docs/blueprint/phase0.md` §2 + `MVP_SCOPE.md` §7 | TIME-1, EPIST-1 (price), PACK-1, STATE-1 |
| iter-3 knowledge/relations | `docs/blueprint/phase0.md` §3 + `MVP_SCOPE.md` §10 | EPIST-1, LOD-1 (crowd), STATE-1 |
| iter-4 director + goals | `docs/blueprint/phase0.md` §4 + `SPECS_BACKLOG.md` DIRECTOR_SPEC sketch | DIR-1, TIME-1, LOD-1 |
| iter-5 chronicle & CLI | `docs/blueprint/phase0.md` §5 + `MVP_SCOPE.md` §12 | CHRON-1, RNG-1 (cosmetic stream) |
| iter-6 gate | `docs/blueprint/phase0.md` §6 + `MVP_SCOPE.md` §15–16 + `ROADMAP.md` §5 | TEST-1 |
| phase 1 mediator | `docs/blueprint/phases.md` §1 + `SPECS_BACKLOG.md` BRIEF/VALIDATION sketches | BRIEF-1, TEST-1 |
| phase 2 parser (OPEN) | `docs/blueprint/phases.md` §2 + `docs/PARSER_SPEC.md` (the written contract) | BRIEF-1, L2 |
| phase 3 director evolution + grammar | `docs/blueprint/phases.md` §3 | TIME-1, DIR-1, EPIST-1 |
| phase 4 memory/retrieval | `docs/blueprint/phases.md` §4 | STORE-1, BRIEF-1, LOD-1, L3 |
| phase 5 worldgen/depth | `docs/blueprint/phases.md` §5 | LOD-1, TIME-1, L9 |
| phase 6 packs/CI | `docs/blueprint/phases.md` §6 | PACK-1, L1, L10 |

File caps: `BLUEPRINT.md` and each `docs/blueprint/*.md` ≤600 lines
(`AGENTS.md` §6, substance filter §6.1). This index is the only place the
ledger is restated at length; everywhere else, cite the row ID
(e.g. "per RNG-1") — one-line summaries and links only (D-024 discipline).

---

← Part files: [`docs/blueprint/phase0.md`](blueprint/phase0.md) (iter-1..6)
· [`docs/blueprint/phases.md`](blueprint/phases.md) (phases 1–6).
Up: [`README.md`](../README.md) · index of sources:
[`docs/REFERENCES_DEEP.md`](REFERENCES_DEEP.md).
