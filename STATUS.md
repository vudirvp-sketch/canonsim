# STATUS — canonsim

Iteration: 1 (`iter-1-core-plumbing` — the first functional-code
iteration; the 26-iteration docs streak ends here)
· Phase: 0 — simulator without LLM · Date: 2026-08-28

iter-1 lands the core plumbing per `docs/blueprint/phase0.md` §1:
`core/{schema,rng,ids,clock,queue,log,fold,pack,loop}.py` — the RngBank
with `assure`/`audit`/`peek` guards and the substantive-draw fingerprint;
the band-ordered heapq queue `(tick, sub_order, actor_id, seq)`; the
append-only JSONL writer (cause-chain integrity, gap-free writer-assigned
ids, write-time schema validation — the only canon-write path); the
incremental projection + fold (STATE-1, KI#5 closed by construction);
the pack loader with the phase-0 minimum lint; and the playscript runner
(movement + wait — the two check-less actions; the ten check-bearing
ones land iter-2 with the ActionResolver registry). Tests: architecture
fitness (import boundary · RNG monopoly · network ban · print ban), T0
(the EVENT_SCHEMA examples are extracted from the doc at test time — no
fixture copy to drift), minimal T1 (byte-identical runs + the committed
golden `tests/fixtures/plumbing_smoke_seed42.jsonl`), core units, loop
e2e — 78 green, ruff clean. Owner decisions recorded: D-032 (KI#10 →
stdlib mini-validator, closed), D-033 (P2c → iter-3), D-034 (DECISIONS
cap: collapse at phase gates; the file sits at 34 entries until then).

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index; the log writer is the
  only canon-write path (D-031).
- INV-2 Determinism: single point of randomness control — one master seed;
  named streams derived via the RngBank (`stable_hash` = sha256-based);
  no wall-clock; `sorted()` iteration; fixed `PYTHONHASHSEED`; queue key
  `(tick, sub_order, actor_id)`; cosmetic draws never desync canon replay
  (D-028 — the law text itself now carries this; AGENTS.md is the single
  reading owner).
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#3 · `expectation_violation` primitive missing — NPC reacts only to presence in `knowledge`, not to absence (purse gone, guard missing). Fix: P2d in `CORE_DESIGN_RESEARCH.md` §6, slated for iter-3; resolution recorded as ledger row EPIST-1 (`docs/BLUEPRINT.md` §1).
- KI#4 · balance harness (1000-sim distribution plots of `suspicion` / `fire_spread`) missing — MVP_SCOPE §15 promises an iter-6 baseline but no tool exists. Added as `balance-1` in `docs/TASKS.md` infra backlog; folded into the iter-6 verification stack (`docs/blueprint/phase0.md` §6).
- KI#5 · runtime state vs test fold not explicitly separated — CLOSED iter-1: the Simulator keeps the incremental projection (`apply_event` per emission), `fold` exists only on the T2 test path — D-023/STATE-1 implemented and test-enforced (`tests/test_loop.py::test_t2_fold_equals_runtime_projection`).
- KI#10 · stdlib JSON-Schema validation path undefined — CLOSED iter-1: owner approved the stdlib mini-validator; landed as `core/schema.py` (D-032) — write-time validation in the log writer, T0 on doc examples + committed logs.
- KI#11 · doc drift batch, 11 findings — CLOSED iter-0aa: tick arithmetic + fabricated "MVP_SCOPE §4.1" citation (phase0 §1, df_worldgen.md); ROADMAP §4 "week 1"; MVP_SCOPE §13 "day 3" + §5 system-3 npc↔npc gap; TASKS "post-sprint" + missing iter-0f Done line; P3c mislabels (phase0 §2, EVENT_SCHEMA §11); AGENT_NAVIGATION tests rows; README "empty". Details: worklog iter-0aa.

## FAQ / Pitfalls

- **The golden T1 fixture is env-pinned.** The log header records the
  Python version (`AGENTS.md` §10 — same-environment determinism only), so
  `tests/fixtures/plumbing_smoke_seed42.jsonl` byte-compares only on the
  Python it was generated on. On an interpreter bump the byte-compare
  fails **by design**: regenerate (Simulator, seed 42, commit `"0000000"`,
  playscript `tests/playscripts/plumbing_smoke.json`) and commit the new
  fixture together with the env change. The full in-pytest regeneration
  guard lands with T1 at iter-6 (`docs/blueprint/phase0.md` §6).
- **A ref citing a spec section it never contained is drift, not history.**
  The pre-D-028 FAQ rule protects *real* historical wording — verify with
  `git log -S "<phrase>" -- <file>` before calling something history.
  iter-0aa example: `df_worldgen.md` cited "MVP_SCOPE §4.1: 1 tick = 12
  in-world minutes" — §4.1 is the locations table and never owned time
  numbers; the fabricated figure leaked into `phase0.md` §1 and contradicted
  MVP_SCOPE §8's own arithmetic (1440 ticks/day). Diagnostic: any
  cross-doc numeric claim is re-derived from its claimed owner before it
  enters a prescriptive doc.
- **Where the code-quality bar lives (D-031).** Law: `AGENTS.md` §4
  (invariants + the canon-write privilege line) + §9 (DoD: conventions per
  `MVP_SCOPE.md` §18 — type hints, no `print()` outside `cli/` — and the
  L13/L14 elegance laws). Constitution: `docs/BLUEPRINT.md` §2 — L13
  (abstraction cost gate, Rule-of-Three tiers, 4-branch registry threshold)
  and L14 (elegance standard + review checklist). Build clauses:
  `docs/blueprint/phase0.md` §1 (type discipline, fail-fast, the
  architecture fitness test), §2 (ActionResolver registry), §6 (tests
  document the invariants; negative tests prove them). Executable:
  `tests/test_architecture.py` (iter-1) + the stoplist test (iter-2).
  Rationale: D-031; sources: `docs/REFERENCES.md` §15. The two owner texts
  are absorbed, not filed — no `docs/ARCHITECTURE.md` /
  `TYPE_DISCIPLINE.md` / `TESTING_PHILOSOPHY.md` will be created (the
  D-018 pattern); a new canonical layer is the named anti-pattern.
- **Zip upload loses dotfiles and empty dirs.** "Add files via upload" on GitHub
  dropped `.gitignore` (and every dir without tracked files). After any future
  upload: verify `.gitignore` exists and `git status --short` shows no runtime
  artifacts (KI#1).
- **Workspace files ≠ tracked files.** `git status --short` shows changes
  *vs HEAD*, not what is *in HEAD* — a file present in your working directory
  may not be committed at all. After any structural change, run
  `git ls-files <path>` (or `git ls-files | head -50`) to confirm what is
  actually tracked. This is the diagnostic for KI#1-class losses and for
  "the file exists but tests can't find it" surprises.
- **Content/tone questions → D-030 + the `PACK_SPEC.md` sketch row.** The
  start pack for phase 0 is `tavern_pack` v0.1 as scoped (`MVP_SCOPE.md`
  §4–§7 own the counts); tone is data asymmetry inside the existing systems,
  not new systems. Growing the pack or writing a pack spec before its
  trigger = scope creep (AGENTS §2.4; SPECS_BACKLOG header rule). Grim/romance
  material accumulates in the sketch row + `pack-1` (TASKS infra backlog)
  until the PACK_SPEC trigger fires (phase 6 / a 2nd setting).
- **Doc-loop alarm vs owner-requested research.** Twenty-six docs iterations
  in a row would normally force a stop (AGENTS §2.5). Owner-requested passes
  are the explicit exception (D-022) — the documented condition is a fresh
  owner request (iter-0s/0t additionally had fresh external sources;
  iter-0u/0v — distillation and audit; iter-0w — concept realignment; iter-0x
  — reference-influence audit; iter-0y — content principles; iter-0z — the
  quality round with two provided analyses; iter-0aa — the pre-code doc
  audit — rest on the request alone).
  iter-0aa is the twenty-sixth docs iteration in a row (0, 0b, 0c, 0e, 0f,
  0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n, 0o, 0p, 0q, 0r, 0s, 0t, 0u, 0v, 0w, 0x,
  0y, 0z, 0aa; iter-0d was infra). All ref-N backlog items are complete — ref-1
  through ref-13 plus the iter-0h cousins; ref-14/ref-15 (Sims, Prom Week)
  are owner-request-only candidates; no doc pass at all without a fresh
  owner request. **iter-1 code is next, unconditionally.**
- **Four places, four jobs (D-027).** `docs/REFERENCES.md` catalogs sources
  (license, URL, phase gating); `docs/CORE_DESIGN_RESEARCH.md` §2 carries
  the one-line synthesis per source; `docs/ref/<source>.md` carries the
  concrete mechanics; `docs/BLUEPRINT.md` + `docs/blueprint/` carry the
  cross-reference resolutions and donor combinations per build component.
  Drift rule: link, never restate; cite ledger row IDs (e.g. "per RNG-1")
  instead of re-deriving a resolution. The old STATUS "Next step" prose
  mapping of refs → iterations was exactly this drift and has been folded
  into the blueprint build index (`docs/BLUEPRINT.md` §3), its single
  owner.
- **Pre-D-028 RNG wording in `docs/ref/*` and `REFERENCES_DEEP.md` is
  historical evidence, not prescription.** Several ref files quote
  "INV-2: one `random.Random(seed)` instance" as it read at deep-dive
  time. Do not "fix" those — they document what the donor comparison was
  made against. The single reading owner of INV-2 is `AGENTS.md` §4
  (D-028); anything prescriptive points there (same pattern as the KI#6
  license-drift rule: catalog is the owner, index rows can lag).
- **Substance over line count (D-025) + per-ref split (D-026).** The cap is
  600 with the §6.1 substance filter as the real law — filler is cut
  always; named systems, real field lists, type enumerations, per-source
  verdicts are never cut to fit. The iter-0l..0r per-ref files run
  101–605 lines each, each under cap by construction or §6.1-justified;
  the iter-0u blueprint files are 149/340/224 lines — under cap by
  construction.
- **"Ref graveyard" check (iter-0x audit method).** To verify the reference
  corpus still influences the plans (not just exists as a folder), grep a
  sample of ledger terms across the planning docs — ShufflePool,
  ASSERT_stable, Influence Boundary, promoteTile, bm25, copy-from — over
  `docs/BLUEPRINT.md` + `docs/blueprint/` + `docs/TASKS.md` +
  `docs/SPECS_BACKLOG.md`: every term must land in at least one planning
  doc; the concrete mechanics stay owned by `docs/ref/` by design (link,
  never restate — D-027). Verified iter-0x; re-run at the phase-0 gate
  review.
- **License drift between catalog and index (KI#6, closed iter-0n; pitfall
  persists).** The `REFERENCES_DEEP.md` §2 index table is **not** the source
  of truth for licenses — `REFERENCES.md` (the catalog) is. Diagnostic:
  before flipping any ref-N row todo→done, grep the source row in
  `REFERENCES.md` and verify the license column matches the index entry.
  The standing pre-flip check is exercised across iter-0o/0p/0q/0r/0s/0t;
  iter-0u touched no ref rows, so no check was needed this iteration.

## Next step

**iter-2 · actions** (`docs/TASKS.md`): the 12 actions with
checks/outcomes/durations (`MVP_SCOPE.md` §7), pack-driven preconditions,
INTENT_SCHEMA with `based_on_event_seq` OCC, the scheduler DAG with
`reads`/`writes` annotations, the ActionResolver registry (the two
iter-1 resolvers grow into it), and the INV-3 grep stoplist test. Read
before building: `docs/blueprint/phase0.md` §2 + `MVP_SCOPE.md` §7;
ledger rows TIME-1, EPIST-1 (price precursor), PACK-1, STATE-1
(`docs/BLUEPRINT.md` §3 build index).
