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
  ChatMessage,
  ChatSendResult,
  InferenceDocument,
  InferenceReadResult,
  InferenceUpdateChanges,
  LaunchSettingsDocument,
  ModelDispatchResult,
  ModelListResult,
  ModelRunStartInput,
  ModelStatesResult,
  ObservatoryReadResult,
  ObservatoryRunsResult,
  RequestEnvelope,
  RunCancelResult,
  RunDocument,
  RunStartResult,
  SessionAttachResult,
  SessionCreateResult,
  SessionDocument,
  SessionEventsResult,
} from "./contracts.ts";
import {
  appStatusResultSchema,
  backendSettingsResultSchema,
  inferenceDocumentSchema,
  inferenceReadResultSchema,
  modelDispatchResultSchema,
  modelListResultSchema,
  modelStatesResultSchema,
  observatoryReadResultSchema,
  observatoryRunsResultSchema,
  runCancelResultSchema,
  runDocumentSchema,
  runStartResultSchema,
  chatSendResultSchema,
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

  /**
   * `chat.send` — the chat completion's ADMISSION (MUTATION,
   * session-scoped): the closed argument set is
   * messages/temperature/max_tokens (an absent temperature resolves
   * through the inference profile's BASE layer — the composition's
   * own law, never a client guess); one dispatch with a FRESH
   * idempotency key (G4 — no blind retry); the answer is the
   * execution identity, never the completion itself (`run.get` is
   * the observation path).
   */
  async chatSend(input: {
    readonly sessionId: string;
    readonly clientRequestId: string;
    readonly messages: readonly ChatMessage[];
    readonly temperature?: number;
    readonly maxTokens?: number;
  }): Promise<DispatchResult<ChatSendResult>> {
    const chatArguments: Record<string, unknown> = {
      messages: input.messages.map((message) => ({
        role: message.role,
        content: message.content,
      })),
    };
    if (input.temperature !== undefined) {
      chatArguments["temperature"] = input.temperature;
    }
    if (input.maxTokens !== undefined) {
      chatArguments["max_tokens"] = input.maxTokens;
    }
    const dispatch = await this.postOp({
      operation: "chat.send",
      arguments: chatArguments,
      session_id: input.sessionId,
      client_request_id: input.clientRequestId,
    });
    return narrow(dispatch, chatSendResultSchema, "chat.send");
  }

  /**
   * `run.get` — the execution's live/terminal document (READ,
   * session-scoped, `{execution_id}`): the observation path for a
   * chat completion (and every other run kind — the envelope is
   * work-generic). The state/terminal pair is the registry's own
   * truth; a domain violation (unknown execution / foreign session)
   * is a DELIVERED REJECTED with the observed cause.
   */
  async runGet(input: {
    readonly sessionId: string;
    readonly executionId: string;
  }): Promise<DispatchResult<RunDocument>> {
    const dispatch = await this.postOp({
      operation: "run.get",
      arguments: { execution_id: input.executionId },
      session_id: input.sessionId,
    });
    return narrow(dispatch, runDocumentSchema, "run.get");
  }

  /**
   * `run.cancel` — the truthful cancellation REQUEST (MUTATION,
   * session-scoped): the outcome is the observed answer
   * (CANCEL_REQUESTED / CANCELED / FAILED_TO_CANCEL — a request is
   * never a completion); a fresh idempotency key per explicit
   * attempt (G4).
   */
  async runCancel(input: {
    readonly sessionId: string;
    readonly executionId: string;
    readonly clientRequestId: string;
  }): Promise<DispatchResult<RunCancelResult>> {
    const dispatch = await this.postOp({
      operation: "run.cancel",
      arguments: { execution_id: input.executionId },
      session_id: input.sessionId,
      client_request_id: input.clientRequestId,
    });
    return narrow(dispatch, runCancelResultSchema, "run.cancel");
  }

  /**
   * `model.list` — the §20 discovery scan (READ, session-free, no
   * arguments): the directory classification + the discovered
   * entries + the MODELS_ASSETS folder itself. The scan never
   * validates the bytes — a discovered file proves nothing beyond
   * its cheap fingerprint (§8's model-lifecycle law).
   */
  async modelList(): Promise<DispatchResult<ModelListResult>> {
    const dispatch = await this.postOp({ operation: "model.list" });
    return narrow(dispatch, modelListResultSchema, "model.list");
  }

  /**
   * `model.states` — the Model-lifecycle read view (READ,
   * session-free, no arguments): the per-model states over the
   * closed MODEL ladder + the ACTIVE slot. The Chat header's model
   * line reads THIS document — never a discovery guess (selected ≠
   * loaded ≠ active).
   */
  async modelStates(): Promise<DispatchResult<ModelStatesResult>> {
    const dispatch = await this.postOp({ operation: "model.states" });
    return narrow(dispatch, modelStatesResultSchema, "model.states");
  }

  /**
   * `model.load` — §20's loading half as a RUN (MUTATION,
   * session-scoped): the fast dispatch walks the ladder to SELECTED
   * and answers the execution identity — the minutes-class port call
   * (the managed spawn or the attached load) rides the worker
   * thread; `run.get` is the observation path. One explicit attempt
   * with a FRESH idempotency key (G4 — no blind retry); the ladder's
   * own admission gates (not discovered / already ACTIVE / FAILED
   * terminal / the single slot occupied / already loading) answer
   * DOMAIN_REJECTED with the observed cause — rendered verbatim,
   * never coerced.
   */
  async modelLoad(input: {
    readonly sessionId: string;
    readonly clientRequestId: string;
    readonly logicalName: string;
  }): Promise<DispatchResult<ModelDispatchResult>> {
    const dispatch = await this.postOp({
      operation: "model.load",
      arguments: { logical_name: input.logicalName },
      session_id: input.sessionId,
      client_request_id: input.clientRequestId,
    });
    return narrow(dispatch, modelDispatchResultSchema, "model.load");
  }

  /**
   * `model.unload` — §20's unload half as a RUN (MUTATION,
   * session-scoped): the graceful stop / attached unload rides the
   * worker thread — ACTIVE → EVICTED observed on the run's terminal.
   * The admission gate (not ACTIVE) answers DOMAIN_REJECTED with the
   * observed state — rendered verbatim. A fresh idempotency key per
   * explicit attempt (G4).
   */
  async modelUnload(input: {
    readonly sessionId: string;
    readonly clientRequestId: string;
    readonly logicalName: string;
  }): Promise<DispatchResult<ModelDispatchResult>> {
    const dispatch = await this.postOp({
      operation: "model.unload",
      arguments: { logical_name: input.logicalName },
      session_id: input.sessionId,
      client_request_id: input.clientRequestId,
    });
    return narrow(dispatch, modelDispatchResultSchema, "model.unload");
  }

  /**
   * `run.start` — the model family's work-kind ADMISSION (MUTATION,
   * session-scoped): the per-kind argument sets are CLOSED at this
   * seam (fetch: url + optional logical_name; import: the absolute
   * path list; digest: the logical name) — a foreign key or a wrong
   * type is the work kind's own DOMAIN_REJECTED, rendered verbatim.
   * The answer is the execution identity; `run.get` is the
   * observation path (live progress rides the run document). A fresh
   * idempotency key per explicit attempt (G4).
   */
  async runStart(input: {
    readonly sessionId: string;
    readonly clientRequestId: string;
    readonly start: ModelRunStartInput;
  }): Promise<DispatchResult<RunStartResult>> {
    const argumentsFor: Record<string, unknown> = (() => {
      if (input.start.work === "model.fetch") {
        return input.start.logicalName === undefined
          ? { url: input.start.url }
          : { url: input.start.url, logical_name: input.start.logicalName };
      }
      if (input.start.work === "model.import") {
        return { paths: [...input.start.paths] };
      }
      return { logical_name: input.start.logicalName };
    })();
    const dispatch = await this.postOp({
      operation: "run.start",
      arguments: { work: input.start.work, arguments: argumentsFor },
      session_id: input.sessionId,
      client_request_id: input.clientRequestId,
    });
    return narrow(dispatch, runStartResultSchema, "run.start");
  }

  /**
   * `inference.read` — the resolved inference-control document
   * (READ, session-free, no arguments), consumed here ONLY as the
   * Chat side's COMPACT contextual projection (§21.2: the profile's
   * name, the per-control effective value/state/source, the applies
   * constant, the managed liveness, the pinned ids). The full
   * control depth stays behind the seam — the vocabulary is
   * backend-owned data the UI never re-encodes; the Inference
   * surface's own row mirrors the depth it consumes.
   */
  async inferenceRead(): Promise<DispatchResult<InferenceReadResult>> {
    const dispatch = await this.postOp({ operation: "inference.read" });
    const narrowed = narrow(
      dispatch,
      inferenceReadResultSchema,
      "inference.read",
    );
    if (narrowed.transport === "DELIVERED" && narrowed.status === "OK") {
      return { ...narrowed, result: projectInference(narrowed.result) };
    }
    return narrowed;
  }

  /**
   * `inference.read` — the Inference WORKSPACE's own full document
   * (READ, session-free, no arguments): the control metadata depth
   * the data-driven editors build over (§21.2 — each control's own
   * kind/forms/limits; the UI never re-encodes the vocabulary), the
   * ordered sampler chain, the transparent presets, the categories
   * with honest counts, the pinned ids, and the compiled preview
   * (the technical artifact, read-only). The seam's projection
   * DROPS the unconsumed members (`profile`'s raw values vocabulary,
   * `request_layer`) — no loose index signature reaches a surface.
   */
  async inferenceDocument(): Promise<DispatchResult<InferenceDocument>> {
    const dispatch = await this.postOp({ operation: "inference.read" });
    const narrowed = narrow(
      dispatch,
      inferenceDocumentSchema,
      "inference.read",
    );
    if (narrowed.transport === "DELIVERED" && narrowed.status === "OK") {
      return { ...narrowed, result: projectInferenceDocument(narrowed.result) };
    }
    return narrowed;
  }

  /**
   * `inference.update` — the closed partial UPDATE over the semantic
   * profile (MUTATION, session-scoped): absent fields unchanged (the
   * store's own partial law — ONLY the changed keys ride the wire);
   * `pinned` routes to the WORKSPACE section (its own concern, never
   * a profile value); a fresh `client_request_id` per explicit
   * attempt (G4 — no blind retry); the returned document is the new
   * current (the caller's evidence, never a guess about the file). A
   * domain violation (unknown field / wrong type / a partial chain)
   * is a DELIVERED REJECTED with the observed cause — rendered
   * verbatim, never coerced.
   */
  async inferenceUpdate(input: {
    readonly sessionId: string;
    readonly clientRequestId: string;
    readonly changes: InferenceUpdateChanges;
  }): Promise<DispatchResult<InferenceDocument>> {
    const updateArguments: Record<string, unknown> = {
      ...(input.changes.values as Record<string, unknown> | undefined),
    };
    if (input.changes.name !== undefined) {
      updateArguments["name"] = input.changes.name;
    }
    if (input.changes.sampler_chain !== undefined) {
      updateArguments["sampler_chain"] = input.changes.sampler_chain.map(
        (item) => ({ id: item.id, enabled: item.enabled }),
      );
    }
    if (input.changes.pinned !== undefined) {
      updateArguments["pinned"] = [...input.changes.pinned];
    }
    const dispatch = await this.postOp({
      operation: "inference.update",
      arguments: updateArguments,
      session_id: input.sessionId,
      client_request_id: input.clientRequestId,
    });
    const narrowed = narrow(
      dispatch,
      inferenceDocumentSchema,
      "inference.update",
    );
    if (narrowed.transport === "DELIVERED" && narrowed.status === "OK") {
      return { ...narrowed, result: projectInferenceDocument(narrowed.result) };
    }
    return narrowed;
  }
}

/** The compact projection at the seam: the consumed members pass
 * through, the vocabulary members stay behind (the parsed loose
 * document's index signature never leaks into a surface). */
function projectInference(
  parsed: z.infer<typeof inferenceReadResultSchema>,
): InferenceReadResult {
  return {
    profile_name: parsed.profile_name,
    controls: parsed.controls.map((control) => ({
      id: control.id,
      value: control.value,
      state: control.state,
      source: control.source,
    })),
    applies: parsed.applies,
    managed_live: parsed.managed_live,
    pinned: parsed.pinned,
  };
}

/** The WORKSPACE projection at the seam: the consumed depth passes
 * through closed (every member re-picked by name), the unconsumed
 * members (`profile`'s raw values vocabulary, `request_layer`) stay
 * behind — the surfaces never see the loose index signature the
 * data-driven law keeps at the wire. */
function projectInferenceDocument(
  parsed: z.infer<typeof inferenceDocumentSchema>,
): InferenceDocument {
  return {
    profile_name: parsed.profile_name,
    categories: parsed.categories.map((category) => ({
      id: category.id,
      controls: category.controls,
    })),
    controls: parsed.controls.map((control) => ({
      id: control.id,
      name: control.name,
      category: control.category,
      kind: control.kind,
      scope: control.scope,
      flag: control.flag,
      field: control.field,
      value: control.value,
      value_doc: control.value_doc,
      value_type: control.value_type,
      forms: [...control.forms],
      minimum: control.minimum,
      maximum: control.maximum,
      step: control.step,
      advanced: control.advanced,
      source: control.source,
      state: control.state,
      reasons: [...control.reasons],
      baseline: control.baseline,
      upstream_default: control.upstream_default,
      notes: [...control.notes],
    })),
    sampler_chain: parsed.sampler_chain.map((member) => ({
      id: member.id,
      name: member.name,
      enabled: member.enabled,
      order: member.order,
      value: member.value,
      state: member.state,
      reasons: [...member.reasons],
    })),
    chain_order: [...parsed.chain_order],
    deterministic: parsed.deterministic,
    presets: parsed.presets.map((preset) => ({
      id: preset.id,
      name: preset.name,
      description: preset.description,
      values: preset.values,
    })),
    pinned: [...parsed.pinned],
    managed_live: parsed.managed_live,
    applies: parsed.applies,
    compiled_preview: parsed.compiled_preview,
    note: parsed.note,
  };
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
