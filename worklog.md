# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.
> Order: newest first (normalized at iter-8c — the order had drifted
> since iter-5).

---
iter-10 · 2026-08-29 · scene-ledger LLM-free half (iter-10-scene-ledger)
- `brief/ledger.py` (D-053): the entry shape + discrete one-way
  lifecycle, scenes as PC-location intervals (a pure log fold — zero
  new event types), the ONE validation gateway (scope/canon-slot/
  laundering/unique-slot/duplicate/slot-conflict + presence incl. the
  carrier closure; 8-reason closed refusal vocabulary in the §7 shape,
  loud DeltaError on document drift), beat-pass contradiction
  retirement, scene-close bulk retirement, auto-sync inside apply_delta
  (D-037), texture-OCC withdrawals + the promotion marker. Plus the
  `scene_texture` 7th brief block (position 3; window law, pinned-first,
  tombstones, ranking caps) and the BRIEF_SPEC §9 ATOMIC flip (purity
  pair → (log, ledger); §3 renumbered — scene_texture is §3.3).
- 15 files (above the 3–5 soft cap; the code+spec+suite+golden set plus
  the AGENTS §6 sync set — iter-9 precedent): ledger.py (new),
  assembler.py, brief/__init__.py, core/pack.py (BRIEF_BLOCK_IDS + lint),
  rules.json (block budget + scene_texture config), test_ledger.py (new,
  32), test_brief.py (+13), texture_deltas.json (new golden fixture,
  13 cases), BRIEF_SPEC (flip, held at 300 via a §6.1 cruft pass),
  VALIDATION_SPEC §8/§10, TASKS, AGENT_NAVIGATION, DECISIONS D-053,
  STATUS (KI#36 deleted per §5), README, this worklog.
  390→435 green, ruff clean, golden fixtures byte-identical. No new KIs.
- iter-8a evicted per the one-in/one-out cap (history in git).
---
iter-9 · 2026-08-29 · VALIDATION_SPEC + validator LLM-free half (iter-9-validation-spec)
- The phase-1 spec trigger fired: `docs/VALIDATION_SPEC.md` (closed
  proposal document — no prose field exists, injection neutralized
  structurally; honest verdicts under closed-world semantics;
  ExpectedVersion OCC = the intent-door semantics reused; the fact
  transaction; ≤2-regens protocol + the call-budget reconciliation;
  scene-ledger protocol clauses for iter-10; golden-set plumbing) +
  `brief/validator.py` (pure functions of (proposal, log, pack):
  loud shape gate, per-claim verdicts with first-break attribution,
  rebase-or-refuse, intent grammar pass-through, RegenBudget,
  refusal notes, golden-set runner) + the committed golden set
  `tests/fixtures/validation_golden.json` (18 pinned verdict cases
  over the smoke fixture log, all three verdicts).
- 11 files (above the 3–5 soft cap; the spec+code+suite set plus the
  AGENTS §6 sync set — iter-8 precedent): VALIDATION_SPEC (new),
  brief/validator.py (new), tests/test_validator.py (new, 38 tests),
  tests/fixtures/validation_golden.json (new), SPECS_BACKLOG (row →
  written), TASKS (iter-9 done + iter-10 re-sequenced),
  AGENT_NAVIGATION §1, DECISIONS D-052, STATUS, README, this worklog.
  352→390 green, ruff clean, golden fixtures byte-identical. No new KIs.
- iter-8 evicted per the one-in/one-out cap (history in git).
---
bg-1-sqlite-sink · 2026-08-29 · DF SQLite sink — bg-1 closed (D-051)
- Owner-directed (the new "large" world export supplied as input): the
  bg-1 remainder landed — `scripts/df_import.py` over the unchanged
  survey core: typed cores + EAV fields + `event_participant` +
  membership/parent links + one generic JSON `records` table;
  truncation policy owned (flagged partial default, `--strict` abort).
  Cross-validated on the large world (2.38 GB → 898 MB, 174 s): every
  table count reproduces the survey exactly. 352 green (was 340;
  +11 sink tests, +1 audit test). KI#36 opened+closed: UNDOCUMENTED
  marker implemented (first catches: `artifact`, `historical_era` —
  both matrix gaps fixed); the 8g truncation-test comment corrected
  (the in-flight record IS counted — measured, now pinned).
- 10 files (above the 3–5 soft cap; the tool + tests + the AGENTS §6
  sync set, iter-8e precedent): scripts/{df_survey,df_import}.py,
  tests/{test_df_survey,test_df_import}.py, TECH_NOTES §3.1+§3.2
  (fourth world + the owner's size answer: world size scales geography
  and occasions, not history volume), df_legends_xml.md matrix,
  TASKS (bg-1 done + bg-2/bg-3 DB pointers), DECISIONS D-051,
  AGENT_NAVIGATION, STATUS, this worklog.
---
iter-8h · 2026-08-29 · derived-index micro-pass (iter-8h-derived-indexes)
- Owner-directed: an external patch list (six items) verified against
  the code item by item before landing — each proven
  semantics-preserving; the rejected variant (plain per-knower token
  SETS) would have broken `holds(before_source=...)` (crime.py's
  novelty test). D-050 owns the rationale and the benchmark numbers
  (decay 45×, occ 40×, holds 664×, releases 24×, scene-delta 5×,
  salient 1.9×; harness outside the repo — D-012).
- Applied: `KnowledgeView` token→sources index (`add` the only
  writer; `holds` O(1)); Simulator `(entity, prop) → tick` index in
  `_commit` (`decay_drafts` signature `events` → `last_change`);
  scene-delta window break (tick-monotonicity); `salient()` top-1
  `max`; `occ_breaking_cause` one forward fold; director `entropy`
  once per `releases()`. Tests +2 contract pins; the T2 rebuild test
  extended to the token index; one brief-test fixture fixed to be
  log-shaped (it encoded an out-of-order log the writer forbids).
- 13 files (above the 3–5 soft cap: six independent micro-patches,
  each with its code target — the sync set is task-mandated):
  core/{knowledge,states,loop,intent,director}.py,
  brief/assembler.py, tests/{states,knowledge,brief}.py +
  DECISIONS/TASKS/STATUS/this worklog. Worklog found at 11 entries
  (iter-6's body had survived its own 8g tombstone) — evicted iter-6
  (per its tombstone) + iter-6a (this entry's one-in/one-out) back to
  the cap. 338→340 green, ruff clean, golden fixtures
  byte-identical. No new KIs.
---
iter-8g · 2026-08-29 · DF coverage audit (iter-8g-df-coverage-audit)
- Owner question: "is anything being missed in the giant DF exports?"
  Answer: `scripts/df_survey.py --audit` — coverage census instead of
  measured F7/F8 detail. For every top-level section: per-record-tag
  counts + every unique child-tag set per record tag (a structural
  fingerprint bounded by DF record uniformity — typically 1-3 variants;
  growth past 3 = drift signal). HANDLED records (historical_event /
  _collection / _figure — F7/F8 detail) marked; UNHANDLED records
  (site, entity, region, artifact, written_content, …) carry their
  child-tag sets so bg-1's SQLite sink can plan field extraction without
  re-parsing a 5 GB export. Replaces head/middle/tail positional
  sampling strictly — every variant captured, not three positions;
  runs in the same single streaming pass (no second parse). First
  `tests/test_df_survey.py` (9 tests) pins the four load-bearing
  invariants (sanitize, recover, census, audit render) on a tiny
  synthetic DF-like XML. Coverage matrix: `docs/ref/df_legends_xml.md`
  ("Coverage matrix — survey vs SQLite sink" section).
- 8 files (above the 3–5 soft limit; the §6 sync set is task-mandated
  — every AGENTS §6 touched file updated in the same iteration):
  scripts/df_survey.py (the --audit flag + census + render section),
  tests/test_df_survey.py (new), docs/ref/df_legends_xml.md (coverage
  matrix), docs/TECH_NOTES.md §3 (audit note), STATUS.md (iteration
  header + FAQ sync + Next-step bg-1 update), this worklog, TASKS.md
  (bg-1 next-step note), docs/AGENT_NAVIGATION.md §1 (scripts/ row).
  329→338 green, ruff clean, fixture byte-identical. No new KIs.
- iter-6 evicted per the one-in/one-out cap (history in git).
---
iter-8f · 2026-08-29 · audit-fix: truncated-export survival + 101st type (iter-8f-audit-fix)
- Owner-approved option A after the iter-8e audit: KI#34 (raw ParseError
  on truncated exports) fixed in `scripts/df_survey.py` — tail check +
  `RecoveringReader` (open-element stack tracking, closing-tag synthesis
  at EOF, loud PARTIAL warnings); KI#35 ("site tribute forced" →
  war-geopolitics; vocabulary count re-anchored to TECH_NOTES §3.1).
  Verified: synthetic truncated fixture (3 synthetic closers = the exact
  region3 shape; sanitize delegation intact), byte-identical rerun,
  329 green, ruff clean.
- The owner's new upload ("large 500") is the completed re-export of the
  same small-dense region3-00500 world (4.95 GB, intact): the recovered
  prefix counts reproduce exactly (933,476 events · 99 types · micro
  7.71% · slayer 41.35%) — ground-truth validation of the recovery;
  third-column numbers into TECH_NOTES §3.1. 6 files (soft limit 5; the
  §5 drift-fix in docs/ref/df_legends_xml.md joined the planned 5).
---
iter-8e · 2026-08-28 · DF empirical F7/F8 survey (iter-8e-df-empirical-survey)
- Owner-requested (files attached; closes iter-8d's not-done item):
  `scripts/df_survey.py` — the sanitize+stream survey tool (byte-level
  CP437 control-byte strip + iterparse/clear; the validated bg-1 parsing
  core) over the owner's two exports; measured F7 (bookkeeping 52–57%,
  micro 7.7–8.8% notable-to-notable) and F8 (19–24% events in any
  collection; unique direct refs; single-parent trees; 39–58% slayer-less
  deaths) — numbers distilled into `docs/TECH_NOTES.md` §3.1 (single
  owner); F7/F8 verdict one-liners in `docs/ref/df_design.md`; KI#33
  schema-drift fix in `docs/ref/df_legends_xml.md` (event/eventcol tags,
  naming duality, many-to-many → single-parent correction).
- 10 files (above the 3–5 soft limit; task-mandated tool + numbers owner
  + 2 ref fixes + the AGENTS §6 sync set — precedent iter-8a): the tool,
  TECH_NOTES (numbers owner), 2 ref fixes, TASKS/STATUS (incl. KI#30–32
  deletion + FAQ gate-family merge to hold the ≤20 cap), this worklog,
  AGENT_NAVIGATION/README scripts rows, .gitignore dfworlds/ guard
  (iter-4 out per the one-in/one-out cap). 329 green, ruff clean.
  No new DECISIONS (research verdicts; iter-8d precedent).
---
iter-8d · 2026-08-28 · DF designed-experience deep dive (iter-8d-df-design-lessons)
- ref-17 (owner-requested research pass, the D-022 exception):
  `docs/ref/df_design.md` — the third DF entry (the player-facing
  half not owned by df_legends_xml.md / df_worldgen.md): six
  enchantment pillars P1–P6; flaw taxonomy F1–F10 by root cause —
  every flaw is a MISSING layer (salience/pacing/audience-
  epistemology/LOD/continuity), not wrong simulation; the successor
  trade-off matrix (each "fix" amputates a pillar — RimWorld/KoDP/
  Songs of Syx/Versu/Rain World/SS13/…); the structural read
  (layer-adding over an honest sim IS the canonsim thesis);
  reader-as-knower symmetry; bg-1 hardening (streaming/selective/
  name-normalization/determinism quarantine) + bg-2 ambiguity-as-
  data + bg-3 corpus-division guidance; a verdict table mapping every
  flaw to an existing mechanism or recorded phase.
- 5 files — the ref file + the D-026 mandated index flip
  (REFERENCES_DEEP §1+§2) + the AGENTS §6 sync set (TASKS incl. the
  bg-1 guidance link, STATUS incl. the KI#29 >2-iteration deletion,
  this worklog; iter-3 out per the one-in/one-out cap). Docs-only
  (fresh owner request; iter-9 stays the code iteration).
- 329 tests green, ruff clean (baseline re-verified before the
  pass). No new DECISIONS entries — research verdicts, not stable
  decisions; recommendations reach their owning docs by link only.
---
iter-8c · 2026-08-28 · owner-requested audit of iter-8a/8b (iter-8c-audit)
- All claims reproduced: 329 green, ruff clean, T1 byte-identical; the
  8b "2 false alarms" verdict verified against pre-8b git state (the
  (log, ledger) purity flip WAS already in BRIEF_SPEC §9/D-048); atlas
  MIT re-verified via the GitHub API. 3 KIs fixed: KI#30 — the D-018c
  letter-suffix citation never resolved (the KI#23/#28 false-citation
  family, propagated by 8b into D-049/worklog/phases.md; the lettering
  died at the iter-7 D-034 collapse, and even pre-collapse the
  structural boundary was D-018(b)) → plain D-018, 4 sites; KI#31 —
  blueprint §1 wording debts (stale 8a "pinned never auto-evicted"
  remnant vs the D-049 ledger-never-evicts resolution; lifecycle
  notation now matches the precedence/texture-OCC paragraphs:
  {active, pinned} → terminal states); KI#32 — sync misses (TASKS
  ref-N line gained ref-16; BLUEPRINT BRIEF-1 gained the atlas donor
  line + corpus count per its own §0 deep-dive protocol).
- Verdict on the owner's question: NO rework of iter-1..8 needed —
  the 7th block lands additively (assembler Block/fill/eviction shape
  verified; zero new event types; the atomic flip set is enumerated in
  BRIEF_SPEC §9). Worklog reordered to strict newest-first. 6 files —
  audit fix set + mandated sync set (iter-6a precedent); docs-only,
  the D-022 fresh owner request (iter-9 stays the code iteration).
- 329 tests green, ruff clean, golden fixture byte-identical. No new
  DECISIONS entries (drift fixes, not decisions); DECISIONS stays
  33/30 transiently (collapse at the phase-1→2 gate, D-034).
---
iter-8b · 2026-08-28 · scene-ledger hardening (iter-8b-scene-ledger-hardening)
- Owner-requested dispute-resolution pass on an external LLM review of
  D-048: claims audited against the repo (2 false alarms — the purity
  flip was already in BRIEF_SPEC §9/D-048; "zero RNG" was never a
  log-determinism claim), 4 real gaps + 3 wording debts + 2 missed
  gaps (establishment-time canon check; texture-OCC mirror) → KI#29,
  closed same iteration. D-049: seven resolutions hardening the
  scene ledger in place — determinism quarantine, scene =
  PC-location interval, structural pinning, grammar/vocabulary split
  (core stays ledger-blind), render-vs-epistemics,
  ledger-never-evicts (bounds live in the brief),
  tombstones-in-brief; every resolution reuses existing law
  (D-018/D-035/D-037/D-047/L12/atlas).
- 7 files — the mechanism owner (blueprint/phases.md §1) + the
  mandated sync set (DECISIONS D-049, BRIEF_SPEC §9 atomic flip set,
  SPECS_BACKLOG VALIDATION_SPEC sketch, TASKS iter-9+, STATUS incl.
  KI#22–28 deletion, this worklog). Docs-only — the D-022 fresh
  owner request (no doc-loop alarm; iter-9 is code).
- 329 tests green, ruff clean, golden fixture byte-identical.
  DECISIONS transiently 33/30 (collapse at the phase-1→2 gate, D-034).
---
(iter-8a deleted at iter-10 per the one-in/one-out cap; history in git.)
(iter-8 deleted at iter-9 per the one-in/one-out cap; history in git.)
(iter-7 deleted at bg-1 per the one-in/one-out cap; history in git.)
(iter-6a deleted at iter-8h per the one-in/one-out cap; history in git.)
(iter-6 deleted at iter-8g per the one-in/one-out cap; history in git.)
(iter-5 deleted at iter-8f per the one-in/one-out cap; history in git.)
(iter-4 deleted at iter-8e per the one-in/one-out cap; history in git.)
(iter-3 deleted at iter-8d per the one-in/one-out cap; history in git.)
(iter-2a deleted at iter-8c per the one-in/one-out cap; history in git.)
(iter-2 deleted at iter-8b per the one-in/one-out cap; history in git.)
