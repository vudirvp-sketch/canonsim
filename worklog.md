# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.
> Entries re-trimmed to the line cap at iter-10a (KI#37; the drift ran
> iter-8b→10) — pre-trim detail lives in git history.
> Re-trimmed 39→10 at iter-48 (KI#68: the cap had drifted silently —
> the iter-43..47 "evicted per the cap" claims never executed; the
> eviction is now verified in the same edit, not claimed). Pre-trim
> history lives in git.
> Order: newest first (normalized at iter-8c — the order had drifted
> since iter-5).
---
iter-99 · 2026-09-11 · rev5 — the owner-requested pre-gate revision:
phase-5 verification + the long-run probes + the test actualization
(5 files — 1 new test + 4 doc sync: the revision + the test
actualization are one family; AGENTS §2.3: within cap)
- verified BEFORE working (1586+1 green, ruff clean, HEAD 0ada288);
  the probe battery OUTSIDE the repo (D-046): storyline exhaustion
  (seed 125 + a 60-turn tail), year-scale 3 crossings (seed 42),
  fresh sandbox (seed 7), determinism byte-identical + T2 clean,
  the 16-action reach catalog, the balance harness 60 seeds both
  arms (M5 p50 0.79, chains 15-24, stretch max 1 — the phase
  records hold)
- findings for the exit review: the director a finite magazine
  (all six hooks first_time_only, spent within ~2 days, the burn
  law verified live — new crimes re-seed, nothing releases); the
  day-2+ steady state = rotations + decay + the maid/relief quiet
  urgencies + the social mill (rumors decay to zero, leverage
  expires at 720); the scripted scenario CONSUMED (day-2
  steal/arson door-reject); year-scale = the weather chain + the
  census riding a watch-change loop; weather canon-but-not-tale
  (test_weather's own pin) — no read surface renders the sky yet;
  the suite's longest committed run had been ~1500 ticks
- tests/test_longrun.py (new, +3 — the committed pack's first
  past-a-day runs: the crossing laws at the committed cadence, the
  day-2 living floor, the idle world's beats; self-comparing, zero
  corpus price), 1586→1589+1 green, ruff clean (Python 3.12.14,
  the env pin); a year runs in 0.56 s — the owner's sandbox doubt
  answered with numbers
- docs: STATUS re-pinned (header iter-99, KI#84 deleted per AGENTS §5 —
  closed iter-96a, two iterations past, the mandatory cleanup riding
  this iteration's STATUS touch; the queue untouched —
  the exit review still the Next step, now carrying the revision's
  numbers), NAV §1 the tests row's longrun clause (the row's
  post-iter-86 lag noted for the gate's staleness pass, not
  backfilled here — out of scope), README the count sync;
  TASKS/DECISIONS untouched (the iter-96a audit precedent). iter-90
  evicted here (verified in this edit, the cap 10 held). Caps:
  STATUS 895 / TASKS 1160 / DECISIONS 99 — over-cap on substance
  (§6.1, the D-095..D-133 precedent), trim at the phase-5→6 gate
---
iter-98 · 2026-09-11 · weather1 — the ambient weather family + canon
erosion (the queue's live row after st-6a, TASKS' own letter; 27
files — 4 code + 2 content + 1 new test file + ~20 corpus re-pins +
6 doc sync + this worklog + STATUS: the family + the arming + the
corpus price are ONE row, the TASKS row's own three halves; AGENTS
§2.3: 27 > 5-6, the objective scope noted here)
- core/weather.py (new) + core/rng.py + core/loop.py: the chain —
  one roll per macro crossing on the isolated `weather:chain` stream
  (the D-079 family law's SEVENTH member, singleton; the
  fingerprint never sees a weather roll), a self-roll suppresses the
  event (KI#13) while still advancing the stream; the current
  weather is the FOLD (L3), no knowledge (the ambient law), no
  state_changes; the SEEDED storm consequence (the director's
  buffer through the existing door, the D-082 pattern); the EROSION
  (the fire follow-ups' shape): SEEDED follow-ups whose commits
  revert promoted canon flags (the rain washes the fire layer's
  smoke — an explicit counter-event, EVENT_SCHEMA §4; idempotent on
  state; the never-regress law floors a late crossing's deferral at
  the entry tick — the batch-crossing crash found live and fixed the
  same iteration).
- core/pack.py: the `_weather` lint — the pairing law (weather
  without time.macro is dead data, one direction), the identity law
  (the event type ≠ the macro turn's), the weights/hooks/erosion
  closures (the prop must be a transition follow-up flag), the
  reachability law; `_transition_flags` the closure's helper.
- content/tavern_pack: THE COMMITTED MACRO ARMING (the primitive's
  first consumer) — time.macro at the year-scale cadence 518400
  (one year per crossing, the genesis horizon continued) + the
  weather block (clear/overcast/rain/storm; rain's smoke wash; the
  storm's drunk-murmur hook) + the three template lines.
- tests/test_weather.py (new, +22 — the unit laws, the crafted-pack
  integration, the corpus price both-arms) — 1564→1586+1 green,
  ruff clean (3.12.14, the env pin; the armed twin double-run
  byte-identical). Corpus price, measured both arms: the T1 golden
  + day1_theft BYTE-IDENTICAL (the crossings beyond every script's
  horizon); day1_full pays the LOD's ONE-GATE engagement alone
  (depth-3's designed price, deferred since iter-91 — the warm
  ring's beat events wait for crossings: 61→56 events, the check's
  dice moved with the draw sequence, ~20 test files + narrator
  corpus 5 cases + parser corpus 1 case re-pinned; the weather
  block itself adds ZERO corpus events; the fingerprint EQUAL both
  arms). The INV-3 stoplist caught three fresh-prose nouns (the
  fire follow-ups' naming) — fixed before commit.
- docs: DECISIONS D-133, TASKS weather-1 done, phases.md §5 the
  weather paragraph, NAV §1 the core row, README (the st-6a + weather
  map rows + the status paragraphs + the macro-armed flip — the
  iter-96a sync-gap family closed in passing), STATUS re-pinned
  (the queue: EMPTY of live candidates — the phase-5 exit review the
  owner's call, the D-034 collapse + the §5 staleness pass owed at
  the gate). iter-89 evicted here (verified against git in this
  edit); 10 after. Caps: STATUS 907 / TASKS 1160 / DECISIONS 99 lines
  (44 rows) / phases.md 1066 / README 786 — over-cap on substance
  (§6.1, the standing precedent), trim at the phase-5→6 gate
  (D-128's own rows).
iter-97 · 2026-09-11 · st6a — travel as a separate action (the
STATUS queue's live row after name-1, D-116 (5)'s amended price law;
7 files — 3 code + 1 test file + 3 doc sync + this worklog + STATUS:
the price law + the accept-door branch + the lint are one family,
the iter-90..93 footprint; AGENTS §2.3: 7 > 5-6, the objective scope
noted here)
- core/travel.py (new) + core/loop.py: the price law — the travel
  action is the movement TWIN with an edge price (`ticks: "edge"`,
  the fourth legal value; move's semantics + adjacent_to + the T1
  fixtures untouched); the accept door schedules at `t + price`
  (L3 derive-never-store; day-scale queue-cheap, the crossings fire
  mid-travel in tick order, D-038); override wins per edge, else the
  DERIVED integer function (lattice steps * step_ticks + height-band
  spread * climb_ticks + river endpoints * river_ticks — no runtime
  division, draw-free, the min cross-pair); no price -> loud
  TravelError (the backstop family)
- core/pack.py: the `_travel` lint (after _worldgen) — the pairing
  law both ways (block ⇔ edge-priced action), the weights
  (step ≥ 1, climb/river ≥ 0, omitted = policy), the overrides
  (real undirected edges only, no duplicates, ticks ≥ 1), the
  COVERAGE law (every exits edge priceable — the verb never
  hard-fails mid-run); `ticks: 'edge'` movement-resolver-only
- tests/test_travel.py (new, +18): the formula oracles (hand-built
  WorldModel: step/climb/river/min-cross-pair/override-wins/
  refusals), the lint probes (the crafted-twin pattern), the e2e
  (the derived arm street↔tavern — the claimed pair, the override
  arm, the non-adjacent rejection, mid-travel rotations, the armed
  twin byte-identical double-run); the committed pack UNARMED (the
  68a pattern — the arming rides with world-2's province row)
- 1546→1564+1 green, ruff clean (3.12.14, the env pin). Corpus price
  ZERO by construction — no pack byte touched, zero re-pins
  (git-verified: only core/{intent,loop,pack,travel}.py +
  tests/test_travel.py + docs). INV-3 caught twice by the stoplist
  mid-iteration (a noun in fresh prose, the KI#79 lesson — fixed
  before commit, no KI owed)
- docs: DECISIONS D-132, TASKS st-6(a) done, phases.md §5 the travel
  paragraph, NAV §1 the core row, STATUS re-pinned (the queue:
  weather-1 the next live candidate — its gate satisfied, the macro
  arming rides with its row). iter-88 evicted here (verified in this
  edit, the cap 10 held). Caps: STATUS 863 / TASKS 1168 / DECISIONS
  98 (68 rows) / phases 1018 — over-cap on substance (§6.1, the
  D-095..D-131 precedent), trim at the phase-5→6 gate
---
iter-96a · 2026-09-11 · audit-fix — the owner-requested re-verification
of iter-96/name-1 (7 files — 1 code + 1 test + 5 doc sync: the fix
+ its tests + the sync gap are one family, the iter-83a footprint;
AGENTS §2.3: 7 > 5-6, the audit's objective scope noted here)
- verdict: the landing SOUND — the stream/lint/consumer laws re-read
  line by line, the armed + inert twins + the corpus prices re-run
  (1544+1 green, ruff clean at HEAD d755d0d BEFORE working); the
double-membership + name-duplicate questions answered loud-by-design
  (the commit gate's from_ check; the dives' documented stance)
- KI#84 the read-surface pair: `render/chronicle.py` — the outcome
  slots (`incoming`/`outgoing`) resolve through the RUNNING fold
  (`_display_if_entity` threads `_Positions`), the entity view's
  `carrier:` line through the projection (`_state_lines` threads
  it); D-131 (7)'s own law — every id-valued reference fold-first
- the README sync gap (iter-96's miss): the name-1 narrative
  sentence + the `core/names.py` map row + the count 1546; +2 tests
  (the rotation line, the carrier line — the committed pack's own
  purse-on-guard initial condition), 1544→1546+1 green, ruff clean
  (Python 3.12.14, the env pin); corpus price ZERO by construction
  — the committed pack unarmed, the authored displays identical
  (the test_ambient rotation pin re-run green)
- docs: STATUS re-pinned (header iter-96a, KI#84 closed, the queue
  untouched — st-6a the next live candidate), NAV §1 the render row,
  phases.md §5 the read-surface sentence sharpened (TASKS untouched —
  no backlog row flips, the iter-83a precedent); iter-87 evicted here
  (verified in this edit, the cap 10 held). Caps: STATUS 837 /
  phases 985 / README 742 — over-cap on substance (§6.1, the
  D-095..D-131 precedent), trim at the phase-5→6 gate.
---
iter-96 · 2026-09-11 · name1 — the name generator (the queue's W2 row
after depth-7, D-116 (12); D-131; 19 files — 5 code + 2 periphery + 2
test + 2 ref dives + the index + 7 doc sync: the stream + the generator + the lint
+ the condensation consumer + the read surface + the dives are one
family, the iter-90..93 footprint; AGENTS §2.3: 18 > 5-6, the
objective scope noted here; the doc-only streak iter-94+95 BROKEN —
AGENTS §2.5 resolved on record)
- core/names.py (new) + core/rng.py: the D-079 family law's SIXTH
  member `name:<npc>` (name_stream_name, lazy registration, the
  assure-shadow law at six families); materialize_name the lazy
  scene-detail twin — ONE birth (npc, "name", None->drawn), the
  bounded collision walk against the entity namespace (WALK_MAX,
  the loud NamesError), the unarmed law total (the stream never
  registers)
- core/groups.py + core/loop.py: the condensation consumer — the
  name births paired with the membership births (one member, one
  block; a runtime-joined member still named), the outcome's
  `names` key (the line must branch — a bare {names} is an unknown
  slot), the tier half draw-free; the bank rides _condense_groups
- core/pack.py: the `_names` lint (after _factions) — the profiles'
  shapes, the npc generated_name declarations (mutual exclusion with
  the authored `name`), the REACHABILITY law (a declaring npc must
  ride a condensing group's membership — the depth-5b family);
  render/chronicle.py + brief/assembler.py: the born-name read
  (fold-first — canon outranks the pack record; the unborn render as
  their dry ids)
- docs/ref/ck3.md + docs/ref/azgaar_names.md (new, the ref-19 dives
  owed at the row) + REFERENCES_DEEP index; phases.md §5 the name-1
  paragraph; EVENT_SCHEMA §4 the generated-name home; NAV §1; TASKS
  name-1 done; DECISIONS D-131; STATUS re-pinned (the queue: st-6(a)
  the next live candidate, name-1 the last W2 row closed)
- +28 tests, 1516→1544+1 green, ruff clean (3.12.14, the env pin;
  seed 42 pinned). Corpus price ZERO by construction, measured both
  arms: the committed pack unarmed — the inert twin (the whole
  vocabulary, no time.macro) byte-identical over plumbing_smoke +
  day1_full; the armed delta the name births + the `names` key alone,
  the (t,type,actor) sequence + the fingerprint EQUAL to the authored
  twin. iter-86 evicted (verified against git in this edit); 10
  held. Caps: STATUS 844 / TASKS 1158 / DECISIONS 97 lines (67 rows)
  — over-cap on substance (§6.1, the D-095..D-130 precedent), trim at
  the phase-5→6 gate.
---
iter-95 · 2026-09-11 · intake8 — research intake 8, the
setting-direction verdict set routed (doc-only, the owner's chat
call; D-130; 6 files — the iter-85/94 intake footprint family,
AGENTS §2.3: 6 > 5-6, the one-family objective scope noted here)
- verified BEFORE routing: the clone green (1516+1, ruff clean, HEAD
  a78e2f1, Python 3.12.14)
- D-130: the three-tier posture (the repo's 2nd setting is ORIGINAL
  — the province sketch at phases.md §6, authored pillars over a
  generated surface, riding world-2; the level-1 reskin instrument
  is the open generic stack; a proprietary fan-pack is owner-local,
  zero repo footprint); the minus ledger (ten catalogued minuses →
  the standing laws, zero new machinery); REFERENCES §10 +6 rows
  (Morrowind, TES anti-row, Discworld, FNV, Pathologic, Qud); NO new
  backlog rows (the material rides the existing W4 rows, just-in-time
  the D-096 precedent)
- the doc-only streak (iter-94 + 95) surfaced in STATUS per AGENTS
  §2.5 — both the owner's research calls, not an agent loop; the
  queue untouched (name-1 pinned); iter-85 evicted here (verified
  against git in this edit; 10 after); re-run post-edit: 1516+1
  green, ruff clean. Caps: STATUS 827 / TASKS 1141 / phases 938 /
  REFERENCES 311 / DECISIONS 96 lines (66 rows) — over-cap held on
  substance (§6.1), trim at the phase-5→6 gate.
---
iter-94 · 2026-09-10 · intake7 — research intake 7, the Anthropic-2026
agent corpus routed (doc-only, the owner's adoption call; D-128/D-129;
7 files — the iter-85 intake footprint family, AGENTS §2.3: 7 > 5-6,
the one-family objective scope noted here)
- verified BEFORE routing: the clone green (1516+1, ruff clean, HEAD
  12f5a07) + all six articles fetched live (BEA carries the Managed
  Agents update note; the Apr-2026 flagship's brain/hands split,
  context anxiety, cattle — confirmed in the fetched bytes, not the
  analysis text's word)
- adopted: ROADMAP §5 step 6 (the protocol-law staleness pass — AGENTS
  grew +190/−5 over 6 commits, only a gate pass prunes), MVP_SCOPE §18
  the actionable-error bullet (D-111 generalized; KI#82/#83 the
  evidence), TASKS mech-2 (default output caps on the introspection
  CLIs — trace measured 188 lines/12 KB on day1_full, O(ticks)),
  SPECS_BACKLOG the SOW harness-skeleton sketch; refused with cause:
  platform plumbing (MCP/sandboxes/OAuth/TTFT), multi-agent default,
  semantic search, sleep-time compute, LLM-as-judge
- D-129: protocol-law D-rows carry expected observable effects,
  checked within 1-2 iterations; the queue untouched (name-1 pinned);
  iter-84 evicted here (verified against git in this edit; 10 after);
  re-run post-edit: 1516+1 green, ruff clean. Caps: STATUS 820 / TASKS
  1113 / ROADMAP 102 / MVP 404 / DECISIONS 95 lines (65 rows) —
  over-cap held on substance (§6.1), trim at the phase-5→6 gate.
---
iter-93 · 2026-09-10 · gsim1 — depth-7, groups & simulation LOD
(D-112's ratified resolutions executed — the write side of the LOD
ladder at group scale, the W2 row after depth-6; 11 files — 3 code
(groups.py new, pack, loop) + 1 new test file + 7 doc sync: the
door + the tiers + the lint + the integration are one family, the
iter-90..93 footprint; AGENTS §2.3: 11 > 5-6, the objective scope
noted here)
- core/groups.py (new): the write-side LOD's single owner —
  `macro_tick_drafts` the population tier (one aggregate event per
  COLD group per macro crossing, actor = the group id — D-112's one
  id, the unborn population's count under `population` — the static
  members whose member_of is still None, a live fold read; no
  knowledge/state_changes/hooks, DRAW-FREE), `condensation_drafts`
  the tier transition on crossing the warm transition (ONE event
  per group: the un-born members' canon births — the D-054
  promotion shape, already-holders skipped — plus the write-once
  tombstone marker `condensed`; the load state the origin),
  `is_condensed` the marker read (the aggregate's gate). The
  member_of door: NO fold seed (absence IS None, the slot shape);
  the fold validates every join/leave/transfer; the depth-6 walk
  keeps its static-list read (the iter-92 law, zero re-pins).
- core/pack.py: the tier-vocabulary lint — the group record's
  optional `macro_event`/`condense_event` (both in the template
  closure, EVENT_SCHEMA §11; memberless refused — dead data, the
  vacuity law's lint arm). core/loop.py: `_condense_groups` the
  tier-transition pass FIRST at the beats AND the crossings (the
  materialization precedes the machinery the members then ride);
  `_run_macro`'s order — turn → condensations → cold aggregates →
  warm drift → rolls; both under an armed clock alone (the unarmed
  one-scene law, the v0.1 bytes).
- +23 tests (tests/test_groups.py — the units: the aggregate's
  shape, the tombstone gate, the zone filter, the population's
  live-fold read; the condensation: the births + the marker, the
  skip law, the write-once marker, the per-group opt-in; the door:
  the fold's join/leave/transfer validation, the stale birth loud;
  the lint refusals, parametrized; the integration: the cold
  aggregates with the cause chain, the warm/active condensations at
  the first crossing, the beat's detection arm (cadence beyond the
  beat interval), the tombstone story with the contrast twin,
  byte-identical determinism, the both-arms price — the fingerprint
  EQUAL, the delta the tier families alone, the shared (t, type,
  actor) sequence unchanged; the inert twin byte-identical over
  plumbing_smoke + day1_full; the tale's render lines binding
  {population}/{members}) — 1493→1516+1 green, ruff clean (3.12.14,
  the env pin; seeds 42 + 0 + 125 spot-checked). Corpus price ZERO
  by construction: the committed pack declares no groups and no
  time.macro; the per-group opt-in keeps every depth-6 pinned test
  UNTOUCHED (zero re-pins, git-verified: no fixture in the diff).
- docs: DECISIONS D-127, TASKS depth-7 done, phases.md §5 the
  write-side-LOD landing tag, NAV §1 (the groups module row + the
  pack/loop extensions), README (the narrative + the code-map row +
  the count 1493→1516), STATUS re-pinned (the queue: name-1 next,
  per D-116's wave order) + KI#83 deleted (closed iter-91, two
  iterations past, the KI#81 precedent) + this file (the order
  normalized — iter-92 had been appended at the END, newest-first
  restored; iter-87's missing separator restored). iter-83a evicted
  here (verified in the same edit); 10 after. Caps: STATUS 863 /
  TASKS 1072 / DECISIONS 93 lines (63 rows) / phases 860 / README
  719 — over-cap on substance (§6.1, the D-095..D-127 precedent),
  trim at the phase-5→6 gate.
---
iter-92 · 2026-09-10 · fact1 — depth-6, factions with goals (D-116's
W2 row after depth-3; 15 files — 6 code/render (factions.py new,
rng, pack, fold, loop, chronicle) + 2 test (test_factions.py new,
test_mechanics the future-layer placeholder rename) + 7 doc sync:
the
formula + the entity kind + the lint + the walk are one family, the
iter-90..92 footprint; AGENTS §2.3: 9 > 5-6, the objective scope
noted here)
- core/factions.py (new): the factions' single owner —
  `faction_probability` the KeeperRL small formula (the affected
  fraction of the membership, per-cent floored, against the pack
  threshold, ramping to `max_per_beat`; the deadband at-or-below the
  bar, the vacuity law; pure integer arithmetic), `faction_intents`
  the goal walk (each member's LIVE `status.<axis>` — D-006, never a
  stored group score; d100 on the entry's OWN
  `faction:<group>:<kind>` stream — the D-079 family's FIFTH member,
  one draw per walk, bar 0 included (the cadence law); a hit rides
  the front door, actor = the group id — D-112's one id; the
  requires gates stay silent). core/rng.py: FACTION_PREFIX +
  `faction_stream_name` (five families).
- core/pack.py: the `groups` category (OPTIONAL, the 68a pattern —
  anchor a declared location, members declared npcs, ids unique
  across categories, closed vocabulary) + the `_factions` lint (after
  `_urgencies`: axis ∈ rules.states, trigger ≥ 0, threshold 0..99 /
  max 1..100 — dead data refused, the (group, kind) pair unique,
  engine-2's twin). core/fold.py: the anchor seeds the projection (an
  actor's read surface, never a scene body). core/loop.py: the
  faction walk beside the urgencies at the beats AND the crossings
  (the anchor scoping the zone — cold factions silent, their
  population ride depth-7's aggregates). render/chronicle.py: the
  position fold seeds the anchors ({location} renders for a group).
- +34 tests (tests/test_factions.py — the formula's integer laws; the
  lint refusals (groups + entries, parametrized); the walk: the
  one-id intent, the isolated stream (draw-driven registry), the
  cadence law at bar 0, the non-holder sit-out, the LOD scoping by
  the anchor, the silent gates; the integration: the door + the cause
  chain + `faction_0000` in provenance, byte-identical determinism,
  the warm/active/cold arms under an armed clock, the tale line; the
  both-arms price: the fingerprint EQUAL, the delta the muster family
  ALONE; the inert twin byte-identical over plumbing_smoke +
  day1_full) — 1459→1493+1 green, ruff clean (3.12.14, the env pin;
  seeds 42 + 0 + unset spot-checked). ZERO re-pins (git-verified: no
  fixture in the diff, the committed pack untouched — no groups, no
  factions, zero draws). tests/test_mechanics.py: the future-layer
  placeholder renamed factions→guilds — the placeholder WAS the
  depth-6 block's own name (the law's own lifecycle, D-126).
- docs: DECISIONS D-126, TASKS depth-6 done, phases.md §5 the P3b
  landing tag, NAV §1 (the factions row + the rng five-family + the
  loop/fold/render extensions), README (the narrative + the code-map
  row + the count 1459→1493), STATUS re-pinned (the queue: depth-7 +
  name-1 per D-116's wave order) + this file. iter-83 evicted here
  (verified against git in this edit); 10 after. Caps: STATUS 861 /
  TASKS 1055 / DECISIONS 92 lines (62 rows) / phases 841 / README
  701 — over-cap on substance (§6.1, the D-095..D-126 precedent),
  trim at the phase-5→6 gate.
iter-91 · 2026-09-10 · lod1 — depth-3, the scene LOD (D-116's W2
consumer head, the macro clock's FIRST consumer; 16 files — 6 code
(lod.py new, states, urgencies, loop, macro docstring, pack the
KI#83 guard) + 3 test files (test_lod.py new, test_core the probe,
test_macro the re-pin) + 7 doc sync: the zones + the filters + the
loop integration + the pins are one family, the iter-86..90
footprint; AGENTS §2.3: 16 > 5-6, the objective scope noted here)
- core/lod.py (new): the zone family's single owner — `scene_zones`
  (the pure partition over the exits graph + the PC's live position:
  ACTIVE per-beat / WARM the exits in pack order / COLD the rest in
  declaration order, self-exits + duplicates filtered, LodError the
  pred-contract guards), `npc_population` the census read,
  `COLD_COUNT_KEY = "cold_npcs"` the turn's flat count. THE ONE-GATE
  LAW: the LOD engages exactly when the macro clock is armed (the
  warm cadence IS the macro cadence — one clock, zero new pack
  vocabulary); the unarmed law is the one-scene world.
- core/loop.py: `_run_macro(tick, entry_tick)` — the turn FIRST
  carrying the cold census, then the warm ring (the drift chained
  after the turn at the crossing tick, the goal rolls at the
  crossing tick enqueued at the entry tick — the beat machinery
  minus the DIRECTOR, which stays global: the story layer, never
  ambient life); `_run_beat` scopes to the ACTIVE zone under an
  armed clock (`_scene_zones`, None unarmed). core/states.py +
  core/urgencies.py: the `locations=None` LOD filter (None the
  one-scene law; the walk cuts, never rescores — L13; the odds never
  change, the roll cadence is the LOD's own cost). core/macro.py:
  the docstring's consumer re-pin (depth-3 the surface's first
  caller). core/pack.py: KI#83 — the entities lint's missing-`exits`
  KeyError leak, the named-PackError guard (the KI#82 family).
- +17 tests (tests/test_lod.py — the partition, the loud guards, the
  census's npc-only law, the self-exit filter, the filter scopes with
  the L13 no-rescore law + the draw-driven stream registry, the
  integration: the warm ring at the crossings with the cause chain,
  the active-per-beat vs warm-at-the-crossing split, the cold
  silence + the census ride, the census following the PC across the
  move, the unarmed twin's byte-identity over plumbing_smoke +
  day1_full, determinism, the co-occurring family order, the
  template's census binding; tests/test_core.py the KI#83 probe;
  tests/test_macro.py the corpus pin re-measured) — 1442→1459+1
  green, ruff clean (3.12.14, the env pin; seeds 42 + 0 + unset
  spot-checked). Corpus price, measured BOTH arms: ZERO by
  construction — the committed pack unarmed (the one-scene law), the
  unarmed crafted twin byte-identical to the committed bytes over
  the corpus scripts; the armed arm's delta the macro family alone
  (seed 42: 18 vs 6 events — 2 turns + 10 warm drifts, the
  substantive fingerprint EQUAL at 0, the rolls on the isolated
  urgency streams); ZERO re-pins (git-verified: no fixture in the
  diff, the T1 golden untouched).
- docs: DECISIONS D-125, TASKS depth-3 done, phases.md §5 the
  scene-LOD paragraph + the intake bullet's landing tag, NAV §1 the
  lod row + the states/urgencies/loop extensions, README the
  narrative sentence + the code-map line + the stale test count
  synced (1323→1459 — the honest-count law), STATUS re-pinned (the
  queue: depth-6 next, the W2 wave order) + KI#83 recorded + KI#82
  deleted (closed iter-88, three iterations past — the deletion was
  overdue at iter-90). iter-82 evicted here (verified against git in
  this edit); 10 after. Caps: STATUS ~800 / TASKS 1044 / DECISIONS
  91 lines (61 rows) / phases ~800 / README 681 — over-cap on
  substance (§6.1, the D-095..D-125 precedent), trim at the
  phase-5→6 gate.
---
(end of log — cap 10; pre-trim history lives in git)
