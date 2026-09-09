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
iter-86 · 2026-09-10 · bridge1 — the scene-line projection pipe (W1's
head, D-116 (1) verbatim; 11 files — 2 code + 1 pack data + 2 test
files + 6 doc sync: the pipe + the pack migration + the lint pair +
the pins are one family, the iter-75/83 footprint; AGENTS §2.3: 11 >
5-6, the objective scope noted here)
- brief/assembler.py: the scene fields' VALUE SOURCE is the FOLDED
  PROJECTION — a prop the scene location's fold holds renders its
  canon value (the claims ride world_formed's state_changes), the pack
  record the fallback for unclaimed fields, a field neither holds
  renders nothing; the card law held (static first, event-born last —
  the claims ARE event-born; then promoted props in log order);
  `_token_value` renders booleans JSON-style (`near_river=false` — the
  values are JSON-born canon, never the host language's caps).
- content/tavern_pack/rules.json: scene_line_fields += terrain /
  world_region / near_river (the arming's visible half — an armed
  world invisible to the narrator is no longer half-armed) + the
  bridge-1 note in the block's notes.
- core/pack.py: `_brief`'s scene-line legal set = location record
  fields ∪ armed claim slots (`_armed_claim_slots`, the defensive walk
  — the worldgen shape lint runs last, the KI#77 order law);
  `_worldgen`'s REACHABILITY gains the scene-line consumer arm (the
  claims' first brief-side consumer, D-117's pinned future landed).
- +3 tests (the pipe pin: the tavern scene line carries
  terrain=coast + world_region=region_00 after the static layout; the
  street arm near_river=false over the genesis-only log; the
  determinism double-assembly; the lint negative — the unarmed twin's
  dead claim fields refuse at load; the reachability scene-line arm
  positive + the crafted_pack scene-line sync + the hook-consumer
  test's slot sync) — 1403→1406+1 green, ruff clean (3.12.14, the env
  pin; seeds 0/42/unset spot-checked). Corpus price ZERO by
  construction, measured both arms: no runtime byte reads
  scene_line_fields — the T1 + corpus fixtures byte-identical (zero
  re-pins, git-verified); the price paid is the visible claim tokens
  in genesis-bearing briefs (the pipe's purpose); the narrator
  corpus's 4 call pins unaffected (loc_backyard carries no claims).
- docs: BRIEF_SPEC §3.8/§6 + the example, DECISIONS D-120, TASKS
  bridge-1 done, STATUS re-pinned (the queue: chron-2 next, D-116's
  wave order), AGENT_NAVIGATION §1 the brief/core/content/tests rows.
  D-120. iter-77 evicted (verified against git in this edit); 10
  held. Caps: STATUS 678 / TASKS 1005 / DECISIONS 85 lines (56 rows)
  — over-cap on substance (§6.1, the D-095..D-119 precedent), trim at
  the phase-5→6 gate.
---
iter-85 · 2026-09-10 · intake6 — research intake 6, the
consolidated-analysis residue cataloged (doc-only, 5 files:
REFERENCES, DECISIONS, TASKS, this log, STATUS; the owner's
variant-A call, the D-096/D-116 intake family; every claim verified
against HEAD `cf8d06e` — ~80% of the text already landed/cataloged).
- D-119: REFERENCES §10 +3 rows (Dune → res-1's pack-declaration
  shape; Warhammer 40k → depth-6/PACK_SPEC prohibitions framing;
  Outer Wilds anti-reference, knowledge-as-progression refuted); the
  record-systems dictionary + ethos mutagenesis deferred to the
  phase-6 opening on the existing owner-gated W4 rows (just-in-time);
  Actor Model + CRDT refused — the pros already delivered by
  SCHED-1/STATE-1/D-114/single-writer log, the minuses fatal to
  INV-2/L4/T1. The queue untouched: bridge-1 stays pinned.
- KI#81 opened + closed this edit: iter-84's worklog entry landed
  without its closing separator AND without the owed eviction (11
  entries held vs the claimed "10 held (9 + this one, git-verified)"
  — the KI#80 family, second recurrence). Fixed here: separator
  restored, iter-76 (the eviction iter-84 owed) + bg-8 (this
  entry's own) evicted — 10 held, verified against git in this
  edit. 1403+1 green, ruff clean (3.12.14; seeds 0/42/unset).
  Caps: STATUS 668 / TASKS 1002 / REFERENCES 305 / DECISIONS 84
  (55 rows) — over-cap held on substance (§6.1), trim at the
  phase-5→6 gate.
---
iter-84 · 2026-09-10 · mech-1 — the mechanics introspection CLI (the
owner's session call: an infra slot ahead of the queue's bridge-1, the
ORDER owner's prerogative; 8 files — 1 tool + 1 suite + 6 doc sync
(git-verified: 2 new + 6 modified), AGENTS §2.3 scope noted here).
`scripts/mechanics.py` (D-046
CLI-class, stdlib + core imports only, stdout-only): `matrix` (static
wiring queries --event/--hook/--token/--prop + the unindexed-blocks
fallback — a future layer is listed, never guessed), `trace` (the
shadow replay: per-tick events + beat panels with entropy/pacing),
`why --hook TAG` (the postmortem: seeded/armed/option-gate values),
`blast` (the two-arm same-seed A/B — the corpus-price pattern, no
resume door). D-118: the shadow-replay law — the tool replays the log
through the public pipeline (fold/Director/predicates/entropy), INV-2
makes it equal the runtime; the runtime is never instrumented.
- tests/test_mechanics.py: 11 pins — the exactness pin (the shadow's
  release ids == the log's director events on day1_full) + the STATUS
  pins (the relief's check at t=734, the sweep last at t=1456) + the
  future-layer law (an unknown rules block loads and lists). 1392→
  1403+1, ruff clean (3.12.14, the env pin; seeds 0/42/unset all
  green, verified in this iteration).
- docs: TASKS the mech-1 row, AGENT_NAVIGATION §1 scripts row + §2
  Normal + §5, DECISIONS D-118, README the scripts-map line, STATUS
  header. The queue is untouched:
  bridge-1 stays the pinned Next step. 10 entries held (9 + this one,
  git-verified per the KI#80 law). Caps: STATUS 654 / TASKS 985 /
  README 627 / DECISIONS 83 lines (54 rows) — over-cap on substance
  (§6.1, the D-095..D-116 precedent), trim at the phase-5→6 gate.
---
iter-83a · 2026-09-09 · audit-fix — the owner's re-check of iter-83
(the iter-11c precedent): substance VERDICT SOUND — 1392+1 green
re-verified under seeds 0/42/unset, ruff clean, the D-116 W0
checklist fully landed, the T1 genesis diff (5 events + the id
shift) + the murmur-timing pins reproduced; the defects were the
LANDING COUNTS (KI#80, opened + closed in this edit; 2 files: this
log + STATUS). Doc-only, no code/fixtures/pins touched.
- worklog: iter-83's counts corrected vs git — "17 files" → 33
  (3 code + 2 pack data + 5 fixtures + 18 test files: 1 landing +
  17 re-pins + 5 doc sync), "14 suites" → the 17 re-pinned files,
  "10 entries held" → 11 (the missed eviction); iter-82's "9
  after" → 10; iter-73 (the eviction iter-83 owed) + iter-75 (this
  entry's own) evicted — 10 held, verified against git in this
  edit (the KI#68 law).
- STATUS: the Scope re-counted (`docs/AGENT_NAVIGATION.md` named,
  17 re-pin suites, 33 files); KI#80 recorded; the audit note in
  the header; one clause in the FAQ doc-drift entry — the durable
  law: landing counts are git-verified, never asserted. D-117's
  own "17 files" left per the append-only law; git owns the count.
- The suite re-run green AFTER these edits (1392+1, ruff clean);
  archive: STATUS.md + worklog.md + BASE_COMMIT 21ea6a7.
---
iter-83 · 2026-09-09 · worldgen-arm — depth-5b, the worldgen ARMING,
EXTENDED per D-116 (33 files — 3 code + 2 pack data + 5 fixture
regen/re-pin + 18 test files: 1 landing + 17 re-pins + 5 doc sync;
re-counted vs git at iter-83a, KI#80: the arming + its lint laws +
its pins + its paid price are one mechanism family, the iter-76/81
footprint; AGENTS §2.3: 33 > 5-6, the objective scope noted here)
- core/worldgen.py: the flat claim keys — each committed claim's slot
  rides the world_formed outcome as a render-surface key (D-116 (4):
  the template binds them through `_event_context`; the `claims` list
  stays the structured record) + RESERVED_CLAIM_SLOTS (the collision
  law: outcome keys are clobbered, derived slots shadowed);
  core/pack.py::_worldgen: CONDUCTANCE (the genesis importances
  computed through `pack_importance` against the tale gate — the
  dead-arming refusal; tune-1's law enforced by computation, never a
  second scoring path) + REACHABILITY (L1: `_bound_template_slots`
  scans the template braces, `_director_prop_reads` the hook prop
  leaves — every armed claim names a live consumer) + the
  reserved-slot refusal; core/metrics.py: the M5 run-start note
  re-pinned (the genesis prefix counts as non-PC, actor world).
- content/tavern_pack ARMED: rules.json the worldgen block (48/8 map,
  jitter 3, relax 1, octaves 3/2, bands [4000,5000,7000]/
  [2500,5000,7500], watershed 4/6, 3 capitals, chronicle 150y / 5
  events / world_history / hooks [the sweep + the murmur], 3 claims:
  terrain + world_region @ loc_tavern, near_river @ loc_street) +
  world_history in importance.story_critical_events; templates.json
  the world_history line (the {year?…} shape branch + the claim
  clauses — the binding surface).
- The price, measured BOTH arms first (the D-108 law, a Rule-9 probe
  over the smoke + day1 ten + arson): the genesis events alone + the
  mechanical id shift — fingerprint equal on every probe, the
  post-genesis stream identical modulo id references. Paid: the T1
  fixture regenerated (12 lines, the iter-15 precedent), the corpus
  fixtures re-pinned (+5 ev ids / event_seqs / causes; the murmur's
  release moved to the FIRST quiet beat — the pre-seed's designed
  price, D-005: the genesis seeds the director's buffer), ~70 test
  pins updated across the 17 re-pinned files (the day1 scan ids,
  the golden-log slices, the reflection/retrieval pins, the pacing
  A/B record).
- +14 tests (tests/test_worldgen.py 26→40: conductance both arms,
  reachability both consumer arms + the reserved law, the flat keys,
  the live template render, the both-arms price law (smoke + day1
  seed 125, ids remapped), the M5 note, double-open loud, the genesis
  checkpoint/restore, the two drift guards) — 1378→1392+1 green, ruff
  clean. D-117; TASKS depth-5b done; STATUS re-pinned (the queue:
  bridge-1 next — inseparable, D-116); AGENT_NAVIGATION §1 the armed
  rows. 11 entries held after this edit (10 + this, the eviction
  missed — restored to 10 at iter-83a, KI#80).
---
iter-82 · 2026-09-09 · concept-land — doc-only, the generator-concept
verdict set (D-116; 8 files — the verdict row + the routed plan are
one family, the iter-77/78 footprint; AGENTS §2.3: 8 > 5-6, the
objective scope noted here). The suite re-verified green at HEAD
`0d6a3bf` BEFORE the edits (1378+1, ruff clean, 3.12.14 — the env
pin); no code touched.
- docs/DECISIONS.md: D-116 — the 13 owner-questions resolved as
  best-of-variants syntheses (the scene-line reads the folded
  projection; conductance through the importance rule + the
  dead-arming lint; ceilings REFUSED in favor of the geo-1 rework —
  policy ≠ correctness; the calendar deferred to maclock-1 as the
  macro-clock's counter; travel prices derived from the WorldModel
  with pack-override; maclock-1 the dedicated primitive row; bounded
  plane the topology of record; the LOD ladder as mode G's boundary;
  renotation through the render layer; world-2 the phase-6 gate
  instrument; the Azgaar donor split; res-1 the owner-gated resource
  layer) + the 13 contradictions dissolved (native 3D = final
  refusal, the spatial model pinned as phase law).
- docs/TASKS.md: intake-5 the wave plan routed (bridge-1 / chron-2 /
  place-1 / geo-1 / maclock-1 / name-1 + world-2 / res-1 / roads-1
  owner-gated at phase 6); depth-5b EXTENDED (conductance +
  reachability + genesis×resume + the T1 regen, NO ceilings); st-6a's
  price law amended (derived + pack-override, the gate satisfied).
  TASKS 971 — rides above 600 (substance rows: the plan; the pattern
  documented here per §6.1).
- docs/blueprint/phases.md §5: the spatial model pinned as phase law
  (the graph of scales, attributive Z, vertical edges, bounded plane
  of record, void filtering = pack-CI); docs/ROADMAP.md §4: the
  Azgaar donor split; docs/REFERENCES.md §10: eight catalog rows (the
  economics/culture donors) + Kenshi amended; docs/REFERENCES_DEEP.md
  §1: ref-18/19/20 planned just-in-time at their consumers.
- STATUS.md re-pinned (iter-82 header + the wave queue); worklog
  iter-82 in / iter-72 out (verified in this edit); 10 after (the
  log held 10 at HEAD — the cap law held, the count did not grow;
  the 9s corrected iter-83a, KI#80).
---
iter-81 · 2026-09-09 · worldgen — depth-5, the ordered worldgen
passes, mechanics only (13 files — 3 code edit + 1 new code + 1 new
suite + 8 doc sync: the pass family + its lint + its genesis wiring +
its pins are one mechanism family, the iter-75 footprint; AGENTS §2.3:
13 > 5-6, the objective scope noted here)
- core/rng.py: `worldgen:<pass>` — the D-079 family law's fourth
  member (`WORLDGEN_PREFIX` + `worldgen_stream_name` + the assure
  nesting law); per-pass isolation pinned (the armed arm's
  substantive fingerprint EQUALS the unarmed arm's — the corpus price
  of worldgen is the genesis events alone).
- core/worldgen.py (new): `PASS_ORDER` the ordered passes — sites
  (jittered integer lattice) → relax (integer-centroid Lloyd) →
  height/moisture (integer-octave value noise, fixed-point weights
  that divide out, normalized 0..9999) → watershed (downhill flow +
  rivers) → biomes (band table + coastal refinement) → states
  (capitals + growth) → chronicle (pre-PC history); WorldModel
  INTEGER-ONLY (the Azgaar float-drift refusal, test-walked);
  `resolve_claims` = `detail_claim`'s FIRST LEGAL CALLER (commit
  rides world_formed, no_op skipped, slot_conflict refused with the
  cause chain); genesis drafts (world_formed cause-null + history
  events ascending year, hooks, NO knowledge — the DF
  epistemology-empty law); core/loop.py::open the armed-only genesis
  (the director's buffer pre-seeded, the PC chains to the last
  genesis event); core/pack.py::_worldgen the shape lint (closed
  vocabularies, template closure, declared-hook law, the claim
  double-claim family). Committed pack UNARMED — v0.1 bytes (the 68a
  pattern; depth-5b the arming row laid).
- +26 tests (tests/test_worldgen.py, 1352→1378+1 green, ruff clean;
  corpus price ZERO by construction — no committed-pack byte moved,
  T1 + every corpus pin green). D-115; TASKS depth-5 done + depth-5b
  laid. iter-71 evicted (verified in this edit); 10 after. Caps:
  STATUS 643 / TASKS 849 / DECISIONS 80 lines (51 rows) / TECH_NOTES
  695 / TEST_PLAN 722 / phases 719 — over-cap on substance (§6.1, the
  D-095..D-114 precedent), trim at the phase-5→6 gate.
---
iter-80 · 2026-09-09 · foldcheck — depth-4, the fold-checkpoint
mechanism family (11 files — 1 new code + 1 new operator tool + 1
new suite + 7 doc sync: the mechanism + its builder + its pins are
one family, the iter-75 footprint pattern; AGENTS §2.3: 11 > 5-6,
the objective scope noted here)
- core/checkpoint.py (new): FoldCheckpoint = deep-copied projection
snapshot + event-index offset; ONE canonical serialization (compact
JSON, sorted keys); restore = snapshot + tail replay (rollback, the
from_-net loud); verify/verify_all the re-fold law (batch folds
once, O(N + states)); the sha256 anchor in the derived index
index.json (offset + snapshot sha256 + prefix sha256 — never an
event in the truth, intake-4's refusal held); prefix_digest =
sha256 over the first 1+offset log lines, append-stable (INV-5);
load/read anchor teeth (edited artifact, re-filed offset, hand-ed
index — loud).
- scripts/checkpoint.py (new): the chronicler-family builder —
read_log validation + the pack↔header name_version gate + one
incremental fold, snapshots at every requested offset, born-verified
BEFORE any write (the count-gate spirit); default the END
checkpoint, --every N the cadence ∪ the end; output/checkpoints/
(gitignored). The KnowledgeView half deliberately OUT (shape is
knowledge-internal — the read-side-indexes row owns it at the
mediator iteration; the resume door owner-gated, phases.md §7).
- +25 tests (tests/test_checkpoint.py, 1327→1352+1 green, ruff
clean; the rollback law cross-checked against the LIVE runtime
projection — the blind-1 instrument; corpus price ZERO by
construction, no runtime pipeline byte moved). D-114; TASKS depth-4
done. iter-70 evicted (verified in this edit); 10 after. Caps:
STATUS 633 / TASKS 837 / DECISIONS 79 lines (50 rows) / TECH_NOTES
695 / TEST_PLAN 666 / phases 700 — over-cap on substance (§6.1, the
D-095..D-113 precedent), trim at the phase-5→6 gate.
---
(end of log — cap 10; pre-trim history lives in git)
