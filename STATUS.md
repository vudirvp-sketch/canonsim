# STATUS — canonsim

Iteration: 6a (`iter-6a-code-audit`) · Phase: 0 — closed (gate: **PASS**,
iter-6) · Date: 2026-08-28 · owner-requested audit of iter-5/6 (the
iter-2a/iter-4a precedent).

Audit scope: re-verify the iter-5/6 deliverables end-to-end. Reproduced:
298 tests green + ruff clean; the 1000-sim balance baseline **exactly**
(M5 p50=0.77, emergent_chains p50=20, M3_mean p50=13.81, M1 p50=0.24,
M4_repetition p50=0.18, suspicion peaks, destroyed-locations); T8 OFF =
26 emergent chains (ON fires `director_0000`, logs byte-differ, M2=0.5);
the chronicle is PYTHONHASHSEED-independent (0/1/42/random); the session
doors + the KI#17 feed gate are correct in code; `tale_gate=low` and the
medium-gate count (4 events) match the T7 claims. Three drift bugs found
+ fixed as KI#22/23/24 — all in citing documents, not in the numbers.
Mandatory §5/§6 cleanup: KI#17–20 deleted (closed >2 iterations); KI
entries trimmed to the 2-line cap; FAQ 24→20 (merged families + the new
chain-counting law).

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index; the log writer is the
  only canon-write path (D-031).
- INV-2 Determinism: single point of randomness control — one master seed;
  named streams derived via the RngBank (`stable_hash` = sha256-based);
  no wall-clock; `sorted()` iteration; fixed `PYTHONHASHSEED`; queue key
  `(tick, sub_order, actor_id)`; cosmetic draws never desync canon replay
  (D-028 — AGENTS.md §4 is the single reading owner).
- INV-3 Content/code split: no domain words in engine code (`core/` +
  `sim/`); all setting data in `content/tavern_pack/`; the periphery dirs
  (`render/`, `cli/`, `scripts/`) carry pack paths/help text/prose by
  design (D-046).
- INV-4 LLM boundary: no LLM/network calls in track A — executable against
  every package dir incl. `scripts/` since iter-6a (D-046).
- INV-5 Log immutability: committed logs are never edited; corrections are
  new events.

## Active KIs

- KI#22 · TEST_PLAN + test_t8_ab docstrings drifted from the shipped gate
  facts (seed "32"→125 ×4; chains "24"→26 ×2; the M2 formula contradicted
  MVP_SCOPE §15 + the impl; §6 filename) — CLOSED iter-6a (worklog; §1.2
  gained the per-endpoint counting note).
- KI#23 · `scripts/` outside the executable invariants + the false
  "AGENTS §9" citation (README/TEST_PLAN/D-044) + the 5–15%/73–83%
  qualifier loss — CLOSED iter-6a: D-046; PACKAGE_DIRS += scripts; the
  closure test; the CLI-class print exemption (MVP_SCOPE §18).
- KI#24 · dead `fold_events` export with a false docstring in
  `core/metrics.py` — CLOSED iter-6a: removed (L13/L14).
- KI#4 · balance harness — CLOSED iter-6: `scripts/balance_harness.py`
  (1000-sim distribution; reproduced exactly by the iter-6a audit);
  baselines M5 p50=0.77, chains p50=20, M3_mean p50=13.81, M1 p50=0.24.
- KI#21 · draft templates drifted from the shipped event contract —
  CLOSED iter-5 (inverted suspicion line, `[` collision, steal object);
  fixed as pack data before any renderer existed.

## FAQ / Pitfalls

- **Crossings fire in tick order, not by type (iter-4 law, D-038).**
  Rotations and beats interleave by tick; the loop picks
  `min(candidates)` per iteration; the writer's tick-monotonicity
  invariant forbids out-of-order commits. Same rule for any future
  clock-crossing system.
- **Autonomous intents enqueue at entry.tick, never beat_tick (D-039) —
  and NEVER advance the playscript (KI#17).** Urgency/director intents
  enqueue at `entry.tick` (sub_order NPC_REACTION); decay commits
  directly at beat_tick; the runner feeds the next step only on the
  PLAYER's own step endings.
- **Director releases ride the intent door, not the canon door (D-037).**
  A released hook = IntentData (`director_<N>`) through the front door
  (rejections emit `intent_rejected` no-ops with `cause_intent`); the
  director never bypasses Intent→Event. Same door for urgencies
  (`urgency_<N>`).
- **Reactions dispatch from the commit door; novelty is per (knower,
  token) (D-037).** `_commit` feeds the knowledge index + runs `_react`
  for EVERY committed event — no call site can forget a reaction;
  cascades terminate; suspicion reacts only to tokens the knower did not
  already hold; the arrest resolution rides the same door.
- **System passes scan the whole projection, not the events that seeded
  them (KI#16 lesson).** Per-layer bookkeeping must be global and
  mergeable by new ignitions, never a frozen snapshot in the queue
  payload. The decay pass scans ALL npcs; its per-axis baseline is the
  tick of the LAST event that changed that axis (KI#19).
- **Hardcoded `from_` is a desync waiting to happen (KI#13 lesson).**
  Read current values from the projection; make repeat effects
  idempotent; the `_commit` gate (D-035) fails loud BEFORE the write.
- **INV-3's stoplist scope (iter-2 interpretation, test-owned; D-046).**
  The stoplist bans setting nouns in the ENGINE (`core/`+`sim/`),
  segment-matched; mechanic words stay legal; the word list is pack-tied
  by a self-check. `render/`/`cli/`/`scripts/` are periphery — pack path
  strings, CLI help examples, docstring prose live there by design
  (INV-3's substance: a second pack requires zero ENGINE changes).
- **The loud/soft front-door line.** Malformed playscript steps raise
  `RunnerError` — author bugs crash. Well-formed but world-impossible
  intents emit `intent_rejected` no-ops — attempts are facts. Director
  rejections emit events (budget consumed); urgency rejections stay
  silent (the world's noise floor absorbs them).
- **The golden T1 fixture is env-pinned; the fixture-regeneration guard
  is the iter-6 discipline (TEST_PLAN §1.1).** The header records the
  Python version — byte-compare only on the generating interpreter;
  regenerate + commit the fixture with env changes. The guard pins (a)
  the fixture header's `schema_version` == the current schema `$id`
  version, (b) a fresh regen byte-diff — a breaking schema change
  without fixture regen fails loudly (§3 migration procedure).
- **Doc drift is evidence, not prescription — verify with
  `git log -S` before acting.** A ref citing a spec section it never
  contained is drift (iter-6a: "AGENTS.md §9 — Script Persistence Rule"
  in README/TEST_PLAN/D-044 — the text bled from the session prompt;
  D-046 supersedes). Pre-D-028 wording and license copies in
  `docs/ref/*`/`REFERENCES_DEEP.md` are historical; the owners are
  AGENTS.md §4 and `REFERENCES.md` (the catalog).
- **Where the code-quality bar lives (D-031).** Law: AGENTS §4+§9
  (invariants, canon-write privilege, DoD). Constitution: BLUEPRINT §2
  (L13/L14). Build clauses: `docs/blueprint/phase0.md` §1/§2/§6.
  Executable: `tests/test_architecture.py` (PACKAGE_DIRS covers every
  top-level code dir — the closure test, D-046) + the stoplist test.
  No new canonical layers (D-018 pattern).
- **GitHub upload / git hygiene (the KI#1 family).** Uploads drop
  `.gitignore` and empty dirs — verify it exists after any upload.
  `git status --short` shows changes vs HEAD, not what IS in HEAD; after
  structural changes run `git ls-files <path>`.
- **Content/tone questions → D-030 + the `PACK_SPEC.md` sketch row.**
  Tone is data asymmetry inside existing systems; growing the pack or
  writing a pack spec before its trigger = scope creep (AGENTS §2.4;
  SPECS_BACKLOG header rule). Grim material waits in `pack-1` (phase 6 /
  2nd setting).
- **Doc-loop alarm vs owner-requested research.** Consecutive doc-only
  iterations force a stop (AGENTS §2.5); a fresh owner request is the
  documented exception (D-022). Code iterations never fire the alarm.
- **Four places, four jobs (D-027).** `REFERENCES.md` catalogs;
  `CORE_DESIGN_RESEARCH.md` §2 synthesizes (one line per source);
  `docs/ref/<source>.md` carries mechanics; `BLUEPRINT.md` +
  `docs/blueprint/` carry resolutions. Link, never restate; cite ledger
  row IDs (e.g. "per RNG-1").
- **Substance over line count (D-025) + per-ref split (D-026).** The cap
  is 600 with the §6.1 substance filter as the real law — filler is cut
  always; named systems, field lists, enum values, per-source verdicts
  are never cut to fit.
- **"Ref graveyard" check (iter-0x audit method).** Grep a sample of
  ledger terms across the planning docs — every term must land in at
  least one; mechanics stay owned by `docs/ref/` (D-027). Verified
  iter-0x.
- **The read-side layers are pure functions of the log (iter-5/6 laws).**
  Every render entry point builds a fresh `RngBank` from the log HEADER
  seed — same log → same bytes in any process/`PYTHONHASHSEED`; a
  growing log keeps its rendered prefix (the session delta-print rides
  on this). A session is one opened Simulator: `open`/`run_steps`/
  `close`; session == batch bytes; `seed <n>` starts a NEW log (INV-5).
  `core/metrics.py` reads `(events, projection)` — the simulator never
  knows a metric exists (L3; Mesa DataCollector inverted).
- **Gate mechanics: the T8 single-factor A/B + the balance harness
  (iter-6 laws).** Same playscript/seed (125), only the director flag
  changes: ON fires `director_0000`; OFF keeps seeding (D-005) and
  produces ≥3 emergent chains (baseline 26); the logs byte-differ. The
  harness is a script, not a test (a 1000-sim sweep would dominate the
  suite); kill-criteria operationalize as M3 mean ≥2, M1 non-trivial,
  M2 non-zero.
- **The emergent-chain count is per qualifying endpoint; decay
  self-chaining inflates M3 (iter-6a).** Each non-PC, non-director event
  whose maximal backward cause-walk reaches a player root with ≥2
  non-PC links counts once — one decay cascade (consecutive
  `status_decayed` cause-chained per the beat rule) contributes several
  endpoints, and M3's magnitude is decay-dominated. The directionality
  targets (≥3 chains; M3 ≥2) are unaffected; phase-1 tuning reads
  composition, not just totals.

## Next step

**Phase-0 gate: PASS** (iter-6; audit-clean iter-6a). Track A is
feature-frozen at phase-0 scope. **Phase 1 (narrator over the log)** is
the next track-A work (`ROADMAP.md` §2); the pre-trigger
`BRIEF_SPEC.md`/`VALIDATION_SPEC.md` sketches in `SPECS_BACKLOG.md` fire
AT phase-1 start. **Track B (`bg-1..bg-4`) is unblocked** for parallel
LLM-circuit spikes on DF Legends XML.

Phase-1 intake backlog (none block phase 0): `doc-1` VISION freeze
review; the DECISIONS ≤30 collapse per D-034 (46 entries now — over cap,
rationale recorded D-045(a), due at the intake); the rest-action
candidate (`pack-2`-style pack data); `qa-1` mypy (owner-gated);
`ci-1` GitHub Actions; `perf-1` 10k-tick profile; the iter-7+ tuning
knob (importance rule hooks for story-critical events, D-045(b)).
