# STATUS — canonsim

Iteration: 0i (owner-requested: ref-1 deep dive) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0i is the owner's explicit follow-up to iter-0h: ship the first
solo ref-N deep dive (`ref-1` per `docs/TASKS.md` infra backlog).
`ref-1` covers the **other half of Dwarf Fortress** — worldgen +
history layer — vs the export-schema half in iter-0h. New §3 in
`docs/REFERENCES_DEEP.md`: history ticks, populations vs notables
LOD, age/civ dynamics, artifact anchors, reputation as event. §2 of
the same file aggressively trimmed (cap 400, AGENTS §6) — cross-refs
preserved, multi-line sub-content collapsed to single clauses. Per
AGENTS §2.5 this is the **eighth** docs iteration in a row (0, 0b,
0c, 0e, 0f, 0g, 0h, 0i; iter-0d was infra, not docs) — the doc-loop
alarm has fired again; this iteration is owner-requested, so the D-022
exception applies. iter-1 is still the next functional step; no
further docs iterations without a fresh owner request. KI#3, KI#4,
KI#5 unchanged.

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index.
- INV-2 Determinism: single seeded RNG, no wall-clock, `sorted()` iteration,
  fixed `PYTHONHASHSEED`, queue key `(tick, sub_order, actor_id)`.
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#3 · `expectation_violation` primitive missing — NPC reacts only to presence in `knowledge`, not to absence (purse gone, guard missing). Fix: P2d in `CORE_DESIGN_RESEARCH.md` §6, slated for iter-3.
- KI#4 · balance harness (1000-sim distribution plots of `suspicion` / `fire_spread`) missing — MVP_SCOPE §15 promises an iter-6 baseline but no tool exists. Added as `balance-1` in `docs/TASKS.md` infra backlog.
- KI#5 · runtime state vs test fold not explicitly separated — risk of O(N²) at startup if `fold(log)` is misused as runtime path. D-023 records the rule: runtime = incremental projection; fold = T2 replay only.

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
- **Doc-loop alarm vs owner-requested research.** Seven docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0i is the eighth docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i; iter-0d was infra).
- **Catalog vs deep dives vs synthesis — three places, three jobs.**
  `docs/REFERENCES.md` is the **catalog** (license, URL, phase gating,
  intake rules). `docs/CORE_DESIGN_RESEARCH.md` §2 is the **synthesis**
  (one-line depth primitive + failure mode per source).
  `docs/REFERENCES_DEEP.md` is the **deep dive** (named mechanics, real
  data structures, what we take/adapt/inspire, strengths/weaknesses, and
  a per-source verdict). Drift rule (AGENTS §3): never restate across
  these three — link only. A future reference detail belongs in deep
  dives, not in the catalog or the synthesis table.

## Next step

iter-1 · core plumbing is the next functional step: seed, RNG instance, clock,
event queue, JSONL log with header, playscript runner, pack loader for the
drafted `content/tavern_pack/` v0.1. Acceptance criteria in `docs/TASKS.md`.
Owner's blocking answers to Q1–Q3 are absorbed as D-019..D-021 and flip
P2a/P2b and M3/M4/M5 from proposals to accepted iter-3/iter-4/iter-6 scope.
