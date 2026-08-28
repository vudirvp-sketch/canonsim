# BRIEF_SPEC.md — Brief Assembly Contract

> Trigger fired at phase-1 start (`docs/SPECS_BACKLOG.md`). Single owner
> of the brief assembler's contract; the donor design lives in
> `docs/blueprint/phases.md` §1 (ledger row BRIEF-1), the mechanics in
> `brief/assembler.py`. Field-level clauses are born just-in-time — §9
> lists what is deliberately deferred. ≤300 lines. No LLM, no network
> anywhere in this contract (INV-4 holds until the owner-gated
> narrator-boundary iteration, AGENTS §8).

## 1. What the brief is

The brief is the **mediator's input document**: everything a narrator
may draw on for one beat, as a sequence of typed blocks. It is
**O(relevance), never O(history)** (`VISION.md` §5) — bounded by token
budgets regardless of log length — and assembled fresh every beat from
the log. The brief carries **facts as structured tokens**; it never
*describes* style (L2 — voice lives in the exemplar block, facts stay
dry). `importance` dials creative freedom downstream; the brief itself
never invents, orders by feel, or drops silently.

Phase-0-era scope (this spec, iter-8): the **deterministic assembler**
— a pure function of a committed log. The LLM side of the pipeline
(max-2-calls-per-beat mediator, `VISION.md` §4 Layer 3) is a later,
owner-gated iteration.

## 2. Determinism & purity (the D-042/D-043/D-044 read-side family)

- `assemble(events, pack)` is a **pure function of the log**: same log
  + same pack → **same brief bytes** in any process, any call order,
  any `PYTHONHASHSEED`.
- The assembler draws **no randomness at all** (unlike the chronicle's
  cosmetic stream): every block is `sorted()`/construction-order
  iteration over deterministic inputs (INV-2).
- The assembler **writes nothing** (INV-1): it reads events, never
  emits them. A brief pass that emits canon events is the named
  violation.
- Dynamic facts are never vector-searched (`TECH_NOTES.md` §6): the
  recalled-facts block reads the PC's own `knowledge` records
  (`known_by` as an architectural filter, `VISION.md` §5). Static-lore
  retrieval (FTS5) is a phase-4 concern (§9).
- A growing log keeps its brief prefix stable in the same sense as the
  chronicle: same events prefix → same block items for the same beat
  window (the window itself moves with the log's last tick).

## 3. The block pipeline (six blocks, fixed order)

Assembled and rendered in this order (BRIEF-1; letta block-manager
layout; voice exemplars sit near the context end — position 5 of 6,
the live-char author's-note geometry):

| # | Block | Source (iter-8) | Item shape |
|---|---|---|---|
| 1 | `directives` | pack `brief.directives` (static lines) | line, verbatim |
| 2 | `scene_delta` | events in the beat window the PC perceived | `[t <t>] <type>: <actor> -> <target>` |
| 3 | `recalled_facts` | the PC's `knowledge` records, ranked | `- [t <at>, <channel>, <fidelity>] <knows>` |
| 4 | `scheduled_lore` | pack `brief.lore`, beat-window eligible | lore text, verbatim |
| 5 | `voice_exemplars` | pack `brief.voice_exemplars` (static lines) | line, verbatim |
| 6 | `active_options` | pack `actions.json` intents + fields | `- <intent>(<field>, ...)` |

### 3.1 Directives

Static mode-role lines, verbatim, pack data. Never dropped, never
truncated (§5). These will seed the narrator's system prompt at the
LLM boundary; today they are data rendered as text and nothing more.

### 3.2 Scene delta (the beat-boundary law, D-018)

What the PC perceived **since the last beat** — a delta, never a world
dump; size bounded O(perception) regardless of log length. Exact
clauses:

- Window: events with `t > last_beat_tick`, where `last_beat_tick` is
  the largest beat tick ≤ the log's last event tick (beats = the pack's
  `urgencies.beat_ticks` offsets repeated every
  `time.ticks_per_day`, excluding a beat at t=0 — the mirror of the
  loop's forward scheduling, `core/loop.py` `_next_beat_after`). No
  beat crossed → the window is the whole log (run start).
- Perceived (the blind-NPC law, T3): the PC is the event's actor, OR
  the event carries a knowledge record with `who == player_id`. No
  record → not in the delta.
- Order: **newest first** (recent-facts-first — recency dominates on
  12B-class models, live-char).
- Display names (pack `entities.json`) resolve ids; the line is dry —
  no prose, no embellishment.

### 3.3 Recalled facts (the three-signal shape, deterministic inputs)

Top-k over the PC's knowledge records ranked by the Generative Agents
three-signal shape with deterministic inputs:

```
score = recency_weight / (1 + current_tick - record.at)
      + importance_weight * rank(record.source_event.importance)
```

- `recency_weight`, `importance_weight`, `max_items`: pack data.
  `rank`: low=0, medium=1, high=2.
- Tie-break: acquisition order (construction order, INV-2).
- **Dedup by `knows` token**: the best-ranked record per token
  survives — the brief shows what the PC knows, not the learning
  history.
- `max_items` is a **ranking cap** (the top-k of the O(relevance)
  law), not a budget drop — records beyond it never become block
  items, and the `[truncated:N]` marker counts budget drops only
  (§5). The third signal (**relevance**: cascade-free keyword match
  against a query) arrives with the mediator, which owns the query
  (§9). Until then the ranking is the two deterministic signals.

### 3.4 Scheduled static lore

Pack lore entries with a **beat-window schedule**: an entry is
eligible when `from_beat <= beats_crossed < to_beat`, where
`beats_crossed` counts beat boundaries ≤ the log's last tick. Order:
pack declaration order. The full live-char scheduling grammar
(probability / cooldown / sticky / range-cascade / `exclude_key`) is
deferred (§9) — it needs the mediator's message cadence to mean
anything.

### 3.5 Voice exemplars (the voice-isolation law, L2)

Static style lines, verbatim, pack data, injected near the context
end. They are the ONLY place style lives; the other five blocks stay
dry. Refresh cadence (every 5–10 messages) is a mediator concern (§9).

### 3.6 Active options

The pack's action intents as a grammar-constrained choice list —
intent name + declared `fields`, pack order. This is the phase-2
parser's target grammar. **Not precondition-filtered** in iter-8: the
brief lists the vocabulary; the intent door (INTENT_SCHEMA §1) remains
the sole gatekeeper of what is actually possible — a listed option the
world rejects is an `intent_rejected` fact, not a brief bug.

## 4. Token model

- `token_count(text) = len(text.split())` — whitespace tokens. A
  deterministic, dependency-free proxy; the real tokenizer arrives
  with the LLM circuit and **must not** change committed formats
  without a spec bump (§8).
- A block's token count = the sum over its header + body lines + the
  truncation marker (if any). The total = the sum over blocks.

## 5. Budgets & the eviction contract

Every block carries a **soft** and a **hard** token budget (pack
data). Assembly never exceeds a hard budget with content items, and
never drops silently:

### 5.1 Per-block fill law

Items are taken best-first while BOTH hold:

1. `tokens_so_far < soft` — the fill target: once reached, the block
   stops wanting more (the item that crosses the target lands whole;
   items are never cut mid-line);
2. `tokens_so_far + tokens(item) <= hard` — the ceiling: an item that
   would bust the hard budget is skipped even below soft (greedy
   best-fit; a smaller lower-ranked item may still fit).

Every item not taken — soft reached, ceiling skip, or list exhausted —
counts as **dropped**. A block with dropped items ends with the marker
line `[truncated:N items dropped]`. The marker itself is metadata:
exempt from the hard-budget check (a marker must always fit — a
truncated block that hides its truncation would be a silent drop).

### 5.2 Whole-block eviction (total overflow)

After per-block assembly, if the total exceeds `brief.total_hard`,
whole blocks are evicted in ascending priority order:

```
scheduled_lore -> recalled_facts -> scene_delta -> voice_exemplars -> active_options
```

**Directives are never evicted.** An evicted block renders as its
header + `[truncated:N items dropped]` (N = all its items). Eviction
stops as soon as the total fits; if evicting every evictable block
still does not fit, what remains renders anyway (the directives law
outranks the total budget) — the pack lint (§6) exists to make that
state an authoring error, not a runtime gamble.

### 5.3 Eviction vs compaction

Eviction is *inside-beat assembly policy*; reflection-on-recurrence is
*periodic compaction between beats* (phase 4). Both exist; neither
substitutes for the other (phases.md §1).

## 6. Pack data (`rules.json::brief`)

One cohesive section — budgets, ranking weights, and the static text
(directives, lore, exemplars). `templates.json` stays the tracery
grammar (chronicle prose); the brief's static text is mediator data,
not chronicle grammar.

```json
"brief": {
  "total_hard": 700,
  "blocks": {
    "directives":      {"soft": 60, "hard": 80},
    "scene_delta":     {"soft": 150, "hard": 200},
    "recalled_facts":  {"soft": 180, "hard": 240},
    "scheduled_lore":  {"soft": 90, "hard": 120},
    "voice_exemplars": {"soft": 90, "hard": 120},
    "active_options":  {"soft": 90, "hard": 120}
  },
  "recalled_facts": {"max_items": 12, "recency_weight": 1.0,
                      "importance_weight": 1.0},
  "directives": ["...", "..."],
  "lore": [{"id": "...", "text": "...", "from_beat": 0, "to_beat": 3}],
  "voice_exemplars": ["..."]
}
```

Load-time lint (fails loudly, `core/pack.py`): the `blocks` key set is
exactly the six block ids; every budget is a positive int with
`soft <= hard`; `total_hard` a positive int; `directives` a non-empty
list of strings; every `directives` line fits its own hard budget
(never-dropped data must fit by construction); `lore` entries carry
`id` (unique), `text`, `from_beat >= 0 < to_beat` (ints);
`voice_exemplars` a list of strings; `recalled_facts` weights
non-negative numbers, `max_items >= 1`. The eviction order (§5.2) is
architecture, not balance — it lives in code, not in the pack.

## 7. Render format (exact bytes)

```
## <block_id>
<item line>
<item line>
[truncated:N items dropped]

## <block_id>
...
```

- Every block renders its `## <block_id>` header; an empty block is
  the header alone (explicit absence, never omission).
- Blocks are separated by one blank line; the document ends with a
  newline. Line shapes per §3. The arrow in scene-delta lines is `->`
  (ASCII — the brief is machine-facing; the chronicle's `→` is
  prose-facing).
- `brief_from_log(path, pack, schema)` reads a committed log and
  renders its brief — the golden-fixture byte-identity test pins this
  exact format; any format change is a spec change first.

## 8. Versioning

The brief is a derived read-side artifact (no committed bytes), so
there is no `schema_version` to bump. The **format contract** (§7 line
shapes, §5 marker text) is owned by this spec: a change to rendered
bytes = a spec edit in the same commit as the code change. Tests pin
the golden fixture's exact brief — drift is loud.

## 9. Deferred (just-in-time — writing these early = scope creep)

| Deferred | Arrives with | Owner |
|---|---|---|
| Relevance signal (query keyword match) | the mediator (it owns the query) | BRIEF_SPEC §3.3 |
| **Scene-texture block** (`scene_texture`, 7th block, position 3; reads the session scene ledger — assemble becomes a pure function of (log, ledger); same pair → same bytes; entry lifecycle + promotion: `docs/blueprint/phases.md` §1, D-048) | the ledger's LLM-free half may land as track-A code (fixture-shaped deltas); the live writer is the owner-gated narrator boundary | blueprint §1 (the scene ledger) |
| Lore scheduling grammar (probability / cooldown / sticky / range-cascade / `exclude_key`) | the mediator (message cadence) | live-char ref; phases.md §1 |
| Precondition-filtered active options | the mediator wiring through the intent door | INTENT_SCHEMA §1 |
| Voice-exemplar refresh cadence (5–10 messages) | the mediator | live-char geometry |
| Static-lore retrieval (FTS5) + trait expansion instead of raw records | phase 4 | STORE-1, LEGEND_SPEC |
| Any LLM/network call (the narrator itself) | owner-gated boundary iteration | AGENTS §8 |
