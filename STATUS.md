Iteration: iter-198 (`iter-198-abfalsifier` — the mech-2 A/B falsifier's
measurement, the owner's «верх очереди не изменился: (1) A/B
фальсификатор mech-2 — измерение на операторской стороне (Rule 9),
инструмент готов» call): the measurement RAN operator-side — 6
realistic pack-edit tasks × bare/impact-gated × n=3 at glm-4-plus
(whole-file protocol, max_tokens 32k, thinking disabled; runner +
transcripts outside the repo, Rule 9; ~1.09M prompt + 0.60M completion
tokens, 0 transport failures). The verdict: the injected impact gate
moved NONE of the three named metrics (success 8/18 both arms, lint
refusals 0, patches tiny); the cognitive premise REFUTED at the
current scale (conditional on a valid round-trip: 8/8 bare vs 8/9
gated — find/scope is not the binding constraint); the measured
bottleneck is the whole-file emission pattern itself: the bracket-
drift wall in `director.hooks` (10/15 bare, 9/15 gated rules.json
re-emissions invalid, two recurring drift sites) + 73% silent notes
paraphrase in the valid emissions; the rename task 0/6 (the one valid
gated cell dropped the cross-file seeding tag the gate itself had
named; the lint blind to it — the pre-run probe agrees). The
structured-patch PROPOSAL re-scoped to emission reliability (the
API-agent class), fate the owner's call. Doc-only, zero code touch;
the numbers: TECH_NOTES §17.
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §2/§6) ·
2026 passed + 1 skipped, ruff clean, docguard clean (Python 3.12.14,
the env pin; verified at BASE_COMMIT 808ef89 — 2026+1 green, ruff
clean, docguard clean, before the change) ·
Date: 2026-09-23 ·
Scope: docs/TECH_NOTES.md + docs/blueprint/phases.md + docs/TASKS.md +
STATUS.md + worklog.md — 5 paths (the measurement's residue routing:
the numbers' owner + the intake-37 premise line + the mech-2 row +
the state docs).
Track A and track B untouched this session — the world track a
separate track (D-186, never a second queue); the covering series
(STATUS Next step 1) left to the next iteration by the owner's
«если в одну итерацию не уместишься» instruction — the A/B consumed
the iteration. The prior iterations' record: iter-197 (revalid2),
iter-196 (mech2), iter-195 (bottleneck). The detail lives in the
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

**iter-198 DONE: the mech-2 A/B falsifier's measurement (the owner's
call, STATUS item 1) — the gate moved none of the three metrics
(success 8/18 both arms, lint refusals 0, patches tiny); the cognitive
premise refuted at the current scale; the whole-file emission wall +
73% silent notes paraphrase measured instead; the structured-patch
PROPOSAL re-scoped to emission reliability, fate the owner's call
(TECH_NOTES §17). The covering series (the queue's item 2) NOT
STARTED — the A/B consumed the iteration, per the owner's break-clean
instruction.**

1. THE COVERING RESIDUE'S FUTURE ROW (the arc's assembly — the
   owner's call, WORLD_TESTS §9's W5 entry's named remainder): the
   +3 reckonings' covering, the shave → starvation arc, and now the
   withhold's own joke — the contradiction still not ONE surface;
   never "improve the prose".
2. The structured-patch PROPOSAL's call (the A/B's fresh material,
   the owner's decision): the emission-reliability motivation measured
   (the wall + the silent notes paraphrase, the API-agent class) vs
   the weakened cognitive-crutch motivation — open, close, or park
   with the re-scoped rationale; the rename-safety lint gap (the
   dangling hook tag passes admission) a separable small candidate if
   the owner wants the cheapest slice.
3. The W5 trio's remaining stations (each on the owner's call,
   WORLD_WORKPLAN §7's decision points): the heartbreak probe (its
   design material carries intake-36's C03+F02 consult) and the human
   live-band re-run (the LLM reader the instrument so far, glm n=2 —
   the owner's option (б)).
4. The remaining station rows (the owner's next engine run, TEST_PLAN
   §8.5's standing gaps): the 27B GBNF parse arm + the
   one-model-constrained A/B (CONTRACTS §4.3 arm a) + the brief/parse
   component split; the narrator-convention call for live narrate
   play is two-sided now — more live beats at Q9B (size the tail) or
   the 27B as the one-model candidate (the §1 sweet spot, both
   doors) — the owner's choice (round 5's 12B + round 6's 9B data:
   §13.1; bg-9's mapping-drift datum rides the same decision).
5. The standing frames: the embodiment options (the older units' rows
   — the step's notch record/hatch, the kin's own — each a future
   row's own call), the debt-1 residues (the crossing's own standing
   state the charcoalpaper precedent's sibling — the punt's purchase
   and the flood paper's fall still authored, each a future row's own
   call), the re-weigh's SALE (the heap's bloom drain — the
   withhold's own future row), the SoW horizon (bg-6, owner-deferred —
   long-parked per the owner's 2026-09-21 call). New rows enter on the
   owner's call only.
6. The intake-34/35/36 residues (each behind its own trigger, never a
   default): the ref-file deep record — a named row consuming a
   specific math-catalog or guide29 mechanism family (the per-card
   pass done at intake-35, the families re-confirmed at HEAD;
   Experiment 0's verdict + R1's landing close the other two
   residues — phases.md §6); the road-traffic depth-7 rider's
   evaluation grammar now carries intake-36's P01+P03 consult
   (capacity ≠ existence, the edge-perturbation discriminant, the
   fracture regime-change test — phases.md §6's intake-36 block).
