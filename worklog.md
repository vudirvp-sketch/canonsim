# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.

---
iter-0v · 2026-08-27 · owner-requested audit patches (the 21-point iter-0u audit, applied)
- INV-2 rewritten in AGENTS.md per D-028 (one master seed; named streams;
  sha256-based `stable_hash`); stale one-instance wording purged from TASKS
  iter-1 / TECH_NOTES §4 / MVP_SCOPE §3+§13; KI#8 opened/closed. The 18
  remaining audit resolutions landed as sub-clauses: phase0 §1 (pack lint),
  §2 (DAG language, intent OCC + lifecycle, price precursor), §4 (director
  rejection + per-run scope), §5 (ShufflePool, prune_window), §6 (T1 fixture
  guard); phases §1 (eviction), §4 (precedence + provenance), §6 (cycle
  contract); EVENT_SCHEMA §11 (vocabulary-per-pack); SPECS_BACKLOG sketches;
  DECISIONS D-028; STATUS synced.
- KI#7 resolved: worklog trimmed to the 10×3–5 cap, TASKS done-entries
  collapsed (1187 → ~215 lines; pre-trim history in git). 12 files touched —
  over the 3–5 soft limit: mandated sync set + the collapse, same pattern as
  iter-0u. No code; pytest green, ruff clean. 21st docs iteration
  (owner-requested, D-022); **iter-1 code is next, unconditionally**.
---
iter-0u · 2026-08-27 · owner-requested references distillation (synthesis pass)
- New `docs/BLUEPRINT.md` (149 — resolution ledger: 12 cross-ref tensions →
  mechanisms; 12 cross-cutting laws; build index) + `docs/blueprint/phase0.md`
  (340 — iter-1..6 combined donor designs) + `docs/blueprint/phases.md` (224 —
  phases 1–6 + cross-cutting). D-027: fourth anti-drift place; RNG-1/EPIST-1
  clarifications enacted as ledger rows.
- 9 files touched (3 new + mandated sync set: AGENT_NAVIGATION §1/§2/§3,
  DECISIONS D-027, REFERENCES_DEEP pointer, TASKS, STATUS, worklog). No code;
  pytest green, ruff clean.
- Next: iter-1 core plumbing, unconditionally — read `docs/blueprint/
  phase0.md` §1 + ledger rows RNG-1/SCHED-1/STATE-1/STORE-1/TEST-1 first.
---
iter-0t · 2026-08-27 · owner-requested ref-13 solo deep dive (live-char-guide)
- New `docs/ref/live_char_guide.md` (304): SPINE/Price/observability,
  Influence Boundary candidate rule, BRIEF_SPEC injection grammar, AP →
  PACK_SPEC lint vocabulary. License clean MIT. All ref-N backlog complete
  (ref-1..ref-13 + iter-0h cousins).
---
iter-0s-followup · 2026-08-27 · post-push verification pass (owner request)
- KI#7 opened (capped-memory drift: worklog ~880-line entries vs the 3–5
  law; TASKS done entries uncollapsed); no functional change.
---
iter-0s · 2026-08-27 · owner-requested ref-12 solo deep dive (UAP webapp)
- New `docs/ref/uap_audit.md`: rubric donor, 7-hole test crosswalk, phase-1
  harness patterns, pack-lint vocabulary. License catch: README claims MIT,
  no LICENSE file — reference only. Catalog §9 + index + synthesis + TEST_PLAN/
  PACK_SPEC sketches synced.
---
iter-0r · 2026-08-26 · owner-requested ref-10 + ref-11 6-batch deep dive
- New `docs/ref/{entt,bevy,eventstore,sqlite_fts5,duckdb,sqlite_vec}.md`;
  ref-10/ref-11 flipped todo→done; EventStore license drift fixed (index
  "MIT" → BSD-3-Clause/ESLv2 pattern-only); sqlite-vec catalog "verify" →
  dual MIT OR Apache-2.0.
---
iter-0q · 2026-08-26 · owner-requested ref-8 + ref-9 6-batch deep dive
- New `docs/ref/{azgaar_fmg,natural_earth,geonames,libtcod,rot_js,
  red_blob_games}.md`; ref-8/ref-9 flipped todo→done; AGENT_NAVIGATION §1 +
  STATUS + TASKS synced.
---
iter-0p · 2026-08-26 · owner-requested ref-7 3-batch deep dive
- New `docs/ref/{generative_agents,ai_town,letta}.md` (LLM-agent precedents,
  mostly negative; bg-4 cost anchors); ref-7-a/b/c flipped todo→done with
  corrected Apache-2.0 license annotation on ref-7-a.
---
iter-0n · 2026-08-26 · owner-requested ref-5 4-batch deep dive
- New `docs/ref/{wesnoth_wml,endless_sky_dsl,ink,tracery}.md` (event/narrative
  grammar family); ref-5 done; KI#6 license drift closed; AGENT_NAV §1 +
  STATUS + worklog + TASKS synced.
---
iter-0m · 2026-08-26 · owner-requested ref-4 batch deep dive
- New `docs/ref/{rimworld,l4d_director,alien_isolation}.md` (pacing trio);
  ref-4 done in-place; AGENT_NAVIGATION §1 + STATUS + worklog + TASKS synced.
