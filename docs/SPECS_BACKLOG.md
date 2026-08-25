# SPECS_BACKLOG.md — Just-in-Time Spec Queue

> Rule: a spec is written ONLY when its trigger fires, FROM experiment
> results — never speculation. One spec per phase. ≤300 lines each. Writing a
> spec before its trigger = scope creep (`AGENTS.md` §2). Further polishing of
> the concept without experiments produces paper, not knowledge.

| Spec | Trigger | Track | Content sketch |
|---|---|---|---|
| `INTENT_SCHEMA.md` | iter-2 starts | A | intent record: type, target, method, risk, uncertainty; button/command mapping |
| `DIRECTOR_SPEC.md` | iter-4 starts | A | buffer, seeding rules, triggers, stagnation detector |
| `TEST_PLAN.md` | iter-6 starts | A | T0–T8 formalization, gate protocol, metrics M1/M2 |
| `docs/TAXONOMY.md` | bg-2 done | B | 100–300 DF event types mapped onto our ontology |
| `CORE_ONTOLOGY.md` | phase-0 gate passed | A | generalize from the tavern slice to the universal core |
| `BRIEF_SPEC.md` | phase 1 | B → A | brief assembly, per-block token budgets, `known_by` filter |
| `VALIDATION_SPEC.md` | phase 1 | B → A | fact transaction, reverse prose validation, regen cap |
| `PACK_SPEC.md` | phase 6, or a 2nd setting is needed | A | manifest, module contracts, pack CI |
| `LEGEND_SPEC.md` | phase 4 | B | offline compression; legends always rebuildable from the log |
| `SOW_INTEGRATION_SPEC.md` | phase-1 gate passed | A | dumb-terminal contract, mode wiring inside Soul-of-Waifu |
