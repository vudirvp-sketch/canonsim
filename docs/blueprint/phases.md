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
3+ events without the player (`ROADMAP.md` §2). Real-world donors (Natural Earth / GeoNames) arrive as data — shapes
and metadata only, per `docs/ref/natural_earth.md` +
`docs/ref/geonames.md`; CC-BY sidecar at intake; fantasy content from
packs, never real-world toponyms.

**Groups & simulation LOD (stress-test resolutions, iter-11b; owner
verdict pending).** The LOD ladder above is a READ ladder; the write
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
**Arrival snapshot** (write side): entering a scene emits ONE
perception event → O(present) knowledge records with observable
markers (per-present-target expansion of the actor-held `knows`
template — the audience stays `actor`; additive per INTENT_SCHEMA
§7/§10); the read-side twin is the §1 entity-card
block. Spec home when its trigger fires: the GROUP_SPEC sketch
(`SPECS_BACKLOG.md`). **The template half landed iter-15 (D-056): the
expansion rides the move event's templates (INTENT_SCHEMA §7), not a
separate perception event — KI#43's grammar correction made the event
an implementation detail the pack does not need.**

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
  iter-11b; owner verdict pending).** The `in` relation: position may
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
