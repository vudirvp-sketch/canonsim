Iteration: iter-225 (`iter-225-redot-engine-index` — the owner's
2026-09-25 «отразить в репозитории» call over the external Redot/
Godot agent reference index): the index ADMITTED as
`docs/REDOT_ENGINE_INDEX.md` (the version firewall + the routing
map — admission deltas only: §2.2/§2.3 reconciled to the landed
wb-4..wb-8 surface, §10's skills pinned agent-side per AGENTS
§2.8, the external changelog cut) + the routing surfaces wired
(AGENT_NAVIGATION §1/§2/§3 + the STATUS FAQ one-liner + TASKS'
wb-9+ pointer + CONTRACTS §5's composition block + README's agent
list) + docguard's allowlist entry (the 600-cap's §6.1 rationale)
+ D-207 into the standing-rows family row (the compound row's own
append form — the 30-row cap held).
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
(the wb family its live head, wb-8 DONE) + the world track + the SoW
horizon, ROADMAP §2/§6) ·
2223 passed + 6 skipped, ruff clean, docguard clean (Python 3.12.14,
the env pin; the 5 REDOT_EXE-gated visual packets + duckdb skipping
clean per D6/D-093 — the sandbox binary absent) ·
Date: 2026-09-25 ·
Scope: docs/REDOT_ENGINE_INDEX.md (new — the 1.4k-line engine
reference index, the docguard allowlist entry carrying the §6.1
rationale) + scripts/docguard.py (the allowlist line) + the routing
pointers (AGENT_NAVIGATION/TASKS/CONTRACTS/DECISIONS/README) + the
state docs (STATUS/worklog) — 9 paths (doc-only, the owner's
explicit call; zero code change beyond the guard's own allowlist,
the LOG untouched).
Track A: doc-only (the wb family's engine-facts layer). The prior
iterations' record: iter-224 (the wb-8 handback + D-206's delivery
protocol), 223 (wb-8), 222 (wb-7), 221 (wb-6), 220 (wb-5), 219
(wb-4), 218 (wb-3), 217 (wb-2), 216/215 (wb-1). The detail lives in
the worklog + git.


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

- KI#91 · wb-8's five shell.gd notes as adjacent literals refused the Redot parse · CLOSED iter-224 (one literal per line + the contract-test ban)

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
- **GDScript has NO implicit string-literal concatenation — two adjacent literals across lines are a Python-ism that refuses the whole file at parse (KI#91, iter-224's five sites); one literal per line; and any Redot/Godot engine question routes FIRST through `docs/REDOT_ENGINE_INDEX.md` (Redot 26.2 LTS pinned, Godot docs secondary cross-reference only; Redot 26.2 has NO `HTTPServer` — the app gateway stays Python-side; route to the smallest section, never read whole)** — test_shell_contract.py's adjacent-literal ban + the index §0/§21, D-207

## Next step

**iter-225 DONE: the Redot/Godot engine reference index admitted into
the repo (`docs/REDOT_ENGINE_INDEX.md` — the version firewall + the
routing map, D-207) + the routing surfaces wired (NAV §1/§2/§3, the
FAQ one-liner, the wb-9+ pointers in TASKS/CONTRACTS §5, README's
agent list) + docguard's allowlist entry.**

1. wb-9+ per the family rows (app §32's ladder: live events +
   reconnect/resync + the idempotency/revision/lease tests at live
   scale — session.events' frontend consumer + the RESYNC arm;
   persistence CAS + recovery roles; the frontend §46 rows — the
   Inference surface, history/diagnostics; the §11.1 replacement
   path (prepare-new → swap → retire-old over a live server); the
   live-build /models/load re-verification against the owner's
   station; the CanonSim seam) — the owner's call opens each row.
2. The remaining station rows (the owner's next engine run,
   TEST_PLAN §8.5's standing gaps + the wb-6 arm: the live-build
   /models/load + /models/unload re-verification against the
   b11064 station's ROUTER reality): the 27B GBNF parse arm + the
   one-model-constrained A/B (CONTRACTS §4.3 arm a) + the brief/
   parse component split; the narrator-convention call for live
   narrate play is two-sided now — more live beats at Q9B (size
   the tail) or the 27B as the one-model candidate (the §1 sweet
   spot, both doors) — the owner's choice (round 5's 12B + round
   6's 9B data: §13.1; bg-9's mapping-drift datum rides the same
   decision).
2. The standing frames: the embodiment options (the older units'
   rows — the step's notch record/hatch, the kin's own — each a
   future row's own call), the debt-1 residues (the crossing's
   own standing state the charcoalpaper precedent's sibling — the
   punt's purchase and the flood paper's fall still authored, each
   a future row's own call), the re-weigh's SALE (the heap's bloom
   drain — the withhold's own future row), the shave's temporal
   placement (the arc's assembly's remaining half — a future row's
   own call), the SoW horizon (bg-6, owner-deferred — long-parked
   per the owner's 2026-09-21 call). New rows enter on the
   owner's call only.
3. The intake-34/35/36/38 residues (each behind its own trigger,
   never a default): the ref-file deep record — a named row
   consuming a specific math-catalog or guide29 mechanism family
   (the per-card pass done at intake-35, the families re-confirmed
   at HEAD; Experiment 0's verdict + R1's landing close the other
   two residues — phases.md §6); the road-traffic depth-7 rider's
   evaluation grammar now carries intake-36's P01+P03 consult
   (capacity ≠ existence, the edge-perturbation discriminant, the
   fracture regime-change test — phases.md §6's intake-36 block);
   the intake-38 candidates (held-out transfer behind engine-1's
   corpus arms; the contract fields stopping-rule/spillover/
   nuisance behind the first claim packet that needs them —
   phases.md §6's intake-38 block, each behind its named first
   consumer, never a default).
