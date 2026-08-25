# Endless Sky mission DSL · `REFERENCES.md` §1 + §14 · GPL-3.0 code; mixed assets · phase 3 (event grammar family)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is open GPL-3.0 code; mixed
> assets (some CC-BY-2.0). Reading the parser, the mission system,
> the conversation engine is permitted per §0.4 — copying the text
> would force GPL on our files, so we port the shape (offer/accept/
> complete lifecycle, flat effect vocabulary) into JSON, never the
> syntax. Reference repo: `endless-sky/endless-sky` `data/` tree.

**What it is.** Endless Sky (Michael Zahniser / various, 2015 open-
source release) is a space-trade/combat sim in the tradition of
Escape Velocity. The mission scripting system is a custom whitespace-
delimited DSL in `.txt` files under `data/`; the engine parses them
into mission templates, conditions, and effects. The DSL is the
relevant reference — the grammar is **much simpler than Paradox**
(`paradox_scripting.md`): no MTTH, no scopes, no weights, no on_action
IDs. The simplicity is the lesson — a small grammar with clean
lifecycle (offer/accept/complete/fail) lets non-programmers author
content; the ES `data/` tree is ~300 mission files by community
contributors without coding experience.

**Concrete mechanics.**

- **File format.** Human-readable, whitespace-delimited `.txt` files.
  Top-level keywords: `mission`, `event`, `npc`, `conversation`,
  `ship`, `outfit`, `planet`, `system`, `government`, `phrase`,
  `fleet`, `news`, `effect`. Each keyword begins a named block;
  blocks nest by indentation or by the `to:`, `on:`, `if:` field
  convention.
- **`mission` block — the canonical reactive atom.** Fields:
  `name`, `description`, `deadline`, `cargo`, `passengers`,
  `illegal`, `invisible`, `priority`, `where shown`, `reputation`
  (required reputation floor), `government`. Lifecycle transitions:
  - `to: offer` — when to make the mission available (a condition
    over player state, system, attribute levels).
  - `to: accept` — when the player accepts the offered mission.
  - `to: decline` — when the player declines (clears the offer).
  - `to: complete` — success condition (cargo delivered, kill count
    reached, system visited, etc.).
  - `to: fail` — failure condition (cargo destroyed, deadline
    passed, NPC killed).
  - `to: defer` — re-offer later (a different condition becomes
    true).
  - `to: visit` — when an NPC visits a system.
  The lifecycle is a state machine; each transition is a named
  condition. Public, documented.
- **Condition expression language.** A small infix language:
  `requires: "Pilot rating > 4"`, `requires: ("nav rating >= 50" &&
  "system = Rim")`. Operators: `=`, `!=`, `<`, `>`, `<=`, `>=`, `&`
  (and), `|` (or), `!` (not). Quantities can be: numeric literal,
  an attribute name (`nav rating`, `combat rating`, `wealth`,
  `pirate missions`), or a string for equality. No scopes, no
  MTTH, no weights — the **smallest grammar in the event-scripting
  family**.
- **Trigger conditions.** `to: offer` accepts a condition (when to
  make the mission available), not a probability. No MTTH; missions
  are pulled from the offered pool when the player lands on a planet
  with a matching condition. The pattern: **condition-driven
  availability, not time-driven probability** — the inversion of
  Paradox MTTH (`paradox_scripting.md`).
- **Effect mini-language.** An `effect` block within a mission or
  event. Actions: `set` (set a flag), `clear` (clear a flag), `pay`
  (give money), `outfit` (give/take an outfit), `ship` (give/take
  a ship), `event` (trigger a named event), `conversation` (start
  a conversation), `fail` (fail this mission), `log` (add to
  player log). Flat action vocabulary; no scopes, no chained
  effects. Each effect is a discrete (key, delta) on the world.
- **`conversation` block — the dialogue DSL.** Nodes: `text` (a
  paragraph), `choice` (a numbered option), `goto` (jump to label),
  `branch` (conditional fork), `action` (run an effect mid-
  conversation), `condition` (gate a choice by a flag), `label`
  (a goto target). The conversation is a graph, not a tree — cycles
  via `goto` are explicit.
- **`npc` block — a named NPC.** Fields: `name`, `government`,
  `personality` (one of `unfazed`, `talkative`, `naive`, `cowardly`,
  etc. — affects conversation branch conditions), `description`,
  `plural`. The pattern: **NPCs have personality flags that change
  dialogue branch conditions** — our `content/tavern_pack/`
  `entities.json` `traits` field inherits the same shape.
- **`event` block (separate from missions) — fires globally on a
  condition.** Fields: `name`, `date` (a system date range),
  `unavailable`, `conditions`, `effects`. Unlike missions, events
  don't require player interaction. The pattern: **background
  events without an NPC trigger** — exactly our `seeded_hooks`
  (`MVP_SCOPE.md` §5, `P2e` director proposal). Condition + effect
  list + no accepter. Fires on the world's tick, not on a mission
  lifecycle.
- **`phrase` block — a one-symbol random-text vocabulary.**
  `phrase name = ["text1", "text2", "text3"]` — a single name
  resolves to one of a list at runtime. The pattern: **lightweight
  tracery** (`tracery.md`) — a one-symbol grammar for prose variety,
  without nested expansion or modifiers. Our `templates.json`
  carries the same shape, with full tracery-style nested expansion
  added on top.
- **Pack split.** `data/` has top-level categories — `missions/`,
  `events/`, `federation/`, `free worlds/`, `kwereth/`, `hai/`,
  `remnant/`, `wanderer/`, `quarg/`, etc. Each is a campaign as a
  directory; each mission is a `.txt` file. **No single index file**
  — the engine loads every `.txt` in `data/` recursively; the order
  is filesystem-determined (a known determinism hazard — ES uses
  sorted directory listings internally, but the convention is
  fragile). Our `pack_loader` (iter-1) uses `sorted()` over the
  glob result, INV-2 deterministic.
- **The "lightweight vs Paradox" verdict.** ES intentionally rejected
  the Paradox grammar's complexity. No MTTH (the engine's random-
  offer system replaces it), no scopes (missions act on the player
  only), no on_action IDs (events poll on a date check). The result:
  ES mission files are readable by non-programmers; the corpus is
  ~300 mission files authored by community contributors without
  coding experience. The lesson: **simplicity is a feature, not a
  deficit** — a small grammar with clean lifecycle (offer/accept/
  complete/fail) lets non-programmers author content.

**What we take.**

- **The `to: offer`/`to: accept`/`to: complete` lifecycle as the
  shape for our `Intent`** (`INTENT_SCHEMA` sketch in
  `SPECS_BACKLOG.md`). A mission has explicit success and failure
  transitions, not implicit "best-effort" semantics — our `Intent`
  carries the same `accept_if`/`complete_if`/`fail_if` triad.
- **The `phrase` block** — exactly the tracery-shaped one-symbol
  grammar that `templates.json` will use. ES's implementation is the
  **simpler-than-tracery precedent**: no nested symbol expansion, no
  modifiers — just a list, picked at random. Our `templates.json`
  extends with full tracery (`tracery.md`).
- **The `event` block (background, no NPC trigger)** — exactly our
  `seeded_hooks` (`MVP_SCOPE.md` §5, `P2e` director). The shape: a
  condition + an effect list + no accepter. Fires on the world's
  tick.
- **The `effect` mini-language flat vocabulary** — `set`/`clear`/
  `pay`/`log`/`event`. Our `effect` field on events
  (`EVENT_SCHEMA.md` §4 `state_changes`) inherits the flat shape —
  no scopes, no chained effects. Each effect is a discrete
  (key, delta) on the world.
- **`npc` `personality` flags** — the precedent for our
  `entities.json` `traits` field (`MVP_SCOPE.md` §4). ES `personality`
  = `unfazed`/`talkative`/`naive`/`cowardly`; our `traits` =
  `drunkard`/`watchful`/`shy`/`reckless` — same shape (a closed
  enum that gates branch conditions in `actions.json`).

**What we adapt.**

- **ES's whitespace-delimited DSL → JSON content packs.** ES has
  its own parser; we use JSON Schema (D-023) for the same purpose —
  read/write access without a custom parser.
- **ES's `to: offer` condition language (infix arithmetic on
  attributes) → our `preconditions` in `actions.json` as a
  `Dict[str, list]` data structure, not as a string language.** The
  fix: INV-3 forbids "domain words in code" — a string expression
  language in `actions.json` would require an evaluator in core
  code with domain words; a structured data precondition stays
  generic.
- **ES's `conversation` graph (goto/label cycles) → our `Brief`
  sketch in `SPECS_BACKLOG.md` (phase 1+).** The conversation is a
  graph; the briefer walks it under LLM-driven choice selection.
  Phase-0 has no conversations (the PC is a tick, not a player);
  the graph shape is reserved for the briefer.
- **ES's "no MTTH" → our `narrative_entropy` (`P2e` proposal).**
  Where Paradox uses MTTH to time probabilistic events, ES uses
  condition-driven availability with a background offer pool; our
  `P2e` director releases seeded hooks when entropy drops, not
  when a clock ticks. ES is the precedent that condition-driven
  beats MTTH for player-facing content.

**What inspires us.** The **lightweight grammar beats heavyweight
grammar for community-authored content** lesson. ES has ~300 mission
files authored by community contributors; the Paradox wikis
(CK3/EU4/Stellaris) require a `script_docs` machinery to even
document the grammar. The pattern: **simplicity is a feature, not a
deficit** — a small grammar with clean lifecycle (offer/accept/
complete/fail) lets non-programmers author content. Our
`content/tavern_pack/` v0.1 is the same shape (small, JSON,
community-authorable).

**Strengths.**

- Open GPL codebase — the parser, the mission system, the
  conversation engine, all readable. The grammar is fully documented
  in the source; no reverse-engineering required.
- The `mission` lifecycle (offer/accept/complete/fail/defer) is the
  cleanest public reference for state-machine-shaped reactive
  content. Each transition is a named condition.
- The `phrase` block is the simplest public implementation of a
  one-symbol grammar — the simplest thing that could work, and 15
  years of community content proves it works.
- The `event` block (separate from `mission`) is the cleanest public
  precedent for **player-independent background events** — our
  `seeded_hooks` are a direct inheritance.

**Weaknesses.**

- ES's grammar has no determinism law — random offers, system-date
  checks, NPC spawn randomness. Our INV-2 (single seeded RNG, sorted
  iteration, queue key) is the explicit fix; the ES grammar would be
  non-deterministic under our replay test (T1).
- ES has no event log — runtime state lives in the save file. Our
  INV-1 (state = fold(log)) is the inverse; the ES save-on-event
  approach is the same Mesa/Sims amnesia anti-pattern (`mesa.md`).
- ES's `effect` mini-language has no causality field. `cause` is
  implicit in the firing mission/event; our `EVENT_SCHEMA.md` §2
  `cause` is explicit. The ES precedent shows what we add, not what
  we copy.
- ES's conversation DSL is a closed graph (goto/label) with no
  `if`-branch primitive — branching is done by `choice`+`condition`
  (a choice is hidden if its condition is false). Our `Brief` sketch
  inherits this; the choice-gating pattern is the same shape.
- ES missions can fail silently — if the player destroys the mission
  cargo, the engine detects it via a `to: fail` condition, not via
  a `cause` chain. Our `EVENT_SCHEMA.md` §2 `cause` makes the chain
  explicit.

**Verdict.** Phase-3 event-grammar reference, positive on the
lightweight grammar (mission lifecycle, phrase, event-as-background,
effect mini-language flat vocabulary, `npc` `personality` flags),
explicitly negative on determinism (no INV-2 analogue) and event-
sourcing (save-on-event, not fold(log)). The grammar is simpler than
Paradox for the same expressive power; the community-authored corpus
is the proof. Our `Intent`/`effect`/`traits` shapes inherit directly;
our `Brief` sketch reserves the conversation-graph shape for phase 1+.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
