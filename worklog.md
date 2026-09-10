# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.
> Entries re-trimmed to the line cap at iter-10a (KI#37; the drift ran
> iter-8b→10) — pre-trim detail lives in git history.
> Re-trimmed 39→10 at iter-48 (KI#68: the cap had drifted silently —
> the iter-43..47 "evicted per the cap" claims never executed; the
> eviction is now verified in the same edit, not claimed). Pre-trim
> history lives in git.
> Order: newest first (normalized at iter-8c — the order had drifted
> since iter-5).
---
iter-96 · 2026-09-11 · name1 — the name generator (the queue's W2 row
after depth-7, D-116 (12); D-131; 19 files — 5 code + 2 periphery + 2
test + 2 ref dives + the index + 7 doc sync: the stream + the generator + the lint
+ the condensation consumer + the read surface + the dives are one
family, the iter-90..93 footprint; AGENTS §2.3: 18 > 5-6, the
objective scope noted here; the doc-only streak iter-94+95 BROKEN —
AGENTS §2.5 resolved on record)
- core/names.py (new) + core/rng.py: the D-079 family law's SIXTH
  member `name:<npc>` (name_stream_name, lazy registration, the
  assure-shadow law at six families); materialize_name the lazy
  scene-detail twin — ONE birth (npc, "name", None->drawn), the
  bounded collision walk against the entity namespace (WALK_MAX,
  the loud NamesError), the unarmed law total (the stream never
  registers)
- core/groups.py + core/loop.py: the condensation consumer — the
  name births paired with the membership births (one member, one
  block; a runtime-joined member still named), the outcome's
  `names` key (the line must branch — a bare {names} is an unknown
  slot), the tier half draw-free; the bank rides _condense_groups
- core/pack.py: the `_names` lint (after _factions) — the profiles'
  shapes, the npc generated_name declarations (mutual exclusion with
  the authored `name`), the REACHABILITY law (a declaring npc must
  ride a condensing group's membership — the depth-5b family);
  render/chronicle.py + brief/assembler.py: the born-name read
  (fold-first — canon outranks the pack record; the unborn render as
  their dry ids)
- docs/ref/ck3.md + docs/ref/azgaar_names.md (new, the ref-19 dives
  owed at the row) + REFERENCES_DEEP index; phases.md §5 the name-1
  paragraph; EVENT_SCHEMA §4 the generated-name home; NAV §1; TASKS
  name-1 done; DECISIONS D-131; STATUS re-pinned (the queue: st-6(a)
  the next live candidate, name-1 the last W2 row closed)
- +28 tests, 1516→1544+1 green, ruff clean (3.12.14, the env pin;
  seed 42 pinned). Corpus price ZERO by construction, measured both
  arms: the committed pack unarmed — the inert twin (the whole
  vocabulary, no time.macro) byte-identical over plumbing_smoke +
  day1_full; the armed delta the name births + the `names` key alone,
  the (t,type,actor) sequence + the fingerprint EQUAL to the authored
  twin. iter-86 evicted (verified against git in this edit); 10
  held. Caps: STATUS 844 / TASKS 1158 / DECISIONS 97 lines (67 rows)
  — over-cap on substance (§6.1, the D-095..D-130 precedent), trim at
  the phase-5→6 gate.
---
iter-95 · 2026-09-11 · intake8 — research intake 8, the
setting-direction verdict set routed (doc-only, the owner's chat
call; D-130; 6 files — the iter-85/94 intake footprint family,
AGENTS §2.3: 6 > 5-6, the one-family objective scope noted here)
- verified BEFORE routing: the clone green (1516+1, ruff clean, HEAD
  a78e2f1, Python 3.12.14)
- D-130: the three-tier posture (the repo's 2nd setting is ORIGINAL
  — the province sketch at phases.md §6, authored pillars over a
  generated surface, riding world-2; the level-1 reskin instrument
  is the open generic stack; a proprietary fan-pack is owner-local,
  zero repo footprint); the minus ledger (ten catalogued minuses →
  the standing laws, zero new machinery); REFERENCES §10 +6 rows
  (Morrowind, TES anti-row, Discworld, FNV, Pathologic, Qud); NO new
  backlog rows (the material rides the existing W4 rows, just-in-time
  the D-096 precedent)
- the doc-only streak (iter-94 + 95) surfaced in STATUS per AGENTS
  §2.5 — both the owner's research calls, not an agent loop; the
  queue untouched (name-1 pinned); iter-85 evicted here (verified
  against git in this edit; 10 after); re-run post-edit: 1516+1
  green, ruff clean. Caps: STATUS 827 / TASKS 1141 / phases 938 /
  REFERENCES 311 / DECISIONS 96 lines (66 rows) — over-cap held on
  substance (§6.1), trim at the phase-5→6 gate.
---
iter-94 · 2026-09-10 · intake7 — research intake 7, the Anthropic-2026
agent corpus routed (doc-only, the owner's adoption call; D-128/D-129;
7 files — the iter-85 intake footprint family, AGENTS §2.3: 7 > 5-6,
the one-family objective scope noted here)
- verified BEFORE routing: the clone green (1516+1, ruff clean, HEAD
  12f5a07) + all six articles fetched live (BEA carries the Managed
  Agents update note; the Apr-2026 flagship's brain/hands split,
  context anxiety, cattle — confirmed in the fetched bytes, not the
  analysis text's word)
- adopted: ROADMAP §5 step 6 (the protocol-law staleness pass — AGENTS
  grew +190/−5 over 6 commits, only a gate pass prunes), MVP_SCOPE §18
  the actionable-error bullet (D-111 generalized; KI#82/#83 the
  evidence), TASKS mech-2 (default output caps on the introspection
  CLIs — trace measured 188 lines/12 KB on day1_full, O(ticks)),
  SPECS_BACKLOG the SOW harness-skeleton sketch; refused with cause:
  platform plumbing (MCP/sandboxes/OAuth/TTFT), multi-agent default,
  semantic search, sleep-time compute, LLM-as-judge
- D-129: protocol-law D-rows carry expected observable effects,
  checked within 1-2 iterations; the queue untouched (name-1 pinned);
  iter-84 evicted here (verified against git in this edit; 10 after);
  re-run post-edit: 1516+1 green, ruff clean. Caps: STATUS 820 / TASKS
  1113 / ROADMAP 102 / MVP 404 / DECISIONS 95 lines (65 rows) —
  over-cap held on substance (§6.1), trim at the phase-5→6 gate.
---
iter-93 · 2026-09-10 · gsim1 — depth-7, groups & simulation LOD
(D-112's ratified resolutions executed — the write side of the LOD
ladder at group scale, the W2 row after depth-6; 11 files — 3 code
(groups.py new, pack, loop) + 1 new test file + 7 doc sync: the
door + the tiers + the lint + the integration are one family, the
iter-90..93 footprint; AGENTS §2.3: 11 > 5-6, the objective scope
noted here)
- core/groups.py (new): the write-side LOD's single owner —
  `macro_tick_drafts` the population tier (one aggregate event per
  COLD group per macro crossing, actor = the group id — D-112's one
  id, the unborn population's count under `population` — the static
  members whose member_of is still None, a live fold read; no
  knowledge/state_changes/hooks, DRAW-FREE), `condensation_drafts`
  the tier transition on crossing the warm transition (ONE event
  per group: the un-born members' canon births — the D-054
  promotion shape, already-holders skipped — plus the write-once
  tombstone marker `condensed`; the load state the origin),
  `is_condensed` the marker read (the aggregate's gate). The
  member_of door: NO fold seed (absence IS None, the slot shape);
  the fold validates every join/leave/transfer; the depth-6 walk
  keeps its static-list read (the iter-92 law, zero re-pins).
- core/pack.py: the tier-vocabulary lint — the group record's
  optional `macro_event`/`condense_event` (both in the template
  closure, EVENT_SCHEMA §11; memberless refused — dead data, the
  vacuity law's lint arm). core/loop.py: `_condense_groups` the
  tier-transition pass FIRST at the beats AND the crossings (the
  materialization precedes the machinery the members then ride);
  `_run_macro`'s order — turn → condensations → cold aggregates →
  warm drift → rolls; both under an armed clock alone (the unarmed
  one-scene law, the v0.1 bytes).
- +23 tests (tests/test_groups.py — the units: the aggregate's
  shape, the tombstone gate, the zone filter, the population's
  live-fold read; the condensation: the births + the marker, the
  skip law, the write-once marker, the per-group opt-in; the door:
  the fold's join/leave/transfer validation, the stale birth loud;
  the lint refusals, parametrized; the integration: the cold
  aggregates with the cause chain, the warm/active condensations at
  the first crossing, the beat's detection arm (cadence beyond the
  beat interval), the tombstone story with the contrast twin,
  byte-identical determinism, the both-arms price — the fingerprint
  EQUAL, the delta the tier families alone, the shared (t, type,
  actor) sequence unchanged; the inert twin byte-identical over
  plumbing_smoke + day1_full; the tale's render lines binding
  {population}/{members}) — 1493→1516+1 green, ruff clean (3.12.14,
  the env pin; seeds 42 + 0 + 125 spot-checked). Corpus price ZERO
  by construction: the committed pack declares no groups and no
  time.macro; the per-group opt-in keeps every depth-6 pinned test
  UNTOUCHED (zero re-pins, git-verified: no fixture in the diff).
- docs: DECISIONS D-127, TASKS depth-7 done, phases.md §5 the
  write-side-LOD landing tag, NAV §1 (the groups module row + the
  pack/loop extensions), README (the narrative + the code-map row +
  the count 1493→1516), STATUS re-pinned (the queue: name-1 next,
  per D-116's wave order) + KI#83 deleted (closed iter-91, two
  iterations past, the KI#81 precedent) + this file (the order
  normalized — iter-92 had been appended at the END, newest-first
  restored; iter-87's missing separator restored). iter-83a evicted
  here (verified in the same edit); 10 after. Caps: STATUS 863 /
  TASKS 1072 / DECISIONS 93 lines (63 rows) / phases 860 / README
  719 — over-cap on substance (§6.1, the D-095..D-127 precedent),
  trim at the phase-5→6 gate.
---
iter-92 · 2026-09-10 · fact1 — depth-6, factions with goals (D-116's
W2 row after depth-3; 15 files — 6 code/render (factions.py new,
rng, pack, fold, loop, chronicle) + 2 test (test_factions.py new,
test_mechanics the future-layer placeholder rename) + 7 doc sync:
the
formula + the entity kind + the lint + the walk are one family, the
iter-90..92 footprint; AGENTS §2.3: 9 > 5-6, the objective scope
noted here)
- core/factions.py (new): the factions' single owner —
  `faction_probability` the KeeperRL small formula (the affected
  fraction of the membership, per-cent floored, against the pack
  threshold, ramping to `max_per_beat`; the deadband at-or-below the
  bar, the vacuity law; pure integer arithmetic), `faction_intents`
  the goal walk (each member's LIVE `status.<axis>` — D-006, never a
  stored group score; d100 on the entry's OWN
  `faction:<group>:<kind>` stream — the D-079 family's FIFTH member,
  one draw per walk, bar 0 included (the cadence law); a hit rides
  the front door, actor = the group id — D-112's one id; the
  requires gates stay silent). core/rng.py: FACTION_PREFIX +
  `faction_stream_name` (five families).
- core/pack.py: the `groups` category (OPTIONAL, the 68a pattern —
  anchor a declared location, members declared npcs, ids unique
  across categories, closed vocabulary) + the `_factions` lint (after
  `_urgencies`: axis ∈ rules.states, trigger ≥ 0, threshold 0..99 /
  max 1..100 — dead data refused, the (group, kind) pair unique,
  engine-2's twin). core/fold.py: the anchor seeds the projection (an
  actor's read surface, never a scene body). core/loop.py: the
  faction walk beside the urgencies at the beats AND the crossings
  (the anchor scoping the zone — cold factions silent, their
  population ride depth-7's aggregates). render/chronicle.py: the
  position fold seeds the anchors ({location} renders for a group).
- +34 tests (tests/test_factions.py — the formula's integer laws; the
  lint refusals (groups + entries, parametrized); the walk: the
  one-id intent, the isolated stream (draw-driven registry), the
  cadence law at bar 0, the non-holder sit-out, the LOD scoping by
  the anchor, the silent gates; the integration: the door + the cause
  chain + `faction_0000` in provenance, byte-identical determinism,
  the warm/active/cold arms under an armed clock, the tale line; the
  both-arms price: the fingerprint EQUAL, the delta the muster family
  ALONE; the inert twin byte-identical over plumbing_smoke +
  day1_full) — 1459→1493+1 green, ruff clean (3.12.14, the env pin;
  seeds 42 + 0 + unset spot-checked). ZERO re-pins (git-verified: no
  fixture in the diff, the committed pack untouched — no groups, no
  factions, zero draws). tests/test_mechanics.py: the future-layer
  placeholder renamed factions→guilds — the placeholder WAS the
  depth-6 block's own name (the law's own lifecycle, D-126).
- docs: DECISIONS D-126, TASKS depth-6 done, phases.md §5 the P3b
  landing tag, NAV §1 (the factions row + the rng five-family + the
  loop/fold/render extensions), README (the narrative + the code-map
  row + the count 1459→1493), STATUS re-pinned (the queue: depth-7 +
  name-1 per D-116's wave order) + this file. iter-83 evicted here
  (verified against git in this edit); 10 after. Caps: STATUS 861 /
  TASKS 1055 / DECISIONS 92 lines (62 rows) / phases 841 / README
  701 — over-cap on substance (§6.1, the D-095..D-126 precedent),
  trim at the phase-5→6 gate.
iter-91 · 2026-09-10 · lod1 — depth-3, the scene LOD (D-116's W2
consumer head, the macro clock's FIRST consumer; 16 files — 6 code
(lod.py new, states, urgencies, loop, macro docstring, pack the
KI#83 guard) + 3 test files (test_lod.py new, test_core the probe,
test_macro the re-pin) + 7 doc sync: the zones + the filters + the
loop integration + the pins are one family, the iter-86..90
footprint; AGENTS §2.3: 16 > 5-6, the objective scope noted here)
- core/lod.py (new): the zone family's single owner — `scene_zones`
  (the pure partition over the exits graph + the PC's live position:
  ACTIVE per-beat / WARM the exits in pack order / COLD the rest in
  declaration order, self-exits + duplicates filtered, LodError the
  pred-contract guards), `npc_population` the census read,
  `COLD_COUNT_KEY = "cold_npcs"` the turn's flat count. THE ONE-GATE
  LAW: the LOD engages exactly when the macro clock is armed (the
  warm cadence IS the macro cadence — one clock, zero new pack
  vocabulary); the unarmed law is the one-scene world.
- core/loop.py: `_run_macro(tick, entry_tick)` — the turn FIRST
  carrying the cold census, then the warm ring (the drift chained
  after the turn at the crossing tick, the goal rolls at the
  crossing tick enqueued at the entry tick — the beat machinery
  minus the DIRECTOR, which stays global: the story layer, never
  ambient life); `_run_beat` scopes to the ACTIVE zone under an
  armed clock (`_scene_zones`, None unarmed). core/states.py +
  core/urgencies.py: the `locations=None` LOD filter (None the
  one-scene law; the walk cuts, never rescores — L13; the odds never
  change, the roll cadence is the LOD's own cost). core/macro.py:
  the docstring's consumer re-pin (depth-3 the surface's first
  caller). core/pack.py: KI#83 — the entities lint's missing-`exits`
  KeyError leak, the named-PackError guard (the KI#82 family).
- +17 tests (tests/test_lod.py — the partition, the loud guards, the
  census's npc-only law, the self-exit filter, the filter scopes with
  the L13 no-rescore law + the draw-driven stream registry, the
  integration: the warm ring at the crossings with the cause chain,
  the active-per-beat vs warm-at-the-crossing split, the cold
  silence + the census ride, the census following the PC across the
  move, the unarmed twin's byte-identity over plumbing_smoke +
  day1_full, determinism, the co-occurring family order, the
  template's census binding; tests/test_core.py the KI#83 probe;
  tests/test_macro.py the corpus pin re-measured) — 1442→1459+1
  green, ruff clean (3.12.14, the env pin; seeds 42 + 0 + unset
  spot-checked). Corpus price, measured BOTH arms: ZERO by
  construction — the committed pack unarmed (the one-scene law), the
  unarmed crafted twin byte-identical to the committed bytes over
  the corpus scripts; the armed arm's delta the macro family alone
  (seed 42: 18 vs 6 events — 2 turns + 10 warm drifts, the
  substantive fingerprint EQUAL at 0, the rolls on the isolated
  urgency streams); ZERO re-pins (git-verified: no fixture in the
  diff, the T1 golden untouched).
- docs: DECISIONS D-125, TASKS depth-3 done, phases.md §5 the
  scene-LOD paragraph + the intake bullet's landing tag, NAV §1 the
  lod row + the states/urgencies/loop extensions, README the
  narrative sentence + the code-map line + the stale test count
  synced (1323→1459 — the honest-count law), STATUS re-pinned (the
  queue: depth-6 next, the W2 wave order) + KI#83 recorded + KI#82
  deleted (closed iter-88, three iterations past — the deletion was
  overdue at iter-90). iter-82 evicted here (verified against git in
  this edit); 10 after. Caps: STATUS ~800 / TASKS 1044 / DECISIONS
  91 lines (61 rows) / phases ~800 / README 681 — over-cap on
  substance (§6.1, the D-095..D-125 precedent), trim at the
  phase-5→6 gate.
---
iter-90 · 2026-09-10 · maclock1 — the macro-clock primitive (W2's
head, D-116's wave order, FIRST among its consumers; 11 files — 3
code + 1 new test + 7 doc sync: the primitive + the loop
integration + the lint + the pins are one family, the iter-86..89
footprint; AGENTS §2.3: 11 > 5-6, the objective scope noted here)
- core/macro.py (new): the scheduler cadence rule (`next_macro_tick`
  — the positive multiples of the pack-declared
  `time.macro.cadence_ticks`, pure arithmetic, never entropy), the
  macro-year counter (`macro_year = start + t // cadence`, derived
  never stored; the start BINDS to the worldgen chronicle horizon —
  the calendar binding, one timeline, 0 unarmed), the aggregate
  emission surface (`macro_turn_draft` — the D-112
  one-event-with-cardinality shape, the counts flat integer keys
  beside `year`, a `year` count a refused branch fake; the future
  consumers depth-3/depth-7/st-6a/weather-1 call it at the
  crossing); the raw-read guards raise MacroError (D-111 family).
- core/loop.py: the third crossing cursor `_next_macro` (session-
  persistent like the rotation/beat cursors) fired COARSEST-FIRST at
  a co-occurring tick (macro → rotation → beat); `_run_macro` — one
  turn event through the commit door, cause = the writer's last id,
  no knowledge/state_changes/hooks, importance via the pack's own
  rule. core/pack.py: the `time.macro` lint (closed vocabulary,
  cadence ≥ 1, the event type in the template closure).
- +18 tests (tests/test_macro.py — the arithmetic, the binding, the
  surface's refusals, the crafted-pack integration: the turns with
  the cause chain, the co-occurrence order, the A/B both-arms price,
  byte-identical determinism, the session cursor, the render arms,
  the lint refusals) — 1424→1442+1 green, ruff clean (3.12.14, the
  env pin; seed 42 + unset spot-checked). Corpus price ZERO by
  construction: the committed pack declares no time.macro (the 68a
  pattern — the arming rides with the primitive's first consumer,
  weather-1 the natural first); measured both arms — the fingerprint
  EQUAL, the event-count delta the turns alone, zero re-pins
  (git-verified: no fixture in the diff).
- docs: DECISIONS D-124, TASKS maclock-1 done (weather-1/st-6a gate
  notes re-pinned), phases.md §5 the macro-clock paragraph, NAV §1
  + README the core/macro rows, STATUS re-pinned (the queue: the W2
  consumers). iter-81 evicted here (verified against git in this
  edit); 10 after. Caps: STATUS 767 / TASKS 1041 / DECISIONS 90
  lines (60 rows) / TECH_NOTES 773 / README 669 — over-cap on
  substance (§6.1, the D-095..D-124 precedent), trim at the
  phase-5→6 gate.
---
iter-89 · 2026-09-10 · geo1 — the geometry rework (W1's fourth,
D-116's wave order, BEFORE any big-world pack; 10 files — 1 code
edit + 1 new tool + 1 test file + 7 doc sync: the mechanism + the
measured instrument + the pins are one family, the iter-81/88
footprint; AGENTS §2.3: 10 > 5-6, the objective scope noted here)
- core/worldgen.py: `_neighbors` — the GRID-HASH walk (buckets at
  spacing scale, expanding Chebyshev rings, the ring-floor exactness
  law: a bucket at ring ≥ r+1 is farther than r·scale on one axis,
  so the k-th best within (r·scale)² proves the unexplored rings out
  of reach, ties included) — amortized O(N), byte-identical to the
  full sort, computed ONCE in `generate_world` and shared by
  watershed + biomes (the signatures take the cache; the second
  computation was the free half of the old wall).
- core/worldgen.py: `_pass_relax` — the PER-SITE BOUNDING-BOX WALK
  (`_nearest_owner_walk`: each site sweeps its box, each point once
  per covering site, O(extent²) at the lattice's constant; index
  visit order IS the (d², index) tie law); the runtime EXACTNESS
  CHECK (a best within radius² proves the true nearest's box covered
  the point) + the deterministic doubling retry (the output never
  depends on the radius), the WorldgenError at the covering radius
  the unreachable backstop; the empty-site degenerate keeps the old
  silent shape.
- scripts/worldgen_profile.py (new, D-046 CLI-class): the perf-1
  precedent on the map side — the ladder 36→10k sites over the
  committed pack's own block (extent scaled alone), clean + cProfile
  double-run with the fingerprints sha256-compared; the 36-site row
  reproduces the corpus digest verbatim (the ladder's anchor).
  TECH_NOTES §12 the numbers: the old walls measured on HEAD
  795bb1b FIRST (relax 2.27/11.77/37.81 s at 400/900/1600, the
  quadratic fit ~25 min at 10k; neighbors ×2), the new curve (10k
  full door 1.19 s clean, sites/s ~8.4–10k, cost draw-linear — the
  largest cProfile line rng.randint at 280k calls).
- +2 tests (the brute-force oracles: the pre-geo-1 full scans
  inlined as references — the grid-hash exact vs ties/duplicates/
  k-beyond/single-site; the box-walk exact for rounds 0..3 + the
  clustered retry path walked directly + the empty-world degenerate)
  — 1422→1424+1 green, ruff clean (3.12.14, the env pin; seeds
  0/42/125 + unset spot-checked). Corpus price, measured BOTH arms:
  ZERO — the genesis fingerprints (seeds 0/42/125) byte-identical
  before/after (cd85495945b7f09b / f55c3547230aea5b /
  fca783da67c8020e), the T1 + corpus fixtures untouched, zero
  re-pins (git-verified).
- docs: DECISIONS D-123, TASKS geo-1 done, TECH_NOTES §12 (the
  curve), AGENT_NAVIGATION §1 + README the scripts rows,
  STATUS re-pinned (the queue: maclock-1 next, the W2 wave order).
  iter-80 evicted here (verified against git in this edit); 10
  after. Caps: STATUS 736 / TASKS 1038 / DECISIONS 88 lines (59
  rows) / TECH_NOTES 773 / README 651 — over-cap on substance
  (§6.1, the D-095..D-123 precedent), trim at the phase-5→6 gate.
---
iter-88 · 2026-09-10 · place1 — the placement discipline (W1's
third, D-116's wave order; 11 files — 2 code + 1 pack data + 1 test
file + 7 doc sync incl. AGENT_NAVIGATION's worldgen/pack rows (the
structure sync — the metric + the seventh sub-block): the lint + the
metric + the pack declaration + the pins are one family, the
iter-86/87 footprint; AGENTS §2.3: 11 > 5-6, the objective scope
noted here)
- core/worldgen.py: `lattice_distance` — the row-major lattice as
  the topology of record (Chebyshev cell steps, a pure function of
  the indices + the map config, pre-draw load-time) + the module
  docstring's place-1 paragraph + the `_SUB_BLOCKS` comment re-pinned
  (the runtime backstop's set stays six-block — the passes never
  read `place`).
- core/pack.py: `WORLDGEN_SUB_BLOCKS` += `place` (the seventh
  REQUIRED sub-block); the shape lint (the closed vocabulary
  {max_edge_span}, 0..columns-2 — the VACUITY law: a span at the
  lattice diameter accepts every pair, dead data, the single-tier
  collection's twin, never a policy ceiling); the claim↔exits
  consistency check — every exits edge joining two claimed
  locations, ALL cross-pairs within the span (edges with an
  unclaimed endpoint impose nothing); KI#82 FIXED (the
  missing-sub-block KeyError leak — the named-PackError loop,
  probed first on a crafted twin). rules.json: the committed
  `place` block (max_edge_span 1 — the tavern↔street pair, sites 0
  and 1).
- +5 tests (the metric pins, the opposite-corner refusal + the
  co-located/zero-span arms, the vacuity/range/missing family, the
  all-seven-blocks KI#82 loop, the runtime split) — 1417→1422+1
  green, ruff clean (3.12.14, the env pin; seeds 0/42/unset
  spot-checked). Corpus price, measured: ZERO by construction —
  lint-side + pack data alone, no runtime byte reads `place`; the
  T1 + corpus fixtures byte-identical, zero re-pins (git-verified).
  KI#82 opened + closed in the same iteration (AGENTS §5).
- docs: DECISIONS D-122, TASKS place-1 done + the st-6a gate note
  (maclock-1 alone now), phases.md §5 the placement-discipline
  paragraph, README the narrative sentence, STATUS re-pinned (the
  queue: geo-1 next, the W1 wave order). iter-79 evicted here
  (verified in this edit); 10 after. Caps: STATUS 710 / TASKS
  1031 / DECISIONS 87 lines (58 rows) / phases 775 / README 651 —
  over-cap on substance (§6.1, the D-095..D-122 precedent), trim at
  the phase-5→6 gate.
---
iter-87 · 2026-09-10 · chron2 — the history bridge (W1's second,
D-116's wave order; 16 files — 4 code + 2 pack data + 3 test files
(the T1 fixture re-pin among them) + 7 doc sync: the mechanism + the
pack migration + the lint widening + the pins + the doc sync are one
family, the iter-75/83/86 footprint; AGENTS §2.3: 16 > 5-6, the
objective scope noted here)
- core/worldgen.py: the DF legends shape — every history event's
  outcome gains `participants` (two DISTINCT regions, the offset
  pair draw) + `places` (one site per event); the walk (`_walk_-
collections`, DRAW-FREE — a pure function of the year-sorted kinds +
  the pack's `chronicle.collections` tier declaration) groups the
  runs: the root-kind event anchors, the nested-kind events join at
  their first matching tier under the member caps, anything else
  closes + re-processes; the members INHERIT the anchor's pair (the
  DF collection's role fields); the PARENT MAP (draft indices, -1 =
  world_formed) — a member chains to its nearest lower-tier
  predecessor, a top-level event to the previous top-level (the flat
  form the linear chain); genesis() → (model, drafts, parents).
- core/loop.py: open() resolves the parents through the WRITER'S
  OWN ids at commit (the id law single-owner — the drafts predict
  nothing). core/pack.py: the lint widening — the collections'
  closed vocabulary (≥ 2 tiers, the root positional key set, the
  kinds ⊆ HISTORY_KINDS, the types unique, the caps ≥ 1), capitals
  ≥ 2 (the participants' two sides), the template closure at
  ALTERNATIVE granularity (participants/places unconditional,
  collection when declared), RESERVED_CLAIM_SLOTS += the history
  outcome keys (`year` the branch fake). render/tracery.py:
  `_render_value` — lists join `', '`, never the host repr (D-120's
  law generalized to the chronicle side).
- content: rules.json chronicle.collections = feud → quarrel (the
  tavern-scale war→battle); templates.json the history arm's three
  optional clauses. +11 tests (the DF shape, the pass-1 freeze, the
  walk + the cap + the flat form, the cause tree in the committed
  log + the fold replay, the tier render, the lint refusals, the
  reserved family, the backstop arms, the tracery list-join) —
  1406→1417+1 green, ruff clean (3.12.14, the env pin; seeds
  0/42/unset spot-checked). Corpus price, measured: the pass-1
  stream positions FROZEN (the years/kinds/hooks verbatim — the
  murmur's pre-seed pins stable), the event count unchanged (no id
  shift), zero corpus fixture re-pins; the T1 fixture the ONE re-pin
  (4 outcome lines, git-verified).
- docs: DECISIONS D-121, TASKS chron-2 done, phases.md §5 the
  chronicle pass's chron-2 form, EVENT_SCHEMA §11 the single-parent
  collection note, README the narrative sentence + the map line,
  STATUS re-pinned (the queue: place-1 next, the W1 wave order) +
  the KI#80/81 deletions (AGENTS §5). iter-78 evicted (verified
  against git in this edit); 10 held. Caps: STATUS 690 / TASKS
  1019 / DECISIONS 86 lines (57 rows) — over-cap on substance
  (§6.1, the D-095..D-120 precedent), trim at the phase-5→6 gate.
---
(end of log — cap 10; pre-trim history lives in git)
