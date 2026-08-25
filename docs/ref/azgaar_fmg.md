# Azgaar Fantasy-Map-Generator · `REFERENCES.md` §2 + §14 · MIT · phase 5 (worldgen donors)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is open MIT — code and the
> `.map` save format both. Reading and porting the architecture is
> permitted per §0.4; copying the JS/TS implementation is not useful
> — our runtime is Python stdlib (D-012), and Azgaar's generators are
> tightly coupled to d3 + Voronoi + SVG/WebGL rendering; we lift the
> **architecture** (data/generators/editors/renderers split + the
> ordered-generator pipeline + the chronology-as-diplomacy-history
> shape) into our `content/packs/` + `core/` plumbing + `sim/systems/`,
> never the rendering. Reference repo:
> `Azgaar/Fantasy-Map-Generator` (the
> `azgaar.github.io/Fantasy-Map-Generator` web app). Catalog §2 row
> reads "states, cultures, religions, chronology generator"; the
> chronology lives in `states-generator.ts` as `generateCampaigns` +
> `generateDiplomacy` (no separate `chronology-generator.ts` file)
> — minor catalog↔repo drift, fixed in this per-ref file, not in
> the catalog (the catalog row is the short version; this file is
> the long one).

**What it is.** Azgaar's _Fantasy Map Generator_ is a free
web application that procedurally generates editable fantasy maps
(coastlines, biomes, rivers, states, cultures, religions, cities,
provinces, military, trade routes, markers, labels) from a single
integer seed. The map is editable: the user can draw coastline
overrides, rename states, promote/split cultures, regenerate
religions, edit burg names, etc. — the generator pipeline is
_re-entrant_, not a one-shot. A `.map` save file is JSON; the seed is
the canonical reproducibility handle. MIT-licensed, JS/TS, currently
transitioning from vanilla JS to TypeScript. The generator pipeline
and the editor layer are the precedent for our phase-5 worldgen
donor + iter-1 `core/` plumbing shape (ordered pipeline + seed +
re-entrant edits on top of an append-only event log).

**Concrete mechanics.**

- **Architecture: four-layer split.** The README
  (`README.md` §"Contribution") states the future architecture
  explicitly: a separation between **world data** (state),
  **procedural generation** (model), **interactive editing**
  (controllers), and **rendering** (view). Flow:
  `settings → generators → world data → renderer`;
  `UI → editors → world data → renderer`. The data layer contains
  no logic and no rendering code; the renderer is a pure
  visualization step and does not modify world data; editors
  perform "controlled mutations of the world state" (the README
  calls them "interactive generators"). The pattern: **state is
  passive; generators and editors are mutations on state; the
  renderer is a projection**. This is a clean cut of the
  command/event-sourcing trichotomy — INV-1 inherits this shape
  directly: the canon log is the world data; `sim/systems/` are
  the generators; `cli/` are the editors (validation front-door);
  `render/` is the renderer.
- **Ordered generator pipeline.** `src/generators/index.ts`
  declares the canonical order of generator invocations as a
  list of side-effecting `import "./X";` statements:
  `voronoi` → `heightmap-generator` → `features` →
  `names-generator` → `lakes` → `river-generator` →
  `burgs-generator` → `biomes-generator` → `cultures-generator`
  → `routes-generator` → `states-generator` → `zones-generator`
  → `religions-generator` → `labels-generator` →
  `added-labels` → `provinces-generator` → `emblems-generator`
  → `ice-generator` → `ocean-generator` → `relief-generator`
  → `military-generator` → `markers-generator` →
  `measurers-generator` → `goods-generator` →
  `production-generator` → `markets-generator` → `resample`.
  Each generator depends on the output of the previous one
  (states need cultures, cultures need biomes, biomes need
  heightmap + rivers + temperature). The pattern: **a
  dependency-ordered pipeline of generator passes**, where each
  pass adds a layer to the world data. INV-2 inherits the shape
  (sorted iteration order, no per-pass RNG ambiguity); iter-1
  `core/queue.py` is the canonsim shape (heapq with
  `(tick, sub_order, actor_id)`, not a flat import list).
- **`State` interface — the per-entity record shape.**
  `src/generators/states-generator.ts` declares:
  `interface State { i: number; name: string; expansionism:
  number; capital: number; type: string; center: number;
  culture: number; coa: Emblem; lock?: boolean; removed?:
  boolean; pole?: [number, number]; neighbors?: number[];
  color?: string; cells?: number; area?: number; burgs?:
  number; rural?: number; urban?: number; campaigns?:
  Campaign[]; diplomacy?: string[]; formName?: string;
  fullName?: string; }`. The fields: `i` is the integer id,
  `name` is the display name, `capital` is the burg id of the
  capital, `culture` is a foreign-key to `cultures-generator`,
  `neighbors` is a list of adjacent state ids (computed once,
  cached on the record), `campaigns` is the embedded chronology
  (see below), `diplomacy` is a list of relationship strings per
  other state (state[0] holds the chronicle). The pattern:
  **per-entity record with foreign keys + cached adjacency +
  embedded sub-records** — this is the shape `entities.json`
  + `relations.json` (P2a in `MVP_SCOPE.md` §4.2) inherits,
  lifted into our pack format.
- **`Campaign` — the chronology event shape.** `states-generator.ts`
  line ~62 declares `interface Campaign { name: string; start:
  number; end: number; attacker: number; defender: number; }`
  — a single war with a start year, an end year, the attacking
  state id, the defending state id, and a name. The
  `generateCampaign(state)` function (line 463) picks a war type
  from a weighted table `{ War: 6, Campaign: 4, ... }` (line
  464-467) and returns a `Campaign[]` for that state.
  `generateCampaigns()` (line 486) loops over states and
  populates `s.campaigns`. The chronology is a list of typed
  events with integer years and actor ids — the shape that
  `EVENT_SCHEMA.md` §2 (`tick` + `actor_id` + `cause` chain)
  inherits directly. The pattern: **chronology = list of typed
  records with temporal bounds + actor references** — INV-1
  event sourcing is the canonsim shape.
- **Diplomacy chronicle.** `generateDiplomacy()` (line 494) declares
  `// FIRST STATE IS ALWAYS NEUTRAL and contains the history of
  diplomacy` and writes to `const chronicle = states[0].diplomacy;`
  — the diplomatic history is stored on a designated "neutral"
  pseudo-state as a list of strings. Lines like `chronicle.push(war
  as any);` append records. The pattern: **a designated
  per-world chronicle record, append-only** — the canonsim shape
  is the global JSONL log (one record per event), not a per-state
  field; the canonsim analogue is "the log is the chronicle",
  which is a strict subset of Azgaar's per-state design.
- **Re-entrant pipeline.** The README notes editors are
  "interactive generators" that "perform controlled mutations of
  the world state" — the same generator code is re-runnable on a
  subset of the world (regenerate religions, regenerate provinces
  for one state). The pattern: **a generator is a pure-ish
  function `(state, params) → state'`**; the editor calls it on a
  subset. Our `Intent` → `Event` validation front-door (iter-3+
  `cli/` + `sim/systems/`) inherits this shape: a player intent
  is a controlled mutation, the simulator validates and emits
  the event, the canon log records the diff.
- **`.map` save file — the state snapshot.** The map is saved as
  a `.map` file (JSON-ish). The seed is the canonical handle;
  the snapshot is for incremental state recovery, not replay.
  Re-running `voronoi` + `heightmap-generator` + ... from the
  same seed reproduces the same map byte-identically (the d3
  random calls are seeded). The pattern: **seed + replay = the
  canonical handle; snapshot = the convenience** — INV-1 + INV-2
  inherit this distinction (the JSONL log is replay; the SQLite
  index is the convenience).
- **Generator sub-modules — the per-system scope.** Each generator
  module is a separate `.ts` file in `src/generators/` with a
  tight, single-purpose scope (e.g., `river-generator.ts` only
  does river networks; it consumes the heightmap and the cell
  graph from `voronoi`, produces a list of rivers). The
  generator file is the system boundary; cross-system calls go
  through the shared world-data layer, not direct imports. The
  pattern: **system = file = one responsibility** — iter-2
  `sim/systems/` inherits this shape (8 systems, one file each,
  per `MVP_SCOPE.md` §5).

**What we take.**

- The four-layer architecture (world data / generators /
  editors / renderers) is the cleanest precedent for INV-1's
  state/log/simulator/renderer trichotomy. Lifted into the
  canonsim layout (`core/` = plumbing, `sim/systems/` =
  generators, `cli/` = editors, `render/` = renderer) — the
  shape is direct.
- The `State` interface shape (per-entity record with foreign
  keys + cached adjacency + embedded sub-records) is the
  precedent for `content/packs/<pack>/entities.json` records
  in phase 3+ content packs.
- The `Campaign` interface shape (`name`/`start`/`end`/
  `attacker`/`defender`) is the precedent for the chronology
  event shape in `EVENT_SCHEMA.md` §2 — typed records with
  temporal bounds + actor references, append-only.
- The ordered generator pipeline as a list of side-effecting
  passes is the precedent for iter-1 `core/queue.py` — except
  our pipeline is `heapq`-driven with `(tick, sub_order,
  actor_id)` keys, not a flat import list (the INV-2 fix).

**What we adapt.**

- The per-state `diplomacy` chronicle array becomes a global
  JSONL log (INV-1): all events go to one append-only stream;
  per-actor projections are `fold(log)` views, not separate
  fields on the entity. This is the canonsim adaptation: the
  shape is preserved (chronicle is append-only, typed records),
  the storage is global (one log, not per-entity).
- The re-entrant pipeline (editors as "interactive generators")
  becomes the `Intent` → `Event` validation front-door in
  iter-3+ `cli/`: the player's intent is the controlled
  mutation, the simulator validates + emits the event, the log
  records the diff. Azgaar's editors mutate state in place;
  our adaptation never mutates — only appends (INV-5).
- The `.map` save file (state snapshot + seed) becomes the
  JSONL log (replay) + SQLite index (snapshot) split. The
  distinction is the same; the substrate is different.

**What inspires us.**

- The README's "Inspiration" section cites Martin O'Leary's
  _Generating fantasy maps_ and Amit Patel's _Polygonal Map
  Generation for Games_ and Scott Turner's _Here Dragons
  Abound_. The lesson: a procedural world generator is a small
  composition of focused passes (heightmap → drainage → biomes
  → cultures → states), each pass a separate algorithm with
  clear inputs and outputs. The "small alphabet, deep
  composition" lesson (cf. `brogue.md` "small rule alphabet
  producing emergent depth") is the same design principle,
  applied to worldgen rather than environmental sim.

**Strengths.**

- MIT-licensed — code and save format both. Pattern lifting is
  permitted per `REFERENCES.md` §0.4 without license friction.
- The four-layer architecture is documented explicitly in the
  README; it is not inferred from code reading. This is rare
  for a procedural project; most roguelike/worldgen tools leave
  the architecture implicit.
- The `State` and `Campaign` interfaces have real, named fields
  with types — the per-entity record + chronology event shapes
  are concrete, not abstract.
- The ordered generator pipeline is declarative in
  `src/generators/index.ts` — a list of side-effecting imports
  that documents the dependency order. The dependency graph is
  in the file, not implied.
- The seed is the canonical reproducibility handle; the snapshot
  is convenience. This distinction is the INV-1 + INV-2 design
  principle in production.

**Weaknesses.**

- The generator pipeline is **side-effecting imports**, not
  event emissions — generators mutate the world-data layer in
  place. INV-1 forbids in-place mutation; the canonsim
  adaptation is "every generator pass emits events to the log".
  The pattern is preserved (ordered passes), the storage is
  inverted (append-only log vs in-place mutation).
- The pipeline is **not** byte-identical-replayable across
  machines — d3's PRNG and Voronoi triangulation are
  floating-point-heavy; small float drift between JS engines
  or CPUs produces different maps. INV-2 requires
  byte-identical replay; the canonsim adaptation is integer
  ticks + integer sub_order + `random.Random(seed)` (no
  floating-point in the canonical path).
- The `diplomacy` chronicle is **per-state**, stored as a field
  on the state record. This is convenient for rendering but
  breaks the global-order guarantee — events across states
  have no total ordering. The canonsim adaptation is a global
  JSONL log with monotonic ticks; per-actor projections are
  `fold(log)` views.
- The `.map` save file mixes **state snapshot + generator
  parameters** — there is no clean separation between "what
  was generated" and "what was edited". The canonsim
  adaptation is "the log is the truth; the snapshot is an
  index".
- The catalog row says "chronology generator" but there is
  no `chronology-generator.ts` file — the chronology is
  embedded in `states-generator.ts` as `generateCampaigns`
  + `generateDiplomacy`. Minor catalog↔repo drift; this per-
  ref file is the long version, the catalog is the short.

**Verdict.** Phase-5 worldgen donor reference, mostly positive
on architecture (the four-layer split is the cleanest precedent
for INV-1's state/log/simulator/renderer trichotomy; the
`State` and `Campaign` interface shapes are the per-entity
record + chronology event shapes that `entities.json` +
`EVENT_SCHEMA.md` §2 inherit), explicitly negative on
side-effecting pipeline (INV-1 fix: emit events, not in-place
mutation) + per-state chronicle (INV-1 fix: global JSONL log)
+ floating-point Voronoi determinism (INV-2 fix: integer
ticks + `random.Random(seed)`). The `.map` save file is the
seed-handle + snapshot distinction in production; the canonsim
adaptation is the JSONL log + SQLite index split. The "small
alphabet, deep composition" lesson (heightmap → drainage →
biomes → cultures → states, each a focused pass) is the
design principle for iter-2+ `sim/systems/` (8 systems, one
file each, ordered pipeline). The catalog row reads "chronology
generator" but the chronology lives in `states-generator.ts`;
this per-ref file is the long version that fixes the short-
hand.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
