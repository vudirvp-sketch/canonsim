Iteration: iter-176 (`iter-176-doc3` — the owner's declared doc-3
build, the cleanup the iter-175 audit routed to): the state-layer
reassembly LANDED — STATUS's FAQ essays to one-liners + owner links
(NAV §3's own law), the two unique operational recipes moved to
TECH_NOTES §14/§15, TASKS's three history ledgers dead (git owns
them; a guard-capped one-line ledger tail remains), the standing rows
de-historized (engine-1's rounds a closure clause + pointers),
worklog re-trimmed to the 3–5-line entry law, README's phase block
to one-liners + the repo map to function level, the DECISIONS
D-034/D-185 collapse 31→30 with D-119's 8.4k intake restatement a
pointer to phases.md §6, and the mechanical cap guard LIVE
(`scripts/docguard.py` + `tests/test_docguard.py` — the recurrence
fix the iter-140/151 GC passes lacked).
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §2/§6) ·
1926 passed + 1 skipped, ruff clean (Python 3.12.14, the env pin;
verified at BASE_COMMIT 2687465 BEFORE working — 1916+1 green, ruff
clean, the iter-175 pin re-confirmed — and re-verified after with the
diff in place: 1926+1 green (the +10 the docguard test packet),
doc + tooling only, ruff clean) ·
Date: 2026-09-21 ·
Scope: docs/TASKS.md + `STATUS.md` + worklog.md + README.md +
docs/DECISIONS.md + docs/TECH_NOTES.md + scripts/docguard.py +
tests/test_docguard.py + scripts/digest.py (the landings parser
adapted to the ledger one-liners) + docs/AGENT_NAVIGATION.md §1 (the
scripts row) — 10 paths, doc + tooling. The prior iteration's record:
iter-175 (docrev1 — doc-3 OPENED). The detail lives in the worklog +
git.

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
- INV-4 LLM boundary: no LLM/network calls in track A — executable against
  every package dir incl. `scripts/` since iter-6a (D-046).
- INV-5 Log immutability: committed logs are never edited; corrections are
  new events.

## Active KIs

- (None open. KI#88/#89 — qa-1's holes — CLOSED iter-169 at load-lint;
  deleted iter-172 per AGENTS §5's 2-iteration cleanup law.)

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

**iter-176 DONE: doc3 — the state-layer reassembly landed (doc-3
CLOSED): the FAQ essays one-liners + owner links, the recipes to
TECH_NOTES §14/§15, the three TASKS ledgers dead, the DECISIONS
collapse 31→30, the cap guard live. The standing queue unchanged.**

1. **engine-1 (b)**: the build landing — the GBNF mapping repo-side +
   the door wiring + the failure→ladder mapping, INV-4 lifting there
   with the AGENTS §4/§8 edits riding it (CONTRACTS §4 the boundary;
   §4.3's claim packet F the build's evidence; the adapter contract
   tests fire at the build).
2. **presentation-1's write**: the exit criterion MET (iter-174 — the
   narrator floor measured between E4B and Q9B); the spec fires from
   the measured results per D-022 (TECH_NOTES §13.1 the material; the
   three consult cards: intake-30/32/33).
3. The standing frames: Track B's gap rows (the bg-7 prose families,
   the per-family latency distribution), the world track's frontier
   (WORLD_WORKPLAN §6 — the embodiment options, W5's live band, the
   camp's meso half), the debt-1 residues (each a future row's own
   call), the SoW horizon (bg-6, owner-deferred). New rows enter on
   the owner's call only.
