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

**Phase 0 gate: PASS** (iter-6, 2026-08-28). All `MVP_SCOPE.md` §16
exit criteria met; no kill-criteria hit. The simulator produces
facts; the chronicle reads them from the log; the world acts without
the player (M5 p50=0.77 across 1000 seeds); old events surface later
via the reaction cascade + watch rotation; losses are permanent (the
backyard stays destroyed — T4). The gate deliverables: `docs/TEST_PLAN.md`
(T0–T8 + M1–M5 + gate protocol + UAP crosswalk), `core/metrics.py`
(M1–M5 + emergent-chain count as pure functions of the log — Mesa
`DataCollector` inverted), the T1 fixture-regeneration guard
(schema-version pin + fresh-regen byte diff), `tests/test_t8_ab.py`
(single-factor A/B: ≥3 emergent chains OFF, director_0000 fires ON,
seed 125 gate playscript), `scripts/balance_harness.py` (KI#4 close —
the 1000-sim distribution harness; full table in `output/`). Phase 1
(narrator over the log) opened with the iter-7 intake and landed its
first deliverable at iter-8: `docs/BRIEF_SPEC.md` + `brief/assembler.py`
— the deterministic six-block brief (budgets, eviction, voice
isolation) as pure functions of the log, zero RNG, byte-identical on
the golden fixture. 329 tests green, ruff clean, golden fixture
byte-identical. Next: iter-9+, `VALIDATION_SPEC.md` + the validator's
LLM-free half (`docs/TASKS.md`); the narrator LLM boundary is an
owner-gated checkpoint (AGENTS §8). Track B (`bg-1..bg-4`) unblocked
for parallel LLM-circuit spikes on Dwarf Fortress Legends XML.

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
| `core/`, `sim/systems/`, `render/`, `brief/`, `cli/` | code (core iter-1..4; the iter-3/4 systems live in `core/` per D-037 — `sim/systems/` stays reserved for periphery; render + cli landed iter-5; `core/metrics.py` landed iter-6; `brief/assembler.py` landed iter-8 — the deterministic brief, `docs/BRIEF_SPEC.md`) |
| `scripts/` | operator tooling (CLI-class, D-046): `balance_harness.py` iter-6 (the 1000-sim distribution harness, KI#4 close) |
| `tests/`, `tests/playscripts/` | test suite + seed/intent fixtures |

## Running

```
pip install -e ".[dev]"
PYTHONHASHSEED=0 pytest -q
ruff check .
```

Play the slice (no LLM anywhere):

```
python -m cli play tests/playscripts/day1_theft_and_arson.json
python -m cli                      # interactive session ('help' lists commands)
python -m cli chronicle logs/run_8_0.jsonl
python -m cli state purse_01 logs/run_8_0.jsonl
python -m cli replay logs/run_8_0.jsonl
```

A playscript plays end-to-end through the simulator; its log is
byte-identical across runs on the same environment (T1), and the
rendered chronicle is byte-identical, period (a pure function of the
log). Runtime logs land in `logs/` and rendered chronicles in
`output/` (both gitignored).

## License

TBD — no monetization planned. Donor code/data policy and licensing stance:
`docs/ROADMAP.md` §4. Full verified source catalog: `docs/REFERENCES.md`.
