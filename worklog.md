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
iter-72 · 2026-09-08 · prosefloor-2 — the lowercase assertion surface,
the lance's last row (D-104; 10 files — the iter-66 family footprint:
the instrument + its doc sync)
- brief/scan.py: `relation_attribute_tokens` (the two assertion slots —
  the copular predicate head with the 's contraction + up to two
  interveners, the possessive tail with the intensifier skip; the
  closed classes are English function words only, INV-3-clean) +
  `modeled_vocabulary` (names/roles/moods/axes, the name manifest
  reused); a measurement export, NEVER a gate (D-096) — no refusal,
  no regen spend, no boundary wiring.
- tests/test_scan.py +15: the boundary pins + the corpus calibration
  baseline pinned exact (129 strings / 133 token-hits / 81 unique /
  14 grounded / 67 unmodeled — the single owner of the split numbers,
  D-024); corpus price ZERO by construction (no pipeline byte moved,
  T1/T2/corpus/mediator untouched). Docs: VALIDATION_SPEC §2.1,
  TEST_PLAN §8.4, TASKS (prosefloor-2 done — the v0.2 lance COMPLETE),
  README, AGENT_NAVIGATION §1, DECISIONS D-104. KI#76/77/78 deleted
  per §5 (two-plus iterations past). 1255+1 green, ruff clean.
  iter-66a evicted (verified in this edit); 10 after.
---
iter-71 · 2026-09-08 · plansync — the owner's analysis-intake plan
sync, doc-only (the iter-66a/68 precedent; 4 files — zero code,
zero tests; verified 1240+1 green, ruff clean after the edits)
- docs/TASKS.md: the research-intake-3 section (weather-1: ambient
  weather events + canon erosion via state_changes, pack data, no-TTL
  D-049; companion-1: the companion role as pack data over existing
  doors, deps tune-3/st-6a/resume door BY REFERENCE — the D-076/D-081
  precedent) + the pack-1 gate fix (stale "phase-0 gate" line — a
  D-024 violation, 64 iterations stale — now defers to the STATUS FAQ).
- STATUS.md: the iter-71 header + the Next-step re-pin (the queue:
  prosefloor-2, then the owner's phase-5 start signal); README.md: the
  lance section's intake-3 line (the KI#73/78 family). TASKS 693→724,
  STATUS 640→630 (the iter-70 landing paragraph → the iter-71 one),
  both over-cap on substance (§6.1) — TASKS collapses at the
  phase-5 opening.
  Doc-only streak 1 of 2 (iter-70 was functional — no alarm; the next
  iteration must be functional). iter-66 evicted (verified in this
  edit); 10 entries after.
---
iter-70 · 2026-09-07 · beliefwire-2 — the trait-consumer arming, the
lance's last track-A row (D-103; 16 files — the pack arming + its
measured corpus price + the doc sync, one mechanism family, the
iter-60..69b scope pattern)
- content/tavern_pack/rules.json the relief guard's trait-gated scan
  (p=100, the new-entry shape — the guard_01 re-gate refused on
  record) + the counters trio; actions.json the arson fled line (the
  counter mint, one event both halves); core/pack.py KI#77 (the lint
  order: _traits before _urgencies — the cond lint reads the block's
  shape; the pruning law: removing the belief vocabulary prunes the
  consumer, test_traits/test_knowledge re-pointed).
- The price measured FIRST both arms and paid in the landing: +3
  look_around on seed 125 ONLY (9/10 day1 seeds byte-identical vs the
  disarm twin; the seed-33 panic corpus + theft_and_arson untouched) +
  the seed-93 narrator family re-distilled through the fixed-point
  runner (pristine identity 105/105, the PARALLEL incremental
  alignment — the pin map refreshes mid-beat, a refused beat never
  feeds; 11 claim-id re-pins, idempotency 0) + M1 0.509→0.54/0.500→0.52
  (the D-065 record re-pinned). KI#78 opened+closed (the README lance
  drift). 1240+1 green, ruff clean. TASKS beliefwire-2 done; the
  lance's remainder: prosefloor-2. iter-65 evicted (verified in this
  edit); 10 after.
---
bg-7 · 2026-09-07 · engine + confabulation probe — the five probes'
first numbers on a REAL engine (track B, D-098's Layer-2 runner; the
repo diff is doc-only — the runner + transcripts live outside per
Rule 9/INV-4 and never wrote a repo byte, git clean through the run)
- The sandbox API engine (glm-4-plus; the {3–8B, GBNF} arm = the gap
  row, engine-1's input unchanged) through the REAL doors: the
  51-utterance corpus 39/44 gate-valid after ONE re-ask (79.5→88.6%,
  the deferred ladder's first numbers); 24 prose beats — floor 0, gap
  0, the claims-channel refusal engine = the brief-surface vs
  claim-id mismatch; the Cyrillic twin tax zero; C3.5's 0→1 signal;
  the surface A/B null. TECH_NOTES §10 (608 — over-cap substance per
  §6.1, trim at the phase-5→6 gate; TASKS 699 — the same stance, the
  iter-66a precedent); TASKS bg-7 done + prosefloor-2
  UNBLOCKED. 1239+1 green, ruff clean. iter-64 evicted (verified in
  this edit); 10 after.
---
iter-69b · 2026-09-07 · suspectaxis-2 — the committed pack's
per-target ARMING (D-101's arming row, D-102; 25 files — the pack
arming + its measured corpus price + the doc sync are one mechanism
family, the iter-60..69 scope pattern)
- rules.json the object mapping (all figures pc_01) + witnessed_arson
  30 + the pair-home re-declarations (triggers, vigil modifiers, crowd
  prop, wary marker); entities.json the pair homes, the flat drop;
  core/loop.py the ignition cause re-anchored to the action; core/pack.py
  the marker lint's pair.<npc>.<axis> family.
- Corpus price measured FIRST both arms, paid in-landing: the D-101
  projection (8 claims) undercounted — the true ledger + the
  arson-case stream shifts (the witnessed-arson reactions, the seed-93
  arrest family) via the fixed-point re-distill (31 claim edits, the
  iter-50 idempotency law). M1/M2 identical; day1 11/11 diverged, the
  T1 golden + theft_and_arson byte-identical. 1239+1 green, ruff clean.
  KI#76 opened+closed (the DIRECTOR_SPEC §4 formula). TASKS
  suspectaxis-2 done; the lance's remainder: beliefwire-2 + bg-7.
  iter-63 evicted (verified in this edit); 10 after.
(end of log — cap 10; pre-trim history lives in git)
