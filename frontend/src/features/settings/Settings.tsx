/**
 * The Settings surface (Phase 3's third row; iter-301 grows it into
 * its own SECONDARY NAVIGATION — the external IA verdict's step 5,
 * reconciled with the law by the D-246 method): the CONFIG world now
 * carries TWO sections, each with real content — never a feature
 * directory (§2's own named failure mode; a section without a live
 * document is a fabrication, not a placeholder).
 *
 * The D-246 reconciliation of the verdict's
 * General/Deployment/Appearance/Advanced shape (donor informs, law
 * decides):
 * - **Deployment** (KEEP) — the launch-settings DEPLOYMENT world over
 *   the two EXISTING gateway ops: `backend.settings` (the READ) +
 *   `backend.settings.update` (the closed partial MUTATION). The
 *   verdict's "Advanced" DISSOLVES here: `extra_args` is the same
 *   document's raw escape hatch, and §19's law is explicit —
 *   disclosure layers are not semantic classes; one document, one
 *   draft, one Save carrying only the delta.
 * - **About** (the verdict's "General", re-scoped to what exists) —
 *   the gateway's own identity document, READ-ONLY over the EXISTING
 *   session-free `app.status` READ. "General" implied editable
 *   general preferences — none exist (the closed three-field set is
 *   the store's own law; the UI never invents a fourth field).
 * - **Appearance** (OPENED by i18n-1's `lang` row, iter-408) — the
 *   ONE real appearance preference that exists: the interface
 *   language. It is session-scoped BY CONSTRUCTION (the boundary's
 *   module-level language — no browser storage, the guard's R3 row),
 *   and the section's note says exactly that: it returns to English
 *   on reload. The visual tokens remain the design's own law
 *   (VISUAL_SYSTEM_UI), not a user preference — the section carries
 *   the language and nothing else, never a fabricated theme picker.
 *   The selector re-renders every mounted surface through
 *   `useLanguage` (the i18n boundary's subscription), not a reload.
 * - inf-1 STANDS: the semantic generation controls live in the
 *   Inference surface — a separate surface, NEVER a Settings
 *   subsection (the header note carries the pointer).
 *
 * The secondary nav is THIS surface's own concern (§2.1: "its
 * secondary navigation is its own surface's concern") — the
 * Diagnostics area's in-workspace tab precedent, mirrored. The
 * active section is the surface's allowed local UI state (§7's
 * allowance); a switch unmounts the inactive section (the mounting
 * discipline — a remounted section re-reads its evidence), and the
 * SHELL-level switch still drops everything (the surface unmounts,
 * the law's honest form).
 *
 * The draft's owner is the CONTAINER: `useSettings` lives here, the
 * Deployment section is its projection — so an intra-surface section
 * switch never drops the user's REQUEST in flight (the draft is
 * presentation state owned by the SURFACE, not by the form section;
 * bounded: one document + one draft + one identity read).
 *
 * EFFECTIVE-STATE CLOSURE (FRONTEND_WEB_LAW §8), rendered as the
 * stages it is — never collapsed (unchanged from the row-3 law):
 * - the DRAFT is local presentation state (§7's explicit allowance);
 *   `dirty` is a marker that must reconcile, never an effective-state
 *   claim (`input.value !== EFFECTIVE`);
 * - the Save is ONE explicit dispatch with a FRESH idempotency key
 *   (G4 — no auto-retry, no double-click storm);
 * - on ACCEPTED the returned document is the new OBSERVED baseline
 *   and the draft reconciles to the SERVER's evidence;
 * - EFFECTIVE is the store's own honest law, rendered verbatim:
 *   `applies: next-spawn` — a LIVE server keeps its launch flags
 *   until unloaded (the note rides the document when live);
 * - the command preview is the composition root's compiled view (the
 *   §18 EFFECTIVE display) — read-only, never client-computed.
 */
import { useEffect, useState } from "react";
import type { ReactNode } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import { setLang, tr, useLanguage } from "../../i18n/index.ts";
import type { MessageKey } from "../../i18n/index.ts";
import type { SettingsLoad, SettingsSave, SettingsState } from "./useSettings.ts";
import { useSettings } from "./useSettings.ts";
import { SettingsAbout } from "./SettingsAbout.tsx";

export interface SettingsProps {
  readonly client: GatewayClient;
  /** the UPDATE is session-scoped: null disables the Save honestly. */
  readonly sessionId: string | null;
  readonly className?: string;
}

/** The secondary nav's closed section set — real content only. */
type SectionId = "deployment" | "about" | "appearance";

/** The interface languages the boundary ships as data: the LABEL
 * resolves through the catalog like every other string, so an overlay
 * translates a language name as it translates prose. */
const LANGUAGES = [
  { tag: "en", label: "settings.appearance.lang.en" },
  { tag: "ru", label: "settings.appearance.lang.ru" },
] as const satisfies readonly { readonly tag: string; readonly label: MessageKey }[];

export function Settings(props: SettingsProps): ReactNode {
  const settings = useSettings({
    client: props.client,
    sessionId: props.sessionId,
  });
  // The active section — the surface's allowed local UI state (§7's
  // allowance, the shell-focus precedent); it resets to Deployment on
  // remount (the mounting law's honest form).
  const [section, setSection] = useState<SectionId>("deployment");
  // The surface itself is a language subscriber: the section nav is
  // THIS component's render, so a switch made in Appearance must
  // re-render the nav (and the section, whose own `useLanguage` would
  // otherwise be the only subscriber). `data-lang` is the honest
  // observation hook for the browser band.
  const language = useLanguage();

  // The mount READ — exactly one dispatch at the CONTAINER (the
  // section switches never re-read the settings document; refresh's
  // identity is stable, the deps list is empty by design).
  useEffect(() => {
    void settings.refresh();
  }, []);

  return (
    <section className={props.className ?? "surface"} aria-label={tr("settings.region")} data-lang={language}>
      <header className="surface-header">
        <h2>
          {tr("settings.title")} <span className="tag tag-config">{tr("settings.tag")}</span>
        </h2>
        <p className="surface-note" data-testid="settings-inf1-note">
          {tr("settings.note")}
        </p>
      </header>

      {/* The secondary navigation — this surface's own concern (§2.1),
          the Diagnostics area's in-workspace tab precedent. */}
      <nav className="settings-sections" aria-label={tr("settings.sectionsNav")}>
        <button
          className={section === "deployment" ? "section-tab section-tab-active" : "section-tab"}
          aria-current={section === "deployment" ? "page" : undefined}
          onClick={() => setSection("deployment")}
        >
          {tr("settings.tab.deployment")}
        </button>
        <button
          className={section === "about" ? "section-tab section-tab-active" : "section-tab"}
          aria-current={section === "about" ? "page" : undefined}
          onClick={() => setSection("about")}
        >
          {tr("settings.tab.about")}
        </button>
        <button
          className={section === "appearance" ? "section-tab section-tab-active" : "section-tab"}
          aria-current={section === "appearance" ? "page" : undefined}
          onClick={() => setSection("appearance")}
        >
          {tr("settings.tab.appearance")}
        </button>
      </nav>

      {section === "deployment" ? (
        <DeploymentSection settings={settings} sessionId={props.sessionId} />
      ) : section === "about" ? (
        <SettingsAbout client={props.client} />
      ) : (
        <AppearanceSection />
      )}
    </section>
  );
}

/** The DEPLOYMENT section — the launch-settings store's own document
 * (the closed three-field form, the save closure, the compiled
 * preview). A projection of the container's settings state: the
 * draft survives section switches because its owner never unmounts
 * while the surface is active. */
function DeploymentSection(props: {
  readonly settings: SettingsState;
  readonly sessionId: string | null;
}): ReactNode {
  const { settings } = props;
  const { load, draft, save } = settings;

  const formDisabled = draft === null || settings.busy;

  return (
    <section className="settings-section" aria-label={tr("settings.deployment.region")}>
      <header className="surface-header">
        <h3>
          {tr("settings.deployment.title")}{" "}
          <span className="tag tag-config">{tr("settings.deployment.tag")}</span>
        </h3>
        <p className="surface-note">{tr("settings.deployment.note")}</p>
      </header>
      <LoadLane load={load} />
      {draft !== null ? (
        <>
          <div className="strip" data-testid="settings-context">
            <span>
              {tr("settings.context.applies")}{" "}
              <code>{load.kind === "LOADED" ? load.result.applies : "next-spawn"}</code>
            </span>
            <span>
              {tr("settings.context.managed")}{" "}
              <code>
                {load.kind === "LOADED"
                  ? load.result.managed_live
                    ? tr("settings.context.live")
                    : tr("settings.context.down")
                  : "—"}
              </code>
            </span>
            {settings.dirty ? (
              <span className="tag tag-config" data-testid="settings-dirty">
                {tr("settings.context.draft")}
              </span>
            ) : (
              <span className="tag">{tr("settings.context.clean")}</span>
            )}
            {props.sessionId === null ? (
              <span className="freshness freshness-stale">{tr("settings.context.noSession")}</span>
            ) : null}
          </div>

          {load.kind === "LOADED" && load.result.managed_live && load.result.note !== undefined ? (
            <div className="banner banner-stale" role="note">
              {load.result.note}
            </div>
          ) : null}

          {/* The DRAFT — the closed three-field form. */}
          <form
            className="settings-form"
            onSubmit={(event) => {
              event.preventDefault();
              void settings.saveChanges();
            }}
          >
            <label className="settings-field">
              <span className="settings-label">
                <code>llama_server_exe</code> <em>{tr("settings.field.llamaServer.hint")}</em>
              </span>
              <input
                name="llama_server_exe"
                type="text"
                value={draft.llama_server_exe}
                disabled={formDisabled}
                onChange={(event) => settings.editField("llama_server_exe", event.target.value)}
              />
            </label>
            <label className="settings-field">
              <span className="settings-label">
                <code>no_webui</code> <em>{tr("settings.field.noWebui.hint")}</em>
              </span>
              <input
                name="no_webui"
                type="checkbox"
                checked={draft.no_webui}
                disabled={formDisabled}
                onChange={(event) => settings.editField("no_webui", event.target.checked)}
              />
            </label>
            <label className="settings-field">
              <span className="settings-label">
                <code>extra_args</code> <em>{tr("settings.field.extraArgs.hint")}</em>
              </span>
              <input
                name="extra_args"
                type="text"
                value={draft.extra_args}
                disabled={formDisabled}
                onChange={(event) => settings.editField("extra_args", event.target.value)}
              />
            </label>
          </form>

          <div className="controls">
            <button onClick={() => void settings.refresh()} disabled={settings.busy}>
              {tr("settings.controls.reread")}
            </button>
            <button onClick={settings.resetDraft} disabled={formDisabled || !settings.dirty}>
              {tr("settings.controls.reset")}
            </button>
            <button
              onClick={() => void settings.saveChanges()}
              disabled={formDisabled || !settings.dirty || props.sessionId === null}
            >
              {tr("settings.controls.save")}
            </button>
            <span className="controls-note">{tr("settings.controls.note")}</span>
          </div>

          <SaveLane save={save} />

          {/* OBSERVED / the §18 EFFECTIVE display — the composition
              root's compiled preview, read-only, never client-computed. */}
          {load.kind === "LOADED" ? (
            <div className="preview-block">
              <h3>{tr("settings.preview.title")}</h3>
              <pre className="command-preview" data-testid="settings-preview">
                {load.result.command_preview ?? tr("settings.preview.none")}
              </pre>
            </div>
          ) : null}
        </>
      ) : load.kind === "NOT_LOADED" || load.kind === "LOADING" ? (
        <p className="empty">{tr("settings.empty")}</p>
      ) : null}
    </section>
  );
}

/** The APPEARANCE section — the interface language, the one real
 * appearance preference (i18n-1's `lang` row). The choice is the
 * boundary's own module-level state: it survives a section/surface
 * switch inside the session, dies on reload, and is never written to
 * browser storage (the guard's R3 law). `useLanguage` is what makes
 * the switch visible immediately on every surface that calls it. */
function AppearanceSection(): ReactNode {
  const language = useLanguage();
  return (
    <section className="settings-section" aria-label={tr("settings.appearance.region")}>
      <header className="surface-header">
        <h3>
          {tr("settings.appearance.title")}{" "}
          <span className="tag tag-config">{tr("settings.appearance.tag")}</span>
        </h3>
        <p className="surface-note">{tr("settings.appearance.note")}</p>
      </header>
      <label className="settings-field">
        <span className="settings-label">
          {tr("settings.appearance.lang.label")}{" "}
          <em>{tr("settings.appearance.lang.hint")}</em>
        </span>
        <select
          name="lang"
          value={language}
          onChange={(event) => setLang(event.target.value)}
        >
          {LANGUAGES.map((option) => (
            <option key={option.tag} value={option.tag}>
              {tr(option.label)}
            </option>
          ))}
        </select>
      </label>
    </section>
  );
}

/** The read's four honest lanes — never collapsed into one spinner. */
function LoadLane(props: { readonly load: SettingsLoad }): ReactNode {
  const { load } = props;
  if (load.kind === "NOT_LOADED" || load.kind === "LOADING") return null;
  if (load.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("settings.read.transport", { failure: load.failure })}
      </div>
    );
  }
  if (load.kind === "MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("settings.read.mismatch", { error: load.error })}
      </div>
    );
  }
  if (load.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("settings.read.rejected", {
          rejection: load.rejection,
          reason: load.reason ?? tr("settings.noReason"),
        })}
      </div>
    );
  }
  return null;
}

/** The Save's closure — the stages rendered as stages (§8). */
function SaveLane(props: { readonly save: SettingsSave }): ReactNode {
  const { save } = props;
  if (save.kind === "IDLE") return null;
  if (save.kind === "SAVING") {
    return <p className="empty">{tr("settings.save.saving", { fields: save.requested.join(", ") })}</p>;
  }
  if (save.kind === "SAVED") {
    return (
      <div className="banner banner-accepted" data-testid="settings-save-closure">
        {tr("settings.save.saved", {
          fields: save.requested.join(", "),
          applies: save.result.applies,
        })}
        {save.result.managed_live ? tr("settings.save.savedLive") : ""}
      </div>
    );
  }
  if (save.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("settings.save.rejected", {
          rejection: save.rejection,
          reason: save.reason ?? tr("settings.noReason"),
          fields: save.requested.join(", "),
        })}
      </div>
    );
  }
  if (save.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        {tr("settings.save.transport", { failure: save.failure })}
      </div>
    );
  }
  return (
    <div className="banner banner-error" role="alert">
      {tr("settings.save.mismatch", { error: save.error })}
    </div>
  );
}
