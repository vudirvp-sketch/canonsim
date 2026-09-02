# STATUS — canonsim

Iteration: iter-48 (`iter-48-content2-alarm-echo` — the owner's
"continue work per the plan, quality over speed" session call; the
phase-3 backlog's top un-gated item: content-2 — the alarm panic
echo, the DIRECTOR_SPEC §11 first row closing, the LAST content row
that owed a corpus regen) ·
Phase: 3 (Director)
**OPEN — the alarm panic echo landed LIVE: the through-the-walls
law as one on_action entry over the standing drama-3 dispatch —
witnesses of `alarm_raised` gain fear, the panic contagion compounding
on the direct spike, its own chronicle line directly after the shout;
zero engine edits, the 7-case corpus re-distill paid in-iteration**
· Date: 2026-09-03 ·
Scope: `alarm_raised` → `panic_ripple` (scope `witnesses`, state
`status.fear` +10 — the CONTAGION quarter of the hardcoded +40
direct spike; NO gate — the alarm's own knowledge resolution decides
who heard the shout; the adjacent-hearer half dormant per the tune-3
static-placement finding), the event type story-critical with the
static chronicle line "Panic ripples through the walls of
{location}.", NO system_of_type entry (the crowd_wary precedent —
the state changes classify it to one system, M1 untouched). The
measured semantics: the occupants compound 40→50 (the fire seen AND
the panic heard), the cause actor 0→10 (hears his own shout — the
corpus's own knowledge pin made a fear fact), the echo commits at
the alarm's own tick (the decay baseline stays — beat-360 decay
50→46 / 10→6), the cascade terminates (no knowledge, no hooks, the
one-hop law). The corpus regen (the fixed-point runner outside the
repo per Rule 9, the iter-43/44 precedent): 7 fire-family cases
re-distilled — the fear claims re-pinned 40→50 (guard_01's decayed
36→46), the post-alarm event ids +1 (the panic insert), the alarm
case gaining the echo's own claims (the panic event by id + the
cause actor's fear), the regen-ladder shapes preserved
(outgoing_guard beat 0 stays the designed blind-guard refusal). The
day1_full 10-seed A/B (committed vs the alarm-entry-stripped
variant) 10/10 byte-IDENTICAL — the empty-backyard law (the gate
script's fire never shares a room; the live divergence lives in the
corpus's seed-33/93 scripts, TEST_PLAN §6). Tests 943→951
(+8 tests/test_panic.py; test_actions' folded-fear pin 40→50, the
intentional world change), ruff clean. KI#67 deleted per AGENTS §5
(closed iter-46, two iterations past).

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

(none open.)

- KI#68 · worklog cap drift: the file held 44 entries vs the 10 cap;
  the iter-43..47 entries each CLAIMED an eviction ("iter-NN evicted
  per the cap") that never landed — the named entries are present
  (the KI#62 family recurred; the claims were drift, the trim was
  never executed) · opened 2026-09-03 · CLOSED iter-48 (trimmed to
  the newest 10 in the same turn, per §6 "the trim is part of the
  task"; pre-trim history lives in git, the header note actualized;
  every future entry re-verifies the eviction actually happened).

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

- **The echo is a read model gated by L6 — NEVER an entropy input
  (iter-46 law).** The psychological residue (`core/echo.py`) is
  knowledge-derived per-NPC valence: the intent door's `echo_at_least`
  gate may read it (behavior selection, the P2b consumer), but the
  DIRECTOR may not — narrative entropy reads observable state only
  (DIRECTOR_SPEC §4, L6/EPIST-1), and a score folded from an NPC's
  private knowledge records is not observable state. Wiring the echo
  into `entropy` (or any channel input) would make the director read
  minds through a derived number — an invariant-grade bug that would
  look like a tuning change. Same fence for the chronicle: the echo
  renders nothing; the behavior it gates (the intent's own event) is
  the only legal visibility.

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

- **Crossings fire in tick order, not by type (iter-4 law, D-038).**
  Rotations and beats interleave by tick; the loop picks
  `min(candidates)` per iteration; the writer's tick-monotonicity
  invariant forbids out-of-order commits. Same rule for any future
  clock-crossing system. The read-side mirror of the beat law:
  `brief/assembler.py` `last_beat_tick`/`beats_crossed` reproduce the
  same beat set (intraday offsets repeated daily; an offset of 0
  belongs to day 1+, never t=0) — owner `BRIEF_SPEC.md` §3.2, tested.
- **Autonomous intents enqueue at entry.tick, never beat_tick (D-039) —
  and NEVER advance the playscript (KI#17).** Urgency/director intents
  enqueue at `entry.tick` (sub_order NPC_REACTION); decay commits
  directly at beat_tick; the runner feeds the next step only on the
  PLAYER's own step endings.
- **The intent door and the commit door (D-037).** Director releases
  and urgencies ride the INTENT door: a released hook = IntentData
  (`director_<N>` / `urgency_<N>`) through the front door (rejections
  emit `intent_rejected` no-ops with `cause_intent`); the director
  never bypasses Intent→Event. Reactions ride the COMMIT door:
  `_commit` feeds the knowledge index + runs `_react` for EVERY
  committed event — no call site can forget a reaction; cascades
  terminate; suspicion reacts only to tokens the knower did not
  already hold; the arrest resolution rides the same door.
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
- **Doc drift is evidence, not prescription — verify with `git log -S`
  AND the pinning test before acting (KI#42/KI#48).** A ref citing a
  spec section it never contained is drift (iter-6a: "AGENTS.md §9 —
  Script Persistence Rule" in README/TEST_PLAN/D-044 — the text bled
  from the session prompt; D-046 supersedes). A reported-but-unlanded
  pass is drift too: archives are ephemeral, git is real — check
  `git log` before building on any reported state (KI#42). A
  code-behavior claim is drift until the test that pins it is named
  (KI#48: the gateway's canon_slot check reads BOTH prop sources —
  the folded projection AND the pack record, `brief/ledger.py::
  establish` — so a pack-modeled field (exits, fire_spots, layout)
  is texture-guarded the moment the pack declares it; brief
  rendering of such fields is the pack's `scene_line_fields` list,
  BRIEF_SPEC §3.4/D-057). Pre-D-028 wording, license copies, and
  iter-0q/0r lift-target notes (`sim/systems/*.py`, `sim/store.py`,
  `core/store.py`, `core/runner.py`, `content/packs/*.py` — names
  that never existed; the plans were superseded by D-037
  systems-live-in-core and D-023 projection-is-fold) in
  `docs/ref/*`/`REFERENCES_DEEP.md` are historical; the owners are
  AGENTS.md §4, `REFERENCES.md` (the catalog), and
  `docs/AGENT_NAVIGATION.md` §1 (where things actually live).
  External-paper figures are drift until fetched: KI#51 caught a
  fully-formed cost citation ("Table 2, §6.4, ~$70") that exists
  nowhere in Park 2023 — verify against the arXiv full text before
  restating any number (bg-4, TECH_NOTES §9).
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

- **The corpus-regen protocol (iter-48 law; content-4/5/6 will need
  it).** A content landing that shifts the event stream re-distills
  the affected cases through the REAL mediator cycle with a
  FIXED-POINT runner outside the repo (Rule 9; the iter-43/44 hand
  re-pin is the manual precedent). The three laws the runner taught:
  (1) the corpus test pins only the LAST beat's status — a beat may
  be a DESIGNED refusal (the regen-ladder probes: outgoing_guard
  beat 0); the reference ladder comes from the HEAD-pack green
  replay, and convergence means the ladder SHAPE is preserved, not
  that every beat accepts; (2) the per-beat measurements (the state
  fold at each beat's reply gate, the event-id alignment) are
  trustworthy only when the beat's PREDECESSORS landed their HEAD
  statuses — a refused beat never feeds its intents, so every later
  stream is starved until the refusal's cause is re-pinned; (3) the
  id re-pin must be IDEMPOTENT — the alignment always maps
  pristine-old → current-new (re-aligning a re-pinned id increments
  it forever; the fixed point never settles). New-event claims (the
  deliberate pins of the landing's own events) ride AFTER
  convergence — the old-id alignment must never touch them. The
  runner: `/home/z/my-project/scripts/iter48_regen.py` (ephemeral
  session artifact; the laws live here, the runner's shape in
  worklog iter-48).

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
- **Four places, four jobs (D-027) + the ref-graveyard diagnostic.**
  `REFERENCES.md` catalogs; `CORE_DESIGN_RESEARCH.md` §2 synthesizes
  (one line per source); `docs/ref/<source>.md` carries mechanics;
  `BLUEPRINT.md` + `docs/blueprint/` carry resolutions. Link, never
  restate; cite ledger row IDs (e.g. "per RNG-1"). The audit method:
  grep a sample of ledger terms across the planning docs — every term
  must land in at least one; verified iter-0x.
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
(iter-35); next due at the phase-3→4 gate.
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
  brief.
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

**Phase 3 is OPEN (iter-36..48 — the pacing clock D-065 + the
exit-criterion instrument D-066 + the climax layer D-067 + the
multi-channel split D-068 + the grammar's three layers D-069/D-070/
D-071 + the document_check content set D-072 + the secrets &
leverage fact clusters D-073 + the coerce door D-074 + the
psychological echo D-075 + the release-chain layer D-076 + the
alarm panic echo D-077 landed — the phase-3 build column's ENGINE
side is complete: stagnation detector, complication buffer, arcs;
the content rows: the alarm echo is LIVE, its corpus regen paid.
What remains of phase 3 is the DRIVER rows (content-4/5/6 — each
shifting the substantive stream, the fixed-point regen protocol
now proven) + content-3 + the gate.)** The phase-3 remainder in
`docs/TASKS.md`'s backlog: the content rows, each as its own
iteration on the documented design —
`content-4` (the coerce driver), `content-5` (the echo driver),
`content-6` (the arc driver — NOT the naive watcher-pair chaining:
the D-076 e2e showed a never-firing predecessor holds the
corpus-pinned successor forever; the driver needs a first member
live on the runs it targets), `content-3` (ambient-channel
content). The dir-2/dir-4/drama-1/2/3 measurement's honest finding
STANDS SUPERSEDED in part: the document_check landing is the first
deliberate divergence (the check fires on the runs that reach the
confrontation — 1/10 day1_full seeds; the corpus's seed-93 script
fires), and social-1 adds the second (the same 1/10 hot seed mints
the leverage facts — the same steal failure drives both), while the
content-2 echo is corpus-script-only (the day1_full A/B 10/10
byte-identical — the empty-backyard law) and the
clock/channel/weight/arc layers stay inert on day1_full (every run
ends in PEAK — a measurable pacing delta needs a gate-protocol
script set that walks the world into quiet; recorded in D-066, a
phase-gate question, not forced).

1. **Phase-3 remainder** (TASKS backlog): the content rows
   (`content-4` the coerce driver; `content-5` the echo driver; `content-6`
   the arc driver; `content-3` ambient-channel) → then the phase-3→4
   gate (DECISIONS 43/30 collapse + the FAQ trim owed per the
   KI#64 note + TASKS/phases over-cap trims — all recorded as owed
   at the gate).
2. **Owner-gated, unchanged from phase 1/2:** `parse-2` (buttons +
   multi-intent), `engine-1` (the runtime inference engine decision
   — llama.cpp + GBNF, TECH_NOTES §1; the dev-time external parser
   carries mode C until then), tune-3 (the three-way NPC-movement
   fork), st-2 (identity persistence), the phase-1 corpus
   consolidation pass, `bg-6` (SoW audit, D-055 deferral), `qa-1`
   mypy + `ci-1` GitHub Actions. NEW for the owner: the Alien
   unknown-axis L6 conflict (DIRECTOR_SPEC §11 — the sketch vs the
   entropy law; resolve before any phase-3+ pacing work reads
   knowledge records).
3. Track B: **bg-2 DONE, bg-3 DONE, bg-4 DONE**, bg-6 owner-deferred.
   New track-B ideas enter the `docs/TASKS.md` backlog on the owner's
   call, never spontaneously. `pack-3` (Sci-Fi sketches) stays parked
   until the 2nd-setting gate. `CORE_ONTOLOGY.md`'s SPECS_BACKLOG
   trigger ("phase-0 gate passed") fired at iter-6, was never
   scheduled, and the just-in-time reading keeps deferring it: write
   specs FROM experiment results at need, not ahead — it stays
   parked.
