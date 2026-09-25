# SSI PACKAGE INDEX

| ID | Module | Core question | Mandatory artifacts |
|---|---|---|---|
| A | Core baseline | What does the system mean? | invariants/contracts |
| B | Topology | What actually changes together? | dependency + co-change + ownership topology |
| C | Complexity | How large is the semantic state space? | state/transition/interaction budget |
| D | Formal verification | Which claims need model-level proof? | safety/liveness/model |
| E | Static semantics | Can the rule be enforced before runtime? | AST/IR/policy checks |
| F | Testing | Can the claim be falsified? | property/mutation/fuzz/model |
| G | Runtime control | How is degradation bounded? | SLO/error/retry/concurrency budgets |
| H | Agent governance | What may the agent do and know? | capability + context + tool provenance + approval |
| I | Evolution | How do we change/remove safely? | compatibility + rollback + GC |
| J | Provenance | Can the artifact be traced/reproduced? | provenance/attestation |
| K | Operations | Was every block applied or explicitly skipped? | change record + disposition |
| L | Frontier controls | Which expert mechanisms strengthen construction, proof, runtime and governance? | semantic types + compositional proof + deterministic simulation + delivery/agent controls + proof-carrying change |

## Severity / evidence rule

`evidence threshold ∝ blast radius × irreversibility × privilege × uncertainty`

## Problem-mode rule

Before selecting a method, classify the problem by observed characteristics: deterministic/known, complicated/structurally analyzable, complex/experiment-driven, or unstable/containment-first. This is a method-selection heuristic, not a correctness proof.

## Block state

`NOT_APPLICABLE | OPEN | PARTIAL | VERIFIED | WAIVED`
