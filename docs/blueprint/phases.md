# blueprint/phases.md — Phases 1–6 Architecture Distillation + Cross-Cutting

> The resolved architecture for everything after the phase-0 gate.
> Architectural depth only — field-level specs are born just-in-time from
> experiments (`SPECS_BACKLOG.md` owns the trigger-gated sketches; this file
> sequences their donors). Entry point + resolution ledger:
> [`docs/BLUEPRINT.md`](../BLUEPRINT.md). Track-B spikes (bg-*) validate
> briefer mechanics on DF Legends XML before phase 1 — they never block
> track A (`ROADMAP.md` §1).

## 1. Phase 1 — mediator & narrator (mode A; track B graduates)

**The block pipeline** (BRIEF-1; `SPECS_BACKLOG.md` BRIEF_SPEC sketch owns
the field-level clauses — sensory emitters, beat-boundary delta,
voice-isolation law). The brief is a sequence of typed blocks with hard
token budgets, assembled fresh every beat (letta block-manager layout;
`VISION.md` §5 "O(relevance), never O(history)"):

1. **Directives** — the narrow mode roles; max 2 LLM calls per beat on the
   critical path (`VISION.md` §4 Layer 3).
2. **Scene delta** — what the PC perceived since the last beat, from
   sensory emitters; size bounded O(perception radius) regardless of log
   length (D-018).
3. **Recalled facts** — top-k over the PC's own knowledge records:
   recency (tick delta) + importance (event `weight`) + relevance — the
   Generative Agents three-signal shape with deterministic inputs
   (tick integer, weight field, cascade-free keyword match). **Dynamic
   facts are never vector-searched** (`TECH_NOTES.md` §6 boundary,
   `VISION.md` §5 `known_by` filter is architectural).
4. **Scheduled static lore** — injection grammar from live-char lorebook
   scheduling: depth / probability / cooldown / sticky / range-cascade;
   recent-facts-first assembly (recency dominates on 12B-class models).
5. **Voice exemplars** — near the context end (position 3–5 messages from
   the end, 100–200 tokens, refresh every 5–10 messages — live-char
   geometry). The brief carries facts as structured tokens and never
   describes style (L2).
6. **Active options** — the available intents as a grammar-constrained
   choice list.

**Eviction contract (BRIEF-1; letta's overflow lesson, deterministic):**
every block carries a soft and a hard token budget (pack data — doubles as
the AP-1 pack-budget lint input). When assembly exceeds a block's hard
budget, blocks are evicted in ascending priority order:
`scheduled-lore → recalled-facts → scene-delta → voice-exemplars →
active-options → directives` — **directives are never dropped**; a freed
slot is replaced by the marker `[truncated:N items dropped]` — silent drops
are forbidden. Reflection-on-recurrence is *periodic compaction between
beats*; eviction is *inside-beat assembly policy* — both exist, they are
different mechanisms and neither substitutes for the other.

**The validator** (VALIDATION_SPEC sketch owns the clauses): fact
transaction proposal → check → commit → narrative, with `ExpectedVersion`
OCC semantics (EventStore) — an Intent references the event version it
was based on; stale proposals are rejected, not merged. Reverse prose
validation with ≤2 regenerations; the prose→proposal boundary is
structural — mode-A prose is never a fact proposal, the C-parser emits
grammar-constrained Intent JSON, no post-hoc text sanitization (D-018 —
the structural injection-neutralization clause).
Honest verdicts default to INSUFFICIENT_DATA, never fabricated (UAP).

**The scene ledger (canon vs texture — D-048; hardened D-049 after an
external design review).** The brief is a pure function of the log, and
the narrator (any model, any temperature) inevitably invents *texture*
— candles, a cloak on a chair, an ajar window — the "free texture at
low importance" `VISION.md` §5 licenses. Unstored, that texture dies at
beat end: the next call re-receives the same canonical brief and the
scene drifts (the player says "blow out the candles" about candles
canon never knew). The fix is a **second stream**: the ledger is a
session-scoped, append-only, mediator-owned record of established
texture — never folded into **canonical** state (it *is* session
render state, named and lifecycle-governed — the atlas admission test:
identity + corrigibility, not sophistication), never committed, never
replayed (the cosmetic-stream doctrine, D-028: a side-channel that
cannot desync canon replay).

- **Determinism quarantine (D-049).** The session runs three named
  streams: (1) the canon log — deterministic, byte-identical replay
  (INV-2); (2) the ledger — append-only session state, deterministic
  **given its inputs** (same (log, ledger, pack) → same brief bytes)
  but auditable, never replayable: its inputs include the narrator, so
  every entry carries `surface` + `source` + `cause`; (3) the
  transcript tail — capped, ephemeral, never a ledger source except
  via the extraction pass. Nondeterminism enters ONLY at the narrator
  call and is captured structurally once, then frozen. "Zero RNG" is a
  claim about function internals (the assembler draws no randomness),
  never about log-relative determinism of the ledger-fed brief. Canon
  replay (T1/T2) never touches the ledger; the ledger's only write
  path into the log is the intent door (player-driven).
- **Scene = PC-location interval (D-049).** A scene is the maximal
  session interval over which the PC's location is constant: opens at
  session start or PC arrival, closes when the canon moves the PC (any
  committed event that changes the PC's location) or the session
  closes. Identity `(location_id, ordinal)` — a revisit is a NEW
  scene (scene-scoped texture starts empty; entity-scoped texture
  survives). Derived by folding the log; zero new event types — scene
  markers are read-side view state, never logged (the log stays free
  of mediator concerns). Scene close retires scene-scoped entries in
  bulk (cause: `scene_close`) — an event-caused recorded decision, not
  a TTL timer (the MTTH lesson holds).
- **Entry shape:** `{id: tex_NNNN, t, scope, slot, value, surface,
  status, cause, source}` — ids allocate in append order (a counter,
  never a hash, INV-2); `scope` is `scene:<location>` or `entity:<id>`,
  FIXED at establishment (scope-as-key, atlas); `slot`+`value` are
  normalized (the fact), `surface` is the verbatim prose that
  introduced it (evidence-before-belief, atlas); `source` cites the
  narration turn. In-scene updates are `retire + establish` pairs in
  one delta — entries are never edited in place (append-only
  discipline).
- **Lifecycle — discrete states, no floats** (trust-state machine,
  atlas): `active` → `pinned` (the structural trigger, below); the
  live states `active`+`pinned` end in `retired` (narrator-declared,
  scene close) | `contradicted` (canon overrode; cause-linked to the
  event) | `promoted` (became canon; cause-linked) — terminal, one-way
  (no un-pinning, no resurrection). Retirement is always an explicit
  recorded decision — no TTL, no turn counters, no decay timers (MTTH
  lesson).
- **Pinning is structural (D-049).** An entry pins when its id or
  slot/noun is referenced by (a) an Intent through the door (the
  texture noun resolution) or (b) the narrator's own structural delta
  (a `refs` list). Free-text player mentions NEVER pin at the mediator
  — zero-LLM capture; at phase 2 the parser turns mentions into
  Intents, which then pin. Un-pinning does not exist: pin holds to a
  terminal state or scene close. The atlas's four hysteresis knobs
  collapse to one.
- **Write path — one call, two jobs, ONE gateway (D-049).** The
  narrator emits prose + a structural texture delta
  (established/retired/refs) in the SAME call; the mediator parses the
  delta deterministically (zero-LLM capture). The prose→ledger
  boundary is structural, the same law as the prose→proposal boundary
  (D-018). Both delta sources — the narrator's inline delta and the
  extraction pass's grammar-constrained output — pass the SAME
  validation gateway (scope check, establishment-time canon check,
  tombstone/laundering check, unique-slot check, duplicate rule): the
  governed write gateway pattern (atlas "already ours"). The duplicate
  rule is idempotent: same (slot, value) in scope = a no-op; same slot
  + different value while active = refused unless the delta retires
  the old entry first. Degradation ladder: structural delta →
  post-hoc extraction pass (LLM-based, best-effort, eats the 2nd call;
  used only when the inline delta is absent or malformed) → dry mode
  (no ledger this beat; prose must not lean on texture — a legal
  steady state, never a failure, L12). Extraction failure is
  continuity loss for a detail, never corruption: the worst case is
  the status quo ante.
- **Read path:** a 7th brief block `scene_texture` (position 3, after
  scene_delta; eviction order between scene_delta and voice_exemplars
  — current-scene continuity outranks lore, below voice/options).
  **The ledger never evicts (D-049):** it only transitions entries;
  ALL boundedness lives in the brief, a windowed view — active+pinned
  entries whose scope matches the current scene or a present entity,
  ranked pinned-first then newest-first, construction-order tie-break,
  capped by block budgets + a max_items ranking cap (D-047 law:
  ranking cap ≠ budget drop; drops render `[truncated:N]`). Budgets
  and caps are pack data (`BRIEF_SPEC.md` §9 deferral). Size
  guarantee: the block is O(current scene), never O(session history).
  The mediator's context = invariant head + brief blocks +
  current-beat transcript tail (capped, ephemeral) — the ledger is
  what survives transcript eviction (letta's fifo adapted; the
  frontend never owns a window, VISION §10).
- **Tombstones ride the brief (D-049).** The block carries contradicted
  entries as short tombstone lines (slot + refuted + cause), scoped to
  the current scene, newest-first, capped (pack data). Prevention (the
  narrator sees what was refuted) + enforcement (the laundering
  refusal) — both exist; prevention is cheap, enforcement is bounded.
  This is the atlas rejected-value tombstone made feed-forward, and
  the negative-evidence discipline for the phase-1 regression set
  (forbidden-assertion cases).
- **Precedence — canon always outranks texture.** Texture occupies
  only slots canon does not model: the gateway checks each
  establishment against current canon state for the scope (slot/prop
  overlap → dropped + flagged, the same refusal shape); on every beat
  the mediator cross-checks active entries against the new canon delta
  and retires overlaps as `contradicted` with a cause link. Both
  checks are STRUCTURAL (slot/prop overlap only) — semantic
  invalidation (a spreading fire killing the candlelight texture) is
  narrator-retirement territory (its own delta) or a validator catch,
  never mediator guessing (semantics in the mediator is the
  INV-4-adjacent hazard). **Laundering refusal** (rejected-value
  tombstone, atlas): a delta re-asserting a contradicted or
  promoted-away value is dropped and flagged; the flag rides the next
  call's directives; the ≤2-regens protocol (regen = one narrator
  re-invocation with the refusal note; exhaustion → dry mode for the
  beat — never a silent drop, never a blocked beat) is owned by
  VALIDATION_SPEC. **Render vs epistemics (D-049):** the narrator may
  render NPCs perceiving shared scene texture (it is the same scene it
  renders for the player) — this creates NO knowledge records;
  mechanical load (relations, suspicion, resources) flows only through
  committed events, and prose implying a state change is a validator
  catch, not a ledger job. When the noticing must matter, the path is
  promotion ("the guard saw the room go dark" is the promoted-event
  shape).
- **Promotion — only through the intent door; grammar/vocabulary split
  (D-037, D-049).** The PACK owns the grammar — which action slots are
  texture-capable (`requires`-level declarations, additive test kinds
  per INTENT_SCHEMA §10); the LEDGER owns the vocabulary — which
  texture nouns are addressable (active entries for the current
  scope). The phase-2 parser's target grammar = pack verbs ∪ active
  texture nouns, so **ghost interactivity is structurally impossible**
  — any noun the narrator established is parseable by construction; a
  noun that is neither canon nor texture gets the disambiguation path
  (uncertainty surfaced, never guessed) or, well-formed but
  world-impossible, an `intent_rejected` no-op (attempts are facts).
  The mediator resolves noun → active entry BEFORE the door (an
  unresolvable noun never becomes an Intent); core stays ledger-blind
  — the Intent carries the resolved slot as data, the simulator
  decides (rolls, preconditions over pack + projection), and the
  committed event IS the promotion: it carries state_changes +
  knowledge records (the object's canon birth), feeds the normal brief
  blocks thereafter, and the entry flips to `promoted` (cause: ev).
  One-way; composes with existing mechanics (a knocked-over candle
  near an oil spot seeds the fire chain through the same hooks as
  drop_break). A failed attempt does NOT kill the texture (the entry
  stays active+pinned). A pending texture Intent whose entry retires
  before completion (contradiction, scene close) is withdrawn by the
  mediator — the ledger-side mirror of intent OCC; protocol clauses
  are VALIDATION_SPEC's. Inter-scope movement of a texture object is
  impossible without promotion (take = Intent = committed event = the
  object becomes canon) — zombie texture cannot arise through legal
  paths; a pack `unique` slot flag makes cross-scope
  re-establishment of the same slot a laundering refusal (pack data,
  INV-3-clean). The ledger never evicts ANY entry (read path) —
  pinned only wins the brief window's ranking.
- **Death:** session close discards the ledger. Cross-session
  continuity is canon + phase-4 reflection/legends, never the ledger
  — texture is never summarized, never consolidated (chained-lossy
  antipattern, atlas; blueprint §4 originals-never-dropped law).
  Conscious trade-off (D-049): persisting unpromoted texture grows
  unbounded uncommitted state toward a second canon — the disease the
  architecture exists to cure; the escape hatch is promotion (texture
  that must survive goes through the door and is canon thereafter;
  phase-4 reflection distills promoted texture — it IS canon — never
  raw texture).
- Mode B (phase 4): the scene manager shares one ledger per scene —
  the chorus reads the same texture block and stays consistent (the
  scenes are the same PC-anchored intervals).

**The harness** (bg-3): prompt shapes from UAP — role persona in the
system prompt, full criteria + thresholds + worked examples embedded,
staged context injection (later blocks receive the *distilled weaknesses*
of earlier blocks, not their full text), per-stage temperature policy
(0.2 extraction / 0.45 analysis / 0.6 synthesis). Free-tier resilience:
chunked sub-requests, pacing, single retry with backoff. Golden-set
comparison against committed chronicles — computed, never LLM-judged.
Cost discipline: Park et al. 2023 + "1,000 People" 2024 + ai-town are
the benchmarks that justify the deterministic-core split (bg-4).

**Degradation ladder** from day one: LLM → template → dry log line (L12).
Local inference only (llama.cpp + GBNF / Outlines; `TECH_NOTES.md` §1);
prefix-cache the invariant prompt head to blunt the prefill cost
(`TECH_NOTES.md` §2).

## 2. Phase 2 — parser (mode C)

Small model (3–8B) + grammar-constrained JSON (`VISION.md` §4 Layer 3 —
no tool use at 12–27B; grammar-constrained JSON only). The target grammar
is the phase-0 Intent union — the 12 actions with their fields — so the
parser is a *classification with slots*, never free-form generation.
Disambiguation: when parse confidence is low, the mediator asks a
disambiguation question or offers buttons — uncertainty is surfaced, not
guessed (exit criterion: ≥90% valid intents; else redo the grammar).
Player input is data, not instruction (`VISION.md` §5) — the parser
produces Intents; the simulator decides outcomes; the only cure for
sycophancy is that the world answers, not the model.

## 3. Phase 3 — director evolution + event grammar + social depth

**The Paradox grammar, adapted** (TIME-1 rides underneath; L10 keeps it
data): trigger predicates as JSON structures over the projection;
`weight_multiplier` shape (`base` + `modifier{add|factor|trigger}`) for
context-sensitive weights; option blocks with per-option availability
gates; `immediate`/`option`/`after` three-phase lifecycle → seed /
choose / apply; on_action-style dispatch (event X fires → content reacts)
with **append-not-overwrite** composition so packs extend without
clobbering. `first_time_only` (Wesnoth) = hook release policy. Scopes
become an explicit context argument (`ctx`) with `every/random/any`
iterator helpers — the cleanest Paradox abstraction, minus the implicit-
`this` footguns. MTTH stays the named anti-pattern: SAMPLED timing only.

**Director refinements** (recorded at phase 0, built here): layered
thresholds (L4D2), `PEAK_CLIMAX` for high-severity hooks, three-axis
anxiety (Alien) — the `unknown` axis becomes measurable as the gap
between actual state (log) and perceived state (knowledge records);
the director may pace against the gap, still never against the player
(L6). Re-plan-on-violation for hook chains (Generative Agents planning
shape, deterministic engine).

**Social depth**: secrets & leverage as first-class fact clusters (P3a;
CK3 `add_hook` — a hook *is an event* with target, type, expiry tick,
cause); arcs & tension shaping (P3c; L4D/Alien pacing layered over the
seeded buffer, never replacing it); **psychological echo** (P3e) — NPC
behavior modifiers derived from own knowledge records + ticks since
learned; the emotional residue is per-NPC valence, never player-adapted
(L6). C:DDA field/smoke mechanics arrive here as content scale; state-
gated epilogue blocks (C:DDA) as director trigger data.

## 4. Phase 4 — knowledge, scene, retrieval, legends

**Memory** (L3 all the way down): reflection-on-recurrence (Generative
Agents) — compaction emits higher-level entries that are themselves log
entries; originals never dropped (INV-1; letta's
`summarize_messages_in_place` is the named anti-pattern).
**Reflection provenance:** every reflection entry carries
`provenance: list[event_id]` linking to the source records it summarizes;
on retrieval, when a query hits a contradiction between a reflection and
one of its sources, the source record outranks the reflection's recency —
the source is always queryable, the reflection is a derived view, never a
replacement. A reflection whose provenance no longer resolves (possible
only in derived stores after offline scavenge — the log itself never drops
originals, INV-1) is flagged `stale` and excluded from retrieval.
**Trait
crystallization** (P3f, LEGEND_SPEC sketch): 3+ related knowledge records
collapse into a discrete belief token; traits are derived state (fold of
subset), expandable back to source records for the brief — memory made
compressible while echo (P3e) makes it felt.

**Retrieval** (STORE-1): SQLite FTS5 keyword search as the zero-dependency
default — `bm25()` ranking with column weights, `NEAR` proximity,
`highlight`/`snippet` for quoted evidence; `rebuild` is the INV-1
mechanism (drop, replay, re-index). sqlite-vec for **static lore only**:
conditionally loaded (probe + fallback), matryoshka slicing if the corpus
grows, pure-Python `cosine_sim()` fallback so the ladder never breaks
(L12). **Deterministic precedence chain for a static-lore query:**
(1) FTS5 BM25 always runs first — zero-dep, always available, never fails;
(2) if the sqlite-vec probe succeeded at startup, vec kNN runs in parallel
— the two candidate sets union and a Python re-ranker scores
`α·recency + β·authority + γ·bm25 + δ·cosine` (coefficients are pack
data, so ranking stays deterministic); (3) if vec is not loaded, FTS5
candidates alone are returned — **never an empty result**; (4) probe
fallback order: `vec → pure-Python cosine scan → FTS5-only`. Hard
boundary unchanged: dynamic world state = SQL + `known_by`, never
vectors.

**Scene manager & mode B** (one NPC per call): the chorus is a queue, not
a convention. **Choricler mode F offline**: DuckDB `read_ndjson_auto()`
over the JSONL log, `LAG/LEAD` per-actor state diffs, parquet rollups,
ATTACH back into SQLite — the offline chronicler pipeline, never in the
runtime import graph (D-012). Offline compaction = scavenge with
tombstones (EventStore); committed logs never edited (INV-5).

## 5. Phase 5 — depth & worldgen

**Ordered generator passes** over the seed (Azgaar pipeline; Red Blob
polygon map pipeline — Voronoi + Lloyd + noise + watershed + biomes):
each pass a focused algorithm with clear inputs/outputs, one file per
system (L9). Geometry discipline: integer coordinates or fixed-point in
the canonical path; floats live in the render layer only (Azgaar's
cross-engine float drift is the named cause; Brogue's fixed-point is the
precedent).

**The LOD ladder** (LOD-1), coherent at every scale: canon log = ground
truth; per-NPC projection = mid LOD; brief cache = top LOD; populations
vs notables below (DF worldgen — history ticks abstractly, counts for
populations, events for notables); ambient crowd entities above
(already seeded in phase 0). Worldgen runs before the PC arrives — the
PC walks into a running world; pre-PC history seeds the director's
initial buffer (DF "history without a player"). Micro-time (ticks) and
macro-time (years) are layered clocks — same authority, two granularities
(L4).

**Factions with goals** (P3b): small-formula dynamics (KeeperRL rebellion
precedent — a ratio and a threshold, not a psychology engine); Neighborly
is the settlement cousin reading. Exit criterion: an emergent chain of
3+ events without the player (`ROADMAP.md` §2). Real-world donors arrive
as data: Natural Earth (LOD ladder shape, `featurecla` closed enum,
semantic versioning) and GeoNames (9-class/684-code enum shape, typed
parent/child relations, alternate names, daily deltas as append-only
discipline) — shapes and metadata only; CC-BY attribution sidecar at
intake; fantasy content from packs, not from real-world toponyms.

## 6. Phase 6 — packs & worldbuilder

**The pack system** (PACK-1 top rung): manifest + module contracts + pack
CI. Growth rungs, all pre-placed at phase 0: per-category file split
(C:DDA, ~111 categories proven); `abstract` + `copy-from` inheritance
(C:DDA / RimWorld `ParentName` / KeeperRL `inherit`) with the cycle
contract: `copy-from` is a **single-parent chain** (no multi-inheritance —
diamonds rejected by design), **cycle detection at load = CI fail naming
the offending id pair**, and `abstract: true` records are template-only —
never instantiated at runtime; cycle detection is a phase-6 design gate on
PACK-1, not an afterthought. Closed enums on every record (GeoNames/NE);
`"_"` inline commentary; localized name sets (one symbol per language,
renderer picks — NE `NAME_<lang>` shape); append-not-overwrite composition
(Paradox on_action); CREDITS sidecar for CC-BY sources.

**Pack lint = CI, not taste** (L1): the UAP teleology gate as deterministic
checks — dead event types (no state delta, no hook), orphan entities,
empty intersection-matrix cells, declared-but-unused templates; thematic
law / pillars / prohibitions as pack metadata enforced by log asserts at
gate review. The live-char AP crosswalk over spine-shaped entity records:
want/need tension with flaw rooted in a cause (AP-9); every flaw ≥1
behavior rule (AP-8); no clone NPCs sharing trigger→action pairs (AP-11 —
the design-time twin of M4 novelty); rule atomicity (AP-15); pack budgets
(AP-1); no contradictory rules (AP-13); **price markers present** on every
socially meaningful behavior. Mode G (worldbuilder) drafts packs offline
through the same CI, never into the engine. Exit criterion: a new T1
reskin without core edits, ≤1 day (`ROADMAP.md` §2).

## 7. Cross-cutting (the questions that span phases)

- **Do we ever need a real ECS?** Not in phases 0–2: the projection with
  entt-shaped sparse+packed storage and view queries (STATE-1) gives the
  ergonomics without the machinery. Revisit only if `perf-1` (10k-tick
  profile) shows view iteration dominating; even then, port shapes
  (smallest-pool-leads views, id+version handles), not a framework (D-012).
  Bevy's parallelism is irrelevant — a fold must be serial to be
  reproducible.
- **The storage ladder** (STORE-1, one table to rule them all): JSONL log
  = truth → SQLite projection = runtime + checkpoint → FTS5 = phase-4
  keyword → sqlite-vec = static-lore vectors (conditional) → DuckDB +
  parquet = offline analytics. Each rung rebuildable; none authoritative;
  the canon path touches only the first two.
- **The determinism contract**: T1 byte-identity holds for the same
  environment (Python version in the header); the RNG fingerprint extends
  it to a cheap invariant check for every test. The four silent breakers,
  each with its named donor counter-example: wall-clock (MTTH), unsorted
  iteration (ai-town), float geometry in canon (Azgaar), unkeyed
  randomness (tracery/ink defaults).
- **The LLM boundary over time**: INV-4 gates track A until phase-0 exit;
  track B exercises briefer/validator/renderer on DF Legends XML in
  parallel (`ROADMAP.md` §1 fork); the switch to our canon happens only
  after the gate. Early integration is the named hazard — a narrator
  masks simulator holes with pretty prose (`TECH_NOTES.md` §5).
- **Scale posture**: phase 0 is one tavern, ~10 entities, 10^3–10^4 ticks;
  every donor discipline above was chosen to hold at 10^6 events (DCSS
  multi-stream at 150k LOC; C:DDA content at 111 categories; FTS5/vec at
  millions of rows). Nothing in the blueprint has a phase-0-only shape
  that must be rewritten later — the shapes are the scalable ones, only
  the constants are small.

---

← Up: [`docs/BLUEPRINT.md`](../BLUEPRINT.md) · previous part:
[`docs/blueprint/phase0.md`](phase0.md).
