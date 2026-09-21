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
iter-150, D-184; each build row's verification plan rides TEST_PLAN §9's
claim packet)

> The world-authoring track is NOT this queue: the setting's own plan
> (the anchor's A1/A2/A3 + the W-ladder) lives in
> `docs/worldbuild/WORLD_WORKPLAN.md` (D-186) — a separate track, never
> a second queue; a world-authoring need for engine capability lands
> HERE as a standing row on the owner's call.

- `engine-1` — the runtime inference engine, DECIDED (iter-170, D-192:
  llama-server behind an EXPLICIT ADAPTER + GBNF; the file-contract
  frame (D-055) the insertion point; CONTRACTS §4 the build boundary).
  Move (a), the {3–8B, GBNF} experiment: CLOSED iter-174, four
  owner-session rounds (iter-171..174; the full corpus landed at
  E4B/Q9B, the §4.3 arms measured, the transcripts re-distilled as
  the Layer-1 corpus + its 16 tests; the Rule-9 runners outside the
  repo, never committed). Remaining: (b) the build landing — the GBNF
  mapping repo-side + the door wiring + the failure→ladder mapping,
  INV-4 lifting there with the AGENTS §4/§8 edits riding it,
  owner-gated; presentation-1's write call rides the same evidence.
  Unlocked by the phase-1 gate; the dev-time external parser carried
  phase 2 to its gate PASS (iter-35) and carries mode C until the
  landing. Evidence: TECH_NOTES §13/§13.1, TEST_PLAN §8.5,
  `tests/fixtures/engine1_deviation_corpus.json`; detail: git.
- `presentation-1` — the LLM presentation contract, engine-1's
  decision-input child, never a sibling competitor (intake-12, D-148): the
  model-facing serializer spec over the STABLE brief IR (BRIEF_SPEC §7
  bytes + §7.1 protocol — the D-055 file-contract pattern's fourth
  instance), written FROM the {3–8B, GBNF} arm's results at the engine-1
  call (D-022 — a contract without a consumer has unknown requirements).
  Absorbs `st-4` at write time (the call budget + the transcript-tail
  contract + thinking-as-ephemeral-texture + the Script Tax clause — one
  owner, never two). The spec's shape when written: a thin mapping table
  over the existing 8 blocks + `narrator_protocol` — never a second
  re-labeling vocabulary (D-024). Exit criterion: the weak-arm run on owner
  hardware — MET (iter-174, engine-1 round 4: the mode-A bound measured —
  E4B parser-only at this call shape, Q9B narrates 6/8 per ladder, the
  narrator floor between 4B and 9B; the local transcripts' own call/reply
  documents are the spec's material). Evidence base: TECH_NOTES
  §10/§11/§13 (§13.1 the round-4 record — the mode-A arm, the script-tax
  twins, the regen ladder's measured behavior, the JSON-envelope failure
  mode at E4B); consult material at write
  time: the intake-30 visual-system card (phases.md §6 — the visual
  surface's parked residue: the development-order law, the fidelity
  target, the rejection table; D-187/D-174's surface ownership) + the
  intake-32 Vantiel card (`docs/ref/vantiel.md` — the model boundary's
  parked residue: the re-expansion law — a bounded context bundle keeps
  stable event/entity handles and re-expands deterministically from canon,
  never a second truth — + the staged-interpretation sketch input →
  interpretation → context → model proposal → validation → prose; D-190,
  the falsifier: the real consumer vs the current brief/retrieval stack on
  context cost, traceability, re-expansion correctness) + the intake-33
  outcome-perception card (`docs/ref/game_design_talks.md` §"What we
  take" — the layered legibility ladder: truth never bends / failure
  carries cause + avoidance path / odds as expectation bands, never naked
  percentages / transparency opt-in by flag, nothing dropped silently /
  outcomes legible through residue / stakes irreversible; D-191, the
  falsifier: at the write, each layer either changes the narrator
  document's shape or dissolves as already-satisfied).
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

### Iteration ledger (one line per iteration; the tail capped at 10 by the doc guard — older lines live in git; per-iteration detail: the D-rows + the owning docs + worklog + git, never restated here, the header's own law)

- iter-176 · 2026-09-21 · doc3 — the state-layer reassembly landed (doc-3 DONE) + the mechanical cap guard live
- iter-175 · 2026-09-21 · docrev1 — the state-layer audit routed, doc-3 OPENED (the owner's doc-revision call)
- iter-174 · 2026-09-21 · engine-1 round 4 — the full corpus landed at E4B/Q9B, move (a) CLOSED
- iter-173 · 2026-09-21 · engine-1 round 3 — the runner v3 delivered; the s6 crash triaged runner-side
- iter-172 · 2026-09-21 · engine-1 round 2 — the runner v2 delivered; the `--arm all` crash triaged runner-side
- iter-171 · 2026-09-21 · engine-1 round 1 — the {3–8B, GBNF} experiment convened; the Rule-9 runner delivered
- iter-170 · 2026-09-21 · engine-1 — the runtime inference engine DECIDED (D-192)
- iter-169 · 2026-09-21 · qa2 — the KI#88/#89 lint-side closures landed
- iter-168 · 2026-09-21 · qa1 — the type-discipline audit (mypy --strict core/ 207 → 0)
- iter-167 · 2026-09-21 · stepread — the step bench's first embodiment landed (pure pack data)

## Track B — background (evenings, foreign canon)

### bg-7 · engine + confabulation probe — done (2026-09-07)

- Done one-liner: all five probes' FIRST NUMBERS on the sandbox API engine (glm-4-plus) — TECH_NOTES §10; the {3–8B, GBNF} arm the gap row; runner + transcripts outside the repo (Rule 9).

### bg-8 · engine — the LLM-integration test runner — done (2026-09-09)

- Done one-liner: the testproto live half — the deviation corpus F1–F6 through the REAL mode-C door: the world-answer law's first live numbers (coverage 34/34 = 100%, honest 17/36) + the heartbeat's first run (84.4 → 93.3% after one re-ask). Transcripts re-distilled: tests/fixtures/deviation_corpus.json + tests/test_deviation.py + TECH_NOTES §11. Gap rows standing: the {3–8B, GBNF} arm, the bg-7 prose families, the per-family latency distribution. Detail: TEST_PLAN §8.2/§8.5, TECH_NOTES §11.

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
