# STATUS — canonsim

Iteration: iter-62 (`iter-62-tex-1` — TASKS.md's top phase-4 todo,
tex-1: the scene_texture window's identity tier + per-scope quotas;
the owner's "continue per plans" call — no design fork this session:
the tier and the quota are the two halves of blueprint §1's ONE
identity-persistence resolution; no conflict, no KI) ·
Phase: 4 (Knowledge & scene) — OPEN (iter-55)
**tex-1 landed: the identity tier + per-scope quotas (D-091) —
identity never loses to fresh texture, one entity never floods the
window. `brief/assembler.py::_scene_texture_items` owns both
read-path laws (the write side — the ledger, the lifecycle, D-049 —
untouched): the ranking key widened to the identity-or-pinned tier
(an entry whose slot is pack-declared `identity_slots` ranks WITH
pinned; key: identity-or-pinned → pinned → newest → construction; the
slot is a CLASS, never a scope condition; pinned above identity
within the tier; an EMPTY set reduces the key to the pinned-only law
exactly — the D-048 bytes), and the quota walk AFTER the ranking (at
most `per_entity_max_items` lines per entity scope — a chatty entity
renders nothing beyond K, its identity slots filling its quota first
by construction — "identity slot first" without a second mechanism;
identity itself is bounded too, it cannot become the flooding
channel; scene scopes carry no quota — the room's texture is the
block's core content, `max_items` bounds it; tombstones carry none —
their own cap bounds them, a refuted identity line is gone;
beyond-quota lines render nothing, never drop, never mark — the
D-047 law; a value >= `max_items` is the documented inert state).
The pack contract: `identity_slots` + `per_entity_max_items` join
the REQUIRED `scene_texture` key set (lint `core/pack.py::_brief`,
the closed-vocabulary family); the committed pack armed
DECLARATIVE-ONLY (speech_pattern/look/mannerism, K=2 — the chorus
cap's own cost posture) with the corpus price zero by construction:
the committed corpora carry scene-scoped texture only
(candles/hearth/exits/shadows/kindling — no tier member, no entity
scope past any K). MEASURED: the tier live — the OLDER identity slot
above every newer plain entry, and identity SURVIVES max_items=1
pressure (the trader problem closed: a crowded scene never silently
evicts exactly what long sessions must keep); pinned above identity
within the tier; the quota live — the chatty guard (three plain +
identity) capped at K=2, identity first, the barkeep's and the
scene's lines untouched; three identity slots render exactly two;
the tombstone half unquota'd (K=1, both refuted lines render); the
empty-set reduction pinned (the pre-tex-1 bytes); the corpus price
ZERO — the 10-seed day1_full A/B (committed pack vs the empty-tier /
inert-quota copy) 10/10 byte-identical, the golden-prefix brief
byte-identical over the texture fixture, the narrator corpus 105 +
the parse corpus 10 + the T1 golden replay green unchanged over the
ARMED pack.**
·
Date: 2026-09-06 ·
Scope: `brief/assembler.py` (the tier key + the quota walk — the one
mechanism), `core/pack.py` (the two-key lint),
`content/tavern_pack/rules.json` (the declarative-only arming + the
notes), `tests/test_brief.py` (+23 — the tex-1 family: the tier, the
quota, the lint, the 10-seed A/B), `docs/BRIEF_SPEC.md`
(§3.3/§6/§9 — the same-commit law §8), `docs/TASKS.md` (tex-1 done
+ st-2 re-pointed to the promotion door), `docs/DECISIONS.md` (D-091
into the phase family, cap 30 held), `worklog.md` (iter-52 evicted),
`STATUS.md` (this header + the Next step flip + KI#71 deleted per
§5). 9 files — the one-mechanism-family scope (the iter-60/61
pattern). 1118→1141 tests green, ruff clean.

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

- KI#72 · the BRIEF_SPEC §9 identity-slot row over-projected onto
  scene-2 vs the TASKS row's scope (both written by iter-60's own
  edit — the deferral ledger promised the texture-window identity
  tier with a wiring row that never carried it) · opened+closed
  iter-61 (re-pointed to the `tex-1` row, the underdeliver law — the
  row is now LANDED, the debt paid; the lesson: the deferral table's
  "arrives with" must name the TASKS row's OWN scope, never a
  projection past it).

- (KI#71 deleted at iter-62 per AGENTS §5 — closed iter-59, three
  iterations past; the lesson lives in git + the REFERENCES/TECH_NOTES
  license-verify lines.)

- (KI#70 deleted at iter-58 per AGENTS §5 — closed iter-56, two
  iterations past; the lesson lives in git + the BRIEF_SPEC header
  that now reads the owning law, AGENTS §6/§6.1.)

- (KI#69 deleted at iter-56 per AGENTS §5 — closed iter-54, two
  iterations past; the lesson lives in git + the worklog's
  line-cap header note.)

- (KI#68 deleted at iter-51 per AGENTS §5 — closed iter-48, two
  iterations past; the lesson lives in git + the worklog header's
  re-trim note.)

- (KI#67 deleted at iter-48 per AGENTS §5 — closed iter-46, two
  iterations past; the lesson lives in git + the README sync law.)
- (KI#66 deleted at iter-47 per AGENTS §5 — closed iter-45, two
  iterations past; the lesson lives in git + the KI#67 family —
  every count restated in a second place goes stale.)
- (KI#65 deleted at iter-46 per AGENTS §5 — closed iter-44, two
  iterations past; the lesson lives in git + the FAQ.)
- (KI#64 deleted at iter-46 per AGENTS §5 — closed iter-44, two
  iterations past; the FAQ trim it flagged owes at the phase-3→4 gate
  alongside the DECISIONS collapse.)
- (KI#63 deleted at iter-44 per AGENTS §5 — closed iter-39, five
  iterations past; the lesson lives in git + the FAQ.)
- (KI#61/KI#62 deleted at iter-39 per AGENTS §5 — closed iter-37,
  two iterations past; the lessons live in git + the worklog.)
- (KI#60 deleted at iter-38 per AGENTS §5 — closed iter-36, two
  iterations past; the lesson lives in the FAQ + git.)
- (KI#55–59 deleted at iter-36 per AGENTS §5 — closed iter-34, two
  iterations past; the lessons live in the FAQ + git.)

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
  the only legal canon visibility.

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
  tick order, never by type: rotations and beats interleave by tick,
  the loop picks `min(candidates)` per iteration, the writer's
  tick-monotonicity invariant forbids out-of-order commits (the
  read-side mirror: `brief/assembler.py`'s `last_beat_tick`/
  `beats_crossed` reproduce the same beat set — BRIEF_SPEC §3.2,
  tested). Autonomous (urgency/director) intents enqueue at
  `entry.tick`, never beat_tick (sub_order NPC_REACTION), decay
  commits directly at beat_tick, and the runner feeds the next
  playscript step only on the PLAYER's own step endings (KI#17). The
  two doors: director releases and urgencies ride the INTENT door
  (a released hook = IntentData `director_<N>`/`urgency_<N>` through
  the front door; rejections emit `intent_rejected` no-ops with
  `cause_intent`; the director never bypasses Intent→Event) —
  reactions ride the COMMIT door: `_commit` feeds the knowledge
  index + runs `_react` for EVERY committed event (no call site can
  forget a reaction; cascades terminate; suspicion reacts only to
  tokens the knower did not already hold; the arrest resolution
  rides the same door).
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
  KI#51: external-paper figures are drift until fetched). Four
  places, four jobs: `REFERENCES.md` catalogs;
  `CORE_DESIGN_RESEARCH.md` §2 synthesizes; `docs/ref/<source>.md`
  carries mechanics; `BLUEPRINT.md` + `docs/blueprint/` carry
  resolutions. Link, never restate; cite ledger row IDs (e.g. "per
  RNG-1"). The audit method: grep a sample of ledger terms across
  the planning docs — every term must land in at least one (verified
  iter-0x; the ref-graveyard diagnostic).
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
(iter-35), 48→30 at the phase-3→4 gate (iter-54); next due at the
phase-4→5 gate.
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
  chronicle lines.
- **Gate mechanics + chain counting (iter-6/6a laws).** Same
  playscript/seed (125), only the director flag changes: ON fires
  `director_0000`; OFF keeps seeding (D-005) and produces ≥3 emergent
  chains (baseline 26); the logs byte-differ. The harness is a script,
  not a test (a 1000-sim sweep would dominate the suite); kill-criteria
  operationalize as M3 mean ≥2, M1 non-trivial, M2 non-zero. M3 counts
  per qualifying endpoint: each non-PC, non-director event whose maximal
  backward cause-walk reaches a player root with ≥2 non-PC links counts
  once — decay self-chaining inflates the total (M3's magnitude is
  decay-dominated; the targets are unaffected; phase-1 tuning reads
  composition, not totals).

## Next step

**Phase 4 (Knowledge & scene) is OPEN — leg-1/leg-2/leg-3/leg-3b/
retr-1/scene-1/scene-2/tex-1 are LANDED (D-084..D-091, the phase
family row): the trait fold with its brief read, the reflection mint,
the arming, the retrieval ladder (now QUERIED by the runtime — the
actor calls' protocol lines), the scene manager + mode B, the
session wiring (the chorus drain inside the beat cycle, the actor
reply door, the keyword query), and now the texture window's own
read-path pair — the identity-or-pinned tier (identity never loses
to fresh texture on recency) + the per-entity quota (one chatty
entity never floods the window). The next row: `leg-4` mode F
offline chronicler or `blind-1` the leak suite's extension to the
phase-4 surfaces (the exit criterion's own instrument) on the
owner's call. The exit criterion
"0 leaks on the blind-NPC suite" reads T3 (`docs/TEST_PLAN.md` §1)
extended to the phase-4 surfaces — the blind-1 row owns the
instrument (mode B + retrieval outputs under the zero-leak law); the
suite's core is already live in tests/test_scene.py. The phase-3
verdict record: D-083 + worklog iter-54.**

1. **The phase-4 queue (TASKS.md owns the rows):** leg-1/leg-2 —
   LANDED (iter-55/56, D-084/D-085) → leg-3/leg-3b — LANDED
   (iter-57/58, D-086/D-087) → `retr-1` LANDED (iter-59, D-088 — the
   ladder: the FTS5 index + the vec probe/scan/floor chain + the
   pack-coefficient re-ranker; the knower parameter IS known_by; the
   two LEGEND_SPEC contract points live; the corpus price zero) →
   `scene-1` LANDED (iter-60, D-089 — the chorus queue + the knower
   parameter + the actor call document; the leak suite core live;
   the corpus price zero) → `scene-2` LANDED (iter-61, D-090 — the
   drain, the actor reply door, the keyword query; the ladder's
   DORMANT gate opened; the corpus price zero) → `tex-1` LANDED
   (iter-62, D-091 — the identity-or-pinned tier + the per-entity
   quota, blueprint §1's identity-persistence read path; the pack
   armed declarative-only, the corpus price zero) → `leg-4` mode F
   offline chronicler / `blind-1` the leak
   suite's extension.
2. **Owner-gated, unchanged from phase 1/2:** `parse-2` (buttons +
   multi-intent), `engine-1` (the runtime inference engine decision
   — llama.cpp + GBNF, TECH_NOTES §1; the dev-time external parser
   carries mode C until then), tune-3 (the three-way NPC-movement
   fork), st-2 (the identity promotion door — the read-path half
   landed as tex-1, iter-62), the phase-1 corpus
   consolidation pass, `bg-6` (SoW audit, D-055 deferral), `qa-1`
   mypy + `ci-1` GitHub Actions. Still open for the owner: the Alien
   unknown-axis L6 conflict (DIRECTOR_SPEC §11) + the arc driver's
   review question (the climax flag on a weight-0 closing beat;
   D-081 records the tension, the owner may veto). NEW for the owner
   (leg-1's recorded questions): the testimony-crystallization
   fidelity floor — v0.1 counts any held token toward the family
   however learned (the hearsay shape: one telling of three related
   facts crystallizes the belief, provenance length 1); a fidelity
   floor for testimony (e.g. `told`-channel records counting only
   above the chain floor) is a pack-grammar question, recorded here,
   not forced; and the static-personality half of the owner's
   character-card question (spine lints, archetype expansion) stays
   PACK_SPEC territory (phase 6 / the 2nd-setting gate, the AP
   crosswalk already sketched there).
3. Track B: **bg-2 DONE, bg-3 DONE, bg-4 DONE**, bg-6 owner-deferred.
   New track-B ideas enter the `docs/TASKS.md` backlog on the owner's
   call, never spontaneously. `pack-3` (Sci-Fi sketches) stays parked
   until the 2nd-setting gate. `CORE_ONTOLOGY.md`'s SPECS_BACKLOG
   trigger ("phase-0 gate passed") fired at iter-6, was never
   scheduled, and the just-in-time reading keeps deferring it: write
   specs FROM experiment results at need, not ahead — it stays
   parked.
