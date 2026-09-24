# canonsim

Deterministic canonical simulation core for an LLM-narrator architecture.
Phase 0 deliverable: **TavernSim v0** — one tavern, a theft, an arson, spreading
rumors — running as a pure Python simulation with an append-only event log.
No LLM anywhere near the canon yet.

> **Simulator produces facts. LLM produces prose. The log stores canon.
> The mediator holds the boundary.**

North star: a "living world" simulation mode inside
[Soul-of-Waifu](https://github.com/jofizcd/Soul-of-Waifu) (local-first desktop
AI companion app) — see `docs/VISION.md` §10. This repo stays frontend-agnostic;
the dumb-terminal frontend contract is the SoW horizon's (`docs/ROADMAP.md` §6).

## Status

**The roadmap's phase ladder is COMPLETE — phases 0..6 all CLOSED**
(`docs/ROADMAP.md` §2 the single owner of closed/open — one-liners
here, the per-phase evidence in DECISIONS' gate-verdict family):

- Phase 0 (Sim without LLM) — gate PASS iter-6: TavernSim v0, the
  chronicle reads as a story.
- Phase 1 (Narrator) — gate PASS iter-26, D-058: 0 canon violations
  over 109 live beats.
- Phase 2 (Parser) — gate PASS iter-35, D-064: 35/35 boundary
  validity over 51 utterances.
- Phase 3 (Director) — gate PASS iter-54, D-083: max eventless
  stretch 1.
- Phase 4 (Knowledge & scene) — gate PASS iter-65, D-094: 0 leaks on
  the blind-NPC suite.
- Phase 5 (Depth) — gate PASS iter-102, D-136: emergent chains
  without the player (the worldgen-fed form).
- Phase 6 (Packs & worldbuilder) — gate PASS iter-116, D-151: the
  reskin day 14m24s, zero core edits (D-149).

**The standing work**: the owner-gated backlog (`docs/TASKS.md`) + the
world track (`docs/worldbuild/`, D-186) + the Soul-of-Waifu horizon
(`docs/ROADMAP.md` §6). Track B: bg-2/3/4/7/8/9 DONE, bg-6
owner-deferred; engine-1 LANDED iter-177 (D-193 — the explicit adapter,
INV-4's one-module form).

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
| `.github/workflows/ci.yml` | CI: pytest + ruff on push to `main` (ci-1; Python 3.12.14 the env pin, `PYTHONHASHSEED=0`) |
| `docs/` | all specs & plans (the full map: `docs/AGENT_NAVIGATION.md` §1) |
| `docs/worldbuild/` | the authored-setting surface: world kernel, Resonance, the Sarrow Vale anchor, the authoring doctrine (D-186) |
| `schemas/` | machine-readable contracts (`event.schema.json`) |
| `content/` | the five packs — setting as data (tavern, road, province, grim, pressure), loaded + linted by `core/pack.py` (the admission gate; lint bodies in `core/packlint/`) |
| `core/` | the engine (stdlib-only, D-012; engine-agnostic — INV-4): the event-sourced kernel (log, queue, loop, fold), the RngBank, the knowledge/director/world/social stacks, economy, intent + resolvers, metrics, pack |
| `render/` | the deterministic renderer: the tracery grammar engine (cosmetic stream) + the chronicle/entity views (pure functions of the log) |
| `workbench/` | the Workbench family (wb rows, CONTRACTS §5, D-200): the Python half — the renderer-neutral Visual Scene IR + the read model + `application/` the application-operations skeleton (app §32 step 1: identity/artifact/directories/clock) + `api/` the inbound gateway (app §32 step 4, wb-4/D-201: the §8 envelopes + the socket-free dispatch core + `transport.py` the loopback HTTP binding — INV-4's second sanctioned network module, one per direction) + `application/operations/` the application operations (app §32 steps 5+7, wb-5/D-202 + wb-6/D-203: the §11 lifecycles + the §12 deadline/cancellation + the run registry + the model-discovery family + the §6.1 composition root — the run/model families registered on the gateway + the backend family over the injected llama.cpp port — chat.send + model.load/unload) — and `presentation/redot/` the pinned Redot 26.2 LTS project (the application shell + the semantic-token theme; the engine binary external, one `REDOT_EXE` path) |
| `brief/` | the mediator circuit (LLM-free engine side): assembler, scene ledger, validator, mediator, the mode-C parser boundary + its GBNF serialization, scan, since |
| `cli/` | the play interface: batch `play`/`chronicle`/`state`/`replay` + the interactive session with the narrator door, `--resume`, `--pack`, `--engine` (the runtime engine as the doors' operator — the adapter the repo's outbound network module; the inbound sibling workbench/api/transport.py, D-201) |
| `scripts/` | operator tooling (CLI-class, D-046): the harnesses (balance/profile/worldgen), the offline builders (chronicle/checkpoint), pack tools (scaffold/doctor), digest, docguard, the `df_*` track-B tools |
| `tests/`, `tests/playscripts/` | the suite + seed/intent fixtures |

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
python -m cli --resume logs/run_42_0.jsonl   # continue that session's run (D-139)
python -m cli chronicle logs/run_8_0.jsonl
python -m cli state purse_01 logs/run_8_0.jsonl
python -m cli replay logs/run_8_0.jsonl
```

A playscript plays end-to-end through the simulator; its log is
byte-identical across runs on the same environment (T1), and the
rendered chronicle is byte-identical, period (a pure function of the
log). Runtime logs land in `logs/` and rendered chronicles in
`output/` (both gitignored).

Fold checkpoints over a committed log (depth-4 — derived artifacts,
never truth; the session resume consumes them as its fast-path —
`--resume` restores the world as snapshot + tail replay, and the
continued run is byte-identical to an uninterrupted session):

```
python scripts/checkpoint.py logs/run_8_0.jsonl            # one end checkpoint
python scripts/checkpoint.py logs/run_8_0.jsonl --every 20 # cadence + the end
```

The one-page digest — the current state, derived (STATUS/TASKS/
DECISIONS are the sources; the digest is a viewport, never a second
truth):

```
python -m scripts.digest
```

## License

AGPL-3.0 — the GNU Affero General Public License v3.0; the full text
lives in `LICENSE` (SPDX: `AGPL-3.0-only`). Donor code/data policy and
licensing stance (what this repo takes in — a separate question from
what it publishes under): `docs/ROADMAP.md` §4. Full verified source
catalog: `docs/REFERENCES.md`.
