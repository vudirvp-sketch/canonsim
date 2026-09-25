# WORKBENCH_APP_LAW.md — The Workbench Application/Runtime Architecture Law

> The owner's 2026-09-25 corpus re-homing call (D-218, iter-237) over the
> external `CANONSIM_WORKBENCH_APPLICATION_ARCHITECTURE_V5_2.md` — the app
> spec. Per the D-024/D-200 law the external brief is NEVER vendored; THIS
> file is the repo-side binding distillation. **The spec's §-numbering is
> preserved 1:1** — every existing `app §N` reference in CONTRACTS/TASKS/
> STATUS/NAV resolves HERE without edits.
>
> **Routing law:** every Workbench application/runtime question —
> operations, lifecycles, identity, deadlines, streaming, persistence,
> inference policy, gateway semantics, shutdown, boundedness — routes HERE
> first. Interaction/UI → `docs/FRONTEND_UIUX_LAW.md` (D-214); visual
> tokens/chrome → `docs/VISUAL_SYSTEM_UI.md` (D-211); world presentation /
> Scene IR / assets → `docs/WORLD_PRESENTATION_LAW.md` (D-218); Observatory
> analytical semantics → `docs/OBSERVATORY_LAW.md` (D-218); engine facts →
> `docs/REDOT_ENGINE_INDEX.md` (D-207). `AGENTS.md`, active `STATUS.md`,
> CanonSim owning specs and `docs/DECISIONS.md` remain HIGHER authority.
>
> **Honesty law:** each section carries its CURRENT state —
> `[LANDED iter-N]` (implemented + tested), `[PARTIAL …]`, or
> `[CONTRACT …]` (binding on the named future row, not yet implemented).
> Documentation is not implementation (D-218's audit law).

## 0. Scope and consolidation rule

This law keeps the concrete architecture load — owners, contracts, state
vocabularies, identities, lifecycles, persistence, inference, external
control, provenance, recovery, tests — and drops history/repetition.

```text
CanonSim core = canonical simulation semantics/events/fold/doors
Workbench app = operations/runtime/identity/lifecycle/persistence/inference/gateway
Frontend companion = UX/UI/Redot/Visual Scene IR/assets/visual validation
OBSERVATORY = rebuildable analytical evidence over canonical runs
PRESENTATION_SPEC = model-facing CanonSim presentation/serialization
```

Redot is a presentation/runtime implementation detail, never a semantic
owner. The single shared seam with the frontend is §23.

## 1. Product boundary

ONE product/frontend — not `Workbench.exe + Game.exe`, not a second
simulator, not a wrapper around a parallel semantic engine. Primary
surfaces: Models, Inference, Prompts, Chat, History, Diagnostics,
Simulation, Settings/Appearance, Runs/Jobs, GUI, CLI/batch,
persistence/recovery, inbound control. Future optional edges: TTS, STT,
translation, additional inference backends.

```text
clients: GUI | CLI | local client | mobile web | agent
→ Workbench gateway → application operations → domain/execution/stores
→ CanonSim semantic seam | backend adapter → cli/engine.py (INV-4) | LLM backend
```

## 2. Authority hierarchy and responsibility ownership

```text
AGENTS.md / repo invariants → CanonSim owning specs + decisions + roadmap
+ tests → THIS LAW ↕ the frontend companions → external/research/style evidence
```

Single-owner examples (a consumer may USE another owner's contract; it
may not silently BECOME the owner): canonical world/events/fold →
CanonSim, never Workbench/UI · application operations/policy →
`workbench/application`, never widgets/CLI/gateway · llama wire/protocol
→ `cli/engine.py` under INV-4 (a later adapter extraction only by
one-owner move), never UI · prompt/profile/history/session stores → the
respective persistence owner, never ViewModels · inbound
transport/schema/auth → `workbench/api/gateway`, never feature code ·
ordered stream delivery → the execution/`api/streaming` edge, never
widgets · process mechanics → `workbench/platform`, never application
policy · visual/UI policy → the frontend companions, never
application/domain · cache → the local owning feature/store, never a
global registry. (The spec's `domain`/`features` skeletons are
design-only — §5.)

### 2.1 No God Object

No one manager for window/tabs/models/inference/prompts/history/
persistence/logging/CanonSim/theme/networking. A coordinator is justified
only by a bounded real lifecycle or application operation; a proposed
abstraction must identify ONE responsibility, owned state/lifecycle, a
concrete consumer/problem, and a test/falsifier — otherwise the
responsibility stays local.

## 3. Canonical/semantic boundary

CanonSim stays sole owner of canonical truth (`canonical event log →
fold/projections → semantic products`). Workbench never creates a second
world model, canonical log, semantic validator, brief builder, parser
authority or truth store; LLM output is candidate data until it crosses
the existing validation seam. State/authority classes stay distinct:

```text
CANONICAL = semantic truth        CONFIGURATION = user-owned durable behavior
SESSION = restorable working context    WIDGET = ephemeral local interaction
RUNTIME = live process/model/execution/resource state
OBSERVATION = source/revision/freshness evidence
HISTORY = operational indexed record    OBSERVATORY = rebuildable analytical evidence
CACHE = rebuildable acceleration       BACKUP = explicit recovery artifact
```

Consequential evidence may carry `CANONICAL | OBSERVED | DERIVED |
INFERRED | MODEL_CLAIM | HYPOTHETICAL | STALE | UNKNOWN | CONFLICT |
HIDDEN | PRESENTATION`. Never infer absence from omission; never
silently upgrade authority.

## 4. Runtime topology, host and exposure modes

```text
HOST = DESKTOP | HEADLESS_SERVER    EXPOSURE = LOOPBACK | LAN | TUNNEL
BACKEND = ATTACHED | MANAGED        OBSERVE = MINIMAL | STANDARD | DEV
```

Public exposure is never implicit; LAN/remote control is opt-in and
authenticated through a private/tunneled or explicitly configured
boundary. GUI/CLI/mobile/agent clients all resolve to the SAME
application operations.

### 4.1 The network boundaries — INV-4's landed form

The repo's standing form (AGENTS §4 owns the law): THREE sanctioned
modules — the OUTBOUND engine adapter `cli/engine.py` (D-193), the
INBOUND gateway binding `workbench/api/transport.py` (D-201: loopback
hosts only; non-loopback refuses to start without auth, executable at
construction `[LANDED wb-4]`), and the OUTBOUND model-assets fetch
`workbench/platform/model_fetch.py` (D-208: HTTP GET downloads into the
§16 MODELS_ASSETS root only). The gateway owns protocol/schema/auth/
session translation only — never backend transport, persistence
internals or CanonSim internals. No generic RPC framework, event bus,
plugin ABI, service locator, DI container or separate agent runtime is
implied or admitted.

## 5. Package/feature shape — design skeleton, not a mandate

```text
workbench/
├─ application/{operations, identity, artifact, directories, clock, settings}
├─ api/{contract, gateway, transport}          # + streaming (§13, future)
├─ platform/{llama_process, model_fetch}
└─ presentation/redot/                          # the frontend companion's own
```

The spec's `domain/`, `features/`, `persistence/`, `adapters/llama_cpp/`
skeletons remain DESIGN-ONLY: physical modules earn existence through
independent state/lifecycle, persistence, external protocol, tests or
meaningful change locality — directories are created when they acquire a
real owner/consumer, never as architecture theatre (the landed tree is
the proof: `application/operations` + `platform/` + `api/` exist;
`domain/`/`features/` do not, and nothing misses them).

## 6. Dependency direction

```text
views/ViewModels → presentation + feature-local presentation
→ application operations → domain contracts
adapters/persistence/platform/integrations → implement/serve application/domain contracts
```

### 6.1 Composition Root contract `[LANDED wb-5/wb-7 — composition.py + scripts/workbench_app.py]`

The composition root is the SINGLE wiring owner: construct → validate
dependencies → wire owners → start lifecycle. Not a service locator,
not a global registry, not a god object, not a hidden injector.
Concrete dependency selection is visible at the composition boundary;
feature/domain/application code depends on contracts, not on the root;
tests may build smaller compositions explicitly; a dependency that
exists only because the root can create it is not justified.

### 6.2 Feature ownership map

Every user-facing feature has ONE state/operation owner; presentation
projects that state, never competes with it:

| Feature | Owns | Must not own |
|---|---|---|
| Models | discovery/selection flow + presentation state | backend wire, canonical truth |
| Inference | inference configuration flow | sampler wire quirks, transport |
| Chat | conversation interaction flow | CanonSim semantics, execution transport |
| History | query/navigation/read presentation | canonical event log, backend state |
| Diagnostics | diagnostic presentation/filtering | semantic truth, secrets |
| Simulation | simulation controls/read presentation | world rules, fold, semantic time |
| Settings/Appearance | preferences + workspace presentation | runtime ownership, hidden defaults |
| Runs/Jobs | long-running operation presentation | retry semantics, execution lifecycle |

A feature may own local ephemeral state ONLY when it has no application
semantic meaning. Forbidden direct edges: `domain → features/presentation/
CLI/concrete adapter` · `features → backend process control / another
feature's private state` · `presentation → llama transport / CanonSim
internals / persistence internals` · `api/gateway → backend transport /
CanonSim / persistence internals` · `streaming → canonical execution
store` · `persistence → CanonSim truth` · `UI → direct world mutation`.

## 7. Data, configuration and state

- **7.1 Configuration** (user-owned durable behavior): model/inference
  profiles, sampler presets, prompt profiles, theme/font/density/
  language/accessibility preferences, model-directory selection, backup
  policy. **7.2 Session** (restorable context): open/selected tabs,
  selected model, simulation pack/seed, conversation, history filters,
  meaningful panel/layout state. **7.3 Widget-local**: `hover | focus |
  cursor | drag | temporary expansion | animation phase | pre-commit
  local edit | transient selection`. **7.4 Runtime**: `backend process |
  loaded model | execution | stream buffer | cancellation handle |
  workers | admission slots`. **7.5 Cache**: model metadata,
  compatibility checks, token counts, capability discovery, history
  indexes, read-model fragments, render-prepared content, translation
  lookups — every entry has identity/dependencies, a validity rule and
  a rebuild path; no global `everything` cache; cache is never the sole
  copy of user data.

### 7.6 Snapshot / checkpoint / artifact / cache — never interchangeable

```text
SESSION SNAPSHOT      = restorable Workbench working context
SIMULATION CHECKPOINT = CanonSim-defined reproducible simulation position
EXECUTION ARTIFACT    = immutable record of one operation/run + material inputs/outcome
VISUAL CACHE          = rebuildable presentation acceleration artifact
```

A session snapshot MUST NOT present itself as a simulation checkpoint; a
visual cache MUST be disposable without changing canonical or durable
state; an execution artifact is not a replacement for CanonSim's
canonical log; Workbench may REFERENCE checkpoint semantics but never
invent them.

## 8. External gateway/API contract `[LANDED wb-4 — api/contract.py + gateway.py]`

HTTP/SSE/WebSocket are delivery mechanisms; the semantic API is
application operations. Families: `session.create/get/attach/detach/
events`, `run.start/get/cancel/stream`, `chat.send`, `prompt.test/
prompt.compare` `[CONTRACT]`, `execution.get/replay` `[CONTRACT]`,
`model.list/inspect/load/unload` `[LANDED]`, `simulation.start/step/
stop` `[CONTRACT]`, `history.query/get` `[CONTRACT]`, `diagnostics.get/
export` `[CONTRACT]`, `observatory.runs/read` `[LANDED obs-2]`. The
analytical family (`observatory.query | compare | profile | archaeology
| calibrate`) stays owner-gated capability FAMILIES — OBSERVATORY_LAW
owns their semantics. Mutations use `client_request_id` idempotency
keys; mutable sessions use expected revision; exclusive control uses a
short-lived lease token; long-running work returns identity immediately.
Event envelope: `event_id | session_id | operation_id/execution_id |
sequence | event_type | observed_at | payload`. Minimum rejection/
failure distinctions (the landed closed vocabulary): `AUTH_FAILED |
AUTHZ_DENIED | DUPLICATE_REQUEST | STALE_REVISION | LEASE_EXPIRED |
DOMAIN_REJECTED | RUNTIME_FAILED | SENT_OUTCOME_UNKNOWN`.

### 8.1 Tool/MCP authority `[CONTRACT — no consumer yet]`

```text
model proposes tool call → parse/bound → capability check
→ permission/authz → application operation → result
```

A model-emitted tool name/arguments are INERT data until explicitly
authorized; tool execution cannot bypass the application/semantic seam.

## 9. Identity closure `[LANDED wb-3 — application/identity.py]`

Path is location, NOT identity: `logical_name + revision/version +
strong content identity + relevant schema/metadata identity = material
identity`. Multi-file/sharded/multimodal assets use deterministic
composite identity over all material constituents. Distinguish
`logical_name`, `revision/version`, `content_digest`, `location`,
`metadata`:

```text
same path + new bytes     → new content identity
same name + new revision  → new revision identity
same revision + new bytes → identity mismatch; never silently reuse
```

Size/mtime/platform fingerprints are cheap SCAN screens, never
correctness identity. Failed/incomplete strong hashing is explicit
(`INTEGRITY_UNKNOWN`); `recheck()` makes the mismatch law executable:
`VERIFIED | MISMATCH | INTEGRITY_UNKNOWN` — never a quiet pass.

## 10. Immutable execution artifact + provenance `[LANDED wb-3 — application/artifact.py]`

Before side effects, freeze all materially relevant run inputs:

```text
execution_id/operation_id · model identity + content identity
pack/schema identity where relevant · prompt identity + frozen material inputs
resolved inference configuration · backend/runtime/build/protocol identity
capability snapshot · serialized request identity/digest · seed/deterministic inputs
tool-authority state where relevant · terminal result/status + relevant diagnostics
```

Existing engine/CanonSim provenance stays authoritative for its fields;
Workbench extends/references it — never a competing duplicate schema.
Reproducibility scopes: `EXACT_BITWISE | SEMANTIC | APPROXIMATE |
EXPLANATORY_ONLY`. Keep separate: canonical reproducibility (same
canonical inputs → same canonical replay) · request reproducibility
(same immutable request inputs → same serialized request) · inference
reproducibility (request + declared model/backend/runtime conditions).
Prompt text ALONE is insufficient when templates, special tokens,
grammar, tokenizer metadata, seed or runtime configuration can differ.
Replay = a NEW execution identity.

### 10.1 Capability snapshot

`backend capability → normalized capability → product control policy →
widget`. Capability discovery never auto-generates controls; if
capability data materially influences a run, the observed snapshot is
immutable run provenance. `[LANDED in the wb-6 props-probe form:
evidence, not gate]`

### 10.2 Observatory analytical run identity `[CONTRACT — OBSERVATORY_LAW §2 owns the full form]`

Workbench owns the analytical-run lifecycle and artifact identity;
CanonSim owns canonical simulation meaning. Analytical projections are
rebuildable from CanonSim JSONL + declared metadata; no analytical store
becomes canonical truth.

## 11. Application/backend/model/execution lifecycles `[LANDED wb-5 — operations/lifecycles.py; the FAILED_SHUTDOWN + process-loss UNKNOWN branches resolved]`

Four DISTINCT state machines (contract vocabularies, not
one-class-per-state):

```text
Application: STARTING → READY → DEGRADED → STOPPING → STOPPED
Backend: ABSENT → STARTING → PROBING → READY → BUSY → STOPPING → STOPPED
         ↘ FAILED ↔ RECOVERING
Model: DISCOVERED → VALIDATED → SELECTED → LOADING → LOADED → ACTIVE
       ↘ FAILED;  ACTIVE → UNLOADING → EVICTED
Execution: ADMITTED → STARTING → RUNNING → COMPLETING → COMPLETED
           ↘ FAILED;  ↘ CANCEL_REQUESTED → CANCELED | FAILED_TO_CANCEL | UNKNOWN
```

Each has one owner, legal-transition tables, terminal semantics (the
empty successor set) and invalid-transition loudness.

### 11.1 Backend process ownership `[LANDED wb-8/wb-9 — platform/llama_process.py + the MANAGED default]`

Application/runtime owns lifecycle POLICY; `platform/` owns OS MECHANICS
(spawn, termination, handles, stdio, exit observation); the adapter owns
backend PROTOCOL. `ATTACHED`: observe readiness/health/exit, no implicit
start/stop/restart, the backend may disappear independently. `MANAGED`:
readiness/health/exit observation, bounded graceful stop (TERM →
deadline → kill with the OBSERVED exit code), force-stop only under
explicit policy/deadline. Replacement: `prepare new → validate → ready →
swap → retire old`; on failed replacement preserve the known-good
runtime when possible.

## 12. Operation identity, deadlines, retry and cancellation `[LANDED wb-4/wb-5 — execution.py]`

One logical operation owns ONE absolute deadline on the monotonic clock;
lower layers receive remaining budget only. `OperationContext =
operation_id + started_monotonic + deadline_monotonic + cancellation`.
Per-attempt socket timeout is transport policy, NOT a new logical
deadline; `tries × timeout_s` is invalid.

### 12.1 Dispatch outcome

```text
NOT_SENT             → retry may be permitted within remaining budget
SENT_AND_TERMINAL    → return the known result
SENT_OUTCOME_UNKNOWN → NO blind retry
```

Retry after `SENT_OUTCOME_UNKNOWN` requires strong backend
idempotency/deduplication evidence; otherwise UNKNOWN is the truthful
terminal state. A mutating raise after admission is SENT_OUTCOME_UNKNOWN;
a read raise is RUNTIME_FAILED.

### 12.2 Idempotency / stale control

Stable mutation identity prevents duplicate semantic effects across
GUI/CLI/API retry; idempotency does NOT replace semantic validation,
lease or stale-revision checks.

### 12.3 Cancellation truth

Cancellation is a state transition: `CANCEL_REQUESTED → CANCELED |
FAILED_TO_CANCEL | UNKNOWN`. Never claim completion because a stop
button was pressed. Late results are rejected by operation/execution
identity and current revision; they cannot mutate newer state.

## 13. Streaming, bounded buffers and reconnect `[CONTRACT — the live-events row]`

```text
backend stream → bounded execution buffer → immutable execution record
→ ordered session events → clients
```

Canonical execution data is never silently dropped; derived presentation
deltas may coalesce/drop. Overflow is bounded and observable; if
complete output cannot be preserved, record partial/truncated semantics
instead of pretending completeness. Reconnect: `reconnect(last_sequence)
→ replay retained ordered events OR RESYNC_REQUIRED + bounded current
snapshot`. Identity/order stay stable; a client disconnect never
implicitly cancels unrelated execution. SSE is the default one-way event
direction; WebSocket only for a concrete bidirectional need.

## 14. Resource admission `[CONTRACT]`

Before mutable runtime transitions resolve relevant limits: `CPU | RAM |
VRAM | context budget | active model slots | queue capacity | stream
buffers | other explicit resources`. Allowed result vocabulary:
`ACCEPT | QUEUE | REJECT | EVICT | RELOAD`. Admission cannot half-apply
a rejected transition or hide pressure behind infinite retries.

## 15. Persistence ownership `[PARTIAL — settings.py's atomic schema-tagged store landed wb-9; the rest CONTRACT]`

```text
CanonSim JSONL = canonical truth (INV-1)   Workbench history = indexed operational/user data
config/session = user-owned durable state  cache = rebuildable   backup = explicit recovery artifact
```

When indexed history is actually required, the first local candidate is
stdlib `sqlite3` — no universal ORM/repository abstraction before a
second backend/concurrency case exists. Each durable store declares:
`schema identity/version | logical writer | transaction boundary |
atomic commit rule | recovery role | future-version behavior |
backup/restore scope`.

- **15.1 Save/backup**: `edited state → serialize → temporary artifact →
  flush/close → atomic replace → optional backup rotation`. Distinguish
  `manual save | autosave | atomic write | backup | restore | export`.
  Backup policy: `enabled | max_count | max_age | before_migration |
  before_destructive_change`. Failures: cache → rebuild; backup → visible
  diagnostic; config corruption → preserve evidence + explicit recovery.
- **15.2 Stale-writer protection**: `loaded revision → edit → atomic
  compare-and-swap commit → COMMITTED | STALE_WRITER`. Compare+write is
  ONE atomic store operation (CAS-equivalent); separate
  read/compare/write is insufficient. Conflict disposition: `RELOAD |
  MERGE | REJECT`. No speculative MVCC/CRDT layer.
- **15.3 Schema evolution**: bounded migrations per store; unsupported
  future versions are never silently downgraded/emptied/defaulted;
  migration failure preserves the original artifact and emits a
  diagnostic.
- **15.4 Cross-store crash recovery**: stores are not one distributed
  transaction. Recovery roles: `AUTHORITATIVE (never invent source data)
  | REBUILDABLE (regenerate from authoritative data) | RECONCILABLE
  (temporary inconsistency has deterministic repair)`. Crash between
  related commits reconciles via durable identity/revision evidence.
  ViewModels never perform recovery.

## 16. Runtime/data-directory contract `[LANDED wb-3 — application/directories.py]`

Production paths are explicit and `.git`/CWD independent: application/
runtime, user configuration, user data/history, models/assets, cache,
backups, logs/diagnostics. The seven path roles + the absolute-root law
+ the startup/recovery outcome vocabulary (missing, read-only,
permission-denied, corrupt, partially migrated, externally removed) are
executable in `directories.py`. Upgrade/migration must cover missing
runtime/backend executable, native-library mismatch, model-directory
failure, schema incompatibility, failed recovery.

## 17. Clock contract `[LANDED wb-3 — application/clock.py]`

```text
CanonSim semantic time → simulation meaning/determinism
monotonic clock        → deadline/timeout/retry/duration
UTC/wall observation   → display/persistence timestamps where needed
UI animation time      → visual only
```

MONOTONIC + UTC_WALL provided injectably; SEMANTIC/UI_ANIMATION
named-only. No wall clock ever enters CanonSim deterministic state,
canonical replay or request identity; zero clock imports in the artifact
layer.

## 18. Prompt ownership and reproducibility `[CONTRACT — the Prompts row]`

Prompt roles: `system | user/chat | narrator | summarizer |
parser/structured-output | CanonSim-specific`. Sources: `built-in |
profile | session override | call-local override` where the semantic
owner permits. Editable prompt UI is NOT permission to alter semantics
owned by `BRIEF_SPEC`, `PARSER_SPEC`, `PRESENTATION_SPEC` or another
owner. Material prompt inputs are frozen per execution; a mutable
profile name alone is insufficient for reproducibility.

### 18.1 Simulation Pack identity and compatibility `[CONTRACT — the CanonSim seam row]`

A Simulation Pack is a content/provenance input, not a filesystem
folder: `logical_pack_id + pack_revision + schema_identity +
content_identity + compatibility + location`. Execution provenance
consuming a pack records at minimum `pack_identity + pack_schema_identity
+ seed + source_revision where material`. Rules: `logical_pack_id`
identifies the logical pack; `pack_revision` the intended revision;
`content_identity` closes the ACTUAL material content; a path alone is
never pack identity; schema incompatibility is a VALIDATION result, not
a missing-file condition; re-running with the same visible pack name but
different content must not masquerade as the same reproducibility input.
The application may discover/validate/select a pack; CanonSim remains
owner of pack semantics.

## 19. Inference and sampler policy `[PARTIAL — inf-1: the semantic inference-control layer landed; docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md owns the llama.cpp chip architecture]`

Backend-specific flags, server defaults and wire quirks stay in the
adapter; generic Workbench types stay backend-neutral. §19.1 is the
contract. **Settings ≠ Inference Control (inf-1):** the launch-
settings store owns DEPLOYMENT only; the inference profile store
(`workbench/application/inference.py`) owns the semantic
generation-control values — the llama.cpp chip model, its scopes,
the sampler chain and the effective-state resolver route through
LLAMA_CPP_INFERENCE_CONTROL_LAW FIRST, never a restatement here. Build-sensitive sampler surfaces (temperature, top-k, top-p,
min-p, top-n-sigma, typical-p, XTC, DRY, repetition/presence/frequency
penalties, dynamic temperature, adaptive-p, Mirostat, sampler ordering)
are FRESHNESS EVIDENCE, not a frozen list — re-verify the pinned build
before implementation. Basic/Advanced/Expert are disclosure layers, not
semantic classes. Preset data requires `id | name | backend
compatibility | parameter values | optional sampler order | description
| schema/version` and must not silently modify out-of-scope settings.

### 19.1 Inference profile composition and effective-state closure

A named profile is a source of REQUESTED values, never proof of runtime
state. Composition is explicit:

```text
BASE PROFILE → SESSION OVERRIDE → CALL-LOCAL OVERRIDE
→ VALIDATION/CLAMP → BACKEND RESOLUTION → OBSERVATION
```

Persist/diagnose as separate layers where material: `REQUESTED = what
the caller asked for · ACCEPTED = what the contract accepted ·
EFFECTIVE = resolved values for execution · OBSERVED = what the
backend/runtime showed · PRESENTED = what the UI currently shows`. A UI
control MUST NOT overwrite `EFFECTIVE` merely because its widget value
differs; backend defaults, clamps, unsupported parameters and sampler
ordering stay observable when they materially change behaviour.
`[LANDED wb-9: chat.send's absent-temperature default resolves from
the BASE layer; the explicit value wins. LANDED inf-1: the BASE
layer is the inference profile's resolver — the run document
carries the REQUESTED/EFFECTIVE pair; the composition chain itself
stays THIS section's own law]`

## 20. Model discovery and loading `[LANDED wb-5..wb-11 — models.py/backend.py/model_fetch.py + the shell circuits]`

```text
discover → inspect → select → resolve configuration → validate
compatibility/capabilities → prepare backend → load → observe ready
→ expose active model
```

`file exists ≠ valid ≠ selected ≠ loading ≠ loaded ≠ active`. Cheap
size/mtime scans screen routine refresh; strong identity is computed
when needed (`inspect`'s fresh §9 identity; `digest_work` the one real
work kind with §12 checkpoints between chunks). Build-specific llama.cpp
router/`/props`/`/slots` findings remain research evidence and must be
re-verified. `model.load`/`model.unload` are RUNS (the wb-11 wire shape:
the execution document returns immediately, the terminal truth rides
`run.get`, FAILED diagnostics carry the observed cause); the single-slot
+ in-flight admission guards hold; the DISPATCH-LOCK regression
(model.list answers while a gated load stands in the port call) is
pinned by test. Arrival: URL fetch (D-208, HTTP GET only) + local
import (the native picker → `model.import`, a local copy with live
progress, NO network).

## 21. History and diagnostics `[CONTRACT — the History/Diagnostics rows; the honesty landed in the shell]`

```text
persistent history → bounded query/page → read model
→ frontend mapping → virtualized renderer
```

Never instantiate every historical message as a permanently live UI
node; selected records fetch detail on demand; history rows and
executions link via immutable IDs. Diagnostics explain WHAT was
attempted, WHAT happened, WHY. The structured diagnostic envelope:
`observation time | source/component | operation/execution ID | severity
| code/category | human message | structured context | redaction status
| related resource identity`. Observation profiles: `MINIMAL =
operational evidence | STANDARD = normal diagnostics | DEV = explicitly
enabled deep bounded evidence`. DEV may retain bounded raw
prompt/response/backend evidence for calibration when permitted;
credentials, tokens, secrets and secret-bearing headers NEVER enter
ordinary diagnostics; raw evidence needs explicit size/lifetime/
redaction/export policy.

## 22. CLI/batch parity `[PARTIAL — workbench_app/workbench_launch are the CLI forms]`

CLI/batch is a delivery surface over application operations. Console
output is bounded, stable enough for operators/automation,
machine-readable where required, secret-free, explicit about terminal
state. A `.bat`/launcher may select runtime paths but must not embed a
second backend client or semantics implementation.

## 23. Shared seam with the frontend companion

### 23.1 Redot runtime contract `[LANDED — CONTRACTS D1/D2 + REDOT_ENGINE_INDEX own the details]`

Redot 26.2 LTS (`redot-26.2-stable`) pinned; project root
`workbench/presentation/redot/`; GDScript; Compatibility renderer for
the measured 2D/2.5D slice; CLI automation `--path`/`--headless`; the
engine binary OUTSIDE the git tree (the launcher owns the resolution
chain, wb-9/wb-10). No application/domain module imports Redot classes,
resource paths, SceneTree or engine lifecycle objects. Redot 26.3+ are
research/compatibility targets only until separately admitted
(ENGINE_INDEX §20.1 the gate).

```text
application operation / ordered event → typed semantic read model
→ ViewModel only when presentation derivation is real
→ UI state and/or Visual Scene IR → Redot controls/sprites/compositor
```

Application owner: operations, domain semantics, identity, lifecycle,
inference, persistence, recovery, gateway/authz, backend boundaries.
Frontend owner: UX/human factors, navigation, tokens/components,
accessibility, Redot, ViewModels, Scene IR, camera/composition/assets/
LOD/cache/effects, screenshots/regression/usability. The frontend may
derive presentation data but cannot mutate application semantics; there
is no generic "presentation super-layer".

## 24. CanonSim vertical seam `[LANDED read-side — wb-1 scene_build + obs-2 observatory_read]`

The first serious simulation slice proves: `Workbench intent → the
shared CanonSim application/semantic seam → the existing parser/action/
door/validation path where applicable → the canonical event path → the
existing consequence/read-side projection → the typed Workbench read
model → the frontend surface`. Never duplicate CanonSim pack parsing,
canonical validation, folding, world truth or semantic time. The
read-side edge is `core.log` imports ONLY (the render/chronicle
pattern); the operations package stays CanonSim-free per its dependency
envelope — the seam's one home per family (scene_build.py /
observatory_read.py).

## 25. Shutdown/process-loss contract `[PARTIAL — the launcher's two-child shutdown + lifecycles' FAILED_SHUTDOWN]`

```text
STOPPING → stop new work → signal owned runtimes → bounded graceful period
→ force-stop only under explicit policy/deadline → observe the actual outcome
→ flush required state → STOPPED | FAILED_SHUTDOWN
```

ATTACHED backends are not silently terminated by Workbench shutdown.
Backend loss during execution yields truthful terminal/unknown state and
preserves evidence.

## 26. Boundedness/performance contract `[CONTRACT]`

"Bounded" requires an explicit ceiling AND a degradation policy. Before
production acceptance define ceilings for: cold/warm startup, model
discovery, history first-page/pagination, pending operations per class,
stream buffer/update cadence, diagnostics export size/duration,
graceful/forced shutdown, in-memory history materialisation, runtime
resource usage. Frontend CPU/GPU/VRAM budgets belong to the companions
(FRONTEND_UIUX_LAW §20 + WORLD_PRESENTATION_LAW §12).

## 27. Dependency admission `[ABSORBED into AGENTS §2.8 — the standing law: real consumer → demonstrated problem/risk → smallest typed seam → licence/runtime envelope → mechanical verification; no future-proofing; runtime deps and offline content tooling separate; no generic framework without a concrete consumer]`

## 28. Research and decision discipline `[ABSORBED into AGENTS §11 + D-198: problem → current mechanism → alternatives → real consumer → falsifiable discriminating test → realized result → disposition; claims FACT|INFERENCE|HYPOTHESIS|PROPOSAL|UNKNOWN; dispositions CONFIRMED|PARTIALLY_CONFIRMED|REJECTED|UNRESOLVED|DEFERRED; never promote build-sensitive observations into generic law]`

## 29. Adapter contract tests `[PARTIAL — test_engine over the stub server]`

Every backend/platform adapter crossing an application boundary carries
executable contract tests for the behaviour the application relies on:
`capability discovery/normalisation · request serialization + identity
propagation · backend defaults/clamps/unsupported fields · error and
timeout mapping · cancellation propagation + truthful terminality ·
stream ordering/terminal event semantics · reconnect/resync where
supported · model lifecycle and replacement · backend disconnect/crash ·
SENT_OUTCOME_UNKNOWN handling · secret/redaction boundaries`. Adapter
tests prove the typed application contract against the concrete backend;
they are not implementation snapshots.

### 29b. The required failure matrix

| Failure | Required observation | Default disposition |
|---|---|---|
| backend unavailable | `FAILED/UNAVAILABLE` | bounded retry if allowed |
| startup timeout | `FAILED/STARTUP_TIMEOUT` | terminal; no hidden loop |
| malformed response | `FAILED/MALFORMED` | fail; retry only with evidence |
| protocol failure | `FAILED/PROTOCOL` | contract-defined retry |
| stream disconnect | `UNKNOWN` or confirmed terminal | bounded reconnect if safe |
| cancellation race | truthful terminal state | never fabricate canceled |
| late result | stale/discarded | diagnostics only |
| same-path replacement | identity mismatch | refresh/reject |
| stale writer | explicit conflict | reload/merge/reject |
| interrupted write | prior valid/recovery artifact | never silently empty |
| future schema | `UNSUPPORTED_VERSION` | preserve original |
| backup exhaustion | visible failure | no false durability claim |
| backend crash during run | terminal/unknown | preserve evidence |
| shutdown deadline | forced stop/failed shutdown | record actual outcome |

A boundary is recovery-ready only when its relevant rows have executable
tests.

## 30. Verification before abstraction promotion

The durable proof set (checked = LANDED and test-pinned; the rest ride
their named rows):

```text
[x] fixed operation deadline across retries        [x] ambiguous post-dispatch result → UNKNOWN unless safe idempotency
[x] NOT_SENT retry consumes remaining deadline     [x] ATTACHED not silently terminated/restarted
[x] MANAGED replacement = prepare/validate/swap/retire (the _ManagedBackend policy)
[ ] atomic stale-writer CAS prevents overwrite     [x] immutable execution artifact closes material run inputs
[x] composite identity changes when a shard changes [ ] canonical stream data never silently drops (the streaming row)
[ ] resource admission cannot half-apply rejection [ ] crash-between-stores follows declared recovery roles
[ ] tool call inert without capability/permission  [x] duplicate mutation with same identity → one effect
[x] stale revision/expired lease cannot mutate newer state
[x] reconnect continues order or emits RESYNC_REQUIRED (the gateway session events)
[ ] client disconnect does not cancel unrelated work [ ] DEV observation never serializes credentials
[x] non-loopback exposure cannot start without auth [x] GUI/CLI/API share operation semantics
[x] no second outbound LLM transport owner (INV-4)  [x] composition root the only wiring owner, no service locator
[ ] feature ownership map: one owner per consequential state (the features skeleton stays unlanded)
[x] session snapshot / checkpoint / artifact / cache stay distinct (§7.6's vocabulary)
[ ] simulation pack identity includes logical id/revision/schema/content (the CanonSim seam row)
[ ] inference profile composition closure testable  [x] adapter contract tests (serialization/capabilities/errors/cancellation)
[x] architecture tests catch forbidden dependency edges
```

## 31. Agent-friendly change locality `[ABSORBED into AGENT_NAVIGATION — the map layer]`

For any feature an agent quickly locates: `application operation |
state owner | persistence owner | feature/view | adapter/integration
edge | owning tests`. Every material boundary exposes: `OWNER | INPUT |
IDENTITY | CONTRACT | BOUNDS | AUTHORITY | PROGRESS/TERMINALITY |
OBSERVATION | FAILURE/RECOVERY | IDEMPOTENCY/REVISION/LEASE |
CLIENT/TRANSPORT | TEST`. ViewModel is optional — only for real
presentation-specific derivation/local state.

## 32. Implementation order (dependency logic, not backlog)

```text
 1 identity + execution artifact + directories + clock + envelope      [LANDED wb-3]
 2 lifecycle + ATTACHED/MANAGED + deadline/retry/ambiguity + admission [wb-5/8; §14 admission CONTRACT]
 3 persistence CAS + recovery roles + migrations + fault tests         [CONTRACT]
 4 one outbound LLM owner + one inbound gateway                        [LANDED D-193/D-201]
 5 minimal application operations + typed API contract                 [LANDED wb-4/wb-5]
 6 live events + reconnect/resync + idempotency/revision/lease tests   [CONTRACT]
 7 capability-aware inference/configuration + model identity/loading   [LANDED wb-6..wb-10]
 8 persistence foundations + provenance closure                        [PARTIAL]
 9 thin Observatory substrate + run manifests + bounded World Question [PARTIAL — obs-1/obs-2 the slice + the read seam]
10 frontend theme/primitives + Chat/Models/Inference                   [LANDED Chat/Models/Settings]
11 Diagnostics/History + CLI parity + reproducibility inspection       [CONTRACT]
12 CanonSim seam + placeholder world                                   [LANDED read-side; the intent-side row CONTRACT]
13 Visual Scene IR + deterministic visual proof                        [LANDED wb-1/wb-2]
14 reusable asset vocabulary + maps/inventory/journal                  [CONTRACT — WORLD_PRESENTATION_LAW]
15 visual/LLM concurrency optimization                                 [CONTRACT]
16 optional TTS/STT/translation/backends                               [not started]
```

This is dependency logic; the ORDER stays the owner's call (TASKS the
queue owner; FRONTEND_UIUX_LAW §25 the frontend ladder).

## 33. Non-negotiable checklist

```text
[ ] one responsibility owner; no God Object            [x] CanonSim sole canonical authority
[x] one outbound LLM transport owner (INV-4)           [x] one inbound gateway over application operations
[x] GUI/CLI/API share operation semantics              [x] strong + composite content identity
[x] immutable execution artifact when material         [x] explicit application/backend/model/execution lifecycles
[x] ATTACHED/MANAGED ownership explicit                [x] monotonic single deadline; retry cannot extend it
[x] UNKNOWN after ambiguous dispatch                   [x] truthful cancellation; safe late-result rejection
[ ] bounded streaming; ordered reconnect/resync        [ ] explicit resource admission
[ ] atomic stale-writer CAS                            [ ] store schema/migration/recovery/backup contracts
[ ] cross-store recovery roles                         [x] runtime/data paths .git/CWD independent
[x] clock domains separated                            [ ] secrets excluded from ordinary diagnostics
[x] non-loopback exposure explicit/authenticated       [ ] tool calls inert until capability/permission
[ ] prompts remain under their semantic owner          [x] requested/effective/observed distinction preserved
[x] configuration/session/widget/runtime/cache distinct[x] history/read surfaces bounded
[x] no speculative generic framework layers            [x] relevant failure/architecture tests executable
[x] feature change locality agent-understandable       [x] Observatory artifacts derived/rebuildable
[ ] analytical runs close run/pack/seed/arm/environment provenance (OBSERVATORY_LAW §2)
[x] World Question outputs expose evidence, scope, uncertainty, next discriminator (the obs surface)
```

## 34. Final architecture

```text
                         CANONSIM
                 canonical events / fold
                           │
                  semantic/application seam
                           │
                  WORKBENCH APPLICATION
        ┌──────────────────┼───────────────────┐
    operations         persistence          adapters
        │                  │                   │
    gateway/CLI       history/session      LLM backend
    API clients       profiles/backups          │
        └──────────────────┼───────────────────┘
                    typed read models
                           │
                FRONTEND / VISUAL COMPANION
                    ViewModel / Scene IR
                           │
                         REDOT
```

CanonSim decides canonical meaning/world change; the Workbench
application decides safe operations, lifecycle, persistence, inference
and external control; the frontend companion decides how results become
understandable and visual; Redot presents without becoming a second
simulator.
