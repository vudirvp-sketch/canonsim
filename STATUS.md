Iteration: iter-326 (`lab4` — the owner's «продолжай» call
  (the Atomic World Lab agent pack v1.5; the E1 horizon row the
  iter-325 NEXT named — the kiloyear datum, the pack's 04 §12
  horizon battery 100y → 1,000y → 10,000y)): THE E1 LADDER MEASURED
  — `scripts/labrunner.py` the lab-4 REPLAY-COST instrument
  (`read_seconds`/`fold_seconds`/`replay_alloc_peak_mb` — the
  read-side cost split a resume/replay pays, the tracemalloc peak
  honestly labeled as interpreter allocations, NEVER the OS RSS,
  Windows-portable; `wall_seconds` and every prior field untouched,
  the records backward-compatible) + `tests/test_lab.py` the two
  lab-4 laws (the instrument law — every record carries the block on
  both protocols, a non-empty log pays real read+fold time; THE
  KILOYEAR ARITHMETIC law — the step-list pure at 1,000y: exactly
  1,000 cadence waits, custom segments sum EXACTLY to the span,
  whole stays ONE wait at any horizon, zero corpus price) + THE
  SEGMENTED LADDER 2y→650y (farstead, seed 7, square, eight rungs;
  650y = 81,823 events / 465.22 s — the deepest rung the sandbox's
  600-s tool-call window holds, the window itself measured honestly:
  background processes do not survive the call boundary) + THE
  STATION HORIZON PROBE v1 (outside the repo per Rule 9 — the
  session's offload rule: the 1,000y PAIRED battery rides the
  owner's hardware, every stage a checkpoint, a timeout is itself a
  datum, self-checked end-to-end in-sandbox). THE E1 FINDINGS: the
  wall curve STEEPENS monotonically (local exponents 1.00→1.81 — the
  iter-325 t^1.3 forecast REFUTED at depth: 1,000y ≈ 930–1100 s on
  the sandbox CPU, 16–18 min, never "minutes"; events stay LINEAR
  122–132/year — the super-linearity is the per-EVENT cost growth,
  never the count); THE FLAT-LIFE LAW (life ~71–72/year from 10y to
  650y, 650/651 spans live — a 325× horizon range with zero life
  trend: no collapse, no explosion, the deferred-realize law's
  kiloyear answer); THE LINEAR VERB LAWS (sourced 4.00/year EXACT,
  consumed 4.03, settled 8.03 — iter-325's seed-invariance now
  measured across scale to 6.5 centuries); THE CONSTANT-STATE LAW
  (projection_entities = 25 at 100/500/650y — the state NEVER grows
  with the horizon, only the LOG does; the accounts pile linearly
  ~26.3 units/year, water 1,060→6,560 — the Stage B bounded-source
  falsifier at 6.5-century scale; the super-linear wall at CONSTANT
  state = the scale-1 decomposition's named gap, never guessed);
  THE REPLAY-COST DATUM (read-bound: 0.62 s/MB flat, the fold
  near-free 0.055 s at 81,823 events, the alloc peak 3.34× the log —
  a resume pays O(log bytes), the state never participates in the
  price).
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116,
  D-151; the ladder complete 0..6 — the standing work: the
  owner-gated backlog + the web-frontend track + the world track
  + the SoW horizon, ROADMAP §2/§6) ·
2582 passed + 1 skipped, ruff clean, docguard clean, topology
  --check clean (Python 3.12.14, the env pin; R2 local-add — the
  labrunner's replay-cost instrument + two NEW tests, zero
  core/sim/render change, INV-1..5 untouched, the LOG untouched,
  zero corpus price; NO test deleted or weakened — 2 added) ·
Date: 2026-10-04 ·
Scope: scripts/labrunner.py (the lab-4 replay-cost instrument),
  tests/test_lab.py (the two lab-4 laws),
  docs/iterations/iter-326-lab4-report.md (new — this row's RU
  report) + docs/TASKS.md (the lab-4 row + the ledger, iter-316
  evicted), STATUS.md (this header), worklog.md (the iter-326 entry,
  iter-316 evicted) — 6 changed/created (5 modified + 1 created).

Track A: sem-1 DONE (iter-316) + caus-1 DONE (iter-317) + replay-1
  DONE (iter-318) + scale-1 DONE (iter-319) + speech-1 DONE
  (iter-320) + auth-1 DONE (iter-321) — ALL SIX of the queue's
  contracts LANDED and OWNER-ACCEPTED AS LAW (S1–S7 + K1–K6 +
  E1..E6 + Q1–Q7 2026-10-03; P1–P7 + A1–A7 2026-10-04); the
  implementation rows are NOT standing rows — the owner's «пока не
  открываю» call: each opens on the owner's separate call behind
  the runtime-promotion gate; core-1 stays PARKED (owner-gated
  RESEARCH/POC-ONLY — scale-1's Q5/Q6 map onto its C2/C3/C5
  surfaces, speech-1's P3/P4 and auth-1's A5 onto its C4, through
  the pinned namespace fence). The web-frontend track — S0 LANDED;
  floor's rows + the V1/V2/V3 visual floors LANDED
  (iter-293/297/304/307); Phase 3's SEVEN rows LANDED
  (iter-294/295/296/298/299/300/301) + the IA REPAIR LANDED
  (iter-297, D-247); the owner-side bands CLOSED LIVE (iter-302)
  and RE-CLOSED LIVE inside the matrix session (iter-308); THE
  STREAMING ADMISSION LANDED (iter-305/306); THE FULL ACCEPTANCE
  MATRIX CLOSED (iter-308 — 39 verified / 2 open / 1 partial / 2
  not-exposed, zero defects); THE TOOLING FLOOR'S CI + SMOKE ROWS
  LANDED + THE BOOT-TIME OBSERVED-SYNC LANDED (iter-309); THE
  STANDING QUEUE DISPOSITIONED + THE DECISIONS COLLAPSE LANDED
  (iter-310, D-250); the §8.5 heartbeat ledger COMPLETE through the
  27B band (iter-312/313/314 — the station records). The next
  frontend rows the owner's call: the replay-UI NOT-EXPOSED row;
  the standing boundaries: a SharedWorker stream transport, Tauri,
  PWA, the Settings Appearance section (no persisted store) — each
  its own admission (the import form's native file/folder picker
  rides the Tauri row). The world track: W8's remaining rows the
  owner's call. The ssi family COMPLETE except ssi-5, owner-gated.

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

- (none open — KI#112 was opened AND closed inside iter-325: the labrunner's log filename collided on identity prefixes (the anchor pair batteries first, then the 10y/100y pair), each found by the batteries themselves; the fix — the full (seed, anchor, horizon, arm, protocol) tuple in the stem. The record: git + worklog iter-325)

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

**iter-326 DONE: lab4 (the owner's «продолжай» call — the E1 horizon
  row).** The replay-cost instrument landed + the segmented ladder
  measured 2y→650y: the wall curve steepens monotonically (local
  exponents 1.00→1.81, the t^1.3 forecast refuted — 1,000y ≈ 930–1100
  s on the sandbox CPU), the FLAT-LIFE LAW (life ~71–72/year across a
  325× horizon range, 650/651 spans live), the LINEAR VERB LAWS
  (sourced 4.00/year exact), the CONSTANT-STATE LAW (projection 25
  entities at every depth — only the log grows; the accounts pile
  linearly, the Stage B bounded-source falsifier at 6.5-century
  scale), the REPLAY-COST DATUM (read-bound 0.62 s/MB, the fold
  near-free, the alloc peak 3.34× the log); the station horizon probe
  v1 built + self-checked (the 1,000y PAIRED battery — whole +
  segmented + the kiloyear REALIZED_DELTA — rides the owner's
  hardware, the session's offload rule). 2582+1 + ruff + docguard +
  topology clean. The RU report:
  docs/iterations/iter-326-lab4-report.md. The prior queue's
  standing: P1–P7
  (speech-1, CONTRACTS §10) and A1–A7 (auth-1, §11) ACCEPTED AS
  LAW — the §10/§11 notes landed in the §6/§7 form; the
  implementation rows stay CLOSED («Строки имплементации пока не
  открываю» — each opens separately behind the runtime-promotion
  gate: a named consumer + a measured native limit + the
  falsifier already pinned); CONTRACTS stays THE SINGLE REGISTRY
  (the iter-320 report §G's option (б) — the standing-over-cap
  form the permanent shape, the phases.md precedent; the header
  note landed). THE CONFIRMED QUEUE FULLY DISCHARGED AND ACCEPTED
  — all six contracts law (S/K/E/Q/P/A). KI#111's §5 cleanup
  executed (the Active-KIs list now empty). 2557+1 + ruff +
  docguard + topology --check clean. The RU report:
  docs/iterations/iter-322-acceptland-report.md.
Next: THE OWNER'S CALLS (nothing open on the agent side — every
  remaining row owner-gated): (0) THE STATION RUN FIRST — the owner
  runs canonsim_station_horizon_probe_v1.zip (preflight → sanity
  2y+T1 → control 100y paired → MAIN 1,000y paired; ~1.5–2.5 h; the
  zip comes back for the agent's kiloyear analysis: the whole arm's
  first deep datum + the kiloyear REALIZED_DELTA + the cross-hardware
  wall), then the Lab queue's remaining rows: the Stage B contract
  rows (transformation/wear/bounded sources — the measured
  falsifiers in hand), the scale-1 follow-up (the wall-cost
  decomposition: WHY the per-event cost grows at constant state — now
  a SHARPER named gap than the 2.5× herd question);
  (1) the implementation rows —
  sem-1/caus-1/replay-1/scale-1/speech-1/auth-1 each opens on the
  owner's separate call behind the runtime-promotion gate; (2) M2
  (the surface→canonical-ID normalisation A/B) the next
  measurement battery when the owner calls it — station-side,
  never a repo row; (3) the standing owner calls preserved: the
  replay-UI NOT-EXPOSED row, the world track's rows (W8's
  remaining), the frontend P1/P2/P3 continuation rows; (4) the
  probe-side fixture refinement (scene-relative fixtures or a
  distinct premise-drift status) when the owner calls it.
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
3. The station side: §8.5's ledger COMPLETE through the 27B band
   (iter-312/313/314 — the split instrument, the three round-7 rows,
   the 27B one-model run, the narrator arms, the cross-run
   reproducibility datum); the narrator production-form DECIDED
   2026-10-03 (L12 the production form — PRESENTATION_SPEC §7; the
   heavier arm gated behind the contract rows). The remaining owner
   calls: the probe-side fixture refinement (scene-relative fixtures
   or a distinct premise-drift status — the round-8 root cause) and
   M2 (the surface→canonical-ID normalisation A/B — a station
   battery, the motivating data the agreement columns, full never
   above 15/51); GET /models/sse the observed load-progress surface —
   a candidate row when a live consumer names it.
4. The standing frames: the embodiment options (§6.4 → §6.1 → §6.5 →
   §6.2 per the owner's 2026-09-27 order; §6.3 closed iter-204..210,
   its fill row removed), the debt-1 residues, the re-weigh's SALE,
   the runner's grudge surface (the standing order's first surface),
   the shave's temporal surface (the standing order's second), the
   SoW horizon (bg-6, owner-deferred — long-parked per the owner's
   2026-09-21 call). New rows enter on the owner's call only.

