/**
 * The Observatory surface (Phase 3's Observatory entry) — the HISTORY
 * half of the dual-read law (FRONTEND_WEB_LAW §4): the durable,
 * queryable evidence world over the COMMITTED canonical logs. Where
 * the Trajectory pane renders the LIVE session tail (volatile,
 * retention-limited), this pane renders bounded windows of past runs
 * — the two cursors NEVER mix, and each pane labels its own world.
 *
 * The analytical projection (§9): CONTEXT (the runs discovery scan)
 * → QUERY/SCOPE (the selected run + the event-id cursor) → PRIMARY
 * VIEW (the bounded event window) → INSPECTOR (the selected row's
 * SAME document — no second per-event op). The context strip carries
 * the run identity, seed, pack, profile, authority, and window
 * bounds — the honest identity line.
 *
 * Empty-state grammar (§9, kept distinct): NO DATA (the runs root
 * holds no committed runs) ≠ NO MATCH (the run does not exist) ≠
 * STALE CURSOR (the after-id left the run — re-read from the head)
 * ≠ TRANSPORT ≠ MISMATCH. A domain violation renders the gateway's
 * own reason VERBATIM — never a fabricated empty window.
 *
 * Boundedness: ONE window in memory (≤ the backend's 200 cap); the
 * forward pagination REPLACES the view — the client never
 * materializes a run, and there is no polling (history is durable;
 * every read is explicit).
 */
import { useMemo } from "react";
import type { ReactNode } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type { ObservatoryEventRow } from "../../api/gateway/contracts.ts";
import { tr } from "../../i18n/index.ts";
import { useObservatory } from "./useObservatory.ts";

export interface ObservatoryProps {
  readonly client: GatewayClient;
  readonly className?: string;
}

export function Observatory(props: ObservatoryProps): ReactNode {
  const observatory = useObservatory({ client: props.client });
  const { scan, view } = observatory;

  const selected = useMemo(() => {
    if (view.kind !== "WINDOW") return null;
    return view.result.window.events.find((row) => row.id === observatory.selectedEventId) ?? null;
  }, [view, observatory.selectedEventId]);

  return (
    <section className={props.className ?? "surface"} aria-label={tr("observatory.region")}>
      <header className="surface-header">
        <h2>
          {tr("observatory.title")}{" "}
          <span className="tag tag-history">{tr("observatory.tag")}</span>
        </h2>
        <p className="surface-note">{tr("observatory.note")}</p>
      </header>

      {/* CONTEXT — the discovery scan */}
      <div className="controls">
        <button onClick={() => void observatory.scanRuns()} disabled={observatory.busy}>
          {tr("observatory.controls.rescan")}
        </button>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            const input = event.currentTarget.elements.namedItem("run");
            if (input instanceof HTMLInputElement && input.value.trim() !== "") {
              void observatory.openRun(input.value.trim());
            }
          }}
        >
          <input name="run" placeholder={tr("observatory.controls.openStemPlaceholder")} />
          <button type="submit" disabled={observatory.busy}>
            {tr("observatory.controls.openStem")}
          </button>
        </form>
      </div>

      <RunsScanView scan={scan} onOpen={(run) => void observatory.openRun(run)} />

      {/* QUERY/SCOPE + PRIMARY VIEW — the selected run's window */}
      {view.kind === "NO_RUN_SELECTED" ? (
        <p className="empty">{tr("observatory.noRun")}</p>
      ) : (
        <ReadViewBody view={view} observatory={observatory} selected={selected} />
      )}
    </section>
  );
}

function RunsScanView(props: {
  readonly scan: ReturnType<typeof useObservatory>["scan"];
  readonly onOpen: (run: string) => void;
}): ReactNode {
  const { scan, onOpen } = props;
  if (scan.kind === "NOT_SCANNED") {
    return <p className="empty">{tr("observatory.scan.notScanned")}</p>;
  }
  if (scan.kind === "SCANNING") {
    return <p className="empty">{tr("observatory.scan.scanning")}</p>;
  }
  if (scan.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("observatory.scan.transport", { failure: scan.failure })}
      </div>
    );
  }
  if (scan.kind === "MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("observatory.scan.mismatch", { error: scan.error })}
      </div>
    );
  }
  const { result } = scan;
  return (
    <div className="runs-block" aria-label={tr("observatory.scan.blockLabel")}>
      <h3>
        {tr("observatory.scan.found", {
          root: result.runs_root,
          count: String(result.runs.length),
        })}
      </h3>
      {result.runs.length === 0 ? (
        <p className="empty">
          {tr("observatory.scan.noDataA")}{" "}
          <code>{tr("observatory.scan.noDataB")}</code>
        </p>
      ) : (
        <ul className="runs-list">
          {result.runs.map((run) => (
            <li key={run.name} className="runs-row">
              <button onClick={() => onOpen(run.name)} className="runs-open">
                {tr("observatory.scan.open")}
              </button>
              <span className="runs-name" title={run.name}>
                {run.name}
              </span>
              {run.header !== null ? (
                <span className="runs-meta">
                  {tr("observatory.scan.seed")} <code>{String(run.header.seed)}</code>{" "}
                  {tr("observatory.scan.join")} {run.header.pack}{" "}
                  {tr("observatory.scan.join")} {tr("observatory.scan.schema")}{" "}
                  <code>{run.header.schema_version}</code>{" "}
                  {tr("observatory.scan.join")} {formatBytes(run.size_bytes)}
                </span>
              ) : (
                <span className="runs-meta runs-error" title={run.error ?? ""}>
                  {tr("observatory.scan.headerUnreadable", {
                    error: run.error ?? tr("observatory.scan.unknownError"),
                  })}
                </span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function ReadViewBody(props: {
  readonly view: Exclude<ReturnType<typeof useObservatory>["view"], { kind: "NO_RUN_SELECTED" }>;
  readonly observatory: ReturnType<typeof useObservatory>;
  readonly selected: ObservatoryEventRow | null;
}): ReactNode {
  const { view, observatory, selected } = props;

  if (view.kind === "READING") {
    return <p className="empty">{tr("observatory.read.reading", { run: view.run })}</p>;
  }
  if (view.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("observatory.read.transport", { failure: view.failure })}
      </div>
    );
  }
  if (view.kind === "MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("observatory.read.mismatch", { error: view.error })}
      </div>
    );
  }
  if (view.kind === "REJECTED") {
    const stale = view.reason !== null && view.reason.includes("stale cursor");
    return (
      <div className="banner banner-error" role="alert" data-testid="read-rejected">
        <strong>
          {tr("observatory.read.rejectedA", {
            rejection: view.rejection,
            reason: view.reason ?? tr("chat.lane.noReason"),
          })}
        </strong>
        {stale ? (
          <>
            {" "}
            <button onClick={() => void observatory.openRun(view.run)}>
              {tr("observatory.read.reread")}
            </button>
          </>
        ) : null}
      </div>
    );
  }

  const { result } = view;
  const { window: window_, header } = result;
  const more = window_.next_after !== null;
  return (
    <>
      {/* The context strip — the honest identity line (§9). */}
      <div className="strip" data-testid="obs-context">
        <span>
          {tr("observatory.context.run")} <code>{result.run}</code>
        </span>
        <span>
          {tr("observatory.context.seed")} <code>{String(header.seed)}</code>
        </span>
        <span>{header.pack}</span>
        <span>
          {tr("observatory.context.profile")} <code>{result.profile}</code>
        </span>
        <span>
          {tr("observatory.context.authority")} <code>{result.authority}</code>
        </span>
        <span>
          {tr("observatory.context.events")}{" "}
          <code>
            {tr("observatory.context.eventsValue", {
              window: String(window_.events.length),
              total: String(result.total_events),
            })}
          </code>
        </span>
        <span>
          {tr("observatory.context.window")}{" "}
          <code>
            {window_.after === ""
              ? tr("observatory.context.fromHead")
              : tr("observatory.context.after", { id: short(window_.after, 10) })}{" "}
            {tr("observatory.context.limit")} {String(window_.limit)}
          </code>
        </span>
        <span className="freshness freshness-history">{tr("observatory.context.durable")}</span>
      </div>

      {/* PRIMARY VIEW — the bounded window (one at a time, replaced
          forward: never an ever-growing client buffer). */}
      <div className="controls">
        <button
          onClick={() => void observatory.nextWindow()}
          disabled={observatory.busy || !more}
          data-testid="next-window"
        >
          {more
            ? tr("observatory.window.next", { after: short(window_.next_after ?? "", 10) })
            : tr("observatory.window.end")}
        </button>
        <button onClick={() => void observatory.openRun(result.run)} disabled={observatory.busy}>
          {tr("observatory.window.reread")}
        </button>
        <span className="controls-note">
          {tr("observatory.window.note", {
            window: String(window_.events.length),
            total: String(result.total_events),
            tail: more
              ? tr("observatory.window.moreRemain")
              : tr("observatory.window.runEnd"),
          })}
        </span>
      </div>

      <div className="orow-header" aria-hidden="true">
        <span>{tr("observatory.header.tick")}</span>
        <span>{tr("observatory.header.type")}</span>
        <span>{tr("observatory.header.kind")}</span>
        <span>{tr("observatory.header.actor")}</span>
        <span>{tr("observatory.header.imp")}</span>
        <span>{tr("observatory.header.eventId")}</span>
      </div>
      <ul className="orow-list" aria-label={tr("observatory.windowLabel")}>
        {window_.events.map((row) => (
          <EventRowView
            key={row.id}
            row={row}
            selected={row.id === observatory.selectedEventId}
            onSelect={() => observatory.selectEvent(row.id)}
          />
        ))}
      </ul>

      {/* INSPECTOR — the selected row's SAME document (LAW §5.1). */}
      <div className="inspector" aria-label={tr("observatory.inspector.region")}>
        {selected === null ? (
          <p className="empty-inspector">{tr("observatory.inspector.empty")}</p>
        ) : (
          <pre data-testid="inspector-json">{JSON.stringify(selected, null, 2)}</pre>
        )}
      </div>
    </>
  );
}

function EventRowView(props: {
  readonly row: ObservatoryEventRow;
  readonly selected: boolean;
  readonly onSelect: () => void;
}): ReactNode {
  const { row, selected, onSelect } = props;
  return (
    <li
      className={`orow${selected ? " orow-selected" : ""}${row.importance === "high" ? " orow-high" : ""}`}
      onClick={onSelect}
      data-event-id={row.id}
      role="button"
      tabIndex={0}
      onKeyDown={(keyEvent) => {
        if (keyEvent.key === "Enter" || keyEvent.key === " ") {
          keyEvent.preventDefault();
          onSelect();
        }
      }}
    >
      <span className="cell-seq">{String(row.t)}</span>
      <span className="cell-type">{row.type}</span>
      <span className="cell-kind">{row.kind}</span>
      <span className="cell-actor">{row.actor}</span>
      <span className={`cell-imp cell-imp-${row.importance}`}>{row.importance}</span>
      <span className="cell-id" title={row.id}>
        {short(row.id, 14)}
      </span>
    </li>
  );
}

function formatBytes(size: number): string {
  if (size < 1024) return `${String(size)} B`;
  return `${(size / 1024).toFixed(1)} KiB`;
}

function short(value: string, max: number): string {
  if (value.length <= max) return value;
  return `${value.slice(0, Math.ceil(max / 2))}…${value.slice(-Math.floor(max / 2))}`;
}
