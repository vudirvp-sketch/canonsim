# STATUS — canonsim

Iteration: 0u (owner-requested: references distillation — the synthesis pass over the whole reference corpus; no new external source: the owner's request is the trigger, satisfying D-022's "no further docs iterations without a fresh owner request") · Phase: 0 — simulator without LLM · Date: 2026-08-27

iter-0u is the **reference distillation** the owner requested: process
every reference deep dive and assemble it into one contradiction-free
construction plan. Deliverable: `docs/BLUEPRINT.md` (method + resolution
ledger + cross-cutting laws + build index) + `docs/blueprint/phase0.md`
(iter-1..6 combined donor designs) + `docs/blueprint/phases.md` (phases
1–6 architecture + cross-cutting) — decision D-027; 9 files touched (the
3 new files + the mandated sync set: AGENT_NAVIGATION §1/§2/§3,
DECISIONS, REFERENCES_DEEP pointer, TASKS, STATUS, worklog).

**What the distillation is.** The fourth place of the anti-drift system:
catalog (`REFERENCES.md`) ↔ one-line synthesis (`CORE_DESIGN_RESEARCH.md`
§2) ↔ deep dives (`docs/ref/`) ↔ **blueprint** (cross-reference
resolutions + donor combinations, organized by build component, not by
source). The blueprint owns the *resolutions* — new facts created by
synthesis; every mechanic cited stays owned by its per-ref file, linked.
Maintenance protocol: a future deep dive updates only the ledger rows and
part-file sections it changes, at deep-dive time (BLUEPRINT §0).

**The twelve resolutions** (full table: `docs/BLUEPRINT.md` §1):
RNG-1 single RngBank authority with deterministically seed-derived named
streams (Brogue/DCSS discipline inside INV-2's intent; replay
fingerprint for T1) · TIME-1 all timing reduces to SCHEDULED / SEEDED /
SAMPLED — MTTH is the named anti-pattern · STATE-1 the projection IS the
storage (entt layout + views; Bevy double-buffer = tick boundary; writes
only via log append) · SCHED-1 one heapq, `(tick, sub_order, actor_id)`
with sub_order bands + build-time ambiguity check · EPIST-1 Influence
Boundary + embodiment mapping + expectation-mismatch `inferred` records
+ Price markers · DIR-1 director reads observables only; entropy floor
sensor; objective broadcast; three named negatives (from-nothing,
player-learning, canon-softening) · BRIEF-1 block pipeline with the
retrieval split (dynamic facts never vector-searched) · PACK-1 the pack
ladder with lint as the top rung · CHRON-1 event-vs-tale split +
deterministic tracery · STORE-1 the storage ladder, each rung
rebuildable · TEST-1 the verification stack (fingerprints, seed
catalogs, single-factor A/B, 7-hole crosswalk) · LOD-1 the LOD ladder
(crowd entity is the seed already in the pack).

**Two standing clarifications enacted** (D-027, both recorded as ledger
rows with rationale): RNG-1 clarifies INV-2's "one `random.Random(seed)`
instance" as *single point of randomness control* — named streams
derived from the master seed keep byte-identical replay and add the
cosmetic-stream isolation Brogue/DCSS prove; EPIST-1 adopts the
Influence Boundary (live-char-guide) as the default iter-2/3 design —
flagged owner-call in iter-0t, adopted by this distillation, vetoable
at the iter-3 design gate.

**Doc-loop accounting:** 20th consecutive docs iteration. No fresh
external source this time — the exception rests on the owner's explicit
request alone (D-022 wording satisfied). The alarm condition stands:
**iter-1 is unconditionally the next iteration** — no further ref-N, no
spec writing, no doc polish without a fresh owner request.

**iter-0t closing summary** (full detail: git history + worklog entry):
ref-13 live-char-guide deep dive delivered (`docs/ref/live_char_guide.md`:
SPINE/Price/observability, brief-layer injection grammar, AP→pack-lint
vocabulary; license clean MIT). All ref-N backlog items complete
(ref-1..ref-13 + the iter-0h cousins).

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index.
- INV-2 Determinism: single seeded RNG, no wall-clock, `sorted()` iteration,
  fixed `PYTHONHASHSEED`, queue key `(tick, sub_order, actor_id)`
  (clarified by D-027/RNG-1: single RngBank authority, named derived
  streams).
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#3 · `expectation_violation` primitive missing — NPC reacts only to presence in `knowledge`, not to absence (purse gone, guard missing). Fix: P2d in `CORE_DESIGN_RESEARCH.md` §6, slated for iter-3; resolution recorded as ledger row EPIST-1 (`docs/BLUEPRINT.md` §1).
- KI#4 · balance harness (1000-sim distribution plots of `suspicion` / `fire_spread`) missing — MVP_SCOPE §15 promises an iter-6 baseline but no tool exists. Added as `balance-1` in `docs/TASKS.md` infra backlog; folded into the iter-6 verification stack (`docs/blueprint/phase0.md` §6).
- KI#5 · runtime state vs test fold not explicitly separated — risk of O(N²) at startup if `fold(log)` is misused as runtime path. D-023 records the rule: runtime = incremental projection; fold = T2 replay only; resolution recorded as ledger row STATE-1.
- KI#7 · Capped-memory drift (2026-08-27): `worklog.md` entries up to ~880 lines vs the 3–5-line law; `TASKS.md` at 1136 with done entries not one-line-collapsed — trim vs migrate needs an owner call (D-025 covers `docs/*.md` caps only, not these rows).

## FAQ / Pitfalls

- **Zip upload loses dotfiles and empty dirs.** "Add files via upload" on GitHub
  dropped `.gitignore` (and every dir without tracked files). After any future
  upload: verify `.gitignore` exists and `git status --short` shows no runtime
  artifacts (KI#1).
- **Workspace files ≠ tracked files.** `git status --short` shows changes
  *vs HEAD*, not what is *in HEAD* — a file present in your working directory
  may not be committed at all. After any structural change, run
  `git ls-files <path>` (or `git ls-files | head -50`) to confirm what is
  actually tracked. This is the diagnostic for KI#1-class losses and for
  "the file exists but tests can't find it" surprises.
- **Doc-loop alarm vs owner-requested research.** Twenty docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested passes
  are the explicit exception (D-022) — the documented condition is a fresh
  owner request (iter-0s/0t additionally had fresh external sources;
  iter-0u, the distillation, rests on the request alone). iter-0u is the
  twentieth docs iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j,
  0k, 0l, 0m, 0n, 0o, 0p, 0q, 0r, 0s, 0t, 0u; iter-0d was infra). All
  ref-N backlog items are complete — ref-1 through ref-13 plus the
  iter-0h cousins; no further ref-N iterations remain without a fresh
  external source, and no doc pass at all without a fresh owner request.
- **Four places, four jobs (D-027).** `docs/REFERENCES.md` catalogs sources
  (license, URL, phase gating); `docs/CORE_DESIGN_RESEARCH.md` §2 carries
  the one-line synthesis per source; `docs/ref/<source>.md` carries the
  concrete mechanics; `docs/BLUEPRINT.md` + `docs/blueprint/` carry the
  cross-reference resolutions and donor combinations per build component.
  Drift rule: link, never restate; cite ledger row IDs (e.g. "per RNG-1")
  instead of re-deriving a resolution. The old STATUS "Next step" prose
  mapping of refs → iterations was exactly this drift and has been folded
  into the blueprint build index (`docs/BLUEPRINT.md` §3), its single
  owner.
- **Substance over line count (D-025) + per-ref split (D-026).** The cap is
  600 with the §6.1 substance filter as the real law — filler is cut
  always; named systems, real field lists, type enumerations, per-source
  verdicts are never cut to fit. The iter-0l..0r per-ref files run
  101–605 lines each, each under cap by construction or §6.1-justified;
  the iter-0u blueprint files are 149/340/224 lines — under cap by
  construction.
- **License drift between catalog and index (KI#6, closed iter-0n; pitfall
  persists).** The `REFERENCES_DEEP.md` §2 index table is **not** the source
  of truth for licenses — `REFERENCES.md` (the catalog) is. Diagnostic:
  before flipping any ref-N row todo→done, grep the source row in
  `REFERENCES.md` and verify the license column matches the index entry.
  The standing pre-flip check is exercised across iter-0o/0p/0q/0r/0s/0t;
  iter-0u touched no ref rows, so no check was needed this iteration.

## Next step

**iter-1 · core plumbing** — unconditionally the next iteration (functional
code, not docs). Read before building: `docs/blueprint/phase0.md` §1 (the
combined donor design: RngBank, heapq queue with sub_order bands, JSONL
writer with cause-chain integrity, fold vs incremental projection, pack
loader) + `docs/BLUEPRINT.md` §1 ledger rows RNG-1/SCHED-1/STATE-1/STORE-1/
TEST-1 + `MVP_SCOPE.md` §8 + `docs/TASKS.md` iter-1 acceptance criteria.
The full ref→iteration donor mapping now lives in the blueprint build
index (`docs/BLUEPRINT.md` §3) — it is no longer restated here (D-027).
