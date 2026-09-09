# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2. Done-detail lives in git
> history + `worklog.md` + the owning docs — never restated here (KI#7
> cleanup, iter-0v). Day-tags removed per D-029 (calendar dropped); the
> build sequence is iteration-counted (`MVP_SCOPE.md` §17).

## Track A — main (simulator, no LLM)

> Phase 0 closed (gate PASS, iter-6; audit-clean iter-6a). Phase 1 closed
> (gate PASS, iter-26, D-058; the polish menu tune-1/tune-2/pack-2 landed
> iter-27–29). Phase 2 closed (gate PASS, iter-35, D-064 — 35/35 boundary
> validity over 51 combined utterances, 0 honest misfires; the parse corpus
> 10 cases + the full §5 protocol re-run, M1/M2 identical to iter-26).
> Phase 3 (Director) CLOSED — see the condensed ledger below. Phase 4
> (Knowledge & scene) CLOSED — gate PASS iter-65, D-094 (opened iter-55,
> the owner's "start phase 4" call; the backlog below was drafted from
> `docs/blueprint/phases.md` §4 — the phase's architecture owner; every
> declared row landed). Phase 5 (Depth) **OPEN — opened iter-73, the
> owner's start call (D-105)**; the backlog below drafted from
> `docs/blueprint/phases.md` §5 + the D-096 drafting material (in place
> since iter-66a). Architecture owner: `docs/blueprint/phases.md` §5;
> exit criterion "an emergent chain of 3+ events without the player"
> (ROADMAP §2 — T8's OFF arm already reads 26 chains on the committed
> scenario; the phase-5 target is the worldgen-fed form).

### Phase-5 depth backlog (opened iter-73; the owner's start call, D-105)

- `depth-1` · the acquisition gate — **done (iter-73, D-105;
  collapsed iter-77 per the header law — the detail lives in git +
  worklog + D-105)**: acquisition_fidelity at the resolve point,
  pack-linted closed condition vocabulary, the committed pack
  unarmed (v0.1 bytes). Detail: tests/test_acquisition.py.
- `depth-1b` · the acquisition arming — **done (iter-74, D-106;
  collapsed iter-77)**: the pack's `position_visibility.acquisition`
  block + location flags; corpus price paid fidelity-only. Detail:
  tests/test_acquisition.py.
- `depth-2` · lazy detail materialization, the gate — **done
  (iter-75, D-107; collapsed iter-77)**: the `scene:<id>:detail`
  stream family + `materialize_scene_detail` + the `detail_claim`
  mirror + the lint; zero corpus price by construction. Detail:
  tests/test_detail.py.
- `depth-2b` · the scene-detail ARMING — **done (iter-76, D-108;
  collapsed iter-77)**: the pack's `scene_detail` block; the price
  measured both arms, paid fidelity-only; zero new knowledge tokens
  (D-108). Detail: tests/test_detail.py.
- `depth-3` · scene LOD (three zones) — **done (iter-91, D-125)**: the
  zone family `core/lod.py` (the partition, the census) + the LOD
  filters on the decay/urgency walks + the loop's warm ring at the
  macro crossings (the one-gate law: the unarmed pack is the
  one-scene world, the v0.1 bytes) — the macro clock's first
  consumer, `cold_npcs` on the turn. Detail: tests/test_lod.py.
- `depth-4` · fold checkpoints — **done (iter-80, D-114)**: the
  chronicler-family derived artifact (fold-checkpoint + event-index
  offset, `core/checkpoint.py`) + the sha256 index-anchor (intake-4);
  rollback = snapshot + tail replay, verified by re-fold; the resume
  door stays owner-gated (phases.md §7). Detail:
  tests/test_checkpoint.py.
- `depth-5` · the ordered worldgen passes — **done (iter-81, D-115)**:
  the pass family `core/worldgen.py` (PASS_ORDER, integer-only
  geometry, `worldgen:<pass>` streams — the D-079 family's fourth
  member, `detail_claim`'s first legal caller, the genesis at open
  time seeding the director's buffer; NO knowledge records — the DF
  epistemology-empty discipline); the committed pack unarmed at the
  landing (the 68a pattern — zero draws, zero events, v0.1 bytes; the
  arming is depth-5b below). Detail: tests/test_worldgen.py.
- `depth-5b` · the worldgen ARMING — **done (iter-83, D-117)**: the
  committed pack's own `worldgen` block (the map + chronicle + claims)
  + the `world_history` template line (the `{year?…}` shape branch +
  the claim clauses — the flat claim keys are the binding surface) +
  the story-critical listing; the corpus price measured BOTH arms
  first (the genesis events alone + the mechanical id shift — the
  fingerprint pinned equal; the T1 fixture regenerated, the corpus
  fixtures re-pinned, the murmur's release moved to the first quiet
  beat as the pre-seed's designed price); the M5 run-start note (the
  genesis prefix counts as non-PC); the D-116 additions — CONDUCTANCE
  (the lint computes the genesis importances through `pack_importance`
  against the tale gate — dead template lines are dead data),
  REACHABILITY (L1: every claim names a live consumer — a template
  line binding the slot or a director hook reading the pair), the
  genesis×resume pins (double `open()` loud at the header guard, the
  checkpoint flow, the entities/config drift guards), the reserved
  claim-slot law; NO lint ceilings (D-116 held). Detail:
  tests/test_worldgen.py.
- `depth-6` · factions with goals — **done (iter-92, D-126)**: the
  small-formula dynamics `core/factions.py` (the KeeperRL
  ratio+threshold over the members' LIVE per-entity axes — D-006
  holds, never a stored group score; the `faction:<group>:<kind>`
  roll stream, the D-079 family's fifth member) + the group entity
  kind (`entities.json::groups`, D-112's one id all tiers — the
  faction acts through the intent door, actor = the entity id) + the
  `factions` pack block (closed vocabulary, pack-linted) + the walk
  at the beats and the crossings (the scene-LOD scoping by the
  faction's ANCHOR, depth-3's one-gate law); the committed pack
  unarmed (the 68a pattern — zero entries, zero draws, the v0.1
  bytes; the arming rides with a future content row). Detail:
  tests/test_factions.py.
- `depth-7` · groups & simulation LOD — **done (iter-93, D-127)**: the
  write-side LOD at group scale, D-112's ratified resolutions executed
  — the `member_of` state door (D-020's pair-relation: no fold seed,
  absence IS None — the D-054 slot shape; the fold validates every
  join/leave/transfer from-value), the population tier
  (`core/groups.py::macro_tick_drafts`: one aggregate event per cold
  group per macro crossing, actor = the group id, the unborn
  population's count under `population` — a live fold read, draw-free),
  the condensation on crossing the warm transition (ONE event per
  group: the un-born members' canon births — the D-054 promotion shape
  at group scale, already-holders skipped — plus the write-once
  tombstone marker; detected at the zone recomputations, beats AND
  crossings, the load state the origin), the per-group opt-in (the
  group record's `macro_event`/`condense_event` — template-closure
  linted, memberless refused as dead data; without them depth-6's
  intent-door actor alone — zero re-pins, the depth-6 pinned behaviors
  pass unchanged); the loop order at the crossing: turn →
  condensations → aggregates → warm drift → rolls; the unarmed law
  keeps the one-scene world. +23 tests, 1493→1516+1 green, corpus
  price zero measured both arms (the inert twin byte-identical seeds
  42/0/125; the armed delta the tier families alone, the fingerprint
  equal). Detail: tests/test_groups.py + D-127.

### iter-77 · meta-analysis routed candidates — LANDED (the owner's
iter-79 verdict call executed; every row below collapsed per the
header law — the detail lives in git + worklog + D-110..D-113)

- `pred-failclosed` · **done (iter-79, D-110)**: §3's blanket
  fail-closed restored — missing → False under ALL comparators in
  both twins; the equals-null hole closed by the lint ban.
- `pred-contract` · **done (iter-79, D-111)**: the `_require` family —
  ValueError on every raw-read surface (6 sites), KeyError never
  leaks.
- `seq-owner` · **done (iter-79, D-113)**: the split landed —
  NAVIGATION §3 (ORDER → STATUS Next step; composition → TASKS) +
  the bootstrap text (chat-side).
- `rule9-resolver` · **done (iter-79, D-113)**: Rule 9 defined in
  AGENTS §7 (census verified 25 hits / 8 files + worklog).
- `verify-seed` · **done (iter-79, chat-side per D-113)**: the
  bootstrap verify line gains `PYTHONHASHSEED=0` — §10 alignment;
  repo untouched (the suite is seed-agnostic, the guard was the
  rejected crutch).
- `archive-protocol` · **done (iter-79, chat-side per D-113)**:
  BASE_COMMIT.txt + owner-runs-git + inline-diff fallback adopted
  into the bootstrap; the metadata-never-in-worktree clause included.
- `tn12-claim` · **done (iter-79, D-113)**: the claim DROPPED — no
  §12 landed; each of the five proposals already had an owner
  (D-109/§8.5 gap rows, D-109's snapshot law, §8.1 Layer 2, YAGNI);
  zero diff (no §12 reference in the tree besides the claim's own
  record).
- Re-raise guard (iter-78, the owner's ignore-list ruling — re-flag
  only with NEW measured evidence): LLM-drift / rate-limit /
  token-econ concerns are already TEST_PLAN §8.1–8.5 law + the gap
  rows (Layer 1 = fence, L2/3 = advisory — new mechanisms are YAGNI);
  stream-name injectivity holds by construction (kinds are a closed
  ":"-free vocabulary; the scene family's lint docstring pins "map
  keys, injective by construction" — a lint is L1 noise); the FAQ
  aging + cap trim ride the phase-5→6 gate; the sandbox essay's
  value-prop section (its own §9, chat-side — no repo section) is
  correct self-description, no action.

### Research intake 4 (iter-73; the phase-5 synthesis cross-review, routed)

> The owner's 2026-09-08 analysis session: a two-model chain (a
> phase-5 synthesis text + its cross-review) verified against
> HEAD `742d7e9`/`198b657` before intake — every load-bearing claim
> landed against the owning docs/code. The reinvented half (the
> D-055/D-062 file contract, engine-1's owner gating, the scoped float
> law, the three-zone LOD design) is already law or already-drafted
> material — no new decision owed there; the violations the texts
> proposed (the queue-key change, a mypy-in-CI tool against §10, the
> global float ban, a snapshot anchor event in the canon log) are
> refusals on record. The two confirmed additions routed below; the
> numbering intake-4 follows the landed intake-3 (iter-71).

- `sha256` integrity anchor on the fold-checkpoint's derived-index
  record — done (iter-73, routed to phases.md §5, depth-4's row):
  byte-deterministic serialization, verified by re-fold, never an
  event in the truth.
- pack-declared margins on any future threshold-crossing surface —
  done (iter-73, routed to phases.md §5, depth-1's row): deadband,
  never entropy.

### Research intake 5 (iter-82; the generator-concept verdict set, routed)

> The owner's 2026-09-09 concept text — a two-pass-verified analysis
> of the generator's state (three independent clone reviews + a
> worldgen/space/dimensionality memorandum + a procedural-generation
> essay, with an economics/culture donor digest) — cross-checked
> against HEAD `0d6a3bf` before intake; the load-bearing claims
> confirmed on the code this session (the scene-line pack-record read
> at `brief/assembler.py`; the importance trap — world_formed 0 /
> history 1 / gate 2; the O(extent²·N·R) relax; the double
> `_neighbors`; the absent `worldgen` block in the committed pack;
> the 4 claim fields / 8 biomes / 4 history verbs). The verdict set is
> D-116 (each question a best-of-variants synthesis); the wave plan
> routes below, W0 → W4. The concept text itself stays outside the
> repo (the convenience-copy law, STATUS FAQ).

- `bridge-1` · the scene-line projection pipe — **done (iter-86,
  D-120)**: the scene fields read the FOLDED PROJECTION (the committed
  claims ride world_formed's state_changes into the fold; the pipe
  test: an armed claim visible in the brief of the scene that claims
  it, determinism pinned), the pack record the fallback for unclaimed
  fields (the card law preserved — static surface first, event-born
  news last, the claims ARE event-born; L3 held, read-side derive);
  the corpus price read-side zero by construction (no runtime byte
  reads `scene_line_fields` — the T1 + corpus fixtures byte-identical,
  zero re-pins; the price paid is the visible claim tokens alone);
  the pack migration (scene_line_fields += the three claim slots) +
  the lint pair (the _brief legal set gains the armed claim slots,
  defensively; the reachability lint gains the scene-line consumer
  arm — the claims' first brief-side consumer). Detail:
  tests/test_brief.py + tests/test_worldgen.py.
- `chron-2` · chronicle v2, the history bridge (W1) — **done (iter-87,
  D-121)**: the history events gain the DF legends shape
  (participants — two distinct regions, the run's root anchor's draw
  inherited by its members, the DF collection's role fields; places —
  one site per event; world_formed carries neither) and the cause
  TREE (L7 — the chain visible at record time: a member chains to its
  nearest lower-tier predecessor, a top-level event to the previous
  top-level, the flat form the linear chain; the drafts ride a parent
  map the loop resolves through the writer's own ids — the id law
  single-owner); the war→battle→episode hierarchy as a PACK-DECLARED
  collection vocabulary (`chronicle.collections`, the DF
  `event_collections` donor shape, L10: JSON + lint, never string
  languages — the tiers root-first, the root anchors, the nested
  tiers carry the member caps; the walk draw-free, the grouping
  opportunistic per the DF measurement); HISTORY_KINDS stayed closed
  (the 4 verbs; the collection types are the pack's layer); template
  closure linted at alternative granularity + the reserved-slot
  family widened (the history outcome keys) + capitals ≥ 2 (the
  participants' two sides); the committed pack declares feud →
  quarrel; the corpus price: the pass-1 stream positions frozen (the
  drawn years/kinds/hooks verbatim, the murmur's pre-seed pins
  stable, zero corpus re-pins), the T1 fixture the one re-pin (4
  outcome lines). Detail: tests/test_worldgen.py + D-121.
- `place-1` · placement discipline (W1) — **done (iter-88, D-122)**:
  the claim↔exits consistency lint — every exits edge joining two
  CLAIMED locations reads sites within the pack-declared
  `place.max_edge_span` lattice steps (`worldgen.place`, the graph's
  edge contract: the METRIC is the engine's row-major Chebyshev
  `lattice_distance`, the THRESHOLD the pack's — never engine
  geography knowledge, INV-3; two locations joined by exits never
  read sites from opposite corners of the map — the map↔graph
  coherence the derived travel prices of st-6a read, D-116 (5)); the
  vacuity law (a span at the lattice diameter accepts every pair —
  dead data, the single-tier twin law, never a policy ceiling); the
  passes never read `place` (load-time law alone, the runtime
  backstop stays six-block); the committed pack declares span 1 (the
  tavern↔street pair: sites 0 and 1, one step); KI#82 (the
  missing-sub-block KeyError leak) opened + fixed in the same
  iteration; corpus price zero (lint-side + pack data alone — the T1
  + corpus fixtures byte-identical, zero re-pins). Detail:
  tests/test_worldgen.py + D-122.
- `geo-1` · the geometry rework (W1, BEFORE any big-world pack) —
  **done (iter-89, D-123)**: the grid-hash neighbor walk (buckets at
  spacing scale — `_neighbors` O(N) amortized under the ring-floor
  exactness law, computed ONCE and shared by watershed + biomes), the
  relax pass's per-site bounding-box walk (the ×N factor leaves the
  cost: each lattice point examined once per covering site, O(extent²)
  total — the old O(extent²·N·R) wall measured on HEAD first, 2.27/
  11.77/37.81 s at 400/900/1600 sites, the quadratic fit ~25 min at
  10k), the worldgen perf profile (`scripts/worldgen_profile.py`, the
  perf-1 precedent — the ladder 36→10k, clean + cProfile double-run,
  the fingerprints compared; the numbers in TECH_NOTES §12: the 10k
  site full door 1.19 s clean, sites/s ~8.4–10k, the cost
  draw-linear). NO lint ceilings (D-116: policy ≠ correctness — the
  queue order is the enforcement). Corpus price zero, measured both
  arms (the genesis fingerprints seeds 0/42/125 byte-identical, zero
  re-pins); the exactness oracles (the pre-geo-1 full scans as
  brute-force references) in tests/test_worldgen.py. Detail:
  tests/test_worldgen.py + D-123 + TECH_NOTES §12.
- `maclock-1` · the macro-clock primitive — **done (iter-90, D-124)**:
  `core/macro.py` (the cadence rule — the positive multiples of the
  pack-declared `time.macro.cadence_ticks`, the loop's THIRD crossing,
  coarsest-first at a co-occurring tick; the macro-year counter —
  `start + t // cadence`, derived never stored, the calendar binding
  to the worldgen chronicle horizon; the aggregate emission surface —
  `macro_turn_draft`, one event with cardinality, the D-112 shape) +
  the `time.macro` lint + 18 tests; the committed pack UNARMED (the
  68a pattern — the arming rides with the primitive's first
  consumer), corpus price zero measured both arms. Detail:
  tests/test_macro.py + D-124.
- `name-1` · the name generator (W2, beside depth-7) — todo:
  pack-declared phonotactic profiles (culture-keyed n-gram pools —
  the CK3/Azgaar donor shape; deep dive owed at the row: ref-19,
  DEEP §1), pure functions over per-stream draws (the D-079 family
  law; INV-2 deterministic, INV-3 clean — phonotactics are pack
  data, the generator is pure functions); the consumers: depth-7's
  condensation canon-birth events (region_00 does not scale) +
  world-2's cultures. Output linted against the entity namespace
  (no collision).
- `world-2` · the second world, the phase-6 gate's own instrument
  (W4, owner-gated — new name: pack-2 is the made iter-29
  door-check) — todo: the TWO-LEVEL gate — level 1 the T1 reskin
  ≤ 1 day (ROADMAP §2's phase-6 exit, measured on this pack),
  level 2 the deep second world (weeks — VISION §7's honest twin;
  the mero distinguishing a reskin from a real world). A fantasy
  province at pack scale (the concept's W4 shape); the phase-5 exit
  needs NO second world (the emergent chain rides the armed
  committed pack, depth-5b + the worldgen hooks).
- `res-1` · the resource/economy layer (W4, owner-gated, phase 6 —
  VISION §6's "scarcity" formula word gets its row owner) — todo:
  the closed scarcity cycle (source → flow → sink) as PACK DATA: the
  dependency graph (nodes/edges, integer inventories as state on the
  existing surfaces), flows as aggregate macro-events on maclock
  cadence (a convoy loss → a station's halt — the X4 cascade shape),
  sinks via the existing irreversible item laws (the INV-5 family),
  price spreads as derived read-side values (L3); never a second
  economy engine beside the canon door (D-116). Deep dives owed at
  the phase-6 opening (ref-18/ref-20, DEEP §1).
- `roads-1` · the generated-exits pass (W4, owner-gated, phase
  6/mode G) — todo: mode G must EMIT exits for generated worlds
  (hand-authoring a generated world's edges is impossible — the
  concept's §8.6 measured need); an MST/k-nearest graph over the
  sites (the Red Blob family); a PASS_ORDER growth = a D-row when it
  lands (core change, the closed-vocabulary discipline); authored
  packs keep manual exits (the pack wins).

> W3 closes without new rows: the calendar binding is maclock-1's own
> (D-116), weather-1's row stands (intake-3 — its gate read as
> bridge-1 + maclock-1 landed), directions are pack data over the
> graph today (zero core — no row owed until a measured need).

### Research intake 6 (iter-85; the consolidated-analysis residue, cataloged)

> The owner's 2026-09-10 external text (an economy/social/procedural
> consolidation, the D-096/D-116 intake family) verified against HEAD
> `cf8d06e` before landing: ~80% already landed or cataloged; the
> verdict set is D-119 (catalog / defer / refuse). NO new backlog
> rows: the three donor rows landed in REFERENCES §10 (Dune → res-1's
> pack-declaration shape; Warhammer 40k → depth-6/PACK_SPEC
> prohibitions framing; Outer Wilds anti-reference — knowledge-as-
> progression refuted). The deferred residue — the medieval
> record-systems dictionary (the economic half rides res-1, the social
> half PACK_SPEC) and ethos mutagenesis (the phase-6 culture rows) —
> lands on the EXISTING owner-gated W4 rows at the phase-6 opening,
> just-in-time. Actor Model + CRDT refused (INV-2/L4/T1/L13 — the
> pros already delivered by SCHED-1/STATE-1/D-114/single-writer log).
> The text itself stays outside the repo (convenience-copy law).

### v0.2 refinement backlog (opened iter-66; the owner's post-gate quality pass)

> The research review's confirmed holes, landed additively — one family
> row D-095; no breaking schema change; every landing measures its own
> corpus price first (the both-arms law).

- `prosefloor` · the invented-entity prose floor (C2'') — done
  (iter-66, D-095; detail: VALIDATION_SPEC §2.1).
- `beliefwire` · the `trait_held` leaf (a requires-GATE, never a
  multiplier), the traits channel into the loop's reads, the
  counter-family in the fold — done (iter-67, D-097; detail:
  INTENT_SCHEMA §3/§4 + tests/test_beliefwire.py).
- `beliefwire-2` · the pack arming — done (iter-70, D-103): the
  relief guard's trait-gated scan (the new-entry shape — the guard_01
  re-gate refused on record) + the counter-family content (the arson
  fled line, the counters trio at the threshold bar); the price paid
  in the landing: +3 scans on the canonical seed-125 run only, the
  seed-93 narrator family re-distilled (11 id re-pins), the M1 pair
  0.54/0.52, the KI#77 lint-order fix riding the arming. Detail:
  tests/test_beliefwire.py + the D-103 row.
- `rumordrift` · A2'' — done (iter-68a/68b, D-099/D-100): the
  mechanics + the stream-isolation law + `drifted_from` in outcome
  (EVENT_SCHEMA §3, §11 no-bump); the pack ARMED (68b) — the
  `figure_deeds` family (the two crime sightings), the monotone
  0/30/50 ladder, the measured corpus price ZERO (every corpus talk
  tells a non-member token), live on the guard-talk geometry (12/22
  seeds hit). Detail: tests/test_rumordrift.py.
- `suspectaxis` · per-target suspicion, the drift teeth's first
  consumer — done (iter-69, D-101, mechanics declarative-only: the
  `{source, figure}` mapping, the `pair.<figure>.<axis>` home, the
  parameterized flip/arrest — the committed pack stays flat, corpus
  price ZERO by construction + byte-measured; the blame surfaces live
  on crafted packs, the 68b guard-talk geometry reused. Detail:
  tests/test_suspectaxis.py).
- `suspectaxis-2` · the pack arming — done (iter-69b, D-102): the
  committed pack's per-target switch, every flat-mode pack reader
  re-declared on the pair home, `figure_starting_fire` live
  (witnessed_arson 30). The corpus price measured FIRST both arms and
  paid in the same landing: the 8 state claims re-pinned + the
  arson-action cases' stream shifts (the witnessed-arson reactions, the
  seed-93 arrest family) through the fixed-point re-distill — 31 claim
  edits, the projection's undercount recorded in D-102. Detail:
  tests/test_suspectaxis.py.
- `testproto` · the intermediate-build LLM-integration test protocol —
  done (iter-68, D-098 — research, doc-only): the fork closed by
  decomposition into the three-layer spiral (contract simulacrum /
  live probes / gate heartbeat) over one pinned corpus + one metric
  vocabulary; the anti-trap corpus-growth law; the deviation corpus
  + the world-answer law (the owner's living-world clarification,
  2026-09-07). Detail: TEST_PLAN §8; the live half: bg-8 (below).

### Research intake 2 (iter-66a; the depth-architecture review, D-096)

> The external depth-architecture review (2026-09-07), verified against
> the repo before intake — D-096 records the three corrections and the
> routing. The phase-5 design material lives in
> `docs/blueprint/phases.md` §5 (the never-before-opening law, STATUS
> Next — drafted into TASKS only at the phase-5 opening), never here.

- `prosefloor-2` · relations/attribute claims in prose — done
  (iter-72, D-104: the DETECTION surface only, D-096's routing — the
  two assertion slots + the modeled-vocabulary split in
  `brief/scan.py`, a measurement export for bg-8's weaker-engine arm;
  no refusal, no wiring, corpus price zero by construction; detail:
  VALIDATION_SPEC §2.1 + tests/test_scan.py).
- `packtaxonomy` · material-derived props (the flammability
  generalization) — owner-gated (phase-6 PACK-1: the authoring path is
  the reserved `copy-from` chain, phases.md §6; a runtime
  material-to-props fold would be core code — the fork is the owner's).
- `story-critical objects` · the `story_critical` pack flag, director
  activation through NPCs — owner-gated (phase-5+; the director
  grammar, DIRECTOR_SPEC — events already have the arc/hook/complication
  family, objects would need the flag + a release path; detail: D-096).

### Research intake 3 (iter-71; the owner's vision-vs-repo cross-review, routed)

> The owner's 2026-09-08 analysis session: two external model reviews
> cross-checked against HEAD `0b09508` (1240+1 green, ruff clean,
> re-verified) before intake — every factual claim landed against the
> owning docs/code. The fabricated mechanics in the reviewed texts
> (texture durability params, fade timers, autonomous intents
> addressing texture) are D-049/D-054 refusals on record — no KI, no
> new decision owed. The two confirmed holes route below; the
> sequencing (prosefloor-2, then the phase-5 start signal) is STATUS
> Next's.

- `weather-1` · ambient weather + canon erosion — todo, owner-gated:
  weather as ambient-channel events (the director's seeded
  consequences, TIME-1) + erosion of promoted canon objects via
  `state_changes` in seeded follow-ups (the arson family's shape);
  all pack data over the existing doors (INV-3) — no TTL, no turn
  counters, no decay timers (D-049); persistence is the promotion
  door's (st-2). Gate: phase 5 (the ambient channel + macro clocks
  — bridge-1 + maclock-1 both LANDED, the gate satisfied) or pack-1;
  the macro cadence the ambient family rides is `core/macro.py`'s
  (maclock-1, D-124 — the committed pack's arming rides here, the
  primitive's first consumer).
- `companion-1` · the companion/party role — todo, owner-gated: pack
  data over the existing doors, zero new core systems — follow-duty
  in the rotation/urgency grammar, mode B actors voice (scene-1),
  pair-relations axes, presence re-verification (iter-61), the landed
  arrival-snapshot knowledge records (iter-15/D-056 — what §5 still
  owns is the group-scale form). Dependencies BY REFERENCE, never
  duplicated rows (the D-076/D-081 refused-fork precedent): tune-3,
  st-6a, the resume door (phases.md §7). Gate: phase 5, after st-6a.

### Phase-4 backlog (opened iter-55; CLOSED iter-65)

- `leg-1` · trait crystallization (P3f) — done (iter-55, D-084):
  the belief-token fold. Detail: the D-084..D-093 family row +
  tests/test_traits.py.
- `leg-2` · the brief's derived-trait read — done (iter-56, D-085):
  belief lines lead recalled_facts. Detail: BRIEF_SPEC §3.5 +
  tests/test_brief.py.
- `leg-3` · reflection & memory compaction — done (iter-57, D-086):
  reflection-on-recurrence through the canon door. Detail:
  LEGEND_SPEC + tests/test_reflection.py.
- `leg-3b` · the tavern reflection set — done (iter-58, D-087): the
  arming, `conclusion_drawn` story-critical. Detail: LEGEND_SPEC §7 +
  tests/test_reflection.py.
- `retr-1` · the retrieval ladder (STORE-1) — done (iter-59, D-088):
  FTS5 + the vec probe/scan/floor chain + the re-ranker; `knower` IS
  known_by. Detail: tests/test_retrieval.py + phases.md §4.
- `scene-1` · the scene manager + mode B — done (iter-60, D-089):
  the chorus queue + the knower parameter. Detail: BRIEF_SPEC §3.9 +
  tests/test_scene.py.
- `scene-2` · the mode-B session wiring — done (iter-61, D-090):
  the drain + the actor reply door + the keyword query. Detail:
  BRIEF_SPEC §3.9/§7.1 + tests/test_scene.py.
- `tex-1` · the texture identity tier + quotas — done (iter-62,
  D-091): `identity_slots` + `per_entity_max_items`. Detail:
  BRIEF_SPEC §3.3/§6 + tests/test_brief.py.
- `leg-4` · mode F offline chronicler — done (iter-64, D-093):
  `scripts/chronicle.py`, the [chronicler] extra, D-012 executable.
  Detail: TEST_PLAN §7 + tests/test_chronicle.py.
- `blind-1` · the blind-NPC leak suite's phase-4 extension — done
  (iter-63, D-092): the exit criterion's instrument. Detail:
  TEST_PLAN §1.3.
- `scav-1` · offline compaction = scavenge with tombstones (the
  EventStore shape, phases.md §4's later half): derived-store entries
  drop with tombstones AFTER the chronicler's rollups make them
  rebuildable; committed logs never edited (INV-5). Out of leg-4's
  named scope by the scope-creep law — deferred here, not forced.

> Phase 4 (Knowledge & scene) landing ledger, condensed: the folds
> iter-55..58 (D-084..D-087 — traits, the brief's belief read,
> reflection-on-recurrence, the tavern arming), the retrieval ladder
> iter-59 (D-088), the scene stack iter-60..62 (D-089/D-090/D-091 —
> mode B + the chorus queue, the session wiring, the identity tier),
> the leak suite's instrument iter-63 (D-092), the mode F chronicler
> iter-64 (D-093 — the owner's duckdb approval crossing the §8 fence,
> the chronicler outside the runtime graph); the build column
> completed at iter-64, the gate PASS at iter-65. Architecture
> owner: `docs/blueprint/phases.md` §4; exit criterion "0 leaks on
> the blind-NPC suite" (ROADMAP §2 — MET). Detail: the
> D-084..D-093 family row + the per-row owners above + worklog +
> git (the pre-collapse detail lives there, KI#7 law).

### iter-65 · phase-4 gate — done (verdict: PASS, D-094)

Full ROADMAP §5 protocol re-run on the owner's call: the corpus 105
+ parse corpus green (1178 tests collected — 1168 passed + 1 module
skip pure-dev, 1177 passed + 1 offline-probe skip with the
[chronicler] extra; ruff clean); the seed-125 pair ON M1=0.509 /
M2=0.333 / OFF T8 26 chains ≥ 3 — IDENTICAL to the iter-54 record
(the phase-4 landings kept the corpus-price-zero promise on the
committed scenario); the stretch table max 1 (both arms — the
phase-3 exit criterion holds, no regression); T1 double-run
byte-identical; T7 reads as a story; the exit criterion re-measured
— 0 leaks on the blind-NPC suite (all four layers); the mode-F
chronicler acceptance green (TEST_PLAN §7: 53/53 through the count
gate, manifest content-derived, write_mode=stdlib in the offline
env). The doc debts paid: TASKS 626→589 (the phase-4 ledger
collapse — the deferred trim landing at its promised gate),
DECISIONS 30 held (D-094 joins the verdict family), FAQ 20 held,
README resynced (KI#73 — three landings had gone unrecorded).
Phase 5 unlocked — opens on the owner's call. Detail: worklog
iter-65 + D-094.

> Phase 3 (Director) landing ledger, condensed: the pacing stack
> iter-36..39 (D-065..D-068), the event grammar iter-40..42
> (D-069/D-070/D-071 — predicate/weight, options, on_action), the
> social stack iter-44..46 (D-073/D-074/D-075 — secrets, leverage,
> the echo), the arcs iter-47 (D-076), the content column
> iter-43/48/49/51/52/53 (D-072/D-077/D-078/D-080/D-081/D-082 —
> every layer and declared channel dimension live); the build column
> completed at iter-53, the gate PASS at iter-54. Architecture owner:
> `docs/blueprint/phases.md` §3; runtime contract owner:
> `docs/DIRECTOR_SPEC.md`; exit criterion "a scene without an event
> < N beats" (ROADMAP §2). Detail: the D-083 compound row + worklog.

### Phase-3 director backlog (opened iter-36)

- `dir-1` · pacing clock — **done (iter-36, D-065)**: the per-run
  RAMP/PEAK/REST/STAGNATION clock over narrative entropy; `director.pacing`
  pack data + lint; clock-gated stagnation releases; explicit triggers
  ungated (D-005). Detail: the D-065/D-066/D-067/D-068 compound row +
  DIRECTOR_SPEC §5 + TEST_PLAN §6.
- `dir-2` · the eventless-stretch instrument — **done (iter-37, D-066)**:
  `core.metrics.eventless_beat_stretches` (the exit criterion's
  measurement) + the harness `--pacing on|off` A/B; measured 1000 seeds:
  max stretch 1, both arms byte-identical (the all-PEAK law). Detail:
  TEST_PLAN §6.
- `dir-3` · layered thresholds + `PEAK_CLIMAX` — **done (iter-38, D-067)**:
  the third entropy layer `climax_floor` (75 = 3× the peak floor) + the
  climax release path (boss beats END peaks, the option gate consulted, a
  closed boss never burns) + the one-beat PEAK_CLIMAX state. Detail:
  DIRECTOR_SPEC §5.
- `dir-4` · multi-channel policies — **done (iter-39, D-068)**:
  `director.channels` (threat/social/ambient, the L4D family) +
  `SeededHook.channel` + the per-hook quiet gate (`permit_quiet`); the
  clock/budget/climax/explicit triggers stay global on purpose. Detail:
  DIRECTOR_SPEC §5.
- `drama-1` · the event grammar, predicate + weight layer — **done
  (iter-40, D-069)**: trigger predicates as JSON (`core/predicates.py`:
  leaves + compounds + the prop leaf), the `weight_multiplier`, the
  `first_time_only` burn; MTTH stays the named anti-pattern. Detail:
  DIRECTOR_SPEC §3/§3a.
- `drama-2` · the grammar's option layer — **done (iter-41, D-070)**:
  option blocks with availability gates + ai_chance-style weighting (a
  pure deterministic pick), payload overrides whole-key; the
  immediate/option/after lifecycle maps onto seed/choose/apply. Detail:
  DIRECTOR_SPEC §3b.
- `drama-3` · the on_action dispatch layer — **done (iter-42, D-071)**:
  the pack table keyed by committed event type, appended after the
  hardcoded reactions (append-not-overwrite), the witnesses scope + the
  quantified gate + the alarm-shaped state change; one-hop lint. Detail:
  DIRECTOR_SPEC §3c.
- `content-1` · the document_check content set — **done (iter-43, D-072)**:
  the 14th action over the inspect resolver (the verdict token → the
  standing arrest machinery), the climax flag live on the watcher pair,
  the crowd reaction, the 4-case corpus regen. Zero engine edits. Detail:
  the D-072/... compound row + TEST_PLAN §6.
- `social-1` · secrets & leverage as fact clusters — **done (iter-44,
  D-073)**: `core/leverage.py` + `rules.json::secrets` (the CK3 add_hook
  precedent): a novel knower mints a `leverage_gained` fact event; expiry
  a read-side fold; ONE live token; the 9-case corpus regen paid. Detail:
  the social-stack compound row.
- `social-1b` · the leverage use — the coerce door — **done (iter-45,
  D-074)**: the 15th action over the coerce resolver: `leverage_over`
  (the door's first fold-reading precondition), the spend a NEW event
  naming the cluster (one secret buys one play), the unconditional
  tick-window OCC re-check, the balance as pack data. Detail: the
  social-stack compound row.
- `social-2` · psychological echo (P3e) — **done (iter-46, D-075)**:
  `core/echo.py` — the residue as a pure read-side fold (per-NPC
  valence, linear decay, fidelity-scaled; writes nothing, feeds no
  entropy — L6) + the `echo_at_least` behavior gate. Detail: the
  content-column compound row.
- `arc-1` · arcs & tension shaping (P3c) — **done (iter-47, D-076)**:
  `director.arcs` pack chains — the ORDER law + the GAP law + the
  entropy mirror (the burn law's twin) + the one-sided membership lint;
  dormant until content-6. Detail: the D-076/D-081 compound row.
- `content-2` · the alarm panic echo — **done (iter-48, D-077)**: the
  through-the-walls law as one on_action entry (panic_ripple, witnesses
  +10 fear), story-critical with its own line, zero engine edits; the
  7-case corpus re-distill paid. Detail: the content-column compound row.
- `content-4` · the coerce driver — **done (iter-49, D-078)**: the
  drunkard's urgency entry re-armed by the REPLACEMENT law (the draw
  count holds, the corpus ladders hold); 4 seed-93 cases see the spend;
  the corpus regen via the fixed-point runner. Detail: the social-stack
  compound row + the STATUS regen FAQ.
- `content-5` · the echo driver — **done (iter-51, D-080)**: the
  jittery-watcher beat (the guard's `look_around` over `echo_at_least
  dread >= 15`, p=100 the compulsion semantics); the wariness arm
  measured and refused; the corpus ZERO broken pins + the deliberate
  pins. Detail: the content-column compound row.
- `content-6` · the arc driver — **done (iter-52, D-081)**: the
  aftermath chain `[the relief's check, the barkeep's wary sweep]` gap 2
  — the gap law LOAD-BEARING (the unchained sweep would land before the
  check: a causality lie); the closing beat riding the climax path; zero
  corpus re-distill. Detail: the D-076/D-081 compound row.
- `content-3` · the ambient driver — **done (iter-53, D-082)**: the
  drunkard's ramble, the room's murmur (the L4D Music analog) — the 16th
  action + the weight-0 ambient hook (the channel's own quiet gate its
  only road), seeded on the wait action's hooks (the resolver-sparse
  minting gap closed); day1 birth-record-only, the quiet march pinned.
  Detail: the content-column compound row + TEST_PLAN §6.
### iter-54 · phase-3 gate — done (verdict: PASS, D-083)

Full ROADMAP §5 protocol re-run: the corpus 105 + parse corpus green
(973 tests, ruff clean); the seed-125 pair ON M1=0.509 / M2=0.333 /
OFF T8 26 chains ≥ 3; the stretch table max 1 (both pacing arms + the
quiet-walk stage — the D-066 question answered); T7 reads as a story.
The doc debts paid: DECISIONS 48→30, FAQ 23→20, TASKS 854→510,
DIRECTOR_SPEC 641→593, phases.md kept over per §6.1 (the worklog
records why). Phase 4 unlocked — opens on the owner's call. Detail:
worklog iter-54 + D-083.

### Phase-2 parser backlog

- `parse-2` (owner-gated) disambiguation buttons + multi-intent
  utterances — deferred with a frontend consumer / live-session
  evidence (PARSER_SPEC §7).
- `engine-1` (owner-gated) the runtime inference engine decision
  (llama.cpp + GBNF; TECH_NOTES §1) — unlocked by the phase-1 gate,
  waits on the owner; the dev-time external parser carried phase 2 to
  its gate PASS (iter-35) and carries mode C until then.

### iter-26 · phase-1 gate — done (verdict: PASS, D-058)

Full ROADMAP §5 protocol re-run: 109 live beats / 0 canon violations /
corpus 105 green; DECISIONS collapsed 41→30; `doc-1` closed clean;
phase 2 unlocked. Detail: worklog iter-26 + `docs/DECISIONS.md` D-058.

### Phase-1 tuning backlog (post-assembler, owner-gated)

- `tune-3` alarm-adjacent reachability (iter-21 session finding):
  `transitions.fire.knowledge.alarm_adjacent` (`shouting_near_<loc>`)
  is structurally unreachable in v0.1 — the token needs a knower
  adjacent to the fire location at ignition, but NPC placement is
  static (the rotation is a direct duty↔rest swap, playscript steps
  are player-only, urgencies are all waits), so the street/backyard
  are never occupied when the fire starts; the same-location half
  (alarm + fear spike) fires fine and is corpus-pinned. Session 8
  (iter-23) pinned the same family live on the §3 rumor leg: the
  market crowd holds no `figure_at_back_door_last_night` — the
  drunkard never leaves the tavern (the refusal is corpus-pinned,
  the boundary probed, not forced). Owner's
  call: a v0.2 pack NPC-movement source (e.g. a transit route
  through the street), leave as declared-but-dormant layer
  vocabulary (a second pack may exercise it), or phase-5 spatial
  material.

(tune-1 done iter-27, tune-2 done iter-28 — see Done.)

### Stress-test backlog (iter-11b resolutions; owner-gated)

- `st-2` identity persistence: the identity promotion door (pack
  grammar beyond `take`, the D-054 machine; blueprint §1) — the
  read-path half (the window tier + per-scope quotas) landed as
  `tex-1` (iter-62, D-091); only the door remains. Optional
  second trigger (bg-5): repetition-counted promotion — N repeats of
  a priced pattern via a counted fold (the ref-13 GHOST-layers
  counter pattern); owner's call: alongside or instead of the
  pack-grammar door.
- `st-3` groups & simulation LOD: one id across tiers, aggregate
  macro-clock events with cardinality, condensation on crossing
  (GROUP_SPEC trigger = phase 5 or owner request; blueprint §5).
- `st-4` the call budget (head + brief + tail + thinking + output ≤
  MECW target) + the transcript-tail contract + thinking-as-ephemeral-
  texture (the narrator-boundary iteration; blueprint §1) + the Script
  Tax clause (bg-5): non-Latin tail/prose costs ≈1.5–2× tokens on
  32K-vocab local models (guide part_07a §7A.5; ref-13) — the
  whitespace proxy under-charges Cyrillic; budget per script at the
  mediator, never in core.
- `st-5` containers: the `in` relation + entity-birth promotion
  (with `st-3`, phase 5; blueprint §7).

### Spatial backlog (owner analyses 2026-08-30, audited iter-19; owner-gated)

- `st-6` spatial vocabulary — `travel` + `layout` (the narrator's
  revisit-stability question: scene-scoped texture dies on
  `scene_close` by design, D-049, so important architecture must be
  canon from birth). (a) **`travel` as a separate action, NOT
  weighted `move`** — move semantics, `adjacent_to`, and the T1
  golden fixtures stay untouched; duration = pack-precomputed edge
  cost OR derived from the WorldModel (D-116: a pure integer function
  of distance + height/river modifiers at resolve time — generated
  worlds never hand-author prices; the pack override wins per edge;
  integer math, no runtime division in the resolver); mechanically legal today (`t + duration`, MVP_SCOPE §8;
  the clock jumps ahead so day-scale durations are queue-cheap;
  beats/rotations still fire mid-travel in tick order, D-038); macro
  clocks (L4) enter only when regions/worldgen arrive. (b)
  **`layout` — LANDED iter-20 (D-057/KI#48)**: a top-level pack
  field on every location rendered canon-from-birth on the scene
  line via `brief.present_entities.scene_line_fields` — no
  `initial_projection` seeding (the iter-19 claim that the gateway's
  canon_slot reads top-level pack fields only was WRONG: the check
  reads both prop sources, and a pack field was already guarded —
  the `exits` precedent, KI#41); the validator adjudicates claims on
  it; mutable decor stays texture (the existing door). The gates for
  (a): SATISFIED (depth-5 landed, D-115 — the phase-5 spatial layer
  exists; D-116 amended the price law above; place-1 LANDED iter-88,
  D-122 — the exits↔map consistency the prices read) — the row is a
  live candidate (maclock-1 LANDED iter-90, D-124 — the macro
  cadence the edge-state aggregates ride is `core/macro.py`'s).

### iter-6 · gate — done (phase-0 verdict: PASS)

Phase-0 gate closed; full evidence in `worklog.md` iter-6 + the
`docs/TEST_PLAN.md` spec. Track A was feature-frozen at phase-0 scope;
phase 1 (narrator over the log) opened per `docs/ROADMAP.md` §2.

## Track B — background (evenings, foreign canon)

### bg-7 · engine + confabulation probe — done (2026-09-07)

- Done one-liner: all five probes' FIRST NUMBERS on the sandbox API
  engine (glm-4-plus) — TECH_NOTES §10 (the 51-utterance corpus
  39/44 gate-valid after one re-ask vs the 35/35 operator baseline;
  the prose floor 0/24 beats and the sentence-initial gap 0/24; the
  claims-channel refusal engine = the brief-surface vs claim-id
  vocabulary mismatch; the Cyrillic twin tax ZERO; C3.5's thin 0→1
  signal; the surface A/B null). The `{3–8B, GBNF}` arm records the
  gap row (owner hardware — engine-1's decision input unchanged,
  TEST_PLAN §8.1 Layer 3's law); runner + transcripts outside the
  repo (Rule 9); prosefloor-2's gate now holds its numbers — the
  surface-section decision: no extension warranted by the API-engine
  numbers, the weaker-engine arm re-measures.

### bg-8 · engine — the LLM-integration test runner — done (2026-09-09)

- Done one-liner: the testproto live half LANDED (the owner's
  sandbox-simulation call lifting the hardware gate — the same API
  engine class as bg-7, glm-4-plus; the {3–8B, GBNF} arm stays the gap
  row) — the deviation corpus F1–F6 through the REAL mode-C door: **the
  world-answer law's first live numbers, coverage 34/34 = 100%** (the
  failures live in mapping quality: F3 invented names 1/6 — the guess
  engine, 4 wrong world actions committed; F4 unmodeled verbs 2/6 —
  closest-verb guesses; F6 injections 0/6 — two EXECUTED, the
  protocol-echo leak the run's only unanswered cycle; honest 17/36) +
  the heartbeat's first run (the parse corpus re-driven: 84.4 → 93.3%
  after one re-ask, refusal families DRIFT run-to-run — TEST_PLAN §8.5
  the baseline row). Transcripts re-distilled one way:
  `tests/fixtures/deviation_corpus.json` (Layer-1's calibrated
  worst-case repliers) + `tests/test_deviation.py` (the world-answer
  law's regression teeth, +8 tests, 1315 → 1323) + TECH_NOTES §11.
  Gap rows standing: the {3–8B, GBNF} arm (owner hardware), the bg-7
  prose families skipped this heartbeat (rate-limit economics), the
  per-family latency distribution. The candidate follow-on (pack-
  declared noun aliases) stays routed not forced — the F2 numbers
  (6/6 honest, the question fired) do not force it. Detail: TEST_PLAN
  §8.2/§8.5, TECH_NOTES §11.

### bg-2 · event taxonomy — DONE (bg-2-event-taxonomy)

- Done one-liner: `docs/TAXONOMY.md` (120 entries across the 16 target
  types; AC ≥100 MET) + `scripts/df_taxonomy.py` (the quantile-spread
  survey over the sink DB) + the sink v2 plus pass
  (`scripts/df_import.py` — D-051's deferral fired: theft/beast detail
  is companion-only, D-063). Measured findings + the bg-3 consumer
  caveats: TAXONOMY §4/§5; recipe: TECH_NOTES §3.2.

### bg-3 · briefer spike — DONE (bg-3-briefer-spike)

- Done one-liner: `scripts/df_briefer.py` — the POV mini-briefer (the
  participant-index prefix scan as the knowledge model; the assignment
  frame kept apart from the subject's records) + the closed-vocabulary
  reverse-validation gate (`supported | contradicted | beyond_records |
  unknown_*`; prose never parsed; the ≤2-regen ladder with the dry
  floor) + the retrieval stress harness (double-build byte-compare).
  Live session: 4 TAXONOMY §5-anchored cases, 31 claims — 19 supported
  / 12 deliberate-probe non-supported, 0 honest misfires; 1 regen
  recovery, 1 exhaustion. Numbers (brief p50 ≈ 2.9 KB on GB-scale
  exports; scan p99 ≤ 0.2 ms; 3 worlds, determinism PASS): TECH_NOTES
  §3.3; regression `tests/test_df_briefer.py`. The F7 honest
  expectation held — mechanics validated, not micro-event
  interestingness.

### bg-6 · SoW integration audit — todo (owner-deferred)

- Read-only pass over `github.com/jofizcd/Soul-of-Waifu` (registered
  2026-08-30 at the owner's request; the owner defers integration "until
  unavoidable"): extension points for a separate simulation chat mode
  (a new mode vs. invasive edits), where llama.cpp sits, what the
  frontend must NOT own (the dumb-terminal contract, VISION §10).
  Output: a TECH_NOTES section + the `SOW_INTEGRATION_SPEC` sketch.
  Unlocked by the phase-1 gate (D-058); owner-deferred "until
  unavoidable" (D-055). Never blocks track A.

## Infra backlog (pick by need)

- `mech-1` · the mechanics introspection CLI — **done (iter-84, D-118)**:
  the owner's agent-tooling call (an infra slot ahead of the queue's
  bridge-1 — the ORDER owner's prerogative, the queue itself untouched).
  `scripts/mechanics.py` (D-046 operator tooling, stdlib + core imports
  only, stdout-only): `matrix` (static wiring off the loaded pack —
  --event/--hook/--token/--prop queries + the unindexed-blocks fallback:
  a future layer is listed the iteration it lands, a shape rule joins
  later, never a rewrite), `trace` (the shadow replay — the log's events
  and beats through the real fold/Director/predicates, INV-2-equal to the
  runtime: the release-equality pin), `why --hook TAG` (the postmortem —
  seeded/armed/option-gate/entropy/pacing values; the law stays
  DIRECTOR_SPEC's, D-024), `blast` (the two-arm same-seed A/B — the
  corpus-price pattern; no resume door, both arms replay from t=0).
  11 pins in `tests/test_mechanics.py` (the exactness pin + the STATUS
  pins: the relief's check t=734, the sweep last t=1456); 1392→1403+1,
  ruff clean, seeds 0/42/unset.
- `engine-2` · the urgency-roll stream split — **done (iter-50,
  D-079)**: the owner's "quality over speed" fork call. Per-entry
  streams `urgency:<npc>:<kind>` (content-addressed, pack-linted
  unique, lazily registered, the assure nesting law reworked for the
  family); the single shared stream was measured and refused (the
  entries couple by draw position). Add-safety 10/10 day1_full
  byte-identical on the iter-49 refused scenario; the one-time flip
  paid (0/10, 2 corpus cases + 1 parse pin + 2 seed re-probes).
- `ci-1` GitHub Actions: pytest + ruff on push (`PYTHONHASHSEED=0`, pinned
  Python).
- `qa-1` mypy --strict on `core/` (owner-approval-gated: dev tooling is
  capped at pytest + ruff — AGENTS §8/§10; D-031 parks the candidate here.
  The type-discipline values are law from iter-1 via
  `docs/blueprint/phase0.md` §1; the tool is optional).
- `perf-1` 10k-tick timing profile — DONE iter-30
  (iter-30-perf1-profile): `scripts/profile_harness.py` (story phase +
  grid-aligned waits to the target; clean + cProfile double-run with a
  byte-compare probe — held at 10k ticks). 10k ticks ≈ 0.01–0.02 s
  write-side (~9.8k events/s), read side ≈ 0.017 s; cost is
  event-linear, schema validation dominates the per-event write cost;
  target met with ~3 orders of margin — no structural work warranted at
  v0.1 scale. Numbers owner: `docs/TECH_NOTES.md` §8.
- `balance-1` 1000-headless-sim distribution harness — DONE iter-6:
  `scripts/balance_harness.py` runs the gate playscript 1000× across
  seeds 100–1099 (director off), folds each log through
  `core/metrics.py`, emits a distribution table for M1–M5 +
  emergent_chains + suspicion peaks per NPC + destroyed-locations.
  Baseline (1000 seeds): M5 p50=0.77, emergent_chains p50=20, M3_mean
  p50=13.81, M1 p50=0.24 — full table at
  `output/balance_1000_seed100_off.txt` (gitignored runtime artifact;
  reproducible). KI#4 closed.
- `doc-1` VISION freeze review after the phase-0 verdict — DONE
  iter-26 (the phase-1 gate's doc-actualization sweep): the frozen text
  verified against phase-1 reality — the 3-layer shape, the call-budget
  law, the honest limits all hold; no changes, the freeze stands.
- `doc-2` REFERENCES.md license/URL re-verification, quarterly (alongside the
  TECH_NOTES review).
- `pack-1` Grim tavern pack candidate (post-gate; `PACK_SPEC.md` trigger —
  phase 6 or a 2nd setting): the romance/intimacy/coercion line as **pure
  pack data** — relation axes (`attraction`/`intimacy`/`loyalty`), status
  axes (`shame`/`anger`), a flirt→proposition action ladder,
  `consented`/`coerced` crafted knowledge records (D-008 pattern), seeded
  consequence hooks (jealousy, exposure, regret), dark templates, item
  extensions. Darkness levers per D-030; zero core change (axis-blind core;
  event vocabulary per pack, EVENT_SCHEMA §11). Distillation source:
  D-030 + the PACK_SPEC sketch row. Gate: the PACK_SPEC trigger
  (phase 6 / 2nd setting; the when-one-liner's owner is the STATUS
  FAQ, D-024 — the stale "phase-0 gate" clause removed iter-71).
- `pack-2` Arson-on-ashes guard (iter-2a audit note) — DONE iter-29
  (D-061): the `spot_available` door check (the closed precondition
  set's 15th test, layer-param lint-checked) — arson on a destroyed or
  fully-burning location is an `intent_rejected` no-op with
  `failed_test target.spot_available`, never the no-ignition success
  that pretended the world changed; the door-outcome vocabulary's
  fourth axis. The seed-41 corpus probe flipped with it (renamed
  `arson_on_a_destroyed_yard_is_door_rejected`).
- `pack-3` Sci-Fi setting candidate (owner sketches, 2026-08-30 chat;
  parked, not scheduled): frontier station / ark fleet / lawless
  asteroid belt / derelict megastructure. The sketches map
  mechanic-for-mechanic onto what already exists — watch rotations →
  station shifts, spreading rumors → leaks & paranoia, arson →
  sabotage / hull breach, theft → cargo/data theft, status markers →
  drunk/weary/afraid analogues per setting, pair axes + factions, watch
  change knowledge transfer → shift handover. Zero core change by
  design (INV-3's substance: a second pack must require zero ENGINE
  changes); blocked until the 2nd-setting gate (phase 6, same trigger
  as `pack-1`, ROADMAP §6).
- `ref-N` Reference deep dives — the plan table and the per-file index live
  in `docs/REFERENCES_DEEP.md` §1/§2 (single owner). All ref-1..ref-13
  items are done — status one-liners below; ref-16 (agent-memory-atlas,
  owner-supplied) was absorbed inside iter-8a, no solo iteration
  (`docs/ref/agent_memory_atlas.md`):
  - ref-1 DF worldgen — done (iter-0i) → `docs/ref/df_worldgen.md`
  - ref-2 C:DDA data/json — done (iter-0j) → `docs/ref/cdda_data_json.md`
  - ref-3 Paradox scripting — done (iter-0l) → `docs/ref/paradox_scripting.md`
  - ref-4 RimWorld + L4D + Alien — done (iter-0m) → `docs/ref/{rimworld,l4d_director,alien_isolation}.md`
  - ref-5 Wesnoth + Endless Sky + ink + tracery — done (iter-0n) → `docs/ref/{wesnoth_wml,endless_sky_dsl,ink,tracery}.md`
  - ref-6 Brogue + DCSS + KeeperRL — done (iter-0o) → `docs/ref/{brogue,dcss,keeperrl}.md`
  - ref-7 Generative Agents + ai-town + letta — done (iter-0p) → `docs/ref/{generative_agents,ai_town,letta}.md`
  - ref-8 Azgaar + Natural Earth + GeoNames — done (iter-0q) → `docs/ref/{azgaar_fmg,natural_earth,geonames}.md`
  - ref-9 libtcod + rot.js + Red Blob — done (iter-0q) → `docs/ref/{libtcod,rot_js,red_blob_games}.md`
  - ref-10 entt + Bevy + EventStore — done (iter-0r) → `docs/ref/{entt,bevy,eventstore}.md`
  - ref-11 SQLite FTS5 + DuckDB + sqlite-vec — done (iter-0r) → `docs/ref/{sqlite_fts5,duckdb,sqlite_vec}.md`
  - ref-12 Universe Audit Protocol — done (iter-0s) → `docs/ref/uap_audit.md`
  - ref-13 Live Character Guide — done (iter-0t) → `docs/ref/live_char_guide.md`
  - ref-17 DF designed experience (the player-facing half; owner-requested
    research pass, D-022 exception) — done (iter-8d) →
    `docs/ref/df_design.md`
- Candidates (owner-request only — D-022 law: no doc pass without a fresh
  owner request; both are synthesis-only today, cited via
  `CORE_DESIGN_RESEARCH.md` §2 and marked as such in the blueprint donor
  stacks):
  - `ref-14` The Sims — proprietary; patterns-from-papers only (D-015).
  - `ref-15` Prom Week — academic paper + GDC talk; no code repo.

## Done

- iter-40 · 2026-09-01 · drama-1 event grammar, predicate + weight layer — detail: worklog + the owning docs (D-row where named).

- iter-39 · 2026-09-01 · dir-4 multi-channel policies — detail: worklog + the owning docs (D-row where named).

- iter-35 · 2026-09-01 · phase-2 gate — detail: worklog + the owning docs (D-row where named).

- iter-34 · 2026-09-01 · owner-requested planning-layer audit — detail: worklog + the owning docs (D-row where named).

- iter-33 · 2026-09-01 · parse-1 batch 2 — detail: worklog + the owning docs (D-row where named).

- iter-32 · 2026-09-01 · parse-1 validation beats — detail: worklog + the owning docs (D-row where named).

- iter-31 · 2026-09-01 · phase-2 parser door — detail: worklog + the owning docs (D-row where named).

- bg-4 · 2026-08-31 · cost notes — detail: worklog + the owning docs (D-row where named).

- iter-30 · 2026-08-31 · perf-1 — the 10k-tick timing profile — detail: worklog + the owning docs (D-row where named).

- iter-29 · 2026-08-31 · pack-2 — the arson-on-ashes door check — detail: worklog + the owning docs (D-row where named).

- iter-28 · 2026-08-31 · tune-2 — the crime cascade renders on the — detail: worklog + the owning docs (D-row where named).

- iter-27 · 2026-08-31 · tune-1 — the rest action + the story-critical — detail: worklog + the owning docs (D-row where named).

- iter-25 · 2026-08-31 · validation beats — session 10, the — detail: worklog + the owning docs (D-row where named).

- iter-24 · 2026-08-31 · validation beats — session 9, the day-2 — detail: worklog + the owning docs (D-row where named).

- iter-23 · 2026-08-31 · validation beats — session 8, the — detail: worklog + the owning docs (D-row where named).

- iter-22 · 2026-08-31 · validation beats — session 7, the theft half — detail: worklog + the owning docs (D-row where named).

- iter-21 · 2026-08-31 · validation beats — session 6, the alarm — detail: worklog + the owning docs (D-row where named).

- iter-20 · 2026-08-30 · universality pass — the transition-layer and — detail: worklog + the owning docs (D-row where named).

- iter-19 · 2026-08-30 · owner-requested audit of two pasted spatial — detail: worklog + the owning docs (D-row where named).

- iter-18 · 2026-08-30 · validation beats — session 5, the arson half — detail: worklog + the owning docs (D-row where named).

- iter-17 · 2026-08-30 · validation beats — session 4, crime cascade — detail: worklog + the owning docs (D-row where named).

- iter-16 · 2026-08-30 · validation beats — session 3 — detail: worklog + the owning docs (D-row where named).

- iter-15 · 2026-08-30 · presence & entity cards — st-1 landed — detail: worklog + the owning docs (D-row where named).

- iter-14 · 2026-08-30 · validation beats — session 2 — detail: worklog + the owning docs (D-row where named).

- iter-13 · 2026-08-30 · validation beats — session 1 — detail: worklog + the owning docs (D-row where named).

- iter-12 · 2026-08-30 · the mediator session loop — detail: worklog + the owning docs (D-row where named).

- bg-5 · 2026-08-30 · owner-requested verdict on a pasted external integration spec — detail: worklog + the owning docs (D-row where named).

- iter-11c · 2026-08-30 · owner-requested re-check of iter-11b — detail: worklog + the owning docs (D-row where named).

- iter-11b · 2026-08-30 · roadmap stress-test re-verified + problems 4–6 — detail: worklog + the owning docs (D-row where named).

- iter-11a · 2026-08-29 · post-iter-11 audit — detail: worklog + the owning docs (D-row where named).

- iter-11 · 2026-08-29 · texture promotion door — detail: worklog + the owning docs (D-row where named).

- iter-10a · 2026-08-29 · post-iter-9/10 audit sync — detail: worklog + the owning docs (D-row where named).

- iter-10 · 2026-08-29 · scene-ledger LLM-free half — detail: worklog + the owning docs (D-row where named).

- bg-1 · 2026-08-29 · DF export pipeline CLOSED — detail: worklog + the owning docs (D-row where named).

- iter-8h · 2026-08-29 · owner-directed derived-index micro-pass — detail: worklog + the owning docs (D-row where named).

- iter-8g · 2026-08-29 · DF coverage audit — detail: worklog + the owning docs (D-row where named).

- iter-8f · 2026-08-29 · audit-fix after iter-8e — detail: worklog + the owning docs (D-row where named).

- iter-8e · 2026-08-28 · DF empirical F7/F8 survey on the owner's two world exports — detail: worklog + the owning docs (D-row where named).

- iter-8d · 2026-08-28 · DF designed-experience deep dive — detail: worklog + the owning docs (D-row where named).

- iter-8c · 2026-08-28 · owner-requested audit of iter-8a/8b: every claim reproduced; KI#30 — detail: worklog + the owning docs (D-row where named).

- iter-8a · 2026-08-28 · scene-ledger design pass — detail: worklog + the owning docs (D-row where named).

- iter-8 · 2026-08-28 · BRIEF_SPEC + brief assembler — detail: worklog + the owning docs (D-row where named).

- iter-7 · 2026-08-28 · phase-1 intake — detail: worklog + the owning docs (D-row where named).

- iter-6a · 2026-08-28 · owner-requested code audit of iter-5/6: every gate claim reproduced — detail: worklog + the owning docs (D-row where named).

- iter-6 · 2026-08-28 · phase-0 gate — detail: worklog + the owning docs (D-row where named).

- iter-5 · 2026-08-28 · chronicle & CLI — detail: worklog + the owning docs (D-row where named).

- iter-4a · 2026-08-28 · owner-requested code audit of iter-3/4 — detail: worklog + the owning docs (D-row where named).

- iter-4 · 2026-08-28 · director + goal ticker — detail: worklog + the owning docs (D-row where named).

- iter-3 · 2026-08-28 · knowledge, relations, expectations — detail: worklog + the owning docs (D-row where named).

- iter-2a · 2026-08-28 · owner-requested code audit of iter-1/2: KI#13–16 fixed — detail: worklog + the owning docs (D-row where named).

- iter-2 · 2026-08-28 · actions — detail: worklog + the owning docs (D-row where named).

- iter-1 · 2026-08-28 · core plumbing — detail: worklog + the owning docs (D-row where named).

- iter-0 · 2026-08-25 · docs & tooling bootstrap. — detail: worklog + the owning docs (D-row where named).

- iter-0b · 2026-08-25 · docs review + external source catalog — detail: worklog + the owning docs (D-row where named).

- iter-0c · 2026-08-25 · REFERENCES rev v2 merge — detail: worklog + the owning docs (D-row where named).

- iter-0d · 2026-08-25 · infra restore: `.gitignore`, package skeleton, smoke tests — detail: worklog + the owning docs (D-row where named).

- iter-0e · 2026-08-25 · `docs/CORE_DESIGN_RESEARCH.md` — detail: worklog + the owning docs (D-row where named).

- iter-0f · 2026-08-25 · manifesto absorption — detail: worklog + the owning docs (D-row where named).

- iter-0g · 2026-08-25 · research pass: Q1–Q3 absorbed — detail: worklog + the owning docs (D-row where named).

- iter-0h · 2026-08-26 · `docs/REFERENCES_DEEP.md` + D-024 anti-drift policy; ref batch 1 — detail: worklog + the owning docs (D-row where named).

- iter-0i · 2026-08-26 · ref-1 DF worldgen solo dive. — detail: worklog + the owning docs (D-row where named).

- iter-0j · 2026-08-26 · ref-2 C:DDA solo dive + cap policy rewrite — detail: worklog + the owning docs (D-row where named).

- iter-0k · 2026-08-26 · per-ref split into `docs/ref/` — detail: worklog + the owning docs (D-row where named).

- iter-0l · 2026-08-26 · ref-3 Paradox scripting solo dive. — detail: worklog + the owning docs (D-row where named).

- iter-0m · 2026-08-26 · ref-4 pacing trio dive — detail: worklog + the owning docs (D-row where named).

- iter-0n · 2026-08-26 · ref-5 event/narrative grammar family dive. — detail: worklog + the owning docs (D-row where named).

- iter-0o · 2026-08-26 · ref-6 roguelike emergence trio dive — detail: worklog + the owning docs (D-row where named).

- iter-0p · 2026-08-26 · ref-7 LLM-agent precedents dive — detail: worklog + the owning docs (D-row where named).

- iter-0q · 2026-08-26 · ref-8 + ref-9 six-file batch — detail: worklog + the owning docs (D-row where named).

- iter-0r · 2026-08-26 · ref-10 + ref-11 six-file batch — detail: worklog + the owning docs (D-row where named).

- iter-0s · 2026-08-27 · ref-12 UAP webapp dive — detail: worklog + the owning docs (D-row where named).

- iter-0t · 2026-08-27 · ref-13 live-char-guide dive — detail: worklog + the owning docs (D-row where named).

- iter-0u · 2026-08-27 · references distillation: `docs/BLUEPRINT.md` + `docs/blueprint/{phase0,phases}.md` — detail: worklog + the owning docs (D-row where named).

- iter-0v · 2026-08-27 · owner-requested audit patches: INV-2 rewritten per D-028 — detail: worklog + the owning docs (D-row where named).

- iter-0w · 2026-08-27 · owner-requested post-reference concept realignment: D-029 — digestion complete, skeleton — detail: worklog + the owning docs (D-row where named).

- iter-0x · 2026-08-27 · owner-requested reference-influence traceability audit: verdict "load-bearing" recorded in STATUS — detail: worklog + the owning docs (D-row where named).

- iter-0y · 2026-08-27 · owner-requested content-principles pass: D-030 — detail: worklog + the owning docs (D-row where named).

- iter-0z · 2026-08-27 · owner-requested quality round: D-031 — INVARIANT-CORE v3 + Elegant Solutions absorbed surgically — detail: worklog + the owning docs (D-row where named).
