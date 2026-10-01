/**
 * The Settings integration proof (Phase 3's third row; iter-301 adds
 * the SECONDARY NAV rows), in the browser-less band (jsdom +
 * testing-library; the live evidence rides the iteration report):
 * the CONFIG world over the two EXISTING gateway ops — the
 * session-free READ and the session-scoped closed partial UPDATE —
 * now carrying its own sections (Deployment | About).
 *
 * What is pinned here (each row a law):
 * - the mount fires EXACTLY ONE READ (backend.settings, no arguments,
 *   no session) — no polling: the settings do not change under the
 *   reader (the honest next-spawn law);
 * - the surface labels itself CONFIG (never LIVE, never HISTORY —
 *   the channel law) and renders the store's own document: the closed
 *   three fields, applies next-spawn, the compiled command preview;
 * - the EFFECTIVE-STATE CLOSURE (§8): a draft edit is a REQUEST (the
 *   DRAFT marker appears, never an effective-state claim); the Save
 *   body carries ONLY the changed fields (the store's partial law)
 *   with a session_id + a FRESH idempotency key per attempt (G4);
 * - on ACCEPTED the returned document is the new OBSERVED baseline
 *   and the draft reconciles to the SERVER's answer (the forbidden
 *   `input.value === EFFECTIVE` collapse, falsified);
 * - a REJECTED save renders the gateway's reason VERBATIM, preserves
 *   the draft, and NEVER auto-retries (G4's one-dispatch falsifier);
 * - without a session the Save is honestly disabled (the UPDATE is
 *   session-scoped) while the READ still works;
 * - a transport failure renders TRANSPORT with its own lane — never
 *   "rejected" — and the honest UNKNOWN note for a possibly-sent
 *   mutation.
 *
 * The secondary-nav rows (iter-301 — the verdict's step 5 reconciled
 * with inf-1 by the D-246 method):
 * - the nav carries EXACTLY the two approved sections (Deployment |
 *   About — real content only, never a feature directory: Appearance
 *   is a named boundary, Advanced dissolves into the document);
 * - Deployment is the default section; the About pane is absent
 *   until asked;
 * - switching to About mounts the About section with ONE identity
 *   READ (app.status — no arguments, no session) and does NOT
 *   re-read the settings document (the container owns the read);
 * - the About identity renders the gateway's own document VERBATIM
 *   (service/contract/exposure/auth + the full operation registry);
 * - the DRAFT SURVIVES a section switch (the draft's owner is the
 *   SURFACE, never the form section — the forbidden collapse: a
 *   section switch dropping the user's REQUEST in flight);
 * - the About lanes stay honest: TRANSPORT renders with the explicit
 *   re-read note, never "rejected"; MISMATCH reports, never coerces;
 * - a remounted About re-reads its evidence (the mounting
 *   discipline), and the identity never polls.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";

import { GatewayClient } from "../../src/api/gateway/client.ts";
import { Settings } from "../../src/features/settings/Settings.tsx";

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

function mountSettings(
  fetchImpl: typeof fetch,
  sessionId: string | null = "sess-settings-test",
): void {
  vi.stubGlobal("fetch", fetchImpl);
  const client = new GatewayClient();
  render(<Settings client={client} sessionId={sessionId} />);
}

describe("the Settings surface (Phase 3, row 3 — the CONFIG world)", () => {
  it("mounts with EXACTLY ONE READ (no arguments, no session) and never polls", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("backend_settings_read_ok")));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("settings-preview").textContent).toContain("llama-server");
    });
    // The mount read: the operation, the ABSENT arguments, and no
    // session on the wire (the READ is session-free).
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const body = callsOf(fetchMock)[0]!;
    expect(body["operation"]).toBe("backend.settings");
    expect(body["arguments"]).toBeUndefined();
    expect(body["session_id"]).toBeUndefined();

    // No polling: a mounted pane that already read stays at one.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("labels itself CONFIG (never LIVE/HISTORY) and renders the store's own document", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("backend_settings_read_ok")));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByText(/CONFIG · USER/i)).toBeTruthy();
    });
    expect(screen.queryByText(/^LIVE SESSION TAIL$/)).toBeNull();
    expect(screen.queryByText(/HISTORY · COMMITTED LOGS/i)).toBeNull();

    const context = screen.getByTestId("settings-context");
    expect(context.textContent).toContain("next-spawn");
    expect(context.textContent).toContain("down");
    // The closed three-field form, seeded from the READ document.
    const exe = screen.getByLabelText(/llama_server_exe/i) as HTMLInputElement;
    const webui = screen.getByLabelText(/no_webui/i) as HTMLInputElement;
    const extra = screen.getByLabelText(/extra_args/i) as HTMLInputElement;
    expect(exe.value).toBe("");
    expect(webui.checked).toBe(true);
    expect(extra.value).toBe("");
    // The draft starts CLEAN: the save is honestly disabled.
    expect(screen.queryByTestId("settings-dirty")).toBeNull();
    expect(screen.getByRole("button", { name: "save changes" }).hasAttribute("disabled")).toBe(true);
  });

  it("the honest closure: a draft edit is a REQUEST; the save sends ONLY the delta with a fresh key; the server's answer becomes the OBSERVED state", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("backend_settings_read_ok")))
      .mockResolvedValueOnce(json(fixture("backend_settings_update_ok")));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByLabelText(/no_webui/i)).toBeTruthy();
    });

    // The REQUEST stage: a draft edit shows the marker, never an
    // effective-state claim.
    fireEvent.click(screen.getByLabelText(/no_webui/i));
    expect(screen.getByTestId("settings-dirty").textContent).toContain("DRAFT");
    expect(screen.getByRole("button", { name: "save changes" }).hasAttribute("disabled")).toBe(false);

    fireEvent.click(screen.getByRole("button", { name: "save changes" }));

    const closure = await screen.findByTestId("settings-save-closure");
    expect(closure.textContent).toContain("SAVED");
    expect(closure.textContent).toContain("no_webui");
    expect(closure.textContent).toContain("EFFECTIVE at the NEXT managed spawn");
    expect(closure.textContent).toContain("applies: next-spawn");

    // The wire law: the UPDATE carried ONLY the changed field, the
    // session, and a fresh idempotency key.
    const updates = callsOf(fetchMock).filter(
      (body) => body["operation"] === "backend.settings.update",
    );
    expect(updates.length).toBe(1);
    expect(updates[0]!["arguments"]).toEqual({ no_webui: false });
    expect(updates[0]!["session_id"]).toBe("sess-settings-test");
    expect(typeof updates[0]!["client_request_id"]).toBe("string");

    // The reconciliation: the draft follows the SERVER's answer (the
    // OBSERVED state, never the local projection) — the read's
    // observed no_webui (true) is superseded by the answer (false).
    await waitFor(() => {
      expect((screen.getByLabelText(/no_webui/i) as HTMLInputElement).checked).toBe(false);
    });
    expect(screen.queryByTestId("settings-dirty")).toBeNull();
    expect(screen.getByRole("button", { name: "save changes" }).hasAttribute("disabled")).toBe(true);
  });

  it("a second explicit attempt carries a DIFFERENT idempotency key (G4's fresh-key falsifier)", async () => {
    const read = fixture("backend_settings_read_ok");
    const firstAnswer = fixture("backend_settings_update_ok");
    const secondAnswer = structuredClone(firstAnswer);
    (secondAnswer["result"] as Record<string, unknown>)["settings"] = {
      llama_server_exe: "",
      no_webui: true,
      extra_args: "--verbose",
    };
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(read))
      .mockResolvedValueOnce(json(firstAnswer))
      .mockResolvedValueOnce(json(read))
      .mockResolvedValueOnce(json(secondAnswer));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByLabelText(/no_webui/i)).toBeTruthy();
    });

    // Attempt one: toggle the web-UI flag.
    fireEvent.click(screen.getByLabelText(/no_webui/i));
    fireEvent.click(screen.getByRole("button", { name: "save changes" }));
    await waitFor(() => {
      expect(screen.getByTestId("settings-save-closure")).toBeTruthy();
    });

    // Attempt two: a different field, a fresh key.
    const extra = screen.getByLabelText(/extra_args/i) as HTMLInputElement;
    fireEvent.change(extra, { target: { value: "--verbose" } });
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "save changes" }).hasAttribute("disabled")).toBe(false);
    });
    fireEvent.click(screen.getByRole("button", { name: "save changes" }));
    await waitFor(() => {
      expect(callsOf(fetchMock).filter((b) => b["operation"] === "backend.settings.update").length).toBe(2);
    });

    const updates = callsOf(fetchMock).filter(
      (body) => body["operation"] === "backend.settings.update",
    );
    expect(updates[1]!["arguments"]).toEqual({ extra_args: "--verbose" });
    expect(updates[0]!["client_request_id"]).not.toBe(updates[1]!["client_request_id"]);
  });

  it("a REJECTED save: the verbatim reason, the draft PRESERVED, no auto-retry (G4)", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("backend_settings_read_ok")))
      .mockResolvedValueOnce(json(fixture("backend_settings_update_bad_type")));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByLabelText(/no_webui/i)).toBeTruthy();
    });

    fireEvent.click(screen.getByLabelText(/no_webui/i));
    fireEvent.click(screen.getByRole("button", { name: "save changes" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("REJECTED · DOMAIN_REJECTED");
    expect(banner.textContent).toContain("no_webui 'yes' must be a bool");
    expect(banner.textContent).toContain("the draft is preserved");

    // The draft IS preserved (the user's work, the user's decision).
    expect(screen.getByTestId("settings-dirty").textContent).toContain("DRAFT");
    expect((screen.getByLabelText(/no_webui/i) as HTMLInputElement).checked).toBe(false);

    // G4's falsifier: one dispatch, and it stays one.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("without a session the Save is honestly disabled while the READ still works", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("backend_settings_read_ok")));
    mountSettings(fetchMock, null);

    await waitFor(() => {
      expect(screen.getByTestId("settings-preview").textContent).toContain("llama-server");
    });
    // The READ dispatched (session-free); the save is disabled with
    // the honest marker — the UPDATE is session-scoped.
    expect(screen.getByText(/no session — save disabled/i)).toBeTruthy();
    expect(screen.getByRole("button", { name: "save changes" }).hasAttribute("disabled")).toBe(true);

    // The session-scoped op is never dispatched without a session.
    fireEvent.click(screen.getByLabelText(/no_webui/i));
    fireEvent.click(screen.getByRole("button", { name: "save changes" }));
    expect(
      callsOf(fetchMock).filter((body) => body["operation"] === "backend.settings.update").length,
    ).toBe(0);
  });

  it("a transport failure on the save renders TRANSPORT with the honest UNKNOWN note — never 'rejected'", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("backend_settings_read_ok")))
      .mockRejectedValueOnce(new TypeError("fetch failed"));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByLabelText(/no_webui/i)).toBeTruthy();
    });

    fireEvent.click(screen.getByLabelText(/no_webui/i));
    fireEvent.click(screen.getByRole("button", { name: "save changes" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("save TRANSPORT");
    expect(banner.textContent).toContain("UNKNOWN");
    expect(banner.textContent).toContain("no blind retry");
    // The draft is preserved — the reconciliation is the user's.
    expect(screen.getByTestId("settings-dirty").textContent).toContain("DRAFT");
  });
});

describe("the Settings secondary navigation (iter-301 — the verdict's step 5, reconciled with inf-1)", () => {
  it("carries EXACTLY the two approved sections; Deployment is the default; About is absent until asked", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("backend_settings_read_ok")));
    mountSettings(fetchMock);

    const nav = screen.getByRole("navigation", { name: "Settings sections" });
    const tabs = [...nav.querySelectorAll("button")].map((button) => button.textContent);
    expect(tabs).toEqual(["Deployment", "About"]);

    // Deployment is active (aria-current); the About pane is absent.
    expect(screen.getByRole("button", { name: "Deployment" }).getAttribute("aria-current")).toBe("page");
    expect(screen.getByRole("button", { name: "About" }).getAttribute("aria-current")).toBeNull();
    expect(screen.queryByTestId("about-identity")).toBeNull();
    // The Deployment document is live (the closed form).
    await waitFor(() => {
      expect(screen.getByLabelText(/llama_server_exe/i)).toBeTruthy();
    });
    // The mount read is the SETTINGS read only — About never dispatched.
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(callsOf(fetchMock)[0]!["operation"]).toBe("backend.settings");
  });

  it("switching to About: ONE identity READ (no arguments, no session); the settings document is NOT re-read; the identity renders VERBATIM", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("backend_settings_read_ok")))
      .mockResolvedValueOnce(json(fixture("app_status_composition")));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByLabelText(/llama_server_exe/i)).toBeTruthy();
    });

    fireEvent.click(screen.getByRole("button", { name: "About" }));

    const identity = await screen.findByTestId("about-identity");
    expect(identity.textContent).toContain("canonsim-workbench-gateway");
    expect(identity.textContent).toContain("canon_workbench_gateway@0.1");
    expect(identity.textContent).toContain("LOOPBACK");
    expect(identity.textContent).toContain("not required (loopback)");
    // The full registry, verbatim: the honest count + the chips
    // (the model work kinds ride run.start, never the registry).
    expect(screen.getByTestId("about-operations-count").textContent).toBe("21 registered");
    expect(identity.textContent).toContain("chat.send");
    expect(identity.textContent).toContain("model.load");
    expect(identity.textContent).toContain("observatory.read");

    // The wire law: app.status carried NO arguments and NO session;
    // the settings document was NOT re-read (the container's one
    // mount read is still the only backend.settings dispatch).
    const calls = callsOf(fetchMock);
    const statusCalls = calls.filter((body) => body["operation"] === "app.status");
    expect(statusCalls.length).toBe(1);
    expect(statusCalls[0]!["arguments"]).toBeUndefined();
    expect(statusCalls[0]!["session_id"]).toBeUndefined();
    expect(calls.filter((body) => body["operation"] === "backend.settings").length).toBe(1);

    // The Deployment form is unmounted (the mounting discipline —
    // only the active section renders).
    expect(screen.queryByLabelText(/llama_server_exe/i)).toBeNull();
    // No polling: the identity does not change under the reader.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("the DRAFT SURVIVES a section switch (the draft's owner is the SURFACE, never the form section)", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("backend_settings_read_ok")))
      .mockResolvedValueOnce(json(fixture("app_status_composition")));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByLabelText(/no_webui/i)).toBeTruthy();
    });

    // The REQUEST in flight: a draft edit, unsaved.
    fireEvent.click(screen.getByLabelText(/no_webui/i));
    expect(screen.getByTestId("settings-dirty").textContent).toContain("DRAFT");

    // Away to About and back.
    fireEvent.click(screen.getByRole("button", { name: "About" }));
    await screen.findByTestId("about-identity");
    fireEvent.click(screen.getByRole("button", { name: "Deployment" }));

    // The forbidden collapse, falsified: the section switch never
    // dropped the user's REQUEST — the draft is intact, the save
    // still armed.
    await waitFor(() => {
      expect(screen.getByTestId("settings-dirty").textContent).toContain("DRAFT");
    });
    expect((screen.getByLabelText(/no_webui/i) as HTMLInputElement).checked).toBe(false);
    expect(screen.getByRole("button", { name: "save changes" }).hasAttribute("disabled")).toBe(false);

    // The settings document was read exactly ONCE (the container's
    // mount read; the section switches never re-read it) — and the
    // identity read exactly once (one About mount).
    expect(callsOf(fetchMock).filter((body) => body["operation"] === "backend.settings").length).toBe(1);
    expect(callsOf(fetchMock).filter((body) => body["operation"] === "app.status").length).toBe(1);
  });

  it("a remounted About re-reads its evidence (the mounting discipline); the identity never polls", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("backend_settings_read_ok")))
      .mockResolvedValueOnce(json(fixture("app_status_composition")))
      .mockResolvedValueOnce(json(fixture("app_status_composition")));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByLabelText(/llama_server_exe/i)).toBeTruthy();
    });

    // About → Deployment → About: the second About mount re-reads
    // (a remounted section re-reads its evidence — never a cache).
    fireEvent.click(screen.getByRole("button", { name: "About" }));
    await screen.findByTestId("about-identity");
    fireEvent.click(screen.getByRole("button", { name: "Deployment" }));
    await waitFor(() => {
      expect(screen.getByLabelText(/llama_server_exe/i)).toBeTruthy();
    });
    fireEvent.click(screen.getByRole("button", { name: "About" }));
    await screen.findByTestId("about-identity");

    expect(callsOf(fetchMock).filter((body) => body["operation"] === "app.status").length).toBe(2);
    // No polling: the count stays.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });

  it("the About TRANSPORT lane: the honest re-read note, never 'rejected'", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("backend_settings_read_ok")))
      .mockRejectedValueOnce(new TypeError("fetch failed"));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByLabelText(/llama_server_exe/i)).toBeTruthy();
    });

    fireEvent.click(screen.getByRole("button", { name: "About" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("identity read TRANSPORT");
    expect(banner.textContent).toContain("the re-read is your explicit retry");
    // G4: no auto-retry — the dispatch count stays.
    await new Promise((resolve) => setTimeout(resolve, 40));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("the About MISMATCH lane: reported, never coerced (a fabricated identity document is a contract violation)", async () => {
    // A response envelope whose result misses `service` — the
    // strict schema rejects it at the client boundary (§3's law:
    // unknown/missing keys are contract violations, not noise).
    const mismatch = {
      operation_id: "mismatch-probe",
      result: {
        contract: "canon_workbench_gateway@0.1",
        exposure: "LOOPBACK",
        auth_required: false,
        operations: ["app.status"],
      },
      status: "OK",
    };
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(json(fixture("backend_settings_read_ok")))
      .mockResolvedValueOnce(json(mismatch));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByLabelText(/llama_server_exe/i)).toBeTruthy();
    });

    fireEvent.click(screen.getByRole("button", { name: "About" }));

    const banner = await screen.findByRole("alert");
    expect(banner.textContent).toContain("identity read CONTRACT MISMATCH");
    expect(banner.textContent).toContain("reported, never coerced");
    // The fabricated document never rendered.
    expect(screen.queryByTestId("about-identity")).toBeNull();
  });

  it("the inf-1 pointer renders: the generation controls live in the Inference surface, never a Settings subsection", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(json(fixture("backend_settings_read_ok")));
    mountSettings(fetchMock);

    await waitFor(() => {
      expect(screen.getByTestId("settings-inf1-note").textContent).toContain("Inference");
    });
    expect(screen.getByTestId("settings-inf1-note").textContent).toContain("Settings ≠ Inference Control");
    // And no Inference subsection ever appears in the section nav.
    const tabs = [
      ...screen.getByRole("navigation", { name: "Settings sections" }).querySelectorAll("button"),
    ].map((button) => button.textContent);
    expect(tabs).not.toContain("Inference");
    expect(tabs).not.toContain("Appearance");
  });
});
