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
specs — `docs/AGENT_NAVIGATION.md` §3 the map):

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

Delivery horizon (owner: `docs/VISION.md` §10): a "living world"
simulation mode inside
[Soul-of-Waifu](https://github.com/jofizcd/Soul-of-Waifu) (local-first
desktop AI companion app). This repo stays frontend-agnostic; the
dumb-terminal frontend contract is the SoW horizon's (`docs/ROADMAP.md`
§6).

## Status — the verified state, not product completion

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

The ladder's closure is the completion of a verification program on
bounded slices: each gate proves its named mechanisms against its exit
criteria — none of them establishes the living-world ambition at
open-ended scale. Vision vs verified state stays explicit:
`docs/VISION.md` §6–§7 (the limits), `STATUS.md` (the current state +
next step), `docs/TASKS.md` (the standing backlog), `docs/worldbuild/`
(the authored world and its active frontier).

**The standing work**: the owner-gated backlog (`docs/TASKS.md`) + the
web-frontend track (`docs/FRONTEND_WEB_LAW.md`) + the world track
(`docs/worldbuild/`, D-186) + the Soul-of-Waifu horizon
(`docs/ROADMAP.md` §6). Track B: bg-2/3/4/7/8/9 DONE, bg-6
owner-deferred; engine-1 LANDED iter-177 (D-193 — the explicit adapter,
INV-4's one-module form).

## For AI agents (primary audience)

1. `AGENTS.md` — the law: invariants, iteration protocol, caps, git safety.
2. `docs/AGENT_NAVIGATION.md` — reading gradient + where things are.
3. `docs/TASKS.md` — what to do next, with acceptance criteria.
4. `docs/FRONTEND_WEB_LAW.md` — the ACTIVE frontend path (React + TS +
   Vite, Web/PWA-first; the S0 skeleton gate; entry surface
   `docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md`). The Redot tree is
   DELETED (D-245, the owner's «удаляй redot» call) — the git history
   + the archived agent pack preserve the reference material.

By question class: the product and the why → `docs/VISION.md`; the laws →
`AGENTS.md` §4 + the owning specs; the current state and next step →
`STATUS.md`; the authored world and its frontier →
`docs/worldbuild/README.md` → `docs/worldbuild/WORLD_TRACK_AGENT_CONTEXT.md`.

Humans: `docs/MVP_SCOPE.md` for the phase-0 tech spec. Everything here is
written for agents first — dense, tabular, no prose padding.

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
| `content/` | the six packs — setting as data (tavern, road, province, grim, pressure, farstead), loaded + linted by `core/pack.py` (the admission gate; lint bodies in `core/packlint/`) |
| `core/` | the engine (stdlib-only, D-012; engine-agnostic — INV-4): the event-sourced kernel (log, queue, loop, fold), the RngBank, the knowledge/director/world/social stacks, economy, intent + resolvers, metrics, pack |
| `render/` | the deterministic renderer: the tracery grammar engine (cosmetic stream) + the chronicle/entity views (pure functions of the log) |
| `frontend/` | the ACTIVE web client (frontend-1, D-244): React + TypeScript + Vite, Web/PWA-first — the S0 walking skeleton over the existing loopback gateway (`POST /op`, INV-4 untouched: the browser is a gateway client, never a fourth network surface; typed runtime-validated payloads, the virtualized LIVE Trajectory tail, per-tab independent clients; POST-only — no SSE/WebSocket in S0; dev serves via the Vite proxy to `127.0.0.1:8765`) |
| `workbench/` | the Workbench family (wb rows, CONTRACTS §5, D-200): the Python half — the renderer-neutral Visual Scene IR + the read model + `application/` the application-operations skeleton (app §32 step 1: identity/artifact/directories/clock) + `api/` the inbound gateway (app §32 step 4, wb-4/D-201: the §8 envelopes + the socket-free dispatch core + `transport.py` the loopback HTTP binding — INV-4's second sanctioned network module, one per direction) + `application/operations/` the application operations (app §32 steps 5+7, wb-5/D-202 + wb-6/D-203: the §11 lifecycles + the §12 deadline/cancellation + the run registry + the model-discovery family (`model.fetch` the URL arrival + `model.import` the LOCAL native-picker arrival — wb-10/D-209, no network) + the §6.1 composition root — the run/model families registered on the gateway + the backend family over the injected llama.cpp port — chat.send + model.load/unload + model.states) + `platform/` the OS mechanics (wb-8/D-205: the managed llama-server's process row — spawn/observe/graceful-stop, the injected readiness probe; wb-9/D-208: + `model_fetch.py` the outbound model-assets fetch — INV-4's third sanctioned network surface, owner-gated) + `application/settings.py` (wb-9: the launch-settings store + the backend.settings operations); the live stack's app-gateway `scripts/workbench_app.py` (wb-7 + wb-8 + wb-9: the gateway + the operations + the injected llama.cpp backend port + the launch-settings store + the injected fetcher, served on loopback — the frontend dials the gateway only; MANAGED the default = the launcher owns the llama-server process, spawning it on the first model.load; the runtime layout workbench/runtime/{models,llama.cpp,settings.json} gitignored) + `scripts/workbench_launch.py` the ZERO-COMMAND launcher (wb-9 + wb-10, re-pointed to the web client at D-245: the gateway + the Vite dev server together — npm resolved over PATH, the first-run npm install, the observed bind URL forwarded as GATEWAY_TARGET, the honest two-child shutdown; `Workbench.bat` at the repo root is the double-click entry; the Redot presentation tree DELETED at D-245 — recovery: git history) |
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
