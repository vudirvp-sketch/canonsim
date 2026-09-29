# CanonSim Workbench — the web client (frontend-1, S0)

The ACTIVE frontend path (D-244: the owner's 2026-09-29 freeze+open
call; the Redot tree deleted at D-245 — the owner's «удаляй redot»
call). React + TypeScript + Vite, Web/PWA-first — the S0 walking
skeleton over the existing loopback gateway. The law:
`docs/FRONTEND_WEB_LAW.md` (the S0 gate §2; the entry surface
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
npm test            # vitest run (unit + contract + integration)
npm run build       # typecheck + the production build
```

The contract tests run against the committed fixtures
(`tests/fixtures/*.json`) — captured from the live gateway code
(in-process dispatch, the parity law's byte form; `manifest.json`
the provenance). Regenerate with the iter-289 capture notes (the
sandbox-side capture script lives outside the repo per AGENTS §7
Rule 9; the fixtures' shape is the contract, the capture is
re-runnable from `tests/test_gateway.py`'s own patterns).

## The S0 surfaces

| Surface | What it proves |
|---|---|
| Gateway (status) | the `app.status` round-trip + the honest rejection probes (DOMAIN_REJECTED / STALE_REVISION / DUPLICATE_REQUEST) — the DELIVERED/TRANSPORT/MISMATCH lanes never collapse |
| Load probe | drives real `session.attach` ops (the CAS loop) — the S0-4 measurement instrument |
| Trajectory | the LIVE session tail (`session.events`): virtualized ≥10k rows (only the window mounts), the semantic-sequence cursor, event-id selection, RESYNC_REQUIRED handled honestly, the LIVE label (volatile tail, never durable history) |

## The laws this tree lives by

- Every wire payload enters as `unknown` and is runtime-validated
  (`src/api/gateway/validators.ts`) — raw JSON never reaches a
  component; unknown keys are contract violations, not noise.
- The client auto-retries nothing (G4): UNKNOWN and transport
  ambiguity stay honest; a retry is an explicit user action.
- The live tail buffer is bounded (50k rows): presentation window,
  never a client-side log; durable history is the Observatory's.
- One composition root (`src/app/composition/`); surfaces reach
  the gateway only through the typed client; the transport adapter
  is the only place `fetch` exists.
- Synthetic load-test rows are flagged at the row, in the banner,
  and in the payload — presentation-only, never gateway truth.

## Not in S0 (the gate list)

SSE/WebSocket; the layout manifest / surface registry; the full
Observatory suite; PWA offline packaging; Tauri 2; V5.2 polish;
JSON-Schema-driven settings; dependency-cruiser CI (recommended
immediately after S0 green).
