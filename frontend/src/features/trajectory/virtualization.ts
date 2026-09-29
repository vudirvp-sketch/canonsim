/**
 * The virtualization math — PURE functions, no DOM (testable in
 * jsdom with zero layout). Fixed row height: the S0 event rows are
 * uniform-height by design, which keeps the window computation a
 * closed-form expression (no measurement, no estimation, no
 * layout thrash — the SKELETON's "explicit hard window" done as a
 * real window, not a style).
 *
 * The law carried here (FRONTEND_WEB_LAW §6): never materialize an
 * unbounded list as a live React tree — the window is bounded by
 * construction; a 10_000-row tail mounts only the visible window
 * (plus overscan).
 */

export interface WindowRange {
  /** The first row index rendered (inclusive). */
  readonly start: number;
  /** How many rows are rendered. */
  readonly count: number;
}

export interface WindowOptions {
  /** Total rows in the data (>= 0). */
  readonly total: number;
  /** Fixed row height in px (> 0). */
  readonly rowHeight: number;
  /** The viewport's height in px (> 0). */
  readonly viewportHeight: number;
  /** The container's current scroll offset (>= 0). */
  readonly scrollTop: number;
  /** Extra rows rendered above and below the viewport (>= 0). */
  readonly overscan: number;
}

/** The window [start, start+count) for the current scroll state. */
export function windowRange(options: WindowOptions): WindowRange {
  const { total, rowHeight, viewportHeight, scrollTop, overscan } = options;
  if (total <= 0 || rowHeight <= 0 || viewportHeight <= 0) {
    return { start: 0, count: 0 };
  }
  const clampedScroll = Math.max(0, scrollTop);
  const firstVisible = Math.floor(clampedScroll / rowHeight);
  const visibleCount = Math.ceil(viewportHeight / rowHeight);
  const start = Math.max(0, firstVisible - overscan);
  const end = Math.min(total, firstVisible + visibleCount + overscan);
  return { start, count: Math.max(0, end - start) };
}

/** The scroll offset that puts row `index` at the viewport's top. */
export function scrollTopForIndex(index: number, rowHeight: number): number {
  return Math.max(0, index) * rowHeight;
}

/** The total scrollable height of the virtualized content (px). */
export function totalHeight(total: number, rowHeight: number): number {
  return Math.max(0, total) * rowHeight;
}
