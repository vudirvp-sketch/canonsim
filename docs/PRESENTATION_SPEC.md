# PRESENTATION_SPEC.md — The LLM Presentation Contract (presentation-1)

> Trigger fired: the exit criterion MET (iter-174 — the weak-arm run on
> owner hardware; the narrator floor measured between E4B and Q9B);
> written iter-178 FROM the measured results (D-022: a contract without
> a consumer has unknown requirements — the consumer landed FIRST:
> `cli/engine.py`, iter-177/D-193). Single owner of the MODEL-FACING
> serializer surface; the brief's own contract stays `BRIEF_SPEC.md`'s
> and the parse boundary's `PARSER_SPEC.md`'s — this spec is a THIN
> mapping table over the stable IR (the eight blocks +
> `narrator_protocol`), never a second re-labeling vocabulary (D-024).
> Absorbs `st-4` at write time (the call budget + the transcript-tail
> contract + thinking-as-ephemeral-texture + the Script Tax clause —
> one owner, never two). The consult cards' integration (§8–§10);
> the measured numbers' owner: TECH_NOTES §13.1 (rotting — this spec
> cites, never restates). ≤300 lines.

## 1. What this contract is

The model-facing serializer over the STABLE brief IR — the D-055
file-contract pattern's fourth instance (the narrator door, the parse
door, the validator's reply document, and now the request side). What
it maps: the doors' call documents (already byte-stable pure functions
of (log, ledger, pack) — the D-049 quarantine) → the chat-completions
request; the backend's response → the doors' reply documents. The law
that governs everything below: **the serializer re-labels, never
re-writes** — the call documents' bytes ride verbatim; the mapping is a
pure function of (the call document, the engine config), so the request
identity is pinned (D-192's D3 request tier: same call bytes + same
config → same request bytes).

The consumers: the repo-side adapter `cli/engine.py` (the session's
`--engine` operator — the only network module, INV-4's form) and the
Rule-9 experiment runners (outside the repo, D-046) — both obey this
table; the doors' gates are byte-identical for either consumer.

## 2. The mapping table (the whole contract)

| Call element | Model-facing form | Source owner |
|---|---|---|
| The parse call document | the USER message, **DOCUMENT-ONLY** — no parser-side system role (the measured request identity; a system role would shift every agreement number's identity, D3) | PARSER_SPEC §3 |
| The narrator call, block 1 (`directives`) | the **SYSTEM role** — the pack's mode-role lines are the standing law (BRIEF_SPEC §3.1's recorded intent; L2: facts as tokens, the role as law) | BRIEF_SPEC §3.1 |
| The narrator call, blocks 2–8 + `narrator_protocol` | the USER message, **byte-verbatim** (the D-049 purity) | BRIEF_SPEC §3/§7.1 |
| The mode-B actor calls | the same mapping (the knower's own document; the `actor:`/`query:`/`retrieval:` lines ride the user message like every protocol line) | BRIEF_SPEC §3.9/§7.1 |
| The off-grammar re-ask | a repair turn: user (the original call) / assistant (the refused bytes verbatim) / user (the refusal note — the nearest-valid menu riding it, iter-107); still grammar-constrained | PARSER_SPEC §5 |
| The reply documents | the response's content, verbatim, to the reply file (the file contract preserved — the engine is "the operator"); validated at the doors' gates, never here | VALIDATION_SPEC §7.1; PARSER_SPEC §4 |
| The GBNF grammar | the TOP-LEVEL `grammar` param, **the parse door only** — the narrator side is unconstrained by design (the measured E4B json-retry exhaustion: a constrained narrator emits no prose at this band; the boundary validates, the source stays free) | PARSER_SPEC §2.1 |
| Sampling identity | `temperature`: parse 0 / prose 0.8 (the round-4 recipe); `seed`: the config's (the seeded-local tier — byte-identical replies at a fixed manifest); `chat_template_kwargs.enable_thinking`: **false, every request** (the empty-content trap: reasoning consumes `max_tokens`) | this spec §5; TECH_NOTES §13 |
| Completion budgets | `max_tokens`: parse 160 (the measured ~617-token prompts + ≤160 completions); prose 512 (the beat scale — the exemplars' own 100–200-token band) | this spec §3 |
| Provenance | the per-run manifest row (model+sha256, `build_info`, params, the first parse call's grammar id, the seed) — `output/engine/`, a runtime artifact, never canon | D-192's D3; TEST_PLAN §8.4 |

## 3. The call budget (st-4's first half, absorbed)

The arithmetic, never a guessed number: **head + document + output ≤
the effective window** (`n_ctx_slot` — the `-np` halving law pins it:
the requested context is NOT per-slot under parallelism, §13). Head =
the system role + the chat template's own tokens; document = the call
document's model tokens; output = the completion budget; thinking = 0
(§5). The anchors, measured at the committed packs: the parse calls
~617 model tokens; the narrator calls bounded by the brief's OWN
budgets (BRIEF_SPEC §5's per-block soft/hard + `total_hard`, the
eviction contract owning the document side — this spec adds no second
budget mechanism). The terminal signal `finish_reason: "length"` is
observable and surfaces to the operator (never a silent truncation —
I6). A budget breach is a CONFIG change (the pack's brief budgets, the
adapter's completion budgets), never a FORMAT change: the document
bytes stay what they are.

## 4. The transcript-tail contract (st-4's second half — the measured resolution)

**No tail.** The call documents are self-contained state summaries
(O(relevance), never O(history) — BRIEF_SPEC §1): the recency channel
is the brief's own block ranking (scene_delta/scene_texture first —
current-scene continuity outranks recall, D-049; recent-facts-first
assembly), and the voice channel is the voice_exemplars block's
position law (near the context end, BRIEF_SPEC §3.7 — the live-char
author's-note geometry). The measured runs never carried a tail (the
committed corpora + all four station rounds), and a prose-echo channel
would be a second chronicle (D-024 — one owner per fact). The
multi-turn surface exists ONLY inside the bounded repair turn (§2) —
never across beats: each call document stands alone.

## 5. Thinking as ephemeral texture (st-4's third half, absorbed)

Reasoning is an engine/request concern, never a presentation flag
(D-192's D4): it changes request identity, output budget (the
thinking-consumed-`max_tokens` fact), parsing, and latency. The recipe
is the contract: **thinking OFF on every request**. IF a future band
runs thinking-on (a measured decision, never a default): the thinking
text is EPHEMERAL — never canon, never a ledger entry, never texture,
never riding the next call (unlike the refusal notes, which are the
operator's own feedback channel); it is engine metadata (I6), recorded
nowhere the log can read.

## 6. The Script Tax clause (st-4's fourth half, absorbed)

The presentation layer is script-agnostic: the utterance and the
documents ride verbatim, UTF-8 end to end — no normalization, no
transliteration, no casing passes (the gates were always script-blind:
F5's measured confirmation). The tax at the 3–8B band is a parse-side
validity/mix cost (Q9B's Cyrillic twins needed the one re-ask; E4B
clean 7/7) with ZERO latency penalty (§13.1) — it shows up in the
heartbeat's re-ask row (TEST_PLAN §8.5), never in the format. The
presentation contract refuses every script-specific branch.

## 7. The narrator band (the measured bound, §4.3 arm d)

Mode-A prose at the weak arm: the 4B class is **parser-only** at this
call shape (every beat dry across all three ladders — the narrator
replies are not valid JSON, the bounded json-retry ladder exhausted);
the 9B class **narrates** (6/8 accepted per ladder, the regen ladder
working). The narrator floor sits BETWEEN 4B and 9B: the contract's
consumer requirement — the narrator door needs a ≥9B-class model at
this station shape; the 3–8B band serves the parse door
(GBNF-constrained). The 12–27B band stays the §1 sweet spot; the
one-model-constrained A/B (27B GBNF parse) is TEST_PLAN §8.5's standing
gap row, the owner's next station run.

## 8. The re-expansion law + the staged interpretation (intake-32's card, mapped)

The brief IS the bounded model-facing context bundle (the Vantiel
card's law, D-190): every block carries stable event/entity handles —
the scene_delta's event ticks, the present_entities ids, the texture
entry ids (`{entry, scope, slot, value}`, copy-verbatim), the
retrieval refs with their minting event ids — and the bundle re-expands
deterministically from canonical evidence (the fold, T2-proven). The
bundle is DISPOSABLE by design (assembled fresh per beat, the ledger
dies with its session — D-049): never a second truth, never a mutated
memory. The staged-interpretation sketch maps onto the existing loop
with NO new stage: input (the utterance) → interpretation (the parse
door's reply) → bounded context (the brief) → model decision (the
narrator reply's proposal) → repository validation (the validator's
verdicts) → prose (the accepted beat) — the owners PARSER_SPEC /
BRIEF_SPEC / VALIDATION_SPEC respectively. The card's falsifier (the
real consumer vs the current stack on context cost, traceability,
re-expansion correctness): answered by measurement — the prompts are
bounded (~617 tokens at the committed packs), the handles are the
documents' own lines, the re-expansion is the fold. **The card
dissolves as already-satisfied**; this section is the mapping record.

## 9. The outcome-perception layers (intake-33's card, D-191's falsifier applied)

Each layer either changed the model-facing shape or dissolved as
already-satisfied; the honest verdict: **no layer changed a shape** —
the card is a cross-domain confirmation, not a redesign.

- **Truth never bends** — the validator's honest verdicts against
  CURRENT canon (VALIDATION_SPEC §4). Dissolves.
- **Failure carries cause + avoidance path** — the parse door's
  nearest-valid menu (iter-107: the refusal payload IS the avoidance
  path), the world's `intent_rejected` answers (attempts are facts),
  the narrator's REFUSED notes with reasons. Dissolves.
- **Odds as expectation bands, never naked percentages** — nothing in
  the model-facing surface renders odds (the checks are the door's;
  the surface carries facts and options). The clause stands as LAW for
  any future odds surface: bands as pack data, never a dice UI.
- **Transparency opt-in, nothing dropped silently** — the brief's
  `[truncated:N items dropped]` markers (BRIEF_SPEC §5), the doors'
  loud refusals, the adapter's stop-reason note (§3). Dissolves.
- **Outcomes legible through residue** — the committed event IS the
  residue (INV-1); the chronicle renders it. Dissolves.
- **Stakes irreversible** — the append-only log; corrections are new
  events (INV-5). Dissolves.

## 10. The visual surface fence (intake-30's card)

This contract owns the MODEL-facing surface only. The visual/render
surface — the development-order law (prove the semantic read surface
first), the fidelity target ("the world should look the way it does
BECAUSE the simulated world is the way it is"), the rejection table
(universal WFC; asset-heavy sprites as primary; full-scene AI image
generation as truth) — stays PARKED behind the SoW fence (D-187,
D-174's recorded ownership): the card's consumers are the SoW frontend
debates, and the semantic read surface it demands already exists on
this side (the brief IS that surface — the falsifier satisfied by the
IR itself). No visual vocabulary enters this spec.

## 11. Versioning

Code-owned (`cli/engine.py` + `brief/gbnf.py` — the mapping table's
executable form). A change to §2's mapping or §3's budgets = a spec
edit in the same commit as the code change (BRIEF_SPEC §8's pattern);
the measured numbers re-anchor at the owner's station runs (TECH_NOTES
§13's rot law), the table's LAWS stay.
