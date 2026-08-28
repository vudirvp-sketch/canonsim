# STATUS — canonsim

Iteration: 8h (`iter-8h-derived-indexes`) · Phase: 1 · Date: 2026-08-29 ·
owner-directed perf micro-pass: an external patch list (six items) was
verified against the code item by item — each proven semantics-preserving
— then applied (D-050, the single owner of the rationale). Two derived
runtime indexes beside their single mutation funnels: `KnowledgeView`
gains `who → token → source-ids` (maintained in `add`, the only writer;
`holds` drops the row scan — and `before_source` survives: a token
learned only from the excluded source is NOT held, the plain-token-set
variant from the external review would have broken exactly that) and
the Simulator gains `(entity, prop) → last committed tick` (maintained
in `_commit`; the decay pass reads the index instead of scanning the
whole log per NPC-axis — the KI#19 "any committer" baseline unchanged).
Four scan eliminations: `_scene_delta_lines` breaks at the beat-window
edge (ticks are log-monotonic — the writer invariant; one brief-test
fixture fixed to be log-shaped, it encoded an out-of-order log),
`salient()` is a top-1 `max` (first-of-equals ties identical to the
stable reverse sort), `occ_breaking_cause` folds forward once from the
proposal point (strict left fold — O(events), not O(w·events)),
director `entropy` is computed once per `releases()` (was eagerly
recomputed per policy call — pure waste under a rejecting policy:
k+1 identical evaluations per beat). Micro-benchmarks (the D-031
data): decay pass 45×, occ 40×, holds 664×, releases 24×, scene-delta
5×, salient 1.9× at the measured sizes — all asymptotic wins. 340
green (was 338; +2 contract pins, T2 extended to the token index),
ruff clean, golden fixtures byte-identical. KI#33/34/35 deleted (§5,
due since 8h). No new KIs. iter-9 (VALIDATION_SPEC) unchanged.

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

- None. (KI#33/34/35 deleted at iter-8h per §5 — closed iter-8e/8f,
  history in git.)

## FAQ / Pitfalls

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
  survey tool owns the recipe (iter-8e/8f/8g).** Raw CP437 control bytes
  (item-quality symbols) sit inside artifact names — byte-level sanitize
  before any parse; the exporter can die mid-write (no `</df_world>` at
  EOF) — the survey tail-checks and synthesizes the closing tags
  best-effort, loudly marking every count PARTIAL (KI#34); stream with
  iterparse + clear (a non-clearing parse OOMs 4 GB on a 2 GB export);
  main-file type names are display-style, the plus companion's are
  snake_case — normalize. **`--audit` (iter-8g) is the coverage census:
  per-section per-record-tag counts + every unique child-tag set per
  record tag — a structural fingerprint bounded by DF record uniformity
  (typically 1-3 variants; >3 = schema drift signal). Replaces
  head/middle/tail positional sampling strictly — every structural
  variant is captured, not three positions; runs in the same single
  streaming pass as the F7/F8 detail (no second parse). Coverage matrix:
  `docs/ref/df_legends_xml.md`.** Measured numbers + the full recipe:
  `docs/TECH_NOTES.md` §3; tool: `scripts/df_survey.py`; regression
  protection: `tests/test_df_survey.py` (9 tests, synthetic DF-like XML).
- **Substance over line count (D-025) + per-ref split (D-026).** The cap
  is 600 with the §6.1 substance filter as the real law — filler is cut
  always; named systems, field lists, enum values, per-source verdicts
  are never cut to fit.
- **The DECISIONS gate-collapse is ID-preserving (D-034, iter-7 law).**
  Family merges write compound IDs with the FULL prefix on every member
  (`D-018/D-022/D-029` — `D-018/022/029` does NOT resolve); compressed
  rows keep decision→why→consequence and link the single owner of the
  detail (D-024 anti-drift: spec-restatement in a decision row is
  duplication, not substance). Pre-collapse history lives in git.
  Due again at the phase-1→2 gate.
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

**Phase 1 continues** — iter-8c audit verdict: no rework of
iter-1..8 required (the 7th-block landing is additive — assembler +
pack + enum flip atomically per BRIEF_SPEC §9). The plan's single
owner is `docs/TASKS.md`
(Track A: iter-9+ = VALIDATION_SPEC + the validator's LLM-free half —
fact transaction, ExpectedVersion OCC, ≤2 regens, INSUFFICIENT_DATA
default, golden-set plumbing; then the scene-ledger LLM-free half —
`brief/ledger.py` + the `scene_texture` 7th block + fixture-shaped
deltas, per D-048/D-049/blueprint §1 — the hardening gave it complete
inputs (scene definition, structural pinning, the gateway checks, the
tombstone window, the texture-OCC mirror); the narrator LLM boundary
itself remains an AGENTS §8 owner checkpoint, INV-4 holds until then,
and it carries the ledger's live wiring). Track B (`bg-1..bg-4`) stays
unblocked in parallel — bg-1's parsing half is validated (iter-8e: the
owner supplied three worlds — incl. a truncated copy + its complete
re-export, which ground-truth-validated the iter-8f truncation
recovery; `scripts/df_survey.py` + the measured pitfalls in
`docs/TECH_NOTES.md` §3); the iter-8g `--audit` mode + the coverage
matrix in `docs/ref/df_legends_xml.md` give bg-1's SQLite sink the
field plan (HANDLED vs UNHANDLED records + every UNHANDLED child-tag
set) without re-parsing a 5 GB export; so bg-1's remainder is the
SQLite sink over that core (owning its truncation policy — abort vs
flagged partial import); the survey also sharpened bg-2's sampling
frame (`docs/TASKS.md` bg-2, measured tails in TECH_NOTES §3).
Backlog
that did NOT land in iter-8b (each stays in its TASKS home, none
blocks iter-9): `doc-1` VISION freeze review; `qa-1` mypy + `ci-1`
GitHub Actions (owner-gated, AGENTS §8); `perf-1` 10k-tick profile
(the iter-8h micro-pass landed the six locally-provable asymptotic
wins — the full profile remains the gate for anything structural,
e.g. a Path-B revisit); `tune-1` rest action + the D-045(b)
importance-rule knob; the
BRIEF_SPEC §9 deferrals (relevance signal, lore scheduling grammar,
precondition-filtered options, exemplar refresh cadence — all arrive
with the mediator, never early).
