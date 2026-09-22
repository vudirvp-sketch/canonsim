Iteration: iter-195 (`iter-195-bottleneck` — intake-37, the owner's
mandatory-research-artifact call over the uploaded agent-bottleneck
research note): the research ROUTED whole — every measurement
re-verified at HEAD, the verdict PARTIALLY CONFIRMED: the formats +
the tooling-first direction CONFIRMED (zero format change — JSONL +
the four-file pack stand; matrix/doctor/checkpoints/arch-tests/
docguard all present and green), the full-file-rewrite claim REFUTED
by the measured history (97% of 120 pack-JSON touches surgical, 82%
≤10%, the three rewrites early-era; AGENTS §2 the standing defence),
the mutation-adequacy gap upgraded from proposal to MEASURED FACT
(the session's probe: the admission lint refuses the structural
breaks 4/6 but ACCEPTS value mutations 2/6 — a director
release_threshold 10→4, an urgency probability 40→55 — and the
tavern golden is blind to both; TEST_PLAN §9's new path-bound law +
the mutation-prism row the grammar), the numeric corrections
recorded (≈614 KB reproduces under no measure; the density figures
extractor-dependent, the ordering claim holds); the
research/intervention documentation SCHEMA landed (residue →
phases.md §6, interventions → scratch/ gitignored, adoptions →
DECISIONS, tasks → TASKS — the intake-37 block the record); ONE row
convened on the owner's call (mech-2 — the agent impact surface,
R03's first named consumer, its falsifier the A/B measurement); the
structured-patch machinery + the edit-shape guard stay PROPOSAL
behind the same falsifier.
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §2/§6) ·
2018 passed + 1 skipped, ruff clean, docguard clean (Python 3.12.14,
the env pin; verified at BASE_COMMIT 462e84a both ends — 2018+1
green, ruff clean, docguard clean) ·
Date: 2026-09-22 ·
Scope: .gitignore + docs/blueprint/phases.md + docs/DECISIONS.md +
docs/TEST_PLAN.md + docs/TASKS.md + docs/AGENT_NAVIGATION.md +
STATUS.md + worklog.md — 8 paths (the intake-37 record + D-197 + the
§9 prism + the mech-2 row + the scratch/ law + the state docs; the
probe runners + the measurement scripts outside the repo, Rule 9 —
8 files over the 3–5 soft cap, the owner's schema+routing task the
scope justification, noted per AGENTS §2.3).
Track A and track B untouched this session — the world track a
separate track (D-186, never a second queue). The prior iterations'
record: iter-194 (humorgloss), iter-193 (intake36), iter-192
(humorprobe), iter-191 (accountgloss), iter-190 (bioprobe),
iter-189 (charcoalpaper), iter-188 (knowsgloss), iter-187
(freightvol), iter-186 (campaccount), iter-185 (tallyread). The
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

**iter-195 DONE: the agent-bottleneck research routed whole (intake-37,
D-197) — the verdict PARTIALLY CONFIRMED, the schema landed, mech-2
convened. iter-194 before it: the W5 humor fix landed (rs-3) and the
re-run's mandatory bar MET (the station PARTIALLY CONFIRMED, the
authored residues open). iter-191: the biography re-run PASSED CLEAN —
the embargo lifted (stands).**

1. The mech-2 decision (the owner's call — the row convened this
   iteration): the agent impact surface (`mechanics impact --path`,
   R03's family) — open the row for the tooling spike, or hold it
   behind its A/B falsifier first; the structured-patch machinery +
   the edit-shape guard stay PROPOSAL behind the same falsifier.
2. THE COVERING RESIDUE'S FUTURE ROW (the arc's assembly — the
   owner's call, WORLD_TESTS §9's W5 entry's named remainder): the
   +3 reckonings' covering, the shave → starvation arc, and now the
   withhold's own joke — the contradiction still not ONE surface;
   never "improve the prose".
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
