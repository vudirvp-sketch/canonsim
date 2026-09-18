# blueprint/phases.md — Phases 1–6 Architecture Distillation + Cross-Cutting

> The resolved architecture for everything after the phase-0 gate.
> Architectural depth only — field-level specs are born just-in-time from
> experiments (`SPECS_BACKLOG.md` owns the trigger-gated sketches; this file
> sequences their donors). Entry point + resolution ledger:
> [`docs/BLUEPRINT.md`](../BLUEPRINT.md). Track-B spikes (bg-*) validate
> briefer mechanics on DF Legends XML before phase 1 — they never block
> track A (`ROADMAP.md` §1).

## 1. Phase 1 — mediator & narrator (mode A) — CLOSED (gate PASS
iter-26, D-058; polish iter-27–29, D-059–D-061)

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

   Flown in flight: the 7th block **scene_texture** (position 3, D-049,
   below) and the 8th **present_entities** (position 4, iter-15/D-056);
   positions/budgets: `docs/BRIEF_SPEC.md` §3.

**Eviction contract (BRIEF-1; letta's overflow lesson, deterministic):**
every block carries a soft and a hard token budget (pack data — doubles as
the AP-1 pack-budget lint input). When assembly exceeds a block's hard
budget, blocks are evicted in ascending priority order:
`scheduled-lore → recalled-facts → scene-delta → scene_texture →
present_entities → voice-exemplars → active-options → directives`
(the two insertions: D-049/D-056; order owner `docs/BRIEF_SPEC.md` §3) —
**directives are never dropped**; a freed
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
  continuity loss for a detail, never corruption.
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
- Mode B (phase 4): one ledger per scene — the chorus reads the same
  texture block (see §4).

**Stress-test resolutions (iter-11b — owner-requested roadmap
stress-test; verdicts pending per-section — presence landed as
D-056, the rest owner-gated).**

- **Identity persistence (the trader problem).** Entity texture
  survives scene change and renders on presence (BRIEF_SPEC §3.3), but
  the ONE `max_items` cap for the whole window makes identity (voice,
  look, mannerisms) compete with fresh scene texture on recency — a
  crowded scene silently evicts exactly what long sessions must keep.
  Read-path resolutions (lifecycle and D-049 untouched): pack
  `identity_slots` rank in a tier with pinned (key: identity-or-pinned
  → pinned → newest → construction); a per-scope quota (at most K
  lines per entity, identity slot first) keeps one chatty entity from
  flooding the window; mode B renders an entity slot
  (`speech_pattern`) in the exemplar geometry per present NPC (pack
  may seed static per-entity exemplars; L2 intact). **The identity
  promotion door**: the D-054 machine with pack grammar widened beyond
  `take` (an `affirm`/introduce family, pack-owned like the texture
  block) — a committed `StateChange(npc, trait.slot, None→value)` +
  knowledge records is an identity trait's canon birth; one door, core
  ledger-blind. Tombstone feed-forward extends to narrator-retired
  PINNED identity entries (prevention; the retire+establish gap stays
  bounded and visible — new candles stay legal). Cross-session
  PC-side identity already survives via knowledge records + P3f; this
  adds the world-side path. (Canon names stay defended — the gateway's
  canon-slot check already refuses pack-modeled fields; epithets are
  the texture path, KI#41.)
- **Presence & entity cards (the quiet-beat hole).** A beat with no
  PC-perceived events carries no structural fact about WHO is present
  — perception emits coarse tokens only (`look_around` →
  `scene_<location>`, `examine` → `details_<target>`); no snapshot
  semantics exist anywhere yet. Resolution: a `present_entities` block
  candidate — one dry line per present entity (id, display name,
  observable surface: status markers, visibly-carried items, promoted
  props) plus pairwise relation tokens for present pairs (O(pairs),
  capped). A read-side fold, zero new event types; closes quiet-beat
  presence, cross-NPC consistency (A-fears-B rides the card, not
  recall luck; AP-11 voice markers get a structural home), and
  promoted-prop visibility in one mechanism. The write-side twin (the
  arrival snapshot) is §5's. **Landed iter-15 (D-056): the 8th brief
  block (BRIEF_SPEC §3.4) + the actor-held per-present-target `knows`
  expansion (INTENT_SCHEMA §7); the scene line carries scene-scoped
  promoted props (post-promotion visibility).**
- **The call budget law (MECW) + the transcript tail.** Local
  27B-class models show a measured effective window (attention
  dilution / context rot) of ~8–16k tokens — the figure's owner is
  TECH_NOTES §2 (which plans @8K); the brief (`total_hard` 700) is
  ~9% of it; VISION §1/§6 encode the thesis. But no spec owns the
  per-call ledger:
  `head + brief + transcript tail + thinking + output ≤ MECW target`
  (pack data per model class; the thinking allowance is 0 for
  non-thinking models). The tail is the shock absorber (evicted
  first, directives never); the head is invariant by construction
  (prefix cache). The transcript-tail contract (what enters: player
  verbatim + narrator prose; cap; eviction) is a named spec item of
  the narrator-boundary iteration — it is the nuance channel: player
  tone and mode-A prose ride the tail to the next call, never the JSON
  (the intent carries the mechanical skeleton; VISION §5
  player-input-is-data holds).
- **Thinking is ephemeral texture.** Hidden CoT / scratchpad lives
  INSIDE the narrator call — GBNF-separated sections (reasoning →
  prose → delta), capped by the call budget, discarded at beat end:
  never in the brief (L2), never in the ledger, never committed
  (INV-1); quarantined at the call like all narrator nondeterminism
  (D-049). Regens inherit the same per-call budget. A brief-resident
  scratchpad would break the purity pair — rejected.
- **Mode B is knower-parameterized assembly.** The blocks are
  PC-parameterized today (recalled facts = the PC's records; scene
  delta = PC perception). An actor-NPC call runs the same pipeline
  over its own knowledge view (`KnowledgeView.records_of(npc)` — the
  machinery exists) plus the entity cards of the other present parties
  (observables only, L6) and its own exemplar geometry. The chorus
  budget is a named phase-4 spec item: the 2-call law is mode A's; a
  mode-B beat with K speaking NPCs is up to K actor calls + extraction
  — a per-beat actor-call cap (pack data) with the L12 template
  fallback beyond it.

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

**The narrator is external at dev-time (D-055, iter-12):** the mediator
emits `output/mediator/call_<N>.md` (brief + narrator_protocol); the
operator — the owner's assistant, outside the codebase — returns ONE
closed reply document with deep shape gates AT the boundary; a refused
document never feeds intents (the beat regens whole). Zero
LLM/network/dependency code — INV-4 held through the whole phase; the
runtime engine is the owner-gated `engine-1` (unlocked at D-058).

## 2. Phase 2 — parser (mode C) — CLOSED (gate PASS iter-35, D-064;
contract owner `docs/PARSER_SPEC.md`)

**Landed half (D-062 — D-055's pattern on the player's free text): the
parser is EXTERNAL at dev-time over a file contract** — `brief/parser.py`
(pure: the grammar snapshot, the call document, the closed reply gate —
off-grammar = loud ParseError, never a feed) + `cli/parser.py`
`ParserDoor` (`say` / `say apply`, one shared ledger; the pin law —
blueprint §1(a)'s first consumer: the reference IS the pin). The target
grammar is PACK data, not a fixed union (INV-3): the pack's verbs with
pack-derived field constraints (the tavern pack ships 13 — a
pack-owned count) ∪ the addressable nouns — canon entities + live
texture entries, ghost interactivity structurally impossible (§1's
promotion clause). A *classification with slots*, never free-form
generation. Attempts are facts: parse validity ≠ world legality;
disambiguation is asked, never guessed (questions live; buttons +
multi-intent = the `parse-2` deferrals, PARSER_SPEC §7). Exit ≥90%
boundary-valid intents: 35/35 on the combined 51-utterance corpus
(iter-32/33) — the gate review is the owner's (the iter-24/26
precedent).

**Runtime half (owner-gated `engine-1`):** small model (3–8B) +
grammar-constrained decoding (llama.cpp + GBNF, `TECH_NOTES.md` §1 —
off-grammar output becomes structurally impossible at the source; the
dev-time boundary gate is its stand-in). Player input is data, not
instruction (`VISION.md` §5); the world answers, not the model.

## 3. Phase 3 — director evolution + event grammar + social depth —
CLOSED (gate PASS iter-54, D-083; opened iter-36 on the owner's call;
the full build column: the pacing stack D-065..D-068, the grammar
D-069/D-070/D-071, the content column D-072..D-082 — every layer and
every declared channel dimension carries a live consumer)

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
**The grammar landed in three layers (drama-1/2/3, iter-40/41/42,
D-069/D-070/D-071): predicates (`core/predicates.py` — the v0.1 leaves
+ compounds + the `prop` leaf) + the weight multiplier + the
`first_time_only` burn; then the option blocks (availability gates +
the deterministic ai_chance-style pick, payload overrides whole-key,
the immediate/option/after lifecycle onto seed/choose/apply); then
the on_action dispatch (a pack table keyed by committed event type,
append-not-overwrite, the witnesses scope + the quantified gate + the
alarm-shaped state change, the one-hop lint). The `any`/`random`
scope helpers stay recorded-not-built (the first-consumer law);
DIRECTOR_SPEC §3/§3a-§3c owns the contracts, the D-069/D-070/D-071
compound row the landing records.**

**Director refinements** (recorded at phase 0, built here): the
pacing clock **landed iter-36** (DIR-1, L4D peak/rest — `RAMP / PEAK /
REST / STAGNATION` over entropy, pack data `director.pacing`,
clock-gated stagnation releases, explicit triggers ungated; owner
`DIRECTOR_SPEC.md` §5); the eventless-stretch instrument **landed
iter-37** (DIR-2, D-066); layered thresholds + `PEAK_CLIMAX` for
high-severity hooks **landed iter-38** (DIR-3, the L4D2 layering +
boss-beat rules, D-067); the multi-channel quiet split **landed
iter-39** (DIR-4, the L4D three-director family — per-channel floors
+ input bindings, D-068). Still ahead: three-axis anxiety (Alien) —
the `unknown` axis becomes measurable as the gap between actual state
(log) and perceived state (knowledge records); the director may pace
against the gap, still never against the player (L6). Re-plan-on-
violation for hook chains (Generative Agents planning shape,
deterministic engine).

**Social depth**: secrets & leverage as first-class fact clusters (P3a;
CK3 `add_hook` — a hook *is an event* with target, type, expiry tick,
cause) **landed iter-44/45 + the coerce driver iter-49, D-073/D-074/
D-078** (the replacement law holds the draw count; the coupling
resolved by **engine-2, iter-50, D-079: the per-entry urgency streams
`urgency:<npc>:<kind>`** — an added/removed entry shifts no check draw
and no other entry's rolls); **arcs & tension shaping (P3c) landed
iter-47 + its driver iter-52, D-076/D-081** (the order law + the gap
law + the entropy mirror; the aftermath chain's gap law
load-bearing); **the ambient driver landed iter-53, D-082** (the
drunkard's ramble — weight 0, the ambient channel's own quiet gate,
seeded on the wait action's hooks, first_time_only; the recurring
variant recorded-not-built); the Alien three-axis unknown-axis is
recorded NOT built — its sketch conflicts with the entropy law's L6
fence, the owner's call to resolve (DIRECTOR_SPEC §11); **psychological echo (P3e) — landed iter-46 (D-075,
social-2): NPC behavior modifiers derived from own knowledge records +
ticks since learned** — `core/echo.py`, a pure read-side fold (per-NPC
valence, linear decay over the pack's `fades_ticks`, fidelity-scaled,
never canon, never an entropy input — L6), consumed by the intent
door's `echo_at_least` gate (the P2b dependency; INTENT_SCHEMA §3 —
the residue drives autonomous behavior and fades with time). The
emotional residue is per-NPC valence, never player-adapted (L6). The live driver landed iter-51 (content-5, D-080 — the guard's
jittery-watcher beat).
C:DDA field/smoke mechanics arrive here as content scale; state-
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

**Legends donor reality (bg-2 measured, `docs/TAXONOMY.md` §4):** DF
history is canon-dense, epistemology-empty — no witness/knowledge
events exist in the exports; DF donates the legends structure
(collections, participants, causality fields), knowledge propagation
has no DF donor and stays ours to design.

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
precedent). **Landed iter-81 as depth-5 (D-115): `core/worldgen.py` the
pass family — `PASS_ORDER` = sites (jittered integer lattice) → relax
(integer-centroid Lloyd) → height/moisture (integer-octave value noise,
fixed-point weights that divide out, normalized into 0..9999) →
watershed (downhill flow, rivers at the threshold) → biomes (the band
table + the coastal refinement) → states (capitals + nearest-capital
growth) → chronicle (pre-PC history); every drawing pass owns one
`worldgen:<pass>` stream (the D-079 family law's fourth member — pass
granularity isolation: re-tuning the map shifts neither a canon check
draw nor another pass's draws); the claims ride `detail_claim` (the
gate's first legal caller — commit/no_op/slot_conflict, canon outranks
the generator); the genesis (world_formed + history events, hooks
seeding the director's buffer, NO knowledge records — the DF
epistemology-empty discipline) commits through the canon door at
`Simulator.open()`; the committed pack UNARMED (the 68a pattern —
zero draws, zero events, v0.1 bytes; the arming is depth-5b). The
chronicle pass's chron-2 form (iter-87, D-121 — the history bridge):
the history events carry the DF legends shape (two distinct region
participants — the run's anchor's draw inherited by its members, the
DF collection's role fields; one site place per event) and the cause
TREE (L7 — a member chains to its nearest lower-tier predecessor, a
top-level event to the previous top-level; the drafts' parent map
resolved through the writer's ids at commit); the war→battle→episode
hierarchy is a PACK-DECLARED collection vocabulary
(`chronicle.collections`, the tiers root-first with the nested member
caps, the kinds ⊆ the closed HISTORY_KINDS — L10, never string
languages); the walk is draw-free (the grouping opportunistic, the
DF-measured minority shape). The
populations/macros half stays depth-7's row; the lazy mid-run
materialization door (a site's passes re-running against a non-empty
log) is the future consumer the claim gate's conflict/no_op verdicts
wait for.**

**The placement discipline (place-1, iter-88/D-122):** the claim↔exits
consistency — a location's claimed site must be topologically
compatible with its exits. The LATTICE is the topology of record
(`core/worldgen.py::lattice_distance`: row-major cells, Chebyshev
steps — a pure function of the site indices + the map config,
computable pre-draw at load time; the drawn sites are the lattice's
jittered, relaxed realization, each bounded in its cell's
neighborhood, so the cell-step distance bounds every realization);
the RELATION is the pack's (`worldgen.place.max_edge_span`, the exits
graph's edge contract — the engine measures, the pack decides; never
engine geography knowledge, INV-3). Every exits edge joining two
claimed locations must read sites within the span — two locations
joined by exits never read sites from opposite corners of the map:
the map↔graph coherence the derived travel prices of st-6a read
(D-116 (5) — an edge-local price needs edge-local sites; authored
packs override per edge, the pack wins). Edges with an unclaimed
endpoint impose nothing (the law is edge-mediated). The vacuity law:
a span at the lattice diameter accepts every pair — dead data,
refused (the single-tier twin law, never a policy ceiling); the
passes never read the `place` block (placement is a load-time law —
the runtime backstop's required set stays six-block).

**The macro-clock primitive (maclock-1, iter-90/D-124):** L4's second
granularity, live — micro-time (ticks) and macro-time (years) are
layered clocks, one authority. The CADENCE is pack-declared
(`rules.json::time.macro`: `cadence_ticks` + `event_type`, closed
vocabulary, linted; absent = the unarmed law — zero crossings, zero
events, the v0.1 bytes untouched, the 68a pattern; the committed
pack's arming rides with the primitive's first consumer). The
crossings are the positive multiples of the cadence — pure tick
arithmetic, never entropy (the depth-3 "scheduler rule" family); the
loop fires them in the crossing discipline, COARSEST CLOCK FIRST at
a co-occurring tick (the year turns before the day's rotation, the
rotation before the beat). The MACRO-YEAR is the macro-clock's
counter — `start + t // cadence`, derived never stored (L3); the
start BINDS to the worldgen chronicle horizon (the genesis years are
the world's history before the run — one timeline, D-116 (4): neither
a global tick↔year constant nor forever-decorative years). Each turn
is ONE event through the canon door (INV-1): actor `world`, cause =
the chronological chain, no knowledge, no state changes, no hooks;
importance rides the pack's own rule (the story-critical listing
decides tale visibility). The AGGREGATE-EVENT EMISSION SURFACE
(`core/macro.py::macro_turn_draft`, the D-112 shape — one event with
cardinality): the consumer's counts ride the outcome as flat integer
keys beside `year`; the consumers — depth-3 (warm ring), depth-7
(group ticks), st-6a (travel), weather-1 (ambient) — land AFTER the
primitive, each calling the surface at the crossing (log growth
O(consumers × macrobeats), never O(members × ticks); the count
vocabulary is theirs, the surface shape-only).

**The scene LOD (depth-3, iter-91/D-125): the three zones, live.**
The partition (`core/lod.py::scene_zones`) is a pure function of the
exits graph + the PC's live position — ACTIVE (the PC's location,
per-beat), WARM (its exits, pack declaration order), COLD (the rest);
recomputed at each tick it scopes, so the zones follow the reader.
The ONE-GATE law: the LOD engages exactly when the macro clock is
armed — the warm cadence IS the macro cadence (one clock, one
cadence, no second pack declaration); the unarmed law is the
one-scene world, the whole simulation per-beat, the v0.1 bytes (the
68a pattern; the committed pack's arming rides with weather-1's row).
At the crossing the warm ring ticks the beat machinery minus the
director (the story layer stays global — pack-authored hooks,
budget-bounded): drift chained after the turn (the consumer rides the
clock's own event), goal rolls at the crossing tick enqueued at the
entry tick — the roll cadence is the LOD's cost, the odds never
change (L13). The cold background rides the turn alone: its NPC
census as one flat count (`cold_npcs`, the D-112 cardinality shape —
counts for populations, events for notables; L3 derived, INV-1
recorded, never stored) — the cold NPCs never tick. Log growth
O(active + warm/cadence + aggregates), the long-history fear bounded
by construction.

**The name generator (name-1, iter-96/D-131 — D-116 (12): the Azgaar
split; condensation's canon-birth events need names, `region_00`-style
ids do not scale to a story):** pack-declared PHONOTACTIC PROFILES,
culture-keyed — `rules.json::names.profiles`, the id the pack's own
vocabulary (the Azgaar nameBase shape: the syllable-component pools
`onsets`/`nuclei`/`codas` — the empty fragment legal in onsets/codas —
plus the `syllables` bounds; the CK3 culture keying and the
id↔display split — `docs/ref/ck3.md` + `docs/ref/azgaar_names.md`).
The npc record declares the origin: `generated_name: <profile>`
(mutually exclusive with an authored `name` — one name origin per
npc; `name` stays the pure string surface every reader already
knows). `core/names.py::materialize_name` — the lazy scene-detail
twin at npc scale (the D-054 law, never a second mechanism): ONE
birth (npc, `name`, None -> drawn) on the npc's own content-addressed
`name:<npc>` stream (the D-079 family law's SIXTH member —
per-declaration isolation: an added or re-armed declaration shifts
neither a canon check draw nor another npc's name; first-commit-wins:
canon never redraws, a re-tuned profile pays only on the unborn).
The OUTPUT-NAMESPACE law: a drawn name never collides with the
entity namespace (every declared entity id) — the bounded collision
walk redraws past colliding candidates, then the loud refusal (the
render's id↔display mapping stays injective; a load-time lint cannot
check a seed-dependent space, the walk is the law's single owner).
The REACHABILITY law (the depth-5b family): a `generated_name`
declaration must ride a condensing group's membership — a declaration
nothing can materialize is dead data, refused by the lint. THE
CONSUMER: depth-7's condensation — the event carries each member's
name birth PAIRED with the membership birth (one member, one block;
a runtime-joined member still gets the name it never had), the
outcome's `names` key the flat template surface (present only when
something materialized, the drifted_from law; the line must BRANCH —
`{names?...|...}` — a bare `{names}` on a nameless condensation is
an unknown slot). The tier half stays draw-free; the unborn
population stays counts — the lazy-depth law: unnamed until the
reader's zone warms (the phases §6 "inn's strangers ARE the
condensation" shape). The READ surface is fold-first (canon
outranks the pack record) on EVERY id-valued reference (iter-96a/
KI#84): the chronicle's running name fold (the derived actor/
target slots AND the outcome payload's ids — the rotation's
incoming/outgoing), the scene card + entity views over the
projection (the `carrier:` line included), the brief's delta
lines + entity cards; an unborn generated name renders honestly as
its dry id. The committed pack UNARMED (the 68a pattern — zero
draws, the v0.1 bytes by construction; the arming rides with
world-2's cultures row, the phase-6 consumer — the province's two
tongues, its own name dogfooding the profiles).

**The travel price law (st-6a, iter-97/D-132 — travel as a separate
action, never a weighted move):** the travel action is the movement
TWIN with an edge price — `ticks: "edge"` (the action vocabulary's
fourth value, movement-resolver-only by lint; the registry law held:
no new resolver, the edge-priced DURATION is the new mechanic; move's
semantics, `adjacent_to`, and the T1 golden fixtures untouched). The
ACCEPT DOOR prices at resolve time (`core/travel.py::travel_ticks`,
the loop's branch): the completion rides the queue at `t + price`
(L3 derive-never-store; day-scale durations queue-cheap, MVP_SCOPE
§8 — the clock jumps ahead), and the crossings fire MID-TRAVEL in
tick order (D-038 — the beats/rotations/macro turns the queue pops
between accept and completion). THE PRICE: the pack override wins
per edge (`travel.edges`, one entry per undirected REAL exits edge);
else the DERIVED integer function of the WorldModel — lattice cell
steps * `step_ticks` + the height-band spread * `climb_ticks` +
river endpoints * `river_ticks`, the MIN cross-pair read (the road
takes the closest approach; place-1 bounds every cross-pair for
correctness, the price reads the cheapest for cost) — integer
add/multiply only, NO runtime division (bands, never raw-height
ratios — the pack's `height_bands` is the same vocabulary the biome
pass reads), draw-free (a pure function of pack data + the
genesis-frozen model; the fingerprint never sees a price). place-1's
claim↔exits consistency is what makes derived prices meaningful: an
edge-local price needs edge-local sites — both endpoints claimed or
an override, and the COVERAGE lint (with the verb declared, EVERY
exits edge priceable — the travel verb never hard-fails mid-run).
The committed pack UNARMED (the 68a pattern — the arming rides with
world-2's province row; the v0.1 world's every edge is one lattice
step). The macro consumer half (edge-state aggregate macro-events,
road-traffic counts) is the space pack's own future row — D-116's
"the space-pack return", the cadence owner (`core/macro.py`) already
landed.

**The ambient weather family (weather-1, iter-98/D-133 — TASKS'
"ambient weather + canon erosion"; D-116 (7): an ambient family over
the existing doors, no physics engine):** the family rides the MACRO
CLOCK'S cadence — at each crossing, AFTER the turn, the weather CHAIN
rolls its next state and a CHANGE commits ONE event chained to the
turn (the drift's precedent: the consumer rides the clock's own
event); a roll that lands on the current state suppresses the event
(KI#13's no-op discipline) while still advancing the stream. THE
CHAIN is pack data — `rules.json::weather` (the closed vocabulary:
`event_type` + `initial` + `states`, each state's per-state WEIGHTS —
a Markov chain in data, self-weights keep weather sticky; NO TTL, no
turn counters, no decay timers, D-049's fence; the reachability law:
every state reachable from `initial`, the vacuity family). THE
STREAM: `weather:chain` — the D-079 family law's SEVENTH member,
SINGLETON (the world's one weather; arming or re-tuning shifts
neither a canon check draw nor any other family's rolls, the
substantive fingerprint never sees a weather roll). THE STATE IS THE
FOLD (L3): the current weather = the last weather event's outcome
key, the pack's `initial` before the first; the event carries no
knowledge (the ambient law — a world event, the macro turn's shape)
and no state_changes. THE SEEDED CONSEQUENCES (TIME-1): the change
event carries the new state's hook tags — the director's buffer seeds
them at commit through the existing door (D-005); the storm's murmur
rides the ambient channel's quiet gate (the D-082 pattern verbatim:
weight 0, first_time_only). THE EROSION (the fire follow-ups' shape):
promoted canon objects erode via `state_changes` in SEEDED
follow-ups — the change event seeds one queue entry per pack-declared
rule at the crossing + `after_ticks`; the entry's commit scans the
fold for entities holding the rule's `from` value on the target
`prop` (the transition layers' follow-up flags — the closure law) and
emits ONE event per eroded entity (an explicit counter-event, the
legal revert of a held flag, EVENT_SCHEMA §4; idempotent on state —
KI#13). The never-regress law: a crossing that fires LATE (a batch
before a far entry) seeds its follow-ups no earlier than the world's
resumed tick — the deferral bends, the order never breaks. THE
COMMITTED ARMING (the primitive's first consumer): `time.macro` at
the year-scale cadence 518400 (360 days × 1440 — the calendar binding
continuing the genesis horizon, one year per crossing) + the weather
block (clear/overcast/rain/storm; rain's wash reverts the fire
layer's smoke; the storm's drunk-murmur hook) + the three template
lines. The crossings sit beyond every corpus script's horizon by
construction: the T1 golden + day1_theft byte-identical, the corpus
price the LOD's ONE-GATE engagement alone (depth-3's designed price,
paid at the arming — the warm ring's beat events wait for crossings
no day-scale run reaches: day1_full's status_decayed/urgency-scan
counts drop, the day1-family pins re-measured; the weather block
itself adds zero corpus events).

**The spatial model (D-116, the generator-concept verdict — phase
law):** no native 3D — integer-only geometry and the event-simulator
nature forbid it (heavy determinants, the int64/long-arith risk, the
wrong corpus weight); space needs no voxels, it needs movement
between significant nodes. The world is a **graph of scales** (sector
→ system → surface → interior): a scale transition is a change of the
ACTIVE GRAPH, never physical nesting — locations are vertices with
`exits` (the v0.1 shape); the `in`-relation + transitive closure are
st-5 / D-112 §7. **Attributive Z**: `orbit_depth` / `z_layer` /
`elevation_band` / `deck_level` are entity-or-edge state values (pack
payload on `state_changes`, EVENT_SCHEMA §4) — vertical edges
(`stairs` / `hatch` / `airlock` — pack vocabulary) instead of
geometry; "the ship above the target" is a checks modifier, never
geometry. **Layered maps** = Z-levels joined by edges (each layer 2D
or graph). **Topology: bounded plane of record** — the passes'
contract (border sinks in the watershed, the coastal refinement at
the border — the edge rules explicit); sphere breaks integer-only
and the lattice; torus is integer-friendly but changes neighbor
semantics everywhere — both return only via a D-row on measured
need. Void filtering (a space map's empty cells) is a pack-CI
sanitizer (phase 6), never a core pass.

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
is the settlement cousin reading. **Landed iter-92 as depth-6 (D-126):
`core/factions.py` the formula family — the affected fraction of the
membership (per-cent, floored) against the pack-declared threshold,
ramping to `max_per_beat` (the deadband at-or-below the bar; the
probability form is churn-free by construction — no state flips, no
hysteresis owed); the faction is a GROUP ENTITY (`entities.json::groups`,
D-112's one id: actor = the entity id through the SAME intent door,
positioned by its ANCHOR, never a scene body) whose members are the
pack's static initial condition; the goal rolls on the entry's own
`faction:<group>:<kind>` stream (the D-079 family's fifth member) at the
beats and the macro crossings — the scene-LOD scoping by the anchor
(depth-3's one-gate law); the committed pack unarmed (the 68a pattern —
the arming rides with a content row; the runtime `member_of` state door
and the condensation law are depth-7's).** Exit criterion: an emergent
chain of 3+ events without the player (`ROADMAP.md` §2). Real-world donors (Natural Earth / GeoNames) arrive as data — shapes
and metadata only, per `docs/ref/natural_earth.md` +
`docs/ref/geonames.md`; CC-BY sidecar at intake; fantasy content from
packs, never real-world toponyms.

**Groups & simulation LOD (stress-test resolutions, iter-11b;
RATIFIED iter-79 — D-112, in the D-056-amended edition below).**
The LOD ladder above is a READ ladder; the write
side — how off-screen life ticks, how a group becomes an actor, how it
materializes on crossing — was undesigned. Resolutions, zero new
machinery families: (1) **one id, all tiers** — a group is a pack
entity (kind `group`; the event vocabulary is pack data, EVENT_SCHEMA
§11) acting through the SAME intent door (actor = entity id; urgencies
and director releases already ride it, D-037/D-039); `member_of` is a
pair-relation state (D-020); group axes are small-formula data
(KeeperRL ratio+threshold; D-006 holds — no group reputation, axes are
per-entity data). (2) **Simulation LOD = O(relevance) in the tick
loop** — the brief law generalized: notables tick per-beat as today;
groups/regions tick on macro-clocks (L4 layered clocks) emitting ONE
aggregate event with cardinality (`band_raid {caravans: 3, losses: 1}`)
— log growth O(groups × macrobeats), never O(members × ticks);
off-screen rumor cost rides the same cadence. (3) **Condensation on
crossing** (DF populations→notables): group region ∩ PC presence →
members get canon-birth events (the D-054 shape at group scale); the
aggregate is tombstoned as realized in derived stores only (INV-5
untouched); the id never changes between tiers — `known_by`, entity
texture, and old knowledge keys survive without migration. (4)
**Arrival snapshot** (write side, ratified in the D-056-landed form):
entering a scene feeds knowledge per present target through the move
event's own templates (INTENT_SCHEMA §7 — the template half landed
iter-15, D-056; KI#43's grammar correction made a separate perception
event an implementation detail the pack does not need) → O(present)
knowledge records with observable markers (the actor-held `knows`
template expanded per present target — the audience stays `actor`;
additive per INTENT_SCHEMA §7/§10); the read-side twin is the §1
entity-card block. Spec home when its trigger fires: the GROUP_SPEC
sketch (`SPECS_BACKLOG.md`). **Landed iter-93 as depth-7 (D-127 —
after depth-6's one-id actor, iter-92): `core/groups.py` the
write-side LOD's single owner. The `member_of` door (D-020's
pair-relation): the projection seeds NOTHING (absence IS None, the
D-054 slot shape) — the condensation births it, the fold validates
every join/leave/transfer; the depth-6 walk keeps its static-list
read (the iter-92 law). The population tier: one aggregate event per
cold group per macro crossing (actor = the group id, the unborn
population's count under `population`, draw-free — the cardinality
the engine can honestly derive; domain counts like the `band_raid`
example ride future pack grammar, never engine arithmetic). The
condensation on crossing the warm transition (warm ring ∪ active
scene, detected at the zone recomputations — beats AND crossings,
the load state the origin): ONE event per group with the un-born
members' births (the D-054 shape: already-holders skipped) plus the
write-once tombstone marker (`condensed`), after which the
macro-ticks stay silent (the derived store, INV-5). Per-group opt-in
(the 68a pattern): the record's `macro_event`/`condense_event`
(template-closure linted, memberless refused — dead data); the
runtime join/leave pack grammar stays st-3's own row.**

**Research intake 2 (iter-66a, D-096): the depth-phase design material
— recorded here, drafted into TASKS only at the phase-5 opening.**

- **Lazy detail materialization.** A scene's unobserved detail is
  generated deterministically from a content-addressed stream
  `scene:<id>:detail` (the D-079 family law: lazy registration,
  injective name, add-safety) on first meaningful observation;
  re-observation reproduces the same detail. The significant action is
  a MATERIALIZATION EVENT validated against the committed world — the
  D-054 texture-promotion law at scene scale: first-commit-wins, the
  loser rejected with the cause chain (the ledger's texture-OCC
  mirror, `slot_conflict`), a slot already described empty rejects the
  later gold. Never a second mechanism beside the ledger/promotion
  door.
- **Scene LOD (three zones).** GROUP_SPEC owns the group macro-tick;
  scenes get the same discipline: the active scene ticks per-beat, the
  warm ring (adjacent scenes) ticks every Nth beat (a scheduler rule —
  INV-2 clean, never entropy), the cold background rides aggregate
  events only. Log growth stays O(active + warm/N + aggregates) — the
  long-history fear bounded by construction. **Landed iter-91 as
  depth-3 (D-125): the zones read the macro clock's own cadence (one
  gate, no second declaration), the cold background's ride is the
  turn's census count — `core/lod.py` + the §5 paragraph above.**
- **Perception depth — the acquisition side.** The intake's "knowledge
  is binary by presence" premise is FALSE today (channels
  saw/heard/told/inferred, birth fidelity exact/partial/vague,
  `position_visibility` hearing vague-only to adjacent locations,
  perception checks with status modifiers + smoke_penalty — live since
  iter-3). The real gap: continuous acquisition CONDITIONS (light,
  noise, distance, obstruction) feeding birth fidelity — pack data in
  rules.json, mechanics in the perception path/knowledge templates,
  never a second knowledge store; rumordrift (68a/68b) gains its
  distorting medium here. **The acquisition gate landed iter-73 as
  depth-1 (D-105): mechanics only, the committed pack unarmed — the
  arming (rules.json `position_visibility.acquisition`) is depth-1b.**
  Any future threshold-crossing surface carries pack-declared margins
  (a deadband — boundary churn is a number, never entropy; intake-4's
  addition). Distance/obstruction condition kinds wait on world state
  that can express them (doors, sight-lines — the depth-5 layer).
- **Fold checkpoints.** The live projection and KnowledgeView are
  incremental — full refold pays only on replay/branch, the phase-5
  long-history cost. A snapshot is a DERIVED artifact (the SQLite-index
  law, INV-5): fold-checkpoint + event-index offset, grown from the
  chronicler family (iter-64's LAG/LEAD state diffs); rollback =
  snapshot + tail replay. Never truth, never committed, never edited.
  The checkpoint's derived-index record carries the snapshot's sha256
  (byte-deterministic serialization, the `stable_hash` family's
  hashlib; verified by re-fold) — the integrity anchor lives in the
  index, never an event in the truth (intake-4's addition; the resume
  door stays owner-gated, §7). **Landed iter-80 as depth-4 (D-114):
  `core/checkpoint.py` the mechanism (canonical bytes, the anchor,
  verify/verify_all, restore) + `scripts/checkpoint.py` the
  chronicler-family builder + the prefix digest (the append-stable
  log-prefix identity, sha256 over the first 1+offset lines); the
  projection is the checkpointed surface, the KnowledgeView rides the
  read-side-indexes row at the mediator iteration (§7 below) — no
  consumer before then.**

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

**The 2nd-setting design material** (intake-8, D-130 — the owner's
2026-09-11 setting-direction call routed just-in-time for the phase-6
opening, the D-096 precedent; the sketch rides world-2's two-level gate,
res-1, roads-1, PACK_SPEC — never new machinery):

The posture — three tiers, one direction. The repo's public 2nd setting
is ORIGINAL (the sketch below; D-015 + REFERENCES §10: proprietary
universes are pattern rows, never committed content). The level-1 T1
reskin instrument is the OPEN generic stack (SRD 5.1 / Open5e, the §13
starter table; CREDITS sidecar; speed over distinctiveness — the ≤1-day
gate's own shape). A proprietary-universe fan-pack is owner-LOCAL data
outside the repo (the convenience-copy law family): mechanically
possible — a pack is data, INV-3 — but it buys the narrator flavor that
mode A already renders from pillar tokens; zero repo footprint, low
priority by verdict.

The sketch — a poor frontier province on a river trade artery, authored
pillars over a generated surface (the Qud split; the current v0.1 pack —
tavern/street/backyard/guardroom/market — is the seed settlement the
province grows around, the polygon's continuity):

- **Scale**: 3–6 settlements on the travel lattice, a 200–600-site map
  (the geo-1-measured cost — sub-second genesis); roads-1's generated
  exits; place-1's claim↔exits consistency over the settlements' grounds.
- **The artery**: the river road, the trade spine — st-6a's derived
  travel prices make geography MECHANICAL (distance → convoy cost →
  scarcity), never decorative; news rides the road (rumordrift, landed —
  fidelity decays with distance).
- **The focal resource** (the Dune shape, res-1's declaration): ONE
  binding scarcity — hill-smelted iron on the river — tying the market
  town's wealth, the garrison's supply, the old families' claim; the X4
  cascade when it narrows (convoy loss → price shock → crime-pattern
  shift — the Kenshi desperation economy over the landed theft/arson
  families; the Pathologic register: the closed cycle is the story
  engine, not bookkeeping).
- **The triangle** (FNV shape, depth-6): trade guild / old families /
  garrison — three ratio+threshold dynamics over members' live axes;
  the player tips ratios, never script gates (the emergent "many roads").
- **The cultures** (the Morrowind lesson: estrangement is data — naming,
  customs, prohibitions): lowland traders vs hill folk; two name-1
  phonotactic profiles, two custom vocabularies, two prohibition sets
  (the guild's shelter law, the hills' wergeld memory — the WH40k
  grammar); the province's own name minted from the profiles it declares
  (dogfooding name-1).
- **The history** (chron-2): the feud backstory as the cause TREE —
  whose quarrel burned the old mill; the `world_history` template +
  the story-critical claims seed the director's buffer (depth-5b's
  listing).
- **The population** (depth-7): road traffic as cold aggregates
  (population counts on the macro crossings), condensing into named
  travelers when the reader's zone warms — the inn's strangers ARE the
  condensation; the unborn stay counts until approached (lazy depth,
  VISION §3).
- **The calendar** (maclock-1): market days, the fair, the river's
  seasonal rise — cadence pack-declared; the seasons ride weather-1's
  satisfied gate.
- **The tone** (D-030): mid-grim asymmetric data — trust builds slow,
  breaks fast; losses irreversible; the darkness dial pack-declared,
  never a tone lock (the WH40k minus).
- **Magic**: absent BY DESIGN at province scale (the core admission
  test, VISION §5); a low-magic layer is future pack data with zero
  engine change (INV-3's substance) — the slot is left empty on purpose.

The minus ledger (the catalogued minuses → the standing laws that
already cure them; the pack design consults this, never builds around
it): canonless drift (AI Dungeon) → INV-1/INV-5; incident theater (the
RimWorld storyteller) → D-005 (pressure from scarcity + factions, never
scripted incidents); static lore (TES, the museum world) → bridge-1
(claims are event-born, state = fold(log)); knowledge metagates (Outer
Wilds) → L6; mono-resource flattening (Dune) → res-1's closed cycle
(one focal point + ordinary flows + sinks); tone lock (WH40k) → the
D-030 dial; unreadable depth (DF Legends) → the renderer is first-class
(mode A/F, the brief's O(relevance), the story-critical listing); fake
causality → the cause TREE + closed event vocabularies; generic mush
(the reskin risk) → estrangement-as-data (prohibitions + phonotactics +
custom vocabulary); the player-centered world → the cold tiers + macro
aggregates (the phase-5 exit criterion's own shape).

The cost & consequence laws (intake-9, D-134 — the owner's 2026-09-12
cross-media analysis routed; the document's three declared contradictions
resolved as PACK LAWS, zero engine change; a future pack consults these
before inventing its own consequence shapes — the same consult posture as
the minus ledger above):

- **The cost law** (death/maiming — the Soul-Scars-vs-Hades conflict):
  mechanics own the cost, narration owns the meaning. A consequence is
  diegetic state (flags, claims, relations, knowledge records);
  recovery is an explicit costed counter-event (the D-133 legal revert,
  the weather-1 erosion family's own shape); never stat-debt math (the
  cumulative-debt minus), never a price the optimizer pre-builds into
  the sheet (the power-tax minus). The skill-gap minus is the
  director's own job (the weight_multiplier + per-NPC targeting —
  pressure adapts to the party); the narrative half (the scar as
  story) rides the reflection folds + the tone dial. Punishment and
  romanticization stop competing because they own different layers.
- **The failure law** (fail-forward): standing law named for pack
  designers — a failed action must change the world's answer, never
  repeat the question (the KI#13 no-op discipline + the door-reject
  state writes: failure is canon). The d20 host conflict is void:
  checks are state-coupled door tests, not naked dice.
- **The corruption law** (any power-with-a-price family): hard
  pack-declared thresholds (lint-tested — the depth-6 law, Sekiro's
  predictability), diegetic per-NPC consequences (specific relations
  flip, specific NPCs refuse — the player sees consequences rendered,
  never a scale: the thermometer minus), the table's softness kept as
  pack data (the D-030 dial — per-table reproducible, never GM
  discretion at runtime).
- **The decay-branch law** (B4 / Darkest Dungeon): any degradation or
  affliction family branches on the NPC's live axes (the player's
  pattern of falls chooses the branch), never a linear depth-tied
  track.
- **The flashback law** (Blades in the Dark): retroactive facts are
  NEW events through the validation door (consistency-gated — the
  fact transaction + ExpectedVersion re-checks), never history edits
  (INV-5 held); a pack wanting heist fiction costs them against a
  stress-like resource (the leverage/expiry shape).
- **The ambient law** (RotF/Auril): ambient pressure (weather,
  seasons) never carries personal drama — it seeds human consequences
  (the D-082 pattern: the storm seeds the murmur); the antagonist is
  the triangle, the sky is context (weather-1's canon-but-not-tale
  design, promoted to law).
- **Parked pack patterns** (owner-gated, zero engine change — named
  here so a future row finds them): the loop pack (Majora — the macro
  clock re-fires its cadence, knowledge survives in `known_by` (L6:
  knowledge is state, never a gate), world resets via counter-events);
  the low-magic layer with its three lessons (magic as scarcity, never
  infrastructure; mishaps as state-coupled seeds (D-082), never a
  class tax; defiling as a res-1 sink — power's price is scarcity
  somewhere); the soul-scar pattern riding any future combat-bearing
  pack (combat outside every planned phase); belief-as-rules (the
  phase-6 culture rows' per-NPC half — AP-8 behavior rules +
  prohibitions, the Disco Elysium shape).

The encounter & event-generation pattern catalog (intake-10, D-135 —
the owner's 2026-09-12 encounter-design notes routed; the same consult
posture as the minus ledger and the cost laws: a future pack reads this
before authoring encounter families — the patterns are pack data +
read-side surfaces over landed primitives, zero new machinery):

- **The substrate mapping** (the source's 23 patterns collapse into
  eight families, each with a landed owner): *identity & recurrence*
  (the same NPC met twice, escalating recognition) = INV-1's
  persistent ids + the D-112 (3) tier law (the id never changes —
  `known_by`, texture, old knowledge survive condensation) + the
  echo/traits/reflection ladder (felt / believed / concluded — the
  escalating-dialogue gates ride the intent door); *memory-debt*
  (itemized per-NPC entries, never one relationship number) = the
  knowledge records themselves (token / fidelity / channel /
  acquisition) + the pair axes — the source argues itself to the
  landed shape; *residue & promotion* (smoke → scar → "the known
  thief") = `state_changes` + texture + the D-133 erosion (reversal
  as an explicit counter-event) + the trait/reflection promotions;
  *collision & combination* (rain + open fire; drunk + narrow pass +
  cargo) = the on_action table + the erosion family + the `prop`
  leaf's any-path projection reads + the weight modifiers;
  *continuation & chains* = the hooks buffer (EVENT_SCHEMA §5, 10–50
  turns out) + the arcs + the options + the cause tree (M3);
  *off-screen life & absence* = the cold tiers' macro aggregates +
  autonomous urgencies + rotations (D-021 — the world answers for
  itself); *false coincidence* = pack-declared schedules (rotations,
  travel) that the reader patterns into legends — the perception is
  the player's, the machinery zero; *second-order stories* (the
  reader infers the event from its residue) = the scene-line claims +
  the fire-follow-up shapes. The source's NPCLedger IS the projection
  + knowledge view (goals → urgencies/faction rolls, schedule →
  rotations, route → travel, memory → knowledge/echo/traits, state →
  status axes) — zero new ontology, the source's own verdict.
- **The one gap — the re-encounter delta** (`since-1`, TASKS,
  owner-gated): the rendered half of "what happened since last
  meeting" — a read-side line family on the entity/scene cards (fold
  deltas since the last co-presence tick + the knower's own heard
  records), the source's single-highest-value pick; the world-side
  half already runs on the macro cadences.
- **The event-source taxonomy** (pack-design vocabulary, never code):
  encounter (entity intersection) / interruption (crosses the
  reader's route) / consequence (a past event reaches a new state) /
  opportunity (world state opens a door) / discovery (arrival at a
  running process — lazy detail + condensation) / recurrence (a known
  entity again) / chain (a causal continuation). The doors and the
  director's release paths already implement all seven; the taxonomy
  names what a pack's families are.
- **The world-state law** (the source's `world_state` object
  refined): global pressure ("bandit_threat: low") is a DERIVED read
  over the fold at its consuming surface (a predicate, a rendered
  line — L3), never a stored mutable object (STATE-1/D-006); the
  causal route to the same effect: the destroyed den shrinks the
  faction's live member base and the ratio dynamics answer (depth-6),
  the scarcity answers (res-1's derived spreads).
- **The detour fence**: "off the obvious path" triggers are WORLD-SIDE
  predicates (a place leaf on a declared location + the quiet gate —
  pack data today), never player-intent inference (a "deviated" flag
  is the Alien learns-the-player anti-pattern's edge case; L6/
  EPIST-1 — the director reads the world, not the player's plan).
- **The anti-repetition composition** (the anti-spam asks, answered
  by standing layers): the per-NPC cooldown + the first_time_only
  burn + the arc gaps + the world-coupled weights (different runs,
  different winners) + the REST breathing room; a novelty-score
  subsystem is REFUSED as duplicate bookkeeping — a multi-day pack
  that repeats a family cures it with a weight modifier reading a
  recent-release leaf (zero new machinery). Per-TAG recurring
  cooldowns wait with the recurring murmur (DIRECTOR_SPEC §11, the
  first-consumer law).
- **The selection law** (the source's "weighted selection" refined):
  the Paradox ai_chance lands as weight EVALUATION — the heaviest
  effective option wins, ties by declaration order, zero RNG
  (drama-2); the weighted draw stays excluded with MTTH (TIME-1).
- **Parked, owner-gated**: the Kenshi arrival-side dive (squads
  triggering events on arrival = the condensation consumer; joins
  ref-20's/world-2's opening, just-in-time); the 5–8 hook-pattern +
  condition-pair catalog over the committed tavern_pack (this block's
  first consumer — a content row with a real corpus price,
  post-exit-review); the radiant-template authoring shape (the
  step-off-the-road micro-scenario as pack data — rides PACK_SPEC).

The pressure-city donor (intake-11, D-147 — the owner's 2026-09-13
donor-blueprint call routed; the same consult posture as the minus
ledger, the cost laws and the encounter catalog: a future pack reads
this before authoring; the external document stays outside the repo):

- **The displacement law** (the concept's one word-for-word keeper):
  stabilization is displacement — reducing pressure at one node raises
  it at another, and part of the cost is never repaid in space, it is
  deferred into time. The engine's three halves: res-1's closed cycle
  carries the spatial half (the flows), the Cooling Debt carries the
  temporal half, diegetic consequence rendering carries the moral half
  (the thermometer minus — the moral cost never gets a meter).
- **The Cooling Debt**: a monotonic, publicly-recorded, irreversible
  aggregate that grows on major thermal events and surfaces as a
  delayed public follow-up — weather-1's chain + erosion SHAPE over
  the maclock cadence: time-triggered explicit counter-events, the
  never-regress law, draw-free ratcheting (no new stream family); NOT
  a second res-1 engine (D-116/D-119 held — res-1 keeps the actual
  flows coal/water/metal, the Debt rides the ambient family).
- **The gauge**: one legible local meter that systematically omits the
  aggregate cost — exactly res-1's designed read surface (REFERENCES
  §10 Darkest Dungeon/Frostpunk: integer truth below, one rendered
  line above). One visible meter only; extending it into a corruption
  or decay meter is the thermometer minus (consequence-rendered,
  never scored).
- **Legal exclusion** (the un-personed layer): districts struck from
  the registry = the D-134 cost/failure family's application — a
  state/flag axis (`legal_status: excluded`) + knowledge records
  documenting the exclusion; a claim filed from an excluded district
  is a logged, rejected attempt (failure is canon). "DORMANT" stays
  reserved for the engine's declared-but-unarmed meaning.
- **Objective-function factions**: the antagonist pair is two agents
  optimizing different objectives over the same system (minimum
  immediate deaths vs. minimum 20-year systemic damage) — depth-6's
  own shape (each faction's dependency → goal → threshold → action →
  downstream consequence over live member axes), never a scripted
  thesis; internal splits stay emergent.
- **The lore hooks** (pack-ready, templates + `provenance.cause_hook`,
  D-140): the Wall of Disconnections (a recurring template + state
  flip + cause_hook back to the exclusion event), the three-tap pipe
  ritual (texture, zero mechanic cost), "he died in a working machine"
  (a tone-dial phrase, D-030), the Regulator's Archive (a
  knowledge/retrieval-ready artifact, retr-1).
- **The biome verdict** (the owner's question): a pressure city is
  authored pack data, never a worldgen biome — biomes are surface
  texture over generated sites; the city's substance (rings, legal
  exclusion, the Debt, the faction triangle) is the Qud split's
  authored half. The lost-city form is the cheap fold: one
  struck-from-the-registry location + hooks + un-personed residents
  inside any pack (world-2 L2 the natural host); the full concept
  needs the third pack slot (TASKS `pack-4`) — the minimal T1 slice:
  one district, one boiler, one gauge, three factions, one
  Cooling-Debt chain, zero core edits.
- **Refused at the door** (the donor's own cut list, confirmed): the
  pre-written ending set and the protagonist arc (D-005 — endings are
  reads over accumulated state, never four authored texts); the
  thermal-maneuver physics (the second-engine ban); the corruption
  meter (the thermometer minus). Two micro-drifts in the donor's
  mapping corrected: the AP crosswalk's enforcement rung is specified,
  not landed (rides `pack-ci`); tone/prohibition data rides the four
  files' blocks — there is no literal `meta.json`.

The presentation-contract consolidation (intake-12, D-148 — the
owner's 2026-09-13 verdict call over a multi-audit summary of the
"does the Brief IR suffice as the final LLM representation, or is a
separate presentation layer owed" question; the same consult posture
as the intakes 6..11: the external document stays outside the repo,
every load-bearing citation verified against HEAD first. A future
engine-1 opening reads this before wiring the autonomous narrator):

- **Verified at HEAD (the audit half — facts, not hypotheses).** The
  model-facing bytes: `narrator_call` = the BRIEF_SPEC §7 brief bytes
  + the `narrator_protocol` block appended — no separate
  serialization layer exists (BRIEF_SPEC §7.1; the live mode-A call
  dump: `anchor`/`regen` ride the bytes literally, the `query`/
  `retrieval` lines are mode-B-only, the document ends `## narrator_
  protocol`). The `[truncated:N]` marker: fires on budget drops
  only (§5) — on day1_full (seed 125, 56 events) the brief runs
  208–274 ws-tokens against `total_hard` 800 and NO marker ever
  fires; the committed 105-case corpus pins none. The format is
  compact ASCII (the "JSON brief" question — non-existent). The
  consolidation's evidence base predates bg-7/bg-8 (TECH_NOTES
  §10/§11), which RE-SIZE the gap: at 27B-class the input side is
  clean (0/8 invented names, zero instruction leakage in 24 beat
  replies), the measured failures live on the REPLY side — the
  brief-surface vs claim-id vocabulary mismatch IS the refusal
  engine (7/8 prose beats regen-exhausted), GBNF's own target —
  and the one INPUT-side intervention A/B-tested (bg-7 (v),
  cast_surface) earned nothing and RAISED refusals (55 vs 45):
  richer surface is not free at this class.
- **Micro-drifts corrected** (the consolidation vs HEAD): (a) "the
  trait → tendency → consequence chain is not specified" — WRONG at
  HEAD: PACK_SPEC §6 (iter-109) carries the AP crosswalk — AP-9
  spine records (want/need tension + flaw rooted in a cause), AP-8
  behavior rules CONSUMING each flaw (urgency entry, hook weight
  modifier, on_action reaction, prohibition) — specified, pack data,
  lint-checkable; enforcement rides `pack-ci`, the first consumer is
  world-2. (b) "no semantic-condensation layer exists" — PARTIAL:
  three mechanisms are landed — the traits fold → belief lines
  (BRIEF_SPEC §3.5: N records → one belief token + provenance — the
  exact atomic-facts→one-thought shape), `card_markers`
  (state→word, §3.4), the chronicle's 46 per-event template
  families. What is genuinely absent: pair-causality prose ("the
  guard suspects the player BECAUSE X and Y"). (c) "no
  don't-infer instruction" — true at spec level, misframed in
  substance: the anti-invention directives are PACK data ("Narrate
  only what the brief contains… Never invent events, names, or
  outcomes") — and by INV-3's own law narrator-prompt text MUST be
  pack data, never spec/code; the enforcement backstop is
  structural (the validator's closed world + the prose floor +
  L12), never promptual.
- **The verdict set (the eight disputed rows):**
  1. **The "60–70% ready" frame: REFUSED.** A contract without a
     consumer has unknown requirements — the metric is
     meaningless-by-construction, not merely contested; its only
     honest form is the consumer measurement (the {3–8B, GBNF}
     run). The gap is sequenced-by-design: D-022 + BRIEF_SPEC §9's
     last row names the owner gate (engine-1, AGENTS §8).
  2. **`narrator_protocol` as model noise: fact CONFIRMED, harm
     re-owned.** The block rides the model-facing bytes with no
     "not world facts" marking — true. But at dev-time it is the
     operator's reply-contract signal (the anchor is what the reply
     must carry — signal, not noise, for the D-055 external
     narrator), and the measured leakage at 27B is zero. The
     concern fires exactly at engine-1's opening — where the GBNF
     grammar makes output-side protocol noise structurally
     impossible and the input-side split (canon-facts vs
     control-metadata) is a one-block serializer decision, not an
     architectural gap.
  3. **`[truncated:N]`: the marker STAYS; the A/B rides the weak
     arm.** The marker is the anti-silent-drop invariant (§5:
     hiding truncation is the named violation) — trading an
     auditable invariant for an unmeasured prompt-theory benefit is
     a crutch. The golden-set experiment (with/without marker) is
     legitimate science but belongs to the {3–8B, GBNF} family
     (bg-7's instrument), never a standalone iteration: at 27B the
     adjacent C3.5 signal is clean (0/8 first-reply confabulations)
     and the structural gates hold everywhere (L12 never blocked a
     beat).
  4. **Deterministic condensation: pattern CONFIRMED, instrument
     corrected.** The landed pattern is fold → token → provenance
     (LEGEND_SPEC family: the belief line IS condensation, inside
     the brief since leg-2). Pair-causality condensation, if a
     consumer ever demands it, rides the SAME fold pattern — never
     tracery (flat-key conditionals, event-per-line: the iter-43
     law puts nested causality out of its shape) and never the
     assembler (L2: the brief renders dry tokens; prose is
     downstream).
  5. **Lost-in-the-Middle: REFUSED as a requirement driver.** The
     repo owns the geometry law its own way — MECW (TECH_NOTES §2:
     the MEASURED effective window 8–16k on local 27B, "budgets
     against THIS number, never the nominal context size") + the
     landed live-char geometry (voice exemplars near the context
     end, recency-first scene_delta). Foreign LiM conclusions
     measure other models and other documents; the local
     instrument is the heartbeat trend line (TEST_PLAN §8.5) on
     the engine-1 arm — measuring mapping honesty and refusals,
     not positional recall. No bespoke LiM replication, no
     author's-note placement requirements from foreign research.
  6. **`LLM_PRESENTATION_SPEC` now vs by parts: NEITHER.** The
     spec is written at the engine-1 trigger FROM the weak-arm
     results (D-022 + SPECS_BACKLOG's own header: a spec before
     its trigger is scope creep; a draft spec is a convenience
     copy that rots). When written it is the D-055 file-contract
     pattern's FOURTH instance (VALIDATION_SPEC owns the reply,
     PARSER_SPEC owns mode C, this spec owns the call's
     model-class wiring), ABSORBS `st-4` (the call budget +
     transcript-tail contract — already the row's own sketch; one
     owner, never two), and owns a THIN MAPPING table over the
     existing 8 blocks + `narrator_protocol` (canon-facts vs
     control-metadata, truncation semantics, MECW small/medium/
     large profiles) — never a second re-labeling vocabulary for
     the same blocks (D-024: link, never restate).
  7. **The character/behavioral layer: ANSWERED by PACK_SPEC §6.**
     The chain decomposes by design across existing homes: the
     spine record (AP-9) → the behavior rule consuming the trait
     (AP-8, through the intent door's gate family — the iter-46/55
     fence: folds gate behavior through the door, never channel
     inputs, never probability multipliers) → the committed event
     (canon) → the existing presentation surfaces (card markers
     for standing state, belief lines for derived views, voice
     exemplars for style). A presentation-side behavioral layer
     (richer voice/directives prose) is REFUSED — wrong layer: it
     puts behavior where the engine cannot gate it, violates L2
     voice isolation, and duplicates four homes.
  8. **The priority dichotomy (bg-8's weak arm vs the presentation
     contract): DISSOLVED.** One row, one gate: the {3–8B, GBNF}
     run is not the alternative to the presentation contract — it
     is the contract's requirements-generating measurement (what a
     3–8B model misreads in the current format IS the requirement
     set; what GBNF makes structurally impossible IS the
     non-requirement set). Sequencing after the owner call: run →
     requirements from results → the spec written (absorbing
     st-4).
- **Landed:** the TASKS `presentation-1` row (owner-gated,
  engine-1's decision-input child; exit criterion the {3–8B, GBNF}
  run — bg-7's five families + the two surviving intake-12 probes:
  the truncation-marker A/B, the protocol-split A/B). The build
  queue UNTOUCHED — world-2 L1 stays the pinned CODE row.
- **Refused at the door:** the draft `LLM_PRESENTATION_SPEC.md`
  now (the trigger law); the 7-layer ROLE/SCENE/EPISTEMIC/CAUSAL/
  STYLE/TASK/OUTPUT vocabulary (a re-labeling of the 8 blocks);
  any BRIEF_SPEC §7.1 byte change or pack directives edit today
  (both corpus-priced; the protocol-block geometry is §7.1's owned
  bytes); the bespoke LiM experiment; the presentation-side
  behavioral layer.

The open-ended actions & honest-simulation analysis (intake-13,
D-150 — the owner's 2026-09-13 research call over the uploaded
architectural review "open-ended действия, контент-паки и честная
симуляция"; the same consult posture as the intakes 6..12: the
external document stays outside the repo, every load-bearing
citation verified against HEAD first. The review's doctrine half
re-derives the standing law with near-zero factual drift; its
proposal half carries four genuinely new items — all routed
below, none build-grade now. A future parse-2/engine-1 opening
reads this before widening any grammar):

- **Verified at HEAD (the doctrine half — facts, not hypotheses).**
  The review's core contract — simulator produces facts, mediator
  resolves intents, LLM interprets, canon changes only via the
  simulator — is VISION §1 verbatim-compatible; the sycophancy
  cure ("rolls decide, never prompts") is VISION §5/§6 standing
  law; the §13 may/cannot table is INV-4 + the mediator's closed
  document (D-055) + the validator's closed world (an invented
  entity is `contradicted`, an unmodeled prop `insufficient_data`
  — canon never fabricates an opinion). The epistemology (§8:
  claim ≠ fact, belief ≠ fact) is the landed knowledge model:
  records carry `who/channel/fidelity/source`, never a truth
  field; lies are crafted records (D-008); acceptance rolls from
  the listener's own trust (EPIST-1); rumor drift is family-gated
  (68a/68b). The four-case taxonomy (§6) maps onto the door's
  actual layers: case A = the wired resolver computes (a declared
  action always wires a resolver + lint-closed event types,
  PACK_SPEC §3); case C = the off-grammar refusal at the parse
  boundary (the grammar snapshot; the nearest-valid menu,
  iter-107) — never a fake event; case D = the FAILURE branch
  (check margin + the `failure_total` band); case B (an action
  declared with no modeled effect) is structurally unreachable in
  authored packs — the one half-case that exists (use on an item
  without `use_effect`) is a door REJECTION via `has_field`, an
  honest in-world refusal. The unsupported ≠ failure distinction
  the review demands HOLDS at HEAD — at the boundary-vs-canon
  layer split, not as canon-level statuses. The chain-execution
  half of §7 is the loop's standing semantics (door check →
  schedule → OCC re-check → check → resolver → ignitions; the
  step-feeding law: step N+1 reads step N's real state, a
  rejection is cause-chained, nothing pretends); only the NL
  decomposition (one utterance → N intents) is owed — and it is
  parse-2's own row (PARSER_SPEC §7, the live-session-evidence
  trigger). The travel half of §12 is landed (st-6a price law,
  D-112's three zones, macro aggregates, the road_pack L1 with
  derived prices 150/210/300/360); roads-1 stays owner-gated.
  The explainability ask (§17) is largely standing:
  `scripts/mechanics.py` trace/why/blast (D-118),
  `outcome.failed_test` on every rejection, OCC cause chains,
  check summaries in outcomes, `provenance.cause_hook` +
  payoff-latency; the known boundary is deliberate — autonomous
  precondition failures stay silent (the noise floor, D-005).
  The pack-sufficiency criterion (§1 — long explainable chains
  without a scripted scenario) is the repo's own instrument: M3
  mean ≥ 2, T8 OFF 24 chains seed 125 (15–24 over 60 seeds), and
  the review's own example chain is live pack data (fire → smoke
  → `smoke_penalty` −20 on perception → the acquisition fidelity
  stepping down at smoking sites, D-106 → telling/drift →
  relation effects).
- **Micro-drifts (the review vs HEAD):** (a) "Phase 6 remains a
  future litmus test" — stale by three days: the exit instrument
  is MET BY MEASUREMENT (iter-112/D-149, the clock 14m24s, zero
  core edits); the gate verdict stays the owner's. (b) The §4
  primitive lists read as near-term machinery; the admission law
  (D-142) splits them — the social half already exists as
  resolvers (converse/coerce/divert/steal + the secrets/leverage
  blocks), the physical half (combine/separate/transform) is
  res-1-territory mechanic growth, each entry passing the
  second-pack test on its own, never a batch import. (c) No
  factual errors were found — the review was written against the
  repo, and its §18 doctrine table restates the standing
  invariants (intent ≠ execution, attempt ≠ success, description
  ≠ outcome, LLM narration ≠ canon authority).
- **The verdict set (the four proposals):**
  1. **The compositional causal substrate (§4): CONFIRMED as
     direction, ROUTED — never a new layer.** The buildable form
     decomposes onto existing rows: D-096's affordance derivation
     (action availability from entity props — pack-lint data,
     never an open resolver), parse-2 (the multi-intent reply; the
     loop needs ZERO simulator change to execute a chain — the
     queue/door/OCC machinery already sequences intents
     causally), and engine-1 (the GBNF grammar enumerating the
     closed action set is where composition-in-grammar would be
     decided). A generic "primitive operations" engine layer is
     REFUSED as speculative — no consumer, and the abstraction
     cost gate (L13) fails it today.
  2. **PARTIAL as an outcome status (§15): DEFERRED to the first
     real consumer.** Genuinely absent — the steal margin split
     is a failure BAND, not part-success. The house shape exists
     (the `failure_total` precedent: a pack-declared branch riding
     the closed pattern); the admission question ("must a second
     pack carry it for the mechanic to exist?") answers itself
     only when an action with separable sub-effects is authored.
     No core pre-work.
  3. **UNDER_MODELLED / NO_MODELED_EFFECT (§16): REFUSED as a
     standing runtime status; CONDITIONAL on composition.** In
     closed-grammar worlds the class is unreachable — an action
     exists only with a wired, lint-closed effect; the honest
     limit is the grammar boundary itself, and a runtime "I
     don't know" status would soften the closed-world discipline
     (an authoring failure would become a playable outcome). The
     preferred cure, if compositional actions ever land, is the
     PACK-CI CLOSURE LAW: the lint refuses any declared
     composition whose reachable pairs do not all resolve to
     declared effects (the reaction table closes at authoring
     time; an unresolvable pair is an author error, never a
     runtime status). This gathers the review's honesty goal
     (never hallucinate an effect) with the repo's closure
     discipline (never unknown at runtime) and eliminates the
     third status entirely.
  4. **Inventions as emergence-from-repetition (§5): PARKED
     pattern, no row.** Genuinely new — no standing row or
     parked pattern covers
     repeatable-combination → procedure → knowledge transfer.
     The honest-recording chain (combine → state_change →
     repeatable_result → knowledge_created) maps onto existing
     grammar (events + knowledge records + hooks), so a future
     pack system needs no core pre-work; its real substrate
     arrives with res-1 (the closed scarcity cycle gives
     combinations stakes) and world-2 L2 (the province gives
     them a world). Parked here with the intake-9 parked-pattern
     family.
- **Landed:** D-150 (this verdict set) + this intake block. The
  build queue UNTOUCHED — nothing unpins, nothing reorders; the
  standing owner-gated rows own every build-grade item (parse-2,
  engine-1, res-1, world-2 L2, roads-1, pack-ci).
- **Re-entry (iter-122, the owner's 2026-09-18 «отработай по
  файлу» call over the re-uploaded review — the same source,
  content-matched section-by-section against this block's
  citations; re-verified at HEAD 1a9efaf): D-150's verdict set
  holds, zero new findings, NO ACTION.** The cited sections
  (§1/§4/§5/§6/§7/§8/§12/§13/§15/§16/§17/§18) match this block's
  record exactly; the uncited §2/§3/§9/§10/§11/§14 decompose onto
  its own principles — cast_fireball is case C, the politics/
  manipulation/dragon sections ride §8's claim≠fact over the
  landed knowledge/relations model, §14's factor-list-then-RNG is
  the check margin + EPIST-1's acceptance rolls under INV-2. The
  code anchors re-verified: `core/loop.py`'s door→schedule→OCC→
  check→resolver chain + the st-6a price law (verdict 1's
  zero-simulator-change claim), PARSER_SPEC's grammar snapshot +
  nearest-valid menu (case C), mechanics trace/why/blast (§17),
  the who/channel/fidelity records (§8), and the parked rows
  (res-1, roads-1, since-1, parse-2, engine-1) all standing. Two
  pins strengthened since this block was written: micro-drift
  (a)'s correction now carries the gate verdict itself (D-151
  PASS, the ladder complete) plus a second measured instance (the
  province pack D-153/154 — original content, its one core touch
  a load-time lint rung, never runtime); and verdict 3's preferred
  cure is now live enforcement (D-152's teleology rung refuses a
  declared action without declared effects at load). PARTIAL stays
  deferred — no separable-sub-effects action authored yet. The
  re-uploaded v2 methodology document re-derives intake-15's own
  confirmed record with no new drift. Nothing re-routed; no new
  D-row; the queue untouched.

The causal-architecture research bootstrap (intake-14, D-155 — the
owner's 2026-09-18 research call over the uploaded bootstrap document
(`canonsim_causal_architecture_research_bootstrap`); the same consult
posture as the intakes 6..13: the external document stays outside the
repo, every load-bearing claim verified against HEAD first. The
bootstrap frames one objective — a single canonical world in which NL
intent compiles to a constrained causal representation, deterministic
core logic validates and resolves it, accepted consequences become
ordinary canonical events/state, dynamically created entities behave
exactly like generated state, existing mechanisms consume them
normally, special-case mechanics do not grow combinatorially,
simulation scales coexist without second authoritative worlds, and
recurring secondary outcomes derive from more fundamental causes.
The doctrine half is intake-13's own confirmed ground; the genuinely
new material is five architecture questions. A future
res-1/st-5/parse-2/engine-1 opening reads this before promising any
of the eight properties):

- **Verified at HEAD (the standing half — facts, not hypotheses).**
  The bootstrap's foundational boundary, canonical-vs-interpretation
  split, LLM may/may-not lists, prevention list, and
  persistence-without-the-conversation requirement re-derive
  intake-13's confirmed doctrine (VISION §1/§5; INV-1..5; D-055's
  file contract; D-052's closed world — an invented entity
  `contradicted`, an unmodeled prop `insufficient_data`; D-095's
  prose floor; D-139's resume law — promoted texture rode events and
  stays canon, live texture dies with its session, so the
  originating LLM conversation is never required for persistence).
  Its §16 question list decomposes onto the intake-13 routing
  (substrate → D-096/parse-2/engine-1; PARTIAL deferred;
  UNDER_MODELLED refused; inventions parked) — zero factual drift
  found beyond intake-13's own record.
- **The five questions (the bootstrap's new material):**
  1. **Causal compression (§5/§6/§10): CONFIRMED as standing
     practice, never as one law sentence.** The bootstrap's
     principle — a result is either an explicit canonical fact or a
     deterministic consequence of more fundamental causes — is L3
     ("derive, never store") plus the authored-facts-win boundary,
     with the strongest landed instances: the travel price law
     (st-6a — the DERIVED integer function of the WorldModel:
     lattice steps * `step_ticks` + height-band spread *
     `climb_ticks` + river endpoints * `river_ticks`, integer math,
     draw-free, the pack override winning per edge; armed twice —
     the road's 150/210/300/360, the province's 345–705), the
     faction small formula (the affected fraction of the
     membership, per-cent floored, pure integer arithmetic), the
     macro-year counter, the weather state as fold, the cold
     census, the echo/traits read folds, and intake-10's
     world-state law (global pressure a derived read at its
     consuming surface, never a stored object). The bootstrap's
     two failure modes are both fenced: outcome-table explosion by
     L9/L13 (the affordance clause rides PACK_SPEC §8,
     AFFORD_SPEC trigger-gated — pack-lint table data, never an
     open resolver), universal-model explosion by the
     authored-facts-win law (`travel.edges`, D-030's tone dial,
     the spine records, the names profiles — authored world
     knowledge stays canonical without derivation). The
     damage-as-derived question (§10) is the future combat-bearing
     pack's own (the soul-scar parked family; combat outside every
     planned phase) — no pre-work owed.
  2. **Simulation levels (§7): CONFIRMED — one world, resolution
     strategies, never second engines.** The bootstrap's "one
     canonical world, one event/state truth, one causal substrate,
     multiple domains and resolutions" is the landed shape: the LOD
     one-gate law (depth-3), maclock-1's layered clocks under L4,
     the D-112 one-event-with-cardinality surface (counts for
     populations, events for notables), the condensation tier
     transition, and the id-never-changes law (known_by, texture,
     old knowledge survive the tier shift). The separate-engine
     alternative (NPC engine / battle engine / economy engine /
     weather engine) was never built and is the named anti-pattern
     family ("no physics engine", D-116 (7); "never a second
     economy engine beside the canon door", D-116; "never a second
     res-1", D-147). The bootstrap's domain list maps onto the
     resolvers registry + the closed mechanic set — domains are
     PACK vocabulary over one door, not engine seams (D-142's
     admission law owns the boundary).
  3. **Large-scale aggregation (§8): UNRESOLVED — the substrate
     landed, the claim unmeasured, correctly.** The bootstrap's
     1k–10k-actor battle/siege question has no repo evidence, and
     the bootstrap's own discipline ("do not promise a scale
     target until benchmark evidence exists"; "do not infer
     10k-actor feasibility from architecture alone") is the repo's
     measured-numbers law (TECH_NOTES owns numbers, never prose).
     What landed: the aggregate machinery the question would ride
     (macro aggregates with cardinality, O(groups × macrobeats)
     log growth, the group as intent-door actor — depth-6's one-id
     law, condensation with first-commit-wins, the cold census),
     and the only 10k-scale measurement that exists (worldgen
     genesis: 10,000 sites in 1.19 s, draw-linear — TECH_NOTES
     §12). What does not: combat itself, any battle benchmark, any
     measured aggregate→individual mid-event refinement. PARKED
     with the intake-9 family: the first combat-bearing pack
     decides whether a benchmark row opens (the st-5
     first-consumer law's own shape); no row created now.
  4. **Stealth as a causal chain (§9): PARTIAL — the epistemic
     half landed, the physical half authored.** The bootstrap's
     chain decomposes at HEAD as: movement (landed — the sighting
     records, visual only, same-location never through exits) →
     emission (PARTIAL — noise is authored per-action knowledge
     resolution: `drop_break`'s noise, the alarm's through-walls
     heard channel; no surface/load/equipment-dependent sound
     model) → propagation (authored adjacency — `alarm_adjacent`
     — never derived attenuation) → perception (landed — the
     acquisition conditions, depth-1: smoke steps birth fidelity
     down at the event site, the fire chain's own measured
     modifier) → knowledge (landed — channels, birth fidelity,
     `known_by`) → reaction (landed — panic contagion, wariness,
     suspicion, the beliefwire gates). Whether the
     emission/propagation half ever generalizes is a
     first-consumer question (a pack wanting stealth as a mechanic
     decides, per D-142 — a derived noise substrate alters WHAT
     mechanics exist); no pre-work owed, no row created.
  5. **Dynamic entities / materialization generalization (§4):
     CONFIRMED at the law level — one shape, four instances, zero
     generic engine, by design.** The bootstrap asks whether
     texture promotion is a special case of a more general
     materialization mechanism; at HEAD the relationship is the
     inverse of a special-case: the D-054 slot shape
     (`StateChange(entity, prop, None -> value)`, absence IS the
     unborn state, first-commit-wins, canon never redraws) is the
     PARENT LAW, and the landed family are its instances —
     texture promotion (iter-11, the object's canon birth on a
     take), scene detail (depth-2, `scene:<id>:detail`), names
     (name-1, `name:<npc>`), member_of (depth-7's condensation) —
     each docstring-declared "never a second mechanism".
     Entity-birth promotion (the bootstrap's portable figurine —
     carried, stored, stolen, burned) is designed as the same
     door with pack grammar (blueprint §7's containers law) and
     deferred to st-5's first consumer (a pack wanting portable
     objects, a res-1 sink shape — never a speculative build).
     The integration half is landed law: materialized state is
     ordinary fold state (the erosion commit scans the fold for
     the rule's `from` holders — one counter-event per entity;
     the fire layer's follow-ups; knowledge and texture survive
     condensation by the id law).
- **Micro-drifts (the bootstrap vs HEAD):** (a) the bootstrap's §4
  framing ("texture promotion as a special case of a more general
  materialization mechanism") inverts the repo's law — D-096's own
  record: the D-054 texture-promotion door is the ONLY
  materialization mechanism, phase 5 extends it, never builds
  beside it; the generalization exists as the shared SLOT SHAPE,
  never as a generic engine, and L13 holds that line deliberately.
  (b) The bootstrap's §12 outcome-class vocabulary
  (RESOLVED_PARTIAL, INSUFFICIENT_INFORMATION,
  UNSUPPORTED_NOVELTY) re-proposes intake-13's refused and
  deferred rows — D-150's verdicts stand unchanged (PARTIAL
  deferred to the first separable-sub-effects action;
  UNDER_MODELLED refused under the pack-CI closure law; the honest
  boundary is the grammar edge, never a runtime status). No
  factual errors found in the bootstrap's repo-facing claims.
- **Landed:** D-155 (this verdict set) + this intake block. The
  build queue UNTOUCHED — nothing unpins, nothing reorders; the
  standing owner-gated rows own every build-grade item the
  bootstrap touches (res-1, st-5 via its consumers, parse-2,
  engine-1, world-2 L2, roads-1), and the three parked patterns
  (the scale benchmark, the stealth emission substrate,
  damage-as-derived) join the intake-9 parked family — named here
  so a future row finds them.

The narrative-design research dossier (intake-15, D-156 — the
owner's 2026-09-18 research call «начни работу с документом» over
the uploaded seven-source GDC synthesis
(`CANONSIM_NARRATIVE_DESIGN_RESEARCH`: RimWorld/Sylvester, Slime
Rancher/Popovich, Sims/M. Brown, Shrouded Isle/Kim, Heaven's
Vault/Ingold, Procedural Narrative Generation/Cardona-Rivera &
Martens, the PAX-2015 DF panel) + the research-workflow methodology
document (v2 supplemented — the process half); the same consult
posture as the intakes 6..14: the external documents stay outside
the repo, every load-bearing claim verified against HEAD first. The
dossier proposes 18 design laws, 7 gaps, 10 narrative-quality
metrics, 4 diagnostic surfaces, 5 documentation rules, a
12-iteration research-to-code program, 10 anti-patterns, and 8
reference fixtures. A future brief/director/metrics/pack opening
reads this before proposing any narrative-quality instrument):

- **Verified at HEAD (the doctrine half — facts, not hypotheses).**
  The dossier's boundary quote is VISION §1 verbatim (simulator
  produces facts, LLM produces meaning, log stores canon, mediator
  holds the boundary); its repo inventory (§1/§11.1 — director
  pacing/channels/hooks/release chains, knowledge + blind-NPC
  tests, deterministic scene briefs, scene texture as a separate
  narrator-created layer, worldgen history, factions with goals,
  travel + weather, packs, deterministic replay + narrative
  regression machinery) is all standing surface, checked one row
  one owner. Its named risk — "mechanics becoming technically
  correct but narratively inert" — is the M-metric targets' own
  text (MVP_SCOPE §15: M1 non-trivial and rising, M3 mean ≥ 2, M4
  novelty rising, M5 non-zero at director-off), so the risk is not
  an uncovered alarm but a restatement of the standing instruments'
  reason to exist. The seven source dossiers' mechanisms decompose
  onto landed shapes: RimWorld's elastic failure = the door's
  FAILURE branch (a cause-chained rejection is a fact; the
  crime ladder rides a steal FAILURE to its boss beat);
  Slime Rancher's needs-as-engines = the AP-9 spine
  (want/need/flaw/cause, lint-live since iter-117, five spines in
  the province pack); the Sims' promise trees = the hook buffer
  (seeded at event time), inverse autonomy = panic/wariness gates +
  the urgency weight modifiers, fear trees = the suspicion pair
  axes escalating by family; Shrouded Isle's
  tragedy-from-locally-rational-decisions = D-005's own law (harm
  emerges from state, never director whim); Heaven's Vault's
  authored/procedural coexistence = the pack/worldgen split; the
  PNG drama-management triad = D-005 + DIR-4 (the consequence
  planner IS the "sits between them" answer); the DF panel's
  history-as-consequence-graph = the worldgen history bridge (the
  DF Legends donor family, `docs/ref/df_design.md`).
- **The 18 laws: CONFIRMED as re-derivations of standing law —
  zero new law text owed, the L-family owns the namespace.** The
  mapping (each law → its standing owner): 01→L9+L1+the M targets;
  02→L9/L13/L14; 03→L9's own formula (depth = O(intersections)) +
  M1 + `mechanics.py matrix`; 04→L8 (consequence pairing: same-
  scene Price + deferred hooks) + EPIST-1's price + the
  price-marker admission lint (PACK_SPEC §6, D-152); 05→D-005's
  seeding law (complications seeded at event time, never invented
  later) + M2; 06→M2 + `payoff_latencies` (D-140) + L8's deferred
  half; 07→the failure branch (the `failure_total` band, the
  step-feeding law — intake-13's confirmed set); 08→AP-9 spine +
  urgency entries + EPIST-1 (the pressures-vs-biographies split is
  the spine's own shape — traits are derived folds, never authored
  biography fields); 09→the landed knowledge model (records carry
  who/channel/fidelity/source, never a truth field; lies are
  crafted records D-008; EPIST-1; L6); 10→the epistemic laws +
  D-055's narrator file contract (implication is the narrator's
  licensed read, canon claims need canon basis — the refuted-entry
  ledger law); 11→D-005 (consequence planner, never an
  improviser; entropy reads observables only, L6) + the T8
  director-off A/B; 12→the authored/procedural split (packs buy
  guarantees, worldgen buys variation, PACK_SPEC + D-142's
  admission law); 13→the knowledge-channel substrate (PARTIAL —
  the recovery half is since-1's standing row); 14→L7 (causality
  is recorded, not reconstructed) + `provenance.cause_hook` +
  mechanics `why`; 15→the T-family graph discipline (T8 A/B, the
  arc-driver tests, the corpus pins — TEST_PLAN §6); 16→
  `emergent_chains` + `beat_tension_profile` + the chronicle's
  tale importance gates; 17→BRIEF_SPEC §5's eviction contract
  (verbatim-compatible: beyond-cap items render nothing, never a
  budget drop; whole-block eviction in ascending priority order);
  18→BRIEF_SPEC §3's eight blocks — fact=`scene_delta`,
  state=`present_entities`, epistemics=`recalled_facts` (the
  belief line + the knowledge line, already two distinct item
  shapes), texture=`scene_texture`, affordance=`active_options`.
- **The 7 gaps: five PROVEN as landed instruments, one PARTIAL
  (standing row), one re-labeling refused.** GAP A (narrative
  leverage) — the M-family + `systems_touched` + `payoff_latencies`
  are the landed instruments and the balance harness runs them
  across 1000 seed-varied runs; the composite
  `narrative_leverage(event)` formula is REFUSED as a second
  metric vocabulary (D-024/L13: no consumer, the components are
  already measured and reported). GAP B (consequence half-life) —
  `payoff_latencies` (D-140) measures exactly
  seeding→release in ticks; "half-life" is a re-labeling of the
  same measurement, refused as duplicate vocabulary. GAP C
  (action-loop pressure) — M4 novelty/repetition +
  `eventless_beat_stretches`, landed iter-6. GAP D (retrospective
  explainability) — `scripts/mechanics.py` trace/why/blast
  (D-118) + L7 cause chains + OCC cause attribution + outcome
  check summaries — the dossier's ITERATION-5 `why EVENT_ID`
  proposal predates D-118 (a stale pin, the intake-13 litmus
  drift's own family); the hook-centric `why` + the tick-centric
  `trace` + the two-arm `blast` cover the ask. GAP E (breadcrumb
  density) — PARTIAL: the substrate landed (knowledge records,
  channels, sighting/witness/rumor/telling spread, the leverage
  clusters, the drift family); no density metric exists and none
  is owed pre-consumer; the recovery half (alternate evidence
  routes when a clue is missed) is since-1's own standing
  owner-gated row — no new row. GAP F (character pressure
  surfaces) — the AP-9 spine IS the pressure card (lint-enforced
  want/need/flaw/cause per named NPC; the echo/traits folds the
  derived residue; `mechanics.py matrix` the static view); a
  dedicated projection surface is REFUSED (L13: the existing
  reads own the need). GAP G (director anti-authoriality) —
  PROVEN by construction: the director releases only seeded hooks
  through the intent door (D-005 — it cannot write canon, it
  cannot invent an action, a release rides the actor's own intent
  machinery); the "forced action" class is structurally
  unreachable; T8 director-off is the standing A/B; the entropy
  mirror + the burn law fence un-dischargeable tension.
- **The NQ-01..10 metric vocabulary: REFUSED as a second label set
  (D-024) — the T/M families own the metric namespace.** The
  mapping: NQ-01→L7 (cause on every event); NQ-02→the door's gate
  family + the urgency/beliefwire channel law; NQ-03→M2 +
  payoff_latencies; NQ-04→T3 blind-NPC (LIVE, the phase-4
  extension iter-63) + beliefwire counters (the de-crystallization
  path — belief divergence IS landed, a belief held at T can be
  absent at T' > T) + suspectaxis per-target figures + the drift
  twins; NQ-05→GAP E/since-1; NQ-06→mechanics `why`/L7; NQ-07→the
  failure branch; NQ-08→`emergent_chains`/`beat_tension_profile`;
  NQ-09→M4; NQ-10→T7 (the manual retell) + TEST_PLAN §8's
  testproto Layer-1 contract tests + the golden-set A/B (D-148's
  weak arm) + the deviation corpus (the owner's 2026-09-07
  clarification). Recorded here so a future row finds the
  translation, never as adopted names.
- **The 4 diagnostic surfaces: why/blast LANDED, the ledger and
  the card are standing shapes.** §14.1/§14.2 (`why`/`blast`) are
  D-118's own instruments. §14.3 (story-material ledger: open
  threads, unresolved tensions, active suspicions) IS the director
  buffer + the folds — hooks are tension facts folded from the log
  (rebuildable, L11; un-dischargeable tension counts toward
  entropy), the crystallized beliefs are the standing suspicions;
  a second ledger would violate L3/L11. §14.4 (character pressure
  card) — the spine + the present_entities/pair reads +
  `mechanics.py matrix`; a dedicated card surface is REFUSED (L13,
  same as GAP F).
- **The documentation rules D1–D5: four standing, one refused.**
  D1 (architecture changes update the owning spec), D3 (every new
  mechanism gets fixtures — the corpus's own landing shape), D4
  (narrative bug → KI — AGENTS §5 verbatim-compatible), D5 (avoid
  duplicate truth — D-024 verbatim-compatible) are standing law.
  D2's NLAW-* ID family is REFUSED: the law namespace is owned
  (L1–L14, EPIST-*, DIR-*, drama-*, AP-*, INV-*, M-*, T-*, the
  D-rows); the dossier's 18 laws re-derive the L-family, so a
  parallel NLAW numbering would be duplicate truth — the ID
  discipline itself is already standing practice.
- **The 12-iteration program: decomposes onto standing
  instruments and owner-gated rows — zero build-grade items.**
  IT-1 (the law audit) is THIS intake's verdict set; the standalone
  `NARRATIVE_LAW_AUDIT.md`/`NARRATIVE_INTERACTION_MATRIX.md`/
  `CONSEQUENCE_AUDIT.md`/`EPISTEMIC_NARRATIVE_AUDIT.md` documents
  are REFUSED under D-024 (parallel owners for audits the block
  and TEST_PLAN already carry). IT-2 = `mechanics.py matrix` + M1;
  IT-3 = the door gates + the urgency/beliefwire tests; IT-4 = the
  metrics + payoff_latencies + `blast`; IT-5 = landed (D-118);
  IT-6 = the T3 extension + beliefwire/suspectaxis/drift; IT-7 =
  since-1's row (PARTIAL); IT-8 = D-005 + T8 (structurally
  answered); IT-9 = the M-family (iter-6); IT-10 = the committed
  corpus (the 105-case narrator corpus + the playscripts +
  `emergent_chains`) with the labeled-for-LLM-eval half owned by
  the testproto corpus discipline (TEST_PLAN §8.2 — live
  transcripts re-distilled, the anti-trap law); IT-11 = TEST_PLAN
  §8 testproto (D-098) + the deviation corpus — standing, rides
  bg-8/engine-1; IT-12 (promote the laws into governance) is this
  routing itself — the repo's governance already carries the laws.
- **The 10 anti-patterns: all standing law, and the AP numbering
  COLLIDES — the genuine new finding of this intake.** The
  anti-patterns restate: 01→D-005 (the RimWorld storyteller IS the
  repo's founding named anti-pattern, from the same source);
  02→the crystallized-belief design (traits are derived folds,
  never added personality fields; the beliefwire gate law);
  03→the noise floor (D-005's silent autonomous precondition
  failures) + M4; 04→O(relevance) never O(history) (BRIEF_SPEC
  §1/VISION §5); 05→D-005's causality law + the state-coupled
  randomization law (the Fallout anti-row, D-135); 06→the
  epistemic laws (mystery = real canon + observer uncertainty,
  L6/D-008); 07→L1 observability + the GHOST-without-anchors lint
  (dead pack data); 08→D-005 + the intent door (structurally
  unreachable); 09→since-1's family; 10→L7. But the dossier's
  AP-01..AP-10 prefix is TAKEN: the live-char crosswalk owns the
  AP family with different semantics (PACK_SPEC §6 — AP-1 pack
  budgets, AP-2 price markers, AP-8 flaw-consuming rules, AP-9
  the spine, AP-11 clone NPCs, AP-13 contradictions, AP-15
  atomicity). The anti-patterns route as THIS block's verdicts,
  never as a second AP numbering — a future doc citing "AP-8"
  must mean the crosswalk row.
- **The 8 fixtures: the corpus already carries the family; F8 is
  since-1's own row.** F1 (the theft that keeps living) =
  day1_theft_and_arson + the crime ladder (theft → partial
  witness → rumor → suspicion → the confrontation boss beat —
  the committed pack's own spine); F2 (failure redirects) = the
  steal-FAILURE path (crowd_wary, the band opens, the
  document_check ladder — seed 19/93/2/125's own probe set);
  F3 (missing witness) = the rotation/transfer family (the relief
  rotation moves the token; Doren's half waits all run — the door
  never sees a world-impossible attempt); F4 (false belief) =
  beliefwire counters + suspectaxis figures + the drift twins;
  F5 (cascading local need) = the fire chain (ignition → smoke →
  the perception penalty → telling/drift — intake-13's own
  example); F6 (retrospective tragedy) = mechanics `why` + the
  chronicle's cause-chained rendering (partial — the chains are
  pinned, no labeled tragedy fixture); F7 (director pressure
  without puppeteering) = the document_check boss beat (pack data
  over standing machinery, the option-gated confrontation) + T8;
  F8 (breadcrumb recovery) = since-1's standing row. New fixtures
  are born with the mechanics they pin (the D-098 anti-trap law —
  the corpus grows from live transcripts too), never
  batch-authored ahead of consumers.
- **Micro-drifts (the dossier vs HEAD):** (a) IT-5's `why` and
  §14.1/§14.2 propose what D-118 landed — a stale pin (the
  dossier was written against a pre-iter-84 HEAD), the
  intake-13 litmus drift's own family; (b) NQ-04's "extend
  blind-NPC from leak detection into belief divergence" is
  largely landed since iter-63/67/70 (the leak suite checks
  belief lines against the knower's fold; the counters
  de-crystallize; the figures diverge per-target) — the residue
  is the multi-POV rendering check, which is testproto
  Layer-1/2 territory (the golden-set A/B), not a track-A gap;
  (c) the methodology document's worldgen numbers (400→~0.03 s,
  2500→~0.23 s) are the external procedural-generation research's
  own measurements, slightly off TECH_NOTES §12's owned rows
  (400→0.04, 2500→0.28, 10000→1.19) — TECH_NOTES stays the
  single owner of numbers, the external figures never enter the
  repo; (d) no factual errors found in the dossier's repo-facing
  claims (§1/§11.1/§17's BRIEF_SPEC citations all verified).
- **The methodology document (the upload's second file):
  CONFIRMED as a re-derivation of the standing intake discipline
  — the repo's own protocol IS the methodology.** Its routing
  model (distill → classify → reconcile → route to the existing
  owner → smallest verification) is the D-150/D-155 intake
  precedent; its ownership map and reading gradient re-derive
  AGENT_NAVIGATION §2/§3; its anti-parallel-source laws re-derive
  D-024; its two-axis classification vocabulary
  (FACT/INFERENCE/HYPOTHESIS/PROPOSAL/UNKNOWN ×
  PROVEN/PARTIAL/MISSING/REJECTED/DEFERRED/SHOULD-NOT-ADD) is
  compatible with the intake verdict sets — adopted as this
  block's working vocabulary, never as repo law. Its §6.1 names
  two further research files
  (`CANONSIM_INTERFACE_ORIENTED_PROCEDURAL_COMPOSITION_RESEARCH`,
  `RESEARCH_PLAYER_DECISION_MECHANICS`) that were NOT uploaded
  this session — they stay outside the repo; recorded here so a
  future session knows they exist in the owner's corpus and join
  a synthesis only on the owner's call.
- **Landed:** D-156 (this verdict set) + this intake block + the
  five new source rows in REFERENCES §10 (the intake-8/9/10
  precedent: The Sims, Slime Rancher, Shrouded Isle, Heaven's
  Vault, Procedural Narrative Generation — RimWorld and the DF
  family already carry their rows). The build queue UNTOUCHED —
  nothing unpins, nothing reorders; the one genuine residue
  (alternate evidence routes / breadcrumb recovery) already owns
  its standing row (since-1, owner-gated), and every other
  build-grade-adjacent item routes to the standing owner-gated
  rows (bg-8/engine-1 for the LLM-eval half, res-1/world-2 for
  the future consumers).

The procedural-generation research routed (intake-16, D-157 — the
owner's «отработай по второму файлу» research call over the
uploaded `PROCEDURAL_GENERATION_RESEARCH.md`, the methodology
document's own §10 example now uploaded in its grounded later form
(the §13 spike rides the province nouns that landed with D-153);
the consult posture of the intakes 6..15: the external document
stays outside the repo, every load-bearing claim verified against
HEAD, and the three measurement claims RE-DERIVED by a read-only
probe over the committed province pack through the public API at
HEAD b48ab18 (the probe script an outside-the-repo sandbox driver,
the operator's Rule 9): 200 seeds → 200/200 distinct topology
probe signatures at the pack's own six claimed anchor sites, the
height dimension alone 200/200 distinct (the research's own probe
read 200/200 + 193/200 on its anchor set — same order,
at-least-as-strong on the committed anchors); 60 seeds → 60/60
distinct history signatures (kind/year/participants/places/hooks);
the 3-member faction probe 8 raw membership states → 3 distinct
probability outcomes across three parameter bands — the small
formula's per-cent floor measured, not asserted). The four domain
verdicts:

- **Topology — CONFIRMED, already standing practice.** The
  authored surface is compact by construction (the pack's own
  `worldgen` block: extent 144 / spacing 8 → 324 sites, six
  claims, capitals 3); the cost claim re-derives TECH_NOTES §12's
  owned ladder (400→0.04, 2500→0.28, 10000→1.19 — the research's
  0.03/0.23/1.0–1.2 its own external measurements, intake-15's
  micro-drift (c) family; TECH_NOTES stays the single owner of
  numbers); the downstream consumer is landed (st-6a's derived
  prices, the province legs 345–705), roads-1 the parked one —
  the research's own §12 admits the dependency. PROVEN — nothing
  to build; the research confirms the standing shape.
- **History — CONFIRMED for causal anchors, the cap already
  authored.** The province chronicle's own shape (years 150,
  events_max 5 — event 0 world_formed, four history draws, the
  feud/quarrel collections) IS the sparse-consequential-anchors
  law; the anti-volume proposal re-derives the payoff-latency
  family (D-140: lore hooks ride templates + cause_hook, never
  bulk chronicle). PROVEN.
- **Social structure — PARTIALLY CONFIRMED, the research's own
  verdict.** The machinery inventory all landed (macro
  aggregation, group membership, the ratio formula, relations/
  pressure, the one-gate LOD, deterministic name streams — the
  condensation travelers the committed arming, D-154); the
  raw-combinatorics collapse now measured at HEAD (8 → 3
  outcomes); the structure/texture split is the standing LLM
  boundary (D-095's prose floor + D-150's doctrine). The one
  genuinely new item: the outcome-divergence experiment (vary one
  social edge, count divergent downstream event paths) — an
  evaluation discipline, not a mechanic; its natural first
  consumer is world-2 L2 slice 3 (the triangle), the ORDER owner
  decides. UNKNOWN kept honest: downstream story divergence is
  unmeasured in the real engine.
- **Resources — PROVISIONALLY HIGH-VALUE, still inference at
  HEAD.** res-1 todo owner-gated; the donor list matches the
  landed dives exactly (Kenshi/EVE/Albion/PoE/DW/Stellaris, the
  TASKS row's own record); the §13 spike is grounded on the
  actual province nouns (loc_crofts/bloom_heap, the Sarrow
  crossing, Malby + the half-pay keep — verified in
  entities.json) and its declared boundary matches the TASKS
  row's shape (source→flow→sink as pack data, aggregate macro
  cadence, irreversible consumption, derived price spreads —
  never a second economy engine). The spike's numbers (729
  authored configs → 55 event-path signatures / 21 compact player
  trajectories / 73 player-relevant transitions) are the
  research's own offline measurements — no code committed, by
  design; recorded here as external evidence, MISSING as runtime.
  The one-knob finding (source_yield/route_capacity/route_risk
  move the player signature; town_demand/garrison_demand/
  sink_priority do not in the compact band) is the spike's real
  contribution: rank authored knobs by causal-output density, not
  count — the gut-check family's metric form, res-1's own row
  the consumer. UNKNOWN kept: whether the leverage survives the
  real canonical event machinery.

The boundary law (§8/§11 — procedural fills causal gaps, LLM fills
representational gaps) re-derives the standing doctrine (INV-4 +
D-095 + D-150's may/may-not lists; the LLM-invents-a-road example
is D-052's closed world). The five failure modes (§9) are all
fenced by standing law (L9/L13 named consumers; the measured
collapse; INV-2 streams; the UNKNOWN discipline; the one-gate
LOD). The allocation table (§10) is a working map compatible with
standing law — never a new information owner (the methodology's
own §7 law). Zero build-grade items: no engine, no subsystem, no
queue change — the governing question "what should be
proceduralized" was already answered by the standing shape; the
research independently re-derives it with measured support. The
two §6.1-named research files (interface-oriented composition,
player decision mechanics) remain outside the repo — they join a
synthesis only on the owner's call.

The interface-oriented procedural composition research routed
(intake-17, D-158 — the owner's «отработай по второму файлу»
research call over the uploaded
`CANONSIM_INTERFACE_ORIENTED_PROCEDURAL_COMPOSITION_RESEARCH.md`,
the methodology document's §6.1 FIRST-named file — the owner call
that intake-16's tail note awaited; the D-150/D-155/D-156/D-157
intake precedent, the consult posture: the external text stays
outside the repo, every load-bearing claim verified against HEAD).
The research asked whether a small authored causal vocabulary can
produce materially different causal situations by fitting
reusable motifs to different worlds/relations/interfaces — without
a second simulator, weakened determinism, or abstraction ahead of
value. Two fresh measurements RE-DERIVED by a read-only probe over
the committed province pack through the public API (the sandbox
driver outside the repo, Rule 9): 60 seeds → **60/60 distinct
motif-binding sets** (the authored chronicle vocabulary fixed —
feud `war_fought` + quarrel `pact_signed`/`lineage_ended`, two
hooks; the participant pairs, places, years per-seed — the
collection motif's topology binding moves with the seed, 6
distinct region pairs over 3 regions), and the derived edge
prices → **54/60 distinct vectors, per-edge 6–7 distinct values**
(the five exits edges of the province graph, spreads 300–825
ticks — interface-local friction IS per-seed relation-local; the
collisions are the price's coarser projection, the same collapse
discipline intake-16 measured on the faction formula). The five
candidate verdicts (the research's own §24 table, the
PROVEN/PARTIAL/MISSING/REJECTED/DEFERRED/SHOULD-NOT-ADD axis):

| Candidate | Existing primitive | Evidence | Causal leverage | Abstraction cost | Disposition | Timing |
|---|---|---|---|---|---|---|
| Interface state | st-6a derived edge prices (L3); the `pair.<figure>.<axis>` homes; the macro aggregate surface; the erosion follow-ups | static interface facts PROVEN (the probe); dynamic route state (blockage/obstruction over time) MISSING-as-runtime | high where a consumer exists (travel legs, the planned flows) | a generic `InterfaceState` = SHOULD-NOT-ADD (L13: the pair-home + aggregate + follow-up families already carry relation facts through the one canon door) | PARTIAL | res-1 + the space-pack return (D-116) — both standing, owner-gated |
| Secondary topology | ONE canonical exits graph + L3 derived projections (the LOD zones, roads-1's L11 pass graph) + pack-data overlays (res-1's dependency graph) | the standing shape; distinct propagation rules already live in separate owners (macro cadence vs beat vs knowledge fold) | UNKNOWN for a second runtime graph — no false-coupling case demonstrated | high (a second authoritative world representation, INV-1) | REJECTED-as-subsystem | never, absent an owner-demonstrated coupling failure |
| Constraint propagation | drama-2 options (gate + weight, heaviest wins, declaration order, RNG-free); the arcs ORDER/GAP laws; the weighted weather chain; the ordered worldgen passes | every selection surface is a deterministic small mechanism | no propagation need in evidence | high (a solver family the corpus never asked for) | NO ACTION; WFC stays out (the research's own fence, the D-116 spatial family) | — |
| Causal motif fitting | the chronicle collections (authored motif + per-seed bindings, hooks → the director's buffer); res-1's declared shape (source→flow→sink as PACK DATA + aggregate macro-events + irreversible sinks) | PROVEN at genesis (60/60, the probe; intake-16's history twin); the runtime TRADE_BLOCK form is res-1's own row | high (the research's §8 thesis, confirmed in its genesis form) | a `MotifEngine` = SHOULD-NOT-ADD; cross-pack motif reuse is PACK-SIDE authoring under D-142's admission law | PARTIAL (PROVEN at genesis; MISSING-as-runtime where res-1 owns it) | res-1 + world-2 L2 slice 3/4 — the standing rows |
| Multi-node motifs | the collections' parent-map cause chains (L7); the director arcs; the commit-door reaction cascades; res-1's dependency graph | PROVEN as primitives in three separate owners | real but domain-owned | a unifying motif runtime would duplicate all three | NO ACTION (each domain owns its composition mechanism) | — |

The key reconciliation: the Townscaper transfer the research
proposes — authored primitives, compatibility constraints, fit to
current topology, canonical events, cross-system consequences —
is REAL in canonsim and ALREADY OWNED by the standing
architecture: the compact authored pack (INV-3) + the
deterministic generated substrate (worldgen, L11 derived) + the
per-seed bindings (the chronicle, the claims, the derived prices)
+ the one canon door (INV-1) + the commit-door consequences. The
research's own §22 scope guard (no `MotifEngine`, no
`ConstraintEngine`, no `InterfaceState`, no WFC, no schema/queue
change) holds verbatim at HEAD — each named anti-candidate is
fenced by standing law (L13's Rule-of-Three, D-116's
never-a-second-engine family, INV-1/INV-2, D-142's
core-ends/pack-begins line). The §12 alternatives comparison
resolves to the standing order: existing primitives + res-1's
pack-data shape (the smallest explanation that survives — the
probe shows the pattern already yielding distinct canonical
chains); more-authored-scenarios is the pack-side route (D-142);
full-procedural and LLM-generated were both rejected by the
standing verdicts (D-157; INV-4/D-052/D-095). The §13
counterexamples all fence: combinations-collapse (measured twice
now — intake-16's 8→3 and the probe's 54/60), prose-only
variation (the LLM boundary), private-knowledge leakage (L6/
EPIST-1 — the observer-opportunity machinery, the acquisition
gate and presence reads, never writes knowledge), pack-intent
violations (the pack-wins law: the derived price fires only where
the pack declares no override, D-132's
override-else-derived), nondeterministic ordering (the isolated
stream families + construction order, INV-2), debuggability (the
log IS the inspection surface — a generic motif runtime would
obscure exactly what the small mechanisms keep visible). The two
priority test cases route to their standing rows unchanged: res-1
(§14 — its declared shape already answers the research's flow/
route/shortage questions as pack data + existing doors; the
one-motif-many-bindings question is res-1's own evaluation
discipline when it lands) and world-2 (§15 — slice 3 the
triangle: faction pressure + the deep feud; slice 4 the calendar
+ the verdict call; the Sarrow Vale's river-crossing/
trade-junction structures already the committed surface). Zero
build-grade items: no engine, no subsystem, no schema change, no
queue reorder, nothing unpins. The methodology's §6.1
cross-synthesis with `RESEARCH_PLAYER_DECISION_MECHANICS` stays
OPEN — that file remains outside the repo, joining only on the
owner's call (the intake-16 tail note's second half, still
standing).

The player-decision-mechanics research routed (intake-18, D-159 —
the owner's «отработай по второму файлу» research call over the
uploaded `RESEARCH_PLAYER_DECISION_MECHANICS.md`, the methodology
document's §6.1 SECOND-named file — the owner call that intake-17's
tail note awaited, closing the §6.1 pair; the D-150/D-155/D-156/
D-157/D-158 intake precedent, the consult posture: the external
text stays outside the repo, every load-bearing claim verified
against HEAD 29b931b). The research asked whether the existing
deterministic simulation produces a compelling recurring player
decision loop (action → context → rules → world delta → knowledge
delta → system reactions → new information → next decision) or
only rich simulation state — VISION §6/§7's own "interesting
simulator: goal, not property" line, verified verbatim. Three
fresh measurements RE-DERIVED by a read-only probe over the
committed packs and playscripts through the public API (the
sandbox driver outside the repo, Rule 9):

- **The decision-loop census (day1_full, tavern, seed 125, director
  on): 56 events over 8 player steps — 13 PC knowledge records, 15
  suspicion deltas, 5 leverage mints, 1 expectation violation, 1
  rejected intent, the full fire chain (fire_started → fire_spread
  → smoke_rising → location_burned_out).** The loop's epistemic
  half runs end to end in the committed corpus: the failed steal
  (pickpocket_failed, the d100 check lost by margin 13) leaves FOUR
  witnesses holding `figure_reaching_for_purse`; the guard's
  violated expectation (purse expected carried, observed on the PC)
  mints the INFERRED `purse_missing` record — suspicion-from-
  absence, the P2d law; the watch's document check (failed by
  margin 1) teaches the PC `papers_demanded_of_pc_01`; the crowd's
  suspicion rises 35→40 on the pair axes. The drunk's coerce
  against the PC is REJECTED at the same door for
  `actor.leverage_over` — the action space is epistemically gated
  for every actor through the one mechanism, never two.
- **The removal test (the brief's own Test 6, executed literally):
  minus the steal steps, 56→31 events — ALL 15 suspicion deltas,
  ALL 5 leverage mints, the pickpocket risk, the crowd wariness,
  the document check and the expectation violation vanish; the
  arson chain survives untouched.** The social-risk half of the
  loop hangs on ONE verb; the loop decomposes into independent
  causal chains (the gut-check family's own shape). Minus the
  final wait, the burned-out ending loses 4 system events
  including the t=1080 watch handover (the crime_watch briefing
  transfer) — the timing window is load-bearing for the
  information half: waiting is never empty (rotations, decay and
  transfers keep firing, the D-038 mid-travel law's twin).
- **The travel-loop probe (province_smoke, seed 42): the derived
  legs 705/660/405/345 ticks; 14/14 PC knowledge records born on
  the five waypoint arrivals (the presence reads — who and what is
  where, the raw material for the next talk/steal/examine
  decision); the t=3240 NPC-to-NPC transfer fires mid-leg inside
  the Malby→Thornmill travel (the T1 pin).** Travel converts space
  into time cost AND an arrival-gated information harvest — the
  route choice is already a time/exposure/information trade, not a
  movement service.

The candidate verdicts (the brief's own A–G domains; the
FACT/INFERENCE/HYPOTHESIS/PROPOSAL/UNKNOWN axis kept separate from
the PROVEN/PARTIAL/MISSING/REJECTED/DEFERRED/SHOULD-NOT-ADD
disposition):

| Candidate | Existing primitive | Measured evidence | Decision created | Disposition |
|---|---|---|---|---|
| A. Time/Timing | beats/day phases/rotations; maclock-1 year cadence; st-6a prices; the director pacing clock | the wait window's handover + the mid-leg transfer | wait-vs-act changes rotations, decay, transfers, arrivals | PARTIAL — the pressure half PROVEN; the INFORMED half (enough information to time rather than gamble) rides world-2 L2 slice 4's calendar + the brief |
| B. Information/Knowledge | the knowledge system (fidelity/channels/salience/drift, EPIST-1); the brief; echo/traits; leverage; the OCC stale-view | every census delta is epistemic (4 witnesses, the inferred record, the papers lesson) | conceal vs disclose; coerce timing; act-on-stale-view (OCC) | PROVEN as substrate (FACT); the "most distinctive layer" hypothesis INFERENCE + PARTIAL — compellingness not decidable in track A |
| C. Social/Suspicion | pair axes + suspectaxis; trust-gated talk (≥20); leverage-gated coerce; factions' ratio dynamics | 15 deltas, 5 mints, the symmetric door rejection | spend-or-hold leverage; appease vs flee; the status-flip stakes | PROVEN — the crime chain is the v0 core; the faction-pressure half awaits world-2 L2 slice 3 |
| D. Travel/Geography | st-6a derived prices; the road pack's TRAVEL main loop; the province surface | the legs, the arrival harvest, the mid-leg transfer | route = time/exposure/information choice | PROVEN — the L1 instrument + the province surface; the dynamic route state rides the space-pack return + res-1 (intake-17's own verdict) |
| E. Resources/Scarcity | res-1's declared shape (pack data, macro aggregates, irreversible sinks, derived spreads) | none at runtime (the offline spike's 729→55/21/73 stays external) | not yet | DEFERRED — res-1 owner-gated, unchanged |
| F. Irreversibility | INV-1/INV-5; the leverage spend-consumes; drop_break; the fire chain | the fire chain's terminal location_burned_out; the spent cluster dies at its spend tick | spend-or-hold, break-or-keep, burn-or-not | PROVEN as law + live stakes |
| G. Experimentation | the log as inspection surface (mechanics.py, the dev side); belief tracking (records/echo/traits); the observe verbs | act-to-learn measured (the papers check buys the PC a fact at risk) | probe actions that buy information | PARTIAL — the dev instrument PROVEN; the player-facing feedback half UNKNOWN (presentation-1's) |

The key reconciliation: the brief's own core model IS the standing
architecture, layer by layer — PLAYER ACTION the intent door
(INTENT_SCHEMA), CONTEXT/RULES the pack preconditions against the
live projection (the OCC anchor), WORLD DELTA the canon event
(EVENT_SCHEMA), KNOWLEDGE DELTA the per-knower records (EPIST-1),
SYSTEM REACTIONS the cascade + urgencies + director hooks, NEW
INFORMATION the brief's scene_delta/recalled_facts (BRIEF_SPEC),
NEXT DECISION the state-gated action surface (actions.json through
the one door). The four-layer separation the brief demands (engine
mechanism / player-facing mechanic / systemic consequence /
presentation) re-derives the standing fences (L2/L6, D-095's prose
floor, INV-4) — "engine complexity is not gameplay depth" is
already the law's shape. The decision heuristic (REAL PROBLEM →
EXISTING PRIMITIVE → MEANINGFUL DECISION → MULTI-SYSTEM
CONSEQUENCE → NEW INFO → NEXT DECISION) re-derives D-142's
admission test + the gut-check family; the Do-not list (no UI,
meters, currencies, flags or verbs without a demonstrated decision
function; never state-space size as depth evidence) is L13/INV-3/
the measured-collapse discipline verbatim. The player-decision
inventory (the brief's research-order item 1) lives in the packs'
actions.json (INV-3), surfaced per-beat by the brief's
active_options block — no new owner.

The §6.1 cross-synthesis CLOSED (both files now routed; the
methodology's four questions): (1) the causal substrate yields
materially different states without a new generic runtime — PROVEN
(intake-17's 60/60 motif bindings + 54/60 price vectors);
(2) those states change the player's actions, risks, costs,
information and next choice — YES at the mechanism level, measured
here (the state-gated action space, the per-seed price vectors,
the route-dependent arrival harvest, the suspicion risk surface);
the EXPERIENCE-level verdict ("does it compel") is not decidable in
track A — the narrator/presentation circuit owns it
(presentation-1, engine-1's decision-input child; the SoW horizon);
(3) the two researches share ONE existing primitive — the intent
door + the log + the brief as the read-side bridge — not merely
similar vocabulary; (4) no new owner is warranted: every candidate
routes to standing rows (world-2 L2 slice 3 the faction triangle,
slice 4 the calendar; res-1 the scarcity half; presentation-1 the
compellingness half; since-1 the re-encounter information
surface). The two documents confirming one underlying need —
composition, content and presentation over new machinery — is
evidence FOR the existing primitives, never for a DecisionEngine,
GameplayLayer or new information owner (L13; the brief's own
fence). The one genuine residue: the brief's next-decision test
(Test 5) as an EVALUATION DISCIPLINE — when world-2 L2 slice 3
runs its outcome-divergence experiment (intake-16's residue),
count divergent NEXT-DECISION surfaces (the state-gated action
sets + the PC knowledge deltas), not only divergent event paths;
routes to the world-2 row's own evaluation half, the ORDER owner
decides. Zero build-grade items: no engine, no subsystem, no
schema change, no queue reorder, nothing unpins.

The persistent-groups / settlement-development research routed
(intake-19, D-160 — the owner's «отработай по второму файлу»
research call over the uploaded `Research task — Persistent
Groups, Camps, Settlements and Emergent Territorial
Development.md`; the D-150/D-155/D-156/D-157/D-158/D-159 intake
precedent, the consult posture: the external text stays outside
the repo, every load-bearing claim verified against HEAD 2b168e9).
The research asked whether persistent player-created groups and
player-driven territorial/settlement development are a natural
extension of the causal/event-driven architecture — not a set of
special subsystems — and what minimal universal substrate they
actually need. ONE fresh probe RE-DERIVED the whole surface
through the public API (the sandbox driver outside the repo, Rule
9): a tavern_pack copy carrying the settlement vocabulary as PACK
DATA — a second transitions layer `build`, a group with the tier
keys, a faction goal, an on_action witness reaction, an erosion
rule, a new buildable location + tool item + witness NPC, a
`raise_timber` action over the EXISTING ignite resolver — passed
the full pack-ci admission lint (M0: the settlement surface is
legal pack data, zero core edits) and ran seed 7 twice
byte-identically. The measurements:

- **M1 — construction as causal state (the fire chain re-declared
  as a second layer):** `timber_raised` (the player verb,
  cause-chained) → `build_started` (the spot birth
  `build.palisade: None → under_construction`, irreversible) →
  `build_spread` ×2 (the stochastic per-tick promotion — partial
  completion) → `structure_raised` (the SEEDED `usable` follow-up
  at t+15) → `camp_completed` (the halt flag at t+30,
  irreversible). The PC DEPARTED at t=59 mid-build; the entire
  chain (spread, usable, completed) fired after the departure —
  construction continues on world rules, never player presence.
- **M2 — the group tiers:** the cold aggregate `company_counts`
  (population 2, actor = the group id) at the crossing while the
  PC stood two steps away; the condensation `company_musters` at
  the warm-ring crossing (BOTH members' `member_of` births + the
  write-once tombstone); ZERO aggregates after the tombstone; the
  cold census `[1, 4, 4, 4, 4]` riding the year turns.
- **M3 — the group as actor:** five events with actor =
  `grp_company` — the two tier events plus three faction-goal
  `wait`s through the front door (`cause_intent: faction_0000`),
  fired at crossings while the PC was elsewhere. Group-level
  intent and member-level intent (the urgencies) ride the SAME
  door — one mechanism, never two.
- **M4 — visibility:** the build's knowers = the witness NPC
  alone (`same_location` minus the cause actor); the drunk two
  rooms away holds ZERO records (the blind-NPC law live at
  settlement scale); the `on_action` witness reaction fired
  (fear 0→5, one hop); the telling chain delivered the fact to
  the returning PC at fidelity `vague` (partial → decayed one
  step, channel `told`).
- **M5 — decay:** the rain crossing seeded the erosion; the
  counter-event at t+20 reverted `usable: True → False` (the
  works weathered while the PC was away) while the irreversible
  `camp_finished` survived — EVENT_SCHEMA §4's revert law live.
  The final fold: the camp's derived state = three spot props +
  `usable: False` + `camp_finished: True`; the watchman's
  `member_of`; the tombstone — settlement state IS the fold.
- **M6 — determinism + the resume door:** two whole runs
  byte-identical; the split run (interrupted after the arrival,
  before the build, at a clean drain boundary) byte-identical to
  the whole. One honest edge finding: a split taken INSIDE an
  autonomous silent tail shifts the next step's feed tick (the
  pipelined batch feeds at the step's own completion tick; the
  session feeds at the drain-end clock) — the resume law's
  equivalence class is the clean drain boundary, D-139's own
  record; a live-session semantic, not a determinism breach.
- **M7 — scale (a second probe):** 50 cold groups / 100 unborn
  members over 5 crossings = 250 aggregate lines (one per group
  per crossing), 3 per-member events total (their own warm-zone
  urgencies, never the group machinery), 294 log lines for the
  200-tick run — the D-112 cardinality law measured at
  settlement count: O(groups × macrobeats), never
  O(members × ticks).

The verdict set (the brief's own §1–§18 domains; the
FACT/INFERENCE axis kept separate from the disposition):

| Domain | Existing primitive | Probe evidence | Disposition |
|---|---|---|---|
| Persistent group / party | the group entity (one id, all tiers — D-112); the `member_of` door (join/leave/transfer, fold-validated, test-pinned); the tiers; the faction goal walk; per-member urgencies | M2 + M3 end to end | PROVEN as scaffold (pack-declared group + runtime membership); the player-FOUNDED entity MISSING — `apply_event` rejects unknown entities, the mint is st-5's entity-birth row; the membership VERBS (recruit/dismiss) missing — the door is open, no resolver writes it, one mechanic away (companion-1 / the first consumer) |
| Party→caravan→…→settlement population on ONE primitive | the anchor + members + tiers + the door — no specialization surface anywhere | the same group record served aggregate, condensation and door actor | CONFIRMED — a `PartyEngine` = SHOULD-NOT-ADD (L13; the named anti-candidate family) |
| Group dimensions (risk/greed/mobility/…) | per-entity status axes (D-006) + pair relations (P2a) + derived reads (L3) | the faction formula read the LIVE fold | MOSTLY over-modeling — each candidate must name its observable (L1); mobility is the anchor position (derived); the KeeperRL small formula is the anti-psychology-engine precedent |
| Group disagreements as first-class mechanics | goals/resources/relations consequences | — | REJECTED — stay ordinary consequences (the brief's own minimal-model preference; the crime chain is the measured instance) |
| Construction lifecycle | the transitions engine (spot births, spread, follow-ups, halt, blocked_by) + counter-events + the erosion family | M1 + M5: the full chain incl. mid-build departure | PROVEN — the fire chain IS the construction state machine; `planned`= `spot_available`, `usable`/`completed` = follow-ups, `damaged`/`abandoned` = counter-events/erosion |
| Settlement as derived state (no level ladder) | L3 folds; locations.flags; claims; the census | the final camp fold | CONFIRMED — `castle` = a derived classification, never an entity type |
| Settlement dimensions (food/trade/defense/…) | res-1's declared shape (source→flow→sink); the alarm/on_action; pair axes; the knowledge system | the probe's security/visibility/reputation halves | PARTIAL — the economic half rides res-1 (owner-gated, unchanged); every proposed meter owes the causal-justification test (L1) |
| Externalities | the reaction cascade + knowledge propagation + res-1's flows | the one-hop gossip + the telling | PARTIAL — the propagation machinery is universal; the price/scarcity half is res-1's own row |
| Visibility / information propagation | the knowledge system (channels, fidelity, salience, transfer decay, drift, expectations) | M4: blind/witness/told, fidelity decay | PROVEN as substrate — a `SettlementDiscoverySystem` = SHOULD-NOT-ADD (the per-knower index is the universal form) |
| Claims / ownership / control / legitimacy | position + presence (physical); pair relations + pack events (contested claims as relations) | — | UNKNOWN / DEFERRED — no canonical claim state, none demonstrated needed; L3 favours derived control; world-2 L2 slice 3 (the triangle's overlapping loyalties) is the natural first consumer, the ORDER owner decides |
| Conflict escalation ladder | the door + the cascade + leverage + the crime chain (arrest) + the director | intake-18's census (the same surfaces) | PROVEN as the standing shape — each rung is a pack-declared reaction/goal, never a scene graph; the anti-magnet law is L1 + D-005 |
| NPC-driven development | urgencies + factions through the door (an NPC goal whose verb IS the build action — expressible today); the erosion | the faction actor + the autonomous chain | PARTIAL — autonomous construction is pack authoring over landed mechanics; the "return to a changed place" beat measured in miniature (the works completed + weathered + told) |
| Decay / abandonment / succession | the erosion family (SEEDED counter-events); irreversibility; the id-survival law; append-mode logs + checkpoints | M5 + M6b | PARTIAL — decay PROVEN; succession/inheritance = pack event vocabulary over the pair/member doors, no new mechanic named |
| Content-pack independence | INV-3 + the admission lint | M0: the settlement passed pack-ci whole | PROVEN by construction — the named engines (Settlement/Party/Castle/Companion/BanditCamp) all = SHOULD-NOT-ADD |
| Determinism / replay | INV-1/INV-2; draw-free tiers; SEEDED follow-ups; the cursor | M6a/M6b byte-identity | PROVEN |
| Performance / scale | the cold tier + the census + the aggregates; the one-gate LOD | M7: 50 groups = 250 lines | PROVEN at the measured band — the distant settlement exists causally as counts, exactly the brief's requirement |

The final architectural question — can the group, the camp and
the fortress be manifestations of the same causal primitives —
answers YES on the standing substrate: `group + place + the
state-door + relations + knowledge + intents + events + the
macro cadence` are all landed, `structure` IS the transitions
layer (a mechanic, armed as data — M1), and the genuine gaps all
own standing rows already: **st-5** (entity birth — the
player-founded group/place), **res-1** (the material life of a
settlement), **world-2 L2 slice 3** (the claim/legitimacy first
consumer) + **slice 4** (the calendar), and the one
mechanic-scale verb gap (the membership writer — a resolver
family, companion-1's natural shape). The brief's §20 vertical
slice is exactly the probe's chain extended by those rows:
player forms a group (st-5) → divergent goals (factions +
urgencies, landed) → group acts without player (landed) → camp
(structures, landed) → another actor learns (landed) → external
response (landed) → deterministic/replayable (landed) → no
scripted scene (the standing law). Nothing in the finding
rewrites that slice's order; its validation target status holds.
Zero build-grade items: no engine, no subsystem, no schema
change, no queue reorder, nothing unpins — the research confirms
the architecture and routes its residue to the standing
owner-gated rows.

The content-archetype / pack-strategy framework research routed
(intake-20, D-161 — the owner's «используя research_method_v5.md =>
разберись что перенять можно, дополнить или улучшить… долгосрок
важен и качество» call over the uploaded `canonsim — Content
Archetype, Pack Strategy & Capability Audit.md`; the
D-150/D-155/D-156/D-157/D-158/D-159/D-160 intake precedent, the
consult posture: the external text AND the method file stay outside
the repo, every load-bearing claim verified against HEAD 362f167 —
1726+1 green, ruff clean, all three committed packs load-green
through the full admission lint). Unlike intakes 16..19 (mechanism
researches), this document is a FRAMEWORK: it proposes a durable
method for choosing, classifying and admitting future content —
"which candidates provide new architectural evidence, which are
reusable patterns or skins, what do they require, and which stay
deferred." The reconciliation therefore runs over the framework's
own §36 "what should become permanent" list (26 items), each
checked per the method's four questions (principle / existing
form / quality / transfer), with the combined-design question
answered by ONE parked consult card (below). The capability truth
table the document's §39.A asks for, verified at HEAD:

| Mechanism family | Verified state | Classification |
|---|---|---|
| The v0..phase-5 columns: determinism (INV-2/T1), event sourcing (INV-1/T2), knowledge/known_by, relations, states/transitions, crime/watch, urgencies, director, traits, factions/objectives, weather chain+erosion, worldgen, names, macro clock, reflection, retrieval, importance/metrics/brief | the phase gates' own measurements (ROADMAP §2) | PROVEN |
| The phase-6 pack surfaces: travel pricing (the road pack's main loop), pack CI/scaffold/doctor (all three packs green today), the AP-8/AP-9 crosswalk, authored-vs-derived toponyms (D-132's override-else-derived law) | iter-112/D-149 (the reskin day, 14m24s zero core edits); iter-117/D-152 | PROVEN |
| The scene/texture family: scene_detail, scene_texture + promotion, the session scene ledger, tombstones, echo | phase-4 gate (the 0-leak suite) + D-048/D-049; intake-19's decay measurement | PROVEN |
| Groups/LOD: the group entity + tiers + `member_of`, condensation, cold aggregates, mobility | intake-19's probe (D-160); the province pack the committed consumer | PROVEN |
| Single-committed-consumer surfaces: the `cultures` block, spine records, the condensation travelers, the price overrides | province-only today (slice 2, D-154) | LANDED BUT UNDER-TESTED — the document's own term, and a genuine sharpening: a mechanism's ARCHITECTURAL proof completes only when a second materially different pack arms it (the AP-9 precedent: "first committed consumer" is rung one, not the summit) |
| The pending family: resources/scarcity (absent from core — grep-verified), entity birth (st-5), membership verbs (companion-1), generated exits (roads-1), claims/legitimacy (world-2 L2 slice 3), the calendar (slice 4), the narrator half (engine-1/presentation-1), qa-1/ci-1 | every gap owns a standing owner-gated row | PENDING / OWNER-GATED — nothing is ACTUALLY-ABSENT-without-a-row (the queue discipline guarantees it); no LIKELY-NEW-PRIMITIVE is claimed, and the document's own guard ("not merely because authoring is inconvenient") holds — every 2026 intake's named-engine SHOULD-NOT-ADD verdicts are the counterweight record |

The verdict set over the framework's §36 items, grouped (the
FACT/INFERENCE axis kept separate from the disposition):

| Framework family (§36 items) | Repo owner / state | Disposition |
|---|---|---|
| The core thesis — "demonstrated compositional breadth of a domain-blind causal core"; surface vs causal archetype; proof value; novelty types (1, 20, 21) | D-146 (the loop-change law: a reskin twin proves nothing — the universal-core claim is tested by the loop change); L9; VISION §7's "T1 reskin only" row; the minus ledger's generic-mush row | OWNED — the substance is standing law, often stronger (measured, not classified); the falsifiable-proposition FORM and the litmus join the card |
| The capability discipline — proven/expressible/pending; implemented ≠ demonstrated generic; the evidence ladder (3, 25) | the intake verdict discipline (intakes 16..19: FACT/INFERENCE kept separate from disposition, measurements re-derived at HEAD, never trusted from text); TEST-1 | OWNED — the L0..L5 ladder vocabulary + the cross-context promotion condition join the card |
| The topology framework — spatial/social/information/incentive/conflict/power/institutional; decision friction; canon-vs-knowledge (8–15) | each dimension's standing system: travel graph + derived prices; groups + pair relations; channels/fidelity/salience/distance decay ("news rides the road"); factions + urgencies + expectations; crime + leverage + feuds; secrets + the leverage registry; institutions EMERGENT (intake-19's verdict — no institution system); decision friction = intake-18's measured next-decision loop (the removal test: minus steal, all suspicion/leverage deltas vanish) | OWNED — the seven-dimension consult read joins the card as a COMPOSITION checklist citing owners, never a subsystem proposal (the document's own §9.7/§12/§13 test-first guards re-derive the standing law) |
| The anchor ontology — mobility × persistence; absence as state (5–7, 16) | groups (mobile anchors), the write-once tombstone (destroyed-but-remembered), the worldgen chronicle (historical-only), erosion (decaying), since-1 (the return delta, parked) | PARTIAL — the anchor vocabulary joins the card; since-1 owns the read half |
| The loop/signature/counterfactual family (17–19) | the phase-5 exit criterion (3+ emergent chains); M3; TEST-1 (metrics from the log only, never LLM-judged); T8 director-off A/B; the `--systems-minus` arms; intake-18's literally-executed removal test | OWNED — and the transfer point is recorded: engine-1's validation inherits "prose is never proof" (the narrative-vs-behavioral signature split is TEST-1's own shape) |
| The portfolio family — orthogonality; behavioral yield per authored complexity (22, 23) | the floor is enforced (AP-1 budgets, the teleology gate, the reskin-day clock, the corpus-price discipline); the SELECTION question (which candidate diversifies the portfolio) owns no row | ADOPT-AS-PARKED — the genuine new residue; the card's portfolio read (below) |
| The admission test (24) | PACK_SPEC §3/§5/§6 + the ≤1-day budget — the document's own §31 orders using the repo's real rules, and they suffice (verified: no replacement caps needed) | OWNED |
| The order relationship (26) | the ORDER owner law; the nothing-unpins discipline | OWNED (the document's own §34 current-order protection re-derives it) |
| The heavyweight artifacts — the 22-column standing matrix, a standing capability-truth-table document, the 17-candidate catalogue (§22, §25, §39.C/F) | — | REJECTED as standing artifacts: parallel truth (D-024), premature per the document's OWN §34 ("do not prematurely commit to a large future portfolio before empirical evidence exists"), and the speculative-worldbuilding ban (§38, the D-022 law's shape). This block's tables are the one-pass form; the card is the durable form |

**The pack-candidate consult card** (the framework's crystallized
residue — PARKED; a future pack-slot opening or pack intake reads
this BEFORE a row opens; recalibrated by the first independent
multi-pack authoring experiment, the document's own §34 law; the
same consult posture as the minus ledger, the cost laws and the
encounter catalog — each line cites its owner, nothing restates):

1. **The proof-value proposition** (falsifiable, stated first): "this
   pack tests whether X emerges from A+B+C without D." A candidate
   that cannot state one is a reskin twin — the named zero-value
   shape (D-146). The discharged precedent: the travel-loop question
   ("a second setting authored within the contract and budget, zero
   core edits" — met by measurement, D-149).
2. **The causal-archetype litmus**: strip proper nouns, lore, visual
   style and franchise references — the candidate keeps its value
   iff a distinct combination of interacting primitives plus a
   distinct class of persistent consequences survives. Else it is a
   SKIN (presentation-level variation) or a MODULE (a reusable
   causal configuration enriching multiple packs — the
   radiant-template family, PACK_SPEC §11).
3. **The topology read** (each dimension cites its standing owner;
   the read is a composition checklist, never a subsystem
   proposal): spatial (the travel graph + derived prices); social
   (groups + pair relations); information (channels, fidelity,
   distance decay); incentive (factions + urgencies + expectations);
   conflict (the crime chain + leverage + feuds); power (secrets +
   the leverage registry); institutional (EMERGENT from groups +
   relations + factions — intake-19). Decision friction — the gap
   between preferring an action and executing it before the world
   changes — is the timing/access/information lens over the same
   owners (intake-18's measured next-decision surface; slice 3's
   experiment carries the census).
4. **The anchor read**: mobility (static / mobile / ephemeral) ×
   persistence (living / decaying / destroyed-but-remembered — the
   tombstone / historical-only — the worldgen chronicle). Absence is
   causally meaningful iff downstream behavior reads it (since-1's
   delta; the erosion counter-event — intake-19 M5).
5. **The novelty type**: primitive / composition / scale /
   topological / consequence — composition and consequence carry
   the value (L9); vocabulary novelty is the reskin minus.
6. **Portfolio orthogonality**: the standing behavioral coverage —
   the tavern (the social-crime loop, MICRO scale), the road pack
   (the travel loop, the settlement-to-region band), the province
   (worldgen + factions + cultures at REGION scale), the parked rows
   (grim: the intimacy/coercion line; sci-fi: the mapping class;
   pressure-city: the displacement law) — a candidate must diversify
   BEHAVIORAL coverage, never art direction; five packs differing by
   aesthetics is the named failure (the document's §29).
7. **Behavioral yield per authored complexity**: more distinct
   behavior from fewer authored primitives — the SELECTION metric
   (AP-1, the teleology gate and the reskin clock enforce the floor;
   this question is the ceiling).
8. **The evidence ladder** for every claim: vocabulary → declaration
   → execution → causal loop → persistence → cross-context. High
   proof value requires ≥ the loop rung; the cross-context rung
   completes when a SECOND materially different pack arms the
   mechanism. Prose is never proof (TEST-1; engine-1's validation
   inherits this law).
9. **The verdict vocabulary**: PACK / MODULE / SKIN / DEFERRED /
   NEW-PRIMITIVE-CANDIDATE — the last evidence-based and rare (the
   SHOULD-NOT-ADD family is the default counterweight; the burden
   of proof rides the proposer, never the status quo).

Refused at the door (the document's own cut list, confirmed against
repo law): no candidate evaluation NOW (the 17-archetype catalogue
stays unevaluated — speculative worldbuilding is banned, and the
parked rows already own the standing candidates); no new
matrix/truth-table document (this block is the one-pass form); no
runtime change, no phase opening, no gate bypass, no queue reorder;
no "politics/belief/maritime/group-as-location" systems (the §38
non-actions re-derive the intake-17/18/19 SHOULD-NOT-ADD records);
no replacement admission caps (the real ones suffice). The §37
follow-up iteration is NOT warranted as a separate row: this intake
is the routing, and the card's validation is bound to the standing
evidence producers — world-2 L2 slice 3's outcome-divergence
experiment (the next behavioral-evidence producer, already carrying
intake-18's next-decision census) and the first pack-slot opening
(pack-1 the first authored pack to run the full crosswalk
deliberately). Zero build-grade items; nothing unpins, nothing
reorders.

The unified-observatory / worldbuilder / agent-gateway research
routed (intake-21, D-162 — the owner's «используя
research_method_v5.md => разберись что перенять можно, дополнить
или улучшить… долгосрок важен и качество» call over the uploaded
`Architecture Research Task — Unified Simulation Observatory /
Worldbuilder / Agent Gateway.md`; the D-150..D-161 intake
precedent, the consult posture: the external text and the method
file stay outside the repo, every load-bearing claim verified
against HEAD 4459500 — 1726+1 green, ruff clean). Where intake-14
asked the SUBSTRATE questions (causal compression, simulation
levels, aggregation, stealth, materialization), this document
asks the OBSERVER-SIDE questions: how the one world is inspected,
explained, balanced, forked, authored, and safely operated by
both a human developer and an AI agent. The capability map (the
document's §12.A, its §9 four-question frame as the organizer,
verified at HEAD):

| The document's §9 question | Verified state at HEAD | Classification |
|---|---|---|
| STATE — what exists right now | the fold/projection (the runtime truth), `mechanics.py matrix` (the static wiring), the chronicler's `state_current`/`facts_summary` (offline), `digest.py` (the doc viewport) | PROVEN |
| CAUSALITY — why did this happen | the provenance family (`cause` + `cause_intent` + `cause_hook` — EVENT_SCHEMA §7: "enough to re-derive why"), M3 chain lengths, chron-2's genesis cause tree (parent maps + collections), `mechanics.py trace` (the shadow: fold deltas + knowledge mints + hook seeds + the director's beat decisions) + `why` (the hook postmortem), payoff latency | PROVEN per component — the document's `trace_event` unified view is a read-side convenience, not a principle gap: all four quadrants (causes / event / knowledge / effects) are log data already |
| KNOWLEDGE — why does this agent know / not know | knowledge records (who/channel/fidelity/at/source — the why-KNOWN and why-NOT answers are the record set plus its absence), the blind-NPC leak suite (0 leaks, D-094), L6/EPIST-1 + the STATUS FAQ law (the director reads observable state only; the folds never entropy inputs), `chronicle.py knowledge_summary` | PROVEN |
| COUNTERFACTUAL — what changes if X is altered | `mechanics.py blast` (two-arm same-seed: fingerprint EQUAL/DIVERGED + type/hook/director counter diffs), the harness arms (`--pacing`/`--directors`/`--systems-minus`), fold checkpoints (verify-by-refold, depth-4), T1/T2 replay, seed-range distributions | PARTIAL — the primitive exists; the first-divergence-event read and the branch-from-checkpoint form are the residues (below) |

The §6 three-class balance taxonomy maps one-to-one onto standing
instruments: mechanical correctness = the T-suite (door outcomes,
invariants, the stoplist) + the admission lint; statistical = the
balance-1 harness (1000-seed distributions, M1–M5, thresholds from
data D-019, payoff latency, beat tension); emergent = T8 chain
counts + the corpus reads + the heartbeat Layer-3 trend. The §9
18-surface list: 13 surfaces exist as named instruments, resources
waits on res-1's row, forks and emergent-pattern analysis are the
partial/parked items below. The §14 scenario walks: S3 (knowledge
asymmetry) PROVEN end-to-end (the fidelity ladder, drift families,
the settlement probe's visibility chain, the t=3240 mid-leg
transfer); S5 (LOD transition) PROVEN (condensation + member_of
births + the tombstone + the census + the id law); S4
(counterfactual) = blast plus the divergence-read residue; S1's
pieces proven separately (the crime chain, move with visual-only
sightings, the mid-build-departure precedent t=59) but never
authored as one pack — a composition question, not an
architecture gap; S2's economy half is res-1's own row (the
document's §15 law applies: the row owns the finding).

The verdict set (the method's four questions + the combined
design, the FACT/INFERENCE axis kept separate from disposition):

| The document's proposal | Repo form (principle → form → quality/transfer) | Disposition |
|---|---|---|
| §1–§4 the one-world doctrine (shared canon, deterministic ordering, LOD-as-resolution, knowledge-not-canon) | INV-1/INV-2 + the queue/door laws (D-037/38/39: bands, coarsest-first co-occurring ticks, OCC cause chains, tick-monotonicity) + the one-gate law/tiers/id law + L6/EPIST-1/channels/fidelity/decay — the collision cases resolve by standing law, never narrator-side; re-derives intake-14's confirmed record with zero drift | OWNED — CONFIRMED |
| §5 `trace_event` (the unified causal explorer) | principle: the log already carries the full causal graph, the explorer is a VIEW; form: provenance + the shadow trace/why; quality: release-equality pinned | PARTIAL — the single-event postmortem form (one command over one event id: its cause chain, its knowledge records, its cascade children) joins mech-2's ride (the standing mechanics.py-touch row), never a new row |
| §6 the three balance classes + the bug/imbalance/emergence verdict routing | the instruments proven (above); the routing is the reading discipline — T-suite first, then the harness distributions, then the corpus/T8/heartbeat | OWNED as instruments; the routing line joins the card |
| §7 true fork / divergence analysis | principle: same-prefix logs + deterministic ids ⇒ divergence is a READ; form: blast deliberately replays both arms from t=0 (no state fork — the resume door stays owner-gated); the checkpoint substrate landed (depth-4) | PARTIAL — the first-divergence read (first differing event, then the amplifying chain) routes to world-2 L2 slice 3's outcome-divergence experiment (its natural first consumer, already carrying intake-18's next-decision census form); branch-from-mid-run rides the owner-gated resume door (§7's own record) |
| §8 Worldbuilder as interface over the pack layer | the Phase-6 litmus PROVEN by measurement (D-149 reskin day 14m24s zero core edits; the province pack at pack scale); scaffold/doctor/lint + the admission rungs (D-152); mode G drafts offline through pack CI (VISION §4, PACK_SPEC); the impossible-authoring list = the admission lint + INV-3 + the author prohibitions | OWNED (the data-driven claim) / the UI DEFERRED to the SoW horizon (bg-6/presentation-1 — the document's own schema/data/tools/runtime split re-derives the repo's law) |
| §9 the Observatory convergence | principle: convergence at the CONCEPT level (four questions), never the tool level; form: each question owns proven instruments; transfer: engine-1's validation asks exactly these four — the frame joins the engine-1 consult material (the intake-20 card posture) | ADOPT-AS-CONSULT-CARD (below); the God Tool and any standing truth-table document REJECTED — parallel truth (D-024), and the document's own §12.C guard re-derives the refusal |
| §10 the Agent Gateway | principle: the agent uses the same authoritative interfaces, no bypass, owner gates on mutation; form: the doors + the D-055 file-contract family (A narrator, C parser, presentation-1 the fourth instance) + testproto's three layers (D-098) + the closed write path (INV-1: the log writer the only canon path) + "prose is never proof" (TEST-1) + AGENTS.md's iteration protocol (the dev-time gateway IS the standing law); the candidate capability list maps: inspect/query/trace/explain → mechanics, query_knowledge → the records, simulate/replay/checkpoint → the Simulator/T2/scripts, fork/compare → blast + arms, measure → metrics/harness, validate_pack/lint → the admission lint, propose_patch → the iteration protocol | OWNED at the law level — CONFIRMED; the SoW-facing formal surface rides engine-1/presentation-1/bg-6 (owner-gated, testproto the standing protocol); nothing to formalize now |
| §11 the emergent-behavior detector family | principle: surface behavior worth human inspection, never judge it; form: the teleology gate (dead event types = the "never happens" detector, at admission), the harness distributions ("too often"), the corpus growth law (measured failure, never imagination); the too-early/too-late/narrow-seed/runaway detectors have no consumer yet | PARKED — the first consumers are the standing verdict producers (slice 3/4's calls, the phase-gate heartbeat); the first-consumer law (st-5's shape); no row created |
| §12.D concept canonization | World/Canon, Simulation-Resolution/LOD, Knowledge State, the trace family: already named (INV-1/D-052, the one-gate law, L6/EPIST-1, the provenance family); Observatory, Counterfactual Branch, Agent Capability Gateway: the umbrella names wait for their SoW carriers | 4 already-solved; 3 correctly DEFERRED — canonizing now would be label-matching (the method's own law, D-024) |
| §13/§16 the standing deliverable documents + a dedicated formalization iteration | every build-grade item owns a standing row or carrier; the ladder is complete, new work is owner-gated rows | REJECTED as a new row/phase — this block is the one-pass mapping, the card the durable form (the intake-20 precedent) |

**The observability consult card** (the crystallized residue —
PARKED; the engine-1/presentation-1 spec writes and the world-2 L2
slice 3/4 experiments read this BEFORE promising observability;
the intake-20 card posture — each line cites its owner, nothing
restates):

1. **The four questions** route every observability ask: STATE →
   the fold/projection + `matrix` + the chronicler's summaries;
   CAUSALITY → `trace`/`why` + the provenance family + M3;
   KNOWLEDGE → the records + the blind suite + L6/EPIST-1;
   COUNTERFACTUAL → `blast` + the harness arms + checkpoints.
2. **The verdict routing** for a surprising outcome: T-suite
   first (bug) → the balance-1 distributions (imbalance) → the
   corpus/T8/heartbeat (emergence); prose is never proof (TEST-1).
3. **The single-event postmortem** (trace_event's shape) rides
   mech-2's next mechanics.py touch — one event id in, the cause
   chain + knowledge records + cascade children out.
4. **The first-divergence read** rides slice 3's
   outcome-divergence experiment: count divergent NEXT-DECISION
   surfaces (intake-18's form) AND name the first divergent event
   + the amplifying chain.
5. **The agent-operates-the-same-interfaces principle**: dev-time
   = AGENTS.md itself; SoW-time = the D-055 file-contract family +
   testproto; worldbuilder-mode agents draft packs through pack
   CI, never the engine (mode G).
6. **The detector family** waits for its first consumer; the
   corpus grows from measured failure (§8.2's law), never
   imagination.

Refused at the door (the document's own cut list, confirmed
against repo law): no God Tool or unified observability UI now
(the SoW horizon owns surfaces; the dumb-terminal law); no
standing capability-truth-table document (this block is the
one-pass form, the card the durable form); no new
formalization phase or row (every item owns a carrier or a
standing row — slice 3/4, mech-2, engine-1, presentation-1,
bg-6, res-1, the resume door); no runtime instrumentation (the
D-118 shadow-replay law — the runtime is never instrumented);
no second engine, no unrestricted LLM mutation, no
UI-driven architecture (INV-4, the D-116/D-147 anti-pattern
family, the document's §12.C); no new label set over the four
already-named concepts (D-024).

Micro-drifts (the document vs HEAD): (a) its §2 assumes LOD is
always-on ("is the NPC active/warm/cold during the interval") —
the one-gate law holds the one-scene world while the macro clock
is unarmed (the tavern pack), LOD is live only in the armed packs
(road/province); the pack DECLARES the resolution, the engine
never assumes it. (b) Its §7 "true simulation fork" — both blast
arms replay from t=0 by design; branch-from-checkpoint is not a
surfaced operation (the resume door, owner-gated). (c) Its §9
"should eventually expose" list reads as a TODO; at HEAD 13 of 18
surfaces exist as named instruments, and the document's own §12.C
guard would refuse building the missing five as standing
artifacts before their consumers exist. No factual errors found
in the document's repo-facing claims. Landed: D-162 + this
block. The build queue UNTOUCHED — nothing unpins, nothing
reorders; zero build-grade items.

The ComfyUI / modular-architecture consolidation research
routed (intake-22, D-163 — the owner's «используя
research_method_v5.md => разберись что перенять можно, дополнить
или улучшить… долгосрок важен и качество» call over the uploaded
`canonsim_модульная_архитектура.md` — the CONSOLIDATED
multi-session report over the ComfyUI/node-graph question; the
D-155..D-162 intake precedent, the consult posture: the external
text and the method file stay outside the repo, every
load-bearing claim verified against HEAD 309aa17 — 1726+1 green,
ruff clean; where the report's own access record states most of
its consolidated sessions DNS-failed at clone, THIS session
verified from a real clone, BASE_COMMIT 309aa17, 180 commits on
`main`). Where intakes 14..21 each routed one fresh agenda, this
one routes a META-RESULT: the report is itself a reconciled
verdict set — the session's value is the verification against a
real HEAD, the sharpening of its one open claim, the resolution
of its six disputed items, and the routing of the surviving
residue. The verification map (the report's repo-facing facts,
claim by claim):

| The report's repo-facing fact | Verified at HEAD 309aa17 |
|---|---|
| Deterministic event-sourced core (fold(log), the one canon-write path, the queue key, the named RngBank streams) | INV-1/INV-2 law + the T1/T2 suite; 1726+1 green |
| Content fully modular (three packs; the second-pack criterion; modding measured) | `content/{tavern,road,province}_pack/`; PACK_SPEC's "second pack requires zero ENGINE changes" (§ the pack-3 mapping note); the reskin day D-149 — 14m24s, zero core edits, git-verified at iter-112 |
| Core split into single-owner modules; `sim/systems/` reserved; the core↛sim boundary | 38 `core/` modules; `sim/systems/__init__.py` the empty reservation; `tests/test_architecture.py` the boundary test (D-031/D-037) |
| The Systems DAG as data (reads/writes in rules.json, ambiguity fails at load) | TRUE with a SHARPENED SCOPE — `rules.json::systems` carries reads/writes for the NINE original passes (time, position_visibility, relations, knowledge, states, fire, crime_watch, director, notes); the newer families (weather, travel, echo, traits, cultures, names, budget + the macro/lod/factions wiring) declare heterogeneous top-level pack blocks + per-family lint + code-owned wiring — the uniform form does NOT cover them |
| CLI observability (matrix/trace/why/blast; pack_doctor; balance_harness) | verified — the four subcommands at `scripts/mechanics.py`; NO viz subcommand exists (the report's tooling gap accurate at HEAD) |
| Kernel↔periphery split (stdlib-only, ports, the abstraction gate; frontend-agnostic, dumb terminal; the file protocol) | BLUEPRINT L13/L11; VISION the dumb-terminal law + §7's overrated theses; the D-054/D-055/D-062 file-contract family |
| Presentation in the backlog, owner-gated | `engine-1` + `presentation-1` (TASKS), `roads-1`/`res-1`/`pack-3`/`pack-4` standing — the rows live in TASKS.md, STATUS's Next step pins the ORDER (the report's "STATUS.md among the rows" is the drift, below) |
| The pack-DSL growth paths (abstract + copy-from, per-category split, append-composition) | PACK_SPEC's inheritance sections (the D-142 guard family) |

The verdict set (the method's four questions + the combined
design, the FACT/INFERENCE axis kept separate from disposition):

| The report's finding | Repo form (principle → form → quality/transfer) | Disposition |
|---|---|---|
| Node-graph as RUNTIME — rejected | principle: a graph runtime either breaks `state = fold(log)` or wraps resolvers in nodes (graph for graph's sake); the execution-order contract lives in DATA (the queue key + the pack-side DAG lint) — a UI-side duplicate is a second truth; form: INV-1/INV-2 + the queue laws + VISION §7's "engine fits any world" row + the no-second-engine law (the D-116/D-147 family); transfer: none wanted | CONFIRMED — the report's rejection re-derived from standing law, zero drift |
| The replaceability reframe (canonical engine → explicit contracts → projections/protocols → interchangeable editors/debuggers/frontends/agents) | principle: the ComfyUI effect worth keeping is ARCHITECTURAL REPLACEABILITY, not visual execution; form: the D-055 file-contract family (A narrator, C parser, presentation-1 the fourth instance) + the dumb-terminal law + L11 everything-rebuildable + the BLUEPRINT ports; quality: the file protocol carried phases 1..2 to their gates; transfer: the SoW frontends, the agent gateway (intake-21 §10 CONFIRMED), mode G's pack drafting | CONFIRMED — OWNED (the report's target formula restates the standing shape) |
| Three senses of modularity (A code / B mechanics / C authoring) | A: owned — single-owner modules, the stoplist, the boundary test; an `AbstractSystem`/plugin layer is L13's textbook violation (the report's own Do-not list re-derives it); C: owned-as-direction — presentation-1/bg-6/the SoW horizon; B: the genuine open question — the asymmetry verified above | A/C OWNED; B PARTIAL — the residue carrier (the card below) |
| The minimal system contract (identity + inputs/outputs + events in/out + RNG streams + pack surface + validation + diagnostics) | principle: a contract shrinks an agent's reasoning space by DECLARING the module's blast radius; form: the pieces exist per family — the DAG half (`systems` reads/writes), the RNG half (the RngBank stream families), the events half (the provenance family + the closed event vocabulary), the validation half (the admission lint + per-family lint), the diagnostics half (mechanics matrix/trace/why) — the UNIFORM per-system expression does not; quality: UNMEASURED — 128 iterations green without it, and the dev-time gateway (AGENTS.md + the reading gradient + mechanics.py + the stoplist) is the standing restrictor (intake-21 §10); transfer: the engine-1/presentation-1 spec writes, any future mechanic family; combined design: the report's own minimal shape (never manifest/lifecycle/plugin ABI) + the decomposition BEFORE any formalization | HYPOTHESIS — the 3..5 system decomposition (the report's list: weather/travel/factions/worldgen/knowledge) is the named next verification; parked on the card; NO new row (the first-consumer law) |
| The DAG visualizer (`mechanics.py viz` — Graphviz/Mermaid over rules.json) | principle: the graph is a PROJECTION of the pack, never a runtime; form: `matrix` already renders the wiring as a table; quality: no consumer named at HEAD; transfer: the engine-1 consult material; combined: rides mech-2's touch alongside intake-21's postmortem | REJECTED as a now-build — rides mech-2 IF a consumer names it; zero build-grade |
| Continue pack-ci/qa-1; wait on engine-1/presentation-1; never self-open a phase/gate | owned: D-152's admission rungs live; qa-1/ci-1 standing; the rows owner-gated | CONFIRMED — OWNED |
| The ComfyUI lesson (registration-based extension layer; the late subgraph/scope boundary debt) | principle: modules attach at EXPLICIT declared points, never core patches — and contracts must exist BEFORE the perimeter grows; form: the doors + the admission lint + hooks-as-data already practice it (the 2-place schema sync, load-time lint, per-family lint at landing time); quality: derived independently here — the lesson CONFIRMS the practice and adds the caution; transfer: the contract-formalization question (the card); ComfyUI is NOT a registered donor (REFERENCES = the owner's survey catalog) | CONFIRMED at the principle level — no donor registration (the owner's catalog policy; a deep-dive would restate owned law) |
| The method file itself (research_method_v5.md — what to adopt into the repo) | the v5 checks (the four questions + combined design, the FACT-vs-disposition axes, the reconciliation routing, the evaluation order, the hard limits) ARE the standing intake practice — intakes 14..21 the evidence (the verdict-table shape, the consult cards, the zero-build + queue-untouched laws); §6.1's two co-read files were routed (intake-17/18, the cross-synthesis CLOSED note) | CONFIRMED — OWNED, fully internalized; the file stays external (the convenience-copy law); nothing left to adopt from it |

**The modularity consult card** (the crystallized residue —
PARKED; the engine-1/presentation-1 spec writes and any future
contract/plugin question read this BEFORE proposing a layer;
each line cites its owner, nothing restates):

1. **The three senses stay separate**: code modularity is DONE
   (single-owner modules; `AbstractSystem`/`PluginManager`/
   lifecycle/DI is L13's textbook violation); authoring
   modularity is the SoW rows' own (presentation-1/bg-6,
   owner-gated); mechanics modularity is the only open third.
2. **The verified asymmetry**: the `systems` reads/writes DAG
   covers the nine original passes; weather/travel/echo/traits/
   cultures/names/budget declare their own top-level blocks +
   per-family lint. A decomposition COUNTERS what is already
   declarative per family before proposing any unification.
3. **The minimal contract shape** if the decomposition ever
   runs: identity + reads/writes + events in/out + RNG streams +
   pack surface + lint + diagnostics — never lifecycle, never a
   plugin ABI, never hidden callbacks (the report's Do-not list
   = L13 + the D-116/D-147 family verbatim; a module never
   creates RNG, writes the log directly, mutates others'
   projections, or changes execution order — the P0 surface).
4. **The agent-speedup claim is a HYPOTHESIS** with a named
   experiment (3..5 systems); the standing restrictor is the
   dev-time gateway itself (AGENTS.md + the gradient +
   mechanics.py + the stoplist); a contract layer must BEAT it
   by measurement, never by plausibility (the method's
   form-only ≠ PROVEN law).
5. **The ComfyUI caution**: contracts BEFORE the perimeter
   grows — the repo's own form is the landing-time lint (every
   new mechanic family lands its pack-block lint with it, the
   cultures/budget precedent), never a retrofit.
6. **The graph is a projection** (rules.json → the DAG → any
   view); the viz export rides mech-2's next touch if a
   consumer names it — never a runtime, never a second truth.

Refused at the door (the report's own cut list, confirmed
against repo law): no PluginManager/ModuleBase/AbstractSystem/
lifecycle framework/DI/100-field manifest (L13); no node-graph
runtime, no second engine (INV-1/INV-2, the D-116/D-147
family); no module-side RNG creation, direct log writes,
cross-projection mutation, hidden callbacks, order changes (the
P0 surface); no new viz row or build (the first-consumer law;
research does not build); no ComfyUI donor registration without
the owner's survey call; no queue reordering, no phase/gate
opening.

Micro-drifts (the report vs HEAD 309aa17): (a) its 171-commit
count was an earlier-HEAD snapshot — 180 at BASE (its own
disputed item #6, resolved as drift, not error); (b) the
owner-gated rows live in TASKS.md with STATUS's Next step
pinning the ORDER (the report's "STATUS.md among the rows"
wording); (c) its weather example (`reads: [macro_tick,
pack.weather]`…) is the PROPOSED contract form, not a HEAD form
— the actual shape is the pack's `weather` block
(event_type/initial/states) + `core/weather.py`'s own constants
+ the one-gate law; (d) its DAG claim's scope sharpened to the
nine original passes (above). No factual errors found in the
document's repo-facing claims. The report's six disputed items
resolved: the verdict-formulation split (1) by the table form
(per-finding dispositions, no single-word verdict); BASE_COMMIT
(2) by this session's real clone; the viz disagreement (3) by
the research-does-not-build law + the mech-2 ride; the
authoring-modularity centrality (4) — the reframe re-derives
standing law, the center of gravity stays the owner-gated SoW
rows; the contract-benefit confidence (5) stays HYPOTHESIS (the
honest label, the report's own admission); the commit count (6)
drift. Landed: D-163 + this block. The build queue UNTOUCHED —
nothing unpins, nothing reorders; zero build-grade items.

The world-execution / spatial-topology / social-information
architecture research routed (intake-23, D-164 — the owner's
«используя research_method_v5.md => разберись что перенять можно,
дополнить или улучшить… долгосрок важен и качество» call over the
uploaded `ARCHITECTURE RESEARCH TASK — Unified World Execution,
Spatial Topology, Social Information, Observability,
Counterfactuals & Agent Gateway.md`; the D-155..D-163 intake
precedent, the consult posture — the external text and the method
file stay outside the repo, every load-bearing claim verified
against HEAD 131c477 — 181 commits, 1726+1 green, ruff clean,
Python 3.12.14 the env pin). Where intake-14 asked the SUBSTRATE
questions and intake-21 the OBSERVER-side questions, this document
expands intake-21's own agenda with the WORLD-STRUCTURE side:
the execution model (intent lifecycle, conflict, re-planning),
the spatial topology (ontology, authored-vs-derived, extent and
boundaries), and the social-information ladder. Its observer-side
sections (§10..§19 observatory/gateway/counterfactual/balance/
emergence/worldbuilder) re-derive intake-21's routed record with
zero drift — not restated here; the world-structure half is the
fresh material below.

**The fresh spatial probe** (read-only, the public API, the
committed province pack, seed 20260918 — the intake-16..19 probe
posture; the document's §3.1 "the engine must answer mechanically"
list, answered):

| §3.1 engine question | The mechanical answer (measured) |
|---|---|
| Where can this entity go from here? | `exits(loc_riverroad)` = `[loc_weirstair, loc_keep]` — the AUTHORED exits graph (`entities.json::locations.exits`, linted symmetric) |
| What lies between these two locations? | the claimed lattice sites + the DERIVED price: riverroad↔weirstair sites 111→36 (4 cell steps) = 660 ticks; keep↔malby 300; crofts↔keep 510; riverroad↔keep 600 — `lattice_steps × step_ticks(150) + band_spread × climb_ticks(60) + river_endpoints × river_ticks(45)`, integer-only, draw-free (`core/travel.py`) |
| What region contains this location? | the typed claim read (`WorldModel.claim_value`, the closed field set biome/height/region/river): riverroad→hills, malby→forest, crofts→coast, keep height→6028 — region membership is a per-site MODEL field, projected into canon only through the claim births |
| What is adjacent? | the exits list (the pack's own declaration order — the WARM ring's derivation input, `core/lod.py`) |
| Is this destination reachable? | the exits-graph walk: 6/6 locations reachable from riverroad (province); the traversal topology of record is the graph, the price reads the lattice |
| What is immediately outside? | the lattice IS the extent: 324 sites = (extent 144 / spacing 8)² = 18×18 cells; no site exists outside it — the world's boundary is the pack-declared map config, mechanically closed (no undefined "outside the scene") |
| Determinism | regeneration from the same seed → equal sites/height/moisture = True (L11: the model is derived, rebuildable, never truth; replay rebuilds from the header seed + pack) |

The probe CONFIRMS the document's own key invariant — "if space
between authored anchors is mechanically relevant, it must have an
authoritative or deterministically reconstructable representation"
— is met by the repo's standing form: the lattice + place-1's
claim↔exits consistency law (`max_edge_span` 4, the pack's edge
contract) + the derived prices. No streets/districts exist and
none are owed (no consumer; the six-location province scale +
the group census + the cultures block carry the current world).

**The verification map** (the world-structure half, claim by
claim):

| The document's claim set | Verified at HEAD 131c477 |
|---|---|
| §1 one fact one authoritative owner; canon/derived/projection split | INV-1 + D-031 privilege separation (the log writer the only canon path) + single-owner modules + L3/L11 — zero drift |
| §2 intent lifecycle (assumed state, staleness, revalidation, rejection, re-planning, conflict, deterministic resolution) | CLOSED mechanically: proposal carries `based_on_event_seq` (the event count); OCC re-check at completion → `projection_moved` rejection with the breaking event's id as cause (`occ_breaking_cause` folds forward — attribution only); the windowed family (`leverage_over`/`echo_at_least`/`trait_held`) re-runs unconditionally (fold-read truths the event-count guard misses); player rejections = `intent_rejected` no-op events, never silent; autonomous failures = the noise floor (`core/urgencies.py`); re-planning = the goal ticker's next beat (p=100 compulsion the content-5 form); conflict resolution = the queue key `(tick, sub_order, actor_id, seq)` + first-commit-wins + `spot_available` (arson-on-ashes refused, pack-2) — INTENT_SCHEMA §4 owns the prose |
| §3.2 authored anchors vs derived structure; generated-space identity/replay | authored: locations, exits, claims, per-edge price overrides; derived: the lattice (seed+pack, deterministic, stable identity via the claim births, replay-stable); roads-1 owns the generated-exits half (iter-104's resolved read-path fork: the derived L3 read, no canon births) |
| §3.3 extent/boundary senses | the six proposed senses collapse to the repo's two authored forms + two derived reads: authored extent (map config) + reachable extent (the exits graph); simulated extent = the LOD zones (derived, the one-gate law); observable extent = position_visibility/acquisition; geometry NEVER assumed (integer topology; presentation never enters the engine) |
| §5 LOD + combinatorial growth sources | the one-gate law + zones + the D-112 aggregate law (log growth O(active + warm/cadence + aggregates) by construction); the complexity-audit residue stays parked with intake-14's (3) family |
| §6 time hierarchy + the no-silent-skip law | L4 layered clocks (maclock-1: tick / phases / beats / macro-year, one authority); crossings coarsest-first at co-occurring ticks (D-039); the macro aggregates + condensation answer the skip question at group scale (S5 PROVEN, intake-21) |
| §7 cross-system composition through explicit interfaces | the systems reads/writes DAG (the nine-pass scope, intake-22's sharpened asymmetry) + the commit door + event-driven reactions (D-037) + typed events + hooks-as-data — the document's "compose through authoritative interfaces" IS the standing shape |
| §8 the fact→knowledge→belief→goal→intent→action ladder | every transition owns a mechanical owner: channels saw/heard/told/inferred + fidelity exact/partial/vague (the decay ladder; lies = crafted records, D-008) → traits crystallization + counters (beliefwire) + reflection mint → urgency/faction goal entries → the door's gates (`trait_held`/`echo_at_least`/`leverage_over`) → the resolver. "Knows but not believes" = below trait threshold; "believes but not acts" = an unarmed gate; omniscience fenced by the blind-NPC leak suite (D-094, 0 leaks) + known_by + L6/EPIST-1; faction knowledge is NEVER group state (the ratio reads members' LIVE axes, D-006) |
| §13 metamorphic guarantees | T1 byte-identical + T2 replay + checkpoint verify-by-refold + the D-079 add-safety law (an added/removed entry shifts neither a later draw nor another's) + the sort laws |
| §20 dependency graph / blast radius | `matrix` (static wiring off the pack's own data) + `blast` (the runtime A/B) — the instruments exist; no separate graph abstraction owed |

The verdict set (the method's four questions + the combined
design, the FACT/INFERENCE axis kept separate from disposition):

| The document's proposal | Repo form (principle → form → quality/transfer) | Disposition |
|---|---|---|
| §1 authority map; no second simulation authority | INV-1/D-031/the fold — the anti-God-manager family (D-116/D-147) | OWNED — CONFIRMED, zero drift |
| §2 the formal intent-conflict taxonomy (independent/compatible/resource/state conflict, exclusive target, stale/invalidated intent) | principle: the taxonomy's WORK is already done by named mechanics (OCC, the queue key, spot_available, the noise floor); form: INTENT_SCHEMA §4 + the queue law name them; quality: the taxonomy adds labels, not leverage; transfer: the document's own "do not invent unless the repository demonstrates the need" clause refuses it | REJECTED as new law — label-matching (D-024); the ANSWER SET (each §2 question answerable by a named mechanism) is the residue, one card line |
| §3.1 spatial ontology as first-class concern | principle: topology-of-record + derived-prices-over-it; form: exits graph + lattice + claims + place-1; quality: MEASURED by the probe (six questions answered); transfer: roads-1's generated-exits half, slice 3/4's province scale | CONFIRMED — OWNED (the probe the fresh evidence) |
| §3.2 derived/generated spatial structure | the lattice + derived prices + roads-1's planned pass; deterministic, stable, replay-safe | OWNED; the streets/districts/traversal-regions vocabulary REJECTED — no consumer (the document's own §24 law: a gap is real only when the repo cannot answer) |
| §3.3 the six extent/boundary senses | the mechanical answers exist (authored extent, reachable extent, the zones, the visibility reads) | OWNED; the six-sense vocabulary REJECTED as new law — label-matching |
| §4 scenarios A–G | A: pieces proven separately (intake-21 S1); B: weather→travel PROVEN (weather-1 erosion + st-6a prices), the economy half res-1's own row; C/E PROVEN (intake-21 S3/S5); D: blast + the first-divergence read → slice 3 (intake-21's routing); F (urban topology) + G (political cascade): the primitives land (factions depth-6 DORMANT awaiting slice 3, leverage/secrets, the knowledge ladder, the census) — the cascades are COMPOSITION questions | ROUTED — F/G's stress-test QUESTIONS join slice 3's consult material (its factions + feud + outcome-divergence experiment the natural carrier); zero new rows (the document's own §15 law: the row owns the finding) |
| §5 LOD as execution concern | the one-gate law + zones + D-112 | OWNED (intake-14's confirmed record) |
| §6 the temporal-fidelity question | maclock-1 + the crossing discipline + the aggregates/condensation | OWNED — CONFIRMED |
| §7 compose through explicit interfaces, never hidden sync | the DAG + the door + event-driven reactions | OWNED — CONFIRMED |
| §8 knowledge/belief/goal/action separation; political asymmetry as stress test | the ladder verified transition-by-transition (above); the political cascade = slice 3's material | OWNED as law; the stress test ROUTED to slice 3 |
| §9 state-ownership matrix | INV-1 + single-owner modules | OWNED |
| §10..§19 observer-side (causality, validation, balance, counterfactual, emergence, worldbuilder, observatory, gateway) | intake-21's routed record — re-verified, zero drift: trace_event rides mech-2, the four-question card, blast/slice-3, the parked detectors, D-149/D-152, the doors + D-055 + testproto | OWNED/PARTIAL/PARKED exactly per intake-21 — not restated |
| §20 a dependency-graph abstraction | matrix + blast already answer reads/writes + the empirical half; a new graph = parallel truth | REJECTED (D-024) |
| §22 the scalability audit | intake-14's (3) parked family + the D-112 bounds + the measured curves (worldgen 10k/1.19s) | PARKED with intake-14 (unchanged) |
| §23 the standing capability matrix | the one-pass form is THIS block + intake-21's map (no standing truth-table document — D-024) | ROUTED into this block |
| §25 the 29-question decision set | 25 answered by standing law/probe in this block's tables; 4 ride standing carriers (conflict/re-planning detail → INTENT_SCHEMA §4; the fork → slice 3 + the resume door; emergence → the parked family; agent development → the engine-1 family) | ANSWERED |
| §26/§27 a dedicated formalization iteration | the ladder complete; the L2 wave plan (D-153) owns the remainder; every build-grade item owns a row or carrier | REJECTED as a new phase/row — the owner-gated L2 wave is the carrier |
| §28 the standing deliverable documents | this block + the card (the intake-20/21 one-pass precedent) | ROUTED |
| §29 the final principle (one canonical world → structure → execution law → mechanics → observability → gateway) | re-derives INV-1/2 + the one-gate law + L6 + the doors + the dumb-terminal family | CONFIRMED — zero drift |

**The world-structure consult card** (the crystallized residue —
PARKED; slice 3/4's experiments and the engine-1/presentation-1
spec writes read this BEFORE promising world-structure
capabilities; the intake-20/21/22 card posture — each line cites
its owner, nothing restates):

1. **The six engine questions are answered and answerable**: exits
   (authored graph) / between (claimed sites + derived price) /
   region (typed claim reads) / adjacent (the exits list) /
   reachable (the graph walk) / outside (the lattice IS the extent).
   Any future topology claim first names which answer it extends.
2. **The three-way existence distinction** the document's F
   scenario demands — exists / currently simulated at resolution /
   currently observable — is already mechanically separated:
   entities+canon (existence), the one-gate zones (resolution),
   position_visibility/acquisition (observability). Slice 3/4's
   experiments use it as the verification prompt (the
   riot-while-elsewhere form).
3. **The §2 answer set**: every intent-lifecycle question
   (staleness, revalidation, rejection, re-planning, conflict)
   resolves to a named mechanism — OCC + `projection_moved` + the
   queue key + `spot_available` + the noise floor + the beat
   re-roll (INTENT_SCHEMA §4 the prose owner). A new conflict
   taxonomy must demonstrate a case these cannot express.
4. **The social-information ladder is closed end-to-end**: fact →
   channel/fidelity record → trait crystallization (+counters) /
   reflection → goal entry → door gate → action. The political
   cascade (scenario G) composes these — never a politics
   subsystem; slice 3's triangle is the first full arming.
5. **Scenario F/G as verification prompts** ride slice 3: the
   factions' ratio dynamics + the census + knowledge propagation
   (F); secrets/leverage + the fidelity ladder + faction goal
   intents at province scale (G) — the outcome-divergence
   experiment already carries intake-18/21's forms.
6. **No mechanically-meaningful empty space**: the lattice + place-1
   own the between-anchors law; roads-1 extends it to generated
   exits; a new spatial vocabulary (streets/districts/boundary
   senses) waits for a consumer that cannot be expressed today.

Refused at the door (the document's own cut list + repo law): no
new phase or formalization iteration (the ladder complete, the L2
wave plan the owner-gated carrier); no intent-conflict taxonomy as
law (label-matching, D-024); no streets/district/settlement
hierarchy or six-sense extent vocabulary (no consumer — the
document's own §24 "a gap is real only when the repo cannot
answer" law); no dedicated politics/city subsystem (the primitives
land, the composition rides slice 3); no dependency-graph
abstraction beside matrix/blast (D-024); no standing
capability-truth-table document (this block is the one-pass form);
no runtime instrumentation (D-118); no second engine / unrestricted
LLM mutation / UI-driven architecture (INV-4, the D-116/D-147
family — the document's §21 re-derives them all).

Micro-drifts (the document vs HEAD 131c477): (a) its §3.2 derived
structure list (streets, connecting edges, district topology,
traversal regions) reads as a proposal — the repo's actual derived
structure is the lattice + the derived edge prices + roads-1's
planned pass; (b) its §2 pipeline sketch names an "arbitration"
stage — the repo's form is the queue key + first-commit-wins, no
separate stage; (c) its §23 matrix row "Population" — the census +
condensation (D-112's counts-for-populations) carry the current
form; (d) its "Economy" row — res-1's own standing row (the dives
landed, the backbone stands). No factual errors found in the
document's repo-facing claims. Landed: D-164 + this block. The
build queue UNTOUCHED — nothing unpins, nothing reorders; zero
build-grade items.

## 7. Cross-cutting (the questions that span phases)

- **Do we ever need a real ECS?** Not in phases 0–2: the projection with
  entt-shaped sparse+packed storage and view queries (STATE-1) gives the
  ergonomics without the machinery. Revisit only if `perf-1` (10k-tick
  profile) shows view iteration dominating; even then, port shapes
  (smallest-pool-leads views, id+version handles), not a framework (D-012).
  Bevy's parallelism is irrelevant — a fold must be serial to be
  reproducible. **perf-1 ran (iter-30, `TECH_NOTES.md` §8): cost is
  event-linear with ~3 orders of margin at the phase-0 scale — the
  revisit is closed at v0.1 scale; no structural work warranted.**
- **The storage ladder** (STORE-1 — the ledger row owns the rungs):
  five rebuildable, none authoritative; the canon path touches only the
  first two (log → SQLite projection).
- **The determinism contract**: T1 byte-identity holds for the same
  environment (Python version in the header); the RNG fingerprint extends
  it to a cheap invariant check for every test. The four silent breakers,
  each with its named donor counter-example: wall-clock (MTTH), unsorted
  iteration (ai-town), float geometry in canon (Azgaar), unkeyed
  randomness (tracery/ink defaults).
- **The LLM boundary over time** (`ROADMAP.md` §1 owns the fork):
  track B exercises the circuit on DF Legends XML; the switch to our
  canon happened at the phase-0 gate. The named hazard is early
  integration (`TECH_NOTES.md` §5).
- **Scale posture**: phase 0 is one tavern, ~10 entities, 10^3–10^4 ticks;
  every donor discipline above was chosen to hold at 10^6 events (DCSS
  multi-stream at 150k LOC; C:DDA content at 111 categories; FTS5/vec at
  millions of rows). Nothing in the blueprint has a phase-0-only shape
  that must be rewritten later — the shapes are the scalable ones, only
  the constants are small.
- **Containers & physical persistence (stress-test resolutions,
  iter-11b; RATIFIED iter-79 — D-112).** The `in` relation: position may
  name a location OR a container entity; `carrier` is the npc-case of
  the same relation; presence/containment = the transitive closure
  (the carrier closure generalized); nesting depth is lint-capped and
  cycles rejected at pack load (the PACK-1 copy-from cycle contract)
  AND at the commit gate (D-035 — runtime puts can cycle what
  pack-load lint never sees).
  Additive — state values are pack payload (EVENT_SCHEMA §4), only the
  projection's position semantics generalize. **Prop birth ≠ entity
  birth:** a D-054 promotion births a PROP on the scope target — right
  for fixtures (the hearth), insufficient for portable objects (the
  axe must carry, drop, be stolen). Entity-birth promotion = the same
  door with pack grammar (the take materializes a pack-declared item
  entity at the scope target, carrier = actor) — deferred with the
  depth phase; no parallel write path.
- **No texture GC — never; append-forever campaigns (stress-test,
  iter-11b).** Runtime log compaction is INV-5-forbidden by
  construction; "GC" lives in derived stores (scavenge, DuckDB —
  phase 4); the ledger dies with the session (D-049); in-session
  boundedness is the brief window alone; a per-scope live-entry cap is
  a named contingency (L13 — only on measured need). Campaign
  continuation = one log per world, a session binding the projection
  checkpoint (D-023); the resume door (open a session over an existing
  log) is the named gap — owner-gated with the mediator boundary;
  segmentation is an owner gate (EVENT_SCHEMA §1), default never.
- **Read-side indexes (stress-test, iter-11b).** The assembler's
  per-beat full folds (the scene fold + `KnowledgeView` rebuild +
  `current_scene`) are O(N)/beat; the D-050 pattern extends to the
  read side at the mediator iteration (session-held scene tail +
  knowledge view + projection checkpoint) — the purity claim is about
  BYTES, not about the fold call, so caching is legality-preserving.

---

← Up: [`docs/BLUEPRINT.md`](../BLUEPRINT.md) · previous part:
[`docs/blueprint/phase0.md`](phase0.md).
