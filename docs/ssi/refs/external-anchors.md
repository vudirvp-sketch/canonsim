# External anchors used for the advanced supplement

Reference anchors are not authority over the SSI doctrine. Import only mechanisms that pass the SSI Material Verdict Test.

- `TLA+ / TLC` — formal specification / model checking.
- `Dafny / P` — implementation-level specification / verification / protocol reasoning.
- `SLSA / in-toto` — provenance / supply-chain attestations.
- `OWASP AI agent security` — least privilege, sandboxing, excessive-autonomy and high-impact action controls.
- `Deterministic Simulation Testing` — replayable seeded fault exploration for stateful/distributed systems.
- `C4` — standardized multi-level architecture views.
- `ADR / RFC / Design Docs` — durable and pre-implementation decision memory.
- `SRE error budgets / burn-rate` — operational reliability control.
- `Canary / progressive delivery` — staged exposure, observation and rollback.
- `OPA / Rego` — executable policy enforcement.
- `ArchUnit / dependency-cruiser` — machine-enforced architecture constraints.
- `Pact` — consumer-driven contract testing.
- `Outbox / Saga / CDC / idempotency / ReBAC / CRDT` — concrete distributed-system mechanisms for specific invariants.

## Import rule

`source → actual mechanism → invariant → target adaptation → incompatibilities → observable consequence → cheapest falsifier → disposition`

Do not treat names, popularity, or external authority as evidence that a mechanism fits the target system.
