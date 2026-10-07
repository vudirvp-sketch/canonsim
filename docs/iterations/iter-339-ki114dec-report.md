# iter-339 — ki114dec: the KI#114 composition-law decision packet

R0 doc-only — the owner's 2026-10-08 decision call («Принимаем B — закон
композиции на чистой границе drain»). Zero committed code change this
iteration: the option-B implementation exists as the sandbox working-tree
prototype (`core/loop.py`, the exact patch preserved as the session
artifact `ki114-prototype-B.patch`, 300 lines, md5 `2a574912…`, ruff
clean); this packet is its evidence. The fix, the test battery, and the
targeted regeneration land ONLY after the owner confirms the packet
(the decision's point 9). Candidate A (mid-drain resume) is OUT OF
CONTRACT per the decision's point 8 — a separate architectural R&D row
at most, never a silent alternative.

## 0. The decision record (the owner's nine points, compact)

1. The next player intent is admissible ONLY at a clean drain boundary
   (queue empty, the current causal cascade fully complete).
2. The canonical law: `run_steps([A,B]) == run_steps([A]); run_steps([B])`
   and every arbitrary partitioning.
3. `resume` introduces NO separate timing semantics: checkpoint + resume
   == continuous == split, semantically and byte-for-byte.
4. NO mass regeneration yet — first this decision/evidence packet over
   all 70 failures, split into: pure timing/value re-pins; expected
   causal/state shifts from the clean-boundary semantics; real semantic
   regressions.
5. Real semantic regressions MUST be 0 — any single one stops the row.
6. The conscious rebase set (the `.jsonl` fixtures + the golden
   expectations) fixed separately; regeneration only after explicit
   acceptance.
7. The regression law strengthened beyond split-after-wait: the
   composition over different partitionings, minimum for wait, move,
   zero-duration and follow-up/autonomous-drain steps.
8. No checkpoint-model expansion to mid-drain resume (candidate A out).
9. Fix + tests + targeted regeneration only after the packet is
   confirmed as the chosen canonical semantics, not a hidden regression.

## 1. The semantics delta — the drain boundary is the only feed law

The law (one sentence): a player step enters the world only when the
world is settled — the queue empty, the clock at the drain's end tick —
so the feed point is a function of the drained state alone, never of
the call structure around it. Everything else follows: a split at any
boundary, a checkpoint at any boundary, and the uninterrupted batch all
compute the SAME next feed tick, by construction, not by compensation.

The prototype's shape (the patch's whole content, no other file moves):

- `run_steps` restructured: an outer `while pending:` loop feeds ONE
  intent, then an inner `while len(self._queue):` drains the FULL
  cascade it seeded (crossings, reactions, follow-ups, passes, beats),
  then the next intent feeds at `self._clock.tick` — the drained clock.
- `_feed_next` DELETED (the mid-drain feed at the terminal event's own
  tick, the KI#114 root), `_step_intent_id` DELETED (the id-matching
  that gated it — under the structural feed no id matching exists at
  all: only the queue's emptiness speaks; the KI#17 law "an autonomous
  intent's ending never advances the script" holds VACUOUSLY — the
  script advances only at drains).
- The crossing discipline, the H9 skip, the OCC index, the commit door,
  the queue key, the log header: untouched. The prototype touches ONE
  function's control flow.

What observably changes (the four mechanism families, every one of the
70 failures maps to exactly one):

- **F1 — the feed-point shift.** The next step enters at the drain end,
  `tail` ticks after the terminal event (the cascade between them):
  farstead 2y +16, province/road corpora +3 per boundary, B2 talks +6.
  Where the tail is EMPTY the two laws coincide byte-for-byte (grim,
  plumbing — §4).
- **F2 — the deferred-realize phase shift.** The waits complete later
  (F1 compounds per boundary), so the beat-born/urgency/director/faction
  intents minted mid-wait EVALUATE at different ticks: the honest door
  verdicts flip per corpus (day1's document_check now fails where it
  passed; temp1 seed-1001's now passes where it failed), the deferred
  piles reject wholesale on `target.same_location` (§3.5), vigils mint
  on the other side of deadband windows.
- **F3 — the exposure-window closure.** The later entry can miss
  decaying/positional windows the mid-drain entry caught: the pole
  carried off before the read enters (`target.same_location`), the
  night phase over at the read/landing tick, the knock's echo residue
  decayed below the keeper's gate at the shifted convening.
- **F4 — the span/boundary effects.** The run's realized span stretches
  (each step waits out the world's full response), so the beat grid and
  urgency windows land differently across the script's end: event-count
  deltas both ways (province +10, pressure +9, day1 −4, p1 −3).

## 2. The law's verification — the strengthened falsifier (point 7)

Design (the session artifact `scripts/ki114_law.py`, to be ported into
`tests/` at landing): for every battery (a 3-step list whose kinds
cover wait, move, zero-duration `look_around`, and the
follow-up/autonomous-drain family) × every pack (farstead armed,
province, pressure, tavern, grim) × every seed (2 per pack) × EVERY
partitioning of the step list (the full cut lattice: `[A,B,C]`,
`[A|B,C]`, `[A,B|C]`, `[A|B|C]` — 143 checks total with the lab
families), in THREE forms: the whole batch, the split (one Simulator,
`run_steps` per cell — the session pattern), and the resume
(checkpoint + cursor round-trip AT EVERY cut), plus the double-run
determinism arm. The lab protocols ride it too (`_anchor_steps` whole
AND segmented, 3y, farstead + province, directors off — the labrunner's
own form). The director protocol follows test_resume's canonical shape
(export flag == construction flag; a first-draft mismatch was caught by
the law itself and fixed — the falsifier bites protocol bugs too).

Results:

- **Prototype: 143 checks, 0 failures.** The unconditional composition
  law holds on every partitioning, step kind, protocol, pack and seed;
  resume is byte-invisible at every boundary (the decision's point 3
  answered by measurement).
- **BASE (the old semantics): 143 checks, 44 failures** — split AND
  resume forms violate composition across farstead, province, pressure
  (e.g. `province-b0 seed 2 split(1,)`, `farstead-b0 seed 11
  resume(2,)`). The falsifier has teeth: the old law CANNOT compose.
- **The KI#114 repro closed**: the farstead 2-segment split
  (`[move, wait 1y]` + resume + `[wait 1y]`) is byte-identical to the
  uninterrupted run (BASE: the +16-tick divergence at ev_0210,
  reproduced first, then gone).

## 3. The 70-failure classification (points 4–5)

Method: the full suite at BASE (2627 passed + 1 skipped — verified
first, the prototype stashed) vs the prototype (70 failed, 2557 passed,
1 skipped, ~2 min each); every failure's assertion captured
(`--tb=short`); every FAMILY probed to its mechanism (BASE vs prototype
event-level diffs); the ambiguous re-pins verified structure-intact
(same-length lists, same actors/kinds). The 70 split: **(a) 23 pure
timing/value re-pins, (b) 23 expected causal/state shifts, 24 golden
byte compares (whose per-fixture mechanism is (a)-like for road, (b)
-like for province/pressure) — and (c) 0 real semantic regressions.**

### 3.1 Bucket (a) — pure timing/value re-pins (23 tests)

The pinned literal shifted; the structure (kinds, counts, actors,
order, the tested law) is intact. Re-pin is mechanical.

| Test | Pin → now | Mechanism |
|---|---|---|
| ambient quiet_march | waits `[363,364,723,1083]` → `[363,364,726,1086]` | F1 (+3/boundary, same 4 waits) |
| ambient weight_zero | fingerprint tail `(724,'wait')` → `(726,'wait')` | F1 (+2; same-length tail) |
| arc_driver march_releases | sweep `ev_0057 t=1456` → `t=1577` | F1 (same event, later tick) |
| balance_harness seed_125 | `"t": 1456` → `1577` (same ev_0057) | F1 |
| mechanics trace_pins | `[t=1456] ev_0057` → `[t=1577]` (58 events both) | F1 |
| mechanics two_times | `latency: min 11 · max 376` → re-pin | F1 (the spans `[731,1577]`) |
| temp1 B2 clustering | min talk `520024` → `520030` | F1 (+6; the test's own note: a runtime-semantics change) |
| t1_province prices | `(1230,'loc_riverroad')` → `(1233,…)` | F1 (+3) |
| t1_reskin prices | `(765,'loc_street')` → `(768,…)` | F1 (+3) |
| accountgloss reweigh | `[t 2574]` rendered line → later t | F1 (rendered surface follows the log) |
| settlement closed_verb / sale / drain / buyers (4) | heap `(6,5)` → `(10,9)` chains | F1/F4 (+4 translation; the compounding chain intact) |
| ignition open_road / changed_next (2) | heaps `[6,5,14,13,22,21]` → `[10,9,16,15,24,23]` | F1/F4 (+4 translation) |
| charcoalpaper reckoning | `(18,2)/(60,76)` → `(21,5)/(64,80)` | F1/F4 (one more settle realized before the point) |
| shavememory banking/state (2) | line count `5→6`, bloom `14→16` | F4 (the boundary count; the dated chain intact) |
| flowgloss reweigh | surplus line count `5→6` | F4 |
| checkpoint offsets (2) | `[0,20,40,48]` → `[0,20,40,44]` | F2 footnote: the count 48→44 IS the day1 arrest-chain loss (§3.3); the offset ARITHMETIC law is count-agnostic — the re-pin rides the accepted corpus |
| echo declared_table | fingerprint `(1290,'wait')` → `(1291,…)` | F1 (+1; both arms shift together — the A/B law intact) |

### 3.2 Bucket (b) — expected causal/state shifts (23 tests)

The world's answer to the same steps changed by design: a window
closed, a verdict flipped, a different actor realized first. Each
probed to its mechanism; the DOOR/HONESTY laws hold in every case.

| Test | The shift | Mechanism (probed) |
|---|---|---|
| poleseed night_read | the `pole_read` NEVER fires (StopIteration) | F3: the wait's drain runs to t=1788; Dellan's move (rejected in BASE at t=1785) now SUCCEEDS at t=1788 and carries the pole off; the read enters the settled world and honestly rejects `target.same_location` — the attempt IS a fact (intent_rejected, PARSER_SPEC §4) |
| stepread night_read | the stair read lands `t=1790`, outside `[1080,1440)` | F3: the night window closed at entry (the same drain tail) |
| gaproutes night_form | the "landing after dark" line gone | F3: the journey lands in daylight (the render follows the log) |
| pressure bench | the keeper's ration `[]` (never releases) | F3: the knock fires t=604 (both arms); under BASE the convening lands t=3608 — inside the echo window — and rations 4 coal; under the prototype the stoke's drain runs to ≈8648, the wait completes t=12251, the convening t=12253 — the residue 11,649 ticks stale, below the gate; the bench DOES convene (twice) — the gate honestly reads a decayed echo |
| marketlegs (4) | the mourns departure `3297→4983`; the vigil's `by_tick[3299]` KeyError; the trade token absent; the trader `npc_corporal_01→npc_sergeant_01` | F2: the director's mourns release realizes at the shifted beat; everything downstream (the vigil mint, the knowledge token, the walk's first trader) follows |
| genre politics | `wergeld_vigil` count `2→1` | F2 (the faction deadband window at the shifted realization) |
| negative mourning | vigil count `4→3` | F2 |
| p1 institutional_check | `checks == []` — the sergeant's checks all rejected | F2/F3: see the OCC census §3.5 — the deferred piles miss the co-location windows |
| p1 market_fire | the guild councils `4760→5067` | F2 (+307, the realization phase) |
| p1 deadband | vigils `4→3` | F2 |
| p1 causally_loud | event_count `2276→2273` | F4 (−3; the vigil family + the checks' downstream) |
| p1 final_projection | suspicion `100→55` | F2 downstream (no arrest consumes it; the decay baseline differs) |
| p1 deferral_latency | min latency `80→25` | F2 (the latency surface re-measured) |
| p1 occ_miss | the ONE pinned rejection → 76 | F2 — the census §3.5 |
| echo jittery | the watcher's first scan `374→494` | F2 (the beat realization moved; 2 scans by the same guard, the fade law's shape intact) |
| beliefwire decrystallizes | scans `1→3` in the window | F2/F4 (more of the walk realized inside the window) |
| mediator regression set (3) | verdicts `'accepted' → 'regen'` | F2 via the corpus protocol: the beats' world moved; the verdicts follow CURRENT canon (VALIDATION_SPEC — the harness's own designed 'regen' answer, never a silent mismatch) |
| temp1 A2 cascade | `document_check_failed` absent from the span | F2 (the honest check now PASSES on seed 1001 — the flip's other direction; day1 below shows the failing direction) |

### 3.3 The golden byte family (24 tests) — per fixture

Nineteen files' corpus checks + the t1 fresh/regeneration pairs ride
THREE fixtures (the census, `scripts/ki114_fixture_census.py`):

| Fixture | Golden vs fresh (prototype) | First divergence | Mechanism | Disposition |
|---|---|---|---|---|
| `province_smoke_seed42.jsonl` | 44 → 54 events (+10) | line 19: `ev_0017` wait `t=630→633` | F1 (+3) then F2/F4 compound (the extra realized beats/urgencies inside the stretched span) | regenerate (20 test files + t1_province ×2 byte laws) |
| `road_smoke_seed42.jsonl` | 24 → 24 (count UNCHANGED) | line 19: `ev_0017` wait `t=555→558` | F1 pure (+3 timing, no texture change) | regenerate (t1_reskin ×2) — a pure-timing rebase |
| `pressure_smoke_seed39.jsonl` | 29 → 38 events (+9) | line 7: golden `ev_0005 move t=10` vs fresh `ev_0005 pipes_knock t=608` | F1/F4: under BASE the player's steps interleave BEFORE the knock; under the law the stoke's whole drain (the knock at 608 and its cascade) completes FIRST | regenerate (pressure ×1 byte law) |
| `grim_smoke_seed42.jsonl` | byte-identical | — | the quiet-boundary law: every step's drain tail EMPTY → the two semantics coincide EXACTLY | UNTOUCHED (no rebase; the census is the proof) |
| `plumbing_smoke_seed42.jsonl` | byte-identical | — | same | UNTOUCHED |

The mediator's `narrator_beats` corpus (the 3 'regen' verdicts) rides
F2 — its expectations regenerate per the corpus protocol at landing
(verdict level, not bytes).

### 3.4 Bucket (c) — real semantic regressions: ZERO (point 5)

The clearance, family by family — every candidate investigated, none
survived as a regression:

- **The composition law itself**: 143/143 green (§2) — the law the
  iteration exists to make.
- **The OCC census** (the scariest number, 1→76): all 76 are
  `reason=precondition` DOOR rejections on `target.same_location`; all
  76 autonomous (75 `document_check` + 1 `talk`; cause families
  urgency/director); ZERO player-step rejections in the P1 corpus (the
  poleseed player rejection is the honest door fact above); the 76 sit
  at exactly 3 distinct evaluation ticks (3797 / 5065 / 526229) — the
  deferred piles of the re-minted walks (`urgency_0001`,
  `urgency_0004`, `director_0002`), realized at the shifted wait
  completions, every one an honest same-location break. No wedge (each
  queue entry pops once; the ids repeat across mints by the family's
  own design — the P1a FIFO law's documented shape).
- **Determinism**: `test_the_twin_run_is_byte_identical` (p1) PASSED
  under the prototype (2273 events, twin-byte-equal); the falsifier's
  double-run arms green; INV-2 untouched (no draw-order change: the
  streams are per-name counters, the feed law moves no draws).
- **INV-1..5**: the prototype touches one function's control flow; the
  log writer, the queue key, the header, the schema untouched (the
  suite's architecture/stoplist tests passed — in the 2557).
- **The door/honesty laws**: every rejection carries cause and failed
  test; attempts are facts; the two-times record richer than before
  (the 512,189-tick deferral window now visible in the corpus).
- **The cursor/resume law**: resume byte-invisible at every boundary
  (§2); the mid-drain save refusal law untouched
  (`test_export_cursor_refuses_mid_drain` passed).
- **The station cross-check corpus** (iter-336): a DOC-level note, not
  a regression — the committed kiloyear canon md5s (`a1d8f05b…`,
  `7cbfb68a…`, the station's logs) are records of the PRE-KI#114
  semantics; after landing, a re-measured canon re-baselines them (the
  historical rows stand as history; no committed fixture depends on
  them — `test_lab`/`test_h9`/`test_occidx` passed, their A/B laws
  compare arms within one code version).

## 4. The conscious rebase list (point 6)

To REGENERATE at landing (only after the owner's confirmation of this
packet): `province_smoke_seed42.jsonl`, `road_smoke_seed42.jsonl`,
`pressure_smoke_seed39.jsonl` (the census table above) + the mediator
`narrator_beats` corpus expectations. To RE-PIN: the 23 (a)-family
literal pins + the 23 (b)-family expectations (§3.1/§3.2 — several of
the (b) tests' AUTHORS' intent may warrant re-crafted corpora to keep
testing their laws meaningfully under the new feed law: the pressure
bench's echo window, the poleseed night chain, the p1 institutional
check — the landing row's named work). PROVEN UNTOUCHED: grim,
plumbing (byte-identical, the quiet-boundary proof).

## 5. The landing row (opened, gated on this packet's confirmation)

`ki114-1-impl` (R2 local behavior — the feed law change): land the
prototype (`core/loop.py`); port the falsifier into `tests/`
(the 143-check battery as the composition law's permanent form);
regenerate the 3 fixtures; re-pin the 46 expectations (the (a)/(b)
tables); the riders (STATUS KI#114 → CLOSED, TASKS, worklog, TEST_PLAN
§9's claim packet). NOT in scope: candidate A (out of contract), any
checkpoint-model expansion, any pack-data change.

## 6. The verification actually run

BASE green first (prototype stashed): `2627 passed, 1 skipped` (~129 s)
— the iter-338 record reproduced. The prototype suite: 70 failed /
2557 passed / 1 skipped, every failure captured and classified above.
The falsifier: 143 checks × both arms (0 vs 44). The census: 5 fixtures
× fresh-run byte-compare. The probes: poleseed/pressure/p1/day1
event-level BASE-vs-prototype diffs. `ruff check .` clean (both arms).
docguard clean (this packet). The suite was NOT re-run green with the
prototype applied — by design: the 70 failures ARE the deliverable's
subject; the committed state (this delta, docs-only) leaves the suite
green.
