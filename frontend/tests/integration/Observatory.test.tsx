/**
 * The Observatory integration proof (Phase 3's second row), in the
 * browser-less band (jsdom + testing-library; the live evidence
 * rides the iteration report): the HISTORY half of the dual-read law
 * over the EXISTING gateway READ ops — the discovery scan, the
 * bounded event window with the event-id cursor, and the honest
 * failure lanes.
 *
 * What is pinned here (each row a law):
 * - the dual-read law, BOTH halves: the pane labels itself HISTORY
 *   (never LIVE) and dispatches ONLY `observatory.*` operations —
 *   never `session.events` (the wire-level falsifier);
 * - the durable world's no-polling law: mounting dispatches NOTHING
 *   (every read is the user's explicit action);
 * - NO DATA (an empty runs root) is the listing's own honest answer,
 *   never an error;
 * - the window opens from the live-captured fixture: the context
 *   strip carries the identity line (seed, pack, CANON_VIEW,
 *   CANONICAL, 50/56, DURABLE);
 * - the forward pagination carries the EVENT-ID cursor (after =
 *   "ev_0049" — the semantic identity, never a row index), and the
 *   next window REPLACES the current one (boundedness: 5 rows in the
 *   DOM, never 55 — the client never materializes the run);
 * - NO MATCH renders the gateway's own DOMAIN_REJECTED reason
 *   VERBATIM — no fabricated empty window, no auto-retry (G4);
 * - a stale cursor offers the explicit re-read from the head (the
 *   user's decision), and the re-read body carries run only;
 * - a transport failure renders TRANSPORT with its own lane — never
 *   "rejected";
 * - the selection is by event id and consumes the SAME document (no
 *   second per-event op — the fetch count is the falsifier).
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import { GatewayClient } from "../../src/api/gateway/client.ts";
import { Observatory } from "../../src/features/observatory/Observatory.tsx";

const FIXTURES = join(dirname(fileURLToPath(import.meta.url)), "..", "fixtures");

function fixture(name: string): Record<string, unknown> {
  return JSON.parse(readFileSync(join(FIXTURES, `${name}.json`), "utf8")) as Record<string, unknown>;
}

/** An empty runs root — the honest NO DATA answer (the wire form). */
function noDataRuns(): Record<string, unknown> {
  return {
    status: "OK",
    operation_id: "op-runs-empty",
    result: { runs_root: "logs", runs: [] },
  };
}

function json(document: unknown): Response {
  return new Response(JSON.stringify(document), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

/** The parsed request bodies, in dispatch order. */
function callsOf(fetchMock: ReturnType<typeof vi.fn>): Record<string, unknown>[] {
  return fetchMock.mock.calls.map(
    (args) => JSON.parse(String(args[1]?.body)) as Record<string, unknown>,
  );
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

function mountObservatory(fetchImpl: typeof fetch): void {
  vi.stubGlobal("fetch", fetchImpl);
  const client = new GatewayClient();
  render(<Observatory client={client} />);
}

describe("the Observatory surface (Phase 3, row 2 — the HISTORY world)", () => {
  it("labels itself HISTORY — never LIVE — and dispatches NOTHING on mount (no polling)", () => {
    const fetchMock = vi.fn();
    mountObservatory(fetchMock);
    expect(screen.getByText(/HISTORY · COMMITTED LOGS/i)).toBeTruthy();
    expect(screen.getByText(/never the live session tail/i)).toBeTruthy();
    // The LIVE tag (the Trajectory pane's own label) never appears here.
    expect(screen.queryByText(/^LIVE SESSION TAIL$/)).toBeNull();
    // The durable world's own law: no auto-read, no polling — a
    // committed log does not change under the reader.
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("the scan renders the honest listing; NO DATA stays the listing's own answer", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("observatory_runs_ok")))
      .mockResolvedValueOnce(json(noDataRuns()));
    mountObservatory(fetchMock);

    fireEvent.click(screen.getByRole("button", { name: "rescan runs" }));
    await waitFor(() => {
      expect(screen.getByText(/1 found/i)).toBeTruthy();
    });
    expect(screen.getByText("run_125_0")).toBeTruthy();
    expect(screen.getByText(/seed/i)).toBeTruthy();
    expect(screen.getByText(/tavern_pack@0\.1/i)).toBeTruthy();

    // The empty runs root: NO DATA, never an error banner.
    fireEvent.click(screen.getByRole("button", { name: "rescan runs" }));
    await waitFor(() => {
      expect(screen.getByText(/NO DATA — the runs root holds no committed runs/i)).toBeTruthy();
    });
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("opens the run: the context strip's identity line + the first bounded window; observatory.* ops ONLY (the dual-read wire law)", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("observatory_runs_ok")))
      .mockResolvedValueOnce(json(fixture("observatory_read_ok")));
    mountObservatory(fetchMock);

    fireEvent.click(screen.getByRole("button", { name: "rescan runs" }));
    await waitFor(() => {
      expect(screen.getByText("run_125_0")).toBeTruthy();
    });
    fireEvent.click(screen.getByRole("button", { name: "open" }));

    const context = await screen.findByTestId("obs-context");
    expect(context.textContent).toContain("run_125_0");
    expect(context.textContent).toContain("125");
    expect(context.textContent).toContain("CANON_VIEW");
    expect(context.textContent).toContain("CANONICAL");
    expect(context.textContent).toContain("50/56");
    expect(context.textContent).toContain("DURABLE");

    const windowList = screen.getByRole("list", { name: "event window" });
    const rows = within(windowList).getAllByRole("button");
    expect(rows.length).toBe(50);
    expect(rows[0]!.getAttribute("data-event-id")).toBe("ev_0000");

    // The dual-read wire falsifier: every dispatched operation is an
    // observatory.* READ — the LIVE tail's session.events is never
    // touched by the HISTORY pane.
    const operations = callsOf(fetchMock).map((body) => body["operation"]);
    expect(operations).toEqual(["observatory.runs", "observatory.read"]);
  });

  it("the forward pagination carries the EVENT-ID cursor and REPLACES the window (boundedness)", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("observatory_read_ok")))
      .mockResolvedValueOnce(json(fixture("observatory_read_tail")));
    mountObservatory(fetchMock);

    fireEvent.click(screen.getByRole("button", { name: "open stem" }));
    const input = screen.getByPlaceholderText(/open run by stem/i);
    fireEvent.change(input, { target: { value: "run_125_0" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByTestId("obs-context").textContent).toContain("50/56");
    });
    fireEvent.click(screen.getByTestId("next-window"));

    // The tail window: 5 rows REPLACED the 50 (never an accumulating
    // buffer — the client never materializes the run).
    const windowList = await screen.findByRole("list", { name: "event window" });
    await waitFor(() => {
      expect(within(windowList).getAllByRole("button").length).toBe(5);
    });
    expect(screen.getByText(/this is the run's end/i)).toBeTruthy();
    // The end of the run: the forward control honestly disabled.
    expect(screen.getByTestId("next-window").hasAttribute("disabled")).toBe(true);

    // The cursor law: the second read's body carried the window's
    // last event id — the SEMANTIC identity, never a row index.
    const reads = callsOf(fetchMock).filter((body) => body["operation"] === "observatory.read");
    expect(reads.length).toBe(2);
    expect(reads[1]!["arguments"]).toEqual({ run: "run_125_0", after: "ev_0049" });
  });

  it("NO MATCH: the verbatim DOMAIN_REJECTED reason, no fabricated window, no auto-retry (G4)", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("observatory_read_no_match")));
    mountObservatory(fetchMock);

    const input = screen.getByPlaceholderText(/open run by stem/i);
    fireEvent.change(input, { target: { value: "run_ghost" } });
    fireEvent.submit(input.closest("form")!);

    const banner = await screen.findByTestId("read-rejected");
    expect(banner.textContent).toContain("REJECTED · DOMAIN_REJECTED");
    expect(banner.textContent).toContain("no run 'run_ghost' in the runs root");
    expect(banner.textContent).toContain("NO MATCH");
    // No fabricated empty window, no stale "re-read" affordance.
    expect(screen.queryByRole("list", { name: "event window" })).toBeNull();
    expect(screen.queryByRole("button", { name: /re-read from the head/i })).toBeNull();
    // G4's falsifier: exactly one dispatch, and it stays one.
    await new Promise((resolve) => setTimeout(resolve, 30));
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("a stale cursor: the verbatim reason + the EXPLICIT re-read from the head (run-only body)", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("observatory_read_ok")))
      .mockResolvedValueOnce(json(fixture("observatory_read_stale_cursor")))
      .mockResolvedValueOnce(json(fixture("observatory_read_tail")));
    mountObservatory(fetchMock);

    const input = screen.getByPlaceholderText(/open run by stem/i);
    fireEvent.change(input, { target: { value: "run_125_0" } });
    fireEvent.submit(input.closest("form")!);
    await waitFor(() => {
      expect(screen.getByTestId("obs-context")).toBeTruthy();
    });

    // The cursor falls out of the run (the log was rewritten): the
    // honest verdict — and NO second dispatch before the user acts.
    fireEvent.click(screen.getByTestId("next-window"));
    const banner = await screen.findByTestId("read-rejected");
    expect(banner.textContent).toContain("stale cursor");
    expect(fetchMock).toHaveBeenCalledTimes(2);

    // The re-read is the USER's decision: the head read carries run
    // only (no after — the head is the honest restart).
    fireEvent.click(screen.getByRole("button", { name: /re-read from the head/i }));
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledTimes(3);
    });
    const reads = callsOf(fetchMock).filter((body) => body["operation"] === "observatory.read");
    expect(reads[2]!["arguments"]).toEqual({ run: "run_125_0" });
  });

  it("a transport failure renders TRANSPORT with its own lane — never 'rejected'", async () => {
    mountObservatory(vi.fn().mockRejectedValue(new TypeError("fetch failed")));

    const input = screen.getByPlaceholderText(/open run by stem/i);
    fireEvent.change(input, { target: { value: "run_125_0" } });
    fireEvent.submit(input.closest("form")!);

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("TRANSPORT");
    expect(banner.textContent).toContain("delivery failed, never a gateway rejection");
    expect(screen.queryByTestId("read-rejected")).toBeNull();
  });

  it("the selection is by event id and consumes the SAME document — no second dispatch", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("observatory_read_ok")));
    mountObservatory(fetchMock);

    const input = screen.getByPlaceholderText(/open run by stem/i);
    fireEvent.change(input, { target: { value: "run_125_0" } });
    fireEvent.submit(input.closest("form")!);
    const windowList = await screen.findByRole("list", { name: "event window" });
    await waitFor(() => {
      expect(within(windowList).getAllByRole("button").length).toBe(50);
    });

    // LAW §5.1: the inspector consumes the row's SAME document.
    fireEvent.click(within(windowList).getAllByRole("button")[3]!);
    const inspector = await screen.findByTestId("inspector-json");
    expect(inspector.textContent).toContain('"id": "ev_0003"');
    expect(inspector.textContent).toContain('"authority": "CANONICAL"');
    // The selection fired NO second per-event op.
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
