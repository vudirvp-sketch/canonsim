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
- df_survey.py (sanitize + stream core for bg-1) over the owner's two
  exports; measured F7/F8 → TECH_NOTES §3.1 (single owner); KI#33
  schema drift fixed in df_legends_xml.md. 10 files.
- 329 green, ruff clean. No new DECISIONS (research verdicts).
---
iter-8d · 2026-08-28 · DF designed-experience deep dive (iter-8d-df-design-lessons)
- ref-17 docs-only pass (the D-022 exception): docs/ref/df_design.md —
  pillars P1–P6, flaw taxonomy F1–F10 (every flaw a MISSING layer),
  successor trade-off matrix, bg-1/2/3 guidance, flaw→mechanism
  verdict table. 5 files.
- 329 green, ruff clean, byte-identical. No new DECISIONS.
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
