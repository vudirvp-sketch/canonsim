# Frontend-Web Track — Agent Context (the durable compact surface)

> What an agent needs repeatedly when working the web-frontend track:
> identity, non-negotiable rules, the reconciliation verdicts, the
> owner-gated boundary, the stage map, navigation, anti-patterns.
> Bootstrap source: `CANONSIM_FRONTEND_WEB_AGENT_PACK_FINAL_v1_3.zip`
> (external implementation-contract pack, ingested iter-288) —
> preserved verbatim as historical evidence in `archive/`, never
> re-ingested wholesale. The binding distilled law is
> `docs/FRONTEND_WEB_LAW.md` (D-243); this file navigates and
> reconciles — it never restates an owner (D-024). Update it only
> when the stage, a boundary, or a verdict changes — never as a
> narrative log.

## 1. Identity

The web-frontend track owns the **browser client of the Workbench**:
React + TypeScript + Vite, Web/PWA-first (the pack's stack decision
v1.7 — the DECIDED external claim; the repo-side authority state in
§5), Tauri 2 optional/deferred, Canvas/WebGL scene-only. The client
is a **presentation layer, never an authority**: semantics stay in
CanonSim/Python; the Workbench application/gateway stays the
application boundary; the Visual Scene IR stays renderer-neutral;
the browser is an **untrusted downstream presentation client**.

```text
CanonSim simulation core
  → Python Workbench application + Gateway
    → canonical/read-side contracts + Visual Scene IR
      → React + TypeScript (typed, validated, replaceable)
        → Vite → Web / PWA-first
          (DOM/CSS chrome; Canvas/WebGL scene-only)
```

INV-4's envelope is untouched by the track: the browser dials the
EXISTING inbound loopback gateway binding
(`workbench/api/transport.py`, `POST /op`) — a gateway client like
the Redot shell before it, never a fourth network surface.

## 2. Non-negotiable rules

- The full distilled law: `docs/FRONTEND_WEB_LAW.md` — §2 the S0
  gate, §3 the gateway seam, §4 dual-read, §5 connection budget/
  stream admission, §6 browser runtime bounds, §7 surface modules,
  §8 effective-state closure, §9 analytical UX, §10 visual proof,
  §11 tooling floor, §14 the migration sequence.
- One-line invariants: no second execution engine / event bus /
  truth authority in React; no raw JSON into components; no browser
  storage as canon; no invented gateway routes; no SSE/WebSocket
  before their gateway contract; live tail never presented as
  durable history; auth material never in URLs.
- Authority precedence (the pack's own routing law): active repo
  binding law > current implementation/tests > the pack's derived
  web contract > historical source-workbench > Redot reference.

## 3. The reconciliation verdicts (iter-288, against HEAD `ae2fa3d`)

| Pack claim class | Verdict against the live repo |
|---|---|
| The gateway seam: `POST /op`, RequestEnvelope/ResponseDocument/EventEnvelope, closed vocabularies, `session.create/get/attach/detach/events` + `app.status`, `RESYNC_REQUIRED` | VERIFIED LIVE — every named seam exists in `workbench/api/{transport,gateway,contract}.py`; the pack's ground-truth pin `cd84069` is an ancestor and `workbench/` has ZERO diff to HEAD (all 15 intervening iterations were world-track) — the pack's snapshot is byte-current on every seam it binds |
| "No React/Vite frontend present in the repo" | TRUE at HEAD — the pack is the implementation contract for ADDING the first web client |
| Execution/artifact/Scene-IR/Observatory seams: operation/execution identity, deadlines, cooperative cancellation, truthful UNKNOWN, `ExecutionArtifact`, `workbench/scene_ir.py`, `workbench/observatory_read.py` (bounded windows, event-id cursors) | VERIFIED LIVE (the wb row family, `docs/CONTRACTS.md` §5; `docs/WORKBENCH_APP_LAW.md` / `OBSERVATORY_LAW.md` the owners) |
| The web laws: S0 gate, dual-read, connection budget, surface modules, browser runtime, effective-state closure, tooling floor | NEW LAW SURFACES — distilled into `docs/FRONTEND_WEB_LAW.md` (D-243); they bind the future web client and change nothing existing |
| The stack decision: React+TS+Vite+Web/PWA-first; Tauri optional; Redot FROZEN+archived | The pack's DECIDED claim; repo-side: the active-path half recorded as the web track's direction; the REDOT-FREEZE half OWNER-GATED (§5 — the one authority tension) |
| `repo-ground-truth/` (the pinned snapshot tree) | NOT LANDED — the live repo is the truth at zero diff; a landed copy would be a second source |
| `source-workbench/` V5.2 + `legacy-redot-reference/` | stay inside the archive zip — external-by-law (the D-200/D-218 family), provenance only |

## 4. What the pack is (the structure map)

52 files, self-verified (`checks/verify_pack.py`: 52 files, 21
required entrypoints). `docs/` — the 16 normative contracts, read in
the pack's own order (`AGENT_READ_ORDER.md`: the S0 subset first,
the full order only after S0 green). `repo-ground-truth/` — the
pinned implementation snapshot (contract/transport/gateway/
artifact/execution/scene_ir/observatory_read + 4 test files).
`source-workbench/` — the historical V5.2 derivation sources (the
app architecture, the frontend UI/visual engineering spec, the
visual presentation runtime, the Observatory/control plane, the
Redot migration package). `legacy-redot-reference/` — the Redot→web
transfer notes + the theme/script reference evidence. The manifest/
README/changelogs v1.1→v1.3 carry the pack's own evolution (v1.3
added the S0 gate, the dual-read law, the connection budget, the
tooling floor, the optional P1 config).

## 5. The owner-gated boundary (the honest list)

1. **The Redot freeze + archive** (the pack's §17, the migration
   Phase 0) — the ONE authority tension: the pack freezes Redot; the
   repo's active law (`docs/REDOT_ENGINE_INDEX.md`, the AGENT_
   NAVIGATION routing) still routes engine/frontend work through
   Redot, and `workbench/presentation/redot/` is the live Workbench
   frontend. Per `AGENTS.md` §11: never silently reconciled — the
   freeze lands only as the owner's D-row, and the pack's own §18
   re-homing family (FRONTEND_UIUX_LAW / REDOT_ENGINE_INDEX /
   AGENT_NAVIGATION / README / launcher re-routing) is migration
   Phase 1, AFTER the freeze call. Until then no Redot file is
   touched — and S0 itself excludes Redot changes, so the tension
   never blocks S0.
2. **The top-level `frontend/` tree** (the pack's §13 recommended
   structure — app/components/features/scene/state/api/design-system/
   tests) — a new top-level directory = `AGENTS.md` §8 stop &
   confirm.
3. **The `frontend-1` opening** (the S0 build) — the parked
   `docs/TASKS.md` standing row; the gate is `FRONTEND_WEB_LAW.md`
   §2; opens only after (1) and (2).
4. **Later gates** (each its own admission, never silent): SSE/
   WebSocket (the §5 admission order), a SharedWorker transport,
   Tauri 2, PWA packaging, the layout manifest/Capabilities screen
   (optional P1), the tooling floor's CI rows.

## 6. The stage map

```text
PACK INGESTED  — iter-288, DONE (this surface + the law + the archive)
S0 NOT STARTED — the walking skeleton: the four criteria
                 (typed gateway client; virtualized LIVE Trajectory
                 ≥10k; two independent POST-only tabs; the load note)
                 opens on the owner's frontend-1 call, AFTER §5's
                 (1)+(2)
POST-S0        — the full acceptance matrix + the streaming
                 admission + the tooling floor
MIGRATION      — the pack's Phase 0..6 sequence (freeze → re-home →
                 foundation → slice → world → remote/PWA → optional
                 Tauri), each phase the owner's call
```

## 7. Navigation (the authoritative owners)

| Question | Read first |
|---|---|
| the binding web law (S0, seams, dual-read, budget, surfaces) | `docs/FRONTEND_WEB_LAW.md` |
| interaction / IA / accessibility / localization / responsive | `docs/FRONTEND_UIUX_LAW.md` |
| visual system / tokens / the state matrix | `docs/VISUAL_SYSTEM_UI.md` |
| application/runtime ownership (operations, lifecycles, deadlines, model lifecycle, admission) | `docs/WORKBENCH_APP_LAW.md` |
| Observatory analytical semantics | `docs/OBSERVATORY_LAW.md` |
| Scene IR / world presentation / degradation | `docs/WORLD_PRESENTATION_LAW.md` |
| inference-control semantics | `docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md` |
| engine facts (Redot — historical/reference) | `docs/REDOT_ENGINE_INDEX.md` |
| ownership / topology | `docs/SSI_TOPOLOGY.md` |
| the pack's full contracts (only when a seam needs them) | `archive/…/docs/` — the pack's own `AGENT_READ_ORDER.md` governs depth |

## 8. Explicit anti-patterns

- Do not build a second execution engine, event bus, semantic
  authority, or trajectory log in React; do not port Cordis/dsh/
  Harness runtimes — import the quality bar only.
- Do not present the live session tail as durable history; do not
  mix LIVE/HISTORY cursors without an explicit mode switch.
- Do not implement SSE/WebSocket before the gateway contract +
  admission policy exist; no unbounded per-tab streams;
  `connection budget exhausted` ≠ gateway dead.
- Do not put browser state, `localStorage`, `BroadcastChannel`, or
  a Service-Worker cache in any authority role; each tab is an
  independent client; no leader election.
- Do not infer effective state from widget values; HTTP 200 ≠
  semantic success; UNKNOWN stays UNKNOWN; cancellation is not
  completion; `selected` ≠ `loaded`.
- Do not redesign the backend to make the frontend cleaner; do not
  remove Python gateway tests when the web client lands (additive
  CI only).
- Do not read source-workbench V5.2, the full ACCEPTANCE_MATRIX, or
  the layout manifests during S0 — the S0 subset only (the pack's
  own discipline).
- Do not treat this file or the archive as a second source of truth;
  one fact has one owner — link it.
