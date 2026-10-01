/**
 * useObservatory — the HISTORY world's read state (Phase 3's
 * Observatory entry), over the EXISTING gateway READ ops only:
 * `observatory.runs` (the discovery scan) + `observatory.read` (one
 * run's bounded event window). No new route is invented (§3); the
 * surface is a projection instrument, never a second authority —
 * every row arrives from the committed log's own read model.
 *
 * DUAL-READ LAW (FRONTEND_WEB_LAW §4): this hook NEVER touches
 * `session.events` — the LIVE tail's cursors and the HISTORY
 * window's event-id cursor never mix. History is DURABLE: there is
 * no polling and no auto-refresh (a committed log does not change
 * under the reader); every read is the user's explicit action.
 *
 * BOUNDEDNESS (§6): ONE window in memory at a time — the forward
 * pagination REPLACES the current window (the client never
 * materializes the run; the backend's own ceiling bounds each
 * window, default 50 / cap 200).
 *
 * G4 (the no-retry law): a rejected read (NO MATCH / stale cursor /
 * corrupt log) is rendered verbatim; the re-read from the head is
 * the USER's explicit decision, never an automatic one.
 */
import { useCallback, useState } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type {
  ObservatoryReadResult,
  ObservatoryRunsResult,
} from "../../api/gateway/contracts.ts";

/** The discovery scan's honest state — the empty-state grammar's
 * NO DATA member rides INSIDE the scanned result (an empty listing
 * is the runs root's own honest answer, never an error). */
export type RunsScan =
  | { readonly kind: "NOT_SCANNED" }
  | { readonly kind: "SCANNING" }
  | { readonly kind: "SCANNED"; readonly result: ObservatoryRunsResult; readonly at: number }
  | { readonly kind: "TRANSPORT"; readonly failure: string; readonly at: number }
  | { readonly kind: "MISMATCH"; readonly error: string; readonly at: number };

/** The selected run's read view — one bounded window, or the honest
 * failure lane (a domain violation is DELIVERED REJECTED with the
 * observed cause, rendered verbatim — never a fabricated empty
 * window). */
export type ReadView =
  | { readonly kind: "NO_RUN_SELECTED" }
  | { readonly kind: "READING"; readonly run: string }
  | { readonly kind: "WINDOW"; readonly result: ObservatoryReadResult; readonly at: number }
  | {
      readonly kind: "REJECTED";
      readonly run: string;
      readonly rejection: string;
      readonly reason: string | null;
      readonly at: number;
    }
  | { readonly kind: "TRANSPORT"; readonly run: string; readonly failure: string; readonly at: number }
  | { readonly kind: "MISMATCH"; readonly run: string; readonly error: string; readonly at: number };

export interface ObservatoryState {
  readonly scan: RunsScan;
  readonly view: ReadView;
  readonly busy: boolean;
  /** the selected event id (the semantic identity — never a row index). */
  readonly selectedEventId: string | null;
  readonly scanRuns: () => Promise<void>;
  readonly openRun: (run: string) => Promise<void>;
  readonly nextWindow: () => Promise<void>;
  readonly selectEvent: (eventId: string) => void;
}

export interface ObservatoryOptions {
  readonly client: GatewayClient;
}

export function useObservatory(options: ObservatoryOptions): ObservatoryState {
  const { client } = options;
  const [scan, setScan] = useState<RunsScan>({ kind: "NOT_SCANNED" });
  const [view, setView] = useState<ReadView>({ kind: "NO_RUN_SELECTED" });
  const [busy, setBusy] = useState(false);
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);

  /** One read's honest exit — the four lanes stay distinct. */
  const readWindow = useCallback(
    async (run: string, after?: string): Promise<void> => {
      setBusy(true);
      setView({ kind: "READING", run });
      setSelectedEventId(null);
      try {
        const dispatch = await client.observatoryRead(
          after === undefined ? { run } : { run, after },
        );
        if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
          setView({ kind: "WINDOW", result: dispatch.result, at: Date.now() });
        } else if (dispatch.transport === "TRANSPORT") {
          setView({
            kind: "TRANSPORT",
            run,
            failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
            at: Date.now(),
          });
        } else if (dispatch.transport === "MISMATCH") {
          setView({ kind: "MISMATCH", run, error: dispatch.error, at: Date.now() });
        } else {
          setView({
            kind: "REJECTED",
            run,
            rejection: dispatch.response.rejection ?? "REJECTED",
            reason: reasonOf(dispatch.response.result),
            at: Date.now(),
          });
        }
      } finally {
        setBusy(false);
      }
    },
    [client],
  );

  const scanRuns = useCallback(async (): Promise<void> => {
    if (busy) return;
    setBusy(true);
    setScan({ kind: "SCANNING" });
    try {
      const dispatch = await client.observatoryRuns();
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        setScan({ kind: "SCANNED", result: dispatch.result, at: Date.now() });
      } else if (dispatch.transport === "TRANSPORT") {
        setScan({
          kind: "TRANSPORT",
          failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
          at: Date.now(),
        });
      } else if (dispatch.transport === "MISMATCH") {
        setScan({ kind: "MISMATCH", error: dispatch.error, at: Date.now() });
      } else {
        // A rejected listing is a domain violation of the READ model
        // itself (e.g. an unknown argument the client never sends) —
        // surfaced in the scan's own failure lane, verbatim.
        setScan({
          kind: "MISMATCH",
          error: `observatory.runs REJECTED ${dispatch.response.rejection ?? "REJECTED"}: ${reasonOf(dispatch.response.result) ?? "(no reason)"}`,
          at: Date.now(),
        });
      }
    } finally {
      setBusy(false);
    }
  }, [busy, client]);

  const openRun = useCallback(
    async (run: string): Promise<void> => {
      if (busy) return;
      await readWindow(run);
    },
    [busy, readWindow],
  );

  const nextWindow = useCallback(
    async (): Promise<void> => {
      if (busy || view.kind !== "WINDOW") return;
      const after = view.result.window.next_after;
      if (after === null) return; // the run's end — honestly nothing more
      await readWindow(view.result.run, after);
    },
    [busy, view, readWindow],
  );

  const selectEvent = useCallback((eventId: string): void => {
    setSelectedEventId(eventId);
  }, []);

  return { scan, view, busy, selectedEventId, scanRuns, openRun, nextWindow, selectEvent };
}

/** The gateway's reason, honestly typed (unknown on the wire). */
function reasonOf(result: Record<string, unknown> | undefined): string | null {
  const value = result?.["reason"];
  return typeof value === "string" ? value : null;
}
