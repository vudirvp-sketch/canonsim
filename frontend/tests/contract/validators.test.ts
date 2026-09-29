/**
 * The contract tests — the committed fixtures ARE the wire truth
 * (captured from the live gateway code, in-process dispatch — the
 * parity law's byte form; see manifest.json). Every fixture must
 * validate; every corrupted variant must be REJECTED (the
 * closed-document law: unknown keys, wrong types, and foreign enum
 * members never pass silently).
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import {
  appStatusResultSchema,
  eventEnvelopeSchema,
  responseDocumentSchema,
  sessionDocumentSchema,
  sessionEventsResultSchema,
  validateResponseDocument,
} from "../../src/api/gateway/validators.ts";

const FIXTURES = join(dirname(fileURLToPath(import.meta.url)), "..", "fixtures");

function fixture(name: string): unknown {
  return JSON.parse(readFileSync(join(FIXTURES, `${name}.json`), "utf8")) as unknown;
}

describe("the live-gateway fixtures validate (the OK family)", () => {
  it("app_status_ok", () => {
    const document = fixture("app_status_ok");
    expect(responseDocumentSchema.parse(document).status).toBe("OK");
    const status = appStatusResultSchema.parse(
      (document as { result: unknown }).result,
    );
    expect(status.contract).toBe("canon_workbench_gateway@0.1");
    expect(status.operations).toContain("session.events");
  });

  it("session_create_ok / session_get_ok / session_attach_ok", () => {
    for (const name of ["session_create_ok", "session_get_ok", "session_attach_ok"]) {
      const document = fixture(name);
      expect(responseDocumentSchema.parse(document).status).toBe("OK");
    }
    const getSession = fixture("session_get_ok") as { result: unknown };
    // Captured BEFORE the attach probe: attached=false, revision 0 —
    // the OBSERVED state, never the assumed one.
    expect(sessionDocumentSchema.parse(getSession.result).attached).toBe(false);
  });

  it("session_events_ok — every event validates against the envelope", () => {
    const document = fixture("session_events_ok") as { result: { events: unknown[] } };
    const parsed = sessionEventsResultSchema.parse(document.result);
    expect(parsed).toHaveProperty("events");
    if ("events" in parsed) {
      expect(parsed.events.length).toBeGreaterThan(0);
      for (const event of parsed.events) {
        expect(() => eventEnvelopeSchema.parse(event)).not.toThrow();
      }
    }
  });

  it("session_events_resync_required — the dual shape's other half", () => {
    const document = fixture("session_events_resync_required") as { result: unknown };
    const parsed = sessionEventsResultSchema.parse(document.result);
    expect(parsed).not.toHaveProperty("events");
    expect(parsed).toHaveProperty("resync", "RESYNC_REQUIRED");
  });
});

describe("the live-gateway fixtures validate (the honest rejection family)", () => {
  it("session_get_domain_rejected", () => {
    const response = validateResponseDocument(fixture("session_get_domain_rejected"));
    expect(response.ok).toBe(false);
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
  });

  it("session_attach_stale_revision", () => {
    const response = validateResponseDocument(fixture("session_attach_stale_revision"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("STALE_REVISION");
  });

  it("session_create_duplicate_request (the result.reason carrier)", () => {
    const response = validateResponseDocument(fixture("session_create_duplicate_request"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DUPLICATE_REQUEST");
  });

  it("session_events_unknown_argument", () => {
    const response = validateResponseDocument(fixture("session_events_unknown_argument"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
  });
});

describe("the closed-document law (corrupted variants are rejected)", () => {
  it("an unknown top-level key fails", () => {
    const document = {
      status: "OK",
      operation_id: "op",
      result: { service: "x" },
      mystery_key: true,
    };
    expect(() => responseDocumentSchema.parse(document)).toThrow();
  });

  it("a foreign status fails", () => {
    expect(() => responseDocumentSchema.parse({ status: "FINE", operation_id: "op" })).toThrow();
  });

  it("a foreign rejection name fails", () => {
    expect(() =>
      responseDocumentSchema.parse({ status: "REJECTED", operation_id: "op", rejection: "NOPE" }),
    ).toThrow();
  });

  it("an OK response with a rejection fails", () => {
    expect(() =>
      validateResponseDocument({ status: "OK", operation_id: "op", rejection: "DOMAIN_REJECTED" }),
    ).toThrow();
  });

  it("a non-OK response without its rejection fails", () => {
    expect(() => validateResponseDocument({ status: "REJECTED", operation_id: "op" })).toThrow();
  });

  it("a foreign event_type fails", () => {
    const event = {
      event_id: "id",
      session_id: "s",
      operation_id: "o",
      sequence: 1,
      event_type: "SOMETHING_ELSE",
      observed_at: 1,
      payload: {},
    };
    expect(() => eventEnvelopeSchema.parse(event)).toThrow();
  });

  it("sequence 0 fails (the stream starts at 1)", () => {
    const event = {
      event_id: "id",
      session_id: "s",
      operation_id: "o",
      sequence: 0,
      event_type: "SESSION_CREATED",
      observed_at: 1,
      payload: {},
    };
    expect(() => eventEnvelopeSchema.parse(event)).toThrow();
  });

  it("a non-finite observed_at fails", () => {
    const document = fixture("session_events_ok") as {
      result: { events: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.events[0]!["observed_at"] = Number.NaN;
    expect(() => sessionEventsResultSchema.parse(corrupted.result)).toThrow();
  });

  it("an event envelope with an unknown key fails", () => {
    const document = fixture("session_events_ok") as {
      result: { events: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.events[0]!["extra"] = 1;
    expect(() => sessionEventsResultSchema.parse(corrupted.result)).toThrow();
  });
});
