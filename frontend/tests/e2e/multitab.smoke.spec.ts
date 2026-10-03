/**
 * The multi-tab smoke (FRONTEND_WEB_LAW §11's Playwright-class row,
 * iter-309 — the iter-308 browser drive's template made committed and
 * executable): four lanes over the REAL gateway + Vite proxy, each a
 * row the drive verified live by hand, now pinned as a suite:
 *
 * 1. Two tabs are INDEPENDENT clients — two sessions minted, two
 *    strips LIVE at boot (the boot-time OBSERVED-sync's live closure:
 *    the create alone never turns the strip LIVE), no shared store.
 * 2. The focused-tab stream policy — only a visible+focused tab
 *    holds a stream; a blurred tab's connection REALLY closes
 *    (PAUSED — STALE, the last-known presentation held), and the
 *    refocus re-dials from the cursor (the reconnect path through
 *    the policy's own signal; headless never blurs by itself —
 *    setFocused drives the app's own listeners, the jsdom band's
 *    form over a live wire).
 * 3. Live push without refresh — real ops driven at the gateway (the
 *    CAS loop: session.get for the revision, session.attach with a
 *    fresh idempotency key) land as new tail rows in the focused tab.
 * 4. The UNKNOWN outcome path — the network cut kills ONLY the
 *    in-flight attach (the read passes): the verdict lane renders
 *    TRANSPORT with the honest "outcome is UNKNOWN (no blind retry)"
 *    note, G4 never fabricates a completion, and the USER's explicit
 *    retry (a fresh request identity) recovers ATTACHED.
 *
 * The drive's standing bar rides with every test: zero app-originated
 * console errors, zero uncaught exceptions (the one sanctioned
 * exception: the network cut of lane 4 is the TEST's own act —
 * Chromium's network layer logs the aborted request; the APP's honest
 * answer is the UI lane, never a console crash).
 */
import { expect, test } from "@playwright/test";
import type { Page } from "@playwright/test";

/** The gateway the Vite proxy forwards to (the e2e-dedicated port —
 * see playwright.config.ts; the browser itself stays same-origin to
 * the dev server, exactly like the product). */
const GATEWAY = "http://127.0.0.1:8788";

/** One page's console-error + uncaught-exception record. */
function watchConsole(page: Page): string[] {
  const errors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });
  page.on("pageerror", (error) => errors.push(`pageerror: ${error.message}`));
  return errors;
}

/** The environment's own network-layer line for an aborted request
 * (Chromium logs it; the app owes its honesty in the UI lane, not the
 * console — the suite never silences the browser's own bookkeeping). */
function appErrors(errors: readonly string[]): string[] {
  return errors.filter((entry) => !/failed to load resource|net::err/i.test(entry));
}

/**
 * Flip the focused-tab policy's own input for one page. Headless
 * Chromium never blurs a background page (every page reports
 * visible+focused — bringToFront changes nothing the app can see),
 * so the drive dispatches the events the policy itself listens to:
 * the window blur/focus pair, with `document.hasFocus` answering the
 * blurred side truthfully. This is the same band the jsdom suite
 * pins (Trajectory.test.tsx's focused-tab row) — but here the
 * EventSource teardown and the cursor re-dial are REAL, over the
 * live gateway's stream.
 */
async function setFocused(page: Page, focused: boolean): Promise<void> {
  await page.evaluate((focused: boolean) => {
    const doc = document as unknown as { hasFocus?: () => boolean };
    if (focused) {
      delete doc.hasFocus; // the browser's own truth returns
      window.dispatchEvent(new Event("focus"));
      return;
    }
    doc.hasFocus = () => false;
    window.dispatchEvent(new Event("blur"));
  }, focused);
}

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test("two tabs are independent clients — two sessions, each strip LIVE at boot (the OBSERVED-sync)", async ({
  page,
  context,
}) => {
  const errorsA = watchConsole(page);
  const tabB = await context.newPage();
  const errorsB = watchConsole(tabB);
  await tabB.goto("/");

  // The boot-time OBSERVED-sync's live closure: ONE session.get after
  // the create turns each strip LIVE — a create-only boot stayed
  // DISCONNECTED (iter-308 §C's observation, the row's before-state).
  await expect(page.getByTestId("session-freshness")).toHaveText("LIVE");
  await expect(tabB.getByTestId("session-freshness")).toHaveText("LIVE");

  // Two INDEPENDENT sessions: distinct 64-hex identities, never a
  // shared client state (S0-3's no-shared-store law).
  const idA = (await page.getByTestId("session-id").textContent()) ?? "";
  const idB = (await tabB.getByTestId("session-id").textContent()) ?? "";
  expect(idA).toMatch(/^[0-9a-f]{16,}$/);
  expect(idB).toMatch(/^[0-9a-f]{16,}$/);
  expect(idA).not.toBe(idB);

  // The READ document, never an assumed one: rev rendered from the
  // observed session.get, both tabs.
  await expect(page.getByTestId("session-rev")).toHaveText(/^[0-9]+$/);
  await expect(tabB.getByTestId("session-rev")).toHaveText(/^[0-9]+$/);

  expect(appErrors(errorsA)).toEqual([]);
  expect(appErrors(errorsB)).toEqual([]);
  await tabB.close();
});

test("the focused-tab stream policy: a blurred tab closes its stream (PAUSED), the refocus re-dials — one stream per focused tab", async ({
  page,
  context,
}) => {
  const errorsA = watchConsole(page);
  // The first tab — the only page — is visible+focused: its stream dials.
  await expect(page.getByTestId("stream-phase")).toHaveText(/stream OPEN/);

  const tabB = await context.newPage();
  const errorsB = watchConsole(tabB);
  await tabB.goto("/");

  // The second tab holds its own stream — one per tab, both live over
  // the SAME gateway (the budget law counts per tab, never per app).
  await expect(tabB.getByTestId("stream-phase")).toHaveText(/stream OPEN/);

  // Blur the FIRST tab (the policy's own signal, see setFocused): the
  // connection REALLY closes (PAUSED — STALE presentation, the
  // last-known rows held) while the focused tab's stream stays OPEN.
  await setFocused(page, false);
  await expect(page.getByTestId("stream-phase")).toHaveText(/stream PAUSED/);
  await expect(
    page.getByRole("region", { name: /Trajectory/i }).locator(".freshness"),
  ).toHaveText("STALE");
  await expect(tabB.getByTestId("stream-phase")).toHaveText(/stream OPEN/);

  // The refocus re-dials from the cursor — the reconnection path
  // through the policy's own mechanism, a REAL second connection.
  await setFocused(page, true);
  await expect(page.getByTestId("stream-phase")).toHaveText(/stream OPEN/);

  // The symmetric cut: the second tab parks, the first one's stream
  // is untouched — never a budget storm, never a cross-tab coupling.
  await setFocused(tabB, false);
  await expect(tabB.getByTestId("stream-phase")).toHaveText(/stream PAUSED/);
  await expect(page.getByTestId("stream-phase")).toHaveText(/stream OPEN/);
  await setFocused(tabB, true);
  await expect(tabB.getByTestId("stream-phase")).toHaveText(/stream OPEN/);

  expect(appErrors(errorsA)).toEqual([]);
  expect(appErrors(errorsB)).toEqual([]);
  await tabB.close();
});

test("live push: real ops driven at the gateway land in the focused tab without any refresh", async ({
  page,
  request,
}) => {
  const errors = watchConsole(page);
  await expect(page.getByTestId("stream-phase")).toHaveText(/stream OPEN/);

  const sessionId = ((await page.getByTestId("session-id").textContent()) ?? "").trim();
  expect(sessionId).toMatch(/^[0-9a-f]{16,}$/);
  const seqBefore = Number(((await page.getByTestId("tail-seq").textContent()) ?? "0").trim());

  // The CAS loop, exactly the S0-4 probe's shape: read the current
  // revision, attach with a FRESH idempotency key (G4), repeat.
  for (let i = 0; i < 3; i += 1) {
    const read = await request.post(`${GATEWAY}/op`, {
      data: { operation: "session.get", session_id: sessionId },
    });
    expect(read.ok(), await read.text()).toBeTruthy();
    const document = (await read.json()) as { result: { revision: number } };
    const attach = await request.post(`${GATEWAY}/op`, {
      data: {
        operation: "session.attach",
        session_id: sessionId,
        expected_revision: document.result.revision,
        client_request_id: `e2e-livepush-${crypto.randomUUID()}`,
        arguments: { label: "multitab smoke live push" },
      },
    });
    expect(attach.ok(), await attach.text()).toBeTruthy();
  }

  // No refresh, no poll: the three attach events arrive over the
  // stream the tab already holds — the tail's semantic cursor moved.
  await expect(page.getByTestId("tail-seq")).toHaveText(String(seqBefore + 3));
  expect(appErrors(errors)).toEqual([]);
});

test("UNKNOWN outcome: the network cut on the in-flight attach renders the honest lane — the explicit retry recovers", async ({
  page,
}) => {
  const errors = watchConsole(page);
  await expect(page.getByTestId("session-freshness")).toHaveText("LIVE");

  await page.getByRole("button", { name: "Diagnostics" }).click();
  await page.getByRole("button", { name: "Session lifecycle" }).click();
  await expect(page.getByRole("region", { name: "Session lifecycle" })).toBeVisible();

  // The cut: ONLY the attach dispatch dies mid-flight — the read
  // before it passes, so the REQUEST was demonstrably sent and its
  // outcome genuinely UNKNOWN (never a fabricated completion).
  await page.route("**/gateway/op", async (route) => {
    const body = route.request().postData() ?? "";
    if (body.includes('"session.attach"')) {
      await route.abort("connectionreset");
      return;
    }
    await route.continue();
  });

  await page.getByRole("button", { name: "attach session" }).click();

  // The honest TRANSPORT lane verbatim — never "rejected".
  await expect(page.getByTestId("verdict-transport")).toContainText("TRANSPORT");
  await expect(page.getByTestId("verdict-transport")).toContainText("UNKNOWN (no blind retry)");
  expect(await page.getByTestId("verdict-accepted").count()).toBe(0);

  // G4 in the wild: the retry is the USER's decision — heal the wire,
  // click again (a fresh request identity inside the surface), and
  // the lease lands ATTACHED.
  await page.unroute("**/gateway/op");
  await page.getByRole("button", { name: "attach session" }).click();
  await expect(page.getByTestId("verdict-accepted")).toContainText("ACCEPTED → EFFECTIVE: ATTACHED");
  expect(appErrors(errors)).toEqual([]);
});
