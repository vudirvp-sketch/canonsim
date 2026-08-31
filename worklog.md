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
bg-2 · 2026-09-01 · event taxonomy — the 120-entry corpus + the sink v2 plus pass
(bg-2-event-taxonomy; the owner supplied the four world exports)
- scripts/df_import.py: plus pass, SINK_VERSION 2 — the companion's
  historical_events land in a separate event_plus_fields EAV keyed by
  the same ids (706,157 events -> 3,509,709 rows on the large world;
  main counts unchanged; everything else in the companion
  counted-not-stored). D-051's recorded deferral fired: item_stolen
  thief/item/method (100% coverage) and creature_devoured
  eater/victim/race live ONLY there.
- scripts/df_taxonomy.py (new): 15 event-type plans + the birth gap +
  war/beast-attack collection plans; fixed quantile-spread selection —
  pure function of the DB content; per-entry participants/place/
  reconstructed cause/witness/long-term consequence -> output/
  df_taxonomy_<stem>.txt (gitignored, reproducible).
- docs/TAXONOMY.md (new, 335 lines): 120 entries across the 16 TASKS
  bg-2 target types (AC >=100 MET) + the E/E+/R/GAP verdict table
  against EVENT_SCHEMA + measured findings: witness gap (9/88 — DF has
  no epistemology events), the hfid1/hfid2 participant-index blind spot
  (25,079 reputation events lift 0 rows), murders always carry
  slayer+site (5,786/5,786), item loss mostly terminal (6/8).
- Tests 664->673 (+6 tests/test_df_taxonomy.py, +3 the plus-pass suite
  in tests/test_df_import.py), ruff clean. KI#54 deleted per AGENTS
  §5 (closed iter-32, two iterations past). Doc-sync: TECH_NOTES §3.2
  (plus-pass recipe + the blind spot), TASKS bg-2 done, STATUS, AGENT_
  NAVIGATION §1, SPECS_BACKLOG row, README, D-063; iter-25 evicted per
  the cap.

---
iter-33 · 2026-09-01 · parse-1 batch 2 — say-door corpus growth
(iter-33-parse1-say-sessions2; the owner's corpus-growth call)
- Four more live mode-C sessions (seeds 111/65/30/32 — the
  untested-verbs walkthrough, the scene-close retirement, the
  disambiguation ladder + the muse families, the narrator withdrawal)
  driven by a runner outside the repo (scripts/iter33_parse_runner.py,
  Rule 9) through the REAL stack (Simulator + Mediator + ParserDoor
  over ONE shared ledger, D-049).
- Batch tally (PARSER_SPEC §6): 21 utterances (14 intent / 4 question /
  2 no_intent + 1 gate-passed door-rejected cycle), 3/3 deliberate
  off-grammar probes caught loudly (the undeclared field on a fieldless
  verb; the RETIRED-entry re-reference ×2 — one scene-close cause, one
  narrator-withdrawal cause), 0 honest misfires; 2 world answers
  (take_failed ×2, the pin surviving both). Combined corpus: 51
  utterances, 35/35 boundary validity — the ≥90% criterion holds on
  the combined volume (the phase-2 gate review stays the owner's).
- Corpus 6→10 cases (tests/fixtures/parse_replies.json): examine/use/
  rest fed live for the first time (the wait-720 decay batch = 16
  events inside the door's own run_steps; per-cycle state pins — use
  intoxication 20, the fatigue clamp 20−30→0); a PINNED entry dies two
  ways (the scene close, the narrator's texture-OCC withdrawal — RETIRED
  joins PROMOTED as terminal, re-reference off-grammar either way,
  fresh establish legal); the question→question→intent ladder; the
  wait-without-ticks gate-passed/door-rejected probe (PARSER_SPEC §4
  live). Corpus machinery +: the narrator-cycle note override + the
  optional per-cycle state assert (tests/test_parser.py).
- 660→664 green, ruff clean. KI#53 deleted per AGENTS §5 (closed
  iter-31, two iterations past). iter-24 evicted per the cap. Docs:
  PARSER_SPEC §7, TASKS (+ the iter-12/13/14 lingering sections
  collapsed to their Done one-liners — back under the 600 cap), STATUS,
  AGENT_NAVIGATION §1, README Status.
---
iter-32 · 2026-09-01 · parse-1 — validation beats over the say door
(iter-32-parse1-say-sessions; the phase-2 arc's first session batch)
- Six live mode-C sessions (seeds 125/42/4/23/8/41 — walkthrough,
  texture-pin-on-failed-take, texture promotion, fire chain,
  disambiguation family, malformed-probe family) driven by a runner
  outside the repo (scripts/iter32_parse_runner.py, Rule 9) through the
  REAL stack: Simulator + Mediator + ParserDoor over ONE shared ledger
  (D-049) — the narrator half establishes, the player's words
  reference; the operator IS the external parser.
- PARSER_SPEC §6 tally: 30 utterances (21 intent / 6 question / 2
  no_intent), 7/7 deliberate off-grammar probes caught loudly, 0 honest
  misfires → boundary validity 21/21 (the ≥90% criterion MET on this
  volume; the phase-2 gate review stays the owner's — the iter-24/26
  precedent); 3 door failures are world answers (take_failed joins
  intent_rejected in that family) + 1 one-path RunnerError after the
  pin.
- Findings distilled live into tests/fixtures/parse_replies.json (6
  cases, the narrator-beats family; replayed through the real doors in
  tests/test_parser.py): a PROMOTED entry is terminal (re-reference =
  off-grammar — found live: the first operator script assumed the
  candles addressable after the take; the boundary refused, the script
  was fixed, the catch became a deliberate probe); the fire cascade
  drains inside the door's own batch (5 events, last
  location_burned_out — the iter-23 batch law through the say door);
  failed takes keep live+pinned, committed takes are the promotion
  (canon birth pinned in the fixture's state asserts).
- KI#54 (the FAQ crept to 21 entries at iter-31, over the ≤20 cap)
  opened + closed: the narrate/parse session recipes merged to one
  entry. 654→660 green, ruff clean. 2 files + the doc-sync set (the
  iter-25 precedent); iter-23 evicted per the cap. Docs: PARSER_SPEC
  §7 (the corpus row lands), TASKS, STATUS, AGENT_NAVIGATION §1,
  README Status. KI#51/KI#52 deleted per AGENTS §5 (closed bg-4, two
  iterations past). TASKS 598→607 stays over the 600 cap by substance
  (the iter-22/23 precedent — the session findings carry load; the
  cruft pass ran: iter-32's own tally restatement cut, single owner
  STATUS + the fixture's source).
---
iter-31 · 2026-09-01 · phase-2 parser door — the mode-C boundary's
LLM-free half (iter-31-phase2-parser-door; the owner's start-phase-2
call — phase 1 closed at D-058, polish done iter-27–29)
- brief/parser.py (pure — no RNG, no I/O, no wall-clock): the grammar
  snapshot (pack verbs with pack-derived field constraints: ticks
  positive-int, method enum, near spot-list from the actor's folded
  position, texture live-entry reference; ∪ addressable nouns — canon
  entities + live ledger entries, ghost interactivity structurally
  impossible); parse_call (utterance + grammar + protocol,
  byte-deterministic); parse_reply_from_mapping — the closed
  {intent | question | no_intent} gate, loud ParseError on
  off-grammar output, never a feed.
- cli/parser.py ParserDoor + the `say`/`say apply` session door
  (shares the session's ONE ledger, D-049): emit (retire window +
  scene sync + document) → apply (gate against the CURRENT snapshot →
  pin → feed one step through the front door → promotions wired like
  the narrator path). The pin law: `SceneLedger.pin` — blueprint
  §1(a)'s first consumer (the reference IS the pin; a failed attempt
  keeps it live+pinned — seed-probed both ways; un-pinning does not
  exist). Attempts are facts: world-impossible intents commit
  intent_rejected.
- docs/PARSER_SPEC.md (the trigger-fired phase-2 spec: boundary,
  snapshot, documents, pin/feed, the ≥90% measurement — parse
  validity ≠ world legality) + SPECS_BACKLOG row; TASKS phase-2
  opening + the parse-1/parse-2/engine-1 backlog; STATUS
  header/FAQ/Next; AGENT_NAVIGATION §1; README Status/repo-map; D-062;
  KI#53 (phase-state doc drift: TASKS' stale phase header + the README
  Status tail) opened + closed.
- 629→654 green (+25: snapshot/call-document/gate/pin/door-e2e/CLI
  wiring), ruff clean. 7 code+spec+test files + the doc-sync set
  (the iter-12 boundary precedent); iter-22 evicted per the cap.
---
bg-4 · 2026-08-31 · cost notes — the prior-art LLM-simulation
costs (bg-4-cost-notes)
- TECH_NOTES §9 (new; single owner of the figures): Park 2023
  verified against the arXiv full text — "thousands of dollars in
  token credits" for 25 agents × 2 game days (gpt3.5-turbo,
  sequential), NO cost table; Zhao et al. 2023 (Lyfe Agents,
  Appendix F) independent estimate: conservative $2,000 → ≈$25 per
  agent per human hour at 10× game speed; Park 2024 (1,052
  participants, GPT-4o) publishes no budget — the 59-agent
  retrieval analysis alone ran 1,281,040 GPT-4o-mini queries.
  Honest reading: prior art prices the per-agent-per-step hot loop
  (N×M×L); our phase-1 bill is beat-proportional (2-call steady
  state) — reference points for the split, not a cross-over claim.
- KI#51 (ref/generative_agents.md carried a fabricated cost
  citation — "Table 2, §6.4, ~$70" never existed in the paper;
  fixed to the verified quote + the TECH_NOTES §9 link) and KI#52
  (stray 678-line pre-iter-26 TASKS.md snapshot at the repo root,
  born in the iter-27 squash commit, over cap, unreferenced —
  deleted) opened + closed. Doc-only iteration: streak 1 of 2 (the
  alarm fires at 2; the next iteration must carry code or a fresh
  owner directive).
- 629 green, ruff clean (no code touched). 5 files (TECH_NOTES §3
  pointer + §9, the ref fix, TASKS/STATUS sync, worklog; + root
  TASKS.md deleted); iter-21 evicted per the cap.
---
iter-30 · 2026-08-31 · perf-1 — the 10k-tick timing profile
(iter-30-perf1-profile)
- scripts/profile_harness.py: day1_full's story steps + grid-aligned
  360-tick waits to the tick target; clean + cProfile double-run with
  a same-process byte-compare (held at 10k ticks — a T1-family probe,
  not a cross-environment claim); read-side timings
  (read_log/fold/metrics/chronicle) over the finished log; outputs to
  output/perf_*.txt (gitignored runtime artifact).
- Numbers (owner TECH_NOTES §8): 10k ticks ≈ 0.01–0.02 s write-side
  (~9.8k events/s), read side ≈ 0.017 s; cost is event-linear (quiet
  ticks near-free), schema validation the per-event hot spot (~24
  validate calls/event); "seconds, not minutes" met with ~3 orders of
  margin — no structural work warranted at v0.1 scale. 43% of the
  7-day stream is status_decayed (the T7 noise floor in raw counts).
- 629 green, ruff clean (count unchanged — the balance_harness
  no-test precedent; the architecture closure test guards the import).
  6 files (script + the doc sync set); iter-20 evicted per the cap.
  Docs: TECH_NOTES §8, TASKS, STATUS, AGENT_NAVIGATION §1.
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
- (deleted at bg-2 per the one-in/one-out cap; history in git.)
---
iter-24 · 2026-08-31 · validation beats — session 9, the day-2
return under burned-yard knowledge (iter-24-validation-beats-9)
- (deleted at iter-33 per the one-in/one-out cap; history in git.)
---
iter-23 · 2026-08-31 · validation beats — session 8, the
arson-after-theft chain (iter-23-validation-beats-8)
- (deleted at iter-32 per the one-in/one-out cap; history in git.)
---
iter-22 · 2026-08-31 · validation beats — session 7, the theft half
under the presence machinery (iter-22-validation-beats-7)
- (deleted at iter-31 per the one-in/one-out cap; history in git.)
---
iter-21 · 2026-08-31 · validation beats — session 6, the alarm cascade
(iter-21-validation-beats-6)
- (deleted at bg-4 per the one-in/one-out cap; history in git.)
---
iter-20 · 2026-08-30 · universality pass — the transition + scene-line
vocabularies become pack data (iter-20-universality, KI#48 + D-057)
- (deleted at iter-30 per the one-in/one-out cap; history in git.)
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
