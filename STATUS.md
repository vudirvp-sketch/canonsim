# STATUS — canonsim

Iteration: 0f (owner-requested: manifesto absorption) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0e delivered the core-design research (`docs/CORE_DESIGN_RESEARCH.md`)
with open questions Q1–Q4 for the owner. iter-0f absorbs the architecture
manifesto that came out of the iter-0e dialogue into the four places it
belongs, **without inventing a new doc**: (a) BRIEF_SPEC sketch in
`docs/SPECS_BACKLOG.md` gets the sensory-emitter + beat-boundary delta
clause; (b) VALIDATION_SPEC sketch gets prompt-injection neutralized
**structurally** at the prose→proposal boundary (no post-hoc text
sanitization — that path is a crutch); (c) `CORE_DESIGN_RESEARCH.md` §6
gets P3e `psychological_echo` as a phase-3+ behavior modifier derived
from existing knowledge records (not new data); (d) this file gets a
`git ls-files` FAQ entry (workspace ≠ tracked). Doc-loop alarm: this
is the **fifth** docs iteration in a row (0, 0b, 0c, 0e, 0f) — iter-1
**must** be functional simulator code (`docs/TASKS.md`); no further
docs iterations without an owner request.

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

- KI#1 · `.gitignore` + code-dir skeleton (`core/`, `sim/systems/`, `render/`, `brief/`, `cli/`, `tests/`) lost in the initial zip upload; recreated this iteration with pack/schema smoke tests · CLOSED iter-0d
- KI#2 · `pyproject.toml` had no package-discovery config: `pip install -e ".[dev]"` fails (multiple top-level packages in flat layout) — the DoD gate was unreachable; fixed with an explicit packages list · CLOSED iter-0d

## FAQ / Pitfalls

- **Zip upload loses dotfiles and empty dirs.** "Add files via upload" on GitHub
  dropped `.gitignore` (and every dir without tracked files). After any future
  upload: verify `.gitignore` exists and `git status --short` shows no runtime
  artifacts (KI#1).
- **Workspace files ≠ tracked files.** `git status --short` shows changes
  *vs HEAD*, not what is *in* HEAD — a file present in your working directory
  may not be committed at all. After any structural change, run
  `git ls-files <path>` (or `git ls-files | head -50`) to confirm what is
  actually tracked. This is the diagnostic for KI#1-class losses and for
  "the file exists but tests can't find it" surprises.

## Next step

Owner: answer `docs/CORE_DESIGN_RESEARCH.md` §8 (Q1–Q4) when ready — they
are not blocking. iter-1 · core plumbing is the next functional step:
seed, RNG instance, clock, event queue, JSONL log with header, playscript
runner, pack loader for the drafted `content/tavern_pack/` v0.1. Acceptance
criteria in `docs/TASKS.md`.
