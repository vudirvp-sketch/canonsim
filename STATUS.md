# STATUS — canonsim

Iteration: 0aa (owner-requested: pre-code documentation audit — drift
sweep + core-readiness verdict)
· Phase: 0 — simulator without LLM · Date: 2026-08-27

iter-0aa sweeps the docs before iter-1 breaks ground: 11 drift findings
fixed as KI#11 (opened/closed here) — the fabricated "1 tick ≈ 12
in-world minutes" citation (`phase0.md` §1 + `df_worldgen.md`; truth:
MVP_SCOPE §8 owns 1440 ticks/day → 1 tick = 1 in-world minute),
calendar remnants (ROADMAP §4 "week 1" → `bg-1`; MVP_SCOPE §13
"day 3"; TASKS "post-sprint"), the missing iter-0f line in the TASKS
Done list, two P3c mislabels (phase0 §2, EVENT_SCHEMA §11), the
MVP_SCOPE §5 system-3 row missing the npc↔npc pair map (D-020), the
`tests/fixtures/` + `tests/playscripts/` map rows, README wording.
Readiness verdict: the rigging for iter-1 is complete — contracts
synced and test-enforced, pack drafted, module-level design in
phase0 §1, acceptance criteria in TASKS; one design point is genuinely
open (KI#10: the stdlib JSON-Schema validation engine). P2c (detail
callbacks) remains the only owner-pending design item before iter-3.

**Doc-loop accounting:** 26th consecutive docs iteration — owner-requested
exception (D-022 wording: a fresh owner request — this audit pass).
The alarm condition stands, now with teeth: **iter-1
(functional code) is unconditionally the next iteration** — no ref-N, no
spec writing, no doc polish without a fresh owner request.

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
- KI#5 · runtime state vs test fold not explicitly separated — risk of O(N²) at startup if `fold(log)` is misused as runtime path. D-023 records the rule: runtime = incremental projection; fold = T2 replay only; resolution recorded as ledger row STATE-1.
- KI#10 · stdlib JSON-Schema validation path undefined — T0 ("every log line validates against `schemas/event.schema.json`") and the pack loader ("JSON-Schema validation at load", phase0 §1) both require schema validation, but `jsonschema` is a runtime dependency (forbidden, D-012) and a dev-dep would breach the pytest+ruff cap (AGENTS §8). Proposed: a stdlib mini-validator for the used schema subset (type/required/enum/pattern/additionalProperties/$defs/minimum, ~100–150 lines) — schema-driven, no contract duplication; fallback: hand-rolled structural checks (test_smoke.py precedent, drift-prone). Owner decision pending; blocks only the T0 mechanism choice, not the rest of iter-1.
- KI#11 · doc drift batch, 11 findings — CLOSED iter-0aa: tick arithmetic + fabricated "MVP_SCOPE §4.1" citation (phase0 §1, df_worldgen.md); ROADMAP §4 "week 1"; MVP_SCOPE §13 "day 3" + §5 system-3 npc↔npc gap; TASKS "post-sprint" + missing iter-0f Done line; P3c mislabels (phase0 §2, EVENT_SCHEMA §11); AGENT_NAVIGATION tests rows; README "empty". Details: worklog iter-0aa.

## FAQ / Pitfalls

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

**iter-1 · core plumbing** — unconditionally the next iteration (functional
code, not docs). The research epoch is closed (D-029); the quality bar for
the code that follows is now law (D-031: L13/L14, type discipline,
fail-fast, the architecture fitness test). Decide KI#10 (the T0 validation
engine: stdlib mini-validator vs hand-rolled checks) at iter-1 kickoff —
the only open design point. Read before building:
`docs/blueprint/phase0.md` §1 (the combined donor design: RngBank, heapq
queue with sub_order bands, JSONL writer with cause-chain integrity, fold
vs incremental projection, pack loader, type discipline,
`tests/test_architecture.py`) + `docs/BLUEPRINT.md` §1 ledger rows
RNG-1/SCHED-1/STATE-1/STORE-1/TEST-1 + `MVP_SCOPE.md` §8 + `docs/TASKS.md`
iter-1 acceptance criteria. The full ref→iteration donor mapping now lives
in the blueprint build index (`docs/BLUEPRINT.md` §3) — it is no longer
restated here (D-027).
