/**
 * VirtualList — the windowed list component. Renders ONLY the
 * current window's rows (absolutely positioned inside one tall
 * inner container): a 10_000-row tail mounts ~visible+2*overscan
 * rows, never the full tree. The scroll container's dimensions are
 * PROPS (not measured): deterministic in jsdom, explicit in the
 * browser. Row identity is the caller's key — for the Trajectory
 * it is the event's SEMANTIC id, never the row index.
 */
import { useEffect, useMemo, useRef, useState } from "react";
import type { CSSProperties, ReactNode } from "react";

import { scrollTopForIndex, totalHeight, windowRange } from "./virtualization.ts";

/** An imperative scroll command — explicit, applied on change. */
export type ScrollCommand =
  | { readonly kind: "INDEX"; readonly index: number; readonly token: number }
  | { readonly kind: "TOP"; readonly token: number }
  | { readonly kind: "BOTTOM"; readonly token: number };

/** A scroll request before the token is minted (distributive omit —
 * a plain Omit over a union loses the per-member fields). */
export type ScrollRequest = ScrollCommand extends infer Command
  ? Command extends { readonly token: number }
    ? Omit<Command, "token">
    : never
  : never;

export function nextScrollToken(previous: number): number {
  return previous + 1;
}

export interface VirtualListProps {
  readonly total: number;
  readonly rowHeight: number;
  readonly viewportHeight: number;
  readonly overscan?: number;
  readonly rowKey: (index: number) => string;
  readonly renderRow: (index: number) => ReactNode;
  readonly className?: string;
  /** Ref to the scroll container (for imperative scrolling). */
  readonly containerRef?: (element: HTMLDivElement | null) => void;
  /** Applied whenever `token` changes (repeatable commands). */
  readonly scrollCommand?: ScrollCommand | null;
}

export function VirtualList(props: VirtualListProps): ReactNode {
  const { total, rowHeight, viewportHeight, overscan = 6 } = props;
  const [scrollTop, setScrollTop] = useState(0);
  const containerRef = useRef<HTMLDivElement | null>(null);

  const range = useMemo(
    () => windowRange({ total, rowHeight, viewportHeight, scrollTop, overscan }),
    [total, rowHeight, viewportHeight, scrollTop, overscan],
  );

  const command = props.scrollCommand ?? null;
  useEffect(() => {
    const container = containerRef.current;
    if (container === null || command === null) return;
    if (command.kind === "TOP") {
      container.scrollTop = 0;
    } else if (command.kind === "BOTTOM") {
      container.scrollTop = totalHeight(total, rowHeight);
    } else {
      container.scrollTop = scrollTopForIndex(command.index, rowHeight);
    }
    // Sync the window state directly: a programmatic scroll does not
    // reliably fire the scroll event (jsdom never does; real browsers
    // fire it async) — the state rides the command, never the event.
    setScrollTop(container.scrollTop);
    // The token makes repeat commands distinct (jump to row 5 twice).
  }, [command, total, rowHeight]);

  const innerStyle: CSSProperties = {
    position: "relative",
    height: `${String(totalHeight(total, rowHeight))}px`,
  };

  return (
    <div
      ref={(element) => {
        containerRef.current = element;
        props.containerRef?.(element);
      }}
      className={props.className}
      role="list"
      aria-rowcount={total}
      style={{
        height: `${String(viewportHeight)}px`,
        overflowY: "auto",
        position: "relative",
      }}
      onScroll={(event) => {
        setScrollTop(event.currentTarget.scrollTop);
      }}
    >
      <div style={innerStyle}>
        {Array.from({ length: range.count }, (_, offset) => {
          const index = range.start + offset;
          return (
            <div
              key={props.rowKey(index)}
              role="listitem"
              style={{
                position: "absolute",
                top: `${String(index * rowHeight)}px`,
                left: 0,
                right: 0,
                height: `${String(rowHeight)}px`,
              }}
            >
              {props.renderRow(index)}
            </div>
          );
        })}
      </div>
    </div>
  );
}
