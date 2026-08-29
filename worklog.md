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
iter-14 · 2026-08-30 · validation beats — session 2, the corpus completes (iter-14-validation-beats-2)
- Live `narrate` session 2 (seed 8, theft-and-arson scenario, 12 beats,
  22 supported claims, 0 canon violations): event_type_mismatch,
  cannot_know, stale_ref, exhaustion→dry, door-rejected intent, rebased
  intents, pin/retire+establish/no-op — all probed live, all caught.
- Corpus 16→25 (tests/fixtures/narrator_beats.json): every validator
  refusal reason + the ladder + both door outcomes pinned at the beat
  level; source line carries both sessions' provenance.
- 493→502 green, ruff clean. 5 files (fixture + sync set); iter-9
  evicted per the cap.
---
iter-13 · 2026-08-30 · validation beats — first live agent-in-the-loop session (iter-13-validation-beats)
- Real `narrate` session (seed 125, 11 beats): 0 canon violations;
  every refusal family probed and caught live (claims, gateway, OCC,
  ladder); the quiet-beat hole confirmed (no presence block — st-1
  evidence, not implemented).
- KI#44 fixed: accepted beats print `BEAT` claims/texture/intents/
  rebased summaries (cli/mediator.py + cli/main.py; VALIDATION_SPEC
  §7.1) — the phase-1 exit numbers are countable in live play.
- The phase-1 regression set: tests/fixtures/narrator_beats.json (16
  cases from the session) replayed through the real cycle
  (test_mediator.py); CLI wiring pinned (test_cli.py). 476→493 green,
  ruff clean; bg-1 evicted per the cap.
---
iter-12 · 2026-08-30 · the mediator session loop — agent-in-the-loop (iter-12-mediator-loop)
- Owner verdict D-055: no SoW/llama.cpp — the dev-time narrator is the
  external agent over files (INV-4 holds); SoW audit parked as bg-6.
- brief/mediator.py (call/response docs, feedable_intents, promotions
  scan) + cli/mediator.py (the D-049 beat cycle + the L12 ladder) +
  `narrate` commands + ledger check_delta_shape.
- Specs synced: BRIEF_SPEC §7.1 (314/300 — §6.1 pass done, the over-cap
  is the new format law), VALIDATION_SPEC §7.1, TASKS/STATUS/
  AGENT_NAVIGATION; KI#42 deleted per §5.
- 453→476 green, ruff clean; iter-8h evicted per the cap.
---
bg-5 · 2026-08-30 · owner-requested external-spec verdict (bg-5-spec-verdict)
- Pasted behavioral-engine integration spec audited against the repo
  + live-char-guide: every D-ID/INV citation resolves, no repo drift;
  not integrated (renames of the MECW/st-1/st-2 vocabulary, fatigue
  emulation re-rejected per ref-13 weakness (4) with INV-5 cited
  inverted, AP-16 + figures invented with no owner).
- Adoptions: backlog amendments only — Script Tax at the mediator
  (st-4) + the repetition-counted promotion option (st-2). KI#39–41
  deleted per AGENTS §5. 3 files; docs-only, D-022 counter = 3.
---
iter-11c · 2026-08-30 · owner-requested iter-11b re-check (iter-11c-audit)
- Verdict: sound — every claim reproduced against the code (453
  green, ruff clean, fixtures byte-identical; perception tokens,
  prop-birth shape, O(N)/beat folds, records_of, canon-slot check,
  D-ID/section citations, caps, KI lifecycle — all exact).
- KI#43 closed: MECW figure gains its single owner (TECH_NOTES §2,
  provenance + rot marker; blueprint §1 links), the arrival snapshot
  re-named to the actor-held per-present-target `knows` expansion
  (INTENT_SCHEMA §7/§10), container cycle guard += the commit gate
  (D-035). 5 files; docs-only, D-022 counter = 2.
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
(iter-9 deleted at iter-14 per the one-in/one-out cap; history in git.)
---
iter-8g · 2026-08-29 · DF coverage audit (iter-8g-df-coverage-audit)
- (deleted at bg-5 per the one-in/one-out cap; history in git.)
---
iter-8f · 2026-08-29 · audit-fix: truncated exports + 101st type (iter-8f-audit-fix)
- (deleted at iter-11c per the one-in/one-out cap; history in git.)
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
