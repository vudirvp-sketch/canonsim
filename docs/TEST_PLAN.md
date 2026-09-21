# TEST_PLAN.md — Verification Stack

> Spec written at the iter-6 trigger (`SPECS_BACKLOG.md` row). Formalizes
> the T0–T8 suite + the M1–M5 metric definitions + the gate protocol.
> Source of truth for what counts as "the gate passed." Scope: the
> whole repo's verification vocabulary — the T-suite + metrics + gate
> protocol (the phase-0 origin), the offline acceptance suites
> (§6–§7.2), the testproto LLM-integration protocol (§8) + the
> heartbeat ledger (§8.5), the claim → instrument selection grammar
> (§9). The T-suite is the invariants made executable (D-031): every
> INV has at least one test that fails loudly on its violation.

## 1. T-suite (the gate tests — `MVP_SCOPE.md` §14, `phase0.md` §6)

| ID | Name | Owner test(s) | Donor technique folded in |
|---|---|---|---|
| T0 | schema | `tests/test_t0_schema.py` | every log line validates; the doc example is the fixture (D-010) |
| T1 | determinism | `tests/test_t1_determinism.py` | two runs byte-identical **+ RngBank fingerprint equality** (Brogue audit counter) **+ fixture-regeneration guard** (iter-6): a fresh regeneration into a tmp dir diffed against the committed fixtures; a divergence with unchanged `schema_version` = fail. The committed fixture's header `schema_version` must equal the version derived from the current `schemas/event.schema.json` `$id` — a schema bump without a fixture regen fails here. |
| T2 | replay | `tests/test_loop.py::test_t2_fold_equals_runtime_projection` | `fold(log) == state`; the simulator's incremental projection and a fresh fold of the committed log produce equal state (EventStore projection equivalence) |
| T3 | blind-NPC | `tests/test_knowledge.py` (+ `tests/test_blind.py` — the phase-4 extension, §1.3) | zero knowledge leaks on the suite; UAP motivation-hole crosswalk designs the cases (an NPC with no record for a fact cannot act on it; suspicion-from-absence is illegal without an `inferred`-channel record cause-chained to the trigger event); blind-1 (iter-63) extends the law to the phase-4 surfaces — mode B + retrieval outputs under the zero-leak law |
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

### 1.3 T3's phase-4 extension — the blind-NPC leak suite (blind-1, iter-63)

The phase-4 exit criterion ("0 leaks on the blind-NPC suite",
`ROADMAP.md` §2) reads T3's zero-leak law over the phase-4 surfaces:
mode B briefs, the retrieval ladder's outputs, and the live session
wiring. Owner: `tests/test_blind.py` (the dir-2 instrument precedent);
the suite core — every declared actor at the selected beat windows —
stays in `tests/test_scene.py` (scene-1's acceptance pin).

The instrument: pure test-side folds, never the engine's own code
paths (a checker that shares the checked code cannot catch its bugs).
Every scene_delta line is backed by a perceived event count-for-count
(the multiset law — the line's own `(t, type, actor, target)` bytes,
never a coarse `(t, type)` key); every recalled_facts line (raw or
belief) maps to the knower's own fold — the raw line's exact
`(at, channel, fidelity, knows)` quadruple, the belief line's exact
`(token, sources, cross)` triple (the provenance IS the leak signal,
not just the token); every retrieval fact row maps to the named
knower's record. The adversarial form: the omniscient query (every
`knows` token on the whole log — the query that knows the future) and
the `knower=None` probe — the known_by boundary must hold under
maximal input. The teeth law: planted leaks are flagged (crafted
records + the pinned seed-125 cross-knower divergence) — a checker
that cannot fail is decoration.

The sweep: the 10-seed day1 family (seeds 120..129, the corpus-price
witness pattern) + the committed golden fixture, EVERY log prefix
(any prefix is a legal assembly state — the log is append-only),
every declared actor + the player; the live drain's every emitted
call document is verified against its own anchor-addressed prefix
(`anchor` = the emission-time event count; append-only makes the
final log's `events[:anchor]` the emission-time log — the document
carries its own log address): composition byte-exact (the knowledge
blocks are the document's own knower's assembly, the query line IS
`recall_query`, the retrieval rows ARE the ladder's top-3) plus the
leak law independently. Zero leaks measured; the suite runs ~3 s.

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

> The per-landing re-measurement records (iter-37..58 — every phase-3/4
> landing's pacing / grammar / content A/B, each naming its pinned unit
> tests + its D-row) live in git + the D-065..D-093 family rows + TASKS'
> phase-3/phase-4 backlogs — the single owners. The instrument
> definitions above and below are the reusable half.

Extended at iter-107 (the risk-synthesis riders — the drama tuning
turned into data): the table gains three measurement surfaces. The
**payoff latency** (D-140): `core.metrics.payoff_latencies(events)`
pairs every director release with its seeding event via
`provenance.cause_hook` (FIFO per tag — exact under the director's
`(release_threshold, seeded_at_tick)` pick law; rejected releases
count, an attempt is a fact), reporting p50/mean/max + the tick
histogram + the released-run share; `[]` on the OFF arm by
construction. The **beat tension**: `core.metrics.beat_tension_profile
(pack_rules, events)` — the same beat-window axis the stretches walk,
per window the sum of its events' importance weights (low 1 / medium
2 / high 3, ALL events), the table reporting the per-run mean +
variance across runs (the flat-drumbeat vs burst-and-quiet rhythm
stat). The **ablation arm**: `--systems-minus <name>` runs the pack
minus one mechanic's arming block — block-scoped by necessity (the
68a law; the systems-table rows are interlocked, not independently
removable), the removable set MEASURED (lint + 3-seed runs):
urgencies, weather, on_action, reflection, secrets, factions; the
director's ablation stays `--directors off`. First pinned finding:
the urgencies-minus world has no beat axis at all — no tension
profile, and the beat-driven release cadence dies with the block
(the whole director loop hangs off `urgencies.beat_ticks`) — pinned
in tests/test_balance_harness.py. The corpus price: the schema
version line of the T1 golden fixture alone (the 0.1 → 0.2 additive
bump, `provenance.cause_hook`), regenerated in the same iteration per
§3. The blast-radius drift guard for the state vocabulary landed the
same iteration (tests/test_drift.py — the systems table ⇔ the metrics
prefix map, the observed corpus pinned).

## 7. leg-4 offline chronicler acceptance (iter-64, D-093)

The mode-F chronicler suite (`tests/test_chronicle.py`; the tool:
`scripts/chronicle.py`; architecture owner `docs/blueprint/phases.md`
§4 "Choricler mode F offline"; the donor pattern set
`docs/ref/duckdb.md`). NOT a gate test — an offline tool's acceptance
suite, the balance-harness §6 precedent. Runs only with the
`[chronicler]` extra installed (`pytest.importorskip` — the pure-dev
env stays green, the module skipped by design).

The laws under test, each by an independent stdlib fold of the same
log via `core.log.read_log` (the blind-1 instrument law — never the
checked pipeline's own code):

- **The count gate**: every log line minus the header appears as a
  row; a line DuckDB cannot serve but the file holds (truncated JSON)
  = ChronicleError, nothing written. A line-aligned prefix is a legal
  log (append-only) and archives as its own event count.
- **The archive is the log**: `events.parquet` ids == read_log ids,
  order and count; always the twelve canonical columns (typed NULLs
  for absent fields — a header-only log is handled uniformly).
- **The window-diff law**: `state_diffs.parquet` == a pure Python
  LAG fold per (entity, prop) ordered by (t, event id) — `prev_to`,
  `continuous` (NULL on a state's first change).
- **The summary cross-check**: every `chronicle.sqlite` table
  (facts_summary / state_current / type_histogram /
  knowledge_summary / chronicle_meta) equals the stdlib fold's
  numbers.
- **Determinism (INV-2's spirit, offline)**: two full runs — every
  artifact byte-identical; the manifest is content-derived only (no
  wall-clock, no absolute paths; the exact key set is pinned).
- **The write ladder (L12)**: attach and stdlib paths produce
  logically identical summaries; the manifest's `write_mode` records
  which ran; `autoinstall_known_extensions=false` — the chronicler
  never phones home (the ref's offline law, INV-4's spirit).
- **D-012 executable** (in `tests/test_architecture.py`, runs
  everywhere): the runtime import graph (core/sim/render/brief/cli)
  imports only stdlib + local packages + ImportError-guarded optional
  probes — duckdb or any future third-party root fails loudly.

### 7.1 depth-4 fold-checkpoint acceptance (iter-80, D-114)

The checkpoint suite (`tests/test_checkpoint.py`; mechanism owner
`core/checkpoint.py`; builder `scripts/checkpoint.py`; design
`docs/blueprint/phases.md` §5 "Fold checkpoints"). Runs everywhere
(stdlib only — no extra, unlike §7's `[chronicler]` gate): 1352
passed + 1 skipped. NOT a gate test — an offline derived-artifact
family's acceptance suite, the §7 precedent.

The laws under test, the rollback law cross-checked against the LIVE
runtime projection (the blind-1 instrument — the Simulator's
incremental state is an evolution path the checkpoint code never
sees):

- **Rollback = snapshot + tail replay**: restoring at any offset and
  replaying the tail reproduces the full fold AND the live runtime
  projection (the three-way agreement); offset 0 is the initial
  projection; restore is loud on a truncated log, and a tampered
  snapshot goes loud on the first diverged-prop tail event
  (apply_event's from_-net, INV-1's own net).
- **The re-fold law**: verify/verify_all catch a tampered snapshot, a
  mislabeled offset, an out-of-bounds offset; verify_all is the batch
  shape (one pass, all offsets) and rejects duplicate offsets.
- **The anchor teeth** (the anchor lives in the index, never an event
  in the truth): load_checkpoint rejects an edited artifact (sha
  mismatch), a missing file, a re-filed offset; read_index rejects
  unsorted/wrong-keys/bad-digest hand edits; from_bytes rejects every
  shape drift.
- **Append-stability** (INV-5): the prefix digest of offset K is
  unchanged when the log grows; it equals sha256 over the first
  1+offset raw lines; loud on a short log.
- **Byte-determinism**: the canonical serialization is exact (sorted
  compact JSON), two builder runs produce identical artifact + index
  bytes.
- **The builder CLI**: default = the single end checkpoint; the
  cadence law (0, N, 2N, … ∪ the end); pack mismatch and a malformed
  log exit 1 with nothing written (the count-gate spirit).
- **The runtime consumer** (iter-106, D-139 — `Simulator.resume`'s
  fast-path, wired from `tests/test_resume.py`): a resume over
  artifacts that anchor cleanly restores the projection as snapshot +
  tail and the resumed log stays byte-identical to the uninterrupted
  run (the fold path and the checkpoint path answer the same state —
  the re-fold law, at runtime); a foreign index, a mismatched prefix
  digest, or a corrupted artifact is loud (exit/raise, nothing
  guessed); ABSENT artifacts are normal operation — the plain fold,
  never an error.

### 7.2 depth-5 worldgen acceptance (iter-81, D-115)

The worldgen suite (`tests/test_worldgen.py`; mechanism owner
`core/worldgen.py`; lint `core/pack.py::_worldgen`; genesis wiring
`core/loop.py::open`; design `docs/blueprint/phases.md` §5 "Ordered
generator passes"). Runs everywhere (stdlib only): 1378 passed + 1
skipped. NOT a gate test — a mechanism family's acceptance suite, the
§7.1 precedent. The committed pack is UNARMED (the 68a pattern): the
unarmed arm of every A/B pin is the committed pack itself; the armed
arm is the crafted twin (the `worldgen` block + the `world_history`
template line, bands calibrated so seed 42 spans the whole biome
vocabulary).

The laws under test:

- **The stream law** (the D-079 family's fourth member):
  `worldgen:<pass>` content-addressed, injective over the closed
  ":"-free PASS_ORDER, lazily registered, per-seed derived; the
  closed-set tripwire survives for non-family names; the one legal
  nesting is inside the assured substantive scope (never the
  reverse).
- **The unarmed law**: no block → `(None, ())` before any stream
  touch (no lazy registration — `count` is a KeyError), zero draws,
  the committed run stays v0.1 (no genesis events, `world` None).
- **The integer discipline**: every model value an int in bounds
  (sites, height 0..9999, moisture, flow) — the Azgaar float-drift
  refusal made executable.
- **The pass laws**: same seed → same model, different seed →
  different; the lattice count (extent//spacing)²; the relax round
  moves sites in-bounds; the biome vocabulary closed with the
  coastal rule structural (band-1 + an ocean neighbor); the
  watershed flow/rivers at the threshold; capitals + nearest-region
  growth; the chronicle capped (events_max), years ascending inside
  [1, years], kinds closed, hooks declared.
- **The claim gate's first legal caller**: commit on an empty log;
  no_op skipped; slot_conflict refused with the cause chain —
  world_formed carries ONLY the committed claims, the refused list
  rides the outcome (never-empty keys only when non-empty).
- **The genesis integration**: the world forms at open time (before
  any player step), the first genesis event is the run-start (cause
  null), the chain is linear, the PC's first event chains to the
  LAST genesis event; the director's buffer holds exactly the
  genesis hooks; the claims live in the projection AND replay
  through the fold (INV-1); NO knowledge records on any genesis
  event (the DF epistemology-empty discipline); same seed →
  byte-identical logs; **the isolation law** — the armed arm's
  substantive fingerprint EQUALS the unarmed arm's (the corpus price
  of worldgen is the genesis events alone).
- **The lint + backstop family**: closed vocabularies at every
  level; the range laws; the template closure (the genesis event
  type is pack vocabulary); the declared-hook law; the claim
  double-claim family (modeled slot, scene_detail overlap, duplicate
  pair, site bounds, unknown location); the runtime backstop
  (WorldgenError naming the offender — KeyError/IndexError never
  leak).

## 8. testproto — the intermediate-build LLM-integration protocol (iter-68, D-098)

The fork closed by decomposition, not election: the three candidates
(bg-7's one-shot probes, the phase-gate heartbeat, the adversarial
simulacrum) answer three different questions — what the real loop
does, whether it drifted since the last gate, whether the boundary
survives the worst case deterministically — so the protocol runs all
three, over ONE pinned corpus set and ONE metric vocabulary. Protocol
contract owner: this section; verdict: D-098; live runner: `bg-8`
(TASKS, owner-gated, tracks bg-7). NOT a gate test — the §6/§7
acceptance-instrument precedent; nothing executes until bg-8 lands.

### 8.1 The three layers (what each measures — and nothing else)

| Layer | Runs | Measures | Structurally cannot |
|---|---|---|---|
| 1 Contract (simulacrum) | in-repo pytest, every commit; INV-4-clean (scripts, never calls) | the boundary under scripted worst-case repliers: the refusal ladder (REFUSED lines, ≤2 regens, the L12 dry floor), the reply gates (shape, closed alternatives, enum/texture-verbatim), the world-answer law (§8.3), injection immunity (the reply is data), OCC/pin/promotion under degraded replies | model quality, distributions, latency, window rot — no model exists here |
| 2 Live probes (bg-7/bg-8 runner; outside the repo, Rule 9) | on demand; a real engine on real hardware | output distribution (utterance → grammar alternative), refusal/confabulation rates (real denominators), context pressure (brief token distribution vs the ~8–16k effective window, TECH_NOTES §2), latency/hardware fit, the Cyrillic Script Tax | regression protection — a snapshot, not a fence; determinism |
| 3 Heartbeat (a protocol, not a harness) | each phase gate: Layer 2 re-run over the SAME pins + metrics | the trend line — drift across engine/model/hardware changes | blocking anything: track B never blocks track A (ROADMAP §1); a run that cannot happen records a gap row, the gate proceeds on track-A evidence, the heartbeat is advisory to engine-1 |

The contract-vs-live split: what the boundary decides (gates,
refusals, no-op facts) is Layer-1-testable without the model; what a
model emits (mapping quality, rates, pressure, latency) needs the
live partner. Layer 1's scripts are CALIBRATED from bg-7 transcripts
(the anti-tautology law: a same-author adversary is the trap reborn).

### 8.2 One corpus, three sources (the anti-trap law)

"Is the corpus a self-diagnosis trap?" — YES by construction (corpus
and gates share one author) unless the corpus grows from sources that
author did not see. Three pinned sources, committed data under
`tests/fixtures/` (replies are fixtures, never calls — INV-4-clean):

1. **Author-declared cases** — the existing families (the 105-case
   narrator corpus; the 51-utterance parse corpus).
2. **The deviation corpus** (the owner's 2026-09-07 clarification —
   off-script play as a first-class protocol member), authored to
   break the boundary's comfort, never to confirm it:
3. **Live transcripts re-distilled** — bg-7/bg-8 outputs become new
   pinned cases; their confabulation shapes calibrate Layer 1.

| Family | Probes | The honest outcome |
|---|---|---|
| F1 verb paraphrase | "have a good look at" → examine; "loiter" → wait | a mapped intent or a question |
| F2 oblique/role nouns | "the barmaid" / Cyrillic "барменша" → the serving maid / the barkeep | semantic mapping or the question — never a guess |
| F3 invented names | the prose floor's input-side twin (a ghost noun cannot feed, PARSER_SPEC §2) | a disambiguation question or no_intent |
| F4 unmodeled actions | "dance on the table" — world-touching but no verb exists | question / no_intent — the honest answer family |
| F5 register noise | Cyrillic, casing, filler — the script-tax family | the gates are script-agnostic; the mapping cost is Layer 2's |
| F6 injection payloads | instructions inside player text and reply prose | data-not-instruction (VISION §5); refused, never executed |

Growth law: the corpus grows from measured failure, never the author's
imagination alone. The first measured gap: the grammar snapshot's noun
surface is the entity name only (PARSER_SPEC §2) — role/alias text is
pack data the snapshot does not yet carry; the fix (pack-declared
aliases, engine-generic, INV-3-clean) is a candidate bg-8/engine-1
landing, routed to the backlog, not ahead of the numbers.

### 8.3 The world-answer law (the living-world metric)

The measurable form of VISION §5 ("player input is data; the world
answers"): every deviation-corpus utterance that carries world-touching
intent must end in exactly one of — a committed event (attempts
included: `intent_rejected` is a fact, PARSER_SPEC §5), a surfaced
disambiguation question, or a `no_intent` verdict; a silent drop, a
crash, or an off-grammar leak reaching the player is a measured
failure with a pinned case. The metric is answer coverage; the target
rides bg-7's numbers, never a guessed threshold.

### 8.4 The runner boundary (Rule-9 shape)

The repo exports the pins, the metric definitions (this section), the
prose-surface instruments (`brief/scan.py` — VALIDATION_SPEC §2.1's
prosefloor-2 clause, iter-72/D-104: `relation_attribute_tokens` +
`modeled_vocabulary`, the lowercase assertion surface and its
grounded/unmodeled split — the weaker-engine arm's lowercase-gap
metric, its calibration baseline pinned in `tests/test_scan.py`), and
the boundary contracts (PARSER_SPEC, BRIEF_SPEC §7.1, VALIDATION_SPEC
§7.1); the runner owns the engine, the transcripts, the hardware.
Transcripts flow back one way — re-distilled into corpus rows (§8.2
source 3) and TECH_NOTES numbers; the runner never writes repo files.
Landed bg-8 (D-109): the deviation corpus is a committed pin
(`tests/fixtures/deviation_corpus.json`, Layer 1's regression teeth in
`tests/test_deviation.py`) and the heartbeat's first run is the §8.5
baseline row — the numbers live in TECH_NOTES §11, never restated here.

### 8.5 The heartbeat ledger (Layer 3 — the trend rows)

One row per heartbeat run; a missed family records a gap row, the gate
proceeds (§8.1 Layer 3's law). The metrics per row: engine_ok, raw gate
validity → after one re-ask, alternative mix (intent/question/
no_intent), full intent agreement vs the pins, the refusal-family
census, the deviation coverage, and the per-component latency
(iter-107, the risk-synthesis §9 rider — FIRST-CLASS COLUMNS): one
p50/p95 pair per pipeline component — **tick** (the loop's sim tick),
**fold** (the log → projection fold), **brief** (the mediator call
assembly), **parse** (the parser-door cycle, repo-side), **generate**
(the external engine's call — the runner's own clock, Rule 9). The
component cut is the latency BUDGET's owner: each future SoW engine
decision reads which component eats the p95, never a single end-to-end
number that hides it. Numbers' owner: TECH_NOTES; this table carries
the trend pointers only. No live row carries the columns yet — the
standing gap row below; the first bg-9+/engine-1 run populates them
(the runner computes p50/p95 with `statistics.quantiles`, n≥4; a
smaller n records the raw min/median/max with the gap noted).

| Run | Date | Engine | Validity raw → 1 re-ask | Mix i/q/n | Agreement | Latency p50/p95 (tick/fold/brief/parse/generate) | Trend note |
|---|---|---|---|---|---|---|---|
| bg-7 | 2026-09-07 | glm-4-plus API | 79.5% → 88.6% | 29/9/6 | 16/30 full | — (gap: the one-shot probes carried no component clock) | the one-shot probes (TECH_NOTES §10) |
| bg-8 | 2026-09-09 | glm-4-plus API | 84.4% → 93.3% | 32/4/6 | 20/35 full, 35/45 alternative | — (gap: the end-to-end p50 1.1 s / p95 6.3 s recorded, components unmetered — §11) | the baseline row (§11): refusal families DRIFT (unknown-keys → texture-reference), question share halves; deviation coverage 34/34, honest 17/36 |
| engine1-e4b | 2026-09-21 | Gemma-4-E4B Q4_K_M local (llama-server b11064, GBNF) | 98.0% → 98.0% | 50/0/0 | 15/51 full | tick 2.3/3.2 · fold 0.7/1.1 · brief+parse 1.1/1.6 (one measured column — the door's emit_call; the split the gap) · generate 537/706 ms | the grammar lifts raw validity above both API rows; the mix collapses to all-intent (the aggressive mapper — TECH_NOTES §13.1); the deviation re-distillation: honest 18/36, the first local world-answer leak 33/34 |
| engine1-q9b | 2026-09-21 | Qwen3.5-9B Q4_K_M local (llama-server b11064, GBNF) | 96.1% → 100% | 21/1/29 | 6/51 full | tick 1.5/4.9 · fold 0.6/0.8 · brief+parse 1.0/1.3 (the same gap) · generate 470/714 ms | the re-ask rescue closes validity; the mix inverts (the cautious assistant declines 29); deviation honest 15/36, coverage 34/34; the gate-valid protocol echo pinned (§13.1) |

Gap rows standing: the 27B GBNF parse arm + the one-model-constrained
A/B (CONTRACTS §4.3 arm a — the owner's next station run, now through
the LANDED surface: the `--engine` session + the repo-side grammar,
iter-177/D-193); the brief/parse component split (the battery's
emit_call measures the door's one repo-side call — the landed session's
engine cycle is the surface that owns the split, its numbers the next
heartbeat's); the API-side prose families (ii)–(v) (rate-limit
economics at bg-8 — the LOCAL band measured them: E4B all-dry, Q9B
6/8, §13.1). Discharged by the engine-1 runs: the {3–8B, GBNF} arm
(both rows), the per-component p50/p95 columns (both rows), the
per-family latency distribution (§13.1 — no Cyrillic latency penalty at
this band), the grammar's live-backend compile check (round 5's live
`--engine` session at an off-plan 12B: grammar accepted + enforced
through the landed wiring — §13.1).

## 9. Claim → instrument selection grammar (intake-26, iter-138 — research-derived, a routing aid, never a gate)

> Source: the intake-26 block (`docs/blueprint/phases.md` §6 — the routed
> record and the full lens/prism catalog; D-171). The compact form is
> adopted here; the catalog is never duplicated (D-024). What this section
> answers: the repo does not lack verification instruments — it lacked a
> compact answer to "which existing instrument falsifies THIS claim"
> (iter-137's audit re-derived its verification form from scratch; the
> intake family's verdict tables each re-derived the instrument mapping).
> A **lens** names what property is judged (the question); a **prism**
> names the controlled perturbation or comparison that reveals it (the
> experiment). One instrument serves many lenses; one lens may need
> several prisms. Select the smallest pair that can falsify the claim —
> never run every test for every change.

**The claim packet** — the reusable verification record for a substantive
claim; a build row's verification plan rides this form (iter-137's A–H
ledger is the standing instance of the packet's shape):

```text
Claim / Problem / Lens(es) / Prism / Scenario + corpus /
Oracle / Falsifier / Counterexamples /
Expected evidence / Observed evidence / Epistemic class / Disposition
```

The **oracle** must be an observable condition tied to the canonical
substrate (door answers, RNG fingerprints, projection properties — never
prose). The **falsifier** must state what would make the claim false. A
plausible description without either is not evidence. The disposition
vocabulary stays the repo family (CONFIRMED / PARTIALLY CONFIRMED /
REJECTED / UNRESOLVED / DEFERRED); no numeric quality score — a scalar
erases the diagnosis the lenses preserve. An **ablation arm** must
demonstrably exercise the target subsystem on the run horizon before
its delta is read — a zero-delta arm over an unexercised subsystem is
a failed experiment, not zero causal effect (the empty-ablation rule,
intake-34's measured lesson).

| Claim shape | First prism | Strong follow-up | Standing instruments (the oracle owners) |
|---|---|---|---|
| "this creates new depth" | one-knob perturb | composition crossing | balance A/B (§6), M1/M3, the depth battery (the F3 form + the three arms, `phases.md` §6) |
| "this is a meaningful player decision" | remove | knowledge restriction / same-seed fork | `--systems-minus`, the door-surface battery, the blind suite (§1.3) |
| "actors only know permitted facts" | knowledge restriction | stress corpus | blind-NPC suite (§1.3), the deviation corpus (§8.2), `knower` boundaries |
| "this does not perturb unrelated runs" | same-seed fork | one-knob | T1/T2, `mechanics.py blast`, the RNG fingerprint |
| "the consequence remains meaningful later" | horizon extension | composition crossing | longrun, eventless stretches, payoff latency (§2) |
| "this system is not dead / not overactive" | horizon extension | same-seed fork / one-knob | pack lint, the balance harness (§6), M1–M5 (§2), the corpus |
| "this outcome is explainable" | same-seed fork | composition crossing | `mechanics.py trace/why`, the provenance family, drift tables |
| "this cannot escape its boundary" | stress corpus | independent re-derivation | the validator golden set, pack lint, cap/floor tests, stoplists |
| "this parameter earns its complexity" | one-knob | remove | the ablation family, the offline one-knob ranking (intake-16's spike record) |

Two standing oracle laws the table carries:

- **Independent re-derivation.** A checker that shares the
  implementation's mistake is not an oracle. Compute the claimed result
  by a path that does not share the validated path: runtime projection vs
  fold/checkpoint refold; live loop vs shadow replay; committed fixture
  vs re-generated run (the checkpoint/blind/mechanics families' shared
  lesson — the strongest transferable rule of the corpus).
- **Order probes are contract-bound.** Perturb an ordering only where the
  owning spec declares the operations commutative; where order is
  semantic, the expected result is NOT invariance — derive the oracle
  from the owning contract first (the D-039 crossing law is the standing
  instance: co-occurring ticks fire coarsest-first by design).

The lenses' own quality bar (intake-26 §12 — the research method's five
questions applied to any future lens): principle / form / quality /
transfer / combined design. A matching name is not proof; a useful form
with unproven quality stays PARTIAL. A new lens or prism enters this
table only after one claim packet used it (the first-consumer law).

