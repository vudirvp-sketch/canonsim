/**
 * The translation-boundary proof (i18n-1 band-1, FRONTEND_UIUX_LAW
 * §17 — the ONE boundary; the row's acceptance laws, browser-less
 * band — the live layout half stays RUNTIME evidence, owner-side):
 *
 * - the DEFAULT locale resolves the catalog byte-for-byte (the
 *   standing suites never call setLang — they observe EN exactly);
 * - a SECOND catalog switches the RENDERED strings (a real migrated
 *   surface re-renders translated through `tr`, never a parallel
 *   component tree);
 * - a PARTIAL overlay falls back to the base for its missing keys
 *   (a half-translated surface stays honest, never blank);
 * - `{param}` interpolation substitutes; an absent param keeps its
 *   placeholder visible (never a silent drop);
 * - `formatNumber`/`formatClock` are locale-aware and owned by the
 *   boundary — a surface never hand-joins a locale format;
 * - a LONG CYRILLIC label renders complete through the boundary
 *   (the render half of the Cyrillic-safety law; the layout/metrics
 *   half is RUNTIME evidence — jsdom cannot measure wrapping).
 */
import { afterEach, describe, expect, it } from "vitest";
import { act, cleanup, render, screen } from "@testing-library/react";
import type { ReactNode } from "react";

import { Shell } from "../../src/features/shell/Shell.tsx";
import type { DiagnosticSurface, ProductRoute } from "../../src/features/shell/Shell.tsx";
import {
  addCatalog,
  currentLanguage,
  formatClock,
  formatNumber,
  setLang,
  subscribeLanguage,
  tr,
  useLanguage,
} from "../../src/i18n/index.ts";
import type { Catalog } from "../../src/i18n/index.ts";

afterEach(() => {
  cleanup();
  setLang("en");
});

/** A deliberately PARTIAL Russian overlay: some keys translated,
 * the rest proving the fallback law. */
const RU: Catalog = {
  "shell.diagnostics": "Диагностика",
  "shell.empty": "продуктовые поверхности не зарегистрированы",
  "shell.diagnosticsHint":
    "Инженерные поверхности — шлюз, жизненный цикл сессии, нагрузочный зонд",
};

const SYNTH_ROUTES: readonly ProductRoute[] = [
  { id: "one", label: "One", hint: "hint one", element: <div data-testid="pane-one" /> },
];
const SYNTH_DIAGNOSTICS: readonly DiagnosticSurface[] = [
  { id: "gateway", label: "Gateway", hint: "hint gateway", element: <div data-testid="diag-gateway" /> },
];

describe("the default locale (the standing suites' band)", () => {
  it("resolves the catalog byte-for-byte; the default language is en", () => {
    expect(currentLanguage()).toBe("en");
    expect(tr("app.title")).toBe("CanonSim Workbench");
    expect(tr("settings.save.saving", { fields: "no_webui" })).toBe("saving no_webui…");
  });

  it("interpolates params; an absent param keeps its placeholder", () => {
    expect(tr("app.banner.createFailed", { error: "ECONNREFUSED" })).toBe(
      "session.create failed: ECONNREFUSED — the gateway may be down (start it: python scripts/workbench_app.py)",
    );
    // An absent param stays visible as its placeholder — the
    // failure is a readable template, never a silent drop.
    expect(tr("app.banner.createFailed", {})).toContain("{error}");
  });
});

describe("a second catalog (the row's acceptance law)", () => {
  it("switches the RENDERED strings of a migrated surface", () => {
    addCatalog("ru", RU);
    setLang("ru");

    // The shell's honest empty state, now Russian through the boundary.
    render(<Shell routes={[]} diagnostics={SYNTH_DIAGNOSTICS} />);
    expect(screen.getByText(RU["shell.empty"] as string)).toBeTruthy();

    // The rail's Diagnostics entry, re-rendered translated — the
    // same component, never a parallel tree.
    cleanup();
    render(<Shell routes={SYNTH_ROUTES} diagnostics={SYNTH_DIAGNOSTICS} />);
    expect(screen.getByRole("button", { name: "Диагностика" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Diagnostics" })).toBeNull();
  });

  it("falls back to the base for keys the overlay does not carry", () => {
    addCatalog("ru", RU);
    setLang("ru");
    // Translated key resolves from the overlay…
    expect(tr("shell.empty")).toBe(RU["shell.empty"]);
    // …an untranslated key keeps the EN base — never blank.
    expect(tr("app.title")).toBe("CanonSim Workbench");
  });

  it("a long Cyrillic label renders COMPLETE through the boundary (the render half)", () => {
    addCatalog("ru", {
      "shell.empty":
        "продуктовые поверхности пока не зарегистрированы — очень длинная кириллическая строка для проверки того, что граница переноса не обрезает текст",
    });
    setLang("ru");
    render(<Shell routes={[]} diagnostics={SYNTH_DIAGNOSTICS} />);
    const paragraph = screen.getByText(/кириллическая строка/);
    expect(paragraph.textContent).toBe(
      "продуктовые поверхности пока не зарегистрированы — очень длинная кириллическая строка для проверки того, что граница переноса не обрезает текст",
    );
  });
});

describe("the locale-aware formatters (owned by the same module)", () => {
  it("formatNumber is locale-aware: ru differs from the en form", () => {
    const en = formatNumber(1234.5);
    setLang("ru");
    const ru = formatNumber(1234.5);
    expect(en).toBe("1,234.5");
    // ru: comma decimal, non-comma group separator (U+00A0 space).
    expect(ru).toContain(",");
    expect(ru).not.toBe(en);
  });

  it("formatClock renders the UTC HH:MM:SS of the instant — machine-independent", () => {
    const iso = "2026-10-25T03:21:05.123Z";
    expect(formatClock(iso)).toContain("03:21:05");
    setLang("ru");
    // The zone stays UTC by construction; the locale owns only the
    // digits/separators form — the reading is stable across machines.
    expect(formatClock(iso)).toContain("03:21:05");
  });
});

describe("the `lang` plumbing (i18n-1's closing slice, iter-408)", () => {
  it("subscribeLanguage notifies on a real change only; unsubscribe stops it", () => {
    const seen: string[] = [];
    const unsubscribe = subscribeLanguage(() => seen.push(currentLanguage()));
    setLang("ru");
    setLang("ru"); // idempotent — no second notification
    expect(seen).toEqual(["ru"]);
    unsubscribe();
    setLang("en");
    expect(seen).toEqual(["ru"]);
  });

  it("useLanguage re-renders a mounted surface on the language change (the selector's engine)", () => {
    function Probe(): ReactNode {
      return <>lang={useLanguage()}</>;
    }
    function Host(): ReactNode {
      return (
        <p data-testid="lang-probe">
          <Probe />
        </p>
      );
    }
    render(<Host />);
    expect(screen.getByTestId("lang-probe").textContent).toBe("lang=en");
    act(() => {
      setLang("ru");
    });
    expect(screen.getByTestId("lang-probe").textContent).toBe("lang=ru");
    // The snapshot is the module's language — no local copy to desync.
    expect(currentLanguage()).toBe("ru");
  });
});
