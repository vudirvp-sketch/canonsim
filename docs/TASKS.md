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
> Phase 5 (Depth) CLOSED — gate PASS iter-102, D-136 (opened iter-73,
> the owner's start call, D-105; the full build column landed
> iter-73..98, every declared row live; the exit criterion "an emergent
> chain of 3+ events without the player" MET in its worldgen-fed form —
> the armed committed pack; ROADMAP §2 owns the state). Phase 6 (Packs & worldbuilder) **CLOSED — gate PASS iter-116, D-151**
> (opened iter-109, the owner's call, D-146; world-2 L1 the reskin day
> LANDED iter-112, D-149 — the exit criterion met by measurement; the
> verdict recorded on the owner's convening gate call; ROADMAP §2 owns
> the state — the roadmap's phase ladder COMPLETE, the standing work is
> the owner-gated backlog + the SoW horizon).

### Standing rows (owner-gated — the live queue; the ORDER owner decides,
this file owns composition, never order — D-113; every row REVALIDATED
iter-150, D-184; each build row's verification plan rides TEST_PLAN §9's
claim packet)

> The world-authoring track is NOT this queue: the setting's own plan
> (the anchor's A1/A2/A3 + the W-ladder) lives in
> `docs/worldbuild/WORLD_WORKPLAN.md` (D-186) — a separate track, never
> a second queue; a world-authoring need for engine capability lands
> HERE as a standing row on the owner's call.

- `engine-1` — DECIDED (iter-170, D-192, the owner's real-backend
  convening call — llama.cpp installed, the RTX 3080 Ti station, the
  three-model set, the real `llama-server` tests; TECH_NOTES §13 the
  evidence record): llama-server behind an EXPLICIT ADAPTER + GBNF, the
  file-contract frame (D-055) the insertion point, semantic typed
  policies never raw flags. The landing's boundary: CONTRACTS §4 (the
  D-177 pattern — the acceptance boundary, the non-goals, the
  experiment design incl. the four new arms). Move (a) CONVENED
  (iter-171, the owner's «за 1 раз как можно больше тестов… разбирайся
  на своих мощностях» call): the Rule-9 runner delivered OUTSIDE the
  repo (the Vantiel-handoff pattern, never committed) — one batched
  session covering the §8.5 gap rows + §4.3's four arms + the §13
  surface probes, sandbox-validated end-to-end at the owner's exact
  build b11064 (§13's sandbox block the surface record); the battery's
  GBNF mapping is the build's repo-side function previewed. Round 2
  (iter-172, the owner's bundle + crash report): the first `--arm all`
  crashed at s2c1 — the v1 grammar's un-encoded shape laws (E4B's
  `take` + `target:"tex_0000"` + texture; the door's RunnerError per
  PARSER_SPEC §4, the repo clean) + the battery's ParseError-only
  catch, plus the agreement census's reply-wrapper bug (the smoke
  bundle's agreement rows carry no signal); the runner v2 delivered
  outside the repo (the grammar encodes the door's shape laws per
  verb — canon/texture variants, canon-only targets, required
  drawn-N ticks; the `door_error` tally, never fatal; the census
  unwrapped), sandbox-checked against the real doors. Remaining:
  the owner's one RE-RUN with the v2 handoff (the bundle back —
  transcripts re-distilled per §8.2 source 3; the heartbeat's first
  local row; presentation-1's local evidence), then (b) the build
  landing (the GBNF mapping + the door wiring + the failure→ladder
  mapping) — INV-4 lifts there, the AGENTS §4/§8 edits riding it.
  Unlocked by the phase-1 gate; the dev-time external parser carried
  phase 2 to its gate PASS (iter-35) and carries mode C until the
  landing.
- `presentation-1` — the LLM presentation contract, engine-1's
  decision-input child, never a sibling competitor (intake-12, D-148): the
  model-facing serializer spec over the STABLE brief IR (BRIEF_SPEC §7
  bytes + §7.1 protocol — the D-055 file-contract pattern's fourth
  instance), written FROM the {3–8B, GBNF} arm's results at the engine-1
  call (D-022 — a contract without a consumer has unknown requirements).
  Absorbs `st-4` at write time (the call budget + the transcript-tail
  contract + thinking-as-ephemeral-texture + the Script Tax clause — one
  owner, never two). The spec's shape when written: a thin mapping table
  over the existing 8 blocks + `narrator_protocol` — never a second
  re-labeling vocabulary (D-024). Exit criterion: the weak-arm run on owner
  hardware. Evidence base: TECH_NOTES §10/§11/§13 (§13 the real-backend
  record); consult material at write
  time: the intake-30 visual-system card (phases.md §6 — the visual
  surface's parked residue: the development-order law, the fidelity
  target, the rejection table; D-187/D-174's surface ownership) + the
  intake-32 Vantiel card (`docs/ref/vantiel.md` — the model boundary's
  parked residue: the re-expansion law — a bounded context bundle keeps
  stable event/entity handles and re-expands deterministically from canon,
  never a second truth — + the staged-interpretation sketch input →
  interpretation → context → model proposal → validation → prose; D-190,
  the falsifier: the real consumer vs the current brief/retrieval stack on
  context cost, traceability, re-expansion correctness) + the intake-33
  outcome-perception card (`docs/ref/game_design_talks.md` §"What we
  take" — the layered legibility ladder: truth never bends / failure
  carries cause + avoidance path / odds as expectation bands, never naked
  percentages / transparency opt-in by flag, nothing dropped silently /
  outcomes legible through residue / stakes irreversible; D-191, the
  falsifier: at the write, each layer either changes the narrator
  document's shape or dissolves as already-satisfied).
- `parse-2` — disambiguation buttons + multi-intent utterances, each half
  behind its own gate (PARSER_SPEC §7; sharpened iter-150): BUTTONS wait on
  a frontend consumer (mode C live play — a UI affordance, never a parser
  change); MULTI-INTENT waits on live-session evidence that real utterances
  carry N intents (one classification per document today); neither half is
  "improve the parser" — the phase-2 grammar is gate-PASSED (D-064) and the
  boundary stays closed until a named consumer opens it.
- `st-2` — the identity promotion door (pack grammar beyond `take`, the
  D-054 machine; the read-path half landed as tex-1, iter-62/D-091):
  consumer-first, PARKED — no committed pack has wanted promotion beyond
  `take` (pack-1/pack-4 built without the door: the pawn-ticket hinge and
  the seams ride ordinary events + folds); the door (and the bg-5
  counted-promotion alternative with it) waits until a pack's design names
  the beat it needs — never a speculative build.
- `scav-1` — offline compaction = scavenge with tombstones: derived-store
  entries drop with tombstones AFTER the chronicler's rollups make them
  rebuildable; committed logs never edited (INV-5). Measurement before
  mechanism, PARKED — the chronicler (iter-64) and the fold checkpoints
  (iter-80) both landed, no derived-state size problem on record; premature
  until a real long-session cost is measured (a derived-store size census
  at a named horizon) — the intake-29 admission rule applied to our own
  queue.
- `st-5` — containers: the `in` relation + entity-birth promotion
  (blueprint §7): the first real consumer decides (a pack wanting portable
  objects, a res-1 sink shape — CONCRETE since res-1 landed iter-146/D-179;
  group-scale entity birth already exists, depth-7's condensation,
  iter-93/D-127). Never a speculative build.
- `qa-1` — DONE (iter-168, the owner's chat call over the row): mypy
  --strict on `core/` 207 → 0 at zero runtime change (1885+1 green both
  ends, goldens byte-untouched); the tool stays optional per D-031 (no
  dev-dep, no CI row — enforcement the owner's call); KI#88/#89 the
  found holes (the lint-side closures routed).
- `pack-3` — the Sci-Fi setting candidate (owner sketches; REWRITTEN
  iter-150): the stale "blocked until the 2nd-setting gate" is GONE —
  phase 6 CLOSED (D-151), the second-setting shape answered (TRAVEL,
  D-146) and consumed (road/province/grim/pressure committed). ONE
  candidate for the next authored pack slot — the owner's call when a slot
  opens, against the pressure pack's post-T1 rows (the legal exclusion
  D-134, the cultures name-1, the road traffic depth-7, the lore hooks
  D-140) and the intake-20 pack-candidate consult card; a
  genre-portability experiment (the engine's universality claim, INV-3's
  substance) its natural verification framing if picked.
- `bg-6` — the SoW integration audit, owner-deferred "until unavoidable"
  (D-055): a read-only pass over Soul-of-Waifu — extension points for a
  separate simulation chat mode, where llama.cpp sits, what the frontend
  must NOT own (the dumb-terminal contract, VISION §10). Output: a
  TECH_NOTES section + the `SOW_INTEGRATION_SPEC` sketch (SPECS_BACKLOG's
  trigger-gated row — the spec itself fires only at bg-6). Never blocks
  track A.
- `doc-2` — REFERENCES.md license/URL re-verification, quarterly
  (alongside the TECH_NOTES review). RUN 2026-09-13 (iter-114): the
  research-layer re-point (17 ref files + REFERENCES_DEEP §2) + the
  license/URL pass (45 repos probed; deltas: dnd-llm-game → MIT, pyDF →
  CC BY-NC-SA file present, RACEngine → bare stub; `a16z/ai-town` →
  `a16z-infra/ai-town`; pcg.wikidot + open5e health notes in the catalog).
  Next run: the next quarterly (owner-called per D-022) or at a phase-6
  pack intake, whichever comes first.

### Iteration ledger (iter-116..171 — the detailed sections collapsed at the
owner's memory-GC calls, iter-140 + iter-151, the iter-102 precedent; the
iter-151 pass restored the iter-140 collapse after a stale-base archive apply
had clobbered it — D-185; the iter-151..156 one-liners backfilled at iter-158
— the practice had lapsed after the compaction; per-iteration detail: the
D-rows + phases.md §6's blocks + worklog at the time + git — never restated
here, the header's own law)

- iter-172 · 2026-09-21 · engine-1 (move a, round 2) — the owner's
  battery bundle back + the `--arm all` crash triaged (the «ты просил
  бангл прислать с тестов, но там еще и ошибки в консоли вылезли»
  report): the smoke cut green on every arm, the full corpus crashed
  at s2c1 (E4B's one-path combo through the v1 grammar; the door's
  RunnerError per PARSER_SPEC §4 — the repo clean, zero code change,
  INV-4 unchanged); THREE runner defects fixed in the v2 handoff
  (never committed): the grammar now encodes the door's shape laws
  per verb (canon/texture path variants, canon-nouns-only targets,
  required drawn-N ticks; the JSON-schema twin the same), the
  `door_error` tally (terminal, `door_shape_errors`, never fatal),
  and the agreement census unwrap (v1: intent-vs-reply-wrapper, every
  comparison kind_mismatch — the smoke bundle's agreement rows carry
  no signal); sandbox-validated against the REAL doors (v1's language
  contains exactly the crashing form; v2's 2109 docs pass the laws +
  the gate; the crash reply replayed → tallied, harness reusable);
  TECH_NOTES §13.1 corrected + the v2 record; doc-only, 1900+1 green,
  ruff clean.

- iter-171 · 2026-09-21 · engine-1 (move a) — the experiment CONVENED (the
  owner's «давай за 1 раз как можно больше тестов… лучше вообще выяснить
  все про llama.cpp и дальше уже разбирайся на своих мощностях» call):
  the Rule-9 runner built + delivered OUTSIDE the repo (the Vantiel-handoff
  pattern — engine1_runner/grammar/battery + the runbook, never committed),
  one batched owner session = the §8.5 gap rows (51-utterance corpus raw →
  1 re-ask, F1–F6 deviation with the guess-within-grammar tally, the bg-7
  prose families (ii)–(v), the per-component p50/p95 columns) + §4.3's four
  arms + the §13 surface probes at the owner's build; sandbox-validated
  end-to-end FIRST (llama.cpp b11064 CPU — the owner's exact commit — a
  1.7B model, every arm smoke-run through the REAL doors: raw GBNF
  validity 100% at n=2 smoke, the prose ladder + C3.5 degradation live);
  TECH_NOTES §13 gains the sandbox surface block (the router, POST /props
  the silent no-op, -np semantics, grammar-on-chat, the GBNF dialect
  facts, determinism mini, cancellation, restart timing — every §13
  "not established" software-bound item closed; the station-bound list
  narrowed); zero engine code in the repo, INV-4 UNCHANGED, doc-only,
  1900+1 green, ruff clean.

- iter-170 · 2026-09-21 · engine-1 — the runtime inference engine DECIDED
  (the owner's real-backend convening call: llama.cpp + the RTX 3080 Ti
  station + the three-model set + the real test evidence, the disposition
  and the session research both riding the call): llama-server behind an
  explicit adapter + GBNF, the file-contract frame the insertion point —
  D-192 the decision, CONTRACTS §4 the build contract (the D-177 pattern:
  semantic policies never raw flags, the reproducibility tiers, the
  non-equivalences, the non-goals, the experiment design incl. the four
  new arms — one-vs-two-model, seeded-local determinism, the GBNF
  latency penalty, mode-A-at-the-weak-arm), TECH_NOTES §2 refreshed +
  §13 the evidence record (the measured facts, verified against the
  owner's raw logs); presentation-1's evidence base gains §13; INV-4
  UNCHANGED (lifts at the build's own iteration, CONTRACTS §4.1 D6);
  doc-only, 1900+1 green both ends, ruff clean; the experiment + the
  build the owner's next calls.

- iter-169 · 2026-09-21 · qa2 — the KI#88/#89 lint-side closures (the
  owner's «проработай открытые в прошлой итерации ki и все связанное,
  нужно доделать все с технической частью» call over the two holes
  qa-1 opened and routed): BOTH KIs closed at LOAD, zero runtime
  behavior change on well-formed packs — KI#89 via the shared
  `lint_direct_keys` row (packlint/shared.py, the lint_echo_cond
  family; presence + type + non-emptiness for the five record-reading
  tests' directly-indexed keys) wired into every `requires` declaration
  site (action canon, texture block, urgency beat gate, faction gate —
  the iter-45 leverage `who` precedent generalized to its family);
  KI#88's first arm via the on_action actor vocabulary split (ACTOR_KEYS
  = world | source_actor, owned in core/onaction.py; the reaction
  event's actor is a schema-required string — `source_target` refused
  with the rationale, the assert the backstop); KI#88's second arm via
  the target-sourced check row reading the door's OWN `needs_target`
  predicate (extracted from validate_shape — one source, two readers,
  agreement by construction); tests/test_qa2.py +15 (the §9 claim
  packet), 1900+1 green both ends, goldens byte-untouched, ruff clean,
  mypy --strict core/ 0; the `flag` test's own twin hole (and kind's
  `is`, the `with`/`axis`/`value` presence) recorded, not routed — the
  owner's call class.
- iter-168 · 2026-09-21 · qa1 — the type-discipline audit (the owner's
  «там еще была задача qy 1 что ли, связанная с проверкой кода» chat
  call naming the standing row): mypy --strict on `core/` taken 207 → 0
  across 36 files at ZERO runtime behavior change (1885+1 green both
  ends, the goldens byte-untouched, ruff clean) — the root-fix shape:
  `_require(condition: object)`, the `Importance`/`Fidelity` Literal
  funnels, the RetrievalIndex slot annotations, the Mapping read-only
  widening (fold's dict `Projection` the owner), the TypeGuard
  `_is_int`/`_is_number`, the Iterable bridges in `Pack.entity`/
  `action`, the assert-after-require narrowings across packlint, the
  shadowing kills, log.py's first-branch annotations; 29 core files
  (the §2.3 soft limit noted — a repo-wide strict pass); two holes
  made loud: KI#88 (asserts landed, the lint-side closure the residue)
  + KI#89 (the iter-45 `who` family, fix routed); the tool stays
  optional (D-031 unchanged — no dev-dep, no CI row).
- iter-167 · 2026-09-21 · stepread — the step bench's first embodiment (the
  owner's «продолжай работы, что логичнее всего сейчас начать» continuation
  call over STATUS's embodiment routing — the natural doc-streak breaker
  after three doc-only iterations): the step's close read, the unit's setting
  verb (the §6.2 gap text's own "a future embodiment's own class, the
  read_pole precedent"), landed in province_pack as PURE PACK DATA, zero
  core change — the read_stair hinge (the read hinge's third instance: the
  grim read_ticket first, the pole second; the family's first location-kind
  target — the stair IS the carrier) minting the literal token the_step_law
  to the reader: the ORDER the road never learns from the books (§6.2's
  knowledge asymmetry; §7.1's stranger row — the road's misread correctable
  in play, the meaning slice's misread-correcting half widened to the
  committed band; the brief's recalled facts the read surface); the token
  deliberately PLAIN KNOWLEDGE, never a secret (the vale's own category, no
  lever — no secrets entry, no cluster, the registry stays two keys); the
  unlit weir steps the night read down to partial; the field_in pin + the
  co-location gate die at the door as named rejections; zero corpus price
  (no committed script reads the stair); tests/test_stepread.py +7 (the §9
  claim packet); the remaining embodiment options (the notch record's arming,
  the hatch) stay the owner's call class; the water level's half stays
  owner-routed (the read mints the LAW, never the PRESENT).
- iter-166 · 2026-09-21 · intake33 — the game-design practitioner talks
  corpus routed (the owner's «изучи gamedesign_knowledge_base.md и
  определи что можно перенять, адаптировать или чем вдохновиться…
  распределить по документации» research call over the uploaded
  consolidated five-source knowledge base: Sawyer PoE attributes /
  Meier psychology / Battle Mode micromanagement / Johnson Old World /
  Wolverson procgen): PARTIALLY CONFIRMED — a perception +
  economy-craft donor, never a systems donor, differentiated from the
  refused UNIFIED GDC base (intake-30's F2) by the one domain no prior
  family owns — outcome-perception psychology. Adopted: the
  OUTCOME-PERCEPTION LAWS CARD (the layered legibility ladder, the
  combined form of the five competing presentation solutions — each
  minus neutralized by another layer) → presentation-1's consult
  material (the third parked card, the visual/Vantiel precedent) + the
  ANTI-ARBITRAGE SPREAD (exchange lossy by construction — the Resource
  open question's donor: ANCHOR_REGION's "how does scarcity become a
  measured price/flow cycle?"; falsifier: the water's function-loss
  arbiter) + the TURNOVER QUESTION (the ECS cure = the function-loss
  probe aimed at holder mortality — the anti-freeze law →
  WORLD_AUTHORING §5; consumers: the camp's meso half, W5's biography
  arc) + two parked notes (the Hot-Path placement pair beside the
  intake-27 topology proposal — the road-traffic rider's material; the
  weak-coupling authoring law — pack-3's event families); the largest
  cross-domain confirmation batch since intake-27 (seed-in-save =
  INV-2/T2; no-cheats AI = the one-id door; infinite tooltips =
  mechanics.py; automation-red-flag inverted = mech-2's
  nothing-dropped-silently; direct-and-verify = the worldgen's
  MST-by-construction superior own form); refused binding (all
  dice-bending — perceived fairness only at the render layer, never the
  roll layer; the 3:1/2× constants — threshold leakage; tech-deck /
  order-system / no-counterattack — no substrate, no consumer;
  Voronoi/two-layer-noise — saturated by ref-8/ref-9 + the LOD ladder;
  the K-table as repo taxonomy); doc-only (10 paths, over the soft
  limit per AGENTS §2.3 — the intake-31/32 precedent: the source record
  ref/game_design_talks.md + the five §10 catalog rows + the DEEP index
  + the phases.md §6 stub + DECISIONS + TASKS + WORLD_AUTHORING §5 +
  NAV + STATUS + worklog; the third consecutive doc-only iteration,
  the D-022 exception consumed by THIS session's fresh owner research
  call — the next authored-band move needs a fresh call); 1878+1 green
  both ends at BASE 319e3e9 (doc-only, zero test change; ruff not
  runnable in the sandbox — zero Python files touched)
- iter-165 · 2026-09-20 · kin1 — the world track's fourth W4 candidate (the
  owner's «продолжай работу с world track» call, the working set's last): the
  constructed kinship edge (candidate 4) tested at the authored band over
  committed substrate only and CONFIRMED as THE WINTER KIN, doc-only — care
  performed under the shelter law through one full stranded season mints a
  socially recognized kin edge (the milk-kinship MECHANISM, never the
  practice; the Hindu Kush foster-relations donor, ref-21's named pair):
  the winter's board through a stranded season, never the night's board (the
  rarity gate); the edge binding both ways (the guest's line owing
  protection + the mourning of the house's dead; the host's house owing the
  barred purse — the purse-read bend's own boundary, the exclusion rung);
  the edge passing down both lines (the drowned generation's notch now the
  toll-taker's — never unnotched, the recognition living); the candidate's
  own falsifier PASSED (the Sarrow need demonstrated — the native generator
  confirmed, the stranded season's stores eight of the paper twenty, the
  care currently carried one way: household → debt → the bend, the committed
  symptom; the function-loss arbiter — the reciprocal function no existing
  mechanism performs; the anti-noise check — the mint flood-year rare, the
  edge priced by the lifecycle); the mesh's seventh loop G AUTHORED
  (ANCHOR_REGION §5: the notch → the recognition → the obligations → the
  recognition again, state-closing; the disable test + the shared-stage
  rule re-applied, the E-sibling note — one catastrophe, two circuits) +
  three interlock edges (E⇄G one winter two prices, B⇄G the feud's
  arithmetic meeting the notch at the door, D⇄G the road materializing the
  return); the crisis probe (the return: the guest's son at the stair in
  the thin months) + the humor probe (the pole-counting joke,
  position-dependent) + the heartbreak row's first authored half (the
  mourning rung — the flood's dead kept by name outside blood); three
  first-exposure substrate gaps recorded, NOT routed (the relation form, the
  proof's read, the mourning surface — the separate-track law); the
  embodiment options stay the owner's call class (the pole's iter-161
  precedent); the W4 working set COMPLETE; 1878+1 green + ruff clean both
  ends at BASE 6d22a33 (doc-only, zero test change); 6 paths
- iter-164 · 2026-09-20 · water1 — the world track's second meso unit (the
  owner's «продолжай работу с world track» call, the W4 candidates' next):
  the practitioner water-governance node (candidate 3) authored as THE STEP
  BENCH, doc-only, over committed substrate only — the weir stair's three
  hands over one head (Ketta's pool, Wilmot's race, Maren's run), the head
  named by the stair's wet step (four rungs; the committed high_water line
  the fourth's own text), held by the practitioners' reading at the season's
  turn, enforced at the water by the users themselves (the hatch wattled,
  the beam's talk over the committed rumor channel, the keeper's
  book-setting read against the tally's notch); the candidate's own
  falsifier PASSED (the function-loss arbiter: the allocation order among
  uses is a function neither the guild's paper nor the crossing's custom
  performs; the anti-council check by mechanism — no axis, no threshold,
  no institutional door, Loop A's family negative image); the mesh's sixth
  loop F AUTHORED (ANCHOR_REGION §5: the recurring band → the step rule →
  the allocation's acts → the head again, state-closing; the disable test
  + the shared-stage rule re-applied) + three interlock edges (C⇄F, E⇄F,
  B⇄F — the timber law died in the feud's fire, the water law lives in
  stone); the chronicle's un-themed quarrel collection (pact_signed, three
  members) themed as the stair pact; §7.1's Thornmill household obligation
  ANSWERED (the race's keeping); the crisis probe (the dry long_light, the
  hatch found open) + the humor probe (the step's position-dependent joke,
  WORLD_TESTS' humor row upgraded to the authored band) run at the authored
  band; three first-exposure substrate gaps recorded, NOT routed (the
  water level, the setting verb, the hatch gate — the separate-track law);
  the embodiment options stay the owner's call class (the pole's iter-161
  precedent); 1878+1 green + ruff clean both ends at BASE 815476a (doc-only,
  zero test change); 6 paths

- iter-163 · 2026-09-20 · mech-2 — the introspection CLI's attention budget
  (the standing row's build, the owner's «mech 2 давай сделаем» call; the
  caps core + the two riders in one mechanism): DEFAULTS bounded, nothing
  dropped silently, every expansion an explicit flag (D-128's effect line
  + D-148's [truncated:N] law applied to CLI defaults) — `trace`'s
  unqualified default capped to the last 720 ticks (measured 27/43 lines
  on the canonical runs vs 175/277 full) with the tail note naming the
  flags; `matrix`'s default the compact query-vocabulary inventory (the
  row's "past a screen" conditional now fact: 300+ lines on the grown
  packs), `--full` the whole listing; `why --event ID` the single-event
  postmortem (intake-21: the cause chain + the knowledge-wiring join +
  the cascade, counts re-derived, detail capped with named walk-back
  queries); `matrix --dag` the systems read/write graph as Mermaid
  (intake-22: the projection of rules.json::systems via the scheduler's
  public parse, never a runtime); tests/test_mechanics.py +6 (the §9
  claim packet: recount oracles for chain/children/edges).
- iter-162 · 2026-09-20 · debt-1 — the crossing household's flood debt economy
  arm (the standing row's build, the owner's «продолжай работу, где логично»
  continuation call over the iter-161 routing): the province pack's `economy`
  block armed over the res-1 substrate as PURE PACK DATA, zero core — the
  THIRD consumer arming (grim first, pressure second): the accounts (the
  toll-taker's thin surplus coin 2; the guild's chest at the weighbeam
  loc_malby coin 40 — the grim till's location form, the group taking no
  stock: the entity lint's closed group vocabulary, the finding recorded),
  the toll-surplus flow (the net source +2) + the guild's collection (the
  take +4) — the FOLD answering D-182's named co-due limit by construction
  (both sources, the gross six's split the notes' only mirror); the paper
  twenty / punt twelve / five-years-to-clear authored arithmetic in the
  notes (ONE COIN, TWO CLAIMS as live account state); the reckoning a story
  beat (account_sourced listed, the tale carrying the year's lines); the
  budget's honest re-declare (60→65); tests/test_debt1.py +9 (the §9 claim
  packet: census, the committed year band, the tale, the golden
  byte-identity, the fold, the legible arithmetic, the fingerprint
  both-arms, determinism) + the unarmed law's third-consumer update
  (test_economy); zero corpus price (the golden T1 byte-untouched, pinned).
- iter-161 · 2026-09-20 · poleseed — the pole's embodiment seeds (the owner's
  «надо решить что начали в прошлой итерации» call): the flood-story
  recognition token + the steal_target flag landed in province_pack as PURE
  PACK DATA, zero core change (the KI#87 precedent class) — the read_pole
  hinge (the grim read_ticket pattern's second instance) minting
  the_flood_story, the secrets registry's second key over the toll-taker
  (type debt, a season's window; the lever chain read → mint → corner
  test-pinned); the pole flagged liftable-unseen, the verb-gate boundary's
  unless-arm (the take/drop_break gates unchanged, the lift flips the
  carrier binding and the road-leg beat walks the second hand pole-less —
  the player-facing ablation armed, tests/test_poleseed.py); the debt-1
  standing row OPENED (the economy arm routed on the owner's call); zero
  corpus price (no committed script reads the pole or lifts it).
- iter-160 · 2026-09-20 · w4exp1 — the world track's W4 bounded experiment
  (the owner's «продолжай работу по world track» call — the working set's
  own first move): the crossing household walked once through the full
  operator stack on existing substrate; CONFIRMED at the split band, the
  transfer KEPT (the carrier-availability law + the verb-gate boundary +
  the carrier-ablation probe; the debt's lifecycle table authored; the
  candidates 1/2 informed); the debt's arithmetic the third recorded
  exposure, owner-routed; the vigil-null + reputation-writer findings
  recorded, not routed; doc-only.
- iter-159 · 2026-09-20 · intake-32 — the Vantiel research handoff routed
  (D-190, the owner's routing call over the uploaded prior-session handoff,
  the handoff's substrate map re-verified claim-by-claim at HEAD):
  PARTIALLY CONFIRMED — a SEPARATIONS donor, never subsystems (all ten
  distinctions substrate-owned); the source record docs/ref/vantiel.md
  (ref-22 + the REFERENCES/REFERENCES_DEEP/NAV wiring) + the presentation-1
  consult material (the re-expansion law + the staged-interpretation sketch,
  parked behind the owner gate); the reject list binding; doc-only.
- iter-158 · 2026-09-20 · intake-31 — the Kurvitz consolidated research routed
  (D-189, the owner's routing call over the uploaded prior-session research
  residue): PARTIALLY CONFIRMED — mined as a generator library, never a
  worldbuilding layer; the W4 operator set + the test operationalizations +
  the bounded crossing-household experiment adopted into the worldbuild owners,
  the source mechanics recorded at docs/ref/kurvitz.md (ref-21); the TASKS
  ledger backfill + the worldbuild embodiment sync riding — doc-only.
- iter-157 · 2026-09-20 · companion1 — the companion arming (companion-1 +
  tune-3, together as the row's own law; the owner's «довести до ума сам
  генератор» call): the crossing household's second hand embodied in
  province_pack (Dellan — ANCHOR_REGION §6.1's first meso unit, the pack
  embodiment §9 names the engineering side), the FIRST committed NPC
  movement source (the road-leg urgency beat, kind=move — the census flip),
  the traveling-knower probe CONFIRMED (the crafted twin: alarm_adjacent
  heard+vague on the MOVER, the panic echo +10, the telling carried the
  shout to the player), the mode B voice + the paired escort leg + the
  arrival snapshots pinned, the punt pole committed (KI#87 CLOSED); zero
  core change — D-188.
- iter-156 · 2026-09-20 · mesh1 — the world track's W3 causal mesh audit
  (doc-only): five loops pass the disable test + the shared-stage rule (four
  COMMITTED + the credit loop AUTHORED), the anti-double-count ruling applied
  once, four interlock edges named — ANCHOR_REGION §5, WORLD_TESTS §9.
- iter-155 · 2026-09-20 · anchor1 — the world track's first anchor pass
  (doc-only): A1 the causal map's unsupported links deepened, A2 the crossing
  household authored as the first meso unit (ANCHOR_REGION §6.1), A3 the
  high-water double-toll meaning slice (§7.1); KI#87 opened (the punt pole's
  item gap).
- iter-154 · 2026-09-20 · intake-30 — the agent-dense v3 hybrid pack routed
  (D-187): the corpus map (nine units already owned), the agent/ layer refused
  (no docs/agent/), the visual consult card parked behind the SoW fence with
  presentation-1 wired, the UNIFIED GDC KB not admitted.
- iter-153 · 2026-09-20 · worldbuild1 — the worldbuild archive intake (D-186):
  the active worldbuilding surface landed as docs/worldbuild/ (10 files, the
  README index + the terminology fence) + the agent-path wiring (NAV §1/§2/§3,
  the README map, the separate-track pointer).
- iter-152 · 2026-09-20 · docgc2 — the CORE_DESIGN_RESEARCH deletion + the
  evidence-class citation sweep (27 paths re-pointed to their live owners;
  D-185's recorded next step executed).
- iter-151 · 2026-09-20 · docscomp1 — the semantic documentation compaction pass
  (D-185): DECISIONS 63→30 rows, TASKS 2422→914 + the thirteen standing rows
  extracted, phases.md §6 restored compact, NAV/TEST_PLAN/REFERENCES_DEEP
  re-compacted, the re-points restored.
- iter-150 · 2026-09-20 · revalid-1 — the AGPLv3 relicense (LICENSE + the
  README's License section, D-183) + the standing-backlog revalidation (all
  13 rows audited, 8 revised — D-184) — doc-only.
- iter-149 · 2026-09-20 · pack-4 — the pressure-city pack (T1): the
  displacement law as pure pack data, ZERO CORE CHANGE; res-1's second
  consumer arming; the first authored non-scaffold pack — D-182.
- iter-148 · 2026-09-19 · pack-1 — the grim tavern pack: the dark line as
  pure pack data (the ladder with the world's reply, the consent split +
  its fact/belief lint, the pawn-ticket hinge); res-1/since-1 first
  consumer armings — D-181.
- iter-147 · 2026-09-19 · since-1 — the re-encounter delta: the per-entity
  encounter-epoch fold, the cards' since-segments; the unarmed landing —
  D-180.
- iter-146 · 2026-09-19 · res-1 — the economy substrate: the account
  primitive, the three verbs through the canon door, the derived prices;
  the underflow floor's two arms; the unarmed landing — D-179.
- iter-145 · 2026-09-19 · roads-1 — the generated-exits pass: the MST
  backbone + mutual k-nearest overlay over the claimed locations; the one
  shared exits read (authored wins); the pack.py split rider
  (core/packlint/) — D-178.
- iter-144 · 2026-09-19 · contracts — the three pre-implementation contract
  writes (roads-1/res-1/since-1): docs/CONTRACTS.md + the row pointers —
  D-177 (doc-only).
- iter-143 · 2026-09-19 · ci-1 — the GitHub Actions runner: pytest + ruff on
  push/PR to main, PYTHONHASHSEED=0, Python 3.12.14 the env pin — D-176.
- iter-142 · 2026-09-19 · intake-29 — the external-audit / roadmap-review
  output routed: the audit CONFIRMED (live-verified), six contract
  sharpenings adopted into the rows, two rider rules, the intake admission
  rule — D-175 (doc-only).
- iter-141 · 2026-09-19 · intake-28 — the Stålberg-conspectus /
  transplantation-method output routed: the combination fence adopted (the
  fifth check's operational sharpening), the local-pattern hypothesis
  routed to the standing consumers — D-174 (doc-only).
- iter-140 · 2026-09-19 · intake-27 — the level-design & worldbuilding
  consolidation routed: five compact instruments adopted (the reader law,
  the priced-option question, the top-LOD readability question, the
  realization table, the sacrifice protocol), the topology-aware hook
  distribution the proposal — D-173 (doc-only; the same-numbered
  iter-140-memgc commit carried the first GC pass, D-185).

- iter-139 · 2026-09-19 · world-2 L2 (the verdict) — the two-level
  gate's level-2 question ANSWERED on the owner's convening call: the
  honest scope DELIVERED at the measured band, the depth's distribution
  the recorded residue, the row closed — D-172 (doc-only).
- iter-138 · 2026-09-19 · intake-26 — the verification-lenses research
  routed: the selection grammar ADOPTED in the compact form (TEST_PLAN
  §9 — the claim packet + the selection table), the full catalog held
  in the intake block, the measurement bound to the next build row —
  D-171 (doc-only).
- iter-137 · 2026-09-19 · world-2 L2 (the depth audit) — the three lens
  documents taken as claims, the converged depth unit, the three
  measured arms, the A–H ledger, the critical separation — D-170
  (doc-only; verdict material, the L2 call the owner's).
- iter-136 · 2026-09-19 · world-2 L2 (slice 4: the calendar) — the
  market days / the fairs / the river's seasonal ride + the weather's
  seasonal layer + the composed YEAR experiment; KI#86; +16 tests —
  D-169.
- iter-135 · 2026-09-19 · world-2 L2 (slice 3: the triangle) — the
  factions armed 0→1 + the deep feud history + the composed
  outcome-divergence experiment; KI#85; +11 tests, the golden regen —
  D-168.
- iter-134 · 2026-09-19 · cumulative-1 — the intake family 4..25 taken
  as ONE body: the arming census, the five cumulative findings, the
  convergence onto slice 3 — D-167 (doc-only).
- iter-133 · 2026-09-18 · intake-25 — the re-verification consolidation
  pack routed: the two measured probes, the dispositions stand — D-166
  (doc-only).
- iter-132 · 2026-09-18 · intake-24 — the cross-domain
  principle-transplantation synthesis routed: the P1–P6 map all OWNED,
  the principle index card — D-165 (doc-only).
- iter-131 · 2026-09-18 · intake-11 re-entry — the pressure-city donor
  re-uploaded & re-verified: D-147 stands, zero new findings (doc-only).
- iter-130 · 2026-09-18 · intake-23 — the world-execution /
  spatial-topology / social-information research routed: the six engine
  questions probed, the world-structure consult card — D-164 (doc-only).
- iter-129 · 2026-09-18 · intake-22 — the ComfyUI/modularity
  consolidation routed: the verdict set re-verified at a real clone, the
  modularity consult card — D-163 (doc-only).
- iter-128 · 2026-09-18 · intake-21 — the unified-observatory /
  worldbuilder / agent-gateway research routed: the four-question
  observability card — D-162 (doc-only).
- iter-127 · 2026-09-18 · intake-20 — the content-archetype /
  pack-strategy framework research routed: the 26-item reconciliation,
  the capability truth table, the pack-candidate consult card — D-161
  (doc-only).
- iter-126 · 2026-09-18 · intake-19 — the persistent-groups /
  settlement-development research routed: the zero-core-edit settlement
  probe, the gaps routed to standing rows — D-160 (doc-only).
- iter-125 · 2026-09-18 · intake-18 — the player-decision-mechanics
  research routed: the A–G candidate verdicts, three measurements
  re-derived, compellingness fenced to the SoW horizon — D-159
  (doc-only).
- iter-124 · 2026-09-18 · intake-17 — the interface-oriented procedural
  composition research routed: the five candidate principles verified,
  two measurements re-derived — D-158 (doc-only).
- iter-123 · 2026-09-18 · intake-16 — the procedural-generation research
  routed: the four domain verdicts, three measurements re-derived —
  D-157 (doc-only).
- iter-122 · 2026-09-18 · intake-13 re-entry — the open-ended actions
  review re-uploaded & re-verified: D-150 stands, zero new findings
  (doc-only).
- iter-121 · 2026-09-18 · intake-15 — the narrative-design research
  dossier routed: the 18 laws re-derive the standing families, since-1
  the one genuine residue — D-156 (doc-only).
- iter-120 · 2026-09-18 · intake-14 — the causal-architecture research
  bootstrap routed: five architecture questions resolved against
  standing owners — D-155 (doc-only).
- iter-119 · 2026-09-13 · world-2 L2 (slice 2: the cultures half) — the
  two name-1 phonotactic profiles, the condensation travelers, the
  cultures block — D-154.
- iter-118 · 2026-09-13 · world-2 L2 (slice 1: the skeleton) — the
  province pack's 324-site generated surface, the settlements on the
  travel lattice, the spine records, the T1 twin — D-153.
- iter-117 · 2026-09-13 · pack-ci — the admission-lint rungs LIVE (the
  teleology gate + the live-char crosswalk + the price-marker lint in
  `core/pack.py`) — D-152.
- iter-116 · 2026-09-13 · phase-6 gate — done (verdict: PASS, D-151);
  ROADMAP §2 CLOSED, the ladder complete; the doc debts paid (DECISIONS
  44→30, NAV resync, README resync).

### iter-115 · intake-13 — the open-ended actions & honest-simulation review routed — done (doc-only, the owner's research call)

The routing verdict set — the doctrine half CONFIRMED as standing law, four proposals routed to existing owner-gated rows, zero build-grade items: D-150; the block: phases.md §6's intake-13. Detail: worklog iter-115 + git.

### iter-114 · doc-2 quarterly — the re-point + the license/URL re-verification — done (doc-only, the owner's call)

17 ref files + the REFERENCES_DEEP §2 verdict columns re-pointed to the current-state owners; 45 repo paths probed alive, 3 license deltas, 2 site health notes, the a16z re-point. Detail: worklog iter-114 + git.

### iter-113 · documentation lossless audit — done (doc-only, the owner's call)

Verdict: the architecture HOLDS, ZERO removals (the cross-layer repetition is the declared link-never-restate pattern); one sync defect repaired (REFERENCES_DEEP §2 +8 rows); the doc debts routed to the phase-6 gate. Detail: worklog iter-113 + git.

### iter-112 · world-2 L1 — the reskin day — done (the owner's «приступай»)

`content/road_pack/` the TRAVEL-loop reskin (SRD 5.1 nouns, CREDITS sidecar, the first committed travel-price arming 150/210/300/360); the clock 14m24s, ZERO core edits git-verified; the T1 twin +7 + ROAD_STOPLIST; 1660+8 → 1668+1 green. The exit criterion MET BY MEASUREMENT: D-149. Detail: worklog iter-112 + git.

### iter-111 · intake-12 presentation-consolidation routing — done (doc-only, the owner's call)

The eight-row verdict set + the presentation-1 row (engine-1's decision-input child) + st-4's absorption pointer: D-148. Detail: worklog iter-111 + git.

### iter-110 · intake-11 donor routing — done (doc-only, the owner's call)

The pressure-city donor blueprint ADOPTED as parked material + the pack-4 row (the lost-city fold world-2 L2's cheap adoption): D-147. Detail: worklog iter-110 + git.

### iter-109 · phase-6 opening — done (doc-only, the owner's call)

PACK_SPEC written, the ref-18/ref-20 economy dives, the gut-check verdict NO CUTS, the second-setting shape pinned TRAVEL: D-146 + phases.md §6. Detail: worklog iter-109 + git.

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

### Phase-6 backlog (OPENED iter-109, CLOSED iter-116 — gate PASS, D-151;
drafted from phases.md §6; every row below DONE — the landing detail: the
ledger above + the D-rows + phases.md §6 + git)

- `world-2` · the phase-6 gate's own instrument — **DONE: the two-level
  gate COMPLETE.** L1 the reskin day (iter-112, D-149 — `content/road_pack/`
  the TRAVEL-loop reskin, 14m24s, ZERO core edits, the exit criterion MET
  BY MEASUREMENT; gate PASS iter-116, D-151, ROADMAP §2 CLOSED). L2 the
  deep second world — DELIVERED at the measured band (iter-139, D-172, the
  material iter-137's depth audit, D-170): the anti-collection half
  MEASURED (one ordinary verb composes through three systems into
  irreversible, divergent, route-stable state), the anti-reskin half
  MEASURED (the reskin day vs the weeks-authored province), the depth's
  DISTRIBUTION the recorded residue. The wave plan's four slices all DONE
  (skeleton iter-118/D-153, cultures iter-119/D-154, triangle
  iter-135/D-168, calendar iter-136/D-169). World-2 NEVER reopens for
  slices — the residue routes to the content-side rows. Detail: phases.md
  §6 (the slice blocks + the verdict) + D-149/D-151/D-170/D-172 + git.
- `res-1` · the resource/economy layer — done (iter-146, D-179): the
  substrate landed per its contract (CONTRACTS §2, collapsed to a pointer);
  UNARMED on the committed packs (zero corpus price). Detail: the ledger +
  D-179 + git.
- `roads-1` · the generated-exits pass — done (iter-145, D-178): the roads
  pass + the ONE shared exits read; the committed packs armed k=0. Detail:
  the ledger + D-178 + git.
- `pack-ci` · the admission-lint rungs — done (iter-117, D-152): the
  teleology gate + the live-char crosswalk + the price-marker lint LIVE in
  `core/pack.py` (PACK_SPEC §5/§6 the single reading owner). `qa-1`/`ci-1`
  stay the standing owner-gated rows.
- `since-1` · the re-encounter delta — done (iter-147, D-180): the
  encounter-epoch fold read-side, unarmed. Detail: the ledger + D-180 +
  git.

> Opening-day questions — ANSWERED iter-109 (D-146): the gut-check NO CUTS
> (the ablation + named-consumer evidence); the second-setting shape
> TRAVEL. The questions are closed; a future shape change is a new owner
> call. W3 closed without new rows (the calendar binding maclock-1's own,
> D-116; intake-8's setting sketch rode world-2's L2 half, D-130).

### iter-108 · fixations — done

The three law rows D-142/D-143/D-144 (folded into the D-145 family row at the phase-6 gate) + the digest (`scripts/digest.py` + `tests/test_digest.py`, D-145); 1660+1 green (+8). Detail: worklog iter-108 + git.

### iter-107 · riders — done

The five risk-synthesis riders: the blast-radius drift contract (test_drift.py), pack-scaffold + pack-doctor, cause_hook + payoff_latencies + beat_tension_profile + the --systems-minus ablation, the nearest-valid re-ask menu, §8.5's per-component latency columns (D-140/D-141); 1652+1 green (+41). Detail: worklog iter-107 + git.

### iter-106 · resume — done

The resume door — `core/cursor.py`, `Simulator.resume`, `--resume`, test_resume.py +19; the INVISIBLE-TO-THE-LOG law (T1 across process boundaries): D-139; 1611+1 green. Detail: worklog iter-106 + git.

### iter-105 · cli-pack — done

The CLI `--pack` flag (periphery only, test_cli.py +3) + the two verdict rows D-137/D-138; 1592+1 green. Detail: worklog iter-105 + git.

### iter-104 · owner-called fork analysis — done (doc-only)

The combined-variant routing: cli-pack pinned iter-105, the roads-1 read-path fork + the world-2 toponym question resolved under the ONE override-else-derived law family (D-132), since-1 routed to phase 6. Detail: worklog iter-104 + git.

### iter-103 · owner-called phase-6 plan audit — done (doc-only)

Verdict: COHERENT — the phase-6 opening stands on solid ground; four detail findings routed (the st-5 pointer, the CLI --pack flag, the roads-1 fork, the name-1 toponym question). Detail: worklog iter-103 + git.

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

- `since-1` · the re-encounter delta — the row MOVED to the phase-6
  backlog above (iter-104 routed it INTO phase 6: world-2's
  condensing travelers the first real consumer); the standing
  detail: a per-entity line family on the brief's entity cards
  (BRIEF_SPEC §3.4's extension) + the scene card, derived at assemble
  time from the fold (status-axis deltas, position/membership transfers,
  relation flips since the last co-presence tick) and the knower's own
  records (what they heard) — the world-simulated half already runs
  (macro ticks, urgencies, rotations); this row renders it on
  re-encounter. Zero canon writes, zero streams, zero corpus price by
  construction (read-side); the pack declares the line vocabulary. The
  source text's pattern #16, its own single-highest-value pick; the
  tavern pack's re-encounter surface is too thin to author the line
  vocabulary against (the leave/return pair + static NPC placement,
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
- `packtaxonomy` · material-derived props — absorbed (iter-152 audit,
  the owner's call; no consumer): the five packs author props directly,
  the closed read grammar is PACK_SPEC §8 (live), the inheritance chain
  a pre-placed growth rung (PACK_SPEC §10 — its own trigger, never
  armed). Detail: PACK_SPEC §8/§10.
- `story-critical objects` · the pack flag + a release path — absorbed
  (iter-152 audit, the owner's call; no consumer): the landed law is
  event-level (`importance.story_critical_events`, tune-1, D-045(b)/
  D-059 — `core/intent.py`); object importance rides the event/hook
  family (the pawn-ticket precedent). Detail: `core/intent.py` + the
  packs' `rules.json`.

### Research intakes 2/3 — routed, collapsed at the phase-5→6 gate

- `intake-2` (iter-66a) — the depth-architecture review; D-096 records
  the corrections + the routing. Verdict set: D-096.
- `intake-3` (iter-71) — the vision-vs-repo cross-review; the two
  confirmed holes routed (weather-1, companion-1). Detail: D-119's
  family + git.
- `weather-1` · done (iter-98, D-133). Detail: tests/test_weather.py +
  phases.md §5.
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

- The two owner-gated rows (`engine-1`, `parse-2`) moved to **Standing
  rows** above. The phase-2 grammar itself: gate-PASSED (iter-35, D-064) —
  the boundary stays closed until a named consumer opens it.

### iter-26 · phase-1 gate — done (verdict: PASS, D-058)

Full ROADMAP §5 protocol re-run: 109 live beats / 0 canon violations /
corpus 105 green; DECISIONS collapsed 41→30; `doc-1` closed clean;
phase 2 unlocked. Detail: worklog iter-26 + `docs/DECISIONS.md` D-058.

### Phase-1 tuning backlog (post-assembler, owner-gated)

- The one owner-gated row (`tune-3`) moved to **Standing rows** above.
  (tune-1 done iter-27, tune-2 done iter-28 — see Done.)

### Stress-test backlog (iter-11b resolutions; owner-gated)

- The owner-gated rows moved to **Standing rows** above: `st-2`, `st-5`,
  `presentation-1` (absorbing `st-4`). `st-3` groups & simulation LOD —
  done via depth-7 (iter-93, D-127; the GROUP_SPEC sketch absorbed — the
  mechanism owners phases.md §5 + `core/groups.py` + tests/test_groups.py).

### Spatial backlog (owner-gated; audited iter-19)

- `st-6` spatial vocabulary — done: (a) `travel` as a separate action
  (iter-97, D-132 — the movement twin with an edge price, `core/travel.py`;
  tests/test_travel.py); (b) `layout` (iter-20, D-057/KI#48 —
  canon-from-birth on the scene line via `scene_line_fields`, mutable decor
  stays texture).

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

- Moved to **Standing rows** above (the D-055 deferral; never blocks
  track A).

## Infra backlog (pick by need)

- `mech-1` · the mechanics introspection CLI — done (iter-84, D-118): `scripts/mechanics.py` matrix/trace/why/blast (the shadow-replay law: the PUBLIC pipeline only); 11 pins in tests/test_mechanics.py. Detail: D-118.
- `mech-1` · the mechanics introspection CLI — done (iter-84, D-118):
  `scripts/mechanics.py` matrix/trace/why/blast; 11 pins in
  tests/test_mechanics.py. Detail: D-118.
- `engine-2` · the urgency-roll stream split — done (iter-50, D-079).
  Detail: D-079.
- `ci-1` GitHub Actions — done (iter-143, D-176): pytest + ruff on
  push/PR to `main` (PYTHONHASHSEED=0, Python 3.12.14 the env pin);
  branch protection the owner's settings step (the recipe in the iter-143
  stop-point report). Detail: the ledger + D-176.
- `perf-1` 10k-tick timing profile — done iter-30: ~9.8k events/s
  write-side, event-linear; the numbers owner TECH_NOTES §8.
- `balance-1` 1000-headless-sim distribution harness — done iter-6:
  `scripts/balance_harness.py`; the harness contract TEST_PLAN §6. KI#4
  closed.
- `doc-1` VISION freeze review — done iter-26 (the phase-1 gate's
  doc-actualization sweep).
- `doc-2` REFERENCES quarterly — the recurring row → **Standing rows**
  above.
- `pack-1` Grim tavern pack — done (iter-148, D-181): the fourth committed
  pack; the consent split's lint the only engine-side touch. Detail: the
  ledger + D-181 + the pack's own notes.
- `pack-2` Arson-on-ashes guard — done iter-29 (D-061): the
  `spot_available` door check — the door-outcome vocabulary's fourth axis.
- `pack-3` Sci-Fi setting candidate — → **Standing rows** above (rewritten
  iter-150).
- `pack-4` Pressure-city pack — done (iter-149, D-182 — the T1 slice):
  zero core change held exactly; the post-T1 rows the future slices'
  material. Detail: the ledger + D-182 + the pack's own notes.
- `ref-N` Reference deep dives — the plan table and the per-file index
  live in `docs/REFERENCES_DEEP.md` §1/§2 (single owner). All
  ref-1..ref-13 done; ref-16 (agent-memory-atlas, owner-supplied) absorbed
  inside iter-8a, no solo iteration; ref-17 (DF designed experience)
  done (iter-8d).
- Candidates (owner-request only — D-022 law: no doc pass without a fresh
  owner request; both synthesis-only today, cited via the blueprint donor
  stacks + `docs/REFERENCES.md`): `ref-14` The Sims (proprietary;
  patterns-from-papers only, D-015); `ref-15` Prom Week (academic paper +
  GDC talk; no code repo).

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

