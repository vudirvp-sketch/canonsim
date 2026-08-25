# Cataclysm: Dark Days Ahead · `REFERENCES.md` §1 · CC-BY-SA 3.0 · phase 3 (content-pack reference)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015).

**What it is.** Post-apocalyptic survival roguelike
(`CleverRaven/Cataclysm-DDA`, CC-BY-SA 3.0). The reference implementation
of "content-as-JSON at scale": ~111 top-level entries in `data/json/` (a
mix of standalone `.json` files and category subdirs), thousands of
objects, the engine a generic JSON interpreter. The closest existing
precedent for our `content/tavern_pack/` at phase 0 and the model for what
phase-3 content packs must scale to.

**Concrete mechanics.**

- **Top-level layout** (`data/json/` — 111 entries at the time of
  writing): a mix of standalone files (`materials.json`, `skills.json`,
  `traps.json`, `monster_factions.json`, `vitamin.json` …) and category
  subdirs (`items/`, `monsters/`, `recipes/`, `itemgroups/`, `npcs/`,
  `mutations/`, `overmap/`, `mapgen/`, `vehicles/`, `vehicleparts/`,
  `proficiencies/` …). `LOADING_ORDER.md` documents the discipline: a
  **breadth-first search** over the tree, so `data/json/X.json` is loaded
  before `data/json/subdir/X.json`. Dependency-respecting: skills load
  before professions, professions before scenarios.
- **Item schema** (`data/json/items/*.json`, `type: "ITEM"`): `id`
  (string, unique), `name` (object with `str` / `str_sp` / `str_pl` keys
  — localization-aware, no bare strings), `description` (same shape, with
  optional `"//~": "NO_I18N"` marker for non-translatable), `symbol`
  (single ASCII char) + `color` (named: `"white"`, `"red"`,
  `"dark_gray"` …), `material` (list of refs into `materials.json`),
  `weight` / `volume` (strings with units: `"350 g"`, `"467 ml"`,
  `"1 L"`), `price` (string: `"0 cent"`, `"150 USD"`), `stackable`
  (bool), `flags` (flat enum list: `PSEUDO`, `PERPETUAL`,
  `WATER_PROOF` … — no inheritance tree, appendable, no schema break on
  adding new flags).
- **Monster schema** (`data/json/monsters/*.json`, `type: "MONSTER"`):
  `abstract` (string — for inheritance; abstract monsters don't spawn,
  others `copy-from` them), `name`/`description` (localization-aware
  objects), `default_faction` (ref into `monster_factions.json`),
  `categories` (`WILDLIFE` etc.) and `species` (`BIRD`, `FISH` …) — two
  orthogonal classification axes, `volume`/`weight`/`hp`/`speed` (units
  or ints), `aggression` (signed int; `-99` = docile, `+99` =
  immediately hostile), `morale` (signed — flees below threshold),
  `melee_dice` + `melee_dice_sides` + `melee_damage` (list of
  `{damage_type, amount}`), `dodge`, `material` (drop-table reference),
  `harvest` (id into `harvest.json`), `weakpoint_sets` (anatomy), and
  `families` (proficiency references — what the player learns from
  dissecting the monster).
- **Recipe schema** (`data/json/recipes/*.json`, `type: "recipe"`):
  `result` (item id produced), `activity_level` (enum: `LIGHT_EXERCISE`,
  `MODERATE_EXERCISE` … — feeds the player fitness system),
  `category` + `subcategory` (`CC_*` / `CSC_*_NESTED` — hierarchical),
  `skill_used` + `difficulty` (skill id + int level), `skills_required`
  (paired list `[[skill_id, level], …]`), `time` (string with units:
  `"25 m"`, `"2 h"`), `reversible` (bool — can be deconstructed),
  `decomp_learn` (skill level granted on deconstruction — bonus learning
  from disassembly), `book_learn` (paired `[[book_id, level_required],
  …]` — recipe gated by a book the player has read), `using` (paired
  `[["tool_qualities_id", charge_count], …]` — tool charge costs),
  `qualities` (list of `{id, level}` — tool qualities required, e.g.
  `{id: "SCREW", level: 1}`), `components` (list of alternatives —
  paired lists, each `[item_id, count]`, alternatives = any-of).
- **Itemgroup schema** (`data/json/itemgroups/*.json`, `type:
  "item_group"`): `subtype` (`"collection"` = spawn-all |
  `"distribution"` = pick-N), `entries` (list of `{item, count, prob,
  variant}`), `prob` is `0–100`, `count` is a range `[min, max]`.
  **Nested `collection` entries** for "one of these sets" — a sub-list
  inside an entry. This is the abstraction for loot tables / tavern
  inventory / NPC starting gear.
- **Mission schema** (`data/json/npcs/missiondef.json`, `type:
  "mission_definition"`): `id`, `name`, `goal` (enum: `MGOAL_GO_TO_TYPE`,
  `MGOAL_CONDITION`, `MGOAL_FIND_ITEM`, `MGOAL_KILL_NPC` …),
  `goal_condition` (JSON-predicate like `{u_has_item: "inhaler"}` —
  evaluated against the player's state), `difficulty` (int), `value`
  (reward in cents), `urgent` (bool), `start` (object with an `effect`
  array and an `assign_mission_target` shape — what happens when the
  mission is issued), `origins` (enum list: `ORIGIN_SECONDARY`,
  `ORIGIN_OPENER_NPC`, `ORIGIN_ANY_NPC` — who can offer it), `deadline`
  (string pair like `["2 days", "3 days"]` — duration range sampled at
  issue time), `dialogue` (object with `describe` / `offer` / `accepted`
  / `rejected` / `advice` / `inquire` / `success` / `success_lie` /
  `failure` — full conversation template inline).
- **NPC faction schema** (`data/json/npcs/factions.json`, `type:
  "faction"`): `id`, `name`, `likes_u`/`respects_u` (signed int — same
  shape as our `relations` map axes), `known_by_u` (bool), `size` /
  `power` (numerical attributes — `power` is the faction's effective
  strength), `consumes_food` / `wealth` (economy flags), `relations`
  (nested map keyed by **other-faction-id**, with booleans: `kill on
  sight`, `watch your back`, `share my stuff`, `guard your stuff`, `lets
  you in`, `defends your space`, `knows your voice` — pair-keyed with
  boolean attributes), `mon_faction` (ref into
  `monster_factions.json`), `epilogues` (state-gated epilogue blocks
  with `power_min` / `power_max` thresholds and `dynamic` cross-faction
  predicates — the precedent for our director triggers in phase 3).
- **Monster faction schema** (`data/json/monster_factions.json`, `type:
  "MONSTER_FACTION"`): `name`, `base_faction` (inheritance — attitude
  chain), `friendly` / `neutral` / `hostile` (lists of faction names),
  `by_mood` (mood-dependent override — faction attitude changes with
  monster mood). **Pair-keyed map** of monster-vs-monster relations —
  same shape as NPC factions and as Neighborly's `RelationshipTracker`
  (see `neighborly.md`).
- **Inline author commentary convention**: every C:DDA JSON file uses
  `"//": "..."` (and `"//2": "..."`, `"//~": "NO_I18N"` as a
  non-translatable marker) as inline documentation for humans. Our
  `content/tavern_pack/` uses `"_"` for the same job — minor cosmetic
  divergence, same pattern.

**What we take.**

- The **per-category file split** (items/ split into `ammo/`, `armor/`,
  `gun/` …) — scales to thousands of objects without merge conflicts.
  Our `content/tavern_pack/` already does this (`entities.json`,
  `actions.json`, `rules.json`, `templates.json`); C:DDA proves the
  discipline scales to ~111 categories.
- The **string-with-units convention** (`"350 g"`, `"25 m"`,
  `"0 cent"`) — human-readable, parseable, no magic numbers. Validates
  the content/code split (INV-3) at scale: ~111 files, thousands of
  objects, zero domain words in engine code.
- The **`abstract` + `copy-from` inheritance** for monsters — base
  archetypes that don't spawn but are referenced. C:DDA proves the
  pattern works for content with hundreds of variants of the same
  archetype (e.g. `mon_bird_flying_base` → many specific bird
  species). Useful precedent if `content/tavern_pack/` grows NPC
  archetypes in a later phase.
- The **`relations` map shape** in `factions.json` — pair-keyed by
  other-faction-id with boolean attributes (`kill on sight`, `watch
  your back`, `share my stuff` …). This is **exactly the same shape** as
  Neighborly's pair-keyed `RelationshipTracker` (see `neighborly.md`)
  and aligns with our P2a (D-020) sparse pair-keyed relation map for
  iter-3. C:DDA is the second independent validation of the data
  structure.
- The **`subtype: "collection" | "distribution"`** abstraction for
  itemgroups — exactly the loot-table / tavern-inventory primitive we
  need for `content/tavern_pack/` placement and starter inventory.
  Nested `collection` entries (one-of-these-sets) are non-trivial and
  on file.
- The **`//` field as inline author commentary** — `//`, `//2`, `//~`
  markers in every JSON file. Our pack uses `"_"` (per
  `content/tavern_pack/`); the convention is identical, the field name
  differs.

**What we adapt.**

- **Inline `dialogue` block → separate `templates.json`**: C:DDA
  inlines the full conversation (`describe`/`offer`/`accepted`/
  `rejected`/`advice`/`inquire`/`success`/`success_lie`/`failure`) in the
  `mission_definition` object — `missiondef.json` is 55k+ lines;
  cross-referencing by id impossible; localization is bolted on via
  `//~` markers. For phase 0 we keep templates in
  `content/tavern_pack/templates.json` and reference by id; for phase 1
  the LLM-renderer generates from the event log directly (canon/voice
  split, `VISION.md` §1).
- **Deadline as duration pair → event-time computation**: C:DDA's
  `deadline: ["2 days", "3 days"]` is a duration range sampled at
  mission-issue. We compute deadline as `issue_tick +
  sampled_duration` (INV-2: sampled via the seeded `random.Random(seed)`
  instance), store as event field, never as wall-clock (D-004,
  `TECH_NOTES.md` §4).
- **String-with-units everywhere → pack data only, not code**: C:DDA
  parses strings like `"350 g"` at load time. For phase 0 we keep
  numbers as JSON numbers (grams, milliliters, ticks), not strings; the
  renderer formats them at output. C:DDA's convention is content-author
  convenience; ours is determinism (no parse-step ambiguity, no unit
  drift across builds — `TECH_NOTES.md` §4).
- **BFS-tree load order → `sorted()` discipline**: C:DDA's BFS-tree
  load discipline is required because of `abstract` + `copy-from`
  inheritance (base monster must exist before child) and cross-file
  references. Our load order is `sorted()` per INV-2 — pack files have no
  inheritance, only references, and references are name-based
  (resolve-after-load). Simpler discipline, same outcome.
- **CC-BY-SA license → lift patterns, not text**: CC-BY-SA is viral —
  if we lift text wholesale, our pack must also be CC-BY-SA. We lift the
  schema *shapes* (the abstractions are general), not the prose, not
  the enum values, not the field names tied to C:DDA's vocabulary. Per
  §0.7 of `REFERENCES.md` and D-015.

**What inspires us.** The **"content as data, code as engine"** posture
at scale. C:DDA is the existence proof that an entire game can be
authored as JSON content with the engine as a generic interpreter — 111
top-level data files, thousands of objects, zero code changes for new
content. Our `content/tavern_pack/` is a phase-0 micro-version of the same
discipline; C:DDA proves it grows.

**Strengths.**

- The reference implementation of content-as-JSON at scale. 111
  top-level entries, thousands of objects, CC-BY-SA, mature (15+ years
  of public development).
- Per-category file split (items/ split into `ammo/`, `armor/`, `gun/`
  etc.) — scales to thousands of objects without merge conflicts.
- String-with-units convention — every quantity carries its unit, no
  magic numbers, no "what does 350 mean?" hunting.
- The `abstract` + `copy-from` inheritance pattern for monsters — base
  archetypes that don't spawn but are referenced.
- The `relations` map shape in `factions.json` — pair-keyed with
  boolean attributes. Same shape as our P2a (D-020) sparse pair-keyed
  relation map; second independent validation after Neighborly
  (see `neighborly.md`).
- The `epilogues` block — state-gated, with `power_min`/`power_max`
  thresholds and `dynamic` cross-faction predicates. Direct precedent
  for our director triggers in phase 3 (D-005 consequence planner).
- The `//` field as inline author commentary — documentation lives next
  to the data, not in a separate README.

**Weaknesses.**

- **No event log / no event sourcing** (`CORE_DESIGN_RESEARCH.md` §2
  row "C:DDA"): C:DDA is state-mutating at runtime; the save file is a
  snapshot, not a fold-replayable log. Same amnesia as Mesa
  (see `mesa.md`). Our JSONL log + `state_changes` (INV-1) is the fix.
- **Inline `dialogue` blocks bloat mission definitions**: the full
  conversation template is inlined in the `mission_definition` object —
  `missiondef.json` is 55k+ lines; cross-referencing by id impossible;
  localization is bolted on via `//~` markers. We split templates from
  definitions (MVP_SCOPE §9, `templates.json`).
- **No causal chain**: missions reference `goal` (an enum) and
  `goal_condition` (a JSON-predicate), but there is no `cause` field —
  the "why did this mission get offered now" lives in the engine C++
  code, not the data. Our `cause` (`EVENT_SCHEMA.md` §2, P1a) is the
  missing ledger.
- **CC-BY-SA viral** — if we lift text, we inherit the license. We lift
  patterns only (D-015, `REFERENCES.md` §0.7); the license rule forces
  the "patterns not content" stance rather than treating it as optional.
- **No determinism contract** — engine uses wall-clock for many
  systems; save files are not byte-reproducible across builds. Our
  INV-2 is the discipline C:DDA lacks; we cannot lift C:DDA's runtime
  patterns, only its data-shape patterns.

**Verdict.** Phase-3 content-pack reference. The proof-of-existence that
the content/code split (INV-3) scales to thousands of objects across ~111
category files. We lift patterns (schema shapes, per-category file split,
string-with-units convention, `abstract`+inherit, pair-keyed `relations`
map, state-gated `epilogues`) — never text, never enum values, never
field names tied to C:DDA's vocabulary. CC-BY-SA forces the "patterns not
content" rule. Read the repo at iter-2 / iter-3 (when actions and the
content loader land). Nothing here gates phase 0.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
