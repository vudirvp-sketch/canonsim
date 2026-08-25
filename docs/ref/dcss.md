# DCSS (Dungeon Crawl Stone Soup) · `REFERENCES.md` §1 + §2 + §14 · GPL-2.0+ · phase 5 (roguelike emergence)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is open GPL-2.0+ — code is
> in scope per §0.4; copying text into our repo would force GPL on
> our files, so we port the shape (multi-stream RNG, energy-based
> turn scheduler, vault grammar) into JSON + stdlib Python, never
> the C syntax. Reference repo: `crawl/crawl` (the official
> DCSS repository). Corpus inspected: `crawl-ref/source/random.h`
> + `random.cc` (534 lines), `pcg.h`, `rng-type.h`,
> `actor.h` (452 lines), `actor.cc`, `mon-act.cc` (4369 lines),
> `dgn-event.h` + `dgn-event.cc`, `defines.h`, `player.cc`
> (9733 lines), `dat/des/altar/altar.des`, `dat/des/guide.txt`.

**What it is.** Dungeon Crawl Stone Soup is a major roguelike
descended from Linley Henzell's 1997 Linley's Dungeon Crawl;
the Stone Soup branch has been the canonical version since
~2006. Public GPL-2.0+; ~787 source files in
`crawl-ref/source/`, of which the C++ engine is ~150k lines.
DCSS is the reference for **deterministic RNG discipline at
production scale** — multiple named RNG streams per subsystem
(gameplay, UI, levelgen, per-branch), an energy-based turn
scheduler, a tag-shaped vault grammar, and a positional event
dispatcher. All four are the precedents for our iter-1 core
plumbing (`docs/TASKS.md` iter-1).

**Concrete mechanics.**

- **Multi-stream RNG — `rng_type` enum + `PcgRNG` instances.**
  `random.h` declares `enum rng_type { GAMEPLAY, UI,
  SYSTEM_SPECIFIC, SPARE2, SPARE3, LEVELGEN,
  NUM_RNGS = LEVELGEN + NUM_BRANCHES, SUB_GENERATOR,
  ASSERT_NO_RNG }` (full text in `rng-type.h`). The persistent
  state is a `FixedVector<PcgRNG, rng::NUM_RNGS>
  _global_state` — one PCG generator per subsystem, saved to
  the save file via `generators_to_vector()` /
  `load_generators()`. The active stream is selected by the
  `rng::generator` RAII class: constructor saves the previous
  `_generator` and sets a new one; destructor restores.
  Branches have their own RNG (`LEVELGEN + branch_type`) —
  entering a new branch switches the active stream so branch
  generation never desyncs the gameplay stream. The pattern:
  **one named RNG per subsystem that must not bias another**;
  the discipline is enforced by RAII (a leaked generator is a
  state restoration bug, not a determinism bug). Our INV-2
  inherits the same discipline — one stream for sim, one for
  the chronicle renderer (`brogue.md` lifts the two-stream
  pattern; DCSS generalises it to N streams).
- **`ASSERT_stable` scope guard — RNG state fingerprint.**
  `random.h` declares `class ASSERT_stable { uint64_t
  initial_peek; ASSERT_stable() : initial_peek(peek_uint64())
  {} ~ASSERT_stable() { ASSERT(peek_uint64() ==
  initial_peek); } }`. Construct one in a scope; on scope exit,
  the destructor asserts the RNG state did not advance. The
  pattern: **scope-bound RNG consumption audit** — a function
  that should not consume RNG will fail loudly if it does.
  Equivalent to Brogue's `brogueAssert(rogue.RNG ==
  RNG_SUBSTANTIVE)` but stronger: it asserts *no* RNG roll
  happened, not just the right stream. Our debug-build RNG
  counter (iter-1 `core/rng.py`) inherits this shape — a
  context manager that snapshots the count and asserts it did
  not change on exit.
- **`peek_uint32()` / `peek_uint64()` — non-advancing reads.**
  `random.h` lines 57-58: `peek_uint32()` returns the next
  value the RNG would produce **without advancing the state**.
  The pattern: **peeking the RNG state is a test/audit
  primitive** — useful for T1 byte-identical replay tests
  that need to compare state without consuming it. Our
  `core/rng.py` (iter-1) inherits the same peekable-stream
  shape — a `peek()` method that returns the next value
  without advancing.
- **`defer_rand` — infinite tree of random values.**
  `random.h` lines 319-337. A `defer_rand` object is a tree:
  each node holds a `vector<uint32_t> bits` and a `map<int,
  defer_rand> children`. The first time a method is called
  on a node, a fraction (random float 0..1) is generated and
  stored; subsequent calls with the same parameters return
  the same value (the stored fraction combined with the
  parameter). Different parameters or methods give different
  results but use the same fraction. Children (`operator[]`)
  generate their own fractions. The pattern: **functional
  randomness as an infinite lazy tree** — the same path
  through the tree always produces the same value, regardless
  of how many other paths were explored. This is the precedent
  for "the simulation state is a function of (seed, call
  graph)" — our INV-2 says the same thing differently: state
  = deterministic function of (seed, event order). We do not
  port `defer_rand` directly (it's complex and niche), but
  the lesson matters: RNG consumption order does not break
  replay if the call graph is deterministic.
- **Energy-based turn scheduler — `speed_increment` +
  `BASELINE_DELAY`.** `defines.h` line 149: `const int
  BASELINE_DELAY = 10;` — the baseline number of "auts"
  (aut = arbitrary unit of time) per action. `mon-act.cc`
  line 1742-1751 `_monster_add_energy`: every tick, the
  monster's `speed_increment` is incremented by
  `div_rand_round(mons.speed * you.time_taken, 10)`. When
  `speed_increment >= BASELINE_DELAY`, the monster can act
  (and `speed_increment -= BASELINE_DELAY`). Player time
  (`you.time_taken`) is computed from `player_speed()`:
  `BASELINE_DELAY * scale` baseline, modified by haste
  (`haste_div`), slow (`haste_mul`), berserk, statue form
  (×1.5), etc. The pattern: **action time = energy /
  speed**; faster creatures accumulate energy faster and
  act more often. Our `core/queue.py` (iter-1) inherits
  the same energy-based discipline — the queue key is
  `(tick, sub_order, actor_id)`, and tick = the integer
  clock that increments when energy accumulates past the
  threshold. The same shape, different storage.
- **`div_rand_round` — stochastic rounding.** `random.h`
  line 75: `int div_rand_round(int num, int den)` — divides
  `num` by `den` with **stochastic rounding**: the integer
  part plus one extra unit with probability `(num % den) /
  den`. The pattern: **deterministic integer math with
  stochastic rounding** avoids systematic bias from floor
  or ceil. The same pattern Brogue uses for gas diffusion
  (`rand_range(0, numSpaces - 1) < (sum % numSpaces)` in
  `updateVolumetricMedia`). Our `rules.json` `fire_spread`
  inherits the same stochastic-rounding shape for integer
  damage / volume decay.
- **Positional event dispatcher — `dgn_event_dispatcher`.**
  `dgn-event.h` declares `enum dgn_event_type` with bitflags:
  `DET_TURN_ELAPSED`, `DET_MONSTER_MOVED`,
  `DET_PLAYER_MOVED`, `DET_LEAVING_LEVEL`,
  `DET_ENTERING_LEVEL`, `DET_ENTERED_LEVEL`,
  `DET_PLAYER_IN_LOS`, `DET_MONSTER_DIED`,
  `DET_ITEM_PICKUP`, `DET_FEAT_CHANGE`,
  `DET_DOOR_OPENED`, `DET_PRESSURE_PLATE`, etc. Two masks:
  `DET_GLOBAL_MASK` (events that fire globally, no position)
  and `DET_POSITION_MASK` (events that fire at a specific
  tile). The dispatcher holds a `list<dgn_event_listener>`
  registered at a position (`has_listeners_at(pos)`); when
  the event fires, every listener at that position is
  notified via `notify_dgn_event(event)`. `fire_vetoable_
  position_event` allows listeners to veto (return false) —
  the action doesn't happen. The pattern: **per-position
  event listeners with veto** — the dungeon is reactive
  at the cell level. Our `seeded_hooks` (MVP_SCOPE §5)
  inherit the same shape — a hook registered at a position
  fires when its trigger condition is met. Wesnoth's
  `[event]`/`[filter]` triad (`wesnoth_wml.md`) is the
  same idea with explicit filter tags; DCSS uses bitflag
  positions instead.
- **Vault grammar — `.des` files.** `dat/des/altar/altar.des`
  is a typical vault definition. Syntax (paraphrased):
  - `NAME: basic_altar` — unique vault id.
  - `TAGS: allow_dup extra no_monster_gen transparent decor`
    — closed enum of behavioural tags.
  - `DEPTH: 1-` — depth range where this vault can spawn.
  - `CHANCE: 20% (D:2)` / `CHANCE: 20% (Orc)` /
    `CHANCE: 10% (Snake)` — per-branch placement weights,
    evaluated in order; first match wins.
  - `SUBST: ? : ??`, `! : ?```` ``` — character substitution
    map (the vault is drawn in ASCII; SUBST maps the ASCII
    glyphs to actual dungeon features at parse time).
  - `FTILE: ` = floor_pebble_red — per-glyph tile
    assignment, conditional on branch (`: if
    you.in_branch("Lair") then ... : elseif ... : end` —
    Lua escape hatch).
  - `CLEAR: ?` — clear the rectangle occupied by `?`
    glyphs before placing the vault.
  - Lua escape (`: ... :`) for conditional logic — same
    shape as Wesnoth's Lua escape hatch (`wesnoth_wml.md`).
  The pattern: **data DSL + script escape** — the vault
  is data (a glyph grid with tags), but Lua is available
  for branch-conditional logic. Our `actions.json` +
  `cli/` split inherits the same shape (data DSL + Python
  escape).
- **Vault dispatch by tag and depth.** `dat/des/00init.des`
  is the vault dispatcher — it pulls vaults by tag and depth
  when generating a level. The pattern: **the dispatcher is
  data-driven**, not a switch statement in C++. Our
  `MVP_SCOPE.md` §5 `seeded_hooks` inherit the same shape —
  the director pulls hooks by tag and trigger from a
  data-driven catalog, not from code.

**What we take.**

- **The multi-stream RNG discipline (one stream per
  subsystem).** Our INV-2 single-seed rule +
  `core/rng.py` carries one stream for sim, one for the
  chronicle renderer — same shape as DCSS, scaled down.
  The RAII `generator` class is the precedent for our
  context manager that swaps streams.
- **`ASSERT_stable` scope guard.** Our debug-build RNG
  counter inherits this shape — a context manager that
  snapshots the count and asserts it did not change on
  exit. Same pattern, different mechanism (counter vs
  peek).
- **The energy-based turn scheduler (`speed_increment` +
  `BASELINE_DELAY`).** Our `core/queue.py` queue key
  `(tick, sub_order, actor_id)` is the same shape — tick
  is the integer clock that increments when energy
  accumulates past the threshold. Same shape, different
  storage (we use `heapq`; DCSS uses a per-creature
  `speed_increment` field on the monster struct).
- **`div_rand_round` stochastic rounding.** Our
  `rules.json` `fire_spread` integer damage / volume
  decay uses the same shape — the integer part plus one
  extra unit with probability equal to the remainder
  fraction. Avoids systematic floor bias.
- **The positional event dispatcher (`dgn_event_type`
  bitflags + per-position listeners + veto).** Our
  `seeded_hooks` (MVP_SCOPE §5) inherit the same shape —
  hooks registered at positions fire when their trigger
  fires; vetoable for action-prevention rules (e.g., "the
  door won't open if there's a creature in the way").
- **The data DSL + Lua escape hatch vault pattern.** Our
  `actions.json` (data DSL) + `cli/` (Python escape)
  inherits the same shape. The vault grammar's per-branch
  `CHANCE` is the precedent for our per-condition
  `weight` field on `Intent` preconditions
  (`SPECS_BACKLOG.md` INTENT_SPEC sketch).

**What we adapt.**

- **DCSS's C++ `PcgRNG` → Python `random.Random(seed)`.**
  DCSS uses PCG for its long period and statistical
  quality; our INV-2 + D-012 (stdlib-only) choice is
  `random.Random` (Mersenne Twister). Both are
  deterministic given the seed; the period is shorter
  but sufficient for phase-0 scale (10^4 ticks, not
  10^9). The multi-stream discipline is ported; the
  algorithm is not.
- **DCSS's per-monster `speed_increment` field → our
  per-actor `energy` field on the queue entry.** DCSS
  stores the energy on the monster struct and recomputes
  it per-tick; we store it on the queue entry and use
  `heapq` to maintain ordering. Same energy model,
  different storage.
- **DCSS's `dgn_event_type` bitflags → our JSONL `event_type`
  enum.** DCSS uses bitflags for O(1) membership tests
  (`if (event.type & DET_GLOBAL_MASK)`); we use a closed
  enum string for readability and JSON Schema validation
  (D-023). The shape is the same; the storage is
  different.
- **DCSS's `.des` vault grammar → our JSON content packs.**
  DCSS uses a custom parser for `.des` files; our
  `content/tavern_pack/*.json` uses JSON Schema
  validation (D-023). The data-DSL shape is ported
  (NAME, TAGS, DEPTH, CHANCE → name, tags, depth_range,
  weight); the syntax is replaced with JSON.
- **DCSS's Lua escape hatch → Python in `cli/` and
  (phase 1+) `brief/`.** The same DSL+escape pattern —
  data DSL for the 90% case, script for the 10% edge.
  Our `cli/` runs Python on top of the JSONL log; DCSS's
  Lua runs on top of the dungeon state. Same shape,
  different language (and our escape is for orchestration
  only — never in the canon path; INV-4 stricter).
- **DCSS's `ASSERT_stable` scope guard → our debug
  context manager.** DCSS uses a C++ destructor; we use
  a Python context manager (`with rng.audit(): ...`).
  Same shape, different language.

**What inspires us.** The **multi-stream RNG discipline at
production scale** lesson. DCSS proves that a 15+ year
old codebase with hundreds of contributors can maintain
byte-identical replayability across versions by sticking
to a few rules: (a) one named RNG per subsystem, (b) RAII
for stream switching, (c) `ASSERT_stable` for scope audits,
(d) `peek_*` for non-advancing test reads, (e) stochastic
rounding for integer math, (f) per-position event
listeners with veto. None of these is novel on its own;
the lesson is that **the discipline scales** — DCSS
maintains it across 787 files and ~150k lines of C++. Our
INV-2 + D-023 (JSON Schema) is the same discipline applied
to a smaller codebase with stricter invariants (no LLM,
no network, stdlib-only).

**Strengths.**

- Public GPL-2.0+ — full source readable; the codebase is
  large but well-organised (`crawl-ref/source/` with
  per-system files like `mon-act.cc`, `dgn-event.cc`,
  `random.cc`). Pattern-lifting is permitted per
  `REFERENCES.md` §0.4.
- The multi-stream RNG discipline is the cleanest public
  reference for "many subsystems, no cross-stream bias".
  The `rng_type` enum + RAII `generator` class is the
  precedent for our `core/rng.py` stream switching.
- `ASSERT_stable` is the cleanest public reference for
  "scope-bound RNG consumption audit" — a one-line guard
  that fires on any unexpected roll.
- The energy-based turn scheduler (`speed_increment` +
  `BASELINE_DELAY`) is the standard roguelike turn model —
  every major roguelike uses some variant (Brogue, NetHack,
  ToME, Angband). DCSS's implementation is the most readable
  public reference.
- The vault grammar (`.des` files) is the cleanest public
  reference for "data DSL + script escape" — the pattern
  Wesnoth uses (`wesnoth_wml.md`), generalized to depth-
  and branch-conditional placement. Our `actions.json` +
  `cli/` inherits the shape.
- The positional event dispatcher (`dgn_event_dispatcher`)
  is the precedent for our `seeded_hooks` — per-position
  listeners with veto, fired by a closed enum of event
  types.

**Weaknesses.**

- The codebase is enormous (~150k lines of C++); the signal-
  to-noise ratio for pattern-lifting is low. We lift 6
  patterns (above); the rest is game-specific combat,
  spell, god, mutation, species, job code.
- DCSS has no event log — runtime state lives in the
  monster struct and the dungeon grid (`env.grid(pos)`).
  Our INV-1 (state = fold(log)) is the inverse; the
  in-memory state is the amnesia anti-pattern (`mesa.md`).
- DCSS's Lua escape hatch is heavily used for vault logic —
  vaults can run arbitrary Lua at parse time and at
  trigger time. Our INV-4 (no LLM/network in track A)
  is stricter; the Python escape in `cli/` is for
  orchestration only, never in the canon path.
- The `.des` parser is custom — no JSON Schema, no
  validation against a type system. Our `content/tavern_
  pack/*.json` is JSON Schema-validated (D-023); the
  spec is enforced, not advisory.
- DCSS's save format is binary (`CrawlVector` serialised
  via cereal); our JSONL log is human-readable. The
  trade-off: DCSS's saves are smaller and faster; ours
  are auditable and replayable by hand.
- No knowledge records — DCSS's monster AI uses the
  player's position and the monster's last-known player
  position; there's no per-monster epistemic state
  beyond "where I last saw the player". Our `knowledge`
  records carry per-NPC epistemic state (who knows
  what, with what fidelity); DCSS has no analogue.
- No director — DCSS is purely reactive (monster AI
  reacts to player; spawns are static or random). Our
  D-005 (director = consequence planner) is the
  RimWorld anti-pattern fix (`rimworld.md`); DCSS has
  no director layer to lift.

**Verdict.** Phase-5 roguelike-emergence reference,
positive on the multi-stream RNG discipline (`rng_type`
enum + RAII `generator` + `ASSERT_stable` + `peek_*`),
the energy-based turn scheduler (`speed_increment` +
`BASELINE_DELAY` + `div_rand_round`), the positional
event dispatcher (`dgn_event_dispatcher` with vetoable
listeners), and the data-DSL-plus-script-escape vault
grammar — all direct inheritances into our iter-1 core
plumbing (`core/rng.py`, `core/queue.py`) and our
`seeded_hooks` (MVP_SCOPE §5). Explicitly negative on
porting the C++ PRNG (stdlib `random.Random` instead),
the in-memory state model (INV-1 JSONL log is the
inverse), the Lua-in-vaults escape hatch (INV-4
stricter), and the lack of a director or knowledge
records (RimWorld and our `knowledge` layer fill the
gaps). DCSS is the canonical proof that multi-stream RNG
discipline scales to a 15+ year codebase with hundreds
of contributors — the precedent that our INV-2 + D-023
discipline is not naive optimism.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
