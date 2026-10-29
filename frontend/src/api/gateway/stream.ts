/**
 * The browser stream adapter — the streaming admission's step 3
 * (FRONTEND_WEB_LAW §5's order; iter-306): EventSource BEHIND the
 * typed gateway client seam, over the contract iter-305 landed
 * (GET /events, the closed frame vocabulary, the D4 byte parity —
 * the stream is a DELIVERY of the same ordered events
 * `session.events` replays by POST, never a second source).
 *
 * Laws carried here:
 * - S0-1's boundary law (the validators' own): every frame's `data`
 *   enters as `unknown` and passes the zod frame validators BEFORE
 *   any consumer sees it — raw JSON never reaches a surface; a wire
 *   deviation is a CONTRACT MISMATCH: surfaced (FAILED with the
 *   detail), the stream closed, never coerced, never retried blind.
 * - OWN reconnection, deliberately NOT the browser's: the wire
 *   contract's cursor law makes the browser's auto-reconnect WRONG
 *   twice — (a) it re-requests the SAME URL, so the ORIGINAL
 *   `since_sequence` parameter wins over Last-Event-ID and the replay
 *   window would be re-delivered as duplicates; (b) a semantic
 *   rejection (`stream.rejected` + server close) would reconnect into
 *   the same verdict forever. So the adapter closes the EventSource
 *   on EVERY terminal and error, and re-dials itself from ITS cursor
 *   with a bounded backoff — the reconnect is an explicit, observable
 *   act, never a hidden browser behavior.
 * - G4's spirit on the stream surface: a SEMANTIC verdict
 *   (`stream.rejected`) is never a blind retry — the stream stops,
 *   the verdict is surfaced verbatim, an explicit restart (the
 *   caller's decision) is the only way back.
 * - §13's dual answer: a REPLAY open means the retained window rides
 *   the event frames that follow (gapless into the live tail); a
 *   RESYNC open means the cursor fell out of retention — the adapter
 *   emits the document and CLOSES (the consumer owns the recovery:
 *   one POST `session.events` read from the retained window — the
 *   same law the POST adapter applies — then re-begins the stream
 *   with the reconciled cursor). The resync stream's live tail starts
 *   at `last_sequence + 1`; continuing it would leave the buffer
 *   gapped — closing is the honest move.
 * - The focused-tab gate (the admission step 4's primitive, §5.3's
 *   default): `setActive(false)` closes the stream and holds NO
 *   connection (one stream per focused tab, never N background
 *   streams exhausting the HTTP/1.1 budget); `setActive(true)`
 *   re-dials from the cursor. The REACT layer owns the policy's
 *   derivation (visibility + focus) — this adapter stays DOM-event
 *   free, pure transport policy, one instance per consuming hook.
 * - Boundedness: one EventSource at a time, one pending reconnect
 *   timer at a time, the backoff capped — no unbounded retry storm,
 *   no stream pool. `connection budget exhausted` never applies to
 *   this tab's own stream; a transport-level failure stays distinct
 *   from every semantic verdict (§5.2's first-class classes).
 *
 * The honest phase vocabulary (never collapsed):
 *   IDLE        — never started, or stopped by the consumer
 *   CONNECTING  — a dial is in flight (initial, reconnect, or resumed)
 *   OPEN        — stream.open accepted; frames flowing
 *   PAUSED      — the focused-tab policy holds no connection
 *   RESYNC      — the cursor fell out of retention; the consumer owns
 *                 the POST recovery + re-begin
 *   REJECTED    — the semantic verdict (no auto-reconnect, verbatim)
 *   FAILED      — a contract mismatch or an HTTP-level dial refusal
 *                 (no auto-reconnect; an explicit restart may clear it)
 */
import type { EventEnvelope } from "./contracts.ts";
import {
  EVENT_TYPES,
  STREAM_CONTROL_FRAMES,
} from "./contracts.ts";
import {
  eventEnvelopeSchema,
  streamCloseDocumentSchema,
  streamOpenDocumentSchema,
  streamOverflowDocumentSchema,
  streamRejectedDocumentSchema,
} from "./validators.ts";
import type {
  StreamCloseDocument,
  StreamOpenDocument,
  StreamOverflowDocument,
  StreamRejectedDocument,
} from "./contracts.ts";

/** The adapter's lifecycle phase — the honest state matrix. */
export type StreamPhase =
  | "IDLE"
  | "CONNECTING"
  | "OPEN"
  | "PAUSED"
  | "RESYNC"
  | "REJECTED"
  | "FAILED";

/** One validated frame, delivered to the consumer AFTER validation. */
export type StreamFrame =
  | { readonly kind: "OPEN"; readonly document: StreamOpenDocument }
  | { readonly kind: "EVENT"; readonly envelope: EventEnvelope }
  | { readonly kind: "REJECTED"; readonly document: StreamRejectedDocument }
  | { readonly kind: "OVERFLOW"; readonly document: StreamOverflowDocument }
  | { readonly kind: "CLOSE"; readonly document: StreamCloseDocument };

export interface GatewayStreamHandlers {
  /** One validated frame — the only data path out of the adapter. */
  onFrame(frame: StreamFrame): void;
  /** A phase transition with its honest note (rendered verbatim). */
  onPhase(phase: StreamPhase, note: string | null): void;
}

export interface GatewayStreamConfig {
  /** The stream route. Default: the same-origin dev-proxy path. */
  readonly url?: string;
  /** The first reconnect delay (ms). Default 500. */
  readonly reconnectBaseMs?: number;
  /** The reconnect delay ceiling (ms). Default 5_000. */
  readonly reconnectMaxMs?: number;
}

const DEFAULT_URL = "/gateway/events";
const DEFAULT_BASE_MS = 500;
const DEFAULT_MAX_MS = 5_000;

export class GatewayStream {
  private readonly url: string;
  private readonly baseMs: number;
  private readonly maxMs: number;
  private readonly handlers: GatewayStreamHandlers;

  private source: EventSource | null = null;
  private sessionId: string | null = null;
  private cursor = 0;
  private phase: StreamPhase = "IDLE";
  private phaseNote: string | null = null;
  private active = true;
  private nextBackoffMs = DEFAULT_BASE_MS;
  private reconnectTimer: ReturnType<typeof setTimeout> | undefined;

  constructor(config: GatewayStreamConfig, handlers: GatewayStreamHandlers) {
    this.url = config.url ?? DEFAULT_URL;
    this.baseMs = config.reconnectBaseMs ?? DEFAULT_BASE_MS;
    this.maxMs = config.reconnectMaxMs ?? DEFAULT_MAX_MS;
    this.nextBackoffMs = this.baseMs;
    this.handlers = handlers;
  }

  /**
   * Begin (or re-begin) the stream from an explicit cursor. A re-begin
   * tears down the current source first — an explicit restart is the
   * caller's decision (the RESYNC recovery, the user's retry after a
   * REJECTED/FAILED terminal), never the adapter's own blind retry.
   */
  start(sessionId: string, sinceSequence: number): void {
    if (typeof EventSource === "undefined") {
      // The honest environment answer — never a silent no-op.
      this.sessionId = sessionId;
      this.cursor = sinceSequence;
      this.fail("this runtime provides no EventSource (the stream adapter cannot dial)");
      return;
    }
    this.sessionId = sessionId;
    this.cursor = sinceSequence;
    this.nextBackoffMs = this.baseMs;
    this.teardownSource();
    this.dial();
  }

  /**
   * The focused-tab gate (the admission step 4 primitive): `false`
   * closes the stream and cancels any pending reconnect (a background
   * tab holds NO connection); `true` re-dials from the cursor. Terminal
   * phases (RESYNC/REJECTED/FAILED) stay put — an explicit `start` is
   * the only way back.
   */
  setActive(next: boolean): void {
    if (this.active === next) return;
    this.active = next;
    if (!next) {
      this.clearReconnectTimer();
      this.teardownSource();
      if (this.phase === "CONNECTING" || this.phase === "OPEN") {
        this.setPhase("PAUSED", "background tab — the stream is closed by the focused-tab policy; the last-known presentation is held");
      }
      return;
    }
    if (this.phase === "PAUSED" && this.sessionId !== null) {
      this.dial();
    }
  }

  /** The final teardown — no further frames, dials, or timers. */
  stop(): void {
    this.clearReconnectTimer();
    this.teardownSource();
    this.sessionId = null;
    this.setPhase("IDLE", null);
  }

  // ------------------------------------------------------------- internals

  private dial(): void {
    const sessionId = this.sessionId;
    if (sessionId === null) return;
    if (!this.active) {
      this.setPhase("PAUSED", "background tab — the stream is closed by the focused-tab policy; the last-known presentation is held");
      return;
    }
    this.setPhase("CONNECTING", `dialing GET /events (session ${short(sessionId, 8)}, since_sequence ${String(this.cursor)})`);
    const source = new EventSource(
      `${this.url}?session_id=${encodeURIComponent(sessionId)}&since_sequence=${String(this.cursor)}`,
    );
    this.source = source;
    // The closed vocabulary is registered member by member: the four
    // control frames + every EVENT_TYPES name. (A frame NAME outside
    // the closed set would dispatch to no listener — EventSource has
    // no wildcard; the vocabulary's closure is pinned by the contract
    // tests on both sides, and every frame DOCUMENT is validated.)
    for (const name of STREAM_CONTROL_FRAMES) {
      source.addEventListener(name, (event) => {
        this.onControlFrame(name, messageData(event));
      });
    }
    for (const name of EVENT_TYPES) {
      source.addEventListener(name, (event) => {
        this.onEventFrame(name, messageData(event));
      });
    }
    source.addEventListener("error", () => {
      this.onError(source);
    });
  }

  private onControlFrame(name: string, data: string): void {
    switch (name) {
      case "stream.open":
        this.onOpenFrame(data);
        return;
      case "stream.rejected":
        this.onRejectedFrame(data);
        return;
      case "stream.overflow":
        this.onOverflowFrame(data);
        return;
      case "stream.close":
        this.onCloseFrame(data);
        return;
      default:
        this.fail(`unknown control frame ${name}`);
    }
  }

  private onOpenFrame(data: string): void {
    const document = this.validate(streamOpenDocumentSchema, data, "stream.open");
    if (document === null) return;
    this.nextBackoffMs = this.baseMs;
    if (document.mode === "RESYNC") {
      // §13's dual answer, the out-of-retention arm: the snapshot IS
      // the answer — the adapter hands it over and closes; the
      // consumer recovers (one POST read over the retained window) and
      // re-begins with the reconciled cursor.
      this.handlers.onFrame({ kind: "OPEN", document });
      this.teardownSource();
      this.setPhase(
        "RESYNC",
        `RESYNC_REQUIRED — the cursor fell out of the retained tail (from seq ${String(document.retained_from)}); the consumer re-reads the retained window and re-begins the stream`,
      );
      return;
    }
    if (document.last_sequence < this.cursor) {
      // The consumer's cursor is AHEAD of the server's truth (an
      // inconsistent consumer — the open document's own observable).
      // The server state wins; the reconciled cursor rides the note.
      this.cursor = document.last_sequence;
      this.handlers.onFrame({ kind: "OPEN", document });
      this.setPhase("OPEN", `replay open — the cursor was ahead of the server (seq ${String(document.last_sequence)}); reconciled`);
      return;
    }
    this.handlers.onFrame({ kind: "OPEN", document });
    this.setPhase("OPEN", null);
  }

  private onEventFrame(name: string, data: string): void {
    const envelope = this.validate(eventEnvelopeSchema, data, `event frame ${name}`);
    if (envelope === null) return;
    // The envelope's own sequence is the truth (the D4 byte parity;
    // the wire `id` line is the browser's bookkeeping, never ours).
    this.cursor = envelope.sequence;
    this.handlers.onFrame({ kind: "EVENT", envelope });
  }

  private onRejectedFrame(data: string): void {
    const document = this.validate(streamRejectedDocumentSchema, data, "stream.rejected");
    if (document === null) return;
    // The semantic lane: ONE frame at HTTP 200, then the stream ends.
    // A semantic verdict is never a blind retry (G4's spirit) — the
    // stream stops here; an explicit restart is the caller's call.
    this.handlers.onFrame({ kind: "REJECTED", document });
    this.teardownSource();
    this.setPhase(
      "REJECTED",
      `stream.rejected (${document.rejection}): ${document.reason}`,
    );
  }

  private onOverflowFrame(data: string): void {
    const document = this.validate(streamOverflowDocumentSchema, data, "stream.overflow");
    if (document === null) return;
    // The bounded buffer's observable terminal: the queued events
    // drained first (the consumer GOT its data), then the channel
    // closed. The reconnect replays from OUR last received id — the
    // always-replay invariant (buffer <= retention) is the server's
    // construction law; the retry is safe by contract.
    this.handlers.onFrame({ kind: "OVERFLOW", document });
    this.teardownSource();
    this.scheduleReconnect(
      `stream overflow — the consumer fell behind; the queued events were delivered, the channel closed; reconnecting from seq ${String(this.cursor)}`,
    );
  }

  private onCloseFrame(data: string): void {
    const document = this.validate(streamCloseDocumentSchema, data, "stream.close");
    if (document === null) return;
    // The honest server-side terminal (e.g. the bounded shutdown). A
    // reconnect may hit a dead gateway (bounded backoff while active)
    // or a gone session (the REJECTED terminal ends the loop) — both
    // observable, never a silent spin.
    this.handlers.onFrame({ kind: "CLOSE", document });
    this.teardownSource();
    this.scheduleReconnect(
      `stream.close (${document.reason}) — the server ended the stream; reconnecting with backoff`,
    );
  }

  private onError(source: EventSource): void {
    if (this.source !== source) return; // a stale source's late error
    // EventSource exposes no status code; its state is the one signal:
    // CLOSED = the dial was refused at the HTTP level (a 4xx guard or
    // a wrong MIME type — permanent, the browser already gave up) —
    // surfaced as FAILED, no blind retry; anything else is a network
    // condition — the browser would auto-reconnect (wrongly: the SAME
    // URL, the ORIGINAL cursor), so we close it and own the retry.
    if (source.readyState === EventSource.CLOSED) {
      this.teardownSource();
      this.fail(
        "the stream dial was refused at the HTTP level (EventSource gives up; no status is exposed — the 4xx JSON body is observable in the devtools network pane)",
      );
      return;
    }
    this.teardownSource();
    this.scheduleReconnect(
      "stream transport error — the connection dropped; reconnecting from the last received sequence with backoff",
    );
  }

  private scheduleReconnect(reason: string): void {
    if (!this.active) {
      this.setPhase("PAUSED", "background tab — the stream is closed by the focused-tab policy; the last-known presentation is held");
      return;
    }
    const delay = this.nextBackoffMs;
    this.nextBackoffMs = Math.min(this.nextBackoffMs * 2, this.maxMs);
    this.setPhase("CONNECTING", `${reason} (backoff ${String(delay)} ms)`);
    this.clearReconnectTimer();
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = undefined;
      this.dial();
    }, delay);
  }

  private fail(detail: string): void {
    this.teardownSource();
    this.clearReconnectTimer();
    this.setPhase("FAILED", detail);
  }

  private validate<R>(
    schema: { parse(input: unknown): R },
    data: string,
    frame: string,
  ): R | null {
    let parsed: unknown;
    try {
      parsed = JSON.parse(data);
    } catch {
      this.fail(`contract mismatch — the ${frame} data is not JSON: ${short(data, 120)}`);
      return null;
    }
    try {
      return schema.parse(parsed);
    } catch (error) {
      this.fail(`contract mismatch — the ${frame} document deviates: ${short(error instanceof Error ? error.message : String(error), 200)}`);
      return null;
    }
  }

  private teardownSource(): void {
    const source = this.source;
    this.source = null;
    if (source !== null) {
      // Closing before the handlers run guarantees no late frame from
      // a torn-down source (the listeners die with the source).
      source.close();
    }
  }

  private clearReconnectTimer(): void {
    if (this.reconnectTimer !== undefined) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = undefined;
    }
  }

  private setPhase(phase: StreamPhase, note: string | null): void {
    if (this.phase === phase && this.phaseNote === note) return;
    this.phase = phase;
    this.phaseNote = note;
    this.handlers.onPhase(phase, note);
  }
}

/** The frame's data string (the DOM listener types the payload as a
 * bare Event; the SSE data field is the string the server wrote). */
function messageData(event: Event): string {
  return (event as MessageEvent<string>).data;
}

function short(value: string, max: number): string {
  if (value.length <= max) return value;
  return `${value.slice(0, Math.ceil(max / 2))}…${value.slice(-Math.floor(max / 2))}`;
}
