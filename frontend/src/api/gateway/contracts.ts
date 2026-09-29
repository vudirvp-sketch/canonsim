/**
 * The gateway contract types — the client-side mirror of
 * `workbench/api/contract.py` (GATEWAY_SCHEMA_IDENTITY
 * `canon_workbench_gateway@0.1`).
 *
 * LAW (FRONTEND_WEB_LAW §3, S0-1): these TYPES are never trusted
 * from the wire. Every payload enters as `unknown` and passes the
 * runtime validators (`validators.ts`) before any UI use. The types
 * below are the *output* of successful validation, nothing else.
 * The closed vocabularies are backend-owned; this mirror exists so
 * the compiler knows the same closed sets the gateway enforces.
 */

/** §8's minimum rejection/failure distinctions — the closed set. */
export const REJECTIONS = [
  "AUTH_FAILED",
  "AUTHZ_DENIED",
  "DUPLICATE_REQUEST",
  "STALE_REVISION",
  "LEASE_EXPIRED",
  "DOMAIN_REJECTED",
  "RUNTIME_FAILED",
  "SENT_OUTCOME_UNKNOWN",
] as const;
export type Rejection = (typeof REJECTIONS)[number];

/** §4's exposure axis — the closed set. */
export const EXPOSURES = ["LOOPBACK", "LAN", "TUNNEL"] as const;
export type Exposure = (typeof EXPOSURES)[number];

/** The dispatch pipeline's terminal statuses — the closed set. */
export const DISPATCH_STATUSES = ["OK", "REJECTED", "FAILED", "UNKNOWN"] as const;
export type DispatchStatus = (typeof DISPATCH_STATUSES)[number];

/** §12.1's dispatch-outcome vocabulary — the closed set. */
export const DISPATCH_OUTCOMES = [
  "NOT_SENT",
  "SENT_AND_TERMINAL",
  "SENT_OUTCOME_UNKNOWN",
] as const;
export type DispatchOutcome = (typeof DISPATCH_OUTCOMES)[number];

/** §12.1's status -> outcome law (G4: UNKNOWN is never a blind retry). */
export const DISPATCH_OUTCOME_FOR_STATUS: Readonly<
  Record<DispatchStatus, DispatchOutcome>
> = {
  OK: "SENT_AND_TERMINAL",
  FAILED: "SENT_AND_TERMINAL",
  REJECTED: "NOT_SENT",
  UNKNOWN: "SENT_OUTCOME_UNKNOWN",
};

/** §13's ordered-stream event types — the closed set. */
export const EVENT_TYPES = [
  "SESSION_CREATED",
  "SESSION_ATTACHED",
  "SESSION_DETACHED",
  "OPERATION_EFFECT",
] as const;
export type EventType = (typeof EVENT_TYPES)[number];

/** The gateway's own schema identity (byte-mirrored). */
export const GATEWAY_SCHEMA_IDENTITY = "canon_workbench_gateway@0.1";

/** One client request, wire-neutral (§8). `client_request_id` is the
 * idempotency key — REQUIRED on mutations (G4). */
export interface RequestEnvelope {
  readonly operation: string;
  readonly arguments?: Readonly<Record<string, unknown>>;
  readonly client_request_id?: string;
  readonly session_id?: string;
  readonly expected_revision?: number;
  readonly lease_token?: string;
  readonly auth_token?: string;
}

/** The dispatch's terminal answer, wire-neutral. */
export interface ResponseDocument {
  readonly status: DispatchStatus;
  readonly operation_id: string;
  readonly rejection?: Rejection;
  readonly result?: Readonly<Record<string, unknown>>;
  readonly session_id?: string;
  readonly revision?: number;
  readonly sequence?: number;
  readonly duplicate?: boolean;
}

/** §12.1's outcome for a response — the closed mapping. */
export function dispatchOutcome(response: ResponseDocument): DispatchOutcome {
  return DISPATCH_OUTCOME_FOR_STATUS[response.status];
}

/** One ordered session event (§8's envelope, §13's stream law). */
export interface EventEnvelope {
  readonly event_id: string;
  readonly session_id: string;
  readonly operation_id: string;
  readonly sequence: number;
  readonly event_type: EventType;
  readonly observed_at: number;
  readonly payload: Readonly<Record<string, unknown>>;
}

/** `app.status` result (construction-stable only — no clock, no counters). */
export interface AppStatusResult {
  readonly service: string;
  readonly contract: string;
  readonly exposure: Exposure;
  readonly auth_required: boolean;
  readonly operations: readonly string[];
}

/** `session.get` / the session document. */
export interface SessionDocument {
  readonly session_id: string;
  readonly attached: boolean;
  readonly created_observed_at: number;
  readonly event_sequence: number;
  readonly revision: number;
}

/** `session.create` result. */
export interface SessionCreateResult {
  readonly session_id: string;
  readonly revision: number;
  readonly event_sequence: number;
}

/** `session.attach` result. */
export interface SessionAttachResult {
  readonly attached: boolean;
  readonly lease_seconds: number;
  readonly lease_token: string;
}

/**
 * `session.events` result — the dual shape (§13): the ordered replay
 * window, or the RESYNC_REQUIRED verdict when the requested cursor
 * fell out of the retained tail (FIFO eviction, never canon loss).
 */
export type SessionEventsResult =
  | { readonly kind: "REPLAY"; readonly events: readonly EventEnvelope[]; readonly last_sequence: number }
  | {
      readonly kind: "RESYNC_REQUIRED";
      readonly last_sequence: number;
      readonly retained_from: number;
      readonly snapshot: SessionDocument;
    };
