# Brogue (BrogueCE) · `REFERENCES.md` §2 + §14 · AGPL-3.0 · phase 5 (roguelike emergence)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is open AGPL-3.0 — code is
> in scope per §0.4; copying text into our repo would force AGPL
> on our files, so we port the shape (layered tile map,
> two-stream RNG, recording header) into JSON + stdlib Python,
> never the C syntax. Reference repo: `tmewett/BrogueCE`
> (Community Edition; original `BrogueCE` org superseded ~2022).
> Corpus inspected: `src/brogue/Time.c` (2644 lines),
> `src/brogue/Light.c` (412 lines), `src/brogue/Math.c` (288 lines),
> `src/brogue/Recordings.c` (1519 lines), `src/brogue/Rogue.h`,
> `src/brogue/Globals.h`, `test/seed_catalogs/`.

**What it is.** Brogue is a single-dungeon roguelike descended
from the original 2009 Brian Walker release; the Community Edition
(`BrogueCE`) is the actively maintained fork. The game is built
around one principle: **a small rule alphabet producing emergent
depth** — fire, gas, water, light, terrain, and creatures combine
into chains of consequences (a thrown potion ignites a gas cloud
which burns the grass which spreads to the bridge which collapses
under the player). No social/epistemic layer; the entire game is
environmental. The mechanics are the precedent for our phase-5
`fire_spread` and `suspicion`/`gas`-style emergent chains (MVP_SCOPE
§15 metric baseline, KI#4 balance harness).

**Concrete mechanics.**

- **Layered dungeon model — `pmap[x][y].layers[layer]`.** Every
  cell is an array of terrain layers (`DUNGEON`, `GAS`, `SURFACE`,
  `ITEMS`, `CREATURES`...). The same coordinate can host a floor
  (`DUNGEON`), a gas cloud (`GAS` layer with a `volume` field),
  a fire (`DF_*` dungeon feature), an item, and a creature — all
  simultaneously. Operations are per-layer (`promoteTile(x, y,
  layer, useFireDF)`), not per-tile. The pattern: **the layer is
  the noun; the tile is a stack**. Direct echo of Wesnoth's
  tag-tree (`wesnoth_wml.md`) and DCSS's per-feature layers
  (`dcss.md`); our content packs (`content/tavern_pack/`) carry
  the same shape in JSON.
- **Two-stream RNG — `RNG_SUBSTANTIVE` / `RNG_COSMETIC`.** `Math.c`
  declares `static ranctx RNGState[2];` — two parallel Bob Jenkins
  `ranval` PRNG instances, both seeded identically from the user
  seed via `seedRandomGenerator`. The `rogue.RNG` field selects
  the active stream; `assureCosmeticRNG` is a macro that swaps
  to cosmetic, runs a block, restores. `brogueAssert(rogue.RNG
  == RNG_SUBSTANTIVE)` guards critical sim paths (e.g.,
  `paintLight` line 62) — the assertion fires if a cosmetic
  roll leaks into substantive state. Only substantive rolls
  increment `randomNumbersGenerated` (used by replay verification).
  The pattern: **separate streams for state-bearing vs
  display-only randomness**; cosmetic rolls cannot desync the
  canonical replay. INV-2 inherits this shape — same single-seed
  rule, same two-stream discipline (one stream for sim, one
  for the chronicle renderer). DCSS's `rng_type` enum is the
  same idea scaled to N subsystems (`dcss.md`).
- **`promoteTile` — generic per-layer state transition.**
  Every terrain layer has `tileCatalog[t].promoteChance` and
  `tileCatalog[t].fireType`/`promoteType`. A tile promotes when:
  (a) `rand_range(0, 10000) < promoteChance` — stochastic
  tick; (b) `exposeTileToFire` is called on a flammable layer
  that isn't extinguished by a higher-priority layer; (c) the
  tile is `TM_IS_WIRED` and an adjacent tile in the same
  machine receives power — `IS_POWERED` flag propagates
  through `activateMachine(machineNumber)`. The `useFireDF`
  boolean selects between the fire-promote type (gas burning
  → fire DF) and the regular promote type (grass growing into
  a bloodwort stalk). The pattern: **one transition primitive
  + a few flag-gated trigger sources** — fire, electricity,
  wiring, time. Our `actions.json` `effect` family inherits
  the same shape (one transition primitive + trigger sources).
- **`updateVolumetricMedia` — gas diffusion with stochastic
  rounding.** Each tick, for every cell: sum the gas volume of
  itself plus all non-`T_OBSTRUCTS_GAS` neighbours; divide by
  the neighbour count; the remainder is added with probability
  `rand_range(0, numSpaces - 1) < (sum % numSpaces)`. Gases
  that encounter `T_AUTO_DESCENT` (chasm/trap door) get an
  extra "escapes the level" space in the divisor. Two gases
  on the same cell: the highest-volume neighbour's type wins,
  but the loser is capped to volume 3 to prevent "crazy
  interactions". `TM_GAS_DISSIPATES` and
  `TM_GAS_DISSIPATES_QUICKLY` flags trigger extra volume
  decay with 20% / 50% probability per tick. The pattern:
  **simple rules + stochastic rounding = emergent diffusion**;
  no Navier-Stokes, no fancy physics. Our `rules.json`
  `fire_spread` is the same shape (D-014 fire spread in
  MVP_SCOPE §15).
- **`exposeTileToFire` — fire propagation with extinguishing
  priority.** A tile has a `T_IS_FLAMMABLE` flag and an
  `exposedToFire` counter (max 12 exposures per turn to
  prevent runaway). The function walks all layers, finds the
  extinguishing layer with the lowest `drawPriority`
  (`TM_EXTINGUISHES_FIRE` flag), then picks the most-flammable
  layer that is either gas or higher-priority than the best
  extinguisher. If found, `spawnDungeonFeature` fires the
  `fireType` of that layer (e.g., `DF_PLAIN_FIRE`). Water
  (`Time.c` line 199) puts out fire — `TM_EXTINGUISHES_FIRE`
  is set on water tiles. The pattern: **a small per-layer
  priority comparison** is sufficient to model fire-vs-water-
  vs-gas-burning interactions. No layered physical model —
  just a priority comparison.
- **Light model — fixed-point RGB + `paintLight` + `IS_IN_SHADOW`.**
  `Light.c` runs the lighting pass on a `tmap[x][y].light[3]`
  array (three color components stored as `fixpt` — Brogue's
  home-grown fixed-point arithmetic; see `fp_sqrt` for the
  bisection sqrt). `paintLight` zeros a local grid, calls
  `getFOVMask` to compute which cells are in line-of-sight of
  the light source (terrain `T_OBSTRUCTS_VISION` occludes),
  then for each in-LOS cell adds `colorComponents[k] *
  lightMultiplier / 100` where `lightMultiplier = 100 - (100
  - fadeToPercent) * fp_sqrt(distance) / radius`. The
  `IS_IN_SHADOW` flag is set on every cell at the start,
  cleared by light sources. The miner's light is the player's
  intrinsic light, with `radialFadeToPercent = 35 + max(0,
  min(65, lightMultiplier * 5)) * fraction / FP_FACTOR`.
  Flares (`newFlare`, `animateFlares`) are transient fading
  lights with `coeffChangeAmount` per frame, geometric decay
  (`coeffChangeAmount = coeffChangeAmount * 12 / 10`). The
  pattern: **light = additive RGB accumulation over a FOV
  mask**; no raytracing, no photon mapping. Our `render/`
  chronicle (iter-5) inherits the additive-accumulator model
  for "what's visible to whom" knowledge records.
- **`updateEnvironment` — per-tick environment tick.** Called
  once per `absoluteTurnNumber` increment (Time.c line 2419
  inside the player's `do` loop). Steps: (a) `monstersFall`
  (creatures over chasms fall); (b) reset `exposedToFire`
  counters; (c) check if any gas exists; if so, run
  `updateVolumetricMedia` **twice** (the double-pass keeps
  generations distinct — the comment at line 1441 explains
  why: "two passes to keep generations distinct"); (d) random
  tile promotions (two passes — first pass marks
  `promotions[i][j]` bitfield, second pass executes the
  promotions; this prevents a promote from triggering another
  promote in the same tick); (e) clear `CAUGHT_FIRE_THIS_TURN`
  flags and pressure plates; (f) update fire — for every
  `T_IS_FIRE` tile, call `exposeTileToFire` on itself and
  all 4 cardinal neighbours. The pattern: **multi-pass tick
  with strict pass separation**; one pass reads, the next
  pass writes — no mid-tick cascades. INV-2 deterministic
  iteration (sorted()) inherits this discipline.
- **Recording header — 36 bytes, no wall-clock.**
  `Recordings.c` writes a 36-byte header at the start of every
  recording file: bytes 0-14 = version string (15 chars max);
  byte 15 = mode (normal/easy); bytes 16-23 = seed (uint64);
  bytes 24-27 = player turn number (uint32); bytes 28-31 =
  deepest level (uint32); bytes 32-35 = length of playback
  file (uint32). After the header, every player input is
  recorded as 3-4 bytes: keystroke events = (type, keystroke,
  modifiers); mouse events = (type, x, y, modifiers). The
  recording is **byte-identical replayable** across the same
  version + same OS — `recordingVersionString` is checked on
  load (line 510) and the engine refuses to replay a recording
  made with a different version. The pattern: **the recording
  header is the entire save-compat surface**; no timestamps,
  no machine IDs. Our JSONL log header (`EVENT_SCHEMA.md` §1)
  inherits the same shape — seed, python_version, schema_version,
  commit, pack — no wall-clock anywhere (D-004). Brogue's
  `seedRandomGenerator(0)` derives the seed from `time(NULL) -
  1352700000` only when the user passes 0; this wall-clock use
  is the one place determinism is loosened, and only for the
  user-facing "give me a random dungeon" path — never for
  replay.
- **`randomNumbersGenerated` counter + AUDIT_RNG build flag.**
  In `Math.c` line 165, every substantive `rand_range` call
  increments the counter; in the `AUDIT_RNG` debug build
  (lines 140-158), every call also logs `#N, lo to hi: retval`
  to an RNG log. The pattern: **randomness is auditable** —
  a debug build produces a full trace of every substantive
  roll, and the count is a fingerprint of the simulation
  state. Our `core/rng.py` (iter-1) inherits this — a debug
  counter on the substantive stream, peekable state for T1
  byte-identical replay tests.

**What we take.**

- **The two-stream RNG discipline (`RNG_SUBSTANTIVE` /
  `RNG_COSMETIC`).** Exactly our INV-2 single-seed rule +
  two streams: one for state-bearing rolls (the simulation),
  one for display-only rolls (the chronicle renderer, the
  UI). Cosmetic rolls cannot desync the canonical replay.
  Same `assureCosmeticRNG` shape — a context manager that
  swaps streams and restores.
- **The recording-header shape (no wall-clock, version +
  seed + counters).** Exactly our JSONL log header
  (`EVENT_SCHEMA.md` §1, D-004). Brogue's 36-byte header
  carries version, mode, seed, turn, level, length — our
  JSONL header carries seed, python_version, schema_version,
  commit, pack. Same shape, different fields.
- **The `promoteTile` + flag-gated trigger pattern.** One
  generic transition primitive + a small set of flag-gated
  trigger sources (`TM_IS_FLAMMABLE`,
  `TM_PROMOTES_ON_ELECTRICITY`, `TM_IS_WIRED`,
  `promoteChance` stochastic tick). Our `actions.json`
  `effect` family and `rules.json` `fire_spread` inherit
  the same shape.
- **The layered dungeon model `layers[layer]`.** Exactly
  our cell-stack concept for `MVP_SCOPE.md` §10 knowledge
  records — a cell can host a creature, a fire, a gas, an
  item, a visibility flag simultaneously. The layer is the
  noun.
- **The `randomNumbersGenerated` audit counter.** Exactly
  our debug-build counter on the substantive RNG stream —
  T1 byte-identical replay tests can compare counter values
  across runs as a fingerprint.

**What we adapt.**

- **Brogue's C `ranval` PRNG → Python `random.Random(seed)`
  with `random.Random(seed)` for the cosmetic stream.**
  Brogue uses a custom Bob Jenkins PRNG for legacy reasons;
  our INV-2 + stdlib-only (D-012) choice is `random.Random`.
  The two-stream discipline is ported; the algorithm is not.
- **Brogue's per-cell fixed-point arithmetic → Python
  floats + JSON integers.** Brogue uses fixed-point (`fixpt`)
  because it predates widespread float determinism; our
  INV-2 + D-004 (no wall-clock) + PYTHONHASHSEED=0 gives
  us float determinism on the same environment. The
  adaptation: floats for `lightMultiplier` and `volume`,
  integers for tick counts and seeds.
- **Brogue's recording file format → our JSONL log.** Brogue
  records every player input as 3-4 bytes; we record every
  state change as a JSONL event. The header shape is ported;
  the body shape is different — we log state changes
  (events), not inputs (intent). The split is INTENT_SCHEMA
  vs EVENT_SCHEMA (`SPECS_BACKLOG.md`).
- **Brogue's `sighted` event implicit in `getFOVMask` → our
  `seen` knowledge channel on a perception tick.** Brogue
  computes visibility per-tick and uses it for rendering;
  we compute it per-tick and emit `seen` knowledge records
  (`MVP_SCOPE.md` §10). Same FOV-mask shape, different
  output (we write to the log, not the screen).
- **Brogue's seed derivation from `time(NULL)` for the
  user-facing "random dungeon" → our explicit seed argument
  only.** Brogue allows seed=0 to mean "give me a random
  one"; we never do this — the user must pass an integer
  seed. INV-2 is stricter; the wall-clock fallback is the
  one thing we do not port.

**What inspires us.** The **"small alphabet, deep
composition"** lesson. Brogue proves that ~5 environmental
rules (fire spreads, gas diffuses, water extinguishes,
terrain promotes, light accumulates) compose into the
emergent chains that make the game famous — a thrown potion
ignites a gas cloud which burns the grass which spreads to
the bridge which collapses under the player. No social
layer, no AI planner, no LLM. The lesson for us: depth is
O(intersections between primitives), not O(content volume)
(CORE_DESIGN_RESEARCH §3). The fire/gas/water/light
quartet is the precedent for our phase-5 `fire_spread`
metric baseline (KI#4) — the same four-rule alphabet,
ported to JSON + stdlib Python.

**Strengths.**

- Public AGPL-3.0 — full source readable; the codebase is
  ~41k lines of C, well-organised (`src/brogue/` for the
  engine, `src/platform/` for I/O, `src/variants/` for
  game-mode variants). Pattern-lifting is permitted per
  `REFERENCES.md` §0.4.
- The two-stream RNG discipline is the cleanest public
  reference for "state-bearing vs display-only randomness"
  — `brogueAssert(rogue.RNG == RNG_SUBSTANTIVE)` is a
  one-line guard that we lift verbatim into a Python
  context manager.
- The 36-byte recording header is the cleanest public
  reference for "no-wall-clock save-compat surface". Our
  JSONL log header is structurally identical.
- The seed-catalog test harness (`test/seed_catalogs/`,
  `test/compare_seed_catalog.py`) is the precedent for
  T1 byte-identical replay — Brogue ships known-good seed
  outputs and a regression script that diffs current runs
  against the catalog. Our T1 inherits this shape.
- The multi-pass environment tick (read pass, write pass,
  cleanup pass) is the precedent for INV-2 deterministic
  iteration — no mid-tick cascade, no order-dependence
  on the iteration sequence within a pass.

**Weaknesses.**

- No social/epistemic layer — Brogue is purely
  environmental. Our 8 systems × intersection matrix
  (`MVP_SCOPE.md` §6) adds the social/epistemic axis
  Brogue lacks; the cross-axis intersections are where
  our depth lives (`CORE_DESIGN_RESEARCH.md` §3).
- No event log — runtime state lives in the `pmap` array
  (in-memory). Our INV-1 (state = fold(log)) is the
  inverse; the in-memory `pmap` is the amnesia anti-pattern
  on a per-cell scale (`mesa.md`).
- The C code is heavily pointer-arithmetic; the layered
  model is `pmap[i][j].layers[layer]` with manual array
  indexing. Our JSON + Python adaptation is cleaner but
  loses the cache locality that lets Brogue run on a
  100×50 grid at 60fps.
- `time(NULL)` seed fallback is the one wall-clock use;
  we explicitly do not port it (INV-2 stricter).
- No knowledge records — Brogue's `seen` is implicit in
  `IN_FIELD_OF_VIEW`/`ANY_KIND_OF_VISIBLE` flags on the
  pmap. Our `seen` knowledge channel is a per-NPC event
  log; Brogue has no per-NPC epistemic state.
- The `IS_IN_SHADOW` flag is a one-bit per-cell state
  that gets cleared by every light source — a global
  mask, not a per-observer mask. Our `knowledge` records
  carry per-NPC epistemic state; Brogue has no analogue.

**Verdict.** Phase-5 environmental-emergence reference,
almost entirely positive on the two-stream RNG discipline
(`RNG_SUBSTANTIVE`/`RNG_COSMETIC`), the no-wall-clock
recording header, the multi-pass environment tick, and
the layered dungeon model — all direct inheritances into
our INV-2 / D-004 / iter-1 core plumbing. The `promoteTile`
+ flag-gated trigger pattern is the precedent for our
`actions.json` `effect` family. Explicitly negative on
porting the C PRNG (stdlib `random.Random` instead), the
`time(NULL)` seed fallback (we never loosen INV-2), and
the in-memory `pmap` state model (our INV-1 JSONL log is
the inverse). Brogue is the canonical proof that ~5
environmental rules compose into emergent chains — the
precedent that depth is O(intersections between primitives),
not O(content volume).

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
