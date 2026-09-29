/**
 * The gateway-status surface (S0-1): the honest op round-trip and
 * the honest REJECTION paths, in the UI, against the real gateway.
 *
 * The probes deliberately exercise the gateway's OWN closed
 * rejection vocabulary (never a fabricated failure):
 * - `session.get` on a bogus session id  -> DOMAIN_REJECTED
 * - `session.attach` with a stale revision -> STALE_REVISION (the CAS guard)
 * - `session.create` reusing a live key with different material -> DUPLICATE_REQUEST
 * Each probe renders the DELIVERED verdict verbatim — status,
 * rejection name, operation_id — never a friendly collapse.
 *
 * The transport lane stays distinct: an unreachable gateway is
 * TRANSPORT (UNREACHABLE/ABORTED/HTTP_ERROR), never "rejected"; an
 * in-flight abort honestly says the outcome would be UNKNOWN (G4 —
 * no blind retry is ever attempted by this client).
 */
import { useCallback, useEffect, useState } from "react";
import type { ReactNode } from "react";

import type { AppStatusResult } from "../../api/gateway/contracts.ts";
import type { DispatchResult, GatewayClient } from "../../api/gateway/client.ts";

interface ProbeRecord {
  readonly label: string;
  readonly at: string;
  readonly outcome:
    | { readonly kind: "DELIVERED"; readonly status: string; readonly rejection?: string | undefined; readonly operationId: string }
    | { readonly kind: "TRANSPORT"; readonly failure: string }
    | { readonly kind: "MISMATCH"; readonly error: string };
}

export interface GatewayStatusProps {
  readonly client: GatewayClient;
  readonly sessionId: string | null;
  readonly className?: string;
}

export function GatewayStatus(props: GatewayStatusProps): ReactNode {
  const [statusResult, setStatusResult] = useState<DispatchResult<AppStatusResult> | null>(null);
  const [statusBusy, setStatusBusy] = useState(false);
  const [probes, setProbes] = useState<readonly ProbeRecord[]>([]);

  const recordProbe = useCallback(
    (label: string, outcome: ProbeRecord["outcome"]) => {
      setProbes((previous) => [
        { label, at: new Date().toISOString().slice(11, 19), outcome },
        ...previous.slice(0, 9),
      ]);
    },
    [],
  );

  const refreshStatus = useCallback(async () => {
    setStatusBusy(true);
    const result = await props.client.appStatus();
    setStatusResult(result);
    setStatusBusy(false);
  }, [props.client]);

  // The round-trip on mount (the ≥1 successful op path).
  useEffect(() => {
    void refreshStatus();
  }, [refreshStatus]);

  const probeBogusSession = useCallback(async () => {
    const result = await props.client.sessionGet("bogus-session-id-probe");
    recordProbe("session.get · bogus session id", describeDispatch(result));
  }, [props.client, recordProbe]);

  const probeStaleRevision = useCallback(async () => {
    if (props.sessionId === null) return;
    // The CAS guard: a revision that can never be current.
    const result = await props.client.sessionAttach({
      sessionId: props.sessionId,
      expectedRevision: 999_999,
      clientRequestId: `probe-stale-${crypto.randomUUID()}`,
      label: "stale-revision probe",
    });
    recordProbe("session.attach · stale expected revision", describeDispatch(result));
  }, [props.client, props.sessionId, recordProbe]);

  const probeDuplicateKey = useCallback(async () => {
    // The idempotency law: the same key + DIFFERENT material is a
    // conflicting reuse (DUPLICATE_REQUEST), never a second effect.
    const key = `probe-dup-${crypto.randomUUID()}`;
    const first = await props.client.sessionCreate({ clientRequestId: key, label: "first material" });
    void first; // whatever it was, the probe is the SECOND call:
    const second = await props.client.sessionCreate({ clientRequestId: key, label: "DIFFERENT material" });
    recordProbe("session.create · same key, different material", describeDispatch(second));
  }, [props.client, recordProbe]);

  return (
    <section className={props.className ?? "surface"} aria-label="Gateway status">
      <header className="surface-header">
        <h2>Gateway</h2>
        <p className="surface-note">POST /op — the one route; every payload runtime-validated at the client boundary</p>
      </header>

      <div className="status-card">
        {statusResult === null ? (
          <p className="empty">reading app.status…</p>
        ) : (
          <StatusLane result={statusResult} />
        )}
        <div className="controls">
          <button onClick={() => void refreshStatus()} disabled={statusBusy}>
            refresh app.status
          </button>
        </div>
      </div>

      <div className="probe-panel">
        <h3>rejection probes — the honest paths, against the real gateway</h3>
        <div className="controls">
          <button className="probe" onClick={() => void probeBogusSession()}>
            DOMAIN_REJECTED probe
          </button>
          <button className="probe" onClick={() => void probeStaleRevision()} disabled={props.sessionId === null}>
            STALE_REVISION probe
          </button>
          <button className="probe" onClick={() => void probeDuplicateKey()}>
            DUPLICATE_REQUEST probe
          </button>
        </div>
        {probes.length === 0 ? (
          <p className="empty-inspector">no probes run yet</p>
        ) : (
          <ul className="probe-list">
            {probes.map((probe, index) => (
              <li key={`${probe.at}-${String(index)}`} className="probe-record">
                <span className="probe-label">{probe.label}</span>
                <span className={`probe-outcome probe-${probe.outcome.kind}`}>
                  {probe.outcome.kind === "DELIVERED"
                    ? `DELIVERED · ${probe.outcome.status}${probe.outcome.rejection === undefined ? "" : ` · ${probe.outcome.rejection}`}`
                    : probe.outcome.kind === "TRANSPORT"
                      ? `TRANSPORT · ${probe.outcome.failure}`
                      : `MISMATCH · ${probe.outcome.error}`}
                </span>
              </li>
            ))}
          </ul>
        )}
        <p className="surface-note">
          the client auto-retries nothing (G4): UNKNOWN and transport ambiguity stay honest, a retry is
          always an explicit user action
        </p>
      </div>
    </section>
  );
}

function describeDispatch(result: DispatchResult<unknown>): ProbeRecord["outcome"] {
  if (result.transport === "DELIVERED") {
    return {
      kind: "DELIVERED",
      status: result.status,
      rejection: result.response.rejection,
      operationId: result.response.operationId,
    };
  }
  if (result.transport === "TRANSPORT") {
    return { kind: "TRANSPORT", failure: `${result.failure.kind}: ${result.failure.detail}` };
  }
  return { kind: "MISMATCH", error: result.error };
}

/** The status card's three honest lanes (narrowed once, at the edge). */
function StatusLane(props: { readonly result: DispatchResult<AppStatusResult> }): ReactNode {
  const { result } = props;
  if (result.transport === "DELIVERED" && result.status === "OK") {
    return (
      <dl className="status-grid">
        <dt>service</dt>
        <dd>{result.result.service}</dd>
        <dt>contract</dt>
        <dd>{result.result.contract}</dd>
        <dt>exposure</dt>
        <dd>{result.result.exposure}</dd>
        <dt>auth</dt>
        <dd>{result.result.auth_required ? "required" : "not required (loopback)"}</dd>
        <dt>operations</dt>
        <dd>
          {result.result.operations.map((operation) => (
            <code key={operation} className="op-chip">
              {operation}
            </code>
          ))}
        </dd>
      </dl>
    );
  }
  if (result.transport === "TRANSPORT") {
    return (
      <p className="banner banner-error" role="alert">
        TRANSPORT — {result.failure.kind}: {result.failure.detail}
      </p>
    );
  }
  if (result.transport === "MISMATCH") {
    return (
      <p className="banner banner-error" role="alert">
        CONTRACT MISMATCH — {result.error}
      </p>
    );
  }
  return (
    <p className="banner banner-error" role="alert">
      the gateway answered, but not OK — see the probe lane
    </p>
  );
}
