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

// -------------------------------------------------------------------- chat

/** chat.send's message roles — the closed set (`backend.py`'s own
 * CHAT_ROLES, mirrored). */
export const CHAT_ROLES = ["system", "user", "assistant"] as const;
export type ChatRole = (typeof CHAT_ROLES)[number];

/** One chat message — exactly `{role, content}` (the closed shape
 * the backend validates member-by-member). */
export interface ChatMessage {
  readonly role: ChatRole;
  readonly content: string;
}

/** The run family's EXECUTION ladder — the closed state set
 * (`lifecycles.py`'s EXECUTION_STATES, mirrored; the run registry
 * owns the transitions, the client only ever renders the observed
 * state — never a locally computed successor). */
export const EXECUTION_STATES = [
  "ADMITTED",
  "STARTING",
  "RUNNING",
  "COMPLETING",
  "COMPLETED",
  "FAILED",
  "CANCEL_REQUESTED",
  "CANCELED",
  "FAILED_TO_CANCEL",
  "UNKNOWN",
] as const;
export type ExecutionState = (typeof EXECUTION_STATES)[number];

/** `run.cancel`'s outcome vocabulary — the closed set (§12.3's
 * truthful cancellation request: a REQUEST that may already be
 * answered, already terminal, or past its last checkpoint). */
export const CANCELLATION_OUTCOMES = [
  "CANCEL_REQUESTED",
  "CANCELED",
  "FAILED_TO_CANCEL",
] as const;
export type CancellationOutcome = (typeof CANCELLATION_OUTCOMES)[number];

/** `chat.send` result — the ADMISSION identity (§8's long-running
 * law: identity returns immediately; `run.get` is the observation
 * path, never a second blocking call). */
export interface ChatSendResult {
  readonly deadline_seconds: number;
  readonly execution_id: string;
  readonly state: "STARTING";
  readonly work: "chat.completion";
}

/**
 * The OBSERVED backend identity — the props probe's two honest
 * shapes: the identity (model path + build) or the failed probe's
 * "unavailable" note (a failed probe never kills the chat —
 * readiness is not identity evidence).
 */
export type ChatBackendIdentity =
  | { readonly model: string | null; readonly build: unknown }
  | { readonly probe: "unavailable"; readonly detail: string };

/**
 * The chat completion's OBSERVED result (the run document's `result`
 * at COMPLETED) — §19.1's REQUESTED/EFFECTIVE pair rides it: the
 * `requested.temperature` is null where the call resolved through
 * the profile's BASE layer (the honest provenance, never guessed).
 */
export interface ChatCompletionResult {
  readonly content: string;
  readonly finish_reason: string;
  readonly backend: ChatBackendIdentity;
  readonly requested: {
    readonly max_tokens: number;
    readonly temperature: number | null;
  };
  readonly effective: {
    readonly max_tokens: number;
    readonly temperature: number;
  };
}

/**
 * One run document — `run.get`'s result (the work-kind-GENERIC
 * envelope: state/terminal/frozen inputs/deadline/progress/
 * diagnostics/artifact). The `result` member's shape is the WORK's
 * own (a chat completion, a model load, a digest) — the generic
 * mirror keeps it a closed record here; the chat surface narrows
 * chat.completion results through its own validator at the consumer.
 */
export interface RunDocument {
  readonly execution_id: string;
  readonly operation_id: string;
  readonly work: string;
  readonly state: ExecutionState;
  readonly terminal: boolean;
  readonly frozen_inputs: readonly (readonly [string, string])[];
  readonly request_digest: string;
  readonly deadline: {
    readonly started_monotonic: number;
    readonly deadline_monotonic: number;
  };
  readonly progress: Readonly<Record<string, unknown>> | null;
  readonly result: Readonly<Record<string, unknown>> | null;
  readonly failure_type: string | null;
  readonly diagnostics: readonly string[];
  readonly artifact: Readonly<Record<string, unknown>> | null;
}

/** `run.cancel` result — the cancellation REQUEST's observed outcome
 * (never itself a completion; §3's seam law). */
export interface RunCancelResult {
  readonly execution_id: string;
  readonly cancellation: CancellationOutcome;
}

// ------------------------------------------------------------------ models

/** The Model ladder — the closed state set (`lifecycles.py`'s
 * MODEL_STATES, mirrored; §8: a file on disk proves nothing,
 * SELECTED must not claim LOADED). */
export const MODEL_STATES = [
  "DISCOVERED",
  "VALIDATED",
  "SELECTED",
  "LOADING",
  "LOADED",
  "ACTIVE",
  "UNLOADING",
  "EVICTED",
  "FAILED",
] as const;
export type ModelState = (typeof MODEL_STATES)[number];

/** `model.list`'s directory classification — the closed pair
 * (`models.py`'s own constants; the CORRUPT form raises, never
 * rides the document). */
export const MODEL_DIRECTORY_STATES = ["OK", "MISSING"] as const;
export type ModelDirectoryState = (typeof MODEL_DIRECTORY_STATES)[number];

/** One discovered model — the §20 scan's entry (the strong identity
 * is null until computed; the cheap fingerprint is the screen,
 * never the correctness identity). */
export interface ModelListEntry {
  readonly logical_name: string;
  readonly location: string;
  readonly size_bytes: number;
  readonly mtime_ns: number;
  readonly content_digest: string | null;
  readonly state: "DISCOVERED";
}

/** `model.list` result — the discovery scan (READ, no arguments):
 * the directory classification + the entries + the folder itself
 * (the open-folder answer, never a local guess — wb-10). */
export interface ModelListResult {
  readonly directory_state: ModelDirectoryState;
  readonly models: readonly ModelListEntry[];
  readonly models_root: string;
}

/** `model.states` result — the Model-lifecycle read view (§11's
 * MACHINE as the load-state owner serves it): the per-model states
 * + the ACTIVE slot (at most one — the slot is single). */
export interface ModelStatesResult {
  readonly states: Readonly<Record<string, ModelState>>;
  readonly active: string | null;
}

// ------------------------------------------- models (the surface's own row)

/**
 * The run kinds the Models surface starts over `run.start` — the
 * closed set of the app composition's model-family work kinds
 * (`compose_workbench_operations`'s own wiring: digest + import
 * unconditionally, fetch with the injected fetcher). The registry's
 * FULL kind vocabulary stays backend-owned — this is the surface's
 * consumed slice, never a re-encoding of the registry.
 */
export const MODEL_WORK_KINDS = [
  "model.fetch",
  "model.import",
  "model.digest",
] as const;
export type ModelWorkKind = (typeof MODEL_WORK_KINDS)[number];

/**
 * `run.start`'s per-kind ARGUMENT sets — the closed forms the three
 * model work kinds' own `validate_arguments` gates admit (mirrored
 * per kind; a foreign key or a wrong type is the backend's own
 * DOMAIN_REJECTED, rendered verbatim — never client-coerced).
 */
export type ModelRunStartInput =
  | {
      readonly work: "model.fetch";
      /** a direct http(s) URL, a huggingface.co URL, or the hf:repo/file shorthand */
      readonly url: string;
      /** absent = the URL's own derived file name */
      readonly logicalName?: string;
    }
  | {
      readonly work: "model.import";
      /** ABSOLUTE file paths (the web form's honest input — the native picker is the Tauri row's own concern) */
      readonly paths: readonly string[];
    }
  | {
      readonly work: "model.digest";
      readonly logicalName: string;
    };

/**
 * `run.start` result — the ADMISSION identity over any work kind
 * (§8's long-running law: identity returns immediately; `run.get` is
 * the observation path). `work` is the registry's own echo (any
 * registered kind — the mirror never re-encodes the registry's full
 * vocabulary; the surface's own starts are the three above).
 */
export interface RunStartResult {
  readonly execution_id: string;
  readonly work: string;
  readonly deadline_seconds: number;
}

/**
 * `model.load` / `model.unload` result — the shared ADMISSION shape
 * (the two handlers' own identical form): the ladder's fast dispatch
 * walks to SELECTED (load) / checks ACTIVE (unload), admits the
 * minutes-class run, and answers the execution identity — the port
 * call itself rides the worker thread (`run.get` is the poll path).
 */
export interface ModelDispatchResult {
  readonly deadline_seconds: number;
  readonly execution_id: string;
  readonly logical_name: string;
  readonly state: "STARTING";
  readonly work: "model.load" | "model.unload";
}

/**
 * The fetch run's live PROGRESS document (the fetcher's own report
 * shape, mirrored closed at the consumer depth): `total_bytes` is
 * null when the wire does not name the size (streamed answers) — the
 * percentage line renders honestly absent, never a guessed total.
 */
export interface ModelFetchProgress {
  readonly downloaded_bytes: number;
  readonly logical_name: string;
  readonly total_bytes: number | null;
}

/**
 * The import run's live PROGRESS document (the per-chunk report: the
 * file's index within the frozen path list, the copied bytes of the
 * CURRENT file, and its total — a multi-GB copy stays cancellable
 * and observable, never a frozen UI).
 */
export interface ModelImportProgress {
  readonly logical_name: string;
  readonly file_index: number;
  readonly file_count: number;
  readonly copied_bytes: number;
  readonly total_bytes: number;
}

/** The fetch run's OBSERVED result at COMPLETED — the landed file
 * (the atomic rename already happened; the NEXT discovery scan sees
 * it) + the source URL, verbatim. */
export interface ModelFetchResult {
  readonly location: string;
  readonly logical_name: string;
  readonly size_bytes: number;
  readonly url: string;
}

/** One landed local file (the import run's honest per-file truth). */
export interface ModelImportedFile {
  readonly logical_name: string;
  readonly size_bytes: number;
}

/** The import run's OBSERVED result at COMPLETED — the landed files
 * (an interrupted import leaves the ALREADY-LANDED files real; the
 * run's terminal tells the truth about the rest). */
export interface ModelImportResult {
  readonly imported: readonly ModelImportedFile[];
  readonly count: number;
}

/** The digest run's OBSERVED result at COMPLETED — the §9 strong
 * identity the run computed (also recorded into the registry: the
 * NEXT model.list carries it on the entry). */
export interface ModelDigestResult {
  readonly chunks: number;
  readonly content_digest: string;
  readonly logical_name: string;
  readonly size_bytes: number;
}

/** The load run's OBSERVED result at COMPLETED — the backend's own
 * reply document (the managed spawn's command or the attached load's
 * answer) rides verbatim; `reply` is backend-owned DATA. */
export interface ModelLoadResult {
  readonly logical_name: string;
  readonly location: string;
  readonly reply: Readonly<Record<string, unknown>>;
  readonly state: "ACTIVE";
}

/** The unload run's OBSERVED result at COMPLETED — the graceful
 * stop's own answer, verbatim. */
export interface ModelUnloadResult {
  readonly logical_name: string;
  readonly reply: Readonly<Record<string, unknown>>;
  readonly state: "EVICTED";
}

// --------------------------------------------------------------- inference

/** The compact projection's own control slice — the fields the CHAT
 * surface reads from one control document (id/value/state/source).
 * The control vocabulary itself (85 controls, their flags, notes,
 * forms) is backend-owned DATA — the UI never re-encodes it (§21.2:
 * the data-driven law); the Inference surface's own row mirrors the
 * depth IT consumes. */
export interface InferenceControlSlice {
  readonly id: string;
  readonly value: unknown;
  readonly state: string;
  readonly source: string;
}

/**
 * `inference.read` result — the Chat-side COMPACT projection
 * (§21.2: Chat carries only a compact contextual projection of the
 * inference state + the link; the full control depth lives in the
 * Inference surface, never here). The validated members are exactly
 * what the projection renders: the profile's name, the controls
 * array (each entry's identity/effective value/state/source), the
 * applies constant, the managed liveness, and the pinned ids. The
 * document's REMAINING members (profile, presets, categories, the
 * sampler chain, the compiled preview) ride the wire unconsumed —
 * validating their depth would re-encode the vocabulary the law
 * forbids the UI to own.
 */
export interface InferenceReadResult {
  readonly profile_name: string;
  readonly controls: readonly InferenceControlSlice[];
  readonly applies: "next-spawn";
  readonly managed_live: boolean;
  readonly pinned: readonly string[];
}

// --------------------------------------------- inference (the workspace row)

/**
 * The resolved-state vocabulary — the closed set (`resolver.py`'s own
 * STATES, mirrored; LLAMA_CPP_INFERENCE_CONTROL_LAW §7 owns the
 * semantics: configured-but-ineffective controls stay VISIBLE with
 * their reason, never hidden).
 */
export const INFERENCE_STATES = [
  "EFFECTIVE",
  "AUTO",
  "INACTIVE",
  "INEFFECTIVE",
  "CONFLICT",
  "RISK",
  "EXPERIMENTAL",
  "UNCLASSIFIED",
  "LEGACY",
  "REMOVED",
] as const;
export type InferenceState = (typeof INFERENCE_STATES)[number];

/** The control kinds — the closed minimum set (the LAW §3's own). */
export const INFERENCE_KINDS = ["value", "mode", "toggle", "chain", "display"] as const;
export type InferenceKind = (typeof INFERENCE_KINDS)[number];

/** The editor's value types — the closed set (`library.py`'s own;
 * the DATA-DRIVEN law: the editors build over the control's own
 * value_type/forms/limits metadata, the UI never re-encodes the
 * vocabulary). */
export const INFERENCE_VALUE_TYPES = ["int", "float", "bool", "enum", "text", "gpu_layers"] as const;
export type InferenceValueType = (typeof INFERENCE_VALUE_TYPES)[number];

/** The scope model — the closed set (the LAW §5's own). */
export const INFERENCE_SCOPES = ["spawn", "request", "spawn+request"] as const;
export type InferenceScope = (typeof INFERENCE_SCOPES)[number];

/**
 * One control's RESOLVED document — the resolver's own field set
 * (`resolve()`'s control_document, mirrored closed). `value`,
 * `baseline`, and `upstream_default` stay `unknown`: they are JSON
 * scalars whose per-control forms are backend-owned DATA (§21.2's
 * data-driven law) — the editors dispatch over the metadata fields,
 * never over a re-encoded value vocabulary.
 */
export interface InferenceControlDocument {
  readonly id: string;
  readonly name: string;
  readonly category: string;
  readonly kind: InferenceKind;
  readonly scope: InferenceScope;
  readonly flag: string;
  readonly field: string;
  readonly value: unknown;
  readonly value_doc: string;
  readonly value_type: InferenceValueType;
  readonly forms: readonly string[];
  readonly minimum: number | null;
  readonly maximum: number | null;
  readonly step: number;
  readonly advanced: boolean;
  readonly source: string;
  readonly state: InferenceState;
  readonly reasons: readonly string[];
  readonly baseline: unknown;
  readonly upstream_default: unknown;
  readonly notes: readonly string[];
}

/** One sampler-chain member's resolved document (the LAW §11: the
 * ordered first-class object; membership and value are SEPARATE
 * concerns — `enabled=false` removes the member from the emitted
 * chain while its value family stays configured). */
export interface InferenceChainMember {
  readonly id: string;
  readonly name: string;
  readonly enabled: boolean;
  readonly order: number;
  readonly value: unknown;
  readonly state: InferenceState;
  readonly reasons: readonly string[];
}

/** One preset's transparent document (the LAW §14: a concrete
 * STARTING POINT applying as a plain update — the `values` keys are
 * the backend's own field vocabulary, loose by the data-driven law). */
export interface InferencePreset {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly values: Readonly<Record<string, unknown>>;
}

/** One category's honest count (the LAW §16: every family its own
 * category, never one "advanced parameters" bucket). */
export interface InferenceCategory {
  readonly id: string;
  readonly controls: number;
}

/**
 * The chain membership on the wire — the profile document's own
 * `{id, enabled}` form (the whole 9-member document; the LAW §11:
 * the chain validation accepts only the WHOLE document, a partial
 * edit refuses loud).
 */
export interface InferenceProfileChainItem {
  readonly id: string;
  readonly enabled: boolean;
}

/**
 * `inference.read` result — the Inference WORKSPACE's own full
 * projection (§21.2: the full control depth lives HERE, never in
 * Chat). The seam drops the unconsumed members (`profile`'s raw
 * values vocabulary, `request_layer`) at the projection — the
 * surfaces never see a loose index signature; the values the
 * editors read ride the per-control `value` fields (the validated
 * depth).
 */
export interface InferenceDocument {
  readonly profile_name: string;
  readonly categories: readonly InferenceCategory[];
  readonly controls: readonly InferenceControlDocument[];
  readonly sampler_chain: readonly InferenceChainMember[];
  readonly chain_order: readonly string[];
  readonly deterministic: boolean;
  readonly presets: readonly InferencePreset[];
  readonly pinned: readonly string[];
  readonly managed_live: boolean;
  readonly applies: "next-spawn";
  readonly compiled_preview: string | null;
  /** rides only when the managed server is live (verbatim). */
  readonly note?: string | undefined;
}

/**
 * `inference.update`'s closed partial document — the store's own law
 * (`store.py`: `name` / `sampler_chain` / `pinned` / the value
 * fields; absent fields unchanged). The VALUE-field keys are
 * backend-owned data (the 85-control vocabulary, never re-encoded
 * here) — they ride the `values` record, and only the CHANGED keys
 * enter it (the partial law, the Settings row's own form).
 */
export interface InferenceUpdateChanges {
  readonly name?: string;
  readonly sampler_chain?: readonly InferenceProfileChainItem[];
  readonly pinned?: readonly string[];
  readonly values?: Readonly<Record<string, unknown>>;
}
