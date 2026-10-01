Iteration: iter-295 (`observatory` — Phase 3's SECOND ROW, the
  owner's «продолжай работы по фронтенду, над теми частями что
  логичнее всего сейчас провести» repeated delegated call; R2
  frontend-local): the OBSERVATORY ENTRY landed over the EXISTING
  observatory.runs/observatory.read READ ops (zero new routes,
  zero Python change) — the dual-read law §4's missing HISTORY
  half: the contract mirror (contracts/validators/client — the
  runs/window/row types, the CANON_VIEW/CANONICAL vocabularies,
  strict zod with recursive-JSON from/to and KEY PRESENCE
  enforced), `features/observatory/{useObservatory,Observatory}`
  the HISTORY surface (the discovery scan with the per-run honest
  degradation pair; ONE bounded window at a time — the event-id
  cursor, next_after forward pagination that REPLACES the window,
  never an accumulating buffer; the context strip's identity line
  run/seed/pack/profile/authority/total; NO DATA ≠ NO MATCH ≠
  stale-cursor ≠ TRANSPORT ≠ MISMATCH rendered distinct; G4 — the
  re-read from the head the user's explicit decision; no polling:
  durable evidence, every read explicit; the violet HISTORY
  channel distinct from the LIVE teal); the root mounts the fifth
  pane (the Trajectory/Observatory dual-read pair); 6 live-captured
  fixtures (the CLI-generated run run_125_0, 56 events) + 8
  integration + 11 contract rows; the LIVE smoke 8/8 against the
  real app gateway (the listing, the head window 50/56
  next_after=ev_0049, the forward window to the end, limit
  honored, NO MATCH verbatim, stale cursor verbatim, the closed
  argument set); the RU report at
  docs/iterations/iter-295-frontendweb-report.md

Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
  the ladder complete 0..6 — the standing work: the owner-gated
  backlog + the web-frontend track + the world track + the SoW
  horizon, ROADMAP §2/§6) ·
2529 passed + 1 skipped, ruff clean, docguard clean, topology
  --check clean (Python 3.12.14, the env pin; zero Python change
  this iteration — the frontend stack: 78 vitest + tsc + build)
  ·
Date: 2026-09-29 ·
Scope: frontend/src/api/gateway/{contracts.ts, validators.ts,
  client.ts} (the observatory contract mirror),
  frontend/src/features/observatory/{useObservatory.ts,
  Observatory.tsx} (new), frontend/src/app/composition/{App.tsx,
  styles.css} (the fifth pane), frontend/tests/fixtures/
  {observatory_runs_ok, observatory_read_ok,
  observatory_read_tail, observatory_read_no_match,
  observatory_read_stale_cursor,
  observatory_read_unknown_argument}.json (new, live-captured) +
  manifest.json, frontend/tests/contract/validators.test.ts,
  frontend/tests/integration/Observatory.test.tsx (new),
  frontend/README.md, docs/frontendweb/
  FRONTEND_WEB_AGENT_CONTEXT.md (the stage map), docs/TASKS.md
  (the ledger, iter-285 evicted), STATUS.md (the header),
  worklog.md (iter-285 evicted),
  docs/iterations/iter-295-frontendweb-report.md (new) — 15
  changed/created (R2 — frontend-local; zero Python change, zero
  canon change, the LOG untouched, zero corpus price)
Track A: the web-frontend track — S0 LANDED; the tooling floor's
  first row LANDED (iter-293); Phase 3's first TWO rows LANDED
  (iter-294 the shell + the session lifecycle; iter-295 the
  Observatory HISTORY entry — the dual-read law's second world);
  the remaining Phase 3 surfaces (Chat/Inference, Settings) NOT
  backend-blocked — their ops already live at the app gateway (the
  iter-294 smoke's enumeration), each its own contract-mirror +
  surface iteration; the standing boundaries: SSE/WebSocket,
  Tauri, PWA — each its own admission. The world track: W8's
  remaining rows the owner's call. The ssi family COMPLETE except
  ssi-5, owner-gated.


## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index; the log writer is the
  only canon-write path (D-031).
- INV-2 Determinism: single point of randomness control — one master seed;
  named streams derived via the RngBank (`stable_hash` = sha256-based);
  no wall-clock; `sorted()` iteration; fixed `PYTHONHASHSEED`; queue key
  `(tick, sub_order, actor_id)`; cosmetic draws never desync canon replay
  (D-028 — AGENTS.md §4 is the single reading owner).
- INV-3 Content/code split: no domain words in engine code (`core/` +
  `sim/` + `brief/` — the mediator circuit joined the stoplist at
  iter-10a); all setting data in `content/tavern_pack/`; the periphery
  dirs (`render/`, `cli/`, `scripts/`) carry pack paths/help text/prose
  by design (D-046).
- INV-4 LLM boundary — the sanctioned surfaces: the network surface is
  EXACTLY THREE modules — `cli/engine.py` (outbound engine wire, D-193),
  `workbench/api/transport.py` (inbound loopback gateway, D-201), and
  `workbench/platform/model_fetch.py` (outbound model-assets fetch, D-208);
  everything else stays network-free and engine-agnostic — AGENTS §4
  the law owner, the architecture test the executable.
- INV-5 Log immutability: committed logs are never edited; corrections are
  new events.

## Active KIs

- KI#109 · the GitHub mirror at HEAD `6c614ce` carries iter-291..293's docs WITHOUT the 16 recorded D-245 deletions (a fresh clone: docguard red on the 1462-line index + the stale shell-contract red; the owner's local tree has them — the mirror never received the deletions in any commit) · 2026-09-29 · CLOSED iter-294 (the 16 paths re-executed in the sandbox, the suite 2529+1 again; the delta carries them in DELETED_PATHS, the owner-side git block lists them for the mirror)

## FAQ / Pitfalls

> One-liners + the owner link (NAV §3's duplication rule); the essays
> restated their named owners (doc-3). The operational recipes live in
> TECH_NOTES §14 (live-session) + §15 (corpus-regen).

- **Read-side folds (echo/traits) never feed entropy/channel inputs (L6/EPIST-1, iter-46/55); the intent door is the only legal path** — DIRECTOR_SPEC §4; the one legal render: BRIEF_SPEC §3.5.
- **Every visual/UI row routes through docs/VISUAL_SYSTEM_UI.md FIRST (the surface-driven grammar, the token taxonomy, the state matrix, the §8 report; mechanisms not looks; the effective-state evidence law wins over quiet chrome) + its §11 companion routing (accessibility/keyboard/reduced-motion/responsive/localization — binding on every visual row, never silently dropped) — VISUAL_SYSTEM_UI §0/§6/§11 (admitted iter-229, D-211); every frontend INTERACTION/IA/selection/epistemic/accessibility/localization/responsive/Observatory question routes through docs/FRONTEND_UIUX_LAW.md FIRST (the interaction law owner, admitted iter-233, D-214); Redot/Godot engine questions route to the archived pack's reference docs (D-245 — the index deleted, never a repo file again); application/runtime contracts (operations/lifecycles/identity/deadlines/streaming/persistence/inference) through docs/WORKBENCH_APP_LAW.md; Observatory analytical semantics (planes/World Question/query families/run identity/promotion gate) through docs/OBSERVATORY_LAW.md; world presentation/Scene IR/assets/LOD/degradation through docs/WORLD_PRESENTATION_LAW.md — all three D-218/iter-237, the v5.2 corpus re-homed, the external docs never needed again; every llama.cpp inference-control question (chips, scopes, AUTO, the sampler chain, relations, effective state, presets/recipes, capability versioning, the extra_args hatch) routes through docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md FIRST (D-219, inf-1 — the semantic core in workbench/application/inference/ (the package since ssi-4); the profile store IS the §19.1 BASE PROFILE layer; the launch settings own DEPLOYMENT only after the one-way migration; chat's BASE temperature resolves through the resolver; the raw extra_args hatch never shadows a semantic control); every SSI / risk-class / proof-carrying-change / ssi-phase question routes through docs/ssi/SSI_OVERLAY.md FIRST (D-222, ssi-2 — the block matrix + the rule subset + the phase ladder; the risk ladder's binding home AGENTS §2.9); every topology / module-ownership / co-change / god-object / read-seam question routes through docs/SSI_TOPOLOGY.md FIRST (D-224, ssi-3 — the 82-module map + the audit verdicts + the phase consequences; scripts/topology.py the instrument).**
- **Chronicle conditionals read FLAT context keys and, since iter-265, the location fold's DOTTED state keys (`loc_malby.destroyed` — the §6.5 render conditional's surface: seeded flags/accounts + event writes, tolerant, a reader never a truth test); a checked action's verdict is NESTED (`outcome.check.passed`, iter-43) — `render/tracery.py` + `render/chronicle.py`; validator verdicts follow CURRENT canon never the anchor (iter-9; invented = contradicted, unmodeled = insufficient_data) — VALIDATION_SPEC §4–§5.**
- **Crossings fire in tick order (co-occurring: the coarsest clock first — macro → rotation → beat); director/urgencies ride the INTENT door, reactions the COMMIT door (D-037/38/39)** — BRIEF_SPEC §3.2/§3.3; KI#17 (git).
- **System passes scan the whole projection, never the seeding events (KI#16); the decay baseline = the last axis-changing event's tick via the (entity, prop) → tick index (KI#19, D-050)** — D-050's record.
- **Hardcoded `from_` is a desync (KI#13/KI#46): repeat effects idempotent; the carried-item position contract single-owned by `movement_changes`; the `_commit` gate fails loud before the write (D-035)** — `core/resolvers.py`.
- **INV-3's stoplist: no setting nouns in the ENGINE (`core/`+`sim/`+`brief/`, segment-matched, pack-tied word list); `render/`/`cli/`/`scripts/` are periphery (D-046)** — the stoplist test owns enforcement.
- **Malformed playscript steps raise RunnerError; well-formed but world-impossible intents emit `intent_rejected` (attempts are facts); urgency rejections stay silent** — PARSER_SPEC §4/§6.
- **Env-pinned verification cuts both ways: the golden T1 fixture byte-compares only on the generating interpreter (TEST_PLAN §1.1, §3 the migration — the cross-interpreter half now answered by the semantic companion layer: ssi-7/D-229 `scripts/semantic_diff.py`, any log vs the golden semantically, TEST_PLAN §1.4); and PIPE-READING subprocess tests never lean on the host's PYTHONUNBUFFERED — the sandbox exports it, CI/owner machines do not (KI#93: three green-local/red-CI iterations) — the chain owns its buffering (`-u` child, line-buffered supervisor, the env-stripping spawn)** — tests/test_workbench_launch.py + TEST_PLAN §1.1/§1.4
- **Doc drift is evidence, not prescription — verify with `git log -S` AND the pinning test before acting (KI#42/48/51/80); bootstrap texts are convenience copies, never a second source** — D-024/D-027.
- **The code-quality bar: AGENTS §4/§9 the law, BLUEPRINT §2 (L13/L14) the constitution, test_architecture + the stoplist test the executable; no new canonical layers (D-018)** — D-031.
- **Procedural guards: git hygiene (verify `.gitignore` after any upload; a file DELETION needs an explicit `git rm` or it never lands (KI#55); `git status --short` before every commit — AGENTS §7) + scope-creep (content/tone → D-030 + PACK_SPEC's sketch row; two consecutive doc-only iterations stop unless a fresh owner request fires (D-022) — AGENTS §2)**
- **DF exports are malformed/truncated CP437 XML: byte-sanitize, stream with iterparse + clear, tail-check truncation; off-matrix record tags render UNDOCUMENTED** — the matrix: `docs/ref/df_legends_xml.md`; the recipe: TECH_NOTES §3.1–§3.3.
- **The cap laws: substance over line count — filler cut always; named systems/field lists/enum values/verdicts never cut to fit; a breach triggers a cruft pass first** — AGENTS §6/§6.1; enforced by `scripts/docguard.py`.
- **The read-side layers are pure: render rebuilds the RngBank from the header seed; the assembler zero-RNG over (log, ledger) (D-049); retrieval a pure fold, `knower` IS known_by (D-088); and the scene ledger: commit → retire_contradicted → sync_scene → assemble → narrator → apply_delta (auto-syncs; re-asserting terminal states = laundering, refused); the ledger dies with its session (D-139)** — BRIEF_SPEC §2/§3.3.
- **The STATUS tests-count line feeds the digest's regex: `N passed + M skipped, ruff clean` — one line, comma-free from the counts to `ruff clean` (parenthetical caveats go AFTER `docguard clean`), else the digest reads `(unparsed)`** — `scripts/digest.py` `_TESTS_RE`.
- **The Workbench runtime layout + the local model flow (wb-9/D-208 + wb-10, re-pointed D-245): `workbench/runtime/` is the gitignored root — `models/` (the MODELS_ASSETS folder, auto-created), `llama.cpp/` (the drop folder; the launcher discovers llama-server.exe at its root or one folder deep, then PATH), `settings.json` (the persisted launch settings — corrupt/foreign-schema refuses loud); the zero-command entry is `Workbench.bat` at the repo ROOT (double-click; needs Python 3.11+ and Node.js LTS on PATH — the launcher resolves npm itself, runs `npm install` on the first run, and forwards the OBSERVED bind URL as `GATEWAY_TARGET` — the Vite proxy target, never a divergent committed default; `scripts/workbench_launch.py` the command form — run it from the repo ROOT, inside scripts/ the path doubles; `--no-frontend` the gateway-only form); a model ARRIVES by the native picker — the OS file/folder dialog hands ABSOLUTE paths to the gateway's `model.import` run (a local copy: `.part` + atomic rename, live progress, cooperative cancel — NO network, INV-4 untouched; the URL fetch stays the collapsed advanced row); `model.list`'s document carries `models_root` (the open-folder answer, never a local guess); `scripts/workbench_app.py` alone serves the gateway with MANAGED the default; the forwarded value is the ROOT (scheme://host:port — the banner's `/op` route STRIPPED, KI#98/iter-238: the client owns the route and appends `/op` itself; a route inside the forwarded value doubles to /op/op → 404, the dead-session chain); the web child runs in its own POSIX session — the teardown killpg's the whole tree, a bare SIGINT-to-npm would orphan npm's sh→vite grandchildren (the iter-290 live-proven defect)** — the modules' own docstrings + CONTRACTS §5's wb-10 note + the launcher docstring
- **The iter-232 laws: a cooperative-cancellation TEST never calls checkpoint() once and prays — the single call races the main thread's run.cancel dispatch (a fast runner's worker passes through, the "unreachable" guard closes the run FAILED; the sandbox stays green on scheduling luck while CI goes red — KI#95, three-form verified: sandbox, forced fast worker, delayed cancel); poll the checkpoint (the work contract's own lock-free observation surface — run.cancel is never starved) bounded until the cancellation lands, an absent cancel fails LOUDLY; discovery lists never freeze behind one-shot success latches — every surface entry re-scans (KI#96: the owner's hand-dropped GGUF must appear on the next Models entry; the wb-11 re-arm lesson generalizes from FAILURE to staleness — a "requested once" flag guarding the happy path is the bug, not the guard)** — tests/test_model_fetch.py `_SlowFetcher.fetch` + the web client's surfaces inherit the same laws, iter-232
- **The deleted Redot era (D-245 — the .gd tree + its proof packets + the engine index removed; recovery: git history + docs/frontendweb/archive/): its GDScript lessons are HISTORICAL now — the adjacent-literal refusal (KI#91), the `static func tr(` parse refusal (the strings.gd `lookup` boundary), the chat follow law (scrollbar max read AFTER a frame, the near-bottom gate), the values-only theme re-pin — carried forward as PRINCIPLES for the web client (one boundary per concern, late-layout reads after a frame, tokens swapped values-only), never as live routing; a Redot/Godot engine question today routes to the archived pack's reference docs, not to any repo file**

## Next step

**iter-295 DONE: observatory (Phase 3's second row, the owner's
  «продолжай работы по фронтенду» repeated call; R2
  frontend-local).** The dual-read law's HISTORY half landed over
  the existing observatory.runs/read READ ops: ONE bounded window
  at a time (the event-id cursor, next_after pagination that
  REPLACES the window), the context strip's identity line, NO
  DATA/NO MATCH/stale-cursor/TRANSPORT distinct, no polling; 78
  vitest + tsc + build + the live smoke 8/8 over a real
  CLI-generated run (run_125_0, 56 events, the head window 50/56,
  the forward window to the end, NO MATCH and the stale cursor
  verbatim).
Next: the owner's calls — the Phase 3 continuation rows (each its
  own iteration: the Chat/Inference contract mirror + surface —
  needs a loaded model for the full band, the Settings mirror —
  the backend.settings family, both ops live at the app gateway),
  the streaming admission (SSE — the backend gateway contract
  first), the acceptance matrix, the DECISIONS collapse (36→30, the
  owner's call), and the world track's parallel rows.
Active KIs: KI#109 CLOSED iter-294 (the record above — deleted at
  the next STATUS-touching iteration per §5). The suite green
  (2529+1; the frontend 78). The owner's RU report:
  docs/iterations/iter-295-frontendweb-report.md.
iter-294 DONE: shell (Phase 3's first row, the owner's
  «продолжай работы по фронтенду, над теми частями что логичнее
  всего сейчас провести» call; R2 frontend-local + KI#109).** The
  SHELL/NAV + the SESSION LIFECYCLE surface over the existing six
  ops: only the active pane mounts (boundedness); the lease closure
  REQUESTED→ACCEPTED/REJECTED→EFFECTIVE→OBSERVED, G4 no-retry,
  STALE_REVISION/LEASE_EXPIRED verbatim; 59 vitest + tsc + build +
  the live smoke (attach/detach/stale/expired against the real
  gateway); KI#109 closed (the mirror's 16 missed D-245 deletions
  re-executed, 2529+1 restored).
iter-292 DONE: methoddoc (the owner's tmpfiles v3 delivery + the
  «определись что перенимаем и куда» call; R0, doc-only).** D-246 —
  the design-research & mechanism-transfer method adopted as METHOD,
  never authority: the verbatim original archived (md5-pinned, the
  read-only-copy class), the durable residue distilled as the agent
  context's §9 (the five mechanisms + the depth ladder + the gates +
  VIS-0..3 + the transfer-record form), the doc's own §34
  rejections made CanonSim's (no parallel authority, no global
  Reference Lock, no novelty quota, no pixel-perfect gate); zero
  code, the product owners untouched.
Active KIs: none new. The suite green (2529+1). The owner's RU
  report: docs/iterations/iter-292-methoddoc-report.md.
iter-291 DONE: redotfix (KI#108 — the half-applied iter-290 delta;
  R3, the completion of the RECORDED D-245).** The owner-side
  application landed the 65 changed/created paths but never executed
  the 16 deletions — the repo claimed Redot deleted while the tree,
  the index, the proof packets, and the Setup .bat stayed tracked
  (docguard red on the 1462-line index, the stale shell-contract pin
  red). Fixed: the 16 paths removed, the suite back to the claimed
  2529+1, docguard clean; the one stale live-routing FAQ half synced
  to the archived-pack form; the law-body residue (UIUX §0's diagram
  row, WPL §14/§15 mentions) named for the owner, never silently
  rewritten.
Active KIs: KI#108 CLOSED iter-291. The suite green (2529+1). The
  owner's RU report: docs/iterations/iter-291-redotfix-report.md.

iter-286 DONE: the W7 station's fourth row (the owner's «точечный
  и быстрый (read-side only)» call — the named-boundary rendering
  route, iter-284/285's boundary (a); the same call conditionally
  declining the disappearance-battery extension and opening W8,
  both conditions resolved; R2 read-side only): rs-13 — the pack
  table rejection_boundaries (leverage_over -> «no minted word to
  lean on»), the ONE gloss boundary, the boundary slot before the
  outcome loop, the intent_rejected line's conditional tail, the
  armed-gate vacuity lint; MEASURED (tests/test_namedroute.py, 6
  tests): the no-word twin's record renders «tries to coerce —
  impossible here — no minted word to lean on» — the Q5 boundary
  CLOSED at the readable surface; the unglossed gates byte-stable,
  the tale gate untouched, the golden corpus byte-identical. W8
  OPENED — the W7 station COMPLETE (iter-283/284/285/286). The
  owner's RU report: docs/iterations/iter-286-namedroute-report.md.
iter-285 DONE: the W7 reading band's LIVE half (the owner's blind
  Q1–Q7 over the iter-284 kit received and scored against the
  standing preset, the iter-270/280/282 precedent's form): every
  pre-set bar MET n=1, the convergence question resolved yes — all
  three ripples caught in the blind half; the reading band
  CONFIRMED at BOTH bands (LLM n=2 + live n=1). The owner's RU
  report: docs/iterations/iter-285-neglive-report.md.
iter-284 DONE: the W7 reading band's LLM half (the battery's
  answers as blind readings over the same battery's twins — the
  W5-form kit of five packages, the preset before any reading, the
  clean n=2 after one discarded contaminated pilot): every bar MET
  (the departure, the carrier, the trade, the vigils 3=3, the dead
  door, the invisible door's sell_bloom catch), the free namings
  divergent; the readers' own discovery: the disappearance's
  footprint wider than the census (the wait-band ripple, the
  watch-briefing ripple, the records' entanglement) — the reading
  band CONFIRMED at the LLM band; the live band stayed the owner's
  (landed iter-285). The owner's RU report:
  docs/iterations/iter-284-negread-report.md.
iter-283 DONE: the W7 station's first row (the owner's «W7 открывай
  если больше ничего не осталось» call): the eight-question battery
  + the compression test on the same committed package — the
  negative-space census, the lint's measured refusals, the
  disappearance battery's three arms (settle / mourning / word), the
  reachability inventory: no decorative material at the measured
  band, the pack compressed; the honest boundaries classified (the
  reachability-by-construction band; the unglossed literals the
  documented dry fallback; the ungarrisoned window the composition
  witness's own limitation). The witness tests/test_negative.py.
iter-281 DONE: the two double-confirmed RENDERING_GAP routings
  (the owner's delegated continuation call over iter-280 §F — the
  W6 station's own remaining rows; W7 stays "after W6"): both gaps
  closed read-side (the night form via phase.*/site.* + the
  symbol-indirected move arm; the balance-move's causal row via
  the account line's knows tail + the re-authored glosses) and
  RE-MEASURED blind n=2 over the regenerated kit (byte-identical
  double build): ADVENTURE 4/4 (the night form extracted and
  quoted by both readings — GAP (a) CLOSED), MYSTERY 3/3 (no
  regression), POLITICS P1/P2 MET + P3 materially improved (the
  guild's agency n=2, the causal row quoted n=2 — GAP (b)'s named
  legs CLOSED; the honest residuals: the intermediate arithmetic
  unassembled though all numbers sit on the surfaces, the
  decisive-move slot still the fires, the public retention not
  explicit), the free namings again divergent — the reading-side
  CONFIRMED at the improved band. W6's own rows COMPLETE.
iter-279 DONE: the W6 reading band's LLM half (the owner's
  «продолжай работу над задачами класса world track, делай то что
  логичнее и правильнее сейчас сделать а не потом» call — the
  current station's open row, the recorded W5 form): the reading
  kit delivered over the committed pack — two one-history packages
  (the JOURNEY seed 42 carrying adventure + mystery together; the
  POLITICS seed 2 carrying the differential institutional answer +
  the squeeze), the pre-set audit written before any reading, the
  blind glm readings n=2 per question — MYSTERY 3/3 convergent,
  ADVENTURE 3/4, POLITICS 2/3 (two RENDERING_GAPs named, never
  fixed: the night risk form, the balance-move assembly), the free
  readings diverging materially across the same pack's packages
  (the W6 hypothesis's divergence half carried at the free band).
  2530+9. The owner's RU report:
  docs/iterations/iter-279-genreread-report.md.
iter-278 DONE: the W6 genre matrix's first row (the owner's
  «открывай задачу по W6» call — the station's law held: a failed
  genre test identifies the missing world substrate, never triggers
  plot writing; no test failed at its named band): the matrix's
  substrate-side measured at the deterministic band on the SAME
  committed package — adventure / mystery / politics CONFIRMED at
  their named bands, the four carried genres cited (biography,
  comedy, tragedy, relationship drama — the W5 evidence), the census
  pinning all seven genres' surfaces; the honest boundaries
  classified (the authored edge closure — the I0 inventory's
  route-writer candidate, SUBSTRATE_GAP awaiting repetition; the
  mystery's one-fact/one-path/one-revelation band; the player's
  re-pricing power — iter-271's residue; the READING band
  owner-routed).
  2530+9. The owner's RU report:
  docs/iterations/iter-278-genre-report.md.
iter-277 DONE: the world-track archive ingestion (the owner's call:
  the external WORLD_TRACK_NEXT_v4_AGENT_PACK_v4.5.zip fully ingested
  and reconciled, the durable agent context created, the pack
  preserved as historical/bootstrap evidence — a future agent never
  needs the zip re-uploaded; KI#106 found and closed; the W-boundary
  recorded: W1–W4 closed historical foundation, W5 gate met /
  evidence retained, W6 the current execution stage, W7 after W6,
  W8 after W7).
  2520+9. The owner's RU report:
  docs/iterations/iter-277-worldcontext-report.md.
iter-276 DONE: the I0 World Ignition Witness (the five-leg chain
  measured on existing primitives over the perturbed keep-Malby
  edge; the four timelines diverging never synchronized; the verdict
  — the substrate expresses the chain, no machinery promoted; the
  limitation inventory opened with three named candidates).
  2520+9. The owner's RU report:
  docs/iterations/iter-276-ignition-report.md.
iter-275 DONE: the §6.2 fill row (PRESENT + NOTCH as live account
  state, HATCH held as prose, the two-sided band gap measured and
  named — the I0 inventory's first candidate; the embodiment
  fill-list now CLOSED).
  2513+9. The owner's RU report:
  docs/iterations/iter-275-stepbench-report.md.
iter-274 DONE: the §6.5 move release (the owner's row at its
  measured price — the mourns intent pick re-authored to the
  departure; the talks 287→2, the council pile 1→208, the honest
  liveness shape: a living world is not a loud one; the smoke corpus
  untouched; the surface re-measured and pinned).
  2506+9. The owner's RU report:
  docs/iterations/iter-274-moverelease-report.md.
iter-273 DONE: the §6.4 SALE fork resolved through the owner's
  generalized transaction synthesis (the fourth verb `settle` — the
  multi-leg transaction over explicit owners; the re-weigh's sale
  `sell_bloom` armed — the withhold's release, one load walked to
  the beam's receiving stock for three coin banked at the crofts'
  own ledger; the grammar wall measured first: the closed verbs'
  from-side always the intent actor, the crafted transfer probe
  refused at the actor's gate while the heap stands full; the class
  pinned with the buyer's purchase — the owner's own example, one
  atomic event over the same verb; the corpus byte-identical, the
  twin deterministic; the R3 PCC record rides phases.md §6).
  2506+9. The owner's RU report:
  docs/iterations/iter-273-settlement-report.md.
iter-272 DONE: the §6.1 fill row (the fill-list's second row —
  the crossing's carrier strengthened): the flood debt's full
  lifecycle over the account resolver's player-scaled arm — pure
  pack data, zero core, the charcoalpaper precedent's family applied
  to the crossing. The FOURTH kind floodpaper (the flood winter's
  own paper — the borrowed punt twelve + the stranded season's
  stores eight, the shelter law's cost; its own dated chain in the
  kind's gloss, never the camp's starved winter) stocked on the
  toll-taker (the paper twenty, the drowned generation's debt the
  living hand's now) + the receiving stock on the second hand (the
  inheritance's existence gate); the four doors: settle_paper (the
  FALL, the covered-fund gate), render_toll (the COLLECTION, the
  geography gate at the chest), pass_paper (the INHERITANCE — the
  drowned generation's open question ANSWERED: the debt walking to
  the living line, the pole and the paper one inheritance), buy_punt
  (the PUNT'S PURCHASE, the punt fund's terminus — the flow
  vocabulary's no-terminus residue closed); ONE COIN, TWO CLAIMS
  made doors (the punt's twelve and the settlement's twenty on the
  same thin surplus — the punt spent first leaves the fall refused).
  Measured: the fall refused early / landed covered with the
  witnesses holding the_floodpaper_fell and the tale carrying both
  reckoning lines with the flood-winter gloss; the coupling
  measured; the inheritance walked to the line with the stockless
  target refused softly; the golden corpus byte-identical (zero
  corpus price); the twin deterministic; the four census re-pins
  (campaccount / charcoalpaper / debt1 / freightvol). Honest
  residues: the punt's item-birth rides the parked st-5 door; a
  dedicated boatyard entity a future row's own call. 2493+9 + ruff +
  docguard + topology --check clean. The owner's RU report:
  docs/iterations/iter-272-floodpaper-report.md.
Next: §6.4's SALE fork (the owner's call on the grammar wall) →
  §6.5 (the move-release, the owner's future row at its iter-263
  price) → §6.2 (present / hatch / notch) → W6 genre.
Active KIs: KI#104, KI#105 (both CLOSED iter-269).
iter-271 DONE: the §6.4 fill row's first landing (the fill-list's
  front row — FACTOR NEGOTIATION armed, the SALE forked to the
  owner, the TAG measured at its boundary): the paper's RENEGOTIATION
  as the guild's SQUEEZE over the account resolver's player-scaled
  arm — the door reprice_paper (the squeeze's two sourced onto the
  standing terms, the withheld margin's own number; the
  standing-terms gate; the receiving-stock gate; the knowledge row
  the_paper_repriced public; the compounding lawful while the terms
  stand); the factor stays gateless as an entity (the beat rides the
  seat's acceptance-door); the honest residue "the renegotiation
  stays authored" CLOSED; the measured FORK recorded (the SALE — the
  heap's drain): the account resolver's ACTOR-SIDE GRAMMAR WALL (a
  location's stock is only ever a TO-side — the drain not authorable
  as pure pack data; the owner's fork (a) the price-door (b) the
  re-seating REJECTED (c) a location-side drain verb R3+); the TAG
  TRANSFER at its boundary (the drop+take pair carries the
  mechanics, the recognition mint stays un-armed). 2484+9 + ruff +
  docguard + topology --check clean. The owner's RU report:
  docs/iterations/iter-271-repricing-report.md.**
iter-270 DONE: the owner's live reading of the delivered kit RECEIVED
  and SCORED (the standing order's third row's own next beat — the
  blind answers in the chat, the convergence assessment against the
  pre-set bars, the live band's fresh n=1): every station bar MET at
  the live band, the strict heartbreak pair CARRIED (the lost-future
  half — the rs-8 re-subjectivation read exactly; the opened half —
  the rs-7 clause quoted exactly), rs-9's causal row + rs-10's dated
  chain both carried in full (the iter-208 human datum closed), the
  humor's position-dependence explicit, the 40/80 echo consumed
  naturally in reading; the heartbreak divergence's class RESOLVED
  per the pre-set rule — the glm recheck's miss was the LLM band's
  own reader-class variance, never a surface regression and never the
  question form; the heartbreak human band MET on the fresh kit; the
  live band's return row CLOSED (both just-landed surfaces read
  together). 2478+9 + ruff + docguard + topology --check clean. The
  owner's RU report: docs/iterations/iter-270-livescored-report.md.**
iter-269 DONE: the live band's return + the heartbreak recheck (the
  standing order's third row) DELIVERED — the reading kit re-established
  over the CURRENT committed pack and handed to the owner: both
  packages regenerated deterministically at seed 42, byte-identical on
  regeneration, the re-weigh package now carrying BOTH just-landed
  surfaces (rs-9's hold line + rs-10's dated withhold line) with EVERY
  recorded substance shape hit exactly (the night read t=1112 partial,
  the fall t=2824, the collection t=2826, seven crossings, the close
  paper 0 / coin 8 / fatigue 98, the heap 18, the runner among the
  fall's witnesses, the tale 90 lines); the heartbreak package
  byte-stable against the recorded form (43 events, the tale 24 lines,
  rs-7/8's lines, the dry holds); the briefs' cut points reconstructed
  to the natural mirror of the recorded form (the honest note — the
  original wording died with its session, Rule 9); the pre-set author
  audit written BEFORE any reading (the isolation law) — the station
  bars + the TWO NEW ROWS' bars; the HEARTBREAK RECHECK — the glm
  blind reading n=2 over the heartbreak package: the opened half 2/2,
  the lost-future half 1/2 (reading 1 carrying the rs-8 clause's own
  semantics; reading 2 in the iter-204 remembered-dead mode), the
  strict n=2 pair NOT met — the divergence's class UNRESOLVED between
  the reader-class variance and the reconstructed question form; a
  surface regression EXCLUDED (the package byte-stable); the iter-206
  n=2 MET and iter-208 n=1 human MET records STAND; no fix attempted
  (NEVER "improve the prose"; the same measurement re-run until it
  passes is probe-shopping — the anti-loop law); the kit + the runner
  + the transcripts outside the repo (Rule 9). 2478+9 + ruff + docguard
  + topology --check clean. The owner's RU report:
  docs/iterations/iter-269-livereturn-report.md.**
iter-268 DONE: the shave's temporal surface (the standing order's
  second row, the W5 owner disposition's ADD TEMPORAL SURFACE call)
  LANDED read-side — the withhold's own line carrying the dated chain:
  "the smelt crofts comes by 2 bloom kept off the weighbeam since the
  guild factor shaved the camp's weight two seasons back and the camp
  starved that winter — the withhold's own ledger at the year's
  reckoning — the camp's answer to a tilted beam: unweighable at it,
  the paper still paid" (the earlier season → the hunger winter → the
  present consequence — the temporal anchor the iter-201/202 readers
  lost, restored on the line they actually read); the mechanism rs-10
  (the rs-5 precedent's own form — the SAME kind row re-authored,
  zero code): ONE table row re-authored (templates.json::
  account_kinds, bloom) + the re-pins (the three committed witnesses'
  gloss constants — the deliberate act the pinning law names) + the
  witness tests/test_shavememory.py (8 tests, the claim packet: the
  dated chain's cells, the arc assembling ACROSS the tale's lines
  through the winter's shared name between the two kind glosses, the
  misparse falsifier — "that winter at the year's reckoning" absent
  by the ledger tail's construction, the regression bars, the corpus
  price, the twin); the measured evidence: the sparse twin's withhold
  line carrying the chain at every crossing (seed 42), the crofts'
  state apposition the same row (one boundary, every consumer), the
  province smoke byte-identical (zero corpus price), the read-side
  twin, and the probe's re-run — the glm blind reading n=2
  convergent over the reconstructed recorded package (every substance
  shape reproduced exactly: the night read t=1112, the fall t=2824,
  the collection t=2826, seven crossings, close 0/8/98, heap 18):
  the shave placed BEFORE the tale's events ("The phrase 'two
  seasons back' clearly indicates this happened before the tale's
  events" — reading 2), the withhold read as the dated past's
  consequence, the regression bars held, the iter-201/202 failure
  modes GONE (no present-weighing conflation, no "dispute remains
  uncertain"); the author audit pre-set BEFORE the reading (the
  isolation law), the runner + transcripts outside the repo (Rule 9);
  the honest boundaries: the row dates the MEMORY as the camp tells
  it (the authored constant, never a runtime clock read), the debt's
  BIRTH stays on the paper's own line (the surfaces chain through
  the winter's shared name — neither probe reading spells the
  borrowing, the arc's assembly at its measured ceiling), the brief's
  recalled-facts token stays dry (the brief's own law), the live
  human band stays open (the standing order's next row reads both
  just-landed surfaces together). 2478+9 + ruff + docguard +
  topology --check clean. The owner's RU report:
  docs/iterations/iter-268-shave-temporal-surface-report.md.**
iter-267 DONE: the runner's grudge discovery surface (the standing
  order's first row, the W5 owner disposition's ADD DISCOVERY SURFACE
  call) LANDED read-side — the hold's own line carrying the
  pack-authored causal row: "the factor's runner now holds something
  over Garrick — the camp's word: the honest count cut in the tally;
  the guild factor shaved the camp's weight two seasons back and the
  camp starved that winter, and the bloom has sat off the weighbeam
  since" (the standing → the remembered incident → the why, never the
  biography); the mechanism rs-9 (the account/flow gloss boundary's
  own shape): ONE table row (templates.json::knows, the_camps_word →
  the prose) + the leverage line's conditional tail ({secret? —
  {secret}}) + the boundary extension (render/chronicle.py: the
  outcome's secret key rides the KNOWS boundary — rs-1's law, one
  table, every consumer; an unglossed secret pre-seeds EMPTY, every
  other hold rendering the dry standing unchanged, a foreign log's
  included); the measured evidence: the lever chain's tale carrying
  the row at seed 42 (the day arm AND the partial-fidelity night arm),
  the grim fixture's leverage line DRY (the unglossed law over a
  committed corpus), the province smoke byte-identical (zero corpus
  price), the read-side twin; the witness tests/test_grudgesurface.py
  (9 tests, the claim packet); the honest boundaries: the row is the
  CAUSAL surface only (the temporal placement the NEXT row's own
  material — the shave's dated-memory surface), the other three
  read-hinge secrets stay unglossed (each its own row's call on the
  owner's voice), the brief's recalled-facts token stays dry (the
  brief's own law). 2470+9 + ruff + docguard + topology --check
  clean. The owner's RU report:
  docs/iterations/iter-267-runner-grudge-surface-report.md.**
iter-266 DONE: the W5 owner decisions LANDED as the owning docs' decision records (zero code/pack/canon) — the residue list SPLIT by disposition (fail-then-pass + 40/80 CLOSE AS RESIDUE; the runner's grudge ADD DISCOVERY SURFACE; the shave's timing ADD TEMPORAL SURFACE), the fill-list re-ordered (§6.4 → §6.1 → §6.5 → §6.2 → W6, §6.3 REMOVED), the decision standard recorded as standing law. 2461+9. The owner's RU report: docs/iterations/iter-266-w5-owner-decisions-report.md.
iter-265 DONE: the render conditional (the §6.5 row's last leg) LANDED read-side, zero core — the renderer's location fold (the DOTTED conditional keys) + the market line's own arm; the falsifier dead (36 ashes lines, 0 standing). 2461+9. The owner's RU report: docs/iterations/iter-265-render-conditional-report.md.
iter-264 DONE: the §6.5 embodiment legs LANDED as pure pack data,
zero core — the mourns hook market_mourns (the prop trigger, the
RAMBLE intent pick, the TRIGGER-ONLY law's option gate), the trade
verb trade_at_market (the stall gate closing the commerce with the
burned market by construction), the council/vigil knowledge blocks;
the composition deltas exactly the iter-263 predictions; the witness
tests/test_marketlegs.py. 2455+9. The owner's RU report:
docs/iterations/iter-264-market-legs-report.md.
iter-263 DONE: the carrier-or-surface discrimination over the owner's
question — the three-move probe (the reader audit → the ablation arm →
the injection arm, WORLD_TESTS §7's third member; zero core/pack
changes): the verdict PER-LEG never per-institution (the market
carries all four bands; the calendar line a surface BY CONSTRUCTION),
the epistemic band named and measured, the market-mourns prop trigger
measured both ways (the move release massive, the ramble
minimal-but-material — §6.5's move-release price), four
expressibility boundaries named, the J-rows re-framed by measurement.
2445+9. The owner's RU report:
docs/iterations/iter-263-carrier-surface-report.md.
iter-262 DONE: the composition-bottleneck diagnosis — the twin-fold causal-inertness test, J-1 re-framed, KI#103 fixed (the wait resolver's knowledge minting), J-3 closed. 2445+9. The owner's RU report: docs/iterations/iter-262-diagnosis-report.md.
iter-261 DONE: the composition question over the parked intake-40
P1 set — P1-1 the Province integrated witness (16 relational-oracle
tests over one 2371-event run), P1-10 the timing witness (mechanics.py
timing — the two-times table, the first named assignment_tick
consumer), cov-1's runtime arm (census --log, the A..H loss
vocabulary), the H1/H2 sliced pair measured (material outcomes
invariant, deltas door-only), the province_calendar provenance fixed,
B3 consumer status diagnostic-only, B1 no promotion evidence, the
J-gaps all pack-level. 2444+9 + ruff + docguard + topology --check
clean. The owner's RU report A–J: docs/iterations/.
iter-260 DONE: the temp-1 LANDING over the owner's contract pick
(A2 + B2/B3, B1 deferred) — the crossing-family slicing contract
pinned (test_temp1_contract.py), the semantic-origin provenance landed
(provenance.assignment_tick, schema 0.3), B2's runtime untouched (the
clustering witness byte-verified), B1 deferred behind the card's
reopening conditions; the five fixtures regenerated with every
canonical field byte-identical to BASE.
iter-257/258/259 DONE: the intake-40 instrument session — the fork
card + cov-1 (D-234) + div-1 (D-235) + KI#101/102 closed.
iter-255+256 DONE: the intake-40 routing (D-233) + KI#100 closed.
iter-251/252 DONE: the ssi tail phases 6+7 (D-229/D-230).
iter-241..250 DONE: the ssi foundation + phases 1..5 + KI#99
(D-221..D-228).
1. The B1 architectural follow-up (generate-at-T) stays DEFERRED and
   OWNER-GATED — iter-261/262 both found NO promotion evidence (the
   material outcomes invariant under slicing; the calendar turns
   causally inert) — reopened only on the card's five conditions
   (phases.md §6's decision record). The B3 production-consumer
   watch: the field's standing consumer set = the contract test + the
   timing instrument (diagnostic); a production consumer
   (chronicle/observatory reading the deferral) or two iterations
   without new consumers → the demotion question (the report's F, an
   owner call, no churn now). THE J-ROWS AFTER iter-265 — ALL CLOSED:
   (J-1) the market DECOMPOSED — its material/economic/social legs
   live carriers (iter-263); the READER legs LANDED iter-264 as pack
   data (the mourns director hook with the ramble release and the
   trigger-only law, the trade door, the council/vigil knowledge
   blocks); the RENDER conditional LANDED iter-265 read-side (the
   renderer's location fold + the market line's own arm — the tale
   never contradicting the projection); the authored unit at
   ANCHOR_REGION §6.5 (the fifth meso unit) with every embodiment row
   closed except the move release (the owner's future row at its
   iter-263 price); the calendar line stays a surface BY LAW
   (measured twice — the lint's closed grammar, the empty on_action
   scope); (J-2 remainder) the knowledge blocks LANDED (the tokens
   minting, the watch-briefing and rumor-cascade consumers live, the
   cascade measured 22→25); (J-3) CLOSED — no row. THE WORLD TRACK
   after iter-266 — the W5 owner decisions LANDED (the dispositions
   record: WORKPLAN §7 + WORLD_TESTS §9's W5 entry + the iter-266
   report's corrected P0 split); the owner's standing order: the
   runner discovery surface → the shave temporal surface → the live
   band's return + the heartbreak recheck → the embodiment fill-list
   rows (§6.4 → §6.1 → §6.5 → §6.2; §6.3 removed — its probe
   completed iter-204..210) → then W6 genre, the region move, the
   fenced set. ssi-5
   stays owner-gated (the N018 evidence law). The owner-side cleanup
   standing from D-230's third card: delete the doubled
   `workbench/workbench/runtime/` tree locally (safe — the iter-246
   root fix landed; the tree regenerates on demand).
2. The P1/P2/P3 continuation per FRONTEND_UIUX_LAW §25 (each row on
   the owner's call): obs-3+ — the P3 analytical rungs (timeline
   lanes, compare arms, semantic zoom, cross-highlighting — the
   interaction grammar per FRONTEND_UIUX_LAW §§5–7, the analytical
   contracts per OBSERVATORY_LAW §§11/18; the question EDITING form
   when its consumer names itself) · wb-13+ the visual rows (P2: the
   shell responsibility split continuing, per VISUAL_SYSTEM_UI §10,
   the chat ergonomics contract now LAW §21.1) · inf-3+ the inference
   continuation (capability discovery, the model-driven context
   awareness, the session/preset persistence layers,
   LLAMA_CPP_INFERENCE_CONTROL_LAW §21). The exported-Windows-build
   row parked per AGENTS §2.4 — a named row when the owner calls it.
3. The remaining station rows (the owner's next engine run, TEST_PLAN
   §8.5's standing gaps + the wb-6 arm: the live-build
   /models/load + /models/unload re-verification against the b11064
   station's ROUTER reality): the 27B GBNF parse arm + the
   one-model-constrained A/B (CONTRACTS §4.3 arm a) + the brief/
   parse component split; the narrator-convention call for live
   narrate play is two-sided now — more live beats at Q9B (size the
   tail) or the 27B as the one-model candidate (the §1 sweet spot,
   both doors) — the owner's choice (round 5's 12B + round 6's 9B
   data: §13.1; bg-9's mapping-drift datum rides the same decision).
4. The standing frames: the embodiment options (§6.4 → §6.1 → §6.5 →
   §6.2 per the owner's 2026-09-27 order; §6.3 closed iter-204..210,
   its fill row removed), the debt-1 residues, the re-weigh's SALE,
   the runner's grudge surface (the standing order's first surface),
   the shave's temporal surface (the standing order's second), the
   SoW horizon (bg-6, owner-deferred — long-parked per the owner's
   2026-09-21 call). New rows enter on the owner's call only.

