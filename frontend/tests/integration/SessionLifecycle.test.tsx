/**
 * The session-lifecycle integration proof (Phase 3's first row), in
 * the browser-less band (jsdom + testing-library; the live evidence
 * rides the iteration report): the lease closure over the EXISTING
 * ops — attach under the CAS guard, detach under the lease guard.
 *
 * What is pinned here (each row an honest-closure law):
 * - the ACCEPTED verdict renders the EFFECT stage verbatim (the
 *   effect's name + the envelope's revision) and the OBSERVED sync
 *   fires (the root's re-read — `selected !== loaded`);
 * - STALE_REVISION renders the gateway's own name + reason with the
 *   NOT_SENT outcome note, and NO second dispatch fires (G4: no
 *   auto-retry — the call count is the falsifier);
 * - the explicit retry is the USER's decision: a fresh request
 *   identity (the two attach bodies carry distinct
 *   client_request_id keys — reusing a key with new material would
 *   be DUPLICATE_REQUEST, never attempted);
 * - the detach path releases the lease (the card empties, the
 *   control disables);
 * - a transport failure renders TRANSPORT with its own lane — never
 *   "rejected".
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import { GatewayClient } from "../../src/api/gateway/client.ts";
import type { SessionDocument } from "../../src/api/gateway/contracts.ts";
import { SessionLifecycle } from "../../src/features/session-lifecycle/SessionLifecycle.tsx";

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

/** The OBSERVED document the root would pass down (session_get_ok's result). */
const OBSERVED: SessionDocument = {
  session_id: SESSION_ID,
  attached: false,
  created_observed_at: 1_000_000,
  event_sequence: 1,
  revision: 0,
};

/** The post-attach observed document (revision bumped — inline, the wire form). */
function observedAtRevision(revision: number, attached: boolean): Record<string, unknown> {
  return {
    status: "OK",
    operation_id: "op-get",
    session_id: SESSION_ID,
    result: {
      session_id: SESSION_ID,
      attached,
      created_observed_at: 1_000_000,
      event_sequence: 1,
      revision,
    },
  };
}

function detachOk(): Record<string, unknown> {
  return {
    status: "OK",
    operation_id: "op-detach",
    session_id: SESSION_ID,
    revision: 2,
    result: { detached: true },
  };
}

/** The parsed request bodies, in dispatch order (the identity check's material). */
function callsOf(fetchMock: ReturnType<typeof vi.fn>): Record<string, unknown>[] {
  return fetchMock.mock.calls.map(
    (args) => JSON.parse(String(args[1]?.body)) as Record<string, unknown>,
  );
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

function mountSurface(fetchImpl: typeof fetch): { readonly refreshDocument: ReturnType<typeof vi.fn>; readonly recreateSession: ReturnType<typeof vi.fn> } {
  vi.stubGlobal("fetch", fetchImpl);
  const refreshDocument = vi.fn().mockResolvedValue(undefined);
  const recreateSession = vi.fn();
  const client = new GatewayClient();
  render(
    <SessionLifecycle
      client={client}
      sessionId={SESSION_ID}
      document={OBSERVED}
      refreshDocument={refreshDocument}
      recreateSession={recreateSession}
    />,
  );
  return { refreshDocument, recreateSession };
}

describe("the session-lifecycle surface (Phase 3, row 1)", () => {
  it("attach: the ACCEPTED verdict renders the EFFECT stage verbatim + fires the OBSERVED sync", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("session_get_ok")))
      .mockResolvedValueOnce(json(fixture("session_attach_ok")));
    const { refreshDocument } = mountSurface(fetchMock);

    fireEvent.click(screen.getByRole("button", { name: "attach session" }));

    const verdict = await screen.findByTestId("verdict-accepted");
    expect(verdict.textContent).toContain("attach");
    expect(verdict.textContent).toContain("ACCEPTED → EFFECTIVE: ATTACHED");
    expect(verdict.textContent).toContain("revision 1");
    expect(verdict.textContent).toContain("lease 30s");
    // The OBSERVED stage: the root's re-read fired exactly once.
    await waitFor(() => {
      expect(refreshDocument).toHaveBeenCalledTimes(1);
    });
    // The lease card carries the detach op's material.
    expect(screen.getByTestId("lease-token").textContent).toContain("e4da937d");
  });

  it("STALE_REVISION: the honest verdict verbatim, and NO second dispatch (G4)", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("session_get_ok")))
      .mockResolvedValueOnce(json(fixture("session_attach_stale_revision")));
    mountSurface(fetchMock);

    fireEvent.click(screen.getByRole("button", { name: "attach session" }));

    const verdict = await screen.findByTestId("verdict-rejected");
    expect(verdict.textContent).toContain("REJECTED · STALE_REVISION");
    expect(verdict.textContent).toContain("a stale writer cannot mutate newer state");
    expect(verdict.textContent).toContain("NOT_SENT — a retry is your explicit decision");
    // G4's falsifier: exactly one get + one attach — no auto-retry.
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledTimes(2);
    });
    await new Promise((resolve) => setTimeout(resolve, 30));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("the explicit retry mints a FRESH request identity (distinct client_request_id)", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("session_get_ok"))) // read for attempt 1
      .mockResolvedValueOnce(json(fixture("session_attach_stale_revision"))) // attempt 1: stale
      .mockResolvedValueOnce(json(observedAtRevision(1, true))) // read for attempt 2
      .mockResolvedValueOnce(json(fixture("session_attach_ok"))); // attempt 2: OK
    mountSurface(fetchMock);

    fireEvent.click(screen.getByRole("button", { name: "attach session" }));
    await screen.findByTestId("verdict-rejected");

    fireEvent.click(screen.getByRole("button", { name: "attach session" }));
    await screen.findByTestId("verdict-accepted");

    expect(fetchMock).toHaveBeenCalledTimes(4);
    const bodies = callsOf(fetchMock).map((call) => call["client_request_id"]);
    const attachKeys = bodies.filter((key): key is string => typeof key === "string" && key.startsWith("attach-"));
    expect(attachKeys.length).toBe(2);
    expect(attachKeys[0]).not.toBe(attachKeys[1]);
  });

  it("detach: releases the lease — the card empties, the control disables", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("session_get_ok"))) // read for attach
      .mockResolvedValueOnce(json(fixture("session_attach_ok"))) // attach OK
      .mockResolvedValueOnce(json(observedAtRevision(1, true))) // read for detach (post-attach)
      .mockResolvedValueOnce(json(detachOk())); // detach OK
    mountSurface(fetchMock);

    // No lease held yet: the detach control honestly disabled.
    expect(screen.getByRole("button", { name: "detach session" }).hasAttribute("disabled")).toBe(true);

    fireEvent.click(screen.getByRole("button", { name: "attach session" }));
    await screen.findByTestId("verdict-accepted");
    // The lease is held now: the control armed.
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "detach session" }).hasAttribute("disabled")).toBe(false);
    });

    fireEvent.click(screen.getByRole("button", { name: "detach session" }));
    const verdict = await screen.findByTestId("verdict-accepted");
    expect(verdict.textContent).toContain("ACCEPTED → EFFECTIVE: DETACHED");
    // The lease card honestly emptied, the detach control disabled again.
    await waitFor(() => {
      expect(screen.getByText(/no lease held/i)).toBeTruthy();
      expect(screen.getByRole("button", { name: "detach session" }).hasAttribute("disabled")).toBe(true);
    });
    // The detach body carried the lease token (the lease guard's material).
    const detachBody = callsOf(fetchMock).find((call) => call["operation"] === "session.detach");
    expect(detachBody?.["lease_token"]).toBe("e4da937d6c8aa07f5b66be54183ee5207f6cb0a28ecd17b2cfd4f383b3c92254");
  });

  it("transport failure: TRANSPORT with its own lane — never 'rejected'", async () => {
    mountSurface(vi.fn().mockRejectedValue(new TypeError("fetch failed")));

    fireEvent.click(screen.getByRole("button", { name: "attach session" }));

    const verdict = await screen.findByTestId("verdict-transport");
    expect(verdict.textContent).toContain("TRANSPORT · UNREACHABLE");
    expect(verdict.textContent).toContain("never");
    expect(verdict.textContent).toContain("outcome is UNKNOWN (no blind retry)");
    expect(screen.queryByTestId("verdict-rejected")).toBeNull();
  });
});
