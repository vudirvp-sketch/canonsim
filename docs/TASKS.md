# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2. Done-detail lives in git
> history + `worklog.md` + the owning docs — never restated here (KI#7
> cleanup, iter-0v). Day-tags removed per D-029 (calendar dropped); the
> build sequence is iteration-counted (`MVP_SCOPE.md` §17).


## Track A — main (simulator, no LLM)

> Phase 0 closed (gate PASS, iter-6; audit-clean iter-6a). Phase 1 closed
> (gate PASS, iter-26, D-058; polish tune-1/tune-2/pack-2 landed
> iter-27–29). Phase 2 closed (gate PASS, iter-35, D-064 — 35/35 boundary
> validity over 51 combined utterances). Phase 3 (Director) CLOSED —
> iter-54, D-083. Phase 4 (Knowledge & scene) CLOSED — iter-65, D-094.
> Phase 5 (Depth) **CLOSED — gate PASS iter-102, D-136** (opened iter-73,
> the owner's start call, D-105; the full build column landed
> iter-73..98, every declared row live; the exit criterion "an emergent
> chain of 3+ events without the player" MET in its worldgen-fed form —
> the armed committed pack; ROADMAP §2 owns the state). Phase 6 (Packs &
> worldbuilder) **PARKED — opens on the owner's call** (the iter-55/73
> opener precedent); the instruments are drafted below.

### iter-102 · phase-5 gate — done (verdict: PASS, D-136)

Full ROADMAP §5 protocol re-run on the owner's exit-review call: 1589
passed + 1 skipped + ruff clean (Python 3.12.14, the env pin); the
seed-125 pair ON M1=0.52 / M2=0.2 (56 events — iter-98's DESIGNED
day1_full price, the LOD's one-gate engagement; the iter-65 record
0.509/0.333/61 events) / OFF T8 24 chains ≥ 3 — the exit criterion MET
in its worldgen-fed form (the armed committed pack: depth-5b genesis +
the year-scale macro arming + the weather chain; rev5's probes +
test_longrun the evidence base; the 60-seed band 15–24, M5 p50 0.79,
stretch max 1 — the phase records hold); T1/T2 on the year-scale log
(test_longrun); T7 the tale reads as a story — the worldgen genesis +
world_history lines open the chronicle; no kill-criteria hit. The §5
step-6 staleness pass: KEEP the rest, REWORD three discharged-phase-0
clauses (AGENTS §1/§4/§8 — INV-4's condition, the phase frame, the LLM
guard → the engine-1 owner gate), DROP none; D-129's effect-line habit
UNEXERCISED (zero protocol-law rows since D-128) — reported per its own
consequence line; D-128's effect lines checked (mech-2 the one still
open, rides the next mechanics touch). The doc debts paid: DECISIONS
collapsed 71→30 (the D-034 gate collapse — the phase-5 build column,
the intake verdict sets, the testproto/protocol rows, the v0.2 lance
folded into families), TASKS collapsed 1240→694 (this pass — the
phase-5 ledger + the intake sections + the phase-3 rows + the Track B
one-liners; the residue over the 600 cap is the closed-phase ledgers'
substance, §6.1), NAV §1 the tests-row lag fixed (the post-iter-86
suites), README resynced. Phase 6 unlocked —
opens on the owner's call. Detail: worklog iter-102 + D-136.

### Phase-5 depth backlog (opened iter-73; CLOSED iter-102 — the rows
collapsed per the header law; the detail lives in git + worklog + the
D-105..D-133 family row + phases.md §5)

- `depth-1`/`depth-1b` · the acquisition gate + arming — done (iter-73/74,
  D-105/D-106). Detail: tests/test_acquisition.py.
- `depth-2`/`depth-2b` · lazy detail materialization + the arming — done
  (iter-75/76, D-107/D-108). Detail: tests/test_detail.py.
- `depth-3` · the scene LOD (three zones, the one-gate law) — done
  (iter-91, D-125). Detail: tests/test_lod.py.
- `depth-4` · fold checkpoints — done (iter-80, D-114; the resume door
  stays owner-gated, phases.md §7). Detail: tests/test_checkpoint.py.
- `depth-5`/`depth-5b` · the ordered worldgen passes + the arming — done
  (iter-81/83, D-115/D-117; D-116 the wave plan). Detail:
  tests/test_worldgen.py.
- `depth-6` · factions with goals — done (iter-92, D-126). Detail:
  tests/test_factions.py.
- `depth-7` · groups & simulation LOD — done (iter-93, D-127). Detail:
  tests/test_groups.py.
- `bridge-1` · the scene-line projection pipe — done (iter-86, D-120).
  Detail: tests/test_brief.py + tests/test_worldgen.py.
- `chron-2` · the history bridge (the DF legends shape, the cause tree) —
  done (iter-87, D-121). Detail: tests/test_worldgen.py.
- `place-1` · the placement discipline (claim↔exits consistency) — done
  (iter-88, D-122). Detail: tests/test_worldgen.py.
- `geo-1` · the geometry rework (grid-hash walk, 10k sites 1.19 s) — done
  (iter-89, D-123). Detail: tests/test_worldgen.py + TECH_NOTES §12.
- `maclock-1` · the macro-clock primitive — done (iter-90, D-124).
  Detail: tests/test_macro.py.
- `name-1` · the name generator + the condensation consumer — done
  (iter-96, D-131; the ref-19 dives landed with it). Detail:
  tests/test_names.py.
- `st-6(a)` · travel as a separate action — done (iter-97, D-132).
  Detail: tests/test_travel.py.
- `weather-1` · the ambient weather family + canon erosion + the
  committed macro arming — done (iter-98, D-133). Detail:
  tests/test_weather.py.

> Phase 5 (Depth) landing ledger, condensed: the acquisition + lazy-detail
> family iter-73..76 (D-105..D-108), the fold checkpoints iter-80
> (D-114), the worldgen passes + arming iter-81/83 (D-115/D-117; D-116
> the wave plan + D-119/D-128/D-130/D-134/D-135 the intake verdict sets
> routed between queue rows), the four W1 bridges iter-86..89
> (D-120..D-123), the macro clock + its consumers iter-90..93
> (D-124..D-127), the W2 tail iter-96..98 (D-131/D-132/D-133 — name-1,
> st-6a, weather-1 with the committed macro arming); the build column
> completed at iter-98, the queue empty of live candidates, the gate PASS
> at iter-102 (rev5 iter-99 the pre-gate evidence base). Architecture
> owner: `docs/blueprint/phases.md` §5; exit criterion "an emergent chain
> of 3+ events without the player" (ROADMAP §2 — MET, the worldgen-fed
> form). Detail: the D-105..D-133 family row + the per-row owners above +
> worklog + git.

### Phase-6 parked instruments (W4, owner-gated; the phase-6 backlog
drafts from phases.md §6 at the opening iteration)

- `resume-1` · the session resume door — done (iter-106, the owner's
  «приступай к реализации» on the iter-105 chat's risk-analysis
  priority list, the cli-pack direct-call precedent): `--resume <log>`
  opens the session OVER an existing log (D-139 — resume is invisible
  to the log); the run cursor (`core/cursor.py`, the entropy state no
  fold recovers) + the checkpoint fast-path (the module's first
  runtime consumer) + the append-mode writer; the landing record: the
  iter-106 section below.
- `cli-pack` · the CLI `--pack` flag — done (iter-105, the pinned
  streak-breaker, D-137/D-138 riding the same call): every
  pack-loading command + the session take the flag, the tavern
  default byte-identical, a bad path refused loudly; the stoplist
  docstring's config claim TRUE (the landing record: the iter-105
  section below).
- `world-2` · the second world, the phase-6 gate's own instrument —
  todo, owner-gated: the TWO-LEVEL gate — level 1 the T1 reskin ≤ 1 day
  (ROADMAP §2's phase-6 exit, measured on the open generic stack), level
  2 the deep second world (weeks — VISION §7's honest twin): a fantasy
  province at pack scale, authored pillars over a generated surface
  (phases.md §6 — D-130's province sketch; the st-6a/travel + name
  profiles arming ride this row's cultures half). The phase-5 exit
  needed NO second world (the emergent chain rode the armed committed
  pack). iter-103 audit notes, resolved iter-104 (the owner's
  fork-analysis call): the CLI `--pack` prerequisite lands at iter-105
  (`cli-pack` above); the stoplist self-check extension stays the
  reskin day's own step; the toponym question resolved by the
  OVERRIDE-ELSE-DERIVED law (the travel price's own family, D-132):
  authored toponyms WIN (level 1 authors everything — speed is the
  gate's own shape), else the name MINTS from the declared profiles
  through a named cosmetic stream (INV-2's law: deterministic per
  seed, never desyncs canon) at the render surfaces that need it —
  the dogfooding line held (the province's name IS minted from its
  profiles, phases.md §6), zero canon events, zero corpus price; no
  genesis birth, no grammar-trigger extension (the npc-only +
  condensation-gated grammar stays untouched — the mint is
  render-side, never a canon materialization).
- `res-1` · the resource/economy layer — todo, owner-gated (VISION §6's
  "scarcity" formula word gets its row owner): the closed scarcity cycle
  (source → flow → sink) as PACK DATA — the dependency graph, flows as
  aggregate macro-events on maclock cadence, sinks via the irreversible
  item laws, price spreads as derived read-side values; never a second
  economy engine beside the canon door (D-116; Dune's critical-resource
  binding the declaration shape, D-119). Deep dives owed at the phase-6
  opening (ref-18/ref-20, DEEP §1).
- `roads-1` · the generated-exits pass — todo, owner-gated (phase
  6/mode G): mode G must EMIT exits for generated worlds (hand-authoring
  a generated world's edges is impossible); an MST/k-nearest graph over
  the sites (the Red Blob family); a PASS_ORDER growth = a D-row when it
  lands; authored packs keep manual exits (the pack wins). iter-104
  resolves the READ-PATH fork (the owner's combined-variant call):
  the derived L3 read WINS, sharpened — the pass-computed graph lives
  on the WorldModel (L11: derived, rebuildable, never truth; replay
  rebuilds it from the header seed + pack, the pure function); the
  consumers (the LOD warm ring, the intent door's move validation,
  travel's edge lookup) re-point through ONE shared read with the
  pack-wins override — `exits(location)` = the authored record if
  declared, else the pass-derived edges mapped through the site
  claims (deterministic order); place-1's claim↔exits invariant
  RELOCATES into the pass for the generated half (asserted at emit,
  where the data is born — relocated, never weakened; the load lint
  unchanged for authored packs). NO canon births for exits:
  seed-dependent derived data stays out of the log (INV-1 untouched —
  the read is runtime L3, the fold never needs it; no event-id
  shifts, no M3/M5 inflation, corpus price zero by construction; the
  `world_formed` outcome block stays as-is).

> W3 closed without new rows (the calendar binding is maclock-1's own,
  D-116); directions are pack data over the graph today. intake-8's
  setting sketch rides world-2's level-2 half (D-130).

### iter-106 · resume — done

The owner's direct call («приступай к работе и реализации», the
risk-synthesis priority list's #1 — the checkpoint-resume wiring;
splitting across iterations licensed, quality first): the session
resume door, the one phases.md §7 left owner-gated since iter-80.
Verified BEFORE working (1592+1 green, ruff clean, HEAD c7508f5,
Python 3.12.14). The law (D-139): **resume is invisible to the log**
— interrupted at a clean drain boundary and resumed with the same
remaining steps, the session is byte-identical to the uninterrupted
run (T1 across process boundaries; pinned at every split point,
directors on and off). The mechanism, two artifacts by nature:
the CURSOR (`core/cursor.py` — new) carries the entropy-and-clock
state no fold recovers (silent draws: urgency misses, weather
self-rolls, faction failures consume stream positions without
events; bank positions via `RngBank.export_state`/`restore_state`
— worldgen streams excluded, `generate_world` re-derives them,
its purity the enabling fact; director run marks via
`export_run_state`/`restore_run_state`, the buffer itself rebuilt
exactly by `seed()` over the log), bound to its log by `event_count`
+ `prefix_sha256` (a stale pin refuses loud — guessing entropy is
save-scumming, not determinism); the CHECKPOINT fast-path
(`Simulator.resume` → `core/checkpoint.py`'s first runtime consumer)
restores the projection as snapshot + tail when the operator's
`output/checkpoints/<stem>/` artifacts exist and anchor cleanly —
absent is normal operation (the plain fold), present-but-wrong is
loud. The writer's append mode (`core/log.py`) rides the same canon
door: read_log validates every line before the file is touched,
the schema-version + env-pin header laws refuse a foreign
continuation, committed lines are never rewritten (INV-5). The
session pins the cursor after every command and at close, only at
a clean drain boundary (`Simulator.drained`; a mid-drain crash
leaves the last clean pin — a later resume over the grown log
refuses loudly). The scene ledger stays session-scoped (D-049):
a resumed session opens a fresh ledger; live texture dies with its
session, promoted texture rode events. `cli/main.py`: `--resume`,
the resumed banner, the delta discipline (new chronicle lines
only). `core/queue.py`: QueueKind gains `weather` (the iter-98
Literal drift, one word). `tests/test_resume.py` +19: the law at
splits 0/1/2/3 + the directors-off arm; the cursor/rng/director
unit refusals; the CLI e2e + the missing/stale/foreign-pack/env-pin
loud refusals; the fast-path + the corrupt-artifact anchor teeth.
1611+1 green, ruff clean; corpus price zero (no fixture regen, the
armed pack's genesis rides the split-0 arm itself). 12 files —
6 core + 1 test + 5 doc (AGENTS §2.3: the objective scope — a
genuine system feature, one coherent landing, noted in worklog).
Zero new KIs.

### iter-105 · cli-pack — done

The pinned streak-breaker (the owner's «поехали» on the iter-104
pin): the CLI `--pack` flag, periphery only. Verified BEFORE
working (1589+1 green, ruff clean, HEAD 08faec2, Python 3.12.14).
`cli/main.py`: every pack-loading command (play/chronicle/state/
replay) + the interactive session take `--pack <dir>` — the
top-level default `content/tavern_pack`, the subparsers
`argparse.SUPPRESS` (the flag honors both orders, before or after
the subcommand — no default clobber); the loud refusal lives in
`_load` (a path that is not a directory exits 1 naming it, BEFORE
any world opens; a directory that is not a pack keeps load_pack's
lint refusal). `tests/test_cli.py` +3: the explicit tavern pack
byte-identical to the no-flag run; the bad-path refusal (batch,
session, and the before-subcommand order — no log born); the
read-side subcommands (chronicle/state render, replay refuses a
non-pack dir). 1592+1 green, ruff clean; corpus price zero
(periphery plumbing, zero draws, no fixture regen). The stoplist
docstring's "the CLI takes the pack dir as config" claim TRUE —
the drift dead at its root. The same owner call verdicted the two
standing questions (one DECISIONS line each): D-137 the Alien
unknown-axis L6 conflict (the OBSERVABLE-answers law, DIRECTOR_SPEC
§11 re-pointed), D-138 the D-081 climax flag (the peak's END
marker). 7 files — 2 code + 5 doc (the verdict set riding the
iteration; AGENTS §2.3: the objective scope noted in worklog).
Zero new KIs. The stoplist self-check extension to a new pack's
nouns stays with the reskin day itself (the second pack must exist
for its vocabulary).

### iter-104 · owner-called fork analysis — done (doc-only)

The owner's chat call: every open question and fork worked into a
final COMBINED variant (the owner's stated preference — one variant
gathering the pros, neutralizing the cons, no crutches). Verified
BEFORE working (1589+1 green, ruff clean, HEAD 13c23c4, Python
3.12.14). Routed into the rows above: `cli-pack` pinned iter-105
(pre-opening, the streak-breaker), the roads-1 read-path fork and
the world-2 toponym question both resolved under the ONE
override-else-derived law family (the travel price's own, D-132 —
pack-authored data wins, else the (seed, pack)-derived read),
since-1 routed to phase 6 (world-2's condensing travelers the first
real consumer). The two standing owner questions (DIRECTOR_SPEC
§11's L6 conflict, D-081's climax flag) NOT silently resolved —
combined-variant proposals delivered in chat, the owner decides —
the verdicts landed at iter-105's call (D-137/D-138, one line
each).
Zero new KIs. The doc-only streak surfaced per AGENTS §2.5: this is
the fifth, the owner's own call again (D-022); iter-105 is pinned
CODE.

### iter-103 · owner-called phase-6 plan audit — done (doc-only)

The owner's chat call: phase 6 + the project re-checked from the
height of the landed solutions, heightened plan-detail attention
(nothing missed, no errors, no contested points needing rework).
Verified BEFORE working: 1589+1 green, ruff clean, HEAD e6c95ff
(Python 3.12.14, the env pin). Verdict: **COHERENT — the phase-6
opening stands on solid ground.** The instruments agree across
TASKS / phases.md §6 / ROADMAP §2; the D-134/D-135 consult material
verified against its landed owners (on_action, hooks buffer, arcs,
the cause tree, the cold tiers, rotations, the folds, the erosion
family); res-1's dependencies all landed (the maclock cadence, the
aggregate surface, derived read-side values, the ratio dynamics);
no TODO/FIXME residue; the owed items already recorded (PACK_SPEC
trigger, ref-18/ref-20 just-in-time). Four detail findings routed
into the rows above: the st-5 stale pointer (re-pointed below),
the CLI `--pack` flag (world-2 level-1's prerequisite; the
stoplist docstring's config claim is drift), the roads-1 read-path
fork, the name-1 toponym question. Zero new KIs — plan-detail
notes, not defects. The doc-only streak surfaced per AGENTS §2.5
(the owner's own call, the D-022 exception).

### Research intakes 4..10 — routed, collapsed at the phase-5→6 gate
(the verdict-set detail lives in the D-rows + git; the external texts
stay outside the repo — the convenience-copy law; the queue itself was
never touched by an intake)

- `intake-4` (iter-73) — routed: the phase-5 synthesis cross-review; the
  two additions landed inside depth-1/depth-4's rows (the sha256 anchor,
  the pack-declared margins). Verdict set: D-105.
- `intake-5` (iter-82) — routed: the generator-concept verdict set — the
  13 questions resolved, the W0..W4 wave plan, the spatial model pinned
  as phase law. Verdict set: D-116.
- `intake-6` (iter-85) — routed: the consolidated-analysis residue —
  REFERENCES §10 +3 (Dune, WH40k, Outer Wilds refuted); the deferred
  residue rides the W4 rows. Verdict set: D-119.
- `intake-7` (iter-94) — routed: the Anthropic-2026 agent corpus —
  ROADMAP §5 step 6 adopted (the gate staleness pass), MVP_SCOPE §18 the
  actionable-error law, `mech-2` the one backlog row; the platform
  plumbing refused with cause. Verdict set: D-128/D-129.
- `intake-8` (iter-95) — routed: the three-tier setting posture + the
  minus ledger + REFERENCES §10 +6; no new rows (rides world-2/res-1/
  roads-1/PACK_SPEC). Verdict set: D-130.
- `intake-9` (iter-100) — routed: the TTRPG cross-media analysis — the
  cost/failure/corruption pack laws + the parked loop-pack/low-magic/
  soul-scar/belief-as-rules patterns (phases.md §6). Verdict set: D-134.
- `intake-10` (iter-101) — routed: the encounter & event-generation
  design notes — the substrate CONFIRMED complete, `since-1` the one
  genuine gap, the four contradictions dissolved. Verdict set: D-135.

- `since-1` · the re-encounter delta — the "what happened since last
  meeting" surface — todo, owner-gated (read-side, v0.2-grade; gate: the
  phase-5 exit review passed — the gate is now OPEN on the owner's
  direct call): a per-entity line family on the brief's entity cards
  (BRIEF_SPEC §3.4's extension) + the scene card, derived at assemble
  time from the fold (status-axis deltas, position/membership transfers,
  relation flips since the last co-presence tick) and the knower's own
  records (what they heard) — the world-simulated half already runs
  (macro ticks, urgencies, rotations); this row renders it on
  re-encounter. Zero canon writes, zero streams, zero corpus price by
  construction (read-side); the pack declares the line vocabulary. The
  source text's pattern #16, its own single-highest-value pick. iter-104
  routing (the owner's fork-analysis call): the surface lands IN phase
  6 — world-2's condensing travelers are the first real consumer (the
  tavern pack's re-encounter surface is too thin to author the line
  vocabulary against: the leave/return pair + static NPC placement,
  the tune-3 finding); the fold deltas it reads all exist today, zero
  pre-opening work owed. Detail: D-135 + phases.md §6's encounter
  block.

### iter-77 · meta-analysis routed candidates — LANDED (iter-79, the
owner's verdict call; the detail lives in git + worklog + D-110..D-113)

- `pred-failclosed` · done (iter-79, D-110) — missing → False under ALL
  comparators in both twins.
- `pred-contract` · done (iter-79, D-111) — the ValueError backstop on
  every raw-read surface.
- `seq-owner` · done (iter-79, D-113) — ORDER → STATUS Next step;
  composition → TASKS.
- `rule9-resolver` · done (iter-79, D-113) — Rule 9 defined in-repo
  (AGENTS §7).
- `verify-seed` / `archive-protocol` · done (iter-79, chat-side per
  D-113) — the bootstrap text's own lines; repo untouched.
- `tn12-claim` · dropped (D-113) — every proposal already had an owner.
- Re-raise guard (iter-78): the ignore-list ruling stands — re-flag only
  with NEW measured evidence.

### v0.2 refinement backlog (opened iter-66; closed at iter-72 — the
lance folded into the phase-4 family row at the phase-5→6 gate; the
per-row detail lives in git + worklog + the D-095..D-104 compound)

- `prosefloor` · done (iter-66, D-095). Detail: VALIDATION_SPEC §2.1.
- `beliefwire` · done (iter-67, D-097). Detail:
  tests/test_beliefwire.py.
- `beliefwire-2` · done (iter-70, D-103 — the arming, the price paid
  in-landing). Detail: tests/test_beliefwire.py.
- `rumordrift` · done (iter-68a/68b, D-099/D-100 — the mechanics + the
  arming). Detail: tests/test_rumordrift.py.
- `suspectaxis`/`suspectaxis-2` · done (iter-69/69b, D-101/D-102 — the
  mechanics + the arming, the corpus price paid in-landing). Detail:
  tests/test_suspectaxis.py.
- `testproto` · done (iter-68, D-098 — research, doc-only). Detail:
  TEST_PLAN §8.
- `prosefloor-2` · done (iter-72, D-104). Detail: VALIDATION_SPEC §2.1 +
  tests/test_scan.py.
- `packtaxonomy` · material-derived props — owner-gated (phase-6
  PACK_SPEC: the `copy-from` chain; phases.md §6).
- `story-critical objects` · the pack flag + a release path — owner-gated
  (phase-5+; DIRECTOR_SPEC — events already carry the arc/hook family).

### Research intakes 2/3 — routed, collapsed at the phase-5→6 gate

- `intake-2` (iter-66a) — the depth-architecture review; D-096 records
  the corrections + the routing. Verdict set: D-096.
- `intake-3` (iter-71) — the vision-vs-repo cross-review; the two
  confirmed holes routed (weather-1, companion-1). Detail: D-119's
  family + git.
- `weather-1` · done (iter-98, D-133). Detail: tests/test_weather.py +
  phases.md §5.
- `companion-1` · the companion/party role — todo, owner-gated: pack
  data over the existing doors, zero new core systems — follow-duty in
  the rotation/urgency grammar, mode B actors voice (scene-1), pair-axis
  relations, presence re-verification (iter-61), the arrival-snapshot
  knowledge records (iter-15/D-056 — what §5 still owns is the
  group-scale form). Dependencies BY REFERENCE: tune-3, st-6a, the
  resume door (phases.md §7). Gate: phase 5 closed — the owner's call
  whenever.

### Phase-4 backlog (opened iter-55; CLOSED iter-65)

- `leg-1` · trait crystallization (P3f) — done (iter-55, D-084):
  the belief-token fold. Detail: the D-084..D-093 family row +
  tests/test_traits.py.
- `leg-2` · the brief's derived-trait read — done (iter-56, D-085):
  belief lines lead recalled_facts. Detail: BRIEF_SPEC §3.5 +
  tests/test_brief.py.
- `leg-3` · reflection & memory compaction — done (iter-57, D-086):
  reflection-on-recurrence through the canon door. Detail:
  LEGEND_SPEC + tests/test_reflection.py.
- `leg-3b` · the tavern reflection set — done (iter-58, D-087): the
  arming, `conclusion_drawn` story-critical. Detail: LEGEND_SPEC §7 +
  tests/test_reflection.py.
- `retr-1` · the retrieval ladder (STORE-1) — done (iter-59, D-088):
  FTS5 + the vec probe/scan/floor chain + the re-ranker; `knower` IS
  known_by. Detail: tests/test_retrieval.py + phases.md §4.
- `scene-1` · the scene manager + mode B — done (iter-60, D-089):
  the chorus queue + the knower parameter. Detail: BRIEF_SPEC §3.9 +
  tests/test_scene.py.
- `scene-2` · the mode-B session wiring — done (iter-61, D-090):
  the drain + the actor reply door + the keyword query. Detail:
  BRIEF_SPEC §3.9/§7.1 + tests/test_scene.py.
- `tex-1` · the texture identity tier + quotas — done (iter-62,
  D-091): `identity_slots` + `per_entity_max_items`. Detail:
  BRIEF_SPEC §3.3/§6 + tests/test_brief.py.
- `leg-4` · mode F offline chronicler — done (iter-64, D-093):
  `scripts/chronicle.py`, the [chronicler] extra, D-012 executable.
  Detail: TEST_PLAN §7 + tests/test_chronicle.py.
- `blind-1` · the blind-NPC leak suite's phase-4 extension — done
  (iter-63, D-092): the exit criterion's instrument. Detail:
  TEST_PLAN §1.3.
- `scav-1` · offline compaction = scavenge with tombstones (the
  EventStore shape, phases.md §4's later half): derived-store entries
  drop with tombstones AFTER the chronicler's rollups make them
  rebuildable; committed logs never edited (INV-5). Out of leg-4's
  named scope by the scope-creep law — deferred here, not forced.

> Phase 4 (Knowledge & scene) landing ledger, condensed: the folds
> iter-55..58 (D-084..D-087 — traits, the brief's belief read,
> reflection-on-recurrence, the tavern arming), the retrieval ladder
> iter-59 (D-088), the scene stack iter-60..62 (D-089/D-090/D-091 —
> mode B + the chorus queue, the session wiring, the identity tier),
> the leak suite's instrument iter-63 (D-092), the mode F chronicler
> iter-64 (D-093 — the owner's duckdb approval crossing the §8 fence,
> the chronicler outside the runtime graph); the build column
> completed at iter-64, the gate PASS at iter-65. Architecture
> owner: `docs/blueprint/phases.md` §4; exit criterion "0 leaks on
> the blind-NPC suite" (ROADMAP §2 — MET). Detail: the
> D-084..D-093 family row + the per-row owners above + worklog +
> git (the pre-collapse detail lives there, KI#7 law).

### iter-65 · phase-4 gate — done (verdict: PASS, D-094)

Full ROADMAP §5 protocol re-run on the owner's call: the corpus 105
+ parse corpus green (1178 tests collected — 1168 passed + 1 module
skip pure-dev, 1177 passed + 1 offline-probe skip with the
[chronicler] extra; ruff clean); the seed-125 pair ON M1=0.509 /
M2=0.333 / OFF T8 26 chains ≥ 3 — IDENTICAL to the iter-54 record
(the phase-4 landings kept the corpus-price-zero promise on the
committed scenario); the stretch table max 1 (both arms — the
phase-3 exit criterion holds, no regression); T1 double-run
byte-identical; T7 reads as a story; the exit criterion re-measured
— 0 leaks on the blind-NPC suite (all four layers); the mode-F
chronicler acceptance green (TEST_PLAN §7: 53/53 through the count
gate, manifest content-derived, write_mode=stdlib in the offline
env). The doc debts paid: TASKS 626→589 (the phase-4 ledger
collapse — the deferred trim landing at its promised gate),
DECISIONS 30 held (D-094 joins the verdict family), FAQ 20 held,
README resynced (KI#73 — three landings had gone unrecorded).
Phase 5 unlocked — opens on the owner's call. Detail: worklog
iter-65 + D-094.

> Phase 3 (Director) landing ledger, condensed: the pacing stack
> iter-36..39 (D-065..D-068), the event grammar iter-40..42
> (D-069/D-070/D-071 — predicate/weight, options, on_action), the
> social stack iter-44..46 (D-073/D-074/D-075 — secrets, leverage,
> the echo), the arcs iter-47 (D-076), the content column
> iter-43/48/49/51/52/53 (D-072/D-077/D-078/D-080/D-081/D-082 —
> every layer and declared channel dimension live); the build column
> completed at iter-53, the gate PASS at iter-54. Architecture owner:
> `docs/blueprint/phases.md` §3; runtime contract owner:
> `docs/DIRECTOR_SPEC.md`; exit criterion "a scene without an event
> < N beats" (ROADMAP §2). Detail: the D-083 compound row + worklog.

### Phase-3 director backlog (opened iter-36; CLOSED iter-54 — the rows
collapsed per the header law at the phase-5→6 gate; the detail lives in
the D-065..D-082 compound row + DIRECTOR_SPEC + git)

- `dir-1` pacing clock — done (iter-36, D-065). Detail: DIRECTOR_SPEC §5.
- `dir-2` the eventless-stretch instrument + the A/B harness — done (iter-37, D-066). Detail: TEST_PLAN §6.
- `dir-3` layered thresholds + PEAK_CLIMAX — done (iter-38, D-067). Detail: DIRECTOR_SPEC §5.
- `dir-4` multi-channel policies — done (iter-39, D-068). Detail: DIRECTOR_SPEC §5.
- `drama-1` the predicate + weight layer — done (iter-40, D-069). Detail: DIRECTOR_SPEC §3/§3a.
- `drama-2` the grammar's option layer — done (iter-41, D-070). Detail: DIRECTOR_SPEC §3b.
- `drama-3` the on_action dispatch layer — done (iter-42, D-071). Detail: DIRECTOR_SPEC §3c.
- `content-1` document_check — done (iter-43, D-072).
- `social-1` secrets & leverage — done (iter-44, D-073).
- `social-1b` the coerce door — done (iter-45, D-074).
- `social-2` the echo engine — done (iter-46, D-075).
- `arc-1` arcs & tension shaping — done (iter-47, D-076).
- `content-2` the alarm panic echo — done (iter-48, D-077).
- `content-4` the coerce driver — done (iter-49, D-078).
- `content-5` the echo driver — done (iter-51, D-080).
- `content-6` the arc driver — done (iter-52, D-081).
- `content-3` the ambient driver — done (iter-53, D-082).

### iter-54 · phase-3 gate — done (verdict: PASS, D-083)

Full ROADMAP §5 protocol re-run: the corpus 105 + parse corpus green
(973 tests, ruff clean); the seed-125 pair ON M1=0.509 / M2=0.333 /
OFF T8 26 chains ≥ 3; the stretch table max 1 (both pacing arms + the
quiet-walk stage — the D-066 question answered); T7 reads as a story.
The doc debts paid: DECISIONS 48→30, FAQ 23→20, TASKS 854→510,
DIRECTOR_SPEC 641→593, phases.md kept over per §6.1 (the worklog
records why). Phase 4 unlocked — opens on the owner's call. Detail:
worklog iter-54 + D-083.

### Phase-2 parser backlog

- `parse-2` (owner-gated) disambiguation buttons + multi-intent
  utterances — deferred with a frontend consumer / live-session
  evidence (PARSER_SPEC §7).
- `engine-1` (owner-gated) the runtime inference engine decision
  (llama.cpp + GBNF; TECH_NOTES §1) — unlocked by the phase-1 gate,
  waits on the owner; the dev-time external parser carried phase 2 to
  its gate PASS (iter-35) and carries mode C until then.

### iter-26 · phase-1 gate — done (verdict: PASS, D-058)

Full ROADMAP §5 protocol re-run: 109 live beats / 0 canon violations /
corpus 105 green; DECISIONS collapsed 41→30; `doc-1` closed clean;
phase 2 unlocked. Detail: worklog iter-26 + `docs/DECISIONS.md` D-058.

### Phase-1 tuning backlog (post-assembler, owner-gated)

- `tune-3` alarm-adjacent reachability (iter-21 session finding):
  `transitions.fire.knowledge.alarm_adjacent` (`shouting_near_<loc>`)
  is structurally unreachable in v0.1 — the token needs a knower
  adjacent to the fire location at ignition, but NPC placement is
  static (the rotation is a direct duty↔rest swap, playscript steps
  are player-only, urgencies are all waits), so the street/backyard
  are never occupied when the fire starts; the same-location half
  (alarm + fear spike) fires fine and is corpus-pinned. Session 8
  (iter-23) pinned the same family live on the §3 rumor leg: the
  market crowd holds no `figure_at_back_door_last_night` — the
  drunkard never leaves the tavern (the refusal is corpus-pinned,
  the boundary probed, not forced). Owner's
  call: a v0.2 pack NPC-movement source (e.g. a transit route
  through the street), leave as declared-but-dormant layer
  vocabulary (a second pack may exercise it), or phase-5 spatial
  material.

(tune-1 done iter-27, tune-2 done iter-28 — see Done.)

### Stress-test backlog (iter-11b resolutions; owner-gated)

- `st-2` identity persistence: the identity promotion door (pack
  grammar beyond `take`, the D-054 machine; blueprint §1) — the
  read-path half (the window tier + per-scope quotas) landed as
  `tex-1` (iter-62, D-091); only the door remains. Optional
  second trigger (bg-5): repetition-counted promotion — N repeats of
  a priced pattern via a counted fold (the ref-13 GHOST-layers
  counter pattern); owner's call: alongside or instead of the
  pack-grammar door.
- `st-3` groups & simulation LOD: one id across tiers, aggregate
  macro-clock events with cardinality, condensation on crossing
  (GROUP_SPEC trigger = phase 5 or owner request; blueprint §5).
- `st-4` the call budget (head + brief + tail + thinking + output ≤
  MECW target) + the transcript-tail contract + thinking-as-ephemeral-
  texture (the narrator-boundary iteration; blueprint §1) + the Script
  Tax clause (bg-5): non-Latin tail/prose costs ≈1.5–2× tokens on
  32K-vocab local models (guide part_07a §7A.5; ref-13) — the
  whitespace proxy under-charges Cyrillic; budget per script at the
  mediator, never in core.
- `st-5` containers: the `in` relation + entity-birth promotion
  (blueprint §7 — "deferred with the depth phase"; phase 5 CLOSED
  iter-102 without this row landing, the pointer retired at the
  iter-103 audit: unowned by a phase now — the first real consumer
  decides (a pack wanting portable objects, a res-1 sink shape),
  never a speculative build).

### Spatial backlog (owner-gated; audited iter-19)

- `st-6` spatial vocabulary — `travel` + `layout`. (a) `travel` as a separate action, NOT weighted `move` — done (iter-97, D-132: the movement TWIN with an edge price — `ticks: "edge"` the fourth action-vocabulary value; `core/travel.py` the price law: override wins per edge, else the derived integer function of the WorldModel, the MIN cross-pair, draw-free; the crossings fire mid-travel D-038; the committed pack unarmed — the arming rides world-2's province row). +18 tests, 1546→1564+1 green, corpus price zero. Detail: tests/test_travel.py + D-132. (b) `layout` — LANDED iter-20 (D-057/KI#48):
  **`layout` — LANDED iter-20 (D-057/KI#48)**: a top-level pack
  field on every location rendered canon-from-birth on the scene
  line via `brief.present_entities.scene_line_fields` — no
  `initial_projection` seeding (the iter-19 claim that the gateway's
  canon_slot reads top-level pack fields only was WRONG: the check
  reads both prop sources, and a pack field was already guarded —
  the `exits` precedent, KI#41); the validator adjudicates claims on
  it; mutable decor stays texture (the existing door).

### iter-6 · gate — done (phase-0 verdict: PASS)

Phase-0 gate closed; full evidence in `worklog.md` iter-6 + the
`docs/TEST_PLAN.md` spec. Track A was feature-frozen at phase-0 scope;
phase 1 (narrator over the log) opened per `docs/ROADMAP.md` §2.

## Track B — background (evenings, foreign canon)

### bg-7 · engine + confabulation probe — done (2026-09-07)

- Done one-liner: all five probes' FIRST NUMBERS on the sandbox API engine (glm-4-plus) — TECH_NOTES §10; the {3–8B, GBNF} arm the gap row; runner + transcripts outside the repo (Rule 9).

### bg-8 · engine — the LLM-integration test runner — done (2026-09-09)

- Done one-liner: the testproto live half — the deviation corpus F1–F6 through the REAL mode-C door: the world-answer law's first live numbers (coverage 34/34 = 100%, honest 17/36) + the heartbeat's first run (84.4 → 93.3% after one re-ask). Transcripts re-distilled: tests/fixtures/deviation_corpus.json + tests/test_deviation.py + TECH_NOTES §11. Gap rows standing: the {3–8B, GBNF} arm, the bg-7 prose families, the per-family latency distribution. Detail: TEST_PLAN §8.2/§8.5, TECH_NOTES §11.

### bg-2 · event taxonomy — DONE (bg-2-event-taxonomy)

- Done one-liner: `docs/TAXONOMY.md` (120 entries across the 16 target
  types; AC ≥100 MET) + `scripts/df_taxonomy.py` (the quantile-spread
  survey over the sink DB) + the sink v2 plus pass
  (`scripts/df_import.py` — D-051's deferral fired: theft/beast detail
  is companion-only, D-063). Measured findings + the bg-3 consumer
  caveats: TAXONOMY §4/§5; recipe: TECH_NOTES §3.2.

### bg-3 · briefer spike — DONE (bg-3-briefer-spike)

- Done one-liner: the POV mini-briefer + the reverse-validation gate over the sink DB (the ≤2-regen ladder + the dry floor ported from VALIDATION_SPEC §7). Detail: TECH_NOTES §3.3 + tests/test_df_briefer.py.

### bg-6 · SoW integration audit — todo (owner-deferred)

- Read-only pass over `github.com/jofizcd/Soul-of-Waifu` (registered
  2026-08-30 at the owner's request; the owner defers integration "until
  unavoidable"): extension points for a separate simulation chat mode
  (a new mode vs. invasive edits), where llama.cpp sits, what the
  frontend must NOT own (the dumb-terminal contract, VISION §10).
  Output: a TECH_NOTES section + the `SOW_INTEGRATION_SPEC` sketch.
  Unlocked by the phase-1 gate (D-058); owner-deferred "until
  unavoidable" (D-055). Never blocks track A.

## Infra backlog (pick by need)

- `mech-1` · the mechanics introspection CLI — done (iter-84, D-118): `scripts/mechanics.py` matrix/trace/why/blast (the shadow-replay law: the PUBLIC pipeline only); 11 pins in tests/test_mechanics.py. Detail: D-118.
- `mech-2` · default output caps on the introspection CLIs — candidate
  (D-128, the Anthropic-2026 attention-budget lesson; rides the next
  `scripts/mechanics.py` touch, never its own iteration): `trace` prints
  the full per-tick view unless the operator remembers `--tail`/`--ticks`
  (measured at iter-94's HEAD: 188 lines / 12 KB on day1_full — O(ticks);
  a long-session log would flood the reading agent's context); cap the
  default (a last-N window + the "pass --<flag> for more" tail note),
  expansion by flag only; `matrix` the same if pack growth ever pushes it
  past a screen. `chronicle.py` writes files (Mode F) — out of scope.
- `engine-2` · the urgency-roll stream split — done (iter-50, D-079): per-entry streams `urgency:<npc>:<kind>`, the coupling measured and refused. Detail: D-079.
- `ci-1` GitHub Actions: pytest + ruff on push (`PYTHONHASHSEED=0`, pinned
  Python).
- `qa-1` mypy --strict on `core/` (owner-approval-gated: dev tooling is
  capped at pytest + ruff — AGENTS §8/§10; D-031 parks the candidate here.
  The type-discipline values are law from iter-1 via
  `docs/blueprint/phase0.md` §1; the tool is optional).
- `perf-1` 10k-tick timing profile — DONE iter-30: ~9.8k events/s write-side, event-linear; the numbers owner TECH_NOTES §8.
- `balance-1` 1000-headless-sim distribution harness — DONE iter-6: `scripts/balance_harness.py`; the baseline table reproducible from the seed range. KI#4 closed.
- `doc-1` VISION freeze review — DONE iter-26 (the phase-1 gate's doc-actualization sweep).
- `doc-2` REFERENCES.md license/URL re-verification, quarterly (alongside the
  TECH_NOTES review).
- `pack-1` Grim tavern pack candidate (post-gate; `PACK_SPEC.md` trigger —
  phase 6 or a 2nd setting): the romance/intimacy/coercion line as **pure
  pack data** — relation axes (`attraction`/`intimacy`/`loyalty`), status
  axes (`shame`/`anger`), a flirt→proposition action ladder,
  `consented`/`coerced` crafted knowledge records (D-008 pattern), seeded
  consequence hooks (jealousy, exposure, regret), dark templates, item
  extensions. Darkness levers per D-030; zero core change (axis-blind core;
  event vocabulary per pack, EVENT_SCHEMA §11). Distillation source:
  D-030 + the PACK_SPEC sketch row. Gate: the PACK_SPEC trigger
  (phase 6 / 2nd setting; the when-one-liner's owner is the STATUS
  FAQ, D-024 — the stale "phase-0 gate" clause removed iter-71).
- `pack-2` Arson-on-ashes guard (iter-2a audit note) — DONE iter-29
  (D-061): the `spot_available` door check (the closed precondition
  set's 15th test, layer-param lint-checked) — arson on a destroyed or
  fully-burning location is an `intent_rejected` no-op with
  `failed_test target.spot_available`, never the no-ignition success
  that pretended the world changed; the door-outcome vocabulary's
  fourth axis. The seed-41 corpus probe flipped with it (renamed
  `arson_on_a_destroyed_yard_is_door_rejected`).
- `pack-3` Sci-Fi setting candidate (owner sketches; parked, not scheduled): the sketches map mechanic-for-mechanic onto what exists — zero core change by design (INV-3's substance: a second pack requires zero ENGINE changes); blocked until the 2nd-setting gate (phase 6, same trigger as `pack-1`, ROADMAP §6).
- `ref-N` Reference deep dives — the plan table and the per-file index live
  in `docs/REFERENCES_DEEP.md` §1/§2 (single owner). All ref-1..ref-13
  items are done — status one-liners below; ref-16 (agent-memory-atlas,
  owner-supplied) was absorbed inside iter-8a, no solo iteration
  (`docs/ref/agent_memory_atlas.md`):
  - ref-1 DF worldgen — done (iter-0i) → `docs/ref/df_worldgen.md`
  - ref-2 C:DDA data/json — done (iter-0j) → `docs/ref/cdda_data_json.md`
  - ref-3 Paradox scripting — done (iter-0l) → `docs/ref/paradox_scripting.md`
  - ref-4 RimWorld + L4D + Alien — done (iter-0m) → `docs/ref/{rimworld,l4d_director,alien_isolation}.md`
  - ref-5 Wesnoth + Endless Sky + ink + tracery — done (iter-0n) → `docs/ref/{wesnoth_wml,endless_sky_dsl,ink,tracery}.md`
  - ref-6 Brogue + DCSS + KeeperRL — done (iter-0o) → `docs/ref/{brogue,dcss,keeperrl}.md`
  - ref-7 Generative Agents + ai-town + letta — done (iter-0p) → `docs/ref/{generative_agents,ai_town,letta}.md`
  - ref-8 Azgaar + Natural Earth + GeoNames — done (iter-0q) → `docs/ref/{azgaar_fmg,natural_earth,geonames}.md`
  - ref-9 libtcod + rot.js + Red Blob — done (iter-0q) → `docs/ref/{libtcod,rot_js,red_blob_games}.md`
  - ref-10 entt + Bevy + EventStore — done (iter-0r) → `docs/ref/{entt,bevy,eventstore}.md`
  - ref-11 SQLite FTS5 + DuckDB + sqlite-vec — done (iter-0r) → `docs/ref/{sqlite_fts5,duckdb,sqlite_vec}.md`
  - ref-12 Universe Audit Protocol — done (iter-0s) → `docs/ref/uap_audit.md`
  - ref-13 Live Character Guide — done (iter-0t) → `docs/ref/live_char_guide.md`
  - ref-17 DF designed experience (the player-facing half; owner-requested
    research pass, D-022 exception) — done (iter-8d) →
    `docs/ref/df_design.md`
- Candidates (owner-request only — D-022 law: no doc pass without a fresh
  owner request; both are synthesis-only today, cited via
  `CORE_DESIGN_RESEARCH.md` §2 and marked as such in the blueprint donor
  stacks):
  - `ref-14` The Sims — proprietary; patterns-from-papers only (D-015).
  - `ref-15` Prom Week — academic paper + GDC talk; no code repo.

## Done

- iter-40 · 2026-09-01 · drama-1 event grammar, predicate + weight layer — detail: worklog + the owning docs (D-row where named).

- iter-39 · 2026-09-01 · dir-4 multi-channel policies — detail: worklog + the owning docs (D-row where named).

- iter-35 · 2026-09-01 · phase-2 gate — detail: worklog + the owning docs (D-row where named).

- iter-34 · 2026-09-01 · owner-requested planning-layer audit — detail: worklog + the owning docs (D-row where named).

- iter-33 · 2026-09-01 · parse-1 batch 2 — detail: worklog + the owning docs (D-row where named).

- iter-32 · 2026-09-01 · parse-1 validation beats — detail: worklog + the owning docs (D-row where named).

- iter-31 · 2026-09-01 · phase-2 parser door — detail: worklog + the owning docs (D-row where named).

- bg-4 · 2026-08-31 · cost notes — detail: worklog + the owning docs (D-row where named).

- iter-30 · 2026-08-31 · perf-1 — the 10k-tick timing profile — detail: worklog + the owning docs (D-row where named).

- iter-29 · 2026-08-31 · pack-2 — the arson-on-ashes door check — detail: worklog + the owning docs (D-row where named).

- iter-28 · 2026-08-31 · tune-2 — the crime cascade renders on the — detail: worklog + the owning docs (D-row where named).

- iter-27 · 2026-08-31 · tune-1 — the rest action + the story-critical — detail: worklog + the owning docs (D-row where named).

- iter-25 · 2026-08-31 · validation beats — session 10, the — detail: worklog + the owning docs (D-row where named).

- iter-24 · 2026-08-31 · validation beats — session 9, the day-2 — detail: worklog + the owning docs (D-row where named).

- iter-23 · 2026-08-31 · validation beats — session 8, the — detail: worklog + the owning docs (D-row where named).

- iter-22 · 2026-08-31 · validation beats — session 7, the theft half — detail: worklog + the owning docs (D-row where named).

- iter-21 · 2026-08-31 · validation beats — session 6, the alarm — detail: worklog + the owning docs (D-row where named).

- iter-20 · 2026-08-30 · universality pass — the transition-layer and — detail: worklog + the owning docs (D-row where named).

- iter-19 · 2026-08-30 · owner-requested audit of two pasted spatial — detail: worklog + the owning docs (D-row where named).

- iter-18 · 2026-08-30 · validation beats — session 5, the arson half — detail: worklog + the owning docs (D-row where named).

- iter-17 · 2026-08-30 · validation beats — session 4, crime cascade — detail: worklog + the owning docs (D-row where named).

- iter-16 · 2026-08-30 · validation beats — session 3 — detail: worklog + the owning docs (D-row where named).

- iter-15 · 2026-08-30 · presence & entity cards — st-1 landed — detail: worklog + the owning docs (D-row where named).

- iter-14 · 2026-08-30 · validation beats — session 2 — detail: worklog + the owning docs (D-row where named).

- iter-13 · 2026-08-30 · validation beats — session 1 — detail: worklog + the owning docs (D-row where named).

- iter-12 · 2026-08-30 · the mediator session loop — detail: worklog + the owning docs (D-row where named).

- bg-5 · 2026-08-30 · owner-requested verdict on a pasted external integration spec — detail: worklog + the owning docs (D-row where named).

- iter-11c · 2026-08-30 · owner-requested re-check of iter-11b — detail: worklog + the owning docs (D-row where named).

- iter-11b · 2026-08-30 · roadmap stress-test re-verified + problems 4–6 — detail: worklog + the owning docs (D-row where named).

- iter-11a · 2026-08-29 · post-iter-11 audit — detail: worklog + the owning docs (D-row where named).

- iter-11 · 2026-08-29 · texture promotion door — detail: worklog + the owning docs (D-row where named).

- iter-10a · 2026-08-29 · post-iter-9/10 audit sync — detail: worklog + the owning docs (D-row where named).

- iter-10 · 2026-08-29 · scene-ledger LLM-free half — detail: worklog + the owning docs (D-row where named).

- bg-1 · 2026-08-29 · DF export pipeline CLOSED — detail: worklog + the owning docs (D-row where named).

- iter-8h · 2026-08-29 · owner-directed derived-index micro-pass — detail: worklog + the owning docs (D-row where named).

- iter-8g · 2026-08-29 · DF coverage audit — detail: worklog + the owning docs (D-row where named).

- iter-8f · 2026-08-29 · audit-fix after iter-8e — detail: worklog + the owning docs (D-row where named).

- iter-8e · 2026-08-28 · DF empirical F7/F8 survey on the owner's two world exports — detail: worklog + the owning docs (D-row where named).

- iter-8d · 2026-08-28 · DF designed-experience deep dive — detail: worklog + the owning docs (D-row where named).

- iter-8c · 2026-08-28 · owner-requested audit of iter-8a/8b: every claim reproduced; KI#30 — detail: worklog + the owning docs (D-row where named).

- iter-8a · 2026-08-28 · scene-ledger design pass — detail: worklog + the owning docs (D-row where named).

- iter-8 · 2026-08-28 · BRIEF_SPEC + brief assembler — detail: worklog + the owning docs (D-row where named).

- iter-7 · 2026-08-28 · phase-1 intake — detail: worklog + the owning docs (D-row where named).

- iter-6a · 2026-08-28 · owner-requested code audit of iter-5/6: every gate claim reproduced — detail: worklog + the owning docs (D-row where named).

- iter-6 · 2026-08-28 · phase-0 gate — detail: worklog + the owning docs (D-row where named).

- iter-5 · 2026-08-28 · chronicle & CLI — detail: worklog + the owning docs (D-row where named).

- iter-4a · 2026-08-28 · owner-requested code audit of iter-3/4 — detail: worklog + the owning docs (D-row where named).

- iter-4 · 2026-08-28 · director + goal ticker — detail: worklog + the owning docs (D-row where named).

- iter-3 · 2026-08-28 · knowledge, relations, expectations — detail: worklog + the owning docs (D-row where named).

- iter-2a · 2026-08-28 · owner-requested code audit of iter-1/2: KI#13–16 fixed — detail: worklog + the owning docs (D-row where named).

- iter-2 · 2026-08-28 · actions — detail: worklog + the owning docs (D-row where named).

- iter-1 · 2026-08-28 · core plumbing — detail: worklog + the owning docs (D-row where named).

- iter-0 · 2026-08-25 · docs & tooling bootstrap. — detail: worklog + the owning docs (D-row where named).

- iter-0b · 2026-08-25 · docs review + external source catalog — detail: worklog + the owning docs (D-row where named).

- iter-0c · 2026-08-25 · REFERENCES rev v2 merge — detail: worklog + the owning docs (D-row where named).

- iter-0d · 2026-08-25 · infra restore: `.gitignore`, package skeleton, smoke tests — detail: worklog + the owning docs (D-row where named).

- iter-0e · 2026-08-25 · `docs/CORE_DESIGN_RESEARCH.md` — detail: worklog + the owning docs (D-row where named).

- iter-0f · 2026-08-25 · manifesto absorption — detail: worklog + the owning docs (D-row where named).

- iter-0g · 2026-08-25 · research pass: Q1–Q3 absorbed — detail: worklog + the owning docs (D-row where named).

- iter-0h · 2026-08-26 · `docs/REFERENCES_DEEP.md` + D-024 anti-drift policy; ref batch 1 — detail: worklog + the owning docs (D-row where named).

- iter-0i · 2026-08-26 · ref-1 DF worldgen solo dive. — detail: worklog + the owning docs (D-row where named).

- iter-0j · 2026-08-26 · ref-2 C:DDA solo dive + cap policy rewrite — detail: worklog + the owning docs (D-row where named).

- iter-0k · 2026-08-26 · per-ref split into `docs/ref/` — detail: worklog + the owning docs (D-row where named).

- iter-0l · 2026-08-26 · ref-3 Paradox scripting solo dive. — detail: worklog + the owning docs (D-row where named).

- iter-0m · 2026-08-26 · ref-4 pacing trio dive — detail: worklog + the owning docs (D-row where named).

- iter-0n · 2026-08-26 · ref-5 event/narrative grammar family dive. — detail: worklog + the owning docs (D-row where named).

- iter-0o · 2026-08-26 · ref-6 roguelike emergence trio dive — detail: worklog + the owning docs (D-row where named).

- iter-0p · 2026-08-26 · ref-7 LLM-agent precedents dive — detail: worklog + the owning docs (D-row where named).

- iter-0q · 2026-08-26 · ref-8 + ref-9 six-file batch — detail: worklog + the owning docs (D-row where named).

- iter-0r · 2026-08-26 · ref-10 + ref-11 six-file batch — detail: worklog + the owning docs (D-row where named).

- iter-0s · 2026-08-27 · ref-12 UAP webapp dive — detail: worklog + the owning docs (D-row where named).

- iter-0t · 2026-08-27 · ref-13 live-char-guide dive — detail: worklog + the owning docs (D-row where named).

- iter-0u · 2026-08-27 · references distillation: `docs/BLUEPRINT.md` + `docs/blueprint/{phase0,phases}.md` — detail: worklog + the owning docs (D-row where named).

- iter-0v · 2026-08-27 · owner-requested audit patches: INV-2 rewritten per D-028 — detail: worklog + the owning docs (D-row where named).

- iter-0w · 2026-08-27 · owner-requested post-reference concept realignment: D-029 — digestion complete, skeleton — detail: worklog + the owning docs (D-row where named).

- iter-0x · 2026-08-27 · owner-requested reference-influence traceability audit: verdict "load-bearing" recorded in STATUS — detail: worklog + the owning docs (D-row where named).

- iter-0y · 2026-08-27 · owner-requested content-principles pass: D-030 — detail: worklog + the owning docs (D-row where named).

- iter-0z · 2026-08-27 · owner-requested quality round: D-031 — INVARIANT-CORE v3 + Elegant Solutions absorbed surgically — detail: worklog + the owning docs (D-row where named).

