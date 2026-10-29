/**
 * useSessionLease — the session lifecycle state (Phase 3's
 * lifecycle/error/reconnect row), over the EXISTING gateway ops
 * only: `session.get` (the CAS read), `session.attach`,
 * `session.detach`. No new route is invented (§3); the surface is a
 * presentation client, never a second authority.
 *
 * The honest closure this hook owns (FRONTEND_WEB_LAW §8):
 * REQUESTED → ACCEPTED/REJECTED → EFFECTIVE → OBSERVED. A mutation
 * reply is the ACCEPTED + EFFECTIVE evidence (the gateway's answer
 * IS the effect confirmation); OBSERVED rides the root's re-read
 * (`onObserved` = the composition root's refreshDocument — the
 * single read path, the root stays the OBSERVED owner).
 *
 * G4 (the no-retry law): the hook auto-retries NOTHING. A fresh
 * `client_request_id` is minted per user action — each explicit
 * attempt is a NEW request identity; reusing a key with different
 * material (a new expected_revision) is DUPLICATE_REQUEST, never
 * attempted. STALE_REVISION (another writer moved the revision
 * between our read and our write) and LEASE_EXPIRED surface
 * verbatim — the retry is always the user's explicit decision.
 */
import { useCallback, useEffect, useRef, useState } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";

/** The two mutations this surface drives. */
export type MutationName = "attach" | "detach";

/**
 * The last mutation's honest verdict — a discriminated union, never
 * a friendly collapse. TRANSPORT is never rendered as "rejected";
 * REJECTED carries the gateway's own closed-vocabulary name.
 */
export type LeaseVerdict =
  | {
      readonly kind: "ACCEPTED";
      readonly at: number;
      readonly operation: MutationName;
      /** the effect's honest name: ATTACHED (lease taken) / DETACHED (released) */
      readonly effect: "ATTACHED" | "DETACHED";
      /** the post-effect revision, from the response envelope (null if absent). */
      readonly revision: number | null;
      /** ATTACHED only: the lease token + seconds (the detach op's material). */
      readonly leaseToken: string | null;
      readonly leaseSeconds: number | null;
    }
  | {
      readonly kind: "REJECTED";
      readonly at: number;
      readonly operation: MutationName;
      /** the gateway's own rejection name (STALE_REVISION / LEASE_EXPIRED / …). */
      readonly rejection: string;
      /** the gateway's reason, when it carries one (unknown-typed on the wire). */
      readonly reason: string | null;
    }
  | {
      readonly kind: "TRANSPORT";
      readonly at: number;
      readonly operation: MutationName;
      readonly failure: string;
    }
  | {
      readonly kind: "MISMATCH";
      readonly at: number;
      readonly operation: MutationName;
      readonly error: string;
    };

/** The held lease — the detach op's material, held in tab memory only. */
export interface HeldLease {
  readonly token: string;
  readonly seconds: number;
}

export interface SessionLeaseState {
  /** the in-flight mutation (the REQUESTED stage) or null. */
  readonly busy: MutationName | null;
  readonly verdict: LeaseVerdict | null;
  readonly lease: HeldLease | null;
}

export interface SessionLeaseOptions {
  readonly client: GatewayClient;
  readonly sessionId: string | null;
  /** the OBSERVED sync — the composition root's refreshDocument. */
  readonly onObserved: () => Promise<void> | void;
}

export function useSessionLease(options: SessionLeaseOptions): SessionLeaseState & {
  readonly attach: () => Promise<void>;
  readonly detach: () => Promise<void>;
} {
  const { client, sessionId, onObserved } = options;
  const [busy, setBusy] = useState<MutationName | null>(null);
  const [verdict, setVerdict] = useState<LeaseVerdict | null>(null);
  const [lease, setLease] = useState<HeldLease | null>(null);
  // A session switch invalidates the held lease (a new session is a
  // new evidence world; the old lease belongs to the old session).
  // The useLiveTail precedent's effect form — the reset rides the
  // commit, never a side effect in the render body.
  const sessionRef = useRef<string | null>(null);
  useEffect(() => {
    const switched = sessionRef.current !== sessionId;
    sessionRef.current = sessionId;
    if (!switched) return;
    setLease(null);
    setVerdict(null);
  }, [sessionId]);

  /** The CAS read: the CURRENT revision the mutation must expect.
   * The caller names its own operation (the verdict must never
   * mislabel a read failure — busy is set but not yet committed
   * when this closure was minted). */
  const readRevision = useCallback(
    async (operation: MutationName): Promise<number | null> => {
    if (sessionId === null) return null;
    const read = await client.sessionGet(sessionId);
    if (read.transport === "DELIVERED" && read.status === "OK") {
      return read.result.revision;
    }
    // The read itself failed honestly: surface it as the mutation's
    // verdict (the request never left the browser — the outcome law
    // keeps it distinct from a gateway rejection).
    if (read.transport === "TRANSPORT") {
      setVerdict({
        kind: "TRANSPORT",
        at: Date.now(),
        operation,
        failure: `${read.failure.kind}: ${read.failure.detail}`,
      });
    } else if (read.transport === "MISMATCH") {
      setVerdict({
        kind: "MISMATCH",
        at: Date.now(),
        operation,
        error: read.error,
      });
    } else {
      setVerdict({
        kind: "REJECTED",
        at: Date.now(),
        operation,
        rejection: read.response.rejection ?? "REJECTED",
        reason: reasonOf(read.response.result),
      });
    }
    return null;
    },
    [client, sessionId],
  );

  const attach = useCallback(async (): Promise<void> => {
    if (sessionId === null || busy !== null) return;
    setBusy("attach");
    try {
      const expectedRevision = await readRevision("attach");
      if (expectedRevision === null) return; // the read's verdict is already set
      const dispatch = await client.sessionAttach({
        sessionId,
        expectedRevision,
        // G4: a fresh idempotency key per explicit attempt — a retry
        // is a NEW request, never a blind reuse.
        clientRequestId: `attach-${crypto.randomUUID()}`,
        label: "workbench web session lifecycle",
      });
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        const held: HeldLease = {
          token: dispatch.result.lease_token,
          seconds: dispatch.result.lease_seconds,
        };
        setLease(held);
        setVerdict({
          kind: "ACCEPTED",
          at: Date.now(),
          operation: "attach",
          effect: "ATTACHED",
          revision: dispatch.response.revision ?? null,
          leaseToken: held.token,
          leaseSeconds: held.seconds,
        });
        await onObserved(); // the OBSERVED stage: the root re-reads
      } else if (dispatch.transport === "TRANSPORT") {
        setVerdict({
          kind: "TRANSPORT",
          at: Date.now(),
          operation: "attach",
          failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
        });
      } else if (dispatch.transport === "MISMATCH") {
        setVerdict({
          kind: "MISMATCH",
          at: Date.now(),
          operation: "attach",
          error: dispatch.error,
        });
      } else {
        setVerdict({
          kind: "REJECTED",
          at: Date.now(),
          operation: "attach",
          rejection: dispatch.response.rejection ?? "REJECTED",
          reason: reasonOf(dispatch.response.result),
        });
      }
    } finally {
      setBusy(null);
    }
  }, [client, sessionId, busy, readRevision, onObserved]);

  const detach = useCallback(async (): Promise<void> => {
    if (sessionId === null || busy !== null || lease === null) return;
    setBusy("detach");
    try {
      const expectedRevision = await readRevision("detach");
      if (expectedRevision === null) return; // the read's verdict is already set
      const dispatch = await client.sessionDetach({
        sessionId,
        expectedRevision,
        leaseToken: lease.token,
        clientRequestId: `detach-${crypto.randomUUID()}`,
      });
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        setLease(null);
        setVerdict({
          kind: "ACCEPTED",
          at: Date.now(),
          operation: "detach",
          effect: "DETACHED",
          revision: dispatch.response.revision ?? null,
          leaseToken: null,
          leaseSeconds: null,
        });
        await onObserved(); // the OBSERVED stage: the root re-reads
      } else if (dispatch.transport === "TRANSPORT") {
        setVerdict({
          kind: "TRANSPORT",
          at: Date.now(),
          operation: "detach",
          failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
        });
      } else if (dispatch.transport === "MISMATCH") {
        setVerdict({
          kind: "MISMATCH",
          at: Date.now(),
          operation: "detach",
          error: dispatch.error,
        });
      } else {
        setVerdict({
          kind: "REJECTED",
          at: Date.now(),
          operation: "detach",
          rejection: dispatch.response.rejection ?? "REJECTED",
          reason: reasonOf(dispatch.response.result),
        });
      }
    } finally {
      setBusy(null);
    }
  }, [client, sessionId, busy, lease, readRevision, onObserved]);

  return { busy, verdict, lease, attach, detach };
}

/** The gateway's reason, honestly typed (unknown on the wire). */
function reasonOf(result: Record<string, unknown> | undefined): string | null {
  const value = result?.["reason"];
  return typeof value === "string" ? value : null;
}
