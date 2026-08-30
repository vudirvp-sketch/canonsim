# STATUS — canonsim

Iteration: iter-29 (`iter-29-pack2-spot-available`) · Phase: 1 closed
(gate PASS, D-058; polish open per the owner's finish-phase-1
directive) · Date: 2026-08-31 · pack-2 landed, the third polish item:
the arson-on-ashes door check. The closed precondition set gains
`spot_available` — the target location holds at least one spot of the
pack-declared transition layer NOT in the layer's `spot_state`, the
exact condition the ignite resolver keys on (door and resolver agree
by construction); the arson requires carry it and the `layer` param
is lint-checked against the declared layers. Arson on a destroyed or
fully-burning location is now an `intent_rejected` no-op with
`failed_test target.spot_available` — the door-outcome vocabulary's
fourth axis (no unburning spot, beside not co-located / no flagged
target / no fuel); the iter-24 no-ignition-success probe (a success
that pretended the world changed) is closed. The seed-41 corpus case
flipped with it (renamed, prose + last_event_type updated — provenance
note in the fixture's `source`). 626→629 green, ruff clean. D-061 =
the decision row; DECISIONS transiently 33/30 (collapse due at the
phase-2→3 gate per D-034).

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
- **Live narrate session in the sandbox (operational recipe; iter-24,
  the owner's directive to make the recipe durable).** `python -m cli`
  opens the interactive session; the narrator door is `narrate
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
  same batch structure (session 10's seed-93 cases).

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

**The owner answered the phase-2-vs-polish call (2026-08-31 chat):
finish everything phase-1 first — "если полировка нужна - делай, нужно
закончить все что относится к первой фазе". tune-1 (iter-27, D-059),
tune-2 (iter-28, D-060), and pack-2 (iter-29, D-061) landed; what
remains:

1. **`tune-3`** — no declared candidate (a three-way owner call: a
   v0.2 NPC-movement source / declared-but-dormant / phase-5
   spatial); the dormant stance stands as documented until the owner
   picks. `st-2` and the corpus consolidation pass stay owner-gated
   backlog (not phase-1 exit criteria — the gate passed without
   them).
2. Phase 2 (Parser, mode C: ≥90% valid intents; disambiguation
   questions on uncertainty) opens on the owner's call — the
   code-carrying polish menu (tune-1/tune-2/pack-2) is done; what
   remains (tune-3, st-2, corpus consolidation) carries no declared
   candidate and waits on the owner.
3. **Unlocked by the gate** (owner's call when): the runtime-engine
   decision (llama.cpp + GBNF, TECH_NOTES §1) and the `bg-6` SoW
   audit (ROADMAP §6 lifts with the gate; the D-055 deferral stands
   until the owner calls it).
4. Track B stays parallel + non-blocking: bg-2 (taxonomy) + bg-3
   (briefer spike) query the SQLite sink; bg-4 (cost notes) is
   read-only. Infra backlog: `qa-1` mypy + `ci-1` GitHub Actions
   (owner-gated); `perf-1` 10k-tick profile (the gate for anything
   structural). `pack-3` (the owner's Sci-Fi setting sketches) is
   parked in TASKS until the 2nd-setting gate.
