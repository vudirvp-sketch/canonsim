# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Trimmed to cap at iter-0v (KI#7); pre-trim history lives in git history.
> Entries re-trimmed to the line cap at iter-10a (KI#37; the drift ran
> iter-8b→10) — pre-trim detail lives in git history.
> Re-trimmed 39→10 at iter-48 (KI#68: the cap had drifted silently —
> the iter-43..47 "evicted per the cap" claims never executed; the
> eviction is now verified in the same edit, not claimed). Pre-trim
> history lives in git.
> Order: newest first (normalized at iter-8c — the order had drifted
> since iter-5).



---
iter-58 · 2026-09-05 · leg-3b — the tavern reflection set (arming
the v0.1 pack block; the owner's §2 design review first — endorsed)
- content/tavern_pack rules+templates: the live reflection block —
  `sneak_at_work_here`/`figure_reaching_for_purse` (the watcher) +
  `trouble_by_the_bar`/`noise_by_the_bar` (the room), threshold 2;
  `conclusion_drawn` story-critical, renders in the tale.
- Measured-first: the corpus price ZERO (narrator 105 + parse 10 +
  the T1 golden untouched; 8/10 day1 seeds byte-identical, exactly
  123/128 mint 4 events each); the told-conclusion law live (the
  briefing tells the insight, never-re-reflect blocks the re-derivation).
- tests/test_reflection.py: the dormancy test flipped to the armed
  law + 4 committed-pack pins. 1026→1030, ruff clean. LEGEND_SPEC §7
  + TASKS leg-3b done + D-087 into the phase family (cap 30 held).
  iter-48 evicted; 10 entries after.
---
iter-57 · 2026-09-05 · leg-3 — reflection & memory compaction (phase 4,
phases.md §4's memory paragraph; LEGEND_SPEC written just-in-time)
- core/reflection.py (NEW) + the _reflection lint + the loop._react
  wiring (after leverage): reflection-on-recurrence mints ONE event
  per (knower, insight) per run — outcome.provenance the
  list[event_id] handle, the never-re-reflect law, the stale fold,
  expand_reflection the demand side; no RNG, no hooks (L6).
- Measured-first: the recurrence EXISTS (day1_full seeds 123/128);
  the committed pack carries NO block — DORMANT (the arc-1
  precedent): the 10-seed A/B 10/10 byte-identical, zero corpus
  regen; +22 tests/test_reflection.py. 1004→1026, ruff clean.
- LEGEND_SPEC.md (193 lines) + SPECS_BACKLOG flip + TASKS leg-3
  done + the leg-3b arming row (the corpus price tagged) + D-086
  into the D-084/D-085/D-086 family (cap 30 held). iter-47 evicted;
  10 entries after.
---
iter-56 · 2026-09-05 · leg-2 — the brief's derived-trait read, leg-1's
first consumer (phase 4, BRIEF_SPEC's phase-4 clause)
- brief/assembler.py + core/traits.py (+14 tests: 10 brief, 4 traits):
  the PC's crystallized beliefs LEAD recalled_facts as belief lines
  `- belief <token> (t <cross>, sources: <ids>)`, the family records
  render nothing raw; expand_trait the demand side (the expansion
  law). BRIEF_SPEC §3.5 + §3 table + §9 split — same commit (§8).
- Measured-first: the PC holds no family token on ANY committed
  corpus — the 10-seed day1_full A/B (120..129) 10/10 byte-identical
  (brief + log), zero corpus regen; the golden no-belief pin.
- DECISIONS D-085 merged into the D-084/D-085 phase family (cap 30
  held); TASKS leg-2 done; KI#70 (the BRIEF_SPEC self-cap rot,
  389 > the declared 300 at HEAD — the header now reads AGENTS §6)
  opened+closed; KI#69 deleted per §5. 991→1004 tests, ruff clean.
  iter-46 evicted; 10 entries after.
---
iter-55 · 2026-09-05 · phase-4 open + leg-1 — trait crystallization
(P3f; the owner's "start phase 4" call, the iter-36 opener precedent)
- core/traits.py (NEW) + the _traits lint + rules.json::traits (the
  v0.1 belief set) + 18 tests: the belief-token fold — threshold
  DISTINCT family tokens crystallize a belief, source ids as
  provenance; read-model laws (no writes, no entropy — L6; no decay).
- Measured-first: day1_full seed 125 — the guard pair crystallizes
  paranoid_about_thieves (eyewitness 2 events / hearsay 1 event);
  10-seed A/B (120..129) 10/10 byte-identical, zero corpus regen —
  DORMANT (leg-2 owns the brief's derived-trait read).
- Phase 4 OPENED: ROADMAP §2 flipped, TASKS phase-4 backlog drafted
  from phases.md §4 (leg-1..4, retr-1, scene-1, blind-1); the
  phase-3 ledger condensed to a link row; DECISIONS D-084 + the
  gate-verdict family merge (cap 30 held). 973→991 tests, ruff
  clean. D-084 + STATUS. iter-45 evicted; 10 entries after.
---
iter-54 · 2026-09-05 · phase-3 gate — verdict PASS (the owner's "finish
at gate 3, then approach 4" call; docs-only, the iter-35 precedent)
- The §5 protocol green: seed-125 ON M1=0.509/M2=0.333, OFF T8 26
  chains, stretch max 1 (both arms + the quiet-walk stage), T7 a
  story, 973 tests + ruff clean; the exit criterion reads N=2.
- The doc debts paid: DECISIONS 48→30, FAQ 23→20, TASKS 854→510,
  DIRECTOR_SPEC 641→593; phases.md 644 kept over per §6.1 (the
  architecture substance — rationale here). ROADMAP §2 flipped;
  phase 4 UNLOCKED (opens on the owner's call). KI#69 (the worklog
  line-cap drift, the KI#68 family) opened+closed — trimmed in this
  edit. Detail: D-083 + STATUS. iter-44 evicted; 10 entries after.
---
iter-53 · 2026-09-05 · content-3 — the ambient driver, the murmur LIVE
(the phase-3 backlog's last content row)
- The 16th action `ramble` + the weight-0 ambient hook (the channel's
  own quiet gate, first_time_only), seeded on the wait action's hooks —
  the resolver-sparse minting gap closed (the KI#15 family,
  first-consumer law). core/resolvers.py + the pack trio.
- Measured: day1 10/10 birth-record-only (the all-PEAK law), the T1
  fixture regen (two fields), the corpus 105/105 + the quiet-beat
  case's deliberate pins, the nopacing arm re-pinned (D-065 again).
  +7 tests/test_ambient.py; 966→973, ruff clean. D-082 + TASKS +
  TEST_PLAN §6 carry the detail.
---
iter-52 · 2026-09-04 · content-6 — the arc driver, the aftermath chain
LIVE (the release-chain layer's first LIVE consumer)
- rules.json + actions.json: the `barkeep_wary_sweep` successor
  (trigger-less, climax-flagged, weight 0, first_time_only) + the
  aftermath arc gap 2; zero engine edits. The GAP law load-bearing
  (the unchained sweep would land before the check — a causality
  lie).
- day1 9/10 byte-identical + seed 125's one appended event; the
  corpus 105/105 pin-green, ZERO re-distill (the birth-record law).
  +6 tests/test_arc_driver.py; 960→966, ruff clean. D-081 + TASKS
  + TEST_PLAN §6.
---
iter-51 · 2026-09-04 · content-5 — the echo driver, the jittery-watcher
beat LIVE (social-2's live content set)
- rules.json: the guard's urgency entry (look_around, echo_at_least
  dread >= 15, p=100); the wariness arm measured FIRST and refused
  (34/105 cases + the never-fading rotation-renewed residue). Zero
  engine edits.
- The corpus: ZERO broken pins + the deliberate pins on the
  watch-change case; day1_full 10/10 byte-identical (the
  dread-silent law). tests/test_echo.py flipped to the committed
  pack; 959→960, ruff clean. D-080 + TASKS + TEST_PLAN §6.
---
iter-50 · 2026-09-03 · engine-2 — the urgency-roll stream split,
per-entry streams (the owner's "quality over speed" fork call)
- core/rng.py + urgencies.py + pack.py: per-entry streams
  `urgency:<npc>:<kind>` (lazily registered, pack-linted unique, the
  assure nesting law reworked); the single shared stream measured
  and refused (4/10 — the entries couple by draw position);
  add-safety 10/10.
- The one-time migration flip paid (0/10: 2 corpus cases + 1 parse
  pin + 2 seed re-probes) via the identity-proved fixed-point runner
  (the laws in the STATUS FAQ). +7 tests; 952→959, ruff clean.
  D-079 + TASKS + TEST_PLAN §6.
---
iter-49 · 2026-09-03 · content-4 — the coerce driver, the drunkard's
roll re-armed (social-1b's live content set)
- rules.json: the drunkard's urgency entry re-armed as the coerce
  carrier — the REPLACEMENT law (the slot and weight stay, the draw
  count holds, the corpus ladders hold); an ADDED entry was measured
  and refused (3 flipped ladders — engine-2 opened for it).
- The corpus re-distill through the identity-proved fixed-point
  runner (2 id re-pins + the silent_second tail, zero ladder flips);
  the live-fire tests moved onto the committed pack. 951→952, ruff
  clean. D-078 + TASKS + TEST_PLAN §6.
