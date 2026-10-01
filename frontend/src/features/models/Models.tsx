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
import type {
  ContextLoad,
  ModelsRunLane,
  ModelsRunOutcome,
  ModelsRunProgress,
} from "./useModels.ts";
import { useModels } from "./useModels.ts";

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
      aria-label="Models — the model family"
      data-testid="models-surface"
    >
      <header className="surface-header">
        <h2>Models</h2>
        <p className="surface-note">
          the model family — discovery, arrival, and the load ladder; a file on disk proves
          nothing: discovered ≠ selected ≠ loading ≠ active, and the ladder state is the
          backend&rsquo;s own answer, never a guess
        </p>
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
          <h3>fetch from anywhere</h3>
          <label className="settings-field">
            <span className="settings-label">
              URL <em>(a direct http(s) link, a huggingface.co page, or the hf:repo/file shorthand)</em>
            </span>
            <input
              name="fetch-url"
              type="text"
              data-testid="models-fetch-url"
              value={models.fetchDraft.url}
              disabled={props.sessionId === null}
              placeholder="https://huggingface.co/<org>/<repo>/resolve/main/<model>.gguf"
              onChange={(event) => models.editFetchDraft("url", event.target.value)}
            />
          </label>
          <label className="settings-field">
            <span className="settings-label">
              save as <em>(empty = the URL&rsquo;s own file name)</em>
            </span>
            <input
              name="fetch-name"
              type="text"
              data-testid="models-fetch-name"
              value={models.fetchDraft.name}
              disabled={props.sessionId === null}
              placeholder="model.gguf"
              onChange={(event) => models.editFetchDraft("name", event.target.value)}
            />
          </label>
          <div className="controls">
            <button type="submit" disabled={fetchDisabled}>
              fetch
            </button>
            <span className="controls-note">
              a run with live progress — the file lands for the NEXT discovery scan (a name
              already discovered or a leftover .part rejects at admission, never mid-flight)
            </span>
          </div>
        </form>

        <form
          className="models-arrival-form"
          onSubmit={(event) => {
            event.preventDefault();
            void models.importPaths();
          }}
        >
          <h3>import local files</h3>
          <label className="settings-field">
            <span className="settings-label">
              absolute paths <em>(one per line — the web form&rsquo;s honest input; the native picker is the desktop row&rsquo;s own concern)</em>
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
              import
            </button>
            <span className="controls-note">
              a local copy on the gateway&rsquo;s host (loopback — the same machine), no
              network; every admission gate (absolute, existing, plain name, unoccupied)
              rejects verbatim
            </span>
          </div>
        </form>
      </div>

      <RunLane run={models.run} cancelOutcome={models.cancelOutcome} onRepoll={models.repoll} onCancel={() => void models.cancel()} busy={models.busy} />

      {props.sessionId === null ? (
        <p className="empty">
          no session — every dispatch is disabled (model.load/model.unload/run.start are
          session-scoped); the two reads above stay available
        </p>
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
          folder <code>{listing !== null ? listing.models_root : "—"}</code>
        </span>
        <span>
          directory <code>{listing !== null ? listing.directory_state : "—"}</code>
        </span>
        <span>
          discovered <code>{listing !== null ? String(listing.models.length) : "—"}</code>
        </span>
        <span>
          active{" "}
          <code data-testid="models-active">
            {states !== null ? (states.active ?? "none") : "—"}
          </code>
        </span>
        <button type="button" onClick={props.onRefresh}>
          refresh
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
    return <p className="empty">the discovery scan has not landed yet</p>;
  }
  const listing = models.result;
  const states = modelStates.kind === "LOADED" ? modelStates.result.states : {};
  const active = modelStates.kind === "LOADED" ? modelStates.result.active : null;

  if (listing.directory_state === "MISSING") {
    return (
      <p className="empty" data-testid="models-missing">
        the models folder does not exist yet — fetch or import lands it (the composition
        creates it at startup; the scan says so honestly, never an error)
      </p>
    );
  }
  if (listing.models.length === 0) {
    return (
      <p className="empty" data-testid="models-empty">
        no model files discovered — fetch one from anywhere or import local files below
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
        {isActive ? <span className="tag tag-live">ACTIVE</span> : null}
        <span className={`control-state state-ladder-${ladderState.toLowerCase()}`}>
          {ladderState}
        </span>
      </div>
      <div className="models-row-meta">
        <span>{formatBytes(entry.size_bytes)}</span>
        <span className="models-digest" title={entry.content_digest ?? undefined}>
          {entry.content_digest !== null
            ? `sha256 ${entry.content_digest.slice(0, 16)}…`
            : "strong identity not computed"}
        </span>
      </div>
      <div className="controls">
        <button
          type="button"
          disabled={props.disabled || isActive || ladderState === "FAILED"}
          title={
            ladderState === "FAILED"
              ? "the ladder's FAILED is terminal (no re-selection path)"
              : "load — the admission walks the ladder to SELECTED; the load itself is a run"
          }
          onClick={() => props.onLoad(entry.logical_name)}
        >
          load
        </button>
        <button
          type="button"
          disabled={props.disabled || !isActive}
          title="unload — the graceful stop is a run; ACTIVE → EVICTED observed on its terminal"
          onClick={() => props.onUnload(entry.logical_name)}
        >
          unload
        </button>
        <button
          type="button"
          disabled={props.disabled || entry.content_digest !== null}
          title="compute the §9 strong identity as a run — the honest long arm for a multi-GB file (cancellable, observable)"
          onClick={() => props.onDigest(entry.logical_name)}
        >
          {entry.content_digest !== null ? "identity computed" : "compute identity"}
        </button>
      </div>
    </li>
  );
}

/** The ONE run's honest closure lane — every stage rendered as
 * itself; the progress verbatim per work kind; the cancel answer
 * verbatim (a request's answer, never a completion). */
function RunLane(props: {
  readonly run: ModelsRunLane | null;
  readonly cancelOutcome: string | null;
  readonly busy: boolean;
  readonly onRepoll: () => void;
  readonly onCancel: () => void;
}): ReactNode {
  const { run } = props;
  if (run === null) {
    return (
      <p className="empty" data-testid="models-run-idle">
        no run yet — every load, unload, fetch, import, and identity computation is an
        honest run: admitted, observed, terminal
      </p>
    );
  }
  return (
    <div className="models-run" data-testid="models-run-lane">
      {run.kind === "DISPATCHING" ? <p className="empty">admitting the run ({run.work})…</p> : null}
      {run.kind === "IN_FLIGHT" ? (
        <>
          <p className="empty" data-testid="models-run-inflight">
            run {shortId(run.executionId)} · {run.work} · {run.runState}
            {run.stale ? " · STALE (the observation itself failed)" : "…"}
          </p>
          <ProgressLine progress={run.progress} />
          {props.cancelOutcome !== null ? (
            <p className="empty" data-testid="models-cancel-outcome">
              stop requested — observed outcome: <code>{props.cancelOutcome}</code> (a
              request&rsquo;s answer, never a completion; the run&rsquo;s terminal state is
              the truth)
            </p>
          ) : null}
          {run.stale ? (
            <div className="banner banner-stale" role="alert">
              run.get TRANSPORT · {run.failure} — the outcome is UNKNOWN; the re-poll is
              your explicit action (no blind retry)
              <button type="button" className="chat-repoll" onClick={props.onRepoll}>
                re-poll
              </button>
            </div>
          ) : (
            <button type="button" onClick={props.onCancel} disabled={props.busy}>
              stop
            </button>
          )}
        </>
      ) : null}
      {run.kind === "COMPLETED" ? <CompletedOutcome outcome={run.outcome} /> : null}
      {run.kind === "COMPLETED_MISMATCH" ? (
        <div className="banner banner-error" role="alert">
          the run COMPLETED but its result deviates from the contract · {run.error} —
          reported, never coerced
        </div>
      ) : null}
      {run.kind === "FAILED" ? (
        <div className="banner banner-error" role="alert" data-testid="models-run-failed">
          run FAILED ({run.work}) · {run.failureType ?? "(no failure type)"} —{" "}
          {run.diagnostics.length > 0 ? run.diagnostics.join(" | ") : "(no diagnostics)"}
        </div>
      ) : null}
      {run.kind === "OTHER_TERMINAL" ? (
        <div className="banner banner-stale" role="alert" data-testid="models-run-terminal">
          run terminal · {run.work} · {run.runState}
          {run.diagnostics.length > 0 ? ` — ${run.diagnostics.join(" | ")}` : ""}
        </div>
      ) : null}
      {run.kind === "DISPATCH_REJECTED" ? (
        <div className="banner banner-error" role="alert">
          dispatch REJECTED · {run.rejection}: {run.reason ?? "(no reason)"} — nothing was
          sent; a new dispatch is your explicit new command (never an auto-retry)
        </div>
      ) : null}
      {run.kind === "DISPATCH_TRANSPORT" ? (
        <div className="banner banner-error" role="alert">
          dispatch TRANSPORT · {run.failure} — if the request was sent, the outcome is
          UNKNOWN (no blind retry)
        </div>
      ) : null}
      {run.kind === "DISPATCH_MISMATCH" ? (
        <div className="banner banner-error" role="alert">
          dispatch CONTRACT MISMATCH · {run.error} — reported, never coerced
        </div>
      ) : null}
      {run.kind === "POLL_REJECTED" ? (
        <div className="banner banner-error" role="alert">
          run.get REJECTED · {run.rejection}: {run.reason ?? "(no reason)"} — the
          observation itself was rejected; the run&rsquo;s truth is unreachable from here
        </div>
      ) : null}
      {run.kind === "POLL_MISMATCH" ? (
        <div className="banner banner-error" role="alert">
          run.get CONTRACT MISMATCH · {run.error} — reported, never coerced
        </div>
      ) : null}
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
        {fetch.logical_name}: {formatBytes(fetch.downloaded_bytes)}
        {fetch.total_bytes !== null ? ` of ${formatBytes(fetch.total_bytes)}` : " (total unknown — never a guess)"}
      </p>
    );
  }
  if (progress.kind === "IMPORT") {
    const { progress: imported } = progress;
    return (
      <p className="empty" data-testid="models-progress">
        file {String(imported.file_index + 1)}/{String(imported.file_count)} (
        {imported.logical_name}): {formatBytes(imported.copied_bytes)} of{" "}
        {formatBytes(imported.total_bytes)}
      </p>
    );
  }
  return (
    <p className="empty" data-testid="models-progress">
      progress reported in a shape this surface does not recognize — shown as itself, never
      coerced
    </p>
  );
}

/** The completed run's observed result, rendered per work kind. */
function CompletedOutcome(props: { readonly outcome: ModelsRunOutcome }): ReactNode {
  const { outcome } = props;
  if (outcome.work === "model.load") {
    return (
      <div className="banner banner-accepted" data-testid="models-run-completed">
        load COMPLETED — <code>{outcome.result.logical_name}</code> is ACTIVE (the ladder&rsquo;s
        own landing: SELECTED → LOADING → LOADED → ACTIVE)
      </div>
    );
  }
  if (outcome.work === "model.unload") {
    return (
      <div className="banner banner-accepted" data-testid="models-run-completed">
        unload COMPLETED — <code>{outcome.result.logical_name}</code> is EVICTED (the graceful
        stop&rsquo;s observed fold)
      </div>
    );
  }
  if (outcome.work === "model.fetch") {
    return (
      <div className="banner banner-accepted" data-testid="models-run-completed">
        fetch COMPLETED — <code>{outcome.result.logical_name}</code> landed (
        {formatBytes(outcome.result.size_bytes)}) from {outcome.result.url}; the NEXT
        discovery scan sees it
      </div>
    );
  }
  if (outcome.work === "model.import") {
    return (
      <div className="banner banner-accepted" data-testid="models-run-completed">
        import COMPLETED — {String(outcome.result.count)} file(s) landed:{" "}
        {outcome.result.imported.map((file) => `${file.logical_name} (${formatBytes(file.size_bytes)})`).join(", ")}
      </div>
    );
  }
  return (
    <div className="banner banner-accepted" data-testid="models-run-completed">
      identity COMPLETED — <code>{outcome.result.logical_name}</code>: sha256{" "}
      {outcome.result.content_digest} ({String(outcome.result.chunks)} chunks,{" "}
      {formatBytes(outcome.result.size_bytes)})
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
