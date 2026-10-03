# Agent Intake Package — Concept Review 2026-10

**Revision:** REWORKED-v2 (D0–D11 synthesis, owner-requested update, 2026-10-03)

> **Authority:** OWNER-GATED intake material.
> This directory is the operational synthesis of the 2026-10 concept review.
> The owner explicitly requested this update; it supersedes the previous version of this package.
> Implementation remains forbidden until the owner confirms concrete task IDs.

**HEAD reference:** `528de9c5324d37a46278da4614a028f59cf83d08` (`iter-311-worldsuite`)
**Package date:** 2026-10-03
**Mode:** R0 / definition / triage only. No implementation. No phase reopen. No runtime promotion.
**core-1:** remains PARKED (owner-gated RESEARCH/POC-ONLY).

---

## 1. Master law

### D0 — Future-Reachability / Causal-Obligation Conservation

The primary design criterion for scale, LOD, locality, concurrency, recovery, director behaviour, and model interaction is:

> **A representation, execution path, optimisation, or authority transition may change representation and computation, but must not add or remove future canonical possibilities or obligations that were already implied by the same canonical history.**

Operationally, preserve the set of future-relevant obligations / capabilities and the conditions that make them reachable. Do **not** require identical event counts or identical internal representation.

Corollaries:

- refinement may reveal an already-latent obligation; it may not create one merely because the player approached or an entity became visible;
- deferred computation is legal; silently dropped semantic work is not;
- parallel execution is legal where effects are proven commutative under the semantic contract; unordered canon is not;
- the director may choose among already-eligible consequences; it may not invent semantic premises;
- model outputs are candidates until normal authorization + semantic validation + commit;
- recovery may restore runtime state, but canonical truth remains the append-only log;
- different representations are equivalent when they preserve future canonical reachability, not when their internal forms or event sequences are byte-identical.

This law is the synthesis point for C1–C29. It is a design contract, not a request for a new subsystem.

---

## 2. Architecture that must remain intact

```text
input / observation / model output
        ↓
interpretation → intent classification → authorization
        ↓
semantic resolver (sole semantic owner)
        ↓
declared effect surface + postconditions
        ↓
pure admissibility / authority gate (non-resolving)
        ↓
sole writer → append-only JSONL truth
        ↓
fold / derived indexes / presentation
```

- Simulator remains the sole canonical writer.
- Log remains canon; fold / indexes remain rebuildable.
- Mediator remains the authority boundary.
- LLM remains interpretation / candidate generation / narration; it never writes canon directly.
- Packs remain content/data; engine remains domain-agnostic.
- No second truth store, semantic resolver, generic planner, or generic reactive/lifecycle framework.

---

## 3. Required synthesis rules

1. **One semantic owner.** A post-resolver gate may reject an unauthorized or contract-violating effect, but may not independently decide what the event means.
2. **Causal spine, not full causal graph.** Record primary cause + necessary supports + provenance. Add full graph machinery only if a named consumer and measured native limit force it.
3. **Obligation-preserving refinement.** Macro/meso/individual representations may differ; future-relevant obligations must not be created or destroyed by observation/refinement.
4. **Causal-demand locality.** Work propagates because an event demands it, not because something is far/near. Budget exhaustion means defer, never silent loss.
5. **Strict order by default.** Admit explicit parallel cohorts only where commutativity is proven; do not introduce CRDT/MVCC by default.
6. **Derive-first replay.** Semantic replay identity is explicit; continuation state is only irreducible runtime state. Never equate `flush` with OS durability without crash evidence.
7. **Director = affordance scheduler.** It may select, release, pace, or defer eligible consequences; it may not invent entity, motive, goal, cause, or world fact.
8. **Agency without generic planning.** Use bounded deterministic persistent goals / commitments / progress / failure / adaptation when a consumer needs them. No LLM planner.
9. **Ambiguity by effect equivalence.** Auto-accept distinct interpretations only when their canonical effect surface is equivalent; otherwise clarify / reject. Do not add a global confidence score.
10. **Typed speech acts.** Free prose is never canon. Language may create social facts only when explicitly typed and admitted through the normal simulator path.
11. **Measurement before runtime growth.** Target-model quality, playtime, claim normalisation, injection/recovery, and scale must be measured before architecture is expanded for them.

---

## 4. Mandatory reading order

1. **This file**
2. `03_OPEN_CONTRACTS.md` — D0 + P0 contracts first
3. `05_PROPOSED_TASKS.md`
4. `07_OUT_OF_SCOPE.md`
5. Only when needed:
   - `04_MEASUREMENT_GAPS.md`
   - `06_CONTRADICTIONS.md`
   - `02_CLOSED.md`
   - `01_SOURCE.md`

Do not read the superseded free-form review as operational input.

---

## 5. Namespace warning

| This package | `docs/TASKS.md::core-1` |
|---|---|
| C1 semantic event validity / authority | C1 representation continuity |
| C2 causal sufficiency | C2 compiled / indexed execution |
| C3 representation continuity / future reachability | C3 history / replay scale |
| C4 replay identity / recovery | C4 LLM boundary under unusual interaction |
| C5 locality / causal work budget | C5 shared semantic equivalence |

Shared surface: representation continuity / player-independence. Never merge labels mechanically.

---

## 6. Allowed actions after owner intake

- Triage every open contract against current `STATUS.md`, `docs/TASKS.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md`, and `core-1`.
- Mark: already closed / superseded / contradictory to standing decision / still open / needs owner decision.
- Propose **≤7** rows for `docs/TASKS.md`, adapting `05_PROPOSED_TASKS.md` and collapsing coverage already present.
- Report measurement gaps and unresolved owner choices.
- Stop.

## 7. Forbidden actions

- Implementing any contract from this package.
- Changing `core/`, schemas, packs, queue key, tick semantics, or log header during intake.
- Expanding scope beyond confirmed task IDs.
- Reopening phases 0–6.
- Adding a second canonical store, second semantic resolver, full causal graph, CRDT/MVCC layer, generic workflow/reactive engine, generic planner, global confidence/truth/risk score, permanent diagnostic graph, or self-adjusting global runtime without the runtime-promotion gate.
- Treating philosophical tensions as defects requiring code.
- Claiming scale / living-world proof while P0 contracts or required measurements remain open.
- Creating nested AGENTS / second memory / heavy tooling without owner proof of need.

---

## 8. Correct work sequence

```text
master law D0
→ precise semantic contracts
→ cheapest discriminating probes / counterexamples
→ minimal contract refinement
→ named consumer + measured native limit
→ targeted runtime promotion only when the gate is met
```

Never optimize a metric without a decision it distinguishes (avoid Goodharting).

---

## 9. Success condition for first intake session

1. A triage table over all open contracts.
2. ≤7 proposed `docs/TASKS.md` rows or confirmation that existing rows cover them.
3. Explicit owner choices still required.
4. Clear stop. No code, schema, runtime, or phase changes.
