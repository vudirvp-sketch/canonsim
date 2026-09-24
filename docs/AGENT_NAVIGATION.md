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
| `LICENSE` | the repo license: AGPL-3.0 (SPDX `AGPL-3.0-only`), the canonical verbatim text; `README.md` §License the pointer, `docs/ROADMAP.md` §4 the donor-policy owner (what the repo TAKES — a separate question) | stable |
| `.github/workflows/ci.yml` | the ci-1 runner: pytest + ruff on push/PR to `main` (`PYTHONHASHSEED=0`, Python 3.12.14 the env pin — the golden byte-compare law, TEST_PLAN §1.1) | live (iter-143, D-176) |
| `docs/VISION.md` | frozen why + honest limits | frozen |
| `docs/MVP_SCOPE.md` | phase-0 tech spec (TavernSim v0) | active |
| `docs/EVENT_SCHEMA.md` | event contract (2-place sync with `schemas/`, test-enforced) | active |
| `docs/INTENT_SCHEMA.md` | intent contract (the proposal side of the door; trigger-gated, written iter-2) | active |
| `docs/ROADMAP.md` | phases, gates, tracks, donors | active |
| `docs/TASKS.md` | backlog: the standing rows (the live owner-gated queue) + the iteration ledger (one line per iteration, the tail capped by the doc guard — done-detail lives in git, the header law) | active |
| `docs/CONTRACTS.md` | pre-implementation contracts for the owner-gated build rows (a contract is the boundary, never the row's spec; sections collapse to pointers when their builds land) | active |
| `docs/TEST_PLAN.md` | the verification stack: T0–T8 + M1–M5 + gate protocol + UAP crosswalk + the schema-bump migration + §8 the testproto LLM-integration protocol + §8.5 the heartbeat ledger + §9 the claim → instrument selection grammar (a routing aid, never a gate) | active |
| `docs/TECH_NOTES.md` | rotting notes: models, hardware, DF spike, measurements, the operator recipes (the live session §14, the corpus-regen protocol §15) | live |
| `docs/DECISIONS.md` | ADR-lite, stable decisions (≤30 compound-ID family rows; collapses fire on the owner's explicit call — D-034/D-185) | append-only |
| `docs/SPECS_BACKLOG.md` | just-in-time spec queue (fired-and-absorbed triggers re-pointed) | active |
| `docs/BLUEPRINT.md` | reference distillation: the resolution ledger + cross-cutting laws + build index; entry to `docs/blueprint/` | active |
| `docs/blueprint/` | per-part applied synthesis: `phase0.md` (the phase-0 donor designs + the §1 type-discipline law), `phases.md` (phases 1–6 architecture + §6 the research archive per its own law — the consult cards + the intake compact blocks + the world-2 records, D-185) | active; read before the matching iteration |
| `docs/REFERENCES.md` | external source catalog: donors, licenses, phase gating | active (rots — quarterly review) |
| `docs/REFERENCES_DEEP.md` | index + format template + iteration plan for the per-ref deep dives; the content lives in `docs/ref/` (D-026) | active (rots — quarterly alongside `doc-2`) |
| `docs/ref/` | per-reference deep dives, one file per source (48 files); mechanics, take/adapt/inspire/strengths/weaknesses/verdict | active (rots — quarterly review) |
| `schemas/event.schema.json` | machine-readable event contract | synced with `docs/EVENT_SCHEMA.md` |
| `core/` | the engine: the event-sourced core (`log`, `queue`, `loop`, `schema`, `fold`, `cursor`), `rng` (RngBank + the seven content-addressed stream families), the knowledge stack (`knowledge`, `echo`, `traits`, `reflection`, `retrieval`), the director stack (`director`, `predicates`, `urgencies`, `states`), the world stack (`worldgen`, `roads`, `travel`, `lod`, `groups`, `factions`, `names`, `weather`, `calendar`, `macro`), the social stack (`crime`, `leverage`, `transitions`, `onaction`), `economy`, `intent` + `resolvers`, `metrics`, `pack` + `packlint/` | stable; stdlib-only (D-012), engine-agnostic (INV-4) |
| `sim/systems/` | reserved for periphery systems — anything the canon door must dispatch is kernel mechanics and lives in `core/` (the import-boundary law, D-031/D-037) | reserved (empty skeleton) |
| `content/tavern_pack/` | the first pack: the theft/arson/rumor scenario | v0.1; armed (worldgen + the macro weather) |
| `content/road_pack/` | the SECOND pack: the travel-loop reskin (world-2 L1; the SRD 5.1 generic stack, `CREDITS.md` the CC-BY-4.0 sidecar) | v0.1 (iter-112, D-149) |
| `content/province_pack/` | the THIRD pack: the original province (world-2 L2 — the Sarrow Vale; authored original content) | v0.1 (iter-118/119, D-153/D-154) |
| `content/grim_pack/` | the FOURTH pack: the grim tavern (pack-1 — the dark line as pure pack data) | v0.1 (iter-148, D-181) |
| `content/pressure_pack/` | the FIFTH pack: the pressure city (pack-4 — the displacement law as pure pack data, zero core change; the first authored non-scaffold pack) | v0.1 (iter-149, D-182) |
| `render/` | the deterministic renderer: `tracery.py` (the CHRON-1 grammar engine, cosmetic stream only) + `chronicle.py` (chronicle / scene card / entity views — pure functions of the log) | active |
| `workbench/` | the Workbench family's Python half (CONTRACTS §5, D-200): `scene_ir.py` the renderer-neutral Visual Scene IR (typed, deterministic, the v5.2 identity closure + status laws) + `scene_build.py` the read model (log → fold → present_in_order → IR — the render/chronicle read-side pattern; periphery per D-046) + `application/` the application-operations skeleton (app spec §32 step 1: `identity` §9 / `artifact` §10 / `directories` §16 / `clock` §17 + the §27 dependency envelope; the application-operations/policy owner per the app spec §2) + `api/` the inbound gateway (app §32 step 4's second half, wb-4/D-201: `contract.py` the §8 envelopes + closed vocabularies, `gateway.py` the socket-free dispatch core — protocol/schema/auth/session translation only (§4.1), `transport.py` the loopback HTTP binding — INV-4's second sanctioned network module, loopback-only) + `application/operations/` the minimal application operations (app §32 step 5, wb-5/D-202: `lifecycles.py` §11's four closed state machines, `execution.py` §12's absolute deadline + cooperative cancellation + the in-memory run registry over the §10 freeze, `models.py` §20's model-discovery half + the digest work kind, `composition.py` §6.1's single wiring owner — the run/model families registered on the gateway, `backend.py` the backend family (wb-6/D-203: the typed `BackendPort` — props/chat/load_model/unload_model, injected at the composition root, never imported (INV-4's two-surface form holds); chat.send the §19.1 layer walk over the run registry + model.load/model.unload §20's loading half — the Model ladder walked on observed outcomes; `model.states` the load-state READ, wb-8's consumer) + `application/settings.py` (wb-9/D-208: the typed launch-settings store over the §16 USER_CONFIG role — the closed validated field set, the atomic schema-tagged persistence, the backend.settings operations with the composition-root-injected preview/liveness) + `platform/` the OS mechanics (wb-8/D-205: `llama_process.py` — the managed llama-server's spawn/command-line-with-sampler-defaults/exit-observation/bounded-graceful-stop, the readiness wait over an INJECTED probe; wb-9/D-208: `model_fetch.py` — INV-4's THIRD sanctioned network surface, the outbound model-assets fetch (HTTP GET downloads only) — the platform row's one network exception, owner-gated) + the wb-10/D-209 import kind (models.py: `model.import` — the LOCAL file copy into the models root with live progress + cooperative cancel, NO network; discover()'s `models_root` field) | active (wb-1, wb-3, wb-4, wb-5, wb-6, wb-8) |
| `workbench/presentation/redot/` | the Workbench family's Redot project (the pinned engine line): project.godot (the application shell the main scene + the canonism_workbench/gateway/url committed default) + code-built scenes/scripts + `themes/` the semantic-token theme (theme@0.2 — wb-10's visual refresh) + `scripts/gateway_client.gd` the typed POST /op client (wb-7/D-204: the live chat circuit's frontend half — the shell dials the GATEWAY only, never llama.cpp; wb-8's per-call `timeout_s` envelope for the minutes-class model.load) + `shell.gd`'s Models surface (wb-8/D-205: discovery + lifecycle states + Load/Unload over the gateway's model.* operations; wb-9/D-208: + the MANAGER — the URL fetch row over run.start model.fetch with the live-progress poll and Cancel = run.cancel; wb-10/D-209: the native-picker PRIMARY flow — Add local models…/Add folder… over FileDialog.use_native_dialog + ACCESS_FILESYSTEM into the model.import run, Open models folder via OS.shell_open on the gateway's models_root answer) + the REAL Settings surface (wb-9/D-208: the llama.cpp launch settings over backend.settings — the typed fields + the collapsed advanced extras + the command preview + the next-spawn note) — the engine binary EXTERNAL (the launcher's folder-aware resolution chain); presentation-only, never canonical state (CONTRACTS §5 D1/D2) | active (wb-2, wb-7, wb-8) |
| `docs/REDOT_ENGINE_INDEX.md` | the Redot/Godot engine reference index — the version firewall (Redot 26.2 LTS pinned, Godot secondary cross-reference only) + the routing map for every engine/API/UI/networking/performance/export question on the Redot surface (wb-9+'s engine-facts owner; the owner's external index admitted iter-225, D-207; the v5.2 docs stay outside — D-024/D-200) | active (rots — the REFERENCES quarterly pass) |
| `brief/` | the phase-1 mediator circuit (LLM-free engine side): `assembler` (the eight-block pipeline), `ledger` (the scene ledger), `validator`, `mediator`, `parser` (mode C), `gbnf` (the snapshot's engine-facing GBNF serialization — pure, PARSER_SPEC §2.1), `scan`, `scene`, `since` (the re-encounter delta) | active |
| `cli/` | the play interface: `main.py` (batch `play`/`chronicle`/`state`/`replay` + the interactive session with the narrator door, `--resume`, `--pack`, `--engine`) + `mediator.py` + `parser.py` + `engine.py` (the runtime engine adapter — the repo's OUTBOUND network module, INV-4's D-193 form; the inbound sibling `workbench/api/transport.py`, D-201) | active |
| `scripts/` | operator tooling (CLI-class, D-046): `mechanics.py` (the introspection CLI), `balance_harness`/`profile_harness`/`worldgen_profile`, `chronicle`/`checkpoint` (the offline builders), `pack_scaffold`/`pack_doctor`, `digest`, `docguard` (the state-layer cap lint, doc-3), `regen_parse_gbnf` (the golden-grammar fixture regen), `visual_proof` (the wb proofs' REDOT_EXE runner — the seam + the shell modes; Xvfb/screenshot artifacts), `workbench_app` (wb-7/D-204: the composition root + loopback serve — the ONE app-gateway assembling the gateway + the operations + the injected llama.cpp backend port; wb-8/D-205: the managed form — the §11.1 lifecycle policy, `_ManagedBackend` spawning llama-server on the first model.load, the graceful stop at shutdown; wb-9/D-208: MANAGED the DEFAULT (`--attached` the observe-only opt-out), the launch-settings store + the exe auto-discovery (runtime/llama.cpp scan) + the injected fetcher + the models-dir bootstrap) + `workbench_launch` (wb-9/D-208 + wb-10/D-209: the ZERO-COMMAND launcher — the runtime bootstrap (workbench/runtime/{models,llama.cpp}/), the gateway child + the Redot child (the folder-aware resolution: --redot-exe exe-OR-folder > the persisted runtime/launcher.json > REDOT_EXE > the Desktop-shaped auto-scan > the native folder picker once), the stdout bind-line readiness watch with the observed bind URL forwarded to the Redot child, the either-exit/Ctrl+C honest two-child shutdown; Workbench.bat/Workbench Setup.bat the repo-root double-click entries), the `df_*` track-B tools | active |
| `tests/` | the suite: architecture fitness (INV-1..5 — the network ban narrowed to the adapter module, iter-177), T0–T8, per-system units, the per-pack e2e suites, the state-layer cap guard (doc-3), the engine-1 packets (`test_gbnf` the mapping + the golden grammar, `test_engine` the adapter contract tests over the stub server) | active |
| `tests/fixtures/` | committed golden fixtures for T0/T1 (log lines, byte-identical run outputs, the deviation corpus) | active |
| `tests/playscripts/` | seed + ordered-intent fixtures (the gate scripts + the per-pack smoke scripts) | active |
| `docs/DIRECTOR_SPEC.md` | director runtime contract (the trigger/weight/option/arc/channel layers) | active |
| `docs/BRIEF_SPEC.md` | brief assembly contract (the eight-block pipeline, budgets, eviction, render format §7 + the narrator call document §7.1) | active |
| `docs/VALIDATION_SPEC.md` | validation contract (the closed proposal document, verdict semantics, OCC, the fact transaction, the regen protocol) | active |
| `docs/PARSER_SPEC.md` | the mode-C parser boundary contract (the external-parser file contract, the grammar snapshot + the GBNF serialization §2.1, the closed reply document, the runtime re-ask ladder §5) | active |
| `docs/PRESENTATION_SPEC.md` | the LLM presentation contract (presentation-1, written iter-178 from the measured results): the model-facing serializer over the stable brief IR — the mapping table, the call budget, the transcript-tail resolution, the Script Tax clause; absorbs st-4 | active |
| `docs/PACK_SPEC.md` | the pack module contract (the four-file directory, the admission law's enforcement half, the lint families, the authoring loop, the growth rungs) | active |
| `docs/TAXONOMY.md` | the bg-2 DF event taxonomy: the 16-target type map + the 120-entry corpus + the measured findings | written bg-2 (D-063) |
| `docs/LEGEND_SPEC.md` | the reflection & compaction contract (reflection-on-recurrence, the reflection event shape, the provenance/stale laws, the pack contract) | active |
| `docs/worldbuild/` | the active worldbuilding surface — the authored-setting model (10 files: `README.md` the index + the terminology fence, `WORLD_KERNEL.md` the world-law owner, the domain owners `RESONANCE.md`/`LIFE_PERSONHOOD.md`/`PEOPLES.md`/`CULTURES_CIVILIZATION.md`, `ANCHOR_REGION.md` the Sarrow Vale laboratory, `WORLD_AUTHORING.md` the doctrine, `WORLD_TESTS.md` the evidence, `WORLD_WORKPLAN.md` the world track's plan; D-186 — a separate track from the engineering backlog, never runtime contracts/pack schemas/build order; the legacy source archive stays outside the repo) | active (the world track) |

## 2. Reading gradient (what to read before working)

| Scale | Read, in order |
|---|---|
| Trivial — typo, single value, doc fix | `STATUS.md` |
| Normal — bugfix, small feature, one system | this file → `STATUS.md` → `worklog.md`; mechanics-level questions (who consumes an event, why a hook waits) → `scripts/mechanics.py` (§5) |
| Deep — new system, schema/queue/director touch | + `AGENTS.md` → `docs/BLUEPRINT.md` (ledger rows for the component) → `docs/MVP_SCOPE.md` → `docs/EVENT_SCHEMA.md` |
| Huge — phase gate, architecture, restructure | + `docs/ROADMAP.md` → `docs/VISION.md` → `docs/DECISIONS.md` |
| Research residue / consult card (a task row or STATUS names an intake/card) | `docs/blueprint/phases.md` §6 — the named card/block only (the archive law at §6's head pins what is durable); the full one-pass records: git at the D-row's commit |
| World-setting authoring (world canon, a region's authored depth, the anchor) | `docs/worldbuild/README.md` (the index + the ownership table + the terminology fence) → the ONE named domain owner, never the whole set; `WORLD_AUTHORING.md` the method, `WORLD_TESTS.md` the tests, `WORLD_WORKPLAN.md` the frontier (A1/A2/A3); the engine side of any claim: the owning spec, never this surface |
| Redot / frontend / engine (any wb row, any `.gd`/scene/theme touch, any engine-API/networking/performance/export question) | `docs/REDOT_ENGINE_INDEX.md` FIRST — the routing map + the version firewall (route to the smallest sufficient section, never read whole) → the owning contract (`docs/CONTRACTS.md` §5) / spec; the official Redot 26.2 class reference the external authority, Godot docs secondary cross-reference only |
| LLM-track (`bg-*`) | + `docs/TECH_NOTES.md` → `docs/SPECS_BACKLOG.md` |

Three standing rules bound how deep the gradient goes (D-198):

- **Context closure**: read until the selected task's dependency closure —
  task → owner → contract → relevant invariants → dependencies → affected
  mechanism → evidence. Stop when further reading would no longer change
  scope, owner, decision, required implementation, or required
  verification; excess reading mixes current/intended/historical/proposal
  state — a failure mode, not thoroughness.
- **Question classes**, separate from depth: OWNER (who decides) /
  CONTRACT (what is promised) / DEPENDENCY (what consumes what) /
  MECHANISM (how it works) / EVIDENCE (what proves it) — classes that
  route into the rows above, each at its own depth; not a second scale.
- **Change-impact gate**: before implementing, check whether the change
  crosses an invariant / schema / contract / subsystem / pack-core / LLM
  boundary. No crossing → stay local. A crossing → expand context past
  the boundary and run the impact arm first (`scripts/mechanics.py`
  `impact` / `blast`, §5); the stronger verification rides TEST_PLAN §9's
  claim packet.

## 3. Information ownership (anti-drift map)

| Information | Single owner | Everyone else |
|---|---|---|
| Phase-0 scope: entities, systems, actions, tests | `docs/MVP_SCOPE.md` | link, never restate |
| Event fields, enums, header, versioning | `docs/EVENT_SCHEMA.md` ↔ `schemas/event.schema.json` (2-place sync, test-enforced) | examples must match |
| Phases, gates, kill-criteria, donors | `docs/ROADMAP.md` | link |
| What to do next | the ORDER: `STATUS.md`'s **Next step** line (re-pinned every iteration; owner-gated / gate-blocked rows are not auto-candidates) · the backlog COMPOSITION: `docs/TASKS.md` (the standing rows the live queue) | link |
| Why it all exists, honest limits | `docs/VISION.md` | link |
| Stable design decisions | `docs/DECISIONS.md` | link |
| Research residue (intake verdicts, consult cards) | `docs/blueprint/phases.md` §6 (the archive law, D-185); the adoptions live in DECISIONS/TASKS. The research→implementation routing schema (intake-37/D-197): durable residue → §6 intake blocks; interventions (probe runners, mutated copies, spike drafts) → `scratch/` (gitignored, never staged — Rule 9's family); architectural adoptions → DECISIONS; tasks → TASKS. No parallel research tree (D-194's refusal) | link; open a card only when a row names it |
| The authored-setting model (world identity/laws, Resonance ontology, lineages, cultures, the anchor's world-level design, the authoring doctrine) | `docs/worldbuild/` (the README's ownership table the sub-map; `WORLD_KERNEL.md` the world-law owner; D-186) | link, never restate; setting facts ride packs as data (INV-3), never prose duplication in specs; world-track asks for engine capability route to `docs/TASKS.md` standing rows; "canon"/"Echo" on that side never mean INV-1's log canon / `core/echo.py`'s read model (the README's terminology fence) |
| Cross-reference resolutions & donor combinations per build component | `docs/BLUEPRINT.md` (ledger + laws) + `docs/blueprint/<part>.md` (application) | link, never restate; cite ledger row IDs (e.g. "per RNG-1") |
| Verification definitions (T-suite, metrics, gate protocol, acceptance laws) | `docs/TEST_PLAN.md` | link; cite §N |
| Volatile: model stack, hardware, DF pitfalls | `docs/TECH_NOTES.md` | link, expect rot |
| External sources: donors, licenses, phase gating | `docs/REFERENCES.md` (catalog) ↔ `docs/ROADMAP.md` §4 (active shortlist) ↔ per-source deep dives (`docs/REFERENCES_DEEP.md` index + `docs/ref/<source>.md` files, D-026) | link, never restate |
| Redot/Godot engine facts: version truth, class routing, networking/remote-access patterns, performance/debugging references | `docs/REDOT_ENGINE_INDEX.md` (the index + decision firewall; the official Redot 26.2 class reference the external authority) | link, never restate |
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

For causal questions prefer the introspection CLI over raw filters:
`scripts/mechanics.py trace --log <log> [--ticks|--tail|--entity|--hook]`
(the unqualified default is capped to the last 720 ticks and the tail note
names the expansion flags — the attention budget), `why --hook TAG
[--at-tick N]` (the hook postmortem) or `why --event ID` (the one-event
postmortem: cause chain + the knowledge wiring join + the cascade), `matrix`
(static wiring; the compact default lists the query vocabulary — `--full`
the whole inventory, `--dag` the systems read/write graph), `impact` (the
agent impact surface — one pack path's derived readers + references, or
the reverse query: which sites reference a name), `blast` (the two-arm
A/B). Derived, never truth (D-118); the tool re-derives answers
through the engine's public API, so its output is INV-2-equal to what the
runtime itself decided.
