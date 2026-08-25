# Paradox event scripting (CK3 + EU4 + Stellaris) · `REFERENCES.md` §1/§10 · proprietary (wikis are CC-BY-SA documentation; games closed) · phase 3 (event grammar)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md` §10;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2 (row
> "CK3 / Paradox scripting"); concrete mechanics here. License filter
> and "patterns not content" rule: `REFERENCES.md` §0.7 (D-015). The
> three Paradox grand-strategy wikis are documentation under CC-BY-SA,
> but the games themselves are proprietary. We lift *grammar shapes*
> (trigger / effect / option / scope / on_action / weight / MTTH), never
> prose, never vanilla event IDs, never CK3-specific on_action names
> (`on_betrothal_broken` is a game-domain word; our on_action IDs are
> tavern-domain — `on_purse_reported_missing`).

**What it is.** The scripting grammar shared across CK3, EU4, and
Stellaris: events as `events/*.txt` blocks with a typed root scope, a
trigger predicate, an optional MTTH, an `immediate` effect block, and
one-or-more player-facing `option` blocks with `ai_chance` weighting.
The single most influential existing event grammar for any
narrative-simulation project — and the named anti-pattern our INV-2 was
designed against (MTTH = wall-clock + per-scope RNG, anti-deterministic
by construction).

**Concrete mechanics.**

- **File layout**: `events/*.txt` in the mod's `events/` folder; BFS
  loaded; arbitrarily many events per file. CK3 allows namespaces
  spanning multiple files; each file declares `namespace = <name>` as
  its first non-comment line, event ids are `<namespace>.<number>` (max
  9999 per namespace — exceeding breaks the calling system). EU4 +
  Stellaris use the same `namespace = X` + `id = X.N` pattern; in EU4
  the namespace is optional (raw numeric IDs allowed, 0–9999). Stellaris
  trims leading zeros (`action.003` == `action.3`). CK3 wiki explicit:
  "Events do not fire automatically otherwise" — every event must be
  *fired* from somewhere (an `on_action`, a decision, an effect, another
  event).
- **Typed root scope wrapper (the outer attribute declares what kind of
  entity the event fires on)**:
  - CK3: `type = character_event | letter_event | duel_event |
    fullscreen_event | empty | none`. `empty` = "characterless events";
    `none` = no root scope.
  - EU4: `country_event` (root scope = country) or `province_event`
    (root scope = province). Two wrappers only.
  - Stellaris (richest): `event` (global), `country_event`,
    `planet_event`, `fleet_event`, `ship_event`, `pop_faction_event`,
    `pop_group_event` (was `pop_event` pre-v4), `observer_event`,
    `system_event`, `starbase_event`, `leader_event`,
    `espionage_operation_event`, `first_contact_event`,
    `situation_event`, `agreement_event`.
- **Required + optional top-level fields inside an event block**:
  `id` (required, unique). The wiki checklist: `id`, `title`, `desc`,
  `picture`, `trigger`, `MTTH` or `is_triggered_only = yes`, ≥1
  `option`. Real optional flags (universal): `is_triggered_only = yes`
  (only fires when called from elsewhere — makes MTTH useless except in
  on_action `random_events`), `fire_only_once = yes` (stateful
  "already-fired" gate, game-wide not per-actor), `hidden = yes` (EU4) /
  `hide_window = yes` (Stellaris) / `hidden = yes` (CK3) — runs in
  background, no popup. EU4-only: `major = yes` (popup shown to *all*
  countries, optionally filtered by a `major_trigger = { ... }` block).
  Stellaris-only: `diplomatic = yes` (looks like first-contact comms),
  `custom_gui` / `custom_gui_option` (replace event UI).
- **Trigger block** (`trigger = { ... }`): the condition that must hold
  for the event to fire. The root of a `trigger = {}` is an implicit
  **AND** — wrapping contents in `AND = { ... }` is redundant.
  "Early-out" semantics: as soon as one inner trigger returns false,
  the rest are not evaluated (perf matters in pulse events). Logic
  blocks: `AND = { ... }`, `OR = { ... }`, `NOT = { <single trigger> }`
  (negation, only one inner trigger recommended), `NOR = { ... }`
  (none true), `NAND = { ... }` (not all true). CK3 adds
  `trigger_if = { limit = { ... }  <triggers> }`, `trigger_else_if`,
  `trigger_else` for conditional evaluation — exists because early-out
  breaks when tooltipped. EU4 encodes implication as
  `OR = { NOT = { P }  Q }`. Stellaris supports
  `switch = { trigger = ...  case_1 = { ... }  fallback = { ... } }`.
  Value comparison operators: `>`, `>=`, `<`, `<=`, `=`, `!=`.
- **Trigger subforms (CK3 generalized)**: *basic* boolean (`is_ai = yes`),
  *simple* one-arg (`has_trait = brave`), *complex* block
  (`is_scheming_against = { target = ...  type = ... }`), and
  *scripted triggers* — macros in `common/scripted_triggers/`, callable
  as `is_rich_adult_independent_ruler = yes`; complex form takes `$ARG$`
  substitution (`is_related_vassal_of = { TARGET = title:k_france.holder }`).
- **Real trigger tokens (CK3, sampled)**: `is_ai`, `is_adult`,
  `is_female`, `is_independent_ruler`, `is_vassal_of = <scope>`,
  `is_close_family_of = <scope>`, `is_scheming_against = { target = X
  type = Y }`, `has_trait = brave | drunkard | infirm`, `has_title =
  title:k_france`, `has_innovation = innovation_guilds`,
  `has_building_or_higher = blacksmiths_01`, `gold > 1000`,
  `exists = primary_spouse`, `always = yes | no`.
- **Real trigger tokens (EU4, sampled)**: `tag = FRA`, `stability = 1`,
  `religion = protestant`, `culture = basque`, `culture_group = iberian`,
  `adm = 3 | dip = 6 | mil = ...` (ruler skill), `adm_power = 600`,
  `adm_tech = 4`, `army_size = 15`, `army_tradition = 75`,
  `army_professionalism = 0.10`, `absolutism = 50`,
  `accepted_culture = ROOT`, `is_part_of_hre = yes`, `alliance_with =
  FRA`, `at_war_with_religious_enemy = yes`, `has_building = fort_15th`,
  `has_country_flag = X`, `is_year = 1500`, `num_of_estates = 3`,
  `gold = 2` (note: this is "≥2 provinces producing gold", not
  currency — EU4 reuses bare keys as type-polymorphic triggers: `<advisor>
  = 3` = "has hired a level-3 advisor of that type"; `<building> = 3` =
  "≥3 buildings of that type"; `<religion> = -2` = "tolerance of that
  religion ≥ -2"; `<trade good> = 2` = "≥2 provinces producing that good").
- **MTTH — `mean_time_to_happen = { ... }`** (the anti-pattern):
  - Base value: `days = N`, `months = N`, `years = N`. EU4 has
    `is_mtth_scaled_to_size = 1` for province events (doubles MTTH
    when owner has 2 provinces, quadruples with 4 — prevents event spam
    in large empires). CK3 has moved away from MTTH in favor of
    `is_triggered_only` + pulse on_actions. Stellaris wiki explicit:
    vanilla is removing MTTH for performance.
  - Modifier blocks stack when their conditions hold:
    ```
    mean_time_to_happen = {
      months = 400
      modifier = { factor = 0.8  NOT = { stability = 0 } }
      modifier = { factor = 0.5  war_exhaustion = 5 }
    }
    ```
    `factor = N` multiplies the MTTH (smaller = fires sooner). EU4
    inverts this for `random_events` MTTH: when the event is in an
    on_action's `random_events` list with `days = 1`, `factor = 0.8`
    makes the event *less* likely (applied to the weight, not the
    MTTH). Same field name, opposite meaning by call site.
  - **Why MTTH is anti-deterministic by construction**: the wiki prose:
    "A MTTH of 3 months means that on average, the event should fire
    about every 6-7 months (though of course, it may fire the next day,
    or never at all, such is the nature of probability)." Stellaris
    wiki: "it is not clear how exact the internal implementation of this
    delay works, however it seems likely the MTTH is regularly polled
    just like all other triggers." MTTH is wall-clock + per-scope RNG
    state, polled at an engine-internal cadence — **not** a
    tick-scheduled fire keyed by an externally observable deterministic
    queue. There is no contract that two runs of the same seed produce
    the same fire tick.
- **Weight blocks** — `weight_multiplier = { ... }`, also `ai_chance`:
  ```
  weight_multiplier = {
    base = 1
    modifier = { add = 1  trigger_conditions = yes }
    modifier = { factor = 0.5  has_trait = paranoid }
  }
  ```
  Shape: `base = <int>` + zero-or-more `modifier = { add = N | factor =
  N  <trigger> }`. CK3 `ai_chance` inside an option uses this exact
  shape plus a CK3-only `ai_value_modifier = { ... }` block referencing
  AI personality axes: `ai_boldness`, `ai_compassion`, `ai_greed`,
  `ai_energy`, `ai_honor`, `ai_rationality`, `ai_sociability`,
  `ai_vengefulness`, `ai_zeal` — nine axes. Stellaris `ai_chance` is
  simpler: `factor = N` at top + `modifier = { factor = 0  <trigger> }`
  blocks (multiplicative, can zero an option out). EU4 follows the same
  shape as Stellaris (no personality axes). Where weight is used: (a)
  **AI option selection** — every `option` may carry `ai_chance`; (b)
  **on_action `random_events` picking** — weights are literal integers
  prefixed to event ids; (c) **`random_list` outcomes** in effects.
- **Effect lifecycle** (universal three-phase):
  - `immediate = { <effects> }` — runs the instant the event fires,
    before the title/desc/portraits are evaluated or rendered. Used
    for state mutation the player can't undo (e.g. spawn the rebel
    stack *before* the option that mentions them appears), for saving
    scopes (`save_scope_as = generated_actor`) the localization will
    reference, and for variables the options will read.
  - `option = { name = <loc_key>  <effects> }` — runs when the player
    picks that option. May carry its own `trigger = {}` (gates
    availability), `ai_chance = {}`, `custom_tooltip`,
    `hidden_effect = { ... }` (effects whose tooltips are suppressed),
    `goto = <province_id>` (camera refocus), `highlight = yes`.
    CK3-only: `show_as_unavailable = { ... }`, `fallback = yes` (shown
    when no other option's trigger passes), `exclusive = yes` (when
    valid, hides other options), `flavor = <loc_key>`, `trait = honest`,
    `skill = prowess` (display flavor — the trait/skill icon on the
    option's left side; does not affect functionality, only tooltip
    flavor), `add_internal_flag = special | dangerous` (yellow/red
    highlight on the button), `highlight_portrait = scope:X`.
    Stellaris-only: `default_hide_option = yes` (selected when
    "Cancel" is pressed — does NOT hide the option despite the name),
    `exclusive_trigger = { ... }` (when valid, disables all others),
    `allow = { ... }` (shown but not choosable — checked once when the
    window opens, not every tick), `tag = ...` (special tag for
    leader-recruit event-window type).
  - `after = { <effects> }` — runs after the chosen option's effects,
    regardless of which option was picked. The "finally" block: clean
    up variables, delete event-spawned characters, clear flags.
- **Real effect tokens (CK3 + EU4, sampled)**: `add_gold = 50` /
  `add_short_term_gold` / `add_long_term_gold` / `add_reserved_gold` /
  `add_war_chest_gold` (CK3 partitions gold by use-bucket); `add_prestige
  = 10`; `add_piety = 10` (CK3) / `add_dip_power`, `add_adm_power`,
  `add_mil_power` (EU4 — monarch power, the EU4 analog of piety);
  `add_stability = 1` (EU4); `add_treasury = 50` (EU4 currency — not to
  be confused with `gold =` trigger which is "provinces producing
  gold"); `add_dread = 5` (CK3); `add_trait = brave`;
  `add_opinion = { target = scope:X  modifier = rebellious_vassal_opinion
  opinion = 25  years = 10 }` (CK3, complex block form);
  `add_hook = { type = X  target = Y  secret = Z  days | months | years
  = W }` (CK3) — **secrets and leverage as first-class facts** (the
  P3a precedent); `create_character = { age = { 20 32 }  location =
  root.capital_province  culture = root.culture  faith = root.faith
  random_traits = yes  trait = blind  martial = { 3 10 }  dynasty = none
  after_creation = { ... }  save_scope_as = generated_actor }` (CK3 —
  block form, range-typed sub-fields, after-creation hook, save scope);
  `create_dynamic_title`, `create_alliance = scope:X`,
  `create_divergent_culture`, `create_hybrid_culture =
  culture:anglo-saxon` (CK3); `set_relation_best_friend = scope:X`,
  `set_relation_antiquarian = scope:X` (CK3 — `set_relation_<type>`
  family); `change_religion`, `change_culture`, `change_graphical_culture
  = westerngfx` (EU4); `set_country_flag = my_flag` (EU4) /
  `set_global_flag = X` (EU4) / `clr_country_flag = X` /
  `clr_global_flag = X` — flags are persistent boolean state used as
  guard rails ("event already fired", "decision available");
  `declare_war_with_cb = { who = ROOT  casus_belli =
  cb_independence_war }` (EU4); `remove_country = yes`, `change_tag =
  FRA`, `release = CHL`, `set_bankruptcy = FRA`,
  `add_government_reform = revolutionary_empire_reform`,
  `add_absolutism = 10`, `add_inflation = 2`, `add_mercantilism = 2`
  (EU4).
- **`random_list = { ... }` shape (probabilistic effects)**:
  ```
  random_list = {
    20 = { add_prestige = 40
           modifier = { factor = 2  tag = CAS } }
    80 = { trigger = { alliance_with = FRA }
           add_stability = 1 }
  }
  ```
  Weights sum to 100; if not, they're scaled to keep the ratio. CK3 form
  is simpler: `random_list = { 50 = { add_gold = 25 }  50 = { add_gold =
  500 } }`. CK3 also has the singleton `random = { chance = 25
  <effects> }` — 25% chance the effects fire, 75% nothing. EU4 wiki
  determinism caveat: "both of these scopes may not always return a
  random result. This occurs when they are used in a non-seeded script
  location. An example of this are decisions and any events in the same
  event chain — using a random scope there will always return the same
  result every time the decision is done." (Anti-pattern: random
  behavior without an explicit seed.)
- **Scopes — the heart of Paradox scripting.** A scope is an implicit
  context object — the database entity the current trigger/effect is
  operating on. Triggers read from the current scope; effects write to
  it; scope-switching effects move to a different scope.
  - Standard top-level scopes:
    - CK3: `character`, `landed_title` (a.k.a. `title`), `province`,
      `dynasty`, `house`, `religion`/`faith`, `culture`, `government`,
      `war`, `combat_side`, `faction`, `scheme`, `activity`, `artifact`,
      `struggle`, `secret`, `hook`, `knight`, `army`, `regiment`,
      `court`.
    - EU4: only two base internal scopes — `country` and `province`.
      Everything else is reached by scope-switching from one of these.
      Tags (`FRA`) and province IDs (`110`) are direct scopes.
    - Stellaris (richest): `country`, `sector`, `galactic_object`
      (solar system), `megastructure`, `ambient_object`, `planet`,
      `deposit`, `archaeological_site`, `army`, `pop`, `pop_faction`,
      `species`, `leader`, `ship`, `fleet`, `debris`, `design`,
      `federation`, `alliance`, `starbase`, `pop_group`,
      `first_contact`, `situation`, `agreement`, `espionage_operation`,
      plus the `any` / `every` / `random` / `ordered` / `all`
      *list-builders* which are both scope prefixes and iterator macros.
  - Scope-switching effects (CK3, real names): `every_child`,
    `every_courtier`, `every_vassal`, `every_knight`, `every_held_county`,
    `every_county_province`, `random_courtier`, `random_child`,
    `any_courtier`, `any_child`, `any_vassal`, `any_knight`, `liege`,
    `father`, `mother`, `primary_spouse`, `primary_heir`, `realm`,
    `capital_county`, `capital_province`, `holder` (title → character),
    `dynasty`, `culture`, `faith`, `religion`. EU4: `capital_scope`,
    `owner`, `controller`, `random_active_trade_node`,
    `every_owned_province`, `every_country`, `random_country`,
    `any_country`. Stellaris: `owner`, `controller`, `space_owner`,
    `overlord`, `subject`, `last_created_country`, `branch_office_owner`,
    `home_planet`, `unhappiest_pop`, `leader`, `ruler`, `heir`,
    `alliance`, `associated_federation`, `species`, `owner_species`,
    `built_species`, `last_created_pop`, `last_created_army`,
    `last_created_leader`, `last_created_ship`, `last_created_fleet`,
    `last_created_system`, `last_created_design`.
  - Scope chaining: `title:k_france.holder` chains title → character.
    CK3 scope comparison: `title:k_france.holder = father` (true if the
    holder of France is the current scope's father). Database access:
    `<scope_type>:<key>` — `title:k_france`, `character:123`
    (historical only; runtime IDs not referenceable). Stellaris chains
    `prev` up to `prevprevprevprev` (4×), `from` up to `fromfromfromfrom`
    (4×). EU4: `PREV` / `PREV_PREV` / `ROOT` / `FROM` / `THIS`
    (uppercase). CK3: lowercase `root` / `prev` (single-step only) /
    `this`.
  - Saved scopes: `save_scope_as = <name>` (CK3),
    `save_event_target_as = <name>` (EU4 / Stellaris),
    `save_global_event_target_as = <name>` (persists across the chain /
    globally), `save_temporary_scope_as = <name>` (CK3 — expires at end
    of current block). Accessed as `scope:<name>` (CK3) /
    `event_target:<name>` (EU4 / Stellaris). Saved scopes carry through
    an unbroken effect chain (event A fires event B → `scope:X` set in
    A is readable in B); cleared at chain end or manually with
    `clear_saved_scope` / `clear_global_event_target`.
- **The three (four) iterator families** — the central Paradox
  abstraction:

  | Family | Variant | Role | Returns |
  |---|---|---|---|
  | `every_X = { ... }` | effect | iterate all matching scopes, apply inner effects to each | nothing (effect); skips if list empty |
  | `random_X = { ... }` | effect | pick one matching scope at random, apply inner effects | nothing; skips if list empty |
  | `ordered_X = { ... }` | effect (CK3) | sort by `order_by = <value>`, apply to first (or to a `position`/`min`/`max` range) | nothing |
  | `any_X = { ... }` | trigger | true if any matching scope satisfies inner triggers; stops at first true | boolean |
  | `all_X = { ... }` | trigger (EU4) | true if all matching scopes satisfy | boolean |

  All four accept a `limit = { <triggers> }` (EU4/CK3/Stellaris) or
  `filter = { <triggers> }` (CK3, inside `any_X`) sub-block to narrow
  the list before iteration. CK3 `any_X` also supports `count >= N` and
  `percent >= 0.5` to require N matches or a fraction. The shape is
  universal across all three games — only the spelling differs. **This
  is the single most important Paradox abstraction to lift.**
- **On-action events** — fire on game triggers. File location:
  `common/on_action/*.txt` (singular `on_action` — CK3 wiki flags
  plural `on_actions` as a common modder mistake). The canonical full
  block shape (CK3):
  ```
  on_birth_child = {                               # the on_action id
    events = {                                     # always-fire list
      my_event.1
      delay = { days = 365 }                       # delay applies to entries AFTER it
      my_event.2
      delay = { months = { 6 12 } }                # supports ranges; overrides previous
      my_event.3
    }
    random_events = {                              # pick ONE event (weighted)
      chance_to_happen = 25                       # % chance the whole block evaluates
      chance_of_no_event = { value = 0  if = { limit = { ... }  add = 10 } }
      100 = my_event.10                           # weight = 100
      200 = my_event.11
      100 = 0                                      # explicit "fire nothing"
    }
    first_valid = { my_event.20  my_event.21  fallback_event_without_trigger }
    on_actions = { my_other_on_action }           # fire other on_actions
    random_on_actions = { 100 = on_action_1  200 = on_action_2  100 = 0 }
    first_valid_on_action = { on_action_1  on_action_2 }
    effect = { <effects> }                         # runs concurrently with fired events
    fallback = another_on_action                   # called if nothing else fires
    trigger = { ... }                              # gates the whole on_action
    weight_multiplier = { base = N  modifier = { ... } }
  }
  ```
  Real on_action IDs (CK3, sampled from ~150+ total): `on_birth_child`,
  `on_birth_father`, `on_16th_birthday`, `on_death`, `on_divorce`,
  `on_leave_court`, `on_join_court`, `on_fired_from_council`,
  `on_pregnancy_mother`, `on_pregnancy_ended_mother`,
  `on_war_invalidated`, `on_war_transferred`,
  `on_war_won_attacker`, `on_war_white_peace`, `on_siege_completion`,
  `on_combat_end_loser`, `on_knight_combat_pulse`,
  `on_commander_combat_pulse`, `on_army_enter_province`,
  `on_raid_action_start`, `on_raid_action_completion`,
  `on_raid_loot_delivered`, `on_defeat_raid_army`,
  `on_county_faith_change`, `on_character_culture_change`,
  `on_title_gain`, `on_title_gain_usurpation`, `on_title_lost`,
  `on_rank_down`, `on_prestige_level_gain`,
  `on_prestige_level_loss`, `on_release_from_prison`,
  `on_faith_created`, `on_faith_monthly`, `on_holy_order_hired`,
  `on_great_holy_war_invalidation`, `on_alliance_added`,
  `on_betrothal_broken`, `on_concubinage`, `on_perks_refunded`,
  `on_weight_changed`, `on_guest_arrived_from_pool`,
  `random_yearly_playable_pulse`, `random_yearly_everyone_pulse`,
  `quarterly_playable_pulse`, `three_year_playable_pulse`,
  `five_year_everyone_pulse`, `on_game_start`,
  `on_game_start_after_lobby`. Stellaris (sampled): `on_game_start`,
  `on_game_start_country`, `on_single_player_save_game_load`,
  `on_monthly_pulse`, `on_yearly_pulse`, `on_bi_yearly_pulse`,
  `on_five_year_pulse`, `on_decade_pulse`, `on_mid_game_pulse`,
  `on_late_game_pulse`, `on_monthly_pulse_country`,
  `on_yearly_pulse_country`, `on_five_year_random_pulse_country`,
  `on_first_contact`, `on_first_contact_finished`,
  `on_enforce_borders`, `on_ground_combat_started`,
  `on_planet_attackers_win`, `on_planet_attackers_lose`,
  `on_planet_defenders_win`, `on_planet_defenders_lose`,
  `on_system_first_visited`, `on_entering_system`,
  `on_entering_system_first_time`, `on_entering_system_fleet`,
  `on_crossing_border`, `on_survey`, `on_planet_surveyed`,
  `on_system_survey`, `on_colonization_started`, `on_colonized`,
  `on_colony_destroyed`, `on_entering_battle`,
  `on_ship_destroyed_victim`.
  - **Append-vs-overwrite rule** (CK3): to add to an existing vanilla
    on_action without overwriting it, define your *own* custom
    on_action and add it via `on_actions = { my_on_action }` inside
    the vanilla on_action. Direct `trigger = { ... }` / `effect = {
    ... }` blocks on a vanilla on_action *overwrite* all vanilla logic
    for that on_action. Appending applies only to events and nested
    on_actions, not to trigger/effect blocks.
  - **Scope rule per on_action**: each on_action documents its
    expected scope. `on_game_start` has no root scope (fires globally
    once — must use `every_ruler` or similar). `yearly_playable_pulse`
    fires per playable character with that character as root. Stellaris
    uses `this` / `from` / `fromfrom` per on_action. **Critical perf
    rule from CK3 wiki**: "Do not use `every_living_character` in
    `yearly_playable_pulse` and similar on_actions. That on_action
    already fires for every character. If you then try to iterate
    through all characters, that would result in ~20000² operations."
- **Picture / portrait / window setup** (cosmetic; we drop all of it,
  see "What we adapt"): `picture = GFX_picture_key` (all three games)
  — references a sprite name in `interface/*.gfx`; culture/religion-
  prefixed sprite variants (`muslimgfx_ANGRY_MOB_eventPicture`) picked
  by the receiver's graphical culture, DLC-gated. CK3 portrait
  positions: `left_portrait`/`right_portrait`/`lower_left_portrait`/
  `lower_center_portrait`/`lower_right_portrait` — each a block with
  `character = scope:X`, `animation = idle | anger | fear | scheme |
  paranoia | grief | ...` (CK3 ships ~150+ animation IDs),
  `triggered_animation`, `triggered_outfit`, `hide_info`. CK3
  `theme = mental_break | realm | ...`, `override_background`,
  `override_sound`, `widgets = { widget = { gui = "..."  container =
  "..."  controller = ...  setup_scope = { ... } } }` (custom GUI).
  Stellaris `event_window_type = leader_recruit` (special-cased window
  for hiring leaders; option `tag = ...`), `picture_event_data =
  { portrait = ...  planet_background = ...  graphical_culture = ...
  city_level = ...  room = ... }` (diplomatic event window with
  animated portrait + room backdrop + city scale). The strict
  separation of "what happened" (event payload) from "how to show it"
  (asset reference) is the lesson — our `templates.json` is the analog
  of the `.gfx` file (canon/voice split, `VISION.md` §1).

**What we take.**

- **The typed root scope wrapper pattern** — an event declares what
  kind of scope it fires on as its outermost attribute
  (`character_event`, `province_event`, `planet_event`). Our
  `EVENT_SCHEMA.md` event type field is the analog. The
  `namespace.id` discipline (`my_events.1`, max 9999 per namespace) is
  the right shape for stable cross-reference and human-readable replay
  logs.
- **`trigger = { ... }` with implicit-AND root + `AND`/`OR`/`NOT`/
  `NOR`/`NAND` logic blocks + `trigger_if`/`trigger_else_if`/
  `trigger_else`** for safe conditional evaluation. The "early-out"
  rule (most-likely-to-fail first) is a perf principle we can adopt.
  Value comparisons with `>`, `>=`, `<`, `<=`, `=`, `!=` operators.
- **The `weight_multiplier = { base = N  modifier = { add = N | factor
  = N  <trigger> } }` shape** — the canonical primitive for
  context-sensitive probability. Use it for: (a) NPC option selection
  (the `ai_chance` analog — in our case NPC decision weighting, no
  "AI" vs "player" split); (b) on_action `random_events` picking;
  (c) `random_list` effects. The CK3 personality axes (`ai_boldness`,
  `ai_compassion`, `ai_greed`, `ai_energy`, `ai_honor`,
  `ai_rationality`, `ai_sociability`, `ai_vengefulness`, `ai_zeal`)
  are a great precedent for our NPC trait axes (per
  `content/tavern_pack/entities.json` NPC trait maps) — nine axes
  covering boldness, compassion, greed, energy, honor, rationality,
  sociability, vengefulness, zeal. We lift the *axes idea* (not the
  names — license-clean), generalized to a tavern setting.
- **The three-phase effect lifecycle**: `immediate = { ... }` +
  `option = { name = ...  <effects> }` + `after = { ... }` — before
  choice / on choice / after choice. In canonsim this maps to: (a)
  `consequences_seed` emitted at event-fire time (D-005), (b) the
  player-or-NPC choice, (c) the `state_changes` applied post-choice.
- **The three iterator families** — `every_X` (all matching), `random_X`
  (one random), `any_X` (test if any matches) — plus `ordered_X` and
  `all_X`. Saved scopes (`scope:foo` / `event_target:bar`) for
  cross-event reference. Scope chaining (`title:k_france.holder`). The
  `every/random/any` trinity is the cleanest possible abstraction for
  "do this to all / one-random / test-if-any of these related things."
- **The `add_opinion` / `add_hook` family** — *secrets and leverage
  as first-class facts* (P3a, `CORE_DESIGN_RESEARCH.md` §2 row for
  CK3). A hook *is an event in the log*, with a target, a type, an
  expiry tick, and a cause — not mutable state. Precedent for our
  `knowledge_record` and `leverage_record` event kinds.
- **The on_action dispatch table**: `on_action = { events = { ... }
  random_events = { ... }  first_valid = { ... }  on_actions = { ... }
  effect = { ... }  fallback = ... }` — the contract surface between
  the simulation core and the content layer. The simulation fires
  on_actions, content reacts. This is exactly our sim/director
  boundary.
- **The append-vs-overwrite rule** (CK3): multiple content packs can
  each add to the same on_action without clobbering. Our content-pack
  loader should support this.
- **The `fallback = yes` escape hatch** on options — guarantees "the
  player always has at least one option" — invariant-critical for our
  director.

**What we adapt.**

- **File location `events/*.txt` → JSON content packs** (D-015 — we
  lift patterns not text; the Paradox `.txt` parser is hand-rolled,
  our events are JSON per `EVENT_SCHEMA.md` §2, and the engine is a
  generic interpreter — the C:DDA pattern, see
  `docs/ref/cdda_data_json.md`).
- **MTTH → tick-bounded probability sampled by the seeded RNG**.
  Instead of "fires on average every 400 months" we compute, for each
  tick T where the trigger passes: `if rng.random() < p_per_tick:
  fire`. The per-tick probability `p_per_tick` is derived from a
  content-pack field `expected_interval_ticks` (e.g. 12000 for ~yearly
  at 100 ticks/day). Modifiers scale `p_per_tick` multiplicatively —
  but the *rng* call is keyed by `(tick, sub_order, actor_id)` per
  INV-2, so two runs of the same seed produce the same fire tick. This
  is the explicit rejection of the MTTH anti-pattern: consequences
  seeded at event time (D-005), never invented from nothing, never
  wall-clock-sampled. "MTTH is anti-deterministic by construction" is
  the named anti-pattern in `CORE_DESIGN_RESEARCH.md` §2 — INV-2 is
  the discipline that rejects it.
- **Triggers → pure predicates over projected state** (per D-023:
  runtime state = incremental projection over the log). No
  `is_triggered_only` flag — we *always* evaluate trigger
  predicates against current projection. No "early-out optimization"
  beyond what Python short-circuit gives us for free. The Paradox
  "scope comparison" `title:k_france.holder = father` becomes a
  Python equality check between two context-object refs.
- **Implicit-`this` language primitive → explicit context argument**:
  `def trigger(state, ctx): ...` — `ctx` is the current scope,
  `ctx.liege` is the scope-switched parent. The iterator families
  become Python helpers: `every(state, ctx, "vassal", predicate)`,
  `random_one(state, ctx, "courtier", predicate, rng)`,
  `any_match(state, ctx, "knight", predicate)`. The `rng` is the
  *seeded* `random.Random` instance, keyed by `(tick, sub_order,
  actor_id)` per INV-2. Same idea as Paradox scopes, more explicit,
  easier to test.
- **Effects emit, not mutate** — `add_gold = -50` becomes a
  `gold_changed` event in the JSONL log with `delta = -50, cause =
  "tavern_purse.1.option.a"`. The projection layer applies it (INV-1).
  `set_character_flag` becomes a `flag_set` event; "has flag X" is a
  *log query*, not engine-mutated state. The Paradox
  `set_country_flag` / `set_global_flag` pattern is a stateful kludge
  we replace by log queries.
- **`option.name` localization key → `templates.json` reference** (the
  canon/voice split, `VISION.md` §1). Track A emits structured event
  records; the LLM-renderer (track B, phase 1+) turns them into prose.
  We drop all of `picture`, `portrait`, `theme`, `widgets`,
  `override_background`, `override_sound`, `clicksound`,
  `event_window_type`, `custom_gui`, `custom_gui_option`, `goto`,
  `highlight`, `trait`, `skill`, `add_internal_flag` — all
  player-UX-cosmetic.
- **CK3 on_action names → tavern-domain IDs**: `on_betrothal_broken`
  is a game-domain word; our on_action IDs are tavern-domain
  (`on_npc_enters_tavern`, `on_purse_reported_missing`,
  `on_quarterly_pulse`, `on_day_phase_change`). We lift the
  dispatch-table grammar, not the game-domain vocabulary (INV-3 — no
  domain words in code).

**What inspires us.** **"Scopes-as-context" is the lesson, not the
syntax.** The Paradox language *is* scope-switching; our fold function
*takes* scope as a parameter. Same idea, more explicit, easier to test
— and the iterator trinity (`every/random/any`) is the smallest possible
abstraction for "do this to all / one-random / test-if-any of these
related things."

**Strengths.**

- The single most influential existing event grammar for any
  narrative-simulation project: three games, two decades of public
  iteration, ~150+ on_action IDs, hundreds of trigger/effect tokens.
- The `every/random/any` iterator trinity (plus `ordered` and `all`)
  is the cleanest possible abstraction for "do this to all /
  one-random / test-if-any."
- The `weight_multiplier` shape (`base + modifier{add|factor + trigger}`)
  is the smallest possible context-sensitive probability primitive.
- The `immediate + option + after` three-phase effect lifecycle
  captures "things that must happen before the choice is offered,
  things that happen on each choice, things that happen regardless."
- The `add_hook` family is the cleanest existing precedent for
  secrets-and-leverage as first-class facts (P3a).
- The on_action append-vs-overwrite rule is a real composability win
  — multiple content packs can each add to the same on_action without
  clobbering.

**Weaknesses.**

- **MTTH is anti-deterministic by construction** — wall-clock +
  per-scope RNG state, polled at an engine-internal cadence, not a
  tick-scheduled fire keyed by an externally observable deterministic
  queue. No contract that two runs of the same seed produce the same
  fire tick. This is the explicit reason INV-2 exists (per "What we
  adapt" above). EU4 wiki caveat: `random = { chance = N }` in
  non-seeded script locations (decisions, event chains) "will always
  return the same result" — Paradox's own RNG discipline is
  inconsistent across script sites.
- **Implicit scope-spaghetti** — `prev.prev.prev` chains,
  `fromfromfromfrom`, `ROOT` vs `THIS` confusion (EU4 uppercase vs CK3
  lowercase), `event_target:X` carrying across unbroken effect chains
  but cleared at chain end, "saved scope overwrites previous save with
  same name" footgun. CK3 wiki has multiple "common misconception"
  callouts. Our explicit context argument eliminates this entire class
  of bugs.
- **`is_triggered_only` + `fire_only_once` + `set_country_flag`** are
  implicitly stateful — the engine tracks "has this fired" via global
  flags, the same amnesia anti-pattern as Mesa / C:DDA (see
  `docs/ref/mesa.md`, `docs/ref/cdda_data_json.md`). INV-1 (append-only
  log) replaces this: "has event E fired for actor A at tick T" is a
  query against the log, not a flag the engine mutates.
- **Scope-typing is implicit** — wrong-scope-type trigger produces a
  runtime error in the *log*, not at parse time. We reject this by
  making scope-type a first-class field in the JSON event schema
  (parse-time validation).
- **Localization coupling** — every `name` points to a key in a
  localization file; events and loc files drift independently. CK3
  vanilla has 50k+ line event files. Our split (templates.json + canon
  events) has the same drift risk — mitigate with parse-time
  cross-reference validation.
- **Performance**: Stellaris wiki explicitly notes vanilla is removing
  MTTH for performance ("considerably more expensive in terms of
  performance" when modifiers are introduced, because the engine
  checks conditions every day per scope). The CK3 "do not use
  `every_living_character` in `yearly_playable_pulse`" perf footgun
  is real — iterator composition needs documenting. Our version:
  O(num_actors × num_active_triggers) per tick, deterministic, no
  polling-cadence question.
- **Closed-source engine** — we can read the wikis, not the engine
  code. Behavior claims are documentation-grade, not source-grade.

**Verdict.** Phase-3 event-grammar backbone. We lift the trigger /
weight / option / scope / on_action shapes (the grammar), never prose,
never vanilla event IDs, never CK3-specific on_action names. MTTH is
the named anti-pattern our INV-2 was designed against — wall-clock +
per-scope RNG, not tick-bounded + seeded RNG. Read at iter-4 (director
triggers, consequence planner) and iter-5 (chronicle templates). The
`add_hook` family is the precedent for P3a secrets-and-leverage (phase
4). Nothing here gates phase 0.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
