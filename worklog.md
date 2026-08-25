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

---
iter-0f · 2026-08-26 · owner-requested manifesto absorption (4 surgical edits)
- No new doc — the manifesto lands where it belongs: (a) BRIEF_SPEC sketch
  in SPECS_BACKLOG gets sensory-emitter + beat-boundary delta clause; (b)
  VALIDATION_SPEC sketch gets prompt-injection neutralized structurally
  (prose→proposal boundary, grammar-constrained Intent, no post-hoc text
  sanitization — that path is a crutch); (c) CORE_DESIGN_RESEARCH §6 gets
  P3e `psychological_echo` as a phase-3+ behavior modifier derived from
  existing knowledge records (not new data); (d) STATUS FAQ gets a
  `git ls-files` pitfall (workspace ≠ tracked).
- Files: docs/SPECS_BACKLOG.md, docs/CORE_DESIGN_RESEARCH.md, STATUS.md,
  this file, docs/DECISIONS.md (D-018). AGENT_NAVIGATION unchanged — no
  structural change.
- Doc-loop alarm: 5th docs iteration in a row. iter-1 MUST be functional
  code; no further docs iterations without an owner request.
- Next: iter-1 core plumbing per `docs/TASKS.md`.

---
iter-0g · 2026-08-26 · owner-requested research pass (Q1–Q3 yes, Q4 no)
- Owner answered CORE_DESIGN_RESEARCH §8 Q1–Q4: M3/M4/M5 → iter-6 (D-019);
  NPC↔NPC relations → iter-3 (D-020); goal/urge ticker → iter-3/4 (D-021);
  one more research pass before iter-1 (D-022, doc-loop exception). KI#1,
  KI#2 deleted per AGENTS §5 (closed ≥3 iterations).
- Audit of owner's critique vs repo: 3 real gaps logged as KI#3
  (expectation_violation), KI#4 (balance harness), KI#5 (runtime-vs-fold).
  ~55% of critique already in docs; ~20% mistimed. §2 deepened (Mesa,
  Neighborly, Red Blob, Game Programming Patterns); P1e/P2d/P2e/P3f new.
  7 files touched — over the 3–5 soft limit, owner-requested scope.
- Files: STATUS, worklog, CORE_DESIGN_RESEARCH, DECISIONS, TASKS,
  SPECS_BACKLOG, MVP_SCOPE. AGENT_NAVIGATION unchanged. No code touched.
- Next: iter-1 core plumbing per `docs/TASKS.md`; no further docs iterations
  without an owner request.
