/**
 * The Shell — Phase 3's navigation surface (§7's recommended
 * first-class surface "Shell/navigation"): the pane registry and
 * the switch. Presentation only: it owns NO semantics, reaches no
 * gateway, imports no feature — the composition root wires the
 * panes in (the surface-module law; the guard's R5/R7 rows).
 *
 * Boundedness by mounting discipline (§6): ONLY the active pane
 * mounts. A pane switch unmounts the previous surface — its local
 * presentation state (a live-tail buffer, a probe list) is dropped,
 * and that is the honest form: presentation state is per-surface
 * and volatile, the gateway remains the only truth (the LIVE tail
 * label already declares that volatility; a remounted surface
 * re-reads its evidence — possibly via RESYNC, never silently).
 * The active pane id is this surface's allowed local state (UI
 * open/closed/tab — §7's explicit allowance).
 */
import { useState } from "react";
import type { ReactNode } from "react";

/** One registered pane — the composition root supplies the element. */
export interface ShellPane {
  readonly id: string;
  readonly label: string;
  /** the nav row's one-line honest hint (what this surface proves). */
  readonly hint: string;
  readonly element: ReactNode;
}

export interface ShellProps {
  readonly panes: readonly ShellPane[];
  /** the initially active pane id (defaults to the first pane). */
  readonly initialPaneId?: string;
}

export function Shell(props: ShellProps): ReactNode {
  const [activeId, setActiveId] = useState<string>(
    props.initialPaneId ?? props.panes[0]?.id ?? "",
  );
  const active = props.panes.find((pane) => pane.id === activeId) ?? props.panes[0];
  if (active === undefined) {
    return <p className="empty">no surfaces registered</p>;
  }
  return (
    <div className="shell" aria-label="Workbench surfaces">
      <nav className="shell-nav" aria-label="Surface navigation">
        {props.panes.map((pane) => {
          const isActive = pane.id === active.id;
          return (
            <button
              key={pane.id}
              className={isActive ? "shell-tab shell-tab-active" : "shell-tab"}
              aria-current={isActive ? "page" : undefined}
              title={pane.hint}
              onClick={() => setActiveId(pane.id)}
            >
              {pane.label}
            </button>
          );
        })}
        <span className="shell-nav-note">
          only the active surface mounts — a switch drops the pane&rsquo;s local presentation state
          (the gateway stays the truth)
        </span>
      </nav>
      <div className="shell-pane">{active.element}</div>
    </div>
  );
}
