# rot.js · `REFERENCES.md` §3 + §14 · BSD-3-Clause · phase 5 (grid math, pattern only D-012)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is BSD-3-Clause (per
> `package.json` `license` field, verified 2026-08-26) — pattern
> lifting is permitted per §0.4; copying the TypeScript/JS
> implementation is not useful — our runtime is Python stdlib
> (D-012), rot.js is TypeScript/JS; we lift the **algorithm
> shapes** (event queue with min-heap, scheduler family,
  map-generator family, FOV/PreciseShadowcasting, RNG/Alea)
> into our `core/queue.py` + `sim/systems/` + `core/rng.py`,
> never the TypeScript code. Reference repo:
> `ondras/rot.js` (active). Catalog §3 row reads "rot.js |
> BSD-3-Clause | JS toolkit: scheduler, FOV, map generators —
> well-documented algorithms"; index §2 row had "BSD" shorthand
> — standing pre-flip check (KI#6-class) caught the drift
> against catalog §3's "BSD-3-Clause"; index fixed in the same
> §2 edit that flips ref-9-b todo → done.

**What it is.** rot.js ("Roguelike Toolkit") is a JavaScript /
TypeScript roguelike toolkit, originally created by Ondřej
Žára in 2013 and considered "feature-complete". The library
covers: RNG (Alea algorithm), event queue (min-heap-based),
scheduler (simple/speed/action), FOV (DiscreteShadowcasting,
PreciseShadowcasting, RecursiveShadowcasting), path (A*,
Dijkstra), map (Arena, Cellular, Digger, DividedMaze, Dungeon,
EllerMaze, Features, IceyMaze, Rogue, Uniform), lighting,
color, text, stringgenerator (procedural name generation),
engine (game loop wrapper). BSD-3-Clause — pattern lifting is
permitted without license friction; the TypeScript/JS code is
not useful as a runtime dependency for our Python stdlib-only
core (D-012), but the algorithm shapes (event queue with
min-heap, scheduler family, map generator family) are direct
precedents for `core/queue.py` (iter-1) and `sim/systems/`
(iter-2+). rot.js is the "sibling" of libtcod (`libtcod.md`)
in JavaScript — the same conceptual family, different
language. The pattern: a small focused toolkit with clear
module boundaries.

**Concrete mechanics.**

- **Module split — per-feature file scope.** The library is
  split into per-feature TypeScript files in `src/`:
  `rng.ts` (Alea RNG), `eventqueue.ts` (the min-heap event
  queue), `engine.ts` (game loop wrapper), `lighting.ts`
  (light propagation), `color.ts`, `constants.ts`, `text.ts`,
  `stringgenerator.ts` (procedural name generation), `util.ts`,
  `index.ts` (the public API surface). Sub-directories:
  `src/scheduler/` (scheduler family: `scheduler.ts`
  abstract, `simple.ts`, `speed.ts`, `action.ts`, `index.ts`),
  `src/fov/` (FOV family: `fov.ts` abstract, `discrete-
  shadowcasting.ts`, `precise-shadowcasting.ts`,
  `recursive-shadowcasting.ts`, `index.ts`), `src/path/`
  (path family: `path.ts` abstract, `astar.ts`, `dijkstra.ts`,
  `index.ts`), `src/map/` (map family: `arena.ts`,
  `cellular.ts`, `digger.ts`, `dividedmaze.ts`, `dungeon.ts`,
  `ellermaze.ts`, `features.ts`, `iceymaze.ts`, `map.ts`
  abstract, `rogue.ts`, `uniform.ts`, `index.ts`). The
  pattern: **per-feature directory + abstract base class +
  concrete subclasses** — the feature is the directory
  boundary; variants are subclasses. Our `sim/systems/`
  inherits the shape (per-system file; if a system has
  variants, they're subclasses).
- **`EventQueue` — the min-heap core.** `src/eventqueue.ts`
  declares `export default class EventQueue<T = any> {
  _time: number; _events: MinHeap<T>; constructor() {
  this._time = 0; this._events = new MinHeap(); } getTime()
  { return this._time; } clear() { this._events = new
  MinHeap(); return this; } ... }`. The event queue uses
  `MinHeap<T>` (from `./MinHeap.js`) to store events by
  time; `_time` tracks the current simulation time. The
  pattern: **a min-heap of events ordered by time + a current
  time pointer** — the canonical event-scheduling primitive.
  Our `core/queue.py` (iter-1) inherits the shape directly:
  `heapq` (Python stdlib) for the heap, `_time` is the
  integer tick, the heap key is `(tick, sub_order, actor_id)`
  (the INV-2 fix — rot.js uses just `_time`, which can
  collide on simultaneous events; our 3-tuple tiebreaker is
  the addition).
- **Scheduler family — three scheduling disciplines.**
  `src/scheduler/` has:
  - `scheduler.ts` (abstract base): `class Scheduler<T> {
  _queue: EventQueue<T>; _repeat: T[]; _current: any;
  constructor() { this._queue = new EventQueue<T>();
  this._repeat = []; this._current = null; }
  getTime() { return this._queue.getTime(); }
  add(item, repeat) { ... } clear() { ... }
  remove(item) { ... } next() { ... abstract }
  }`. The abstract scheduler delegates to an `EventQueue`
  for time-ordered retrieval; subclasses define `next()`
  to control the order.
  - `simple.ts`: round-robin — `next()` returns the next
    item in insertion order. No time progression; the queue
    is just an order list.
  - `speed.ts`: speed-based — each actor has a `getSpeed()`
    that returns a number; the scheduler schedules the next
    event at `_time + 1/speed`, so faster actors act more
    frequently. The classic roguelike turn scheduler.
  - `action.ts`: action-point-based — actors accumulate
    action points over time; when they have enough, they
    can act. More flexible than speed-based (an action can
    cost more or fewer points).

  The pattern: **a family of schedulers extending one
  abstract base, each defining a turn discipline**. Our
  `core/queue.py` (iter-1) inherits the shape (the queue
  key `(tick, sub_order, actor_id)` is the discipline;
  iter-3+ may add a speed-based variant — but the base
  shape is the same).
- **FOV family — three shadowcasting algorithms.**
  `src/fov/` has:
  - `fov.ts` (abstract base): `abstract class FOV {
  abstract compute(x, y, R, callback: VisibilityCallback):
  void; }` with `LightPassesCallback` (boolean per tile)
  + `VisibilityCallback` (per tile in FOV: x, y, r,
  visibility 0..1). The base defines the interface; the
  subclasses implement `compute`.
  - `discrete-shadowcasting.ts`: per-octant line-tracing
    FOV; tiles are 0/1 visible.
  - `precise-shadowcasting.ts`: per-octant with
    fractional visibility; tiles have visibility 0..1
    (relevant for partial cover, dim light).
  - `recursive-shadowcasting.ts`: the "classic" recursive
    shadowcasting (the same family as libtcod's
    `FOV_SHADOW`).

  The pattern: **a closed family of FOV algorithms extending
  one abstract base, each implementing `compute(x, y, R,
  callback)`**. Our `sim/systems/perception.py` (iter-3)
  inherits the shape (closed enum at config time; the
  interface is the same — viewer position + radius +
  per-tile callback).
- **Path family — A* and Dijkstra.** `src/path/` has:
  - `path.ts` (abstract base): defines the pathfinding
    interface — `compute(x1, y1, x2, y2, callback)` returns
    a list of waypoints. The base takes a `8xN` neighbor
    function + a cost function.
  - `astar.ts`: A* with a heuristic (Manhattan by default).
  - `dijkstra.ts`: Dijkstra (no heuristic; finds shortest
    paths to all reachable tiles).

  The pattern: **two algorithms extending one abstract base,
  same interface**. Our `sim/systems/movement.py` (iter-2)
  inherits the shape (closed enum at config time; the
  interface is `compute(start, goal, callback)`).
- **Map family — 11 procedural map generators.** `src/map/`
  has: `arena.ts` (full rectangular room), `cellular.ts`
  (cellular automata cave generator), `digger.ts` (recursive
  room digger), `dividedmaze.ts` (recursive maze splitter),
  `dungeon.ts` (multi-room dungeon), `ellermaze.ts` (Eller's
  algorithm maze), `features.ts` (feature-based dungeon),
  `iceymaze.ts` (icy variant of EllerMaze), `map.ts` (abstract
  base), `rogue.ts` (Rogue-like rooms + corridors),
  `uniform.ts` (uniform random rooms). The pattern: **a
  closed family of map generators extending one abstract
  base** — each defines a `create(callback)` method. Our
  phase-5+ spatial layer (if we ever add one) inherits the
  shape; phase-0 tavern uses a fixed grid, not procedural.
- **RNG — Alea algorithm.** `src/rng.ts` declares
  `class RNG { _seed = 0; _s0 = 0; _s1 = 0; _s2 = 0; _c = 0;
  getSeed() { return this._seed; }
  setSeed(seed) { seed = (seed < 1 ? 1/seed : seed);
  this._seed = seed; this._s0 = (seed >>> 0) * FRAC;
  seed = (seed*69069 + 1) >>> 0; this._s1 = seed * FRAC;
  seed = (seed*69069 + 1) >>> 0; this._s2 = seed * FRAC;
  ... }`. The class uses Johannes Baagøe's Alea algorithm,
  with three internal state values `_s0`/`_s1`/`_s2` and a
  carry `_c`. The seeding uses the formula
  `seed*69069 + 1` (a classic LCG for state expansion). The
  pattern: **a single PRNG class with a seed, all rolls go
  through one instance**. Our `core/rng.py` (iter-1) inherits
  the shape — Python's `random.Random(seed)` (Mersenne
  Twister) is the equivalent; INV-2 requires one instance.
- **Engine — the game loop wrapper.** `src/engine.ts` defines
  the loop: `while (this._scheduler.length) { const actor =
  this._scheduler.next(); if (!actor) { break; } const
  result = actor.act(); if (result && result.then)
  { result.then(() => this._loop()); return; } }`. The
  pattern: **a single-threaded loop that pulls actors from
  the scheduler, calls `act()`, and repeats** — the canonical
  roguelike turn loop. Our `core/runner.py` (iter-1) inherits
  the shape (the canonsim runner pulls the next event from
  the queue, applies the action, emits the event, repeats).
  Note: rot.js's loop supports async `result.then` — for
  browser-side promise-based actions. Our core is sync; the
  async path is not relevant.
- **StringGenerator — procedural name generation.**
  `src/stringgenerator.ts` provides a context-free grammar
  for procedural name generation — the same conceptual shape
  as tracery (`tracery.md`), but a separate implementation.
  The pattern: **a CFG-based procedural text generator** —
  our `templates.json` + `render/` (iter-5) inherits the
  shape directly (via tracery, which is the more polished
  reference).

**What we take.**

- The `EventQueue` min-heap shape (events ordered by time +
  a current time pointer) is the precedent for our `core/
  queue.py` (iter-1) — using Python's `heapq` for the heap,
  the integer tick for time, and the 3-tuple `(tick,
  sub_order, actor_id)` for the queue key (the INV-2 fix
  for tiebreaking — rot.js's bare `_time` can collide on
  simultaneous events).
- The scheduler family pattern (abstract base + concrete
  subclasses for simple/speed/action) is the precedent for
  our `core/queue.py` discipline — the queue key IS the
  discipline; iter-3+ may add a speed-based variant if
  needed.
- The FOV family pattern (abstract base + concrete
  subclasses for Discrete/Precise/Recursive Shadowcasting)
  is the precedent for our `sim/systems/perception.py`
  (iter-3) — closed enum at config time; the interface is
  `compute(viewer_x, viewer_y, radius, callback)`.
- The path family pattern (A* and Dijkstra extending one
  abstract base) is the precedent for our `sim/systems/
  movement.py` (iter-2).
- The single-class seeded RNG (Alea with `_s0`/`_s1`/`_s2` +
  carry) is the precedent for our `core/rng.py` (iter-1) —
  Python's `random.Random(seed)` is the equivalent (INV-2:
  one instance, no wall-clock).
- The per-feature directory + abstract base + concrete
  subclasses shape is the precedent for our `sim/systems/`
  file layout.

**What we adapt.**

- The TypeScript/JS implementation is not useful as a runtime
  dependency; we adapt by porting the algorithm shapes into
  Python stdlib. No external code is vendored (D-012).
- The bare `_time` event-queue key is replaced with the
  3-tuple `(tick, sub_order, actor_id)` queue key (INV-2
  fix) — simultaneous events are sorted deterministically
  by sub_order then actor_id, not by insertion order.
- The async `result.then` engine loop is replaced with a
  sync loop (our core is sync; no async path needed in
  phase 0).
- The map generator family (11 algorithms) is deferred to
  phase-5+ spatial layer; phase-0 tavern uses a fixed grid.
- The `stringgenerator.ts` is superseded by tracery
  (`tracery.md`) as the more polished reference for our
  `templates.json` + `render/` shape.

**What inspires us.**

- The library is **considered "feature-complete"** — the
  README says "largely considered 'feature-complete', but
  bugfixes, documentation, and some new features are
  welcomed." The lesson: a focused toolkit reaches
  feature-completeness in its domain and stops growing;
  the test of stability is not new features but bugfixes +
  documentation. Our `sim/systems/` (8 systems in phase 0)
  is a similar scope — focused, complete, stops growing
  after iter-6 phase gate.
- The scheduler family (simple/speed/action) is the lesson
  that **the right answer depends on the game's needs** —
  a turn-based roguelike uses speed-based; an action-point
  game uses action-based. Our phase-0 uses a fixed queue key
  (`(tick, sub_order, actor_id)`); iter-3+ may add a speed-
  based variant if P2b minimal goal/urge ticker (D-021)
  needs it.

**Strengths.**

- BSD-3-Clause — pattern lifting is permitted without license
  friction. The algorithm shapes are direct inheritances.
- The library is "feature-complete" — stable, no breaking
  changes; the algorithm shapes are durable.
- The `EventQueue` min-heap is the canonical event-scheduling
  primitive — the shape is direct and battle-tested.
- The scheduler family (abstract base + 3 concrete
  subclasses for simple/speed/action) is a clean closure of
  the scheduling variants; the consumer picks one at
  construction time.
- The FOV family (abstract base + 3 concrete subclasses
  for Discrete/Precise/Recursive Shadowcasting) is a clean
  closure of the FOV variants.
- The map generator family (11 algorithms extending one
  abstract base) is the most complete closure of procedural
  map generation variants in any single toolkit.
- TypeScript/JS — readable, well-commented; the algorithm
  shapes are clear in the code.

**Weaknesses.**

- The library is **TypeScript/JS** — not useful as a runtime
  dependency for our Python stdlib-only core (D-012). We
  port the algorithm shapes, not the code.
- The `EventQueue` uses **bare `_time`** as the heap key —
  simultaneous events collide; the order is determined by
  heap insertion, which is not deterministic across
  implementations. INV-2 fixes this with the 3-tuple
  `(tick, sub_order, actor_id)` queue key.
- The library is **browser-focused** (the README has
  sections on `<script>` tag, ES2015 modules, babel+rollup
  bundlers, Node.js with `term` layout backend). Our
  phase-0 is CLI; the browser concerns are not relevant.
- The library has **no event sourcing** — the engine loop
  calls `actor.act()` and discards the result; there is no
  event log. INV-1 inverts: every action is an event in
  the canon log, the act() returns an Intent that the
  simulator validates.
- The library has **no determinism contract** — the RNG
  (Alea) is single-instance seeded, but the library does
  not enforce no-wall-clock, sorted iteration, or queue
  key discipline. INV-2 fixes this.
- The library has **no content/code split** — the algorithm
  parameters are hardcoded in the TypeScript classes, not
  configurable from a content pack. INV-3 inverts.
- The `setSeed` function has the line `seed = (seed < 1 ?
  1/seed : seed);` — this is a hack to handle fractional
  seeds by inverting them. Our `random.Random(seed)` accepts
  any hashable; we use an integer seed, no inversion.

**Verdict.** Phase-5 grid-math pattern-only reference (D-012),
mostly positive on algorithm shapes (the `EventQueue` min-heap,
the scheduler family with abstract base + 3 concrete
subclasses, the FOV family with abstract base + 3 concrete
subclasses, the path family with A* + Dijkstra, the single-
class seeded RNG, the per-feature directory + abstract base
+ concrete subclasses shape are all direct inheritances),
explicitly negative on TypeScript/JS implementation (D-012
fix: port shapes to Python stdlib) + bare `_time` queue key
(INV-2 fix: 3-tuple `(tick, sub_order, actor_id)` queue key
for tiebreaking) + browser focus (CLI not relevant; lift only
the algorithm shapes) + no event sourcing (INV-1 fix: every
action is a canon event) + no determinism contract (INV-2
fix: one RNG instance, no wall-clock, sorted iteration,
queue key) + no content/code split (INV-3 fix: algorithm
choice is config-time, recorded in the determinism contract).
BSD-3-Clause license (verified 2026-08-26 from `package.json`
`license` field) is the most permissive that still requires
attribution — no license friction at intake. The "feature-
complete focused toolkit" lesson is the inspiration: our
`sim/systems/` (8 systems) is a similar scope, stops growing
after iter-6 phase gate. The scheduler family pattern (3
disciplines for different game types) is the precedent for
our queue-key discipline — iter-3+ may add a speed-based
variant if P2b minimal goal/urge ticker (D-021) needs it.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
