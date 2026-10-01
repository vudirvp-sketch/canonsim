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
