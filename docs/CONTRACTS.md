# CONTRACTS.md — Pre-Implementation Contracts

> What this file is: the compact pre-implementation contracts for the
> contract-write rows (intake-29/D-175's closing proposal, written
> iter-144/D-177 under the owner's delegation). A contract pins what a
> row's build must satisfy BEFORE it starts: the decisions the row
> leaves open (each grounded in standing code or law), the invariant
> set, the falsifier (TEST_PLAN §9's claim-packet form), the minimal
> test set. What it is NOT: the row's spec — the spec fires
> just-in-time at the row's start, FROM experiment results
> (SPECS_BACKLOG's header law); the contract is the boundary, the spec
> the implementation's own words. Ownership never moves: TASKS owns
> WHAT/WHEN (the ORDER owner decides), the row keeps its acceptance
> criteria, this file owns the pre-implementation HOW-boundary. When a
> row's build lands, its spec absorbs its contract by reference (never
> restated, D-024) and the section here collapses to a one-line
> pointer. Cap-law: `docs/*.md` ≤600 lines, substance-filtered
> (AGENTS §6.1).

## 1. roads-1 — LANDED (iter-145, D-178)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-145 + D-178 + worklog
> iter-145 own the landing record — the pass
> (`core/worldgen.py::_pass_roads`), the one shared read
> (`core/roads.py::exits`), the lint, the §9 claim-packet evidence.
> The contract's own pinned decisions, verbatim, in git history at
> the iter-144 commit.

## 2. res-1 — LANDED (iter-146, D-179)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-146 + D-179 + worklog
> iter-146 own the landing record — the substrate
> (`core/economy.py`: the account primitive, the three verbs, the
> flows on the macro cadence, the derived prices), the door's soft
> arm (`account_at_least`), the resolver (`account`), the commit
> gate's loud floor, the lint (`core/packlint/economy.py` + the
> actions/entities cross-checks), the §9 claim-packet evidence. The
> contract's own pinned decisions, verbatim, in git history at the
> iter-144 commit.

## 3. since-1 — LANDED (iter-147, D-180)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-147 + D-180 + worklog
> iter-147 own the landing record — the fold
> (`brief/since.py::ReunionFold`: the per-entity encounter epochs,
> the apart-window deltas, the reader's apart-born records), the
> cards' since-segments (BRIEF_SPEC §3.4's extension, §3.9's
> amendment — the knower's own segments riding the shared cards),
> the pack's `since_lines` vocabulary + its lint, the §9 claim-packet
> evidence (the fold/document/zero-price arms CONFIRMED at the
> measured band; the decision arm DEFERRED to the first consumer).
> The contract's own pinned decisions, verbatim, in git history at
> the iter-144 commit.

## 4. engine-1 — LANDED (iter-177, D-193)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-177 + D-193 + worklog
> iter-177 own the landing record — the GBNF mapping repo-side
> (`brief/gbnf.py`, the snapshot's engine-facing serialization with
> the door's shape laws encoded; PARSER_SPEC §2.1), the explicit
> adapter (`cli/engine.py` — INV-4's one-module form, AGENTS §4), the
> door wiring (`--engine`, the file contract preserved — the runtime
> engine is "the operator"), the failure→ladder mapping (§5's re-ask
> ladder + the D7 degradation rungs; PARSER_SPEC §5), INV-4 lifted
> with the AGENTS §4/§8 edits riding, the model-facing serializer
> contract now `docs/PRESENTATION_SPEC.md`'s (iter-178), the adapter
> contract tests + the golden grammar + the Layer-1 suite green with
> ZERO gate edits (the §4.3 claim packet's proof; TEST_PLAN §9's
> form). The contract's own pinned decisions D1–D8 + the invariant
> set + the falsifier, verbatim, in git history at the iter-170
> commit. The station-side remainder (the 27B GBNF parse arm + the
> one-model-constrained A/B — §4.3 arm a; the grammar's compile
> check at the live backend) lives on as TEST_PLAN §8.5's standing
> gap rows, the owner's next station run.

## 5. wb-1..N — the Workbench family (the v5.2 Redot brief, owner's 2026-09-24 call)

> Source: the owner-supplied `canonsim_workbench_v5_2_redot_2026-09-24`
> package (5 documents, external — the convenience-copy law D-024: they
> stay outside the repo, this section + the TASKS wb rows the distilled
> owners, D-200 the admission). Contract written BEFORE wb-1 starts
> (iter-215); when each wb row lands, its section here collapses to a
> pointer per the file's own law.
>
> **§-reference map (D-218, iter-237 — the corpus re-homing):** every
> `app spec §N` citation below and across the repo resolves to
> `docs/WORKBENCH_APP_LAW.md` §N (the binding distillation, the spec's
> §-numbering preserved 1:1); every Observatory-doc §N resolves to
> `docs/OBSERVATORY_LAW.md` §N; the frontend spec's §46 implementation
> ladder resolves to `docs/FRONTEND_UIUX_LAW.md` §25; the world-
> presentation contracts (the spec's §§23–31) live in
> `docs/WORLD_PRESENTATION_LAW.md`. The external originals stay with the
> owner — no repo work requires them anymore.
>
> **wb-1 LANDED (iter-215 the Python half + iter-216 the Redot half):**
> the seam chain proven end to end — the tavern and province fixtures
> composed and captured, the double-run PNG byte-diff CONFIRMED (the D4
> falsifier), the REDOT_EXE-gated packet skipping clean without the
> binary; the landing record: TASKS iter-215/216 + the worklog + git.
> **wb-2 LANDED (iter-217):** the Redot shell + the semantic-token theme
> — `themes/workbench_theme.tres` (the §10 token ladder: the
> `Workbench/*` semantic namespace + the styled component types with
> their state sets, the §12 contrast pairs recorded in-file),
> `scenes/shell.tscn` + `scripts/shell.gd` (the code-built shell: the
> §17 nav axes — Chat/Settings live, the later axes honestly disabled —
> the Chat/Settings placeholder surfaces, the §16 status vocabulary
> strip, the §18 backend badge), the main scene switched to the shell
> (the app-entry law; the seam-proof scene now passed explicitly by the
> runner), `scripts/visual_proof.py --shell` the proof mode, the gated
> packet (double-run byte-diff CONFIRMED, the settings capture included)
> + the non-gated committed-file contract. The landing record: TASKS
> iter-217 + the worklog + git.
> **wb-3 LANDED (iter-218):** the application-operations skeleton
> (app §32 step 1) — `workbench/application/` the Python-side
> package: `identity.py` (the §9 identity closure — the five axes
> apart, sha256 content digests, the order-independent composite
> identity, `recheck()` making the mismatch law executable:
> VERIFIED | MISMATCH | INTEGRITY_UNKNOWN, never a quiet pass),
> `artifact.py` (the §10 immutable execution artifact — the frozen
> field list, the reproducibility scopes EXACT_BITWISE | SEMANTIC |
> APPROXIMATE | EXPLANATORY_ONLY + the three kinds separated, the
> request digest, the replay = NEW execution identity law, the
> strict roundtrip, zero clock imports), `directories.py` (the §16
> contract — the seven path roles, the absolute-root law, the
> startup/recovery outcome vocabulary, the errno-classifying
> probe), `clock.py` (the §17 four clock domains — MONOTONIC +
> UTC_WALL provided injectably, SEMANTIC/UI_ANIMATION named-only),
> + `__init__.py` the §27 dependency envelope (RUNTIME_DEPENDENCIES
> = empty, agreeing with pyproject). The claim packet:
> `tests/test_application_skeleton.py` (25 tests). The landing
> record: TASKS iter-218 + the worklog + git. The family contract
> below stays (wb-4..N still owner-gated rows).
> **wb-4 LANDED (iter-219, the owner's «продолжай работу» continuation
> call over the v5.2 brief):** the inbound gateway — `workbench/api/`
> the Python-side package: `contract.py` (the §8 envelopes + the
> closed vocabularies — the rejection set, the exposure axis, the
> §12.1 status→outcome mapping, the event types; the strict
> closed-document roundtrip), `gateway.py` (the SOCKET-FREE dispatch
> core: auth → idempotency → revision/lease → operation → outcome;
> the recorded-outcome replay = one effect; the §12.1 law — a
> mutating raise after admission is SENT_OUTCOME_UNKNOWN, a read
> raise RUNTIME_FAILED; the ordered per-session events + the
> RESYNC_REQUIRED law; the in-memory session-translation seed
> session.create/get/attach/detach/events + app.status; the typed
> `OperationSpec` registration surface — wb-5+'s composition point),
> `transport.py` (the loopback HTTP binding — INV-4's second
> sanctioned module, D-201: loopback hosts only, the non-loopback
> refusal executable at construction, the bounded body/drain
> ceilings) + the architecture-test exception edit (the two-module
> pin). The claim packet: `tests/test_gateway.py` (36 tests: the
> vocabulary closures, the envelope laws, the auth/idempotency/
> revision/lease laws, the dispatch-outcome mapping, the events +
> RESYNC law, the direct-vs-HTTP byte parity, the cross-seed pair,
> the boundary edges). The landing record: TASKS iter-219 + the
> worklog + git. The G1..G7 pinned decisions, verbatim, in git
> history at the iter-219 contract commit (23a3251). The family
> contract below stays (wb-5..N still owner-gated rows).
> **wb-5 LANDED (iter-220, the owner's «продолжай работу» continuation
> call over the v5.2 brief):** the minimal application operations
> (app §32 step 5) — `workbench/application/operations/` the
> Python-side package: `lifecycles.py` (§11's four closed state
> machines — Application/Backend/Model/Execution with the legal-
> transition tables, the terminal semantics = the empty successor
> set, the invalid-transition loudness; §25's FAILED_SHUTDOWN +
> the process-loss UNKNOWN branches resolved), `execution.py` (§12's
> absolute `OperationDeadline` — one per logical operation, frozen at
> admission, remaining budget the only lower-layer view; the
> cooperative `CancellationToken` + `WorkContext.check()`; the
> in-memory `ExecutionRegistry`: admit freezes the §10 inputs BEFORE
> any side effect, launch walks STARTING + spawns the daemon worker,
> the truthful terminal close — the late result lands FAILED_TO_CANCEL
> with the result recorded, the checkpoint abort CANCELED, the
> deadline/anomalous raises FAILED, `mark_unknown` the §25 surface),
> `models.py` (§20's discovery half over the §16 MODELS_ASSETS role:
> the scan with the cheap fingerprint screen, `inspect`'s fresh §9
> strong identity, `digest_work` the one real work kind — §20's
> computed-when-needed long arm with the §12 checkpoints between
> chunks), `composition.py` (§6.1's single wiring owner: the five
> registered operations run.start/get/cancel + model.list/inspect,
> the injectable work kinds; chat.send honestly NOT registered — its
> consumer is the backend row, app §32 step 7, the admission law)
> + the gateway's two targeted edits (`OperationRejected` the public
> rejection carrier — the closed vocabulary enforced at raise time;
> `OperationEffects` the session-scoped OPERATION_EFFECT surface on
> the dispatch context). The claim packet: `tests/test_operations.py`
> (46 tests). The landing record: TASKS iter-220 + the worklog +
> git. The family contract below stays (wb-7..N still owner-gated
> rows).
> **wb-6 LANDED (iter-221, the owner's «подключи llama.cpp» call —
> the backend row, app §32 step 7, the row that closes chat.send's
> admission-law deferral):** the backend family —
> `workbench/application/operations/backend.py`: the typed
> `BackendPort` (props/chat/load_model/unload_model — every member
> carrying a registered consumer; the physical owner
> `cli/engine.py`'s `LlamaServerClient` satisfies it structurally,
> NEVER imported: INV-4's two-surface form untouched, the §27
> envelope holds — the port is injected at the composition root),
> `ModelLoadStates` (§11's Model ladder walked on OBSERVED outcomes —
> the state = the fold of the backend's replies; LOADING/LOADED/
> UNLOADING transit states, never resting ones), `chat.send`
> (§19.1's REQUESTED→ACCEPTED→EFFECTIVE→OBSERVED walk over the wb-5
> run registry — identity-then-poll per §8; the caller-tunable §12
> deadline; the props probe is evidence, not a gate — the failed
> probe the honest «unavailable» note, the chat still completes),
> `model.load`/`model.unload` (§20's loading half: the discovery
> entry gate, select, the observed settle — ACTIVE on success, FAILED
> on the observed refusal with the ladder's terminal-FAILED gap
> recorded as D-203's open note, the unknown «unavailable» outcome
> resting SELECTED — §12.1's sibling, the re-load legal; the unload
> failure NO walk — the still-loaded truth) + `cli/engine.py`'s
> model-management transport half (POST /models/load + /models/unload
> — BUILD-SENSITIVE research evidence per app §20: the b11064
> station's model-management reality is the ROUTER, the dedicated
> endpoints the newer upstream line; the wire shapes stub-pinned,
> the live re-verification a station row; single-try, no ladder) +
> the composition's `backend=` wiring (the three operations
> registered ONLY when the port is injected — the admission law's
> honest form continued; a malformed port the §6.1 validate step's
> loud CompositionError). The claim packet:
> `tests/test_backend_row.py` (28 tests — the REAL adapter's port
> conformance over the live stub server among them) + test_engine's
> four management pins. The landing record: TASKS iter-221 + the
> worklog + git. The family contract below stays (wb-9..N still
> owner-gated rows).
> **wb-7 LANDED (iter-222, the owner's «продолжай работу по wb 7» +
> «могу ли я подключить llama.cpp к реготу» call — the live chat
> circuit, frontend §46 Phase A's Chat row + app §22's CLI/batch
> delivery surface):** the row that makes llama.cpp REACHABLE from
> the Redot Chat surface — `scripts/workbench_app.py` the
> composition root + loopback serve (the ONE launcher: Gateway +
> `compose_workbench_operations(backend=LlamaServerClient(
> EngineConfig(endpoint=...)))` + `LoopbackHttpTransport` on
> 127.0.0.1:8765 — the only place INV-4's two sanctioned surfaces
> meet, the port injected never imported; `--no-backend` the honest
> admission form — the three backend operations simply unregistered;
> the startup health probe evidence-not-gate — the app serves with
> the backend down, chat runs closing FAILED with the observed cause;
> the missing-models-dir loud AppError; the defaults 127.0.0.1:8765
> + llama-server's own 8080 + `workbench/runtime/models` gitignored)
> + the Redot frontend half — `presentation/redot/scripts/
> gateway_client.gd` the typed POST /op client (the sequential
> one-in-flight queue, `operation_answered`/`transport_failed`, the
> non-200 = transport-failure law, NO endpoint of its own — G8's
> executable half: the frontend dials the GATEWAY only, never
> llama.cpp) + `shell.gd`'s live circuit (the URL resolution order
> `--gateway-url` > `CANONSIM_GATEWAY_URL` > the committed project
> setting; app.status → session.create (the per-process idempotency
> key) → chat.send → the run.get poll to the truthful terminal —
> COMPLETED lands the message + the backend OBSERVED note,
> FAILED/CANCELED/FAILED_TO_CANCEL/UNKNOWN land their honest notes,
> never a fake; Stop = run.cancel; the bounded §15 message list with
> the one-shot trim note; the badge/Settings/status-bar live updates;
> the proof mode stays the STATIC deterministic form — no network in
> the capture, the wb-2 D4 law preserved) + `project.godot`'s
> `canonism_workbench/gateway/url` committed default (the launcher's
> own port). The claim packet: `tests/test_workbench_app.py` (8
> tests — the wiring law, the honest no-backend form, the loud
> arguments, the live loopback roundtrip, THE END-TO-END chat over
> HTTP against the live stub llama-server, the dead-endpoint FAILED
> close) + `test_shell_contract.py`'s three wb-7 pins. The landing
> **wb-8 LANDED (iter-223, the owner's «выбирать модель я должно из
> интерфейса» + «llama.cpp тоже запускаться при загрузке модели» +
> «настройки подтягиваться и самые нужные флаги» calls over the v5.2
> brief — frontend §46 Phase A's Models row + app §11.1's MANAGED
> half):** the row that makes the model flow a UI flow —
> `workbench/platform/llama_process.py` the process mechanics
> (§2's platform/process row: `build_server_command` the typed
> honest default flag set — `-m`/`--host`/`--port`/`-ngl`/`-c`/
> `-fa on`/`-a`/`--jinja`/`--no-webui` + the operator's extras
> verbatim, re-verified 2026-09-25 against the current llama.cpp
> server surface; `LlamaServerProcess` spawn/exit-observation/the
> §11.1 bounded graceful stop TERM→deadline→kill with the OBSERVED
> exit code; the readiness wait over an INJECTED probe — ZERO
> network imports: the engine adapter stays the one outbound
> surface) + `scripts/workbench_app.py`'s `--managed` form (§11.1's
> lifecycle policy at the composition root: `_ManagedBackend` the
> port-face wrapper — a HEALTHY server delegates unchanged (the
> ATTACHED behaviour preserved), `model.load` on a DOWN server
> spawns llama-server WITH the caller's model (prepare → validate →
> ready through the adapter's own health probe), the spawned
> model's unload STOPS the process, Ctrl+C stops only OUR process;
> the spawn/ready failure surfaces the honest 'unavailable' cause —
> §12.1's sibling, the model rests SELECTED, the deliberate re-load
> legal; `--llama-server-exe/--llama-ctx/--llama-ngl/--llama-args`
> the operator's override surface; the managed ABSENT/LIVE evidence
> line) + `backend.py`'s `model.states` READ operation (the
> load-state read surface's registered consumer) + the Redot half —
> `shell.gd`'s Models surface (the discovered list over `model.list`
> + the per-model lifecycle states over `model.states`, Load/Unload
> over `model.load`/`model.unload` with the honest minutes-class
> per-call timeout (`gateway_client.gd`'s `timeout_s` envelope),
> the truthful UNKNOWN/refusal/transport notes, FAILED terminal
> shown never hidden — D-203's gap; the owner-reported launcher
> warnings fixed — `_tag`/`_body`, the hygiene pinned in the
> contract test). The claim packet: `tests/test_managed_backend.py`
> (17 tests — the flag set, the process mechanics, the lifecycle
> policy incl. THE REAL SPAWN over the stand-in server
> `tests/_managed_fake_server.py`, the honest unavailable causes,
> the launcher wiring + precedence) + `test_shell_contract.py`'s
> three wb-8 pins. The landing record: TASKS iter-223 + the worklog
> + git. The family contract below stays (wb-9..N still
> owner-gated rows).

> **wb-9 LANDED (iter-226, the owner's 2026-09-26 «открыл воркбенч,
> зашел и загрузил модель» + «подтянуть модель откуда угодно» +
> «настройки запуска llama.cpp... сэмплеры всякие» calls — the
> model-flow row, frontend §46 Phase A's Models/Settings real-surface
> half + app §11.1's managed default + §20's arrival half):** the row
> that makes the model flow a ONE-COMMAND experience —
> `workbench/platform/model_fetch.py` (D-208, INV-4's THIRD sanctioned
> network surface, the owner-gated outbound model-assets fetch: the
> operator URL vocabulary direct/HF-resolve/HF-blob→resolve/
> hf:namespace/name/file → the `.part` stream with the injected §12
> checkpoint (the caller's WorkCancelled/DeadlineExceeded carriers
> propagate untouched) → the atomic rename into the models root; the
> D1-family failure vocabulary; HTTP GET ONLY) + the `model.fetch`
> work kind (models.py over the INJECTED fetcher — the BackendPort
> pattern: the admission gates BEFORE the run exists (the occupied
> name, the `.part` residue, the non-plain name — NOT_SENT), the run
> registry's live PROGRESS surface (WorkContext.progress → the
> run.get document, JSON-safe-gated), the kind's own 3600s default
> deadline — the WorkKind field, chat.send's own-deadline pattern) +
> `workbench/application/settings.py` (the typed LaunchSettings
> document — exe/context/ngl/fa/jinja/no-webui/temp/top-k/top-p/
> min-p/repeat-penalty/extra_args over the closed validated set, loud
> never clamped; the atomic schema-tagged persistence at
> workbench/runtime/settings.json — §16's USER_CONFIG role; the loud
> load; the backend.settings / backend.settings.update operations with
> the command preview + the managed liveness INJECTED at the
> composition root; chat.send's absent-temperature default resolves
> from the store — §19.1's BASE layer, the explicit value still wins) +
> `llama_process.py`'s sampler default flags (--temp/--top-k/--top-p/
> --min-p/--repeat-penalty, each emitted EXPLICITLY — the `-fa on`
> pinning law) + `workbench_app.py`'s MANAGED DEFAULT (the
> owner's model-flow call as THE default ownership form; `--attached`
> restores wb-8's observe-only form; the settings load + the
> CLI-over-store per-field overrides read at each spawn — a UI update
> applies at the NEXT spawn; the exe auto-discovery: CLI > the store's
> preference > the runtime/llama.cpp scan > PATH; the DEFAULT models
> dir auto-creates — a custom missing dir stays the loud typo guard) +
> `scripts/workbench_launch.py` the ONE-COMMAND launcher (the runtime
> bootstrap workbench/runtime/{models,llama.cpp}/; the gateway child's
> stdout bind-line watch — the readiness evidence without a
> launcher-side socket; the Redot child after the bind (REDOT_EXE the
> convention); either exit or Ctrl+C stops both, the gateway first so
> the managed llama-server rides its own graceful path) + the Redot
> half — shell.gd's Settings surface goes REAL (the typed launch
> fields + the collapsed advanced extras + the command preview + the
> honest next-spawn/LIVE note, backend.settings over the gateway) and
> the Models surface gains the MANAGER (the URL row — a direct link, a
> huggingface.co page, or hf:repo/file; Fetch/Cancel over
> run.start/run.cancel; the distinct fetch-get poll tag with the live
> progress note; the honest terminal notes; the offline hints name
> workbench_launch.py). The claim packet: tests/test_model_fetch.py
> (11 — the URL vocabulary, the admission gates, THE REAL end-to-end
> fetch against a live loopback HTTP file server, the live progress,
> the 404/cancellation truth, the .part cleanup) + tests/
> test_settings.py (10 — the store laws, the loud load, the
> operations over the gateway incl. the SETTINGS_UPDATED effect) + the
> workbench_app/managed/shell_contract/architecture/operations/
> gateway pin updates (35 new tests total). The landing record: TASKS
> iter-226 + the worklog + git. The family contract below stays
> (wb-10..N still owner-gated rows).

> **wb-10 LANDED (iter-227, the owner's 2026-09-25 fix list over the
> wb-9 handback — the launcher's Popen `buffering` TypeError + «где
> найти redot.exe и как его подключить?» + «просто открывающийся
> проводник и выбор уже скаченных локальных моделей» +
> «пользователь не должен вводить команды чтобы запустить или скачать
> что-либо!» + «интерфейс вверх убожества»):** the ZERO-COMMAND owner
> experience — `scripts/workbench_launch.py` reworked (the bufsize
> fix; the FOLDER-AWARE Redot resolution: a release folder scans for
> the engine executable — the known names in preference order
> (redot.windows.editor.x86_64.exe first, the owner's exact binary),
> then the sorted redot* glob, root + one folder deep; the chain:
> --redot-exe (exe or folder) > the persisted
> workbench/runtime/launcher.json pick > REDOT_EXE > the
> Desktop-shaped common-roots auto-scan > the native tk folder picker
> ONCE (the pick persists); the explicit CLI/env forms pass verbatim
> (strict — the spawn's own loud error), the persisted pick recovers
> when stale; the OBSERVED bind URL is forwarded to the Redot child as
> --gateway-url — the shell dials the gateway the launcher actually
> started; the bare "--" separator stripped before the child's parser
> — the latent wb-9 gateway-arg bug) + the `model.import` WORK KIND
> (models.py: a LOCAL copy into the models root — one or more
> absolute paths, the same admission gates as the fetch (exists,
> plain name, unoccupied, no .part residue, no duplicates — NOT_SENT),
> the .part stream + the atomic rename, the per-file live progress
> (logical_name/file_index/file_count/copied_bytes/total_bytes) + the
> cooperative §12 checkpoint per chunk, the best-effort .part cleanup
> on every failure path; NO network anywhere — INV-4 untouched, wired
> into the default composition unconditionally) + `discover()`'s
> `models_root` (the frontend's open-folder answer, never a local
> guess) + the Redot half — shell.gd's native-picker Models manager
> (Add local models… = the OS file dialog multiselect with the .gguf
> filter over FileDialog.use_native_dialog + ACCESS_FILESYSTEM; Add
> folder… = the OS folder dialog, the .gguf files enumerated
> presentation-locally; Open models folder = OS.shell_open on the
> gateway's own models_root; the URL fetch demoted to the collapsed
> advanced row, fully functional) + the theme@0.2 visual pass (the
> warmer surface ramp, the pill chip, the user-card accent edge, the
> taller nav) + `Workbench.bat` / `Workbench Setup.bat` the repo-root
> double-click entries (the python/py resolution + the honest pause
> on failure) + project.godot 1440×900. The claim packet:
> tests/test_model_import.py (8 — the admission gates, THE REAL
> end-to-end local copy with the independent sha256 oracle, the
> multi-file form, the models_root field, the kind's checkpoint/
> progress/cancellation laws) + tests/test_workbench_launch.py (12 —
> THE REAL SPAWN integration: the launcher process starts the real
> gateway, observes the bind line, and stops both on SIGINT — the
> buffering crash pinned dead; the folder resolution; the auto-scan;
> the persisted pick; the bind-URL parse) + the pin updates
> (test_shell_contract +3 — the import surface, the zero-command
> entries, the theme tokens; test_workbench_app's resolution +
> passthrough; test_operations' work_kinds/models_root). The landing
> record: TASKS iter-227 + the worklog + git. The family contract
> below stays (wb-11..N still owner-gated rows).

> **wb-11 LANDED (iter-228, the owner's 2026-09-26 report over the
> wb-10 handback — «молча висят + транспорт результ 13» + «модель
> выбрать не могу, там пусто, моделей не видно, кнопка выбрать модель
> не работает (проводник не открывается)» + the evidence «llama.cpp и
> модели запускаются штатно если отдельно запускать»):** the
> transport-13 freeze chain pinned dead — the DIAGNOSIS: a
> minutes-class managed model.load ran its spawn+readiness walk
> INSIDE the gateway's coarse dispatch lock (gateway.py's one lock
> around the whole pipeline), starving every concurrent request
> (model.list, session.create, app.status) past the client's 10s
> budget → HTTPRequest RESULT_TIMEOUT (13) on everything → the empty
> Models list + the dead session-gated buttons; the client's
> sequential one-request queue wedged behind the long call too; the
> undrained Windows PIPEs could wedge the managed server mid-load;
> the `os.set_blocking` stderr_tail raised on Windows — the failure
> cause showed '(empty)'. THE FIX: `model.load`/`model.unload` become
> RUNS (app §8's own law, the chat.send pattern — **the wire shape
> change: both now return the execution document
> {execution_id, state: "STARTING", work, deadline_seconds}, the
> terminal truth rides run.get, the FAILED diagnostics carry the
> observed cause**; the single-slot + in-flight admission guards;
> MODEL_LOAD/UNLOAD_DEFAULT_DEADLINE_SECONDS 330/30 the rows' own §12
> budgets) + `llama_process.py`'s `_PipeDrain` (one daemon reader per
> captured pipe into a bounded 64KB tail ring — the pipe never fills,
> stderr_tail cross-platform over the ring) + shell.gd's run-poll
> Models circuits (model-load-get/model-unload-get on the shared
> tick; the honest picker/load guards — never a silent return, §18;
> the failed scan re-arms so the empty list never sticks). The claim
> packet: test_backend_row's run-form rework + 3 new pins incl. THE
> DISPATCH-LOCK regression (model.list ANSWERS while a gated load
> stands in the port call) + test_shell_contract's wb-11 pins. The
> landing record: TASKS iter-228 + D-210 + the worklog + git. The
> family contract below stays (wb-12..N still owner-gated rows).

> **wb-12 LANDED (iter-230, the owner's 2026-09-25 «тема и UI все так же
> убоги, тема ужасная» + «в чате при получении сообщений от языковой
> модели => не происходит плавной прокрутки вниз» calls over the v5.2
> plans pack — VISUAL_SYSTEM_UI §10's queue head, D-211's law + D-212
> the landing):** theme@0.3 — the token audit per the law's §2/§3: the
> neutral ramp re-pinned over the Catppuccin Mocha VALUE reference
> (§6's transplantation protocol applied to values — the MECHANISM
> taken is the tuned layered luminance separation, the provenance
> noted in the theme header; no assets, no code), exactly ONE accent
> (the soft blue #89b4fa family: accent/accent_soft/focus_ring — the
> old warm-orange family and its brown-tinted pressed/selected
> surfaces retired, accent_deep RETIRED as token-without-consumer),
> the NavButton type variation (the rail's quiet navigation set —
> every value in the theme, the code names the type only) + the
> styles/chip_busy token; ON THE SAME ROW the owner's named chat
> blocker: the follow law in shell.gd (`_scroll_to_bottom_smooth` —
> the smooth tween over the scrollbar's float value, never the integer
> `scroll_vertical` jump; `await get_tree().process_frame` before the
> target is read — the autowrapped labels size late, the old
> call_deferred read was the short-scroll bug; the near-bottom gate
> (SCROLL_FOLLOW_SLOP_PX) so a reader deep in history is never yanked;
> the follow fires for EVERY role incl. the user's own send; the
> bounded late-layout re-settle) + the GENERATING chip (§5's Chat
> matrix state made visible: a pulsing accent dot AND a text label —
> §4's not-color-only law, wired into `_set_busy` the single busy
> owner). The claim packet: test_shell_contract's theme@0.3 pins
> (the NavButton state set, chip_busy, the accent_deep-retirement
> regression) + THE SMOOTH-FOLLOW pins (the tween recipe, the
> layout-settle await, the near-bottom gate, the retired integer
> jump, the every-role follow, the busy-chip carriers). The landing
> record: TASKS iter-230 + D-212 + the worklog + git. The family
> contract below stays (wb-13..N still owner-gated rows).

**Pinned decisions** (each grounded in the brief or standing law):

- D1 Runtime: Redot 26.2 LTS (`redot-26.2-stable`), Compatibility
  renderer, GDScript. The engine binary + export templates are an
  EXTERNAL toolchain (never committed); one configurable `REDOT_EXE`
  path is the single resolution point (the brief's integration §7).
  Redot project root: `workbench/presentation/redot/`; committed:
  project.godot, scenes, scripts, themes, source assets; ignored:
  `.godot/`.
- D2 Boundary: Redot owns presentation-local state only (camera,
  selection, animation playback, transient effects, caches) — never
  canonical world state, event history, semantic time, identity or
  simulation rules. The chain is
  `fixture → typed read model → Visual Scene IR → Redot composition →
  screenshot artifact`; the IR is renderer-neutral (no Node/Texture/
  UID as identity) with the v5.2 identity closure
  (`scene_ir_schema_identity + composition_seed + asset_manifest_
  identity + semantic_input_identity + composition_policy_version`).
- D3 Python side: `workbench/` is periphery (the render/cli/scripts
  class, D-046 — outside the INV-3 stoplist by the same law: entity
  ids and location ids arrive as data from the log/pack, never
  hardcoded). It imports `core/` read-side APIs only (read_log, fold,
  present_in_order — the render/chronicle.py pattern); zero canon
  writes, zero new network surfaces (INV-4 untouched: `cli/engine.py`
  stays the only network module; the future inbound gateway is an
  owner-gated row with its own contract + architecture-test exception
  when it fires).
- D4 Determinism: same semantic input + same seed → byte-identical IR
  JSON; two consecutive Redot runs in the same environment →
  byte-identical PNG (measured in-sandbox before this contract:
  llvmpipe/Xvfb, 1280x720). No wall clock, no PYTHONHASHSEED
  dependence (sha256 stable hashes + sorted/construction order — the
  INV-2 read-side discipline; no RNG draws at all in the Python half).
- D5 Status laws: the IR distinguishes
  CANONICAL | DERIVED | OBSERVED | UNKNOWN | HIDDEN | VISUAL; the
  silent collapses UNKNOWN→ABSENT, HIDDEN→ABSENT, VISUAL→CANONICAL,
  LLM-text→CANONICAL are forbidden (the brief's §7/§23 vocabulary).
- D6 Observation: the proof's artifacts (PNG + metadata JSON) are
  runtime output — gitignored, never committed; the pytest regenerates
  and compares in-run (the iter-207/209 byte-identical-on-regeneration
  pattern). Tests skip cleanly without `REDOT_EXE` (the duckdb/D-093
  pattern; CI stays engine-free).

**Invariant set**: INV-1..INV-5 all hold unmodified; the seam adds no
second semantic authority, no second fold, no second presence rule
(`present_in_order` is the one presence law, reused).

**Falsifier** (TEST_PLAN §9's packet form): any byte difference in the
IR JSON on rebuild from the same fixture; any byte difference between
two consecutive screenshot runs in one environment; any network import
or canon write in the new modules (test_architecture); any setting
word hardcoded in `workbench/` source (review — the stoplist does not
scan periphery, the discipline is the review's).

**Minimal test set**: `tests/test_scene_ir.py` (determinism + status
laws + identity closure over the tavern and province smoke fixtures);
`tests/test_visual_proof.py` (REDOT_EXE-gated: the artifact exists,
metadata carries the identity fields, the double-run PNG byte-diff).

**Family composition** (TASKS owns WHAT/WHEN; the brief's own order,
owner-gated per row): wb-1 the vertical seam (this contract's first
consumer); wb-2 the Redot shell + theme; wb-3 the application
operations skeleton; wb-4 the gateway (INV-4's owner-gated exception);
wb-5 the minimal application operations (app §32 step 5 — the
operations substrate + the run/model-discovery families over the
registered surface); wb-6 the backend row (the llama.cpp port —
chat.send's consumer, D-203); wb-7 the live chat circuit (D-204);
wb-8 the managed models surface (app §11.1's MANAGED half + the
Models surface — D-205); wb-9+ per the brief's §32/§46 ladders
(live events + reconnect/resync; persistence; the frontend rows —
inference; history/diagnostics; the CanonSim seam). Every wb row's
engine/API facts route through `docs/REDOT_ENGINE_INDEX.md` (the
Redot 26.2 version firewall + the class/networking/performance/
debugging reference map — read before the row starts; admitted
iter-225, D-207).
