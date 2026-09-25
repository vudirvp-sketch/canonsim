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

### Iteration ledger (one line per iteration; the tail capped at 10 by the doc guard — older lines live in git; per-iteration detail: the D-rows + the owning docs + worklog + git, never restated here, the header's own law)

- iter-231 · 2026-09-25 · ci-unred-nav-variation (the owner's 2026-09-25 engine report — the nonexistent add_theme_type_variation call killing _ready at _build_nav_rail + the unused row warning — + the CI-red report «в прошлых двух итерациях как минимум у тебя тесты на репо проваливаются», runs 82–84 red since iter-227): KI#93 the launcher/gateway pipe chain's buffering owned by the chain itself (the gateway child rides -u, the supervisor line-buffers its own stdout, the test spawn strips PYTHONUNBUFFERED — the sandbox's global var had masked CI red: the bind line sat in the child's block buffer past the 90s boot probe, the launcher honestly reported failure while every local run stayed green) + KI#94 the NavButton wiring through the theme_type_variation PROPERTY (Redot 26.2 has no method form; the negative pin) + the dead row local removed; 7 paths; 2285+6 + ruff + docguard clean (verified in the standard AND the stripped-var env — the CI/owner condition; zero core change, zero pack change, the LOG untouched)
- iter-230 · 2026-09-25 · wb-12-token-audit-chat-follow (the owner's «тема и UI все так же убоги, тема ужасная» + «в чате при получении сообщений от языковой модели => не происходит плавной прокрутки вниз» calls, the v5.2 plans pack the direction hand-off): theme@0.3 — the token audit per VISUAL_SYSTEM_UI §2/§3 (the neutral ramp re-pinned over the Catppuccin Mocha VALUE reference — the layered-luminance mechanism per §6, ONE accent #89b4fa, accent_deep retired, the NavButton type variation + styles/chip_busy) + the chat follow law (the tween over the scrollbar's float value never the int jump, the layout-settle await, the near-bottom gate so a reading owner is never yanked, the follow on every role, the bounded late-layout re-settle) + the GENERATING chip (§5's Chat matrix state made visible: pulsing dot AND label, §4's not-color-only) + test_shell_contract's theme@0.3/smooth-follow pins (+1 test); 10 paths; 2285+6 + ruff + docguard clean (zero core change, zero pack change, the LOG untouched)

- iter-229 · 2026-09-26 · visual-system-admission (the owner's 2026-09-26 «вот и отлично, зафиксируй где нужно и обращайся при дальнейшей работе! нынешний ui - ужасен! поэтому всеми тремя руками и ногами - за!» call over the external 24-section Visual System and UI Engineering instruction document): docs/VISUAL_SYSTEM_UI.md ADMITTED as the visual rows' law owner (D-211) — the surface-driven grammar (CANVAS/SURFACE/CONTAINER/CONTENT/ACTION, not card-driven) + the semantic token taxonomy (SURFACE_*/CONTENT_*/ACTION_*/BORDER_*/STATE_*/AUTHORITY_* — the theme the single source) + the neutral-first/ONE-accent color law + the not-color-only accessibility invariant + the per-surface visual state matrix (Chat EMPTY/ACTIVE/GENERATING · Models EMPTY/DISCOVERED/ACTIVE/LOADING/FAILED · Settings DEFAULT/EDITING/DISABLED/ERROR) + the transplantation protocol (SOURCE→TECHNIQUE→MECHANISM→INVARIANT→ADAPTATION→CONSEQUENCE — mechanisms, not looks) + the reference pack under AGENTS §2.8 (ThemeGen a tool never a decision source; SillyTavern license-sensitive — mechanisms only) + the §8 per-row UI report + the anti-patterns + the wb-12+ candidate queue (each row owner-gated, one row per iteration) + the standing resolutions (functional first, the doc is the law for each row never a parallel program, the app spec's §18 evidence law wins over quiet chrome) + the routing surfaces (NAV §1 + TASKS wb-9+ pointer + STATUS FAQ); 7 paths; 2284+6 + ruff + docguard clean (doc-only, zero code change, the LOG untouched)
- iter-228 · 2026-09-26 · wb-11-load-unload-runs (the owner's 2026-09-26 report over the wb-10 handback — «молча висят + транспорт результ 13» + «модель выбрать не могу, там пусто, моделей не видно, кнопка выбрать модель не работает (проводник не открывается)» + the evidence «llama.cpp и модели запускаются штатно если отдельно запускать»): the transport-13 freeze chain pinned dead — backend.py's model.load/model.unload as RUNS (the chat.send pattern: validate + the ladder walk + admit + launch under milliseconds, the minutes-class managed spawn / graceful stop on the registry's worker thread OFF the coarse dispatch lock, the FAILED diagnostics carrying the observed cause on the run.get wire — §21's honest surface; the single-slot + in-flight admission guards; MODEL_LOAD/UNLOAD_DEFAULT_DEADLINE_SECONDS the rows' own §12 budgets) + llama_process.py's _PipeDrain (one daemon reader per captured pipe into a bounded 64KB tail ring — the Windows pipe-buffer wedge pinned dead, stderr_tail cross-platform over the ring, the os.set_blocking '(empty)' bug dead) + shell.gd's run-poll Models circuits (model-load-get/model-unload-get on the shared tick, the honest picker/load guards — never a silent return, §18; the failed scan re-arm so «моделей не видно» never sticks) + tests (test_backend_row the run-form rework + 3 new pins incl. THE DISPATCH-LOCK regression — model.list ANSWERS while a gated load stands in the port call; test_shell_contract's wb-11 pins); 10 paths; 2284+6 + ruff + docguard clean (zero core change, zero pack change, the LOG untouched, INV-4's three-surface form unchanged)
- iter-227 · 2026-09-26 · wb-10-owner-experience (the owner's 2026-09-25 fix list over the wb-9 handback — the launcher's Popen `buffering` TypeError + «где найти redot.exe и как его подключить?» + «просто открывающийся проводник и выбор уже скаченных локальных моделей» + «пользователь не должен вводить команды чтобы запустить или скачать что-либо!» + «интерфейс вверх убожества»): scripts/workbench_launch.py reworked (the bufsize fix + the folder-aware Redot resolution — release folder → the engine exe, the known names in preference order, one folder deep; CLI/env strict-verbatim, the persisted workbench/runtime/launcher.json, the Desktop-shaped auto-scan, the native tk folder picker once; the observed bind URL forwarded to the Redot child; the bare "--" separator stripped — the latent wb-9 gateway-arg bug) + the model.import work kind (models.py: a LOCAL copy into the models root — .part + atomic rename + live progress + cooperative cancel, the admission gates pre-run, NO network — INV-4 untouched; composition.py wires it unconditionally) + discover()'s models_root (the frontend's open-folder answer) + shell.gd's native-picker Models manager (Add local models…/Add folder… over FileDialog.use_native_dialog with ACCESS_FILESYSTEM, Open models folder via OS.shell_open, the URL fetch demoted to the collapsed advanced row; the theme@0.2 visual pass — the chip/card_user tokens) + Workbench.bat/Workbench Setup.bat the repo-root double-click entries + project.godot 1440×900; tests/test_model_import.py (8) + tests/test_workbench_launch.py (12 — THE REAL SPAWN integration: the buffering crash pinned dead) + the shell_contract/workbench_app/operations pin updates; 18 paths; 2281+6 + ruff + docguard clean (zero core change, zero pack change, the LOG untouched, INV-4's three-surface form unchanged)
- iter-226 · 2026-09-26 · wb-9-model-flow (the owner's «открыл воркбенч, зашел и загрузил модель» + «подтянуть модель откуда угодно» + «настройки запуска llama.cpp... сэмплеры всякие» calls — the model flow end to end): workbench/platform/model_fetch.py (D-208 — INV-4's third sanctioned surface: the outbound model-assets fetch, HTTP GET downloads only) + the model.fetch work kind (models.py, the injected fetcher, admission gates pre-run, the registry's live progress surface + the kind's own 3600s deadline) + workbench/application/settings.py (the typed launch-settings store + backend.settings/backend.settings.update + the atomic persistence) + llama_process.py's sampler flag family + workbench_app.py's MANAGED default (--attached restores the observe-only form) + the exe auto-discovery + the runtime layout (workbench/runtime/{models,llama.cpp,settings.json}, gitignored) + scripts/workbench_launch.py the one-command launcher (the gateway + Redot, the stdout bind-line watch) + shell.gd's REAL Settings surface (the typed fields + the collapsed advanced + the preview) + the Models manager (the URL fetch with live progress); tests/test_model_fetch.py (11) + tests/test_settings.py (10) + the workbench_app/managed/shell_contract/architecture/operations/gateway pin updates; 2258+6 + ruff + docguard clean (zero core change, zero pack change, the LOG untouched, INV-4's three-surface form pinned)
- iter-225 · 2026-09-25 · redot-engine-index (the owner's «отразить в репозитории» call over the external Redot/Godot agent reference index — the tmpfiles hand-off ephemeral, the engine routing homeless): docs/REDOT_ENGINE_INDEX.md ADMITTED (the version firewall + the routing map; admission deltas only — §2.2/§2.3 reconciled to the landed wb-4..wb-8 surface + the v5.2 docs' external-by-law status, §10's skills pinned agent-side per AGENTS §2.8, the external changelog cut) + the routing surfaces (NAV §1/§2/§3 + STATUS FAQ + the wb-9+ pointers in TASKS/CONTRACTS §5 + README's agent list) + docguard's allowlist entry (§6.1's substance record) + D-207 into the standing-rows family row; 9 paths; 2223+6 + ruff + docguard clean (doc-only, zero code change, the LOG untouched)
- iter-224 · 2026-09-25 · gdscript-fix-delivery-protocol (the owner's 2026-09-25 wb-8 handback — five shell.gd parse refusals (806/861/868/999/1042: adjacent string literals, the Python-ism GDScript refuses) + the «тебе ничего комитить и пушить не надо» directive): the five notes ONE literal per line + test_shell_contract.py's adjacent-literal ban over every committed .gd + AGENTS §9/§12 the delivery protocol's standing form (D-206: the agent NEVER git commit/push against the owner's repository — no access; the delta archive rides both channels + the owner-side Git Bash block closes every file-touching report, re-runnable); 7 paths; 2223+6 + ruff + docguard clean (zero core change, the LOG untouched)
- iter-223 · 2026-09-24 · wb-8-managed-models (the owner's «выбирать модель я должно из интерфейса» + «llama.cpp тоже запускаться при загрузке модели» + «настройки подтягиваться и самые нужные флаги» calls over the v5.2 brief — frontend §46 Phase A's Models row + app §11.1's MANAGED half): the managed-models row LANDED — workbench/platform/llama_process.py (the process mechanics, §2's platform/process row: build_server_command the typed honest default flag set — -m/--host/--port/-ngl/-c/-fa on/-a/--jinja/--no-webui + the operator's extras verbatim, re-verified 2026-09-25 against the current llama.cpp server surface; LlamaServerProcess spawn/exit-observation/the §11.1 bounded graceful stop with the OBSERVED exit code; the readiness wait over an INJECTED probe — zero network imports) + scripts/workbench_app.py's --managed form (§11.1's lifecycle policy at the composition root: _ManagedBackend the port-face wrapper — a healthy server delegates unchanged, model.load on a DOWN server spawns llama-server WITH the caller's model (prepare→validate→ready through the adapter's own health probe), the spawned model's unload stops the process, Ctrl+C stops only OUR process, the honest 'unavailable' cause on spawn/ready failures — §12.1's sibling, the model rests SELECTED, the re-load legal; --llama-server-exe/--llama-ctx/--llama-ngl/--llama-args the override surface; the managed ABSENT/LIVE evidence line) + backend.py's model.states READ operation (the load-state read surface's registered consumer) + the Redot half (shell.gd's Models surface — the discovered list + the per-model lifecycle states + Load/Unload with the honest minutes-class per-call timeout over gateway_client.gd's timeout_s envelope, the truthful UNKNOWN/refusal/transport notes, FAILED terminal shown never hidden (D-203's gap); the owner-reported launcher warnings fixed — the UNUSED tag → _tag, the SHADOWED _text → _body, the hygiene pinned) + tests/test_managed_backend.py (17 tests incl. THE REAL SPAWN over the stand-in server tests/_managed_fake_server.py) + test_shell_contract.py's three wb-8 pins + pyproject (workbench.platform); 13 paths; 2222+6 + ruff + docguard clean (zero core change, zero pack change, the LOG untouched, INV-4's two-surface form unchanged — the wrapper only decides WHEN a process must exist, the HTTP stays cli/engine.py's)
- iter-222 · 2026-09-24 · wb-7-live-chat (the owner's «продолжай работу по wb 7» + «могу ли я подключить llama.cpp к реготу» call over the v5.2 brief — frontend §46 Phase A's Chat row + app §22's launcher): the live chat circuit LANDED — scripts/workbench_app.py (the composition root + loopback serve: Gateway + compose_workbench_operations(backend=LlamaServerClient(EngineConfig(endpoint=...))) + LoopbackHttpTransport — the ONE place INV-4's two sanctioned surfaces meet, the port injected never imported; --no-backend the honest admission form — chat.send/model.load/model.unload unregistered; the startup health probe evidence-not-gate — the app serves regardless, chat runs close FAILED with the observed cause; the missing-models-dir loud AppError; the documented defaults 127.0.0.1:8765 + http://127.0.0.1:8080 + workbench/runtime/models (gitignored)) + the Redot half (presentation/redot/scripts/gateway_client.gd the typed POST /op client: the sequential one-in-flight queue, operation_answered/transport_failed, the non-200 transport-failure law, NO endpoint of its own — the shell configures it; shell.gd's live circuit: the URL resolution order --gateway-url > CANONSIM_GATEWAY_URL > the project setting, app.status → session.create (per-process idempotency key) → chat.send → the run.get poll to the truthful terminal COMPLETED/FAILED/CANCELED/FAILED_TO_CANCEL/UNKNOWN with the honest notes, Stop = run.cancel, the bounded §15 message list with the one-shot trim note, the honest badge/Settings/status-bar updates, the backend OBSERVED note from the run's result; the proof mode stays the STATIC deterministic form — no network in the capture) + project.godot (canonism_workbench/gateway/url="http://127.0.0.1:8765" the committed default) + tests/test_workbench_app.py (8 tests: the wiring law incl. the injected-never-imported pin, the honest no-backend form, the loud arguments + the documented defaults, the live loopback roundtrip (session.create + app.status over real HTTP), THE END-TO-END chat circuit over HTTP against the live stub llama-server — the scripted reply observed COMPLETED with the backend identity, the dead-endpoint run closing FAILED) + test_shell_contract.py's three wb-7 pins (the client's committed contract — G8's executable half: no endpoint/llama-API text; the shell's live-circuit markers; the project setting) + .gitignore (workbench/runtime/); 14 paths; 2202+6 + ruff + docguard clean (zero core change, zero pack change, the LOG untouched, INV-4's two-surface form unchanged — the frontend dials the GATEWAY only, frontend §47 G8)
