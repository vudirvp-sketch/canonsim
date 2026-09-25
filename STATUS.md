Iteration: iter-232 (`ki95-ki96-oled-repin` — the owner's
2026-09-25 report: the CI-red cancellation test + «проводник опять
сломался видимо, я не могу папки открыть и модели не показывает
языковые» + «цвет лучше взять темный под oled мониторы, но не синий
такой убогий»): TWO shipped defects + one owner-called re-pin.
KI#95 — the wb-9 cancellation test's single checkpoint() call RACED
the main thread's run.cancel dispatch: on a fast CI runner the worker
thread reached the checkpoint BEFORE the cancel landed, the
checkpoint passed, and the "unreachable" AssertionError closed the
run FAILED — the honest registry truth for an abort never requested
(production code truthful; a test bug — the local sandbox stayed
green on scheduling luck while CI went red); the fetch now POLLS the
checkpoint (the work contract's own observation surface, lock-free)
until the cancellation lands, bounded 20s — deterministic under any
thread scheduling. KI#96 — the Models surface's scan latch
(_models_requested) froze the discovery list after ONE successful
scan: GGUF files dropped into the folder by hand never appeared
without a manual Refresh (the owner's «модели не показывает» family);
the latch is retired — every surface entry re-scans (§20's routine
refresh; both reads cheap). theme@0.4 — the OLED re-pin (D-213, the
owner's explicit call over the external brief's "never pure black"
doctrine): the TRULY neutral ramp over the near-black #050505 (the
Catppuccin navy tint retired — «не синий») + the ONE teal accent
#4cc9a6 (the blue AND the older warm-orange families both rejected
by name); values-only — every token name, size and pin unchanged; 21
contrast pairs measured (scripts/contrast_check.py).
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
(the wb family its live head, wb-12 DONE + theme@0.4 the OLED re-pin
landed + the visual rows queued wb-13+) + the world track + the SoW
horizon, ROADMAP §2/§6) ·
2285 passed + 6 skipped, ruff clean, docguard clean (Python 3.12.14,
the env pin; the 5 REDOT_EXE-gated visual packets + duckdb skipping
clean per D6/D-093 — the sandbox binary absent) ·
Date: 2026-09-25 ·
Scope: tests/test_model_fetch.py (the deterministic checkpoint poll)
+ workbench/presentation/redot/scripts/shell.gd (the latch retired ×3
sites + the theme version string) + workbench/presentation/redot/
themes/workbench_theme.tres (the OLED re-pin) + tests/
test_shell_contract.py (the latch ban + the theme@0.4/base/accent
pins) + the state docs (STATUS/TASKS/worklog/DECISIONS) — 8 paths
(the 3–5 soft limit honestly over: two defects + the owner-called
re-pin + the pin updates + the state docs, AGENTS §2.3).
Track A: the wb family (iter-232 the race/latch fixes + the OLED
re-pin; wb-12 DONE + theme@0.4 — the visual rows queued wb-13+
per VISUAL_SYSTEM_UI §10; the prior record: iter-231 CI-unred +
NavButton, 230 wb-12, 229 the law admission, 228 wb-11 transport
chain, 227 wb-10, 226 wb-9 D-208, 225 the engine index D-207, 224
D-206, 223 wb-8, 222 wb-7, 221 wb-6, 220 wb-5, 219 wb-4, 218 wb-3,
216/215 wb-1). The detail lives in the worklog + git.

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

- (none — KI#95 + KI#96 opened + CLOSED iter-232 in the same row:
  KI#95 — the wb-9 cancellation test red in CI while the sandbox
  stayed green: the test's single checkpoint() call RACED the main
  thread's run.cancel dispatch — a fast CI runner's worker passed
  the checkpoint BEFORE the cancel landed, the fetcher's own
  "unreachable" AssertionError closed the run FAILED (the honest
  registry truth for an abort never requested: production code
  truthful, the TEST buggy — scheduling luck masked it locally);
  the test now POLLS the checkpoint (the work contract's own
  lock-free observation surface) until the cancellation lands,
  bounded 20s — deterministic under any thread scheduling, and an
  absent cancel fails loudly with its own honest cause.
  KI#96 — the Models surface's scan latch (_models_requested)
  froze the discovery list after ONE successful scan: GGUF files
  dropped into the folder by hand never appeared without a manual
  Refresh (the owner's «модели не показывает» family — wb-11's
  failed-scan re-arm applied to failure only, never to success's
  staleness); the latch is retired — every surface entry re-scans,
  the negative pin owns the ban.)

## FAQ / Pitfalls

> One-liners + the owner link (NAV §3's duplication rule); the essays
> restated their named owners (doc-3). The operational recipes live in
> TECH_NOTES §14 (live-session) + §15 (corpus-regen).

- **Read-side folds (echo/traits) never feed entropy/channel inputs (L6/EPIST-1, iter-46/55); the intent door is the only legal path** — DIRECTOR_SPEC §4; the one legal render: BRIEF_SPEC §3.5.
- **Every visual/UI row routes through docs/VISUAL_SYSTEM_UI.md FIRST (the surface-driven grammar, the token taxonomy, the state matrix, the §8 report; mechanisms not looks; the app spec's §18 evidence law wins over quiet chrome)** — VISUAL_SYSTEM_UI §0/§6 (admitted iter-229, D-211); engine/API questions still route through docs/REDOT_ENGINE_INDEX.md (D-207).
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
- **The Workbench runtime layout + the local model flow (wb-9/D-208 + wb-10): `workbench/runtime/` is the gitignored root — `models/` (the MODELS_ASSETS folder, auto-created), `llama.cpp/` (the drop folder; the launcher discovers llama-server.exe at its root or one folder deep, then PATH), `settings.json` (the persisted launch settings — corrupt/foreign-schema refuses loud), `launcher.json` (the launcher's own persisted Redot pick); the zero-command entry is `Workbench.bat` at the repo ROOT (double-click; the Redot FOLDER resolves its engine exe — the persisted pick, then REDOT_EXE, then the Desktop-shaped auto-scan, then the native folder picker once; `Workbench Setup.bat` re-picks; `scripts/workbench_launch.py` the same chain for the command form — run it from the repo ROOT, inside scripts/ the path doubles); a model ARRIVES by the native picker — the OS file/folder dialog hands ABSOLUTE paths to the gateway's `model.import` run (a local copy: `.part` + atomic rename, live progress, cooperative cancel — NO network, INV-4 untouched; the URL fetch stays the collapsed advanced row); `model.list`'s document carries `models_root` (the open-folder answer, never a local guess); `scripts/workbench_app.py` alone serves the gateway with MANAGED the default** — the modules' own docstrings + CONTRACTS §5's wb-10 note
- **The iter-232 laws: a cooperative-cancellation TEST never calls checkpoint() once and prays — the single call races the main thread's run.cancel dispatch (a fast runner's worker passes through, the "unreachable" guard closes the run FAILED; the sandbox stays green on scheduling luck while CI goes red — KI#95, three-form verified: sandbox, forced fast worker, delayed cancel); poll the checkpoint (the work contract's own lock-free observation surface — run.cancel is never starved) bounded until the cancellation lands, an absent cancel fails LOUDLY; discovery lists never freeze behind one-shot success latches — every surface entry re-scans (KI#96: the owner's hand-dropped GGUF must appear on the next Models entry; the wb-11 re-arm lesson generalizes from FAILURE to staleness — a "requested once" flag guarding the happy path is the bug, not the guard); and a theme re-pin is VALUES-ONLY — every token name, size and pin survives the palette swap (theme@0.4/D-213: the owner's OLED call over the external brief's "never pure black" doctrine — the neutral near-black ramp + the ONE teal accent, 21 WCAG contrast pairs measured)** — tests/test_model_fetch.py `_SlowFetcher.fetch` + shell.gd `_refresh_models` + test_shell_contract.py (the latch ban + the base/accent pins), iter-232
- **GDScript has NO implicit string-literal concatenation — two adjacent literals across lines are a Python-ism that refuses the whole file at parse (KI#91, iter-224's five sites); one literal per line; and any Redot/Godot engine question routes FIRST through `docs/REDOT_ENGINE_INDEX.md` (Redot 26.2 LTS pinned, Godot docs secondary cross-reference only; Redot 26.2 has NO `HTTPServer` — the app gateway stays Python-side; route to the smallest section, never read whole)** — test_shell_contract.py's adjacent-literal ban + the index §0/§21, D-207
- **The chat follow law (iter-230): read the scrollbar's max AFTER a frame — the autowrapped labels size late, reading it at call_deferred time is the short-scroll bug; TWEEN the bar's float `value` (never the int `scroll_vertical` jump); gate on near-bottom (SCROLL_FOLLOW_SLOP_PX) so a reader deep in history is never yanked; the late-layout re-settle stays bounded to ONE pass** — shell.gd `_scroll_to_bottom_smooth` (the owner's «не происходит плавной прокрутки вниз» call, the LM Studio/Discord follow mechanism)

## Next step

**iter-232 DONE: KI#95 (the CI-red cancellation test — the single
checkpoint() call raced run.cancel's dispatch; the poll form)
+ KI#96 (the Models scan latch — the owner's «модели не показывает»
family; every surface entry re-scans) + theme@0.4 (the OLED re-pin,
D-213 — «цвет лучше взять темный под oled мониторы, но не синий
такой убогий»; the neutral near-black ramp + the ONE teal accent)
LANDED (the owner's 2026-09-25 report; the wb family stays the
live head, wb-13+ the visual queue).**

1. wb-13+ per the visual queue (VISUAL_SYSTEM_UI §10 — the Models
   surface's matrix rendering over the wb-11 run circuits, then the
   Chat surface's semantic containers + composer states, then
   Settings) — the owner's call opens each row; the wb-14 remainder
   (the message containers' width/alignment grammar + the
   new-messages-below affordance + a reduced-motion setting) parked as
   the row's own scope. The exported-Windows-build row (the owner's
   «по человечески сделать это нельзя?» — Workbench.bat's dev form is
   the editor binary running the project; the product form is an
   exported .exe over export presets, a row of its own) parked per
   AGENTS §2.4 — a named row when the owner calls it.
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
