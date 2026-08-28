# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.

---
iter-4a · 2026-08-28 · owner-requested code audit of iter-3/4 (iter-4a-code-audit)
- Read core (knowledge/crime/director/urgencies/states/loop) + tests
  + pack vs doc owners; probes: 60-seed day1 sweep × director on/off,
  T1 double-runs, T2 folds, crafted records — 124 runs, zero crashes.
  4 KIs fixed: KI#17 autonomous completions fed player steps (feed
  gates on player actor); KI#18 caught→suspect downgrade (flip guards
  the status_values progression); KI#19 reset_on_rotation unimplemented
  (rotation_resets + per-axis last-change decay baseline); KI#20 dead
  pack keys deleted (document_check section, document_check_at,
  spike_on_alarm). 11 files — audit fix set + mandated sync set.
- Tests 219→225 green (+6 regressions), ruff clean, golden fixture
  byte-identical; D-041 recorded; KI#13–16 deleted (closed >2 iters);
  FAQ gains the never-advance-the-script + decay-baseline laws.
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
---
iter-2a · 2026-08-28 · owner-requested code audit of iter-1/2 (iter-2a-code-audit)
- Full read core/ + tests + pack + contracts vs blueprint; claims
  verified; probe-driven hunting (brute-forced seeds). 4 KIs found+fixed:
  KI#13 drop desync + write-before-validate → `Simulator._commit` gate
  (D-035, validate deltas pre-write); KI#14 next_log_path truncation;
  KI#15 pack-lint gaps (use_effect axis, failure_total branches,
  StopIteration guard); KI#16 parallel spread passes (double chance,
  cause=None crash, seed 19) → per-layer singleton pass + shared cause
  map (D-036); repeat smoke/burnout now silent. 15 files — audit fix set
  + mandated sync set.
- Tests 148→155 green, ruff clean; plumbing_smoke + day1 logs
  byte-identical to pre-fix baselines; KI#11 deleted (closed >2 iters).
  Observations parked: arrest-75 duplicated in rules.json (iter-3 picks
  the owner), arson-on-ashes = backlog pack-2, statuses clamp by the
  relations scale (documented INTENT_SCHEMA §6 — owner may veto).
---
iter-2 · 2026-08-28 · actions — the 12, checks, price (iter-2-actions)
- core/{intent,resolvers,transitions,scheduler}.py + loop rewire: front
  door (shape loud / preconditions soft → `intent_rejected` no-ops with
  cause chains), OCC `based_on_event_seq` with breaking-event attribution,
  opposed checks + knowledge templates + preconditions all pack-driven;
  fire = a pack-declared transition layer (generic engine, no layer names
  in code); system-pass DAG with build-time ambiguity check. INTENT_SCHEMA
  written (trigger fired). INV-3 stoplist test (segment matching, pack
  self-check). 20 files — over the 3–5 soft limit (task-mandated module
  set + sync set, same pattern as iter-1).
- Tests 77→148 green, ruff clean; golden fixture survived byte-identical.
  KI#12 opened (OCC lacks a natural e2e trigger until NPC reactions).
  KI#4 gains the first balance observation (low-difficulty environment
  checks auto-succeed at v0.1 numbers). Fix during work: spread-pass spot
  prefix mismatch (prop keys vs spot names) caught by the day1 probe.
---
(iter-0aa deleted at iter-7 per the one-in/one-out cap; history in git.)
(iter-1 deleted at iter-8 per the one-in/one-out cap; history in git.)
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
