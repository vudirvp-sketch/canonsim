# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.

---
iter-0 · 2026-08-25 · bootstrap
- Created the docs & tooling pack: README, AGENTS, STATUS, worklog,
  AGENT_NAVIGATION, VISION, MVP_SCOPE, EVENT_SCHEMA, ROADMAP, TASKS,
  TECH_NOTES, DECISIONS, SPECS_BACKLOG.
- Added `schemas/event.schema.json`, `pyproject.toml`, `.gitignore`, and the
  directory skeleton (`core/`, `sim/systems/`, `content/tavern_pack/`,
  `render/`, `brief/`, `cli/`, `tests/playscripts/`).
- Next: iter-1 core plumbing per `docs/TASKS.md`.

---
iter-0b · 2026-08-25 · owner-requested docs revision
- Review pass over all docs (cross-refs, invariants, schema sync): fixed the
  dangling `npc_market_crowd_01` entity (MVP_SCOPE §4.2 ambient-entity note);
  clarified the header-shape test target (TASKS iter-1).
- Added `docs/REFERENCES.md`: curated external-source catalog from the owner's
  survey, licenses verified 2026-08-25 (two passes: web search, then GitHub
  search-by-exact-name + raw LICENSE probes); wired into ROADMAP §4,
  AGENT_NAVIGATION, README, DECISIONS D-016.
- Owner-caught miss fixed: Labyrinthia-AI, ReputeX-Engine and Echo DO exist —
  restored into §9. Pass-1 SEO search misses small repos (lesson in §11, D-016).
  Still unverified: StrobeServer, Story-Engine, Astray-as-Lua (misattributed).
- Next: iter-1 core plumbing per `docs/TASKS.md`.

---
iter-0c · 2026-08-25 · owner-requested rev v2 merge + tavern pack data
- REFERENCES.md: added §14 (layer/priority map, Must/Should/Could); rev-v2
  sources admitted with "verify" licenses (sqlite-vec, nomic-embed-text,
  bge-m3, cross-encoder rerankers); qdrant demoted to server-infra-only; FTS5
  noted on SQLite; §13 phase-4 row updated; owner policy in §0.7 (inspiration,
  never 1:1). D-017 records the merge policy + v2→ROADMAP phase mapping.
- TECH_NOTES §6: static-lore retrieval stack + phase-1 QA metric ideas.
- content/tavern_pack/ v0.1 drafted as data: entities (5 locations, 6 NPCs +
  crowd, 5 items), 12 actions, rules (time/visibility/relations/knowledge/
  states/fire/watch/director/importance), starter chronicle templates.
  AGENT_NAVIGATION §1, README map, TASKS iter-1 wording synced (loader
  consumes the drafted pack). 13 files touched — over the 3–5 soft limit,
  owner-requested scope.
- Doc-loop alarm (AGENTS §2.5): three docs/data iterations in a row — iter-1
  must be functional code.
- Next: iter-1 core plumbing per `docs/TASKS.md`.

---
iter-0d · 2026-08-25 · owner-requested infra restore (KI#1, KI#2)
- Recreated `.gitignore` (logs/, output/, `*.jsonl` with tests/fixtures/
  exception, caches) and the package skeleton (core/, sim/systems/, render/,
  brief/, cli/, tests/, tests/playscripts/) — both lost in the initial zip
  upload (KI#1). 12 files touched — over the 3–5 soft limit, owner-requested.
- First executable tests: tests/test_smoke.py — pack data integrity + event
  contract shape (13 tests). Fixed pyproject.toml package discovery so
  `pip install -e ".[dev]"` works (KI#2 — the DoD gate was unreachable).
- pytest -q green, ruff check . clean, editable install OK.
- Next: iter-0e core-design research, then iter-1 core plumbing.

---
iter-0e · 2026-08-25 · owner-requested core-design research
- Added `docs/CORE_DESIGN_RESEARCH.md`: reference synthesis (18 sources →
  depth primitives + failure modes), composition principle, depth equation,
  phase-0 audit, proposals P1–P3 (M3/M4/M5 metrics, npc↔npc relations, goal
  ticker, detail callbacks), open questions Q1–Q4.
- Conclusion: the phase-0 ontology is already depth-first; real gaps are
  execution details (P1) plus three small P2 additions — owner decision
  pending on Q1–Q4.
- AGENT_NAVIGATION §1/§3 updated (new doc + ownership row).
- Next: owner answers §8 questions; iter-1 core plumbing per `docs/TASKS.md`.
