# BRIEF_SPEC.md — Brief Assembly Contract

> Trigger fired at phase-1 start (`docs/SPECS_BACKLOG.md`). Single owner
> of the brief assembler's contract; the donor design lives in
> `docs/blueprint/phases.md` §1 (ledger row BRIEF-1), the mechanics in
> `brief/assembler.py` + `brief/ledger.py` (the scene ledger). Field-level
> clauses are born just-in-time — §9 lists what is deliberately deferred.
> ≤600 lines, substance-filtered (`AGENTS.md` §6/§6.1; the original ≤300
> self-cap had rotted to 389 by iter-55 — KI#70, the header now reads the
> owning law). No LLM, no network (INV-4; §9).

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

## 3. The block pipeline (eight blocks, fixed order)

Assembled and rendered in this order (BRIEF-1; letta block-manager
layout; voice exemplars near the context end — the live-char
author's-note geometry; scene_texture at position 3 — current-scene
continuity outranks recall, D-049; present_entities at position 4 — the
scene trio completes before recall, st-1):

| # | Block | Source (iter-8/10/15) | Item shape |
|---|---|---|---|
| 1 | `directives` | pack `brief.directives` (static lines) | line, verbatim |
| 2 | `scene_delta` | events in the beat window the PC perceived | `[t <t>] <type>: <actor> -> <target>` |
| 3 | `scene_texture` | the session ledger's window (live + tombstones) | `- [t <t>, <status>] (<id>: )<slot> = <value>` / `- [t <t>, refuted] ... (cause: <ev>)` |
| 4 | `present_entities` | the projection's present set + the pair map + promotions + the pack's scene-line fields (st-1, iter-20; tune-2: the prop-path `card_markers` table) | `- <id> (<display>)[ markers=<m>][ carries=<ids>][ <prop>=<v>]` / `- scene <loc> (<display>) <field>=<v>[...] [<prop>=<v>...]` / `- pair <a> -> <b> <axis>=<v>` |
| 5 | `recalled_facts` | the PC's crystallized beliefs (leg-2, the derived-trait read) + non-family `knowledge` records, ranked | `- belief <token> (t <cross>, sources: <id>, <id>)` / `- [t <at>, <channel>, <fidelity>] <knows>` |
| 6 | `scheduled_lore` | pack `brief.lore`, beat-window eligible | lore text, verbatim |
| 7 | `voice_exemplars` | pack `brief.voice_exemplars` (static lines) | line, verbatim |
| 8 | `active_options` | pack `actions.json` intents + fields | `- <intent>(<field>, ...)` |

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

### 3.4 Present entities (the 8th block — st-1, the entity cards)

The quiet-beat fix: a beat with no PC-perceived events still carries
the structural fact of WHO is present — a read-side fold over the
projection (`core/fold.py::present_in_order`), zero new event types.
Closes quiet-beat presence, cross-NPC consistency (A-fears-B rides
the card, not recall luck), and promoted-prop visibility in one
mechanism (blueprint §1; the write-side twin is INTENT_SCHEMA §7's
per-present expansion).

- **Entity lines**: one dry line per present entity in pack declaration
  order (npcs → ambient → items) — id, display name, then the
  observable surface, all segments omitted when empty: `markers=`
  from the pack's `card_markers` table — prop-path keyed with two row
  kinds (tune-2, D-060): a **threshold row** (`{"prop":
  "status.fear", "min": 30, "marker": "afraid"}`) renders when the
  numeric prop meets the min; a **value row** (`{"prop":
  "crime_status", "value": "suspect", "marker": "suspect"}`)
  renders on string equality — so `relations.suspicion` and
  `crime_status` rows are expressible pack data and the crime
  cascade's standing state reads on the cards (iter-17's finding;
  the marker surface is the closed prop set `status.<axis>` /
  `relations.<axis>` / `crime_status`, lint-checked); `carries=` the
  visibly-carried items (an item carried by a present non-item folds
  into the carrier's segment — it is the carrier's surface, not a
  room fixture; loose items keep their own lines); promoted props as
  bare `prop=value` pairs (the D-054 scan: events whose outcome
  carries a texture reference whose state_changes birth the slot).
  The epistemics split: the CARD is the narrator's read surface for
  standing state; the PC's own perception stays governed by the
  blind-NPC law in scene_delta (§3.2 — `suspicion_changed` rides no
  knowledge record and never enters the delta window by design).
- **Scene line**: the pack's `scene_line_fields` (iter-20, D-057) list
  the location's pack-modeled fields (e.g. `layout`) that render
  canon-from-birth — static architecture needs no promotion to be
  narratable, and the gateway's `canon_slot` check already guards these
  fields against texture (KI#48). Promoted props append after them
  (canon-born scene texture would otherwise vanish from the brief
  post-promotion — the scene_texture window renders live entries only;
  the card law: static surface first, event-born news last). A pack
  that declares no `scene_line_fields` renders the line only when the
  scene location holds promoted props (the pre-iter-20 law).
- **Pair lines**: one line per DIRECTED (holder, other) present pair
  carrying pair-map axes (`pair.<other>.<axis>`), projection order —
  A-fears-B and B-trusts-A are different facts; BOTH parties must be
  present. Capped by `max_pairs`.
- **Caps**: `max_entities`/`max_pairs` are ranking caps (the D-047
  law — beyond-cap items render nothing, never a budget drop); the
  scene line is structural (≤1, never capped).

### 3.5 Recalled facts (the derived-trait read + the three-signal shape)

Top-k over the PC's knowledge read **through the derived-trait lens**
(the phase-4 clause, leg-2; `core/traits.py` owns the fold): the PC's
crystallized beliefs render as **belief lines that lead the block**,
and the family records that minted them render nothing raw — the
belief is the derived view, the source records stay queryable on
demand via the provenance ids (`core/traits.py::expand_trait`, the
expansion law — the source is always queryable, the belief never a
replacement). Size O(traits + records), never O(history); a
below-threshold family still renders raw (no belief, no replacement).
Belief line shape: `- belief <token> (t <cross>, sources: <id>, <id>)`
— `cross` is the threshold crossing (the latest source event's tick),
`sources` the contributing records' event ids in acquisition order
deduped first-seen (an event minting two family records is one
source). Beliefs render in pack declaration order; belief lines count
against `max_items` (the top-k law). No pack data beyond
`rules.json::traits` — the traits block's existence is the gate
(INV-3).

The surviving raw records rank by the Generative Agents three-signal
shape (the relevance signal landed with scene-2 — the mediator owns
the query, §9's deferral closed):

```
score = recency_weight / (1 + current_tick - record.at)
      + importance_weight * rank(record.source_event.importance)
      + relevance_weight * overlap(query, record)
```
- `recency_weight`, `importance_weight`, `relevance_weight`,
  `max_items`: pack data.  `rank`: low=0, medium=1, high=2.
- `overlap(query, record) = |query_words ∩ knows_words| /
  |query_words|` over the word view (`core.retrieval.word_tokens` —
  the ladder's floor semantics, the single owner of the word view;
  rung-independent by construction: the brief's bytes never hinge on
  a SQLite build's FTS5 presence).
- The query is **mode B only**: the knower's fresh-window tokens
  (`brief/scene.py::recall_query` — the knows tokens the beat window
  minted for the knower; leak-free by construction, T3's twin). Mode
  A never queries — the two-signal shape, the committed corpus bytes
  (any `relevance_weight` is inert there; the zero-regen law).
- Tie-break: acquisition order (construction order, INV-2).
- **Dedup by `knows` token**: the best-ranked record per token
  survives — the brief shows what the PC knows, not the learning
  history.
- `max_items` is a **ranking cap** (the top-k of the O(relevance)
  law), not a budget drop — records beyond it never become block
  items, and the `[truncated:N]` marker counts budget drops only
  (§5).

### 3.6 Scheduled static lore

Pack lore entries with a **beat-window schedule**: an entry is
eligible when `from_beat <= beats_crossed < to_beat`, where
`beats_crossed` counts beat boundaries ≤ the log's last tick. Order:
pack declaration order.

### 3.7 Voice exemplars (the voice-isolation law, L2)

Static style lines, verbatim, pack data, injected near the context
end — the only place style lives; the other seven blocks stay dry.

### 3.8 Active options

The pack's action intents as a grammar-constrained choice list —
intent name + declared `fields`, pack order. This is the phase-2
parser's target grammar. **Not precondition-filtered** in iter-8: the
brief lists the vocabulary; the intent door (INTENT_SCHEMA §1) remains
the sole gatekeeper of what is actually possible — a listed option the
world rejects is an `intent_rejected` fact, not a brief bug.

### 3.9 Mode B — the knower parameter (scene-1, iter-60)

The blocks are PC-parameterized by default. `assemble_brief` takes
`knower=None` (mode A — the player; the committed corpus bytes,
byte-identical by construction: an explicit player id renders the same
bytes) or `knower=<npc>` (mode B — one NPC per call, the chorus served
head-first through `brief/scene.py::speaking_queue`). Mode B runs the
SAME pipeline with three parameterized halves and four shared ones:

- **scene_delta** reads the knower's own perception — the blind-NPC
  law (§3.2) parameterized: the knower is the event's actor or holds
  a record born on the event. An event nobody told this knower about
  never renders for it; the empty window after departure is the
  honest answer, never a leak.
- **recalled_facts** reads the knower's own memory — its records and
  its crystallized beliefs (§3.5, the per-knower traits fold). The
  leak surface is closed by construction: the records ARE the
  knower's fold, a held-by-another token can never render.
- **directives** and **voice_exemplars** come from the pack's
  `brief.actors` entry — the actor's role text and voice, never the
  narrator's (mode A's static text stays the block's own; the tables
  are disjoint by lint).
- **Shared, never parameterized**: `scene_texture` (one ledger per
  scene — the chorus reads the same texture block, D-049),
  `present_entities` (the cards are observables, L6 — the room's
  structural answer is the same for every present party),
  `scheduled_lore` (pack-declared shared background), and
  `active_options` (the door's grammar, not the knower's).

The **knower gate**: an id that is neither the player nor a pack NPC
carrying an `actors` entry is a loud `ValueError`, never a wrong
brief — an ambient group holds records but never speaks (the
knower-gate law's sibling); an item or a location is not a knower at
all; the player never carries an `actors` entry (mode A owns its
directives).

The **scene manager** — `brief/scene.py::speaking_queue` — is the
chorus queue law: the present, actors-declared NPCs at the current
scene's location, pack declaration order (INV-2), capped by
`brief.chorus.max_actor_calls` per beat; the NPCs beyond the cap fall
to the L12 template rung (their beats already render through the
chronicle — never a blocked beat). A pack without the `chorus` block
runs mode B off — the queue is empty, every run byte-identical (the
pack's own declaration is the gate, INV-3).

**The session wiring (scene-2 — the drain inside the beat cycle).**
The mediator (`cli/mediator.py`) owns the drain: a beat is the
player's exchange, then the chorus. On the player's ACCEPT the
mediator snapshots `speaking_queue` over the post-action log — **the
beat's own cast, fixed at curtain** (mid-beat arrivals join the NEXT
beat's chorus; the queue is never re-taken mid-beat) — and drains it
head-first, one actor call per queued NPC. Each actor exchange is the
SAME cycle (shape gate → proposal verdicts → texture gateway →
intents through the door → promotions) with its own regen budget (one
budget per narrator exchange — the mode-A law preserved exactly) and
its own **caller gate**: `feedable_intents` keeps a proposal only when
its actor is the call's own caller (a reply proposes its own caller's
actions — mode A's caller is the player, mode B's the actor; the
actor's intents feed the door as actor steps, INTENT_SCHEMA §9). The
drain's guards, all L12 — never a blocked beat, never a silent drop:

- **live presence re-verification** — each emission re-reads presence
  (`brief/scene.py::present_at_scene`): an NPC who left the scene
  mid-drain is skipped (the template rung); a call never goes to an
  NPC standing elsewhere.
- **`narrate dry`** on an actor call skips that actor and advances;
  on the player's call it closes the whole beat (declining the head
  declines the beat — the chorus never starts).
- **a bare `narrate`** (the player's next beat) DROPS a pending drain
  — the unanswered actor calls fall to the template rung (the
  operator moved on).
- an exhausted actor budget drops that actor to the template rung
  with the refusal notes on the result; the drain lives on.

The notes' law is subject-scoped (§7.1): the withdrawal notes minted
by a reply wait for the NEXT PLAYER call — the actor calls never
consume them; an actor's own regen refusals ride its own re-emit.

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
scheduled_lore -> recalled_facts -> scene_delta -> scene_texture -> present_entities -> voice_exemplars -> active_options
```

`present_entities` sits between scene_texture and voice_exemplars
(st-1): canon-projection structure outranks narrator-invented texture
(canon always outranks texture, D-049), below the voice/options
core.

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
  "total_hard": 800,
  "blocks": {
    "directives":      {"soft": 60, "hard": 80},
    "scene_delta":     {"soft": 150, "hard": 200},
    "scene_texture":   {"soft": 100, "hard": 140},
    "present_entities": {"soft": 90, "hard": 120},
    "recalled_facts":  {"soft": 180, "hard": 240},
    "scheduled_lore":  {"soft": 90, "hard": 120},
    "voice_exemplars": {"soft": 90, "hard": 120},
    "active_options":  {"soft": 90, "hard": 120}
  },
  "recalled_facts": {"max_items": 12, "recency_weight": 1.0,
                      "importance_weight": 1.0,
                      "relevance_weight": 1.0},
  "scene_texture": {"max_items": 8, "tombstone_max_items": 4, "unique_slots": ["hearth"]},
  "present_entities": {"max_entities": 8, "max_pairs": 6,
                        "scene_line_fields": ["layout"],
                        "card_markers": [
                          {"prop": "status.intoxication", "min": 30, "marker": "drunk"},
                          {"prop": "status.fatigue", "min": 30, "marker": "weary"},
                          {"prop": "status.fear", "min": 30, "marker": "afraid"},
                          {"prop": "status.injury", "min": 1, "marker": "hurt"},
                          {"prop": "relations.suspicion", "min": 25, "marker": "wary"},
                          {"prop": "crime_status", "value": "suspect", "marker": "suspect"},
                          {"prop": "crime_status", "value": "caught", "marker": "caught"}]},
  "directives": ["...", "..."],
  "lore": [{"id": "...", "text": "...", "from_beat": 0, "to_beat": 3}],
  "voice_exemplars": ["..."],
  "chorus": {"max_actor_calls": 2},
  "actors": {
    "npc_guard_01": {
      "directives": ["...", "..."],
      "voice_exemplars": ["..."],
      "notes": "..."
    }
  }
}
```

Load-time lint (fails loudly, `core/pack.py`): the `blocks` key set is
exactly the eight block ids; every budget is a positive int with
`soft <= hard`; `total_hard` a positive int; `directives` a non-empty
list of strings; every `directives` line fits its own hard budget
(never-dropped data must fit by construction); `lore` entries carry
`id` (unique), `text`, `from_beat >= 0 < to_beat` (ints);
`voice_exemplars` a list of strings; `recalled_facts` weights
non-negative numbers (`recency_weight`, `importance_weight`, and
`relevance_weight` — scene-2's third signal, inert without a query),
`max_items >= 1`; `scene_texture` caps integers
>= 1, `unique_slots` unique non-empty strings (empty = no globally-
unique slots; iter-11 ships `["hearth"]` — the hearth is one object);
`present_entities` caps integers >= 1 and a `card_markers` table
(tune-2, D-060): each row keys `prop` — one of `status.<axis>` (a
declared states axis), `relations.<axis>` (a declared relations axis),
or `crime_status` (the closed marker surface) — with EXACTLY ONE of
`min` (a non-negative int, threshold row) or `value` (a non-empty
string, value row), and a non-empty `marker` string (marker names are
pack vocabulary, INV-3); `scene_line_fields` (iter-20) unique non-empty strings, each
a field of at least one location record (a typo'd field fails at load
time). The mode-B pair (scene-1, §3.9): `chorus` is optional with a
closed key set (`max_actor_calls` an integer >= 1 — a zero cap is a
block-less pack, declare nothing instead; `notes` prose); `actors` is
optional, non-empty, keyed by pack NPC id — never the player (mode A
owns its directives; the tables are disjoint by law) — with a closed
per-actor key set (`directives` a non-empty string list whose total
fits the `directives` hard budget — the same construction-fit law for
never-dropped data; `voice_exemplars` a string list, L2's only home
for the actor's style; `notes` prose). The eviction order (§5.2) is
architecture, not balance — it
lives in code, not in the pack.

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
actor: <id>            # mode B only (scene-1): whose beat-projection
anchor: <len(events) at assembly>
regen: <used>/<max>
query: <keywords>      # mode B, scene-2: the relevance signal's text
retrieval: fact <ref> (<channel>/<fidelity>, <source>)  # the ladder's top rows
retrieval: lore <ref>
<note line>            # refusal / withdrawal notes, verbatim, zero or more
```

`anchor` is the OCC anchor a reply's proposal must carry
  (`VALIDATION_SPEC.md` §5); `regen` is the per-exchange counter (its
  §7 — scene-2: one budget per narrator exchange, the mode-A law
  preserved exactly); notes are the dry refusal lines riding the
  re-invocation. A pure function
  of (log, ledger, pack) + the protocol state — same inputs → same bytes
  (the D-049 quarantine). The reply document's contract is
  `VALIDATION_SPEC.md` §7.1's. **Mode B (scene-1, §3.9): the actor call
  is the same document with `knower=<npc>` — the protocol section's
  first line becomes `actor: <id>` (whose beat-projection the call
  carries — the operator knows whose voice to speak); mode A's bytes
  carry no actor line (the player is the narrator's subject by
  construction — the committed corpus shape, unchanged).**

**Scene-2's protocol lines (mode B only; mode A's bytes carry none of
them):** `query:` — the keyword query that ranked this actor's memory
(§3.5's relevance signal, `brief/scene.py::recall_query` — the
operator sees WHY the records ranked as they did); `retrieval:` — the
retrieval ladder's top rows for that query (`RetrievalIndex.query`,
capped at `RETRIEVAL_LINES = 3` — the ladder's first runtime QUERY
consumer, one index build per actor call, `cli/mediator.py::_emit_actor`):
dry demand handles, no scores, no prose (L2) — the ORDER carries the
ranking (the source-outranks law visible); fact rows carry the
fidelity and the minting event id (the expansion law's handle), lore
rows the lore id. A pack without a `retrieval` block serves no rows
(the ladder is the pack's own declaration, INV-3).

**The notes' subject-scoping (scene-2):** the withdrawal notes minted
by a reply (whose proposals were withdrawn — the caller gate or the
noun resolution) ride the NEXT PLAYER call — the actor calls never
consume them (the operator's beat-level feedback channel); an actor's
own regen refusals ride that actor's re-emit. The committed corpus
pins this law: the withdrawals surface on the player's next call,
unchanged by the chorus in between.

## 8. Versioning

The brief is a derived read-side artifact (no committed bytes), so
there is no `schema_version` to bump. The **format contract** (§7 line
shapes, §5 marker text) is owned by this spec: a change to rendered
bytes = a spec edit in the same commit as the code change.

## 9. Deferred (just-in-time — writing these early = scope creep)

| Deferred | Arrives with | Owner |
|---|---|---|
| Lore scheduling grammar (probability / cooldown / sticky / range-cascade / `exclude_key`) | the mediator (message cadence) | live-char ref; phases.md §1 |
| Precondition-filtered active options | the mediator wiring through the intent door | INTENT_SCHEMA §1 |
| Voice-exemplar refresh cadence (5–10 messages) | the mediator | live-char geometry |
| Identity-slot tier + per-scope quotas in the scene_texture window ranking (the per-entity exemplar half landed with mode B — §3.9 `actors`) | `tex-1` (TASKS backlog — scene-2's row carried the wiring only; the underdeliver law, the remainder re-pointed) | blueprint §1 |
| The call budget (head + brief + tail + thinking + output ≤ MECW target) + the transcript-tail contract | `st-4` (TASKS backlog) | blueprint §1 |
| Knower-parameterized assembly (an actor-NPC brief over its own KnowledgeView) | **landed iter-60** (`assemble_brief(knower=...)` + `brief/scene.py` the chorus queue — §3.9) | blueprint §1 |
| Relevance signal (query keyword match) | **landed iter-61** (scene-2: `assemble_brief(query=...)` the third signal + `recall_query` the derivation + the ladder's first runtime query — §3.5/§7.1) | BRIEF_SPEC §3.5 |
| Static-lore retrieval (FTS5) | **landed iter-59** (`core/retrieval.py`, D-088 — the ladder); **queried by the runtime since iter-61** (the actor calls' `retrieval:` lines — §7.1) | STORE-1 |
| The runtime inference engine (llama.cpp + GBNF local inference, SoW wiring) | the phase-1 gate (`SOW_INTEGRATION_SPEC` trigger, ROADMAP §6; the dev-time narrator is the external agent door, D-055) | AGENTS §8 |
