/**
 * The Playwright multi-tab smoke — the tooling floor's Playwright-class
 * row (FRONTEND_WEB_LAW §11, landed iter-309 on the iter-308 browser
 * drive's template): multi-tab independent clients, the focused-tab
 * stream policy's STALE/reconnect round-trip, live push without
 * refresh, and the UNKNOWN outcome path — over the REAL composition
 * (the loopback gateway + the Vite dev proxy), never a mock.
 *
 * Form laws:
 * - The suite boots its OWN composition: the Python gateway
 *   (`scripts/workbench_app.py --no-backend` — the honest admission
 *   law: no llama.cpp means the backend-dependent ops stay
 *   UNREGISTERED, and this smoke touches none of them) plus the Vite
 *   dev server with `GATEWAY_TARGET` pointed at it — the same
 *   zero-command form `Workbench.bat` composes, never a parallel
 *   route around INV-4's sanctioned binding.
 * - Readiness is TCP-level (`port`, not `url`): the gateway's only
 *   2xx GET is the SSE stream itself (POST /op answers 200 to
 *   dispatched envelopes only; GET /op is a 405 by design) — polling
 *   it would demand a fake route, and opening the stream would mint
 *   a phantom subscription. A TCP accept is the honest "it is up".
 * - `workers: 1` — one browser, one focused tab at a time: the
 *   focused-tab policy IS the thing under test (only a visible+
 *   focused tab holds a stream), so parallel workers would fight
 *   over the front seat, not speed it up.
 * - No artifacts: traces/screenshots off — the report is the run
 *   itself (the iteration report carries the live evidence); the
 *   runner's output dirs stay gitignored.
 * - The suite is NOT a CI job (the additive frontend CI row is
 *   vitest+tsc+build by the owner's spec) — it is the committed
 *   owner-side/sandbox smoke, run by `npm run e2e`.
 */
import { defineConfig } from "@playwright/test";

/** The e2e-dedicated gateway port — deliberately NOT the documented
 * 8765 default, so an owner's live Workbench never collides with a
 * smoke run (sessions are independent either way — the port is
 * hygiene, never a correctness dependency). */
const GATEWAY_PORT = 8788;
const GATEWAY_TARGET = `http://127.0.0.1:${String(GATEWAY_PORT)}`;
const VITE_PORT = 5173;

export default defineConfig({
  testDir: "tests/e2e",
  timeout: 30_000,
  expect: { timeout: 10_000 },
  workers: 1,
  fullyParallel: false,
  reporter: [["list"]],
  outputDir: "test-results",
  use: {
    baseURL: `http://127.0.0.1:${String(VITE_PORT)}`,
    trace: "off",
    screenshot: "off",
    video: "off",
  },
  webServer: [
    {
      name: "gateway",
      command: `python scripts/workbench_app.py --no-backend --host 127.0.0.1 --port ${String(GATEWAY_PORT)}`,
      cwd: "..", // the repo root (workbench_app.py's own paths anchor there)
      port: GATEWAY_PORT,
      reuseExistingServer: true,
      timeout: 60_000,
    },
    {
      name: "vite",
      // --host 127.0.0.1: without it Vite binds ::1 only (the "localhost"
      // first resolution), and the browser at http://127.0.0.1:5173 is
      // connection-refused — an IPv6/IPv4 split, never an app defect.
      command: `npm run dev -- --strictPort --host 127.0.0.1 --port ${String(VITE_PORT)}`,
      port: VITE_PORT,
      reuseExistingServer: true,
      timeout: 60_000,
      // CI:"true" is Vite's OWN documented interop flag, not a CI claim:
      // vite wires `stdin.on("end") -> graceful shutdown` unless CI is
      // exactly "true", and Playwright's spawned child sees its stdin
      // pipe close — without this the dev server exits the moment it
      // becomes "available" (vite/dist setupSIGTERMListener).
      env: { GATEWAY_TARGET, CI: "true" },
    },
  ],
});
