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

Phase 0, iteration 0aa — owner-requested pre-code documentation audit:
11 drift findings fixed (tick arithmetic, calendar remnants, citation
mislabels, map gaps); readiness verdict recorded — the rigging for
iter-1 is complete, one design point open (KI#10: the stdlib
JSON-Schema validation engine). No code yet; first code lands in iter-1
(`docs/TASKS.md`) — unconditionally next.

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
| `content/tavern_pack/` | setting as data (v0.1 drafted; loader in iter-1) |
| `core/`, `sim/systems/`, `render/`, `brief/`, `cli/` | code (skeletons since iter-0d; first code lands iter-1) |
| `tests/`, `tests/playscripts/` | test suite + seed/intent fixtures |

## Running

Nothing runs yet. When iter-1 lands:

```
pip install -e ".[dev]"
pytest -q
python -m cli play tests/playscripts/day1_theft_and_arson.json
```

## License

TBD — no monetization planned. Donor code/data policy and licensing stance:
`docs/ROADMAP.md` §4. Full verified source catalog: `docs/REFERENCES.md`.
