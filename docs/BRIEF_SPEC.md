# BRIEF_SPEC.md — Brief Assembly Contract

> Trigger fired at phase-1 start (`docs/SPECS_BACKLOG.md`). Single owner
> of the brief assembler's contract; the donor design lives in
> `docs/blueprint/phases.md` §1 (ledger row BRIEF-1), the mechanics in
> `brief/assembler.py` + `brief/ledger.py` (the scene ledger). Field-level
> clauses are born just-in-time — §9 lists what is deliberately deferred.
> ≤300 lines. No LLM, no network (INV-4; §9).

## 1. What the brief is

The brief is the **mediator's input document**: everything a narrator
may draw on for one beat, as a sequence of typed blocks. It is
**O(relevance), never O(history)** (`VISION.md` §5) — bounded by token
budgets regardless of log length — and assembled fresh every beat from
the log. The brief carries **facts as structured tokens**; it never
*describes* style (L2 — voice lives in the exemplar block, facts stay
dry). `importance` dials creative freedom downstream; the brief itself
never invents, orders by feel, or drops silently. Scope: the
deterministic assembler (iter-8); the purity pair is **(log, ledger)**
since iter-10 (§2/§3.3).

## 2. Determinism & purity (the D-042/D-043/D-044 read-side family)

- `assemble(events, pack, ledger)` is a **pure function of (log, ledger)**
  (the iter-10 widening, D-049): same log + same ledger + same pack →
  **same brief bytes** in any process, any call order, any
  `PYTHONHASHSEED`. `ledger=None` is byte-identical to an empty ledger.
- The ledger is **session render state, never canon** (the D-049
  determinism quarantine): auditable (surface/source/cause per entry),
  never replayable — its inputs include the narrator. Canon replay
  (T1/T2) never touches it; "zero RNG" is assembler-internal only.
- The assembler draws **no randomness at all** (unlike the chronicle's
  cosmetic stream): every block is `sorted()`/construction-order
  iteration over deterministic inputs (INV-2).
- The assembler **writes nothing** (INV-1): it reads events, never
  emits them — a brief pass that emits canon events is the named
  violation.
- Dynamic facts are never vector-searched (`TECH_NOTES.md` §6): the
  recalled-facts block reads the PC's own `knowledge` records
  (`known_by` as an architectural filter, `VISION.md` §5). Static-lore
  retrieval (FTS5) is a phase-4 concern (§9).
- A growing log keeps its brief prefix stable: same prefix → same
  block items for the same beat window (the window moves with the
  log's last tick).

## 3. The block pipeline (seven blocks, fixed order)

Assembled and rendered in this order (BRIEF-1; letta block-manager
layout; voice exemplars near the context end — the live-char
author's-note geometry; scene_texture at position 3 — current-scene
continuity outranks recall, D-049):

| # | Block | Source (iter-8/10) | Item shape |
|---|---|---|---|
| 1 | `directives` | pack `brief.directives` (static lines) | line, verbatim |
| 2 | `scene_delta` | events in the beat window the PC perceived | `[t <t>] <type>: <actor> -> <target>` |
| 3 | `scene_texture` | the session ledger's window (live + tombstones) | `- [t <t>, <status>] (<id>: )<slot> = <value>` / `- [t <t>, refuted] ... (cause: <ev>)` |
| 4 | `recalled_facts` | the PC's `knowledge` records, ranked | `- [t <at>, <channel>, <fidelity>] <knows>` |
| 5 | `scheduled_lore` | pack `brief.lore`, beat-window eligible | lore text, verbatim |
| 6 | `voice_exemplars` | pack `brief.voice_exemplars` (static lines) | line, verbatim |
| 7 | `active_options` | pack `actions.json` intents + fields | `- <intent>(<field>, ...)` |

### 3.1 Directives

Static mode-role lines, verbatim, pack data. Never dropped, never
truncated (§5). These will seed the narrator's system prompt at the
LLM boundary.

### 3.2 Scene delta (the beat-boundary law, D-018)

What the PC perceived **since the last beat** — a delta, never a world
dump; size bounded O(perception) regardless of log length. Exact
clauses:

- Window: events with `t > last_beat_tick` — the largest beat tick ≤
  the log's last event tick (beats = the pack's `urgencies.beat_ticks`
  offsets repeated every `time.ticks_per_day`, excluding a beat at t=0
  — the backward mirror of `core/loop.py` `_next_beat_after`). No beat
  crossed → the window is the whole log (run start).
- Perceived (the blind-NPC law, T3): the PC is the event's actor, OR
  the event carries a knowledge record with `who == player_id`. No
  record → not in the delta.
- Order: **newest first** (recent-facts-first — recency dominates on
  12B-class models, live-char).
- Display names (pack `entities.json`) resolve ids; the line is dry —
  no prose, no embellishment.

### 3.3 Scene texture (the 7th block — the ledger window, D-048/D-049)

The scene ledger (`brief/ledger.py`; mechanism blueprint §1, protocol
VALIDATION_SPEC §8) records established texture — the narrator's
invented details canon never knew. This block is its **windowed
view**: the ledger never evicts, all boundedness lives here.

- **Window law.** Live (`active`+`pinned`) entries whose scope matches the
  current scene: `scene:<loc>` with `loc == the current scene's location
  AND t >= scene.from_tick` (texture from an earlier scene at the same
  location is gone with that scene — a revisit starts empty, even if a
  stale ledger still holds it live), or `entity:<id>` whose entity is
  **present** (positioned at the scene location, or an item carried by a
  present non-item — the carrier closure; the PC is covered by
  construction). Presence is a structural projection read.
- **Ranking.** Pinned first, then newest-first; construction-order
  tie-break (ids allocate in append order — the index is the
  tie-break). Capped by `max_items` — a ranking cap, never a budget
  drop (§3.4's D-047 law: beyond-cap items render nothing, never
  dropped).
- **Tombstones.** `contradicted` entries in the same scope window
  render as short tombstone lines (slot + refuted + the causing
  event), newest-first, capped by `tombstone_max_items`, AFTER the
  live lines (prevention + enforcement both bounded, D-049).
- **Line shapes** (§3 table): raw ids, never display names — the scope
  is an address, not prose; the `surface` (verbatim introducing prose)
  is ledger audit data and NEVER renders (L2).

### 3.4 Recalled facts (the three-signal shape, deterministic inputs)

Top-k over the PC's knowledge records ranked by the Generative Agents
three-signal shape with two deterministic inputs (the relevance signal
arrives with the mediator, §9):

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
  (§5).

### 3.5 Scheduled static lore

Pack lore entries with a **beat-window schedule**: an entry is
eligible when `from_beat <= beats_crossed < to_beat`, where
`beats_crossed` counts beat boundaries ≤ the log's last tick. Order:
pack declaration order.

### 3.6 Voice exemplars (the voice-isolation law, L2)

Static style lines, verbatim, pack data, injected near the context
end — the only place style lives; the other six blocks stay dry.

### 3.7 Active options

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
line `[truncated:N items dropped]`. The marker is metadata, exempt
from the hard-budget check (a marker must always fit — hiding
truncation would be a silent drop).

### 5.2 Whole-block eviction (total overflow)

After per-block assembly, if the total exceeds `brief.total_hard`,
whole blocks are evicted in ascending priority order:

```
scheduled_lore -> recalled_facts -> scene_delta -> scene_texture -> voice_exemplars -> active_options
```

**Directives are never evicted.** An evicted block renders as its
header + `[truncated:N items dropped]` (N = all its items). Eviction
stops as soon as the total fits; if evicting every evictable block
still does not fit, what remains renders anyway (the directives law
outranks the total budget) — the pack lint (§6) exists to make that
state an authoring error, not a runtime gamble.

### 5.3 Eviction vs compaction

Eviction is inside-beat assembly policy; reflection-on-recurrence is
periodic compaction between beats (phase 4) — both exist, neither
substitutes for the other (`phases.md` §1 owns the distinction).

## 6. Pack data (`rules.json::brief`)

One cohesive section — budgets, weights, static text.
`templates.json` stays the tracery grammar (chronicle prose); the
brief's static text is mediator data, not chronicle grammar.

```json
"brief": {
  "total_hard": 700,
  "blocks": {
    "directives":      {"soft": 60, "hard": 80},
    "scene_delta":     {"soft": 150, "hard": 200},
    "scene_texture":   {"soft": 100, "hard": 140},
    "recalled_facts":  {"soft": 180, "hard": 240},
    "scheduled_lore":  {"soft": 90, "hard": 120},
    "voice_exemplars": {"soft": 90, "hard": 120},
    "active_options":  {"soft": 90, "hard": 120}
  },
  "recalled_facts": {"max_items": 12, "recency_weight": 1.0,
                      "importance_weight": 1.0},
  "scene_texture": {"max_items": 8, "tombstone_max_items": 4, "unique_slots": ["hearth"]},
  "directives": ["...", "..."],
  "lore": [{"id": "...", "text": "...", "from_beat": 0, "to_beat": 3}],
  "voice_exemplars": ["..."]
}
```

Load-time lint (fails loudly, `core/pack.py`): the `blocks` key set is
exactly the seven block ids; every budget is a positive int with
`soft <= hard`; `total_hard` a positive int; `directives` a non-empty
list of strings; every `directives` line fits its own hard budget
(never-dropped data must fit by construction); `lore` entries carry
`id` (unique), `text`, `from_beat >= 0 < to_beat` (ints);
`voice_exemplars` a list of strings; `recalled_facts` weights
non-negative numbers, `max_items >= 1`; `scene_texture` caps integers
>= 1, `unique_slots` unique non-empty strings (empty = no globally-
unique slots; iter-11 ships `["hearth"]` — the hearth is one object).
The eviction order (§5.2) is architecture, not balance — it lives in
code, not in the pack.

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
- `brief_from_log(path, pack, schema, ledger=None)` reads a committed
  log and renders its brief — the golden-fixture byte-identity entry
  point; §8 owns the change discipline.

### 7.1 The narrator call document (iter-12, D-055)

The mediator's narrator call = the brief (§7 bytes, unchanged) + one
appended protocol section (block geometry — one blank line separator):

```
## narrator_protocol
anchor: <len(events) at assembly>
regen: <used>/<max>
<note line>            # refusal / withdrawal notes, verbatim, zero or more
```

`anchor` is the OCC anchor a reply's proposal must carry
  (`VALIDATION_SPEC.md` §5); `regen` is the per-beat counter (its §7);
  notes are the dry refusal lines riding the call's top. A pure function
  of (log, ledger, pack) + the protocol state — same inputs → same bytes
  (the D-049 quarantine). The reply document's contract is
  `VALIDATION_SPEC.md` §7.1's.

## 8. Versioning

The brief is a derived read-side artifact (no committed bytes), so
there is no `schema_version` to bump. The **format contract** (§7 line
shapes, §5 marker text) is owned by this spec: a change to rendered
bytes = a spec edit in the same commit as the code change.

## 9. Deferred (just-in-time — writing these early = scope creep)

| Deferred | Arrives with | Owner |
|---|---|---|
| Relevance signal (query keyword match) | the mediator (it owns the query) | BRIEF_SPEC §3.4 |
| Lore scheduling grammar (probability / cooldown / sticky / range-cascade / `exclude_key`) | the mediator (message cadence) | live-char ref; phases.md §1 |
| Precondition-filtered active options | the mediator wiring through the intent door | INTENT_SCHEMA §1 |
| Voice-exemplar refresh cadence (5–10 messages) | the mediator | live-char geometry |
| Presence & entity cards (present entities + pairwise relations + promoted props; the quiet-beat hole) | `st-1` (TASKS backlog) | blueprint §1 |
| Identity-slot tier + per-scope quotas in the scene_texture window ranking | phase 4 (mode B; with per-entity exemplar geometry) | blueprint §1 |
| The call budget (head + brief + tail + thinking + output ≤ MECW target) + the transcript-tail contract | `st-4` (TASKS backlog) | blueprint §1 |
| Knower-parameterized assembly (an actor-NPC brief over its own KnowledgeView) | phase 4 (mode B) | blueprint §1 |
| Static-lore retrieval (FTS5) + trait expansion instead of raw records | phase 4 | STORE-1, LEGEND_SPEC |
| The runtime inference engine (llama.cpp + GBNF local inference, SoW wiring) | the phase-1 gate (`SOW_INTEGRATION_SPEC` trigger, ROADMAP §6; the dev-time narrator is the external agent door, D-055) | AGENTS §8 |
