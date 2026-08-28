# STATUS — canonsim

Iteration: 8a (`iter-8a-scene-ledger-design`) · Phase: 1 · Date:
2026-08-28 · owner-requested design pass (the D-022 exception) on the
session-continuity question: a long scene loses narrator-invented
texture because the brief is a pure function of the log and "free
texture at low importance" (`VISION.md` §5) had no storage. Outcome:
D-048 — the **scene ledger** (mechanism owner `docs/blueprint/phases.md`
§1): a session-scoped, append-only, mediator-owned second stream;
discrete lifecycle states; canon always outranks texture; promotion
only through the intent door; laundering refusal; no TTL; dies with
the session. Pattern source absorbed as ref-16
(`docs/ref/agent_memory_atlas.md` — the owner-supplied 151-system
memory survey, MIT verified via GitHub API). Spec triggers synced
(SPECS_BACKLOG VALIDATION_SPEC row + BRIEF_SPEC §9 deferral);
sequencing added to TASKS. Docs-only iteration — no doc-loop alarm
(iter-8 was code-heavy); 329 tests green, ruff clean, fixture
byte-identical.

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

- KI#25 · stale `_enqueue_autonomous` docstring — "fires at the beat
  tick itself" contradicted the entry-tick law (D-039, the `_run_beat`
  docstring, the FAQ) — CLOSED iter-7: rewritten in place.
- KI#26 · dead-parameter family (L14, the KI#24 precedent):
  `Director.releases(knowledge)` — the signature falsely implied the
  director reads knowledge records (L6 forbids it); `briefing_draft(projection)`;
  `urgency_intents(beat_tick)`; `_axis_deltas(pack)` — CLOSED iter-7:
  params removed, call sites + tests updated; fixture byte-identical.
- KI#27 · README drift: "298 tests" (iter-6a made 299) + "systems land
  iter-2" (the systems live in `core/` per D-037; `sim/systems/` stays
  reserved) — CLOSED iter-7.
- KI#28 · residual instance of the KI#23 false citation: AGENT_NAVIGATION
  §1 `scripts/` row still cited "AGENTS.md §9 — Script Persistence Rule"
  (superseded by D-046; iter-6a fixed README/TEST_PLAN/D-044 but missed
  this one) — CLOSED iter-7: row rewritten to the true owner (TEST_PLAN §6).
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
- KI#4 deleted at iter-8 (closed iter-6 — more than 2 iterations).

## FAQ / Pitfalls

- **Crossings fire in tick order, not by type (iter-4 law, D-038).**
  Rotations and beats interleave by tick; the loop picks
  `min(candidates)` per iteration; the writer's tick-monotonicity
  invariant forbids out-of-order commits. Same rule for any future
  clock-crossing system. The read-side mirror of the beat law:
  `brief/assembler.py` `last_beat_tick`/`beats_crossed` reproduce the
  same beat set (intraday offsets repeated daily; an offset of 0
  belongs to day 1+, never t=0) — owner `BRIEF_SPEC.md` §3.2, tested.
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
- **Four places, four jobs (D-027) + the ref-graveyard diagnostic.**
  `REFERENCES.md` catalogs; `CORE_DESIGN_RESEARCH.md` §2 synthesizes
  (one line per source); `docs/ref/<source>.md` carries mechanics;
  `BLUEPRINT.md` + `docs/blueprint/` carry resolutions. Link, never
  restate; cite ledger row IDs (e.g. "per RNG-1"). The audit method:
  grep a sample of ledger terms across the planning docs — every term
  must land in at least one; verified iter-0x.
- **Substance over line count (D-025) + per-ref split (D-026).** The cap
  is 600 with the §6.1 substance filter as the real law — filler is cut
  always; named systems, field lists, enum values, per-source verdicts
  are never cut to fit.
- **The DECISIONS gate-collapse is ID-preserving (D-034, iter-7 law).**
  Family merges write compound IDs with the FULL prefix on every member
  (`D-018/D-022/D-029` — `D-018/022/029` does NOT resolve); compressed
  rows keep decision→why→consequence and link the single owner of the
  detail (D-024 anti-drift: spec-restatement in a decision row is
  duplication, not substance). Pre-collapse history lives in git.
  Due again at the phase-1→2 gate.
- **The read-side layers are pure functions of the log (iter-5/6/8 laws).**
  Every render entry point builds a fresh `RngBank` from the log HEADER
  seed — same log → same bytes in any process/`PYTHONHASHSEED`; a
  growing log keeps its rendered prefix (the session delta-print rides
  on this). A session is one opened Simulator: `open`/`run_steps`/
  `close`; session == batch bytes; `seed <n>` starts a NEW log (INV-5).
  `core/metrics.py` reads `(events, projection)` — the simulator never
  knows a metric exists (L3; Mesa DataCollector inverted). The brief
  assembler goes further: **zero RNG at all** (dry structured tokens,
  L2 — `brief/assembler.py`, BRIEF_SPEC §2); its recall `max_items` is
  a ranking cap (the O(relevance) top-k), NOT a budget drop — the
  `[truncated:N]` marker counts budget drops only.
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

**Phase 1 continues** — the plan's single owner is `docs/TASKS.md`
(Track A: iter-9+ = VALIDATION_SPEC + the validator's LLM-free half —
fact transaction, ExpectedVersion OCC, ≤2 regens, INSUFFICIENT_DATA
default, golden-set plumbing; then the scene-ledger LLM-free half —
`brief/ledger.py` + the `scene_texture` 7th block + fixture-shaped
deltas, per D-048/blueprint §1 — the narrator LLM boundary itself
remains an AGENTS §8 owner checkpoint, INV-4 holds until then, and it
carries the ledger's live wiring). Track B (`bg-1..bg-4`) stays
unblocked in parallel — note bg-1 needs the owner's local DF Classic
+ DFHack setup (world export cannot run in this sandbox). Backlog
that did NOT land in iter-8a (each stays in its TASKS home, none
blocks iter-9): `doc-1` VISION freeze review; `qa-1` mypy + `ci-1`
GitHub Actions (owner-gated, AGENTS §8); `perf-1` 10k-tick profile;
`tune-1` rest action + the D-045(b) importance-rule knob; the
BRIEF_SPEC §9 deferrals (relevance signal, lore scheduling grammar,
precondition-filtered options, exemplar refresh cadence — all arrive
with the mediator, never early).
