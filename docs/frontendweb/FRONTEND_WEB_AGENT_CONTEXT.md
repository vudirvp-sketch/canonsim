# Frontend-Web Track — Agent Context (the durable compact surface)

> What an agent needs repeatedly when working the web-frontend track:
> identity, non-negotiable rules, the reconciliation verdicts, the
> owner-gated boundary, the stage map, navigation, anti-patterns,
> the design-research method.
> Bootstrap source: `CANONSIM_FRONTEND_WEB_AGENT_PACK_FINAL_v1_3.zip`
> (external implementation-contract pack, ingested iter-288) —
> preserved verbatim as historical evidence in `archive/`, never
> re-ingested wholesale. Second source: the design-research &
> mechanism-transfer method v3 (ingested iter-292, D-246 — §9).
> The binding distilled law is
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
| The stack decision: React+TS+Vite+Web/PWA-first; Tauri optional; Redot FROZEN+archived | LANDED — D-244 (the owner's 2026-09-29 call): the freeze + the frontend-1 opening + the `frontend/` tree admission, all three §5 boundaries resolved; the S0-minimal §18 re-homing done (REDOT_ENGINE_INDEX/AGENT_NAVIGATION/README); CLOSED by DELETION at iter-290/D-245 (the owner's «удаляй redot» call: the tree + its index + its proof packets removed, the launcher re-pointed to the web dev server) |
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

## 5. The standing boundaries (post-D-244)

1. ~~**The Redot freeze + archive**~~ — RESOLVED: D-244 (the owner's
   2026-09-29 call «redot замораживаем, а возможно и вовсе
   отказываемся => делаем и работаем по [the pack]»), then CLOSED by
   DELETION at iter-290/D-245 (the owner's «удаляй redot» call): the
   tree, the engine index, the proof/contract packets, and the Setup
   launcher removed; the launcher re-pointed to the web dev server
   (the pack's §16 gate discharged by the deletion itself — a frozen
   target no longer exists); recovery: git history + the archive.
2. ~~**The top-level `frontend/` tree**~~ — RESOLVED: admitted by the
   same call (the pack's §13 structure; AGENTS §8 satisfied by the
   owner's explicit work-per-the-pack directive). LANDED at
   `frontend/` (iter-289).
3. ~~**The `frontend-1` opening**~~ — RESOLVED: the S0 build landed
   iter-289 (the four criteria; the evidence in
   `docs/iterations/iter-289-frontendweb-report.md`).
4. **Still gated** (each its own admission, never silent):
   SSE/WebSocket (the §5
   admission order), a SharedWorker transport, Tauri 2, PWA
   packaging, the layout manifest/Capabilities screen (optional
   P1), the tooling floor's CI rows.

## 6. The stage map

```text
PACK INGESTED  — iter-288, DONE (this surface + the law + the archive)
REDOT FROZEN   — iter-289, DONE (D-244: the freeze + the §18
                 S0-minimal re-homing + the frontend/ admission)
REDOT DELETED  — iter-290, DONE (D-245: the tree + its index + its
                 proof packets removed; the launcher re-pointed to
                 the web dev server; recovery: git history)
S0 LANDED      — iter-289, DONE (the four criteria evidenced: the
                 typed gateway client, the virtualized LIVE
                 Trajectory ≥10k, two independent POST-only tabs,
                 the load note — the report
                 docs/iterations/iter-289-frontendweb-report.md;
                 S0-green confirmation the owner's review call)
METHOD ROW     — iter-292, DONE (D-246: the design-research &
                 mechanism-transfer method adopted for visual/
                 interface research rows — §9 below; method, never
                 authority)
POST-S0        — the tooling floor's first row LANDED (iter-293: the
                 architecture guard — the dependency-boundary row as
                 tests/test_architecture's parity form, riding npm
                 test); THE STREAMING ADMISSION LANDED (iter-305, the
                 owner's «начни работы по SSE-контракту гейтвея»
                 call: the §5 admission order's step 2 — the explicit
                 SSE gateway contract, BACKEND FIRST —
                 workbench/api/gateway.py the §13 subscription core
                 (subscribe's dual answer under the dispatch lock —
                 the gapless replay/live boundary; the bounded
                 per-subscriber buffer with the observable overflow
                 terminal; close_subscriptions the bounded-shutdown
                 wake) + workbench/api/transport.py the GET /events
                 SSE binding (the frame vocabulary
                 stream.open/rejected/overflow/close + the event
                 frames byte-identical to session.events' replay;
                 the heartbeat cadence; the Last-Event-ID fallback;
                 the pre-stream 4xx guards + the auth-required 403 —
                 auth never rides URLs; the semantic rejection riding
                 ONE frame at HTTP 200; the bounded stop() waking
                 every writer), the contract packet
                 tests/test_sse_stream.py (24 rows: the byte parity,
                 the gapless boundary, the overflow law + its
                 always-replay invariant, the bounded shutdown, the
                 disconnect law, one-thread-per-stream); the browser
                 adapter (step 3) + the focused-tab policy (step 4)
                 the NEXT rows, each its own admission; the standing
                 gates that remain: the acceptance matrix, the
                 tooling floor's remaining rows (the CI wiring, the
                 Playwright-class multi-tab smoke)
PHASE 3        — the first row LANDED (iter-294, the owner's
                 «продолжай работы по фронтенду» delegated call: the
                 SHELL/NAV + the SESSION LIFECYCLE surface over the
                 existing six ops — the honest closure REQUESTED ->
                 ACCEPTED/REJECTED -> EFFECTIVE -> OBSERVED, G4
                 no-retry, only the active pane mounts; 59 vitest +
                 tsc + build + the live smoke against the real
                 gateway); the second row LANDED (iter-295, the same
                 delegated call: the OBSERVATORY ENTRY — the HISTORY
                 half of the dual-read law §4, over the existing
                 observatory.runs/read READ ops — the discovery scan,
                 ONE bounded window at a time with the event-id
                 cursor + next_after pagination that REPLACES the
                 window, the context strip's identity line, NO DATA /
                 NO MATCH / stale-cursor / TRANSPORT distinct, no
                 polling; 78 vitest + the 8/8 live smoke over a real
                 CLI-generated run); the third row LANDED (iter-296,
                 the same delegated call: the SETTINGS ENTRY — the
                 CONFIG world over the existing backend.settings
                 READ + backend.settings.update closed partial
                 MUTATION — §8's closure over a real persisted
                 store: the draft a REQUEST never an effective-state
                 claim, the Save ONLY the changed fields with a
                 fresh idempotency key (G4), the returned document
                 the new OBSERVED baseline, applies: next-spawn
                 verbatim, the compiled command preview read-only,
                 the verbatim DOMAIN_REJECTED lanes; 96 vitest + the
                 15/15 live smoke + the live browser closure
                 evidence); the IA REPAIR LANDED (iter-297, the
                 owner's «вперед реализовывай» call over the external
                 IA verdict, D-247: the registry SPLIT — ProductRoute
                 ≠ DiagnosticSurface, the vertical product rail +
                 the subdued Diagnostics entry with its own secondary
                 nav, the prose out of the product chrome, the
                 navigation contract amended into FRONTEND_UIUX_LAW
                 §2.1, the acceptance floor executable (the Shell/App
                 vitest rows + the guard's V1 raw-color scan, which
                 closed a standing 9-literal violation by tokenizing
                 it); 108 vitest + the live gateway/browser closure);
                 the fourth row LANDED (iter-298, the owner's
                 «продолжай работу над фронтендом» delegated call:
                 the CHAT ENTRY — the conversation world over the
                 existing chat.send/run.get/run.cancel run family +
                 model.list/model.states (the header's model line)
                 + inference.read (the §21.2 COMPACT contextual
                 projection — the effective temperature the next
                 send resolves from; the unconsumed control depth
                 loose-typed, the vocabulary never re-encoded);
                 header/viewport/composer/status, the transcript
                 per-surface VOLATILE (chat history is not canon),
                 the REQUESTED/EFFECTIVE provenance line per turn,
                 the near-bottom follow law, the call-local
                 overrides explicitly surfaced, the BOUNDED 700ms
                 poll loop (dead at terminal/TRANSPORT/unmount, the
                 re-poll explicit — G4), the messages-context rule
                 (only admitted turns + completed replies ride the
                 next send), every lane verbatim; Chat at the rail's
                 HEAD; 139 vitest + the 16/16 live smoke + the live
                 browser closure; the COMPLETED band CLOSED LIVE at
                 iter-302 — a real reply + provenance over a sandbox
                 llama.cpp, never a fabricated completion); the fifth
                 row LANDED
                 (iter-299, the owner's «продолжай работу над
                 фронтендом» delegated call: the INFERENCE ENTRY —
                 the generation-control WORKSPACE over the existing
                 inference.read/inference.update ops (the §21.2
                 regions: the preset row with the TRANSPARENT diff
                 preview + the clean-draft guard, the SEARCH over
                 name/flag/category — a match is an explicit ask
                 that shows the advanced rows, the PINNED
                 quick-access strip of reveals (a pin/unpin its own
                 dispatch over the workspace section, never a profile
                 edit), the collapsible categories with honest
                 counts (the six general-chat families open by
                 default, an all-advanced family opens with the
                 honest note), the advanced rung, the ordered
                 9-member sampler chain (membership a DRAFT edit —
                 the Save carries the WHOLE document), the compiled
                 preview read-only); the DATA-DRIVEN editors over the
                 read document's own value_type/forms/limits
                 metadata (the UI never re-encodes the vocabulary);
                 every row renders the OBSERVED state + the
                 resolver's reasons verbatim + the §4 defaults
                 ladder side by side; §8's closure over the persisted
                 profile store (the Save sends ONLY the changed keys,
                 a fresh idempotency key per attempt — G4; on
                 ACCEPTED the returned document the new OBSERVED
                 baseline, the draft reconciles to the SERVER's
                 answer); Inference right behind Chat in the rail
                 (§2.1's canonical IA tree); 174 vitest + the 11/11
                 live smoke + 4 live-captured update fixtures); the
                 sixth row LANDED (iter-300, the owner's «продолжай
                 работу над фронтендом» delegated call: the MODELS
                 ENTRY — the model family's mirror over the existing
                 model.list/model.states READs + model.load/
                 model.unload (the §20 loading half as RUNS) +
                 run.start's three model work kinds (model.fetch/
                 model.import/model.digest — identity-then-poll with
                 live progress) observed through run.get/run.cancel:
                 the §20 ladder law rendered (the row's chip is
                 model.states's own answer per name — a discovery
                 entry never proves the ladder; the ACTIVE slot is
                 the load-state owner's), the arrival pane (the fetch
                 form over the pure-string normalize gate; the import
                 form's honest web shape — ABSOLUTE paths as text, the
                 native picker the Tauri row's own concern), the §9
                 strong-identity affordance as the digest RUN (the
                 honest long arm — cancellable, observable; the
                 synchronous model.inspect stays a backend surface),
                 the terminal-triggered exactly-ONE context re-read
                 (the OBSERVED baseline, never polling), G4 fresh
                 keys + no blind retry, ONE run at a time; Models in
                 the rail right behind Inference (§2.1's canonical IA
                 tree — the RESOURCES group's head); 214 vitest +
                 the 24/24 live smoke over the served composition +
                 11 live-captured fixtures); the SEVENTH row LANDED
                 (iter-301, the owner's «продолжай работу над
                 фронтендом» delegated call: the SETTINGS SECONDARY
                 NAV — the surface's own sections over real documents
                 only, the verdict's step 5 reconciled with inf-1 by
                 the D-246 method: Deployment (the launch-settings
                 store; the raw extra_args hatch dissolves into the
                 document — §19's disclosure law) | About (the
                 gateway's own identity read-only over the EXISTING
                 app.status; the verdict's "General" re-scoped to
                 what exists — the probe console stays in
                 Diagnostics: identity here, proof there);
                 Appearance a NAMED standing boundary (no persisted
                 appearance store, browser storage never truth — the
                 guard's R3), never a fabricated empty section; the
                 DRAFT's owner the SURFACE (the container's hook) —
                 a section switch never drops the unsaved REQUEST,
                 falsified live in the browser; 221 vitest + the
                 38/38 live smoke + the browser closure); the LIVE
                 BAND CLOSURE LANDED (iter-302, the owner's
                 «продолжай работу над фронтендом» call + the
                 explicit sandbox-environment enabler «можешь
                 поставить в песочницу llama.cpp и любое окружение
                 нужное»: the declared owner-side bands CLOSED LIVE
                 over a real sandbox llama.cpp — the fetch COMPLETED
                 band (the models arriving THROUGH the gateway's own
                 model.fetch op, PROGRESS observed — the first live
                 closure after iter-300's admission-only form), the
                 models ACTIVE/EVICTED bands (through the UI's OWN
                 buttons: load → ACTIVE with the slot filled, the
                 single-slot rejection verbatim, unload → EVICTED,
                 re-selection), the chat COMPLETED band (a REAL
                 reply, finish stop, backend identity, the
                 REQUESTED/EFFECTIVE pair), the S0-4 load probe
                 measured WITH a live LLM (≈108–110 ops/s — the
                 criterion literally met), zero console errors; the
                 stale probe copy fixed — App.tsx asserted an
                 environment fact stale on the owner's own station;
                 KI#110 opened+closed — the launch-params merge test
                 assumed an empty llama.cpp discovery home, the
                 documented drop made it red, the exe rung pinned
                 hermetically; the suite green WITH the tree
                 present); the next rows the owner's call: the
                 streaming admission (SSE — the backend gateway
                 contract first), the acceptance matrix, the
                 DECISIONS collapse (the owner's call); each its own
                 iteration
MIGRATION      — the pack's Phase 3..6 sequence (slice → world →
                 remote/PWA → optional Tauri), each phase the
                 owner's call
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

## 9. The design-research & mechanism-transfer method (iter-292, D-246)

> The owner's 2026-09-29 delivery: the external method document v3
> (the Refero-derived design-research discipline, adapted to
> CanonSim), preserved verbatim at
> `archive/canonsim_design_research_and_mechanism_transfer_method_v3.md`
> (md5-pinned). Adopted as METHOD, never authority: it disciplines
> HOW the track's visual/interface research rows are researched,
> transferred, and proven — it defines no product law, no visual
> identity, no runtime semantics, no proof authority. Product
> questions stay with their §7 owners; external references inform,
> CanonSim law decides.

The binding core — five mechanisms, applied when an external
reference materially influences a design decision:

1. **Observation before interpretation.** Extract the observable
   evidence first (a stable action region, subordinate metadata,
   a non-colour state channel); adjectives ("cleaner", "premium",
   "modern") describe preference, never evidence.
2. **Mechanism, not appearance.** Every material donor pattern
   answers: what happens, why it works in the donor, what problem
   it solves, which donor assumptions are non-portable, which
   CanonSim invariant survives, which existing owner/carrier
   implements it, how transfer success is falsified. The portable
   unit is mechanism + function + boundary — never palette, page
   anatomy, or component shape.
3. **The transfer boundary.** State what STOPS at the donor
   boundary (navigation model, labels, styling, framework,
   vocabulary, architecture). Only the justified mechanism crosses.
4. **The target envelope.** A reference frame is an exemplar, not a
   pixel-perfect command: MUST PRESERVE (hierarchy, density
   relationship, semantic accent role, state visibility,
   selection/focus treatment, epistemic distinctions) vs MAY VARY
   (text length, item count, dynamic data, geometry under
   DPI/locale, supported viewport adaptation). The envelope must
   survive Cyrillic, long labels, loading/stale/failed states,
   multi-tab — visual proof compares against the envelope, never
   blind pixels.
5. **Claim → falsifier → evidence.** A material design proposition
   carries a claim, a falsifier (the observation that would disprove
   it), evidence in distinct classes (static / runtime / task /
   performance — one never impersonates another), and a disposition
   (KEEP | MODIFY | BOUND | DEFER | REJECT).

The gates: research depth scales with risk (direct build → light →
standard → deep — never a ritual quota; an approved target means
bounded direct build); references are never averaged into a generic
centroid (one primary direction, bounded secondaries); the
anti-slop questions fire on non-trivial choices (what real CanonSim
property motivates this? which invariant does it express? would the
identity survive removing the decoration?); VIS-0..3 classify
visual defects (visual classification only, never a replacement
for the project's P0–P4); a material transfer leaves the compact
record (the archive document's §27 template: TASK / OWNER / SOURCE
/ OBSERVATION / MECHANISM / FUNCTION / TRANSFER BOUNDARY / CANONSIM
INVARIANT / NATIVE CARRIER / ADAPTATION / TARGET ENVELOPE / COST /
FALSIFIER / PROOF / DISPOSITION / DURABLE RESIDUE ROUTING) in the
owning iteration's report; durable residue routes into the existing
§7 owners. The document's own §34 rejections are CanonSim's: no
parallel Refero tree or registry, no global Reference Lock, no
novelty quota, no mandatory multi-source ritual, no pixel-perfect
gate, no Refero runtime dependency — the method is valuable
precisely because it never becomes a second product system.
