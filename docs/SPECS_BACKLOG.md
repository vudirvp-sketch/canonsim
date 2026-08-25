# SPECS_BACKLOG.md — Just-in-Time Spec Queue

> Rule: a spec is written ONLY when its trigger fires, FROM experiment
> results — never speculation. One spec per phase. ≤300 lines each. Writing a
> spec before its trigger = scope creep (`AGENTS.md` §2). Further polishing of
> the concept without experiments produces paper, not knowledge.

| Spec | Trigger | Track | Content sketch |
|---|---|---|---|
| `INTENT_SCHEMA.md` | iter-2 starts | A | intent record: type, target, method, risk, uncertainty; button/command mapping |
| `DIRECTOR_SPEC.md` | iter-4 starts | A | buffer, seeding rules, triggers, stagnation detector; **narrative entropy** (P2e, proposal) = sum(seeded-hook weights) + global suspicion + visible physical threats — stagnation_detector releases when entropy drops below threshold, not on a flat timer; entropy computed only from seeded hooks + visible state, never invents new threats (D-005 preserved) |
| `TEST_PLAN.md` | iter-6 starts | A | T0–T8 formalization, gate protocol, metrics M1–M5 (M3 causal chain length, M4 novelty/repetition, M5 non-PC event share — D-019) |
| `docs/TAXONOMY.md` | bg-2 done | B | 100–300 DF event types mapped onto our ontology |
| `CORE_ONTOLOGY.md` | phase-0 gate passed | A | generalize from the tavern slice to the universal core |
| `BRIEF_SPEC.md` | phase 1 | B → A | brief assembly, per-block token budgets, `known_by` filter, **sensory emitters + beat-boundary delta** (the brief is a delta of what the PC perceived since the last beat, not a world dump — bounds size to O(perception radius) regardless of log length); from phase 4+ the brief reads **derived traits** (LEGEND_SPEC) instead of raw `knowledge.records` when both exist — keeps brief size O(traits × PC perception), not O(history) |
| `VALIDATION_SPEC.md` | phase 1 | B → A | fact transaction, reverse prose validation, regen cap, **prompt-injection neutralized structurally** (the prose→proposal boundary: mode-A prose is never a fact proposal; the C-parser emits grammar-constrained Intent JSON; the validator accepts structured proposals only — no post-hoc text sanitization) |
| `PACK_SPEC.md` | phase 6, or a 2nd setting is needed | A | manifest, module contracts, pack CI |
| `LEGEND_SPEC.md` | phase 4 | B | offline compression; legends always rebuildable from the log; **trait crystallization** (P3f): 3+ related `knowledge.records` collapse into a discrete belief token (e.g., `paranoid_about_thieves`); traits are derived state (fold of subset), never stored as primary data (INV-1 preserved); on demand, traits expand back to source records for the brief |
| `SOW_INTEGRATION_SPEC.md` | phase-1 gate passed | A | dumb-terminal contract, mode wiring inside Soul-of-Waifu |
