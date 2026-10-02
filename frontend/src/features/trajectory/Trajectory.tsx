/**
 * The Trajectory surface (S0-2): an ordered, read-only projection of
 * the session's LIVE event tail — rendered over the virtualized
 * list, cursor = the semantic sequence, selection = the event_id
 * (never a row index).
 *
 * DUAL-READ LAW (FRONTEND_WEB_LAW §4): this view is labelled LIVE
 * SESSION TAIL — volatile, retention-limited, resync-on-gap. It is
 * NEVER presented as the durable history of past runs (the
 * Observatory's read-side owns that world; nothing here queries
 * it). The empty-state grammar stays honest: NO DATA (the session
 * has no events yet) is not STALE (reads failing with data held)
 * and not DISCONNECTED (never read successfully).
 */
import { useCallback, useMemo, useState } from "react";
import type { ReactNode } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type { TailEvent } from "./useLiveTail.ts";
import { useLiveTail } from "./useLiveTail.ts";
import { VirtualList, nextScrollToken } from "./VirtualList.tsx";
import type { ScrollCommand, ScrollRequest } from "./VirtualList.tsx";

const ROW_HEIGHT = 28;
const VIEWPORT_HEIGHT = 420;

/** The tail's feed choices: the SSE stream (the admission step 3+4
 * landing — the default) or the POST poll ladder (S0's mandate,
 * always valid — the stream's own fallback), down to off. */
const FEED_CHOICES: readonly { readonly label: string; readonly value: string }[] = [
  { label: "stream (SSE)", value: "stream" },
  { label: "poll 1s", value: "1000" },
  { label: "poll 2s", value: "2000" },
  { label: "poll 5s", value: "5000" },
  { label: "off", value: "0" },
];

export interface TrajectoryProps {
  readonly client: GatewayClient;
  readonly sessionId: string | null;
  readonly className?: string;
}

export function Trajectory(props: TrajectoryProps): ReactNode {
  const [feed, setFeed] = useState("stream");
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);
  const [scrollCommand, setScrollCommand] = useState<ScrollCommand | null>(null);
  const [scrollToken, setScrollToken] = useState(0);

  const tail = useLiveTail({
    client: props.client,
    sessionId: props.sessionId,
    transport: feed === "stream" ? "stream" : "poll",
    intervalMs: feed === "stream" ? 0 : Number.parseInt(feed, 10),
  });

  const events = tail.events;
  const selectedIndex = useMemo(
    () => events.findIndex((event) => event.event_id === selectedEventId),
    [events, selectedEventId],
  );
  const selected = selectedIndex >= 0 ? events[selectedIndex] : null;

  const scroll = useCallback((command: ScrollRequest) => {
    const token = nextScrollToken(scrollToken);
    setScrollToken(token);
    setScrollCommand({ ...command, token } as ScrollCommand);
  }, [scrollToken]);

  const jumpToSequence = useCallback(
    (raw: string) => {
      const target = Number.parseInt(raw, 10);
      if (!Number.isFinite(target)) return;
      // The SEMANTIC cursor: find the row by its sequence, never by
      // assuming the row index equals the sequence (the buffer is a
      // window; sequences and indices diverge after trims/synthetic).
      let index = -1;
      for (let i = events.length - 1; i >= 0; i -= 1) {
        if (events[i]!.sequence === target) {
          index = i;
          break;
        }
      }
      if (index >= 0) {
        scroll({ kind: "INDEX", index });
        setSelectedEventId(events[index]!.event_id);
      }
    },
    [events, scroll],
  );

  return (
    <section className={props.className ?? "surface"} aria-label="Trajectory — live session tail">
      <header className="surface-header">
        <h2>
          Trajectory <span className="tag tag-live">LIVE SESSION TAIL</span>
        </h2>
        <p className="surface-note">
          volatile, retention-limited, resync-on-gap — not durable history
          (the Observatory read-side owns the durable world)
        </p>
        <div className="strip">
          <span>session <code>{props.sessionId === null ? "—" : short(props.sessionId, 12)}</code></span>
          <span>seq <code>{String(tail.lastSequence)}</code></span>
          <span>rows <code>{String(events.length)}</code></span>
          <span className={`freshness freshness-${tail.freshness.toLowerCase()}`}>{tail.freshness}</span>
          {feed === "stream" ? (
            <span className="stream-phase" data-testid="stream-phase">
              stream {tail.streamPhase ?? "—"}
            </span>
          ) : (
            <span>poll {tail.polling ? "on" : "off"}</span>
          )}
          <span>
            read{" "}
            <code>{tail.lastReadAt === null ? "never" : new Date(tail.lastReadAt).toISOString().slice(11, 19)}</code>
          </span>
        </div>
      </header>

      {tail.resync !== null ? (
        <div className="banner banner-resync" role="status">
          RESYNC_REQUIRED — the cursor fell out of the retained tail (FIFO eviction, not canon loss);
          re-read from the server's retained window (from seq {String(tail.resync.retainedFrom)}).
        </div>
      ) : null}
      {tail.syntheticCount > 0 ? (
        <div className="banner banner-synthetic" role="status">
          {String(tail.syntheticCount)} synthetic load-test rows appended — presentation-only, not gateway
          truth. <button onClick={() => tail.clearSynthetic()}>clear</button>
        </div>
      ) : null}
      {tail.trimmedCount > 0 ? (
        <div className="banner banner-trim">
          {String(tail.trimmedCount)} older rows trimmed from the presentation window (the buffer is
          bounded; durable evidence lives on the server).
        </div>
      ) : null}
      {tail.transportNote !== null ? (
        <div
          className={`banner ${tail.freshness === "STALE" ? "banner-stale" : "banner-error"}`}
          role={tail.freshness === "STALE" ? "status" : "alert"}
        >
          {tail.transportNote}
          {tail.freshness === "DISCONNECTED" ? " — presentation is last-known, not fresh" : ""}
        </div>
      ) : null}

      <div className="controls">
        <label>
          feed{" "}
          <select
            aria-label="feed transport"
            value={feed}
            onChange={(event) => {
              setFeed(event.target.value);
            }}
          >
            {FEED_CHOICES.map((choice) => (
              <option key={choice.value} value={choice.value}>
                {choice.label}
              </option>
            ))}
          </select>
        </label>
        <button onClick={() => void tail.refreshNow()} disabled={props.sessionId === null} title="the POST read — always valid (S0's mandate is the stream's own fallback)">
          refresh now
        </button>
        <button onClick={() => scroll({ kind: "TOP" })}>top</button>
        <button onClick={() => scroll({ kind: "BOTTOM" })}>latest</button>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            const input = event.currentTarget.elements.namedItem("seq");
            if (input instanceof HTMLInputElement) jumpToSequence(input.value);
          }}
        >
          <input name="seq" placeholder="jump to seq…" inputMode="numeric" />
          <button type="submit">go</button>
        </form>
        <span className="spacer" />
        <button className="probe" onClick={() => tail.appendSynthetic(1000)}>
          +1k synthetic
        </button>
        <button className="probe" onClick={() => tail.appendSynthetic(10_000)}>
          +10k synthetic
        </button>
      </div>

      {events.length === 0 ? (
        <div className="empty">
          {tail.freshness === "DISCONNECTED"
            ? "DISCONNECTED — no successful read yet"
            : "NO DATA — the session has no events yet (every op emits one)"}
        </div>
      ) : (
        <VirtualList
          total={events.length}
          rowHeight={ROW_HEIGHT}
          viewportHeight={VIEWPORT_HEIGHT}
          rowKey={(index) => events[index]!.event_id}
          renderRow={(index) => (
            <EventRow
              event={events[index]!}
              selected={events[index]!.event_id === selectedEventId}
              onSelect={() => {
                setSelectedEventId(events[index]!.event_id);
              }}
            />
          )}
          className="vlist"
          scrollCommand={scrollCommand}
        />
      )}

      <div className="inspector" aria-label="selected event">
        {selected === null ? (
          <p className="empty-inspector">no selection — click a row (selection is by event id, the semantic identity)</p>
        ) : (
          <pre data-testid="inspector-json">{JSON.stringify(selected, null, 2)}</pre>
        )}
      </div>
    </section>
  );
}

function EventRow(props: { readonly event: TailEvent; readonly selected: boolean; readonly onSelect: () => void }): ReactNode {
  const { event, selected, onSelect } = props;
  return (
    <div
      className={`trow${"synthetic" in event && event.synthetic ? " trow-synthetic" : ""}${selected ? " trow-selected" : ""}`}
      onClick={onSelect}
      data-event-id={event.event_id}
      data-sequence={String(event.sequence)}
      role="button"
      tabIndex={0}
      onKeyDown={(keyEvent) => {
        if (keyEvent.key === "Enter" || keyEvent.key === " ") {
          keyEvent.preventDefault();
          onSelect();
        }
      }}
    >
      <span className="cell-seq">{String(event.sequence)}</span>
      <span className="cell-type">{event.event_type}</span>
      <span className="cell-op">{"synthetic" in event && event.synthetic ? "SYNTHETIC" : short(event.operation_id, 18)}</span>
      <span className="cell-id" title={event.event_id}>
        {short(event.event_id, 16)}
      </span>
    </div>
  );
}

function short(value: string, max: number): string {
  if (value.length <= max) return value;
  return `${value.slice(0, Math.ceil(max / 2))}…${value.slice(-Math.floor(max / 2))}`;
}
