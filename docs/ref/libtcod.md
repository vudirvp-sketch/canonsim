# libtcod · `REFERENCES.md` §3 + §14 · BSD-3-Clause · phase 5 (grid math, pattern only D-012)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is BSD-3-Clause — pattern
> lifting is permitted per §0.4; copying the C/C++ implementation
> is permitted but not useful — our runtime is Python stdlib
> (D-012), libtcod is C/C++; we lift the **algorithm shapes**
> (FOV enum, A* pseudo-code, BSP dungeon pattern, heightmap
> pipeline) into our `sim/systems/` + `render/`, never the C
> code. Reference repo: `libtcod/libtcod` (active fork by
> `HexDecimal`). Catalog §3 row reads "libtcod | BSD-3-Clause |
> the classic: FOV, pathfinding, RNG, noise"; index §2 row had
> "BSD" shorthand — standing pre-flip check (KI#6-class) caught
> the drift against catalog §3's "BSD-3-Clause"; index fixed in
> the same §2 edit that flips ref-9-a todo → done.

**What it is.** libtcod is a free, fast, portable C/C++ API for
roguelike developers providing a true-color console, pathfinding,
field-of-view (FOV), and a few other utilities frequently used in
roguelikes. First released ~2008, still actively maintained by
`HexDecimal` (Kyle Benham) at the time of writing. The library
covers: console (true-color, ASCII, tileset rendering), FOV (8
algorithms), pathfinding (A* and Dijkstra), noise (Perlin,
Simplex, Wavelet), BSP (binary space partitioning for dungeon
generation), heightmap (perlin-noise-driven terrain), RNG
(Mersenne Twister), name generation, image manipulation, color
math, lex/parser (data-driven config), txtfield (text fields),
tree, list. BSD-3-Clause — pattern lifting is permitted without
license friction; the C/C++ code is not useful as a runtime
dependency for our Python stdlib-only core (D-012), but the
algorithm shapes are direct precedents for `sim/systems/`
(perception system FOV, movement system A*) and `core/` (RNG
discipline, heightmap pipeline).

**Concrete mechanics.**

- **Module split — per-feature file scope.** The library is
  split into per-feature files in `src/libtcod/`: `fov.h`/`fov.hpp`
  (FOV algorithms), `path.h`/`path.hpp` (A*, Dijkstra),
  `pathfinder.h`/`pathfinder_frontier.h` (modern pathfinder),
  `noise.h`/`noise.hpp`/`noise_defaults.h` (Perlin/Simplex/
  Wavelet), `bsp.h`/`bsp.hpp` (binary space partitioning),
  `heightmap.h`/`heightmap.hpp` (terrain heightmaps),
  `mersenne.h`/`mersenne.hpp`/`mersenne_types.h` (Mersenne
  Twister RNG), `random.h` (RNG interface), `color.h`/`color.hpp`
  (color math), `console.h`/`console.hpp`/`console_*.h` (true-color
  console), `context.h`/`context_init.h`/`context_viewport.h`
  (modern context), `image.h`/`image.hpp`, `lex.h`/`lex.hpp`/
  `parser.h`/`parser.hpp` (data-driven config), `list.h`/
  `list.hpp`, `tree.h`/`tree.hpp`, `heapq.h` (binary heap
  priority queue, used by path), `txtfield.h`/`txtfield.hpp`
  (text fields), `namegen.h`/`namegen.hpp` (procedural name
  generation), `bresenham.h`/`bresenham.hpp` (line drawing),
  `mouse.h`/`mouse.hpp` (mouse input), `sys.h`/`sys.hpp`
  (system utilities), `tileset.h`/`tileset_*.h` (tileset
  rendering: BDF, fallback, TrueType, render), `renderer_xterm.h`
  (xterm renderer), `logging.h`, `version.h`, `utility.h`,
  `portability.h`, `error.h`/`error.hpp`, `globals.h`,
  `matrix.hpp`, `config.h`, `console_drawing.h`,
  `console_etc.h`, `console_init.h`, `console_printing.h`/
  `console_printing.hpp`, `console_rexpaint.h`/`console_rexpaint.hpp`,
  `console_types.h`/`console_types.hpp`. The pattern:
  **one file per feature, .h for C and .hpp for C++** — the
  feature is the file boundary. Our `sim/systems/` inherits
  the shape (8 systems in `MVP_SCOPE.md` §5, one file each).
- **FOV algorithm enum — the closed choice of algorithms.**
  `src/libtcod/fov_types.h` declares `typedef enum {
  FOV_BASIC, FOV_DIAMOND, FOV_SHADOW, FOV_PERMISSIVE_0,
  FOV_PERMISSIVE_1, FOV_PERMISSIVE_2, FOV_PERMISSIVE_3,
  FOV_PERMISSIVE_4, FOV_PERMISSIVE_5, FOV_PERMISSIVE_6,
  FOV_PERMISSIVE_7, FOV_PERMISSIVE_8, FOV_RESTRICTIVE,
  FOV_SYMMETRIC_SHADOWCAST, NB_FOV_ALGORITHMS }`. The enum
  has 14 algorithm values (FOV_BASIC, FOV_DIAMOND, FOV_SHADOW,
  9 permissive levels 0–8, FOV_RESTRICTIVE,
  FOV_SYMMETRIC_SHADOWCAST) plus `NB_FOV_ALGORITHMS` as the
  sentinel count. The pattern: **a closed enum of available
  algorithms** — the consumer picks one at the API call. Our
  `sim/systems/perception.py` (iter-3) inherits the shape:
  the perception system picks an FOV algorithm from a closed
  enum at config time; the algorithm choice is part of the
  determinism contract (one algorithm per simulation run).
- **`TCOD_MapCell` — the per-tile FOV state.** `fov_types.h`
  declares `struct TCOD_MapCell { bool transparent; bool
  walkable; bool fov; }`. The `transparent` flag is input
  (whether light passes through), `walkable` is for
  pathfinding input, `fov` is output (whether the tile is in
  the current FOV). A `TCOD_Map` is `struct TCOD_Map { int
  width; int height; int nbcells; struct TCOD_MapCell*
  __restrict cells; }` — a flat array of cells indexed by
  `y * width + x`. The pattern: **per-tile state with input
  + output flags**, computed by the FOV algorithm. Our
  `sim/systems/perception.py` inherits the shape: per-tile
  visibility is a derived projection from the canon log
  (the log records "what is there", the perception system
  projects "what can be seen" given the viewer's position +
  sight radius).
- **A* and Dijkstra pathfinders.** `src/libtcod/path.h`
  documents "Libtcod A* and Dijkstra pathfinders." The
  pathfinder interface takes a `TCOD_map_t` (or a custom
  callback for walkable + cost) and produces a path as a list
  of `(x, y)` waypoints. The A* uses a binary heap (cf.
  `heapq.h` — libtcod's own heap implementation, the same
  Python's `heapq` is in stdlib). The pattern: **A* is a
  graph-search algorithm with a per-tile cost function +
  a priority queue** — the canonsim `core/queue.py` uses
  the same `heapq` primitive with the queue key `(tick,
  sub_order, actor_id)` (a 3-tuple, the same shape as
  libtcod's heap key would have for pathfinding if we
  used it).
- **BSP dungeon generator — binary space partitioning.**
  `src/libtcod/bsp.h` provides `TCOD_bsp_t` (a tree node
  with `x, y, w, h, level, position, [left, right]` for
  children) and `TCOD_bsp_split` (recursively split a node
  into two children). The pattern: **recursive space
  partitioning → leaf rooms + connecting corridors** —
  the classic roguelike dungeon generator. Our phase-5+
  spatial layer (if we ever add one) inherits the shape;
  phase-0 tavern uses a fixed grid, not procedural.
- **Heightmap pipeline — Perlin-noise terrain.**
  `src/libtcod/heightmap.h` provides `TCOD_heightmap_t`
  (a 2D float array + width + height) and operations:
  `TCOD_heightmap_add` (offset all values), `TCOD_heightmap_
  normalize` (remap to a range), `TCOD_heightmap_add_fbm`
  (add Fractal Brownian Motion noise — Perlin/Simplex at
  multiple octaves), `TCOD_heightmap_scale_fbm`,
  `TCOD_heightmap_dig` (set values below a threshold to a
  constant — for lakes), `TCOD_heightmap_kernel_transform`
  (apply a kernel — erosion, smoothing). The pattern:
  **heightmap = 2D float array + Perlin noise + remap
  operations**. Our phase-5+ worldgen inherits the shape
  (cf. `azgaar_fmg.md`'s `heightmap-generator.ts` for the
  same pattern in JS/TS). Phase-0 tavern uses no heightmap.
- **Mersenne Twister RNG — the default PRNG.**
  `src/libtcod/mersenne.h` provides `TCODRandom` (the
  Mersenne Twister with a seed). The pattern: **a single
  PRNG instance with a seed**, all rolls go through one
  instance. Our `core/rng.py` inherits the shape directly:
  `random.Random(seed)` (Python stdlib — the Mersenne
  Twister is `random.Random`'s default in Python; INV-2
  requires one instance, no wall-clock, sorted iteration).
- **`heapq.h` — the binary heap primitive.** libtcod
  ships its own binary heap implementation (`heapq.h`) used
  by the pathfinder. The pattern: **a binary heap is the
  primitive for both pathfinding (A*) and event scheduling
  (priority queue)**. Python's `heapq` stdlib module is the
  direct equivalent — we use it for `core/queue.py` (the
  event queue). No external dependency required (D-012).

**What we take.**

- The FOV algorithm closed enum (14 algorithms) is the
  precedent for our `sim/systems/perception.py` perception
  system (iter-3): the algorithm choice is a config-time
  decision, recorded in the determinism contract.
- The per-tile `TCOD_MapCell` shape (`transparent` + `walkable`
  + `fov` flags) is the precedent for our per-tile state
  projection (the canon log records the underlying state;
  the perception system projects "what can be seen" — INV-1
  state = fold(log), the projection is derived).
- The A* + Dijkstra pathfinder interface (graph-search with
  per-tile cost function + priority queue) is the precedent
  for our `sim/systems/movement.py` (iter-2) — using Python's
  `heapq` for the priority queue, no external dependency.
- The single-instance seeded RNG (Mersenne Twister) is the
  precedent for our `core/rng.py` (iter-1) — Python's
  `random.Random(seed)` is the Mersenne Twister; INV-2
  requires one instance, no wall-clock.
- The per-feature file split (one .h/.hpp pair per
  feature) is the precedent for our `sim/systems/` file
  layout (one file per system, per `MVP_SCOPE.md` §5).

**What we adapt.**

- The C/C++ implementation is not useful as a runtime
  dependency; we adapt by porting the algorithm shapes into
  Python stdlib. No external code is vendored (D-012).
- The BSP dungeon generator is for procedural spatial layouts;
  we adapt by deferring to phase-5+ (phase-0 tavern uses a
  fixed grid). The shape is preserved; the timing is deferred.
- The heightmap pipeline (Perlin-noise terrain) is for
  worldgen; we adapt by deferring to phase-5+ worldgen (cf.
  `azgaar_fmg.md`'s `heightmap-generator.ts` for the same
  pattern in JS/TS). Phase-0 tavern uses no heightmap.
- The console rendering (true-color ASCII + tileset) is for
  display; we adapt by deferring to phase-5+ frontend work
  (our phase-0 is CLI, no UI). The render API shape (callback-
  driven, per-tile draw) is preserved in `render/` (iter-5).

**What inspires us.**

- The library is **BSD-3-Clause** — pattern lifting is
  permitted without license friction. The lesson: a permissive
  license on a reference implementation is a gift to the
  ecosystem; we lift the shapes, not the syntax, and we are
  under no obligation to ship our own code under the same
  license (unlike GPL/AGPL).
- The 14-algorithm FOV enum is the lesson that **the right
  answer depends on the game's needs** (basic for speed,
  permissive for "I want to see around corners",
  symmetric for "I want strict equality between viewer and
  viewee"). Our phase-0 perception system will pick one
  algorithm at config time and record the choice in the
  determinism contract — the choice is part of the replay
  contract.

**Strengths.**

- BSD-3-Clause — pattern lifting is permitted without license
  friction. The algorithm shapes are direct inheritances.
- 15+ years of codebase discipline (active since ~2008,
  maintained by `HexDecimal`) — the algorithms are battle-
  tested in production roguelikes (the official
  `libtcod/python-tcod` tutorial uses it as the canonical
  Python roguelike starter).
- The FOV algorithm enum is a closed list of well-documented
  algorithms (basic recursive shadowcasting, permissive levels
  0–8, restrictive, symmetric shadowcast) — the consumer picks
  one at the API call. The shape is direct.
- The per-feature file split (one .h/.hpp pair per feature)
  is a clean separation; each feature is independent.
- The library includes `heapq.h` — a binary heap primitive
  used by both pathfinding and (potentially) scheduling.
  Python's `heapq` stdlib module is the direct equivalent.

**Weaknesses.**

- The library is **C/C++** — not useful as a runtime
  dependency for our Python stdlib-only core (D-012). We
  port the algorithm shapes, not the code.
- The library is **broad but shallow** — many features
  (console, mouse, image, tileset rendering) are not
  relevant to a CLI simulation. We lift only the parts that
  apply to `sim/systems/` + `core/` + `render/`.
- The library has **no event sourcing** — the pathfinder
  result is a list of waypoints, not a stream of events.
  INV-1 inverts: every movement is an event in the canon
  log, the path is a derived projection.
- The library has **no determinism contract** — the RNG
  (Mersenne Twister) is single-instance seeded, but the
  library does not enforce no-wall-clock, sorted iteration,
  or queue key discipline. INV-2 fixes this; the canonsim
  adaptation is the rule, not the inspiration.
- The library has **no content/code split** — the FOV
  algorithms are hardcoded in `fov.h`, not configurable from
  a content pack. INV-3 inverts: the algorithm choice is
  config-time, recorded in the determinism contract; the
  algorithm parameters (e.g., permissive level 0–8) are
  data in the content pack, not code constants.

**Verdict.** Phase-5 grid-math pattern-only reference (D-012),
mostly positive on algorithm shapes (the FOV algorithm closed
enum, the per-tile `TCOD_MapCell` state, the A* + Dijkstra
pathfinder interface, the single-instance seeded RNG, the
per-feature file split are all direct inheritances), explicitly
negative on C/C++ implementation (D-012 fix: port shapes to
Python stdlib) + breadth-irrelevant-to-CLI (console, mouse,
image, tileset are not relevant to a CLI simulation; lift only
`sim/systems/` + `core/` + `render/` parts) + no event
sourcing (INV-1 fix: every movement is a canon event) + no
determinism contract (INV-2 fix: one RNG instance, no
wall-clock, sorted iteration, queue key) + no content/code
split (INV-3 fix: algorithm choice is config-time, recorded
in the determinism contract). BSD-3-Clause license is the most
permissive that still requires attribution — no license
friction at intake. The "permissive license on a reference
implementation is a gift to the ecosystem" lesson is the
inspiration: we lift shapes, not syntax, and we are under no
obligation to ship our code under the same license. The 14-
algorithm FOV enum is the precedent that the right answer
depends on the game's needs; we pick one at config time and
record the choice in the determinism contract.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
