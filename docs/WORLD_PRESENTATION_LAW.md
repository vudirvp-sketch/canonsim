# WORLD_PRESENTATION_LAW.md — The World Presentation / Visual Runtime Law

> The owner's 2026-09-25 corpus re-homing call (D-218, iter-237) over the
> world-presentation half of the external v5.2 corpus —
> `CANONSIM_FRONTEND_UI_VISUAL_ENGINEERING_SPEC_V5_2.md` §§23–31, 35–36
> + the unique depth of `CANONSIM_VISUAL_PRESENTATION_RUNTIME_
> ARCHITECTURE_V5_2.md` (asset vocabulary, formats, animation policy, map
> architecture, degradation). Per the D-024/D-200 law the external briefs
> are NEVER vendored; THIS file is the repo-side binding distillation and
> the LAW OWNER for the P4 row family (FRONTEND_UIUX_LAW §25's "world
> presentation" rung).
>
> **Routing law:** every world-presentation question — Visual Scene IR
> beyond the landed identity closure, composition, assets, manifests,
> LOD, camera layers, maps, backgrounds, effects, degradation, visual
> performance — routes HERE first. Interaction/UI → FRONTEND_UIUX_LAW;
> chrome tokens/typography → VISUAL_SYSTEM_UI; engine facts/API →
> REDOT_ENGINE_INDEX; application operations → WORKBENCH_APP_LAW;
> analytical semantics → OBSERVATORY_LAW. The seam's identity/determinism
> contracts stay `docs/CONTRACTS.md` §5 D2/D4/D5 (wb-1's landed form);
> this law extends them, never re-states them as a competing owner.
>
> **Current state:** the Python half is LANDED (`workbench/scene_ir.py` +
> `scene_build.py`, wb-1: typed, deterministic, the identity closure +
> status laws, byte-identical IR JSON + the double-run PNG proof). The
> Redot consumption half is NOT STARTED (the P4 family). Sections below
> carry `[LANDED …]` / `[CONTRACT — the P4 rows]` honestly.

## 1. The boundary and the two procedurality forms

```text
CanonSim semantic/read products → Visual Scene IR → scene composition
policy → asset selection/variation → presentation read model
→ Redot → Canvas/sprites/effects/UI
```

The two procedural forms are NEVER conflated:

```text
semantic procedural generation = what semantically exists/matters/is observable
visual procedural composition  = how existing semantics are shown
```

CanonSim determines semantic existence, relevance and observability; the
compositor determines how a BOUNDED subset is shown and cannot create
canonical facts. A second parallel frontend scene authority is
prohibited; the World view is a projection of authoritative/typed data.

## 2. Visual Scene IR contract `[LANDED — scene_ir.py; CONTRACTS D2/D4/D5 own identity/determinism]`

The IR is engine-independent and read-side: no Redot `Node`,
`Texture2D`, GPU IDs, renderer resource paths as identity, or renderer
internals. Conceptual structure:

```text
Scene = scene_identity + source_revision + observation_profile + camera
      + background + layers[] + props[] + actors[] + effects[]
      + overlays[] + interaction_hints[] + provenance
Instance = asset_id + variant_id + position + rotation + scale + layer
         + visibility + animation/state + material/palette variant
         + semantic status + source/provenance reference
```

Presentation semantics distinguish at least `CANONICAL | DERIVED |
OBSERVED | UNKNOWN | HIDDEN | TEXTURE/PURELY_VISUAL`; the silent
collapses `UNKNOWN→ABSENT`, `HIDDEN→ABSENT`, `VISUAL→CANONICAL`,
`LLM-text→CANONICAL` are forbidden (D5). The IR exists to separate
semantics from rendering, make compositor output testable, enable
screenshot regression/CLI/debug reuse, and keep Redot from becoming
CanonSim. Keep the IR minimal — it is not a universal scene DSL; a giant
generic Visual DSL before the first real scene is an anti-pattern.

## 3. Deterministic composition

Composition input:

```text
local semantic context + seed + style profile + asset vocabulary
+ placement/visibility constraints → deterministic composition
```

Grammar: `region/scene type → structural grammar → compatible asset
families → neighbour/anchor constraints → deterministic variation →
occlusion/layer rules → density → final composition`. Candidate
algorithms (weighted selection, graph grammar, constraint propagation,
WFC-like methods, local search/backtracking) are selected EMPIRICALLY
from representative scenes — never frozen because fashionable.

Determinism target:

```text
same semantic input + same seed + same asset manifest → same composition
```

unless intentional nondeterminism is declared. The Townscaper-like
PRINCIPLE: small compatible vocabulary + strong composition rules >
thousands of hand-authored finished scenes — the principle is adopted,
never the implementation. `[CONTRACT — the P4 composition rows]`

## 4. Asset-first, not asset-heavy

The primary visual bottleneck is a coherent VOCABULARY, not a renderer.
AI/offline content tooling produces base sprites/textures, style/material
variants, pose/expression variants, prop families, background fragments;
runtime procedural composition owns placement, transforms, variant
choice, compatibility, density, layering, occlusion, clutter, light
effects; CanonSim owns semantic existence/state.

The initial reusable vocabulary (the P4 kit's first cut):

```text
terrain/ground · roads/paths · walls/floors/roofs · windows/doors/stairs
fences/arches/pillars · signs/lamps/pipes · vegetation/rocks/water accents
crates/barrels/bags/tables/chairs/tools/baskets/books/bottles/clutter
actor base + pose + idle + expression + state variants
inventory/map/compass/journal/notice/status icons
```

Prefer PARAMETERIZED variants when adequate: mirror/rotation/scale,
palette/material, weather, wear/damage, occupancy, expression/pose,
decals — never a full independent asset per variation when composition
parameters suffice. `[CONTRACT — the P4 vocabulary rows; do not scale
asset production before §1's seam is proven end-to-end in Redot]`

## 5. Asset identity, provenance and the Asset Manifest contract

Filesystem path is LOCATION only. Distinguish:

```text
AssetId · ContentIdentity/digest · Location · Version/compatibility
Lifecycle state · Variant · Source asset · Derived asset · Runtime artifact
```

Example: `actor.blacksmith + variant angry_02 + content digest +
compatibility`. Same path with changed bytes = a new content identity.
Multi-file/sharded assets use deterministic composite identity over
material constituents + relevant metadata/schema. AI-generated/offline
provenance must be available to the manifest — a path alone is never
sufficient for reproducibility.

Assets are consumed through an EXPLICIT MANIFEST, never ad-hoc file
paths. A material asset entry exposes:

```text
asset_id · asset_revision/content_identity · format + dimensions +
colour/alpha metadata · semantic/visual role · licence/provenance
compatibility/runtime requirements · source/tool/version where material
validation status
```

Lifecycle:

```text
DISCOVERED → IDENTITY_VERIFIED → FORMAT_VALID → COMPATIBLE
→ VISUALLY_VALID → RUNTIME_READY
```

Failure states: `MISSING | INVALID | INCOMPATIBLE | STALE | CORRUPT |
UNKNOWN`. A bad asset is NEVER silently replaced by an arbitrary
visually similar asset when that would change reproducibility or
semantic presentation — fallbacks are explicit and typed.
`[CONTRACT — the manifest row; G12 (asset identity/provenance before
large ingestion) is its gate]`

## 6. Pipeline, formats and offline tooling

```text
semantic asset specification → generation/acquisition → cleanup/normalisation
→ validation → variant generation → atlas/spritesheet → asset manifest
→ content identity → runtime load
```

Formats are chosen per class (source vs runtime vs archive), recorded in
the manifest, and validated at admission — never improvised per asset.
Offline content tooling (ComfyUI/Qwen Image, Blender headless, Pillow,
trimesh, atlas/validation tools) generates/validates content but NEVER
becomes a runtime dependency merely because it touches assets
(WORKBENCH_APP_LAW §27 + AGENTS §2.8 the admission law). Every shipped
asset carries licence/redistribution provenance (§13). `[CONTRACT]`

## 7. Camera, maps and the P4 surfaces

Camera state has separate layers:

```text
SEMANTIC FOCUS/TARGET = read-side consequence of the current task/world view
PRESENTATION CAMERA    = framing/composition chosen to make the focus legible
USER CAMERA STATE      = user-controlled navigation/zoom/pan context
```

Changing the presentation camera must NOT mutate semantic focus or world
state; a camera target derived from canonical/read-side facts is not
itself a canonical fact. Camera is presentation state — it may depend on
scene type, focal actor, UI mode, preferences, zoom; never on world
semantics. Profiles: `LOCAL_SCENE · MAP · CHARACTER_FOCUS · INSPECTION ·
DEBUG`.

Map projection levels: `WORLD → REGIONAL → LOCAL → SCENE` — each level
may have a different visual vocabulary/resolution. The P4 surfaces are
PROJECTIONS, never independent semantic models: inventory maps semantic
items to icons/state/quantity; compass maps semantic heading/bearing to
UI; journal/notes maps persisted records to a surface; notice boards map
world-backed notices to procedural cards. None requires another graphics
engine. `[CONTRACT — the P4 map/surfaces rows]`

## 8. Backgrounds, LOD, effects, animation

- **Static backgrounds are an optimization feature**:
  `semantic local context → deterministic composition → cached
  background → dynamic actors/effects/UI`; update only changed layers;
  never store/reload the entire visual world for the current viewport.
- **Visual LOD** (independent of semantic LOD; can never alter semantic
  truth):

```text
FULL = actor animation + local props + effects
REDUCED = simpler sprite + reduced animation + fewer props
IMPOSTOR/COMPOSITE = precomposed/simplified layer
ABSTRACT = icon/silhouette/map symbol
```

- **Effects** are presentation unless they represent a semantic entity
  (rain/fog/snow/wind/dust/spark/glow/fire ambience/ink/splatter/
  transitions/focus/selection). Prefer particles, animated textures,
  sprite sequences, small shaders — ordinary effects never become
  GPU-heavy simulations without measured need.
- **Animation policy**: motion supports state and hierarchy, never
  decorates (FRONTEND_UIUX_LAW §15's reduced-motion law applies to world
  motion too); animation state is derived from semantic state + declared
  visual policy; deterministic playback where captures must regress.
  `[CONTRACT]`

## 9. Observation boundary and assurance views

World presentation respects the selected observation scope:

```text
CANON VIEW · PERCEPTION VIEW · ASSURANCE VIEW · DEBUG VIEW
```

Distinguish what exists, what is visible, what is known/observed, what
is derived only for presentation, what is intentionally hidden — the
visual system shows only what the chosen observation profile permits
(OBSERVATORY_LAW §11's information states are the semantic source).
Assurance/debug metadata may include: `asset_id · entity_id · layer ·
visual LOD · semantic status · source revision · scene seed ·
composition rule · unknown/hidden markers · provenance`. Debug may be
more informative than player-facing UI without creating additional
authority. `[CONTRACT — the assurance rows]`

## 10. Scene invalidation and rebuild contract

Presentation state has EXPLICIT invalidation causes:

```text
SEMANTIC_CHANGE           → rebuild the affected semantic projections
ASSET_MANIFEST_CHANGE     → invalidate affected asset bindings/composition
COMPOSITION_POLICY_CHANGE → rebuild the visual composition
SCHEMA_CHANGE             → migrate/reject the Scene IR per the schema contract
CAMERA_ONLY_CHANGE        → presentation update; NO semantic rebuild
UI_THEME_CHANGE           → UI restyle; NO semantic rebuild
CACHE_EVICTION            → rebuild from authoritative/read-side inputs
```

The frontend must not use a stale visual cache as if it were current
semantic state. Rebuild operations are bounded and observable; a failed
rebuild preserves the last known valid presentation when safe and
exposes a stale/degraded status rather than silently fabricating
replacement content. `[CONTRACT — the P4 invalidation row; the LAW §20
boundedness laws apply to every rebuild]`

## 11. Stylistic rendering and the two-layer identity

Professional distinctiveness is not `dark + neon + rounded cards + glow`
— it is hierarchy, controlled contrast, intentional density, restrained
geometry, stable alignment, coherent type, semantic colour, purposeful
motion (VISUAL_SYSTEM_UI owns the chrome side; this law owns the WORLD
side). CanonSim's world presentation MAY use an aggressive graphic
language — strong silhouettes, high contrast, controlled material
separation, limited intentional shading, graphic overlays, ink/splatter/
stencil/screenprint energy — as STYLISTIC choice, never as usability
law; style must not hide state or weaken hierarchy. The world and the
Workbench chrome may share typography logic, spacing, selection/focus
grammar and semantic status grammar — not necessarily ornamental
treatment. World visuals may express place/regime/material state/
silhouette/structure/spatial relation/visible consequences, but
authority stays explicit metadata: the user never infers canonical/
observed/derived/unknown from artistic appearance (FRONTEND_UIUX_LAW
§19's rendering principle). `[CONTRACT]`

## 12. Performance and resource model

**The shared-GPU admission rule (LAW)**: the visual runtime MUST assume
the same machine/GPU may concurrently host a local LLM — visual capacity
is never treated as dedicated headroom. Acceptance uses measured
profiles for: `visual-only · visual + representative local-LLM load ·
peak asset/scene transition · worst supported window/DPI case`. The
benchmark matches the real product: `Redot UI + large history + mostly
static scene + several animated actors + light effects + concurrent
local LLM on the same GPU`. Measure frontend alone AND frontend +
concurrent LLM:

```text
cold/warm startup · RAM/VRAM idle+active · CPU during streaming
GPU during scene/effects · frame p50/p95/p99 · UI latency during streaming
history/query/render cost · scene rebuild frequency/cost
asset load/reload · stream buffer size/update cadence
shutdown/reconnect behaviour
```

Budget categories: `active texture memory · cached texture memory ·
asset count · active actors · active effects · atlas/texture size ·
scene rebuild frequency · materialised history · pending stream
buffers · CPU frame budget · GPU frame budget`. "Bounded" = declared
ceiling + measurement + degradation path. `[CONTRACT — the perf row;
G9/G10 its gates]`

## 13. Failure and degradation behaviour

The minimum visual recovery policy:

```text
missing asset        → safe placeholder/fallback + diagnostic (never an arbitrary lookalike)
invalid manifest     → reject the affected set, preserve the usable scene
stale scene revision → mark stale / rebuild from the current source
backend/LLM stall    → expose lifecycle/timeout, never fake completion
history over budget  → page/virtualize
resource pressure    → explicit degradation ladder: reduce visual detail/effects
                       → reduce offscreen/cache size → collapse distant layers
                       → switch visual LOD → page/virtualize history
```

Canonical/backend failures are never hidden by attractive visual
masking; UNKNOWN renders as unknown, never as success or absence. Every
admitted runtime dependency, plugin, codec, importer and shipped asset
carries an explicit licence/redistribution inventory — a permissive
engine licence does not imply the shipped bundle is permissively
redistributable. Trust boundary (the LAW §21 set, world side): `path ≠
command · import ≠ execution · model output ≠ authority · asset
metadata ≠ executable code · UI command ≠ direct CanonSim mutation`;
Redot input, imported assets and external metadata are UNTRUSTED until
application validation. `[CONTRACT — the degradation row]`

## 14. The renderer fork gate

The runtime baseline is Redot 26.2 LTS (Compatibility). Another
engine/runtime is admitted ONLY when ALL are demonstrated: `real
consumer + concrete limitation/risk + measured quality/performance gap +
acceptable runtime/dependency/licence envelope + testable agent
workflow`. Reconsider Redot only if: 2D/2.5D cannot represent the
required visual class; a required asset class demands a materially
different runtime; measured GPU/RAM overhead breaks the product budget;
agent automation cannot reliably achieve required changes; packaging
creates an unacceptable constraint. Never add Panda3D/ModernGL/wgpu/
full-3D machinery just for future-proofing. `[LAW — mirrors
REDOT_ENGINE_INDEX's version firewall]`

## 15. Acceptance and gates

The world-presentation slice of the acceptance benchmark
(FRONTEND_UIUX_LAW §22.2 owns the full set + the A–I design gates):

```text
G4  CanonSim read-side seam explicit/renderer-independent      [LANDED wb-1]
G5  Visual Scene IR fixture deterministic                      [LANDED wb-1]
G6  placeholder scene renders without hand-authored per-instance lists
G7  screenshot/headless regression works                       [LANDED — visual_proof]
G9  resource budgets measured with degradation paths
G10 concurrent LLM + frontend measured
G11 dependency/licence inventory complete for admitted runtime
G12 asset identity/provenance exists before large ingestion
```

Visual regression compares SEMANTICS where rendering is nondeterministic;
screenshot-driven development (agent → code/config → Redot headless →
deterministic capture → inspect → patch → rerun) is the standing
workflow — REDOT_ENGINE_INDEX owns its mechanics. `[CONTRACT — the P4
acceptance row]`

## 16. Design rules (the world-presentation subset)

```text
1  Workbench and game are one frontend/product.
2  2D/2.5D is the baseline; 3D/another renderer requires measured admission.
3  CanonSim is sole semantic authority; the UI is a read/control surface.
4  The Scene IR is a renderer-independent read-side contract.
5  UNKNOWN/HIDDEN/ABSENT and CANONICAL/DERIVED/OBSERVED/VISUAL stay distinct.
6  Visual composition may vary presentation but cannot invent canonical facts.
7  Semantic LOD and visual LOD are separate; static layers/caches are bounded
   optimizations, never canonical state.
8  Small reusable asset vocabulary + deterministic variants + procedural
   composition is the baseline content strategy.
9  AI/offline tooling creates the vocabulary; runtime composes it; CanonSim
   supplies semantics.
10 All consequential actions expose status, recovery and effective outcome.
11 Large history/streams/assets are explicitly bounded; visual performance
   is measured with AND without concurrent local LLM inference.
12 Style is subordinate to hierarchy, state clarity and task success.
13 The agent workflow is code/config/CLI/headless/screenshot-first; the GUI
   editor is support tooling.
14 New visual abstractions/dependencies require real consumer + problem +
   test/falsifier (AGENTS §2.8).
```

Implementation order for the P4 family (dependency logic; the ORDER is
the owner's call): `A seam: read model → minimal Scene IR → placeholder
compositor → semantic/visual overlay → deterministic replay proof
[LANDED] → B vocabulary: manifest/identity → small reusable kit →
variants → placement constraints → backgrounds → actors → effects →
C surface expansion: map → inventory → compass → journal → notices →
perception/assurance/debug → D optimization: atlas/cache → visual LOD →
rebuild limits → history virtualization → CPU/GPU/VRAM budgets → the
concurrent-LLM benchmark`. Never scale asset production before the seam
is proven.
