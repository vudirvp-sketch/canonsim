# 07 — Out of Scope / Hard Rejects

This package is a contract-and-triage layer. Owner confirmation of a task ID is required before implementation.

## Never do from this package alone

1. Implement an open contract merely because it is written here.
2. Change `core/`, schemas, pack format, queue key, tick semantics, or log header during intake.
3. Add runtime dependencies or network surfaces.
4. Build a second canonical store, second semantic resolver, or second truth authority.
5. Add a full causal / provenance graph when the causal-spine contract is sufficient.
6. Add CRDT/MVCC solely to obtain concurrency; first test certified commutative cohorts under strict canonical order.
7. Add a generic workflow / lifecycle / reactive / incremental runtime layer.
8. Add a generic planner or LLM planner.
9. Add a global truth / risk / confidence score as a substitute for explicit effect, authority, and epistemic contracts.
10. Turn the director into a storyteller, hidden semantic author, or source of new motives/entities/causes.
11. Turn free-form prose into canon without a typed speech-act path and normal simulator admission.
12. Make player observation/refinement a semantic cause of new world obligations.
13. Silently drop deferred work when a budget is exhausted.
14. Reopen phases 0–6 as “incomplete” without new falsifying evidence.
15. Expand ontology / mechanic families without a new owner-gated design.
16. Claim “living-world / continent-scale proven” while P0 contracts or required measurements remain open.
17. Optimise metrics without a decision they distinguish (Goodhart surface).
18. Reopen Soul-of-Waifu integration without explicit owner scope and product decisions.
19. Create nested AGENTS, second project memory, or heavy tooling without owner proof of need.

## Runtime-promotion rule

A runtime change requires all of:

```text
named consumer
+ real failure
+ material quality gap
+ measured native limit
+ repeated shape
+ falsifier
+ semantic/information owner
+ phase/gate
```

No “architecture clean-up” exception.

## Valid scope of first intake session

- Read mandatory files.
- Triage contracts against current repository state.
- Collapse duplicates.
- Propose ≤7 TASKS rows.
- Surface owner choices.
- Stop.

## Valid scope after task confirmation

- Work on the confirmed task only.
- Keep the change set small and risk-classed.
- Preserve proof-carrying change / AGENTS iteration rules.
- Escalate scope only with owner instruction.

## End-state criterion

> CanonSim guarantees not only deterministic, structurally valid canonical events, but preservation of future canonical obligations and reachability across authority transitions, representation/refinement, locality/defer, concurrency, recovery, and model uncertainty — without granting a secondary system the right to define canon.
