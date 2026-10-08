# iter-340 — ki114-1-impl: THE COMPOSITION LAW LANDED

R3 (state/authority semantics — the feed law change; the PCC record at
§G). The owner's 2026-10-08 acceptance of the iter-339 packet («Пакет
KI#114 принят. Переходи к ki114-1-impl и садись на каноническое
направление B») — the landing the packet gated: the clean-drain-boundary
composition law is now the ENGINE's own contract, not a prototype.

## A. The law (one function's control flow)

`core/loop.py` `run_steps` restructured: an outer `while pending:` loop
feeds ONE intent, an inner `while len(self._queue):` drains the FULL
cascade it seeded (crossings, reactions, follow-ups, passes, beats),
then the next intent enters at `self._clock.tick` — the drained clock.
`_feed_next` DELETED (the mid-drain feed at the terminal event's own
tick, KI#114's root), `_step_intent_id` DELETED (the id-matching gate —
under the structural feed no id matching exists: only the queue's
emptiness speaks; KI#17 holds vacuously, the script advancing only at
drains). The crossing discipline, the H9 skip, the OCC index, the
commit door, the queue key, the log header: untouched.

The law, made permanent:

```text
run_steps([A,B]) == run_steps([A]); run_steps([B])   # every partitioning
continuous == split == checkpoint/resume             # byte-for-byte
```

The feed point is a function of the drained state alone — never of the
call structure around it. `resume` carries no timing semantics of its
own; the cursor (a drain-boundary artifact by its own law, D-139) and
the split land on the SAME boundary the batch now feeds on.

**The distinction the owner's point 9 fixes in the record:**
`partition([A,B,C]) => composition` is a law about ONE player-input
sequence composed at every cut. It does NOT assert
`run_steps([wait(2y)]) == run_steps([wait(1y), wait(1y)])` — those are
two DIFFERENT sequences, and their measured divergence (the
deferred-realize law) is the Lab's own instrument
(`scripts/labrunner.py`, whole vs segmented), never erased or
redefined by KI#114. The falsifier's Lab family holds the composition
WITHIN each protocol form; the whole-vs-segmented contract stands.

## B. The permanent falsifier — tests/test_composition.py

The iter-339 session artifact ported: **143 checks** (10 batteries x 2
seeds x (1 double-run + 3 splits + 3 resumes) + 3 Lab checks —
`_anchor_steps` segmented 3y, farstead + province, directors off),
with the count pinned BY THE LAW (a check added or lost fails the
battery-shape assert). Coverage axes per the packet's §2: the full cut
lattice, wait/move/zero-duration (`look_around`)/follow-up-drain
kinds, 5 packs (farstead armed, province, pressure, tavern, grim), the
resume protocol in test_resume's canonical shape (export flag ==
construction flag), the double-run determinism arm. Three laws: the
composition battery itself, the historical KI#114 repro (farstead seed
7, the 2-segment split, pinned forever), and the boundary-door witness
(every inter-step boundary of a batch admits `export_cursor` — the
cursor refuses mid-drain states, so the batch's own internal
boundaries are clean boundaries).

**Teeth, re-measured at landing:** the BASE arm (the law stashed)
fails 45/143 — the same families the iter-339 record measured at
44/143 (the session's battery shapes differ in the unrecoverable
details; the reconstruction is family-exact: farthest/province/
pressure/tavern splits and resumes + the Lab forms). Under the landed
law: **0/143**.

## C. The rebase (the owner's point 8 — targeted, conscious)

The census re-measured at landing, EXACTLY the iter-339 §3.3 table:
province 44→54 (+10), road 24→24 (pure +3 timing), pressure 29→38
(+9), grim + plumbing **byte-identical** (the quiet-boundary law —
committed proof, not assertion). Regenerated: the three smoke fixtures
+ the mediator `narrator_beats` corpus expectations (verdict level,
three cases 'accepted' → 'regen' with the contradiction notes pinned —
the corpus protocol's own designed answer, VALIDATION_SPEC).

Re-pinned: the 46 classified expectations (23 (a) timing/value + 23
(b) causal/state — every pin carries its mechanism note) + 2
pressure-fixture readers (the (b)-mechanism's per-fixture legs:
the stokers' autonomous stokes now realize at t=4332, the machine's
whole seam set spent) = **48 re-pins, every one mechanism-named**.
One (b) corpus re-crafted: stepread's night chain (wait 375 → 1107 —
the read lands at 2522, inside the SECOND day's night window; the
first window is owned by the road-leg beat's drain under the law —
the re-craft keeps the night-phase partial-fidelity witness alive).
Two re-pins are honest door facts where the packet's §4 named
re-craft questions (the poleseed night chain — the pole rides the
road-leg beat, every clean night boundary finds it gone, the
`target.same_location` rejection pinned as the world's answer; the
pressure bench — the convening sits 11,649 ticks past the knock, the
decayed echo honestly below the keeper's gate). The p1 institutional
check pins the packet's own OCC census as the law (76 autonomous
rejections, all `target.same_location`, three evaluation ticks
3797/5065/526229, zero player-step rejections, no wedge).

## D. The new finding — KI#115 (pre-existing, NOT the law's)

The battery's year-scale waits reached the grim pack's first year turn
for the first time in the repo's history and the run refused LOUD at
the `_commit` gate: the pack's economy declares two `every:1` flows on
one account (`till_settling` +12, `license_fee` −4, both on
`loc_tavern.account.coin`) and `flow_drafts` computes both drafts
against one projection snapshot — the second flow's `from` is stale
the moment the first commits. Reproduced with the composition law
stripped (BASE) — pre-existing, sleeping behind the corpus's day-scale
horizon (the pack's own notes admit the flows sit "beyond every
day-scale corpus script's horizon by construction"). Recorded as
KI#115; the falsifier's grim battery stays below the year horizon BY
DESIGN (it falsifies the composition law, not the pack's economy
graph). The fix — one account per flow, or per-flow projection
re-reads — is pack-data work, explicitly OUT of this row's scope; the
owner's call.

## E. The verification actually run

`PYTHONHASHSEED=0 python -m pytest -q`: **2630 passed + 1 skipped**
(~134 s; BASE was 2627+1 — the falsifier's 3 laws added, nothing
deleted or weakened). `ruff check .` clean. `docguard` clean.
`topology --check` clean. The 143-check battery green inside the
suite. The law verified on the LANDED `core/loop.py` (the working
tree == the committed tree; the sandbox commit precedes the delivery
archive, and the falsifier re-run green post-commit — the user's
point 6). INV-1..5 untouched: one function's control flow, the log
writer / queue key / header / schema untouched, the architecture +
stoplist tests green in the 2630.

## F. The honest residues (named, never silently dropped)

- The poleseed night chain and the p1 institutional-check arrest
  chain lost their witnesses to the F3/F2 window closures — re-craft
  rows on the owner's call (the packet's §4 named them; the honest
  door facts pinned meanwhile).
- The pressure bench's ration release (the echo-gated door's firing
  witness) — the same family, the same honest pin.
- The station kiloyear canon rows (iter-335/336 md5s) are records of
  the PRE-KI#114 semantics; a re-measured canon re-baselines them on
  the owner's call (no committed fixture depends on them).

## G. The PCC record (R3)

```text
[PCC: intent=make run_steps compose at every clean drain boundary
  (the owner's B-direction decision, iter-339's packet accepted);
 invariants=INV-1 (events only through the queue→_commit door),
  INV-2 (no draw-order change — the feed law moves no draws; the
  double-run arms green), INV-5 (committed logs never edited — the
  three fixtures REGENERATED per TEST_PLAN §3, the regen guards
  green), D-035 (the commit gate — it caught KI#115's stale from,
  the gate working);
 delta=core/loop.py run_steps restructured (feed-at-drain, the
  mid-drain _feed_next and the id-matching _step_intent_id deleted);
 verification=tests/test_composition.py (143 checks + the repro +
  the boundary law) + the full suite 2630+1 + ruff + docguard +
  topology --check;
 provenance=iter-339's decision packet (the owner's 2026-10-08
  acceptance) + the 70-failure classification (0 real regressions)
  + this report;
 runtime=sandbox Python 3.12.14, PYTHONHASHSEED=0, ~134 s suite]
```

## H. Done / Not done / Next

Done: the law landed; the falsifier permanent (143 checks); the three
fixtures + the mediator corpus rebaselined; the 48 expectations
re-pinned mechanism-named; one corpus re-crafted (stepread); the
riders (STATUS KI#114 CLOSED + KI#115 opened, TASKS, worklog,
TEST_PLAN §9's packet row).

Not done (the owner's call, per the packet's §4): the three re-craft
rows (poleseed night, p1 institutional, pressure bench ration); KI#115
(the grim economy graph — pack data); the station canon re-measure.

Next: the standing owner calls — KI#115's fix row, the re-craft rows,
then the standing queue (E02/E31, M2, the replay-UI row, W8, the
frontend P1/P2/P3 continuations). NOT started here (the owner's
explicit order): core-1, ssi-5, any other architectural extension.
