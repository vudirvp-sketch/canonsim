/**
 * The Shell/IA integration proof (iter-297 / D-247, the IA repair), in
 * the browser-less band (jsdom + testing-library; the live evidence
 * rides the iteration report). Two bands:
 *
 * 1. The SHELL mechanism (rendered directly with synthetic routes —
 *    the shell is presentation-only, so no gateway is involved):
 *    - the rail exposes ONLY the product routes + ONE Diagnostics
 *      entry — the navigation contract (FRONTEND_UIUX_LAW §2.1);
 *    - diagnostic surfaces NEVER appear in the rail (their labels
 *      live in the workspace's own secondary nav, and only after the
 *      Diagnostics entry is opened);
 *    - exactly ONE active workspace renders, and ONLY the active
 *      surface mounts (a switch unmounts the previous surface —
 *      boundedness, unchanged from the pane form);
 *    - an empty registry is an honest empty state, never a fake nav.
 *
 * 2. The COMPOSITION ROOT's split (the real App rendered over a
 *    fixture gateway): the rail carries exactly the approved route
 *    labels (Trajectory / Observatory / Settings + Diagnostics) — the
 *    Session lifecycle / Gateway / Load probe labels appear ONLY
 *    inside the diagnostics secondary nav; the header carries the
 *    identity strip and NO engineering prose (the IA acceptance
 *    floor, as DOM assertions).
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import { App } from "../../src/app/composition/App.tsx";
import { Shell } from "../../src/features/shell/Shell.tsx";
import type { DiagnosticSurface, ProductRoute } from "../../src/features/shell/Shell.tsx";

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

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

/** The parsed request bodies, in dispatch order. */
function callsOf(fetchMock: ReturnType<typeof vi.fn>): Record<string, unknown>[] {
  return fetchMock.mock.calls.map(
    (args) => JSON.parse(String(args[1]?.body)) as Record<string, unknown>,
  );
}

/* ------------------------------------------------------------------ */
/* Band 1 — the shell mechanism (synthetic routes, no gateway)         */
/* ------------------------------------------------------------------ */

const SYNTH_ROUTES: readonly ProductRoute[] = [
  { id: "one", label: "One", hint: "hint one", element: <div data-testid="pane-one" /> },
  { id: "two", label: "Two", hint: "hint two", element: <div data-testid="pane-two" /> },
  {
    id: "settings",
    label: "Settings",
    hint: "hint settings",
    pinned: true,
    element: <div data-testid="pane-settings" />,
  },
];

const SYNTH_DIAGNOSTICS: readonly DiagnosticSurface[] = [
  { id: "gateway", label: "Gateway", hint: "hint gateway", element: <div data-testid="diag-gateway" /> },
  { id: "probe", label: "Load probe", hint: "hint probe", element: <div data-testid="diag-probe" /> },
];

function railButtons(): HTMLElement {
  return screen.getByRole("navigation", { name: "Primary navigation" });
}

describe("the shell mechanism (the navigation contract, FRONTEND_UIUX_LAW §2.1)", () => {
  it("the rail exposes ONLY the product routes + one Diagnostics entry", () => {
    render(<Shell routes={SYNTH_ROUTES} diagnostics={SYNTH_DIAGNOSTICS} />);

    const rail = railButtons();
    const labels = within(rail)
      .getAllByRole("button")
      .map((button) => button.textContent);
    expect(labels).toEqual(["One", "Two", "Settings", "Diagnostics"]);
  });

  it("diagnostic labels NEVER appear in the rail — only behind the entry", () => {
    render(<Shell routes={SYNTH_ROUTES} diagnostics={SYNTH_DIAGNOSTICS} />);

    const rail = railButtons();
    expect(within(rail).queryByRole("button", { name: "Gateway" })).toBeNull();
    expect(within(rail).queryByRole("button", { name: "Load probe" })).toBeNull();
    expect(screen.queryByTestId("diag-gateway")).toBeNull();

    fireEvent.click(within(rail).getByRole("button", { name: "Diagnostics" }));

    // The secondary nav appears INSIDE the workspace, never the rail.
    const secondary = screen.getByRole("navigation", { name: "Diagnostic surfaces" });
    expect(within(secondary).getByRole("button", { name: "Gateway" })).toBeTruthy();
    expect(within(secondary).getByRole("button", { name: "Load probe" })).toBeTruthy();
    expect(within(rail).queryByRole("button", { name: "Gateway" })).toBeNull();
  });

  it("exactly ONE active workspace renders and ONLY the active surface mounts", () => {
    render(<Shell routes={SYNTH_ROUTES} diagnostics={SYNTH_DIAGNOSTICS} />);

    expect(screen.getAllByTestId("active-workspace")).toHaveLength(1);
    expect(screen.getByTestId("pane-one")).toBeTruthy();
    expect(screen.queryByTestId("pane-two")).toBeNull();
    expect(screen.queryByTestId("diag-gateway")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "Two" }));
    expect(screen.getAllByTestId("active-workspace")).toHaveLength(1);
    expect(screen.getByTestId("pane-two")).toBeTruthy();
    // The previous surface UNMOUNTS (boundedness: only the active mounts).
    expect(screen.queryByTestId("pane-one")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "Settings" }));
    expect(screen.getByTestId("pane-settings")).toBeTruthy();
    expect(screen.queryByTestId("pane-two")).toBeNull();
  });

  it("entering diagnostics unmounts the product route; a sub-switch unmounts the previous diagnostic surface", () => {
    render(<Shell routes={SYNTH_ROUTES} diagnostics={SYNTH_DIAGNOSTICS} />);

    fireEvent.click(screen.getByRole("button", { name: "Diagnostics" }));
    expect(screen.getByTestId("diag-gateway")).toBeTruthy();
    expect(screen.queryByTestId("pane-one")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "Load probe" }));
    expect(screen.getByTestId("diag-probe")).toBeTruthy();
    expect(screen.queryByTestId("diag-gateway")).toBeNull();
    // The rail's product routes stay reachable the whole time.
    expect(screen.getByRole("button", { name: "One" })).toBeTruthy();
  });

  it("leaving diagnostics closes the secondary nav and restores the product workspace", () => {
    render(<Shell routes={SYNTH_ROUTES} diagnostics={SYNTH_DIAGNOSTICS} />);

    fireEvent.click(screen.getByRole("button", { name: "Diagnostics" }));
    expect(screen.getByRole("navigation", { name: "Diagnostic surfaces" })).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "Two" }));
    expect(screen.queryByRole("navigation", { name: "Diagnostic surfaces" })).toBeNull();
    expect(screen.queryByTestId("diag-gateway")).toBeNull();
    expect(screen.getByTestId("pane-two")).toBeTruthy();
  });

  it("the initial route honors initialRouteId", () => {
    render(<Shell routes={SYNTH_ROUTES} diagnostics={SYNTH_DIAGNOSTICS} initialRouteId="two" />);
    expect(screen.getByTestId("pane-two")).toBeTruthy();
    expect(screen.queryByTestId("pane-one")).toBeNull();
  });

  it("an empty route registry is an honest empty state", () => {
    render(<Shell routes={[]} diagnostics={SYNTH_DIAGNOSTICS} />);
    expect(screen.getByText("no product surfaces registered")).toBeTruthy();
  });
});

/* ------------------------------------------------------------------ */
/* Band 2 — the composition root's split (the real App, fixture gateway) */
/* ------------------------------------------------------------------ */

/** A routing fetch mock: each op answers its live-captured fixture. */
function gatewayRouter(ops: Record<string, unknown>): ReturnType<typeof vi.fn> {
  return vi.fn(async (_input: unknown, init?: RequestInit) => {
    const body = JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>;
    const op = String(body["operation"] ?? "");
    const doc = ops[op];
    return json(doc ?? { status: "REJECTED", rejection: "UNKNOWN_OPERATION", operation_id: "op_router_miss" });
  });
}

const APP_OPS: Record<string, unknown> = {
  "session.create": fixture("session_create_ok"),
  "session.events": fixture("session_events_ok"),
  "session.get": fixture("session_get_ok"),
  "app.status": fixture("app_status_ok"),
  "backend.settings": fixture("backend_settings_read_ok"),
  "observatory.runs": fixture("observatory_runs_ok"),
  "observatory.read": fixture("observatory_read_ok"),
  "model.list": fixture("model_list_ok"),
  "model.states": fixture("model_states_ok"),
  "inference.read": fixture("inference_read_ok"),
};

describe("the composition root's registry split (the IA acceptance floor)", () => {
  it("the rail carries exactly the approved routes — Chat at the HEAD; diagnostics never appear as rail peers", async () => {
    const fetchMock = gatewayRouter(APP_OPS);
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    // The tab's session mints (session.create) before the shell settles.
    await waitFor(() => {
      // session.create answered: the id is a real id, never "creating…" / "—".
      expect(screen.getByTestId("session-id").textContent).toMatch(/^[0-9a-f]{16,}$/);
    });

    const rail = railButtons();
    const labels = within(rail)
      .getAllByRole("button")
      .map((button) => button.textContent);
    expect(labels).toEqual(["Chat", "Trajectory", "Observatory", "Settings", "Diagnostics"]);
    // The proof instruments are NOT rail items.
    for (const forbidden of ["Session lifecycle", "Gateway", "Load probe"]) {
      expect(within(rail).queryByRole("button", { name: forbidden })).toBeNull();
    }
  });

  it("the product chrome carries the identity strip, not engineering prose", async () => {
    const fetchMock = gatewayRouter(APP_OPS);
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await waitFor(() => {
      // session.create answered: the id is a real id, never "creating…" / "—".
      expect(screen.getByTestId("session-id").textContent).toMatch(/^[0-9a-f]{16,}$/);
    });

    expect(screen.getByRole("heading", { level: 1, name: "CanonSim Workbench" })).toBeTruthy();
    // The identity strip's honest state labels stay (the header strip
    // and the live surface may both carry one — state, never prose)…
    expect(screen.getAllByText("DISCONNECTED").length).toBeGreaterThan(0);
    // …the architecture essays do not (the IA floor's prose row).
    expect(screen.queryByText(/untrusted presentation client/i)).toBeNull();
    expect(screen.queryByText(/only the active surface mounts/i)).toBeNull();
    expect(screen.queryByText(/no cross-tab store/i)).toBeNull();
  });

  it("the diagnostics entry opens the secondary nav; the Gateway surface answers app.status", async () => {
    const fetchMock = gatewayRouter(APP_OPS);
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await waitFor(() => {
      // session.create answered: the id is a real id, never "creating…" / "—".
      expect(screen.getByTestId("session-id").textContent).toMatch(/^[0-9a-f]{16,}$/);
    });

    fireEvent.click(screen.getByRole("button", { name: "Diagnostics" }));
    const secondary = screen.getByRole("navigation", { name: "Diagnostic surfaces" });
    expect(within(secondary).getByRole("button", { name: "Session lifecycle" })).toBeTruthy();

    fireEvent.click(within(secondary).getByRole("button", { name: "Gateway" }));
    await waitFor(() => {
      expect(callsOf(fetchMock).some((body) => body["operation"] === "app.status")).toBe(true);
    });
    expect(screen.queryByRole("navigation", { name: "Diagnostic surfaces" })).toBeTruthy();
  });

  it("a product route still mounts its surface (Settings over the CONFIG store)", async () => {
    const fetchMock = gatewayRouter(APP_OPS);
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await waitFor(() => {
      // session.create answered: the id is a real id, never "creating…" / "—".
      expect(screen.getByTestId("session-id").textContent).toMatch(/^[0-9a-f]{16,}$/);
    });

    fireEvent.click(screen.getByRole("button", { name: "Settings" }));
    await waitFor(() => {
      expect(screen.getByText(/CONFIG · USER/i)).toBeTruthy();
    });
    await waitFor(() => {
      expect(callsOf(fetchMock).some((body) => body["operation"] === "backend.settings")).toBe(true);
    });
    // Exactly one workspace the whole time.
    expect(screen.getAllByTestId("active-workspace")).toHaveLength(1);
  });

  it("the Chat product route mounts its surface (the conversation world's three context READs)", async () => {
    const fetchMock = gatewayRouter(APP_OPS);
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);

    await waitFor(() => {
      // session.create answered: the id is a real id, never "creating…" / "—".
      expect(screen.getByTestId("session-id").textContent).toMatch(/^[0-9a-f]{16,}$/);
    });

    fireEvent.click(screen.getByRole("button", { name: "Chat" }));
    await waitFor(() => {
      expect(screen.getByRole("region", { name: /Chat — the conversation world/i })).toBeTruthy();
    });
    await waitFor(() => {
      // The header's three session-free context READs dispatched.
      expect(callsOf(fetchMock).some((body) => body["operation"] === "model.list")).toBe(true);
      expect(callsOf(fetchMock).some((body) => body["operation"] === "model.states")).toBe(true);
      expect(callsOf(fetchMock).some((body) => body["operation"] === "inference.read")).toBe(true);
    });
    // Exactly one workspace the whole time.
    expect(screen.getAllByTestId("active-workspace")).toHaveLength(1);
  });
});
