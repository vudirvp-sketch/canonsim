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
  wb-7+ per the brief's §32/§46 ladders (live events +
  reconnect/resync + the idempotency/revision/lease tests at live
  scale; persistence; the frontend rows — chat, models, inference,
  history, diagnostics, the CanonSim seam, asset vocabulary, the
  G1–G12 gates). Never speculative — a row opens only when the
  owner names it.

### Iteration ledger (one line per iteration; the tail capped at 10 by the doc guard — older lines live in git; per-iteration detail: the D-rows + the owning docs + worklog + git, never restated here, the header's own law)

- iter-221 · 2026-09-24 · wb-6-backend (the owner's «подключи llama.cpp» call over the v5.2 brief — the row that closes chat.send's admission-law deferral, app §32 step 7): the backend family LANDED — workbench/application/operations/backend.py (the typed BackendPort — props/chat/load_model/unload_model, the §6.1 validate step loud on a malformed port; ModelLoadStates the Model-ladder state owner walked on OBSERVED outcomes — LOADING/LOADED/UNLOADING transit states, ACTIVE/EVICTED/FAILED/SELECTED the resting truths; chat_completion_work the §19.1 EFFECTIVE→OBSERVED half — the props probe never kills the chat, the identity lands the honest «unavailable» note; the handlers: chat.send the identity-then-poll admission over the wb-5 run registry with the caller-tunable §12 deadline, model.load the discovery gate + select + the observed settle (the unknown outcome rests SELECTED — §12.1's sibling), model.unload the ACTIVE gate + the observed eviction, a failure NO walk — the still-loaded truth) + cli/engine.py's model-management half (load_model/unload_model the POST /models/load|unload transport — build-sensitive research evidence, single-try no-ladder, the wire shapes stub-pinned; chat's grammar default None — the port conformance) + composition.py's backend= wiring (register_backend_operations: the three operations only when the port is injected — the admission law's honest form continued; WorkbenchOperations.model_loads the state handle) + the __init__ envelope note + tests/test_backend_row.py (28 tests: the REAL adapter's port conformance over the live stub server, the §19.1 layer walk, the defaults/ranges validation, the backend-failure run close, the failed-probe resilience, the cancellation trio CANCELED/FAILED_TO_CANCEL, the deadline terminal, the session ownership, the effects stream, the load/unload walks + the terminal-FAILED gap + the unknown-outcome re-load + the re-selection, the composition closures, the parity, the byte-deterministic pair, the cross-seed pair, the import closure) + test_engine.py's four management pins (the wire shapes, the error mapping, the no-ladder law, the grammar-default) + test_operations.py's envelope extension (backend in the allowed set); 11 paths; 2191+6 + ruff + docguard clean (zero core change, zero pack change, the LOG untouched, INV-4's two-surface form unchanged — the port injected, never imported; D-203 the landing)
- iter-220 · 2026-09-24 · wb-5-operations (the owner's «продолжай работу» continuation call over the v5.2 brief, the family's fifth row, app §32 step 5): the minimal application operations LANDED under workbench/application/operations/ — lifecycles.py (§11's four closed state machines: the legal-transition tables, the terminal semantics = the empty successor set, the invalid-transition loudness; §25's FAILED_SHUTDOWN + the process-loss UNKNOWN branches resolved), execution.py (§12's absolute OperationDeadline frozen at admission — remaining budget the only lower-layer view, the tries×timeout law structural: no extension API exists; the cooperative CancellationToken + WorkContext.check(); the in-memory ExecutionRegistry — admit freezes the §10 inputs BEFORE any side effect, launch walks STARTING + spawns the daemon worker, the truthful terminal close: the late result FAILED_TO_CANCEL with the result recorded, the checkpoint abort CANCELED, the deadline/raise FAILED, mark_unknown the §25 surface; the session-ownership guard; the §26 deadline ceilings), models.py (§20's discovery half over the §16 MODELS_ASSETS role: the scan + the cheap-fingerprint screen, inspect's fresh §9 strong identity — never a cached correctness identity, digest_work the one real work kind — the chunked sha256 with the §12 checkpoints), composition.py (§6.1's single wiring owner: the five registered operations run.start/get/cancel + model.list/inspect, the injectable work kinds, chat.send honestly NOT registered — the backend row's consumer per the admission law) + gateway.py's two targeted edits (OperationRejected the public rejection carrier — the closed vocabulary enforced at raise time, riding the same NOT_SENT pipeline path; OperationEffects the session-scoped OPERATION_EFFECT surface on OperationContext — the wb-4 composition point's designed growth) + pyproject (workbench.application.operations) + tests/test_operations.py (46 tests: the vocabulary closures + the ladder walks + the invalid-transition falsifiers; the deadline arithmetic + the checkpoint laws; the artifact-before-side-effects proof observed from inside the work; the immediate-identity return; the truthful cancellation trio; the spawn-failure SENT_OUTCOME_UNKNOWN integration with the registry's own FAILED truth; the idempotent replay over runs; the §9 identity laws with the independent sha256 oracle; the §16 MISSING/CORRUPT slot vocabulary; the composition closure + the duplicate loudness; the direct-vs-HTTP byte parity over the new surface; the byte-deterministic pair; the cross-PYTHONHASHSEED subprocess pair; the AST import-closure scan); 15 paths; 2159+6 + ruff + docguard clean (zero core change, zero pack change, the LOG untouched, INV-4's two-surface form unchanged)

- iter-219 · 2026-09-24 · wb-4-gateway (the owner's «продолжай работу» continuation call over the v5.2 brief, the family's fourth row, app §32 step 4's second half — INV-4's owner-gated exception): the inbound gateway LANDED under workbench/api/ — the contract written FIRST (the G1..G7 block at commit 23a3251, collapsed to the pointer per the file's law) — contract.py (the §8 envelopes + the closed vocabularies: the 8-member rejection set, the exposure axis, the §12.1 status→outcome mapping, the event types; the strict closed-document roundtrip, JSON-safety loud), gateway.py (the SOCKET-FREE dispatch core: auth (constant-time, scope-checked) → idempotency (the recorded-outcome replay = one effect; DUPLICATE_REQUEST the conflicting reuse) → revision/lease guards (STALE_REVISION, LEASE_EXPIRED on the monotonic window) → operation → outcome (a mutating raise after admission = SENT_OUTCOME_UNKNOWN recorded so the blind retry is blocked; a read raise = RUNTIME_FAILED); the ordered per-session events (§8's envelope, no clock in identity, bounded retention) + session.events' replay-or-RESYNC_REQUIRED law; the in-memory session-translation seed session.create/get/attach/detach/events + app.status; the typed OperationSpec registration surface — wb-5+'s composition point), transport.py (the loopback HTTP binding — INV-4's second sanctioned module per D-201: loopback hosts only, the non-loopback refusal executable at construction, the bounded body/drain ceilings, canonical-JSON responses) + tests/test_architecture.py (NETWORK_EXCEPTIONS = the two modules, D-201) + tests/test_gateway.py (36 tests: the vocabulary closures, the envelope laws, the auth/idempotency/revision/lease laws, the dispatch-outcome mapping, the events + RESYNC law, the direct-vs-HTTP byte parity, the cross-PYTHONHASHSEED pair, the boundary edges) + AGENTS.md §4/§8 (INV-4's two-surface rewording) + pyproject (workbench.api); 13 paths; 2113+6 + ruff + docguard clean (zero Redot need in this row)

- iter-218 · 2026-09-24 · wb-3-skeleton (the owner's «продолжай работу» continuation call over the v5.2 brief, the family's third row, app §32 step 1): the application-operations skeleton LANDED under workbench/application/ — identity.py (§9: the five identity axes apart, sha256 content digests, the order-independent composite, recheck() VERIFIED/MISMATCH/INTEGRITY_UNKNOWN never silent), artifact.py (§10: the frozen field list, the closed reproducibility scopes + kinds, request_digest, replay = a NEW execution identity, strict roundtrip, zero clock imports), directories.py (§16: seven path roles, the absolute-root/.git-CWD-independence law, the closed startup/recovery vocabulary, the errno probe), clock.py (§17: four domains, MONOTONIC+UTC_WALL injectable, SEMANTIC/UI_ANIMATION named-only) + __init__.py the §27 envelope (empty, agreeing with pyproject) + tests/test_application_skeleton.py (25 tests: determinism incl. a cross-PYTHONHASHSEED subprocess pair, the mismatch laws, CWD-independence via chdir, injected clock doubles, the pyproject agreement); 12 paths; 2077+6 + ruff + docguard clean (the 5 REDOT_EXE-gated visual packets skipping clean per D6 — the sandbox binary absent, zero Redot need in this row)

- iter-217 · 2026-09-24 · wb-2-shell (the owner's «продолжай работу» call over the v5.2 brief, the family's second row): the Redot shell + custom theme LANDED — themes/workbench_theme.tres (the §10 token ladder: the Workbench/* semantic namespace — colours/type roles/spacings/chrome styleboxes — + the styled component types with their state sets, the §12 contrast pairs recorded in-file), scenes/shell.tscn + scripts/shell.gd (the code-built shell: the §17 nav axes with Chat/Settings live + the later axes honestly disabled, the placeholder surfaces, the §16 status strip, the §18 backend badge, the §13 focus ownership), project.godot main scene -> the shell (the app-entry law; the seam scene now explicit in the runner), scripts/visual_proof.py the --shell proof mode (+ --surface), tests/test_shell_proof.py (REDOT_EXE-gated: double-run byte-diff CONFIRMED + the settings capture) + tests/test_shell_contract.py (non-gated committed-file contract); 13 paths; 2057+1 + ruff + docguard clean

- iter-216 · 2026-09-24 · wb-1-redot (the seam's Redot half, the owner's step-by-step directive): the pinned Redot 26.2 LTS project landed at workbench/presentation/redot/ (gl_compatibility, the code-built placeholder compositor over the IR — ColorRects + provenance/status labels + the debug overlay, screenshot + metadata artifacts, user args, exit codes) + scripts/visual_proof.py the REDOT_EXE operator runner (one toolchain path, a private Xvfb when no display, absolute artifact paths) + tests/test_visual_proof.py (REDOT_EXE-gated, the D-093 skip pattern; the double-run PNG byte-diff the D4 falsifier CONFIRMED; tavern + province fixtures both green live); 9 paths; 2051+1 + ruff + docguard clean

- iter-215 · 2026-09-24 · wb-1-python (the Workbench family's opening, the owner's «начать разработку» call over the v5.2 Redot brief — this ledger line landed one iteration late, the iter-216 sync, noted): CONTRACTS §5 the family contract (D1–D6) + the TASKS wb rows + D-200 in the landings family + NAV/README/.gitignore/pyproject sync; the Python seam half — workbench/scene_ir.py (the typed renderer-neutral IR: the v5.2 identity closure, the closed status enum, byte-deterministic serialization) + workbench/scene_build.py (read_log → fold → present_in_order → IR, stable-hash placement, zero RNG) + tests/test_scene_ir.py (8 tests: byte-identical rebuild, the truncated-log identity discriminant, cross-PYTHONHASHSEED subprocess pair, status laws, strict roundtrip); 14 paths; 2049+1 + ruff + docguard clean

- iter-214 · 2026-09-24 · doc-7 (intake-38 — the cross-domain principle document routed, the owner's «сажай intake-38» call): the 552-line doctrine verified against HEAD ff9ccbb before routing (D-024) — CONFIRMED-owned, the standing discipline's own live form (§18's five-part test = BLUEPRINT §2 L15 verbatim; §19 = AGENTS §2.8; §20 = the binding do-not-import list; §21 the same owners named); the §8/§9 method families landed or parked through intakes 34..37 (ablation/empty-ablation, the mutation probe, CEGAR→mech-2, delta-debug PROPOSED, sham HYPOTHESIS, CRN CONFIRMED); the fresh residue parked per D-175, ZERO new rows — held-out transfer (HYPOTHESIS, engine-1's {3–8B} corpus the named first consumer), the experiment-contract fields stopping-rule/spillover/blocked-nuisance (PROPOSAL/UNRESOLVED beside the deletion criterion), evidence-independence + metric anti-Goodhart (each behind its first consumer), §12's residual relation-lens as consult vocabulary; a second agent's independent 20-file corpus pass recorded as the corroboration (intake-35's precedent, its ADOPT list predating the intake-34..37 absorption); D-199 rides the intake family row; 5 paths doc-only (phases/DECISIONS/TASKS/STATUS/worklog; the D-022 exception honest: the owner's fresh intake request)

- iter-213 · 2026-09-24 · doc-6 (the CP-migration family's acceptance, the owner's continuation call over STATUS Next step 1): the family CLOSED — doc-4 (iter-211: the external CP document's durable layer → AGENTS §2/§10/§11/§12 + NAV §2, D-113's chat-side placement superseded), doc-5 (iter-212: TEST_PLAN §9's claim-side epistemic classes + BLUEPRINT §2 L15), doc-6 (this line) the acceptance collapse — the D-198 row's family-closed marker landed, the ledger/state docs at the minimal current-state form; the minimal-invocation artifact delivered CHAT-SIDE (never a repo file — the convenience-copy law): the repository + task-words form, the big bootstrap prompts retired; 4 paths doc-only (the state docs; the D-022 exception: the owner's fresh continuation request)

- iter-212 · 2026-09-24 · doc-5 (the research-discipline vocabulary into its owners, the CP-migration family's second slice, the owner's continuation call over STATUS Next step 1): the claim-side epistemic classes FACT (directly established by evidence) / INFERENCE (a reasoned conclusion from evidence) / HYPOTHESIS (plausible, unverified) / PROPOSAL (a possible future direction) / UNKNOWN (not presently decidable) named in TEST_PLAN §9 beside the standing disposition vocabulary — class and disposition separate axes (the claim's kind as asserted vs the verification's verdict), the class gating what a disposition may license (hypothesis → requirement, proposal → architecture, research → implementation, plausibility → proof the forbidden transitions; a surviving HYPOTHESIS/PROPOSAL routes to an owner-gated row, never into a build); the five-part design test (Principle / Form / Quality / Transfer / Combined design) landed as BLUEPRINT §2 L15 beside L13/L14 — form-match alone never enough (an existing form with quality/transfer/combined-design unproven caps the strongest disposition at PARTIALLY CONFIRMED), applied at a genuine design fork only, never a ritual; TEST_PLAN §9's lens quality-bar sentence re-pointed at L15 (the single owner, D-024); the D-198 row's doc-5 clause closed; 6 paths doc-only (the two owner docs + the state docs; the D-022 exception: the owner's fresh continuation request)


