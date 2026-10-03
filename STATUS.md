Iteration: iter-312 (`stationlive` — the owner's 2026-10-03
  delegation «дорабатывай прошлую итерацию и делай что должно,
  разрешаю. мне нужно качество и отсутствие костылей» + the repeated
  llama.cpp enabler «можешь устанавливать llama.cpp для работы и
  прочее окружение» — iter-311's deferred live inference row fired):
  the LIVE STATION ROW at the sandbox band (b11337 in the documented
  drop layout `workbench/runtime/llama.cpp/`, both models through the
  gateway's OWN model.fetch — the proven flow). CLOSED LIVE: (1) THE
  BRIEF/PARSE COMPONENT SPLIT + the heartbeat's FIRST FULL-COLUMN ROW
  (engine1-q1p7b — the 51-utterance corpus through the real mode-C
  stack at Qwen3-1.7B, the landed cycle mirrored verb-for-verb, the
  five-component clock: raw validity 51/51 with zero re-asks, mix
  51/0/0, agreement 4/15/32, tick 0.3/0.5 · fold 0.8/0.9 · brief
  0.9/1.1 · parse 2.7/3.4 · generate 11598/12512 ms; the determinism
  mini greedy/seeded/cacheless ×3 byte-identical, one across-priming
  cache flip honestly recorded; the manifest's parse_grammar_id
  byte-equal to round 5's station id); (2) THE WB-6 ARM — POST
  /models/load + /models/unload re-verified live through the repo's
  own adapter (router-mode-only at b11337; the unload matches the
  stub pins exactly; the load takes the REGISTRY STEM never a path;
  OpenAI-style 400/404 envelopes, the terminal-HTTP mapping correct;
  GET /models/sse observed as the new live-status surface — parked a
  candidate row; the §13.1 router laws all held). HELD OPEN honestly:
  the 27B GBNF parse arm + the one-model-constrained A/B — owner-side
  hardware rows (the sandbox's 4.1 GB RAM cannot host a 27B Q4_K_M)
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
  the ladder complete 0..6 — the standing work: the owner-gated
  backlog + the web-frontend track + the world track + the SoW
  horizon, ROADMAP §2/§6) ·
2556 passed + 1 skipped, ruff clean, docguard
  clean, topology --check clean (Python 3.12.14, the env pin; one
  adapter docstring/module-note refresh — zero behavior change, the
  live evidence doc-side) ·
Date: 2026-10-03 ·
Scope: docs/TEST_PLAN.md (§8.5 the engine1-q1p7b row + the split
  discharge), docs/TECH_NOTES.md (§13 the iter-312 record),
  cli/engine.py (the module note + the load_model docstring — the
  b11337 measured reality, comment-only), docs/TASKS.md (the ledger),
  STATUS.md, worklog.md (the iter-312 entry, iter-302 evicted),
  docs/iterations/iter-312-stationlive-report.md (new — this row's RU
  report) — 7 changed/created (6 modified + 1 created); R0/R1
  verification — the substance the live session's evidence (the
  runner + the probes outside the repo, Rule 9), zero engine behavior
  change, INV-1..5 untouched, the LOG untouched, zero corpus price;
  NO test deleted or weakened
Track A: the web-frontend track — S0 LANDED; the tooling floor's
  first row + the V1/V2/V3 visual floors LANDED (iter-293/297/
  304/307); Phase 3's SEVEN rows LANDED
  (iter-294/295/296/298/299/300/301) + the IA REPAIR LANDED
  (iter-297, D-247); the owner-side bands CLOSED LIVE (iter-302)
  and RE-CLOSED LIVE inside the matrix session (iter-308); THE
  STREAMING ADMISSION LANDED (iter-305/306); THE FULL ACCEPTANCE
  MATRIX CLOSED (iter-308 — 39 verified / 2 open / 1 partial /
  2 not-exposed, zero defects); THE TOOLING FLOOR'S CI + SMOKE
  ROWS LANDED + THE BOOT-TIME OBSERVED-SYNC LANDED (iter-309 —
  iter-308's two OPEN rows and the §C candidate all closed; the
  smoke NOT in CI by the owner's row spec — the owner-side/sandbox
  `npm run e2e`); THE STANDING QUEUE DISPOSITIONED + THE DECISIONS
  COLLAPSE LANDED (iter-310, D-250 — the 40→30 collapse with the
  docguard section-form tooth; the B1/C4 law diffs CLOSED WITHOUT
  DIFF — both verdicts already measured; the pixel-diff row
  POSTPONED — a real visual-regression pipeline when a live need
  names it, the token-guards + the live screenshots stand); the
  next frontend rows the owner's call: the replay-UI NOT-EXPOSED
  row; the standing boundaries: a SharedWorker stream transport,
  Tauri, PWA, the Settings Appearance section (no persisted store)
  — each its own admission (the import form's native file/folder
  picker rides the Tauri row). The world track: W8's remaining
  rows the owner's call. The ssi family COMPLETE except ssi-5,
  owner-gated.



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

- KI#110 · the launch-params merge test assumed an empty llama.cpp discovery
  home (the documented drop → red); pinned hermetically · CLOSED iter-302

(none further — KI#109 deleted at the iter-301 §5 cleanup: closed
  iter-294, seven iterations past the 2-iteration deletion rule; its
  substance verified resolved at the current mirror HEAD — the 16
  D-245 deletions all present, the architecture suite green; the
  iter-303 audit's CI-trigger suspicion was RETRACTED at the byte
  layer — a rendered-output artifact, never a repo defect — the
  report's §D)

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

**iter-312 DONE: stationlive (the owner's 2026-10-03 delegation
  «дорабатывай прошлую итерацию и делай что должно, разрешаю» + the
  llama.cpp enabler — iter-311's deferred live inference row).** TWO
  standing rows CLOSED LIVE at the b11337 sandbox band: the
  BRIEF/PARSE COMPONENT SPLIT — the heartbeat's first full-column row
  engine1-q1p7b (TEST_PLAN §8.5; the 51-utterance corpus at
  Qwen3-1.7B, raw validity 51/51, the five-component latency split,
  the determinism mini ×3 byte-identical in all three arms); the WB-6
  ARM — POST /models/load + /models/unload re-verified through the
  repo's own adapter (router-mode-only at b11337, the stem-not-path
  load semantics, the success-form unload matching the stub pins, the
  terminal-HTTP mapping correct; GET /models/sse the observed new
  surface, parked a candidate row). 2556+1 + ruff + docguard +
  topology --check clean (R0/R1 — the adapter's comment-only refresh,
  zero behavior change). The RU report:
  docs/iterations/iter-312-stationlive-report.md.
Next: the owner's calls — (1) the standing queue: the replay-UI
  NOT-EXPOSED row and the world track's parallel rows (the queue's
  three other rows dispositioned by the same 2026-10-03 call,
  D-250: the collapse LANDED iter-310; B1/C4 CLOSED WITHOUT DIFF —
  both iter-303 verdicts already measured; pixel-diff POSTPONED —
  a real visual-regression pipeline when a live need names it).
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
3. The remaining station rows (the owner's next engine run —
   OWNER-SIDE HARDWARE rows after iter-312: the 27B GBNF parse arm +
   the one-model-constrained A/B, CONTRACTS §4.3 arm a — the sandbox's
   4.1 GB RAM cannot host a 27B Q4_K_M; the row runs at the owner's
   GPU station with the landed split instrument ready to reuse);
   DISCHARGED iter-312: the brief/parse component split (the
   engine1-q1p7b row, TEST_PLAN §8.5) + the wb-6 live re-verification
   (TECH_NOTES §13's iter-312 record); the narrator-convention call
   for live narrate play is two-sided now — more live beats at Q9B
   (size the tail) or the 27B as the one-model candidate (the §1
   sweet spot, both doors) — the owner's choice (round 5's 12B +
   round 6's 9B + iter-312's 1.7B data: §13/§13.1; bg-9's
   mapping-drift datum rides the same decision; GET /models/sse the
   observed load-progress surface — a candidate row when a live
   consumer names it).
4. The standing frames: the embodiment options (§6.4 → §6.1 → §6.5 →
   §6.2 per the owner's 2026-09-27 order; §6.3 closed iter-204..210,
   its fill row removed), the debt-1 residues, the re-weigh's SALE,
   the runner's grudge surface (the standing order's first surface),
   the shave's temporal surface (the standing order's second), the
   SoW horizon (bg-6, owner-deferred — long-parked per the owner's
   2026-09-21 call). New rows enter on the owner's call only.

