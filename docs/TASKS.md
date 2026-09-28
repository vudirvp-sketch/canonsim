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

- iter-286 · 2026-09-28 · namedroute (R2 — the W7 station's FOURTH row, the owner's «точечный и быстрый (read-side only)» call over iter-284/285's boundary (a) — the refusal's institutional cause as a rendering row; the same call conditionally declining the disappearance-battery extension and opening W8, both conditions resolved): the named-boundary rendering route landed read-side (rs-13, the gloss-boundary family's thirteenth member, the rs-2/rs-4 precedents' own shape — zero canon, zero gate, zero machinery, the LOG untouched, the golden corpus byte-identical, zero corpus price): the pack table templates.json::rejection_boundaries (GATE name -> the reader prose naming the refusing authority; leverage_over -> «no minted word to lean on» — the registry as the leverage authority, the coerce family's own lean/hold register), glossed at ONE boundary (render/chronicle.py::gloss_rejection_boundary — the failed_test's gate segment, the noun/holder prefix the door's own machinery; an unglossed gate answers EMPTY, the flow-gloss fallback law: the raw machine token never reaching the reader) and landed as the boundary slot BEFORE the generic outcome loop (the rs-2/rs-4 precedence), the province intent_rejected line carrying the rs-12-form conditional tail {boundary? — {boundary}} — every consumer (the tale's gated line, the entity view's ungated record) through the one template, rs-1's one-boundary law; the block-name constant's single owner core/intent.py (REJECTION_BOUNDARY_BLOCK, D-024 — the lint and the renderer import one constant); the load-time lint owns the refusal (core/packlint/actions.py::_templates — the vacuity law at the door: a gloss for a gate this pack's requires never arms is dead data, the armed union the vocabulary); MEASURED (the witness tests/test_namedroute.py, 6 tests): the no-word twin's runner record renders «tries to coerce — impossible here — no minted word to lean on» — the Q5 boundary CLOSED at the readable surface (the committed package's record carries the hold minted and spent — «now holds something over Garrick … / leans on Garrick — the hold is spent» — the discrimination now a PROSE fact, the raw failed_test token never leaking), the unglossed gates render the standing line UNCHANGED (the golden corpus's own move-refusal byte-stable), the tale gate UNTOUCHED (the refusal never enters the tale — the boundary rides the RECORDS surface, the surface the W7 kit's readers actually read), the unarmed twin loads and renders the standing line (the table optional, the other packs' bytes untouched), the lint refuses the dead rows (the never-armed gate trait_held, the unknown gate, the empty and non-string glosses); THE OWNER'S TWO DISPOSITIONS, both resolved by the same call: (1) the disappearance-battery extension to the remaining majors (the meso units: the crossing, the step bench, the winter kin, the camp) — NO by the owner's own criterion («глобально поможет проекту, а не допиливание»): the meso units' drivers already pass the anchor's disable test (ANCHOR_REGION §5 — eight loops, remove one unique driver, the others survive), the battery's three arms answered NEW capability questions (the verb, the hook, the registry — no uncovered capability remains), further arms would re-measure carried evidence; the row STAYS AVAILABLE for a NEW major's own arm (the station law's own form: the battery fires per new capability, never as backlog); (2) W8 (integration readiness) OPENED on the conditional call («если нет, то и w8 открыть») — the W7 station COMPLETE (four rows: iter-283 the battery, iter-284 the LLM half, iter-285 the live half, iter-286 the named-boundary route), W8's first row the seven-criteria readiness audit (WORLD_WORKPLAN §10 — each criterion cited to its standing owner, the gaps named where the evidence is thinner than the claim); 13 paths (render/chronicle.py, core/intent.py, core/packlint/actions.py, content/province_pack/templates.json, tests/test_namedroute.py (new) + the 8 doc syncs); 2564 dots + ruff + docguard + topology --check clean (R2 — read-side only; zero canon change, the LOG untouched, zero corpus price); KI#107 deleted at the §5 cleanup (closed iter-285)
- iter-285 · 2026-09-28 · neglive (R0, doc-only — the W7 reading band's LIVE half, the owner's «продолжай работу над задачами класса мирового трека» continuation call with the live reading delivered in the chat; the iter-270/280/282 precedent's exact form — the blind Q1–Q7 before the preset reveal, then the owner's own post-preset scoring, this iteration verifying it against the standing iter-284 preset): every pre-set bar MET n=1 — Q1 both halves (the departure «Maren takes the road to the half-pay keep» in A against «at: Malby» in B + the social voice: the councils 12/1, the owner's own 11×t26335+1×t4175 count, B's nine talk/rumor_told pairs with seven rumors and two disbeliefs), Q2 the carrier per world (A: Maren leaving for the keep, her fear persisting at 43, the market silent after her last fire-talk; B: no carrier, the fear decaying to 0 through the drift records, the market talking on one-voiced — plus the live band's own epistemic note: no «grief» variable in the files, the carrier an interpretation over fear/fatigue/movement), Q3 the trade (the presence exchanged — Maren absent from A's brief_final present_entities; the market «не мёртв, а изменён», the dead reading refused; the voice passed from a person to the institution; the intentional-exchange conclusion honestly refused), Q4 the wergeld vigils 3=3 (no ritual difference claimed), Q5 the dead door's both halves (C's lever + the landed coercion with trust 25/fear 75 against D's inert knowledge + the refusal «impossible here») with the institutional cause declared beyond the readable surface unprompted + the live band's sharpenings (the coerce verb present in both vocabularies — the block at the intent level; the mechanisms indistinguishable; coin 6=6), Q6 the invisible door's FULL catch (the histories byte-identical by the owner's own diff AND the sell_bloom vocabulary line named with exact references, 38 verbs against 37, never used — the D-108 law at the live band), Q7 free (the namings divergent from both LLM readings' lexicons while the differential shapes converge — the free-band law reproduced across reader classes); THE CONVERGENCE QUESTION (iter-284 §G) RESOLVED YES — the same forms as the converged LLM readings AND all three ripples (the wait-band, the watch-briefing, the records' entanglement) caught in the blind half: the disappearance's footprint measured at BOTH bands; the honest boundaries: the live band n=1, the Q3 soft-form leg (the person-vs-place thesis circled, never pronounced verbatim — reader-form variance, never prose-fixed), the kit README's one-scenario framing imprecise for C/D (the owner's catch — kit-side, Rule 9, the repo's records carry the correct two-slice facts); VERDICT: the W7 reading band CONFIRMED at BOTH bands (LLM n=2 + live n=1); KI#107 found and closed (STATUS.md's rolling header left one iteration stale by iter-284's Next-step-only edit)
- iter-284 · 2026-09-28 · negread (R0, doc-only in the repo — the W7 reading band's LLM half, the owner's «продолжай работу над задачами класса мирового трека, W7» continuation call — the station's second row, its agent side; the experiment itself outside the repo, Rule 9 — the runner, the kit, the transcripts): the battery's answers as BLIND READINGS over the same battery's own twins — the reading kit in the recorded W5 form (FIVE packages over the committed pack + the three iter-283 twins: the compressed mourning carrier seed 2 committed/no-mourns/no-settle + the crafted JOURNEY seed 42 committed/no-word; each package the tale + the actor's opening/close records + the site's close record + three briefs at the natural cut mirrors; byte-identical on the double regeneration; A/E's tale+records+site byte-identical, the briefs differing by exactly one active_options line sell_bloom); the pre-set audit BEFORE any reading (seven bars restating the battery's measured facts); THE PROTOCOL ERROR AND THE HONEST FIX — the first two blind sessions ran while the preset sat inside the kit dir, both readers transparently disclosed opening it, the pair DISCARDED as formal evidence, the preset staged OUT, two FRESH clean sessions run — the formal n=2 (the pilot's convergence with the clean pair the robustness datum, never the measurement); MEASURED: Q1 MET convergent (the disappearance differential's both halves — the departure «Maren takes the road to the half-pay keep» in A against staying in B + the social voice: the councils 12/1, the rumors 2/11), Q2 MET convergent (the carrier per world — the fear axis 43/0), Q3 MET convergent (the trade — the voice rode the person, the market CHANGED not dead, the dead reading refused by both), Q4 MET n=2 (the families' wergeld vigils identical 3=3 — the disable test's core), Q5 MET convergent (C's lever + the landed coercion with the pair axes trust 25/fear 75 against D's inert knowledge + the refusal «impossible here», the pair axes absent — the institutional cause declared beyond the readable surface by both readers unprompted), Q6 MET convergent — the invisible door's FULL catch (the histories identical AND the sell_bloom vocabulary line named by both — the D-108 law at the reading band: the unused door invisible in the tale and the records, legible ONLY in the briefs' action vocabulary), Q7 free (the namings divergent across the two readings of the same material — the free-band law reproduced — while the differential shapes converge); THE READERS' OWN DISCOVERY: the disappearance's footprint WIDER than the deterministic census — the wait-band ripple (A's waits medium / B's low: the importance rule's per_far_hook term, the committed wait action's TWO success hooks [wilmot_grief_ramble, market_mourns] against the twin's ONE at the medium threshold 2 — the seeding law's shadow over every wait's score, the mechanism verified post-hoc), the watch-briefing ripple (7/6 knowledge_transfers), the records' memory entanglement (the vigils + the runner's return in B's Maren record only) — canonical differences the iter-283 census never enumerated, found from the read material alone; VERDICT: the reading band CONFIRMED at the LLM band n=2 — every pre-set bar met, the station's law held (no prose edited, no gate raised, no machinery promoted, no pack change); the honest boundaries classified (the refusal's institutional cause beyond the readable surface, named never routed; the talks' volume riding the low-importance tale band — the talk half legible in the actor records; the Q4 guild-classification variance reader-side); the owner's live half open — the kit delivered with the questions + the sealed preset, the convergence the owner's own next beat; 8 paths; 2550+9 + ruff + docguard + topology --check clean (R0 — doc-only in the repo; zero code, zero pack, zero canon change, the LOG untouched, the golden corpus byte-identical, zero corpus price)
- iter-283 · 2026-09-28 · negative (R2 — the W7 station's FIRST ROW, the owner's «продолжай работу над задачами класса мирового трека, W7 открывай если больше ничего не осталось» call: W6 complete at both bands, no open row remained — the station ENTERED on the owner's explicit call; the station's law: for any new major capability, regime or institution the eight questions — why possible / why not universal / what does it replace / what does it make harder / who profits / who resists / who remembers / what if it disappears — then the compression test): the battery run on the SAME committed package, zero core, zero pack change, the LOG untouched, zero corpus price; the scope — the three majors with committed consumers and honest deterministic instruments (the fourth verb settle iter-273, the mourning hook market_mourns iter-264/274, the secrets/leverage registry); the admission evidence CITED to its owners (D-024 — the grammar wall, the measured door, iter-274's price), never re-derived; MEASURED: the negative-space census (why not universal — the closed gate vocabulary: exactly one of noun/holder per account gate; the no-leak option gate: the option's availability gate the SAME prop read as the hook trigger; the families' deadband: threshold 50 over trigger 40; the tale gate: min_importance medium; the fixed secret subjects; D-238's calendar cited never re-measured); the lint's measured refusals (who resists — an EMPTY registry and an unseeded hook both refuse at load: the capability's structural floor); the disappearance battery's three arms over pack-data twins (what if it disappears): (a) settle gone → the calm composition run BYTE-IDENTICAL (2269=2269 — the D-108 both-arms law at the capability scale: an unused door costs nothing) + the buyer's purchase probe refused at the GRAMMAR level (RunnerError — the iter-273 wall returned in its hardest form: the world cannot even express the transfer); (b) the mourning gone (the hook AND its seed removed together — the loading band the two lint refusals measured) → the departure never fires (the mistress's moves 1→0, her end keep→Malby), the market's social surface stays loud (talks 2→287, rumors 2→22, the council 208→1 — iter-274's measured price inverted arm for arm, the carrier's footprint), the other families surviving the disable test (the feud's vigils 4=4, the macro arm's sourced 4=4; totals 2269→2372); (c) the word unregistered (the registry's third key removed) → the read STILL mints the knowledge exact (the fact survives — the write is the action's own) but zero levers and the coerce refused at actor.leverage_over (the door dies — the registry IS the leverage authority); the compression test's reachability inventory (who profits): all 76 event templates producible by construction (an action's event type, a structural rules declaration, a group's own macro/condense arming, or the intent door), every account-kind gloss / flow gloss / symbol declared or referenced, every knows-table entry matchable by a mintable token, the four entity ids no other data references each carrying their own canonical door (the lamp the corpus's instrument, the traffic group its macro_event arming, the jug its use_effect on an axis with three named consumers, the sack its flammability), the census's «0 consumerless» cited (the cov-1 instrument's row) — VERDICT: no decorative material at the measured band, the pack compressed; the honest boundaries classified: the band is reachability-BY-CONSTRUCTION (an unfired surface is possibility-space — the player's doors stay, the anti-pattern law), the unglossed mintable literals (the_flood_story, the_winter_kin, the failure-path tokens) ride the documented dry fallback (a reading-side shape, never touched), the ungarrisoned window (0 patrols both mourning arms) the composition witness's own recorded limitation; no plot written, no machinery promoted, no pack change; the witness tests/test_negative.py (10 tests, the claim packet); the station's next rows — the owner's call (the negative questions' reading band, further majors' disappearance arms, or W8 when the owner calls the station complete); 9 paths; 2550+9 + ruff + docguard + topology --check clean (R2 — the crafted twin pairs + the static inventories + the docs; zero core, zero pack, zero canon change, the LOG untouched, the golden corpus byte-identical, zero corpus price)
- iter-282 · 2026-09-28 · liveconfirm (R0, doc-only — the W6 reading band's live half over the FIXED material, the owner's «продолжай работу над задачами класса мирового трека» continuation call; the owner's blind Q1–Q5 over the iter-281 re-measured kit received in the chat BEFORE the preset reveal, then the preset with the owner's own scoring, this iteration verifying it against the pre-set bars — the iter-270/280 precedent's exact form): ADVENTURE met 4/4 at the live band (A1 the departure with the route's own ticks; A2 FULL — the road's toll (fatigue 0→70) AND the NIGHT FORM quoted verbatim, both night lines: GAP (a) closed at the LIVE band — 0/3 readings at the unfixed kit → 3/3 at the fixed kit, the routing's measured effect at both bands; A3 the objective reconstructed through the causal path per the bar's own rule — the iter-280 live miss FLIPPED to MET, reader-policy variance on materially unchanged material; A4 the changed return — the fatigue as the physical trace, «the hold is spent» as the spent lever, the static 50/50/6 as the contrast); MYSTERY met 3/3 (the FOURTH consecutive full carry — six independent readings across both bands and both kit versions, the contour reader-forced, the strongest standing extraction datum); POLITICS P1 PARTIAL (the interests core carried — camp/Garrick, guild, old families, watch — but the market's people NOT isolated as a standing interest, the market read only through Malby as a location: the live breadth variance against the LLM band's P1 MET n=2, iter-280's live reading had carried it via Maren — reader-side, never prose-fixed), P2 MET (the differential table assembled AS different: the watch's alarm, the guild's administrative barring, the families' ritual wergeld vigil), P3 PARTIAL at the strict bar in the SAME shape as the LLM re-measure band (the named legs closed at the live band too — the guild's AGENCY carried, the squeeze never misread as Garrick's doing; the causal row quoted in full riding rs-12's knows tail, the account line's own surface: GAP (b)'s named legs closed at BOTH bands; the honest residual set reproducing one-for-one: the climb quoted «16→20» without the intermediate 18 — the record's two +2 increments at t4767/t4769, all the numbers on the surfaces; the decisive-move slot the fires — the same honest pick as both LLM readings; the standing terms inside the quoted row never separately fixed; the public retention not explicit — reader-synthesis residuals, never prose-fixed, the discrimination law standing); the FREE namings again divergent across the same pack's two packages (noir-blackmail / labor drama / errand-quest against diversionary drama / debt strife / blood-feud chronicle — the genre-matrix labels never the free namings, the owner's own explicit note; the difference itself the measured datum per the FREE rule) — the divergence half carried at the live band over the fixed material; the extraction-strength datum updated (the mystery contour 6/6 reader-forced; the adventure objective live 0/1 → 1/1, the variance measured in both directions; the night form and the named legs 3/3 at the fixed kit); the honest delivery note recorded (the iter-281 kit attachment did not re-carry audit_preset.md — the owner's own observation; the reveal rode the standing iter-279 preset, the same pre-set bars unchanged, the blind sequence held per the owner's own statement; iter-281 §G's «с пресетом» claim corrected — a kit-side delivery wrinkle, zero repo state, no KI); the verdict: the reading-side CONFIRMED at BOTH bands over the fixed material, W6 COMPLETE at both bands (the substrate row iter-278, the reading band iter-279/280, the routings + the LLM re-measure iter-281, the live re-read iter-282) — W7 the owner's explicit call; 8 paths; 2540+9 + ruff + docguard + topology --check clean (R0 — doc-only; zero code, zero pack, zero canon change, the LOG untouched, zero corpus price)
- iter-281 · 2026-09-28 · gaproutes (R2 — the W6 station's two double-confirmed RENDERING_GAP routings, the owner's «продолжай работу над задачами класса мирового трека, делай то, что логичнее и правильнее сейчас сделать, а не потом» delegated call over iter-280 §F; W7 stays "after W6" — the station order held, the iter-279 argument): the repair class per the classification law — a RENDERING surface, never prose, never a gate, never machinery (the rejected knob law respected: the moves stay low-importance, the T7 tale gate untouched — the night form lives on the records surface, the entity views, the kit's own surface); GAP (a) THE NIGHT RISK FORM closed read-side: two condition namespaces over the iter-265 law (render/chronicle.py — the event's own phase as `phase.<id>` booleans via phase_of_tick, the event site's props as `site.<prop>`, the location fold's event-scoped view) + the move line's night arm `{phase.night?#night_arrival#|.}` (the SYMBOL indirection carrying the composed night+lit condition — the engine's conditional partition splits at the first `|`, the inner branch rides a symbol expanded after the outer choice; zero engine change); GAP (b) THE BALANCE-MOVE ASSEMBLY closed at its named legs: the account line's KNOWS TAIL `{knows? — {knows}}` on account_sourced (rs-9's `{secret?}` tail's own shape — an account event that mints knowledge carries its witnessed row on the line through rs-1's boundary, one table every consumer; the flow events carry no knowledge and render dry) + the_paper_repriced re-authored as the tail (the guild's agency + the answer-to-withhold + the standing terms + the climb) + the_dry_year_notched de-redundantized against its kind gloss; zero canon, zero core, the LOG untouched, the golden corpus byte-identical (the templates never enter the log); the witness tests/test_gaproutes.py (10 tests, the claim packet: the mechanism census, the symbol shape, the journey arm, the tale-gate arm, the lit-night arm, the squeeze arm, the pure-function arm, the corpus arm) + the pins updated (repricing/stepbench/debt1/campaccount/freightvol); THE RE-MEASURE (Rule 9, outside the repo): the kit regenerated in the iter-279 form over the fixed pack (JOURNEY 43 events / tale 25 lines — the prior kit's exact shape; POLITICS 96/58), byte-identical on the double build, the same Q1–Q5 frames, the blind glm n=2 per question, fresh sessions, the bars never shown — ADVENTURE 4/4 n=2 (the NIGHT FORM extracted and quoted by both readings — GAP (a) CLOSED at the re-measure; the prior band: absent from the material, missed by three readings across two bands), MYSTERY 3/3 n=2 (no regression), POLITICS P1/P2 MET n=2 + P3 materially improved (the guild's agency carried n=2 — the prior band's single agency misread eliminated; the causal row quoted in full n=2 — GAP (b)'s named legs CLOSED; the honest residuals named never prose-fixed: the intermediate 16→18→20 arithmetic unassembled though all numbers sit on the surfaces (the opening record's 16, the two squeeze lines, the close's 20 — a reader-synthesis residual, the discrimination law's mirror), the decisive-move slot still the fires (an honest pick — the fires ARE a balance move), the public retention not explicit); the free namings again divergent (tragedy only for the politics, the travelogue only for the journey — the divergence half carried at the re-measure); the verdict: the two routings LANDED, the reading-side now CONFIRMED at the improved band, W6's own rows COMPLETE — W7 the owner's explicit call; the kit + the preset delivered as the sandbox attachment (the owner's live re-read the owner's own next beat); 14 paths (the soft-limit breach the scope's own note — the two routings + the re-measure one task, the census re-pins the template change's own blast radius); 2540+9 + ruff + docguard + topology --check clean (R2 — read-side only; zero canon change, zero corpus price)
- iter-280 · 2026-09-28 · liveread (R0, doc-only — the W6 reading band's LIVE half, the owner's «продолжай работу над задачами класса мирового трека...» continuation call; the owner's blind Q1–Q5 received in the chat BEFORE audit_preset.md, then the preset reveal with the owner's own scoring, this iteration verifying it against the pre-set bars — the iter-270 livescored precedent's exact form): MYSTERY met 3/3 at the live band (the hidden shave, the deliberate tally read, the knowledge-as-leverage — FULL cross-band convergence with the LLM band's 3/3); ADVENTURE A1/A4 MET, A2 PARTIAL (the road's toll carried — the live token the fatigue 0→70 against the LLM band's road-toll, the same half; the NIGHT form missed), A3 MISSED at the bar (the obtained half carried — the shave knowledge + the leverage over Garrick; the goal half refused as «not given explicitly» — the too-literal criterion against the bar's reconstruct-through-the-causal-path rule); POLITICS P1/P2 MET (the differential table assembled: the guild's economic barring, the families' ritual vigil, the watch's rotation, Maren's distrust), P3 PARTIAL at the strict bar (the climb 16→20 + the public rituals carried; the standing-terms persistence, the intermediate 16→18→20, the repriced row's public retainment missed); the standing CONVERGENCE question answered YES at the band level — the SAME two legs fail at BOTH bands (the night form, the balance-move assembly — three independent readings across two reader classes), the two iter-279 RENDERING_GAPs DOUBLE-CONFIRMED and closed as named gaps (the live band did not rescue them; no prose edited, no pack change, no machinery); the ONE cross-band leg divergence (A3) classified as the LIVE band's reader-class variance — the mirror of iter-270's resolution (there the glm miss was the LLM band's own; here the live miss against the LLM band's n=2 carry), the material carries the form; the honest extraction-strength datum recorded: the mystery contour reader-forced (every reading, both bands), the adventure objective reader-optional (LLM 2/2, live 0/1); the FREE band: the two packages again read materially differently (the journey: travel vignette + economic mystery + coercion; the politics: institutional + disaster + debt + feud-ritual) — the divergence half carried at BOTH bands, the genre-matrix labels again never the free namings; the RENDERING_GAP/SUBSTRATE_GAP discrimination law STANDING per the owner's own closing note (a reading miss never proves a substrate lack — the deterministic band carries the night form and the terms' persistence; first separate form-loss-at-reading from form-absence-in-material); the verdict: the W6 READING BAND COMPLETE (LLM n=2 + live n=1), the reading-side PARTIALLY CONFIRMED at both bands, W7 + the two gap routings owner-routed; + the §5 mandatory KI cleanup paid (KI#104/105 closed iter-269, KI#106 closed iter-277 — deleted from STATUS, the records in git + this ledger); 7 paths; 2530+9 + ruff + docguard + topology --check clean (R0 — doc-only; zero code, zero pack, zero canon change, the LOG untouched, zero corpus price)
- iter-279 · 2026-09-28 · genreread (R0, doc-only in the repo — the W6 reading band's LLM half, the owner's «продолжай работу над задачами класса world track, делай то что логичнее и правильнее сейчас сделать а не потом» call; the experiment itself outside the repo, Rule 9 — the runner, the kit, the transcripts): the reading kit built over the COMMITTED pack in the recorded W5 form (iter-207) — TWO packages, each carrying its genres' chains in ONE history (the JOURNEY package seed 42: the iter-278 JOURNEY chain, adventure + mystery together; the POLITICS package seed 2: the both-fires road merged with the master's walk and squeeze — the keep + Malby fires, the grief at each, the guild's council, the families' two vigils, the paper 16→18→20, the repriced row public), byte-identical on the double regeneration; the pre-set audit written BEFORE any reading (the isolation law — the iter-278 genre shapes restated as reading bars, a separate kit artifact); the blind glm readings n=2 per question, a fresh session per reading, the bars never shown — MYSTERY met 3/3 legs n=2 convergent (the hidden fact, the deliberate tally read as the discovery path, the revelation as the landed corner against the dead door); ADVENTURE 3/4 n=2 (the departure, the objective, the changed return — one reading carrying the moved pair's numbers; the risk leg's road-toll half carried, the NIGHT form absent from the material — RENDERING_GAP named: the unlit crofts a substrate fact the reading form never surfaces, the moves low-importance by the T7 law, no gate raised); POLITICS 2/3 n=2 (the interests + the differential contrast extracted cleanly — the guild's economic barring against the families' ritual vigil; the balance-moving move NOT assembled at the strict bar — the climb quoted by both, the permanence slot taken by the burnout, the agency misread once — RENDERING_GAP named: the squeeze's causal row rides the scene card's knows gloss, outside the W5 kit form); the FREE-genre band: the same pack's two packages read materially differently (tragedy only for the politics, the economic/character frames only for the journey — the hypothesis's divergence half carried; the genre-matrix labels not the free namings, the chronicle register leading the spontaneous vocabulary, the shapes extracting under directed frames); the verdict — the W6 hypothesis's reading-side PARTIALLY CONFIRMED at the LLM band, two RENDERING_GAPs named never fixed (no prose edited, no pack change, no machinery — the station's law held); the owner's LIVE band OPEN (the kit delivered: READING_INSTRUCTIONS.md Q1–Q5 + audit_preset.md, the owner's reading the standing next beat); 8 paths; 2530+9 + ruff + docguard + topology --check clean (R0 — doc-only; zero code, zero pack, zero canon change, the LOG untouched, zero corpus price)
- iter-278 · 2026-09-28 · genre (R2 — the W6 genre matrix's FIRST ROW, the owner's «открывай задачу по W6» call; the station's law: a failed genre test identifies the missing world substrate, never triggers plot writing): the matrix run on the SAME canonical package at the deterministic band — the committed province_pack untouched, zero core, zero pack change, the LOG untouched, zero corpus price; ADVENTURE measured (the tally journey's four legs: the departure, the night risk cited (iter-185's law), the objective — the word exact + the lever at the read's own commit, the changed return — the corner's pair trust 25 / fear 75, home with the word, the lever and the changed relation; the HARD risk: the riverroad-keep edge closed (the divergence-probe form, the I0 twin's shape) — the world refuses the journey outright, three rejections as facts, nothing minted, the fork's two returns diverging materially); MYSTERY measured (the registered secret the_camps_word NEVER volunteered — the silent world: a full morning at the stacks, zero word records, the corner refused at the lever gate itself, the door IS the leverage test; the revelation's causal weight as the fork — the corner lands only through the discovery, the knowledge the difference between a moved relation and a dead door); POLITICS measured (the same fire pressure family tipping THREE institutions at the arms' pinned seeds 53/139/2 — the market fire → the guild's council + the public row, the keep fire → the garrison's patrol, both fires → the families' vigil ×2 (each single fire waking exactly one elder, the deadband); the balance-moving move: the squeeze re-priced twice on the COMMITTED package — the paper 16→18→20, the beam's people learning the_paper_repriced exact, the coin untouched, the terms persisting); the four carried genres cite their W5 evidence (biography iter-191; comedy/tragedy iter-194/206/208/209/270; relationship drama the winter-kin line) and the census pins all seven genres' committed surfaces (rs-7/rs-8, rs-6 on rs-10, the winter-kin doors + secret, the account-chain doors); the mechanics owned by test_tallyread/test_triangle/test_repricing (cited, read under the genre's lens, never re-derived); the honest boundaries classified: the hard-risk arm rides the AUTHORED edge closure (the I0 inventory's route-writer candidate — SUBSTRATE_GAP, awaiting repetition), the mystery's band one fact/one path/one revelation, the player's re-pricing power iter-271's own residue, the READING band owner-routed; the witness tests/test_genre.py (10 tests); 9 paths; 2530+9 + ruff + docguard + topology --check clean (R2 — the crafted runs + the docs; zero core, zero pack, zero canon change, the LOG untouched, zero corpus price)
- iter-277 · 2026-09-28 · worldcontext (R0, doc-only — the owner's world-track archive-ingestion call: the external WORLD_TRACK_NEXT_v4_AGENT_PACK_v4.5.zip FULLY INGESTED AND RECONCILED against HEAD, never merely summarized): every pack claim classified — canonical doctrine (already owned by AGENTS/VISION/the worldbuild owners), current implementation truth (the pack pins iter-272 @ 8ec6442 — four iterations behind: the iter-266 dispositions, rs-9/rs-10, the settlement verb, stepbench, moverelease and the I0 witness all postdate its snapshot; repository code/tests/STATUS/TASKS kept authoritative), historical evidence (D-236–D-240 retained as evidence, never reopened), hypothesis (the frontier synthesis candidates — PROPOSAL, unpromoted), deferred (B1, the dormant regimes, the standing rows), owner-gated (D-236, the runtime-promotion gate, W6 entry), closed (W1–W4, the phase ladder); the durable result docs/worldbuild/WORLD_TRACK_AGENT_CONTEXT.md (new — the compact surface: identity, the non-negotiable causal rules, the canon/LLM/player boundary, the worldbuilding boundary, the proven substrate, the evidence conclusions, the open hypotheses, the deferred mechanisms, the W-stage boundary, navigation, anti-patterns — a future agent never needs the pack re-uploaded); the pack preserved verbatim as historical/bootstrap evidence at docs/worldbuild/archive/ (the md5-pinned zip + the provenance README — the legacy-archive law: open only for the caravan dossier, the probe contracts, the regime cards, the intake crosswalk); the W-boundary recorded per the owner's directive (W1–W4 closed historical foundation, W5 gate met / evidence retained, W6 the current execution stage, W7 after W6, W8 after W7 — no old stage reopened without fresh regression evidence); KI#106 found and closed (the ledger's duplicated iter-276/iter-275 rows — the squash landing's artifact); 11 paths; 2520+9 + ruff + docguard + topology --check clean (R0 — doc-only; zero code, zero pack, zero canon change, the LOG untouched, zero corpus price)
