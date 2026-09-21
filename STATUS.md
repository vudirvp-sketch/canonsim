Iteration: iter-179 (`iter-179-engine1-round5`, the owner's bundle —
the first LIVE `--engine` session, the landed surface's station
verification at an off-plan model): round 5 triaged — the GBNF
grammar's live compile + enforcement VERIFIED through the landed
wiring (TEST_PLAN §8.5's compile-check gap row discharged), the
provenance manifest end-to-end (model_sha256 null — the server's
relative path), the parse door's whole vocabulary exercised (intents
fed + the world's honest `intent_rejected` answers + a clarification
question); the narrator door FAILED 2/2 (prose, not the reply document
— the E4B class at a nominal 12B, one datum) and exposed KI#90:
`cli/mediator.py::apply_reply` raised MediatorError on a non-JSON
reply BEFORE the gate family — the engine cycle died with the beat
open (D7's mapping hole; round 4's runner-side json-retry ladder had
masked the class). FIXED: the JSON class routes to the MALFORMED regen
ladder (the note riding each re-invocation, exhaustion to the template
rung — never a blocked beat), the unreadable-FILE class stays the
operator error; the pins in test_mediator + the stub-server round-5
replay (test_engine). TECH_NOTES §13.1 the round-5 record.
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §2/§6) ·
1962 passed + 1 skipped, ruff clean (Python 3.12.14, the env pin;
verified at BASE_COMMIT cf6b6fd BEFORE working — 1960+1 green, ruff
clean — and re-verified after with the diff in place: 1962+1 green
(the +2 KI#90's pins), ruff clean, docguard clean) ·
Date: 2026-09-21 ·
Scope: cli/mediator.py + tests/test_mediator.py + tests/test_engine.py
+ docs/TECH_NOTES.md + docs/TEST_PLAN.md + docs/TASKS.md + `STATUS.md`
+ worklog.md — 8 paths (the KI fix + its pins + the round record + the
state docs, over the §2.3 soft limit). The prior iterations' record:
iter-177/178 (engine-1 (b) + presentation-1), iter-176 (doc-3). The
detail lives in the worklog + git.

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
  `sim/` + `brief/` — the mediator circuit joined the stoplist at
  iter-10a); all setting data in `content/tavern_pack/`; the periphery
  dirs (`render/`, `cli/`, `scripts/`) carry pack paths/help text/prose
  by design (D-046).
- INV-4 LLM boundary — the explicit adapter: the network surface is
  EXACTLY ONE module, `cli/engine.py` (engine-1's landing, D-193);
  everything else stays network-free and engine-agnostic — AGENTS §4
  the law owner, the architecture test the executable.
- INV-5 Log immutability: committed logs are never edited; corrections are
  new events.

## Active KIs

- KI#90 · a non-JSON narrator reply blocked the beat (round 5) ·
  opened+CLOSED iter-179 (JSON → the MALFORMED regen; the file class unchanged).

## FAQ / Pitfalls

> One-liners + the owner link (NAV §3's duplication rule); the essays
> restated their named owners (doc-3). The operational recipes live in
> TECH_NOTES §14 (live-session) + §15 (corpus-regen).

- **Read-side folds (echo/traits) never feed entropy/channel inputs (L6/EPIST-1, iter-46/55); the intent door is the only legal path** — DIRECTOR_SPEC §4; the one legal render: BRIEF_SPEC §3.5.
- **Chronicle conditionals read FLAT context keys; a checked action's verdict is NESTED (`outcome.check.passed`) — the branch EVENT TYPE is the carrier (iter-43)** — `render/tracery.py`.
- **Validator verdicts follow CURRENT canon, never the anchor (iter-9); invented = contradicted, unmodeled = insufficient_data** — VALIDATION_SPEC §4–§5; the call budget §7.
- **Crossings fire in tick order (co-occurring: the coarsest clock first — macro → rotation → beat); director/urgencies ride the INTENT door, reactions the COMMIT door (D-037/38/39)** — BRIEF_SPEC §3.2/§3.3; KI#17 (git).
- **System passes scan the whole projection, never the seeding events (KI#16); the decay baseline = the last axis-changing event's tick via the (entity, prop) → tick index (KI#19, D-050)** — D-050's record.
- **Hardcoded `from_` is a desync (KI#13/KI#46): repeat effects idempotent; the carried-item position contract single-owned by `movement_changes`; the `_commit` gate fails loud before the write (D-035)** — `core/resolvers.py`.
- **INV-3's stoplist: no setting nouns in the ENGINE (`core/`+`sim/`+`brief/`, segment-matched, pack-tied word list); `render/`/`cli/`/`scripts/` are periphery (D-046)** — the stoplist test owns enforcement.
- **Malformed playscript steps raise RunnerError; well-formed but world-impossible intents emit `intent_rejected` (attempts are facts); urgency rejections stay silent** — PARSER_SPEC §4/§6.
- **The golden T1 fixture is env-pinned: byte-compare only on the generating interpreter; the regen guard pins schema_version + a fresh byte-diff** — TEST_PLAN §1.1 (§3 the migration).
- **Doc drift is evidence, not prescription — verify with `git log -S` AND the pinning test before acting (KI#42/48/51/80); bootstrap texts are convenience copies, never a second source** — D-024/D-027.
- **The code-quality bar: AGENTS §4/§9 the law, BLUEPRINT §2 (L13/L14) the constitution, test_architecture + the stoplist test the executable; no new canonical layers (D-018)** — D-031.
- **Git hygiene: verify `.gitignore` after any upload; a file DELETION needs an explicit `git rm` in the report block or it never lands (KI#55); `git status --short` before every commit** — AGENTS §7.
- **Scope-creep guards: content/tone → D-030 + PACK_SPEC's sketch row; two consecutive doc-only iterations stop unless a fresh owner request fires (D-022)** — AGENTS §2.
- **DF exports are malformed/truncated CP437 XML: byte-sanitize, stream with iterparse + clear, tail-check truncation; off-matrix record tags render UNDOCUMENTED** — the matrix: `docs/ref/df_legends_xml.md`; the recipe: TECH_NOTES §3.1–§3.3.
- **The cap laws: substance over line count — filler cut always; named systems/field lists/enum values/verdicts never cut to fit; a breach triggers a cruft pass first** — AGENTS §6/§6.1; enforced by `scripts/docguard.py`.
- **The read-side layers are pure: render rebuilds the RngBank from the header seed; the assembler zero-RNG over (log, ledger) (D-049); retrieval a pure fold, `knower` IS known_by (D-088)** — BRIEF_SPEC §2/§3.3.
- **The scene ledger: commit → retire_contradicted → sync_scene → assemble → narrator → apply_delta (auto-syncs; re-asserting terminal states = laundering, refused); the ledger dies with its session (D-139)** — BRIEF_SPEC §3.3.
- **Gate mechanics: seed 125, only the director flag changes — ON fires `director_0000`, OFF ≥3 emergent chains (baseline 24); M3 counts per endpoint, decay-dominated in magnitude** — TEST_PLAN §4 + the D-136 verdict row.

## Next step

**iter-179 DONE: round 5 triaged — the first live `--engine` session
(the landed surface's station verification at an off-plan 12B): the
compile check discharged, KI#90 (the blocked-beat mapping hole) found
+ fixed.**

1. The remaining station rows (the owner's next engine run, TEST_PLAN
   §8.5's standing gaps): the 27B GBNF parse arm + the
   one-model-constrained A/B (CONTRACTS §4.3 arm a) + the brief/parse
   component split; a narrator-convention model for live narrate play
   is the same run's choice (round 5's 12B datum: prose, not the reply
   document — §13.1).
2. The standing frames: Track B's gap rows (the bg-7 prose families,
   the per-family latency distribution), the world track's frontier
   (WORLD_WORKPLAN §6 — the embodiment options, W5's live band, the
   camp's meso half), the debt-1 residues (each a future row's own
   call), the SoW horizon (bg-6, owner-deferred). New rows enter on
   the owner's call only.
