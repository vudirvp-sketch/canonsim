# 04 — Measurement Gaps

These are empirical gaps. Treat them as measurement / falsification work, not as reasons to enlarge the runtime by intuition.

## M1 — Target-model pipeline

Known:

- Architecture assumes a 27B sweet spot (14B for routine work).
- Existing prose batteries were run on API-class models.
- Local observations: E4B fails to narrate; 12B returns prose instead of reply document; Q9B is mixed; 27B has only smoke-level evidence.
- Phase-1 machinery gates used operator answers, not full target-model confabulation behaviour.

Required:

- Full 27B one-model live battery through the actual mediator + claims path.
- Record structured-validity, semantic-authority, grounding, regeneration, latency, and failure-mode distributions.
- Run only after the semantic / representation / recovery contracts are sufficiently defined.

## M2 — Claims vocabulary mismatch

Known: model surface vocabulary can differ from canonical IDs; weak hardware can trigger refusal-heavy behaviour.

Required A/B:

- surface→canonical-ID normalisation strategies;
- policy for unverifiable claims: block, downgrade, or allow as non-canonical narration;
- decision metric = reduction in semantic friction without increasing canon leakage.

## M3 — End-to-end playtime budget

Known local benchmark: 27B Q4_K_M on RTX 3080 Ti ≈ 4.51 tok/s; roughly 30–55s per reply before parse/regeneration overhead.

Required:

- one-model vs two-model economics;
- end-to-end latency with realistic brief sizes and regeneration rates;
- acceptable user-visible budget by interaction mode.

Do not call “local-first viable” a measured fact until this exists.

## M4 — Injection + wrong-but-committed recovery

Known: instruction-shaped injected output can reach intent handling and may end in `intent_rejected` or a real event. Canon is intentionally irreversible; no undo/retcon path exists.

Required:

- measure semantic intent distinction limits;
- classify instruction / proposal / authority / realised intervention / canonical consequence;
- owner decision on whether any dispute/recovery path is allowed, and under what canonical semantics.

## M5 — Soul-of-Waifu integration horizon

Open product questions: AGPL/GPL combined-work implications, conceptual overlap, voice/realtime, context ownership, emotional-time vs simulation tick-time.

Keep horizon-only until the owner explicitly opens it.

## Measurement order

1. M1 target-model live battery.
2. M2 claims normalisation A/B.
3. M3 playtime budget.
4. M4 injection / dispute policy.
5. M5 SoW product decisions.
