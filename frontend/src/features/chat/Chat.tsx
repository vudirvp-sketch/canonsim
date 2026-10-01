/**
 * The Chat surface (Phase 3's fourth row) — the conversation world
 * over the EXISTING gateway ops: `chat.send` (admission) →
 * `run.get` (the bounded observation) → `run.cancel` (the truthful
 * stop), with the header's model line (`model.list` +
 * `model.states`) and the COMPACT inference projection
 * (`inference.read`, §21.2 — the effective temperature the next
 * send resolves from, never a hidden sampler setting; the full
 * control depth lives in the Inference surface, a later row).
 *
 * The four regions (iter-297's named shape): header / viewport /
 * composer / status. The transcript is PRESENTATION state — per-
 * surface and volatile (chat history is not canon; unmount drops
 * it, the same honest boundedness as every surface's local buffer).
 *
 * The near-bottom follow law (§21.1, the Redot-era principle carried
 * to the web): the viewport follows new content ONLY while the
 * reader sits near the bottom (never yanking a reading position),
 * and the scroll read/set happens AFTER a frame — the late-layout
 * settle. The follow is a direct jump (its own static equivalent —
 * compliant with the reduced-motion law by construction).
 *
 * Empty-state grammar (§9): the transcript's EMPTY (no messages
 * yet) stays distinct from every lane below; each read/dispatch
 * lane renders its own honest state; a REJECTED anything renders
 * the gateway's reason VERBATIM. No polling beyond the ONE
 * in-flight run's bounded observer; the context reads are the
 * mount's one pass + the user's explicit refresh.
 */
import { useEffect, useRef } from "react";
import type { ReactNode } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type {
  InferenceReadResult,
  ModelListResult,
  ModelStatesResult,
} from "../../api/gateway/contracts.ts";
import type { ChatExchange } from "./useChat.ts";
import type { ContextLoad } from "./useChat.ts";
import { useChat } from "./useChat.ts";

export interface ChatProps {
  readonly client: GatewayClient;
  /** the run family's ops are session-scoped: null disables the
   * composer's send honestly (the context READs stay available). */
  readonly sessionId: string | null;
  readonly className?: string;
}

/** The near-bottom gate's threshold (px) — the follow law's own
 * constant (§21.1: the reader's position wins over the follow). */
const NEAR_BOTTOM_PX = 80;

export function Chat(props: ChatProps): ReactNode {
  const chat = useChat({ client: props.client, sessionId: props.sessionId });
  const viewportRef = useRef<HTMLDivElement>(null);
  const composerRef = useRef<HTMLTextAreaElement>(null);
  const nearBottomRef = useRef(true);

  // Task-aware focus entry (§15): Chat → composer.
  useEffect(() => {
    composerRef.current?.focus();
  }, []);

  // The near-bottom follow (§21.1): the gate reads the reader's
  // position on every scroll; the follow settles AFTER a frame.
  useEffect(() => {
    const element = viewportRef.current;
    if (element === null || !nearBottomRef.current) return;
    const frame = requestAnimationFrame(() => {
      element.scrollTop = element.scrollHeight;
    });
    return () => cancelAnimationFrame(frame);
  }, [chat.exchanges.length]);

  const onViewportScroll = (): void => {
    const element = viewportRef.current;
    if (element === null) return;
    nearBottomRef.current =
      element.scrollHeight - element.scrollTop - element.clientHeight < NEAR_BOTTOM_PX;
  };

  const sendDisabled =
    props.sessionId === null ||
    chat.busy ||
    chat.draft.trim() === "" ||
    chat.callLocalValue === null ||
    chat.runInFlight;

  return (
    <section className={props.className ?? "surface"} aria-label="Chat — the conversation world">
      <header className="surface-header">
        <h2>Chat</h2>
        <p className="surface-note">
          one conversation with the backend model — every turn an honest run: admitted, observed,
          terminal; the effective temperature the next send resolves from is shown in the strip
        </p>
      </header>

      <ContextStrip
        models={chat.models}
        modelStates={chat.modelStates}
        inference={chat.inference}
      />

      {/* VIEWPORT — the transcript (per-surface presentation state). */}
      <div
        className="chat-viewport"
        data-testid="chat-viewport"
        ref={viewportRef}
        onScroll={onViewportScroll}
        role="log"
        aria-label="the conversation"
        aria-live="polite"
      >
        {chat.exchanges.length === 0 ? (
          <p className="empty" data-testid="chat-empty">
            no messages yet — the transcript lives with this surface (volatile by law: unmount
            drops it, the gateway documents are the truth)
          </p>
        ) : (
          chat.exchanges.map((exchange) => (
            <ChatTurn key={exchange.id} exchange={exchange} onRepoll={chat.repoll} />
          ))
        )}
      </div>

      {/* STATUS — the in-flight run's own line (the per-exchange
          lanes ride the transcript; this is the composer-side truth). */}
      {chat.runInFlight ? (
        <p className="empty" data-testid="chat-run-status">
          a run is in flight — the send stays disabled until it is terminal (one run at a time)
        </p>
      ) : null}
      {chat.callLocalValue === null ? (
        <div className="banner banner-stale" role="note">
          the call-local overrides are not a legal explicit value yet (temperature: a number in
          [0, 2]; max_tokens: an integer in [1, 4096]) — the send stays disabled
        </div>
      ) : null}

      {/* COMPOSER — the REQUEST side (the draft never a state claim). */}
      <form
        className="chat-composer"
        onSubmit={(event) => {
          event.preventDefault();
          void chat.send();
        }}
      >
        <label className="settings-field">
          <span className="settings-label">
            message <em>(Enter sends · Shift+Enter breaks a line)</em>
          </span>
          <textarea
            data-testid="chat-input"
            ref={composerRef}
            rows={3}
            value={chat.draft}
            disabled={props.sessionId === null}
            placeholder={
              props.sessionId === null ? "no session — the run ops are session-scoped" : "…"
            }
            onChange={(event) => chat.editDraft(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                void chat.send();
              }
            }}
          />
        </label>
        <div className="chat-overrides">
          <label className="settings-field">
            <span className="settings-label">
              temperature <em>(empty = the profile&rsquo;s BASE resolution)</em>
            </span>
            <input
              name="temperature"
              type="text"
              inputMode="decimal"
              value={chat.callLocal.temperature}
              disabled={props.sessionId === null}
              onChange={(event) => chat.editCallLocal("temperature", event.target.value)}
            />
          </label>
          <label className="settings-field">
            <span className="settings-label">
              max_tokens <em>(empty = the row&rsquo;s own default)</em>
            </span>
            <input
              name="max_tokens"
              type="text"
              inputMode="numeric"
              value={chat.callLocal.maxTokens}
              disabled={props.sessionId === null}
              onChange={(event) => chat.editCallLocal("maxTokens", event.target.value)}
            />
          </label>
        </div>
        <div className="controls">
          <button type="submit" disabled={sendDisabled}>
            send
          </button>
          {chat.runInFlight ? (
            <button type="button" onClick={() => void chat.stop()} disabled={chat.busy}>
              stop
            </button>
          ) : null}
          <span className="controls-note">
            one explicit dispatch per send (a fresh idempotency key) — never a blind retry; the
            message list rides the wire as the conversation context
          </span>
        </div>
      </form>

      {props.sessionId === null ? (
        <p className="empty">no session — the send is disabled (chat.send is session-scoped)</p>
      ) : null}
    </section>
  );
}

/** The header's context strip: the model line (the load-state truth,
 * never a discovery guess) + the compact inference projection. Each
 * read's lane renders its own honest state. */
function ContextStrip(props: {
  readonly models: ContextLoad<ModelListResult>;
  readonly modelStates: ContextLoad<ModelStatesResult>;
  readonly inference: ContextLoad<InferenceReadResult>;
}): ReactNode {
  const { models, modelStates, inference } = props;
  const active =
    modelStates.kind === "LOADED" ? modelStates.result.active : null;
  const discovered = models.kind === "LOADED" ? models.result.models.length : null;
  const temperature =
    inference.kind === "LOADED"
      ? inference.result.controls.find((control) => control.id === "sampling.temperature")
      : undefined;

  return (
    <>
      <div className="strip" data-testid="chat-context">
        <span>
          model{" "}
          <code>
            {active !== null && active !== undefined ? active : "none ACTIVE"}
          </code>
        </span>
        <span>
          discovered <code>{discovered !== null ? String(discovered) : "—"}</code>
        </span>
        <span>
          profile{" "}
          <code>{inference.kind === "LOADED" ? inference.result.profile_name : "—"}</code>
        </span>
        <span>
          temp{" "}
          <code>
            {temperature !== undefined
              ? `${String(temperature.value)} (${temperature.state} · ${temperature.source})`
              : "—"}
          </code>
        </span>
        <span>
          managed{" "}
          <code>{inference.kind === "LOADED" ? (inference.result.managed_live ? "LIVE" : "down") : "—"}</code>
        </span>
        <span>
          applies <code>{inference.kind === "LOADED" ? inference.result.applies : "—"}</code>
        </span>
      </div>
      <ContextLane title="model.list" load={models.kind} detail={laneDetail(models)} />
      <ContextLane title="model.states" load={modelStates.kind} detail={laneDetail(modelStates)} />
      <ContextLane title="inference.read" load={inference.kind} detail={laneDetail(inference)} />
      {inference.kind === "LOADED" ? (
        <p className="controls-note">
          the compact projection only — the full control depth lives in the Inference surface (a
          later row), never hidden here
        </p>
      ) : null}
    </>
  );
}

/** One context read's failure lane — distinct, never a blank. */
function ContextLane(props: {
  readonly title: string;
  readonly load: ContextLoad<unknown>["kind"];
  readonly detail: string | null;
}): ReactNode {
  if (props.detail === null) return null;
  return (
    <div className="banner banner-error" role="alert">
      {props.title} {props.load} · {props.detail}
    </div>
  );
}

function laneDetail(load: ContextLoad<unknown>): string | null {
  if (load.kind === "TRANSPORT") return `${load.failure} — the re-read is your explicit retry`;
  if (load.kind === "MISMATCH") return `${load.error} — reported, never coerced`;
  if (load.kind === "REJECTED") {
    return `${load.rejection}: ${load.reason ?? "(no reason)"}`;
  }
  return null;
}

/** One transcript turn: the user's REQUESTED echo + the run's lane. */
function ChatTurn(props: {
  readonly exchange: ChatExchange;
  readonly onRepoll: () => void;
}): ReactNode {
  const { exchange } = props;
  return (
    <article className="chat-turn" data-testid={`chat-turn-${exchange.id}`}>
      <div className="chat-bubble chat-bubble-user">
        <span className="chat-role">you</span>
        <p className="chat-content">{exchange.userContent}</p>
      </div>
      <ExchangeLane exchange={exchange} onRepoll={props.onRepoll} />
    </article>
  );
}

/** The run's honest closure lane — every stage rendered as itself. */
function ExchangeLane(props: {
  readonly exchange: ChatExchange;
  readonly onRepoll: () => void;
}): ReactNode {
  const { exchange } = props;
  const lane = exchange.lane;
  if (lane.kind === "DISPATCHING") {
    return (
      <p className="chat-lane" data-testid={`chat-lane-${exchange.id}`}>
        admitting the run…
      </p>
    );
  }
  if (lane.kind === "IN_FLIGHT") {
    return (
      <div className="chat-lane" data-testid={`chat-lane-${exchange.id}`}>
        <p className="empty">
          run {shortId(exchange.executionId)} · {lane.runState}
          {lane.stale ? " · STALE (the observation itself failed)" : "…"}
        </p>
        {exchange.cancelOutcome !== null ? (
          <p className="empty" data-testid={`chat-cancel-${exchange.id}`}>
            stop requested — observed outcome: <code>{exchange.cancelOutcome}</code> (a request&rsquo;s
            answer, never a completion; the run&rsquo;s terminal state is the truth)
          </p>
        ) : null}
        {lane.stale ? (
          <div className="banner banner-stale" role="alert">
            run.get TRANSPORT · {lane.failure} — the outcome is UNKNOWN; the re-poll is your
            explicit action (no blind retry)
            <button type="button" className="chat-repoll" onClick={props.onRepoll}>
              re-poll
            </button>
          </div>
        ) : null}
      </div>
    );
  }
  if (lane.kind === "COMPLETED") {
    const backend = lane.completion.backend;
    const backendLine = "model" in backend ? String(backend.model ?? "(no model id)") : backend.probe;
    return (
      <div className="chat-bubble chat-bubble-assistant">
        <span className="chat-role">assistant</span>
        <p className="chat-content">{lane.completion.content}</p>
        <p className="chat-provenance" data-testid={`chat-provenance-${exchange.id}`}>
          run {shortId(exchange.executionId)} · finish {lane.completion.finish_reason} ·{" "}
          {backendLine} · temp requested{" "}
          {lane.completion.requested.temperature === null
            ? "(absent — the profile's BASE)"
            : String(lane.completion.requested.temperature)}{" "}
          → effective {String(lane.completion.effective.temperature)} · max_tokens{" "}
          {String(lane.completion.effective.max_tokens)}
        </p>
      </div>
    );
  }
  if (lane.kind === "COMPLETED_MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        the run COMPLETED but its result deviates from the chat contract · {lane.error} — reported,
        never coerced
      </div>
    );
  }
  if (lane.kind === "FAILED") {
    return (
      <div className="banner banner-error" role="alert" data-testid={`chat-failed-${exchange.id}`}>
        run FAILED · {lane.failureType ?? "(no failure type)"} —{" "}
        {lane.diagnostics.length > 0 ? lane.diagnostics.join(" | ") : "(no diagnostics)"}
      </div>
    );
  }
  if (lane.kind === "OTHER_TERMINAL") {
    return (
      <div className="banner banner-stale" role="alert" data-testid={`chat-terminal-${exchange.id}`}>
        run terminal · {lane.runState}
        {lane.diagnostics.length > 0 ? ` — ${lane.diagnostics.join(" | ")}` : ""}
      </div>
    );
  }
  if (lane.kind === "SEND_REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        chat.send REJECTED · {lane.rejection}: {lane.reason ?? "(no reason)"} — the message was
        never sent; a new send is your explicit new command (never an auto-retry)
      </div>
    );
  }
  if (lane.kind === "SEND_TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        chat.send TRANSPORT · {lane.failure} — if the request was sent, the outcome is UNKNOWN (no
        blind retry); this turn stays out of the next send&rsquo;s context
      </div>
    );
  }
  if (lane.kind === "POLL_REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        run.get REJECTED · {lane.rejection}: {lane.reason ?? "(no reason)"} — the observation
        itself was rejected; the run&rsquo;s truth is unreachable from here
      </div>
    );
  }
  return (
    <div className="banner banner-error" role="alert">
      run.get CONTRACT MISMATCH · {lane.error} — reported, never coerced
    </div>
  );
}

function shortId(executionId: string | null): string {
  if (executionId === null) return "—";
  return executionId.length <= 12 ? executionId : `${executionId.slice(0, 8)}…`;
}
