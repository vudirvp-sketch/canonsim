# worklog — canonsim

> Cap: 10 entries, one in / one out. 3–5 lines per entry: what changed, why,
> files touched. No diffs, no command output, no reasoning traces. Long-term
> rationale belongs in `docs/DECISIONS.md`. Pre-trim history lives in git.

---
iter-176 · 2026-09-21 · doc3 — the owner-declared build: the state-layer reassembly
(FAQ one-liners, recipes → TECH_NOTES §14/§15, the three TASKS ledgers dead,
DECISIONS 31→30, README/worklog to their functions) + the cap guard + the digest
landings adaptation; 10 paths, doc + tooling; 1916+1 BEFORE at 2687465, 1926+1
after (+10 the guard's packet) + ruff clean; iter-166 evicted per the cap

---
iter-175 · 2026-09-21 · docrev1 — the owner-called state-layer audit: doc-3 OPENED
(the reassembly row + the cap guard, the recurrence fix); STATUS re-pinned (the
DONE-block protocol restored, seven stale blocks → git); verdict: the queue healthy,
the mass duplicated history; 3 paths, doc-only; 1916+1 green + ruff clean at efedd89;
iter-165 evicted per the cap

---
iter-174 · 2026-09-21 · engine-1 (move a, round 4 — CLOSED) — the v3 bundle triaged:
the full corpus landed at E4B/Q9B, the §4.3 arms measured (the seeded-local tier
holds, the GBNF penalty, mode-A's floor), the transcripts re-distilled (the deviation
corpus + 16 Layer-1 tests, zero replay divergence); 7 paths; 1916+1 green + ruff clean
at 1f4f20d; iter-164 evicted per the cap

---
iter-173 · 2026-09-21 · engine-1 (move a, round 3) — the v2 smoke bundle triaged (the
s6 crash runner-side, the double_apply_probe fixture kind, + two v2 defects: the
manifest's build half, the S7 -np 2 argv); the runner v3 delivered outside the repo,
sandbox-validated by the stub-client full-corpus walk; TECH_NOTES §13.1 the round-3
record; 4 paths, doc-only; 1900+1 green at 69db4f4; iter-163 evicted per the cap

---
iter-172 · 2026-09-21 · engine-1 (move a, round 2) — the `--arm all` crash triaged
(both defects runner-side: the v1 grammar's un-encoded shape laws + the battery's
ParseError-only catch; the census unwrap bug found in validation); the runner v2
delivered outside the repo, validated against the REAL doors (2109 docs pass the laws
+ the gate); 4 paths, doc-only; 1900+1 green at dcba648; iter-162 evicted per the cap

---
iter-171 · 2026-09-21 · engine-1 (move a, round 1) — the {3–8B, GBNF} experiment
convened (the owner's batched-test call): the Rule-9 runner delivered outside the repo
(the Vantiel-handoff pattern), sandbox-validated end-to-end at the owner's exact build
b11064 CPU; TECH_NOTES §13 gains the sandbox surface block; 4 paths, doc-only; 1900+1
green; iter-161 evicted per the cap

---
iter-170 · 2026-09-21 · engine-1 — the runtime inference engine DECIDED (the owner's
real-backend convening call): llama-server behind an explicit adapter + GBNF, the
file-contract frame the insertion point — D-192 the decision, CONTRACTS §4 the build
contract, TECH_NOTES §2/§13 the evidence (verified against the owner's raw logs); 6
paths, doc-only; 1900+1 green both ends at 7618714; iter-160 evicted per the cap

---
iter-169 · 2026-09-21 · qa2 — the KI#88/#89 lint-side closures: the shared
lint_direct_keys row wired into all four requires sites; the ACTOR_KEYS split + the
needs_target predicate extraction; tests/test_qa2.py +15; 12 paths (over the §2.3 soft
limit — the two-KI closure + its packet); 1900+1 green, mypy --strict core/ 0, goldens
byte-untouched at e15a091; iter-159 evicted per the cap

---
iter-168 · 2026-09-21 · qa1 — the owner-called type-discipline audit: mypy --strict on
`core/` 207 → 0 across 36 files at zero runtime change (the root-fix shape: _require,
the Literal funnels, the TypeGuards, the Mapping widening); two holes made loud (KI#88
+ KI#89); the tool stays optional (D-031); 29 core files, over the §2.3 soft limit;
1885+1 green, goldens byte-untouched at c82c7ca; iter-158 evicted per the cap

---
iter-167 · 2026-09-21 · stepread — the step bench's first embodiment: the read_stair
hinge + the the_step_law token landed in province_pack as pure pack data, zero core
change; tests/test_stepread.py +7; the water level's half + the remaining embodiment
options stay owner-routed; 9 paths; 1885+1 green at a317db3 (the +7 the claim packet);
iter-157 evicted per the cap
