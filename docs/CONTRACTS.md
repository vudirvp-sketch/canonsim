# CONTRACTS.md — Pre-Implementation Contracts

> What this file is: the compact pre-implementation contracts for the
> contract-write rows (intake-29/D-175's closing proposal, written
> iter-144/D-177 under the owner's delegation). A contract pins what a
> row's build must satisfy BEFORE it starts: the decisions the row
> leaves open (each grounded in standing code or law), the invariant
> set, the falsifier (TEST_PLAN §9's claim-packet form), the minimal
> test set. What it is NOT: the row's spec — the spec fires
> just-in-time at the row's start, FROM experiment results
> (SPECS_BACKLOG's header law); the contract is the boundary, the spec
> the implementation's own words. Ownership never moves: TASKS owns
> WHAT/WHEN (the ORDER owner decides), the row keeps its acceptance
> criteria, this file owns the pre-implementation HOW-boundary. When a
> row's build lands, its spec absorbs its contract by reference (never
> restated, D-024) and the section here collapses to a one-line
> pointer. Cap-law: `docs/*.md` ≤600 lines, substance-filtered
> (AGENTS §6.1); the fifth contract (§9, iter-319) crossed the
> ceiling after the cruft passes — the file stands over with the
> guard's allowlist entry + the worklog rationale owners (§6.1's own
> law: the file stays over, the worklog records why). iter-320's cap
> pass: the §6..§9 falsifier RECORDS collapsed to the pointer form
> (the verbatim numbers + md5 pins live in the iteration reports —
> D-024's single owner); the new sections land natively in that form;
> the decisions themselves are never-cut substance (owner-accepted
> law). iter-321 lands §11 the same way — the registry's seven
> definitions are the standing shape; a per-contract split is the
> owner's call, never a silent restructure.

## 1. roads-1 — LANDED (iter-145, D-178)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-145 + D-178 + worklog
> iter-145 own the landing record — the pass
> (`core/worldgen.py::_pass_roads`), the one shared read
> (`core/roads.py::exits`), the lint, the §9 claim-packet evidence.
> The contract's own pinned decisions, verbatim, in git history at
> the iter-144 commit.

## 2. res-1 — LANDED (iter-146, D-179)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-146 + D-179 + worklog
> iter-146 own the landing record — the substrate
> (`core/economy.py`: the account primitive, the three verbs, the
> flows on the macro cadence, the derived prices), the door's soft
> arm (`account_at_least`), the resolver (`account`), the commit
> gate's loud floor, the lint (`core/packlint/economy.py` + the
> actions/entities cross-checks), the §9 claim-packet evidence. The
> contract's own pinned decisions, verbatim, in git history at the
> iter-144 commit.

## 3. since-1 — LANDED (iter-147, D-180)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-147 + D-180 + worklog
> iter-147 own the landing record — the fold
> (`brief/since.py::ReunionFold`: the per-entity encounter epochs,
> the apart-window deltas, the reader's apart-born records), the
> cards' since-segments (BRIEF_SPEC §3.4's extension, §3.9's
> amendment — the knower's own segments riding the shared cards),
> the pack's `since_lines` vocabulary + its lint, the §9 claim-packet
> evidence (the fold/document/zero-price arms CONFIRMED at the
> measured band; the decision arm DEFERRED to the first consumer).
> The contract's own pinned decisions, verbatim, in git history at
> the iter-144 commit.

## 4. engine-1 — LANDED (iter-177, D-193)

> The build's spec absorbed this contract by reference (never
> restated, D-024): `docs/TASKS.md` iter-177 + D-193 + worklog
> iter-177 own the landing record — the GBNF mapping repo-side
> (`brief/gbnf.py`, the snapshot's engine-facing serialization with
> the door's shape laws encoded; PARSER_SPEC §2.1), the explicit
> adapter (`cli/engine.py` — INV-4's one-module form, AGENTS §4), the
> door wiring (`--engine`, the file contract preserved — the runtime
> engine is "the operator"), the failure→ladder mapping (§5's re-ask
> ladder + the D7 degradation rungs; PARSER_SPEC §5), INV-4 lifted
> with the AGENTS §4/§8 edits riding, the model-facing serializer
> contract now `docs/PRESENTATION_SPEC.md`'s (iter-178), the adapter
> contract tests + the golden grammar + the Layer-1 suite green with
> ZERO gate edits (the §4.3 claim packet's proof; TEST_PLAN §9's
> form). The contract's own pinned decisions D1–D8 + the invariant
> set + the falsifier, verbatim, in git history at the iter-170
> commit. The station-side remainder (the 27B GBNF parse arm + the
> one-model-constrained A/B — §4.3 arm a; the grammar's compile
> check at the live backend) lives on as TEST_PLAN §8.5's standing
> gap rows, the owner's next station run.

## 5. wb-1..N — the Workbench family (the v5.2 Redot brief, owner's 2026-09-24 call)
> Source: the owner-supplied `canonsim_workbench_v5_2_redot_2026-09-24`
> package (5 documents, external — the convenience-copy law D-024; D-200
> the admission). **§-reference map (D-218, iter-237):** every `app
> spec §N` citation resolves to `docs/WORKBENCH_APP_LAW.md` §N,
> Observatory-doc §N to `docs/OBSERVATORY_LAW.md` §N, the frontend
> spec's §46 ladder to `docs/FRONTEND_UIUX_LAW.md` §25, the
> world-presentation contracts (§§23–31) to
> `docs/WORLD_PRESENTATION_LAW.md`; the external originals stay with
> the owner — no repo work requires them.
>
> **Redot half DELETED (iter-290/D-245 — the owner's «удаляй redot»
> call):** the whole `.gd` tree, its proof packets
> (`test_visual_proof`/`test_shell_proof`/`test_shell_contract`), and
> the engine index are gone (recovery: git history +
> `docs/frontendweb/archive/`); its GDScript lessons carry forward as
> PRINCIPLES only (STATUS FAQ). The Python half (scene IR, gateway,
> operations, platform) is untouched: `workbench/` is periphery
> (D-046), imports `core/` read-side APIs only, zero canon writes,
> network surfaces exactly INV-4's three sanctioned modules (the
> wb-4/D-201 + wb-9/D-208 owner-gated exceptions). The web client
> (`frontend/`, D-244) is the active consumer.
>
> wb-1..12 all LANDED (the landing detail: TASKS' wb rows + the
> worklog + git — the per-row notes collapsed at iter-316's cap pass,
> the family's decision text at this pass, both verbatim in git
> history). The remaining rows (wb-13..N) are owner-gated — TASKS owns
> WHAT/WHEN; the live boundary laws live in their owners (INV-4,
> WORKBENCH_APP_LAW, FRONTEND_WEB_LAW, the scene-IR status laws in
> `tests/test_scene_ir.py`).

**Family composition** (TASKS owns WHAT/WHEN; the brief's own order,
owner-gated per row): the landed ladder wb-1..12 above; wb-13+ per the
brief's §32/§46 ladders (live events + reconnect/resync; persistence;
the frontend rows — inference; history/diagnostics; the CanonSim
seam). Engine/API facts for the deleted Redot half route to the
archived pack's reference docs (D-245); the web client (`frontend/`,
D-244) is the active consumer.
## 6. sem-1 — the semantic event validity + authority contract (review-C1/D1, the confirmed queue's head; the DEFINITION landed iter-316)

> Owner-confirmed 2026-10-03 (iter-315's queue). R0–R1 definition
> only: NOTHING here is implemented — no gate code, no schema change,
> no draft field added (the row's own law). This section pins what any
> future admissibility build must satisfy BEFORE it starts; the
> implementation is NOT a standing row — the owner opens it after
> accepting this contract (the runtime-promotion gate: a named
> consumer + a measured native limit + the falsifier below).
> **Owner-ACCEPTED AS LAW 2026-10-03** (the iter-318 continuation call:
> S1–S7 binding for every future implementation; the implementation
> row itself stays the owner's separate call).

**Pinned decisions** (each grounded in standing code or law):

- **S1 — one semantic owner.** The resolver circuit — the intent door
  (`core/intent.py`: loud shape validation, preconditions, checks,
  OCC) + the resolver registry (`core/resolvers.py`) + the loop's
  mechanic producers (the map below) — stays the SOLE decider of what
  an event means: its type, outcome payload, effects. The
  admissibility gate never re-derives meaning, never re-runs a
  precondition or check, never recomputes an outcome, never edits a
  draft (review-D1; INV-1's writer monopoly untouched).
- **S2 — the declared effect surface.** Admission is checked against
  a declaration that exists INDEPENDENTLY of the draft instance: per
  event type, (a) the legal actor classes, (b) the allowed effect
  surface — the state-change family (entity-kind × prop pattern; or
  NONE for knowledge-only/no-op types), the knowledge channels, the
  hooks vocabulary, (c) the postconditions — pure predicates over
  (projection, draft, pack). The declaration lives in pack data (the
  action's `events` branches + effect blocks — `status_effects`/
  `balance`/`ignition` — and the templates' closed type vocabulary
  `Pack.event_types()`) + the mechanic modules' named constants
  (`STATE_MUTATING`, `REJECTION_EVENT`, the economy verbs + the
  account-stock props, the macro/calendar turn types + actor `world`,
  the weather/transition/crime/group/knowledge/leverage families) —
  NEVER per-draft, never derived from the producer's output at run
  time (the static twin: the packlint admission family already reads
  the pack-side half, D-152).
- **S3 — the authority vocabulary (emit-side).** The actor classes the
  producers already imply: the player entity, npc ids, `world` (the
  ambient/clock/genesis family — macro/calendar/weather/worldgen/economy
  aggregates), group ids (the condensation aggregates). An event type's
  declared authority = the legal actor classes for THAT type (e.g.
  `year_turns` → `world` only, `core/macro.py`'s own declaration;
  `intent_rejected` → the front door's own emission). auth-1 (D9) owns
  the INPUT-side pipeline (interpretation → classification →
  authorization); sem-1 pins only the emit-side check — the two
  vocabularies must never contradict (the namespace fence, the
  package's §5).
- **S4 — the gate.** Pure and non-resolving:
  `admit(draft, declaration, projection) → ADMIT | REJECT(reason)` —
  total, no writes, no RNG, no queue or resolver calls; it checks ONLY
  authority (S3) + the declared surface and postconditions (S2).
  Placement: INSIDE `_commit`, after the existing delta gate, before
  `writer.append` — ONE door, one more check (D-035's form extended;
  never a second door, never a second writer).
- **S5 — the RED semantics, two lanes.** An INTERNAL producer violation
  (a resolver/mechanic bug) fails LOUD — the pre-write `ValueError`
  form, the log stays clean (the delta gate's own law, KI#13's form).
  An EXTERNAL candidate (the mediator/engine path — a model-mediated
  draft) is refused SOFT — the candidate dies at the door, never an
  append of the unauthorized effect; what gets logged is the
  attempt-fact per the mediator's own vocabulary (PARSER_SPEC §4/§6's
  split, the emit-side twin). The lane is the producer's side of the
  door: internal = trusted-but-buggy, external = untrusted-by-contract.
- **S6 — no tautology.** The gate's reference is the DECLARATION (S2)
  — an artifact independent of the draft instance. Forbidden:
  comparing the draft to itself (its own fields as its reference), a
  checker derived from the producer's output at run time, "valid
  because the resolver produced it". The falsifier below is the
  executable disproof: the SAME declaration that admits the unmutated
  run rejects the mutated arms.
- **S7 — the `_commit` probe is a contract gap, not a production
  exploit.** Verified live at the iter-315 triage and re-proven by the
  falsifier at iter-316: `core/loop.py::_commit` gates deltas + schema
  + chain, never a declared effect surface or authority. No production
  path feeds hand-mutated drafts through the private door — every live
  producer is deterministic code over pack data; the gap is the absent
  check, not a live hole. The implementation row (the owner's call)
  closes it.

**Producer map at HEAD** (the declaration's owners): the pack-action
producers (the resolvers REGISTRY over the action's declared branches);
worldgen genesis; the front door's rejection; the crime family
(rotations/briefings/suspicion); the economy verbs; the clock family
(macro/calendar — actor `world`); the weather family; the group
aggregates; the transitions; the knowledge transfers; leverage;
reflection/onaction/states; the director releases (through the intent
door — auth-1's side).

**Invariant set**: INV-1..5 unmodified — the gate adds a check inside
the existing door (no second writer, no log edit, no schema change, no
network); INV-2 untouched (pure, zero draws — the byte-identical replay
over an admitted-only run is the proof); INV-3 untouched (the registry's
code side carries no domain words — pack data carries them); L13/L14
(one check at one door — no new layer, no framework).

**Falsifier** (TEST_PLAN §9's packet form — the future implementation
row's first RED test; run LIVE at iter-316, seed 42, the
plumbing_smoke playscript, the probe outside the repo per Rule 9):
mutate a captured producer output to stay schema-valid +
delta-consistent + chain-valid while violating the declared
authority/effect → the gate MUST go RED, no append. Both arms APPEND
today (the gap demonstrated live): Arm A (effect surface) the `wait`
output + a `pc_01.position` teleport → `ev_0011`; Arm B (authority)
the re-typed `year_turns` with actor `pc_01` → `ev_0012`; the
polluted log folds cleanly — a schema-valid log encoding an
unauthorized semantic effect, exactly review-C1's risk. The verbatim
probe output + the artifact md5 pins: the iter-316 report §D (the
record's single owner, D-024 — collapsed at iter-320's cap pass).

**Minimal test set** (the implementation row's, not today's): the two
falsifier arms RED→GREEN with NO append; the positive control — every
committed playscript corpus run admits 100% of its drafts, the golden
T1 fixtures byte-identical (zero false positives); the tautology guard
— flipping the DECLARATION side (e.g. declaring `wait` position-writable)
flips Arm A's verdict, proving the gate reads the declaration, not the
draft; the loud/soft split (S5's two lanes); INV-2 — byte-identical
replay over an admitted-only run.

**Deliberately NOT done here** (the row's own fence): no semantic
checker implemented, no schema or draft-field change, no second
resolver, no authority pipeline (auth-1's), no speech-act admission
(speech-1's), no representation or LLM-boundary work (core-1-C4's —
the namespace fence: review-C1 ≠ TASKS::core-1 C4).

## 7. caus-1 — the causal sufficiency contract (review-C2/D2; the DEFINITION landed iter-317)

> Owner-confirmed 2026-10-03 (iter-315's queue — the T2 half of the
> package's own T1+T2 sequence, sem-1's natural pair). R0–R1
> definition only: NOTHING here is implemented — no field added, no
> schema change (the row's own law). The implementation is NOT a
> standing row — the owner opens it after accepting this contract (the
> runtime-promotion gate).
> **Owner-ACCEPTED AS LAW 2026-10-03** (the iter-318 continuation call:
> K1–K6 binding for every future implementation; the implementation
> row itself stays the owner's separate call).

**Pinned decisions** (each grounded in standing code or law):

- **K1 — the causal spine, three parts, no graph.** `primary_cause` +
  `necessary_supports[]` + `provenance`. Today's `cause` field IS the
  primary-cause slot — the writer-enforced chain link (`core/loop.py`
  sets it to `writer.last_id` at build, the chronological-chain law;
  the hook family's `cause_hook` (D-140) and the OCC's
  `based_on_event_seq` are the per-family attributions the spine
  keeps). `necessary_supports[]` is the NEW declared claim: the prior
  events WITHOUT EACH the outcome becomes unreachable. `provenance`
  stays the evidentiary lineage block (seed / `cause_intent` /
  `cause_hook` / `assignment_tick` — the temp-1 primitive, D-236) —
  NEVER a causal claim (review-D2: provenance is lineage, not a
  second causal ontology).
- **K2 — counterfactual necessity (the definition).** Support X is
  NECESSARY iff the same-seed ablation of X (removing X's producing
  step/mechanic from the run's inputs) makes the claimed outcome
  UNREACHABLE: no event with the outcome's identity (type + actor +
  the material state-effect family) can occur in the re-derived run —
  replacements (`intent_rejected` and kin) do not count as the
  outcome. Enabling-but-unrequired, correlated, or downstream events
  are NOT necessary — no matter how informative they are.
- **K3 — necessity vs optional evidence, the split.** Optional
  evidence = everything the outcome's audiences observed or the fold
  consumed (perception records, ambient context, downstream
  reactions) — it lives where it already lives (knowledge records,
  the projection, the outcome payload), NEVER in `supports`. The
  discriminating test is the ablation pair: evidence-removal leaves
  the outcome REACHABLE (possibly shifted in tick or branch — the
  deterministic streams shift, reachability is the invariant);
  support-removal kills it.
- **K4 — the ablation battery, off-line only.** The verification
  instrument is the landed same-seed BASE/PERTURBED pair form
  (`scripts/divergence_probe.py`, D-235 — the semantic_diff oracle +
  the `cause`-ancestry walk). The battery runs over runs/logs,
  NEVER inside the tick loop: no runtime re-derivation of necessity
  (sem-1's S1 twin — the second-resolver ban holds for causal claims
  too).
- **K5 — the producer declares, the battery verifies.**
  `necessary_supports` is a PRODUCER-DECLARED claim: the
  resolver/mechanic names the events that established the facts its
  resolution materially used (the read-set × the establishing events
  — the loop's `_last_change` index (L3, D-050) is the existing
  `(entity, prop) → tick` derivation seed). The declaration is
  verified by the ablation battery over the corpus; a declared
  support that survives ablation (the outcome still reachable) is
  REFUTED — RED — and an omitted-but-required support is the
  completeness gap the battery reports.
- **K6 — compatibility + the no-DAG law.** INV-1: the supports ride
  the event document (an additive provenance-family field — any
  schema bump is the implementation row's business through AGENTS §8
  stop&confirm, never this definition). INV-5: supports reference
  committed event ids — append-only, never edited. Current consumers
  unaffected and additive-only: the divergence probe's ancestry walk,
  the observatory's cause-as-data (LAW §12), the hook-discharge
  family (director/urgencies/factions/metrics), `brief/validator`,
  the census forward walk. FORBIDDEN: DAG storage, graph-traversal
  machinery, provenance engines, generic causal inference — the spine
  is fields + one off-line battery; full graph machinery only behind
  the runtime-promotion gate (a named consumer + a measured native
  limit + the falsifier).

**Falsifier** (TEST_PLAN §9's packet form — the future implementation
row's first RED test; run LIVE at iter-317, seed 8, the day1 theft
scenario + one inserted perception step, the probe outside the repo
per Rule 9): the same-seed ablation pair demonstrates BOTH directions
AND the gap — BASE: the steal outcome `ev_0007` names as its `cause`
the CHRONOLOGICAL predecessor `ev_0006` (`look_around`) while the
materially-REQUIRED move `ev_0005` (without which the steal is
world-impossible) is INDISTINGUISHABLE in the outcome's own fields:
the necessity real, measurable, UNRECORDED (review-C2's risk —
"tree-like reduction can erase conditions required for the
outcome"). ABLATE-MOVE: zero steal-family outcomes, three
`intent_rejected` — the outcome unreachable (necessity). ABLATE-LOOK:
the steal still fires (evidence, not necessity). The verbatim probe
output + the artifact md5 pins: the iter-317 report §D (the record's
single owner, D-024 — collapsed at iter-320's cap pass).

**Minimal test set** (the implementation row's, not today's): the
ablation battery over the committed corpus — every declared support
kills its outcome under ablation (REFUTED declarations RED), the
evidence controls stay reachable; the declaration completeness
report; INV-1/INV-5 — the supports reference committed ids only, the
append-only log untouched; the consumers additive-only (the
divergence probe, the observatory, the hook family, the validator,
the census).

**Deliberately NOT done here** (the row's own fence): no field added,
no schema change, no DAG/provenance engine, no runtime causal
checking (the battery is off-line), no rewrite of the hook/OCC
attribution families (the spine EXTENDS them, never merges).

## 8. replay-1 — the semantic replay identity + recovery durability contract (review-C4/C7/C13/D4; the DEFINITION landed iter-318)

> Owner-confirmed 2026-10-03 (iter-315's queue — the T4 row, the
> queue's head after the owner's «продолжай очередь с replay-1 и так
> далее» call; S1–S7 + K1–K6 accepted AS LAW the same call, §6/§7's
> notes). R0–R1 definition + exactly ONE R2 KI fix (KI#111, found
> live by this contract's own falsifier — AGENTS §5's record-then-fix;
> a reader envelope fix, zero serialization change): NOTHING else is
> implemented — no serialization change (the row's own law), no digest
> field, no fsync policy. The implementation is NOT a standing row —
> the owner opens it after accepting this contract (the
> runtime-promotion gate).

**Pinned decisions** (each grounded in standing code or law):

- **E1 — the identity tuple, six components.** A run's semantic
  replay identity = `log_prefix_digest + engine_semantic_version +
  schema_identity + pack_semantic_digest + execution_config_digest +
  seed`. The question it answers: "may this execution legitimately
  CONTINUE or compare FUTURES with that one?" — never "are these two
  logs equal" (byte equality is T1's same-environment law, a different
  question). The components against their live carriers (the triage's
  named gaps, now code-grounded): `seed` — carried (header.seed) and
  checked at resume; `log_prefix_digest` — carried and checked
  (`core.checkpoint.prefix_digest`, sha256 over the first `1+offset`
  lines, append-stable under INV-5 — the cursor's binding teeth);
  `schema_identity` — carried and checked (header.schema_version,
  derived from the schema `$id` through the writer's own path; the
  reader + append-writer gates, log-1/KI#100 — a stale log is a
  migration, never a silent read), granularity a version STRING, not a
  content digest (an un-bumped schema edit slips — named limitation,
  the engine component the backstop); `pack_semantic_digest` — **GAP**:
  header + cursor carry `pack.name_version` (name@version) only —
  same-name content drift resumes silently (the falsifier's Arm A);
  `engine_semantic_version` — **GAP (implicit)**: header.commit
  records the writing build (the CLI's `_commit_id`, short HEAD or
  `unknown` offline) but resume never compares it (Arm B) — recorded,
  never checked; `execution_config_digest` — **GAP**: no complete
  run-level config identity exists; the only carried knob is
  `director_enabled` (cursor), and the Python env pin (header.python,
  checked at append) is the same-environment law's carrier (TEST_PLAN
  §1.1), not a config digest.
- **E2 — semantic identity ≠ continuation state.** Two different
  questions, different artifacts, different failure semantics.
  IDENTITY asks "same world semantics?" — the tuple, compared BEFORE
  anything else; a mismatch is a REFUSAL (a different world, never a
  warning). CONTINUATION asks "where in this run did the session
  stop?" — the cursor (entropy positions, clocks, counters); a
  mismatch is STALENESS (a different point in the same world) — also
  loud, the standing save-scumming law. The cursor's existing split is
  this law's embodiment: log-derivable state deliberately absent (the
  projection, the indexes, the WorldModel, the scene ledger re-derive;
  D-139). Never mixed: an identity component never rides the cursor,
  and continuation state never becomes identity.
- **E3 — the irreducible continuation state is a closed set.**
  "Irreducible" = not a pure function of (log, seed, pack, config).
  Today's complete set (the cursor's own law, restated as the
  contract's closed list): the bank positions, the director run marks,
  the clock tick, the crossing cursors (rotation / beat / macro /
  calendar), the intent counter, the live director toggle. Nothing
  else may enter: a new runtime field declares its side — identity
  component, continuation state, or non-canon presentation — and a
  continuation claim must prove irreducibility (a resumed continuation
  desyncs without it) or stay out.
- **E4 — the lifecycle: proposed → accepted → durable → committed.**
  PROPOSED: a producer's `EventDraft` (no id yet). ACCEPTED: the
  `_commit` door's checks pass (schema validate + the delta gate +
  the chain/tick laws, D-035) — an in-memory record, still refusable,
  invisible to the log. DURABLE: the line reached its durability
  boundary — today that boundary is the FLUSH (the honest form; its
  OS-crash semantics unproven, E6). COMMITTED: durable AND the
  continuation invariants hold (id assigned, cause chained onto a
  written event, tick monotone — the writer's own laws). The log line
  IS the commit record (INV-1/INV-5: committed lines are never
  rewritten); an accepted-but-not-durable line lost to a crash NEVER
  EXISTED — not a rollback, an un-happened event (E5a's recovery
  semantics).
- **E5 — the crash contract, three boundaries.** (a)
  APPEND-BEFORE-DURABLE — a flushed line torn or lost (OS crash,
  power loss): the truth is the last durable prefix; detection is LOUD
  never silent (a torn line fails the reader's format gate — LogError;
  KI#111 closed the bare-`JSONDecodeError` leak this iteration — and a
  lost tail behind the cursor pin refuses at resume, count/digest
  mismatch, never guessing the entropy); repair (dropping the
  never-committed tail) is the implementation row's business with its
  own crash curriculum — the definition pins the semantics only.
  (b) POST-DURABLE — the durable prefix moved PAST the cursor pin (a
  mid-drain crash, a manual append): the extra events' entropy state
  is unrecoverable → LOUD refusal (the standing law, already
  implemented). (c) DERIVED-STATE — checkpoints, the SQLite index, the
  chronicle artifacts: derived, never truth (INV-1; the checkpoint
  family's law) — a crash corrupting them costs replay cost, never
  canon, and verify-by-refold detects the drift loud.
- **E6 — `flush == durable` REJECTED (an evidence-free claim).** The
  writer flushes (three sites: header, append, close) and never
  fsyncs (zero calls across `core/`) — flushed bytes live in the OS
  page cache; an OS crash may eat them. What IS proven: clean-boundary
  resume — D-139, `tests/test_resume.py` byte-identity at every split
  point: LOGICAL durability across process boundaries, same
  environment. What is NOT: OS-level durability. Any fsync policy, a
  documented durability boundary, or a crash curriculum (kill -9 /
  power-loss simulation over the writer) is the implementation row's
  business — durable is never claimed on flush alone.

**Falsifier** (TEST_PLAN §9's packet form; run LIVE at iter-318 — the
test_resume corpus, seed 42, split after step 2, the probe outside
the repo per Rule 9): CONTROL — split+resume (same pack)
byte-identical to the uninterrupted run — the falsifier targets the
GAPS, never the law. Arm A (pack content drift): a rules.json content
mutation with `name@version` UNCHANGED — resume ACCEPTED, the tails
diverge from the first appended event — the SAME identity as far as
any carrier can see continued into a DIFFERENT future execution
(review-C4's risk, live). Arm B (engine identity decorative): the
header's commit never read by `Simulator.resume` — recorded, never
checked. Arm C (flush ≠ durable): the writer's 0 fsync / 3 flush(); a
torn tail → LOUD LogError (found KI#111 pre-fix); a lost pre-pin
tail → LOUD CursorError. The verbatim probe output + the artifact
md5 pins: the iter-318 report §D (the record's single owner, D-024 —
collapsed at iter-320's cap pass).

**Minimal test set** (the implementation row's, not today's — KI#111's
closed torn-tail test excepted): the identity-gate RED arms — a
same-name content-drifted pack REFUSED at resume (E1's pack digest
component); a foreign engine label REFUSED or the policy explicitly
pinned (E1's engine component); the positive control — the committed
corpus and every `test_resume` split stay GREEN with the gate live
(zero false refusals); the lifecycle arms — a torn tail never
silently repaired, a lost pre-pin tail refused; the closed-set pin —
the cursor envelope unchanged unless a field proves irreducibility.

**Deliberately NOT done here** (the row's own fence): no serialization
change (the row's law), no digest field added to the header or the
cursor, no fsync policy, no crash curriculum, no second store — the
identity components land behind the runtime-promotion gate (a named
consumer + a measured native limit + the falsifier), the owner's
call.

## 9. scale-1 — the causal-demand locality + work budget + certified commutativity contract (review-C5/C6/C16/C28/D5+D6; the DEFINITION landed iter-319)

> Owner-confirmed 2026-10-03 (iter-315's queue — the T5 row, the
> queue's head after the owner's «продолжай работу прошлой итерации,
> со scale-1 как я понимаю, и так далее» call; E1..E6 accepted AS LAW
> the same call, §8's note). R0–R1 definition only: NOTHING is
> implemented — no index, no budget counter, no cohort machinery (the
> row's own law). The implementation is NOT a standing row — the owner
> opens it after accepting this contract (the runtime-promotion gate).

**Pinned decisions** (each grounded in standing code or law):

- **Q1 — the three work classes, classified by CAUSAL DEMAND, never
  by implementation shape; declared per mechanism (pack data + mechanic
  constants — S2's twin); an implementation MEETS its class's
  complexity obligation or the gap is recorded (Q7).** LOCAL: the
  affected set by direct/indexed access — the resolver path, the OCC
  re-check (`based_on_event_seq`), the decay baseline via
  `_last_change` (L3/D-050, the standing indexed exemplar), the
  follow-up drafts' one-location reads. REGIONAL: bounded causal
  traversal from a demand seed — the transition spread over a
  location's spot set, the scene zones' ring recompute (depth-3), the
  one shared road-exits read (roads-1). GLOBAL: an explicit scheduled
  pass whose semantics IS the whole world — the fold/replay (T2), the
  macro/calendar turns, the entropy view, the unarmed one-scene law's
  per-beat everything, the cold census.
- **Q2 — the work budget is explicit, per origin, and exhaustion
  DEFERS (semantic debt), never silently drops.** A budget is a
  declared bound per scheduling unit (beat / crossing / pass tick),
  owned by the spending mechanism, visible in pack data or a mechanic
  constant — never an implicit emergent cap. Today's inventory: the
  director's 1-release-per-beat (a PACING budget, DIRECTOR_SPEC's
  law) is the ONLY budget in the tick loop — no general work budget
  exists (measured, Arm C2). The deferral law: exhaustion produces
  DURABLE deferred work through the standing queue forms — the
  self-rescheduling pass continuation (`loop._run_pass`), the SEEDED
  follow-ups (TIME-1), the director's seeded-hook buffer (D-005) —
  today all three unbounded and unaccounted (Arm C3). The pinned
  distinction: DUE WORK (the mechanism's semantics says it must run —
  a decay with a non-zero delta, a scheduled completion, a seeded
  follow-up) NEVER silently vanishes on exhaustion — it defers
  visibly; an ATTEMPT (a roll whose miss is the no-op outcome — an
  urgency miss, a gated autonomous try) is canon-noise (PARSER_SPEC
  §4/§6), never deferral, never loss.
- **Q3 — the default canonical order STANDS; no scheduler machinery.**
  The queue's total order `(tick, sub_order, actor_id, seq)`
  (SCHED-1, INV-2) is the single execution order — the sub_order
  bands and the build-time system-pass schedule (reads/writes
  topological order, `ScheduleAmbiguityError` on write-write
  ambiguity) stay the only scheduling authorities. No second ordering
  authority, no priority preemption, no work-stealing pool, no eager
  index.
- **Q4 — a parallel cohort is legal ONLY with a proof obligation.**
  No parallel execution exists today (single-threaded kernel, D-2's
  reject list standing). A cohort runs concurrently only when every
  member pair carries a MECHANICAL certificate of order-commutativity:
  disjoint write sets AND read sets not intersecting the cohort's
  writes — the scheduler's build-time discipline generalized to the
  cohort, verified at BUILD time from the pack-declared
  `reads`/`writes` (SystemDecl the certificate substrate), never
  trusted from runtime observation. The log still records the
  canonical order — parallelism is an execution detail, never a
  serialization change (Q6). FORBIDDEN: CRDT/MVCC/merge semantics
  (D-6's reject — the single-writer kernel makes them redundant),
  commutativity heuristics, benchmark-derived certifications.
- **Q5 — the measurement is the admission instrument: `world size ×
  fan-out × operation → inspected / candidate / committed + wall
  time`.** INSPECTED = entities/props/events/entries the operation's
  walk touches (exact, counted — the probe's counting proxies);
  CANDIDATE = drafts/intents/changes produced; COMMITTED = events
  through the `_commit` door (1:1 with drafts by construction);
  wall time observed (perf_counter, median — a deployment property,
  never canon, INV-2). ANY runtime-promotion claim (index, cache,
  locality rework, budget) carries this battery at ≥2 world sizes
  naming the native limit — D-11 made executable; a claim without
  the measurement is refused.
- **Q6 — locality never changes semantics: byte-identical canon.**
  Any locality mechanism (zone filter, index, cache, coarser cadence)
  leaves the canon stream byte-identical (T1, same environment) — the
  standing exemplars: the depth-3 LOD filter (L13: fewer rolls, never
  different odds), the decay interval law (the same linear drift,
  value-exact modulo the floor), `_last_change` (the baseline the
  scan would find). A locality change that shifts ANY canon byte is a
  semantic change masquerading as an optimization — RED, R3+ through
  AGENTS §8. The core-1 tie: obligation conservation (D0/D3) is
  core-1's law over future reachability; scale-1's is byte-identity
  over the canon stream — neither restates the other.
- **Q7 — the gap record: today's measured profile (the implementation
  row's RED targets; seed 4242, PYTHONHASHSEED=0, live at iter-319).**
  (a) the beat's supporting read folds are per-beat GLOBAL —
  `live_leverage` walks the whole log TWICE (32,002 iterations at
  |log|=16k, 5.9 ms/beat), `echo_scores`/`crystallized_traits` walk
  all knowers × records (2,880 at 96×30) — while the beat's demand is
  the ACTIVE ZONE; (b) the spread pass scans the ENTIRE projection
  per pass tick for a REGIONAL demand (1,053 map reads at 320
  locations for ONE burning location — linear in L, flat in fan-out
  S, committed S-shaped); (c) the decay/urgency walks are pack-wide
  per beat with the LOD filter INSIDE the walk (N records walked,
  in-zone commits only); (d) NO work budget exists in the tick loop;
  the three deferral surfaces unbounded, unaccounted. The four gaps
  close behind the gate (named consumer + the Q5 battery + a
  falsifier).

**Falsifier** (TEST_PLAN §9's packet form; run LIVE at iter-319 — the
REAL `core/` functions over the real tavern config with synthetic
scaled worlds, seed 4242, the probe outside the repo per Rule 9):
ARM A — the beat's LOCAL demand pays pack-wide walks and O(|log|)/
O(knowledge) folds (decay: inspected 36→1,248 at N=6→384, commits
4→80; leverage 502→32,002; echo 180→2,880; urgency 10→197 entries
walked). ARM B — the spread pass: B1 the world axis (inspected
108→1,053 at L=5→320 for ONE burning location — REGIONAL demand at
GLOBAL cost, review-C5 measured exact); B2 the fan-out axis (chance
1.0 probe-side: committed 3→24 = S, inspected ~flat). ARM C — the
budget/deferral inventory: C1 101 gated-off urgency entries → 0
intents, 0 events, 0 deferrals (the noise-floor law live); C2 the
uncapped beat (384 drafts in one beat); C3 the deferral exemplars
live (unbounded, unaccounted). The verbatim probe output + the
artifact md5 pins: the iter-319 report §D (the record's single
owner, D-024 — collapsed at iter-320's cap pass).

**Minimal test set** (the implementation row's, not today's): the Q5
battery as a committed counting-proxy harness (inspected/candidate/
committed pinned per operation at ≥2 world sizes — RED while the four
Q7 gaps stand); the locality-identity law — any locality mechanism
lands with the T1 corpus control byte-identical; the budget law —
exhaustion produces a visible deferral record, due work never
vanishes; the cohort law — a cohort without a build-time certificate
REFUSED (the ScheduleAmbiguityError shape); the deferral accounting —
every deferral surface carries origin and age.

**Deliberately NOT done here** (the row's own fence): no index, no
cache, no budget counter, no cohort machinery, no CRDT/MVCC, no
second scheduler (the queue stands); no pack or schema change; the
class declarations (Q1's per-mechanism map) ride the implementation
row's pack-data design — never this definition.

## 10. speech-1 — the typed speech-act channel contract (review-C8/C9/C10/C25/C26/D10; the DEFINITION landed iter-320)

> Owner-confirmed 2026-10-03 (iter-315's queue — the T6 row, the
> queue's head after the owner's «Продолжай очередь с speech-1 и так
> далее» call; Q1–Q7 accepted AS LAW the same call, §9's note). R0–R1
> definition only: NOTHING here is implemented — no channel code, no
> freeze machinery, no forgetting vocabulary, no mediator rewrite (the
> row's own law). The implementation is NOT a standing row — the
> owner opens it after accepting this contract (the runtime-promotion
> gate).

**Pinned decisions** (each grounded in standing code or law):

- **P1 — the channel enumeration, six channels, each with its live
  carrier.** (1) CANONICAL FACT — the committed event log (INV-1:
  state_changes + the knowledge/hook blocks; the writer the only
  canon-write path). (2) KNOWLEDGE-BELIEF — the per-knower records
  (L3: `who/channel/fidelity/knows/at` + the writer-stamped `source`;
  the channel enum `saw|heard|told|inferred`, EVENT_SCHEMA §3; the
  fidelity chain `exact|partial|vague`). (3) PERCEPTION — the
  ACQUISITION FACE of (2), never a second store: the visibility
  model (`rules.json::position_visibility` — sight same-location,
  hearing adjacent-vague) + the action knowledge templates
  (actions.json `knowledge` blocks) MINT the saw/heard records.
  (4) STRUCTURED SPEECH ACT — a TYPED act through the intent door:
  the pack's action grammar (talk/coerce/document_check/ramble —
  social language as pack data, INV-3), the mode-C parser's `intent`
  alternative (PARSER_SPEC §4), the mediator's IntentProposal
  (VALIDATION_SPEC §3) — the ONLY social-language-to-canon route.
  (5) NARRATION — the mediator's prose + the chronicle/tracery
  render (read-side; the L12 production form, PRESENTATION_SPEC §7;
  D-049's quarantine). (6) DIAGNOSTIC TRACE — the metrics/
  observatory/chronicle artifacts (derived, rebuildable, never
  canon). Measured live: the committed logs' observed channels
  {saw, told} ⊂ the enum.
- **P2 — free prose never canon (C25/D10).** The prose field is
  display-only by construction: the response document is CLOSED
  (`{prose, texture_delta?, proposal?}` — the unknown-key gate), the
  parser's `question`/`no_intent` alternatives surface and feed
  nothing (PARSER_SPEC §4), and the prose's world-assertions are
  CHECKED against canon (the claims, P5) — never imported by it.
  Measured live (Arm B1): a prose-only document asserting a world
  change → accepted, ZERO events, the knowledge index unchanged.
- **P3 — the promotion path (D10's pipeline, mapped): free-form
  prose → candidate structure → normal authorization → semantic
  validation → canonical event.** The candidate structure is the
  CLOSED document family (IntentProposal / the parser intent — both
  the INTENT_SCHEMA §2 grammar); authorization is the intent door
  (`validate_shape`, the preconditions, the OCC
  `based_on_event_seq`); semantic validation is the resolver circuit
  (S1's law — the sole semantic owner); the canonical event is
  `_commit`'s append. A typed speech act enters canon ONLY through
  this normal admission — never a second door, never a prose import;
  the mode-C parser path and the mode-A/B mediator path are two
  entrances of the SAME door (INTENT_SCHEMA §9's conversion). auth-1
  (D9) owns the INPUT-side pipeline vocabulary; speech-1 pins the
  CHANNEL laws — the two never contradict (the S3 fence's twin).
  Measured live (Arm B2): the content B1's prose carried, typed as
  a `talk` intent → the door commits (`talk` + the telling
  reaction's `rumor_told` — two canonical facts from one typed
  act).
- **P4 — channel isolation: an admitted structured act is FROZEN
  against presentation retries (C8); today the boundary is ABSENT —
  the measured gap.** The law for the future row: a
  PRESENTATION-side defect (prose shape, the invented-entity floor,
  a contradicted prose claim) must never invalidate, mutate, or
  silently reopen an already-admitted structured act — the
  presentation retries the presentation; conversely a structured-act
  refusal never touches canon (the prose was never canon, P2). TODAY
  (measured, Arm A): the response document is monolithic — an empty
  prose kills the delta+proposal at the parse gate (A1:
  NarratorError, the structured half never reaches its gates); a
  contradicted prose claim regens the WHOLE exchange, the valid
  intents half dying with ZERO trace (A2: 0 events, 0 withdrawal
  notes, 0 deferral records), the re-delivered document free to
  carry a different structured half (no freeze constraint); the
  accepted delta items staying applied across regens (the gateway's
  idempotent duplicate rule) is the one standing partial-survival
  exemplar. Freeze machinery: 0 hits (A3).
- **P5 — grounding scoped to ATOMIC externally-testable assertions
  (C9); the closed halves referenced, never restated.** The claim
  kinds are the closed set `state|knowledge|event` (VALIDATION_SPEC
  §3 — additive kinds a spec edit, never silent); verdicts run
  against CURRENT canon (the honest-verdict law, §4); the prose-side
  twins: the invented-entity floor (§2.1) and the lowercase
  assertion surface (`relation_attribute_tokens` — a measurement
  export, never a gate, D-096). What the vocabulary cannot express
  it does not ground: metaphors, tone, word-by-word token grounding
  are OUT OF SCOPE by construction — the refusal is the
  vocabulary's shape, never a per-prose judgment.
- **P6 — the epistemic scope law: four scopes; dramatic irony is a
  READ-side composition, never a write-side fact (C26).** ACTOR —
  the per-knower records only (the fold IS the memory,
  `records_of`); the acceptance roll reads only the listener's own
  trust + the teller's own status (EPIST-1, the Influence
  Boundary); a record the knower does not hold can never render in
  their brief (mode B's leak surface, by construction). PLAYER —
  the mode-A brief's bytes. NARRATOR — the call document, nothing
  beyond (D-049); the prose may only assert what the document
  carried (P5's checks enforce it). DEBUG — the observatory/
  chronicle read-side: everything visible, nothing writable.
  Dramatic irony lives ONLY in the debug/read composition (a reader
  seeing several scopes at once); NO canon channel ever mixes
  scopes — an NPC never draws on another's records, the narrator
  never sees past the document, the fold never mints cross-knower.
  Measured live (Arm C1): the player doc + the actor docs (the
  chorus drain) each carry ONLY their knower's rows; the pc-only
  and barkeep-only tokens never leak.
- **P7 — the explicit forgetting vocabulary (C10) + the epistemic
  field homes.** TODAY no forgetting exists — the fold is
  append-only acquisition; measured live (Arm C2): 10,000 ticks
  later NO holder ever dropped a token (acquisition continued).
  Forgetting, when a named consumer requires it, is EXPLICIT: new
  events (INV-5 — never an edit), a declared vocabulary (a `forgot`
  record family or a pack-declared TTL — the design is the
  implementation row's), and a derived cache may evict for cost but
  NEVER changes the semantic answer (`holds` stays the fold's). The
  C10 field homes: proposition = `knows`; source = the minting
  event id (writer-stamped, L3); acquired_at = `at`; fidelity =
  the chain; trust = the relations/pair axes (read per-pair by
  `trust_toward` — NEVER a record field); status = the read-side
  verdict family (supported/contradicted/insufficient_data —
  computed per claim, NEVER stored belief state). No generic belief
  graph (the reject list; the docstring 'belief' prose is
  vocabulary, the module absent).

**Falsifier** (TEST_PLAN §9's packet form; run LIVE at iter-320 —
the REAL Simulator/Mediator/validator/ledger/knowledge over the
real tavern pack, seed 42, the probe outside the repo per Rule 9;
the verbatim output + the artifact md5 pins: the iter-320 report
§D, the record's single owner): ARM A the C8 freeze gap — A1 the
empty-prose kill at the boundary (NarratorError, the structured
half never gated); A2 the monolithic regen (the valid take intent
died with a contradicted prose claim: 0 events / 0 withdrawals / 0
deferrals; the re-delivery unconstrained); A3 the freeze
vocabulary 0 hits (`frozenset` the false friend, 74 — none
machinery). ARM B the prose/canon boundary BOTH ways — B1
prose-only → 0 events, the knowledge index unchanged; B2 the same
content typed as `talk` → `talk`+`rumor_told` committed; B3 the
observed channels {saw, told} ⊂ the enum {saw, heard, told,
inferred}. ARM C the scope + forgetting — C1 the player + 2 actor
documents, each knowledge block ⊆ its knower's records, zero
cross-knower leaks; C2 no holder ever dropped a token across
10,000 ticks, the forgetting vocabulary ABSENT.

**Minimal test set** (the implementation row's, not today's): the
freeze law — a presentation-defect document with a boundary-valid
structured half feeds or withdraws the structure loudly while the
presentation retries (the A1/A2 arms RED→GREEN); the
prose-never-canon control (B1) and the typed-act route (B2) stay
green; the scope law — the mode-B documents pinned per-knower (the
C1 arms as committed fixtures); the forgetting vocabulary — an
explicit-forget event flips `holds` through the fold (INV-5: a new
event, never an edit; a cache eviction NEVER flips `holds`); INV-2
— byte-identical replay over a run whose exchanges include frozen
acts (the protocol changes, never the canon stream).

**Deliberately NOT done here** (the row's own fence): no mediator
code rewritten, no channel code, no freeze machinery, no
speech-act admission family, no forgetting mechanism, no schema or
pack change (the row's R0–R1 law).

## 11. auth-1 — the intent / agency / director boundary contract (review-C11/C12/C20 + M4's vocabulary/D7–D9; the DEFINITION landed iter-321)

> Owner-confirmed 2026-10-03 (iter-315's queue — the T7 row, the
> queue's LAST row, opened by the owner's «Продолжай очередь с
> speech-1 и так далее» continuation; Q1–Q7 accepted AS LAW the same
> call, §9's note). R0–R1 definition only: NOTHING here is
> implemented — no pipeline code, no authority registry, no director
> or mediator machinery (the row's own law). The implementation is
> NOT a standing row — the owner opens it after accepting this
> contract (the runtime-promotion gate).

**Pinned decisions** (each grounded in standing code or law):

- **A1 — the pipeline, five stages, each with its live carrier
  (D9's input side).** INPUT — the player's free text (mode C:
  `ParserDoor.emit_call`), the narrator reply document (mode A/B:
  `Mediator.apply_reply`), the playscript steps (`run_steps`), the
  autonomous producers (urgencies / the director — through the SAME
  door). INTERPRETATION — the parse into the typed candidate: the
  closed gate accepting EXACTLY ONE of `intent|question|no_intent`
  (`brief/parser.py`, PARSER_SPEC §4) / the proposal document
  (`brief/validator.py`, VALIDATION_SPEC §3). CLASSIFICATION — the
  kind/target/fields against the pack's action grammar
  (`PACK.action`, the snapshot's verbs/nouns — INV-3: the grammar
  is pack data). AUTHORIZATION — the intent door: `validate_shape`
  (the loud shape half) + the closed precondition test set
  (`core/intent.py`) + the OCC `based_on_event_seq`. EXECUTION —
  the resolver circuit + `_commit` (S1's law; INV-1's writer).
- **A2 — valid ≠ authorized; three DISTINCT axes with distinct
  refusal vocabularies.** SHAPE-VALID (the grammar/gate families)
  is not WORLD-LEGAL (the door's preconditions/OCC) is not
  COMMITTED (the execution). Malformed → the LOUD family
  (RunnerError/ParseError/ProposalError), ZERO events — nothing in
  the world; well-formed but world-impossible → the committed
  `intent_rejected` no-op (an attempt IS a fact, PARSER_SPEC §4/§5
  — the noise floor's commit-side twin); valid+authorized → the
  event, INV-5-immutable. Measured live: all three axes (Arm A).
- **A3 — the authority classes, INPUT-side (D9's list): player |
  NPC | director | system | pack.** PLAYER — the mode-A/C caller,
  the playscript actor. NPC — mode B's caller gate (a reply
  proposes its own caller's actions ONLY — `feedable_intents`;
  measured live, Arm B1) + the urgencies' per-NPC templates.
  DIRECTOR — the released hooks' payloads through the door
  (`origin_hook` provenance, D-140). SYSTEM — the mechanic
  producers (world/genesis/clock/weather/economy — emissions, not
  intents). PACK — the seeded hooks, follow-ups, expectations (pack
  data as origin). S3 (sem-1) owns the EMIT-side vocabulary; A3
  owns the INPUT side — the two never contradict (the namespace
  fence, the package's §5).
- **A4 — ambiguity collapses ONLY on equivalent canonical effect
  surfaces (D9); NO global confidence score.** Auto-collapse is
  legal only when the candidate interpretations map to an
  EQUIVALENT canonical effect surface (S2's declaration form); any
  other ambiguity → CLARIFY (the parser's `question` alternative —
  measured live, Arm C1: the question surfaced, nothing fed) or
  REJECT. A global confidence/risk/truth number is FORBIDDEN
  (measured: zero machinery, Arm A4/C2). Today no collapse
  machinery exists — the collapse is the implementation row's, with
  its equivalence proof.
- **A5 — the D7 invariant: `DirectorOutput ⊆ EligibleConsequences(
  world, pack, current_state)` + the mutation probe.** The eligible
  set IS the seeded-hook buffer (pack-declared hooks seeded at
  event time, D-005 — measured live: 5 instances over the day1
  run, each with its pack-declared payload); the release paths
  (explicit triggers / the quiet path / the climax layer) only
  SELECT from the buffer under the pacing budget (1 release per
  beat) and the pure option choice (no RNG — a function of (pack,
  projection, beat_tick)); releases ride the intent door (D-037)
  with `origin_hook` provenance. The director NEVER invents entity,
  motive, goal, cause, or fact. The mutation probe's standing form:
  (i) an invented KIND dies loud at the door (`PACK.action` → None
  → the loud RunnerError — measured live, Arm B2c); (ii) an
  unseeded consequence has NO release path (no release-by-tag API;
  the buffer is the only source — the Director's public surface,
  Arm B2b); (iii) the emit-side authority check is sem-1's S3/S5.
- **A6 — bounded deterministic agency where a named consumer needs
  it (D8); NO generic planner, NO LLM planner.** The standing
  carriers: the urgencies (per-NPC goal specs, d100 per beat on
  isolated streams, the precondition gate, the silent noise floor
  — PARSER_SPEC §4/§6), the crystallized traits (the read-side
  lens), the grudge/debt families. Selection stays bounded,
  deterministic, and persistent only behind a named consumer; a
  generic planning engine or an LLM planner is on the review's
  reject list (VISION §6 — the Generative-Agents cost
  anti-precedent). The through-the-door discipline (D-037):
  autonomous intents broadcast objectives through the SAME door
  the player's intents use — one mechanism, never two.
- **A7 — the M4 vocabulary + HARD CANON (the owner's 2026-10-03
  decision, iter-315's record): the model-path contract.**
  INSTRUCTION — the prompt-side directives (the call document's
  protocol lines; never canon). PROPOSAL — the typed candidate
  (the IntentProposal / the parsed intent). AUTHORITY — the door's
  authorization (A1/A2). REALISED INTERVENTION — the committed
  event. CANONICAL CONSEQUENCE — the fold's downstream effects.
  The HARD-CANON law: a wrong-but-committed model-mediated action
  is INV-5-immutable — NO recovery/dispute path EVER; the
  correction form is a NEW event, never an edit; a retcon path
  would need a new owner-gated design — REFUSED by the standing
  decision. Measured live: the writer's public surface is
  append/close only (no edit, no undo, no retcon — Arm B3; zero
  machinery hits).

**Falsifier** (TEST_PLAN §9's packet form; run LIVE at iter-321 —
the REAL Simulator / Mediator / ParserDoor / intent door /
director / writer over the real tavern pack, seeds 42 + 8 (the
day1 corpus), the probe outside the repo per Rule 9; the verbatim
output + the artifact md5 pins: the iter-321 report §D, the
record's single owner): ARM A the pipeline + the three axes — A1
the world-impossible `talk` → `intent_rejected` committed
(ev_0006, zero state changes, the world unchanged); A2 the unknown
kind `seduce` → the loud RunnerError, ZERO events; A3 the valid
`move` → committed; A4 the confidence/risk/truth-score machinery:
0 hits. ARM B the authority + D7 + M4 — B1 the guard's actor reply
proposing the player's talk → WITHDRAWN ("a reply proposes its own
caller's actions only"), 0 fed, the note riding the player's next
call; B2 the eligibility set enumerated (5 seeded instances) + the
Director's public surface (seed/releases/next_beat — no
release-by-tag API); B2c the invented `spawn_dragon` → `PACK.
action` → None → the door's loud refusal; B3 the writer's surface
append/close only, 0 retcon/undo/rewrite hits. ARM C the ambiguity
law — C1 the `question` alternative surfaced, ZERO events fed; C2
the effect-equivalence/auto-collapse machinery: 0 hits.

**Minimal test set** (the implementation row's, not today's): the
three-axis pipeline arms as committed fixtures (the rejection
event, the loud malformed, the committed valid); the caller-gate
arms (the foreign-actor withdrawal, mode A and B); the D7 mutation
probes (the invented kind RED at the door; the unseeded-tag
release REFUSED at the API shape); the collapse law — a collapse
carries its effect-surface equivalence PROOF, otherwise the
question path (C1 green); the M4 immutability — the writer stays
append-only (the architecture pin); INV-2 — the director's pure
selection (same log → same releases).

**Deliberately NOT done here** (the row's own fence): no
director/mediator runtime machinery, no pipeline code, no authority
registry, no collapse implementation, no schema change (the row's
R0–R1 law).
