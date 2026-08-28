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

### 3.1 Measured on the owner's exports (iter-8e, 2026-08-28)

`scripts/df_survey.py` over region1-00250-01-01 ("small", 250y, 315.6 MB)
and region2-00500-01-01 ("medium", 500y, 1.99 GB + 302 MB plus companion);
format: small / medium. Full tables regenerate to `output/df_survey_*.txt`
from the same exports (`dfworlds/`, gitignored; cross-version
reproducibility is not a DF property — the df_design.md determinism
quarantine). F7/F8 are `docs/ref/df_design.md`'s flaw rows.

Scale (bg-3's "tens of MB, 10^4–10^5 events" is off by 1–2 orders):

- events 450,867 / 1,220,772 · distinct types 97 / 99 · collections
  29,663 / 110,519 · figures 44,955 / 105,898 (61% / 83% dead at export)
  · sites 1,575 / 2,273 · entities 3,253 / 7,013 · artifacts 9,158 /
  27,872 · written_contents 46,858 / 113,000.
- events/year grows with compounding history (small: 890 @y1 → ~2,700
  late; medium peak 6,966 @y361, last-10y 2,297) — no density cliff
  inside worldgen.

F7 (macro-dense, micro-empty) — confirmed, one refinement (shares):

- bookkeeping 57.3% / 52.2% · artifact-culture 16.1% / 16.4% ·
  personal-violence 14.6% / 15.5% · **micro (street/personal) 7.7% /
  8.8%** · occasion-ritual 3.5% / 5.1% · war-geopolitics 0.7% / 1.8% ·
  arcane 0.1% / 0.25%; top-5 types = 60.1% / 55.8% of all events.
- Refinement: modern DF is not literally micro-empty — intrigue exists
  (reputation relationships 3.1–3.6%, relationship denied, assume
  identity, trade, gamble, agreements, convictions, reunions) — but it
  is notable-to-notable politics, not street texture: no gossip
  propagation records, theft = artifact theft. The bg-3
  distribution-mismatch warning stands: ≤9% of the log is tavern-scale.
- events-per-figure: p50 7 mentions, p99 44 / 56, max 499 / 2,975;
  top-1% of figures hold 9.1% / 11.1% of mentions (long tail, not
  hub-dominated); 96.4% / 98.5% of figures appear in ≥1 event.

F8 (causality as archaeology) — confirmed and sharpened:

- Only **19.3% / 23.8%** of events sit in ANY collection; orphans (no
  collection ref, no `*_hfid` role, no cause) = 21.3% / 22.7%.
- Direct event→collection references are **unique** (0 events with 2+
  parent collections in either world); collections form strict
  single-parent trees (max 1 parent per subcollection) — the
  many-to-many claim is false for these exports (KI#33). The bg-2
  "2+ collections → candidate_causes" trigger fires never; realistic
  ambiguity = absent role fields (39% / 58% of deaths carry no slayer)
  plus the ~76–81% ungrouped mass.
- `hf died` cause enum: struck 50.6% / 51.7%, old age 21.6% / 27.3%,
  murdered 23.9% / 18.1%, shot 2.4% / 1.6%, executions + suicides <1.5%.
- Median collection holds 1 direct event (p90 = 6, max 665 / 3,222) —
  grouping context is shallow even where it exists.

Pipeline (bg-1) — the validated recipe, `scripts/df_survey.py`:

- Exports are NOT well-formed XML: 24 invalid CP437 control bytes per
  file (12 artifacts × item-quality symbols 0x10/0x11 inside
  `<name_string>`). Byte-level sanitize before parse — safe: CP437 is
  single-byte, UTF-8 continuation bytes are ≥ 0x80.
- Stream: `iterparse` + `elem.clear()` per record + `section.clear()`
  every 4096 records. A non-clearing parse OOMs a 4 GB machine on the
  medium world; the streaming recipe does 1.99 GB in 76 s at 162 MB
  peak RSS (small: 15 s, 74 MB). Never DOM.
- Type names are display-style in the main file ("change hf state",
  "hf died") and snake_case in the plus companion ("change_hf_state")
  — a normalization table is mandatory (KI#33; the old doc examples
  mixed the two styles).
- The plus companion repeats `historical_events` (62% of the main
  count, complementary fields such as `reason`) and adds
  `historical_event_relationships` (118,896 / 281,003), `identities`,
  `creature_raw` — import selectively, never wholesale.
- Collection nesting lives in parents' `<eventcol>` child lists
  (15,581 / 61,648 links); the `parent_eventcol` up-edge is almost
  never set (199 / 710 collections) — reconstruct the tree from parent
  lists. Actual child tags are `<event>` / `<eventcol>` (repeated
  elements), not `event_ids` / `subcollection_ids` (KI#33, fixed in
  `docs/ref/df_legends_xml.md`).

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
