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
 * - `new session` (the root's recreate path, iter-297/D-247: the
 *   lifecycle action moved out of the product chrome and home here)
 *   mints a FRESH tab session identity — the old session's lease is
 *   left to expire server-side, never silently detached.
 */
import type { ReactNode } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type { SessionDocument } from "../../api/gateway/contracts.ts";
import { formatClock, tr } from "../../i18n/index.ts";
import type { LeaseVerdict } from "./useSessionLease.ts";
import { useSessionLease } from "./useSessionLease.ts";

export interface SessionLifecycleProps {
  readonly client: GatewayClient;
  readonly sessionId: string | null;
  /** the root's OBSERVED document (the re-read, never the optimistic echo). */
  readonly document: SessionDocument | null;
  /** the root's read path — called after each ACCEPTED effect (the OBSERVED stage). */
  readonly refreshDocument: () => Promise<void>;
  /** the root's recreate path — mints a fresh tab session identity (the
   * lifecycle action's honest home since iter-297: out of the product chrome). */
  readonly recreateSession: () => void;
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
    <section className={props.className ?? "surface"} aria-label={tr("session.region")}>
      <header className="surface-header">
        <h2>{tr("session.title")}</h2>
        <p className="surface-note">{tr("session.note")}</p>
      </header>

      <div className="status-card">
        <h3>{tr("session.observed.title")}</h3>
        {props.document === null ? (
          <p className="empty">{tr("session.observed.empty")}</p>
        ) : (
          <dl className="status-grid">
            <dt>{tr("session.observed.session")}</dt>
            <dd>
              <code data-testid="observed-session">{short(props.document.session_id, 20)}</code>
            </dd>
            <dt>{tr("session.observed.attached")}</dt>
            <dd>
              <span className={`tag ${attached ? "tag-live" : ""}`}>
                {attached ? tr("session.observed.true") : tr("session.observed.false")}
              </span>
            </dd>
            <dt>{tr("session.observed.revision")}</dt>
            <dd>
              <code data-testid="observed-revision">{String(props.document.revision)}</code>
            </dd>
            <dt>{tr("session.observed.eventSequence")}</dt>
            <dd>
              <code>{String(props.document.event_sequence)}</code>
            </dd>
            <dt>{tr("session.observed.createdObservedAt")}</dt>
            <dd>
              <code>{String(props.document.created_observed_at)}</code>
            </dd>
          </dl>
        )}
      </div>

      <div className="controls">
        <button
          onClick={() => void lifecycle.attach()}
          disabled={props.sessionId === null || lifecycle.busy !== null}
        >
          {lifecycle.busy === "attach" ? tr("session.requested") : tr("session.attach")}
        </button>
        <button
          onClick={() => void lifecycle.detach()}
          disabled={props.sessionId === null || lifecycle.busy !== null || lifecycle.lease === null}
        >
          {lifecycle.busy === "detach" ? tr("session.requested") : tr("session.detach")}
        </button>
        <button onClick={() => void props.refreshDocument()} disabled={props.sessionId === null}>
          {tr("session.refresh")}
        </button>
        <button onClick={props.recreateSession} disabled={lifecycle.busy !== null}>
          {tr("session.new")}
        </button>
      </div>

      <VerdictLane verdict={lifecycle.verdict} />

      <div className="status-card">
        <h3>{tr("session.lease.title")}</h3>
        {lifecycle.lease === null ? (
          <p className="empty-inspector">{tr("session.lease.empty")}</p>
        ) : (
          <dl className="status-grid">
            <dt>{tr("session.lease.token")}</dt>
            <dd>
              <code data-testid="lease-token">{short(lifecycle.lease.token, 20)}</code>
            </dd>
            <dt>{tr("session.lease.seconds")}</dt>
            <dd>
              <code>{String(lifecycle.lease.seconds)}</code>
            </dd>
          </dl>
        )}
        <p className="surface-note">{tr("session.lease.note")}</p>
      </div>
    </section>
  );
}

/** The verdict lane — the honest stage line for the last mutation. */
function VerdictLane(props: { readonly verdict: LeaseVerdict | null }): ReactNode {
  const { verdict } = props;
  if (verdict === null) {
    return <p className="empty-inspector">{tr("session.verdict.empty")}</p>;
  }
  const at = formatClock(new Date(verdict.at).toISOString());
  if (verdict.kind === "ACCEPTED") {
    return (
      <div className="banner banner-accepted" role="status" data-testid="verdict-accepted">
        {tr("session.verdict.accepted", {
          operation: verdict.operation,
          at,
          effect: verdict.effect,
          revision:
            verdict.revision === null
              ? ""
              : tr("session.verdict.revision", { revision: String(verdict.revision) }),
          lease:
            verdict.effect === "ATTACHED" && verdict.leaseSeconds !== null
              ? tr("session.verdict.lease", { seconds: String(verdict.leaseSeconds) })
              : "",
        })}
      </div>
    );
  }
  if (verdict.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert" data-testid="verdict-rejected">
        {tr("session.verdict.rejected", {
          operation: verdict.operation,
          at,
          rejection: verdict.rejection,
          reason:
            verdict.reason === null
              ? ""
              : tr("session.verdict.reason", { reason: verdict.reason }),
        })}
      </div>
    );
  }
  if (verdict.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert" data-testid="verdict-transport">
        {tr("session.verdict.transport", {
          operation: verdict.operation,
          at,
          failure: verdict.failure,
        })}
      </div>
    );
  }
  return (
    <div className="banner banner-error" role="alert" data-testid="verdict-mismatch">
      {tr("session.verdict.mismatch", {
        operation: verdict.operation,
        at,
        error: verdict.error,
      })}
    </div>
  );
}

function short(value: string, max: number): string {
  if (value.length <= max) return value;
  return `${value.slice(0, Math.ceil(max / 2))}…${value.slice(-Math.floor(max / 2))}`;
}
