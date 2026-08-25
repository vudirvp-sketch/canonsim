# STATUS — canonsim

Iteration: 0l (owner-requested: ref-3 Paradox event scripting deep dive) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0l is the **ref-3 solo iteration** — the Paradox event scripting
deep dive (`docs/ref/paradox_scripting.md`, 605 lines). Owner asked to
continue reference work after iter-0k; per §1 of `REFERENCES_DEEP.md`
the next item in the queue was ref-3 (CK3 + EU4 + Stellaris: trigger /
weight / mtth / effect / option / scope grammar). Research: 15 wiki
pages fetched (CK3 Events / Event_modding / Triggers / Effects / Scopes,
EU4 Event_modding / Conditions / Effects / Scope, Stellaris Event_modding
/ Conditions / Effects / Scopes / On_actions), paraphrased — patterns
not content per §0.7 of `REFERENCES.md` (D-015). The file is 5 lines
over the 600 cap after a real cruft pass — substance per AGENTS §6.1
(named systems, real field names, type enumerations, ~150+ on_action
IDs, real trigger/effect tokens, the `every/random/any` iterator
trinity, the `weight_multiplier` shape, the `immediate + option + after`
three-phase effect lifecycle, the `add_hook` family as P3a precedent,
the MTTH anti-pattern named against INV-2); the breach is documented
here and in the worklog. §2 of `REFERENCES_DEEP.md` flips ref-3 from
todo → done. AGENT_NAVIGATION §1 adds `paradox_scripting.md` to the
`docs/ref/` list. Per AGENTS §2.5 this is the **eleventh** docs
iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l; iter-0d
was infra) — the doc-loop alarm has fired again; the owner explicitly
asked to continue reference work, so the D-022 exception applies.
iter-1 is still the next functional step; no further docs iterations
without a fresh owner request. KI#3, KI#4, KI#5 unchanged. AGENTS,
ROADMAP, MVP_SCOPE, EVENT_SCHEMA, schemas, TECH_NOTES, SPECS_BACKLOG,
CORE_DESIGN_RESEARCH, VISION — untouched.

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
- **Doc-loop alarm vs owner-requested research.** Eleven docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0l is the eleventh docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l; iter-0d
  was infra).
- **Substance over line count (D-025) + per-ref split (D-026).** The
  400-line cap was a crutch — iter-0i trimmed real depth (XML element
  lists, event-type enumerations, Mesa pseudo-code, DataCollector
  details) to fit. AGENTS §6 cap is 600, but §6.1 is the real law — filler /
  restatements / linker chains / decorative prose are cut always; named
  systems, real field lists, type enumerations, pseudo-code, per-source
  verdicts are never cut to fit the cap. Over cap after a real cruft pass:
  keep, document in worklog. At iter-0j the single-file
  `docs/REFERENCES_DEEP.md` was 737 lines — 4 deep dives with concrete
  field names and type enumerations justified the breach. At iter-0k the
  same content was split into 5 per-ref files in `docs/ref/` (D-026);
  each is 101–244 lines — under the cap by construction. At iter-0l
  `paradox_scripting.md` is 605 lines — 5 over the cap, justified per
  §6.1 (three games × trigger/MTTH/weight/effect/scope/on_action
  subsystems with real field names and ~150+ on_action IDs).
- **Catalog vs deep dives vs synthesis — three places, three jobs.**
  `docs/REFERENCES.md` is the **catalog** (license, URL, phase gating,
  intake rules). `docs/CORE_DESIGN_RESEARCH.md` §2 is the **synthesis**
  (one-line depth primitive + failure mode per source). Per-source
  **deep dives** live in `docs/ref/<source>.md` (one file per source,
  indexed by `docs/REFERENCES_DEEP.md` §2 — D-026; the single-file
  arrangement from D-024 did not scale). Drift rule (AGENTS §3): never
  restate across these three — link only. A future reference detail
  belongs in a per-ref file under `docs/ref/`, not in the catalog or the
  synthesis table.

## Next step

iter-1 · core plumbing is the next functional step: seed, RNG instance, clock,
event queue, JSONL log with header, playscript runner, pack loader for the
drafted `content/tavern_pack/` v0.1. Acceptance criteria in `docs/TASKS.md`.
Owner's blocking answers to Q1–Q3 are absorbed as D-019..D-021 and flip
P2a/P2b and M3/M4/M5 from proposals to accepted iter-3/iter-4/iter-6 scope.
