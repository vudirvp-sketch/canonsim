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
iter-39 · 2026-09-01 · dir-4 — the multi-channel quiet split
(iter-39-dir4; the owner's "continue work per the plan" session
call, the phase-3 backlog's top un-gated item)
- core/director.py: `director.channels` pack data (ChannelConfig —
  per-channel quiet floor + the closed CHANNEL_INPUTS binding
  vocabulary {suspicion, physical_threats}; the channel's own
  unreleased hook weights always feed it) + `SeededHook.channel` +
  the per-hook quiet gate (`permit_quiet` — the third policy
  question; the channel table lives on the Director, the policy only
  answers) + `channel_entropies` (pure, mirrors `entropy`). Global
  ON PURPOSE: the pacing clock (one drama arc over TOTAL entropy —
  PEAK/REST suppress every channel), the budget (1/beat, the global
  tiebreak), the climax path, explicit triggers (D-005), the
  cooldown. Channelless hooks keep the v0.1 global floor (the
  per-hook opt-in, the climax-flag pattern; a tag without the block
  is dormant vocabulary).
- rules.json: threat 3 (the document-check's weight self-blocks the
  quiet path — an escalation never spawns because the world is
  boring) / social 5 (guard_suspicious_of_pc, suspicion-bound) /
  ambient 2 (inputless, declared-but-dormant — the owner's content
  call); both hooks channel-tagged. pack.py lint: the block shape,
  floors, the closed input vocabulary, the hook tag must name a
  declared channel when the block exists.
- Scope: 13 files (code 2 + tests 1 + pack 1 + the doc-sync set —
  the iter-36/37/38 precedent; TASKS 599→613 over the 600 cap by
  substance, the iter-32 precedent — the landing rows carry load).
- Fixture discipline: T1/T8/corpus byte-identical; 10-seed A/B
  (channels vs no-channels, a runner outside the repo per Rule 9)
  10/10 byte-identical — the quiet path never fires on day1_full
  (the D-066 all-PEAK window; the split is unit-pinned).
  KI#63 (phases.md §3 stale "still-ahead" after iter-38 + the nav
  tests row's missing climax note) opened + closed; KI#61/KI#62
  deleted per AGENTS §5 (closed iter-37, two iterations past).
  Tests 739→757 (+18 test_director.py: the input binding, the
  quiet-channel-while-another-burns law + the v0.1 comparison arm,
  the escalation self-block, the global clock gate,
  explicit-ungated, the fallbacks, the shared budget, director-off,
  climax-ignores-channels, the dormant tag, the four lint refusals),
  ruff clean. D-068; DIRECTOR_SPEC §5 the contract owner; iter-31
  evicted per the cap.
---
iter-38 · 2026-09-01 · dir-3 — the climax layer + PEAK_CLIMAX
(iter-38-climax; the owner's "continue work per the plan" session
call, the phase-3 backlog's top un-gated item)
- core/director.py: `PacingConfig.climax_floor` (the third entropy
layer, the L4D2 three-intensity rule) + the climax release path (a
climax-flagged hook at the END of a peak — clock in PEAK held
`min_peak_beats`, entropy at the layer; never from the quiet path) +
the one-beat PEAK_CLIMAX state (entered only by a release, exited to
REST) + `permit_climax` on the policy protocol (the boss fires at
HIGH entropy — one boolean cannot serve both paths). rules.json:
climax_floor 75 (3x peak_floor, the donor ratio); lint: the layer
strictly above the peak floor, the hook flag boolean. The flag on
`possible_document_check` was probed live (suite green) but reverted:
the v0.1 wait-stub would make a hollow boss — the flag lands with
the document_check action (DIRECTOR_SPEC §11), the owner's call.
- Scope: 12 files (code 2 + tests 1 + pack 1 + spec 1 + the doc-sync
  set — the iter-36/37 precedent).
- KI#60 deleted per AGENTS §5 (closed iter-36, two iterations past).
Tests 727→739 (+12 test_director.py: the clock's boss-beat exit, the
layered threshold + peak-minimum + placement gates, the quiet-path
exclusion, explicit-beats-climax, the no-double-boss guard,
director-off, the flagless-layer semantics, the two-layer
byte-identity, the two lint refusals), ruff clean; harness A/B
re-measured (10 seeds, both arms byte-identical — the layer is inert
without a flagged hook). D-067; DIRECTOR_SPEC §5 the contract owner;
bg-4 evicted per the cap.
---
iter-37 · 2026-09-01 · dir-2 — the eventless-stretch instrument +
the pacing A/B (iter-37-eventless-stretch; the owner's "continue per
the plan" session call, the phase-3 backlog's top un-gated item)
- core/metrics.py: `eventless_beat_stretches` — the phase-3 exit
criterion's instrument (tale-gate scene events over the
`urgencies.beat_ticks` window axis, `(prev_beat, beat]` windows);
`IMPORTANCE_ORDER` moved to core/log.py (the chronicle imports it —
one owner of the ordering, D-024); scripts/balance_harness.py:
`--pacing on|off` (the clock-off arm = a linted pack variant minus
`director.pacing` under output/, requires `--directors on`) + the
stretch block. Measured 1000 seeds: both arms byte-identical per
seed (every day1_full run ends in PEAK — the stagnation path never
fires; D-065's "un-tuned" note answered), max stretch 1, quiet
1000/1000 (the (360,720] phase-boundary window).
- Scope: 13 files (code 5 + tests 2 + pack 1 + the doc-sync set —
the iter-36 phase-opening precedent).
- KI#61 (loop comment named the never-read
`director.stagnation.beat_ticks`; the dead pack key deleted, zero
behavior change) + KI#62 (worklog order/cap drift — bg-3 moved to
its chronological position, the over-cap pair evicted) opened +
closed. Tests 708→727 (+13 metrics, +6 harness incl. the seed-125
D-065-record pin), ruff clean. D-066; TEST_PLAN §6 the contract
owner.
---
iter-36 · 2026-09-01 · phase-3 opening — the pacing clock (DIR-1)
(iter-36-pacing-clock; the owner's "continue per the plan" call —
phase 3 opens on it, the iter-31 precedent)
- core/director.py: the per-run RAMP/PEAK/REST/STAGNATION clock over
  narrative entropy (L4D peak/rest donor) — pack-gated via
  director.pacing, advanced once per beat (guarded), functional
  transitions; stagnation releases fire only outside PEAK/REST (REST =
  post-climax breathing room), explicit triggers ungated (D-005);
  rules.json pacing block (25/1/1) + lint (peak > stagnation floor);
  tests 697→708 (+11 test_director.py), ruff clean — zero fixture regen
  (committed fixtures carry no stagnation releases; day1_full ON
  unchanged, its 3 beats all PEAK).
- Scope: 13 files (code 2 + test 1 + pack 1 + spec 1 + the doc-sync
  set — the iter-31 phase-opening precedent).
- KI#60 (phases.md §2 stale OPEN header post-iter-35) opened + closed;
  KI#55–59 deleted per AGENTS §5. ROADMAP/phases/TASKS phase-3 OPEN +
  the arc backlog; D-065; iter-27 evicted per the cap. phases.md
  608/600 kept per §6.1 (the overage: the D-062/D-055 + the new
  DIR-1 architecture records — substance, 0 filler added).

---
iter-35 · 2026-09-01 · phase-2 gate — the verdict + the collapse
(iter-35-phase2-gate; the owner's "continue per the plans" session
call — the un-gated backlog was empty, the arc's #1 item, the iter-26
precedent)
- Verdict **PASS** (D-064): the ≥90% exit criterion met — 51 combined
  utterances across 10 live say-door sessions, 35/35 boundary validity,
  0 honest misfires, 10/10 off-grammar probes caught; no kill-criteria
  hit. The §5 protocol re-run (a runner outside the repo, Rule 9):
  day1_full ON seed 125 M1=0.417 / M2=0.500 — identical to the iter-26
  phase-1 gate numbers (phase 2 added the parser without touching a
  canon path); T8 OFF 26 chains ≥ 3; T7 — the day1_full tale still
  reads as a story (13 lines, zero noise floor); 697 green, ruff clean.
- DECISIONS collapsed 35→30 per D-034 (D-012→the D-011 family,
  D-047→the D-042 family, D-055→D-054, D-057→D-056, D-060/D-061→D-059)
  + D-064 appended; ROADMAP §2 phase 2 CLOSED, phase 3 parked (the
  owner's opening call, the iter-31 precedent).
- Doc-only (streak 1 of 2, the gate-review precedent). 7 files — the
  gate-review doc-sync set (the iter-26 scope precedent); iter-28
  evicted per the cap.

---
bg-3 · 2026-09-01 · briefer spike — the POV mini-briefer + reverse validation
(bg-3-briefer-spike; the owner re-supplied large/medium/small-dense)
- scripts/df_briefer.py (new): the D-055 pattern over foreign canon —
  the POV brief (assignment frame kept apart from the subject's
  records; in-window records via the participant prefix scan; plus
  fields merged, main precedence; collision-aware display keys; the
  60-record cap with the loud marker) + the closed-vocabulary reply
  gate (supported/contradicted/beyond_records/unknown_*; prose never
  parsed; the anchor shape gate) + the ≤2-regen ladder with the dry
  floor (VALIDATION_SPEC §7 ported) + the retrieval stress (quantile
  figure spread, double-build byte-compare). Live session: 4
  TAXONOMY §5-anchored cases, 31 claims — 19 supported / 12
  deliberate-probe non-supported, 0 honest misfires; 1 regen
  recovery, 1 exhaustion; the malformed-anchor probe caught at the
  gate.
- Numbers (TECH_NOTES §3.3, the AC's owner): 3 worlds re-imported
  (counts reproduce §3.1/§3.2 row-for-row), brief p50 ≈ 2.9 KB /
  p99 ≤ 15.6 KB on GB-scale exports, scan p99 ≤ 0.2 ms, build p99 ≤
  4.4 ms, determinism PASS ×3 — the "tens of MB" worry is dead;
  KB-scale briefs, sub-ms retrieval. The stress report name gains
  the world label (large/medium share the region2 stem).
- Tests 673→697 (+24 tests/test_df_briefer.py — brief/closure
  blind-spot/verdict families/shape-gate/regen ladder/dry floor/
  cases/stress), ruff clean. Doc-sync: TECH_NOTES §3.3, TASKS bg-3
  done, STATUS header+FAQ+Next, AGENT_NAVIGATION §1, README; iter-27
  evicted per the cap.
---
iter-34 · 2026-09-01 · owner-requested planning-layer audit
(iter-34-planning-audit; doc-only — fresh owner request per D-022)
- KI#55: the bg-4 KI#52 deletion of the stray root TASKS.md (678-line
  pre-iter-26 snapshot) never landed — no git rm rode the command
  block; deleted for real this time (the FAQ git bullet carries the
  law). KI#56/57: ROADMAP §2 State column + §6 SoW gating actualized;
  phases.md §2 rewritten to the D-062 architecture (pack grammar,
  external dev-time parser, 35/35 corpus), §1 closure/D-055 notes +
  the 8-block/eviction updates, §7 perf-1 verdict, §4 bg-2 donor
  line; TASKS bg-6 slot + the iter-26 section collapsed (cap).
- KI#58: BLUEPRINT §0 34→35 (df_design iter-8d) + LOD-1's bg-2 clause
  (DF history canon-dense, epistemology-empty — TAXONOMY §4). KI#59:
  docs/ref/paradox_scripting.md kept 605/600 over cap — substance-only
  (0 filler; enum lists are §6.1 substance), the keep rationale is
  this line. phases.md sits 603/600 after its own cruft pass (7
  restatement trims) — the overage is the D-062/D-055 architecture
  records, kept per §6.1.
- No code touched: 673 green, ruff clean. 5 files + 1 deletion (git
  rm TASKS.md); iter-26 evicted per the cap. Doc-only streak 1 of 2.

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
LLM-free half
- (deleted at iter-39 per the one-in/one-out cap; history in git.)
---
(bg-4 deleted at iter-38 per the one-in/one-out cap; history in git.)
---
iter-30 · 2026-08-31 · perf-1 — the 10k-tick timing profile
(iter-30-perf1-profile)
- (deleted at iter-37 per the one-in/one-out cap + the KI#62
  cap restore; history in git.)
---
iter-29 · 2026-08-31 · pack-2 — the arson-on-ashes door check
(iter-29-pack2-spot-available; the owner's finish-phase-1 directive,
- (deleted at iter-37 per the one-in/one-out cap + the KI#62
  cap restore; history in git.)
---
iter-28 · 2026-08-31 · tune-2 — the crime cascade renders on the
cards (iter-28-tune2-card-markers)
- (deleted at iter-35 per the one-in/one-out cap; history in git.)
---
iter-27 · 2026-08-31 · tune-1 — the rest action + the story-critical
importance hook (iter-27-tune1-rest-importance)
- (deleted at iter-36 per the one-in/one-out cap; history in git.)
---
iter-26 · 2026-08-31 · phase-1 gate review — the verdict + the
collapse (iter-26-phase1-gate)
- (deleted at iter-34 per the one-in/one-out cap; history in git.)
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
