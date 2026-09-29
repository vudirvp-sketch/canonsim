/**
 * The typed gateway client — S0's ONLY transport adapter
 * (FRONTEND_WEB_LAW §3 / the browser-runtime §4 split): surfaces
 * call this API, nothing else. No component ever sees `fetch`, a
 * URL, or raw JSON.
 *
 * Honesty laws carried here:
 * - G4: UNKNOWN is never a blind retry — the client auto-retries
 *   NOTHING (mutations carry `client_request_id`; a retry is the
 *   caller's explicit decision).
 * - Delivery vs semantics (§8's split): ANY envelope the core
 *   processed answers HTTP 200 — a semantic rejection is a
 *   DELIVERED outcome; 4xx/not-JSON/network failures are
 *   transport-level failures, a distinct class (never rendered as
 *   "gateway rejected").
 * - The closed-document law: the response is runtime-validated;
 *   a wire payload that deviates from the contract is a
 *   CONTRACT_MISMATCH — reported, never coerced.
 * - POST /op only (S0-3): no SSE, no WebSocket, no GETs.
 */
import type {
  AppStatusResult,
  RequestEnvelope,
  SessionAttachResult,
  SessionCreateResult,
  SessionDocument,
  SessionEventsResult,
} from "./contracts.ts";
import {
  appStatusResultSchema,
  sessionAttachResultSchema,
  sessionCreateResultSchema,
  sessionDetachResultSchema,
  sessionDocumentSchema,
  sessionEventsResultSchema,
  validateResponseDocument,
  type ValidatedResponse,
} from "./validators.ts";
import type { z } from "zod";

/** The transport failure classes — distinct from any semantic verdict. */
export type TransportFailureKind =
  | "UNREACHABLE" // the dial itself failed (gateway down / refused)
  | "ABORTED" // in-flight abort/timeout — the outcome is UNKNOWN if it was sent
  | "HTTP_ERROR" // a 4xx delivery-level answer (bad path/method/body)
  | "NOT_JSON"; // a 200 whose body is not JSON

export interface TransportFailure {
  readonly kind: TransportFailureKind;
  readonly detail: string;
}

/**
 * One dispatch's honest closure. Four lanes, never collapsed:
 * DELIVERED+OK (the validated result), DELIVERED with a non-OK
 * semantic verdict (REJECTED / FAILED / UNKNOWN — the honest name
 * rides the response), TRANSPORT (delivery failed), MISMATCH (the
 * wire deviates from the contract).
 */
export type DispatchResult<R> =
  | { readonly transport: "DELIVERED"; readonly status: "OK"; readonly result: R; readonly response: ValidatedResponse }
  | { readonly transport: "DELIVERED"; readonly status: "REJECTED" | "FAILED" | "UNKNOWN"; readonly response: ValidatedResponse }
  | { readonly transport: "TRANSPORT"; readonly failure: TransportFailure }
  | { readonly transport: "MISMATCH"; readonly error: string };

export interface GatewayClientConfig {
  /** The POST target. Default: the same-origin dev-proxy path. */
  readonly url?: string;
  /** Per-request deadline (ms). Default 10_000. */
  readonly timeoutMs?: number;
}

export class GatewayClient {
  private readonly url: string;
  private readonly timeoutMs: number;

  constructor(config: GatewayClientConfig = {}) {
    this.url = config.url ?? "/gateway/op";
    this.timeoutMs = config.timeoutMs ?? 10_000;
  }

  /** The one route (§8's single dispatch entry) — the raw envelope. */
  async postOp(envelope: RequestEnvelope): Promise<DispatchResult<Record<string, unknown>>> {
    let response: Response;
    try {
      response = await fetch(this.url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(envelope),
        signal: AbortSignal.timeout(this.timeoutMs),
      });
    } catch (error) {
      return { transport: "TRANSPORT", failure: transportFailureFrom(error) };
    }
    if (!response.ok) {
      const body = await response.text().catch(() => "");
      return {
        transport: "TRANSPORT",
        failure: { kind: "HTTP_ERROR", detail: `HTTP ${String(response.status)} ${body.slice(0, 200)}` },
      };
    }
    let document: unknown;
    try {
      document = await response.json();
    } catch {
      return { transport: "TRANSPORT", failure: { kind: "NOT_JSON", detail: "the 200 body is not JSON" } };
    }
    return validateEnvelopeResult(document);
  }

  /** `app.status` — the READ any client can make with no session. */
  async appStatus(): Promise<DispatchResult<AppStatusResult>> {
    const dispatch = await this.postOp({ operation: "app.status" });
    return narrow(dispatch, appStatusResultSchema, "app.status");
  }

  /**
   * `session.create` — the §8 first family's MUTATION. The session id
   * derives from (client_request_id, arguments): the same key + the
   * same material is idempotent (one effect); a conflicting reuse of
   * the key is DUPLICATE_REQUEST (the gateway's own law).
   */
  async sessionCreate(input: {
    readonly clientRequestId: string;
    readonly label?: string;
  }): Promise<DispatchResult<SessionCreateResult>> {
    const dispatch = await this.postOp({
      operation: "session.create",
      arguments: input.label === undefined ? {} : { label: input.label },
      client_request_id: input.clientRequestId,
    });
    return narrow(dispatch, sessionCreateResultSchema, "session.create");
  }

  /** `session.get` — the session document READ. */
  async sessionGet(sessionId: string): Promise<DispatchResult<SessionDocument>> {
    const dispatch = await this.postOp({
      operation: "session.get",
      session_id: sessionId,
    });
    return narrow(dispatch, sessionDocumentSchema, "session.get");
  }

  /** `session.attach` — the MUTATION that takes the lease (CAS on the revision). */
  async sessionAttach(input: {
    readonly sessionId: string;
    readonly expectedRevision: number;
    readonly clientRequestId: string;
    readonly label?: string;
  }): Promise<DispatchResult<SessionAttachResult>> {
    const dispatch = await this.postOp({
      operation: "session.attach",
      arguments: input.label === undefined ? {} : { label: input.label },
      session_id: input.sessionId,
      expected_revision: input.expectedRevision,
      client_request_id: input.clientRequestId,
    });
    return narrow(dispatch, sessionAttachResultSchema, "session.attach");
  }

  /** `session.detach` — the MUTATION that releases the lease. */
  async sessionDetach(input: {
    readonly sessionId: string;
    readonly expectedRevision: number;
    readonly leaseToken: string;
    readonly clientRequestId: string;
  }): Promise<DispatchResult<{ detached: true }>> {
    const dispatch = await this.postOp({
      operation: "session.detach",
      session_id: input.sessionId,
      expected_revision: input.expectedRevision,
      lease_token: input.leaseToken,
      client_request_id: input.clientRequestId,
    });
    return narrow(dispatch, sessionDetachResultSchema, "session.detach");
  }

  /**
   * `session.events` — the ordered replay READ (§13). The dual shape
   * stays distinct: REPLAY (the window after the cursor) or
   * RESYNC_REQUIRED (the cursor fell out of the retained tail).
   */
  async sessionEvents(input: {
    readonly sessionId: string;
    readonly sinceSequence: number;
  }): Promise<DispatchResult<SessionEventsResult>> {
    const dispatch = await this.postOp({
      operation: "session.events",
      session_id: input.sessionId,
      arguments: { since_sequence: input.sinceSequence },
    });
    const narrowed = narrow(dispatch, sessionEventsResultSchema, "session.events");
    if (narrowed.transport === "DELIVERED" && narrowed.status === "OK") {
      return { ...narrowed, result: classifyEvents(narrowed.result) };
    }
    return narrowed;
  }
}

/** REPLAY | RESYNC_REQUIRED — the discriminated form (§13). */
function classifyEvents(
  parsed: z.infer<typeof sessionEventsResultSchema>,
): SessionEventsResult {
  if ("events" in parsed) {
    return { kind: "REPLAY", events: parsed.events, last_sequence: parsed.last_sequence };
  }
  return {
    kind: "RESYNC_REQUIRED",
    last_sequence: parsed.last_sequence,
    retained_from: parsed.retained_from,
    snapshot: parsed.snapshot,
  };
}

/** Envelope validation — the shared postOp exit. The rejection law
 * (OK carries none; non-OK carries its name) lives in the schema's
 * refine — ONE owner, the backend's own `__post_init__` mirrored. */
function validateEnvelopeResult(
  document: unknown,
): DispatchResult<Record<string, unknown>> {
  try {
    const response = validateResponseDocument(document);
    if (response.status === "OK") {
      return {
        transport: "DELIVERED",
        status: "OK",
        result: (response.result ?? {}) as Record<string, unknown>,
        response,
      };
    }
    return {
      transport: "DELIVERED",
      status: response.status,
      response,
    };
  } catch (error) {
    return { transport: "MISMATCH", error: contractMismatchDetail(error) };
  }
}

/** Result narrowing — the per-operation schema over a delivered OK. */
function narrow<R>(
  dispatch: DispatchResult<Record<string, unknown>>,
  schema: z.ZodType<R>,
  operation: string,
): DispatchResult<R> {
  if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
    try {
      return { transport: "DELIVERED", status: "OK", result: schema.parse(dispatch.result), response: dispatch.response };
    } catch (error) {
      return { transport: "MISMATCH", error: `${operation} result: ${contractMismatchDetail(error)}` };
    }
  }
  return dispatch;
}

function transportFailureFrom(error: unknown): TransportFailure {
  if (error instanceof DOMException && (error.name === "TimeoutError" || error.name === "AbortError")) {
    return {
      kind: "ABORTED",
      detail: "the request was aborted or timed out — if it was sent, the outcome is UNKNOWN (no blind retry)",
    };
  }
  return { kind: "UNREACHABLE", detail: `the gateway dial failed: ${String(error)}` };
}

function contractMismatchDetail(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error);
}
