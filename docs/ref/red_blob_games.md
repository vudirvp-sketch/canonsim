# Red Blob Games · `REFERENCES.md` §8 · CC-BY (treat as) · phase 5 (grid math, pattern only D-012)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). **License note (no catalog column
> for §8 sources):** Red Blob Games (Amit Patel's site at
> `redblobgames.com`) does not carry an explicit license
> statement on its article pages (verified 2026-08-26 by
> inspecting `/grids/hexagons/`, `/pathfinding/a-star/introduction.html`,
  `/about` — none publishes a license; the CSS comment says
  "CSS Copyright 2007-2026 by Amit J. Patel" but that's the
  stylesheet, not the content). Amit Patel explicitly requests
  attribution in academic contexts (per `/blog/` "For attribution
  in academic contexts, please cite this work as ..."). The
  convention adopted here is **treat as CC-BY 4.0** —
  attribution required; no commercial restriction implied. The
  catalog §8 row has no license column (it's a knowledge-base
  table, not a donor/pattern table), so the index §2 row "CC-BY"
  is the source-of-truth license for this per-ref file. We lift
  the **algorithm shapes** (hex grid coordinate conversions,
  A* pseudo-code, Voronoi for region borders, polygon map
  generation) into our `sim/systems/` + `core/` + `render/`,
  never the prose. Reference site: `redblobgames.com` (Amit
  Patel, Stanford-affiliated, maintained since 2007).

**What it is.** Red Blob Games is Amit Patel's personal site of
interactive tutorials and write-ups for math and algorithms
relevant to game development, maintained since 2007 (CSS
Copyright "2007-2026"). The site is the canonical reference for
hexagonal-grid math, A* pathfinding (the "Introduction to A*"
page is the most-cited A* tutorial in game development), polygon
map generation (the "Polygon Map Generation" article uses Voronoi
diagrams + noise for fantasy map coastlines), grid math (parts,
edges, circle-drawing), and various other algorithm write-ups
(noisy-edges, curved-paths, distance-to-any, all-pairs
shortest paths, SDF fonts). The articles are interactive
(HTML5 canvas demos, JS code samples) and well-illustrated
(diagrams, animations). The site is the precedent for our
phase-5 algorithm references — the canonical write-up layer
above the libtcod/rot.js implementations.

**Concrete mechanics.**

- **Hex grid coordinate systems — the axial/cube/doubled family.**
  `/grids/hexagons/` ("Amit's Guide to Hexagonal Grids") is
  the canonical reference for hex grid math. The page covers:
  - **Coordinate systems**: offset coordinates (row/col +
    odd-r/even-r/odd-q/even-q), axial coordinates (q, r),
    cube coordinates (x, y, z with `x + y + z = 0`), and
    doubled coordinates. The page recommends axial for most
    uses; cube for algorithms that benefit from the symmetry
    (e.g., distance, line-drawing).
  - **Coordinate conversions**: offset ↔ axial ↔ cube — the
    page documents the exact formulas for each conversion.
  - **Distance**: in cube coordinates, `distance(a, b) =
    max(|a.x - b.x|, |a.y - b.y|, |a.z - b.z|)` (the
    Manhattan distance in cube space, which is the
    hex-grid distance).
  - **Line drawing**: a hex-grid Bresenham-like algorithm
    that interpolates between two hexes by sampling a line
    in cube coordinates and rounding.
  - **Range**: the set of hexes within N steps of a given
    hex — computed by walking the cube coordinate ring.
  - **Rotation**: rotate a hex by 60° around the origin in
    cube coordinates — the rotation is a simple linear map.
  - **Field of view / line of sight**: per-hex visibility
    on a hex grid, using the line-drawing algorithm to
    check each candidate target.
  - **Pixel-to-hex conversion**: given a pixel (x, y), find
    the hex that contains it — the page documents
    `pixel_to_hex` formulas for both pointy-top and flat-top
    orientations, with the fractional hex intermediate.
  - **Storage**: hex coordinates stored as `(q, r)` pairs;
    cube coordinates computed on demand from `(q, r)` (z =
    -q - r).

  The pattern: **a complete algebra of hex coordinates with
  conversions, distance, line, range, rotation, FOV, and
  pixel-to-hex** — the canonical write-up that every other
  hex-grid library (libtcod, rot.js, hexlib, reffy) implements.
  Our phase-5+ spatial layer (if hex-based) inherits the
  formulas; the phase-0 tavern is a fixed pack-authored
  location graph (no grid at all).

- **A* pathfinding — the canonical write-up.**
  `/pathfinding/a-star/introduction.html` ("Introduction to A*")
  is the most-cited A* tutorial in game development. The page
  covers:
  - **The A* algorithm**: open set, closed set, `g` (cost
    from start), `h` (heuristic estimate to goal), `f = g +
    h`; pick the node with the lowest `f`, expand neighbors,
    update their `g` and parent; continue until the goal is
    reached. The pseudo-code is implementation-independent
    (BFS, Dijkstra, A* are presented as a family with
    different `h` choices: 0 for BFS, "exact cost" for
    Dijkstra, "estimated cost" for A*).
  - **Heuristic functions**: Manhattan, Euclidean, Chebyshev,
    Octile — the choice depends on the movement rules (4-way
    vs 8-way vs continuous).
  - **Implementation notes**: priority queue (binary heap),
    tiebreaking (prefer the higher `g` to break ties toward
    the goal), IDA* for memory-constrained searches.
  - **Variants**: weighted A* (multiply `h` by a factor > 1
    for faster but suboptimal search), bidirectional A*
    (search from both ends), hierarchical A* (pre-computed
    cluster graph).

  The pattern: **A* is a graph-search algorithm with a
  priority queue + a heuristic; the choice of heuristic
  determines the variant**. Our `sim/systems/movement.py`
  (iter-2) inherits the shape directly; the libtcod (`libtcod.md`)
  and rot.js (`rot_js.md`) implementations are concrete
  instances of the same algorithm.

- **Polygon map generation — Voronoi + noise.**
  Amit's "Polygon Map Generation" article (the canonical
  reference, dated ~2010) uses:
  - **Voronoi diagram**: start with N random points;
    compute the Voronoi diagram (each cell is the region
    closer to its seed than to any other seed). Use
    `d3-delaunay` (or `delaunator`) for the computation.
  - **Relaxed Voronoi (Lloyd's algorithm)**: replace each
    seed with the centroid of its Voronoi cell; iterate
    1-2 times for a more uniform distribution.
  - **Perlin noise for elevation**: assign each Voronoi
    corner an elevation = the Perlin noise value at its
    position; interpolate to island shape (subtract a
    radial gradient to push the edges to ocean).
  - **Watershed for rivers**: trace downhill from each
    corner to its lowest neighbor; the corners with the
    most upstream corners are rivers.
  - **Biome assignment**: assign each Voronoi cell a biome
    based on (elevation, moisture) — the Whittaker
    diagram (elevation × moisture → biome type).
  - **Noisy edges**: replace the straight Voronoi edges
    with subdivided noisy lines for a hand-drawn look
    (separate article: `/maps/noisy-edges/`).

  The pattern: **Voronoi + noise + watershed + biome
  assignment** — the canonical polygon map generator. Our
  phase-5+ worldgen inherits the shape; the Azgaar FMG
  (`azgaar_fmg.md`) implements the same algorithm with
  additional passes (states, cultures, religions).

- **Grid parts and edges — the relational-grid abstraction.**
  `/grids/parts/` documents a grid abstraction where each
  cell has **parts**: faces, edges, corners. Each part has
  a list of relations (a face has edges, each edge has 2
  corners, each corner has 3 edges, etc.). The page covers
  square grids, hex grids, triangle grids — the same
  relational shape, different geometries. The pattern:
  **a grid is a graph of parts (face/edge/corner) with
  typed relations** — our phase-5+ spatial layer (if it
  supports hex or other grids) inherits the relational
  shape; the canon log records per-part events, the
  projection queries per-part relations.

- **Circle drawing — for circular rooms and AoE effects.**
  `/grids/circle-drawing/` covers several algorithms for
  drawing a circle on a square grid (midpoint circle,
  Andreev's algorithm, etc.) — relevant for AoE effects
  (a fireball's blast radius) and circular rooms. Our
  `sim/systems/` (iter-2 fire_spread) inherits the shape
  for AoE queries.

- **Distance to any / all-pairs shortest paths.**
  `/pathfinding/distance-to-any/` covers single-source
  shortest paths (Dijkstra); `/pathfinding/all-pairs/`
  covers Floyd-Warshall for pre-computing all-pairs
  shortest paths (useful when the map is small and
  queries are frequent). Our `sim/systems/movement.py`
  (iter-2) inherits the choice: Dijkstra for one-off
  paths, Floyd-Warshall for pre-computed small maps.

**What we take.**

- The hex grid coordinate algebra (axial/cube/doubled +
  conversions + distance + line + range + rotation + FOV +
  pixel-to-hex) is the precedent for our phase-5+ spatial
  layer (if hex-based). The formulas are direct.
- The A* pseudo-code (open set + closed set + g/h/f +
  priority queue + tiebreaking) is the precedent for our
  `sim/systems/movement.py` (iter-2). The shape is direct.
- The polygon map generation pipeline (Voronoi + Lloyd's
  relaxation + Perlin noise + watershed + biome assignment
  + noisy edges) is the precedent for our phase-5+ worldgen
  (cf. `azgaar_fmg.md`'s implementation of the same
  algorithm).
- The relational grid abstraction (face/edge/corner + typed
  relations) is the precedent for our phase-5+ spatial
  layer's per-part query interface.
- The "BFS / Dijkstra / A* are a family with different
  heuristics" framing is the precedent for our `sim/systems/
  movement.py` config-time choice of algorithm.

**What we adapt.**

- The articles are interactive HTML5 canvas demos — we
  cannot lift the interactivity; we lift the formulas and
  pseudo-code only.
- The polygon map generation uses `d3-delaunay` / `delaunator`
  for the Voronoi computation — these are JS libraries; we
  adapt by porting the Voronoi algorithm to Python stdlib
  (Python's `geometry` and `math` modules suffice for a
  small N; the canon log records the result, not the
  computation).
- The hex grid coordinate algebra is for hex-based games;
  we adapt by deferring to phase-5+ if we go hex. The phase-0
  tavern is a fixed pack-authored location graph (no grid;
  the formulas are not needed).

**What inspires us.**

- The "BFS / Dijkstra / A* are a family with different
  heuristics" framing is the lesson that **algorithm
  variants are not separate algorithms but parameterized
  instances of one algorithm**. Our `sim/systems/movement.py`
  (iter-2) inherits the framing: one algorithm with a
  config-time choice of heuristic.
- The polygon map generation pipeline is the lesson that
  **a worldgen is a composition of focused passes** (Voronoi
  → relax → elevation → watershed → biomes → noisy edges) —
  the same lesson as Azgaar FMG (`azgaar_fmg.md`) and the
  "small alphabet, deep composition" lesson from
  `brogue.md`. Each pass is a separate algorithm with clear
  inputs and outputs.
- The interactive HTML5 canvas demos are the lesson that
  **algorithm write-ups benefit from interactivity** — the
  reader can play with parameters and see the result
  immediately. Our phase-5+ frontend (if we add one) inherits
  the lesson: the simulation should be explorable, not just
  readable.

**Strengths.**

- The articles are **interactive** (HTML5 canvas demos, JS
  code samples) — the algorithm shapes are clear and
  illustrated; the reader can play with parameters.
- The hex grid page is **the canonical reference** — every
  other hex-grid library (libtcod, rot.js, hexlib, reffy)
  implements the same formulas, derived from this page.
- The A* page is **the most-cited A* tutorial** in game
  development — the canonical write-up that everyone reads
  first.
- The polygon map generation page is **the canonical
  reference** for Voronoi + noise worldgen — the basis for
  Azgaar FMG (`azgaar_fmg.md`) and many other fantasy map
  generators.
- The articles are **well-illustrated** (diagrams,
  animations, code samples) — the algorithm shapes are
  visually clear.
- The site has **been maintained since 2007** (CSS
  Copyright "2007-2026 by Amit J. Patel") — the articles
  are stable; the algorithm shapes are durable.

**Weaknesses.**

- The site has **no explicit license statement** on the
  article pages (verified 2026-08-26). The convention
  adopted here is "treat as CC-BY 4.0" (Amit Patel
  explicitly requests attribution in academic contexts; the
  CSS comment says "I'd appreciate it if you gave me
  credit"). This is a convention, not a license — if Amit
  changes his stance, we re-evaluate.
- The articles are **HTML5 canvas demos** — we cannot lift
  the interactivity; we lift the formulas and pseudo-code
  only.
- The polygon map generation uses **`d3-delaunay` /
  `delaunator`** (JS libraries) for the Voronoi computation
  — not stdlib; we port the algorithm shape to Python
  stdlib.
- The site is **not a code repository** — it's a set of
  articles. There is no `git clone` to inspect the
  implementation; the formulas are in the prose + diagrams.
- The hex grid coordinate algebra is **for hex-based grids**
  — not directly relevant to phase-0 (a location graph, no
  grid). We defer to phase-5+ if we go hex.
- The polygon map generation is **for fantasy-world
  worldgen** — not directly relevant to phase-0 (fixed
  tavern). We defer to phase-5+ worldgen.

**Verdict.** Phase-5 grid-math pattern-only reference (D-012),
mostly positive on algorithm shapes (the hex grid coordinate
algebra, the A* pseudo-code, the polygon map generation
pipeline, the relational grid abstraction, the BFS/Dijkstra/A*
family framing are all direct inheritances), explicitly
negative on no explicit license (treat as CC-BY 4.0 — Amit
Patel requests attribution; convention adopted here, re-
evaluate if stance changes) + HTML5 canvas demos (lift
formulas + pseudo-code only) + d3-delaunay dependency (port
to Python stdlib) + not a code repository (formulas in
prose + diagrams, no git clone to inspect) + hex grid not
directly relevant to phase-0 (defer to phase-5+ if we go
hex) + polygon map generation not directly relevant to
phase-0 (defer to phase-5+ worldgen). The site is the
canonical write-up layer above the libtcod/rot.js
implementations — the algorithm shapes here are the source
of truth that the implementations are concrete instances of.
The "BFS / Dijkstra / A* are a family with different
heuristics" lesson is the inspiration for our `sim/systems/
movement.py` config-time choice of algorithm. The polygon
map generation pipeline is the inspiration for our phase-5+
worldgen (each pass is a separate algorithm with clear
inputs and outputs — the same lesson as Azgaar FMG and
the "small alphabet, deep composition" lesson from
`brogue.md`).

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
