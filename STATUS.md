Iteration: iter-186 (`iter-186-campaccount` — the world track, the camp's
account; the owner's embodiment-options call over STATUS's standing
frames — «оставшиеся embodiment-опции лагеря (счёт, объём — каждый
свой ряд)», the account the first of the two called rows): the
charcoal debt's arithmetic ANSWERED at the pack band as pure pack data
over the res-1 substrate (the debt-1 residue class's newest row) — the
master's THIN STOCK (npc_smelter_01, coin 3: the camp's unspent year,
the withhold's own savings, the debt fund's climb toward the charcoal
paper sixteen — the account riding the paper's named holder, the
seat's own purse) + the `the_bloom_nets` net flow (+3 each macro year,
the weighing season's reckoning: the bloom walked to the beam at the
year's turn nets the camp three) + THE FOLD one level deeper (the
gross bloom sale NINE splits as the camp's net THREE and the charcoal
row's standing service SIX — the service minting NO stock, the chest's
one-flow law: a second every-year source into loc_malby's coin would
co-due with the_guild_collects, the D-182 constraint; the notes the
arithmetic's only mirror — ONE SALE, TWO CLAIMS, the guild's claim
double the camp's, the tilted beam's justice uniform across the vale's
papers); the paper SIXTEEN with NO amortization path (the service the
weight, never its fall — the debt outlives the man unless the strong
honest season outruns it; the fund crossing the row's size at the
fifth reckoning; the paper's fall a discrete event beyond the flows —
debt-1's own residue law). The tale carries the THIRD reckoning line
(the vale's year in three lines — the coupled liabilities at one
turn); zero core, the golden corpus byte-untouched (the zero-price
law), the source template reused.
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §2/§6) ·
1988 passed + 1 skipped, ruff clean (Python 3.12.14, the env pin;
verified at BASE_COMMIT fd9c475 BEFORE working — 1979+1 green, ruff
clean, docguard clean — and re-verified after with the full diff in
place) ·
Date: 2026-09-22 ·
Scope: content/province_pack/rules.json + entities.json +
tests/test_campaccount.py + tests/test_debt1.py (the census/year-run/
climb pins widened to the flow-id filter — the third flow's corpus
price) + docs/worldbuild/ANCHOR_REGION.md + docs/worldbuild/WORLD_
TESTS.md + docs/worldbuild/WORLD_WORKPLAN.md + STATUS.md + worklog.md
+ docs/TASKS.md — 10 paths (the embodiment form — iter-185's own
eleven-path shape less the tally's committed item, the account landing
inside the existing entities; over the 3–5 soft limit, noted per
AGENTS §2.3). Track A and track B untouched this session — the world
track a separate track (D-186, never a second queue). The prior
iterations' record: iter-185 (tallyread), iter-184 (charcoal1), bg-9
(apiprose), iter-183 (residues34), iter-182 (intake-35), iter-181
(intake-34), iter-180 (round 6), iter-179 (round 5), iter-177/178
(engine-1 (b) + presentation-1). The detail lives in the worklog + git.

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

**iter-186 DONE: the camp's account — the charcoal debt's arithmetic
(the master's thin stock + the `the_bloom_nets` net flow + the fold's
service carried in the notes, ONE SALE TWO CLAIMS — ANCHOR_REGION
§6.4, WORLD_TESTS §9's record, `tests/test_campaccount.py`).**

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
   reader — the reader's materials prepared over the committed
   surfaces this session, the owner's reading the missing half) and
   the embodiment options (the owner's called row remaining: the
   camp's freight volume — the withhold's volume surface, the debt-1
   residue class; the older units' — the step's notch record/hatch,
   the kin's own — each a future row's own call), the debt-1 residues
   (each a future row's own call — the player-scaled door the class's
   standing member), the SoW horizon (bg-6, owner-deferred —
   long-parked per the owner's 2026-09-21 call). Track B's gap rows
   all closed (round 4 + bg-9). New rows enter on the owner's call
   only.
3. The intake-34/35 residues (each behind its own trigger, never a
   default): the ref-file deep record — a named row consuming a
   specific math-catalog mechanism family (the per-card pass done at
   intake-35, the families re-confirmed at HEAD; Experiment 0's
   verdict + R1's landing close the other two residues — phases.md
   §6).
