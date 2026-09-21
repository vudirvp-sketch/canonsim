Iteration: iter-178 (`iter-178-presentation1` + `iter-177-engine1b`, the
owner's batched call over the two named tasks): presentation-1's spec
WRITTEN from the measured results — `docs/PRESENTATION_SPEC.md` (the
model-facing serializer contract over the stable brief IR, the D-055
pattern's fourth instance; st-4 absorbed: the call budget, the
no-tail resolution, thinking-as-ephemeral, the Script Tax clause; the
three consult cards integrated — intake-30 the visual fence, intake-32
the re-expansion mapping, intake-33 the outcome-perception layers,
no shape changed) — and engine-1 (b) LANDED before it (iter-177,
D-193): the GBNF mapping repo-side (`brief/gbnf.py` + the golden
fixture), the explicit adapter `cli/engine.py` (INV-4 lifted to the
one-module form — the AGENTS §4/§8 edits riding), the `--engine` door
wiring (the file contract preserved, ZERO gate edits), the
failure→ladder mapping (the runtime re-ask ×1 + D7's degradation
rungs), the provenance manifest, the contract collapsed (CONTRACTS §4
the pointer).
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §2/§6) ·
1960 passed + 1 skipped, ruff clean (Python 3.12.14, the env pin;
verified at BASE_COMMIT 446603d BEFORE working — 1926+1 green, ruff
clean — and re-verified after with the diff in place: 1960+1 green
(the +34 the two engine-1 packets: the GBNF mapping + the adapter
contract tests), ruff clean, docguard clean) ·
Date: 2026-09-21 ·
Scope: brief/gbnf.py + brief/parser.py + cli/engine.py + cli/main.py +
tests/test_gbnf.py + tests/test_engine.py + tests/test_architecture.py +
tests/fixtures/parse_gbnf_seed125.gbnf + scripts/regen_parse_gbnf.py +
docs/PRESENTATION_SPEC.md + AGENTS.md + docs/PARSER_SPEC.md +
docs/BRIEF_SPEC.md + docs/VALIDATION_SPEC.md + docs/CONTRACTS.md +
docs/TEST_PLAN.md + docs/TECH_NOTES.md + docs/AGENT_NAVIGATION.md +
README.md + docs/DECISIONS.md + docs/TASKS.md + `STATUS.md` + worklog.md
— 24 paths, the build over the §2.3 soft limit (the landing + the spec
+ their state docs, the owner's batched call). The prior iterations'
record: iter-176 (doc-3), iter-175 (docrev1). The detail lives in the
worklog + git.

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

**iter-177/178 DONE: engine-1 (b) the build landing (D-193 — the GBNF
mapping + the adapter + the wiring + the ladders, INV-4 lifted) +
presentation-1's spec written (PRESENTATION_SPEC, st-4 absorbed). The
standing queue's two named rows closed by the owner's batched call.**

1. The landed surface's station verification (the owner's next engine
   session): the first live `--engine` run — the grammar's compile
   check at the real backend, the session manifest, the heartbeat's
   brief/parse component split; the 27B GBNF parse arm + the
   one-model-constrained A/B (TEST_PLAN §8.5's gap rows, CONTRACTS
   §4.3 arm a).
2. The standing frames: Track B's gap rows (the bg-7 prose families,
   the per-family latency distribution), the world track's frontier
   (WORLD_WORKPLAN §6 — the embodiment options, W5's live band, the
   camp's meso half), the debt-1 residues (each a future row's own
   call), the SoW horizon (bg-6, owner-deferred). New rows enter on
   the owner's call only.
