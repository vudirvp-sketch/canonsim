# FRONTEND_WEB_LAW.md — The Web Frontend Implementation Law

> The owner's 2026-09-29 delivery: the external
> `CANONSIM_FRONTEND_WEB_AGENT_PACK_FINAL` v1.3 (the tmpfiles upload),
> admitted by the «выполняй» ingestion call — iter-288, D-243. Per the
> D-024/D-200/D-214 law the external pack is NEVER vendored as live
> docs: the verbatim original is preserved at
> `docs/frontendweb/archive/` (md5-pinned, never re-ingested); THIS
> file is the repo-side binding distillation of the pack's normative
> web contracts (the pack's own stack decision content revision v1.7).
> The pack's routing law rides here: **active repo binding law >
> current implementation/tests > the pack's derived web contract >
> historical source-workbench > Redot reference.**
>
> **Routing law:** every web-frontend (React/browser client)
> implementation question routes HERE first — the stack decision's
> active half, the S0 skeleton gate, the gateway seam, dual-read,
> connection budget/stream admission, browser runtime bounds, surface
> modules, the web-side effective-state closure, analytical UX
> projection, visual proof, the tooling floor. Interaction/IA/
> accessibility → `FRONTEND_UIUX_LAW.md`; visual tokens/state matrix →
> `VISUAL_SYSTEM_UI.md`; application/runtime ownership →
> `WORKBENCH_APP_LAW.md`; Observatory semantics → `OBSERVATORY_LAW.md`;
> Scene IR/world presentation → `WORLD_PRESENTATION_LAW.md`; inference
> control semantics → `LLAMA_CPP_INFERENCE_CONTROL_LAW.md`.
> **Scope fence:** the Redot-freeze half of the pack's stack
> decision LANDED as D-244 (the owner's 2026-09-29 «redot
> замораживаем» call), then CLOSED by DELETION at iter-290/D-245
> (the owner's 2026-09-29 «удаляй redot» call — the tree, its
> engine index, its proof/contract packets, and the Setup launcher
> removed; the launcher re-pointed to the web dev server, the
> pack's §16 gate discharged by the deletion itself — a frozen
> target no longer exists; recovery: git history + the verbatim
> pack at `docs/frontendweb/archive/`). This law now
> binds the ACTIVE web client at `frontend/` (frontend-1, the S0
> gate §2).

## 0. Status

- Active path (the pack's DECIDED claim, recorded as the web track's
  direction): **React + TypeScript + Vite, Web/PWA-first; Tauri 2
  optional and deferred; DOM/CSS for ordinary chrome; Canvas/WebGL
  only where scene workload requires it.**
- Landed (iter-289, D-244): the `frontend/` tree exists — the S0
  walking skeleton (React + TS + Vite), and the `frontend-1` build
  row is discharged. The pre-D-244 "not yet in repo" snapshot lines
  were retired with this landing (the verbatim pack record stays at
  `docs/frontendweb/archive/`, never re-ingested).
- Core rule (the pack's §1): semantics stay in CanonSim/Python;
  presentation and interaction stay downstream, typed, replaceable,
  non-authoritative. The React client is never a second simulator,
  canonical-state authority, event-log authority, hidden rules
  engine, or LLM semantic authority.
- INV-4: the browser dials the EXISTING inbound loopback gateway
  binding (`workbench/api/transport.py`, `POST /op`) — a gateway
  client like the Redot shell before it, NOT a fourth network
  surface. No new network module, no engine client anywhere.
- The browser is an **untrusted presentation client** (§15): the
  backend validates every semantic capability; the frontend improves
  UX, never widens authority. Never trust browser state, URL
  parameters, local storage, imported assets, client-side capability
  claims, model output, or client-computed semantic results.

## 1. Authority precedence + snapshot honesty

```text
ACTIVE REPO BINDING LAW
  > current executable implementation/tests
  > this distilled web law (the pack's derived contract)
  > selected historical Workbench source (source-workbench/ V5.2)
  > Redot reference
```

- The pack's ground-truth pin is a dirty working-tree checkpoint
  (iter-269..272 @ `cd84069`, 131 status entries) — its
  repo-ground-truth/ tree is pinned evidence, never a substitute for
  the live repository (verified zero-diff against HEAD `ae2fa3d` at
  ingestion, iter-288).
- Do not describe browser SSE/WebSocket as already implemented; do
  not treat `source-workbench/` as the current architectural owner
  when an active `docs/*_LAW.md` covers the same concern.
- If an active owner and this law disagree, stop at the seam, name
  the exact contradiction, and update this law before implementing.

## 2. Phase gate — Skeleton S0 (the primary gate until green)

A minimal React + TS + Vite client over the existing loopback
gateway, proving multi-tab and large-list behaviour, and measuring
cost next to a live sim/LLM — ~1–2 weeks of focused work. **During
S0, agents MUST NOT expand into the full ACCEPTANCE_MATRIX, the V5.2
source trees, SSE implementation, a surface registry, a layout
manifest, or Redot parity.** Those gates open only after S0 is green.

| # | Criterion |
|---|---|
| S0-1 | One Vite + React + TS app, single composition root; a typed `POST /op` client; every payload enters as `unknown` and is runtime-validated before UI use; ≥1 successful op round-trip AND ≥1 honest UNKNOWN/rejection path in UI; no raw `fetch` JSON into components; no second envelope; no browser-side semantics |
| S0-2 | A Trajectory (or equivalent) surface renders ordered evidence from `session.events`; virtualization or an explicit hard window — UI usable at **≥ 10,000** appended events (scroll, select by semantic id, no full-tree mount); cursor is semantic id/sequence, never row index; the view is labelled **live session tail** (volatile), never durable history |
| S0-3 | Two browser tabs act as **independent** gateway clients (no shared mutable semantic store; no `localStorage`/`BroadcastChannel` as truth); concurrent behaviour documented; **NO SSE/WebSocket in S0** — `POST /op` only (poll/explicit refresh allowed, must show STALE/freshness); a third+ tab must not silently corrupt state — degradation may be coarse but must be truthful |
| S0-4 | With simulation and/or a local LLM active on the Python side, record rough numbers: interaction feel, tab memory, scene/WebGL off by default (feature flag `scene=off`); a short markdown note, no perf lab |

Out of scope for S0 (exact list): SSE/WebSocket; layout manifest /
surface registry; the full Observatory compare/graph suite; PWA
offline package; Tauri; Redot changes or deletion; reading
source-workbench V5.2 for implementation detail; closing the full
ACCEPTANCE_MATRIX; JSON-Schema-driven settings UI; dependency-cruiser
CI (recommended immediately after S0, never blocking S0 green).

Dual-read reminder (even in S0): `session.events`/live tail →
volatile, sequenced, resync — label LIVE; durable logs/artifacts →
Observatory history — not required in S0 UI. Never present the live
tail as the full durable Trajectory.

Pass: S0-1..S0-4 evidenced (demo or short notes + tests where
cheap). Agent discipline: (1) prefer this gate over the full matrix
until green; (2) never invent gateway routes; (3) no visual-system /
V5.2 polish in S0; (4) one PR theme at a time — client shell →
trajectory virtualized → multi-tab note → load note.

## 3. The gateway seam (POST /op)

| Seam | Law |
|---|---|
| Gateway | the semantic entry is `POST /op`; RequestEnvelope / ResponseDocument / EventEnvelope; closed vocabularies and unknown-key rejection are backend-owned; the browser consumes typed/validated adapters — raw JSON never reaches components |
| Session stream | `session.events` is the ordered per-session replay surface; retained sequence + `RESYNC_REQUIRED` semantics are existing backend law; browser transport for future SSE/WebSocket is NOT landed and must be separately admitted/tested; the client isolates transport adapters so surfaces never hard-code POST-only assumptions beyond the typed client API |
| Execution | long-running work already has execution identity, deadline, cancellation, progress; ambiguous post-dispatch results remain UNKNOWN; cancellation is never visually treated as completed merely because a request was sent |
| Provenance | execution artifacts freeze material inputs/identities and may carry capability/runtime/model/protocol/reproducibility information; replay creates a NEW execution identity, lineage via `replay_of` |
| Observatory | the read-side already supports bounded run listing and bounded event windows; event ids are the semantic cursor/selection identities; NO DATA / NO MATCH / stale cursor / corrupt log are distinct observations; Trajectory is a presentation of the same evidence class, never a second store |
| Scene | Visual Scene IR is renderer-neutral; scene composition identity stays distinct from canonical semantic identity; asset identity/provenance is presentation metadata, never canonical truth |
| Effective state | see §8 |
| Model/resource | a selected model is not necessarily loaded or active — preserve discovery/validation/selection/loading/loaded/active/failure/eviction and `ACCEPT/QUEUE/REJECT/EVICT/RELOAD` where exposed |
| Reproduction | replay uses a new execution identity; material packs are not identified by path/display label alone — preserve logical/revision/schema/content/compatibility identity where exposed |
| Multi-tab | each browser tab is an independent gateway client; cross-tab channels (if any) are non-authoritative UX hints only; browser storage is never the operation log or effective-state authority (§6) |

## 4. Dual-read law (LIVE ≠ HISTORY)

Two different evidence worlds; the UI must never merge them into one
silent cursor.

| | LIVE session tail | DURABLE history |
|---|---|---|
| Source | gateway `session.events` (or equivalent ordered live surface) | Observatory read-side over committed logs (`logs/*.jsonl`), execution artifacts, provenance |
| Properties | volatile, FIFO/retention-limited, sequenced, `RESYNC_REQUIRED` | durable, queryable, bounded pages, pack/run identity |
| UI label | LIVE / SESSION | HISTORY / ARCHIVE |
| Use | current-run progress, live Trajectory tail, reconnect | past runs, full Trajectory across sessions, replay lineage |

Rules: (1) a Trajectory surface reading only the live tail is
titled/labelled as live session evidence, never "all history";
(2) cross-run Trajectory requires durable Observatory read models —
never an ever-growing client buffer of `session.events`; (3) cursors,
selection ids, and load-more tokens are never mixed across LIVE and
HISTORY without an explicit mode switch; (4) FIFO eviction in the
live tail is not canon loss — durable logs remain the historical
authority.

## 5. Connection budget & stream admission

Facts: HTTP/1.1 browsers allow ~six concurrent connections per
origin; the gateway transport is loopback HTTP
(ThreadingHTTPServer-class), not automatically HTTP/2; N tabs each
holding a long-lived stream can exhaust the budget and stall further
tabs.

1. No unbounded streams (one SSE/EventSource per tab × many tabs)
   without an admission policy.
2. `connection budget exhausted` is a FIRST-CLASS failure class,
   distinct from `transport unavailable`, `stream disconnect`, and
   `stale / resync required` — never rendered as "gateway dead".
3. Defaults before HTTP/2 or server-side fan-out: **focused-tab
   stream** (only the focused tab holds a live stream; background
   tabs poll / show last-known snapshot / explicit refresh + STALE),
   or a documented cap (1–2 live streams per origin); POST-only is
   always valid and is the S0 mandate.
4. SharedWorker / Service Worker must NOT become a hidden stream
   multiplexer owning semantics or a second event bus;
   packaging-only shared transport requires its own gateway contract
   and tests — never an agent improvisation.
5. Auth material never appears in stream URLs.

Admission order (never skip ahead; never implement 2–4 during S0):

```text
1. POST /op only (landed; S0)
2. explicit gateway contract for a one-way stream (SSE or
   fetch-stream) + tests
   [LANDED iter-305 — the backend first: GET /events over
   workbench/api/{gateway,transport}.py, WORKBENCH_APP_LAW §13's
   landed form; the frame vocabulary + the byte parity +
   boundedness are tested in tests/test_sse_stream.py]
3. browser adapter behind the typed gateway client (NOT landed —
   its own row: the EventSource/fetch-stream adapter, the zod frame
   validators, the focused-tab reconnection policy)
4. focused-tab / budget policy enforced in UI (rides 3)
5. HTTP/2 or server fan-out only on measured need
6. WebSocket only for a concrete bidirectional requirement
```

## 6. Browser runtime bounds

Tab model: modern browsers isolate tabs; each tab is an independent
client — no shared in-memory React state across tabs, no elected
"leader tab" owning semantics (semantics stay on the Python
gateway). Optional cross-tab UX ("already open", badges) may use
`BroadcastChannel` ONLY for non-authoritative hints.

| Forbidden | Allowed |
|---|---|
| `localStorage`/`sessionStorage` as operation log or effective-state store | per-tab gateway client + validated session sequence |
| `BroadcastChannel` as second event/command bus | `BroadcastChannel` for UX hints only |
| SharedWorker as hidden semantic authority | PWA cache for static assets + explicit offline shells |
| Service-Worker cache as canonical run/result store | |
| optimistic multi-tab writes without a gateway round-trip | |

Rendering split: DOM/CSS → ordinary Workbench chrome, forms, lists,
inspectors; Canvas/WebGL → world/scene only when the Scene IR
workload requires it. Hard rules: (1) never permanently materialize
unbounded history as a live React tree — virtualize/window/
progressive-fetch (activate at order 10³+); (2) read models are
bounded queries over application evidence, never full-log mirrors;
(3) animation respects reduced-motion + the declared interaction
cost budget — prefer passive updates on evidence arrival over
polling storms; (4) heavy scene surfaces single-instance per user
intent (warn or reuse, never silently N WebGL contexts); (5) cache
keys include revision/identity — cache miss ≠ data loss, stale
cache ≠ effective state. Targets: shell input→paint < 100ms;
stable lower FPS over unbounded quality spikes; bounded diagnostic
logs with redaction. **Measure before optimizing; no WebWorkers or
WebGPU "because scale".**

PWA/offline (when shipped): static shell may cache, semantic
authority never; offline shows last-known presentation with explicit
STALE/DISCONNECTED — never silent success; updates never wipe
in-flight operation identity without a recovery path; incompatible
asset/shell update is the first-class failure class `incompatible
PWA update`.

## 7. Surface modules

Material UI areas mount as surface modules under ONE composition
root. Shape:

```text
surfaces/<surface_id>/
  index (mount API)
  state matrix (honest UI states)
  adapters (typed gateway client usage only)
  components (presentation)
  tests / fixtures / proof hooks
```

Required metadata: `surface_id`, owner, gateway ops/read models
consumed, local presentation state only (explicit), honest state
matrix, entry routes/commands. Allowed local state: draft form
fields; UI open/closed/tab/scroll restore; pending optimistic
markers (must reconcile); non-authoritative view preferences.
Forbidden inside a surface: canonical event log; retry/deadline/
idempotency policy; second transport or event bus; raw network JSON
into components; model load/evict policy; admission policy; pack
identity invention from path alone. Mounting: one composition root;
code-splitting via dynamic import is packaging, not semantics;
shared selection/context strips are shared facilities, never one
surface's hidden globals. Extension checklist (before adding a
surface): confirm the read-side/gateway ops already expose the
evidence (or land the backend first); declare the state matrix
including empty/stale/failed/partial; wire only through the gateway
client + validators; add contract tests for UNKNOWN/cancel/
rejection; add visual proof hooks if material; update the transfer/
acceptance docs only if a NEW capability class is introduced.
Recommended first-class surfaces (as read-side/ops support them):
Shell/navigation, Models, Settings, Chat/control, Observatory,
Trajectory, Chronicle/world, Diagnostics.

## 8. Effective-state closure (web side)

For material controls and consequential operations, keep the stages
distinct — they may coincide, they are never assumed equivalent:

```text
REQUESTED → ACCEPTED/REJECTED → EFFECTIVE → OBSERVED → PRESENTED
```

Forbidden collapses: `input.value === EFFECTIVE`; `click ===
success`; `selected === loaded`; `profile label === execution
identity`; `HTTP 200 === semantic success`; `tab local state ===
shared truth across tabs`. The frontend mirrors application
evidence; it never promotes a draft or optimistic projection into
semantic truth.

Composition path (settings/inference controls — the application
owns it): `BASE PROFILE → SESSION OVERRIDE → CALL-LOCAL OVERRIDE →
VALIDATION/CLAMP/NORMALIZATION → EFFECTIVE CONTROL STATE → OBSERVED
RUNTIME STATE → PRESENTATION`. The UI may edit the first three
layers per the exposed contract; it never silently replaces the
effective-state calculation. A control with `AUTO`, an explicit
value, `DISABLED`, or `INEFFECTIVE` renders the state and reason
supplied by the application — never inferred from the widget value.

Model lifecycle is not one boolean: `DISCOVERED → VALIDATED →
SELECTED → LOADING → LOADED → ACTIVE → UNLOADING/EVICTED → FAILED`
(a file on disk proves nothing; SELECTED must not claim LOADED).
Resource admission where exposed: `ACCEPT | QUEUE | REJECT | EVICT |
RELOAD` — the browser reports the owner-provided reason and
recoverable action, it never decides admission policy. Prompt/input
ownership: material inputs freeze at the execution boundary; a later
UI edit never retroactively rewrites a created execution's effective
inputs. Pack identity: `logical_pack_id + pack_revision +
schema_identity + content_identity + compatibility` — path/URL is a
locator, never identity.

## 9. Analytical UX (the web projection)

Role line: `CONTEXT → QUERY/SCOPE → PRIMARY VIEW → INSPECTOR →
EVIDENCE/PROVENANCE`. Shared selection: one canonical typed identity
drives cross-highlighting — never row index, display text, or local
widget ids. Context strip: at minimum run/execution identity,
scope/time, seed where relevant, observation profile, revision,
freshness for high-consequence surfaces. Semantic navigation:
scope → target → evidence → source, Back/Forward preserved. Compare:
BASE/PERTURBED share semantic/time coordinates; differences anchored
to identity/time, not color alone. Semantic zoom: aggregation
changes, semantic identity never silently changes. Trajectory: an
ordered read-only projection of session events + execution
identities + admissions/cancellations + `replay_of` lineage — cursor
is semantic id/sequence; search is a bounded read-side query, never
a second log; fork/replay always requests a NEW execution identity;
Trajectory never mutates canon. Empty-state grammar: `NO DATA ≠ NO
MATCH ≠ NO EVIDENCE ≠ UNKNOWN ≠ OUT OF SCOPE ≠ BLOCKED ≠ PARTIAL ≠
STALE ≠ FAILED`. Evidence strength is independent of graphical
adjacency or generated prose. Multi-surface coordination (Observatory/
Trajectory/Inspector/Chronicle) shares selection identity + gateway
evidence — never a private cross-surface event bus.

## 10. Visual proof & degradation

Proof classes stay distinct: `STATIC_VERIFIED / RUNTIME_VERIFIED /
TASK_VERIFIED / VISUAL_VERIFIED / MANUALLY_VERIFIED / DEFERRED /
NOT_VERIFIED`; a screenshot is visual evidence, never semantic
proof; runtime-unavailable is never reported as runtime-pass.
Screenshot artifacts (where useful) carry build identity,
surface/state identity, fixture/seed, revision/compatibility
identity, bounded debug metadata. Scene: Visual Scene IR is
renderer-neutral, typed, non-authoritative; composition identity
includes semantic/read input identity, seed, composition policy
version, Scene IR schema identity, asset-manifest identity where
applicable. Assets: logical identity + revision/content identity;
invalid/stale/incompatible assets fail visibly or degrade safely —
asset paths/URLs are not semantic identity. Camera: semantic focus/
target ≠ presentation camera ≠ user camera state. Boundedness: no
unbounded history tree, stream buffer, graph, scene allocation, or
asset cache. Degradation ladder: missing asset → placeholder/
diagnostic; stale scene → rebuild/refresh; backend loss → preserve
local UI state + show unavailable; render failure ≠ semantic
failure. Every material surface declares its honest state matrix
(`EMPTY / LOADING/DISCOVERING / ACTIVE/RESOLVED / STALE/DEGRADED /
FAILED` as applicable) — a missing state is an explicit gap, never
an invitation for a generic spinner/error. The active visual owner
is `docs/VISUAL_SYSTEM_UI.md`.

## 11. Tooling floor (post-S0 recommendation, then mandatory)

- Deterministic `typecheck` + unit/contract tests for the gateway
  client.
- Dependency boundary check (eslint-boundaries / dependency-cruiser):
  components never import raw transport/fetch.
- Runtime validators (zod/valibot-class) with types derived from or
  checked against Python contract fixtures — never hand-retyped in
  isolation.
- Virtualization proof for large event/run lists.
- Playwright-class smoke: multi-tab independent clients, reconnect/
  STALE path, UNKNOWN outcome path.
- Frontend CI is ADDITIVE — it never replaces the Python CI (ruff +
  pytest stay the semantic verification; the web checks are a new
  layer).

## 12. The transfer matrix (mandatory rows)

The pack's full TRANSFER_MATRIX.md carries the complete set
(owner-gated rows included); the mandatory core: composition root/
ownership law; typed gateway contract + runtime validation;
operation/execution identity preserved; deadlines/cancellation/
terminality rendered truthfully (never reimplemented); execution
artifact/provenance read-only; session sequence/replay/
RESYNC_REQUIRED as the client reconnect adapter; the context
identity strip; the evidence ladder/epistemic grammar; empty-state
distinctions; Scene IR renderer-neutrality; screenshot-driven
development; static/runtime/task proof separation; graceful
degradation/boundedness; requested→effective closure; model
lifecycle; prompt/profile composition; simulation pack identity;
surface module boundaries; multi-tab independent clients; gateway
client transport isolation; bounded list virtualization;
harness-quality failure presentation; dual-read; connection budget/
focused-tab policy; the S0 gate before the full matrix.

## 13. Non-goals / standing refusals

Redot↔React feature parity; pixel parity with the Redot UI; a
separate native mobile UI; Electron; moving CanonSim semantics into
the browser; browser-side model inference by default; WebGPU before
measured need; a large generic visualization DSL; a mandatory global
state-management framework; a mandatory UI/component framework;
rebuilding the backend to make the frontend "cleaner"; porting
DeepSeek Harness/Cordis/dsh runtimes (import the quality bar only);
a client-authored trajectory/event log diverging from gateway
`session.events`; multi-tab leader election or browser storage as
semantic authority. Plus the pack's critical rules: do not implement
SSE/WebSocket before the gateway contract + connection policy;
never create a second execution engine, event bus, or truth
authority in React; each tab is an independent gateway client; the
live repository remains authoritative over this law's snapshot.

## 14. The migration sequence (all phases owner-gated)

```text
Phase 0 — freeze Redot + archive cleanly (DONE — D-244 the freeze,
          D-245 the owner's «удаляй redot» deletion: the tree removed,
          the launcher re-pointed to the web dev server; recovery:
          git history)
Phase 1 — re-home the laws (Redot → historical/reference-only)
Phase 2 — frontend foundation (the S0-class client: shell, typed
          gateway client, runtime validation, state models, design
          tokens, harnesses, locked reproducible build)
Phase 3 — Workbench vertical slice (shell/nav, connection state,
          Chat/Inference, Settings, Observatory entry, lifecycle/
          error/reconnect)
Phase 4 — simulation + world (run/session surfaces, Scene IR, the
          web scene renderer, deterministic fixtures + visual proofs)
Phase 5 — remote/PWA (mobile, install/update, secure remote
          transport, reconnect, degraded/offline honesty)
Phase 6 — optional Tauri 2 (thin shell, web stays fully functional)
```

The final agent rule (the pack's, binding): build forward only on
React + TS + Vite + Web/PWA-first; treat Redot as deleted history
(D-245 — the reference material lives in git history and the
archived pack); preserve CanonSim, the Workbench
application/gateway, typed contracts, renderer-neutral Visual Scene
IR, execution/provenance identity, and read-side analytical
contracts as the stable backbone; never create a second semantic
authority, second transport/server, or parallel frontend product;
treat the browser as untrusted and validate every wire payload at
the gateway-client boundary; route conflicts through
`docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md` §7's owner map.
