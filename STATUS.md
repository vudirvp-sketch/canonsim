Iteration: iter-207 (`iter-207-humanband` — the owner's option (б)
call firing STATUS Next step item 1 — the human live-band re-run after
the reader-side fixes, the rs family's seven measured fixes + the
eighth's met pair the band it waits on; the question the human
reader's convergence): the human band's INSTRUMENT re-established and
the READING KIT delivered to the owner — the human reading itself the
owner's side, never a sandbox claim. The two packages regenerated
deterministically at seed 42, the runner + the kit outside the repo
(Rule 9 — the iter-191/206 reconstruction precedent's own class, the
honest notes below): the RE-WEIGH package (the sparse twin macro 480 /
calendar 240/360/420, the full chain — the factor's runner's crofts
detour, the tally read at the crofts (the night arm, t=1112, partial
fidelity, the cluster still minted — the recorded fall geometry's own
consequence: no morning wait fits t=2824), the walks to Malby, the
FALL at t=2824 with the fund 18, the COLLECTION, two aftermath
crossings; the close paper 0 / coin 8, the heap 18, seven crossings +
seven banks, the tale 87 lines, every rs-2/3/4/5/6 surface carried;
the package = the tale + Garrick's opening/close records + the
crofts' close record + three briefs — the player's crisis at the fall
(the_paper_fell exact), Garrick's crisis (fall + collection, his
voice), the player's close) and the HEARTBREAK package (the committed
pack, the return's chain — 43 events, the tale 24 lines, the read's
fail-then-pass, the claim's road-hearing, the echo 40→80, the names,
rs-7/8's lines; the package = the tale + Tork's opening/close records
+ Ketta's close record + three briefs — the runner's road window,
Ketta's arrival + close, her voice); both byte-identical on
regeneration; the author audit pre-set BEFORE the reading (the repo's
own recorded pass bars — the same bars the LLM band's glm n=2 readings
were measured against, the convergence question stated as the band's
own). The kit (the packages + the blind reader questions + the audit)
handed to the owner as the sandbox deliverable; the LLM band's
measured results the comparison baseline — the convergence the
owner's reading away.
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §2/§6) ·
2041 passed + 1 skipped, ruff clean, docguard clean (Python 3.12.14,
the env pin; verified at BASE_COMMIT ff65edf — 2041 passed + 1
skipped, ruff clean, docguard clean, before the change) ·
Date: 2026-09-23 ·
Scope: docs/worldbuild/WORLD_TESTS.md + docs/worldbuild/WORLD_WORKPLAN.md
+ docs/TASKS.md + STATUS.md + worklog.md — 5 paths doc-only (the
probe-instrument state-docs class, iter-204's own form; the runner +
the kit outside the repo, Rule 9; zero code, zero pack change, the LOG
untouched).
Track A: the W5 human live band's instrument re-established + the
reading kit delivered (option (б) — the convergence the owner's
reading away). The prior iterations' record: iter-206
(heartbreak-subject — the mandatory pair MET at the LLM band), 205
(heartbreak-fix), 204 (heartbreak). The detail lives in the worklog +
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

**iter-207 DONE: the human live band's instrument re-established and
the READING KIT delivered to the owner (option (б) — the rs family's
eight fixed surfaces + the eighth's met pair the band it waits on)
— the human reading itself the owner's side, the convergence the
band's standing question.**

1. The owner's HUMAN READING over the delivered kit (the two packages
   + the three blind questions; the author audit read after) — the
   convergence assessment against the LLM band's measured baseline
   (glm n=2, WORLD_TESTS §9's W5 entry) the reading's own next beat;
   where the reading diverges, the divergence's class the datum (the
   boundary law, never "improve the prose").
2. The remaining station rows (the owner's next engine run, TEST_PLAN
   §8.5's standing gaps): the 27B GBNF parse arm + the
   one-model-constrained A/B (CONTRACTS §4.3 arm a) + the brief/parse
   component split; the narrator-convention call for live narrate
   play is two-sided now — more live beats at Q9B (size the tail) or
   the 27B as the one-model candidate (the §1 sweet spot, both
   doors) — the owner's choice (round 5's 12B + round 6's 9B data:
   §13.1; bg-9's mapping-drift datum rides the same decision).
3. The standing frames: the embodiment options (the older units' rows
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
4. The intake-34/35/36 residues (each behind its own trigger, never a
   default): the ref-file deep record — a named row consuming a
   specific math-catalog or guide29 mechanism family (the per-card
   pass done at intake-35, the families re-confirmed at HEAD;
   Experiment 0's verdict + R1's landing close the other two
   residues — phases.md §6); the road-traffic depth-7 rider's
   evaluation grammar now carries intake-36's P01+P03 consult
   (capacity ≠ existence, the edge-perturbation discriminant, the
   fracture regime-change test — phases.md §6's intake-36 block).
