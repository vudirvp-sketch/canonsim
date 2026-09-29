import { describe, expect, it } from "vitest";

import { scrollTopForIndex, totalHeight, windowRange } from "../../src/features/trajectory/virtualization.ts";

describe("windowRange (the virtualization math)", () => {
  it("renders nothing for an empty list", () => {
    expect(windowRange({ total: 0, rowHeight: 28, viewportHeight: 420, scrollTop: 0, overscan: 6 })).toEqual({
      start: 0,
      count: 0,
    });
  });

  it("renders only the first viewport plus overscan at the top", () => {
    const range = windowRange({ total: 10_000, rowHeight: 28, viewportHeight: 420, scrollTop: 0, overscan: 6 });
    // 420 / 28 = 15 visible rows; start clamped to 0; end = 0 + 15 + 6 = 21.
    expect(range.start).toBe(0);
    expect(range.count).toBe(21);
  });

  it("windows the middle of a 10k list (the S0-2 proof shape)", () => {
    const rowHeight = 28;
    const scrollTop = 5000 * rowHeight; // scrolled to row 5000
    const range = windowRange({ total: 10_000, rowHeight, viewportHeight: 420, scrollTop, overscan: 6 });
    expect(range.start).toBe(5000 - 6);
    expect(range.count).toBe(15 + 12); // visible 15 + overscan 6 + 6
  });

  it("clamps the window at the list's end (no phantom rows)", () => {
    const range = windowRange({ total: 100, rowHeight: 28, viewportHeight: 420, scrollTop: 100 * 28, overscan: 6 });
    // firstVisible = 100 (past the end); start = 94, end clamped to 100.
    expect(range.start).toBe(94);
    expect(range.start + range.count).toBe(100);
  });

  it("never renders more than viewport+2*overscan rows regardless of total", () => {
    for (const total of [1_000, 10_000, 100_000, 1_000_000]) {
      for (const scrollTop of [0, 28 * 17, 28 * 999_999]) {
        const range = windowRange({ total, rowHeight: 28, viewportHeight: 420, scrollTop, overscan: 6 });
        expect(range.count).toBeLessThanOrEqual(15 + 12);
      }
    }
  });

  it("clamps negative scroll to zero", () => {
    const range = windowRange({ total: 100, rowHeight: 28, viewportHeight: 420, scrollTop: -400, overscan: 2 });
    expect(range.start).toBe(0);
  });

  it("scrollTopForIndex and totalHeight are the closed-form inverses", () => {
    expect(scrollTopForIndex(7, 28)).toBe(196);
    expect(scrollTopForIndex(-3, 28)).toBe(0);
    expect(totalHeight(10_000, 28)).toBe(280_000);
    expect(totalHeight(0, 28)).toBe(0);
  });
});
