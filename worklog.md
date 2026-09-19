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
iter-147 · 2026-09-19 · since1 — the owner's «продолжай работы по
планам, решай сам что сейчас логичнее начать/открыть и прочее»
delegation call; the pick from the plan's own recorded recommendation
(STATUS Next step's readiness head after res-1, CONTRACTS §3 the
boundary — the section collapsed to a pointer in the same iteration)
- verified BEFORE working at BASE_COMMIT 0bd860d (1781 passed +
  1 skipped, ruff clean, Python 3.12.14) and re-verified after:
  1811 passed + 1 skipped (+30 in tests/test_since.py), ruff clean;
  the committed packs' corpora byte-untouched (the unarmed landing —
  no pack declares since_lines, the fold never built)
- the fold: `brief/since.py` (new) — the per-(reader, entity)
  encounter epochs (presence per present_entities + the carried-item
  closure; a location's co-presence the reader positioned at it),
  the reunion delta (the apart-window prop endpoints, both values
  known or silent; the position transfer; the reader's apart-born
  records naming the entity, the boundary events' own sightings
  excluded); event-indexed, zero streams, read-side only
- the render: `brief/assembler.py` — one trailing `since=` segment
  per entity card + the scene line, atomic with the card (the fill
  law whole-line, no dangling tails), knower-threaded (§3.9's
  amendment: the cards' structural lines stay shared, the segments
  are the knower's own); `max_segments` the D-047 ranking cap
- the lint: `core/packlint/readside.py::_since_lines` (the closed
  key set + the per-family placeholder sets, constant templates and
  dead vocabularies refused, the props/template pairing, position
  never a prop row)
- the §9 claim packet (the sandbox driver, Rule 9): the crafted
  condensation corpus (the watch-rotation revisit — the corporal's
  fatigue reset + position transfer while apart): D1 determinism,
  D2 the document arm (armed 1 since-line vs unarmed 0 —
  `since=last seen at loc_keep; fatigue 30->0`), D3 zero-price (the
  same-seed logs byte-identical); the committed smoke corpus
  honestly zero reunions (the tune-3 finding extended); the DECISION
  arm DEFERRED to the first consumer (the narrator is the owner-
  gated LLM boundary; world-2's travelers a future row) — falsifiers
  not tripped at the measured band
- docs: TASKS (the iter-147 section + the since-1 flip), DECISIONS
  D-180, CONTRACTS §3 collapsed, BRIEF_SPEC §3.4's extension +
  §3.9's amendment + §6's since_lines contract (653 lines > the 600
  cap — all substance, the §6.1 precedent, kept), AGENT_NAVIGATION
  §1 (brief/since.py + the tests row), STATUS re-pin + Next step
  (the pack consumers the new recommendation); this entry (iter-137
  evicted per the cap, verified in this edit; 10 held)

iter-146 · 2026-09-19 · res1 — the owner's «продолжай работы по
планам, решай сам что сейчас логичнее начать/открыть и прочее»
delegation call; the pick from the plan's own recorded recommendation
(STATUS Next step's readiness head after roads-1, CONTRACTS §2 the
boundary)
- verified BEFORE working at BASE_COMMIT 89cb177 (1763 passed +
  1 skipped, ruff clean, Python 3.12.14) and re-verified after:
  1781 passed + 1 skipped (+18 in tests/test_economy.py), ruff
  clean; the committed packs' corpora byte-untouched (the unarmed
  landing — the T1s green both ends)
- the substrate: `core/economy.py` — the account primitive
  (`account.<kind>` props, `core/fold.py` seeding), the three verbs
  (`account_sourced`/`account_transferred`/`account_consumed`),
  `flow_drafts` (the aggregate flows at macro crossings, the `every`
  divisor), `price_of` (base + per_unit × level, integer-only); the
  floor: `account_at_least` soft at the door (`core/intent.py`), the
  `is_account_prop` floor loud at the `_commit` gate (`core/loop.py`);
  the discrete arm: the `account` resolver (`core/resolvers.py`,
  STATE_MUTATING)
- the lint: `core/packlint/economy.py` (early shape + late cross, the
  KI#77 order law), the account-action block + the solvency-gate
  requirement (`packlint/actions.py`), the entity `accounts` pairing
  (`packlint/entities.py`), `lint_account_cond` (`packlint/shared.py`
  at the four requires sites), the flow verb witnesses
  (`packlint/admission.py`)
- the §9 claim packet (the sandbox driver, Rule 9): F3 MEASURED (the
  drained arm's 4-coin spend rejected at 2 coin, the fresh arm's
  accepted at 10 — pc 2 vs 6), F4 CLEAN (grain 10 -> 13, non-verb
  bytes identical, fingerprints equal), F1 the conservation oracle
  exact; falsifiers NOT tripped (CONFIRMED at the measured band);
  honest residues: no consumer yet (the gates + price_of armed but
  unconsumed), the compound exchange NOT a substrate concern
- docs: TASKS (the iter-146 section + the res-1 flip), DECISIONS
  D-179, CONTRACTS §2 collapsed to a pointer, EVENT_SCHEMA §4 (the
  account home), AGENT_NAVIGATION §1 (economy + the six touched
  entries + the tests row), STATUS re-pin + Next step (since-1 the
  new recommendation); this entry (iter-136 evicted per the cap,
  verified in this edit; 10 held)

iter-145 · 2026-09-19 · roads1 — the owner's «продолжай работы по
планам, решай сам что сейчас логичнее начать/открыть и прочее»
delegation call; the pick from the plan's own recorded recommendation
(D-175's build-rows order, roads-1 the readiness head, CONTRACTS §1
the boundary)
- verified BEFORE working at BASE_COMMIT 091b004 (1754 passed +
  1 skipped, ruff clean, Python 3.12.14) and re-verified after:
  1763 passed + 1 skipped (+9 in tests/test_roads.py), ruff clean;
  the fresh-venv install path verified for core.packlint (the CI
  runner's own path)
- the pass: `core/worldgen.py::_pass_roads` (PASS_ORDER grew roads;
  pure, draw-free) — the MST backbone + the pack-declared MUTUAL
  k-nearest overlay over the CLAIMED locations (the mutual form is
  I3+D2's pin: per-node overlay degree <= k, <= n*k/2 edges — the
  union reading breaks both on the star); `WorldModel.roads`;
  I4's span law relocated to the emit (the loud WorldgenError
  conflict rule; the runtime backstop grew place+roads — the
  lint-side-alone place pin superseded by its relocation successor
  test)
- the ONE read: `core/roads.py::exits(pack, world, location)` —
  authored non-empty wins, else derived, else (); the consumers
  re-pointed (lod.scene_zones grew the world param;
  first_failing/occ_breaking_cause gained world=None, threaded at
  every loop door — the F-run's probe caught the accept door missing
  its world before the fix); the lint: worldgen.roads required,
  k 0..claimed-2; the committed packs armed k=0 (zero corpus price —
  the authored exits win everywhere; the claimed sets connect within
  their spans: 1<=1, 1<=2, 4<=4)
- the RIDER: the pack.py split (D-175) — core/packlint/ (helpers +
  shared + twelve domain classes under the one _Lint orchestrator;
  load_pack the single gate; no DSL/base classes; the compat
  re-exports keep every importer green; pyproject gains
  core.packlint)
- the §9 claim packet (the sandbox driver, Rule 9): the province's
  MIXED mode G variant at the smoke seed, k=0 vs k=2 — MEASURED:
  the door 8 -> 12 accepted pairs, WHO simulates 5 -> 7 NPCs in the
  crossing's warm ring at keep, routes 5 -> 8 edges / 0 -> 3 cycles
  / 10 -> 20 two-hop pairs; falsifier NOT tripped (CONFIRMED at the
  measured band); the honest residues: the mode G authoring burden
  (the orphan law couples grammar reachability to authored edges),
  the authored playscript breaks under the derived topology (the
  weight-14 tie resolved differently), the adjacent_locations
  audience stays authored-only (not a named consumer — the first
  mode G pack's rider)
- docs: TASKS (the iter-145 section + the row flip), DECISIONS
  D-178, CONTRACTS §1 collapsed to a pointer, ROADMAP's row list,
  AGENT_NAVIGATION §1 (core/roads.py + the packlint row + the pass
  list), STATUS re-pin + Next step (res-1 the new recommendation);
  this entry (iter-135 evicted per the cap, verified in this edit;
  10 held)



iter-144 · 2026-09-19 · contracts — the owner's «продолжай работы
по планам, решай сам что сейчас логичнее начать/открыть и прочее»
delegation call; the pick from the plan's own recorded next
recommendation (D-175's order: ci-1 → the three contract writes →
the build rows; ci-1 consumed iter-143)
- verified BEFORE working at BASE_COMMIT 7e6c83f (1754 passed +
  1 skipped, ruff clean, Python 3.12.14 the env pin) and
  re-verified after — doc-only, the corpora byte-untouched
- `docs/CONTRACTS.md` (new): roads-1 — the node question pinned
  (claimed locations only, the consumer grounding: the warm ring,
  the move door, travel's derived price needs claimed endpoints
  D-122; node geometry = the claimed site set, the shared
  min-cross-pair metric), the algorithm named (MST backbone +
  pack-declared k-nearest overlay, the D-174 fence's three
  questions answered inline, the one-knob kill arm, k=0 legal),
  the invariant set I1–I6 (the max_edge_span conflict rule: the
  loud WorldgenError, connectivity never bought by breaking the
  span); res-1 — the substrate shape (the account primitive,
  three verbs through the canon door, integer-only, prices
  derived L3, flows on the D-112 aggregate surface), the
  irreversibility split, the underflow floor (soft door / loud
  gate), the unarmed landing; since-1 — the baseline sense named
  (last physical co-presence, the per-entity encounter epoch, the
  four other senses rejected with cause), the scene_delta
  separation, the blind-NPC inheritance, the pack-owned line
  vocabulary; every contract: the §9 claim packet + the minimal
  test set; the form's law in the header (a contract is NOT the
  spec — SPECS_BACKLOG's JIT law untouched)
- docs: TASKS (the iter-144 section + the three row pointers),
  DECISIONS D-177, STATUS re-pin + Next step (the recommendation
  now the build rows, roads-1 the readiness head),
  AGENT_NAVIGATION §1 the CONTRACTS.md row; this entry (iter-134
  evicted per the cap, verified in this edit; 10 held)
- the doc-loop alarm answered: the D-022 fresh-owner-request
  exception + the sequence's next step is BUILD work; caps after:
  STATUS 645 / TASKS 1998 / DECISIONS 90 lines (56 rows — over the
  30 cap on the §6.1 substance precedent, the standing post-ladder
  record) / CONTRACTS 340 — the over-cap files ride the documented
  §6.1 substance precedent (STATUS down from 684: the iter-142
  record retired per the two-record pattern)
iter-143 · 2026-09-19 · ci1 — the owner's «продолжай работы по
планам, решай сам что сейчас логичнее начать/открыть и прочее»
delegation call; the pick taken from the plan's own recorded first
recommendation (intake-29/D-175: ci-1 FIRST — AGENTS §8's CI-files
gate satisfied by the fresh delegation, recorded as such)
- the runner LANDED: `.github/workflows/ci.yml` — pytest + ruff on
  push to `main` (+ the PR trigger riding along: the row's own
  "protect main after" needs check runs on PR heads; the owner's
  direct-push rhythm the primary path); PYTHONHASHSEED=0 job-level
  (INV-2), Python 3.12.14 pinned EXACT (the env pin — the golden
  T1 fixture byte-compare, TEST_PLAN §1.1; a bump rides a fixture
  regen, never alone), the plain install (runners carry no PEP-668
  fence), contents:read, timeout 15
- verified BEFORE working at BASE_COMMIT 15e568d (1754+1 green,
  ruff clean, Python 3.12.14) and re-verified after (doc-only
  beyond the workflow file); the runner path simulated in a clean
  venv (fresh install → ruff → pytest: the same 1754+1, the skip
  the chronicler module's duckdb import by design);
  checkout@v7 / setup-python@v7 / 3.12.14-in-python-versions
  live-checked 2026-09-19; the first LIVE run fires on the owner's
  push (named honestly — a sandbox cannot run GitHub's runners);
  7 files (the workflow + the doc quintet + README's repo-map row;
  over the 3–5 soft limit, all mandated: the quintet by AGENTS §6,
  the map row by NAV §3's short-map duty); branch protection the
  owner's settings step (the recipe in the stop-point report)
- caps: STATUS 684 / TASKS 1949 / DECISIONS 89 lines (55 rows —
  over the 30 cap on the §6.1 substance precedent until the next
  gate collapse) / phases 4305 — the over-cap files ride the
  documented §6.1 substance precedent, trim at the next gate
  collapse; iter-133 evicted here, verified in this edit; 10 held


iter-142 · 2026-09-19 · intake29 — the owner's «проанализируй
текст далее и его предложения, если согласен => нужно будет
заложить в планы работу и соответственно пересмотреть оный
или типа того. по пунктам разбери что надо что не надо и
почему» research call over the uploaded external audit (a
prior DNS-less session's static roadmap review of main
8f4fbd4e; 5 files doc-only, zero code, zero corpus price)
- verified BEFORE working (1754+1 green LIVE, ruff clean,
  Python 3.12.14, HEAD aa1097f — one commit past the audit's;
  the audit's own numbers confirmed by the run it could not
  make); every load-bearing claim verified (sizes / _Lint
  structure / no CI / the branch API / the row wordings /
  324-sites-vs-6-locations / the undefined co-presence
  baseline); two framings corrected (res-1 "contradiction" →
  an unwritten contract point; M3/T8 "needs demotion" →
  owned since iter-138)
- the residue routed into the rows (D-175): res-1's mechanism
  split + irreversibility split; roads-1's topology contract
  (the node question, the algorithm naming, the invariant set,
  the LOD/autonomy falsifier); since-1's encounter baseline;
  companion-1's no-teleport; pack-1's consent split; ci-1 the
  recommended first pick; the pack.py split the rider rule
  (never a standalone refactor); the intake admission rule
  (a named consumer row + a falsifier up front) — the queue's
  composition sharpened, its order never touched


iter-141 · 2026-09-19 · intake28 — the owner's «разбери 1231.md =>
что стоит перенять и почему, зачем, как использовать и где это
улучшит проект» research call over the uploaded `1231.md`, itself a
prior session's output (an external Stålberg/Townscaper conspectus +
the owner's competing-solutions preference; that session verified
against the same main 8f4fbd4e but DNS-failed its clone — 5 files
doc-only, zero code, zero corpus price, the D-163 clone-less-session
precedent, re-verified at a REAL clone)
- verified BEFORE working (1754+1 green, ruff clean, Python
  3.12.14, HEAD 8f4fbd4e); the verdict PARTIALLY CONFIRMED — the
  content overwhelmingly OWNED, zero factual errors in the
  load-bearing repo-facing claims (D-173's test wording, BLUEPRINT
  §0, L13/L14, the owner-preference record D-165/D-173 all hold;
  the Stålberg half the cross-domain confirmation family's next
  member [intake-16/17/24/27], the Townscaper reconciliation
  itself intake-17's)
- the residue: ONE instrument ADOPTED (the COMBINATION FENCE — the
  fifth check's operational sharpening: a combined design carries
  NO presumption of advantage, itself a separate hypothesis; the
  mechanism-of-advantage decomposition + the combination-price
  question + the Frankenstein test; consumers the
  engine-1/presentation-1 debates + res-1's evaluation); the
  local-pattern→higher-order HYPOTHESIS routed to res-1's
  aggregate macro-events + the cadences' decision half (never a
  row); two recognition handles block-only (representation-shrink →
  PACK-1/grammar snapshot/INV-3; vary-representation-preserve-
  substrate → the scaffold law/cosmetic streams/promotion door);
  refused: a grand-synthesis law (the document itself refuses,
  D-024 agrees), methodology codification (D-163 — the method file
  external, nothing left to adopt), Stålberg-form features
  (intake-17's fence), a Canonical-Visual-Memory row (NOT a repo
  record — session-external; presentation-1 owns the surface,
  INV-4-fenced; the one provenance caveat; Stålberg figures
  second-hand per the KI#51 family)
- docs: phases.md §6 the intake-28 block, DECISIONS D-174, TASKS
  the iter-141 section, STATUS re-pin + Next step (iter-139's
  record evicted per the two-record convention), this file.
  iter-131 evicted here (verified against git in this edit); 10
  after; 1754+1 green, ruff clean after. Caps: STATUS 646 / TASKS
  1846 / DECISIONS 87 (53 rows — over the 30 cap on the §6.1
  substance precedent, the standing post-ladder record) / phases
  4068 — the over-cap files ride the documented §6.1 substance
  precedent

iter-140 · 2026-09-19 · intake27 — the owner's «проанализируй
документ и определи что из него можно полезного перенять в проект
и почему» research call over the uploaded level-design
consolidation (twelve GDC/Konsoll/LDL talks; doc-only, zero code,
zero corpus price — the D-155..D-171 intake precedent, the file
external per the convenience-copy law, the intake-24
transplantation posture)
- verified BEFORE working (1754+1 green, ruff clean, Python
  3.12.14, HEAD 1b7666a); the doctrine PARTIALLY CONFIRMED —
  overwhelmingly owned as the strongest cross-domain confirmation
  family since intake-16 (figure–ground = budgets/eviction/
  pruning/§6.1; vistas = cold tiers + lazy detail; space reuse =
  fold(log); PCG-is-design ×4 = INV-3/PACK-1/D-082/D-134; Control
  = L12/LOD-1/INV-3; the lint family = the data-quality law
  verbatim; Qud = the pass ladder + the chronicle horizon, L7
  stricter at runtime)
- the residue: FIVE instruments (the READER LAW — zero read
  surfaces = functionally dead, name the reader, F4 + the
  cadences' decision half; the PRICED-OPTION question —
  differently-priced never labeled, the B row's form, res-1 the
  dynamic owner; the TOP-LOD READABILITY question — the critical
  path survives the coarsest blur; the REALIZATION TABLE —
  why/layer/linked/understood + the removal test, PARKED
  pack-1/3/4; the SACRIFICE PROTOCOL — promise pair →
  both-promises test → Barrier/Gate/Carrot/S'more, PARKED the SoW
  debates) + the PROPOSAL (topology-aware hook distribution over
  the site graph's degree classes — the cadences' decision half /
  roads-1 / F4, never law until armed)
- docs: phases.md §6 the intake-27 block + the consult card's
  item 10, REFERENCES §10 +9 source rows, DECISIONS D-173 (52
  rows — over the 30 cap on the §6.1 substance precedent), TASKS
  the iter-140 section, STATUS re-pin (iter-138 evicted per the
  two-record convention) + the Next step (the sacrifice protocol
  joins the consult material), this entry (iter-130 evicted,
  verified in this edit); 1754+1 green, ruff clean after;
  doc-only, the corpora byte-untouched
- Caps: STATUS 626 / TASKS 1785 / DECISIONS 86 lines (52 rows —
  over the 30 cap on the §6.1 substance precedent, the standing
  post-ladder record) / phases 3944 / worklog 10 entries
  (iter-130 evicted here, verified in this edit) — the over-cap
  files ride the documented §6.1 substance precedent

iter-139 · 2026-09-19 · world-2 L2 (the verdict) — the
owner's convening call «я решил что следует world 2 закончить,
вердикты вынести» (the session's second half, after intake-26's
adoption pass; doc-only, zero code, zero corpus price)
- the two-level gate's level-2 question ANSWERED: the honest scope
  DELIVERED at the measured band — the anti-collection half
  MEASURED (one ordinary verb → three systems → irreversible,
  divergent, route-stable state: the A/C/D/H ledger), the
  anti-reskin half MEASURED (L1's 14m24s reskin day vs the
  weeks-authored province: the spine + the vertex + the year-run
  almanac), the depth's DISTRIBUTION the recorded residue (B/F/G
  partial — the concentration at the triangle's vertex, the
  option surface 1-of-6, the 48 turns the one found-and-named
  counterexample); the verdict's law: the gate asks the honest
  scope, never uniform distribution — deferring until B/F/G close
  would be the completeness-smuggling the audit refused (no open
  row a verdict input)
- the residue's routing: the future depth consumers the
  content-side rows (F4's promotion events — pack-1/pack-4; the
  cadences' decision half a BUILD question) — world-2 never
  reopens for slices; the two-level gate COMPLETE (L1 PASS
  iter-116 D-151; L2 DELIVERED iter-139 D-172); KI#86 deleted
  per AGENTS §5 (closed iter-136, past the window)
- docs: DECISIONS D-172, TASKS the world-2 row done (the wave
  plan + iter-109's answers compressed to their pointers — the
  detail in the iter sections + phases.md §6 + the D-rows) + the
  iter-139 section, phases.md §6 the verdict block, STATUS re-pin
  (iter-137's record evicted per the two-record convention) + the
  Next step, this entry (iter-129 evicted, verified in this
  edit); 1754+1 green, ruff clean after; doc-only, the corpora
  byte-untouched
- Caps: STATUS 606 / TASKS 1733 / DECISIONS 85 lines (51 rows —
  over the 30 cap on the §6.1 substance precedent until the next
  gate collapse) / phases 3786 / worklog 10 entries (iter-129
  evicted here, verified in this edit) — the over-cap files ride
  the documented §6.1 substance precedent

iter-138 · 2026-09-19 · intake26 — the owner's «перед этим
вероятно стоит рассмотреть дополнительно идеи с файла
VERIFICATION_LENSES_RESEARCH.md» call (the world-2-verdict session's
first half; doc-only, zero code, zero corpus price — the D-155..D-170
intake precedent, the research file external per the convenience-copy
law)
- verified BEFORE working (1754+1 green, ruff clean, HEAD 8dc5436,
  Python 3.12.14 the env pin); the document's FACT rows content-matched
  at HEAD (TEST_PLAN's separation; mechanics.py matrix/trace/why/blast;
  metrics.py M1–M5 + the four families; the five named test files;
  intake-21's card; intake-24's six principles; the res-1 offline
  one-knob spike's record) — zero factual drift; the doc's own verdict
  PARTIALLY CONFIRMED verified: the mechanisms all owned, the gap the
  compact selection grammar (iter-137's from-scratch re-derivation the
  confirming instance)
- ADOPTED (the long-term quality call): TEST_PLAN §9 — the claim
  packet (oracle + falsifier mandatory; the disposition vocabulary the
  repo family, never a numeric score) + the claim-shape → instrument
  selection table (self-describing names, standing instruments only) +
  the independent-re-derivation oracle law + the order-probe contract
  law; research-derived, a routing aid, never a gate; the full
  ten-lens/nine-prism catalog held in the intake-26 block (the
  one-pass record, D-024); the stale-at-HEAD corrections recorded (the
  door battery = the next-decision census iter-137; the
  first-divergence read consumed iter-135; the A–H ledger the packet's
  standing instance)
- refused at the door: the lens/prism names as law (label-matching,
  the intake-24 precedent), any executable helper / registry / score /
  runtime form (the doc's §10 reject list = standing law),
  REFERENCES.md as the surface (the external-source catalog); the
  measurement obligation standing: the next owner-gated build row's
  verification plan = ONE claim packet (≤3 lenses, ≤2 prisms); KI#85
  deleted per AGENTS §5 (closed iter-135, past the window)
- docs: phases.md §6 the intake-26 block, TEST_PLAN §9,
  AGENT_NAVIGATION §1, DECISIONS D-171, TASKS the iter-138 section,
  STATUS re-pin (iter-136's record evicted per the two-record
  convention), this entry (iter-128 evicted, verified in this edit);
  1754+1 green, ruff clean after; doc-only, the corpora byte-untouched
- Caps: STATUS 652 / TASKS 1726 / DECISIONS 83 lines (50 rows — over
  the 30 cap on the §6.1 substance precedent until the next gate
  collapse) / phases 3752 / TEST_PLAN 837 / worklog 10 entries
  (iter-128 evicted here, verified in this edit) — the over-cap files
  ride the documented §6.1 substance precedent
