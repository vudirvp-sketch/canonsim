# STATUS — canonsim

Iteration: 0o (owner-requested: ref-6 batch — Brogue CE + DCSS + KeeperRL roguelike emergence + micro-sim family) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0o is the **ref-6 3-batch iteration** — the
open-licensed roguelike emergence + micro-sim family
(one AGPL, two GPL; all open per `REFERENCES.md` §0.4 —
pattern lifting permitted, port the shape not the syntax
per §0.7 / D-015), each in its own per-ref file:
`docs/ref/brogue.md` (326 lines — the two-stream RNG
discipline `RNG_SUBSTANTIVE`/`RNG_COSMETIC` with
`brogueAssert(rogue.RNG == RNG_SUBSTANTIVE)` scope
guards in `Math.c` + `assureCosmeticRNG` macro for
stream switching, the 36-byte no-wall-clock recording
header in `Recordings.c` writeHeaderInfo
[bytes 0-14 version string, byte 15 mode, 16-23 seed
uint64, 24-27 player turn uint32, 28-31 deepest level
uint32, 32-35 length uint32], `promoteTile` per-layer
state-transition primitive with flag-gated trigger
sources [`TM_IS_FLAMMABLE`/`TM_PROMOTES_ON_ELECTRICITY`/
`TM_IS_WIRED`/`promoteChance` stochastic tick], the
multi-pass environment tick in `Time.c` updateEnvironment
with read→write→cleanup pass separation [the comment at
line 1441 explains: "two passes to keep generations
distinct"], the layered `pmap[x][y].layers[layer]`
cell-stack model, `updateVolumetricMedia` stochastic
gas diffusion with `rand_range(0, numSpaces - 1) <
(sum % numSpaces)` stochastic rounding, `paintLight`
additive RGB over `getFOVMask` with `IS_IN_SHADOW`
flag, `randomNumbersGenerated` audit counter + the
`AUDIT_RNG` debug build that logs every substantive
roll, the "small alphabet deep composition" lesson
[fire/gas/water/light ~5 rules → emergent chains:
thrown potion → gas ignite → grass burns → bridge
collapses], explicitly negative on in-memory `pmap`
state model [INV-1 amnesia anti-pattern] + the
`time(NULL) - 1352700000` seed fallback [we never
loosen INV-2 — seed is an explicit argument only]);
`docs/ref/dcss.md` (360 lines — the multi-stream RNG
discipline at production scale in `random.h` + `random.cc`
[`rng_type` enum: `GAMEPLAY`/`UI`/`SYSTEM_SPECIFIC`/
`LEVELGEN`+per-branch with `NUM_RNGS = LEVELGEN +
NUM_BRANCHES`, RAII `rng::generator` class for stream
switching with constructor/destructor save-restore,
the persistent `FixedVector<PcgRNG, NUM_RNGS>
_global_state` saved to the save file via
`generators_to_vector`/`load_generators`, the
`ASSERT_stable` scope guard [snapshot peek_uint64 in
constructor, assert peek unchanged in destructor —
verifies no RNG consumption happened in the scope],
`peek_uint32/peek_uint64` non-advancing reads for
tests, `defer_rand` infinite lazy tree [functional
randomness — same path through the tree always
produces the same value regardless of how many other
paths were explored], the energy-based turn scheduler
in `mon-act.cc` [`speed_increment` field per monster,
`BASELINE_DELAY = 10` auts per action, `div_rand_round`
stochastic rounding to avoid systematic floor bias,
`_monster_add_energy` increments per-tick by
`div_rand_round(mons.speed * you.time_taken, 10)`],
the `dgn_event_dispatcher` positional event system in
`dgn-event.h`/`dgn-event.cc` [`DET_*` bitflags:
`DET_TURN_ELAPSED`/`DET_MONSTER_MOVED`/`DET_PLAYER_
MOVED`/`DET_MONSTER_DIED`/`DET_ITEM_PICKUP`/
`DET_FEAT_CHANGE`/`DET_DOOR_OPENED`/
`DET_PRESSURE_PLATE`/... with `DET_GLOBAL_MASK` vs
`DET_POSITION_MASK`, per-position listeners +
`fire_vetoable_position_event` for vetoable action-
prevention rules], the `.des` vault grammar in
`dat/des/altar/altar.des` [`NAME`/`TAGS`/`DEPTH`/
`CHANCE: 20% (D:2)` per-branch placement weights/
`SUBST` character substitution map/`FTILE` per-glyph
tile assignment + Lua `: if you.in_branch("Lair") then
... : end` escape hatch for branch-conditional logic],
the 15-year-codebase-scales discipline precedent
[~150k lines of C++, ~787 source files, hundreds of
contributors, byte-identical replayability maintained
across versions], explicitly negative on in-memory
monster struct state [INV-1 amnesia] + Lua-in-vaults
escape hatch [INV-4 stricter — our Python escape is
for orchestration only, never in the canon path] +
no knowledge records [per-NPC epistemic state beyond
"where I last saw the player"] + no director [purely
reactive monster AI; our D-005 director = consequence
planner is the RimWorld anti-pattern fix]);
`docs/ref/keeperrl.md` (444 lines — the
continuous-time queue in `time_queue.h`/`time_queue.cpp`
[`map<ExtendedTime, Queue>` with `ExtendedTime { Local
Time time; bool extraTurn }`, two deques
`players`/`nonPlayers` inside `Queue` so the player
goes first within a tick, `orderMap` per-queue-position
integer counter for deterministic tie-breaking,
`makeExtraMove`/`hasExtraMove` for haste via the
`extraTurn` flag without advancing the local clock,
`compareOrder` with `willMoveThisTurn` + `getLastMove
Counter` fallback], the `Model::tick(LocalTime)` per-
tick update in `model.cpp` lines 143-163 with the
fixed sequence creatures → levels → collectives →
territory rebuild → external enemies [same shape as
our `MVP_SCOPE.md` §5 eight-systems tick order], the
`Collective::tick()` 11-step subsystem update in
`collective.cpp` lines 616-629 [`updateBorderTiles`/
`considerRebellion`/`updateGuardTasks`/
`updateMinionPromotions`/`dangerLevelCache = none`/
`control->tick`/`zones->tick`/`taskMap->tick`/
`constructions->clearUnsupportedFurniturePlans`/
`dancing->setArea`/`if (Random.roll(5))
warnings->considerWarnings`], the
`getRebellionProbability` small-formula social dynamics
[12-line prisoner/fighter ratio formula: `if
numPrisoners <= 4 return 0; if numFighters == 0 return
1; min(1, max(0, (ratio - 0.5) / 1.0))` — complex
social phenomenon as a small formula over existing
state], the `ExternalEnemies` 500-wave pre-computed
planner in `external_enemies.cpp` [constructor
generates 500 waves at worldgen with
`firstAttackDelay = 1800`, `attackInterval = 1200`,
`attackVariation = 450`; each wave's attack time is
`firstAttackDelay + max(0, i * attackInterval +
random.get(-attackVariation, attackVariation + 1))`;
dispatched by `popNextWave(localTime)` which returns
the next wave whose `attackTime <= localTime` —
schedule is data, dispatcher is a small `if`], the
`GameEvent` X-macro 24-event closed variant in
`game_event.h` [`VARIANT_TYPES_LIST` X-macro
generates `CreatureMoved`/`CreatureKilled`/
`ItemsPickedUp`/`Projectile`/`ConqueredEnemy`/
`WonGame`/`Alarm`/`CreatureAttacked`/
`VisibilityChanged`/`MovementChanged`/... — same
shape as our `EVENT_SCHEMA.md` `event_type` enum +
per-type fields], the `cereal` binary serialisation
[inverse of our JSONL log — KeeperRL's saves are
smaller and faster but not human-readable; our INV-1
state = fold(log) is the inverse trade-off], the
data-driven content DSL in `data_free/game_config/
*.txt` with `inherit` [same shape as C:DDA's
`copy-from`, `cdda_data_json.md`], the `Fire` minimal
optional-state machine in `fire.h` [36 lines of C++:
`int burnTime; optional<int> burnState;` + `tick`/
`set`/`isBurning`/`isBurntOut` — same shape as our
`rules.json` `fire_spread` tile state], the
single-instance `extern RandomGen Random` global
[same shape as our INV-2 single `random.Random(seed)`
instance; KeeperRL has no two-stream discipline — we
add the separation from `brogue.md`], explicitly
negative on single-stream RNG [no
`RNG_SUBSTANTIVE`/`RNG_COSMETIC` separation] + binary
save format [INV-1 JSONL is the inverse] + no
knowledge records [per-NPC epistemic state beyond
`knownTiles` visibility map] + custom DSL with no
schema validation [D-023 JSON Schema fix]). All three
paraphrased from the open-source corpus per §0.4 / §0.7
(D-015). Licenses verified against `REFERENCES.md` §2
on 2026-08-26: Brogue CE = AGPL-3.0 (LICENSE.txt
header); DCSS = GPL-2.0+ (LICENSE + README.md line 96
"Crawl is licensed as GPLv2+"); KeeperRL = GPL-2.0
(LICENSE + COPYING.txt both headers + per-file
copyright headers). No license drift between catalog
and index this iteration — KI#6-class pitfall
avoided. §2 of `REFERENCES_DEEP.md` flips ref-6-a/b/c
from todo → done with rich one-line verdicts (the
catalog-row + index-row license-match check is now
a standing pre-flip step). AGENT_NAVIGATION §1 adds
the three new files to the `docs/ref/` list. Per
AGENTS §2.5 this is the **fourteenth** docs iteration
in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l,
0m, 0n, 0o; iter-0d was infra) — the doc-loop alarm
has fired again; the owner explicitly asked to
continue reference work, so the D-022 exception
applies. iter-1 is still the next functional step;
no further docs iterations without a fresh owner
request. KI#6 (closed iter-0n, >2 iterations ago)
deleted per AGENTS §5 mandatory cleanup. KI#3,
KI#4, KI#5 unchanged. AGENTS, ROADMAP, MVP_SCOPE,
EVENT_SCHEMA, schemas, TECH_NOTES, SPECS_BACKLOG,
CORE_DESIGN_RESEARCH, VISION, DECISIONS — untouched.

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
- **Doc-loop alarm vs owner-requested research.** Fourteen docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0o is the fourteenth docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n, 0o;
  iter-0d was infra).
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
  the §6.1 substance filter protects the depth).
- **License drift between catalog and index (KI#6, closed iter-0n; pitfall
  persists).** The `REFERENCES_DEEP.md` §2 index table is **not** the source
  of truth for licenses — `REFERENCES.md` (the catalog) is. The index
  restates the license as a one-line convenience column; if the two
  disagree, the catalog wins. iter-0n found two drifts in §2 (ref-5-b
  "CC-BY-SA" vs catalog "GPL-3.0 code; mixed assets"; ref-5-d "CC0"
  vs catalog "Apache-2.0"); both fixed in the same edit. iter-0o
  verified the three new ref-6 rows (AGPL/GPL/GPL shorthand) against
  catalog §2 (AGPL-3.0 (CE) / GPL-2.0+ / GPL-2.0) — no drift this
  iteration. The diagnostic: before flipping any ref-N row todo→done,
  grep the source row in `REFERENCES.md` and verify the license column
  matches the index entry. Same pattern as the catalog ↔ synthesis ↔
  deep-dive anti-drift rule (D-024/D-026): a fact restated in two
  places drifts; the catalog is the owner. Standing pre-flip check
  added to the iter-0o workflow.
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
order) are the direct precedents — iter-1 inherits the shapes from these
three files.
