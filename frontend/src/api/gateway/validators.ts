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
  DISPATCH_STATUSES,
  EVENT_TYPES,
  EXPOSURES,
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

/** The transport-level 4xx JSON error (the delivery half's shape). */
export const transportErrorSchema = z.strictObject({
  error: nonEmptyString,
  path: z.string().optional(),
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
