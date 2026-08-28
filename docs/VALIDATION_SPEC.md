# VALIDATION_SPEC.md — Validation Contract (Phase 1)

> Trigger fired at phase-1 start (`docs/SPECS_BACKLOG.md` sketch row); written
> iter-9 from the built LLM-free half, not ahead of it. Single owner of the
> validator's contract; the mechanism donors are `docs/blueprint/phases.md` §1
> (the validator + the scene ledger). The intent door stays `INTENT_SCHEMA.md`'s,
> events stay `docs/EVENT_SCHEMA.md`'s — this doc never restates them. No LLM,
> no network anywhere in this contract (INV-4 holds until the owner-gated
> narrator-boundary iteration, AGENTS §8). ≤300 lines.

## 1. What the validator is

The validator is the mediator's **deterministic gate between every LLM output
and canon**: `proposal → check → commit → narrative` (VISION §4 Layer 2). It
is a pure function of `(proposal, log, pack)` — no RNG, no wall-clock, writes
nothing (INV-1/INV-2; the D-042 read-side family). The commit step is the
intent door and ONLY the intent door (D-037): the validator never writes
canon, never merges, never sanitizes text. The narrative step is the
narrator's, owner-gated.

Scope split inside phase 1:

| Half | Status | Contents |
|---|---|---|
| LLM-free (iter-9, this spec's code) | landed | proposal shaping (§3), verdicts (§4), ExpectedVersion OCC (§5), fact-transaction pass-through (§6), regen protocol core (§7), golden-set plumbing (§9) |
| Live wiring (owner-gated, AGENTS §8) | deferred | the narrator call itself, the extraction pass, dry-mode rendering, the mediator session loop |

## 2. The structural boundary (injection neutralization, D-018)

Mode-A prose is **never a fact proposal**. The validator accepts exactly one
structured document shape (§3); there is no prose field anywhere in it, so
**no post-hoc text sanitization exists or is needed** — prompt injection can
carry instructions, but instructions are not a claim, an intent, or a slot,
and nothing else crosses this boundary. Shape violations raise `ProposalError`
loudly: the grammar-constrained emitter (the phase-2 C-parser, or a test
harness) is the author, and author bugs crash (the loud/soft front-door law).
Malformed LLM output is the boundary's degradation problem (ladder:
extraction pass → dry mode, L12), handled BEFORE the validator is called —
the validator itself never guesses, never repairs, never degrades.

## 3. The proposal document

One document per narrator call, machine-shaped:

| Field | Type | Req | Meaning |
|---|---|---|---|
| `expected_event_seq` | int ≥ 0 | yes | the log's event count the proposal was based on — the OCC anchor (§5) |
| `claims` | list of Claim | no | assertions the prose makes about canon (reverse validation, §4) |
| `intents` | list of IntentProposal | no | fact proposals for the intent door (§6) |

Claim kinds (closed set — additive kinds are a spec edit, never silent):

| Kind | Fields | Asserts |
|---|---|---|
| `state` | `entity`, `prop`, `value` | the projection holds exactly this value |
| `knowledge` | `who`, `knows` | the knower holds this token (channel/fidelity are render details, never claim fields) |
| `event` | `event_id`, `type` (optional) | this event exists, with this type |

IntentProposal fields: `kind`, `actor` (required), `target`, `fields`,
`based_on_event_seq` (INTENT_SCHEMA §2 grammar — the C-parser's target
shape). Every unknown key, wrong type, or missing required key anywhere in
the document is a loud `ProposalError`; the document is closed, not
lenient — that closedness IS the neutralization clause of §2.

## 4. Verdicts (the honest-verdict law, UAP)

Every claim gets one verdict: `supported | contradicted | insufficient_data`.
**Verdicts are always evaluated against current canon** (the full log); the
anchor only participates in attribution (§5). Canon is closed-world:

| Claim | supported | contradicted | insufficient_data |
|---|---|---|---|
| `state` | projection value == claim | value differs (`value_mismatch`; evidence = current value) or entity unknown (`unknown_entity` — an invented entity is a fabricated fact) | prop not modeled on a known entity (`unmodeled_prop`) |
| `knowledge` | the index holds the token (evidence = first source event) | token absent (`token_absent` — the blind-NPC law: no record, cannot know), `who` unknown (`unknown_entity`), or `who` is an item/location (`cannot_know`) | never — the knowledge index is complete and decidable |
| `event` | id found, type matches (if given) | id not in the log (`unknown_event`) or type differs (`event_type_mismatch`, evidence = actual type) | never — the log is the complete event registry |

The honest default: canon never fabricates an opinion it does not hold — a
prop it does not model is `insufficient_data`, NOT a contradiction (UAP
INSUFFICIENT_DATA semantics; never invented evidence). Reasons are a closed
vocabulary (module constant `REASONS`); evidence and causes are structured
values, never prose.

## 5. ExpectedVersion OCC (stale-version rejection)

The document anchor vs the current log length `M = len(events)`:

- **Fresh** (`anchor == M`): verdicts as §4.
- **Stale** (`anchor < M`): the proposal is never accepted on its own terms.
  Every claim is re-validated against current canon; then:
  - any `contradicted` → **refused**. A claim that held at the anchor and
    broke since carries `cause` = the first event after the anchor whose
    application broke it (reason `stale_broken`; the INTENT_SCHEMA §4
    attribution semantics — first break wins), so the refusal note can say
    what moved. Knowledge and event claims are append-only in canon and can
    never flip via staleness — only `state` claims can.
  - all claims hold → **rebased**: verdicts stand against current canon, the
    report records `rebased_to = M`, and intents pass through with their own
    anchors unchanged (the door re-checks — one mechanism, §6).
- **Future** (`anchor > M`): loud `ProposalError` — a proposal referencing a
  version that does not exist is an emitter bug, not world data.

## 6. The fact transaction (proposal → check → commit → narrative)

- `intents` are shaped into `IntentData` (loud `ProposalError` on a kind
  outside the pack's action grammar, unknown fields, missing target —
  reusing `core.intent.validate_shape`, the same loudness law as playscript
  steps) and handed to the intent door with their `based_on_event_seq`
  **unchanged**. The door's own OCC (INTENT_SCHEMA §4) stays the single
  intent enforcement point: stale-and-broken rejects at completion as a
  committed `intent_rejected` fact; stale-and-intact proceeds. The validator
  never pre-merges, never rewrites anchors, never executes.
- Door rejections are committed events (attempts are facts); mediator-side
  refusals (§5, §7) are NOT events — nothing happened in the world, the beat
  just regens. These two refusal families never mix.
- Texture promotion rides the same door (D-049): the committed event IS the
  promotion. The withdrawal mirror (a pending texture Intent whose ledger
  entry retired) is §8's protocol clause.

## 7. The regen protocol (≤2) and the call-budget reconciliation

A refused document (any `contradicted` claim, or a §8 laundering refusal)
triggers the retry protocol, per beat:

- **Regen** = one narrator re-invocation with the refusal note (the
  contradicted claims + reasons + causes, dry structured lines riding the
  next call's directives — D-049). `RegenBudget` caps regens at **2 per
  beat** (architecture, VISION §4; not pack data).
- **Exhaustion → dry mode for the beat** (the L12 floor: template/dry line):
  never a silent drop, never a blocked beat, nothing laundered.
- **Budget reconciliation** (this spec owns it): VISION §4 fixes two numbers
  — "max 2 LLM calls per beat on the critical path" and "≤2 regenerations".
  They bound different quantities. The 2-call law is the **steady state**:
  the narrator plus at most one auxiliary call — the extraction pass, and
  only when the inline delta is absent or malformed. The ≤2-regens law is
  the **retry ceiling**: regens preempt the extraction slot (a regen
  re-delivers the delta; extraction and a regen never share a beat), so the
  worst-case beat is 3 calls (narrator + 2 regens) — the bounded, loud
  exception the steady-state law tolerates. Every regen is counted
  (`regen_count`, §9), never silent; chronic exhaustion is a narrator or
  prompt bug, observable, not absorbed.

## 8. Scene-ledger protocol clauses (mechanism: blueprint §1, D-048/D-049)

The ledger itself is the next iteration's build (`brief/ledger.py` per
TASKS); these are the validation-side clauses this spec owns:

- **One gateway.** Inline deltas and extraction output pass the SAME checks:
  scope, establishment-time canon overlap, laundering (re-asserted
  contradicted/promoted-away values), unique-slot, and the idempotent
  duplicate rule (same (slot, value) in scope = no-op). Refusals use the §7
  protocol verbatim — one refusal shape, one regen budget.
- **Texture-OCC mirror.** A pending texture-referencing Intent whose entry
  retires (contradiction, scene close) is withdrawn by the mediator BEFORE
  the door could complete it — the mediator-side mirror of intent OCC;
  withdrawal is not an event (the attempt never reached the world).
- **Render vs epistemics.** Prose may render NPCs perceiving texture; that
  creates no knowledge records — mechanical load flows only through
  committed events. A prose implication of state change is a claim
  (contradicted → §7), never a ledger job.

## 9. Golden-set plumbing (computed, never LLM-judged)

The golden set is a committed JSON document pinning verdict semantics
against a committed log — the regression harness the narrator boundary and
bg-3 reuse:

```json
{"log": "tests/fixtures/plumbing_smoke_seed42.jsonl",
 "cases": [{"name": "...", "claim": {"kind": "state", "...": "..."},
            "expect": "supported"}]}
```

`load_golden_set` (loud on shape drift) → `run_golden_set(golden, events,
pack)` → per-case expected-vs-computed diff plus summary counts. Every
comparison is computed (dict equality over structured verdicts); no LLM
judges anything, ever. The report carries the harness metrics: `invented`
(contradicted count) and `unverifiable` (insufficient_data count) — bg-3's
invented-facts metric and the §7 `regen_count` ride the same numbers.

## 10. Deferred (just-in-time — writing these early = scope creep)

| Deferred | Arrives with | Owner |
|---|---|---|
| The live narrator call, extraction pass, dry-mode rendering, session wiring | the owner-gated narrator boundary (AGENTS §8) | blueprint §1 |
| The C-parser emitting IntentProposal JSON | phase 2 | blueprint §2 |
| Knowledge-negation claims, fidelity-bearing claims | a real consumer (phase-2 parser disputes) | this spec §3 |
| Semantic invalidation (a spreading fire kills the candlelight) | narrator delta territory or a later validator pass — never mediator guessing | blueprint §1 |
| The scene ledger build (entry shape, lifecycle, pinning, 7th block) | the next track-A iteration | blueprint §1, BRIEF_SPEC §9 |

## 11. Versioning

The validator is a read-side derived artifact (no committed bytes of its
own); the **committed golden fixture** is test data pinning §4 semantics.
A verdict-semantics change = a spec edit + a golden-fixture regen in the
same commit (the BRIEF_SPEC §8 pattern; drift is loud by construction).
