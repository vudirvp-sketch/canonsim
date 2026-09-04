# TEST_PLAN.md — Phase-0 Verification Stack

> Spec written at the iter-6 trigger (`SPECS_BACKLOG.md` row). Formalizes
> the T0–T8 suite + the M1–M5 metric definitions + the gate protocol.
> Source of truth for what counts as "the gate passed." Scope: phase 0
> only. The T-suite is the invariants made executable (D-031): every
> INV has at least one test that fails loudly on its violation.

## 1. T-suite (the gate tests — `MVP_SCOPE.md` §14, `phase0.md` §6)

| ID | Name | Owner test(s) | Donor technique folded in |
|---|---|---|---|
| T0 | schema | `tests/test_t0_schema.py` | every log line validates; the doc example is the fixture (D-010) |
| T1 | determinism | `tests/test_t1_determinism.py` | two runs byte-identical **+ RngBank fingerprint equality** (Brogue audit counter) **+ fixture-regeneration guard** (iter-6): a fresh regeneration into a tmp dir diffed against the committed fixtures; a divergence with unchanged `schema_version` = fail. The committed fixture's header `schema_version` must equal the version derived from the current `schemas/event.schema.json` `$id` — a schema bump without a fixture regen fails here. |
| T2 | replay | `tests/test_loop.py::test_t2_fold_equals_runtime_projection` | `fold(log) == state`; the simulator's incremental projection and a fresh fold of the committed log produce equal state (EventStore projection equivalence) |
| T3 | blind-NPC | `tests/test_knowledge.py` | zero knowledge leaks on the suite; UAP motivation-hole crosswalk designs the cases (an NPC with no record for a fact cannot act on it; suspicion-from-absence is illegal without an `inferred`-channel record cause-chained to the trigger event) |
| T4 | irreversibility | `tests/test_crime.py`, `tests/test_states.py` | `irreversible` state changes never revert without an explicit counter-event (fire has none — `location_burned_out` clamps the spot to `burned_out` and no later event reverts it; the arrest `caught` value is terminal) |
| T5 | impossible | `tests/test_loop.py::test_teleport_stays_impossible`, `tests/test_intent.py`, `tests/test_actions.py` | teleport / sourceless arson / absent items / knowing the unseen stays impossible — well-formed but world-impossible intents emit `intent_rejected` no-op events (the world did not change); shape errors raise `RunnerError` loud |
| T6 | smoke | `tests/test_urgencies.py::test_urgencies_fire_when_player_waits_long_enough` (1100-tick wait crosses the 1000-tick line) | 1000 ticks without exceptions or hangs — the queue drains, every system that fires on a beat fires, the writer closes cleanly |
| T7 | readability | manual (this iteration's playtest entry in `worklog.md`) | a human retells the chronicle in their own words — the only human judgment in the stack; the tuning knob is the IMPORTANCE RULE's story-critical hook (D-045(b); landed tune-1/iter-27, D-059 — `tale_gate.min_importance` follows the rule, it is not the primary knob) |
| T8 | director-off | `tests/test_t8_ab.py` (iter-6) | A/B on identical seed + playscript, **single-factor** (live-char one-change rule: only the director flag changes); ≥3 emergent chains without the director. M5 non-PC share is non-zero in the OFF run by construction (D-021 urgencies). |

### 1.1 T1 fixture-regeneration guard (iter-6 specific — `phase0.md` §6)

The guard runs in-pytest (no CI change). T1 executes twice in
`tests/test_t1_determinism.py`:

1. **byte-identity**: two fresh runs with the same seed + script produce
   byte-identical logs (the existing `test_two_runs_are_byte_identical`).
2. **fixture-regeneration**: a fresh run is diffed byte-by-byte against the
   committed `tests/fixtures/plumbing_smoke_seed42.jsonl` (the existing
   `test_fresh_run_matches_committed_golden`), AND the committed fixture's
   header `schema_version` must equal the `$id` version of the current
   `schemas/event.schema.json`. A schema bump without a fixture regen fails
   here loudly — the migration procedure (§3 below) is forced, not punted.

### 1.2 T8 emergent chain (the operational definition)

An **emergent chain** is a maximal causal path `ev_n → ev_{n-1} → … → ev_0`
in the OFF-run log such that:

- `ev_n.actor != pc_01` AND `ev_n.provenance.cause_intent` does NOT start
  with `director_` (the director did not inject it);
- the chain walks `cause` links until it reaches a `pc_01`-actor event (the
  player's own action that seeded the consequence) or a `world`-actor root
  (a transition-engine ignition seeded by a player action);
- the chain length is ≥ 2 (one event, then another = not emergence).

Counting is **per qualifying endpoint**: each non-PC, non-director event
whose backward walk (maximal — it extends to the player root, never
stops early) traverses ≥ 2 non-PC links counts once. Consecutive
`status_decayed` events cause-chain to each other (the beat chaining
rule, D-038/D-041), so one decay cascade contributes several endpoints
and M3's magnitude is decay-dominated — the ≥3 gate and the M3 ≥ 2
kill-criterion read directionality, not deduplicated path counts.

The OFF run of the gate playscript (`tests/playscripts/day1_full.json`,
seed 125) produces ≥ 3 such chains. The full count is reported in
`worklog.md`; the test asserts the gate minimum (3).

## 2. Metrics M1–M5 (`MVP_SCOPE.md` §15 owns the definitions)

Computed by folding the log — never collected by feel (Mesa
`DataCollector` is the shape, inverted: the metric is a pure function of
`(events, projection)`, no per-event hook into the simulator). The
implementation is `core/metrics.py`; the system classification table lives
in `content/tavern_pack/rules.json` under `metrics.system_of_type`
(pack data — INV-3).

| ID | Metric | Computation | Directionality (MVP_SCOPE §15) |
|---|---|---|---|
| M1 | cross-system share | for each event, the set of systems touched = the union of systems of the event's `type` + systems of each `state_change.prop` (e.g. `position`, `relations.suspicion`, `status.fatigue`, `fire.<spot>`); share = `len(events_with ≥2 systems) / len(events)` | non-trivial and rising across the slice |
| M2 | deferred hooks fired | released / seeded, computed on the ON-run log (the OFF run is 0 by construction). **Released** = events whose `provenance.cause_intent` starts with `director_` — a release is the director's dispatch; a world-rejected release still counts as released. **Seeded** = total hook instances (`len(hooks)` summed over events — a multi-hook event counts as multi-seeded). On the gate ON log: 1 released / 2 seeded = 0.5. | non-zero (≥1 release per the cli AB test) |
| M3 | causal chain length | for each event, walk `cause` links until `null`; depth = chain length. M3 = mean and median depth over all events. | mean ≥ 2 (one event, then another = failure) |
| M4 | novelty / repetition | (a) rate of repeated `(type, actor)` bigrams: `repeated_bigrams / total_bigrams`; (b) share of distinct `knows` tokens: `len(distinct knows) / len(knowledge records)`. RimWorld's repetitive-tale problem, measured instead of felt. | novelty share rising (repetition rate low) |
| M5 | non-PC event share | `len(events where actor != pc_01) / len(events)` — computed on the OFF-run log. "World not player-centered" (Kenshi/RimWorld lesson) made measurable at the director-off gate. | non-zero (≥3 emergent chains by T8 construction) |

### 2.1 Thresholds (set from the measured baseline — D-019)

Direction first, numbers from data. The iter-6 baseline runs the gate
playscript (`tests/playscripts/day1_full.json`, seed 125) ON and OFF, folds
each log through `core/metrics.py`, and records the numbers in
`worklog.md`. The phase-0 exit verdict reads those numbers against the
directionality targets; honest reporting if a target is missed — the
kill-criteria (`MVP_SCOPE.md` §16) win over a Green verdict.

## 3. Schema-bump migration procedure (INV-5 discipline)

When `schemas/event.schema.json` or `docs/EVENT_SCHEMA.md` changes
breaking (rename/remove/retype a field, remove an enum value):

1. Bump `schema_version` in `schemas/event.schema.json` `$id`
   (`canonsim/event/<ver>`).
2. Append a migration note to `docs/EVENT_SCHEMA.md` §8 listing the
   change, the rationale, and the replay-compatibility stance (does
   replay code understand the old version? the default is no).
3. Regenerate every committed fixture under `tests/fixtures/` against
   the new schema; commit the new fixtures together with the schema
   change in the SAME iteration.
4. Re-run T1 — the fixture-regeneration guard passes when the
   committed fixture's `schema_version` equals the current schema `$id`
   version AND a fresh run still matches the committed bytes.

A breaking schema change WITHOUT fixture regen is the loud failure the
guard is designed to catch — the alternative is silent drift between
the schema, the committed fixtures, and the runtime.

## 4. Gate protocol (`ROADMAP.md` §5)

A gate is passed only on evidence. The phase-0 gate runs:

1. **The committed playscripts** — `tests/playscripts/plumbing_smoke.json`
   (T1/T2 anchor) and `tests/playscripts/day1_full.json` (T8 gate) —
   with identical seeds (42 and 125 respectively). Director on and off.
2. **M1/M2** computed on the ON-run; **M3/M4** on both; **M5** on the
   OFF-run. Numbers in `worklog.md`.
3. **Director-off A/B run** (T8): single-factor switch, ≥3 emergent
   chains, the director buffer seeds in both runs (D-005 hygiene).
4. **Human chronicle read** (T7): the gate author retells the
   `day1_full` chronicle in their own words, evaluates noise vs signal,
   and (if needed) tunes the importance rule's story-critical hook
   (D-045(b)/D-059 — the tale gate follows the rule's split; tune-1
   landed the initial hook + the medium gate, iter-27).
5. **Verdict in `worklog.md` + `STATUS.md`**: pass / pass-with-deferred /
   kill. A kill-criteria hit stops feature work until the ontology is
   fixed — honestly reported, never averaged away.

## 5. UAP 7-hole crosswalk (motivation design — `docs/ref/uap_audit.md`)

The Universe Audit Protocol's seven motivation holes map onto the
phase-0 T-suite as test-design rubrics, not as a checklist:

| UAP hole | Phase-0 crosswalk |
|---|---|
| motivation | T3 blind-NPC — does the world act only on what an NPC knows? A guard who never saw the theft cannot arrest; the absence of a record is the test. |
| memory | T2 replay — does `fold(log)` restore the canonical state? A projection that disagrees with its own log fails loudly. |
| competence | rules-driven behavior — actions draw checks through the same pack data, not a special-case branch per NPC; the drunkard's vague testimony is the intoxication → perception → witness-quality chain by construction. |
| scale | D-005 buffer — the director's consequence buffer scales by event count, not by world size; the stagnation sensor reads observable state only. |
| resources | tick queue + per-action duration — the queue key `(tick, sub_order, actor_id)` is the resource model; OCC gates ensure a cancelled action is a new event, not a free one. |
| ideology | phase-5 factions — out of scope for phase 0 (MVP_SCOPE §2); the crosswalk is forward-looking. |
| time | tick queue + the beat cycle — rotations and beats ride clock-crossings in tick order (D-038); the queue forbids out-of-order commits. |

The crosswalk lives in `TEST_PLAN.md` (this file). The per-hole
diagnostics are the donor techniques in §1's donor column — the UAP is
a design lens, not a runtime component.

## 6. balance-1 harness (KI#4 close) + the DIR-2 pacing A/B (iter-37)

The 1000-sim distribution harness (`scripts/balance_harness.py`,
committed as a script — D-044; operator tooling per D-046): runs the
gate playscript (or a variant) 1000
times across sampled seeds, folds each log through `core/metrics.py`,
and emits a distribution table for `suspicion` peak per NPC, `fire_spread`
spot count at burnout, M5 share, and emergent-chain count. Validates
that `rules.json` thresholds are tuned, not guessed. Uses T1
determinism (no new infra). Output:
`output/balance_<N>_seed<S>_<on|off>.txt` (gitignored runtime
artifact — never committed; a `…_nopacing.txt` suffix marks the
clock-off arm).

The harness is the iter-6 close of KI#4: it exists, it runs, the
observations accumulated across iter-2..5 are recorded as concrete
distributions, not feel. The kill-criteria in `MVP_SCOPE.md` §16
("Events without consequences", "Knowledge does not affect behavior",
"The director produces noise instead of causal complications") are
operationalized as M3 mean ≥ 2, M1 share non-trivial, M2 release
non-zero.

**The DIR-2 pacing A/B (phase 3, iter-37 — the exit criterion's
measurement).** `--pacing on|off` (default on; requires
`--directors on` — a disabled director never consults the clock):
the on arm runs the committed pack, the off arm runs the same pack
minus `director.pacing` — a pack without the block runs the v0.1
minimal pair (the pack's own declaration is the gate, INV-3) —
materialized once per invocation under the gitignored
`output/pack_nopacing/` and linted on load. The instrument is
`core.metrics.eventless_beat_stretches(pack_rules, events, gate=…)` —
a pure function of the log + pack data (D-042): a **scene event** is an
event at or above the pack's tale gate (`Grammar.tale_gate`, the
same gate the chronicle renders by — the importance rule owns the
signal/noise split); a **beat window** is `(previous_beat, beat]`
over the `urgencies.beat_ticks` axis the loop actually fires
(DIRECTOR_SPEC §7; an event at a beat's tick belongs to that beat's
window; the trailing partial window is dropped). A stretch is a
maximal run of consecutive eventless windows; the table reports
`eventless_max_stretch` stats, the quiet-run share, and the
length histogram — the numbers the phase-3 exit criterion ("a
scene without an event < N beats", ROADMAP §2) reads at its gate.

Measured (iter-37, 1000 seeds 100–1099, day1_full, director on):
**both arms identical, per-seed byte-identical (10 probed) — max
stretch 1, one stretch per run (the (360,720] phase-boundary window
between the theft ladder and the fire chain), quiet 1000/1000.**
The clock's measurable delta on this pack+script is exactly zero:
every run ends in PEAK (the double-steal suspicion holds entropy ≥
peak_floor 25 through the last beat; the stagnation path never
fires, so REST never gates anything — the D-065 "un-tuned numbers"
note gets its answer). A measurable delta needs a script/pack that
walks the world into quiet — a phase-3 gate-protocol script-set
question, recorded in D-066, not forced here.

Re-measured at iter-38 (DIR-3, the climax layer landed): 10 seeds,
both arms byte-identical, stretch blocks equal — the climax layer is
likewise inert without a climax-flagged hook (the pack declares
`climax_floor` 75, no hook carries the flag; D-067).

Re-measured at iter-39 (DIR-4, the multi-channel split landed): 10
seeds, the committed pack (channels declared, both hooks tagged) vs a
channels-stripped linted variant — per-seed byte-identical logs
10/10. The channel split only gates the quiet path, and the quiet
path never fires on day1_full (every run ends in PEAK, the D-066
finding) — the split is unit-pinned instead
(tests/test_director.py: the quiet-channel-while-another-burns law,
the escalation self-block, the global clock gate; D-068).

Re-measured at iter-40 (drama-1, the event grammar's predicate +
weight layer landed): 10 seeds (125 + the nine corpus-session seeds),
the committed pack (the vigil hook carries the weight_multiplier
object + first_time_only) vs a grammar-stripped linted variant
(`output/pack_nogrammar/`) — per-seed byte-identical logs 10/10. The
mechanism: the multiplier only ADDS tension on these runs (the
escalation arm needs suspicion ≥ 50, which already puts every quiet
gate over its floor) and the vigil never releases there (the quiet
path never fires; the hook is trigger-less) — so no release decision
can flip. The escalation, the truncation order, and the burn law are
unit-pinned instead (tests/test_predicates.py +
tests/test_director.py; D-069).

Re-measured at iter-41 (drama-2, the option layer landed): the same
10 seeds, the committed pack (the vigil hook carries the glance/stare
option pair) vs an options-stripped linted variant
(`output/pack_nooptions/`, a runner outside the repo per Rule 9) —
per-seed byte-identical logs 10/10. The mechanism: the option choice
resolves only at release, and neither tavern hook can release on
these runs through a changed path — the vigil is quiet-path-only (the
D-066 all-PEAK window) and the document-check carries no options (its
causal release runs the implicit base option, the exact v0.1 payload
path). The pick laws — the tie by declaration order, the escalation
flip at the band, the zero-out, the deferred release, the closed-boss
no-mark law — are unit-pinned instead (tests/test_director.py;
D-070; DIRECTOR_SPEC §3b the contract owner).

Re-measured at iter-42 (drama-3, the on_action dispatch landed): the
same 10 seeds, the committed pack (the then-dormant
`document_check` → `crowd_wary` entry) vs an on_action-stripped
linted variant — per-seed byte-identical logs 10/10 (the entry keyed
on an event no action emitted).

Re-measured at iter-43 (the document_check action landed — D-072,
the owner's content call): the entry is LIVE, so the A/B measures its
real delta. The same 10 seeds on day1_full, the committed pack vs the
on_action-stripped variant (a runner outside the repo per Rule 9):
the check fires on 1/10 (seed 125 — the only seed whose day1_full
steal geometry opens a watcher's band with the confrontation world
open; the `take` shifts each seed's stream), that seed diverges by
exactly the `crowd_wary` reaction events, the other 9 stay
byte-identical (no check, no entry — the corpus's own seed-93 script
fires instead: 4 corpus cases re-distilled in the same iteration, the
iter-15 regen precedent). The dispatch's live behavior — the ladder
(verdict → arrest → caught), the talked-down branch, the deferred
release, the climax-path release, the crowd reaction on both branch
types — is pinned directly (tests/test_doccheck.py; D-072;
DIRECTOR_SPEC §3c/§11). The alarm panic echo stays the
recorded-not-landed row (DIRECTOR_SPEC §11) — the next content row,
with its own corpus regen.

Re-measured at iter-48 (content-2, the alarm panic echo landed —
D-077, the §11 row closing): the entry is LIVE, so the A/B measures
its real delta — but the day1_full stage never gives it one: the
same 10 seeds, the committed pack vs the alarm-entry-stripped
linted variant (a runner outside the repo per Rule 9) — 10/10
byte-identical, zero `alarm_raised` events in any log (the
empty-backyard law: the gate script's arson burns the yard the PC
stands alone in, `when_occupants_present` raises no alarm, no event
for the entry to key on — the iter-42 dormant-arm shape, now for a
LIVE entry). The echo's live divergence lives in the corpus's own
occupied-room scripts: the 7 fire-family cases (seeds 33 and 93)
re-distilled in the same iteration (the occupants' fear claims
40→50, the post-alarm event ids +1, the alarm case gaining the
panic event claim + the cause actor's fear — the iter-43 regen
precedent, the fixed-point runner outside the repo). The live
behavior — the compounding (spike + contagion), the cause actor's
own-shout fear, the decay baseline (the echo commits at the alarm's
tick, the beat-360 decay reads 50→46 / 10→6), the chronicle line
directly after the shout, the one-hop termination, the stripped-
entry byte-identity on alarm-free runs — is pinned directly
(tests/test_panic.py; D-077; DIRECTOR_SPEC §3c).

Re-measured at iter-49 (content-4, the coerce driver landed —
D-078, social-1b's live content set): the entry is LIVE, so the A/B
measures its real delta — 2/10 byte-identical (seeds 15, 85: the
drunkard's roll misses at every crossed beat), the 8 diverging seeds
change by exactly the drunkard's idle waits disappearing (event-id
shifts, ZERO outcome flips — the replacement law keeps the per-beat
draw count, so every check keeps its draw position) plus seed 125's
two `intent_rejected` (failed_test `actor.leverage_over`: the theft
failure mints the room's clusters at t=9 expiring at 729, the
beat-720 gate passes on the live fold, the door's own re-read at the
entry tick finds the card expired — the tick-window law live on
day1_full, the world's honest record of a stale reach). No coerce
commits on day1_full: the gate script's theft succeeds on 9 seeds
(no mint, no card to play), and the one minting seed's card expires
before the door. The live behavior — the spend's outcome.cluster
naming the drunkard's mint, the pair axes 25/75, one-secret-one-
play, the expired-card rejection, the chronicle line — is pinned
directly on the COMMITTED pack (tests/test_coerce.py; D-078). The
corpus re-distill (the fixed-point runner, identity-proved first —
105/105 zero-change on the unshifted stream): 2 id re-pins + the
silent_second tail re-pin (crowd_wary → coerce) + the deliberate
spend claims on outgoing_guard beat0, zero ladder flips; 4 seed-93
corpus cases see the coercion.

Re-measured at iter-50 (engine-2, D-079 — the urgency-roll stream
split): two arms. The FLIP arm (HEAD vs the split, the one-time
migration's honest measure): 0/10 byte-identical — every seed
diverges at the beat-720 region, the checks shift by the removed
draws (fingerprints 15→6 / 17→10 / 20→14 / 38→11 / 35→13: the
urgency draws left the substantive stream and the flipped ladders
changed the downstream draw counts); seed 125's doccheck ladder
flips (intent_rejected → document_check_failed — the confrontation
now passes its check). The ADD-SAFETY arm (the iter-49 refused
scenario rehabilitated: an ADDED p=40 entry, silent by gate): 10/10
byte-identical — the per-entry streams decouple the rolls from the
checks AND from each other. The single shared urgency stream was
measured FIRST and refused: 4/10 byte-identical (the added entry
shifts the later beats' roll positions — the maid's urgency stops
firing; the entries couple by draw position). The corpus
migration: 2 narrator cases (the flee-pursuit check flipped; one
case migrates to the refusal family — its caught-fleeing knowledge
claims die with the vanished flee_caught event) + 1 parse pin (the
s7 wait-720 batch 15→14) + 2 unit seed re-probes, through the
identity-proved fixed-point runner (105/105 zero-change on the
unshifted stream, the runner rebuilt per the FAQ laws).

Re-measured at iter-51 (content-5, the echo driver landed — D-080,
social-2's live content set): the entry is LIVE, so the A/B measures
its real delta — the same 10 seeds, the committed pack vs a
driver-stripped linted variant (a runner outside the repo per Rule
9): **10/10 byte-identical** (the dread-silent law: day1_full's
residue channels all sit below the dread-15 bar — the reach family's
partial sighting reads 6, the purse family's inference is
wariness-only; the empty-backyard fire never mints a sighting). The
live divergence is corpus-script-only: **1/105 cases** — the
watch-change case (seed 33, the fire family) diverges by exactly the
guard's scan (ev_0020, t=374, the guardroom), the trailing wait's id
+1, ZERO ladder flips and ZERO broken pins — the corpus regen is the
deliberate pins alone (the scan claim by id + the scene snapshot
knowledge, the case's beat needle 10→12; the iter-48/49 deliberate-
pin law with no forced re-distill behind it — engine-2's add-safety
delivered at the corpus level: the landing's events ride after the
case's claimed ids). The refused design arm (the wariness gate over
the purse residue): 34/105 cases + 10/10 day1_full seeds would fire,
the document-check release case's arson beat starves on the
anchor-shifted event ids (the stream count moves the reply gate —
the fixed-point runner would own it, but the designed ladder's
survival becomes re-pin luck), and the rotation briefings renew the
purse residue every 720 — the jitteriness would never fade on
multi-day runs; refused and recorded in D-080. The live behavior —
the two scans (beats 360/720) then the fade silence (beat 1080,
dread 7 < 15), the scan's snapshot mint, the silent-skip law, the
driver-stripped fingerprint identity — is pinned directly
(tests/test_echo.py; D-080).

Re-measured at iter-52 (content-6, the arc driver landed — D-081,
arc-1's live content set): the chain is LIVE, so the A/B measures its
real delta — the same 10 seeds on day1_full, the committed pack (the
aftermath arc `[possible_document_check_relief, barkeep_wary_sweep]`
gap 2) vs the arcs-stripped linted variant (a runner outside the repo
per Rule 9): **9/10 byte-identical** (the quiet seeds' steals succeed
— no failure event, no seeding, the successor never enters the
buffer; not even the hooks field diverges), **seed 125 diverges by
exactly ONE appended event** (ev_0052, t=1456, the barkeep's
look_around via director_0001 — after everything HEAD held, zero id
shifts; the release march: the relief at beat 1, the sweep at beat 3,
the gap law holding beat 720). The STRIPPED arm's shape is the
driver's proof: the sweep releases at beat 720 instead — both
intents ride the same entry tick (t=732) and the queue's actor_id
tiebreak pops the barkeep BEFORE the relief guard, so the sweep's
event lands at t=733, BEFORE the check's own event at t=734 — a
second beat landing before its predecessor is a causality lie in the
canon, and the gap law is what prevents it (the arc load-bearing,
not decorative: removing it changes WHERE the beat lands and what
the canon order says). The corpus: **105/105 pin-green, ZERO
re-distill** — the first content landing with none (the 14
theft-failure cases diverge by exactly the seeding event's own
`hooks` field, the birth record; no new corpus event — the runs the
driver targets end before a second beat scan, and the unchained arm
fires zero sweeps there too). The successor's weight 0 keeps the
entropy footprint exactly zero on every run (the +W gate-flip class
dead by construction); the fingerprint identity (the sweep adds no
draws) and the quiet-seed byte-identity are pinned directly
(tests/test_arc_driver.py; D-081). The nopacing arm (DIR-2's A/B)
now differs by exactly the sweep: the trigger-less climax-flagged
successor dies without the climax layer — the D-065
"both arms identical" record superseded in part (the clock's
PEAK/REST bands still gate nothing; the closing beat rides the
climax path), re-pinned in tests/test_balance_harness.py.

Re-measured at iter-53 (content-3, the ambient driver landed — D-082,
DIR-4's declared-but-dormant dimension gains its live consumer): the
hook is LIVE but day1_full never opens its gate — the same 10 seeds,
the committed pack vs the landing-stripped linted variant (a runner
outside the repo per Rule 9): **10/10 diverge by EXACTLY the wait
events' `hooks` field** (2-5 lines per seed, the ambient tag's birth
record — the iter-52 zero-regen shape) and **zero appended events on
every seed** (the all-PEAK law: the quiet path is suppressed at every
beat; seed 125's closing sweep stays the last event). The T1 fixture
regenerated in the same commit (the plumbing waits' birth record —
two `hooks` fields, byte-diff verified as exactly those two lines,
TEST_PLAN §3 procedure). The corpus: **105/105 pin-green, ONE
deliberate divergence** — the quiet-beat case (seed 7) gains the
ramble at t=733, its LAST event; the case's own claims grown to pin
the murmur by id+type + the barkeep's heard record (the iter-51
deliberate-pin pattern, no re-distill behind it). The live behavior
— the quiet march (the wait-seeded tag, the beat-720 release through
the ambient channel's own floor with the rotated guard honestly
absent from the listeners), the chronicle line in log order, the
burn, the directors-off arm, the seeding-stripped isolation, the
fingerprint identity (the ramble draws nothing; its one honest
downstream — the heard record crossing the t=1080 watch change as
the evening guard's briefing) — is pinned directly
(tests/test_ambient.py; D-082). The nopacing arm of THIS test's
D-065 record re-pinned: without the pacing clock no PEAK suppression
remains, so the ambient channel's own floor gates the last beat —
the nopacing arm now closes on the ramble (t=1458) where the ON arm
closes on the sweep (t=1456); both arms share their 52-line prefix
(the clock's presence swaps WHICH director beat closes the day —
tests/test_balance_harness.py).
