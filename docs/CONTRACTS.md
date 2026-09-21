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
