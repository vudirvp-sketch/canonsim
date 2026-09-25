# LLAMA_CPP_INFERENCE_CONTROL_LAW.md — The Semantic Inference-Control Architecture Law

> The owner's 2026-09-25 chip-workspace hand-off (the external
> `llama_cpp_chip_workspace_spec_2026-09-25.md` + the reviewed
> `флаги llama.cpp.txt` runtime snapshot — research inputs, NEVER
> vendored). Per D-024/D-200 THIS file is the repo-side binding
> distillation: the single normative owner of the llama.cpp semantic
> inference-control architecture. The external documents stay with
> the owner; nothing in this repo restates them as authority.
>
> **Routing law:** every llama.cpp semantic-control question —
> chip identity, kinds, scopes, AUTO, the sampler chain, relations,
> effective state, presets/scenarios/recipes/hardware-profile
> semantics, capability versioning, backend translation, the
> extra_args hatch — routes HERE first. Application composition →
> `docs/WORKBENCH_APP_LAW.md` (§19 owns the composition chain);
> interaction → `docs/FRONTEND_UIUX_LAW.md`; visual treatment →
> `docs/VISUAL_SYSTEM_UI.md`; Redot facts →
> `docs/REDOT_ENGINE_INDEX.md`; implementation order →
> `docs/TASKS.md`. `AGENTS.md`, `STATUS.md`, `DECISIONS.md` remain
> HIGHER authority.
>
> **Honesty law:** each section carries its CURRENT state —
> `[LANDED iter-239 (inf-1)]`, `[PARTIAL …]`, or `[CONTRACT …]`.

## 0. The core position

A flat list of 100+ llama.cpp flags is the wrong primary surface.
The useful abstraction is a **state-aware semantic configuration
layer**: the user manipulates semantic controls ("chips"); the
application resolves them into an effective configuration; the
compiled CLI/request form is a technical artifact.

```text
A CHIP IS NOT A CLI FLAG.
A CHIP IS NOT A UI BUTTON.
A CHIP IS A SEMANTIC RUNTIME CONTROL,
AND THE UI CHIP IS ONE PROJECTION OF IT.
```

The pipeline this law owns:

```text
LLAMA.CPP CAPABILITY → SEMANTIC CONTROL → PROFILE COMPOSITION
→ VALIDATION + RELATION RESOLUTION → EFFECTIVE CONFIGURATION
→ BACKEND COMPILATION → LLAMA.CPP RUNTIME → OBSERVED STATE
→ INFERENCE / CHAT / RUNS / OBSERVATORY PROJECTIONS
```

Non-negotiable principles (the research specification's own ten,
binding here): upstream is authoritative for existence/syntax;
semantic metadata is application-owned; `default=off` ≠ unneeded;
not everything is a "sampler"; no universal performance claims;
configured-but-ineffective controls stay VISIBLE; ordering is
personal/context, never a community ranking; presets are
transparent; configuration ≠ procedure; the current version is a
snapshot — `--help` of the actual binary is the final check.

## 1. Ownership: Settings ≠ Inference Control

```text
SETTINGS  = persistent DEPLOYMENT/launch configuration (the
            executable preference, the web-UI surface, the raw
            extra_args hatch)  — workbench/application/settings.py
INFERENCE = the semantic generation-control workspace (the chip
            library, the profile, the resolver, the compiled
            surface) — workbench/application/inference.py
```

The launch-settings store is the DEPLOYMENT half (schema
`canonsim.workbench.settings/2`); the inference profile store is
the §19.1 BASE PROFILE layer (`canonsim.workbench.inference/1`,
`workbench/runtime/inference.json`). One control, ONE value owner:
the semantic generation-control values live in the inference
profile — never duplicated into the settings store, never a second
configuration system. `[LANDED inf-1: the split + the one-way
migrate_launch_semantics boot migration (values preserved
verbatim, a present profile wins)]`; `[LANDED inf-2: the FULL
reviewed surface — 85 controls over 15 categories (model, device,
memory, loading, moe, cpu, sampling, chat, structured, server,
observability, speculative, rope, special, lora — the §31 category
ladder), every family its own category, never one "advanced
parameters" bucket; the profile document is field-stable (the
inf-1 flat fields unchanged, the new fields default; the 5-member
chain upgrades to 9 at load — the operator's order preserved)]`

Single-owner routing (the whole table):

| Concern | Owner |
|---|---|
| flag existence/syntax/values/defaults | the actual installed llama.cpp runtime (evidence: the reviewed snapshot; re-verify per §19) |
| semantic control model/identity/relations/effective state | THIS LAW + `workbench/application/inference.py` |
| deployment/launch persistence | `workbench/application/settings.py` (app §7.1) |
| profile composition chain + REQUESTED/ACCEPTED/EFFECTIVE/OBSERVED/PRESENTED | `WORKBENCH_APP_LAW.md` §19.1 (never restated here) |
| flag emission (the runtime translation) | `workbench/platform/llama_process.py` (the platform's typed surface — app §2's seam law) |
| inference interaction/IA | `FRONTEND_UIUX_LAW.md` (§21.2) |
| chip visual states | `VISUAL_SYSTEM_UI.md` (§5) |
| implementation order | `TASKS.md` |

## 2. The three layers (never collapsed)

```text
RAW CAPABILITY      the runtime's own surface — existence, syntax,
                    supported values, actual defaults. The reviewed
                    --help snapshot is EVIDENCE; the installed binary
                    is AUTHORITY. Never hardcoded as permanent law.
SEMANTIC CONTROL    the application's overlay — identity, human
                    name, category, kind, scope, default, relations,
                    effective state. THIS layer owns MEANING.
UI REPRESENTATION   the Redot projection — one representation of a
                    control, never the semantic authority. A chip
                    widget edit is a REQUEST, never a truth.
```

Identity is the SEMANTIC id (`sampling.top_k`), never the raw flag;
the flag (`--top-k`) is the raw mapping — tooltip/compile detail.
The human name is the primary surface (`MoE CPU Offload`, never
`--n-cpu-moe`).

## 3. The control model

Every semantic control carries:

```text
id (namespaced) · human name · category · kind · scope ·
raw flag mapping · value documentation · project baseline ·
upstream default · notes (evidence-tagged) · status
```

Kinds (the minimum set; the UI renders each as it sees fit —
DATA-DRIVEN over the control's own value_type/forms/limits
metadata, inf-2: the UI never re-encodes the vocabulary):

```text
value   an inline scalar (Context, Temperature, Seed)
mode    an enum selection incl. AUTO forms (GPU Layers, Flash
        Attention, Fit, KV K/V, Chat Template, Load Mode, NUMA,
        Reasoning, Speculative Type)
toggle  a boolean state (Fit in its on/off flag form, Warmup,
        Continuous Batching, Prompt Caching)
chain   an ordered semantic object (the Sampler Chain, §11)
display a read-only semantic projection (reserved)
```

Status (the capability vocabulary, future discovery's states):

```text
ACTIVE | UNCLASSIFIED (a NEW upstream control, nobody classified)
| LEGACY | REMOVED (searchable, never emitted for the current
runtime)
```

`[LANDED inf-1: CONTROL_LIBRARY — the first admitted set; the
vocabulary is representable and test-pinned; REMOVED never emits]`
`[LANDED inf-2: the library covers the WHOLE reviewed surface —
the complete sampling family (Top-K/P, Min-P, Typical-P,
Top-N-Sigma, the penalties family, the DRY family, the XTC family,
the Mirostat family, Dynatemp, Adaptive-P, Ignore EOS, Logit Bias,
Seed), the model/device/memory/loading/moe/cpu families, chat +
reasoning, structured output, server/concurrency, observability,
speculative, RoPE/YaRN, special modes and LoRA — every disabled
form and AUTO form the runtime's own literal, pinned per control]`

## 4. Defaults ladder (never collapsed into one "default")

```text
UPSTREAM DEFAULT    the runtime's own value (runtime evidence —
                    e.g. --temp 0.80, top-k 40, penalties 1.00)
PROJECT BASELINE    CanonSim's own pin (e.g. penalties 1.1, -fa on
                    — deliberately ≠ upstream, documented per
                    control)
PROFILE VALUE       the user's persisted BASE PROFILE value
SESSION OVERRIDE    [CONTRACT — the session-profile row]
REQUEST OVERRIDE    the call-local value (chat.send's explicit
                    temperature)
EFFECTIVE VALUE     what the resolver composed for execution
OBSERVED VALUE      what the runtime actually showed
```

Never silently rewrite the project baseline to match upstream (and
conversely). Both ride the resolver document side by side.

## 5. Scope model

Every control carries an explicit scope:

```text
spawn    the llama-server launch flags (context, GPU, KV, the chain)
request  the per-request API surface (chat.send's temperature)
spawn+request  both layers (temperature; seed [CONTRACT — the
               adapter's request surface row])
```

`CLI default ≠ server default ≠ request default ≠ effective value`:
the scope field is the discrimination, never one universal
"default".

## 6. Composition and the resolver

Composition follows WORKBENCH_APP_LAW §19.1 (its own law, never
restated): BASE PROFILE → SESSION OVERRIDE [CONTRACT] → CALL-LOCAL
OVERRIDE → VALIDATION → RELATION RESOLUTION → VERSION CAPABILITY
CHECK [CONTRACT — the discovery row] → EFFECTIVE CONFIGURATION.

The resolver (`resolve()`) is a DETERMINISTIC pure function of the
profile (+ the request layer): every resolved control names its
value, its source (profile/request), its state and its reasons.
UI state is never the backend configuration; a widget edit never
overwrites EFFECTIVE. `[LANDED inf-1]`

## 7. Effective-state vocabulary

```text
EFFECTIVE       the value reaches the runtime at its scope
AUTO            the value is an AUTO form (§10)
INACTIVE        the control is off BY ITS OWN VALUE FORM (the
                runtime's disabled values: top_k 0, top_p 1.0,
                min_p 0.0, penalties 1.0)
INEFFECTIVE     accepted but nullified by a relation — the REASON
                is mandatory (deterministic decoding; out of chain)
CONFLICT        hard incompatibility (the §13 duplicate ownership)
RISK            runs, environment-specific cost/instability risk
                [no slice relations yet — representable, never
                faked]
EXPERIMENTAL / UNCLASSIFIED / LEGACY / REMOVED  capability statuses
```

Do NOT hide configured-but-ineffective controls: they stay VISIBLE
with their reason (the Top-P-0.95-under-Mirostat shape). Risk never
masquerades as invalid. `[LANDED inf-1: the vocabulary + the
deterministic-decoding and chain-membership relations]`

## 8. Operational truth

The §19.1 chain — REQUESTED / ACCEPTED / EFFECTIVE / OBSERVED /
PRESENTED — stays distinguishable end to end: the chat run document
carries `requested` (the caller's explicit ask, None where absent)
separate from `effective` (the composition's resolution); OBSERVED
stays the backend's own answer (content/finish_reason/identity);
the UI never infers runtime truth from an edited field.
`[LANDED inf-1: the chat row's pair; the rest ride §19.1's law]`

## 9. AUTO is a real state

`AUTO` is a first-class RUNTIME form, never "unset"/"off":
`-ngl auto` (GPU Layers AUTO), `-fa auto` (Flash Attention AUTO),
`--seed -1` (the runtime's own random sentinel). AUTO, an explicit
value, and disabled (INACTIVE) are three DISTINCT states — the
resolver and the UI never collapse them. `[LANDED inf-1]`

## 10. Capability authority and versioning

The installed binary outranks every document (including this one)
for existence/syntax/values. New upstream controls surface as
UNCLASSIFIED (visible in discovery, classifiable, never silently
omitted); disappeared controls archive as LEGACY/REMOVED
(searchable, replacement attached when known, NEVER emitted for the
current runtime). The semantic layer survives upstream churn; the
raw registry never pretends upstream is static.
`[CONTRACT — the capability-discovery row (§19); the slice's
library is the admitted snapshot with the build-sensitive notes
pinned per control]`

## 11. The sampler chain

The chain is an ORDERED first-class semantic object — never an
unordered favorites grid. A member exposes:

```text
id · enabled (chain membership) · order · value · state ·
reason-if-not-effective
```

The reviewed default order (runtime evidence): `penalties → dry →
top_n_sigma → top_k → typ_p → top_p → min_p → xtc → temperature`
(simplified `edskypmxt`); the chain's controllable set is the FULL
nine-member reviewed order (`[LANDED inf-2]` — the inf-1 slice
carried the controllable five). An actual order change changes
the EMITTED configuration (`--samplers`, the runtime's own ';'
separator — pinned from the reviewed evidence).

Membership and value are SEPARATE concerns: `enabled=false` removes
the member from the emitted chain while its VALUE family stays
configured (INEFFECTIVE with its reason — the FAMILY concern: the
"dry" step governs the whole DRY family, never just the
multiplier). Temperature 0 is the DETERMINISTIC decoding state: the
distribution samplers go INEFFECTIVE with reasons — their values
are PRESERVED, never deleted (the user returns by restoring the
temperature; the profile is non-destructive). `[LANDED inf-1]`
`[LANDED inf-2: the chain validation accepts only the WHOLE
nine-member document — a partial edit refuses LOUD; an inf-1
5-member profile upgrades at load, the operator's order preserved
and the missing members inserted at their canonical positions]`

## 12. Relations (the smallest typed mechanism)

```text
requires              a CONDITION for meaningful use (predicates,
                      never bare flag-name pairs) [LANDED inf-2 —
                      the DRY/Mirostat/dynatemp/adaptive/XTC/
                      speculative/custom-template families]
mutually_exclusive    true enum alternatives (the mode values'
                      own exclusivity)
effective_noop        accepted but nullified (temperature 0 → the
                      samplers; chain membership; MIROSTAT ACTIVE →
                      top-k/top-p/typical — the --help's own ignored
                      list, pinned verbatim) [LANDED]
overrides             source-of-truth precedence (the explicit
                      chat-template → model template [LANDED inf-2:
                      the CUSTOM mode emits --chat-template and the
                      compile refuses a half-config LOUDLY])
risk_warning          empirical, environment-specific risk — never
                      a block [CONTRACT — no slice relations; the
                      fit control carries the evidence-tagged note]
affects               affected resources/behavior (VRAM, latency,
                      reproducibility — the explain/benchmark feed)
```

No generic rule engine: relations are TYPED data (Condition /
Requires / EffectiveNoop over the profile values), evidence-pinned
and evaluated by the resolver. Never invent a relation the runtime
evidence or this law does not carry.

## 13. Backend translation and the raw hatch

```text
APPLICATION  the semantic control / profile / resolution
PLATFORM     process management + runtime translation (the typed
             surface: build_server_command owns the flag emission)
ADAPTER      the wire boundary (cli/engine.py, INV-4 — never a
             second transport)
REDOT        presentation (never invokes llama.cpp)
```

The emitted command is a COMPILED ARTIFACT, never the authoring
language. `extra_args` stays the RAW COMPATIBILITY/DEBUG ESCAPE
HATCH (the launch settings store) — never the semantic storage: a
semantic control plus a raw duplicate (`--top-k` in the hatch) is a
CONFLICT refused loudly at the compile step (the platform's
`semantic_flag_tokens` — EVERY owned flag form, off-form and alias,
138 tokens over the full surface), never an ambiguous precedence.
`[LANDED inf-1: _duplicate_flag_ownership + the preview's CONFLICT
surface]` `[LANDED inf-2: build_semantic_command — the platform's
SEMANTIC_FLAG_TABLE (field → flag syntax, emission kind, canonical
order); the application compiles field-keyed values
(`compile_semantic`), the platform validates its own boundary and
refuses unknown fields LOUD; build_server_command stays
byte-stable as the DEPLOYMENT path's own surface]`

## 14. Profile / scenario / recipe / preset / hardware / workspace

```text
PROFILE     reusable semantic configuration (the persisted BASE
            document — inference.json) [LANDED]
SCENARIO    workload/user intent (Long-form, Structured JSON, Low
            VRAM…) [CONTRACT — its own row]
PRESET      a concrete configuration STARTING POINT — applies as a
            TRANSPARENT diff preview, chips stay editable, never an
            opaque "mode" [LANDED inf-2: the four §30 presets
            (general chat / long-form / adaptive / deterministic)
            as TRANSPARENT partial documents — the UI previews every
            field the apply would change, the store validates; a
            preset apply is a plain update, never a mode switch]
RECIPE      a PROCEDURE for finding/evaluating a configuration
            (fit-the-MoE, benchmark staged offload) [CONTRACT]
HARDWARE    the machine description (GPU/RAM/backend) — influences
            SUGGESTIONS and context visibility, never silently
            rewrites the user's configuration [CONTRACT]
WORKSPACE   the user's live state: pinned/active/recent + the
            context-aware library [LANDED inf-2: the PINNED ids
            persist in the profile document's OWN workspace section
            (one file, two named sections — profile + workspace;
            never a second store); the pinned chips are quick-access
            reveals, never second editors]
```

## 15. Context-aware visibility (progressive disclosure)

Not all controls are equally visible. The intended library shape:
PINNED / ACTIVE / RECENT + the CONTEXT-AWARE LIBRARY (a MoE model
raises MoE controls; server mode raises concurrency; vision raises
multimodal). Ordering policy: explicit personal pin → personal
recent/frequent → semantic default order → context relevance —
community popularity is never the primary sort (performance is
hardware/model/workload-dependent). `[LANDED inf-2: the workspace
surface — the pinned quick-access strip, the SEARCH over name/flag/
category (§32's match families), the COLLAPSIBLE categories with
honest counts (the six general-chat categories open by default,
§17's own list), the ADVANCED rung (the expert controls hidden
until asked, a search match shows them — an explicit ask); the
MODEL-DRIVEN context awareness itself stays a CONTRACT row (it
needs the loaded-model facts)]`

## 16. The capability-group ladder (the extension law)

Only after the semantic core is sound do further groups land, each
a named row (never one "advanced parameters" bucket):
DRY/XTC/adaptive/dynamic/Mirostat · CPU/NUMA · KV/cache mechanics ·
MoE placement · loading modes · chat template/reasoning ·
structured output · server/concurrency · observability ·
speculative/lookup decoding · multimodal/embeddings/rerank · LoRA/
control vectors · low-level diagnostics · tools/MCP · legacy
migration. Sampling is ONE subsystem — temperature/top-p UI is not
"the inference architecture".

## 17. Chat integration

Chat carries a COMPACT contextual projection of the same inference
state (profile + effective temperature + the link) — never its own
hidden sampler settings; the full control depth lives in the
Inference workspace. `[LANDED inf-1: the projection row +
Inference under WORK per FRONTEND_UIUX_LAW §2]`

## 18. Observability and benchmark provenance

A run's provenance carries the resolved inference configuration
(the §19.1 EFFECTIVE layer on the run document); benchmark records
preserve the configuration SHAPE (backend/model/quant/seed + ctx/
batch/parallel + placement + KV + the sampler chain + speculative/
template/reasoning state) and measure load/TTFT/tokens-per-second/
VRAM — never a universal good/bad claim attached to a setting (§0's
own law). Inference configuration feeds the Observatory's
context/provenance, never an inference dashboard (the OBSERVATORY
grammar owns its surface).

## 19. Maintenance protocol

At every llama.cpp upgrade: run the actual binary's `--help`;
diff against the registry (the vocabulary sets); detect
new/removed/changed flags; update the semantic overlay ONLY where
needed; re-run the dependency/effective-state tests (the claim
packet's cross-layer vocabulary pins); re-verify the emitted
command's acceptance against the live spawn (an unknown flag
refuses LOUD at the process boundary — the honest failure mode,
never a silent skip). No document outranks the installed binary.

## 20. Anti-patterns (stop on sight)

```text
Settings = a 100+ flag browser          chip = merely a Button
extra_args = the semantic store         temperature = the whole model
all controls equally visible            all controls = "samplers"
preset = an opaque hidden mode          UI = runtime truth
frontend = a direct llama transport     CLI syntax = the authoring language
one universal resolver framework        one giant Settings object
duplicate control definitions           every category = top-level nav
```

## 21. The landed slice and the deferred rows

`[LANDED iter-239 (inf-1)]` — the vertical slice: the control
library (13 controls across 5 categories: Context, GPU Layers
AUTO/all/explicit, Flash Attention, Fit, KV K/V, Temperature,
Top-K, Top-P, Min-P, Penalties, Seed, Chat Template, the ordered
sampler chain), the profile store (+ the schema/1 → schema/2
settings migration), the resolver (deterministic composition, the
evidence-pinned relations), the compiled spawn surface
(build_server_command's additive params), the duplicate-ownership
guard, the gateway family (inference.read/update), the chat BASE
re-point + the REQUESTED/EFFECTIVE pair, the Redot Inference
surface + the Chat projection + the Settings slim, the claim
packet (tests/test_inference.py, 26 tests).

`[LANDED iter-240 (inf-2 — the owner's 2026-09-26 «доделывай
по-человечески + далеко не все сэмплеры и настройки есть» call)]` —
the FULL library + the honest workspace: the 85-control library
over the 15 reviewed categories (the complete sampling surface —
Top-K/P, Min-P, Typical-P, Top-N-Sigma, the penalties family, the
DRY family, the XTC family, the Mirostat family, Dynatemp,
Adaptive-P, Ignore EOS, Logit Bias, Seed — plus the
model/device/memory/loading/moe/cpu/chat-reasoning/structured/
server/observability/speculative/rope/special/lora families), the
typed relations (the mirostat noop from the --help's own words,
the temperature-0 deterministic noop, the family requires, the
chain-family membership concern), the 9-member chain (+ the inf-1
load upgrade), the four §30 presets as transparent diff-previewed
documents, the workspace PINNING (the profile document's own
workspace section), the DATA-DRIVEN Redot workspace (the
preset/search/pinned/collapsible-category/advanced-rung regions —
the editors built from the read document's own metadata; inf-1's
compose-before-read bug — the live flow rendered EMPTY groups —
repaired: the rows build ON the read), the platform compile seam
(build_semantic_command over SEMANTIC_FLAG_TABLE; compile_semantic
field-keyed), the full 138-token duplicate-ownership guard, the
claim packet (tests/test_inference.py, 34 tests + the proof
capture).

Deferred (each a named TASKS row, owner-gated): the session
override layer · capability discovery (§10) · the MODEL-DRIVEN
context awareness (§15's context row) · recent/frequent ordering ·
scenarios/recipes/hardware profiles (§14) · custom preset PERSISTENCE
(the four built-ins landed; saving the operator's own is a row) ·
seed's request scope (the adapter row) · observability feeds (§18's
benchmark shape) · the risk_warning relations (the first consumer).
