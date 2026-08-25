# ink · `REFERENCES.md` §4 + §14 · MIT · phase 3 (event grammar family)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is open MIT — code and
> runtime both; reading and porting grammar shapes is permitted per
> §0.4. Copying ink-runtime code into our repo is permitted but not
> useful — our runtime is Python stdlib (D-012), ink-runtime is
> C#/JS; we lift the **grammar** (knot/stitch/divert/gather/choice)
> into our `Brief` schema sketch, never the runtime. Public spec:
> inkle's "Writing with Ink" manual (the canonical grammar reference).

**What it is.** inkle's ink is a scripting language for branching
narrative, first released 2014 (ink 1.0) and open-sourced under MIT
(ink compiler + runtime + ports). Used in-house for *80 Days*,
*Sorcery!*, *Heaven's Vault*, *Overboarded*; widely adopted by AAA
studios (Universal, Disney, EA) and indie. Public tooling:
`inklecate` (compiler, C#), `ink-runtime` (C#/JS; community Python
port `ink-py`). The reference is the **language grammar** — flow-
based authoring where content is a sequence of text paragraphs with
choices, diverts between knots/stitches, and a small expression
language for conditionals and variables. Used as the precedent for
our `Brief` sketch (`SPECS_BACKLOG.md`, phase 1+).

**Concrete mechanics.**

- **Flow-based authoring.** Content is a sequence of text paragraphs
  with choices. The reader walks the flow; choices branch. No
  "scene" primitive — **flow is the primitive**. The grammar has no
  concept of "current state"; the callstack of visited knots is the
  state.
- **Knots (`== knot_name ==`)** and **stitches (`= stitch_name =`)**:
  labelled landing points for diverts. A knot is a chapter; a stitch
  is a subsection. Both are addressable as `knot_name` or
  `knot_name.stitch_name`. The address shape is identical to a
  filesystem path — direct echo of our `Brief` `target_id` field.
- **Diverts (`-> knot`) and gathers (`<-`)**: jumps between
  knots/stitches. Gathers collect choices that converged — the
  chosen choice's flow falls through to the gather. Diverts can be
  at end of paragraph (`-> next_knot`) or inline (`Text -> next_knot`).
  A divert is the explicit-jump primitive; a gather is the implicit-
  continuation primitive.
- **Tunnels (`-> tunnel ->`)**: parameterised sub-flows. The caller
  supplies args; the tunnel returns to the caller. The function-call-
  shaped divert. The tunnel is the only parametrised-jump primitive
  in the grammar.
- **Choices (`*` single-shot, `+` persistent)**: each choice has a
  label, optional condition, optional bracketed text shown only if
  condition fails, optional divert. Example: `*   [condition] "Choice
  label" -> target_knot`. `+` choices are available every visit until
  taken; `*` choices disappear after taken. The **first_time_only** vs
  **persistent** distinction is structural, not a flag (cf. Wesnoth
  `first_time_only`, `wesnoth_wml.md`).
- **Conditional text.** `{condition: text}` (inline if),
  `{condition: text|else text}` (inline if/else), multi-line
  `{condition:` blocks. Conditionals are first-class; the engine
  evaluates the boolean and emits one branch.
- **Sequences — three flavours.**
  - `cycle: a, b, c` — rotate through, never stop. Last item
    repeats after exhaustion.
  - `sequence: a, b, c` — go through, then stop on last.
  - `shuffle: a, b, c` — random pick without immediate repeat.
  - `shuffle sequence` / `shuffle cycle` — combinations.
  These are the **determinism hazard** — `shuffle` uses a runtime
  RNG without seed control. Our adaptation makes them deterministic
  (INV-2: single seeded RNG, `sorted()` over alternatives).
- **Variables.** `VAR x = 5`, `VAR y = "string"`, `LIST state = (a,
  b, c)` (multivalued — set semantics), `LIST state = a` (single-
  valued — enum semantics), `CONST k = 10`. Mutable with `~ x = x +
  1`, `~ state = b`, `~ state += c` (multivalued add). Variables are
  global; saves snapshot them.
- **Global lists.** `LIST TopColors = (red, blue, green)` — a
  multivalued flag set. `LIST currentColor = ()` — empty
  multivalued. `LIST currentColor += red`, `LIST currentColor -=
  red`. Use case: track which dialogue branches the reader has
  visited — exactly our `seen` channel on knowledge records
  (`MVP_SCOPE.md` §10).
- **Tags.** `# tag_value` after a paragraph. Author metadata; passed
  to runtime via the Story API. Used for scene-card assembly, audio
  cues, content warnings, beat-type classification. Our `Brief`
  `metadata` field inherits the shape.
- **Functions.** `== function name(arg1, arg2) ==` — a knot-shaped
  block with `~ return value`. Pure functions (no side effects on
  variables). Functions are first-class — a divert can target a
  function call.
- **Logic operators.** `&&`, `||`, `!`, `==`, `!=`, `>`, `<`, `>=`,
  `<=`, unary `-`, arithmetic `+ - * / %`. English aliases `not`/
  `and`/`or` also accepted. Pattern matching on lists: `?state`
  (true if any state set), `state?` (alias), `KnotName?` (true if
  knot visited). Built-in jumps: `-> KnotName`, `-> DONE` (end of
  story), `-> END` (terminal end).
- **Runtime.** `ink-runtime` in JS/C#; the Story object exposes
  `Continue()`, `currentText`, `currentChoices`,
  `ChooseChoiceIndex(i)`. State is a single mutable snapshot; save
  = serialise the snapshot. **No event log** — this is the amnesia
  anti-pattern (`mesa.md`). Replay requires the snapshot; the source
  alone is insufficient. The runtime keeps a `callstack` of knots
  visited, the current set of choices, and the variable snapshot.

**What we take.**

- **Knots/stitches/diverts/gathers** — the **shape for our `Brief`
  sketch** (`SPECS_BACKLOG.md`). A scene is a knot; a sub-scene is
  a stitch; a divert is an Intent to transition; a gather is the
  implicit continuation after a choice resolves. The grammar is the
  cleanest public reference for branching narrative as a graph, not
  a tree.
- **Conditional text `{condition: text}`** — the shape for our
  `templates.json` conditional expansion. Our `render/` will use
  the same `{condition: ...}` shape, but deterministic (no `shuffle`
  random pick; a `sorted()` sequence or a fixed-RNG draw per INV-2).
- **The `LIST` multivalued flag set** — the shape for our `state`
  on entities (`MVP_SCOPE.md` §10 `state` field on NPC; `seen` /
  `inferred` / `spoken` channels are flags on a per-entity
  multivalued).
- **The `+` persistent choice vs `*` single-shot** — the shape for
  our `Intent` `accept_policy` field. Some Intents can be re-accepted
  every tick; some can be accepted once per playthrough
  (`first_time_only`, the Wesnoth lesson — `wesnoth_wml.md`).
- **Tags (`# tag`)** — the shape for our `Brief` `metadata` field.
  Tags carry non-prose info to the runtime: scene mood, NPC emphasis,
  beat type (peacetime / threat / rest).
- **Pattern matching `KnotName?`** — the shape for our `seen`
  knowledge channel (`MVP_SCOPE.md` §10). The pattern: "has this
  beat been visited" as a first-class query. Our `seen` records
  "who has seen what", the same shape with epistemic depth ink
  lacks.

**What we adapt.**

- **ink's flow-based content → our `Brief` sketch (phase 1+).**
  Phase 0 has no flow (the PC is a tick, not a player); the flow
  primitive is reserved for the briefer.
- **ink's `shuffle` (random pick) → our `sorted()`-deterministic
  `sequence`** (`render/` spec, not yet written). The RNG hazard is
  explicit: ink uses runtime random; we use the seeded RNG instance
  (INV-2) — the same grammar, deterministic enforcement. The pattern
  ported verbatim; the random policy replaced.
- **ink's variable snapshot save → our JSONL log.** ink's save is a
  snapshot; our state is `fold(log)` (INV-1). The ink lesson: a
  snapshot works for branching narrative; an event log is required
  for simulation with causality (`cause` chain on every event).
- **ink's `KnotName?` (visited check) → our `seen` knowledge
  channel** (`MVP_SCOPE.md` §10). The pattern: "has this beat been
  visited" as a first-class query. Our `seen` records "who has seen
  what", the same shape with epistemic depth ink lacks.
- **ink's tags → our `Brief` `metadata`.** We keep the shape (string-
  keyed metadata on a content node); we don't port the exact syntax
  (JSON in our `Brief` schema, not `# tag` text).

**What inspires us.** The **flow as primitive, knots/stitches as
addresses, choices as conditional jumps** lesson. ink is the cleanest
public reference for branching-narrative-as-flow; every node is
reachable by name, every jump is a divert, every choice is a typed
branch. The design lesson: **narrative structure is a labelled graph**,
not a tree or a state machine. Our `Brief` sketch inherits this —
the briefer walks a labelled graph under LLM-driven choice selection
(phase 1+).

**Strengths.**

- Public MIT — runtime in C#, JS, Python (community `ink-py`); the
  compiler is also MIT. Full reference implementation readable.
- The grammar is small (~30 keywords), documented (inkle's "Writing
  with Ink" manual is the public spec), and proven in production (4
  inkle games + 100s of community/AAA projects).
- The `knot`/`stitch`/`divert`/`gather` primitive is the cleanest
  public reference for branching narrative as a graph, not a tree.
- `LIST` multivalued flags are the cleanest public implementation of
  "track which branches visited" as a first-class primitive.
- Tunnel pattern is the only parametrised-jump primitive in the
  survey — directly shapes our `Brief` `target_args` sketch.

**Weaknesses.**

- ink is **non-deterministic by default** — `shuffle` random picks
  use a runtime RNG without seed control. Our INV-2 makes the same
  shape deterministic; the adaptation is the rule.
- ink has **no event log** — state is a snapshot, replays require
  the snapshot. The amnesia anti-pattern (`mesa.md`) ported to
  narrative scale.
- ink has **no causality** — choices don't carry a `cause` field.
  Our `EVENT_SCHEMA.md` §2 makes the chain explicit; ink's lesson
  is what we add, not what we copy.
- ink has **no epistemology** — variables are global; the runtime
  knows everything. Our `knowledge` records (`MVP_SCOPE.md` §10)
  carry "who knows what" with fidelity; ink has no analogue.
- ink's runtime is interpreter-shaped — the Story object is mutable,
  choices mutate it. Our `Brief` sketch (phase 1+) will wrap the
  ink-runtime-equivalent in an event-sourced shell (every choice
  emits a `brief_choice` event with `cause` chain, INV-1).
- ink has no `Intent`/`Event` boundary — a choice is both the
  trigger and the action. Our INTENT_SPEC sketch separates them
  (`SPECS_BACKLOG.md`); ink's grammar conflates them.

**Verdict.** Phase-3 narrative-grammar reference, positive on the
knot/stitch/divert/gather shape (Brief sketch inherits directly),
positive on the `LIST` multivalued flag pattern (entity `state`
inherits), positive on the `#` tag pattern (Brief `metadata`
inherits), positive on the `+` vs `*` choice persistence shape
(Intent `accept_policy` inherits), explicitly negative on the
default non-determinism (INV-2 makes the same shape deterministic)
and the snapshot-only state (INV-1 makes the state an event log).
The reference is for the shape, not the runtime — we don't port
ink-runtime; we port its grammar into our `Brief` schema.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
