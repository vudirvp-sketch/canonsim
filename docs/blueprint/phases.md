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
