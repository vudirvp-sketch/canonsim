# tracery · `REFERENCES.md` §4 + §14 · Apache-2.0 · phase 3 (event grammar family)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is open Apache-2.0 — code
> and grammar format both. Reading and porting the algorithm is
> permitted per §0.4; copying the reference implementation is
> permitted but not useful — our runtime is Python stdlib (D-012),
> tracery's reference is JS; we lift the **grammar** (JSON symbol
> table + recursive `#symbol#` expansion + save/restore stack) into
> our `templates.json` + `render/`, never the runtime. Reference
> repo: `GalaxyKate/tracery` (JS); `katef/tracery` (Python port).

**What it is.** tracery is a JSON-based recursive grammar expansion
engine for procedural text generation, created by Kate Compton
(Galapag.us / @GalaxyKate), first released 2013 and open-sourced under
Apache-2.0. Originally a JS library for Twitter bots (the Cheap Bots
Done Quick hosting service); ports exist for Python, C#, Haxe, Rust.
The grammar is JSON; the runtime is a small recursive expander with a
symbol table and a stack for state. Public, permissively licensed —
code is in scope per `REFERENCES.md` §0.4 (Apache-2.0 + port-permitted
per §0.7). Used as the precedent for our `templates.json` +
`render/` shape.

**Concrete mechanics.**

- **Grammar format.** A JSON object mapping symbol names to lists of
  expansion alternatives. Example: `{"origin": "#creature# is
  #state#", "creature": ["dragon", "ogre", "goblin"], "state":
  ["asleep", "hungry", "angry"]}`. The expander starts at the
  `origin` symbol and recursively expands `#symbol#` references until
  no symbols remain. The grammar is the JSON object; the runtime is
  the expander.
- **Recursive expansion.** Every `#symbol#` in a string is replaced
  by a random pick from the symbol's list. Picks are uniform by
  default; extensions support weighted picks (a `{"weight": 2,
  "text": "..."}` shape). Recursive: a symbol's expansion can
  contain other `#symbols#`. The recursion terminates when no
  symbols remain in the string.
- **Modifier functions.** `#symbol.modifier#` applies a
  transformation. Built-in: `a` (article — `#creature.a#` → "a
  dragon"), `capitalize`, `upper`, `s` (plural — `#name.s#` →
  "dragons"), `ed` (past tense), `er` (agentive). Custom modifiers
  can be registered (e.g. `#verb.past#`); JS tracery supports
  function-registered modifiers. The modifier list is the **single
  most useful extension point** — a small set of built-ins plus a
  registration hook for domain-specific transformations.
- **Nested symbol access.** `#creature.action#` — looks up
  `creature.action` as a separate symbol (dot-separated). Allows per-
  creature action vocabularies; the grammar is a flat namespace, but
  the convention is hierarchical keys. Our `templates.json` uses the
  same dot-notation for `NPC.emotion.immediate` / `NPC.emotion.long`
  hierarchies.
- **Save/restore state.** `[symbol:value#]` pushes `symbol=value`
  onto a stack; `[symbol:#]` pops. Used for article agreement ("a
  dragon" not "an dragon"), pronoun agreement, salutation tracking
  across a sentence. **This is the only stateful feature** — the
  stack is the entire state model. The pattern: **per-expansion
  stack is sufficient for cross-clause agreement**; no global state
  needed.
- **Avoidance rules.** tracery has no native "don't repeat" mechanism,
  but a common extension is `["action", "action", "action",
  {"action": "...", "noAction": "previous_action"}]` — the engine
  avoids the previous pick. Our adaptation: deterministic iteration
  (`sorted()` over the alternatives + a fixed RNG draw) gives the
  same effect without runtime randomness — the previous pick is the
  last in `sorted()` order, never picked twice in sequence.
- **Action syntax.** `[name:value]` and `[name:]` (clear) are stack
  pushes/pops. `[name:#]` is "push the next expansion of name" — for
  late binding. The action syntax is minimal — five operators cover
  the entire stateful surface.
- **Rhizome extension.** Kate Compton's later `rhizome` package
  (also Apache-2.0) adds graph-shaped grammars (a node can transit to
  another node, not just expand). Not standard tracery; the precedent
  is for the post-tracery family. Our `Brief` sketch
  (`SPECS_BACKLOG.md`, phase 1+) is graph-shaped — rhizome is a
  closer reference than tracery for the briefer, but ink
  (`ink.md`) is the cleaner graph-shaped grammar.
- **Output is text only.** No game state, no side effects. tracery
  is a pure function from (grammar, RNG state) → string. The runtime
  is **stateless between expansions** except the save/restore stack.
  This is by design — the grammar is the data; the runtime is the
  pure expander. Our `render/` is the same shape (text-only by
  intent; the canon is in the JSONL log, not in templates).
- **Runtime size.** ~200 lines of JS for the core expander. The
  reference implementation is in `tracery/tracery.js` (Cheap-Bots-
  Done-Quick infrastructure); ports are similar in scale. The
  smallness is the precedent — a useful procedural-text grammar is
  ~200 lines of Python. Our `render/` will be the same scale.

**What we take.**

- **The JSON grammar shape.** Exactly our `templates.json`
  (`MVP_SCOPE.md` §11 `templates.json`). Symbol → list of
  alternatives; recursive expansion. Same shape, same JSON. The
  grammar is a direct lift; the runtime is a direct port (with INV-2
  determinism added).
- **The save/restore stack.** Exactly our `stack[pop]` for
  pronoun/article/salutation agreement in the chronicle. The lesson:
  a per-expansion stack is sufficient for cross-clause agreement; no
  global state needed. The stack discipline (push, pop, mutate) is
  structurally identical to tracery's.
- **The modifier pattern (`#symbol.modifier#`).** Exactly our
  `templates.json` modifier functions (registered in `render/`,
  applied at expansion time). Built-ins: `.a` (article), `.capitalize`,
  `.plural`. Custom: `.past_tense`, `.speaker_pov`, `.narrator_pov`,
  etc. The registration hook is the single most useful extension
  point.
- **The "pure function from (grammar, RNG state) → string" pattern.**
  Exactly our `render/` shape. The chronicle is a deterministic
  function of (log, templates.json, seed). INV-1 + INV-2 together
  make the chronicle byte-identical on replay (T1).

**What we adapt.**

- **tracery's runtime RNG → our single seeded `random.Random(seed)`
  instance** (INV-2). tracery uses `Math.random()` (JS) or
  `random.random()` (Python) — both unseeded by default. Our
  adaptation: the same expander with a seeded RNG instance gives
  byte-identical chronicle on replay. The grammar is ported; the
  random policy is replaced.
- **tracery's `#symbol#` → our `templates.json` with the same
  `#symbol#` syntax**, but the expansion is deterministic
  (`sorted()` iteration over alternatives + a fixed RNG draw). The
  grammar stays the same; the avoidance is enforced by the iteration
  order (the previous pick is the last in `sorted()` order — never
  picked twice in sequence).
- **tracery's stack `[symbol:value#]` → our `stack[pop]` shape in
  `render/`.** Same stack discipline (push, pop, mutate), but the
  stack is part of the event log (each push/pop is a
  `chronicle_stack` event with `cause`), not just runtime memory.
  INV-1 + `cause` chain — the stack mutation is an event, not a
  side-effect.
- **tracery's weighted picks (the `{"weight": N, "text": "..."}`
  extension) → our `weight` field on each alternative in
  `templates.json`.** Same shape; the weight is a float (per
  `MVP_SCOPE.md` §11). The weighted-random draw uses the seeded RNG
  instance, deterministic per replay.
- **tracery's avoidance (no immediate repeat) → our `sorted()`
  iteration + fixed RNG draw.** The grammar stays the same; the
  avoidance is enforced by the iteration order (the previous pick is
  the last in `sorted()` order — never picked twice in sequence).
  No runtime avoidance state needed — the deterministic iteration
  makes it implicit.

**What inspires us.** The **grammar is data, runtime is 200 lines
of Python** lesson. tracery is the canonical proof that a recursive
text-generation grammar can be JSON + a small expander; the entire
ecosystem of Twitter bots, name generators, rumor mills, and
chronicle skins is 200 lines of code per port. Our `render/` will be
the same shape — `templates.json` + a 200-line `expand()` function.
The determinism law (INV-2) is the only addition; the grammar is
the precedent. The save/restore stack is the inspiration for cross-
clause agreement without global state — the cleanest public
reference for stateful text agreement.

**Strengths.**

- Public Apache-2.0 — the reference implementation is 200 lines of
  JS; the Python port (`tracery` on PyPI) is similar in scale. Full
  source readable; the algorithm is small enough to audit in an
  afternoon.
- The grammar is JSON — no custom parser, no DSL syntax. Our
  `templates.json` is a direct lift; the format is the same.
- The save/restore stack is the cleanest public reference for
  stateful text agreement — 5 lines of code, fully sufficient for
  pronoun/article/salutation across a sentence.
- The grammar has been ported to JS/Python/C#/Haxe/Rust — the
  algorithm is portable across languages without IP friction. Our
  stdlib-only runtime (D-012) inherits without external dependency.
- The runtime scale (~200 lines) is the precedent that useful
  procedural text generation is a small algorithm, not a framework.
  Our `render/` will be the same scale.

**Weaknesses.**

- tracery's runtime RNG is **unseeded by default** —
  `Math.random()` or `random.random()`. Our INV-2 makes the same
  expander deterministic; the adaptation is the rule, not the
  inspiration.
- tracery has **no causality** — the expansion is a pure function,
  but there's no `cause` field on the produced text. Our
  `EVENT_SCHEMA.md` §2 makes the chain explicit; tracery's lesson is
  what we add.
- tracery has **no epistemology** — the grammar doesn't know who is
  speaking, who is hearing. Our `knowledge` records carry per-NPC
  epistemic state; tracery has no analogue. The briefer (phase 1+)
  will wrap tracery in an epistemic shell.
- tracery is **text-only** — no game state, no side effects. Our
  `render/` is also text-only by design (the canon is in the JSONL
  log, not in templates); tracery's "weakness" is the same as our
  `render/` — by intent.
- tracery's grammar can be **inconsistent across ports** — the JS
  reference and the Python port differ in edge cases (modifier
  chaining, stack nesting). Our `templates.json` is JSON Schema-
  validated (D-023); the spec is the same across implementations.
- No weighted picks in the reference grammar — the `{"weight": N,
  "text": "..."}` shape is a common extension but not standardised.
  Our `templates.json` bakes weights into the spec.

**Verdict.** Phase-3 text-generation reference, almost entirely
positive (the JSON grammar shape, the save/restore stack, the
modifier pattern, the 200-line runtime scale are all direct
inheritances), explicitly negative on the default unseeded RNG (INV-2
fixes it) and the text-only scope (our `render/` is also text-only
by design, so the "weakness" is by intent for our use case). The
grammar is the precedent; the determinism is the rule. tracery is
the reference that proves useful procedural text generation is a
small algorithm, not a framework — the precedent that our `render/`
will be ~200 lines of Python stdlib, not a vendored library.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
