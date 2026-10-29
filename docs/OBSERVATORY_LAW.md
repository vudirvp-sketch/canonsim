# OBSERVATORY_LAW.md — The World Observatory & Control-Plane Law

> The owner's 2026-09-25 corpus re-homing call (D-218, iter-237) over the
> external `CANONSIM_WORLD_OBSERVATORY_AND_CONTROL_PLANE_V5_2.md`. Per the
> D-024/D-200 law the external brief is NEVER vendored; THIS file is the
> repo-side binding distillation. **The source's §-numbering is preserved
> 1:1** (the source itself has no §15 — kept as-is so every reference
> resolves).
>
> **Status discipline:** the source self-declares `PROPOSAL / RESEARCH
> ARCHITECTURE / OPERATIONAL ANALYTICS`. This law therefore owns TWO
> distinct layers, never blended: (a) the **operating contracts** binding
> on the obs-N row family (the plane law, run identity, the World Question
> contract, query families, result schemas, the promotion gate, the agent
> loop, the DoD) — these are LAW for every Observatory row; (b) the
> **research semantics** (§3–§10) — the analytical vocabulary and design
> direction those rows draw from, promoted into implementation ONLY
> through their own owner-gated row + falsifier. Historical findings
> (§17) are EVIDENCE SNAPSHOTS, never current-state truth.
>
> **Routing law:** every Observatory question routes HERE for analytical
> semantics (planes, queries, evidence, experiments, promotion); the
> INTERACTION grammar (workspace regions, selection, focus, compare,
> timeline, zoom, epistemic rendering, empty semantics) stays
> `docs/FRONTEND_UIUX_LAW.md` §3–§13; application operations/lifecycles
> stay `docs/WORKBENCH_APP_LAW.md`; world/semantic truth stays CanonSim's
> owning specs. This document never overrides `AGENTS.md`, `STATUS.md`,
> `docs/TASKS.md`, `docs/TEST_PLAN.md`, the owning `*_SPEC.md` or
> `worldbuild/*`.

## 0. Operating law

One semantic authority:

```text
CANON generates truth
→ OBSERVATORY explains/queries truth
→ EXPERIMENTS test claims
→ CALIBRATION searches bounded parameter space
→ STEERING only proposes/selects lawful bounded interventions
→ LLM interprets/renders evidence; it never authors canon
```

Authority order for Observatory work:

```text
AGENTS.md / repository law → STATUS.md / active state
→ owning specs / runtime contracts → CanonSim / worldbuild semantics
→ THIS LAW → derived analytical artifacts → agent / LLM interpretation
```

Never create: a second semantic authority, a second canonical event
store, a second world model, a hand-maintained causal database, analytics
that can mutate canon, optimizer output promoted to canon, LLM output
promoted to canon.

Evidence classes: `FACT | INFERENCE | HYPOTHESIS | PROPOSAL | UNKNOWN` ×
dispositions `CONFIRMED | PARTIALLY_CONFIRMED | REJECTED | UNRESOLVED |
DEFERRED`.

Distinctions that must survive every projection and every rendering:

```text
observed behavior ≠ intended behavior ≠ possible implementation ≠ warranted implementation
chronology ≠ dependency ≠ influence ≠ causation
world truth ≠ actor knowledge ≠ belief ≠ interpretation ≠ intent ≠ resolution ≠ consequence ≠ narration
permission ≠ capability ≠ intent ≠ resolution ≠ consequence ≠ learning
assignment ≠ realized intervention
```

Agent laws:

```text
Do not infer a world law from one seed.            Do not infer causality from event adjacency.
Do not infer coverage from a fixed script.         Do not infer semantic outcomes from cosmetic hashes.
Do not widen claim scope beyond evidence scope.    Do not add runtime machinery when a derived projection answers.
Do not let analytics become authoritative.         Do not call a read dependency causal without intervention evidence.
Do not treat a research rollout as a real run.     Do not promote a regime label into canonical state.
```

Core doctrine: **do not make the world cognitively small — make its
consequential structure queryable.** A strong long-horizon witness is a
durable loop:

```text
PAST EVENT → STATE/RELATION/OBJECT/KNOWLEDGE/RESOURCE/INSTITUTIONAL RESIDUE
→ CONSUMER → DECISION/EVENT → NEW RESIDUE → LATER CONSUMER
→ CHANGED FUTURE OPTION
```

Not every event needs every link; claims about durable world behavior do.

## 1. Plane separation and Workbench ownership

Five logical planes plus presentation:

```text
CANONICAL PLANE     creates truth; append-only events; fold/replay; canonical state
OBSERVATION PLANE   regenerable projections and queries over runs/logs
EXPERIMENT PLANE    controlled comparisons, ablations, mutations, counterfactuals
CALIBRATION PLANE   offline bounded parameter search and held-out checks
CONTROL PLANE       lawful bounded intervention selection only
PRESENTATION PLANE  human/agent/LLM rendering of evidence
```

The Workbench application owns: operation identity, analytical-run
lifecycle, analysis job admission/bounds, query dispatch, artifact
identity/provenance, result retention/recovery policy. CanonSim owns:
canonical events, fold/replay, semantic time, RNG, world truth,
pack/world meaning, canonical validation. The frontend owns:
observation-profile selection, query/result presentation, assurance/debug
views, visualisation of derived analytical data, camera/UI/presentation
state.

Derived analytical stores are allowed only when: `read-only |
rebuildable | attributable | scoped | versioned | deletable`. Canonical
JSONL remains sufficient to reconstruct every analytical projection.

## 2. Run identity and analytical evidence

Every analytical run must be attributable. Minimal manifest:

```text
run_id · parent_run_id · pack · pack_version · schema_version · seed
scenario/script · arm · parameter_fingerprint · start_tick · end_tick
canonical_log_digest · environment_fingerprint · analysis_version
```

For byte-sensitive work also retain as material: Python version,
`PYTHONHASHSEED`, pack/version, schema version, seed, scenario/script,
arm, parameter fingerprint, environment fingerprint. Never claim
cross-version byte identity unless the contract explicitly establishes
it (`requires-python >=3.11` alone is not a golden-byte contract).

Minimal rebuildable derived model:

```text
run · event_fact · state_delta · knowledge_fact · event_object
relation_delta · object_lifecycle · decision_trace · dependency_edge
world_profile · experiment · outcome
```

Field semantics (the projection contracts):

```text
event_fact:      event_id, tick, type, actor, target, cause_id, cause_kind, outcome
state_delta:     event_id, tick, entity, property, from, to, irreversible
knowledge_fact:  event_id, tick, actor/subject, knowledge_item, effect
event_object:    event_id, object_id, object_type, role
dependency_edge: derived evidence only; NEVER causal authority
outcome:         semantic predicate, first-passage time, persistence, scope, disposition
```

Storage ladder (never moved into runtime merely because useful offline):

```text
JSONL canonical truth · SQLite rebuildable local projection
FTS/vec derived retrieval only · DuckDB offline analysis
Parquet columnar population/archive · OCEL 2.0 optional analytical interchange
```

Reuse the existing analytical infrastructure before adding machinery:
`balance_harness.py`, `profile_harness.py`, `worldgen_profile.py`,
`chronicle.py`, `checkpoint.py`, paired-delta/common-random-number runs,
block-scoped ablations. The seven-hole UAP vocabulary is a test-design
lens, never a second ontology. Analytical output declares at least:
`source identity | scope | analysis version | observation profile |
claim/evidence class | freshness or source revision where relevant |
disposition`.

## 3. Semantic coverage: declaration → consequence

One canonical coverage path — a declared mechanism is COVERED only when
its consequence chain is observable end to end (the declaration alone
never counts; the §0 residue loop is the test). Coverage claims carry
their scope; a fixed script × one seed is never coverage. `[RESEARCH
SEMANTICS — promote per-row]`

## 4. World projections

Four projection families, each a bounded derived view over the run
model: **temporal** (windows, rates, transitions), **relational**
(pair/axis trajectories over relation_delta), **object-centric**
(lifecycle, residue, holders), **decision** (intent → gate → resolution
→ consequence traces). Projections are pure functions of (log, fold,
declared scope); they never feed back. `[RESEARCH SEMANTICS — the obs-3+
views draw from here]`

## 5. Causal archaeology, residue, influence

Archaeology reconstructs the verified chain behind a PRESENT condition:
`present blocker → residue chain → earliest verified difference →
disposition`. Influence footprints aggregate read/write/decision
dependencies as EVIDENCE — the evidence ladder (FRONTEND_UIUX_LAW §9)
governs what may be claimed: a read dependency alone never confirms
causation; only an intervention (BASE vs PERTURBED) moves the rung.
`[RESEARCH SEMANTICS]`

## 6. Ensembles, World Profile, regimes

A World Profile is a VECTOR of observables, never a scalar quality
score. Ensembles answer distribution questions (never one-seed laws);
regimes are detected labels over trajectory segments — presentation
vocabulary, never canonical state. Micro→meso→macro scales stay
explicit in every query's scope. `[RESEARCH SEMANTICS]`

## 7. Exceptional spaces

Outliers/rare events are first-class analytical targets (rare-event
discovery, exceptional-space detection/ablation) — never noise to be
averaged away. `[RESEARCH SEMANTICS]`

## 8. Endogenous agency: test before redesign

Apparent actor passivity is a HYPOTHESIS, never a design verdict:
measure the autonomous consequential rate and the intervention ladder
(§20's preference order) before any agency mechanism is proposed.
`[RESEARCH SEMANTICS]`

## 9. Experiments, mutations, counterfactuals

The experiment plane: controlled BASE vs PERTURBED pairs
(common-random-number where byte-fair), block-scoped ablations,
counterfactual replays. Every experiment closes §2's manifest per arm +
the assignment-vs-realized-delta record. An experiment never mutates the
canonical runs it reads. `[CONTRACT for the experiment rows]`

## 10. Sensitivity, calibration, world envelope, steering

Sensitivity screening → selected interaction sensitivity → constrained
calibration with held-out evaluation; the World Envelope is the DECLARED
acceptable trajectory band (alignment compares against it); steering is
research-only bounded rollout comparison — CONTROL-plane proposals
select lawful interventions, never rewrite canon; runtime steering
requires the §14 promotion gate. `[RESEARCH SEMANTICS + the steering
non-goals are LAW]`

## 11. Observation boundaries, player surface, and Workbench queries

Information states:

```text
OBJECTIVE → PERCEIVED → KNOWN → INFERRED → BELIEVED → NARRATED
```

Queries must distinguish: what is true · what actor A knows · what B
believes · what C actually observed · what D can legally infer · what
the player can receive · what the narrator said. Player/reader proof
chain: `WORLD TRUTH → OBSERVER ACCESS → KNOWLEDGE/ARTIFACT/INSTITUTION/
ENVIRONMENT SIGNAL → CHRONICLE/BRIEF/SURFACE → PLAYER INFERENCE`.
Readable prose never proves canon. Observer-boundary adversarial corpus
covers omniscient queries, `knower=None`, planted leaks, legal prefixes,
relevant actors, provenance matching.

### World Question contract (the full field set — obs-1 landed the
DRAFT display's first four; the rest are the obs-3+ contracts)

```text
QUESTION · CLASS · TARGET · SCOPE · KNOWN · UNKNOWN
COMPETING_HYPOTHESES · INTERVENTION · CONTROL · OBSERVABLES
PRIMARY_DISCRIMINANT · RUN PLAN · REALIZED DELTA · FIRST DIVERGENCE
CAUSAL SLICE · PERSISTENCE · REPLICATION · FAILURE CLASS · DISPOSITION
PRACTICAL CONSEQUENCE · ENVIRONMENT/SCOPE
```

Result rule (every answer returns):

```text
ANSWER → EVIDENCE → MINIMAL CAUSAL SLICE → UNCERTAINTY → NEXT DISCRIMINATOR
```

Query families:

```text
OBSERVE      profile / ensemble / relation / object / temporal / regime
EXPLAIN      why event / what reads / what consumes / where divergence begins
SEARCH       reach target / deep action / missing consumer
ARCHAEOLOGY  present blocker / residue chain / earliest verified difference
ALIGN        trajectory vs envelope / violated dimension
CALIBRATE    bounded parameter search
STEER        lawful bounded rollout comparison
```

Standard result schemas (the bounded shapes every EXPLAIN-class query
returns; WHY STAGNANT and WHY RELATION X are the canonical examples):

```text
EXPLAIN EVENT: EVENT · PRECONDITIONS/READS · IMMEDIATE EFFECT
  RELATION/OBJECT/RESOURCE EFFECT · DOWNSTREAM CONSUMER · FIRST DIVERGENCE
  PERSISTENCE · OBSERVER EFFECT · PLAYER EFFECT · EVIDENCE CLASS/DISPOSITION

WHY STAGNANT:  WINDOW · ROUTINE SHARE · CONSEQUENTIAL SHARE
  ACTOR CONCENTRATION · AUTONOMOUS CONSEQUENTIAL RATE · EVENT CLUSTERING
  CHANGE FROM PRIOR WINDOW · COMPETING DIAGNOSES · CONTROL RESULTS · DISPOSITION

WHY RELATION X: PAIR/AXIS · TRAJECTORY · EVENT CONTRIBUTORS
  (+ the influence/residue fields per §5)
```

## 12. Verification and recertification

Every Observatory capability is verified against its declared question:
replay determinism, projection equality from the canonical log, observer-
boundary enforcement, held-out checks where claimed. Recertification
fires on: engine/pack/schema change, projection logic change, worldbuild
material change. Historical evidence never stands in for current
repository state — re-read the owner files. `[CONTRACT per row]`

## 13. Worldbuilding-scale validation

World-scale claims (worldbuild/*) route to the world track's own tests
(`docs/worldbuild/WORLD_TESTS.md`); the Observatory provides the
measurement substrate, never the world-law authority. The terminology
fence applies: "canon"/"Echo" on the worldbuild side never mean INV-1's
log canon or `core/echo.py`'s read model.

## 14. Runtime-promotion gate and standing non-goals

A new runtime primitive requires ALL of:

```text
REAL CONSUMER · REAL FAILURE/MATERIAL QUALITY GAP · NATIVE LIMIT
REPEATED SHAPE · MINIMAL INTERVENTION · FALSIFIER
INFORMATION/SEMANTIC OWNER · PHASE/GATE · VERIFICATION PLAN
```

Otherwise the result stays a research vocabulary / read-side projection
/ test relation / proposal. Standing NON-GOALS absent new evidence and
explicit ownership:

```text
second canonical world database        second semantic authority
generic canonical graph database       generic workflow/lifecycle runtime
generic reactive engine                full CRDT/MVCC semantic world state
generic all-purpose planner            LLM-controlled canon
universal truth/confidence/risk score  multi-oracle "truth" engine
permanent diagnostic graph as authority
full distributed data platform without workload evidence
optimizer as world law
```

Derived graph/object/process/warehouse/optimizer structures are fine
when their non-authority boundary is explicit.

## 16. Unknowns and evidence discipline

Keep visible until evidence changes status:

```text
current long-horizon endogenous idleness   = HYPOTHESIS / UNRESOLVED
fork-with-perturbation semantics           = UNKNOWN until measured
runtime steering cost                      = UNKNOWN until measured
cross-version byte identity                 = NOT A CONTRACT unless established
derived read-set sidecar necessity          = PROPOSAL; shadow derivation first
OCEL runtime role                           = NOT RUNTIME; analytical interchange only
distributed analytical backend necessity    = UNKNOWN / workload-gated
```

## 17. Preserved historical evidence (snapshots — never current truth)

The witness findings that justify the roadmap (from the supplied source;
re-read `STATUS.md` before treating any number as current):

- **F1** raw `cause` depth is mostly adjacency (`cause == previous` ≈
  100%/87%/64% across the three historical witnesses) — raw cause depth
  is not world depth.
- **F2** the historical long-horizon witness was routine-dominated
  (routine share ≈ 0.91; ≈98% signature repetition; 0 irreversible
  state changes) — witness-specific evidence, not a world law.
- **F3** a witness is not a distribution (province_feud seeds 1–60: the
  headline chain 6/60; all final-state fingerprints differed).
- **F4** action census is cheap (~27 ms/run); naive mutation guidance is
  weak (25/42 ≈ random) — deep reachability needs precondition-aware
  search.
- **F5** fixed-script coverage is confounded by driver design and seed
  choice.
- **F6** the stale schema-reader defect (writer rejects stale
  `schema_version`, reader accepted it) — routed through normal
  verification ownership, not Observatory authority.

Witness portfolio (complementary witnesses; never collapse into one
giant scenario): `tavern/{day1_full, day1_theft_and_arson, exp0_week}`,
`road/road_smoke`, `grim/grim_smoke`, `pressure/pressure_smoke`,
`province/{province_smoke, province_companion, province_feud,
province_calendar}`. The per-pack capability matrix (movement, relations,
knowledge asymmetry, rumor, crime, fire, object lifecycle, economy,
groups, calendar, weather, director, leverage, worldgen, long horizon,
causal ablation) is ROUTING EVIDENCE for choosing a witness per question
— the full table lives in the owner's source copy; the committed packs
are the ground truth.

Cross-domain mechanism transfer (the transplantation law):
`foreign domain → mechanism → invariant → remove domain cargo → target
adaptation → incompatibilities/hidden assumptions → cheapest
discriminating test → realized consequence → transfer/scope check →
durable residue`. Search for OPERATIONS, not labels (generation,
propagation, filtering, feedback, degradation, counterfactual ablation,
…). Reject `SURFACE ANALOGY | CARGO-CULT TRANSFER | HIDDEN ASSUMPTION |
ARBITRARY TRANSFER | DECORATIVE COMPLEXITY | THRESHOLD LEAKAGE |
TERMINOLOGY LEAKAGE | FALSE INDEPENDENCE`.

Big-data strategy: many runs/long histories/wide populations —
`SMALL JSONL+SQLite · MEDIUM DuckDB over exports · LARGE Parquet+DuckDB
· DISTRIBUTED only after workload evidence`. High-value population
queries: relation trajectories, object lifecycles, outcome/time-to-event
distributions, rare-event discovery, run clustering, regime transitions,
parameter sensitivity, counterfactual divergence, process variants.

## 18. Execution roadmap

```text
P0 expose the substrate   action-to-consequence census · multi-seed population
                          runner + manifest · BASE/PERTURBED divergence harness
                          · thin analytical projection · compact World Profile
                          · run/trajectory artifact format · H-AUTONOMY tests
P1 explanation            relation ledger/lifecycle · object lifecycle · temporal
                          multiplex graph projection · shadow decision/read
                          traces · causal slices + counterexample capsules
                          · residue/persistence · influence footprints · regime
                          detection · bounded World Question surface
P2 search/calibration     precondition-aware backward reachability · sensitivity
                          screening · interaction sensitivity · constrained
                          calibration + held-out · exceptional-space ablation
                          · research-only steering
P3 conditional runtime    receding-horizon director · runtime bounded intervention
                          search · endogenous goal arbitration · adaptive params
                          — EVERY item needs a new runtime contract + §14's gate
```

## 19. Candidate analytical CLI

Names illustrative; exact commands implementation-owned: `obs run
--pack --script --seeds a:b --arm` · `obs outcomes --class` · `obs
census --pack` · `obs profile --run/--seeds --window` · `obs relation
--actor A --actor B` · `obs object --id X` · `obs slice --event/
--entity/--property` · `obs archaeology --condition` · `obs pair --base
--perturb` · `obs regimes` · `obs reach --target` · `obs sens` · `obs
calibrate` · `obs align` · `obs steer`. All outputs bounded,
deterministic where the underlying run is, scoped, evidence-bearing.

## 20. Agent operating loop

For any material world question:

```text
 1 DEFINE    target phenomenon, scope, horizon, envelope    7 TEST      cheapest minimal pair/ablation/control
 2 OBSERVE   multi-seed population, not one witness        8 SCREEN    load-bearing parameter/content candidates
 3 PROJECT   action/relation/object/decision/outcome views 9 CALIBRATE bounded offline search + held-out
 4 PROFILE   vector trajectory + regime signals           10 ALIGN     trajectory vs envelope
 5 DIAGNOSE  violated dimension + competing explanations   11 STEER     optional lawful bounded rollout
 6 TRACE     causal slice + residue + consumers + first
             divergence                                          12 VERIFY    replay/mutation/observer/surface/held-out
                                                            13 PERSIST    only decisions/evidence that change future work
```

Default intervention preference (diagnostic default, not law):
measurement/observation gap → declared-but-unreachable path → missing
downstream consumer → content gap → parameter mis-calibration → missing
mechanism → research-only steering → runtime steering only after
explicit promotion.

## 21. Definition of done

An Observatory capability is complete only when:

```text
REAL QUESTION → REAL CONSUMER → MINIMAL DERIVED DATA → REPRODUCIBLE RUN
→ EXPLICIT OBSERVABLE → FALSIFIER → ACCEPTANCE TEST → BOUNDED AGENT
OUTPUT → DISPOSITION → DURABLE DECISION only if future work changes
```

A negative/inconclusive result is valid when evidence supports it. Every
completed research session records: `QUESTION · VERDICT · ESTABLISHED
EVIDENCE · KEY ALTERNATIVES TESTED · REMAINING UNCERTAINTY · PRACTICAL
CONSEQUENCE · NEXT VERIFICATION STEP`.

Final operating model:

```text
WORLD/CONTENT → CANONICAL DETERMINISTIC RUNTIME → IMMUTABLE RUNS
  (MICRO decisions/reads · RELATIONS trajectories · OBJECTS lifecycle/residue
   MESO groups/institutions/processes · MACRO ensembles/profile/regimes)
→ CAUSAL ARCHAEOLOGY → COUNTERFACTUAL DIVERGENCE → SENSITIVITY
→ CALIBRATION → WORLD ENVELOPE → BOUNDED STEERING (optional)
→ NORMAL INTENT DOOR → NEW CANON EVENT → FUTURE EVIDENCE
```

Absolute boundary:

```text
CANONICAL SIMULATION = truth
ALL OTHER LAYERS     = observation, experiment, search, calibration, control, or presentation
```

The intended outcome is not a simpler world — it is a world whose
history, relationships, dependencies, residues, distributions, causal
structure, failure modes and controllable degrees of freedom can be
queried by a human or LLM without manually reconstructing the repository.
