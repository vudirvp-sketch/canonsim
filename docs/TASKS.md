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
  «открывай mech 2» call over STATUS Next step 1, the tooling-spike arm):
  `mechanics impact --path <pack path> | --ref <name>` — the derived
  reader index (the AST scan over core/brief/render/cli/sim + the
  packlint family, D-118 extended to the source), the exact-name reverse
  query (the rename-safety set), the indexed-matrix pointers (D-024);
  bounded one-hop traversal; tooling-only, stdlib-only (D-012), zero
  runtime change. The A/B falsifier RAN (iter-198, the owner's call;
  TECH_NOTES §17): the injected gate moved none of the three metrics,
  the cognitive premise refuted at scale, the whole-file emission wall
  + silent notes paraphrase measured instead. The structured-patch
  proposal PARKED (the owner's 2026-09-23 call): no machinery, no
  infrastructure — the next step, if it ever opens, is a minimal
  prototype testing exactly whether structured patch reduces the
  whole-file emission failures and the silent notes drift (§17's
  measured classes); full work does not open until that experiment
  exists. The rename-safety lint gap closed as its own slice
  (`rename-1` below). Detail: the iter-196/198/200 records + D-197
  + git.
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
  public-contract surfaces (event schema, canonical log format, fold
  semantics, scheduler order, RNG semantics, pack format, checkpoint
  semantics, the Workbench-gateway public operations) confirmed at
  their standing owners (INV-1..5 + `docs/EVENT_SCHEMA.md` +
  `docs/PACK_SPEC.md` + WORKBENCH_APP_LAW) and FROZEN for the ssi
  initiative's duration — never re-stated (D-024), the strangler
  phases move INTERNAL ownership only; doc-only, zero code, the LOG
  untouched.
- `ssi-2` — DONE (iter-242+243, D-222/D-223): Phase 1 the SSI
  foundation — the READ-ONLY reference copy at `docs/ssi/` (the
  external package verbatim, the overlay the ONLY authored file) +
  `docs/ssi/SSI_OVERLAY.md` (the A–L block matrix onto the existing
  mechanisms, the executable negative-rules subset, the phase
  ladder) + the risk ladder R0–R5 as AGENTS §2.9 (a refinement of
  the 3–5-file soft limit, never a replacement — R0–R2 zero added
  bureaucracy, R3+ carries the compact PCC record in the DECISIONS
  row, docguard-linted) + the executable checks: SSI-N001/N002 in
  `tests/test_architecture.py`, SSI-N006/N007/N010/N017/N018 in
  `scripts/docguard.py` (N018/N020's full forms fire with their
  phases — OPEN, never a silent skip).
- `ssi-3` — DONE (iter-244, D-224 — the owner's 2026-09-26 go-ahead):
  Phase 2 CLOSED — the machine-readable map at
  `docs/SSI_TOPOLOGY.md` (owner/reads/writes/emits for all 82
  core/+workbench/ Python modules; the mechanical columns derived by
  `scripts/topology.py --audit`, drift-pinned by `--check` +
  `tests/test_topology.py`) + the co-change/trajectory audit over
  the last 150 commits (iter-90..HEAD): line counts CONFIRMED
  exactly (1714/1419/1388/1080/2511); loop.py↔pack.py the #1 code
  pair numerically (11 co-changes, lift 9.07, J 0.69) but HISTORICAL
  — all in iter-90..168, dormant since, pack already decomposed
  3990→290 via packlint; ssi-5's core scope SHRINKS on the refuted
  live coupling (the god-objects dormant 75+ iterations — core/'s
  last touch the iter-200 lint guard), ssi-4's target
  (inference.py: 2511 lines born in 2 iterations, single dep)
  CONFIRMED as the active hotspot; N018 VERIFIED (the trajectory
  audit is the executable). VERIFIED independently at iter-245 (the
  owner's verification call: every figure reproduced at the recorded
  BASE; two R0 precisions landed — the D-224 ID column, the
  dormancy wording).
- `ssi-4` — DONE (iter-247+248+249, D-225/D-226/D-227 the PCC
  records; the owner's 2026-09-26 «ssi4 вроде открыть можно»
  go-ahead): Phase 3 CLOSED — the workbench/application/inference.py
  split COMPLETE: 2511 lines → the 10 owner modules (library/chain/
  presets/relations — the semantic-control DATA half; profile/
  resolver — the RESOLUTION half; store/migration/operations/
  compiled — the PERSISTENCE/OPERATIONS half) + the 176-line pure
  re-export facade; split by the ssi-3 semantic owners (the LAW's
  three-layer split, LLAMA_CPP_INFERENCE_CONTROL_LAW §2), never an
  external template; zero behavior change across the steps — the
  public import surface, the gateway operations and the test claim
  packet byte-stable throughout (tests/test_inference.py untouched
  since iter-240); the topology map rows updated in the same
  iteration as every watchlist change (the --check drift pin); the
  packlint decomposition (D-175: pack.py 3990→290, zero functional
  change) the method precedent, now proven twice.
- `ssi-5` — the core strangler (Phase 4, owner-gated):
  loop/director/worldgen/intent internal-ownership moves ONLY — the
  public surface (director.next_beat(...) et al.) byte-frozen (the
  ssi-1 freeze); each step its own R2/R3 iteration with a PCC
  record.
- `ssi-6` — DONE (iter-250, D-228 — the owner's «продолжай работу»
  go-ahead over the confirmed Phase 3 closure): Phase 5 CLOSED — the
  canonical read seam LANDED: `workbench/canonical_read.py` the ONE
  workbench core-import module (a pure re-export shell over the
  10-name read surface: log read_log/validate_header/EventRecord/
  LogError, fold fold/initial_projection/present_in_order, pack
  load_pack/PackError, rng stable_hash); the map's three consumers
  (scene_build, observatory_read, scene_ir) migrated at zero behavior
  change; the law executable twice over (test_architecture's
  core-import ban outside the seam + the seam's watchlist reads pin
  in topology --check); WORKBENCH_APP_LAW §24 synced; ssi-5 explicitly
  NOT opened on the same call — the N018 evidence gate unmet (the
  audit-refuted live coupling stands; that phase needs the owner's
  fresh co-change evidence or the explicit skip, never momentum).
- `ssi-7` — DONE (iter-251, D-229 (R3) the PCC record; the owner's
  «ssi7 и/или ssi8 ==> можешь начать» go-ahead): Phase 6 CLOSED — the
  semantic diff layer over T1: `scripts/semantic_diff.py` (pure
  stdlib, zero core imports) + the 22-test claim packet + TEST_PLAN
  §1.4 the law owner; env-pinning stays §1.1's documented decision —
  the layer ADDS, never replaces T1 (the ledger line + D-229 the
  detail).
- `ssi-8` — DONE (iter-252, D-230; the same go-ahead): Phase 7 CLOSED —
  the GC pass FIRED: the N020 sweep (every artifact class clean — the
  honest negative) + the three deletion cards — the .gitkeep family in
  NON-empty dirs DELETED (7 × 0 bytes; sim/systems/.gitkeep retained),
  sim/ RETAINED (NAV §1's reserved row + D-037 stand — consumer
  absence alone is never deletion evidence), the KI#99 doubled tree
  the owner-side cleanup card (iter-246's fix landed); N020 + block I
  VERIFIED — the ladder complete except ssi-5 (D-230 the detail).
### Iteration ledger (one line per iteration; the tail capped at 10 by the doc guard — older lines live in git; per-iteration detail: the D-rows + the owning docs + worklog + git, never restated here, the header's own law)

- iter-254 · 2026-09-26 · doc9-agents-fork-synthesis (D-232, the optional half of the owner's «согласен с твоими вердиктами => приступай» call): the design-fork law's missing half LANDED — AGENTS §2.7 extended with the synthesis step (intake-39's one fresh atom, the doctrine's §19: enumerate the candidates' advantage/disadvantage axes as independent axes → decompose every disadvantage intrinsic-to-mechanism vs artifact-of-formulation → construct the candidate satisfying the union of advantage constraints and none of the disadvantage-avoidance constraints → name/verify emergence → the honest comparison — kept only if it matches-or-beats the best parent on every material axis while eliminating ≥1 material disadvantage, else discarded for selection; a re-labeled parent or averaged parameters is not a synthesis; L15's combined-design question made a procedure); the selection half (D-198's compare/prefer/never-generalize) untouched — the fork law now carries both halves; 5 paths; 2384+9 + ruff + docguard + topology --check clean (doc-only, the D-022 exception — the owner's fresh call)
- iter-253 · 2026-09-26 · doc8-intake39-routing (D-231, the owner's «согласен с твоими вердиктами => приступай» call over the tmpfiles.org upload): the 413-line agent-instruction edition of intake-38's corpus routed — CONFIRMED-owned (the rework: 552→413 lines, +Role/§0 Governing Loop/§24 Checklist, the contract 17→18, the old §19 gate renumbered to §20; D-199's per-atom verdicts carry over unchanged, the parked five still behind their first consumers — a restating rework is not new evidence, intake-35's second-pass precedent); the ONE fresh atom (§19 Synthesis Over Selection) routed to AGENTS §2.7 — landed iter-254 the same session; the instruction FORM refused (AGENTS §2.8's standing refusals — no second project memory, no nested agent-instruction files); ZERO rows convened (D-175), no REFERENCES entry (the convenience-copy law, the research-method class), no worldbuild routing (WORLD_AUTHORING §19/D-189 the world track's own transfer law); the record: the intake-39 block + D-231; 5 paths; 2384+9 + ruff + docguard + topology --check clean (doc-only, the D-022 exception — the owner's fresh call)
- iter-252 · 2026-09-26 · ssi8-gc-pass (Phase 7, the owner's «ssi7 и/или ssi8 ==> можешь начать» go-ahead): the GC pass FIRED — the N020 sweep over every artifact class (19 scripts + fixtures + playscripts + packs + docs incl. every subdir: every file consumer-referenced; zero tracked-ignored; zero orphans — the honest negative: the cap/collapse/KI-cleanup discipline left no dead committed artifact beyond the marker family) + the three deletion cards (D-230): the redundant .gitkeep family in NON-empty dirs DELETED via git rm (core/brief/cli/render/tests/tests.playscripts/content.tavern_pack — 7 × 0 bytes; sim/systems/.gitkeep retained, the reserved skeleton's only content), sim/ RETAINED (zero imports since birth BUT authority holds: NAV §1's reserved row + D-037's reservation + INV-3's stoplist scope — consumer absence alone is never deletion evidence; dissolving the reservation is the owner's explicit call), the KI#99 doubled workbench/workbench/runtime/ tree the OWNER-SIDE cleanup card (the iter-246 root fix landed, the tree regenerates, the repo carries zero change); the overlay: N020 VERIFIED + block I VERIFIED + phase 7 CLOSED — the ssi ladder complete except ssi-5; 10 paths (7 deletions + 3 docs); 2384+9 + ruff + docguard + topology --check clean (zero code change, the LOG untouched)
- iter-251 · 2026-09-26 · ssi7-semantic-diff-layer (Phase 6, the same go-ahead): the semantic diff layer over T1 LANDED — scripts/semantic_diff.py the instrument (pure stdlib, ZERO core imports: the independent-re-derivation law TEST_PLAN §9 + §1.3's instrument law — the checker never shares the checked implementation's parser; the header's semantic fields schema_version/seed/pack vs the environmental python/commit ignored BY DESIGN and named in the report; the anchors id/t/type/actor/target/cause + deep field paths + the append-only prefix relation + the both-or-neither run-side RngBank fingerprints, the latent-divergence axis RNG-1; exit 0/1/2, loud inputs) + tests/test_semantic_diff.py the 22-test claim packet (the independence arms GREEN: CRLF/interpreter/commit; the mutation teeth RED: every anchor + deep paths + the bool/number kind boundary + length/prefix + the fingerprint axis; the fresh-run↔golden companion arm — run↔golden equality at the semantic level in ANY environment) + TEST_PLAN §1.4 (the law owner — env-pinning stays the documented decision §1.1, the layer ADDS never replaces) + the T1 row pointer + the overlay (block L VERIFIED, phase 6 CLOSED) + NAV (the scripts row + the §3 routing row); D-229 (R3) the PCC record; 8 paths; 2384+9 + ruff + docguard + topology --check clean (zero core change — no core/ file imported or edited, the LOG untouched)
- iter-250 · 2026-09-26 · ssi6-canonical-read-seam (Phase 5, the owner's «продолжай работу» go-ahead over the confirmed Phase 3 closure): the canonical read seam LANDED — workbench/canonical_read.py the ONE workbench core-import module (a pure re-export shell over the 10-name read surface: log read_log/validate_header/EventRecord/LogError, fold fold/initial_projection/present_in_order, pack load_pack/PackError, rng stable_hash; __all__ the pinned surface) + the map's three consumers migrated (scene_build.py, observatory_read.py, scene_ir.py — import re-points + docstring syncs, zero behavior change, the public surfaces byte-stable) + the law executable twice over: tests/test_architecture.py (h) the core-import ban outside the seam across workbench/ (INV-4's sanctioned-module idiom at the core-read boundary) + the seam's watchlist row (its reads cell hard-pinned by topology --check; the drift pin RED on the missing row → GREEN in-iteration, the designed loudness) + the map refresh (the seam's row + the three consumers' rows + the watchlist line + §0/§5) + scripts/topology.py's WATCHLIST sync + WORKBENCH_APP_LAW §24 (the read-side edge = the one seam) + the overlay's phase 5 CLOSED; ssi-5 explicitly NOT opened (the N018 evidence gate unmet — the owner's fresh co-change evidence or the explicit skip, never momentum); D-228 (R3) the PCC record; 13 paths; 2362+9 + ruff + docguard + topology --check clean (zero core change — no core/ file edited, the LOG untouched)
- iter-249 · 2026-09-26 · ssi4-step3-phase-close (Phase 3 step 3, the FINAL): the PERSISTENCE/OPERATIONS half out of the facade — store.py (SCHEMA + InferenceStore), migration.py (the one-way settings migration), operations.py (the gateway family + the chat BASE provider — the ops deriving at their true owner), compiled.py (the platform seam's input) extracted verbatim; the facade = the PURE re-export shell (176 lines); PHASE 3 CLOSED — 2511 → 10 owner modules + the facade, zero behavior change across the three steps, the public surface/ops/claim packet byte-stable throughout (tests/test_inference.py untouched since iter-240); the drift-pin test re-pinned to the emission-free facade; D-227 (R3) the PCC record; 8 paths; 2361+9 + ruff + docguard + topology --check clean (zero core change, the LOG untouched)
- iter-248 · 2026-09-26 · ssi4-step2-resolution-half (Phase 3 step 2): the RESOLUTION half out of the facade — profile.py (the InferenceProfile document + the validation family, §19.1's ACCEPTED laws) + resolver.py (STATES/resolve/_chain_item_state, the §6/§8 effective-state resolver, pure) extracted verbatim; the facade 1157→700; the drift pin RED→GREEN in-iteration (the facade reads + the two inventory rows — the map refresh the same iteration's own law); __all__ completed with the de-facto public names; D-226 (R3) the PCC record; 7 paths; 2361+9 + ruff + docguard + topology --check clean (zero behavior change, the LOG untouched)
- iter-247 · 2026-09-26 · ssi4-step1-inference-package (Phase 3 step 1, the owner's «ssi4 вроде открыть можно» go-ahead): workbench/application/inference.py (2511) became the inference/ PACKAGE — the semantic-control DATA half verbatim (library.py the control model + the 85-control data + the indexes; chain.py; presets.py; relations.py) + the facade __init__.py (the behavior halves pending their steps, the re-exports, __all__ completed) — the public import surface UNCHANGED (tests/test_inference.py untouched and green), the gateway ops byte-stable, zero behavior change; pyproject packages; the WATCHLIST successor = the facade (topology.py + the map refresh + the re-anchored drift-pin breach); the LAW/APP_LAW/NAV/overlay path syncs; D-225 (R3) the PCC record; 15 paths; 2361+9 + ruff + docguard + topology --check clean (zero core change, the LOG untouched)
- iter-246 · 2026-09-26 · ki99-ui-state-path (the owner's «ki99 закрыть» half of the ssi-4/ki99 call): KI#99 CLOSED — the shell's ui_state path doubling (workbench/workbench/runtime/) fixed at its root: globalize_path("res://") returns the project root WITH the trailing slash, the raw three-call base-dir walk counted the slash as a level, landed one short, and the appended literal doubled workbench/ (KI#98's class); the fix normalizes the trailing slash FIRST then walks EXACTLY the real project-root depth (both engine forms correct, never slash-dependent) + the contract pin (test_shell_contract.py) derives the walk depth from project.godot's committed location — a moved root goes RED, never a silent wrong path; 5 paths; 2361+9 + ruff + docguard + topology --check clean (one .gd behavior fix, zero core change, the LOG untouched)

- iter-245 · 2026-09-26 · ssi3-close-verify (the owner's Phase 2 verification call «вторую фазу вроде завершили»): the INDEPENDENT re-verification of D-224 in a fresh session — every recorded figure reproduced EXACTLY at the recorded BASE_COMMIT 08300a0 (the inclusive last-150 window: loop↔pack co=11, touches 13/14, lift 9.07, J 0.69, all co-changes iter-90..168; the window-start sizes pack 3990 / loop 1024; the state-doc pairs 148/144; the line counts; 82 modules; the god-objects' last touches 168/107/145/169; the executable battery 2360+9 + ruff + docguard + topology --check green) + two R0 doc precisions: DECISIONS.md the compound row's ID column completed with D-224 (the body carried the record, the ID list stopped at D-223 — citations now resolve) + the dormancy wording made god-object-precise everywhere it was directory-loose (core/'s post-iter-169 touches = exactly the three gloss/lint commits iter-191/199/200 — economy.py constants + the packlint rename guard; the REFUTED verdict unchanged); 5 paths; doc-only, zero functional change, the D-022 exception (the owner's fresh verification request)
