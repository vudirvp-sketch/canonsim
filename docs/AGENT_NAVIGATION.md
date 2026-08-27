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
| `docs/INTENT_SCHEMA.md` | intent contract (the proposal side of the door; trigger-gated, written iter-2) | active |
| `docs/ROADMAP.md` | phases, gates, tracks, donors | active |
| `docs/TASKS.md` | backlog + iteration statuses | active |
| `docs/TECH_NOTES.md` | rotting notes: models, hardware, DF spike | live |
| `docs/DECISIONS.md` | ADR-lite, stable decisions | append-only |
| `docs/SPECS_BACKLOG.md` | just-in-time spec queue | active |
| `docs/CORE_DESIGN_RESEARCH.md` | depth-first core design: reference synthesis, gaps, proposals | absorbed (D-029; P2c accepted — D-033); retired at the phase-0 gate review (`doc-1`) |
| `docs/BLUEPRINT.md` | reference distillation: resolution ledger (12 mechanisms) + cross-cutting laws + build index; entry to `docs/blueprint/` | active (iter-0u); maintained at deep-dive time |
| `docs/blueprint/` | per-part applied synthesis: `phase0.md` (iter-1..6 combined donor designs), `phases.md` (phases 1–6 architecture + cross-cutting) | active; read before the matching iteration/phase |
| `docs/REFERENCES.md` | external source catalog: donors, licenses, phase gating | active (rots — quarterly review) |
| `docs/REFERENCES_DEEP.md` | index + format template + iteration plan for per-ref deep dives; the deep-dive content lives in `docs/ref/` (D-026) | active (rots — quarterly review alongside `doc-2`) |
| `docs/ref/` | per-reference deep dives (one file per source: `neighborly.md`, `mesa.md`, `df_legends_xml.md`, `df_worldgen.md`, `cdda_data_json.md`, `paradox_scripting.md`, `rimworld.md`, `l4d_director.md`, `alien_isolation.md`, `wesnoth_wml.md`, `endless_sky_dsl.md`, `ink.md`, `tracery.md`, `brogue.md`, `dcss.md`, `keeperrl.md`, `generative_agents.md`, `ai_town.md`, `letta.md`, `azgaar_fmg.md`, `natural_earth.md`, `geonames.md`, `libtcod.md`, `rot_js.md`, `red_blob_games.md`, `entt.md`, `bevy.md`, `eventstore.md`, `sqlite_fts5.md`, `duckdb.md`, `sqlite_vec.md`, …); mechanics, take/adapt/inspire/strengths/weaknesses/verdict | active (rots — quarterly review alongside `doc-2`) |
| `schemas/event.schema.json` | machine-readable event contract | synced with `docs/EVENT_SCHEMA.md` |
| `core/` | engine: `schema` (mini-validator, D-032), `rng` (RngBank), `ids`, `clock`, `queue`, `log` (the only canon-write path), `fold` (projection seed + apply; pair map + crime-status conventions), `pack` (loader + lint), `intent` (front-door machinery: preconditions, checks, OCC, knowledge resolution incl. `destination_location`), `resolvers` (the 12-action registry), `transitions` (the generic layer engine — fire as pack data), `knowledge` (iter-3: derived per-knower index, salience, transfer decay, telling reaction, expectation checks), `crime` (iter-3: suspicion reactions + status flip + arrest; iter-4: arrest resolution), `scheduler` (the system-pass DAG), `director` (iter-4: consequence buffer + triggers + narrative entropy + on/off policy; iter-5: `policy_from_rules`), `urgencies` (iter-4: P2b goal ticker — NPC probability rolls through the intent door), `states` (iter-4: fatigue/intoxication/fear decay passes at clock beats; iter-4a: `reset_on_rotation` resets on the watch_change event + per-axis last-change decay baseline), `loop` (tick driver + playscript runner + the reaction cascade + clock-crossing rotations + clock-crossing beats in tick order; iter-4a: the playscript feed is player-driven only; iter-5: public session doors `open`/`run_steps`/`close`) | iter-1..4 landed, iter-4a audited, iter-5 session-factored |
| `sim/systems/` | reserved for periphery systems — anything the canon door must dispatch is kernel mechanics and lives in `core/` (the import-boundary law, D-031/D-037: core never imports sim) | reserved (empty skeleton since iter-0d) |
| `content/tavern_pack/` | the setting as data | v0.1 + iter-3 (all 12 actions executable; expectations + telling + suspicion mapping + watch rotation + pair-relations seeds + movement sighting templates) + iter-4 (director.hooks config, urgencies.entries, arrest.resolution_* fields, status_values +`caught`) + iter-5 (templates.json completed into the tracery grammar: symbols, alternatives, conditionals, tale_gate; display names carry articles); loaded + linted by `core/pack.py` |
| `render/` | the deterministic renderer: `tracery.py` (CHRON-1 engine — grammar + ShufflePool + modifiers + save/restore + conditionals, cosmetic stream only) · `chronicle.py` (chronicle / scene card / entity views / replay report — pure functions of the log) | landed iter-5 |
| `brief/` | frame/brief assembler | skeleton restored iter-0d; reserved for phase 1 |
| `cli/` | the play interface: `main.py` (batch `play`/`chronicle`/`state`/`replay` + the interactive session: `look`, `wait N`, `play`, `directors on|off`, `seed`) · `__main__.py` (`python -m cli` entry) | landed iter-5 |
| `tests/` | test suite | smoke + architecture fitness, T0, minimal T1/T2, core units, loop e2e (iter-1); intent units, the 12 actions e2e, scheduler DAG, transition units, INV-3 stoplist (iter-2); T3 blind-NPC + knowledge/transfer/expectation suites, crime/rotation/OCC suites, iter-3 pack lint (iter-3); director + urgencies + states suites, arrest resolution updated, iter-4 pack lint (iter-4); tracery engine + chronicle + CLI suites incl. T1-chronicle and the directors A/B wiring (iter-5); T4–T8 grow iter-6 |
| `tests/fixtures/` | committed golden fixtures for T0/T1 (log lines, byte-identical run outputs) | `plumbing_smoke_seed42.jsonl` (iter-1; env-pinned — header records the Python version; iter-4 kept byte-identical — the 58-tick scenario crosses no beat) |
| `tests/playscripts/` | seed + ordered-intent fixtures | `plumbing_smoke.json` (iter-1), `day1_theft_and_arson.json` (iter-2 — the §3 walkthrough: steal, take, drop-lamp, fire chain) |
| `docs/DIRECTOR_SPEC.md` | director runtime contract (the trigger fired at iter-4 start — `SPECS_BACKLOG.md` sketch row) | written iter-4 |

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
