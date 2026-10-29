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
 * observed ops/s. With a model loaded the measurement runs
 * alongside a live llama-server (iter-302's liveband closure);
 * without one it remains the honest Python-side stand-in — the
 * probe never fabricates the LLM side either way.
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
import { formatClock, formatNumber, tr, useLanguage } from "../../i18n/index.ts";
import { useTabSession } from "../../state/session/useTabSession.ts";

interface DriveReport {
  readonly at: string;
  readonly ops: number;
  readonly seconds: number;
  readonly opsPerSecond: number;
}

export function App(): ReactNode {
  const session = useTabSession();
  // i18n-1's `lang` row: the composition root subscribes to the
  // boundary, so a language switch re-renders the header + the shell's
  // rail labels (the routes registry is rebuilt per render — the
  // labels are read fresh from `tr`). `data-lang` is the honest
  // observation hook for the browser band.
  const language = useLanguage();
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
        at: new Date().toISOString(),
        ops: done,
        seconds: Math.round(seconds * 100) / 100,
        opsPerSecond: done / Math.max(seconds, 0.001),
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
      label: tr("app.route.chat.label"),
      hint: tr("app.route.chat.hint"),
      element: <Chat client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "inference",
      label: tr("app.route.inference.label"),
      hint: tr("app.route.inference.hint"),
      element: <Inference client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "models",
      label: tr("app.route.models.label"),
      hint: tr("app.route.models.hint"),
      element: <Models client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "trajectory",
      label: tr("app.route.trajectory.label"),
      hint: tr("app.route.trajectory.hint"),
      element: <Trajectory client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "observatory",
      label: tr("app.route.observatory.label"),
      hint: tr("app.route.observatory.hint"),
      element: <Observatory client={session.client} />,
    },
    {
      id: "settings",
      label: tr("app.route.settings.label"),
      hint: tr("app.route.settings.hint"),
      pinned: true,
      element: <Settings client={session.client} sessionId={session.sessionId} />,
    },
  ];

  const diagnostics: readonly DiagnosticSurface[] = [
    {
      id: "session",
      label: tr("app.diag.session.label"),
      hint: tr("app.diag.session.hint"),
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
      label: tr("app.diag.gateway.label"),
      hint: tr("app.diag.gateway.hint"),
      element: <GatewayStatus client={session.client} sessionId={session.sessionId} />,
    },
    {
      id: "probe",
      label: tr("app.diag.probe.label"),
      hint: tr("app.diag.probe.hint"),
      element: (
        <div className="surface" aria-label={tr("app.probe.region")}>
          <header className="surface-header">
            <h2>{tr("app.probe.title")}</h2>
            <p className="surface-note">
              {tr("app.probe.noteA")}
              <code>session.attach</code>
              {tr("app.probe.noteB")}
            </p>
          </header>
          <div className="controls">
            <button onClick={() => void driveOps(50)} disabled={session.sessionId === null || driving}>
              {tr("app.probe.drive50")}
            </button>
            <button onClick={() => void driveOps(300)} disabled={session.sessionId === null || driving}>
              {tr("app.probe.drive300")}
            </button>
          </div>
          {driving ? <p className="empty">{tr("app.probe.driving")}</p> : null}
          {driveReport !== null ? (
            <dl className="status-grid">
              <dt>{tr("app.probe.dt.ops")}</dt>
              <dd>{formatNumber(driveReport.ops)}</dd>
              <dt>{tr("app.probe.dt.wall")}</dt>
              <dd>{tr("app.probe.wallValue", { seconds: formatNumber(driveReport.seconds) })}</dd>
              <dt>{tr("app.probe.dt.observed")}</dt>
              <dd>
                {tr("app.probe.observedValue", {
                  ops: formatNumber(driveReport.opsPerSecond, {
                    minimumFractionDigits: 1,
                    maximumFractionDigits: 1,
                  }),
                })}
              </dd>
              <dt>{tr("app.probe.dt.at")}</dt>
              <dd>{formatClock(driveReport.at)}</dd>
            </dl>
          ) : (
            <p className="empty-inspector">{tr("app.probe.notRun")}</p>
          )}
        </div>
      ),
    },
  ];

  return (
    <div className="app" data-lang={language}>
      <header className="app-header">
        <div className="app-header-row">
          <h1>{tr("app.title")}</h1>
          <div className="strip">
            <span>
              {tr("app.strip.session")}{" "}
              <code data-testid="session-id">
                {session.creating ? tr("app.strip.creating") : (session.sessionId ?? short(session.createError ?? "—", 20))}
              </code>
            </span>
            <span>
              {tr("app.strip.rev")}{" "}
              <code data-testid="session-rev">{String(session.document?.revision ?? "—")}</code>
            </span>
            <span>
              {tr("app.strip.seq")}{" "}
              <code data-testid="session-seq">{String(session.document?.event_sequence ?? "—")}</code>
            </span>
            <span className={`freshness freshness-${session.freshness.toLowerCase()}`} data-testid="session-freshness">
              {session.freshness}
            </span>
            <button onClick={() => void session.refreshDocument()} disabled={session.sessionId === null}>
              {tr("app.strip.refresh")}
            </button>
          </div>
        </div>
        {session.createError !== null ? (
          <p className="banner banner-error" role="alert">
            {tr("app.banner.createFailed", { error: session.createError })}
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
