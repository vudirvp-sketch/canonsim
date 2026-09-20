# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Re-trimmed at iter-151 (the entries had drifted to ~40 lines each; the
> compaction entry carries the §6.1 over-cap rationale, as AGENTS §6
> demands); pre-trim history lives in git.
---
iter-170 · 2026-09-21 · engine-1 — the runtime inference engine
DECIDED (the owner's real-backend convening call: llama.cpp + the RTX
3080 Ti station + the three-model set + the real `llama-server` test
evidence; the disposition + the session research both riding the call)
- D-192 (DECISIONS): llama-server behind an explicit adapter + GBNF,
  the file-contract frame (D-055) the insertion point; CONTRACTS §4
  the build contract (the D-177 pattern): D1–D8 the pinned decisions
  (semantic policies never raw flags; the reproducibility tiers;
  reasoning engine-side; structured output ≠ validation; the client's
  home + the INV-4 lift pinned to the build's own iteration; the
  non-equivalences; the non-goals), I1–I6 the invariants, §4.3 the
  falsifier (zero gate edits + the honesty floor) + the experiment
  design (the {3–8B, GBNF} gap rows + the FOUR new arms: one-vs-two-
  model, seeded-local determinism, the GBNF latency penalty, mode-A
  at the weak arm)
- TECH_NOTES §2 refreshed to the measured station + §13 the evidence
  record — every cited fact verified against the owner's raw logs
  (113–126 tok/s E4B, 94.5 9B, 27B hybrid 12.95/4.51, the -ngl
  fit-refusal, the thinking-consumed budget, the -np ctx halving,
  streaming/truncation, cancellation, /health /props /slots,
  warnings, deployment defaults); TASKS: the engine-1 row DECIDED +
  presentation-1's evidence base §10/§11/§13 + the ledger line;
  STATUS re-pin; 6 paths, doc-only — over the §2.3 soft limit (the
  decision + contract + evidence rows, the intake-31/32 precedent)
- caps: DECISIONS 31 rows (one over ≤30, collapses at the owner's
  next gate call, D-034/D-185); TECH_NOTES 854 lines (over the 600
  docs cap — the pre-existing 773 + pure measured substance, §6.1);
  TASKS 1205 (the pre-existing over-cap 1180 + the law-required
  ledger line + the row rewrite, §6.1's standing state); verified
  BEFORE at BASE_COMMIT 7618714 (1900+1 green, ruff clean —
  the iter-169 pin re-confirmed) and re-verified after: 1900+1 green,
  ruff clean, zero test change; iter-160 evicted per the cap
---
iter-169 · 2026-09-21 · qa2 — the KI#88/#89 lint-side closures (the
owner's «проработай открытые в прошлой итерации ki и все связанное,
нужно доделать все с технической частью» call): both holes qa-1 opened
closed at LOAD, zero runtime change on well-formed packs
- KI#89: shared `lint_direct_keys` (packlint/shared.py, the
  lint_echo_cond family) — presence + type + non-emptiness for the five
  record-reading tests' directly-indexed keys, wired into ALL FOUR
  `requires` lint sites (action canon, texture block, urgencies,
  factions; the iter-45 `who` precedent generalized to its family)
- KI#88 arm 1: ACTOR_KEYS split in core/onaction.py (world |
  source_actor; the reaction actor is schema-required) + the dedicated
  story.py row refusing `actor: source_target` with the rationale;
  arm 2: the target-sourced check row in actions.py reading the door's
  OWN `needs_target` predicate (extracted from validate_shape into
  core/intent.py — one source, two readers); the runtime asserts stay
  the backstops
- tests/test_qa2.py +15 (the §9 claim packet: the five presence rows
  parametrized, the type/dead arms, the three site arms, both KI#88
  arms + the negative load arm); docs: DIRECTOR_SPEC §3c (the actor
  row split), INTENT_SCHEMA §3/§5 (the presence row + the check row);
  12 paths, over the §2.3 soft limit (the two-KI closure + its packet)
- verified BEFORE at BASE_COMMIT e15a091 (1885+1 green, ruff clean,
  the iter-168 pin re-confirmed) and re-verified after: 1900+1 green,
  ruff clean, mypy --strict core/ 0, goldens byte-untouched, the five
  committed packs loading; the `flag` test's twin hole recorded, not
  routed (the owner's call class); iter-159 evicted per the cap
---
iter-168 · 2026-09-21 · qa1 — the owner-called type-discipline audit
(the owner's «там еще была задача qy 1 что ли, связанная с проверкой
кода» chat call naming the standing row over STATUS's Next step):
mypy --strict on `core/` taken 207 → 0 across 36 files at ZERO runtime
behavior change (the suite + the golden fixtures byte-identical both
ends)
- root fixes: `_require(condition: object)`; the `Importance`/`Fidelity`
  Literal funnels (pack_importance/_importance, decay/acquisition);
  the RetrievalIndex slot annotations; the Mapping read-only widening
  (fold's dict `Projection` the write owner, resolvers' own alias
  retired); `_is_int`/`_is_number` → TypeGuard; `Pack.entity/action`
  Iterable bridges; assert-after-require narrowings across packlint
  (the lint's loud refusals stay the contract); the shadowing kills
  (metrics/echo/admission/worldgen); log.py's first-branch annotations;
  29 core files (over the §2.3 soft limit — a repo-wide strict pass)
- two real holes made loud: KI#88 (the source_target actor null + the
  target-sourced defender — asserts landed, the lint-side closure the
  residue); KI#89 (the door's directly-indexed cond keys `flag`/
  `field`/`values` not load-linted — the iter-45 `who` family, fix
  routed); the tool stays optional (D-031 unchanged — no dev-dep, no
  CI row, enforcement the owner's call class)
- verified BEFORE at BASE_COMMIT c82c7ca (1885+1 green, ruff clean —
  the iter-167 pin re-confirmed) and re-verified after: 1885+1 green,
  ruff clean, mypy --strict core/ 0 errors, goldens byte-untouched;
  iter-158 evicted per the cap
---
iter-167 · 2026-09-21 · stepread — the step bench's first embodiment (the
owner's «продолжай работы, что логичнее всего сейчас начать» continuation
call over STATUS's embodiment routing, the natural doc-streak breaker after
three doc-only iterations): the step's close read — the unit's setting verb
(the §6.2 gap text's own "a future embodiment's own class, the read_pole
precedent") — landed as pure pack data, zero core
- pack: actions.json (the read_stair hinge — the read family's third
  instance, its first location-kind target: the stair IS the carrier; the
  perception gate 30, the field_in pin + the co-location gate),
  templates.json (the stair_read + stair_read_failed lines — 63 templates,
  inside the 65 budget); the literal token the_step_law minted to the
  reader: the ORDER the road never learns from the books (§7.1's stranger
  row — the road's misread correctable in play, the brief's recalled facts
  the read surface); the token deliberately PLAIN knowledge — no secrets
  entry, no cluster, the registry stays two keys (the pole's debt-lever
  class not duplicated)
- tests: test_stepread.py (+7, the §9 claim packet — the census + the
  plain-knowledge boundary; the day chain exact at three probed seeds; the
  brief's recalled-facts line; the night chain partial — the unlit weir;
  the off-site/far rejection arms; the determinism twin); docs: the
  worldbuild trio (ANCHOR_REGION §6.2, WORKPLAN §2/§6, WORLD_TESTS §9) +
  TASKS + STATUS; 9 paths (the iter-161/162 pack-landing precedent); zero
  corpus price (no committed script reads the stair — the golden T1
  byte-untouched)
- honest residues: the read mints the LAW, never the PRESENT (the water
  level's gap stays owner-routed, the separate-track law); no NPC driver
  reads the stair (the player-facing verb, the pole's dormant-family
  class); the remaining embodiment options (the notch record's arming, the
  hatch — and the winter kin's three) stay the owner's call class
- ANCHOR_REGION stays over the 600-line docs cap (771 after the +9): the
  pre-existing substance-law state, the iter-165 rationale standing (the
  unit's rungs/tables are substance, no cruft found in the pass)
- verified BEFORE working at BASE_COMMIT a317db3 (1878+1 green, ruff clean
  — the pin re-confirmed) and re-verified after: 1885+1 green, ruff clean
  (the +7 the claim packet); iter-157 evicted per the cap
iter-166 · 2026-09-21 · intake33 — the game-design practitioner
talks corpus routed (the owner's research call over the uploaded
five-source knowledge base: Sawyer/Meier/Battle Mode/Johnson/Wolverson):
PARTIALLY CONFIRMED — a perception + economy-craft donor, never a
systems donor
- adopted: the OUTCOME-PERCEPTION LAWS CARD (the layered legibility
  ladder — the combined form of the five competing presentation
  solutions) → presentation-1's consult material (the third parked
  card, the visual/Vantiel precedent); the ANTI-ARBITRAGE SPREAD →
  the Resource open question's donor (ANCHOR_REGION's price/flow row);
  the TURNOVER QUESTION → WORLD_AUTHORING §5 (the ECS cure = the
  function-loss probe aimed at holder mortality, the anti-freeze law);
  two parked notes: the Hot-Path placement pair (the road-traffic
  rider's material, beside the intake-27 topology proposal) + the
  weak-coupling authoring law (pack-3's event families)
- the largest cross-domain confirmation batch since intake-27
  (seed-in-save = INV-2/T2; no-cheats AI = the one-id door; infinite
  tooltips = mechanics.py; automation-red-flag = mech-2; direct-and-
  verify = the worldgen's MST-by-construction own form); refused
  binding: all dice-bending, the 3:1/2× constants, tech-deck/order/
  no-counterattack mechanics, Voronoi/two-layer-noise, the K-table
  as repo taxonomy (the do-not-import list in the ref file)
- doc-only (10 paths, over the soft limit per AGENTS §2.3 — the
  intake-31/32 precedent: ref/game_design_talks.md + the five §10
  rows + DEEP + phases.md §6 + DECISIONS + TASKS + WORLD_AUTHORING +
  NAV + STATUS + worklog; the third consecutive doc-only iteration,
  the D-022 exception consumed by this session's fresh call)
- verified BEFORE working at BASE_COMMIT 319e3e9 (1878+1 green; ruff
  not runnable in the sandbox — zero Python files touched) and
  re-verified after: 1878+1 green (doc-only, zero test change);
  iter-156 evicted per the cap
iter-165 · 2026-09-20 · kin1 — the world track's fourth W4 candidate (the
owner's «продолжай работу с world track» call, the working set's last): the
constructed kinship edge (candidate 4) tested at the authored band over
committed substrate only (the shelter law, the flood year, the notch habit,
the road's word) and CONFIRMED as THE WINTER KIN (ANCHOR_REGION §6.3)
- doc-only (6 paths, over the soft limit per AGENTS §2.3 — the worldbuild
  trio + STATUS/TASKS/worklog, the iter-164 doc-only precedent; the second
  consecutive doc-only iteration under the session's fresh owner request,
  the D-022 exception — the next authored-band move needs a fresh call):
  ANCHOR_REGION carries the edge (§6.3 — the mint's three rungs, the ladder,
  the lifecycle, the crisis + humor probes, the band split) + the mesh's G
  row (§5, seventh loop AUTHORED, three new interlock edges E⇄G/B⇄G/D⇄G,
  the disable test re-applied, the E-sibling note — one catastrophe, two
  circuits) + §4's three rows + §7.1's inherited-duty probe's third answer
  + §9's third chain walk; WORKPLAN §2/§6 the TESTED verdict (the W4
  working set COMPLETE); WORLD_TESTS §9 the run record + the
  humor/heartbreak row's extension
- the candidate's own falsifier PASSED (the Sarrow need demonstrated — the
  native generator confirmed: the stranded season's stores eight of the
  paper twenty, the care currently carried one way into the debt and the
  bend; the function-loss arbiter — the reciprocal function no existing
  mechanism performs); three first-exposure substrate gaps recorded, NOT
  routed (the relation form, the proof's read, the mourning surface); the
  embodiment options the owner's call class (the pole's iter-161 precedent)
- ANCHOR_REGION over the 600-line docs cap after the landing (762): the
  §6.1 substance law (AGENTS §6.1 — the unit's rungs/tables are substance,
  no cruft found in the pass; the cap is a signal, not a wall); kept, this
  entry the rationale
- verified BEFORE working at BASE_COMMIT 6d22a33 (1878+1 green, ruff
  clean — the pin re-confirmed) and re-verified after: 1878+1 green, ruff
  clean (doc-only, zero test change); iter-155 evicted per the cap
---
iter-164 · 2026-09-20 · water1 — the world track's second meso unit (the
owner's «продолжай работу с world track» call, the W4 candidates' next):
the practitioner water-governance node (candidate 3) authored as the STEP
BENCH over committed substrate only (the stair, the race's timbers, the
bank market, the seasons, the tally staff, the quarrel collection)
- doc-only (6 paths, over the soft limit per AGENTS §2.3 — the worldbuild
  trio + STATUS/TASKS/worklog, the iter-155/156/160 doc-only precedent):
  ANCHOR_REGION carries the unit (§6.2 — the ladder, the four steps, the
  year, the enforcement's three doors, the lifecycle table, the crisis +
  humor probes, the band split) + the mesh's F row (§5, sixth loop
  AUTHORED, three new interlock edges C⇄F/E⇄F/B⇄F, the disable test
  re-applied) + §7.1's Thornmill obligation ANSWERED; the candidate's
  own falsifier PASSED (the function-loss arbiter; the anti-council
  check by mechanism); §5's E band cell synced to the loop's own text
  (the iter-162 arming, a one-cell consistency fix inside the edited
  table); WORKPLAN §2/§6 the TESTED verdict; WORLD_TESTS §9 the run
  record + the humor row's authored-band upgrade
- honest residues: three first-exposure substrate gaps recorded, NOT
  routed (the water level, the setting verb, the hatch gate — the
  separate-track law); the embodiment options named, never committed
  (the pole's iter-161 precedent class); the live-session question stands
- verified BEFORE working at BASE_COMMIT 815476a (1878+1 green, ruff
  clean — the pin re-confirmed) and re-verified after: 1878+1 green,
  ruff clean (doc-only, zero test change); iter-154 evicted per the cap
---
iter-163 · 2026-09-20 · mech-2 — the introspection CLI's attention budget
(the standing row's build, the owner's «mech 2 давай сделаем» call): the
caps core + intake-21's postmortem + intake-22's DAG export as ONE
mechanism — defaults bounded, nothing dropped silently, expansion by flag
- mechanics.py: trace's unqualified default = the last 720 ticks + the
  naming tail note (27/43 lines on the canonical runs vs 175/277 full);
  matrix's default = the compact query-vocabulary inventory (--full the
  whole, the row's "past a screen" conditional now fact: 300+ lines on
  grim/province); why --event ID (the cause chain + the knowledge-wiring
  join + the cascade, capped with walk-back-naming truncation lines);
  matrix --dag (rules.json::systems as Mermaid via the scheduler's public
  parse); the law in the tool docstring, D-128/D-148 cited, no new D-row
- tests/test_mechanics.py +6 (the §9 claim packet — recount oracles for
  chain/children/edge counts, window policy, compact/full, honest edges);
  docs: NAV §5, TASKS (row collapse + ledger), phases.md §6 (the two
  cards' rider lines), STATUS re-pin; 7 paths (the iter-160 precedent)
- verified at BASE_COMMIT ee09105 (1872+1 green, ruff clean — the pin
  re-confirmed) and re-verified after: 1878+1 green, ruff clean;
  not-built residues (impact-query, first-divergence operator) stay
  zero-consumer per the first-consumer law; iter-153 evicted per the cap
---
iter-162 · 2026-09-20 · debt-1 — the standing row's build (the owner's
«продолжай работу, где логично» continuation call over the iter-161
routing): the flood debt's economy arm landed in province_pack as PURE
PACK DATA over res-1, zero core — the THIRD consumer arming
- pack: entities.json (the toll-taker's thin surplus coin 2 + the
  weighbeam chest coin 40 — the grim till's location form, the group
  taking no stock: the entity-lint closed vocabulary, the finding
  recorded), rules.json (the economy block: the net source +2 + the
  take +4, both sources — THE FOLD answering D-182's co-due limit by
  construction; the story listing + the budget re-declare 60→65),
  templates.json (the reckoning line); tests: test_debt1.py (+9, the §9
  claim packet), test_economy.py (the unarmed law's third consumer)
- docs: TASKS (row collapse + ledger), STATUS re-pin, the three
  worldbuild owners (ANCHOR_REGION §6.1, WORLD_WORKPLAN §2/§6,
  WORLD_TESTS §9); 11 paths (the iter-157/161 pack-landing precedent);
  zero corpus price (the golden T1 byte-untouched, pinned; the
  committed year run sees the flows by its own year-scale design)
- verified at BASE_COMMIT 2ea09ac (1863+1 green, ruff clean — the pin
  re-confirmed) and re-verified after: 1872+1 green, ruff clean;
  honest residues: no terminus/amortization in the flow vocabulary —
  the clearance lump + the punt purchase are discrete events, no
  player-scaled door armed; iter-152 evicted per the cap
---
iter-161 · 2026-09-20 · poleseed — the pole's embodiment seeds (the owner's
«надо решить что начали в прошлой итерации» call, the W4 options list):
the flood-story recognition token + the steal_target flag landed in
province_pack, PURE PACK DATA, zero core (the KI#87 precedent class)
- pack: entities.json (the pole's flag), actions.json (the read_pole hinge —
  the grim read_ticket pattern's second instance; the meta/steal notes sync),
  rules.json (the_flood_story over the toll-taker: type debt, a season's
  window), templates.json (the two read lines + the item-neutral pickpocket
  line); tests: test_poleseed.py (+11 — the lever chain read → mint →
  corner, the night partial, the lift + the pole-less hop, the total-failure
  arm, determinism)
- the debt-1 standing row OPENED (the economy arm routed on the owner's
  call); docs: ANCHOR_REGION §6.1/§9, WORLD_WORKPLAN §2/§6, WORLD_TESTS
  §7/§9, TASKS, STATUS; zero corpus price (no committed script reads the
  pole or lifts it); 11 paths (the iter-157 pack-landing precedent); honest
  residue: the family's own read/telling mints the cluster (dormant, no
  driver) — recorded in the secrets notes
- verified at BASE_COMMIT 26d57f7 (1852+1 green, ruff clean — the pin
  re-confirmed) and re-verified after: 1863+1 green, ruff clean; iter-151
  evicted per the cap

