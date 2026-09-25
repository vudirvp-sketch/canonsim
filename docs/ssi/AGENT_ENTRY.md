# SSI AGENT ENTRY POINT

Read this first.

## Hard protocol

1. Load `controls/manifest.yaml`.
2. Classify problem mode and task risk R0–R5.
3. Walk `mandatory_order` exactly unless a block is marked `NOT_APPLICABLE`.
4. Never convert `OPEN` → `VERIFIED` without evidence.
5. Never treat documentation, tests, agent self-review, or generated rationale as proof by default.
6. For R3–R5 make compositional assumptions explicit; for R4/R5 require an independent verification path.
7. For material agent actions verify effective context sufficiency and obey `controls/agent-capabilities.yaml`.
8. Treat external tool providers as untrusted supply-chain boundaries until provenance/capability/identity gates pass.
9. For material changes produce `templates/proof-carrying-change.md`; for decisions use `templates/decision-record.md`; for material AI claims use `templates/agent-claim.md`.
10. At completion produce a change record and disposition.

## Canonical doctrine

`software-semantic-integrity-unified-v3.md`

## Non-negotiable execution rule

`insufficient_context ≠ permission_to_guess`
