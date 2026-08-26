# Live Character Guide · `REFERENCES.md` §9 · MIT (LICENSE file present — verified 2026-08-27) · track A (iter-2+ observability discipline) + track B (phase-1 brief layer) / phase 6 (pack authoring lint)

> Per-reference deep dive. Format template: `REFERENCES_DEEP.md` §0. Iteration
> plan: `REFERENCES_DEEP.md` §1. Anti-drift (D-026): catalog/license/URL/phase
> gating in `docs/REFERENCES.md`; one-line synthesis in
> `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics here. License filter
> and "patterns not content" rule: `REFERENCES.md` §0.7 (D-015).
> Source: `github.com/vudirvp-sketch/live-char-guide` — the owner's own
> project; guide v9.2.6, MIT LICENSE file read in full (2026-08-27). Read in
> full: `docs/canon/` — parts 00–10 + 4 appendices, ~4700 lines, the repo's
> declared single source of truth for content — plus
> `data/character_schema.json` (684), `data/ocean.json`,
> `data/enneagram.json`, `docs/elena_character_bible.md`,
> `docs/vyshcherblenny_character_bible.md`. Scope per the owner's request:
> the guide's **content and meaning** (the card methodology), not the webapp
> engineering (build pipeline, widgets, visual system).

**What it is.** A single-linear-flow methodology (10 Parts + 4 Appendices)
for building RP character cards for 12B–32B+ models (SillyTavern-compatible)
that treats the card as a **behavioral engine**: every element must produce
an observable action, never decorate a description. Pipeline: SPINE
(psychological causal chain) → Behavioral Anchors (Trigger → Action → Price)
→ Voice Isolation → System Prompt assembly → anti-patterns → diagnostics.
The machine-readable mirror `data/character_schema.json` turns the whole
methodology into a checkable contract: `spine.want/need/flaw` required,
`anchors` minItems 3 / maxItems 12 with `trigger/action/price` required on
every item, `examples` minItems 2, OCEAN values as integers 0–100.

**Concrete mechanics.**

- **SPINE — the causal chain `GHOST → LIE → FLAW → NEED → WANT`.** GHOST is
  a concrete past event, never a label ("at 7, watched the house burn while
  the firefighters were late", not "childhood trauma" — the guide bans
  trauma-conclusion words outright); it begets LIE, a quoted false belief
  protecting from that pain ("I don't need anyone's approval. I work
  alone."); LIE distorts perception into FLAW, a concrete maladaptive
  *behavior*, never an adjective ("pushes people away with sarcasm when
  they get close", not "cynical"); FLAW blocks NEED, the true need the
  character does not recognize; WANT, the conscious goal, is **compatible
  with LIE** (the character sees no contradiction) and stands in **tension**
  with NEED (right-vs-closeness). Every element is an "observable unit" —
  the §4.9 consistency checklist is a causality audit over the chain (each
  element must explain the next; "WANT compatible with NEED" = broken
  SPINE, AP-9). **GHOST Layers** (G1 core/childhood → LIE, G2 reinforcement
  /youth → FLAW, G3 present-day triggers) extend this for multi-trauma
  characters; the canonical degradation counter — "after the 3rd extraction
  he no longer remembers his name, after the 5th why he helps, after the
  7th what 'help' means" — is capability loss expressed as an event count.
- **Behavioral Anchors — `Trigger → Action → Price`.** The Price is the
  load-bearing invention: an **immediate, physical, same-scene observable
  cost** of the behavior (someone lies → she squints, goes silent → jaw
  tension). "Will regret it later" is explicitly rejected as a Price — no
  deferred, abstract, or emotional prices. Anchor quality rules: action
  observable (seeable/hearable, not internal state); price physical; price
  in the same scene; trigger concrete ("when asked about the past", not
  "when he's sad"). Anchor types derived from SPINE: FLAW-linked
  **mandatory** (every FLAW ≥ 1 anchor), GHOST → sensory (5 channels:
  tactile/auditory/olfactory/visual/proprioceptive), LIE → psychological,
  WANT → at-rest, NEED → growth. Budget: 3–5 anchors for calm/stress/joy/
  talk coverage, 5–7 with FLAW/embodiment, 7–12 with CoT/sensory.
  Atomicity rule: one anchor = one T→A→P link; nested conditions ("when X,
  and if Y before that, then Z") are AP-15 and must split.
- **Embodiment Protocol — `State → Body → Sensor → Speech`.** Every
  emotional state must surface physically before speech: weight/balance/
  breathing/micro-movement → tension/relaxation/tremor → texture/sound/
  smell/temperature → tone/pace/volume/lexicon. The sensor layer is the
  result of the body's contact with the environment through action, never
  a decorative aside.
- **Voice Isolation.** The governing empirical claim: the model is a
  **pattern matcher, not a rule executor** — style directives without
  examples get 40–60% compliance on ≤14B. Linguistic voice (words,
  syntax, lexicon, rhythm, paradoxes) lives **only** in Examples +
  Greeting; physical voice characteristics (timbre, rasp, mechanical hum)
  count as embodiment facts and may live in Description. The influence
  hierarchy (12B): recent chat ~85%, examples ~10%, greeting ~3%,
  author's note ~2%, description **0%** — style tokens in Description are
  wasted or harmful. Multi-character scenes require ≥3 distinct voice
  markers per character or the voices bleed (AP-11); one `<START>`
  delimiter per example block, or patterns leak across examples.
- **CORE DIRECTIVES — the 7-directive generation "operating system"** in
  the System Prompt: (1) Show Never Tell; (2) Embodiment First
  (State→Body→Sensor→Speech, always); (3) Spatial & Anatomical Lock —
  track distance, posture, weight, line of sight; no teleportation, no
  anatomical contradictions; (4) Environmental Reactivity — sensory and
  spatial details enter only through character action or presence, never
  as decoration; (5) Influence Boundary — react only to the other party's
  **observable symptoms** (may notice a flinch; may not declare "he is
  scared"); (6) Consequence Driven — WANT shifts toward NEED as Price
  accumulates over the session; (7) Pre-Generation Filter — verify
  embodiment, observability, zero-meta before every response. Around
  them: anti-godmoding (2 lines: prohibition + positive formulation),
  Tone Frame (~25–30 tokens: tonality + content-drift guard), Format Lock
  (exactly one markup system; on conflict the model follows the example,
  not the instruction), OOC Protection / Immersion Boundary.
- **OCEAN / Enneagram as validators, not generators.** Numeric OCEAN tags
  (`<ocean>O:72 C:65 E:41 A:38 N:68</ocean>` — numbers read as patterns
  better than prose); the **1–2 extreme-poles budget** (<30 / >70 — more
  extremes = internal conflicts the model cannot resolve consistently;
  cautious zones 30–40 / 60–70 still carry SPINE links); stress types
  derived from N (anxious-reactive / explosive-hostile / avoidant-
  withdrawn / stable-resistant), each requiring ≥1 explicit
  trigger→stress-type→FLAW→anchor chain or it stays an abstraction;
  Enneagram's 9 types cross-validate SPINE (core fear→LIE, core desire→
  WANT, stress direction→FLAW, growth direction→NEED). Rule: build SPINE
  first, validate with the frameworks — never assemble SPINE bottom-up
  from psychometrics.
- **CoT — Tier 0–3 internal process.** Tier 0 = embodiment only; Tier 1 =
  `[INTERNAL: …]` label; Tier 2 = INTERNAL block tied to the GHOST
  connection; Tier 3 = `<processus_analysium>` XML with stimulus /
  analysis / counter-analysis / synthesis / resolution. Hard budget:
  2–3 CoT anchors per card — beyond that the character thinks instead of
  acting (AP-10).
- **Lorebook — injection scheduling, not lore storage.** Entry =
  Key / Content / Position / Depth / Probability / Cooldown. Behavioral
  mechanics: range-cascade (`min_msg`/`max_msg` stages — automatic plot
  progression replacing manual note updates), combo-trigger (`sticky`
  3–5 + cooldown 20–30 — temporary behavior modes without personality
  drift), context filter (depth 3–5 + `exclude_key` — cuts false
  triggers). Recommended parameters: context/GHOST facts depth 2–4,
  probability 80–100%, cooldown 5–10; world entries depth 0–1,
  probability 30–50%, cooldown 15–20; 2–3 mechanics per session. Hard
  rule: never place `{{user}}`'s actions or thoughts in `content`
  (anti-godmoding applies to data, not just prose). Author's Note:
  position 3–5 messages from the end, 100–200 tokens, refreshed every
  5–10 messages; templates carry State / WANT→NEED balance /
  GHOST-activation / Blind Spot.
- **Anti-patterns — 15 APs, each symptom → cause → fix:** AP-1 token
  bloat; AP-2 missing price; AP-3 voice in description; AP-4 psychology
  in SP; AP-5 RepPen > 1.10; AP-6 no anti-godmoding; AP-7 presence
  penalty > 0; AP-8 GHOST without anchors; AP-9 broken SPINE; AP-10 CoT
  overload; AP-11 voice bleed; AP-12 malformed XML; AP-13 lorebook
  conflicts; AP-14 context violation; AP-15 nested anchors.
- **Diagnostics.** Four-zone quality scale (target "Good" 50–85%, not
  "Excellent" — polish is for production); symptom table (symptom →
  check → fix reference); decision tree; **6 test scenarios** — neutral
  greeting, conflict/stress, sincere care, personal probe, 10+ turn
  longevity, multi-char scene; **6 success metrics** — voice stable at
  10+ messages, Price appears in every 2–3 responses at trigger, FLAW
  manifests under conflict, 0 godmoding per 10 messages, 0 style
  directives in Description, AN measurably changes behavior; the
  **one-change rule** — never change more than one parameter per test
  cycle (change → test 5–10 messages → evaluate → next); pre-deploy
  validation: 5 quick checks (PP=0, voice only in examples, price in
  every anchor, format lock, anti-godmoding) + 14 full checks.
- **Methodology honesty.** The guide itself disclaims its percentages
  (~40%/~10% voice drift, ~85% recent-chat share) as empirical markers
  from ~50 cards on 2024–2025 12B–32B models: "qualitative markers
  (stable / drifts / broken), not precise measurements".

**What we take.**

- **"Every element must produce an observable action" = our event law.**
  The card discipline and the causal-density checklist (`MVP_SCOPE.md`
  §15) are the same law discovered from opposite ends: an element that
  changes nothing and seeds nothing is dead data. Their AP-2 (anchor
  without Price) is our "bad event: tried to steal — failed (the world
  did not change, nothing to grab)". After UAP §0.6 this is the second
  independent external convergence on "quality must be countable over
  observables" — now at character granularity, not world granularity.
- **Price as the immediate-observable half of consequence.** D-005 owns
  the deferred half (hooks seeded at event time); the guide adds the
  immediate half: a socially meaningful behavior must carry a
  same-scene observable marker — a knowledge record or a perceivable
  state token — or it is socially invisible. For iter-2 this is a
  pack-rule design pattern (outcome payloads include the perceivable
  marker alongside state deltas and hooks) and a causal-density
  checklist wording change ("what did witnesses perceive of the price
  paid?"); no schema change, no new field.
- **Influence Boundary as a candidate iter-2/3 architecture rule.** The
  strongest single design transfer: NPC behavior functions read **own
  state + own knowledge only**; other entities' internal states enter
  exclusively via perception of their observable markers (embodiment as
  the states→observables mapping). The guard cannot react to the
  drunkard's intoxication field — only to slurred speech arriving as a
  `heard` record. This closes system 5 (states) into the perception →
  knowledge chain instead of leaving it a private numeric layer, makes
  "who can be wrong" (`MVP_SCOPE.md` §15) answerable per observer, and
  is the narrative-side statement of T3/blind-NPC. Recorded here as a
  candidate rule for the iter-2/3 system design; adopting it as law is
  an owner call, not a ref-file decision.
- **Voice Isolation / pattern-matcher as the brief-layer law (track B,
  phase 1).** The brief must never *describe* style — it carries facts
  as structured tokens, and style lives in template exemplars. The
  recency-dominant influence hierarchy (~85% recent chat on 12B) is
  direct design data for `BRIEF_SPEC.md`: recent-facts-first assembly,
  exemplar/voice block injected near the context end (their AN numbers:
  position 3–5 messages from the end, 100–200 tokens, every 5–10
  messages), and the lorebook scheduling parameters (depth /
  probability / cooldown / sticky / range-cascade / exclude_key) as a
  proven injection-scheduling grammar for context injection.
- **The AP catalog → pack-lint vocabulary (phase 6, `PACK_SPEC.md`).**
  All statically checkable over pack data: spine-shaped records with
  want/need tension and flaw rooted in a cause (AP-9); every flaw/deep
  trait connected to ≥1 behavior rule (AP-8 — "GHOST without anchors" =
  dead pack data); no two NPCs sharing identical trigger→action pairs
  (AP-11 clone check — the design-time twin of M4 novelty); no
  contradictory pack rules (AP-13); rule atomicity (AP-15); pack size
  budgets (AP-1). Converges with the UAP teleology gate on "dead data =
  no observable consequence".
- **Test discipline.** The 6-scenario battery maps onto playscript
  design (neutral/stress/care/probe ≈ our walkthrough variants;
  longevity ≈ T6 1000-tick; multi-char ≈ the market scene); the 6
  success metrics all have log-computable analogs (voice stability →
  M4 novelty; price appearance → state_changes + hooks presence;
  godmoding → actor-discipline asserts); the one-change rule is our
  single-factor A/B on identical seed (T1/T8) stated as general
  experimental method — one factor per run, or you learn nothing.

**What we adapt.**

- **SPINE as pack metadata — never core schema or core code (INV-3).**
  The naive transfer — spine hooks as core event fields, a
  `generate_spine_hooks(event, npc)` in core code — would embed domain
  words and psychology into the engine; rejected. Correct route:
  `content/tavern_pack/entities.json` NPC records may grow optional
  spine-shaped data (formative past events, sustaining belief, flawed
  behavior, blocked need, stated goal — display English per D-009);
  generic behavior rules in `rules.json` reference those fields by path
  exactly as suspicion thresholds are referenced today. The core learns
  zero new words; the pack gains a causality-auditable character layer
  that phase-6 lint can check statically (tension, rootedness,
  connectivity — the §4.9 checklist as a pack check).
- **OCEAN / stress types as numeric pack data + modifier tables.** The
  extreme-pole budget becomes pack authoring guidance (PACK_SPEC: 1–2
  extremes per NPC; cautious-zone values must link to a behavior rule);
  stress types become modifier tables in `rules.json` applied through
  existing systems — perception penalties, suspicion deltas, relation
  decay — never a parallel personality engine, never five live scores
  per NPC in runtime state. The numbers-over-prose rule validates our
  structured `knows` tokens (models read structure as patterns better
  than narrative).
- **GHOST Layers → backstory layering + counted degradation.** Backstory
  layers as pack data with per-layer trigger keys; the degradation
  counter (capability X lost at the Nth event of class C) is a fold over
  counted events — the event-sourced form of character decay, relevant
  to phase-4 memory work; never wall-clock decay without events.
- **Consequence Driven → relation drift as a fold over price-bearing
  events.** The guide's WANT→NEED shift driven by accumulated Price maps
  to iter-3/4 relations: trust/reputation drift keys off *cost-bearing*
  events for that NPC (events that carried an observable price for
  them), not off scene count or director decisions — long-arc character
  change is event-sourced, like everything else. Candidate pattern for
  the P2a relation map design; not new law until it lands in an iter.
- **Their empirical percentages stay shape, not thresholds.** Our law:
  thresholds come from the iter-6 measured baseline (`MVP_SCOPE.md`
  §15). The guide itself marks the numbers as qualitative markers — we
  cite the shapes (recency dominates; description style-directives are
  dead tokens) and invent no numeric gates from them.

**What inspires us.** The phase-1 brief assembler is a **card generator**:
a card is a static behavioral engine over authored data; our brief is a
dynamic one assembled from the log. SPINE fields come from entity pack data
plus live folds; facts travel as structured tokens; voice stays in template
exemplars; every behavior carries its Price. The guide is what a mature
prompt-side craft converged to when it demanded the same things our
invariants demand — observability, causality, consequences — without an
event log to lean on. Where UAP audits worlds, this engineers characters:
together they are the two halves of the phase-1 narrator's input contract.

**Strengths.** Every rule is operationalized — an observable, a count, a
budget, or a test scenario, never a vibe; the Price concept gives
"observable consequence" a concrete same-scene unit, which even our §15
checklist only implied; the AP catalog is a complete symptom→cause→fix
loop, the exact shape a lint ruleset wants; diagnostics are countable and
honest about their own estimate nature; the machine-readable schema mirrors
the prose methodology — the same docs↔schema pairing discipline as
`EVENT_SCHEMA.md` ↔ `schemas/event.schema.json`; MIT LICENSE file present
and verified (2026-08-27) — unlike UAP, both content and patterns are
liftable with attribution; the owner's own project: zero negotiation cost.

**Weaknesses.** (1) **Prompt-side compensation machinery**: token budgets,
PP = 0, format locks, 4K fallbacks, Script Tax exist to patch LLM
limitations that phase 0 does not have — track-B-only value, never core
law. (2) **Self-disclaimed estimates as numbers** — the ~40%/85% family is
unusable as thresholds under our baseline-first law; the guide agrees.
(3) **Psychometrics as validation**: OCEAN/Enneagram/MBTI are narrative
tools, unfalsifiable as mechanics; porting them as runtime systems would
violate INV-3 — they stay authoring-side pack data and lint guidance.
(4) **Canon-breaking mechanics by design**: false memory (unfalsifiable
memory injection, "strictly dosed" or not) and fatigue emulation (hidden
context-window degradation narrated as character trait) are precisely the
inversions INV-1/INV-5 exist to prevent — in our world the first is a
crafted lie record with provenance, the second is explicit events or
nothing. (5) **Human-judged gates**: pre-deploy checks are
read-by-a-person; our equivalents must be log-computed (M1–M5), with
humans only at T7. (6) **Single-character focus**: no world model, no
NPC↔NPC epistemology, no knowledge transfer, no space — nothing here
feeds systems 2/4/6; that remains DF Legends / Paradox territory.
(7) **No runtime verification**: every check is design-time over the
card; nothing validates the session as it runs — the exact gap our
fold(log) metrics fill.

**Verdict.** The character-depth donor: Price/observability discipline and
the AP→lint vocabulary for phase-6 pack authoring; the injection-scheduling
grammar (voice isolation, recency hierarchy, lorebook parameters) for the
phase-1 brief layer; the Influence Boundary as a candidate track-A rule
that sharpens T3 and closes states into the perception chain; and
independent prompt-side validation that dead data, unpriced behavior and
unobservable influence are the enemies our invariants already target. MIT
and the owner's own: lift patterns and content freely.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
