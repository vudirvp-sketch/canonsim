# RimWorld · `REFERENCES.md` §1 + §10 + §14 · proprietary (pattern only) · phase 3 (director / pacing ref)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015). Source is proprietary — public modding wiki, dev
> diaries, GDC talks only. No code, no assets, no 1:1 rewrites
> (`REFERENCES.md` §0.5).

**What it is.** A colony-management/simulation game by Ludeon Studios
(Tynan Sylvester, 2013 early access, 2018 1.0). The player directs
colonists on a frontier world; an AI "Storyteller" paces events. Closed
source; the modding wiki and the in-game XML def format are public; the
AI director logic itself is in C# assemblies and only visible through
decompiled code (forbidden per §0.5 — read the wiki's behavioural
descriptions only).

**Concrete mechanics.**

- **Defs** — every content object is an XML `<Def>` with a `defName`
  and a `<parent>` inheritance chain. The canonical categories (from
  the modding wiki ` RimWorldWiki: Modding Tutorials/Defs`):
  `ThingDef` (items, pawns, buildings, plants), `PawnKindDef` (a
  pawn archetype — fleshed out by `ThingDef` for the species),
  `FactionDef` (a faction's ideological + spawn rules), `QuestDef`
  (a chained-script for narratives), `IncidentDef` (the storytelling
  atom), `RulePackDef` (a procedural-text rulepack shared by
  quests, names, tales), `TaleDef` (a logged event format for
  the chronicle), `RoyalTitleDef` (a status ladder), `ToolCapacityDef`,
  `HediffDef` (a state on a pawn — injury, disease, augmentation),
  `TraitDef`, `SkillDef`, `RecipeDef`, `WorkGiverDef` (an action
  source for pawns), `DesignationDef`, `TrainableConceptDef`. The
  pattern: **every noun in the world is a `*Def`; the engine is
  a Def-table interpreter**. The wiki lists ~50 top-level def
  types; the actual engine has ~120.
- **`ThingDef` inheritance** — `<ThingDef ParentName="MealBase">`
  is the canonical example. A child def inherits `<statBases>`,
  `<comps>` (a `List<CompProperties>` of component-property blocks),
  `<tradeTags>`, `<recipes>`, `<costList>` and adds or overrides
  per-field values. The `copy-from` analogue in C:DDA
  (`cdda_data_json.md`) is the same idea, but RimWorld inherits on
  class ancestry (`ParentName`) rather than by an explicit
  `copy-from` string. **`abstract="True"`** marks a def as a
  template — never instantiated; only inherited from.
- **`IncidentDef` — the storytelling atom.** Every world-level event
  has: `<workerClass>` (the C# `IncidentWorker` subclass that
  executes it), `<category>` (one of `ThreatBig`, `ThreatSmall`,
  `Neutral`, `Good`, `Misc`, `AllyArrival`), `<targetTags>` (what
  the target must be — `Map_PlayerHome`, `Map_Misc`, `World`),
  `<baseChance>` (the per-day weight used by the category picker
  when not overridden), `<minDays>`, `<maxDays>` (a soft cooldown
  window), `<minRefireDays>`, `<earlyChance`/`lateChance` (a
  per-population-stage curve), `<mtthDays>` for some incident
  families, and a `<rules>` block (a `RulePackDef` reference) that
  generates the letter text and Tale. The fields are public on the
  wiki. The **`IncidentWorker` subclasses** implement generation
  (where to spawn, how many raiders, what loot) and **execute**
  (spawn the raid, register the tale, fire the next-stage quest
  hook). The category picker is the storyteller's prerogative.
- **Three storytellers = three pacing policies**, not three AI
  personalities. Each is a `StorytellerDef` with an
  `<incidentMaker>` class chain — `StorytellerComp_PermanentCounter`,
  `_Random`, `_OnboardingCycle`. The wiki and the in-game
  difficulty select screen name them:
  - **Cassandra Classic** — strict **escalation**: every cycle,
    threat points grow linearly with the colony wealth + day count.
    The "desired threat score" curve rises monotonically; incidents
    are queued to push the actual score toward the desired.
  - **Phoebe Chillax** — long plateaus: same escalation math, but
    with longer rest beats between incidents; the threat growth
    slope is halved.
  - **Randy Random** — pure stochastic: no escalation, no
    cooldown symmetry, an `IncidentQueue` shuffled by a single
    seeded RNG. Randy is the existence proof that "AI director =
    pacing algorithm" — the same IncidentDefs behave wildly
    differently under a random queue vs an escalation curve.
- **Threat points = f(wealth, day, population)** — a single number
  that scales raider count / raid composition / loot per incident.
  Formula fields on the wiki: `pointsPerColonist` (wealth-weighted
  per pawn), `timeFactor` (a `PlotType.Ascending` curve from
  `GameConditionDef`), `populationFactor` (a 5-step table indexed
  by `PawnsInFaction`). The point is **not** the exact formula
  (which is closed source) — the pattern is: **a scalar combining
  wealth + time + population drives the difficulty of every spawned
  threat**. The director scales output, never invents new content
  (D-005 preserved — same lesson we adopt for `P2e narrative
  entropy`).
- **Tales — the chronicle layer.** A `TaleDef` is the canonical
  record of a notable event (`Raid`, `ManhunterPack`,
  `MaddenedHumanlike`, `Fired`, `Recruited`, `Tamed`,
  `KilledColonist`, `KilledBy`, `BuildingsConstructed`, …). Each
  Tale has: `rulePackDef` (the prose generator — a list of rule
  bags, each with `[taleNoun]`, `[subject]`, `[object]`,
  `[place]` substitutions — exactly the tracery-shaped template
  expansion that our `render/` will use); `baseRules` (a
  default pack); `taleType` enum (`PawnEvent`, `AlliedBattle`,
  `ColonistEvent`, etc.); `maxThreads` (how many concurrent
  instances the chronicle may stack before pruning the oldest).
  The Tale is created at incident execution, attached to the
  entity or location that participated, and consumed by the
  chronicle generator — this is **the public-facing canonical
  record**, exactly the role our JSONL log plays. The lesson:
  separate the **event** (incident execution, effect applied) from
  the **tale** (prose-ready canonical record).
- **QuestDef — scripted arcs.** A `QuestDef` chains signals
  (`signals`), timeout properties (`hoursRegrow`,
  `daysAccepted`), and a sequence of `QuestPart` blocks:
  `QuestPart_CollectThings`, `QuestPart_PawnsArrive`,
  `QuestPart_DropPods`, `QuestPart_TravelAndShoot`, `QuestPart_
  ActivationTargets`, `QuestPart_Monolith_PsychicSpecifier`. Each
  part is a stage — the quest signals fire from incidents, the
  signal bus dispatches, and parts execute on activation. **This
  is the same shape as our `Intent`/`Event` boundary:** the quest
  is the spec, the parts execute at signal time, the chronicle
  records. The def is **data**; the executor is **code** — the
  INV-3 split, executed at RimWorld scale.
- **The named anti-pattern (D-005).** The storyteller is the
  reference case for "from-nothing complications" — Randy's
  `raidAmbush` may drop a mechanoid cluster on a peaceful colony
  because the queue was shuffled and the worker class can target
  any map with `Map_PlayerHome`. Our director (`P2e`) explicitly
  refuses this: the lowest-threshold seeded hook is released
  **only when entropy drops** (sum of seeded-hook weights + global
  suspicion + visible physical threats), never inventing new
  threats. RimWorld is the cautionary tale that names the rule.

**What we take.**

- **Defs taxonomy shape.** The `*Def` family — `ThingDef` /
  `PawnKindDef` / `IncidentDef` / `TaleDef` / `QuestDef` /
  `FactionDef` / `RulePackDef` — is the same conceptual shape
  our `content/tavern_pack/` uses: `entities.json`,
  `actions.json`, `rules.json`, `templates.json`. The C:DDA
  precedent (`cdda_data_json.md`) lifted the same shape; RimWorld
  adds the **inheritance chain** (`ParentName` + `abstract="True"`)
  that we should adopt in iter-2 if duplication appears.
- **`IncidentDef` field set** — the **`baseChance`** (per-day
  weight), **`earlyChance`/`lateChance`** (per-population-stage
  curve), **`minRefireDays`** (cooldown), **`category`** enum
  (Threat/Neutral/Good) — is the exact shape for our seeded-hook
  director (`DIRECTOR_SPEC` sketch in `SPECS_BACKLOG.md`). We
  rename the fields (no domain words: "raid", "mech cluster") but
  the **scalar-weight + category-bucket + cooldown** triad is
  RimWorld's contribution.
- **TaleDef = our `ChronicleEntry` analogue** (`render/` spec,
  not yet written). The rulePack + baseRules + taleType trio is
  the tracery-shaped prose generator — exactly the template
  expansion our `render/` will use. RimWorld's lesson: the tale
  is created at incident execution time, attached to the entity
  or location that participated, and pruned after `maxThreads`
  concurrent instances. This is the **canonical record → prose
  record** split our `MVP_SCOPE.md` §11 already models.
- **Threat points = scalar combining wealth + day + population**
  — the pattern (not the formula) for our `M4` novelty / `M5`
  non-PC event share metrics. The director scales output by
  visible state, never by invisible state — same lesson our
  `P2e` narrative entropy formalizes.
- **Storyteller = policy, not personality.** Cassandra /
  Phoebe / Randy are three policies on the same IncidentDefs.
  Our director on/off switch (`MVP_SCOPE.md` §5) and the
  A/B replay at the gate (T8) inherit this directly: the
  IncidentDefs are the same; the queue is different; the run
  is byte-identical given seed.

**What we adapt.**

- **`IncidentDef` with `earlyChance`/`lateChance` → seeded-hook
  weights in `rules.json`.** RimWorld's curve is indexed by
  population stage; our director's curve is indexed by **visible
  state** (suspicion level, fire spread, watch roster). Same
  shape (a `Dict[str, float]` keyed by stage), different axis.
- **StorytellerComp classes → director policies in core code
  (no domain words).** RimWorld's `StorytellerComp_PermanentCounter`
  and `_Random` are C# classes named for in-universe concepts.
  Our equivalent is an **abstract `DirectorPolicy` interface** in
  `core/` with `escalation_factor(tick, visible_state) → float`
  and `should_fire(seeded_hook, current_state) → bool` — the
  in-universe narrators ("the barkeep's voice", "the watch
  captain's eye") live in `content/tavern_pack/` data, not code.
- **Threat points → `narrative_entropy` (`P2e` proposal).**
  RimWorld's scalar is `wealth + day + population`; ours is
  `seeded_hook_weights_sum + global_suspicion +
  visible_physical_threats`. Same shape (a single float for
  pacing decisions), different inputs — and explicitly no
  invisible inputs (D-005 preserved).
- **TaleDef pruning by `maxThreads` → chronological-pruning
  window in `render/`.** RimWorld keeps the last N tales per
  `taleType`; our chronicle will keep the last N events per
  `cause` chain — same idea, applied to causal chains not just
  type buckets.

**What inspires us.** The **director = pacing algorithm, not
narrator** lesson. RimWorld's storytellers are not LLMs, not
generators of novel threats; they are queue-and-weight policies
over a fixed content set. This is the existence proof that **a
simulation can pace itself without inventing** — exactly the
design our `MVP_SCOPE.md` §2 promises and `VISION.md` §6 forbids
LLMs from doing. Randy Random is the limit case: an AI director
with no escalation curve, just a seeded shuffle, and it is still
playable. The anti-pattern (D-005) is what we cut from Randy;
the queue-and-weight pattern is what we keep from all three.

**Strengths.**

- The Defs wiki is **the largest single public dataset of
  data-driven game content** (~120 def types, every one with
  field names + examples). The pattern is the gold standard.
- The storyteller trio is a **living proof-of-concept** that
  three policies on the same content set produce three
  recognisably different experiences — our T8 A/B replay is a
  direct homage.
- Tales + RulePacks are **the only public chronicle format**
  in the survey with explicit `rulePack` + `baseRules` +
  `taleType` + `maxThreads` — the canonical-record →
  prose-record split, public and documented.

**Weaknesses.**

- **Closed source.** The C# `IncidentWorker` executor classes
  are public in decompiled form (permitted — but only the
  signatures and names; the algorithm internals are inferred
  from play, not from code). The exact `desiredThreatScore`
  curve is undocumented; our adaptation copies the shape, not
  the numbers.
- **Randy's from-nothing anti-pattern** (D-005) — explicitly
  named in our `CORE_DESIGN_RESEARCH.md` §2 row. Our `P2e`
  refuses this: no new threats from the queue, only releases
  of the lowest-threshold seeded hook when entropy drops.
- **No causal chain.** RimWorld Tales are records, not graphs;
  the cause of a raid is implicit in the worker class, not in
  the Tale. Our `cause` (P1a) is a separate field — the
  RimWorld lesson is what we add, not what we copy.
- **No event-sourcing.** The Defs are static content; the
  runtime state lives in save files (a snapshot, not a log).
  Our INV-1 (state = fold(log)) is the inverse of RimWorld's
  save-on-event approach — the amnesia anti-pattern is the
  same Mesa / Sims problem (`mesa.md` weakness), ported to
  colony-sim scale.

**Verdict.** Phase-3 director + content-pack reference, mostly
positive on the data-driven layer (Defs taxonomy, IncidentDef
field shape, TaleDef = chronicle record, StorytellerDef = pacing
policy), explicitly negative on the Randy from-nothing
anti-pattern (D-005). The C# `IncidentWorker` internals are
out of bounds (closed source); the wiki field set is in
bounds (public documentation). RimWorld is the reference that
names our anti-pattern and gives shape to our director.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
