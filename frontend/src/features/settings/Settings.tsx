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
 * - **Appearance** (BOUND, never a fabricated empty section) — no
 *   persisted appearance store exists; browser storage is never
 *   truth (the guard's R3 row); an in-memory preference would die on
 *   remount (only the active surface mounts). The token system is
 *   the design's own law (VISUAL_SYSTEM_UI), not a user preference.
 *   A named standing boundary, like the import form's native picker.
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
type SectionId = "deployment" | "about";

export function Settings(props: SettingsProps): ReactNode {
  const settings = useSettings({
    client: props.client,
    sessionId: props.sessionId,
  });
  // The active section — the surface's allowed local UI state (§7's
  // allowance, the shell-focus precedent); it resets to Deployment on
  // remount (the mounting law's honest form).
  const [section, setSection] = useState<SectionId>("deployment");

  // The mount READ — exactly one dispatch at the CONTAINER (the
  // section switches never re-read the settings document; refresh's
  // identity is stable, the deps list is empty by design).
  useEffect(() => {
    void settings.refresh();
  }, []);

  return (
    <section className={props.className ?? "surface"} aria-label="Settings — launch configuration">
      <header className="surface-header">
        <h2>
          Settings <span className="tag tag-config">CONFIG · USER</span>
        </h2>
        <p className="surface-note" data-testid="settings-inf1-note">
          the managed spawn&rsquo;s DEPLOYMENT knobs + the gateway identity — persisted by the
          store, effective at the NEXT spawn; the semantic generation controls live in the
          Inference surface (Settings ≠ Inference Control)
        </p>
      </header>

      {/* The secondary navigation — this surface's own concern (§2.1),
          the Diagnostics area's in-workspace tab precedent. */}
      <nav className="settings-sections" aria-label="Settings sections">
        <button
          className={section === "deployment" ? "section-tab section-tab-active" : "section-tab"}
          aria-current={section === "deployment" ? "page" : undefined}
          onClick={() => setSection("deployment")}
        >
          Deployment
        </button>
        <button
          className={section === "about" ? "section-tab section-tab-active" : "section-tab"}
          aria-current={section === "about" ? "page" : undefined}
          onClick={() => setSection("about")}
        >
          About
        </button>
      </nav>

      {section === "deployment" ? (
        <DeploymentSection settings={settings} sessionId={props.sessionId} />
      ) : (
        <SettingsAbout client={props.client} />
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
    <section className="settings-section" aria-label="Settings — Deployment">
      <header className="surface-header">
        <h3>
          Deployment <span className="tag tag-config">LAUNCH · NEXT-SPAWN</span>
        </h3>
        <p className="surface-note">
          the managed llama-server spawn&rsquo;s knobs — the executable preference, the web-UI
          surface, the raw extra_args hatch; the raw hatch belongs HERE (disclosure layers are
          not semantic classes — one document, one draft, one Save)
        </p>
      </header>
      <LoadLane load={load} />
      {draft !== null ? (
        <>
          <div className="strip" data-testid="settings-context">
            <span>
              applies <code>{load.kind === "LOADED" ? load.result.applies : "next-spawn"}</code>
            </span>
            <span>
              managed{" "}
              <code>{load.kind === "LOADED" ? (load.result.managed_live ? "LIVE" : "down") : "—"}</code>
            </span>
            {settings.dirty ? (
              <span className="tag tag-config" data-testid="settings-dirty">
                DRAFT — unsaved changes
              </span>
            ) : (
              <span className="tag">draft matches the observed document</span>
            )}
            {props.sessionId === null ? (
              <span className="freshness freshness-stale">no session — save disabled</span>
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
                llama_server_exe <em>(the executable preference; empty = auto-discovery)</em>
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
                no_webui <em>(llama-server&rsquo;s own web-UI surface on the spawned process)</em>
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
                extra_args <em>(the RAW compatibility/debug escape hatch — duplicate flag
                ownership rejects loudly at the compile step)</em>
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
              re-read settings
            </button>
            <button onClick={settings.resetDraft} disabled={formDisabled || !settings.dirty}>
              reset draft
            </button>
            <button
              onClick={() => void settings.saveChanges()}
              disabled={formDisabled || !settings.dirty || props.sessionId === null}
            >
              save changes
            </button>
            <span className="controls-note">
              save sends ONLY the changed fields (absent fields unchanged) with a fresh
              idempotency key — one explicit attempt, never a blind retry
            </span>
          </div>

          <SaveLane save={save} />

          {/* OBSERVED / the §18 EFFECTIVE display — the composition
              root's compiled preview, read-only, never client-computed. */}
          {load.kind === "LOADED" ? (
            <div className="preview-block">
              <h3>the next spawn&rsquo;s compiled command (the composition root&rsquo;s view)</h3>
              <pre className="command-preview" data-testid="settings-preview">
                {load.result.command_preview ?? "(no preview — the composition did not inject one)"}
              </pre>
            </div>
          ) : null}
        </>
      ) : load.kind === "NOT_LOADED" || load.kind === "LOADING" ? (
        <p className="empty">the settings document not read yet…</p>
      ) : null}
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
        settings read TRANSPORT · {load.failure} — the gateway may be down; the re-read is
        your explicit retry
      </div>
    );
  }
  if (load.kind === "MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        settings read CONTRACT MISMATCH · {load.error} — reported, never coerced
      </div>
    );
  }
  if (load.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        settings read REJECTED · {load.rejection}: {load.reason ?? "(no reason)"}
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
    return <p className="empty">saving {save.requested.join(", ")}…</p>;
  }
  if (save.kind === "SAVED") {
    return (
      <div className="banner banner-accepted" data-testid="settings-save-closure">
        SAVED — requested [{save.requested.join(", ")}] accepted; EFFECTIVE at the NEXT
        managed spawn (applies: {save.result.applies})
        {save.result.managed_live
          ? " — the LIVE server keeps its flags until unloaded"
          : ""}
      </div>
    );
  }
  if (save.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        save REJECTED · {save.rejection}: {save.reason ?? "(no reason)"} — the requested
        [{save.requested.join(", ")}] was NOT applied; the draft is preserved (your
        decision, never an auto-retry)
      </div>
    );
  }
  if (save.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        save TRANSPORT · {save.failure} — if the request was sent, the outcome is UNKNOWN
        (no blind retry); re-read to reconcile, the draft is preserved
      </div>
    );
  }
  return (
    <div className="banner banner-error" role="alert">
      save CONTRACT MISMATCH · {save.error} — reported, never coerced
    </div>
  );
}
