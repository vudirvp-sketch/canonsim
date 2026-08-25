# STATUS — canonsim

Iteration: 0k (owner-requested: REFERENCES_DEEP split into per-ref files, D-026) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0k has one owner-requested goal: **split the deep-dive content
out of `docs/REFERENCES_DEEP.md` into per-reference files** under a
new `docs/ref/` subdirectory. The single-file arrangement from D-024 did
not scale: at iter-0j the file was 737 lines (over the 600 cap, justified
by substance per D-025) and the iteration plan in §1 has 9 more ref-N
iterations queued (ref-3..ref-11), projecting ~2500–3500 lines at
single-file scale (4–6× the cap). The same logic that D-024 applied
recursively to the catalog/synthesis/deep-dive split applies again:
when one place bloats, split the place. **Five per-ref files created**
(`neighborly.md`, `mesa.md`, `df_legends_xml.md`, `df_worldgen.md`,
`cdda_data_json.md`) carrying the iter-0h + ref-1 + ref-2 content
verbatim, with cross-refs updated (`§2 above` → `df_legends_xml.md`,
`(see below)` → `mesa.md`, etc.). Each is 101–244 lines — under the 600
cap by construction; no substance exceptions are needed. **The new
`docs/REFERENCES_DEEP.md` is 133 lines**: header + §0 format template +
§1 iteration plan + §2 NEW index table (one row per ref: id, source,
file, license, phase, one-line verdict, status). Future ref-N iterations
touch 2 files (one new `docs/ref/<source>.md` + the index to flip status)
— well within the 3–5 soft limit. D-026 supersedes the "single file"
wording of D-024; the three-place anti-drift policy stands unchanged
(catalog ↔ synthesis ↔ deep dives); the deep-dive place is now a
directory, not one file. Per AGENTS §2.5 this is the **tenth** docs
iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k; iter-0d was
infra) — the doc-loop alarm has fired again; this iteration is
owner-requested (the owner asked for the restructure explicitly), so
the D-022 exception applies. iter-1 is still the next functional step;
no further docs iterations without a fresh owner request. KI#3, KI#4,
KI#5 unchanged. AGENTS, ROADMAP, MVP_SCOPE, EVENT_SCHEMA, schemas,
TECH_NOTES, SPECS_BACKLOG, CORE_DESIGN_RESEARCH, VISION, TASKS main
tracks — all untouched.

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
- **Doc-loop alarm vs owner-requested research.** Ten docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0k is the tenth docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k; iter-0d was infra).
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
  each is 101–244 lines — under the cap by construction. The substance
  filter still applies within each per-ref file, but no exception is
  needed.
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
