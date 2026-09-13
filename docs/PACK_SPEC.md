# PACK_SPEC.md — The Pack Module Contract

> Trigger fired at the phase-6 opening (iter-109 — the `PACK_SPEC` row,
> `docs/SPECS_BACKLOG.md`; the phase-6 / 2nd-setting trigger). Single owner
> of the pack module's contract: what a pack IS, what the lint enforces,
> how packs are authored. The admission law's single sentence lives in
> `docs/DECISIONS.md` D-142; INV-3 owns the vocabulary half
> (`AGENTS.md` §4). The donor design lives in `docs/blueprint/phases.md`
> §6 (PACK-1); the lint mechanics in `core/pack.py` (the loader); the
> authoring rungs in `scripts/pack_scaffold.py` + `scripts/pack_doctor.py`.
> Field-level clauses are born just-in-time — §12 lists what is
> deliberately deferred. ≤600 lines, substance-filtered (`AGENTS.md`
> §6/§6.1). No LLM, no network (INV-4).

## 1. What a pack is

A pack is **a directory of four JSON files that fully declares one
setting**: entities, actions, rules, templates. The engine core is
domain-blind (INV-3: no setting words in `core/` + `sim/` + `brief/`);
every noun, weight, template, and profile a setting needs lives in pack
JSON. The corollary is the universal-core claim this phase tests: **a
second pack requires zero ENGINE changes** (the `pack-3` sketches map
mechanic-for-mechanic onto what exists by design). The phase-6 exit
criterion reads this claim directly: a new T1 reskin without core edits,
authored in ≤1 day (`ROADMAP.md` §2).

The pack is also the **tuning surface**: weights, thresholds, hooks,
templates, entities, actions, profiles, optional arming blocks. The
admission law (D-142) draws the one line this spec enforces:

- A change lands in `core/` **iff it alters WHAT mechanics exist** — a
  new resolver kind, a predicate leaf/compound/comparator, an entropy
  input (hook weight source, channel, trigger), an event-grammar field,
  a systems-table row.
- It lands in pack JSON **iff it tunes HOW declared mechanics behave**.
- The test question: *"must a second pack carry this for the mechanic to
  exist at all?"* — yes is core, no is pack.

Named errors (both directions): "add a mechanic by editing a pack" and
"tune a mechanic by editing core". A phase-6 DSL/macro layer, if ever
built, **compiles INTO pack JSON**, never across the line.

## 2. The four files

Fixed shape today (PACK-1, phase-0 minimum, live in `core/pack.py`):

| File | Declares | Cross-ref owner |
|---|---|---|
| `entities.json` | locations, npcs, items, ambient entities — ids, positions, statuses, pair axes, profiles | — |
| `actions.json` | the verb set: intents, preconditions, resolver wiring, checks, knowledge emissions, crime/seeds wiring | `docs/INTENT_SCHEMA.md` |
| `rules.json` | the behavior blocks (§4 below) | per-block rows in §4 |
| `templates.json` | the chronicle's rendering vocabulary, per event type | `docs/EVENT_SCHEMA.md` §6 |

- **Identity**: each file's `meta` block carries the pack `id` +
  `version`; all four must agree (linted). The playscript binds to
  `id@version` — a script aimed at another pack is refused loudly.
- **`"_"` commentary fields are ignored** wherever references are
  collected — prose rides beside data, never inside it.
- **Load order is `sorted()`, INV-2**: the same pack bytes load in the
  same order in any process. References are **load-then-resolve**: all
  four files load first; name-based references are checked only after
  (no forward-declaration ordering burden on the author).
- **Closed enums everywhere a value belongs to a vocabulary** (channels,
  audiences, fidelities, scopes, comparators, leaf kinds…): the closed
  set's owner is the named core module (§4); the lint enforces
  membership. GeoNames/NE-style open vocabularies never enter pack
  files.
- **A MANIFEST rung is designed, not landed** (§12): today the four
  `meta` blocks ARE the manifest; a sidecar (licenses, credits, entry
  points) grows with the first multi-file growth rung.

## 3. Lint = CI, not taste

`load_pack(dir)` is the single admission gate: **a pack that does not
lint never runs** (a loud `PackError`, never a silent behavior change).
`scripts/pack_doctor.py` is the fix-hint reader (diagnosis + trace +
the health inventory); `scripts/mechanics.py matrix` displays the
loaded wiring; `scripts/mechanics.py blast` reads the boundary for the
blast-radius question (D-142). The lint families, all live in
`core/pack.py`:

- **Orphan references** — exits, positions, carriers, carries, knowers,
  hook payloads, faction members: every name resolves to a declared
  entity.
- **Intent-contract cross-refs** (from iter-2): resolver keys against
  the registry; precondition tests against the closed set; action event
  types against the template vocabulary; check kinds against
  `rules.checks`; knowledge audiences/channels/fidelity/slots against
  their closed sets; transition layers against the template vocabulary.
- **The systems DAG** (`core/scheduler.py`): the systems table's
  reads/writes annotations build the per-tick pass order; a write-write
  ambiguity without before/after hints fails at load.
- **on_action closed keys** (drama-3): the reaction table's
  scope/gate/event/state vocabularies; the one-hop law.
- **Per-block shapes**: every optional block (`urgencies`, `weather`,
  `on_action`, `secrets`, `reflection`, `factions`, `names`, `travel`,
  `worldgen`, …) has its closed key vocabulary and cross-lints
  (`_urgencies` … `_travel` in `core/pack.py`); an absent optional
  block is the primitive silent (the 68a law — the ablation arm's
  foundation, D-141(c)).
- **Pack meta consistency** and the phase coverage of the day.
- **The wiring contract** (iter-107, `tests/test_drift.py`): the
  systems table ⇄ the metrics prefix map agree in four directions —
  phantom systems, claimed prefixes, declared-write coverage, the
  observed corpus vocabulary. A new mechanic grows its drift row in the
  same iteration it lands (D-141(a)).
- **The teleology gate + the live-char crosswalk** (iter-117, pack-ci,
  §5/§6 below): dead action types, orphan entities, empty matrix rows,
  declared-but-unused templates, the AP rows and the price-marker lint —
  the cross-block admission families, running after every block lint.

**Full JSON-Schemas per file are a phase-6 rung, deliberately not
landed** (§12): the lint covers shape today; the event-contract enums
the pack mirrors are cross-checked by `tests/test_smoke.py` against
`schemas/event.schema.json`.

## 4. The rules blocks (module contracts)

Each top-level `rules.json` block names its core owner and its spec.
The block list is the **mechanic inventory** — the D-142 line runs
through it: adding a BLOCK (a new mechanic) is a core landing + its
lint + its drift row in the same iteration; filling an existing block
with setting data is pack work.

| Block | Core owner | Contract owner |
|---|---|---|
| `systems` | `core/scheduler.py` | `docs/blueprint/phase0.md` §2 (SCHED-1) |
| `time` / `states` / `transitions` | `core/clock.py`, `core/states.py` | `docs/EVENT_SCHEMA.md` §4 |
| `relations` / `knowledge` | `core/knowledge.py` | `docs/EVENT_SCHEMA.md` §3, `MVP_SCOPE.md` §5 |
| `crime_watch` | `core/crime.py` | `docs/blueprint/phases.md` §3 |
| `director` (hooks, triggers, arcs, pacing, stagnation, channels) | `core/director.py` | `docs/DIRECTOR_SPEC.md` |
| `urgencies` | `core/urgencies.py` | `docs/blueprint/phases.md` §3 (P2b) |
| `on_action` | `core/onaction.py` | `docs/blueprint/phases.md` §6 |
| `secrets` (leverage registry) | `core/leverage.py` | `docs/blueprint/phases.md` §3 (P3a) |
| `echo` / `traits` / `reflection` | `core/echo.py` / `core/traits.py` / `core/reflection.py` | `docs/LEGEND_SPEC.md` |
| `retrieval` | `core/retrieval.py` | `docs/LEGEND_SPEC.md` §5 |
| `factions` | `core/factions.py` | `docs/blueprint/phases.md` §5 (depth-6) |
| `worldgen` (map, biomes, chronicle, claims, place, states, watershed) | `core/worldgen.py` | `docs/blueprint/phases.md` §5 |
| `travel` (roads, prices) | `core/travel.py` | `docs/blueprint/phases.md` §6 (st-6a) |
| `weather` | `core/weather.py` | `docs/blueprint/phases.md` §5 (weather-1) |
| `names` (phonotactic profiles) | `core/names.py` | `docs/blueprint/phases.md` §5 (name-1) |
| `macro` (the macro clock cadences) | `core/macro.py` | `docs/blueprint/phases.md` §5 (maclock-1) |
| `brief` | `brief/assembler.py` | `docs/BRIEF_SPEC.md` §6 |
| `importance` / `metrics` / `expectations` / `checks` / `scene_detail` / `acquisition` | `core/intent.py`, `core/metrics.py`, `core/detail.py` | the named spec per module |

The optional-block law (68a): a pack declares a mechanic by carrying
its block; the engine primitive runs only when the block exists. The
removable set (measured, D-141(c)): urgencies, weather, on_action,
reflection, secrets, factions. The systems-table rows (fire, relations,
knowledge, states, crime_watch) are interlocked — never independently
removable.

## 5. The teleology gate (admission lint — LIVE since iter-117)

From the UAP audit (`docs/ref/uap_audit.md`): **every event type must
produce a state delta or a hook — dead content otherwise**. The four
checks, enforced in `core/pack.py::_teleology` (after every block
lint — they read the whole validated pack):

- **Dead action types** — an action whose success/failure events carry
  no state_changes, no knowledge, no seeds, no on_action entry. The
  state-change witnesses: the declared blocks (`status_effects`,
  `balance`, `ignition`, any knowledge or hooks branch, the texture
  sub-block), an `on_action` reaction to one of its event types, a
  `metrics.system_of_type` row naming one (the pack's own attribution —
  the goal-verb family's witness), or a resolver in
  `core/resolvers.py::STATE_MUTATING` (the position/carrier/layer
  mutators, declared at the registry's own owner).
- **Orphan entities** — declared entities no event, position read, or
  template ever touches. Touched iff: name-referenced in the pack's
  data (keys and values, `notes`/`_` prose excluded — the reference
  walk), an edged location (the exits graph's position reads), a
  knowledge-holder at an edged location in a pack declaring positional
  audiences, an item the target grammar can address (some action's
  target-noun conjunction passes for it, or its truthy flag is read by
  an actor-side `flagged_accessible` / `ignition.item_flag`).
- **Empty intersection-matrix cells** (`MVP_SCOPE.md` §6) — NPC ×
  action pairs the setting never exercises. The row check: every
  non-player NPC must appear in ≥1 authored surface — an urgency entry
  (the pair itself), a watch-rotation slot, an expectations rule, a
  director hook target, a group membership, a pair relation (either
  side), or a carrier/carries binding. An NPC the dynamic grammar
  reaches but no authored surface wires is dead design space.
- **Declared-but-unused templates** — template vocabulary entries no
  event type renders. The emission witnesses: the action branch
  events, `on_action` keys and reaction events, transition-layer
  events, the `crime_watch` event set, `expectations.event`, the
  `telling` pair, `secrets` events, `reflection.event`,
  `time.macro.event_type`, `weather.event_type` + erosion rows, the
  worldgen chronicle event, the group tier events, the core constants
  (`intent_rejected` always; `status_decayed` iff any states axis
  declares a drift rate), and `importance.story_critical_events` — the
  authored-intent witness (a listed line is deliberately kept tale
  vocabulary, the 68a twin's dormant lines, never dead-by-accident).
  A new emission site that misses the collector fails the committed
  packs loudly — the closure is pinned by the packs that pass it (the
  drift-contract family).

Thematic Law, pillars, and Author Prohibitions enter as **pack
metadata** (INV-3: content, not code), enforced as log asserts at gate
review — never LLM-judged, never core systems. UAP's Grief Architecture
likewise: pack metadata for packs that want it (the `pack-1` grim
row's family).

## 6. The live-char crosswalk (static character checks — LIVE since iter-117)

From `docs/ref/live_char_guide.md` (AP rows → deterministic lint
checks over spine-shaped NPC records), enforced in
`core/pack.py::_live_char` (+ the spine shape in `_entities`, the
atomicity law inside `_predicate_error`):

- **AP-9** — every named NPC carries a want/need tension and a flaw
  rooted in a cause (SPINE shape; the record fields, lint-checked).
  The optional `spine` block on an npc record: `want | need | flaw |
  cause` — all four non-empty strings when present, all-or-nothing (a
  half-declared spine is a broken spine). Absent = silent (the 68a
  pattern; world-2 L2 the crosswalk's first consumer, D-148).
- **AP-8** — every flaw/deep trait carries ≥1 behavior rule that
  consumes it. The consuming surface today: the urgency entry's
  optional `flaw` key (the owner's own rule); both directions linted —
  an entry's flaw must name a declared spine flaw, and every declared
  flaw must be consumed (GHOST without anchors = dead pack data).
  Hook-weight modifiers, on_action reactions and prohibitions join on
  their own triggers.
- **AP-11** — no clone NPCs sharing trigger→action pairs (the
  design-time twin of M4 novelty): two LIVE urgency entries
  (`probability_per_beat` > 0 — a zero-weight slot is a stream
  placeholder that never fires, not a behavior) from different NPCs
  with identical `(intent, requires)` pairs are clones.
- **AP-15** — rule atomicity: one condition per rule; compound
  conditions split. In the predicate grammar: a compound's members
  must be LEAVES — nested compounds are the conditional chains ("if X
  and if Y before that, then Z") the crosswalk refuses. The evaluator
  keeps its recursive grammar; the law is the authoring gate.
- **AP-13** — no contradictory rules (two rules asserting the same
  axis in opposite directions with no gate separating them): two
  ungated on_action reactions to the same event type asserting the
  same `state.prop` with opposite `add` signs cancel out — separate
  them with a gate.
- **AP-1** — pack size budgets (counts of npcs/items/hooks/templates
  within declared bounds; the budget block is metadata the lint
  reads). The optional `rules.json::budget` block:
  `{npcs | items | hooks | templates}`, each `{min, max}` — both
  required, `0 <= min <= max`; absent = silent.
- **Price markers present** on every socially meaningful behavior: an
  immediate observable (a knowledge record or a perceivable state
  token) alongside the deferred hooks — AP-2's design-time half. A
  branch whose hooks seed non-`ambient`-channel deferred consequences
  must carry a knowledge record on that branch or a declared state
  token (`status_effects` / `balance` / `ignition`) — or the behavior
  is socially invisible.

## 7. Tone = data (the darkness dial)

The darkness-as-data law (D-030): **tone is asymmetric pack data** —
trust/relations build slow and break fast, losses are irreversible,
rumor fidelity decay hits per-NPC relations (never a group reputation,
D-006). The dial is pack-declared per axis (build/break rates, decay
curves, irreversibility flags), never a tone lock. A grim/romance line
(flirt→proposition ladder, `consented`/`coerced` as crafted knowledge
records per D-008, jealousy/shame axes) enters **only as pack
vocabulary on the generic core** — never LLM-judged, never a core
system. A future pack consults the cost & consequence laws
(`docs/blueprint/phases.md` §6: the cost law, the failure law, the
corruption law, the decay-branch law, the flashback law, the ambient
law) before inventing its own consequence shapes.

## 8. Affordance derivation (the closed `requires` grammar)

L10: the intent `requires` grammar stays CLOSED. The pack may **derive
action availability from entity props** (`material: wood` +
`has: fire` → ignite available) as pack-lint/table data — never an
open resolver. The live seeds: the flammability + fire_spots +
`spot_available` row (pack-2, iter-29) and the director-side `prop`
leaf (iter-40) that already owns the generalized projection read.
Parser-side verb enumeration rides the parse-2/engine-1 owner gates.
**AFFORD_SPEC stays trigger-gated** (D-096) until a second consumer
arrives.

## 9. Pack authoring (the loop)

The authoring loop's rungs, live since iter-107 (D-141(b)):

1. **`scripts/pack_scaffold.py --out <dir> --name <id>`** — a
   lint-clean copy of the committed tavern pack with the identity
   renamed; `SCAFFOLD.md` rides beside the four files as the editing
   map (the noun surfaces, the verbs, the tools list). Refuses a
   non-empty dir — never clobbers author work. `load_pack` gates the
   result: a scaffold that does not lint is a bug.
2. **Edit the noun surfaces** (SCAFFOLD.md maps them).
3. **`python -m scripts.pack_doctor <dir>` after every edit** — the
   diagnosis + trace + health inventory; (unparsed) degradation, never
   a crash.
4. **Measure**: `scripts/balance_harness.py --script <script> --runs
   50` (the distribution table), `--systems-minus` arms, `scripts/
   mechanics.py matrix|blast|trace|why` (the wiring views).

**The reskin day** (world-2 level 1, the gate's own instrument): the
≤1-day authoring budget measured on the OPEN generic stack (SRD 5.1 /
Open5e, the starter table; speed over distinctiveness). The stoplist
**self-check extension** is the reskin day's own step: the second pack
must exist before its nouns join the INV-3 audit vocabulary (the
stoplist test grows the reskin pack's nouns same-day). A **CREDITS
sidecar** (CC-BY attribution) rides any pack whose data derives from
open sources; a proprietary-universe fan-pack is owner-LOCAL data
outside the repo (the convenience-copy law, D-130's posture tier).

The second pack runs a **different main loop** (the travel class,
D-146): a reskin twin of the tavern proves nothing the tavern did not
— the universal-core claim is tested by the loop change, not the noun
swap.

## 10. Growth rungs (pre-placed at phase 0, land on their own triggers)

- **Per-category file split** (C:DDA, ~111 categories proven): the
  four-file shape splits per category when a pack's single files stop
  being readable. Trigger: measured authoring pain, not anticipation.
- **`abstract` + `copy-from` inheritance** (C:DDA / RimWorld
  `ParentName` / KeeperRL `inherit`): a **single-parent chain** — no
  multi-inheritance, diamonds rejected by design. `abstract: true`
  records are template-only, never instantiated at runtime. **Cycle
  detection at load = CI fail naming the offending id pair** — a
  phase-6 design gate on PACK-1, not an afterthought.
- **Localized name sets** (one symbol per language, the NE
  `NAME_<lang>` shape): the renderer picks; the pack carries them.
- **Append-not-overwrite composition** (the Paradox on_action
  posture): two blocks composing append entries; a collision is a
  load failure, never a silent last-wins.
- **Mode G (worldbuilder) drafts packs offline through the same CI**
  — never into the engine. `roads-1` is the first mode-G pass (the
  generated-exits rung, TASKS' parked row).

## 11. The radiant-template shape (parked authoring pattern)

The step-off-the-road micro-scenario as pack data — the radiant-quest
grammar without the scripting: a schedule + a trigger predicate + a
payoff hook, all three pack-declared over landed primitives (rotations,
hooks, arcs). Named here so a future authoring row finds it; landing it
is a content decision (a real corpus price), owner-gated
(`docs/blueprint/phases.md` §6's parked list).

## 12. Deferred (just-in-time — writing these early = scope creep)

- **Full JSON-Schemas per pack file** (PACK-1's schema rung): lands
  with the first pack whose shape the lint cannot express.
- **The manifest sidecar** (licenses, credits, entry points): lands
  with the first multi-file or multi-source pack — the four `meta`
  blocks carry identity today.
- **The teleology lint rows** (§5) and the **live-char crosswalk rows**
  (§6): LANDED (iter-117, pack-ci) — the enforcement rungs above; the
  reskin pack was the first pack the rows ran against, the tavern and
  the road both green. The 68a twins complete their ablations with the
  stripped family's template lines (a stripped block leaves its
  emission vocabulary dead — the v0.1 twin's own compliance shape).
- **Pack CI runner** (qa-1 mypy / ci-1 GitHub Actions — the standing
  owner-gated rows): `load_pack` is the CI today; the runner automates
  it at the owner's call.
- **The DSL/macro layer**: compiles INTO pack JSON (D-142's guard);
  only after authoring pain is measured across ≥2 packs (L13).
- **Per-category split / copy-from / localized name sets**: their
  triggers in §10.

---

← Up: [`docs/SPECS_BACKLOG.md`](SPECS_BACKLOG.md) · the admission law:
[`docs/DECISIONS.md`](DECISIONS.md) D-142 · the donor design:
[`docs/blueprint/phases.md`](blueprint/phases.md) §6.
