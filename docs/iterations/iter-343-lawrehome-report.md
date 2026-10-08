# iter-343 — doc-4-lawrehome: THE LAW-BODY RE-HOMING LANDED

R1 (doc-only — zero runtime code, zero pack data, the suite
byte-untouched; the owner's 2026-10-08 repo-revision call:
«очистить от мусора документацию, в частности от старой информации
по redot и фронтенду той "обвязки", что уже неактуальна, чтобы ты не
путался в оной при работе дальнейшей» + «ревизию провести в общем
всех путей, данных и файлов внутри репо… расследовать упущения,
ошибки и противоречия»). This is FRONTEND_WEB_LAW §14's migration
**Phase 1 — re-home the laws (Redot → historical/reference-only)**:
the D-245 deletion (iter-290) removed the tree, the engine index and
the proof packets, and re-pointed the routing-minimal set; its own
closing note deferred the deep law-body re-homing («Глубокий re-homing
тел законов… остаётся»). That deferred work is this iteration — the
live law bodies no longer present the deleted engine as the runtime.

## A. The audit (the revision the owner called)

The full-repo revision ran before any edit — every live doc scanned
for dead path references (the audit script: path-like tokens in
backticks checked against the tree), every Redot mention classified
(historical record vs live routing), the stage maps and ladders
cross-checked against STATUS/TASKS. Findings:

1. **Dead live routing** — `docs/TASKS.md`'s standing instruction
   «Engine/API facts for any wb row: `docs/REDOT_ENGINE_INDEX.md`
   (read before the row starts)» pointed at a file deleted at
   iter-290/D-245. The same dead index was named by
   FRONTEND_UIUX_LAW §5's layering diagram and
   WORLD_PRESENTATION_LAW §14/§15.
2. **Stale law bodies** — five live laws still described the Redot
   frontend as the presentation runtime: FRONTEND_UIUX_LAW (the
   central invariant pipeline «→ Redot presentation», §19's gap
   «Redot does not consume it», §21's static/runtime split «needs
   Redot», §22.2's acceptance «Redot startup/packaging» + gate G1,
   §23's anti-pattern/decision questions, §24's P4 row, §25's Scene
   IR row); WORKBENCH_APP_LAW (§0's «Frontend companion =
   UX/UI/Redot/…», §3's tree carrying `presentation/redot/`, §33's
   REDOT box); WORLD_PRESENTATION_LAW (§0's «Redot consumption half
   NOT STARTED», §1's chain, §2's engine-type ban, §4's seam proof
   «in Redot», §12's benchmark «Redot UI + …», §13's untrusted-input
   wording, §14's runtime baseline «Redot 26.2 LTS», §15's
   screenshot workflow + the stale G7 marker «[LANDED —
   visual_proof]» over a deleted tool);
   LLAMA_CPP_INFERENCE_CONTROL_LAW (§0's «the Redot projection»,
   §5's REDOT adapter line, §19's landing notes naming the
   Redot-era surfaces without their current carriers);
   VISUAL_SYSTEM_UI (§8's VERIFICATION STATE naming the deleted
   REDOT_EXE packets).
3. **The TASKS sprawl** — the DONE rows wb-1..wb-12, ux-1, obs-1/2,
   inf-1/2 carried their full §8-style landing reports inline
   (TARGET PROBLEM / CURRENT PRIMITIVE / … / VERIFICATION STATE —
   the report format, restated in the queue): ~356 lines of
   restatement whose detail owners are git history + CONTRACTS §5 +
   the D-rows — the KI#7/iter-0v anti-pattern TASKS' own header
   forbids. These rows are also where 19 of TASKS' Redot mentions
   lived, including the deleted-era file lists (shell.gd,
   observatory.gd, REDOT_EXE packets).
4. **Stage contradictions** — `docs/frontendweb/README.md`'s
   «Current stage: S0 LANDED — awaiting the owner's green review»
   (S0 was accepted; seven Phase-3 rows, the streaming admission,
   the acceptance matrix and the CI rows all landed after);
   FRONTEND_WEB_LAW §14's migration ladder carried no status
   markers (Phase 1 unmarked-and-undone, Phases 2/3
   landed-unmarked).
5. **Verified non-issues (kept, never touched)** — STATUS' FAQ
   Redot-era entry (the correct principles form), README/
   AGENT_NAVIGATION/SSI_TOPOLOGY/CONTRACTS §5/DECISIONS D-244/D-245
   (the correct deleted-era record forms), the iteration reports
   and `docs/frontendweb/archive/` (point-in-time/verbatim records
   by law), the code docstrings naming Redot as provenance
   (workbench_launch.py, topology.py, the web client's carried
   principles comments), `workbench/runtime/inference.json` (a
   runtime path by design), STATUS' `workbench/workbench/runtime/`
   (the standing owner-side cleanup card), SSI_TOPOLOGY's
   `inference.py` rows (the pre-split audit records, the package
   form correctly current in NAV).

## B. The re-homing (what changed, file by file)

- **`docs/TASKS.md`** (616 → 346 lines) — the DONE rows collapsed
  to the landing-record form (the repo's own convention: iteration
  refs + the one-paragraph essence naming the SURVIVING modules +
  the Detail pointer; the §8-report restatements cut, verbatim in
  git + CONTRACTS §5). The dead engine-index instruction replaced
  by the D-245 routing: Redot/Godot engine questions route to the
  archived pack's reference docs (`docs/frontendweb/archive/` —
  never a repo file again). The exported-Windows-build row's
  product-form description updated (the Redot export form died with
  the tree; the product form re-scoped to the web client when the
  owner calls the row). The `doc-4` row + the iter-343 ledger entry
  added (iter-333's ledger line evicted — one in, one out).
- **`docs/FRONTEND_UIUX_LAW.md`** (14 → 2 Redot mentions, both
  historical) — the central invariant pipeline and the §5 layering
  diagram re-pointed (WEB IMPLEMENTATION ← FRONTEND_WEB_LAW.md);
  §19's gap + chain re-worded (no presentation consumer wired yet;
  the Redot consumer deleted at D-245; the P4 family owner-gated);
  §20's joint workload, §21's static/runtime split, §21.1's capture
  surface (the Playwright e2e), §22.2's acceptance + G1 (the web
  client build/serve), §23's anti-pattern (the engine resource/UID
  class, the deleted Redot's the named example), §23.3's question
  (12), the §23 corrected-conclusion (b) and §18's widget-per-file
  note (de-Godot-ified), §24's P4 row (the web scene renderer),
  §25's Scene IR row (the presentation client).
- **`docs/WORKBENCH_APP_LAW.md`** — §0's layering names the web
  client as the frontend companion (the Redot-era companion deleted
  at D-245); §3's package tree drops the dead `presentation/redot/`
  line (the companion lives outside at `frontend/`); §23 gains the
  LIVE seam note (the browser dials the loopback gateway —
  FRONTEND_WEB_LAW the implementation-law owner) above §23.1's
  correctly-DELETED historical record; §33's architecture diagram's
  REDOT box becomes the WEB CLIENT box.
- **`docs/WORLD_PRESENTATION_LAW.md`** (12 → 6, all deleted-noting)
  — §0's current state honest (no presentation consumer wired yet —
  the Redot consumer deleted at D-245; the P4 family owner-gated);
  §1's chain ends at the web client (DOM/CSS chrome +
  Canvas/WebGL scene-only); §2's engine-type ban generalized (the
  deleted Redot's Node/Texture2D the named historical example); §4,
  §12, §13 re-worded to the presentation client; **§14's fork gate
  re-based** — the presentation runtime baseline is now the web
  client (React + TS + Vite over the browser), the admission
  conditions unchanged, the dead index mirror replaced by the D-245
  archive routing; §15's G7 marker honest (the Redot-era LANDED via
  visual_proof — deleted D-245; the web-side capture rides the
  Playwright e2e + the P4 acceptance row) + the screenshot-driven
  workflow re-pointed.
- **`docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md`** — §0's UI
  REPRESENTATION layer and §5's adapter diagram name the web
  client; §19's landing notes name the current carrier (the web
  client's `frontend/src/features/inference/`) beside the
  Redot-era landing fact.
- **`docs/VISUAL_SYSTEM_UI.md`** — §8's VERIFICATION STATE
  vocabulary re-pointed (the browser-side capture evidence — the
  web e2e/Playwright surface; the Redot-era REDOT_EXE packets
  deleted at D-245).
- **`docs/FRONTEND_WEB_LAW.md`** — §2's S0 gate header carries its
  GREEN state (landed iter-289, accepted; the S0 laws remain
  binding); §14's migration ladder carries the phase markers
  (Phase 1 DONE — this iteration; Phases 2/3 LANDED with their
  iteration ranges; Phases 4..6 owner-gated).
- **`docs/frontendweb/README.md` + `FRONTEND_WEB_AGENT_CONTEXT.md`**
  — the Current stage line synced (beyond S0: the floors, Phase 3,
  the streaming admission, the acceptance matrix, the CI rows, the
  heartbeat ledger — the next rows the owner's call); the stage map
  gains the LAWS RE-HOMED stage line.
- **`scripts/docguard.py`** — the TASKS.md allowlist entry REMOVED
  (the guard's own designed exit: «A file leaves this table only by
  a real cruft pass that brings it under the cap»): TASKS.md at 346
  lines is under the cap, and the cap is now ENFORCED on it again
  (a regrowth past 600 goes red — better teeth than the exemption
  it replaces).
- **`STATUS.md` / `worklog.md`** — the riders (the header swap, the
  Next step, the worklog entry with iter-333 evicted).

## C. What was deliberately NOT done

- No history rewritten: the iteration reports, DECISIONS rows,
  the archive packs, and every `[DELETED …]`-marked historical
  block stand verbatim (AGENTS §11 — the historical record is a
  separate class from the live routing).
- No code, no pack data, no tests touched: the re-homing is the
  doc layer only; the web client's own principles-carrying
  docstrings (Chat.tsx's follow law, Inference.tsx's category
  list) keep their Redot-era provenance notes by design.
- The archive zips (`docs/frontendweb/archive/*.zip`,
  `docs/worldbuild/archive/*.zip`) retained — D-200/D-218/D-246's
  provenance law; their deletion would be an owner call (recorded
  here as the standing candidate, never executed unilaterally).
- `docs/AGENT_NAVIGATION.md` untouched — its Redot rows were
  already the correct deleted-era routing form (verified).

## D. Verification

- `PYTHONHASHSEED=0 python -m pytest -q` — **2632 passed + 1 skipped,
  zero failures, exit 0** — the collection and results IDENTICAL at
  BASE `a22fc61` and at this iteration's tree (the suite is
  byte-untouched; verified via the junit report at both ends). The
  prior session's claimed 2638+1 does not reproduce in THIS sandbox
  (a −6 environment delta — this environment's own measure is the
  honest number; the identical-collection BASE check is what makes
  the zero-test-change claim verifiable).
- `ruff check .` — clean.
- `python scripts/docguard.py` — clean (TASKS.md now under the cap
  WITH the entry removed; the ledger tail at 10; the worklog at 10
  entries; STATUS' shapes held; the digest parses the count line —
  `tests: 2632 passed + 1 skipped`).
- `python scripts/topology.py --check` — clean.
- The dead-path audit re-run: zero dead file/directory references
  in the live docs (the only remaining `redot` path tokens are the
  historical record forms — DECISIONS' D-245 rows, the §23.1
  historical block, the archive paths, which exist).

## E. Risks and next

- Risk surface: none runtime — INV-1..5 untouched, the LOG
  untouched, zero corpus price. The doc claims about the web client
  (Playwright e2e as the capture surface, the surfaces' paths)
  were verified against the tree before writing.
- The standing follow-ups ride STATUS' Next: the station canon
  re-measure, E02/E31, M2, the replay-UI row, W8, the frontend
  P1/P2/P3 continuations. The Phase 4..6 rows stay owner-gated.
- The one open candidate this audit surfaced for the owner: the
  archive zips' retention vs deletion (D-246's read-only-method
  document and the two pack zips) — kept by law this iteration.

## F. The owner-side git block

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add docs/TASKS.md docs/FRONTEND_UIUX_LAW.md docs/WORKBENCH_APP_LAW.md docs/WORLD_PRESENTATION_LAW.md docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md docs/VISUAL_SYSTEM_UI.md docs/FRONTEND_WEB_LAW.md docs/frontendweb/README.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md scripts/docguard.py STATUS.md worklog.md docs/iterations/iter-343-lawrehome-report.md
git status --short
git commit -m "iter-343-doc4-lawrehome: THE LAW-BODY RE-HOMING (Phase 1 of the web migration — the five live laws re-pointed to the web client, the dead engine-index routing replaced by the D-245 archive routing, the TASKS DONE rows collapsed 616->346, the docguard cap re-enforced on TASKS.md); 2638+1 + ruff + docguard + topology clean"
git push
```
