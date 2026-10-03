# CONTRACTS.md — Pre-Implementation Contracts

> What this file is: the compact pre-implementation contracts for the
> contract-write rows (intake-29/D-175's closing proposal, written
> iter-144/D-177 under the owner's delegation). A contract pins what a
> row's build must satisfy BEFORE it starts: the decisions the row
> leaves open (each grounded in standing code or law), the invariant
> set, the falsifier (TEST_PLAN §9's claim-packet form), the minimal
> test set. What it is NOT: the row's spec — the spec fires
> just-in-time at the row's start, FROM experiment results
> (SPECS_BACKLOG's header law); the contract is the boundary, the spec
> the implementation's own words. Ownership never moves: TASKS owns
> WHAT/WHEN (the ORDER owner decides), the row keeps its acceptance
> criteria, this file owns the pre-implementation HOW-boundary. When a
> row's build lands, its spec absorbs its contract by reference (never
> restated, D-024) and the section here collapses to a one-line
> pointer. Cap-law: `docs/*.md` ≤600 lines, substance-filtered
> (AGENTS §6.1).

## 1. roads-1 — LANDED (iter-145, D-178)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-145 + D-178 + worklog
> iter-145 own the landing record — the pass
> (`core/worldgen.py::_pass_roads`), the one shared read
> (`core/roads.py::exits`), the lint, the §9 claim-packet evidence.
> The contract's own pinned decisions, verbatim, in git history at
> the iter-144 commit.

## 2. res-1 — LANDED (iter-146, D-179)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-146 + D-179 + worklog
> iter-146 own the landing record — the substrate
> (`core/economy.py`: the account primitive, the three verbs, the
> flows on the macro cadence, the derived prices), the door's soft
> arm (`account_at_least`), the resolver (`account`), the commit
> gate's loud floor, the lint (`core/packlint/economy.py` + the
> actions/entities cross-checks), the §9 claim-packet evidence. The
> contract's own pinned decisions, verbatim, in git history at the
> iter-144 commit.

## 3. since-1 — LANDED (iter-147, D-180)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-147 + D-180 + worklog
> iter-147 own the landing record — the fold
> (`brief/since.py::ReunionFold`: the per-entity encounter epochs,
> the apart-window deltas, the reader's apart-born records), the
> cards' since-segments (BRIEF_SPEC §3.4's extension, §3.9's
> amendment — the knower's own segments riding the shared cards),
> the pack's `since_lines` vocabulary + its lint, the §9 claim-packet
> evidence (the fold/document/zero-price arms CONFIRMED at the
> measured band; the decision arm DEFERRED to the first consumer).
> The contract's own pinned decisions, verbatim, in git history at
> the iter-144 commit.

## 4. engine-1 — LANDED (iter-177, D-193)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-177 + D-193 + worklog
> iter-177 own the landing record — the GBNF mapping repo-side
> (`brief/gbnf.py`, the snapshot's engine-facing serialization with
> the door's shape laws encoded; PARSER_SPEC §2.1), the explicit
> adapter (`cli/engine.py` — INV-4's one-module form, AGENTS §4), the
> door wiring (`--engine`, the file contract preserved — the runtime
> engine is "the operator"), the failure→ladder mapping (§5's re-ask
> ladder + the D7 degradation rungs; PARSER_SPEC §5), INV-4 lifted
> with the AGENTS §4/§8 edits riding, the model-facing serializer
> contract now `docs/PRESENTATION_SPEC.md`'s (iter-178), the adapter
> contract tests + the golden grammar + the Layer-1 suite green with
> ZERO gate edits (the §4.3 claim packet's proof; TEST_PLAN §9's
> form). The contract's own pinned decisions D1–D8 + the invariant
> set + the falsifier, verbatim, in git history at the iter-170
> commit. The station-side remainder (the 27B GBNF parse arm + the
> one-model-constrained A/B — §4.3 arm a; the grammar's compile
> check at the live backend) lives on as TEST_PLAN §8.5's standing
> gap rows, the owner's next station run.

## 5. wb-1..N — the Workbench family (the v5.2 Redot brief, owner's 2026-09-24 call)

> Source: the owner-supplied `canonsim_workbench_v5_2_redot_2026-09-24`
> package (5 documents, external — the convenience-copy law D-024: they
> stay outside the repo, this section + the TASKS wb rows the distilled
> owners, D-200 the admission). Contract written BEFORE wb-1 starts
> (iter-215); when each wb row lands, its section here collapses to a
> pointer per the file's own law.
>
> **§-reference map (D-218, iter-237 — the corpus re-homing):** every
> `app spec §N` citation below and across the repo resolves to
> `docs/WORKBENCH_APP_LAW.md` §N (the binding distillation, the spec's
> §-numbering preserved 1:1); every Observatory-doc §N resolves to
> `docs/OBSERVATORY_LAW.md` §N; the frontend spec's §46 implementation
> ladder resolves to `docs/FRONTEND_UIUX_LAW.md` §25; the world-
> presentation contracts (the spec's §§23–31) live in
> `docs/WORLD_PRESENTATION_LAW.md`. The external originals stay with the
> owner — no repo work requires them anymore.
>
> **Redot half DELETED (iter-290/D-245 — the owner's «удаляй redot»
> call):** `workbench/presentation/redot/`, `scripts/visual_proof.py`,
> the Redot proof/contract packets (`tests/test_visual_proof.py`,
> `tests/test_shell_proof.py`, `tests/test_shell_contract.py`), the
> engine index (`docs/REDOT_ENGINE_INDEX.md`), and `Workbench
> Setup.bat` are removed; the launcher re-pointed to the web dev
> server (D-245). The landing notes below collapsed to pointers at
> iter-316's cap pass (this file's own law + D-024 — the verbatim notes
> in git history) — the Python half (scene IR, gateway, operations,
> platform) is untouched and the web client (`frontend/`, D-244) is the
> active consumer. Recovery: git history + the verbatim pack at
> `docs/frontendweb/archive/`.
>
> **Landed rows — collapsed to pointers per this file's own law + D-024**
> (the per-row landing detail: `docs/TASKS.md`'s wb rows + the worklog +
> git — never restated here; the collapse executed iter-316's cap pass,
> the verbatim landing notes live in git history at each iteration's
> commit): wb-1 the vertical seam (iter-215/216 — scene IR + scene build
> + the visual proof, the D4 double-run PNG byte-diff CONFIRMED); wb-2
> the shell + semantic-token theme (iter-217); wb-3 the
> application-operations skeleton (iter-218 — identity/artifact/
> directories/clock, 25 tests); wb-4 the inbound gateway (iter-219,
> D-201 — contract/gateway/transport, INV-4's second sanctioned module,
> 36 tests); wb-5 the minimal application operations (iter-220 —
> lifecycles/execution/models/composition, 46 tests); wb-6 the backend
> row (iter-221, D-203 — the typed BackendPort + chat.send +
> model.load/unload, 28 tests); wb-7 the live chat circuit (iter-222,
> D-204 — `scripts/workbench_app.py` the composition root + the Redot
> chat surface, 8 tests); wb-8 the managed models surface (iter-223,
> D-205 — `llama_process.py` + `--managed` + `model.states`, 17 tests);
> wb-9 the one-command model flow (iter-226, D-208 — `model_fetch.py`
> INV-4's THIRD sanctioned surface + `settings.py` + the launcher, 35
> new tests); wb-10 the zero-command owner experience (iter-227 — the
> launcher rework + the `model.import` work kind + the native picker);
> wb-11 the dispatch-lock freeze chain (iter-228, D-210 —
> model.load/unload as RUNS + the pipe drain); wb-12 the theme@0.3
> token audit + the chat follow law (iter-230, D-212). The family
> contract below stays (wb-13..N still owner-gated rows).

**Pinned decisions** (each grounded in the brief or standing law):

- D1 Runtime: Redot 26.2 LTS (`redot-26.2-stable`), Compatibility
  renderer, GDScript. The engine binary + export templates are an
  EXTERNAL toolchain (never committed); one configurable `REDOT_EXE`
  path is the single resolution point (the brief's integration §7).
  Redot project root: `workbench/presentation/redot/`; committed:
  project.godot, scenes, scripts, themes, source assets; ignored:
  `.godot/`.
- D2 Boundary: Redot owns presentation-local state only (camera,
  selection, animation playback, transient effects, caches) — never
  canonical world state, event history, semantic time, identity or
  simulation rules. The chain is
  `fixture → typed read model → Visual Scene IR → Redot composition →
  screenshot artifact`; the IR is renderer-neutral (no Node/Texture/
  UID as identity) with the v5.2 identity closure
  (`scene_ir_schema_identity + composition_seed + asset_manifest_
  identity + semantic_input_identity + composition_policy_version`).
- D3 Python side: `workbench/` is periphery (the render/cli/scripts
  class, D-046 — outside the INV-3 stoplist by the same law: entity
  ids and location ids arrive as data from the log/pack, never
  hardcoded). It imports `core/` read-side APIs only (read_log, fold,
  present_in_order — the render/chronicle.py pattern); zero canon
  writes, zero new network surfaces (INV-4 untouched: `cli/engine.py`
  stays the only network module; the future inbound gateway is an
  owner-gated row with its own contract + architecture-test exception
  when it fires).
- D4 Determinism: same semantic input + same seed → byte-identical IR
  JSON; two consecutive Redot runs in the same environment →
  byte-identical PNG (measured in-sandbox before this contract:
  llvmpipe/Xvfb, 1280x720). No wall clock, no PYTHONHASHSEED
  dependence (sha256 stable hashes + sorted/construction order — the
  INV-2 read-side discipline; no RNG draws at all in the Python half).
- D5 Status laws: the IR distinguishes
  CANONICAL | DERIVED | OBSERVED | UNKNOWN | HIDDEN | VISUAL; the
  silent collapses UNKNOWN→ABSENT, HIDDEN→ABSENT, VISUAL→CANONICAL,
  LLM-text→CANONICAL are forbidden (the brief's §7/§23 vocabulary).
- D6 Observation: the proof's artifacts (PNG + metadata JSON) are
  runtime output — gitignored, never committed; the pytest regenerates
  and compares in-run (the iter-207/209 byte-identical-on-regeneration
  pattern). Tests skip cleanly without `REDOT_EXE` (the duckdb/D-093
  pattern; CI stays engine-free).

**Invariant set**: INV-1..INV-5 all hold unmodified; the seam adds no
second semantic authority, no second fold, no second presence rule
(`present_in_order` is the one presence law, reused).

**Falsifier** (TEST_PLAN §9's packet form): any byte difference in the
IR JSON on rebuild from the same fixture; any byte difference between
two consecutive screenshot runs in one environment; any network import
or canon write in the new modules (test_architecture); any setting
word hardcoded in `workbench/` source (review — the stoplist does not
scan periphery, the discipline is the review's).

**Minimal test set**: `tests/test_scene_ir.py` (determinism + status
laws + identity closure over the tavern and province smoke fixtures);
`tests/test_visual_proof.py` (REDOT_EXE-gated: the artifact exists,
metadata carries the identity fields, the double-run PNG byte-diff).

**Family composition** (TASKS owns WHAT/WHEN; the brief's own order,
owner-gated per row): wb-1 the vertical seam (this contract's first
consumer); wb-2 the Redot shell + theme; wb-3 the application
operations skeleton; wb-4 the gateway (INV-4's owner-gated exception);
wb-5 the minimal application operations (app §32 step 5 — the
operations substrate + the run/model-discovery families over the
registered surface); wb-6 the backend row (the llama.cpp port —
chat.send's consumer, D-203); wb-7 the live chat circuit (D-204);
wb-8 the managed models surface (app §11.1's MANAGED half + the
Models surface — D-205); wb-9+ per the brief's §32/§46 ladders
(live events + reconnect/resync; persistence; the frontend rows —
inference; history/diagnostics; the CanonSim seam). Engine/API facts
for the deleted Redot half route to the archived pack's reference docs
(D-245 — the index deleted, never a repo file again); the web client
(`frontend/`, D-244) is the active consumer.

## 6. sem-1 — the semantic event validity + authority contract (review-C1/D1, the confirmed queue's head; the DEFINITION landed iter-316)

> Owner-confirmed 2026-10-03 (iter-315's queue). R0–R1 definition
> only: NOTHING here is implemented — no gate code, no schema change,
> no draft field added (the row's own law). This section pins what any
> future admissibility build must satisfy BEFORE it starts; the
> implementation is NOT a standing row — the owner opens it after
> accepting this contract (the runtime-promotion gate: a named
> consumer + a measured native limit + the falsifier below).

**Pinned decisions** (each grounded in standing code or law):

- **S1 — one semantic owner.** The resolver circuit — the intent door
  (`core/intent.py`: loud shape validation, preconditions, checks,
  OCC) + the resolver registry (`core/resolvers.py`) + the loop's
  mechanic producers (the map below) — stays the SOLE decider of what
  an event means: its type, outcome payload, effects. The
  admissibility gate never re-derives meaning, never re-runs a
  precondition or check, never recomputes an outcome, never edits a
  draft (review-D1; INV-1's writer monopoly untouched).
- **S2 — the declared effect surface.** Admission is checked against
  a declaration that exists INDEPENDENTLY of the draft instance: per
  event type, (a) the legal actor classes, (b) the allowed effect
  surface — the state-change family (entity-kind × prop pattern; or
  NONE for knowledge-only/no-op types), the knowledge channels, the
  hooks vocabulary, (c) the postconditions — pure predicates over
  (projection, draft, pack). The declaration lives in pack data (the
  action's `events` branches + effect blocks — `status_effects`/
  `balance`/`ignition` — and the templates' closed type vocabulary
  `Pack.event_types()`) + the mechanic modules' named constants
  (`STATE_MUTATING`, `REJECTION_EVENT`, the economy verbs + the
  account-stock props, the macro/calendar turn types + actor `world`,
  the weather/transition/crime/group/knowledge/leverage families) —
  NEVER per-draft, never derived from the producer's output at run
  time (the static twin: the packlint admission family already reads
  the pack-side half, D-152).
- **S3 — the authority vocabulary (emit-side).** The actor classes the
  producers already imply: the player entity, npc ids, `world` (the
  ambient/clock/genesis family — macro/calendar/weather/worldgen/economy
  aggregates), group ids (the condensation aggregates). An event type's
  declared authority = the legal actor classes for THAT type (e.g.
  `year_turns` → `world` only, `core/macro.py`'s own declaration;
  `intent_rejected` → the front door's own emission). auth-1 (D9) owns
  the INPUT-side pipeline (interpretation → classification →
  authorization); sem-1 pins only the emit-side check — the two
  vocabularies must never contradict (the namespace fence, the
  package's §5).
- **S4 — the gate.** Pure and non-resolving:
  `admit(draft, declaration, projection) → ADMIT | REJECT(reason)` —
  total, no writes, no RNG, no queue or resolver calls; it checks ONLY
  authority (S3) + the declared surface and postconditions (S2).
  Placement: INSIDE `_commit`, after the existing delta gate, before
  `writer.append` — ONE door, one more check (D-035's form extended;
  never a second door, never a second writer).
- **S5 — the RED semantics, two lanes.** An INTERNAL producer violation
  (a resolver/mechanic bug) fails LOUD — the pre-write `ValueError`
  form, the log stays clean (the delta gate's own law, KI#13's form).
  An EXTERNAL candidate (the mediator/engine path — a model-mediated
  draft) is refused SOFT — the candidate dies at the door, never an
  append of the unauthorized effect; what gets logged is the
  attempt-fact per the mediator's own vocabulary (PARSER_SPEC §4/§6's
  split, the emit-side twin). The lane is the producer's side of the
  door: internal = trusted-but-buggy, external = untrusted-by-contract.
- **S6 — no tautology.** The gate's reference is the DECLARATION (S2)
  — an artifact independent of the draft instance. Forbidden:
  comparing the draft to itself (its own fields as its reference), a
  checker derived from the producer's output at run time, "valid
  because the resolver produced it". The falsifier below is the
  executable disproof: the SAME declaration that admits the unmutated
  run rejects the mutated arms.
- **S7 — the `_commit` probe is a contract gap, not a production
  exploit.** Verified live at the iter-315 triage and re-proven by the
  falsifier at iter-316: `core/loop.py::_commit` gates deltas + schema
  + chain, never a declared effect surface or authority. No production
  path feeds hand-mutated drafts through the private door — every live
  producer is deterministic code over pack data; the gap is the absent
  check, not a live hole. The implementation row (the owner's call)
  closes it.

**Producer map at HEAD** (the declaration's owners): the pack-action
producers (the resolvers REGISTRY over the action's declared branches);
worldgen genesis; the front door's rejection; the crime family
(rotations/briefings/suspicion); the economy verbs; the clock family
(macro/calendar — actor `world`); the weather family; the group
aggregates; the transitions; the knowledge transfers; leverage;
reflection/onaction/states; the director releases (through the intent
door — auth-1's side).

**Invariant set**: INV-1..5 unmodified — the gate adds a check inside
the existing door (no second writer, no log edit, no schema change, no
network); INV-2 untouched (pure, zero draws — the byte-identical replay
over an admitted-only run is the proof); INV-3 untouched (the registry's
code side carries no domain words — pack data carries them); L13/L14
(one check at one door — no new layer, no framework).

**Falsifier** (TEST_PLAN §9's packet form — the future implementation
row's first RED test; run LIVE at iter-316: seed 42, the
plumbing_smoke playscript, the probe script outside the repo per Rule 9,
the artifact md5 `228ea08bff9b87afc9761d34bb704071`): mutate a captured
producer output to stay schema-valid + delta-consistent + chain-valid
while violating the declared authority/effect → the gate MUST go RED,
no append. Both arms APPEND today (the gap demonstrated live): **Arm
A** (effect surface) — a real `wait` producer output (declared surface:
NO state changes) + an added `pc_01.position` teleport to a
non-adjacent location (from_ = the live projection, so the D-035 delta
gate passes) → appended `ev_0011`; **Arm B** (authority) — a producer
output re-typed `year_turns` (declared actor `world`) with actor
`pc_01` → appended `ev_0012`; the polluted log then FOLDS CLEANLY (T2
holds — `pc_01.position` == the teleported value): a schema-valid log
encoding an unauthorized semantic effect, exactly review-C1's risk.

**Minimal test set** (the implementation row's, not today's): the two
falsifier arms RED→GREEN with NO append; the positive control — every
committed playscript corpus run admits 100% of its drafts, the golden
T1 fixtures byte-identical (zero false positives); the tautology guard
— flipping the DECLARATION side (e.g. declaring `wait` position-writable)
flips Arm A's verdict, proving the gate reads the declaration, not the
draft; the loud/soft split (S5's two lanes); INV-2 — byte-identical
replay over an admitted-only run.

**Deliberately NOT done here** (the row's own fence): no semantic
checker implemented, no schema or draft-field change, no second
resolver, no authority pipeline (auth-1's), no speech-act admission
(speech-1's), no representation or LLM-boundary work (core-1-C4's —
the namespace fence: review-C1 ≠ TASKS::core-1 C4).

## 7. caus-1 — the causal sufficiency contract (review-C2/D2; the DEFINITION landed iter-317)

> Owner-confirmed 2026-10-03 (iter-315's queue — the T2 half of the
> package's own T1+T2 sequence, sem-1's natural pair). R0–R1
> definition only: NOTHING here is implemented — no field added, no
> schema change (the row's own law). The implementation is NOT a
> standing row — the owner opens it after accepting this contract (the
> runtime-promotion gate).

**Pinned decisions** (each grounded in standing code or law):

- **K1 — the causal spine, three parts, no graph.** `primary_cause` +
  `necessary_supports[]` + `provenance`. Today's `cause` field IS the
  primary-cause slot — the writer-enforced chain link (`core/loop.py`
  sets it to `writer.last_id` at build, the chronological-chain law;
  the hook family's `cause_hook` (D-140) and the OCC's
  `based_on_event_seq` are the per-family attributions the spine
  keeps). `necessary_supports[]` is the NEW declared claim: the prior
  events WITHOUT EACH the outcome becomes unreachable. `provenance`
  stays the evidentiary lineage block (seed / `cause_intent` /
  `cause_hook` / `assignment_tick` — the temp-1 primitive, D-236) —
  NEVER a causal claim (review-D2: provenance is lineage, not a
  second causal ontology).
- **K2 — counterfactual necessity (the definition).** Support X is
  NECESSARY iff the same-seed ablation of X (removing X's producing
  step/mechanic from the run's inputs) makes the claimed outcome
  UNREACHABLE: no event with the outcome's identity (type + actor +
  the material state-effect family) can occur in the re-derived run —
  replacements (`intent_rejected` and kin) do not count as the
  outcome. Enabling-but-unrequired, correlated, or downstream events
  are NOT necessary — no matter how informative they are.
- **K3 — necessity vs optional evidence, the split.** Optional
  evidence = everything the outcome's audiences observed or the fold
  consumed (perception records, ambient context, downstream
  reactions) — it lives where it already lives (knowledge records,
  the projection, the outcome payload), NEVER in `supports`. The
  discriminating test is the ablation pair: evidence-removal leaves
  the outcome REACHABLE (possibly shifted in tick or branch — the
  deterministic streams shift, reachability is the invariant);
  support-removal kills it.
- **K4 — the ablation battery, off-line only.** The verification
  instrument is the landed same-seed BASE/PERTURBED pair form
  (`scripts/divergence_probe.py`, D-235 — the semantic_diff oracle +
  the `cause`-ancestry walk). The battery runs over runs/logs,
  NEVER inside the tick loop: no runtime re-derivation of necessity
  (sem-1's S1 twin — the second-resolver ban holds for causal claims
  too).
- **K5 — the producer declares, the battery verifies.**
  `necessary_supports` is a PRODUCER-DECLARED claim: the
  resolver/mechanic names the events that established the facts its
  resolution materially used (the read-set × the establishing events
  — the loop's `_last_change` index (L3, D-050) is the existing
  `(entity, prop) → tick` derivation seed). The declaration is
  verified by the ablation battery over the corpus; a declared
  support that survives ablation (the outcome still reachable) is
  REFUTED — RED — and an omitted-but-required support is the
  completeness gap the battery reports.
- **K6 — compatibility + the no-DAG law.** INV-1: the supports ride
  the event document (an additive provenance-family field — any
  schema bump is the implementation row's business through AGENTS §8
  stop&confirm, never this definition). INV-5: supports reference
  committed event ids — append-only, never edited. Current consumers
  unaffected and additive-only: the divergence probe's ancestry walk,
  the observatory's cause-as-data (LAW §12), the hook-discharge
  family (director/urgencies/factions/metrics), `brief/validator`,
  the census forward walk. FORBIDDEN: DAG storage, graph-traversal
  machinery, provenance engines, generic causal inference — the spine
  is fields + one off-line battery; full graph machinery only behind
  the runtime-promotion gate (a named consumer + a measured native
  limit + the falsifier).

**Falsifier** (TEST_PLAN §9's packet form — the future implementation
row's first RED test; run LIVE at iter-317: seed 8, the day1 theft
scenario's own steps + one inserted perception step, the probe script
outside the repo per Rule 9; artifacts md5 base `947adfb5358984f76e21
f5feb4208789` / ablate-move `ce05d72bb60ef4e94c5bf1d50ba59349` /
ablate-look `26d5e6a11c0ec032d0d2d1a0a0052a10`): the same-seed
ablation pair demonstrates BOTH directions AND the gap — BASE: the
steal outcome `ev_0007` (type `steal`, the purse carrier delta) names
as its `cause` the CHRONOLOGICAL predecessor `ev_0006`
(`look_around`), while the materially-REQUIRED `ev_0005` (the move to
the tavern — without which the steal is world-impossible) is
INDISTINGUISHABLE from the look in the outcome's own fields: the
necessity is real, measurable, and UNRECORDED (review-C2's risk —
"tree-like reduction can erase conditions required for the outcome").
ABLATE-MOVE: zero steal-family outcomes, three `intent_rejected` —
the outcome unreachable (necessity). ABLATE-LOOK: the steal still
fires — the outcome reachable (evidence, not necessity).

**Minimal test set** (the implementation row's, not today's): the
ablation battery over the committed corpus — every declared support
kills its outcome under ablation (REFUTED declarations RED), the
evidence controls stay reachable; the declaration completeness
report; INV-1/INV-5 — the supports reference committed ids only, the
append-only log untouched; the consumers additive-only (the
divergence probe, the observatory, the hook family, the validator,
the census).

**Deliberately NOT done here** (the row's own fence): no field added,
no schema change, no DAG/provenance engine, no runtime causal
checking (the battery is off-line), no rewrite of the hook/OCC
attribution families (the spine EXTENDS them, never merges).
