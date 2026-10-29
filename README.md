# canonsim

**A deterministic, autonomous, data-driven living-world simulation engine
for persistent, open-ended play through local LLMs.** canonsim generates
and evolves worlds whose histories emerge from interacting systems, actors,
resources, institutions, relationships, constraints, knowledge, and
persistent consequences. Long-term quality target (owner: `docs/VISION.md`
§10) — emergent-history depth on the order of the strongest
simulation-heavy games (Dwarf Fortress, RimWorld, Kenshi): a direction,
never a claim about current capability.

> **Simulator produces facts. LLM produces meaning. The log stores canon.
> The mediator holds the boundary.** — the thesis (owner: `docs/VISION.md`
> §1–§2; §6–§7 the honest limits).

**The engine generates reality; the LLM interprets and narrates it; the
player participates in it.** Canonical state and history live in an
append-only event log outside the context window — a prompt is a temporary
workbench rebuilt from persistent state, never the world's memory, and
forgetting a fact from the prompt cannot delete it from the world. The
world advances on its own — actors, institutions, and the environment act
without a player prompt and without an LLM call for every development —
and it does not exist to serve the player: player language is input, not
privileged truth; outcomes are decided by the simulator's rules (the
mechanical cure for sycophancy). What the architecture cannot fix — model
prose ceilings, refusals, narration drift — stays an honestly stated
limit, handled by validation and degradation ladders, never "solved".

Who owns what (the product meaning; the binding contracts live with their
specs):

| Component | Owns |
|---|---|
| Simulator (`core/`) | world rules, causal resolution, autonomous developments, outcomes — the sole canon authority; advances the world with no LLM in the loop |
| Event log (`core/log.py`, INV-1) | the append-only canonical history; state = fold(log); SQLite, caches, projections, summaries are rebuildable |
| Mediator & adapters (`brief/` + the sanctioned surfaces, INV-4) | the LLM boundary: intent validation, bounded perspective-correct briefs, narration validation, bounded failure handling — model output is a proposal or a presentation, never a fact |
| LLM | parse player language into structured intents; narrate authorized state (prose, dialogue, texture); never decide outcomes, invent canon, or grant unauthorized knowledge |
| Player | an embodied canonical actor under the same world rules as every other actor |
| Worldbuilding & packs (`content/`, `docs/worldbuild/`) | the setting as data — ontology, laws, entities, institutions; the engine supplies the mechanisms, the pack supplies the world |

The intended cycle (conceptual; ordering, budgets, and failure behavior
are owned by `docs/BRIEF_SPEC.md`, `docs/PARSER_SPEC.md`,
`docs/VALIDATION_SPEC.md`, `docs/DIRECTOR_SPEC.md`): retrieve the relevant
canonical state and history → assemble a bounded brief for the active
scene and authorized perspective → the LLM narrates the scene, or parses
player language into a structured intent → validate and resolve the intent
under the simulator's rules → record consequential changes through the
event log → advance autonomous world processes → assemble the next brief.
Repeat without relying on the model holding the conversation history.

**TavernSim v0 — one tavern, a theft, an arson, spreading rumors — is the
historical phase-0 proof fixture**, not the product: a bounded, LLM-free
slice that demonstrated the architecture's mechanisms run and read as a
story. The packs, benchmark corpora, and test scenarios hold the same
subordinate role — controlled environments in which mechanisms and claims
are verified. A passed gate proves its stated claim within its measured
scope; it never establishes that the ambition above is complete or
delivered.

Product and delivery horizon (owner: `docs/VISION.md` §10): the product is
the game built on this engine; the project ships its own local-first shell
(chat, inference, world views — `workbench/` + `frontend/` are the
engineering base, and the visual direction is an open owner call). This repo
stays frontend-agnostic; third-party clients (LM Studio, SillyTavern) are a
deferred modularity goal.

## Status — the verified state, not product completion

**The roadmap's phase ladder is COMPLETE — phases 0..6 all CLOSED**
(`docs/ROADMAP.md` §2 owns the closed/open state):

- Phase 0 (Sim without LLM) — TavernSim v0: the chronicle reads as a story.
- Phase 1 (Narrator) — 0 canon violations over 109 live beats.
- Phase 2 (Parser) — 35/35 boundary validity over 51 utterances.
- Phase 3 (Director) — max eventless stretch 1.
- Phase 4 (Knowledge & scene) — 0 leaks on the blind-NPC suite.
- Phase 5 (Depth) — emergent chains without the player (the worldgen-fed form).
- Phase 6 (Packs & worldbuilder) — the reskin day, zero core edits.

The ladder's closure is the completion of a verification program on bounded
slices: each gate proves its named mechanisms against its exit criteria —
none of them establishes the living-world ambition at open-ended scale.
Vision vs verified state stays explicit: `docs/VISION.md` §6–§7 (the limits)
and the authored world (`docs/worldbuild/`).

**The standing work**: the product aims (`docs/VISION.md` §10, A1–A7) + the
world track (`docs/worldbuild/`) + the product shell (the engine stays
frontend-agnostic; the web client is the shipped base).

## Where to look

By question class: the product, the why and the aims A1–A7 →
`docs/VISION.md` §10; the binding laws and contracts → the owning spec
(`docs/BRIEF_SPEC.md`, `docs/PARSER_SPEC.md`, `docs/VALIDATION_SPEC.md`,
`docs/DIRECTOR_SPEC.md`, `docs/EVENT_SCHEMA.md`); the authored world and its
frontier → `docs/worldbuild/README.md`; the phase-0 tech spec →
`docs/MVP_SCOPE.md`. Everything here is written dense and tabular.

## Repo map

| Path | What |
|---|---|
| `.github/workflows/ci.yml` | CI: `ruff` + `pytest` on push to `main` (Python 3.12.14 the env pin, `PYTHONHASHSEED=0`) + the frontend job |
| `docs/` | the specs & plans: vision, roadmap, blueprint, the per-surface specs, the authored world |
| `docs/worldbuild/` | the authored-setting surface: world kernel, Resonance, the Sarrow Vale anchor, the authoring doctrine |
| `schemas/` | machine-readable contracts (`event.schema.json`) |
| `content/` | the six packs — setting as data (tavern, road, province, grim, pressure, farstead), loaded + linted by `core/pack.py` (the admission gate; lint bodies in `core/packlint/`) |
| `core/` | the engine (stdlib-only, D-012; engine-agnostic — INV-4): the event-sourced kernel (log, queue, loop, fold), the RngBank, the knowledge/director/world/social stacks, economy, intent + resolvers, metrics, pack |
| `render/` | the deterministic renderer: the tracery grammar engine (cosmetic stream) + the chronicle/entity views (pure functions of the log) |
| `frontend/` | the ACTIVE web client (frontend-1, D-244): React + TypeScript + Vite, Web/PWA-first — the S0 walking skeleton over the existing loopback gateway (`POST /op`, INV-4 untouched: the browser is a gateway client, never a fourth network surface; typed runtime-validated payloads, the virtualized LIVE Trajectory tail, per-tab independent clients; POST-only — no SSE/WebSocket in S0; dev serves via the Vite proxy to `127.0.0.1:8765`) |
| `workbench/` | the Workbench family (wb rows, CONTRACTS §5, D-200): the Python half — the renderer-neutral Visual Scene IR + the read model + `application/` the application-operations skeleton (app §32 step 1: identity/artifact/directories/clock) + `api/` the inbound gateway (app §32 step 4, wb-4/D-201: the §8 envelopes + the socket-free dispatch core + `transport.py` the loopback HTTP binding — INV-4's second sanctioned network module, one per direction) + `application/operations/` the application operations (app §32 steps 5+7, wb-5/D-202 + wb-6/D-203: the §11 lifecycles + the §12 deadline/cancellation + the run registry + the model-discovery family (`model.fetch` the URL arrival + `model.import` the LOCAL native-picker arrival — wb-10/D-209, no network) + the §6.1 composition root — the run/model families registered on the gateway + the backend family over the injected llama.cpp port — chat.send + model.load/unload + model.states) + `platform/` the OS mechanics (wb-8/D-205: the managed llama-server's process row — spawn/observe/graceful-stop, the injected readiness probe; wb-9/D-208: + `model_fetch.py` the outbound model-assets fetch — INV-4's third sanctioned network surface, owner-gated) + `application/settings.py` (wb-9: the launch-settings store + the backend.settings operations); the live stack's app-gateway `scripts/workbench_app.py` (wb-7 + wb-8 + wb-9: the gateway + the operations + the injected llama.cpp backend port + the launch-settings store + the injected fetcher, served on loopback — the frontend dials the gateway only; MANAGED the default = the launcher owns the llama-server process, spawning it on the first model.load; the runtime layout workbench/runtime/{models,llama.cpp,settings.json} gitignored) + `scripts/workbench_launch.py` the ZERO-COMMAND launcher (wb-9 + wb-10, re-pointed to the web client at D-245: the gateway + the Vite dev server together — npm resolved over PATH, the first-run npm install, the observed bind URL forwarded as GATEWAY_TARGET, the honest two-child shutdown; `Workbench.bat` at the repo root is the double-click entry; the Redot presentation tree DELETED at D-245 — recovery: git history) |
| `brief/` | the mediator circuit (LLM-free engine side): assembler, scene ledger, validator, mediator, the mode-C parser boundary + its GBNF serialization, scan, since |
| `cli/` | the play interface: batch `play`/`chronicle`/`state`/`replay` + the interactive session with the narrator door, `--resume`, `--pack`, `--engine` (the runtime engine as the doors' operator — the adapter the repo's outbound network module; the inbound sibling workbench/api/transport.py, D-201) |
| `scripts/` | operator tooling (CLI-class, D-046): `check.py` (the named verification profiles), `docguard.py`, the harnesses (balance/profile/worldgen), the offline builders (chronicle/checkpoint), pack tools, topology, the `df_*` track-B tools |
| `tests/`, `tests/playscripts/` | the suite + seed/intent fixtures |

## Running

The interpreter is pinned (the T1 golden byte-compare is same-environment
only, `docs/TEST_PLAN.md` §1.1): **CPython 3.12.14**. A local checkout keeps it
in `.venv` — the pinned standalone build, dev deps `pytest` + `ruff` only:

```
python -m venv .venv && .venv\Scripts\python -m pip install -e ".[dev]"   # Windows
python scripts/check.py full        # the per-commit gate: pytest -q + ruff
python scripts/check.py docs        # docguard + reference scan, ~1 s
python scripts/check.py frontend    # vitest + tsc
python scripts/check.py model       # headless gateway; asset roots resolve
python scripts/check.py --help      # all profiles
```

Raw forms, if you need them: `PYTHONHASHSEED=0 pytest -q`, `ruff check .`,
`python scripts/docguard.py`. A profile that cannot run reports `SKIPPED` with
its reason and is recorded as such — never as green.

The runtime payload — the GGUF pool (18.6 GB), the llama.cpp build and the
station-pack archive — lives OUTSIDE the working tree in the workspace asset
area. `workbench/platform/assets.py` is the one resolver (env override
`CANONSIM_MODELS_ASSETS` / `CANONSIM_LLAMA_ROOT` → the workspace pool → the
in-tree `workbench/runtime/` drop folder), so a fresh clone still starts with
no configuration.

The Workbench (the owner's zero-command form — no console needed):

double-click **`Workbench.bat`** at the repo root (the gateway + the
web frontend together; needs Python 3.11+ and Node.js LTS on PATH —
the first run installs the web client's dependencies by itself, and
the browser opens on its own). The command forms:

```
python scripts/workbench_launch.py                 # from the repo ROOT
python scripts/workbench_launch.py --no-frontend  # the gateway alone
python scripts/workbench_app.py                    # the app-gateway alone
```

The ACTIVE web frontend (frontend-1, D-244 — React + TS + Vite; the
Redot tree deleted at D-245): `Workbench.bat` starts both halves —
the gateway + the Vite dev server — and opens the browser; by hand:
start the gateway (`python scripts/workbench_app.py` — default bind
`http://127.0.0.1:8765/op`), then:

```
cd frontend
npm install
npm run dev        # the Vite dev server; its /gateway proxy dials
                   # the loopback gateway (POST /op only in S0)
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

## License

AGPL-3.0 — the GNU Affero General Public License v3.0; the full text
lives in `LICENSE` (SPDX: `AGPL-3.0-only`). Donor code/data policy and
licensing stance (what this repo takes in — a separate question from
what it publishes under): `docs/ROADMAP.md` §4.
