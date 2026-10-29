/**
 * The per-tab session state (S0-3): each browser tab is an
 * INDEPENDENT gateway client — this hook mints the tab's own
 * session identity (a unique `client_request_id`, hence a unique
 * deterministic `session_id`) and tracks the tab's OWN view of the
 * session state. Nothing here ever touches `localStorage`,
 * `sessionStorage`, or `BroadcastChannel` (the browser-runtime
 * law's forbidden list): close the tab and the client state is gone;
 * the gateway remains the only truth.
 *
 * The freshness vocabulary (the honest state matrix):
 * - LIVE       — the last read succeeded within the poll window
 * - STALE      — we hold a last-known presentation but the read
 *                failed or polling is paused (hidden tab)
 * - DISCONNECTED — no successful read yet, or the client was never
 *                able to reach the gateway
 *
 * The boot-time OBSERVED-sync (iter-309, the iter-308 §C candidate
 * row): a successful `session.create` is a MUTATION, so without a
 * read the strip honestly says DISCONNECTED — by the vocabulary's
 * own first arm, yet a user can read that as “gateway dead” while
 * operations run fine. The boot therefore issues exactly ONE
 * `session.get` right after the create: a FIRST OBSERVATION, never
 * a retry (G4 — the create already answered), never a poll (exactly
 * one read; failures keep their own honest lane below).
 */
import { useCallback, useEffect, useRef, useState } from "react";

import { GatewayClient, type DispatchResult } from "../../api/gateway/client.ts";
import type { SessionDocument } from "../../api/gateway/contracts.ts";

export type Freshness = "LIVE" | "STALE" | "DISCONNECTED";

export interface TabSessionState {
  readonly client: GatewayClient;
  readonly sessionId: string | null;
  readonly creating: boolean;
  readonly createError: string | null;
  /** The tab's observed session document (OBSERVED, never assumed). */
  readonly document: SessionDocument | null;
  readonly freshness: Freshness;
  readonly lastReadAt: number | null;
}

/** One tab's client + session. Mount this ONCE per tab (the
 * composition root owns it; surfaces consume the returned state). */
export function useTabSession(): TabSessionState & {
  readonly recreateSession: () => void;
  readonly refreshDocument: () => Promise<void>;
} {
  // The client and the creation key are per-TAB by construction:
  // one mount, one identity; a second tab runs a second mount in a
  // separate renderer process with its own key. No shared store.
  const client = useMemoClient();
  const creationKey = useRef<string>(`web-s0-${crypto.randomUUID()}`);

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [creating, setCreating] = useState(true);
  const [createError, setCreateError] = useState<string | null>(null);
  const [document, setDocument] = useState<SessionDocument | null>(null);
  const [freshness, setFreshness] = useState<Freshness>("DISCONNECTED");
  const [lastReadAt, setLastReadAt] = useState<number | null>(null);

  /** One OBSERVED read into the tab state — the single owner of the
   * read lanes (the boot-time sync and the explicit refresh share
   * it; the lane semantics are the vocabulary’s own, never split). */
  const readInto = useCallback(
    async (id: string) => {
      const result = await client.sessionGet(id);
      if (result.transport === "DELIVERED" && result.status === "OK") {
        setDocument(result.result);
        setFreshness("LIVE");
        setLastReadAt(Date.now());
      } else if (result.transport === "DELIVERED") {
        // A delivered semantic rejection: the observation is honest —
        // it is NOT a transport failure; present it as STALE-with-reason.
        setFreshness("STALE");
        setLastReadAt(Date.now());
      } else {
        setFreshness("DISCONNECTED");
      }
    },
    [client],
  );

  const runCreate = useCallback(
    (key: string) => {
      setCreating(true);
      setCreateError(null);
      void (async () => {
        const result: DispatchResult<import("../../api/gateway/contracts.ts").SessionCreateResult> =
          await client.sessionCreate({ clientRequestId: key, label: "workbench web s0" });
        if (result.transport === "DELIVERED" && result.status === "OK") {
          setSessionId(result.result.session_id);
          setCreating(false);
          // The boot-time OBSERVED-sync (iter-308 §C's candidate): ONE
          // session.get immediately after the create — the freshness
          // vocabulary counts READS, and this is the first one. Not a
          // retry (the create already answered OK), not a poll (one
          // read; the sync’s own failure keeps its honest lane).
          void readInto(result.result.session_id);
        } else {
          setCreateError(describeFailure(result));
          setCreating(false);
        }
      })();
    },
    [client, readInto],
  );

  useEffect(() => {
    runCreate(creationKey.current);
  }, [runCreate]);

  const recreateSession = useCallback(() => {
    creationKey.current = `web-s0-${crypto.randomUUID()}`;
    setDocument(null);
    runCreate(creationKey.current);
  }, [runCreate]);

  const refreshDocument = useCallback(async () => {
    if (sessionId === null) return;
    await readInto(sessionId);
  }, [readInto, sessionId]);

  return {
    client,
    sessionId,
    creating,
    createError,
    document,
    freshness,
    lastReadAt,
    recreateSession,
    refreshDocument,
  };
}

function useMemoClient(): GatewayClient {
  const ref = useRef<GatewayClient | null>(null);
  if (ref.current === null) {
    ref.current = new GatewayClient();
  }
  return ref.current;
}

function describeFailure(result: DispatchResult<unknown>): string {
  if (result.transport === "TRANSPORT") {
    return `${result.failure.kind}: ${result.failure.detail}`;
  }
  if (result.transport === "MISMATCH") {
    return `contract mismatch: ${result.error}`;
  }
  return `${result.status}${result.response.rejection === undefined ? "" : ` (${result.response.rejection})`}`;
}
