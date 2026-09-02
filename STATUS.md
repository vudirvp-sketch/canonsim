# STATUS — canonsim

Iteration: iter-46 (`iter-46-social2-echo` — the owner's "continue
work per the plan, quality over speed" session call, the phase-3
backlog's top un-gated item: social-2, P3e — the psychological echo) ·
Phase: 3 (Director)
**OPEN — the residue read model landed: the emotional residue of what
an NPC knows, as a pure fold (per-NPC valence, linear decay, fidelity
scaled) driving behavior through the intent door's gate — "a watcher
who saw the fire is jittery next morning", and the residue fades so
events that happened but no longer matter stop driving behavior (the
P3e headline)** · Date: 2026-09-03 ·
Scope: `core/echo.py` (NEW) — the read-side fold: score(who, axis) =
Σ over the knower's records of pack-declared token valence ×
(fades_ticks − age) // fades_ticks × the fidelity percent (integer,
floored; dead AT the boundary tick — the leverage expiry law's twin;
a re-learned token RENEWS — records sum; a vague telling carries a
quarter of the seeing), clamped to the pack scale; zero pairs absent
from the tuple — a missing pair IS zero, the honest answer. The echo
writes NOTHING (no events, no knowledge, no hooks, no state, no
templates, no metrics — INV-1 by construction, the social family's
cleanest landing: iter-44 minted facts, the echo never even does
that); the fold runs ONLY for intents whose preconditions carry the
echo test (the iter-45 laziness — every other action pays nothing);
the L6 fence holds by construction: per-NPC valence over the NPC's
OWN records, never player-adapted, NEVER an entropy input
(DIRECTOR_SPEC §4 — the director reads observable state only; a
knowledge-derived score is not observable). The consumer:
`echo_at_least` (axis, value) — the closed test set's 17th, the P2b
behavior gate (the sketch's "the urge ticker acts on the echo"
dependency); scores duck-typed through `first_failing(...,
echoes=...)` (the import direction one-way — core.intent never
imports core.echo); the window law GENERALIZED: `WINDOWED_TESTS` =
(leverage_over, echo_at_least) — the OCC re-check unconditional for
the family, `occ_breaking_cause` excludes the family (a decay close
never attributes an event the log does not hold); the loop reads each
fold lazily per evaluation point (the door at the entry tick, the beat
gate at the beat tick, the completion at its own). The pack:
`rules.json::echo` — scale [0,100], fidelity_weight over the pack's
own chain (100/50/25), four tokens = the day-1 walkthrough's residue
(the theft sighting dread 25 / wariness 35, fades 720; the
fire-starting sighting dread 60 / wariness 30, fades 1440; the
inferred absence wariness 30; the bar noise wariness 15, fades 360;
papers_unsatisfactory UNdeclared — the iter-44 institutional call,
the crime ladder owns that rung's escalation). Lint: `_echo` (the
closed key sets, the chain coverage, the mintable-token law, non-zero
valence — a sign is legal, zero is dead vocabulary) + the requires
cross-lint on BOTH sides (actions + urgencies: axis declared, value
strictly above the scale floor and at or below the ceiling — a dead
gate refused at load, the leverage `who` family). DORMANT in the
committed content set (the iter-38/42/45 pattern — no action or
urgency carries echo_at_least; the live driver is content-5's row):
the declaration is INERT — the 10-seed day1_full A/B (125 + the nine
corpus seeds, a runner outside the repo per Rule 9) 10/10
byte-identical, ZERO corpus regen (the first social-family landing
with none — the echo writes nothing; iter-44 paid 9 cases because
the mint is event-driven). Measured (crafted driver, seed 93, tuned
token dread 100 / fades 720): the drunk's partial sighting at t=5
reads dread 25 at the beat-360 gate → the driver's look_around fires
once (t=406); the beat-720 read is 0 — the roll silent (the fade
law live); the window-close probe (the ACTION carrying the gate,
ticks 400 — the coerce shape: the door and the OCC re-validate what
the action declares): the door accepts at 405 (residue 22 at the
caller's own tick), the completion at 805 rejects
projection_moved / actor.echo_at_least with the cause chained to the
last committed canon; the committed valence reads real residue on
the committed pack (dread 6 / wariness 8 at the beat-360 read).
KI#67 opened+closed (README's Status froze at iter-43 — "846 tests",
the social rows absent; the KI#66 family, iter-44/45 both skipped
the README sync). Tests 895→924 (+29 tests/test_echo.py), ruff
clean.

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

- KI#67 · doc drift: README.md's Status paragraph froze at iter-43
  ("846 tests green"; the social-depth rows absent — the "Next:" line
  still pointed at social-1/2) — the iter-44/45 doc-sync sets skipped
  the README entirely (the KI#66 family: a count and a status restated
  in a second place, both left stale) · opened 2026-09-03 · CLOSED
  iter-46 (the paragraph actualized: the social-1/1b/2 landings, 924
  green, the Next line re-aimed at the content rows).
- KI#66 · doc drift: `cli/main.py`'s docstring still said "13 actions"
  after iter-43 landed the 14th — the iter-43 doc-sync updated
  MVP_SCOPE/DIRECTOR_SPEC/TASKS but missed the CLI module docstring
  (the KI#65 family: a count restated in a second place) · opened
  2026-09-03 · CLOSED iter-45 (actualized to 15 with coerce's landing).
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

**Phase 3 is OPEN (iter-36..44 — the pacing clock D-065 + the
exit-criterion instrument D-066 + the climax layer D-067 + the
multi-channel split D-068 + the grammar's three layers D-069/D-070/
D-071 + the document_check content set D-072 + the secrets & leverage
fact clusters D-073 landed — the boss beat runs end to end as pack
data, and the social layer mints first-class facts: the room's
knowledge of the theft is now leverage, live in the log and the tale).**
The phase-3 arc in `docs/TASKS.md`'s backlog: `social-1b` (the
leverage use — the coerce door, the fact cluster's first consumer),
then `social-2` (psychological echo, P3e)/`arc-1` (arcs & tension
shaping, P3c); the owner's standing quality directive resolves the
remaining content rows on the documented design — each as its own
iteration: `content-2` (the alarm panic echo, with its corpus regen —
the content-1 precedent), `content-3` (ambient-channel content, its
own row — it did NOT ride social-1). The dir-2/dir-4/drama-1/2/3
measurement's honest finding STANDS SUPERSEDED in part: the
document_check landing is the first deliberate divergence (the check
fires on the runs that reach the confrontation — 1/10 day1_full
seeds; the corpus's seed-93 script fires), and social-1 adds the
second (the same 1/10 hot seed mints the leverage facts — the same
steal failure drives both), while the clock/channel/weight layers
stay inert on day1_full (every run ends in PEAK — a measurable pacing
delta needs a gate-protocol script set that walks the world into
quiet; recorded in D-066, a phase-gate question, not forced).

1. **Phase-3 arc** (TASKS backlog): social-1b (the leverage use) →
   social-2/arc-1 (the social-depth run) → the content rows
   (`content-2` the alarm echo with its corpus regen; `content-3`
   ambient-channel).
2. **Owner-gated, unchanged from phase 1/2:** `parse-2` (buttons +
   multi-intent), `engine-1` (the runtime inference engine decision
   — llama.cpp + GBNF, TECH_NOTES §1; the dev-time external parser
   carries mode C until then), tune-3 (the three-way NPC-movement
   fork), st-2 (identity persistence), the phase-1 corpus
   consolidation pass, `bg-6` (SoW audit, D-055 deferral), `qa-1`
   mypy + `ci-1` GitHub Actions.
3. Track B: **bg-2 DONE, bg-3 DONE, bg-4 DONE**, bg-6 owner-deferred.
   New track-B ideas enter the `docs/TASKS.md` backlog on the owner's
   call, never spontaneously. `pack-3` (Sci-Fi sketches) stays parked
   until the 2nd-setting gate. `CORE_ONTOLOGY.md`'s SPECS_BACKLOG
   trigger ("phase-0 gate passed") fired at iter-6, was never
   scheduled, and the just-in-time reading keeps deferring it: write
   specs FROM experiment results at need, not ahead — it stays
   parked.
