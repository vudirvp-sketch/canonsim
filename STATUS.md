# STATUS — canonsim

Iteration: 0j (owner-requested: ref-2 deep dive + cap policy rewrite) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0j has two owner-requested goals. (1) **Cap policy rewrite**: the
rigid 400-line wall (D-024-era) was a crutch — iter-0i trimmed ~85 lines
of substance out of `docs/REFERENCES_DEEP.md` §2 to fit it. AGENTS.md §6
is rewritten with §6.1 "Substance vs cruft" criteria: filler /
restatements / linker chains = cut always; named systems, real field
lists, type enumerations, pseudo-code, per-source verdicts = never cut
to fit cap. Cap raised to 600 as a generous ceiling; substance can
exceed it with a worklog rationale (D-025). (2) **ref-2 deep dive**: new
§4 in `docs/REFERENCES_DEEP.md` — Cataclysm: DDA `data/json/` schema
(items / monsters / recipes / itemgroups / missions / NPC factions /
monster factions / inline `//` commentary). §2 of the same file is
restored from iter-0h pre-trim (substance returned: full XML top-level
elements list, event-type enumeration with field names, Mesa pseudo-code
tick loop, DataCollector detailed description, dropped "no determinism
by construction" Mesa weakness bullet). File now 737 lines — over the
new 600 cap, justified by substance (4 deep dives + format + plan); see
worklog iter-0j for the rationale. Per AGENTS §2.5 this is the **ninth**
docs iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j; iter-0d was
infra) — the doc-loop alarm has fired again; this iteration is
owner-requested, so the D-022 exception applies. iter-1 is still the next
functional step; no further docs iterations without a fresh owner
request. KI#3, KI#4, KI#5 unchanged.

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index.
- INV-2 Determinism: single seeded RNG, no wall-clock, `sorted()` iteration,
  fixed `PYTHONHASHSEED`, queue key `(tick, sub_order, actor_id)`.
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#3 · `expectation_violation` primitive missing — NPC reacts only to presence in `knowledge`, not to absence (purse gone, guard missing). Fix: P2d in `CORE_DESIGN_RESEARCH.md` §6, slated for iter-3.
- KI#4 · balance harness (1000-sim distribution plots of `suspicion` / `fire_spread`) missing — MVP_SCOPE §15 promises an iter-6 baseline but no tool exists. Added as `balance-1` in `docs/TASKS.md` infra backlog.
- KI#5 · runtime state vs test fold not explicitly separated — risk of O(N²) at startup if `fold(log)` is misused as runtime path. D-023 records the rule: runtime = incremental projection; fold = T2 replay only.

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
- **Doc-loop alarm vs owner-requested research.** Nine docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0j is the ninth docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j; iter-0d was infra).
- **Substance over line count (D-025).** The 400-line cap was a crutch —
  iter-0i trimmed real depth (XML element lists, event-type enumerations,
  Mesa pseudo-code, DataCollector details) to fit. New policy: AGENTS §6
  cap is 600, but §6.1 is the real law — filler / restatements / linker
  chains / decorative prose are cut always; named systems, real field
  lists, type enumerations, pseudo-code, per-source verdicts are never cut
  to fit the cap. Over cap after a real cruft pass: keep, document in
  worklog. `docs/REFERENCES_DEEP.md` is 737 lines in iter-0j — 4 deep
  dives with concrete field names and type enumerations justify the
  breach.
- **Catalog vs deep dives vs synthesis — three places, three jobs.**
  `docs/REFERENCES.md` is the **catalog** (license, URL, phase gating,
  intake rules). `docs/CORE_DESIGN_RESEARCH.md` §2 is the **synthesis**
  (one-line depth primitive + failure mode per source).
  `docs/REFERENCES_DEEP.md` is the **deep dive** (named mechanics, real
  data structures, what we take/adapt/inspire, strengths/weaknesses, and
  a per-source verdict). Drift rule (AGENTS §3): never restate across
  these three — link only. A future reference detail belongs in deep
  dives, not in the catalog or the synthesis table.

## Next step

iter-1 · core plumbing is the next functional step: seed, RNG instance, clock,
event queue, JSONL log with header, playscript runner, pack loader for the
drafted `content/tavern_pack/` v0.1. Acceptance criteria in `docs/TASKS.md`.
Owner's blocking answers to Q1–Q3 are absorbed as D-019..D-021 and flip
P2a/P2b and M3/M4/M5 from proposals to accepted iter-3/iter-4/iter-6 scope.
