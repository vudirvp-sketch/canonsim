# agent-memory-atlas · `REFERENCES.md` §5 · MIT (verified 2026-08-28, GitHub API) · track B (phase-1 scene ledger) + phase 4 (memory patterns)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1 (ref-16 — owner-requested
> fresh source, the D-022 doc-pass exception; absorbed inside iter-8a,
> no solo iteration). Anti-drift (D-026): catalog/license/URL/phase
> gating in `docs/REFERENCES.md`; one-line synthesis in
> `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics here. License
> filter and "patterns not content" rule: `REFERENCES.md` §0.7 (D-015).
> Source: `neoneye/agent-memory-atlas` (MIT, license checked via the
> GitHub API 2026-08-28), content pinned 2026-08-06. Corpus: 151 OSS
> agent-memory systems reviewed at pinned commits by static code
> reading, judged against 7 binary capability marks and 22 named
> patterns; two suites executed (CLIO `test_ltm_corroboration.pl` — 92
> assertions; Aura `tests/test_audit_chain.py` — 16 tests). Read: the
> distilled research extract supplied by the owner (2026-08-28), not
> the repo tree — the extract is itself the structured artifact
> (per-system reports + pattern library under `content/`). Role for
> canonsim: the pattern source for the phase-1 **scene ledger**
> (`docs/blueprint/phases.md` §1, D-048) and a design checklist for
> phase-4 memory (reflection provenance, retrieval, legends).

**What it is.** A meta-survey: 151 memory systems × 7 strict capability
marks × 22 named functional patterns, each pattern with carriers,
counterexamples, and failure modes — the missing cross-system grammar
for "what does agent memory actually consist of", telegraphic and
sourced (every claim names a system slug or a pattern).

**Concrete mechanics.**

The **admission test** is itself a design lesson: a memory is something
that "survives the session with an identity that can later be
corrected" — sophisticated chat-buffer compactors are excluded, a
300-line Markdown file with stable entry IDs is admitted. Identity +
corrigibility, not sophistication, is the bar.

The **7-mechanism rubric** (binary marks; "partial" rejected because
the middle bucket absorbs every hard case): (1) rejected-value
tombstone — 8/151; (2) explicit trust state (discrete epistemic status,
not a float) — 24/151; (3) bi-temporal validity — 14/151; (4) scope
enforced in retrieval — 85/151; (5) append-only mutation audit — 32/151;
(6) human review surface — 34/151; (7) negative retrieval assertion
(forbidden-hit tests) — 25/151. The counts are the finding: scope is
the most implemented and shallowest mechanism; correction is "the
phase that goes unbuilt"; trust is "usually a number, not a state" —
a confidence float can rank but cannot express *rejected*, so it
cannot survive being wrong.

The **22-pattern catalog** is the reusable part. Each pattern is a
failure-prevention move, not a checklist item; each names its carriers
(Verel, RainBox, SillyTavern, Graphiti, letta, MemPalace…) and its
counterexamples. The canonsim-relevant subset, with verdicts:

| Pattern | Carriers (atlas) | Canonsim verdict |
|---|---|---|
| Trust-state machine (Candidate → Verified → Stale → Rejected; discrete, retrieval-gated) | Verel, Gini, Magic Context | **take** — scene-ledger lifecycle states (blueprint §1, D-048); no confidence floats anywhere |
| Rejected-value tombstone (keyed on the *value*, refuses re-write; "a tombstone you got for free is one you can lose for free" — Mnemosyne's accidental one is untested) | Verel, RainBox, memsem, Perseus Vault | **take** — contradicted/prompted-away texture is laundering-refused at the mediator |
| Retrieval hysteresis (sticky / cooldown / delay per unit; "known solution to a problem the rest of the field has, sitting in codebases the rest of the field does not read") | SillyTavern, RisuAI, Project N.E.K.O. | **adapt** — pinning (player-referenced texture stays for the scene); retirement on explicit decisions, never turn counters alone |
| Memory as editing surface (every verb the automatic path has, the human has) | SillyTavern, RisuAI, Logseq | **adapt later** — the dumb terminal's scene panel (VISION §10) is the surface; player reference = pin; full edit verbs = the frontend phase, deferred |
| Evidence before belief (raw event first; derived records cite evidence ids; source outranks derived on contradiction) | MemPalace, Graphiti, MemMachine, nanobot | **take** — every ledger entry keeps its verbatim `surface` + provenance; mirrors the reflection-provenance law already in blueprint §4 |
| Scope as a first-class key (in the memory key, not a metadata tag) | Memory Engine, OpenClaw, Memobase | **take** — ledger entries carry `scope` = scene or entity; the brief filters by current scene |
| Zero-LLM capture (no model call on the synchronous write path) | agentmemory, Claude-Mem, OpenClaw | **adapt** — the ledger write is a deterministic parse of the narrator's structural side channel; no second call |
| Governed write gateway (every mutation through one transactional path) | RainBox `record_belief`, Verel, MateClaw | **already ours** — the intent door + the `_commit` gate (D-035/D-037); the atlas independently validates the design |
| Decay and reinforcement (decay reachability, never truth) | Verel, NOOA, Redis Agent Memory Server | **reject for texture** — no TTL, no timers (the MTTH lesson); retirement is always an explicit recorded decision |
| Promotion between tiers ("the discriminating question is not whether the tiers exist but what moves a memory up one") | Core Memory, Cambium, NOOA | **take the discipline** — texture→canon promotion is one named rule (the intent door), computable and cause-linked |
| Background summarization / chained compaction (named antipattern: a summary that replaces its source has no per-fact identity) | CowAgent, RisuAI (negative); letta `summarize_messages_in_place` (negative) | **reject** — already law (blueprint §4: originals never dropped; letta's in-place summarize is our named anti-pattern) |
| Vector retrieval over dynamic facts | — (counter: our `TECH_NOTES.md` §6) | **reject** — the atlas never contradicts the boundary: hard filters + lexical/structural beat retrieval for anything dynamic |
| Bi-temporal validity (application time vs system time) | Graphiti, Gini, Atomic Agent | **defer** — canon ticks are one deterministic clock; session-scoped texture needs no second clock; revisit only if texture ever outlives sessions (it must not, D-048) |
| Cache-preserving injection (stable bytes in the cached prefix, volatile last) | Hermes Agent, Memobase | **note** — already `TECH_NOTES.md` §2 (prefix-cache the invariant prompt head); the ledger never sits in the head |

The **headline findings** map onto us almost one-to-one: (1)
correction unbuilt → our contradicted-state + refusal exists from day
one, not as a retrofit (the atlas's hardest-won lesson: retrofitted
correction is where memory systems go to die); (2) negative evidence
untested → the phase-1 regression suite must carry forbidden-assertion
cases (prose that must NOT re-assert a contradicted detail) alongside
the canon-violation count; (3) scope shallow → the ledger's scope key
is structural (in the entry, filtered at assembly), not a tag.

The **stacks**: the Correctable Stack (scope → evidence → gateway →
tombstone, in that order — "each cheap alone, expensive to retrofit")
is precisely the layering our existing law already has; the Companion
Stack (hysteresis + editing surface) is the part we were missing and
now take via pinning + the scene panel. The atlas's central prediction
— next-generation memory is judged on paradigm-8 properties
(correction, provenance, governance), not retrieval quality — is the
external confirmation of the canonsim thesis itself: determinism and
corrigibility over plausibility.

**What we take.** The trust-state machine shape (discrete states, no
floats) for the ledger lifecycle; the rejected-value tombstone as the
laundering refusal; hysteresis as pinning; evidence-before-belief as
the `surface` + provenance fields; scope-as-key as the entry `scope`
field; the forbidden-assertion test discipline for the phase-1
regression suite.

**What we adapt.** Zero-LLM capture — our capture rides the narrator
call's structural side channel (one call, two jobs: prose + texture
delta), a stricter variant than the atlas's hook pattern. Hysteresis —
SillyTavern's four knobs collapse to one (pinned) because scene
retirement is deterministic in our architecture (canon move events
define scene boundaries; no turn counters). The editing surface —
read-only + reference-to-pin at phase 1, full verbs only if the
frontend ever wants them.

**What inspires us.** The admission test: *identity + corrigibility,
not sophistication* — the same bar INV-1/INV-5 set for canon, now
restated for rendering state.

**Strengths.** Breadth with teeth: 151 systems, binary marks, named
counterexamples per pattern (the counterexamples are worth more than
the carriers); telegraphic, sourced, no filler; the pattern catalog is
directly reusable as a design checklist; two reference suites actually
executed; honest about method limits (static review, OSS-only,
mid-2026 skew; closed hosted products out of reach).

**Weaknesses.** It is a survey of *chat-assistant and coding-agent*
memory — companion/roleplay systems appear but tavern-class
world-simulation with a deterministic canon does not exist in the
corpus; nothing there faces our actual constraint (a byte-identical
replayable log), so every verdict needed translation, not copying.
The "one score for truth and reachability" and "telemetry mistaken for
truth" antipatterns describe systems with feedback loops we simply do
not have (no retrieval telemetry reaches belief in our architecture —
the read side is pure functions of the log). No benchmark exists for
the exact failure we care about (the atlas says so: "forgetting has no
benchmark") — our scene-continuity metrics will have to be built, not
quoted.

**Verdict.** The pattern source for the scene ledger (D-048) and the
phase-4 memory checklist; consumed via translation — every take/adapt
verdict above is a canonsim-shaped restatement, never a copy, per the
standing policy (`REFERENCES.md` §0.7). The atlas's deepest
contribution is negative-space: our architecture already is the
Correctable Stack; the one unbuilt cell was the texture lifecycle,
which is exactly what iter-8a designed.
