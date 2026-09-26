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
entity-card block. Spec home: absorbed into depth-7 — the SPECS_BACKLOG sketch row's
re-point; the mechanism owners `core/groups.py` +
`tests/test_groups.py`. **Landed iter-93 as depth-7 (D-127 —
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
- **Scene LOD (three zones).** The group macro-tick (depth-7,
`core/groups.py`) owns the group side;
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

**The research archive law (D-185; first landed as iter-140-memgc's D-173, restored iter-151 after a stale-base archive apply clobbered it):** this section carries the
phase-6 architecture AND the repo's research record. The durable forms
are: the consult cards (the pack-design consults of intakes 9/10, the
pack-candidate / observability / modularity / world-structure /
principle cards), the slice blocks + the depth audit + the verdict (the
world-2 records), and the intake stubs — finding → consequence →
consumer. The full one-pass records (the verified-at-HEAD tables, the
micro-drifts, the session narratives) live in git at the D-rows' commits;
nothing there is re-derived. STATUS Next step pins which card an opening
row reads; no agent opens this section's archive without a named
consumer.


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
**Re-entry (iter-131, the owner's re-verification call over the
re-uploaded donor blueprint): D-147's verdict set holds at HEAD
e7147df, zero new findings, NO ACTION** — the section-by-section
content match and the citation re-verification live in git (37bcf6b);
one pin strengthened since (micro-drift (a) self-resolved: the AP
crosswalk's enforcement rung now live, pack-ci iter-117/D-152, the
province pack's five spine records the first committed consumer).
Nothing re-routed; no new D-row; the queue untouched.

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
**Re-entry (iter-122, the owner's re-verification call over the
re-uploaded review): D-150's verdict set holds at HEAD 1a9efaf, zero
new findings, NO ACTION** — the section-by-section content match and
the code-anchor re-verification live in git (b48ab18); two pins
strengthened since (the D-151 gate verdict + the province pack; D-152
making verdict 3's closure cure live enforcement). The re-uploaded v2
methodology document re-derives intake-15's own confirmed record with
no new drift. Nothing re-routed; no new D-row; the queue untouched.

The causal-architecture research bootstrap routed (intake-14, D-155 —
the owner's 2026-09-18 research call; the consult posture; the full
one-pass record — the verified-at-HEAD tables, the micro-drifts —
lives in git at c699c4f). The doctrine half re-derived intake-13's
confirmed standing law with zero drift; the genuinely new material
was five architecture questions, all resolved against standing owners:
(1) causal compression CONFIRMED as standing practice, never as one
law sentence — L3 + the authored-facts-win boundary (the strongest
landed instances: st-6a's derived price law, the faction small
formula, the macro-year counter, the echo/traits read folds); the two
failure modes fenced (outcome-table explosion by L9/L13 — the
AFFORD_SPEC trigger-gated pack-lint clause; universal-model explosion
by authored-facts-win); damage-as-derived parked with the
combat-bearing packs. (2) Simulation levels CONFIRMED — one world,
resolution strategies, never second engines (the LOD one-gate law,
the D-112 cardinality surface, condensation; the separate-engine
family the named anti-pattern). (3) Large-scale aggregation UNRESOLVED,
correctly: the substrate landed (macro aggregates, the group as
intent-door actor, the cold census), the 1k–10k-actor claim unmeasured
and un-promised (only measured: worldgen 10k sites / 1.19 s,
TECH_NOTES §12); parked — the first combat-bearing pack decides
whether a benchmark row opens. (4) Stealth as a causal chain PARTIAL:
movement, perception, knowledge, reaction landed; emission/
propagation authored per-action (`drop_break`'s noise, the alarm's
heard channel), never derived attenuation — a first-consumer
question, no pre-work owed. (5) Materialization generalization
CONFIRMED at the law level: the D-054 slot shape (`None -> value`,
first-commit-wins, canon never redraws) is the PARENT LAW with four
landed instances (texture promotion, scene detail, names, member_of);
entity-birth promotion designed as the same door, deferred to st-5's
first consumer. The three parked patterns (the scale benchmark, the
stealth emission substrate, damage-as-derived) join the intake-9
parked family — named here so a future row finds them.

The narrative-design research dossier routed (intake-15, D-156 — the
owner's 2026-09-18 research call over the seven-source GDC synthesis
(RimWorld, Slime Rancher, the Sims, Shrouded Isle, Heaven's Vault, the
PNG survey, the DF panel); the consult posture; the full one-pass
record — the 18-law mapping table, the 7-gap verdicts, the NQ-01..10
metric mapping — lives in git at 1a9efaf). The verdict: the dossier's
18 proposed design laws RE-DERIVE the standing law families (L1–L14,
EPIST-1, D-005, the brief/knowledge contracts) with zero factual
drift — the mapping table cited the owners row by row, nothing
restated here (D-024). Of the seven gaps: five PROVEN as landed
instruments (the M-family + payoff_latencies + eventless_stretches +
mechanics why/trace/blast + the AP-9 spine), one PARTIAL (the
breadcrumb recovery half — since-1's own standing row), the
re-labelings REFUSED as second vocabularies (the composite
narrative_leverage formula, the "consequence half-life" — D-024/L13:
the components are already measured and reported). The NQ-01..10
metric vocabulary REFUSED as a second label set (the T/M families own
the metric namespace). The durable residues: since-1 confirmed as the
one genuine gap-row; the "mechanics becoming narratively inert" risk
named as the standing M-metric targets' own text (MVP_SCOPE §15);
REFERENCES §10 gained the five source rows; the methodology document's
process half already standing law (TEST-1 — prose is never proof).
Landed: D-156 + REFERENCES §10. Zero build-grade items; the queue
untouched.

The procedural-generation research routed (intake-16, D-157 — the
owner's 2026-09-18 research call; the consult posture; the full
one-pass record — the four domain tables, the probe protocol — lives
in git at b748923). Three measurements RE-DERIVED by a read-only
probe over the committed province pack: 200/200 distinct topology
probe signatures at the six claimed anchor sites (the height
dimension alone 200/200), 60/60 distinct history signatures
(kind/year/participants/places/hooks), and the 3-member faction
probe's 8 raw membership states collapsing to 3 distinct probability
outcomes across three parameter bands (the small formula's per-cent
floor measured, not asserted). The four domain verdicts: topology
CONFIRMED as standing practice (TECH_NOTES §12 owns the cost ladder;
the downstream consumer landed — st-6a; roads-1 the parked one);
history CONFIRMED for causal anchors with the cap already authored
(the sparse-consequential-anchors law; the anti-volume proposal
re-derives the payoff-latency family, D-140); social structure
PARTIALLY CONFIRMED — the machinery all landed, the one genuinely new
item the outcome-divergence experiment (an evaluation discipline, its
natural first consumer world-2 L2 slice 3 — consumed there,
iter-135); resources PROVISIONALLY HIGH-VALUE, still inference at HEAD
(res-1 todo owner-gated; the §13 spike grounded on the actual province
nouns). The volume-without-connectivity fence (intake-24's P6 cites
it). Landed: D-157. Zero build-grade items; the queue untouched.

The interface-oriented procedural composition research routed
(intake-17, D-158 — the owner's 2026-09-18 research call; the consult
posture; the full one-pass record — the five-candidate
PROVEN/PARTIAL/MISSING/REJECTED/DEFERRED table, the probe protocol —
lives in git at 29b931b). Two measurements RE-DERIVED over the
committed province pack: 60/60 distinct motif-binding sets (the
collection motif's topology binding moves with the seed) and 54/60
distinct derived edge price vectors (per-edge 6–7 distinct values —
interface-local friction is per-seed relation-local; the collisions
the price's coarser projection, the same collapse discipline intake-16
measured on the faction formula). The five candidate verdicts:
interface state (static facts PROVEN; the dynamic route state MISSING
— parked on the standing rows), secondary topology (the standing
shape; roads-1's L11 pass graph), constraint propagation (every
selection surface a deterministic small mechanism — owned), causal
motif fitting (PROVEN at genesis — the chronicle collections;
res-1's declared runtime shape), multi-node motifs (the primitives in
three separate owners; a unifying runtime REFUSED — L13). The
Townscaper transfer REAL and already owned: authored pack + generated
substrate + per-seed bindings + the one canon door + commit-door
consequences; every named anti-candidate fenced (`MotifEngine`,
`ConstraintEngine`, `InterfaceState`, WFC — the L13/D-116/INV-1
family). The two priority test cases routed to their standing rows
(res-1; world-2 slice 3 — consumed, iter-135). Landed: D-158. Zero
build-grade items; the queue untouched.
cross-synthesis with `RESEARCH_PLAYER_DECISION_MECHANICS` stays
OPEN — that file remains outside the repo, joining only on the
owner's call (the intake-16 tail note's second half, still
standing).

The player-decision-mechanics research routed (intake-18, D-159 — the
owner's 2026-09-18 research call; the consult posture; the full
one-pass record — the decision-loop census protocol, the A–G candidate
verdict table, the §6.1 cross-synthesis — lives in git at 2b168e9).
Three measurements RE-DERIVED by a read-only probe over the committed
packs and playscripts: the decision-loop census (day1_full, seed 125:
56 events over 8 player steps — the loop's epistemic half runs end to
end: the failed steal leaves four witnesses holding the
reaching-for-purse figure, the violated expectation mints the
INFERRED purse_missing record, suspicion escalates by family); the
knowledge/option surfaces probed at the committed band; travel
measured as the time/exposure/information trade (the mid-leg transfer
the T1 pin). The verdict: the recurring decision loop EXISTS in the
committed corpus (action → world delta → knowledge delta → system
reactions → new information), with the honest residues — the option
surface narrow at the probed band (re-measured by iter-137's
door-surface battery: exactly 1 of 6 door answers changes per ordinary
verb) and player-facing compellingness INV-4-fenced (presentation-1/
engine-1 + the SoW horizon own it, never a track-A row). The A–G
candidates: C/D/F PROVEN, A/B PARTIAL, E DEFERRED (res-1's own row),
G partial — the brief's core model re-derives the standing
architecture layer by layer; the Do-not list is L13/INV-3 verbatim.
The next-decision census form: consumed as iter-137's door-surface
battery (the standing depth-battery arm). Landed: D-159. Zero
build-grade items; the queue untouched.
schema change, no queue reorder, nothing unpins.

The persistent-groups / settlement-development research routed
(intake-19, D-160 — the owner's 2026-09-18 research call; the consult
posture; the full one-pass record — the §1–§18 verdict table, the probe
protocol, the three measurement sections — lives in git at 362f167).
ONE fresh probe RE-DERIVED the whole settlement surface through the
public API: a tavern_pack copy carrying the settlement vocabulary as
PACK DATA (a second transitions layer `build`, a group with tier keys,
a faction goal, an on_action witness reaction, an erosion rule, a
buildable location + tool item + witness NPC, a `raise_timber` action
over the EXISTING ignite resolver) passed the full pack-ci admission
lint — M0: the settlement surface is legal pack data, ZERO core edits
— and ran seed 7 twice byte-identically. The measured shape:
construction as causal state (the build chain continues on world
rules after the PC departs mid-build); the group tiers (the cold
aggregate at the crossing, the condensation with the write-once
tombstone, the cold census on the year turns); the group as actor
(faction-goal waits through the front door — group-level and
member-level intent ride the SAME door, one mechanism, never two).
The residues routed: claim/legitimacy → slice 3's contested-wergeld
vigil (the first consumer, iter-135); the M5 erosion counter-event;
the player-founded mint → st-5. The probe stands as F1's strongest
single proof (the corpus's most demanding composition question
answered with zero core edits). Landed: D-160. Zero build-grade
items; the queue untouched.

The content-archetype / pack-strategy framework research routed
(intake-20, D-161 — the owner's 2026-09-18 framework-audit call over
the uploaded capability-audit document (a FRAMEWORK, unlike the
mechanism researches of intakes 16..19); the consult posture; the full
one-pass record — the capability truth table, the 26-item
reconciliation, the 36-row verdict table, the micro-drifts — lives in
git at 4459500). The verdict set: the framework's core thesis (the
universal-core claim's demonstrated compositional breadth) confirmed
as D-146's own law; the capability discipline (proven/expressible/
pending; implemented ≠ demonstrated) confirmed as the intake verdict
discipline's standing shape; the heavyweight artifacts (the
22-column standing matrix, the standing truth-table document, the
17-candidate catalogue) REJECTED as standing artifacts (parallel
truth, D-024; speculative worldbuilding banned — the parked rows
already own the standing candidates); the admission test and the
order relationship OWNED (PACK_SPEC §3/§5/§6 + the ORDER owner law).
The durable form:

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

10. **The depth battery's intake-27 sharpenings** (the level-design
   consolidation, D-173; the card's own recalibration law applies): the
   pack-gate evaluation now asks (a) **name the reader** — every new event
   type cites its read surface (a projection consumer, a knowledge channel,
   a door check, a tale line, or a hook; zero readers = functionally dead —
   the 48-turns law, D-170's census law gone event-side); (b) count
   **differently-priced options**, never labeled options (static prices =
   the fictitious-choice symptom, the A–H B row's own measured shape);
   (c) the **top-LOD read survives the blur** — the critical path (who /
   where / what changed / why) reads at the coarsest LOD. The authoring-side
   companions held in the intake-27 block: the realization table (why
   exists / which layer / linked to what / what the reader understands +
   the removal test) and the motivation scope question (which player
   motivation does this pack serve — no answer → scope creep;
   presentation-1's lens, INV-4-fenced).

Refused at the door: no candidate evaluation NOW; no new
matrix/truth-table document; no runtime change, no phase opening, no
gate bypass, no queue reorder; no "politics/belief/maritime/
group-as-location" systems; no replacement admission caps. The card's
validation is bound to the standing evidence producers — the first
pack-slot opening (pack-1 the first authored pack to run the full
crosswalk deliberately).

Zero build-grade items; nothing unpins, nothing reorders.

The unified-observatory / worldbuilder / agent-gateway research routed
(intake-21, D-162 — the owner's 2026-09-18 «используя
research_method_v5.md => …» call; the consult posture; the full
one-pass record — the §9 four-question capability map, the verification
map, the verdict table, the micro-drifts — lives in git at 309aa17).
The §9 map (18 surfaces, 13 existing as named instruments) was CONSUMED
as iter-135's experiment design review; the detector family waits for
its first consumer (the corpus grows from measured failure, never
imagination); the §12.C guards re-derive standing fences (no God Tool,
no standing truth-table, no runtime instrumentation — D-118/D-024).
The durable form — the observability consult card (PARKED; the
engine-1/presentation-1 spec writes and any observability question
read this first; each line cites its owner, nothing restates):

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
3. **The single-event postmortem** (trace_event's shape) LANDED
   iter-163 as `why --event ID` (mech-2's build): one event id in,
   the cause chain + knowledge records + cascade children out.
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

Refused at the door: no God Tool or unified observability UI now (the
SoW horizon owns surfaces; the dumb-terminal law); no standing
capability-truth-table document; no new formalization phase or row;
no runtime instrumentation (the D-118 shadow-replay law); no second
engine, no unrestricted LLM mutation, no UI-driven architecture
(INV-4, the D-116/D-147 family); no new label set over the four
already-named concepts (D-024).

Landed: D-162 + this block. The build queue UNTOUCHED — nothing
unpins, nothing reorders; zero build-grade items.

The ComfyUI/modularity consolidation research routed (intake-22,
D-163 — the owner's 2026-09-18 «используя research_method_v5.md => …»
call over the consolidated multi-session report; the consult posture;
the full one-pass record — the verification map over a real clone
(BASE_COMMIT 309aa17), the verdict table, the six disputed items, the
micro-drifts — lives in git at 131c477). The report is itself a
reconciled verdict set; this routing verified it against a real HEAD
and resolved its six disputed items. The core reframe: the ComfyUI
effect worth keeping is ARCHITECTURAL REPLACEABILITY, not visual
execution — explicit contracts before the perimeter grows, modules
attaching at declared points, never core patches; the node-graph
RUNTIME rejected (the execution-order contract lives in DATA — the
queue key + the pack-side DAG lint); the minimal system contract shape
and the DAG visualizer ride the standing carriers. The durable form:

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
   view); the viz export LANDED iter-163 as `matrix --dag` (the
   rules.json::systems Mermaid projection, mech-2's build) — never
   a runtime, never a second truth.

Refused at the door: no PluginManager/ModuleBase/AbstractSystem/
lifecycle framework/DI (L13); no node-graph runtime, no second engine
(INV-1/INV-2, the D-116/D-147 family); no module-side RNG creation,
direct log writes, cross-projection mutation, hidden callbacks, order
changes; no new viz row or build (the first-consumer law held —
the export landed as mech-2's own build, never a new row); no ComfyUI
donor registration without the owner's survey call.

Landed: D-163 + this block. The build queue UNTOUCHED — nothing
unpins, nothing reorders; zero build-grade items.

The world-execution / spatial-topology / social-information
architecture research routed (intake-23, D-164 — the owner's
2026-09-18 «используя research_method_v5.md => …» call; the consult
posture; the full one-pass record — the §3.1 probe table, the §2
intent-lifecycle answer set, the verification map, the verdict table,
the micro-drifts — lives in git at e7147df). The §3.1 six engine
questions answered by a fresh province-pack probe; the §2
intent-lifecycle answer set closed (every question resolves to a named
mechanism — OCC + projection_moved + the queue key + spot_available +
the noise floor + the beat re-roll, INTENT_SCHEMA §4 the prose owner);
the F/G scenario questions routed onto slice 3 (consumed, iter-135);
the streets/districts/six-sense vocabularies REJECTED (no consumer);
the dependency-graph abstraction REJECTED (matrix + blast answer it,
D-024); the standing capability matrix ROUTED into this block + the
intake-21 map (no standing truth-table document — D-024). The durable
form:

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

Refused at the door: no new phase or formalization iteration (the
ladder complete, the L2 wave plan the carrier); no intent-conflict
taxonomy as law; no streets/district/settlement hierarchy vocabulary;
no dedicated politics/city subsystem; no dependency-graph abstraction
beside matrix/blast; no runtime instrumentation (D-118); no second
engine / unrestricted LLM mutation / UI-driven architecture (INV-4,
the D-116/D-147 family).

Landed: D-164 + this block. The build queue UNTOUCHED — nothing
unpins, nothing reorders; zero build-grade items.

The cross-domain principle-transplantation synthesis routed
The cross-domain principle-transplantation synthesis routed (intake-24,
D-165 — the owner's 2026-09-18 «проанализируй глубоко документ и
оцени…» research call over the uploaded synthesis document; the consult
posture — the external text stays outside the repo; the full one-pass
record — the P1–P6 verification map, the micro-drift list — lives in
git at 90c04fb). The six named principles content-matched against the
routed records: ALL OWNED (each re-derives standing law with its
measured quality); the P2 universalization and the knowledge-closure
slice refused at the door (no substrate — the first-consumer law); the
names-as-law refused (label-matching, D-024). The durable form:

**The principle index card** (the crystallized residue — PARKED;
the future intakes' pattern-matching step ("Form: does an
existing primitive express the same shape?") and the res-1/
pack-4/world-2-slice-3 evaluation disciplines read this; each
line names the owner, nothing restates):

1. **Dual projection** → L3/L11/L6 + the brief's never-invent
   law; the landed projections: brief / KnowledgeView / LOD /
   `known_by` / `live_leverage` / the derived prices. Fence:
   stored dual state that drifts (L3).
2. **Displacement + debt** → D-147's law (pack-4's design
   constraint), res-1's cycle, weather-1's erosion, the
   thermometer minus (D-134). Fence: universalized MUST forms;
   second meters.
3. **Causal motif** → D-158's table: the chronicle collections
   (genesis, PROVEN), res-1's runtime shape, pack-side reuse
   (D-142). Fence: `MotifEngine` (L13).
4. **Group-as-entity** → D-160's table: the group entity + the
   `member_of` door + the tiers. Fence: group dimensions without
   an observable (L1); scripted group AI.
5. **Gauge law** → REFERENCES §10's DD/FP law + D-134/D-147 +
   the card/delta split. Fence: aggregate meters.
6. **Controlled irregularity** → worldgen's `PASS_ORDER` (the
   relax pass) + place-1's consistency law + the reachability
   walk. Fence: volume without connectivity (intake-16).

Landed: D-165 + this block. The build queue UNTOUCHED — nothing
unpins, nothing reorders; zero build-grade items.

The re-verification consolidation pack routed (intake-25, D-166 — the
owner's 2026-09-18 research call over the three-document consolidation
pack re-asking intakes 13..19's sources as quality-open rows; the consult
posture; the full one-pass record — the ten-row verdict table, the two
probe protocols — lives in git at ed23c52). TWO fresh read-only probes
executed the pack's own two smallest-verification steps: the mid-chain
stop semantics MEASURED (day1_full seed 125 — each of the 8 player steps
answered by the door or the resolver on real state; the chain stops
cleanly, failure is canon) and the status census MEASURED (the
admission/status vocabulary — the UNDER_MODELLED class closed at load
by D-152's teleology rung; a runtime "I don't know" would soften the
closed-world discipline — an authoring failure must never become a
playable outcome). The dispositions stand: the pack's remaining
smallest-verification steps all decompose onto the standing rows' own
evaluation disciplines (res-1's vertical measurement, the slice
divergence experiments, the corpus + T7 family). PARTIAL as a standing
status: refused (0/48 consumers — the first separable-sub-effects
action decides, D-150's deferral). Landed: D-166. Zero build-grade
items; the queue untouched.

**The cumulative research reconciliation (iter-134, D-167 — the owner's
«согласно CUMULATIVE_RESEARCH_v2 (1).md работай» call; the intake family
4..25 taken as ONE body of evidence; the full one-pass record — the method
narrative, the cross-pollination prose — lives in git at 9cc3ee3).** The
closure form the method's own trigger awaited: the intake family 4..25
closed by its last two members, the phase ladder complete, nothing pinned.
The central question: what does the corpus taken as one body imply about
the capability frontier and the highest-leverage evidence-backed path?

**The fresh measurement — the arming census** (read-only, the
public API + the pack files; the frontier MEASURED, never
asserted — intake-20's own law: implemented ≠ demonstrated, the
proof completes when a materially different pack arms it):

| The landed, isolation-tested family | tavern | road | province | committed consumers |
|---|---|---|---|---|
| factions (depth-6, iter-92; 24 test pins) | — | — | ARMED (iter-135, D-168 — the triangle) | 1 (the census's zero-consumer family, armed same-pack) |
| names (name-1) · cultures (slice-2) · npc spines (AP-9, 5/10 cast) · groups + condensation (depth-7, the road-traffic group) | — | — | ARMED | 1 — the province-only family (intake-20's LANDED-BUT-UNDER-TESTED list, confirmed whole) |
| travel derived prices (st-6a) | — | ARMED | ARMED | 2 |
| weather (weather-1) | ARMED | ARMED | ARMED | 3 — promoted |
| the core families (worldgen, reflection, traits, retrieval, secrets/leverage, urgencies, on_action, echo, expectations) | ARMED | ARMED | ARMED | 3 — promoted |

**The cumulative findings** (established only by combination):

- **F1 — the frontier is composition-limited, never
  implementation-limited.** Every mechanism question the corpus asked is
  answered by a landed, isolation-tested family; the census shows the
  residue is ARMING (factions, 0 consumers at the census), PROMOTION
  (four families at one), and CONTENT (the pack slots) — never missing
  machinery. The strongest single proof stays D-160's settlement probe.
- **F2 — the corpus is saturated.** The intake family 11..25 (15
  distinct documents + 2 re-entries) closed with zero build-grade items
  every time; the marginal research value now lives in the OPEN ROWS'
  own evaluation disciplines. Re-open condition: a fresh question aimed
  at an open row's evaluation form.
- **F3 — the convergence: world-2 L2 slice 3 the highest-leverage
  proof** (six intakes' residues consuming ONE standing row; the slice
  arms the census's only zero-consumer family). CONSUMED: iter-135.
- **F4 — the promotion ladder is the content-side frontier**: slice 3
  armed factions 0→1 same-pack; the promotion events for names,
  cultures, spines and condensation are the FUTURE PACK SLOTS
  (pack-1/pack-4) — never more province arming; the pack-candidate
  consult card the selection discipline.
- **F5 — the SoW fence holds**: player-facing compellingness is
  INV-4-fenced; its owners engine-1/presentation-1 + the hardware arm.

**Should-not-add** (the combination's own list): no fresh research
capacity before slice 3; no factions arming spike separate from slice 3;
no capability-truth-table document (D-024); no res-1 pre-work; no queue
reorder. The verdict on the whole: CONFIRMED — the frontier established
(F1, measured), the path dependency-ordered (F3/F4); the corpus
discovered NO rowless gap. Zero build-grade items; the census table and
the saturation finding the durable residues.

**The triangle slice landed (iter-135, D-168 — the owner's
«теперь настала пора приступать к работе по планам» call, the
iter-118/119 precedent phrase; the census's only zero-consumer
family ARMED 0→1, F3's convergence consumed).** The factions
(the river guild / the old families / the half-pay garrison,
three group entities over the settlement cast — the budget
block's own prediction) read two axes at two thresholds: the
escalation ladder (fear at trigger 30 for the trade, 40 for the
trained watch — the same axis, the FNV cascade) and the
deep-history arm (the NEW `grievance` axis, decay 0 — the
wergeld law, injury's counter-event family — at the deliberate
deadband: threshold 50 over two members means BOTH elders must
grieve). The player's levers are the ordinary verbs, never
script gates: the fire family spikes fear (the alarm), and the
grief-wake reaction (`on_action.alarm_raised` → witnesses'
grievance +20, "the mill burned once before" — the numeric-home
law filtering to the seeded elders alone) wakes the feud. ONE
verb, MANY ROADS, each mechanically distinct: burning the
market tips the guild (Maren's fear, fraction 50, bar 20) and
wakes Wilmot (the alarm heard at Thornmill — the
riot-while-elsewhere form, intake-23's F prompt); burning the
keep tips the garrison (the anchor active while the runner
lingers) and wakes Garrick (the keep heard at the crofts); both
fires open the deadband and the families hold the vigil
(intake-19's claim/legitimacy FIRST CONSUMER — the contested
wergeld as ratio dynamics over live per-entity axes, never a
canonical claim state, exactly the L3-favours-derived-control
verdict). The deep feud history: the chronicle deepens 5→9
events over the same 150 years with the collection vocabulary
RE-CUT — feud roots = war_fought + lineage_ended (the blood
endings open feuds), quarrel = the pacts under them, exodus =
the foundings at the leaves — and the wergeld claim joins the
story-critical hooks (the sweep, the murmur, the count: the
feud's three living claims seeding the director's buffer). The
cause TREE lands in the log (the members chain to their nearest
lower tier, the roots to the previous top-level — the sagas
chain) and renders through the tier clauses + the year chain.

The composed outcome-divergence experiment (F3's evaluation
discipline, the sandbox driver per Rule 9 — seed 53, both arms
from t=0, the fork = take the lamp + burn the row): STATE +16
events, zero drops (the fire chain ×6, the grief, the council,
suspicion ×3, the take, a transfer, a look, a decay); CAUSALITY
the first divergence at the take (t=2) with the amplifying chain
rooted through the fork — the guild councils at t=3443 riding
`faction_0000` through the front door; KNOWLEDGE the runner's
records +4/−1 (the fire family learned, the lamp's presence
unlearned) and the next-decision surfaces diverged — the watch's
suspicion 0→30 (witnessed_arson), the runner's crime status
SUSPECT, the door's answers changed; COUNTERFACTUAL the
same-seed fork itself (fingerprints 0x0 vs 0x7). Intake-23's G
cascade named: arson → alarm → (fear | grief) → (the ratio | the
crime chain) — three systems answering one verb, the composition
the intake predicted measured live. The census recalibration
(intake-20's card input): factions 0→1 ARMED same-pack; the
promotion events for the four province-only families stay the
future pack slots (F4 unchanged). ONE forced core edit — KI#85
(the alarm fear spike now applies the ripple's numeric-home law:
an ambient knowledge-holder hears the shout but takes no fear
write; the province's market crowd at a burning location first
exercised the latent D-035 mismatch — the modularity probe's
sharpening finding, exactly F3's predicted shape; pack-data-only
held everywhere else). The both-arms corpus price: the calm vale
byte-identical without the entries (the D-108 law — the rolls
ride the isolated faction streams, the deadband the designed
rest state); the golden fixture regenerated 39→44 (+4 deep
history, +1 ramble — the wergeld count), fingerprint 0, the
tavern/road corpora byte-untouched.

**The calendar slice landed (iter-136, D-169 — the owner's
«продолжай работу по планам» call, the iter-135 precedent
phrase's continuation; the L2 wave plan's remainder, the
triangle's ratio dynamics gaining their seasonal cadence).**
Maclock-1's middle granularities: L4's layered clocks grown to
three tiers (micro-time, the SUB-YEAR calendar cadences,
macro-time — one authority). `rules.json::time.calendar`: named
entries `{every_ticks, event_type}` or `{every_ticks, cycle}`,
the cycle the phase pairs `{phase, event_type}` — each season's
turn renders its OWN tale line (the tale's readability surface,
never a shared template keyed on a raw id), the phases rotating
by pure arithmetic (`cycle[k % len]`, the run OPENS at cycle[0] —
the weather `initial`'s own law, the thaw the vale's opening
season, the wrap's thaw turning with the year). The crossing
law: the positive multiples (the scheduler rule, INV-2-clean),
fired coarsest-first at co-occurring ticks — the year before the
season, the season before the fair, the fair before the market
day, the market day before the rotation — within the calendar
the deterministic order `every_ticks` DESC then id. The lints:
the pairing law (the middle granularities hang from the head
block — a calendar without time.macro is dead data), the sub-year
law (every_ticks strictly below the cadence — the year clock
owns the year turns), the identity laws (the types unique, ≠ the
macro's and the weather's), the both-or-neither cycle refusal,
the emission witnesses (the teleology gate's reverse walk reads
the phase types). The weather's SEASONAL layer rides the
satisfied gate (this section's own law): `weather.seasonal.ride`
names a declared calendar entry — the chain's rolls MOVE to
that cadence's crossings (ONE roll cadence per family, the
reference never a declaration — "one clock, one cadence"'s
substance held by reference), and the per-phase
per-current-state weight overrides carry the D-030 asymmetric
data: the RISE breaks the sky toward storm from ANY state (the
meltwater weather), the long light carries NO override (the calm
rebuilds slow through the base weights — the dial never snaps
back). The phase at the roll is pure tick arithmetic (L3 —
`calendar_phase`, the fold never scanned).

The committed arming (the province): the market days 14400 (the
decan rhythm), the fairs 43200 (the month's weighing), the
seasons 129600 + [thaw, high_water, long_light, first_frost] —
every crossing beyond the day-scale corpus scripts' horizon BY
CONSTRUCTION (the weather-1 arming's own law: the golden bytes
untouched, the corpus price zero, the T1 pin green). The
composed YEAR experiment (province_calendar.json, seed 42, the
F3 four-read-surfaces form): 36 markets, 12 fairs, the four
seasons in cycle order, the year's turn (151 — the chronicle
binding), four weather rolls (the rise draws STORM — the D-030
read measured), the co-occurrence order pinned at day 90 (the
rise → its weather roll → the fair → the market — the
coarsest-first discipline over the whole family), the twin run
byte-identical, the tale rendering the calendar's lines while
the ambient weather stays canon-without-a-line. ONE forced core
edit — KI#86 (the erosion's seed-time gate): the seasonal ride
exposed a latent unbounded queue feed (a rule whose `from` no
entity holds still seeded an entry per changing roll; with the
ride cadence below the rule's `after_ticks` the queue chases the
crossings forever — the crafted forced-alternation test hung);
`erosion_due` gates the seed on the fold, the fire-time read
unchanged (the rain washes the smoke that was there when it
rained). The T7 playtest read (worklog iter-136): the year's
chronicle reads as a town's almanac — the calendar the spine,
the watch/talk texture the noise floor at the year scale (the
tale gate's day-scale tuning the honest finding, the tune row's
own question — never this slice's edit).

The world-2 L2 depth audit (iter-137, D-170 — the owner's
research call over the uploaded depth-audit method file; the
three lens documents — the Cadwell roguelike principles, the
Ingold Narrative-Sorcery discipline, the Haggis scene-change
material — external per the convenience-copy law, repository
evidence authoritative; doc-only, zero code, zero corpus price,
the Rule-9 runners' logs outside the repo; verified BEFORE
working at HEAD 4be2a17 — 1754+1 green, ruff clean, Python
3.12.14 the env pin). The method's question: is world-2 L2 a
genuinely deep second world — not a larger collection of
independent features, not a decorated reskin — evaluated as ONE
composed world over the four landed slices, never as four
checklists? The verdict call itself stays the OWNER's (the
two-level gate's level-2 question); this audit the material.

**The converged unit.** The three lenses, taken as claims and
tested, converge on ONE falsifiable definition none supplies
alone: depth = the changed NEXT-DECISION landscape per ordinary
verb. Haggis supplies the unit — complexification is a structural
change in the next decision (knowledge / options / constraints /
costs / risks), never event-volume growth; Cadwell supplies the
stake — strategic commitment means actions close futures, "not
merely add positive progress"; Ingold supplies the validity
condition — encounter-first robustness: a depth reading that
survives only the authored happy path is not a depth reading.
The operational form is the F3 four-read-surfaces experiment
EXTENDED with three read-only arms: the door-surface battery
(the door's own answers as the decision-landscape read), the
reorder arm, the calendar ablation — zero new instruments, the
standing experiment's own shape sharpened.

**The fresh measurements** (seeds 53/53/42, all read-only):

- EXP-A, the door-surface census (province_feud, seed 53, BURN
  vs CALM — the arson step alone removed): the burn's marginal
  product = +15 events over 13 types (the fire chain ×4, the
  alarm, the panic ripple, the grief-wake, the council, the
  knowledge transfer, the look, the decay, suspicion ×3) and
  EXACTLY 13 projection properties over six entities (the
  market destroyed irreversibly + the stall-row detail; three
  watchers' pair suspicion 0→30 + fear 39/39/9; the steward's
  grievance 35→55; the runner's crime status SUSPECT), knowledge
  +4 (the runner — the fire family) / +9 (each watch member — the
  figure-who-fired family). The battery: six fresh-run probes per
  arm, each reading the door's own answer — EXACTLY ONE of six
  door answers changes (the re-ignition: REJECT
  `target.spot_available` in BURN, ACCEPT in CALM — the burned
  spot is gone); the other five identical, the two rejections
  arm-independent state facts (the sergeant carries the pay tin
  at the keep; no flagged steal target on the mistress). First
  stream divergence: index 35, tick 2421.
- EXP-B, the reorder arm (seed 53, Thornmill-first — the runner
  meets the steward BEFORE the arson): the grief-wake IDENTICAL
  (the steward 35→55 — route-independent), the vigil deadband
  HOLDS (the smelter at 30, one elder short by the deliberate
  design), the council still fires, the tale coherent, the twin
  byte-identical. The one lawful difference: an NPC's own
  autonomous talk rejected at `target.same_location` — the market
  mistress seeking the departed runner, the intent door's
  uniform law (NPC intents refused exactly like player ones).
  The longer route (two added waits) grows MORE autonomous
  texture (76 vs 64 events): the world composes richer under a
  different entry order, never breaks.
- EXP-C, the calendar ablation (the year run, seed 42, the armed
  pack vs `time.calendar` + `weather.seasonal` stripped — the
  macro year clock stays in both arms): the stripped layers' own
  product = 57 events (36 market days, 12 fairs, 4 season turns,
  3 extra weather rolls, 1 ramble, 1 rumor) + 52 tale lines; the
  mechanical leverage BEYOND their own events = EXACTLY ONE
  second-order path — the rise's storm roll at t129600 (the
  D-030 asymmetric read) arms the storm-market murmur hook
  (weather-1's seeded consequence, D-133), the ambient quiet
  gate releases it at t520068 (Maren's ramble at the emptied
  stall row — the one ablated projection property, the
  scene-detail slot), the knowledge lands on three hearers (the
  runner, the sergeant, the crowd), one rumor told back to the
  source. The 48 market/fair turns: ZERO consumers, measured —
  no state, no knowledge, no door answer rides them.

**The A–H ledger** (the method's world-2 test, each half
measured, never asserted):

| Test | Verdict | The measured ground |
|---|---|---|
| A causal composition | CONFIRMED | one ordinary verb → the fire cascade + the panic ripple + the crime chain (suspicion ×3, SUSPECT) + the feud's grief (35→55) + the guild's ratio (the council) — three systems, one door |
| B decision-landscape change | PARTIAL | knowledge, risks, status: yes; options narrow — exactly 1 of 6 probed door answers; costs: no property in the delta (the lattice prices static) |
| C strategic commitment | CONFIRMED | the market burns irreversibly (the re-ignition door closed); the SUSPECT status persists; the deadband one fire from the vigil |
| D world-away-from-player | CONFIRMED | the Thornmill grief-wake while the runner stands at Malby (iter-135's F answer); route-independent in EXP-B |
| E encounter robustness | CONFIRMED at the measured band | one full reordering coherent; the corpus of entry states is since-1/qa-1 territory — the honest boundary |
| F temporal composition | PARTIAL | the tale spine + ONE second-order path (the murmur chain); the cadences' decision half (opportunity/cost/co-presence at the market days) unowned — the promotion/pack-slot question |
| G cross-pillar interaction | PARTIAL | rich at the triangle's vertex (weather × crime × factions × history per verb); the cultures/calendar pillars contribute spine + texture + one measured path |
| H counterfactual divergence | CONFIRMED | the same-seed fork: fingerprints 0x0/0x7, +16 events zero drops, the door answers changed (iter-135) + the BURN/CALM fork's 13-property delta |

**The principles, the five questions each** (the method's
mandatory analysis — principle / form / quality / transfer /
combined design, compressed to the table; form-match alone
insufficient, every row carries its measured quality):

| The principle (source) | The mechanism, source-free | The standing form | Quality, measured | Transfer / combined |
|---|---|---|---|---|
| strategic commitment (Cadwell) | actions close futures; the stake is the closed branch | the irreversible event family + the door's state tests | the burn closes the re-ignition, arms SUSPECT, the deadband holds | the vigil's deadband — commitment's own escalation surface (owned) |
| make-do under imperfect tools (Cadwell) | no dominant strategy without the world's friction | the door's requires/tests + the epistemic limits | the verbs compose with knowledge; the "no ideal tool" tension is authoring-side | the pack slots' authoring question (routed) |
| curated variety / vectors of mastery (Cadwell) | multiple independent understanding axes beat raw RNG | the pillar families + the read surfaces | the vectors exist (knowledge / relations / factions / history); the aha-measurement is compellingness — INV-4-fenced | presentation-1's half (fenced) |
| high contrast (Cadwell) | expected failure and earned success must read differently | the outcome grammar + the fear/grief/suspicion spikes | the spikes measured (39/55/30) | the ceremony half is render-side — presentation-1's |
| encounter-first robustness (Ingold) | scenes survive entry order | the door's uniform law + deterministic replay | EXP-B: one full reordering coherent, one lawful NPC rejection | the corpus of orders — since-1 + qa-1's (routed) |
| defensive validation (Ingold) | validity for ALL reachable states, not the happy path | the commit gate + the preconditions + the admission lints | the same_location / carries / uncarried rejections measured live in both arms | owned; the lints' own family |
| multi-source knowledge (Ingold) | critical knowledge via independent routes or deterministic recovery | the channels/fidelity ladder + the rumor chain | the murmur chain is a measured second route; the recovery question open | since-1's recovery half (routed) |
| path traversal + semantic checks (Ingold) | automated dead-end / contradiction search | blast + the first-divergence read | the fork read exists; the contradiction corpus is qa-1's | no new instrument (should-not-add) |
| objective → conflict → outcome → change (Haggis) | the beat's four-part shape | intent door → outcome → state_changes/knowledge → the fold | the standing event grammar IS the shape — no new entity owed | owned as substrate |
| complexification = decision-structure change (Haggis) | escalation changes the next decision, not the volume | the door-surface battery (this audit's unit) | EXP-A: 1 of 6 answers + 13 properties + the risk surface | THIS audit — the unit operationalized |
| consequential success (Haggis) | success can worsen the future | the failure-law family + irreversibility | the burn succeeds AND closes — measured | owned |
| motivation needs a runtime consumer (Haggis) | inert want/need is lore, not force | the consumer discipline (the census law) | want/need authoring facts confirmed; the calendar's 48 turns the fresh instance | owned as law, applied |

**The strong counterexamples searched** (the method's mandate,
each answered by measurement): many-events-unchanged-decision —
FOUND and named: the 48 market/fair turns, zero consumers (the
honest F residue); calendar-output-without-behavior-change —
found: one second-order path, not a landscape;
systems-firing-independently — the murmur chain is a measured
composition (calendar × weather × knowledge × rumor), the
cadences themselves do not compose yet; knowledge-that-never-
changes-action — NOT found at this band (the fire-family
knowledge rides the trust/suspicion gates that own the
talk/coerce surfaces); history-inert — NOT found (the wergeld
claims seed the director's buffer, the grief-wake consumes the
feud); success-leaves-the-future-unchanged — NOT found (the
burn closes and distorts); robustness-only-happy-path — NOT
found at the band (EXP-B). The reverse — simple mechanisms,
many futures — CONFIRMED: one verb + three systems + the
deadband; composition, not machinery, is the generator.

**The critical separation** (the method's mandate — no future
completeness smuggled into the depth definition): NONE of
res-1 / roads-1 / since-1 / pack-1 / pack-4 / engine-1 /
presentation-1 is a prerequisite for the world-2 depth claim.
res-1: useful, non-essential — the scarcity pillar is absent,
the claim does not rest on it. roads-1: a separate engine
capability — the lattice + the authored toponyms already
deliver the geography pillar (L1's own measurement). since-1:
the robustness corpus's future — E is measured at the band,
the corpus sharpens, never gates. pack-1 / pack-4: the
cross-context promotion, F4's own content-side question.
engine-1 / presentation-1: the SoW / presentation fence (INV-4
— compellingness undecidable in track A). The claim is
decidable on the current evidence; the rows sharpen future
depth, never the verdict's inputs.

**The verdict**: PARTIALLY CONFIRMED. The anti-collection half
is MEASURED — one ordinary verb composes through three systems
into irreversible, divergent, route-stable state; the
anti-reskin half is MEASURED — the L1 reskin day + the travel
main loop, the standing records. The "deep" qualifier's
DISTRIBUTION is the honest residue: the composition
concentrates at the triangle's vertex while the cultures and
calendar pillars contribute spine + texture + one second-order
path — "the weeks made explicit" bought the spine and one
vertex, not yet the distributed landscape. What the synthesis
revealed that no document alone did: the converged unit + the
battery protocol — none of the three sources supplied the
measurement form; the combination did, and it is the standing
experiment's own shape extended, never a new instrument.

Remaining uncertainty: compellingness (INV-4-fenced,
unchanged); the robustness band (one reordering measured — a
corpus is since-1 + qa-1's); the cadences' future consumers
(F4's promotion question, the owner's). Practical consequence:
NO ACTION on the queue — nothing unpins, nothing reorders; the
depth battery (the door-surface battery + the reorder arm +
the ablation) joins the F3 four-read-surfaces form as the
standing evaluation discipline for the future pack gates
(F4's consult card carries it — zero new rows); the runners
stay outside the repo (Rule 9). The smallest next verification
step: NONE owed for the verdict call itself — the materials are
complete in the measured band; if the owner weighs the
calendar's decision half first, the smallest step is arming
ONE consumer on a market/fair cadence (co-presence, travel
exposure, or a price read) — a BUILD question (the promotion
events), never a verification one.

Landed: D-170 + this block. The build queue UNTOUCHED; zero
build-grade items (the three probes read-only, their logs
outside the repo).

**The verification-lenses research routed (intake-26, iter-138, D-171
— the owner's «перед этим вероятно стоит рассмотреть дополнительно идеи
с файла VERIFICATION_LENSES_RESEARCH.md» call; the consult posture, the
research file external per the convenience-copy law; the full one-pass
record — the verification narrative — lives in git at 1b7666a).** The
document's question: what reusable verification vocabulary and experiment
shapes should future research use AFTER the implementation claim has been
made — without a second simulator, a generic Verifier/Observatory runtime,
or a second source of truth. Its own verdict PARTIALLY CONFIRMED, verified
at HEAD: the mechanisms all owned (the FACT rows content-matched), the
missing piece the compact SELECTION GRAMMAR — which existing instrument
falsifies which claim. The adoption: `docs/TEST_PLAN.md` §9 (the
verification owner's surface) — the CLAIM PACKET + the claim-shape →
instrument selection table + the independent-re-derivation oracle law +
the order-probe contract law; research-derived, a routing aid, never a
gate.

**The lens/prism catalog** (the document's durable residue, held HERE as
the one-pass record — never a second standing document, D-024; a claim
packet's author picks from it, ≤3 lenses / ≤2 prisms). Ten LENSES — what
property is judged: canon/authority (one canonical truth; every claimed
result derivable from it); reachability/liveness (the behavior occurs
under ordinary valid inputs, live across a corpus); causal leverage (a
small change → materially different downstream canonical behavior);
decision/agency leverage (the changed NEXT-DECISION landscape); epistemic
closure (each actor knows only what its evidence path permits —
available ≠ understood ≠ communicable ≠ actionable ≠
actionable-in-time); stability/invariance (what must remain unchanged
under equivalent executions and irrelevant perturbations);
persistence/displacement (a meaningful consequence alters future state;
reduced pressure is displaced, never merely erased);
population/emergent behavior (over seeds and long horizons: never/rare/
common × early/on-time/late × broad/narrow × stable/oscillating/
runaway × local/distributed — never "the golden seed looks right");
attribution/explainability (causal trace backward — why did this happen?
— kept separate from dependency/blast forward — what could this change
affect?); boundary/boundedness (the mechanism stays inside its declared
authority, vocabulary, resource, and temporal limits under stress —
broader than error handling: locally valid but architecturally
unbounded is the target). Nine PRISMS — the controlled experiment:
remove (P1); one-knob perturb (P2); same-seed fork (P3); horizon
extension (P4); knowledge restriction (P5); composition crossing
(P6); order/permutation probe (P7 — contract-bound: where order is
semantic, invariance is NOT the oracle); stress corpus (P8 —
adversarial, edge, malformed, repeated, low-information,
simultaneous-reaction, refuses-the-subsystem cases); independent
re-derivation (P9 — a checker that shares the implementation's mistake
is not an oracle). Every lens and prism maps to standing carriers
(INV-1/INV-5, fold/checkpoint, pack lint, the blind suite, T1/T2, the
RNG fingerprint, the balance harness, longrun, mechanics trace/why/
blast, the deviation corpus, cap/floor tests, the F3 form + the depth
battery's three arms). The intake-21 four-question surface map (STATE /
CAUSALITY / KNOWLEDGE / COUNTERFACTUAL) stays complementary: it
identifies WHERE to look; the lenses WHAT property to judge; the prisms
HOW to perturb or compare it.

**Stale-at-HEAD corrections** (the document's snapshot predates
iter-135..137): its "no generic next-decision census" — the door-surface
battery (iter-137) IS the next-decision census form, landed as the
standing depth-battery arm (the RUNTIME census stays zero-consumer —
never a mech-2 rider, the first-consumer law); its "first-divergence
reporting missing as a reusable operator" — CONSUMED by iter-135's
composed experiment, the operator form still parked (zero consumers;
the synced mech-2 row never carried it — TASKS owns composition,
D-113); its "no common claim → oracle →
falsifier record" — iter-137's A–H ledger is the form's standing
instance. The persistence/displacement analysis surface stays PARTIAL
with zero consumers (no row owed until a consumer names it — the
first-consumer law).

**Refused at the door** (the document's own reject list + repo law): the
generic Verifier class, the runtime observer hook for tests, the second
stored truth table, the single universal quality score, LLM pass/fail
judgments for canonical behavior, the simulation engine hidden in
tooling, mandatory full-universe test runs (INV-1, INV-4, D-024); the
lens/prism NAMES as repo law (label-matching — the intake-24 precedent;
the names ride this block and TEST_PLAN §9's self-describing table);
the catalog as a standing document; REFERENCES.md as the surface; any
executable lens helper (zero consumers).

**The measurement obligation** (the document's own §14, now standing):
the next owner-gated build row (res-1 / pack-1 the natural candidates)
writes its verification plan as ONE claim packet — three lenses max, two
prisms max — and that run decides whether any executable lens helper is
ever warranted.

Landed: D-171 + this block + TEST_PLAN §9. The build queue UNTOUCHED —
nothing unpins, nothing reorders; zero build-grade items.

**The world-2 L2 verdict (iter-139, D-172 — the owner's convening
call, the session's second half; the verdict material COMPLETE in the
measured band — iter-137's own law: "NONE owed for the verdict call
itself" — the call now made).** The two-level gate's level-2 question
— is the deep second world's honest scope delivered (VISION §7's
twin: "deep unique worlds take weeks; the slices are the weeks made
explicit" — the weeks now spent)? — **ANSWERED: DELIVERED at the
measured band.** The verdict's ground, cited to the standing owners
(never restated — D-024): the anti-collection half MEASURED (the
depth audit's A/C/D/H ledger — one ordinary verb composes through
three systems into irreversible, divergent, route-stable state); the
anti-reskin half MEASURED (L1's 14m24s reskin day vs the
weeks-authored province — the spine, the vertex composition, the
year-run almanac, the T7 reads); the depth's DISTRIBUTION the
recorded residue (B/F/G partial — the concentration at the triangle's
vertex, the option surface 1-of-6 at the probed band, the 48
market/fair turns the one found-and-named counterexample). The
verdict's law: the gate asks the HONEST scope, never uniform
distribution — VISION §7's own reality row separates the reskin day
from the weeks, and the audit measured exactly that separation;
deferring until B/F/G close would be the completeness-smuggling the
audit refused (the critical separation: no open row a verdict input —
the claim decidable on the current evidence). The residue's routing:
the future depth consumers are the content-side rows — the pack
slots' promotion events (F4: pack-1 / pack-4), the cadences' decision
half a BUILD question (arming one consumer on a market/fair cadence —
co-presence, travel exposure, or a price read); world-2 NEVER
reopens for slices. The two-level gate COMPLETE: L1 the reskin day
(PASS iter-116, D-151), L2 the deep second world (DELIVERED iter-139,
D-172); the world-2 TASKS row done.

Landed: D-172 + this block + the TASKS row's done flip. The build
queue UNTOUCHED — nothing unpins, nothing reorders.

**The level-design & worldbuilding consolidation routed (intake-27, iter-140,
D-173 — the owner's «проанализируй документ и определи что из него можно
полезного перенять в проект и почему» research call over the uploaded
twelve-talk conspectus; the consult posture, the research file external per
the convenience-copy law; the full one-pass record — the verification map,
the verdict table, the instrument derivations — lives in git at 8f4fbd4).**
The document's question for the repo: which of its principles transplant
into a simulation core whose "level" is the event log, whose "player path"
is the intent door, and whose "renderer" is the brief — and what is already
owned law. The verdict: **PARTIALLY CONFIRMED — the doctrine overwhelmingly
OWNED** (the strongest cross-domain confirmation family since intake-16: a
spatial-geometry discipline and an event-sourcing simulation arriving at
the same laws — budgets, subtraction, LOD, authored-over-generated,
data-driven behavior). The residue: FIVE compact instruments adopted — the
reader law (every design names its reader; the brief's budget discipline
the standing form), the priced-option question (an option carries its price
in the same breath — the intent door's own shape), the top-LOD readability
question (the critical path reads at the coarsest LOD — the
almanac/chronicle surfaces), the realization table (why exists / which
owner / what it costs — the standing-rows discipline), the sacrifice
protocol (what a promise DELETES, not adds — the SoW debates' instrument) —
plus ONE proposal parked: the topology-aware hook distribution (a future
content row's material, never a standing row). The depth battery's
recalibration (the pack-candidate card's item 10) rides the same call.
Zero build-grade items; the queue untouched.
Landed: D-173 + this block. Detail: git at 8f4fbd4.

**The Stålberg-conspectus / transplantation-method output routed (intake-28,
iter-141, D-174 — the owner's «разбери 1231.md => что стоит перенять и
почему, зачем, как использовать и где это улучшит проект» research call over
the uploaded prior-session conspectus; the full one-pass record lives in git
at aa1097f).** The verdict: PARTIALLY CONFIRMED — the content overwhelmingly
OWNED (the cross-domain confirmation family's next member; the Townscaper
reconciliation itself intake-17's), zero factual errors in the load-bearing
repo-facing claims. The residue: ONE instrument adopted — the COMBINATION
FENCE (the fifth check's operational sharpening: a combined design carries
NO presumption of advantage, itself a separate hypothesis; the
mechanism-of-advantage decomposition + the combination-price question + the
Frankenstein test; the consumers: the engine-1/presentation-1 debates +
res-1's evaluation); the local-pattern→higher-order hypothesis routed to
res-1's aggregate macro-events + the cadences' decision half (never a row);
two recognition handles block-only (representation-shrink →
PACK-1/grammar snapshot/INV-3; vary-representation-preserve-substrate → the
scaffold law/cosmetic streams/promotion door); refused at the door: a
grand-synthesis law (the document itself refuses, D-024 agrees), methodology
codification (D-163), Stålberg-form features (intake-17's fence), a
Canonical-Visual-Memory row (presentation-1 owns the surface, INV-4-fenced).
Landed: D-174 + this block. The build queue UNTOUCHED — nothing unpins,
nothing reorders. Detail: git at aa1097f.

**The external-audit / roadmap-review output routed (intake-29, iter-142,
D-175 — the owner's «проанализируй текст далее и его предложения, если
согласен => нужно будет заложить в планы работу и соответственно
пересмотреть оный или типа того. по пунктам разбери что надо что не надо и
почему» research call over a prior session's DNS-less static audit of main
at 8f4fbd4e — re-verified at a REAL clone one commit ahead, AND with the
live suite the audit could not run: 1754 passed + 1 skipped, ruff clean,
verified BEFORE working; the full one-pass record — the ten-proposal
verification map, the per-proposal verdicts — lives in git at 15e568d).**
The verdict: the audit CONFIRMED on the facts; the foundation SUPPORTED —
no reopening of INV-1..5, the closed phases, or world-2. Adopted into the
rows: SIX contract sharpenings (res-1's mechanism split + irreversibility
split; roads-1's topology contract — the node question, the algorithm
naming, the invariant set, the LOD/autonomy falsifier; since-1's encounter
baseline — the epoch semantics + the scene_delta separation; companion-1's
no-teleport law; pack-1's consent split; ci-1 the recommended first owner
pick) + TWO rider rules (the pack.py split rides the first pack.py-growing
row, never a standalone refactor; the intake ADMISSION RULE — a new external
intake convenes only with a named open build row/standing debate it feeds +
a potential falsifier stated up front: new knowledge now comes from building
and measuring). The ORDER recommendation recorded, never enforced (D-113).
Landed: D-175 + this block + the six TASKS row sharpenings. The build queue
UNTOUCHED — nothing unpins, nothing reorders. Detail: git at 15e568d.

**The agent-dense v3 hybrid pack routed (intake-30, iter-154, D-187 — the
owner's archive-intake call over the uploaded `Canonsim_Agent_Dense_v3_hybrid`
package: an external three-layer re-consolidation of the already-routed
research corpus; the consult posture, the pack itself external per the
convenience-copy law; every active file read). The corpus map — nine of the pack's eleven
content units re-derive OWNED material, each already routed through
its intake (the pack is a sibling compression of the same sources, not new
evidence): `agent/00` (method + lenses/prisms + transplant filters) = the
intake-26 catalog above + TEST_PLAN §9 (D-171) + D-024/D-175; `agent/01`
(the findings ledger) = the iter-134 cumulative body (D-167) + the iter-137
three lens documents (D-170) + intake-24 (D-165); `agent/02` (architecture)
= intakes 13/14/17/19/21/22/23 (D-150/155/158/160/162/163/164); `agent/03`
(design/content) = intakes 15/16/18/20/27 (D-156/157/159/161/173);
`agent/05` (donors) = intake-11 (D-147) + the Kurvitz residue (D-186);
`agent/06` (worldbuilding constitution) = `docs/worldbuild/`
(`WORLD_AUTHORING.md` the repo's own compression of the same source — the
two are near-isomorphic, the repo surface wired and law-fenced, D-186);
`agent/07` + the manifests = package metadata, never repo material.
Stale-at-HEAD: the pack snapshot predates iter-145..147 (its donor mapping
marks res-1/roads-1/since-1 un-landed — all three landed). The structure
verdict: the pack's `agent/` layer — which declares itself the canonical
documentation layer for the corpus — REFUSED as a parallel authority
(D-024's single owner; the D-018/D-186 content-class law: engineering
concepts land surgically in existing owners, the D-186 directory exception
reserved for an owned domain model with NO existing owner — every domain
this pack carries has one; the iter-140/151/152 compactions would be
reversed); no `docs/agent/`; the pack's own manifest discipline (one active
owner per durable concept, sources preserved separately) acknowledged as
the same law NAV §3 and D-011/D-024 already own. The TWO fresh units: (1)
the visual-system research (the pack's `agent/04`, source
`canonsim-визуализация-final`) — the ONE domain the intake family never
routed; its verdict + consult card below; (2) the
`UNIFIED_GAME_DESIGN_KNOWLEDGE_BASE` (a 52 KB three-collection GDC corpus:
level design, narrative/choice/social, quest theory/PCG/balance) — NOT
ADMITTED: no named open row it feeds (D-175's admission rule), the
saturated-corpus finding applies (F2 — its §9 transfer invariants re-derive
the standing families: the information gradient = the brief tiers, the
cascades+callbacks = the hook/cause_hook family, the pair-axis reactivity,
the DCP task shape = the pack purpose laws); the re-open condition stays
F2's own — a fresh question aimed at an open row's evaluation form.

**The visual-system consult card** (intake-30's durable residue, PARKED
behind the SoW fence; the consumers: the presentation-1 write + the SoW
frontend debates; each line cites its owner, nothing restates):

1. **The verdict**: PARTIALLY CONFIRMED — the constitution half re-derives
   standing law whole (the canon → derived-projection → presentation
   ladder = INV-1 + D-118's derived-never-truth; the determinism clauses =
   INV-2/D-028; visual vocabulary as pack data = INV-3; offline-AI-as-
   authoring-aid-only = INV-4; rebuildability = the fold/checkpoint family;
   the degradation ladder = the render ladder's own shape) — the
   cross-domain confirmation family's next member, zero new law.
2. **The development-order law**: prove the semantic read surface FIRST —
   a static, inspectable representation over a golden province run; the
   first objective is "meaning survives visualization" (a read-surface
   falsifier, never a renderer commitment); the stack (semantic projection
   → audience filter → topology/fields → composition/grammar) only after;
   never begin by committing a renderer stack.
3. **The fidelity target**: "the world should look the way it does BECAUSE
   the simulated world is the way it is" — visual form as a readable
   compression of history/topology/relationships/state; every important
   visual difference means something (the visual-side L3 — the
   anti-decoration law).
4. **The rejection table**: universal WFC (a local composer only —
   intake-16/17's own fence); asset-heavy sprite strategy as primary
   (poor leverage per authored-unit); full-scene AI image generation as
   truth (a second physical interpretation — INV-4's shape).
5. **The fence**: presentation-1 owns the visual surface (D-174's recorded
   refusal of a separate visual row); a contract without a consumer has
   unknown requirements (D-148); player-facing compellingness INV-4-fenced
   (F5); the first falsifier is the read-surface spike itself (line 2).

Landed: D-187 + this block + the presentation-1 consult-material wiring.
The build queue UNTOUCHED — nothing unpins, nothing reorders; zero
build-grade items.

**The Kurvitz consolidated research routed (intake-31, iter-158, D-189 — the
owner's «обработай … реши что перенять, адаптировать или привнести в мой
проект и зачем» call over the uploaded prior-session research residue on the
Kurvitz worldbuilding corpus; the research input itself verified against HEAD —
its snapshot pin 2e64ae28 identical to the working BASE; the full one-pass
record: the upload + git at this row's commit).** The verdict: PARTIALLY
CONFIRMED — the corpus mined as a GENERATOR LIBRARY, never a worldbuilding
layer (the uploaded research's own verdict, re-confirmed independently at
HEAD): the strongest principles already owned by the worldbuild surface
(prohibition, negative space, residue-first, meso bridge, knowledge asymmetry
— the doctrine half), the fresh value OPERATIONAL (the generator/probe forms).
Adopted: the W4 operator set (the function-loss probe → WORLD_AUTHORING §5;
the meso assembly probe → §7; the residue lifecycle trace → §8; the
natural-pattern transfer rule + the third-order synthesis → §19) + the test
operationalizations (the biography crisis probe + the humor generator →
WORLD_TESTS §3) + the W4 working set (the bounded crossing-household
experiment with its three-way decision rule + four falsifier-carrying
candidates → WORLD_WORKPLAN §6) + the source mechanics record
(`docs/ref/kurvitz.md`, ref-21 + the REFERENCES/REFERENCES_DEEP/NAV wiring —
the owner's «создать новую в референсах» option taken for the SOURCE layer).
Refused: a Kurvitz document inside `docs/worldbuild/` (D-024 — every domain
it carries has an owner; the uploaded research's own Alternative C upheld); a
generic residue subsystem (SHOULD-NOT-ADD until the bounded experiment proves
a substrate gap); the canon import list (races, name catalogues, humor
tables, life-goal tables, exact thresholds, one-to-one institutions,
contested relativity claims — binding, recorded in the ref file); the two
cross-domain donors admitted as institutions (mechanism-only — the
irrigation-tribunal and milk-kinship mechanisms ride WORLD_WORKPLAN §6's
candidates with named falsifiers, never as imports). The admission rule
(D-175) satisfied: the named open consumer is the world track's W4 frontier
(STATUS Next step's own standing frame); the falsifier is the bounded
experiment's decision rule. Same-iteration syncs (doc drift caught and fixed
in the touched owners): the TASKS ledger's iter-151..156 one-liner hole
backfilled + the ledger header re-scoped (the practice lapsed after the
iter-151 compaction; verified against git); the worldbuild embodiment lines
re-synced to iter-157's landing (the second hand + the pole committed, KI#87
closed — ANCHOR_REGION §6.1/§9, WORLD_TESTS §9, WORLD_WORKPLAN §2/§3 read
stale at HEAD). Landed: D-189 + this block. The build queue UNTOUCHED —
nothing unpins, nothing reorders; zero build-grade items.

**The Vantiel research handoff routed (intake-32, iter-159, D-190 — the
owner's «обработай … реши что перенять, адаптировать или привнести в мой
проект и зачем» + «куда определить … по документации или создать новую в
референсах» + «подключи междоменную трансплантацию» call over the
uploaded `Vantiel_Canonsim_Research_Handoff_v2.md`; the handoff's
substrate map re-verified claim-by-claim at HEAD `44151f1` — every named
mechanism confirmed present; the full one-pass record: the upload + git
at this row's commit).** The verdict: PARTIALLY CONFIRMED — Vantiel as a
source of SEPARATIONS, never subsystems: all ten distinctions (truth
retention ≠ recall salience; fact ≠ interpretation; emotion ≠ factual
memory; relationship magnitude ≠ history; failure ≠ punishment; recovery
≠ undo; knowledge ≠ accessibility; context bundle ≠ memory truth;
journal ≠ canon; world intervention ≠ narrative override) map to owned
substrate (log+knowledge+retrieval / knowledge+traits+reflection /
knowledge+echo / pair axes+events / intent_rejected+predicates / the
append-only log / known_by+transfer / retrieval+brief+since-1 /
render+chronicle / the intent-OCC-event door) — the cross-domain
confirmation family's next member, zero new law. Adopted: the source
record `docs/ref/vantiel.md` (ref-22 + the REFERENCES/REFERENCES_DEEP/NAV
wiring — the owner's «создать новую в референсах» option taken for the
SOURCE layer) + the presentation-1 consult-material wiring: the
RE-EXPANSION LAW (a bounded model-facing context bundle may be disposable
only if its compact claims retain stable event/entity handles and
re-expand deterministically from canonical evidence — never a second
truth, never a mutation of knowledge) and the STAGED-INTERPRETATION
SKETCH (input → interpretation/intent proposal → bounded context → model
decision proposal → repository validation → prose; the exact contract
derived from the real engine-1 consumer, D-022/D-055) — both parked
behind the owner gate, the intake-30 visual-card precedent. Cross-domain
notes recorded in the ref file: the D-105 deadband family is the
SUPERIOR own-form of Vantiel's relationship inertia (chatter prevented by
construction — no enter/exit threshold pair to tune; the transplant test
ran both directions and the existing form won); magnitude-dependent
emotional persistence already emergent in the echo's linear form
(valence × decay ⇒ larger shocks outlast any fixed threshold). Refused:
every subsystem donor (affinity meters, flag catalogs, universal
cognition multipliers, difficulty percentages, mutable memory threads,
free-form Architect edits, journal-as-state, classes/combat/inventory) —
the handoff's own reject list, binding in the ref file; a Vantiel
document inside `docs/worldbuild/` (no authored-model change
demonstrated — the handoff's own fence); the generic knowledge-propagation
graph (PROPOSAL/UNRESOLVED — falsifier: two independent propagation
consumers requiring shared edge-selection semantics beyond
known_by+trust+locality+drift); the hysteresis proposal (UNKNOWN until a
measured oscillation problem the deadbands do not already prevent); the
worldbuild ripple-audit question (parked — falsifier: a recurring
authored-change failure an explicit impact set would have prevented).
The admission rule (D-175) satisfied: the named open row is
presentation-1 (engine-1's decision-input child, the postponed standing
row); the falsifier is the handoff's own — a real presentation consumer
compared against the current brief/retrieval stack on context cost,
traceability, re-expansion correctness. The build queue UNTOUCHED —
nothing unpins, nothing reorders; zero build-grade items.

**The game-design practitioner talks corpus routed (intake-33, iter-166,
D-191 — the owner's «изучи gamedesign_knowledge_base.md и определи что
можно перенять, адаптировать или чем вдохновиться… куда определить
полученные знания, вердикты и данные и распределить по документации»
research call over the uploaded consolidated five-source knowledge base
(Sawyer / Meier / Battle Mode / Johnson / Wolverson; the transplantation
method itself already standing law — intake-24's D-165 card, applied
here, never re-imported); the corpus map verified against HEAD before
routing; the full one-pass record: the upload + git at this row's
commit).** The verdict: PARTIALLY CONFIRMED — a PERCEPTION +
ECONOMY-CRAFT donor, never a systems donor. Differentiated from the
refused UNIFIED GDC knowledge base (intake-30's F2 finding): that
corpus re-derived the standing families (level design / narrative /
quest theory); this one carries a domain no prior GDC family owns —
outcome-perception psychology (S2: expectation bands, the
invisible-roll paranoia law, cause + avoidance path on every failure)
plus the economy-craft pair (S4: the anti-arbitrage spread, the
mortality-as-force-change ECS cure). Adopted: the OUTCOME-PERCEPTION
LAWS CARD (the layered legibility ladder — truth never bends / failure
carries cause / odds as expectation bands / transparency opt-in by
flag / outcomes legible through residue / stakes irreversible; the
combined form of the five competing presentation solutions, each
minus neutralized by another layer) → presentation-1's consult
material (the third parked card, joining the intake-30 visual card and
the intake-32 Vantiel card) + THE ANTI-ARBITRAGE SPREAD (exchange
between stocks lossy by construction — the mechanism, never the 2×
number; the Resource open question's donor: ANCHOR_REGION's "how does
scarcity become a measured price/flow cycle?"; falsifier: the water's
own function-loss arbiter) + THE TURNOVER QUESTION (the ECS cure as
the function-loss probe aimed at holder mortality — the anti-freeze
law, WORLD_AUTHORING §5; consumers: the camp's meso half, W5's
biography arc) + TWO parked notes (the Hot-Path placement pair beside
the intake-27 topology proposal — the road-traffic rider's material;
the weak-coupling authoring law — pack-3's event-family material).
The confirmation batch (the largest since intake-27): seed-in-save =
INV-2/T2; undo-because-deterministic = the same family; no-cheats
asymmetric AI = the one-id intent door; infinite tooltips =
mechanics.py; automation-red-flag inverted for observability = mech-2's
nothing-dropped-silently; direct-and-verify randomness = the worldgen's
superior own form (MST connectivity by construction + the
reachability/dead-arming lints); the Covert Action center-of-gravity =
the brief's bounded blocks; the imagination economy = L6/mode A; the
known-denominator thresholds = the world track's store budgets;
events-offer-not-negotiate = the door's attempts-are-facts. Refused
(the binding do-not-import list, in the ref file): all dice-bending
(the source's own anti-streak mechanism — the invariant is perceived
fairness, bought only at the render layer, never the roll layer); the
3:1/2×/N-levels constants as law (threshold leakage); the tech-deck,
order-system, no-counterattack mechanics (no substrate, no consumer);
the difficulty taxonomy; the Voronoi/two-layer-noise worldgen
additions (saturated by ref-8/ref-9 + the LOD ladder); the K-table
typography as repo law (the per-finding verdict discipline already
owns it — noted as the source's own synthesis strength). The admission
rule (D-175) satisfied: the named consumers — presentation-1 (the
standing row), the world track's Resource open question + the camp/W5
frontier (STATUS Next step's own standing frame), the road-traffic
rider (the pressure pack's post-T1 rows); the falsifiers stated per
adoption above. Landed: D-191 + this block + the source record
(`docs/ref/game_design_talks.md`, ref-23 + the REFERENCES/
REFERENCES_DEEP/NAV wiring) + the five catalog rows + the presentation-1
consult-material pointer + the WORLD_AUTHORING §5 turnover line. The
build queue UNTOUCHED — nothing unpins, nothing reorders; zero
build-grade items.

**The ultimate research corpus routed (intake-34, iter-181, D-194 — the
owner's «начать работу с загруженным ресерч-корпусом… определить что с
ним делать… брать в референсы в отдельную папку как с worldbuild было
или нет и почему… если нереально за 1 итерацию — планируй несколько»
call over the uploaded `canonsim_research_ultimate_v2_with_doctrine_v3_
integrated.zip` (2.3 MB: the four source zips + the doctrine + the
method + the two-layer consolidation + the manifest); the consult
posture — the corpus stays outside the repo, the convenience-copy law;
every fresh claim verified against HEAD before routing; the full
one-pass record: the upload + git at this row's commit).** The corpus
map — the six source units split cleanly by prior routing: (1) the
RESEARCH BLOCK (S1–S4: the capability/resolution/progression
consolidation, the cross-domain ultimate v12, the 44-card math-transplant
reference) — FRESH, its legacy sources pinned to iter-159..172 HEADs,
never routed, this intake's actual subject; (2) the Dense v3 hybrid
original — already routed whole (intake-30/D-187; the visual card + the
UNIFIED-KB refusal stand, nothing re-opened); (3)+(4) the v1 + the
alternate consolidations — the corpus's own COMPARISON.md material,
provenance only; (5) the doctrine v3 + (6) cross_domain_principles — the
operating/research doctrine whose LIVE form is the owner's standing
session discipline (the five-question material-verdict test, the
dispositions, the promotion gate, the session-completion contract —
verified intent-identical) — ABSORBED, nothing to land.

**The structural verdict — the proposed drop-in tree (`docs/research/` +
`research_archive/` inside the repo) REFUSED**: a parallel documentation
layer over fully-owned domains (00_INDEX/01_SNAPSHOT → STATUS/NAV;
02_AGENT_KERNEL → AGENTS + the standing doctrine + TEST_PLAN §9;
03_OWNERSHIP_ROUTING → NAV §3; 04–07 → this section's intake records +
the parked cards + `docs/worldbuild/`) — the intake-30 precedent's exact
ruling on the same material's earlier consolidation (D-024 single-owner;
D-187; the corpus's own crosswalk concedes every owner). The D-186
directory exception INAPPLICABLE — worldbuild earned its surface as an
ownerless authored-domain model; this corpus is research residue, the
content class D-185's archive law already owns (§6 compact blocks + git
+ the outside sources). The corpus's "two-speed architecture" (compact
active + deep on demand + archive) re-derives the repo's standing shape —
the confirmation family, zero new architecture. The owner's worldbuild
question answered: NO separate folder; the per-source deep-record option
(the ref-file form, the intake-31/33 precedent) remains available for
the math catalog — deferred behind its own trigger (below), never a
default import.

**The capability/progression consult card** (the fresh domain — S1+S2's
research, its own verdict PARTIALLY CONFIRMED, re-confirmed independently
at HEAD: the FACT table holds — pack-level skill bases
(`core/intent.py::skill_total` over `rules.json`), status modifiers
live, per-actor persistent mastery absent, the parser emits structured
intent, failure materially represented; PARKED behind the owner gate;
the consumers: the SoW horizon (player-visible growth in a game
frontend), the world track's W5 biography arc, any future combat-bearing
pack; the falsifier: the research's own Experiment 0 — one long
scenario, zero implementation: no quality deficit expressible through
status/relations/knowledge/resources/world state → no progression
layer; a deficit → the leading candidate first, never XP):

1. **The five-layer decomposition** (permission / capability /
   resolution / consequence / learning — never collapse into one skill
   check): permission = reach/possession/knowledge/access (the doors'
   existing gates); resolution specializes per action class
   (deterministic / roll / opposed / NPC decision — the intent door's
   own vocabulary), one shared protocol, no universal formula.
2. **The leading candidate (H1)** — event-derived evidence-weighted
   mastery: `effective = pack base + fold(log) mastery + status
   modifiers`; coverage/novelty-weighted evidence (repetition ≈
   nothing, informative failure first-class), PC/NPC symmetric, zero
   new streams (INV-2), derived-never-stored (L3). XP/levels/classes/
   global currency REJECTED as unsupported necessity (the corpus's own
   verdict, upheld); pure use-count REJECTED.
3. **The carrier taxonomy** — capability rides actors/tools/procedures/
   groups/roles/relations/locations (INV-3-compliant: pack data +
   folds, no engine nouns); "more effective without higher level" via
   equipment/access/knowledge/role.
4. **The NPC-agency hypothesis** — negotiation as agent decision from
   canonical state (goals/alternatives/trust/reservation conditions),
   never `social + d20`; the epistemic-bluff test (one utterance,
   different NPC knowledge → different reactions) is the cheapest
   discriminator.
5. **The guard set** — the 22 stress cases + the 15 evaluation criteria
   + the treadmill/grind/LOD pitfalls (cold NPCs never learn; the world
   never silently scales to the player) travel with the card;
   Experiment 0 decides before any row opens (D-175: no row without
   the measured deficit).

**The BNF/contracts verdict** (S3's semantic control layer): the
cross-domain confirmation family's next member — PARTIALLY CONFIRMED,
mostly re-derivation (one canon/one write door = INV-1/D-031; the four
planes = L3/L11/L12 + TEST_PLAN §8.4 + the render ladder; safety ≠
liveness = the ladder/drain family, PARSER_SPEC §5 + VALIDATION_SPEC
§7; dependency ≠ cause = L7; diagnostics-explain-never-authorize =
D-118; the promotion gate = the standing doctrine). The T1–T40
verification grammar REFUSED as a second label set — it collides with
the T-suite's own namespace and re-derives TEST_PLAN §9's lenses/prisms
+ the standing instruments (D-024: label-matching is not
reconciliation). L27–L34 NOT landed as constitutional laws (the
corpus's own inflation discipline; the runtime halves already INV/L-
owned, the research halves standing doctrine); its "existing L1–L26
family" claim FALSE at HEAD (the repo owns L1–L14) — the drift marker
recorded. The identity algebra (request/intent/event/derivation/
content) confirms the landed shapes (intent ids, event ids, the
cursor's `prefix_sha256`, `grammar_fingerprint`, the manifest's
model sha256); no idempotency store (the corpus's own rule). The
U1–U12 open questions correctly self-parked — no consumer at HEAD for
coherent-cut enforcement, fairness, FailureCore, bi-temporal validity,
or incremental reuse.

**The math-mechanism index card** (S4's 44 cards — the family
dispositions CONFIRMED at HEAD; the per-mechanism bodies live in the
corpus, the owner's on-demand source; a future row naming a family
reads this card, then the corpus):

| family (cards) | disposition | the trigger that re-opens |
|---|---|---|
| keyed/counter-addressed RNG; keyed worldgen/cursor | PARTIALLY CONFIRMED, selective | a real order-independent-local-generation or lazy-expansion consumer; the measured world-expansion instability (~0.3% noise-value preservation, 7–9% sites under extent growth) is the substrate fact, never a global-RNG-rewrite warrant; costs ~20× / ~1.7× (different baselines — do not collapse) |
| CRN / paired seeds | CONFIRMED as research methodology | the R1 candidate — paired-Δ reporting in `balance_harness` (TEST_PLAN §6's contract unchanged until an owner call); the measured pair-variance ratios 0.011–0.039 (M3 0.338) |
| metamorphic testing; delta debugging; Δ² interaction; POR / sequence covering | PROPOSED (the assurance plane) | a recurring failing-scenario reduction need / a measured order-space explosion with a sound commutativity relation |
| representation transforms (PQ/OPQ+RHT — the synthetic MSE 0.824→0.068 numbers; JL; wavelets; bitsets/FWHT; delta+varint; Bloom/CMS/HLL; HAMT; SDF) | DEFERRED | a measured memory/latency hotspot the exact representation change cannot fix first — the 1.41× flat-index exact win is the standing precedent (representation before algorithm) |
| causal read-side DAG; provenance semirings; SCC/min-cut; vector clocks | PROPOSED (read-side POC) / DEFERRED | a recurring multi-hop provenance consumer beyond `mechanics.py why`'s single-parent chains |
| entropy/JSD drift metrics; EWMA/CUSUM; temporal monitors | PROPOSED (derived metrics) | an M-family question the existing metrics cannot answer (R7: compare against M4/M5 first) |
| Director PID; Lyapunov runtime; global truth/risk scores; QMC blanket RNG; bisect indexing | REJECTED / offline-only / SHOULD-NOT-ADD | the measured stable hysteresis (`eventless_max_stretch=1` × 300 runs); nothing measurable to control |

The binding do-not-import list (the corpus's anti-pattern catalogue,
upheld at HEAD): a second canonical store; MVCC; a CRDT/vector-clock
semantic layer; generic provenance/dependency/causal-graph runtimes;
generic fairness/reactive/workflow engines; global truth/risk scores; a
bi-temporal subsystem; a procedural-memory subsystem; a permanent
FailureCore/CausalSlice runtime; canonical lossy quantization (exact
replay non-negotiable). The measured lesson routed to its owner:
TEST_PLAN §9's claim packet gains the empty-ablation rule (a zero-delta
`--systems-minus` arm is a failed experiment, not zero causal effect —
the arm must demonstrably exercise the target subsystem on the run
horizon).

Landed: D-194 (the D-119 family row's extension) + this block + the
TEST_PLAN §9 line + the state docs. The build queue UNTOUCHED — nothing
unpins, nothing reorders; zero build-grade items. The second pass (the
per-card math verification + the ref-file deep record) DEFERRED behind
its own trigger: a named row asking for a mechanism family, or the
owner's explicit call.

**The ultimate research corpus — the second pass (intake-35, iter-182,
D-195 — the owner's «продолжай и прочую работу с архивом, я хочу чтобы
ты извлек пользу по максимуму из идей, механизмов и предложений внутри!
мне главное качество в долгосрок» call firing intake-34's deferred
trigger; the inspiration & transfer analysis posture: underlying
principles and mechanisms, never surface labels or ready dictionaries;
the corpus stays outside the repo, the convenience-copy law; every
disposition re-verified against HEAD — the full one-pass table: the
upload + git at this row's commit).** The verdict — the 44-card family
dispositions and the two parked cards' FACT tables independently
RE-CONFIRMED at HEAD (the anchors: `core/rng.py`'s seven
content-addressed stream families — the semantic-addressing principle
already the repo's stream-level form, the draw-level half correctly
deferred behind the lazy-chunk consumer; `mechanics.py why`'s
single-parent chains covering the current causal consumers;
`balance_harness`'s marginal-only reporting — R1's substrate fact,
code-verified; M4's internal-diversity form vs the corpus's
JSD-vs-baseline — a distinct question, parked with R7); zero new
build-grade items; zero new consumers found; the ref-file deep record
REMAINS deferred — its trigger is a named row consuming a specific
mechanism family, never an inspiration pass. The confirmation family
(the corpus's strongest principles re-derive standing law, nothing to
land): materialized causal residue = INV-1's own point; heterogeneous
agency = depth-6's faction chains; the peripheral observer probe = the
brief's O(relevance) + the knower boundaries; the promotion rule's
eight gates = L13 + D-175 + the first-consumer law, distributed; the
identity algebra = the landed id family (intent/event ids,
`prefix_sha256`, `grammar_fingerprint`, the manifest sha256); the
two-baselines and environment caveats = the env-pin law (TEST_PLAN
§1.1). Four precisions (each rides this block, one pointer from its
consumer):

1. **Experiment 0's reframe** (the parked capability card's falsifier,
   sharpened — INFERENCE): the landed folds already implement
   differential evidence weighting (knowledge = fidelity-weighted,
   echo/traits = recurrence-weighted, reflection =
   contradiction/staleness-weighted) — the null outcome is «growth runs
   on the landed folds», never «no growth»; the discriminating scenario
   is procedural skill (the musket stress case: knowledge records +
   traits exist, no per-actor resolution modifier). No card edit — the
   card's own decision rule carries it. EXECUTED iter-183 (the record
   below).
2. **R1's sharpest argument** (the owner's pending methodology call —
   INFERENCE over the corpus's MEASURED ratios): M3, the gate-read
   causal-chain metric, is the noisiest under marginal reporting (0.338
   vs 0.011–0.039); the seed ranges pair by construction across arms,
   but the harness computes no paired Δ — the report is the marginal
   table (code-verified); R1 is the reporting change alone. LANDED
   iter-183 (TEST_PLAN §6 + tests/test_balance_harness.py — our own
   ratios confirm the shape).
3. **The deletion criterion** (TEST_PLAN §9's claim packet — the
   corpus's six-question doctrine's one unnamed half: the Falsifier
   guards admission, the deletion criterion guards retention; the repo
   practices it distributed — the KI cleanup, the doc collapses, the
   deferred rows' re-trigger clauses): PROPOSAL / UNRESOLVED, the
   owner's call; the first-consumer law holds — the §9 field waits for
   a claim packet that actually needs it.
4. **The generalized-controls hypothesis** (the empty-ablation rule is
   the sham-control principle's first landed instance; the general form
   — every intervention experiment names its positive/negative/sham
   arms — waits for a second instance in a different protocol):
   HYPOTHESIS / DEFERRED.

Landed: D-195 (the D-119 family row's extension) + this block + the
state docs. The build queue UNTOUCHED — nothing unpins, nothing
reorders; zero build-grade items; zero production behaviour change.

**Experiment 0 executed — the parked capability card's falsifier
(iter-183, the owner's «residues intake-34/35» call; zero
implementation by the card's own law — the instruments are the
committed `tests/playscripts/exp0_week.json` + `tests/test_exp0.py`:
the apprentice thief's five days — the purse gambit (the crime-mapped
escalation race) + 25 lift attempts on the ale mug (the procedural
coin), the world's rotations/beats/transfers running through; seed 32
the canonical arc, seeds 2000..2007 the pinned sweep, seeds 1000..1039
the recorded sweep). The reframe's null half CONFIRMED — growth runs
on the landed folds for every arc the scenario reaches for: the day-one
botch seeds four leverage holders plus the transferred fifth; the purse
lift fires the expectation violation; the document challenge is
answered; the trait crystallizes on both guards and the trait-gated
scans fire all week (the permanent paranoia); the suspicion axes persist
below the arrest line at seed 32 while 4/40 sweep runs end arrested (the
world's memory has teeth); the knowledge fold dedups the practice loop's
repeated tokens after first sight — the corpus's own evidence law
(«identical repetition: rapidly diminishing»), landed. The falsifier's
flat half: the thief's effective resolution inputs are EXACTLY the
day-one values after 159 canonical events of practice (skill_total =
the pack base at the horizon; every take-check attacker total =
base + d20; the sweep's attacker means flat across the week's windows
50.31/50.34/50.76/49.95) — the only lawful difficulty mover is the world's
own status drift (the on-duty guard's fatigue moves the lift rate from
the fresh 0.1125 to the measured 0.152: the status dimension, live and
working). THE VERDICT, per the card's decision rule: no live deficit at
v0.1 → no progression layer, no row (D-175); the procedural-competence
gap is real-but-latent — structurally unexpressible (the read-side
folds can never feed resolution, L6/EPIST-1), unconsumed (no beat, hook,
urgency or chronicle line in the scenario asks for «better») — the card
STAYS PARKED behind its named consumers (the SoW player-visible
growth, the world track's W5 biography arc, a combat-bearing pack): the
first to go live flips the latent gap to a live deficit and fires the
leading candidate (event-derived evidence-weighted mastery, never XP).**

**The curated unit archive routed (intake-36, iter-193, D-196 — the
owner's «провести работу с canonsim_research_packet_ULTIMATE_v2.zip,
решить что можно перенимать, чем вдохновляться, что требует проверки…
где есть упущения и с доработкой можно и даже нужно реализовать» call
over the uploaded packet (39 curated units / 10 families / 85
provenance atoms / 5 sources; the single-unit Packet ×
cross-domain_units_v3 hybrid; the consult posture — the packet stays
outside the repo, the convenience-copy law; every unit body read,
every carrier claim code-verified at HEAD `16a4aa4`; the full one-pass
verdict table: the upload + git at this row's commit).** The corpus
map — the dominant source (guide29, 67/85 atoms — the cross-domain
transplantation guide) is the METHOD the repo already absorbed as
standing law (D-165's card; the owner's session discipline the live
form): its mechanism atoms re-derive owned substrate family by family;
the S-family's source is the intake-30 visual source's updated sibling
(the visual card parked, nothing re-opened); the control plane (the
triage protocol, the one-unit law, the completion contract, the
quality rubric, the stdlib tools — verify_packet PASS) is the standing
doctrine in archival form, one operational novelty: the PHYSICAL
BUNDLE firewall (`make_iteration_bundle.py` — siblings physically
absent from the materialized context, stronger than a prompt
prohibition), an owner-side session practice, never repo material
(Rule 9). The verdict: PARTIALLY CONFIRMED — the largest single
confirmation batch: 34/39 units CONFIRMED-owned, each re-deriving
standing law or owned substrate at its named carrier: L01 =
`mechanics.py why` + D-118 (the local certificate already the
one-event postmortem's own shape); L02 = INV-1's own point + the
charcoal-paper standing state (iter-189) the live proof (the inverse
archaeology read deferred — no consumer); C01 = the event → state →
authorized-observation → decision loop + the withhold banks (iter-187)
residue-mediated coordination in practice; C02 = `expectation_drafts`
(P2d) the mismatch → evidence-acquisition mechanism, the director
urgency family the routing half; C04 = `known_by` (D-088) + the
per-watcher suspicion bands (scoped aggregation already the shape);
C05 = res-1's stock/flow verbs + the known-denominator thresholds
(D-191); D01 = THE INTENT DOOR whole (the finite option set + the GBNF
grammar + the closed reply document + external policy — PARSER_SPEC's
own contract, the packet's strongest confirmation member); E01 = the
knowledge scopes + the knower boundary; E02 = the validator's verdict
semantics (iter-9) + the W5 boundary classification the live practice;
F01/F03 = the LOD ladder's own task-relative sufficiency law +
maclock-1 + depth-7 condensation (closure under named consumers); F04
= INV-1 closed-by-construction (the three verbs carry their own
gain/loss; no canonical residual can exist — the derived-aggregate
residual half deferred, routed below); F05 = depth-6's faction chains
(intake-35's own mapping); G01 = PASS_ORDER (D-165 #6, the one-way
layer law); G02 = the relax pass's airtight radius bound — the
effect-distance declaration in derived form (no gap at current scale);
G05 = the brief's O(relevance) budgets (structural allocation, the
read-side form); G06 = the on_action/transitions layers ARE the
local-rewrite form (the runtime rewrite engine L13-refused); M01–M07
= the standing doctrine's own atoms (the five-part test; M03 the
empty-ablation rule landed intake-34; M05 the n=2 convergent-reader
independence discipline; M06 the W5 blind-reader probes themselves;
M07 the flat-index precedent); S01–S04 = the canon →
derived-projection → presentation ladder + the lattice/claim laws +
the LOD ladder + the render/presentation split (S01's reader-surface
half the W5 probes' own instrument); R01/R02 = the math catalog's
deferred assurance family (intake-34's own trigger); R03 = PROPOSAL
(`mechanics.py blast`'s minimal-intervention extension — a candidate
instrument, no current consumer); R04 = the STATUS routing discipline;
P02 = REJECTED twice over (the D-105 deadband superiority, intake-32's
two-direction transplant test + the measured stable hysteresis,
intake-34) — re-opens only on a measured oscillation the deadbands do
not prevent; G03 = the intake-16/17/30 WFC fence stands; G04 = DEFERRED
(authored placement + MST today, no consumer). The THREE fresh
routings — the packet's real decision leverage, each joining a NAMED
consumer, zero new rows (D-175):

1. **C03 + F02 → the W5 heartbreak station** (the trio's last open
   station, WORLD_WORKPLAN §7's standing decision point): the
   relation-formation factor triple (repeated consequential
   co-presence × reciprocity × selective disclosure → an endogenous
   relation that expands future legal options) as the station's design
   material — pack-authorable TODAY (on_action deltas + pair axes +
   threshold-gated hooks + `requires` gates — zero engine change,
   INV-3/D-142), the formation side untested in a committed pack
   (relations today move via witnessed-token reactions, not
   co-presence); F02's option-topology classification (ADD / REMOVE /
   MERGE / SPLIT / SEMANTIC-CHANGE) as the probe's «future option»
   measurement vocabulary — the station's own success criterion names
   a lost future option. Falsifier: the probe itself (the blind-reader
   discipline; a failure classified by boundary, never «improve the
   prose»).
2. **P01 + P03 → the road-traffic depth-7 rider** (the named future
   row — travel's own deferral, `core/travel.py`'s head + D-188's
   post-T1 residue): capacity ≠ route existence (today's price law is
   duration-only), the edge-capacity perturbation discriminant
   (perturb one edge → realized delay → stock divergence →
   institutional response), and P03's fracture test (a named
   downstream regime change — queue formation, spillover, abandonment
   — never average utilization) as the row's evaluation grammar when
   it opens; F04's derived-aggregate residual rides the same row (the
   accounting half for derived tallies).
3. **C05's denominator integrity → the group-stock lint gap** (D-182's
   recorded, never-patched finding): the honest-denominator principle
   (a rate = flow over the declared membership base; a base change
   without a claim update is a semantic change) as that future lint's
   design law.

The ref-file deep record for guide29 DEFERRED behind the math
catalog's own trigger (a named row consuming a specific mechanism
family — intake-35's recorded condition; the three routings above
carry their material in this block). Landed: D-196 (the D-119 family
row's extension) + this block + the state docs. The build queue
UNTOUCHED — nothing unpins, nothing reorders; zero build-grade items;
zero production behavior change.

**The agent-bottleneck research routed (intake-37, iter-195, D-197 —
the owner's «отнестись к canonsim-agent-bottleneck-research.md как к
обязательному research-артефакту, а не заметке» call over the uploaded
research note: the pack-scale agent cognitive-bottleneck investigation
at `<10%` volume; the note's BASE `16a4aa4`, every measurement
re-verified at HEAD `462e84a` — 2018+1, ruff, docguard clean at both;
the note itself stays outside the repo, the convenience-copy law; the
probe runners outside the repo, Rule 9).** The verdict: PARTIALLY
CONFIRMED — the note's own verdict upheld, with one claim REFUTED by
measurement and one gap upgraded from proposal to measured fact.

*Confirmed (re-measured):* the formats sound — JSONL + the four-file
pack re-derive standing law (D-002/PACK_SPEC); zero format change
warranted. The tooling foundation as stated: matrix's narrow
hook/event/token/prop vocabulary (+`--full`/`--dag`), pack_doctor,
checkpoints, the architecture tests, docguard — present and green.
The size tables: core 22,557 LOC (loop 1714 / director 1419 /
worldgen 1388 / intent 1080 — the note's figures each +1, a counting
artifact); 5 packs × 4 files, 12,728 lines; `rules.director` the
hotspot (17–19 KB × 3 packs, ~23 blocks per rules.json, nesting depth
10 — the «nested JSON hostile to precise edits» pressure real);
`impact --path` ABSENT — the named gap real (matrix lists the
unindexed rules blocks generically). **The mutation-adequacy gap
MEASURED (the session's probe):** the admission lint refuses the
structural breaks (orphan ref, closed enum, intent-contract, template
vocabulary — 4/6 probes REFUSED) but ACCEPTS value mutations (a
director `release_threshold` 10→4, an urgency `probability_per_beat`
40→55 — 2/6), and the tavern golden is blind to BOTH on the covered
path — a semantic pack change can pass the whole verification stack
silently when its path is uncovered.

*Refuted:* «agent default behaviour is full-file rewrite; current
defence: None» — the git history measured (120 pack-JSON file-touches):
97% surgical (<50% of the file), 82% tiny (≤10%); the three rewrites
are all early-era growth; the defence is standing law (AGENTS §2
«patch files in place; never regenerate a whole file»). Residual
truth: conventional, not mechanical — nothing refuses a rewrite; the
risk is future-scale with unfamiliar agents, not present behavior.
Numeric corrections: the note's ≈614 KB pack size reproduces under no
measure (598.3 KB byte-sum / 599.1 with the sidecar / 672 du-blocks —
the note's own «correction» introduced the error; the first draft's
672 was du-based); the reference-density figures (811/1004/1146) are
extractor-dependent and not reproducible (total 9696/11725/13367,
unique 2154/2413/2514) — the ordering claim (density grows
tavern < grim < province) HOLDS under both measures.

*Unknown (working premise, not fact):* the `<10%`-ready volume
framing (the owner's own; the SoW horizon unbuilt); the 5–10×
cognitive-load scaling — **measured 2026-09-23 (iter-198's A/B
falsifier, TECH_NOTES §17): REFUTED at the current scale for the
tested model class** (conditional on a valid round-trip, bare agents
land the asked edit 8/8 — find/scope is not the binding constraint;
the emission mechanics are; untested above the current pack scale);
future-context softening (undecidable).

*The documentation schema (the research→implementation routing law,
this block the record):* durable residue → phases.md §6 intake blocks
(D-185 unchanged); interventions (probe runners, mutated pack copies,
spike drafts) → `scratch/` (gitignored, never staged — Rule 9's
family; the .gitignore comment the pointer); architectural adoptions
→ DECISIONS; tasks → TASKS. No parallel research tree (D-194's
refusal stands — residue, not an ownerless domain).

*The routing:* ONE row convened — `mech-2` (the agent impact surface:
`mechanics impact --path`, R03's family joined by its first named
consumer — the note's smallest useful residue, tooling-only, D-012
untouched; its design material: bounded causal traversal, CEGAR
refinement, the minimal-witness fallback — the note's extracted
mechanisms, never copied solutions). TEST_PLAN §9 gains the
mutation-adequacy claim shape (the prism this session's probe
instantiated). **The A/B falsifier RAN (iter-198, the owner's call;
TECH_NOTES §17 the numbers' owner): the injected impact gate moved
none of the three metrics (success 8/18 both arms, lint refusals 0,
patches tiny); the measured failure mass sits in the whole-file
emission pattern itself (the bracket-drift wall in `director.hooks`
+ 73% silent notes paraphrase) — the tool-less API-agent class's
failure, not the file-tool agents'.** The structured-patch admission
machinery and the edit-shape guard stay PROPOSAL — the original
cognitive-crutch motivation weakened, an emission-reliability
motivation measured in its place; the fate the owner's call
(scav-1's measurement-before-mechanism precedent stands). Zero
format changes; the build queue otherwise UNTOUCHED.

**The cross-domain principle document routed (intake-38, iter-214-doc7,
D-199 — the owner's «тогда вперед сажай intake-38 над „Междоменной“»
call over the uploaded research-method text: the 552-line "CanonSim —
Cross-Domain Principle Transplantation" doctrine — the purpose + 23
sections + the governing principle; verified against HEAD `ff9ccbb`
before routing, the baseline triple green at both ends (2041+1, ruff,
docguard); the document itself stays outside the repo, the
convenience-copy law).** The verdict: CONFIRMED-owned — the doctrine
is the standing discipline's own live form, the corpus family's
doctrine-level sibling (its §8/§9 method atoms the very families
intakes 34..37 landed or parked), the second full external
restatement and the strongest convergence yet.

*Confirmed (owned, re-verified at HEAD):* §1's class/disposition pair
= TEST_PLAN §9's two axes (doc-5's landing); §3's transplantation
pipeline = D-024's own test; §4's falsification filter = the
do-not-import grammar's rejection shapes; §5's research-control loop
= the §9 claim packet's own order; §6's constraint = D-142's
admission law over the INV fence; §18's five-part material verdict
test = BLUEPRINT §2 L15 verbatim (principle / form / quality /
transfer / combined design); §19's runtime-promotion gate = AGENTS
§2.8's admission ladder; §20's anti-pattern list = the binding
do-not-import list nearly verbatim (second canonical store, generic
provenance/causal graph, global truth/risk/confidence score, permanent
diagnostic types — each already REJECTED on measured grounds); §21's
persistence law = D-185's own form, the same owners named; §22's
session completion contract = the handoff report's shape.

*The §8/§9 method families — CONFIRMED-owned through intakes 34..37:*
counterfactual ablation → the `--systems-minus` family + the
empty-ablation rule; perturbation propagation → the one-knob prism;
the peripheral observer probe → the blind suites + the
knowledge/perception boundary; materialized causal residue → INV-1's
own shape (the log the truth, the state the fold — the past causally
present through changed state, never a second store); heterogeneous
agency → depth-6's objective-function triangle + D-196's C05 routing;
bounded causal traversal + CEGAR → mech-2's design material; mutation
adequacy → §9's mutation-probe row + the path-bound law (intake-37's
measured lesson); positive/negative/sham controls → the
generalized-controls hypothesis (HYPOTHESIS/DEFERRED, the
empty-ablation rule the first landed instance); the
realized-intervention gate → the empty-ablation rule itself, iter-198's
A/B falsifier the standing measured instance (the injected gate moved
none of the three metrics — a failed experiment, never zero causal
effect); minimal pairs → INV-3's pack-declaration gate + engine-1's
arms; delta debugging → the assurance plane's PROPOSED row, its
promotion trigger named; translation validation → the
representation-transforms row's own pattern (DEFERRED); the
deterministic fault curriculum → the deviation corpus's fault
families; CRN/paired seeds → CONFIRMED as methodology (the measured
pair-variance ratios).

*The fresh residue (the genuinely unsurfaced atoms — parked per
D-175, zero new rows, each behind its named first consumer):*

1. **Held-out transfer** — the only §9 method with no current owner
   surface (acquisition contexts → freeze relevant state → held-out
   contexts/packs → evaluate; familiarity ≠ transferable competence);
   the §14 form already parks in the capability/progression consult
   card (D-194) — HYPOTHESIS, the trigger: a first capability or
   learning claim whose acquisition and evaluation share the corpus
   (engine-1's {3–8B} GBNF corpus the natural first instance).
2. **The experiment contract's unfilled fields** — §11's 17-field
   contract over the §9 claim packet: STOPPING RULE / SPILLOVER /
   BLOCKED-NUISANCE have no packet surface yet (trace identity ≈ the
   packet's scenario + corpus) — PROPOSAL/UNRESOLVED beside the
   deletion criterion (intake-35's precedent: the field waits for a
   claim packet that actually needs it, the first-consumer law).
3. **Evidence-independence audit** — independent re-derivation's
   multi-evidence generalization (confirmations sharing root /
   assumption / metric / observation boundary are not independent) —
   HYPOTHESIS, the trigger: a first claim resting on two or more
   confirmations.
4. **Metric anti-Goodhart test** — the two-question form (can the
   metric move without the phenomenon; the phenomenon without the
   metric) — the §9 metric rows carry the decoy/oracle vocabulary,
   not this shape — PROPOSAL, the trigger: a first metric-led claim.
5. **§12's residual relation-lens** — the verification grammar's 24
   lens, the majority already owned (canonical authority = the canon
   door; observation boundary = the blind suites; semantic lowering =
   L6/EPIST-1; retry-safe admission = the idempotency law;
   authority/truth separation = the fact/belief split; freshness =
   the derived-state law; mutation adequacy = the probe; realized
   intervention = the empty-ablation rule; metamorphic equivalence =
   the order probes; counterexample preservation = the capsule law);
   the residual set parks as consult vocabulary, never a production
   feature (the document's own clause).

*The corroborating record:* a second agent's independent full-corpus
pass over the same 20-file archive (the owner's cross-review request,
2026-09-24) reached the same core verdict — mechanisms, never
architecture; TITAN/Guardian/SAE a donor catalog, never a second
control plane — and independently reproduced the archive's own
contradictions (the `AGENT_PROTOCOL_ULTIMATE v1.1.yaml` claiming
machine-readable YAML while failing `yaml.safe_load` at line 3; the
CONSENSUS_SCORE 99/100 self-assessments; «сведенные анализы» citing
documents absent from the archive). Its ADOPT list predates the
intake-34..37 absorption — the "new" mechanisms (mutation adequacy,
realized-intervention, sham controls, CEGAR, delta debugging, CRN)
already landed or parked with measured evidence; the review's value
is the second independent confirmation of the family dispositions
(intake-35's own precedent), recorded as this intake's corroboration,
never a parallel plan. Its 15-question donor filter restates
D-024 + D-175 — correctly NOT planted (no second tree, D-194's
refusal stands).

*The routing:* ZERO rows convened (D-175 — no fresh residue names a
standing open row); zero build-grade items; the build queue
UNTOUCHED; TEST_PLAN §9's claim-shape table untouched (the
first-consumer law — a new lens enters only after a claim packet used
it); the document never enters REFERENCES (a research-method text,
not a donor source — the intake-34/36/37 class).

**The doctrine's agent-instruction re-edition routed (intake-39,
iter-253-doc8, D-231 — the owner's «согласен с твоими вердиктами =>
приступай» call over the tmpfiles.org upload: the 413-line
"Cross-Domain Mechanism Transplantation — Agent Instruction" (md5
80fdb9d9b39f8c13351ebe23cee528c4), the REWORKED edition of
intake-38's own corpus — the 552-line doctrine compressed to 413,
restructured into the agent-instruction form (+Role, +§0 Governing
Loop, +§24 Agent Checklist, the renumbering that moves the old
runtime-promotion gate from §19 to §20), the experiment contract
re-counted 17→18 fields; verified against HEAD `f209d68` before
routing, the baseline triple green (2384+9, ruff, docguard); the
document itself stays outside the repo, the convenience-copy law).**
The verdict: CONFIRMED-owned — the re-edition's CONTENT is
intake-38's own corpus, D-199's per-atom verdicts carrying over
unchanged: the confirmed-owned map (the transplantation pipeline,
the falsification filter, the five-part test, the promotion gate,
the anti-patterns, the persistence owners), the §8/§9 method
families landed or parked through intakes 34..37, and the five
parked atoms each still behind its named first consumer — the
contract's re-count opens no parked surface (stopping-rule /
spillover / blocked-nuisance remain the unfilled three; a rework
that restates them is not new evidence, intake-35's second-pass
precedent).

*The genuinely new material — one fresh atom, one adoption, one
refusal:*

1. **§19 Synthesis Over Selection** — the ONE fresh principle (no
   counterpart in the 552-line original): at a fork whose candidates
   carry real trade-offs, enumerate each candidate's concrete
   advantages/disadvantages as independent axes; decompose every
   disadvantage into intrinsic-to-mechanism vs
   artifact-of-formulation; construct a novel candidate satisfying
   the union of the advantage constraints while violating none of
   the disadvantage-avoidance constraints (a redesign that dissolves
   the trade-off, never a weighted compromise); name and verify any
   emergent property; then the honest comparison — the synthesis is
   kept only if it matches or beats the best parent on every
   material axis while eliminating at least one material
   disadvantage, otherwise discarded for selection from the original
   set (a re-labeled parent or averaged parameters is not a
   synthesis). CONFIRMED as the design-fork law's missing half:
   BLUEPRINT §2 L15's Combined-design part already asks the question
   (is there a combination preserving the advantages while
   neutralizing the disadvantages — doc-5, D-198), and AGENTS §2.7
   owns the selection half (compare, prefer the quality option,
   never generalize) — the synthesis step is the PROCEDURE the
   question always lacked; it landed as §2.7's extension the same
   session (iter-254-doc9, D-232), this intake's one live adoption.
   §24's checklist line ("synthesis attempted where trade-offs
   exist") rides it, no separate surface.
2. **The instruction FORM** — the Role / §0 loop / §24 checklist
   agent-instruction shape itself — REFUSED: AGENTS §2.8's standing
   refusals (no second project memory, no nested agent-instruction
   files; the named law docs are the repo's operative form, D-024's
   single-owner law). The form is the author's delivery choice over
   the same content, never a repo need — the doc-4..doc-6 family's
   refusals stand unchanged.

*The routing:* ZERO rows convened (D-175 — the one fresh atom names
AGENTS §2.7, a standing law, never a queue row; the parked five keep
their first-consumer gates); zero build-grade items; the build queue
UNTOUCHED; no REFERENCES entry (a research-method re-edition, the
intake-34/36/37/38 class — never a donor source); no worldbuild
routing — the world track's own transfer law (WORLD_AUTHORING §19,
D-189) governs there, and a doctrine rework adds nothing to it.

**The testing-and-verification ultimate corpus routed (intake-40,
iter-255-doc10, D-233 — the owner's «продолжи работы с документами, я
согласен с вердиктами» call over the tmpfiles.org upload: the
2818-line "CanonSim — TESTING & VERIFICATION — ULTIMATE" (md5
a7c80d52b727d08c1c8eb8477dce9773), a second TEST_PLAN by content; the
document's own audit snapshot HEAD `41be836`/iter-216 (2051+1) — every
claim re-verified against HEAD `254411b`/iter-254 (2384+9) before
routing, a 38-iteration drift (iter-217..254: the wb family, the ssi
family incl. ssi-7's semantic_diff, ux/obs/inf, intake-38/39); the
document itself stays outside the repo, the convenience-copy law).**
The verdict: CONFIRMED-owned core + four fresh atoms + one fresh
defect; the document FORM refused — its own §4 forbids exactly that
("Never maintain: second TEST_PLAN"), AGENTS §6's substance-filtered
cap and §2.8's standing refusals (no second source of truth) concur,
and 2818 lines over a closed phase ladder is cruft-pass territory.

*Confirmed-owned (zero rows, zero doc edits — the D-024 duplication
law):* §2.1's epistemic classes + dispositions = TEST_PLAN §9's two
axes (D-171 + D-198); §6's T0–T8 engineering gates = TEST_PLAN §1
(richer: §1.3 the blind suite, §1.4 the semantic-diff companion, T8's
seed-125 pin matching); §8's M1–M5 meanings/limits = TEST_PLAN §2 —
except the M4 contract drift (the one genuine catch, below); §25's LLM
boundary 3 layers + live measures = TEST_PLAN §8 (testproto Layer
1/2/3) + §8.5's heartbeat ledger (the 4 station rows standing); §26's
world verification (reader + perturbation oracle) = WORLD_TESTS + the
world track's own law (D-186, WORLD_AUTHORING §19/D-189 — zero
worldbuild routing, the iter-253 precedent); §28's minimal-pair /
ablation / inactive-ablation-invalid = §9's empty-ablation rule +
the balance-harness arms (`--pacing`/`--systems-minus`/`--directors`);
§29's metamorphic/order probes = §9's order-probe contract (D-039 the
standing instance); §30/§36's mutation adequacy + blind spots =
§9's mutation prism + intake-37's MEASURED lesson (mutation visibility
is path-bound — release_threshold + probability mutations passed lint
AND the golden, iter-195); §31's evidence independence = §9's
independent re-derivation law (ssi-7 made it executable: semantic_diff
shares zero code with the checked path); §32's CRN/paired seeds/no
keyed RNG = LANDED `--paired-delta` (iter-183, D-195, the corpus CRN
verdict CONFIRMED as research methodology) + INV-2's RNG add-safety
(D-079); §34's change-triggered recertification = T1's
fixture-regeneration guard (every run: golden ↔ current schema_version
byte-check + §3 the migration procedure); §49's runtime-promotion
gate = AGENTS §2.8's admission law + intake-38's promotion gate
(D-199) — the same shape, already routed; §37's witness portfolio =
`tests/playscripts/` — all 11 witnesses exist and are the committed
gate/smoke scripts.

*The fresh material — one code defect, one contract pick, three parked
rows (each verified at HEAD, never trusted from the document):*

1. **P0-1 — the log reader accepts a stale schema_version header (the
   one CODE defect).** CONFIRMED at HEAD: `core/log.py::validate_header`
   checks the header SHAPE only; the append-mode writer checks version
   + interpreter ("a schema bump between runs is a migration, not an
   append"); `read_log` accepted a structurally valid header with ANY
   `schema_version` while validating the events against the
   caller-passed current schema — the writer/reader asymmetry, a
   reader-boundary defect per the repo's own migration law (§3). Routed:
   **KI#100** + the fix row **`log-1`** — read_log derives the expected
   version from the passed schema's `$id` (the writer's own
   `_extract_schema_version` path) and raises `LogError` on
   mismatch/foreign version; the canonical read seam (ssi-6's
   `workbench/canonical_read.py`) inherits it for free; a stale-header
   test case pins it. R2 (local behavior change), one iteration.
2. **P0-2 — the M4 semantics drift (doc ↔ code).** CONFIRMED: TEST_PLAN
   §2 M4(a) read `repeated_bigrams / total_bigrams` (the occurrence
   reading); `core/metrics.py::m4_novelty_repetition` computes repeated
   TYPES / distinct TYPES (pinned by test_metrics's `1/2 = 0.5` case);
   a skewed stream separates the readings. No longitudinal M4 threshold
   is load-bearing today (the phase gates closed; M4 rides the harness
   as a measured surface). Routed: **D-233** picks ONE semantics — the
   implemented, test-pinned type-based form stays, §2 worded exactly,
   the ambiguity + the historical note recorded in the D-row; a future
   "experienced repetition" consumer (if any) gets a NEW named metric
   (M4b), never a silent redefinition. Doc-only (R0), riding the
   routing iteration.
3. **P0-3/P0-4 — the temporal contracts (UNRESOLVED, research-first).**
   The §16.3 measured signal (wait(N) vs sliced waits diverging across
   state/relations/crime-status/event families) and §16.5/§22 (the
   late-tick autonomous talk clustering on province_calendar; 2288
   events ≈ 1098 decay + 722 watch + 265 talk) are contract questions,
   not proven bugs — the document says exactly this, and §11's
   authority law (define the intended contract first, never silently
   reconcile) agrees. Routed: the parked row **`temp-1`** with TWO
   gated halves (the parse-2 shape precedent): (a) the wait-slicing
   equivalence contract — declare the intended relation, then test it;
   (b) the autonomous-intent temporal semantics — assignment /
   scheduled / realized / canonical tick / recording separated, the
   contract selecting generate-at-T vs deferred-realize vs
   record-late-preserve-semantic-time. Zero code until the contract
   decision lands (AGENTS §2.4/§2.5).
4. **P0-5 — the action-to-consequence census.** Genuinely new as an
   INSTRUMENT; TEST_PLAN §9 already NAMES it (the mutation prism's
   strong follow-up — which paths the goldens actually bind), and
   intake-37 measured why it matters (the path-bound mutation escape).
   Admission via the existing-mechanism ladder (AGENTS §2.8): a minimal
   extension of mech-2's `scripts/mechanics.py` derived index (the
   forward direction: pack action → parser reachability → realized →
   canonical events → downstream consumers), output a REGENERABLE
   derived report (never a second truth — the document's own §4 law).
   Routed: the parked row **`cov-1`**, owner-gated; first consumers:
   the next pack gate + the mutation-escape falsifier.
5. **P0-6 — the future-divergence minimal-pair probe.** T8 is the one
   landed instance (director on/off); the harness owns the A/B arms;
   the genuinely-new half is the bounded BASE/PERTURBED semantic future
   comparison with first-divergence / causal-path / persistence
   records; the oracle already exists (ssi-7's
   `scripts/semantic_diff.py`, deterministic, zero shared code). Routed:
   the parked row **`div-1`**, owner-gated; first consumer: any "this
   creates new depth / changes reachable futures" claim packet
   (TEST_PLAN §9's first-prism row), pack-3's genre-portability arm if
   picked.

*Refused:* the document as a repo document (a second TEST_PLAN by
content, self-forbidden by its own §4, 2818 lines over the substance
cap, AGENTS §2.8's standing refusals — the convenience-copy law, the
iter-253 precedent); §5's INV-4 restatement ("exactly one surface:
cli/engine.py" — STALE by 38 iterations; AGENTS §4 owns the current
three-module form, D-193/D-201/D-208; never adopted from a snapshot);
§38's SC-* witness queue as a standing queue (speculative verification
build, D-175's zero-rows law — every SC reduces to an owned instrument
or one of the routed rows: SC-PLAYER-SURFACE = §8.5's station rows,
SC-HELDOUT has no standing generalization claim — pack-3 would be its
first consumer, SC-MUTANT-SENSITIVITY = cov-1's falsifier half + §9's
prism); §47's P2 observability optimization (behind the document's own
gate — "only after routing value is demonstrated" — plus AGENTS §2.4's
research-park law); §47's P1 set (parked behind first consumers: P1-1
the Province integrated witness — EXECUTED iter-261 on the owner's
explicit «prove composition» call (D-237, the record below);
P1-2/P1-3 the relation/object lifecycle matrices on the world track's
first engine-capability call, still parked; P1-10 the autonomous
timing witness — EXECUTED iter-261 as `mechanics.py timing` + the
composition witness's timing oracles, D-237); §34.2's periodic
portfolio recertification cadence
(no release candidate exists — pre-product; the change-triggered half
is already automatic in T1's guard; parked behind the first release).

*The routing:* KI#100 opened in STATUS.md (the one code defect) + FOUR
TASKS rows — `log-1` doing (the fix), `temp-1`/`cov-1`/`div-1` parked
behind their named gates — + the TEST_PLAN §2 M4 wording sync (D-233's
pick, doc-only, this iteration) + the intake-40 ledger line; zero
worldbuild routing (WORLD_TESTS owns it, the iter-253 precedent); no
REFERENCES entry (the research-method class); the build queue otherwise
UNTOUCHED.

**The temp-1 contract card (iter-257, the owner's «работай над temp-1,
цензус cov-1 и прочими» call opening the parked row — research-first,
zero engine code per the row's own law; the card is the fork record the
owner's contract decision reads; the interventions live in `scratch/`,
D-197, never staged).**

*Mechanism, measured at HEAD `a6b4547` (both halves share ONE root):*
`core/loop.py::_run_beat`'s enqueue law — "urgency and director intents
are enqueued at ``entry_tick`` (the tick of the entry the loop is
currently processing): the entry was already popped, and the queue
discipline forbids enqueuing at a tick the clock has already passed" —
so a beat-minted autonomous intent's DOOR tick is the LANDING tick of
whatever entry carried the crossing, never the beat tick. Under a long
wait the landing is the wait's completion tick; under slicing every
tick has traffic, so the landing ≈ the beat. The two families of canon
events disagree about when the world moved: the crossing-committed
families (decay / watch / calendar — committed inline at the crossing
tick) record at TRUE time; the door-committed families (urgency /
director intents — the whole door: preconditions, OCC, opposed checks,
completion) record at landing + duration.

*Half (a) — the wait-slicing A/B, 8 pairs over 4 seeds (125/42/7/1001,
tavern, the scratch runners):* the minimal pair ([wait 720] vs
[720 × wait 1]) — projection EQUAL at every seed, the only type delta
`wait +719`, fingerprints EQUAL; the crossing families never appear in
any delta (8/8 pairs). The day1_full pairs — seed-dependent door-family
divergence: seed 125 the coerce flip (span: the beat-720 intent lands
at the door t=732, the leverage card expired t=729 → `intent_rejected`;
sliced: the door at t=720, the card live → `coerce` at 723, the pair
relation trust 25 / fear 75 minted — a STATE divergence); seed 1001 the
cascade (`document_check`→`document_check_failed` flip, ±2
`suspicion_changed`, `arrest_attempt`/`arrest_resolved` appear, the
guards' suspicion props diverge, the FINGERPRINT diverges — the only
RNG divergence in 8 pairs); seeds 42/7 only `wait +1438` (the door
families happen to agree). Secondary mechanism: the wait resolver mints
hooks per EVENT (iter-53/KI#15 — idle time is the ambient tag's seed),
so 720 waits seed the ambient hook 720× vs 1× — the entropy budget
crosses the release threshold at a different beat (the minimal pair's
`ramble`: t=723 span vs t=363 sliced, fingerprints EQUAL — the timing
shift is seed-count-driven, never draw-driven).

*Half (b) — the province_calendar clustering, re-measured at HEAD
(seed 42, wait 519000):* 2288 events = decay 1098 + watch 722 + talk
265 + 203 others (the corpus's own numbers, byte-stable) — and the
clustering is TOTAL, stronger than the corpus worded: ALL 265 talks in
t ∈ [520069, 520073] (the last 5 ticks; the wait completes at 520065),
every single one from ONE urgency entry (`urgency_0004`, minted at each
of the 1083 fired beats, 265 accepted at the door, 0 rejections); the
decay/watch families spread evenly across the whole 519000-tick span
(bucketed: ~69-70 watch / ~104 decay per 50k ticks). The assignment ↔
canonical separation is the full span: intents assigned at beats
360..519480, all realized in the last 8 ticks. The five time notions in
the current implementation: assignment = the beat tick (the urgency
gate's fold read); scheduled = the beat + duration (never committed as
data); door = the landing tick (`entry_tick`); realized/recording =
door + duration (the completion event's t); canonical = the recording
tick (the log's truth — every downstream consumer reads it: decay
windows, echo folds, the chronicle).

*The fork (the owner picks ONE per half; AGENTS §2.7 — axes named,
disadvantages decomposed, a synthesis attempted):*

- (a) The wait-slicing relation: **A1 full equivalence** (wait(N) ≡
  N × wait(1) at every semantic family — requires span-aware hook
  minting + beat-anchored door ticks; both are (b)'s machinery, so A1
  is (b)'s contract wearing the slicing test) · **A2
  crossing-family equivalence** (declare: the crossing-committed
  families + the projection's non-door props are slicing-invariant —
  the measured 8/8 invariant; the door families FREE to diverge, the
  divergence causes named (the entry_tick law + the ambient seed
  count); testable TODAY at zero engine change, the honest
  measured-contract form) · **A3 documented non-equivalence** (the span
  is one idle unit, never N moments — the minting law's own reading;
  A2 minus the test). Recommendation: **A2** — it pins what the
  measurement already holds, names what is free, and leaves the deeper
  semantics to (b)'s decision.
- (b) The autonomous-intent temporal semantics: **B1 generate-at-T**
  (the intents' doors evaluate at the beat tick — the clock IS at the
  beat during `_run_beat`; but the completion still records at
  max(clock, beat+duration) = the landing unless the scheduler becomes
  a continuous clock-walk popping queue entries as the clock passes
  their ticks — a queue-key/tick-semantics change, AGENTS §8's
  stop-and-confirm territory, and the door-inline form re-derives the
  OCC/precondition world at beat time: the honest fix and the deepest
  one) · **B2 deferred-realize (current, declared)** (the intents fire
  "after the beat, at the moment the world resumes moving" —
  `_run_beat`'s own docstring; under a long span the world resumes only
  at the landing: the states decay across the year while nobody acts
  until its last 5 ticks — coherent only as "the door is the world's
  resumption", which the clustering makes visible as a world-model
  incoherence) · **B3 record-late-preserve-semantic-time** (the event
  records at the landing (B2's scheduler untouched) but carries the
  assignment tick in provenance — a schema addition (R4,
  owner-gated), the consumers can read both times; the synthesis
  attempt per §2.7: B3-with-beat-anchored-doors (the door evaluates at
  the beat, the completion records at the landing, both times named in
  provenance) satisfies B1's fold-coherence and B2's scheduler
  stability but keeps the recording/canonical gap — an honest
  improvement, not a dissolved trade-off, and it buys a schema change;
  discarded as a synthesis, offered as B3's own form). Recommendation:
  the fork is REAL and owner-owned: B2 costs nothing but documents a
  visible incoherence; B3 names both times for every future consumer
  at one schema-field price; B1 is the world-coherent form at a
  scheduler-law price. The card records no pick — AGENTS §11 (never a
  silent reconciliation).

*The falsifiers (whatever the pick):* A2's test arm = the 8-pair A/B
pinned as a contract test (the crossing-family invariance + the
projection equality on the minimal pair); B1/B3's test arm = the
province_calendar witness re-run (the talk spread across beats vs the
last-5-tick pile); the probe for any pick = div-1's first-divergence
records over the same minimal pairs.

**The temp-1 decision record (iter-260, D-236 — the owner's 2026-09-26
pick over the card above: A2 + B2/B3, B1 deferred; the card's two
halves are now CLOSED contracts, the standing law per half):**

- **A2 — crossing-family equivalence IS the slicing contract.** The
  declared scope (tavern): the crossing-committed families
  `status_decayed` / `watch_change` / `knowledge_transfer` /
  `expectation_violation` are count-invariant across `[wait N]` vs
  `[N × wait 1]` at the four measured seeds (125/42/7/1001); the
  minimal pair additionally pins projection + RNG-fingerprint
  invariance (the only type delta: the wait events' own count).
  **Full slice equivalence is NOT claimed** — the door families
  (player steps + autonomous urgency/faction/director intents, the
  whole OCC/opposed-check/completion chain) are FREE to diverge (the
  entry_tick enqueue law + the per-event ambient minting), and the
  known divergences (seed 125 the coerce flip, seed 1001 the
  document-check cascade + the one fingerprint divergence) are PINNED
  as regression guards — a future change that silently "fixes" them
  has changed runtime semantics, not healing. One measured boundary:
  a crossing event whose PAYLOAD reads the knowledge fold (a rotation
  briefing's `count`) can reflect door divergence (seed 1001: count 2
  vs 3) — family counts are the contract, payloads are inside the free
  surface. The contract executable: `tests/test_temp1_contract.py`.
- **B2 — deferred-realize REMAINS the runtime semantics** (observed,
  declared — never "a bug"): the beat-minted autonomous intent's door
  lands at the world's resumption tick; under a long span the world
  resumes only at the landing (the province_calendar witness: all 265
  talks still realize in the last five ticks [520069, 520073],
  unchanged by this landing). No scheduler, queue, tick, or ordering
  change is made or implied.
- **B3 — provenance records the semantic origin separately from the
  canonical realization** (`provenance.assignment_tick`, schema
  0.2 → 0.3 additive over the cause_hook precedent, EVENT_SCHEMA §7):
  the beat/crossing tick an autonomous intent was minted at, stamped
  at the ONE enqueue door (`_enqueue_autonomous`, the
  `based_on_event_seq` precedent) and carried to accepted AND rejected
  resolutions alike; player intents never carry it (a playscript
  step's assignment IS its enqueue tick). `event.t` stays THE
  canonical timestamp — B3 records the deferral (`event.t -
  assignment_tick`, up to 518269 ticks on the witness), never
  re-times, never back-fills, never de-clusters. The measured
  before/after evidence: every canonical field of every affected
  scenario byte-identical to BASE (the five fixtures regenerated:
  header bump + 4/1/6 assignment_tick lines on province/road/pressure,
  plumbing/grim header-only), fingerprints unchanged on all eight A/B
  arms.
- **B1 — generate-at-T stays DEFERRED**, an owner-gated future
  scheduler decision, never this row's work. The reopening conditions
  (the card's standing list, unchanged): a named runtime consumer that
  needs generate-at-T; deferred realization shown as a repeatable
  MATERIAL failure (not a stress-case artifact); a measured
  product-level quality gap not closed by B2+B3; the scheduler shown a
  native limitation; an owner/phase gate on the temporal-law change.
  Until then B1 is a PROPOSAL, never an implementation requirement
  (the §9 epistemic law).

**The iter-261 composition record (D-237 — the owner's iter-261 brief
over the parked intake-40 P1 set; P1-1 opened by the explicit «prove
composition» call, P1-10 = temp-1's half (b) test arm):**

- **P1-1 EXECUTED — the Province integrated witness**
  (`tests/playscripts/province_composition.json`, province_pack@0.1
  seed 2, EXISTING verbs only, zero new content; the executable
  `tests/test_p1_composition.py`, 16 RELATIONAL oracles, no golden
  snapshot). One run, 2371 events, six interacting chains end-to-end:
  the crime family (the failed pay-tin steal → the witnessed knowledge
  mint → three leverage clusters → the suspicion stack → the WATCH
  ROTATION's briefing carrying the whole stack to the relief → the
  sergeant's `document_check` (urgency_0001) crossing the arrest bar
  co-located → the arrest → `caught` irreversible) + Loop A's guild
  arm (arson → alarm → fear → `guild_councils`, faction_0000 through
  the door) + Loop B (both elders' grief → the deadband → the vigil
  ×4, INCLUDING the year-later re-fire at t=525335 off the decay-0
  residue — the persistence→future-option oracle) + Loop C (the full
  calendar year 36/12/4/1 + the seasonal ride, the thaw's storm) +
  the macro economy (the year turn's four account flows) + Loop D
  (the first-beat condensation) + the ambient band (287 talks, 730
  rotations, 22 rumors). The honest gaps classified per the §14 law:
  the garrison arm and the storm murmur stay at their own committed
  witnesses (test_triangle seed 139 / test_weather) — witness-window
  limits, never missing mechanics; the scene LOD scopes five urgency
  families out of this route entirely (structural, depth-3).
- **P1-10 EXECUTED — the timing witness** (`scripts/mechanics.py
  timing`, the first NAMED `assignment_tick` consumer outside the
  contract test): the composition corpus's two-times surface — 383
  autonomous resolutions, ALL carrying the origin (B3's discipline),
  latency 7..518861 (mean 247898), the early window's chains closing
  at ≤1656, ONE OCC miss (director_0001 at 2520 → t 3449, latency
  929: the duty rotation moved the sergeant inside the deferral
  window — the province's own seed-125-class instance).
- **cov-1's runtime arm** (`census --log/--script`, the A..H loss
  vocabulary over one run): the measured verdict over the composition
  run — A 1 · B 3 · C 5 (three structural LOD + the gates/rolls) ·
  D 1 · E 2 (the faction answers quiet: their consumer the tale
  render, never the projection) · F 0 · G 0 · H 10. **The losses sit
  in assignment and consequence, never in the scheduler.**
- **The H1/H2 season-scale sliced pair measured** (span vs
  129600×wait-1, the temp-1 transform, semantic_diff + the family
  deltas + the final projections): the MATERIAL chain outcomes
  IDENTICAL (arrest/caught/council/vigil/burnouts/leverage), the
  crossing families invariant (A2's law at province scale — decay
  300/300, watch 189/189, transfers 5/5, markets/fairs/seasons 1:1),
  the deltas door-only (intent_rejected 20→0, checks 1(+0)→11(+10),
  exactly two final-projection props — the pair suspicions). The
  deferral does real work at the door (the OCC losses scale with the
  span; the year-scale witness accepts 86 checks at ONE landing tick
  by the rotation's phase there), but no material trajectory change
  at this substrate — H2 holds at the measured band with the named
  boundary: the deferral becomes material exactly where an EXPIRING
  gate or a mid-window consumer exists (the tavern's seed-125
  leverage-expiry class).
- **The provenance fix (the brief's §3):** `province_calendar.json`
  is a THREE-step temporal stress shape (two moves + one 519000
  wait; all 265 talks one urgency entry) — the 265/265 clustering is
  NOT integrated-world evidence; the composition witness above now
  carries that claim with explicit provenance.
- **B3's consumer status (the brief's §9):** UNRESOLVED for
  production — the standing named consumers are the contract test +
  the timing instrument (diagnostic); no chronicle/observatory/
  runtime reader exists. The demotion question (permanent schema vs
  research-only) is an owner call on the report's F proposal — no
  schema churn now, no rollback.
- **B1: NO promotion evidence acquired** (the H2 verdict at the
  measured band; the losses substrate/integration, never the queue
  law) — the reopening conditions unchanged.

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
