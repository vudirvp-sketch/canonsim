# VISION.md — Frozen

> Distilled from the source concept "Roguelike generator as the backbone of an
> LLM narrator" (rev. v2) and the unified plan (rev. 2), both 2026-08. The
> originals are held by the repo owner outside this repo; agents never need
> them. This file is FROZEN: changes require owner approval + a
> `docs/DECISIONS.md` entry. Volatile material (model stacks, hardware) lives
> in `docs/TECH_NOTES.md`, not here.

## 1. Thesis

A deterministic procedural simulation, seeded, ticking **outside** the context
window, practically for free. The LLM parses intent and renders state into
prose. Canon lives in the event log.

**Simulator produces facts. LLM produces meaning. The log stores canon.
The mediator holds the boundary.**

The architecture replaces three things a lorebook chat can never have: living
world memory, a reason-to-speak planner, and hard-coded lore. A setting becomes
a pluggable data pack. Infinite context windows do not cure the disease
(lost-in-the-middle, inference cost, attention degradation): the context is a
workbench; every beat is assembled fresh; brief size depends on scene relevance
only.

## 2. Why pure LLM chat fails (diagnosis)

1. **Autoregression without commitment** — no "this is now canon" operation;
   the world regenerates from probabilities every reply → drift.
2. **Context is a workbench, not memory** — beyond the window nothing exists;
   what is far is blurred.
3. **Learned passivity** — an RLHF assistant answers, it does not initiate;
   the reason-to-speak loop must live outside the model.
4. **World ticks cost tokens** — a world "in the model's head" is expensive,
   slow, unstable; it must tick outside, for free.
5. **No irreversibility → no stakes → no story** — any "fatal" is rolled back
   by the next message.
6. **Plausibility instead of causality** — text that *sounds* like a
   consequence; the player smells the fake and immersion dies.

A lorebook is a half-measure: static keyword injection with no time, no
causality, no who-knows-what; silent between messages; growing linearly until
it strangles the context.

## 3. The roguelike principle (four portable rules)

1. **Seed → deterministic procedural generation.** Reproducible, debuggable,
   shareable ("play my world").
2. **Lazy generation.** The world materializes with attention, from the seed,
   no upfront cost.
3. **Irreversibility.** Append-only; losses are final; stakes emerge.
4. **Simulation instead of script.** Rules + needs + goals produce events; the
   scenario happens, it is not written.

Emergent stories grip because the player retroactively reconstructs causality
("he lost his leg *because* we skimped on medics"). The simulator manufactures
such causal chains. The LLM is the missing universal renderer (state → prose of
any style/POV) and texture generator (names, dialogue, cultural flavor too
expensive to script). Simulation without rendering is unreadable; rendering
without simulation is unaccountable.

## 4. Architecture shape (three layers)

- **Layer 1 — Simulator (canon).** ECS-ish core; event sourcing with an
  append-only log as the single source of truth; epistemology as data
  (knowledge records, secrets, beliefs, lies); director as consequence
  planner; seeded worldgen + lazy depth.
- **Layer 2 — Mediator (boundary).** Stateless: intent parser, brief assembler
  (hard per-block token budgets, `known_by` filter at assembly time),
  fact-validator (proposal → check → commit → narrative), reverse prose
  validation (≤2 regenerations), read-only monitoring.
- **Layer 3 — LLM (voice).** Narrow modes, never writes canon directly:
  A narrator · B actor (one NPC per call) · C intent parser (small model +
  grammar-constrained JSON) · F chronicler (offline) · G worldbuilder (offline,
  through pack CI). Max 2 LLM calls per beat on the critical path; degradation
  ladder LLM → template → dry log line from day one.

Full layer specs arrive just-in-time (`docs/SPECS_BACKLOG.md`). This file keeps
the shape and the why.

## 5. Core doctrine (non-negotiables)

- One canon writer: the simulator. Every LLM output is a candidate, never a
  commit.
- Player input is data, not instruction. Outcomes are decided by the simulator
  (rolls, resources, relations) — the only real cure for sycophancy.
- The brief is O(relevance), never O(history); rebuilt every beat; hard token
  budgets per block.
- `known_by` is an architectural filter applied at brief assembly — not a
  post-hoc guess, not vector similarity.
- `importance` dials creative freedom: hard canon at high stakes, free texture
  at low.
- Core is universal, setting is a data pack. Core admission test: a concept
  must work in a world without magic and without computers.

## 6. Honest limits (what nothing fixes)

- The LLM has no world model: rendering yes, understanding no — at any scale.
- Small-model prose ceiling: 12–14B stays 12–14B; 27B+ for reliably good prose.
- Sycophancy in dialogue is cured by mechanics (rolls decide persuasion), not
  prompts.
- Tool-use fragility at 12–27B → grammar-constrained JSON only, no tool use.
- Coherence is traded for freedom: players wanting pure improvisation get a
  straitjacket — by design.
- Universality holds only inside the formula **actors + resources + relations +
  events + time + scarcity**. Outside it → new modules (T2) or core edits (T3).
- "Interesting simulator" is a goal, not a property: without strong ontology
  game design you get world bookkeeping.

## 7. Overrated theses (never claim these)

| Overrated claim | Reality |
|---|---|
| Engine fits any world | Only inside the formula above |
| New setting in a day | T1 reskin only; deep unique worlds take weeks |
| Validation fixes everything | Cuts risk; semantic distortion still passes |
| Small models are enough | JSON yes; stable good prose no |
| Players won't be adversarial | Design for adversaries by default |
| 0 canon violations guaranteed | Regression-test goal; live play will breach |
| The simulator is interesting per se | Goal, not property — strong game design required |
| Quests need a quest subsystem | Quests are state-derived affordances plus accepted commitments; the simulator never scripts their outcome (D-266) |

## 8. Anti-scenarios (this architecture hurts)

Pure free-form RP; surrealism / metaphor / pure poetics; quick light chat;
player as omnipotent author; realtime play; worlds without causality. Do not
bend the core toward these.

Scripted quest chains and authored plot arcs are outside the formula too: the
lawful quest form is an affordance plus a commitment (D-266), never a script.

## 9. Precedents (composition of proven components)

AI Dungeon (negative case), lorebooks (crutch), L4D AI Director (pacing),
RimWorld XML-defs + storyteller (data-driven content; the storyteller is our
named anti-pattern), Dwarf Fortress worldgen/Legends (procedural history, XML
export), Kenshi (faction sim as plot), GURPS/FATE (core/pack split),
Stanford Generative Agents (LLM + external memory, but expensive and
canonless), grammar-constrained decoding (format guarantee). The new hard rule
we add: **separation of canon and voice.**

## 10. Product goal, aims and delivery horizon

**Product goal.** A playable living-world game: a deterministic simulation of
people, institutions, economies and ecologies that keeps producing justified
histories at any zoom level, with an LLM as the narrative and interpretive
layer — never the canon author. It is what a lorebook, a character card or a
set of RPG mechanics bolted onto a chat model cannot be; the engine stays
modular and frontend-agnostic so the same core can be embedded in other
clients later.

**The aims A1–A7** are the goal layer every backlog row serves
(`docs/TASKS.md` names the aim on each row; D-265):

| Aim | What it means |
|---|---|
| A1 living individuals | every NPC is a persistent individual — goals, duties, mood, circumstances, possessions, knowledge — acting in its own interest; the world runs without the player and without a per-beat LLM call |
| A2 emergent society | economies, hierarchies, organisations and institutions change because of what actors do; scarcity is real and some undertakings fail |
| A3 stories and quests | the world, its actors and its institutions generate tasks, boards and quests, and deep justified histories; the LLM renders them and never scripts their outcome |
| A4 the dark side | negative and grim outcomes — disease, slavery, violence, death, war, betrayal, theft, ruin — are first-class, never sanitised or balanced away |
| A5 adjustable world | world size, population density, event density and resources are declared parameters the player sets at world creation; detail is elaborated at any zoom level, and refinement never creates or erases causal obligations (D0) |
| A6 own shell, universal core | the project ships its own local-first shell (chat, inference, world views); the core stays modular enough to embed in third-party clients later |
| A7 verifiable history | deterministic canon: one seed, an append-only log, byte-identical replay — the substrate that makes A1–A6 honest |

**Content stance** (D-267). Adult audience, one audience: there is no
child-safe mode and no sanitised variant of the world. The simulation's
possibility space includes disease, slavery, violence, sexual coercion,
death, war, betrayal, theft and ruin; mechanics decide outcomes and the LLM
renders them. A pleasant balance is not a goal — conflict and failure are what
generate history. Where a local model refuses material, the owner may supply
the asset; the simulator never simulates a fact away to spare a model.

**Scale** (D-268). The world is a profile, not a cap: size, population
density, event density and resources are declared data the player sets at
world creation. Detail follows observation and causal demand; refinement
preserves the obligations already implied by the same history (D0). The
measured envelope owns "how far this holds", never a promise.

**Delivery horizon** (D-265/D-270). The project ships its own local-first
shell — chat, inference setup for llama.cpp and local/cloud APIs, and world
views around the simulator; the `workbench/` + `frontend/` family is the
engineering base, and its current visual direction is not accepted (G-010 is
the open owner call). Soul-of-Waifu is retired as the delivery horizon:
integration with third-party clients (LM Studio, SillyTavern) is a later
modularity goal, deferred (G-011). The engine repo stays frontend-agnostic;
the shell is the **dumb terminal** side of the split — it renders, the
mediator owns the context window (no sliding window, no auto-summarization, no
keyword lorebook injection).

**North star (quality target).** Emergent-history depth on the order of DF /
RimWorld / Kenshi (§9's precedents) — a long-term quality target and an
ambition, never a claim about current capability. Depth is earned system by
system; no gate, fixture, or phase closure establishes it.

## 11. What this repo deliberately drops from the source concept

Specific model stacks and hardware budgets (→ `docs/TECH_NOTES.md`; they rot),
long lorebook comparisons and percentage tables (→ owner's archive), phased
specs (→ `docs/SPECS_BACKLOG.md`, written just-in-time). Percentages anywhere =
qualitative goals, never measurements.
