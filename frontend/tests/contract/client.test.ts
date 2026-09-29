/**
 * The gateway client's contract tests (mocked transport — the
 * delivery/semantics split): the envelope goes out as one POST; the
 * four outcome lanes stay distinct (DELIVERED OK / DELIVERED
 * non-OK / TRANSPORT / MISMATCH); G4 holds (the client never
 * retries); the dual `session.events` shape classifies.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { afterEach, describe, expect, it, vi } from "vitest";

import { GatewayClient } from "../../src/api/gateway/client.ts";

const FIXTURES = join(dirname(fileURLToPath(import.meta.url)), "..", "fixtures");

function fixture(name: string): unknown {
  return JSON.parse(readFileSync(join(FIXTURES, `${name}.json`), "utf8")) as unknown;
}

function jsonResponse(document: unknown, status = 200): Response {
  return new Response(JSON.stringify(document), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("the outbound envelope (one POST, the right shape)", () => {
  it("POSTs the envelope to the configured URL as JSON", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse(fixture("app_status_ok")));
    vi.stubGlobal("fetch", fetchMock);
    const client = new GatewayClient({ url: "http://127.0.0.1:8765/op" });
    await client.appStatus();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("http://127.0.0.1:8765/op");
    expect(init.method).toBe("POST");
    expect(init.headers).toMatchObject({ "Content-Type": "application/json" });
    const body = JSON.parse(String(init.body)) as Record<string, unknown>;
    expect(body).toEqual({ operation: "app.status" });
  });

  it("carries the idempotency key and session fields on mutations", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse(fixture("session_attach_ok")));
    vi.stubGlobal("fetch", fetchMock);
    const client = new GatewayClient();
    await client.sessionAttach({
      sessionId: "s1",
      expectedRevision: 3,
      clientRequestId: "key-1",
    });
    const body = JSON.parse(String(fetchMock.mock.calls[0]![1]!.body)) as Record<string, unknown>;
    expect(body).toEqual({
      operation: "session.attach",
      arguments: {},
      session_id: "s1",
      expected_revision: 3,
      client_request_id: "key-1",
    });
  });
});

describe("the four outcome lanes stay distinct", () => {
  it("DELIVERED + OK — the validated result rides", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(fixture("app_status_ok"))));
    const client = new GatewayClient();
    const result = await client.appStatus();
    expect(result.transport).toBe("DELIVERED");
    if (result.transport === "DELIVERED" && result.status === "OK") {
      expect(result.result.service).toBe("canonsim-workbench-gateway");
    } else {
      expect.unreachable("the fixture is an OK response");
    }
  });

  it("DELIVERED + REJECTED — the honest rejection name (DOMAIN_REJECTED)", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(fixture("session_get_domain_rejected"))));
    const client = new GatewayClient();
    const result = await client.sessionGet("bogus");
    expect(result.transport).toBe("DELIVERED");
    if (result.transport === "DELIVERED" && result.status !== "OK") {
      expect(result.status).toBe("REJECTED");
      expect(result.response.rejection).toBe("DOMAIN_REJECTED");
    } else {
      expect.unreachable("the fixture is a rejection");
    }
  });

  it("DELIVERED + REJECTED — STALE_REVISION (the CAS guard)", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(fixture("session_attach_stale_revision"))));
    const client = new GatewayClient();
    const result = await client.sessionAttach({
      sessionId: "s",
      expectedRevision: 999,
      clientRequestId: "k",
    });
    expect(result.transport).toBe("DELIVERED");
    if (result.transport === "DELIVERED" && result.status !== "OK") {
      expect(result.response.rejection).toBe("STALE_REVISION");
    } else {
      expect.unreachable("the fixture is a rejection");
    }
  });

  it("DELIVERED + REJECTED — DUPLICATE_REQUEST (the conflicting reuse)", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(fixture("session_create_duplicate_request"))));
    const client = new GatewayClient();
    const result = await client.sessionCreate({ clientRequestId: "dup" });
    expect(result.transport).toBe("DELIVERED");
    if (result.transport === "DELIVERED" && result.status !== "OK") {
      expect(result.response.rejection).toBe("DUPLICATE_REQUEST");
    } else {
      expect.unreachable("the fixture is a rejection");
    }
  });

  it("TRANSPORT — HTTP_ERROR on a 4xx delivery-level answer", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(jsonResponse({ error: "NOT_FOUND", path: "/nope" }, 404)),
    );
    const client = new GatewayClient();
    const result = await client.appStatus();
    expect(result.transport).toBe("TRANSPORT");
    if (result.transport === "TRANSPORT") {
      expect(result.failure.kind).toBe("HTTP_ERROR");
    }
  });

  it("TRANSPORT — UNREACHABLE when the dial fails (never 'rejected')", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("fetch failed")));
    const client = new GatewayClient();
    const result = await client.appStatus();
    expect(result.transport).toBe("TRANSPORT");
    if (result.transport === "TRANSPORT") {
      expect(result.failure.kind).toBe("UNREACHABLE");
    }
  });

  it("TRANSPORT — ABORTED says the outcome is UNKNOWN if it was sent (G4's honest form)", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new DOMException("aborted", "AbortError")));
    const client = new GatewayClient();
    const result = await client.appStatus();
    expect(result.transport).toBe("TRANSPORT");
    if (result.transport === "TRANSPORT") {
      expect(result.failure.kind).toBe("ABORTED");
      expect(result.failure.detail).toContain("UNKNOWN");
    }
  });

  it("TRANSPORT — NOT_JSON on a 200 with a non-JSON body", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("<html>not json</html>", { status: 200 })));
    const client = new GatewayClient();
    const result = await client.appStatus();
    expect(result.transport).toBe("TRANSPORT");
    if (result.transport === "TRANSPORT") {
      expect(result.failure.kind).toBe("NOT_JSON");
    }
  });

  it("MISMATCH — an unknown key in the response document is a contract violation", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(jsonResponse({ status: "OK", operation_id: "op", result: {}, rogue: 1 })),
    );
    const client = new GatewayClient();
    const result = await client.appStatus();
    expect(result.transport).toBe("MISMATCH");
  });

  it("MISMATCH — an OK envelope whose result violates the op schema", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        jsonResponse({ status: "OK", operation_id: "op", result: { service: "x" } }),
      ),
    );
    const client = new GatewayClient();
    const result = await client.appStatus();
    expect(result.transport).toBe("MISMATCH");
  });
});

describe("the dual session.events shape classifies (§13)", () => {
  it("REPLAY carries the ordered events", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(fixture("session_events_ok"))));
    const client = new GatewayClient();
    const result = await client.sessionEvents({ sessionId: "s", sinceSequence: 0 });
    if (result.transport === "DELIVERED" && result.status === "OK") {
      expect(result.result.kind).toBe("REPLAY");
      if (result.result.kind === "REPLAY") {
        expect(result.result.events.length).toBeGreaterThan(0);
      }
    } else {
      expect.unreachable("the fixture is an OK replay");
    }
  });

  it("RESYNC_REQUIRED carries the retained window + the snapshot", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(fixture("session_events_resync_required"))));
    const client = new GatewayClient();
    const result = await client.sessionEvents({ sessionId: "s", sinceSequence: 0 });
    if (result.transport === "DELIVERED" && result.status === "OK") {
      expect(result.result.kind).toBe("RESYNC_REQUIRED");
      if (result.result.kind === "RESYNC_REQUIRED") {
        expect(result.result.retained_from).toBeGreaterThan(0);
        expect(result.result.snapshot.revision).toBe(10);
      }
    } else {
      expect.unreachable("the fixture is an OK resync");
    }
  });
});

describe("G4 — the client retries nothing", () => {
  it("a transport failure is returned, never retried in-client", async () => {
    const fetchMock = vi.fn().mockRejectedValue(new TypeError("fetch failed"));
    vi.stubGlobal("fetch", fetchMock);
    const client = new GatewayClient();
    const first = await client.appStatus();
    expect(first.transport).toBe("TRANSPORT");
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
