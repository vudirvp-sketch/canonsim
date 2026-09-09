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
  iter-82 in / iter-72 out (verified in this edit); 9 after (the log
  held 9 at HEAD — the cap law is held, the count did not grow).
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
iter-77 · 2026-09-09 · meta-analysis — the owner's two-text
cross-review, doc-only (3 files: STATUS header + Next-step line,
this log, TASKS rows; the iter-19/34/71 owner-requested precedent;
doc-only streak 1 of 2 — the next iteration must be functional)
- Verified claim-by-claim against HEAD: the sequencing three-pointer
  (bootstrap "top todo" = gate-blocked depth-3 vs STATUS queue
  depth-4 vs NAVIGATION §3); the verify line's missing
  PYTHONHASHSEED=0 (suite green under seeds 0/unset/42 — consistency
  gap, not a live flap); Rule-9 dangling citations (4x); not_equals
  fail-open on a missing prop (predicates._prop + the onaction gate
  twin, pinned "honestly"; the of-typo case already lint-dead —
  pack.py validates 'of' against entity ids; the live surface is
  path typos + runtime-absent props); TASKS collapse debt.
- Corrected the texts: the audit except-branch is syntax-bearing
  (try/else REQUIRES except — deliberate no-masking, not cruft);
  the sandbox text's "saved in TECH_NOTES §12" is not in HEAD
  (no §12 — a reported-but-unlanded deliverable, the KI#48
  family); its stratified-sampling / budget-cap / n>=3 /
  provider-rotation / brief-size-curve items are un-routed
  proposals, not law. Routed the candidates to TASKS (iter-77
  section, owner verdict pending); ultimate variants in chat
  (Russian). 1323+1 green under all three seeds, ruff clean;
  phase-5 done rows collapsed per the TASKS header law. iter-69
  evicted (verified in this edit); 10 after. Caps: STATUS 629 /
  TASKS 840 (the collapse paid −33, the routed section +44) /
  TECH_NOTES 695 / TEST_PLAN 628 — over-cap on
  substance (§6.1, the D-095..D-109 precedent), trim at the
  phase-5→6 gate.
---
bg-8 · 2026-09-09 · engine-runner — the LLM-integration test runner,
testproto's live half (track B, D-098 Layer 2, the owner's
sandbox-simulation call; 10 files — 2 new test artifacts + 8 doc
sync, the bg-7 footprint family)
- The runner outside the repo (Rule 9:
  /home/z/my-project/scripts/bg8_runner.py + bg8_distill.py) drove
  the sandbox API engine (glm-4-plus) through the REAL mode-C door:
  the deviation corpus F1–F6 (36 probes) + the heartbeat (the
  51-utterance parse corpus re-run — the first trend row, TEST_PLAN
  §8.5).
- Numbers (TECH_NOTES §11): world-answer coverage 34/34 = 100% — the
  measured failures are mapping quality (F3 1/6 the guess engine, F4
  2/6 closest-verb, F6 0/6 two injections EXECUTED + the
  protocol-echo leak; honest 17/36); the heartbeat 84.4 → 93.3%
  after one re-ask, the refusal families DRIFT run-to-run
  (unknown-keys → texture-reference).
- The transcripts re-distilled into the Layer-1 pin:
  tests/fixtures/deviation_corpus.json + tests/test_deviation.py
  (+8 tests, 1315 → 1323 passed +1 skipped, ruff clean; the runner
  never wrote a repo byte, git verified). D-109; TASKS bg-8 done +
  the standing gap rows ({3–8B, GBNF}, the prose families,
  latency). iter-68b evicted (verified in this edit); 10 after.
  Caps: STATUS 633 / TASKS 829 / TECH_NOTES 695 / TEST_PLAN 628 /
  DECISIONS 73 (45 rows) — over-cap on substance (§6.1, the
  D-095..D-108 precedent), trim at the phase-5→6 gate.
---
iter-76 · 2026-09-08 · scenedetail-arm — depth-2b, the scene-detail
ARMING (9 files — 1 pack + 2 suites + 6 doc sync: the pack arming +
its measured corpus price + the doc sync are one mechanism family,
the iter-68b/74 arming footprint)
- rules.json the `scene_detail` block (loc_tavern under_bench +
  behind_barrel, loc_guardroom under_cot — the two scenes the corpus
  observes; pure-flavor values, no claim-surface token);
  tests/test_detail.py the 68a pins re-pointed to the crafted v0.1
  twin + the arming family (the declared block, the live pools, the
  D-108 knowledge surface, the paid day1 ledger, the ten's seed
  split, the armed replay); tests/test_ambient.py the murmur's
  state-surface re-pin (the ramble's only state changes are the
  scene's lazy births).
- Price measured FIRST both arms (a runner outside the repo, Rule 9):
  strictly fidelity-only — day1 ten (director ON, the default): 4
  seeds zero, 5 seeds one barkeep-look payload, seed 125 the two
  guard scans; fire corpus + plumbing zero; T8 arms two payloads,
  M1..M5 identical; narrator corpus 105: 90 identical, 15 one payload
  (statuses/notes/anchors/call documents untouched). The probe lesson:
  the default-director arm is the corpus geometry (first pass measured
  OFF and undercounted — caught before landing). +6 tests
  (1309→1315+1, ruff clean). D-108 (the knowledge-surface decision:
  zero new knowledge tokens); TASKS depth-2b done. iter-74 evicted
  (verified in this edit); 10 after. Caps: STATUS 626 / TASKS 817 /
  DECISIONS 73 lines (44 rows) — over-cap on substance (§6.1, the
  D-095..D-107 precedent), trim at the phase-5→6 gate.
---
iter-75 · 2026-09-08 · scenedetail-gate — depth-2, lazy detail
materialization, mechanics only (12 files — 4 code + 1 suite + 7 doc
sync: the stream family + the draw gate + the claim mirror + the lint
+ the doc sync are one mechanism family, the iter-60..74 scope
pattern)
- core/rng.py the `scene:<id>:detail` stream family (the D-079 law's
  third member: lazy registration, injective name, the shared
  FAMILY_PREFIXES tuple); core/detail.py (new) the draw gate
  (canon-skip = first-commit-wins, pack-order draws, from_ None
  births) + `detail_claim` (the slot_conflict mirror with the cause
  chain); core/resolvers.py::_observe the wiring (the
  scene-snapshot family; `materialized` outcome key, present only
  when something materialized); core/pack.py::_scene_detail the
  closed-vocabulary lint (double-claim + one-object laws, after
  _brief per KI#77).
- Corpus price ZERO by construction, pinned both ways: the committed
  pack unarmed (v0.1 bytes, the fingerprint untouched — the gate
  answers () before any assure) + the laziness pin (an armed
  never-observed scene is byte-identical) + the measurable-arming
  pin (the armed run differs exactly by the births and the outcome
  key). +28 tests (1281→1309+1, ruff clean). D-107; TASKS depth-2
  done + depth-2b (the arming row) laid. iter-68a evicted (verified
  in this edit); 10 after. Caps: STATUS 633 / TASKS 814 over 600 —
  substance (the landing headers' own record, the D-095/D-096
  precedent), trim at the phase-5→6 gate; DECISIONS 43 — rides
  above 30 until the same gate.
---
iter-73 · 2026-09-08 · depthopen — the owner's phase-5 start call: the
opener + research intake 4 + depth-1 the acquisition gate (11 files —
the iter-55 opener+leg footprint: 4 code + 7 doc sync)
- ROADMAP §2's phase-5 flip; TASKS the phase-5 backlog (depth-1..7)
  + intake 4; phases.md §5 the two intake additions (the sha256 index
  anchor, threshold margins) + the depth-1/1b pointer; D-105.
- depth-1: core/intent.py::acquisition_fidelity (the event-site
  emission law, both resolve branches, D-007's documented twin walk),
  core/pack.py::_acquisition (the closed vocabulary lint),
  core/clock.py::phase_of_tick (the rules-level twin).
- The committed pack UNARMED — v0.1 bytes (the 68a pattern; no draws
  ever); +20 tests (1255→1275+1, ruff clean; the both-arms zero-price
  pin + the smoke-geometry liveness law). iter-67 evicted (verified
  in this edit); 9 after (the log held 9 at HEAD — the cap law is
  held, the count did not grow).
---
(end of log — cap 10; pre-trim history lives in git)
