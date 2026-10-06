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
- `scale-1` — DONE (iter-319, R0/R1 definition + the live measurement falsifier, zero engine change; the queue's head, the owner's «продолжай работу прошлой итерации, со scale-1 как я понимаю, и так далее» call — E1..E6 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §9 (review-C5/C6/C16/C28/D5+D6) — seven pinned decisions Q1..Q7 (the three work classes by CAUSAL DEMAND, never implementation shape / the explicit budget: exhaustion DEFERS as semantic debt, the due-work-vs-attempt split pinned / the canonical order stands — no scheduler machinery / the cohort's build-time commutativity certificate, no CRDT/MVCC / the measurement `world size × fan-out × operation → inspected/candidate/committed + wall time` as the admission instrument / locality = byte-identical canon / the four measured gap targets) + THE FALSIFIER RUN LIVE (the REAL core functions, real tavern config, synthetic scaled worlds, seed 4242: Arm A the beat's LOCAL demand pays pack-wide walks and O(|log|) folds — leverage 32,002 iterations at |log|=16k, decay 1,248 reads at N=384 for 80 zone commits; Arm B the spread pass's REGIONAL demand scans the WHOLE projection — 1,053 reads at L=320 for ONE burning location, flat in fan-out while committed is S-shaped; Arm C NO work budget exists, gated attempts vanish silently (canon-noise), the three deferral surfaces unbounded and unaccounted; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned (the battery as a counting-proxy harness, the locality T1 control, the budget-deferral law, the cohort certificate refusal, the deferral accounting). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate) — OPENED 2026-10-04 (the iter-329 call; the standing `scale-1-impl` row). Detail: CONTRACTS §9 + the iter-319 report + git.
- `speech-1` — DONE (iter-320, R0/R1 definition + the live falsifier, zero code change; the queue's head, the owner's «Продолжай очередь с speech-1 и так далее» call — Q1–Q7 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §10 (review-C8/C9/C10/C25/C26/D10) — seven pinned decisions (P1 the channel enumeration, six channels with their live carriers — canonical fact / knowledge-belief / perception-as-acquisition-face / structured speech act / narration / diagnostic trace; P2 free prose never canon — the closed documents, the checked-never-imported assertions; P3 the promotion path — candidate structure → the intent door → the resolver circuit → `_commit`, never a second door, the auth-1 fence; P4 channel isolation — an admitted structured act FROZEN against presentation retries, today the monolithic regen, the measured gap; P5 grounding scoped to atomic externally-testable assertions — the closed claim kinds, the closed halves referenced; P6 the epistemic scope law — actor/player/narrator/debug, irony a read-side composition never a write-side fact; P7 the explicit forgetting vocabulary + the C10 field homes — trust in the relations axes, status read-side, no belief graph) + THE FALSIFIER RUN LIVE (the REAL Simulator/Mediator/validator/ledger/knowledge, seed 42: Arm A the C8 freeze gap — the empty-prose kill + the monolithic regen, the valid take intent dying with a contradicted prose claim at 0 events/0 withdrawals/0 deferrals, freeze machinery 0 hits; Arm B the prose/canon boundary BOTH ways — prose-only → 0 events, the same content typed as `talk` → `talk`+`rumor_told` committed; Arm C the scope + forgetting — the player + actor docs each ⊆ their knower's records, zero cross-knower leaks, no holder ever dropped a token across 10,000 ticks; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned (the freeze arms RED→GREEN, the prose/canon controls, the per-knower scope fixtures, the explicit-forget fold flip, the INV-2 replay). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate). **Owner-ACCEPTED AS LAW 2026-10-04** (P1–P7 binding for every future implementation; the implementation rows NOT opened — «Строки имплементации пока не открываю», each row opens separately behind the gate). Detail: CONTRACTS §10 + the iter-320 report + git.
- `auth-1` — DONE (iter-321, R0/R1 definition + the live falsifier, zero code change; the queue's LAST row, opened by the owner's «Продолжай очередь с speech-1 и так далее» continuation — Q1–Q7 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §11 (review-C11/C12/C20 + M4's vocabulary/D7–D9) — seven pinned decisions (A1 the pipeline input → interpretation → classification → authorization → execution, each stage with its live carrier; A2 valid ≠ authorized — the three DISTINCT axes with distinct refusal vocabularies: malformed loud/zero events, world-impossible → the committed `intent_rejected` attempt-fact, valid+authorized → the INV-5-immutable event; A3 the INPUT-side authority classes player|NPC|director|system|pack with the S3 emit-side fence; A4 ambiguity collapses ONLY on equivalent canonical effect surfaces, the question alternative the clarify path, NO global confidence score; A5 the D7 invariant `DirectorOutput ⊆ EligibleConsequences` — the eligible set IS the seeded-hook buffer, the release paths only SELECT, the mutation probe's standing form; A6 bounded deterministic agency where a named consumer needs it — no generic planner, no LLM planner; A7 the M4 vocabulary instruction/proposal/authority/realised intervention/canonical consequence + HARD CANON — the owner's 2026-10-03 decision: no recovery/dispute path EVER for wrong-but-committed model-mediated actions, the correction form a NEW event, a retcon path REFUSED) + THE FALSIFIER RUN LIVE (the REAL Simulator/Mediator/ParserDoor/intent door/director/writer, seeds 42 + 8: Arm A the three axes — the world-impossible talk → `intent_rejected` committed ev_0006 with zero state changes, the unknown kind → the loud RunnerError at zero events, the valid move → committed, the confidence machinery 0 hits; Arm B the caller gate WITHDRAWN the guard's reply proposing the player's talk, the eligibility set enumerated (5 seeded instances) + no release-by-tag API, the invented `spawn_dragon` refused loud at the door, the writer's surface append/close only with 0 retcon hits; Arm C the question surfaced at zero events, the collapse machinery 0 hits; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned (the three-axis fixtures, the caller-gate arms, the D7 mutation probes, the collapse's equivalence proof, the writer's append-only pin, the director's pure-selection INV-2). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate). **Owner-ACCEPTED AS LAW 2026-10-04** (A1–A7 binding for every future implementation; the implementation rows NOT opened — «Строки имплементации пока не открываю», each row opens separately behind the gate). Detail: CONTRACTS §11 + the iter-321 report + git. THE QUEUE IS NOW EMPTY — all six contracts landed; the next moves the owner's calls (M2 station-side, the implementation rows' gates, the standing frontend/world rows).
- `lab-1` — DONE (iter-323, R2 local-add — the owner's Atomic World Lab agent-pack call «начни работу с архивом» (CANONSIM_ATOMIC_WORLD_LAB_AGENT_PACK_v1_5.zip, the pack's 04 §2 the Stage A order owner); the pack is a research program over the SAME substrate — this row is the harness landing, never an engine change): `scripts/labrunner.py` the Lab batch runner + `tests/test_lab.py` the nine Stage A laws — THE PLAYER-ABSENT LAW (the fixed declared anchor = the pack's own player position, ONE whole-horizon wait, the player authors nothing else; the anchor move only when the player does not already stand there — a rejected move is harness noise), the MINIMAL observation profile (identity/horizon/counts/mix/state/cost — derived read-side over `read_log`, no second log/RNG/scheduler/resolver, the record rebuildable from seed+pack+horizon), the experiment-contract record (`output/lab_<tag>.json`, gitignored runtime space, QUESTION/IDENTITY/ARMS/RUNS/DISPOSITION — assignment ≠ realized kept apart), the T1 double-run (`--verify-replay` byte-identity, the F1 falsifier), THE ABLATION ARM with the measured-not-inherited removable set (the dead-vocabulary fixpoint — the lint names the dead lines, the materializer strips them, bounded 32 passes; measured for province at 1y+: CLEAN on_action/reflection/secrets/factions, LINT-REFUSED urgencies/expectations/traits, RUNTIME-REFUSED weather (cadence-armed by the macro clock — the day-1 balance set does NOT transfer to long horizons) + crime_watch (a missing-block KeyError, the runtime-backstop gap recorded, never patched here)); THE E0 BASELINE MEASURED (province_pack, directors off): 10y × 4 smoke seeds — 7,861–7,865 events (seed variance ±2), ~100% autonomous, the mix 97.3% maintenance+account_flow (watch_change 7201/10y dominates), ZERO ecology-closing families (the pack's 01 §11 finding now a measured per-run law and the test suite's honest canary); the 100y deep run seed 7 — 78,212 events, 45.26 MB log, **546 s wall: the 10× horizon costs 83× time — the super-linear native work growth LIVE (scale-1's Q5 RED finding measured at the whole-run scale: the LOCAL beat demand pays O(|log|) folds)**; the E1 horizon gate: 1,000y at this native curve ≈ 90 min single-seed — the Lab's first scale datum, an input to Stage J's LOD work, never an optimization permission. NEXT: lab-2 the Tier A synthetic fixture (the 02 §12 smallest world — 1 settlement, sources, 10–20 adults — as a NEW content pack through the full admission lint), then the A/B battery deepening. Detail: the labrunner docstring + the iter-323 report + git.
- `lab-2` — DONE (iter-324, R2 local-add — the owner's «продолжай lab2 и так далее» call, the pack's 04 §3 Stage B the first entry; the fixture IS the deliverable, zero core/sim/render change): `content/farstead_pack/` THE TIER A SYNTHETIC FIXTURE (the 02 §12 smallest world — 1 settlement (the green carries storage + exchange), 4 finite sources + regrowth flows, 1 workshop + the finite rack, 1 road, 12 adults in 3 households, 4 roles) through the FULL admission lint (the sixth pack; the direct-settle hauls source→store in ONE event, the keeper's float-based meal, the on_action fatigue reply) + `tests/test_farstead_pack.py` the nine Tier A laws (the lint, the shape, the player-absent+T1, THE LOOP CLOSES — every L1 edge live, CONSERVATION exact per kind, THE ANCHOR PAIR — the LOD datum, the removable set re-measured, the deferred-realize law) + the labrunner's honest account-verb disposition line; THE E0 MEASURED: the anchor pair 10y × 4 seeds — square 933–971 events with the material cycle SEED-INVARIANT (132 account events, every seed — the year clock's determinism) vs road 165–187 events (the frozen diorama: the sources regrow untended, the store untouched, the boy's talk the world's one active voice); the 100y deep run square seed 7 — 8,663 events / 51.2 s: **THE DEFERRED-REALIZE LAW AT WHOLE-HORIZON SCALE: 94% of the century's autonomous life discharges in the final ~10 ticks (temp-1/D-236 measured — the mid-wait log is the scheduled machinery alone, 5 events/year); the herd tail ~5,400 door-rejects = p × beats × years (the protocol's noise law)**; the per-block findings: the one-goal-per-verb + one-target laws force THE HAUNT MODEL (no commuter form — the direct settle is the honest round), the chained round CANNOT roll (the second verb's gate reads pre-first state — the float law), the rack empties at year ~6 (no conversion primitive — the Stage B gate's own input), the tools pile unconsumed, regrowth uncapped; the removable set for farstead: urgencies + on_action BOTH CLEAN (province's verdicts do not transfer — the re-measured law); the stoplist's sixth list + the economy test's fourth armed consumer. 2576+1 + ruff + docguard + topology clean (INV-1..5 untouched, the LOG untouched, zero corpus price; NO test deleted or weakened — 10 added). NEXT: lab-3 the A/B deepening (paired seeds, the segmented-wait protocol row the owner's call — the deferred-realize finding's answer) + the Stage B contract rows (transformation/wear/bounded sources) behind their gates. Detail: the pack's own notes + the iter-324 report + git.
- `lab-3` — DONE (iter-325, R2 local-add + ONE R2 KI fix (KI#112, found BY the batteries themselves) — the owner's «продолжай lab3 и/или можешь прогнать полную батарею 100y×4 сида (~4 мин) для репортажа» call, the row the iter-324 NEXT named; the pack's 04 §8 experiment-contract form (QUESTION/ARMS/REALIZED_DELTA/DISPOSITION) made executable; zero core/sim/render change): THE PROTOCOL ARM in `scripts/labrunner.py` (`--protocol whole|segmented|paired` + `--segment-ticks`; the new law 7: the player authors NOTHING but null waits — segmentation changes WHEN the world moves, never WHAT the player is; `whole` stays the DEFAULT, byte-compatible with every prior record) + the lab-3 metric block in the MINIMAL profile (the MID-HORIZON LIFE profile — autonomous non-machinery events per year-span, the deferred-realize discriminant; the FINAL MATERIAL STATE — per-holder account levels read from the fold, the 03 §8 REALIZED_DELTA surface; `player_waits`) + the paired record (per-seed whole-vs-segmented deltas: events, life spans, account verbs, the final material state, wall) + `tests/test_lab.py` the four lab-3 laws (the step-list law — whole ONE wait / segmented N waits summing EXACTLY to the span with the remainder tail, the years=1 boundary coincidence; the segmented player-absent + T1 byte-identity; THE MID-HORIZON LIFE DISCRIMINANT — whole `[0, 0, total]` 100% final vs segmented every year live; the paired record's REALIZED_DELTA executable + the verdict live) + KI#112's log-identity fix (the run tuple (seed, anchor, horizon, arm, protocol) joins the log filename — two prefix collisions found by the batteries: the road run overwrote the square logs, then the 10y overwrote the 100y); THE BATTERY MEASURED (farstead, directors off): the 100y paired × 4 seeds — whole 8,564–8,749 events, life 100% at the horizon's final boundary (the deferred-realize law at century scale) vs segmented 12,212–14,038 (+42–61%) with life in 100/101 spans (1% final); **THE REALIZED DELTAS LIVE ON EVERY SEED** — the verb deltas SEED-INVARIANT (consumed +394, settled +395, every seed — the year clock's determinism), the material delta IS the two different worlds: whole leaves ~200 of each kind ON THE STORE (the century realized as ONE deferred batch: meals 28, meal_eased 3, decay 49) vs segmented the store near-EMPTY with ~200 ore+wood on the RACK (the steady flow: meals 422, meal_eased 267, decay 5,417 — the fatigue cycle arms with the meal cycle); **THE CONTROL FAMILY: talk 3,209 = 3,209** (protocol-invariant — the beat rolls never move; the divergence enters exactly where the gates read MUTABLE state) + the road diorama pair (life totals 1,072 = 1,072 invariant — the diorama's one voice defers under whole, spreads under segmented, the material stays frozen: the LOD gate WHO-rolls orthogonal to the protocol WHEN-realizes); **THE COST DATUM: segmented 20–22 s vs whole 51–53 s per century-seed (2.5× FASTER — the whole protocol's "cheap" century was an illusion of deferral: the final drain pays the ~8,000-intent herd against the fat end-state)**; the granularity datum: day-waits at 2y — 720 player waits = 42% of the log (the daily form's noise law). NEXT: the E1 horizon row (the segmented 1,000y probe — the measured curve (0.26s/2y → 20.4s/100y, ~t^1.3) says minutes, the whole 1,000y stays the lab-1 ~90-min gate), the Stage B contract rows (transformation/wear/bounded sources) behind their gates, the scale-1 follow-up (the wall-cost decomposition: WHY the deferred herd pays 2.5× — a named gap, never guessed). Detail: the labrunner docstring + the iter-325 report + git.
- `lab-4` — DONE (iter-326, R2 local-add — the owner's «продолжай» continuation call, the E1 horizon row the iter-325 NEXT named; zero core/sim/render change): the lab-4 REPLAY-COST instrument in `scripts/labrunner.py` (the pack's 04 §12 horizon battery made executable: `read_seconds`/`fold_seconds`/`replay_alloc_peak_mb` — the read-side cost split a resume/replay pays, the tracemalloc peak honestly labeled as interpreter allocations, NEVER the OS RSS, portable to the owner's Windows station) + the two lab-4 laws in `tests/test_lab.py` (the instrument law — every record carries the block on both protocols, a non-empty log pays real read+fold time; the KILOYEAR ARITHMETIC law — the step-list is a pure function of (years, segment_ticks): 1,000y segmented = EXACTLY 1,000 cadence waits, custom segments sum EXACTLY to the span, whole stays ONE wait at any horizon — zero corpus price) + THE E1 SEGMENTED LADDER MEASURED (farstead, seed 7, square, year-segmented, 2y→650y in eight rungs; 650y = 81,823 events / 465.22 s — the deepest rung the sandbox's 600-s window holds, the window itself measured honestly: background processes do not survive the tool-call boundary) + THE STATION HORIZON PROBE v1 (outside the repo per Rule 9, the session's offload rule — the kiloyear paired battery rides the owner's hardware: preflight → sanity (2y paired + T1 on the station) → control (100y paired, the cross-hardware wall) → MAIN (1,000y paired, whole + segmented + the kiloyear REALIZED_DELTA) → package (records + raw logs md5-pinned, one zip); every stage a checkpoint in try/except, a fallen stage never stops the rest, a stage timeout is itself a datum; self-checked end-to-end in-sandbox) + THE MEASURED E1 FINDINGS: the wall curve STEEPENS monotonically (local exponents 1.00→1.05→1.20→1.34→1.59→1.68→1.81 — the t^1.3 forecast from iter-325 REFUTED at depth: 1,000y ≈ 930–1100 s on the sandbox CPU, 16–18 min, not "minutes"; events stay linear 122–132/year — the super-linearity is the per-EVENT cost growth, never the count), THE FLAT-LIFE LAW (life ~71–72/year from 10y to 650y, 650/651 spans live — a 325× horizon range with zero life trend: the year-segmented world is a stable annual cycle, no collapse, no explosion; the deferred-realize law's kiloyear answer), THE LINEAR VERB LAWS (sourced 4.00/year EXACT, consumed 4.03, settled 8.03 — iter-325's seed-invariance now measured across SCALE to 6.5 centuries), THE CONSTANT-STATE LAW (projection_entities = 25 at 100/500/650y — the state never grows with the horizon, only the LOG does; the accounts pile linearly ~26.3 units/year: water 1,060→6,560, the Stage B bounded-source falsifier measured at 6.5-century scale; the super-linear wall at CONSTANT state = the scale-1 decomposition's named gap, never guessed here), THE REPLAY-COST DATUM (read-bound: 0.62 s/MB flat, the fold near-free 0.055 s at 81,823 events, the alloc peak 3.34× the log, all linear — a resume pays O(log bytes), the state never participates in the price). 2582+1 + ruff + docguard + topology clean (INV-1..5 untouched, the LOG untouched, zero corpus price; NO test deleted or weakened — 2 added). NEXT: the owner runs the station probe v1 (the kiloyear pair + the cross-hardware wall), then the Stage B contract rows (transformation/wear/bounded sources — the falsifiers measured), the scale-1 wall decomposition. Detail: the labrunner docstring + the iter-326 report + git.
- `stageb-1` — DONE (iter-327, R0 definition, ZERO code change — the owner's «продолжай работу» call after the station zip's in-session analysis; the row the iter-326 NEXT named first after the station run): THE STATION KILOYEAR DATUM ANALYZED (the owner's `horizon_station_20261004_112903` zip, v2.1 probe, Python 3.14.3/30.9 GB/HEAD febab32: preflight + sanity 2y + control 100y + MAIN 1,000y paired ALL ok; T1 byte-identity HELD on the station; the control 100y pair byte-for-byte the sandbox's own numbers (8,663/13,234) — the cross-hardware determinism law; station ≈ 1.20–1.24× faster): THE KILOYEAR PAIR — whole 86,265 events / 3,306.63 s / life 81,214 in ONE final tick vs segmented 126,392 / 884.39 s / 71,798 life in 1000/1000 spans (the flat-life law at the kiloyear: 71.8/year); THE CONTROL FAMILY talk 32,165 = 32,165 EXACT; THE VERB LAWS sourced 4,000 = 4.00/year in both arms; THE KILOYEAR REALIZED_DELTA — the Stage B falsifier in its final form: segmented leaves loc_workshop ore 2,004 + wood 2,012 = 4,016 units DEAD at tool = 0 (the conveyor delivered, nothing transforms), whole leaves ~200/kind on the store with the workshop untouched; tools 8 at the square UNCONSUMED a millennium in BOTH arms (no wear); the spring 10,060 = 60 + 10/year EXACT linear (no cap); THE WALL DATUM — the iter-326 forecast HELD (sandbox-equivalent ≈ 1,061 s vs the predicted 930–1,100), and the in-session cProfile decomposition (10y vs 100y, farthest seed 7) NAMES the super-linearity's mechanism: TWO quadratic read-side members — `occ_breaking_cause`'s full-log refold per OCC rejection (per-call ×9.51) + `knowledge._novel_facts`' whole-knowledge re-ranking per talk (per-call ×9.17); the A·t + B·t² model reproduces the α-ladder (1.01→1.83 model vs 1.00→1.81 measured) and explains 77.5% of the kiloyear wall — the scale-1 decomposition's answer, measured not guessed + THE CONTRACT LANDED at CONTRACTS.md §12 — eight pinned decisions (B1 one substrate — the account primitive, never a second mechanism / B2 the conversion verb: ONE atomic recipe event, the settle precedent, conservation PER RECIPE, the float law respected by construction / B3 the wear law: per-USE integer consume on the named instrument, never wall-clock, break-at-zero the door's soft arm / B4 the bounded source: the mint's min() cap, silence at full — the every-miss form / B5 the unarmed law — zero events without pack declarations, the golden fixtures byte-identical / B6 the REALIZED_DELTA oracle — acceptance MATERIALIZED: the dead pile dies, the linear piling breaks at the cap, the instrument turnover bounded / B7 the cost law — every new read surface index-based (the _last_change pattern), never a log scan: the measured wall law makes any O(|log|)-per-event surface RED at the row's own gate / B8 the pack-data boundary + the promotion gate — additive enum values, no schema break) + the falsifier pointer block (the three gaps' measured records: iter-324 + iter-326 + the iter-327 report §B, md5-pinned) + the future row's minimal test set pinned. The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate) — ACCEPTED + OPENED 2026-10-04 (the iter-329 call, B1..B8 as law; the standing `stageb-1-impl` row). Detail: CONTRACTS §12 + the iter-327 report + git.
- `lab-5` — DONE (iter-328, R2 local-add — the owner's «инструментальную строку scale-1 в labrunner» call (the row the iter-327 NEXT named first), the same message's C-13 decision recorded below; zero core/sim/render change): THE WALL-DECOMPOSITION INSTRUMENT in `scripts/labrunner.py` (`--profile-depths 10,100` — the first seed once per depth under cProfile; the record gains the `profile` block: the member split by entry CUMTIME over a documented map — occ_refold (the OCC prefix refold) / knowledge_rerank (_novel_facts) / beat_rolls / decay_walk / the derived folds BY CALLER (the clock's greedy `_run_beat`+`_run_macro` path vs the intent door's lazy `_fold_reads`) — plus the ULTIMATE pack's counters made executable: E03 rule-parses/beat (the `_specs` re-parse), E04 derived-read calls/beat vs the STATIC gated-entry demand (the pack's own parsers, never a second truth), beats/event; the growth block = the per-call ratios between the shallowest and deepest rung; canon_check = the instrument's own falsifier — the profiled bytes vs the unprofiled battery's at every coinciding depth, RED on breach) + `tests/test_lab.py` the three laws (the CANON-NEUTRALITY law — profiling observes, never mutates; the ACCOUNTING law — members + rest == the profiled total, the disjointness flag, E03 >= 1/beat, every fold function computed on the clock path at least once per beat with this fixture's gated demand ZERO (P0.5-A's RED baseline — flips deliberately when beat laziness lands), beats/event measured; the GROWTH + honest-label law — the two-depth per-call ratios, `profiled_wall_seconds` never the battery's `cost.wall_seconds`, the artifact note); THE DATUM MEASURED (farstead seed 7, segmented, 10y+100y): the iter-327 in-session decomposition REPRODUCED as a committed record — occ_refold 27.3% + knowledge_rerank 10.8% of the 100y profiled wall (the two quadratic read-side members named), the growth ratios fold x9.67 / _novel_facts x9.54 / _ranked x10.4 (iter-327's x9.51/x9.17/x10.02, within noise), CANON-NEUTRALITY HELD at 100y (the profiled 7.7 MB byte-identical to the battery's), E03 2.0 parses/beat + E04 5.01 greedy calls/beat vs 0 gated entries (the Q7a waste quantified on the pack with no secrets/echo/traits — the folds early-return, the CALLS still fire every beat), beats/event 8.16 at 100y (the pack's stale "~50" replaced by the measured per-run number). Detail: the labrunner docstring law 8 + the iter-328 report + git.
- `rng-1` — DONE (iter-334, R3 core — the owner's «==> P0.5-C, rng-1 (эпоха), станционный килогод» call, the row's own opening; the counter-block epoch LANDED in `core/rng.py`: `U(stream,k) = word(k mod 4) of sha256(key:k div 4)` — O(1) access to the k-th draw (the end-state time-skip horizon H9 structurally unlocked), a checkpoint of COUNTERS ONLY (`core/cursor.py` refuses pre-epoch MT cursors loud), branch isolation STRUCTURAL (a draw's value fixed by (seed, stream, k) — a re-armed neighbor cannot move it even in principle); the block form: one sha256 per 4 draws (~0.42 µs/draw = MT randint's own CPython price — free on the real call mix), the wall price measured +3.7% (farstead 100y 10.0→10.37 s); **THE CORPUS PRICE PAID AND RECORDED**: 228 failures at the flip, all re-pinned with the laws' assertions intact (seed re-pins, beat-grid t-stamps, the document-check verdict flip on seed 125, the golden corpus regenerated ×7, 3 playscripts re-seeded, the CRN test's power doubled 8→16 pairs at the SAME thresholds — never weakened; one mechanical corruption caught and fixed: test_echo's `pack`→`PACK` from an earlier re-pin); P0.5-C closed as exhausted (the hoist rode P0.5-A, the LOD filter reclassified P1, the ~22% occ_refold residual measured near-linear); the owner's balance condition verified on the B6 oracle under the epoch's draws — 10 conversions = 10 bloom wears at 10y, every source at-or-below its cap, **NO pack-data fork needed**: the cycle balances on its own mechanics. NEXT: the station kiloyear with the armed world (the call's third item, now unblocked — the epoch boundary paid), H9 behind it. Detail: the iter-334 report + git.
- `scale-1-impl` — DONE (iter-330 + iter-331, the byte-identical wall row COMPLETE; the owner's «можешь начинать (stageb-1 и scale-1)» call): **P0.5-A** the beat/macro derived folds on the pack's DECLARED gated-entry demand (`_fold_demand` at init + `_clock_fold_reads`, one shared computation per tick) + **P0.5-B** the specs parse-once memo (`urgency_specs`/`faction_specs` + `specs=`, every existing caller untouched) — the E03/E04 RED baselines flipped as iter-328 designed (2.0→0.0 parses/beat, 5.01→0.0 calls/beat vs 0 gated) + **P1a** the OCC attribution snapshot (the enqueue-time projection copy in a FIFO side-table — the ids repeat across beats, the queue's seq order restores the exact pairing — popped at the accept door, carried on the CompletionPayload, the walk pays the WINDOW never the prefix; the attributable-empty early return exact; the fold stays the resume/external fallback) + **P1b** the knowledge rank-bucket iteration (per knower per rank, tie-runs newest-first, arrival order within a run — EXACTLY the stable sort, zero comparisons, `at` monotone by the writer's tick-regression law) + the (teller,listener) novelty count (the O(1) saturated answer, born-correct for late knowers). **THE WALL FIXED, BYTE-IDENTICAL**: farstead 100y segmented 20–22 s → 10.0 s (2.1×); occ_refold 27.3%→3.1% + knowledge_rerank 10.8%→0.0% of the profiled wall; `fold` ZERO calls in-window at both depths; the per-call growth ratios ×9.5–10.4 → ×1.0–1.1 (the super-linearity dead at constant state); the local exponents the station ladder measured now flat. BYTE-IDENTITY: the cross-version md5 pair (farstead 2y/10y segmented seed 7 + province 2y whole seed 42 — zero-demand AND armed-demand sides) equal at EVERY stage (post-P0.5, post-P1, post-FIFO); the snapshot-vs-fold equivalence law (254+ real projection_moved walks byte-equal with start_state stripped); the golden T1 corpora + resume tests green. P0.5-C surfaced honestly (the candidates in the iter-330 report §E — the hoist rode P0.5-A; the owner's call on the rest). Detail: the iter-330 + iter-331 reports + git.
- `stageb-1-impl` — DONE (iter-332 + iter-333, the material cycle COMPLETE; CONTRACTS §12 B1..B8 the owner-accepted law): **iter-332 the ENGINE mechanics** (B2 the convert verb — ONE atomic recipe event, the settle aggregation; B3 the use-hook wear — a per-use consume at the successful completion, the instrument named, break-at-zero the last use; B4 the capacity cap — the min() mint, silence at full, the _commit cap floor loud; the lint arms; the renderer slots; the unarmed law held) + **iter-333 the FARSTEAD ARMING + THE B6 BATTERY**: the recipe forge_a_tool (the workshop's ore 2 + wood 2 → tool 1), the wear on the bloom bench (tool 1 per use, the lint-required gate), the caps on all four sources (the seeded basins: bank 40 / copse 40 / outcrop 24 / spring 60 — the first cut below the seeds was caught BY the cap floor itself, the pack bug refused loud, exactly the floor's law); **THE B6 REALIZED_DELTA ORACLE GREEN at 10y+100y**: (a) THE DEAD PILE DIES — the workshop's terminal ore+wood the recipe's WORKING stock (static: ore 4 = the seed, wood 12 the conveyor's buffer; the unarmed trajectory grew past 24 ore by 10y heading to 2,004 at the kiloyear); (b) THE LINEAR PILING BREAKS — every source at-or-below its basin (the spring ≤ 60 vs the unarmed 60+10/year → 10,060 at the kiloyear; the TOTAL account mass CONSTANT, the unarmed +26.3/year dead); (c) THE INSTRUMENT TURNOVER LIVE AND BALANCED — 100 conversions = 100 bloom wears over the century (1/year each way), the tool stock static at the seed 6, produced → worn → reproduced forever. The verb mix shifted measurably (account_converted 100/100y; the smith's settles became conversions — the loop-closes law extended to the verb family); **the B7 cost law held** (the armed wall 10.07 s vs 10.0 s unarmed — the cycle costs ~0.7%; occ_refold 3.1% + knowledge 0.0% unchanged; the growth ratios ×1.17–1.5, not steeper; canon-neutrality HELD); the conservation law extended per B2's own letter (initial + minted + transformed_in == final + consumed + transformed_out, per kind — the contract named the test as the extension point). +3 farstead laws (the arming's shape, the B6 oracle, the per-recipe conservation) + the loop-closes/cost re-pins. Detail: the iter-332 + iter-333 reports + git.
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
- iter-334 · 2026-10-05 · rng1 (R3 core — the owner's «P0.5-C, rng-1 (эпоха), станционный килогод» call, the row opened by the message itself): THE EPOCH LANDED — the counter-block RNG bank (U(stream,k) = word(k mod 4) of sha256(key:k div 4); O(1) to the k-th draw, counters-only checkpoint, structural branch isolation; the legacy MT cursor refused loud) + THE CORPUS PRICE PAID: 228 failures re-pinned with every law's assertion intact (7 golden fixtures regenerated, 3 playscripts re-seeded, the document-check verdict flip, the CRN power doubled at the same thresholds; test_echo's mechanical pack→PACK corruption caught and fixed) + P0.5-C closed as exhausted + the owner's balance condition verified: the B6 oracle GREEN under the epoch's own draws (10 conversions = 10 wears, all caps held — zero pack-data forks); measured: 766,832 draws/100y (98.7% urgency family), the block form free per-draw (0.42 µs = MT randint's own), the wall +3.7% (10.0→10.37 s); 2606+1 + ruff + docguard + topology clean (NO test deleted or weakened); NEXT: the station kiloyear with the armed world (unblocked — the boundary paid), H9 behind it; the report iter-334-rng1-report.md
- iter-333 · 2026-10-04 · stageb1impl2 (R2 pack-data — the farstead arming + the B6 battery, the material cycle COMPLETE): the recipe forge_a_tool (ore 2 + wood 2 → tool 1 at the workshop), the bloom-bench wear (tool 1 per use), the four source caps (the seeded basins — the first cut BELOW the seeds caught by the cap floor itself: the loud refusal the law's own proof); THE B6 ORACLE GREEN: the dead pile dies (the workshop static: ore 4 the seed, wood 12 the buffer), the piling breaks (the total account mass CONSTANT vs the unarmed +26.3/year; the spring ≤ 60 vs 10,060 at the kiloyear), the turnover balanced (100 conversions = 100 wears/century, the tools static at the seed); B7 held (the armed wall +0.7%, the growth ratios ×1.17–1.5); the conservation law extended per B2's letter (transformed_in/out legs); +3 farstead laws, the loop-closes law re-pinned to the verb family; the tuning honest (v1→v4 by the battery: the wear balanced to the production, the recipe's inputs to the delivery cadence); 2606+1 + ruff + docguard + topology clean; the report iter-333-stageb1impl2-report.md
- iter-332 · 2026-10-04 · stageb1impl1 (R3, the PCC in the report §G — the stageb-1-impl row's engine half, the material cycle's three mechanics): B2 the convert verb (ONE atomic recipe event — the settle aggregation, per-recipe conservation fold-checkable, the float law by construction), B3 the use-hook wear (a per-use consume at the successful completion, the instrument named, break-at-zero the last use, the lint-required solvency gate at the door), B4 the capacity cap (min() mint, silence at full, the _commit cap floor loud any-verb) + the lint arms (recipes/capacity/convert/instrument, 8 refusal laws) + the renderer's input_/output_ slots; B5 unarmed held (farstead 2y md5 equal), B7 index law by construction (projection reads only), B8 additive vocabulary (account_converted — no schema change); +11 laws (tests/test_stageb_impl.py); 2603+1 + ruff + docguard + topology clean; 7 changed/created (6 + report; DECISIONS at cap 30 — the PCC rides the report, the iter-322 precedent); the report iter-332-stageb1impl1-report.md
- iter-331 · 2026-10-04 · scale1impl2 (R2 local behavior — the scale-1-impl row's second half, P1a + P1b, byte-identical; the WALL FIXED): P1a the OCC attribution snapshot (the enqueue-time projection copy, a FIFO side-table over the repeating intent ids — the queue's seq order restores the exact pairing, found live by the instrument: the first battery showed fold still 2,495-call because the id collisions starved the pops; the accept-door popleft + the first-step door + the attributable-empty early return complete it) + P1b the knowledge rank-buckets (tie-runs, the writer's tick-monotonicity the ground) + the novelty count (born-correct for late knowers, the O(1) saturated answer); THE MEASURED FIX: farstead 100y 20–22 s → 10.0 s, occ_refold 27.3→3.1%, knowledge 10.8→0.0%, fold ZERO in-window calls, growth ratios ×9.5–10.4 → ×1.0–1.1, canon-neutrality HELD, 13,234 events byte-for-byte; +3 laws (the bucket-vs-sort oracle over interleaved adds, the novelty-count-vs-walk property, the snapshot-vs-fold byte equivalence over 254 real walks); the byte-identity md5 pair re-verified at every stage; 8 changed/created (core/intent.py, core/knowledge.py, core/loop.py, tests/test_scale1impl.py, + 4 riders); 2592+1 + ruff + docguard + topology clean; the report iter-331-scale1impl2-report.md
- iter-330 · 2026-10-04 · scale1impl1 (R2 local behavior — the scale-1-impl row's first half, P0.5-A + P0.5-B, byte-identical by Q6's law): the beat/macro derived folds ride the pack's DECLARED gated-entry demand (`_fold_demand` at init from both families' requires + `_clock_fold_reads`, one shared computation per tick — the old greedy form paid all three folds every beat, two of them twice) + the spec families parse ONCE (`urgency_specs`/`faction_specs` + `specs=` on both walks, the loop's init memo — E03's 2.0 parses/beat closed); the instrument's RED baselines FLIPPED as designed: E03 2.0→0.0/beat, E04 5.01→0.0 calls/beat vs 0 gated, clock_derived_folds 0.7→0.0%, the accounting-law test flipped, the 100y wall 20–22→17.8 s; byte-identity: the cross-version md5 pair (farstead 2y/10y segmented + province 2y whole — the zero-demand AND armed-demand sides) equal, the golden T1 corpora green; +4 laws (tests/test_scale1impl.py: the demand axis, the zero-demand no-call law, the armed once-per-tick hoist law, the parse-once memo law); the two quadratic members STAND (occ_refold 29.1% + knowledge 11.2%, ×9.69/×8.99 — P1a/P1b next); one INV-3 comment fix caught BY the stoplist test (a pack name in an engine comment — the executable working); 9 changed/created (5 code/test + 4 riders: core/loop.py, core/urgencies.py, core/factions.py, tests/test_lab.py, tests/test_scale1impl.py); 2589+1 + ruff + docguard + topology clean; the report iter-330-scale1impl1-report.md
- iter-329 · 2026-10-04 · acceptland12 (R0 doc-only — the owner's «§12 (B1..B8) = принимаю, можешь начинать (stageb-1 и scale-1) и прочее» call): (1) B1–B8 (stageb-1, CONTRACTS §12) ACCEPTED AS LAW — the §12 acceptance note in the §10/§11 form (binding for every future implementation); (2) the first TWO implementation rows OPENED behind the runtime-promotion gate — the standing `scale-1-impl` + `stageb-1-impl` rows (the rng-1 order: the byte-identical scale-1 rows first, then the material cycle's edges); KI#113 OPENED (the wall-split accounting law's one-time AssertionError under post-install load, unreproduced in 6 retries — the timing-sensitive candidates named, honest open); zero code change, DECISIONS untouched (the acceptances ride their owners, the iter-322 precedent); 5 changed/created (4 modified + 1 created); 2585+1 + ruff + docguard + topology clean (INV-1..5 untouched, the LOG untouched, zero corpus price; NO test deleted or weakened); the report iter-329-acceptland12-report.md
- iter-328 · 2026-10-04 · lab5 (R2 local-add — the owner's «инструментальную строку scale-1 в labrunner» call, the scale-1 instrumentation row the iter-327 NEXT named + the same message's C-13 RNG-epoch decision): the WALL-DECOMPOSITION INSTRUMENT in the labrunner (--profile-depths: the member split by entry cumtime — occ_refold / knowledge_rerank / beat_rolls / decay_walk / the derived folds BY CALLER (clock-greedy vs door-lazy) — + the pack's counters E03 parses/beat, E04 derived reads/beat vs the static gated-entry demand, beats/event; canon_check = the profiled-vs-unprofiled byte identity, the instrument's own falsifier) + tests/test_lab.py the three laws (canon-neutrality, the accounting + P0.5-A RED baseline, growth + honest labels); THE DATUM (farstead 7, segmented, 10y+100y): iter-327's decomposition REPRODUCED — occ_refold 27.3% + knowledge_rerank 10.8% of the 100y profiled wall, fold x9.67 / _novel_facts x9.54 / _ranked x10.4 per-call growth (iter-327: x9.51/x9.17/x10.02), canon-neutrality HELD at 100y, E03 2.0/beat, E04 5.01/beat vs 0 gated, beats/event 8.16 (the pack's "~50" replaced); the rng-1 standing row landed (the owner's C-13 call — the epoch approved in principle, the byte-identical rows first); 6 changed/created (5 modified + 1 created); 2585+1 + ruff + docguard + topology clean; the report iter-328-lab5-report.md
- iter-327 · 2026-10-04 · stageb1 (R0 definition, ZERO code change — the owner's «продолжай работу» call after the station zip's in-session analysis): THE STATION KILOYEAR DATUM ANALYZED (horizon_station_20261004_112903: all five stages ok, T1 HELD on the station, the control 100y byte-for-byte the sandbox's numbers, station ≈ 1.20–1.24× faster; the kiloyear pair whole 86,265/3,306.63 s/life 100% final vs segmented 126,392/884.39 s/life 1000/1000 spans; talk 32,165=32,165; sourced 4,000 both arms; the REALIZED_DELTA falsifier final: 4,016 units DEAD at the workshop at tool=0, tools 8 unconsumed a millennium, the spring 10,060 linear no cap) + THE WALL DECOMPOSED IN-SESSION (cProfile 10y vs 100y: TWO quadratic read-side members — the OCC refold ×9.51 per-call + the knowledge re-ranking ×9.17; A·t+B·t² reproduces the α-ladder and explains 77.5% of the kiloyear wall) + THE stageb-1 CONTRACT at CONTRACTS.md §12 (B1..B8: one substrate / the atomic recipe event / per-use wear / the min() cap + silence / the unarmed law / the REALIZED_DELTA oracle / the index-based cost law / the pack-data boundary + gate); the implementation NOT a row (the runtime-promotion gate); 6 changed/created (5 modified + 1 created); 2582+1 + ruff + docguard + topology clean; the report iter-327-stageb-report.md
- iter-326 · 2026-10-04 · lab4 (R2 local-add — the owner's «продолжай» call, the E1 horizon row the iter-325 NEXT named): the lab-4 REPLAY-COST instrument (read/fold seconds + the tracemalloc alloc peak, honest labels, Windows-portable) + the two laws (the instrument law, the KILOYEAR ARITHMETIC law — the step-list pure at 1,000y, zero corpus price) + THE E1 SEGMENTED LADDER 2y→650y (650y = 81,823 events / 465.22 s — the deepest rung the sandbox's 600-s window holds; the t^1.3 forecast REFUTED: local exponents steepen monotonically to 1.81, 1,000y ≈ 930–1100 s) + THE E1 FINDINGS: the FLAT-LIFE LAW (life ~71–72/year from 10y to 650y, 650/651 spans live — no collapse, no explosion), the LINEAR VERB LAWS (sourced 4.00/year exact to 6.5 centuries), the CONSTANT-STATE LAW (projection 25 entities at every depth — only the LOG grows; the accounts pile ~26.3 units/year, the Stage B bounded-source falsifier at scale), the REPLAY-COST DATUM (read-bound 0.62 s/MB, the fold near-free, the alloc peak 3.34× the log) + THE STATION HORIZON PROBE v1 (outside the repo per Rule 9, self-checked end-to-end: the 1,000y PAIRED battery + T1 + the cross-hardware control ride the owner's hardware — the kiloyear REALIZED_DELTA row); 5 changed/created (2 modified + 1 created + 2 docs); 2582+1 + ruff + docguard + topology clean; the report iter-326-lab4-report.md
- iter-325 · 2026-10-04 · lab3 (R2 local-add + one KI#112 fix — the owner's «продолжай lab3 … полную батарею 100y×4» call; the pack's 04 §8 A/B form executable): the labrunner's PROTOCOL ARM (--protocol whole/segmented/paired, --segment-ticks; law 7 — null waits only; whole the default, prior records untouched) + the lab-3 metrics (the mid-horizon LIFE profile, the FINAL MATERIAL STATE — the 03 §8 REALIZED_DELTA surface, player_waits) + tests/test_lab.py the four laws (step-list, segmented player-absent+T1, the LIFE discriminant, the paired delta record); the battery: 100y paired × 4 — whole 8,564–8,749 (life 100% final) vs segmented 12,212–14,038, life 100/101 spans; REALIZED DELTAS LIVE every seed, verb deltas seed-invariant (+394 consumed); the two worlds: the deferred batch (~200 on the store, 28 meals) vs the flow (the rack's ~200, 422 meals); the talk control 3,209=3,209; segmented 2.5× FASTER (20 s vs 51 s); the road pair (1,072=1,072 — the diorama invariant); KI#112 the log identity (seed, anchor, horizon, arm, protocol); 6 changed/created (4 modified + 1 created + 1 KI test-file line); 2580+1 + ruff + docguard + topology clean; the report iter-325-lab3-report.md
