/**
 * useSettings — the Settings surface's read/save state (Phase 3's
 * third row), over the EXISTING gateway ops only:
 * `backend.settings` (the session-free READ) + `backend.settings.update`
 * (the session-scoped closed partial MUTATION). No new route is
 * invented (§3); the store on the Python side stays the one
 * authority — this hook never promotes a draft into effective state.
 *
 * EFFECTIVE-STATE CLOSURE (FRONTEND_WEB_LAW §8, the stages stay
 * distinct — they may coincide, they are never assumed equivalent):
 *
 * ```text
 * REQUESTED  the draft's CHANGED fields the Save sent (the delta)
 * ACCEPTED   what passed the store's validation (the returned doc)
 * EFFECTIVE  what the NEXT managed spawn will use (applies: next-spawn)
 * OBSERVED   the returned document + the compiled command preview
 * PRESENTED  this surface's read document + the preview line
 * ```
 *
 * The forbidden collapses, named: `input.value === EFFECTIVE` (a
 * draft edit is a REQUEST, never a state change); `click === success`
 * (the Save is one dispatch with four honest outcome lanes);
 * `HTTP 200 === semantic success` (a REJECTED document answers 200).
 *
 * G4 (the no-retry law): every explicit Save attempt carries a FRESH
 * `client_request_id`; the hook auto-retries NOTHING. A TRANSPORT
 * failure after send leaves the outcome UNKNOWN — the re-read is the
 * user's explicit reconciliation, and the draft is PRESERVED (the
 * user decides, never the surface).
 *
 * Boundedness: ONE document + ONE draft in memory; no polling, no
 * timers — the settings do not change under the reader (the honest
 * next-spawn law); every read and every save is the user's explicit
 * action. The one-dispatch-at-a-time guard is a ref (the callbacks
 * keep stable identities — the mount READ fires exactly once).
 */
import { useCallback, useRef, useState } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type {
  BackendSettingsResult,
  LaunchSettingsDocument,
  SettingsField,
} from "../../api/gateway/contracts.ts";
import { SETTINGS_FIELDS } from "../../api/gateway/contracts.ts";

/** The read's honest state — the four outcome lanes never collapse. */
export type SettingsLoad =
  | { readonly kind: "NOT_LOADED" }
  | { readonly kind: "LOADING" }
  | { readonly kind: "LOADED"; readonly result: BackendSettingsResult; readonly at: number }
  | {
      readonly kind: "REJECTED";
      readonly rejection: string;
      readonly reason: string | null;
      readonly at: number;
    }
  | { readonly kind: "TRANSPORT"; readonly failure: string; readonly at: number }
  | { readonly kind: "MISMATCH"; readonly error: string; readonly at: number };

/** The last explicit Save's closure — REQUESTED rides every lane (the
 * honest record of what was sent, never inferred from the draft). */
export type SettingsSave =
  | { readonly kind: "IDLE" }
  | { readonly kind: "SAVING"; readonly requested: readonly SettingsField[] }
  | {
      readonly kind: "SAVED";
      readonly requested: readonly SettingsField[];
      readonly result: BackendSettingsResult;
      readonly at: number;
    }
  | {
      readonly kind: "REJECTED";
      readonly requested: readonly SettingsField[];
      readonly rejection: string;
      readonly reason: string | null;
      readonly at: number;
    }
  | {
      readonly kind: "TRANSPORT";
      readonly requested: readonly SettingsField[];
      readonly failure: string;
      readonly at: number;
    }
  | {
      readonly kind: "MISMATCH";
      readonly requested: readonly SettingsField[];
      readonly error: string;
      readonly at: number;
    };

export interface SettingsState {
  /** the OBSERVED document — the store's own truth, never the draft. */
  readonly load: SettingsLoad;
  /** the REQUESTED-to-be (draft form fields — §7's explicit allowance). */
  readonly draft: LaunchSettingsDocument | null;
  /** the last explicit Save's closure lane. */
  readonly save: SettingsSave;
  /** one in-flight dispatch at a time (a read or a save). */
  readonly busy: boolean;
  /** draft differs from the observed document — a presentation marker
   * that must reconcile (never itself an effective-state claim). */
  readonly dirty: boolean;
  readonly refresh: () => Promise<void>;
  readonly editField: (field: SettingsField, value: string | boolean) => void;
  readonly resetDraft: () => void;
  readonly saveChanges: () => Promise<void>;
}

export interface SettingsOptions {
  readonly client: GatewayClient;
  /** the UPDATE is session-scoped: null disables the Save honestly
   * (the READ stays available — it is session-free). */
  readonly sessionId: string | null;
}

/** The REQUESTED delta's mutable form — the wire type's writable
 * twin (the readonly law holds at the boundary; the draft's delta is
 * built locally before it rides the client's typed input). */
type LaunchSettingsChanges = {
  -readonly [K in keyof LaunchSettingsDocument]?: LaunchSettingsDocument[K];
};

export function useSettings(options: SettingsOptions): SettingsState {
  const { client, sessionId } = options;
  const [load, setLoad] = useState<SettingsLoad>({ kind: "NOT_LOADED" });
  const [draft, setDraft] = useState<LaunchSettingsDocument | null>(null);
  const [save, setSave] = useState<SettingsSave>({ kind: "IDLE" });
  const [busy, setBusy] = useState(false);
  // The one-dispatch-at-a-time guard (a ref — the callbacks' identities
  // stay stable, the mount READ fires exactly once, no busy-deps loop).
  const inFlight = useRef(false);

  /** The READ — the store's current document (session-free, no
   * arguments). The draft seeds from the FIRST read only; a later
   * refresh updates the OBSERVED baseline and leaves the draft ALONE
   * (the user's in-flight work stays visible in `dirty` — the
   * divergence is a presentation fact, the reconciliation the user's
   * explicit decision: save or reset). */
  const refresh = useCallback(async (): Promise<void> => {
    if (inFlight.current) return;
    inFlight.current = true;
    setBusy(true);
    setLoad({ kind: "LOADING" });
    try {
      const dispatch = await client.backendSettings();
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        setLoad({ kind: "LOADED", result: dispatch.result, at: Date.now() });
        setDraft((previous) => previous ?? dispatch.result.settings);
      } else if (dispatch.transport === "TRANSPORT") {
        setLoad({
          kind: "TRANSPORT",
          failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
          at: Date.now(),
        });
      } else if (dispatch.transport === "MISMATCH") {
        setLoad({ kind: "MISMATCH", error: dispatch.error, at: Date.now() });
      } else {
        setLoad({
          kind: "REJECTED",
          rejection: dispatch.response.rejection ?? "REJECTED",
          reason: reasonOf(dispatch.response.result),
          at: Date.now(),
        });
      }
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  }, [client]);

  const editField = useCallback(
    (field: SettingsField, value: string | boolean): void => {
      setDraft((previous) => {
        if (previous === null) return previous;
        if (field === "no_webui") {
          return typeof value === "boolean"
            ? { ...previous, no_webui: value }
            : previous;
        }
        if (typeof value !== "string") return previous;
        if (field === "llama_server_exe") {
          return { ...previous, llama_server_exe: value };
        }
        return { ...previous, extra_args: value };
      });
    },
    [],
  );

  const resetDraft = useCallback((): void => {
    setDraft((previous) => {
      if (previous === null || load.kind !== "LOADED") return previous;
      return load.result.settings;
    });
  }, [load]);

  /** The SAVE — one explicit attempt, a fresh idempotency key (G4),
   * only the CHANGED fields on the wire (the store's partial law:
   * absent fields unchanged). On ACCEPTED the returned document is the
   * new OBSERVED baseline and the draft reconciles to it (the
   * server's evidence, never the local projection). On any failure
   * lane the draft is PRESERVED — the user decides. */
  const saveChanges = useCallback(async (): Promise<void> => {
    if (inFlight.current || sessionId === null) return;
    if (load.kind !== "LOADED" || draft === null) return;
    const observed = load.result.settings;
    // The REQUESTED delta — the closed set spelled out (the store's
    // partial law: absent fields unchanged; the wire carries ONLY
    // what the draft changed).
    const changes: LaunchSettingsChanges = {};
    const requested: SettingsField[] = [];
    if (draft.llama_server_exe !== observed.llama_server_exe) {
      changes.llama_server_exe = draft.llama_server_exe;
      requested.push("llama_server_exe");
    }
    if (draft.no_webui !== observed.no_webui) {
      changes.no_webui = draft.no_webui;
      requested.push("no_webui");
    }
    if (draft.extra_args !== observed.extra_args) {
      changes.extra_args = draft.extra_args;
      requested.push("extra_args");
    }
    if (requested.length === 0) return; // nothing REQUESTED — no dispatch
    inFlight.current = true;
    setBusy(true);
    setSave({ kind: "SAVING", requested });
    try {
      const dispatch = await client.backendSettingsUpdate({
        sessionId,
        clientRequestId: `settings-save-${crypto.randomUUID()}`,
        changes,
      });
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        setLoad({ kind: "LOADED", result: dispatch.result, at: Date.now() });
        setDraft(dispatch.result.settings);
        setSave({
          kind: "SAVED",
          requested,
          result: dispatch.result,
          at: Date.now(),
        });
      } else if (dispatch.transport === "TRANSPORT") {
        setSave({
          kind: "TRANSPORT",
          requested,
          failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
          at: Date.now(),
        });
      } else if (dispatch.transport === "MISMATCH") {
        setSave({ kind: "MISMATCH", requested, error: dispatch.error, at: Date.now() });
      } else {
        setSave({
          kind: "REJECTED",
          requested,
          rejection: dispatch.response.rejection ?? "REJECTED",
          reason: reasonOf(dispatch.response.result),
          at: Date.now(),
        });
      }
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  }, [sessionId, load, draft, client]);

  const dirty =
    load.kind === "LOADED" &&
    draft !== null &&
    SETTINGS_FIELDS.some((field) => draft[field] !== load.result.settings[field]);

  return {
    load,
    draft,
    save,
    busy,
    dirty,
    refresh,
    editField,
    resetDraft,
    saveChanges,
  };
}

/** The gateway's reason, honestly typed (unknown on the wire). */
function reasonOf(result: Record<string, unknown> | undefined): string | null {
  const value = result?.["reason"];
  return typeof value === "string" ? value : null;
}
