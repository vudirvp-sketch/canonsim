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
iter-29 · 2026-08-31 · pack-2 — the arson-on-ashes door check
(iter-29-pack2-spot-available; the owner's finish-phase-1 directive,
polish item 3)
- The closed precondition set gains `spot_available` (the 15th test):
  the target location holds an unburning spot of the declared layer —
  the exact condition the ignite resolver keys on (door and resolver
  agree by construction); the arson requires carry it, the `layer`
  param is lint-checked against rules.json transitions (a typo would
  KeyError mid-run). INV-3 caught my own first docstring draft ("door
  guard"/"arson" — setting words) — rewritten, the stoplist holds.
- Arson on a destroyed or fully-burning location is now an
  intent_rejected no-op (failed_test target.spot_available) — the
  door-outcome vocabulary's fourth axis; the iter-24 no-ignition
  success (a success that pretended the world changed) is closed. The
  seed-41 corpus probe flipped with it (renamed + prose/last_event_type
  updated + a provenance note in the fixture's `source`).
- 626→629 green, ruff clean. 8 files (core intent/pack + actions +
  corpus + the doc sync set); D-061; iter-19 evicted per the cap.
  Docs: INTENT_SCHEMA §3 (the test row), TASKS, STATUS, DECISIONS
  (transiently 33/30 — collapse due at the phase-2→3 gate per D-034).
---
iter-28 · 2026-08-31 · tune-2 — the crime cascade renders on the
cards (iter-28-tune2-card-markers; the owner's finish-phase-1
directive, polish item 2)
- The declared candidate landed: `status_markers` → the prop-path
  `card_markers` table (threshold rows `min` + value rows `value`; the
  closed marker surface `status.<axis>` / `relations.<axis>` /
  `crime_status`, lint-checked against the declared axes); the render
  segment is `markers=` (the old `status=` lied for non-status props);
  the pack ships `wary` at suspicion ≥ 25 (aligned with the
  status_suspect_at flip) + `suspect`/`caught` on the player's card —
  iter-17's claimable-but-invisible asymmetry resolved in the
  readable-tension direction.
- The scene_delta half of the finding resolved as lawful blindness
  (NOT a defect): `suspicion_changed` rides no knowledge record and the
  delta window is the PC's perception (blind-NPC, D-037) — the card is
  the narrator's read surface, the delta window the player's; both
  pinned by tests. The corpus `status=afraid` pin updated to
  `markers=afraid` (render format, no canon impact).
- 619→626 green, ruff clean. 9 files (assembler + lint + pack + the
  doc sync set — within the 3–5 soft limit's family precedent); D-060;
  KI#50 deleted per AGENTS §5 (closed iter-26); iter-18 evicted per
  the cap. Docs: BRIEF_SPEC §3.4/§6 (the table law + the render
  format), TASKS, STATUS, DECISIONS (transiently 32/30 — collapse due
  at the phase-2→3 gate per D-034).
---
iter-27 · 2026-08-31 · tune-1 — the rest action + the story-critical
importance hook (iter-27-tune1-rest-importance; the owner's
finish-phase-1 directive opening the polish menu)
- The D-045(b) knob: `importance.score.story_critical_event` (+2) +
  `importance.story_critical_events` (19 event types, lint-closed
  against the template vocabulary); `pack_importance` takes the event
  type (all 12 emit sites: actions, transitions, crime, knowledge,
  states, rotations); the tale gate follows low→medium (templates.json)
  — the RULE owns the signal/noise split, the gate is not the knob.
  Evidence: day1_full seed 125 OFF renders 47 events → 14 tale lines —
  the theft ladder, both handovers, both briefings, the fire chain;
  zero decay/wariness/wait lines (the T7 noise floor: 27/47 events were
  repetition). Pinned by the tale-split regression test.
- The KI#4 counter-play: `rest` (13th action, 60 ticks, fatigue −30)
  as pack data — the new `recuperate` resolver applies the action's
  `status_effects` (projection-read `from_`, scale-clamped, zero-delta
  skip); pack lint refuses a typo'd story-critical entry, a
  status_effects block on a non-recuperate resolver, an undeclared
  axis, a zero delta. The 1000-sim baseline re-run IDENTICAL (importance
  is an annotation; the canon stream untouched); T1 fixture
  byte-identical (smoke = move/wait only); the mediator dry floor now
  distinguishes "no tale-worthy lines" from "no new canon events"
  (the medium gate made the old wording a lie).
- 610→619 green, ruff clean. 17 files (two subsystems + the doc sync
  set — the iter-15/20 scope precedent; one task ID per TASKS tune-1);
  D-059; KI#49 deleted per AGENTS §5 (closed iter-25); iter-17 evicted
  per the cap. Docs synced: MVP_SCOPE §2/§7/§9, EVENT_SCHEMA §6 +
  schema description (non-breaking), INTENT_SCHEMA §6, TEST_PLAN T7,
  AGENT_NAVIGATION §1, TASKS, STATUS, DECISIONS (transiently 31/30 —
  collapse due at the phase-2→3 gate per D-034).
---
iter-26 · 2026-08-31 · phase-1 gate review — the verdict + the
collapse (iter-26-phase1-gate)
- Evidence re-run per ROADMAP §5: 610 green + ruff clean; T1
  byte-identity + the fixture guard (the venv 3.12.14 = the fixture's
  generating interpreter); T8 single-factor A/B on day1_full/seed 125 —
  OFF 26 chains, ON M1=0.417 / M2=0.500; T7 — the chronicle re-read:
  the theft→suspicion→rotation→briefing and break→fire→burnout chains
  read causally across the day boundary, the decay/wariness repetition
  is the noise floor (tale_gate = the tune-1 knob, owner's call). Exit
  criterion MET with margin: 109 live beats (the accepted-beat sum
  alone 104) / 0 canon violations / corpus 105 green; no kill hit
  (0 breaches in 109 beats — the per-1000 kill reads a rate the live
  volume cannot yet reach, recorded honestly).
- DECISIONS collapsed 41→30 per D-034 (the owner's quality-first
  directive — cleanup INSIDE the gate iteration): 7 family merges, all
  58 D-IDs resolve (verified by sweep — every D-ID is cited), survivors
  verbatim, merged rows keep decision→why→consequence + owner links.
  D-058 = the PASS verdict. KI#50 opened+closed (the FAQ cap-laws
  bullet cited D-025/D-026 — D-026 is the per-ref split; fixed).
  doc-1 VISION freeze review closed clean (frozen text verified against
  phase-1 reality; the freeze stands).
- TASKS Done consolidated (pre-mediator entries → one-liners per
  AGENTS §6; all 70 entries verified preserved; TASKS 683→477, back
  under the 600 cap). Verdict: phase-1 PASS — phase 2 (Parser, mode C)
  may open, the phase-2-vs-polish call stays the owner's. 4 files (the
  doc sync set; no code — the gate review IS verification + collapse
  work, the owner's fresh request per D-022); iter-16 evicted per the
  cap.
---
iter-25 · 2026-08-31 · validation beats — session 10, the
witnessed-steal-then-alarm chain (iter-25-validation-beats-10)
- Live narrate session 10 (seed 93, 6 accepted beats + 2
  refused-and-caught documents, 34 supported claims, 5 intents fed, 0
  canon violations): sessions 4 and 6 back to back — a total-failure
  steal (everyone saw; suspicion 35 room-wide, crime_status suspect
  at the failure) → a silent second steal → the t=360 rotation
  (expectation_violation pushes both guards to 55, past the
  document_check threshold 50) → **the director releases
  director_0000 live for the first time in a narrate session** (the
  v0.1 stub wait, npc_guard_01 t=409, claimable by id+type — ev_0025,
  a canon event no card or brief surfaces) → the arson-as-distraction
  through the door (fire_started + alarm_raised raised_by the relief
  guard + fear 40 claimable per NPC; the cause actor hears his own
  alarm) → flee_caught at t=535 (the door batch drained the fire
  cascade to location_burned_out t=533 first; crime_status stays
  suspect — 55 < the arrest threshold 75; the purse stays on the
  thief's card through the catch).
- Probes: the outgoing guard's fire blindness (npc_guard_01 rotated
  out pre-fire → `fire_in_loc_tavern` token_absent — session 8's
  transfer-bounded-by-holder law under the document-check context) +
  1 live MALFORMED catch (the 'anchor' placeholder left in a live
  reply — corpus-test sugar, never a live document; the boundary's
  shape gate caught it; FAQ pitfall (5)).
- Corpus 99→105 (+6 seed-93 cases, 8 beat documents — the arson rides
  a `between` batch, the flee rides the door: the iter-23
  batch-boundary lesson applied); 604→610 green, ruff clean. 5 files
  (fixture + the 4-doc sync set — incl. KI#49: AGENT_NAVIGATION §1's
  corpus descriptions made structural, the fixture-count drift
  family); iter-24's missing TASKS one-liner backfilled (its commit
  skipped it — the iter-22 precedent, found via `git show --stat`);
  iter-15 evicted per the cap. TASKS 639→683 stays over the 600 cap
  by substance (the iter-22/23 precedent — the session findings and
  the backfill carry load; the last cruft pass ran iter-22). Live
  beats 101→109 — the corpus moves to the phase-1 gate review
  (ROADMAP §2).
---
iter-24 · 2026-08-31 · validation beats — session 9, the day-2
return under burned-yard knowledge (iter-24-validation-beats-9)
- Live narrate session 9 (seed 41, 13 accepted + 2 refused-and-caught,
  39 supported claims, 0 canon violations): the day-1 theft-and-arson
  chain (move → take → steal → move → drop_break → wait 1440) lands
  at t=1452 (day-2 morning post-second-rotation); the recall block
  past day 1 probed at the beat level (a quiet prose-only beat
  accepts with no BEAT summary — the absence-of-summary law).
- The day-1 canon events all claimable by id+type under day 2
  (fire_started / location_burned_out / expectation_violation /
  watch_change — canon never closes across a 1440-tick gap,
  complement to session 5's id+type probe on the same tick); the
  burned yard's `destroyed` flag is canon-from-birth state-claimable
  under day 2 (the layout/D-057 precedent extended to a destruction
  flag).
- The arson-on-a-destroyed-yard case is the pack-2 backlog's first
  live probe: both fire spots still 'burning' (set t=12/15, never
  reset — the halted-state law), `_ignite_action` finds no unburning
  spot, commits the arson event with `spot=None`, no ignition
  follows — a no-ignition success (distinct from session 8's
  spotless-street `field_nonempty` failure; the door-outcome
  vocabulary completes its three axes: not co-located, no flagged
  target, no fuel). The cause-actor blindness and the §3 market leg
  pinned unreachable under day 2 (the tune-3 family); the third
  watch_change (t=1812) hands purse_missing to the relief guard
  (inferred/exact → told/partial, the transfer_decay_steps=1 law
  under day 2); the suspicion axis state-claimable for
  npc_guard_01 (value 20, the tune-2 boundary re-pinned).
- Corpus 84→99 (+15 seed-41 cases, single-beat each); 589→604
  green, ruff clean. The phase-1 ≥100-beat exit criterion HIT
  (86→101 live beats); the sandbox narrate-session recipe landed
  in the STATUS FAQ (the owner's directive — operational recipe +
  pitfalls made durable across iterations; consolidated with the
  iter-23 batch-boundary lesson). 4 files (fixture + the 3-doc
  sync set — the iter-18 scope precedent); iter-14 evicted per
  the cap.
---
iter-23 · 2026-08-31 · validation beats — session 8, the
arson-after-theft chain (iter-23-validation-beats-8)
- Live narrate session 8 (seed 85, 12 beats + 3 refused-and-caught
  probes, 49 supported claims, 0 canon violations): the take →
  silent steal → drop_break → fire chain under a successful-theft
  context — sessions 4/5/7 tied; both prizes on one coat, the
  departure token (`pc_01_left_toward_loc_backyard`) claimable at
  the yard arrival.
- The unseen arson: the rotation hands the crime half across the
  watch change (purse_missing inferred/exact → told/partial, the
  trail + noise tokens, suspicion 20 both guards — crime_status
  stays unknown post-inference, 20 < 25) while the fire half never
  crosses — guard-side fire tokens all token_absent refusals (the
  transfer bounded by what the holder holds; session 6's positive
  half complemented). The arsonist's calm (status.fear 0 — the
  cause-actor fear exclusion) and the cause-actor blindness refusal
  pin the ignition exception from both sides.
- The flee fed through the door from a burned-out yard (the
  unpursued half; the purse leaves the fire, the lamp stays); the
  street arson attempt commits intent_rejected (claimable by
  id+type — a new door-outcome action kind); the maid's autonomous
  urgency event claimable by id+type; the §3 market leg pinned
  unreachable live (tune-3 family).
- Corpus 70→84 (+14 seed-85 cases; the post-cascade batch structure
  expressed as the flee-intent beat + between-steps — byte-equal to
  the live stream, the new FAQ lesson); 575→589 green, ruff clean.
  4 files (fixture + the 3-doc sync set — the iter-18 scope
  precedent); iter-13 evicted per the cap; TASKS 611→627 stays over
  the 600 cap by substance (the iter-22 precedent — session findings
  carry load).
---
iter-22 · 2026-08-31 · validation beats — session 7, the theft half
under the presence machinery (iter-22-validation-beats-7)
- Live narrate session 7 (seed 54, 11 beats, 24 supported /
  1 refused-and-caught, 0 canon violations): the pre-steal arrival
  snapshot pins the cards BEFORE the crime (guard carries purse,
  barkeep carries club, drunkard's intoxication 50 renders the
  `drunk` marker; the drunk→guard fear 40 + maid→barkeep trust 70
  pair tokens render as directed pair lines — the second seeded pair
  axis now state-claimed, complement to session 3's drunk→guard
  probe under seed 7).
- A successful first steal moves the purse silently — no
  witnessed_steal_failure, no suspicion, crime_status stays
  `unknown` (the silent-steal vs failed-steal fork in the steal
  ladder; session 4 took the failed half). The watch rotation
  carries the standard crime cascade; the expectation_violation
  event is claimable by id+type (complement to session 5's
  fire-event-by-id); post-inference purse_missing is positively
  claimable for both guards (inferred/exact for the victim,
  told/partial — one fidelity step down — for the relief guard,
  the transfer_decay_steps=1 law live at the beat level).
- The suspicion axis is state-claimable for both guards even
  though no card marker renders it (the tune-2 boundary —
  observability ≠ claimability; the projection holds the value
  the brief does not surface). The second steal after watch
  rotation returns intent_rejected (target moved to guardroom —
  co-location precondition fails, distinct from session 4's
  second-steal-success case where the guard stayed put); the
  stolen purse rides a plain move (no pursuit) to the backyard
  (KI#46's contract in a non-pursuit context); the
  witness-cannot-know-purse_missing refusal pins the inference
  boundary (the barkeep never held the purse-on-himself
  expectation — token_absent).
- Corpus 59→70 (+11 seed-54 cases); 564→575 green, ruff clean.
  4 files (fixture + the 3-doc sync set — the iter-18 scope
  precedent); iter-12 evicted per the cap; iter-21's missing
  TASKS one-liner backfilled (the iter-21 commit skipped it);
  TASKS 584→611 — the §6.1 cruft pass ran (iter-7/8/8a/8c/8g/4a
  trimmed, no substance cut) — substance remains: the iter-22 +
  iter-21 one-liners carry load-bearing session findings (the
  silent-steal fork, the expectation_violation id+type probe, the
  tune-2 re-pin); AGENTS §6.1 substance-vs-cruft law: stays over,
  recorded here.
---
iter-21 · 2026-08-31 · validation beats — session 6, the alarm
cascade (iter-21-validation-beats-6)
- Live narrate session 6 (seed 33, arson in the crowded taproom,
  12 beats + 2 refused-regen probes, 53 supported / 0 canon
  violations): with witnesses present the cascade session 5 could
  never fire now fires — alarm_raised (raised_by the first
  occupant in pack order), the fear spike 40 claimable per NPC and
  rendered as the `afraid` card marker, cause actor hears
  fire_alarm_in_<loc> yet stays blind to fire_in_<loc> (session
  5's law holds witnessed).
- The §3 watch-change handover live: the rotation carries the
  purse (KI#46) while knowledge_transfer hands the whole fire
  record set to the relief guard (told, one fidelity step down) —
  knowledge moves, fear does not (40→36 decay at the beat, D-050);
  flee_caught and the plain walk-out after it pinned at the beat
  level.
- Finding → tune-3 backlog row: shouting_near_<loc> is structurally
  unreachable in v0.1 (NPC placement static, the rotation a direct
  post swap, playscript steps player-only) — the guardroom
  refusal pair pins the boundary.
- Corpus 51→59 (+8 seed-33 cases); 556→564 green, ruff clean.
  4 files (fixture + the 3-doc sync set — the iter-18 scope);
  bg-5 evicted per the cap; KI#47 deleted per AGENTS §5.
---
iter-20 · 2026-08-30 · universality pass — the transition + scene-line
vocabularies become pack data (iter-20-universality, KI#48 + D-057)
- core/transitions.py iterates rules.json transitions.<layer>.
  follow_ups (kinds/flags/values/blocked_by) + spot_state/halt_flag;
  resolvers + the director's threat sensor read the declared
  vocabulary; pack lint joins every kind to an event + knowledge
  entry. Tavern behavior byte-identical (T1 fixture untouched); a
  synthetic `rot` layer (infested/condemned/stench/collapse)
  proves generality (test_transitions.py).
- `layout` on all 5 locations + brief.present_entities.
  scene_line_fields: the scene line renders pack fields
  canon-from-birth (assembler, BRIEF_SPEC §3.4/§6; the corpus
  call_contains line updated to the new scene-line shape).
- KI#48 opened+closed: iter-19's "canon_slot reads top-level fields
  only / seeding needed" was false both ways (the ledger reads BOTH
  prop sources — KI#41 precedent) — STATUS/worklog/TASKS phrases
  fixed in place; st-6 shrinks to the travel half.
- 547→556 green, ruff clean. 17 files (two subsystems + the doc
  sync set — over the 3–5 soft limit, the iter-15 scope
  precedent); iter-11c evicted per cap.
---
iter-19 · 2026-08-30 · owner-requested audit of two pasted spatial analyses
- (deleted at iter-29 per the one-in/one-out cap; history in git.)
---
iter-18 · 2026-08-30 · validation beats — session 5, the arson half
- (deleted at iter-28 per the one-in/one-out cap; history in git.)
---
iter-17 · 2026-08-30 · validation beats — session 4, the crime cascade
- (deleted at iter-27 per the one-in/one-out cap; history in git.)
---
iter-16 · 2026-08-30 · validation beats — session 3 over the presence
machinery (iter-16-validation-beats-3)
- (deleted at iter-26 per the one-in/one-out cap; history in git.)
---
iter-15 · 2026-08-30 · presence & entity cards — st-1 landed (iter-15-presence, D-056)
- (deleted at iter-25 per the one-in/one-out cap; history in git.)
---
iter-14 · 2026-08-30 · validation beats — session 2, the corpus completes (iter-14-validation-beats-2)
- (deleted at iter-24 per the one-in/one-out cap; history in git.)
---
iter-13 · 2026-08-30 · validation beats — first live agent-in-the-loop session (iter-13-validation-beats)
- (deleted at iter-23 per the one-in/one-out cap; history in git.)
---
(iter-12 deleted at iter-22 per the one-in/one-out cap; history in git.)
---
iter-11c · 2026-08-30 · owner-requested iter-11b re-check (iter-11c-audit)
- (deleted at iter-20 per the one-in/one-out cap; history in git.)
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
