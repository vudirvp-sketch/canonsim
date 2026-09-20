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

## 4. engine-1 — the build contract (written iter-170, D-192, on the owner's real-backend call)

Row: `docs/TASKS.md` `engine-1` (DECIDED iter-170; this contract pins
the LANDING's boundary — the experiment + the client build). Starting
material: the owner's real-backend evidence (TECH_NOTES §13) + the
session research + the disposition (both outside the repo, the
Vantiel-handoff precedent); the design brief v2 stays a LENS (its
control plane waits on a GUI consumer — bg-6/SoW territory, D-022).

### 4.1 The pinned decisions

**D1 — the backend boundary: a long-lived `llama-server` process
behind an explicit adapter** (HTTP, `127.0.0.1`, endpoint pinned —
never assumed). The adapter owns transport, endpoint selection,
serialization, backend errors, capability translation, process
lifecycle; the application owns orchestration, acceptance policy,
operation identity. The backend process is not application state. The
file-contract frame (D-055) is the insertion point: the doors' gates
run on the reply document, engine-agnostic by construction — the
runtime engine is "the operator" (whatever reads `call_<NNNN>.md` and
writes `reply_<NNNN>.json` passes the same gates).

**D2 — semantic config, never raw flags.** The generic surface is
the typed policy set (RuntimeResourcePolicy: automatic | explicit —
never `gpu_layers` as a UI concept; ContextPolicy; ConcurrencyPolicy;
SamplingPolicy; ReasoningPolicy; StructuredOutputConstraint); the
adapter translates to llama.cpp parameters. Backend-local options stay
backend-local (the `-ngl 99` fit-refusal and the `-np`-halved
per-slot context are the measured reasons, §13).

**D3 — the reproducibility tiers, never conflated:** canonical
(INV-2, byte-identical replay) / request (the call-document bytes,
BRIEF_SPEC §2 purity) / inference (the manifest: model identity+hash,
backend build, params, grammar id, seed — the log-header/BASE_COMMIT
provenance pattern). Text-equal prompts ≠ identical model input; never
promise identical output from equal text. The seeded-local
determinism probe (same manifest → byte-identical output, n≥5) is the
experiment's arm — if it holds, weak-arm replies become pinnable
fixtures (a testproto economics change, recorded not assumed).

**D4 — reasoning is an engine/request concern** (ReasoningPolicy:
enabled / budget-when-supported / preservation / visibility), never a
presentation flag: it changes request identity, output budget (the
thinking-consumed-`max_tokens` fact, §13), parsing, latency, and
potentially structured-output behavior.

**D5 — structured output ≠ validation.** The backend constraint
result (GBNF/JSON schema) and the application validation result (the
doors' gates) are separate; grammar fixes validity, never honesty (the
guess-within-grammar class persists — F4/F5). The doors' gates stay
regardless of the engine; attempts are facts.

**D6 — the client's home + the INV-4 lift.** The experiment runner
stays OUTSIDE the repo (Rule 9, D-046 — the bg-7/bg-8 precedent,
consuming `brief/` functions headless). Repo-side engine code, when
the build lands, is periphery only (the GBNF mapping = one INV-3-clean
pure function over the grammar snapshot; any CLI wiring in `cli/`);
no engine client ever enters `core/` (the import-boundary law
D-031/D-037). INV-4 lifts ONLY at the build's own iteration, on the
owner's call, with the AGENTS §4/§8 wording edits riding that landing
— this contract is the pin, not the lift.

**D7 — the non-equivalences (I5's test form):** accepted ≠ applied;
client disconnect ≠ acknowledged cancel; partial output ≠ final
response; model loaded ≠ loaded clean (warnings = structured
diagnostics: severity/code/owner/message). APPLIED requires
effective-state observation (`/health`, `/props`, `/slots` — §13); the
engine-unavailable path maps onto the existing degradation ladders
(bg-8's 5-try precedent; the regen/re-ask budgets unchanged).

**D8 — non-goals (framework inflation refused):** no universal
BackendManager/ConfigManager, no DI container, no event bus, no
runtime plugin graph, no generic workflow engine, no universal UI
state store/ViewModel, no migration framework, no flag-for-flag DSL,
no UI component registry. The DraftConfig→ApplyPlan→AppliedEngineState
pipeline and the capability vocabulary wait on a settings-UI consumer
(bg-6/SoW, the brief v2's own §5/§7) — parked, never pre-built.

### 4.2 The invariant set

- I1 INV-1/INV-5 unchanged: the engine never writes canon; effects
  enter only through the doors as proposals (attempts are facts); no
  implicit canonical mutation on any engine failure.
- I2 INV-2 unchanged: inference sits OUTSIDE the canonical
  determinism envelope (the runner boundary, TEST_PLAN §8.4);
  transcripts flow back as re-distilled corpus rows + §13/§11 numbers.
- I3 INV-3: the GBNF mapping is engine-generic pure data (the grammar
  snapshot → grammar text); no domain words in code.
- I4 INV-4 stands until the build's own lift (D6); this iteration
  lands zero engine code.
- I5 the non-equivalences (D7) — each an observable boundary.
- I6 the observation boundary: `/health`/`/props`/`/slots` are the
  effective-state evidence; engine metadata (timings, token counts,
  stop reason) is recorded into the §13/heartbeat rows, never canon.

### 4.3 The falsifier + the minimal test set (TEST_PLAN §9, build-time)

**F — the claim packet.** Claim: "the local engine changes the loop's
economics, not its laws — the doors serve a real llama.cpp consumer
with zero gate edits." Lens: boundary-escape + the changed-economics
unit. Prism: the `{3–8B, GBNF}` arm on the owner's hardware (the
TEST_PLAN §8.5 gap rows: the 51-utterance corpus raw → 1 re-ask, the
deviation families F1–F6 with the guess-within-grammar class tallied
separately, the bg-7 prose families (ii)–(v), the per-component
p50/p95 columns tick/fold/brief/parse/generate) PLUS the four new
arms: (a) one-model-constrained (27B GBNF) vs two-model (E4B/9B
dedicated) + the swap/reload cost; (b) the seeded-local determinism
probe (D3); (c) the GBNF latency penalty (constrained vs
unconstrained, its own A/B); (d) mode-A prose at the weak arm (E4B/9B
sit below the 12–27B narrator band — measure whether they narrate at
all, or are parser-only; this bounds presentation-1's contract).
Oracle: the heartbeat row vs the two API baselines (drift is the
measured quantity) + the Layer-1 simulacra green with ZERO gate edits
+ the golden T1 byte-compare (zero corpus price). Falsifier: any
boundary gate needing an edit to accommodate the engine → the
engine-agnostic claim REJECTED; the weak arm below the bg-8 honesty
floor after one re-ask → the {3–8B} band claim REJECTED (the 14B
fallback / the 27B-constrained arm the routed alternatives).
Counterexamples: the `-ngl`-forced config (the fit-refusal family);
the thinking-on structured request (the empty-content trap).

The tests: (1) Layer-1 (in-repo, INV-4-clean) unchanged and green —
the contract's own zero-gate-edit proof; (2) the provenance manifest
row per run (model+hash, build, params, grammar id, seed) — the
§8.4/§13 pattern; (3) the adapter contract tests fire at the BUILD,
not before (health/readiness, capability discovery, serialization,
template application, reasoning mapping, structured-output mapping,
unsupported-option refusal, applied-state observation, streaming,
cancellation, stale-result rejection, shutdown, replacement, error
mapping — backend-specific behavior only); (4) the experiment's
transcripts re-distilled per §8.2 source 3; (5) the claim packet F
run — the build's own evidence, recorded at landing.
