# CanonSim — Redot / Godot / Agent Reference Index

**Purpose:** agent-facing reference and routing map for CanonSim Workbench and its Redot presentation/runtime layer.

**Checked:** 2026-09-24  
**Production engine baseline:** Redot 26.2 LTS (`redot-26.2-stable`)  
**Redot API reference revision:** `4f5b14abade2`  
**Project scripting baseline:** GDScript  
**Project visual baseline:** 2D / 2.5D-first; Compatibility renderer for the initial measured slice; desktop/local-AI Workbench; renderer choices remain project-owned.

This document is an **index and decision firewall**, not a substitute for the repository's owning documents or the official Redot class reference.

**Repo status:** this file IS the project's copy of the owner's external hand-off artifact `canonsim_redot_godot_agent_reference_index.md`, admitted iter-225 (the owner's 2026-09-25 call, D-207). Admission deltas against the external original — routing-level only, the engine facts untouched: §2.2/§2.3 reconciled with the repo's current surface (the v5.2 documents' external-by-law status + the in-repo owners + the wb-4..wb-8 seams); §10's skills pinned agent-side (AGENTS §2.8 — no repo-side skill trees); the external changelog section cut (history lives in git + worklog); the duplicate section-20 numbering fixed. The document rots by design — the engine facts carry the **Checked:** date above; refresh alongside the REFERENCES quarterly pass (AGENTS §6's rot family).

---

## 0. Non-negotiable agent rules

### 0.1 Authority order

Use this order for implementation decisions:

```text
CANONSIM REPOSITORY AUTHORITY
  -> owning project document / contract
  -> current implementation
  -> official Redot 26.2 class reference / docs
  -> installed Redot binary + --version / --help + runtime evidence
  -> Redot source / release / issue evidence
  -> Godot documentation as secondary cross-reference
  -> community skills / tutorials / forum material
```

The lower layers may suggest or explain a solution; they do not override the higher layers.

### 0.2 Version firewall

The project baseline is **Redot 26.2 LTS**. Never silently substitute another engine/version.

```text
Godot 4.x != Redot 26.2
Redot 26.1 != Redot 26.2
unversioned/latest docs != proof of 26.2 behavior
community example != API authority
```

For every version-sensitive API, syntax, CLI, export, rendering, networking, or runtime-behavior claim:

```text
1. identify exact target version;
2. consult Redot 26.2 class reference/docs;
3. verify installed executable/version when behavior matters;
4. if ambiguous, inspect Redot source/release/issues;
5. run a minimal proof when the claim affects implementation;
6. record architecture-changing conclusions in the owning CanonSim document.
```

### 0.3 CanonSim ownership firewall

Do not move canonical semantic state into:

- Redot `Node` hierarchy;
- `SceneTree` state;
- `.tscn` scene structure;
- `Resource`/UID identity;
- renderer objects;
- visual-only caches;
- engine RPC state;
- network transport state.

Canonical pipeline:

```text
ordered application operation / CanonSim facts
  -> typed semantic read model
  -> optional ViewModel / presentation derivation
  -> Visual Scene IR / UI state
  -> Redot presentation/runtime
```

Redot is presentation/runtime, not canonical-world authority.

### 0.4 Evidence over intuition

Never replace:

```text
"this should work"
"this should be faster"
"this is probably the right network protocol"
```

with a project decision.

Prefer:

```text
hypothesis -> minimal reproduction -> measurement/proof -> change -> regression
```

---

# 1. Current engine/version truth

## 1.1 Production baseline

Primary sources:

- Redot release list: https://github.com/Redot-Engine/redot-engine/releases
- Production tag: `redot-26.2-stable`
- Production release commit: `4f5b14a`
- Redot documentation hub: https://docs.redotengine.org/
- Versioned class reference: https://docs.redotengine.org/en/26.2/Classes

The Redot 26.2 class reference states that its API reference is synchronized from Redot Engine revision `4f5b14abade2`. Use that revision as the API evidence anchor when a behavior is disputed.

## 1.2 Godot is secondary

Current Godot release/archive reference:

- https://godotengine.org/download/archive/
- https://docs.godotengine.org/en/latest/

Use Godot for shared concepts, historical context, alternative explanations, migration background, or an example not clearly covered in Redot docs.

Before using a Godot-derived implementation detail, prove the corresponding Redot 26.2 behavior.

## 1.3 Documentation-version hazard

Redot has a versioned class-reference surface and also an unversioned/latest documentation tree. The latest tree is useful, but it is mutable.

```text
API existence / exact signature
    -> Redot 26.2 class reference

Current conceptual tutorial / explanation
    -> Redot docs tutorial tree

Behavior disputed or version-sensitive
    -> class reference + installed binary + source/release evidence
```

Do not treat a current unversioned tutorial footer or a Godot latest page as proof of Redot 26.2 API compatibility.

---

# 2. CanonSim repository sources to read first

## 2.1 Always

- `AGENTS.md` — agent operating law, invariants, Git safety, stop/confirm gates, Definition of Done.
- `docs/AGENT_NAVIGATION.md` — repository navigation and reading gradient.
- `docs/BLUEPRINT.md` — cross-cutting architecture laws and component/build index.
- `STATUS.md` — current iteration state and active work.

## 2.2 Redot Workbench

- `workbench/presentation/redot/project.godot` — live engine project configuration.
- `workbench/presentation/redot/` — current Redot-owned presentation code/assets.
- `CANONSIM_WORKBENCH_APPLICATION_ARCHITECTURE_V5_2.md` — application ownership and typed seam.
- `CANONSIM_VISUAL_PRESENTATION_RUNTIME_ARCHITECTURE_V5_2.md` — Redot runtime/presentation architecture.
- `CANONSIM_FRONTEND_UI_VISUAL_ENGINEERING_SPEC_V5_2.md` — UI/visual contract.
- `REDOT_INTEGRATION_AND_REPO_LAYOUT_V1.md` — Redot version/toolchain/repository boundary.
- `REDOT_MIGRATION_README.md` — migration/baseline notes.

The five v5.2 documents are **external by law** (the owner-supplied `canonsim_workbench_v5_2_redot_2026-09-24` package — the convenience-copy law D-024, the family admission D-200): they never live in this repo. The distilled in-repo owners of the same surface: `docs/CONTRACTS.md` §5 (the wb family contract: D1–D6, the seam chain, the family composition) + the wb rows in `docs/TASKS.md` + the `workbench/` rows in `docs/AGENT_NAVIGATION.md` §1. Do not hunt for the external files in the tree.

## 2.3 Relevant implementation seams

- `workbench/scene_ir.py` — renderer-neutral Visual Scene IR.
- `workbench/scene_build.py` — read-side scene assembly.
- `workbench/api/` — the inbound gateway (D-201): `contract.py` the envelopes + closed vocabularies, `gateway.py` the socket-free dispatch core, `transport.py` the loopback HTTP binding (INV-4's second sanctioned network module).
- `scripts/workbench_app.py` — the composition root + loopback serve (the ONE launcher; `--managed` = the launcher owns the llama-server lifecycle).
- `scripts/visual_proof.py` — Redot proof/runner tooling.
- `workbench/presentation/redot/scripts/gateway_client.gd` — the typed POST /op client (the frontend dials the GATEWAY only, never llama.cpp — G8).
- `workbench/presentation/redot/scripts/shell.gd` — the application shell (the Chat/Settings/Models surfaces).
- `tests/test_visual_proof.py` / `tests/test_shell_proof.py` — REDOT_EXE-gated visual proofs (skip cleanly without the binary).
- `tests/test_shell_contract.py` — the committed `.gd` file contract (the adjacent-literal ban among its pins).
- `tests/test_gateway.py` / `tests/test_workbench_app.py` / `tests/test_backend_row.py` / `tests/test_managed_backend.py` — the gateway/launcher/backend/managed claim packets.

## 2.4 Engine boundary

Redot may transform and display information derived from CanonSim, but must not become an alternate source of semantic truth.

---

# 3. Official Redot reference stack

## 3.1 Redot 26.2 class reference — primary API source

https://docs.redotengine.org/en/26.2/Classes

Use this for:

- class existence;
- inheritance;
- methods;
- properties;
- signals;
- constants/enums;
- annotations;
- exact API names/signatures;
- version-sensitive engine behavior.

The class index currently includes dedicated Redot MCP classes, WebSocket/WebRTC networking, threading primitives, performance/runtime services, and the normal 2D/UI stack.

## 3.2 GDScript / syntax

Primary:

- https://docs.redotengine.org/en/26.2/Tutorials/scripting/gdscript/gdscript_basics
- https://docs.redotengine.org/tutorials/scripting/gdscript/gdscript_styleguide
- class reference: `GDScript`, `@GDScript`, `Callable`, `Variant`, `StringName`

Use for:

- typed GDScript;
- annotations;
- signals/callables;
- `await`;
- properties/getters/setters;
- lifecycle methods;
- static typing/warnings;
- current built-in methods/types;
- exact language syntax.

The Redot 26.2 GDScript reference is explicitly the language reference for Redot. Do not assume Python semantics merely because the syntax is Python-like.

**Agent rule:** for syntax questions, prefer the exact 26.2 language reference over memory or a generic Godot snippet.

**Pinned 26.2 JSON laws (obs-2, D-217 — each found by a live runtime failure, never by memory):**

- `JSON.parse(text)` is an INSTANCE method in 26.2 (the 4.3+ JSON
  rework); the static form is `JSON.parse_string(text)` — a Variant
  (or null on parse failure), never a `result`/`error` pair.
- `JSON.parse_string` parses EVERY number as a **float** (typeof 3):
  `"seed": 42` arrives as `42.0`, and `str(42.0)` renders `"42.0"` —
  canonical integers must normalize (`_int_text`/`_normalize_numbers`
  in observatory.gd; JSON.stringify of a float-parsed dict carries
  the same hazard).
- JSON `null` is a PRESENT key with a null value — `dict.get(k, "")`
  never fires its default, and `String(null)` is a runtime error:
  the null arm must be explicit.
- a `GridContainer` column whose cells set only `clip_text` (min
  width 0) collapses to zero width — the value cells need
  `SIZE_EXPAND_FILL` (the question-contract pattern).

## 3.3 Scene / resource model

Use the Redot class reference for:

- `Node`
- `SceneTree`
- `PackedScene`
- `Resource`
- `ResourceLoader`
- `ResourceSaver`
- `ResourceUID`
- `SceneState`

Conceptual resource tutorial:

- https://docs.redotengine.org/tutorials/scripting/resources

Canonical rule:

```text
Redot Resource/Scene
    = presentation/configuration/storage mechanism
    != CanonSim semantic truth store
```

## 3.4 UI / controls

Core classes to route to:

- `Control`
- `Container`
- `BoxContainer`, `HBoxContainer`, `VBoxContainer`
- `GridContainer`
- `MarginContainer`
- `PanelContainer`
- `ScrollContainer`
- `SplitContainer`, `HSplitContainer`
- `TabContainer`, `TabBar`
- `Tree`, `TreeItem`
- `ItemList`
- `RichTextLabel`
- `Label`, `LabelSettings`
- `LineEdit`, `TextEdit`
- `Button`, `MenuButton`, `PopupMenu`
- `TextureRect`
- `Theme`, `ThemeDB`
- `StyleBox`, `StyleBoxFlat`, `StyleBoxTexture`
- `Window`, dialogs/popups as relevant

Use class reference:

https://docs.redotengine.org/en/26.2/Classes

Read the project UI spec before altering layout, theme, navigation, component ownership, or visual state.

## 3.5 Input / focus / touch

Conceptual guide:

- https://docs.redotengine.org/tutorials/inputs/input_examples

Core classes:

- `Input`
- `InputMap`
- `InputEvent`
- `InputEventScreenTouch`
- `InputEventScreenDrag`
- `Viewport`
- `Control`
- relevant mouse/key event classes

Verify independently:

```text
keyboard
mouse
touch
resize/orientation
focus/navigation
handled vs unhandled input
```

Mobile UI is not simply desktop UI at a smaller size.

## 3.6 2D / visual runtime

Core classes:

- `CanvasItem`
- `Node2D`
- `Sprite2D`
- `AnimatedSprite2D`
- `SpriteFrames`
- `Camera2D`
- `CanvasLayer`
- `CPUParticles2D`
- `GPUParticles2D`
- `Shader`
- `ShaderMaterial`
- `MultiMesh`
- `MultiMeshInstance2D`

Do not introduce a 3D-first architecture unless an explicit CanonSim project decision changes the visual baseline.

## 3.7 Window / display / DPI / platform

Route to:

- `DisplayServer`
- `Window`
- `Viewport`
- `DPITexture`
- `SystemFont` / `FontFile` / `FontVariation`

Also consult the relevant Redot docs for:

- multiple resolutions;
- anchors/offsets/containers;
- display scaling;
- platform/window behavior;
- font rendering.

## 3.8 Export / target platforms

Use Redot export/platform documentation and verify against the installed 26.2 toolchain:

- https://docs.redotengine.org/tutorials/export/
- https://docs.redotengine.org/about/system_requirements
- Android / iOS / Web platform sections under the Redot documentation hub.

Do not infer export capability from Godot export docs without a Redot compatibility check.

Redot's current documented smartphone requirements distinguish native and web targets and include separate renderer/GPU requirements; validate the target device/runtime rather than assuming desktop parity.

---

# 4. Networking reference — Redot 26.2

## 4.1 First decide what is actually being networked

CanonSim Workbench remote control is primarily **application control and state/event delivery**, not multiplayer game replication.

Default conceptual split:

```text
Workbench Gateway
  HTTP      -> discovery / health / bounded request-response
  SSE       -> one-way event stream where sufficient
  WebSocket -> bidirectional commands + live events/state

Redot MultiplayerAPI / ENet
  -> only when true Redot multiplayer semantics are needed

WebRTC
  -> only when P2P/NAT traversal/direct data channels materially solve a requirement
```

Do not choose ENet just because the client is a game engine.

## 4.2 WebSocket — primary Redot-side transport candidate

Core Redot classes:

- `WebSocketPeer`
- `WebSocketMultiplayerPeer`
- `PacketPeer`
- `MultiplayerPeer` where relevant

Class reference:

https://docs.redotengine.org/en/26.2/Classes

For custom Workbench protocol, prefer `WebSocketPeer` and an application-level envelope over engine RPC.

Recommended envelope concepts:

```text
request_id
session_id
operation
payload
client_revision / cursor
expected_server_revision (when needed)
capabilities
```

Required protocol behavior:

- request identity;
- bounded payload size;
- bounded queue depth;
- timeout policy;
- ping/heartbeat;
- reconnect;
- replay or resync;
- deterministic duplicate handling;
- explicit auth/session lifecycle;
- explicit server revision/order semantics;
- no secret leakage through logs/diagnostics.

The Redot WebSocket API requires regular polling and supports `ws://` / `wss://`; use the 26.2 reference for exact methods and state handling.

## 4.3 HTTP/HTTPS — client-side Redot references

Relevant Redot classes:

- `HTTPClient`
- `HTTPRequest`
- `JSON`
- `StreamPeerTCP`
- `StreamPeerTLS`
- `TLSOptions`
- `X509Certificate`
- `TCPServer` when a true TCP listener is required

**Do not invent or import an `HTTPServer` class from generic Godot material.** The Redot 26.2 class index lists `HTTPClient` and `HTTPRequest` but not `HTTPServer`; if the Workbench needs an HTTP server, use the already-owned application gateway outside Redot rather than creating a parallel server inside the frontend.

This distinction is important for agent accuracy.

## 4.4 ENet / high-level multiplayer

Relevant classes:

- `ENetMultiplayerPeer`
- `ENetConnection`
- `ENetPacketPeer`
- `MultiplayerAPI`
- `SceneMultiplayer`
- `MultiplayerSpawner`
- `MultiplayerSynchronizer`

Use only when the feature is actually Redot multiplayer.

Do not use it as the default Workbench remote API because:

- the Workbench is an application, not a networked game world;
- browser/mobile-web clients cannot directly speak raw ENet;
- application-level auth/replay/idempotency still need to be designed separately.

## 4.5 WebRTC / NAT traversal

Relevant classes:

- `WebRTCPeerConnection`
- `WebRTCMultiplayerPeer`
- `WebRTCDataChannel`
- `WebRTCPeerConnectionExtension`

WebRTC normally requires signaling and ICE/STUN/TURN configuration.

Use it when:

- direct P2P is materially useful;
- relay infrastructure is acceptable;
- a signaling service is available;
- NAT traversal behavior is a real requirement.

Otherwise, application WebSocket over HTTPS/WSS is simpler for Workbench control.

## 4.6 TLS / secure transport

Relevant classes:

- `StreamPeerTLS`
- `TLSOptions`
- `X509Certificate`
- `WebSocketPeer`

Remote production mode should use TLS/WSS.

Never disable certificate verification solely to make a remote connection work.

Development exceptions must be explicit, temporary, and never silently become the production default.

## 4.7 LAN discovery

Preferred user-facing mechanism:

```text
PC Workbench
  -> "Pair phone"
  -> short-lived pairing record
  -> QR code
  -> phone scans
  -> mobile UI connects
```

Do not make the user manually discover IP addresses unless an advanced mode is explicitly requested.

Possible implementation layers:

- gateway-level interface inspection;
- explicit LAN endpoint advertisement;
- QR bootstrap;
- optional UDP discovery only if it materially improves UX.

Discovery is a convenience layer, not an authentication system.

---

# 5. Remote phone -> PC patterns

The target UX is: **PC runs Workbench; phone can control/inspect it from home LAN or from anywhere on the Internet without manual router surgery.**

## 5.1 Pattern A — same LAN / Wi-Fi

```text
Phone browser / companion client
   -> HTTP / WSS
   -> PC LAN address
   -> Workbench gateway
   -> application operations
```

Best UX:

```text
[Pair phone]
   -> show QR
   -> phone scans
   -> one-time bootstrap credential
   -> mobile interface opens
```

Security requirements:

- LAN mode opt-in;
- authenticated pairing;
- short-lived bootstrap token;
- revocation;
- no assumption that LAN is trusted.

## 5.2 Pattern B — private remote / owner-only

**Tailscale Serve** is a strong private-overlay pattern.

References:

- https://tailscale.com/docs/features/tailscale-serve
- https://tailscale.com/docs/reference/tailscale-cli/serve
- https://tailscale.com/docs/reference/examples/serve
- https://tailscale.com/docs/use-cases/application-testing/share-local-dev-server-with-team

Tailscale Serve routes traffic from devices in the same tailnet to a local service and can terminate HTTPS; Tailscale access-control rules also apply. The phone must participate in the tailnet.

Use when:

- it is acceptable to install Tailscale on PC and phone;
- private/owner-only access is desired;
- the user wants no manual port forwarding.

This is a strong owner/developer mode.

## 5.3 Pattern C — Internet access without VPN app on phone

**Cloudflare Tunnel + HTTPS/WSS** is a strong browser-friendly pattern.

References:

- https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/
- https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/get-started/
- https://developers.cloudflare.com/cloudflare-one/faq/cloudflare-tunnels-faq/
- https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/
- https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/troubleshoot-tunnels/common-errors/

Recommended architecture:

```text
PC Workbench
  -> localhost application gateway
  -> outbound cloudflared tunnel
  -> HTTPS/WSS public hostname
  -> phone browser
```

Do not treat a public URL as authentication. Put an authentication layer in front of the application.

Cloudflare's current self-hosted-application guidance describes Access as an identity-aware layer in front of the origin and recommends establishing the Access application before publishing the tunnel route; it also documents token validation at the origin/tunnel layer.

For the project, browser-friendly remote control should normally be a **mobile web client/PWA-like surface**, not a streamed desktop framebuffer and not a requirement to install a special engine runtime on the phone.

## 5.4 Pattern D — Tailscale Funnel

References:

- https://tailscale.com/docs/features/tailscale-funnel
- https://tailscale.com/docs/reference/tailscale-cli/funnel
- https://tailscale.com/docs/use-cases/application-testing/share-local-dev-server-with-internet

Funnel makes a local service public without requiring the remote client to use Tailscale, but the current documentation labels Funnel **beta**. Treat it as a development/demo option, not the default production architecture.

## 5.5 Pattern E — direct port forwarding

Keep as advanced deployment only.

Do not make the normal user flow depend on:

- router port forwarding;
- dynamic DNS setup;
- firewall rule authoring;
- manual certificate setup;
- guessing the current home IP.

---

# 6. Remote UX architecture

## 6.1 Connection profiles

Model connection as a capability/profile, not a hard-coded mode:

```text
ConnectionProfile
  mode: LOCAL | LAN | PRIVATE_REMOTE | PUBLIC_REMOTE
  transport: HTTP | SSE | WEBSOCKET
  endpoint: resolved runtime endpoint
  auth: pairing/session credential
  tls: REQUIRED for remote/public
  capabilities: bounded operation set
  status: CONNECTING | READY | DEGRADED | OFFLINE
```

## 6.2 One user-facing connection flow

```text
Connect phone
   |
   +-- LAN available ----------> QR -> local HTTPS/WSS
   |
   +-- private remote ----------> QR -> Tailscale HTTPS
   |
   +-- public remote -----------> QR -> public HTTPS/WSS
```

The QR bootstrap should contain an expiring bootstrap token or equivalent, not a permanent password.

## 6.3 Mobile should be an application client

Do not make remote control depend on desktop streaming.

Preferred:

```text
phone UI
  -> bounded application operation
  -> Workbench gateway
  -> application owner
  -> CanonSim / LLM / state stores
  -> ordered result/event
```

Benefits:

- low bandwidth;
- better mobile UX;
- robust reconnect/resync;
- no full-frame streaming requirement;
- preserves application semantics;
- allows a browser client without a native Redot mobile build.

---

# 7. Performance / optimization reference stack

## 7.1 Primary official performance hub

https://docs.redotengine.org/tutorials/performance/

The Redot performance docs cover general optimization, server-level optimization, CPU optimization, GPU optimization, MultiMesh, shader/pipeline compilation stutter, 3D performance, and threading.

Useful topics to search from that hub:

- General optimization tips
- Optimization using Servers
- CPU optimization
- GPU optimization
- Optimization using MultiMeshes
- Reducing stutter from shader/pipeline compilations
- Using multiple threads
- Thread-safe APIs
- Optimizing 3D performance

## 7.2 Runtime measurements

Primary class:

- `Performance`

Use `Performance` monitors plus project-owned instrumentation.

Potential metrics:

- FPS/frame time;
- process time;
- physics time when applicable;
- object/node counts;
- visible objects;
- draw calls;
- render/texture/buffer memory;
- video/VRAM-related measures where available;
- pipeline compilation behavior;
- application-side queue/latency metrics.

Do not optimize from FPS alone.

Minimum benchmark record:

```text
workload
engine/build
hardware
rendering mode
baseline
metric(s)
change
after
regression threshold
artifact/evidence
```

## 7.3 CanonSim-specific performance concerns

Benchmark the real combined workload:

```text
Redot UI
+ long conversation/history
+ mostly static visual scene
+ several animated actors
+ light visual effects
+ concurrent local LLM inference on the same GPU
+ application gateway/network activity
```

Optimization must account for the shared-GPU constraint. A visual optimization that steals memory/compute from the local LLM may be a regression even when Redot FPS improves.

## 7.4 Rendering optimization

Relevant Redot concepts/classes:

- `CanvasItem`
- `RenderingServer`
- `Performance`
- shaders / `ShaderMaterial`
- `MultiMesh` where object counts justify it

Look for evidence of:

- excessive redraw;
- text/layout churn;
- texture memory pressure;
- unnecessary scene-tree work;
- shader/pipeline compilation stalls;
- excessive effects/particles;
- over-large history UI updates;
- avoidable GPU contention.

## 7.5 Threads / concurrency

Primary topics:

- Using multiple threads
- Thread-safe APIs

Primary classes:

- `Thread`
- `WorkerThreadPool`
- `Mutex`
- `Semaphore`

The Redot threading guidance explicitly warns that not every engine API is thread-safe and recommends checking the thread-safe API documentation before using built-in classes from a worker thread.

**Important for Workbench:** do not create threads just because they exist. First prove a CPU bottleneck and decide whether the work belongs in Redot or in the application layer.

The current Redot threading documentation also warns that creating runtime threads can be slow on Windows and recommends designs that avoid unnecessary runtime thread creation.

## 7.6 Low-level servers

Specialist-only references:

- `RenderingServer`
- `DisplayServer`
- `PhysicsServer2D`
- `AudioServer`

These are not default optimization targets. Use them when measurement shows that the higher-level path is the bottleneck and the complexity is justified.

## 7.7 Mobile performance

Use:

- https://docs.redotengine.org/about/system_requirements
- Redot performance hub
- relevant target-platform documentation

Proof must include a real target device where mobile performance is part of acceptance.

---

# 8. Debugging / problem-solving references

## 8.1 Primary sources

- https://docs.redotengine.org/tutorials/troubleshooting
- https://docs.redotengine.org/contributing/development/debugging/
- https://github.com/Redot-Engine/redot-engine/issues
- https://github.com/Redot-Engine/redot-engine/releases
- https://github.com/Redot-Engine/redot-engine/blob/master/CHANGELOG.md

Redot's troubleshooting documentation is the first stop for known engine/runtime problems; source/issues come after the problem has been narrowed.

## 8.2 Evidence ladder

```text
1. reproduce
2. capture exact Redot version/build
3. capture stdout/stderr/editor/runtime errors
4. capture backtrace where available
5. reduce to minimal case
6. inspect Redot 26.2 class/API reference
7. validate script/syntax with the actual Redot binary
8. run targeted/headless verification
9. inspect runtime scene/state/logs/screenshots when relevant
10. search releases/issues/source for version-specific evidence
11. patch minimally
12. rerun regression
```

## 8.3 Distinguish execution contexts

Never conflate:

- editor-only behavior;
- editor tool scripts;
- normal runtime;
- debug export;
- release export;
- headless runtime;
- Windows/Linux/macOS differences;
- Android/iOS differences;
- Web/browser differences.

The proof must run in the context in which the failure matters.

---

# 9. Agent automation and Redot MCP

## 9.1 Native Redot MCP

Redot includes a native MCP subsystem. The 26.2 class reference includes:

- `MCPBridge`
- `MCPProtocol`
- `MCPServer`

Primary reference:

- https://github.com/Redot-Engine/redot-engine/blob/master/doc/mcp-integration.md
- https://github.com/Redot-Engine/redot-engine
- https://docs.redotengine.org/en/26.2/Classes

The native MCP subsystem is highly relevant to agent workflows because the engine itself exposes an agent-facing integration surface in addition to ordinary project files. The existence of these MCP classes is confirmed in the Redot 26.2 class reference.

### Agent rule

MCP is an **inspection/execution interface**, not an architecture owner.

Preferred loop:

```text
read repository authority
  -> inspect current project
  -> verify engine/API
  -> make minimal change
  -> validate syntax
  -> run targeted test
  -> inspect logs/live state/screenshot as needed
  -> compare expected vs observed
  -> retain evidence
```

Do not let agent tooling rewrite project ownership boundaries.

## 9.2 `gda` / `godot-agent`

- https://github.com/aigengame/godot-agent
- https://github.com/aigengame/godot-agent/blob/main/src/gda/skill/SKILL.md

Useful for:

- agent-first headless inspection;
- structured project manipulation;
- scene/node/script/resource operations;
- headless verification workflows.

It is Godot-oriented. Treat it as a workflow/tooling candidate and verify Redot 26.2 compatibility before adding it as a project dependency.

## 9.3 `@vl4dt/godot-skills`

- https://github.com/vl4dt/godot-skills

The repository currently exposes a broad set of Godot-oriented skills. Treat the inventory as mutable and re-check it at use time. Useful skills:

- `godot-project-setup`
- `godot-brainstorming`
- `godot-gdscript-patterns`
- `godot-code-review`
- `godot-debugging`
- `godot-headless-workflow`
- `godot-ui`
- `godot-performance`
- `godot-animation`
- `godot-networking` when actual networking is in scope
- `godot-physics` only when physics is actually in scope
- `godot-csharp-patterns` — not admitted for the current GDScript baseline
- `godot-47-migration` — Godot-specific migration reference only; not a Redot 26.2 authority

Use these as methodology/pattern sources, never as proof of Redot 26.2 API compatibility.

## 9.4 Other useful community skill references

Retain as secondary pattern sources:

- https://github.com/wshobson/agents/tree/main/plugins/game-development/skills/godot-gdscript-patterns
- https://github.com/sickn33/agentic-awesome-skills/tree/main/skills/godot-gdscript-patterns
- https://github.com/Courtshipfy/Godot-skills/blob/main/dot_codex/skills/godot-ui-builder/SKILL.md

These are useful for pattern discovery and practical construction techniques. Reconcile all engine/API claims with Redot 26.2.

## 9.5 Agent Skills specification

- https://agentskills.io/specification
- https://github.com/anthropics/skills

Project-local skills should be small, task-specific, progressively disclosed, and versioned/tested like code.

---

# 10. Project-local skills to create/use

> These are **agent-environment** skills (the working agent's own tooling layer), never repo-side trees — this repository's law refuses repo-embedded skill directories and a second project memory (AGENTS §2.8). This index is the single repo-side carrier of their contracts.

## `canonsim-redot`

Enforce:

- Redot 26.2 baseline;
- GDScript baseline;
- engine boundary;
- version admission before API claims;
- no semantic truth in Redot structures.

## `canonsim-redot-ui`

Enforce:

- Control/container-first UI;
- theme ownership;
- mobile/touch responsiveness;
- focus/navigation;
- bounded/efficient long-history rendering;
- measured redraw/layout costs;
- project visual language.

## `canonsim-redot-networking`

Enforce:

- gateway ownership;
- HTTP/SSE/WebSocket decision table;
- LAN/private/public modes;
- auth/pairing/revocation;
- WSS/TLS for remote mode;
- reconnect/resync;
- request idempotency and revision/cursor semantics;
- bounded payloads/queues/timeouts;
- no hidden public exposure;
- explicit tunnel choice.

## `canonsim-redot-performance`

Enforce:

- benchmark before optimization;
- CPU/GPU/RAM/VRAM attribution;
- Redot `Performance` evidence;
- shared-GPU/LLM awareness;
- before/after evidence;
- regression thresholds.

## `canonsim-redot-debugging`

Enforce:

- exact engine version first;
- minimal reproduction;
- logs/backtraces;
- 26.2 API verification;
- targeted/headless test;
- source/release/issue search after narrowing;
- regression proof.

## `canonsim-redot-agent-verification`

Enforce:

- correct project path;
- correct Redot executable;
- version check;
- syntax validation;
- deterministic test entry points;
- runtime health check;
- screenshot/scene inspection where needed;
- artifact capture.

## `canonsim-redot-visual-ir`

Enforce:

- Visual Scene IR remains renderer-neutral;
- canonical facts remain canonical;
- no Redot state leaks backward into semantic layers;
- predictable asset/resource mapping;
- graceful/declarative visual degradation.

---

# 11. Version-admission protocol

Before implementing a new engine/API feature:

```text
A. Identify pinned engine: Redot 26.2 LTS.
B. Identify exact class/method/property/signal/CLI item.
C. Search the versioned Redot 26.2 class reference.
D. If unclear, inspect the release/tag/source.
E. Check release notes/issues for version-specific changes.
F. Run a minimal proof with the installed executable if behavior matters.
G. Only then incorporate the feature.
H. Record architecture-level discoveries in the owning project document.
```

For a Godot-only result:

```text
Godot claim
  -> locate corresponding Redot concept/class
  -> verify in Redot 26.2 reference/source
  -> minimal runtime proof if material
  -> only then implement
```

For drift-sensitive community skills:

```text
skill repository
  -> pin/record commit when admitted as a project dependency
  -> inspect skill content
  -> reconcile API claims with Redot 26.2
  -> test tool against actual project
```

Do not rely on mutable `main` branch content as permanent project evidence without recording the revision.

---

# 12. Mandatory API-proof checklist

When an agent proposes an engine/API-specific change, require these fields in its internal work record or final task evidence:

```text
ENGINE = Redot 26.2 LTS
API = exact class/method/property/signal
SOURCE = exact versioned Redot reference URL or source revision
CONTEXT = editor/runtime/headless/export/platform
PROOF = syntax/runtime/test evidence
ASSUMPTIONS = any remaining uncertainty
```

For performance claims:

```text
WORKLOAD
BASELINE
MEASURED METRIC
CHANGE
AFTER
REGRESSION THRESHOLD
```

For networking claims:

```text
CLIENT TYPE
NETWORK LOCATION
TRANSPORT
TLS
AUTH
RECONNECT
RESYNC
EXPOSURE MODEL
TEST RESULT
```

---

# 13. Standard test matrix for Redot-facing work

| Area | Minimum proof |
|---|---|
| GDScript syntax | Actual Redot 26.2 parser/syntax validation succeeds |
| Scene/resource | Project loads; target scene/resource resolves |
| UI | Launch + target interaction + resize check |
| Mobile UI | Touch/focus + narrow viewport/orientation behavior where applicable |
| Visual | Deterministic screenshot/proof when visual contract matters |
| Performance | Before/after measured workload + selected monitors |
| LAN networking | Phone/client connects and executes bounded operation |
| Remote networking | External-network client connects through chosen tunnel |
| Auth | Missing/invalid/expired credential rejected |
| TLS | Valid TLS/WSS path verified for remote mode |
| Reconnect | Connection loss/recovery does not duplicate/corrupt operations |
| Version | Proof confirms intended Redot executable/build |
| Export | Tested export behaves correctly for supported features |

---

# 14. Remote networking test matrix

```text
NET-LAN-01
PC + phone on same LAN
-> pair via QR
-> health
-> read-only operation
-> bounded mutation
-> verify result/order

NET-LAN-02
LAN interruption
-> reconnect
-> stream resume or explicit resync
-> no duplicate mutation

NET-REMOTE-01
PC home network -> phone on unrelated mobile/Internet network
-> HTTPS/WSS through chosen tunnel
-> health/read/mutate

NET-REMOTE-02
Tunnel interruption/restart
-> client becomes DEGRADED/OFFLINE
-> reconnect
-> no phantom duplicate execution

NET-REMOTE-03
Invalid/expired pairing credential
-> reject
-> no partial execution

NET-REMOTE-04
Malformed or oversized payload
-> bounded rejection
-> deterministic connection behavior
-> no uncontrolled memory growth

NET-REMOTE-05
Slow mobile connection
-> bounded queue
-> backpressure/compaction/resync behavior
-> no unbounded RAM growth

NET-REMOTE-06
Local LLM actively generating
-> remote control remains responsive within project budget
-> no uncontrolled resource starvation
```

---

# 15. Anti-confusion prompts for agents

When an agent says:

> Godot supports X.

Force the following check:

```text
Which Godot version?
Which Redot version?
Which exact Redot class/method?
Is it present in the 26.2 class reference?
Is it runtime/editor/headless/platform-specific?
Was the behavior actually tested?
```

When an agent says:

> This should be faster.

Force:

```text
metric
workload
baseline
change
measured result
regression threshold
```

When an agent says:

> Expose the app to the phone.

Force:

```text
LAN or Internet?
private or public?
browser or native client?
transport?
TLS?
auth?
pairing?
reconnect/resync?
message bounds?
reverse proxy/tunnel?
```

When an agent says:

> Use an engine multiplayer API.

Force:

```text
Is this actually gameplay replication?
Or is it application control/state delivery?
If application control: why not gateway + HTTP/SSE/WebSocket?
```

---

# 16. External references by purpose

## Official Redot — authority

- https://docs.redotengine.org/
- https://docs.redotengine.org/en/26.2/Classes
- https://docs.redotengine.org/en/26.2/Tutorials/scripting/gdscript/gdscript_basics
- https://docs.redotengine.org/tutorials/scripting/gdscript/gdscript_styleguide
- https://docs.redotengine.org/tutorials/scripting/resources
- https://docs.redotengine.org/tutorials/inputs/input_examples
- https://docs.redotengine.org/tutorials/performance/
- https://docs.redotengine.org/tutorials/troubleshooting
- https://docs.redotengine.org/about/system_requirements
- https://github.com/Redot-Engine/redot-engine
- https://github.com/Redot-Engine/redot-engine/releases
- https://github.com/Redot-Engine/redot-docs
- https://github.com/Redot-Engine/redot-demo-projects
- https://github.com/Redot-Engine/redot-cpp
- https://github.com/Redot-Engine/redot-engine/blob/master/doc/mcp-integration.md

## Remote access / networking infrastructure

- https://tailscale.com/docs/features/tailscale-serve
- https://tailscale.com/docs/reference/tailscale-cli/serve
- https://tailscale.com/docs/reference/examples/serve
- https://tailscale.com/docs/features/tailscale-funnel
- https://tailscale.com/docs/reference/tailscale-cli/funnel
- https://tailscale.com/docs/use-cases/application-testing/share-local-dev-server-with-team
- https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/
- https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/get-started/
- https://developers.cloudflare.com/cloudflare-one/faq/cloudflare-tunnels-faq/
- https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/
- https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/troubleshoot-tunnels/common-errors/

## Agent tooling / skills

- https://github.com/aigengame/godot-agent
- https://github.com/aigengame/godot-agent/blob/main/src/gda/skill/SKILL.md
- https://github.com/vl4dt/godot-skills
- https://github.com/vl4dt/godot-skills/blob/main/skills/godot-ui/SKILL.md
- https://github.com/vl4dt/godot-skills/blob/main/skills/godot-performance/SKILL.md
- https://github.com/wshobson/agents/tree/main/plugins/game-development/skills/godot-gdscript-patterns
- https://github.com/sickn33/agentic-awesome-skills/tree/main/skills/godot-gdscript-patterns
- https://github.com/Courtshipfy/Godot-skills/blob/main/dot_codex/skills/godot-ui-builder/SKILL.md
- https://agentskills.io/specification
- https://github.com/anthropics/skills

## Godot secondary reference

- https://docs.godotengine.org/en/latest/
- https://godotengine.org/download/archive/

---

# 17. Suggested agent routing matrix

| Task trigger | Read first | External authority | Local skill |
|---|---|---|---|
| Any Redot change | project authority + current implementation | Redot 26.2 class reference | `canonsim-redot` |
| GDScript syntax/API | owning component | Redot 26.2 GDScript/class reference | `canonsim-redot` + `godot-gdscript-patterns` |
| UI/layout/theme | UI spec + current scene/component | Redot UI classes | `canonsim-redot-ui` + `godot-ui` |
| Touch/mobile UI | UI spec | Redot input/display classes + target platform docs | `canonsim-redot-ui` |
| Visual Scene/asset mapping | visual runtime spec + Scene IR | Redot 2D classes | `canonsim-redot-visual-ir` |
| Startup/scene problem | migration/integration contract | Redot troubleshooting + CLI/help | `canonsim-redot-debugging` |
| API not found / syntax error | current code + version | 26.2 class reference + installed binary | `canonsim-redot-debugging` |
| Headless/proof task | proof scripts/tests | Redot CLI + actual executable | `canonsim-redot-agent-verification` + `godot-headless-workflow` |
| Screenshot/visual regression | visual spec + proof tooling | Redot runtime/CLI | `canonsim-redot-agent-verification` |
| Performance/stutter/VRAM | performance benchmark/contract | Redot performance docs + `Performance` | `canonsim-redot-performance` |
| Threading | workload owner | Redot threading/thread-safe docs | `canonsim-redot-performance` |
| LAN phone connection | application gateway owner | Redot HTTP/WebSocket references | `canonsim-redot-networking` |
| Internet remote phone | gateway + exposure profile | Tailscale/Cloudflare docs + Redot WebSocket/TLS refs | `canonsim-redot-networking` |
| Multiplayer gameplay | runtime architecture | ENet/MultiplayerAPI/WebRTC refs | `canonsim-redot-networking` |
| Export/package | packaging contract | Redot export/platform docs | `canonsim-redot-agent-verification` |
| GDExtension | dependency-admission gate | Redot GDExtension/source/release | specialist review only |
| Architecture change | owning CanonSim docs | Redot only for feasibility | project-specific owner skill |

---

# 18. Compact delegation preamble

Use this when assigning a Redot task to an agent:

> Work on CanonSim Workbench against the pinned Redot 26.2 LTS baseline. Read repository authority and the owning CanonSim document first. For engine/API facts use the versioned Redot 26.2 class reference and, where needed, the installed Redot binary/source at the pinned release. Use Godot documentation only as secondary cross-reference; never assume Godot 4.x equals Redot 26.2. Preserve the semantic boundary: CanonSim facts/events -> typed read model -> Visual Scene IR/UI state -> Redot. Treat Redot as presentation/runtime, not canonical state. For networking, treat the Workbench application gateway as owner; choose HTTP/SSE/WebSocket by actual need, and make LAN/private/public exposure explicit, authenticated, bounded and testable. For remote Internet access prefer an outbound tunnel pattern over manual port forwarding; evaluate Tailscale Serve for private access and Cloudflare Tunnel + HTTPS/WSS for browser-friendly remote access. For performance, measure before optimizing and account for shared local-LLM GPU load. Validate with the actual Redot executable, targeted/headless tests, logs, runtime inspection and screenshots when relevant. Leave evidence of what was actually verified.

---

# 19. Non-authoritative sources / prohibited shortcuts

Do not use random tutorials, SEO articles, forum answers, old Stack Overflow snippets, or unpinned examples as primary API evidence.

Community material is useful for:

- alternate implementation ideas;
- troubleshooting hypotheses;
- pattern discovery;
- examples.

It is insufficient by itself for:

- claiming a Redot 26.2 API exists;
- changing CanonSim architecture;
- admitting a dependency;
- declaring performance success;
- deciding network exposure/security policy.

---

# 20. Current-state snapshot

At the index date:

- Redot 26.2 LTS is the production baseline.
- The versioned Redot 26.2 class reference is synchronized from `4f5b14abade2`.
- The Redot release list identifies `redot-26.2-stable` as the 26.2 LTS release.
- The current Redot 26.2 class index includes `MCPBridge`, `MCPProtocol`, `MCPServer`, WebSocket/WebRTC networking, `WorkerThreadPool`, `Thread`, `Mutex`, `TCPServer`, and `UPNP`.
- The current project contract pins Compatibility rendering for the initial 2D/2.5D slice.
- Redot 26.3+ is not production baseline until explicit project version admission.
- The strongest external agent tooling found is still predominantly Godot-oriented; use it as workflow/pattern tooling and verify Redot compatibility before dependency admission.

# 21. Practical reading rule

Do **not** feed this entire document to an agent for every task.

Route first, then load the smallest sufficient evidence set:

```text
ANY REDOT TASK
  -> canonsim-redot

UI / THEME / LAYOUT / TOUCH
  -> canonsim-redot-ui

LAN / PHONE / INTERNET / WSS / TUNNEL
  -> canonsim-redot-networking

FPS / STUTTER / VRAM / REDRAW / THREADS
  -> canonsim-redot-performance

CRASH / PARSE / API ERROR / EXPORT ERROR
  -> canonsim-redot-debugging

TEST / CI / HEADLESS / SCREENSHOT / PROOF
  -> canonsim-redot-agent-verification

VISUAL SCENE / ASSET MAPPING / CANON FACTS
  -> canonsim-redot-visual-ir
```

Then fetch only the relevant Redot 26.2 reference pages and evidence.

The intended outcome is **not a larger memory dump**. It is a routing firewall that makes the agent consult the correct source, for the correct engine version, in the correct execution context, and then prove the change.
