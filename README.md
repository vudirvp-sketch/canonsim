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

Phase 0, iteration 4a — the owner-requested code audit of iter-3/iter-4
closed: 124 probe runs (60-seed day1 sweep × director on/off, T1
double-runs, T2 folds, crafted records) found zero crashes, desyncs or
replay breaks — determinism, event sourcing and T4 held. Four KIs
fixed: autonomous (urgency/director) intents never advance the
playscript (only the player's own step endings feed the next step);
the crime-status flip guards the pack's ordered `status_values`
progression (caught never downgrades to suspect — T4);
`reset_on_rotation` implemented (flagged axes reset for the watch
participants on the watch_change event; per-axis last-change decay
baseline); dead pack keys removed (single owners stay — D-024). The
audited iter-4 systems stand: the consequence-planner director (D-005:
hooks seeded at event time, entropy floor, releases through the intent
door), the P2b goal ticker (D-021), states decay passes, arrest
resolution (evasion_vs_pursuit → arrest_resolved, caught irreversible),
crossings firing in tick order (D-038). 225 tests green, ruff clean;
golden fixture byte-identical. Next: iter-5 · chronicle & CLI
(`docs/TASKS.md`).

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
