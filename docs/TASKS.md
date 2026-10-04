# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2. Done-detail lives in git
> history + `worklog.md` + the owning docs — never restated here (KI#7
> cleanup, iter-0v). Day-tags removed per D-029 (calendar dropped); the
> build sequence is iteration-counted (`MVP_SCOPE.md` §17).

## Track A — main (simulator, no LLM)

> The phase ladder COMPLETE — phases 0..6 all CLOSED (gates
> iter-6/26/35/54/65/102/116); `docs/ROADMAP.md` §2 the single owner of
> closed/open, README/STATUS carry one-liners only. The standing work: the
> owner-gated backlog below + the world track (`docs/worldbuild/`, D-186)
> + the SoW horizon (ROADMAP §6).

### Standing rows (owner-gated — the live queue; the ORDER owner decides,
this file owns composition, never order — D-113; every row REVALIDATED
iter-150 (D-184) + iter-197 (the second pass: every parked premise
code-verified current at HEAD, zero closures-as-dead; the done rows
collapsed to the minimal form); each build row's verification plan rides
TEST_PLAN §9's claim packet)

> The world-authoring track is NOT this queue: the setting's own plan
> (the anchor's A1/A2/A3 + the W-ladder) lives in
> `docs/worldbuild/WORLD_WORKPLAN.md` (D-186) — a separate track, never
> a second queue; a world-authoring need for engine capability lands
> HERE as a standing row on the owner's call.

- `engine-1` — DONE (iter-170 D-192 DECIDED + iter-171..174 the {3-8B, GBNF}
  experiment, move (a) CLOSED + iter-177 D-193 the BUILD LANDING):
  llama-server behind the explicit adapter (`cli/engine.py`, INV-4's
  one-module form) — the GBNF mapping repo-side (`brief/gbnf.py`), the
  `--engine` door (the file contract preserved), the failure→ladder
  mapping, the provenance manifest; the contract absorbed (CONTRACTS §4);
  the serializer contract PRESENTATION_SPEC's (iter-178). Station
  remainder: TEST_PLAN §8.5's standing gap rows + PRESENTATION_SPEC §7's
  band (the owner's next engine run). Detail: D-192/D-193 + TECH_NOTES
  §13/§13.1 + git.
- `presentation-1` — DONE (iter-178, the owner's write call on the met
  exit criterion): `docs/PRESENTATION_SPEC.md` — the model-facing
  serializer contract over the stable brief IR (the D-055 pattern's
  fourth instance), written FROM the measured results (the mapping
  table + the narrator band; st-4 ABSORBED — the call budget, the
  no-tail resolution, thinking-as-ephemeral, the Script Tax clause);
  the three consult cards integrated (intake-30 the visual fence,
  intake-32 the re-expansion mapping, intake-33 the outcome-perception
  layers — no layer changed a shape, the cross-domain confirmation).
  Detail: the spec itself + D-193's tail + git.
- `parse-2` — disambiguation buttons + multi-intent utterances, each half
  behind its own gate (PARSER_SPEC §7; sharpened iter-150): BUTTONS wait on
  a frontend consumer (mode C live play — a UI affordance, never a parser
  change); MULTI-INTENT waits on live-session evidence that real utterances
  carry N intents (one classification per document today); neither half is
  "improve the parser" — the phase-2 grammar is gate-PASSED (D-064) and the
  boundary stays closed until a named consumer opens it.
- `st-2` — the identity promotion door (pack grammar beyond `take`, the
  D-054 machine; the read-path half landed as tex-1, iter-62/D-091):
  consumer-first, PARKED — no committed pack has wanted promotion beyond
  `take` (pack-1/pack-4 built without the door: the pawn-ticket hinge and
  the seams ride ordinary events + folds); the door (and the bg-5
  counted-promotion alternative with it) waits until a pack's design names
  the beat it needs — never a speculative build.
- `scav-1` — offline compaction = scavenge with tombstones: derived-store
  entries drop with tombstones AFTER the chronicler's rollups make them
  rebuildable; committed logs never edited (INV-5). Measurement before
  mechanism, PARKED — the chronicler (iter-64) and the fold checkpoints
  (iter-80) both landed, no derived-state size problem on record; premature
  until a real long-session cost is measured (a derived-store size census
  at a named horizon) — the intake-29 admission rule applied to our own
  queue.
- `st-5` — containers: the `in` relation + entity-birth promotion
  (blueprint §7): the first real consumer decides (a pack wanting portable
  objects, a res-1 sink shape — CONCRETE since res-1 landed iter-146/D-179;
  group-scale entity birth already exists, depth-7's condensation,
  iter-93/D-127). Never a speculative build.
- `qa-1` — DONE (iter-168, the owner's chat call over the row): mypy
  --strict on `core/` 207 → 0 at zero runtime change (1885+1 green both
  ends, goldens byte-untouched); the tool stays optional per D-031 (no
  dev-dep, no CI row — enforcement the owner's call); KI#88/#89 the
  found holes (the lint-side closures routed).
- `pack-3` — the Sci-Fi setting candidate (owner sketches; REWRITTEN
  iter-150): ONE candidate for the next authored pack slot — the owner's
  call when a slot opens, against the pressure pack's post-T1 rows (the
  legal exclusion D-134, the cultures name-1, the road traffic depth-7,
  the lore hooks D-140) and the intake-20 pack-candidate consult card; a
  genre-portability experiment (the engine's universality claim, INV-3's
  substance) its natural verification framing if picked.
- `bg-6` — the SoW integration audit, owner-deferred "until unavoidable"
  (D-055): a read-only pass over Soul-of-Waifu — extension points for a
  separate simulation chat mode, where llama.cpp sits, what the frontend
  must NOT own (the dumb-terminal contract, VISION §10). Output: a
  TECH_NOTES section + the `SOW_INTEGRATION_SPEC` sketch (SPECS_BACKLOG's
  trigger-gated row — the spec itself fires only at bg-6). Never blocks
  track A.
- `doc-2` — REFERENCES.md license/URL re-verification, quarterly
  (alongside the TECH_NOTES review). Last run 2026-09-13 (iter-114 — the
  research-layer re-point + the license/URL pass; the deltas in the
  iter-114 record). Next run: the next quarterly (owner-called per
  D-022) or at a phase-6 pack intake, whichever comes first.
- `doc-3` — DONE (iter-176, the owner's declared build): the state-layer
  reassembly landed — STATUS/TASKS/worklog/README/DECISIONS/TECH_NOTES to
  their declared functions (the FAQ essays one-liners + owner links, the
  operational recipes → TECH_NOTES §14/§15, the three TASKS history
  ledgers dead, the DECISIONS collapse 31→30) + the mechanical cap guard
  LIVE (`scripts/docguard.py` + `tests/test_docguard.py` — the recurrence
  fix). Detail: the iter-176 record + git.
- `mech-2` — the agent impact surface — DONE (iter-196, the owner's
  «открывай mech 2» call; `mechanics impact --path <pack path> |
  --ref <name>` the derived reader index (the AST scan, D-118
  extended) + the exact-name reverse query (the rename-safety set)
  + the indexed-matrix pointers (D-024); bounded one-hop;
  tooling-only, stdlib-only (D-012), zero runtime change. The A/B
  falsifier RAN (iter-198; TECH_NOTES §17): the injected gate moved
  none of the three metrics — the premise refuted at scale, the
  whole-file emission wall + the silent notes paraphrase measured
  instead; the structured-patch proposal PARKED behind a minimal
  prototype; the rename-safety lint gap closed as `rename-1`.
  Detail: iter-196/198/200 + D-197 + git.
- `wb-1` — the Workbench vertical seam (the v5.2 Redot brief, the
  owner's 2026-09-24 «start development» call — the family's first
  row, CONTRACTS §5 the pre-implementation contract, D-200 the
  admission): the chain
  `known fixture → typed read model → Visual Scene IR → Redot
  composition → screenshot artifact` — the Python half
  (`workbench/scene_ir.py` + `workbench/scene_build.py` over the
  smoke fixtures, present_in_order the one presence law) and the
  Redot half (`workbench/presentation/redot/` the pinned 26.2 LTS
  project, code-built composition, `scripts/visual_proof.py` the
  REDOT_EXE operator runner). DONE (iter-215 the Python half + the
  contract; iter-216 the Redot half + the live proof — the tavern and
  province fixtures both composed and captured, the double-run PNG
  byte-diff CONFIRMED, the REDOT_EXE-gated packet skipping clean
  without the binary).
- `wb-2..wb-N` — the family's forward rows (owner-gated, each fires
  on the owner's call in the brief's own order — CONTRACTS §5's
  composition block): wb-2 the Redot shell + custom theme (frontend
  §46 Phase A) — DONE (iter-217: the semantic-token theme file + the
  code-built application shell + the Chat/Settings placeholder
  surfaces + the shell proof mode/packet; the landing record: CONTRACTS
  §5's wb-2 note + the worklog + git); wb-3 the application-operations
  skeleton (app §32 step 1: identity + execution artifact +
  directories + clock) — DONE (iter-218: `workbench/application/` the
  Python-side package — identity/artifact/directories/clock + the
  §27 dependency envelope, the 25-test claim packet; the landing
  record: CONTRACTS §5's wb-3 note + the worklog + git); wb-4 the
  inbound gateway (INV-4's owner-gated exception, its own contract
  first) — DONE (iter-219: `workbench/api/` the Python-side package —
  contract.py the §8 envelopes + closed vocabularies, gateway.py the
  socket-free dispatch core (the recorded-outcome replay, the §12.1
  outcome mapping, the ordered events + RESYNC law, the in-memory
  session-translation seed), transport.py the loopback HTTP binding —
  INV-4's second sanctioned module, D-201, the architecture-test
  exception + AGENTS §4/§8 rewording riding; the 36-test claim packet;
  the landing record: CONTRACTS §5's wb-4 note + the worklog + git);
  wb-5 the minimal application operations (app §32 step 5) — DONE
  (iter-220, the owner's «продолжай работу» continuation call:
  workbench/application/operations/ the Python-side package —
  lifecycles.py §11's four closed state machines, execution.py §12's
  absolute deadline + cooperative cancellation + the in-memory run
  registry over the §10 artifact-before-side-effects freeze,
  models.py §20's discovery half + the one real work kind (the
  chunked digest), composition.py §6.1's single wiring owner
  registering run.start/get/cancel + model.list/inspect — chat.send
  honestly NOT registered (the backend row's consumer, the
  admission law) + the gateway's two targeted edits
  (OperationRejected the public rejection carrier, OperationEffects
  the session-scoped event surface); the 46-test claim packet; the
  landing record: CONTRACTS §5's wb-5 note + the worklog + git);
  wb-6 the backend row (app §32 step 7 — capability-aware
  inference/configuration + model identity/loading; the owner's
  «подключи llama.cpp» call, the row that closes chat.send's
  admission-law deferral) — DONE (iter-221:
  `workbench/application/operations/backend.py` the backend family's
  module — the typed `BackendPort` (props/chat/load_model/unload_model,
  the physical owner `cli/engine.py`'s LlamaServerClient satisfying it
  structurally, never imported — INV-4's two-surface form untouched)
  + `chat.send` (the §19.1 REQUESTED→ACCEPTED→EFFECTIVE→OBSERVED walk
  over the wb-5 run registry — identity-then-poll, the failed props
  probe the honest «unavailable» note) + `model.load`/`model.unload`
  (§20's loading half — the Model ladder walked on OBSERVED outcomes:
  ACTIVE on success, FAILED on the observed refusal — the terminal
  FAILED the recorded ladder gap, D-203 — SELECTED rest on the
  unknown outcome, EVICTED→SELECTED the re-selection) + the engine
  adapter's model-management half (POST /models/load +
  /models/unload — build-sensitive research evidence, the stub-pinned
  wire shapes, the live re-verification a station row) + the
  composition's `backend=` wiring (the three operations registered
  only when the port is injected — the admission law's honest form
  continued); the 28-test claim packet
  (tests/test_backend_row.py: the port conformance over the live
  stub server, the layer walk, the cancellation trio, the deadline
  terminal, the load/unload walks incl. the unknown-outcome rest, the
  direct-vs-HTTP parity over the new surface, the byte-deterministic
  pair, the cross-PYTHONHASHSEED pair, the import-closure scan) +
  test_engine.py's four management adapter pins; the landing record:
  CONTRACTS §5's wb-6 note + the worklog + git);
  wb-7 the live chat circuit (frontend §46 Phase A's Chat row — the
  Chat surface's real machinery over the gateway + app §22's
  launcher; the owner's «продолжай работу по wb 7» + «могу ли я
  подключить llama.cpp к реготу» call) — DONE (iter-222:
  scripts/workbench_app.py the composition root + loopback serve —
  the ONE launcher assembling the gateway + the operations + the
  injected llama.cpp backend port (the two sanctioned surfaces meet
  only there) + LoopbackHttpTransport on 127.0.0.1:8765, the
  honest --no-backend admission form, the startup health probe
  evidence-not-gate; the Redot half — presentation/redot/scripts/
  gateway_client.gd the typed POST /op client (the sequential queue,
  NO endpoint of its own) + shell.gd's live circuit (app.status →
  session.create → chat.send → the run.get poll to the truthful
  terminal; Stop = run.cancel; the honest NOT CONNECTED/refusal/
  failure notes; the bounded message list) + project.godot's
  canonism_workbench/gateway/url default; tests/test_workbench_app.py
  the 8-test claim packet (the end-to-end chat over HTTP against the
  live stub llama-server + the dead-endpoint FAILED close) +
  test_shell_contract.py's three G8 pins; the landing record:
  CONTRACTS §5's wb-7 note + the worklog + git);
  wb-9 the model-flow row (frontend §46 Phase A's Models/Settings
  real-surface half + app §11.1's managed default + §20's arrival
  half — the owner's 2026-09-26 «открыл воркбенч, зашел и загрузил
  модель» + «подтянуть модель откуда угодно» + «настройки запуска
  llama.cpp... сэмплеры всякие» calls) — DONE (iter-226: the D-208
  third network surface workbench/platform/model_fetch.py + the
  model.fetch work kind with live progress + the launch-settings
  family (settings.py + backend.settings ops + the persisted
  workbench/runtime/settings.json) + the runtime layout decision
  (workbench/runtime/{models,llama.cpp}/) + workbench_app.py's MANAGED
  default + the exe auto-discovery + scripts/workbench_launch.py the
  one-command launcher + shell.gd's real Settings surface + the Models
  manager; the 35-test claim packet; detail: CONTRACTS §5's wb-9 note +
  D-208 + the worklog + git);
  wb-10 the owner-experience row (the owner's 2026-09-25 fix list
  over the wb-9 handback: the launcher's Popen `buffering` TypeError +
  «редот у меня такой …\Redot_v26.2-stable_windows_win64, где найти
  redot.exe и как его подключить?» + «просто открывающийся проводник
  и выбор уже скаченных локальных моделей» + «пользователь не должен
  вводить команды чтобы запустить или скачать что-либо!» +
  «интерфейс вверх убожества») — DONE (iter-227: the launcher rework —
  bufsize, the folder-aware Redot resolution with the persisted
  launcher.json + the Desktop-shaped auto-scan + the native tk picker,
  the observed bind URL forwarded to the Redot child, the bare "--"
  stripped; the model.import work kind — the local copy with live
  progress + cooperative cancel, NO network; discover()'s models_root;
  shell.gd's native-picker Models manager with the URL fetch demoted
  to the collapsed advanced row; the theme@0.2 visual pass; the
  Workbench.bat/Workbench Setup.bat zero-command entries; the 23-test
  claim packet incl. THE REAL SPAWN integration; detail: CONTRACTS §5's
  wb-10 note + D-209 + the worklog + git);
  wb-11 the transport-chain row (the owner's 2026-09-26 report over
  the wb-10 handback: «молча висят + транспорт результ 13» + «модель
  выбрать не могу, там пусто, моделей не видно, кнопка выбрать модель
  не работает (проводник не открывается)» + the evidence «llama.cpp и
  модели запускаются штатно если отдельно запускать») — DONE
  (iter-228: model.load/model.unload as RUNS — the fast dispatch +
  the worker-thread port call + the cause on the run.get wire (§21);
  llama_process.py's pipe drains + the cross-platform stderr_tail
  (the Windows pipe wedge + '(empty)' pinned dead); shell.gd's
  run-poll circuits + the honest picker/load guards + the scan
  re-arm; the single-slot + in-flight guards; the 3-new-pin claim
  packet incl. THE DISPATCH-LOCK regression; detail: CONTRACTS §5's
  wb-11 note + D-210 + the worklog + git);
  wb-12 the token-audit row (VISUAL_SYSTEM_UI §10's queue head — the
  owner's 2026-09-25 «тема и UI все так же убоги» + «не происходит
  плавной прокрутки вниз» calls over the v5.2 plans pack) — DONE
  (iter-230: theme@0.3 — the neutral ramp re-pinned over the
  Catppuccin Mocha VALUE reference (§6 mechanisms-not-looks), ONE
  accent #89b4fa, accent_deep retired, the NavButton variation + the
  chip_busy token; + the chat's follow law on the same row — the
  smooth tween over the scrollbar's float value, the layout-settle
  await, the near-bottom gate, the follow on every role; + the
  GENERATING chip (§5's matrix state visible); detail: CONTRACTS §5's
  wb-12 note + D-212 + the worklog + git);
  the exported-Windows-build row (the owner's «по человечески сделать
  это нельзя?» — the dev form runs the project through the editor
  binary; the product form is an exported .exe over Redot export
  presets + the launcher's export-binary resolution arm) — PARKED per
  AGENTS §2.4 (a named row when the owner calls it);
  wb-9+ per the brief's §32/§46 ladders (live events +
  reconnect/resync + the idempotency/revision/lease tests at live
  scale; persistence; the frontend rows — inference, history,
  diagnostics, the CanonSim seam, asset vocabulary, the G1–G12
  gates; the VISUAL rows — wb-12+ per docs/VISUAL_SYSTEM_UI.md §10,
  each visual row its own §8 report, the functional row first).
  Never speculative — a row opens only when the owner names
  it. Engine/API facts for any wb row: `docs/REDOT_ENGINE_INDEX.md`
  (the Redot 26.2 routing firewall — read before the row starts;
  admitted iter-225, D-207). Visual/UI facts for any wb row:
  `docs/VISUAL_SYSTEM_UI.md` (the surface-driven grammar + the token
  taxonomy + the state matrix + the transplantation protocol —
  admitted iter-229, D-211).
- `ux-1` — DONE (iter-234, 2026-09-25). The §8-style report:
  TARGET PROBLEM: the P0 minimums absent — hard-coded strings,
  no motion policy, fixed-viewport bootstrap, no keyboard path
  (FRONTEND_UIUX_LAW §17/§15/§16). CURRENT PRIMITIVE: shell.gd's
  ~197 inline literals, the always-on chat tween + busy pulse, the
  bare 1440x900, focus grabbed by the nav button.
  TRANSFERRED MECHANISM: first-party (the LAW's own contracts);
  the catalog pattern preload+static lookup (Object.tr's native
  signature forbids `static func tr(` — pinned). INVARIANT: the
  wire, the theme values, the follow law's settle frame, KI#96's
  re-scan, the honest-note vocabulary all unchanged; the canonical
  protocol vocabulary (lifecycle states) renders verbatim, never
  re-worded; proof captures stay byte-identical (locale explicit-
  only, ui_state never read/written, the seam harness pins its own
  window). FILES: scripts/strings.gd (new), shell.gd, seam_proof.gd,
  project.godot, tests/{test_shell_contract.py,test_shell_proof.py}.
  EXPECTED CONSEQUENCE: ru renders natively on the owner's machine
  (OS locale), motion-doling users get static equivalents, the
  window scales below base without clipping, Esc/Ctrl+. stop a
  generation, each surface opens focused on its task entry.
  REJECT CONDITIONS: any catalog key missing in a locale; Cyrillic
  tofu/clipping; a proof-capture diff between same-arg runs; the
  gated pins drifting again. VERIFICATION STATE: STATIC_VERIFIED
  (the boundary scan + the four ux-1 contract tests, 2289+6 CI)
  + RUNTIME_VERIFIED (the five REDOT_EXE packets green 2294+1; the
  ru screenshot VLM-checked: no tofu, no clipping) + DEFERRED: the
  language picker row (the override chain suffices), the
  per-surface font-size scaling (rides the stretch scale).
- `obs-1` — DONE (iter-235, 2026-09-25). The §8-style report:
  TARGET PROBLEM: the Observatory absent even as a stub — the
  project's defining analytical surface had no frontend entry
  (LAW §25's standing resolution: "more important than polishing secondary shell surfaces
  indefinitely"). CURRENT PRIMITIVE: nothing — no nav entry, no
  regions, no grammar. TRANSFERRED MECHANISM: first-party (the LAW's
  own §3/§25 grammar — the workspace regions + the slice ladder); the hosting form — observatory.gd composes
  itself over the injected theme + the shell's _tr Callable (LAW
  §18's split seed). INVARIANT: zero dispatch, zero new transport,
  zero fabricated data (INVARIANTS 1/2); the read-only DRAFT
  lifecycle; the distinct NO DATA semantics; the evidence rungs'
  unknown as text. FILES: observatory.gd (new), shell.gd, strings.gd,
  visual_proof.py, tests ×2. EXPECTED CONSEQUENCE: the interaction
  grammar is visible and navigable — the IA reads as intent groups;
  every region exists honestly-empty, ready for the read-side seam.
  REJECT CONDITIONS: any fabricated value; a second transport or
  authority; a flat nav catalog; color-only state. VERIFICATION
  STATE: STATIC_VERIFIED (the obs-1 slice contract, the boundary-
  from-birth scan) + RUNTIME_VERIFIED (the observatory capture
  under the pinned engine, VLM-checked composition) + DEFERRED: the
  live-run feed (obs-2's own row — a READ-side seam into the
  canonical backend), selection (needs rows to select), the
  question EDITING form (the DRAFT display is the slice's truth).
- `obs-2` — DONE (iter-236, 2026-09-25). The §8-style report:
  TARGET PROBLEM: obs-1's regions were honestly empty — no data
  reached the Observatory (LAW §25's P1 continuation: the live run
  feeding the context strip + the event table over a READ-side
  seam; the selection model's first consumer, §6). CURRENT
  PRIMITIVE: nothing — no read op, no feed path, no selection.
  TRANSFERRED MECHANISM: first-party (the LAW's own §3/§4/§20/§21
  grammars) over the wb-1 read-side edge precedent
  (workbench/scene_build.py's core.log import): the seam's one home
  workbench/observatory_read.py + the ops layer
  operations/observatory.py + the shell's two-signal hosting +
  observatory.gd v0.2's feeds. INVARIANT: zero new transport (the
  loopback gateway is the only seam; the observatory never touches
  the client), zero fabricated values (every render from a feed
  document), the boundedness ceiling ONE (the op's default 50/cap
  200 — the UI re-declares nothing), the selection the event ID
  (never a row index), the authority CANONICAL rendered never
  guessed, the distinct empties (probing/NO RUNS/NO EVENTS/refused
  never collapse), only the READ rung confirms under a selection
  (a cause_id never confirms BRANCH). FILES:
  workbench/observatory_read.py (new), workbench/application/
  operations/observatory.py (new), composition.py, workbench_app.py,
  observatory.gd, shell.gd, strings.gd, visual_proof.py,
  tests/{test_observatory_read.py(new), test_shell_contract.py,
  test_shell_proof.py, test_operations.py}. EXPECTED CONSEQUENCE:
  opening the Observatory with a gateway live lists the runs, loads
  the first readable one, renders its context + rows, and a click
  opens the inspector + scopes the ladder + extends the breadcrumb;
  pagination windows the history; a corrupt log degrades honestly.
  REJECT CONDITIONS: any fabricated value; a second transport or
  authority; a UI-side page-size constant; selection by position;
  "42.0"-style float rendering; the loaded capture masquerading as
  empty. VERIFICATION STATE: STATIC_VERIFIED (the op contract's 17
  tests + the obs-2 shell contract) + RUNTIME_VERIFIED (the
  REDOT_EXE loaded capture — double-run byte-identical, distinct
  from the empty slice, VLM-verified composition incl. the
  inspector's full dump via the headless harness) + DEFERRED: the
  timeline lanes (P3), the question EDITING form (obs-3+), the
  perception/observation profiles (their own rows).
- `obs-3..obs-N` — the Observatory continuation family (each row
  owner-gated, the LAW §25 ladder): the P3 rungs after obs-2
  (timeline lanes, compare arms, semantic zoom, cross-highlighting,
  Evidence Capsules, persistent research contexts) + the question
  editing form when its consumer names itself.
- `inf-1` — DONE (iter-239, 2026-09-25). The §8-style report:
  TARGET PROBLEM: the llama.cpp generation-control surface was flat
  launch fields with no meaning layer (no categories, no AUTO, no
  ordered chain, no relations, no effective state) and Settings was
  becoming the flag browser the chip specification forbids. The
  owner's 2026-09-25 chip-workspace hand-off (the external
  `llama_cpp_chip_workspace_spec_2026-09-25.md` + the reviewed
  `флаги llama.cpp.txt` snapshot — research inputs, never vendored).
  CURRENT PRIMITIVE: the flat launch-settings fields (context/gpu/
  fa/jinja + the five sampler flags) + build_server_command's fixed
  emission. TRANSFERRED MECHANISM: the chip specification's own
  three-layer split (raw capability / semantic control / UI
  projection) over the repo's single-owner seam (settings.py's own
  store pattern, llama_process's typed surface, composition.py's
  injection seams): docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md (the
  binding owner, D-219) + workbench/application/inference.py (the
  control library — 13 controls over 5 categories; the profile
  store inference.json; the deterministic resolver — composition,
  the evidence-pinned relations, the effective-state vocabulary;
  the compiled launch surface; the migrate_launch_semantics
  one-way schema/1→settings/2+inference/1 value-preserving
  migration) + the settings store's DEPLOYMENT slim + the platform
  builder's additive params (samplers/seed/fit/kv; the legacy
  command byte-stable) + the extra_args duplicate-ownership guard +
  the gateway family (inference.read/update) + chat's BASE
  re-point (the resolver's effective temperature) + the run
  document's REQUESTED/EFFECTIVE pair + inference.gd the Inference
  surface (the control groups + the ordered chain + the state
  badges + the compiled preview + the save circuit) + the Chat
  projection row + the Settings slim + the proof injection
  (--inference-document). INVARIANT: Settings ≠ Inference Control
  (one value owner per control; the profile store the single
  semantic authority); AUTO ≠ unset ≠ disabled (the runtime's own
  forms: -ngl auto/all, -fa auto, --seed -1); the chain is ordered
  (an order change changes the emitted --samplers); temperature 0
  PRESERVES the sampler configuration (INEFFECTIVE with reasons,
  never deleted); configured-but-ineffective stays VISIBLE with the
  reason; the raw hatch never shadows a semantic control (the
  compile-time conflict, both flag forms matched); the states shown
  are the SERVER's resolution (a local edit never fabricates a
  state). VERIFICATION STATE: STATIC_VERIFIED (test_inference.py —
  26 tests: the semantic-model laws, the resolver laws, the chain
  round-trips, the backend translation, the truth layers, the store
  + migration laws, the guard, the operations; the updated
  settings/workbench_app/shell_contract/operations packets; 2335+8
  + ruff + docguard clean) + the runtime proof row (the
  --inference-document capture) as the follow-up arm. DEFERRED: the
  session override layer, capability discovery (--help registry),
  the library/pinning/search workspace, presets/scenarios/recipes/
  hardware profiles, the later capability groups (DRY/XTC/Mirostat/
  MoE/server/speculative...), seed's request scope, the chat-template
  override relation — each its own owner-gated row.
- `inf-2` — DONE (iter-240, 2026-09-26). The §8-style report:
  TARGET PROBLEM: the owner's «результат вообще неудовлетворительный!
  Очень коряво, криво и косо + далеко не все сэмплеры и настройки
  есть» report over the inf-1 slice: the library carried 13 of the
  ~85 reviewed controls (the DRY/XTC/Mirostat/Typical/Top-N-Sigma/
  penalties/MoE/loading/server/reasoning/... families all missing),
  the Inference surface COMPOSED its rows before the first read (the
  live flow rendered EMPTY category groups — only the proof-only
  injection masked it), and the UI re-encoded the vocabulary
  client-side (VALUE_SPINS + the form constants — a second source
  of truth). TRANSFERRED MECHANISM: the same three-layer split,
  completed — the library over the WHOLE reviewed snapshot (the
  §31 category ladder, every disabled/AUTO form the runtime's own
  literal), the typed relation DATA (Condition/Requires/
  EffectiveNoop — the mirostat noop pinned from the --help's own
  words, the temperature-0 deterministic noop, the family
  requires), the DATA-DRIVEN Redot workspace (the editors built
  from the read document's own value_type/forms/limits metadata;
  the rows build ON the read; search/pins/collapsible categories/
  the advanced rung/the transparent preset diff preview), the
  platform's SEMANTIC_FLAG_TABLE + build_semantic_command (the
  compile seam: field-keyed values in, flag syntax out, unknown
  fields LOUD; build_server_command byte-stable as the deployment
  path), and the workspace section (the pinned ids ride the
  profile document — one file, two named sections). INVARIANT: the
  profile document FIELD-STABLE (an inf-1 profile loads as-is; the
  5-member chain upgrades to 9 at load, the operator's order
  preserved); one value owner per control; the UI never re-encodes
  the vocabulary; the unsaved edits survive a refresh (the carried
  editor values law, the own-save exception). VERIFICATION STATE:
  STATIC_VERIFIED (test_inference.py — 34 tests: the full-library
  laws, the cross-layer vocabulary pins, the relation laws, the
  chain upgrade, the presets/pins, the compile surface, the guard
  over 138 tokens; 2344+9 / 2352+1 REDOT_EXE + ruff + docguard
  clean) + RUNTIME_VERIFIED (the --inference-document capture
  double-run byte-identical + the VLM eyeball: the pinned chips,
  the preset row, the search field, the collapsible categories with
  counts, the 9-member chain with states — the effective-state
  presentation renders). DEFERRED: the session override layer,
  capability discovery, the model-driven context awareness,
  recent/frequent ordering, scenarios/recipes/hardware profiles,
  custom preset persistence, seed's request scope, observability
  feeds — each its own owner-gated row.
- `inf-3..inf-N` — the inference continuation family (each row
  owner-gated, LLAMA_CPP_INFERENCE_CONTROL_LAW §21's ladder): the
  capability discovery + the context-aware/model-driven visibility +
  the session/preset persistence layers above, never one "advanced
  flags" bucket.
- `core-1` — the cross-cutting execution/scale research family (PARKED, owner-gated; source: the ingested suite's CORE_WORLD half, iter-311/D-251 — the archive zip's `CORE_WORLD/04+05`): C1 representation continuity (macro↔meso↔individual causal obligations under a representation change), C2 compiled/indexed execution (index-superset — no false negatives; exact verification; the same EventDraft commit path), C3 history/replay scale (measure checkpoint/replay/index-rebuild costs before touching canonical storage), C4 the LLM boundary under unusual interaction (multi-intent/novel/hidden/partially-realized/canon-conflicting), C5 shared semantic equivalence (the byte-identical replay contract the bar). RESEARCH/POC-ONLY, nothing approved runtime architecture; a row opens on a named consumer + a measured native limit + a falsifier (the world-track §2 promotion gate's form); the POC contracts open from the archive when a row fires. AMENDED iter-315 (the owner's same confirmation call): the POC contract set now opens from the 2026-10 concept-review package too (`docs/analysis/concept-review-2026-10/`, verbatim, md5-pinned) — D0/D3 as the law set (future-reachability / obligation-preserving refinement), the conserved-set definition, the observation-path probe (same prefix + elapsed world time + seed, different observation/refinement path → compare conserved obligations and reachable futures); the namespace fence pinned: review-C3/C14/C18 ↔ core-1-C1, review-C5 ↔ core-1-C2/C3, review-C1 ↔ core-1-C4 — mapped explicitly, never mechanically merged. Never a speculative build.
- `sem-1` — DONE (iter-316, R0/R1 definition + the live falsifier, zero code change; the confirmed queue's head, the owner's «sem1 открывай и так далее» call): the CONTRACT landed at CONTRACTS.md §6 — seven pinned decisions (S1 one semantic owner — the resolver circuit, the gate never re-derives; S2 the declared effect surface: per type the legal actor classes + the state-change family + the knowledge channels + the hooks + the postconditions, declared in pack data + the mechanic modules' named constants, NEVER per-draft; S3 the emit-side authority vocabulary with auth-1's input-side fence; S4 the pure non-resolving gate INSIDE `_commit` after the delta gate, before `writer.append`; S5 the two RED lanes — internal loud / external soft; S6 the anti-tautology law; S7 the `_commit` probe = a contract gap, never a production-exploit claim) + the producer map + the invariant set + THE CHEAPEST FALSIFIER RUN LIVE (Arm A: a real `wait` producer output + a `pc_01.position` teleport, schema-valid + delta-consistent → APPENDED `ev_0011`; Arm B: a producer output re-typed `year_turns` with actor `pc_01` → APPENDED `ev_0012`; the polluted log FOLDS CLEANLY — review-C1's risk demonstrated; the probe outside the repo per Rule 9, the artifact md5 228ea08bff…) + the future implementation row's minimal test set pinned (the two arms RED→GREEN, the corpus positive control byte-identical, the declaration-flip tautology guard, the two lanes, the INV-2 replay). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate). Detail: CONTRACTS §6 + the iter-316 report + git.
- `caus-1` — DONE (iter-317, R0/R1 definition + the live ablation falsifier, zero code change; the package's T1+T2 sequence, sem-1's natural pair): the CONTRACT landed at CONTRACTS.md §7 — six pinned decisions (K1 the causal spine `primary_cause + necessary_supports[] + provenance`, no graph — today's `cause` IS the primary-cause slot, provenance stays lineage never causal claims; K2 counterfactual necessity — the same-seed ablation makes the claimed outcome UNREACHABLE, replacements don't count; K3 the necessity-vs-evidence split — evidence lives in knowledge/projection/payload, never supports; K4 the ablation battery OFF-LINE only — the divergence-probe form, never a runtime gate; K5 the producer declares, the battery verifies — the read-set × the `_last_change` index (D-050) the derivation seed, a support surviving ablation is REFUTED; K6 compatibility + the no-DAG law — additive provenance-family field, INV-1/INV-5 + the consumers additive-only) + THE ABLATION FALSIFIER RUN LIVE (seed 8, the day1 theft scenario + one inserted perception step: BASE — the steal outcome `ev_0007` names as `cause` the CHRONOLOGICAL predecessor `ev_0006` (`look_around`) while the materially-REQUIRED move `ev_0005` is indistinguishable — the necessity real, measurable, UNRECORDED (review-C2's risk); ABLATE-MOVE — zero steal-family outcomes, the outcome unreachable (necessity); ABLATE-LOOK — the steal still fires (evidence, not necessity); the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned. The implementation is NOT a row — the owner opens it after accepting the contract. Detail: CONTRACTS §7 + the iter-317 report + git.
- `replay-1` — DONE (iter-318, R0–R1 definition + the live falsifier + ONE R2 KI fix — KI#111, found BY the falsifier, AGENTS §5's record-then-fix; the queue's head, the owner's «продолжай очередь с replay-1 и так далее» call — S1–S7 + K1–K6 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §8 — six pinned decisions (E1 the identity tuple, six components, mapped to live carriers — seed/prefix-digest/schema-version carried AND checked, pack-content digest / engine commit / execution-config digest the three named GAPS; E2 semantic identity ≠ continuation state — refusal vs staleness, never mixed; E3 the irreducible continuation state a CLOSED set — the cursor's own list, a new field declares its side; E4 the lifecycle proposed → accepted → durable → committed — a lost un-durable event NEVER EXISTED; E5 the crash contract over append-before-durable / post-durable / derived-state — loud detection everywhere, repair the implementation row's business; E6 `flush == durable` REJECTED — 0 fsync / 3 flush() audited, logical durability (D-139) proven, OS durability NOT) + THE FALSIFIER RUN LIVE (the test_resume corpus, seed 42, split after step 2: CONTROL byte-identity HELD — the law untouched; Arm A pack content drift, name@version unchanged → resume ACCEPTED, tails diverge from the FIRST appended event (17 vs 23 events) — review-C4's risk live; Arm B header.commit never read at resume, a foreign label accepted silently; Arm C no-fsync audit + torn tail LOUD (found KI#111 pre-fix) + lost pre-pin tail LOUD; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned. The implementation is NOT a row — the owner opens it after accepting the contract. Detail: CONTRACTS §8 + the iter-318 report + git.
- `scale-1` — DONE (iter-319, R0/R1 definition + the live measurement falsifier, zero engine change; the queue's head, the owner's «продолжай работу прошлой итерации, со scale-1 как я понимаю, и так далее» call — E1..E6 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §9 (review-C5/C6/C16/C28/D5+D6) — seven pinned decisions Q1..Q7 (the three work classes by CAUSAL DEMAND, never implementation shape / the explicit budget: exhaustion DEFERS as semantic debt, the due-work-vs-attempt split pinned / the canonical order stands — no scheduler machinery / the cohort's build-time commutativity certificate, no CRDT/MVCC / the measurement `world size × fan-out × operation → inspected/candidate/committed + wall time` as the admission instrument / locality = byte-identical canon / the four measured gap targets) + THE FALSIFIER RUN LIVE (the REAL core functions, real tavern config, synthetic scaled worlds, seed 4242: Arm A the beat's LOCAL demand pays pack-wide walks and O(|log|) folds — leverage 32,002 iterations at |log|=16k, decay 1,248 reads at N=384 for 80 zone commits; Arm B the spread pass's REGIONAL demand scans the WHOLE projection — 1,053 reads at L=320 for ONE burning location, flat in fan-out while committed is S-shaped; Arm C NO work budget exists, gated attempts vanish silently (canon-noise), the three deferral surfaces unbounded and unaccounted; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned (the battery as a counting-proxy harness, the locality T1 control, the budget-deferral law, the cohort certificate refusal, the deferral accounting). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate). Detail: CONTRACTS §9 + the iter-319 report + git.
- `speech-1` — DONE (iter-320, R0/R1 definition + the live falsifier, zero code change; the queue's head, the owner's «Продолжай очередь с speech-1 и так далее» call — Q1–Q7 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §10 (review-C8/C9/C10/C25/C26/D10) — seven pinned decisions (P1 the channel enumeration, six channels with their live carriers — canonical fact / knowledge-belief / perception-as-acquisition-face / structured speech act / narration / diagnostic trace; P2 free prose never canon — the closed documents, the checked-never-imported assertions; P3 the promotion path — candidate structure → the intent door → the resolver circuit → `_commit`, never a second door, the auth-1 fence; P4 channel isolation — an admitted structured act FROZEN against presentation retries, today the monolithic regen, the measured gap; P5 grounding scoped to atomic externally-testable assertions — the closed claim kinds, the closed halves referenced; P6 the epistemic scope law — actor/player/narrator/debug, irony a read-side composition never a write-side fact; P7 the explicit forgetting vocabulary + the C10 field homes — trust in the relations axes, status read-side, no belief graph) + THE FALSIFIER RUN LIVE (the REAL Simulator/Mediator/validator/ledger/knowledge, seed 42: Arm A the C8 freeze gap — the empty-prose kill + the monolithic regen, the valid take intent dying with a contradicted prose claim at 0 events/0 withdrawals/0 deferrals, freeze machinery 0 hits; Arm B the prose/canon boundary BOTH ways — prose-only → 0 events, the same content typed as `talk` → `talk`+`rumor_told` committed; Arm C the scope + forgetting — the player + actor docs each ⊆ their knower's records, zero cross-knower leaks, no holder ever dropped a token across 10,000 ticks; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned (the freeze arms RED→GREEN, the prose/canon controls, the per-knower scope fixtures, the explicit-forget fold flip, the INV-2 replay). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate). **Owner-ACCEPTED AS LAW 2026-10-04** (P1–P7 binding for every future implementation; the implementation rows NOT opened — «Строки имплементации пока не открываю», each row opens separately behind the gate). Detail: CONTRACTS §10 + the iter-320 report + git.
- `auth-1` — DONE (iter-321, R0/R1 definition + the live falsifier, zero code change; the queue's LAST row, opened by the owner's «Продолжай очередь с speech-1 и так далее» continuation — Q1–Q7 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §11 (review-C11/C12/C20 + M4's vocabulary/D7–D9) — seven pinned decisions (A1 the pipeline input → interpretation → classification → authorization → execution, each stage with its live carrier; A2 valid ≠ authorized — the three DISTINCT axes with distinct refusal vocabularies: malformed loud/zero events, world-impossible → the committed `intent_rejected` attempt-fact, valid+authorized → the INV-5-immutable event; A3 the INPUT-side authority classes player|NPC|director|system|pack with the S3 emit-side fence; A4 ambiguity collapses ONLY on equivalent canonical effect surfaces, the question alternative the clarify path, NO global confidence score; A5 the D7 invariant `DirectorOutput ⊆ EligibleConsequences` — the eligible set IS the seeded-hook buffer, the release paths only SELECT, the mutation probe's standing form; A6 bounded deterministic agency where a named consumer needs it — no generic planner, no LLM planner; A7 the M4 vocabulary instruction/proposal/authority/realised intervention/canonical consequence + HARD CANON — the owner's 2026-10-03 decision: no recovery/dispute path EVER for wrong-but-committed model-mediated actions, the correction form a NEW event, a retcon path REFUSED) + THE FALSIFIER RUN LIVE (the REAL Simulator/Mediator/ParserDoor/intent door/director/writer, seeds 42 + 8: Arm A the three axes — the world-impossible talk → `intent_rejected` committed ev_0006 with zero state changes, the unknown kind → the loud RunnerError at zero events, the valid move → committed, the confidence machinery 0 hits; Arm B the caller gate WITHDRAWN the guard's reply proposing the player's talk, the eligibility set enumerated (5 seeded instances) + no release-by-tag API, the invented `spawn_dragon` refused loud at the door, the writer's surface append/close only with 0 retcon hits; Arm C the question surfaced at zero events, the collapse machinery 0 hits; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned (the three-axis fixtures, the caller-gate arms, the D7 mutation probes, the collapse's equivalence proof, the writer's append-only pin, the director's pure-selection INV-2). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate). **Owner-ACCEPTED AS LAW 2026-10-04** (A1–A7 binding for every future implementation; the implementation rows NOT opened — «Строки имплементации пока не открываю», each row opens separately behind the gate). Detail: CONTRACTS §11 + the iter-321 report + git. THE QUEUE IS NOW EMPTY — all six contracts landed; the next moves the owner's calls (M2 station-side, the implementation rows' gates, the standing frontend/world rows).
- `lab-1` — DONE (iter-323, R2 local-add — the owner's Atomic World Lab agent-pack call «начни работу с архивом» (CANONSIM_ATOMIC_WORLD_LAB_AGENT_PACK_v1_5.zip, the pack's 04 §2 the Stage A order owner); the pack is a research program over the SAME substrate — this row is the harness landing, never an engine change): `scripts/labrunner.py` the Lab batch runner + `tests/test_lab.py` the nine Stage A laws — THE PLAYER-ABSENT LAW (the fixed declared anchor = the pack's own player position, ONE whole-horizon wait, the player authors nothing else; the anchor move only when the player does not already stand there — a rejected move is harness noise), the MINIMAL observation profile (identity/horizon/counts/mix/state/cost — derived read-side over `read_log`, no second log/RNG/scheduler/resolver, the record rebuildable from seed+pack+horizon), the experiment-contract record (`output/lab_<tag>.json`, gitignored runtime space, QUESTION/IDENTITY/ARMS/RUNS/DISPOSITION — assignment ≠ realized kept apart), the T1 double-run (`--verify-replay` byte-identity, the F1 falsifier), THE ABLATION ARM with the measured-not-inherited removable set (the dead-vocabulary fixpoint — the lint names the dead lines, the materializer strips them, bounded 32 passes; measured for province at 1y+: CLEAN on_action/reflection/secrets/factions, LINT-REFUSED urgencies/expectations/traits, RUNTIME-REFUSED weather (cadence-armed by the macro clock — the day-1 balance set does NOT transfer to long horizons) + crime_watch (a missing-block KeyError, the runtime-backstop gap recorded, never patched here)); THE E0 BASELINE MEASURED (province_pack, directors off): 10y × 4 smoke seeds — 7,861–7,865 events (seed variance ±2), ~100% autonomous, the mix 97.3% maintenance+account_flow (watch_change 7201/10y dominates), ZERO ecology-closing families (the pack's 01 §11 finding now a measured per-run law and the test suite's honest canary); the 100y deep run seed 7 — 78,212 events, 45.26 MB log, **546 s wall: the 10× horizon costs 83× time — the super-linear native work growth LIVE (scale-1's Q5 RED finding measured at the whole-run scale: the LOCAL beat demand pays O(|log|) folds)**; the E1 horizon gate: 1,000y at this native curve ≈ 90 min single-seed — the Lab's first scale datum, an input to Stage J's LOD work, never an optimization permission. NEXT: lab-2 the Tier A synthetic fixture (the 02 §12 smallest world — 1 settlement, sources, 10–20 adults — as a NEW content pack through the full admission lint), then the A/B battery deepening. Detail: the labrunner docstring + the iter-323 report + git.
- `ssi-1` — DONE (iter-241, D-221 — the owner's 2026-09-26 SSIEC-v3
  control-plane call): Phase 0 the architecture freeze — the eight
  public-contract surfaces confirmed at their standing owners
  (INV-1..5 + EVENT_SCHEMA + PACK_SPEC + WORKBENCH_APP_LAW) and FROZEN
  for the initiative's duration; the strangler phases move INTERNAL
  ownership only. Detail: D-221 + the overlay.
- `ssi-2` — DONE (iter-242+243, D-222/D-223): Phase 1 the SSI
  foundation — `docs/ssi/` the read-only reference copy +
  SSI_OVERLAY.md (the A–L block matrix, the executable rule subset,
  the phase ladder) + the R0–R5 risk ladder as AGENTS §2.9 + the
  executable checks (test_architecture + docguard). Detail: D-222/
  D-223 + the overlay.
- `ssi-3` — DONE (iter-244, D-224; independently re-verified iter-245):
  Phase 2 CLOSED — the 82-module map at SSI_TOPOLOGY.md (drift-pinned
  by topology --check + test_topology) + the co-change/trajectory
  audit: loop↔pack HISTORICAL (dormant since iter-168, pack already
  decomposed via packlint), inference.py CONFIRMED the active hotspot
  — ssi-5's scope shrunk on the refuted coupling, ssi-4's target
  named. Detail: D-224 + the map.
- `ssi-4` — DONE (iter-247+248+249, D-225/D-226/D-227 the PCC
  records): Phase 3 CLOSED — workbench/application/inference.py 2511
  lines → the 10 owner modules + the 176-line pure re-export facade,
  split by the LAW's §2 semantic owners (never an external template);
  zero behavior change — the public surface/ops/claim packet
  byte-stable throughout. Detail: the D-rows + the map.
- `ssi-5` — the core strangler (Phase 4, owner-gated):
  loop/director/worldgen/intent internal-ownership moves ONLY — the
  public surface (director.next_beat(...) et al.) byte-frozen (the
  ssi-1 freeze); each step its own R2/R3 iteration with a PCC
  record.
- `ssi-6` — DONE (iter-250, D-228 (R3) — the owner's «продолжай
  работу» go-ahead): Phase 5 CLOSED — workbench/canonical_read.py the
  ONE workbench core-import module (the 10-name read surface); the
  three consumers (scene_build, observatory_read, scene_ir) migrated
  at zero behavior change; the law executable twice over (the
  import ban + the watchlist pin); ssi-5 explicitly NOT opened on the
  same call (the N018 gate unmet). Detail: D-228 + WORKBENCH_APP_LAW
  §24.
- `ssi-7` — DONE (iter-251, D-229 (R3); the owner's «ssi7 и/или ssi8
  ==> можешь начать» go-ahead): Phase 6 CLOSED —
  scripts/semantic_diff.py the semantic diff layer over T1 (pure
  stdlib, zero core imports) + the 22-test claim packet + TEST_PLAN
  §1.4 the law owner; the layer ADDS, never replaces T1. Detail:
  D-229 + §1.4.
- `ssi-8` — DONE (iter-252, D-230; the same go-ahead): Phase 7 CLOSED
  — the GC pass FIRED: the N020 sweep (every artifact class clean —
  the honest negative) + the three deletion cards (the .gitkeep
  family DELETED, sim/ RETAINED on authority — consumer absence
  alone is never deletion evidence, the KI#99 doubled tree the
  owner-side cleanup card). Detail: D-230 + the overlay.
- `log-1` — DONE (iter-256, KI#100 closed — intake-40's one code
  defect, D-233; the owner's 2026-09-26 verdict-agreement call): the
  reader's stale-header gate — read_log derives the expected
  `schema_version` from the passed schema's `$id` (the writer's own
  `_extract_schema_version` path, promoted module-level so both doors
  derive through ONE function) and refuses a mismatch loudly; the
  canonical read seam + the whole read surface inherit it for free;
  the writer's append check kept as defense-in-depth; the stale-header
  pin test + the test_render header sync ride it. Detail: the intake-40
  block + KI#100 + git.
- `temp-1` — DONE (iter-260, D-236; the owner's 2026-09-26 contract pick
  over the iter-257 fork card — **A2 + B2/B3; B1 deferred**): A2 the
  crossing-family slicing contract PINNED as `tests/test_temp1_contract.py`
  (the declared tavern scope count-invariant across the arms at all four
  seeds; the minimal pair projection + fingerprint invariance; the door
  families FREE with the known divergences — the seed-125 coerce flip,
  the seed-1001 cascade — PINNED so no future change can silently "fix"
  them); B3 the semantic-origin provenance LANDED through the existing
  primitive (`provenance.assignment_tick`, schema 0.2 → 0.3, the
  cause_hook precedent; B2's runtime UNTOUCHED — the clustering witness
  unchanged, both times now observable; B1 DEFERRED behind the card's
  evidence conditions; all five fixtures regenerated, canonical fields
  byte-identical to BASE). Detail: D-236 + phases.md §6 + git.
- `cov-1` — DONE (iter-258, D-234; the owner's «цензус cov-1» call):
  `scripts/mechanics.py census` — the action-to-consequence forward
  walk (action → parser verb → realized → canonical events →
  downstream consumers), a REGENERABLE derived report (never a second
  truth); the compact view = the coverage summary + the FLAGGED rows
  (UNREALIZED — the mutation-escape surface: tavern 6 / province 19 /
  pressure 2 at landing; CONSUMERLESS — the admission lint's own law
  re-derived); 7 tests pin the coverage, the forward block, the matrix
  agreement, the pack-scoped corpus, the regenerable law. Detail:
  D-234 + TEST_PLAN §9's census cell + git.
- `div-1` — DONE (iter-259, D-235 + KI#101 closed; the owner's «и
  прочими» call): `scripts/divergence_probe.py` — one same-seed
  BASE/PERTURBED pair over the existing balance-harness arms
  (`--directors-off` the T8 instance and the default; `--pacing-off` /
  `--systems-minus` the tavern family via balance_harness's own
  materializers, imported never duplicated), the semantic_diff
  oracle's §1.4 verdict + the bounded records it does not carry
  (first-divergence, causal-path ≤8 links, persistence + the family
  deltas + the projection delta); exit 0/1/2; 8 tests pin the T8
  instance, the null control, the arms, the loud errors, the oracle
  agreement, determinism. Detail: D-235 + TEST_PLAN §9's first-prism
  row + git.
### Iteration ledger (one line per iteration; the tail capped at 10 by the doc guard — older lines live in git; per-iteration detail: the D-rows + the owning docs + worklog + git, never restated here, the header's own law)
- iter-323 · 2026-10-04 · lab1 (R2 local-add — the owner's Atomic World Lab agent-pack call, the pack's 04 §2 Stage A the order owner; the harness landing, zero core/ change): scripts/labrunner.py the Lab batch runner (player-absent law, MINIMAL profile, experiment-contract record, T1 --verify-replay, the ablation arm with the dead-vocabulary fixpoint) + tests/test_lab.py the nine laws + THE E0 BASELINE MEASURED (10y × 4 seeds: 7,861–7,865 events, ±2 variance, 100% autonomous, 97.3% maintenance-dominated, ZERO ecology-closing families; the 100y deep run: 78,212 events / 546 s — the 10× horizon costs 83× wall, scale-1's super-linear RED live at whole-run scale; the ablation set re-measured: weather cadence-armed, the day-1 balance set does not transfer); 2566+1 + ruff + docguard + topology clean; the report iter-323-lab1-report.md
- iter-322 · 2026-10-04 · acceptland (R0 doc-only — the owner's acceptance call «Принимаю P1–P7 и A1–A7 как закон. Строки имплементации пока не открываю. CONTRACTS оставляем как реестр.»): the last two pending owner calls ANSWERED — (1) P1–P7 (speech-1, CONTRACTS §10) and A1–A7 (auth-1, §11) ACCEPTED AS LAW, the §10/§11 notes landed in the §6/§7 form (binding for every future implementation; the implementation row itself the owner's separate call); (2) the CONTRACTS registry's standing-over disposition: THE SINGLE-REGISTRY FORM STANDS (iter-320 report §G's option (б) — the standing-over-cap form the permanent shape, the phases.md precedent; the per-contract split (а) refused, the deeper collapse (в) not called; the header note landed); the implementation rows stay CLOSED behind the runtime-promotion gate («пока не открываю»); KI#111's §5 cleanup executed (closed iter-318, three iterations past — mandatory, AGENTS §5); THE CONFIRMED QUEUE FULLY DISCHARGED AND ACCEPTED — all six contracts law (S/K/E/Q/P/A); the report iter-322-acceptland-report.md
- iter-321 · 2026-10-04 · auth1 (R0/R1 definition + the live falsifier, ZERO code change — the queue's LAST row, opened by the owner's «Продолжай очередь с speech-1 и так далее» continuation; Q1–Q7 accepted AS LAW the same call): the auth-1 CONTRACT LANDED at CONTRACTS.md §11 (review-C11/C12/C20 + M4's vocabulary/D7–D9) — seven pinned decisions (A1 the pipeline's five stages with live carriers / A2 valid ≠ authorized — the three axes: malformed loud, world-impossible the committed intent_rejected attempt-fact, valid+authorized the INV-5-immutable event / A3 the INPUT-side authority classes with the S3 fence / A4 ambiguity by effect-equivalence, no confidence score / A5 the D7 director invariant — the eligible set IS the seeded buffer, the mutation probe's standing form / A6 bounded deterministic agency, no planner / A7 the M4 vocabulary + HARD CANON — the owner's 2026-10-03 decision) + THE FALSIFIER RUN LIVE (the REAL Simulator/Mediator/ParserDoor/door/director/writer, seeds 42+8: Arm A the three axes live — intent_rejected ev_0006 committed with zero state changes, the unknown kind loud at zero events, the valid move committed; Arm B the caller gate WITHDRAWN the guard's reply proposing the player's talk, the eligibility set enumerated (5 seeded instances), the invented spawn_dragon refused loud, the writer append/close only with 0 retcon hits; Arm C the question surfaced at zero events, the collapse machinery 0 hits; the probe outside the repo per Rule 9, artifacts md5-pinned); THE QUEUE EMPTY — all six contracts landed; the report iter-321-auth1-report.md
- iter-320 · 2026-10-04 · speech1 (R0/R1 definition + the live falsifier, ZERO code change — the queue's head, the owner's «Продолжай очередь с speech-1 и так далее» call — Q1–Q7 accepted AS LAW the same call): the speech-1 CONTRACT LANDED at CONTRACTS.md §10 (review-C8/C9/C10/C25/C26/D10) — seven pinned decisions (P1 the channel enumeration, six channels with live carriers / P2 free prose never canon / P3 the promotion path through the normal admission, the auth-1 fence / P4 channel isolation — the freeze law for the future row, today the monolithic regen measured / P5 grounding scoped to atomic externally-testable assertions / P6 the epistemic scope law — irony read-side never write-side / P7 the explicit forgetting vocabulary + the C10 field homes) + THE FALSIFIER RUN LIVE (the REAL Simulator/Mediator/validator/ledger/knowledge, seed 42: Arm A the C8 freeze gap — the empty-prose kill, the valid take intent dying with a contradicted prose claim at 0 events/0 withdrawals/0 deferrals, freeze machinery 0 hits; Arm B the prose/canon boundary BOTH ways — prose-only 0 events, typed as talk → talk+rumor_told; Arm C the per-knower scope held across the player + actor docs, no token ever dropped across 10,000 ticks — the forgetting vocabulary ABSENT; the probe outside the repo per Rule 9, artifacts md5-pinned) + THE CONTRACTS CAP PASS (the §6..§9 falsifier RECORDS collapsed to the pointer form per D-024 — the reports own the verbatim + md5 pins; §10 lands natively in that form; the file stands over at 790 with the allowlist rationale updated); the report iter-320-speech1-report.md
- iter-319 · 2026-10-03 · scale1 (R0/R1 definition + the live measurement falsifier, ZERO engine change — the queue's head, the owner's «продолжай работу прошлой итерации, со scale-1 как я понимаю, и так далее» call — E1..E6 accepted AS LAW the same call): the scale-1 CONTRACT LANDED at CONTRACTS.md §9 (review-C5/C6/C16/C28/D5+D6) — seven pinned decisions (Q1 the three work classes by CAUSAL DEMAND / Q2 the explicit budget — exhaustion DEFERS as semantic debt, the due-work-vs-attempt split / Q3 the canonical order stands, no scheduler machinery / Q4 the cohort's build-time commutativity certificate, no CRDT/MVCC / Q5 the measurement `world size × fan-out × operation → inspected/candidate/committed + wall time` the admission instrument / Q6 locality = byte-identical canon / Q7 the four measured gap targets) + THE FALSIFIER RUN LIVE (the REAL core functions, real tavern config, synthetic scaled worlds, seed 4242: Arm A the beat's LOCAL demand pays pack-wide walks and O(|log|) folds — leverage 32,002 iterations at |log|=16k, 5.9 ms/beat; Arm B the spread pass's REGIONAL demand scans the WHOLE projection — 1,053 reads at L=320 for ONE burning location, flat in fan-out, committed S-shaped; Arm C NO work budget exists, gated attempts vanish silently, the three deferral surfaces unbounded; the probe outside the repo per Rule 9, artifacts md5-pinned) + the CONTRACTS cap pass (§5's wb family collapsed to the pointer form, 589→494; §9 lands the file at 636 — the guard's allowlist entry + the worklog the §6.1 rationale owners); the report iter-319-scale1-report.md
- iter-318 · 2026-10-03 · replay1 (R0–R1 definition + the live falsifier + ONE R2 KI fix — KI#111, found BY the falsifier; the queue's head, the owner's «продолжай очередь с replay-1 и так далее» call — S1–S7 + K1–K6 accepted AS LAW the same call): the replay-1 CONTRACT LANDED at CONTRACTS.md §8 (review-C4/C7/C13/D4) — six pinned decisions (E1 the identity tuple / E2 identity ≠ continuation / E3 the irreducible continuation set CLOSED / E4 the lifecycle proposed→accepted→durable→committed / E5 the crash contract over three boundaries / E6 flush==durable REJECTED) + THE FALSIFIER RUN LIVE (test_resume corpus seed 42: CONTROL byte-identity HELD; Arm A same-name pack drift → resume ACCEPTED, tails diverge from the first appended event — review-C4's risk live; Arm B header.commit never checked at resume; Arm C 0 fsync / torn tail LOUD / lost pre-pin tail LOUD; the probe outside the repo per Rule 9, artifacts md5-pinned) + KI#111 opened AND closed (read_log's bare JSONDecodeError on a torn line → LogError, +1 test); the implementation NOT a row (the owner opens it after accepting); the report iter-318-replay1-report.md
- iter-317 · 2026-10-03 · caus1 (R0/R1 definition + the live ablation falsifier, ZERO code change — the package's T1+T2 sequence, sem-1's natural pair, the owner's «и так далее» continuation): the caus-1 CONTRACT LANDED at CONTRACTS.md §7 (review-C2/D2) — six pinned decisions (K1 the causal spine primary_cause+necessary_supports[]+provenance no graph / K2 counterfactual necessity via the same-seed ablation — the outcome UNREACHABLE, replacements don't count / K3 the necessity-vs-evidence split / K4 the ablation battery OFF-LINE only — the divergence-probe form, never a runtime gate / K5 the producer declares, the battery verifies — the _last_change index the derivation seed / K6 compatibility + the no-DAG law) + THE ABLATION FALSIFIER RUN LIVE (seed 8, day1 theft + one inserted look step: BASE — the steal outcome ev_0007 names as cause the CHRONOLOGICAL predecessor ev_0006 (look_around) while the materially-REQUIRED move ev_0005 is indistinguishable — the necessity real, measurable, UNRECORDED (review-C2's risk live); ABLATE-MOVE — zero steal-family outcomes (necessity); ABLATE-LOOK — the steal still fires (evidence, not necessity); the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned; the implementation NOT a row (the owner opens it after accepting — the runtime-promotion gate); the report iter-317-caus1-report.md
- iter-316 · 2026-10-03 · sem1 (R0/R1 definition + the live falsifier, ZERO code change — the confirmed queue's head, the owner's «sem1 открывай и так далее» continuation call): the sem-1 CONTRACT LANDED at CONTRACTS.md §6 (review-C1/D1) — seven pinned decisions (S1 one semantic owner / S2 the declared effect surface from pack data + the mechanic constants, never per-draft / S3 the emit-side authority vocabulary with the auth-1 fence / S4 the pure non-resolving gate inside _commit / S5 the loud-soft RED lanes / S6 the anti-tautology law / S7 the _commit gap record) + the producer map + the invariant set + THE CHEAPEST FALSIFIER RUN LIVE (Arm A: a real wait producer output + a pc_01.position teleport — schema-valid, delta-consistent, APPENDED ev_0011; Arm B: a producer output re-typed year_turns with actor pc_01 — APPENDED ev_0012; the polluted log FOLDS CLEANLY — C1's risk live; the probe outside the repo per Rule 9, the artifact md5 228ea08bff9b…) + the future row's minimal test set pinned; the implementation NOT a row (the owner opens it after accepting the contract — the runtime-promotion gate); the CONTRACTS §5 cap pass riding (the landed wb landing notes collapsed to pointers per the file's own law + D-024, 576→338 lines; the stale REDOT_ENGINE_INDEX routing fixed to the D-245 form); the report iter-316-sem1-report.md
- iter-315 · 2026-10-03 · intakeland (R0 doc-only — the owner's 2026-10-03 concept-review confirmation call «м4 => жесткий канон … Сейчас — L12 как production-форма … принимаем все правки и строки предложенные!»; the REWORKED-v2 package's intake closure, the triage session's landing): the CONFIRMED CONTRACT QUEUE LANDED — six TASKS rows (sem-1/caus-1/replay-1/scale-1/speech-1/auth-1 — the review's T1–T7 adapted, T3 folded into core-1's amended POC set with the namespace fence pinned) + the package VERBATIM at docs/analysis/concept-review-2026-10/ (9 files, md5 17cfe3f8798d0a5a0ec48aedd6c68433 — the D-242 self-containment form, fourth instance) + the phases.md §6 intake record (the triage verdicts: 29 contracts classified, all six code probes verified live at HEAD) + THE OWNER'S FOUR DECISIONS in their owners: M4 = HARD CANON (no recovery/dispute path ever — auth-1's row, INV-5 the standing form); the narrator = the L12 template rung AS PRODUCTION NOW (PRESENTATION_SPEC §7 — the heavier arm re-opens only behind the closed contract rows; the owner's framing pinned: the production shape is the simulator-side prompt contract, the prose quality the MODEL's business); NO fixed playtime frame (work structured by readiness — the budget an observed per-deployment property, never a repo-side target; M3's fixed-frame question dissolved); liveness/emergence (C24/C27) stays PARKED until sem-1/auth-1/scale-1 close; the report iter-315-intakeland-report.md
- iter-314 · 2026-10-03 · q27b (R0 doc-only — the owner's second station delivery «вот результаты прогона» (`station_20261003_161523.zip`, four engines at one sitting through the v2 probe); the round-8 record, TECH_NOTES §13): THE LAST STANDING §8.5 ARM LANDED — the 27B one-model run engine1-q27b-r8 (Qwen3.8-27B-OrcaRouter-GSQ-RCO-IQ3_XXS 9.67 GiB, the tuned form: ctx 16384 · b 512/ub 256 · t 8 · --jinja · the probed draft-mtp pair · KV q8_0 · AUTO placement): raw validity 51/51 with zero re-asks (the grammar's size law at the FOURTH band); mix 31/3/17 BETWEEN e4b and q9b — the caution gradient NOT monotone in size (agreement_full 14/51 the highest measured); the MTP draft live (acceptance 0.41–1.00); no GBNF penalty at 16K (−19.6 ms); the determinism mini ×3 + restart byte-identical at the deepest ctx; the one battery_bug's ROOT CAUSE named (s8 c5 scene_mismatch — the pinned fixture's PREMISE drift, the SUBSTRATE HELD, no repo defect, no KI) + the three round-7 bands re-run BYTE-EQUAL in the same sitting (the cross-run reproducibility datum) + the narrator 27B arm (0/8 — 32 beats, 96 calls, zero accepted cumulative; PRESENTATION_SPEC §7: the floor above 27B at the IQ3_XXS quant) + the router big-switch (9B→27B 9.0 s at --models-max 1 — no size penalty against the small swap); §8.5's gap rows DISCHARGED — none stand; the probe + the runner outside the repo (Rule 9); the report iter-314-q27b-report.md
