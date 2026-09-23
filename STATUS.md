Iteration: iter-205 (`iter-205-heartbreak-fix` — the owner's
minimal-fix call firing STATUS Next step item 1 — the heartbreak
station's rendering FIX over the iter-204 measured failure): rs-7
landed (the rs family's seventh member) — TWO template lines
re-authored in the province pack, zero code, zero corpus price, the
LOG untouched: the mourning line (`the_names_kept`) now carries the
loss's future-option dimension ("their line, their duties and their
holdings never handed on" — the owner's called vocabulary) and the
echo line (`the_edge_answers`) the claim's forward framing ("the
crossing's table open to the claimant's line from this day" — the
opened possibility, never only the standing); the pins updated as
the deliberate act (tests/test_winterkin.py). The SAME blind probe
re-run (the iter-204 protocol re-established — the package the same
bounded form, the tale 24 lines, the chain byte-identical twice at
seed 42, the package byte-identical twice; the author audit pre-set
BEFORE the reading with the same F02 pass bar; the blind reader glm
n=2 independent, the runner + transcripts outside the repo, Rule 9):
the mandatory pair NOT MET at the strict n=2 bar, with MEASURED
MOVEMENT on both halves — the opened-option half extracted CLEANLY
by reading 2 (the table-open clause verbatim + the forward synthesis
"seizes the future of the weir stair"; reading 1 still the present
right-transfer — 1/2, the echo route CONFIRMED as the working
class), iter-204's ZERO-futures mode GONE n=2 (both readings now
carry the inheritance/obligation topology — reading 2's "a tale of
inheritance, but not of wealth or land" the closest lost-future
extraction) — but the drowned generation still not read as the
futures' OWN holders (the SUBJECT problem: the mourning line's
clause resolves to the inheritance's character, never to the dead as
the loss's subject); the supporting bars MET n=2 convergent (the
relation never a trade; the memory change; the world-specificity).
The disposition: NEVER "improve the prose" — the further fix's
route the owner's call (the natural class the measurement names: the
dead as the loss's grammatical subject); the anti-loop law held (the
first fix attempt only). The 40/80 asymmetry, the fail-then-pass and
the second-holder structure untouched per the owner's call (each its
own surface's question).
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §2/§6) ·
2041 passed + 1 skipped, ruff clean, docguard clean (Python 3.12.14,
the env pin; verified at BASE_COMMIT 57ebc3f — 2041 passed + 1
skipped, ruff clean, docguard clean, before the change) ·
Date: 2026-09-23 ·
Scope: content/province_pack/templates.json + tests/test_winterkin.py
+ docs/worldbuild/WORLD_TESTS.md + docs/worldbuild/WORLD_WORKPLAN.md
+ docs/TASKS.md + STATUS.md + worklog.md — 7 paths (the rs-landing
class: the pack line + the pin + the state docs; two over the soft
cap — the AGENTS §9 doc-sync law, the probe-run record the state
docs' own class; the runner + the transcripts outside the repo,
Rule 9).
Track A: the W5 heartbreak station's rendering fix measured (the
mandatory pair's halves moved — the opened option cleanly extracted
once, the zero-futures mode gone n=2 — the strict bar still not met:
the further route the owner's call). The prior iterations' record:
iter-204 (heartbreak — the first measurement), iter-203 (winterkin).
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

**iter-205 DONE: the heartbreak station's minimal RENDERING FIX landed
and measured (rs-7 — two template lines re-authored, zero code; the
re-run: the opened-option half cleanly extracted once, the
zero-futures mode gone n=2, the mandatory pair still NOT MET at the
strict n=2 bar — the dead still not read as the futures' own holders,
the SUBJECT problem; the further route the owner's call).**

1. The heartbreak FIX'S FURTHER ROUTE (the owner's call over the
   iter-205 measured movement): the dead as the loss's grammatical
   SUBJECT — the natural class the measurement names (the mourning
   line's clause re-subjected: the futures THEIRS, removed with them
   — or the flood's removal named with the dead as its holders; the
   measured failure mode: the clause resolves to the inheritance's
   character, what the claim brings or excludes, never to the dead
   as future-holders); the echo half's route (the "from this day"
   forward frame) CONFIRMED at 1/2 — no further work there unless
   the owner calls; the discovery-path residues alongside (the
   fail-then-pass + the 40/80 asymmetry + the second-holder
   structure — each its own surface's question); never "improve the
   prose"; the anti-loop law held (the first fix attempt only — a
   second attempt on the owner's call).
2. The human live-band re-run after the reader-side fixes (the LLM
   reader the instrument so far, glm n=2 — the owner's option (б);
   the rs family's six measured fixes + the seventh's measured
   movement the band it waits on; the heartbreak's own half still
   open — its further fix joins the band when called).
3. The remaining station rows (the owner's next engine run, TEST_PLAN
   §8.5's standing gaps): the 27B GBNF parse arm + the
   one-model-constrained A/B (CONTRACTS §4.3 arm a) + the brief/parse
   component split; the narrator-convention call for live narrate
   play is two-sided now — more live beats at Q9B (size the tail) or
   the 27B as the one-model candidate (the §1 sweet spot, both
   doors) — the owner's choice (round 5's 12B + round 6's 9B data:
   §13.1; bg-9's mapping-drift datum rides the same decision).
4. The standing frames: the embodiment options (the older units' rows
   — the step's notch record/hatch, the kin's own — each a future
   row's own call), the debt-1 residues (the crossing's own standing
   state the charcoalpaper precedent's sibling — the punt's purchase
   and the flood paper's fall still authored, each a future row's own
   call), the re-weigh's SALE (the heap's bloom drain —
   the withhold's own future row), the shave's temporal placement
   (the arc's assembly's remaining half — a future row's own call),
   the SoW horizon (bg-6, owner-deferred —
   long-parked per the owner's 2026-09-21 call). New rows enter on the
   owner's call only.
5. The intake-34/35/36 residues (each behind its own trigger, never a
   default): the ref-file deep record — a named row consuming a
   specific math-catalog or guide29 mechanism family (the per-card
   pass done at intake-35, the families re-confirmed at HEAD;
   Experiment 0's verdict + R1's landing close the other two
   residues — phases.md §6); the road-traffic depth-7 rider's
   evaluation grammar now carries intake-36's P01+P03 consult
   (capacity ≠ existence, the edge-perturbation discriminant, the
   fracture regime-change test — phases.md §6's intake-36 block).
