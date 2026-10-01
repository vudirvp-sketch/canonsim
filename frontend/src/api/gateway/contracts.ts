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

// --------------------------------------------------------------- observatory

/**
 * §14's authority axis as the read model serves it — the closed set
 * the CANONICAL member owns today (the perception/assurance profiles
 * are later rows over their own read models, never fabricated here).
 */
export const OBSERVATORY_AUTHORITIES = ["CANONICAL"] as const;
export type ObservatoryAuthority = (typeof OBSERVATORY_AUTHORITIES)[number];

/** The reading profile vocabulary — the canon member is the only
 * honest value for a direct committed-log read. */
export const OBSERVATORY_PROFILES = ["CANON_VIEW"] as const;
export type ObservatoryProfile = (typeof OBSERVATORY_PROFILES)[number];

/** The event importance vocabulary (`schemas/event.schema.json`'s own
 * enum — the pack rule computes it, tune-1/D-059). */
export const EVENT_IMPORTANCES = ["low", "medium", "high"] as const;
export type EventImportance = (typeof EVENT_IMPORTANCES)[number];

/** One discovered run's parsed header (or null — a corrupt first line
 * never fails the whole listing; the per-run error rides alongside). */
export interface ObservatoryRunHeader {
  readonly seed: number;
  readonly pack: string;
  readonly schema_version: string;
}

/** One `*.jsonl` run in the discovery scan — the honest degradation
 * pair: `header` XOR `error` (a blank/corrupt/unreadable first line
 * is the run's own observed error, never a raised listing). */
export interface ObservatoryRunEntry {
  readonly name: string;
  readonly size_bytes: number;
  readonly header: ObservatoryRunHeader | null;
  readonly error: string | null;
}

/** `observatory.runs` result — the discovery scan (READ, no arguments). */
export interface ObservatoryRunsResult {
  readonly runs_root: string;
  readonly runs: readonly ObservatoryRunEntry[];
}

/** One state change's bounded projection — `from`/`to` are JSON
 * values of any type (the event schema's own law). */
export interface ObservatoryStateChange {
  readonly entity: string;
  readonly prop: string;
  readonly from: unknown;
  readonly to: unknown;
}

/**
 * One committed event's bounded projection — the HISTORY row (LAW
 * §5.1: the selection consumes this SAME document; no second
 * per-event op). `id` is the semantic identity (the cursor AND the
 * selection key — never a row index); `cause` is declared DATA, never
 * an implied causal conclusion.
 */
export interface ObservatoryEventRow {
  readonly id: string;
  readonly t: number;
  readonly type: string;
  readonly actor: string;
  readonly kind: string;
  readonly importance: EventImportance;
  readonly cause: string | null;
  readonly authority: ObservatoryAuthority;
  readonly state_changes: readonly ObservatoryStateChange[];
  readonly knowledge_count: number;
  readonly provenance: Readonly<Record<string, unknown>>;
}

/** The read window's committed-log header (content truths only). */
export interface ObservatoryReadHeader {
  readonly schema_version: string;
  readonly seed: number;
  readonly python: string;
  readonly commit: string;
  readonly pack: string;
}

/**
 * `observatory.read` result — ONE run's bounded event window (READ,
 * `{run, after?, limit?}`): the cursor is an event id (the semantic
 * identity), the window is bounded (default 50, cap 200 — the
 * backend's own ceiling), `next_after` is the forward pagination
 * token or null at the run's end.
 */
export interface ObservatoryReadResult {
  readonly run: string;
  readonly header: ObservatoryReadHeader;
  readonly profile: ObservatoryProfile;
  readonly authority: ObservatoryAuthority;
  readonly total_events: number;
  readonly window: {
    readonly after: string;
    readonly limit: number;
    readonly events: readonly ObservatoryEventRow[];
    readonly next_after: string | null;
  };
}

// ----------------------------------------------------------------- settings

/**
 * The launch-settings DEPLOYMENT field set — the closed set
 * (`workbench/application/settings.py`'s own `_FIELDS`, mirrored).
 * The semantic generation controls live in the inference profile
 * store (inf-1's Settings ≠ Inference Control split) — this mirror
 * never invents a fourth field.
 */
export const SETTINGS_FIELDS = [
  "llama_server_exe",
  "no_webui",
  "extra_args",
] as const;
export type SettingsField = (typeof SETTINGS_FIELDS)[number];

/**
 * The persisted settings document — the wire form of the store's
 * `LaunchSettings`. `llama_server_exe` is a PREFERENCE ("" =
 * auto-discovery — the composition root owns the resolution and the
 * preview shows the effective command), `extra_args` the RAW
 * compatibility/debug escape hatch (the law's §13 — duplicate flag
 * ownership against the semantic layer rejects loudly at the compile
 * step, never a silent merge).
 */
export interface LaunchSettingsDocument {
  readonly llama_server_exe: string;
  readonly no_webui: boolean;
  readonly extra_args: string;
}

/**
 * `backend.settings` / `backend.settings.update` result — the SAME
 * document shape (the update returns the new current): the effective
 * settings, the managed backend's liveness, the honest applies
 * constant (the store's own law: a saved update is EFFECTIVE at the
 * NEXT managed spawn — a LIVE server keeps its flags until
 * unloaded), and the composition root's compiled command preview
 * (the §18 EFFECTIVE display). `note` rides only when the managed
 * server is live — rendered verbatim, never fabricated client-side.
 */
export interface BackendSettingsResult {
  readonly settings: LaunchSettingsDocument;
  readonly managed_live: boolean;
  readonly applies: "next-spawn";
  readonly command_preview: string | null;
  /** rides only when the managed server is live (verbatim). */
  readonly note?: string | undefined;
}
