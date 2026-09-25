# FRONTEND_UIUX_LAW.md — The Workbench Frontend UI/UX Law

> The owner's 2026-09-25 hand-off: the external *CanonSim Workbench —
> Ultimate Frontend / UI / UX / Visual Architecture* consolidated pack
> (the tmpfiles delivery, 60 sections) + the «начать работать в этом
> направлении» direction call. Per the D-024/D-200 law the external
> brief is NEVER vendored — the original stays with the owner; THIS
> file is the repo-side binding distillation. Admission: iter-233,
> D-214.
>
> **Routing law:** every frontend question about interaction
> architecture, information architecture, selection/context/focus,
> epistemic grammar, Observatory, accessibility, localization,
> responsive/DPI, or verification routes HERE first. The VISUAL subset
> (token taxonomy, color law, per-surface state matrix, transplantation)
> stays with `docs/VISUAL_SYSTEM_UI.md` (D-211); engine facts with
> `docs/REDOT_ENGINE_INDEX.md` (D-207); application/runtime contracts
> (operations, lifecycles, identity, deadlines, streaming, persistence,
> inference policy) with `docs/WORKBENCH_APP_LAW.md`; Observatory
> analytical semantics (planes, query families, run identity, the
> promotion gate) with `docs/OBSERVATORY_LAW.md`; world presentation /
> Scene IR / assets / LOD / degradation with
> `docs/WORLD_PRESENTATION_LAW.md` (all D-218, iter-237 — the corpus
> re-homing). The v5.2 external specs stay outside the repo; the §-map:
> app spec §N → WORKBENCH_APP_LAW §N 1:1, Observatory §N →
> OBSERVATORY_LAW §N 1:1, frontend spec §46/§52 → THIS LAW §25. Where
> this law and an external copy disagree, THIS file + the app spec's
> evidence law (WORKBENCH_APP_LAW §19.1) win.

## 0. Executive doctrine

The Workbench is an **instrument for truthful interaction with
deterministic world state and evidence** — not a generic dashboard,
not a generic dark AI client, not a collection of independent screens.

The optimization order:

```text
semantic truthfulness
→ low cognitive load
→ fast task completion
→ inspectability
→ reversible navigation where appropriate
→ explicit evidence / provenance
→ deterministic rendering
→ bounded complexity
→ accessibility
→ agent maintainability
```

The central UX invariant (every major surface walks this loop):

```text
QUESTION → SCOPE → FOCUS → PRIMARY VIEW → CONTEXT
→ INSPECT / COMPARE / DRILL → EVIDENCE → PROVENANCE
→ NEXT DISCRIMINATOR
```

The central implementation invariant:

```text
canonical/backend state → typed read model
→ ViewModel only where projection logic is needed
→ UI / Visual Scene IR → Redot presentation
```

Never: `UI → hidden transport → semantic authority`.
Never: `visual appearance → implied truth`.

The diagnosis this law exists for: the planning documents were
stronger at "what the UI must not falsely imply" than at "how a human
investigates a complex world efficiently". The missing middle layer —
the ANALYTICAL INTERACTION GRAMMAR between the semantic/backend
contract and the visual/UI system — is what this law owns:

```text
SEMANTIC / BACKEND CONTRACT
    ↓ ANALYTICAL INTERACTION GRAMMAR   ← this law
VISUAL / UI SYSTEM                    ← VISUAL_SYSTEM_UI.md
REDOT IMPLEMENTATION                  ← REDOT_ENGINE_INDEX.md
RUNTIME + TASK PROOF                  ← §22 here
```

## 1. The law chain (specification integrity)

Every approved requirement survives through:

```text
FULL NORMATIVE SPEC → ACTIVE WORKING LAW
→ IMPLEMENTATION CONTRACT → TEST / PROOF
```

No requirement silently disappears while documents are shortened. A
compact working law (e.g. VISUAL_SYSTEM_UI.md) is a routing/index
layer that EXPLICITLY references the binding companion requirements —
never an accidental lossy compression of the approved law
(VISUAL_SYSTEM_UI §11 is the repair instance; the drift it closed:
accessibility, keyboard/focus, reduced motion, responsive/DPI,
localization/Cyrillic were materially missing from the short law).

## 2. Information architecture

```text
SURFACE = user intent / work context
VIEW    = representation of information
```

Conceptual grouping (an IA, not a mandatory literal menu):

```text
WORK       Chat · Simulation · Observatory
RESOURCES  Models · Prompts · History
SYSTEM     Runs · Diagnostics · Settings
```

Invariants: intent surfaces stay few; representations live INSIDE
the relevant surface; a nav rail is a navigation instrument, never a
feature directory — before surface count expands, define grouping,
hierarchy, selection, focus, keyboard traversal, restoration, and
overflow/collapse behavior (a flat catalog of 12–20 equally prominent
destinations is the failure mode).

## 3. The analytical workspace grammar

Conceptual regions — semantic ROLES, not mandatory permanent panels;
collapsible/resizable per task and viewport:

```text
CONTEXT · QUERY · SCOPE/FILTER · PRIMARY VIEW
· INSPECTOR · EVIDENCE / PROVENANCE
```

- **Context** answers: what am I looking at / under which run / which
  seed / which time window / which observation profile / against
  which result revision (example:
  `province · run_0042 · seed 42 · tick 1180–1540 · CANON VIEW`).
- **Query** represents the research question: question, class,
  target, scope, observer/profile, comparison arm, filters.
- **Primary view**: exactly ONE representation holds primary visual
  attention (timeline / table / diff / profile / map / graph) — never
  show every representation simultaneously merely because the backend
  can produce it.
- **Inspector**: identity, state, history, relations, contributors,
  consumers, downstream effects, provenance — with evidence,
  disposition, scope, uncertainty, source, analysis revision, and
  next discriminator in the evidence region.

## 4. The shared selection model

Selection is a first-class APPLICATION concept, not widget-local
state. A selected semantic identity propagates across representations
(timeline highlights E → graph highlights dependencies → inspector
opens E → evidence scopes to E) and stays stable across view
switches, semantic zoom, drill-down, compare, and filter changes —
unless the identity genuinely leaves the active scope.
Cross-highlighting references canonical/typed read-model identity —
NEVER display strings, row indices, or ad-hoc local IDs.

## 5. Focus + context; semantic zoom

The central Observatory primitive is `FOCUS + CONTEXT`, not geometric
zoom alone (FOCUS: event 714; CONTEXT: ±30 events, same actor, same
object, same relation axis, same causal slice). Changing context
never loses the focal identity. Semantic zoom levels
(event → cluster → regime → world) change aggregation, labels, and
metadata density — never the underlying identities or meaning.

## 6. Compare mode

BASE vs PERTURBED analysis uses ONE temporal coordinate system with
TWO experiment arms — never two independent pages. Both arms share:
time axis, semantic identity space, selection, scale where
meaningful, navigation position, comparison scope. The vocabulary:

```text
BASE · PERTURBED · COMMON PREFIX · FIRST DIVERGENCE
· CHANGED CONSEQUENCES · PERSISTENCE
```

Difference markers anchor to semantic identity AND time — not merely
color.

## 7. Timeline

The timeline is a first-class Observatory representation. Semantic
lanes: actors, events, relations, objects, resources, institutions,
knowledge, regimes, divergence, observer access. Derived markers:
FIRST DIVERGENCE, PERSISTENCE INTERVAL, REGIME TRANSITION,
RE-ENCOUNTER, STATE EFFECT. Interactions: select, range, scrub,
focus, semantic zoom, compare alignment, jump to divergence, jump to
source evidence.

## 8. Graph policy

Graph is a contextual MICROSCOPE, not the default world
representation. Prefer timeline / table / inspector / diff before
unrestricted graph; a graph answers explicit questions (dependency
neighborhood, relation neighborhood, object flow, institutional
links). Always bound: node count, edge count, neighborhood depth,
visible labels, layout scope. Local neighborhoods over hairballs.

## 9. The evidence ladder

A reusable UI component, not prose:

```text
READ DEPENDENCY → BRANCH INFLUENCE → STATE EFFECT
→ DOWNSTREAM DIVERGENCE → PERSISTENT CAUSAL DEPENDENCY
```

with the claim model:

```text
CLAIM: X contributed to Y · DISPOSITION: PARTIALLY_CONFIRMED
SCOPE: run=42..60 · NEXT DISCRIMINATOR: matched counterfactual
```

A graph edge, prose statement, or `cause_id` alone must never
visually imply a causal conclusion.

## 10. Epistemic grammar

```text
UNKNOWN ≠ NOT OBSERVED ≠ NO MATCH ≠ NO EVIDENCE ≠ ABSENT
≠ OUT OF SCOPE ≠ FAILED ≠ STALE
```

Semantic states: `KNOWN · SUPPORTED · PARTIAL · AMBIGUOUS ·
UNRESOLVED · UNKNOWN · OUT_OF_SCOPE · STALE` — each carried by at
least TWO of {label, icon, shape, pattern, line treatment, position,
textual explanation}; color is supportive, never authoritative.

Orthogonal dimensions, never collapsed:

```text
AUTHORITY: CANONICAL | OBSERVED | DERIVED | UNKNOWN
CLAIM:     FACT | INFERENCE | HYPOTHESIS | PROPOSAL | UNKNOWN
```

The UI must render `OBSERVED + INFERENCE` and `CANONICAL + FACT`
without semantic collision — one overloaded status color/label is
the bug.

## 11. Query lifecycle; empty semantics

```text
DRAFT → VALIDATED → ADMITTED → RUNNING → PARTIAL → COMPLETE
      → FAILED → CANCELED → STALE
```

Stable identifiers where relevant: QUERY ID, RUN ID, RESULT
REVISION. The user always knows whether they view live, previous,
partial, stale, or recomputed results.

Empty outcomes NEVER collapse into one generic empty card:

```text
NO DATA · NO MATCH · NO EVIDENCE · UNKNOWN
· OUT OF SCOPE · BLOCKED · PARTIAL
```

`NO EVIDENCE` must not render as `NO RELATION`; `OUT OF SCOPE` must
not render as `NOT FOUND`.

### 11.1 Dense data surfaces, forms and search

Density is task-dependent: reading low/medium · authoring/chat medium ·
data grids/diagnostics high + strong hierarchy · expert configuration
high + progressive disclosure. Tables are for row/column comparison,
not arbitrary layout. Dense data supports `find → compare →
inspect/edit → act` and, where relevant:

```text
stable columns · numeric alignment · row grouping · sticky/frozen headers
sorting/filtering near the data · visible selection · keyboard semantics
accessible headers · stable semantic identity · virtualization
```

Forms follow user reasoning, not database schema: `identity/target →
essential choice → dependent choices → optional detail → advanced →
validation → commit`; preserve recoverable input; keep `invalid ≠
incomplete ≠ unavailable` distinct. Search supports partial knowledge,
preserved query state and an explicit result scope. (The Observatory
event table, History and Diagnostics are the dense-data consumers;
obs-2's table is the first landed instance.)

## 12. Drill-down; persistent workspace

Predictable analytical path: world profile → regime → time window →
event → actor/object/relation → causal slice → source event → exact
evidence. Navigation history is SEMANTIC (breadcrumbs over entities
and scopes, never `Screen 1 > Screen 2`); Back / Forward / return to
current scope / restore prior focus all hold. An investigation is
reopenable as the same working context — persist where semantically
appropriate: query, scope, selection, filters, view, semantic zoom
level, comparison arms, inspector state, evidence position, navigation
context; reopening restores the research state, never a generic home
screen.

## 13. The Evidence Capsule

A first-class immutable/read-only research artifact:

```text
question · scope · run(s) · target · result · evidence
· causal slice · uncertainty · disposition · next discriminator
· provenance · analysis revision
```

A capsule reopens into its analytical context. A screenshot is NOT an
Evidence Capsule.

## 14. Task suite; interaction-cost budget

Minimum task suite (task proof covers these):

```text
T1 discover → load → verify a model      T5 compare BASE vs PERTURBED
T2 prompt → generate → stop → recover   T6 locate evidence behind a claim
T3 find a world divergence              T7 return to a prior context
T4 select event → inspect consequences  T8 export / reopen a result
```

Per task define: entry state, goal, primary actions, focus/state
transitions, error branches, completion proof, recovery path.
Budgets (product targets, not HCI laws): COMMON ACTION ≤ 1 primary
interaction after context is established; CONTEXT CHANGE ≤ 2–3
deliberate interactions; DEEP INSPECTION — a predictable path with NO
manual ID copying; RECOVERY — never a whole-task restart.

Consequent-state vocabulary:
`IDLE · READY · QUEUED · RUNNING · WAITING · BLOCKED · SUCCEEDED ·
FAILED · CANCELED · RECOVERING · STALE · DEGRADED · OFFLINE ·
PARTIAL · UNKNOWN`. Action contract: constraint → preview →
confirmation only when needed → commit → verify. Every important
failure exposes WHAT FAILED / WHY (best available cause) / WHAT
REMAINS INTACT / WHAT CAN BE DONE NOW / whether the semantic effect
is known / RETRY-UNDO-BACK-RESET-EXPORT-RECONCILE where applicable —
never a generic error wall.

### 14.1 Task modelling; the human-centred loop

A screen is a projection of a workflow, never the design starting
point. Every major surface walks: `context of use → user/goal/
constraints → task/workflow → information architecture → interaction
model → visual/type system → prototype → usability evaluation →
implementation → measurement → iteration`. For each major task define:

```text
USER · GOAL · TASK · CONTEXT · INPUT · DECISION · ACTION
→ FEEDBACK · SUCCESS · FAILURE · RECOVERY
→ ACCESSIBILITY · INPUT MODALITY · INTERRUPTION · RESUMPTION
```

Task graph: `goal → choose → inspect → decide → act → verify →
recover/continue`. Prioritise high-frequency, high-cost, high-risk and
high-load workflows before decorative refinement. HCI model caveats
(never laws): Fitts → target acquisition guidance; Hick-Hyman →
grouping/defaults/search guidance; "7±2" is not an interface-capacity
law; WCAG target sizes are conformance guidance, not universal desktop
geometry.

## 15. Accessibility; reduced motion; focus/keyboard

Minimum: semantic accessible names, keyboard reachability, visible
focus, logical tab order, screen-reader-compatible roles where
supported, non-color state encoding, reduced motion, adequate hit
targets, contrast, text-scaling tolerance. Reference baseline:
applicable WCAG 2.2 + ISO 9241-171:2025. Accessibility defects that
block task completion are FUNCTIONAL defects; focus tokens existing
is not "done".

Focus/keyboard contract — define per surface: focus order, entry,
restoration, shortcuts, Escape (cancel/close/clear the transient
action), stop shortcut, default action, selection movement; surface
switch restores meaningful focus; reopen restores last meaningful
focus where valid. Task-aware focus entry: Chat → composer; Models →
search/selected model; Settings → first/last meaningful field;
Observatory → query or preserved selection.

Reduced motion: EVERY motion effect (chat scroll tween, busy-dot
pulse, future transitions) has a meaningful static equivalent; the
reduced mode removes non-essential pulsing/decorative motion/long
transitions while preserving essential state visibility.

## 16. Responsive / DPI / multi-monitor

The fixed 1440×900 baseline is a bootstrap, not a product contract.
Viewport classes: `SMALL · MEDIUM · LARGE · HIGH-DPI · ULTRAWIDE`.
Per class verify: no critical clipping, critical actions reachable,
critical text visible, focus reachable, inspector collapsible,
navigation usable, context identity visible. Also define: minimum
window size, stretch/scaling behavior, font-scaling assumptions,
multi-monitor restore, DPI-change behavior.

## 17. Localization

ONE translation boundary — `_tr("chat.empty_state")` style keys, never
hard-coded user-facing strings across GDScript. The requirement is
localization-READY LAYOUT (Cyrillic-safe metrics, wrapping, button
resizing, tooltip expansion, long-label testing), not merely
"translate later". Never design fixed widths from English labels
alone — font metrics are part of layout.

## 18. Component architecture

`shell.gd` (2400+ lines) is an accepted bootstrap, not the long-term
composition boundary. The refactor is BY SEMANTIC RESPONSIBILITY:

```text
shell/workspace controller · nav · chat · models · settings
· observatory · shared controls · visual proof hooks
```

NOT 2200→100 tiny classes, and NOT widget-per-`.tscn`. A reusable
component is created only when it has reuse, independent state, an
independent test contract, or a meaningful lifecycle — neither a
god-script nor cargo-cult proliferation.

## 19. Scene IR integration; world presentation

The gap: Scene IR exists Python-side; Redot does not consume it.
The target chain (the world view stays a projection of
authoritative/typed data — never a second parallel scene authority):

```text
canonical scene/read model → Visual Scene IR → scene composition
policy → presentation read model → Redot → Canvas/sprites/effects/UI
```

Target graphics scope: 2D/2.5D (static/procedural background +
composited layers + sprite actors + animated sprite states + small
transient effects + UI overlays). NOT mandatory foundations: physics
world, rigid bodies, large 3D terrain, ray tracing, heavy GI,
volumetrics, massive skeletal animation — later admission is a
separate runtime/dependency decision. CanonSim determines semantic
existence/relevance/observability; the compositor only shows a bounded
subset and cannot create canonical facts. Camera layers (SEMANTIC
FOCUS/TARGET, PRESENTATION CAMERA, USER CAMERA STATE) never mutate
semantic focus or world state. Visual LOD (FULL → REDUCED →
IMPOSTOR → ABSTRACT) is distinct from semantic LOD and never alters
semantic truth. World visuals may express place/regime/material/
silhouette/structure/spatial relation/visible consequences — but
authority stays explicit metadata; the user never infers
canonical/observed/derived/unknown from artistic appearance.

## 20. Bounded rendering; performance

For large worlds/histories:

```text
viewport → visible semantic subset → aggregation → culling
→ virtualization
```

Never instantiate thousands of live Controls because the backend has
thousands of records (History, Observatory, timeline, tables, graph
neighborhoods, world objects). Long-range UI uses paged read models +
viewport virtualization + stable identity + selection preservation +
incremental loading. Analytical populations scale SMALL (JSONL +
SQLite) → MEDIUM (DuckDB over exports) → LARGE (Parquet + DuckDB);
distributed only on measured workload evidence. Boundedness = declared
ceiling + measurement + degradation path; measure the joint workload
(Redot UI + concurrent local LLM on the same GPU) — cold/warm
startup, RAM/VRAM idle+active, CPU during streaming, frame-time
p50/p95/p99, UI latency during streaming, history render cost, scene
rebuild cost, peak memory. Budget categories (declare a ceiling per
category): active/cache texture memory · asset count · active actors ·
active effects · atlas/texture size · scene rebuild frequency ·
materialised history · pending stream buffers · CPU frame budget ·
GPU frame budget. Do not solve every budget breach by growing caches —
the degradation ladder comes first (WORLD_PRESENTATION_LAW §13).

## 21. Surface hygiene

- **Dashboard syndrome — prohibited**: many simultaneously visible
  metrics/charts/status cards with no primary question, focal
  selection, analytical navigation, or next action. A World Profile
  is a vector of observables, not a scalar quality score; success is
  QUESTION → PRIMARY DISCRIMINANT → PRIMARY VIEW → DETAIL → EVIDENCE.
- **Context identity strip** on every high-consequence analytical
  surface: pack, run, seed, tick/time window, model/inference context
  where relevant, observation profile, result revision, freshness —
  progressive disclosure (compact strip → expandable detail).
- **Status bar**: engineering metadata (seam status, engine version,
  proof state) belongs in Diagnostics/About unless currently
  actionable; the task surface prioritizes connection, current
  run/context, active operation, unsaved changes, critical state.
- **Truncation**: never silently clip errors, diagnostics, effective
  state, model/result identity, provenance, important status — wrap,
  expand, tooltip, inspector, copy action, or detail view instead.
- **Settings UX**: EFFECTIVE vs DRAFT vs PENDING vs OBSERVED stay
  distinct (a control appearing changed while the backend is
  unchanged is the classic AI-tool lie).
- **Iconography**: a small semantic vocabulary (run, stop, pause,
  refresh, inspect, copy, search, filter, compare, timeline,
  relation, object, knowledge, warning, unknown, provenance, scope,
  lock); icon-only controls carry accessible name + tooltip; no icon
  soup.
- **Native vs custom**: native OS affordances for file/folder
  selection, window behavior, clipboard; custom controls only where
  CanonSim semantics require (evidence ladder, semantic timeline,
  compare alignment, world inspector, canonical status notation).
- **Drag/drop**: an accelerator with an equivalent
  keyboard/menu path — never the only route.
- **Persistence split**: application configuration / session state /
  chat-history / simulation checkpoint / visual cache / asset cache /
  UI-local state stay distinct; caches are rebuildable, canonical state
  is not. One product is visible even under multi-process topology;
  offline content tools (ComfyUI, Blender headless, Pillow) never
  become runtime dependencies; every admitted runtime dependency
  carries a licence/redistribution inventory. Trust boundary:
  `path ≠ command` · `import ≠ execution` · `model output ≠
  authority` · `asset metadata ≠ executable code` · `UI command ≠
  direct CanonSim mutation` · `external API/agent ≠ semantic bypass`.

### 21.1 Chat ergonomics

Chat must grow beyond `messages + input + send + stop`. Message-level
affordances where applicable: `copy · regenerate/retry · inspect
metadata · recover failure · export`. Chat output supports text
selection, code/log selection, clear error presentation, per-message
identity, run/model provenance. The near-bottom follow law (iter-230's
`tween + near-bottom gate + late-layout settle`) stays the reference
pattern. (wb-14 the Chat surface row's contract.)

### 21.2 AI-specific interaction contract

inf-1's consequence (LLAMA_CPP_INFERENCE_CONTROL_LAW §17): Inference
is the semantic generation-control WORKSPACE (under WORK); Chat
carries only a COMPACT contextual projection of the same inference
state + the link; the full control depth (chips, the sampler chain,
the effective-state presentation) lives in Inference — Chat never
holds its own hidden sampler settings.

AI-driven surfaces expose operational truth: `USER INPUT · SYSTEM/
DEVELOPER POLICY · MODEL INPUT · RESOLVED CONFIGURATION · MODEL OUTPUT
· OBSERVED RUNTIME · DIAGNOSTICS`. Preserve `requested ≠ accepted ≠
effective ≠ observed ≠ presented` (WORKBENCH_APP_LAW §19.1 owns the
composition; the UI renders the layers, never overwrites EFFECTIVE
from a widget value). Presets are intent-named, inspectable, editable,
versioned when persistence matters, and never silently modify
out-of-scope settings. Failure classes stay distinct: user input ·
configuration incompatibility · backend/model · resource · transport ·
cancellation · internal failure. For expensive/state-changing commands
distinguish NEW COMMAND vs RETRY; after transport loss with unknown
outcome, surface the uncertainty (SENT_OUTCOME_UNKNOWN) rather than
blindly retrying a possibly duplicated operation. Where reproducibility
matters, retain `model · backend · configuration · prompt · seed · run
· relevant diagnostics`; never claim bitwise reproducibility without
backend guarantees.

## 22. Verification architecture

Three DISTINCT proof layers — never conflated:

```text
STATIC UI PROOF ≠ RUNTIME UI PROOF ≠ TASK / HUMAN UX PROOF
```

- **Static** (no Redot needed): token usage, forbidden raw values,
  translation boundary, interactive control metadata, status-role
  mapping, contrast calculations, configuration invariants,
  component naming, surface registration.
- **Runtime** (needs Redot): layout, focus, keyboard, responsive, DPI,
  visual regression, scroll behavior, interaction states,
  accessibility tree, motion policy.
- **Task**: T1..T8 complete without hidden assumptions, without
  manual ID copying, without false semantic implication, without
  unnecessary recovery cost.

Gate matrix: A task validity · B information architecture · C
interaction + state correctness · D visual/token correctness · E
accessibility · F performance/boundedness · G empirical runtime
validation · H truth/provenance/epistemic correctness · I
agent-verifiability/maintainability. A surface is not "complete"
while major gates are undocumented.

Evidence classification (never fake a runtime pass):

```text
STATIC_VERIFIED · RUNTIME_VERIFIED · MANUALLY_VERIFIED
· TASK_VERIFIED · DEFERRED · NOT_VERIFIED
```

Where Redot runtime is available: deterministic captures across
SMALL/MEDIUM/LARGE/HIGH-DPI/ULTRAWIDE viewports × the task states
(empty, loading, ready, partial, stale, failed, selected, focused,
disabled, compare, evidence, inspector); regression compares semantics
where rendering is nondeterministic.

### 22.1 Usability evaluation and engineering metrics

The evaluation stack (cheapest sufficient evidence first):

```text
0 static/automated audit → 1 expert heuristic review
→ 2 cognitive walkthrough → 3 task-based usability test
→ 4 controlled comparison when a defined question exists
→ 5 validated subjective scales when useful (SUS · UEQ/UEQ-S · NASA-TLX)
→ 6 local instrumented behaviour when explicitly enabled/privacy-safe
→ 7 eye tracking/physiology only when cheaper evidence is insufficient
```

Subjective scales COMPLEMENT task evidence; they never replace observed
task completion and recovery behaviour. Track: effectiveness
(completion, error, accuracy, first-attempt success) · efficiency
(time-on-task, pointer travel, steps, backtracking) · recovery
(recovery time, undo/retry, abandonment) · cognitive workload ·
temporal latency (first feedback/actionability/completion/recovery) ·
state integrity (stale incidence, unknown outcomes,
requested/effective mismatch, reconciliation) · interaction integrity
(focus loss/restoration, duplicates, misfires, accidental destructive
actions) · system quality (input latency, frame time/drops, layout
shift, memory/CPU/GPU/VRAM pressure). Track DISTRIBUTIONS, not only
means. Controlled-comparison discipline: neutral variant naming,
counterbalanced/balanced order, control learning/fatigue/order/
carryover, predefined primary outcome, stable trace identity,
`ASSIGNMENT ≠ REALISED DELTA`; never call a design better because it
was shown second; never infer equivalence from non-significance
alone.

### 22.2 The acceptance benchmark and the final gates

The representative acceptance covers: Redot startup/packaging · custom
UI + keyboard/focus/accessibility · Chat streaming + large history ·
Models/Inference controls + effective-state display · the CanonSim
placeholder world + deterministic Visual Scene IR · procedural props/
actors + map/inventory interaction · assurance/observation views ·
asset load/reload + missing/stale degradation · backend loss →
reconnect/cancellation truth · screenshot/headless regression ·
frontend alone vs frontend + concurrent local LLM.

```text
G1  Redot startup/packaging works in the actual runtime envelope
G2  Chat/Settings/History use shared application operations
G3  backend reconnect/cancellation semantics remain correct
G4  CanonSim read-side seam explicit/renderer-independent
G5  Visual Scene IR fixture deterministic
G6  placeholder scene renders without hand-authored per-instance lists
G7  screenshot/headless regression works
G8  frontend cannot bypass application/semantic boundaries
G9  resource budgets measured with degradation paths
G10 concurrent LLM + frontend measured
G11 dependency/licence inventory complete for admitted runtime
G12 asset identity/provenance exists before large ingestion
```

Current owners: G4/G5/G7 LANDED (wb-1/wb-2 + visual_proof, the gated
packets); G1 rides the export row; G2/G3 partially landed (Chat/Models
over the gateway; reconnect is the streaming row); G6/G9/G10/G12 are
the P4 family's gates (WORLD_PRESENTATION_LAW §15); G8 is the
architecture-test set; G11 rides each dependency admission. A gate
passes only when its task, contract and evidence exist — visual polish
never substitutes.

## 23. Anti-patterns; corrected conclusions

Prohibited: second hidden frontend transport · second semantic
authority · visual inference of truth · color-only status · status
rainbow · generic dashboard syndrome · graph hairballs ·
card-everything · decorative motion as state · default engine theme
as product identity · unbounded Control-node rendering · silent
truncation of critical information · hard-coded UI strings · flat
navigation feature catalogs · component proliferation without
responsibility · manual ID copying between views · two
unsynchronised comparison screens · fake runtime "passed" status ·
"more panels" as the default answer to "more information" · a player
surface implying omniscient observability · model-capability data
auto-generating widgets · a giant generic Visual DSL before the first
real scene · modal chains compensating for missing IA · fixed-English
geometry (font metrics are part of layout) · a renderer dependency
added "just in case" · Redot resource/UID as CanonSim identity ·
style compensating for weak IA.

Corrected conclusions (do not adopt too literally): (a) accent
overload is fixed FIRST by shape/pattern/weight/iconography/position,
colors only if truly required; (b) NOT every component becomes
`.gd`+`.tscn` — split by responsibility/state/reuse/testability; (c)
accessibility is "materially incomplete implementation and
verification", not "zero"; (d) "1 of 12 surfaces" is a scope warning,
not a KPI; (e) never encode user-population assumptions — the
defensible requirement is Cyrillic-safe localization-ready UI.

## 24. Agent decision rules; Definition of Done

Before any frontend task, answer in order: (1) what user task? (2)
what semantic state is authoritative? (3) minimum information needed?
(4) which existing surface owns the task? (5) new surface or merely a
new view? (6) what selection/focus/context behavior? (7) what
epistemic states must be visible? (8) smallest reusable component
boundary? (9) which tokens? (10) which
accessibility/localization/responsive requirements? (11) how
statically verified? (12) how runtime-verified if Redot is available?
(13) how task-proven?

A need for new transport, new authority, a new generic visualization
abstraction, a new global status color, or a new top-level surface is
an ARCHITECTURAL ESCALATION — never a normal implementation detail.

A surface is complete only when: task defined + IA defined + state
model defined + interaction model defined + focus/keyboard path
defined + token usage verified + critical text not silently clipped +
accessibility path defined + responsive behavior defined +
localization boundary respected + truth/evidence semantics explicit +
boundedness respected + static proof passes + runtime proof passes
when available + task proof exists. Every intentionally deferred item
is explicitly marked `DEFERRED` — never silently omitted.

## 25. The implementation order (the row family)

The practical sequence (the queue COMPOSITION this law registers;
the ORDER stays the owner's call, TASKS the queue owner):

```text
P0 normative foundation   this admission + the ux-1 minimums row
                         (the _tr boundary, reduced-motion,
                         viewport/min-size, focus/keyboard baseline)
P1 Observatory skeleton  obs-1..obs-N — the vertical UX slice FIRST:
                         nav entry → empty/read-only surface → World
                         Question contract → context strip → query
                         lifecycle → primary view → selection →
                         inspector → evidence ladder → semantic
                         breadcrumb (validate the grammar BEFORE full
                         analytical backend coverage; no need for full
                         causal graph/map/history/ensembles in the
                         slice)
P2 structural cleanup     shell responsibility split · shared
                         components · localization boundary · token
                         expansion · truncation audit · keyboard
                         shortcuts · focus restoration ·
                         viewport/min-size policy — the wb-13+
                         visual rows continue here per
                         VISUAL_SYSTEM_UI §10
P3 analytical depth       timeline · compare · semantic zoom ·
                         cross-highlighting · archaeology · bounded
                         graph · Evidence Capsules · persistent
                         research contexts
P4 world presentation    Scene IR → Redot · deterministic world
                         rendering · world visual identity ·
                         procedural/asset presentation ·
                         assurance/debug overlays
```

The standing resolution: do NOT spend iterations polishing a
peripheral generic chat shell while the project's defining analytical
surface remains absent — but do not jump from documentation to a
1800-line Observatory either; the slice validates the interaction
grammar (question grammar, selection, context, focus, drill-down,
evidence, visual hierarchy) first.

## 26. Contradictions register (resolutions)

| Issue | Resolution |
|---|---|
| Accent color | Keep restrained; distribute meaning across non-color channels first; add colors only if semantically necessary |
| Component architecture | Split by responsibility/state/reuse/testability; avoid both extremes |
| Observatory priority | Small vertical slice EARLY; only proven-necessary peripheral work continues |
| Accessibility status | Materially incomplete in implementation and proof despite good foundations |
| Specification size | One authoritative source; a compact routing law that references, never silently deletes |
| Graph centrality | Bounded contextual view; timeline/table/diff/inspector primary |
| Visual identity | Semantic geometry/typography/iconography/notation; no ornamental overload |
| Current UI state | Useful infrastructure slice, not the completed product |
| Runtime testing | Static proof cannot substitute for runtime/task proof |
| Localization | Boundary established NOW; language expansion staged |
| Fixed viewport | Baseline kept; min-size/stretch/viewport matrix before surface count grows |
| Visual Scene IR | Does not block the interaction spike; one eventual semantic path into Redot; never a second scene authority |

## 27. Non-negotiable invariants

```text
 1. UI never becomes semantic authority.
 2. Frontend never invents truth from appearance.
 3. CANONICAL / OBSERVED / DERIVED / UNKNOWN remain distinct.
 4. FACT / INFERENCE / HYPOTHESIS / PROPOSAL / UNKNOWN remain distinct.
 5. Selection is shared semantic identity, not widget-local state.
 6. Context is visible for high-consequence analytical work.
 7. Compare uses synchronized semantic coordinates.
 8. Graph remains bounded.
 9. Critical information is never silently truncated.
10. Color is never the sole carrier of important state.
11. Accessibility is part of implementation, not documentation.
12. Localization is part of layout architecture, not post-hoc.
13. Responsive/DPI behavior is a contract, not an anecdote.
14. Static proof does not masquerade as runtime proof.
15. Runtime proof does not masquerade as task proof.
16. New abstractions require semantic justification.
17. New top-level surfaces require intent justification.
18. Evidence and provenance remain reachable from analytical claims.
19. Results remain reopenable with sufficient context.
20. Every deliberately deferred requirement is explicitly marked DEFERRED.
```
