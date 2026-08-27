# canonsim

Deterministic canonical simulation core for an LLM-narrator architecture.
Phase 0 deliverable: **TavernSim v0** — one tavern, a theft, an arson, spreading
rumors — running as a pure Python simulation with an append-only event log.
No LLM anywhere near the canon yet.

> **Simulator produces facts. LLM produces prose. The log stores canon.
> The mediator holds the boundary.**

North star: a "living world" simulation mode inside
[Soul-of-Waifu](https://github.com/jofizcd/Soul-of-Waifu) (local-first desktop
AI companion app) — see `docs/VISION.md` §10. This repo stays frontend-agnostic
until the phase-1 gate.

## Status

Phase 0, iteration 2a — the owner-requested audit of the first two code
iterations: four defects found and fixed in place (a resolver/projection
desync that could write a bad event before crashing — events now pass a
pre-write `_commit` gate; a log-path collision that could truncate a
prior run's log; three pack-lint gaps; parallel fire-spread passes that
crashed runs with two staggered fires). 155 tests green, ruff clean;
both baseline logs byte-identical through the fixes. The action layer
(iter-2) stands: intent front door with OCC, the 12 pack-driven
resolvers, scheduler DAG, and the generic fire chain. Next: iter-3 ·
knowledge, relations, expectations (`docs/TASKS.md`).

## For AI agents (primary audience)

1. `AGENTS.md` — the law: invariants, iteration protocol, caps, git safety.
2. `docs/AGENT_NAVIGATION.md` — reading gradient + where things are.
3. `docs/TASKS.md` — what to do next, with acceptance criteria.

Humans: `docs/VISION.md` for the why; `docs/MVP_SCOPE.md` for the phase-0 tech
spec. Everything here is written for agents first — dense, tabular, no prose
padding.

## Repo map

| Path | What |
|---|---|
| `AGENTS.md` | operating conventions for AI agents (law) |
| `STATUS.md` | iteration state, KIs, pitfalls (read every task) |
| `worklog.md` | capped short-term memory (≤10 entries) |
| `docs/` | all specs & plans (see `docs/AGENT_NAVIGATION.md` §1) |
| `schemas/` | machine-readable contracts (`event.schema.json`) |
| `content/tavern_pack/` | setting as data (v0.1; loaded + linted by `core/pack.py`) |
| `core/`, `sim/systems/`, `render/`, `brief/`, `cli/` | code (core landed iter-1; systems land iter-2, render/cli iter-5) |
| `tests/`, `tests/playscripts/` | test suite + seed/intent fixtures |

## Running

The core runs headless (the play CLI lands in iter-5):

```
pip install -e ".[dev]"
PYTHONHASHSEED=0 pytest -q
ruff check .
```

A playscript plays end-to-end through the simulator; see
`tests/test_loop.py` and the fixture `tests/playscripts/plumbing_smoke.json`.
Its log is byte-identical across runs on the same environment (T1).

## License

TBD — no monetization planned. Donor code/data policy and licensing stance:
`docs/ROADMAP.md` §4. Full verified source catalog: `docs/REFERENCES.md`.
