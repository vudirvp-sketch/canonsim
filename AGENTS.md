# AGENTS.md — Operating Conventions for AI Agents

> Law for anyone (agent or human) making non-trivial changes in this repo.
> Trivial changes (typo, single value, doc fix) may proceed from `STATUS.md` alone.
> Repo language: English (docs, code, identifiers, commit messages). Chat with the
> owner: Russian.

## 1. What this repo is

`canonsim` — a deterministic canonical simulation core (Python, stdlib-first).
Phase 0 builds **TavernSim v0**: one tavern scenario (theft, arson, rumors) that
runs and reads as a story **without any LLM**. North star: a simulation mode
inside Soul-of-Waifu (`docs/VISION.md` §10).

Two work tracks (`docs/ROADMAP.md` §1):

- **A (main):** the simulator, no LLM. Iterations `iter-N`.
- **B (background):** LLM-circuit spikes on foreign canon (Dwarf Fortress
  Legends XML). Tasks `bg-N`. Never blocks track A; can be dropped independently.

## 2. Iteration protocol

1. Plan first, then code. Better to underdeliver than to break things — the
   remainder goes into the next iteration.
2. Task ID: `iter-<N>-<short-desc>` or `bg-<N>-<short-desc>`. One iteration =
   one task ID from `docs/TASKS.md`.
3. Soft limit: 3–5 files per iteration. If objectively more are needed,
   continue, but note the scope in `worklog.md`.
4. Scope creep = stop. Anything not required by the current task ID goes into
   the `docs/TASKS.md` backlog, not into the diff.
5. **Anti-loop rules:**
   - The same failing fix attempted twice → record a KI in `STATUS.md`, stop,
     ask the owner. Never a third blind retry.
   - Patch files in place (targeted edit); never regenerate a whole file to fix
     a small bug.
   - Two consecutive iterations producing only doc edits with no functional
     progress → stop and ask the owner (documentation-loop alarm).

## 3. Reading gradient

Before working, follow the gradient in `docs/AGENT_NAVIGATION.md` §2.

Token hygiene: never read JSONL logs whole — use `tail`, `wc -l`, or a
`python -c` extraction one-liner. `docs/VISION.md` is the distilled source of
truth; the original concept documents live outside this repo — do not ask for
them.

## 4. Invariants (P0 — a violation is a bug of the highest severity)

| ID | Invariant | Enforced by |
|---|---|---|
| INV-1 | **Event sourcing.** No state change outside an event. State = fold(log). The raw JSONL log is the only truth; SQLite is a rebuildable index. | T2 replay test; review |
| INV-2 | **Determinism.** One `random.Random(seed)` instance; no wall-clock (including the log header); iteration only via `sorted()` or construction order; queue key `(tick, sub_order, actor_id)`; `PYTHONHASHSEED=0`. | T1 byte-identical test |
| INV-3 | **Content/code split.** Core code contains no domain words ("guard", "purse", "tavern"). All setting data lives in `content/tavern_pack/*.json`. | grep stoplist test (from iter-2) |
| INV-4 | **LLM boundary.** No LLM or network calls in track A before the phase-0 gate passes. | review; import check |
| INV-5 | **Log immutability.** Committed logs are never edited; corrections are new events. Runtime logs are never committed. | review; `.gitignore` |

## 5. Bug → doc → fix (KI lifecycle)

Found a bug → first record it in `STATUS.md` as `KI#<N>`, then fix it.

- On open: one line — `KI#<N> · short description · date opened`.
- On close: mark `CLOSED iter-<N>`; do not delete immediately.
- Any KI closed for more than 2 iterations MUST be deleted at the start of the
  next iteration that touches `STATUS.md`. This is mandatory cleanup, same
  priority as writing new entries — not "later housekeeping".

## 6. Output caps (anti-bloat — enforced every iteration)

| File | Cap |
|---|---|
| `STATUS.md` | ≤15 active KIs, ≤2 lines each; FAQ ≤20 entries; no stack traces or snippets — link the worklog entry |
| `worklog.md` | ≤10 entries, 3–5 lines each; adding #11 requires deleting the oldest in the same edit (one in, one out) |
| `docs/*.md` | ≤400 lines each (`MVP_SCOPE.md` ≤450). Over cap → trim before adding, in the same turn |
| `docs/AGENT_NAVIGATION.md` | structure changes only; never history or narrative |
| `docs/DECISIONS.md` | append-only; ≤30 entries; supersede, don't delete |
| `docs/TASKS.md` | done tasks collapse to one line at the end of each iteration |

General rule: check the current size before writing to any of these. The trim
is part of the task, not future work. Long-term design rationale goes to
`docs/DECISIONS.md`, never to the worklog.

## 7. Git safety

- NEVER `git add -A` / `git add .` / `git add -u`. Only `git add <specific paths>`.
- Runtime artifacts are gitignored and must never be staged: `logs/`, `output/`,
  any `*.jsonl` outside `tests/fixtures/`.
- Committed by design: `docs/`, `schemas/`, `content/`, `tests/` (including
  `tests/playscripts/*.json` fixtures).
- Commit messages: `iter-N-desc: what changed`. No secrets, no `.env`.
- Before every commit, verify with `git status --short` that nothing forbidden
  is staged.

## 8. Stop & confirm (owner approval required before proceeding)

- A **breaking** change to `schemas/event.schema.json` or
  `docs/EVENT_SCHEMA.md` (rename/remove a field, remove an enum value) —
  requires a `schema_version` bump + migration note.
- Changing the queue key, tick semantics, or log header fields.
- Adding any runtime dependency (core is stdlib-only) or bumping
  `requires-python`.
- Touching CI workflow files.
- Introducing any LLM/network call into track A (phase-0 gate must pass first).
- Moving or renaming top-level directories.
- Deleting or rewriting committed log or fixture files.

## 9. Definition of Done + stop-point report

An iteration is done when:

- `pytest -q` is green and `ruff check .` is clean;
- docs affected by the change are synced (`docs/AGENT_NAVIGATION.md` §1 if
  structure changed; `docs/TASKS.md` statuses updated);
- caps (§6) are respected;
- the stop-point report is posted:

```
Done: ...
Not done: ... (reason)
Next: ...
Active KIs: ...
```

- If files changed, end the report with the exact git commands to run, listing
  each changed file explicitly (never `.` / `-A` / wildcards).

## 10. Environment (determinism)

```
PYTHONHASHSEED=0
Python >= 3.11
dev deps: pytest, ruff — nothing else
```

The byte-identical replay guarantee holds for the same environment only; the
log header records the Python version (see `docs/TECH_NOTES.md` §4).
