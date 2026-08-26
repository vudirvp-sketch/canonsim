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
  playing a fortress — export from a clean legends-mode save. Hundreds of MB
  for large worlds; translated-name layers to strip.
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
