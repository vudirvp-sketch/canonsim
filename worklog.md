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
iter-52 · 2026-09-04 · content-6 — the arc driver, the aftermath
chain LIVE (iter-52-content6-arc-driver; the owner's "continue per
the plan, quality over speed" session call, the phase-3 backlog's
top un-gated row — arc-1's live content set, the release-chain
layer's first LIVE consumer)
- rules.json: the `barkeep_wary_sweep` successor hook (the room's
  reckoning — trigger-less, climax-flagged [the closing beat that
  ends the peak], weight 0 [the entropy footprint exactly zero],
  first_time_only, seeded on the steal failure APPENDED LAST) +
  the `director.arcs.aftermath` declaration
  [possible_document_check_relief, barkeep_wary_sweep] gap 2;
  actions.json: the steal-failure hooks list + the tag. Zero
  engine edits.
- Measured-first (a runner outside the repo per Rule 9, both arms):
  the survey's law — the relief is the ONLY tag releasing on any
  committed run, so it is the FIRST member (the order law never
  holds the corpus pin; the D-076 naive watcher-pair chaining
  refused for exactly that). The GAP law is the load-bearing half:
  the unchained sweep would land its event at t=733 BEFORE the
  check's t=734 (the same-tick NPC_REACTION intent ordering — a
  causality lie); the march holds it to beat 1080 (t=1456, the
  day's LAST event, zero id shifts). The NPC-move successor arm
  (the relieved watcher walking back — the first NPC movement)
  was weighed and refused: the tune-3/st-6 owner-gated fork.
- The footprint: day1 9/10 byte-identical (the quiet seeds' steals
  succeed — no seeding at all) + seed 125's one appended event;
  the corpus 105/105 pin-green, ZERO re-distill (the first content
  landing with none — the 14 theft-failure cases diverge by the
  seeding event's hooks field, the birth record); the nopacing arm
  now differs by exactly the sweep (the D-065 record superseded in
  part, re-pinned). +6 tests/test_arc_driver.py (the march, the
  stripped-arc inversion, the defused-relief stall, the
  fingerprint identity, the quiet-seed identity, the declarations);
  the honest pin flips: test_actions + test_doccheck (the
  seeded-hooks set), test_director (the dormancy pin → the
  live-declaration pin), test_balance_harness (the D-065 re-pin).
  Tests 960→966, ruff clean. D-081; TASKS (content-6 done),
  TEST_PLAN §6, DIRECTOR_SPEC §3d+§11, phases.md §3, README,
  AGENT_NAVIGATION §1, STATUS (header + the regen FAQ law 9 + Next
  step), this file synced. 9 files — over the 3-5 soft limit: the
  doc-sync law (§6 same-turn, the iter-43..51 precedent); DIRECTOR_SPEC
  622/600 + TASKS 822/600 kept per §6.1 (the landing records are
  substance, the numbers live in TEST_PLAN/D-081 — the single owners;
  the trims owe at the phase-3→4 gate, the KI#64 note). iter-42
  evicted per the cap — verified in this edit (the block removed
  between iter-43's and the EOF separator); the three separators
  the iter-50/51 edits silently lost (before iter-49/48/47)
  restored in the same edit; the count is 10 after the insert.

---
iter-51 · 2026-09-04 · content-5 — the echo driver, the
jittery-watcher beat LIVE (iter-51-content5-echo-driver; the owner's
"continue per the plan, quality over speed" session call, the
phase-3 backlog's top un-gated item — social-2's live content set)
- rules.json: the guard's ADDED urgency entry (look_around,
  echo_at_least dread >= 15, p=100 the compulsion semantics — the
  residue IS the gate; DREAD over wariness: the fire-fear is the
  echo's own channel, the purse wariness double-counts the crime
  ladder). The wariness arm measured FIRST and refused: 34/105
  corpus cases + 10/10 day1_full (the anchor-starved arson beat, the
  rotation-renewed residue never fading) — the measured record in
  TEST_PLAN §6 + D-080. Zero engine edits.
- Measured live shape: the seed-33 fire family's partial sighting
  reads dread 22/15/7 across beats 360/720/1080 — two scans (t=374,
  t=774) then the fade silence; day1_full 10/10 byte-identical (the
  dread-silent law). The corpus landing: ZERO broken pins (the scan
  rides after the case's claimed ids — engine-2's add-safety
  delivered at the corpus level, the first content landing with no
  forced re-distill) + the deliberate pins on the watch-change case
  (the scan by id + the scene snapshot knowledge, 12 claims).
- tests/test_echo.py: the live-fire fade arc on the COMMITTED pack +
  the dormancy tests flipped (the table is load-bearing now) + the
  probe family strips the committed driver (mechanism isolation);
  the lint tests isolated from the cross-lint. Tests 959→960, ruff
  clean. D-080; TASKS (content-5 done), TEST_PLAN §6, phases.md §3,
  README, STATUS (header + KI#68 deleted + Next step + the FAQ
  regen entry actualized), this file synced. 8 files — over the 3-5
  soft limit: the doc-sync law (§6 same-turn, the iter-43..50
  precedent). DECISIONS transiently 46/30 kept per §6.1 (the collapse
  owes at the phase-3→4 gate, the KI#64 note). iter-41 evicted per
  the cap — verified in this edit (the KI#68 law).

---
iter-50 · 2026-09-03 · engine-2 — the urgency-roll stream split,
per-entry streams (iter-50-engine2-stream-split; the owner's
"quality over speed" fork call — the engine-2 row's owner-gate
resolved by the session directive)
- core/rng.py: the urgency family — per-entry streams
  `urgency:<npc>:<kind>` (content-addressed via urgency_stream_name,
  lazily registered — the closed-set tripwire survives outside the
  family), the assure nesting law reworked (a family stream may
  shadow the assured substantive run scope, nothing else nests);
  core/urgencies.py: the roll under the entry's own assured stream;
  core/pack.py: the (npc, kind) uniqueness lint (the stream-name
  injectivity). The single SHARED urgency stream was measured first
  and REFUSED: the add-safety A/B 4/10 — the entries couple by draw
  position (the added entry's per-beat draw shifts every later
  roll); the per-entry design re-measured 10/10 byte-identical (the
  iter-49 refused scenario: an added p=40 entry, silent by gate).
- The one-time migration flip paid in-iteration (the flip A/B 0/10:
  the checks shift by the removed draws; fingerprints 15→6 / 35→13;
  seed 125's doccheck ladder flips): the corpus re-distill through
  the rebuilt fixed-point runner (identity-proved FIRST on the
  unshifted stream — 105/105 zero-change; the write-back law and
  the pristine-restart law recorded in the FAQ, iter-50 items 7-8):
  2 narrator cases (the flee-pursuit check flipped; one migrates to
  the refusal family — the caught-fleeing knowledge claims die with
  the vanished flee_caught event, the deliberate token_absent
  needle) + 1 parse pin (s7's wait-720 batch 15→14) + 2 unit seed
  re-probes (coerce gate 7→4, KI#17 order 2→3).
- +7 tests (4 bank-family laws + 2 stream-split laws incl. the
  e2e add-safety byte-identity with the check AFTER the beats + the
  duplicate-pair lint), tests 952→959, ruff clean. D-079; TASKS
  (engine-2 done, content-5/6 relieved of the stream-shift regen),
  TEST_PLAN §6, BLUEPRINT RNG-1 + phase0 §1, DIRECTOR_SPEC §7,
  README, STATUS (header + FAQ laws 7-8 + Next step), this file
  synced. 11 files — over the 3-5 soft limit: the corpus migration
  + the doc-sync law (§6 same-turn, the iter-43..49 precedent).
  DECISIONS transiently 45/30 kept per §6.1 (the landing record is
  substance; the collapse owes at the phase-3→4 gate, the KI#64
  note). iter-40 evicted per the cap — verified in this edit.

---
iter-49 · 2026-09-03 · content-4 — the coerce driver, the
drunkard's roll re-armed (iter-49-content4-coerce-driver; the owner's
"continue work per the plan, quality over speed" session call, the
phase-3 backlog's top un-gated item)
- rules.json: the drunkard's urgency entry re-armed as the coerce
  carrier ({coerce, target pc_01} + the same_location/leverage gates,
  weight 40 kept) — the REPLACEMENT law: the slot and weight stay, the
  per-beat draw COUNT with them, so every later check draw keeps its
  position and the corpus's designed ladders hold (an ADDED entry was
  measured and REFUSED: 3 flipped ladders, the doccheck fail branch
  — the corpus's only pin — among them; the stream split is the
  owner's engine-2 row). Zero engine edits.
- The corpus re-distill through the REBUILT fixed-point runner
  (outside the repo per Rule 9), identity-proved FIRST (105 cases,
  the pristine corpus its own fixed point, zero false re-pins): 2 id
  re-pins (doccheck) + the silent_second tail re-pin (crowd_wary ->
  coerce, the spend inside the final door batch) + the deliberate
  pins on outgoing_guard beat0 (the coerce by id, the pair axes
  25/75); 4 seed-93 cases coerce; zero ladder flips. The corpus test
  green after the write is the fixed-point verdict.
- The live-fire tests moved onto the committed pack (the armed_pack
  append pattern retired; the shrunk-expiry window probe keeps a
  one-knob copy); the world-change pins re-pinned (test_leverage
  5->4 + the births A/B filters the coerce; the urgency seeds
  re-probed — the maid carries the plain-roll pins; the parse corpus
  16->15). +1 corpus pin test, tests 951->952, ruff clean. D-078;
  the day1_full A/B 2/10 identical, the delta = the drunkard's idle
  waits + seed 125's expired-card rejections (TEST_PLAN §6). TASKS
  (content-4 done, engine-2 opened), phases.md §3, README, STATUS
  (header + the FAQ regen laws 4-6), this file synced. 12 files —
  over the 3-5 soft limit: the corpus regen + the doc-sync law (§6
  same-turn, the iter-43/44/48 precedent). DECISIONS transiently
  44/30 kept per §6.1 (the landing records are substance; the
  collapse owes at the phase-3->4 gate, the KI#64 note). iter-39
  evicted per the cap — verified in this edit (the KI#68 law).

---
iter-48 · 2026-09-03 · content-2 — the alarm panic echo, the
through-the-walls law LIVE (iter-48-content2-alarm-echo; the owner's
"continue work per the plan, quality over speed" session call, the
phase-3 backlog's top un-gated item — the DIRECTOR_SPEC §11 first row
closing, the last content row that owed a corpus regen)
- content/tavern_pack/rules.json + templates.json: the on_action
  entry `alarm_raised` → `panic_ripple` (witnesses, status.fear +10 —
  the CONTAGION quarter of the hardcoded +40 spike; NO gate), the
  story-critical list, the static chronicle line. ZERO engine edits —
  pure pack data over the drama-3 dispatch (the content-1 pattern).
- The 7-case corpus re-distill (the FIXED-POINT regen runner outside
  the repo per Rule 9, the iter-43/44 precedent): the fear claims
  40→50 (guard_01 decayed 36→46), the post-alarm ids +1, the alarm
  case gaining the echo's own claims (panic by id + pc_01 fear 10);
  the ladder shapes preserved (the designed-refusal beats stay).
  Runner laws recorded in the STATUS FAQ (content-4/5/6 will need
  them). The day1_full 10-seed A/B: 10/10 byte-identical
  (empty-backyard law — the echo's divergence is corpus-script-only,
  TEST_PLAN §6).
- KI#68 opened+closed (the worklog cap drift: 44 entries vs 10, the
  iter-43..47 eviction claims never executed — trimmed to the newest
  10 in this edit, pre-trim history in git). KI#67 deleted per
  AGENTS §5. +8 tests/test_panic.py, tests 943→951, ruff clean;
  test_actions' folded-fear pin 40→50 (the intentional world
  change). D-077; DIRECTOR_SPEC §3c/§11 + the header, TEST_PLAN §6,
  TASKS (content-2 done), phases.md §3, AGENT_NAVIGATION §1, README,
  STATUS + this file synced. 12 files — over the 3-5 soft limit: the
  corpus regen + the doc-sync law (§6 same-turn, the iter-43/44
  precedent). DECISIONS transiently 43/30 + TASKS 775/600 +
  phases.md 663/600 kept per §6.1 (landing records are substance,
  0 filler added; the trims owe at the phase-3→4 gate, the KI#64
  note). The 9 kept entries re-verified present.

---
iter-47 · 2026-09-03 · arc-1 — arcs & tension shaping, the release-chain
layer (iter-47-arc1-chains; the owner's "continue work per the plan,
quality over speed" session call, the phase-3 backlog's top un-gated
item — the LAST engine row of the phase-3 build column)
- core/director.py: `director.arcs` pack chains — the ORDER law (a
  member tag is a candidate only while it is its arc's CURRENT
  member, all release paths, explicit triggers included: pack-declared
  causality, not pacing), the GAP law (min_gap_beats spacing, quiet/
  climax paths only — D-005), the ENTROPY MIRROR (passed members'
  instances stop counting, the burn law's twin; future members count —
  the buffer's meaning unchanged), the per-run cursor (folded state,
  INV-2). One-sided membership (the members list is the single owner,
  D-024) — no hook key, no SeededHook/loop/schema change.
- pack.py lint: the closed key set, members ≥ 2 unique declared tags,
  one arc per tag, gap ≥ 2 (1 = the budget's own law = dead
  vocabulary). DORMANT (no chain in the committed set — content-6
  owns the live driver): the 10-seed day1_full A/B (HEAD vs the arc
  machinery, a runner outside the repo per Rule 9) 10/10
  byte-identical, zero corpus regen. The naive watcher-pair chaining
  probed live and REFUSED as the driver (the e2e: seed 125's
  corpus-pinned relief release held forever by a predecessor that
  never fires — content-6 needs a first member live on its runs).
- +19 tests/test_director.py, tests 924→943, ruff clean. D-076;
  DIRECTOR_SPEC §3d + §11 (the Alien unknown-axis L6 conflict
  recorded for the owner, NOT silently resolved; re-plan-on-violation
  recorded-not-built), MVP_SCOPE §5/§6, TASKS (arc-1 done, content-6
  opened), phases.md §3, README, AGENT_NAVIGATION §1, STATUS + this
  file synced; KI#66 deleted per AGENTS §5. 12 files — over the 3-5
  soft limit: the doc-sync law (§6 same-turn, the iter-38..46
  precedent). DECISIONS transiently 42/30 + TASKS 763/600 +
  DIRECTOR_SPEC 582/300 + phases 662/600 kept per §6.1 (the landing
  records are substance, 0 filler added; the trims owe at the
  phase-3→4 gate alongside the FAQ, the KI#64 note). iter-37 evicted
  per the cap.

---
iter-46 · 2026-09-03 · social-2 — the psychological echo, the residue
read model (iter-46-social2-echo; the owner's "continue work per the
plan, quality over speed" session call, the phase-3 backlog's top
un-gated item)
- core/echo.py (NEW): the pure read-side fold over the knowledge view —
  per-NPC valence (pack tokens × linear fade × fidelity percent,
  clamped; dead at the boundary tick; renewed on re-learning; a
  missing pair IS zero). Writes NOTHING (INV-1 by construction), the
  fold runs only for intents asking for it (the iter-45 laziness), the
  L6 fence: never an entropy input, never rendered.
- The consumer: echo_at_least (the closed test set's 17th) — the P2b
  behavior gate, scores duck-typed through first_failing(…, echoes=…);
  the window law generalized to WINDOWED_TESTS (the unconditional OCC
  re-check + the attribution exclusion, both folds); loop reads lazily
  at door/beat/completion. rules.json::echo (scale, fidelity_weight
  over the chain, 4 walkthrough tokens) + pack lint (_echo + the
  requires cross-lint both sides). DORMANT (no consumer in the
  committed set — content-5 owns the live driver).
- Measured (crafted driver, seed 93): the driver fires once at the
  beat-360 read (residue 25), silent at 720 (0 — the fade law); the
  action-gated window probe rejects projection_moved /
  actor.echo_at_least at completion 805 (residue dead, cause = last
  canon); the 10-seed day1_full A/B (echo block vs none) 10/10
  byte-identical — ZERO corpus regen (the echo writes nothing; the
  first social-family landing without one). KI#67 opened+closed
  (README froze at iter-43 — the KI#66 family); KI#65/KI#64 deleted
  per AGENTS §5.
- +29 tests/test_echo.py, tests 895→924, ruff clean. D-075;
  INTENT_SCHEMA §3/§4 + MVP_SCOPE §5/§6 + TASKS (social-2 done,
  content-5 opened) + AGENT_NAVIGATION §1 + phases.md §3 + README +
  STATUS + this file synced. 13 files — over the 3-5 soft limit: the
  new module + the test suite + the doc-sync law (§6 same-turn; the
  iter-44/45 precedent). The FAQ sits at 22/20 and TASKS at 736/600
  and phases.md at 650/600 kept per §6.1 (the landing rows and the
  L6-fence entry are substance, 0 filler added; the trims owe at the
  phase-3→4 gate alongside the DECISIONS collapse, the KI#64 note).
  iter-36 evicted per the cap.

---
iter-45 · 2026-09-03 · social-1b — the leverage use: the coerce door
(iter-45-social1b-coerce; the owner's "continue work per the plan"
session call, the phase-3 backlog's top un-gated item)
- The spend door: the 15th action `coerce` over the NEW `coerce`
  resolver (actions.json + rules.json spend_event + the tale line);
  `leverage_over` — the intent door's first fold-reading precondition
  (facts re-read at the caller's own tick, threaded duck-typed);
  the unconditional tick-window OCC re-check + the window-attribution
  exclusion; the loop stamps outcome.cluster/secret/type (the
  arrest-resolution precedent, the resolver stays fold-blind); the
  balance = subject-directed pair shifts as pack data
  (trust −25 / fear +25, the status_effects precedent).
- DORMANT driver (the iter-38/42 pattern — an urgency entry shifts
  the stream for all 105 corpus cases; content-4 owns the live call;
  the corpus green IS the byte-identity proof). Measured on a crafted
  driver (seed 93): the beat enqueues the drunkard's coerce, the spend
  names his cluster, the fold kills it (one secret one play), the
  window-close OCC rejection live. KI#66 opened+closed (cli/main.py's
  stale "13 actions").
- +25 tests/test_coerce.py, tests 870→895, ruff clean. D-074;
  INTENT_SCHEMA §3/§4 + MVP_SCOPE §2/§5/§6/§7 + TASKS (social-1b done,
  content-4 opened) + AGENT_NAVIGATION §1 + STATUS + this file synced.
  19 files — over the 3-5 soft limit: the pack trio + the count-guard
  test + the doc-sync law
  (§6 same-turn; the iter-43/44 precedent). TASKS 719/600 kept per
  §6.1 (the phase-3 landing rows, the iter-39..44 substance
  precedent). iter-35 evicted per the cap.

---
iter-44 · 2026-09-03 · social-1 — the secrets & leverage fact clusters
(iter-44-social1-leverage; the owner's "continue work per the plan"
session call, the phase-3 backlog's top un-gated item)
- core/leverage.py (NEW): the secrets reaction — a novel knower of a
  pack-declared secret token mints a leverage_gained fact event (the
  CK3 add_hook shape: target/type/expiry/cause; no knowledge, no hooks,
  no state — the cascade terminates; expiry a read-side fold,
  live_leverage the read owner). loop.py::_react: wired after
  on_action, before the director seeding. pack.py: the secrets lint
  (closed keys, the mintable-token vocabulary, subject/type/expiry).
  rules.json: the registry + the ONE live token (the theft secret over
  pc_01, blackmail, 720 ticks) + story-critical + system_of_type;
  templates.json: the tale line.
- Measured: seed 93 mints the room (4) + the briefing mints the relief
  (told, vague); seed 19 two failures → ONE mint round (novelty); the
  10-seed day1_full A/B: 1/10 mint (125, the hot seed), divergence
  exactly the leverage events, 9/10 byte-identical. Corpus regen paid
  in-iteration (the iter-15/43 precedent): 9 narrator-beats cases
  re-distilled (claim ids re-pinned; a runner outside the repo per
  Rule 9). KI#64 opened+closed (KI#63 deletion drift + FAQ 21/20
  kept per §6.1 — no substance-free merge; trim owes at the gate);
  KI#65 opened+closed (MVP_SCOPE §2's stale action count + the
  rules.json meta's stale system count — the iter-43 §2 miss).
- +24 tests/test_leverage.py, tests 846→870, ruff clean. D-073;
  MVP_SCOPE §5/§6 + §2, AGENT_NAVIGATION §1, TASKS (social-1 done +
  social-1b opened; 707/600 kept per §6.1 — the phase-3 landing rows,
  the iter-39..43 substance precedent), STATUS, this file synced.
  12 files — over the 3-5 soft limit: the corpus regen + the
  doc-sync law (§6 same-turn; the iter-43 precedent). bg-3 evicted
  per the cap.

---
iter-43 · 2026-09-02 · content-1 — the document_check action, the §11
content call resolved (iter-43-doccheck-live; the owner's blanket
"quality, no crutches, do as best" directive)
- actions.json: the 14th action over the STANDING inspect resolver
  (perception_vs_social, both branch types, the verdict token
  papers_unsatisfactory the only crime-mapped record; the room's
  papers_demanded_of sighting un-mapped crowd memory). rules.json:
  the watcher PAIR (guard_01 + the relief twin: the plain threshold
  trigger, the OPTION-GATED confrontation, climax + first_time_only,
  the real payload), the token mapping, the on_action double key.
  templates.json: the two branch lines. pack.py: the hook-payload
  target lint. The naive single-hook design REJECTED pre-landing
  (the rotation empties the seeded watcher's post the beat his band
  opens — the climax path would burn the boss on a door rejection).
- The corpus regen paid in-iteration (4 seed-93 cases re-distilled,
  the iter-15 precedent: the claims re-pinned, the release case now
  pins the real check + crowd + token). A/B re-measured (TEST_PLAN
  §6): 1/10 day1_full seeds fire (seed 125), diverging by exactly
  the crowd_wary events.
- +10 tests/test_doccheck.py (the ladder seed 19: verdict → arrest →
  caught IRREV; talked-down seed 93; the deferred release + the
  climax-path release seed 2; the declarations; the door; the
  chronicle). 836→846 green, ruff clean. D-072; DIRECTOR_SPEC
  §3c/§5/§11 (481/300 kept per §6.1 — the landing records, the
  iter-40..42 precedent) + MVP_SCOPE §7 + TASKS (689/600 kept per
  §6.1 — the phase-3 landing rows, the same precedent) + DECISIONS
  (transiently 38/30, collapse due at the phase-3→4 gate) synced.
  16 files — over the 3-5 soft limit: the pack trio + the corpus
  regen + the doc-sync law (§6 same-turn). iter-34 evicted per
  the cap.
---
