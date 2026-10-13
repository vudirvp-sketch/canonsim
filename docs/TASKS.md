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

- `m4-r` — THE M4 R-arm (DELIVERED iter-357 + STATION RUN
  iter-358 + FLAG FIX iter-359 + VERB FIX iter-360 + FULL RUN
  READ iter-361 — the row is COMPLETE, awaiting the owner's
  M2/M3 decisions): `canonsim_m4_station_pack` v4.3 — the
  pinned b11541 CUDA installer + the model doctor + the R
  battery + the G control + the RU band + the det + the gate
  sweep. THE FULL RUN (m4_20261010_170258.zip, read iter-361):
  the FIRST complete station run of the series — zero crashes,
  the Verb fix proven LIVE (s4's fire cascade committed by the
  real door: drop_break → fire_started back_wall → fire_spread
  woodpile → smoke_rising → location_burned_out → flee); the
  fourth byte-identical run (s1..s3 match v4.1 + both v4.2
  exactly); 0 inventions / 42 docs + output_tokens=[0] ×42
  (0/132 series-wide); med 0.556 s; the sweep monotone
  67.7/87.1/96.8/100%@0.5/0.4/0.3/0.2. THE RU BAND ANSWERED:
  every gate-passed Russian row assembled PERFECTLY (5/5
  kind+target); all 5 misses are the gate's 0.38–0.49 threshold
  on low-agency verbs — comprehension is NOT the problem, the
  threshold is the knob. THE G CONTROL like-for-like: R full
  38.1% vs G 21.4%, R max 0.796 s vs G max 2.907 s. The M2/M3
  decision material: iter-350 §G + iter-361 §G. Detail:
  iter-357-m4station-report.md + iter-358-m4station-run-report.md
  + iter-359-m4flags-report.md + iter-360-m4verbfix-report.md +
  iter-361-m4fullrun-report.md.

- `m5-station` — DONE (iter-365 the agent half + iter-366 the
  reading half: the owner returned `m5_20261011_002908.zip` —
  the FIRST FULL m5 run, all 9 stages, zero crashes, pack v5.0 on
  the 3080 Ti («both models FULL offload» — CORRECTED iter-368:
  the logs carry zero CUDA lines, KI#119, the band was CPU; every
  m5_report number
  re-derived from the raw jsonl, the false-allow policy
  reconstructed with 0 divergences). THE M3 LIKE-FOR-LIKE CLOSED
  (iter-361 §G's ask — one corpus, one session, one main spawn):
  R the verdict-path leader (full 16/38.1% ×1.8 over G/H; the
  target class 1 vs 8/10; med 0.52 s vs 7.31 s; output_tokens=[0]
  ×54; det identical — the FIFTH byte-identical R run; the det-g
  digest gap closed: c2e33bd90d353d2b) + THE VERDICT-LAYER
  READING, CORRECTED iter-367 (KI#118 — the owner's counter-check
  reproduced exactly: reply bytes G/H0 37/42, G/H8 30/42; census
  40/42, door 37/42; the 42/42 byte-identity claim was never
  byte-checked and is FALSE; the hybrid MOSTLY preserves the
  verdict — a statistical reading, never a byte law — and buys
  prose, not verdict quality); the terminated-prose
  law held on station (41/42 stop; two eos_held = the 416-token
  ceiling; h8's 1 json_bleed — the door safe, the flag fired) +
  THE M2 KNOB LEDGER: EN 0.5→0.4 correct 15→20 / misses 10→4 /
  nonintent-false 4→7 / object-false 4=4 INVARIANT; RU correct
  4→6; precision on passed FLAT (60.0→58.8%); the bands OVERLAP —
  no separating threshold, the structural cost the nonintent
  family the gate cannot see; the m4 parity (R census
  byte-identical, the s4 cascade, s7cy0 1:1); inventions 0/108
  (0/240 series-wide). THE M2/M3 DECISIONS RECORDED (the owner's
  2026-10-11 call — DECISIONS D-250: R at the door / prose a
  separate surface / production stays the L12 template rung /
  H not promoted on m5; 0.5 default / 0.4 the recall-oriented
  override with its measured cost; runtime only on the separate
  promotion permission). cuda_gate.bands still {} (the
  formalized band sweep unexercised — a candidate for the next
  station flags). Detail: iter-365-m5station-report.md +
  iter-366-m5read-report.md + iter-367-m5correct-report.md.

- `m6-station` — DONE (iter-368 the R-promotion pack + iter-371
  the KI#120 fix + **iter-374 THE STATION RUN READ** — the
  promotion series m4→m6 COMPLETE; the owner's run
  `m6_20261012_063055.zip` on THE v6.2 PACK (the iter-372/373
  interlude recorded in-repo by iter-374 §0: KI#121 the argparse
  `%` crash + KI#122 the band instrument's false negative —
  both proven live by the run); EVERY m6_report number re-derived
  from the raw records, ZERO divergences (per-row censuses 1:1
  on 54 rows; the windows reconciled — input med 1531 = R+RU);
  THE BAND QUESTION CLOSED: markers -lv 4 in both logs
  (load_backend/device_info/ggml_cuda_init; FULL offload 33/33 +
  43/43) + the physics (Gemma prefill med 4015/max 4445 tok/s,
  decode med 68; the router ≥2800 tok/s inside the 0.546 s wall)
  — the m4/m5/m6 latencies were ALWAYS the CUDA band, KI#119
  re-read, the m4 GPU readings RESTORED; R the production form:
  full 16 (38.1%)/kind+ 21 (50.0%) — EXACTLY m5's numbers, det
  router identical 962b30a4… the SIXTH byte-identical R run, g
  c2e33bd9… the second; 0/42 inventions (0/282 series),
  output_tokens [0]×42; THE DRIFT COLUMN reads the GOLD
  trajectory live (the reference commits: s4 6→7→8→13→14, the
  fire cascade 15 events through the real door; R CLEAN 23/42
  full 43.5% vs G CLEAN 13/42 full 23.1%, R drifts less
  19/42 vs 29/42); the standing watch armed: EN
  correct 15/FALSE 10/blocked 17 @0.5 (m5's classes exact), RU
  correct 4/FALSE 1 (ru_05 the series-constant texture pin);
  narrate 20/20, r==gold prose 7/10 (s4 cascade identical);
  station Python 3.14.3 (the log-header env datum). THE
  RUNTIME PROMOTION remains the owner's separate permission
  (D-250) — its measured basis now COMPLETE. Owner-side
  housekeeping: drop the v6.2 zip into docs/station/archive/
  (the pattern's fourth instance). Detail:
  iter-368-m6promotion-report.md + iter-371-refemit-report.md +
  iter-374-m6read-report.md + the packs
  docs/station/archive/canonsim_m6_station_pack_v6.0.zip and
  …v6.1.zip (v6.2 — the owner's local copy).

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
- `doc-4` — DONE (iter-343, R1 doc-only — the owner's 2026-10-08
  repo-revision call: clean the docs of the stale Redot-era
  frontend-wrapper information): FRONTEND_WEB_LAW §14's Phase 1
  LANDED — the law bodies re-homed (Redot → historical/reference-only):
  the five live laws (FRONTEND_UIUX_LAW / WORKBENCH_APP_LAW /
  WORLD_PRESENTATION_LAW / LLAMA_CPP_INFERENCE_CONTROL_LAW /
  VISUAL_SYSTEM_UI) name the web client as the presentation runtime,
  the dead REDOT_ENGINE_INDEX routing replaced by the D-245 archive
  routing everywhere it survived; the TASKS DONE rows (wb/ux/obs/inf)
  collapsed to the landing-record form (the §8-report restatements
  cut — the detail verbatim in git + CONTRACTS §5). Detail: the
  iter-343 report + git.
- `mech-2` — the agent impact surface — DONE (iter-196, the owner's
  «открывай mech 2» call; `mechanics impact --path <pack path> |
  --ref <name>` the derived reader index (the AST scan, D-118
  extended) + the exact-name reverse query (the rename-safety set)
  + the indexed-matrix pointers (D-024); bounded one-hop;
  tooling-only, stdlib-only (D-012), zero runtime change. The A/B
  falsifier RAN (iter-198; TECH_NOTES §17): the injected gate moved
  none of the three metrics — the premise refuted at scale, the
  whole-file emission wall + the silent notes paraphrase measured
  instead; the structured-patch proposal PARKED behind a minimal
  prototype; the rename-safety lint gap closed as `rename-1`.
  Detail: iter-196/198/200 + D-197 + git.
- `wb-1` — DONE (iter-215 the Python half + the contract; iter-216
  the presentation half + the live double-run PNG byte-diff proof —
  the v5.2 brief's first row, D-200 the admission, CONTRACTS §5 the
  pre-implementation contract): the Workbench vertical seam — the
  chain `known fixture → typed read model → Visual Scene IR →
  composition → screenshot artifact`; the Python half
  (`workbench/scene_ir.py` + `workbench/scene_build.py`,
  present_in_order the one presence law) alive; the presentation
  half was the Redot composition, DELETED at iter-290/D-245 (the
  web client the active consumer). Detail: CONTRACTS §5 + git.
- `wb-2..wb-12` — DONE (iter-217..230, the brief's own order, one
  row per landing; the per-row landing records verbatim in git
  history): the Workbench application stack — wb-2 the shell + the
  semantic-token theme; wb-3 `workbench/application/`
  (identity/artifact/directories/clock); wb-4 `workbench/api/` the
  socket-free gateway + `transport.py` the loopback binding (INV-4's
  second sanctioned module, D-201); wb-5 `operations/` (the §11
  lifecycles, the §12 deadline/cancellation run registry, the
  model-discovery half — chat.send honestly deferred to its
  consumer, the admission law); wb-6 the backend row
  (`operations/backend.py` the typed BackendPort + chat.send +
  model.load/unload over the OBSERVED ladder, D-203); wb-7
  `scripts/workbench_app.py` the composition root + the live chat
  circuit; wb-8 `platform/llama_process.py` the managed llama-server
  process row (D-205); wb-9 the model-flow row
  (`platform/model_fetch.py` INV-4's third sanctioned module, D-208,
  + the launch-settings store + the runtime layout +
  `scripts/workbench_launch.py` the zero-command launcher); wb-10
  the owner-experience rework (model.import the local native-picker
  arrival, NO network, D-209); wb-11 the transport-chain row (the
  load/unload runs' fast dispatch, the pipe drains, D-210); wb-12
  the token-audit row (theme@0.3 + the chat follow law, D-212). The
  Redot frontend halves (shell.gd & co.) DELETED at iter-290/D-245 —
  the web client (`frontend/`, D-244) the active consumer; the
  exported-Windows-build row PARKED per AGENTS §2.4 (the Redot
  export form died with the tree; the product form re-scoped to the
  web client when the owner calls it). Detail: CONTRACTS §5 + git.
- `wb-13+` — the family's forward rows (owner-gated, each fires on
  the owner's call — the brief's §32/§46 ladders: live events +
  reconnect/resync + the idempotency/revision/lease tests at live
  scale; persistence; the frontend continuation rows — inference,
  history, diagnostics, the CanonSim seam, the asset vocabulary; the
  visual rows per VISUAL_SYSTEM_UI §10). Never speculative — a row
  opens only when the owner names it. Redot/Godot engine questions
  route to the archived pack's reference docs
  (`docs/frontendweb/archive/`, D-245 — the repo's engine index
  deleted, never a repo file again); visual/UI facts for any wb
  row: `docs/VISUAL_SYSTEM_UI.md` (the surface-driven grammar + the
  token taxonomy + the state matrix, D-211).
- `ux-1` — DONE (iter-234): the P0 UX minimums over the then-Redot
  shell (deleted D-245) — the string catalog, the motion policy, the
  responsive bootstrap, the keyboard path; the lessons carry to the
  web client as PRINCIPLES (STATUS FAQ's Redot-era entry). Detail:
  git.
- `obs-1`/`obs-2` — DONE (iter-235/236): the Observatory frontend
  entry — the IA regions + the interaction grammar (obs-1); the
  read-side seam + the feeds (obs-2: `workbench/observatory_read.py`
  + `workbench/application/operations/observatory.py`, the
  boundedness ceiling ONE, selection by event ID, the distinct
  empties). The live surfaces now the web client's Observatory
  feature (`frontend/src/features/observatory/`); the obs-3+ P3
  rungs the owner's call. Detail: OBSERVATORY_LAW + git.
- `obs-3..obs-N` — the Observatory continuation family (each row
  owner-gated, the LAW §25 ladder): the P3 rungs after obs-2
  (timeline lanes, compare arms, semantic zoom, cross-highlighting,
  Evidence Capsules, persistent research contexts) + the question
  editing form when its consumer names itself.
- `inf-1`/`inf-2` — DONE (iter-239/240): the llama.cpp
  inference-control family —
  `docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md` (D-219) the binding
  owner + `workbench/application/inference/` the control library
  (the three-layer split: raw capability / semantic control / UI
  projection; the whole reviewed control set; the typed relations;
  the deterministic resolver; the compiled launch surface; the
  profile store + the one-way migration; the extra_args
  duplicate-ownership guard) + the gateway family
  (inference.read/update). The Inference surface now the web
  client's feature (`frontend/src/features/inference/`); the inf-3+
  continuation rows the owner's call. Detail: the law + git.
- `inf-3..inf-N` — the inference continuation family (each row
  owner-gated, LLAMA_CPP_INFERENCE_CONTROL_LAW §21's ladder): the
  capability discovery + the context-aware/model-driven visibility +
  the session/preset persistence layers above, never one "advanced
  flags" bucket.
- `core-1` — the cross-cutting execution/scale research family (PARKED, owner-gated; source: the ingested suite's CORE_WORLD half, iter-311/D-251 — the archive zip's `CORE_WORLD/04+05`): C1 representation continuity (macro↔meso↔individual causal obligations under a representation change), C2 compiled/indexed execution (index-superset — no false negatives; exact verification; the same EventDraft commit path), C3 history/replay scale (measure checkpoint/replay/index-rebuild costs before touching canonical storage), C4 the LLM boundary under unusual interaction (multi-intent/novel/hidden/partially-realized/canon-conflicting), C5 shared semantic equivalence (the byte-identical replay contract the bar). RESEARCH/POC-ONLY, nothing approved runtime architecture; a row opens on a named consumer + a measured native limit + a falsifier (the world-track §2 promotion gate's form); the POC contracts open from the archive when a row fires. AMENDED iter-315 (the owner's same confirmation call): the POC contract set now opens from the 2026-10 concept-review package too (`docs/analysis/concept-review-2026-10/`, verbatim, md5-pinned) — D0/D3 as the law set (future-reachability / obligation-preserving refinement), the conserved-set definition, the observation-path probe (same prefix + elapsed world time + seed, different observation/refinement path → compare conserved obligations and reachable futures); the namespace fence pinned: review-C3/C14/C18 ↔ core-1-C1, review-C5 ↔ core-1-C2/C3, review-C1 ↔ core-1-C4 — mapped explicitly, never mechanically merged. Never a speculative build.
- `sem-1` — DONE (iter-316, R0/R1 definition + the live falsifier, zero code change; the confirmed queue's head, the owner's «sem1 открывай и так далее» call): the CONTRACT landed at CONTRACTS.md §6 — seven pinned decisions (S1 one semantic owner — the resolver circuit, the gate never re-derives; S2 the declared effect surface: per type the legal actor classes + the state-change family + the knowledge channels + the hooks + the postconditions, declared in pack data + the mechanic modules' named constants, NEVER per-draft; S3 the emit-side authority vocabulary with auth-1's input-side fence; S4 the pure non-resolving gate INSIDE `_commit` after the delta gate, before `writer.append`; S5 the two RED lanes — internal loud / external soft; S6 the anti-tautology law; S7 the `_commit` probe = a contract gap, never a production-exploit claim) + the producer map + the invariant set + THE CHEAPEST FALSIFIER RUN LIVE (Arm A: a real `wait` producer output + a `pc_01.position` teleport, schema-valid + delta-consistent → APPENDED `ev_0011`; Arm B: a producer output re-typed `year_turns` with actor `pc_01` → APPENDED `ev_0012`; the polluted log FOLDS CLEANLY — review-C1's risk demonstrated; the probe outside the repo per Rule 9, the artifact md5 228ea08bff…) + the future implementation row's minimal test set pinned (the two arms RED→GREEN, the corpus positive control byte-identical, the declaration-flip tautology guard, the two lanes, the INV-2 replay). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate). Detail: CONTRACTS §6 + the iter-316 report + git.
- `caus-1` — DONE (iter-317, R0/R1 definition + the live ablation falsifier, zero code change; the package's T1+T2 sequence, sem-1's natural pair): the CONTRACT landed at CONTRACTS.md §7 — six pinned decisions (K1 the causal spine `primary_cause + necessary_supports[] + provenance`, no graph — today's `cause` IS the primary-cause slot, provenance stays lineage never causal claims; K2 counterfactual necessity — the same-seed ablation makes the claimed outcome UNREACHABLE, replacements don't count; K3 the necessity-vs-evidence split — evidence lives in knowledge/projection/payload, never supports; K4 the ablation battery OFF-LINE only — the divergence-probe form, never a runtime gate; K5 the producer declares, the battery verifies — the read-set × the `_last_change` index (D-050) the derivation seed, a support surviving ablation is REFUTED; K6 compatibility + the no-DAG law — additive provenance-family field, INV-1/INV-5 + the consumers additive-only) + THE ABLATION FALSIFIER RUN LIVE (seed 8, the day1 theft scenario + one inserted perception step: BASE — the steal outcome `ev_0007` names as `cause` the CHRONOLOGICAL predecessor `ev_0006` (`look_around`) while the materially-REQUIRED move `ev_0005` is indistinguishable — the necessity real, measurable, UNRECORDED (review-C2's risk); ABLATE-MOVE — zero steal-family outcomes, the outcome unreachable (necessity); ABLATE-LOOK — the steal still fires (evidence, not necessity); the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned. The implementation is NOT a row — the owner opens it after accepting the contract. Detail: CONTRACTS §7 + the iter-317 report + git.
- `replay-1` — DONE (iter-318, R0–R1 definition + the live falsifier + ONE R2 KI fix — KI#111, found BY the falsifier, AGENTS §5's record-then-fix; the queue's head, the owner's «продолжай очередь с replay-1 и так далее» call — S1–S7 + K1–K6 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §8 — six pinned decisions (E1 the identity tuple, six components, mapped to live carriers — seed/prefix-digest/schema-version carried AND checked, pack-content digest / engine commit / execution-config digest the three named GAPS; E2 semantic identity ≠ continuation state — refusal vs staleness, never mixed; E3 the irreducible continuation state a CLOSED set — the cursor's own list, a new field declares its side; E4 the lifecycle proposed → accepted → durable → committed — a lost un-durable event NEVER EXISTED; E5 the crash contract over append-before-durable / post-durable / derived-state — loud detection everywhere, repair the implementation row's business; E6 `flush == durable` REJECTED — 0 fsync / 3 flush() audited, logical durability (D-139) proven, OS durability NOT) + THE FALSIFIER RUN LIVE (the test_resume corpus, seed 42, split after step 2: CONTROL byte-identity HELD — the law untouched; Arm A pack content drift, name@version unchanged → resume ACCEPTED, tails diverge from the FIRST appended event (17 vs 23 events) — review-C4's risk live; Arm B header.commit never read at resume, a foreign label accepted silently; Arm C no-fsync audit + torn tail LOUD (found KI#111 pre-fix) + lost pre-pin tail LOUD; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned. The implementation is NOT a row — the owner opens it after accepting the contract. Detail: CONTRACTS §8 + the iter-318 report + git.
- `scale-1` — DONE (iter-319, R0/R1 definition + the live measurement falsifier, zero engine change; the queue's head, the owner's «продолжай работу прошлой итерации, со scale-1 как я понимаю, и так далее» call — E1..E6 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §9 (review-C5/C6/C16/C28/D5+D6) — seven pinned decisions Q1..Q7 (the three work classes by CAUSAL DEMAND, never implementation shape / the explicit budget: exhaustion DEFERS as semantic debt, the due-work-vs-attempt split pinned / the canonical order stands — no scheduler machinery / the cohort's build-time commutativity certificate, no CRDT/MVCC / the measurement `world size × fan-out × operation → inspected/candidate/committed + wall time` as the admission instrument / locality = byte-identical canon / the four measured gap targets) + THE FALSIFIER RUN LIVE (the REAL core functions, real tavern config, synthetic scaled worlds, seed 4242: Arm A the beat's LOCAL demand pays pack-wide walks and O(|log|) folds — leverage 32,002 iterations at |log|=16k, decay 1,248 reads at N=384 for 80 zone commits; Arm B the spread pass's REGIONAL demand scans the WHOLE projection — 1,053 reads at L=320 for ONE burning location, flat in fan-out while committed is S-shaped; Arm C NO work budget exists, gated attempts vanish silently (canon-noise), the three deferral surfaces unbounded and unaccounted; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned (the battery as a counting-proxy harness, the locality T1 control, the budget-deferral law, the cohort certificate refusal, the deferral accounting). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate) — OPENED 2026-10-04 (the iter-329 call; the standing `scale-1-impl` row). Detail: CONTRACTS §9 + the iter-319 report + git.
- `speech-1` — DONE (iter-320, R0/R1 definition + the live falsifier, zero code change; the queue's head, the owner's «Продолжай очередь с speech-1 и так далее» call — Q1–Q7 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §10 (review-C8/C9/C10/C25/C26/D10) — seven pinned decisions (P1 the channel enumeration, six channels with their live carriers — canonical fact / knowledge-belief / perception-as-acquisition-face / structured speech act / narration / diagnostic trace; P2 free prose never canon — the closed documents, the checked-never-imported assertions; P3 the promotion path — candidate structure → the intent door → the resolver circuit → `_commit`, never a second door, the auth-1 fence; P4 channel isolation — an admitted structured act FROZEN against presentation retries, today the monolithic regen, the measured gap; P5 grounding scoped to atomic externally-testable assertions — the closed claim kinds, the closed halves referenced; P6 the epistemic scope law — actor/player/narrator/debug, irony a read-side composition never a write-side fact; P7 the explicit forgetting vocabulary + the C10 field homes — trust in the relations axes, status read-side, no belief graph) + THE FALSIFIER RUN LIVE (the REAL Simulator/Mediator/validator/ledger/knowledge, seed 42: Arm A the C8 freeze gap — the empty-prose kill + the monolithic regen, the valid take intent dying with a contradicted prose claim at 0 events/0 withdrawals/0 deferrals, freeze machinery 0 hits; Arm B the prose/canon boundary BOTH ways — prose-only → 0 events, the same content typed as `talk` → `talk`+`rumor_told` committed; Arm C the scope + forgetting — the player + actor docs each ⊆ their knower's records, zero cross-knower leaks, no holder ever dropped a token across 10,000 ticks; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned (the freeze arms RED→GREEN, the prose/canon controls, the per-knower scope fixtures, the explicit-forget fold flip, the INV-2 replay). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate). **Owner-ACCEPTED AS LAW 2026-10-04** (P1–P7 binding for every future implementation; the implementation rows NOT opened — «Строки имплементации пока не открываю», each row opens separately behind the gate). Detail: CONTRACTS §10 + the iter-320 report + git.
- `auth-1` — DONE (iter-321, R0/R1 definition + the live falsifier, zero code change; the queue's LAST row, opened by the owner's «Продолжай очередь с speech-1 и так далее» continuation — Q1–Q7 accepted AS LAW the same call): the CONTRACT landed at CONTRACTS.md §11 (review-C11/C12/C20 + M4's vocabulary/D7–D9) — seven pinned decisions (A1 the pipeline input → interpretation → classification → authorization → execution, each stage with its live carrier; A2 valid ≠ authorized — the three DISTINCT axes with distinct refusal vocabularies: malformed loud/zero events, world-impossible → the committed `intent_rejected` attempt-fact, valid+authorized → the INV-5-immutable event; A3 the INPUT-side authority classes player|NPC|director|system|pack with the S3 emit-side fence; A4 ambiguity collapses ONLY on equivalent canonical effect surfaces, the question alternative the clarify path, NO global confidence score; A5 the D7 invariant `DirectorOutput ⊆ EligibleConsequences` — the eligible set IS the seeded-hook buffer, the release paths only SELECT, the mutation probe's standing form; A6 bounded deterministic agency where a named consumer needs it — no generic planner, no LLM planner; A7 the M4 vocabulary instruction/proposal/authority/realised intervention/canonical consequence + HARD CANON — the owner's 2026-10-03 decision: no recovery/dispute path EVER for wrong-but-committed model-mediated actions, the correction form a NEW event, a retcon path REFUSED) + THE FALSIFIER RUN LIVE (the REAL Simulator/Mediator/ParserDoor/intent door/director/writer, seeds 42 + 8: Arm A the three axes — the world-impossible talk → `intent_rejected` committed ev_0006 with zero state changes, the unknown kind → the loud RunnerError at zero events, the valid move → committed, the confidence machinery 0 hits; Arm B the caller gate WITHDRAWN the guard's reply proposing the player's talk, the eligibility set enumerated (5 seeded instances) + no release-by-tag API, the invented `spawn_dragon` refused loud at the door, the writer's surface append/close only with 0 retcon hits; Arm C the question surfaced at zero events, the collapse machinery 0 hits; the probe outside the repo per Rule 9, artifacts md5-pinned) + the future row's minimal test set pinned (the three-axis fixtures, the caller-gate arms, the D7 mutation probes, the collapse's equivalence proof, the writer's append-only pin, the director's pure-selection INV-2). The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate). **Owner-ACCEPTED AS LAW 2026-10-04** (A1–A7 binding for every future implementation; the implementation rows NOT opened — «Строки имплементации пока не открываю», each row opens separately behind the gate). Detail: CONTRACTS §11 + the iter-321 report + git. THE QUEUE IS NOW EMPTY — all six contracts landed; the next moves the owner's calls (M2 station-side, the implementation rows' gates, the standing frontend/world rows).
- `lab-1` — DONE (iter-323, R2 local-add — the owner's Atomic World Lab agent-pack call «начни работу с архивом» (CANONSIM_ATOMIC_WORLD_LAB_AGENT_PACK_v1_5.zip, the pack's 04 §2 the Stage A order owner); the pack is a research program over the SAME substrate — this row is the harness landing, never an engine change): `scripts/labrunner.py` the Lab batch runner + `tests/test_lab.py` the nine Stage A laws — THE PLAYER-ABSENT LAW (the fixed declared anchor = the pack's own player position, ONE whole-horizon wait, the player authors nothing else; the anchor move only when the player does not already stand there — a rejected move is harness noise), the MINIMAL observation profile (identity/horizon/counts/mix/state/cost — derived read-side over `read_log`, no second log/RNG/scheduler/resolver, the record rebuildable from seed+pack+horizon), the experiment-contract record (`output/lab_<tag>.json`, gitignored runtime space, QUESTION/IDENTITY/ARMS/RUNS/DISPOSITION — assignment ≠ realized kept apart), the T1 double-run (`--verify-replay` byte-identity, the F1 falsifier), THE ABLATION ARM with the measured-not-inherited removable set (the dead-vocabulary fixpoint — the lint names the dead lines, the materializer strips them, bounded 32 passes; measured for province at 1y+: CLEAN on_action/reflection/secrets/factions, LINT-REFUSED urgencies/expectations/traits, RUNTIME-REFUSED weather (cadence-armed by the macro clock — the day-1 balance set does NOT transfer to long horizons) + crime_watch (a missing-block KeyError, the runtime-backstop gap recorded, never patched here)); THE E0 BASELINE MEASURED (province_pack, directors off): 10y × 4 smoke seeds — 7,861–7,865 events (seed variance ±2), ~100% autonomous, the mix 97.3% maintenance+account_flow (watch_change 7201/10y dominates), ZERO ecology-closing families (the pack's 01 §11 finding now a measured per-run law and the test suite's honest canary); the 100y deep run seed 7 — 78,212 events, 45.26 MB log, **546 s wall: the 10× horizon costs 83× time — the super-linear native work growth LIVE (scale-1's Q5 RED finding measured at the whole-run scale: the LOCAL beat demand pays O(|log|) folds)**; the E1 horizon gate: 1,000y at this native curve ≈ 90 min single-seed — the Lab's first scale datum, an input to Stage J's LOD work, never an optimization permission. NEXT: lab-2 the Tier A synthetic fixture (the 02 §12 smallest world — 1 settlement, sources, 10–20 adults — as a NEW content pack through the full admission lint), then the A/B battery deepening. Detail: the labrunner docstring + the iter-323 report + git.
- `lab-2` — DONE (iter-324, R2 local-add — the owner's «продолжай lab2 и так далее» call, the pack's 04 §3 Stage B the first entry; the fixture IS the deliverable, zero core/sim/render change): `content/farstead_pack/` THE TIER A SYNTHETIC FIXTURE (the 02 §12 smallest world — 1 settlement (the green carries storage + exchange), 4 finite sources + regrowth flows, 1 workshop + the finite rack, 1 road, 12 adults in 3 households, 4 roles) through the FULL admission lint (the sixth pack; the direct-settle hauls source→store in ONE event, the keeper's float-based meal, the on_action fatigue reply) + `tests/test_farstead_pack.py` the nine Tier A laws (the lint, the shape, the player-absent+T1, THE LOOP CLOSES — every L1 edge live, CONSERVATION exact per kind, THE ANCHOR PAIR — the LOD datum, the removable set re-measured, the deferred-realize law) + the labrunner's honest account-verb disposition line; THE E0 MEASURED: the anchor pair 10y × 4 seeds — square 933–971 events with the material cycle SEED-INVARIANT (132 account events, every seed — the year clock's determinism) vs road 165–187 events (the frozen diorama: the sources regrow untended, the store untouched, the boy's talk the world's one active voice); the 100y deep run square seed 7 — 8,663 events / 51.2 s: **THE DEFERRED-REALIZE LAW AT WHOLE-HORIZON SCALE: 94% of the century's autonomous life discharges in the final ~10 ticks (temp-1/D-236 measured — the mid-wait log is the scheduled machinery alone, 5 events/year); the herd tail ~5,400 door-rejects = p × beats × years (the protocol's noise law)**; the per-block findings: the one-goal-per-verb + one-target laws force THE HAUNT MODEL (no commuter form — the direct settle is the honest round), the chained round CANNOT roll (the second verb's gate reads pre-first state — the float law), the rack empties at year ~6 (no conversion primitive — the Stage B gate's own input), the tools pile unconsumed, regrowth uncapped; the removable set for farstead: urgencies + on_action BOTH CLEAN (province's verdicts do not transfer — the re-measured law); the stoplist's sixth list + the economy test's fourth armed consumer. 2576+1 + ruff + docguard + topology clean (INV-1..5 untouched, the LOG untouched, zero corpus price; NO test deleted or weakened — 10 added). NEXT: lab-3 the A/B deepening (paired seeds, the segmented-wait protocol row the owner's call — the deferred-realize finding's answer) + the Stage B contract rows (transformation/wear/bounded sources) behind their gates. Detail: the pack's own notes + the iter-324 report + git.
- `lab-3` — DONE (iter-325, R2 local-add + ONE R2 KI fix (KI#112, found BY the batteries themselves) — the owner's «продолжай lab3 и/или можешь прогнать полную батарею 100y×4 сида (~4 мин) для репортажа» call, the row the iter-324 NEXT named; the pack's 04 §8 experiment-contract form (QUESTION/ARMS/REALIZED_DELTA/DISPOSITION) made executable; zero core/sim/render change): THE PROTOCOL ARM in `scripts/labrunner.py` (`--protocol whole|segmented|paired` + `--segment-ticks`; the new law 7: the player authors NOTHING but null waits — segmentation changes WHEN the world moves, never WHAT the player is; `whole` stays the DEFAULT, byte-compatible with every prior record) + the lab-3 metric block in the MINIMAL profile (the MID-HORIZON LIFE profile — autonomous non-machinery events per year-span, the deferred-realize discriminant; the FINAL MATERIAL STATE — per-holder account levels read from the fold, the 03 §8 REALIZED_DELTA surface; `player_waits`) + the paired record (per-seed whole-vs-segmented deltas: events, life spans, account verbs, the final material state, wall) + `tests/test_lab.py` the four lab-3 laws (the step-list law — whole ONE wait / segmented N waits summing EXACTLY to the span with the remainder tail, the years=1 boundary coincidence; the segmented player-absent + T1 byte-identity; THE MID-HORIZON LIFE DISCRIMINANT — whole `[0, 0, total]` 100% final vs segmented every year live; the paired record's REALIZED_DELTA executable + the verdict live) + KI#112's log-identity fix (the run tuple (seed, anchor, horizon, arm, protocol) joins the log filename — two prefix collisions found by the batteries: the road run overwrote the square logs, then the 10y overwrote the 100y); THE BATTERY MEASURED (farstead, directors off): the 100y paired × 4 seeds — whole 8,564–8,749 events, life 100% at the horizon's final boundary (the deferred-realize law at century scale) vs segmented 12,212–14,038 (+42–61%) with life in 100/101 spans (1% final); **THE REALIZED DELTAS LIVE ON EVERY SEED** — the verb deltas SEED-INVARIANT (consumed +394, settled +395, every seed — the year clock's determinism), the material delta IS the two different worlds: whole leaves ~200 of each kind ON THE STORE (the century realized as ONE deferred batch: meals 28, meal_eased 3, decay 49) vs segmented the store near-EMPTY with ~200 ore+wood on the RACK (the steady flow: meals 422, meal_eased 267, decay 5,417 — the fatigue cycle arms with the meal cycle); **THE CONTROL FAMILY: talk 3,209 = 3,209** (protocol-invariant — the beat rolls never move; the divergence enters exactly where the gates read MUTABLE state) + the road diorama pair (life totals 1,072 = 1,072 invariant — the diorama's one voice defers under whole, spreads under segmented, the material stays frozen: the LOD gate WHO-rolls orthogonal to the protocol WHEN-realizes); **THE COST DATUM: segmented 20–22 s vs whole 51–53 s per century-seed (2.5× FASTER — the whole protocol's "cheap" century was an illusion of deferral: the final drain pays the ~8,000-intent herd against the fat end-state)**; the granularity datum: day-waits at 2y — 720 player waits = 42% of the log (the daily form's noise law). NEXT: the E1 horizon row (the segmented 1,000y probe — the measured curve (0.26s/2y → 20.4s/100y, ~t^1.3) says minutes, the whole 1,000y stays the lab-1 ~90-min gate), the Stage B contract rows (transformation/wear/bounded sources) behind their gates, the scale-1 follow-up (the wall-cost decomposition: WHY the deferred herd pays 2.5× — a named gap, never guessed). Detail: the labrunner docstring + the iter-325 report + git.
- `lab-4` — DONE (iter-326, R2 local-add — the owner's «продолжай» continuation call, the E1 horizon row the iter-325 NEXT named; zero core/sim/render change): the lab-4 REPLAY-COST instrument in `scripts/labrunner.py` (the pack's 04 §12 horizon battery made executable: `read_seconds`/`fold_seconds`/`replay_alloc_peak_mb` — the read-side cost split a resume/replay pays, the tracemalloc peak honestly labeled as interpreter allocations, NEVER the OS RSS, portable to the owner's Windows station) + the two lab-4 laws in `tests/test_lab.py` (the instrument law — every record carries the block on both protocols, a non-empty log pays real read+fold time; the KILOYEAR ARITHMETIC law — the step-list is a pure function of (years, segment_ticks): 1,000y segmented = EXACTLY 1,000 cadence waits, custom segments sum EXACTLY to the span, whole stays ONE wait at any horizon — zero corpus price) + THE E1 SEGMENTED LADDER MEASURED (farstead, seed 7, square, year-segmented, 2y→650y in eight rungs; 650y = 81,823 events / 465.22 s — the deepest rung the sandbox's 600-s window holds, the window itself measured honestly: background processes do not survive the tool-call boundary) + THE STATION HORIZON PROBE v1 (outside the repo per Rule 9, the session's offload rule — the kiloyear paired battery rides the owner's hardware: preflight → sanity (2y paired + T1 on the station) → control (100y paired, the cross-hardware wall) → MAIN (1,000y paired, whole + segmented + the kiloyear REALIZED_DELTA) → package (records + raw logs md5-pinned, one zip); every stage a checkpoint in try/except, a fallen stage never stops the rest, a stage timeout is itself a datum; self-checked end-to-end in-sandbox) + THE MEASURED E1 FINDINGS: the wall curve STEEPENS monotonically (local exponents 1.00→1.05→1.20→1.34→1.59→1.68→1.81 — the t^1.3 forecast from iter-325 REFUTED at depth: 1,000y ≈ 930–1100 s on the sandbox CPU, 16–18 min, not "minutes"; events stay linear 122–132/year — the super-linearity is the per-EVENT cost growth, never the count), THE FLAT-LIFE LAW (life ~71–72/year from 10y to 650y, 650/651 spans live — a 325× horizon range with zero life trend: the year-segmented world is a stable annual cycle, no collapse, no explosion; the deferred-realize law's kiloyear answer), THE LINEAR VERB LAWS (sourced 4.00/year EXACT, consumed 4.03, settled 8.03 — iter-325's seed-invariance now measured across SCALE to 6.5 centuries), THE CONSTANT-STATE LAW (projection_entities = 25 at 100/500/650y — the state never grows with the horizon, only the LOG does; the accounts pile linearly ~26.3 units/year: water 1,060→6,560, the Stage B bounded-source falsifier measured at 6.5-century scale; the super-linear wall at CONSTANT state = the scale-1 decomposition's named gap, never guessed here), THE REPLAY-COST DATUM (read-bound: 0.62 s/MB flat, the fold near-free 0.055 s at 81,823 events, the alloc peak 3.34× the log, all linear — a resume pays O(log bytes), the state never participates in the price). 2582+1 + ruff + docguard + topology clean (INV-1..5 untouched, the LOG untouched, zero corpus price; NO test deleted or weakened — 2 added). NEXT: the owner runs the station probe v1 (the kiloyear pair + the cross-hardware wall), then the Stage B contract rows (transformation/wear/bounded sources — the falsifiers measured), the scale-1 wall decomposition. Detail: the labrunner docstring + the iter-326 report + git.
- `stageb-1` — DONE (iter-327, R0 definition, ZERO code change — the owner's «продолжай работу» call after the station zip's in-session analysis; the row the iter-326 NEXT named first after the station run): THE STATION KILOYEAR DATUM ANALYZED (the owner's `horizon_station_20261004_112903` zip, v2.1 probe, Python 3.14.3/30.9 GB/HEAD febab32: preflight + sanity 2y + control 100y + MAIN 1,000y paired ALL ok; T1 byte-identity HELD on the station; the control 100y pair byte-for-byte the sandbox's own numbers (8,663/13,234) — the cross-hardware determinism law; station ≈ 1.20–1.24× faster): THE KILOYEAR PAIR — whole 86,265 events / 3,306.63 s / life 81,214 in ONE final tick vs segmented 126,392 / 884.39 s / 71,798 life in 1000/1000 spans (the flat-life law at the kiloyear: 71.8/year); THE CONTROL FAMILY talk 32,165 = 32,165 EXACT; THE VERB LAWS sourced 4,000 = 4.00/year in both arms; THE KILOYEAR REALIZED_DELTA — the Stage B falsifier in its final form: segmented leaves loc_workshop ore 2,004 + wood 2,012 = 4,016 units DEAD at tool = 0 (the conveyor delivered, nothing transforms), whole leaves ~200/kind on the store with the workshop untouched; tools 8 at the square UNCONSUMED a millennium in BOTH arms (no wear); the spring 10,060 = 60 + 10/year EXACT linear (no cap); THE WALL DATUM — the iter-326 forecast HELD (sandbox-equivalent ≈ 1,061 s vs the predicted 930–1,100), and the in-session cProfile decomposition (10y vs 100y, farthest seed 7) NAMES the super-linearity's mechanism: TWO quadratic read-side members — `occ_breaking_cause`'s full-log refold per OCC rejection (per-call ×9.51) + `knowledge._novel_facts`' whole-knowledge re-ranking per talk (per-call ×9.17); the A·t + B·t² model reproduces the α-ladder (1.01→1.83 model vs 1.00→1.81 measured) and explains 77.5% of the kiloyear wall — the scale-1 decomposition's answer, measured not guessed + THE CONTRACT LANDED at CONTRACTS.md §12 — eight pinned decisions (B1 one substrate — the account primitive, never a second mechanism / B2 the conversion verb: ONE atomic recipe event, the settle precedent, conservation PER RECIPE, the float law respected by construction / B3 the wear law: per-USE integer consume on the named instrument, never wall-clock, break-at-zero the door's soft arm / B4 the bounded source: the mint's min() cap, silence at full — the every-miss form / B5 the unarmed law — zero events without pack declarations, the golden fixtures byte-identical / B6 the REALIZED_DELTA oracle — acceptance MATERIALIZED: the dead pile dies, the linear piling breaks at the cap, the instrument turnover bounded / B7 the cost law — every new read surface index-based (the _last_change pattern), never a log scan: the measured wall law makes any O(|log|)-per-event surface RED at the row's own gate / B8 the pack-data boundary + the promotion gate — additive enum values, no schema break) + the falsifier pointer block (the three gaps' measured records: iter-324 + iter-326 + the iter-327 report §B, md5-pinned) + the future row's minimal test set pinned. The implementation is NOT a row — the owner opens it after accepting the contract (the runtime-promotion gate) — ACCEPTED + OPENED 2026-10-04 (the iter-329 call, B1..B8 as law; the standing `stageb-1-impl` row). Detail: CONTRACTS §12 + the iter-327 report + git.
- `lab-5` — DONE (iter-328, R2 local-add — the owner's «инструментальную строку scale-1 в labrunner» call (the row the iter-327 NEXT named first), the same message's C-13 decision recorded below; zero core/sim/render change): THE WALL-DECOMPOSITION INSTRUMENT in `scripts/labrunner.py` (`--profile-depths 10,100` — the first seed once per depth under cProfile; the record gains the `profile` block: the member split by entry CUMTIME over a documented map — occ_refold (the OCC prefix refold) / knowledge_rerank (_novel_facts) / beat_rolls / decay_walk / the derived folds BY CALLER (the clock's greedy `_run_beat`+`_run_macro` path vs the intent door's lazy `_fold_reads`) — plus the ULTIMATE pack's counters made executable: E03 rule-parses/beat (the `_specs` re-parse), E04 derived-read calls/beat vs the STATIC gated-entry demand (the pack's own parsers, never a second truth), beats/event; the growth block = the per-call ratios between the shallowest and deepest rung; canon_check = the instrument's own falsifier — the profiled bytes vs the unprofiled battery's at every coinciding depth, RED on breach) + `tests/test_lab.py` the three laws (the CANON-NEUTRALITY law — profiling observes, never mutates; the ACCOUNTING law — members + rest == the profiled total, the disjointness flag, E03 >= 1/beat, every fold function computed on the clock path at least once per beat with this fixture's gated demand ZERO (P0.5-A's RED baseline — flips deliberately when beat laziness lands), beats/event measured; the GROWTH + honest-label law — the two-depth per-call ratios, `profiled_wall_seconds` never the battery's `cost.wall_seconds`, the artifact note); THE DATUM MEASURED (farstead seed 7, segmented, 10y+100y): the iter-327 in-session decomposition REPRODUCED as a committed record — occ_refold 27.3% + knowledge_rerank 10.8% of the 100y profiled wall (the two quadratic read-side members named), the growth ratios fold x9.67 / _novel_facts x9.54 / _ranked x10.4 (iter-327's x9.51/x9.17/x10.02, within noise), CANON-NEUTRALITY HELD at 100y (the profiled 7.7 MB byte-identical to the battery's), E03 2.0 parses/beat + E04 5.01 greedy calls/beat vs 0 gated entries (the Q7a waste quantified on the pack with no secrets/echo/traits — the folds early-return, the CALLS still fire every beat), beats/event 8.16 at 100y (the pack's stale "~50" replaced by the measured per-run number). Detail: the labrunner docstring law 8 + the iter-328 report + git.
- `rng-1` — DONE (iter-334, R3 core — the owner's «==> P0.5-C, rng-1 (эпоха), станционный килогод» call, the row's own opening; the counter-block epoch LANDED in `core/rng.py`: `U(stream,k) = word(k mod 4) of sha256(key:k div 4)` — O(1) access to the k-th draw (the end-state time-skip horizon H9 structurally unlocked), a checkpoint of COUNTERS ONLY (`core/cursor.py` refuses pre-epoch MT cursors loud), branch isolation STRUCTURAL (a draw's value fixed by (seed, stream, k) — a re-armed neighbor cannot move it even in principle); the block form: one sha256 per 4 draws (~0.42 µs/draw = MT randint's own CPython price — free on the real call mix), the wall price measured +3.7% (farstead 100y 10.0→10.37 s); **THE CORPUS PRICE PAID AND RECORDED**: 228 failures at the flip, all re-pinned with the laws' assertions intact (seed re-pins, beat-grid t-stamps, the document-check verdict flip on seed 125, the golden corpus regenerated ×7, 3 playscripts re-seeded, the CRN test's power doubled 8→16 pairs at the SAME thresholds — never weakened; one mechanical corruption caught and fixed: test_echo's `pack`→`PACK` from an earlier re-pin); P0.5-C closed as exhausted (the hoist rode P0.5-A, the LOD filter reclassified P1, the ~22% occ_refold residual measured near-linear); the owner's balance condition verified on the B6 oracle under the epoch's draws — 10 conversions = 10 bloom wears at 10y, every source at-or-below its cap, **NO pack-data fork needed**: the cycle balances on its own mechanics. NEXT: the station kiloyear with the armed world (the call's third item, now unblocked — the epoch boundary paid), H9 behind it. Detail: the iter-334 report + git.
- `kiloyear-1` — DONE (iter-335, R2 local-add — the owner's standing third call item «станционный килогод с вооружённым миром» (opened with rng-1, unblocked by the epoch) + the active «продолжай работы, открывай важнейшее» directive; the row the iter-334 NEXT named first): THE ARMED-WORLD KILOYEAR BATTERY UNDER THE EPOCH (farstead, seed 7, loc_square, directors off — sanity 2y paired + T1 HELD 183,697 bytes; control 100y paired — whole 8,557/56.2 s, segmented 14,210/10.32 s, THE CONTROL FAMILY talk 3,355 = 3,355 INVARIANT under the epoch (the MT absolute 3,209 — the epoch moves the number, never the invariance); MAIN segmented 1,000y — 130,327 events / **102.54 s** / life 74,322 in 1000/1001 spans 0.1% final, **T1 HELD at 76,951,399 bytes × 2 — the deepest determinism verification ever run** (the full kiloyear double-run)); **THE B6 ORACLE GREEN AT THE MILLENNIUM**: (a) the dead pile DIES — the workshop static at the SAME levels as 10y (ore 4 / wood 12 / tool 6; the unarmed MT left 4,016 DEAD at tool=0), (b) the linear piling BREAKS — every source ≤ its basin (58/60, 38/40, 38/40, 22/24; the total mass −30 vs seed, the unarmed +26,300), (c) the turnover BALANCED — **1,000 conversions = 1,000 bloom wears (exactly 1.00/year, delta 0)**, the tools alive — the material cycle holds equilibrium a millennium with ZERO pack-data forks (B6 closed at every scale 10y→100y→1000y); THE KILOYEAR LAWS under the epoch: verb linearity (sourced 3,996 = 4.00/year EXACT, converted 1.00/year), flat life (74.3/year, first500/last500 = 0.976), constant state (25 entities), the fatigue cycle alive (decay 50.0/year, meal_eased 2.46/year), replay-cost read-bound 0.604 s/MB (the station datum 0.648), fold near-free 0.089 s at 130k events; **THE WALL**: segmented LINEAR (10.32 s@100y → 102.54 s@1000y = 9.94× on 10×; 10.3× faster than the unarmed MT sandbox-equivalent ~1,061 s — the iter-333 "~4.5 min" prediction beaten at 1.7 min); **THE WHOLE ARM DECOMPOSED** (lab-5 on whole 50y/100y, canon-neutrality HELD): occ_refold 68.8%→81.7% of the profiled wall, per-call ×2.0, knowledge_rerank 0.0% (P1b holds on BOTH protocols) — THE MECHANISM NAMED IN CODE: the deferred-realize law holds completions to the horizon's end, so the whole protocol's OCC attribution window [seq, end) is horizon-long (the P1a snapshot removed only the PREFIX refold; on segmented the same window ≈ one year) — NOT a P1a regression (its "fold ZERO in-window" law was measured and holds on the segmented form); the whole-arm bound 400y > 595 s (α ≈ 1.72), the station prediction ~3,000–4,500 s; the fix (an index-based window attribution, B7's letter) a FUTURE gated row; the armed whole world at 100y: 4 conversions/century vs 100/year segmented (the drain cuts the conveyor), the store's deferred pile CAP-BOUNDED (40/24/40/64 — the unarmed whole's pile was unbounded); + the convert verb joins the labrunner's account_verbs full-read (the family's fifth verb, the B6 turnover counter — invisible to the top-12 cutoff on long horizons) + its law in test_lab; the station probe v3 (session artifact, Rule 9, self-checked green) delivered for the owner's cross-check (the whole kiloyear + the cross-hardware wall + the cross-hardware T1). NEXT: the station cross-check on the owner's hardware, H9 behind it. Detail: the iter-335 report + git.
- `stationcross-1` — DONE (iter-336, R0 datum-parse, zero code change — the owner's «Продолжай работу, я архив с результатами предоставил» call answering the standing proposal «запустите зонд v3 на станции… после его zip я разберу датум»; the STATUS Next item (1), the row the iter-335 NEXT named first): THE STATION CROSS-CHECK CLOSED on the owner's iron (probe v3.0, Win11 / **Python 3.14.3** / Coffee Lake / 30.9 GB, HEAD `ad79e1f` = the sandbox BASE_COMMIT; all six stages ok, the manifest md5s re-verified in-sandbox — all 8 copied files match): **THE WHOLE KILOYEAR MEASURED** — 3,818.15 s / 82,757 events / life 81,706 in 1/1001 spans 100% final (the deferred-realize law at the millennium), the whole-arm material universe REALIZED_DELTA-closed (the workshop starved ore=0/wood=6/tool=8, 4 conversions per millennium, consumed=30/settled=100 — the iter-335 §D item «REALIZED_DELTA килогода — со станционным прогоном»), **INSIDE the predicted 3,000–4,500 s window** (the A·t+B·t² model holds cross-iron; the station's own α(100→1000) = 1.91); **THE CROSS-IRON WALL**: segmented 104.36 s vs the sandbox's 102.54 s = **+1.8%** (nearly iron-neutral at kiloyear depth while the station reads 7% slower — 0.647 vs 0.604 s/MB, the iter-327 law 0.648 holding), the LINEAR law on both irons (the station 9.85× on 10×), the whole arm iron-sensitive the OTHER way (46.94 vs 57.14 s — the station 1.22× faster on the occ-refold's allocation churn); **THE CROSS-IRON T1 DECOMPOSED TO THE BYTE** — the file delta = (lines − 1) EXACTLY on every measurable pair (+230/+290/+8,557/+14,210 on 2y/100y × whole/segmented, +130,327 on the kiloyear by manifest arithmetic), the two named mechanical causes: the Windows CRLF newline translation (+1 byte × every line, od-dumped `}}\n` vs `}}\r\n`, zero lone CRs) + the header's python meta (−1 byte: "3.14.3" 6 chars vs "3.12.14" 7); **THE EVENT STREAM IS BYTE-IDENTICAL cross-iron** — after the \r strip ALL event lines identical on all four pairs, the event-stream md5 (header excluded) IDENTICAL (3e9505ab… / 45606949… / b13f22719868… / e94a0e259595…), `scripts/semantic_diff.py` exit 0 SEMANTICALLY EQUAL ×4 (the sanctioned comparator, D-229 — the only ignored difference the python meta, §1.4 by design) — **THE INTERPRETER CONTRIBUTES ZERO CONTENT BYTES** (3.12.14 ↔ 3.14.3, two minors apart: the byte-identity of T1 is a property of the CONTENT, not the environment; the env pin's excluded question answered by measurement), the derived prediction: the whole-kiloyear log would be 45,000,433 bytes on a LF platform (the CRLF law's arithmetic — the sandbox window keeps it unrun); **B6 GREEN on the independent iron** (1,000 conversions = 1,000 wears, every source ≤ its cap, the workshop static 4/12/6, the mass −30 — iter-335's numbers reproduced on foreign hardware+interpreter) + **the kiloyear talk invariant 32,404 = 32,404 both arms** + the 100y control family 3,355 = 3,355 (the triple check: station, iter-335, this session's reproduction) + the 100y event counts 8,557/14,210 identical. NEXT: H9 (the event-to-event waiting on the time-skip — structurally unblocked by the epoch), the whole-arm occ-window fix (B7's letter) behind it on the owner's call. Detail: the iter-336 report + git.
- `h9-1` — DONE (iter-337, R3 core — the STATUS Next item (1), the row iter-334/335/336's NEXT lines named first («H9 — event-to-event waiting на скипе времени», structurally unblocked by the epoch's O(1) counter jump; the owner's active «продолжай работы, открывай важнейшее на долгосрок» directive): **THE QUIET-BEAT SKIP LANDED IN THE CROSSING DISCIPLINE** — the loop jumps the clock, the bank counters (`RngBank.skip_draws`), and the director's beat counter across beats whose machinery would produce NOTHING, landing at the first producing beat or the stretch's bound (rotation/calendar/macro crossings all COMMIT — never skipped past). The landing computation, all reads against the frozen state: the decay formula twin (`next_decay_tick` — the interval-proportional first-draft tick, the pinned-axis law), the condensation emptiness twin (`condensation_pending` — zero draws, the drafts themselves burn name streams), and the family scans (`urgency_scan`/`faction_scan`: the shared `urgency_rolls`/`faction_rolls` predicates + one `first_failing` gate evaluation per stretch + `next_d100_hit` — the epoch's O(1) block walk over the rolling streams); **THE FALSIFIER IS THE A/B BYTE-IDENTITY LAW** (tests/test_h9.py law 1: the same (seed, step list) ON vs OFF — byte-identical, the ON arm's stats NON-VACUOUS): measured farstead 10y × 3 seeds × both protocols IDENTICAL, 100y segmented IDENTICAL (md5 `ee8459fa…` = the iter-335 canonical log), **the KILOYEAR IDENTICAL at md5 `a1d8f05b…` = the iter-335 canon, T1 HELD 76,951,399 B × 2**, whole 50y IDENTICAL; THE WALL: segmented kiloyear **102.54 → 46.44 s (2.21×)**, 100y 10.34 → 4.78 s (2.16×), 10y 1.03 → 0.48 s (2.15×); the skip ate 1,009,806 of 1,080,000 beats (93.5%) in 60,039 stretches with 59,091 landings; the whole arm 16.27 → 13.61 s at 50y (1.20× — the occ-refold residue is B7's row, not this one); **THE CAPABILITY FENCES** (checked once at init, a failing pack keeps the exact tick-by-tick path): the requested arm (`skip_quiet_beats`, the falsifier's off-switch), the DIRECTOR IS QUIET (disabled or no hooks — a hook-declaring enabled world keeps the old path: the pacing clock reads beat counts, the named residue), and THE FOLD DEMAND IS EMPTY (no gate reads the time-dependent folds — the per-tick fold verdicts are the second named residue, a future row); the live set is the Lab's own fixture family (farstead both director arms, pressure REFUSED — the echo-gated institutional verbs; tavern REFUSED — the fold gates); the committed corpus rides the ON arm by default and stays green byte-for-byte. +10 laws in tests/test_h9.py (the A/B pair, T1 under the skip, the counter identity, the fences ×2, the decay-formula property, the scan-vs-walk, the grid arithmetic, the labrunner arm, the CLI flag) + the labrunner's `--skip on|off` arm (the `_noskip` volume, the cost.skip block — the honest acceleration labels). NEXT: the standing owner calls (the whole-arm occ-window fix B7, the Lab battery rows E02/E31, M2, replay-UI, W8, the frontend P1/P2/P3). Detail: the iter-337 report + git.
- `occ-1` — DONE (iter-338, R3 core — the STATUS Next item (1), the row iter-335/336/337's NEXT lines named first (the whole-arm occ-window fix, B7's letter); the owner's active «продолжай работы, открывай важнейшее на долгосрок» directive): **THE INDEX-BASED WINDOW ATTRIBUTION** — the Simulator maintains the WRITE INDEX (`_occ_index`: (entity, prop) -> the ascending event indices of every committed write, the `_last_change` pattern's full-history form; `_commit` its only writer, the resume loop its only rebuilder) and `occ_breaking_cause(changes=…)` visits ONLY the window events that write a pair the intent's attributable tests can read — the read-set declared by the TWIN TABLE in core/intent.py (`OCC_READ_PAIRS` + `STATIC_TESTS` + `precondition_read_pairs`, next to the test family, never a second truth; the static family reads pack records never the projection; the windowed family absent by the attribution filter; COMPLETENESS IS LAW — every PRECONDITION_TESTS name is exactly one of table/static/windowed); the index law: a verdict is a function of its read pairs' values (pack/world/intent constant through one walk — both forms evaluate through the same live objects), so a non-writer can never flip one; the from_-check kept ON the read pairs (the index law's net — unfireable on a complete index); the one shortcut (verdict already failing at the start + the first window event not a writer -> events[seq].id) exact; the default (changes=None) keeps the exact full walk for every external caller. **THE FALSIFIER IS THE A/B ATTRIBUTION-EQUIVALENCE LAW** (tests/test_occidx.py: every index answer == the full walk's on the SAME call, both protocols, non-vacuous) + the byte-identity A/B + the twin-agreement property over all 6 committed packs x every action x seeded non-read mutations + the twin-completeness law + the resume rebuild law (index == the independent fold of the log's write history; armed == stripped through the split) + the unit grid (break / no-break / break-at-snapshot / repair-at-seq-then-rebreak / empty window / static conds) — +11 laws. **THE WALL**: whole 50y 13.66 -> 2.22 s (6.15x), whole 100y 51.64 -> 4.36 s (11.8x, the local exponent 1.89 -> 0.997 — the quadratic member DEAD), **THE WHOLE KILOYEAR 3,818 -> 43.5 s (87.7x — now CHEAPER than the segmented arm; T1 HELD md5 `7cbfb68a…` x 2 at 45,000,433 B — the iter-336 LF-platform byte prediction landed EXACTLY; events 82,757 = the station's number)**; the walk surface at whole 100y: window 18,341,200 -> inspected 82,174 (223x); the profiled wall: occ_refold 81.7% -> 7.3%, per-call x2.0 -> x1.02; the segmented kiloyear md5 `a1d8f05b…` = the iter-335 canon (46.15 s); the honest labels ride `Simulator.occ_stats` + the labrunner `cost.occ` block (calls/window/inspected/attributed). SIDE FINDING: KI#114 OPENED (the pre-existing resume-boundary drain divergence — a split AFTER a wait enters the next step +16 ticks late vs the uninterrupted feed; found by the law's first draft, reproduced with occ-1 fully stripped; the fix its own row, never silently). NEXT: the standing owner calls (E02/E31, M2, replay-UI, W8, the frontend P1/P2/P3) + the KI#114 fix row. Detail: the iter-338 report + git.
- `ki114dec-1` — DONE (iter-339, R0 doc-only — the owner's 2026-10-08 decision call «Принимаем B — закон композиции на чистой границе drain»; THE DECISION/EVIDENCE PACKET over KI#114, zero committed code change): (1) the decision recorded — the clean-drain-boundary admission as the canonical feed law (the next player intent only at queue-empty, the cascade fully complete), the composition law `run_steps([A,B]) == run_steps([A]); run_steps([B])` for EVERY partitioning, resume with NO separate timing semantics, candidate A (mid-drain resume) OUT OF CONTRACT (a separate R&D row at most, never a silent alternative); (2) THE STRENGTHENED FALSIFIER (the session artifact `scripts/ki114_law.py`, 143 checks): the full cut lattice of the step list x wait/move/zero-duration/follow-up-drain kinds x 5 packs (farstead armed, province, pressure, tavern, grim) x 2 seeds x both lab protocols x split AND checkpoint-resume-at-every-cut x double-run determinism — PROTOTYPE 0/143, BASE 44/143 (the falsifier's teeth: the old semantics CANNOT compose); the KI#114 repro closed (the farstead split byte-identical, the +16 gone); (3) THE 70-FAILURE CLASSIFICATION (the prototype suite 70 failed / 2557+1, BASE 2627+1 verified first, every assertion captured): 23 pure timing/value re-pins + 23 expected causal/state shifts + 24 golden byte compares (the census: province +10 events / road pure +3 timing / pressure +9) — **REAL SEMANTIC REGRESSIONS: 0**, every family mechanism-named (F1 the feed-point shift, F2 the deferred-realize phase shift, F3 the exposure-window closure — the pole carried off before the read enters, the night window over, the knock's echo residue decayed past the keeper's gate, F4 the span/boundary effects; the OCC census 1→76: ALL honest door breaks on `target.same_location` at 3 evaluation ticks — the deferred piles of the re-minted walks, zero player-step rejections, no wedge; determinism + INV-1..5 + the door/honesty laws held, the twin-run law green under the prototype); (4) THE CONSCIOUS REBASE LIST fixed (the decision's point 6): regenerate `province_smoke_seed42.jsonl` + `road_smoke_seed42.jsonl` + `pressure_smoke_seed39.jsonl` + the mediator narrator-beats expectations; grim + plumbing PROVEN byte-identical (the quiet-boundary law: an empty drain tail makes the two semantics coincide exactly); the station kiloyear canon rows stand as pre-KI#114 history; (5) the landing row `ki114-1-impl` OPENED behind the owner's confirmation of this packet. Detail: the iter-339 report + the session artifacts (`ki114-prototype-B.patch`, the law/census/probe scripts).
- `ki114-1-impl` — DONE (iter-340, R3 — the owner's «Пакет KI#114 принят» call, the iter-339 packet's landing): THE CLEAN-DRAIN-BOUNDARY COMPOSITION LAW LANDED in `core/loop.py` (run_steps feeds one intent, drains the FULL cascade, feeds the next at the drained clock; `_feed_next`/`_step_intent_id` deleted — the feed point a function of the drained state alone, never the call structure; resume carries no timing semantics of its own); THE PERMANENT FALSIFIER `tests/test_composition.py` (143 checks pinned by the battery-shape assert: the full cut lattice x wait/move/zero-duration/follow-up-drain kinds x 5 packs x 2 seeds x split + resume-at-every-cut + double-run + the Lab segmented 3y family — 0/143 under the law, BASE 45/143 the teeth; the historical farthest repro + the boundary-door laws); the partition-vs-wait-split distinction fixed in the record (the Lab's whole-vs-segmented contract untouched); THE CONSCIOUS REBASE (the census exactly the iter-339 table): the 3 smoke fixtures regenerated (province +10 / road pure +3 / pressure +9; grim + plumbing byte-identical — the quiet-boundary proof) + the mediator narrator-beats corpus (3 verdicts, the corpus protocol's 'regen') + 48 expectations re-pinned mechanism-named + the stepread night corpus re-crafted (the second day's window); KI#114 CLOSED; KI#115 opened (the grim two-same-account-flows latent pack bug, caught BY the _commit gate at the first year turn any grim run reached — pre-existing, the fix pack data, the owner's call); 2630+1 + ruff + docguard + topology clean. Detail: the iter-340 report + the report's §G PCC + git.
- `ki114-recraft` — DONE (iter-342, R0 test/doc only — the owner's 2026-10-08 «три строки ki114-recraft» call, the iter-339 packet §4's named residue; zero runtime code, zero pack data): **(A) THE POLESEED NIGHT CHAIN re-crafted** — the reader FOLLOWS the pole: the walk to the artery before the road-leg beat delivers Dellan and the pole there (t=2118, the beat's own move, cause urgency_0007), the read completing at t=2820 inside the SECOND day's night window [2520, 2880) — the partial-by-dark acquisition arm alive again (the flood story `saw`/`partial`, the cluster partial over Ketta; the beat's next leg honestly rejecting at `target.adjacent_to`); **(B) THE P1 INSTITUTIONAL CHECK re-crafted** — a second corpus (`tests/playscripts/province_institutional.json`, seed 2) whose re-timed wait (1100, completing t=2897) lands inside the sergeant's duty window at Malby (the rotation keep→malby at t=2520): the deferred check CO-LOCATES — the verdict honestly unsatisfactory (perception 60 vs social 57, margin −3), the waybill consuming the witnessed stack 55→80 (the arrest bar 75 crossed), the arrest attempt at the threshold, the resolution the world's own roll (the EVASION arm 61 vs 48 — the caught arm stays `tests/test_crime.py`'s witness; no seed in 2..53 aligns the three rolls on this chain); **(C) THE PRESSURE BENCH RATION re-crafted** — the registry-parked corpus (seed 7, the player a pure audience): the stokers' year-crossing stoke (t=520004, faction_0000 — no player lever anywhere), the knock (t=520604, the keeper's vague hearing through the shared walls), the in-window beat's mint (t=520920, the residue 11 of the vague 60-weight token's 1440-tick fade), the firing at the drain's own boundary (t=524327): FOUR COAL to the firehole (24→20 / 5→9), the bench convening one tick before, the warmth the reply — the antagonist pair's OTHER answer, the honest-refusal pin kept beside it. The honest-rejection pins (the loud detectors) untouched; the three corpora double-run byte-identical. Detail: the iter-342 report + git.
- `ki115-fix` — DONE (iter-341, R2 — the owner's 2026-10-08 «ki115-fix» call, the row opened at iter-340's landing): THE CROSSING'S PROGRESSIVE LAW — `flow_drafts` drafts flow N against the state as changed by flows 0..N-1 of the SAME crossing (`_commit`'s pending-dict law one level up), a copy-on-write OVERLAY inside the function (pure in its inputs; every signature + `core/loop.py` untouched); the capped source's occupancy read rides the same overlay (the fill + silence arms). THE FORK RESOLVED for the engine side: the lint declares co-due same-account flows LEGAL pack data (the crash was the engine's); the D-182 fold stays valid pack data with its own semantics; the till's +12/−4 REQUIRE the shared account. ZERO CORPUS PRICE PROVEN (grim the only co-due pack — the census; no committed corpus crosses the grim year; 2636 passed with every golden byte-compare green). The year-scale grim witness LANDED (the row's own ask): the progressive reckoning (30→42→38, chained to the turn, the shapes exact), the multi-year ladder (38→50→46→58→54, +8/year), T1 at the year scale, the composition law at the year boundary (continuous == split == resume byte-for-byte). Detail: the iter-341 report + git.
- `scale-1-impl` — DONE (iter-330 + iter-331, the byte-identical wall row COMPLETE; the owner's «можешь начинать (stageb-1 и scale-1)» call): **P0.5-A** the beat/macro derived folds on the pack's DECLARED gated-entry demand (`_fold_demand` at init + `_clock_fold_reads`, one shared computation per tick) + **P0.5-B** the specs parse-once memo (`urgency_specs`/`faction_specs` + `specs=`, every existing caller untouched) — the E03/E04 RED baselines flipped as iter-328 designed (2.0→0.0 parses/beat, 5.01→0.0 calls/beat vs 0 gated) + **P1a** the OCC attribution snapshot (the enqueue-time projection copy in a FIFO side-table — the ids repeat across beats, the queue's seq order restores the exact pairing — popped at the accept door, carried on the CompletionPayload, the walk pays the WINDOW never the prefix; the attributable-empty early return exact; the fold stays the resume/external fallback) + **P1b** the knowledge rank-bucket iteration (per knower per rank, tie-runs newest-first, arrival order within a run — EXACTLY the stable sort, zero comparisons, `at` monotone by the writer's tick-regression law) + the (teller,listener) novelty count (the O(1) saturated answer, born-correct for late knowers). **THE WALL FIXED, BYTE-IDENTICAL**: farstead 100y segmented 20–22 s → 10.0 s (2.1×); occ_refold 27.3%→3.1% + knowledge_rerank 10.8%→0.0% of the profiled wall; `fold` ZERO calls in-window at both depths; the per-call growth ratios ×9.5–10.4 → ×1.0–1.1 (the super-linearity dead at constant state); the local exponents the station ladder measured now flat. BYTE-IDENTITY: the cross-version md5 pair (farstead 2y/10y segmented seed 7 + province 2y whole seed 42 — zero-demand AND armed-demand sides) equal at EVERY stage (post-P0.5, post-P1, post-FIFO); the snapshot-vs-fold equivalence law (254+ real projection_moved walks byte-equal with start_state stripped); the golden T1 corpora + resume tests green. P0.5-C surfaced honestly (the candidates in the iter-330 report §E — the hoist rode P0.5-A; the owner's call on the rest). Detail: the iter-330 + iter-331 reports + git.
- `stageb-1-impl` — DONE (iter-332 + iter-333, the material cycle COMPLETE; CONTRACTS §12 B1..B8 the owner-accepted law): **iter-332 the ENGINE mechanics** (B2 the convert verb — ONE atomic recipe event, the settle aggregation; B3 the use-hook wear — a per-use consume at the successful completion, the instrument named, break-at-zero the last use; B4 the capacity cap — the min() mint, silence at full, the _commit cap floor loud; the lint arms; the renderer slots; the unarmed law held) + **iter-333 the FARSTEAD ARMING + THE B6 BATTERY**: the recipe forge_a_tool (the workshop's ore 2 + wood 2 → tool 1), the wear on the bloom bench (tool 1 per use, the lint-required gate), the caps on all four sources (the seeded basins: bank 40 / copse 40 / outcrop 24 / spring 60 — the first cut below the seeds was caught BY the cap floor itself, the pack bug refused loud, exactly the floor's law); **THE B6 REALIZED_DELTA ORACLE GREEN at 10y+100y**: (a) THE DEAD PILE DIES — the workshop's terminal ore+wood the recipe's WORKING stock (static: ore 4 = the seed, wood 12 the conveyor's buffer; the unarmed trajectory grew past 24 ore by 10y heading to 2,004 at the kiloyear); (b) THE LINEAR PILING BREAKS — every source at-or-below its basin (the spring ≤ 60 vs the unarmed 60+10/year → 10,060 at the kiloyear; the TOTAL account mass CONSTANT, the unarmed +26.3/year dead); (c) THE INSTRUMENT TURNOVER LIVE AND BALANCED — 100 conversions = 100 bloom wears over the century (1/year each way), the tool stock static at the seed 6, produced → worn → reproduced forever. The verb mix shifted measurably (account_converted 100/100y; the smith's settles became conversions — the loop-closes law extended to the verb family); **the B7 cost law held** (the armed wall 10.07 s vs 10.0 s unarmed — the cycle costs ~0.7%; occ_refold 3.1% + knowledge 0.0% unchanged; the growth ratios ×1.17–1.5, not steeper; canon-neutrality HELD); the conservation law extended per B2's own letter (initial + minted + transformed_in == final + consumed + transformed_out, per kind — the contract named the test as the extension point). +3 farstead laws (the arming's shape, the B6 oracle, the per-recipe conservation) + the loop-closes/cost re-pins. Detail: the iter-332 + iter-333 reports + git.
- `ssi-1` — DONE (iter-241, D-221 — the owner's 2026-09-26 SSIEC-v3
  control-plane call): Phase 0 the architecture freeze — the eight
  public-contract surfaces confirmed at their standing owners
  (INV-1..5 + EVENT_SCHEMA + PACK_SPEC + WORKBENCH_APP_LAW) and FROZEN
  for the initiative's duration; the strangler phases move INTERNAL
  ownership only. Detail: D-221 + the overlay.
- `ssi-2` — DONE (iter-242+243, D-222/D-223): Phase 1 the SSI
  foundation — `docs/ssi/` the read-only reference copy +
  SSI_OVERLAY.md (the A–L block matrix, the executable rule subset,
  the phase ladder) + the R0–R5 risk ladder as AGENTS §2.9 + the
  executable checks (test_architecture + docguard). Detail: D-222/
  D-223 + the overlay.
- `ssi-3` — DONE (iter-244, D-224; independently re-verified iter-245):
  Phase 2 CLOSED — the 82-module map at SSI_TOPOLOGY.md (drift-pinned
  by topology --check + test_topology) + the co-change/trajectory
  audit: loop↔pack HISTORICAL (dormant since iter-168, pack already
  decomposed via packlint), inference.py CONFIRMED the active hotspot
  — ssi-5's scope shrunk on the refuted coupling, ssi-4's target
  named. Detail: D-224 + the map.
- `ssi-4` — DONE (iter-247+248+249, D-225/D-226/D-227 the PCC
  records): Phase 3 CLOSED — workbench/application/inference.py 2511
  lines → the 10 owner modules + the 176-line pure re-export facade,
  split by the LAW's §2 semantic owners (never an external template);
  zero behavior change — the public surface/ops/claim packet
  byte-stable throughout. Detail: the D-rows + the map.
- `ssi-5` — the core strangler (Phase 4, owner-gated):
  loop/director/worldgen/intent internal-ownership moves ONLY — the
  public surface (director.next_beat(...) et al.) byte-frozen (the
  ssi-1 freeze); each step its own R2/R3 iteration with a PCC
  record.
- `ssi-6` — DONE (iter-250, D-228 (R3) — the owner's «продолжай
  работу» go-ahead): Phase 5 CLOSED — workbench/canonical_read.py the
  ONE workbench core-import module (the 10-name read surface); the
  three consumers (scene_build, observatory_read, scene_ir) migrated
  at zero behavior change; the law executable twice over (the
  import ban + the watchlist pin); ssi-5 explicitly NOT opened on the
  same call (the N018 gate unmet). Detail: D-228 + WORKBENCH_APP_LAW
  §24.
- `ssi-7` — DONE (iter-251, D-229 (R3); the owner's «ssi7 и/или ssi8
  ==> можешь начать» go-ahead): Phase 6 CLOSED —
  scripts/semantic_diff.py the semantic diff layer over T1 (pure
  stdlib, zero core imports) + the 22-test claim packet + TEST_PLAN
  §1.4 the law owner; the layer ADDS, never replaces T1. Detail:
  D-229 + §1.4.
- `ssi-8` — DONE (iter-252, D-230; the same go-ahead): Phase 7 CLOSED
  — the GC pass FIRED: the N020 sweep (every artifact class clean —
  the honest negative) + the three deletion cards (the .gitkeep
  family DELETED, sim/ RETAINED on authority — consumer absence
  alone is never deletion evidence, the KI#99 doubled tree the
  owner-side cleanup card). Detail: D-230 + the overlay.
- `log-1` — DONE (iter-256, KI#100 closed — intake-40's one code
  defect, D-233; the owner's 2026-09-26 verdict-agreement call): the
  reader's stale-header gate — read_log derives the expected
  `schema_version` from the passed schema's `$id` (the writer's own
  `_extract_schema_version` path, promoted module-level so both doors
  derive through ONE function) and refuses a mismatch loudly; the
  canonical read seam + the whole read surface inherit it for free;
  the writer's append check kept as defense-in-depth; the stale-header
  pin test + the test_render header sync ride it. Detail: the intake-40
  block + KI#100 + git.
- `temp-1` — DONE (iter-260, D-236; the owner's 2026-09-26 contract pick
  over the iter-257 fork card — **A2 + B2/B3; B1 deferred**): A2 the
  crossing-family slicing contract PINNED as `tests/test_temp1_contract.py`
  (the declared tavern scope count-invariant across the arms at all four
  seeds; the minimal pair projection + fingerprint invariance; the door
  families FREE with the known divergences — the seed-125 coerce flip,
  the seed-1001 cascade — PINNED so no future change can silently "fix"
  them); B3 the semantic-origin provenance LANDED through the existing
  primitive (`provenance.assignment_tick`, schema 0.2 → 0.3, the
  cause_hook precedent; B2's runtime UNTOUCHED — the clustering witness
  unchanged, both times now observable; B1 DEFERRED behind the card's
  evidence conditions; all five fixtures regenerated, canonical fields
  byte-identical to BASE). Detail: D-236 + phases.md §6 + git.
- `cov-1` — DONE (iter-258, D-234; the owner's «цензус cov-1» call):
  `scripts/mechanics.py census` — the action-to-consequence forward
  walk (action → parser verb → realized → canonical events →
  downstream consumers), a REGENERABLE derived report (never a second
  truth); the compact view = the coverage summary + the FLAGGED rows
  (UNREALIZED — the mutation-escape surface: tavern 6 / province 19 /
  pressure 2 at landing; CONSUMERLESS — the admission lint's own law
  re-derived); 7 tests pin the coverage, the forward block, the matrix
  agreement, the pack-scoped corpus, the regenerable law. Detail:
  D-234 + TEST_PLAN §9's census cell + git.
- `div-1` — DONE (iter-259, D-235 + KI#101 closed; the owner's «и
  прочими» call): `scripts/divergence_probe.py` — one same-seed
  BASE/PERTURBED pair over the existing balance-harness arms
  (`--directors-off` the T8 instance and the default; `--pacing-off` /
  `--systems-minus` the tavern family via balance_harness's own
  materializers, imported never duplicated), the semantic_diff
  oracle's §1.4 verdict + the bounded records it does not carry
  (first-divergence, causal-path ≤8 links, persistence + the family
  deltas + the projection delta); exit 0/1/2; 8 tests pin the T8
  instance, the null control, the arms, the loud errors, the oracle
  agreement, determinism. Detail: D-235 + TEST_PLAN §9's first-prism
  row + git.
- `pack-absorb-1` — DONE (iter-344, R1 doc-only — the owner's
  2026-10-08 pack-absorption call «проработай архив… впитал полезное…
  припарковал куда нужно законы и паттерны»; the unified pack v1.5
  read whole, 12/12 files): THE DURABLE LAWS PARKED at their
  repo consumers — (1) the scale-claim sufficiency law (the
  E/L/R/F/ρ/K/H/Q axes, the UNEXERCISED..TARGET-SCALE classes, the
  oracle tiers, the minimal scale-claim packet, the named workload
  profiles, the standing SEMANTIC-ONLY classification of the
  farstead kiloyear family) → TEST_PLAN §9.1; (2) the composite
  proof-test pattern map (14 patterns, live owners named where they
  exist — h9/composition/occidx/mutation-probe — vocabulary-only
  markers where they do not) → TEST_PLAN §9.2; (3) the 8-part
  runtime-promotion gate DEFINITION (referenced 10+ times, never
  defined repo-side before) → CONTRACTS.md's preamble. NOT parked
  (deliberately): CONS T1–T7 (already absorbed as CONTRACTS §6–11),
  CDMT v2 (the pack owns the method; the synthesis doctrine already
  AGENTS §2.7), TEXT2 disposition (the pack's own memory), the
  M-register wholesale (the pack owns the register; the landed facts
  live in git + the DONE rows). The queue rows opened:
  `density-1` + `lab-composite-1` (the E02/E31 re-derivation, see
  below). Detail: the iter-344 report (the freshness reconciliation
  table: the pack's snapshot iter-337 vs HEAD — B7/M-2/M-7/M-8 stale
  in the pack, all landed) + git.
- `density-1` — DONE (iter-345 the first half + iter-346 the second
  half, R2 local-add — the row iter-344 opened, the owner's standing
  «продолжай работу, открывай важнейшее» directive + the called
  order's head): **THE PROFILE→PACK MATERIALIZER**
  (`scripts/densitypack.py` — the SCALE_TESTING_LAW §15 boundary
  honored: the ONLY new mechanism; no second runner, no second
  schema — the packs consume `load_pack`/`Simulator`/`labrunner`
  as-is, disposable under gitignored `output/`): the settlement =
  the repeating unit, the committed Tier A fixture the template,
  every id namespaced `s<i>` with every cross-reference rewritten
  (the scaffold's law); the knobs = `--settlements` (E: 12·S adults
  + the player; L: 7·S; K=0 by construction — no inter-unit edges),
  `--talk-links` (R: the relation web's degree, the AP-11
  one-goal-per-NPC-per-verb ceiling enforced loud), `--prob-scale`
  (ρ: the SAMPLED family only — the p=100 crossings stay certain,
  B6's law); determinism pure (no RNG — same profile → identical
  bytes); PROFILE.md the transparent axes echo. +7 LAWS
  (`tests/test_densitypack.py`). **THE FIRST DATUM (iter-345, the
  locality-control ladder, seeds 7/42, 10y, both protocols, the
  square anchor)**: E 25→205, L 7→112, the living surface held at
  one unit — the event stream INVARIANT (segmented
  1195=1195=1195=1195; whole 899 = 899), **THE BYTE-LEVEL
  ISOLATION LAW: the S=1 vs S=16 whole logs differ in EXACTLY 10
  lines — the census digits, every other byte identical**; T1 HELD
  both ends; the wall 0.43→0.95 s (2.2× on 16× E); §9.1 class
  LOCAL-SCALE; H2 dead by construction under the LOD, H1
  1.4-1.5%. **THE SECOND DATUM (iter-346 — the `rest`-member
  split, the profile instrument's map extension)**: the
  projection-plane family landed in `_MEMBER_ENTRIES` —
  `director_global_passes` (entropy's per-beat whole-population
  pass), `projection_snapshot` (the O(E) state copy per autonomous
  enqueue), `skip_probes` (h9's population twins), `lod_zone_walk`
  (the zone computation over L), every entry's call subtree
  measured DISJOINT from the other entries' (caller attribution;
  `kind_of` deliberately NOT a member — its O(E) lookups ride
  occ_refold's/skip_probes' subtrees, the accounting law's
  boundary); +1 law (`tests/test_lab.py` — the grown-world law:
  the four members non-zero on a materialized S=4 pack, the
  partition holds, canon-neutral); the ladder re-measured with the
  decomposed wall: **director_global_passes 5.4%→31.2% (the
  E-dominant member — the story layer global by law, its E-price
  named)**, rest 37.7%→20.7%, per-call ×13.2 (_global_suspicion)
  / ×6.2 (snapshot) / ×3.7 (decay tick) / ×2.7 (lod) / ×1.01
  (next_d100_hit — the block walk E-flat as designed); the 100y
  ladder: the per-call growth ratios ALL ≈×1.0 (no depth-super-
  linear member), the stream invariant 10863 = 10863 at 100y; the
  wall S16/S1 = ×2.17 at 10y = ×2.16 at 100y (the E-exponent
  scale-stable across H). NEXT: `density-2` (the households knob —
  the warm-ring density, the DENSITY-SCALE arm).
- `density-2` — DONE (iter-347 `households`, the owner's standing
  «продолжай работы, открывай важнейшее, на долгосрок» directive;
  the environment permission for the station rows granted the same
  session): THE HOUSEHOLDS KNOB — `--households H` grows the ACTIVE
  unit's roster (H−3 extension households of four hearth-voice
  adults on loc_s0_square, the Ashen-mirror pair web, ONE talk
  post each on the extension's INTERNAL 2-step ring — bijective,
  no template adult targeted: the knobs orthogonal, every AP-11
  pair unique by construction; H=3 the density-1 form
  byte-for-byte) + 4 laws (identity/axes/ring+refusals/run-law:
  the material substream IDENTICAL, the census untouched, the
  extension talks PRESENT); THE THIRD DATUM — the DENSITY-SCALE
  ladder (warm 12→128 on H=3/6/12/24/32, S=4, cold 36 FIXED,
  segmented 10y, seeds 7/42): the wall ×114 QUADRATIC (exponent
  2.04 — vs the locality arm's ×2.17 on 16× cold E), **skip_probes
  35.9%→75.0% THE dominant member (×211 absolute — the quiet-skip
  economy INVERTS at density: the beats themselves grow ×10.4 with
  the population, each probe walks posts × projection; per-call
  costs linear: urgency_scan ×9.6, decay ×10.3)**, the rumor
  cascade the super-linear event amplifier (rumor_told 3→6097),
  the E-flat members flat (next_d100_hit ×1.08, occ_refold FLAT —
  the iter-338 index dividend holds at density), T1 + census +
  material-multiset + canon-neutrality ALL held (the segmented
  tick shift ±1-3 the honest beat-lattice coupling, declared; the
  WHOLE protocol's material substream byte-identical);
  **THE FIRST LOCAL-SCALE → DENSITY-SCALE PROMOTION** (TEST_PLAN
  §9.1's standing line synced); the named future row: the
  skip_probes optimization address (the spec filter + the O(E)
  kind_of walks riding it — admission the owner's call).
- `skipprobe-1` — DONE (iter-362, R3 core — the row iter-347 NAMED
  (the skip_probes address: the spec filter + the O(E) kind_of
  walks), opened on the owner's standing «продолжай работы, открывай
  то что сейчас важнее всего сделать, логичнее и качественнее на
  долгосрок. я разрешаю» directive — the admission the owner's call,
  called): **THE COLLECTIVE BEAT-OUTER WALK + THE O(1) id→kind
  INDEX** — `RngBank.first_d100_hit(rolls, limit)` (the per-stream
  `next_d100_hit` removed; the walk reads the same pure counter
  words beat-outer, stops at the FIRST beat any stream hits — the
  per-stream minimum by construction; duplicate entries fold to the
  max probability per stream name, the monotonicity law) + the
  `core/pack.py` `__post_init__` id→kind/id→record index (first-wins
  in category order, the old linear scan's exact semantics);
  **THE WALL: 61.87 → 18.34 s ×3.37 on the h32 density deep end**
  (skip_probes 74.9% → 33.2%, the walk member ×33), **ZERO canon
  bytes moved** (the h32 log md5 identical before/after, skip_stats
  + occ_stats identical verbatim; farthest envelope farstead 100y
  4.48 → 3.28 s, no regression); +5 laws (index-vs-linear over all
  six packs + first-wins duplicate; the collective-vs-per-stream
  reference oracle + the max-fold law + the p100 full-map law);
  the residual members named (rest/beat_rolls/decay_walk/
  director_global_passes — each its own future admission; THREE of
  the four now landed: the walk itself iter-362, the beat machinery
  iter-370, the director's senses iter-378 — decay_walk the last
  named row). Detail: the iter-362 report + git.
- `lab-composite-1` — OPEN (behind `density-1`, the same owner
  order; the old `E31` + «метаморфические семейства §26» labels'
  v1.5-successor form — ULT §17.4.1 + §17.5): **the composite/
  metamorphic battery** — the §9.2 pattern map's vocabulary-only
  rows made executable WHERE a consumer names itself (locality
  injection + boundary surgery first: the density envelope's own
  axes are their workload), each landing its live owner in §9.2's
  registry the same iteration; promotion ping-pong / adaptive
  sufficient state stay parked until the meso/world rows open their
  consumers. The E31 old definition died with the deleted pack — the
  owner re-scopes on their call if the old registry's E31 differs
  from the v1.5 re-derivation (the honest-unknown note, iter-344's
  report §D).
- `hygiene-1` — DONE iter-377 (the owner's «даю добро на hygiene-1»
  2026-10-12 call; R0): all three iter-376 findings fixed — (1) the
  four stale `inference.py` comment paths re-pointed to the package
  (`settings.py:30,121` + `test_inference.py:2` →
  `workbench/application/inference/`; `settings.py:98` →
  `inference/migration.py`, where `migrate_launch_semantics` lives);
  (2) TEST_PLAN §9.1's `docs/SCALE_TESTING_LAW.md` + ULT §3/§17.2
  marked «both paths inside that EXTERNAL pack, never this repo»;
  (3) MVP_SCOPE §9's verbatim `ev_0007` copy replaced by the
  EVENT_SCHEMA §10 pointer — the fork resolved to option B (D-024:
  a pinned copy is a second truth source kept alive by test
  machinery; the single owner is already test-pinned by T0/D-010;
  option A stays one iteration away if the owner wants the inline
  convenience back); zero behavior — text only; the report
  iter-377-hygiene1-report.md
### Iteration ledger (one line per iteration; the tail capped at 10 by the doc guard — older lines live in git; per-iteration detail: the D-rows + the owning docs + worklog + git, never restated here, the header's own law)
- iter-382 · 2026-10-13 · gatefold (R3 core, D-258 the PCC row — the owner's standing «продолжай работы… я разрешаю» directive, the standing order's SIXTH head: the scan key builds — iter-375's honest remainder; the iter-362/375 class): ФОЛД ГЕЙТОВ, НУЛЬ КАНОН-БАЙТ — ScanGateFold (core/intent.py, рядом с ScanGateMemo): сравнение ключа мемо ПЕРЕНЕСЕНО со стороны чтения на сторону записи — declared map (probe → пары, объединение обеих семейств; оконные/негейтованные не входят) + readers inversion; ЗАКОН POP (запись в объявленную пару выталкивает подтверждённых читателей — консервативно, вернувшееся значение ре-хитит ключ); ЗАКОН SERVE (фаст-путь подаёт РОВНО вердикт компара ключа: гейты идентичности/DECLARED/STAMP — объект записи мемо в штампе, заменённая запись никогда не подаётся устаревшей); ScanGateMemo.answer/entry_at — два аксессора (владелец вердикта — мемо, D-024); рождение БЕЗ чтения проекции (времена, не значения; мемо холодная); оба скана gate_fold=None дефолт; loop.py: рождение + re-birth + фолд в _commit + оба вызова; ИЗМЕРЕНО: pair_values 1.935 с / 939 351 → 0.000 с / 159 вызовов (честный остаток — сами ре-деривации, 144 стора идентичны), lookup 0.384/939K → 0.000/159; фаст-путь 1.04 проф. с / 939K подач; стена h32 10y 7.46/7.39→6.99/7.20 с (×1.07); профильная 18.76→17.31 с; +9 095 apply_change / +0.005 с; конверт h3 0.27 плоско / farstead 100y 2.58→2.52 с; НУЛЬ КАНОН-БАЙТ: h32 07e924cb… / h3 796afbe1… / farstead 4e4f4cf2… идентичны; +10 законов-оракулов (tests/test_gatefold.py: рождение+readers на 6 паках; закон serve на уровне функций с порядком dict'ов; батарея внутри/вне по СВЯЗАННОЙ проекции; фолд-двойник по всем классам краёв + отсутствие; штамп-гейт (замещённая запись) + флеш; идентичность + чистота (fresh parse подаётся); declared-гейт (крафт-коллизия); фракционный двойник; реальный лог провинции; резюм); 2663+27 (известный T1 набор, ИДЕНТИЧЕН базлайну ДО правок имя-в-имя, ноль новых — INV-3 поймал одно докстринг-слово до финальной батареи, исправлено на месте), ruff+docguard+topology+digest clean; D-258 на 35/35 — НА КАПЕ, следующая строка DECISIONS — коллапс владельца; the report iter-382-gatefold-report.md
- iter-381 · 2026-10-13 · rollidx (R3 core, D-257 the PCC row — the owner's standing «продолжай работы… я разрешаю» directive, the standing order's FIFTH head: the rolling-filter row; the iter-362 class): ИНДЕКС РОЛЛИНГ-МНОЖЕСТВА, НУЛЬ КАНОН-БАЙТ — RollIndex (core/urgencies.py): бакеты ПО ЛОКАЦИЯМ из пар (позиция спека, спек) над живыми не-пойманными NPC (рождение из initial-проекции — KI#16; фолд на пути коммита в _commit — закон ТОЧНОСТИ: перепроизводство членства из живого состояния, порядко-иммунно, remove мимо ГРОМКО; закон ПОРЯДКА ПАКА: insort по позиции спека — порядок dict'ов и дроу идентичны по построению); гейт идентичности serves (чужие держат предикат — семантический владелец; roll_index=None — дефолт-фильтр); loop.py: рождение + re-birth при resume + 3 места вызова; ИЗМЕРЕНО: стена h32 10y 8.05→7.35/7.48 с (×1.10), профильная 21.18→18.62 с; urgency_rolls 1.669 с / 2.63M вызовов → НОЛЬ в профиле; skip_probes 6.79→5.61 / beat_rolls 4.02→2.83 с; экспонента скана ×7.7→×4.50; НУЛЬ КАНОН-БАЙТ: h32 07e924cb… / h3 796afbe1… / farstead 4e4f4cf2… идентичны; +9 законов-оракулов (tests/test_rollidx.py: рождение 6 паков, фолд-двойник после 12 краёв, скан/обход-двойники + счётчики стримов, гейт, реальный лог провинции, резюм); 2653+27 (известный T1 набор, ноль новых; +9 зелёные), ruff+docguard+topology+digest clean; D-257 на 34/35 — ЗАКОННО; the report iter-381-rollidx-report.md
- iter-380 · 2026-10-13 · deccollapse2 (R0 riders — ПРЯМОЙ ВЫЗОВ ВЛАДЕЛЬЦА «можешь коллапс провести»; класс iter-310-deccollapse): КОЛЛАПС DECISIONS 36→33 — четыре строки iter-362-класса (D-253/D-254/D-255/D-256, iters 370/375/378/379 — одна семья: один класс, одна директива, последовательные головы) свёрнуты в ОДНУ компаунд-строку «D-253/D-254/D-255/D-256 | 2026-10-12..13» (субстанция по §6.1 сохранена: системы family_randint/ScanGateMemo/saturated/SensesIndex/DecayIndex, стены 18.58→8.08 с, md5, остаточный рейтинг; деталь — отчёты + git, D-024; семейный PCC цел); леджер шапки дополнен (36→33, вызов владельца); РАЗРЕШИМОСТЬ 256/256 D-ID (диапазоны развёрнуты), ноль повисших; 2644+27 (провалы ИДЕНТИЧНЫ базлайну, строка счёта гварда ушла в зелёный), ruff+docguard (33/35 ЧИСТ)+topology+digest clean; the report iter-380-deccollapse2-report.md
- iter-379 · 2026-10-13 · decayheap (R3 core, D-256 the PCC row — the owner's standing «продолжай работы… я разрешаю» directive, the standing order's FOURTH head — the STATUS Next row's own words: the decay landing index FIRST, the heap form; the iter-362 class): ИНДЕКС ПРИЗЕМЛЕНИЯ DECAY, НУЛЬ КАНОН-БАЙТ — DecayIndex (core/states.py): min-кучи ПО ЛОКАЦИЯМ из ячеек (next_fire, npc, prop) над ЖИВЫМИ парами (рождение из initial-проекции — KI#16, базы из last_change; фолд на пути коммита в _commit — двойник apply_event: ось перекладывает свою пару, position/crime_status — все пары сущности); ЗАКОНЫ УСТАРЕВАНИЯ/ВЕТО: INV-1 ЛИЦЕНЗИРУЕТ устаревание (вся причина ездит закоммиченным событием — отброшенная ячейка ВСЕГДА имеет свежего наследника или пара легитимно мертва); валидация НА ВИДУ (фильтры обхода против живого состояния — позиция == ключ кучи, свежесть next_fire); перечисление НЕ ПОТРЕБЛЯЕТ (re-push); гейт идентичности serves (чужие держат обходы — семантические владельцы; формула в _axis_change, обе ветки зовут её; clamp остаётся у next_decay_tick); loop.py: рождение + re-birth при resume; ИЗМЕРЕНО: стена h32 10y 9.59→8.08/7.99 с (×1.19), член decay_walk 3.31→0.26 проф. с (12.5%→1.2%, ×12.9; per-call 224.7→4.8 мкс), next_decay_tick 2.68→0.05 с (×50), ЭКСПОНЕНТА ПЛОТНОСТИ ×8.1→×1.85 (честное линейное ядро — число выстрелов растёт с популяцией) / ×1.11 (next_decay_tick — плоско), разреженный конверт без регрессии (farstead 100y 2.56 с); НУЛЬ КАНОН-БАЙТ: h32 07e924cb… / h3 796afbe1… / farstead 4e4f4cf2… идентичны, canon_check HELD; +8 законов-оракулов (tests/test_decayidx.py: рождение 6 паков + зубы посевов, двойник ПОСЛЕ КАЖДОГО из 17 краёв устаревания, caught-вето, перечисление-не-потребляет, гейт идентичности, реальный лог mid-run/конец + живой пул == свежему рождению, resume); 2643+28 (27 известный T1 набор, множество имён ИДЕНТИЧНО базлайну ДО правок, ноль новых + 1 строка guard-теста: D-256 36/35 — НАД КАПОЙ D-252, коллапс — вызов владельца, прецедент D-250; +8 зелёные), ruff+topology+digest clean; the report iter-379-decayheap-report.md
- iter-378 · 2026-10-13 · sensesidx (R3 core, D-255 the PCC row — the owner's standing «продолжай работы… я разрешаю» directive, the standing order's THIRD head: director_global_passes; the iter-362 class): ИНДЕКС ЧУВСТВ ДИРЕКТОРА, НУЛЬ КАНОН-БАЙТ — SensesIndex (core/director.py): сумма подозрения (оба дома, единый владелец формы _is_suspicion_home) + счёт видимых угроз как СКЛАДКА НА ПУТИ КОММИТА (рождение из initial-проекции — закон целой проекции KI#16 по построению; apply_change на КАЖДОМ событии в Director.seed — двойник apply_event, from_ есть валидированное до-значение); гейт идентичности (форма ScanGateMemo): bind пересканирует + штампует живой объект, releases читает индекс ТОЛЬКО для него, чужие проекции держат сканы (entropy/channel_entropies keyword-only senses=None — прежние вызывающие не тронуты); loop.py bind при construction + после resume; индекс НЕ в export_run_state (перестраиваем по логу); ИЗМЕРЕНО: стена h32 10y 11.37→9.57/9.49 с (×1.19), член 5.07→0.02 проф. с (16.1%→0.1%), entropy per-call cum 663→3.1 мкс — НЕЗАВИСИМ ОТ ПОПУЛЯЦИИ (datum ×2.50 списан), оба скана честный ноль в профиле; НУЛЬ КАНОН-БАЙТ: h32 07e924cb… / h3 796afbe1… / farstead 4e4f4cf2… идентичны; +7 законов-оракулов (tests/test_senses.py: рождение 6 паков + зубы сидов, двойник-согласие после каждого события по краевому сценарию, гейт идентичности, реальный лог mid-run/конец, resume); 2636+27 (известный T1 набор, ноль новых; +7 зелёные), ruff+docguard+topology+digest clean; DECISIONS 35/35 — НА КАПЕ D-252; the report iter-378-sensesidx-report.md
- iter-377 · 2026-10-12 · hygiene1 (R0 text — the owner's «даю добро на hygiene-1» call on iter-376's three findings; D-198: the session's explicit request IS the current task): ВСЕ ТРИ ФИКСА РЕВИЗИИ ПОСАЖЕНЫ — (1) 4 устаревших пути `workbench/application/inference.py` в комментариях/докстрингах перепинены на пакет (settings.py:30 → `inference/`, :98 → `inference/migration.py` — носитель `migrate_launch_semantics`, :121 → `inference/`, test_inference.py:2 → `inference/`) — сплит iter-247 теперь отражён во всех живых носителях; (2) TEST_PLAN §9.1: голый `docs/SCALE_TESTING_LAW.md` + ULT §3/§17.2 помечены «both paths inside that EXTERNAL pack, never this repo» (+1 строка); (3) MVP_SCOPE §9: дословная непиненая копия ev_0007 (18 строк) заменена указателем на EVENT_SCHEMA §10 — единственный владелец уже закреплён тестом (T0/D-010), вариант B развилки (D-024: пиненая копия = второй источник истины на тест-механизме; −13 строк, развилка записана в отчёте §B, вариант A остаётся одной итерацией по вызову); 2629+27 (известный T1-набор, множество ИДЕНТИЧНО базлайну iter-376 ДО правок)+1, ruff+docguard+topology+digest clean; the report iter-377-hygiene1-report.md
- iter-376 · 2026-10-12 · revision (R0 riders — вызов владельца 2026-10-12 «провести ревизию репозитория… мусор, дублирование, расхождения, мёртвые хвосты вроде redot… чисто исследовательская итерация»; D-198: явный запрос сессии = текущая задача): ПОЛНАЯ РЕВИЗИЯ РЕПО — ВЕРДИКТ: ЧИСТО. Заявления STATUS воспроизведены ТОЧНО на свежем клоне (pytest 2629+27+1 байт-в-байт, ruff/docguard/topology/digest чисто); REDOT — ноль артефактов, все 205 упоминаний в 40 файлах в санкционированных носителях (DECISIONS D-244/245, FAQ/NAV-роутинг, переразмещение iter-343, архив); мусор под git НОЛЬ (ни pycache/логов/ignore-пересечений, .git 11 МБ); 23/23 скрипта живы, 0 модулей без импортов, 0 осиротевших фикстур/frontend-файлов, 0 идентичных тел функций, 62/62 путей NAV живы, 6/6 паков потребляются, капы+allowlist чисты, ноль TODO-долга; ТРИ подлинные находки R0 → строка hygiene-1 (4 устаревших inference.py-пути в комментариях settings.py:30/98/121 + test_inference.py:2 — пакет с iter-247; голый внешний путь SCALE_TESTING_LAW в TEST_PLAN §9.1; непиненая дословная копия ev_0007 в MVP_SCOPE §9) + честный леджер ложных срабатываний (sim/ резерв, ssi v1/v2/v3 verbatim, зипы по D-242..248, README-сокращения, ref/-пути внешних репо); 2629+27 (известный T1-набор, перепроверен на нетронутом клоне до правок)+1, ruff+docguard+topology+digest clean; the report iter-376-revision-report.md
- iter-375 · 2026-10-12 · scangate (R3 core, D-254 the PCC row — the owner's standing «продолжай работы… я разрешаю» directive, the standing order's FIRST TWO heads: first_failing → commit_knowledge_fold; the iter-362/370 class): МЕМО ГЕЙТОВ СКАНА + ЛЕНИВАЯ НАСЫЩЕННОСТЬ, НУЛЬ КАНОН-БАЙТ — (1) ScanGateMemo (core/intent.py, рядом с precondition_read_pairs): ключ чтений ЕСТЬ инвалидация (закон occ-1; вердикт = функция pack/world/probe/requires + значения на объявленных парах; идентичность (pack, world) смывает при чужом объекте; оконное семейство НИКОГДА не мемоизируется — pairs=None, fence стал законом семейства); спеки несут parse-время pairs, оба скана принимают gate_memo=None (дефолт = свежая оценка), луп проводит один мемо через _skip_quiet_beats; (2) eager-счётчик новизны (teller, listener) УДАЛЁН (O(знающих) на запись, K×K dict; _rows_by_token/_token_holders удалены с ним) — zero-тест _novel_facts стал предикатом saturated (токены рассказчика ⊆ токены слушателя; P7-монотонность — точно, обслуживания ноль, _tokens O(1) на запись); ИЗМЕРЕНО: стена h32 10y 13.01→11.14/11.26 с (×1.16); first_failing в сканах 939K→41K вызовов (~3.5→0.33 с), hit rate 1.0 (4 447 240 консультаций / 508 ре-эвалов — зонд вне репо); commit_knowledge_fold 4.48→0.25 с (×17.7), per-call knowledge.add ПОПУЛЯЦИОННО-ПЛОСКИЙ 5.0→5.8 мкс (×6.74 datum СПИСАН); НУЛЬ КАНОН-БАЙТ: h32 07e924cb… / h3 796afbe1… / farstead-100y 4e4f4cf2… идентичны до/после; +3 закона-оракула (мемо-закон farstead/province: parse + twin-agreement + внутри/вне + идентичность; фракционный двойник; закон насыщенности с real-log оракулом farstead по ВСЕМ парам); 2629+27 (известный T1-набор, ИДЕНТИЧЕН чистому базлайну ДО правок)+1, ruff+docguard+topology+digest clean; честный остаток: сборка ключей 939K + urgency_rolls 1.70 с (роллинг-фильтр — locations-ключевой двойник, будущая строка) + first_d100_hit (уже оптимален); director_global_passes (5.06 с, третья голова) — следующая строка; the report iter-375-scangate-report.md
- iter-374 · 2026-10-12 · m6read (R0/R1 riders-only — вызов владельца «продолжай работы… я разрешаю»; m6_20261012_063055.zip + doctor.json в сессии): СТАНЦИОННЫЙ ПРОГОН M6 ПРОЧИТАН, промоушен-серия m4→m6 ЗАВЕРШЕНА — каждый номер m6_report переприведён из сырья (нуль расхождений, построчные цензы 1:1 на 54 строках, окна сверены: input med 1531 = R+RU); БЕНД ЗАКРЫТ маркерами -lv 4 в обоих логах (load_backend/device_info/ggml_cuda_init, FULL offload 33/33 + 43/43) + физикой (Gemma prefill med 4015/max 4445 tok/s, decode med 68; роутер ≥2800 tok/s внутри стены 0.546 с) — латентности m4/m5/m6 ВСЕГДА были CUDA-бендом, KI#119 перечитан, GPU-показания m4 восстановлены; R-ценза = m5 ТОЧНО (full 16/38.1%, kind+ 21/50.0%), det роутер 962b30a4… ШЕСТОЙ байт-идентичный, g c2e33bd9… второй; 0/42 изобретений (0/282 серия), [0]×42 токенов; drift нового смысла live: R CLEAN 23/42 (full 43.5%) против G CLEAN 13/42 (full 23.1%), R сходит реже 19/42 против 29/42; дозор: EN 15/10/17, RU 4/1/7 (ru_05 константа); narrate 20/20, r==gold проза 7/10 (s4 каскад идентичен); s4 = 15 событий живьём; INTERLUDE v6.2 (iter-372/373: KI#121 argparse %, KI#122 ложноотрицание бенд-грепа) записан в репо, оба фикса доказаны прогоном; строка m6-station закрыта, RUNTIME-promotion остаётся отдельным разрешением владельца (D-250) с полным базисом; 2626+27 (известный T1-набор, идентичен чистому базлайну ДО правок; ноль флейков test_lab)+1, ruff+docguard+topology+digest clean; the report iter-374-m6read-report.md
- iter-371 · 2026-10-12 · refemit (R0/R1 riders + R2 вне репо — вызов владельца «готовь прогон или ki закрывай» (2026-10-12), ОБЕ половины исполнены: KI#120 ЗАКРЫТ ФИКСОМ, станционный прогон подготовлен на v6.1): THE M6 STATION PACK v6.1 — РЕФЕРЕНС КОММИТИТ ЗОЛОТУЮ ТРАЕКТОРИЮ: emit_call в say-циклах run_reference (форма собственного теста парсера репо, test_parser.py; баг с рождения m3 — каждый закреплённый ответ умирал глотаемым ParseError'ом, референс-логи = setup + narrator-биты, золото никогда не выполнялось, drift мерил «от premise»); закон пропуска probe-циклов не тронут (руки и референс пропускают одни и те же циклы — apples-to-apples); DRIFT-КОЛОНКА — новый смысл «расхождение с золотой траекторией» (числа m4/m5 остаются в узком чтении, оба задокументированы в README/отчёте пака); ДОКАЗАНО ЖИВЬЁМ до/после: s4 = 6 событий без цепочки → 15 событий (take → move → drop_break → fire_started → fire_spread → smoke_rising → location_burned_out → flee → intent_rejected); ВАЛИДАЦИЯ полный корпус (b11541 ubuntu + Laya + Qwen3-0.6B, md5-pinned): юниты 13/13 (+1 новый: референс коммитит золото), смоук зелёный, полный корпус одним чанком — все стадии done, ПАРИТЕТ m4/m5/v6.0 ТОЧНЫЙ (R full=6/14.3%, G full=4/kind+=16/38.1%/refusals=11, RU-классы идентичны, output_tokens=[0]×42, inventions 0/42, вход med 841 — перепроверено из сырья); отпечатки референса растут (s4 6→7→8→13→14, s7 до 24), gold:s4 = 13 строк прозы с каскадом, drift нового смысла R 28/42 / G 29/42 (CLEAN 14/13), narrate 20/20, det identical, бенд CPU громко; v6.1-зип в docs/station/archive/ (паттерн m5/m6.0); 2626+27 (известный T1-набор, идентичен базе ДО правок; ноль флейков)+1, ruff+docguard+topology+digest clean; the report iter-371-refemit-report.md
