/**
 * The S0-2 + iter-306 integration proof, in the browser-less band
 * (jsdom + testing-library; the live-browser evidence rides the
 * iteration report): a ≥10_000-row tail renders with ONLY the window
 * mounted (never the full tree); the cursor is the semantic sequence;
 * the selection is the event_id; the LIVE label and the dual-read note
 * stand; the RESYNC banner shows the honest verdict — over BOTH
 * transports: the POST poll lane (S0's mandate) and the SSE stream
 * lane (the admission step 3+4 — the FakeEventSource double drives the
 * frames, the focused-tab policy, the overflow reconnect, and the
 * resync POST-recovery exactly as the adapter dispatches them).
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import { GatewayClient } from "../../src/api/gateway/client.ts";
import { Trajectory } from "../../src/features/trajectory/Trajectory.tsx";
import { FakeEventSource, frameData } from "../helpers/fakeEventSource.ts";

const FIXTURES = join(dirname(fileURLToPath(import.meta.url)), "..", "fixtures");

function fixture(name: string): Record<string, unknown> {
  return JSON.parse(readFileSync(join(FIXTURES, `${name}.json`), "utf8")) as Record<string, unknown>;
}

/** A deterministic event for the mocked replay window. */
function syntheticGatewayEvent(sequence: number): Record<string, unknown> {
  return {
    event_id: `evt-${String(sequence).padStart(5, "0")}`,
    session_id: "test-session",
    operation_id: `op-${String(sequence).padStart(5, "0")}`,
    sequence,
    event_type: sequence % 2 === 0 ? "SESSION_ATTACHED" : "OPERATION_EFFECT",
    observed_at: 1_000_000 + sequence,
    payload: { note: "gateway truth (mocked wire)" },
  };
}

function replayResponse(count: number): Record<string, unknown> {
  return {
    status: "OK",
    operation_id: "op-response",
    result: {
      events: Array.from({ length: count }, (_, i) => syntheticGatewayEvent(i + 1)),
      last_sequence: count,
    },
  };
}

function json(document: unknown): Response {
  return new Response(JSON.stringify(document), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  FakeEventSource.resetInstances();
});

/** The POST-lane mount: the feed select switched to the 2s poll (the
 * original S0 posture — the stream lane has its own mounts below). */
function mountTrajectory(fetchImpl: typeof fetch): void {
  vi.stubGlobal("fetch", fetchImpl);
  const client = new GatewayClient();
  render(<Trajectory client={client} sessionId="test-session" />);
  fireEvent.change(screen.getByLabelText("feed transport"), { target: { value: "2000" } });
}

/** The STREAM-lane mount: the FakeEventSource double carries the wire.
 * jsdom's defaults (visibilityState "prerender", hasFocus false) would
 * honestly PAUSE the stream — the focused-tab policy firing on an
 * unfocused test world. The stream-lane rows run as a VISIBLE+FOCUSED
 * tab; the policy's own row flips the focus spy. */
function mountTrajectoryStream(fetchImpl: typeof fetch): FakeEventSource {
  vi.stubGlobal("fetch", fetchImpl);
  vi.stubGlobal("EventSource", FakeEventSource as unknown as typeof EventSource);
  FakeEventSource.resetInstances();
  Object.defineProperty(document, "visibilityState", {
    value: "visible",
    configurable: true,
  });
  vi.spyOn(document, "hasFocus").mockReturnValue(true);
  const client = new GatewayClient();
  render(<Trajectory client={client} sessionId="test-session" />);
  return FakeEventSource.instances[0]!;
}

describe("the Trajectory surface (S0-2)", () => {
  it("labels itself a LIVE session tail — never durable history", async () => {
    mountTrajectory(vi.fn().mockResolvedValue(json(replayResponse(3))));
    expect(screen.getByText(/LIVE SESSION TAIL/i)).toBeTruthy();
    expect(screen.getByText(/not durable history/i)).toBeTruthy();
    await waitFor(() => {
      expect(screen.getByRole("list")).toBeTruthy();
    });
  });

  it("renders the gateway's events after a refresh (the round-trip path)", async () => {
    mountTrajectory(vi.fn().mockResolvedValue(json(replayResponse(5))));
    fireEvent.click(screen.getByRole("button", { name: "refresh now" }));
    await waitFor(() => {
      expect(screen.getAllByRole("listitem").length).toBeGreaterThanOrEqual(5);
    });
    expect(screen.queryByText(/NO DATA/)).toBeNull();
  });

  it("10_000+ rows: only the window mounts, aria-rowcount carries the truth", async () => {
    mountTrajectory(vi.fn().mockResolvedValue(json(replayResponse(5))));
    fireEvent.click(screen.getByRole("button", { name: "refresh now" }));
    await waitFor(() => {
      expect(screen.getAllByRole("listitem").length).toBeGreaterThanOrEqual(5);
    });
    fireEvent.click(screen.getByRole("button", { name: "+10k synthetic" }));
    const list = screen.getByRole("list");
    // 5 gateway + 10_000 synthetic rows exist; only the window mounts.
    await waitFor(() => {
      expect(list.getAttribute("aria-rowcount")).toBe("10005");
    });
    const mounted = screen.getAllByRole("listitem").length;
    expect(mounted).toBeGreaterThan(0);
    expect(mounted).toBeLessThanOrEqual(15 + 12 + 5); // viewport + overscan
    // The synthetic banner stands (honest presentation-only marking).
    expect(screen.getByText(/synthetic load-test rows/i)).toBeTruthy();
  });

  it("selects by the SEMANTIC event id, not the row index", async () => {
    mountTrajectory(vi.fn().mockResolvedValue(json(replayResponse(5))));
    fireEvent.click(screen.getByRole("button", { name: "refresh now" }));
    const thirdRow = await waitFor(() => {
      const rows = screen.getAllByRole("listitem");
      expect(rows.length).toBeGreaterThanOrEqual(5);
      return rows[2]!;
    });
    // The interactive element is the row itself (role=button inside).
    fireEvent.click(within(thirdRow).getByRole("button"));
    const inspector = await screen.findByTestId("inspector-json");
    const parsed = JSON.parse(inspector.textContent ?? "{}") as { event_id?: string };
    expect(parsed.event_id).toBe("evt-00003");
  });

  it("jumps by the semantic sequence (the cursor is the sequence)", async () => {
    mountTrajectory(vi.fn().mockResolvedValue(json(replayResponse(5))));
    fireEvent.click(screen.getByRole("button", { name: "refresh now" }));
    await waitFor(() => {
      expect(screen.getAllByRole("listitem").length).toBeGreaterThanOrEqual(5);
    });
    fireEvent.click(screen.getByRole("button", { name: "+10k synthetic" }));
    await waitFor(() => {
      expect(screen.getByRole("list").getAttribute("aria-rowcount")).toBe("10005");
    });
    // Jump to the last synthetic sequence: 5 gateway + 10000 synthetic.
    const input = screen.getByPlaceholderText("jump to seq…") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "10005" } });
    fireEvent.submit(input.form!);
    await waitFor(() => {
      const rows = screen.getAllByRole("listitem");
      const sequences = rows.map(
        (row) => Number(within(row).getByRole("button").getAttribute("data-sequence")),
      );
      expect(sequences).toContain(10005);
    });
    // The selection rode the jump (the row was selected by its id).
    const inspector = await screen.findByTestId("inspector-json");
    expect(inspector.textContent).toContain("synthetic");
  });

  it("renders the RESYNC_REQUIRED verdict honestly", async () => {
    let calls = 0;
    const resyncFixture = fixture("session_events_resync_required");
    const fetchImpl = vi.fn().mockImplementation(() => {
      calls += 1;
      // First read: RESYNC; then the retained window (sequences 8..11).
      if (calls === 1) {
        return Promise.resolve(json(resyncFixture));
      }
      return Promise.resolve(
        json({
          status: "OK",
          operation_id: "op-response",
          result: {
            events: [8, 9, 10, 11].map((sequence) => syntheticGatewayEvent(sequence)),
            last_sequence: 11,
          },
        }),
      );
    });
    mountTrajectory(fetchImpl);
    fireEvent.click(screen.getByRole("button", { name: "refresh now" }));
    await waitFor(() => {
      expect(screen.getByText(/RESYNC_REQUIRED/i)).toBeTruthy();
    });
    // The adapter re-reads from the retained window (the poll that
    // follows the verdict), and the retained rows mount.
    fireEvent.click(screen.getByRole("button", { name: "refresh now" }));
    await waitFor(() => {
      const rows = screen.getAllByRole("listitem");
      expect(rows.length).toBeGreaterThanOrEqual(4);
    });
  });

  it("shows DISCONNECTED honestly when the gateway is down (never 'rejected')", async () => {
    mountTrajectory(vi.fn().mockRejectedValue(new TypeError("fetch failed")));
    fireEvent.click(screen.getByRole("button", { name: "refresh now" }));
    await waitFor(() => {
      expect(screen.getByRole("alert")).toBeTruthy();
    });
    expect(screen.getByRole("alert").textContent).toContain("UNREACHABLE");
    expect(screen.getByText(/DISCONNECTED — no successful read yet/i)).toBeTruthy();
  });
});

describe("the Trajectory surface — the STREAM lane (iter-306, the admission step 3+4)", () => {
  const openReplay = { mode: "REPLAY", session_id: "test-session", last_sequence: 2 };

  it("the stream is the DEFAULT feed: the dial carries the session + the zero cursor; the frames render rows; the phase line reads OPEN", async () => {
    const source = mountTrajectoryStream(vi.fn());
    expect(source.url).toBe("/gateway/events?session_id=test-session&since_sequence=0");
    source.emit("stream.open", frameData(openReplay));
    source.emit("SESSION_CREATED", frameData(syntheticGatewayEvent(1)));
    source.emit("SESSION_ATTACHED", frameData(syntheticGatewayEvent(2)));
    await waitFor(() => {
      expect(screen.getAllByRole("listitem").length).toBeGreaterThanOrEqual(2);
    });
    expect(screen.getByTestId("stream-phase").textContent).toBe("stream OPEN");
    expect(screen.getByText(/LIVE SESSION TAIL/i)).toBeTruthy();
  });

  it("the focused-tab policy: a blurred tab closes its stream (PAUSED, STALE); the refocus re-dials from the cursor", async () => {
    const source = mountTrajectoryStream(vi.fn());
    source.emit("stream.open", frameData(openReplay));
    source.emit("SESSION_CREATED", frameData(syntheticGatewayEvent(1)));
    await waitFor(() => {
      expect(screen.getAllByRole("listitem").length).toBeGreaterThanOrEqual(1);
    });
    const focusSpy = vi.spyOn(document, "hasFocus").mockReturnValue(false);
    window.dispatchEvent(new Event("blur"));
    await waitFor(() => {
      expect(screen.getByTestId("stream-phase").textContent).toBe("stream PAUSED");
    });
    expect(source.closed).toBe(true);
    expect(screen.getByText(/STALE/i)).toBeTruthy();
    focusSpy.mockReturnValue(true);
    window.dispatchEvent(new Event("focus"));
    await waitFor(() => {
      expect(FakeEventSource.instances.length).toBe(2);
    });
    // The re-dial resumes from the LAST RECEIVED sequence (1), never 0.
    expect(FakeEventSource.instances[1]!.url).toContain("since_sequence=1");
  });

  it("a semantic rejection surfaces verbatim and nothing retries (G4's spirit on the stream surface)", async () => {
    const source = mountTrajectoryStream(vi.fn());
    source.emit("stream.rejected", frameData(fixture("stream_rejected")));
    await waitFor(() => {
      expect(screen.getByTestId("stream-phase").textContent).toBe("stream REJECTED");
    });
    const banner = screen.getByRole("status");
    expect(banner.textContent).toContain("DOMAIN_REJECTED");
    // No re-dial ever fires for a semantic verdict.
    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(FakeEventSource.instances.length).toBe(1);
  });

  it("the overflow terminal: the honest note; the adapter's own reconnect re-dials from the last received id", async () => {
    const source = mountTrajectoryStream(vi.fn());
    source.emit("stream.open", frameData(openReplay));
    source.emit("SESSION_CREATED", frameData(syntheticGatewayEvent(1)));
    source.emit("stream.overflow", frameData(fixture("stream_overflow")));
    await waitFor(() => {
      expect(screen.getByTestId("stream-phase").textContent).toBe("stream CONNECTING");
    });
    expect(screen.getByRole("status").textContent).toContain("reconnecting from seq 1");
    await waitFor(
      () => {
        expect(FakeEventSource.instances.length).toBe(2);
      },
      { timeout: 2000 },
    );
    expect(FakeEventSource.instances[1]!.url).toContain("since_sequence=1");
  });

  it("the RESYNC answer: the one-POST recovery fills the retained window, then the stream re-begins from the reconciled cursor", async () => {
    const fetchImpl = vi.fn().mockResolvedValue(
      json({
        status: "OK",
        operation_id: "op-recovery",
        result: {
          events: [4, 5, 6, 7].map((sequence) => syntheticGatewayEvent(sequence)),
          last_sequence: 7,
        },
      }),
    );
    const source = mountTrajectoryStream(fetchImpl);
    source.emit(
      "stream.open",
      frameData({
        mode: "RESYNC",
        session_id: "test-session",
        last_sequence: 7,
        resync: "RESYNC_REQUIRED",
        retained_from: 4,
        snapshot: {
          session_id: "test-session",
          attached: true,
          created_observed_at: 1_000_000,
          event_sequence: 7,
          revision: 6,
        },
      }),
    );
    // The recovery read re-reads from the retained window (since 3).
    await waitFor(() => {
      expect(fetchImpl).toHaveBeenCalledTimes(1);
    });
    const body = JSON.parse(String(fetchImpl.mock.calls[0]![1]!.body)) as Record<string, unknown>;
    expect(body).toMatchObject({ operation: "session.events", arguments: { since_sequence: 3 } });
    await waitFor(() => {
      expect(screen.getAllByRole("listitem").length).toBeGreaterThanOrEqual(4);
    });
    expect(screen.getByText(/RESYNC_REQUIRED/i)).toBeTruthy();
    // The stream re-begins from the POST answer's last_sequence (7).
    await waitFor(() => {
      expect(FakeEventSource.instances.length).toBe(2);
    });
    expect(FakeEventSource.instances[1]!.url).toContain("since_sequence=7");
  });

  it("the transport switch stream -> poll: the stream stops (the source closes), the POST lane takes over", async () => {
    const source = mountTrajectoryStream(vi.fn().mockResolvedValue(json(replayResponse(5))));
    source.emit("stream.open", frameData(openReplay));
    fireEvent.change(screen.getByLabelText("feed transport"), { target: { value: "2000" } });
    await waitFor(() => {
      expect(source.closed).toBe(true);
    });
    await waitFor(() => {
      expect(screen.getAllByRole("listitem").length).toBeGreaterThanOrEqual(5);
    });
    expect(screen.getByText(/poll on/i)).toBeTruthy();
  });
});
