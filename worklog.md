# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`.
> Re-trimmed at iter-151 (the entries had drifted to ~40 lines each; the
> compaction entry carries the §6.1 over-cap rationale, as AGENTS §6
> demands); pre-trim history lives in git.
---
iter-152 · 2026-09-20 · docgc2 — the owner's doc-pass call: the CORE_DESIGN_RESEARCH
deletion (D-185's recorded next step; absorbed D-029/D-033) + the citation sweep
- docs (27 paths, over the soft limit per AGENTS §2.3 — the sweep IS the scope):
  the file DELETED; ref/ ×18 (9 template headers → the BLUEPRINT form, the
  iter-151 34-file precedent; the in-body citations → their live owners:
  D-019/D-020/D-005, phases.md §3/§5, BLUEPRINT §2 L9, core/echo.py, kenshi.md);
  phase0 ×2; REFERENCES_DEEP (ownership + §0 template + the iter-0h rationale);
  NAV §1 row; FAQ four→three; DIRECTOR_SPEC ≤300 → ≤600 (the BRIEF_SPEC
  precedent); TASKS' two v0.2 rows closed absorbed (no consumer: PACK_SPEC
  §8/§10 + the event-level story-critical law); D-185's execution note
- 1842+1 green + ruff clean both ends at BASE accfd72d (env pin 3.12.14; the first
  run's system-3.13.5 shebang trip = the TEST_PLAN §1.1 env-pin law, not a
  defect); worldbuild.zip stays deleted (the owner's call)

iter-151 · 2026-09-20 · docscomp1 — the owner's matrix session + the «вперед
приступай к работе» call: the semantic documentation compaction pass — the
iter-140-memgc GC restored and extended (D-185; the memgc had been clobbered
by iter-140-intake27's stale-base archive apply, found this session)
- DECISIONS 63→30 rows / 231→48KB (D-185 restored, the intake family absorbs
  D-173..D-175/D-184, the fixation families merged, the landings family
  D-176..D-182, the fat rows slimmed to decision + pointer); TASKS 2422→914
  (the phase-6-era ledger extended to iter-150, the 13 standing rows
  extracted to the live queue head); phases.md §6 restored compact + the
  intake-27/28/29 blocks (4305→2650); NAV 88→14KB; TEST_PLAN retitled the
  Verification Stack (837→588); REFERENCES_DEEP 63→31KB; SPECS_BACKLOG
  re-points restored; TAXONOMY/BLUEPRINT/PARSER/BRIEF re-points; ref/* (34
  files); DIRECTOR_SPEC header; AGENTS §6 one line; CORE_DESIGN_RESEARCH
  structural inbound → zero (deletion the owner's next call); STATUS re-pin
- verified BEFORE working at BASE_COMMIT 5d88bd0 (1842+1 green, ruff clean —
  the prior session's baseline re-confirmed) and re-verified after: 1842+1
  green, ruff clean; doc-only, zero code, zero corpus price; 16 paths (over
  the 3–5 soft limit, all mandated by the pass's own scope, per AGENTS §2.3)
- Caps after: DECISIONS 73 lines (30 rows, at cap) / TASKS 914 / NAV 140 /
  TEST_PLAN 588 / phases 2650 + DIRECTOR_SPEC 585 + BRIEF_SPEC 656 over the
  600/300 signals — substance (the intact cards/slices/audit/verdict + the
  runtime contracts), the §6.1 precedent, recorded here as the law demands

iter-150 · 2026-09-20 · revalid1 — the owner's two-part call: the AGPLv3
relicense (LICENSE + the README License section, D-183) + the 13-row
standing-backlog revalidation (D-184; 8 rows revised, no rows added/deleted)
- docs: TASKS (the iter-150 section + eight revalidated rows), DECISIONS
  D-183/D-184, STATUS re-pin + Next step, NAV §1 (the LICENSE row);
  doc-only, 1842+1 green both ends, iter-140 evicted per the cap

iter-149 · 2026-09-20 · pressure1 — pack-4 the pressure city (T1), the
owner's resumption call: the displacement law as pure pack data, ZERO CORE
CHANGE held exactly; res-1's second consumer arming; the first authored
non-scaffold pack; +16 pressure tests
- docs: TASKS (the section + the flip), DECISIONS D-182, STATUS re-pin, NAV
  §1 (the fifth pack); the engine findings (the group-stock lint gap, the
  co-due same-account limit) recorded in D-182, never patched in-core

iter-148 · 2026-09-19 · grim1 — pack-1 the grim tavern, the owner's
delegation call: the dark line as pure pack data (the axes, the
flirt→proposition ladder with the world's reply, the consent split + its
fact/belief lint `core/packlint/admission.py`, the pawn-ticket hinge);
res-1/since-1 first consumer armings; +14+1 tests
- docs: TASKS, DECISIONS D-181, PACK_SPEC §5 (the lint row), STATUS re-pin,
  NAV §1 (the fourth pack); the §9 claim packet CONFIRMED at the band

iter-147 · 2026-09-19 · since1 — since-1 the re-encounter delta: `brief/
since.py` (the per-entity encounter-epoch fold, read-side only, zero
streams), the cards' since-segments, the packlint readside lint; the
unarmed landing, +30 tests, the committed corpora byte-untouched
- docs: TASKS, DECISIONS D-180, CONTRACTS §3 collapsed, BRIEF_SPEC
  §3.4/§3.9/§6, STATUS re-pin, NAV §1

iter-146 · 2026-09-19 · res1 — res-1 the economy substrate: `core/economy.py`
(the account primitive, the three verbs through the canon door, the flow
drafts, `price_of`), the door/gate underflow floors, the discrete arm, the
packlint economy family; the unarmed landing, +18 tests
- docs: TASKS, DECISIONS D-179, CONTRACTS §2 collapsed, EVENT_SCHEMA §4,
  STATUS re-pin, NAV §1; the §9 claim packet CONFIRMED (F3/F4 + the oracle)

iter-145 · 2026-09-19 · roads1 — roads-1 the generated-exits pass: the MST
backbone + the mutual k-nearest overlay over the claimed locations
(`_pass_roads`), the ONE shared read `core/roads.py::exits` (authored wins),
the worldgen lint; the pack.py split rider (`core/packlint/`); armed k=0,
+9 tests
- docs: TASKS, DECISIONS D-178, CONTRACTS §1 collapsed, ROADMAP's row list,
  STATUS re-pin, NAV §1; the measured fork evidence in the iter-145 record

iter-144 · 2026-09-19 · contracts — `docs/CONTRACTS.md` (new): the three
pre-implementation contracts (roads-1/res-1/since-1 — pinned decisions,
invariant sets, §9 claim packets, minimal test sets); doc-only
- docs: TASKS (the section + the row pointers), DECISIONS D-177, STATUS
  re-pin + Next step, NAV §1 (the CONTRACTS row); the doc-loop alarm
  answered (the D-022 exception + the next step BUILD work)

iter-143 · 2026-09-19 · ci1 — ci-1 the GitHub Actions runner:
`.github/workflows/ci.yml` (pytest + ruff on push/PR to `main`,
PYTHONHASHSEED=0, Python 3.12.14 the env pin); the runner path simulated in
a clean venv (1754+1, ruff clean); branch protection the owner's settings
step (the recipe in the stop-point report)
- doc-only beyond the workflow file; the first LIVE run fires on the owner's
  push; 7 files (over the soft limit, all mandated — the doc quintet by
  AGENTS §6, the map row by NAV §3's short-map duty)
