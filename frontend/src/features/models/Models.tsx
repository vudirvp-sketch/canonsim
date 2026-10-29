/**
 * The Models surface (Phase 3's sixth row) — the model family's
 * mirror: the §20 discovery list (the ladder law rendered: file
 * exists ≠ valid ≠ selected ≠ loading ≠ loaded ≠ active), the
 * arrival pane (fetch from anywhere / import local files — both as
 * RUNS with live progress), the load/unload dispatches (the §20
 * loading half as RUNS — the admission walks the ladder fast, the
 * minutes-class port call rides the worker thread), and the §9
 * strong-identity affordance (the digest RUN — the honest long arm
 * for a multi-GB file, cancellable and observable; the synchronous
 * model.inspect READ stays a backend surface, never a frozen UI).
 *
 * §20's law is the surface's spine: the discovery entry proves
 * nothing beyond its cheap fingerprint; the ladder state comes from
 * model.states (the load-state owner); the ACTIVE slot is the
 * owner's answer, never a discovery guess. The import form's honest
 * web shape: ABSOLUTE paths as text (the browser hides local paths —
 * the native file/folder picker is the Tauri row's own concern, a
 * standing boundary, never silently faked here).
 *
 * Empty-state grammar (§9): MISSING directory, the empty folder, and
 * NO MODELS each render their own honest state; every read/dispatch
 * lane renders distinctly; a REJECTED anything renders the gateway's
 * reason VERBATIM. One run at a time; the observation is bounded
 * (dead at terminal/TRANSPORT/unmount); the terminal triggers
 * exactly ONE context re-read — never polling.
 */
import type { ReactNode } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type {
  ModelListEntry,
  ModelListResult,
  ModelStatesResult,
} from "../../api/gateway/contracts.ts";
import { formatNumber, tr } from "../../i18n/index.ts";
import type {
  ContextLoad,
  ModelsCancelOutcome,
  ModelsReplayLane,
  ModelsRunLane,
  ModelsRunOutcome,
  ModelsRunProgress,
  ReplayLineage,
} from "./useModels.ts";
import { isReplayableModelWorkKind, isTerminalRunLane, useModels } from "./useModels.ts";

export interface ModelsProps {
  readonly client: GatewayClient;
  /** the run family's + load/unload ops are session-scoped: null
   * disables every dispatch honestly (the two context READs stay
   * available — they are session-free). */
  readonly sessionId: string | null;
  readonly className?: string;
}

export function Models(props: ModelsProps): ReactNode {
  const models = useModels({ client: props.client, sessionId: props.sessionId });

  const fetchDisabled =
    props.sessionId === null || models.busy || models.runInFlight || models.fetchDraft.url.trim() === "";
  const importDisabled =
    props.sessionId === null || models.busy || models.runInFlight || models.importDraft.trim() === "";

  return (
    <section
      className={props.className ?? "surface"}
      aria-label={tr("models.region")}
      data-testid="models-surface"
    >
      <header className="surface-header">
        <h2>{tr("models.title")}</h2>
        <p className="surface-note">{tr("models.note")}</p>
      </header>

      <ContextStrip models={models.models} modelStates={models.modelStates} onRefresh={() => void models.refreshContext()} />

      <DiscoveryList
        models={models.models}
        modelStates={models.modelStates}
        sessionId={props.sessionId}
        busy={models.busy}
        runInFlight={models.runInFlight}
        onLoad={(name) => void models.load(name)}
        onUnload={(name) => void models.unload(name)}
        onDigest={(name) => void models.digest(name)}
      />

      {/* ARRIVAL — both forms are RUNS (identity-then-poll, live progress). */}
      <div className="models-arrival">
        <form
          className="models-arrival-form"
          onSubmit={(event) => {
            event.preventDefault();
            void models.fetchModel();
          }}
        >
          <h3>{tr("models.arrival.fetchTitle")}</h3>
          <label className="settings-field">
            <span className="settings-label">
              {tr("models.arrival.urlLabel")}{" "}
              <em>{tr("models.arrival.urlHint")}</em>
            </span>
            <input
              name="fetch-url"
              type="text"
              data-testid="models-fetch-url"
              value={models.fetchDraft.url}
              disabled={props.sessionId === null}
              placeholder={tr("models.arrival.urlPlaceholder")}
              onChange={(event) => models.editFetchDraft("url", event.target.value)}
            />
          </label>
          <label className="settings-field">
            <span className="settings-label">
              {tr("models.arrival.saveAs")}{" "}
              <em>{tr("models.arrival.saveAsHint")}</em>
            </span>
            <input
              name="fetch-name"
              type="text"
              data-testid="models-fetch-name"
              value={models.fetchDraft.name}
              disabled={props.sessionId === null}
              placeholder={tr("models.arrival.saveAsPlaceholder")}
              onChange={(event) => models.editFetchDraft("name", event.target.value)}
            />
          </label>
          <div className="controls">
            <button type="submit" disabled={fetchDisabled}>
              {tr("models.arrival.fetch")}
            </button>
            <span className="controls-note">{tr("models.arrival.fetchNote")}</span>
          </div>
        </form>

        <form
          className="models-arrival-form"
          onSubmit={(event) => {
            event.preventDefault();
            void models.importPaths();
          }}
        >
          <h3>{tr("models.arrival.importTitle")}</h3>
          <label className="settings-field">
            <span className="settings-label">
              {tr("models.arrival.pathsLabel")}{" "}
              <em>{tr("models.arrival.pathsHint")}</em>
            </span>
            <textarea
              name="import-paths"
              data-testid="models-import-paths"
              rows={3}
              value={models.importDraft}
              disabled={props.sessionId === null}
              placeholder={"/home/you/models/tiny.gguf\nD:\\llama.cpp\\models\\q4km.gguf"}
              onChange={(event) => models.editImportDraft(event.target.value)}
            />
          </label>
          <div className="controls">
            <button type="submit" disabled={importDisabled}>
              {tr("models.arrival.import")}
            </button>
            <span className="controls-note">{tr("models.arrival.importNote")}</span>
          </div>
        </form>
      </div>

      <RunLane
        run={models.run}
        cancelOutcome={models.cancelOutcome}
        replayLane={models.replayLane}
        replayLineage={models.replayLineage}
        onRepoll={models.repoll}
        onCancel={() => void models.cancel()}
        onReplay={() => void models.replay()}
        replayDisabled={props.sessionId === null || models.busy || models.runInFlight}
        busy={models.busy}
      />

      {props.sessionId === null ? (
        <p className="empty">{tr("models.noSession")}</p>
      ) : null}
    </section>
  );
}

/** The strip: the folder itself (the gateway's own answer, never a
 * local guess), the directory classification, the count, and the
 * ACTIVE slot (the load-state owner's truth) + the explicit
 * re-read (every later read is the user's own action). */
function ContextStrip(props: {
  readonly models: ContextLoad<ModelListResult>;
  readonly modelStates: ContextLoad<ModelStatesResult>;
  readonly onRefresh: () => void;
}): ReactNode {
  const { models, modelStates } = props;
  const listing = models.kind === "LOADED" ? models.result : null;
  const states = modelStates.kind === "LOADED" ? modelStates.result : null;
  return (
    <>
      <div className="strip" data-testid="models-context">
        <span>
          {tr("models.context.folder")} <code>{listing !== null ? listing.models_root : "—"}</code>
        </span>
        <span>
          {tr("models.context.directory")}{" "}
          <code>{listing !== null ? listing.directory_state : "—"}</code>
        </span>
        <span>
          {tr("models.context.discovered")}{" "}
          <code>{listing !== null ? formatNumber(listing.models.length) : "—"}</code>
        </span>
        <span>
          {tr("models.context.active")}{" "}
          <code data-testid="models-active">
            {states !== null ? (states.active ?? tr("models.context.none")) : "—"}
          </code>
        </span>
        <button type="button" onClick={props.onRefresh}>
          {tr("models.context.refresh")}
        </button>
      </div>
      <ContextLane title="model.list" load={models.kind} detail={laneDetail(models)} />
      <ContextLane title="model.states" load={modelStates.kind} detail={laneDetail(modelStates)} />
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
      {tr("models.context.laneJoin", {
        title: props.title,
        load: props.load,
        detail: props.detail,
      })}
    </div>
  );
}

function laneDetail(load: ContextLoad<unknown>): string | null {
  if (load.kind === "TRANSPORT")
    return tr("models.context.laneRetry", { failure: load.failure });
  if (load.kind === "MISMATCH") return tr("models.context.laneMismatch", { error: load.error });
  if (load.kind === "REJECTED") {
    return tr("models.context.laneRejected", {
      rejection: load.rejection,
      reason: load.reason ?? tr("models.context.noReason"),
    });
  }
  return null;
}

/** The §20 discovery list: one row per discovered file, the ladder
 * chip from model.states (joined by logical_name — the observed
 * truth, never a discovery guess), the ACTIVE marker, the strong
 * identity (or the digest affordance), and the load/unload
 * dispatches with their honest disabled states. */
function DiscoveryList(props: {
  readonly models: ContextLoad<ModelListResult>;
  readonly modelStates: ContextLoad<ModelStatesResult>;
  readonly sessionId: string | null;
  readonly busy: boolean;
  readonly runInFlight: boolean;
  readonly onLoad: (logicalName: string) => void;
  readonly onUnload: (logicalName: string) => void;
  readonly onDigest: (logicalName: string) => void;
}): ReactNode {
  const { models, modelStates } = props;
  if (models.kind !== "LOADED") {
    return <p className="empty">{tr("models.list.notLanded")}</p>;
  }
  const listing = models.result;
  const states = modelStates.kind === "LOADED" ? modelStates.result.states : {};
  const active = modelStates.kind === "LOADED" ? modelStates.result.active : null;

  if (listing.directory_state === "MISSING") {
    return (
      <p className="empty" data-testid="models-missing">
        {tr("models.list.missing")}
      </p>
    );
  }
  if (listing.models.length === 0) {
    return (
      <p className="empty" data-testid="models-empty">
        {tr("models.list.empty")}
      </p>
    );
  }
  return (
    <ul className="models-list" data-testid="models-list">
      {listing.models.map((entry) => (
        <ModelRow
          key={entry.logical_name}
          entry={entry}
          ladderState={states[entry.logical_name] ?? "DISCOVERED"}
          isActive={active === entry.logical_name}
          disabled={props.sessionId === null || props.busy || props.runInFlight}
          onLoad={props.onLoad}
          onUnload={props.onUnload}
          onDigest={props.onDigest}
        />
      ))}
    </ul>
  );
}

/** One discovery row — the ladder chip is the OBSERVED state (the
 * load-state owner's answer for THIS name; DISCOVERED when never
 * touched), the ACTIVE marker its own channel. */
function ModelRow(props: {
  readonly entry: ModelListEntry;
  readonly ladderState: string;
  readonly isActive: boolean;
  readonly disabled: boolean;
  readonly onLoad: (logicalName: string) => void;
  readonly onUnload: (logicalName: string) => void;
  readonly onDigest: (logicalName: string) => void;
}): ReactNode {
  const { entry, ladderState, isActive } = props;
  return (
    <li className="models-row" data-testid={`models-row-${entry.logical_name}`}>
      <div className="models-row-head">
        <span className="models-name">{entry.logical_name}</span>
        {isActive ? <span className="tag tag-live">{tr("models.row.activeMarker")}</span> : null}
        <span className={`control-state state-ladder-${ladderState.toLowerCase()}`}>
          {ladderState}
        </span>
      </div>
      <div className="models-row-meta">
        <span>{formatBytes(entry.size_bytes)}</span>
        <span className="models-digest" title={entry.content_digest ?? undefined}>
          {entry.content_digest !== null
            ? `sha256 ${entry.content_digest.slice(0, 16)}…`
            : tr("models.row.noIdentity")}
        </span>
      </div>
      <div className="controls">
        <button
          type="button"
          disabled={props.disabled || isActive || ladderState === "FAILED"}
          title={
            ladderState === "FAILED"
              ? tr("models.row.loadTitleFailed")
              : tr("models.row.loadTitle")
          }
          onClick={() => props.onLoad(entry.logical_name)}
        >
          {tr("models.row.load")}
        </button>
        <button
          type="button"
          disabled={props.disabled || !isActive}
          title={tr("models.row.unloadTitle")}
          onClick={() => props.onUnload(entry.logical_name)}
        >
          {tr("models.row.unload")}
        </button>
        <button
          type="button"
          disabled={props.disabled || entry.content_digest !== null}
          title={tr("models.row.digestTitle")}
          onClick={() => props.onDigest(entry.logical_name)}
        >
          {entry.content_digest !== null
            ? tr("models.row.identityComputed")
            : tr("models.row.computeIdentity")}
        </button>
      </div>
    </li>
  );
}

/** The ONE run's honest closure lane — every stage rendered as
 * itself; the progress verbatim per work kind; the cancel answer
 * verbatim (a request's answer, never a completion); at terminal, the
 * replay affordance (a NEW execution over the frozen material,
 * offered only for the kinds the composition wires an adapter for). */
function RunLane(props: {
  readonly run: ModelsRunLane | null;
  readonly cancelOutcome: ModelsCancelOutcome | null;
  readonly replayLane: ModelsReplayLane | null;
  readonly replayLineage: ReplayLineage | null;
  readonly busy: boolean;
  readonly onRepoll: () => void;
  readonly onCancel: () => void;
  readonly onReplay: () => void;
  readonly replayDisabled: boolean;
}): ReactNode {
  const { run } = props;
  if (run === null) {
    return (
      <p className="empty" data-testid="models-run-idle">
        {tr("models.run.idle")}
      </p>
    );
  }
  return (
    <div className="models-run" data-testid="models-run-lane">
      {props.replayLineage !== null ? (
        <p className="empty" data-testid="models-replay-lineage">
          {tr("models.run.replayLineageA")}{" "}
          <code>{shortId(props.replayLineage.replayedFrom)}</code>{" "}
          {tr("models.run.replayLineageJoin")}{" "}
          <code>{shortId(props.replayLineage.executionId)}</code>{" "}
          {tr("models.run.replayLineageB")}
        </p>
      ) : null}      {run.kind === "DISPATCHING" ? (
        <p className="empty">{tr("models.run.admitting", { work: run.work })}</p>
      ) : null}
      {run.kind === "IN_FLIGHT" ? (
        <>
          <p className="empty" data-testid="models-run-inflight">
            {tr("models.run.inFlight", {
              id: shortId(run.executionId),
              work: run.work,
              state: run.runState,
            })}
            {run.stale ? tr("models.run.staleMarker") : tr("models.run.inFlightEllipsis")}
          </p>
          <ProgressLine progress={run.progress} />
          {props.cancelOutcome !== null ? (
            <p className="empty" data-testid="models-cancel-outcome">
              {tr("models.run.cancelOutcomeLabel")}{" "}
              <code>{cancelOutcomeText(props.cancelOutcome)}</code>{" "}
              {tr("models.run.cancelTail")}
            </p>
          ) : null}
          {run.stale ? (
            <div className="banner banner-stale" role="alert">
              {tr("models.run.repollNote", { failure: run.failure ?? "" })}
              <button type="button" className="chat-repoll" onClick={props.onRepoll}>
                {tr("models.run.repoll")}
              </button>
            </div>
          ) : (
            <button type="button" onClick={props.onCancel} disabled={props.busy}>
              {tr("models.run.stop")}
            </button>
          )}
        </>
      ) : null}
      {run.kind === "COMPLETED" ? <CompletedOutcome outcome={run.outcome} /> : null}
      {run.kind === "COMPLETED_MISMATCH" ? (
        <div className="banner banner-error" role="alert">
          {tr("models.run.completedMismatch", { work: run.work })}
        </div>
      ) : null}
      {run.kind === "FAILED" ? (
        <div className="banner banner-error" role="alert" data-testid="models-run-failed">
          {tr("models.run.failed", {
            work: run.work,
            failureType: run.failureType ?? tr("models.run.noFailureType"),
            diagnostics:
              run.diagnostics.length > 0
                ? run.diagnostics.join(" | ")
                : tr("models.run.noDiagnostics"),
          })}
        </div>
      ) : null}
      {run.kind === "OTHER_TERMINAL" ? (
        <div className="banner banner-stale" role="alert" data-testid="models-run-terminal">
          {tr("models.run.terminal", { work: run.work, state: run.runState })}
          {run.diagnostics.length > 0 ? ` — ${run.diagnostics.join(" | ")}` : ""}
        </div>
      ) : null}
      {run.kind === "DISPATCH_REJECTED" ? (
        <div className="banner banner-error" role="alert">
          {tr("models.run.dispatchRejected", {
            rejection: run.rejection,
            reason: run.reason ?? tr("models.run.noReason"),
          })}
        </div>
      ) : null}
      {run.kind === "DISPATCH_TRANSPORT" ? (
        <div className="banner banner-error" role="alert">
          {tr("models.run.dispatchTransport", { failure: run.failure })}
        </div>
      ) : null}
      {run.kind === "DISPATCH_MISMATCH" ? (
        <div className="banner banner-error" role="alert">
          {tr("models.run.dispatchMismatch", { error: run.error })}
        </div>
      ) : null}
      {run.kind === "POLL_REJECTED" ? (
        <div className="banner banner-error" role="alert">
          {tr("models.run.pollRejected", {
            rejection: run.rejection,
            reason: run.reason ?? tr("models.run.noReason"),
          })}
        </div>
      ) : null}
      {run.kind === "POLL_MISMATCH" ? (
        <div className="banner banner-error" role="alert">
          {tr("models.run.pollMismatch", { error: run.error })}
        </div>
      ) : null}
      {isTerminalRunLane(run) ? (
        <div className="controls" data-testid="models-run-actions">
          {isReplayableModelWorkKind(run.work) ? (
            <>
              <button
                type="button"
                disabled={props.replayDisabled}
                title={tr("models.run.replayTitle")}
                onClick={props.onReplay}
              >
                {tr("models.run.replay")}
              </button>
              <span className="controls-note">{tr("models.run.replayNote")}</span>
            </>
          ) : (
            <span className="controls-note">
              {tr("models.run.notReplayableNote", { work: run.work })}
            </span>
          )}
        </div>
      ) : null}
      <ReplayLaneBanners lane={props.replayLane} />
    </div>
  );
}

/** The stop's observed answer — the structural code (useModels'
 * ModelsCancelOutcome) rendered as its verbatim prose lane. */
function cancelOutcomeText(outcome: ModelsCancelOutcome): string {
  if (outcome.kind === "OBSERVED") return outcome.cancellation;
  if (outcome.kind === "TRANSPORT")
    return tr("models.run.cancelTransport", { kind: outcome.failureKind });
  if (outcome.kind === "MISMATCH")
    return tr("models.run.cancelMismatch", { error: outcome.error });
  return tr("models.run.cancelRejected", {
    rejection: outcome.rejection,
    reason: outcome.reason ?? tr("models.run.noReason"),
  });
}

/** The replay dispatch's honest closure, verbatim per lane. */
function ReplayLaneBanners(props: { readonly lane: ModelsReplayLane | null }): ReactNode {
  const lane = props.lane;
  if (lane === null || lane.kind === "DISPATCHING") {
    return lane === null ? null : <p className="empty">{tr("models.replay.dispatching")}</p>;
  }
  if (lane.kind === "ADMITTED") {
    return (
      <p className="empty" data-testid="models-replay-admitted">
        {tr("models.replay.admittedA")} <code>{shortId(lane.executionId)}</code>{" "}
        {tr("models.replay.admittedB")}
      </p>
    );
  }
  if (lane.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("models.replay.rejected", {
          rejection: lane.rejection,
          reason: lane.reason ?? tr("models.run.noReason"),
        })}
      </div>
    );
  }
  if (lane.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("models.replay.transport", { failure: lane.failure })}
      </div>
    );
  }
  return (
    <div className="banner banner-error" role="alert">
      {tr("models.replay.mismatch", { error: lane.error })}
    </div>
  );
}

/** The live progress line, verbatim per work kind. */
function ProgressLine(props: { readonly progress: ModelsRunProgress | null }): ReactNode {
  const { progress } = props;
  if (progress === null) return null;
  if (progress.kind === "FETCH") {
    const { progress: fetch } = progress;
    return (
      <p className="empty" data-testid="models-progress">
        {fetch.total_bytes !== null
          ? tr("models.progress.fetch", {
              name: fetch.logical_name,
              downloaded: formatBytes(fetch.downloaded_bytes),
              total: formatBytes(fetch.total_bytes),
            })
          : tr("models.progress.fetchTotalUnknown", {
              name: fetch.logical_name,
              downloaded: formatBytes(fetch.downloaded_bytes),
            })}
      </p>
    );
  }
  if (progress.kind === "IMPORT") {
    const { progress: imported } = progress;
    return (
      <p className="empty" data-testid="models-progress">
        {tr("models.progress.importRow", {
          index: String(imported.file_index + 1),
          count: String(imported.file_count),
          name: imported.logical_name,
          copied: formatBytes(imported.copied_bytes),
          total: formatBytes(imported.total_bytes),
        })}
      </p>
    );
  }
  return (
    <p className="empty" data-testid="models-progress">{tr("models.progress.unrecognized")}</p>
  );
}

/** The completed run's observed result, rendered per work kind. */
function CompletedOutcome(props: { readonly outcome: ModelsRunOutcome }): ReactNode {
  const { outcome } = props;
  if (outcome.work === "model.load") {
    return (
      <div className="banner banner-accepted" data-testid="models-run-completed">
        {tr("models.outcome.loadSplitA")} <code>{outcome.result.logical_name}</code>{" "}
        {tr("models.outcome.loadSplitB")}
      </div>
    );
  }
  if (outcome.work === "model.unload") {
    return (
      <div className="banner banner-accepted" data-testid="models-run-completed">
        {tr("models.outcome.unloadSplitA")} <code>{outcome.result.logical_name}</code>{" "}
        {tr("models.outcome.unloadSplitB")}
      </div>
    );
  }
  if (outcome.work === "model.fetch") {
    return (
      <div className="banner banner-accepted" data-testid="models-run-completed">
        {tr("models.outcome.fetchA")} <code>{outcome.result.logical_name}</code>{" "}
        {tr("models.outcome.fetchB", { size: formatBytes(outcome.result.size_bytes) })}{" "}
        {tr("models.outcome.fetchC", { url: outcome.result.url })}
      </div>
    );
  }
  if (outcome.work === "model.import") {
    return (
      <div className="banner banner-accepted" data-testid="models-run-completed">
        {tr("models.outcome.importA", { count: String(outcome.result.count) })}{" "}
        {outcome.result.imported
          .map((file) => `${file.logical_name} (${formatBytes(file.size_bytes)})`)
          .join(", ")}
      </div>
    );
  }
  return (
    <div className="banner banner-accepted" data-testid="models-run-completed">
      {tr("models.outcome.identityA")} <code>{outcome.result.logical_name}</code>{" "}
      {tr("models.outcome.identityJoin")}{" "}
      {tr("models.outcome.identityB", {
        digest: outcome.result.content_digest,
        chunks: String(outcome.result.chunks),
        size: formatBytes(outcome.result.size_bytes),
      })}
    </div>
  );
}

function formatBytes(size: number): string {
  if (size < 1024) return `${String(size)} B`;
  const units = ["KiB", "MiB", "GiB", "TiB"];
  let value = size;
  let unit = -1;
  do {
    value /= 1024;
    unit += 1;
  } while (value >= 1024 && unit < units.length - 1);
  return `${value.toFixed(value >= 100 ? 0 : 1)} ${units[unit]}`;
}

function shortId(executionId: string): string {
  return executionId.length <= 12 ? executionId : `${executionId.slice(0, 8)}…`;
}
