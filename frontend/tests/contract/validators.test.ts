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
  inferenceReadResultSchema,
  launchSettingsDocumentSchema,
  modelListResultSchema,
  modelStatesResultSchema,
  observatoryEventRowSchema,
  observatoryReadResultSchema,
  observatoryRunsResultSchema,
  responseDocumentSchema,
  runCancelResultSchema,
  runDocumentSchema,
  sessionDocumentSchema,
  sessionEventsResultSchema,
  validateResponseDocument,
} from "../../src/api/gateway/validators.ts";

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
