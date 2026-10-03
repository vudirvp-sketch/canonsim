# 08 — Ready-to-Paste Owner Intake Prompt

Copy the block below into the agent session.

```text
Owner request (concept-review intake):

Read docs/analysis/concept-review-2026-10/00_README_AGENT.md and follow its
master law D0, mandatory reading order, allowed actions, and forbidden actions.

The purpose of this session is TRIAGE, not implementation.

1. Read 03_OPEN_CONTRACTS.md first, especially D0 and P0.
2. Triage every C1–C29 surface against current STATUS.md,
   docs/TASKS.md, docs/DECISIONS.md, docs/ROADMAP.md, and core-1.
3. For each item classify it as:
   already-closed / superseded / contradicted-by-standing-decision /
   still-open / needs-owner-decision.
4. Produce one compact triage table. Do not restate contract prose that
   already appears in the package.
5. Propose at most 7 docs/TASKS.md rows. Prefer 05_PROPOSED_TASKS.md;
   collapse any row already covered by the live backlog.
6. Preserve these adopted syntheses unless repository evidence falsifies them:
   - D0 future-reachability / causal-obligation conservation;
   - D1 one semantic owner + non-resolving admissibility gate;
   - D2 causal spine, not full DAG;
   - D3 obligation-preserving refinement;
   - D4 explicit semantic replay identity + separate continuation + durability;
   - D5 causal-demand locality + deferred semantic debt;
   - D6 strict order + certified commutative cohorts;
   - D7 director as affordance scheduler;
   - D8 bounded persistent agency, no generic planner;
   - D9 ambiguity collapse only by canonical effect-equivalence;
   - D10 typed speech acts through the normal simulator path;
   - D11 measurement before runtime promotion.
7. Surface only owner choices still genuinely unresolved (especially M4/M5,
   playtime budget, and product weighting of liveness/emergence).
8. Stop. No code. No schema changes. No core edits. No new runtime architecture.

Risk class: R0–R1 (docs / triage only).
```

## P0-only variant

```text
Owner request (P0 contract intake):

Read docs/analysis/concept-review-2026-10/00_README_AGENT.md and
03_OPEN_CONTRACTS.md.

Triage only C1–C5. Apply D0 as the master law. Map each item against the
live TASKS/STATUS/DECISIONS state, collapse duplicates, and propose at most
5 task rows from 05_PROPOSED_TASKS.md. Stop. No code.
```

## Contract-deep-dive variant

```text
Owner request (single contract definition):

Read docs/analysis/concept-review-2026-10/00_README_AGENT.md,
03_OPEN_CONTRACTS.md, and the relevant section of 05_PROPOSED_TASKS.md.

Work on the named contract only. Write the definition, the cheapest
counterexample/falsifier, and the acceptance criterion. Do not implement.
Do not broaden scope.
```
