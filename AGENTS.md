# AGENTS.md — Operating Conventions for AI Agents

> Law for anyone (agent or human) making non-trivial changes in this repo.
> Trivial changes (typo, single value, doc fix) may proceed from `STATUS.md` alone.
> Repo language: English (docs, code, identifiers, commit messages). Chat with the
> owner: Russian.

## 1. What this repo is

`canonsim` — a deterministic canonical simulation core (Python, stdlib-first).
Phase 0 built **TavernSim v0**: one tavern scenario (theft, arson, rumors) that
runs and reads as a story **without any LLM** — closed iter-6; the roadmap's
phase ladder is COMPLETE — phases 0..6 all closed (ROADMAP §2 owns the state;
the standing work: the owner-gated backlog rows + the Soul-of-Waifu horizon).
North star: a simulation mode
inside Soul-of-Waifu (`docs/VISION.md` §10).

Two work tracks (`docs/ROADMAP.md` §1):

- **A (main):** the simulator — LLM-free at the core, the runtime engine
  wired as the doors' operator through the explicit adapter
  (`cli/engine.py`, engine-1/D-193; INV-4's form). Iterations `iter-N`.
- **B (background):** LLM-circuit spikes on foreign canon (Dwarf Fortress
  Legends XML). Tasks `bg-N`. Never blocks track A; can be dropped independently.

## 2. Iteration protocol

1. Plan first, then code. Better to underdeliver than to break things — the
   remainder goes into the next iteration.
2. Task ID: `iter-<N>-<short-desc>` or `bg-<N>-<short-desc>`. One iteration =
   one task ID from `docs/TASKS.md`.
3. Soft limit: 3–5 files per iteration. If objectively more are needed,
   continue, but note the scope in `worklog.md`.
4. Scope creep = stop. Anything not required by the current task ID goes into
   the `docs/TASKS.md` backlog, not into the diff.
5. **Anti-loop rules:**
   - The same failing fix attempted twice → record a KI in `STATUS.md`, stop,
     ask the owner. Never a third blind retry.
   - Patch files in place (targeted edit); never regenerate a whole file to fix
     a small bug.
   - Two consecutive iterations producing only doc edits with no functional
     progress → stop and ask the owner (documentation-loop alarm).
   - A task that cannot establish its owner → stop the semantic change; an
     unresolved authority contradiction → stop the affected implementation
     (§11) — never pick a side silently.
   - Research with no falsifiable decision path → park it (a
     `docs/TASKS.md` row), never drift into building.
   - Two consecutive iterations that do not reduce the declared gap → stop
     and re-scope with the owner.
6. Task intake (D-198): an explicit owner request in the active session IS
   the current task — it does not yield to `STATUS.md`'s `Next step`; with
   no explicit request, the `Next step` line is the working ORDER and
   `docs/TASKS.md` the backlog COMPOSITION — never the reverse.
7. At a genuine design fork (D-198): establish the underlying problem,
   compare the existing mechanism with the alternatives, prefer the
   higher-quality option that neutralizes material disadvantages over a
   minimal shift — and never generalize beyond the actual consumer and
   acceptance criteria.
8. New agent-facing tooling (scripts, CI, harnesses, doc machinery), D-198:
   existing mechanism → minimal extension → new mechanism, each step only
   on proof the previous one is insufficient. Admission requires a named
   consumer, a demonstrated problem/risk, an owner, a minimal
   intervention, a verification, and scope safety (no second source of
   truth). A cheap deterministic check protecting an established
   invariant is admissible without a recorded failure; heavy machinery
   without evidence is not. Standing refusals: no `agentcheck.py`, no
   `.agents/skills/`, no second project memory, no nested AGENTS files.
9. Risk ladder (ssi-2/D-222, the owner's 2026-09-26 SSIEC-v3 call —
   `docs/ssi/SSI_OVERLAY.md` the overlay owner): R0 text/style only; R1
   local pure refactor; R2 local behavior change; R3 cross-boundary or
   dependency change; R4 state/authority/schema/public-API change; R5
   security/distributed/irreversible/external-contract change. The
   ladder REFINES the §2.3 soft limit, never replaces it. R0–R2: this
   protocol as-is, zero added bureaucracy, no recorded class. R3+: the
   closing `docs/DECISIONS.md` row self-declares its class tag
   (`(R3)`/`(R4)`/`(R5)`) and carries the compact PCC record —
   `(R3) [PCC: intent=…; invariants=…; delta=…; verification=…;
   provenance=…; runtime=…]` (proof-carrying-change, SSI-N017, the
   overlay §4; docguard lints the shape, an R3+ row missing a field
   goes red). Escalation factors: blast radius, irreversibility,
   privilege, uncertainty, work amplification, external contract — any
   two present, consider one class up.

## 3. Reading gradient

Before working, follow the gradient in `docs/AGENT_NAVIGATION.md` §2.

Token hygiene: never read JSONL logs whole — use `tail`, `wc -l`, or a
`python -c` extraction one-liner. `docs/VISION.md` is the distilled source of
truth; the original concept documents live outside this repo — do not ask for
them.

## 4. Invariants (P0 — a violation is a bug of the highest severity)

| ID | Invariant | Enforced by |
|---|---|---|
| INV-1 | **Event sourcing.** No state change outside an event. State = fold(log). The raw JSONL log is the only truth; SQLite is a rebuildable index. The log writer (`core/log.py`) is the only canon-write path; every other module emits through the queue (privilege separation, D-031). | T2 replay test; review |
| INV-2 | **Determinism.** Single point of randomness control — one master seed; named streams deterministically derived from it via the `RngBank` authority (stable hash of `f"{seed}:{stream}"`); no wall-clock anywhere (including the log header); iteration only via `sorted()` or construction order; queue key `(tick, sub_order, actor_id)`; `PYTHONHASHSEED=0`. Cosmetic-stream draws can never desync canon replay. (D-028; supersedes the "one `random.Random(seed)` instance" wording — the donor sources themselves are multi-stream.) | T1 byte-identical test + RngBank fingerprint |
| INV-3 | **Content/code split.** Core code contains no domain words ("guard", "purse", "tavern"). All setting data lives in `content/tavern_pack/*.json`. | grep stoplist test (from iter-2) |
| INV-4 | **Network boundary — one module per direction-and-asset.** The network surface is EXACTLY THREE modules: the OUTBOUND engine adapter `cli/engine.py` (D-192/D-193, engine-1's landing — the owner's lift call), the INBOUND Workbench gateway binding `workbench/api/transport.py` (D-201, wb-4's owner-gated exception — loopback hosts only; non-loopback exposure refuses to start without auth, executable at construction), and the OUTBOUND model-assets fetch `workbench/platform/model_fetch.py` (D-208, wb-9's owner-gated exception over the «подтянуть модель откуда угодно» call — HTTP GET downloads of model files into the §16 MODELS_ASSETS root only). Everything else — `core/`, `sim/`, `render/`, `brief/`, `scripts/` — stays network-free and engine-agnostic; the gateway's semantic core (`workbench/api/gateway.py` + `contract.py`) is socket-free and never touches backend transport, persistence internals, or CanonSim internals (the app spec §4.1/§6.2 edges); no engine client ever enters `core/` (D-031/D-037). The doors' gates run on the reply document, engine-agnostic by construction (D-055's file contract — the runtime engine is "the operator"); inference sits outside the canonical determinism envelope (TEST_PLAN §8.4). | review; the narrowed import check (test_architecture — the ban outside the three sanctioned modules) |
| INV-5 | **Log immutability.** Committed logs are never edited; corrections are new events. Runtime logs are never committed. | review; `.gitignore` |

## 5. Bug → doc → fix (KI lifecycle)

Found a bug → first record it in `STATUS.md` as `KI#<N>`, then fix it.

- On open: one line — `KI#<N> · short description · date opened`.
- On close: mark `CLOSED iter-<N>`; do not delete immediately.
- Any KI closed for more than 2 iterations MUST be deleted at the start of the
  next iteration that touches `STATUS.md`. This is mandatory cleanup, same
  priority as writing new entries — not "later housekeeping".

## 6. Output caps (substance over line count — enforced every iteration)

| File | Cap |
|---|---|
| `STATUS.md` | ≤15 active KIs, ≤2 lines each; FAQ ≤20 entries; no stack traces or snippets — link the worklog entry |
| `worklog.md` | ≤10 entries, 3–5 lines each; adding #11 requires deleting the oldest in the same edit (one in, one out) |
| `docs/*.md` | ≤600 lines each. The cap is **substance-filtered**, not a hard wall — see §6.1. Over cap after a real cruft pass: keep, document the rationale in `worklog.md` |
| `docs/AGENT_NAVIGATION.md` | structure changes only; never history or narrative |
| `docs/DECISIONS.md` | append-only within a phase; ≤30 entries enforced by collapsing at phase gates, post-ladder on the owner's explicit call (D-034/D-185); supersede, don't delete |
| `docs/TASKS.md` | done tasks collapse to one line at the end of each iteration |

General rule: check the current size before writing to any of these. The trim
is part of the task, not future work. Long-term design rationale goes to
`docs/DECISIONS.md`, never to the worklog.

### 6.1 Substance vs cruft (the cap is a signal, not a wall)

A cap breach triggers a **cruft pass first**, never a substance cut. The
owner's directive (iter-0j): "quality > crutches; determine what is garbage
and what carries semantic/functional load." Cutting real depth to fit a line
count is a crutch — forbidden. The hard cap is a generous ceiling (600) for
scale; the substance-vs-cruft filter is the real anti-bloat law.

**Cruft (cut always, before any substance):**

- Filler words: "really", "actually", "essentially", "in fact", "indeed",
  "as such", "basically". Tighter prose is more readable.
- Restatements: if a clause already says X, the second "in other words, X"
  paragraph is cruft — link the single owner of X instead (D-024).
- Linker chains: "and so therefore we can see that, as a result, …" —
  collapse to one connective or none.
- Multi-clause run-ons that should be split: a sentence with three
  semicolons is two sentences plus a list.
- "As mentioned above" / "as noted earlier" without adding new value.
- Decorative prose that does not carry a fact, a name, or a decision.

**Substance (never cut to fit the cap):**

- Named systems, classes, functions, files.
- Concrete data structures with real field names.
- Type enumerations and enum value lists (e.g. every event type with its
  real fields — the iter-0i trim of the DF Legends XML event-type list
  was a substance cut; this entry exists so it does not happen again).
- Pseudo-code where it earns its keep (tick loops, queue keys, fold
  examples).
- Real numerical values, durations, thresholds, enum string values.
- Per-source verdicts: "what we take / adapt / inspire / strengths /
  weaknesses" — the entire point of a deep dive.
- Cross-references and links to the single owner of a fact.

**Test**: would removing this sentence or list cost the reader a concrete
fact, a named reference, or a real data structure? If yes — substance, do
not cut. If no — cruft, cut. The cap is reached only after the cruft is
gone; if substance remains and the cap is exceeded, the file stays over and
the worklog records why.

## 7. Git safety

- NEVER `git add -A` / `git add .` / `git add -u`. Only `git add <specific paths>`.
- Runtime artifacts are gitignored and must never be staged: `logs/`, `output/`,
  any `*.jsonl` outside `tests/fixtures/`.
- Live session runners (sandbox drivers, corpus-price probes, LLM-circuit
  test runners) live OUTSIDE the repo — the operator's **Rule 9**; `scripts/`
  holds only git-committed repo tooling (D-046). Never stage, commit, or
  archive an ephemeral runner into the repo.
- Committed by design: `docs/`, `schemas/`, `content/`, `tests/` (including
  `tests/playscripts/*.json` fixtures).
- Commit messages: `iter-N-desc: what changed`. No secrets, no `.env`.
- Before every commit, verify with `git status --short` that nothing forbidden
  is staged.

## 8. Stop & confirm (owner approval required before proceeding)

- A **breaking** change to `schemas/event.schema.json` or
  `docs/EVENT_SCHEMA.md` (rename/remove a field, remove an enum value) —
  requires a `schema_version` bump + migration note.
- Changing the queue key, tick semantics, or log header fields.
- Adding any runtime dependency (core is stdlib-only) or bumping
  `requires-python`.
- Touching CI workflow files.
- Introducing a new LLM/network call site ANYWHERE outside the engine
  adapter `cli/engine.py`, the inbound gateway binding
  `workbench/api/transport.py`, and the model-assets fetch
  `workbench/platform/model_fetch.py` (a second engine module, a network
  import in `core/`/`brief/`/`scripts/`, an engine client in the
  kernel — INV-4's standing form, D-192/D-193/D-201/D-208).
- Moving or renaming top-level directories.
- Deleting or rewriting committed log or fixture files.

## 9. Definition of Done + stop-point report

An iteration is done when:

- `pytest -q` is green and `ruff check .` is clean;
- the verification claim rides `docs/TEST_PLAN.md` §9's claim packet — the
  claimed EFFECT is checked, not merely that tests happened to pass;
- the code-quality bar holds: conventions per `docs/MVP_SCOPE.md` §18 (type
  hints on public functions; no `print()` outside `cli/`) and the elegance
  laws L13/L14 (`docs/BLUEPRINT.md` §2 — the abstraction cost gate and the
  elegance checklist);
- docs affected by the change are synced (`docs/AGENT_NAVIGATION.md` §1 if
  structure changed; `docs/TASKS.md` statuses updated);
- caps (§6) are respected;
- the stop-point report is posted:

```
Done: ...
Not done: ... (reason)
Next: ...
Active KIs: ...
```

- If files changed, end the report with the owner-side Git Bash block (§12.3),
  listing each changed file explicitly (never `.` / `-A` / wildcards).

## 10. Environment (determinism)

```
PYTHONHASHSEED=0
Python >= 3.11
dev deps: pytest, ruff — nothing else
```

Required checks, in order (a doc-touching iteration adds the doc guard as
the fourth):

```
python -m pip install -e ".[dev]"    # --break-system-packages on a system Python
PYTHONHASHSEED=0 python -m pytest -q
ruff check .
python scripts/docguard.py            # any docs/ or state-doc touch
```

The byte-identical replay guarantee holds for the same environment only; the
log header records the Python version (see `docs/TECH_NOTES.md` §4).

## 11. Authority & conflict resolution

Authority resolves by question class — `docs/AGENT_NAVIGATION.md` §3 owns
the map — never by file hierarchy, recency, length, or convenience. When
two sources disagree (D-198):

1. Define the exact question.
2. Identify the semantic owner for it (`docs/AGENT_NAVIGATION.md` §3).
3. Separate intended contract / observed behavior / verification
   evidence / historical record.
4. Inspect the owner; implementation and tests only as needed.
5. Classify the discrepancy: intentional divergence, stale declaration,
   implementation bug, test bug, or unresolved contradiction.
6. Never silently reconcile: no merging two contradicting documents, no
   rewriting an owner "to match the code", no treating the newer or
   longer text as automatically right.
7. Preserve unresolved contradictions through the KI (`STATUS.md`) /
   research / owner route — and stop the affected implementation until
   resolved.

## 12. Handoff & reproducibility (sandbox → owner)

The sandbox clone is disposable; the owner's local repository is the real
one. **The agent has NO push access to the owner's repository and NEVER
runs `git commit` / `git push` against it — not at the end, not "just to
verify", not ever (D-206, the owner's 2026-09-25 directive). All
owner-side git is the owner's own hands, driven by the §12.3 block.** The
sandbox's own git is bookkeeping only — BASE_COMMIT and the changed-path
enumeration; a sandbox commit is internal verification, never the
deliverable, never something the owner pulls from (D-198, superseding
D-113's chat-side placement).

### 12.1 The delta archive

- `BASE_COMMIT` = the exact HEAD of the actual checkout, recorded via
  `git rev-parse HEAD` before any modification — never copied from a stale
  `BASE_COMMIT.txt` or a previous session's text (D-185's stale-archive
  lesson: a delta built against a stale base silently erases landed work).
- The deliverable is a delta archive against BASE_COMMIT: exactly the
  changed/created files, repo structure preserved, plus `BASE_COMMIT.txt`
  (the hash) and `DELETED_PATHS.txt` (or `None`); never `.git/`, caches,
  logs, outputs, or unrelated files. Name: `canonsim_<iter-tag>_<yyyy-mm-dd>.zip`.
- Self-check the archive against BASE_COMMIT before delivery (the path
  list must equal `git status --porcelain -uall` against the base); the
  owner re-checks it against HEAD before applying.

### 12.2 Delivery channels — both, every time files changed

- Save the archive into the session's download directory so it rides the
  chat as a file attachment.
- Upload the same archive to a file host (tmpfiles.org) and post the
  DIRECT download link (`https://tmpfiles.org/dl/...`), the md5, and the
  byte size, so the owner can verify the copy.

### 12.3 The owner-side git block — always the report's last section

Every iteration that changed/created files ends with a copy-pasteable
Git Bash block; every path explicit (§7: never `.` / `-A` / wildcards;
deletions ride explicit `git rm` lines, KI#55; never stage `logs/`,
`output/`, or `*.jsonl` outside `tests/fixtures/`):

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add <path-1> <path-2> ...
git status --short
git commit -m "iter-N-desc: what changed"
git push
```

(The recorded owner root is `C:\Users\fallo\OneDrive\Desktop\repo\canonsim`
— `/c/Users/fallo/OneDrive/Desktop/repo/canonsim` in Git Bash form;
re-confirm with the owner when the checkout moves. Re-listing a path the
owner already committed stages only the real diff — the block stays safe
to re-run.)

- The report itself ends with: what changed, the verification actually
  run, the archive (attachment + link + md5), changed/deleted paths, the
  §12.3 git block, risks, next.
