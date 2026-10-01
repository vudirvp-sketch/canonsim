/**
 * The Chat integration proof (Phase 3's fourth row), in the
 * browser-less band (jsdom + testing-library; the live evidence
 * rides the iteration report): the conversation world over the
 * EXISTING gateway ops — chat.send (admission) + run.get (the
 * bounded observation) + run.cancel (the truthful stop) + the
 * header's model.list/model.states + inference.read (the compact
 * projection).
 *
 * What is pinned here (each row a law):
 * - the mount fires EXACTLY THREE session-free READs (model.list,
 *   model.states, inference.read — no arguments) and never polls the
 *   context again (every later read is the user's explicit refresh);
 * - the context strip renders the HONEST model line (none ACTIVE —
 *   the load-state truth, never a discovery guess) and the compact
 *   inference projection (the effective temperature the next send
 *   resolves from — never a hidden sampler setting, §21.2);
 * - the send's wire law: ONE dispatch, the session, a FRESH
 *   idempotency key (G4), the message list as the conversation
 *   context, and the call-local overrides ONLY where explicitly set;
 * - the run's honest closure: the admission answer is STARTING
 *   (never the completion); run.get is the observation path; the
 *   terminal band renders VERBATIM (FAILED: the failure type + the
 *   diagnostics; COMPLETED: the content + the REQUESTED/EFFECTIVE
 *   provenance);
 * - the bounded loop: dead at terminal (no further run.get), dead
 *   at TRANSPORT (the STALE lane + the user's explicit re-poll —
 *   never an auto-retry), one cadence step between observations;
 * - the messages-context rule: only ADMITTED user turns and
 *   COMPLETED assistant turns ride the next send's context (a
 *   TRANSPORT exchange may never have happened — it stays OUT);
 * - a REJECTED send renders the gateway's reason VERBATIM and never
 *   auto-retries;
 * - the stop dispatches run.cancel with a fresh key and renders the
 *   observed outcome verbatim (a REQUEST, never a completion);
 * - without a session the send is honestly disabled while the three
 *   context READs still work (they are session-free).
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import { GatewayClient } from "../../src/api/gateway/client.ts";
import { Chat } from "../../src/features/chat/Chat.tsx";

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
  vi.useRealTimers();
});

function mountChat(
  fetchImpl: typeof fetch,
  sessionId: string | null = "sess-chat-test",
): void {
  vi.stubGlobal("fetch", fetchImpl);
  const client = new GatewayClient();
  render(<Chat client={client} sessionId={sessionId} />);
}

/** The chat routing mock: the op fixtures + an ordered run.get
 * sequence (each answer consumed in order; the last repeats). */
function chatRouter(
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
  "inference.read": fixture("inference_read_ok"),
};

/** A fabricated COMPLETED run document — derived from the captured
 * run envelope (the committed fixtures stay the live-captured set;
 * the completed band is the owner-side live proof, declared here). */
function completedRun(): Record<string, unknown> {
  const run = structuredClone(fixture("run_get_failed"))["result"] as Record<string, unknown>;
  run["state"] = "COMPLETED";
  run["terminal"] = true;
  run["failure_type"] = null;
  run["diagnostics"] = [];
  run["result"] = {
    content: "The tavern hums — a slow night, two lamps short.",
    finish_reason: "stop",
    backend: { model: "probe-model.gguf", build: "b4521" },
    requested: { max_tokens: 512, temperature: null },
    effective: { max_tokens: 512, temperature: 0.8 },
  };
  return { status: "OK", operation_id: "op_completed", result: run };
}

/** A fabricated non-terminal RUNNING answer (the same derivation). */
function runningRun(): Record<string, unknown> {
  const run = structuredClone(fixture("run_get_failed"))["result"] as Record<string, unknown>;
  run["state"] = "RUNNING";
  run["terminal"] = false;
  run["failure_type"] = null;
  run["diagnostics"] = [];
  return { status: "OK", operation_id: "op_running", result: run };
}

describe("the Chat surface (Phase 3, row 4 — the conversation world)", () => {
  it("mounts with EXACTLY THREE session-free READs and never polls the context", async () => {
    const fetchMock = chatRouter(CONTEXT_OPS);
    mountChat(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });
    const bodies = callsOf(fetchMock);
    expect(bodies.length).toBe(3);
    expect(bodies.map((body) => body["operation"])).toEqual([
      "model.list",
      "model.states",
      "inference.read",
    ]);
    for (const body of bodies) {
      expect(body["arguments"]).toBeUndefined();
      expect(body["session_id"]).toBeUndefined();
    }

    // No context polling: a mounted surface that already read stays at three.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });

  it("renders the honest model line + the compact inference projection (never a hidden sampler setting)", async () => {
    const fetchMock = chatRouter(CONTEXT_OPS);
    mountChat(fetchMock);

    await waitFor(() => {
      const strip = screen.getByTestId("chat-context");
      // The load-state truth: nothing ACTIVE (never a discovery guess).
      expect(strip.textContent).toContain("none ACTIVE");
      expect(strip.textContent).toContain("discovered 1");
      // The compact projection: the effective temperature the next
      // send resolves from + the applies law, verbatim.
      expect(strip.textContent).toContain("Baseline");
      expect(strip.textContent).toContain("0.8 (EFFECTIVE · profile)");
      expect(strip.textContent).toContain("managed down");
      expect(strip.textContent).toContain("next-spawn");
    });
    expect(screen.getByText(/full control depth lives in the Inference surface/i)).toBeTruthy();
    // The empty transcript's honest EMPTY state.
    expect(screen.getByTestId("chat-empty").textContent).toContain("no messages yet");
  });

  it("the honest closure to FAILED: one send, one admission, one observation — the diagnostics verbatim, then the loop is DEAD", async () => {
    const fetchMock = chatRouter(
      { ...CONTEXT_OPS, "chat.send": fixture("chat_send_ok") },
      [fixture("run_get_failed")],
    );
    mountChat(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });

    fireEvent.change(screen.getByTestId("chat-input"), {
      target: { value: "What is the tavern's mood tonight?" },
    });
    fireEvent.click(screen.getByRole("button", { name: "send" }));

    const failed = await screen.findByTestId("chat-failed-1");
    expect(failed.textContent).toContain("FAILED");
    expect(failed.textContent).toContain("EngineError");
    expect(failed.textContent).toContain("unavailable");
    // The user's REQUESTED echo rides the transcript (the record).
    expect(screen.getByText("What is the tavern's mood tonight?")).toBeTruthy();

    // The wire law: chat.send carried the session, a fresh key, the
    // message list — and NO temperature (the override was empty).
    const sends = callsOf(fetchMock).filter((body) => body["operation"] === "chat.send");
    expect(sends.length).toBe(1);
    expect(sends[0]!["session_id"]).toBe("sess-chat-test");
    expect(typeof sends[0]!["client_request_id"]).toBe("string");
    expect(sends[0]!["arguments"]).toEqual({
      messages: [{ role: "user", content: "What is the tavern's mood tonight?" }],
    });
    // The observation: run.get over the SAME session + execution id.
    const reads = callsOf(fetchMock).filter((body) => body["operation"] === "run.get");
    expect(reads.length).toBe(1);
    expect(reads[0]!["session_id"]).toBe("sess-chat-test");
    expect(reads[0]!["arguments"]).toEqual({
      execution_id: (fixture("chat_send_ok")["result"] as Record<string, unknown>)["execution_id"],
    });

    // The loop is DEAD at terminal — the composer honestly re-arms:
    // the draft was consumed into the row, so the send is disabled
    // BECAUSE EMPTY; typing re-arms it.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(5);
    expect((screen.getByTestId("chat-input") as HTMLTextAreaElement).value).toBe("");
    expect(screen.getByRole("button", { name: "send" }).hasAttribute("disabled")).toBe(true);
    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "next" } });
    expect(screen.getByRole("button", { name: "send" }).hasAttribute("disabled")).toBe(false);
  });

  it("the COMPLETED band: the assistant bubble + the REQUESTED/EFFECTIVE provenance; the next send carries the conversation context", async () => {
    const fetchMock = chatRouter(
      { ...CONTEXT_OPS, "chat.send": fixture("chat_send_ok") },
      [completedRun()],
    );
    mountChat(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });

    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "first question" } });
    fireEvent.click(screen.getByRole("button", { name: "send" }));

    const provenance = await screen.findByTestId("chat-provenance-1");
    expect(provenance.textContent).toContain("finish stop");
    expect(provenance.textContent).toContain("probe-model.gguf");
    expect(provenance.textContent).toContain("temp requested (absent — the profile's BASE)");
    expect(provenance.textContent).toContain("effective 0.8");
    expect(screen.getByText("The tavern hums — a slow night, two lamps short.")).toBeTruthy();

    // The second send's context: [user, assistant, user] — the
    // conversation rule (admitted turns + completed replies).
    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "second question" } });
    fireEvent.click(screen.getByRole("button", { name: "send" }));
    await waitFor(() => {
      expect(
        callsOf(fetchMock).filter((body) => body["operation"] === "chat.send").length,
      ).toBe(2);
    });
    const secondSend = callsOf(fetchMock).filter(
      (body) => body["operation"] === "chat.send",
    )[1]!;
    expect(secondSend["arguments"]).toEqual({
      messages: [
        { role: "user", content: "first question" },
        { role: "assistant", content: "The tavern hums — a slow night, two lamps short." },
        { role: "user", content: "second question" },
      ],
    });
  });

  it("the call-local overrides ride the wire ONLY where explicitly set", async () => {
    const fetchMock = chatRouter(
      { ...CONTEXT_OPS, "chat.send": fixture("chat_send_ok") },
      [completedRun()],
    );
    mountChat(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });

    fireEvent.change(screen.getByLabelText(/temperature/i), { target: { value: "1.2" } });
    fireEvent.change(screen.getByLabelText(/max_tokens/i), { target: { value: "256" } });
    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "hello" } });
    fireEvent.click(screen.getByRole("button", { name: "send" }));

    await screen.findByTestId("chat-provenance-1");
    const sends = callsOf(fetchMock).filter((body) => body["operation"] === "chat.send");
    expect(sends[0]!["arguments"]).toEqual({
      messages: [{ role: "user", content: "hello" }],
      temperature: 1.2,
      max_tokens: 256,
    });
  });

  it("an ILLEGAL explicit override disables the send honestly (the affordance; the law stays backend-side)", async () => {
    const fetchMock = chatRouter(CONTEXT_OPS);
    mountChat(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });

    fireEvent.change(screen.getByLabelText(/temperature/i), { target: { value: "5" } });
    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "hello" } });
    expect(screen.getByRole("button", { name: "send" }).hasAttribute("disabled")).toBe(true);
    expect(screen.getByText(/not a legal explicit value yet/i)).toBeTruthy();
    expect(
      callsOf(fetchMock).filter((body) => body["operation"] === "chat.send").length,
    ).toBe(0);
  });

  it("a REJECTED send renders the verbatim reason and never auto-retries (G4)", async () => {
    const fetchMock = chatRouter({
      ...CONTEXT_OPS,
      "chat.send": fixture("chat_send_unknown_argument"),
    });
    mountChat(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });

    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "hi" } });
    fireEvent.click(screen.getByRole("button", { name: "send" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("chat.send REJECTED · DOMAIN_REJECTED");
    expect(banner.textContent).toContain("unknown argument(s) ['top_p']");
    expect(banner.textContent).toContain("never an auto-retry");

    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(4); // 3 reads + the one send
  });

  it("a send TRANSPORT renders the UNKNOWN note — and the turn stays OUT of the next send's context", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("model_list_ok")))
      .mockResolvedValueOnce(json(fixture("model_states_ok")))
      .mockResolvedValueOnce(json(fixture("inference_read_ok")))
      .mockRejectedValueOnce(new TypeError("fetch failed"));
    mountChat(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });

    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "lost message" } });
    fireEvent.click(screen.getByRole("button", { name: "send" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("chat.send TRANSPORT");
    expect(banner.textContent).toContain("UNKNOWN");
    expect(banner.textContent).toContain("no blind retry");

    // The possibly-never-happened turn rides NO later context.
    const next = chatRouter({ ...CONTEXT_OPS, "chat.send": fixture("chat_send_ok") }, [
      completedRun(),
    ]);
    vi.stubGlobal("fetch", next);
    const client = new GatewayClient();
    cleanup();
    render(<Chat client={client} sessionId="sess-chat-test" />);
    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });
    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "next message" } });
    fireEvent.click(screen.getByRole("button", { name: "send" }));
    await screen.findByTestId("chat-provenance-1");
    const send = callsOf(next).find((body) => body["operation"] === "chat.send")!;
    expect(send["arguments"]).toEqual({
      messages: [{ role: "user", content: "next message" }],
    });
  });

  it("the stop: run.cancel with a FRESH key; the observed outcome verbatim (a request, never a completion)", async () => {
    const fetchMock = chatRouter(
      {
        ...CONTEXT_OPS,
        "chat.send": fixture("chat_send_ok"),
        "run.cancel": {
          status: "OK",
          operation_id: "op_cancel",
          result: { execution_id: "exec-x", cancellation: "CANCEL_REQUESTED" },
        },
      },
      [runningRun()],
    );
    mountChat(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });

    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "long question" } });
    fireEvent.click(screen.getByRole("button", { name: "send" }));

    await waitFor(() => {
      expect(screen.getByTestId("chat-lane-1").textContent).toContain("RUNNING");
    });
    fireEvent.click(screen.getByRole("button", { name: "stop" }));

    await waitFor(() => {
      expect(screen.getByTestId("chat-lane-1").textContent).toContain("CANCEL_REQUESTED");
    });
    const cancels = callsOf(fetchMock).filter((body) => body["operation"] === "run.cancel");
    expect(cancels.length).toBe(1);
    expect(cancels[0]!["session_id"]).toBe("sess-chat-test");
    expect(typeof cancels[0]!["client_request_id"]).toBe("string");
    // The run lane still shows the observed state — the poll
    // continues toward the terminal truth.
    expect(screen.getByTestId("chat-lane-1").textContent).toContain("RUNNING");
  });

  it("a run.get TRANSPORT stops the loop (STALE) — the re-poll is the user's explicit action", async () => {
    // The dispatch sequence: the three context reads, chat.send, then
    // the FIRST run.get fails at the transport level.
    const sequence: (Response | TypeError)[] = [
      json(fixture("model_list_ok")),
      json(fixture("model_states_ok")),
      json(fixture("inference_read_ok")),
      json(fixture("chat_send_ok")),
      new TypeError("poll transport failed"),
    ];
    let index = 0;
    const fetchMock = vi.fn(async (): Promise<Response> => {
      const answer = sequence[index] ?? json(fixture("run_get_failed"));
      index += 1;
      if (answer instanceof TypeError) throw answer;
      return answer;
    });
    mountChat(fetchMock);

    // The context reads settle BEFORE the interaction (the composer's
    // busy-guard rides them).
    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });

    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "any" } });
    fireEvent.click(screen.getByRole("button", { name: "send" }));

    const stale = await screen.findByRole("alert");
    expect(stale.textContent).toContain("run.get TRANSPORT");
    expect(stale.textContent).toContain("UNKNOWN");
    expect(stale.textContent).toContain("re-poll");

    // The loop is dead: no second run.get fires on its own.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(
      callsOf(fetchMock).filter((body) => body["operation"] === "run.get").length,
    ).toBe(1);

    // The explicit re-poll — the user's action (G4).
    fireEvent.click(screen.getByRole("button", { name: "re-poll" }));
    await waitFor(() => {
      expect(
        callsOf(fetchMock).filter((body) => body["operation"] === "run.get").length,
      ).toBe(2);
    });
  });

  it("the bounded cadence: one observation per interval, dead at terminal (real-time proof)", async () => {
    const fetchMock = chatRouter(
      { ...CONTEXT_OPS, "chat.send": fixture("chat_send_ok") },
      [runningRun(), fixture("run_get_failed")],
    );
    mountChat(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });

    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "timed" } });
    fireEvent.click(screen.getByRole("button", { name: "send" }));

    // The FIRST observation (immediate): RUNNING, not terminal.
    await waitFor(() => {
      expect(screen.getByTestId("chat-lane-1").textContent).toContain("RUNNING");
    });
    expect(
      callsOf(fetchMock).filter((body) => body["operation"] === "run.get").length,
    ).toBe(1);

    // One interval later (real time): the SECOND observation — terminal.
    const failed = await screen.findByTestId("chat-failed-1", {}, { timeout: 2000 });
    expect(failed.textContent).toContain("EngineError");
    expect(
      callsOf(fetchMock).filter((body) => body["operation"] === "run.get").length,
    ).toBe(2);

    // The loop is dead: an interval past terminal adds NOTHING.
    await new Promise((resolve) => setTimeout(resolve, 800));
    expect(
      callsOf(fetchMock).filter((body) => body["operation"] === "run.get").length,
    ).toBe(2);
  });

  it("without a session the send is honestly disabled while the three context READs still work", async () => {
    const fetchMock = chatRouter(CONTEXT_OPS);
    mountChat(fetchMock, null);

    await waitFor(() => {
      expect(screen.getByTestId("chat-context").textContent).toContain("Baseline");
    });
    expect(fetchMock).toHaveBeenCalledTimes(3);
    expect(screen.getByRole("button", { name: "send" }).hasAttribute("disabled")).toBe(true);
    expect(screen.getByText(/no session — the send is disabled/i)).toBeTruthy();
    expect(
      callsOf(fetchMock).filter((body) => body["operation"] === "chat.send").length,
    ).toBe(0);
  });
});
