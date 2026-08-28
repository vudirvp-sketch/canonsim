# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.
> Order: newest first (normalized at iter-8c — the order had drifted
> since iter-5).

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
iter-8a · 2026-08-28 · scene-ledger design pass (iter-8a-scene-ledger-design)
- Owner-requested continuity question (long scenes lose narrator texture;
  the brief is log-pure): absorbed the owner-supplied memory atlas as
  ref-16 (`docs/ref/agent_memory_atlas.md`, MIT verified) and designed
  the scene ledger into `docs/blueprint/phases.md` §1 — session-scoped
  append-only mediator stream, discrete states, canon outranks texture,
  intent-door promotion, laundering refusal, no TTL (D-048).
- Spec triggers synced (SPECS_BACKLOG VALIDATION_SPEC row, BRIEF_SPEC §9
  deferral) + TASKS sequencing + intake sync set (REFERENCES,
  REFERENCES_DEEP, CORE_DESIGN_RESEARCH §2, AGENT_NAVIGATION §1).
  12 files — task-mandated design set + the intake/sync set (iter-8
  precedent). Docs-only (D-022 owner-request exception).
- 329 tests green, ruff clean, golden fixture byte-identical. DECISIONS
  transiently 32/30 (collapse due at the phase-1→2 gate, D-034).
---
iter-8 · 2026-08-28 · BRIEF_SPEC + brief assembler (iter-8-brief-spec-assembler)
- docs/BRIEF_SPEC.md (trigger fired at phase-1 start: six-block pipeline,
  two-level budgets — soft fill target / hard per-item ceiling /
  total_hard whole-block eviction with `[truncated:N]` markers and
  never-drop-directives, voice isolation L2, max_items = ranking cap not
  budget drop, §9 just-in-time deferral table) + brief/assembler.py
  (pure functions of the log, ZERO RNG — byte-identity on the golden
  fixture across calls, PYTHONHASHSEED-independent; beat arithmetic =
  the read-side mirror of the loop's day-1-edge law) + rules.json::brief
  pack contract (budgets + directives/lore/exemplars text) +
  core/pack.py::_brief lint (BRIEF_BLOCK_IDS closed enum) +
  tests/test_brief.py (30 tests). D-047 recorded — DECISIONS transiently
  31/30 mid-phase (iter-1 precedent; collapse due at the phase-1→2 gate).
- 13 files — task-mandated set (spec + assembler + pack + tests + lint)
  + the AGENTS §6 sync set (TASKS/SPECS_BACKLOG/AGENT_NAVIGATION/STATUS/
  worklog/README/DECISIONS). 299→329 tests green, ruff clean, golden
  fixture byte-identical.
---
iter-7 · 2026-08-28 · phase-1 intake (iter-7-phase1-intake)
- Owner-requested retrospective at the phase boundary: baseline
  re-verified (299 green + ruff clean), then the D-034-mandated
  DECISIONS collapse 46→30 (ID-preserving family merges; compound IDs
  use the FULL prefix per member — `D-018/022/029` does not resolve,
  the FAQ law); 55KB→20KB. TASKS.md regained the what-next ownership
  (phase-1 sequence: iter-8 BRIEF_SPEC + brief assembler; iter-9+
  VALIDATION_SPEC; tune-1 knobs); STATUS Next step → pointer.
- Intake audit fixes: KI#25 stale `_enqueue_autonomous` docstring
  (beat-tick claim vs the entry-tick law); KI#26 dead-parameter family
  (Director.releases knowledge — L6-dangerous false interface;
  briefing_draft projection; urgency_intents beat_tick; _axis_deltas
  pack) removed with call sites + tests; KI#27 README drift (298→299,
  "systems land iter-2"); KI#28 residual false "AGENTS §9" citation in
  AGENT_NAVIGATION §1 (the KI#23 family — iter-6a missed this instance).
  KI#21 deleted (closed >2 iters); FAQ: ref
  places + graveyard merged (20 held), the collapse law added.
- 13 files — intake fix set + mandated sync set (precedent: iter-4a/6a).
  299 tests green, ruff clean, golden fixture byte-identical (dead
  params — no canon-path change).
---
iter-6a · 2026-08-28 · owner-requested code audit of iter-5/6 (iter-6a-code-audit)
- Re-verified end-to-end: 298 green + ruff clean reproduced; the 1000-sim
  baseline reproduces EXACTLY; T8 OFF = 26 chains / ON = director_0000;
  chronicle PYTHONHASHSEED-independent; session doors + KI#17 gate
  correct; tale_gate claims accurate (medium → 4 events).
- 3 KIs fixed: KI#22 TEST_PLAN/test-docstring drift (seed 32→125 ×4,
  24→26 ×2, M2 formula vs MVP_SCOPE §15 + impl, §6 filename, §1.2
  per-endpoint note); KI#23 scripts/ outside the executable invariants
  + the false "AGENTS §9" citation + the 5–15%/73–83% qualifier loss
  (D-046; PACKAGE_DIRS += scripts + closure test + CLI-class print
  exemption, MVP_SCOPE §18 pinned); KI#24 dead fold_events removed.
- KI#17–20 deleted (closed >2 iters); KI entries to the 2-line cap; FAQ
  24→20 (purity/drift/fixture/gate families merged + the chain-counting
  law added). 11 files — audit fix set + mandated sync set.
- Tests 298→299 green (+1 closure test); ruff clean; golden fixture
  byte-identical. No canon-path change: the drift was in citing
  documents, not in the numbers.
---
iter-6 · 2026-08-28 · phase-0 gate (iter-6-gate) · **VERDICT: PASS**
- TEST_PLAN.md (trigger-fired spec: T0-T8 + M1-M5 + gate protocol + UAP
  crosswalk + §3 schema-bump migration) + core/metrics.py (M1-M5 +
  emergent chains as pure functions of the log) + test_metrics.py (24)
  + the T1 fixture-regeneration guard + tests/playscripts/day1_full.json
  (seed 125) + test_t8_ab.py (single-factor A/B) +
  scripts/balance_harness.py (KI#4 close) + rules.json::metrics.
  11 files — task-mandated. D-042/D-043/D-044/D-045 recorded.
- Tests 264→298 green (+34); ruff clean; golden fixture byte-identical.
  T7 playtest + the full verdict evidence live in D-045; the 1000-seed
  baseline numbers live in D-044 + STATUS KI#4 (M5 p50=0.77, chains
  p50=20, M3_mean p50=13.81, M1 p50=0.24). Track A frozen.
---
(iter-5 deleted at iter-8f per the one-in/one-out cap; history in git.)
(iter-4 deleted at iter-8e per the one-in/one-out cap; history in git.)
(iter-3 deleted at iter-8d per the one-in/one-out cap; history in git.)
(iter-2a deleted at iter-8c per the one-in/one-out cap; history in git.)
(iter-2 deleted at iter-8b per the one-in/one-out cap; history in git.)
(iter-4a deleted at iter-8a per the one-in/one-out cap; history in git.)
(iter-0aa deleted at iter-7 per the one-in/one-out cap; history in git.)
(iter-1 deleted at iter-8 per the one-in/one-out cap; history in git.)
