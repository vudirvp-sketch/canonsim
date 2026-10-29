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
import { formatNumber, tr } from "../../i18n/index.ts";
import type { ChatExchange, ProvenanceLoad, ReplayLane, CancelOutcome } from "./useChat.ts";
import type { ContextLoad } from "./useChat.ts";
import { isTerminalLane, useChat } from "./useChat.ts";

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
    <section className={props.className ?? "surface"} aria-label={tr("chat.region")}>
      <header className="surface-header">
        <h2>{tr("chat.title")}</h2>
        <p className="surface-note">{tr("chat.note")}</p>
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
        aria-label={tr("chat.viewportLabel")}
        aria-live="polite"
      >
        {chat.exchanges.length === 0 ? (
          <p className="empty" data-testid="chat-empty">
            {tr("chat.empty")}
          </p>
        ) : (
          chat.exchanges.map((exchange) => (
            <ChatTurn
              key={exchange.id}
              exchange={exchange}
              sessionId={props.sessionId}
              busy={chat.busy}
              runInFlight={chat.runInFlight}
              onRepoll={chat.repoll}
              onReplay={() => void chat.replayFrom(exchange.id)}
              onToggleProvenance={() => chat.toggleProvenance(exchange.id)}
              onRefreshProvenance={() => void chat.refreshProvenance(exchange.id)}
            />
          ))
        )}
      </div>

      {/* STATUS — the in-flight run's own line (the per-exchange
          lanes ride the transcript; this is the composer-side truth). */}
      {chat.runInFlight ? (
        <p className="empty" data-testid="chat-run-status">
          {tr("chat.runInFlight")}
        </p>
      ) : null}
      {chat.callLocalValue === null ? (
        <div className="banner banner-stale" role="note">
          {tr("chat.callLocalInvalid")}
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
            {tr("chat.composer.message")} <em>{tr("chat.composer.messageHint")}</em>
          </span>
          <textarea
            data-testid="chat-input"
            ref={composerRef}
            rows={3}
            value={chat.draft}
            disabled={props.sessionId === null}
            placeholder={
              props.sessionId === null
                ? tr("chat.composer.noSessionPlaceholder")
                : tr("chat.composer.ellipsis")
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
              {tr("chat.composer.temperature")}{" "}
              <em>{tr("chat.composer.temperatureHint")}</em>
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
              {tr("chat.composer.maxTokens")} <em>{tr("chat.composer.maxTokensHint")}</em>
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
            {tr("chat.composer.send")}
          </button>
          {chat.runInFlight ? (
            <button type="button" onClick={() => void chat.stop()} disabled={chat.busy}>
              {tr("chat.composer.stop")}
            </button>
          ) : null}
          <span className="controls-note">{tr("chat.composer.sendNote")}</span>
        </div>
      </form>

      {props.sessionId === null ? (
        <p className="empty">{tr("chat.noSession")}</p>
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
          {tr("chat.context.model")}{" "}
          <code>
            {active !== null && active !== undefined ? active : tr("chat.context.noneActive")}
          </code>
        </span>
        <span>
          {tr("chat.context.discovered")}{" "}
          <code>{discovered !== null ? formatNumber(discovered) : "—"}</code>
        </span>
        <span>
          {tr("chat.context.profile")}{" "}
          <code>{inference.kind === "LOADED" ? inference.result.profile_name : "—"}</code>
        </span>
        <span>
          {tr("chat.context.temp")}{" "}
          <code>
            {temperature !== undefined
              ? tr("chat.context.tempValue", {
                  value: String(temperature.value),
                  state: temperature.state,
                  source: temperature.source,
                })
              : "—"}
          </code>
        </span>
        <span>
          {tr("chat.context.managed")}{" "}
          <code>
            {inference.kind === "LOADED"
              ? inference.result.managed_live
                ? tr("chat.context.live")
                : tr("chat.context.down")
              : "—"}
          </code>
        </span>
        <span>
          {tr("chat.context.applies")}{" "}
          <code>{inference.kind === "LOADED" ? inference.result.applies : "—"}</code>
        </span>
      </div>
      <ContextLane title="model.list" load={models.kind} detail={laneDetail(models)} />
      <ContextLane title="model.states" load={modelStates.kind} detail={laneDetail(modelStates)} />
      <ContextLane title="inference.read" load={inference.kind} detail={laneDetail(inference)} />
      {inference.kind === "LOADED" ? (
        <p className="controls-note">{tr("chat.context.compactNote")}</p>
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
      {tr("chat.context.laneJoin", {
        title: props.title,
        load: props.load,
        detail: props.detail,
      })}
    </div>
  );
}

function laneDetail(load: ContextLoad<unknown>): string | null {
  if (load.kind === "TRANSPORT")
    return tr("chat.context.laneRetry", { failure: load.failure });
  if (load.kind === "MISMATCH") return tr("chat.context.laneMismatch", { error: load.error });
  if (load.kind === "REJECTED") {
    return tr("chat.context.laneRejected", {
      rejection: load.rejection,
      reason: load.reason ?? tr("chat.lane.noReason"),
    });
  }
  return null;
}

/** One transcript turn: the user's REQUESTED echo + the run's lane
 * (+ the terminal affordances: the replay admission and the lineage
 * inspector; a replay echo names its original and stays out of the
 * next send's context). */
function ChatTurn(props: {
  readonly exchange: ChatExchange;
  readonly sessionId: string | null;
  readonly busy: boolean;
  readonly runInFlight: boolean;
  readonly onRepoll: () => void;
  readonly onReplay: () => void;
  readonly onToggleProvenance: () => void;
  readonly onRefreshProvenance: () => void;
}): ReactNode {
  const { exchange } = props;
  return (
    <article className="chat-turn" data-testid={`chat-turn-${exchange.id}`}>
      {exchange.replayOf !== null ? (
        <p className="chat-replay-note" data-testid={`chat-replay-note-${exchange.id}`}>
          {tr("chat.turn.replayOfLabel")} <code>{shortId(exchange.replayOf)}</code>
          {tr("chat.turn.replayEchoTail")}
        </p>
      ) : null}
      <div className="chat-bubble chat-bubble-user">
        <span className="chat-role">
          {exchange.replayOf !== null ? tr("chat.turn.roleReplay") : tr("chat.turn.roleYou")}
        </span>
        <p className="chat-content">{exchange.userContent}</p>
      </div>
      <ExchangeLane exchange={exchange} onRepoll={props.onRepoll} />
      {isTerminalLane(exchange.lane) ? (
        <>
          <TerminalActions
            exchange={exchange}
            sessionId={props.sessionId}
            busy={props.busy}
            runInFlight={props.runInFlight}
            onReplay={props.onReplay}
            onToggleProvenance={props.onToggleProvenance}
          />
          {exchange.provenance.kind !== "CLOSED" ? (
            <ProvenancePanel exchange={exchange} onRefresh={props.onRefreshProvenance} />
          ) : null}
        </>
      ) : null}
    </article>
  );
}

/** The terminal turn's affordances — a replay REQUEST's own lane
 * (kept distinct from the replayed run's observation lane) and the
 * lineage inspector's toggle (§21.1: per-message inspect metadata;
 * the replay is the honest regenerate form: a NEW execution over the
 * frozen material, never identity reuse). */
function TerminalActions(props: {
  readonly exchange: ChatExchange;
  readonly sessionId: string | null;
  readonly busy: boolean;
  readonly runInFlight: boolean;
  readonly onReplay: () => void;
  readonly onToggleProvenance: () => void;
}): ReactNode {
  const { exchange } = props;
  const replaying = exchange.replay.kind === "DISPATCHING";
  const replayDisabled =
    props.sessionId === null || props.busy || props.runInFlight || replaying;
  const open = exchange.provenance.kind !== "CLOSED";
  return (
    <>
      <div className="chat-actions" data-testid={`chat-actions-${exchange.id}`}>
        <button
          type="button"
          disabled={replayDisabled}
          title={tr("chat.actions.replayTitle")}
          onClick={props.onReplay}
        >
          {tr("chat.actions.replay")}
        </button>
        <button
          type="button"
          aria-expanded={open}
          aria-controls={`chat-provenance-panel-${exchange.id}`}
          title={tr("chat.actions.lineageTitle")}
          onClick={props.onToggleProvenance}
        >
          {open ? tr("chat.actions.hideLineage") : tr("chat.actions.inspectLineage")}
        </button>
        <span className="controls-note">{tr("chat.actions.note")}</span>
      </div>
      <ReplayLaneBanner exchange={exchange} />
    </>
  );
}

/** The replay dispatch's honest closure, verbatim per lane. */
function ReplayLaneBanner(props: { readonly exchange: ChatExchange }): ReactNode {
  const lane: ReplayLane = props.exchange.replay;
  if (lane.kind === "NOT_ATTEMPTED") return null;
  if (lane.kind === "DISPATCHING") {
    return (
      <p className="empty" data-testid={`chat-replay-dispatching-${props.exchange.id}`}>
        {tr("chat.replay.dispatching")}
      </p>
    );
  }
  if (lane.kind === "ADMITTED") {
    return (
      <p className="empty" data-testid={`chat-replay-admitted-${props.exchange.id}`}>
        {tr("chat.replay.admittedA")} <code>{shortId(lane.executionId)}</code>{" "}
        {tr("chat.replay.admittedB")}
      </p>
    );
  }
  if (lane.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("chat.replay.rejected", {
          rejection: lane.rejection,
          reason: lane.reason ?? tr("chat.lane.noReason"),
        })}
      </div>
    );
  }
  if (lane.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("chat.replay.transport", { failure: lane.failure })}
      </div>
    );
  }
  return (
    <div className="banner banner-error" role="alert">
      {tr("chat.replay.mismatch", { error: lane.error })}
    </div>
  );
}

/** The lineage inspector — `execution.get`'s observed document,
 * rendered as itself: the link, the children, the digest, the closed
 * artifact, and the frozen pairs the replay re-runs. */
function ProvenancePanel(props: {
  readonly exchange: ChatExchange;
  readonly onRefresh: () => void;
}): ReactNode {
  const { exchange } = props;
  return (
    <section
      className="provenance-panel"
      id={`chat-provenance-panel-${exchange.id}`}
      aria-label={tr("chat.lineage.region", { id: shortId(exchange.executionId) })}
      data-testid={`chat-provenance-panel-${exchange.id}`}
    >
      <h4>
        {tr("chat.lineage.titleA")} <code>{shortId(exchange.executionId)}</code>
      </h4>
      <ProvenanceDocument provenance={exchange.provenance} />
      <div className="controls">
        <button
          type="button"
          onClick={props.onRefresh}
          disabled={exchange.provenance.kind === "LOADING"}
        >
          {tr("chat.lineage.refresh")}
        </button>
        <span className="controls-note">{tr("chat.lineage.refreshNote")}</span>
      </div>
    </section>
  );
}

/** Every provenance READ state its own lane — never a blank panel. */
function ProvenanceDocument(props: { readonly provenance: ProvenanceLoad }): ReactNode {
  const provenance = props.provenance;
  if (provenance.kind === "CLOSED") return null;
  if (provenance.kind === "LOADING") {
    return <p className="empty">{tr("chat.lineage.reading")}</p>;
  }
  if (provenance.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("chat.lineage.transport", { failure: provenance.failure })}
      </div>
    );
  }
  if (provenance.kind === "MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("chat.lineage.mismatch", { error: provenance.error })}
      </div>
    );
  }
  if (provenance.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("chat.lineage.rejected", {
          rejection: provenance.rejection,
          reason: provenance.reason ?? tr("chat.lane.noReason"),
        })}
      </div>
    );
  }
  const document = provenance.document;
  const artifact = document.artifact;
  const artifactStatus =
    artifact !== null && typeof artifact["status"] === "string" ? artifact["status"] : null;
  const artifactSchema =
    artifact !== null && typeof artifact["artifact_schema_identity"] === "string"
      ? artifact["artifact_schema_identity"]
      : null;
  return (
    <>
      <dl className="status-grid" data-testid="chat-provenance-doc">
        <dt>{tr("chat.lineage.work")}</dt>
        <dd>
          <code>{document.work}</code>{" "}
          {document.terminal ? tr("chat.lineage.workTerminal") : tr("chat.lineage.workInFlight")}
        </dd>
        <dt>{tr("chat.lineage.state")}</dt>
        <dd>
          <code>{document.state}</code>
        </dd>
        <dt>{tr("chat.lineage.operation")}</dt>
        <dd>
          <code>{document.operation_id}</code>
        </dd>
        <dt>{tr("chat.lineage.lineage")}</dt>
        <dd>
          {tr("chat.lineage.replayOf")}{" "}
          <code>
            {document.replay_of !== null ? shortId(document.replay_of) : tr("chat.lineage.original")}
          </code>{" "}
          {tr("chat.lineage.replays")} <code>{String(document.replays.length)}</code>
          {document.replays.length > 0 ? (
            <>
              {" "}
              {tr("chat.lineage.children")} <code>{document.replays.map(shortId).join(", ")}</code>
            </>
          ) : null}
        </dd>
        <dt>{tr("chat.lineage.requestDigest")}</dt>
        <dd>
          <code>{document.request_digest}</code>
        </dd>
        <dt>{tr("chat.lineage.artifact")}</dt>
        <dd>
          {artifact === null ? (
            tr("chat.lineage.notClosed")
          ) : (
            <>
              <code>{artifactStatus ?? tr("chat.lineage.noStatus")}</code>
              {artifactSchema !== null ? (
                <>
                  {" "}
                  {tr("chat.lineage.artifactSchemaJoin")} <code>{artifactSchema}</code>
                </>
              ) : null}
            </>
          )}
        </dd>
      </dl>
      <h4>{tr("chat.lineage.frozenTitle")}</h4>
      {document.frozen_inputs.length === 0 ? (
        <p className="empty">{tr("chat.lineage.noPairs")}</p>
      ) : (
        <table className="frozen-table">
          <thead>
            <tr>
              <th scope="col">{tr("chat.lineage.key")}</th>
              <th scope="col">{tr("chat.lineage.frozenValue")}</th>
            </tr>
          </thead>
          <tbody>
            {document.frozen_inputs.map(([key, value]) => (
              <tr key={key}>
                <th scope="row">{key}</th>
                <td>{value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}

/** The stop's observed answer — the structural code (useChat's
 * CancelOutcome) rendered as its verbatim prose lane; the
 * cancellation token itself stays verbatim in a <code>. */
function cancelOutcomeText(outcome: CancelOutcome): string {
  if (outcome.kind === "OBSERVED") return outcome.cancellation;
  if (outcome.kind === "TRANSPORT")
    return tr("chat.lane.cancelTransport", { kind: outcome.failureKind });
  if (outcome.kind === "MISMATCH") return tr("chat.lane.cancelMismatch", { error: outcome.error });
  return tr("chat.lane.cancelRejected", {
    rejection: outcome.rejection,
    reason: outcome.reason ?? tr("chat.lane.noReason"),
  });
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
        {tr("chat.lane.dispatching")}
      </p>
    );
  }
  if (lane.kind === "IN_FLIGHT") {
    return (
      <div className="chat-lane" data-testid={`chat-lane-${exchange.id}`}>
        <p className="empty">
          {tr("chat.lane.inFlightRun", {
            id: shortId(exchange.executionId),
            state: lane.runState,
          })}
          {lane.stale ? tr("chat.lane.staleMarker") : tr("chat.lane.inFlightEllipsis")}
        </p>
        {exchange.cancelOutcome !== null ? (
          <p className="empty" data-testid={`chat-cancel-${exchange.id}`}>
            {tr("chat.lane.cancelOutcomeLabel")}{" "}
            <code>{cancelOutcomeText(exchange.cancelOutcome)}</code>{" "}
            {tr("chat.lane.cancelTail")}
          </p>
        ) : null}
        {lane.stale ? (
          <div className="banner banner-stale" role="alert">
            {tr("chat.lane.repollNote", { failure: lane.failure ?? "" })}
            <button type="button" className="chat-repoll" onClick={props.onRepoll}>
              {tr("chat.lane.repoll")}
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
        <span className="chat-role">{tr("chat.turn.roleAssistant")}</span>
        <p className="chat-content">{lane.completion.content}</p>
        <p className="chat-provenance" data-testid={`chat-provenance-${exchange.id}`}>
          {tr("chat.lane.runShort", { id: shortId(exchange.executionId) })}
          {exchange.replayOf !== null ? (
            <>
              {" "}
              {tr("chat.lane.replayOfShort")} <code>{shortId(exchange.replayOf)}</code>
            </>
          ) : null}{" "}
          {tr("chat.lane.finish", { reason: lane.completion.finish_reason })}{" "}
          {backendLine}{" "}
          {tr("chat.lane.tempRequested")}{" "}
          {lane.completion.requested.temperature === null
            ? tr("chat.lane.tempAbsent")
            : String(lane.completion.requested.temperature)}{" "}
          {tr("chat.lane.effective", { value: String(lane.completion.effective.temperature) })}{" "}
          {tr("chat.lane.maxTokensTail", {
            value: String(lane.completion.effective.max_tokens),
          })}
        </p>
      </div>
    );
  }
  if (lane.kind === "COMPLETED_MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("chat.lane.completedMismatch", { error: lane.error })}
      </div>
    );
  }
  if (lane.kind === "FAILED") {
    return (
      <div className="banner banner-error" role="alert" data-testid={`chat-failed-${exchange.id}`}>
        {tr("chat.lane.failed", {
          failureType: lane.failureType ?? tr("chat.lane.noFailureType"),
          diagnostics:
            lane.diagnostics.length > 0
              ? lane.diagnostics.join(" | ")
              : tr("chat.lane.noDiagnostics"),
        })}
      </div>
    );
  }
  if (lane.kind === "OTHER_TERMINAL") {
    return (
      <div className="banner banner-stale" role="alert" data-testid={`chat-terminal-${exchange.id}`}>
        {tr("chat.lane.terminal", { state: lane.runState })}
        {lane.diagnostics.length > 0 ? ` — ${lane.diagnostics.join(" | ")}` : ""}
      </div>
    );
  }
  if (lane.kind === "SEND_REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("chat.lane.sendRejected", {
          rejection: lane.rejection,
          reason: lane.reason ?? tr("chat.lane.noReason"),
        })}
      </div>
    );
  }
  if (lane.kind === "SEND_TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("chat.lane.sendTransport", { failure: lane.failure })}
      </div>
    );
  }
  if (lane.kind === "POLL_REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("chat.lane.pollRejected", {
          rejection: lane.rejection,
          reason: lane.reason ?? tr("chat.lane.noReason"),
        })}
      </div>
    );
  }
  return (
    <div className="banner banner-error" role="alert">
      {tr("chat.lane.pollMismatch", { error: lane.error })}
    </div>
  );
}

function shortId(executionId: string | null): string {
  if (executionId === null) return "—";
  return executionId.length <= 12 ? executionId : `${executionId.slice(0, 8)}…`;
}
