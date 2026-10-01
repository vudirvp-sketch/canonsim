/**
 * The Models integration proof (Phase 3's sixth row), in the
 * browser-less band (jsdom + testing-library; the live evidence rides
 * the iteration report): the model family's mirror over the EXISTING
 * gateway ops — the two session-free context READs (model.list +
 * model.states), the §20 loading half as RUNS (model.load /
 * model.unload), and the run family's three work kinds over run.start
 * (model.fetch / model.import / model.digest), observed through
 * run.get / run.cancel.
 *
 * What is pinned here (each row a law):
 * - the mount fires EXACTLY TWO session-free READs (no arguments, no
 *   session) — no polling;
 * - the §20 ladder law rendered: the row's chip is model.states's own
 *   answer for THAT name (never a discovery guess — the discovery
 *   entry's DISCOVERED and the ladder's SELECTED stay distinct); the
 *   ACTIVE slot is the load-state owner's; MISSING and EMPTY render
 *   their own honest states;
 * - every dispatch carries a session_id + a FRESH idempotency key
 *   (G4 — no blind retry) and the closed per-kind argument sets;
 * - the bounded observation: the terminal triggers EXACTLY ONE
 *   context re-read (the OBSERVED baseline — the landed file rides
 *   the NEXT discovery scan; the ladder rests at its own truth),
 *   never polling;
 * - the verbatim lanes: a REJECTED anything renders the gateway's
 *   reason VERBATIM (unload's not-ACTIVE gate, fetch's admission
 *   gate, the relative import path); TRANSPORT renders the honest
 *   UNKNOWN note; the poll's TRANSPORT renders STALE with the
 *   explicit re-poll (never an auto-retry);
 * - the truthful cancellation: the outcome renders verbatim and the
 *   poll CONTINUES to the run's own terminal;
 * - without a session every dispatch is honestly disabled while the
 *   reads still work; ONE run at a time (the dispatch guard).
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import { GatewayClient } from "../../src/api/gateway/client.ts";
import { Models } from "../../src/features/models/Models.tsx";

const FIXTURES = join(dirname(fileURLToPath(import.meta.url)), "..", "fixtures");

function fixture(name: string): Record<string, unknown> {
  return JSON.parse(readFileSync(join(FIXTURES, `${name}.json`), "utf8")) as Record<string, unknown>;
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

function mountModels(
  fetchImpl: typeof fetch,
  sessionId: string | null = "sess-models-test",
): void {
  vi.stubGlobal("fetch", fetchImpl);
  const client = new GatewayClient();
  render(<Models client={client} sessionId={sessionId} />);
}

/** The models routing mock: the op fixtures + an ordered run.get
 * sequence (each answer consumed in order; the last repeats). */
function modelsRouter(
  ops: Record<string, unknown>,
  runSequence: Record<string, unknown>[] = [],
): ReturnType<typeof vi.fn> {
  let runIndex = 0;
  return vi.fn(async (_input: unknown, init?: RequestInit) => {
    const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
    const op = String(body["operation"] ?? "");
    if (op === "run.get" && runSequence.length > 0) {
      const doc =
        runIndex < runSequence.length ? runSequence[runIndex] : runSequence[runSequence.length - 1]!;
      runIndex += 1;
      return json(doc);
    }
    const doc = ops[op];
    return json(
      doc ?? { status: "REJECTED", rejection: "UNKNOWN_OPERATION", operation_id: "op_router_miss" },
    );
  });
}

const CONTEXT_OPS: Record<string, unknown> = {
  "model.list": fixture("model_list_ok"),
  "model.states": fixture("model_states_ok"),
};

/** The post-load context: the probe touched by the ladder (SELECTED)
 * + the second file landed by the import (derived routing: the same
 * two ops the surface re-reads at the terminal). */
const LANDED_OPS: Record<string, unknown> = {
  "model.list": fixture("model_list_after_import"),
  "model.states": fixture("model_states_selected"),
};

/** A derived non-terminal RUNNING answer over the captured load-run
 * envelope (the committed fixtures stay the live-captured set). */
function runningLoadRun(): Record<string, unknown> {
  const run = structuredClone(fixture("model_load_run_failed"))["result"] as Record<string, unknown>;
  run["state"] = "RUNNING";
  run["terminal"] = false;
  run["failure_type"] = null;
  run["diagnostics"] = [];
  return { status: "OK", operation_id: "op_running", result: run };
}

/** A derived in-flight IMPORT answer with a live progress document
 * (the honest per-chunk report the surface renders verbatim). */
function runningImportRun(copied: number, total: number): Record<string, unknown> {
  const run = structuredClone(fixture("model_import_run_completed"))["result"] as Record<string, unknown>;
  run["state"] = "RUNNING";
  run["terminal"] = false;
  run["progress"] = {
    logical_name: "second-model.gguf",
    file_index: 0,
    file_count: 1,
    copied_bytes: copied,
    total_bytes: total,
  };
  return { status: "OK", operation_id: "op_running_import", result: run };
}

/** A derived load-states view with the probe ACTIVE (the unload
 * affordance's own gate — the committed fixture stays SELECTED). */
function activeStates(): Record<string, unknown> {
  const view = structuredClone(fixture("model_states_selected"));
  const result = view["result"] as Record<string, unknown>;
  result["states"] = { "probe-model.gguf": "ACTIVE" };
  result["active"] = "probe-model.gguf";
  return view;
}

describe("the Models surface (Phase 3, row 6 — the model family's mirror)", () => {
  it("mounts with EXACTLY TWO session-free READs and never polls", async () => {
    const fetchMock = modelsRouter(CONTEXT_OPS);
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });
    const bodies = callsOf(fetchMock);
    expect(bodies.length).toBe(2);
    expect(bodies.map((body) => body["operation"])).toEqual(["model.list", "model.states"]);
    for (const body of bodies) {
      expect(body["arguments"]).toBeUndefined();
      expect(body["session_id"]).toBeUndefined();
    }

    // No context polling: a mounted surface that already read stays at two.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("the §20 ladder law rendered: the chip is model.states's own answer per name, the ACTIVE slot is the owner's, the identity line is honest", async () => {
    const fetchMock = modelsRouter(LANDED_OPS);
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-second-model.gguf")).toBeTruthy();
    });
    // probe: DISCOVERED on the scan, SELECTED on the ladder — the
    // LADDER's answer wins (never a discovery guess); the ACTIVE
    // slot is the strip's own line.
    const probe = screen.getByTestId("models-row-probe-model.gguf");
    expect(within(probe).getByText("SELECTED")).toBeTruthy();
    expect(within(probe).queryByText("ACTIVE")).toBeNull(); // no marker — active is null
    // the digest run's effect rides the discovery entry (the re-scan)
    expect(within(probe).getByText(/sha256 c8d4919ad5f8bc88/)).toBeTruthy();
    // the untouched second file: DISCOVERED, identity not computed
    const second = screen.getByTestId("models-row-second-model.gguf");
    expect(within(second).getByText("DISCOVERED")).toBeTruthy();
    expect(within(second).getByText("strong identity not computed")).toBeTruthy();
    // the strip: the folder + the classification + the count + the slot
    const strip = screen.getByTestId("models-context").textContent;
    expect(strip).toContain("OK");
    expect(strip).toContain("2");
    expect(screen.getByTestId("models-active").textContent).toBe("none");
  });

  it("the MISSING directory renders its own honest state (never an error, never a blank)", async () => {
    const missing = structuredClone(fixture("model_list_ok"));
    const result = missing["result"] as Record<string, unknown>;
    result["directory_state"] = "MISSING";
    result["models"] = [];
    const fetchMock = modelsRouter({
      "model.list": missing,
      "model.states": fixture("model_states_ok"),
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-missing")).toBeTruthy();
    });
    expect(screen.getByTestId("models-missing").textContent).toContain(
      "the models folder does not exist yet",
    );
  });

  it("the EMPTY folder renders its own honest state (distinct from MISSING)", async () => {
    const empty = structuredClone(fixture("model_list_ok"));
    const result = empty["result"] as Record<string, unknown>;
    result["models"] = [];
    const fetchMock = modelsRouter({
      "model.list": empty,
      "model.states": fixture("model_states_ok"),
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-empty")).toBeTruthy();
    });
    expect(screen.getByTestId("models-empty").textContent).toContain(
      "no model files discovered",
    );
  });

  it("the load flow: ONE dispatch with a fresh key → the bounded poll → the FAILED terminal verbatim → exactly ONE context re-read", async () => {
    // the context re-read answers the LANDED form (the ladder truth)
    const fetchMock = modelsRouter(
      { ...CONTEXT_OPS, "model.load": fixture("model_load_start_ok") },
      [fixture("model_load_run_failed")],
    );
    // after the terminal the re-read hits the same op routes; swap
    // them to the landed form on the second call
    let listCount = 0;
    let statesCount = 0;
    fetchMock.mockImplementation(async (_input: unknown, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
      const op = String(body["operation"] ?? "");
      if (op === "model.list") {
        listCount += 1;
        return json(listCount === 1 ? CONTEXT_OPS["model.list"]! : LANDED_OPS["model.list"]!);
      }
      if (op === "model.states") {
        statesCount += 1;
        return json(statesCount === 1 ? CONTEXT_OPS["model.states"]! : LANDED_OPS["model.states"]!);
      }
      if (op === "model.load") {
        return json(fixture("model_load_start_ok"));
      }
      return json(fixture("model_load_run_failed"));
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });

    fireEvent.click(within(screen.getByTestId("models-row-probe-model.gguf")).getByRole("button", { name: "load" }));

    // the FAILED band renders the observed cause verbatim
    const banner = await screen.findByTestId("models-run-failed");
    expect(banner.textContent).toContain("FAILED");
    expect(banner.textContent).toContain("cannot spawn 'llama-server'");

    // exactly ONE context re-read (the closure's OBSERVED baseline)
    await waitFor(() => {
      expect(listCount).toBe(2);
      expect(statesCount).toBe(2);
    });
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(listCount).toBe(2);
    expect(statesCount).toBe(2);

    // the dispatch carried the session + a fresh idempotency key + the closed argument set
    const loadCall = callsOf(fetchMock).find((body) => body["operation"] === "model.load")!;
    expect(loadCall["session_id"]).toBe("sess-models-test");
    expect(String(loadCall["client_request_id"])).toMatch(/^models-load-/);
    expect(loadCall["arguments"]).toEqual({ logical_name: "probe-model.gguf" });
  });

  it("a REJECTED load renders the gateway's reason VERBATIM and never auto-retries (G4)", async () => {
    const rejected = structuredClone(fixture("model_unload_not_active"));
    const result = rejected["result"] as Record<string, unknown>;
    result["reason"] =
      "model.load: 'probe-model.gguf' is FAILED — the Model ladder's FAILED is terminal (no re-selection path; the recorded ladder gap, D-203)";
    const fetchMock = modelsRouter({ ...CONTEXT_OPS, "model.load": rejected });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });
    fireEvent.click(within(screen.getByTestId("models-row-probe-model.gguf")).getByRole("button", { name: "load" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("dispatch REJECTED · DOMAIN_REJECTED");
    expect(banner.textContent).toContain("the Model ladder's FAILED is terminal");
    expect(banner.textContent).toContain("never an auto-retry");

    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(3); // 2 reads + the one dispatch
  });

  it("the unload gate: ACTIVE enables the affordance; the rejection renders the observed state verbatim", async () => {
    const fetchMock = modelsRouter({
      "model.list": fixture("model_list_ok"),
      "model.states": activeStates(),
      "model.unload": fixture("model_unload_not_active"),
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-active").textContent).toBe("probe-model.gguf");
    });
    const probe = screen.getByTestId("models-row-probe-model.gguf");
    // the ACTIVE resting truth: the marker AND the ladder chip (both
    // honest channels — the slot marker and the per-name state)
    expect(within(probe).getAllByText("ACTIVE").length).toBe(2);
    const unloadButton = within(probe).getByRole("button", { name: "unload" });
    expect(unloadButton.hasAttribute("disabled")).toBe(false);

    fireEvent.click(unloadButton);
    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("is not ACTIVE (state: 'SELECTED')");
    expect(banner.textContent).toContain("nothing active to unload");
  });

  it("the unload affordance stays disabled while nothing is ACTIVE (the honest gate)", async () => {
    const fetchMock = modelsRouter(CONTEXT_OPS);
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });
    const unloadButton = within(screen.getByTestId("models-row-probe-model.gguf")).getByRole("button", { name: "unload" });
    expect(unloadButton.hasAttribute("disabled")).toBe(true);
  });

  it("the import flow: the path list rides run.start closed; the live progress renders; the COMPLETED band lands the files; the draft clears ONLY on admission", async () => {
    const fetchMock = modelsRouter(
      { ...CONTEXT_OPS },
      [runningImportRun(30, 67), fixture("model_import_run_completed")],
    );
    // the re-read answers the landed form
    let listCount = 0;
    fetchMock.mockImplementation(async (_input: unknown, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
      const op = String(body["operation"] ?? "");
      if (op === "model.list") {
        listCount += 1;
        return json(listCount === 1 ? CONTEXT_OPS["model.list"]! : LANDED_OPS["model.list"]!);
      }
      if (op === "model.states") {
        return json(CONTEXT_OPS["model.states"]!);
      }
      if (op === "run.start") {
        return json(fixture("model_import_start_ok"));
      }
      if (op === "run.get") {
        return fetchMock.mock.calls.length > 4
          ? json(fixture("model_import_run_completed"))
          : json(runningImportRun(30, 67));
      }
      return json({ status: "REJECTED", rejection: "UNKNOWN_OPERATION", operation_id: "op_miss" });
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });

    fireEvent.change(screen.getByTestId("models-import-paths"), {
      target: { value: "  /home/you/models/tiny.gguf  \n\nrelative-broken.gguf\n" },
    });
    fireEvent.click(screen.getByRole("button", { name: "import" }));

    // the live progress renders (the per-chunk report, verbatim)
    await waitFor(
      () => {
        expect(screen.getByTestId("models-progress").textContent).toContain("file 1/1");
        expect(screen.getByTestId("models-progress").textContent).toContain("30 B of 67 B");
      },
      { timeout: 3000 },
    );

    // the COMPLETED band + the landed row on the re-read
    const completed = await screen.findByTestId("models-run-completed", {}, { timeout: 3000 });
    expect(completed.textContent).toContain("1 file(s) landed");
    expect(completed.textContent).toContain("second-model.gguf");
    await waitFor(() => {
      expect(screen.getByTestId("models-row-second-model.gguf")).toBeTruthy();
    });

    // the wire form: work + the path list (trimmed, empties dropped) + the fresh key
    const startCall = callsOf(fetchMock).find((body) => body["operation"] === "run.start")!;
    expect(startCall["session_id"]).toBe("sess-models-test");
    expect(String(startCall["client_request_id"])).toMatch(/^models-import-/);
    expect(startCall["arguments"]).toEqual({
      work: "model.import",
      arguments: { paths: ["/home/you/models/tiny.gguf", "relative-broken.gguf"] },
    });

    // the draft cleared ONLY on admission
    expect((screen.getByTestId("models-import-paths") as HTMLTextAreaElement).value).toBe("");
  });

  it("the fetch admission rejection renders VERBATIM (the gate fires before any network) and preserves the draft", async () => {
    const fetchMock = modelsRouter({
      ...CONTEXT_OPS,
      "run.start": fixture("model_fetch_exists"),
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });

    fireEvent.change(screen.getByTestId("models-fetch-url"), {
      target: { value: "https://example.com/probe-model.gguf" },
    });
    fireEvent.click(screen.getByRole("button", { name: "fetch" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("already exists in the models directory");
    // the draft survives a REJECTED admission (the user's explicit
    // recovery is editing + re-dispatching, never a retyped URL)
    expect((screen.getByTestId("models-fetch-url") as HTMLInputElement).value).toBe(
      "https://example.com/probe-model.gguf",
    );
  });

  it("the relative import path rejection renders the §16 law VERBATIM", async () => {
    const fetchMock = modelsRouter({
      ...CONTEXT_OPS,
      "run.start": fixture("model_import_relative_path"),
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });

    fireEvent.change(screen.getByTestId("models-import-paths"), {
      target: { value: "relative/model.gguf" },
    });
    fireEvent.click(screen.getByRole("button", { name: "import" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("is relative");
    expect(banner.textContent).toContain("requires absolute paths");
  });

  it("the digest flow: the §9 affordance rides run.start; the COMPLETED band carries the real sha256; the re-read lands it on the row", async () => {
    const fetchMock = vi.fn(async (_input: unknown, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
      const op = String(body["operation"] ?? "");
      if (op === "model.list") {
        return json(fixture("model_list_ok"));
      }
      if (op === "model.states") {
        return json(fixture("model_states_ok"));
      }
      if (op === "run.start") {
        return json(fixture("model_digest_start_ok"));
      }
      if (op === "run.get") {
        return json(fixture("model_digest_run_completed"));
      }
      return json({ status: "REJECTED", rejection: "UNKNOWN_OPERATION", operation_id: "op_miss" });
    });
    // the re-read answers the landed form (the digest rides the entry)
    let listCount = 0;
    fetchMock.mockImplementation(async (_input: unknown, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
      const op = String(body["operation"] ?? "");
      if (op === "model.list") {
        listCount += 1;
        return json(listCount === 1 ? fixture("model_list_ok") : fixture("model_list_after_import"));
      }
      if (op === "model.states") {
        return json(fixture("model_states_selected"));
      }
      if (op === "run.start") {
        return json(fixture("model_digest_start_ok"));
      }
      return json(fixture("model_digest_run_completed"));
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });

    fireEvent.click(within(screen.getByTestId("models-row-probe-model.gguf")).getByRole("button", { name: "compute identity" }));

    const completed = await screen.findByTestId("models-run-completed", {}, { timeout: 3000 });
    expect(completed.textContent).toContain("identity COMPLETED");
    expect(completed.textContent).toContain("c8d4919ad5f8bc8851ca3fc1dda35c181bdc44e2ebe56cd0db4af0d7a0446ea2");

    // the re-read lands the digest on the row (the identity computed,
    // the affordance consumed)
    await waitFor(() => {
      expect(within(screen.getByTestId("models-row-probe-model.gguf")).getByText(/sha256 c8d4919ad5f8bc88/)).toBeTruthy();
    });

    // the wire form: the closed digest argument set + the fresh key
    const startCall = callsOf(fetchMock).find((body) => body["operation"] === "run.start")!;
    expect(String(startCall["client_request_id"])).toMatch(/^models-digest-/);
    expect(startCall["arguments"]).toEqual({
      work: "model.digest",
      arguments: { logical_name: "probe-model.gguf" },
    });
  });

  it("the truthful cancellation: the observed outcome renders verbatim and the poll CONTINUES to the run's own terminal", async () => {
    const fetchMock = modelsRouter(
      {
        ...CONTEXT_OPS,
        "model.load": fixture("model_load_start_ok"),
        "run.cancel": fixture("run_cancel_terminal"),
      },
      [runningLoadRun(), fixture("model_load_run_failed")],
    );
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });
    fireEvent.click(within(screen.getByTestId("models-row-probe-model.gguf")).getByRole("button", { name: "load" }));

    await waitFor(() => {
      expect(screen.getByTestId("models-run-inflight")).toBeTruthy();
    });
    fireEvent.click(screen.getByRole("button", { name: "stop" }));

    await waitFor(() => {
      expect(screen.getByTestId("models-cancel-outcome").textContent).toContain("FAILED_TO_CANCEL");
    });
    // the poll CONTINUES: the run's own terminal lands (the FAILED
    // band — the cancel answer never was a completion)
    const banner = await screen.findByTestId("models-run-failed", {}, { timeout: 3000 });
    expect(banner.textContent).toContain("cannot spawn 'llama-server'");

    // the cancel carried a fresh key + the execution id
    const cancelCall = callsOf(fetchMock).find((body) => body["operation"] === "run.cancel")!;
    expect(String(cancelCall["client_request_id"])).toMatch(/^models-cancel-/);
    expect(cancelCall["arguments"]).toEqual({
      execution_id: "20649469b006c5057ce2d4dd6aa826fa26acc8e9b2fc4832e6c4f386858ecb47",
    });
  });

  it("a poll TRANSPORT renders STALE, stops the loop, and the re-poll is the user's EXPLICIT action (G4)", async () => {
    let runCall = 0;
    const fetchMock = vi.fn(async (_input: unknown, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
      const op = String(body["operation"] ?? "");
      if (op === "model.list") return json(fixture("model_list_ok"));
      if (op === "model.states") return json(fixture("model_states_ok"));
      if (op === "model.load") return json(fixture("model_load_start_ok"));
      if (op === "run.get") {
        runCall += 1;
        if (runCall === 1) return json(runningLoadRun());
        if (runCall === 2) return Promise.reject(new TypeError("gateway dial failed"));
        return json(fixture("model_load_run_failed"));
      }
      return json({ status: "REJECTED", rejection: "UNKNOWN_OPERATION", operation_id: "op_miss" });
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });
    fireEvent.click(within(screen.getByTestId("models-row-probe-model.gguf")).getByRole("button", { name: "load" }));

    await waitFor(
      () => {
        // the IN-FLIGHT line carries the STALE marker; the alert
        // carries the honest UNKNOWN note (two distinct channels)
        expect(screen.getByTestId("models-run-inflight").textContent).toContain(
          "STALE (the observation itself failed)",
        );
        expect(screen.getByRole("alert").textContent).toContain("UNKNOWN");
      },
      { timeout: 3000 },
    );

    // the loop STOPPED: no further run.get until the explicit re-poll
    const callsAfterStale = callsOf(fetchMock).filter((body) => body["operation"] === "run.get").length;
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(callsOf(fetchMock).filter((body) => body["operation"] === "run.get").length).toBe(callsAfterStale);

    // the explicit re-poll resumes the observation (the user's action)
    fireEvent.click(screen.getByRole("button", { name: "re-poll" }));
    await waitFor(
      () => {
        expect(screen.getByTestId("models-run-failed").textContent).toContain("cannot spawn");
      },
      { timeout: 3000 },
    );
  });

  it("a dispatch TRANSPORT renders the honest UNKNOWN note (never a blind retry)", async () => {
    const fetchMock = vi.fn(async (_input: unknown, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
      const op = String(body["operation"] ?? "");
      if (op === "model.list") return json(fixture("model_list_ok"));
      if (op === "model.states") return json(fixture("model_states_ok"));
      if (op === "model.load") return Promise.reject(new TypeError("gateway dial failed"));
      return json({ status: "REJECTED", rejection: "UNKNOWN_OPERATION", operation_id: "op_miss" });
    });
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });
    fireEvent.click(within(screen.getByTestId("models-row-probe-model.gguf")).getByRole("button", { name: "load" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("dispatch TRANSPORT");
    expect(banner.textContent).toContain("the outcome is UNKNOWN");
    expect(banner.textContent).toContain("no blind retry");
  });

  it("without a session every dispatch is honestly disabled while the two READs still work", async () => {
    const fetchMock = modelsRouter(CONTEXT_OPS);
    mountModels(fetchMock, null);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });
    expect(fetchMock).toHaveBeenCalledTimes(2); // the reads are session-free

    const probe = screen.getByTestId("models-row-probe-model.gguf");
    expect(within(probe).getByRole("button", { name: "load" }).hasAttribute("disabled")).toBe(true);
    expect(within(probe).getByRole("button", { name: "unload" }).hasAttribute("disabled")).toBe(true);
    expect(within(probe).getByRole("button", { name: "compute identity" }).hasAttribute("disabled")).toBe(true);
    expect(screen.getByRole("button", { name: "fetch" }).hasAttribute("disabled")).toBe(true);
    expect(screen.getByRole("button", { name: "import" }).hasAttribute("disabled")).toBe(true);
    expect(screen.getByTestId("models-fetch-url").hasAttribute("disabled")).toBe(true);
    expect(screen.getByTestId("models-import-paths").hasAttribute("disabled")).toBe(true);
    expect(screen.getByText(/no session — every dispatch is disabled/i)).toBeTruthy();
  });

  it("ONE run at a time: while a run is in flight every other dispatch stays armed-off (the boundedness guard)", async () => {
    const fetchMock = modelsRouter(
      { ...CONTEXT_OPS, "model.load": fixture("model_load_start_ok") },
      [runningLoadRun()],
    );
    mountModels(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("models-row-probe-model.gguf")).toBeTruthy();
    });
    fireEvent.click(within(screen.getByTestId("models-row-probe-model.gguf")).getByRole("button", { name: "load" }));

    await waitFor(() => {
      expect(screen.getByTestId("models-run-inflight")).toBeTruthy();
    });

    // the guard: every dispatch affordance disabled, no second dispatch
    const probe = screen.getByTestId("models-row-probe-model.gguf");
    expect(within(probe).getByRole("button", { name: "load" }).hasAttribute("disabled")).toBe(true);
    expect(within(probe).getByRole("button", { name: "compute identity" }).hasAttribute("disabled")).toBe(true);
    expect(screen.getByRole("button", { name: "fetch" }).hasAttribute("disabled")).toBe(true);
    expect(screen.getByRole("button", { name: "import" }).hasAttribute("disabled")).toBe(true);

    await new Promise((resolve) => setTimeout(resolve, 40));
    const loads = callsOf(fetchMock).filter((body) => body["operation"] === "model.load").length;
    const starts = callsOf(fetchMock).filter((body) => body["operation"] === "run.start").length;
    expect(loads).toBe(1);
    expect(starts).toBe(0);
  });
});
