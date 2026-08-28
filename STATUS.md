# STATUS — canonsim

Iteration: iter-9 (`iter-9-validation-spec`) · Phase: 1 · Date: 2026-08-29 ·
VALIDATION_SPEC written (the phase-1 trigger fired) + the validator's
LLM-free half landed: `brief/validator.py` — a pure function of
(proposal, log, pack), writes nothing, no RNG, no network (INV-1/2/4).
The laws it owns: the CLOSED proposal document (claims + intents +
`expected_event_seq`; no prose field exists anywhere — prompt injection
is neutralized structurally, D-018; loud `ProposalError` on shape drift,
emitter bugs crash); honest verdicts `supported/contradicted/
insufficient_data` against CURRENT canon under closed-world semantics
(invented entity/event = contradicted, unmodeled prop = insufficient —
never fabricated, UAP); ExpectedVersion OCC reusing the intent-door
semantics (stale+broken → refused with first-break attribution;
stale+intact → rebased; knowledge/event claims only grow — only state
claims flip via staleness); the fact-transaction pass-through (intents
shape-checked against the pack grammar, anchors untouched — the door
stays the single commit path, D-037); the ≤2-regens protocol + the
call-budget reconciliation (2-call steady state: narrator + extraction
OR regen; 3-call worst case: narrator + 2 regens; exhaustion → dry mode
L12); golden-set plumbing — `tests/fixtures/validation_golden.json`
pins verdict semantics over the committed smoke log, computed, never
LLM-judged. 390 green (was 352; +38), ruff clean, golden fixtures
byte-identical. bg-1 (SQLite sink) closed the previous iteration; the
scene-ledger LLM-free half is now iter-10 (TASKS re-sequenced).

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
  `sim/`); all setting data in `content/tavern_pack/`; the periphery dirs
  (`render/`, `cli/`, `scripts/`) carry pack paths/help text/prose by
  design (D-046).
- INV-4 LLM boundary: no LLM/network calls in track A — executable against
  every package dir incl. `scripts/` since iter-6a (D-046).
- INV-5 Log immutability: committed logs are never edited; corrections are
  new events.

## Active KIs

- None. KI#36 (bg-1: doc↔tool drift — the UNDOCUMENTED audit marker was
  documented but never implemented; plus the 8g truncation-test comment
  misstatement) — CLOSED bg-1, history in git; deletes at the next
  STATUS-touching iteration per §5.

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
- **Hardcoded `from_` is a desync waiting to happen (KI#13 lesson).**
  Read current values from the projection; make repeat effects
  idempotent; the `_commit` gate (D-035) fails loud BEFORE the write.
- **INV-3's stoplist scope (iter-2 interpretation, test-owned; D-046).**
  The stoplist bans setting nouns in the ENGINE (`core/`+`sim/`),
  segment-matched; mechanic words stay legal; the word list is pack-tied
  by a self-check. `render/`/`cli/`/`scripts/` are periphery — pack path
  strings, CLI help examples, docstring prose live there by design
  (INV-3's substance: a second pack requires zero ENGINE changes).
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
- **Doc drift is evidence, not prescription — verify with
  `git log -S` before acting.** A ref citing a spec section it never
  contained is drift (iter-6a: "AGENTS.md §9 — Script Persistence Rule"
  in README/TEST_PLAN/D-044 — the text bled from the session prompt;
  D-046 supersedes). Pre-D-028 wording and license copies in
  `docs/ref/*`/`REFERENCES_DEEP.md` are historical; the owners are
  AGENTS.md §4 and `REFERENCES.md` (the catalog).
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
- **Content/tone questions → D-030 + the `PACK_SPEC.md` sketch row.**
  Tone is data asymmetry inside existing systems; growing the pack or
  writing a pack spec before its trigger = scope creep (AGENTS §2.4;
  SPECS_BACKLOG header rule). Grim material waits in `pack-1` (phase 6 /
  2nd setting).
- **Doc-loop alarm vs owner-requested research.** Consecutive doc-only
  iterations force a stop (AGENTS §2.5); a fresh owner request is the
  documented exception (D-022). Code iterations never fire the alarm.
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
- **The read-side layers are pure functions of the log (iter-5/6/8 laws).**
  Every render entry point builds a fresh `RngBank` from the log HEADER
  seed — same log → same bytes in any process/`PYTHONHASHSEED`; a
  growing log keeps its rendered prefix (the session delta-print rides
  on this). A session is one opened Simulator: `open`/`run_steps`/
  `close`; session == batch bytes; `seed <n>` starts a NEW log (INV-5).
  `core/metrics.py` reads `(events, projection)` — the simulator never
  knows a metric exists (L3; Mesa DataCollector inverted). The brief
  assembler goes further: **zero RNG at all** (dry structured tokens,
  L2 — `brief/assembler.py`, BRIEF_SPEC §2); its recall `max_items` is
  a ranking cap (the O(relevance) top-k), NOT a budget drop — the
  `[truncated:N]` marker counts budget drops only. **When the 7th block
  lands the purity pair becomes (log, ledger) — the D-049 determinism
  quarantine:** the ledger is session render state (auditable via
  surface/source/cause, never replayable); T1/T2 canon tests never
  touch it; "zero RNG" stays a claim about assembler internals, never
  about log-relative determinism of the ledger-fed brief.
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

**Phase 1 continues on track A** — iter-10 is the next code iteration
(the plan's single owner is `docs/TASKS.md`): the scene-ledger LLM-free
half per D-048/D-049/blueprint §1 — `brief/ledger.py` (entry shape,
scene = PC-location interval, discrete lifecycle, structural pinning,
the validation gateway — scope/establishment-canon/laundering/
unique-slot checks + the idempotent duplicate rule, contradiction
retirement, the texture-OCC mirror) + the `scene_texture` 7th brief
block (pinned-first window + tombstone lines; the BRIEF_SPEC §9 atomic
flip set) + fixture-shaped narrator deltas + pack lint. The gateway
reuses iter-9's refusal shape and regen budget (VALIDATION_SPEC §8).
The narrator LLM boundary itself remains an AGENTS §8 owner checkpoint
(INV-4 holds until then). **Track B: bg-1 CLOSED** (D-051); bg-2
(taxonomy) and bg-3 (briefer spike) are unblocked and query the DB
(`output/df_world_<stem>.sqlite3`; bg-3's reverse validation reuses
iter-9's `invented`/`regen_count` metrics). Backlog (each stays in its
TASKS home, none blocks iter-10): `doc-1` VISION freeze review; `qa-1`
mypy + `ci-1` GitHub Actions (owner-gated, AGENTS §8); `perf-1`
10k-tick profile (the full profile stays the gate for anything
structural); `tune-1` rest action + the D-045(b) importance-rule knob;
the BRIEF_SPEC §9 deferrals that did not land with the ledger
(relevance signal, lore scheduling grammar, precondition-filtered
options, exemplar refresh cadence — all arrive with the mediator,
never early).
