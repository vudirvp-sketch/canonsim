# TECH_NOTES.md — Live Notes (Rot by Design)

> Review quarterly; anything here may already be stale. Model names age in
> ~6 months. Stable rationale lives in `docs/DECISIONS.md` / `docs/VISION.md`,
> never here.

## 1. Model stack snapshot (2026-08, carried from the concept — verify before use)

| Mode | Role | Class | Notes |
|---|---|---|---|
| A narrator | brief → prose | 27B (Qwen 3.8 27B sweet spot; Gemma 4 27B) | 14B acceptable for routine beats with a hard brief |
| B actor | one NPC per call | 12–27B | chorus handled by a scene manager queue |
| C parser | text → Intent JSON | 3–8B + grammar (GBNF / Outlines / guidance / JSON Schema) | on tight RAM, run mode C on the same model as A via constrained decoding |
| F chronicler | offline log compression | any, batched | between sessions |
| G worldbuilder | pack drafts offline | top | through pack CI, never the engine |

No tool use at 12–27B (argument confusion, invented functions) —
grammar-constrained JSON only.

Stack note (2026-03 agent-codegen benchmark, 600 runs — rot by design,
re-verify before any phase-5 decision): Python is the most stable and
cheapest target for LLM-agent code generation (100% task success, lowest
variance and cost); Go/Rust cost more tokens and vary more — supports the
D-031 stack freeze (stdlib-only Python through phase 2; any revisit is
gated by `perf-1` data).

## 2. Hardware reality (the ~25 GB RAM scenario)

- 27B Q4_K_M + Q8 KV-cache @ 8K context ≈ 22–24 GB → one model only; the
  parser runs on the same model through a grammar. A second model = swap =
  a dead session (turn latency 10 s → 2–3 min).
- 14B Q6_K/Q8 ≈ 10–14 GB — the comfortable fallback for long campaigns; with
  a hard brief the prose difference on routine beats is near-zero.
- Cloud: ~$0.01–0.03 per turn at 2 calls × (5K in / 1K out); a 100-turn
  session ≈ $1–3; weekly active play ≈ $50–150/month.
- Prefill cost every beat: a freshly assembled brief invalidates the KV cache;
  mitigate with prefix caching of the invariant prompt head (system + style +
  glossary + PC card). Not fully solvable — the price of a constant-size,
  always-fresh context.
- Measured effective window (attention dilution / context rot) on local
  27B-class models: ~8–16k tokens — the figure's single owner (linked from
  blueprint §1's MECW call-budget law, which budgets against THIS number,
  never the nominal context size). Owner-reported stress-test figure
  (2026-08, reconstructed iter-11b, verified iter-11c); rot by design —
  re-verify before the narrator-boundary iteration.

## 3. DF spike practical notes

- Export: DF Classic (free) + DFHack `exportlegends info`. HEX errors after
  playing a fortress — export from a clean legends-mode save. Translated-name
  layers to strip.
- **Causality is reconstructed, not parsed:** it lives in `event_collections`
  (war → battle → episode) and role fields (killer, abductor), not in
  through-going cause chains. Budget inference work, not parsing work —
  include this in the "cheap evenings" estimate.
- **DF canon is macro-dense and micro-empty** — the exact opposite of the
  tavern: wars and artifacts exist, gossip and pickpocketing do not (DF theft
  = artifact theft). The spike validates briefer mechanics + reverse
  validation, NOT micro-event interestingness — measure that on our own dry
  chronicle, else a distribution mismatch yields a false "briefers are bad".
- Cost references: Park et al. 2023 (Generative Agents);
  "Generative Agent Simulations of 1,000 People" (2024).

### 3.1 Measured on the owner's exports (iter-8e; extended iter-8f, bg-1)

`scripts/df_survey.py` over region1-00250-01-01 ("small", 250y, 315.6 MB),
region2-00500-01-01 ("medium", 500y, 1.99 GB + 302 MB plus), region3-00500-01-01
("small-dense", 500y, 4.95 GB + 232 MB plus — the first export arrived
truncated at 2.91 GB, KI#34; the re-export completed and reproduces the
recovered prefix counts exactly), and a fresh region2-00500-01-01 generated
at the largest world size ("large", 500y, 2.38 GB + 290 MB plus — same slot
name as the old medium, which it replaced on the owner's machine; the
medium numbers below stay as measured); format: small / medium /
small-dense / large. Full tables regenerate to `output/df_survey_*.txt`
from the same exports (`dfworlds/`, gitignored; cross-version
reproducibility is not a DF property — the df_design.md determinism
quarantine). F7/F8 are `docs/ref/df_design.md`'s flaw rows.

Scale (bg-3's "tens of MB, 10^4–10^5 events" is off by 1–2 orders):

- events 450,867 / 1,220,772 / 933,476 / 1,191,388 · distinct types 97 /
  99 / 99 / 101 — 101 across all exports, all classified (zero
  UNCLASSIFIED; "site tribute forced" joined in iter-8f, KI#35; the
  large world alone reaches the full 101-type union) · collections
  29,663 / 110,519 / 93,330 / 197,051 · figures 44,955 / 105,898 /
  76,441 / 98,001 (61% / 83% / 83% / 80% dead at export) · sites 1,575 /
  2,273 / 1,160 / 4,051 · entities 3,253 / 7,013 / 6,038 / 12,557 ·
  artifacts 9,158 / 27,872 / 21,383 / 27,250 · written_contents 46,858 /
  113,000 / 86,166 / 90,947.
- **World size scales geography and occasions, not history volume** (the
  owner's "why is the large world barely bigger" question): large vs
  medium at the same 500y — sites +78%, entities +79%, collections +78%
  (occasion-ritual share doubles, 5.1% → 10.4%), yet events −2.4%,
  figures −7.5%, artifacts flat, written_contents −19%; export size +20%
  (1.99 → 2.38 GB). The notable population and its interaction rate do
  not scale with map area — the event log is sized by the history
  engine, the file by geography on top of it.
- events/year grows with compounding history (small: 890 @y1 → ~2,700
  late; medium peak 6,966 @y361, last-10y 2,297; small-dense mean 1,867,
  peak 6,176 @y220, last-10y 1,722; large peaks at the year-1 genesis
  burst — 4,200 @y1 — then declines to last-10y 1,685) — no density
  cliff inside worldgen, and the large world's shape is front-loaded,
  unlike the medium's mid-history peak.

F7 (macro-dense, micro-empty) — confirmed, one refinement (shares):

- bookkeeping 57.3% / 52.2% / 48.2% / 48.2% · artifact-culture 16.1% /
  16.4% / 15.3% / 15.3% · personal-violence 14.6% / 15.5% / 19.9% /
  13.9% · **micro (street/personal) 7.7% / 8.8% / 7.7% / 8.5%** ·
  occasion-ritual 3.5% / 5.1% / 3.9% / 10.4% · war-geopolitics 0.7% /
  1.8% / 4.3% / 2.7% · arcane 0.1% / 0.25% / 0.7% / 1.1%; top-5 types =
  60.1% / 55.8% / 53.7% / 50.0% of all events. The dense setting trades
  bookkeeping for violence and war; the large setting trades it for
  occasions — the micro ceiling holds everywhere.
- Refinement: modern DF is not literally micro-empty — intrigue exists
  (reputation relationships 3.1–3.6%, relationship denied, assume
  identity, trade, gamble, agreements, convictions, reunions) — but it
  is notable-to-notable politics, not street texture: no gossip
  propagation records, theft = artifact theft. The bg-3
  distribution-mismatch warning stands: ≤9% of the log is tavern-scale.
- events-per-figure: p50 7 mentions, p99 44 / 56 / 73 / 72, max 499 /
  2,975 / 1,644 / 1,157; top-1% of figures hold 9.1% / 11.1% / 12.9% /
  12.7% of mentions (long tail, not hub-dominated); 96.4% / 98.5% /
  95.4% / 98.0% of figures appear in ≥1 event.

F8 (causality as archaeology) — confirmed and sharpened:

- Only **19.3% / 23.8% / 30.7% / 29.9%** of events sit in ANY collection;
  orphans (no collection ref, no `*_hfid` role, no cause) = 21.3% /
  22.7% / 20.3% / 20.4%.
- Direct event→collection references are **unique** (0 events with 2+
  parent collections in any world — quad-confirmed on the large world);
  collections form strict single-parent trees (max 1 parent per
  subcollection) — the many-to-many claim is false for these exports
  (KI#33). The bg-2 "2+ collections → candidate_causes" trigger fires
  never; realistic ambiguity = absent role fields (39% / 58% / 59% /
  64% of deaths carry no slayer — the large world is the most
  slayer-less) plus the ~70–80% ungrouped mass.
- `hf died` cause enum: struck 50.6% / 51.7% / 51.0% / 49.8%, old age
  21.6% / 27.3% / 32.6% / 40.1%, murdered 23.9% / 18.1% / 13.6% / 6.6%,
  shot ≤1.9%, executions + suicides <2.5% — the large world is the
  most peaceful (old age dominates for the first time).
- Median collection holds 1 direct event (p90 = 6 / 6 / 6 / 3, max 665 /
  3,222 / 826 / 430) — grouping context is shallow even where it
  exists.

Pipeline (bg-1) — the validated recipe, `scripts/df_survey.py`:

- **Exports can arrive truncated (KI#34, iter-8f):** the DF exporter died
  mid-write on the small-dense world — 2.91 GB cut inside a battle
  collection, no `</df_world>` (the 7z CRC was intact: the cut happened
  at export time, not in transit). The survey tail-checks for
  `</df_world>` and, on failure, streams through a recovering reader
  that tracks the open-element stack and synthesizes the missing closing
  tags at EOF (loud PARTIAL warnings; deterministic). Ground-truth
  validation: the completed 4.95 GB re-export reproduces the recovered
  prefix counts exactly (events 933,476 · types 99 · micro 7.71% ·
  slayer 41.35%); only collection-derived numbers were partial in the
  truncated copy (referenced 14.99% → 30.74%). bg-1's SQLite sink must
  own its truncation policy (abort vs flagged partial import).
- Exports are NOT well-formed XML: raw CP437 control bytes (item-quality
  symbols 0x10/0x11) sit inside artifact `<name_string>` — measured
  24 / 24 / 12 bytes per file. Byte-level sanitize before parse — safe:
  CP437 is single-byte, UTF-8 continuation bytes are ≥ 0x80.
- Stream: `iterparse` + `elem.clear()` per record + `section.clear()`
  every 4096 records. A non-clearing parse OOMs a 4 GB machine on the
  medium world; the streaming recipe does 1.99 GB in 76 s at 162 MB
  peak RSS (small: 15 s, 74 MB; small-dense: 4.95 GB in 167 s, 141 MB —
  cost is linear in file size). Never DOM.
- Type names are display-style in the main file ("change hf state",
  "hf died") and snake_case in the plus companion ("change_hf_state")
  — a normalization table is mandatory (KI#33; the old doc examples
  mixed the two styles).
- The plus companion repeats `historical_events` (62% of the main
  count, complementary fields such as `reason`) and adds
  `historical_event_relationships` (118,896 / 281,003 / 227,215),
  `identities`, `creature_raw` — import selectively, never wholesale.
- Collection nesting lives in parents' `<eventcol>` child lists
  (15,581 / 61,648 / 64,453 links); the `parent_eventcol` up-edge is
  almost never set (199 / 710 / 464 collections) — reconstruct the tree
  from parent lists. Actual child tags are `<event>` / `<eventcol>`
  (repeated elements), not `event_ids` / `subcollection_ids` (KI#33,
  fixed in `docs/ref/df_legends_xml.md`).
- **Coverage audit** (iter-8g, `scripts/df_survey.py --audit`):
  per-section per-record-tag counts + every unique child-tag set per
  record tag (a structural fingerprint — DF records of the same type
  are uniform, so the set is 1-3 elements; growth past 3 is schema
  drift). Replaces head/middle/tail positional sampling strictly — it
  captures every structural variant, not three positions. The
  HANDLED set (historical_event / _collection / _figure — the F7/F8
  detail records) is marked, UNHANDLED records (site, entity, region,
  artifact, written_content, …) carry their child-tag sets so bg-1's
  SQLite sink can plan field extraction without re-parsing a 5 GB
  export. Coverage matrix: `docs/ref/df_legends_xml.md`. Any record
  tag outside the matrix renders as UNDOCUMENTED (implemented bg-1,
  KI#36 — first catches: `artifact`, missing from the matrix despite
  being in every export, and `historical_era`).

### 3.2 SQLite sink — bg-1 closed (`scripts/df_import.py`, D-051)

The bg-1 AC (parser loads a world into SQLite) is met and
cross-validated: importing the large world (2.38 GB) reproduces the
survey's numbers exactly — events 1,191,388 · event_membership 355,596
(= referenced-by-≥1-collection) · collection_parent 132,875 (= eventcol
child links; all 1,510 `parent_eventcol` up-edges agree with the parent
lists) · event_participant 1,030,343 (= total figure mentions) ·
records 139,534 (= the seven non-noise UNHANDLED sections). Single
pass, 174 s, 898 MB DB, ~190 MB peak RSS (the survey's streaming law,
unchanged). Schema and policy, single owner `scripts/df_import.py`
(docstring); the load-bearing facts:

- **Typed cores + EAV:** events/collections/figures get typed columns
  (id, type, year/…, race/birth/death) plus `*_fields` EAV tables
  carrying every other child tag — repeated tags survive, identical
  duplicates collapse, nested children serialize as canonical JSON
  (sorted keys, parse order preserved). `event_participant (hfid,
  event_id)` lifts every direct child tag ending in `hfid` — bg-3's
  "figure Y's own records" query is a PK prefix scan (measured 4 ms for
  the world's top figure, 1,157 events). Every non-noise UNHANDLED
  record lands in one generic `records` table as native JSON —
  including future UNDOCUMENTED tags, so schema drift never breaks an
  import.
- **Truncation policy (the bg-1 remainder's owned decision):** default
  = flagged partial import (`meta.partial=1`; the record in flight at
  the cut lands with its parsed prefix of fields — KI#36 measured
  behavior, shared with the survey so counts cross-validate);
  `--strict` aborts before parsing. The DB is always rebuilt fresh
  (rebuildable index, D-003 analog; no journal/fsync pragmas).
- **Skips:** art/dance/musical/poetic forms (matrix design-noise law —
  counted, not stored); the plus companion is not imported at all
  (selective import, never wholesale — its complementary fields defer
  until bg-2/bg-3 actually need them).
- **Determinism quarantine:** DB content is a pure function of the
  export bytes — parse order, canonical JSON, no wall-clock in `meta`;
  re-import yields identical rows (pinned in `tests/test_df_import.py`).
  No golden DF fixtures, no cross-DF-version byte-identity claims.

## 4. Python determinism recipe

- `PYTHONHASHSEED=0` (env, CI, docs); randomness flows only through the
  `RngBank` — one master seed, named streams derived via
  `stable_hash(f"{seed}:{stream}")` = sha256-based, environment-independent
  (INV-2, D-028; RNG-1 in `docs/BLUEPRINT.md`); cosmetic draws never touch
  the canon path;
  no wall-clock anywhere **including the log header**; iterate only via
  `sorted()` or construction order; queue key `(tick, sub_order, actor_id)`.
- The byte-identical guarantee is same-environment only: the header records
  the Python version; cross-version identity is NOT claimed.

## 5. Integration risk (why the LLM waits)

Early integration is the real hazard: a narrator masks simulator holes with
pretty prose. The briefer / validator / renderer are exercised on foreign
canon (track B) in parallel; they switch to our canon only after the phase-0
gate. One track can be dropped without losing the other.

## 6. Static-lore retrieval stack (owner survey rev v2 — rot by design)

- Zero-dependency default: **SQLite FTS5** keyword search over facts and lore.
- Vector layer, **static lore only**: sqlite-vec or LanceDB + a light CPU
  embedder (nomic-embed-text / bge-m3); optional cross-encoder reranker if
  the corpus outgrows keyword search. Licenses not yet verified — "verify" in
  `REFERENCES.md` §5/§6; D-016 check at phase-4 intake.
- Qdrant demoted (rev v2): only where server infra already exists;
  local-first is the default.
- Hard boundary (`VISION §5`): dynamic world state = SQL + `known_by`, never
  vector search. RAG never touches dynamic facts; the LLM receives a brief,
  not a retrieval session.
- Phase-1 QA metrics from the survey: p50/p95 turn latency, repeat and
  stagnation counters, degradation/refusal rates — wire into the mode-A
  harness when it exists.

## 7. Log as a stream (jq discipline)

The JSONL log is a stream, not a document: filter → map → group compose
like Unix pipes. `AGENTS.md` §3 is the law (never open a runtime log
whole); these are the stdlib idioms:

- filter by type:
  `python -c "import sys,json; [print(json.dumps(e)) for e in map(json.loads, sys.stdin) if e.get('type')=='rumor']" < logs/run.jsonl`
- count by type:
  `python -c "import sys,json,collections; print(collections.Counter(json.loads(l)['type'] for l in sys.stdin))" < logs/run.jsonl`
- slice one actor: add `if e.get('actor')=='guard_01'` to the filter
  idiom; `tail -n`, `wc -l`, and `grep '"cause": "ev_'` for quick
  cause-chain walks — M3's real home is the metric harness, never grep.
