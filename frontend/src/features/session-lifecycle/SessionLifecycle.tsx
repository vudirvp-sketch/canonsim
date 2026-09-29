/**
 * The session-lifecycle surface (Phase 3's first interactive row):
 * the lease lifecycle over the EXISTING gateway ops — attach (the
 * CAS guard), detach (the lease guard) — with the honest closure
 * REQUESTED → ACCEPTED/REJECTED → EFFECTIVE → OBSERVED
 * (FRONTEND_WEB_LAW §8), rendered stage by stage, never collapsed.
 *
 * What stays distinct here (the law's forbidden collapses):
 * - `click !== success`: the verdict lane names the outcome verbatim
 *   (ACCEPTED with the effect; REJECTED with the gateway's own
 *   rejection name + reason; TRANSPORT never rendered as rejected).
 * - `selected !== loaded`: the OBSERVED card is the root's re-read
 *   document — never the widget's optimistic echo. The card and the
 *   verdict differ until the re-read lands (that gap IS the UI).
 * - The lease is held in TAB MEMORY only (never storage): close the
 *   tab and the lease is forgotten — the gateway stays the truth.
 * - G4: no auto-retry. STALE_REVISION / LEASE_EXPIRED render with
 *   the reason and the explicit retry affordance; the retry mints a
 *   fresh request identity (the user's decision, never the client's).
 */
import type { ReactNode } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type { SessionDocument } from "../../api/gateway/contracts.ts";
import type { LeaseVerdict } from "./useSessionLease.ts";
import { useSessionLease } from "./useSessionLease.ts";

export interface SessionLifecycleProps {
  readonly client: GatewayClient;
  readonly sessionId: string | null;
  /** the root's OBSERVED document (the re-read, never the optimistic echo). */
  readonly document: SessionDocument | null;
  /** the root's read path — called after each ACCEPTED effect (the OBSERVED stage). */
  readonly refreshDocument: () => Promise<void>;
  readonly className?: string;
}

export function SessionLifecycle(props: SessionLifecycleProps): ReactNode {
  const lifecycle = useSessionLease({
    client: props.client,
    sessionId: props.sessionId,
    onObserved: props.refreshDocument,
  });

  const attached = props.document?.attached ?? false;

  return (
    <section className={props.className ?? "surface"} aria-label="Session lifecycle">
      <header className="surface-header">
        <h2>Session</h2>
        <p className="surface-note">
          the lease lifecycle — attach under the CAS revision guard, detach under the lease guard;
          REQUESTED → ACCEPTED/REJECTED → EFFECTIVE → OBSERVED, never collapsed
        </p>
      </header>

      <div className="status-card">
        <h3>observed document — the root&rsquo;s re-read, never the optimistic echo</h3>
        {props.document === null ? (
          <p className="empty">no OBSERVED document yet — reading…</p>
        ) : (
          <dl className="status-grid">
            <dt>session</dt>
            <dd>
              <code data-testid="observed-session">{short(props.document.session_id, 20)}</code>
            </dd>
            <dt>attached</dt>
            <dd>
              <span className={`tag ${attached ? "tag-live" : ""}`}>{attached ? "true" : "false"}</span>
            </dd>
            <dt>revision</dt>
            <dd>
              <code data-testid="observed-revision">{String(props.document.revision)}</code>
            </dd>
            <dt>event_sequence</dt>
            <dd>
              <code>{String(props.document.event_sequence)}</code>
            </dd>
            <dt>created_observed_at</dt>
            <dd>
              <code>{String(props.document.created_observed_at)}</code>
            </dd>
          </dl>
        )}
      </div>

      <div className="controls">
        <button onClick={() => void lifecycle.attach()} disabled={props.sessionId === null || lifecycle.busy !== null}>
          {lifecycle.busy === "attach" ? "REQUESTED…" : "attach session"}
        </button>
        <button
          onClick={() => void lifecycle.detach()}
          disabled={props.sessionId === null || lifecycle.busy !== null || lifecycle.lease === null}
        >
          {lifecycle.busy === "detach" ? "REQUESTED…" : "detach session"}
        </button>
        <button onClick={() => void props.refreshDocument()} disabled={props.sessionId === null}>
          refresh session.get
        </button>
      </div>

      <VerdictLane verdict={lifecycle.verdict} />

      <div className="status-card">
        <h3>held lease — tab memory only, never storage; the detach op&rsquo;s material</h3>
        {lifecycle.lease === null ? (
          <p className="empty-inspector">no lease held (attach to take one; lease_seconds = 30 on this gateway)</p>
        ) : (
          <dl className="status-grid">
            <dt>token</dt>
            <dd>
              <code data-testid="lease-token">{short(lifecycle.lease.token, 20)}</code>
            </dd>
            <dt>lease_seconds</dt>
            <dd>
              <code>{String(lifecycle.lease.seconds)}</code>
            </dd>
          </dl>
        )}
        <p className="surface-note">
          the gateway&rsquo;s lease expires (lease_seconds); a detach past the expiry answers
          LEASE_EXPIRED — the verdict lane renders it verbatim, the retry is your explicit decision
        </p>
      </div>
    </section>
  );
}

/** The verdict lane — the honest stage line for the last mutation. */
function VerdictLane(props: { readonly verdict: LeaseVerdict | null }): ReactNode {
  const { verdict } = props;
  if (verdict === null) {
    return <p className="empty-inspector">no mutation attempted yet — the lane renders the NEXT verdict verbatim</p>;
  }
  const at = new Date(verdict.at).toISOString().slice(11, 19);
  if (verdict.kind === "ACCEPTED") {
    return (
      <div className="banner banner-accepted" role="status" data-testid="verdict-accepted">
        {verdict.operation} · {at} — ACCEPTED → EFFECTIVE: {verdict.effect}
        {verdict.revision === null ? "" : ` (revision ${String(verdict.revision)})`}
        {verdict.effect === "ATTACHED" && verdict.leaseSeconds !== null
          ? `, lease ${String(verdict.leaseSeconds)}s`
          : ""}
        ; OBSERVED rides the re-read above
      </div>
    );
  }
  if (verdict.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert" data-testid="verdict-rejected">
        {verdict.operation} · {at} — REJECTED · {verdict.rejection}
        {verdict.reason === null ? "" : `: ${verdict.reason}`}
        ; the outcome law: NOT_SENT — a retry is your explicit decision (a fresh request identity)
      </div>
    );
  }
  if (verdict.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert" data-testid="verdict-transport">
        {verdict.operation} · {at} — TRANSPORT · {verdict.failure}; never &ldquo;rejected&rdquo; — if the
        request was sent, its outcome is UNKNOWN (no blind retry)
      </div>
    );
  }
  return (
    <div className="banner banner-error" role="alert" data-testid="verdict-mismatch">
      {verdict.operation} · {at} — CONTRACT MISMATCH · {verdict.error}
    </div>
  );
}

function short(value: string, max: number): string {
  if (value.length <= max) return value;
  return `${value.slice(0, Math.ceil(max / 2))}…${value.slice(-Math.floor(max / 2))}`;
}
