# TASKS.md — Backlog

> One task = one iteration. Status: todo / doing / done (collapse to one line
> when done). Update statuses at the end of every iteration. New ideas enter
> here, never the diff. Full law: `AGENTS.md` §2. Done-detail lives in git
> history + `worklog.md` + the owning docs — never restated here (KI#7
> cleanup, iter-0v). Day-tags removed per D-029 (calendar dropped); the
> build sequence is iteration-counted (`MVP_SCOPE.md` §17).

## Track A — main (simulator, no LLM)

> The phase ladder COMPLETE — phases 0..6 all CLOSED (gates
> iter-6/26/35/54/65/102/116); `docs/ROADMAP.md` §2 the single owner of
> closed/open, README/STATUS carry one-liners only. The standing work: the
> owner-gated backlog below + the world track (`docs/worldbuild/`, D-186)
> + the SoW horizon (ROADMAP §6).

### Standing rows (owner-gated — the live queue; the ORDER owner decides,
this file owns composition, never order — D-113; every row REVALIDATED
iter-150 (D-184) + iter-197 (the second pass: every parked premise
code-verified current at HEAD, zero closures-as-dead; the done rows
collapsed to the minimal form); each build row's verification plan rides
TEST_PLAN §9's claim packet)

> The world-authoring track is NOT this queue: the setting's own plan
> (the anchor's A1/A2/A3 + the W-ladder) lives in
> `docs/worldbuild/WORLD_WORKPLAN.md` (D-186) — a separate track, never
> a second queue; a world-authoring need for engine capability lands
> HERE as a standing row on the owner's call.

- `engine-1` — DONE (iter-170 D-192 DECIDED + iter-171..174 the {3-8B, GBNF}
  experiment, move (a) CLOSED + iter-177 D-193 the BUILD LANDING):
  llama-server behind the explicit adapter (`cli/engine.py`, INV-4's
  one-module form) — the GBNF mapping repo-side (`brief/gbnf.py`), the
  `--engine` door (the file contract preserved), the failure→ladder
  mapping, the provenance manifest; the contract absorbed (CONTRACTS §4);
  the serializer contract PRESENTATION_SPEC's (iter-178). Station
  remainder: TEST_PLAN §8.5's standing gap rows + PRESENTATION_SPEC §7's
  band (the owner's next engine run). Detail: D-192/D-193 + TECH_NOTES
  §13/§13.1 + git.
- `presentation-1` — DONE (iter-178, the owner's write call on the met
  exit criterion): `docs/PRESENTATION_SPEC.md` — the model-facing
  serializer contract over the stable brief IR (the D-055 pattern's
  fourth instance), written FROM the measured results (the mapping
  table + the narrator band; st-4 ABSORBED — the call budget, the
  no-tail resolution, thinking-as-ephemeral, the Script Tax clause);
  the three consult cards integrated (intake-30 the visual fence,
  intake-32 the re-expansion mapping, intake-33 the outcome-perception
  layers — no layer changed a shape, the cross-domain confirmation).
  Detail: the spec itself + D-193's tail + git.
- `parse-2` — disambiguation buttons + multi-intent utterances, each half
  behind its own gate (PARSER_SPEC §7; sharpened iter-150): BUTTONS wait on
  a frontend consumer (mode C live play — a UI affordance, never a parser
  change); MULTI-INTENT waits on live-session evidence that real utterances
  carry N intents (one classification per document today); neither half is
  "improve the parser" — the phase-2 grammar is gate-PASSED (D-064) and the
  boundary stays closed until a named consumer opens it.
- `st-2` — the identity promotion door (pack grammar beyond `take`, the
  D-054 machine; the read-path half landed as tex-1, iter-62/D-091):
  consumer-first, PARKED — no committed pack has wanted promotion beyond
  `take` (pack-1/pack-4 built without the door: the pawn-ticket hinge and
  the seams ride ordinary events + folds); the door (and the bg-5
  counted-promotion alternative with it) waits until a pack's design names
  the beat it needs — never a speculative build.
- `scav-1` — offline compaction = scavenge with tombstones: derived-store
  entries drop with tombstones AFTER the chronicler's rollups make them
  rebuildable; committed logs never edited (INV-5). Measurement before
  mechanism, PARKED — the chronicler (iter-64) and the fold checkpoints
  (iter-80) both landed, no derived-state size problem on record; premature
  until a real long-session cost is measured (a derived-store size census
  at a named horizon) — the intake-29 admission rule applied to our own
  queue.
- `st-5` — containers: the `in` relation + entity-birth promotion
  (blueprint §7): the first real consumer decides (a pack wanting portable
  objects, a res-1 sink shape — CONCRETE since res-1 landed iter-146/D-179;
  group-scale entity birth already exists, depth-7's condensation,
  iter-93/D-127). Never a speculative build.
- `qa-1` — DONE (iter-168, the owner's chat call over the row): mypy
  --strict on `core/` 207 → 0 at zero runtime change (1885+1 green both
  ends, goldens byte-untouched); the tool stays optional per D-031 (no
  dev-dep, no CI row — enforcement the owner's call); KI#88/#89 the
  found holes (the lint-side closures routed).
- `pack-3` — the Sci-Fi setting candidate (owner sketches; REWRITTEN
  iter-150): ONE candidate for the next authored pack slot — the owner's
  call when a slot opens, against the pressure pack's post-T1 rows (the
  legal exclusion D-134, the cultures name-1, the road traffic depth-7,
  the lore hooks D-140) and the intake-20 pack-candidate consult card; a
  genre-portability experiment (the engine's universality claim, INV-3's
  substance) its natural verification framing if picked.
- `bg-6` — the SoW integration audit, owner-deferred "until unavoidable"
  (D-055): a read-only pass over Soul-of-Waifu — extension points for a
  separate simulation chat mode, where llama.cpp sits, what the frontend
  must NOT own (the dumb-terminal contract, VISION §10). Output: a
  TECH_NOTES section + the `SOW_INTEGRATION_SPEC` sketch (SPECS_BACKLOG's
  trigger-gated row — the spec itself fires only at bg-6). Never blocks
  track A.
- `doc-2` — REFERENCES.md license/URL re-verification, quarterly
  (alongside the TECH_NOTES review). Last run 2026-09-13 (iter-114 — the
  research-layer re-point + the license/URL pass; the deltas in the
  iter-114 record). Next run: the next quarterly (owner-called per
  D-022) or at a phase-6 pack intake, whichever comes first.
- `doc-3` — DONE (iter-176, the owner's declared build): the state-layer
  reassembly landed — STATUS/TASKS/worklog/README/DECISIONS/TECH_NOTES to
  their declared functions (the FAQ essays one-liners + owner links, the
  operational recipes → TECH_NOTES §14/§15, the three TASKS history
  ledgers dead, the DECISIONS collapse 31→30) + the mechanical cap guard
  LIVE (`scripts/docguard.py` + `tests/test_docguard.py` — the recurrence
  fix). Detail: the iter-176 record + git.
- `mech-2` — the agent impact surface — DONE (iter-196, the owner's
  «открывай mech 2» call over STATUS Next step 1, the tooling-spike arm):
  `mechanics impact --path <pack path> | --ref <name>` — the derived
  reader index (the AST scan over core/brief/render/cli/sim + the
  packlint family, D-118 extended to the source), the exact-name reverse
  query (the rename-safety set), the indexed-matrix pointers (D-024);
  bounded one-hop traversal; tooling-only, stdlib-only (D-012), zero
  runtime change. The A/B falsifier RAN (iter-198, the owner's call;
  TECH_NOTES §17): the injected gate moved none of the three metrics,
  the cognitive premise refuted at scale, the whole-file emission wall
  + silent notes paraphrase measured instead. The structured-patch
  proposal PARKED (the owner's 2026-09-23 call): no machinery, no
  infrastructure — the next step, if it ever opens, is a minimal
  prototype testing exactly whether structured patch reduces the
  whole-file emission failures and the silent notes drift (§17's
  measured classes); full work does not open until that experiment
  exists. The rename-safety lint gap closed as its own slice
  (`rename-1` below). Detail: the iter-196/198/200 records + D-197
  + git.

### Iteration ledger (one line per iteration; the tail capped at 10 by the doc guard — older lines live in git; per-iteration detail: the D-rows + the owning docs + worklog + git, never restated here, the header's own law)

- iter-200 · 2026-09-23 · renamelint (rename-1) — the rename-safety admission closure landed (the owner's session-order call, the iter-198 T3 cell's measured gap): the actions' hooks-branch tags now linted against `director.hooks` (the last unchecked hook-reference surface — the worldgen/weather precedents already checked theirs; the KI#77-guarded read) + the structured-patch proposal PARKED with the minimal-prototype wording (no machinery, no infrastructure — the mech-2 row); 6 paths (the lint + the regression packet + the contract sync + the state docs)
- iter-199 · 2026-09-23 · flowgloss (rs-4) — the covering residue's row landed (the owner's continuation call firing STATUS Next step item 1, carried per the «если в одну итерацию не уместишься» instruction): the flow-gloss boundary (the economy flow's meaning on the reader surface, the rs family's fourth member — the pack's flow_glosses table + the renderer's gloss_flow + the lint closure + the verb line's conditional tail; the LOG untouched) and the probe's re-run's mandatory bar MET (the covering connected, glm n=2 convergent — the income-misreading GONE; the shave's agency + the withhold's one-surface contradiction the open residues) — WORLD_TESTS §9's W5 entry
- iter-198 · 2026-09-23 · abfalsifier (mech-2) — the A/B falsifier's measurement RUN (the owner's call, STATUS item 1): 6 realistic pack-edit tasks × bare/impact-gated × n=3 at glm-4-plus, whole-file protocol (Rule 9, runner + transcripts outside the repo) — the gate moved NO metric (success 8/18 both arms, lint refusals 0, patches tiny); the cognitive premise REFUTED at scale (conditional-on-parse 8/8 vs 8/9); the measured bottleneck: the whole-file emission wall (bracket drift in director.hooks, 60–67%) + 73% silent notes paraphrase; the structured-patch PROPOSAL re-scoped to emission reliability, fate the owner's call — TECH_NOTES §17 + the intake-37 block update; doc-only, zero code touch
- iter-197 · 2026-09-23 · revalid2 — the second standing-queue revalidation + the closure pass (the owner's call, D-184's form): all twelve standing rows audited at HEAD `cd64ce8` — every parked premise CONFIRMED-current (no gate moved), zero closures-as-dead; the done rows engine-1 + mech-2 collapsed to the minimal form (D-024); the ROADMAP §2 res-1/since-1 "open rows" rot + the README engine-1/bg-9 rot fixed; 5 paths doc-only
- iter-196 · 2026-09-22 · mech2 — the mech-2 tooling spike (the owner's row-opening call): `mechanics impact --path/--ref` landed (the derived reader index — the AST scan, D-118 extended to the source; the exact-name reverse query; the matrix pointers), the §9 claim block + 8 pins; the structured-patch machinery + the edit-shape guard stay PROPOSAL behind the A/B falsifier (now armed by the tool)
- iter-195 · 2026-09-22 · bottleneck (intake-37) — the agent-bottleneck research note routed as a mandatory artifact: PARTIALLY CONFIRMED (formats + tooling direction confirmed; the full-file-rewrite claim REFUTED by the measured 97%-surgical history; the mutation-blindness MEASURED — value mutations pass lint + goldens when uncovered); the research/intervention documentation schema (scratch/ the interventions folder); one row convened (mech-2) + TEST_PLAN §9's mutation prism — phases.md §6's intake-37 block
- iter-194 · 2026-09-22 · humorgloss (rs-3) — the W5 humor fix landed (the bloom kind's account-kind gloss — the withhold's meaning on the reader surface, one table row, rs-2's mechanism unchanged) and the humor probe's re-run's mandatory bar MET (the mechanism-grounded joke n=2, the taboo 1/2 — the station PARTIALLY CONFIRMED, the withhold's own joke unextracted; WORLD_TESTS §9's W5 entry)
- iter-193 · 2026-09-22 · intake36 — the ULTIMATE-v2 packet routed whole (intake-36, D-196): 39 units / 10 families, every body read + code-verified at HEAD; 34/39 CONFIRMED-owned (the largest single confirmation batch), the three fresh routings each joining a named consumer (C03+F02 → the W5 heartbreak station, P01+P03 → the road-traffic rider, C05 → the group-stock lint gap), zero new rows — phases.md §6's intake-36 block
- iter-192 · 2026-09-22 · humorprobe — the W5 humor station: the probe RAN and FAILED at the rendering boundary (the withhold's meaning renders nowhere — the banking lines read as income; n=2 convergent on an imported-template joke; the fix's route the owner's call — WORLD_TESTS §9's W5 entry)
- iter-191 · 2026-09-22 · accountgloss (rs-2) — the W5 rendering-boundary fix landed (the account-kind gloss on the reader surface: the pack's `account_kinds` words + the renderer's mapping + the lint's closure) and the biography probe's re-run PASSED CLEAN — the reader reconstructed the persistent obligation, n=2 convergent; the gate's named condition met (WORLD_TESTS §9's W5 entry)

## Track B — background (evenings, foreign canon)

### bg-7 · engine + confabulation probe — done (2026-09-07)

- Done one-liner: all five probes' FIRST NUMBERS on the sandbox API engine (glm-4-plus) — TECH_NOTES §10; the {3–8B, GBNF} arm the gap row; runner + transcripts outside the repo (Rule 9).

### bg-8 · engine — the LLM-integration test runner — done (2026-09-09)

- Done one-liner: the testproto live half — the deviation corpus F1–F6 through the REAL mode-C door: the world-answer law's first live numbers (coverage 34/34 = 100%, honest 17/36) + the heartbeat's first run (84.4 → 93.3% after one re-ask). Transcripts re-distilled: tests/fixtures/deviation_corpus.json + tests/test_deviation.py + TECH_NOTES §11. Gap rows standing: the {3–8B, GBNF} arm, the bg-7 prose families, the per-family latency distribution. Detail: TEST_PLAN §8.2/§8.5, TECH_NOTES §11.

### bg-9 · the API-side prose families re-run — done (2026-09-21)

- Done one-liner: bg-7's standing API-side gap row closed at the
  sandbox API engine (glm-4-plus, paced — the 429 window recovers in
  ~minutes): the four families re-run — (ii) 3/8 accepted, the claims
  channel still the beat-killer, the event-id mint-from-ticks the new
  refusal family, the generic-capital floor family now in the clean
  arm; (iv) the degraded arm's state-refusals rose 8 → 23; (v) the
  cast surface still earns nothing; (iii) validity 7/7 both scripts,
  the script tax moved into mapping quality. The numbers + the
  instrument's honesty notes: TECH_NOTES §10's re-run block; TEST_PLAN
  §8.5 the closure. Runner + transcripts outside the repo (Rule 9).

### bg-2 · event taxonomy — DONE (bg-2-event-taxonomy)

- Done one-liner: `docs/TAXONOMY.md` (120 entries across the 16 target
  types; AC ≥100 MET) + `scripts/df_taxonomy.py` (the quantile-spread
  survey over the sink DB) + the sink v2 plus pass
  (`scripts/df_import.py` — D-051's deferral fired: theft/beast detail
  is companion-only, D-063). Measured findings + the bg-3 consumer
  caveats: TAXONOMY §4/§5; recipe: TECH_NOTES §3.2.

### bg-3 · briefer spike — DONE (bg-3-briefer-spike)

- Done one-liner: the POV mini-briefer + the reverse-validation gate over the sink DB (the ≤2-regen ladder + the dry floor ported from VALIDATION_SPEC §7). Detail: TECH_NOTES §3.3 + tests/test_df_briefer.py.

### bg-6 · SoW integration audit — todo (owner-deferred)

- Moved to **Standing rows** above (the D-055 deferral; never blocks
  track A).

## Infra backlog (pick by need)

- `mech-1` · the mechanics introspection CLI — done (iter-84, D-118): `scripts/mechanics.py` matrix/trace/why/blast (the shadow-replay law: the PUBLIC pipeline only); 11 pins in tests/test_mechanics.py. Detail: D-118.
- `rs-1` · the told-fact gloss boundary — done (iter-188, the owner's W5-decomposition call, finding 3): raw machine ids (`npc_*`, `pay_*`, `tally_*` — the composite knowledge tokens) left the reader surface through `rumor_told`'s `{knows}` slot; FIXED at the boundary/mapping only — the pack-declared `knows` gloss table (templates.json, all five packs) + the renderer's fold-aware matcher (`render/chronicle.py::gloss_knows`, the dry fallback for unmatched tokens) + the regression + coverage census (`tests/test_knowsgloss.py`); the LOG untouched (zero corpus price). Honest residue: LITERAL fact tokens (the read-hinge secrets, `purse_missing`-class names) render dry as-is — no entity ids, their rendering quality the W5 probe's boundary to name, never a preemptive renderer feature. Detail: the test packet's claim block + TECH_NOTES §16's context.
- `rs-2` · the account-kind gloss boundary — done (iter-191, the owner's route (а) call over the W5 first run's failure): the account kind's MEANING rendered nowhere at the first run ("16 paper owed" indistinguishable from "16 paper held"); FIXED at the boundary/mapping only, the rs-1 precedent's own family — the pack-declared `account_kinds` gloss table (templates.json, the kind's meaning as reader prose) + the renderer's mapping (`render/chronicle.py::gloss_account_kind`: the verb lines' `{kind}` slot + the state line's apposition, the dry fallback for unglossed kinds, `core/economy.py::ACCOUNT_GLOSS_BLOCK` the single spelling owner) + the load-time lint closure (`core/packlint/economy.py`: keys inside the economy.accounts vocabulary, values non-empty strings, a gloss table without the economy block refused as dead data); the LOG untouched (zero corpus price). The W5 re-run PASSED CLEAN on the fixed surface (the gate's named condition met — WORLD_TESTS §9's W5 entry). Honest residue: the COVERING not yet one surface (the +3 reckonings read as income — the arc's assembly's own future row); the kind's meaning renders at level 0 too (the apposition states the account's kind, never the balance). Detail: the test packet's claim block + WORLD_TESTS §9's W5 entry.
- `rs-3` · the bloom kind's account-kind gloss — done (iter-194, the owner's «продолжай работу» continuation call firing STATUS Next step item 1 — the W5 humor probe's rendering failure, the rs family's third member): the withhold's MEANING on the reader surface, the rs-2 precedent's own shape — ONE table row in the province pack's `account_kinds` ("bloom kept off the weighbeam since the shave" — the paper gloss's shape, the authored origin loop H's own), the mechanism rs-2's unchanged (the crofts' state line + the banking verb lines now carry the meaning), the LOG untouched (zero corpus price); the humor probe's re-run on the fixed surface: the MANDATORY BAR MET (glm n=2 — the mechanism-grounded joke from both readings, the first run's imported-template mode GONE, the taboo 1/2 with the authored taboo nailed once), the station PARTIALLY CONFIRMED (the withhold's own joke unextracted — the arc's assembly's future row's material). Detail: the test packet's claim block + WORLD_TESTS §9's W5 entry.
- `rs-4` · the economy flow-gloss boundary — done (iter-199, the owner's «продолжай работу по логике» continuation call firing STATUS Next step item 1 — the covering residue's future row, the arc's assembly, carried per the owner's «если в одну итерацию не уместишься» instruction): the economy FLOW's meaning on the reader surface, the rs family's fourth member (rs-1's token-mapping shape, rs-2's pack-table shape one granularity deeper — the kind table glossed the KIND, this table glosses the FLOW; the measured motivation: the +3 reckonings read as periodic income because the flow's relation rendered nowhere, and "coin" is one kind serving four flows, the kind gloss's granularity ceiling) — the pack-declared `flow_glosses` table (templates.json, the three coin flows glossed from the economy notes' own words) + the renderer's `gloss_flow` at the account verbs' `{flow}` slot (landed before the outcome loop — the raw id a machine token, never the reader's; the unglossed flow renders nothing) + the verb line's conditional tail + the load-time lint closure (dead keys refused, the table without the block dead data) + `tests/test_flowgloss.py` the claim packet; the LOG untouched (zero corpus price). The probe's re-run on the fixed surface: the MANDATORY BAR MET (the covering connected, glm n=2 convergent — the income-misreading GONE); the honest residues: the shave's AGENCY and the withhold's one-surface contradiction (each a future row's material — WORLD_TESTS §9's W5 entry). Detail: the test packet's claim block + WORLD_TESTS §9's W5 entry.
- `rename-1` · the rename-safety admission closure — done (iter-200, the owner's session-order call over the iter-198 T3 measured failure, TECH_NOTES §17): every action hooks-branch tag must name a declared `director.hooks` entry — the stale-tag-after-rename class passed admission and the runtime's `director.seed` silently skips unknown tags (the deferred consequence dies invisibly); the guarded read (`core/packlint/actions.py`, the KI#77 order law — `_director` validates the block later) + the two-test regression packet (`tests/test_core.py`: the T3 scenario + the typo twin) + PACK_SPEC §3's cross-ref line the contract sync; the five committed packs load green (zero orphan seeds). Detail: the iter-200 record + TECH_NOTES §17 + git.
- `chron-2` · the chronicler long-horizon legibility experiment — parked until after the W5 probes (the owner's call): the annual tale's routine flood measured (watch_change 722 + document_check 88 of 916 event lines, seed 42 — TECH_NOTES §16); the standing INVARIANT any future work must hold: repeated routine events must not displace causal-change events in the tale. The bounded experiment: deterministic aggregation of the repeated circuits (a cadence line for the rotation, each causal-change event keeping its own line) — never a renderer rebuild, never a global importance change; opens on the owner's call only.
- `engine-2` · the urgency-roll stream split — done (iter-50, D-079).
  Detail: D-079.
- `ci-1` GitHub Actions — done (iter-143, D-176): pytest + ruff on
  push/PR to `main` (PYTHONHASHSEED=0, Python 3.12.14 the env pin);
  branch protection the owner's settings step (the recipe in the iter-143
  stop-point report). Detail: the ledger + D-176.
- `perf-1` 10k-tick timing profile — done iter-30: ~9.8k events/s
  write-side, event-linear; the numbers owner TECH_NOTES §8.
- `balance-1` 1000-headless-sim distribution harness — done iter-6:
  `scripts/balance_harness.py`; the harness contract TEST_PLAN §6. KI#4
  closed.
- `doc-1` VISION freeze review — done iter-26 (the phase-1 gate's
  doc-actualization sweep).
- `doc-2` REFERENCES quarterly — the recurring row → **Standing rows**
  above.
- `pack-1` Grim tavern pack — done (iter-148, D-181): the fourth committed
  pack; the consent split's lint the only engine-side touch. Detail: the
  ledger + D-181 + the pack's own notes.
- `pack-2` Arson-on-ashes guard — done iter-29 (D-061): the
  `spot_available` door check — the door-outcome vocabulary's fourth axis.
- `pack-3` Sci-Fi setting candidate — → **Standing rows** above (rewritten
  iter-150).
- `pack-4` Pressure-city pack — done (iter-149, D-182 — the T1 slice):
  zero core change held exactly; the post-T1 rows the future slices'
  material. Detail: the ledger + D-182 + the pack's own notes.
- `ref-N` Reference deep dives — the plan table and the per-file index
  live in `docs/REFERENCES_DEEP.md` §1/§2 (single owner). All
  ref-1..ref-13 done; ref-16 (agent-memory-atlas, owner-supplied) absorbed
  inside iter-8a, no solo iteration; ref-17 (DF designed experience)
  done (iter-8d).
- Candidates (owner-request only — D-022 law: no doc pass without a fresh
  owner request; both synthesis-only today, cited via the blueprint donor
  stacks + `docs/REFERENCES.md`): `ref-14` The Sims (proprietary;
  patterns-from-papers only, D-015); `ref-15` Prom Week (academic paper +
  GDC talk; no code repo).
