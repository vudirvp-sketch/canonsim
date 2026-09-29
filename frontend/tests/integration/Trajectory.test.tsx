/**
 * The S0-2 integration proof, in the browser-less band (jsdom +
 * testing-library; the live-browser evidence rides the iteration
 * report): a ≥10_000-row tail renders with ONLY the window mounted
 * (never the full tree); the cursor is the semantic sequence; the
 * selection is the event_id; the LIVE label and the dual-read note
 * stand; the RESYNC banner shows the honest verdict.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import { GatewayClient } from "../../src/api/gateway/client.ts";
import { Trajectory } from "../../src/features/trajectory/Trajectory.tsx";

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
});

function mountTrajectory(fetchImpl: typeof fetch): void {
  vi.stubGlobal("fetch", fetchImpl);
  const client = new GatewayClient();
  render(<Trajectory client={client} sessionId="test-session" />);
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
