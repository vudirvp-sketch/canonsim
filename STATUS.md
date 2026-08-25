# STATUS — canonsim

Iteration: 0e (owner-requested: core-design research) · Phase: 0 — simulator without LLM · Date: 2026-08-25

iter-0d restored the zip-lost infra (KI#1, KI#2 closed: `.gitignore`, package
skeleton, smoke tests, pyproject discovery fix). iter-0e adds owner-requested
core-design research (`docs/CORE_DESIGN_RESEARCH.md`) — owner authorized
this docs iteration explicitly (chat, 2026-08-25). Doc-loop alarm: fired
through iter-0c, reset by iter-0d executable tests. **iter-1 must be
functional simulator code** (`docs/TASKS.md`); no further docs iterations
without an owner request.

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

## Next step

Owner: answer `docs/CORE_DESIGN_RESEARCH.md` §8 (Q1–Q4). Then iter-1 · core
plumbing: seed, RNG instance, clock, event queue, JSONL log with header,
playscript runner, pack loader for the drafted `content/tavern_pack/` v0.1.
Acceptance criteria in `docs/TASKS.md`.
