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
---
iter-48 · 2026-09-03 · content-2 — the alarm panic echo, the
through-the-walls law LIVE (the last content row owing a corpus regen)
- rules.json + templates.json: the `alarm_raised` → `panic_ripple`
  on_action entry (witnesses +10 fear, the contagion quarter), the
  story-critical list, the chronicle line; zero engine edits.
- The 7-case corpus re-distill (the fixed-point runner); KI#68
  opened+closed (the worklog cap drift, trimmed to 10 in the same
  edit). +8 tests/test_panic.py; 943→951, ruff clean. D-077 + TASKS
  + TEST_PLAN §6.
---
iter-47 · 2026-09-03 · arc-1 — arcs & tension shaping, the
release-chain layer (the LAST engine row of the build column)
- core/director.py: `director.arcs` pack chains — the ORDER law +
  the GAP law + the entropy mirror + the per-run cursor; one-sided
  membership, the pack lint. DORMANT (content-6 owns the driver).
- The naive watcher-pair chaining probed and REFUSED live (the
  corpus-pinned relief held forever by a never-firing predecessor).
  +19 tests/test_director.py; 924→943, ruff clean. D-076 + TASKS +
  DIRECTOR_SPEC §3d.
---
iter-46 · 2026-09-03 · social-2 — the psychological echo, the residue
read model (the P2b consumer's engine half)
- core/echo.py (NEW): the pure read-side fold over the knowledge
  view (per-NPC valence, linear fade, fidelity-scaled, clamped);
  writes nothing, feeds no entropy (the L6 fence). The
  echo_at_least gate + the WINDOWED_TESTS generalization; rules.json
  the valence table, declared DORMANT (content-5 owns the driver).
- Measured: the crafted driver fires once then fades; the 10-seed
  A/B 10/10 byte-identical — zero corpus regen. +29
  tests/test_echo.py; 895→924, ruff clean. D-075 + TASKS.
---
iter-45 · 2026-09-03 · social-1b — the leverage use: the coerce door
(the fact cluster's first runtime consumer)
- The 15th action `coerce` over the NEW coerce resolver: the
  leverage_over fold-reading precondition, the unconditional
  tick-window OCC re-check, the loop-stamped spend event, the
  balance as pack data (the actions/rules/templates trio).
- DORMANT driver (content-4 owns the live call). +25
  tests/test_coerce.py; 870→895, ruff clean. D-074 + TASKS +
  INTENT_SCHEMA/MVP_SCOPE.
