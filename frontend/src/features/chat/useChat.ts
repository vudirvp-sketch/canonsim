/**
 * useChat — the Chat surface's state (Phase 3's fourth row), over the
 * EXISTING gateway ops only: `chat.send` (the admission) +
 * `run.get`/`run.cancel` (the run family's observation/cancellation)
 * + `model.list`/`model.states` (the header's model line) +
 * `inference.read` (the compact contextual projection, §21.2). No
 * new route is invented (§3); the transcript below is PRESENTATION
 * state — chat history is not canon (§21's persistence split), the
 * gateway documents are the only truth, and unmounting the surface
 * drops the transcript exactly as the shell's boundedness law drops
 * every surface's local buffer.
 *
 * EFFECTIVE-STATE CLOSURE (FRONTEND_WEB_LAW §8, the stages stay
 * distinct — they may coincide, they are never assumed equivalent):
 *
 * ```text
 * REQUESTED  the composer's draft at send (the messages + the
 *            call-local overrides the caller explicitly set)
 * ACCEPTED   chat.send's admission answer (the execution identity)
 * EFFECTIVE  the run's frozen inputs (§10 — frozen at admission,
 *            observable on the run document; an absent temperature
 *            resolved through the profile's BASE layer)
 * OBSERVED   run.get's terminal document (COMPLETED → the completion
 *            result; FAILED → the failure type + diagnostics;
 *            CANCELED/FAILED_TO_CANCEL/UNKNOWN → the state itself)
 * PRESENTED  the transcript rows + the status lanes below
 * ```
 *
 * The forbidden collapses, named: `textarea.value === EFFECTIVE`
 * (the draft is a REQUEST, never state); `click === success` (the
 * send is one dispatch with four honest outcome lanes); `cancel
 * click === canceled` (§12.3: the cancel answer is a REQUEST's
 * observed outcome, the run's terminal state is the truth — the
 * poll continues past a cancel); `HTTP 200 === semantic success`
 * (a REJECTED document answers 200).
 *
 * G4 (the no-retry law): every explicit send carries a FRESH
 * `client_request_id`; the hook auto-retries NOTHING — not the send,
 * not a poll that hit TRANSPORT (the run lane marks STALE and the
 * loop STOPS; the re-poll is the user's explicit action).
 *
 * Boundedness (§6 rule 3 — passive-on-evidence, never a polling
 * storm): ONE poller for the ONE in-flight run (the send guard
 * blocks a second while one is active), a fixed interval, dead at
 * terminal, dead on unmount, dead on the first TRANSPORT. The
 * context reads fire once on mount; every later read is explicit.
 * The transcript itself is bounded by use — the honest per-surface
 * volatile form, never an ever-growing cross-session buffer.
 */
import { useCallback, useEffect, useRef, useState } from "react";

import type { DispatchResult, GatewayClient } from "../../api/gateway/client.ts";
import type {
  ChatCompletionResult,
  ChatMessage,
  ExecutionState,
  InferenceReadResult,
  ModelListResult,
  ModelStatesResult,
} from "../../api/gateway/contracts.ts";
import { chatCompletionResultSchema } from "../../api/gateway/validators.ts";

/** The run observation's fixed cadence (ms) — a declared constant,
 * never a tunable storm. */
const CHAT_POLL_INTERVAL_MS = 700;

/** One send's honest closure lane — the transcript row's own state
 * matrix (every lane renders distinctly; none collapses). */
export type ChatExchangeLane =
  | { readonly kind: "DISPATCHING" }
  | {
      readonly kind: "IN_FLIGHT";
      readonly runState: ExecutionState;
      readonly stale: boolean;
      readonly failure: string | null;
    }
  | { readonly kind: "COMPLETED"; readonly completion: ChatCompletionResult }
  | { readonly kind: "COMPLETED_MISMATCH"; readonly error: string }
  | {
      readonly kind: "FAILED";
      readonly runState: ExecutionState;
      readonly failureType: string | null;
      readonly diagnostics: readonly string[];
    }
  | {
      readonly kind: "OTHER_TERMINAL";
      readonly runState: ExecutionState;
      readonly diagnostics: readonly string[];
    }
  | { readonly kind: "SEND_REJECTED"; readonly rejection: string; readonly reason: string | null }
  | { readonly kind: "SEND_TRANSPORT"; readonly failure: string }
  | { readonly kind: "SEND_MISMATCH"; readonly error: string }
  | { readonly kind: "POLL_REJECTED"; readonly rejection: string; readonly reason: string | null }
  | { readonly kind: "POLL_MISMATCH"; readonly error: string };

/** One transcript exchange: the user's REQUESTED echo + the run's
 * closure lane (+ the observed cancel answer, verbatim). The row's
 * semantic identity is the EXECUTION id (§21.1's per-message
 * identity) — the local `id` is only React's key. */
export interface ChatExchange {
  readonly id: number;
  readonly userContent: string;
  readonly executionId: string | null;
  readonly cancelOutcome: string | null;
  readonly lane: ChatExchangeLane;
}

/** One context read's honest lane (the header's three READs render
 * their own states — a partial failure is a partial header, never
 * a silent blank). */
export type ContextLoad<T> =
  | { readonly kind: "NOT_LOADED" }
  | { readonly kind: "LOADING" }
  | { readonly kind: "LOADED"; readonly result: T; readonly at: number }
  | { readonly kind: "REJECTED"; readonly rejection: string; readonly reason: string | null; readonly at: number }
  | { readonly kind: "TRANSPORT"; readonly failure: string; readonly at: number }
  | { readonly kind: "MISMATCH"; readonly error: string; readonly at: number };

/** The composer's call-local overrides (§8's composition path: the
 * call-local layer is a legal UI edit — explicitly surfaced here,
 * never a hidden sampler setting). Empty string = ABSENT (the
 * profile's BASE resolution, shown in the compact projection). */
export interface CallLocalDraft {
  readonly temperature: string;
  readonly maxTokens: string;
}

/** The parsed call-local overrides (null = ABSENT, the legal base
 * resolution); the PAIR is null where an explicit value is not legal
 * yet — the send stays disabled, honestly. */
export interface CallLocalValue {
  readonly temperature: number | null;
  readonly maxTokens: number | null;
}

export interface ChatState {
  /** the header's three context reads (models / states / inference). */
  readonly models: ContextLoad<ModelListResult>;
  readonly modelStates: ContextLoad<ModelStatesResult>;
  readonly inference: ContextLoad<InferenceReadResult>;
  readonly refreshContext: () => Promise<void>;
  /** the transcript (presentation state — volatile by law). */
  readonly exchanges: readonly ChatExchange[];
  readonly draft: string;
  readonly callLocal: CallLocalDraft;
  readonly callLocalValue: CallLocalValue | null;
  readonly editDraft: (value: string) => void;
  readonly editCallLocal: (field: keyof CallLocalDraft, value: string) => void;
  readonly send: () => Promise<void>;
  readonly stop: () => Promise<void>;
  readonly repoll: () => void;
  /** a dispatch (send/stop/context read) is in flight. */
  readonly busy: boolean;
  /** a run is admitted and not terminal — the send guard's truth. */
  readonly runInFlight: boolean;
}

export interface ChatOptions {
  readonly client: GatewayClient;
  /** chat.send/run.get/run.cancel are session-scoped: null disables
   * the composer's send honestly (the context READs stay available —
   * they are session-free). */
  readonly sessionId: string | null;
}

export function useChat(options: ChatOptions): ChatState {
  const { client, sessionId } = options;
  const [models, setModels] = useState<ContextLoad<ModelListResult>>({ kind: "NOT_LOADED" });
  const [modelStates, setModelStates] = useState<ContextLoad<ModelStatesResult>>({ kind: "NOT_LOADED" });
  const [inference, setInference] = useState<ContextLoad<InferenceReadResult>>({ kind: "NOT_LOADED" });
  const [exchanges, setExchanges] = useState<readonly ChatExchange[]>([]);
  const [draft, setDraft] = useState("");
  const [callLocal, setCallLocal] = useState<CallLocalDraft>({ temperature: "", maxTokens: "" });
  const [busy, setBusy] = useState(false);
  const [pollEpoch, setPollEpoch] = useState(0);
  // The one-dispatch-at-a-time guards (refs — stable callback
  // identities, the mount reads fire exactly once, no busy-deps loop).
  const contextInFlight = useRef(false);
  const sendInFlight = useRef(false);
  const exchangeSeq = useRef(0);
  const exchangesRef = useRef<readonly ChatExchange[]>([]);
  exchangesRef.current = exchanges;

  // The guards' truth, computed BEFORE the callbacks that read it.
  const callLocalValue = parseCallLocal(callLocal);
  const active = activeExchange(exchanges);
  const runInFlight = active !== null;
  const runInFlightRef = useRef(runInFlight);
  runInFlightRef.current = runInFlight;

  /** PATCH one exchange by its local id — the poll loop's write. */
  const patchExchange = useCallback((id: number, patch: Partial<ChatExchange>): void => {
    setExchanges((previous) =>
      previous.map((exchange) => (exchange.id === id ? { ...exchange, ...patch } : exchange)),
    );
  }, []);

  /** The three context READs — sequential, one at a time; every
   * later read is the user's explicit refresh (no polling: the
   * honest refresh is explicit, the worlds do not change under a
   * mounted reader that fast). */
  const refreshContext = useCallback(async (): Promise<void> => {
    if (contextInFlight.current) return;
    contextInFlight.current = true;
    setBusy(true);
    setModels({ kind: "LOADING" });
    setModelStates({ kind: "LOADING" });
    setInference({ kind: "LOADING" });
    try {
      await applyLane(await client.modelList(), setModels);
      await applyLane(await client.modelStates(), setModelStates);
      await applyLane(await client.inferenceRead(), setInference);
    } finally {
      contextInFlight.current = false;
      setBusy(false);
    }
  }, [client]);

  // The mount reads — exactly one pass (the Settings precedent).
  useEffect(() => {
    void refreshContext();
  }, []);

  /** The transcript's message context for the next send: the user
   * turns of ADMITTED exchanges + the assistant contents of
   * COMPLETED ones. A REJECTED/TRANSPORT/UNKNOWN exchange may never
   * have happened server-side — its turn stays OUT of the context
   * (the honest provenance rule, never a guessed history). */
  const messagesForSend = useCallback(
    (currentUserContent: string): readonly ChatMessage[] => {
      const messages: ChatMessage[] = [];
      for (const exchange of exchangesRef.current) {
        const admitted = exchange.executionId !== null;
        if (admitted) {
          messages.push({ role: "user", content: exchange.userContent });
        }
        if (exchange.lane.kind === "COMPLETED") {
          messages.push({ role: "assistant", content: exchange.lane.completion.content });
        }
      }
      messages.push({ role: "user", content: currentUserContent });
      return messages;
    },
    [],
  );

  /** The send — ONE explicit attempt, a fresh idempotency key (G4),
   * the call-local overrides only where the caller set them. The
   * answer is the ADMISSION; the observation is the poll loop. */
  const send = useCallback(async (): Promise<void> => {
    if (sendInFlight.current || sessionId === null) return;
    const content = draft.trim();
    if (content === "" || callLocalValue === null) return;
    if (runInFlightRef.current) return; // ONE run at a time (boundedness)
    sendInFlight.current = true;
    setBusy(true);
    const id = exchangeSeq.current + 1;
    exchangeSeq.current = id;
    const requestMessages = messagesForSend(content);
    setExchanges((previous) => [
      ...previous,
      { id, userContent: content, executionId: null, cancelOutcome: null, lane: { kind: "DISPATCHING" } },
    ]);
    setDraft("");
    try {
      const chatArguments: {
        sessionId: string;
        clientRequestId: string;
        messages: readonly ChatMessage[];
        temperature?: number;
        maxTokens?: number;
      } = {
        sessionId,
        clientRequestId: `chat-send-${crypto.randomUUID()}`,
        messages: requestMessages,
      };
      if (callLocalValue.temperature !== null) {
        chatArguments.temperature = callLocalValue.temperature;
      }
      if (callLocalValue.maxTokens !== null) {
        chatArguments.maxTokens = callLocalValue.maxTokens;
      }
      const dispatch = await client.chatSend(chatArguments);
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        patchExchange(id, {
          executionId: dispatch.result.execution_id,
          lane: { kind: "IN_FLIGHT", runState: dispatch.result.state, stale: false, failure: null },
        });
      } else if (dispatch.transport === "TRANSPORT") {
        patchExchange(id, {
          lane: {
            kind: "SEND_TRANSPORT",
            failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
          },
        });
      } else if (dispatch.transport === "MISMATCH") {
        patchExchange(id, { lane: { kind: "SEND_MISMATCH", error: dispatch.error } });
      } else {
        patchExchange(id, {
          lane: {
            kind: "SEND_REJECTED",
            rejection: dispatch.response.rejection ?? "REJECTED",
            reason: reasonOf(dispatch.response.result),
          },
        });
      }
    } finally {
      sendInFlight.current = false;
      setBusy(false);
    }
  }, [sessionId, draft, callLocalValue, client, messagesForSend, patchExchange]);

  /** The stop — the truthful cancellation REQUEST (§12.3): a fresh
   * key per explicit attempt; the observed outcome renders verbatim
   * on the exchange; the poll CONTINUES (the run's terminal state,
   * not the cancel answer, is the truth). */
  const stop = useCallback(async (): Promise<void> => {
    if (sessionId === null || sendInFlight.current) return;
    const currentActive = activeExchange(exchangesRef.current);
    if (currentActive === null || currentActive.executionId === null) return;
    sendInFlight.current = true;
    setBusy(true);
    try {
      const dispatch = await client.runCancel({
        sessionId,
        executionId: currentActive.executionId,
        clientRequestId: `chat-cancel-${crypto.randomUUID()}`,
      });
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        patchExchange(currentActive.id, { cancelOutcome: dispatch.result.cancellation });
      } else if (dispatch.transport === "TRANSPORT") {
        patchExchange(currentActive.id, {
          cancelOutcome: `TRANSPORT (${dispatch.failure.kind}) — the request's outcome is UNKNOWN`,
        });
      } else if (dispatch.transport === "MISMATCH") {
        patchExchange(currentActive.id, { cancelOutcome: `CONTRACT MISMATCH: ${dispatch.error}` });
      } else {
        patchExchange(currentActive.id, {
          cancelOutcome: `${dispatch.response.rejection ?? "REJECTED"}: ${
            reasonOf(dispatch.response.result) ?? "(no reason)"
          }`,
        });
      }
    } finally {
      sendInFlight.current = false;
      setBusy(false);
    }
  }, [sessionId, client, patchExchange]);

  /** The explicit re-poll after a STALE lane — the user's action
   * (G4), never an automatic recovery. */
  const repoll = useCallback((): void => {
    setPollEpoch((epoch) => epoch + 1);
  }, []);

  // The bounded run observation: fires for the ACTIVE admitted run,
  // stops at terminal / TRANSPORT / REJECTED / MISMATCH / unmount.
  // The key is the (execution id, exchange id) pair — stable across
  // the lane's own patches, so the loop never restarts mid-run. A
  // DISPATCHING exchange has NO execution id yet — its observation
  // begins only at admission (the send's own dispatch is the guard).
  const activeKey =
    active !== null && active.executionId !== null
      ? `${active.executionId}:${active.id}`
      : null;
  useEffect(() => {
    if (activeKey === null || sessionId === null) return;
    const executionId = activeKey.slice(0, activeKey.lastIndexOf(":"));
    const exchangeId = Number(activeKey.slice(activeKey.lastIndexOf(":") + 1));
    let stopped = false;
    let timer: ReturnType<typeof setTimeout> | null = null;
    const step = async (): Promise<void> => {
      if (stopped) return;
      const dispatch = await client.runGet({ sessionId, executionId });
      if (stopped) return;
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        const run = dispatch.result;
        if (run.terminal) {
          patchExchange(exchangeId, { lane: terminalLane(run) });
          return; // the loop's honest end
        }
        patchExchange(exchangeId, {
          lane: { kind: "IN_FLIGHT", runState: run.state, stale: false, failure: null },
        });
        timer = setTimeout(() => void step(), CHAT_POLL_INTERVAL_MS);
        return;
      }
      if (dispatch.transport === "TRANSPORT") {
        // G4: the loop STOPS — the re-poll is the user's explicit action.
        patchExchange(exchangeId, {
          lane: {
            kind: "IN_FLIGHT",
            runState: "RUNNING",
            stale: true,
            failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
          },
        });
        return;
      }
      if (dispatch.transport === "MISMATCH") {
        patchExchange(exchangeId, { lane: { kind: "POLL_MISMATCH", error: dispatch.error } });
        return;
      }
      patchExchange(exchangeId, {
        lane: {
          kind: "POLL_REJECTED",
          rejection: dispatch.response.rejection ?? "REJECTED",
          reason: reasonOf(dispatch.response.result),
        },
      });
    };
    void step();
    return () => {
      stopped = true;
      if (timer !== null) clearTimeout(timer);
    };
  }, [activeKey, pollEpoch, sessionId, client, patchExchange]);

  const editDraft = useCallback((value: string): void => {
    setDraft(value);
  }, []);

  const editCallLocal = useCallback((field: keyof CallLocalDraft, value: string): void => {
    setCallLocal((previous) => ({ ...previous, [field]: value }));
  }, []);

  return {
    models,
    modelStates,
    inference,
    refreshContext,
    exchanges,
    draft,
    callLocal,
    callLocalValue,
    editDraft,
    editCallLocal,
    send,
    stop,
    repoll,
    busy,
    runInFlight,
  };
}

/** The last admitted, non-terminal exchange — at most one exists by
 * the send guard (boundedness: ONE poller, ONE in-flight run). */
function activeExchange(exchanges: readonly ChatExchange[]): ChatExchange | null {
  for (let index = exchanges.length - 1; index >= 0; index -= 1) {
    const exchange = exchanges[index]!;
    if (exchange.lane.kind === "DISPATCHING" || exchange.lane.kind === "IN_FLIGHT") {
      return exchange;
    }
  }
  return null;
}

/** One context read's four-lane application — the shared honest form
 * (every READ state carries its own lane; none collapses). */
async function applyLane<T>(
  dispatch: DispatchResult<T>,
  set: (lane: ContextLoad<T>) => void,
): Promise<void> {
  if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
    set({ kind: "LOADED", result: dispatch.result, at: Date.now() });
  } else if (dispatch.transport === "TRANSPORT") {
    set({
      kind: "TRANSPORT",
      failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
      at: Date.now(),
    });
  } else if (dispatch.transport === "MISMATCH") {
    set({ kind: "MISMATCH", error: dispatch.error, at: Date.now() });
  } else {
    set({
      kind: "REJECTED",
      rejection: dispatch.response.rejection ?? "REJECTED",
      reason: reasonOf(dispatch.response.result),
      at: Date.now(),
    });
  }
}

/** The terminal lane from the run document — the observed truth,
 * narrowed per work kind at the consumer (the chat completion's own
 * closed shape; a completion whose result deviates is the honest
 * COMPLETED_MISMATCH lane, never a coerced bubble). */
function terminalLane(run: {
  state: ExecutionState;
  result: Readonly<Record<string, unknown>> | null;
  failure_type: string | null;
  diagnostics: readonly string[];
}): ChatExchangeLane {
  if (run.state === "COMPLETED" && run.result !== null) {
    const parsed = chatCompletionResultSchema.safeParse(run.result);
    if (parsed.success) {
      return { kind: "COMPLETED", completion: parsed.data };
    }
    return {
      kind: "COMPLETED_MISMATCH",
      error: parsed.error.issues
        .map((issue) => `${issue.path.join(".")}: ${issue.message}`)
        .join("; "),
    };
  }
  if (run.state === "FAILED") {
    return {
      kind: "FAILED",
      runState: run.state,
      failureType: run.failure_type,
      diagnostics: run.diagnostics,
    };
  }
  return {
    kind: "OTHER_TERMINAL",
    runState: run.state,
    diagnostics: run.diagnostics,
  };
}

/** The call-local draft's parse: the PAIR is null where an explicit
 * value is not legal yet (absent values pass as null = ABSENT, a
 * legal state — the profile's BASE resolution). */
function parseCallLocal(draft: CallLocalDraft): CallLocalValue | null {
  const temperatureText = draft.temperature.trim();
  let temperature: number | null = null;
  if (temperatureText !== "") {
    const value = Number(temperatureText);
    if (!Number.isFinite(value) || value < 0 || value > 2) return null;
    temperature = value;
  }
  const maxTokensText = draft.maxTokens.trim();
  let maxTokens: number | null = null;
  if (maxTokensText !== "") {
    if (!/^\d+$/.test(maxTokensText)) return null;
    const value = Number(maxTokensText);
    if (value < 1 || value > 4096) return null;
    maxTokens = value;
  }
  return { temperature, maxTokens };
}

/** The gateway's reason, honestly typed (unknown on the wire). */
function reasonOf(result: Record<string, unknown> | undefined): string | null {
  const value = result?.["reason"];
  return typeof value === "string" ? value : null;
}
