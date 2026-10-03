# 05 — Proposed TASKS.md Drafts

Drafts only. Adapt to the live `docs/TASKS.md`; collapse coverage already present. No implementation until owner confirms task IDs.

## Recommended sequence

```text
T1 + T2 (contracts / definitions)
    → T3 (representation / future reachability)
    → T4 (replay / recovery)
    → T5 (locality / commutativity / budget)
    → T6 (canon / epistemic / speech channels)
    → T7 (intent / agency / director)
    → M1–M4 measurement batteries
```

T5 includes the concurrency synthesis only as a contract: strict order by default, certified commutativity where proven. It is not permission to build CRDT/MVCC.

---

## T1 — Semantic event validity + authority (C1 / D1)

- **Track:** A
- **Risk:** R0–R1 (docs)
- **Goal:** define admissibility without introducing a second semantic authority.
- **Acceptance:**
  - [ ] Resolver = sole semantic owner.
  - [ ] EventDraft declares allowed effect surface + postconditions.
  - [ ] Gate is pure/non-resolving and checks authority + invariants only.
  - [ ] Cheapest falsifier: mutate a producer output to remain schema-valid but violate declared authority/effect → RED gate → no append.
  - [ ] Record explicitly that the private `_commit` probe is a contract gap, not production-path proof.
  - [ ] No tautological “checker compares event to itself”.
- **Do not:** implement a semantic checker or change schemas in the definition task.

## T2 — Causal sufficiency (C2 / D2)

- **Track:** A
- **Risk:** R0–R1
- **Goal:** define `primary_cause + necessary_supports + provenance` without a causal-graph subsystem.
- **Acceptance:**
  - [ ] Necessary support defined counterfactually.
  - [ ] Optional evidence separated from causal necessity.
  - [ ] Ablation probe: remove support X → claimed outcome becomes unreachable.
  - [ ] Compatibility note with INV-1 / INV-5 and current event consumers.
  - [ ] Explicit owner decision recorded.
- **Do not:** introduce full DAG / provenance engine.

## T3 — Representation continuity / future reachability (C3 + C14 + C18 / D3)

- **Track:** A / core-1 mapping
- **Risk:** R1 definition; R3+ only if a consumer + native limit forces code
- **Goal:** replace event-equality LOD reasoning with obligation-preserving refinement.
- **Acceptance:**
  - [ ] Define future-relevant conserved set: identity, existence/disposition, location, ownership, membership, inventory, relationships, authority/debt, relevant knowledge, persistent goals/commitments, and any state capable of changing future canonical outcomes.
  - [ ] Disposition vocabulary: `active | merged | condensed | destroyed | retired | transformed | unknown` + `represented_by`.
  - [ ] State law: refinement may reveal latent obligation; may not create a new causal obligation merely because the player approached/observed.
  - [ ] Define an explicit representation-equivalence relation over future reachability, not event count.
  - [ ] Probe: same semantic history prefix + same elapsed world time + same seed + different observation/refinement path → compare conserved obligations and reachable future outcomes.
  - [ ] Map exactly to `core-1` C1/C3 surfaces; do not merge labels.
- **Do not:** build a new LOD subsystem in the contract task.

## T4 — Replay identity + recovery durability (C4 + C7 + C13 / D4)

- **Track:** A
- **Risk:** R0–R1
- **Goal:** make semantic replay identity and crash boundaries explicit.
- **Acceptance:**
  - [ ] Identity tuple = `log_prefix_digest + engine_semantic_version + schema_identity + pack_semantic_digest + execution_config_digest + seed`.
  - [ ] Distinguish semantic identity from continuation state.
  - [ ] List irreducible continuation state only.
  - [ ] Lifecycle = proposed → accepted → durable → committed.
  - [ ] Crash contract covers append-before-durable, post-durable, and derived-state boundaries.
  - [ ] Explicitly reject “flush == durable” as an evidence-free claim.
- **Do not:** change serialisation format before the contract is accepted.

## T5 — Causal-demand locality + certified commutativity + work budget (C5 + C6 + C16 + C28 / D5 + D6)

- **Track:** A
- **Risk:** R0–R1
- **Goal:** define scale behaviour without a generic concurrency / scheduling framework.
- **Acceptance:**
  - [ ] `LOCAL`: affected set + direct/indexed access.
  - [ ] `REGIONAL`: bounded causal traversal.
  - [ ] `GLOBAL`: explicit scheduled pass.
  - [ ] Work budget is explicit; exhaustion produces deferred work, never silent semantic loss.
  - [ ] Default canonical order remains standing order.
  - [ ] A parallel cohort is legal only with a proof obligation equivalent to order-commutative semantic effects / disjointness.
  - [ ] Measurement: world size × fan-out × operation → inspected / candidate / committed items + wall time.
  - [ ] Runtime promotion needs named consumer + measured native limit + falsifier.
- **Do not:** add indexes, CRDT/MVCC, or new scheduler machinery in the definition task.

## T6 — Canon / epistemic / speech boundary (C8 + C9 + C10 + C25 + C26 / D10)

- **Track:** A
- **Risk:** R0–R1
- **Goal:** keep presentation, knowledge, and social language distinct while permitting explicit typed speech acts.
- **Acceptance:**
  - [ ] Channels: canonical fact / knowledge-belief / perception / structured speech act / narration / diagnostic trace.
  - [ ] Structured proposal is frozen before narration; prose failure retries prose only.
  - [ ] Promotion path: candidate → normal authority/semantic validation → canonical event.
  - [ ] Grounding applies to atomic externally-testable assertions, not every metaphor/token.
  - [ ] Epistemic scope remains actor / player / narrator / debug; no omniscient leak via irony.
  - [ ] Free prose never becomes canon; typed speech acts can, but only through the simulator.
- **Do not:** rewrite mediator code in the definition task.

## T7 — Intent / agency / director boundary (C11 + C12 + C20 + M4 / D7–D9)

- **Track:** A
- **Risk:** R0–R1
- **Goal:** define semantic authority across player/NPC/director/model inputs without adding planners or confidence magic.
- **Acceptance:**
  - [ ] Pipeline: input → interpretation → classification → authorization → execution.
  - [ ] `valid != authorized`.
  - [ ] Authority classes: player | NPC | director | system | pack.
  - [ ] Ambiguity rule: auto-collapse only when candidate canonical effect surfaces are equivalent; otherwise clarify/reject.
  - [ ] Director invariant: `DirectorOutput ⊆ EligibleConsequences(world, pack, current_state)`; mutation probe must catch invented consequences.
  - [ ] Agency state is bounded/deterministic and persistent only where a named consumer needs it: goal / commitment / progress / failure / adaptation.
  - [ ] No generic planner; no LLM planner.
  - [ ] Explicit vocabulary: instruction / proposal / authority / realised intervention / canonical consequence.
  - [ ] Model path: structured candidate → authority → semantic validation → durable immutable commit.
- **Do not:** add director/mediator runtime machinery in the definition task.

---

## Measurement tasks after contract closure

- **M1:** 27B one-model live mediator/claims battery.
- **M2:** surface→ID claim normalisation A/B.
- **M3:** one-model vs two-model end-to-end playtime budget.
- **M4:** semantic intent/injection boundary + owner recovery decision.

These are measurement tasks, not automatic runtime-promotion tickets.

## Runtime-promotion gate

All required before architecture growth:

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
