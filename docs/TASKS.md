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
- iter-298 · 2026-10-01 · chat (R2 frontend-local — Phase 3's FOURTH ROW, the owner's «продолжай работу над фронтендом» delegated call; the row iter-297's own Next named — Chat at the rail's head): the CHAT ENTRY landed over the EXISTING run-family ops (zero new routes, zero Python change) — the contract mirror (contracts.ts: CHAT_ROLES, the EXECUTION ladder, the CANCELLATION outcomes, the run document's frozen-inputs/deadline/diagnostics envelope, the model scan/states, the §21.2 compact inference projection; validators.ts strict zod — a fabricated admission state, a foreign EXECUTION/MODEL state, a non-tuple frozen input, an unknown completion member are all MISMATCH, the inference slice loose-typed at the unconsumed depth per the data-driven law with the seam's projectInference keeping the index signature out of the surfaces; client.ts chatSend/runGet/runCancel/modelList/modelStates/inferenceRead), features/chat/{useChat,Chat} the conversation world (§8's closure REQUESTED→ACCEPTED→EFFECTIVE(the run's frozen inputs)→OBSERVED(terminal verbatim)→PRESENTED; the transcript per-surface VOLATILE — chat history is not canon, unmount drops it like every surface's local buffer; the near-bottom follow law (the reader's position wins, the scroll settles after a frame); the composer's call-local overrides explicitly surfaced (never hidden samplers), Enter/Shift+Enter, the ONE-run-at-a-time guard; the BOUNDED 700ms poll loop — dead at terminal/TRANSPORT/unmount, the re-poll the user's explicit action (G4); the messages-context rule: only admitted user turns + completed replies ride the next send, a possibly-never-sent turn stays OUT; every lane verbatim — FAILED with the observed failure_type + diagnostics, CANCELED/FAILED_TO_CANCEL as the terminal truth past a cancel, DOMAIN_REJECTED/TRANSPORT/UNKNOWN on both the send and the observation), Chat at the rail's HEAD (FRONTEND_UIUX_LAW §2.1's canonical IA tree — pinned by the Shell rows); 10 live-captured fixtures (the in-process parity form over the real composition with throwaway roots + one real dummy .gguf: the honest FAILED band — EngineError, connection refused — captured verbatim, never a fabricated completion) + 18 contract rows + 12 integration rows + the Shell rail label/mount pin; 139 vitest (=108+31) + tsc + build; the LIVE smoke 16/16 against the real app gateway (the six ops exposed, model.list/states/inference.read honest, chat.send admitted STARTING, run.get → FAILED with the §10 freeze observable, run.cancel → FAILED_TO_CANCEL verbatim, the unknown-argument/no-session rejections verbatim); the live browser closure (Chat at the rail's head, two live sends → the honest FAILED band with the verbatim diagnostics, the unmount discipline — the transcript drops with the surface, the composer focus + Enter, zero console errors, 3 screenshots); the §27 transfer records (LM Studio/Jan-class composer mechanics + the own Redot-era follow law) in the report; the COMPLETED band owner-side (a loaded llama.cpp model — declared, never faked); the report docs/iterations/iter-298-frontendweb-report.md
- iter-297 · 2026-10-01 · ia (R2 frontend-local — the IA REPAIR, the owner's «вперед реализовывай и приступай к работе, делай так как наиболее качественно и логично/обоснованно» call over the external IA verdict, D-247): the registry SPLIT landed — ProductRoute ≠ DiagnosticSurface in the composition root (the shell never sees a feature list), the vertical product rail (Trajectory LIVE / Observatory HISTORY / Settings pinned) + ONE subdued Diagnostics entry with its own secondary nav (Session lifecycle / Gateway / Load probe — the proof instruments parked, never deleted), `new session` moved from the product chrome to the Session surface, the engineering essays out of the chrome (the identity strip's honest STATE labels stay), the navigation contract amended into FRONTEND_UIUX_LAW §2.1, the acceptance floor EXECUTABLE (the Shell/App vitest rows: rail content, diagnostics isolation, one workspace, prose absence + the guard's V1 raw-color scan — which caught and closed a STANDING 9-hex-literal violation from iter-289..296 by tokenizing: --row-divider/--row-hover/--row-selected-live/--row-selected-history/--text-mono/--border-strong); the verdict processed per the D-246 method (observations verified true at HEAD; prescriptions reconciled — Settings' secondary nav excludes Inference/LLM per the inf-1 split, Trajectory stays a product route per the dual-read pair); 108 vitest (=96+12) + tsc + build + the live gateway round-trip + the live browser closure (rail = exactly 4 approved entries, zero console errors, 2 screenshots); 2529+1 pytest + ruff + docguard + topology --check clean; the report docs/iterations/iter-297-frontendweb-report.md

- iter-296 · 2026-10-01 · settings (R2 frontend-local — Phase 3's THIRD ROW, the owner's «продолжай работы по фронтенду, над теми частями что логичнее всего сейчас провести» delegated call; of the two remaining surfaces the one whose FULL honest proof band is reachable in this environment — Chat/Inference needs a loaded llama.cpp model): the SETTINGS ENTRY landed over the EXISTING backend.settings READ + backend.settings.update closed partial MUTATION (zero new routes, zero Python change) — the contract mirror (contracts.ts the LaunchSettingsDocument closed three-field set + BackendSettingsResult with applies: "next-spawn" as a literal, never a client guess; validators.ts strict zod — a fourth field, a wrong type, a foreign applies, a non-string preview are all MISMATCH; client.ts backendSettings/backendSettingsUpdate — ONLY the changed fields on the wire, a fresh client_request_id per explicit attempt), features/settings/{useSettings,Settings} the CONFIG surface (§8's closure rendered as stages, never collapsed: the draft a REQUEST — the DRAFT marker, never an effective-state claim; the Save ONE explicit dispatch; on ACCEPTED the returned document the new OBSERVED baseline and the draft reconciles to the SERVER's answer; applies: next-spawn verbatim + the LIVE note when managed_live; the compiled command preview read-only (the composition's own view); the closed set's verbatim DOMAIN_REJECTED lanes with the draft preserved; G4 no-retry — a TRANSPORT save leaves the outcome UNKNOWN, the re-read the user's reconciliation; no polling — ONE mount READ; the blue CONFIG channel distinct from the LIVE teal and the HISTORY violet), the root mounts the sixth pane; 5 live-captured fixtures (the in-process parity form over the real composition, throwaway USER_CONFIG paths) + 11 contract rows + 7 integration tests (96 vitest = 78+18) + tsc + build; the LIVE smoke 15/15 against the real app gateway (the READ defaults + the compiled preview + managed_live, the UPDATE accepted, the PERSISTED settings.json schema/2 evidence, the unknown-field/bad-type/no-arguments/session-scoped rejections verbatim, the idempotent duplicate: true replay) + the live browser closure evidence (the DRAFT marker → the closure banner → the store's file changed on disk, zero console errors); the report docs/iterations/iter-296-frontendweb-report.md
- iter-295 · 2026-09-29 · observatory (R2 frontend-local — Phase 3's SECOND ROW, the owner's repeated «продолжай работы по фронтенду, над теми частями что логичнее всего сейчас провести» delegated call; the dual-read law §4's missing half): the OBSERVATORY ENTRY landed over the EXISTING observatory.runs/observatory.read READ ops (zero new routes, zero Python change) — the contract mirror (contracts.ts the runs/window/row types incl. the CANON_VIEW/CANONICAL vocabularies + the event-schema's importance enum; validators.ts the strict zod schemas, from/to as recursive JSON values with KEY PRESENCE enforced; client.ts observatoryRuns/observatoryRead over the one POST seam), features/observatory/{useObservatory,Observatory} the HISTORY surface (the discovery scan with the per-run honest degradation pair, ONE bounded window at a time — the event-id cursor, next_after forward pagination that REPLACES the window: never an accumulating buffer; the context strip's identity line run/seed/pack/profile/authority/total; NO DATA ≠ NO MATCH ≠ stale-cursor ≠ TRANSPORT ≠ MISMATCH rendered distinct; G4 — the re-read from the head the user's explicit decision; no polling: durable evidence, every read explicit; the violet HISTORY channel distinct from the LIVE teal), the root mounts the fifth pane (the Trajectory/Observatory dual-read pair); 6 live-captured fixtures (the in-process parity form over the CLI-generated run run_125_0, 56 events) + 8 integration + 11 contract rows (78 vitest = 59+19) + tsc + build; the LIVE smoke 8/8 against the real app gateway (the listing, the head window 50/56 next_after=ev_0049, the forward window 6 events to the end, limit honored, NO MATCH verbatim, stale cursor verbatim, the closed argument set); the report docs/iterations/iter-295-frontendweb-report.md
- iter-294 · 2026-09-29 · shell (R2 frontend-local + KI#109's recorded-deletion completion — Phase 3's FIRST ROW, the owner's «продолжай работы по фронтенду, над теми частями что логичнее всего сейчас провести» delegated call): the SHELL/NAV + the SESSION LIFECYCLE surface landed over the EXISTING six gateway ops (zero new routes, zero Python change) — features/shell/Shell.tsx the navigation surface (the pane registry, ONLY the active pane mounts: boundedness; a switch drops the pane's local presentation state, the gateway stays the truth), features/session-lifecycle/{useSessionLease,SessionLifecycle} the lease lifecycle (attach under the CAS revision guard, detach under the lease guard; the honest closure REQUESTED→ACCEPTED/REJECTED→EFFECTIVE→OBSERVED — §8, never collapsed; G4 no-retry, a fresh client_request_id per explicit attempt; STALE_REVISION/LEASE_EXPIRED rendered verbatim with the gateway's own reason), the composition root mounts the four panes (Session, Gateway, Load probe, Trajectory); 5 integration tests on the live-captured fixtures (59 vitest = 54+5) + tsc + build; the LIVE smoke against the real gateway (attach OK rev 1 lease 30s → OBSERVED re-read attached=true → the stale writer REJECTED STALE_REVISION verbatim → detach OK rev 2 → the released-lease detach REJECTED LEASE_EXPIRED) — and the discovery that the remaining Phase 3 surfaces are NOT backend-blocked (the app gateway's op vocabulary already carries model.*/inference.*/chat.send/observatory.*/run.*/backend.settings); KI#109 opened and closed same-iteration (the GitHub mirror at HEAD 6c614ce carried iter-291..293's docs WITHOUT the 16 recorded D-245 deletions — a fresh clone red on docguard + the stale shell-contract; the 16 paths re-executed, the suite restored to 2529+1; the delta carries them in DELETED_PATHS); the report docs/iterations/iter-294-frontendweb-report.md
- iter-293 · 2026-09-29 · frontendweb (R2 — the post-S0 continuation, the owner's «можешь продолжать работу по фронтенду» delegated call over STATUS Next step's named order): the tooling floor's FIRST ROW landed — the frontend architecture guard (tests/architecture/guard.test.ts, 8 tests, FRONTEND_WEB_LAW §11's dependency-boundary check as the backend test_architecture's parity form, AGENTS §2.8's existing-mechanism-first: the existing vitest suite, zero new dependencies — dependency-cruiser/eslint-boundaries + the Playwright-class multi-tab smoke stay parked rows each its own admission): R1 fetch ONLY in the typed gateway client (the one transport adapter, INV-4's client-side mirror), R2 no XMLHttpRequest/EventSource/WebSocket/serviceWorker before their gateway contracts (the stream admission), R3 no browser storage as truth (localStorage/sessionStorage/BroadcastChannel/indexedDB/caches), R4 src/api imports nothing upward, R5 no cross-feature imports, R6 features couple to state only via import type, R7 the ONE composition root, R8 src never imports tests; call-form scan patterns so law-restating docstrings never false-positive; mutation-verified (a localStorage probe + a cross-feature probe both caught with file+line, green again after removal); 54 vitest green (46+8) + tsc + build; the README's Verify section + the gate list synced, the agent-context stage map's POST-S0 row updated; the report docs/iterations/iter-293-frontendweb-report.md
- iter-292 · 2026-09-29 · methoddoc (R0, doc-only — the owner's tmpfiles delivery of canonsim_design_research_and_mechanism_transfer_method_v3.md + the «изучи и определись что перенимаем и куда» delegation call): D-246 — the Refero-derived design-research & mechanism-transfer method adopted as METHOD, never authority (its own §1/§31 routing honored): the verbatim original preserved at docs/frontendweb/archive/canonsim_design_research_and_mechanism_transfer_method_v3.md (md5 8816154ab270cedad200535068b5ddd1, 1851 lines, the read-only-copy docguard allowlist entry), the durable residue distilled as §9 of docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md (the five core mechanisms — observation before interpretation, mechanism not appearance, the transfer boundary, the target envelope, claim→falsifier→evidence — + the risk-based depth ladder, the anti-averaging/anti-slop gates, VIS-0..3, the §27 compact transfer record riding the owning iteration's report), the archive README's second-artifact provenance + the track README's read-order/ownership rows + the agent-context header/stage-map METHOD ROW; REJECTED — the document's own §34 list, now CanonSim's: no parallel Refero authority/tree/registry, no global Reference Lock, no novelty quota, no mandatory research ritual, no pixel-perfect gate (the target envelope wins), no Refero runtime dependency; zero code, zero new law documents, the product owners untouched, INV-1..5 held; the report docs/iterations/iter-292-methoddoc-report.md
- iter-291 · 2026-09-29 · redotfix (R3 — KI#108: the owner-side application of the iter-290 delta landed the 65 changed/created paths but NOT the 16 DELETED_PATHS — the repo said "deleted" while the Redot tree, the engine index, the proof packets, and the Setup .bat stayed tracked; the completion of the RECORDED D-245, no new decision): the 16 paths REMOVED, the suite restored to the claimed 2529 passed + 1 skipped (the two reds gone — docguard's guard_clean_on_the_real_repo + the stale test_shell_contract zero-command pin), docguard clean again (the 1462-line engine index off the tree, its allowlist entry already removed at iter-290), the one stale live-routing FAQ half synced (engine/API questions → the archived pack's reference docs, the D-245 form); the observed law-body residue (FRONTEND_UIUX_LAW §0's layering-diagram row, WORLD_PRESENTATION_LAW §14/§15's firewall/G7 mentions) named for the owner's call, never silently rewritten from a KI fix; the report docs/iterations/iter-291-redotfix-report.md
- iter-290 · 2026-09-29 · redot-removal (R3 — the owner's «удаляй redot» call, the «вовсе отказываемся» half of the D-244 directive): D-245 — the frozen tree DELETED (workbench/presentation/redot/ the 10 files + docs/REDOT_ENGINE_INDEX.md + scripts/visual_proof.py + the three proof/contract packets + "Workbench Setup.bat" — 16 paths; recovery: git history + the verbatim pack at docs/frontendweb/archive/), the zero-command launcher RE-POINTED to the web client (npm over PATH, the first-run npm install, GATEWAY_TARGET the observed bind URL forwarded — the Vite proxy target, --no-frontend the gateway-only form, the POSIX session/group teardown; the pack's §16 gate discharged by the deletion itself — the frozen target no longer exists), tests/test_workbench_launch rewritten (10 tests), the routing sync (AGENT_NAVIGATION, README, FRONTEND_WEB_LAW, CONTRACTS §5, the law banners, frontendweb, SSI_TOPOLOGY, docguard/topology docstrings, .gitignore); 2529 passed + 1 skipped + ruff + docguard + topology --check clean + the live full-stack proof (GATEWAY_TARGET forward, the proxy round-trip app.status, SIGINT → exit 0, zero orphaned processes); ONE cumulative archive over e6789cf carrying the unapplied iter-289 (supersedes its delivery); the report docs/iterations/iter-290-redot-removal-report.md
- iter-289 · 2026-09-29 · frontendweb (R4 — the Redot freeze + the frontend-1 S0 build, the owner's «redot замораживаем, а возможно и вовсе отказываемся => делаем и работаем по canonsim_frontend_web_agent_pack_final_v1_3.zip» call): D-244 — Redot FROZEN historical/reference (the pack's §17 After-freeze law; the tree untouched in place; the archive-move/deletion stays a future owner call), the §18 S0-minimal re-homing landed (REDOT_ENGINE_INDEX frozen header, AGENT_NAVIGATION web-first routing, README; the launcher .bat re-routing deferred per the pack's §16), the top-level frontend/ tree admitted + the S0 skeleton LANDED (the pack's §13 boundary shape): React+TS+Vite, the typed POST /op client (every payload unknown→runtime-validated, the closed vocabularies mirrored, the four outcome lanes DELIVERED-OK/DELIVERED-nonOK/TRANSPORT/MISMATCH, G4 no-retry), the virtualized LIVE Trajectory (10_301 rows → 21 DOM nodes, semantic cursor, event-id selection, RESYNC_REQUIRED handled, LIVE≠HISTORY labels), two+ independent POST-only tabs (no storage as truth), the load note (300 real ops @120.9 ops/s, 12MB heap, 10ms deep-jump paint) — tsc + 46 vitest + build green, the live evidence in docs/iterations/iter-289-frontendweb-report.md; zero Python change, INV-4 untouched
