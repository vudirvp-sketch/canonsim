# STATUS — canonsim

Iteration: iter-20 (`iter-20-universality`, owner-directed from the
iter-19 re-audit) · Phase: 1 · Date: 2026-08-30 · The universality
pass: the transition-layer vocabulary (follow-up kinds, flags,
values, the spreading `spot_state`, the spread `halt_flag`) and the
brief scene-line vocabulary (`scene_line_fields`) moved from core
code into pack data (D-057) — a second layer or pack declares its
own words, zero engine edits. Tavern-pack behavior is
byte-identical (the T1 golden fixture untouched, event stream
unchanged); a synthetic `rot` layer (infested/condemned/
stench/collapse — shares nothing with fire's vocabulary) drives the
same engine in tests, and the director's threat sensor reads the
declared `spot_state` set. `layout` landed as a location pack field
rendered canon-from-birth on the scene line — no `initial_projection`
seeding, because the gateway's canon_slot check reads BOTH prop
sources (projection state + pack record): the iter-19 claim was
factually wrong, recorded as KI#48. 547→556 green, ruff clean.
17 files (two subsystems + the sync set — the iter-15 scope
precedent; noted in worklog).

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

- KI#48 · iter-19 doc drift: "layout needs `initial_projection`
  seeding (canon_slot reads top-level fields only)" was FALSE both
  ways — the check (`brief/ledger.py::establish`) reads BOTH prop
  sources (a pack-modeled field was already guarded — KI#41's
  `exits` precedent); the real gap was scene-line rendering
  (promoted props only) · CLOSED iter-20 (phrases fixed in place;
  layout landed as pack data via `scene_line_fields`, D-057).
- KI#47 · ref-9/ref-10 drift family: phantom lift-targets
  (`sim/systems/*.py`, `core/runner.py`, `core/store.py`,
  `content/packs/*.py`) + never-true "phase-0 uses square/fixed
  grid" phrases in `docs/ref/` + `REFERENCES_DEEP.md` · CLOSED
  iter-19 — 9 grid phrases fixed in place (phase-0 = pack-authored
  location graph); lift-target vocabulary stanced in the FAQ below
  (pre-D-028 precedent — plans superseded by D-037/D-023);
  where-things-are owner: `docs/AGENT_NAVIGATION.md` §1.

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
- **Director releases ride the intent door, not the canon door (D-037).**
  A released hook = IntentData (`director_<N>`) through the front door
  (rejections emit `intent_rejected` no-ops with `cause_intent`); the
  director never bypasses Intent→Event. Same door for urgencies
  (`urgency_<N>`).
- **Reactions dispatch from the commit door; novelty is per (knower,
  token) (D-037).** `_commit` feeds the knowledge index + runs `_react`
  for EVERY committed event — no call site can forget a reaction;
  cascades terminate; suspicion reacts only to tokens the knower did not
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
- **The §6 cap laws: substance over line count (D-025/D-026) + the
  ID-preserving gate-collapse (D-034).** The docs cap is 600 with the
  §6.1 substance filter as the real law — filler is cut always; named
  systems, field lists, enum values, per-source verdicts are never cut
  to fit. The DECISIONS collapse writes compound IDs with the FULL
  prefix on every member (`D-018/D-022/D-029` — `D-018/022/029` does
  NOT resolve); compressed rows keep decision→why→consequence and link
  the single owner (D-024). Pre-collapse history lives in git; due
  again at the phase-1→2 gate.
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

**iter-20 closed the universality pass: the transition layer and the
scene line are pack-data-driven (D-057) — of the four bottlenecks
the re-audit named, two are closed (transition kinds/states + the
scene-line filter); the 12-resolver registry and the closed
`core/intent.py` enums remain phase-6 territory (blueprint/phases.md
§6 — declarative resolvers, never before the gate).** Session 5
left the exit criterion at 51 live beats (target ≥100). Next, in
order:

1. **Validation beats, session 6** — volume: the multi-day session (a
   second rotation, day-2 rumor telling at the market — lore + recall
   under a long log) or the alarm-cascade half (an NPC present at the
   fire location so `alarm_raised` fires + the fear markers + the
   shouting-near knowledge for adjacent occupants). Tallies via the
   `BEAT` summary lines.
2. `tune-1` rest action (pack data; the owner's fatigue observation)
   or `st-2` identity persistence per TASKS; `tune-2` (the
   suspicion/crime-status observability candidate) waits for the
   owner; `st-6` shrinks to the `travel` half, phase-5-gated (the
   `layout` half landed iter-20).
3. The runtime-engine decision (llama.cpp + GBNF, TECH_NOTES §1) and
   the `bg-6` SoW audit wait for the phase-1 gate — never earlier
   (ROADMAP §6; the owner's deferral, D-055).

Track B: bg-2 (taxonomy) + bg-3 (briefer spike) query the SQLite sink;
bg-4 (cost notes) is read-only. Infra backlog: `doc-1` VISION freeze
review; `qa-1` mypy + `ci-1` GitHub Actions (owner-gated); `perf-1`
10k-tick profile (the gate for anything structural). `pack-3` (the
owner's Sci-Fi setting sketches) is parked in TASKS until the
2nd-setting gate.
