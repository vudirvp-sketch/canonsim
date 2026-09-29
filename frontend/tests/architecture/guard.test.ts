/**
 * The frontend architecture guard — the tooling floor's first row
 * (FRONTEND_WEB_LAW §11, the dependency-boundary check), landed as
 * the backend `tests/test_architecture.py`'s parity form: the
 * conventions that hold by discipline become executable, so a
 * violation is a RED TEST, never a silent drift. The instrument is
 * deliberately the existing vitest suite (AGENTS §2.8: existing
 * mechanism first — dependency-cruiser/eslint-boundaries stay
 * parked rows for when the import graph outgrows a guard test).
 *
 * What is enforced, each row citing its law:
 *   R1  the network surface (§3/§5, INV-4's client-side mirror):
 *       `fetch(` exists ONLY in the typed gateway client — the one
 *       transport adapter; everything else reaches the gateway
 *       through it, never around it.
 *   R2  the stream admission (§5): no XMLHttpRequest / EventSource /
 *       WebSocket / serviceWorker anywhere in src — SSE/WS/PWA open
 *       only through their own gateway contracts + admissions.
 *   R3  the forbidden stores (§6): no localStorage/sessionStorage/
 *       BroadcastChannel/indexedDB/caches — each tab is an
 *       independent client; browser storage is never truth.
 *   R4  the seam purity (§7): `src/api/**` imports nothing outside
 *       itself (the gateway seam never depends upward).
 *   R5  surface independence (§7): a feature never imports another
 *       feature's internals — surfaces mount through the ONE
 *       composition root, not through each other.
 *   R6  state coupling is type-only (§7): features may read
 *       presentation TYPES from `src/state/**` (`import type`), but
 *       never runtime-couple to it — surfaces stay portable.
 *   R7  the ONE composition root (§7): only `src/app/composition/**`
 *       wires features AND state together.
 *   R8  the test seam: src never imports from tests.
 *
 * Scans are CALL-FORM patterns (e.g. `fetch(`, `localStorage.`) so
 * law-restating docstrings never false-positive — a comment saying
 * "no component ever sees fetch" is documentation, not usage.
 */
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative, sep } from "node:path";
import { describe, expect, it } from "vitest";

// npm scripts always execute with cwd = the package root (frontend/),
// and the zero-command launcher drives the same npm — so cwd is the
// deterministic anchor. Fail LOUD if invoked from elsewhere, never
// silently scan a wrong tree.
const SRC = join(process.cwd(), "src");
if (!statSync(SRC, { throwIfNoEntry: false })?.isDirectory()) {
  throw new Error(
    `architecture guard: no src/ under ${process.cwd()} — run the suite from frontend/ (npm test)`,
  );
}

interface SourceFile {
  readonly rel: string;
  readonly text: string;
  readonly imports: readonly ImportStmt[];
}

interface ImportStmt {
  readonly specifier: string;
  readonly typeOnly: boolean;
}

function walk(dir: string): string[] {
  const out: string[] = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      out.push(...walk(full));
    } else if (name.endsWith(".ts") || name.endsWith(".tsx")) {
      out.push(full);
    }
  }
  return out;
}

/** Parse top-level import/export-from statements (this tree's uniform style). */
function importsOf(text: string): ImportStmt[] {
  const out: ImportStmt[] = [];
  const lines = text.split("\n");
  let stmt: string[] = [];
  let open = false;
  const flush = (): void => {
    const joined = stmt.join("\n");
    const spec = /from\s+["']([^"']+)["']/.exec(joined);
    const sideEffect = /^import\s+["']([^"']+)["']/.exec(stmt[0] ?? "");
    const specifier = spec?.[1] ?? sideEffect?.[1];
    if (specifier !== undefined) {
      out.push({
        specifier,
        typeOnly: /^import\s+type\b/.test(stmt[0] ?? ""),
      });
    }
    stmt = [];
  };
  for (const line of lines) {
    if (!open && /^(import|export)\b/.test(line)) {
      open = true;
      stmt = [line];
      if (/from\s+["']/.test(line) || /^import\s+["']/.test(line)) {
        flush();
        open = false;
      }
    } else if (open) {
      stmt.push(line);
      if (/from\s+["']/.test(line)) {
        flush();
        open = false;
      }
    }
  }
  return out;
}

const FILES: SourceFile[] = walk(SRC).map((full) => {
  const text = readFileSync(full, "utf8");
  return {
    rel: relative(SRC, full).split(sep).join("/"),
    text,
    imports: importsOf(text),
  };
});

/** Where a relative specifier points, as a src-rooted path ("api/gateway/contracts.ts"). */
function resolveRel(fromRel: string, specifier: string): string | null {
  if (!specifier.startsWith(".")) return null; // a bare package specifier (react, zod)
  const stack = fromRel.split("/").slice(0, -1);
  for (const part of specifier.split("/")) {
    if (part === "." || part === "") continue;
    if (part === "..") stack.pop();
    else stack.push(part);
  }
  return stack.join("/");
}

function hits(pattern: RegExp): { rel: string; line: number; excerpt: string }[] {
  const found: { rel: string; line: number; excerpt: string }[] = [];
  for (const file of FILES) {
    file.text.split("\n").forEach((line, i) => {
      if (pattern.test(line)) {
        found.push({ rel: file.rel, line: i + 1, excerpt: line.trim().slice(0, 90) });
      }
    });
  }
  return found;
}

describe("R1 — the network surface: fetch exists ONLY in the typed gateway client (§3/§5)", () => {
  it("has exactly one fetch site: src/api/gateway/client.ts", () => {
    const found = hits(/\bfetch\(/);
    expect(
      found.map((f) => f.rel),
      "the transport adapter is the ONLY module that may touch the wire",
    ).toEqual(["api/gateway/client.ts"]);
  });
});

describe("R2 — the stream admission: no second transport before its gateway contract (§5)", () => {
  it("has no XMLHttpRequest / EventSource / WebSocket / serviceWorker anywhere in src", () => {
    const found = hits(/\bnew\s+(XMLHttpRequest|EventSource|WebSocket)\b|\bserviceWorker\b/);
    expect(found).toEqual([]);
  });
});

describe("R3 — the forbidden browser stores: no storage as truth, no cross-tab bus (§6)", () => {
  it("has no localStorage / sessionStorage / BroadcastChannel / indexedDB / caches in src", () => {
    const found = hits(
      /\blocalStorage\.|\bsessionStorage\.|\bnew\s+BroadcastChannel\b|\bindexedDB\.|\bcaches\./,
    );
    expect(found).toEqual([]);
  });
});

describe("R4 — the seam purity: src/api never imports upward (§7)", () => {
  it("api modules import only within src/api (plus bare packages)", () => {
    const violations: string[] = [];
    for (const file of FILES.filter((f) => f.rel.startsWith("api/"))) {
      for (const imp of file.imports) {
        const target = resolveRel(file.rel, imp.specifier);
        if (target !== null && !target.startsWith("api/")) {
          violations.push(`${file.rel} -> ${imp.specifier} (${target})`);
        }
      }
    }
    expect(violations).toEqual([]);
  });
});

describe("R5 — surface independence: no cross-feature imports (§7)", () => {
  it("a feature never imports another feature's internals", () => {
    const violations: string[] = [];
    for (const file of FILES.filter((f) => f.rel.startsWith("features/"))) {
      const own = file.rel.split("/")[1];
      for (const imp of file.imports) {
        const target = resolveRel(file.rel, imp.specifier);
        if (target?.startsWith("features/") === true && target.split("/")[1] !== own) {
          violations.push(`${file.rel} -> ${imp.specifier}`);
        }
      }
    }
    expect(violations).toEqual([]);
  });
});

describe("R6 — features couple to state ONLY through presentation types (§7)", () => {
  it("every features -> state import is `import type`", () => {
    const violations: string[] = [];
    for (const file of FILES.filter((f) => f.rel.startsWith("features/"))) {
      for (const imp of file.imports) {
        const target = resolveRel(file.rel, imp.specifier);
        if (target?.startsWith("state/") === true && !imp.typeOnly) {
          violations.push(`${file.rel} -> ${imp.specifier} (a VALUE import)`);
        }
      }
    }
    expect(violations).toEqual([]);
  });
});

describe("R7 — the ONE composition root (§7)", () => {
  it("only app/composition wires features AND state together", () => {
    const violations: string[] = [];
    for (const file of FILES) {
      const targets = file.imports.map((imp) => resolveRel(file.rel, imp.specifier));
      const hasFeatures = targets.some((t) => t?.startsWith("features/") === true);
      const hasState = targets.some((t) => t?.startsWith("state/") === true);
      if (hasFeatures && hasState && !file.rel.startsWith("app/composition/")) {
        violations.push(file.rel);
      }
    }
    expect(violations).toEqual([]);
  });
});

describe("R8 — the test seam: src never imports from tests", () => {
  it("no src module imports anything outside src (besides bare packages)", () => {
    const violations: string[] = [];
    for (const file of FILES) {
      for (const imp of file.imports) {
        const target = resolveRel(file.rel, imp.specifier);
        if (target !== null && (target.startsWith("../") || target === "..")) {
          violations.push(`${file.rel} -> ${imp.specifier}`);
        }
      }
    }
    expect(violations).toEqual([]);
  });
});
