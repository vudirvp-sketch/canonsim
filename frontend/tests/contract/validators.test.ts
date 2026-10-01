/**
 * The contract tests — the committed fixtures ARE the wire truth
 * (captured from the live gateway code, in-process dispatch — the
 * parity law's byte form; see manifest.json). Every fixture must
 * validate; every corrupted variant must be REJECTED (the
 * closed-document law: unknown keys, wrong types, and foreign enum
 * members never pass silently).
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import {
  appStatusResultSchema,
  backendSettingsResultSchema,
  chatCompletionResultSchema,
  chatSendResultSchema,
  eventEnvelopeSchema,
  inferenceCategorySchema,
  inferenceChainMemberSchema,
  inferenceControlSchema,
  inferenceDocumentSchema,
  inferencePresetSchema,
  inferenceReadResultSchema,
  launchSettingsDocumentSchema,
  modelDigestResultSchema,
  modelDispatchResultSchema,
  modelFetchProgressSchema,
  modelFetchResultSchema,
  modelImportProgressSchema,
  modelImportResultSchema,
  modelListResultSchema,
  modelLoadResultSchema,
  modelStatesResultSchema,
  modelUnloadResultSchema,
  observatoryEventRowSchema,
  observatoryReadResultSchema,
  observatoryRunsResultSchema,
  responseDocumentSchema,
  runCancelResultSchema,
  runDocumentSchema,
  runStartResultSchema,
  sessionDocumentSchema,
  sessionEventsResultSchema,
  validateResponseDocument,
} from "../../src/api/gateway/validators.ts";
import {
  INFERENCE_KINDS,
  INFERENCE_SCOPES,
  INFERENCE_STATES,
  INFERENCE_VALUE_TYPES,
  MODEL_STATES,
  MODEL_WORK_KINDS,
} from "../../src/api/gateway/contracts.ts";

const FIXTURES = join(dirname(fileURLToPath(import.meta.url)), "..", "fixtures");

function fixture(name: string): unknown {
  return JSON.parse(readFileSync(join(FIXTURES, `${name}.json`), "utf8")) as unknown;
}

describe("the live-gateway fixtures validate (the OK family)", () => {
  it("app_status_ok", () => {
    const document = fixture("app_status_ok");
    expect(responseDocumentSchema.parse(document).status).toBe("OK");
    const status = appStatusResultSchema.parse(
      (document as { result: unknown }).result,
    );
    expect(status.contract).toBe("canon_workbench_gateway@0.1");
    expect(status.operations).toContain("session.events");
  });

  it("session_create_ok / session_get_ok / session_attach_ok", () => {
    for (const name of ["session_create_ok", "session_get_ok", "session_attach_ok"]) {
      const document = fixture(name);
      expect(responseDocumentSchema.parse(document).status).toBe("OK");
    }
    const getSession = fixture("session_get_ok") as { result: unknown };
    // Captured BEFORE the attach probe: attached=false, revision 0 —
    // the OBSERVED state, never the assumed one.
    expect(sessionDocumentSchema.parse(getSession.result).attached).toBe(false);
  });

  it("session_events_ok — every event validates against the envelope", () => {
    const document = fixture("session_events_ok") as { result: { events: unknown[] } };
    const parsed = sessionEventsResultSchema.parse(document.result);
    expect(parsed).toHaveProperty("events");
    if ("events" in parsed) {
      expect(parsed.events.length).toBeGreaterThan(0);
      for (const event of parsed.events) {
        expect(() => eventEnvelopeSchema.parse(event)).not.toThrow();
      }
    }
  });

  it("session_events_resync_required — the dual shape's other half", () => {
    const document = fixture("session_events_resync_required") as { result: unknown };
    const parsed = sessionEventsResultSchema.parse(document.result);
    expect(parsed).not.toHaveProperty("events");
    expect(parsed).toHaveProperty("resync", "RESYNC_REQUIRED");
  });

  it("observatory_runs_ok — the discovery scan (the HISTORY world's entry)", () => {
    const document = fixture("observatory_runs_ok") as { result: unknown };
    const parsed = observatoryRunsResultSchema.parse(document.result);
    expect(parsed.runs.length).toBe(1);
    expect(parsed.runs[0]!.name).toBe("run_125_0");
    expect(parsed.runs[0]!.header?.seed).toBe(125);
    expect(parsed.runs[0]!.error).toBeNull();
  });

  it("observatory_read_ok — the first bounded window (50 of 56, next_after rides)", () => {
    const document = fixture("observatory_read_ok") as { result: unknown };
    const parsed = observatoryReadResultSchema.parse(document.result);
    expect(parsed.profile).toBe("CANON_VIEW");
    expect(parsed.authority).toBe("CANONICAL");
    expect(parsed.total_events).toBe(56);
    expect(parsed.window.after).toBe("");
    expect(parsed.window.events.length).toBe(50);
    expect(parsed.window.next_after).toBe("ev_0049");
    for (const row of parsed.window.events) {
      expect(() => observatoryEventRowSchema.parse(row)).not.toThrow();
    }
  });

  it("observatory_read_tail — the terminal window (next_after null at the run's end)", () => {
    const document = fixture("observatory_read_tail") as { result: unknown };
    const parsed = observatoryReadResultSchema.parse(document.result);
    expect(parsed.window.events.length).toBe(5);
    expect(parsed.window.next_after).toBeNull();
    // The event-id cursor is the semantic identity: the tail window
    // rides after=ev_0050, never a row index.
    expect(parsed.window.after).toBe("ev_0050");
  });

  it("backend_settings_read_ok — the store's defaults document (the CONFIG world's entry)", () => {
    const document = fixture("backend_settings_read_ok") as { result: unknown };
    const parsed = backendSettingsResultSchema.parse(document.result);
    expect(parsed.settings.llama_server_exe).toBe("");
    expect(parsed.settings.no_webui).toBe(true);
    expect(parsed.settings.extra_args).toBe("");
    expect(parsed.managed_live).toBe(false);
    expect(parsed.applies).toBe("next-spawn");
    expect(typeof parsed.command_preview).toBe("string");
    expect(parsed.command_preview).toContain("llama-server");
  });

  it("backend_settings_update_ok — the accepted partial becomes the new current", () => {
    const document = fixture("backend_settings_update_ok") as { result: unknown };
    const parsed = backendSettingsResultSchema.parse(document.result);
    // The OBSERVED state after the save: the store's own answer, never
    // the client's projection of its draft.
    expect(parsed.settings.no_webui).toBe(false);
    expect(parsed.settings.llama_server_exe).toBe("");
    expect(parsed.applies).toBe("next-spawn");
  });
});

describe("the live-gateway fixtures validate (the honest rejection family)", () => {
  it("session_get_domain_rejected", () => {
    const response = validateResponseDocument(fixture("session_get_domain_rejected"));
    expect(response.ok).toBe(false);
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
  });

  it("session_attach_stale_revision", () => {
    const response = validateResponseDocument(fixture("session_attach_stale_revision"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("STALE_REVISION");
  });

  it("session_create_duplicate_request (the result.reason carrier)", () => {
    const response = validateResponseDocument(fixture("session_create_duplicate_request"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DUPLICATE_REQUEST");
  });

  it("session_events_unknown_argument", () => {
    const response = validateResponseDocument(fixture("session_events_unknown_argument"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
  });

  it("observatory_read_no_match — the honest NO MATCH verdict", () => {
    const response = validateResponseDocument(fixture("observatory_read_no_match"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(response.result?.["reason"]).toContain("NO MATCH");
  });

  it("observatory_read_stale_cursor — the loud stale-cursor verdict", () => {
    const response = validateResponseDocument(fixture("observatory_read_stale_cursor"));
    expect(response.status).toBe("REJECTED");
    expect(String(response.result?.["reason"])).toContain("stale cursor");
  });

  it("observatory_read_unknown_argument", () => {
    const response = validateResponseDocument(fixture("observatory_read_unknown_argument"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
  });

  it("backend_settings_update_unknown_field — the closed set's loud rejection", () => {
    const response = validateResponseDocument(fixture("backend_settings_update_unknown_field"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(String(response.result?.["reason"])).toContain("unknown field(s) ['threads']");
    expect(String(response.result?.["reason"])).toContain(
      "closed set: ['llama_server_exe', 'no_webui', 'extra_args']",
    );
  });

  it("backend_settings_update_bad_type — the wrong type is never clamped", () => {
    const response = validateResponseDocument(fixture("backend_settings_update_bad_type"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(String(response.result?.["reason"])).toContain("no_webui 'yes' must be a bool");
  });

  it("backend_settings_read_unknown_argument — the READ takes no arguments", () => {
    const response = validateResponseDocument(fixture("backend_settings_read_unknown_argument"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(String(response.result?.["reason"])).toContain("takes no arguments");
  });
});

describe("the closed-document law (corrupted variants are rejected)", () => {
  it("an unknown top-level key fails", () => {
    const document = {
      status: "OK",
      operation_id: "op",
      result: { service: "x" },
      mystery_key: true,
    };
    expect(() => responseDocumentSchema.parse(document)).toThrow();
  });

  it("a foreign status fails", () => {
    expect(() => responseDocumentSchema.parse({ status: "FINE", operation_id: "op" })).toThrow();
  });

  it("a foreign rejection name fails", () => {
    expect(() =>
      responseDocumentSchema.parse({ status: "REJECTED", operation_id: "op", rejection: "NOPE" }),
    ).toThrow();
  });

  it("an OK response with a rejection fails", () => {
    expect(() =>
      validateResponseDocument({ status: "OK", operation_id: "op", rejection: "DOMAIN_REJECTED" }),
    ).toThrow();
  });

  it("a non-OK response without its rejection fails", () => {
    expect(() => validateResponseDocument({ status: "REJECTED", operation_id: "op" })).toThrow();
  });

  it("a foreign event_type fails", () => {
    const event = {
      event_id: "id",
      session_id: "s",
      operation_id: "o",
      sequence: 1,
      event_type: "SOMETHING_ELSE",
      observed_at: 1,
      payload: {},
    };
    expect(() => eventEnvelopeSchema.parse(event)).toThrow();
  });

  it("sequence 0 fails (the stream starts at 1)", () => {
    const event = {
      event_id: "id",
      session_id: "s",
      operation_id: "o",
      sequence: 0,
      event_type: "SESSION_CREATED",
      observed_at: 1,
      payload: {},
    };
    expect(() => eventEnvelopeSchema.parse(event)).toThrow();
  });

  it("a non-finite observed_at fails", () => {
    const document = fixture("session_events_ok") as {
      result: { events: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.events[0]!["observed_at"] = Number.NaN;
    expect(() => sessionEventsResultSchema.parse(corrupted.result)).toThrow();
  });

  it("an event envelope with an unknown key fails", () => {
    const document = fixture("session_events_ok") as {
      result: { events: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.events[0]!["extra"] = 1;
    expect(() => sessionEventsResultSchema.parse(corrupted.result)).toThrow();
  });

  it("an observatory row with an unknown key fails", () => {
    const document = fixture("observatory_read_ok") as {
      result: { window: { events: Array<Record<string, unknown>> } };
    };
    const corrupted = structuredClone(document);
    corrupted.result.window.events[0]!["extra"] = 1;
    expect(() => observatoryReadResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a state change with a MISSING from/to member fails (presence is the law)", () => {
    const document = fixture("observatory_read_ok") as {
      result: { window: { events: Array<Record<string, unknown>> } };
    };
    const corrupted = structuredClone(document);
    delete (corrupted.result.window.events[0]!["state_changes"] as Array<Record<string, unknown>>)[0]!["from"];
    expect(() => observatoryReadResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a foreign importance enum member fails", () => {
    const document = fixture("observatory_read_ok") as {
      result: { window: { events: Array<Record<string, unknown>> } };
    };
    const corrupted = structuredClone(document);
    corrupted.result.window.events[0]!["importance"] = "CRITICAL";
    expect(() => observatoryReadResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a foreign authority member fails (CANONICAL is the read model's only member)", () => {
    const document = fixture("observatory_read_ok") as {
      result: { window: { events: Array<Record<string, unknown>> } };
    };
    const corrupted = structuredClone(document);
    corrupted.result.window.events[0]!["authority"] = "DERIVED";
    expect(() => observatoryReadResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a non-string next_after fails (null is the terminal form, never 0)", () => {
    const document = fixture("observatory_read_tail") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    (corrupted.result["window"] as Record<string, unknown>)["next_after"] = 0;
    expect(() => observatoryReadResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a fourth settings field fails (the closed set is three)", () => {
    const corrupted = {
      llama_server_exe: "",
      no_webui: true,
      extra_args: "",
      threads: 4,
    };
    expect(() => launchSettingsDocumentSchema.parse(corrupted)).toThrow();
  });

  it("a missing settings member fails (presence is the closed set's law)", () => {
    const corrupted = { llama_server_exe: "", extra_args: "" };
    expect(() => launchSettingsDocumentSchema.parse(corrupted)).toThrow();
  });

  it("a wrong-typed no_webui in the RESULT fails (never clamped client-side)", () => {
    const document = fixture("backend_settings_read_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    (corrupted.result["settings"] as Record<string, unknown>)["no_webui"] = "yes";
    expect(() => backendSettingsResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a foreign applies value fails (next-spawn is the store's only constant)", () => {
    const document = fixture("backend_settings_read_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["applies"] = "immediate";
    expect(() => backendSettingsResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a non-string non-null command_preview fails", () => {
    const document = fixture("backend_settings_read_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["command_preview"] = 5;
    expect(() => backendSettingsResultSchema.parse(corrupted.result)).toThrow();
  });

  it("an unknown top-level settings-document key fails", () => {
    const document = fixture("backend_settings_read_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["preview"] = "a second preview key";
    expect(() => backendSettingsResultSchema.parse(corrupted.result)).toThrow();
  });
});

/* ------------------------------------------------------------------ */
/* The Chat row's contract rows (iter-298)                             */
/* ------------------------------------------------------------------ */

describe("the chat-row fixtures validate (the OK family)", () => {
  it("chat_send_ok — the admission identity (STARTING, never the completion)", () => {
    const document = fixture("chat_send_ok");
    expect(responseDocumentSchema.parse(document).status).toBe("OK");
    const admission = chatSendResultSchema.parse(
      (document as { result: unknown }).result,
    );
    expect(admission.state).toBe("STARTING");
    expect(admission.work).toBe("chat.completion");
    expect(admission.execution_id).toMatch(/^[0-9a-f]{16,}$/);
  });

  it("run_get_failed — the honest failure band (the envelope validates; the work's result stays null)", () => {
    const document = fixture("run_get_failed");
    expect(responseDocumentSchema.parse(document).status).toBe("OK");
    const run = runDocumentSchema.parse((document as { result: unknown }).result);
    expect(run.state).toBe("FAILED");
    expect(run.terminal).toBe(true);
    expect(run.result).toBeNull();
    expect(run.failure_type).toBe("EngineError");
    expect(run.diagnostics.length).toBeGreaterThan(0);
    // The §10 freeze rides the run document as stringified pairs.
    const keys = run.frozen_inputs.map((pair) => pair[0]);
    expect(keys).toContain("messages");
    expect(keys).toContain("temperature");
  });

  it("run_cancel_terminal — the observed outcome over the closed vocabulary", () => {
    const document = fixture("run_cancel_terminal");
    expect(responseDocumentSchema.parse(document).status).toBe("OK");
    const cancel = runCancelResultSchema.parse((document as { result: unknown }).result);
    expect(cancel.cancellation).toBe("FAILED_TO_CANCEL");
  });

  it("model_list_ok — the §20 scan's entry shape (a real on-disk file)", () => {
    const document = fixture("model_list_ok");
    const scan = modelListResultSchema.parse((document as { result: unknown }).result);
    expect(scan.directory_state).toBe("OK");
    expect(scan.models.length).toBe(1);
    expect(scan.models[0]!.state).toBe("DISCOVERED");
    expect(scan.models[0]!.content_digest).toBeNull();
    expect(scan.models_root).toContain("models");
  });

  it("model_states_ok — the empty load-state view (nothing touched)", () => {
    const document = fixture("model_states_ok");
    const states = modelStatesResultSchema.parse((document as { result: unknown }).result);
    expect(states.active).toBeNull();
    expect(Object.keys(states.states).length).toBe(0);
  });

  it("inference_read_ok — the compact projection's slice validates over the FULL live document", () => {
    const document = fixture("inference_read_ok");
    const projection = inferenceReadResultSchema.parse((document as { result: unknown }).result);
    expect(projection.profile_name).toBe("Baseline");
    expect(projection.applies).toBe("next-spawn");
    expect(projection.managed_live).toBe(false);
    expect(projection.controls.length).toBeGreaterThan(10);
    const temperature = projection.controls.find((control) => control.id === "sampling.temperature");
    expect(temperature?.value).toBe(0.8);
    expect(temperature?.state).toBe("EFFECTIVE");
    expect(temperature?.source).toBe("profile");
    // The vocabulary members ride the wire unconsumed (the loose
    // form's own law — present on the captured document, never
    // re-encoded by the mirror).
    const raw = (document as { result: Record<string, unknown> }).result;
    expect(raw["compiled_preview"]).toContain("llama-server");
    expect(Array.isArray(raw["presets"])).toBe(true);
  });
});

describe("the chat-row corrupted variants are REJECTED (the closed-document law)", () => {
  it("a well-formed completion validates first (the reference shape)", () => {
    expect(() =>
      chatCompletionResultSchema.parse({
        content: "x",
        finish_reason: "stop",
        backend: { model: null, build: null },
        requested: { max_tokens: 512, temperature: null },
        effective: { max_tokens: 512, temperature: 0.8 },
      }),
    ).not.toThrow();
  });

  it("a run document with a foreign EXECUTION state fails", () => {
    const document = fixture("run_get_failed") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["state"] = "FINISHED";
    expect(() => runDocumentSchema.parse(corrupted.result)).toThrow();
  });

  it("a run document with a non-tuple frozen input fails", () => {
    const document = fixture("run_get_failed") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["frozen_inputs"] = { messages: "[]" };
    expect(() => runDocumentSchema.parse(corrupted.result)).toThrow();
  });

  it("a run document missing the deadline block fails (presence is the law)", () => {
    const document = fixture("run_get_failed") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    delete corrupted.result["deadline"];
    expect(() => runDocumentSchema.parse(corrupted.result)).toThrow();
  });

  it("a chat completion with a wrong-typed requested temperature fails", () => {
    const completion = {
      content: "hello",
      finish_reason: "stop",
      backend: { model: "m.gguf", build: "b1" },
      requested: { max_tokens: 512, temperature: "0.8" },
      effective: { max_tokens: 512, temperature: 0.8 },
    };
    expect(() => chatCompletionResultSchema.parse(completion)).toThrow();
  });

  it("a chat completion with an unknown member fails (the closed result shape)", () => {
    const completion = {
      content: "hello",
      finish_reason: "stop",
      backend: { model: "m.gguf", build: "b1" },
      requested: { max_tokens: 512, temperature: null },
      effective: { max_tokens: 512, temperature: 0.8 },
      usage: { tokens: 12 },
    };
    expect(() => chatCompletionResultSchema.parse(completion)).toThrow();
  });

  it("a chat send answer with a fabricated state fails (STARTING is the admission's own constant)", () => {
    const document = fixture("chat_send_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["state"] = "COMPLETED";
    expect(() => chatSendResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a model.list entry with a foreign directory_state fails", () => {
    const document = fixture("model_list_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["directory_state"] = "CORRUPT";
    expect(() => modelListResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a model.states view with a foreign MODEL state fails", () => {
    const document = fixture("model_states_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["states"] = { "m.gguf": "LOADINGGG" };
    expect(() => modelStatesResultSchema.parse(corrupted.result)).toThrow();
  });

  it("an inference.read document missing the controls array fails (the consumed slice is closed)", () => {
    const document = fixture("inference_read_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    delete corrupted.result["controls"];
    expect(() => inferenceReadResultSchema.parse(corrupted.result)).toThrow();
  });

  it("an inference.read control entry missing its identity fails", () => {
    const document = fixture("inference_read_ok") as {
      result: { controls: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    delete corrupted.result.controls[0]!["id"];
    expect(() => inferenceReadResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a run.cancel answer with a foreign outcome fails", () => {
    const document = fixture("run_cancel_terminal") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["cancellation"] = "CANCELED_ALREADY";
    expect(() => runCancelResultSchema.parse(corrupted.result)).toThrow();
  });
});

/* ------------------------------------------------------------------ */
/* The Inference workspace row's contract rows (iter-299)             */
/* ------------------------------------------------------------------ */

describe("the inference-workspace fixtures validate (the OK family)", () => {
  it("inference_update_ok — the full workspace document validates at the depth the surface consumes", () => {
    const document = fixture("inference_update_ok");
    expect(responseDocumentSchema.parse(document).status).toBe("OK");
    const workspace = inferenceDocumentSchema.parse(
      (document as { result: unknown }).result,
    );
    // the OBSERVED state after the accepted partial — the resolver's
    // own answer, never the client's projection of its draft.
    const temperature = workspace.controls.find((c) => c.id === "sampling.temperature");
    expect(temperature?.value).toBe(0.65);
    expect(temperature?.state).toBe("EFFECTIVE");
    const topK = workspace.controls.find((c) => c.id === "sampling.top_k");
    expect(topK?.value).toBe(20);
    expect(workspace.profile_name).toBe("Baseline");
    expect(workspace.applies).toBe("next-spawn");
    expect(workspace.managed_live).toBe(false);
    expect(workspace.controls.length).toBe(85);
    expect(workspace.sampler_chain.length).toBe(9);
    expect(workspace.chain_order.length).toBe(9);
    expect(workspace.presets.length).toBe(4);
    expect(workspace.categories.length).toBe(15);
    expect(workspace.pinned).toEqual([]);
    expect(workspace.compiled_preview).toContain("llama-server");
  });

  it("the control metadata depth validates closed (the data-driven editors' own law)", () => {
    const document = fixture("inference_update_ok") as {
      result: { controls: Array<Record<string, unknown>> };
    };
    const gpuLayers = document.result.controls.find(
      (control) => control["id"] === "device.gpu_layers",
    );
    expect(gpuLayers).toBeDefined();
    const parsed = inferenceControlSchema.parse(gpuLayers);
    expect(parsed.kind).toBe("mode");
    expect(parsed.value_type).toBe("gpu_layers");
    expect(parsed.forms).toEqual(["auto", "all"]);
    expect(parsed.minimum).toBeNull();
    expect(parsed.maximum).toBe(999);
    expect(parsed.flag).toBe("-ngl");
    expect(parsed.field).toBe("gpu_layers");
    // every control in the document validates against the mirror
    for (const control of document.result.controls) {
      expect(() => inferenceControlSchema.parse(control)).not.toThrow();
    }
  });

  it("the chain document — 9 ordered members, every member exactly once", () => {
    const document = fixture("inference_update_ok") as {
      result: { sampler_chain: Array<Record<string, unknown>> };
    };
    for (const member of document.result.sampler_chain) {
      expect(() => inferenceChainMemberSchema.parse(member)).not.toThrow();
    }
    const ids = document.result.sampler_chain.map(
      (member) => String(member["id"]),
    );
    expect(new Set(ids).size).toBe(9);
    expect(ids[0]).toBe("penalties");
    expect(ids[8]).toBe("temperature");
  });

  it("the preset document validates (the transparent partial — the values loose by the data-driven law)", () => {
    const document = fixture("inference_update_ok") as {
      result: { presets: Array<Record<string, unknown>> };
    };
    for (const preset of document.result.presets) {
      const parsed = inferencePresetSchema.parse(preset);
      expect(Object.keys(parsed.values).length).toBeGreaterThan(0);
    }
  });

  it("the mirrored vocabularies are the closed sets (the resolver/library's own)", () => {
    expect(INFERENCE_STATES.length).toBe(10);
    expect(INFERENCE_STATES).toContain("INEFFECTIVE");
    expect(INFERENCE_KINDS).toEqual(["value", "mode", "toggle", "chain", "display"]);
    expect(INFERENCE_VALUE_TYPES.length).toBe(6);
    expect(INFERENCE_SCOPES).toEqual(["spawn", "request", "spawn+request"]);
  });
});

describe("the inference-workspace rejection fixtures (the honest loud lanes)", () => {
  it("inference_update_unknown_field — the closed set's own reason verbatim", () => {
    const response = validateResponseDocument(fixture("inference_update_unknown_field"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(String(response.result?.["reason"])).toContain("unknown field(s) ['bogus_flag']");
    expect(String(response.result?.["reason"])).toContain("closed set:");
  });

  it("inference_update_bad_type — the wrong type is never clamped", () => {
    const response = validateResponseDocument(fixture("inference_update_bad_type"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(String(response.result?.["reason"])).toContain("temperature 'hot' must be a number in [0, 2]");
  });

  it("inference_update_bad_chain — a partial chain edit refuses LOUD (the whole-set law)", () => {
    const response = validateResponseDocument(fixture("inference_update_bad_chain"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(String(response.result?.["reason"])).toContain("sampler_chain");
    expect(String(response.result?.["reason"])).toContain("missing member");
  });
});

describe("the inference-workspace corrupted variants are REJECTED (the closed-document law)", () => {
  it("a control with a foreign kind fails", () => {
    const document = fixture("inference_update_ok") as {
      result: { controls: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.controls[0]!["kind"] = "slider";
    expect(() => inferenceControlSchema.parse(corrupted.result.controls[0])).toThrow();
  });

  it("a control with a foreign state fails (the resolver's closed vocabulary)", () => {
    const document = fixture("inference_update_ok") as {
      result: { controls: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.controls[0]!["state"] = "INVALID";
    expect(() => inferenceControlSchema.parse(corrupted.result.controls[0])).toThrow();
  });

  it("a control with a foreign value_type fails (the editors' dispatch vocabulary)", () => {
    const document = fixture("inference_update_ok") as {
      result: { controls: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.controls[0]!["value_type"] = "percentage";
    expect(() => inferenceControlSchema.parse(corrupted.result.controls[0])).toThrow();
  });

  it("a control with an UNKNOWN extra member fails (the resolver's field set is closed)", () => {
    const document = fixture("inference_update_ok") as {
      result: { controls: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.controls[0]!["tooltip"] = "extra";
    expect(() => inferenceControlSchema.parse(corrupted.result.controls[0])).toThrow();
  });

  it("a control with a non-string reasons entry fails (the reason is the §7 law)", () => {
    const document = fixture("inference_update_ok") as {
      result: { controls: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    const mirostat = corrupted.result.controls.find(
      (control) => control["id"] === "sampling.mirostat",
    );
    (mirostat as Record<string, unknown>)["reasons"] = [42];
    expect(() => inferenceControlSchema.parse(mirostat)).toThrow();
  });

  it("a chain member with a foreign state fails", () => {
    const document = fixture("inference_update_ok") as {
      result: { sampler_chain: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.sampler_chain[0]!["state"] = "BYPASS";
    expect(() => inferenceChainMemberSchema.parse(corrupted.result.sampler_chain[0])).toThrow();
  });

  it("a chain member with a negative order fails", () => {
    const document = fixture("inference_update_ok") as {
      result: { sampler_chain: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.sampler_chain[0]!["order"] = -1;
    expect(() => inferenceChainMemberSchema.parse(corrupted.result.sampler_chain[0])).toThrow();
  });

  it("the document missing the sampler_chain fails (the consumed depth is closed)", () => {
    const document = fixture("inference_update_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    delete corrupted.result["sampler_chain"];
    expect(() => inferenceDocumentSchema.parse(corrupted.result)).toThrow();
  });

  it("the document missing the deterministic flag fails", () => {
    const document = fixture("inference_update_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    delete corrupted.result["deterministic"];
    expect(() => inferenceDocumentSchema.parse(corrupted.result)).toThrow();
  });

  it("a preset values list (never a record) fails", () => {
    const preset = {
      id: "p",
      name: "P",
      description: "d",
      values: ["temperature", 0.8],
    };
    expect(() => inferencePresetSchema.parse(preset)).toThrow();
  });

  it("a category with a zero count fails (every category carries controls)", () => {
    const category = { id: "empty", controls: 0 };
    expect(() => inferenceCategorySchema.parse(category)).toThrow();
  });

  it("a control with a non-finite step fails", () => {
    const document = fixture("inference_update_ok") as {
      result: { controls: Array<Record<string, unknown>> };
    };
    const corrupted = structuredClone(document);
    corrupted.result.controls[0]!["step"] = Number.NaN;
    expect(() => inferenceControlSchema.parse(corrupted.result.controls[0])).toThrow();
  });
});

/* ------------------------------------------------------------------ */
/* The Models row's contract rows (iter-300)                            */
/* ------------------------------------------------------------------ */

describe("the models-row fixtures validate (the OK family)", () => {
  it("model_load_start_ok — the shared load/unload admission shape (STARTING at dispatch)", () => {
    const document = fixture("model_load_start_ok");
    expect(responseDocumentSchema.parse(document).status).toBe("OK");
    const admission = modelDispatchResultSchema.parse(
      (document as { result: unknown }).result,
    );
    expect(admission.state).toBe("STARTING");
    expect(admission.work).toBe("model.load");
    expect(admission.logical_name).toBe("probe-model.gguf");
    expect(admission.deadline_seconds).toBe(330);
    expect(admission.execution_id).toMatch(/^[0-9a-f]{16,}$/);
  });

  it("model_load_run_failed — the honest failure band (no llama-server; the §10 freeze rides)", () => {
    const document = fixture("model_load_run_failed");
    expect(responseDocumentSchema.parse(document).status).toBe("OK");
    const run = runDocumentSchema.parse((document as { result: unknown }).result);
    expect(run.state).toBe("FAILED");
    expect(run.terminal).toBe(true);
    expect(run.work).toBe("model.load");
    expect(run.result).toBeNull();
    expect(run.failure_type).toBe("_ManagedError");
    // the observed cause rides the diagnostics verbatim (§21)
    expect(run.diagnostics.join(" ")).toContain("cannot spawn 'llama-server'");
    const keys = run.frozen_inputs.map((pair) => pair[0]);
    expect(keys).toContain("logical_name");
  });

  it("model_states_selected — the ladder truth after the failed load (SELECTED, re-load legal)", () => {
    const document = fixture("model_states_selected");
    const states = modelStatesResultSchema.parse((document as { result: unknown }).result);
    expect(states.active).toBeNull();
    expect(states.states["probe-model.gguf"]).toBe("SELECTED");
  });

  it("model_digest_start_ok — the run.start admission over the closed three-field shape", () => {
    const document = fixture("model_digest_start_ok");
    expect(responseDocumentSchema.parse(document).status).toBe("OK");
    const admission = runStartResultSchema.parse((document as { result: unknown }).result);
    expect(admission.work).toBe("model.digest");
    expect(admission.execution_id).toMatch(/^[0-9a-f]{16,}$/);
    expect(admission.deadline_seconds).toBe(60);
  });

  it("model_digest_run_completed — the §9 strong identity the run computed (real sha256)", () => {
    const document = fixture("model_digest_run_completed");
    const run = runDocumentSchema.parse((document as { result: unknown }).result);
    expect(run.state).toBe("COMPLETED");
    expect(run.work).toBe("model.digest");
    const digest = modelDigestResultSchema.parse(run.result);
    expect(digest.logical_name).toBe("probe-model.gguf");
    expect(digest.chunks).toBe(1);
    // the digest verified against hashlib at capture time (the
    // manifest's own evidence law) — the shape pins it here.
    expect(digest.content_digest).toMatch(/^[0-9a-f]{64}$/);
  });

  it("model_import_start_ok / model_import_run_completed — the local arrival as a run", () => {
    const startDocument = fixture("model_import_start_ok");
    const admission = runStartResultSchema.parse(
      (startDocument as { result: unknown }).result,
    );
    expect(admission.work).toBe("model.import");
    expect(admission.deadline_seconds).toBe(3600);

    const terminalDocument = fixture("model_import_run_completed");
    const run = runDocumentSchema.parse((terminalDocument as { result: unknown }).result);
    expect(run.state).toBe("COMPLETED");
    expect(run.work).toBe("model.import");
    // the live progress shape validates (the per-chunk report)
    const progress = modelImportProgressSchema.parse(run.progress);
    expect(progress.file_count).toBe(1);
    expect(progress.file_index).toBe(0);
    expect(progress.copied_bytes).toBe(progress.total_bytes);
    // the landed list + the count
    const result = modelImportResultSchema.parse(run.result);
    expect(result.count).toBe(1);
    expect(result.imported[0]!.logical_name).toBe("second-model.gguf");
    // the §10 freeze serializes the path list as ONE JSON string
    const frozen = new Map(run.frozen_inputs);
    expect(String(frozen.get("paths"))).toContain("second-model.gguf");
  });

  it("model_list_after_import — the landed file rides the NEXT scan + the digest on the entry", () => {
    const document = fixture("model_list_after_import");
    const scan = modelListResultSchema.parse((document as { result: unknown }).result);
    expect(scan.directory_state).toBe("OK");
    const names = scan.models.map((entry) => entry.logical_name);
    expect(names).toContain("probe-model.gguf");
    expect(names).toContain("second-model.gguf");
    // the digest run's effect: the strong identity rides the entry
    const probe = scan.models.find((entry) => entry.logical_name === "probe-model.gguf");
    expect(probe?.content_digest).toMatch(/^[0-9a-f]{64}$/);
    const second = scan.models.find((entry) => entry.logical_name === "second-model.gguf");
    expect(second?.content_digest).toBeNull();
  });

  it("the mirrored vocabularies are the closed sets (the registry's own)", () => {
    expect(MODEL_STATES.length).toBe(9);
    expect(MODEL_STATES).toContain("EVICTED");
    expect(MODEL_WORK_KINDS).toEqual(["model.fetch", "model.import", "model.digest"]);
  });
});

describe("the models-row rejection fixtures (the honest loud lanes)", () => {
  it("model_unload_not_active — the ladder's own gate verbatim", () => {
    const response = validateResponseDocument(fixture("model_unload_not_active"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(String(response.result?.["reason"])).toContain("is not ACTIVE (state: 'SELECTED')");
    expect(String(response.result?.["reason"])).toContain("nothing active to unload");
  });

  it("model_fetch_exists — the admission gate BEFORE any network (normalize is pure)", () => {
    const response = validateResponseDocument(fixture("model_fetch_exists"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(String(response.result?.["reason"])).toContain("already exists in the models directory");
  });

  it("model_import_relative_path — the §16 absolute-path law verbatim", () => {
    const response = validateResponseDocument(fixture("model_import_relative_path"));
    expect(response.status).toBe("REJECTED");
    expect(response.rejection).toBe("DOMAIN_REJECTED");
    expect(String(response.result?.["reason"])).toContain("is relative");
    expect(String(response.result?.["reason"])).toContain("requires absolute paths");
  });
});

describe("the models-row corrupted variants are REJECTED (the closed-document law)", () => {
  it("a load admission with a fabricated state fails (STARTING is the handler's own constant)", () => {
    const document = fixture("model_load_start_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["state"] = "RUNNING";
    expect(() => modelDispatchResultSchema.parse(corrupted.result)).toThrow();
  });

  it("an unload admission echoed over a foreign work name fails (the two-op closed set)", () => {
    const document = fixture("model_load_start_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    corrupted.result["work"] = "model.reload";
    expect(() => modelDispatchResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a run.start admission missing the deadline fails", () => {
    const document = fixture("model_digest_start_ok") as { result: Record<string, unknown> };
    const corrupted = structuredClone(document);
    delete corrupted.result["deadline_seconds"];
    expect(() => runStartResultSchema.parse(corrupted.result)).toThrow();
  });

  it("a fetch progress with a negative downloaded counter fails", () => {
    expect(() =>
      modelFetchProgressSchema.parse({
        downloaded_bytes: -1,
        logical_name: "m.gguf",
        total_bytes: 100,
      }),
    ).toThrow();
  });

  it("a fetch progress with a string total fails (the total is a number or null — never a guess)", () => {
    expect(() =>
      modelFetchProgressSchema.parse({
        downloaded_bytes: 1,
        logical_name: "m.gguf",
        total_bytes: "unknown",
      }),
    ).toThrow();
  });

  it("an import progress with a zero file_count fails (a frozen list is never empty)", () => {
    expect(() =>
      modelImportProgressSchema.parse({
        logical_name: "m.gguf",
        file_index: 0,
        file_count: 0,
        copied_bytes: 0,
        total_bytes: 10,
      }),
    ).toThrow();
  });

  it("an import result with a count that is not the list's own member count still validates the SHAPE (the count is backend-owned)", () => {
    // the shape law: count is a positive int; the list's length is
    // the backend's own truth, never re-derived here.
    expect(() =>
      modelImportResultSchema.parse({ imported: [], count: 1 }),
    ).not.toThrow();
  });

  it("a load result with a fabricated state fails (ACTIVE is the observed landing)", () => {
    expect(() =>
      modelLoadResultSchema.parse({
        logical_name: "m.gguf",
        location: "/x/m.gguf",
        reply: {},
        state: "LOADED",
      }),
    ).toThrow();
  });

  it("an unload result with an unknown member fails (the closed shape)", () => {
    expect(() =>
      modelUnloadResultSchema.parse({
        logical_name: "m.gguf",
        reply: {},
        state: "EVICTED",
        exit_code: 0,
      }),
    ).toThrow();
  });

  it("a digest result with a non-hex content_digest still validates the SHAPE (the hex pin is the fixture's, not the schema's)", () => {
    // the schema's own law: a non-empty string; the 64-hex pin rides
    // the captured fixture (the capture verified it against hashlib).
    expect(() =>
      modelDigestResultSchema.parse({
        chunks: 1,
        content_digest: "not-hex-but-present",
        logical_name: "m.gguf",
        size_bytes: 1,
      }),
    ).not.toThrow();
  });

  it("a fetch result missing the source URL fails (the provenance member is the law)", () => {
    expect(() =>
      modelFetchResultSchema.parse({
        location: "/x/m.gguf",
        logical_name: "m.gguf",
        size_bytes: 10,
      }),
    ).toThrow();
  });
});
