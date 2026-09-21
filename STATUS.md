Iteration: iter-185 (`iter-185-tallyread` — the world track, the camp's
first embodiment; the owner's «можешь продолжать мир трек»
continuation call over STATUS's embodiment routing — the natural
doc-streak breaker after two doc-only iterations, the iter-167
precedent's own reading): the tally's read gap ANSWERED at the pack
band as pure pack data, zero core — the `read_tally` hinge (the read
hinge family's fourth instance, the pole's item-kind class: the grim
read_ticket, the pole, the stair, now the tally) + the tally-stick
itself (`camp_tally_01`, the notch habit's own class, the seat's
badge carried by the master — the paper names the master, the camp
reads the seat) + the secrets registration (`the_camps_word` over
the master, type debt, the weighing season's window — the registry's
third key, the first pack with two debt-type subjects): the
re-weigh's proof, the crisis probe's tally leg now on a committed
surface (the count public, the withhold harder to keep — the count
prices trust, never coin). The WORD minted, never the PRESENT count
(the read_stair precedent's LAW-never-PRESENT boundary; the freight's
volume stays owner-routed); the camp's own read mints nothing (the
crews' lived knowledge not event-recorded, INV-1; the holder !=
subject guard); the tally unflagged (the pole's steal_target
boundary deliberately NOT duplicated — the proof is not pocketable).
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §2/§6) ·
1979 passed + 1 skipped, ruff clean (Python 3.12.14, the env pin;
verified at BASE_COMMIT 5b44f78 BEFORE working — 1969+1 green, ruff
clean, docguard clean — and re-verified after with the full diff in
place) ·
Date: 2026-09-22 ·
Scope: content/province_pack/actions.json + entities.json +
templates.json + rules.json + tests/test_tallyread.py +
docs/worldbuild/ANCHOR_REGION.md + docs/worldbuild/WORLD_TESTS.md +
docs/worldbuild/WORLD_WORKPLAN.md + STATUS.md + worklog.md +
docs/TASKS.md — 11 paths (the family's embodiment form — iter-167's
own nine-path shape plus entities.json (the tally-stick committed
with the hinge) and the three worldbuild state docs the unit's
record owns; over the 3–5 soft limit, noted per AGENTS §2.3). Track
A and track B untouched this session — the world track a separate
track (D-186, never a second queue). The prior iterations' record:
iter-184 (charcoal1), bg-9 (apiprose), iter-183 (residues34),
iter-182 (intake-35), iter-181 (intake-34), iter-180 (round 6),
iter-179 (round 5), iter-177/178 (engine-1 (b) + presentation-1).
The detail lives in the worklog + git.

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

(none — KI#90 deleted per AGENTS §5: closed iter-179, more than two
iterations elapsed at this STATUS touch)

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

**iter-185 DONE: the camp's first embodiment — the tally's read (the
`read_tally` hinge + the tally-stick + the secrets registration over
the master, the re-weigh's proof — ANCHOR_REGION §6.4, WORLD_TESTS
§9's record, `tests/test_tallyread.py`).**

1. The remaining station rows (the owner's next engine run, TEST_PLAN
   §8.5's standing gaps): the 27B GBNF parse arm + the
   one-model-constrained A/B (CONTRACTS §4.3 arm a) + the brief/parse
   component split; the narrator-convention call for live narrate
   play is two-sided now — more live beats at Q9B (size the tail) or
   the 27B as the one-model candidate (the §1 sweet spot, both
   doors) — the owner's choice (round 5's 12B + round 6's 9B data:
   §13.1; bg-9's mapping-drift datum rides the same decision).
2. The standing frames: the world track's frontier — W5's human tests
   (the live band: the meaning distribution's unfinished half, a real
   reader) and the embodiment options (the owner's call class: the
   camp's two remaining gaps — the account, the freight volume, the
   debt-1 residue class each a future row's own call; the older
   units' — the step's notch record/hatch, the kin's own), the
   debt-1 residues (each a future row's own call — the camp's account
   the class's newest member), the SoW horizon (bg-6, owner-deferred —
   long-parked per the owner's 2026-09-21 call). Track B's gap rows
   all closed (round 4 + bg-9). New rows enter on the owner's call
   only.
3. The intake-34/35 residues (each behind its own trigger, never a
   default): the ref-file deep record — a named row consuming a
   specific math-catalog mechanism family (the per-card pass done at
   intake-35, the families re-confirmed at HEAD; Experiment 0's
   verdict + R1's landing close the other two residues — phases.md
   §6).
