/**
 * The browser stream adapter's contract tests (iter-306, the
 * streaming admission's step 3+4 — FRONTEND_WEB_LAW §5):
 *
 * Layer 1 — the zod frame validators over the LIVE-CAPTURED wire
 * fixtures (captured off the real Gateway + transport through a real
 * socket at iteration time; the capture script asserted the D4 byte
 * parity against `session.events`' replay): every frame document
 * validates against its closed schema; the dual OPEN arms never
 * cross-validate; a foreign member is a CONTRACT MISMATCH, never a
 * pass-through.
 *
 * Layer 2 — the adapter's own laws (the FakeEventSource double; fake
 * timers for the backoff): ONE EventSource at a time; OWN
 * reconnection (the source is closed on every terminal/error — the
 * browser's auto-reconnect would re-request the ORIGINAL cursor and
 * duplicate the replay window; a semantic rejection would loop
 * forever); the bounded backoff ladder with the reset on OPEN; the
 * semantic rejection never auto-retried (G4's spirit); the
 * HTTP-level refusal and the contract mismatch both terminal; the
 * focused-tab gate (setActive) closes and re-dials; the RESYNC answer
 * hands the recovery to the consumer.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { FakeEventSource, frameData } from "../helpers/fakeEventSource.ts";
import { GatewayStream } from "../../src/api/gateway/stream.ts";
import type { StreamFrame, StreamPhase } from "../../src/api/gateway/stream.ts";
import {
  eventEnvelopeSchema,
  streamCloseDocumentSchema,
  streamOpenDocumentSchema,
  streamOverflowDocumentSchema,
  streamRejectedDocumentSchema,
} from "../../src/api/gateway/validators.ts";

const FIXTURES = join(dirname(fileURLToPath(import.meta.url)), "..", "fixtures");

function fixture(name: string): Record<string, unknown> {
  return JSON.parse(readFileSync(join(FIXTURES, `${name}.json`), "utf8")) as Record<string, unknown>;
}

interface Recorded {
  frames: StreamFrame[];
  phases: Array<{ phase: StreamPhase; note: string | null }>;
}

function record(): Recorded {
  return { frames: [], phases: [] };
}

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
  FakeEventSource.resetInstances();
});

// ------------------------------------------------------------ layer 1

describe("the zod frame validators over the live-captured wire fixtures", () => {
  it("the REPLAY open document validates (closed: mode/identity/bounds)", () => {
    const document = fixture("stream_open_replay");
    const parsed = streamOpenDocumentSchema.parse(document);
    expect(parsed.mode).toBe("REPLAY");
    expect(parsed.session_id).toBe(document["session_id"]);
    expect(parsed.last_sequence).toBe(document["last_sequence"]);
  });

  it("the RESYNC open document validates and carries the snapshot (the POST dual's own shape)", () => {
    const document = fixture("stream_open_resync");
    const parsed = streamOpenDocumentSchema.parse(document);
    if (parsed.mode !== "RESYNC") {
      expect.unreachable("the fixture is the RESYNC arm");
    }
    expect(parsed.resync).toBe("RESYNC_REQUIRED");
    expect(parsed.retained_from).toBe(document["retained_from"]);
    expect(parsed.snapshot.session_id).toBe(parsed.session_id);
  });

  it("the dual arms never cross-validate (a REPLAY carrying resync members is a mismatch; a RESYNC missing the snapshot is a mismatch)", () => {
    const replay = fixture("stream_open_replay");
    const resync = fixture("stream_open_resync");
    // A REPLAY-labeled document carrying the RESYNC members: the
    // REPLAY arm rejects the foreign keys, the RESYNC arm rejects the
    // mode literal — nowhere to validate.
    const replayWithResync = { ...resync, mode: "REPLAY" };
    expect(() => streamOpenDocumentSchema.parse(replayWithResync)).toThrow();
    const { snapshot: _snapshot, ...resyncWithoutSnapshot } = resync;
    expect(() => streamOpenDocumentSchema.parse(resyncWithoutSnapshot)).toThrow();
    void replay;
  });

  it("the event frame's data validates as the EventEnvelope (the D4 parity's consumer half)", () => {
    const envelope = fixture("stream_event_session_attached");
    const parsed = eventEnvelopeSchema.parse(envelope);
    expect(parsed.event_type).toBe("SESSION_ATTACHED");
    expect(parsed.sequence).toBe(envelope["sequence"]);
  });

  it("the rejected document validates over the closed §8 vocabulary; a foreign name is a mismatch", () => {
    const document = fixture("stream_rejected");
    expect(streamRejectedDocumentSchema.parse(document).rejection).toBe("DOMAIN_REJECTED");
    expect(() => streamRejectedDocumentSchema.parse({ ...document, rejection: "NOT_A_REJECTION" })).toThrow();
  });

  it("the overflow terminal document validates (strict)", () => {
    expect(streamOverflowDocumentSchema.parse(fixture("stream_overflow")).last_sequence).toBeGreaterThanOrEqual(0);
    expect(() => streamOverflowDocumentSchema.parse({ last_sequence: 1, extra: true })).toThrow();
  });

  it("the close terminal document validates over the closed reason vocabulary; a foreign reason is a mismatch", () => {
    const document = fixture("stream_close");
    expect(streamCloseDocumentSchema.parse(document).reason).toBe("SHUTDOWN");
    expect(() => streamCloseDocumentSchema.parse({ ...document, reason: "RESTARTED" })).toThrow();
  });

  it("the pre-stream 4xx guard bodies carry the closed guard vocabulary (transport-level, never the stream's frames)", () => {
    expect(fixture("stream_bad_params")["error"]).toBe("BAD_STREAM_PARAMS");
    expect(fixture("stream_auth_required")["error"]).toBe("STREAM_AUTH_REQUIRED");
  });
});

// ------------------------------------------------------------ layer 2

describe("the adapter: one dial, the right URL, the closed vocabulary", () => {
  beforeEach(() => {
    vi.stubGlobal("EventSource", FakeEventSource as unknown as typeof EventSource);
  });

  it("dials GET /events with the session and the explicit cursor (same-origin dev-proxy path)", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("session-abc", 7);
    expect(FakeEventSource.instances.length).toBe(1);
    expect(FakeEventSource.instances[0]!.url).toBe("/gateway/events?session_id=session-abc&since_sequence=7");
    adapter.stop();
  });

  it("registers exactly the closed vocabulary (4 control frames + 4 event types + error)", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    const source = FakeEventSource.instances[0]!;
    for (const name of ["stream.open", "stream.rejected", "stream.overflow", "stream.close"]) {
      expect(source.listenerCount(name)).toBe(1);
    }
    for (const name of ["SESSION_CREATED", "SESSION_ATTACHED", "SESSION_DETACHED", "OPERATION_EFFECT"]) {
      expect(source.listenerCount(name)).toBe(1);
    }
    expect(source.listenerCount("error")).toBe(1);
    adapter.stop();
  });
});

describe("the adapter: the frames flow, validated, with the cursor advancing", () => {
  beforeEach(() => {
    vi.stubGlobal("EventSource", FakeEventSource as unknown as typeof EventSource);
  });

  it("the REPLAY open + event frames reach the consumer validated; the phase goes OPEN", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    const source = FakeEventSource.instances[0]!;
    source.emit("stream.open", frameData(fixture("stream_open_replay")));
    const envelope = fixture("stream_event_session_attached");
    source.emit("SESSION_ATTACHED", frameData(envelope));
    expect(recorded.frames.map((f) => f.kind)).toEqual(["OPEN", "EVENT"]);
    if (recorded.frames[1]!.kind === "EVENT") {
      expect(recorded.frames[1]!.envelope.sequence).toBe(envelope["sequence"]);
    } else {
      expect.unreachable("the event frame arrived");
    }
    expect(recorded.phases.at(-1)!.phase).toBe("OPEN");
    adapter.stop();
  });

  it("the cursor-ahead reconciliation: a REPLAY open behind the cursor resets it (the server state wins)", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 99);
    const source = FakeEventSource.instances[0]!;
    // The honest empty replay: the server's last_sequence (3) < the cursor (99).
    source.emit("stream.open", frameData(fixture("stream_open_replay")));
    expect(recorded.phases.at(-1)!.phase).toBe("OPEN");
    expect(recorded.phases.at(-1)!.note).toContain("reconciled");
    adapter.stop();
  });
});

describe("the adapter: OWN reconnection (never the browser's)", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.stubGlobal("EventSource", FakeEventSource as unknown as typeof EventSource);
  });

  it("the overflow terminal: the frame emitted, the source closed, the reconnect from the LAST RECEIVED id after the backoff", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    const first = FakeEventSource.instances[0]!;
    first.emit("stream.open", frameData(fixture("stream_open_replay")));
    const envelope = fixture("stream_event_session_attached");
    first.emit("SESSION_ATTACHED", frameData(envelope));
    first.emit("stream.overflow", frameData(fixture("stream_overflow")));
    expect(first.closed).toBe(true);
    expect(FakeEventSource.instances.length).toBe(1); // no instant re-dial
    vi.advanceTimersByTime(500);
    expect(FakeEventSource.instances.length).toBe(2);
    // The reconnect cursor is the event frame's own sequence (2).
    expect(FakeEventSource.instances[1]!.url).toContain("since_sequence=2");
    adapter.stop();
  });

  it("the close terminal (SHUTDOWN): the frame emitted, the reconnect scheduled with backoff", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    const first = FakeEventSource.instances[0]!;
    first.emit("stream.open", frameData(fixture("stream_open_replay")));
    first.emit("stream.close", frameData(fixture("stream_close")));
    expect(first.closed).toBe(true);
    vi.advanceTimersByTime(500);
    expect(FakeEventSource.instances.length).toBe(2);
    adapter.stop();
  });

  it("a network error closes the source IMMEDIATELY (the browser's auto-reconnect would replay from the ORIGINAL cursor) and owns the retry", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 5);
    const first = FakeEventSource.instances[0]!;
    first.emitError(FakeEventSource.CONNECTING);
    expect(first.closed).toBe(true);
    expect(FakeEventSource.instances.length).toBe(1);
    vi.advanceTimersByTime(500);
    expect(FakeEventSource.instances.length).toBe(2);
    expect(FakeEventSource.instances[1]!.url).toContain("since_sequence=5");
    adapter.stop();
  });

  it("the backoff ladder: 500 -> 1000 -> 2000 -> 4000 -> 5000 (cap), reset on a successful OPEN", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    let dial = 0;
    const delays: number[] = [];
    let previous = 0;
    for (let i = 0; i < 5; i += 1) {
      const source = FakeEventSource.instances[FakeEventSource.instances.length - 1]!;
      source.emitError(FakeEventSource.CONNECTING);
      vi.advanceTimersByTime(500 * 2 ** i);
      dial = FakeEventSource.instances.length;
      delays.push(dial);
    }
    // Five errors -> five own re-dials, each after its own backoff.
    expect(FakeEventSource.instances.length).toBe(6);
    expect(delays).toEqual([2, 3, 4, 5, 6]);
    // A successful OPEN resets the ladder: the next error waits the base again.
    const open = FakeEventSource.instances[5]!;
    open.emit("stream.open", frameData(fixture("stream_open_replay")));
    open.emitError(FakeEventSource.CONNECTING);
    vi.advanceTimersByTime(499);
    expect(FakeEventSource.instances.length).toBe(6);
    vi.advanceTimersByTime(1);
    expect(FakeEventSource.instances.length).toBe(7);
    void previous;
    adapter.stop();
  });

  it("the HTTP-level refusal (readyState CLOSED): FAILED, terminal, no retry", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    const first = FakeEventSource.instances[0]!;
    first.emitError(FakeEventSource.CLOSED);
    expect(recorded.phases.at(-1)!.phase).toBe("FAILED");
    expect(recorded.phases.at(-1)!.note).toContain("HTTP level");
    vi.advanceTimersByTime(60_000);
    expect(FakeEventSource.instances.length).toBe(1); // never re-dialed
    adapter.stop();
  });
});

describe("the adapter: the semantic and contract terminals (never a blind retry)", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.stubGlobal("EventSource", FakeEventSource as unknown as typeof EventSource);
  });

  it("stream.rejected: the verdict surfaces verbatim, the stream ends, NOTHING retries (G4's spirit)", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("no-such-session", 0);
    const first = FakeEventSource.instances[0]!;
    first.emit("stream.rejected", frameData(fixture("stream_rejected")));
    const last = recorded.phases.at(-1)!;
    expect(last.phase).toBe("REJECTED");
    expect(last.note).toContain("DOMAIN_REJECTED");
    expect(first.closed).toBe(true);
    vi.advanceTimersByTime(60_000);
    expect(FakeEventSource.instances.length).toBe(1);
    // An explicit restart IS allowed (the caller's decision, never the adapter's).
    adapter.start("another-session", 0);
    expect(FakeEventSource.instances.length).toBe(2);
    adapter.stop();
  });

  it("a contract mismatch (a frame document deviating): FAILED with the detail, the stream closed, no retry", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    const first = FakeEventSource.instances[0]!;
    first.emit("stream.open", JSON.stringify({ mode: "REPLAY", session_id: "s", last_sequence: "not-a-number" }));
    expect(recorded.phases.at(-1)!.phase).toBe("FAILED");
    expect(recorded.phases.at(-1)!.note).toContain("contract mismatch");
    expect(first.closed).toBe(true);
    vi.advanceTimersByTime(60_000);
    expect(FakeEventSource.instances.length).toBe(1);
    adapter.stop();
  });

  it("the RESYNC answer: the document handed over, the source closed, the phase RESYNC (the consumer owns the recovery)", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    const first = FakeEventSource.instances[0]!;
    first.emit("stream.open", frameData(fixture("stream_open_resync")));
    expect(recorded.phases.at(-1)!.phase).toBe("RESYNC");
    expect(first.closed).toBe(true);
    vi.advanceTimersByTime(60_000);
    expect(FakeEventSource.instances.length).toBe(1); // no own retry — the consumer re-begins
    adapter.stop();
  });
});

describe("the adapter: the focused-tab gate (the admission step 4 primitive)", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.stubGlobal("EventSource", FakeEventSource as unknown as typeof EventSource);
  });

  it("setActive(false): the stream closes, the pending reconnect cancels, the phase PAUSES (a background tab holds NO connection)", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 3);
    const first = FakeEventSource.instances[0]!;
    first.emit("stream.open", frameData(fixture("stream_open_replay")));
    first.emitError(FakeEventSource.CONNECTING); // a reconnect is scheduled
    adapter.setActive(false);
    expect(first.closed).toBe(true);
    expect(recorded.phases.at(-1)!.phase).toBe("PAUSED");
    vi.advanceTimersByTime(60_000);
    expect(FakeEventSource.instances.length).toBe(1); // the timer was cancelled
    adapter.setActive(true);
    expect(FakeEventSource.instances.length).toBe(2); // the refocus re-dials...
    // ...from the cursor (the last event received / the start cursor).
    expect(FakeEventSource.instances[1]!.url).toContain("since_sequence=3");
    adapter.stop();
  });

  it("terminal phases stay put under the gate (an explicit start is the only way back)", () => {
    const recorded = record();
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    const first = FakeEventSource.instances[0]!;
    first.emit("stream.rejected", frameData(fixture("stream_rejected")));
    adapter.setActive(false);
    adapter.setActive(true);
    expect(FakeEventSource.instances.length).toBe(1);
    expect(recorded.phases.at(-1)!.phase).toBe("REJECTED");
    adapter.stop();
  });
});

describe("the adapter: the honest environment answer", () => {
  it("a runtime with no EventSource FAILS loudly (never a silent no-op)", () => {
    const recorded = record();
    vi.stubGlobal("EventSource", undefined);
    const adapter = new GatewayStream({}, { onFrame: (f) => recorded.frames.push(f), onPhase: (p, n) => recorded.phases.push({ phase: p, note: n }) });
    adapter.start("s", 0);
    expect(recorded.phases.at(-1)!.phase).toBe("FAILED");
    expect(recorded.phases.at(-1)!.note).toContain("no EventSource");
  });
});
