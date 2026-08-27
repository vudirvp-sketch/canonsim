# AGENT_NAVIGATION.md — Where Things Are

> Current-state map: describes what IS, not what happened. Update §1 in the
> same iteration any structure changes. No history, no narrative.

## 1. Where things are

| Path | Purpose | Status |
|---|---|---|
| `README.md` | entry point, repo map | stable |
| `AGENTS.md` | operating law for agents | stable |
| `STATUS.md` | iteration state, KIs, FAQ | every iteration |
| `worklog.md` | capped short-term memory | every iteration |
| `docs/VISION.md` | frozen why + honest limits | frozen |
| `docs/MVP_SCOPE.md` | phase-0 tech spec (TavernSim v0) | active |
| `docs/EVENT_SCHEMA.md` | event contract | active |
| `docs/ROADMAP.md` | phases, gates, tracks, donors | active |
| `docs/TASKS.md` | backlog + iteration statuses | active |
| `docs/TECH_NOTES.md` | rotting notes: models, hardware, DF spike | live |
| `docs/DECISIONS.md` | ADR-lite, stable decisions | append-only |
| `docs/SPECS_BACKLOG.md` | just-in-time spec queue | active |
| `docs/CORE_DESIGN_RESEARCH.md` | depth-first core design: reference synthesis, gaps, proposals | absorbed (D-029; P2c owner-pending); retired at the phase-0 gate review (`doc-1`) |
| `docs/BLUEPRINT.md` | reference distillation: resolution ledger (12 mechanisms) + cross-cutting laws + build index; entry to `docs/blueprint/` | active (iter-0u); maintained at deep-dive time |
| `docs/blueprint/` | per-part applied synthesis: `phase0.md` (iter-1..6 combined donor designs), `phases.md` (phases 1–6 architecture + cross-cutting) | active; read before the matching iteration/phase |
| `docs/REFERENCES.md` | external source catalog: donors, licenses, phase gating | active (rots — quarterly review) |
| `docs/REFERENCES_DEEP.md` | index + format template + iteration plan for per-ref deep dives; the deep-dive content lives in `docs/ref/` (D-026) | active (rots — quarterly review alongside `doc-2`) |
| `docs/ref/` | per-reference deep dives (one file per source: `neighborly.md`, `mesa.md`, `df_legends_xml.md`, `df_worldgen.md`, `cdda_data_json.md`, `paradox_scripting.md`, `rimworld.md`, `l4d_director.md`, `alien_isolation.md`, `wesnoth_wml.md`, `endless_sky_dsl.md`, `ink.md`, `tracery.md`, `brogue.md`, `dcss.md`, `keeperrl.md`, `generative_agents.md`, `ai_town.md`, `letta.md`, `azgaar_fmg.md`, `natural_earth.md`, `geonames.md`, `libtcod.md`, `rot_js.md`, `red_blob_games.md`, `entt.md`, `bevy.md`, `eventstore.md`, `sqlite_fts5.md`, `duckdb.md`, `sqlite_vec.md`, …); mechanics, take/adapt/inspire/strengths/weaknesses/verdict | active (rots — quarterly review alongside `doc-2`) |
| `schemas/event.schema.json` | machine-readable event contract | synced with `docs/EVENT_SCHEMA.md` |
| `core/` | engine: clock, rng, queue, log writer, fold/replay | skeleton restored iter-0d; code lands iter-1 |
| `sim/systems/` | the 8 systems (`MVP_SCOPE.md` §5) | skeleton restored iter-0d; code lands iter-2 |
| `content/tavern_pack/` | the setting as data | v0.1 drafted (iter-0c); loader lands iter-1 |
| `render/` | chronicle templates | skeleton restored iter-0d; code lands iter-5 |
| `brief/` | frame/brief assembler | skeleton restored iter-0d; reserved for phase 1 |
| `cli/` | play interface | skeleton restored iter-0d; code lands iter-5 |
| `tests/` | test suite | pack/schema smoke tests (iter-0d); T0–T8 land iter-1+ |
| `tests/fixtures/` | committed golden fixtures for T0/T1 (log lines, byte-identical run outputs) | empty; first fixtures land iter-1 (`.gitignore` whitelists `tests/fixtures/*.jsonl`) |
| `tests/playscripts/` | seed + ordered-intent fixtures | empty; first fixture lands iter-1 (playscript-runner AC), suite grows iter-2 |

## 2. Reading gradient (what to read before working)

| Scale | Read, in order |
|---|---|
| Trivial — typo, single value, doc fix | `STATUS.md` |
| Normal — bugfix, small feature, one system | this file → `STATUS.md` → `worklog.md` |
| Deep — new system, schema/queue/director touch | + `AGENTS.md` → `docs/BLUEPRINT.md` (ledger rows for the component) → `docs/MVP_SCOPE.md` → `docs/EVENT_SCHEMA.md` |
| Huge — phase gate, architecture, restructure | + `docs/ROADMAP.md` → `docs/VISION.md` → `docs/DECISIONS.md` |
| LLM-track (`bg-*`) | + `docs/TECH_NOTES.md` → `docs/SPECS_BACKLOG.md` |

## 3. Information ownership (anti-drift map)

| Information | Single owner | Everyone else |
|---|---|---|
| Phase-0 scope: entities, systems, actions, tests | `docs/MVP_SCOPE.md` | link, never restate |
| Event fields, enums, header, versioning | `docs/EVENT_SCHEMA.md` ↔ `schemas/event.schema.json` (2-place sync, test-enforced) | examples must match |
| Phases, gates, kill-criteria, donors | `docs/ROADMAP.md` | link |
| What to do next | `docs/TASKS.md` | link |
| Why it all exists, honest limits | `docs/VISION.md` | link |
| Stable design decisions | `docs/DECISIONS.md` | link |
| Core-design research & depth proposals | `docs/CORE_DESIGN_RESEARCH.md` | link; accepted items move to DECISIONS/TASKS, line flips to `absorbed` |
| Cross-reference resolutions & donor combinations per build component | `docs/BLUEPRINT.md` (ledger + laws) + `docs/blueprint/<part>.md` (application) | link, never restate; cite ledger row IDs (e.g. "per RNG-1") |
| Volatile: model stack, hardware, DF pitfalls | `docs/TECH_NOTES.md` | link, expect rot |
| External sources: donors, licenses, phase gating | `docs/REFERENCES.md` (catalog) ↔ `docs/ROADMAP.md` §4 (active shortlist) ↔ per-source deep dives (`docs/REFERENCES_DEEP.md` index + `docs/ref/<source>.md` files, D-026) | link, never restate |
| Agent law, invariants | `AGENTS.md` | `STATUS.md` carries one-liners only |
| Where things are | this file | `README.md` carries a short map |

Duplication rule: if a fact must appear twice (e.g. invariant one-liners), the
copy is a link or a one-line summary — never a second full statement.

## 4. Update rules

- Structure changed (new dir/file/schema) → update §1 in the same iteration.
- New pitfall discovered → `STATUS.md` FAQ (≤20) if durable, `docs/TECH_NOTES.md`
  if it rots.
- This file never carries history or narrative.

## 5. Log hygiene

Runtime logs live in `logs/` (gitignored). Never open one whole: use
`tail -n 50`, `wc -l`, or a `python -c` filter by type/actor/tick. Rendered
chronicles go to `output/` (gitignored).
