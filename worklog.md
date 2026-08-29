# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.
> Entries re-trimmed to the line cap at iter-10a (KI#37; the drift ran
> iter-8b→10) — pre-trim detail lives in git history.
> Order: newest first (normalized at iter-8c — the order had drifted
> since iter-5).

---
iter-11b · 2026-08-30 · roadmap stress-test re-verified + problems 4–6 (iter-11b-stress-test-verified)
- D-022 owner pass, docs-only: the reported-but-lost stress-test
  reconstructed (KI#42 — archive expired, nothing in git), every claim
  re-verified against the code first (453 green, ruff clean); three
  sharpenings: coarse perception tokens (no snapshot semantics),
  prop-birth ≠ entity-birth promotion, O(N)/beat assembler folds.
- Problems 4–6 resolved: call-budget law (MECW), thinking = ephemeral
  texture, transcript-tail contract, mode-B knower parameterization,
  presence/entity cards + the chorus-call budget named; landed as
  blueprint §1/§5/§7 + BRIEF_SPEC §9 (+4 deferrals, cap 300 held) +
  GROUP_SPEC sketch + TASKS st-1..st-5. KI#37/38 deleted per §5.
  6 files; no code changes.
---
iter-11a · 2026-08-29 · post-iter-11 audit (iter-11a-audit-fix)
- KI#39 texture-take chronicle prose broken ("takes .") →
  {target?…|…} take templates + texture_slot derived slot (canon bytes
  unchanged); KI#40 unique-slot claim survives promotion (golden case
  17); KI#41 canon-slot overlap += pack-modeled fields (VALIDATION_SPEC
  §8 synced).
- Hardening: target+texture mix loud, lint (target-defended checks on
  texture actions, {texture_slot} in canon templates, texture
  failure_total consistency), texture-path OCC attribution test,
  doc-sync (INTENT_SCHEMA §9, AGENT_NAVIGATION, TASKS ## Done iter-11).
  443→453 green, ruff clean, fixtures byte-identical. 15 files + sync set.
---
iter-11 · 2026-08-29 · texture promotion door — the narrator boundary's LLM-free half (iter-11-texture-door)
- core/intent.py texture machine (reference shape gate, requires_for
  split, texture noun/test, texture_slot slot) + `_pickup` texture branch
  + loop/OCC wiring: a take-success on a resolved reference IS the
  promotion (canon birth, D-054); take texture-capable + real unique_slots
  ["hearth"] + pack lint; INTENT_SCHEMA §2/§3/§7 synced.
- Golden delta fixture 13→16: laundering + unique_slot pins (8/8 refusal
  reasons; the runner grows the mark_promoted beat op). 14 files + sync
  set (iter-9/10 precedent). 435→443 green, ruff clean, byte-identical. No KIs.
---
iter-10a · 2026-08-29 · post-iter-9/10 audit sync (iter-10a-audit-sync)
- KI#37 doc-sync: worklog re-trimmed to the line cap (the drift ran
  iter-8b→10; the iter-10 count 15→16), AGENT_NAVIGATION/README synced,
  the golden-delta coverage claim qualified (6 of 8 reasons pinned).
- KI#38: the INV-3 stoplist now scans `brief/` (engine-side since
  iter-8). 435 green, ruff clean. 6 files; iter-8b evicted per the cap.
---
iter-10 · 2026-08-29 · scene-ledger LLM-free half (iter-10-scene-ledger)
- brief/ledger.py (D-053): lifecycle, scenes as PC-location intervals,
  the ONE validation gateway (8 refusal reasons), retirement passes,
  texture-OCC mirror; scene_texture 7th block; BRIEF_SPEC §9 flip.
- 16 files (code+spec+suite+golden set + sync set, iter-9 precedent;
  golden delta fixture: 13 cases). 390→435 green, ruff clean. No KIs.
---
iter-9 · 2026-08-29 · VALIDATION_SPEC + validator LLM-free half (iter-9-validation-spec)
- docs/VALIDATION_SPEC.md (closed proposal doc, honest verdicts,
  ExpectedVersion OCC, fact transaction, ≤2-regens protocol) +
  brief/validator.py + validation_golden.json (18 verdict cases).
- 11 files (spec+code+suite+golden set + sync set, iter-8 precedent).
  352→390 green, ruff clean, byte-identical. No new KIs.
---
bg-1-sqlite-sink · 2026-08-29 · DF SQLite sink — bg-1 closed (D-051)
- scripts/df_import.py: typed cores + EAV + event_participant + links
  + generic JSON records; truncation policy owned; cross-validated on
  the large world (2.38 GB → 898 MB in 174 s).
- KI#36 opened+closed (UNDOCUMENTED marker; catches `artifact`,
  `historical_era`). 10 files. 340→352 green, ruff clean.
---
iter-8h · 2026-08-29 · derived-index micro-pass (iter-8h-derived-indexes)
- Owner-directed external patch list, each item proven
  semantics-preserving first (D-050): KnowledgeView token→sources
  index, Simulator (entity,prop)→tick index, scene-delta window break,
  salient top-1 max, occ forward fold, director entropy per releases().
- 13 files. 338→340 green, ruff clean, byte-identical. No new KIs.
---
iter-8g · 2026-08-29 · DF coverage audit (iter-8g-df-coverage-audit)
- df_survey.py `--audit`: coverage census (per-section record-tag
  counts + unique child-tag sets per record tag) in one streaming
  pass; coverage matrix → docs/ref/df_legends_xml.md; first
  test_df_survey.py (9 tests).
- 8 files. 329→338 green, ruff clean, byte-identical. No new KIs.
---
iter-8f · 2026-08-29 · audit-fix: truncated exports + 101st type (iter-8f-audit-fix)
- KI#34 truncated-export survival (tail check + RecoveringReader;
  ground-truth validated on the complete 4.95 GB re-export); KI#35
  "site tribute forced" → war-geopolitics. 6 files.
- 329 green, ruff clean, byte-identical.
---
iter-8e · 2026-08-28 · DF empirical F7/F8 survey (iter-8e-df-empirical-survey)
- (deleted at iter-11b per the one-in/one-out cap; history in git.)
---
iter-8d · 2026-08-28 · DF designed-experience deep dive (iter-8d-df-design-lessons)
- (deleted at iter-11a per the one-in/one-out cap; history in git.)
---
(iter-8c deleted at iter-11 per the one-in/one-out cap; history in git.)
(iter-8b deleted at iter-10a per the one-in/one-out cap; history in git.)
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
