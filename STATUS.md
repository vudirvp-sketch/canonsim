# STATUS — canonsim

Iteration: 0w (owner-requested: post-reference concept realignment — D-029;
the skeleton stands, the sprint calendar falls) · Phase: 0 — simulator
without LLM · Date: 2026-08-27

iter-0w realigns the plan documents to the post-reference reality (D-029,
owner-requested concept review). **Verdict: the concept skeleton stands** —
thesis, three layers, INV-1..5, and the phase gates 0–6 all survived the
33-reference digestion; what changed is the mechanics inside each phase, now
owned by the blueprint layer (D-027/D-028). Plan drift fixed (KI#9, opened/
closed): the pre-research two-week day-numbered sprint calendar is dropped
(`MVP_SCOPE.md` §17 → iteration-counted; TASKS day-tags removed);
`CORE_DESIGN_RESEARCH.md` flips to absorbed per its own lifecycle rule (P2c
remains the only owner-pending proposal); `ROADMAP.md` §2 links the blueprint
as the per-phase architecture owner; README Status refreshed to 0w. No code,
no spec writing, no ref-N.

**Doc-loop accounting:** 22nd consecutive docs iteration — owner-requested
exception (D-022 wording: a fresh owner request). The alarm condition stands,
now with teeth: **iter-1 (functional code) is unconditionally the next
iteration** — no ref-N, no spec writing, no doc polish without a fresh owner
request.

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index.
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
- KI#7 · CLOSED iter-0v · capped-memory drift — worklog entries at ~880 lines vs the 3–5-line law; TASKS done entries uncollapsed. Resolved: worklog trimmed to the 10×3–5 cap; TASKS done-entries collapsed to one line; pre-trim history lives in git (commits pre-iter-0v).
- KI#8 · CLOSED iter-0v · RNG-1 vs INV-2 wording contradiction — the iter-0u audit's blocking finding: the old "one `random.Random(seed)` instance" law text contradicted the RngBank design in AGENTS.md + TASKS iter-1 + TECH_NOTES §4; `stable_hash` was undefined (a built-in `hash()` would have depended on `PYTHONHASHSEED` silently). Resolved by D-028: INV-2 rewritten, sha256-based `stable_hash` pinned, all three sync points fixed in the same iteration.
- KI#9 · CLOSED iter-0w · plan-calendar & lifecycle drift — `MVP_SCOPE.md` §17 + TASKS iter-1..6 headers still carried the pre-research two-week sprint day-tags; `CORE_DESIGN_RESEARCH.md` fully absorbed but not flipped per its own lifecycle rule; README Status stuck at "iteration 0"; `ROADMAP.md` §2 not linked to the blueprint. Resolved by D-029: calendar dropped (iteration-counted sequencing), lifecycle flipped, README refreshed, blueprint pointer added.

## FAQ / Pitfalls

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
- **Doc-loop alarm vs owner-requested research.** Twenty-two docs iterations
  in a row would normally force a stop (AGENTS §2.5). Owner-requested passes
  are the explicit exception (D-022) — the documented condition is a fresh
  owner request (iter-0s/0t additionally had fresh external sources;
  iter-0u/0v — distillation and audit; iter-0w — concept realignment — rest
  on the request alone). iter-0w is the twenty-second docs iteration in a
  row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n, 0o, 0p, 0q, 0r,
  0s, 0t, 0u, 0v, 0w; iter-0d was infra). All ref-N backlog items are
  complete — ref-1 through ref-13 plus the iter-0h cousins; ref-14/ref-15
  (Sims, Prom Week) are owner-request-only candidates; no doc pass at all
  without a fresh owner request. **iter-1 code is next, unconditionally.**
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
- **License drift between catalog and index (KI#6, closed iter-0n; pitfall
  persists).** The `REFERENCES_DEEP.md` §2 index table is **not** the source
  of truth for licenses — `REFERENCES.md` (the catalog) is. Diagnostic:
  before flipping any ref-N row todo→done, grep the source row in
  `REFERENCES.md` and verify the license column matches the index entry.
  The standing pre-flip check is exercised across iter-0o/0p/0q/0r/0s/0t;
  iter-0u touched no ref rows, so no check was needed this iteration.

## Next step

**iter-1 · core plumbing** — unconditionally the next iteration (functional
code, not docs). The research epoch is closed (D-029); no plan-level
blockers remain. Read before building: `docs/blueprint/phase0.md` §1 (the
combined donor design: RngBank, heapq queue with sub_order bands, JSONL
writer with cause-chain integrity, fold vs incremental projection, pack
loader) + `docs/BLUEPRINT.md` §1 ledger rows RNG-1/SCHED-1/STATE-1/STORE-1/
TEST-1 + `MVP_SCOPE.md` §8 + `docs/TASKS.md` iter-1 acceptance criteria.
The full ref→iteration donor mapping now lives in the blueprint build
index (`docs/BLUEPRINT.md` §3) — it is no longer restated here (D-027).
