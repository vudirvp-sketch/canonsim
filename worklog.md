# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.

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
iter-0y · 2026-08-27 · owner-requested content-principles pass (D-030)
- D-030: darkness = architecture, not content scripts — `tavern_pack` v0.1
  unchanged; tone = data asymmetry (price markers, irreversibility,
  per-NPC rumor damage, D-006 held); grim/romance line = post-gate
  `pack-1` candidate (TASKS infra backlog) + PACK_SPEC sketch clauses;
  consent/coercion = crafted records (D-008 pattern). Core corollary for
  iter-1..3: axis-blind (pack-declared axes/statuses/event vocabulary).
- 6 files touched — over the 3–5 soft limit: 2 targets (DECISIONS,
  SPECS_BACKLOG) + the mandated sync set (STATUS, worklog, TASKS, README
  status drift — same pattern as 0w/0x). KI#7/KI#8 deleted (closed >2
  iterations); external LLM romance-pack proposal evaluated in chat, verdict
  distilled into D-030 (insight kept, scope creep fenced off). No code;
  pytest green, ruff clean. 24th docs iteration (owner-requested, D-022);
  **iter-1 code is next, unconditionally**.
---
iter-0x · 2026-08-27 · owner-requested reference-influence traceability audit
- Verdict: load-bearing — 4-place chain verified (docs/ref/ → synthesis →
  blueprint → TASKS/SPECS clauses); ledger-term spot-greps all land in
  planning docs; INV-2 rewrite (D-028) is the constitutional proof; plan
  review found no new blockers beyond KI#3/4/5. Caveats: no code yet
  (iter-1 = the proof point); P2c owner-pending; rules.json flat stagnation
  timer → narrative entropy at iter-4 (phase0 §4). FAQ: ref-graveyard grep
  diagnostic.
- 4 files touched (STATUS, worklog, TASKS, README). No code; pytest green,
  ruff clean. 23rd docs iteration (owner-requested, D-022); **iter-1 code is
  next, unconditionally**.
---
iter-0w · 2026-08-27 · owner-requested post-reference concept realignment (D-029)
- Verdict recorded: skeleton (phases 0–6, 3 layers, INV-1..5) stands; the
  blueprint is the single post-reference mechanics owner. Drift fixed
  (KI#9 opened/closed): sprint calendar dropped (MVP_SCOPE §17
  iteration-counted, TASKS day-tags removed); CORE_DESIGN_RESEARCH →
  absorbed; ROADMAP §2 → blueprint pointer; README Status → 0w; D-029.
- 9 files touched — over the 3–5 soft limit: the mandated sync set (STATUS,
  worklog, TASKS, AGENT_NAVIGATION) + the five realignment targets; same
  pattern as iter-0u/0v. No code; pytest green, ruff clean. 22nd docs
  iteration (owner-requested, D-022); **iter-1 code is next, unconditionally**.
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
