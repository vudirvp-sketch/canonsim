# 03 — Open Contracts + Master Decision Set

Severity: **P0** blocks credible living-world / scale claims; **P1** is high product or correctness risk; **P2** can wait; **P3** is deeper philosophy / later product choice.

## Master law: D0

> **Future-Reachability / Causal-Obligation Conservation:** for the same canonical history prefix and semantic execution identity, changing representation, observation/refinement path, scheduling strategy, or model presentation may change internal form and event realization details, but must not add or remove future canonical possibilities or obligations that were already implied by that prefix.

Use this law instead of asking whether two paths produced identical event counts, identical LOD objects, or identical internal plans.

A useful proof obligation is:

```text
future_reachable(world_A) == future_reachable(world_B)
```

up to an explicit, declared equivalence relation over representations. At minimum, preserve all future-relevant identity, disposition, location, ownership, membership, inventory, relationships, authority/debt, knowledge, persistent commitments, and any other state capable of changing future canonical outcomes.

---

## P0 — Resolve or explicitly park

| ID | Contract | Decision / required form | Risk if left open |
|---|---|---|---|
| C1 | Semantic event validity + authority | **ADOPT D1:** resolver is sole semantic owner; output declares allowed effect surface + postconditions; pure non-resolving authority/invariant gate admits/rejects; sole writer commits. | Schema-valid log may encode an unauthorized semantic effect. |
| C2 | Causal sufficiency / multi-cause | **ADOPT D2:** primary cause + necessary supports + separate provenance. Full causal DAG rejected for now. Use counterfactual ablation to distinguish necessary supports from evidence. | Tree-like reduction can erase conditions required for the outcome. |
| C3 + C14 + C18 | Representation / LOD / disposition / player-independence | **ADOPT D3:** obligation-preserving refinement. Keep eager causal skeleton + latent obligations + explicit disposition + `represented_by`. Refinement may reveal a latent obligation; it may not create a new causal obligation because the player approached / observed. | Player observation can become an accidental semantic input. |
| C4 + C7 + C13 | Replay identity + continuation + recovery | **ADOPT D4:** derive-first; replay identity = log prefix digest + engine semantic version + schema identity + pack semantic digest + execution-config digest + seed. Continuation state = irreducible runtime only. Lifecycle: proposed → accepted → durable → committed. | Same log prefix can produce a different future execution. |
| C5 + C16 + C28 | Locality + causal work budget + temporal | **ADOPT D5:** LOCAL / REGIONAL / GLOBAL work classes driven by causal demand; explicit budget; exhaustion = defer, never silent drop. Measure scans before index/runtime promotion. | Scale claims collapse under hidden pack-wide work. |

---

## P1 — High priority

| ID | Contract | Decision |
|---|---|---|
| C6 | Order / simultaneity | **ADOPT D6:** strict ordered execution by default. Permit explicit cohorts only when effect commutativity is mechanically/semantically proven. No CRDT/MVCC unless a named consumer + native-limit falsifier requires it. |
| C8 | Channel isolation | Freeze structured proposal before narration/retry. Presentation failure retries presentation only. |
| C9 | Prose grounding | Ground atomic externally-testable assertions; do not force word-by-word metaphor grounding. |
| C10 | Epistemology | Keep proposition | source | acquired_at | fidelity | trust | status. Forgetting is explicit. No generic belief graph. |
| C11 | Director | **ADOPT D7:** DirectorOutput ⊆ EligibleConsequences(world, pack, current_state). Director can select/release/pace/defer eligible consequences; may not invent entity, motive, goal, cause, or fact. |
| C12 | Agency | **ADOPT D8:** bounded deterministic persistent state when required by a named consumer: goal/commitment/progress/failure/adaptation. No generic planner; no LLM planner. |
| C14 | Disposition | Explicit vocabulary: `active | merged | condensed | destroyed | retired | transformed | unknown` + `represented_by`. |
| C20 | Intent / authority | **ADOPT D9:** input → interpretation → classification → authorization → execution. `valid != authorized`. Authority classes: player / NPC / director / system / pack. No global confidence score. |
| C25 | Fact / prose | **ADOPT D10:** free prose never becomes canon. Social language may create canon only as typed speech acts admitted by the simulator. |

---

## P2 / P3 — Defer until P0/P1 and product measurement

C15 core growth; C17 save/fork; C19 RNG extensions (mostly closed); C21 invisible causality; C22 psychology; C23 long horizon; C24 determinism vs liveness; C26 dramatic irony; C27 Goodhart / interestingness; C29 lazy terminology.

Current position:

- C24 is a product/philosophy choice, not a runtime bug: do not weaken deterministic canon merely to simulate liveness.
- C27 treats emergence/interestingness as a product target that must be measured, not a subsystem to add by intuition.
- C29 wording should be **eager foundation + lazy refinement/promotion**, not “fully lazy worldgen” while the foundation is eager.

---

## D0–D11 decision set

### D0 — Future-Reachability / Causal-Obligation Conservation
The master criterion above. Preserve future canonical reachability and obligations, not representation identity.

### D1 — One semantic authority + admissibility gate
Resolver decides semantics. A post-resolver gate checks declared effects, postconditions, authorization and invariants without becoming a second resolver.

### D2 — Causal spine
`primary_cause + necessary_supports[] + provenance`. Necessary means counterfactually required for the claimed outcome; provenance is evidentiary lineage, not a second causal ontology.

### D3 — Obligation-preserving refinement
Macro → meso → individual is a representation change. Each refinement can reveal latent detail but cannot manufacture future-relevant obligations that were absent from the same canonical history prefix.

### D4 — Semantic replay closure + explicit durability
Replay identity:

```text
log_prefix_digest
+ engine_semantic_version
+ schema_identity
+ pack_semantic_digest
+ execution_config_digest
+ seed
```

Continuation state contains only irreducible runtime state. `flush != durable` until crash evidence proves the required boundary.

### D5 — Causal-demand locality + deferred debt
`LOCAL` = affected set via direct/indexed access; `REGIONAL` = bounded traversal; `GLOBAL` = explicit scheduled pass. Budget exhaustion creates durable/deferred work, never silent semantic loss.

### D6 — Ordered canon + certified commutativity
Default order stays `(tick, sub_order, actor_id)` / standing queue law. A cohort may execute in parallel only when each member's semantic effects are proven order-commutative under the contract. The log still records canonical order.

### D7 — Director as affordance scheduler
Director schedules existing eligible consequences. It is not a storyteller, generic planner, hidden semantic author, or source of new entities/motives/causes.

### D8 — Agency without generic planner
Persistent commitments supply continuity. Bounded deterministic selection over a small candidate action set produces adaptive behaviour without a generic planning engine.

### D9 — Ambiguity by effect-equivalence
When multiple interpretations map to an equivalent canonical effect surface, ambiguity can collapse safely. Otherwise clarification or rejection is required. Do not replace this with a global confidence/risk/truth number.

### D10 — Typed speech acts
`free-form prose → candidate structure → normal authorization → semantic validation → canonical event`. A promise, command, debt acknowledgement, etc. can be canonical only when explicitly typed and admitted.

### D11 — Measure before promotion
Runtime architecture changes require a named consumer, real failure, material quality gap, measured native limit, repeated shape, falsifier, clear semantic owner, and phase/gate. Metrics are decision instruments, not goals.

---

## Explicit rejects unless the promotion gate is met

```text
second canonical store
second semantic resolver
full causal/provenance graph
semantic CRDT / MVCC layer
generic workflow / lifecycle / reactive engine
generic planner
LLM planner
global truth / risk / confidence score
permanent diagnostic graph
self-adjusting global incremental runtime
core-1 runtime architecture build
```

Prefer an existing primitive + explicit relation/contract + cheapest falsifier.

## Material code probes retained from the review

- C1: private `_commit()` accepts schema-valid undeclared/unauthorized-looking drafts; record the gap, but do not infer a production exploit without a producer-path falsifier.
- C3/C18: current LOD derives zones from player position and filters canonical activity; obligation-conservation is therefore unproven.
- C4: live cursor lacks engine/schema/pack-content/config identity; semantic replay closure is incomplete.
- C5: some hot paths scan pack-wide collections before filtering; locality is not yet a proven complexity property.
- C13: resume is strong at clean boundaries; `flush` is not a durability proof.
- M4: injection corpus still shows instruction-shaped model content reaching the intent door; structure alone does not prove semantic intent separation.
