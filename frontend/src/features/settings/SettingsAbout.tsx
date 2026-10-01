/**
 * The Settings surface's ABOUT section (iter-301, the Settings
 * secondary nav's second member) — the gateway's own IDENTITY
 * document, rendered READ-ONLY over the EXISTING session-free
 * `app.status` READ. Zero new routes (§3); zero invented fields.
 *
 * The D-246 reconciliation this section embodies: the external IA
 * verdict's "General" section implied editable general preferences —
 * none exist (the closed three-field set is the launch-settings
 * store's own law; the UI never invents a fourth field). The honest
 * general content that DOES exist is the application's identity:
 * what service this is, which contract it speaks, how it is exposed,
 * whether auth applies, and the full registered operation registry.
 *
 * The boundary against the Diagnostics area (§2.1's registry split):
 * the Gateway DIAGNOSTIC surface is the PROBE instrument (the
 * round-trip proof + the rejection probes); THIS section is the
 * identity presentation. Same observed document, same owning op —
 * never a second source of truth (the precedent: Chat's header
 * renders model.list/model.states that the Models surface also
 * renders; one fact, one owner, many presentations).
 *
 * The read's honest lanes, never collapsed (§9's empty-state
 * grammar): NOT READ ≠ READING ≠ TRANSPORT ≠ MISMATCH ≠ the
 * answered-but-not-OK fallback. No polling — the identity does not
 * change under the reader (the parity law: construction-stable
 * only); every read is the user's explicit action (ONE READ on
 * mount, the remounted section re-reading its evidence — the
 * mounting discipline; the refresh the explicit re-read).
 */
import { useCallback, useEffect, useState } from "react";
import type { ReactNode } from "react";

import type { AppStatusResult } from "../../api/gateway/contracts.ts";
import type { DispatchResult, GatewayClient } from "../../api/gateway/client.ts";

export interface SettingsAboutProps {
  readonly client: GatewayClient;
  readonly className?: string;
}

/** The identity read's one honest document + its busy marker. */
type StatusState =
  | { readonly kind: "NOT_READ" }
  | { readonly kind: "READING" }
  | { readonly kind: "READ"; readonly result: AppStatusResult; readonly at: number }
  | { readonly kind: "TRANSPORT"; readonly failure: string; readonly at: number }
  | { readonly kind: "MISMATCH"; readonly error: string; readonly at: number }
  | { readonly kind: "NOT_OK"; readonly status: string; readonly at: number };

export function SettingsAbout(props: SettingsAboutProps): ReactNode {
  const [state, setState] = useState<StatusState>({ kind: "NOT_READ" });

  const refresh = useCallback(async (): Promise<void> => {
    setState({ kind: "READING" });
    const dispatch: DispatchResult<AppStatusResult> = await props.client.appStatus();
    if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
      setState({ kind: "READ", result: dispatch.result, at: Date.now() });
    } else if (dispatch.transport === "TRANSPORT") {
      setState({
        kind: "TRANSPORT",
        failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
        at: Date.now(),
      });
    } else if (dispatch.transport === "MISMATCH") {
      setState({ kind: "MISMATCH", error: dispatch.error, at: Date.now() });
    } else {
      // The typed seam sends no arguments, so a domain rejection is
      // structurally unreachable here — the lane stays honest as the
      // defensive fallback, never fabricated in a test.
      setState({
        kind: "NOT_OK",
        status: dispatch.response.rejection ?? dispatch.status,
        at: Date.now(),
      });
    }
  }, [props.client]);

  // The mount READ — exactly one dispatch per mount (the remounted
  // section re-reads its evidence; refresh's identity is stable, the
  // deps list is empty by design — the mount is the one trigger).
  useEffect(() => {
    void refresh();
  }, []);

  return (
    <section className={props.className ?? "settings-section"} aria-label="Settings — About">
      <header className="surface-header">
        <h3>
          About <span className="tag">IDENTITY · READ-ONLY</span>
        </h3>
        <p className="surface-note">
          the gateway&rsquo;s own identity document (<code>app.status</code>) — the service, the
          contract it speaks, the exposure, and the full registered operation registry; nothing
          here is editable. The rejection-probe console lives in Diagnostics (identity here,
          proof there)
        </p>
      </header>

      <AboutLane state={state} />

      <div className="controls">
        <button onClick={() => void refresh()} disabled={state.kind === "READING"}>
          re-read identity
        </button>
        <span className="controls-note">
          one read per visit — the registry is construction-stable, it does not change under the
          reader
        </span>
      </div>
    </section>
  );
}

/** The identity read's honest lanes — never collapsed into one spinner. */
function AboutLane(props: { readonly state: StatusState }): ReactNode {
  const { state } = props;
  if (state.kind === "NOT_READ" || state.kind === "READING") {
    return <p className="empty">reading the gateway identity…</p>;
  }
  if (state.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        identity read TRANSPORT · {state.failure} — the gateway may be down; the re-read is your
        explicit retry
      </div>
    );
  }
  if (state.kind === "MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        identity read CONTRACT MISMATCH · {state.error} — reported, never coerced
      </div>
    );
  }
  if (state.kind === "NOT_OK") {
    return (
      <div className="banner banner-error" role="alert">
        the gateway answered, but not OK ({state.status}) — the honest fallback lane, never a
        friendly collapse
      </div>
    );
  }
  return (
    <dl className="status-grid" data-testid="about-identity">
      <dt>service</dt>
      <dd>{state.result.service}</dd>
      <dt>contract</dt>
      <dd>{state.result.contract}</dd>
      <dt>exposure</dt>
      <dd>{state.result.exposure}</dd>
      <dt>auth</dt>
      <dd>{state.result.auth_required ? "required" : "not required (loopback)"}</dd>
      <dt>operations</dt>
      <dd>
        <span className="controls-note" data-testid="about-operations-count">
          {String(state.result.operations.length)} registered
        </span>
        {state.result.operations.map((operation) => (
          <code key={operation} className="op-chip">
            {operation}
          </code>
        ))}
      </dd>
    </dl>
  );
}
