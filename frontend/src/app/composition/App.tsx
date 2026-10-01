/**
 * The composition root — ONE root, one wiring site (the
 * surface-module law). It owns nothing semantic: it mounts the tab's
 * session client state (`useTabSession`), the identity strip (the
 * honest identity/freshness line — §9's context strip), and the SHELL
 * with the SPLIT registries (iter-297 / D-247, the IA repair —
 * FRONTEND_UIUX_LAW §2.1):
 * - PRODUCT ROUTES (the rail): Chat at the rail's HEAD (the
 *   conversation world — iter-298, Phase 3's fourth row), the
 *   Inference control workspace right behind it (iter-299, Phase
 *   3's fifth row — the AI family adjacent: converse → control the
 *   generation), the Models resource right behind that (iter-300,
 *   Phase 3's sixth row — the model family's mirror: converse →
 *   control → the resource the conversation runs on), the
 *   Trajectory LIVE tail, the Observatory HISTORY world, the
 *   Settings CONFIG world — the approved user-facing intents;
 * - DIAGNOSTIC SURFACES (behind the Diagnostics entry): the session
 *   lifecycle, the gateway status probes, the S0-4 load probe — the
 *   proof instruments, never product navigation peers.
 * Every surface below this root reaches the gateway ONLY through the
 * typed client.
 *
 * The op-driver (the S0-4 load probe) is also wired here: it
 * drives REAL `session.attach` ops against the gateway (the CAS
 * loop: read the revision, attach, repeat) and measures the
 * observed ops/s — the honest "simulation/LLM active on the Python
 * side" stand-in for the load note (no llama.cpp model is present
 * in this environment; that band is declared, not faked).
 *
 * The Observatory route is session-free (its two READ ops are not
 * session-scoped) — the HISTORY world needs no lease, exactly as
 * the durable read-side's own law. The Settings route is the CONFIG
 * world: its READ is session-free, its closed partial UPDATE is
 * session-scoped (the route honestly disables the Save without a
 * session — §8's closure over the store's own persisted document).
 * The Chat route's run family (chat.send / run.get / run.cancel) is
 * session-scoped: without a session the composer's send is honestly
 * disabled while the header's three context READs stay available
 * (they are session-free).
 */
import { useCallback, useState } from "react";
import type { ReactNode } from "react";

import { Chat } from "../../features/chat/Chat.tsx";
import { GatewayStatus } from "../../features/gateway-status/GatewayStatus.tsx";
import { Inference } from "../../features/inference/Inference.tsx";
import { Models } from "../../features/models/Models.tsx";
import { Observatory } from "../../features/observatory/Observatory.tsx";
import { Settings } from "../../features/settings/Settings.tsx";
import { SessionLifecycle } from "../../features/session-lifecycle/SessionLifecycle.tsx";
import { Shell } from "../../features/shell/Shell.tsx";
import type { DiagnosticSurface, ProductRoute } from "../../features/shell/Shell.tsx";
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

  // THE REGISTRY SPLIT (§2.1's law): product intents and diagnostic
  // instruments are separate registries — the shell never sees a
  // feature list, only the approved routes (+ the diagnostics entry).
  // Chat rides the rail's HEAD (§2.1's canonical IA tree); Inference
  // sits right behind it; Models opens the RESOURCES group behind
  // the AI family (converse → control → the model resource).
  const routes: readonly ProductRoute[] = [
    {
      id: "chat",
      label: "Chat",
      hint: "Converse with the loaded model — every turn an honest run",
      element: <Chat client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "inference",
      label: "Inference",
      hint: "The generation-control workspace — chips, the sampler chain, the effective state",
      element: <Inference client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "models",
      label: "Models",
      hint: "The model family — discovery, arrival (fetch/import), and the load ladder",
      element: <Models client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "trajectory",
      label: "Trajectory",
      hint: "Live events of the current session — the volatile tail, never durable history",
      element: <Trajectory client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "observatory",
      label: "Observatory",
      hint: "Committed run history — bounded windows over the archived logs",
      element: <Observatory client={session.client} />,
    },
    {
      id: "settings",
      label: "Settings",
      hint: "Launch configuration — persisted, effective at the next spawn",
      pinned: true,
      element: <Settings client={session.client} sessionId={session.sessionId} />,
    },
  ];

  const diagnostics: readonly DiagnosticSurface[] = [
    {
      id: "session",
      label: "Session lifecycle",
      hint: "the lease lifecycle — attach under the CAS guard, detach under the lease guard, the honest closure",
      element: (
        <SessionLifecycle
          client={session.client}
          sessionId={session.sessionId}
          document={session.document}
          refreshDocument={session.refreshDocument}
          recreateSession={session.recreateSession}
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
  ];

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-row">
          <h1>CanonSim Workbench</h1>
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
            <button onClick={() => void session.refreshDocument()} disabled={session.sessionId === null}>
              refresh
            </button>
          </div>
        </div>
        {session.createError !== null ? (
          <p className="banner banner-error" role="alert">
            session.create failed: {session.createError} — the gateway may be down (start it:
            python scripts/workbench_app.py)
          </p>
        ) : null}
      </header>

      <Shell routes={routes} diagnostics={diagnostics} initialRouteId="trajectory" />
    </div>
  );
}

function short(value: string, max: number): string {
  if (value.length <= max) return value;
  return `${value.slice(0, Math.ceil(max / 2))}…${value.slice(-Math.floor(max / 2))}`;
}
