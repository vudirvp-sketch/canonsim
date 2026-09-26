Iteration: iter-260 (`temp-1` LANDING — the owner's 2026-09-26
  contract pick over the iter-257 fork card: **A2 + B2/B3, B1
  deferred**): A2 the crossing-family slicing contract PINNED as
  `tests/test_temp1_contract.py` (the declared tavern families
  count-invariant across [wait 720] vs [720 x wait 1] at the four
  measured seeds; the minimal pair projection + fingerprint
  invariance; the door families FREE with the seed-125 coerce flip
  and the seed-1001 cascade PINNED as the no-silent-scheduler-change
  guard); B3 the semantic-origin provenance LANDED through the
  existing primitive (`provenance.assignment_tick`, schema 0.2 -> 0.3
  additive over the cause_hook precedent — accepted AND rejected
  autonomous resolutions carry it, player intents never do), B2's
  runtime UNTOUCHED (the province_calendar witness still clusters
  all 265 talks in the last five ticks; the origins [1800, 516600]
  and the deferral latency <= 518269 now observable; `event.t` stays
  THE canonical timestamp); B1 generate-at-T DEFERRED behind the
  card's reopening conditions (phases.md §6's decision record — a
  PROPOSAL, never an implementation requirement); all five fixtures
  regenerated (TEST_PLAN §3 discipline: header bump + province 4 /
  road 1 / pressure 6 assignment_tick lines, every canonical field
  byte-identical to BASE — the pre/post comparison recorded in
  D-236's PCC); three hand-crafted version pins synced (test_smoke
  $id, test_semantic_diff's stale-version arm, test_observatory_read's
  derived expectation)
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
  the ladder complete 0..6 — the standing work: the owner-gated
  backlog (the ssi initiative COMPLETE at iter-241..252 except ssi-5,
  owner-gated — may never open) + the world track + the SoW horizon,
  ROADMAP §2/§6) ·
2421 passed + 9 skipped, ruff clean, docguard clean, topology
  --check clean (Python 3.12.14, the env pin; the REDOT_EXE-gated
  visual packets not run this session — no engine binary in the
  sandbox; the .gd layer untouched since iter-246, the D-093 skips
  unaffected) ·
Date: 2026-09-26 ·
Scope: core/{intent.py (IntentData.assignment_tick), loop.py (the
  enqueue-door stamp + `_provenance` + the two docstrings)} +
  schemas/event.schema.json (the 0.3 $id + the documented property) +
  docs/EVENT_SCHEMA.md (§1/§7/§8) + tests/{test_temp1_contract.py
  (new, 20 tests), test_smoke.py, test_semantic_diff.py,
  test_observatory_read.py (the three version-pin syncs),
  fixtures/*.jsonl (x5 regenerated)} + the state docs
  (STATUS/TASKS/worklog/DECISIONS/phases.md/TEST_PLAN) — 12 paths;
  R4 (D-236, the PCC record): one additive provenance field over the
  existing primitive, zero runtime-semantics change, the canonical
  outputs verified byte-identical to BASE.
Track A: the intake-40 instrument family COMPLETE — log-1 (iter-256),
  cov-1 (iter-258), div-1 (iter-259), temp-1 (iter-260: the research
  card + the owner's pick + the landing). The ssi family COMPLETE
  except ssi-5, owner-gated. The detail lives in the worklog + git.

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

- KI#101 · semantic_diff crashed on unequal-length field lists · CLOSED
  iter-259 (fixed + pinned)
- KI#102 · the dir-closure test's glob vs its committed-files law (red
  wherever scratch/ exists — KI#93's inverse) · CLOSED iter-259

(KI#100 deleted at this STATUS touch per the 2-iteration law — closed
iter-256)

## FAQ / Pitfalls

> One-liners + the owner link (NAV §3's duplication rule); the essays
> restated their named owners (doc-3). The operational recipes live in
> TECH_NOTES §14 (live-session) + §15 (corpus-regen).

- - **Read-side folds (echo/traits) never feed entropy/channel inputs (L6/EPIST-1, iter-46/55); the intent door is the only legal path** — DIRECTOR_SPEC §4; the one legal render: BRIEF_SPEC §3.5.
- **Every visual/UI row routes through docs/VISUAL_SYSTEM_UI.md FIRST (the surface-driven grammar, the token taxonomy, the state matrix, the §8 report; mechanisms not looks; the effective-state evidence law wins over quiet chrome) + its §11 companion routing (accessibility/keyboard/reduced-motion/responsive/localization — binding on every visual row, never silently dropped) — VISUAL_SYSTEM_UI §0/§6/§11 (admitted iter-229, D-211); every frontend INTERACTION/IA/selection/epistemic/accessibility/localization/responsive/Observatory question routes through docs/FRONTEND_UIUX_LAW.md FIRST (the interaction law owner, admitted iter-233, D-214); engine/API questions route through docs/REDOT_ENGINE_INDEX.md (D-207); application/runtime contracts (operations/lifecycles/identity/deadlines/streaming/persistence/inference) through docs/WORKBENCH_APP_LAW.md; Observatory analytical semantics (planes/World Question/query families/run identity/promotion gate) through docs/OBSERVATORY_LAW.md; world presentation/Scene IR/assets/LOD/degradation through docs/WORLD_PRESENTATION_LAW.md — all three D-218/iter-237, the v5.2 corpus re-homed, the external docs never needed again; every llama.cpp inference-control question (chips, scopes, AUTO, the sampler chain, relations, effective state, presets/recipes, capability versioning, the extra_args hatch) routes through docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md FIRST (D-219, inf-1 — the semantic core in workbench/application/inference/ (the package since ssi-4); the profile store IS the §19.1 BASE PROFILE layer; the launch settings own DEPLOYMENT only after the one-way migration; chat's BASE temperature resolves through the resolver; the raw extra_args hatch never shadows a semantic control); every SSI / risk-class / proof-carrying-change / ssi-phase question routes through docs/ssi/SSI_OVERLAY.md FIRST (D-222, ssi-2 — the block matrix + the rule subset + the phase ladder; the risk ladder's binding home AGENTS §2.9); every topology / module-ownership / co-change / god-object / read-seam question routes through docs/SSI_TOPOLOGY.md FIRST (D-224, ssi-3 — the 82-module map + the audit verdicts + the phase consequences; scripts/topology.py the instrument).**
- **Chronicle conditionals read FLAT context keys; a checked action's verdict is NESTED (`outcome.check.passed`, iter-43) — `render/tracery.py`; validator verdicts follow CURRENT canon never the anchor (iter-9; invented = contradicted, unmodeled = insufficient_data) — VALIDATION_SPEC §4–§5.**
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
- **The Workbench runtime layout + the local model flow (wb-9/D-208 + wb-10): `workbench/runtime/` is the gitignored root — `models/` (the MODELS_ASSETS folder, auto-created), `llama.cpp/` (the drop folder; the launcher discovers llama-server.exe at its root or one folder deep, then PATH), `settings.json` (the persisted launch settings — corrupt/foreign-schema refuses loud), `launcher.json` (the launcher's own persisted Redot pick); the zero-command entry is `Workbench.bat` at the repo ROOT (double-click; the Redot FOLDER resolves its engine exe — the persisted pick, then REDOT_EXE, then the Desktop-shaped auto-scan, then the native folder picker once; `Workbench Setup.bat` re-picks; `scripts/workbench_launch.py` the same chain for the command form — run it from the repo ROOT, inside scripts/ the path doubles); a model ARRIVES by the native picker — the OS file/folder dialog hands ABSOLUTE paths to the gateway's `model.import` run (a local copy: `.part` + atomic rename, live progress, cooperative cancel — NO network, INV-4 untouched; the URL fetch stays the collapsed advanced row); `model.list`'s document carries `models_root` (the open-folder answer, never a local guess); `scripts/workbench_app.py` alone serves the gateway with MANAGED the default; the launcher's forwarded URL is the ROOT (scheme://host:port — the banner's `/op` route STRIPPED, KI#98/iter-238: gateway_client.gd owns the route and appends `/op` itself; a route inside the forwarded value doubles to /op/op → 404, the dead-session chain)** — the modules' own docstrings + CONTRACTS §5's wb-10 note
- **The iter-232 laws: a cooperative-cancellation TEST never calls checkpoint() once and prays — the single call races the main thread's run.cancel dispatch (a fast runner's worker passes through, the "unreachable" guard closes the run FAILED; the sandbox stays green on scheduling luck while CI goes red — KI#95, three-form verified: sandbox, forced fast worker, delayed cancel); poll the checkpoint (the work contract's own lock-free observation surface — run.cancel is never starved) bounded until the cancellation lands, an absent cancel fails LOUDLY; discovery lists never freeze behind one-shot success latches — every surface entry re-scans (KI#96: the owner's hand-dropped GGUF must appear on the next Models entry; the wb-11 re-arm lesson generalizes from FAILURE to staleness — a "requested once" flag guarding the happy path is the bug, not the guard); and a theme re-pin is VALUES-ONLY — every token name, size and pin survives the palette swap (theme@0.4/D-213: the owner's OLED call over the external brief's "never pure black" doctrine — the neutral near-black ramp + the ONE teal accent, 21 WCAG contrast pairs measured)** — tests/test_model_fetch.py `_SlowFetcher.fetch` + shell.gd `_refresh_models` + test_shell_contract.py (the latch ban + the base/accent pins), iter-232
- **GDScript has NO implicit string-literal concatenation — two adjacent literals across lines are a Python-ism that refuses the whole file at parse (KI#91, iter-224's five sites); one literal per line; `static func tr(` is likewise a parse refusal (Object's native signature — the strings.gd resolver is `lookup`, iter-234); every user-facing string rides the `_tr` boundary (strings.gd en/ru, LAW §17 — a new literal in shell.gd fails the boundary scan); and any Redot/Godot engine question routes FIRST through `docs/REDOT_ENGINE_INDEX.md` (Redot 26.2 LTS pinned, Godot docs secondary cross-reference only; Redot 26.2 has NO `HTTPServer` — the app gateway stays Python-side; route to the smallest section, never read whole)** — test_shell_contract.py's adjacent-literal ban + the index §0/§21, D-207
- **The chat follow law (iter-230): read the scrollbar's max AFTER a frame — the autowrapped labels size late, reading it at call_deferred time is the short-scroll bug; TWEEN the bar's float `value` (never the int `scroll_vertical` jump); gate on near-bottom (SCROLL_FOLLOW_SLOP_PX) so a reader deep in history is never yanked; the late-layout re-settle stays bounded to ONE pass** — shell.gd `_scroll_to_bottom_smooth` (the owner's «не происходит плавной прокрутки вниз» call, the LM Studio/Discord follow mechanism)

## Next step

**iter-260 DONE: the temp-1 LANDING over the owner's contract pick
(A2 + B2/B3, B1 deferred) — the crossing-family slicing contract
pinned (test_temp1_contract.py), the semantic-origin provenance landed
(provenance.assignment_tick, schema 0.3), B2's runtime untouched (the
clustering witness byte-verified), B1 deferred behind the card's
reopening conditions; the five fixtures regenerated with every
canonical field byte-identical to BASE. 2421+9 + ruff + docguard +
topology --check clean.**
iter-257/258/259 DONE: the intake-40 instrument session — the fork
card + cov-1 (D-234) + div-1 (D-235) + KI#101/102 closed.
iter-255+256 DONE: the intake-40 routing (D-233) + KI#100 closed.
iter-251/252 DONE: the ssi tail phases 6+7 (D-229/D-230).
iter-241..250 DONE: the ssi foundation + phases 1..5 + KI#99
(D-221..D-228).
1. The B1 architectural follow-up (generate-at-T) stays DEFERRED and
   OWNER-GATED — reopened only on the card's five conditions
   (phases.md §6's decision record: a named runtime consumer, a
   repeatable material failure, a measured product-level gap beyond
   B2+B3, the scheduler shown a native limitation, an owner/phase
   gate on the temporal-law change). ssi-5 stays owner-gated (the
   N018 evidence law). The owner-side cleanup standing from D-230's
   third card: delete the doubled `workbench/workbench/runtime/` tree
   locally (safe — the iter-246 root fix landed; the tree regenerates
   on demand).
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
4. The standing frames: the embodiment options, the debt-1 residues,
   the re-weigh's SALE, the shave's temporal placement, the SoW
   horizon (bg-6, owner-deferred — long-parked per the owner's
   2026-09-21 call). New rows enter on the owner's call only.

