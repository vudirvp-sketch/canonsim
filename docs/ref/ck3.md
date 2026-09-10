# Crusader Kings III — name pools & the culture-as-pillar shape · `REFERENCES.md` §1/§10 · proprietary (wiki docs CC-BY-SA; game closed) · phase 5 (name-1) + phase 6 (cultures/religions re-gate, D-116 (12))

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1 (ref-19-a). Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md` §10;
> one-line synthesis in the catalog row ("culture/religion as pillar +
> tag components; dynastic name pools"); concrete mechanics here. The
> Paradox event GRAMMAR (trigger/effect/option/MTTH/on_action) already
> lives in `docs/ref/paradox_scripting.md` — this file covers the other
> half: the culture/name data shapes. License filter: the game is
> proprietary; the wiki is CC-BY-SA documentation. We lift *data
> shapes* (the pool keying, the numbered-variant grammar, the
> key↔localization split), never vanilla name lists, never vanilla
> culture IDs (`norse`, `frankish` are game-domain words; our profile
> ids are the pack's own vocabulary — `tongue_a` in the tests, the
> province's two cultures in world-2).

**What it is.** The character-naming layer of CK3: per-culture curated
name pools (first names per sex, dynasty names) consumed by the
engine at character-generation time (births, courtier creation), plus
the culture-as-data shape those pools ride (heritage / language /
ethos / traditions pillars) — the most influential shipped example of
"names are culture-keyed data, not code".

**Concrete mechanics.**

- **Culture record shape** (`common/culture/cultures/*.txt`): a culture
  block carries its PILLARS by reference — `heritage`, `language`,
  `martial_custom`, `ethos` — plus `traditions` (a list), the
  `male_names` / `female_names` pools, and `dynasty_names`. Pillars are
  themselves records in `common/culture/pillars/` — the composite
  `heritage` pillar bundles `initial_number_of_pops`-style numeric
  payloads and cross-references languages; the point for us is the
  LAYERING: one culture = a few named pillar references + lists of
  domain tokens. Nothing computed, everything declared — the shape
  D-116 (12) re-gated to phase 6 as "cultures/religions/burgs … pack
  richness over mode G" and phases.md §6 sketches as the province's
  two estranged cultures (two profiles, two vocabularies, two
  prohibition sets).
- **The name pools**: flat curated lists of name KEYS per culture —
  `male_names = { Stephen Alfred Wulf... }`. A generated child draws
  from the culture's list (weighted by the parents' names where the
  game models inheritance — CK3 biases toward the father's family
  names for legitimate children); the lists are hand-authored content
  at Paradox, NOT generated — CK3 has no phonotactic generator (the
  syllable-component assembly is the Azgaar half of the donor pair;
  see `docs/ref/azgaar_names.md`).
- **Numbered variants (the regnal grammar)**: a name-key entry may
  declare regnal suffix bases — the wiki's example shape
  `John_2_John`-family entries where the engine, on crowning a holder
  whose name collides with a previous notable holder of the same
  title, renders the ordinal ("Stephen II"). The colliding count is
  per-TITLE state, not global: many living Stephens coexist; only
  titled holders earn numerals. Global uniqueness is NOT a law — the
  map is full of duplicate first names, disambiguated by dynasty and
  title in prose.
- **The key↔localization split**: `male_names` entries are KEYS, not
  display strings — the display form (and its per-language variants)
  lives in the localization files keyed by the name key. The same key
  can render `Stephen` / `Esteban` / `Étienne` per language. This is
  the exact shape of our id↔`name` split (an entity's id is opaque and
  stable; the display name is data on the record — and, since name-1,
  canon born by an event when generated).
- **Dynasty names**: a separate pool (`dynasty_names`), also
  culture-scoped; a dynasty's name renders into character epithets
  ("of Stichting" forms) — the first-name pool and the dynasty pool
  are two different vocabularies over the same culture key. Our group
  records carry their own authored `name` (a display string, "the
  watch") beside the member ids — the same two-vocabulary shape at
  group scale, one authored one generated.
- **The name-pool CONSUMERS** (the reachability question): births
  (children), generated courtiers, the ruler designer. A name list
  nothing consumes is dead data the game would still load — CK3 has no
  lint refusing it; OUR reachability law (a `generated_name`
  declaration must ride a condensing group — `core/pack.py::_names`)
  is the deliberate hardening.

**What we take.** The culture-keyed POOL SHAPE — one name vocabulary
per culture, the culture id the pack's own vocabulary (the `rules.json
::names.profiles` map key; the profile IS the culture's tongue, D-116
(12) "culture-keyed n-gram pools"). The key↔display split — ids stay
opaque, names are data. The dead-data hardening CK3 lacks — our
reachability lint.

**What we adapt.** The POOL FORM: CK3's flat curated lists work for a
hand-authored historical map (they ship ~hundreds of names per
culture); our consumers are GENERATED populations (depth-7's
condensation materializing the unborn) — a flat list exhausts, the
phonotactic component pools (Azgaar's half) compose. A future curated
pool (a pack wanting fixed casts per culture) returns as pack data
beside the profiles, never a second engine mechanism (L13). The regnal
numbering: refused for now — it is TITLE-scoped state (a counter per
title over history), which our engine has no surface for; if a future
pack wants "the second Aldric", it is a pack-side rename event through
the `name` prop door, never engine arithmetic.

**What inspires us.** Names are the cheapest estrangement surface
available (the Morrowind lesson in phases.md §6: naming IS worldbuilding)
— CK3 spends its content budget there first, before any mechanic.

**Strengths.** The layering (culture = pillar references + token
lists) scales to hundreds of cultures without engine changes — pure
data growth; the localization split keeps saves stable across
language changes; the regnal grammar is a complete, minimal solution
to name collision among notables.

**Weaknesses.** Flat lists don't compose: a generated population
drains the pool into repeats (CK3's own courtiers repeat names within
a generation — the disambiguation burden lands on the reader); no
dead-data lint (pools nothing consumes load silently); the numbered
variants are title-coupled engine state — not liftable without the
title system.

**Verdict.** The DATA-SHAPE donor of name-1: the culture-keyed pool
map + the key↔display split are lifted verbatim as shapes; the flat
list form is exchanged for Azgaar's component pools because our
consumer is a generator; the pillar layering is the phase-6 pack-richness
backbone the province sketch rides. Pattern-only intake (the game is
proprietary); no vanilla names, no vanilla culture ids.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
