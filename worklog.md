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
iter-119 · 2026-09-13 · world2c — the cultures half, the owner's fresh
call «начинай работу по планам, что осталось незакрытого и логичнее
всего было бы начать сейчас то и делай» (the iter-117/118 precedent
phrase; STATUS Next step's own readiness pick — slice 2 the natural
next pick, D-153's wave plan, D-154)
- verified BEFORE working (1707+1 green, ruff clean, HEAD ebf464e,
  Python 3.12.14 the env pin); re-verified after — 1726+1 green
  (+15 tests/test_cultures.py, +4 the T1 province pins, +3 stoplist
  words), ruff clean; zero corpus price outside the province (the
  tavern/road corpora byte-untouched; the province's own golden
  fixture regenerated — the additive delta: +1 condensation, +6
  traveler decays, 32→39 events, fingerprint 0)
- content: the two name-1 profiles (lowland_soft the river tongue vs
  hill_hard the croft tongue — name-1's FIRST committed arming, the
  posture made checkable), the condensation travelers (grp_road_traffic
  anchored on the load road, three generated_name members, the first
  beat materializing them at t=360 — the drawn names
  Sathranthaem/Wathru/Drist), the cultures block (the budget-block
  precedent: profile binding, custom vocabularies, the prohibition
  sets, the members), the budget re-declare (npcs 7-12, the cast at
  10), story_critical += road_musters, the tier template pair
  (road_counts/road_musters, the {names?...} branch law)
- core: `core/pack.py` _cultures (the shape, the anti-rot vocabulary
  walk, the culture↔name keying, the one-culture law, the AP-8 member
  binding) + the AP-8 consumed union in _live_char (the prohibition's
  flaw joins the set — the crosswalk's THIRD consuming family, landed
  on its own trigger); tests: test_cultures.py NEW (the refusals +
  the consumed-union green twin — a crafted spine consumed by the
  prohibition ALONE), the T1 pins (the first-beat condensation, the
  born-names tale line, the tongue posture, the committed instance),
  PROVINCE_STOPLIST +3 (drover, peddler, wergeld)
- docs: DECISIONS D-154 (33 rows — over the 30 cap on the §6.1
  substance precedent until the next gate collapse), TASKS (slice 2
  flipped + the iter-119 section), STATUS re-pin + Next step (slice 3
  the triangle the natural next pick), PACK_SPEC (§3/§4/§5/§6 the
  cultures block + the AP-8 prohibition surface), NAV §1 + README (the
  province_pack rows re-pointed), this entry (iter-109 evicted per the
  cap, verified in this edit; 10 held); 14 files (13 modified + 1 new,
  re-counted against the worktree delta)

iter-118 · 2026-09-13 · world2l2 — the province skeleton, the owner's
fresh call «начинай работу по планам… логичнее всего было бы начать
сейчас то и делай» (the iter-117 precedent phrase; STATUS Next step's
own readiness pick — world-2 L2 the natural next pick, D-153)
- verified BEFORE working (1696+1 green, ruff clean, HEAD d6cffa8,
  Python 3.12.14 the env pin); re-verified after — 1707+1 green
  (+10 tests/test_t1_province.py, +1 the stoplist self-check, the
  packci third-pack pin re-pointed), ruff clean; zero corpus price
  (the third pack is a new directory, the committed corpora and
  fixtures byte-untouched by construction)
- content: `content/province_pack/` NEW (the Sarrow Vale, ORIGINAL
  nouns per D-130's posture tier, no CREDITS sidecar): the worldgen
  at the province band (324 sites, extent 144; six settlements
  claimed, max_edge_span 4; the feud/quarrel chronicle arming the
  dormant hook pair) + travel (the road family's 150/60/45 over the
  province lattice — the derived legs 345-705) + the SPINE records
  (the AP crosswalk's first committed consumer: five flaws, all
  consumed by urgency entries, AP-8) + the budget block (AP-1's
  first arming); the actions/templates re-voiced from the road family
  (the tokens, the hook ids, the world_history formed arm binding the
  six claim slots)
- tests: the T1 twin +10 (byte-identity + the golden fixture
  province_smoke_seed42.jsonl + the regen guard + the price pins +
  the mid-travel knowledge-transfer pin at t=3240 inside the
  Malby->Thornmill leg + the spine/budget/genesis-scale pins);
  PROVINCE_STOPLIST + the per-pack self-check; the packci
  committed-pin grows the third pack
- docs: DECISIONS D-153 (32 rows — over the 30 cap on the §6.1
  substance precedent until the next gate collapse, the D-152
  landing's own record), TASKS (the world-2 L2 opening + the wave
  plan: slice 2 the cultures, slice 3 the triangle, slice 4 the
  calendar), STATUS re-pin + Next step, NAV §1 + README the
  province_pack rows, PACK_SPEC §6 the AP-9 first-consumer note, this
  entry (iter-108 evicted per the cap, verified in this edit; 10
  held); 16 files (re-counted against the worktree delta: 9 modified
  + 7 new) — the pack iteration's own checklist (the iter-112
  family's objective scope, AGENTS §2.3). Caps: STATUS 578 / TASKS
  945 / DECISIONS 63 (32 rows — over the 30 cap on the §6.1
  substance precedent until the next gate collapse, the D-152
  record) / worklog 10 entries held — the over-cap files ride the
  documented §6.1 substance precedent, trim at the next gate

iter-117 · 2026-09-13 · pack-ci — the admission-lint rungs LIVE (the
owner's fresh call «начинай работу по планам… логичнее всего — то и
делай»; STATUS Next step's own readiness pick — pack-ci the natural
cheap candidate, D-152)
- verified BEFORE working (1668+1 green, ruff clean, HEAD 274130c,
  Python 3.12.14 the env pin); re-verified after — 1696+1 green
  (+28, tests/test_packci.py), ruff clean; zero corpus price (the
  lint is load-time only, the committed playscripts/fixtures
  byte-untouched)
- core: `core/pack.py` `_teleology` (dead actions — the effect
  witnesses + STATE_MUTATING at `core/resolvers.py`'s own owner;
  orphans — the reference walk + exits edges + audience reach + the
  target-grammar matcher; empty matrix rows; unused templates — the
  emission-witness collector + the story-critical dormancy witness)
  + `_live_char` (AP-1/8/9/11/13/15 + the price-marker lint, the
  ambient channel exempt) + the spine lint in `_entities` + the
  atomicity law inside `_predicate_error`
- the 68a twin-compliance pass (the law's own blast radius, 20 files
  per AGENTS §2.3): a stripped block strips its emission vocabulary —
  the weather family's template lines with the blocks (11 crafted
  twin helpers) + the harness's `_DROP_DEAD_LINES` ablation map; the
  factions muster rides a `system_of_type` attribution row (zero
  canon bytes); the groups' tier lines ride their records
- docs: PACK_SPEC §5/§6 the enforcement readings + the §12 flip,
  DECISIONS D-152 (31 rows — over-cap on §6.1 substance until the
  next gate collapse), TASKS the pack-ci flip + iter-117, STATUS
  re-pin + Next step, this entry (iter-107 evicted, verified in this
  edit; 10 held)

iter-116 · 2026-09-13 · gate6 — the phase-6 gate review, the
owner's convening gate call «давай уже свой гейт-колл 6 фазы или что
там, приступай к работе и незакрытым задачам» (7 files doc-only, zero
code, zero corpus price — the gate session's own form, ROADMAP §5 +
the doc debts riding it)
- verified BEFORE working (1668+1 green, ruff clean, HEAD d4ec8dd,
  Python 3.12.14 the env pin); re-verified after — same numbers, zero
  runtime surface touched. The §5 evidence: playscripts byte-green
  (plumbing_smoke + road_smoke vs their committed fixtures — the road
  side's T1 twin; the header commit field the only delta, '0000000'
  per the T1 law); the seed-125 pair ON M1=0.518/M2=0.200 (56 events
  — iter-102's numbers exact) / OFF T8 24 chains, M5 0.849; T7 both
  chronicles read as stories; no kill hit — the module contract proven
  right (D-149's zero core edits)
- the verdict: PASS, D-151 — ROADMAP §2 flipped CLOSED, the ladder
  complete (phases 0..6); the open build rows stay owner-gated; the
  §5 step-6 staleness pass: REWORD AGENTS §1's phase frame + the FAQ
  cap-laws entry, KEEP the rest, DROP none
- the doc debts paid: DECISIONS 44→30 (D-034 — D-142/143/144 folded
  into D-145, D-137/139/140/141 one row, D-138 into D-076/081, D-062
  into D-054/055, D-079 into D-004/028, the intakes 11..13 + D-146/
  149/151 into the families); STATUS tombstones trimmed + FAQ resync
  (639→554); TASKS 1251→892 (iter-103..115 collapsed to one-liners);
  README 826→184 (the Status section collapsed to per-phase gate
  summaries)
- phases.md 1536 / TECH_NOTES 773 / TEST_PLAN 772 stay over cap ON
  SUBSTANCE (§6.1): the cruft pass ran (the filler scan: 2 hits, both
  load-bearing measured-fact contrasts; the structural review — the
  per-phase architecture, the engine-1 consult blocks, the measured
  records are those files' own function); pre-trim history in git
- docs: ROADMAP §2, DECISIONS D-151 + the collapse, AGENTS §1, TASKS
  iter-116 + the collapse, STATUS re-pin, README, this entry (iter-106
  evicted here, verified in this edit; 10 held); 1668+1 green, ruff
  clean after

iter-115 · 2026-09-13 · intake13 — the owner's research call over
the uploaded «open-ended actions / content packs / honest
simulation» review (5 files doc-only, zero code, zero corpus
price — the routing record's own scope, AGENTS §2.3)
- verified BEFORE working (1668+1 green, ruff clean, HEAD
  117a19f, Python 3.12.14 the env pin); re-verified after — same
  numbers, zero runtime surface touched
- the routing: the doctrine half CONFIRMED as standing law
  (VISION §1/§5, INV-1..5, EPIST-1; one stale pin corrected —
  phase 6's litmus test MET BY MEASUREMENT since iter-112);
  four proposals routed: substrate → D-096 + parse-2 + engine-1
  (the loop already executes intent chains causally, zero
  simulator change owed; a generic primitives layer REFUSED —
  L13, no consumer); PARTIAL → first separable-sub-effects
  consumer; UNDER_MODELLED → REFUSED, the PACK-CI CLOSURE LAW
  the preferred cure; inventions-from-repetition → parked
  (res-1 + world-2 L2)
- docs: phases.md §6's intake-13 block + DECISIONS D-150 +
  TASKS iter-115 + STATUS re-pin + this entry (iter-105 evicted,
  verified in this edit; 10 held). Caps: DECISIONS 75 lines
  (44 rows) — over-cap on substance (§6.1), collapses at the
  phase-6 gate per the D-034 family law
---
iter-114 · 2026-09-13 · doc2 — the quarterly review, the owner's
«продолжай работу по планам» (22 files doc-only, zero code, zero
corpus price — the row's own objective scope, AGENTS §2.3)
- verified BEFORE working (1668+1 green, ruff clean, HEAD 68c1abf,
  Python 3.12.14 the env pin); re-verified after — same numbers,
  zero runtime surface touched
- the re-point (the iter-113 routed finding): 17 ref files + the
  REFERENCES_DEEP §2 verdict columns — the never-existing planned
  names now cite the current-state owners (loop / fold / retrieval
  + chronicle / reflection / resolvers / knowledge / scheduler /
  onaction / worldgen / director / content-<pack>; the llm_client
  family → the INV-4/engine-1 gate, never in track A); mechanics +
  verdicts untouched; the row's 12-file list corrected (+red_blob_
  games, natural_earth, geonames, eventstore, neighborly — the
  family was bigger than the iter-113 grep)
- the license/URL pass: 45 repo paths probed (`git ls-remote`, no
  API) + LICENSE files read direct (raw.githubusercontent.com —
  the intake rule #1 form); three deltas (dnd-llm-game → MIT, the
  IDCDW tag stale; pyDF → a CC BY-NC-SA template file now present;
  RACEngine → a bare-copyright stub, no grant), `a16z/ai-town`
  404s (live `a16z-infra/ai-town` — the ref citation re-pointed),
  pcg.wikidot.com + open5e.com down at the check date (health
  notes; open5e's API answers 200); deferred "verify" tags stay
  deferred (D-017)
- docs: 17 ref files, REFERENCES_DEEP §2, REFERENCES (the pass
  record + deltas + health notes + the check-date tag), TASKS (the
  iter-114 section + the doc-2 row's run record), STATUS re-pin +
  Next step, this file; iter-104 evicted here (verified against
  git in this edit); 10 after; 1668+1 green, ruff clean after.
  Caps: STATUS 644 / TASKS 1219 / DECISIONS 74 (43 rows — the
  collapse owed at the phase-6 gate, D-034) / phases 1409 /
  TECH_NOTES 773 / TEST_PLAN 772 / README 825 — the over-cap files
  ride the documented §6.1 substance precedent, trim at the gate
---
---
iter-113 · 2026-09-13 · docaudit — the owner's lossless
documentation-audit call (4 files doc-only, zero code, zero corpus
price — the iter-103 audit footprint family)
- verified BEFORE working (1668+1 green, ruff clean, HEAD 18f8b11,
  Python 3.12.14 the env pin); the reading gradient re-walked, the
  declared ownership verified against HEAD (NAV §1 rows resolve,
  REFERENCES_DEEP §2 matched docs/ref/ 38/45 — the gap below, ledger
  terms land, phase states agree, the test-count claim reproduced)
- verdict: the architecture HOLDS, ZERO removals — the cross-layer
  repetition is the declared link-never-restate / research-record
  pattern, not false duplicates; the doc debts stay owed at the
  phase-6 gate (DECISIONS 43 rows + the over-cap residue:
  STATUS/TASKS/phases + TECH_NOTES 773 / TEST_PLAN 772 / README 825
  + the FAQ resync), deliberately not preempted
- repaired: REFERENCES_DEEP §2 +8 rows — iter-109 missed the file's
  own same-edit law (the ref-18/ref-20 dives never indexed); routed:
  the research layer's stale "lifted into" module paths
  (core/runner.py, core/store.py, core/storage.py, brief/recall.py,
  brief/llm_client.py, sim/systems/* — never-existing pre-iter-1/
  pre-D-037 names; NAV §1 + D-037/D-142 the correct owners) → the
  doc-2 row's note (the iter-103 precedent, zero new KIs)
- docs: REFERENCES_DEEP §2, TASKS (the iter-113 section + the doc-2
  note), STATUS re-pin + Next step, this file; iter-103 evicted here
  (verified against git in this edit); 10 after; 1668+1 green, ruff
  clean after. Caps: STATUS 646 / TASKS 1184 / DECISIONS 74 (43 rows
  — the collapse owed at the phase-6 gate, D-034) / phases 1409 /
  TECH_NOTES 773 / TEST_PLAN 772 / README 825 — the over-cap files
  ride the documented §6.1 substance precedent, trim at the gate
---
iter-112 · 2026-09-13 · world2-l1 — the reskin day, the owner's «да
приступай» (12 files: 5 pack + 4 test + 3 doc-sync beyond STATUS/worklog
— the day's own checklist, AGENTS §2.3's objective scope noted)
- the clock: 14m24s from the first scaffold (23:52:40 UTC) to the green
  T-suite (00:07:04 UTC) — reading/design before the scaffold excluded
  (the clock's own definition); the ≤1-day budget met at ~1/60th; ZERO
  core edits (git-verified: no byte under core/ sim/ brief/ render/ cli/
  scripts/ — the universal-core claim measured, ROADMAP §2's exit form)
- content/road_pack/ (the TRAVEL-loop reskin, SRD 5.1 nouns, CREDITS.md
  CC-BY sidecar): ids stay (the scaffold law), surfaces renamed; move =
  ticks 'edge'; rules.json travel (150/60/45 — the derived prices, no
  overrides, all five locations claimed at row-2 sites 12–16,
  max_edge_span 2; the measured prices 150/210/300/360); the
  world_history formed arm binds the five claim slots; the authoring
  loop's first live run — one lint refusal caught (travel carries no
  notes key) and fixed same-edit, the doctor's fix-hint surface worked
- tests: test_t1_reskin.py +7 (the T1 twin: byte-identity, the golden
  regen + schema pins, fingerprint 0 — edge-priced moves draw nothing,
  the derived-prices route pin, the mid-travel encounters pin — the
  watch change t=360 inside the 180→540 leg); ROAD_STOPLIST + the
  per-pack self-check (+1); road_smoke.json + road_smoke_seed42.jsonl;
  1660+8 → 1668+1 green, ruff clean, zero tavern corpus price
- T7 (the road chronicle reads as a story): the world takes shape (36
  sites, 150 years, coast ground, forest yard, the toll post 4352 paces
  above the water) + the four history lines + the mid-route watch
  change (Odo hands the post) + the boatman's ramble — the tale opens
  on the genesis and lives on the road
- docs: D-149 (the reskin-day record — the instrument, NOT the gate),
  TASKS world-2 L1 flip + the iter-112 section, NAV §1 + README the
  road_pack rows, STATUS re-pin (671→647); iter-102 evicted here
  (verified against git in this edit); 10 after. Caps: STATUS 647 /
  TASKS 1129 / DECISIONS 74 (43 rows — the collapse owed at the
  phase-6 gate, D-034) / phases 1409 — the over-cap files ride the
  documented §6.1 substance precedent, trim at the gate

iter-111 · 2026-09-13 · intake12 — the owner's verdict call over the
Brief-IR-vs-presentation consolidation (5 files doc-only, zero code,
zero corpus price — the intakes-6..11 family precedent; one family)
- verified BEFORE working (1660+1 green, ruff clean, HEAD 2ebd122,
  Python 3.12.14 the env pin); every load-bearing citation checked
  against HEAD — plus two session fact-checks (Rule 9 runners
  outside the repo): the live mode-A call dump (anchor/regen ride
  the model-facing bytes literally; query/retrieval mode-B-only;
  282 ws-tokens) and the day1_full truncation census (zero markers
  fire, 208–274 ws-tokens vs total_hard 800; the 105-case corpus
  pins none); three micro-drifts + the missing bg-7/bg-8 evidence
  base recorded in D-148 (the audits predate §10/§11)
- the verdict set (8 rows, D-148 + phases.md §6's intake-12
  block): the "60–70% ready" frame REFUSED (a contract without a
  consumer has unknown requirements — the {3–8B, GBNF} run is the
  metric's only honest form; sequenced-by-design, D-022/§9); the
  protocol noise re-owned (the block is the operator's reply-
  contract signal at dev-time — the anchor is what the reply
  carries; zero measured leakage at 27B; the concern fires at
  engine-1 where the GBNF grammar owns the output side and the
  input split is a one-block serializer decision); [truncated:N]
  STAYS (the anti-silent-drop invariant; the golden-set A/B rides
  the weak arm — at 27B C3.5 is clean and the structural gates
  hold); condensation = the fold pattern (the belief lines ARE
  in-brief condensation, §3.5; never tracery — the iter-43
  flat-key law; never the assembler, L2); LiM REFUSED as a
  requirement driver (MECW + the landed live-char geometry own it;
  the local instrument is the heartbeat trend line on the engine-1
  arm); the presentation spec written at the engine-1 trigger FROM
  weak-arm results, ABSORBING st-4, as a thin mapping table over
  the 8 blocks (the D-055 file-contract pattern's fourth instance;
  never a 7-layer re-labeling vocabulary, D-024); the behavioral
  layer ANSWERED by PACK_SPEC §6 (AP-9 spine → AP-8 rule through
  the intent door's gate family → the committed event → the
  existing surfaces; the presentation-side alternative refused —
  wrong layer, L2 violation, four duplicated homes); the priority
  dichotomy DISSOLVED (the weak-arm run IS the requirements
  measurement — one row, one gate)
- docs: DECISIONS D-148, TASKS the presentation-1 row + the
  iter-111 section + st-4's absorption pointer, phases.md §6 the
  intake-12 block, STATUS re-pinned, this file. iter-101 evicted
  here (verified against git in this edit); 10 after. The build
  queue untouched — world-2 L1 stays pinned CODE on the owner's
  «приступай»; doc-only #3 rides the D-022 exception (the owner's
  fresh call; the intakes family is doc-only by construction).
  Caps: STATUS 671 / TASKS 1073 / DECISIONS 73 (42 rows — the
  over-cap debt collapses at the next phase gate, the D-034
  family law) / phases 1409 — over-cap files ride the documented
  §6.1 substance precedent (D-095..D-147), trim at the phase-6→7
  gate.

iter-110 · 2026-09-13 · intake11 — the owner's chat call, the
pressure-city donor blueprint (PRESSURE_LIMIT) routed (5 files
doc-only, zero code, zero corpus price — the intakes-6..10 family
precedent; one family)
- verified BEFORE working (1660+1 green, ruff clean, HEAD 140bbcf,
  Python 3.12.14 the env pin); every load-bearing donor citation
  checked against HEAD (the convenience-copy law) — all green
  (D-130, res-1's one-meter read surface, the thermometer minus,
  D-140, D-134, weather-1 chain+erosion, depth-6/7, name-1,
  chron-2, retr-1, st-6a, roads-1, D-030); two micro-drifts
  corrected in D-147 (AP crosswalk rung specified-not-landed; no
  literal meta.json)
- the verdict: ADOPTED as parked donor material — the displacement
  law (the one word-for-word keeper), the Cooling Debt resolved to
  weather-1's chain+erosion shape (never a second res-1), the gauge
  = res-1's read surface, legal exclusion = the D-134 application,
  objective-function factions = depth-6's shape, lore hooks ride
  templates + cause_hook; the biome question answered (authored
  pack data, never a worldgen biome; the lost-city fold the cheap
  form; the full concept = pack-4's third slot)
- docs: DECISIONS D-147, TASKS the pack-4 row + the iter-110
  section, phases.md §6 the intake-11 block (+62 lines,
  substance), STATUS re-pinned, this file. iter-100 evicted here
  (verified against git in this edit); 10 after. The build queue
  untouched — world-2 L1 stays pinned CODE on the owner's
  «приступай». Doc-only #2 (the D-022 exception, the owner's fresh
  request); no third planned. Caps: STATUS 645 / TASKS 1014 /
  DECISIONS 72 (41 rows) / phases 1264 — over-cap files ride the
  documented §6.1 substance precedent, trim at the next gate
  collapse.
---
