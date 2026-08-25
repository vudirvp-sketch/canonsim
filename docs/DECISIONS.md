# DECISIONS.md — ADR-lite

> Append-only. Each entry: decision → why → consequence. Supersede with a new
> entry, never delete. Cap: 30 entries.

| ID | Date | Decision | Why | Consequence |
|---|---|---|---|---|
| D-001 | 2026-08-25 | Repo docs & code in English; owner chat in Russian | token economy, owner request | all agents write English; UI localization is pack data, zero code |
| D-002 | 2026-08-25 | JSON / JSONL + JSON Schema; no XML tooling | Python-stdlib native; the log is JSONL; XML appears only as DF Legends *input* | `schemas/event.schema.json` is the machine contract |
| D-003 | 2026-08-25 | JSONL log = truth; SQLite = derived index | event-sourcing invariant INV-1 | replay = fold(log); the DB can be dropped and rebuilt at any time |
| D-004 | 2026-08-25 | No wall-clock anywhere, including the log header | byte-identical determinism | header carries seed, python, schema_version, commit, pack — no timestamps |
| D-005 | 2026-08-25 | Director = consequence planner, never improviser | causality by construction; RimWorld storyteller = named anti-pattern | complications are seeded at event time; director-off A/B is mandatory (T8) |
| D-006 | 2026-08-25 | No group reputation in v0 | knowledge spread between guards models it | "reputation with the watch" = transfer events at watch change |
| D-007 | 2026-08-25 | Rumor = knowledge transfer with fidelity decay | distortion comes from source incompleteness; no extra system | one mechanic covers gossip and hearsay distortion |
| D-008 | 2026-08-25 | Lies = crafted knowledge records | foundation for `believes/lies` (phase 4) | no truth field on records in v0 |
| D-009 | 2026-08-25 | Prototype pack display names in English | consistency with logs/tests, token economy | final-product localization is pack data only |
| D-010 | 2026-08-25 | 2-place schema sync (EVENT_SCHEMA.md ↔ event.schema.json), test-enforced | anti-drift | the doc example is a test fixture |
| D-011 | 2026-08-25 | No CHANGELOG.md | worklog + STATUS + schema_version cover it | one less file to bloat |
| D-012 | 2026-08-25 | stdlib-only runtime dependencies | determinism, zero supply-chain surface | pytest / ruff as dev-only deps |
| D-013 | 2026-08-25 | Repo name `canonsim` is a placeholder | no strong naming constraint yet | rename before external visibility = one mechanical commit |
| D-014 | 2026-08-25 | Source concept docs live outside the repo | the English distillation (VISION) is the working truth; originals rot and bloat | agents never request the source docs |
| D-015 | 2026-08-25 | License filter lifted; usefulness & phase is the filter | no monetization planned; open bases adapted freely incl. functional re-invention | donors gated by phase (ROADMAP §4); phase 0 uses zero external code |
| D-016 | 2026-08-25 | External source catalog created (`docs/REFERENCES.md`); ROADMAP §4 stays the active shortlist | owner's source survey was rich but unverified (incl. unverifiable and misattributed repos); phase-0 law forbids early intake | admission rule: verify via GitHub search by exact name first (web SEO search misses small repos), licenses tagged with check date; unverified items logged in §11; quarterly review alongside TECH_NOTES |
| D-017 | 2026-08-25 | Owner survey rev v2 merged: layer/priority map added (`REFERENCES.md` §14); rev-v2 sources admitted with "verify" licenses (sqlite-vec, nomic-embed-text, bge-m3, cross-encoder rerankers); phase law unchanged | priorities are owner intent for the final concept and conflict nowhere with phase gating (Must ≠ phase 0); license check deferred by owner to phase-4 intake (D-016 procedure applies then) | qdrant demoted to "server infra only"; rev v2's 6-phase plan maps onto ROADMAP 0–4 + 6 (no depth phase — ROADMAP stays 7-phase); owner policy on record: donors are inspiration/patterns, never 1:1 copies (`REFERENCES.md` §0.7) |
| D-018 | 2026-08-26 | Architecture manifesto absorbed **surgically into existing docs**, not as a new file | a separate manifesto file would rot, duplicate VISION/MVP_SCOPE, and violate the anti-bloat caps (`AGENTS.md` §6); the manifesto's job was to surface four missing pieces, not to become a fifth canonical layer | (a) BRIEF_SPEC sketch gets sensory-emitter + beat-boundary delta — the brief is a perception delta, not a world dump; (b) VALIDATION_SPEC sketch gets prompt-injection neutralized **structurally** (the prose→proposal boundary + grammar-constrained Intent JSON — no post-hoc text sanitization, that path is a crutch); (c) CORE_DESIGN_RESEARCH §6 gets P3e `psychological_echo` as a phase-3+ behavior modifier derived from existing knowledge records — not new data; (d) STATUS FAQ gets a `git ls-files` pitfall (workspace ≠ tracked) |
