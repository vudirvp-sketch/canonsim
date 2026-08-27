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
iter-1 · 2026-08-28 · core plumbing — first functional code (iter-1-core-plumbing)
- core/{schema,rng,ids,clock,queue,log,fold,pack,loop}.py: RngBank guards
  (assure/audit/peek/fingerprint), band-ordered heapq, cause-checked JSONL
  writer (write-time schema validation, gap-free ids, stamped knowledge
  sources), incremental projection + fold (T2), pack loader + minimum lint,
  playscript runner (movement/wait resolvers; the ten check-bearing actions
  land iter-2). actions.json gained `resolver` keys (INV-3 mapping in data).
- Tests: architecture fitness (import boundary, RNG monopoly, network ban,
  print ban), T0 (doc examples extracted at test time), T1 minimal
  (byte-identical + committed golden fixture tests/fixtures/
  plumbing_smoke_seed42.jsonl), core units, loop e2e — 78 green, ruff clean.
  KI#10 closed (D-032 stdlib validator); KI#5 closed (STATE-1 built);
  D-033 (P2c → iter-3); D-034 (DECISIONS cap: collapse at gates).
  24 files — over the 3–5 soft limit (task-mandated module set + the
  AGENTS §6 sync set); DECISIONS at 34 entries, over cap per D-034 until
  the phase-0 gate collapse.
---
iter-0aa · 2026-08-27 · owner-requested pre-code doc audit (drift + readiness)
- 11 drift findings fixed as KI#11 (closed same iteration): fabricated
  "1 tick ≈ 12 in-world minutes" citation (phase0 §1 + df_worldgen.md —
  MVP_SCOPE §8 owns 1 tick = 1 minute, 1440/day); calendar remnants
  (ROADMAP §4 "week 1" → bg-1; MVP_SCOPE §13 "day 3"; TASKS "post-sprint");
  TASKS Done gap (iter-0f line restored per git e16c9ab); P3c mislabels
  (phase0 §2, EVENT_SCHEMA §11); MVP_SCOPE §5 system-3 npc↔npc pair map
  (D-020); AGENT_NAVIGATION tests/fixtures + playscripts rows; README
  "empty" → "skeletons".
- KI#10 opened (stdlib JSON-Schema validation engine for T0 + pack loader;
  owner decision). Readiness verdict: rigging complete, iter-1
  unconditionally next. 10 files touched (targets + mandated sync set,
  same pattern as 0v/0z). No code; pytest green, ruff clean. 26th docs
  iteration (owner-requested, D-022).
---
iter-0z · 2026-08-27 · owner-requested quality round (D-031)
- INVARIANT-CORE v3 + Elegant Solutions absorbed per the D-018 pattern:
  L13/L14 (BLUEPRINT §2); phase0 §1 type discipline + fail-fast + the
  `tests/test_architecture.py` fitness test, §2 ActionResolver registry,
  §6 negative tests; AGENTS §4 INV-1 canon-write privilege + §9 quality
  DoD; stack frozen through phase 2; mypy parked as owner-gated `qa-1`;
  TECH_NOTES §7 log-as-stream; REFERENCES §15 principle donors.
  Contradictions between the two provided analyses resolved in D-031
  (no new canonical files; no mypy in CI; Upcaster covered; INV-1 stands).
- 10 files touched — over the 3–5 soft limit: 5 targets + the mandated
  sync set (STATUS, worklog, TASKS, README, REFERENCES §15) — same
  pattern as 0v/0w/0y. DECISIONS at 31 entries (>30 cap): every row a
  distinct stable decision, append-only forbids the cut — kept over per
  AGENTS §6.1, rationale here. KI#9 deleted (closed >2 iterations).
  No code; pytest green, ruff clean. 25th docs iteration (owner-requested,
  D-022); **iter-1 code is next, unconditionally**.
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
- docs/TEST_PLAN.md (NEW: trigger-fired spec — T0-T8 formalization,
  M1-M5 definitions, gate protocol, UAP 7-hole crosswalk, §3 schema-
  bump migration procedure). core/metrics.py (NEW: M1-M5 + emergent-
  chain count as pure functions of (events, projection) — Mesa
  DataCollector inverted; system classification is pack data at
  rules.json::metrics.system_of_type). tests/test_metrics.py (NEW, 24
  tests). tests/test_t1_determinism.py EXTENDED with the iter-6
  fixture-regeneration guard (schema_version pin + fresh regen byte
  diff). tests/playscripts/day1_full.json (NEW gate playscript, seed
  125). tests/test_t8_ab.py (NEW: single-factor A/B, ≥3 emergent
  chains OFF, director_0000 ON, M5 non-zero OFF, M3 mean ≥2 both).
  scripts/balance_harness.py (NEW: KI#4 close — 1000-sim distribution
  harness; outputs to output/balance_<N>_seed<S>_<on|off>.txt). Pack
  data: rules.json gained metrics.system_of_type. 11 files — over the
  3-5 soft limit; the task mandated it (T1+T8+metrics+harness+spec
  +sync). D-042/D-043/D-044 recorded.
- Tests 264→298 green (+34); ruff clean; golden fixture byte-identical.
  T7 manual playtest (this entry): the day1_full chronicle reads as a
  story — enter tavern → take lamp → fail 2 steals → succeed → watch
  rotation → knowledge transfer to relief guard → wait → arson → fire
  chain → second rotation back to Doren → drift → Day 2. The noise floor
  is high (15 status_decayed + 4 urgencies 'wait' on a 48-event log);
  tale_gate.min_importance="medium" is too sparse (only 4 events —
  fire_chain + pickpocket_failed — survive). Verdict: the gate stays
  at "low"; the first iter-7+ tuning knob is the IMPORTANCE RULE
  itself (give story-critical events hooks, not the gate threshold).
  Balance baseline (1000 seeds): M5 p50=0.77, emergent_chains p50=20,
  M3_mean p50=13.81, M1 p50=0.24 — see output/balance_1000_seed100_off.
  Phase-0 verdict: PASS (all §16 exit criteria met; no kill-criteria
  hit). KI#4 closed (balance harness delivered). Track A frozen.
