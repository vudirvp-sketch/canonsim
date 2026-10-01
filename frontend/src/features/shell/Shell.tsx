/**
 * The Shell — the product navigation surface (iter-297 / D-247, the
 * IA repair): a vertical rail of APPROVED product routes + ONE active
 * workspace. Presentation only: it owns NO semantics, reaches no
 * gateway, imports no feature — the composition root wires the routes
 * in (the surface-module law; the guard's R5/R7 rows).
 *
 * THE NAVIGATION CONTRACT (FRONTEND_UIUX_LAW §2.1, this row's law —
 * the shell was a feature directory, §2's own named failure mode):
 * - the rail exposes ONLY approved user-facing product intents — a
 *   first-class surface is NOT automatically a navigation item;
 * - diagnostic/proof/instrumentation surfaces never enter the rail as
 *   product peers: they live behind ONE subdued Diagnostics entry,
 *   with their own secondary navigation inside the workspace (Gateway
 *   / Session lifecycle / Load probe — the proof instruments that
 *   validated the contract layer, now honestly parked);
 * - the feature registry is never the navigation registry: the
 *   composition root splits ProductRoute from DiagnosticSurface
 *   BEFORE this shell sees anything (App.tsx owns the split);
 * - Settings is a product route pinned at the rail's end.
 *
 * Boundedness by mounting discipline (unchanged from the pane form):
 * ONLY the active surface mounts. A switch unmounts the previous
 * surface — its local presentation state (a live-tail buffer, a probe
 * list) is dropped, and that is the honest form: presentation state is
 * per-surface and volatile, the gateway remains the only truth (a
 * remounted surface re-reads its evidence — possibly via RESYNC,
 * never silently). The active focus is this surface's allowed local
 * state (UI open/closed/tab — §7's explicit allowance).
 */
import { useState } from "react";
import type { ReactNode } from "react";

/** One PRODUCT route — an approved user-facing intent (§2.1). */
export interface ProductRoute {
  readonly id: string;
  readonly label: string;
  /** the rail row's one-line hint (product phrasing, not engineering prose). */
  readonly hint: string;
  /** pinned routes sit at the rail's end (Settings' place). */
  readonly pinned?: boolean;
  readonly element: ReactNode;
}

/** One DIAGNOSTIC surface — proof/instrumentation, never a rail peer. */
export interface DiagnosticSurface {
  readonly id: string;
  readonly label: string;
  /** the secondary-nav row's one-line hint. */
  readonly hint: string;
  readonly element: ReactNode;
}

/** The rail focus: a product route, or the diagnostics area. */
type Focus =
  | { readonly kind: "product"; readonly id: string }
  | { readonly kind: "diagnostics"; readonly id: string };

export interface ShellProps {
  /** the approved product routes — the rail's ONLY content. */
  readonly routes: readonly ProductRoute[];
  /** the proof/diagnostic surfaces — behind the Diagnostics entry. */
  readonly diagnostics: readonly DiagnosticSurface[];
  /** the initially active route id (defaults to the first route). */
  readonly initialRouteId?: string;
}

export function Shell(props: ShellProps): ReactNode {
  const [focus, setFocus] = useState<Focus>(() => ({
    kind: "product",
    id: props.initialRouteId ?? props.routes[0]?.id ?? "",
  }));

  const focusDiagnostic =
    focus.kind === "diagnostics" ? props.diagnostics.find((d) => d.id === focus.id) : undefined;
  const focusRoute =
    focus.kind === "product" ? props.routes.find((r) => r.id === focus.id) : undefined;
  const route = focusRoute ?? (focusDiagnostic === undefined ? props.routes[0] : undefined);
  const inDiagnostics = focusDiagnostic !== undefined;

  if (props.routes.length === 0) {
    return <p className="empty">no product surfaces registered</p>;
  }

  const enterDiagnostics = () => {
    if (focus.kind === "diagnostics") return;
    const first = props.diagnostics[0];
    if (first !== undefined) setFocus({ kind: "diagnostics", id: first.id });
  };

  return (
    <div className="shell" aria-label="Workbench">
      <nav className="shell-rail" aria-label="Primary navigation">
        {props.routes.map((item) => {
          const active = item.id === route?.id && !inDiagnostics;
          return (
            <button
              key={item.id}
              className={[
                "shell-item",
                active ? "shell-item-active" : "",
                item.pinned ? "shell-item-pinned" : "",
              ]
                .filter(Boolean)
                .join(" ")}
              aria-current={active ? "page" : undefined}
              title={item.hint}
              onClick={() => setFocus({ kind: "product", id: item.id })}
            >
              {item.label}
            </button>
          );
        })}
        {props.diagnostics.length > 0 ? (
          <button
            className={
              inDiagnostics
                ? "shell-item shell-item-diagnostics shell-item-diagnostics-open"
                : "shell-item shell-item-diagnostics"
            }
            aria-current={inDiagnostics ? "page" : undefined}
            title="Engineering surfaces — gateway, session lifecycle, load probe"
            onClick={enterDiagnostics}
          >
            Diagnostics
          </button>
        ) : null}
      </nav>
      <div className="shell-workspace">
        {inDiagnostics ? (
          <div className="diagnostics" aria-label="Diagnostics">
            <nav className="diagnostics-tabs" aria-label="Diagnostic surfaces">
              {props.diagnostics.map((item) => {
                const active = item.id === focusDiagnostic?.id;
                return (
                  <button
                    key={item.id}
                    className={active ? "diag-tab diag-tab-active" : "diag-tab"}
                    aria-current={active ? "page" : undefined}
                    title={item.hint}
                    onClick={() => setFocus({ kind: "diagnostics", id: item.id })}
                  >
                    {item.label}
                  </button>
                );
              })}
            </nav>
            <div className="diagnostics-pane" data-testid="active-workspace">
              {focusDiagnostic?.element}
            </div>
          </div>
        ) : (
          <div className="shell-pane" data-testid="active-workspace">
            {route?.element}
          </div>
        )}
      </div>
    </div>
  );
}
