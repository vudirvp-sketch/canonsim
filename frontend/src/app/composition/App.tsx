/**
 * The composition root — ONE root, one wiring site (the
 * surface-module law). It owns nothing semantic: it mounts the
 * tab's session client state (`useTabSession`), the context strip
 * (the honest identity/freshness line), and the SHELL (Phase 3's
 * navigation surface) with the registered panes — the session
 * lifecycle (the lease closure), the gateway status, the S0-4 load
 * probe, the Trajectory live tail, and the Observatory history (the
 * dual-read pair). Every surface below this root reaches the gateway
 * ONLY through the typed client.
 *
 * The op-driver (the S0-4 load probe) is also wired here: it
 * drives REAL `session.attach` ops against the gateway (the CAS
 * loop: read the revision, attach, repeat) and measures the
 * observed ops/s — the honest "simulation/LLM active on the Python
 * side" stand-in for the load note (no llama.cpp model is present
 * in this environment; that band is declared, not faked).
 *
 * The Observatory pane is session-free (its two READ ops are not
 * session-scoped) — the HISTORY world needs no lease, exactly as
 * the durable read-side's own law. The Settings pane is the CONFIG
 * world: its READ is session-free, its closed partial UPDATE is
 * session-scoped (the pane honestly disables the Save without a
 * session — §8's closure over the store's own persisted document).
 */
import { useCallback, useState } from "react";
import type { ReactNode } from "react";

import { GatewayStatus } from "../../features/gateway-status/GatewayStatus.tsx";
import { Observatory } from "../../features/observatory/Observatory.tsx";
import { Settings } from "../../features/settings/Settings.tsx";
import { SessionLifecycle } from "../../features/session-lifecycle/SessionLifecycle.tsx";
import { Shell } from "../../features/shell/Shell.tsx";
import type { ShellPane } from "../../features/shell/Shell.tsx";
import { Trajectory } from "../../features/trajectory/Trajectory.tsx";
import { useTabSession } from "../../state/session/useTabSession.ts";

interface DriveReport {
  readonly at: string;
  readonly ops: number;
  readonly seconds: number;
  readonly opsPerSecond: string;
}

export function App(): ReactNode {
  const session = useTabSession();
  const [driveReport, setDriveReport] = useState<DriveReport | null>(null);
  const [driving, setDriving] = useState(false);

  const driveOps = useCallback(
    async (count: number) => {
      if (session.sessionId === null || driving) return;
      setDriving(true);
      const started = performance.now();
      let done = 0;
      // The CAS loop: each attach needs the CURRENT revision, so the
      // driver observes the session between mutations (two POSTs per
      // event — the honest cost of the optimistic-concurrency guard).
      for (let i = 0; i < count; i += 1) {
        const read = await session.client.sessionGet(session.sessionId);
        if (read.transport !== "DELIVERED" || read.status !== "OK") break;
        const attach = await session.client.sessionAttach({
          sessionId: session.sessionId,
          expectedRevision: read.result.revision,
          clientRequestId: `drive-${crypto.randomUUID()}`,
          label: "s0 load probe",
        });
        if (attach.transport !== "DELIVERED" || attach.status !== "OK") break;
        done += 1;
      }
      const seconds = (performance.now() - started) / 1000;
      setDriveReport({
        at: new Date().toISOString().slice(11, 19),
        ops: done,
        seconds: Math.round(seconds * 100) / 100,
        opsPerSecond: (done / Math.max(seconds, 0.001)).toFixed(1),
      });
      await session.refreshDocument();
      setDriving(false);
    },
    [session, driving],
  );

  const panes: readonly ShellPane[] = [
    {
      id: "session",
      label: "Session",
      hint: "the lease lifecycle — attach under the CAS guard, detach under the lease guard, the honest closure",
      element: (
        <SessionLifecycle
          client={session.client}
          sessionId={session.sessionId}
          document={session.document}
          refreshDocument={session.refreshDocument}
        />
      ),
    },
    {
      id: "gateway",
      label: "Gateway",
      hint: "the app.status round-trip + the honest rejection probes",
      element: <GatewayStatus client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "probe",
      label: "Load probe",
      hint: "drives real session.attach ops (the CAS loop) — the S0-4 measurement instrument",
      element: (
        <div className="surface" aria-label="Load probe">
          <header className="surface-header">
            <h2>Load probe (S0-4)</h2>
            <p className="surface-note">
              drives real <code>session.attach</code> ops (CAS loop) — the Python-side load stand-in;
              no llama.cpp model present in this environment (that band is declared, not faked)
            </p>
          </header>
          <div className="controls">
            <button onClick={() => void driveOps(50)} disabled={session.sessionId === null || driving}>
              drive 50 ops
            </button>
            <button onClick={() => void driveOps(300)} disabled={session.sessionId === null || driving}>
              drive 300 ops (rolls the 256-event retention)
            </button>
          </div>
          {driving ? <p className="empty">driving…</p> : null}
          {driveReport !== null ? (
            <dl className="status-grid">
              <dt>ops</dt>
              <dd>{String(driveReport.ops)}</dd>
              <dt>wall</dt>
              <dd>{`${String(driveReport.seconds)} s`}</dd>
              <dt>observed</dt>
              <dd>{`${driveReport.opsPerSecond} ops/s (attach+get pairs)`}</dd>
              <dt>at</dt>
              <dd>{driveReport.at}</dd>
            </dl>
          ) : (
            <p className="empty-inspector">not run yet</p>
          )}
        </div>
      ),
    },
    {
      id: "trajectory",
      label: "Trajectory",
      hint: "the LIVE session tail (virtualized) — volatile, never durable history",
      element: <Trajectory client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "observatory",
      label: "Observatory",
      hint: "the HISTORY world — bounded windows over committed logs; the dual-read pair of the Trajectory pane",
      element: <Observatory client={session.client} />,
    },
    {
      id: "settings",
      label: "Settings",
      hint: "the launch-settings CONFIG world — the closed partial save, effective at the next spawn (§8's closure over a real store)",
      element: <Settings client={session.client} sessionId={session.sessionId} />,
    },
  ];

  return (
    <div className="app">
      <header className="app-header">
        <h1>
          CanonSim Workbench <span className="tag">phase-3 slice</span>
        </h1>
        <p className="app-note">
          the browser is an untrusted presentation client — semantics stay in CanonSim/Python; this tab
          is one independent gateway client (no cross-tab store, no browser storage as truth)
        </p>
        <div className="strip">
          <span>
            session{" "}
            <code data-testid="session-id">
              {session.creating ? "creating…" : (session.sessionId ?? short(session.createError ?? "—", 20))}
            </code>
          </span>
          <span>
            rev <code>{String(session.document?.revision ?? "—")}</code>
          </span>
          <span>
            seq <code>{String(session.document?.event_sequence ?? "—")}</code>
          </span>
          <span className={`freshness freshness-${session.freshness.toLowerCase()}`}>
            {session.freshness}
          </span>
          <button onClick={session.recreateSession}>new session</button>
          <button onClick={() => void session.refreshDocument()} disabled={session.sessionId === null}>
            refresh session.get
          </button>
        </div>
        {session.createError !== null ? (
          <p className="banner banner-error" role="alert">
            session.create failed: {session.createError} — the gateway may be down (start it:
            python scripts/workbench_app.py)
          </p>
        ) : null}
      </header>

      <Shell panes={panes} initialPaneId="session" />
    </div>
  );
}

function short(value: string, max: number): string {
  if (value.length <= max) return value;
  return `${value.slice(0, Math.ceil(max / 2))}…${value.slice(-Math.floor(max / 2))}`;
}
