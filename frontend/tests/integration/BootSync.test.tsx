/**
 * The boot-time OBSERVED-sync integration proof (iter-309, the
 * iter-308 §C candidate row landed): the tab's boot sequence is
 * create → ONE session.get — the freshness vocabulary counts READS,
 * so the sync is what turns the strip LIVE at a healthy gateway
 * (iter-308's live observation: a create-only boot honestly showed
 * DISCONNECTED, readable as "gateway dead" while ops ran fine).
 *
 * What is pinned here (each row the row's own law):
 * - a successful create fires EXACTLY ONE session.get (the FIRST
 *   OBSERVATION — never a retry: the create already answered OK;
 *   never a poll: the count is the falsifier) and the strip settles
 *   LIVE with the READ document's rev/seq, never an assumed one;
 * - the sync is one-shot: after LIVE, no further gets arrive (the
 *   no-poll falsifier — a hidden loop would fail the count);
 * - the sync's own TRANSPORT failure keeps the honest DISCONNECTED
 *   lane (no successful read yet — never a fabricated LIVE) and the
 *   create's success is not rewritten into an error banner;
 * - a DELIVERED semantic rejection lands STALE-with-reason — the
 *   observation is honest, never a transport collapse.
 *
 * Browser-less band (jsdom + testing-library), the same fixture
 * gateway as the composition-root proofs; the live closure rides
 * the Playwright multi-tab smoke (tests/e2e/, iter-309).
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";

import { App } from "../../src/app/composition/App.tsx";

const FIXTURES = join(dirname(fileURLToPath(import.meta.url)), "..", "fixtures");
const SESSION_ID = "d9dcca4f7314f1c9adfe66602eb9b8c85830ec8c1561175a7a497876be18007f";

function fixture(name: string): Record<string, unknown> {
  return JSON.parse(readFileSync(join(FIXTURES, `${name}.json`), "utf8")) as Record<string, unknown>;
}

function json(document: unknown): Response {
  return new Response(JSON.stringify(document), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

/** The parsed request bodies, in dispatch order. */
function callsOf(fetchMock: ReturnType<typeof vi.fn>): Record<string, unknown>[] {
  return fetchMock.mock.calls.map(
    (args) => JSON.parse(String(args[1]?.body)) as Record<string, unknown>,
  );
}

function opsOf(fetchMock: ReturnType<typeof vi.fn>): string[] {
  return callsOf(fetchMock).map((call) => String(call["operation"]));
}

/** A routing fetch mock: each op answers its fixture; a missing op
 * falls through to an UNKNOWN_OPERATION rejection (never a hang). */
function gatewayRouter(ops: Record<string, unknown>): ReturnType<typeof vi.fn> {
  return vi.fn(async (_input: unknown, init?: RequestInit) => {
    const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
    const op = String(body["operation"] ?? "");
    const doc = ops[op];
    return json(doc ?? { status: "REJECTED", rejection: "UNKNOWN_OPERATION", operation_id: "op_router_miss" });
  });
}

/** The boot ops the composition root dispatches in the jsdom band (the
 * initial route is Trajectory: its stream dial honestly FAILs here —
 * jsdom provides no EventSource — so no session.events POST rides). */
const BOOT_OPS: Record<string, unknown> = {
  "session.create": fixture("session_create_ok"),
  "session.get": fixture("session_get_ok"),
};

describe("the boot-time OBSERVED-sync (iter-308 §C's candidate row, iter-309)", () => {
  it("create → ONE session.get: the strip settles LIVE with the READ document", async () => {
    const fetchMock = gatewayRouter(BOOT_OPS);
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await waitFor(() => {
      expect(screen.getByTestId("session-freshness").textContent).toBe("LIVE");
    });

    // The document the strip renders is the READ one, never assumed:
    // rev/seq from session_get_ok's result, not the create's echo.
    expect(screen.getByTestId("session-rev").textContent).toBe("0");
    expect(screen.getByTestId("session-seq").textContent).toBe("1");
    expect(screen.getByTestId("session-id").textContent).toBe(SESSION_ID);

    // The boot sequence: exactly one create, then exactly one get —
    // the FIRST OBSERVATION (the row's own law: never a retry, the
    // create already answered OK).
    const ops = opsOf(fetchMock);
    expect(ops.filter((op) => op === "session.create")).toHaveLength(1);
    const gets = callsOf(fetchMock).filter((call) => call["operation"] === "session.get");
    expect(gets).toHaveLength(1);
    expect(gets[0]?.["session_id"]).toBe(SESSION_ID);
    expect(ops.indexOf("session.get")).toBe(1); // immediately after the create
  });

  it("the sync is one-shot — after LIVE, no further gets (the no-poll falsifier)", async () => {
    const fetchMock = gatewayRouter(BOOT_OPS);
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await waitFor(() => {
      expect(screen.getByTestId("session-freshness").textContent).toBe("LIVE");
    });
    await new Promise((resolve) => setTimeout(resolve, 80));
    expect(opsOf(fetchMock).filter((op) => op === "session.get")).toHaveLength(1);
  });

  it("the sync's TRANSPORT failure keeps the honest DISCONNECTED lane — never a fabricated LIVE, never a create banner", async () => {
    const fetchMock = vi.fn(async (_input: unknown, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
      if (String(body["operation"]) === "session.create") {
        return json(fixture("session_create_ok"));
      }
      return Promise.reject(new TypeError("fetch failed"));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    // The sync fired (the get was dispatched)...
    await waitFor(() => {
      expect(opsOf(fetchMock)).toContain("session.get");
    });
    // ...and its failure is honest: no successful read yet → the
    // strip stays DISCONNECTED; the create itself succeeded, so the
    // create-failure banner never renders.
    await new Promise((resolve) => setTimeout(resolve, 30));
    expect(screen.getByTestId("session-freshness").textContent).toBe("DISCONNECTED");
    expect(screen.queryByText(/session\.create failed/i)).toBeNull();
    expect(screen.getByTestId("session-id").textContent).toBe(SESSION_ID);
  });

  it("a DELIVERED semantic rejection lands STALE-with-reason — an honest observation, never a transport collapse", async () => {
    const fetchMock = gatewayRouter({
      "session.create": fixture("session_create_ok"),
      "session.get": fixture("session_get_domain_rejected"),
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await waitFor(() => {
      expect(screen.getByTestId("session-freshness").textContent).toBe("STALE");
    });
    // The observation itself happened (not a transport failure): the
    // gateway answered, and the strip keeps the session identity.
    expect(screen.getByTestId("session-id").textContent).toBe(SESSION_ID);
    expect(screen.queryByText(/session\.create failed/i)).toBeNull();
  });
});
