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
iter-79 · 2026-09-09 · verdict-land — the owner's call on the
iter-77/78 routed candidates executed (14 files — 3 code + 3 suites
+ 8 doc sync: the verdict-set as one mechanism family, the
iter-70/73 scope pattern, AGENTS §2.3 noted here)
- pred-failclosed + pred-contract (D-110/D-111): DIRECTOR_SPEC §3's
  blanket fail-closed restored in BOTH comparison twins
  (predicates._prop + onaction._gate_passes — missing → False under
  every comparator, `not_equals` = present AND ≠ X, `{"not": …}`
  the escape); the equals-null hole closed by the pack-lint null ban
  (prop leaf + gate condition); the `_require` family — 6 raw-read
  surfaces → ValueError naming the field (census corrected 5 → 6:
  the gate's comparator guard covered wrong values, not missing
  keys), shape errors before the world answer. Zero pack migration
  (zero not_equals + zero nulls, verified; T1 + corpus pins green
  byte-identical). DIRECTOR_SPEC §3/§3c + two docstrings + two pins
  flipped ("answers honestly" → fails closed).
- D-112: iter-11b resolutions RATIFIED — phases.md §5 in the
  D-056-amended edition (the arrival snapshot folded to one answer)
  + §7 Containers covered; both pending tags cleared; TASKS depth-7
  stays a todo BUILD row with the design pinned.
- D-113: Rule 9 defined in AGENTS §7 (verified census 25 hits / 8
  files — both earlier counts under); NAVIGATION §3 the sequencing
  split (ORDER = STATUS Next step, composition = TASKS); tn12-claim
  dropped (zero diff — every proposal had a named owner);
  verify-seed + archive-protocol = the owner's bootstrap text
  (chat-side). 1323 → 1327 passed +1 skipped, ruff clean. bg-7
  evicted (verified in this edit); 10 after. Caps: STATUS 647 /
  TASKS 835 / DECISIONS 78 lines (49 rows) / TECH_NOTES 695 / phases
  693 — over-cap on substance (§6.1, the D-095..D-109 precedent),
  trim at the phase-5→6 gate.
---
iter-78 · 2026-09-09 · meta-land — the owner's ultimate-variant text
re-verified claim-by-claim against HEAD `cb91cbe` and landed (3
files: STATUS header + Next-step line, this log, the TASKS iter-77
routed section strengthened; the iter-19/34/71/77 owner-requested
precedent; doc-only streak 2 of 2, both owner-requested — iter-79
must be functional)
- Verified TRUE (every claim of the text): the fail-open
  `not_equals` (`predicates._prop` + `onaction._gate_passes`); lint
  covers 'of', `path` is string-only; content/ carries zero
  `not_equals`; the audit except-branch is deliberate design
  (try/else REQUIRES except, the re-raise never masks); TECH_NOTES
  has no §12; the five sandbox adaptations un-routed; the
  session-prefix law already AGENTS §2.2 (iter-19/34/71/77).
- Three findings landed into the TASKS rows: (1) DIRECTOR_SPEC §3's
  "missing prop answers False" was born iter-40 WITH the prop leaf
  — the spec pins fail-closed; the `not_equals` exception is a
  37-iteration code-vs-spec drift → the candidate is spec
  RESTORATION (ACCEPT: §3 unchanged, §3c wording + 2 docstrings +
  2 existing pins flip; REJECT: §3 documents the exception); (2)
  the Rule-9 census is ~19 citations (STATUS x3, TASKS x1,
  TEST_PLAN x8, TECH_NOTES x2, DECISIONS x5), not iter-77's 4x —
  the AGENTS §7 one-liner resolves all; (3) the owner's ignore-list
  landed as the routed section's re-raise guard. pred-contract was
  already routed — the text missed it; the TASKS collapse + the
  rng.py/of corrections were already iter-77's. 1323+1 green under
  seeds 0/42/unset, ruff clean. iter-69b evicted (verified in this
  edit); 10 after.
---
(end of log — cap 10; pre-trim history lives in git)
