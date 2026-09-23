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
| `brief/` | the phase-1 mediator circuit (LLM-free engine side): `assembler` (the eight-block pipeline), `ledger` (the scene ledger), `validator`, `mediator`, `parser` (mode C), `gbnf` (the snapshot's engine-facing GBNF serialization — pure, PARSER_SPEC §2.1), `scan`, `scene`, `since` (the re-encounter delta) | active |
| `cli/` | the play interface: `main.py` (batch `play`/`chronicle`/`state`/`replay` + the interactive session with the narrator door, `--resume`, `--pack`, `--engine`) + `mediator.py` + `parser.py` + `engine.py` (the runtime engine adapter — the repo's ONE network module, INV-4's explicit form, D-192/D-193) | active |
| `scripts/` | operator tooling (CLI-class, D-046): `mechanics.py` (the introspection CLI), `balance_harness`/`profile_harness`/`worldgen_profile`, `chronicle`/`checkpoint` (the offline builders), `pack_scaffold`/`pack_doctor`, `digest`, `docguard` (the state-layer cap lint, doc-3), `regen_parse_gbnf` (the golden-grammar fixture regen), the `df_*` track-B tools | active |
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
