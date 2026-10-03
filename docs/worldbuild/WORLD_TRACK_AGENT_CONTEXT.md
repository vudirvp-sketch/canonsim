# World Track — Agent Context (the durable compact surface)

> What an agent needs repeatedly when working the world track: identity,
> non-negotiable rules, boundaries, proven substrate, evidence conclusions,
> open hypotheses, deferred mechanisms, the current stage/gate, navigation,
> anti-patterns. Bootstrap source: `WORLD_TRACK_NEXT_v4_AGENT_PACK_v4.5`
> (external navigation bundle, ingested iter-277; superseded as the newest
> bundle form by `CANONSIM_AGENT_WORLD_SUITE_v1_0` — CORE_WORLD v1.3 +
> WORLD_TRACK v4.6 — ingested iter-311, its world half verified byte-
> equivalent to v4.5 beyond the sync notes) — both preserved verbatim as
> historical evidence in `archive/`, never re-ingested wholesale. This file
> supersedes the packs as the durable surface; the repository's owner
> documents remain authoritative everywhere (D-024: this file navigates and
> reconciles, it never restates an owner). Update it only when the stage,
> a boundary, or an evidence verdict changes — never as a narrative log.

## 1. Identity

`canonsim` is a **deterministic living-world simulation core** (Python,
stdlib-first). It is a **story generator, not a storyteller**: history
emerges from rules, actors, constraints, resources, institutions,
knowledge and residue — no hidden runtime plot, no drama manager, no LLM
game master. The world must stay capable of running, changing and
accumulating history **without a player and without an LLM** (the tavern
scenario already reads as a story with zero LLM involvement, INV-4's
envelope; `docs/VISION.md` the why).

The world track (`docs/worldbuild/`, D-186) owns the **authored setting
model and the causal-substrate experiments** — a separate track from the
engineering backlog, never a second queue: a world-authoring need for
engine capability routes to a `docs/TASKS.md` standing row on the owner's
call (the separate-track law). Quality gate (`WORLD_WORKPLAN.md` §13):
not "how much is described" but **how many different human histories can
honestly emerge from the same causal substrate**. First prove one living
region, then scale.

The project model (law, not aspiration — `AGENTS.md` §1/§4):

```text
SIMULATOR → CANON / CAUSALITY
LLM       → INTERFACE / INTERPRETATION
PLAYER    → CANONICAL ACTOR
WORLD     → AUTONOMOUS
NARRATIVE → READ-SIDE INTERPRETATION
```

## 2. Non-negotiable causal rules

- **INV-1 event sourcing** — state changes only via events; the JSONL log
  is the append-only truth; `core/log.py` the only canon-write path;
  SQLite a rebuildable index. Committed logs are never edited (INV-5).
- **INV-2 determinism** — one master seed, named streams via the RngBank,
  no wall-clock, `sorted()` iteration, fixed queue key
  `(tick, sub_order, actor_id)`, `PYTHONHASHSEED=0`; byte-identical replay
  per environment.
- **INV-3 content/code split** — no setting nouns in engine code; all
  setting data rides packs as JSON.
- **INV-4 the LLM/network boundary** — the network surface is exactly
  three sanctioned modules (`cli/engine.py`, `workbench/api/transport.py`,
  `workbench/platform/model_fetch.py`); everything else stays network-free
  and engine-agnostic; inference sits outside the canonical determinism
  envelope.
- **The doors** — all consequential change enters through intents resolved
  by the simulator under the same rules for every actor; world-impossible
  intents emit `intent_rejected` (attempts are facts); director/urgencies
  ride the INTENT door, reactions the COMMIT door.
- **Read-side purity** — render/brief rebuild deterministically from the
  log (the header seed re-mints the RngBank); read-side folds never feed
  entropy or channel inputs (L6/EPIST-1); a reader is never a truth test.
- **Epistemic boundary** — actors act on their own canonical state and
  knowledge; another entity's hidden state enters only through an
  observable marker that can become knowledge (the influence-boundary
  check: fix public surface, swap hidden other-state, require the same
  authorized result). No omniscient authoring.
- **Presentation may be richer than stored detail; causality may not.**
- **The runtime-promotion gate** — a new runtime primitive requires
  `REAL CONSUMER + REAL FAILURE + MATERIAL QUALITY GAP + NATIVE LIMIT +
  REPEATED SHAPE + FALSIFIER + OWNER + PHASE/GATE`. Until then: pack data,
  authoring vocabulary, test logic, or read-side representation — never a
  new canonical layer (D-018/D-031).

## 3. The canon / LLM / player boundary

| Role | May | Must not |
|---|---|---|
| Simulator | decide state, events, outcomes, relations, permissions, resources, knowledge consequences, residue, changed future conditions | — (it is the sole canon authority) |
| LLM | parse player language into structured intent; render canonical state/events into prose, dialogue, perception; non-causal descriptive texture | decide outcomes; invent canonical events or hidden state; override constraints; force NPC behaviour; retroactively alter history; invent unsupported causal motives |
| Player | an embodied canonical actor — language expresses intent; the simulator resolves the consequential result under the same world rules; entering/leaving/re-entering exposes genuine accumulated change | be an exception to the world rules; act as external author or god |

Narrative is a **read-side interpretation** of generated history. A
strong story opportunity is evidence the substrate exposes useful causal
material — never evidence that a plot subsystem is required. Prose
quality is never evidence that a world mechanism is causally live; a
narrative gain may ride along as a secondary signal, never as the causal
justification for admission.

## 4. The worldbuilding boundary

Worldbuilding defines **causal possibility and constraint** — what CAN
exist, happen and matter — never what must happen:

```text
WORLDBUILDING → WHAT CAN EXIST/HAPPEN/MATTER
→ SIMULATION   → WHAT ACTUALLY HAPPENS
→ LLM          → HOW IT IS PERCEIVED AND TOLD
```

It must not become a disguised quest, scene, plot or character-arc
script. The operating loop the track strengthens (`WORLD_AUTHORING.md`
§1/§6, the pack's §1):

```text
PRESSURE → ACCESS/CONTACT → INSTITUTION/PRACTICE → AGENCY
→ EVENT → KNOWLEDGE → RESIDUE → CONSUMER → NEXT-CYCLE CHANGE
```

Admission test for any candidate (`WORLD_AUTHORING.md` §18, the pack's
§8): what future state changes, which existing system consumes it, what
happens if removed, who/what carries the state, who knows it, what
residue persists. If the answer is only "the prose becomes better", the
item belongs to the read/render side, not the world track.

**Liveness law** (the v4 core, now evidenced): a world component is
causally live when a realized change reaches a real consumer that changes
later state, decisions, knowledge, resources, relations, permissions or
future options. Event existence is not causality. Locate where a path
dies with the A–H runtime loss vocabulary (A no pressure … G residue
without consumer, H complete path; `scripts/mechanics.py census` the
instrument). No consumer ⇒ surface/read-side — do not repair it with
prose or by inventing a scheduler.

## 5. Current proven substrate (measured)

The anchor is **Sarrow Vale** (`content/province_pack`; the owner's
second setting) — the strongest witness. Measured, at seed 42, as of
iter-276 (HEAD `55fd4a2`):

- **The causal mesh** — eight audited families (`ANCHOR_REGION.md` §5):
  fire → institutional response; feud residue → present politics;
  season → weather → social signal; route → condensation → culture;
  credit/debt; step/water-governance; winter kinship; camp/charcoal
  debt. Governed by the **disable test** (remove one unique driver; the
  others survive) and the **shared-stage rule** (shared driver + mediator
  = one mechanism counted once).
- **Five authored meso units** — the crossing household (§6.1), the step
  bench (§6.2), the winter kin (§6.3), the charcoal camp (§6.4), the
  market as a carrier assembly (§6.5). The W4 working set (the first
  four) is COMPLETE and closed.
- **The account/economy arm** — pure pack data over the account resolver:
  the crossing's flood debt to full lifecycle (debt-1 → floodpaper), the
  camp's paper as live state (charcoalpaper, freightvol), factor
  renegotiation (repricing), the fourth verb `settle` — the multi-leg
  transaction over explicit owners (settlement) — PRESENT/NOTCH account
  kinds (stepbench). Zero core debt primitives; anti-arbitrage spread
  preserved (D-191).
- **Reader surfaces that carry canon** — the rs-1..rs-12 family: account
  glosses, flow glosses, the runner's grudge causal row (rs-9), the
  shave's dated temporal chain (rs-10), the move line's night form
  (rs-11, iter-281: `phase.<id>`/`site.<prop>` condition keys + the
  symbol-indirected night arm), the account line's knows tail
  (rs-12, iter-281: `{knows? — {knows}}` on account_sourced — the
  witnessed row riding the line, rs-9's own shape) — read-side lines
  carrying pack-authored causal rows through the knows boundary,
  never new canon.
- **Composition** — one 2371-event run, 16 relational oracles, six
  interacting causal families crossing end-to-end, a calendar-year and
  macro-economic witness (D-237, `tests/test_p1_composition.py`).
- **Carrier/surface discrimination** — the three-move probe (reader
  audit → ablation → injection); the verdict is per-leg (D-239,
  `WORLD_TESTS.md` §7).
- **The I0 World Ignition Witness** (iter-276, `tests/test_ignition.py`)
  — the first world-liveness proof: one recurring moving meso (the
  camp's freight loop, three locations, three cycles), one route edge
  perturbed; the five-leg chain measured (exclusion → divergence →
  response → residue → changed next-cycle condition); the four timelines
  (people / material / knowledge / obligations) diverging, never forced
  to synchronize; the rejections mint no knowledge (epistemic silence).
  Verdict: **the substrate expresses the chain; no machinery promoted.**
- Suite state at the landing: 2520 passed + 9 skipped, ruff/docguard/
  topology clean (Python 3.12.14, the env pin); the smoke corpora
  byte-untouched through the whole W5 landing (zero corpus price).

## 6. Important evidence conclusions

The retained measurements that keep being needed (detail:
`WORLD_TESTS.md` §9 + `docs/blueprint/phases.md` §6):

- **D-237 (composition):** the substrate composes many families without
  a plot subsystem; losses concentrate in assignment/consequence
  boundaries, never the scheduler (census `A1·B3·C5·D1·E2·F0·G0·H10`).
- **D-238 (causal inertness):** removing all 52 calendar turns and five
  institutional events left the final projection byte-identical — event
  existence is not causal relevance; a world component needs a consumer,
  not a producer or a story line. The calendar line is surface-only BY
  CONSTRUCTION (measured twice). J-3 road-fear was REJECTED as a
  non-gap: LOD/decay makes the proposed threshold structurally
  unreachable — a density observation, not a missing urgency mechanic.
- **D-239 (carrier vs surface):** representation does not make an entity
  causal; causal status is earned by changed reachable futures; verdicts
  are per-leg, not per-institution.
- **D-240 (market embodiment):** the validated pattern is **carrier leg
  + explicit consumer + pack-only embodiment** — no core change was
  required; render contradiction is never a reason to mutate calendar
  canon.
- **D-236 (temporal contract):** the owner's pick `A2 + B2/B3`, with B1
  `generate-at-T` deferred behind its card's five conditions. The world
  track must not silently reopen this engine contract.
- **W5 human tests:** biography clean (iter-191); humor and heartbreak
  carried at the live band — every station bar met, the strict
  heartbreak pair carried, rs-9/rs-10 read in full (iter-270). The owner's
  residue dispositions (iter-266) are standing law: the fail-then-pass
  reading and the 40/80 asymmetry stay **closed as residue** (do not
  delete, do not explain by default — a surface is owed only on proof a
  reader needs it); the discovery surface (rs-9) and the temporal surface
  (rs-10) landed (iter-267/268).
- **Failure classification before repair** — never "improve the prose";
  a measured failure is first classified:
  `CANONICAL_GAP | DISCOVERY_PATH_GAP | RENDERING_GAP | CONTENT_GAP |
  SUBSTRATE_GAP | TEST_GAP | LIVENESS_GAP | ADMISSIBILITY_GAP`, and
  canonical fact / discovery path / rendering failure stay separated.

## 7. Open hypotheses (PROPOSAL — none is canon)

Status vocabulary is law (`WORLD_TESTS.md` §10):
`CONFIRMED / PARTIALLY CONFIRMED / REJECTED / UNRESOLVED / DEFERRED` —
plus `PROPOSAL` for candidates (`docs/worldbuild/README.md`). Everything
in this section is PROPOSAL unless an owner document promotes it.

- **The I0 substrate-limitation inventory** (iter-276; the only current
  machinery candidates): (a) no runtime route writer — an edge closure is
  not a world event; (b) the two-sided band condition — the gate
  vocabulary reads floors, never ceilings; (c) the response repertoire's
  floor — attempts only, no reroute/adaptation door. Each becomes
  machinery only after repetition with a real consumer, through the §2
  promotion gate.
- **Frontier synthesis candidates** (the pack's v4.3–v4.5 proposals,
  unpromoted): pool/role provenance + meaningful absence; expectation
  feedback (mismatch → evidence → interpretation → action → update);
  maintenance ecology (one narrow consumer-bearing instance, never a
  generic engine); functional corridor / dependency cut; the
  capacity/fracture law (route existence ≠ route capacity; the fracture
  oracle is queue/spillover/abandonment/scarcity/price-or-obligation
  change, never average utilization); synchronization latency / channel
  asymmetry (`BODY | CARGO | WITNESS | CLAIM` arrive independently).
  Probe contracts for each live in the archive (§10 below).
- **Admissibility / contact routing** — the chain region/regime →
  habitat → lineage/culture/institution → knowledge → mobility →
  pool; the boundary law "no unexplained provenance teleportation" (a
  rare crossing is lawful with a contact path that leaves residue);
  causal passports as authoring/test metadata, not runtime state.
- **Institutional reproduction / stateful cadence** — a repeated event
  is not yet an institution; a recurring cycle is causally meaningful
  only when it consumes history, names a real reader/decision that can
  differ, and (durable functions) names what survives carrier
  turnover. `time passed` is never sufficient causal attribution.
- **Relation formation as option-topology change** (D-196, routed):
  co-presence × reciprocity × selective disclosure → future-option
  change (ADD/REMOVE/MERGE/SPLIT/SEMANTIC-CHANGE), never a relationship
  score. First owner: the W5 heartbreak/winter-kin line.
- **The W6 hypothesis itself** — that the same canonical package
  supports materially different valid readings (the genre matrix).

## 8. Deferred mechanisms (named triggers only)

- **B1 `generate-at-T`** (D-236) — deferred behind the card's five
  reopening conditions; two audits found no promotion evidence.
- **The dormant civilizational regimes** — design memory, not a queue:
  maritime/pirate, deepwater, necropolis, sky enclave, closed-tech,
  refuge, ruin frontier (source owners: `CULTURES_CIVILIZATION.md`;
  cards with why-not-now/triggers/contradictions in the archive's
  `02_DORMANT_REGIMES.md`). Disposition vocabulary
  `PRESERVE | TRIGGERED | REJECTED | SUPERSEDED`; `DEFERRED` never means
  forgotten. Activation requires a new material pressure + institutional
  coupling + failure mode + human-history shape the anchor cannot
  discriminate — never map completion. **Mountain/industrial is the
  second-region candidate** (infrastructure/maintenance/succession), only
  after anchor proof, tied to a specific anchor limitation.
- **Engineering standing rows** (owner-gated, `docs/TASKS.md`): st-2
  identity promotion, st-5 containers/entity-birth, scav-1 compaction,
  parse-2 disambiguation halves, P1-2/P1-3, generalized-controls (until
  a second independent instance).
- **Ancient Network research** — contradiction-gated only
  (`WORLD_WORKPLAN.md` §4).
- **The §12 non-goals** (`WORLD_WORKPLAN.md`): full atlas, encyclopedic
  species/religion/language catalogues, continent-scale cosmology,
  production world pack before the anchor/meso proof.

## 9. Current W-stage and gate

The standing work boundary after iter-287 (the owner's execution order;
`WORLD_WORKPLAN.md` §7 the owner):

```text
W1–W4 = closed historical foundation (kernel, domains, anchor A1–A3,
         causal mesh, the meso working set — do not reopen)
W5     = gate met / evidence retained (the dispositions landed, the
         fill-list closed, the live band scored, I0 confirmed)
W6     = COMPLETE at both bands (the substrate row, the reading band
         both halves, the gap routings + the re-measure, the live
         re-read — do not reopen without fresh regression evidence)
W7     = COMPLETE (four rows landed, iter-283/284/285/286: the battery,
         the reading band's LLM half, the live half — the reading band
         CONFIRMED at both bands — and the named-boundary route)
W8     = CURRENT EXECUTION STAGE — integration readiness (opened
         iter-286 on the owner's conditional call; the first row —
         the seven-criteria readiness audit — LANDED iter-287:
         all seven criteria MET at the measured band, the gaps
         named; the remaining rows the owner's call)
```

W6's station law: run the genre matrix
(adventure/mystery/politics/relationship/tragedy/comedy/biography) on
the same canonical package; **a failed genre test identifies the missing
world substrate — it never triggers plot writing**. Classify every
failure by the §6 vocabulary before any response. Do not restart a
closed stage unless fresh evidence demonstrates a regression. W6 is a
new station — entered on the owner's explicit call.

W6 COMPLETE at both bands (the substrate row iter-278, the reading
band iter-279/280, the routings + the re-measure iter-281, the live
re-read iter-282 — every row's record `WORLD_TESTS.md` §9's W6
entry, the single owner). W7 ENTERED on the owner's explicit call
(iter-283, «W7 открывай если больше ничего не осталось» — no W6 row
remained). W7's station law (`WORLD_WORKPLAN.md` §9): for any new
major capability, regime or institution ask the eight questions —
why possible / why not universal / what does it replace / what does
it make harder / who profits / who resists / who remembers / what if
it disappears — then run the compression test and remove or merge
decorative material. Four rows LANDED, in order (every row's full
record `WORLD_TESTS.md` §9's W7 entries — the single owner): the
battery + the compression test (iter-283 — no decorative material at
the measured band; an unfired surface is possibility-space, the doors
stay); the reading band's LLM half (iter-284 — the battery's answers
as blind readings over the same battery's twins, every bar MET, the
readers' own discovery: the disappearance's footprint wider than the
deterministic census); the LIVE half (iter-285 — the owner's own
blind reading scored against the standing preset, every bar MET n=1,
all three ripples caught in the blind half: **the reading band
CONFIRMED at BOTH bands, the ripple footprint measured at both
bands**); the named-boundary rendering route (iter-286, the owner's
«точечный и быстрый (read-side only)» call — iter-284/285's boundary
(a) routed read-side: rs-13, the refusal's institutional cause on
the records surface, `tests/test_namedroute.py` the witness). The
owner's two dispositions on the same call, both resolved: the
disappearance-battery extension to the remaining majors answered NO
(the meso units' drivers already pass the anchor's disable test —
re-measuring carried evidence is polishing; the row stays available
for a NEW major's own arm), and W8 OPENED on the conditional call
(«если нет, то и w8 открыть»). The owner's RU report:
`docs/iterations/iter-286-namedroute-report.md`.

W8's first row LANDED (iter-287, the owner's «w8 можешь начинать
делать» call — the station ENTERED on the owner's explicit call;
R0 doc-only: the audit consumed the accumulated evidence, nothing
re-measured): the seven-criteria readiness audit — every criterion
cited to its standing owner, every gap named where the evidence is
thinner than the claim (the full record `WORLD_TESTS.md` §9's W8
entry — the single owner). All seven MET at the measured band: the
authored causal substrate (ANCHOR_REGION §5's mesh + D-237's
composition), a demonstrated meso unit (§6.1–6.5's five, three
CONFIRMED / two PARTIALLY — the band honesty carried),
pack-primitive representability (D-240/D-191 + the iter-283
compression inventory + the rs-1..rs-13 family; the I0 inventory's
three candidates the named unpromoted gaps), the ordinary event's
persistent human-scale consequence (the I0 witness + the exit
criterion met four times), explicit knowledge asymmetry (the §9
doctrine + the zero-leak blind suite + the measured witnesses),
world-specific material outside the core (INV-3, executable), the
proven-vs-hypothetical distinction (§10's vocabulary + the
PROPOSAL fence). VERDICT: the track READY for the broader
implementation handoff at the measured band — the named gaps (the
meaning-layer thinness, the two PARTIALLY meso units, the three
unpromoted candidates, the one-year persistence band, the
review-time influence check, the documentary reading bands) ride
the handoff as its honest boundary list, never as unknowns. The
station's remaining rows: the owner's call. The owner's RU report:
`docs/iterations/iter-287-readiness-report.md`.

W6's row-by-row landing history (iter-278 the substrate side;
iter-279/280 the reading band's LLM and live halves; iter-281 the two
gap routings + the blind re-measure; iter-282 the owner's live
re-read over the fixed material): every row's full record lives in
`WORLD_TESTS.md` §9's W6 entry — the single owner (D-024: the
verdicts above carry the state; the history is not restated here).

## 10. Navigation (the authoritative owners)

| Question | Read first |
|---|---|
| operating law, invariants, caps, git safety, delivery | `AGENTS.md` |
| where things are / who owns a question | `docs/AGENT_NAVIGATION.md` §1/§3 |
| worldbuild index, ownership table, status vocabulary, terminology fence | `docs/worldbuild/README.md` |
| world identity, hard laws, negative space | `WORLD_KERNEL.md` |
| domain mechanics | `RESONANCE.md` / `LIFE_PERSONHOOD.md` / `PEOPLES.md` / `CULTURES_CIVILIZATION.md` |
| the anchor: causal map, mesh, meso units, meaning slices | `ANCHOR_REGION.md` |
| authoring doctrine (pipeline, meso, residue, knowledge asymmetry, quality bar, transfer) | `WORLD_AUTHORING.md` §§6–10, §18–19 |
| test definitions, evidence records, probe forms | `WORLD_TESTS.md` (§9 the records, §7 the probes) |
| the W-ladder, gates, expansion rules, deferred list | `WORLD_WORKPLAN.md` |
| intake/D provenance, iteration records | `docs/blueprint/phases.md` §6 + `docs/DECISIONS.md` |
| verification claims | `docs/TEST_PLAN.md` §9 |
| actor perception/knowledge boundary | `docs/DIRECTOR_SPEC.md` + `docs/ref/live_char_guide.md` |

**The preserved packs** — `docs/worldbuild/archive/`: the verbatim v4.5
zip (bootstrap evidence, md5-pinned) + the verbatim suite zip
(`CANONSIM_AGENT_WORLD_SUITE_v1_0`, iter-311 — CORE_WORLD v1.3 + WORLD_TRACK
v4.6, md5/sha256-pinned) + the provenance README. The suite's cross-pack
boundary is ROUTING, never authority: cross-cutting execution/scale/
semantic-equivalence/LLM-boundary questions (its C1–C5 taxonomy) are
parked research — the owner-gated TASKS row `core-1`, the POC contracts
opened from the archive only when that row fires; world-specific
questions stay with this file and the worldbuild owners. Open the archive
only for what the packs uniquely retain: the full caravan/mobility dossier
(the RU v3 source), the complete probe contracts, the dormant-regime
cards, the intake crosswalk, and (suite-only) the C1–C5/POC contracts and
the sync matrix. They are derived convenience copies — the repository's
owner documents are current; the packs never override them, and they
must not be re-ingested for subsequent tasks (this file is the
ingestions' durable result).

## 11. Explicit anti-patterns

- Do not evolve the simulator toward a plot generator; no drama manager,
  no global liveness/confidence/story scores, no plot patches to rescue
  failed genre tests.
- Do not let the LLM invent canonical facts, outcomes, hidden state or
  causal motives; do not use prose quality as evidence of causal
  completeness; do not repair a substrate defect with narrative.
- Do not treat the player as an exception to world rules; do not force
  NPC behaviour from outside the doors.
- Do not add runtime primitives without consumer + failure + native
  limit + falsifier (the §2 gate); prefer pack data and test relations;
  do not broaden the engine when a pack already expresses the need.
- Do not promote calendar decoration to causality without a consumer; do
  not duplicate institutional functions (the function-loss probe is the
  arbiter); do not build one giant world-simulation layer.
- Do not flatten regime / lineage / institution / place into one
  taxonomy; do not add a region because the map feels incomplete; do not
  allow unexplained cross-regime placement.
- Do not build a generic relationship meter, belief graph, mobility
  scalar or maintenance engine where a bounded mechanism on existing
  primitives is the honest first step.
- Do not delete dormant design memory because it is not active; do not
  silently drop an intake row (no-loss rule:
  `ABSORBED | DEFERRED | REJECTED | SUPERSEDED`, never silent omission).
- Do not silently reopen: the D-236 temporal contract, the closed W1–W4
  stages, the J-3 rejection, the 40/80 close-as-residue disposition, or
  any owner-gated row.
- Do not turn this file or the archive into a second source of truth;
  one fact has one owner — link it.
