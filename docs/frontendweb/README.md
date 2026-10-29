# Canonsim Frontend-Web Track

> The web-frontend track: the active web client is `frontend/` (React +
> TypeScript + Vite, Web/PWA-first); the binding implementation law lives
> at `docs/FRONTEND_WEB_LAW.md`.

## Purpose

This directory holds the frontend-web track's durable documents. It is
not a runtime contract by itself — `docs/FRONTEND_WEB_LAW.md` is the
binding law (the S0 gate, the gateway seam, dual-read, the connection
budget, browser runtime bounds, surface modules, effective-state
closure, the tooling floor).

## Read order

1. `docs/FRONTEND_WEB_LAW.md` — the binding web-frontend implementation
   law.
2. `frontend/README.md` — how to run the web client.

## Current stage

The S0 walking skeleton and the visual floors landed; the acceptance
matrix is closed and CI runs the web checks (tsc + vitest + build) on
every push to `main`. The Playwright multi-tab smoke (`npm run e2e` in
`frontend/`) boots the real gateway + Vite and stays an owner-side run.
