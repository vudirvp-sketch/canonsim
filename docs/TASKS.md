# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2.

## Track A — main (simulator, no LLM)

### iter-1 · core plumbing (sprint days 3–4) — todo

- Seed → single `random.Random(seed)` instance; integer clock; `heapq` queue
  keyed `(tick, sub_order, actor_id)`; JSONL append-only writer with header
  (no wall-clock); playscript runner (seed + ordered intents);
  pack loader for the drafted `content/tavern_pack/` v0.1 (entities from
  `MVP_SCOPE.md` §4 — that table is the source of truth; pack data landed in
  iter-0c).
- Tests: T0 schema validation (the EVENT_SCHEMA example is a fixture; the log
  header shape per EVENT_SCHEMA §1 is validated as a separate fixture), minimal
  T1 (two runs byte-identical), smoke boot.
- AC: world creates from seed; an event writes; a playscript plays end-to-end;
  `pytest -q` green.

### iter-2 · actions (days 5–6) — todo

- The 12 actions with checks/outcomes/durations (`MVP_SCOPE.md` §7);
  pack-driven preconditions; event emission for each; INV-3 grep stoplist
  test.
- AC: steal / arson / talk = facts in the log with knowledge records;
  impossible stays impossible (T5 partial).

### iter-3 · knowledge (days 7–8) — todo

- Knowledge records; transfer with fidelity decay; suspicion / relations
  updates; watch-change transfer; NPC memory driving behavior (guards act on
  suspicion thresholds).
- AC: characters know different things and react differently; T3 blind-NPC
  passes.

### iter-4 · director (days 9–10) — todo

- Consequence buffer seeded at event time; triggers (time / place /
  threshold); stagnation detector releases; director on/off switch.
- AC: seeded hooks fire causally; no "from nothing" complications; T4
  irreversibility passes.

### iter-5 · chronicle & CLI (days 11–12) — todo

- Template chronicle from the log; scene card; CLI: `play`, `look`, `wait`,
  `chronicle`, `state`, `replay`, `directors on|off`, `seed`.
- AC: playable and readable without LLM.

### iter-6 · gate (days 13–14) — todo

- Full T1–T8; director-off A/B on identical seed + playscript; M1/M2 metrics
  report (thresholds set from baseline); manual playtest; phase-0 verdict in
  `worklog.md`.
- AC: exit criteria `MVP_SCOPE.md` §16 all hold — or kill-criteria documented
  honestly.

## Track B — background (evenings, foreign canon)

### bg-1 · DF export pipeline — todo

- DF Classic (free) + DFHack `exportlegends info` → 2–3 worlds → XML → SQLite
  parser. Watch for: HEX errors after fortress play (export from clean legends
  mode), hundreds of MB per large world, translated-name layers.
- AC: parser loads a world into SQLite; pitfalls recorded in
  `docs/TECH_NOTES.md` §3.

### bg-2 · event taxonomy — todo

- 100–300 interesting events across ~16 types (birth, death, murder, theft,
  betrayal, artifact creation, site destruction, war, journey, captivity,
  escape, founding, item loss, madness, transformation, catastrophe); per
  event: participants, place, cause, witness, long-term consequence,
  expressibility in our ontology → `docs/TAXONOMY.md`.
- AC: ≥100 entries. Honest note baked in: causality is *reconstructed* from
  `event_collections` + role fields, not parsed.

### bg-3 · briefer spike — todo

- Mini-briefer "tell battle X from figure Y's POV, knowing only Y's own
  records" + reverse validation (invented-facts count, regeneration count) +
  retrieval stress test (tens of MB of XML).
- AC: harness runs; numbers in `docs/TECH_NOTES.md`. Expectation to keep
  honest: DF canon is macro-dense and micro-empty — this validates briefer
  *mechanics*, not micro-event interestingness (measure that on our own dry
  chronicle).

### bg-4 · cost notes — todo

- Park et al. 2023 + "Generative Agent Simulations of 1,000 People" (2024)
  figures → `docs/TECH_NOTES.md` cost section.

## Infra backlog (post-sprint, pick by need)

- `ci-1` GitHub Actions: pytest + ruff on push (`PYTHONHASHSEED=0`, pinned
  Python).
- `perf-1` 10k-tick timing profile (target: seconds, not minutes).
- `doc-1` VISION freeze review after the phase-0 verdict.
- `doc-2` REFERENCES.md license/URL re-verification, quarterly (alongside the
  TECH_NOTES review).

## Done

- iter-0 · 2026-08-25 · docs & tooling bootstrap (this pack).
- iter-0b · 2026-08-25 · owner-requested docs review: error fixes + external
  source catalog (`docs/REFERENCES.md`).
- iter-0c · 2026-08-25 · owner-requested rev v2 merge: REFERENCES §14
  layer/priority map, D-017, TECH_NOTES §6; `content/tavern_pack/` v0.1
  drafted (entities, actions, rules, templates).
- iter-0d · 2026-08-25 · owner-requested infra restore: `.gitignore` + package
  skeleton + pack/schema smoke tests; pyproject package-discovery fix (KI#1,
  KI#2 closed).
- iter-0e · 2026-08-25 · owner-requested core-design research:
  `docs/CORE_DESIGN_RESEARCH.md` (reference synthesis, depth equation, gaps
  P1–P3, open questions Q1–Q4 for the owner).
