# STATUS — canonsim

Iteration: 0q (owner-requested: ref-8 + ref-9 6-batch — worldgen data donors Azgaar FMG + Natural Earth + GeoNames + grid math pattern-only libtcod + rot.js + Red Blob Games, mostly positive on architecture/shape, some negative on floating-point geometry) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0q is the **ref-8 + ref-9 6-batch iteration** —
six open-licensed worldgen data donor + grid math
pattern-only references (per `REFERENCES.md` §1+§2+§3+§8 —
pattern lifting permitted, port the shape not the syntax
per §0.7 / D-015), each in its own per-ref file:
`docs/ref/azgaar_fmg.md` (280 — Azgaar Fantasy-Map-Generator
four-layer architecture [world data/generators/editors/
renderers — INV-1 inherits: canon log = world data;
`sim/systems/` = generators; `cli/` = editors; `render/` =
renderer] + ordered generator pipeline [30+ side-effecting
imports in `src/generators/index.ts` documenting dependency
order] + `State`/`Campaign` interface shapes [per-entity
record with foreign keys + cached adjacency + embedded
chronology; typed chronology event with temporal bounds +
actor refs — lifted into `content/packs/<pack>/entities.json`
+ `EVENT_SCHEMA.md` §2 `tick` + `actor_id` + `cause` chain]
+ diplomacy chronicle [per-state `diplomacy` array on
designated neutral state[0] — INV-1 fix: global JSONL log,
not per-state field] + re-entrant pipeline [editors as
'interactive generators'; lifted into `Intent` → `Event`
validation front-door in iter-3+ `cli/`] + `.map` save file
[seed + state snapshot — INV-1 split: JSONL log = replay;
SQLite index = snapshot]; explicitly negative on
side-effecting imports [INV-1 fix: emit events, not in-place
mutation] + per-state chronicle [INV-1 fix: global log] +
floating-point Voronoi determinism [INV-2 fix: integer
ticks + `random.Random(seed)`] + catalog row says
'chronology generator' but chronology embedded in
`states-generator.ts` as `generateCampaigns` +
`generateDiplomacy` — minor catalog↔repo drift, fixed in
this per-ref file),
`docs/ref/natural_earth.md` (250 — Natural Earth three-scale
LOD ladder [1:10m/1:50m/1:110m; lifted into phase-5 LOD:
canon log = ground truth; per-NPC projection = mid LOD;
brief cache = top LOD] + `featurecla` closed-enum-on-each-
record [every feature carries its type; lifted into
`entities.json` `entity_type` enum + `EVENT_SCHEMA.md` §2
`event_type` enum] + 155-property `ne_110m_admin_0_countries`
schema [multiple foreign-key systems ISO/FIPS/UN/WB/WOE/
WIKIDATA + 50 localized-name fields `NAME_<lang>` +
precomputed display hints `MAPCOLOR7`/`8`/`9`/`13` +
`POP_EST`/`GDP_MD`/`ECONOMY`/`INCOME_GRP`; lifted into
`entities.json` closed enum + per-type fields (scale
trimmed) + `templates.json` localized name sets + `render/`
display hints on data records] + semantic versioning
[X.Y.Z with documented major/minor/patch boundaries — 'data
layout is the API'; lifted into `schemas/event.schema.json`
`schema_version` + §3 migration rule] + per-theme file
split [one file per domain: physical/cultural/populated_
places/urban_areas; lifted into `content/packs/<pack>/`
per-category file split]; explicitly negative on 155-
property per-record heaviness [trim to what simulation
uses] + floating-point geometry [INV-2 fix: lift metadata
only in phase 0, defer geometry to phase-5+] + dataset
scale [several GB; lift shape, not data] + real-world
dataset [right shape, wrong content — Azgaar FMG + a
future fantasy toponym source are better fitted];
'multiple LODs of same data should be coherent' lesson
[README 'Neatness Counts'] shapes phase-5 LOD ladder),
`docs/ref/geonames.md` (345 — GeoNames 9-class / 684-code
feature-class enum [verified 2026-08-26 against live
`featureCodes_en.txt` dump — `readme.txt` says 645, stale
by 39 codes; classes A/H/L/P/R/S/T/U/V; lifted into
`entities.json` `entity_type` enum as closed enum at top +
per-type refinements; 4 types in phase 0 vs 684 codes in
GeoNames] + `geoname` table per-feature record shape
[`geonameid` PK + `name` UTF-8 + `asciiname` ASCII
fallback + `alternatenames` comma-separated + `latitude`/
`longitude` WGS84 + `feature class` 1-char + `feature
code` varchar(10) + `country code` ISO-3166 2-letter +
`cc2` alternates + `admin1-4` code chain + `population`
bigint + `elevation` int meters + `dem` SRTM3/GTOPO30 +
`timezone` IANA + `modification date` yyyy-MM-dd; flat
per-feature record with PK + display name + ASCII
fallback + multilingual alternates + lat/long + typed
feature + admin hierarchy + population + elevation +
timezone; lifted into `entities.json` per-entity record
shape] + admin-hierarchy code chain [admin1 → admin2 →
admin3 → admin4 + explicit `hierarchy.zip` typed parent/
child file with type 'ADM'/'related'; implicit hierarchy
via codes + explicit hierarchy via separate file; lifted
into `relations.json` P2a pair-keyed relation map] +
`alternatenames` table [`alternateNameId`/`geonameid` FK/
`isolanguage` ISO 639 + variants `zh-CN`/`post`/`iata`/
`icao`/`fr_1793`/`abbr`/`link`/`wkdt`/`alternate name`
UTF-8/`isPreferredName`/`isShortName`/`isColloquial`/
`isHistoric`/`from`/`to` period bounds; per-feature
multilingual name records with type flags + period-of-use
bounds; lifted into `templates.json` localized name sets +
chronicle rename events — a new name is a new record with
`from` tick] + daily delta files [`modifications-<date>.txt`
+ `deletes-<date>.txt` + `alternateNamesModifications-<date>.txt`
+ `alternateNamesDeletes-<date>.txt` — append-only log
discipline; lifted into INV-1 + INV-5 — the log is
append-only, every change is a new event, no edits ever]
+ per-country dump + all-countries dump + city-only subsets
[`cities500/1000/5000/15000.zip` by population threshold];
explicitly negative on tab-delimited format [INV-3 fix:
schema in sidecar, not in code] + floating-point lat/long
[INV-2 fix: lift metadata only in phase 0] + 684-code enum
scale [trim to 4 types in phase 0; many codes like `S.AIRB`
don't apply to pre-industrial fantasy] + `readme.txt` stale
'645 codes' claim [live dump has 684 — documentation lag,
dump is source of truth; logged here as doc↔repo drift
catch] + CC-BY 4.0 attribution sidecar mandatory at
intake + real-world dataset [right shape, wrong content —
Azgaar FMG is the right content]; 'dataset as append-only
log' lesson [daily modifications/deletes deltas] shapes
INV-1 + INV-5),
`docs/ref/libtcod.md` (279 — libtcod FOV algorithm closed
enum [14 algorithms: `FOV_BASIC`/`FOV_DIAMOND`/`FOV_SHADOW`/
`FOV_PERMISSIVE_0..8`/`FOV_RESTRICTIVE`/
`FOV_SYMMETRIC_SHADOWCAST` + `NB_FOV_ALGORITHMS` sentinel;
lifted into `sim/systems/perception.py` iter-3 — algorithm
choice is config-time, recorded in determinism contract] +
`TCOD_MapCell` per-tile state [`transparent` bool input +
`walkable` bool input + `fov` bool output; lifted into
per-tile visibility projection — canon log records 'what
is there', perception system projects 'what can be seen'
given viewer position + sight radius] + A* + Dijkstra
pathfinder interface [graph-search with per-tile cost
function + priority queue using libtcod's `heapq.h`
binary heap primitive — Python's `heapq` stdlib is the
direct equivalent; lifted into `sim/systems/movement.py`
iter-2 — no external dep, D-012] + BSP dungeon generator
[`TCOD_bsp_t` tree node with `x`/`y`/`w`/`h`/`level`/
`position`/`[left, right]` children + `TCOD_bsp_split`
recursive split; deferred to phase-5+ spatial layer,
phase-0 tavern uses fixed grid] + heightmap pipeline
[`TCOD_heightmap_t` 2D float array + `add`/`normalize`/
`add_fbm` Fractal Brownian Motion Perlin/Simplex at
multiple octaves/`scale_fbm`/`dig`/`kernel_transform`;
deferred to phase-5+ worldgen, cf. Azgaar FMG
`heightmap-generator.ts` for same pattern in JS/TS] +
single-instance seeded Mersenne Twister RNG [`TCODRandom`;
lifted into `core/rng.py` iter-1 — Python's
`random.Random(seed)` is Mersenne Twister, INV-2 requires
one instance, no wall-clock] + per-feature file split [one
.h/.hpp pair per feature: `fov.h`/`path.h`/`bsp.h`/`noise.h`/
`heightmap.h`/`mersenne.h`/...; lifted into `sim/systems/`
per-system file layout]; explicitly negative on C/C++
implementation [D-012 fix: port shapes to Python stdlib] +
breadth-irrelevant-to-CLI [`console.h`/`mouse.h`/`image.h`/
`tileset_*.h`/`renderer_xterm.h` not relevant to a CLI
simulation; lift only `sim/systems/` + `core/` + `render/`
parts] + no event sourcing [INV-1 fix: every movement is
a canon event] + no determinism contract [INV-2 fix: one
RNG instance, no wall-clock, sorted iteration, queue key]
+ no content/code split [INV-3 fix: algorithm choice is
config-time, recorded in determinism contract];
BSD-3-Clause [verified 2026-08-26 against `LICENSE.txt` in
`libtcod/libtcod` repo] — permissive license, no friction
at intake; 'permissive license on a reference
implementation is a gift to the ecosystem' lesson — we
lift shapes not syntax, no obligation to ship our code
under same license),
`docs/ref/rot_js.md` (347 — rot.js `EventQueue` min-heap
core [`_time` + `_events` MinHeap<T> + `getTime()`/`clear()`;
canonical event-scheduling primitive; lifted into
`core/queue.py` iter-1 — Python's `heapq` for the heap,
integer tick for time, queue key `(tick, sub_order,
actor_id)` is INV-2 fix for tiebreaking simultaneous
events that rot.js's bare `_time` would collide on] +
scheduler family [abstract `Scheduler<T>` with `_queue:
EventQueue<T>` + `_repeat: T[]` + `_current: any` +
abstract `next()` + 3 concrete subclasses: `Simple`
round-robin insertion-order + `Speed` speed-based with
next event at `_time + 1/speed` (classic roguelike turn
scheduler) + `Action` action-point-based; family of
schedulers extending one abstract base, each defining a
turn discipline; lifted into `core/queue.py` discipline
— queue key IS the discipline, iter-3+ may add speed-
based variant if P2b minimal goal/urge ticker D-021
needs it] + FOV family [abstract `FOV` with `compute(x,
y, R, VisibilityCallback)` + `LightPassesCallback`
boolean per tile + 3 concrete subclasses: `Discrete
Shadowcasting`/`PreciseShadowcasting`/`Recursive
Shadowcasting`; closed family extending one abstract
base, same interface; lifted into `sim/systems/
perception.py` iter-3] + path family [abstract `Path`
with `compute(x1, y1, x2, y2, callback)` + 2 concrete
subclasses: `AStar` with Manhattan heuristic by default +
`Dijkstra`; lifted into `sim/systems/movement.py` iter-2]
+ map family [11 generators extending abstract `Map` with
`create(callback)`: `Arena`/`Cellular`/`Digger`/
`DividedMaze`/`Dungeon`/`EllerMaze`/`Features`/`IceyMaze`/
`Rogue`/`Uniform`; deferred to phase-5+ spatial layer] +
Alea RNG [Baagøe algorithm with `_s0`/`_s1`/`_s2` state +
carry `_c`, seed expansion via `seed*69069 + 1` LCG;
lifted into `core/rng.py` iter-1 — Python's `random.Random
(seed)` Mersenne Twister is the equivalent, INV-2 requires
one instance] + engine game loop wrapper [single-threaded
loop pulling actors from scheduler, calling `actor.act()`,
supports async `result.then`; lifted into `core/runner.py`
iter-1 — sync loop, no async path in phase 0] + per-feature
directory + abstract base + concrete subclasses shape
[`src/scheduler/` + `src/fov/` + `src/path/` + `src/map/`
with `index.ts` aggregating; lifted into `sim/systems/`
per-system file layout]; explicitly negative on TypeScript/
JS implementation [D-012 fix: port shapes to Python stdlib]
+ bare `_time` queue key [INV-2 fix: 3-tuple `(tick,
sub_order, actor_id)` queue key for tiebreaking] + browser
focus [README has `<script>` tag + ES2015 modules + babel+
rollup bundlers + Node.js with `term` layout backend; CLI
not relevant, lift only algorithm shapes] + no event
sourcing [INV-1 fix: every action is a canon event,
`act()` returns Intent that simulator validates] + no
determinism contract [INV-2 fix: one RNG instance, no
wall-clock, sorted iteration, queue key] + no content/
code split [INV-3 fix] + `setSeed` hack `seed = (seed < 1 ?
1/seed : seed)` for fractional seeds [our `random.Random
(seed)` accepts any hashable, integer seed]; 'feature-
complete focused toolkit' lesson [library 'largely
considered feature-complete' per README] shapes our
`sim/systems/` scope [8 systems in phase 0, stops growing
after iter-6 phase gate]; BSD-3-Clause [verified 2026-08-26
from `package.json` `license` field in `ondras/rot.js` repo]
— no friction at intake),
`docs/ref/red_blob_games.md` (312 — Red Blob Games hex
grid coordinate algebra [offset odd-r/even-r/odd-q/even-q +
axial (q, r) + cube (x, y, z with x+y+z=0) + doubled;
conversions offset↔axial↔cube with exact formulas +
distance in cube coords `max(|Δx|, |Δy|, |Δz|)` + line
drawing via cube-coord sampling + rounding + range
walking the cube coordinate ring + rotation by 60° in
cube coords + FOV/line-of-sight via hex-grid line drawing
+ pixel-to-hex conversion for pointy-top + flat-top
orientations with fractional hex intermediate; the
canonical write-up that every hex-grid library (libtcod +
rot.js + hexlib + reffy) implements; deferred to phase-5+
spatial layer if hex-based, phase-0 tavern uses square
grid] + A* pseudo-code [open set + closed set + g cost-
from-start + h heuristic estimate-to-goal + f = g + h +
pick lowest f + expand neighbors + update g and parent;
BFS/Dijkstra/A* family framing with different h choices
[0 for BFS, exact for Dijkstra, estimated for A*];
heuristic functions Manhattan/Euclidean/Chebyshev/Octile
by movement rules; priority queue binary heap +
tiebreaking prefer higher g toward goal; the most-cited
A* tutorial in game dev; lifted into `sim/systems/
movement.py` iter-2 — libtcod + rot.js implementations are
concrete instances of this algorithm] + polygon map
generation pipeline [Voronoi diagram from N random
points via d3-delaunay/delaunator + Lloyd's relaxation
1-2 iterations for uniform distribution + Perlin noise
elevation with radial gradient for island shape +
watershed downhill tracing for rivers + Whittaker biome
diagram elevation × moisture → biome type + noisy edges
for hand-drawn look; the canonical Voronoi+noise worldgen
— Azgaar FMG implements the same algorithm with
additional passes states/cultures/religions; deferred to
phase-5+ worldgen] + relational grid abstraction [faces/
edges/corners with typed relations — a face has edges,
each edge has 2 corners, each corner has 3 edges; same
relational shape for square/hex/triangle grids, different
geometries; grid as graph of parts with relations;
deferred to phase-5+ spatial layer's per-part query
interface] + circle drawing algorithms [midpoint circle
+ Andreev for AoE effects + circular rooms; lifted into
`sim/systems/` iter-2 fire_spread AoE queries] +
distance-to-any single-source Dijkstra + all-pairs Floyd-
Warshall pre-compute [choice: Dijkstra for one-off paths,
Floyd-Warshall for pre-computed small maps; lifted into
`sim/systems/movement.py`]; explicitly negative on no
explicit license statement [site has no license on
article pages — verified 2026-08-26 by inspecting
`/grids/hexagons/` + `/pathfinding/a-star/introduction.html`
+ `/about`; CSS comment 'CSS Copyright 2007-2026 by Amit
J. Patel' is for stylesheet not content; Amit Patel
explicitly requests attribution in academic contexts per
`/blog/`; convention adopted here = treat as CC-BY 4.0,
re-evaluate if stance changes] + HTML5 canvas demos
[lift formulas + pseudo-code only, not interactivity] +
d3-delaunay/delaunator dependency for Voronoi [port to
Python stdlib — Python's `geometry` + `math` modules
suffice for small N] + not a code repository [formulas
in prose + diagrams, no `git clone` to inspect] + hex
grid not directly relevant to phase-0 [defer to phase-5+
if we go hex] + polygon map generation not directly
relevant to phase-0 [defer to phase-5+ worldgen]; the
site is the canonical write-up layer above the libtcod +
rot.js implementations — algorithm shapes here are the
source of truth that implementations are concrete
instances of; 'BFS/Dijkstra/A* are a family with different
heuristics' lesson shapes `sim/systems/movement.py`
config-time choice of algorithm; 'worldgen is composition
of focused passes' lesson [Voronoi → relax → elevation →
watershed → biomes → noisy edges] is the same lesson as
Azgaar FMG and 'small alphabet deep composition' lesson
from `brogue.md`; interactive HTML5 canvas demos lesson
[algorithm write-ups benefit from interactivity] shapes
phase-5+ frontend explorability goal).

All six paraphrased from the open-source corpus + site
per §0.4 / §0.7 (D-015). Licenses verified against
`REFERENCES.md` catalog §1+§2+§3+§8 on 2026-08-26: Azgaar
FMG = MIT (the `Azgaar/Fantasy-Map-Generator` repo LICENSE
file inspected), Natural Earth = public domain (the
`nvkelso/natural-earth-vector` README "free for use in
any type of project" per the project Terms of Use),
GeoNames = CC-BY 4.0 (the
`download.geonames.org/export/dump/readme.txt` "This work
is licensed under a Creative Commons Attribution 4.0
License"), libtcod = BSD-3-Clause (the `libtcod/libtcod`
repo `LICENSE.txt` file inspected, "BSD 3-Clause License"
header), rot.js = BSD-3-Clause (the `ondras/rot.js` repo
`package.json` `"license": "BSD-3-Clause"` field
inspected), Red Blob Games = no explicit license on
article pages (verified by inspecting `/grids/hexagons/`,
`/pathfinding/a-star/introduction.html`, `/about` — CSS
comment "CSS Copyright 2007-2026 by Amit J. Patel" is
stylesheet not content; Amit Patel explicitly requests
attribution in academic contexts per `/blog/`; convention
adopted = treat as CC-BY 4.0, re-evaluate if stance
changes). Catalog §8 has no license column for
knowledge-base sources (Red Blob Games is in §8, not §1-
§7), so the §2 index "CC-BY (treat as)" annotation for
ref-9-c is not catalog↔index drift — the convention is
documented honestly in the per-ref file. License drift
pre-flip caught (KI#6-class pitfall avoided): ref-9-a
and ref-9-b were listed as "BSD" shorthand in §2 index,
but catalog §3 says "BSD-3-Clause" explicitly; fixed in
the same §2 edit that flipped ref-9-a/b/c todo→done. §2
of `docs/REFERENCES_DEEP.md` flips ref-8-a/b/c + ref-9-a/b/c
from todo → done with rich one-line verdicts. AGENT_
NAVIGATION §1 adds the six new files to the `docs/ref/`
list. Per AGENTS §2.5 this is the **sixteenth** docs
iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j,
0k, 0l, 0m, 0n, 0o, 0p, 0q; iter-0d was infra) — the
doc-loop alarm has fired again; the owner explicitly
asked to continue reference work, so the D-022 exception
applies. iter-1 is still the next functional step; no
further docs iterations without a fresh owner request.
Minor catalog↔repo drift: catalog §2 row for Azgaar FMG
says 'chronology generator' but the actual repo at master
has chronology embedded in `states-generator.ts` (no
separate `chronology-generator.ts` file); documented
honestly in the per-ref file (catalog row is the short
version, per-ref file is the long one). Minor doc↔repo
drift: GeoNames `readme.txt` says '645 codes' but the
live dump has 684 codes (stale by 39); documented
honestly in the per-ref file (dump is source of truth).
KI#3, KI#4, KI#5 unchanged.
AGENTS, ROADMAP, MVP_SCOPE, EVENT_SCHEMA, schemas,
TECH_NOTES, SPECS_BACKLOG, CORE_DESIGN_RESEARCH, VISION,
DECISIONS — untouched.

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index.
- INV-2 Determinism: single seeded RNG, no wall-clock, `sorted()` iteration,
  fixed `PYTHONHASHSEED`, queue key `(tick, sub_order, actor_id)`.
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#3 · `expectation_violation` primitive missing — NPC reacts only to presence in `knowledge`, not to absence (purse gone, guard missing). Fix: P2d in `CORE_DESIGN_RESEARCH.md` §6, slated for iter-3.
- KI#4 · balance harness (1000-sim distribution plots of `suspicion` / `fire_spread`) missing — MVP_SCOPE §15 promises an iter-6 baseline but no tool exists. Added as `balance-1` in `docs/TASKS.md` infra backlog.
- KI#5 · runtime state vs test fold not explicitly separated — risk of O(N²) at startup if `fold(log)` is misused as runtime path. D-023 records the rule: runtime = incremental projection; fold = T2 replay only.

## FAQ / Pitfalls

- **Zip upload loses dotfiles and empty dirs.** "Add files via upload" on GitHub
  dropped `.gitignore` (and every dir without tracked files). After any future
  upload: verify `.gitignore` exists and `git status --short` shows no runtime
  artifacts (KI#1).
- **Workspace files ≠ tracked files.** `git status --short` shows changes
  *vs HEAD*, not what is *in HEAD* — a file present in your working directory
  may not be committed at all. After any structural change, run
  `git ls-files <path>` (or `git ls-files | head -50`) to confirm what is
  actually tracked. This is the diagnostic for KI#1-class losses and for
  "the file exists but tests can't find it" surprises.
- **Doc-loop alarm vs owner-requested research.** Sixteen docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0q is the sixteenth docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n,
  0o, 0p, 0q; iter-0d was infra).
- **Substance over line count (D-025) + per-ref split (D-026).** The
  400-line cap was a crutch — iter-0i trimmed real depth (XML element
  lists, event-type enumerations, Mesa pseudo-code, DataCollector
  details) to fit. AGENTS §6 cap is 600, but §6.1 is the real law — filler /
  restatements / linker chains / decorative prose are cut always; named
  systems, real field lists, type enumerations, pseudo-code, per-source
  verdicts are never cut to fit the cap. Over cap after a real cruft pass:
  keep, document in worklog. At iter-0j the single-file
  `docs/REFERENCES_DEEP.md` was 737 lines — 4 deep dives with concrete
  field names and type enumerations justified the breach. At iter-0k the
  same content was split into 5 per-ref files in `docs/ref/` (D-026);
  each is 101–244 lines — under the cap by construction. At iter-0l
  `paradox_scripting.md` is 605 lines — 5 over the cap, justified per
  §6.1 (three games × trigger/MTTH/weight/effect/scope/on_action
  subsystems with real field names and ~150+ on_action IDs). At
  iter-0m three proprietary §10 source files (`rimworld.md` 253,
  `l4d_director.md` 245, `alien_isolation.md` 296) — all under
  cap by construction (the closed-source constraint forces
  field-shape-from-public-talks only, not full enumeration). At
  iter-0n four open-licensed event/narrative grammar family files
  (`wesnoth_wml.md` 244, `endless_sky_dsl.md` 228, `ink.md` 212,
  `tracery.md` 217) — all under cap by construction (the pattern-
  not-content rule §0.7 + the JSON/grammar shape lift keeps each
  file to the mechanics layer only). At iter-0o three open-
  licensed roguelike emergence + micro-sim files
  (`brogue.md` 326, `dcss.md` 360, `keeperrl.md` 444) — all
  under cap by construction (the pattern-not-content rule §0.7
  + the shape-lift keeps each file to the mechanics layer
  only; the larger line counts vs iter-0n reflect the deeper
  RNG/scheduler/queue mechanics these three sources carry —
  the §6.1 substance filter protects the depth). At iter-0p
  three open-licensed LLM-agent precedent files
  (`generative_agents.md` 371, `ai_town.md` 345,
  `letta.md` 353) — all under cap by construction (the
  pattern-not-content rule §0.7 + the shape-lift keeps each
  file to the mechanics layer only; the larger line counts
  vs iter-0n reflect the deeper memory hierarchy + retrieval
  + context-window block manager mechanics these three
  sources carry — the §6.1 substance filter protects the depth). At iter-0q
  six open-licensed worldgen data donor + grid math pattern-only files
  (`azgaar_fmg.md` 280, `natural_earth.md` 250, `geonames.md` 345,
  `libtcod.md` 279, `rot_js.md` 347, `red_blob_games.md` 312) — all
  under cap by construction (the pattern-not-content rule §0.7 + the
  shape-lift keeps each file to the mechanics layer only; the larger
  line counts vs iter-0n reflect the deeper worldgen donor + FOV /
  pathfinding / grid math mechanics these six sources carry — the
  §6.1 substance filter protects the depth).
- **License drift between catalog and index (KI#6, closed iter-0n; pitfall
  persists).** The `REFERENCES_DEEP.md` §2 index table is **not** the source
  of truth for licenses — `REFERENCES.md` (the catalog) is. The index
  restates the license as a one-line convenience column; if the two
  disagree, the catalog wins. iter-0n found two drifts in §2 (ref-5-b
  "CC-BY-SA" vs catalog "GPL-3.0 code; mixed assets"; ref-5-d "CC0"
  vs catalog "Apache-2.0"); both fixed in the same edit. iter-0o
  verified the three new ref-6 rows (AGPL/GPL/GPL shorthand) against
  catalog §2 (AGPL-3.0 (CE) / GPL-2.0+ / GPL-2.0) — no drift this
  iteration. iter-0p caught one drift on ref-7-a (index said
  "(paper)", misleading — the catalog §5 says Apache-2.0 for the
  `joonspk-research/generative_agents` repo; the paper is the academic
  companion, not the license-bearing artefact); fixed in the same §2
  edit that flipped ref-7-a/b/c todo→done with the corrected
  "Apache-2.0 (repo) + paper" annotation. The diagnostic: before
  flipping any ref-N row todo→done, grep the source row in
  `REFERENCES.md` and verify the license column matches the index
  entry. Same pattern as the catalog ↔ synthesis ↔ deep-dive
  anti-drift rule (D-024/D-026): a fact restated in two places
  drifts; the catalog is the owner. Standing pre-flip check added
  to the iter-0o workflow, exercised again in iter-0p, exercised
  again in iter-0q (ref-9-a + ref-9-b "BSD" shorthand → "BSD-3-Clause"
  to match catalog §3 explicit value; ref-9-c Red Blob Games marked as
  "CC-BY (treat as)" — catalog §8 has no license column for knowledge-
  base sources, so this is not catalog↔index drift; the convention is
  documented honestly in the per-ref file, with Amit Patel's explicit
  attribution-request in academic contexts as the basis).
- **Catalog vs deep dives vs synthesis — three places, three jobs.**
  `docs/REFERENCES.md` is the **catalog** (license, URL, phase gating,
  intake rules). `docs/CORE_DESIGN_RESEARCH.md` §2 is the **synthesis**
  (one-line depth primitive + failure mode per source). Per-source
  **deep dives** live in `docs/ref/<source>.md` (one file per source,
  indexed by `docs/REFERENCES_DEEP.md` §2 — D-026; the single-file
  arrangement from D-024 did not scale). Drift rule (AGENTS §3): never
  restate across these three — link only. A future reference detail
  belongs in a per-ref file under `docs/ref/`, not in the catalog or the
  synthesis table.

## Next step

iter-1 · core plumbing is the next functional step: seed, RNG instance, clock,
event queue, JSONL log with header, playscript runner, pack loader for the
drafted `content/tavern_pack/` v0.1. Acceptance criteria in `docs/TASKS.md`.
Owner's blocking answers to Q1–Q3 are absorbed as D-019..D-021 and flip
P2a/P2b and M3/M4/M5 from proposals to accepted iter-3/iter-4/iter-6 scope.
The ref-6 deep dives (Brogue two-stream RNG, DCSS multi-stream RNG +
energy-based scheduler, KeeperRL continuous-time queue + Collective tick
order) are the direct precedents for iter-1 core plumbing. The ref-7 deep
dives (Generative Agents memory stream + retrieval function + reflection
pattern, ai-town reactive-database anti-pattern, letta block-manager +
three-tier memory hierarchy) are the precedents for the phase-1+ brief
layer (track B only, behind the phase-0 gate). The ref-8 deep dives
(Azgaar FMG four-layer architecture + ordered generator pipeline +
`State`/`Campaign` interface shapes, Natural Earth three-scale LOD
ladder + `featurecla` closed enum + semantic versioning, GeoNames
9-class/684-code feature enum + `geoname` table per-feature record +
admin-hierarchy code chain + `alternatenames` table + daily delta
files) are the precedents for phase-5 worldgen + `entities.json` +
`relations.json` P2a + `templates.json` localized name sets + chronicle
rename events. The ref-9 deep dives (libtcod FOV algorithm closed
enum + `TCOD_MapCell` per-tile state + A*/Dijkstra pathfinder +
heightmap pipeline + Mersenne Twister RNG, rot.js `EventQueue`
min-heap + scheduler family [simple/speed/action] + FOV family +
path family + Alea RNG + engine game loop, Red Blob Games hex grid
coordinate algebra + A* pseudo-code + polygon map generation
pipeline [Voronoi + Lloyd + Perlin + watershed + Whittaker biomes +
noisy edges] + relational grid abstraction + Floyd-Warshall pre-
compute) are the precedents for `core/queue.py` + `core/rng.py` +
`core/runner.py` iter-1 plumbing + `sim/systems/perception.py` +
`sim/systems/movement.py` iter-2/iter-3 systems. The remaining
backlog is ref-10 (entt + Bevy + EventStore — ECS scheduling + event-
sourcing stream/projection patterns) and ref-11 (SQLite FTS5 + DuckDB
+ sqlite-vec — storage layer candidates; depends on phase-4 retrieval
decision); both are phase-5+, both can be deferred until after iter-1.
