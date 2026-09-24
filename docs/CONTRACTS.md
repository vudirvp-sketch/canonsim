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
> **wb-1 LANDED (iter-215 the Python half + iter-216 the Redot half):**
> the seam chain proven end to end — the tavern and province fixtures
> composed and captured, the double-run PNG byte-diff CONFIRMED (the D4
> falsifier), the REDOT_EXE-gated packet skipping clean without the
> binary; the landing record: TASKS iter-215/216 + the worklog + git.
> **wb-2 LANDED (iter-217):** the Redot shell + the semantic-token theme
> — `themes/workbench_theme.tres` (the §10 token ladder: the
> `Workbench/*` semantic namespace + the styled component types with
> their state sets, the §12 contrast pairs recorded in-file),
> `scenes/shell.tscn` + `scripts/shell.gd` (the code-built shell: the
> §17 nav axes — Chat/Settings live, the later axes honestly disabled —
> the Chat/Settings placeholder surfaces, the §16 status vocabulary
> strip, the §18 backend badge), the main scene switched to the shell
> (the app-entry law; the seam-proof scene now passed explicitly by the
> runner), `scripts/visual_proof.py --shell` the proof mode, the gated
> packet (double-run byte-diff CONFIRMED, the settings capture included)
> + the non-gated committed-file contract. The landing record: TASKS
> iter-217 + the worklog + git.
> **wb-3 LANDED (iter-218):** the application-operations skeleton
> (app §32 step 1) — `workbench/application/` the Python-side
> package: `identity.py` (the §9 identity closure — the five axes
> apart, sha256 content digests, the order-independent composite
> identity, `recheck()` making the mismatch law executable:
> VERIFIED | MISMATCH | INTEGRITY_UNKNOWN, never a quiet pass),
> `artifact.py` (the §10 immutable execution artifact — the frozen
> field list, the reproducibility scopes EXACT_BITWISE | SEMANTIC |
> APPROXIMATE | EXPLANATORY_ONLY + the three kinds separated, the
> request digest, the replay = NEW execution identity law, the
> strict roundtrip, zero clock imports), `directories.py` (the §16
> contract — the seven path roles, the absolute-root law, the
> startup/recovery outcome vocabulary, the errno-classifying
> probe), `clock.py` (the §17 four clock domains — MONOTONIC +
> UTC_WALL provided injectably, SEMANTIC/UI_ANIMATION named-only),
> + `__init__.py` the §27 dependency envelope (RUNTIME_DEPENDENCIES
> = empty, agreeing with pyproject). The claim packet:
> `tests/test_application_skeleton.py` (25 tests). The landing
> record: TASKS iter-218 + the worklog + git. The family contract
> below stays (wb-4..N still owner-gated rows).

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
wb-5+ per the brief's §32/§46 ladders.
