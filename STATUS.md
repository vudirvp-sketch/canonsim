Iteration: iter-240 (`inf2-full-chip-library` — the owner's
2026-09-26 «результат вообще неудовлетворительный! Очень коряво,
криво и косо + далеко не все сэмплеры и настройки есть» call over
the inf-1 slice): the FULL chip library landed — 85 controls over
the 15 reviewed categories (the COMPLETE sampling surface —
Typical-P, Top-N-Sigma, the penalties family, the DRY family, the
XTC family, the Mirostat family, Dynatemp, Adaptive-P, Ignore EOS,
Logit Bias included — plus model/device/memory/loading/moe/cpu/
chat-reasoning/structured/server/observability/speculative/rope/
special/lora), the typed relations (the mirostat effective_noop
pinned from the --help's own words, the family requires), the
9-member chain (the inf-1 5-member profiles upgrade at load, the
operator's order preserved), the four §30 presets as transparent
diff-previewed documents, the workspace pinning (the profile
document's own workspace section), the DATA-DRIVEN Redot workspace
(inf-1's compose-before-read bug — the live flow rendering EMPTY
category groups — repaired; the search/pins/collapsible categories/
the advanced rung), the platform compile seam (SEMANTIC_FLAG_TABLE
+ build_semantic_command, the legacy command byte-stable, the
138-token duplicate-ownership guard); D-220; 14 paths.
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
(the obs family its live head per FRONTEND_UIUX_LAW §25, wb-13+ the
P2 continuation) + the world track + the SoW horizon, ROADMAP §2/§6) ·
2344 passed + 9 skipped, ruff clean, docguard clean (Python 3.12.14,
the env pin; the REDOT_EXE run green against redot-26.2-stable:
2352+1 — the eight visual packets (the seven + the inf-2 inference
capture: double-run byte-identical, VLM-verified — the pinned
chips, the collapsible categories with counts, the 9-member chain
with the INEFFECTIVE/INACTIVE states and reasons) + the duckdb skip
alone, per D6/D-093) ·
Date: 2026-09-26 ·
Scope: workbench/application/inference.py (the full library, the
relations, the presets, the workspace section) +
workbench/platform/llama_process.py (the semantic flag table +
build_semantic_command) + scripts/workbench_app.py (the semantic
compile path) + inference.gd (the data-driven workspace) +
strings.gd + the claim packets (test_inference/test_workbench_app/
test_managed_backend/test_shell_proof + the fake server's
token-scan parse) + the law/state docs (the LAW, FRONTEND_UIUX_LAW,
DECISIONS, TASKS, STATUS, worklog) — 14 paths (the 3–5 soft limit
honestly over, the inf-1 precedent, AGENTS §2.3; zero core change,
the LOG untouched).
Track A: the inf family the live head (iter-240 the full chip
library, 239 the inf-1 slice; inf-3+ the owner-gated continuation —
capability discovery, the model-driven context awareness, the
session/preset persistence layers, LLAMA_CPP_INFERENCE_CONTROL_LAW
§21); the obs family behind (iter-236 obs-2, 235 obs-1, 234 ux-1);
the wb family behind: iter-238 the KI#98 URL fix, 237 the corpus
re-homing, 232 the race/latch fixes + the OLED re-pin, 231
CI-unred + NavButton, 230 wb-12, 229 the visual law, 227 wb-10,
226 wb-9 D-208). The detail lives in the worklog + git.

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

- KI#98 · the iter-227 bind-URL forward shipped the gateway's endpoint (route included) as the Redot base URL — every shell request landed on /op/op (404: the dead session, the disabled picker, the undetected models; three symptom-level rounds before the root cause) · 2026-09-25 · CLOSED iter-238: the forwarded value is the ROOT (path stripped); the false test pin re-pinned over the real banner + the end-to-end root+"/op" POST pin.

## FAQ / Pitfalls

> One-liners + the owner link (NAV §3's duplication rule); the essays
> restated their named owners (doc-3). The operational recipes live in
> TECH_NOTES §14 (live-session) + §15 (corpus-regen).

- - **Read-side folds (echo/traits) never feed entropy/channel inputs (L6/EPIST-1, iter-46/55); the intent door is the only legal path** — DIRECTOR_SPEC §4; the one legal render: BRIEF_SPEC §3.5.
- **Every visual/UI row routes through docs/VISUAL_SYSTEM_UI.md FIRST (the surface-driven grammar, the token taxonomy, the state matrix, the §8 report; mechanisms not looks; the effective-state evidence law wins over quiet chrome) + its §11 companion routing (accessibility/keyboard/reduced-motion/responsive/localization — binding on every visual row, never silently dropped) — VISUAL_SYSTEM_UI §0/§6/§11 (admitted iter-229, D-211); every frontend INTERACTION/IA/selection/epistemic/accessibility/localization/responsive/Observatory question routes through docs/FRONTEND_UIUX_LAW.md FIRST (the interaction law owner, admitted iter-233, D-214); engine/API questions route through docs/REDOT_ENGINE_INDEX.md (D-207); application/runtime contracts (operations/lifecycles/identity/deadlines/streaming/persistence/inference) through docs/WORKBENCH_APP_LAW.md; Observatory analytical semantics (planes/World Question/query families/run identity/promotion gate) through docs/OBSERVATORY_LAW.md; world presentation/Scene IR/assets/LOD/degradation through docs/WORLD_PRESENTATION_LAW.md — all three D-218/iter-237, the v5.2 corpus re-homed, the external docs never needed again; every llama.cpp inference-control question (chips, scopes, AUTO, the sampler chain, relations, effective state, presets/recipes, capability versioning, the extra_args hatch) routes through docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md FIRST (D-219, inf-1 — the semantic core in workbench/application/inference.py; the profile store IS the §19.1 BASE PROFILE layer; the launch settings own DEPLOYMENT only after the one-way migration; chat's BASE temperature resolves through the resolver; the raw extra_args hatch never shadows a semantic control).**
- **Chronicle conditionals read FLAT context keys; a checked action's verdict is NESTED (`outcome.check.passed`, iter-43) — `render/tracery.py`; validator verdicts follow CURRENT canon never the anchor (iter-9; invented = contradicted, unmodeled = insufficient_data) — VALIDATION_SPEC §4–§5.**
- **Crossings fire in tick order (co-occurring: the coarsest clock first — macro → rotation → beat); director/urgencies ride the INTENT door, reactions the COMMIT door (D-037/38/39)** — BRIEF_SPEC §3.2/§3.3; KI#17 (git).
- **System passes scan the whole projection, never the seeding events (KI#16); the decay baseline = the last axis-changing event's tick via the (entity, prop) → tick index (KI#19, D-050)** — D-050's record.
- **Hardcoded `from_` is a desync (KI#13/KI#46): repeat effects idempotent; the carried-item position contract single-owned by `movement_changes`; the `_commit` gate fails loud before the write (D-035)** — `core/resolvers.py`.
- **INV-3's stoplist: no setting nouns in the ENGINE (`core/`+`sim/`+`brief/`, segment-matched, pack-tied word list); `render/`/`cli/`/`scripts/` are periphery (D-046)** — the stoplist test owns enforcement.
- **Malformed playscript steps raise RunnerError; well-formed but world-impossible intents emit `intent_rejected` (attempts are facts); urgency rejections stay silent** — PARSER_SPEC §4/§6.
- **Env-pinned verification cuts both ways: the golden T1 fixture byte-compares only on the generating interpreter (TEST_PLAN §1.1, §3 the migration); and PIPE-READING subprocess tests never lean on the host's PYTHONUNBUFFERED — the sandbox exports it, CI/owner machines do not (KI#93: three green-local/red-CI iterations) — the chain owns its buffering (`-u` child, line-buffered supervisor, the env-stripping spawn)** — tests/test_workbench_launch.py + TEST_PLAN §1.1
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

**iter-240 DONE: the FULL chip library + the honest workspace LANDED
(85 controls / 15 categories, the typed relations, the 9-member
chain, the §30 presets, the workspace pinning, the data-driven
Redot workspace, the platform compile seam; 2344+9 / 2352+1 REDOT +
ruff + docguard clean) — the inf-3+ continuation (capability
discovery, the model-driven context awareness, the session/preset
persistence layers) each an owner-gated row. iter-239 DONE: the
inf-1 vertical slice (superseded in surface quality by iter-240's
data-driven rebuild, its laws intact). iter-236 DONE: the obs-2 live run over the READ-side seam LANDED
(the bounded read model + observatory.gd v0.2's live feed, the
selection the EVENT ID, the honest empties) — 2308+8 (CI) / 2315+1
(REDOT_EXE) + ruff + docguard clean. iter-237 DONE: the v5.2 corpus
re-homed (D-218) — three new law owners + the repairs; the external
corpus never needs re-delivery. iter-238 DONE: KI#98 — the launcher's
forwarded bind URL is the ROOT (the /op route stripped; the dead
/op/op chain dead; the live circuit end-to-end green: discovery →
load → chat).**

1. The P1/P2/P3 continuation per FRONTEND_UIUX_LAW §25 (each row on
   the owner's call): obs-3+ — the P3 analytical rungs (timeline
   lanes, compare arms, semantic zoom, cross-highlighting — the
   interaction grammar per FRONTEND_UIUX_LAW §§5–7, the analytical
   contracts per OBSERVATORY_LAW §§11/18; the question EDITING form
   when its consumer names itself) · wb-13+ the visual rows (P2: the
   shell responsibility split continuing, per VISUAL_SYSTEM_UI §10,
   the chat ergonomics contract now LAW §21.1) — each row opens on
   the owner's call (the direction call already given for the
   family's order). The exported-Windows-build row (the owner's «по
   человечески сделать это нельзя?» — Workbench.bat's dev form is the
   editor binary running the project; the product form is an exported
   .exe over export presets, a row of its own) parked per AGENTS
   §2.4 — a named row when the owner calls it.
2. The remaining station rows (the owner's next engine run,
   TEST_PLAN §8.5's standing gaps + the wb-6 arm: the live-build
   /models/load + /models/unload re-verification against the
   b11064 station's ROUTER reality): the 27B GBNF parse arm + the
   one-model-constrained A/B (CONTRACTS §4.3 arm a) + the brief/
   parse component split; the narrator-convention call for live
   narrate play is two-sided now — more live beats at Q9B (size
   the tail) or the 27B as the one-model candidate (the §1 sweet
   spot, both doors) — the owner's choice (round 5's 12B + round
   6's 9B data: §13.1; bg-9's mapping-drift datum rides the same
   decision).
2. The standing frames: the embodiment options (the older units'
   rows — the step's notch record/hatch, the kin's own — each a
   future row's own call), the debt-1 residues (the crossing's
   own standing state the charcoalpaper precedent's sibling — the
   punt's purchase and the flood paper's fall still authored, each
   a future row's own call), the re-weigh's SALE (the heap's bloom
   drain — the withhold's own future row), the shave's temporal
   placement (the arc's assembly's remaining half — a future row's
   own call), the SoW horizon (bg-6, owner-deferred — long-parked
   per the owner's 2026-09-21 call). New rows enter on the
   owner's call only.
3. The intake-34/35/36/38 residues (each behind its own trigger,
   never a default): the ref-file deep record — a named row
   consuming a specific math-catalog or guide29 mechanism family
   (the per-card pass done at intake-35, the families re-confirmed
   at HEAD; Experiment 0's verdict + R1's landing close the other
   two residues — phases.md §6); the road-traffic depth-7 rider's
   evaluation grammar now carries intake-36's P01+P03 consult
   (capacity ≠ existence, the edge-perturbation discriminant, the
   fracture regime-change test — phases.md §6's intake-36 block);
   the intake-38 candidates (held-out transfer behind engine-1's
   corpus arms; the contract fields stopping-rule/spillover/
   nuisance behind the first claim packet that needs them —
   phases.md §6's intake-38 block, each behind its named first
   consumer, never a default).
