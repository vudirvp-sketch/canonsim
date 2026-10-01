/**
 * useInference — the Inference WORKSPACE's state (Phase 3's fifth
 * row), over the EXISTING gateway ops only: `inference.read` (the
 * session-free READ — the full resolved control document) +
 * `inference.update` (the session-scoped closed partial MUTATION).
 * No new route is invented (§3); the profile store on the Python
 * side stays the one authority — this hook never promotes a draft
 * into effective state, and never re-encodes the control vocabulary
 * (the editors are data-driven over the read document's own
 * metadata, §21.2's law).
 *
 * EFFECTIVE-STATE CLOSURE (FRONTEND_WEB_LAW §8, the stages stay
 * distinct — they may coincide, they are never assumed equivalent):
 *
 * ```text
 * REQUESTED  the draft's CHANGED keys the Save sent (the delta),
 *            or the preset's transparent values, or the pinned list
 * ACCEPTED   what passed the store's validation (the returned doc)
 * EFFECTIVE  what the NEXT managed spawn will use (applies: next-spawn)
 * OBSERVED   the returned resolved document + the compiled preview
 * PRESENTED  this surface's read document + the preview line
 * ```
 *
 * The forbidden collapses, named: `input.value === EFFECTIVE` (a
 * chip edit is a REQUEST, never a state change — the row's OBSERVED
 * state/reasons stay the resolver's own answer); `click === success`
 * (every update is one dispatch with four honest outcome lanes);
 * `HTTP 200 === semantic success` (a REJECTED document answers 200).
 *
 * G4 (the no-retry law): every explicit update carries a FRESH
 * `client_request_id`; the hook auto-retries NOTHING. A TRANSPORT
 * failure after send leaves the outcome UNKNOWN — the re-read is the
 * user's explicit reconciliation, and the draft is PRESERVED (the
 * user decides, never the surface).
 *
 * The preset law (§14): a preset apply is a PLAIN update — the
 * preset's values ride the wire verbatim (the store validates and
 * merges; the diff was previewed BEFORE the apply), never an opaque
 * mode switch. The apply is guarded on a CLEAN draft: presets never
 * silently modify out-of-scope settings (§21.2) — a dirty draft is
 * the user's unresolved REQUEST, resolved by save or reset first.
 *
 * The pin law (§14): the pinned list is the WORKSPACE section's own
 * concern — a pin/unpin is its own explicit dispatch carrying the
 * WHOLE list (order preserved, the store's own validation), never a
 * profile edit; the profile draft is untouched by it.
 *
 * Boundedness: ONE document + ONE draft in memory; no polling, no
 * timers — the profile does not change under the reader (the honest
 * next-spawn law); every read and every update is the user's
 * explicit action. The one-dispatch-at-a-time guard is a ref (the
 * callbacks keep stable identities — the mount READ fires exactly
 * once).
 */
import { useCallback, useEffect, useRef, useState } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type {
  InferenceDocument,
  InferenceProfileChainItem,
} from "../../api/gateway/contracts.ts";

/** The read's honest state — the lanes never collapse. */
export type InferenceLoad =
  | { readonly kind: "NOT_LOADED" }
  | { readonly kind: "LOADING" }
  | { readonly kind: "LOADED"; readonly result: InferenceDocument; readonly at: number }
  | {
      readonly kind: "REJECTED";
      readonly rejection: string;
      readonly reason: string | null;
      readonly at: number;
    }
  | { readonly kind: "TRANSPORT"; readonly failure: string; readonly at: number }
  | { readonly kind: "MISMATCH"; readonly error: string; readonly at: number };

/** Which explicit action the last update was (the closure's own record). */
export type InferenceUpdateAction = "save" | "preset" | "pin";

/** The last explicit update's closure — the REQUESTED keys ride every
 * lane (the honest record of what was sent, never inferred). */
export type InferenceUpdateLane =
  | { readonly kind: "IDLE" }
  | {
      readonly kind: "UPDATING";
      readonly action: InferenceUpdateAction;
      readonly requested: readonly string[];
    }
  | {
      readonly kind: "UPDATED";
      readonly action: InferenceUpdateAction;
      readonly requested: readonly string[];
      readonly result: InferenceDocument;
      readonly at: number;
    }
  | {
      readonly kind: "REJECTED";
      readonly action: InferenceUpdateAction;
      readonly requested: readonly string[];
      readonly rejection: string;
      readonly reason: string | null;
      readonly at: number;
    }
  | {
      readonly kind: "TRANSPORT";
      readonly action: InferenceUpdateAction;
      readonly requested: readonly string[];
      readonly failure: string;
      readonly at: number;
    }
  | {
      readonly kind: "MISMATCH";
      readonly action: InferenceUpdateAction;
      readonly requested: readonly string[];
      readonly error: string;
      readonly at: number;
    };

/** The REQUEST layer — the draft (§7's explicit allowance: draft
 * form fields, never an effective-state claim). */
export interface InferenceDraft {
  readonly name: string;
  /** field key → the edited value (the observed resolved values + the
   * user's local edits — the editors commit only legal parsed values). */
  readonly values: Readonly<Record<string, unknown>>;
  /** the WHOLE 9-member membership document, in the observed order. */
  readonly chain: readonly InferenceProfileChainItem[];
}

export interface InferenceState {
  /** the OBSERVED document — the resolver's own truth, never the draft. */
  readonly load: InferenceLoad;
  /** the REQUESTED-to-be (the draft). */
  readonly draft: InferenceDraft | null;
  /** the last explicit update's closure lane. */
  readonly update: InferenceUpdateLane;
  /** one in-flight dispatch at a time (a read or an update). */
  readonly busy: boolean;
  /** the draft differs from the observed document — a presentation
   * marker that must reconcile (never itself an effective-state claim). */
  readonly dirty: boolean;
  /** the fields whose editors hold a value that is not a legal explicit
   * value yet — the Save stays disabled while any rides (the Chat row's
   * own honest form). */
  readonly invalidFields: ReadonlySet<string>;
  readonly refresh: () => Promise<void>;
  readonly editName: (name: string) => void;
  readonly editValue: (field: string, value: unknown) => void;
  readonly toggleChainMember: (chainId: string) => void;
  readonly markFieldValidity: (field: string, valid: boolean) => void;
  readonly resetDraft: () => void;
  readonly saveChanges: () => Promise<void>;
  readonly applyPreset: (presetId: string) => Promise<void>;
  readonly togglePinned: (controlId: string) => Promise<void>;
}

export interface InferenceOptions {
  readonly client: GatewayClient;
  /** the UPDATE is session-scoped: null disables every mutation
   * honestly (the READ stays available — it is session-free). */
  readonly sessionId: string | null;
}

/** The changes' local form (the client's typed input, structural —
 * the same closed partial shape the seam sends). */
interface InferenceChangesArg {
  readonly name?: string;
  readonly sampler_chain?: readonly { readonly id: string; readonly enabled: boolean }[];
  readonly pinned?: readonly string[];
  readonly values?: Readonly<Record<string, unknown>>;
}

/** Seed the draft from a resolved document — the observed baseline. */
function seedDraft(document: InferenceDocument): InferenceDraft {
  const values: Record<string, unknown> = {};
  for (const control of document.controls) {
    values[control.field] = control.value;
  }
  return {
    name: document.profile_name,
    values,
    chain: document.sampler_chain.map((member) => ({
      id: member.id,
      enabled: member.enabled,
    })),
  };
}

/** The changed value-field keys — the draft vs the observed resolved
 * values (a field edited back to the observed value drops out of the
 * delta: nothing REQUESTED, nothing sent). */
function changedValueKeys(
  draft: InferenceDraft,
  document: InferenceDocument,
): string[] {
  const changed: string[] = [];
  for (const control of document.controls) {
    if (draft.values[control.field] !== control.value) {
      changed.push(control.field);
    }
  }
  return changed;
}

/** The chain membership differs — the draft vs the observed. */
function chainChanged(
  draft: InferenceDraft,
  document: InferenceDocument,
): boolean {
  if (draft.chain.length !== document.sampler_chain.length) return true;
  return draft.chain.some(
    (item, index) =>
      item.id !== document.sampler_chain[index]?.id ||
      item.enabled !== document.sampler_chain[index]?.enabled,
  );
}

export function useInference(options: InferenceOptions): InferenceState {
  const { client, sessionId } = options;
  const [load, setLoad] = useState<InferenceLoad>({ kind: "NOT_LOADED" });
  const [draft, setDraft] = useState<InferenceDraft | null>(null);
  const [update, setUpdate] = useState<InferenceUpdateLane>({ kind: "IDLE" });
  const [busy, setBusy] = useState(false);
  const [invalidFields, setInvalidFields] = useState<ReadonlySet<string>>(
    () => new Set<string>(),
  );
  // The one-dispatch-at-a-time guard (a ref — the callbacks' identities
  // stay stable, the mount READ fires exactly once, no busy-deps loop).
  const inFlight = useRef(false);
  const mounted = useRef(true);

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);

  /** The READ — the resolver's current document (session-free, no
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
      const dispatch = await client.inferenceDocument();
      if (!mounted.current) return;
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        setLoad({ kind: "LOADED", result: dispatch.result, at: Date.now() });
        setDraft((previous) => previous ?? seedDraft(dispatch.result));
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
      if (mounted.current) setBusy(false);
    }
  }, [client]);

  // The mount READ — one pass, exactly once (no polling: the profile
  // does not change under the reader — the honest next-spawn law).
  useEffect(() => {
    void refresh();
  }, [refresh]);

  const editName = useCallback((name: string): void => {
    setDraft((previous) => (previous === null ? previous : { ...previous, name }));
  }, []);

  const editValue = useCallback((field: string, value: unknown): void => {
    setDraft((previous) => {
      if (previous === null) return previous;
      if (previous.values[field] === value) return previous;
      return { ...previous, values: { ...previous.values, [field]: value } };
    });
  }, []);

  const toggleChainMember = useCallback((chainId: string): void => {
    setDraft((previous) => {
      if (previous === null) return previous;
      return {
        ...previous,
        chain: previous.chain.map((item) =>
          item.id === chainId ? { ...item, enabled: !item.enabled } : item,
        ),
      };
    });
  }, []);

  const markFieldValidity = useCallback((field: string, valid: boolean): void => {
    setInvalidFields((previous) => {
      const next = new Set(previous);
      if (valid) {
        next.delete(field);
      } else {
        next.add(field);
      }
      return next;
    });
  }, []);

  const resetDraft = useCallback((): void => {
    setDraft((previous) => {
      if (previous === null || load.kind !== "LOADED") return previous;
      return seedDraft(load.result);
    });
    setInvalidFields(new Set());
  }, [load]);

  /** The shared UPDATE path — one explicit dispatch, a fresh
   * idempotency key (G4), the requested keys riding every lane. On
   * ACCEPTED the returned document is the new OBSERVED baseline; the
   * draft reconciles for the SAVE/PRESET actions (their changes
   * landed) and stays for the PIN action (the workspace section never
   * touches the profile values — the user's in-flight REQUEST stays).
   * On any failure lane the draft is PRESERVED — the user decides. */
  const dispatchUpdate = useCallback(
    async (
      action: InferenceUpdateAction,
      requested: readonly string[],
      changes: InferenceChangesArg,
      reconcileDraft: boolean,
    ): Promise<void> => {
      if (inFlight.current || sessionId === null) return;
      inFlight.current = true;
      setBusy(true);
      setUpdate({ kind: "UPDATING", action, requested });
      try {
        const dispatch = await client.inferenceUpdate({
          sessionId,
          clientRequestId: `inference-${action}-${crypto.randomUUID()}`,
          changes,
        });
        if (!mounted.current) return;
        if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
          setLoad({ kind: "LOADED", result: dispatch.result, at: Date.now() });
          if (reconcileDraft) {
            setDraft(seedDraft(dispatch.result));
            setInvalidFields(new Set());
          }
          setUpdate({
            kind: "UPDATED",
            action,
            requested,
            result: dispatch.result,
            at: Date.now(),
          });
        } else if (dispatch.transport === "TRANSPORT") {
          setUpdate({
            kind: "TRANSPORT",
            action,
            requested,
            failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
            at: Date.now(),
          });
        } else if (dispatch.transport === "MISMATCH") {
          setUpdate({
            kind: "MISMATCH",
            action,
            requested,
            error: dispatch.error,
            at: Date.now(),
          });
        } else {
          setUpdate({
            kind: "REJECTED",
            action,
            requested,
            rejection: dispatch.response.rejection ?? "REJECTED",
            reason: reasonOf(dispatch.response.result),
            at: Date.now(),
          });
        }
      } finally {
        inFlight.current = false;
        if (mounted.current) setBusy(false);
      }
    },
    [sessionId, client],
  );

  /** The SAVE — the closed partial document: ONLY the changed keys
   * ride the wire (absent fields unchanged — the store's own partial
   * law): the changed value fields + the name + the WHOLE 9-member
   * chain when its membership changed. Nothing REQUESTED — no
   * dispatch. */
  const saveChanges = useCallback(async (): Promise<void> => {
    if (load.kind !== "LOADED" || draft === null) return;
    if (invalidFields.size > 0) return; // a pending edit is not a legal explicit value yet
    const document = load.result;
    const valueKeys = changedValueKeys(draft, document);
    const nameChanged = draft.name !== document.profile_name;
    const chainDiffers = chainChanged(draft, document);
    if (valueKeys.length === 0 && !nameChanged && !chainDiffers) return;
    const values: Record<string, unknown> = {};
    for (const field of valueKeys) {
      values[field] = draft.values[field];
    }
    await dispatchUpdate(
      "save",
      [
        ...valueKeys,
        ...(nameChanged ? ["name"] : []),
        ...(chainDiffers ? ["sampler_chain"] : []),
      ],
      {
        ...(valueKeys.length > 0 ? { values } : {}),
        ...(nameChanged ? { name: draft.name } : {}),
        ...(chainDiffers
          ? { sampler_chain: draft.chain.map((item) => ({ id: item.id, enabled: item.enabled })) }
          : {}),
      },
      true,
    );
  }, [load, draft, invalidFields, dispatchUpdate]);

  /** The PRESET APPLY — a PLAIN update (§14): the preset's values ride
   * the wire VERBATIM (the store validates and merges; the diff was
   * previewed BEFORE the apply — transparent, never an opaque mode).
   * Guarded on a CLEAN draft: a preset never silently modifies
   * out-of-scope settings — the user's unresolved REQUEST is resolved
   * by save or reset first. */
  const applyPreset = useCallback(
    async (presetId: string): Promise<void> => {
      if (load.kind !== "LOADED") return;
      if (sessionId === null) return;
      // the clean-draft guard (the §21.2 law's own consequence)
      if (
        draft !== null &&
        (changedValueKeys(draft, load.result).length > 0 ||
          draft.name !== load.result.profile_name ||
          chainChanged(draft, load.result))
      ) {
        return;
      }
      const preset = load.result.presets.find((item) => item.id === presetId);
      if (preset === undefined) return;
      const requested = Object.keys(preset.values);
      if (requested.length === 0) return;
      await dispatchUpdate(
        "preset",
        [`preset:${preset.id}`, ...requested],
        { values: { ...preset.values } },
        true,
      );
    },
    [load, draft, sessionId, dispatchUpdate],
  );

  /** The PIN/UNPIN — the workspace section's own explicit dispatch:
   * the WHOLE pinned list (order preserved: a new pin appends at the
   * end, an unpin removes), never a profile edit. */
  const togglePinned = useCallback(
    async (controlId: string): Promise<void> => {
      if (load.kind !== "LOADED" || sessionId === null) return;
      const current = load.result.pinned;
      const next = current.includes(controlId)
        ? current.filter((id) => id !== controlId)
        : [...current, controlId];
      await dispatchUpdate("pin", ["pinned"], { pinned: next }, false);
    },
    [load, sessionId, dispatchUpdate],
  );

  const dirty =
    load.kind === "LOADED" &&
    draft !== null &&
    (changedValueKeys(draft, load.result).length > 0 ||
      draft.name !== load.result.profile_name ||
      chainChanged(draft, load.result));

  return {
    load,
    draft,
    update,
    busy,
    dirty,
    invalidFields,
    refresh,
    editName,
    editValue,
    toggleChainMember,
    markFieldValidity,
    resetDraft,
    saveChanges,
    applyPreset,
    togglePinned,
  };
}

/** The gateway's reason, honestly typed (unknown on the wire). */
function reasonOf(result: Record<string, unknown> | undefined): string | null {
  const value = result?.["reason"];
  return typeof value === "string" ? value : null;
}
