/**
 * useLiveTail — the ordered LIVE session tail (S0-2) over the session's
 * event stream, with TWO transports behind the SAME cursor/buffer
 * discipline (iter-306, the admission step 3+4):
 *
 * - "stream" — the browser stream adapter (GET /events SSE behind the
 *   typed client seam): every frame runtime-validated, the reconnection
 *   owned and bounded (backoff), the FOCUSED-TAB policy enforced (only
 *   a visible+focused tab holds a connection; a background tab holds
 *   NONE — §5.3's default, one stream per tab, never a budget storm);
 * - "poll" — POST-only `session.events` polling (S0's mandate, always
 *   valid, the fallback that needs no stream).
 *
 * The adapter OWNS the cursor discipline both transports share:
 * - the cursor is the SEMANTIC sequence (never a row index);
 * - RESYNC_REQUIRED is handled HERE (§4's transport-adapter law):
 *   the verdict is surfaced honestly and the tail re-reads from
 *   the server's retained window (FIFO eviction is not canon loss) —
 *   the stream lane performs the SAME one-POST recovery the poll lane
 *   applies, then re-begins the stream from the reconciled cursor;
 * - the tab-hidden policy: a hidden tab PAUSES polling / closes the
 *   stream and shows STALE (the focused-tab discipline);
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

import type { EventEnvelope, SessionEventsResult, StreamOpenDocument } from "../../api/gateway/contracts.ts";
import type { GatewayClient } from "../../api/gateway/client.ts";
import { GatewayStream } from "../../api/gateway/stream.ts";
import type { StreamFrame, StreamPhase } from "../../api/gateway/stream.ts";
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
  /** The stream adapter's phase (stream mode only; null in poll mode). */
  readonly streamPhase: StreamPhase | null;
}

/** The tail's transport (iter-306): the SSE stream (the admission
 * step 3+4 form) or POST-only polling (S0's mandate, always valid). */
export type LiveTailTransport = "stream" | "poll";

export interface LiveTailOptions {
  readonly client: GatewayClient;
  readonly sessionId: string | null;
  /** The poll interval (ms) — the POLL transport only; `0` disables. */
  readonly intervalMs: number;
  /** The transport. Default "stream" (the step 3+4 landing). */
  readonly transport?: LiveTailTransport;
}

export function useLiveTail(options: LiveTailOptions): LiveTailState & {
  readonly refreshNow: () => Promise<void>;
  readonly appendSynthetic: (count: number) => void;
  readonly clearSynthetic: () => void;
} {
  const { client, sessionId, intervalMs } = options;
  const transport: LiveTailTransport = options.transport ?? "stream";
  const [buffer, dispatch] = useReducer(tailReducer, EMPTY_BUFFER);
  const [lastSequence, setLastSequence] = useState(0);
  const [resync, setResync] = useState<ResyncNotice | null>(null);
  const [freshness, setFreshness] = useState<Freshness>("DISCONNECTED");
  const [lastReadAt, setLastReadAt] = useState<number | null>(null);
  const [transportNote, setTransportNote] = useState<string | null>(null);
  const [streamPhase, setStreamPhase] = useState<StreamPhase | null>(null);
  const cursorRef = useRef(0);
  const sessionRef = useRef<string | null>(null);
  const streamRef = useRef<GatewayStream | null>(null);
  /** Whether ANY successful read/frame ever landed for the current
   * session — the first dial is DISCONNECTED, a reconnect with held
   * data is STALE (the honest freshness split). */
  const everLiveRef = useRef(false);

  // A session switch resets the whole tail — a new session is a new
  // evidence world (the cursor never leaks across sessions).
  useEffect(() => {
    if (sessionRef.current === sessionId) return;
    sessionRef.current = sessionId;
    cursorRef.current = 0;
    everLiveRef.current = false;
    dispatch({ type: "RESET" });
    setLastSequence(0);
    setResync(null);
    setFreshness("DISCONNECTED");
    setTransportNote(null);
  }, [sessionId]);

  // ------------------------------------------------------------ the poll

  const poll = useCallback(async () => {
    if (sessionId === null) return;
    const result = await client.sessionEvents({
      sessionId,
      sinceSequence: cursorRef.current,
    });
    const now = Date.now();
    if (result.transport === "DELIVERED" && result.status === "OK") {
      everLiveRef.current = true;
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
    // An explicit refresh: the POST read (always valid — S0's mandate
    // is the stream's fallback too; the poll lane advances the SAME
    // cursor the stream lane shares).
    await poll();
  }, [poll]);

  // The poll loop (the POLL transport only): paused when the tab is
  // hidden (focused-tab discipline for the POST world) or when the
  // interval is 0.
  useEffect(() => {
    if (transport !== "poll" || sessionId === null || intervalMs <= 0) return;
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
  }, [transport, poll, sessionId, intervalMs]);

  // ----------------------------------------------------------- the stream

  /** The stream lane's shared exit: apply one REPLAY answer (the poll
   * read's or the recovery read's) to the buffer + cursor. */
  const applyReplay = useCallback((payload: Extract<SessionEventsResult, { kind: "REPLAY" }>) => {
    dispatch({ type: "APPEND", events: payload.events });
    cursorRef.current = payload.last_sequence;
    setLastSequence(payload.last_sequence);
  }, []);

  /** §13's out-of-retention arm over the stream: the SAME one-POST
   * recovery the poll lane applies (the retained window re-reads by
   * POST — the resync stream's live tail starts at last_sequence + 1,
   * so continuing it would leave the buffer gapped), then the stream
   * re-begins from the reconciled cursor. */
  const recoverFromResync = useCallback(async (sessionIdNow: string, document: Extract<StreamOpenDocument, { mode: "RESYNC" }>) => {
    const result = await client.sessionEvents({
      sessionId: sessionIdNow,
      sinceSequence: Math.max(0, document.retained_from - 1),
    });
    if (sessionRef.current !== sessionIdNow) return; // the world moved on
    const now = Date.now();
    if (result.transport === "DELIVERED" && result.status === "OK" && result.result.kind === "REPLAY") {
      everLiveRef.current = true;
      applyReplay(result.result);
      setResync({
        at: now,
        retainedFrom: document.retained_from,
        lastSequence: document.last_sequence,
      });
      setFreshness("LIVE");
      setLastReadAt(now);
      setTransportNote(null);
      const stream = streamRef.current;
      if (stream !== null) {
        stream.start(sessionIdNow, result.result.last_sequence);
      }
      return;
    }
    // The recovery read itself failed honestly — the stream lane stays
    // parked in RESYNC (the phase's own note rides transportNote).
    if (result.transport === "DELIVERED") {
      setFreshness("STALE");
      setTransportNote(
        `session.events (resync recovery): ${result.status}${result.response.rejection === undefined ? "" : ` (${result.response.rejection})`}`,
      );
    } else if (result.transport === "TRANSPORT") {
      setFreshness("DISCONNECTED");
      setTransportNote(`${result.failure.kind}: ${result.failure.detail}`);
    } else {
      setFreshness("DISCONNECTED");
      setTransportNote(`contract mismatch: ${result.error}`);
    }
  }, [client, applyReplay]);

  /** The stream frame handler — every frame arrives VALIDATED (the
   * adapter's law); the buffer/cursor discipline is this lane's own. */
  const onStreamFrame = useCallback((frame: StreamFrame) => {
    const sessionIdNow = sessionRef.current;
    if (sessionIdNow === null) return;
    switch (frame.kind) {
      case "OPEN": {
        if (frame.document.mode === "RESYNC") {
          void recoverFromResync(sessionIdNow, frame.document);
          return;
        }
        // The consumer's cursor ahead of the server's truth: the same
        // reconciliation the adapter applied to ITS cursor.
        if (frame.document.last_sequence < cursorRef.current) {
          cursorRef.current = frame.document.last_sequence;
        }
        everLiveRef.current = true;
        setFreshness("LIVE");
        setLastReadAt(Date.now());
        setTransportNote(null);
        return;
      }
      case "EVENT": {
        dispatch({ type: "APPEND", events: [frame.envelope] });
        cursorRef.current = frame.envelope.sequence;
        setLastSequence(frame.envelope.sequence);
        everLiveRef.current = true;
        setFreshness("LIVE");
        setLastReadAt(Date.now());
        setTransportNote(null);
        return;
      }
      // The control terminals' details ride the PHASE notes (below);
      // the frames are the honest events for anyone who needs them.
      case "REJECTED":
      case "OVERFLOW":
      case "CLOSE":
        return;
    }
  }, [recoverFromResync]);

  const onStreamPhase = useCallback((phase: StreamPhase, note: string | null) => {
    setStreamPhase(phase);
    switch (phase) {
      case "OPEN":
        setFreshness("LIVE");
        setTransportNote(note);
        return;
      case "CONNECTING":
        // The first dial stays DISCONNECTED; a reconnect with held
        // data degrades to STALE (the last-known presentation held).
        if (!everLiveRef.current) setFreshness("DISCONNECTED");
        else setFreshness((previous) => (previous === "LIVE" ? "STALE" : previous));
        setTransportNote(note);
        return;
      case "PAUSED":
        setFreshness("STALE");
        setTransportNote(note);
        return;
      case "RESYNC":
        setFreshness("STALE");
        setTransportNote(note);
        return;
      case "REJECTED":
        setFreshness("STALE");
        setTransportNote(note);
        return;
      case "FAILED":
        setFreshness("DISCONNECTED");
        setTransportNote(note);
        return;
      case "IDLE":
        setTransportNote(note);
        return;
    }
  }, []);

  // The stream lifecycle (the STREAM transport only): one adapter per
  // hook (one stream per tab — the budget law), the FOCUSED-TAB gate
  // (§5.3: only a visible+focused tab holds a connection; background
  // tabs hold NONE), and the honest teardown.
  useEffect(() => {
    if (transport !== "stream") {
      setStreamPhase(null);
      return;
    }
    const stream =
      streamRef.current ??
      new GatewayStream(
        {},
        { onFrame: onStreamFrame, onPhase: onStreamPhase },
      );
    streamRef.current = stream;
    if (sessionId === null) {
      stream.stop();
      setStreamPhase("IDLE");
      return;
    }
    stream.start(sessionId, cursorRef.current);
    // The focused-tab policy: visible AND focused — a background tab
    // (hidden, or visible-but-blurred behind another window) holds no
    // stream; the degradation is coarse but truthful (STALE + note).
    const derive = () => {
      stream.setActive(document.visibilityState === "visible" && document.hasFocus());
    };
    derive();
    document.addEventListener("visibilitychange", derive);
    window.addEventListener("focus", derive);
    window.addEventListener("blur", derive);
    return () => {
      document.removeEventListener("visibilitychange", derive);
      window.removeEventListener("focus", derive);
      window.removeEventListener("blur", derive);
      stream.stop();
    };
  }, [transport, sessionId, onStreamFrame, onStreamPhase]);

  // A transport switch to "poll" parks the stream honestly (the
  // effect above already stopped it); switching back re-begins from
  // the SHARED cursor — the buffer survives the switch, the tail is
  // one evidence world over two transports.

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
      polling: transport === "poll" && intervalMs > 0,
      streamPhase: transport === "stream" ? streamPhase : null,
      refreshNow,
      appendSynthetic,
      clearSynthetic,
    }),
    [buffer, lastSequence, resync, freshness, lastReadAt, transportNote, transport, intervalMs, streamPhase, refreshNow, appendSynthetic, clearSynthetic],
  );
}
