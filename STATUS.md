Iteration: iter-220 (`iter-220-wb5-operations` — the
minimal application operations, the owner's «продолжай работу»
continuation call over the v5.2 brief, the family's fifth row):
app §32 step 5 CLOSED — the operations substrate + the
run/model-discovery families over the wb-4 registered surface:
`workbench/application/operations/` — `lifecycles.py` (§11's four
closed state machines: the legal-transition tables, the terminal
semantics = the empty successor set, the invalid-transition
loudness; §25's FAILED_SHUTDOWN + the process-loss UNKNOWN branches
resolved), `execution.py` (§12's absolute OperationDeadline frozen
at admission — the remaining budget the only lower-layer view, the
cooperative CancellationToken + WorkContext.check(); the in-memory
ExecutionRegistry: admit freezes the §10 inputs BEFORE any side
effect, launch walks STARTING + spawns the daemon worker, the
truthful terminal close — the late result FAILED_TO_CANCEL with
the result recorded, the checkpoint abort CANCELED, the deadline/
anomalous raises FAILED, mark_unknown the §25 surface), `models.py`
(§20's discovery half over the §16 MODELS_ASSETS role: the scan +
the cheap-fingerprint screen, inspect's fresh §9 strong identity,
digest_work the one real work kind), `composition.py` (§6.1's
single wiring owner: run.start/get/cancel + model.list/inspect
registered; chat.send honestly NOT registered — the backend row's
consumer, the admission law) + gateway.py's two targeted edits
(OperationRejected the public rejection carrier, OperationEffects
the session-scoped OPERATION_EFFECT surface).
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
(the wb family its live head, wb-5 DONE) + the world track + the SoW
horizon, ROADMAP §2/§6) ·
2159 passed + 6 skipped, ruff clean, docguard clean (Python 3.12.14,
the env pin; the 5 REDOT_EXE-gated visual packets + duckdb skipping
clean per D6/D-093 — the sandbox binary absent; with REDOT_EXE set
the suite reads 2164+1) ·
Date: 2026-09-24 ·
Scope: workbench/application/operations/ (5 new: __init__ +
lifecycles + execution + models + composition) +
workbench/api/gateway.py (the two targeted composition-point edits) +
tests/test_operations.py (46 tests) + pyproject.toml
(workbench.application.operations) + the state docs (CONTRACTS/
TASKS/DECISIONS/NAV/README/worklog + this file) — 15 paths (the 3–5
soft limit honestly over: the row is a full contract slice — the
substrate + two families + the composition root + the claim packet,
AGENTS §2.3, the scope noted in the worklog; zero core change, zero
pack change, the LOG untouched, INV-4's two-surface form unchanged —
no new network module, cli/engine.py and workbench/api/transport.py
stay the only sanctioned surfaces).
Track A: wb-5 DONE. The prior iterations' record: iter-219 (wb-4
gateway), 218 (wb-3 skeleton), 217 (wb-2 redot shell), 216 (wb-1
redot), 215 (wb-1 python). The detail lives in the worklog + git.


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
- **The STATUS tests-count line feeds the digest's regex: `N passed + M skipped, ruff clean` — one line, comma-free from the counts to `ruff clean` (parenthetical caveats go AFTER `docguard clean`), else the digest reads `(unparsed)`** — `scripts/digest.py` `_TESTS_RE`.

## Next step

**iter-220 DONE: wb-5's minimal application operations — app §32
step 5 CLOSED (the operations substrate + the run/model-discovery
families over the wb-4 registered surface, D-202): the §11
lifecycle vocabularies closed with invalid-transition loudness, the
§12 absolute-deadline/cancellation machinery executable, the run
registry landing the §10 artifact-before-side-effects freeze with
§12.3's truthful cancellation, the model family's discovery half
with the §9 identity laws, the §6.1 composition root the single
wiring owner — one real work kind (model.digest) making the
execution substrate machinery in use; chat.send honestly deferred
to the backend row (the admission law); the 46-test claim packet
landed (the spawn-failure SENT_OUTCOME_UNKNOWN integration, the
independent-sha256 oracle, the direct-vs-HTTP parity, the
cross-seed pair); the epistemic class FACT, the disposition
CONFIRMED. wb-5 row DONE.**

1. wb-6+ per the family rows (app §32's ladder: live events +
   reconnect/resync + the idempotency/revision/lease tests at live
   scale; persistence CAS + recovery roles; the backend row —
   capability-aware inference/configuration + model identity/loading
   (chat.send's consumer); frontend §46's Phase-A remainder) — the
   owner's call opens each row.
2. The remaining station rows (the owner's next engine run, TEST_PLAN
   §8.5's standing gaps): the 27B GBNF parse arm + the
   one-model-constrained A/B (CONTRACTS §4.3 arm a) + the brief/parse
   component split; the narrator-convention call for live narrate
   play is two-sided now — more live beats at Q9B (size the tail) or
   the 27B as the one-model candidate (the §1 sweet spot, both
   doors) — the owner's choice (round 5's 12B + round 6's 9B data:
   §13.1; bg-9's mapping-drift datum rides the same decision).
2. The standing frames: the embodiment options (the older units' rows
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
3. The intake-34/35/36/38 residues (each behind its own trigger, never a
   default): the ref-file deep record — a named row consuming a
   specific math-catalog or guide29 mechanism family (the per-card
   pass done at intake-35, the families re-confirmed at HEAD;
   Experiment 0's verdict + R1's landing close the other two
   residues — phases.md §6); the road-traffic depth-7 rider's
   evaluation grammar now carries intake-36's P01+P03 consult
   (capacity ≠ existence, the edge-perturbation discriminant, the
   fracture regime-change test — phases.md §6's intake-36 block);
   the intake-38 candidates (held-out transfer behind engine-1's
   corpus arms; the contract fields stopping-rule/spillover/nuisance
   behind the first claim packet that needs them — phases.md §6's
   intake-38 block, each behind its named first consumer, never a
   default).
