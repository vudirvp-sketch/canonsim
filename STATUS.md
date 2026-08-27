# STATUS — canonsim

Iteration: 2a (`iter-2a-code-audit`) · Phase: 0 — simulator without LLM ·
Date: 2026-08-28

Owner-requested audit of the first two code iterations ("re-check iter-1/2
before the complexity grows"): full read of `core/` + tests + pack +
contracts against the blueprint, claims verified (148 green, ruff clean,
golden fixture intact), then probe-driven bug hunting. Four KIs found and
fixed in place: KI#13 `_drop` hardcoded `from_=None` desynced the
projection on a legal retake-and-redrop of a broken item — and exposed
that events were written before their state deltas were validated (the
new `_commit` gate validates first, D-035; both baseline logs stayed
byte-identical); KI#14 `next_log_path` could name a live log after a
middle delete and the writer would truncate it; KI#15 pack-lint gaps
(`use_effect` axis, knowledge/events branch consistency, bare
`StopIteration` in the steal resolver); KI#16 two staggered fires forked
parallel spread passes — double `chance_per_tick` and a `cause=None`
crash mid-run (seed 19 reproducer); the pass is now a per-layer
singleton with a shared cause map (D-036). Repeat smoke/burnout
follow-ups now stay silent instead of duplicating chronicle lines.
155 tests green (+7 regression), ruff clean; `intent OCC` (KI#12)
confirmed structurally unreachable in single-actor runs — KI stays open
until an e2e trigger exists.

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index; the log writer is the
  only canon-write path (D-031).
- INV-2 Determinism: single point of randomness control — one master seed;
  named streams derived via the RngBank (`stable_hash` = sha256-based);
  no wall-clock; `sorted()` iteration; fixed `PYTHONHASHSEED`; queue key
  `(tick, sub_order, actor_id)`; cosmetic draws never desync canon replay
  (D-028 — the law text itself now carries this; AGENTS.md is the single
  reading owner).
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#3 · `expectation_violation` primitive missing — NPC reacts only to presence in `knowledge`, not to absence (purse gone, guard missing). Fix: P2d in `CORE_DESIGN_RESEARCH.md` §6, slated for iter-3; resolution recorded as ledger row EPIST-1 (`docs/BLUEPRINT.md` §1).
- KI#4 · balance harness (1000-sim distribution plots of `suspicion` / `fire_spread`) missing — MVP_SCOPE §15 promises an iter-6 baseline but no tool exists. Added as `balance-1` in `docs/TASKS.md` infra backlog; folded into the iter-6 verification stack (`docs/blueprint/phase0.md` §6). First balance observation from iter-2: with v0.1 numbers, environment checks at difficulty ≤ 30 auto-succeed for an unmodified actor (skill base 50 + d20) — talk/examine/use/distract never fail as shipped; the failure branches are mechanism-tested via a crafted high-difficulty pack copy. Retuning is pack data, validated by `balance-1`.
- KI#12 · intent OCC has no natural e2e trigger in iter-2 runs — single-actor sequential playscripts never move the projection between proposal and completion (only the fire chain interleaves, and it moves no positions/carriers). Mechanism + cause attribution are unit-tested (`tests/test_intent.py::test_occ_finds_the_breaking_event`); a natural trigger arrives with NPC reactions (iter-3) or the director (iter-4). iter-2a audit confirmed the unreachability is structural: no current precondition reads a prop any fire event writes. Do not delete until an e2e test exists.
- KI#13 · resolver desync wrote-then-crashed (iter-2a found+fixed) — CLOSED iter-2a: `_drop` hardcoded `from_=None` on the `condition` change; a legal take→drop→retake→redrop of a breakable item (seed 34) crashed after the bad event was already appended. Fix: idempotent condition change + the `Simulator._commit` gate (state deltas validated against the projection BEFORE the write, D-035) + regression tests; both baseline logs stayed byte-identical.
- KI#14 · `next_log_path` could truncate a live log — CLOSED iter-2a: after a middle-file delete, `len(existing)` named an existing path and the writer's "w" mode silently truncated it (INV-5 hygiene). Fix: first-free-slot scan + test.
- KI#15 · pack-lint gaps let data bugs reach mid-run — CLOSED iter-2a: `use_effect.status` not checked against `rules.states` (a typo would silently seed a garbage status axis); `knowledge.failure_total` without `events.failure_total` (a generic resolver would KeyError at completion); the steal resolver raised a bare `StopIteration` when its `carries_flagged` precondition was missing. All three now fail at load or raise a named `RunnerError`; steal's pack data gained the `failure_total` event branch.
- KI#16 · parallel spread passes broke runs with two fires — CLOSED iter-2a: a second ignition while a pass ran forked a second pass — doubling `chance_per_tick` and rolling the new location without a cause (`cause=None` → `LogError` mid-run; seed 19 reproducer, 3/59 seeds). Fix: the spread pass is a per-layer singleton with a shared cause map ignitions merge into (D-036); repeat smoke/burnout follow-ups now emit nothing instead of duplicate no-op events.
- KI#5 · runtime state vs test fold not explicitly separated — CLOSED iter-1: the Simulator keeps the incremental projection (`apply_event` per emission), `fold` exists only on the T2 test path — D-023/STATE-1 implemented and test-enforced (`tests/test_loop.py::test_t2_fold_equals_runtime_projection`).
- KI#10 · stdlib JSON-Schema validation path undefined — CLOSED iter-1: owner approved the stdlib mini-validator; landed as `core/schema.py` (D-032) — write-time validation in the log writer, T0 on doc examples + committed logs.

## FAQ / Pitfalls

- **System passes scan the whole projection, not the events that seeded
  them (KI#16 lesson).** `spread_tick` rolls every burning location with
  unburning spots — including fires ignited after the pass started. Any
  per-layer bookkeeping (cause maps, "already told" flags) must therefore
  be global to the layer and mergeable by new ignitions, never a frozen
  snapshot carried in the queue payload. Same rule for every per-tick
  system iter-3+ adds (knowledge, relations, states passes).
- **Hardcoded `from_` is a desync waiting to happen (KI#13 lesson).** A
  resolver that hardcodes a `from_` value instead of reading the
  projection breaks the moment a legal sequence moves that prop before
  the resolver runs. Two disciplines: read current values from the
  projection (the `_divert`/`_use_item` pattern) and make repeat effects
  idempotent (the `follow_up_draft` None pattern). The `_commit` gate
  (D-035) makes the failure loud BEFORE the write — the log never holds
  a desynced event — but the resolver should not rely on the net.
- **INV-3's stoplist scope (iter-2 interpretation, test-owned).** The
  stoplist (`tests/test_inv3_stoplist.py`) bans **setting** nouns — the
  invariant's named examples plus entity names and location/item
  vocabulary — matched as code segments (`guard`, `npc_guard_01`,
  `loc_guardroom` all trip; English derivations like 'guards' do not).
  Mechanic words (take, move, talk, fire, stealth — MVP_SCOPE §7's own
  vocabulary) stay legal; pack data is never grepped. The word list is
  tied to the pack by a self-check, so it cannot rot silently.
- **The loud/soft front-door line.** Malformed playscript steps (unknown
  fields, missing targets, bad spot names, unknown methods) raise
  `RunnerError` — author bugs crash. Well-formed but world-impossible
  intents emit `intent_rejected` no-op events — character attempts are
  facts. Moving a check from one side to the other is a contract change,
  not a refactor (INTENT_SCHEMA §9).
- **The golden T1 fixture is env-pinned.** The log header records the
  Python version (`AGENTS.md` §10 — same-environment determinism only), so
  `tests/fixtures/plumbing_smoke_seed42.jsonl` byte-compares only on the
  Python it was generated on. On an interpreter bump the byte-compare
  fails **by design**: regenerate (Simulator, seed 42, commit `"0000000"`,
  playscript `tests/playscripts/plumbing_smoke.json`) and commit the new
  fixture together with the env change. The same procedure applies to a
  deliberate behavior change that alters emitted bytes — iter-2 kept the
  fixture byte-identical (move/wait events anchor it), which is the
  regression proof that the front-door rewire changed no iter-1 canon.
  The full in-pytest regeneration guard lands with T1 at iter-6
  (`docs/blueprint/phase0.md` §6).
- **A ref citing a spec section it never contained is drift, not history.**
  The pre-D-028 FAQ rule protects *real* historical wording — verify with
  `git log -S "<phrase>" -- <file>` before calling something history.
  iter-0aa example: `df_worldgen.md` cited "MVP_SCOPE §4.1: 1 tick = 12
  in-world minutes" — §4.1 is the locations table and never owned time
  numbers; the fabricated figure leaked into `phase0.md` §1 and contradicted
  MVP_SCOPE §8's own arithmetic (1440 ticks/day). Diagnostic: any
  cross-doc numeric claim is re-derived from its claimed owner before it
  enters a prescriptive doc.
- **Where the code-quality bar lives (D-031).** Law: `AGENTS.md` §4
  (invariants + the canon-write privilege line) + §9 (DoD: conventions per
  `MVP_SCOPE.md` §18 — type hints, no `print()` outside `cli/` — and the
  L13/L14 elegance laws). Constitution: `docs/BLUEPRINT.md` §2 — L13
  (abstraction cost gate, Rule-of-Three tiers, 4-branch registry threshold)
  and L14 (elegance standard + review checklist). Build clauses:
  `docs/blueprint/phase0.md` §1 (type discipline, fail-fast, the
  architecture fitness test), §2 (ActionResolver registry), §6 (tests
  document the invariants; negative tests prove them). Executable:
  `tests/test_architecture.py` (iter-1) + the stoplist test (iter-2).
  Rationale: D-031; sources: `docs/REFERENCES.md` §15. The two owner texts
  are absorbed, not filed — no `docs/ARCHITECTURE.md` /
  `TYPE_DISCIPLINE.md` / `TESTING_PHILOSOPHY.md` will be created (the
  D-018 pattern); a new canonical layer is the named anti-pattern.
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
- **Content/tone questions → D-030 + the `PACK_SPEC.md` sketch row.** The
  start pack for phase 0 is `tavern_pack` v0.1 as scoped (`MVP_SCOPE.md`
  §4–§7 own the counts); tone is data asymmetry inside the existing systems,
  not new systems. Growing the pack or writing a pack spec before its
  trigger = scope creep (AGENTS §2.4; SPECS_BACKLOG header rule). Grim/romance
  material accumulates in the sketch row + `pack-1` (TASKS infra backlog)
  until the PACK_SPEC trigger fires (phase 6 / a 2nd setting).
- **Doc-loop alarm vs owner-requested research.** Twenty-six docs iterations
  in a row would normally force a stop (AGENTS §2.5). Owner-requested passes
  are the explicit exception (D-022) — the documented condition is a fresh
  owner request (iter-0s/0t additionally had fresh external sources;
  iter-0u/0v — distillation and audit; iter-0w — concept realignment; iter-0x
  — reference-influence audit; iter-0y — content principles; iter-0z — the
  quality round with two provided analyses; iter-0aa — the pre-code doc
  audit — rest on the request alone).
  iter-0aa is the twenty-sixth docs iteration in a row (0, 0b, 0c, 0e, 0f,
  0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n, 0o, 0p, 0q, 0r, 0s, 0t, 0u, 0v, 0w, 0x,
  0y, 0z, 0aa; iter-0d was infra). All ref-N backlog items are complete — ref-1
  through ref-13 plus the iter-0h cousins; ref-14/ref-15 (Sims, Prom Week)
  are owner-request-only candidates; no doc pass at all without a fresh
  owner request. **iter-1 code is next, unconditionally.**
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
- **Pre-D-028 RNG wording in `docs/ref/*` and `REFERENCES_DEEP.md` is
  historical evidence, not prescription.** Several ref files quote
  "INV-2: one `random.Random(seed)` instance" as it read at deep-dive
  time. Do not "fix" those — they document what the donor comparison was
  made against. The single reading owner of INV-2 is `AGENTS.md` §4
  (D-028); anything prescriptive points there (same pattern as the KI#6
  license-drift rule: catalog is the owner, index rows can lag).
- **Substance over line count (D-025) + per-ref split (D-026).** The cap is
  600 with the §6.1 substance filter as the real law — filler is cut
  always; named systems, real field lists, type enumerations, per-source
  verdicts are never cut to fit. The iter-0l..0r per-ref files run
  101–605 lines each, each under cap by construction or §6.1-justified;
  the iter-0u blueprint files are 149/340/224 lines — under cap by
  construction.
- **"Ref graveyard" check (iter-0x audit method).** To verify the reference
  corpus still influences the plans (not just exists as a folder), grep a
  sample of ledger terms across the planning docs — ShufflePool,
  ASSERT_stable, Influence Boundary, promoteTile, bm25, copy-from — over
  `docs/BLUEPRINT.md` + `docs/blueprint/` + `docs/TASKS.md` +
  `docs/SPECS_BACKLOG.md`: every term must land in at least one planning
  doc; the concrete mechanics stay owned by `docs/ref/` by design (link,
  never restate — D-027). Verified iter-0x; re-run at the phase-0 gate
  review.
- **License drift between catalog and index (KI#6, closed iter-0n; pitfall
  persists).** The `REFERENCES_DEEP.md` §2 index table is **not** the source
  of truth for licenses — `REFERENCES.md` (the catalog) is. Diagnostic:
  before flipping any ref-N row todo→done, grep the source row in
  `REFERENCES.md` and verify the license column matches the index entry.
  The standing pre-flip check is exercised across iter-0o/0p/0q/0r/0s/0t;
  iter-0u touched no ref rows, so no check was needed this iteration.

## Next step

**iter-3 · knowledge + relations + expectations** (`docs/TASKS.md`):
knowledge transfer with fidelity decay (rumor = transfer event,
`EVENT_SCHEMA.md` §3), the crime system reacting to steal-failure records
(the ev_0007 state_changes: suspicion 0→25, status → suspect, thresholds
from `rules.json` `crime_watch`), watch-change transfer, P2a npc↔npc
relations (D-020), P2d expectation_violation (KI#3), P2c detail callbacks
(D-033). Read before building: `docs/blueprint/phase0.md` §3 +
`MVP_SCOPE.md` §10; ledger rows EPIST-1, LOD-1, STATE-1. iter-2a audit
notes for the builder: `rules.json` carries the arrest threshold (75) in
two homes (`relations.suspicion_thresholds.arrest_attempt_at` and
`crime_watch.arrest.requires_suspicion`) — pick one owner when the crime
system lands; and arson on a fully-burning/destroyed location currently
logs a no-ignition success (backlog `pack-2` in TASKS).
