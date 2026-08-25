# STATUS — canonsim

Iteration: 0g (owner-requested: research pass before iter-1) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0g is the owner's answer to Q4 in `docs/CORE_DESIGN_RESEARCH.md` §8:
"no, not iter-1 yet — one more research pass to harden the foundation,
mine the references deeper, and finalize the concept". Per AGENTS §2.5
this is the **sixth** docs iteration in a row (0, 0b, 0c, 0e, 0f, 0g) —
the doc-loop alarm has fired; this iteration is owner-requested, so the
exception applies (D-022). iter-1 is still the next functional step; no
further docs iterations without an owner request. Q1–Q3 also answered
(yes); absorbed as D-019..D-021 in `docs/DECISIONS.md`. KI#1 and KI#2
deleted per AGENTS §5 (closed ≥3 iterations). Three new KIs logged from
the audit of the owner's critique: KI#3 expectation_violation primitive
missing, KI#4 balance harness missing, KI#5 runtime-vs-fold ambiguity.

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
- **Doc-loop alarm vs owner-requested research.** Six docs iterations in a row
  would normally force a stop (AGENTS §2.5). Owner-requested research passes
  are the explicit exception (D-022). The rule still bites: this is the last
  allowed research-only iteration before iter-1, no further exceptions
  without a fresh owner request.

## Next step

iter-1 · core plumbing is the next functional step: seed, RNG instance, clock,
event queue, JSONL log with header, playscript runner, pack loader for the
drafted `content/tavern_pack/` v0.1. Acceptance criteria in `docs/TASKS.md`.
Owner's blocking answers to Q1–Q3 are absorbed as D-019..D-021 and flip
P2a/P2b and M3/M4/M5 from proposals to accepted iter-3/iter-4/iter-6 scope.
