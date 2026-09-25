# SSI_TOPOLOGY.md — the ownership/topology map (ssi-3/Phase 2, D-224)

> The Phase 2 deliverable (the owner's 2026-09-26 go-ahead over the
> ssi-1 call): the machine-readable map (owner/reads/writes/emits) +
> the co-change/trajectory audit over git history — the SSI-N018
> evidence base, NEVER a line-count snapshot. The map is a LIVING
> contract: `scripts/topology.py --check` re-derives the mechanical
> columns at HEAD and fails RED on drift (the drift-pin family,
> test_topology.py); `--audit` regenerates everything as JSON.
> Semantic owner: this file. Instrument owner: `scripts/topology.py`.

## 0. Method + scope (read before using the map)

- **Derived** (mechanical, re-derivable at any HEAD): module
  inventory, `lines` (wc), `reads` (stdlib-ast in-repo imports),
  `writes` (`drafts=` EventDraft construction sites + `pushes=` queue
  push sites — INV-1's canon-write participants; `stores:` = data
  filenames appearing as string literals in the module — touchpoints,
  read-or-write), `emits` (`type=`/`kind=` string literals + `dyn`
  when the type flows from pack data at runtime; workbench rows carry
  the gateway operations registered via `name="op.name"` literals).
- **Map refresh iter-250** (ssi-6, Phase 5): the canonical read seam
  `workbench/canonical_read.py` LANDED (D-228) — the ONE workbench
  core-import module; the three read-side consumers (scene_build,
  observatory_read, scene_ir) now read through it (their rows below
  carry the live derivation at this iteration's HEAD); the seam
  joined the watchlist — its `reads` cell (the sanctioned core read
  surface) is now hard-pinned: the surface grows DELIBERATELY, a map
  update in the same iteration, never silently.
- **Authored** (semantic, human): the `owner` column — the module's
  semantic responsibility + its owning spec/decision, sourced from
  NAV §1 and the spec docs.
- **Audit-time facts** (pinned to the recorded audit, NOT re-checked —
  they rot by design and the recipe below is the refresh): the
  `lines` column, §2's co-change figures, §3's trajectories. The
  `--check` pin covers only what must stay true at every HEAD: the
  inventory (every scope module has a row, no stale rows), non-empty
  owners, and the watchlist rows' `reads`+`emits` EXACTLY matching the
  derivation (a seam-relevant change to a strangler target without a
  map update in the same iteration goes RED).
- **Recorded audit**: BASE_COMMIT `08300a022940bd4c80f0893e5cb0cd8e543dc001`
  (2026-09-26), window = the last 150 of 290 commits — iter-90
  (2026-09-10, `5f13f7f`) through HEAD. Refresh recipe:
  `python scripts/topology.py --audit` (full JSON) — paste the changed
  rows' mechanical columns back here in the same iteration.
  **Map refresh iter-247** (ssi-4 step 1): the watchlist module
  `workbench/application/inference.py` (2511 lines) became the
  `workbench/application/inference/` package — the rows below
  carry the live derivation at each split step's HEAD (refreshed at
  iter-248 step 2 and iter-249 step 3 — the split COMPLETE: the pure
  facade + ten owner modules, the ops deriving at operations.py);
  the §3 trajectory
  row stays the PRE-SPLIT record (audit-time, BASE-pinned), the
  watchlist successor is the package facade `__init__.py` (the
  public-surface seam).
- **Independently re-verified** (iter-245, the owner's verification
  session, a fresh clone): every recorded figure reproduces EXACTLY at
  the recorded BASE — the inclusive last-150 window (loop↔pack co=11,
  touches 13/14, lift 9.07, J 0.69, all co-changes iter-90..168), the
  window-start sizes (pack 3990, loop 1024), the state-doc pairs
  (148/144), the line counts, the 82-module inventory, the god-objects'
  last touches (168/107/145/169). Anchoring note for the next verifier:
  the figures bind to BASE_COMMIT and the `git log -150` window is
  INCLUSIVE of iter-90 — a HEAD anchor or an exclusive range shifts
  every count by one (the trap this re-check itself hit first).
- **Instruments' ±1**: the co-change matrix counts via
  `--name-only` (13 loop.py touches), the trajectories via
  `--numstat` (12) — merge-shaped commits list a file without numstat
  digits. Both instruments are named wherever the number matters.
- **Emission caveat (N010-honesty)**: most canon event types are
  DYNAMIC — resolved from pack data (`type=config["reaction_event"]`).
  The `emits` column therefore carries the module's LITERAL vocabulary
  plus the `dyn` marker; the full event-type enumeration lives at its
  standing owners (EVENT_SCHEMA.md + the pack JSONs), never here.
- **Scope**: Python modules under `core/` and `workbench/` (the
  strangler targets are all Python). OUT of the map: the Redot `.gd`
  presentation layer (law owners VISUAL_SYSTEM_UI/FRONTEND_UIUX_LAW),
  and `sim/`/`brief/`/`render/`/`cli/` (NAV §1 owners; no map rows —
  they appear only inside `reads` cells). `__init__.py` rows are
  inventory-closure rows (N002's pattern at file granularity).

## 1. The map (the machine-readable table)

watchlist: core/loop.py, core/director.py, core/worldgen.py, core/intent.py, workbench/application/inference/__init__.py, core/pack.py, workbench/canonical_read.py

| module | owner | lines | reads | writes | emits |
|---|---|---|---|---|---|
| core/__init__.py | the engine package root | 1 | — | — | — |
| core/calendar.py | the sub-year cadence family (world stack, iter-136) | 228 | core/intent.py, core/log.py, core/transitions.py | drafts=1 | dyn |
| core/checkpoint.py | the checkpoint/resume door (D-139, iter-106) | 451 | core/fold.py, core/log.py | stores:index.json | — |
| core/clock.py | the tick clock (engine) | 92 | — | — | — |
| core/crime.py | the crime/reaction family (social stack, BRIEF_SPEC §3.3) | 413 | core/intent.py, core/knowledge.py, core/log.py, core/pack.py, core/resolvers.py, core/rng.py | drafts=4 | dyn |
| core/cursor.py | the run cursor (engine, D-139) | 207 | — | stores:.cursor.json | — |
| core/detail.py | the detail LOD source (world stack) | 157 | core/log.py, core/pack.py, core/rng.py | — | — |
| core/director.py | the beat decision module (DIRECTOR_SPEC) — ssi-5 target | 1419 | core/fold.py, core/ids.py, core/intent.py, core/log.py, core/pack.py, core/predicates.py | — | — |
| core/echo.py | the echo fold (knowledge stack, L6) | 130 | core/knowledge.py, core/pack.py | — | — |
| core/economy.py | the economy substrate (D-179, res-1) | 440 | core/intent.py, core/log.py, core/transitions.py | drafts=1 | dyn |
| core/factions.py | the factions-with-goals family (iter-92, fact-1) | 276 | core/fold.py, core/ids.py, core/intent.py, core/pack.py, core/rng.py, core/worldgen.py | — | — |
| core/fold.py | the projection fold (engine, no-touch floor) | 167 | core/log.py | — | — |
| core/groups.py | the depth-7 groups + group LOD (iter-93, gsim-1) | 311 | core/fold.py, core/intent.py, core/log.py, core/names.py, core/pack.py, core/rng.py | drafts=2 | dyn |
| core/ids.py | the id authority (engine) | 52 | — | — | — |
| core/intent.py | the intent front door (INTENT_SCHEMA) — ssi-5 target | 1080 | core/clock.py, core/fold.py, core/log.py, core/pack.py, core/rng.py, core/roads.py, core/worldgen.py | — | — |
| core/knowledge.py | the knowledge stack core (the epistemic events) | 476 | core/intent.py, core/log.py, core/pack.py, core/rng.py | drafts=2 | dyn |
| core/leverage.py | the leverage family (social stack) | 225 | core/intent.py, core/knowledge.py, core/log.py, core/pack.py | drafts=1 | dyn |
| core/lod.py | the scene LOD three-zones partition (iter-91, lod-1) | 136 | core/fold.py, core/pack.py, core/roads.py, core/worldgen.py | — | — |
| core/log.py | the canon log writer (INV-1, no-touch floor) | 460 | core/ids.py, core/schema.py | — | — |
| core/loop.py | the simulation loop — the kernel's composition root (the omnibus hub; ssi-5's primary target) | 1714 | core/calendar.py, core/checkpoint.py, core/clock.py, core/crime.py, core/cursor.py, core/director.py, core/echo.py, core/economy.py, core/factions.py, core/fold.py, core/groups.py, core/ids.py, core/intent.py, core/knowledge.py, core/leverage.py, core/lod.py, core/log.py, core/macro.py, core/onaction.py, core/pack.py, core/queue.py, core/reflection.py, core/resolvers.py, core/rng.py, core/scheduler.py, core/states.py, core/traits.py, core/transitions.py, core/travel.py, core/urgencies.py, core/weather.py, core/worldgen.py | drafts=3 pushes=8 | completion, follow_up, intent, pass, weather, dyn |
| core/macro.py | the macro-clock family (iter-90, maclock-1) | 205 | core/intent.py, core/log.py, core/transitions.py | drafts=1 | dyn |
| core/metrics.py | the metrics fold (M1/M2, TEST_PLAN) | 537 | core/fold.py, core/log.py | — | — |
| core/names.py | the name generator (D-079, name-1) | 173 | core/log.py, core/pack.py, core/rng.py | — | — |
| core/onaction.py | the on-action reaction family (social stack) | 294 | core/fold.py, core/intent.py, core/log.py, core/pack.py, core/predicates.py, core/transitions.py | drafts=1 | dyn |
| core/pack.py | the pack loader shell over packlint/ (PACK_SPEC, D-175) | 290 | core/packlint/actions.py, core/packlint/actors.py, core/packlint/admission.py, core/packlint/calendar.py, core/packlint/economy.py, core/packlint/entities.py, core/packlint/epistemic.py, core/packlint/helpers.py, core/packlint/readside.py, core/packlint/story.py, core/packlint/systems.py, core/packlint/travel.py, core/packlint/weather.py, core/packlint/worldgen.py | stores:actions.json,entities.json,rules.json,templates.json | — |
| core/packlint/__init__.py | the admission-lint package root (D-175) | 5 | — | — | — |
| core/packlint/actions.py | the actions lint family (PACK_SPEC) | 525 | core/economy.py, core/intent.py, core/packlint/helpers.py, core/packlint/shared.py, core/resolvers.py | stores:actions.json,rules.json,templates.json | — |
| core/packlint/actors.py | the actors lint family (PACK_SPEC) | 578 | core/intent.py, core/packlint/helpers.py, core/packlint/shared.py | stores:actions.json,entities.json,rules.json | — |
| core/packlint/admission.py | the admission law's enforcement half (PACK_SPEC) | 762 | core/economy.py, core/intent.py, core/packlint/helpers.py, core/packlint/shared.py, core/resolvers.py, core/states.py | stores:actions.json,entities.json,rules.json,templates.json | — |
| core/packlint/calendar.py | the calendar lint family (PACK_SPEC) | 198 | core/packlint/helpers.py | stores:rules.json,templates.json | — |
| core/packlint/economy.py | the economy lint family (PACK_SPEC) | 370 | core/economy.py, core/packlint/helpers.py | stores:entities.json,rules.json,templates.json | — |
| core/packlint/entities.py | the entities lint family (PACK_SPEC) | 310 | core/packlint/helpers.py | stores:entities.json,rules.json,templates.json | — |
| core/packlint/epistemic.py | the epistemic lint family (PACK_SPEC) | 268 | core/intent.py, core/packlint/helpers.py, core/retrieval.py | stores:rules.json,templates.json | — |
| core/packlint/helpers.py | the shared lint helpers (PACK_SPEC) | 325 | core/predicates.py, core/worldgen.py | — | — |
| core/packlint/readside.py | the read-side lint family (PACK_SPEC) | 684 | core/detail.py, core/packlint/helpers.py | stores:entities.json,rules.json | — |
| core/packlint/shared.py | the shared literal tokens (PACK_SPEC) | 264 | core/intent.py, core/packlint/helpers.py | stores:actions.json,rules.json | — |
| core/packlint/story.py | the story lint family (PACK_SPEC) | 934 | core/director.py, core/echo.py, core/intent.py, core/leverage.py, core/onaction.py, core/packlint/helpers.py, core/packlint/shared.py, core/predicates.py, core/traits.py | stores:actions.json,entities.json,rules.json,templates.json | — |
| core/packlint/systems.py | the systems lint family (PACK_SPEC) | 632 | core/clock.py, core/knowledge.py, core/packlint/helpers.py, core/packlint/shared.py, core/reflection.py, core/scheduler.py | stores:entities.json,rules.json,templates.json | — |
| core/packlint/travel.py | the travel lint family (PACK_SPEC) | 175 | core/intent.py, core/packlint/helpers.py, core/travel.py, core/worldgen.py | stores:actions.json,entities.json,rules.json | — |
| core/packlint/weather.py | the weather lint family (PACK_SPEC) | 375 | core/packlint/helpers.py, core/weather.py | stores:rules.json,templates.json | — |
| core/packlint/worldgen.py | the worldgen lint family (PACK_SPEC) | 648 | core/intent.py, core/log.py, core/packlint/helpers.py, core/worldgen.py | stores:entities.json,rules.json,templates.json | — |
| core/predicates.py | the director's predicate vocabulary (DIRECTOR_SPEC) | 195 | — | — | — |
| core/queue.py | the band-ordered event queue (engine, the queue key) | 84 | — | — | — |
| core/reflection.py | the reflection fold (LEGEND_SPEC) | 229 | core/intent.py, core/knowledge.py, core/log.py, core/pack.py | drafts=1 | dyn |
| core/resolvers.py | the action resolver registry (iter-2, D-035) | 762 | core/detail.py, core/economy.py, core/intent.py, core/log.py, core/pack.py, core/rng.py, core/transitions.py | — | — |
| core/retrieval.py | the read-side retrieval fold (D-088) | 596 | core/log.py, core/pack.py, core/reflection.py | — | — |
| core/rng.py | the RngBank entropy authority (INV-2, no-touch floor) | 396 | — | — | — |
| core/roads.py | the generated-exits overlay (D-178, roads-1) | 60 | core/pack.py, core/worldgen.py | — | — |
| core/scheduler.py | the cadence scheduler (iter-90) | 122 | — | — | — |
| core/schema.py | the write-time event validation (no-touch floor) | 182 | — | — | — |
| core/states.py | the director's axis states (DIRECTOR_SPEC) | 226 | core/fold.py, core/intent.py, core/log.py, core/pack.py, core/transitions.py | drafts=1 | dyn |
| core/traits.py | the traits fold (knowledge stack) | 175 | core/knowledge.py, core/log.py, core/pack.py | — | — |
| core/transitions.py | the generic transition engine (iter-2) | 365 | core/intent.py, core/log.py, core/pack.py, core/rng.py | drafts=4 | dyn |
| core/travel.py | the movement twin (iter-97, st-6a) | 257 | core/intent.py, core/worldgen.py | — | — |
| core/urgencies.py | the urgency family (director stack) | 188 | core/fold.py, core/ids.py, core/intent.py, core/pack.py, core/rng.py, core/worldgen.py | — | — |
| core/weather.py | the ambient weather family (iter-98, weather-1) | 431 | core/calendar.py, core/intent.py, core/log.py, core/rng.py, core/transitions.py | drafts=2 | dyn |
| core/worldgen.py | the world generator (world stack) — ssi-5 target | 1388 | core/detail.py, core/intent.py, core/log.py, core/rng.py, core/transitions.py | drafts=2 | dyn |
| workbench/__init__.py | the Workbench package root | 4 | — | — | — |
| workbench/api/__init__.py | the api package root | 41 | — | — | — |
| workbench/api/contract.py | the gateway envelopes + closed vocabularies (wb-4, D-201) | 529 | workbench/application/identity.py | — | — |
| workbench/api/gateway.py | the socket-free dispatch core (wb-4, D-201) | 922 | workbench/api/contract.py, workbench/application/clock.py, workbench/application/identity.py | — | app.status, session.attach, session.create, session.detach, session.events, session.get |
| workbench/api/transport.py | the loopback HTTP binding (INV-4's second surface) | 223 | workbench/api/gateway.py | — | — |
| workbench/application/__init__.py | the application package root (app spec) | 59 | — | — | — |
| workbench/application/artifact.py | the artifact store (app §10) | 319 | workbench/application/identity.py | — | — |
| workbench/application/clock.py | the AppClock (app §17) | 108 | — | — | — |
| workbench/application/directories.py | the §16 directory roles | 189 | — | — | — |
| workbench/application/identity.py | the install identity (app §9) | 263 | — | — | — |
| workbench/application/inference/__init__.py | the inference-control facade — the PURE re-export shell, the byte-stable public import surface (LLAMA_CPP_INFERENCE_CONTROL_LAW, D-219/D-220; ssi-4 COMPLETE iter-247/248/249) | 176 | workbench/application/inference/chain.py, workbench/application/inference/compiled.py, workbench/application/inference/library.py, workbench/application/inference/migration.py, workbench/application/inference/operations.py, workbench/application/inference/presets.py, workbench/application/inference/profile.py, workbench/application/inference/relations.py, workbench/application/inference/resolver.py, workbench/application/inference/store.py | — | — |
| workbench/application/inference/chain.py | the sampler chain membership/order semantics (the LAW §11) | 57 | workbench/application/inference/library.py | — | — |
| workbench/application/inference/compiled.py | the compiled semantic document — the platform seam's input vocabulary (the LAW §13) | 39 | workbench/application/inference/library.py, workbench/application/inference/profile.py | — | — |
| workbench/application/inference/library.py | the semantic-control model + the 85-control library data (the LAW §3 atom, the form vocabularies, the indexes) | 1118 | — | — | — |
| workbench/application/inference/migration.py | the one-way settings/1 → settings/2 + inference/1 migration (the composition boot) | 159 | workbench/application/inference/library.py, workbench/application/inference/profile.py, workbench/application/inference/store.py | — | — |
| workbench/application/inference/operations.py | the inference gateway family + the chat BASE-temperature provider (the LAW §17, app §6.1 wiring) | 168 | workbench/api/gateway.py, workbench/application/inference/library.py, workbench/application/inference/resolver.py, workbench/application/inference/store.py | — | inference.read, inference.update |
| workbench/application/inference/presets.py | the four §30 transparent presets (the LAW §14) | 116 | — | — | — |
| workbench/application/inference/profile.py | the typed profile document + its acceptance laws (the LAW §6 input, app §19.1 BASE layer) | 252 | workbench/application/inference/chain.py, workbench/application/inference/library.py | — | — |
| workbench/application/inference/relations.py | the typed relation data (the LAW §12) | 174 | — | — | — |
| workbench/application/inference/resolver.py | the effective-state resolver (the LAW §6/§8: STATES + resolve + the chain-item states) | 269 | workbench/application/inference/chain.py, workbench/application/inference/library.py, workbench/application/inference/presets.py, workbench/application/inference/profile.py, workbench/application/inference/relations.py | — | — |
| workbench/application/inference/store.py | the inference-profile store + the SCHEMA tag (the persistence owner, app §16/§19.1) | 245 | workbench/application/inference/chain.py, workbench/application/inference/library.py, workbench/application/inference/profile.py | — | — |
| workbench/application/operations/__init__.py | the operations package root (wb-5) | 34 | — | — | — |
| workbench/application/operations/backend.py | the backend family: chat.send + model.load/unload/states (wb-6, D-203) | 952 | workbench/api/gateway.py, workbench/application/operations/execution.py, workbench/application/operations/lifecycles.py, workbench/application/operations/models.py | — | chat.send, model.load, model.states, model.unload |
| workbench/application/operations/composition.py | the single wiring owner (app §6.1, wb-5/D-202) | 527 | workbench/api/gateway.py, workbench/application/clock.py, workbench/application/inference/__init__.py, workbench/application/operations/backend.py, workbench/application/operations/execution.py, workbench/application/operations/models.py, workbench/application/operations/observatory.py, workbench/application/settings.py | — | model.digest, model.inspect, model.list, run.cancel, run.get, run.start |
| workbench/application/operations/execution.py | the deadline + cancellation + run registry (app §12) | 702 | workbench/application/artifact.py, workbench/application/clock.py, workbench/application/identity.py, workbench/application/operations/lifecycles.py | — | — |
| workbench/application/operations/lifecycles.py | the four closed state machines (app §11) | 247 | — | — | — |
| workbench/application/operations/models.py | the model discovery + fetch/import (wb-9/wb-10, D-208/D-209) | 627 | workbench/api/gateway.py, workbench/application/operations/execution.py | — | model.fetch, model.import |
| workbench/application/operations/observatory.py | the Observatory ops layer (obs-2, D-217) | 119 | workbench/api/gateway.py, workbench/observatory_read.py | — | observatory.read, observatory.runs |
| workbench/application/settings.py | the launch-settings store (wb-9, D-208) | 385 | workbench/api/gateway.py | — | backend.settings, backend.settings.update |
| workbench/canonical_read.py | the canonical read seam — the ONE workbench core-import module, the narrow read API (Phase 5/ssi-6, D-228; INV-4's sanctioned-module pattern at the core-read boundary) | 59 | core/fold.py, core/log.py, core/pack.py, core/rng.py | — | — |
| workbench/observatory_read.py | the Observatory read model (obs-2, D-217) — reads through the canonical seam | 263 | workbench/canonical_read.py | — | — |
| workbench/platform/__init__.py | the platform package root | 8 | — | — | — |
| workbench/platform/llama_process.py | the managed llama-server process (wb-8, D-205) | 921 | — | — | — |
| workbench/platform/model_fetch.py | the outbound model-assets fetch (INV-4's third surface, D-208) | 278 | — | — | — |
| workbench/scene_build.py | the scene read model (wb-1) — reads through the canonical seam | 210 | workbench/canonical_read.py, workbench/scene_ir.py | stores:event.schema.json | — |
| workbench/scene_ir.py | the Visual Scene IR (CONTRACTS §5) — reads through the canonical seam | 256 | workbench/canonical_read.py | — | — |

## 2. The co-change audit (the last 150 commits)

Window facts: 150 of 290 commits, iter-90 (2026-09-10) → HEAD
(2026-09-26). The state-doc pairs (STATUS.md↔worklog.md 148×,
STATUS↔TASKS 144×, DECISIONS↔… 92×, lift ≈ 1.0) are the every-iteration
protocol rhythm, not coupling — excluded from the code ranking. Every
code pair with ≥ 5 co-changes in the window (the complete list, 8
pairs):

| pair | co | a | b | lift | jaccard |
|---|---|---|---|---|---|
| core/loop.py ↔ core/pack.py | 11 | 13 | 14 | 9.07 | 0.69 |
| tests/test_operations.py ↔ workbench/application/operations/composition.py | 6 | 6 | 6 | 25.00 | 1.00 |
| core/intent.py ↔ core/loop.py | 5 | 6 | 13 | 9.62 | 0.36 |
| scripts/workbench_app.py ↔ tests/test_shell_contract.py | 5 | 6 | 12 | 10.42 | 0.39 |
| scripts/workbench_app.py ↔ tests/test_workbench_app.py | 5 | 6 | 6 | 20.83 | 0.71 |
| tests/test_accountgloss.py ↔ tests/test_freightvol.py | 5 | 5 | 7 | 21.43 | 0.71 |
| tests/test_campaccount.py ↔ tests/test_debt1.py | 5 | 5 | 7 | 21.43 | 0.71 |
| tests/test_shell_contract.py ↔ tests/test_workbench_app.py | 5 | 12 | 6 | 10.42 | 0.39 |

**The loop.py↔pack.py pair — the temporal finding (N018's whole
point)**: the pair IS the repo's #1 code co-change (11 co-changes of
the 16 commits touching either; Jaccard 0.69; lift 9.07 — the
numerical hypothesis CONFIRMED). But ALL 11 co-change commits fall in
iter-90..168 (2026-09-10..21) — the add-a-system feature era (macro
clock, LOD, factions, groups, names, travel, weather, calendar,
roads, economy) when every new system landed in loop+pack together.
Since iter-168 neither file has been touched (≈ 75 iterations of
silence), and pack.py was subsequently DECOMPOSED 3990 → 290 lines
via the core/packlint/ split (D-175's rider) — the coupling the
external analysis measured is HISTORICAL, largely dissolved by the
split, and DORMANT at HEAD. The remaining loop.py partner (intent.py,
5×, same era) tells the same story.

## 3. The trajectories (the watchlist; numstat instrument)

| file | HEAD | @window start | net window | introduced | touches@window | touches@full | last touch |
|---|---|---|---|---|---|---|---|
| core/loop.py | 1714 | 1024 | +690 | 1714 | 12 | 35 | iter-168 (2026-09-21) |
| core/director.py | 1419 | 1272 | +147 | 1419 | 2 | 14 | iter-107 (2026-09-12) |
| core/worldgen.py | 1388 | 1183 | +205 | 1388 | 1 | 6 | iter-145 (2026-09-19) |
| core/intent.py | 1080 | 949 | +131 | 1080 | 6 | 17 | iter-169 (2026-09-21) |
| workbench/application/inference.py | 2511 | 0 | +2511 | 2511 | 2 | 2 | iter-240 (2026-09-25) — became the inference/ package at iter-247 (ssi-4 step 1); the row is the pre-split audit record |
| core/pack.py | 290 | 3990 | −3700 | 290 | 13 | 59 | iter-168 (2026-09-21) |

Readings: loop.py grew +67% in the window but ALL of it before
iter-168 — the core god-objects are large and FROZEN in practice (1–6
window touches each, none in ~75 iterations). inference.py was BORN at
2511 lines inside two iterations (inf-1/inf-2, 2026-09-25) — the
newest, largest, most recently-touched module in the repo. pack.py is
the completed strangler precedent: 3990 → 290 over the packlint
family, zero functional change, the method Phase 4 would reuse.

## 4. The hypotheses verdict (the ssi-3 re-verification)

| hypothesis (the external analysis) | the audit's finding | verdict |
|---|---|---|
| core/loop.py ~1714 lines | 1714 exactly | CONFIRMED |
| core/director.py ~1419 | 1419 exactly | CONFIRMED |
| core/worldgen.py ~1388 | 1388 exactly | CONFIRMED |
| core/intent.py ~1080 | 1080 exactly | CONFIRMED |
| workbench/application/inference.py ~2511 | 2511 exactly | CONFIRMED |
| loop.py↔pack.py co-change over the last 150 commits | the #1 code pair: 11 co-changes, lift 9.07, J 0.69 — but all in iter-90..168; dormant since; pack decomposed | CONFIRMED numerically / REFUTED as live coupling |
| (implied) the core god-objects actively co-change now | the four god-objects + pack untouched since iter-107..169 (75+ iterations); core/'s post-iter-169 touches are exactly three gloss/lint commits (iter-191/199 the economy-gloss constants, iter-200 the packlint rename guard) — none a god-object (the iter-245 verification's precision: the directory-level claim was loose, the verdict unchanged); the window's active pairs are workbench/tests (composition↔test_operations 6×, J 1.00) | REFUTED |
| (implied) inference.py is the actively-growing hotspot | born 2511 lines in 2 iterations, the newest surface, single in-repo dep (gateway) | CONFIRMED |

The N018 conclusion: the line-count snapshot was accurate but its
implied risk profile was stale — the core god-objects are big and
DORMANT; the live growth front is workbench, and Phase 3's target
(inference.py) is exactly where the audit says the active risk is.

## 5. What the map means for the phases (the consumers)

- **ssi-4 (Phase 3, the inference split) — COMPLETE iter-247/248/
  249, the phase CLOSED** (the owner's go-ahead): 2511 lines, born in two
  iterations, single in-repo dependency (the gateway's op
  registration), and the LAW's own three-layer split
  (raw-capability/semantic-control/UI-projection,
  LLAMA_CPP_INFERENCE_CONTROL_LAW §2) already names the semantic
  owners the split follows — never an external template. The split
  follows the packlint precedent (the proven decomposition method);
  the public import surface and the gateway operations are
  byte-stable, the watchlist successor is the package facade (the
  DATA half out at step 1, the RESOLUTION half at step 2, the
  PERSISTENCE/OPERATIONS half + the pure re-export facade at step 3
  — 2511 lines became 10 owner modules + a 176-line facade, the ops
  now deriving at their true owner operations.py).
- **ssi-5 (Phase 4, the core strangler) — scope SHRINKS on this
  evidence** (the pre-registered rule: refuted coupling = shrink):
  the four god-objects' sizes stand, but their live coupling is
  refuted and core/ is dormant — the urgency is low, the phase stays
  owner-gated, and when it opens it follows the packlint precedent
  (the proven decomposition method) with loop.py's 32-module read set
  (§1) as the seam map. The public-interface freeze (D-221) and the
  R2/R3 + PCC stepping stand unchanged.
- **ssi-6 (Phase 5, the canonical read seam) — CLOSED iter-250**
  (the owner's «продолжай работу» go-ahead over the confirmed Phase 3
  closure): the seam LANDED as `workbench/canonical_read.py` — the
  ONE workbench core-import module, a pure re-export shell over the
  10-name canonical read surface (log: read_log/validate_header/
  EventRecord/LogError; fold: fold/initial_projection/
  present_in_order; pack: load_pack/PackError; rng: stable_hash —
  D-024's one-owner law: the edge only, never a second copy). The
  map's candidate set migrated: scene_build.py (fold/log/pack/rng),
  observatory_read.py (log), scene_ir.py (rng) now read through it —
  zero behavior change, the public surfaces byte-stable. The law is
  executable twice over: tests/test_architecture.py (a core import
  anywhere else in workbench/ goes RED) + the seam's watchlist row
  (its reads cell — the sanctioned surface — hard-pinned by
  --check). scripts/ and render/ keep their direct core imports by
  design (the periphery, D-046 — the seam bounds the workbench app
  layer only).
- **The map's own law**: `python scripts/topology.py --check` runs in
  the suite (test_topology.py's drift pin); any iteration that adds a
  scope module, or changes a watchlist module's imports/emits,
  updates the map rows in the same iteration via `--audit`.
