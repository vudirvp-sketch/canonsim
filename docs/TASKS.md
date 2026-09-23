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

- iter-212 · 2026-09-24 · doc-5 (the research-discipline vocabulary into its owners, the CP-migration family's second slice, the owner's continuation call over STATUS Next step 1): the claim-side epistemic classes FACT (directly established by evidence) / INFERENCE (a reasoned conclusion from evidence) / HYPOTHESIS (plausible, unverified) / PROPOSAL (a possible future direction) / UNKNOWN (not presently decidable) named in TEST_PLAN §9 beside the standing disposition vocabulary — class and disposition separate axes (the claim's kind as asserted vs the verification's verdict), the class gating what a disposition may license (hypothesis → requirement, proposal → architecture, research → implementation, plausibility → proof the forbidden transitions; a surviving HYPOTHESIS/PROPOSAL routes to an owner-gated row, never into a build); the five-part design test (Principle / Form / Quality / Transfer / Combined design) landed as BLUEPRINT §2 L15 beside L13/L14 — form-match alone never enough (an existing form with quality/transfer/combined-design unproven caps the strongest disposition at PARTIALLY CONFIRMED), applied at a genuine design fork only, never a ritual; TEST_PLAN §9's lens quality-bar sentence re-pointed at L15 (the single owner, D-024); the D-198 row's doc-5 clause closed; 6 paths doc-only (the two owner docs + the state docs; the D-022 exception: the owner's fresh continuation request)

- iter-211 · 2026-09-24 · doc-4 (the agent control-plane extraction, the owner's CP-rework calls over the external CanonSim Agent Control Plane document): the durable layer extracted surgically into the existing owners — task intake (an explicit owner request = the current task; STATUS Next = the ORDER, TASKS = the COMPOSITION) + the design-fork preference + infrastructure admission (existing → minimal extension → new; the standing refusals) + four stop conditions → AGENTS §2; the 8-step authority & conflict resolution (no silent reconciliation) → the new AGENTS §11; handoff & reproducibility (BASE_COMMIT from the actual checkout, the delta-archive protocol + self-check, the owner-side command form) + the exact check triple → the new AGENTS §12/§10 — D-113's chat-side verify-seed + archive placement SUPERSEDED (D-198, the marker riding the D-113 row); context closure + question classes + the change-impact gate (mechanics impact/blast) → NAV §2 (+ `impact` named in NAV §5); the invocation target: repository + task words; 6 paths doc-only (the merged doc-4+doc-5 slice — the merge the owner's quality call, the soft limit honestly over, the scope noted in the worklog; the D-022 exception: the owner's fresh CP-rework request)

- iter-210 · 2026-09-24 · proberead (the direct coverage probe's reading) — the owner's chat answer over the delivered kit's one question RECEIVED and the question CLOSED (the iter-208 delivery's own class, the reading the owner's side): the pre-set separation audit's NOT-PROBED branch landed — the fund-frame present directly on the readable surface and extracted under the direct question (the annual +3 coin's own material: "the honest year's surplus, the debt fund climbing toward the paper sixteen" — the material itself defining the coins the year's surplus and an accumulating fund toward the paper sixteen's discharge, never mere income); the smelt-crofts separation HELD (their annual +2 bloom another material flow, rs-6's frame "the camp's answer to a tilted beam" — the withhold/bloom, never the same debt fund); the iter-208 divergence classified NOT-PROBED, never NOT-EXTRACTED (the free-answer form's artifact, the surface carries the frame — the human band's covering bar joins the LLM band's): no datum for a renderer/prose/pack fix — zero code, zero pack, zero canon, the boundary law never tripped; the discovery-path residues stand unchanged (the owner's standing prescription), no new probe on the question — WORLD_TESTS §9's W5 entry; 5 paths doc-only (the reading's recording class, iter-208's own form; the D-022 exception honest: the owner's fresh request, the reading's delivery, firing the doc-only recording iteration)
- iter-209 · 2026-09-24 · remeasure (the humor station's LLM re-measure on the rs-6 surface + the coverage kit) — the owner's «продолжай работу если нужно» continuation call firing STATUS item 1's raised questions: the humor's surface-unequal confound RESOLVED — the LLM humor re-measure on the SAME re-weigh package the human band read (regenerated byte-identically, every recorded substance shape hit: the read t=1112 night/partial, the fall t=2824 with the fund 18, the collection t=2826, the close 0/8/98, the heap 18, seven crossings + banks, the tale 87 lines; the audit pre-set BEFORE the reading — the mechanism bar MANDATORY, the withhold-riding class the measured question; the blind reader glm n=2, the runner + transcripts outside the repo, Rule 9): the mandatory bar MET n=2 convergent (two different mechanism-grounded jokes, the imported-template and identical-joke modes absent) AND the withhold-riding joke class EXTRACTED n=2 (the iter-194 unextracted class, the human band's own — the divergence was the SURFACE, the bands equalized; the position-dependence explicit n=2; the taboo 1/2; the withhold-as-answer regression held n=2) — WORLD_TESTS §9's W5 entry; the direct coverage probe kit DELIVERED (the covering's fund-frame divergence: the direct question over the same package + the pre-set separation audit — the fund gloss quoted → not-probed, the fund-frame absent → not-extracted; the reading the owner's side in chat, the iter-208 delivery's own class); the discovery-path residues stand at both bands; 5 paths doc-only (the state docs — iter-204/207/208's own class; the D-022 exception honest: the owner's fresh request fired it)
- iter-208 · 2026-09-24 · humanread (the W5 human live band's reading) — the owner's three blind answers RECEIVED and SCORED against the pre-set audit (the owner's chat delivery firing STATUS item 1 — the reading's own next beat, the convergence the band's standing question): CONVERGENT with the post-fix LLM band on every mandatory bar at n=1 (the debt frame with the mere-holding reading refused, the discharge's direction, the shave's direction, the withhold-as-answer; the mechanism-grounded joke — riding the WITHHOLD itself, the authored answer's own class, beyond the LLM band's rs-3-surface measurements with the surface-unequal confound named, the taboo boundary + the position-dependence explicit; the heartbreak's mandatory pair both halves — the rs-8 clause's own semantics + the echo line's forward frame — and the supporting bars); the single divergence the covering's fund-frame (the reckonings carried and the arc joined, the fund vocabulary not restated — the free-answer form's honest caveat); the reading's own residues recorded (the runner's grudge a standing-renders-story-doesn't; the fail-then-pass + the 40/80 skipped — standing at both bands; the drowned line implicit, no conflation); the stations' states stand — the human-band clauses now measured — WORLD_TESTS §9's W5 entry; 5 paths doc-only (the state docs — iter-204/207's own class; the D-022 exception honest: the owner's fresh request, the reading's delivery, firing the doc-only recording iteration)
- iter-207 · 2026-09-23 · humanband (the W5 human live band, option (б)) — the human band's INSTRUMENT re-established + the READING KIT delivered to the owner (the owner's call, STATUS item 1 — the LLM reader the instrument so far, glm n=2, the human reader's convergence the band's standing question): the two packages regenerated deterministically at seed 42 (the re-weigh twin's full chain: the runner's crofts detour + the night tally read (partial, the cluster still minted — the recorded fall geometry's own consequence), the walks to Malby, the fall t=2824 with the fund 18, the collection, two aftermath crossings; the close paper 0 / coin 8, the heap 18, seven crossings + seven banks, the tale 87 lines, every rs-2..6 surface carried; the heartbreak chain: 43 events, the tale 24 lines, the fail-then-pass, the echo 40→80, rs-7/8's lines; both byte-identical on regeneration; the runner + the kit outside the repo, Rule 9), the author audit pre-set BEFORE the reading (the repo's recorded pass bars — the LLM band's own, the convergence question stated) — the human reading itself + the convergence assessment the owner's side, never a sandbox claim — WORLD_TESTS §9's W5 entry; 5 paths doc-only (the state docs — iter-204's own class)
- iter-206 · 2026-09-23 · heartbreak-subject (rs-8) — the heartbreak station's SECOND fix attempt landed and the re-run's MANDATORY PAIR MET at the strict n=2 bar (the owner's further-route call over the iter-205 subject problem, STATUS item 1 — the dead as the loss's grammatical subject): the mourning line's clause RE-SUBJECTED ("their own futures the flood took down with them, the line, the duties and the holdings that were to be theirs" — the futures theirs, removed with them, the flood the remover; the transmission vocabulary gone; the echo line untouched per its 1/2 confirmation; zero code, zero corpus price, the LOG untouched, the pins updated) and the same probe re-run (the iter-204 protocol re-established, the runner + the reader prompt rebuilt outside the repo — Rule 9, the audit pre-set before the reading, glm n=2): the lost-future half MET n=2 convergent (both readings quoting the re-subjected clause verbatim, the loss predicated of the dead's own futures — the inheritance-character failure mode GONE), the opened half MET 2/2, the supporting bars MET n=2; the anti-loop law not tripped — the station PARTIALLY CONFIRMED (the human band open, the discovery-path residues standing) — WORLD_TESTS §9's W5 entry; 7 paths (the pack line + the pin + the state docs — the rs-landing class)
- iter-205 · 2026-09-23 · heartbreak-fix (rs-7) — the heartbreak station's minimal RENDERING FIX landed and measured (the owner's minimal-fix call over the iter-204 failure, STATUS item 1 — the 40/80 + fail-then-pass + second-holder residues and new mechanics explicitly excluded): TWO template lines re-authored (the mourning line carrying the line/duties/holdings never-handed-on, the echo line the table-open forward frame — zero code, zero corpus price, the LOG untouched, the pins updated) and the same probe re-run (the iter-204 protocol re-established, the audit pre-set before the reading, glm n=2): the opened-option half extracted CLEANLY once (the table-open clause verbatim + the forward synthesis), iter-204's zero-futures mode GONE n=2 (both readings carrying the inheritance topology), the mandatory pair still NOT MET at the strict n=2 bar — the dead still not read as the futures' own holders (the subject problem); the further route the owner's call — WORLD_TESTS §9's W5 entry; 7 paths (the pack line + the pin + the state docs — the rs-landing class)
- iter-204 · 2026-09-23 · heartbreak (the W5 heartbreak station's first probe run) — the trio's last station's measurement RAN (the owner's «давай прогон зонда» call, STATUS item 1): the return's chain walked deterministically at seed 42 (the package the same bounded form — the tale + the records + three briefs, byte-identical twice), the author audit pre-set BEFORE the reading with F02's option-topology vocabulary, the blind reader glm n=2 (the runner + transcripts outside the repo, Rule 9); the mandatory bar's future-option half NOT MET (the drowned generation read as remembered dead by both, never as removed futures — the rendering boundary: the loss's option topology renders nowhere), the opened-option half carried as present standing, the supporting bars (relation / memory / world-specificity) MET n=2 convergent; the fix's route the owner's call — WORLD_TESTS §9's W5 entry; 5 paths doc-only (the state docs)
- iter-203 · 2026-09-23 · winterkin (the W5 heartbreak station's design material) — the winter kin's embodiment landed as pure pack data (the owner's queue-order call «withhold → the heartbreak probe», STATUS item 1, the intake-36 C03+F02 consult): ANCHOR_REGION §6.3's three gaps answered (the kin pair axis + the bilateral inherited seed, the read_kinmark proof hinge minting the_winter_kin, the say_the_names mourning) + the formation side tested in a committed pack (share_board's on_action climbs, both sides to the bar 80 — the first co-presence-formed relation) + the claim_kinmark door (the leverage gate, the F02 criterion's mechanical form); the corpus price paid deliberately (the son hears the wergeld count, the golden regenerated — the iter-157 precedent); the PROBE RUN the station's next beat — WORLD_TESTS §9's W5 entry; 15 paths (the pack's four + the golden + the three pin updates + the claim packet + the state docs)

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
- `rs-5` · the shave's agency gloss — done (iter-201, the owner's queue-order call «agency → withhold → the heartbreak probe» firing STATUS Next step item 1 — the covering residue's first measured successor, the discovery path's own half): the direction of action on the reader surface, the rs family's fifth member (rs-3's own row re-authored — the measured motivation: the iter-199 re-run's readers carried the temporal tie "since the shave" but never WHO shaved whom, reading 2 INVERTING the direction (the camp the accused), reading 1 floating the withhold as private sale) — the bloom kind's gloss origin clause re-worded from the spine's own committed words ("since the guild factor shaved the camp's weight": the actor, the act, the patient on every banking line + the crofts' state apposition), the mechanism UNCHANGED (rs-2's mapping, zero code, zero corpus price), the pins updated as the deliberate act (tests/test_accountgloss.py + test_flowgloss.py + test_freightvol.py). The probe's re-run on the fixed surface: the MANDATORY BAR MET (glm n=2 convergent — the guild the shaver, the camp the shaved, the inversion GONE, the withhold read as the camp's answer); the honest residues: the shave's temporal placement (the arc's assembly's remaining half) + the withhold's one-surface contradiction (the queue's next row). Detail: WORLD_TESTS §9's W5 entry.
- `rs-6` · the withhold's one-surface contradiction — done (iter-202, the owner's queue-order call «withhold → the heartbreak probe» firing STATUS Next step item 1 — the iter-199/201 measured residue): the heap's meaning + the fund's climb + the beam's law joined as the camp's ANSWER to the tilted beam, the rs family's sixth member (the mechanism rs-4's own — the withhold's deliberately-unglossed flow slot filled: ONE `flow_glosses` row for `the_withhold_banks`, authored from ANCHOR_REGION §6.4's CONSEQUENCE row — "the camp's answer to a tilted beam: unweighable at it, the paper still paid" — riding the banking line beside rs-3/5's kind gloss, zero code, zero corpus price; the pins updated as the deliberate act); the probe's re-run MANDATORY BAR MET (glm n=2 convergent — the contradiction JOINED in both readings, the heap never commerce, the regression bars held; the honest residues: the shave's temporal placement + the tally unconnected + the reckonings undiscussed — WORLD_TESTS §9's W5 entry). Detail: the test packet's claim block + WORLD_TESTS §9's W5 entry.
- `rs-7` · the heartbreak station's future-option rendering — done (iter-205, the owner's minimal-fix call over the iter-204 measured failure, STATUS item 1 — «поправить две существующие поверхности heartbreak», the 40/80 + fail-then-pass + second-holder residues and new mechanics explicitly excluded): the loss's future-option dimension + the claim's forward framing on the reader surface, the rs family's seventh member (the measured motivation: iter-204's future-option half failed at the rendering boundary — the drowned generation carried as remembered dead, zero futures vocabulary; the opened option carried as present standing) — TWO template lines re-authored (the mourning line `the_names_kept` carrying "their line, their duties and their holdings never handed on" — the owner's called vocabulary; the echo line `the_edge_answers` carrying "the crossing's table open to the claimant's line from this day" — the opened possibility, never only the standing), zero code, zero corpus price, the LOG untouched; the pins updated as the deliberate act (tests/test_winterkin.py). The probe's re-run on the fixed surface (the iter-204 protocol re-established, the audit pre-set before the reading): the mandatory pair NOT MET at the strict n=2 bar — the MEASURED MOVEMENT: the opened-option half extracted CLEANLY once (reading 2's verbatim table-open quote + the forward synthesis — the echo route CONFIRMED at 1/2), iter-204's zero-futures mode GONE n=2 (both readings carrying the inheritance/obligation topology — reading 2's "not of wealth or land" the holdings' exclusion), the dead still not read as the futures' OWN holders (the subject problem: the mourning line's clause resolves to the inheritance's character); the further fix's route the owner's call. Detail: the audit artifact's verdict block + WORLD_TESTS §9's W5 entry.
- `rs-8` · the heartbreak station's re-subjectivation — done (iter-206, the owner's further-route call over the iter-205 measured subject problem, STATUS item 1 — «мёртвые как грамматический субъект потери», the echo half confirmed at 1/2 and left untouched, the discovery-path residues each its own surface's question): the dead as the loss's grammatical subject on the reader surface, the rs family's eighth member (the measured motivation: iter-205's mourning-line clause resolved in both readings to the inheritance's character — what the claim brings or excludes — never to the dead as the futures' own holders) — ONE template line re-authored (the mourning line `the_names_kept`: iter-205's "their line, their duties and their holdings never handed on" replaced by "their own futures the flood took down with them, the line, the duties and the holdings that were to be theirs" — the futures THEIRS, removed WITH them, the flood NAMED as the remover, the transmission frame's vocabulary gone entirely), zero code, zero corpus price, the LOG untouched; the pins updated as the deliberate act (tests/test_winterkin.py). The probe's re-run on the fixed surface (the iter-204 protocol re-established, the runner + the reader prompt rebuilt outside the repo — Rule 9, the audit pre-set before the reading): the MANDATORY PAIR MET at the strict n=2 bar — the lost-future half MET n=2 convergent (both readings quoting the re-subjected clause verbatim, the loss predicated of the dead's own futures — "their entire potential" / "a complete erasure of a line and its potential"; the inheritance-character failure mode GONE), the opened half MET 2/2 (up from 1/2, the echo line unchanged); the supporting bars MET n=2 convergent (the second-holder structure carried by BOTH this run); the station PARTIALLY CONFIRMED (the humor station's own form — the human band open, the discovery-path residues standing). Detail: the audit artifact's verdict block + WORLD_TESTS §9's W5 entry.
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
