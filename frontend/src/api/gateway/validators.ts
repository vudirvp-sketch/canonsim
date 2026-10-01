/**
 * The runtime validators (S0-1's boundary law): every wire payload
 * enters as `unknown` and is validated HERE — raw JSON never reaches
 * a component. The schemas mirror the backend's closed-document law
 * (strict shapes: unknown keys are REJECTED, not ignored), the
 * closed vocabularies (`contracts.ts`), and §13's dual
 * `session.events` shape (REPLAY | RESYNC_REQUIRED).
 *
 * A validation failure is a CONTRACT MISMATCH: it is reported as
 * such (never silently coerced, never passed through partially).
 */
import { z } from "zod";

import {
  CANCELLATION_OUTCOMES,
  CHAT_ROLES,
  DISPATCH_STATUSES,
  EVENT_IMPORTANCES,
  EVENT_TYPES,
  EXPOSURES,
  EXECUTION_STATES,
  INFERENCE_KINDS,
  INFERENCE_SCOPES,
  INFERENCE_STATES,
  INFERENCE_VALUE_TYPES,
  MODEL_DIRECTORY_STATES,
  MODEL_STATES,
  OBSERVATORY_AUTHORITIES,
  OBSERVATORY_PROFILES,
  REJECTIONS,
} from "./contracts.ts";

/** A non-empty string — the identity fields' shared shape. */
const nonEmptyString = z.string().min(1);

/** A finite float (the closed-document law: no NaN/Infinity). */
const finiteFloat = z.number().finite();

/** A non-negative int — sequences/revision's shared shape. */
const nonNegativeInt = z.number().int().min(0);

/** A strictly positive int — the event sequence's shape (starts at 1). */
const positiveInt = z.number().int().min(1);

/**
 * The response document — the wire form (`to_mapping`'s shape: absent
 * fields stay absent, `duplicate` only rides when true). Strict: an
 * unknown key is a contract mismatch, exactly as the backend's
 * `from_mapping` treats it. The refine mirrors the backend's own
 * `__post_init__` law: OK carries NO rejection; a non-OK carries
 * its rejection — the two lanes never mix.
 */
export const responseDocumentSchema = z
  .strictObject({
    status: z.enum(DISPATCH_STATUSES),
    operation_id: nonEmptyString,
    rejection: z.enum(REJECTIONS).optional(),
    result: z.record(z.string(), z.unknown()).optional(),
    session_id: nonEmptyString.optional(),
    revision: nonNegativeInt.optional(),
    sequence: nonNegativeInt.optional(),
    duplicate: z.literal(true).optional(),
  })
  .refine(
    (document) =>
      document.status === "OK" ? document.rejection === undefined : document.rejection !== undefined,
    { message: "OK carries no rejection; a non-OK carries its rejection" },
  );

/** One ordered session event (§8's envelope). */
export const eventEnvelopeSchema = z.strictObject({
  event_id: nonEmptyString,
  session_id: nonEmptyString,
  operation_id: nonEmptyString,
  sequence: positiveInt,
  event_type: z.enum(EVENT_TYPES),
  observed_at: finiteFloat,
  payload: z.record(z.string(), z.unknown()),
});

/** The session document (`session.get` / the RESYNC snapshot). */
export const sessionDocumentSchema = z.strictObject({
  session_id: nonEmptyString,
  attached: z.boolean(),
  created_observed_at: finiteFloat,
  event_sequence: nonNegativeInt,
  revision: nonNegativeInt,
});

/** `app.status` result — construction-stable fields only. */
export const appStatusResultSchema = z.strictObject({
  service: nonEmptyString,
  contract: nonEmptyString,
  exposure: z.enum(EXPOSURES),
  auth_required: z.boolean(),
  operations: z.array(nonEmptyString),
});

/** `session.create` result. */
export const sessionCreateResultSchema = z.strictObject({
  session_id: nonEmptyString,
  revision: nonNegativeInt,
  event_sequence: nonNegativeInt,
});

/** `session.attach` result. */
export const sessionAttachResultSchema = z.strictObject({
  attached: z.boolean(),
  lease_seconds: finiteFloat,
  lease_token: nonEmptyString,
});

/** `session.detach` result. */
export const sessionDetachResultSchema = z.strictObject({
  detached: z.literal(true),
});

/**
 * `session.events` — the dual §13 shape. The validator itself keeps
 * the two worlds distinct: a REPLAY document and a RESYNC document
 * never validate as each other.
 */
const replayShape = z.strictObject({
  events: z.array(eventEnvelopeSchema),
  last_sequence: nonNegativeInt,
});
const resyncShape = z.strictObject({
  resync: z.literal("RESYNC_REQUIRED"),
  last_sequence: nonNegativeInt,
  retained_from: positiveInt,
  snapshot: sessionDocumentSchema,
});
export const sessionEventsResultSchema = z.union([
  replayShape,
  resyncShape,
]);

// --------------------------------------------------------------- observatory

/** Any JSON value — `from`/`to` are "any type" by the event schema's
 * own law; the recursive form requires the KEY present (a missing
 * member is a contract mismatch, never a silent undefined). */
const jsonValue: z.ZodType<unknown> = z.lazy(() =>
  z.union([
    z.string(),
    z.number(),
    z.boolean(),
    z.null(),
    z.array(jsonValue),
    z.record(z.string(), jsonValue),
  ]),
);

/** One discovered run's header — the listing's cheap arm. */
const observatoryRunHeaderSchema = z.strictObject({
  seed: z.number(),
  pack: nonEmptyString,
  schema_version: nonEmptyString,
});

/** The discovery scan's entry — the honest degradation pair. */
export const observatoryRunEntrySchema = z.strictObject({
  name: nonEmptyString,
  size_bytes: nonNegativeInt,
  header: observatoryRunHeaderSchema.nullable(),
  error: z.string().nullable(),
});

/** `observatory.runs` result — the discovery scan. */
export const observatoryRunsResultSchema = z.strictObject({
  runs_root: z.string(),
  runs: z.array(observatoryRunEntrySchema),
});

/** One state change's bounded projection. */
const observatoryStateChangeSchema = z.strictObject({
  entity: nonEmptyString,
  prop: nonEmptyString,
  from: jsonValue,
  to: jsonValue,
});

/** One committed event's bounded row — the HISTORY evidence. */
export const observatoryEventRowSchema = z.strictObject({
  id: nonEmptyString,
  t: nonNegativeInt,
  type: nonEmptyString,
  actor: nonEmptyString,
  kind: nonEmptyString,
  importance: z.enum(EVENT_IMPORTANCES),
  cause: z.string().nullable(),
  authority: z.enum(OBSERVATORY_AUTHORITIES),
  state_changes: z.array(observatoryStateChangeSchema),
  knowledge_count: nonNegativeInt,
  provenance: z.record(z.string(), z.unknown()),
});

/** `observatory.read` result — one run's bounded event window. */
export const observatoryReadResultSchema = z.strictObject({
  run: nonEmptyString,
  header: z.strictObject({
    schema_version: nonEmptyString,
    seed: z.number(),
    python: nonEmptyString,
    commit: nonEmptyString,
    pack: nonEmptyString,
  }),
  profile: z.enum(OBSERVATORY_PROFILES),
  authority: z.enum(OBSERVATORY_AUTHORITIES),
  total_events: nonNegativeInt,
  window: z.strictObject({
    after: z.string(),
    limit: positiveInt,
    events: z.array(observatoryEventRowSchema),
    next_after: z.string().nullable(),
  }),
});

// ----------------------------------------------------------------- settings

/**
 * The launch-settings document — the closed field set, each field its
 * own closed type (the backend's `_validate_field` law, mirrored: a
 * wrong type is rejected loud, never clamped; an unknown key is a
 * contract mismatch, exactly as the store treats it).
 */
export const launchSettingsDocumentSchema = z.strictObject({
  llama_server_exe: z.string(),
  no_webui: z.boolean(),
  extra_args: z.string(),
});

/**
 * `backend.settings` / `backend.settings.update` result — the store's
 * own document: settings + the managed liveness + the applies
 * constant (a literal, never a client guess) + the composition's
 * command preview (string | null); the note rides only when live.
 */
export const backendSettingsResultSchema = z.strictObject({
  settings: launchSettingsDocumentSchema,
  managed_live: z.boolean(),
  applies: z.literal("next-spawn"),
  command_preview: z.string().nullable(),
  note: z.string().optional(),
});

/** The transport-level 4xx JSON error (the delivery half's shape). */
export const transportErrorSchema = z.strictObject({
  error: nonEmptyString,
  path: z.string().optional(),
});

// -------------------------------------------------------------------- chat

/** One chat message — exactly `{role, content}` over the closed role
 * set (the backend's member-by-member validation, mirrored). */
export const chatMessageSchema = z.strictObject({
  role: z.enum(CHAT_ROLES),
  content: nonEmptyString,
});

/** `chat.send` result — the admission identity (the state is
 * STARTING at admission by the handler's own law; the observation
 * path is run.get, never a second blocking call). */
export const chatSendResultSchema = z.strictObject({
  deadline_seconds: finiteFloat,
  execution_id: nonEmptyString,
  state: z.literal("STARTING"),
  work: z.literal("chat.completion"),
});

/** The backend identity probe's two honest shapes (a failed probe is
 * the honest "unavailable" note — never a fabricated identity). */
const chatBackendIdentitySchema = z.union([
  z.strictObject({
    model: z.string().nullable(),
    build: z.unknown(),
  }),
  z.strictObject({
    probe: z.literal("unavailable"),
    detail: nonEmptyString,
  }),
]);

/**
 * The chat completion's OBSERVED result — the run document's
 * `result` at COMPLETED, narrowed at the chat consumer (the generic
 * run mirror keeps `result` a closed record; THIS is the chat work's
 * own closed shape): content + finish_reason + the backend identity
 * + §19.1's REQUESTED/EFFECTIVE pair (requested.temperature is null
 * where the call resolved through the profile's BASE layer).
 */
export const chatCompletionResultSchema = z.strictObject({
  content: z.string(),
  finish_reason: nonEmptyString,
  backend: chatBackendIdentitySchema,
  requested: z.strictObject({
    max_tokens: z.number().int().min(1),
    temperature: finiteFloat.nullable(),
  }),
  effective: z.strictObject({
    max_tokens: z.number().int().min(1),
    temperature: finiteFloat,
  }),
});

/** One frozen input pair — `[key, value]` (the §10 freeze is a
 * stringified pair list on the run document, by the registry's own
 * serialization law). */
const frozenInputSchema = z.tuple([nonEmptyString, z.string()]);

/**
 * One run document — `run.get`'s result, the work-kind-generic
 * envelope. Strict over the envelope's own members (a renamed/typed
 * member is a mismatch); `result` stays a closed record — the WORK
 * narrows it (the chat completion through its own schema above).
 */
export const runDocumentSchema = z.strictObject({
  execution_id: nonEmptyString,
  operation_id: nonEmptyString,
  work: nonEmptyString,
  state: z.enum(EXECUTION_STATES),
  terminal: z.boolean(),
  frozen_inputs: z.array(frozenInputSchema),
  request_digest: nonEmptyString,
  deadline: z.strictObject({
    started_monotonic: finiteFloat,
    deadline_monotonic: finiteFloat,
  }),
  progress: z.record(z.string(), z.unknown()).nullable(),
  result: z.record(z.string(), z.unknown()).nullable(),
  failure_type: z.string().nullable(),
  diagnostics: z.array(z.string()),
  artifact: z.record(z.string(), z.unknown()).nullable(),
});

/** `run.cancel` result — the cancellation REQUEST's observed outcome
 * (the closed §12.3 vocabulary; never itself a completion). */
export const runCancelResultSchema = z.strictObject({
  execution_id: nonEmptyString,
  cancellation: z.enum(CANCELLATION_OUTCOMES),
});

// ------------------------------------------------------------------ models

/** One discovered model — the §20 scan's entry (the state is
 * DISCOVERED at discovery by the registry's own law). `mtime_ns`
 * is a finite NUMBER, not `.int()`: the nanosecond epoch exceeds
 * JS's safe-integer range (zod's own law) — the field is the
 * registry's cheap FINGERPRINT, opaque to the client, never
 * arithmetic. */
export const modelListEntrySchema = z.strictObject({
  logical_name: nonEmptyString,
  location: z.string(),
  size_bytes: nonNegativeInt,
  mtime_ns: finiteFloat,
  content_digest: z.string().nullable(),
  state: z.literal("DISCOVERED"),
});

/** `model.list` result — the discovery scan over the MODELS_ASSETS
 * root (the CORRUPT form raises at the backend, never rides the
 * document — the closed pair is OK | MISSING). */
export const modelListResultSchema = z.strictObject({
  directory_state: z.enum(MODEL_DIRECTORY_STATES),
  models: z.array(modelListEntrySchema),
  models_root: z.string(),
});

/** `model.states` result — the Model-lifecycle read view: the
 * per-model states over the closed MODEL ladder + the ACTIVE slot. */
export const modelStatesResultSchema = z.strictObject({
  states: z.record(z.string(), z.enum(MODEL_STATES)),
  active: z.string().nullable(),
});

// ------------------------------------------- models (the surface's own row)

/**
 * `run.start` result — the ADMISSION identity (the registry's own
 * echo of the admitted work kind + the execution id + the resolved
 * deadline). Strict over the handler's own three-field answer; `work`
 * stays a string (the registry's full kind vocabulary is
 * backend-owned, never re-encoded here).
 */
export const runStartResultSchema = z.strictObject({
  execution_id: nonEmptyString,
  work: nonEmptyString,
  deadline_seconds: finiteFloat,
});

/**
 * `model.load` / `model.unload` result — the two handlers' shared
 * ADMISSION shape, strict: the state is STARTING at admission by the
 * handlers' own law (the ladder's fast walk already happened; the
 * minutes-class port call rides the worker thread — `run.get` is the
 * observation path, never a second blocking call).
 */
export const modelDispatchResultSchema = z.strictObject({
  deadline_seconds: finiteFloat,
  execution_id: nonEmptyString,
  logical_name: nonEmptyString,
  state: z.literal("STARTING"),
  work: z.enum(["model.load", "model.unload"]),
});

/** The fetch run's live PROGRESS document (the consumer-depth narrow
 * over the generic run document's loose `progress` record). */
export const modelFetchProgressSchema = z.strictObject({
  downloaded_bytes: nonNegativeInt,
  logical_name: nonEmptyString,
  total_bytes: nonNegativeInt.nullable(),
});

/** The import run's live PROGRESS document (the per-chunk report). */
export const modelImportProgressSchema = z.strictObject({
  logical_name: nonEmptyString,
  file_index: nonNegativeInt,
  file_count: positiveInt,
  copied_bytes: nonNegativeInt,
  total_bytes: nonNegativeInt,
});

/** The fetch run's OBSERVED result at COMPLETED. */
export const modelFetchResultSchema = z.strictObject({
  location: z.string(),
  logical_name: nonEmptyString,
  size_bytes: nonNegativeInt,
  url: z.string(),
});

/** The import run's OBSERVED result at COMPLETED (the landed files +
 * the count — the count is the list's own length, never a second
 * truth). */
export const modelImportResultSchema = z.strictObject({
  imported: z.array(
    z.strictObject({
      logical_name: nonEmptyString,
      size_bytes: nonNegativeInt,
    }),
  ),
  count: positiveInt,
});

/** The digest run's OBSERVED result at COMPLETED (the §9 strong
 * identity the run computed). */
export const modelDigestResultSchema = z.strictObject({
  chunks: nonNegativeInt,
  content_digest: nonEmptyString,
  logical_name: nonEmptyString,
  size_bytes: nonNegativeInt,
});

/** The load run's OBSERVED result at COMPLETED (`reply` is the
 * backend's own document — backend-owned DATA, loose by law). */
export const modelLoadResultSchema = z.strictObject({
  logical_name: nonEmptyString,
  location: z.string(),
  reply: z.record(z.string(), z.unknown()),
  state: z.literal("ACTIVE"),
});

/** The unload run's OBSERVED result at COMPLETED. */
export const modelUnloadResultSchema = z.strictObject({
  logical_name: nonEmptyString,
  reply: z.record(z.string(), z.unknown()),
  state: z.literal("EVICTED"),
});

// --------------------------------------------------------------- inference

/**
 * `inference.read` result — the Chat-side COMPACT projection's own
 * slice. The members the projection RENDERS are validated closed
 * (profile_name / controls / applies / managed_live / pinned); the
 * document's remaining members (profile, presets, categories, the
 * sampler chain, the compiled preview) ride the wire UNCONSUMED —
 * `looseObject` is the deliberate form, the data-driven law's own
 * shape (§21.2: the UI never re-encodes the control vocabulary; the
 * Inference surface's own row mirrors the depth IT consumes). Each
 * control entry validates its identity/effective value/state/source
 * — the fields the projection reads — and no more.
 */
export const inferenceReadResultSchema = z.looseObject({
  profile_name: nonEmptyString,
  controls: z.array(
    z.looseObject({
      id: nonEmptyString,
      value: z.unknown(),
      state: nonEmptyString,
      source: nonEmptyString,
    }),
  ),
  applies: z.literal("next-spawn"),
  managed_live: z.boolean(),
  pinned: z.array(nonEmptyString),
});

// ------------------------------------------- inference (the workspace row)

/**
 * One control's RESOLVED document — the resolver's own closed field
 * set, strict: a renamed member, a foreign kind/state/value_type, or
 * a non-string reasons entry is a CONTRACT MISMATCH, exactly as the
 * backend's own document law treats it. `value`/`baseline`/
 * `upstream_default` stay `z.unknown()` — the per-control value
 * forms are backend-owned DATA (§21.2's data-driven law: the UI
 * never re-encodes the vocabulary; the editors dispatch over the
 * metadata fields, never over a value enum).
 */
export const inferenceControlSchema = z.strictObject({
  id: nonEmptyString,
  name: nonEmptyString,
  category: nonEmptyString,
  kind: z.enum(INFERENCE_KINDS),
  scope: z.enum(INFERENCE_SCOPES),
  flag: nonEmptyString,
  field: nonEmptyString,
  value: z.unknown(),
  value_doc: nonEmptyString,
  value_type: z.enum(INFERENCE_VALUE_TYPES),
  forms: z.array(nonEmptyString),
  minimum: finiteFloat.nullable(),
  maximum: finiteFloat.nullable(),
  step: finiteFloat,
  advanced: z.boolean(),
  source: nonEmptyString,
  state: z.enum(INFERENCE_STATES),
  reasons: z.array(nonEmptyString),
  baseline: z.unknown(),
  upstream_default: z.unknown(),
  notes: z.array(nonEmptyString),
});

/** One sampler-chain member's resolved document (the ordered
 * first-class object; the value rides unknown — backend data). */
export const inferenceChainMemberSchema = z.strictObject({
  id: nonEmptyString,
  name: nonEmptyString,
  enabled: z.boolean(),
  order: nonNegativeInt,
  value: z.unknown(),
  state: z.enum(INFERENCE_STATES),
  reasons: z.array(nonEmptyString),
});

/** One preset's transparent document (the values record is the
 * backend's own field vocabulary — loose by the data-driven law). */
export const inferencePresetSchema = z.strictObject({
  id: nonEmptyString,
  name: nonEmptyString,
  description: nonEmptyString,
  values: z.record(z.string(), z.unknown()),
});

/** One category's honest count. */
export const inferenceCategorySchema = z.strictObject({
  id: nonEmptyString,
  controls: positiveInt,
});

/**
 * The Inference WORKSPACE's own full document — the depth the
 * surface consumes, validated closed over the resolver's own field
 * set. The wire document carries MORE (`profile`'s raw values
 * vocabulary, `request_layer`) — `looseObject` is the deliberate
 * form (the same law as the Chat-side compact slice, one depth
 * deeper), and the seam's projection DROPS the unconsumed members
 * so no loose index signature ever reaches a surface.
 */
export const inferenceDocumentSchema = z.looseObject({
  profile_name: nonEmptyString,
  categories: z.array(inferenceCategorySchema),
  controls: z.array(inferenceControlSchema),
  sampler_chain: z.array(inferenceChainMemberSchema),
  chain_order: z.array(nonEmptyString),
  deterministic: z.boolean(),
  presets: z.array(inferencePresetSchema),
  pinned: z.array(nonEmptyString),
  managed_live: z.boolean(),
  applies: z.literal("next-spawn"),
  compiled_preview: z.string().nullable(),
  note: nonEmptyString.optional(),
});

/** The validated response plus its dispatch outcome — the client's
 * one honest return shape (the envelope, validated). */
export interface ValidatedResponse {
  readonly ok: boolean;
  readonly status: z.infer<typeof responseDocumentSchema>["status"];
  readonly operationId: string;
  readonly rejection?: z.infer<typeof responseDocumentSchema>["rejection"] | undefined;
  readonly result?: Record<string, unknown> | undefined;
  readonly sessionId?: string | undefined;
  readonly revision?: number | undefined;
  readonly sequence?: number | undefined;
  readonly duplicate: boolean;
}

/** Validate one response document; throws ContractMismatch on any
 * deviation (the caller renders the mismatch honestly — it is
 * never a silent pass-through). */
export function validateResponseDocument(input: unknown): ValidatedResponse {
  const parsed = responseDocumentSchema.parse(input);
  return {
    ok: parsed.status === "OK",
    status: parsed.status,
    operationId: parsed.operation_id,
    rejection: parsed.rejection,
    result: parsed.result,
    sessionId: parsed.session_id,
    revision: parsed.revision,
    sequence: parsed.sequence,
    duplicate: parsed.duplicate === true,
  };
}
