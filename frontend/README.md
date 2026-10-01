# CanonSim Workbench — the web client (frontend-1)

The ACTIVE frontend path (D-244: the owner's 2026-09-29 freeze+open
call; the Redot tree deleted at D-245 — the owner's «удаляй redot»
call). React + TypeScript + Vite, Web/PWA-first — the S0 walking
skeleton over the existing loopback gateway, now grown into
Phase 3's first three rows (the Shell + the Session lifecycle; the
Observatory HISTORY entry — the dual-read law's second world; the
Settings CONFIG entry — the §8 closure over a real persisted store)
+ the IA REPAIR (iter-297, D-247: the product/diagnostic registry
split — a vertical product rail + the subdued Diagnostics entry,
FRONTEND_UIUX_LAW §2.1's navigation contract).
The law: `docs/FRONTEND_WEB_LAW.md` (the S0 gate §2; the entry surface
`docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md`).

## What this is (and is not)

- **Is**: one presentation client of the Workbench gateway — typed,
  runtime-validated at the client boundary, replaceable,
  non-authoritative. The browser is an untrusted downstream client.
- **Is not**: a second simulator, event-log authority, rules engine,
  or LLM semantic authority. No SSE/WebSocket in S0 (POST `/op`
  only). No browser storage as truth; each tab is an independent
  gateway client.

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
```

The architecture guard (`tests/architecture/guard.test.ts`) is the
tooling floor's first landed row (FRONTEND_WEB_LAW §11's
dependency-boundary check, the backend `test_architecture.py`'s
parity form): it enforces, as executable law — fetch ONLY in the
typed gateway client (the one transport adapter); no
XMLHttpRequest/EventSource/WebSocket/serviceWorker before their
gateway contracts (the stream admission); no browser storage as
truth (localStorage/sessionStorage/BroadcastChannel/indexedDB/
caches); `src/api/**` imports nothing upward; no cross-feature
imports; features couple to state only via `import type`; one
composition root; src never imports tests; **V1 — the visual floor
(iter-297): no raw color literals outside the `:root` token set**
(a color is a named token, never a hex in a rule — VISUAL_SYSTEM_UI
§2/§3; the scan caught and closed a standing 9-literal violation).
A violation is a red
test naming the file and line — never silent drift. The heavier
instruments named by the law (dependency-cruiser / eslint-
boundaries, the Playwright-class multi-tab smoke) stay parked rows,
each its own admission (AGENTS §2.8: the existing suite first).

The contract tests run against the committed fixtures
(`tests/fixtures/*.json`) — captured from the live gateway code
(in-process dispatch, the parity law's byte form; `manifest.json`
the provenance). Regenerate with the iter-289 capture notes (the
sandbox-side capture script lives outside the repo per AGENTS §7
Rule 9; the fixtures' shape is the contract, the capture is
re-runnable from `tests/test_gateway.py`'s own patterns).

## The surfaces (the rail era — Phase 3 rows 1–3 + the IA repair)

The composition root mounts the **Shell** (`src/features/shell/`)
with the SPLIT registries (iter-297, D-247 — FRONTEND_UIUX_LAW
§2.1): `ProductRoute` (the rail's only content: Trajectory LIVE,
Observatory HISTORY, Settings pinned at the rail's end) and
`DiagnosticSurface` (behind ONE subdued Diagnostics entry, its own
secondary nav inside the workspace — Session lifecycle / Gateway /
Load probe, the proof instruments, never product peers). The rail
is a navigation instrument, never a feature directory: a
first-class surface is not automatically a navigation item.

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
| Load probe | drives real `session.attach` ops (the CAS loop) — the S0-4 measurement instrument |
| Trajectory | the LIVE session tail (`session.events`): virtualized ≥10k rows (only the window mounts), the semantic-sequence cursor, event-id selection, RESYNC_REQUIRED handled honestly, the LIVE label (volatile tail, never durable history) |
| Observatory | the HISTORY world (`observatory.runs`/`observatory.read`): the dual-read law's second half — the discovery scan, ONE bounded window at a time (the event-id cursor, `next_after` forward pagination that REPLACES the window, never an accumulating buffer), the context strip's identity line (seed/pack/CANON_VIEW/CANONICAL), event-id selection over the SAME document, NO DATA ≠ NO MATCH ≠ stale cursor ≠ TRANSPORT rendered distinct, no polling (durable evidence; every read explicit) |
| Settings | the CONFIG world (`backend.settings`/`backend.settings.update`): the §8 closure over a real persisted store — the draft is a REQUEST (never `input.value === EFFECTIVE`), the Save sends ONLY the changed fields with a fresh idempotency key (G4), the returned document is the new OBSERVED baseline (the draft reconciles to the server's answer), `applies: next-spawn` rendered verbatim (a LIVE server keeps its flags), the compiled command preview read-only, the closed three-field set with verbatim DOMAIN_REJECTED lanes, no polling (one mount READ) |

## The laws this tree lives by

- Every wire payload enters as `unknown` and is runtime-validated
  (`src/api/gateway/validators.ts`) — raw JSON never reaches a
  component; unknown keys are contract violations, not noise.
- The client auto-retries nothing (G4): UNKNOWN and transport
  ambiguity stay honest; a retry is an explicit user action.
- The live tail buffer is bounded (50k rows): presentation window,
  never a client-side log; durable history is the Observatory's —
  and the Observatory pane holds ONE bounded window (≤ the backend's
  200-row cap) at a time, the forward pagination replacing it, the
  event-id cursor never mixed with the LIVE sequence cursor.
- One composition root (`src/app/composition/`); surfaces reach
  the gateway only through the typed client; the transport adapter
  is the only place `fetch` exists.
- Synthetic load-test rows are flagged at the row, in the banner,
  and in the payload — presentation-only, never gateway truth.

## Not in S0 (the gate list)

SSE/WebSocket; the layout manifest / surface registry; the full
Observatory analytical suite (compare/graphs/cross-run — the ENTRY
row has landed: the runs scan + the bounded window); PWA offline
packaging; Tauri 2; V5.2 polish; JSON-Schema-driven settings (the
Settings ENTRY row has landed over the store's own closed document); the
CI rows (dependency-cruiser CI, the Playwright smoke — post-S0
admissions; the architecture guard itself rides `npm test` and IS
landed).
