# KeeperRL · `REFERENCES.md` §2 + §14 · GPL-2.0 · phase 5 (roguelike emergence + micro-sim)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is open GPL-2.0 — code is
> in scope per §0.4; copying text into our repo would force GPL on
> our files, so we port the shape (continuous-time queue,
> collective-tick loop, cereal binary serialisation, external-enemy
> wave planner) into JSON + stdlib Python, never the C++ syntax.
> Reference repo: `miki151/keeperrl`. Corpus inspected:
> `time_queue.h` + `time_queue.cpp` (232 lines),
> `game_time.h`, `model.cpp` + `model.h`, `level.cpp`,
> `collective.cpp` (1862 lines), `immigration.cpp`,
> `external_enemies.cpp` (154 lines), `fire.cpp` + `fire.h`,
> `monster_ai.h`, `util.h` lines 700-886 (RandomGen class),
> `util.cpp` lines 1-130, `game_event.h` (171 lines),
> `data_free/game_config/creatures.txt`.

**What it is.** KeeperRL is a dwarf-fortress-style
micro-simulation in a roguelike shell, created by Michal
Brzozowski (miki151) starting 2013. Public GPL-2.0; the
codebase is ~500 C++ files, organised by system (model,
collective, level, creature, task, furniture). The game
combines: a continuous-time `LocalTime`/`GlobalTime`
queue, a per-tick collective loop (immigration, rebellion,
guard tasks, minion promotions), a binary `cereal`
serialisation, and a pre-computed external-enemy wave
planner. All four are the precedents for our phase-3
director + iter-3 P2a NPC↔NPC relations + iter-4
`seeded_hooks` (D-021). The catalog note ("creature
micro-simulation + base + world map") undersells the
architecture — the queue and the collective loop are the
load-bearing patterns.

**Concrete mechanics.**

- **Continuous-time queue — `map<ExtendedTime, Queue>`.**
  `time_queue.h` declares `class TimeQueue` with a
  `map<ExtendedTime, Queue> SERIAL(queue)` and a
  `EntityMap<Creature, ExtendedTime> SERIAL(timeMap)`.
  `ExtendedTime` is `{ LocalTime time; bool extraTurn }`
  — the `extraTurn` flag lets a creature act twice in the
  same tick without advancing the local clock (used by
  `makeExtraMove`, e.g., for "haste" effects). The
  operator `<` orders by time first, then by `extraTurn`
  (a non-extra turn sorts before an extra turn at the same
  time). The queue is a `map`, not a `heapq` — the keys
  are sorted, and `getNextCreature(maxTime)` walks from
  the beginning. The pattern: **continuous-time priority
  queue with a per-creature time map** — same shape as
  our `core/queue.py` (iter-1) keyed `(tick, sub_order,
  actor_id)`. The differences: KeeperRL uses a `map`,
  we use `heapq`; KeeperRL's `LocalTime` is a templated
  `GameTime<Tag>` (separate `LocalTime` and `GlobalTime`
  types — same integer count, different tags); we use a
  single integer tick. The shape is the same.
- **`Queue` with `players` and `nonPlayers` deques.**
  Inside `TimeQueue::Queue`, two `deque<Creature*>`
  lists: `players` (the player's creatures, including
  avatars) and `nonPlayers` (NPCs). `front()` returns
  the player front if any, else the non-player front.
  `pushFront` is used by `moveNow` — a creature that
  gets a "move now" effect is placed at the front of
  its deque. The pattern: **players and non-players are
  in the same queue but ordered separately** — the player
  goes first within a tick. Our `sub_order` field in the
  queue key `(tick, sub_order, actor_id)` is the same
  idea — the player's intents get `sub_order = 0`, NPCs
  get `sub_order = 1..N` in `sorted()` order. Same shape,
  different storage.
- **`compareOrder` — tie-breaking by `orderMap`.** When
  two creatures have the same `ExtendedTime`, the
  `Queue::orderMap` (a per-creature integer counter,
  incremented on `push` and decremented on `pushFront`)
  breaks ties. `orderMap.getOrFail(c1) < orderMap.get
  OrFail(c2)` returns the comparison. The pattern:
  **deterministic tie-breaking by insertion-order
  counter** — same shape as our `actor_id` tiebreaker in
  `(tick, sub_order, actor_id)`. The counter is per-queue-
  position, not per-creature; we use a global
  `actor_id` (stable per-creature identifier), which is
  simpler but loses the per-queue-position granularity.
- **`Model::update(double totalTime)` — the tick driver.**
  `model.cpp` lines 116-141. The driver: `if (Creature*
  creature = timeQueue->getNextCreature(totalTime))` —
  pull the next creature whose time is ≤ `totalTime`.
  While `totalTime > lastTick.getDouble()`, increment
  `lastTick += 1_visible` and call `tick(lastTick)` —
  this runs the per-tick collective+level+creature update
  for every integer `LocalTime` boundary crossed. Then
  `creature->makeMove()` — the creature acts. The
  pattern: **the tick driver advances the simulation in
  two phases per iteration — tick all systems at integer
  boundaries, then process one creature's action**. Our
  `core/loop.py` (iter-1) inherits the same shape — pull
  next event, advance tick, run system hooks, process
  the event.
- **`Model::tick(LocalTime)` — the per-tick update.**
  `model.cpp` lines 143-163. Five steps: (a) tick every
  creature (`c->tick()`); (b) tick every level
  (`l->tick()`); (c) tick every collective
  (`col->tick()`); (d) rebuild the territory map
  (`l->territory[v] = nullptr` then reassign per
  collective); (e) update external enemies
  (`externalEnemies->update(getGroundLevel(), time)`).
  The pattern: **system-tick order is fixed:
  creatures → levels → collectives → territory →
  external** — same shape as our `MVP_SCOPE.md` §5
  eight-systems tick order (knowledge → relations →
  intent → action → director → consequence → ...).
  INV-2 deterministic iteration (`sorted()`) is the
  binding constraint.
- **`Collective::tick()` — the collective update.**
  `collective.cpp` lines 616-629. Eight steps:
  `updateBorderTiles()`, `considerRebellion()`,
  `updateGuardTasks()`, `updateMinionPromotions()`,
  `dangerLevelCache = none`, `control->tick()`,
  `zones->tick()`, `taskMap->tick()`,
  `constructions->clearUnsupportedFurniturePlans()`,
  `dancing->setArea(...)`, `if (config->getWarnings()
  && Random.roll(5)) warnings->considerWarnings(this)`.
  The pattern: **a per-tick collective is a fixed-
  sequence of named subsystem updates** — same shape
  as our `core/director.py` (iter-4) tick. The
  subsystems (border, rebellion, guard tasks, minion
  promotions, danger cache, control, zones, task map,
  constructions, dancing, warnings) are domain-specific;
  the shape (fixed-sequence per-tick subsystem updates)
  is the precedent.
- **`getRebellionProbability()` — emergent social
  dynamics from a few numbers.** `collective.cpp` lines
  526-538. The rebellion probability is a function of
  the prisoner/fighter ratio: if `numPrisoners <= 4`,
  return 0; if `numFighters == 0`, return 1; otherwise
  `min(1, max(0, (ratio - 0.5) / 1.0))`. The pattern:
  **a small numeric formula models a complex social
  phenomenon** — rebellion is just (prisoners -
  threshold) / fighters. No state machine, no
  per-prisoner psychology. Our `rules.json` (iter-2)
  inherits the same shape — suspicion, trust, and
  rebellion are small formulas over the existing
  knowledge records, not new systems.
- **`considerRebellion()` — stochastic trigger from the
  probability.** Line 541: `if (Random.chance(p /
  1000))`. The probability is computed per-tick; the
  trigger is `Random.chance(p / 1000)` (i.e., the
  probability is per-mille, and the actual roll happens
  once per tick). The pattern: **probabilistic events
  are computed per-tick and rolled per-tick** — same
  shape as our `seeded_hooks` (MVP_SCOPE §5), which are
  computed per-tick and trigger when the random roll
  beats the threshold. No MTTH (mean-time-to-happen,
  Paradox pattern, `paradox_scripting.md`); pure
  per-tick probability.
- **`ExternalEnemies` — pre-computed wave planner.**
  `external_enemies.cpp` lines 25-54. The constructor
  generates **500 waves at worldgen time** with
  `firstAttackDelay = 1800`, `attackInterval = 1200`,
  `attackVariation = 450` — each wave's attack time is
  `firstAttackDelay + max(0, i * attackInterval +
  random.get(-attackVariation, attackVariation + 1))`.
  The waves are stored in `vector<EnemyEvent> waves`
  and dispatched by `popNextWave(localTime)` which
  returns the next wave whose `attackTime <= localTime`.
  The pattern: **the wave schedule is computed once at
  worldgen, not per-tick** — the schedule is data, the
  dispatcher is a small `if`. Our `seeded_hooks`
  (MVP_SCOPE §5, `directors on|off` AC T8) inherit the
  same shape — hooks are computed at event time (D-005)
  and dispatched when their trigger fires; the
  consequence planner is the precedent for the
  `seeded_hooks` release logic.
- **`external_enemies_type` enum — wave-planner modes.**
  `FROM_START` (waves start at worldgen),
  `AFTER_WINNING` (waves start when the game is won —
  post-game endless mode). The pattern: **the wave
  planner has a small enum of modes** — same shape as
  our `directors on|off` switch (T8 director-off A/B),
  which is a 2-mode enum. Same shape, smaller.
- **`GameEvent` — variant-sum-typed event.**
  `game_event.h` lines 16-170 declares a `VARIANT_TYPES_
  LIST` X-macro list of 24 event types: `CreatureMoved`,
  `CreatureKilled`, `ItemsPickedUp`, `ItemsDropped`,
  `ItemsAppeared`, `ItemsPillaged`, `Projectile`,
  `ConqueredEnemy`, `WonGame`, `RetiredGame`,
  `TechbookRead`, `Alarm`, `CreatureTortured`,
  `CreatureStunned`, `CreatureAttacked`,
  `TrapDisarmed`, `FurnitureRemoved`, `ItemsOwned`,
  `CreatureEvent`, `ItemStolen`, `VisibilityChanged`,
  `MovementChanged`, `LeaderWounded`, `FX`. The
  `gen_variant.h` X-macro generates the C++ variant
  class. The pattern: **events are a closed variant of
  named structs with per-event fields** — same shape as
  our `EVENT_SCHEMA.md` `event_type` enum + per-type
  fields. The 24-event closed list is the precedent for
  our closed event vocabulary (the tavern pack has ~12
  events for phase 0; KeeperRL has 24 for the full game
  scope).
- **`RandomGen` — single-instance RNG.** `util.h` lines
  702-886 + `util.cpp` lines 22-115. The class wraps a
  single `std::mt19937 generator` field, seeded by
  `RandomGen::init(int seed)`. There's a global
  `extern RandomGen Random;` — one instance per
  program. The pattern: **single-instance RNG, globally
  accessible** — same shape as our INV-2 single
  `random.Random(seed)` instance. No multi-stream
  discipline (Brogue's two-stream, DCSS's N-stream);
  KeeperRL has one stream and lives with it. We inherit
  the single-instance discipline but add the two-stream
  separation (Brogue's contribution).
- **`cereal` binary serialisation.** `serialization.h`
  declares `typedef cereal::BinaryInputArchive
  InputArchive;` — the entire game state (model, levels,
  collectives, creatures, items, time queue, etc.) is
  serialised via `cereal`'s binary archive. The pattern:
  **the save format is binary, not human-readable** —
  the inverse of our JSONL log (INV-1: state = fold(log),
  the log is human-readable). The trade-off: KeeperRL's
  saves are smaller and faster; ours are auditable and
  replayable by hand.
- **Data-driven content — `data_free/game_config/*.txt`.**
  `creatures.txt` is 5660 lines of creature definitions
  in a custom DSL: `"KEEPER_MAGE" { viewId = { "keeper1"
  }; body = { type = Humanoid LARGE }; attr = { DAMAGE
  12 DEFENSE 12 SPELL_DAMAGE 20 LABORATORY 10 };
  permanentEffects = { RIDER 1 }; maxLevelIncrease =
  { DAMAGE 7 SPELL_DAMAGE 12 }; aiType = RANGED;
  spellSchools = { "mage" }; spells = { "healing" };
  inventory = { { "Robe"} { "WoodenStaff" } } }`. The
  pattern: **content is data, not code** — same shape
  as our `content/tavern_pack/*.json`. The DSL supports
  `inherit` (line 60: `"ADVENTURER_MAGE" inherit
  "KEEPER_MAGE"`) — same shape as C:DDA's
  `copy-from` (`cdda_data_json.md`). The DSL is custom-
  parsed; our `content/tavern_pack/*.json` is JSON
  Schema-validated (D-023).
- **`Fire` — minimal state machine for tile fire.**
  `fire.h` declares `class Fire { int burnTime;
  optional<int> burnState; }`. `tick()` increments
  `burnState` if not null and `< burnTime`. `set()` sets
  `burnState = 0` (starts burning). `isBurning()` =
  `burnState && *burnState < burnTime`. `isBurntOut()`
  = `burnTime == burnState`. The pattern: **fire as a
  minimal optional-state machine** — same shape as our
  `rules.json` `fire_spread` tile state (burnable,
  burning, burnt-out). 36 lines of C++; our adaptation
  is 3 lines of JSON.
- **`SunlightInfo` — per-tick sunlight cycle.** The
  `sunlight_info.cpp` file implements a day/night cycle
  that affects vision and creature behaviour. The
  pattern: **per-tick environmental state with
  downstream effects on perception** — same shape as
  our future `seen`/`visible` channels on knowledge
  records (phase 3+).

**What we take.**

- **The continuous-time queue shape (`map<ExtendedTime,
  Queue>`).** Our `core/queue.py` (iter-1) inherits the
  shape — `(tick, sub_order, actor_id)` queue key, one
  creature per pop, tick advances per-system. We use
  `heapq` instead of `map` for O(1) push; the shape is
  the same.
- **The `Model::tick` per-tick update order (creatures →
  levels → collectives → territory → external).** Our
  `MVP_SCOPE.md` §5 eight-systems tick order inherits
  the shape — fixed-sequence per-tick subsystem updates.
- **The `getRebellionProbability` small-formula social
  dynamics.** Our `rules.json` (iter-2) inherits the
  shape — suspicion, trust, rebellion are small
  formulas over existing knowledge records, not new
  systems.
- **The `ExternalEnemies` pre-computed wave planner.**
  Our `seeded_hooks` (MVP_SCOPE §5) inherit the shape —
  hooks are computed at event time (D-005 consequence
  planner) and dispatched when their trigger fires.
- **The `GameEvent` closed variant + per-event fields.**
  Our `EVENT_SCHEMA.md` `event_type` enum + per-type
  fields inherits the shape. The 24-event closed list
  is the precedent for our closed event vocabulary.
- **The single-instance RNG (`extern RandomGen Random`).**
  Our INV-2 single `random.Random(seed)` instance
  inherits the shape. We add the two-stream separation
  (Brogue's contribution, `brogue.md`).
- **The data-driven content DSL with `inherit`.** Our
  `content/tavern_pack/*.json` inherits the shape
  (with `copy-from` instead of `inherit`, same idea).
  JSON Schema validation (D-023) is the improvement.

**What we adapt.**

- **KeeperRL's `std::mt19937` → Python `random.Random`.**
  Same single-instance discipline; the algorithm is
  Mersenne Twister in both cases (Python's
  `random.Random` uses MT by default). The adaptation
  is the language, not the shape.
- **KeeperRL's `map<ExtendedTime, Queue>` → our
  `heapq` with `(tick, sub_order, actor_id)` keys.**
  KeeperRL uses a `map` for ordered iteration; we use
  `heapq` for O(1) push. The shape is the same; the
  storage is different. Our queue key collapses
  KeeperRL's `ExtendedTime { LocalTime + extraTurn }`
  into a single integer `tick` + `sub_order` field.
- **KeeperRL's `cereal` binary serialisation → our
  JSONL log.** KeeperRL's saves are binary blobs; our
  log is human-readable JSONL. The trade-off:
  KeeperRL's saves are smaller and faster; ours are
  auditable and replayable by hand (INV-1).
- **KeeperRL's `extern RandomGen Random` global → our
  `core/rng.py` single instance + two-stream context
  manager.** The single-instance discipline is ported;
  the two-stream separation (substantive vs cosmetic,
  from `brogue.md`) is the addition.
- **KeeperRL's `data_free/game_config/*.txt` custom DSL
  → our `content/tavern_pack/*.json` JSON Schema.** The
  data-driven content shape is ported; the syntax is
  replaced with JSON, the validation is added (D-023).
- **KeeperRL's `considerRebellion` per-tick roll → our
  `seeded_hooks` per-tick trigger.** The shape is the
  same (compute probability per-tick, roll per-tick);
  the trigger sources are different (rebellion is one
  source; our hooks have a per-condition trigger map).

**What inspires us.** The **"dwarf-fortress-style
micro-sim in a roguelike shell"** lesson. KeeperRL proves
that a small team (one primary author, ~10 years) can
build a working settlement sim with continuous-time
scheduling, per-tick collective loops, pre-computed wave
planners, and a binary save format — without the
decade-spanning scope of Dwarf Fortress. The lesson: the
shape is portable; the scope is the variable. Our
TavernSim v0 (MVP_SCOPE §3 micro-dense slice) inherits
the shape — continuous-time queue, per-tick systems,
pre-computed hooks — applied to one tavern instead of
a fortress. The `getRebellionProbability` formula is
the precedent for "complex social phenomena as small
formulas over existing state" — same shape as our
`suspicion`/`trust`/`rebellion` rules (iter-2/iter-3).

**Strengths.**

- Public GPL-2.0 — full source readable; the codebase is
  ~500 C++ files, well-organised by system (model,
  collective, level, creature, task, furniture).
  Pattern-lifting is permitted per `REFERENCES.md` §0.4.
- The continuous-time queue is the cleanest public
  reference for "map-based priority queue with
  per-creature time map" — simpler than DCSS's
  per-monster `speed_increment` field, equivalent in
  shape.
- The `ExternalEnemies` wave planner is the cleanest
  public reference for "pre-computed schedule, dispatched
  by a small `if`" — the precedent for our
  `seeded_hooks`. The 500-wave pre-computation at
  worldgen is the proof that the schedule is data, not
  logic.
- The `GameEvent` X-macro variant is the cleanest public
  reference for "closed event vocabulary + per-event
  fields" — the 24-event list is the precedent for our
  ~12-event phase-0 vocabulary. The X-macro pattern is
  portable to Python `Enum` + `dataclass` (or JSON
  Schema discriminated unions, D-023).
- The `getRebellionProbability` formula is the cleanest
  public reference for "complex social phenomena as
  small formulas over existing state" — 12 lines of
  C++ model rebellion from a prisoner/fighter ratio.
- The data-driven content DSL (`data_free/game_config/`)
  is the cleanest public reference for "content is data
  with `inherit`" — same shape as C:DDA's `copy-from`
  (`cdda_data_json.md`).

**Weaknesses.**

- The codebase mixes engine and UI heavily (`view.h`,
  `renderer.cpp`, `sdl_event_generator.cpp`); the
  engine-only patterns are interleaved with SDL/Steam
  integration. Pattern-lifting requires reading past
  the UI.
- No multi-stream RNG discipline — KeeperRL uses a
  single `Random` instance with no separation between
  state-bearing and display-only rolls. Cosmetic rolls
  can desync the canonical replay. We add the two-stream
  separation (Brogue's contribution, `brogue.md`).
- No event log — runtime state lives in the model,
  levels, collectives, creatures, items, time queue,
  all serialised via `cereal`. Our INV-1 (state =
  fold(log)) is the inverse; the in-memory state is
  the amnesia anti-pattern (`mesa.md`). The save file
  is a binary snapshot, not a log.
- No knowledge records — KeeperRL's creatures have
  `knownTiles` (a per-level visibility map) but no
  per-creature epistemic state beyond "what I've seen".
  Our `knowledge` records carry per-NPC epistemic state
  (who knows what, with what fidelity); KeeperRL has
  no analogue.
- The `considerRebellion` per-tick roll uses
  `Random.chance(p / 1000)` — a per-mille probability
  rolled per-tick. This is the simplest probabilistic-
  trigger pattern (no MTTH, no weights, no scopes —
  `endless_sky_dsl.md` has the same simplicity). It's
  also the noisiest — the actual trigger time has high
  variance. Our `seeded_hooks` add threshold-based
  triggers (MVP_SCOPE §5) for less variance.
- The save format is binary (`cereal::BinaryInputArchive`)
  — small and fast, but not human-readable. Our JSONL
  log is the inverse (auditable, replayable by hand).
- The data DSL has no schema — `data_free/game_config/
  creatures.txt` is parsed by a custom parser; typos
  cause silent misbehaviour. Our `content/tavern_pack/
  *.json` is JSON Schema-validated (D-023); the spec
  is enforced, not advisory.

**Verdict.** Phase-5 roguelike-emergence + micro-sim
reference, positive on the continuous-time queue
(`map<ExtendedTime, Queue>` with `players`/`nonPlayers`
deques), the per-tick collective update order
(creatures → levels → collectives → territory →
external), the `ExternalEnemies` pre-computed wave
planner (500 waves at worldgen, dispatched by a small
`if`), the `GameEvent` closed-variant event vocabulary
(24 X-macro types), the `getRebellionProbability`
small-formula social dynamics, and the data-driven
content DSL with `inherit` — all direct inheritances
into our iter-1 core plumbing (`core/queue.py`,
`core/loop.py`), iter-2 actions (`rules.json`), iter-3
P2a NPC↔NPC relations (D-020), and iter-4 `seeded_hooks`
(MVP_SCOPE §5). Explicitly negative on porting the
single-stream RNG (we add the two-stream separation
from `brogue.md`), the `cereal` binary serialisation
(our JSONL log is the inverse, INV-1), the in-memory
state model (amnesia anti-pattern, `mesa.md`), and the
lack of knowledge records (our `knowledge` layer is
the fix). KeeperRL is the canonical proof that a
dwarf-fortress-style micro-sim is buildable in a
roguelike shell by a small team — the precedent that
our TavernSim v0 (MVP_SCOPE §3) inherits the shape at
one-tavern scale.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
