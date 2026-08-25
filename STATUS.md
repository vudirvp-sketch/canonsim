# STATUS — canonsim

Iteration: 0n (owner-requested: ref-5 batch — Wesnoth WML + Endless Sky mission DSL + ink + tracery event/narrative grammar family) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0n is the **ref-5 4-batch iteration** — the
open-licensed event/narrative grammar family (one GPL, one
GPL-3.0 code, one MIT, one Apache-2.0; all open per
`REFERENCES.md` §0.4 — pattern lifting permitted, port the
shape not the syntax per §0.7 / D-015), each in its own per-ref
file: `docs/ref/wesnoth_wml.md` (244 lines — the
`[event]`/`[filter]`/action triad as the reactive atom,
the `first_time_only`/`id`/`delayed_variable_substitution`
orthogonal fields for save-compatible reactive content, the
`[filter]` family (per-noun filter tags with real field
names: `x`/`y`/`side`/`type`/`race`/`canrecruit`/`status`/
`abilities`/`traits` for `[filter]`; terrain/time/owner for
`[filter_location]`), the ~30 action verbs (`[message]`/
`[set_variable]`/`[store_unit]`/`[unstore_unit]`/`[kill]`/
`[modify_unit]`/`[object]`/`[item]`/`[role]`/`[fire_event]`
…), the macro preprocessor (`#define`/`#ifdef`/`#ifhave`),
the Lua escape hatch since 1.7 as the precedent for our
`cli/`/`brief/` split, the `sighted` event as perception-
as-first-class-event-source, the closed `name` enum shape
lifted into `actions.json` `action_type`); `docs/ref/
endless_sky_dsl.md` (228 lines — the mission lifecycle
`to: offer`/`to: accept`/`to: complete`/`to: fail`/`to:
defer` as the state-machine shape for our `Intent`, the
condition expression language (smallest grammar in the
family — `=`/`!=`/`<`/`>`/`&`/`|`, no MTTH, no scopes, no
weights, no on_action IDs), the flat `effect` mini-language
(`set`/`clear`/`pay`/`outfit`/`ship`/`event`/`conversation`/
`fail`/`log`), the `phrase` block as one-symbol grammar
(simpler-than-tracery precedent), the `event` block
separate from `mission` as the cleanest public precedent
for player-independent background events = our
`seeded_hooks`, the `npc` `personality` flags lifted into
our `entities.json` `traits` field, the "lightweight beats
heavyweight for community-authored content" lesson);
`docs/ref/ink.md` (212 lines — the knot/stitch/divert/
gather graph shape lifted into our `Brief` sketch
(phase 1+), the `LIST` multivalued flag set lifted into
our entity `state` field, the `+` persistent vs `*`
single-shot choice persistence lifted into `Intent`
`accept_policy`, the `#` tag pattern lifted into `Brief`
`metadata`, the three sequence flavours `cycle`/`sequence`/
`shuffle` as the determinism hazard (INV-2 fix: same
expander with seeded RNG), the `KnotName?` visited-check
as the precedent for our `seen` knowledge channel, the
snapshot-save amnesia anti-pattern as INV-1 fix);
`docs/ref/tracery.md` (217 lines — the JSON grammar shape
lifted verbatim into `templates.json`, the save/restore
stack `[symbol:value#]` / `[symbol:#]` lifted into our
`render/` `stack[pop]` for cross-clause agreement, the
modifier pattern `#symbol.modifier#` with built-ins `a`/
`capitalize`/`s`/`ed`/`er` and a registration hook lifted
into `templates.json` modifiers, the "pure function from
(grammar, RNG state) → string" pattern = our `render/`
shape, the ~200-line runtime scale as the precedent that
useful procedural text generation is a small algorithm
not a framework). All four paraphrased from public docs
+ the open-source corpus per `REFERENCES.md` §0.4 / §0.7
(D-015). §2 of `REFERENCES_DEEP.md` flips ref-5-a/b/c/d
from todo → done. **KI#6 opened and closed in this
iter**: the §2 index had license drift for ref-5-b (listed
"CC-BY-SA", catalog says "GPL-3.0 code; mixed assets")
and ref-5-d (listed "CC0", catalog says "Apache-2.0");
fixed in the same §2 edit. AGENT_NAVIGATION §1 adds the
four new files to the `docs/ref/` list. Per AGENTS §2.5
this is the **thirteenth** docs iteration in a row (0,
0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n; iter-0d
was infra) — the doc-loop alarm has fired again; the
owner explicitly asked to continue reference work, so
the D-022 exception applies. iter-1 is still the next
functional step; no further docs iterations without a
fresh owner request. KI#3, KI#4, KI#5 unchanged. AGENTS,
ROADMAP, MVP_SCOPE, EVENT_SCHEMA, schemas, TECH_NOTES,
SPECS_BACKLOG, CORE_DESIGN_RESEARCH, VISION — untouched.

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
- KI#6 · CLOSED iter-0n · `REFERENCES_DEEP.md` §2 index license drift — ref-5-b listed "CC-BY-SA" (catalog §1 says "GPL-3.0 code; mixed assets"); ref-5-d listed "CC0" (catalog §4 says "Apache-2.0"). Fixed in the same §2 edit that flipped ref-5-a/b/c/d todo→done. Single-edit fix; no migration; no schema change.

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
- **Doc-loop alarm vs owner-requested research.** Thirteen docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0n is the thirteenth docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n;
  iter-0d was infra).
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
  subsystems with real field names and ~150+ on_action IDs). At
  iter-0m three proprietary §10 source files (`rimworld.md` 253,
  `l4d_director.md` 245, `alien_isolation.md` 296) — all under
  cap by construction (the closed-source constraint forces
  field-shape-from-public-talks only, not full enumeration). At
  iter-0n four open-licensed event/narrative grammar family files
  (`wesnoth_wml.md` 244, `endless_sky_dsl.md` 228, `ink.md` 212,
  `tracery.md` 217) — all under cap by construction (the pattern-
  not-content rule §0.7 + the JSON/grammar shape lift keeps each
  file to the mechanics layer only).
- **License drift between catalog and index (KI#6, closed iter-0n).** The
  `REFERENCES_DEEP.md` §2 index table is **not** the source of truth for
  licenses — `REFERENCES.md` (the catalog) is. The index restates the
  license as a one-line convenience column; if the two disagree, the
  catalog wins. iter-0n found two drifts in §2 (ref-5-b
  "CC-BY-SA" vs catalog "GPL-3.0 code; mixed assets"; ref-5-d "CC0"
  vs catalog "Apache-2.0"); both fixed in the same edit. The diagnostic:
  before flipping any ref-N row todo→done, grep the source row in
  `REFERENCES.md` and verify the license column matches the index entry.
  Same pattern as the catalog ↔ synthesis ↔ deep-dive anti-drift rule
  (D-024/D-026): a fact restated in two places drifts; the catalog is the
  owner.
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
