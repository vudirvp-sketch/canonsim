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
iter-106 · 2026-09-12 · resume — the session resume door, the owner's
direct call on the risk-synthesis priority list (D-139: resume is
invisible to the log)
- core: `core/cursor.py` NEW (the run-cursor artifact — envelope,
  save/load, the event_count + prefix-digest log binding);
  `core/rng.py` export_state/restore_state (worldgen excluded —
  generate_world re-derives); `core/director.py`
  export_run_state/restore_run_state + PACING_STATES (the buffer
  rebuilt exactly by seed() over the log); `core/log.py` the
  append-mode writer (same canon door, env-pin + schema-version
  laws); `core/loop.py` Simulator.resume + export_cursor + drained +
  the checkpoint fast-path; `core/queue.py` QueueKind += weather
  (the iter-98 Literal drift); `cli/main.py` --resume + the cursor
  pin after every command and at close (clean drains only)
- tests: `tests/test_resume.py` +19 — the law at splits 0/1/2/3 +
  the directors-off arm; cursor/rng/director unit refusals; CLI e2e
  + missing/stale/foreign-pack/env-pin loud refusals; the fast-path +
  the corrupt-artifact teeth. 1611+1 green, ruff clean; corpus price
  zero (no fixture regen — the armed pack's genesis rides the
  split-0 arm)
- docs: D-139; TASKS resume-1 + the iter-106 section; STATUS re-pin
  + Next step + the FAQ clause riding the scene-ledger entry; NAV §1
  (cursor entry + checkpoint/log/cli/tests rows); TEST_PLAN §7.1 the
  runtime-consumer line; README the usage block. iter-96a evicted
  here (verified in this edit, the cap 10 held). AGENTS §2.3 scope
  note: 15 files, 7 code + 8 doc — a genuine system feature, one
  coherent landing (the owner licensed splitting, quality kept it
  whole)
---
iter-105 · 2026-09-12 · cli-pack — the pinned streak-breaker (the
owner's «поехали» on the iter-104 pin): the CLI --pack flag; 7
files — 2 code + 5 doc (the two owner verdicts riding the same
call; AGENTS §2.3: the objective scope noted here)
- cli/main.py: every pack-loading command + the session take
  --pack (top-level default content/tavern_pack, the subparsers
  SUPPRESS — both flag orders honored, no default clobber); the
  loud refusal in _load (a bad path exits 1 naming it BEFORE any
  world opens; a not-a-pack dir keeps load_pack's lint refusal);
  tests/test_cli.py +3 — the explicit tavern pack byte-identical
  to the no-flag run, the refusal (batch/session/
  before-subcommand, no log born), the read-side flag
- 1592+1 green (1589+3), ruff clean; corpus price zero (periphery
  plumbing, zero draws, no fixture regen); the stoplist
  docstring's "the CLI takes the pack dir as config" claim TRUE
  (the drift dead at its root, not by deleting the claim)
- the owner verdicts recorded, one DECISIONS line each: D-137 the
  Alien L6 conflict (the OBSERVABLE-answers law, DIRECTOR_SPEC
  §11 re-pointed), D-138 the D-081 climax flag (the peak's END
  marker); DECISIONS 30→32 rows — over-cap on substance (§6.1,
  the owner's own two verdicts; the collapse owed at the phase-6
  gate, D-034)
- iter-96 evicted (verified in this edit); 10 held. Caps: STATUS
  659 / TASKS 813 / DIRECTOR_SPEC 599 / DECISIONS 62 lines (32
  rows) — TASKS over-cap on substance (§6.1), trim at the
  phase-6 gate
---
iter-104 · 2026-09-12 · fork-resolve — the owner's chat call: the
open questions and forks analyzed point-by-point, each worked into a
final COMBINED variant (the owner's stated preference — gather the
pros, neutralize the cons, no crutches); 3 files doc-only, zero
code, zero corpus price (the iter-34/103 owner-call footprint
family; AGENTS §2.3: the objective scope noted here)
- verified BEFORE working (1589+1 green, ruff clean, HEAD 13c23c4,
  Python 3.12.14 the env pin); the resolutions routed to the TASKS
  rows: roads-1's READ-PATH fork → the derived L3 read sharpened
  (the pass graph on the WorldModel, ONE shared exits read with the
  pack-wins override, place-1's invariant relocated into the pass,
  NO canon births — INV-1/L11 held, corpus price zero by
  construction); world-2's toponym question → the same
  override-else-derived law (authored wins, else the profile-minted
  render-side name via a named cosmetic stream — the dogfooding
  line held, the grammar untouched); since-1 → phase 6 (world-2's
  condensing travelers the first real consumer, the tavern surface
  too thin); cli-pack (the CLI --pack flag) PINNED iter-105 — the
  code iteration breaking the doc-only streak (now 100..104, all
  five the owner's own calls, D-022 each time)
- the two standing owner questions (DIRECTOR_SPEC §11's L6
  conflict, D-081's climax flag) NOT silently resolved — the
  combined-variant proposals delivered in chat, the owner decides;
  docs: TASKS (the cli-pack row + the three row resolutions + the
  iter-104 section), STATUS (the header re-pin + the Next step
  iter-105 pin), this file. iter-95 evicted here (verified against
  git in this edit); 10 after; re-run post-edit: 1589+1 green,
  ruff clean. Caps: STATUS 667 / TASKS 788 — over-cap held on
  ledger substance (§6.1, the iter-102/103 precedent), trim at the
  phase-6→7 gate.
---
iter-103 · 2026-09-12 · ph6-audit — the owner's chat call: the
phase-6 plan + the project audited from the height of the landed
solutions, heightened plan-detail attention (3 files doc-only, zero
code, zero corpus price — the iter-34 owner-audit footprint family;
AGENTS §2.3: the objective scope noted here)
- verified BEFORE working (1589+1 green, ruff clean, HEAD e6c95ff,
  Python 3.12.14 the env pin — the first bare-pytest probe failed on
  the 3.13 interpreter, the FAQ's `python -m pytest` law held); the
  verdict: COHERENT — world-2/res-1/roads-1 agree across TASKS /
  phases.md §6 / ROADMAP §2; the D-134/D-135 consult material mapped
  onto its landed owners (verified in code: on_action, the hooks
  buffer, the arcs, the cause tree, the cold tiers, rotations, the
  folds, the erosion family); res-1's dependencies all landed; no
  TODO/FIXME residue; the owed items already recorded (PACK_SPEC
  trigger, ref-18/ref-20 just-in-time); the two standing owner
  questions (DIRECTOR_SPEC §11's L6 conflict, D-081's climax flag)
  re-checked, unchanged
- FOUR detail findings routed to the TASKS rows (zero new KIs —
  plan-detail notes, not defects): st-5's "with phase 5" pointer
  stale post-closure (re-pointed: unowned by a phase, the first
  consumer decides); the CLI `--pack` flag absent — the stoplist
  docstring's "the CLI takes the pack dir as config" claim is drift,
  the flag never existed (git -S verified; world-2 level-1's own
  prerequisite; the stoplist self-check is tavern-tied too); the
  roads-1 exits READ-PATH fork (the exits consumers — LOD warm ring,
  the intent door's move validation, the place-1 lint — read the
  pack record today; a generated world's exits are seed-dependent,
  never static pack data: canon births + fold-reading consumers vs a
  derived L3 read, the opening designs it); the name-1 toponym
  question (the grammar is npc-only + condensation-gated; the
  province-name dogfooding line needs a world-2 design call)
- docs: TASKS (the iter-103 section + the world-2/roads-1 row
  enrichments + the st-5 re-point), STATUS (the header re-pin +
  Next step: st-4/st-5 added to the owner-gated enumeration + the
  audit verdict), this file. iter-94 evicted here (verified against
  git in this edit); 10 after. The doc-only streak surfaced per
  AGENTS §2.5 (iter-100..103, all the owner's own calls, the D-022
  exception — the next iteration should be the phase-6 opening or
  an explicit owner call). Caps: STATUS 657 / TASKS 743 — over-cap
  held on ledger substance (§6.1, the iter-102 precedent), trim at
  the phase-6→7 gate.
---
iter-102 · 2026-09-12 · gate — the phase-5 exit review, the owner's
chat call (8 files doc-only, zero code, zero corpus price — the
iter-54/65 gate footprint family; AGENTS §2.3: the objective scope
noted here)
- verified BEFORE working (1589+1 green, ruff clean, HEAD 5ecba27,
  Python 3.12.14 the env pin); the full ROADMAP §5 protocol re-run:
  the seed-125 pair ON M1=0.52/M2=0.2 (56 events — iter-98's DESIGNED
  day1_full price; the iter-65 record 0.509/0.333/61 events) / OFF
  T8 24 chains (the exit criterion ≥3 met in its worldgen-fed form —
  the ARMED committed pack); the 60-seed band 15–24, M5 p50 0.79,
  stretch max 1 (rev5's records hold); T7 the tale reads as a story —
  the worldgen genesis + world_history lines OPEN the chronicle; the
  longrun pins green; no kill-criteria hit. The verdict: PASS, D-136
  (the gate-verdict family row)
- the §5 step-6 staleness pass (D-128's adopted step, first
  execution): KEEP the rest, REWORD three discharged-phase-0 clauses
  (AGENTS §1's phase frame; INV-4's "before the phase-0 gate passes"
  → the standing boundary + the engine-1 owner gate; §8's guard the
  same), DROP none; D-129's effect-line habit UNEXERCISED — zero
  protocol-law rows since D-128, reported out loud per its own
  consequence line; D-128's own effect lines checked (mech-2 the one
  still open, rides the next mechanics.py touch); the FAQ chain
  baseline synced (26→24, the designed price)
- the doc debts paid: DECISIONS collapsed 71→30 (D-034 — the phase-5
  build column D-105..D-133 → the build-family row, the intakes
  D-119/D-128/D-130/D-134/D-135 → the intake family, the
  testproto/protocol rows D-098/D-109..D-113/D-118/D-129 → the
  protocol family, the v0.2 lance D-095..D-104 → the phase-4 row, the
  four phase-3 columns → one compound; compound IDs keep every
  citation resolvable); TASKS collapsed 1240→694 (the phase-5 ledger
  one-liners + the intake sections + the phase-3 rows + the Track B
  one-liners + the phase-6 instruments section; the residue over the
  600 cap is the closed-phase ledgers' substance, §6.1 — one-line
  ledgers are the file's job, cutting them is the iter-0i mistake);
  ROADMAP §2 phase-5 CLOSED; STATUS re-pinned (901→642, the Next step
  → the phase-6 view); the NAV tests-row lag fixed (the post-iter-86
  suites listed); README resynced
- the external protocol runner outside the repo (Rule 9):
  /home/z/my-project/scripts/gate_protocol_iter102.py + the committed
  balance_harness arms (1-seed gate pair + the 60-seed refresh);
  output/ artifacts gitignored, never staged. iter-93 evicted here
  (verified against git in this edit); 10 after. Caps: TASKS 694 /
  phases 1202 / DECISIONS 30 rows held — TASKS + phases over-cap on
  ledger/architecture substance (§6.1, the iter-54 phases.md
  precedent), the next trim point is the phase-6→7 gate.
---
iter-101 · 2026-09-12 · intake10 — the owner's chat call, the
external encounter & event-generation design notes routed
(6 files doc-only, zero code, zero corpus price — the intake-8/9
six-file precedent; one family)
- verified BEFORE working (1589+1 green, ruff clean, HEAD 533a384);
  the verdict set is D-135: the substrate CONFIRMED complete — 21
  of the document's 23 patterns are pack-level discipline or
  read-side shapes over landed primitives (the eight-family
  mapping, phases.md §6; the NPCLedger IS the projection +
  knowledge view); the ONE gap routed as `since-1` (the
  re-encounter delta — read-side, BRIEF_SPEC §3.4's extension,
  the document's own highest-value pick); the four declared
  contradictions DISSOLVED against standing law (phase-scoping;
  the seven stream families; D-079's rejected-flat XOR
  alternative; D-022 just-in-time)
- refined into phases.md §6's encounter block (~80 lines): the
  substrate mapping + the event-source taxonomy + the world-state
  law (derived reads, never a stored object) + the detour fence
  (world-side predicates, never intent inference) + the
  anti-repetition composition (a novelty subsystem refused as
  duplicate bookkeeping) + the selection law (evaluation, never a
  draw); deferred owner-gated: the Kenshi arrival dive (ref-20/
  world-2), the 5-8 hook-pattern catalog (a content row, real
  corpus price), the per-tag recurring cooldown (the murmur
  placeholder); refused: the standalone EncounterSystem family
  (the doc's own §11), docs/design/ENCOUNTERS.md (the
  single-owner chain), stored world-state objects (STATE-1),
  intent-inferring triggers (L6)
- docs: DECISIONS D-135, TASKS the intake-10 section + since-1,
  phases.md §6 the encounter block, REFERENCES §10 (+7 rows:
  Skyrim, Fallout, Zomboid, STALKER A-Life, Shadow of Mordor,
  Rain World, Wildermyth), STATUS re-pinned (the doc-only streak
  iter-100+101 surfaced per AGENTS §2.5 — both the owner's
  calls, the D-022 exception), this file. iter-92 evicted here
  (verified against git in this edit); 10 after. The queue
  untouched — the phase-5 exit review stays the owner's call.
  Caps: STATUS 901 / TASKS 1240 / DECISIONS 101 (68 rows) /
  phases 1202 / REFERENCES 326 — over-cap files ride the
  documented §6.1 substance precedent (D-095..D-135), trim at
  the phase-5→6 gate.
---
iter-100 · 2026-09-12 · intake9 — the owner's chat call, the external
TTRPG cross-media analysis routed (6 files doc-only, zero code, zero
corpus price — the intake-8 six-file precedent; one family)
- verified BEFORE working (1589+1 green, ruff clean, HEAD 1bfcf41);
  the verdict set is D-134: ~70% confirmed landed/pinned (res-1 =
  Dark Sun's bookkeeping cure, depth-6 = the faction-mechanics cure,
  lazy depth = the unused-content cure, the no-op discipline =
  fail-forward's cure, the balance harness = the untested-statblock
  cure); the document's three declared contradictions refined into
  pack laws — the cost law (mechanics own cost, narration owns
  meaning), the failure law, the corruption law (+ decay-branch,
  flashback, ambient) — phases.md §6's cost & consequence block
- deferred owner-gated: the loop-pack / low-magic / soul-scar /
  belief-as-rules pack patterns (zero engine change, riding
  world-2/res-1/PACK_SPEC); refused: creature-ecology sim, visible
  morality meters, history-editing flashbacks, vehicle subsystems
- docs: DECISIONS D-134, TASKS the intake-9 section, phases.md §6
  (+56 lines, substance), REFERENCES §10 (+8 pattern rows: DD,
  Frostpunk, Sekiro, Disco Elysium, PST, Majora, StS/Hades,
  Kingmaker), STATUS re-pinned, this file. iter-91 evicted here
  (verified against git in this edit); 10 after. The queue untouched
  — the phase-5 exit review stays the owner's call. Caps: STATUS
  ~893 / TASKS 1189 / DECISIONS 100 lines (67 rows) / phases 1122 /
  REFERENCES 319 — over-cap files ride the documented §6.1 substance
  precedent (D-095..D-133), trim at the phase-5→6 gate.
---
iter-99 · 2026-09-11 · rev5 — the owner-requested pre-gate revision:
phase-5 verification + the long-run probes + the test actualization
(5 files — 1 new test + 4 doc sync: the revision + the test
actualization are one family; AGENTS §2.3: within cap)
- verified BEFORE working (1586+1 green, ruff clean, HEAD 0ada288);
  the probe battery OUTSIDE the repo (D-046): storyline exhaustion
  (seed 125 + a 60-turn tail), year-scale 3 crossings (seed 42),
  fresh sandbox (seed 7), determinism byte-identical + T2 clean,
  the 16-action reach catalog, the balance harness 60 seeds both
  arms (M5 p50 0.79, chains 15-24, stretch max 1 — the phase
  records hold)
- findings for the exit review: the director a finite magazine
  (all six hooks first_time_only, spent within ~2 days, the burn
  law verified live — new crimes re-seed, nothing releases); the
  day-2+ steady state = rotations + decay + the maid/relief quiet
  urgencies + the social mill (rumors decay to zero, leverage
  expires at 720); the scripted scenario CONSUMED (day-2
  steal/arson door-reject); year-scale = the weather chain + the
  census riding a watch-change loop; weather canon-but-not-tale
  (test_weather's own pin) — no read surface renders the sky yet;
  the suite's longest committed run had been ~1500 ticks
- tests/test_longrun.py (new, +3 — the committed pack's first
  past-a-day runs: the crossing laws at the committed cadence, the
  day-2 living floor, the idle world's beats; self-comparing, zero
  corpus price), 1586→1589+1 green, ruff clean (Python 3.12.14,
  the env pin); a year runs in 0.56 s — the owner's sandbox doubt
  answered with numbers
- docs: STATUS re-pinned (header iter-99, KI#84 deleted per AGENTS §5 —
  closed iter-96a, two iterations past, the mandatory cleanup riding
  this iteration's STATUS touch; the queue untouched —
  the exit review still the Next step, now carrying the revision's
  numbers), NAV §1 the tests row's longrun clause (the row's
  post-iter-86 lag noted for the gate's staleness pass, not
  backfilled here — out of scope), README the count sync;
  TASKS/DECISIONS untouched (the iter-96a audit precedent). iter-90
  evicted here (verified in this edit, the cap 10 held). Caps:
  STATUS 895 / TASKS 1160 / DECISIONS 99 — over-cap on substance
  (§6.1, the D-095..D-133 precedent), trim at the phase-5→6 gate
---
iter-98 · 2026-09-11 · weather1 — the ambient weather family + canon
erosion (the queue's live row after st-6a, TASKS' own letter; 27
files — 4 code + 2 content + 1 new test file + ~20 corpus re-pins +
6 doc sync + this worklog + STATUS: the family + the arming + the
corpus price are ONE row, the TASKS row's own three halves; AGENTS
§2.3: 27 > 5-6, the objective scope noted here)
- core/weather.py (new) + core/rng.py + core/loop.py: the chain —
  one roll per macro crossing on the isolated `weather:chain` stream
  (the D-079 family law's SEVENTH member, singleton; the
  fingerprint never sees a weather roll), a self-roll suppresses the
  event (KI#13) while still advancing the stream; the current
  weather is the FOLD (L3), no knowledge (the ambient law), no
  state_changes; the SEEDED storm consequence (the director's
  buffer through the existing door, the D-082 pattern); the EROSION
  (the fire follow-ups' shape): SEEDED follow-ups whose commits
  revert promoted canon flags (the rain washes the fire layer's
  smoke — an explicit counter-event, EVENT_SCHEMA §4; idempotent on
  state; the never-regress law floors a late crossing's deferral at
  the entry tick — the batch-crossing crash found live and fixed the
  same iteration).
- core/pack.py: the `_weather` lint — the pairing law (weather
  without time.macro is dead data, one direction), the identity law
  (the event type ≠ the macro turn's), the weights/hooks/erosion
  closures (the prop must be a transition follow-up flag), the
  reachability law; `_transition_flags` the closure's helper.
- content/tavern_pack: THE COMMITTED MACRO ARMING (the primitive's
  first consumer) — time.macro at the year-scale cadence 518400
  (one year per crossing, the genesis horizon continued) + the
  weather block (clear/overcast/rain/storm; rain's smoke wash; the
  storm's drunk-murmur hook) + the three template lines.
- tests/test_weather.py (new, +22 — the unit laws, the crafted-pack
  integration, the corpus price both-arms) — 1564→1586+1 green,
  ruff clean (3.12.14, the env pin; the armed twin double-run
  byte-identical). Corpus price, measured both arms: the T1 golden
  + day1_theft BYTE-IDENTICAL (the crossings beyond every script's
  horizon); day1_full pays the LOD's ONE-GATE engagement alone
  (depth-3's designed price, deferred since iter-91 — the warm
  ring's beat events wait for crossings: 61→56 events, the check's
  dice moved with the draw sequence, ~20 test files + narrator
  corpus 5 cases + parser corpus 1 case re-pinned; the weather
  block itself adds ZERO corpus events; the fingerprint EQUAL both
  arms). The INV-3 stoplist caught three fresh-prose nouns (the
  fire follow-ups' naming) — fixed before commit.
- docs: DECISIONS D-133, TASKS weather-1 done, phases.md §5 the
  weather paragraph, NAV §1 the core row, README (the st-6a + weather
  map rows + the status paragraphs + the macro-armed flip — the
  iter-96a sync-gap family closed in passing), STATUS re-pinned
  (the queue: EMPTY of live candidates — the phase-5 exit review the
  owner's call, the D-034 collapse + the §5 staleness pass owed at
  the gate). iter-89 evicted here (verified against git in this
  edit); 10 after. Caps: STATUS 907 / TASKS 1160 / DECISIONS 99 lines
  (44 rows) / phases.md 1066 / README 786 — over-cap on substance
  (§6.1, the standing precedent), trim at the phase-5→6 gate
  (D-128's own rows).
iter-97 · 2026-09-11 · st6a — travel as a separate action (the
STATUS queue's live row after name-1, D-116 (5)'s amended price law;
7 files — 3 code + 1 test file + 3 doc sync + this worklog + STATUS:
the price law + the accept-door branch + the lint are one family,
the iter-90..93 footprint; AGENTS §2.3: 7 > 5-6, the objective scope
noted here)
- core/travel.py (new) + core/loop.py: the price law — the travel
  action is the movement TWIN with an edge price (`ticks: "edge"`,
  the fourth legal value; move's semantics + adjacent_to + the T1
  fixtures untouched); the accept door schedules at `t + price`
  (L3 derive-never-store; day-scale queue-cheap, the crossings fire
  mid-travel in tick order, D-038); override wins per edge, else the
  DERIVED integer function (lattice steps * step_ticks + height-band
  spread * climb_ticks + river endpoints * river_ticks — no runtime
  division, draw-free, the min cross-pair); no price -> loud
  TravelError (the backstop family)
- core/pack.py: the `_travel` lint (after _worldgen) — the pairing
  law both ways (block ⇔ edge-priced action), the weights
  (step ≥ 1, climb/river ≥ 0, omitted = policy), the overrides
  (real undirected edges only, no duplicates, ticks ≥ 1), the
  COVERAGE law (every exits edge priceable — the verb never
  hard-fails mid-run); `ticks: 'edge'` movement-resolver-only
- tests/test_travel.py (new, +18): the formula oracles (hand-built
  WorldModel: step/climb/river/min-cross-pair/override-wins/
  refusals), the lint probes (the crafted-twin pattern), the e2e
  (the derived arm street↔tavern — the claimed pair, the override
  arm, the non-adjacent rejection, mid-travel rotations, the armed
  twin byte-identical double-run); the committed pack UNARMED (the
  68a pattern — the arming rides with world-2's province row)
- 1546→1564+1 green, ruff clean (3.12.14, the env pin). Corpus price
  ZERO by construction — no pack byte touched, zero re-pins
  (git-verified: only core/{intent,loop,pack,travel}.py +
  tests/test_travel.py + docs). INV-3 caught twice by the stoplist
  mid-iteration (a noun in fresh prose, the KI#79 lesson — fixed
  before commit, no KI owed)
- docs: DECISIONS D-132, TASKS st-6(a) done, phases.md §5 the travel
  paragraph, NAV §1 the core row, STATUS re-pinned (the queue:
  weather-1 the next live candidate — its gate satisfied, the macro
  arming rides with its row). iter-88 evicted here (verified in this
  edit, the cap 10 held). Caps: STATUS 863 / TASKS 1168 / DECISIONS
  98 (68 rows) / phases 1018 — over-cap on substance (§6.1, the
  D-095..D-131 precedent), trim at the phase-5→6 gate
---
(end of log — cap 10; pre-trim history lives in git)
