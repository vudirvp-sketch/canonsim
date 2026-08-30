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
iter-19 · 2026-08-30 · owner-requested audit of two pasted spatial analyses (iter-19-spatial-audit)
- Verdict ~85–95% repo-true: time/space/canon-vs-texture mechanics
  confirmed (D-048/049/053/054/056, queue key, t+duration); the
  second text's corrections repo-exact (D-049 pinning, retire+
  establish, travel-over-weighted-move, layout-over-fire_spots).
- Omissions: drift family is ref-9-a/b/c + entt/bevy wide (phantom
  sim/systems, core/runner, core/store, content/packs/*.py);
  travel is queue-cheap today (clock jump-ahead); layout needs
  initial_projection seeding for canon_slot protection.
- KI#47 opened+closed: 9 grid phrases fixed (docs/ref/{libtcod,
  rot_js,red_blob_games}.md + REFERENCES_DEEP rows); lift-target
  vocabulary stanced in the STATUS FAQ (pre-D-028 precedent);
  st-6 spatial backlog row added (travel + layout, phase-5-gated).
- Docs-only (D-022 exception: fresh owner request); 547 green,
  ruff clean. 7 files (scope: the family-wide fix); iter-11b
  evicted per the cap.
---
iter-18 · 2026-08-30 · validation beats — session 5, the arson half
over the cards (iter-18-validation-beats-5)
- Live narrate session 5 (seed 20, 10 beats, 29 supported / 4
  refused-and-caught / 1 unverifiable, 0 canon violations): the fire
  cascade is in canon regardless of who stood where; the observable
  surface splits by location — cause-actor blind to ignition
  (token_absent on fire_in_<loc>), absent NPCs cannot perceive fire,
  no alarm in the canonical solo-arson scenario, an unmodeled
  fire_intensity prop reads insufficient_data (UAP), and a canon
  event is claimable by id+type even when the brief was silent.
- Corpus 41 → 51 (+10 arson-half cases); 537 → 547 green, ruff clean.
  4 files (fixture + the 3-doc sync set); KI#46 deleted per AGENTS §5
  (closed iter-16, >2 iterations past); iter-11a evicted per cap.
---
iter-17 · 2026-08-30 · validation beats — session 4, the crime
cascade over the presence machinery (iter-17-validation-beats-4)
- Live narrate session 4 (seed 15, 10 beats, 32 supported /
  2 refused-and-caught, 5 intents fed, 0 canon violations): the
  cascade's observable half reads through the cards (witnesses,
  per-witness knowledge, the purse carried across cards and through
  the flee — KI#46's read-side pinned); the suspicion half is
  invisible through the brief (no marker row expressible — the axis
  lookup is status-prefixed; suspicion_changed never enters
  scene_delta) → the tune-2 backlog row, owner's call.
- Corpus 32 → 41 (+9 crime-cascade cases: the blind-witness refusal,
  the uninferred purse_missing refusal, the rumor transfer, the
  carried purse); 528 → 537 green, ruff clean. 4 files (fixture +
  the 3-doc sync set); KI#45 deleted per AGENTS §5; iter-11 evicted
  per the worklog cap.
---
iter-16 · 2026-08-30 · validation beats — session 3 over the presence
machinery (iter-16-validation-beats-3)
- Live `narrate` session 3 (seed 7, 7 beats + 1 regen, 18 supported /
  1 unverifiable / 1 refused-caught, 0 canon violations): all st-1
  acceptance probes hold — quiet-beat room naming, the
  absent-presence refusal, sighting + pair tokens, scene-change
  follow, the promoted prop on the card scene line, post-rotation
  cards.
- KI#46 found live + fixed: the rotation left carried items behind —
  `rotation_plan` (core/crime.py) now rides `movement_changes`
  (core/resolvers.py, renamed public — the single owner of the
  carried-item position contract); regression test in test_crime.py.
- Corpus 25 → 32 (+7 presence probes, seed 7; tests/fixtures/
  narrator_beats.json). 520→528 green, ruff clean; no fixture bytes
  touched (the smoke script crosses no rotation). 8 files (2 code +
  1 test + fixture + the 4-doc sync set — the session+fix scope);
  TASKS pack-3 row parks the owner's Sci-Fi setting sketches;
  iter-10a evicted per cap.
---
iter-15 · 2026-08-30 · presence & entity cards — st-1 landed (iter-15-presence, D-056)
- The 8th brief block `present_entities` (entity cards: status markers,
  carries, promoted props, the scene line, directed pair tokens; ranking
  caps; eviction between scene_texture and voice) + the write-side twin:
  the actor-held per-present-target `knows` expansion on move (the
  arrival snapshot, INTENT_SCHEMA §7 — KI#43's grammar, not an audience).
- present_entities/present_in_order moved to core/fold.py (single owner);
  BRIEF_SPEC §3 table+§3.4 renumber+§5.2+§6+§9, INTENT_SCHEMA §7, pack
  (move template, brief.present_entities, 2 pair seeds), TASKS/NAV sync.
- T1 fixture regenerated (iter-3 precedent; +10 records, stream
  identical); KI#45 (stale §3.4 citation) closed. 502→520 green, ruff
  clean. 10 files + sync set; iter-10 evicted per the cap.
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
- (deleted at iter-19 per the one-in/one-out cap; history in git.)
---
iter-11a · 2026-08-29 · post-iter-11 audit (iter-11a-audit-fix)
- (deleted at iter-18 per the one-in/one-out cap; history in git.)
---
iter-11 · 2026-08-29 · texture promotion door — the narrator boundary's LLM-free half (iter-11-texture-door)
- (deleted at iter-17 per the one-in/one-out cap; history in git.)
(iter-10a deleted at iter-16 per the one-in/one-out cap; history in git.)
iter-10 · 2026-08-29 · scene-ledger LLM-free half (iter-10-scene-ledger)
- (deleted at iter-15 per the one-in/one-out cap; history in git.)
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
