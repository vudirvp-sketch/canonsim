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

Phase 0, iteration 4 — the director + goal ticker stands: hooks seeded
at event time sit in a per-run buffer (D-005 — a complication from
nowhere is a bug); explicit triggers (time / place / threshold) fire
causally; the stagnation detector releases the lowest-threshold hook
when narrative entropy (P2e: sum of seeded-hook weights + global
suspicion + visible physical threats — observable state only, L6)
drops below the pack's floor. Releases ride the intent door (phase0 §4
"Objective broadcast") — a released hook produces an IntentData the
loop enqueues band NPC_REACTION; the director never writes canon
itself. Director-off (T8 A/B baseline) keeps the buffer seeding but
suppresses releases. P2b goal ticker (D-021): per-NPC probability
rolls on the beat cycle, intents through the front door — M5 non-PC
share non-trivially non-zero by construction. States decay passes
deferred from iter-3 landed (fatigue/intoxication/fear proportional
deltas; injury never decays — T4 preserved). Arrest resolution
(iter-3 leftover): evasion_vs_pursuit → arrest_resolved, `crime_status
→ caught` (irreversible). Crossings fire in TICK ORDER (rotations and
beats interleave by tick, not by type — the log writer's
tick-monotonicity invariant). 219 tests green, ruff clean; golden
fixture byte-identical (the 58-tick plumbing_smoke scenario crosses
no beat — no decay, no urgency, no director release). Next: iter-5 ·
chronicle & CLI (`docs/TASKS.md`).

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
