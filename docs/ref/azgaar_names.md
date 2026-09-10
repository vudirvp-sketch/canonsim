# Azgaar Fantasy-Map-Generator — the name pools · `REFERENCES.md` §1/§10 · MIT · phase 5 (name-1; the generator half of the ref-19 pair)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1 (ref-19-b). Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md` §10;
> one-line synthesis in the catalog row ("states, cultures, religions,
> chronology generator"); concrete mechanics here. The MAP-GENERATOR
> half (pipeline, `State`/`Campaign` interfaces, the editors-as-
> controlled-mutations law) already lives in `docs/ref/azgaar_fmg.md`
> — this file covers the names generator alone (`nameBases`, the
> syllable assembly, the collision question). License: MIT — shapes
> AND content liftable; we lift shapes only (INV-3: the pools are pack
> data; our pools are authored fresh, never donor bytes — the
> `tongue_a` test profile and the province's two tongues).

**What it is.** The procedural name layer of F-M-G: per-culture
NAMEBASES — arrays of syllable-component pools plus syllable-count
bounds — from which burgs, states, rivers and cultures draw display
names at generation time; the shipped example of "a name is assembled
from phonotactic parts, per culture, from the seed".

**Concrete mechanics.**

- **The nameBase record** (the `nameBases` data array; one entry per
  real-world language the tool ships — the "English" base, the
  "Nordic" base, …): `name` (the display label), `min` / `max` (the
  syllable-count bounds), and `b` — THE POOLS: an array of arrays of
  string fragments, per position class: the consonant/onset pool, the
  vowel/nucleus pool, the ending components (and the doubled-forms
  list the assembly may reach into — the exact pool count differs by
  base vintage; the SHAPE is positional component pools). Fragments
  include the EMPTY STRING — an empty onset yields vowel-initial
  names, an empty coda yields open syllables. This is the
  `onsets` / `nuclei` / `codas` / `syllables` vocabulary of our
  profile record, verbatim as a shape (`core/names.py::PROFILE_KEYS`).
- **The assembly** (`getBaseName`-family in the generator): draw the
  syllable count in `[min, max]`; per syllable draw one fragment from
  each positional pool; join; capitalize the first letter. Pure
  function of (the RNG state, the base) — the same draw sequence
  reproduces the same name, which is why a re-generate with the same
  seed redraws the same map labels. Our `_assemble` is this function
  with the draws routed through the RngBank (INV-2: F-M-G's single
  seeded `Math.random` chain is the pre-D-028 form — the multi-stream
  discipline is ours).
- **Culture→base binding**: cultures are drawn as cells over the map
  (the states pass family, `azgaar_fmg.md`'s pipeline); each culture
  cell references a nameBase; every burg/state label then draws from
  the LOCAL culture's base — geography decides the tongue, the tongue
  decides the name. The province sketch (phases.md §6) rides this
  exact composition: the river artery's lowland traders vs the hill
  folk, two profiles, the map's cultures bound to them.
- **Collision handling**: the base generator does NOT hold a global
  name-uniqueness law — duplicate labels can occur (user edits and
  province re-rolls re-run the assembly freely); disambiguation is
  left to the reader of the map. Our entity-namespace collision walk
  (`WALK_MAX` bounded redraw, then the loud refusal) is the deliberate
  hardening: our names are CANON (an id↔display mapping the render
  trusts), not decoration — a colliding name would corrupt the
  mapping, so the walk is the law's single owner.
- **The regenerate path**: the options dialog re-runs the names layer
  over the committed map — the same controlled-mutation law the
  `azgaar_fmg.md` dive records for the whole editor family. OUR twin
  is first-commit-wins: a born name is canon and never redraws
  (INV-5); only the unborn re-materialize. The regenerate-over-committed
  form is exactly what the lazy-materialization door refuses.

**What we take.** The nameBase SHAPE — positional component pools
(with the empty fragment) + syllable-count bounds — as the profile
record; the assembly order (count first, then per-syllable components,
pool-index draws, capitalize at the surface) as `_assemble`.

**What we adapt.** The RNG discipline — F-M-G's draws hang off the one
global seeded chain; ours ride the per-npc content-addressed
`name:<npc>` stream (the D-079 family law: an added declaration shifts
neither a canon check nor another npc's name — F-M-G's single chain
would couple every name to every draw, the measured-and-refused
alternative D-079 records for urgencies). The collision law —
bounded redraw + loud refusal against the entity namespace, where
F-M-G tolerates duplicates. The materialization point — F-M-G names
everything at map-build time; our names are LAZY (the unborn stay
counts; the condensation births the name with the membership — the
phases.md §6 "inn's strangers ARE the condensation" shape).

**What inspires us.** A name generator is a few small pools and one
loop — the estrangement-per-byte ratio is the highest in the whole
donor set; Azgaar ships a continent of distinct-feeling labels off
arrays of 5–15 fragments.

**Strengths.** Compositional space from tiny data (hundreds of names
per base); per-culture flavor from pool DIFFERENCES alone (no
mechanics); deterministic under a fixed seed; MIT — liftable whole.

**Weaknesses.** The single RNG chain couples every generated name to
the draw order (re-tuning any earlier generator shifts every later
label — the coupling our per-stream split exists to kill); no
collision law; no dead-base lint (an unused nameBase loads silently —
our reachability law hardens this too); the pools are code-adjacent
data in the generator source rather than declarative pack content
(ours live in `rules.json::names`, linted).

**Verdict.** The GENERATOR donor of name-1: the nameBase shape and the
assembly loop are lifted as shapes; the determinism is re-foundationed
on the RngBank (INV-2), the collision walk and the lazy
materialization are our hardening over the donor's tolerances. The
culture→base binding composes with the world-2 cultures row at the
phase-6 opening (the province's two tongues over the generated map).

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
