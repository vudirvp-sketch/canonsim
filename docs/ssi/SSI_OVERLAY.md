# SSI_OVERLAY.md — the SSIEC-v3 → canonsim control plane (ssi-2/D-222)

> The ONE authored file over the READ-ONLY reference copy (`docs/ssi/`).
> Law: this overlay MAPS the SSI blocks onto canonsim's existing
> mechanisms — it never restates them, never replaces them, never
> becomes a second source of truth (D-024's one-owner law). The
> reference copy is verbatim (md5 305952c10b0997236b93d3c77c2b7681 of
> the source zip, 147249 bytes, 34 files) and read-only: the ONLY file
> ever edited under `docs/ssi/` is this one. Entry points into the
> package: `AGENT_ENTRY.md` (the hard protocol), `00_INDEX.md` (the
> A–L block index), `controls/*.yaml` (the machine-readable policies),
> `templates/*.md` (the record forms). Risk ladder + PCC: AGENTS.md
> §2.9 (the binding home). docguard lints every table below
> (SSI-N006/N007/N010/N017/N018 — the shapes ARE the executable).

## 0. How to use this overlay

1. Classify the change's risk class (§3 / AGENTS.md §2.9) BEFORE
   planning the iteration. R0–R2: the standing protocol, nothing
   added. R3+: the closing DECISIONS row self-declares the class and
   carries the PCC record (§4).
2. Every block/rule/phase row below carries an explicit State from
   the closed vocabulary `NOT_APPLICABLE | OPEN | PARTIAL | VERIFIED
   | WAIVED` — an absent row or an out-of-vocabulary state is a
   violation, never a silent skip (SSI-N006/N007; the guard's own
   docguard family).
3. `WAIVED` is never implicit: `owner= reason= expiry=` required.
   `NOT_APPLICABLE` requires `reason=` (the package's own
   anti-skipping laws, README + AGENT_ENTRY hard protocol 4).
4. The external analysis's numbers anywhere in this overlay (the
   god-object line counts, the co-change hypotheses) are HYPOTHESES
   for ssi-3 to re-verify — never facts, never material_gap on their
   own (SSI-N018).

## 1. The block matrix (A–L → the existing mechanisms)

| Block | SSI core question | canonsim mechanism | State | Evidence |
|---|---|---|---|---|
| A | Core baseline — what does the system mean? | AGENTS.md §4 (INV-1..5) + docs/EVENT_SCHEMA.md + schemas/event.schema.json + core/log.py + core/fold.py | VERIFIED | the 2-place schema sync (test_t0_schema); D-221's freeze is this initiative's boundary |
| B | Topology — what actually changes together? | tests/test_architecture.py (the import boundary, D-031) + docs/SSI_TOPOLOGY.md (the ssi-3 map: owner/reads/writes/emits/co-change, drift-pinned by scripts/topology.py) | VERIFIED | the map + the co-change/trajectory audit landed (D-224): the #1 code pair loop.py↔pack.py is HISTORICAL coupling (iter-90..168, dormant since, pack decomposed) — a line-count snapshot alone was never the evidence (N018 upheld) |
| C | Complexity — how large is the semantic state space? | AGENTS.md §6 (the cap table, docguard-enforced) + core/packlint/ (the content budgets) + the (tick, sub_order, actor_id) queue key's bounded order | PARTIAL | the doc/pack budgets executable at HEAD; ssi-3's map (docs/SSI_TOPOLOGY.md) delivered the complexity DATA (sizes, read-degree, the 32-import loop hub) — the core/ complexity BUDGET itself stays unset until an owner call names one |
| D | Formal verification — which claims need model-level proof? | none | NOT_APPLICABLE | reason= the stdlib-first core carries no model checker and adds none (AGENTS §10); the practical form is the determinism envelope (T1 byte-identical + the RNG fingerprint, TEST_PLAN §1.1); TLA+/TLC stays a reference anchor per controls/manifest.yaml |
| E | Static semantics — can the rule be enforced before runtime? | tests/test_architecture.py + tests/test_inv3_stoplist.py | VERIFIED | the stdlib-ast invariants + the segment-matched stoplist; N001/N002 widened the family (D-223) |
| F | Testing — can the claim be falsified? | docs/TEST_PLAN.md (T0–T8 + M1–M5 + §9 the claim packets) | VERIFIED | the standing stack + the mutation-probe family (a golden byte-diff over a mutated pack copy) |
| G | Runtime control — how is degradation bounded? | docs/WORKBENCH_APP_LAW.md (the four lifecycle machines, §12's deadlines, §25's bounded stop) | VERIFIED | the dispatch/failure matrices + the KI#95 cooperative-cancellation poll law |
| H | Agent governance — what may the agent do and know? | AGENTS.md itself (§2 the iteration protocol, §5 the KI lifecycle, §8 stop-and-confirm, §11 authority, §12 the handoff law) | VERIFIED | the repo's own capability contract; controls/agent-capabilities.yaml stays REFERENCE — its defaults already hold here (read-only fs, no push, explicit gates on CI) |
| I | Evolution — how do we change/remove safely? | docs/DECISIONS.md (append-only, supersede-don't-delete) + AGENTS.md §7 (git safety) + STATUS.md (the KI lifecycle) | PARTIAL | the PCC/deletion forms below arm the ssi phases; the full gc-gate fires with ssi-8 (Phase 7) |
| J | Provenance — can the artifact be traced/reproduced? | the log header (seed/python/scheduler) + the RngBank fingerprint + AGENTS.md §12 (BASE_COMMIT delta archives, md5 + byte size on both channels) | VERIFIED | TEST_PLAN §1.1's env-pinned replay + §12.1's self-check protocol |
| K | Operations — was every block applied or explicitly skipped? | worklog.md + docs/TASKS.md (the ledger) + STATUS.md (the stop-point report) + scripts/docguard.py | VERIFIED | the capped state layer + the guard; this overlay's own lint is the family's newest member |
| L | Frontier — which expert mechanisms strengthen construction and proof? | the PCC record (§4) + T1's deterministic replay + the risk ladder (AGENTS §2.9) | PARTIAL | PCC armed for R3+ (N017); the semantic-diff layer rides ssi-7 (Phase 6); deterministic simulation testing = the T1/T2 replay discipline already standing |

## 2. The executable negative-rules subset (D-223 — the owner's chosen eight)

| Rule | Name | Instrument | State | Findings at HEAD |
|---|---|---|---|---|
| SSI-N001 | no-hidden-effect | tests/test_architecture.py | VERIFIED | none — the canonical kernel imports no wall-clock/entropy root (the check green at landing) |
| SSI-N002 | no-new-primitive-without-gap | tests/test_architecture.py | VERIFIED | sim/ carried no NAV §1 owner row — landed with D-223 (the admission-completion fix, not a waiver) |
| SSI-N006 | no-silent-block-skip | scripts/docguard.py | VERIFIED | none — the block matrix complete, every state explicit |
| SSI-N007 | illegal-states-unrepresentable | scripts/docguard.py | VERIFIED | none — the states ride the closed vocabulary; a typo'd state goes RED |
| SSI-N010 | no-semantic-drift-without-delta | scripts/docguard.py | VERIFIED | none — every instrument claimed below exists on disk at HEAD |
| SSI-N017 | proof-carrying-change | scripts/docguard.py | VERIFIED | the D-221/D-222/D-223 rows carry their PCC records — the live shape, not a vacuous gate |
| SSI-N018 | no-architecture-health-from-snapshot | scripts/docguard.py + scripts/topology.py | VERIFIED | the FULL trajectory audit fired with ssi-3 (D-224): the map doc carries the dated co-change/trajectory evidence pinned to BASE_COMMIT, scripts/topology.py --audit regenerates it at any HEAD, --check drift-pins the mechanical columns, and the verdict table records the external numbers as CONFIRMED-numeric/REFUTED-as-live-coupling — exactly the snapshot-vs-trajectory distinction this rule exists for |
| SSI-N020 | no-deletion-without-constraint-recovery | docs/ssi/SSI_OVERLAY.md | OPEN | the deletion card (§5) is the form; the gc-gate fires with ssi-8 (Phase 7) — apparent inactivity is never evidence |

> The other twelve rules (N003–N005, N008, N009, N011–N016, N019) stay
> REFERENCE-ONLY: each opens on the owner's explicit call (the same
> ladder as the phases below). Mapping them now would be machinery
> without a consumer (AGENTS §2.8's admission law).

## 3. The risk ladder (AGENTS.md §2.9 — the binding home)

R0 text/style only · R1 local pure refactor · R2 local behavior
change · R3 cross-boundary or dependency change · R4 state/authority/
schema/public-API change · R5 security/distributed/irreversible/
external-contract change.

- R0–R2: the standing protocol (AGENTS §2), zero added bureaucracy —
  no recorded class needed; the 3–5-file soft limit stays the sizing
  law (this ladder refines it, never replaces it).
- R3+: the closing DECISIONS row self-declares `(R3)`/`(R4)`/`(R5)`
  and carries the PCC record (§4); docguard lints the shape (N017).
- Escalation factors (controls/risk-classes.yaml): blast radius,
  irreversibility, privilege, uncertainty, work amplification,
  external contract — any two present → consider one class up.

## 4. The PCC record (the DECISIONS-row form, SSI-N017)

Adapted from templates/proof-carrying-change.md to the DECISIONS row
— NEVER a separate file per change (the owner's ssi-1 call):

```text
(R3) [PCC: intent=<one line>; invariants=<which hold / which are
touched>; delta=<the semantic delta — files class, behavior class>;
verification=<the run evidence — counts + instruments>;
provenance=<the inputs — owner call, base commit, external sources>;
runtime=<rollout/rollback plan or "none — doc-only">]
```

docguard's N017 lint: a DECISIONS row carrying `(R3)`/`(R4)`/`(R5)`
must contain all six field markers — `intent=`, `invariants=`,
`delta=`, `verification=`, `provenance=`, `runtime=`. The full
49-line template (the long form, for R4/R5 and the compositional
fields) stays in the reference copy at
docs/ssi/templates/proof-carrying-change.md.

## 5. The deletion card (SSI-N020's form — fires with ssi-8/Phase 7)

```text
[GC: target=<path or id>; consumer_absence=<the scan/grep evidence>;
authority_absence=<the owner/decision check>; historical=<the
constraint check — why it existed, what changed since>;
recovery=<the rollback or reconstruction path>]
```

Apparent inactivity is NEVER deletion evidence; INV-5's log
immutability and DECISIONS' supersede-don't-delete stay the law.

## 6. The phase ladder (owner-gated beyond Phase 1)

| Phase | Track row | Scope | Gate | Evidence bar |
|---|---|---|---|---|
| 0 | ssi-1 | the architecture freeze | CLOSED iter-241 | D-221 — the eight public-contract surfaces confirmed at their standing owners |
| 1 | ssi-2 | the SSI foundation | CLOSED iter-242+243 | the green suite + this overlay's own docguard lint (the shapes ARE the executable) |
| 2 | ssi-3 | the ownership/topology audit (core/, workbench/) | CLOSED iter-244 | D-224 — the map (docs/SSI_TOPOLOGY.md) + the co-change/trajectory audit: line counts CONFIRMED exactly; loop.py↔pack.py the #1 code pair numerically (11×, lift 9.07) but HISTORICAL (iter-90..168, dormant since, pack decomposed 3990→290 via packlint) — ssi-5's core scope SHRINKS on the refuted live coupling, ssi-4's target CONFIRMED as the active hotspot |
| 3 | ssi-4 | the workbench/application/inference.py → inference/ package split | CLOSED iter-247+248+249 | the ssi-3 ownership map + the LAW's §2 semantic owners (the split by owners, never an external template; the public import surface + the gateway ops + the claim packet byte-stable; 2511 → 10 owner modules + the 176-line pure re-export facade, D-225/D-226/D-227 the PCC records) |
| 4 | ssi-5 | the core strangler (loop/director/worldgen/intent) | owner-gated | co-change evidence from ssi-3 + the public-interface freeze (director.next_beat(...) et al. byte-stable; each step an R2/R3 iteration with its PCC record) |
| 5 | ssi-6 | the canonical read seam (core ↔ workbench read-side) | CLOSED iter-250 | INV-4's sanctioned-module pattern LANDED (D-228, the owner's «продолжай работу» go-ahead over the confirmed Phase 3 closure): `workbench/canonical_read.py` the ONE workbench core-import module — a pure re-export shell over the 10-name read surface; the map's three consumers (scene_build/observatory_read/scene_ir) migrated at zero behavior change; the law executable twice over (test_architecture's import ban + the seam's watchlist reads pin) |
| 6 | ssi-7 | the semantic diff layer over T1 | owner-gated | event ids/types/causes/actors/targets/RNG-fingerprint comparison — interpreter/line-ending independent; an ADDITIONAL layer, never a T1 «bug fix» (env-pinning is a documented decision, TEST_PLAN §1.1) |
| 7 | ssi-8 | the GC pass over stale artifacts | owner-gated | the deletion card (§5) per artifact; KI#99's doubled workbench/workbench/runtime/ tree is a candidate |

> Phases 2–7 each open on the owner's separate explicit call, after
> the previous phase closed and the owner confirmed the result. The
> standing refusals (the owner's ssi-1 call): no big-bang rewrite of
> core/, no SSI as a runtime dependency (no core/ssi.py, no
> IntegrityManager), no new top-level control directory, no touching
> core/log.py, core/rng.py, core/schema.py, or the fold mechanics in
> this initiative.
