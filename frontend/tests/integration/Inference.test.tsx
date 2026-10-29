/**
 * The Inference integration proof (Phase 3's fifth row), in the
 * browser-less band (jsdom + testing-library; the live evidence rides
 * the iteration report): the semantic generation-control WORKSPACE
 * over the two EXISTING gateway ops — the session-free full READ and
 * the session-scoped closed partial UPDATE.
 *
 * What is pinned here (each row a law):
 * - the mount fires EXACTLY ONE READ (inference.read, no arguments,
 *   no session) — no polling: the profile does not change under the
 *   reader (the honest next-spawn law);
 * - the workspace builds ON the read: the categories with honest
 *   counts, the SIX default-open families, the closed families one
 *   disclosure away, the advanced rung, the search's §32 match
 *   families (a match shows the advanced rows too), the NO MATCH
 *   empty state distinct;
 * - the DATA-DRIVEN editors: the read document's own metadata builds
 *   them (a number input, an enum select over forms, the gpu_layers
 *   composite, a text field) — the UI never re-encodes the vocabulary;
 * - the §7 law: a configured-but-ineffective control (Mirostat
 *   INACTIVE) stays VISIBLE with the resolver's own reason verbatim;
 * - the EFFECTIVE-STATE CLOSURE (§8): a chip edit is a REQUEST (the
 *   DRAFT marker, never an effective-state claim); the Save carries
 *   ONLY the changed keys (the store's partial law) with a session_id
 *   + a FRESH idempotency key per attempt (G4); on ACCEPTED the
 *   returned document is the new OBSERVED baseline and the draft
 *   reconciles to the SERVER's answer (the forbidden
 *   `input.value === EFFECTIVE` collapse, falsified);
 * - the chain membership is a DRAFT edit — the Save carries the WHOLE
 *   9-member document (never a partial edit);
 * - the preset row: the TRANSPARENT diff preview BEFORE the apply; the
 *   apply is a PLAIN update carrying the preset's values verbatim;
 *   the apply is guarded on a CLEAN draft (never silently modifies
 *   out-of-scope settings);
 * - the pin/unpin is its OWN dispatch over the workspace section (the
 *   whole pinned list), never a profile edit; the pinned strip's
 *   chips are reveals, never second editors;
 * - a REJECTED save renders the gateway's reason VERBATIM, preserves
 *   the draft, and NEVER auto-retries (G4);
 * - without a session every mutation is honestly disabled while the
 *   READ still works; a transport failure renders TRANSPORT with its
 *   own lane and the honest UNKNOWN note.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import { GatewayClient } from "../../src/api/gateway/client.ts";
import { Inference } from "../../src/features/inference/Inference.tsx";

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

function mountInference(
  fetchImpl: typeof fetch,
  sessionId: string | null = "sess-inference-test",
): void {
  vi.stubGlobal("fetch", fetchImpl);
  const client = new GatewayClient();
  render(<Inference client={client} sessionId={sessionId} />);
}

/** A read document with overridden result members (the answer form). */
function readWith(overrides: Record<string, unknown>): Record<string, unknown> {
  const document = structuredClone(fixture("inference_read_ok"));
  const result = document["result"] as Record<string, unknown>;
  Object.assign(result, overrides);
  return document;
}

describe("the Inference surface (Phase 3, row 5 — the generation-control workspace)", () => {
  it("mounts with EXACTLY ONE READ (no arguments, no session) and never polls", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("inference_read_ok")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect((screen.getByTestId("inference-profile-name") as HTMLInputElement).value).toBe("Baseline");
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const body = callsOf(fetchMock)[0]!;
    expect(body["operation"]).toBe("inference.read");
    expect(body["arguments"]).toBeUndefined();
    expect(body["session_id"]).toBeUndefined();

    // No polling: a mounted pane that already read stays at one.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("builds ON the read: the six default-open families render, the closed ones stay one disclosure away, the counts are honest", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("inference_read_ok")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("control-model.context")).toBeTruthy();
    });
    // The six default-open families' rows render (model, device,
    // memory, moe, sampling, chat — §15's own list).
    expect(screen.getByTestId("control-device.flash_attention")).toBeTruthy();
    expect(screen.getByTestId("control-sampling.temperature")).toBeTruthy();
    // The CLOSED families stay collapsed: their rows do not mount
    // until the disclosure click (never a flat 85-control wall).
    expect(screen.queryByTestId("control-loading.warmup")).toBeNull();

    // The honest count: sampling carries 27 controls (the server's
    // own count, rendered verbatim).
    expect(screen.getByTestId("category-sampling").textContent).toContain("27");

    // The disclosure opens the closed family — the rows mount ON it
    // (loading.warmup: a non-advanced member of a closed family).
    fireEvent.click(within(screen.getByTestId("category-loading")).getByRole("button"));
    await waitFor(() => {
      expect(screen.getByTestId("control-loading.warmup")).toBeTruthy();
    });

    // A family whose EVERY member sits on the advanced rung (cpu —
    // NUMA only) opens with the honest note, never a silent blank;
    // the row lands only when the rung is asked for.
    fireEvent.click(within(screen.getByTestId("category-cpu")).getByRole("button"));
    await waitFor(() => {
      expect(screen.getByTestId("category-cpu").textContent).toContain("advanced rung");
    });
    expect(screen.queryByTestId("control-cpu.numa")).toBeNull();
    fireEvent.click(screen.getByText(/advanced controls/i));
    await waitFor(() => {
      expect(screen.getByTestId("control-cpu.numa")).toBeTruthy();
    });
  });

  it("the OBSERVED state rides every row — a configured-but-ineffective control stays VISIBLE with the resolver's own reason", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("inference_read_ok")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("state-sampling.mirostat").textContent).toBe("INACTIVE");
    });
    const reasons = screen.getByTestId("reasons-sampling.mirostat");
    expect(reasons.textContent).toContain("the runtime's own disabled form");
    // The §4 defaults ladder rides side by side (baseline · upstream,
    // never silently reconciled).
    const mirostatRow = screen.getByTestId("control-sampling.mirostat");
    expect(mirostatRow.textContent).toContain("baseline");
    expect(mirostatRow.textContent).toContain("upstream");
  });

  it("the DATA-DRIVEN editors: the read document's own metadata builds them (the UI never re-encodes the vocabulary)", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("inference_read_ok")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("control-sampling.temperature")).toBeTruthy();
    });
    // A float control → a number input seeded from the OBSERVED value.
    const temperature = screen.getByTestId("editor-sampling.temperature") as HTMLInputElement;
    expect(temperature.getAttribute("type")).toBe("number");
    expect(temperature.value).toBe("0.8");
    expect(temperature.getAttribute("min")).toBe("0");
    expect(temperature.getAttribute("max")).toBe("2");
    expect(temperature.getAttribute("step")).toBe("0.05");

    // An enum control → a select over the control's OWN forms.
    const flash = screen.getByTestId("editor-device.flash_attention") as HTMLSelectElement;
    const options = [...flash.options].map((option) => option.value);
    expect(options).toEqual(["auto", "on", "off"]);
    expect(flash.value).toBe("on");

    // The gpu_layers composite: the runtime's literal forms + the
    // explicit count editor ('explicit' is the UI-local mode).
    const gpuForm = screen.getByTestId("editor-device.gpu_layers-form") as HTMLSelectElement;
    expect(gpuForm.value).toBe("explicit");
    const gpuCount = screen.getByTestId("editor-device.gpu_layers") as HTMLInputElement;
    expect(gpuCount.value).toBe("999");

    // A toggle control with enum forms → a select over on/off.
    const fit = screen.getByTestId("editor-device.fit") as HTMLSelectElement;
    expect([...fit.options].map((option) => option.value)).toEqual(["on", "off"]);

    // The chain: the ordered 9-member first-class object.
    expect(screen.getByTestId("chain-penalties")).toBeTruthy();
    expect(screen.getByTestId("chain-temperature")).toBeTruthy();
    expect(screen.getAllByTestId(/^chain-/).length).toBe(9);
  });

  it("the advanced rung and the search: the expert controls hide until asked; a search match is an EXPLICIT ASK; NO MATCH is distinct", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("inference_read_ok")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("control-device.flash_attention")).toBeTruthy();
    });
    // The advanced control (device family, open by default) hides
    // until the rung is asked for.
    expect(screen.queryByTestId("control-device.tensor_split")).toBeNull();
    fireEvent.click(screen.getByText(/advanced controls/i));
    await waitFor(() => {
      expect(screen.getByTestId("control-device.tensor_split")).toBeTruthy();
    });
    // The text editor rides the metadata too.
    expect(
      (screen.getByTestId("editor-device.tensor_split") as HTMLInputElement).getAttribute("type"),
    ).toBe("text");

    // The search over name/flag/category (the §32 match families —
    // the FLAG form carries the hyphen, the name the space).
    fireEvent.change(screen.getByTestId("inference-search"), { target: { value: "top-k" } });
    await waitFor(() => {
      expect(screen.getByTestId("control-sampling.top_k")).toBeTruthy();
    });
    expect(screen.queryByTestId("control-sampling.temperature")).toBeNull();
    expect(screen.queryByTestId("control-model.context")).toBeNull();

    // A FLAG match (the §32 match families — the raw CLI name).
    fireEvent.change(screen.getByTestId("inference-search"), { target: { value: "-ngl" } });
    await waitFor(() => {
      expect(screen.getByTestId("control-device.gpu_layers")).toBeTruthy();
    });
    expect(screen.queryByTestId("control-sampling.top_k")).toBeNull();

    // NO MATCH is its own honest state (never a blank).
    fireEvent.change(screen.getByTestId("inference-search"), { target: { value: "zzz-no-such-control" } });
    await waitFor(() => {
      expect(screen.getByTestId("inference-no-match").textContent).toContain("NO MATCH");
    });

    // The cleared search restores the disclosure state.
    fireEvent.change(screen.getByTestId("inference-search"), { target: { value: "" } });
    await waitFor(() => {
      expect(screen.getByTestId("control-sampling.temperature")).toBeTruthy();
    });
  });

  it("the honest closure: a chip edit is a REQUEST; the save sends ONLY the delta with a fresh key; the server's answer becomes the OBSERVED state", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("inference_read_ok")))
      .mockResolvedValueOnce(json(fixture("inference_update_ok")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("editor-sampling.temperature")).toBeTruthy();
    });

    // The REQUEST stage: a chip edit shows the DRAFT marker — never
    // an effective-state claim (the OBSERVED state stays EFFECTIVE,
    // the row's own state chip).
    fireEvent.change(screen.getByTestId("editor-sampling.temperature"), {
      target: { value: "0.65" },
    });
    expect(screen.getByTestId("draft-sampling.temperature").textContent).toContain("DRAFT");
    expect(screen.getByTestId("inference-dirty").textContent).toContain("DRAFT");
    expect(screen.getByTestId("inference-save").hasAttribute("disabled")).toBe(false);

    fireEvent.click(screen.getByTestId("inference-save"));

    const closure = await screen.findByTestId("inference-update-closure");
    expect(closure.textContent).toContain("UPDATED (save)");
    expect(closure.textContent).toContain("temperature");
    expect(closure.textContent).toContain("EFFECTIVE at the NEXT managed spawn");
    expect(closure.textContent).toContain("applies: next-spawn");

    // The wire law: the UPDATE carried ONLY the changed key, the
    // session, and a fresh idempotency key.
    const updates = callsOf(fetchMock).filter(
      (body) => body["operation"] === "inference.update",
    );
    expect(updates.length).toBe(1);
    expect(updates[0]!["arguments"]).toEqual({ temperature: 0.65 });
    expect(updates[0]!["session_id"]).toBe("sess-inference-test");
    expect(typeof updates[0]!["client_request_id"]).toBe("string");

    // The reconciliation: the draft follows the SERVER's answer — the
    // answer document carries temperature 0.65 AND top_k 20 (a field
    // this client never edited): the server's evidence wins over the
    // local projection (the forbidden collapse, falsified).
    await waitFor(() => {
      expect((screen.getByTestId("editor-sampling.temperature") as HTMLInputElement).value).toBe("0.65");
    });
    await waitFor(() => {
      expect((screen.getByTestId("editor-sampling.top_k") as HTMLInputElement).value).toBe("20");
    });
    expect(screen.queryByTestId("inference-dirty")).toBeNull();
    expect(screen.getByTestId("inference-save").hasAttribute("disabled")).toBe(true);
  });

  it("an entry that is not a legal explicit value yet: the save stays disabled until it is fixed (never clamped)", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("inference_read_ok")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("editor-sampling.temperature")).toBeTruthy();
    });

    // An empty numeric entry is not a legal explicit value — the
    // honest gate, never a silent clamp.
    fireEvent.change(screen.getByTestId("editor-sampling.temperature"), {
      target: { value: "" },
    });
    await waitFor(() => {
      expect(screen.getByText(/not legal explicit values yet|not a legal explicit value yet/i)).toBeTruthy();
    });
    expect(screen.getByTestId("inference-save").hasAttribute("disabled")).toBe(true);

    // Fixing it re-enables the save (the draft rides again).
    fireEvent.change(screen.getByTestId("editor-sampling.temperature"), {
      target: { value: "1.2" },
    });
    await waitFor(() => {
      expect(screen.getByTestId("inference-save").hasAttribute("disabled")).toBe(false);
    });
    expect(screen.queryByText(/not a legal explicit value yet|not legal explicit values yet/i)).toBeNull();
  });

  it("the chain membership is a DRAFT edit — the save carries the WHOLE 9-member document", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("inference_read_ok")))
      .mockResolvedValueOnce(json(fixture("inference_update_ok")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("chain-min_p")).toBeTruthy();
    });
    // Every member is enabled in the observed default chain.
    const minP = screen.getByTestId("chain-min_p").querySelector("input") as HTMLInputElement;
    expect(minP.checked).toBe(true);

    fireEvent.click(minP);
    await waitFor(() => {
      expect(screen.getByTestId("chain-min_p").textContent).toContain("DRAFT — membership");
    });

    fireEvent.click(screen.getByTestId("inference-save"));
    await waitFor(() => {
      expect(screen.getByTestId("inference-update-closure").textContent).toContain("sampler_chain");
    });

    // The wire law: the WHOLE 9-member document rides (never a
    // partial edit — the store's own whole-set law), min_p disabled.
    const updates = callsOf(fetchMock).filter(
      (body) => body["operation"] === "inference.update",
    );
    const arguments_ = updates[0]!["arguments"] as Record<string, unknown>;
    const chain = arguments_["sampler_chain"] as Array<Record<string, unknown>>;
    expect(chain.length).toBe(9);
    const disabled = chain.find((item) => item["id"] === "min_p");
    expect(disabled?.["enabled"]).toBe(false);

    // The reconciliation: the server's answer (all enabled) wins.
    await waitFor(() => {
      expect(
        (screen.getByTestId("chain-min_p").querySelector("input") as HTMLInputElement).checked,
      ).toBe(true);
    });
  });

  it("the preset row: the TRANSPARENT diff preview BEFORE the apply; the apply is a PLAIN update with the preset's values verbatim", async () => {
    // The deterministic preset's single diff: temperature 0.8 → 0.
    const answer = readWith({
      deterministic: true,
      controls: (fixture("inference_read_ok")["result"] as Record<string, unknown>)["controls"],
    });
    // Pin the answer's temperature to the preset's target.
    const controls = answer["result"] as Record<string, unknown>;
    const controlList = controls["controls"] as Array<Record<string, unknown>>;
    const temperature = controlList.find((c) => c["id"] === "sampling.temperature");
    (temperature as Record<string, unknown>)["value"] = 0;
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("inference_read_ok")))
      .mockResolvedValueOnce(json(answer));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("inference-presets")).toBeTruthy();
    });

    // Select the preset — the diff preview renders BEFORE any apply.
    const presetSelect = screen
      .getAllByRole("combobox")
      .find((element) => element.getAttribute("aria-label")?.includes("preset")) as HTMLSelectElement;
    fireEvent.change(presetSelect, { target: { value: "deterministic" } });

    const diff = await screen.findByTestId("inference-preset-diff");
    expect(diff.textContent).toContain("Temperature: 0.8 → 0");

    fireEvent.click(screen.getByTestId("inference-preset-apply"));

    await waitFor(() => {
      expect(screen.getByTestId("inference-update-closure").textContent).toContain("UPDATED (preset)");
    });
    // The wire law: a PLAIN update — the preset's values ride VERBATIM
    // (the deterministic preset is the single-field transparent
    // partial: temperature 0 — never a mode switch).
    const updates = callsOf(fetchMock).filter(
      (body) => body["operation"] === "inference.update",
    );
    expect(updates[0]!["arguments"]).toEqual({ temperature: 0 });

    // The reconciliation: the answer's temperature (0) is the new
    // OBSERVED baseline.
    await waitFor(() => {
      expect((screen.getByTestId("editor-sampling.temperature") as HTMLInputElement).value).toBe("0");
    });
  });

  it("the preset apply is guarded on a CLEAN draft (never silently modifies out-of-scope settings)", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("inference_read_ok")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("editor-sampling.temperature")).toBeTruthy();
    });

    // A dirty draft: the preset apply disables.
    fireEvent.change(screen.getByTestId("editor-sampling.temperature"), {
      target: { value: "1.1" },
    });
    await waitFor(() => {
      expect(screen.getByTestId("inference-dirty")).toBeTruthy();
    });

    const presetSelect = screen
      .getAllByRole("combobox")
      .find((element) => element.getAttribute("aria-label")?.includes("preset")) as HTMLSelectElement;
    fireEvent.change(presetSelect, { target: { value: "deterministic" } });
    await waitFor(() => {
      expect(screen.getByTestId("inference-preset-diff")).toBeTruthy();
    });
    expect(screen.getByTestId("inference-preset-apply").hasAttribute("disabled")).toBe(true);
    // The user's unresolved REQUEST is preserved — no dispatch.
    expect(
      callsOf(fetchMock).filter((body) => body["operation"] === "inference.update").length,
    ).toBe(0);
  });

  it("the pin/unpin is its OWN dispatch over the workspace section; the pinned chip is a REVEAL", async () => {
    const answer = readWith({ pinned: ["sampling.temperature"] });
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("inference_read_ok")))
      .mockResolvedValueOnce(json(answer));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("control-sampling.temperature")).toBeTruthy();
    });
    // Nothing pinned — the honest empty strip.
    expect(screen.getByTestId("inference-pinned-empty").textContent).toContain("nothing pinned");

    // Pin the temperature control — its own explicit dispatch.
    fireEvent.click(screen.getByRole("button", { name: "pin Temperature" }));

    await waitFor(() => {
      expect(screen.getByTestId("inference-update-closure").textContent).toContain("UPDATED (pin)");
    });
    const updates = callsOf(fetchMock).filter(
      (body) => body["operation"] === "inference.update",
    );
    expect(updates[0]!["arguments"]).toEqual({ pinned: ["sampling.temperature"] });

    // The strip renders the chip; the reveal marks the row (a
    // quick-access reveal, never a second editor).
    await waitFor(() => {
      expect(screen.getByTestId("inference-pinned").textContent).toContain("Temperature");
    });
    fireEvent.click(screen.getByRole("button", { name: "Temperature" }));
    await waitFor(() => {
      expect(
        screen.getByTestId("control-sampling.temperature").getAttribute("data-reveal"),
      ).toBe("true");
    });
  });

  it("a REJECTED save: the verbatim reason, the draft PRESERVED, no auto-retry (G4)", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("inference_read_ok")))
      .mockResolvedValueOnce(json(fixture("inference_update_bad_type")));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("editor-sampling.temperature")).toBeTruthy();
    });

    fireEvent.change(screen.getByTestId("editor-sampling.temperature"), {
      target: { value: "1.7" },
    });
    fireEvent.click(screen.getByTestId("inference-save"));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("REJECTED · DOMAIN_REJECTED");
    expect(banner.textContent).toContain("temperature 'hot' must be a number in [0, 2]");
    expect(banner.textContent).toContain("the draft is preserved");

    // The draft IS preserved (the user's work, the user's decision).
    expect(screen.getByTestId("inference-dirty").textContent).toContain("DRAFT");
    expect((screen.getByTestId("editor-sampling.temperature") as HTMLInputElement).value).toBe("1.7");

    // G4's falsifier: one dispatch, and it stays one.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("without a session every mutation is honestly disabled while the READ still works", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("inference_read_ok")));
    mountInference(fetchMock, null);

    await waitFor(() => {
      expect((screen.getByTestId("inference-profile-name") as HTMLInputElement).value).toBe("Baseline");
    });
    expect(screen.getByText(/no session — updates disabled/i)).toBeTruthy();

    // The READ dispatched (session-free); the mutations are disabled —
    // the session-scoped op is never dispatched without a session.
    fireEvent.change(screen.getByTestId("editor-sampling.temperature"), {
      target: { value: "0.9" },
    });
    expect(screen.getByTestId("inference-save").hasAttribute("disabled")).toBe(true);
    expect(
      screen.getByRole("button", { name: "pin Temperature" }).hasAttribute("disabled"),
    ).toBe(true);
    expect(
      callsOf(fetchMock).filter((body) => body["operation"] === "inference.update").length,
    ).toBe(0);
  });

  it("a transport failure on the save renders TRANSPORT with the honest UNKNOWN note — never 'rejected'", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("inference_read_ok")))
      .mockRejectedValueOnce(new TypeError("fetch failed"));
    mountInference(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("editor-sampling.temperature")).toBeTruthy();
    });

    fireEvent.change(screen.getByTestId("editor-sampling.temperature"), {
      target: { value: "0.4" },
    });
    fireEvent.click(screen.getByTestId("inference-save"));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("TRANSPORT");
    expect(banner.textContent).toContain("UNKNOWN");
    expect(banner.textContent).toContain("no blind retry");
    // The draft is preserved — the reconciliation is the user's.
    expect(screen.getByTestId("inference-dirty").textContent).toContain("DRAFT");
  });
});
