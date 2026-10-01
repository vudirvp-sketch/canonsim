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
    <section className={props.className ?? "surface"} aria-label="Observatory — committed history">
      <header className="surface-header">
        <h2>
          Observatory <span className="tag tag-history">HISTORY · COMMITTED LOGS</span>
        </h2>
        <p className="surface-note">
          durable, queryable, bounded windows over the canonical logs — never the live session
          tail (the Trajectory pane owns that world); no polling: every read is explicit
        </p>
      </header>

      {/* CONTEXT — the discovery scan */}
      <div className="controls">
        <button onClick={() => void observatory.scanRuns()} disabled={observatory.busy}>
          rescan runs
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
          <input name="run" placeholder="open run by stem… (e.g. run_125_0)" />
          <button type="submit" disabled={observatory.busy}>
            open stem
          </button>
        </form>
      </div>

      <RunsScanView scan={scan} onOpen={(run) => void observatory.openRun(run)} />

      {/* QUERY/SCOPE + PRIMARY VIEW — the selected run's window */}
      {view.kind === "NO_RUN_SELECTED" ? (
        <p className="empty">no run open — scan the runs root or open a run by its stem</p>
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
    return <p className="empty">not scanned yet — the runs discovery is your explicit read</p>;
  }
  if (scan.kind === "SCANNING") {
    return <p className="empty">scanning the runs root…</p>;
  }
  if (scan.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        runs scan TRANSPORT · {scan.failure} — the gateway may be down; the scan is your explicit
        retry
      </div>
    );
  }
  if (scan.kind === "MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        runs scan CONTRACT MISMATCH · {scan.error} — reported, never coerced
      </div>
    );
  }
  const { result } = scan;
  return (
    <div className="runs-block" aria-label="discovered runs">
      <h3>
        runs <code>{result.runs_root}</code> — {String(result.runs.length)} found
      </h3>
      {result.runs.length === 0 ? (
        <p className="empty">
          NO DATA — the runs root holds no committed runs (generate one: the CLI writes
          <code> logs/*.jsonl</code>)
        </p>
      ) : (
        <ul className="runs-list">
          {result.runs.map((run) => (
            <li key={run.name} className="runs-row">
              <button onClick={() => onOpen(run.name)} className="runs-open">
                open
              </button>
              <span className="runs-name" title={run.name}>
                {run.name}
              </span>
              {run.header !== null ? (
                <span className="runs-meta">
                  seed <code>{String(run.header.seed)}</code> · {run.header.pack} · schema{" "}
                  <code>{run.header.schema_version}</code> ·{" "}
                  {formatBytes(run.size_bytes)}
                </span>
              ) : (
                <span className="runs-meta runs-error" title={run.error ?? ""}>
                  header unreadable — {run.error ?? "unknown error"} (the listing degrades
                  honestly; the run stays openable, its read will name the cause)
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
    return <p className="empty">reading run {view.run}…</p>;
  }
  if (view.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        read TRANSPORT · {view.failure} — delivery failed, never a gateway rejection; the re-read
        is your explicit decision
      </div>
    );
  }
  if (view.kind === "MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        read CONTRACT MISMATCH · {view.error} — reported, never coerced
      </div>
    );
  }
  if (view.kind === "REJECTED") {
    const stale = view.reason !== null && view.reason.includes("stale cursor");
    return (
      <div className="banner banner-error" role="alert" data-testid="read-rejected">
        <strong>REJECTED · {view.rejection}</strong> — {view.reason ?? "(no reason)"}
        {stale ? (
          <>
            {" "}
            <button onClick={() => void observatory.openRun(view.run)}>re-read from the head</button>
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
          run <code>{result.run}</code>
        </span>
        <span>
          seed <code>{String(header.seed)}</code>
        </span>
        <span>{header.pack}</span>
        <span>
          profile <code>{result.profile}</code>
        </span>
        <span>
          authority <code>{result.authority}</code>
        </span>
        <span>
          events{" "}
          <code>
            {String(window_.events.length)}/{String(result.total_events)}
          </code>
        </span>
        <span>
          window{" "}
          <code>
            {window_.after === "" ? "from head" : `after ${short(window_.after, 10)}`} · limit{" "}
            {String(window_.limit)}
          </code>
        </span>
        <span className="freshness freshness-history">DURABLE</span>
      </div>

      {/* PRIMARY VIEW — the bounded window (one at a time, replaced
          forward: never an ever-growing client buffer). */}
      <div className="controls">
        <button
          onClick={() => void observatory.nextWindow()}
          disabled={observatory.busy || !more}
          data-testid="next-window"
        >
          next window {more ? `(after ${short(window_.next_after ?? "", 10)})` : "— end of run"}
        </button>
        <button onClick={() => void observatory.openRun(result.run)} disabled={observatory.busy}>
          re-read from the head
        </button>
        <span className="controls-note">
          {String(window_.events.length)} events in this window · {String(result.total_events)}{" "}
          committed total {more ? "· more remain" : "· this is the run's end"}
        </span>
      </div>

      <div className="orow-header" aria-hidden="true">
        <span>tick</span>
        <span>type</span>
        <span>kind</span>
        <span>actor</span>
        <span>imp</span>
        <span>event id</span>
      </div>
      <ul className="orow-list" aria-label="event window">
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
      <div className="inspector" aria-label="selected history event">
        {selected === null ? (
          <p className="empty-inspector">
            no selection — click a row (selection is by event id, the semantic identity)
          </p>
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
