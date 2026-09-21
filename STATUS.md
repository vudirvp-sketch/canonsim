Iteration: iter-171 (`iter-171-engine1a` — the {3–8B, GBNF} experiment
CONVENED, the owner's «за 1 раз как можно больше тестов… лучше вообще
выяснить все про llama.cpp и дальше уже разбирайся на своих
мощностях» call): the Rule-9 runner DELIVERED outside the repo (the
Vantiel-handoff pattern — engine1_runner/grammar/battery + the
runbook, never committed) — ONE batched owner session covering the
TEST_PLAN §8.5 gap rows (the 51-utterance corpus raw → one re-ask,
the deviation families F1–F6 with the guess-within-grammar tally,
the bg-7 prose families (ii)–(v), the per-component p50/p95 columns
tick/fold/brief/parse/generate) + CONTRACTS §4.3's four arms (one-vs-
two-model, seeded-local determinism, the GBNF latency penalty, mode-A
prose at the weak arm) + the §13 surface probes at the owner's build.
Sandbox-validated END-TO-END FIRST on the owner's exact llama.cpp
build (b11064, commit a894dae93, CPU-side): every arm smoke-run
through the REAL doors — raw GBNF gate validity 100% at the smoke cut
(shape errors structurally impossible; the honest guess-within-
grammar class remains), the mediator prose ladder + the C3.5
degraded-knows probe live, the per-component latency columns
populated. TECH_NOTES §13.1 the sandbox surface block: the router
(model swap = autoload/eviction, never a restart), POST /props the
measured silent no-op, the -np context split at b11064, GBNF on the
chat route (top-level grammar param), the GBNF dialect facts
(underscore rule names rejected; [ ] is a char class), cross-model
thinking×schema mechanics, the determinism mini 5/5, cancellation vs
a second client, restart timing — every software-bound §13 "not
established" item closed; the station-bound list narrowed to the
owner's run. The owner's move: the one run (`--arm all`), the bundle
back — then the transcripts re-distill (§8.2 source 3), the
heartbeat's first local row, presentation-1's local evidence, and the
build landing (b) stays the next owner gate. Zero engine code in the
repo; INV-4 UNCHANGED.
Phase: 6 (Packs & worldbuilder) — CLOSED (gate PASS iter-116, D-151;
the ladder complete 0..6 — the standing work: the owner-gated backlog
+ the world track + the SoW horizon, ROADMAP §6) ·
1900 passed + 1 skipped, ruff clean (Python 3.12.14, the env pin;
verified at BASE_COMMIT 04c8a5f BEFORE working — 1900+1 green, ruff
clean, the iter-170 pin re-confirmed — and re-verified after with the
diff in place: 1900+1, ruff clean, doc-only, zero test change, the
golden fixtures byte-untouched) ·
Date: 2026-09-21 ·
Scope: docs/TASKS.md (the engine-1 row's move (a) CONVENED + the
ledger line) + docs/TECH_NOTES.md (§13.1 the sandbox surface block —
measured substance only; 938 lines — over the 600 docs cap, the
pre-existing 854 + pure measured evidence, the §6.1 law) +
`STATUS.md` (this re-pin) + `worklog.md` (this entry). The prior
iteration's record: iter-170 (engine-1). The detail lives in the
worklog + git.

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
- INV-4 LLM boundary: no LLM/network calls in track A — executable against
  every package dir incl. `scripts/` since iter-6a (D-046).
- INV-5 Log immutability: committed logs are never edited; corrections are
  new events.

## Active KIs

- KI#88 · CLOSED iter-169 (qa2): the lint-side closure landed — the on_action actor vocabulary narrowed to `world | source_actor` (ACTOR_KEYS, owned by core/onaction.py; the reaction event's actor is a schema-required string), and the target-sourced check row pins the intent's target via the door's own `needs_target` predicate; the runtime asserts stay the programmatic backstops.
- KI#89 · CLOSED iter-169 (qa2): the shared `lint_direct_keys` row (the lint_echo_cond family) refuses the five record-reading tests' directly-indexed keys at every `requires` declaration site — presence + type + non-emptiness; a malformed pack KeyErrors mid-run no more.

## FAQ / Pitfalls

- **The read-side folds (echo, traits) are gated by L6 — NEVER entropy
  inputs (iter-46 law; the traits twin iter-55).** The psychological
  residue (`core/echo.py`) and the crystallized beliefs
  (`core/traits.py`) are knowledge-derived per-NPC read models: the
  intent door's `echo_at_least` gate may read the echo (behavior
  selection, the P2b consumer), and the traits feed the brief's
  derived-trait read — LIVE since iter-56/leg-2 (BRIEF_SPEC §3.5:
  the PC's beliefs lead the recalled_facts block, the family records
  render nothing raw, `expand_trait` the demand side) — but the
  DIRECTOR may not read either: narrative entropy reads observable
  state only (DIRECTOR_SPEC §4, L6/EPIST-1), and a score or belief
  folded from an NPC's private knowledge records is not observable
  state. Wiring a fold into `entropy` (or any channel input) would
  make the director read minds through a derived number — an
  invariant-grade bug that would look like a tuning change. Same
  fence for the chronicle: the folds render nothing (the brief's
  belief line is the fold's one legal render — a read-side document,
  not canon); the behavior a fold gates (the intent's own event) is
  the only legal canon visibility. The flip side (the B3 trap's
  record, iter-66): gating behavior through the INTENT door is legal
  and precedent-backed — a `trait_held` requires-leaf may arm or
  disarm an urgency entry (a GATE, never a probability multiplier;
  p=100 is compulsion semantics, the content-5/iter-51 form — one
  leaf, two legal uses). The fence is directional: folds flow into
  behavior selection through the door, never into channel inputs —
  and the predicate layer must receive the fold through its declared
  projection parameter, never by reaching into the fold modules.

- **Chronicle conditionals read FLAT context keys; the action check
  outcome is NESTED (iter-43 law).** `{cond?a|b}` addresses
  `context[cond]` — a one-level flat lookup (`render/tracery.py::
  _expand_brace`); an action event's check result lives at
  `outcome.check.passed`, unreachable by the conditional (a missing
  key silently takes the else arm — a wrong-arm line is a LIE in the
  chronicle, never an error). The house carrier for a checked
  action's verdict is the BRANCH EVENT TYPE (take/take_failed,
  flee/flee_caught — and document_check/document_check_failed since
  iter-43): each type owns its template line, no conditional needed.
  Top-level outcome fields (arrest_resolved's `caught`, rumor_told's
  `accepted`) are the ONLY legal conditional keys.


- **Validator verdicts follow CURRENT canon, never the anchor (iter-9
  law).** Verdicts are computed against the full log; the OCC anchor only
  decides fresh/stale/rebased and the first-break attribution
  (knowledge and events only grow — only `state` claims can flip via
  staleness; a claim false at the anchor but true now is SUPPORTED).
  Closed world: an invented entity/event is `contradicted` (the
  invented-facts metric), an unmodeled prop is `insufficient_data` —
  canon never fabricates an opinion. Owner:
  `docs/VALIDATION_SPEC.md` §4–§5. The call-budget reconciliation
  (2-call steady state; 3-call regen worst case) is §7 — regen_count is
  a first-class metric, never absorbed silently.

- **The queue + door laws (D-037/D-038/D-039).** Crossings fire in
  tick order, never by type: rotations, beats and (since maclock-1)
  the macro-clock interleave by tick, the loop picks `min(candidates)`
  per iteration, the writer's tick-monotonicity invariant forbids
  out-of-order commits (the read-side mirror: `brief/assembler.py`'s
  `last_beat_tick`/`beats_crossed` reproduce the same beat set —
  BRIEF_SPEC §3.2, tested). At a CO-OCCURRING tick the coarsest
  clock fires first (macro → rotation → beat — the calendar contains
  the day, the day contains the beat). Autonomous
  (urgency/director) intents enqueue at `entry.tick`, never beat_tick
  (sub_order NPC_REACTION), decay commits directly at beat_tick, and
  the runner feeds the next
  playscript step only on the PLAYER's own step endings (KI#17). The
  two doors: director releases and urgencies ride the INTENT door
  (a released hook = IntentData `director_<N>`/`urgency_<N>` through
  the front door; rejections emit `intent_rejected` no-ops with
  `cause_intent`; the director never bypasses Intent→Event) —
  reactions ride the COMMIT door: `_commit` feeds the knowledge
  index + runs `_react` for EVERY committed event (no call site can
  forget a reaction; cascades terminate; suspicion reacts only to
  tokens the knower did not already hold; the arrest resolution
  rides the same door). The macro turn rides the COMMIT door at its
  crossing (the rotation's world-schedule precedent — no queue band,
  the bands are for actor ordering).
- **System passes scan the whole projection, not the events that seeded
  them (KI#16 lesson).** Per-layer bookkeeping must be global and
  mergeable by new ignitions, never a frozen snapshot in the queue
  payload. The decay pass scans ALL npcs; its per-axis baseline is the
  tick of the LAST event that changed that axis (KI#19) — read from
  the derived `(entity, prop) → tick` index since iter-8h (D-050),
  not from a log scan.
- **Hardcoded `from_` is a desync waiting to happen (KI#13 lesson;
  KI#46 is the same family).** Read current values from the projection;
  make repeat effects idempotent; the `_commit` gate (D-035) fails loud
  BEFORE the write. KI#46's clause: every position writer must carry
  the items — the carried-item position contract (item position ==
  carrier position) is single-owned by `movement_changes`
  (core/resolvers.py); a mover that swaps positions by hand leaves the
  `from_` desync armed and the presence fold reading the lie.
- **INV-3's stoplist scope (iter-2 interpretation, test-owned; D-046;
  +`brief/` since iter-10a, KI#38).** The stoplist bans setting nouns
  in the ENGINE (`core/`+`sim/`+`brief/` — the mediator circuit is
  engine-side: pure functions of (log, ledger, pack)), segment-matched;
  mechanic words stay legal; the word list is pack-tied by a self-check.
  `render/`/`cli/`/`scripts/` are periphery — pack path strings, CLI help
  examples, docstring prose live there by design (INV-3's substance: a
  second pack requires zero ENGINE changes).
- **The loud/soft front-door line.** Malformed playscript steps raise
  `RunnerError` — author bugs crash. Well-formed but world-impossible
  intents emit `intent_rejected` no-ops — attempts are facts. Director
  rejections emit events (budget consumed); urgency rejections stay
  silent (the world's noise floor absorbs them).
- **The golden T1 fixture is env-pinned; the fixture-regeneration guard
  is the iter-6 discipline (TEST_PLAN §1.1).** The header records the
  Python version — byte-compare only on the generating interpreter;
  regenerate + commit the fixture with env changes. The guard pins (a)
  the fixture header's `schema_version` == the current schema `$id`
  version, (b) a fresh regen byte-diff — a breaking schema change
  without fixture regen fails loudly (§3 migration procedure).
- **Doc drift is evidence, not prescription — and every fact has ONE
  owner (D-024/D-027).** Verify drift with `git log -S` AND the
  pinning test before acting (KI#42/KI#48: a ref citing a section it
  never contained, a reported-but-unlanded pass, a behavior claim
  without its pinning test — archives are ephemeral, git is real;
  KI#51: external-paper figures are drift until fetched; KI#80:
  landing counts — files, entries, suites — are re-counted against
  `git show --stat` before the stop-point report, a count asserted
  from the plan is drift at write time). Three
  places, three jobs: `REFERENCES.md` catalogs;
  `docs/ref/<source>.md`
  carries mechanics; `BLUEPRINT.md` + `docs/blueprint/` carry
  resolutions. Link, never restate; cite ledger row IDs (e.g. "per
  RNG-1"). The audit method: grep a sample of ledger terms across
  the planning docs — every term must land in at least one (verified
  iter-0x; the ref-graveyard diagnostic). External session
  prompt-cards (bootstrap texts) age the same way: on any conflict,
  AGENTS §4/§6, the DECISIONS rows and the repo's own bytes own the
  truth — a bootstrap text is a convenience copy, never a second
  source (the 2026-09-06 research session's four confirmed
  conflicts — the cap, the phase frame, the RNG law, the
  dependencies — none worth a KI; the record lives here).

- **Live sandbox session recipes — narrate + say (operational; iter-24/
  31/32; merged per KI#54 — one session, two doors sharing one ledger,
  D-049).** `python -m cli` opens the interactive session. **narrate**
  (the narrator door, phase 1; the owner's iter-24 directive to make
  the recipe durable): `narrate
  [<reply.json> | dry]`. `emit_call` writes `output/mediator/call_NNNN.md`
  (gitignored runtime); the operator reads the brief +
  `narrator_protocol`, composes a reply JSON `{prose, texture_delta?,
  proposal?}` with `expected_event_seq` = the anchor advertised in the
  protocol (an int; `'anchor'` resolves to it in the corpus), writes it
  to a path, and applies via `narrate <reply>`. The beat cycle:
  `commit → retire_contradicted → sync_scene → assemble → narrator
  reply → apply_delta → intents → mark_promoted`; a refused document
  (delta refusals or contradicted claims) regens the WHOLE beat; the
  L12 ladder: narrator → template (the beat's own chronicle lines) →
  dry. Sandbox specifics (pitfalls fixed once, never re-derived): (1)
  `pip install --break-system-packages -e ".[dev]"` (the PEP-668
  fence); (2) `python -m pytest` — the flat packages
  (`core`/`brief`/`render`/`cli`/`sim`) are not on PATH, bare `pytest`
  fails with `ModuleNotFoundError`; (3) `output/` and `logs/` are
  gitignored runtime artifacts — never stage (`git status --short`
  before every commit); (4) the call/reply paths are runtime, so a
  runner script outside the repo (e.g.
  `/home/z/my-project/scripts/iterNN_runner.py`, Rule 9) is the
  reproducible way to drive multi-beat sessions — read each call body,
  hand-compose the reply, apply, harvest the `BEAT` summary lines
  (KI#44) to pin `notes_contains` for the distilled corpus cases.
  Batch boundaries are world-defining for the corpus (iter-23 lesson,
  kept here): `run_steps` drains the queue to exhaustion between
  batches, but steps inside ONE batch interleave with pending clock
  crossings by tick (D-038); a distilled case must reproduce the live
  batch structure — the intent-carrying beat (the door's own
  `run_steps` batch) plus `between` steps are the corpus's vocabulary
  for it; the test's `between` runs post-call, so its reply rides a
  stale anchor through the rebase path (sessions 6/8's noise/arson
  cases pin the rebased rotation beat live). (5) The `'anchor'`
  placeholder is corpus-test sugar — the LIVE operator writes the
  advertised anchor as an integer (a placeholder left in a live
  reply is a MALFORMED catch at the boundary's shape gate, iter-25
  session 10's first probe: `expected_event_seq must be a
  non-negative integer, got 'anchor'`); a runner that resolves the
  placeholders itself duplicates what the corpus test's
  `_resolve_anchors` does. A late door batch can jump the clock far
  past the crossing: the arson's follow-up cascade drains inside the
  door's own `run_steps` batch (location_burned_out t=533), so the
  NEXT intent (the flee) starts at t=533, not at the arson's
  t=413 — the distilled case must carry the fire cascade inside the
  same batch structure (session 10's seed-93 cases). **say** (the parse
  door, phase 2, iter-31/D-062): `say <free text>` →
  `output/parser/parse_NNNN.md` (utterance +
  grammar + protocol; gitignored runtime), the operator composes the
  reply JSON — exactly ONE of `{"intent": {"kind", "target"?,
  "fields"?}}` (on-grammar: kind a listed verb, target a listed noun,
  only listed fields with listed values; the texture field copies a
  live texture entry's `{entry, scope, slot, value}` verbatim, no
  target — one path per intent), `{"question": "..."}` (uncertainty
  is asked, never guessed), or `{"no_intent": "..."}` — and applies
  via `say apply <reply>`. The gate is loud: off-grammar output
  raises ParseError at the boundary (printed, nothing feeds, the
  cycle stays open — fix the reply file and re-apply); a
  door-rejected attempt still commits `intent_rejected` (attempts are
  facts — parse validity ≠ world legality); a texture reference pins
  its entry BEFORE the feed (the reference IS the pin — a failed
  attempt keeps it live+pinned). The parse corpus recipes mirror the
  narrator's: a runner script outside the repo
  (`/home/z/my-project/scripts/iterNN_runner.py`, Rule 9) reading
  each call, hand-composing replies, harvesting `[parsed intent fed`
  lines. Contract owner: `docs/PARSER_SPEC.md`. iter-32 lessons (six
  sessions through the real stack, both doors on one ledger): a
  PROMOTED texture entry is TERMINAL — a reply referencing it is
  off-grammar at the gate ("not a live texture entry"), the parser
  takes the disambiguation path; un-pinning does not exist and neither
  does re-referencing. `take_failed` joins `intent_rejected` in the
  world-answer family (attempts are facts; PARSER_SPEC §6 tallies them
  apart from parse validity). The door-batch law reproduces through
  `say`: the fire cascade drains inside the door's own `run_steps`
  batch (5 events for one drop_break cycle) — distilled cases carry
  the batch structure, exactly as the narrator corpus does. iter-33
  lessons (batch 2): a PINNED entry dies two ways — the scene close
  (leave + return) and the narrator's own withdrawal (a retire delta;
  un-pinning does not exist, but the narrator's assertion can die) —
  either way RETIRED is terminal, the reference off-grammar at the
  gate, fresh establish legal (a new entry id); `use`/`rest`/`examine`
  fed live for the first time — the wait-720 decay batch drains inside
  the door's own `run_steps` exactly like the fire cascade (16
  events); a wait reply WITHOUT `ticks` passes the parse gate (the
  gate does not duplicate door-owned checks, PARSER_SPEC §4) and dies
  loudly at the door — the cycle is consumed, the fixed reply needs a
  fresh `say`.

- **The corpus-regen protocol (iter-48 law, actualized iter-49/50;
  iter-51 taught the ZERO-regen landing: when the landing's events
  ride after the case's claimed ids, the pins hold and only the
  deliberate pins ride — content-6 will re-check this first).** A
  content landing that shifts the event
  stream re-distills the affected cases through the REAL mediator
  cycle with a FIXED-POINT runner outside the repo (Rule 9; the
  iter-43/44 hand re-pin is the manual precedent). The three laws the
  runner taught: (1) the corpus test pins only the LAST beat's status
  — a beat may be a DESIGNED refusal (the regen-ladder probes:
  outgoing_guard beat 0); the reference ladder comes from the HEAD-pack
  green replay, and convergence means the ladder SHAPE is preserved,
  not that every beat accepts; (2) the per-beat measurements (the
  state fold at each beat's reply gate, the event-id alignment) are
  trustworthy only when the beat's PREDECESSORS landed their HEAD
  statuses — a refused beat never feeds its intents, so every later
  stream is starved until the refusal's cause is re-pinned; (3) the
  id re-pin must be IDEMPOTENT — the alignment always maps
  pristine-old → current-new (re-aligning a re-pinned id increments
  it forever; the fixed point never settles). New-event claims (the
  deliberate pins of the landing's own events) ride AFTER
  convergence — the old-id alignment must never touch them. The
  iter-49 laws (the 105-case pass): (4) **prove the runner first** —
  the identity check replays the pristine corpus through the re-pin
  machinery and asserts ZERO changes (a runner that mis-pins on an
  unshifted stream will mis-pin worse on a shifted one); the corpus
  test green after the fixture write is the fixed-point verdict, not
  a second re-pin pass; (5) **a designed-refusal claim is never
  re-pinned** — the re-pin rule is `fixture value == pristine truth
  AND != current truth → take the current truth`; a claim that never
  matched the pristine truth is the case's own wrongness (the refusal
  family), and an id re-pin follows the pristine referent's role so
  the type mismatch reproduces; (6) **the draw-count coupling is the
  regen's hard edge** — an ADDED urgency entry shifted every later
  check draw and flipped designed ladders (3 cases at one entry; the
  doccheck fail branch — the corpus's only pin — would have been
  LOST, not re-pinned); engine-2 LANDED (iter-50, D-079): the
  per-entry urgency streams remove this coupling entirely — an
  added/removed entry shifts no check draw and no other entry's
  rolls; a landing's regen now covers only its OWN events. The
  iter-50 runner laws: (7) **re-pin writes must land in the
  FIXTURE, not just the applied reply** — `_resolve_anchors` (and
  any deep copy) REBUILDS the reply document, so the re-pinned claims
  must be written back into the fixture's own beats (the identity
  check on HEAD cannot catch a missing write-back: nothing re-pins
  on an unshifted stream — the corpus test green after the write is
  the only verdict); (8) **a measured-and-refused intermediate
  design never lands in the fixtures** — when a landing candidate is
  reworked mid-iteration (engine-2's single shared stream, refused
  at 4/10), the migration re-runs from the PRISTINE fixture, never
  from the refused candidate's output (a second pass over re-pinned
  claims would misread them as designed wrongness). The iter-52 law
  (the true ZERO-regen landing, content-6): (9) **the event's `hooks`
  field IS the seeding record — a pack tag added to a hooks list
  diverges the SEEDING event's bytes on every run that fires it** (a
  birth certificate, not a behavior change: pin-green survives, 14
  corpus cases byte-diverged by one field, ZERO re-distill). A
  weight-0 successor with no draws and no corpus-stage release
  closes the ladder: measure BOTH arms first, and when the only
  divergence is the seeding field + appended events, the landing
  ships with pin updates alone. The runner:
  `/home/z/my-project/scripts/iter50_regen.py` (ephemeral session
  artifact; the laws live here, the runner's shape in worklog
  iter-50).

- **Where the code-quality bar lives (D-031).** Law: AGENTS §4+§9
  (invariants, canon-write privilege, DoD). Constitution: BLUEPRINT §2
  (L13/L14). Build clauses: `docs/blueprint/phase0.md` §1/§2/§6.
  Executable: `tests/test_architecture.py` (PACKAGE_DIRS covers every
  top-level code dir — the closure test, D-046) + the stoplist test.
  No new canonical layers (D-018 pattern).
- **GitHub upload / git hygiene (the KI#1 family; KI#55).** Uploads
  drop `.gitignore` and empty dirs — verify it exists after any upload.
  `git status --short` shows changes vs HEAD, not what IS in HEAD; after
  structural changes run `git ls-files <path>`. A file DELETION cannot
  ride an archive or `git add` — the end-of-report command block must
  list `git rm <path>` explicitly, else the deletion is reported but
  never lands (KI#55: bg-4's KI#52 fix sat unlanded for exactly this
  reason).
- **Scope-creep guards: content/tone + the doc-loop alarm (AGENTS §2).**
  Content/tone questions → D-030 + the `PACK_SPEC.md` sketch row: tone
  is data asymmetry inside existing systems; growing the pack or
  writing a pack spec before its trigger = scope creep (§2.4; grim
  material waits in `pack-1`, phase 6 / 2nd setting). Consecutive
  doc-only iterations force a stop (§2.5) unless a fresh owner request
  fires (the D-022 exception); code iterations never trigger the alarm.
- **DF exports are not well-formed XML and can arrive truncated; the
  survey tool owns the recipe, the sink reuses it unchanged (iter-8e/
  8f/8g; bg-1-sqlite-sink).** Raw CP437 control bytes (item-quality
  symbols) sit inside artifact names — byte-level sanitize before any
  parse; the exporter can die mid-write (no `</df_world>` at EOF) — the
  survey tail-checks and synthesizes the closing tags best-effort,
  loudly marking every count PARTIAL (KI#34); stream with iterparse +
  clear (a non-clearing parse OOMs 4 GB on a 2 GB export); main-file
  type names are display-style, the plus companion's are snake_case —
  normalize. **`--audit` (iter-8g) is the coverage census:
  per-section per-record-tag counts + every unique child-tag set per
  record tag — a structural fingerprint bounded by DF record uniformity
  (typically 1-3 variants; >3 = schema drift signal). Coverage matrix:
  `docs/ref/df_legends_xml.md`.** Any record tag outside the matrix
  renders **UNDOCUMENTED** — implemented bg-1 (KI#36; the marker was
  documented but never implemented — its first real run caught two
  matrix gaps: `artifact`, in every export, and `historical_era`). The
  record in flight at a truncation cut IS counted (the recovering
  reader synthesizes its closing tag — measured, test-pinned; survey
  and sink agree, so counts cross-validate on any export). **The
  SQLite sink landed (D-051):** typed cores + EAV fields +
  `event_participant` + generic JSON `records`; truncation policy =
  flagged partial import by default, `--strict` aborts; the DB is a
  rebuildable index of the export bytes — content-deterministic, no
  wall-clock in `meta`, no golden DF fixtures. **bg-2: the sink v2 plus
  pass (D-063) — the companion's `historical_events` land in a separate
  `event_plus_fields` EAV (same ids, fields only; everything else in
  the companion counted-not-stored); theft/beast detail is
  companion-only. The taxonomy survey: `scripts/df_taxonomy.py` →
  `docs/TAXONOMY.md` (120 entries, the 16 target types, measured
  findings incl. the `hfid1`/`hfid2` participant-index blind spot —
  reputation events carry 0 participant rows; reputation context needs
  the EAV).** Measured numbers + the full recipe:
  `docs/TECH_NOTES.md` §3.1/§3.2/§3.3; tools: `scripts/df_survey.py` +
  `scripts/df_import.py` + `scripts/df_taxonomy.py` +
  `scripts/df_briefer.py` (bg-3 — the POV mini-briefer + the
  closed-vocabulary reverse validation over the sink; the
  invented-facts family is `beyond_records` + `unknown_*` +
  `contradicted`; the epistemic closure IS the participant index,
  blind spot inherited; the ≤2-regen ladder + dry floor ported from
  VALIDATION_SPEC §7); regression: `tests/test_df_survey.py` +
  `tests/test_df_import.py` + `tests/test_df_taxonomy.py` +
  `tests/test_df_briefer.py`.
- **The §6 cap laws: substance over line count (D-025/D-034 — one row
  since the phase-1 collapse) + the ID-preserving gate-collapse.** The
docs cap is 600 with the §6.1 substance filter as the real law — filler
is cut always; named systems, field lists, enum values, per-source
verdicts are never cut to fit. The DECISIONS collapse writes compound
IDs with the FULL prefix on every member (`D-018/D-022/D-029` —
`D-018/022/029` does NOT resolve); compressed rows keep
decision→why→consequence and link the single owner (D-024).
Pre-collapse history lives in git; collapsed 46→30 at the phase-0→1
gate, 41→30 at the phase-1 gate (iter-26), 35→30 at the phase-2 gate
(iter-35), 48→30 at the phase-3→4 gate (iter-54); 30 HELD at the
phase-4→5 gate (iter-65 — no collapse owed: the phase-4 landings rode
the single D-084..D-093 family row as they landed, the verdict D-094
joined the gate-verdict family); 71→30 at the phase-5→6 gate (iter-102
— never resynced here until iter-116); 44→30 at the phase-6 gate
(iter-116, the ladder complete — the phase-6-era rows folded into
families, D-151 the record). The ≤30 cap stands; a future breach
collapses at the owner's next gate call.
- **The read-side layers are pure functions of their inputs (iter-5/6/8/10
  laws).** Every render entry point builds a fresh `RngBank` from the log
  HEADER seed — same log → same bytes in any process/`PYTHONHASHSEED`; a
  growing log keeps its rendered prefix (the session delta-print rides
  on this). A session is one opened Simulator: `open`/`run_steps`/
  `close`; session == batch bytes; `seed <n>` starts a NEW log (INV-5).
  `core/metrics.py` reads `(events, projection)` — the simulator never
  knows a metric exists (L3; Mesa DataCollector inverted). The brief
  assembler: **zero RNG at all** (dry structured tokens, L2 —
  `brief/assembler.py`, BRIEF_SPEC §2); its recall `max_items` is
  a ranking cap (the O(relevance) top-k), NOT a budget drop — the
  `[truncated:N]` marker counts budget drops only (same law for the
  texture caps). **Since iter-10 the purity pair is (log, ledger) — the
  D-049 determinism quarantine LANDED:** the ledger is session render
  state (auditable via surface/source/cause, never replayable); T1/T2
  canon tests never touch it; "zero RNG" stays a claim about assembler
  internals, never about log-relative determinism of the ledger-fed
  brief. Since iter-59 the retrieval ladder joins the read-side family:
  `RetrievalIndex.build` is a pure fold of (pack, events) — an
  in-memory rebuildable index, never a canon write; the `knower` query
  parameter IS the known_by boundary (None = lore only, facts never
  knower-free); the sqlite-vec extension is probed-optional (absence =
  normal operation, the pure-Python cosine scan answers, D-012); the
  never-empty law is about rung failures — a no-match vectorless query
  returns the honest empty; the floats are same-environment
  deterministic only (TECH_NOTES §4).
- **The scene ledger's session laws (iter-10, D-053; owner blueprint §1 +
  BRIEF_SPEC §3.3).** The mediator's beat order is `commit →
  retire_contradicted(window) → sync_scene → assemble → narrator →
  apply_delta` — `apply_delta` auto-syncs, so a scene close cannot be
  forgotten (D-037); retire_contradicted runs BEFORE sync so a
  contradiction (the stronger, tombstoned signal) wins over scene_close
  on the same entry. Scene-scoped texture belongs to ONE scene
  (identity `(location, ordinal)`; a revisit starts empty) and is
  double-guarded: sync retires it AND the window law requires
  `t >= scene.from_tick` (a stale unsynced ledger leaks nothing).
  Entity-scoped texture survives scene changes but renders only when
  the entity is present (position OR carried by a present non-item).
  Re-asserting a CONTRADICTED or PROMOTED (scope, slot, value) is
  laundering (refused + flagged); re-asserting after narrator RETIRE is
  fresh texture (new candles are legal). A ref resolves against LIVE
  entries — terminal/unknown → stale_ref refusal; refs to live-but-
  absent entity texture pin harmlessly (visibility is the read path's
  law, not the gateway's). The live promotion loop (noun resolution →
  intent door → `mark_promoted`) is the owner-gated narrator boundary's,
  never the LLM-free half's. Since iter-12 the narrator half is LIVE
  and external (D-055: call/reply files under `output/mediator/`, the
  contract VALIDATION_SPEC §7.1) — a refused document never feeds
  intents (the beat regens whole); the L12 floor renders the beat's own
  chronicle lines. iter-106/D-139: the ledger is session-scoped through
  a RESUME too — `--resume` opens a fresh ledger (the law's own shape:
  the ledger dies with its session; live texture never crosses the
  process boundary, promoted texture rode events and stays canon).
- **Gate mechanics + chain counting (iter-6/6a laws).** Same
  playscript/seed (125), only the director flag changes: ON fires
  `director_0000`; OFF keeps seeding (D-005) and produces ≥3 emergent
  chains (baseline 24 — 26 through iter-65, the iter-98 designed
day1_full price moved it; the gate verdict row D-136 owns the number);
the logs byte-differ. The harness is a script,
  not a test (a 1000-sim sweep would dominate the suite); kill-criteria
  operationalize as M3 mean ≥2, M1 non-trivial, M2 non-zero. M3 counts
  per qualifying endpoint: each non-PC, non-director event whose maximal
  backward cause-walk reaches a player root with ≥2 non-PC links counts
  once — decay self-chaining inflates the total (M3's magnitude is
  decay-dominated; the targets are unaffected; phase-1 tuning reads
  composition, not totals).

## Next step

**iter-171 DONE: engine-1 move (a) — the {3–8B, GBNF} experiment
CONVENED and the llama.cpp surface mapped (the owner's «за 1 раз как
можно больше тестов… лучше вообще выяснить все про llama.cpp и дальше
уже разбирайся на своих мощностях, а на моем железе только в крайнем
случае» call): the Rule-9 runner DELIVERED outside the repo (the
Vantiel-handoff pattern: engine1_runner.py + engine1_grammar.py +
engine1_battery.py + the runbook + the config template — never
committed, never staged) — ONE batched owner session covering
TEST_PLAN §8.5's gap rows (the 51-utterance corpus raw → one re-ask,
the deviation F1–F6 with the guess-within-grammar tally, the bg-7
prose families (ii)–(v), the per-component p50/p95 columns) + all
four CONTRACTS §4.3 arms + the §13 surface probes at the owner's
build. Validated end-to-end FIRST on the owner's exact build b11064
(commit a894dae93) CPU-side: TECH_NOTES §13.1 the sandbox surface
record — the ROUTER (model swap = autoload/eviction, never a
restart; children inherit the serving args; /slots?model=), POST
/props the measured silent no-op (write 200, effect never lands —
per-request is the only live surface), the -np context split
(explicit np halves per-slot; auto = 4 slots kv-unified), GBNF on
the chat route as a top-level grammar param (response_format
"grammar" refused), the GBNF dialect facts (underscore rule names
rejected — parse failure; [ ] is a char class, the optional group is
( )?; \" escapes in literals), cross-model thinking×schema mechanics
on the Qwen side, the determinism mini 5/5 greedy AND seeded, the
cancellation-vs-second-client row closed, restart timing — every
software-bound §13 "not established" item closed at the owner's
commit; the runner's GBNF mapping is the build's repo-side function
previewed (per-verb precise, subset-enumerated fields). Zero engine
code in the repo, INV-4 UNCHANGED, doc-only, 1900+1 green, ruff
clean. **The owner's move: the one run — `PYTHONHASHSEED=0 python
engine1_battery.py --config engine1_config.json --arm all`, send
back engine1_out/engine1_bundle.zip; smoke first with `--arm smoke
--limit 2`. The natural next moves after the bundle: the re-
distillation + the heartbeat's first local row + presentation-1's
local evidence (the transcripts' own iteration), or the build
landing (b) — the GBNF mapping + the door wiring, INV-4 lifting
there, both owner-gated.**

**iter-169 DONE: qa2 — the KI#88/#89 lint-side closures (the owner's
«проработай открытые в прошлой итерации ki и все связанное, нужно
доделать все с технической частью» call over the two holes qa-1 opened
and routed): BOTH KIs closed at LOAD, zero runtime behavior change on
well-formed packs (1900+1 green both ends — the +15 the §9 claim
packet; the golden fixtures byte-untouched, the five committed packs
loading; ruff clean, mypy --strict core/ 0). KI#89: the shared
`lint_direct_keys` row (packlint/shared.py, the lint_echo_cond family)
refusing the five record-reading tests' directly-indexed keys —
flag/field/values on carries_flagged, flagged_accessible, field_in,
field_nonempty, has_field — for presence + type + non-emptiness, wired
into every `requires` declaration site (the action canon, the texture
block, the urgency beat gate, the faction gate; the iter-45 leverage
`who` precedent generalized to its whole family). KI#88's first arm:
the on_action actor vocabulary split (ACTOR_KEYS = world |
source_actor, owned beside the resolver in core/onaction.py — the
reaction event's actor is a schema-required string, `source_target`
drafts None on a targetless source; the dedicated lint row carries the
rationale, the runtime assert stays the programmatic backstop). KI#88's
second arm: the target-sourced check row — the action must pin the
intent's target with a target-noun precondition, the lint reading the
door's OWN `needs_target` predicate (extracted from validate_shape —
one source, two readers, agreement by construction); the texture-block
twin stays the stricter row. The `flag` test itself (unused by every
committed pack) stays outside the row set exactly as the KI scoped it
— its twin hole (and kind's `is`, the `with`/`axis`/`value` presence)
is the owner's call class, recorded not routed. The natural next moves
stay the owner's: engine-1 (the TASKS standing row's own
recommendation — the SoW horizon's head), the world track's embodiment
options, or another backlog row.**
**iter-168 DONE: qa1 — the type-discipline audit (the owner's «там
еще была задача qy 1 что ли, связанная с проверкой кода» chat call
naming the standing row): mypy --strict on `core/` taken 207 → 0
across 36 files at ZERO runtime behavior change — 1885+1 green both
ends, the golden fixtures byte-untouched, ruff clean. The root-fix
audit: `_require(condition: object)`, the `Importance`/`Fidelity`
Literal funnels, the RetrievalIndex slot annotations, the Mapping
read-only widening under fold's dict `Projection`, the TypeGuard
`_is_int`/`_is_number`, the Iterable bridges in `Pack.entity`/
`action`, the assert-after-require narrowings across the packlint
family, the shadowing kills, log.py's first-branch annotations — 29
core files (the §2.3 soft limit noted: a repo-wide strict pass).
Two real holes made loud: KI#88 (the source_target actor null + the
target-sourced defender — asserts landed, the lint-side closure the
residue) and KI#89 (the door's directly-indexed cond keys not
load-linted — the iter-45 `who` family, the fix routed). The tool
stays OPTIONAL (D-031 unchanged — mypy in no dev deps, no CI row;
enforcement is the owner's call class). The natural next moves stay
the owner's: KI#89's lint rows (small, the iter-45 precedent), KI#88's
lint-side closure, or the embodiment options the world track still
holds.**
**iter-167 DONE: stepread — the step bench's first embodiment (the
owner's «продолжай работы, что логичнее всего сейчас начать»
continuation call over STATUS's embodiment routing — the natural
doc-streak breaker after three doc-only iterations, D-022's own
recommendation): the step's close read, the unit's setting verb (the
§6.2 gap text's own "a future embodiment's own class, the read_pole
precedent"), landed in province_pack as PURE PACK DATA, zero core —
the read_stair hinge (the read hinge's third instance: the grim
read_ticket first, the pole second; the family's first location-kind
target — the stair IS the carrier) minting the literal token
the_step_law to the reader: the ORDER the road never learns from the
books (§6.2's knowledge asymmetry; §7.1's stranger row — the road's
misread correctable in play, the meaning slice's misread-correcting
half widened to the committed band; the brief's recalled facts the read
surface); the token deliberately PLAIN KNOWLEDGE, never a secret (the
vale's own category, no lever — the registry stays two keys); the
unlit weir steps the night read down to partial; the field_in pin +
the co-location gate die at the door as named rejections; zero corpus
price (no committed script reads the stair); tests/test_stepread.py +7
(the §9 claim packet); the remaining embodiment options (the notch
record's arming, the hatch — and the winter kin's three) stay the
owner's call class; the water level's half stays owner-routed (the
read mints the LAW, never the PRESENT); 1885+1 green both ends (the
+7 the claim packet).
**iter-166 DONE: intake33 — the game-design practitioner talks corpus
routed (the owner's «изучи gamedesign_knowledge_base.md и определи что
можно перенять, адаптировать или чем вдохновиться… распределить по
документации» research call over the uploaded consolidated five-source
knowledge base: Sawyer PoE attributes / Meier psychology / Battle Mode
micromanagement / Johnson Old World / Wolverson procgen): PARTIALLY
CONFIRMED — a perception + economy-craft donor, never a systems donor,
differentiated from the refused UNIFIED GDC base (intake-30's F2) by
the one domain no prior family owns — outcome-perception psychology.
Adopted: the OUTCOME-PERCEPTION LAWS CARD (the layered legibility
ladder — truth never bends / failure carries cause + avoidance path /
odds as expectation bands / transparency opt-in by flag / outcomes
legible through residue / stakes irreversible; the combined form of
the five competing presentation solutions, each minus neutralized by
another layer) → presentation-1's consult material (the third parked
card, the visual/Vantiel precedent) + the ANTI-ARBITRAGE SPREAD
(exchange lossy by construction — the Resource open question's donor;
falsifier: the water's function-loss arbiter) + the TURNOVER QUESTION
(the ECS cure = the function-loss probe aimed at holder mortality —
the anti-freeze law, WORLD_AUTHORING §5; consumers: the camp's meso
half, W5's biography arc) + two parked notes (the Hot-Path placement
pair beside the intake-27 topology proposal — the road-traffic
rider's material; the weak-coupling authoring law — pack-3's event
families); the largest cross-domain confirmation batch since
intake-27 (seed-in-save = INV-2/T2; no-cheats AI = the one-id door;
infinite tooltips = mechanics.py; automation-red-flag inverted =
mech-2's nothing-dropped-silently; direct-and-verify = the worldgen's
MST-by-construction superior own form); refused binding (all
dice-bending — perceived fairness only at the render layer, never the
roll layer; the 3:1/2× constants — threshold leakage; tech-deck /
order-system / no-counterattack — no substrate, no consumer); the
source record docs/ref/game_design_talks.md (ref-23) + the five §10
catalog rows + the DEEP index + the phases.md §6 stub + D-191; doc-only,
1878+1 green both ends (zero test change); the third consecutive
doc-only iteration — the D-022 exception consumed by THIS session's
fresh owner research call; the next authored-band move needs a fresh
owner call (an embodiment call remains the code-band breaker).
iter-165 DONE: kin1 — the world track's fourth W4 candidate, the working
set's last (the owner's «продолжай работу с world track» call): the
constructed kinship edge (candidate 4) tested at the authored band over
committed substrate only and CONFIRMED as THE WINTER KIN (ANCHOR_REGION
§6.3) — care under the shelter law through one full stranded season mints a
socially recognized kin edge (the milk-kinship MECHANISM, never the
practice): the winter's board never the night's (the rarity gate), the
edge binding both ways (protection + mourning owed, the barred purse the
bend's own boundary), passing down both lines (never unnotched, the
recognition living); the falsifier PASSED (the Sarrow need demonstrated —
the stores eight of the paper twenty carried one way to the debt and the
bend; the function-loss arbiter; the anti-noise check); the mesh's seventh
loop G + three interlock edges (E⇄G, B⇄G, D⇄G); the crisis + humor probes
run, the heartbreak row's first authored half; three first-exposure
substrate gaps recorded, not routed (the relation form, the proof's read,
the mourning surface); doc-only, 1878+1 green both ends (zero test change)
— THE W4 WORKING SET COMPLETE. iter-164 DONE: water1 — the world track's
second meso unit (the owner's «продолжай работу с world track» call over the W4
candidates' next): the practitioner water-governance node (candidate 3) authored as the STEP BENCH
(ANCHOR_REGION §6.2) — the weir stair's three hands over one head (the
keeper's pool, the steward's race, the beam's run), the head named by the
stair's wet step (four rungs, the committed high_water line the fourth's
own text), held by the practitioners' reading, enforced at the water by the
users themselves; the candidate's falsifier PASSED (the function-loss
arbiter: the allocation order is a function neither the guild's paper nor
the crossing's custom performs; the anti-council check: no axis, no
threshold, no institutional door); the mesh's sixth loop F (AUTHORED) +
three interlock edges (C⇄F, E⇄F, B⇄F); the chronicle's quarrel collection
themed as the stair pact; §7.1's Thornmill obligation ANSWERED; three
first-exposure substrate gaps recorded, not routed (the water level, the
setting verb, the hatch gate); doc-only, 1878+1 green both ends (zero test
change). iter-163 DONE: mech-2 (the owner's «mech 2 давай сделаем» call — the
row's own build): the introspection CLI's attention budget landed as one
mechanism — the caps core (trace's default = the last 720 ticks + the
naming tail note; matrix's default = the compact query-vocabulary
inventory, --full the whole listing; the row's "past a screen"
conditional now fact on the grown packs) + intake-21's single-event
postmortem (`why --event ID`: cause chain + knowledge-wiring join +
cascade, recount-oracle-pinned) + intake-22's DAG export (`matrix --dag`:
the rules.json::systems projection as Mermaid, never a runtime);
tests/test_mechanics.py +6, 1878+1 green both ends; the release-equality
pin green (D-118 untouched). iter-162 DONE: the debt-1 standing row's
build (the flood debt's economy arm landed in province_pack as pure pack
data over the res-1 substrate, zero core — the third consumer arming:
the accounts, the toll-surplus flow + the guild's collection, the FOLD
answering D-182's named co-due limit by construction; tests/test_debt1.py
+9, 1872+1 green both ends; zero corpus price, the golden T1
byte-untouched). iter-161 DONE: the pole's embodiment seeds (the
flood-story recognition token + the steal_target flag, pure pack data,
zero core; the lever chain + the player-facing ablation test-pinned,
tests/test_poleseed.py +11, 1863+1 green both ends; the debt-1 standing
row OPENED — consumed iter-162). iter-160 DONE: the W4 bounded experiment —
the crossing household through the full operator stack on existing substrate
(the working set's own first move; CONFIRMED at the split band, the transfer
KEPT — the carrier-availability law + the verb-gate boundary + the
carrier-ablation probe, the debt's lifecycle table authored, candidates 1/2
informed; doc-only, 1852+1 green both ends). iter-159 DONE: the Vantiel
research handoff routed (intake-32, D-190 — the separations record
docs/ref/vantiel.md ref-22 + the presentation-1 consult material parked
behind the owner gate; doc-only, 1852+1 green both ends). iter-158 DONE: the
Kurvitz consolidated research routed (intake-31, D-189 — the W4 operator set
+ the test operationalizations + the bounded crossing-household experiment +
docs/ref/kurvitz.md ref-21; doc-only, 1852+1 green both ends). iter-157 DONE:
the companion arming (companion-1 + tune-3, together — the crossing
household's second hand embodied as pure pack data, the first committed NPC
movement source, the traveling-knower probe CONFIRMED on the crafted twin,
the punt pole committed (KI#87 CLOSED); zero core change, 1852+1 green both
ends). iter-156: the world track's causal mesh audit (W3 — five loops, four
committed + the credit loop authored; doc-only). iter-155: the first anchor
pass (A1/A2/A3 — the crossing household as the first meso unit; WORLD_TESTS'
three OPEN tests → PARTIALLY CONFIRMED; KI#87 opened, closed iter-157).
iter-154: the agent-dense v3 hybrid pack routed (D-187). iter-153: the
worldbuild archive intake (D-186 — `docs/worldbuild/` landed, 10 files).
iter-152: the CORE_DESIGN_RESEARCH deletion + the evidence-class citation
sweep. iter-151: the semantic documentation compaction pass (D-185 —
DECISIONS 63→30, TASKS 2422→914). iter-150: the AGPLv3 relicense + the
standing-backlog revalidation (D-183/D-184). iter-149: pack-4;
iter-148: pack-1; iter-147: since-1; iter-146: res-1; iter-143: ci-1.**

1. **The owner-gated backlog (the standing rows — the ORDER owner
   decides, TASKS owns composition, never order; each build row's
   verification plan rides TEST_PLAN §9's claim packet):** with
   ci-1/roads-1/res-1/since-1/pack-1/pack-4/companion-1+tune-3
   consumed and `engine-1` DECIDED (iter-170, D-192 — the build
   boundary CONTRACTS §4), the session's RECOMMENDED next call
   (intake-29's readiness order, never the pick) is the `{3–8B,
   GBNF}` experiment's convening (the decision's remaining
   measurement — TEST_PLAN §8/§8.5's gap rows + the contract's four
   new arms, the Rule-9 runner outside the repo) or the build
   landing itself (the GBNF mapping + the door wiring; INV-4 lifts
   there) — `presentation-1` follows from the experiment's results
   (D-022/D-148). The remaining
   standing rows — REVALIDATED iter-150 (D-184; the per-row state lives
   in TASKS' Standing rows):
   `parse-2` (buttons wait on a frontend consumer, multi-intent on
   live-session evidence — neither is "improve the parser"),
   `st-2` (consumer-first, parked — no pack has wanted the
   promotion door), `scav-1` (measurement before mechanism, parked
   — no derived-state size problem on record), `bg-6` (the SoW audit,
   D-055 deferral), `pack-3` (one
   candidate for the next authored pack slot — the 2nd-setting
   blocker gone with phase 6 CLOSED), `st-4` (rides presentation-1
   at its write time, D-148), `st-5` (the first real consumer
   decides — the res-1 sink shape now concrete). mech-2 CONSUMED
   iter-163 (the caps core + the intake-21 single-event postmortem
   + the intake-22 DAG export, one mechanism — DEFAULTS bounded,
   nothing dropped silently, expansion by flag; its not-built
   residues — the impact-query surface, the first-divergence
   operator — stay zero-consumer, the first-consumer law). debt-1
   CONSUMED iter-162
   (the flood debt's economy arm landed in province_pack; its
   discrete-event residues — the paper's fall, the clearance lump,
   the punt's purchase, the player-scaled doors — a future row's
   own call, never auto-candidates).
   For the SoW promise
   debates the intake-27 sacrifice protocol (D-173) and the
   intake-28 combination fence (D-174). The research posture
   (intake-29's admission rule, D-175): a new external intake
   convenes only with a named open build row/standing debate it
   feeds + a potential falsifier stated up front — new knowledge
   now comes from building and measuring. pack-4's own honest
   residues (the future riders' material — the mapping's post-T1
   rows): the legal exclusion (D-134's state/flag + knowledge-record
   family), the cultures (name-1 profiles + prohibition sets), the
   road traffic (depth-7 condensation), the lore hooks (D-140's
   templates + cause_hook); the ENGINE findings the future rows'
   material: the group-stock lint gap (the entities vocabulary vs
   the economy/fold modules), the co-due same-account flow limit
   (the snapshot from_ — the per-flow re-draft), both recorded in
   the pack's own notes + D-182. companion-1's own honest residues
   (the future riders' material): the autonomous follow is
   LOD-bounded by design (the warm ring waits for the reader — a
   trailing follower at beat cadence is architecturally impossible
   under the armed macro clock, the paired mode B legs carry the
   escort; a never-stranding gradient follower would need a grammar
   extension — a negated co-location test or a dynamic target — its
   own consumer's row, never specced here); the beat-carry
   duplicates (the mid-travel stale position re-passing the gate)
   die at the door/OCC as bounded intent_rejected no-ops — attempts
   are facts.
2. **Track B:** bg-2/3/4/7/8 DONE, bg-6 owner-deferred. The standing
   gap rows: the {3–8B, GBNF} arm (owner hardware — engine-1's
   remaining measurement, the experiment convened at the owner's call;
   the four new arms pinned CONTRACTS §4.3), the bg-7 prose families
   skipped in the bg-8 heartbeat, the per-family latency distribution.
   New track-B ideas enter the backlog on the owner's call only.
3. **The SoW horizon (ROADMAP §6) and the world track
   (`docs/worldbuild/`, D-186) are the standing frames** now that
   the ladder is complete: the mediator protocol specs (BRIEF_SPEC
   and friends — SPECS_BACKLOG) + the dumb-terminal frontend
   contract; the SoW audit itself stays owner-gated (bg-6); the
   world track's active frontier is its own plan — the W4 meso
   expansion COMPLETE (each addition created its new causal coupling,
   `WORLD_WORKPLAN.md` §6, never this file's queue; W3 the causal mesh
   done iter-156, widened iter-164/165 — seven loops; A1/A2/A3 done
   iter-155, the first meso unit authored — ANCHOR_REGION §6.1,
   its pack embodiment LANDED iter-157/161/162: the second hand, the pole's
   two halves, the debt's economy arm; the W4 bounded experiment RUN
   iter-160 — CONFIRMED, the transfer kept; the SECOND meso unit AUTHORED
   iter-164 — the step bench, candidate 3 CONFIRMED at the authored band:
   the water's allocation order, the mesh's F loop + three interlock edges;
   the constructed kinship edge TESTED iter-165 — the winter kin,
   candidate 4 CONFIRMED at the authored band: the care's reciprocal
   binding, the mesh's G loop + three interlock edges — the working
   set's four candidates all answered; the step bench's setting verb
   COMMITTED iter-167 — the read_stair hinge minting the_step_law, the
   second meso unit's committed band opened); the next world-track
   call: the embodiment options — the step bench's remaining two (the
   notch record's arming, the hatch) and the winter kin's three gaps'
   class (the relation form, the proof's read, the mourning
   registration) — the owner's call class, the pole's iter-161
   precedent; W5's live band (the human tests — biography / humor /
   heartbreak, the authored halves on record, the live-session band
   open); or the camp's meso half (the charcoal debt — the causal
   map's named-not-authored row).
4. **Nothing is pinned.** The next move is the owner's: the
   recommended remainder of the sequence (the `{3–8B, GBNF}`
   experiment — engine-1's remaining measurement, then the build
   landing + presentation-1 from its results), a world-track call (the
   embodiment options of either authored addition — the step
   bench's remaining two or the winter kin's three — the owner's
   call class, the pole's iter-161 precedent; or W5's
   live band, or the camp's meso half),
   the debt-1 residues (the discrete-event doors the arming left
   un-armed — the paper's fall, the clearance lump, the punt's
   purchase — each a future row's own call), or a fresh call
   (the license's `pyproject.toml` field a one-line option if
   wanted — D-183's recorded follow-up). The three-iteration doc
   streak (iter-164/165 world-track + iter-166 intake33) is BROKEN:
   iter-167 landed the embodiment call on this session's fresh owner
   continuation (the read_stair hinge, code-band, the pole's iter-161
   precedent); iter-170 is doc-only BY ITS OWN NATURE (the decision +
   the contract + the evidence rows — the code band returns at the
   experiment/build calls).
