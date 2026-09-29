/**
 * useLiveTail — the ordered LIVE session tail over `session.events`
 * (S0-2). POST-only polling (no SSE/WebSocket in S0); the adapter
 * OWNS the cursor discipline the browser-runtime law demands:
 *
 * - the cursor is the SEMANTIC sequence (never a row index);
 * - RESYNC_REQUIRED is handled HERE (§4's transport-adapter law):
 *   the verdict is surfaced honestly and the tail re-reads from
 *   the server's retained window (FIFO eviction is not canon loss);
 * - the tab-hidden policy: a hidden tab PAUSES polling and shows
 *   STALE (the focused-tab discipline applied to the POST world —
 *   no background polling storms);
 * - the buffer is BOUNDED (`MAX_TAIL_EVENTS`): the live tail is a
 *   presentation window, never a client-side log (dual-read law —
 *   durable history is the Observatory's, never this buffer).
 *
 * The buffer itself is a PURE reducer (StrictMode-safe: no ref
 * mutation inside updaters, no double-minted synthetic rows).
 * Synthetic load-test rows are APPEND-ONLY presentation evidence,
 * flagged `synthetic` at the row and in a standing banner — never
 * presented as gateway truth.
 */
import { useCallback, useEffect, useMemo, useReducer, useRef, useState } from "react";

import type { EventEnvelope } from "../../api/gateway/contracts.ts";
import type { GatewayClient } from "../../api/gateway/client.ts";
import type { Freshness } from "../../state/session/useTabSession.ts";

/** The presentation buffer's hard ceiling (the boundedness law). */
export const MAX_TAIL_EVENTS = 50_000;

export interface SyntheticEvent extends EventEnvelope {
  readonly synthetic: true;
}

export type TailEvent = EventEnvelope | SyntheticEvent;

export interface ResyncNotice {
  readonly at: number;
  readonly retainedFrom: number;
  readonly lastSequence: number;
}

interface TailBuffer {
  readonly events: readonly TailEvent[];
  readonly trimmedCount: number;
  readonly syntheticCount: number;
  /** The highest sequence number ever minted into this buffer. */
  readonly highSequence: number;
  /** The synthetic event_id serial (monotonic across the tab's life). */
  readonly syntheticSerial: number;
}

type TailAction =
  | { readonly type: "APPEND"; readonly events: readonly EventEnvelope[] }
  | { readonly type: "SYNTHETIC"; readonly count: number; readonly sessionId: string; readonly at: number }
  | { readonly type: "CLEAR_SYNTHETIC" }
  | { readonly type: "RESET" };

const EMPTY_BUFFER: TailBuffer = {
  events: [],
  trimmedCount: 0,
  syntheticCount: 0,
  highSequence: 0,
  syntheticSerial: 0,
};

function tailReducer(state: TailBuffer, action: TailAction): TailBuffer {
  switch (action.type) {
    case "RESET":
      return EMPTY_BUFFER;
    case "CLEAR_SYNTHETIC":
      return { ...state, events: state.events.filter((e) => !("synthetic" in e && e.synthetic)), syntheticCount: 0 };
    case "APPEND": {
      if (action.events.length === 0) return state;
      const merged = [...state.events, ...action.events] as TailEvent[];
      const high = action.events.reduce(
        (max, e) => (e.sequence > max ? e.sequence : max),
        state.highSequence,
      );
      if (merged.length > MAX_TAIL_EVENTS) {
        const trimmed = merged.length - MAX_TAIL_EVENTS;
        return {
          events: merged.slice(trimmed),
          trimmedCount: state.trimmedCount + trimmed,
          syntheticCount: state.syntheticCount,
          highSequence: high,
          syntheticSerial: state.syntheticSerial,
        };
      }
      return { ...state, events: merged, highSequence: high };
    }
    case "SYNTHETIC": {
      const next: SyntheticEvent[] = [];
      for (let i = 0; i < action.count; i += 1) {
        const serial = state.syntheticSerial + 1 + i;
        next.push({
          synthetic: true,
          event_id: `synthetic-${String(serial).padStart(6, "0")}`,
          session_id: action.sessionId,
          operation_id: "synthetic.load-test",
          sequence: state.highSequence + 1 + i,
          event_type: "OPERATION_EFFECT",
          observed_at: action.at,
          payload: {
            synthetic: true,
            note: "presentation-only load-test row — not gateway truth",
          },
        });
      }
      const merged = [...state.events, ...next] as TailEvent[];
      const trimmed = Math.max(0, merged.length - MAX_TAIL_EVENTS);
      return {
        events: trimmed > 0 ? merged.slice(trimmed) : merged,
        trimmedCount: state.trimmedCount + trimmed,
        syntheticCount: state.syntheticCount + action.count,
        highSequence: state.highSequence + action.count,
        syntheticSerial: state.syntheticSerial + action.count,
      };
    }
  }
}

export interface LiveTailState {
  readonly events: readonly TailEvent[];
  readonly lastSequence: number;
  readonly resync: ResyncNotice | null;
  readonly syntheticCount: number;
  readonly trimmedCount: number;
  readonly freshness: Freshness;
  readonly lastReadAt: number | null;
  readonly transportNote: string | null;
  readonly polling: boolean;
}

export interface LiveTailOptions {
  readonly client: GatewayClient;
  readonly sessionId: string | null;
  /** The poll interval (ms). `0` disables automatic polling. */
  readonly intervalMs: number;
}

export function useLiveTail(options: LiveTailOptions): LiveTailState & {
  readonly refreshNow: () => Promise<void>;
  readonly appendSynthetic: (count: number) => void;
  readonly clearSynthetic: () => void;
} {
  const { client, sessionId, intervalMs } = options;
  const [buffer, dispatch] = useReducer(tailReducer, EMPTY_BUFFER);
  const [lastSequence, setLastSequence] = useState(0);
  const [resync, setResync] = useState<ResyncNotice | null>(null);
  const [freshness, setFreshness] = useState<Freshness>("DISCONNECTED");
  const [lastReadAt, setLastReadAt] = useState<number | null>(null);
  const [transportNote, setTransportNote] = useState<string | null>(null);
  const cursorRef = useRef(0);
  const sessionRef = useRef<string | null>(null);

  // A session switch resets the whole tail — a new session is a new
  // evidence world (the cursor never leaks across sessions).
  useEffect(() => {
    if (sessionRef.current === sessionId) return;
    sessionRef.current = sessionId;
    cursorRef.current = 0;
    dispatch({ type: "RESET" });
    setLastSequence(0);
    setResync(null);
    setFreshness("DISCONNECTED");
    setTransportNote(null);
  }, [sessionId]);

  const poll = useCallback(async () => {
    if (sessionId === null) return;
    const result = await client.sessionEvents({
      sessionId,
      sinceSequence: cursorRef.current,
    });
    const now = Date.now();
    if (result.transport === "DELIVERED" && result.status === "OK") {
      const payload = result.result;
      if (payload.kind === "REPLAY") {
        dispatch({ type: "APPEND", events: payload.events });
        cursorRef.current = payload.last_sequence;
        setLastSequence(payload.last_sequence);
      } else {
        // RESYNC_REQUIRED: the cursor fell out of the retained tail.
        // The honest recovery: re-read from the server's window start.
        setResync({
          at: now,
          retainedFrom: payload.retained_from,
          lastSequence: payload.last_sequence,
        });
        cursorRef.current = Math.max(0, payload.retained_from - 1);
        setLastSequence(payload.last_sequence);
      }
      setFreshness("LIVE");
      setLastReadAt(now);
      setTransportNote(null);
    } else if (result.transport === "DELIVERED") {
      // A delivered semantic rejection (e.g. the session vanished):
      // an honest observation, rendered as STALE with its reason.
      setFreshness("STALE");
      setLastReadAt(now);
      setTransportNote(
        `session.events: ${result.status}${result.response.rejection === undefined ? "" : ` (${result.response.rejection})`}`,
      );
    } else if (result.transport === "TRANSPORT") {
      setFreshness("DISCONNECTED");
      setTransportNote(`${result.failure.kind}: ${result.failure.detail}`);
    } else {
      setFreshness("DISCONNECTED");
      setTransportNote(`contract mismatch: ${result.error}`);
    }
  }, [client, sessionId]);

  const refreshNow = useCallback(async () => {
    await poll();
  }, [poll]);

  // The poll loop: paused when the tab is hidden (focused-tab
  // discipline for the POST world) or when the interval is 0.
  useEffect(() => {
    if (sessionId === null || intervalMs <= 0) return;
    let active = true;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const tick = () => {
      if (!active) return;
      if (document.visibilityState === "visible") {
        void poll().finally(() => {
          if (active) timer = setTimeout(tick, intervalMs);
        });
      } else {
        // Hidden: mark STALE, keep the schedule light.
        setFreshness((previous) => (previous === "LIVE" ? "STALE" : previous));
        timer = setTimeout(tick, Math.max(intervalMs, 5000));
      }
    };
    timer = setTimeout(tick, 250);
    const onVisibility = () => {
      if (document.visibilityState === "visible") {
        void poll();
      }
    };
    document.addEventListener("visibilitychange", onVisibility);
    return () => {
      active = false;
      if (timer !== undefined) clearTimeout(timer);
      document.removeEventListener("visibilitychange", onVisibility);
    };
  }, [poll, sessionId, intervalMs]);

  const appendSynthetic = useCallback(
    (count: number) => {
      dispatch({
        type: "SYNTHETIC",
        count,
        sessionId: sessionId ?? "unknown-session",
        at: Date.now() / 1000,
      });
    },
    [sessionId],
  );

  const clearSynthetic = useCallback(() => {
    dispatch({ type: "CLEAR_SYNTHETIC" });
  }, []);

  return useMemo(
    () => ({
      events: buffer.events,
      lastSequence,
      resync,
      syntheticCount: buffer.syntheticCount,
      trimmedCount: buffer.trimmedCount,
      freshness,
      lastReadAt,
      transportNote,
      polling: intervalMs > 0,
      refreshNow,
      appendSynthetic,
      clearSynthetic,
    }),
    [buffer, lastSequence, resync, freshness, lastReadAt, transportNote, intervalMs, refreshNow, appendSynthetic, clearSynthetic],
  );
}
