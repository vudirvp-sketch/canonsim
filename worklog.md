# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.
> Entries re-trimmed to the line cap at iter-10a (KI#37; the drift ran
> iter-8b→10) — pre-trim detail lives in git history.
> Re-trimmed 39→10 at iter-48 (KI#68: the cap had drifted silently —
> the iter-43..47 "evicted per the cap" claims never executed; the
> eviction is now verified in the same edit, not claimed). Pre-trim
> history lives in git.
> Order: newest first (normalized at iter-8c — the order had drifted
> since iter-5).



---
iter-65 · 2026-09-06 · phase-4 gate — the verdict PASS (D-094; the
owner's "final check of everything before closing and preparing for
phase 5" call; 6 files — one over the soft limit: verdict + collapse
+ sync are the gate's one doc-debt mechanism, the iter-54 pattern)
- Full ROADMAP §5 protocol re-run green: the corpus 105 + parse
  corpus (1178 collected — 1168+1 module skip pure-dev, 1177+1
  offline-probe skip with [chronicler]; ruff clean); the seed-125
  pair ON M1=0.509/M2=0.333 / OFF T8 26 chains — IDENTICAL to
  iter-54 (the phase-4 landings kept the corpus price zero on the
  committed scenario); stretch max 1 both arms; T1 double-run
  byte-identical; T7 a story; 0 leaks on the blind suite (26 tests,
  all four layers); the mode-F chronicler 53/53 through the count
  gate, manifest content-derived.
- Doc debts paid: TASKS 626→589 (the phase-4 ledger collapse — the
  trim the iter-61..64 rows deferred to this gate), DECISIONS 30
  held (D-094 joins the verdict family), FAQ 20 held, README
  resynced (KI#73 opened+closed: tex-1/blind-1/leg-4 unrecorded).
- ROADMAP §2: phase 4 CLOSED, phase 5 UNLOCKED (opens on the
  owner's call). No runtime file touched. Doc-only streak 1 of 2.
---
iter-64 · 2026-09-06 · leg-4 — the mode F offline chronicler (phase 4,
TASKS' last phase-4 row; the owner's explicit duckdb approval crossing
the §8 dependency fence — the recorded leg-4/blind-1 owner-gate
resolved; 10 files — over the soft limit: tool + fence + extra + tests
+ doc sync are one mechanism family, the iter-60..63 scope pattern)
- scripts/chronicle.py (NEW): read_ndjson_auto no-ETL intake behind a
  count gate (a silent drop = integrity failure, nothing written);
  events.parquet (canonical 12-column archive), state_diffs.parquet
  (the LAG/LEAD window-diff, the continuous fold read), chronicle.
  sqlite (facts_summary/state_current/type_histogram/knowledge_
  summary/chronicle_meta) via the attach→stdlib probe+fallback ladder
  (autoinstall off — never phones home), manifest.json (content-
  derived, no wall-clock, no abs paths). pyproject [chronicler] extra
  (duckdb>=1.0, runtime deps stay []); D-012 executable
  (test_runtime_imports_stdlib_only).
- Measured: 55/55 events day1 seed 123 (all intake combos); state
  continuity 0 breaks; both write paths byte-deterministic per run,
  logically identical; corpus price zero by construction.
- +10 tests/test_chronicle.py (stdlib-fold cross-checks, determinism,
  ladder, gates; importorskip — pure-dev env 1168+1 skip); 1167→1178,
  ruff clean. D-093 (family, cap 30 held); TEST_PLAN §7; TASKS leg-4
  done + scav-1 deferred (TASKS 626 — over the 600 cap per the §6.1
  phase-ledger pattern, the collapse at the phase-4 gate, the iter-63
  precedent at 606); AGENT_NAVIGATION; iter-54 evicted; 10 after.
---
iter-63 · 2026-09-06 · blind-1 — the blind-NPC leak suite's phase-4
extension (phase 4; the STATUS fork leg-4/blind-1 resolved by law:
leg-4 names DuckDB = the §8 dependency fence (the owner's explicit
call), blind-1 the exit criterion's instrument, dependency-free —
the dir-2 precedent)
- tests/test_blind.py (+26, the new file): the leak predicates
  (pure test-side folds — the multiset delta law, the record-quad /
  trait-provenance fact laws, the retrieval-row law) + four layers:
  the every-prefix × every-knower 10-seed + golden sweep, the
  adversarial omniscient-query retrieval sweep + the None probe,
  the live drain's anchor-addressed call check (composition +
  leak law), the teeth family (planted leaks flagged).
- docs: TEST_PLAN §1.3 (the T3 extension's contract owner) + the T3
  row pointer; TASKS blind-1 done (606 — over the 600 cap per the
  §6.1 phase-ledger pattern, the collapse at the phase gate, the
  iter-62 precedent at 602); D-092 into the phase family (cap 30
  held); AGENT_NAVIGATION tests row; STATUS Next flip (leg-4
  owner-gated on DuckDB).
- 1141→1167 green, ruff clean; zero leaks measured, the suite ~3s.
  iter-53 evicted (verified in this edit); 10 entries after. KI#72
  deleted per §5 (closed iter-61, two iterations past).
---
iter-62 · 2026-09-06 · tex-1 — the scene_texture window's identity
tier + per-scope quotas (phase 4, TASKS' top row; the owner's
"continue per plans" call; 9 files — over the soft limit: the tier,
the quota, the lint, the pack arming, and the test family are one
mechanism family, the iter-60/61 scope pattern)
- brief/assembler.py::_scene_texture_items: the ranking key widened
  to the identity-or-pinned tier (pack `identity_slots`, the slot a
  class, pinned above identity within the tier; an empty set = the
  pinned-only D-048 bytes) + the quota walk (`per_entity_max_items`
  per entity scope, identity first by construction; scene scopes and
  tombstones unquota'd, the D-047 no-drop law).
- core/pack.py the two-key lint (the required closed set) +
  rules.json the declarative-only arming (speech_pattern/look/
  mannerism, K=2). Measured: the tier live (identity survives
  max_items=1 pressure — the trader problem closed), the quota live
  (the chatty guard capped at 2), the 10-seed day1 A/B
  byte-identical, the narrator corpus 105 + the T1 golden green.
- +23 tests/test_brief.py; 1118→1141, ruff clean. D-091 into the
  phase family (cap 30 held); TASKS tex-1 done + st-2 re-pointed to
  the promotion door; TASKS 602 — two over the 600 cap after the
  family squeeze: the phase-4 done rows are the phase ledger (§6.1,
  kept; the collapse lands at the phase gate, the iter-61 precedent
  at 601). KI#71 deleted per §5. iter-52 evicted; 10 entries after.
---
iter-61 · 2026-09-05 · scene-2 — the mode-B session wiring (phase 4,
TASKS' top row; the owner's "continue per plans" call; 20 files —
over the soft limit: the drain + the door + the query + the pack
arming + the corpus suite are one mechanism family, the iter-60 scope
pattern)
- cli/mediator.py (the drain: the cast snapshot at the player's
  accept, one actor call per NPC, live presence re-verification, the
  drop law, one budget per exchange) + the actor step key through the
  door (core/loop.py, KI#17's exact intent-id law) +
  feedable_intents' caller gate (brief/mediator.py).
- The keyword query: recall_query (brief/scene.py) + the assembler's
  relevance term (pure overlap, rung-independent) + the ladder's
  first runtime query — the actor calls' query:/retrieval: lines.
- Measured: the drain live on seed 7 (guard → barkeep → close); the
  caller's event committed; the corpus price zero (10-seed A/B, the
  corpus 105 + T1 untouched). +33 test_scene; 1085→1118, ruff clean.
  D-090 into the phase family (cap 30 held); TASKS scene-2 done +
  tex-1 re-pointed. TASKS 601 — one over the 600 cap after the
  done-row collapse, two squeezes, and a phase-3-verdict de-dup pass:
  the remaining rows are phase-ledger substance (§6.1, kept). iter-51
  evicted; 10 entries after.
---
iter-60 · 2026-09-05 · scene-1 — the scene manager + mode B (phase 4,
TASKS' top row; the owner's "continue per plans" call; 14 files —
over the soft limit: the queue + the parameterization + the pack
arming + the leak suite are one mechanism family, the iter-59
scope pattern)
- brief/scene.py (NEW — the chorus queue: presence/pack/kind gates,
  pack order, the per-beat cap, the L12 beyond-cap rung) + the
  knower parameter on assemble_brief/narrator_call (mode A
  byte-identical; mode B the actor's own perception/memory/role/voice;
  the actor: protocol line) + rules.json chorus+actors (5 NPCs) +
  the _brief lint family.
- Measured-first: the leak surface ZERO (6 windows × 5 actors on day1
  seed 123); the queue live (the watch change swaps the guard by
  PRESENCE); the corpus price zero (mode A byte-identical vs the
  block-less copy). The §2 design-review verdict re-affirmed.
- +30 tests/test_scene.py; 1055→1085, ruff clean. D-089 into the
  phase family (cap 30 held); TASKS scene-1 done + the scene-2 row
  (the wiring, the actor reply door, the keyword query). iter-50
  evicted; 10 entries after.
---
iter-59 · 2026-09-05 · retr-1 — the retrieval ladder (phase 4,
phases.md §4's STORE-1 row; the owner's "continue per plans" call,
the §2 verdict standing from iter-58)
- core/retrieval.py (NEW) + the _retrieval lint + rules.json::retrieval
  (α=β=γ=δ=1.0, knn_k=8, no vectors — D-012): the FTS5 index + the
  vec probe/scan/floor chain + the pack-coefficient re-ranker; the
  knower query param IS known_by; LEGEND_SPEC §4/§5 live (the stale
  exclusion, the source-outranks demotion).
- Measured-first: the block declarative-only — the 10-seed day1_full
  A/B 10/10 byte-identical (zero corpus price); the live-fire over
  the armed pack (the reflection's 1.77 vs the sightings' 1.15, yet
  demoted below both — the law over the score).
- +25 tests/test_retrieval.py; 1030→1055, ruff clean. D-088 into the
  phase family (cap 30 held); KI#71 (the sqlite-vec license drift,
  REFERENCES §6 + TECH_NOTES §6) opened+closed. iter-49 evicted;
  10 entries after.
---
iter-58 · 2026-09-05 · leg-3b — the tavern reflection set (arming
the v0.1 pack block; the owner's §2 design review first — endorsed)
- content/tavern_pack rules+templates: the live reflection block —
  `sneak_at_work_here`/`figure_reaching_for_purse` (the watcher) +
  `trouble_by_the_bar`/`noise_by_the_bar` (the room), threshold 2;
  `conclusion_drawn` story-critical, renders in the tale.
- Measured-first: the corpus price ZERO (narrator 105 + parse 10 +
  the T1 golden untouched; 8/10 day1 seeds byte-identical, exactly
  123/128 mint 4 events each); the told-conclusion law live (the
  briefing tells the insight, never-re-reflect blocks the re-derivation).
- tests/test_reflection.py: the dormancy test flipped to the armed
  law + 4 committed-pack pins. 1026→1030, ruff clean. LEGEND_SPEC §7
  + TASKS leg-3b done + D-087 into the phase family (cap 30 held).
  iter-48 evicted; 10 entries after.
---
iter-57 · 2026-09-05 · leg-3 — reflection & memory compaction (phase 4,
phases.md §4's memory paragraph; LEGEND_SPEC written just-in-time)
- core/reflection.py (NEW) + the _reflection lint + the loop._react
  wiring (after leverage): reflection-on-recurrence mints ONE event
  per (knower, insight) per run — outcome.provenance the
  list[event_id] handle, the never-re-reflect law, the stale fold,
  expand_reflection the demand side; no RNG, no hooks (L6).
- Measured-first: the recurrence EXISTS (day1_full seeds 123/128);
  the committed pack carries NO block — DORMANT (the arc-1
  precedent): the 10-seed A/B 10/10 byte-identical, zero corpus
  regen; +22 tests/test_reflection.py. 1004→1026, ruff clean.
- LEGEND_SPEC.md (193 lines) + SPECS_BACKLOG flip + TASKS leg-3
  done + the leg-3b arming row (the corpus price tagged) + D-086
  into the D-084/D-085/D-086 family (cap 30 held). iter-47 evicted;
  10 entries after.
---
iter-56 · 2026-09-05 · leg-2 — the brief's derived-trait read, leg-1's
first consumer (phase 4, BRIEF_SPEC's phase-4 clause)
- brief/assembler.py + core/traits.py (+14 tests: 10 brief, 4 traits):
  the PC's crystallized beliefs LEAD recalled_facts as belief lines
  `- belief <token> (t <cross>, sources: <ids>)`, the family records
  render nothing raw; expand_trait the demand side (the expansion
  law). BRIEF_SPEC §3.5 + §3 table + §9 split — same commit (§8).
- Measured-first: the PC holds no family token on ANY committed
  corpus — the 10-seed day1_full A/B (120..129) 10/10 byte-identical
  (brief + log), zero corpus regen; the golden no-belief pin.
- DECISIONS D-085 merged into the D-084/D-085 phase family (cap 30
  held); TASKS leg-2 done; KI#70 (the BRIEF_SPEC self-cap rot,
  389 > the declared 300 at HEAD — the header now reads AGENTS §6)
  opened+closed; KI#69 deleted per §5. 991→1004 tests, ruff clean.
  iter-46 evicted; 10 entries after.
