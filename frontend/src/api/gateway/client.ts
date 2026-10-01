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
  BackendSettingsResult,
  LaunchSettingsDocument,
  ObservatoryReadResult,
  ObservatoryRunsResult,
  RequestEnvelope,
  SessionAttachResult,
  SessionCreateResult,
  SessionDocument,
  SessionEventsResult,
} from "./contracts.ts";
import {
  appStatusResultSchema,
  backendSettingsResultSchema,
  observatoryReadResultSchema,
  observatoryRunsResultSchema,
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

  /**
   * `observatory.runs` — the HISTORY discovery scan (READ, no
   * arguments, no session): the committed runs over the canonical
   * logs root. The durable world's entry point — never mixed with
   * the LIVE session tail's cursors (the dual-read law, §4).
   */
  async observatoryRuns(): Promise<DispatchResult<ObservatoryRunsResult>> {
    const dispatch = await this.postOp({ operation: "observatory.runs" });
    return narrow(dispatch, observatoryRunsResultSchema, "observatory.runs");
  }

  /**
   * `observatory.read` — ONE run's bounded HISTORY window (READ,
   * `{run, after?, limit?}`). The cursor is an event id (the semantic
   * identity — never a row index); the backend bounds the window
   * (default 50, cap 200) and answers `next_after` for forward
   * pagination. A domain violation (NO MATCH / stale cursor / corrupt
   * log / bad limit) is a DELIVERED REJECTED with the observed cause —
   * rendered verbatim, never fabricated into an empty window.
   */
  async observatoryRead(input: {
    readonly run: string;
    readonly after?: string;
    readonly limit?: number;
  }): Promise<DispatchResult<ObservatoryReadResult>> {
    const readArguments: Record<string, unknown> = { run: input.run };
    if (input.after !== undefined) {
      readArguments["after"] = input.after;
    }
    if (input.limit !== undefined) {
      readArguments["limit"] = input.limit;
    }
    const dispatch = await this.postOp({
      operation: "observatory.read",
      arguments: readArguments,
    });
    return narrow(dispatch, observatoryReadResultSchema, "observatory.read");
  }

  /**
   * `backend.settings` — the launch-settings READ (session-free, no
   * arguments): the effective DEPLOYMENT document + the managed
   * backend's liveness + the composition's command preview. The
   * store's own truth — the surface never infers effective state
   * from widget values (§8).
   */
  async backendSettings(): Promise<DispatchResult<BackendSettingsResult>> {
    const dispatch = await this.postOp({ operation: "backend.settings" });
    return narrow(dispatch, backendSettingsResultSchema, "backend.settings");
  }

  /**
   * `backend.settings.update` — the closed partial UPDATE (MUTATION,
   * session-scoped): only the CHANGED fields ride the wire (absent
   * fields unchanged — the store's own partial law); a fresh
   * `client_request_id` per explicit attempt (G4 — no blind retry,
   * the idempotency key is the caller's decision); the returned
   * document is the new current (the caller's evidence, never a
   * guess about the file). A domain violation (unknown field / wrong
   * type) is a DELIVERED REJECTED with the observed cause — rendered
   * verbatim, never coerced.
   */
  async backendSettingsUpdate(input: {
    readonly sessionId: string;
    readonly clientRequestId: string;
    readonly changes: Partial<LaunchSettingsDocument>;
  }): Promise<DispatchResult<BackendSettingsResult>> {
    const dispatch = await this.postOp({
      operation: "backend.settings.update",
      arguments: input.changes as Record<string, unknown>,
      session_id: input.sessionId,
      client_request_id: input.clientRequestId,
    });
    return narrow(
      dispatch,
      backendSettingsResultSchema,
      "backend.settings.update",
    );
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
