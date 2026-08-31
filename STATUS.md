# STATUS — canonsim

Iteration: iter-32 (`iter-32-parse1-say-sessions`) · Phase: 2 (parser,
mode C) OPEN · Date: 2026-09-01 · parse-1 validation beats landed: six
live `say`-door sessions (seeds 125/42/4/23/8/41 — the day-one
walkthrough, the texture pin on a failed take, the texture promotion,
the fire chain, the disambiguation family, the malformed-probe family)
driven by a runner outside the repo through the REAL stack (Simulator +
Mediator + ParserDoor over ONE shared ledger, D-049 — the narrator half
establishes, the player's words reference; the operator IS the external
parser, D-062). PARSER_SPEC §6 tally: 30 utterances, mix 21 intent / 6
question / 2 no_intent; 7/7 deliberate off-grammar probes caught loudly
(off-verb, ghost noun, non-integer ticks, off-enum method, two
alternatives in one document, the CONSUMED texture reference, the
double apply); 0 honest misfires — boundary validity 21/21 = 100% among
intent-alternative replies (questions and no-intent verdicts are honest
outcomes; the mix is the record); 3 door failures are world answers
(take_failed, 2× intent_rejected) + 1 one-path RunnerError after the
pin. The ≥90% valid-intents criterion (ROADMAP §2) is MET on this
volume per the §6 procedure — the phase-2 gate closure stays the
owner's (the phase-1 precedent: criterion hit iter-24, gate closed
iter-26). Live findings pinned in the corpus: a PROMOTED texture entry
is terminal — re-referencing it is off-grammar, the parser takes the
disambiguation path (found live: the operator's first script assumed
the candles still addressable after the take; the boundary refused);
the fire cascade drains INSIDE the door's own run_steps batch
(drop_break cycle: 5 events, last location_burned_out — the iter-23
batch law through the say door). The parse-reply regression corpus
(`tests/fixtures/parse_replies.json`, 6 cases, the narrator-beats
fixture's family) replays through the real doors. KI#54 (the FAQ crept
to 21 entries at iter-31, over the ≤20 cap) opened + closed. Doc-only
streak: 0 (iter-32 carries code + fixture + test). 654→660 green, ruff
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

- KI#54 · FAQ cap drift: iter-31's "Live parse session" entry pushed the
  FAQ to 21 entries (cap ≤20 — AGENTS §6's general rule "check the
  current size before writing" was skipped; the KI#50 family) · opened +
  CLOSED iter-32: the narrate + parse session recipes merged into ONE
  "Live sandbox session recipes" entry (they are one session's two
  doors) → 20; the iter-32 lessons folded in.
- KI#53 · phase-state doc drift (two files): `docs/TASKS.md`'s Track-A
  header still said "Phase 1 … is open" after the phase-1 gate closed
  (iter-26/D-058 — the last update predates the gate-review sweep), and
  `README.md`'s Status paragraph still ended at iter-11a ("Next: the
  narrator LLM call itself") — stale through 15+ iterations incl. the
  phase-1 close (family: a phase-state header nobody re-reads rots
  silently) · opened + CLOSED iter-31: TASKS' header rewritten to the
  phase-2 state; README's Status tail rewritten (phase-1 gate PASS +
  the D-055 narrator boundary + phase-2 open, D-062) + the repo-map
  row gains `brief/parser.py`; the phase-state single owner is this
  file's header — TASKS/README link, never restate.
- (KI#51 deleted at iter-32 per AGENTS §5 — closed bg-4, two
  iterations past; the false-external-citation lesson lives in
  TECH_NOTES §9 + worklog bg-4.)
- (KI#52 deleted at iter-32 per AGENTS §5 — closed bg-4, two
  iterations past; detail in git + worklog bg-4.)
- (KI#50 deleted at iter-28 per AGENTS §5 — closed iter-26, two
  iterations past; the cap-laws citation fix detail lives in git +
  worklog iter-26.)
- (KI#49 deleted at iter-27 per AGENTS §5 — closed iter-25, two
  iterations past; the corpus-description drift lesson lives in
  AGENT_NAVIGATION §1's structural cells + the fixture's `source`
  field, detail in git + worklog iter-25.)

## FAQ / Pitfalls

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
  the batch structure, exactly as the narrator corpus does.

- **Where the code-quality bar lives (D-031).** Law: AGENTS §4+§9
  (invariants, canon-write privilege, DoD). Constitution: BLUEPRINT §2
  (L13/L14). Build clauses: `docs/blueprint/phase0.md` §1/§2/§6.
  Executable: `tests/test_architecture.py` (PACKAGE_DIRS covers every
  top-level code dir — the closure test, D-046) + the stoplist test.
  No new canonical layers (D-018 pattern).
- **GitHub upload / git hygiene (the KI#1 family).** Uploads drop
  `.gitignore` and empty dirs — verify it exists after any upload.
  `git status --short` shows changes vs HEAD, not what IS in HEAD; after
  structural changes run `git ls-files <path>`.
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
  wall-clock in `meta`, no golden DF fixtures. Measured numbers + the
  full recipe: `docs/TECH_NOTES.md` §3.1/§3.2; tools:
  `scripts/df_survey.py` + `scripts/df_import.py`; regression:
  `tests/test_df_survey.py` + `tests/test_df_import.py`.
- **The §6 cap laws: substance over line count (D-025/D-034 — one row
  since the phase-1 collapse) + the ID-preserving gate-collapse.** The
docs cap is 600 with the §6.1 substance filter as the real law — filler
is cut always; named systems, field lists, enum values, per-source
verdicts are never cut to fit. The DECISIONS collapse writes compound
IDs with the FULL prefix on every member (`D-018/D-022/D-029` —
`D-018/022/029` does NOT resolve); compressed rows keep
decision→why→consequence and link the single owner (D-024).
Pre-collapse history lives in git; collapsed 46→30 at the phase-0→1
gate, 41→30 at the phase-1 gate (iter-26); next due at the phase-2→3
gate.
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

**Phase 2 is OPEN.** parse-1 landed iter-32 (six live `say`-door
sessions, 30 utterances, 0 honest misfires — the ≥90% boundary-validity
criterion MET on that volume per PARSER_SPEC §6, the composition
recorded; the parse-reply regression corpus committed). The phase-2
arc, in order:

1. **The phase-2 gate review is the owner's** (the phase-1 precedent:
   the criterion hit at iter-24, the gate closed at iter-26) — more
   parse-1-class session volume only on the owner's call for a deeper
   review; the corpus grows the same way on demand.
2. **`parse-2`** (owner-gated) — disambiguation buttons, multi-intent
   utterances (PARSER_SPEC §7's deferrals; a frontend consumer or
   live-session evidence is the trigger).
3. **Owner-gated, unchanged from phase 1:** tune-3 (the three-way
   NPC-movement fork — the dormant stance stands until the owner
   picks), st-2 (identity persistence), the phase-1 corpus
   consolidation pass, `engine-1` (the runtime inference engine
   decision — llama.cpp + GBNF, TECH_NOTES §1; the dev-time external
   parser carries phase 2 until then), `bg-6` (SoW audit, D-055
   deferral), `qa-1` mypy + `ci-1` GitHub Actions.
4. Track B stays parallel + non-blocking: bg-2 (taxonomy) + bg-3
   (briefer spike) still need the owner's DF export files
   (`dfworlds/` stays outside the repo by design); bg-4 DONE. The
   un-gated, un-blocked backlog is EMPTY — the next move is the
   owner's. `pack-3` (Sci-Fi sketches) stays parked until the
   2nd-setting gate. `CORE_ONTOLOGY.md`'s SPECS_BACKLOG trigger
   ("phase-0 gate passed") fired at iter-6, was never scheduled, and
   the just-in-time reading keeps deferring it: write specs FROM
   experiment results at need, not ahead — it stays parked.
