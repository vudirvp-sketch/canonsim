# CanonSim Workbench — the web client (frontend-1)

The ACTIVE frontend path (D-244: the owner's 2026-09-29 freeze+open
call; the Redot tree deleted at D-245 — the owner's «удаляй redot»
call). React + TypeScript + Vite, Web/PWA-first — the S0 walking
skeleton over the existing loopback gateway, now grown into
Phase 3's seven rows (the Shell + the Session lifecycle; the
Observatory HISTORY entry — the dual-read law's second world; the
Settings CONFIG entry — the §8 closure over a real persisted store;
the CHAT entry — the conversation world over the run family; the
INFERENCE entry — the generation-control workspace over the profile
store; the MODELS entry — the model family's mirror: discovery,
arrival, the §20 load ladder; the SETTINGS SECONDARY NAV — the
surface's own sections over real documents: Deployment | About) +
the IA REPAIR (iter-297, D-247: the product/diagnostic registry
split — a vertical product rail + the subdued Diagnostics entry,
FRONTEND_UIUX_LAW §2.1's navigation contract) + THE STREAM
TRANSPORT (iter-306: the streaming admission's steps 3+4 — the
EventSource adapter behind the typed client, the focused-tab
budget policy, the dual-transport Trajectory feed).
The law: `docs/FRONTEND_WEB_LAW.md` (the S0 gate §2; the stream
admission §5; the entry surface
`docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md`).

## What this is (and is not)

- **Is**: one presentation client of the Workbench gateway — typed,
  runtime-validated at the client boundary, replaceable,
  non-authoritative. The browser is an untrusted downstream client.
- **Is not**: a second simulator, event-log authority, rules engine,
  or LLM semantic authority. POST `/op` remains the always-valid
  transport; the SSE stream (iter-306) rides the landed GET
  `/events` gateway contract (iter-305) — never a second event
  source (the frames are the SAME bytes `session.events` replays).
  No browser storage as truth; each tab is an independent gateway
  client — and only the focused tab holds a live stream.

## Run it

The zero-command form: double-click **`Workbench.bat`** at the repo
root (D-245: the launcher starts the gateway + this dev server
together, installs on the first run, and opens the browser) — or
`python scripts/workbench_launch.py` from the repo root. By hand:

1. Start the Python gateway (the repo root):

   ```
   python scripts/workbench_app.py            # binds 127.0.0.1:8765
   python scripts/workbench_launch.py --no-frontend   # the same, launcher form
   ```

2. Start the dev server (this directory):

   ```
   npm install
   npm run dev        # http://localhost:5173
   ```

   The Vite dev server proxies `/gateway/*` to `127.0.0.1:8765`
   (`vite.config.ts`): the browser stays same-origin; the gateway
   itself is untouched (no CORS surface added to the backend — the
   production serving path is a post-S0 concern). A custom gateway
   port: `GATEWAY_TARGET=http://127.0.0.1:9000 npm run dev`.

## Verify

```
npm run typecheck   # tsc --noEmit
npm test            # vitest run (unit + contract + integration + architecture)
npm run build       # typecheck + the production build
npm run e2e         # the Playwright multi-tab smoke (iter-309) — over the REAL
                    # composition: boots the gateway (--no-backend, port 8788)
                    # + this dev server itself; first run needs
                    # `npx playwright install chromium`
```

The e2e smoke (FRONTEND_WEB_LAW §11's Playwright-class row, the
iter-308 browser drive's template made committed): two tabs two
independent sessions (each strip LIVE at boot — the boot-time
OBSERVED-sync), the focused-tab stream policy over a live wire (a
blurred tab's connection really closes, the refocus re-dials), live
push without refresh, and the UNKNOWN outcome path (the mid-flight
attach cut + the user's explicit retry). It is deliberately NOT a
CI job (the owner's row spec: the additive CI lane runs tsc +
vitest + build only); the smoke runs owner-side/sandbox — `npm run
e2e` from this directory. Two environment facts the config pins:
Vite exits on stdin-close unless `CI="true"` (its own interop
flag), and binds `::1` only without `--host 127.0.0.1`.

The architecture guard (`tests/architecture/guard.test.ts`) is the
tooling floor's first landed row (FRONTEND_WEB_LAW §11's
dependency-boundary check, the backend `test_architecture.py`'s
parity form): it enforces, as executable law — fetch ONLY in the
typed gateway client (the one transport adapter); EventSource ONLY
in the stream adapter (`api/gateway/stream.ts`, iter-306 — the
admitted step 3 landing over the iter-305 contract; XMLHttpRequest/
WebSocket/serviceWorker still forbidden everywhere — every further
transport opens only through its own gateway contract + admission);
no browser storage as
truth (localStorage/sessionStorage/BroadcastChannel/indexedDB/
caches); `src/api/**` imports nothing upward; no cross-feature
imports; features couple to state only via `import type`; one
composition root; src never imports tests; **V1 — the visual floor
(iter-297): no raw color literals outside the `:root` token set**
(a color is a named token, never a hex in a rule — VISUAL_SYSTEM_UI
§2/§3; the scan caught and closed a standing 9-literal violation);
**V2 — the dimension floor (iter-304): no raw font-size (px/rem),
font-family stack, numeric font-weight, or border-radius px outside
`:root`** (VISUAL_SYSTEM_UI §2.1/§2.2 — the seven-step type scale
`--font-micro/meta/compact/body/heading/heading-l/heading-xl`, the
`--font-body-family`/`--font-mono` stacks, `--weight-strong`,
`--tracking-label`, and `--radius-s/m/l/pill`; em ratios stay legal
as contextual metrics; the scan's mutation check catches all three
violation classes); **V3 — the spacing floor (iter-307): no raw
px/rem in any padding/margin/gap declaration outside `:root`**
(VISUAL_SYSTEM_UI §1.1/§2.1 — the ten-step spacing scale
`--space-1..10` (2/4/6/8/10/12/16/20/32/48px) consolidating the
seventeen organic values across the 131 layout-affecting
declarations; max drift 2px, 119/149 usages exact; 0 and auto stay
literal — the zero/auto semantics; em/% ratios stay legal; the
scan's mutation check catches all three violation classes). A
violation is a red
test naming the file and line — never silent drift. The heavier
instruments named by the law: the Playwright-class multi-tab smoke
LANDED (iter-309 — `tests/e2e/`, `npm run e2e`); dependency-cruiser /
eslint-boundaries stay parked rows, each its own admission
(AGENTS §2.8: the existing suite first — until the import graph
outgrows the guard test).

The contract tests run against the committed fixtures
(`tests/fixtures/*.json`) — captured from the live gateway code
(in-process dispatch, the parity law's byte form; `manifest.json`
the provenance). Regenerate with the iter-289 capture notes (the
sandbox-side capture script lives outside the repo per AGENTS §7
Rule 9; the fixtures' shape is the contract, the capture is
re-runnable from `tests/test_gateway.py`'s own patterns).

## The surfaces (the rail era — Phase 3 rows 1–6 + the IA repair)

The composition root mounts the **Shell** (`src/features/shell/`)
with the SPLIT registries (iter-297, D-247 — FRONTEND_UIUX_LAW
§2.1): `ProductRoute` (the rail's only content: Chat at the HEAD,
the Inference control workspace right behind it, the Models
resource right behind the AI family, Trajectory LIVE, Observatory
HISTORY, Settings pinned at the rail's end) and `DiagnosticSurface`
(behind ONE subdued Diagnostics entry, its own secondary nav inside
the workspace — Session lifecycle / Gateway / Load probe, the proof
instruments, never product peers). The rail is a navigation
instrument, never a feature directory: a first-class surface is not
automatically a navigation item.

**Only the active surface mounts** —
a switch unmounts the previous surface and drops its local
presentation state (a live-tail buffer, a probe list); the
gateway remains the only truth, and a remounted surface re-reads
its evidence — possibly via RESYNC, never silently. The active
focus is the shell's allowed local UI state (§7's allowance).

The product routes (the rail):

| Surface | What it proves |
|---|---|
| Session (lifecycle) | the lease closure over the existing ops: attach under the CAS revision guard, detach under the lease guard — REQUESTED → ACCEPTED/REJECTED → EFFECTIVE → OBSERVED, never collapsed; STALE_REVISION/LEASE_EXPIRED verbatim with the gateway's own reason; G4 — no auto-retry, a fresh `client_request_id` per explicit attempt |
| Gateway (status) | the `app.status` round-trip + the honest rejection probes (DOMAIN_REJECTED / STALE_REVISION / DUPLICATE_REQUEST) — the DELIVERED/TRANSPORT/MISMATCH lanes never collapse |
| Load probe | drives real `session.attach` ops (the CAS loop) — the S0-4 measurement instrument; with a model loaded the measurement runs alongside a live llama-server (iter-302: ≈108–110 ops/s, the S0-4 criterion literally met) |
| Trajectory | the LIVE session tail — DUAL-TRANSPORT (iter-306): the SSE stream feed (the default) or the POST poll ladder (1s/2s/5s/off — S0's mandate, always valid, the stream's own fallback; the buffer survives the switch — one evidence world, two transports): virtualized ≥10k rows (only the window mounts), the semantic-sequence cursor, event-id selection, RESYNC_REQUIRED handled honestly (the stream lane performs the SAME one-POST recovery the poll lane applies, then re-begins from the reconciled cursor), the LIVE label (volatile tail, never durable history); the stream phase line (IDLE/CONNECTING/OPEN/PAUSED/RESYNC/REJECTED/FAILED) + the honest transport notes verbatim |
| Chat | the conversation world (`chat.send` → `run.get` → `run.cancel` + the header's `model.list`/`model.states` + the `inference.read` compact projection): every turn an honest RUN — the admission answer is STARTING (never the completion), the bounded 700ms observation loop (dead at terminal/TRANSPORT/unmount, the re-poll explicit), the transcript per-surface VOLATILE (chat history is not canon — unmount drops it like every surface's local buffer), the REQUESTED/EFFECTIVE provenance line per turn, the near-bottom follow law, the call-local overrides explicitly surfaced (never hidden samplers), the messages-context rule (only admitted turns + completed replies ride the next send), every lane verbatim (FAILED with the observed diagnostics; CANCELED/FAILED_TO_CANCEL as the terminal truth past a cancel); the COMPLETED band CLOSED LIVE (iter-302: a real reply + provenance over a sandbox llama.cpp — the transcript + screenshots in the report) |
| Models | the model family's mirror (`model.list`/`model.states` + `model.load`/`model.unload` + `run.start` over model.fetch/model.import/model.digest, observed via `run.get`/`run.cancel`): the §20 ladder law rendered — the row's chip is `model.states`'s OWN answer per name (a discovered file proves nothing: discovered ≠ selected ≠ loading ≠ active), the ACTIVE slot is the load-state owner's, MISSING ≠ EMPTY ≠ NO MODELS rendered distinct; the arrival pane (the fetch form — the admission gate fires BEFORE any network over the pure-string normalize law; the import form's honest web shape — ABSOLUTE paths as text, the native file/folder picker the Tauri row's own standing concern); the §9 strong-identity affordance as the digest RUN (the honest long arm for a multi-GB file — cancellable and observable; the synchronous `model.inspect` stays a backend surface, never a frozen UI); every dispatch a RUN with a fresh idempotency key (G4), ONE run at a time, the bounded observation dead at terminal/TRANSPORT/unmount, and exactly ONE context re-read at the terminal (the OBSERVED baseline — the landed file rides the NEXT discovery scan, the ladder rests at its own truth), never polling; the honest disabled gates (FAILED is terminal — no re-selection; unload only while ACTIVE; everything off without a session) |
| Inference | the generation-control WORKSPACE (`inference.read` + `inference.update` — the full control depth, never Chat's compact projection): the §21.2 regions — the preset row (a TRANSPARENT diff preview BEFORE the apply, the apply a plain update guarded on a CLEAN draft), the search over name/flag/category (a match is an explicit ask — it shows the advanced rows), the pinned quick-access strip (reveals, never second editors; a pin/unpin its own dispatch over the workspace section), the collapsible categories with honest counts (the six general-chat families open by default), the advanced rung, the ordered 9-member sampler chain (membership a DRAFT edit — the Save carries the WHOLE document, never a partial edit), the compiled preview read-only; the editors are DATA-DRIVEN over the read document's own value_type/forms/limits metadata (the UI never re-encodes the vocabulary — a new control lands by the server's document alone); every row renders the OBSERVED state + the resolver's reasons verbatim (configured-but-ineffective stays VISIBLE) + the §4 defaults ladder (baseline · upstream side by side); §8's closure over the persisted profile store — the Save sends ONLY the changed keys with a fresh idempotency key (G4), on ACCEPTED the returned document is the new OBSERVED baseline (the draft reconciles to the SERVER's answer), `applies: next-spawn` verbatim, no polling |
| Observatory | the HISTORY world (`observatory.runs`/`observatory.read`): the dual-read law's second half — the discovery scan, ONE bounded window at a time (the event-id cursor, `next_after` forward pagination that REPLACES the window, never an accumulating buffer), the context strip's identity line (seed/pack/CANON_VIEW/CANONICAL), event-id selection over the SAME document, NO DATA ≠ NO MATCH ≠ stale cursor ≠ TRANSPORT rendered distinct, no polling (durable evidence; every read explicit) |
| Settings | the CONFIG world with its own secondary navigation (iter-301 — Deployment \| About, real content only): **Deployment** (`backend.settings`/`backend.settings.update`): the §8 closure over a real persisted store — the draft is a REQUEST (never `input.value === EFFECTIVE`), the Save sends ONLY the changed fields with a fresh idempotency key (G4), the returned document is the new OBSERVED baseline (the draft reconciles to the server's answer), `applies: next-spawn` rendered verbatim (a LIVE server keeps its flags), the compiled command preview read-only, the closed three-field set with verbatim DOMAIN_REJECTED lanes, no polling (one mount READ; the raw extra_args hatch dissolves into the document — disclosure layers are not semantic classes); **About** (the existing session-free `app.status`): the gateway's own identity read-only — service, contract, exposure, auth, the full registered operation registry; the rejection-probe console stays in Diagnostics (identity here, proof there); the DRAFT's owner is the SURFACE — a section switch never drops the unsaved REQUEST (falsified live); Appearance is a named standing boundary (no persisted appearance store; browser storage is never truth) |

## The laws this tree lives by

- Every wire payload enters as `unknown` and is runtime-validated
  (`src/api/gateway/validators.ts`) — raw JSON never reaches a
  component; unknown keys are contract violations, not noise. The
  stream frames carry the SAME law (`stream.ts` validates every
  frame's document through the zod frame validators before any
  consumer sees it; a deviation is a CONTRACT_MISMATCH — the phase
  goes FAILED with the detail, never a silent pass-through).
- The client auto-retries nothing (G4): UNKNOWN and transport
  ambiguity stay honest; a retry is an explicit user action — the
  stream's own law: a semantic `stream.rejected` verdict NEVER
  auto-reconnects (the stream stops, the verdict surfaces verbatim;
  an explicit restart is the caller's decision).
- The stream adapter OWNS its reconnection (never the browser's
  auto-reconnect — the explicit-cursor wire law makes it duplicate
  the replay window): the source is closed on every terminal/error,
  the re-dial rides a bounded backoff (500ms doubling to a 5s cap,
  reset on OPEN) from the adapter's own cursor; the focused-tab
  policy holds ONE stream per visible+focused tab (a background tab
  holds NO connection — STALE, the last-known presentation).
- The live tail buffer is bounded (50k rows): presentation window,
  never a client-side log; durable history is the Observatory's —
  and the Observatory pane holds ONE bounded window (≤ the backend's
  200-row cap) at a time, the forward pagination replacing it, the
  event-id cursor never mixed with the LIVE sequence cursor.
- One composition root (`src/app/composition/`); surfaces reach
  the gateway only through the typed client; the transport adapters
  are the only places `fetch` and `EventSource` exist.
- Synthetic load-test rows are flagged at the row, in the banner,
  and in the payload — presentation-only, never gateway truth.

## Not in S0 (the gate list)

a SharedWorker stream transport (§5's own law — packaging-only
shared transport needs its own gateway contract); WebSocket (only
for a concrete bidirectional requirement); the layout manifest /
surface registry; the full
Observatory analytical suite (compare/graphs/cross-run — the ENTRY
row has landed: the runs scan + the bounded window); PWA offline
packaging; Tauri 2; V5.2 polish; JSON-Schema-driven settings (the
Settings ENTRY row has landed over the store's own closed document);
the pixel-diff visual regression (the tooling floor's last parked
row — the additive CI job AND the Playwright multi-tab smoke are
LANDED, iter-309; dependency-cruiser stays parked behind the guard
test, AGENTS §2.8's existing-mechanism law).
