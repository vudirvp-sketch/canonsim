# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.
> Order: newest first (normalized at iter-8c — the order had drifted
> since iter-5).

---
iter-8c · 2026-08-28 · owner-requested audit of iter-8a/8b (iter-8c-audit)
- All claims reproduced: 329 green, ruff clean, T1 byte-identical; the
  8b "2 false alarms" verdict verified against pre-8b git state (the
  (log, ledger) purity flip WAS already in BRIEF_SPEC §9/D-048); atlas
  MIT re-verified via the GitHub API. 3 KIs fixed: KI#30 — the D-018c
  letter-suffix citation never resolved (the KI#23/#28 false-citation
  family, propagated by 8b into D-049/worklog/phases.md; the lettering
  died at the iter-7 D-034 collapse, and even pre-collapse the
  structural boundary was D-018(b)) → plain D-018, 4 sites; KI#31 —
  blueprint §1 wording debts (stale 8a "pinned never auto-evicted"
  remnant vs the D-049 ledger-never-evicts resolution; lifecycle
  notation now matches the precedence/texture-OCC paragraphs:
  {active, pinned} → terminal states); KI#32 — sync misses (TASKS
  ref-N line gained ref-16; BLUEPRINT BRIEF-1 gained the atlas donor
  line + corpus count per its own §0 deep-dive protocol).
- Verdict on the owner's question: NO rework of iter-1..8 needed —
  the 7th block lands additively (assembler Block/fill/eviction shape
  verified; zero new event types; the atomic flip set is enumerated in
  BRIEF_SPEC §9). Worklog reordered to strict newest-first. 6 files —
  audit fix set + mandated sync set (iter-6a precedent); docs-only,
  the D-022 fresh owner request (iter-9 stays the code iteration).
- 329 tests green, ruff clean, golden fixture byte-identical. No new
  DECISIONS entries (drift fixes, not decisions); DECISIONS stays
  33/30 transiently (collapse at the phase-1→2 gate, D-034).
---
iter-8b · 2026-08-28 · scene-ledger hardening (iter-8b-scene-ledger-hardening)
- Owner-requested dispute-resolution pass on an external LLM review of
  D-048: claims audited against the repo (2 false alarms — the purity
  flip was already in BRIEF_SPEC §9/D-048; "zero RNG" was never a
  log-determinism claim), 4 real gaps + 3 wording debts + 2 missed
  gaps (establishment-time canon check; texture-OCC mirror) → KI#29,
  closed same iteration. D-049: seven resolutions hardening the
  scene ledger in place — determinism quarantine, scene =
  PC-location interval, structural pinning, grammar/vocabulary split
  (core stays ledger-blind), render-vs-epistemics,
  ledger-never-evicts (bounds live in the brief),
  tombstones-in-brief; every resolution reuses existing law
  (D-018/D-035/D-037/D-047/L12/atlas).
- 7 files — the mechanism owner (blueprint/phases.md §1) + the
  mandated sync set (DECISIONS D-049, BRIEF_SPEC §9 atomic flip set,
  SPECS_BACKLOG VALIDATION_SPEC sketch, TASKS iter-9+, STATUS incl.
  KI#22–28 deletion, this worklog). Docs-only — the D-022 fresh
  owner request (no doc-loop alarm; iter-9 is code).
- 329 tests green, ruff clean, golden fixture byte-identical.
  DECISIONS transiently 33/30 (collapse at the phase-1→2 gate, D-034).
---
iter-8a · 2026-08-28 · scene-ledger design pass (iter-8a-scene-ledger-design)
- Owner-requested continuity question (long scenes lose narrator texture;
  the brief is log-pure): absorbed the owner-supplied memory atlas as
  ref-16 (`docs/ref/agent_memory_atlas.md`, MIT verified) and designed
  the scene ledger into `docs/blueprint/phases.md` §1 — session-scoped
  append-only mediator stream, discrete states, canon outranks texture,
  intent-door promotion, laundering refusal, no TTL (D-048).
- Spec triggers synced (SPECS_BACKLOG VALIDATION_SPEC row, BRIEF_SPEC §9
  deferral) + TASKS sequencing + intake sync set (REFERENCES,
  REFERENCES_DEEP, CORE_DESIGN_RESEARCH §2, AGENT_NAVIGATION §1).
  12 files — task-mandated design set + the intake/sync set (iter-8
  precedent). Docs-only (D-022 owner-request exception).
- 329 tests green, ruff clean, golden fixture byte-identical. DECISIONS
  transiently 32/30 (collapse due at the phase-1→2 gate, D-034).
---
iter-8 · 2026-08-28 · BRIEF_SPEC + brief assembler (iter-8-brief-spec-assembler)
- docs/BRIEF_SPEC.md (trigger fired at phase-1 start: six-block pipeline,
  two-level budgets — soft fill target / hard per-item ceiling /
  total_hard whole-block eviction with `[truncated:N]` markers and
  never-drop-directives, voice isolation L2, max_items = ranking cap not
  budget drop, §9 just-in-time deferral table) + brief/assembler.py
  (pure functions of the log, ZERO RNG — byte-identity on the golden
  fixture across calls, PYTHONHASHSEED-independent; beat arithmetic =
  the read-side mirror of the loop's day-1-edge law) + rules.json::brief
  pack contract (budgets + directives/lore/exemplars text) +
  core/pack.py::_brief lint (BRIEF_BLOCK_IDS closed enum) +
  tests/test_brief.py (30 tests). D-047 recorded — DECISIONS transiently
  31/30 mid-phase (iter-1 precedent; collapse due at the phase-1→2 gate).
- 13 files — task-mandated set (spec + assembler + pack + tests + lint)
  + the AGENTS §6 sync set (TASKS/SPECS_BACKLOG/AGENT_NAVIGATION/STATUS/
  worklog/README/DECISIONS). 299→329 tests green, ruff clean, golden
  fixture byte-identical.
---
iter-7 · 2026-08-28 · phase-1 intake (iter-7-phase1-intake)
- Owner-requested retrospective at the phase boundary: baseline
  re-verified (299 green + ruff clean), then the D-034-mandated
  DECISIONS collapse 46→30 (ID-preserving family merges; compound IDs
  use the FULL prefix per member — `D-018/022/029` does not resolve,
  the FAQ law); 55KB→20KB. TASKS.md regained the what-next ownership
  (phase-1 sequence: iter-8 BRIEF_SPEC + brief assembler; iter-9+
  VALIDATION_SPEC; tune-1 knobs); STATUS Next step → pointer.
- Intake audit fixes: KI#25 stale `_enqueue_autonomous` docstring
  (beat-tick claim vs the entry-tick law); KI#26 dead-parameter family
  (Director.releases knowledge — L6-dangerous false interface;
  briefing_draft projection; urgency_intents beat_tick; _axis_deltas
  pack) removed with call sites + tests; KI#27 README drift (298→299,
  "systems land iter-2"); KI#28 residual false "AGENTS §9" citation in
  AGENT_NAVIGATION §1 (the KI#23 family — iter-6a missed this instance).
  KI#21 deleted (closed >2 iters); FAQ: ref
  places + graveyard merged (20 held), the collapse law added.
- 13 files — intake fix set + mandated sync set (precedent: iter-4a/6a).
  299 tests green, ruff clean, golden fixture byte-identical (dead
  params — no canon-path change).
---
iter-6a · 2026-08-28 · owner-requested code audit of iter-5/6 (iter-6a-code-audit)
- Re-verified end-to-end: 298 green + ruff clean reproduced; the 1000-sim
  baseline reproduces EXACTLY; T8 OFF = 26 chains / ON = director_0000;
  chronicle PYTHONHASHSEED-independent; session doors + KI#17 gate
  correct; tale_gate claims accurate (medium → 4 events).
- 3 KIs fixed: KI#22 TEST_PLAN/test-docstring drift (seed 32→125 ×4,
  24→26 ×2, M2 formula vs MVP_SCOPE §15 + impl, §6 filename, §1.2
  per-endpoint note); KI#23 scripts/ outside the executable invariants
  + the false "AGENTS §9" citation + the 5–15%/73–83% qualifier loss
  (D-046; PACKAGE_DIRS += scripts + closure test + CLI-class print
  exemption, MVP_SCOPE §18 pinned); KI#24 dead fold_events removed.
- KI#17–20 deleted (closed >2 iters); KI entries to the 2-line cap; FAQ
  24→20 (purity/drift/fixture/gate families merged + the chain-counting
  law added). 11 files — audit fix set + mandated sync set.
- Tests 298→299 green (+1 closure test); ruff clean; golden fixture
  byte-identical. No canon-path change: the drift was in citing
  documents, not in the numbers.
---
iter-6 · 2026-08-28 · phase-0 gate (iter-6-gate) · **VERDICT: PASS**
- TEST_PLAN.md (trigger-fired spec: T0-T8 + M1-M5 + gate protocol + UAP
  crosswalk + §3 schema-bump migration) + core/metrics.py (M1-M5 +
  emergent chains as pure functions of the log) + test_metrics.py (24)
  + the T1 fixture-regeneration guard + tests/playscripts/day1_full.json
  (seed 125) + test_t8_ab.py (single-factor A/B) +
  scripts/balance_harness.py (KI#4 close) + rules.json::metrics.
  11 files — task-mandated. D-042/D-043/D-044/D-045 recorded.
- Tests 264→298 green (+34); ruff clean; golden fixture byte-identical.
  T7 playtest + the full verdict evidence live in D-045; the 1000-seed
  baseline numbers live in D-044 + STATUS KI#4 (M5 p50=0.77, chains
  p50=20, M3_mean p50=13.81, M1 p50=0.24). Track A frozen.
---
iter-5 · 2026-08-28 · chronicle & CLI (iter-5-chronicle-cli)
- render/tracery.py (CHRON-1: tracery grammar, modifiers, save/restore,
  ink conditionals + ShufflePool no-immediate-repeat on the cosmetic
  stream) + render/chronicle.py (tale = pure function of the log: fresh
  bank from the header seed per pass, day headers, importance gate,
  scene card, ungated entity views) + cli/main.py + __main__.py (batch
  play/chronicle/state/replay + interactive session: look, wait N,
  directors on|off, seed). core/loop.py → open/run_steps/close
  (session == batch bytes, tested); policy_from_rules owns the entropy
  floor. templates.json completed into the grammar; KI#21 closed
  (draft-template drift: inverted suspicion line, '[' collision, steal
  object); display names gained articles (pack data). 12 files —
  task-mandated module set + sync set.
- Tests 225→264 green (+39: tracery units incl. cosmetic-audit + cycle
  guard, chronicle gate/prefix-stability/T1-chronicle, CLI batch +
  session + directors A/B on seed 32); ruff clean; golden fixture
  byte-identical; chronicle verified PYTHONHASHSEED-independent.
  Balance observation for KI#4/balance-1: player fatigue is monotonic
  over long waits (no rest action in v0.1) — visible through the
  readable chronicle.
---
iter-4 · 2026-08-28 · director + goal ticker (iter-4-director-goal-ticker)
- core/director.py + core/urgencies.py + core/states.py (D-038:
  director = event-driven + clock-crossing releases; D-039: urgencies
  through the intent door, band NPC_REACTION; D-040: arrest resolution
  via evasion_vs_pursuit) + loop rewire: clock crossings fire in TICK
  ORDER (rotations + beats interleave by tick, not by type — the log
  writer's tick-monotonicity invariant); director seeds at commit time
  (_react extension); beat cycle fires decay / urgencies / director
  release per beat. Pack: director.hooks (weight/threshold/trigger/
  intent), urgencies.entries (probability/intent/preconditions),
  crime_watch.arrest.resolution_* (caught_value irreversible). Templates
  +arrest_resolved, +status_decayed. DIRECTOR_SPEC.md written (trigger
  fired). 20 files — task-mandated module set + sync set.
- Tests 187→219 green (+32: director, urgencies, states suites; arrest
  test updated for the resolution behavior change); fixture
  byte-identical (plumbing_smoke crosses no beat — no decay/urgency/
  release). D-038/D-039/D-040 recorded; STATUS FAQ gains the tick-order
  + entry.tick-enqueue laws.
---
iter-3 · 2026-08-28 · knowledge, relations, expectations (iter-3-knowledge-relations)
- core/knowledge.py + core/crime.py (D-037: kernel mechanics — the
  import-boundary law beats the old sim/systems plan note) + loop rewire:
  reaction cascade in the commit door (crime → telling), clock-crossing
  watch rotations (swap + expectations + briefing with one-step decay).
  Pack: expectations/telling/suspicion mapping/rotation/pair seeds/
  movement sighting templates; arrest threshold single owner. Fold: pair
  + crime_status seeding. 16 files — task-mandated module set + sync set.
- Tests 155→187 green (+32: T3, transfers, expectations, OCC e2e, lint);
  fixture regenerated (move records — deliberate); KI#3 + KI#12 closed;
  states decay deferred to iter-4; arrest resolution parked (TASKS).
(iter-2a deleted at iter-8c per the one-in/one-out cap; history in git.)
(iter-2 deleted at iter-8b per the one-in/one-out cap; history in git.)
(iter-4a deleted at iter-8a per the one-in/one-out cap; history in git.)
(iter-0aa deleted at iter-7 per the one-in/one-out cap; history in git.)
(iter-1 deleted at iter-8 per the one-in/one-out cap; history in git.)
