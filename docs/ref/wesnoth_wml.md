# Wesnoth WML · `REFERENCES.md` §1 + §14 · GPL-2.0+ · phase 3 (event grammar family)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015). Source is open GPL-2.0+ — pattern lifting permitted
> per §0.4; copying text into our repo would force GPL on our files,
> so we port the shape (tag→key-value) into JSON, never the syntax.
> Reference corpus: `wesnoth/wesnoth` `data/` tree (~10k `.cfg` files,
> 20+ years of community-authored content).

**What it is.** The Battle for Wesnoth's "Wesnoth Markup Language" (WML)
— a domain-specific language for all content: units, scenarios,
campaigns, terrain, events, abilities, items. First shipped 2003
(Wesnoth 0.4 era); grammar stabilised around 1.4 (2007). The parser
(`simple_wml`/`config` in C++) reads a tree of `[tag]`...`[/tag]`
blocks with `key=value` pairs; not XML (no schema validator), but
tag-tree-shaped. The grammar is the precedent that **a small DSL +
an escape valve** ages better than either pure-DSL or pure-script.

**Concrete mechanics.**

- **Tag-tree shape.** Every content node is a `[tag]` block with
  string-valued `key=value` pairs and optional nested tags. Tags are
  domain nouns: `[scenario]`, `[side]`, `[unit]`, `[unit_type]`,
  `[race]`, `[ability]`, `[movement_type]`, `[terrain]`, `[event]`,
  `[item]`, `[objective]`, `[modify_unit]`, `[modify_side]`,
  `[set_variable]`, `[store_unit]`, `[unstore_unit]`, `[kill]`,
  `[message]`, `[filter]`, `[filter_location]`, `[filter_condition]`,
  `[if]`, `[then]`, `[else]`, `[elseif]`, `[switch]`, `[case]`,
  `[lua]`, `[time_area]`, `[area]`, `[goal]`, `[objectives]`,
  `[label]`, `[role]`, `[object]`, `[terrain]`, `[move_unit]`,
  `[teleport]`, `[recall]`, `[place_unit]`, `[fire_event]`,
  `[fire_event_by_id]`, `[end_turn]`, `[endlevel]`, `[gold]`,
  `[unit]` (place), `[sound]`, `[music]`, `[colour_adjust]`,
  `[scroll_to]`, `[lock_view]`, `[animate_unit]`. The pattern: **every
  noun in the world is a `[tag]`; the engine is a tag-tree interpreter**.
  Direct echo of RimWorld's `*Def` family (`rimworld.md`) and
  C:DDA's per-category file split (`cdda_data_json.md`).
- **`[event]` — the reactive atom.** Every state-changing reaction in
  the world is one `[event]` block. Fields:
  - `name` — one of ~80 enum values: `moveto`, `attack`, `attacker_
    hits`, `defender_hits`, `die`, `turn N`, `new turn`, `side N
    turn N`, `prestart`, `start`, `victory`, `defeat`, `enemies
    entered`, `unit placed`, `discover`, `sighted`, `attack_end`,
    `select`, `preload`, `postload`, `prerecruit`, `recruit`,
    `preadvance`, `advance`, `postadvance`, `exit`, `enter`,
    `leave`, etc. Closed vocabulary; extensible by Lua registration
    (`name=lua _hook_<custom>`).
  - `first_time_only` — boolean, **default `true`**: fires once per
    save, then suppressed. The engine maintains a per-event-`id`
    "fired" set. Self-suppression without explicit state.
  - `delayed_variable_substitution` — boolean, default `false`:
    evaluate variable references when the event fires, not at parse
    time. The parse-time/eval-time separation is structural, not
    accidental.
  - `id` — a stable string for save compatibility across versions.
    Without `id`, an event handler is anonymous and the save cannot
    re-attach after a content edit; with `id`, the engine remaps.
  - `filter`, `filter_location`, `filter_condition`, `filter_side`,
    `filter_second_unit`, `filter_weapon`, `filter_attack` — the
    per-noun filter family (below).
- **The `[filter]` family — separate filter per noun.** Each noun
  has its own filter tag with a domain-specific field set:
  - `[filter]` (unit) — `x`, `y`, `side`, `type`, `race`,
    `canrecruit`, `gender`, `variation`, `level`, `defense`,
    `movement_type`, `attacks_left`, `experience`, `hitpoints`,
    `max_hitpoints`, `max_moves`, `max_experience`, `status`
    (`poisoned`/`slowed`/`stone`/`uncovered`), `traits`,
    `abilities`, `profile`, `id`, `name`, `description`, `role`.
  - `[filter_location]` — terrain type, time of day, owner,
    `terrain_class`, `x`, `y`, `radius`, `find_in` (radius search
    mode).
  - `[filter_adjacent_location]` — neighbours of a tile.
  - `[filter_second_unit]` — the defending unit in an attack.
  - `[filter_weapon]` — melee/ranged + attack name.
  - `[filter_condition]` — a small boolean expression language over
    variables and unit attributes; `and`/`or`/`not`, function calls
    (`difficulty`, `turn_number`, `side_number`, `unit.x`, etc.).
    Lisp-in-disguise — we don't want one.
  - The pattern: **filters are first-class data**, not embedded in
    code; the engine evaluates them per-event firing. Our
    `preconditions` in `actions.json` mirror the same shape.
- **`[if]`/`[then]`/`[else]`/`[elseif]` and `[switch]`/`[case]`/
  `[else]`** — the conditional execution primitives. The engine
  evaluates the `[if]` boolean and dispatches to `[then]` or `[else]`;
  `[switch]` matches the variable against `[case]` `value=` fields.
  Both are data, not code — the action body inside `[then]` is the
  same action vocabulary as anywhere else.
- **Action vocabulary inside `[event]`.** The verbs the engine
  executes when an event fires: `[message]` (speaker + caption +
  text; supports `{SPEAKER_NAME}`-style substitution + `[option]`
  choices), `[set_variable]`, `[store_unit]` (snapshot to a WML
  variable), `[unstore_unit]` (restore), `[kill]` (with filter),
  `[modify_unit]` (apply delta to filtered units), `[modify_side]`,
  `[modify_turns]`, `[object]` (give a unit a permanent effect),
  `[item]` (place a map item), `[role]` (assign a unit a role),
  `[terrain]` (change map terrain), `[move_unit]`, `[teleport]`,
  `[recall]`, `[place_unit]`, `[fire_event]`, `[fire_event_by_id]`,
  `[end_turn]`, `[endlevel]`, `[gold]`, `[unit]`, `[sound]`,
  `[music]`, `[colour_adjust]`, `[scroll_to]`, `[lock_view]`,
  `[animate_unit]`. ~30 verbs; flat — no scopes, no chained effects
  (cf. Paradox scopes, `paradox_scripting.md`).
- **Macro preprocessor.** `{NAME}` in a `.cfg` invokes a macro
  defined in `_main.cfg` (or any included file) via `#define NAME
  arg1 arg2` ... `#enddef`. Macros are textual substitution at
  parse time; they take args. The preprocessor also has `#ifdef
  CAMPAIGN_ETT`, `#ifndef`, `#else`, `#endif`, `#ifhave` — single-
  source builds of campaigns with optional content paths. Public
  and documented; the `data/` macros are ~5k lines.
- **Lua escape hatch.** Since 1.7 (2010), `[lua] code=... [/lua]`
  inside `[event]` allows arbitrary Lua. The pattern: **the DSL is
  the substrate, Lua is the escape valve for things the DSL doesn't
  express**. Our `cli/` runs Python on top of the JSONL log — same
  shape (data DSL + scripty escape).
- **The `{event → filter → action}` triad.** Every `[event]` follows
  the same shape: `name` (when), `filter` (who/where), and a sequence
  of action tags (what). The triad is the conceptual core — the same
  shape our `Intent`/`Event` boundary uses (`INTENT_SCHEMA` sketch in
  `SPECS_BACKLOG.md`).
- **`sighted` event** — perception as a first-class event source.
  Fires when a unit becomes visible to a side. Our `MVP_SCOPE.md` §10
  `seen` channel on knowledge records inherits the shape: perception
  baked into the event grammar, not a side-effect of moving.
- **Save-load compatibility via `id`.** Each `[event]` may carry an
  `id`; saves re-attach to event handlers by `id` across content
  edits. Public, documented; the `id` is unique within a campaign.
  Our `event_id` in `EVENT_SCHEMA.md` §1 is the same idea, applied to
  log events for replay compatibility.

**What we take.**

- **The `[event]` → `[filter]` → action triad shape.** Our
  `Intent`/`precondition`/`effect` (`SPECS_BACKLOG.md` INTENT_SPEC
  sketch) is the same triad, renamed for INV-3 (no "filter" in core;
  preconditions live in `actions.json`).
- **The `name` enum shape** (`moveto`, `attack`, `die`, `turn N`,
  `sighted`, etc.). Our `action_type` enum in `actions.json`
  (`MVP_SCOPE.md` §7) is the same idea — closed vocabulary for
  triggers, extensible by pack.
- **The `[filter]` family** — separate filter per noun (unit,
  location, side, weapon). Our `preconditions` in `actions.json`
  mirror this: a per-noun filter map, not one monolithic condition
  language.
- **`first_time_only` default `true`.** Our `seeded_hooks`
  (`MVP_SCOPE.md` §5) inherit this — release once per playthrough,
  suppressed afterwards. Self-suppression without explicit state
  tracking.
- **`[event] id=...` stable identifier.** Our `event_id` in
  `EVENT_SCHEMA.md` §1 is the same shape — a stable string for
  save/replay compatibility, structurally identical to WML's
  per-event-handler id.

**What we adapt.**

- **WML's DSL → JSON content packs** (`content/tavern_pack/`). WML
  is custom-parsed; our `rules.json`/`actions.json`/`entities.json`/
  `templates.json` are JSON. Same shape (tag → key-value), different
  syntax — INV-3 forces the rename. JSON Schema validation (D-023)
  is the WML anti-pattern fix (no schema validator → typos cause
  save-compat bugs).
- **WML's textual `[if]`/`[then]`/`[else]` → Python `Rule`
  evaluation in core code.** We deliberately don't port the
  conditional DSL — preconditions live in data as
  Python-evaluatable structures (P2d `expectation_violation`
  precedent in iter-3), not as a parser-readable mini-language.
- **WML's `sighted` event → our `seen` knowledge channel**
  (`MVP_SCOPE.md` §10). WML's perception fires on visibility
  change; ours fires on the perception tick — same first-class
  perception lesson.
- **WML's Lua escape hatch → Python in `cli/` and (phase 1+)
  `brief/`.** The DSL is the substrate; the script is the escape —
  exact inversion of RimWorld's closed C# `IncidentWorker`
  (`rimworld.md`).
- **WML's `delayed_variable_substitution` flag → our `event_id`
  field's `effective_at` semantics.** WML parses the event body once
  but evaluates variables at fire-time; we similarly separate
  parse-time (load `rules.json`) from eval-time (check preconditions
  at the queue tick).

**What inspires us.** The **DSL-first, escape-hatch-second design**.
Wesnoth proves a small tag-based DSL with a Lua escape valve can
express an entire game's worth of content — the same shape as our
JSON pack + Python rule evaluator. The historical lesson: when
Wesnoth started (2003), every event was WML; over time the engine
gained the Lua escape because some things don't fit a DSL. We start
with the same shape and the same escape valve planned from day one
(`cli/` for orchestration, `brief/` for the LLM briefer in phase 1+).

**Strengths.**

- Public GPL, large corpus — `data/` is ~10k `.cfg` files of working
  event scripts at every scale (1-line item placement to 5k-line
  campaign arcs).
- The grammar is the same triad across every noun — `[event]` is
  universally the reactive atom; `[filter]` is universally the gating
  shape. The pattern is proven at production scale (20+ years).
- `first_time_only` + `id` + `delayed_variable_substitution` are
  the **only three orthogonal fields** needed for save-compatible
  reactive content. Wesnoth discovered this empirically; our
  `event_id`/`first_time_only`/`delayed_variable_substitution`
  shape is the same.
- The Lua escape valve is documented and stable since 1.7 (15+
  years) — the precedent that "DSL + escape" ages better than
  either pure-DSL or pure-script.

**Weaknesses.**

- WML is its own parser — no JSON Schema, no validation against a
  type system. Save-compat bugs from typos are a known Wesnoth pain.
  Our `schemas/event.schema.json` (D-023 / `EVENT_SCHEMA.md` ↔ JSON
  Schema sync, test-enforced) is the explicit fix.
- WML's `filter_condition` expression language has grown organically
  over 20 years — booleans, variable refs, function calls. It's a
  Lisp-in-disguise; we don't want one. Our preconditions stay as
  `Dict[str, list]` data structures, not as an embedded language.
- WML's macro system is textual substitution — debug stack traces
  show post-macro code, not source. Our Python pack loader has
  direct file/line attribution.
- WML's `[event]` `name` enum is open (mods add new names by
  registering Lua hooks); our `action_type` is closed-by-design
  (INV-3: extensibility via pack data, not via code).
- WML events fire on the engine's tick (with wall-clock music
  scheduling, for instance); we fire on our `(tick, sub_order,
  actor_id)` queue key (INV-2). The determinism law is stricter than
  Wesnoth's.
- No event log — runtime state lives in save files (a snapshot,
  not a log). Our INV-1 (state = fold(log)) is the inverse; the
  amnesia anti-pattern ported to DSL scale (`mesa.md`).

**Verdict.** Phase-3 event-grammar reference, positive on the
`[event]`/`[filter]`/`action` triad and the `first_time_only`/
`id`/`delayed_variable_substitution` orthogonal fields, negative on
porting the DSL or the filter expression language — our JSON-schema-
enforced pack data and Python rule evaluator are the INV-3 fix. The
Lua escape hatch is the precedent for our `cli/`/`brief/` split. The
`name` enum shape (closed trigger vocabulary) is the direct lift
into `actions.json`.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
