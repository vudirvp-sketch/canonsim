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
