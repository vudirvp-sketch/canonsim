# REFERENCES_DEEP.md — Index & Format Template for Per-Reference Deep Dives

> Companion to `docs/REFERENCES.md` (catalog) and
> `docs/CORE_DESIGN_RESEARCH.md` §2 (one-line synthesis). Where the
> catalog says "Mesa — Python ABM framework", the per-ref files in
> `docs/ref/` say **what Mesa actually does, mechanically, and what we
> take / adapt / reject / inspire from**.
>
> This file is the **index** + the **format template** + the **iteration
> plan**. The concrete deep dives live in `docs/ref/<source>.md` — one
> file per source (D-026). The single-file arrangement (D-024) did not
> scale: at iter-0j the file was 737 lines and ref-3..ref-11 would push
> it to ~3000. Per-ref files keep each source under the 600 cap
> (AGENTS §6) by construction — no substance exceptions needed.
>
> Anti-drift (AGENTS §3, `AGENT_NAVIGATION.md` §3): the catalog stays
> the source for **license / URL / phase gating / intake rules** — never
> restated in `docs/ref/`. `CORE_DESIGN_RESEARCH.md` §2 stays the source
> for the one-line **depth primitive + failure mode** synthesis — never
> restated in `docs/ref/`. Per-ref files are the **concrete mechanics**
> layer: named systems, real data structures, pseudo-code where it earns
> its keep, honest strengths and weaknesses, a per-source verdict.
> Review quarterly alongside the `doc-2` license re-verification.
>
> Phase law (`ROADMAP.md` §4, `MVP_SCOPE.md` §2) still owns when a source
> is *consulted*. Reading design notes early is allowed; vendoring early
> is scope creep. Nothing here lifts the phase-0 zero-external-code gate
> (D-012, D-015, D-022).

## 0. Format (every per-ref file follows this template)

```
# <source> · <catalog §> · <license> · <phase/track>

> Per-reference deep dive. Format template: this file §0. Iteration
> plan: this file §1. Anti-drift (D-026): catalog/license/URL/phase
> gating in `docs/REFERENCES.md`; one-line synthesis in
> `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics here. License
> filter and "patterns not content" rule: `REFERENCES.md` §0.7 (D-015).

**What it is.** One sentence: what the project IS, mechanically.
**Concrete mechanics.** Named systems, real data structures, a snippet
  where it earns its keep. Not a feature list — the parts that matter.
**What we take.** Specific, named — a class, a pattern, an algorithm.
**What we adapt.** Specific, named — and *how* we change it.
**What inspires us.** The design lesson (one clause, not a paragraph).
**Strengths.** Concrete virtues we cannot get cheaper elsewhere.
**Weaknesses.** Concrete defects — `CORE_DESIGN_RESEARCH.md` §2
  one-liners expanded here.
**Verdict.** One line: what role this source plays in our work.

[body]

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
```

If an entry would not fill every field honestly, the source is too thin
for a deep dive — leave it in the catalog only.

## 1. Iteration plan (which references get a solo iter, which batch)

A reference is **huge** (solo iter) if it has ≥3 distinct subsystems each
worth deep coverage, or if a real reading pass takes a full evening. A
reference is **batchable** (2–3 per iter) if its lessons fit one focused
session. This plan lives in `docs/TASKS.md` (infra backlog, `ref-N`); the
size verdict is recorded here so a future agent picks items in order
without re-judging.

| ID | References | Solo / Batch | Rationale |
|---|---|---|---|
| iter-0h | Neighborly + Mesa + DF Legends XML (export schema only) | 3-batch | framework setup + the three cousins already half-documented in `CORE_DESIGN_RESEARCH.md` §2 |
| ref-1 | DF worldgen + history layer (the half not covered in iter-0h) | solo | 5+ subsystems: history ticks, populations vs notables LOD, age/civ dynamics, artifact anchors, reputation as event |
| ref-2 | C:DDA `data/json/` schema | solo | the reference for content-as-JSON at scale — items, monsters, recipes, missions, factions; CC-BY-SA lets us lift |
| ref-3 | Paradox event scripting (CK3 + EU4 + Stellaris) | solo | three wikis, complex grammar (trigger / weight / mtth / effect / option / scope); phase-3 design backbone |
| ref-4 | RimWorld + L4D Director + Alien: Isolation | 3-batch | pacing/storyteller trio; all closed; design-notes only; phase-3 director ref |
| ref-5 | Wesnoth WML + Endless Sky mission DSL + ink + tracery | 4-batch | event/narrative grammar family; same conceptual shape |
| ref-6 | Brogue + DCSS + KeeperRL | 3-batch | roguelike emergence + micro-sim; environmental sim from few rules |
| ref-7 | Stanford Generative Agents + ai-town + letta | 3-batch | LLM-agent precedents — mostly negative; bg-4 cost notes overlap |
| ref-8 | Azgaar FMG + Natural Earth + GeoNames | 3-batch | worldgen data donors; phase-5 |
| ref-9 | libtcod + rot.js + Red Blob Games | 3-batch | FOV / pathfinding / grid math — pattern only (D-012) |
| ref-10 | entt + Bevy + EventStore | 3-batch | ECS scheduling + event-sourcing stream/projection patterns |
| ref-11 | SQLite FTS5 + DuckDB + sqlite-vec | 3-batch | storage layer candidates; depends on phase-4 retrieval decision |

A "batch" iteration produces one file per source — the batching is a
scheduling concept (which sources to read in the same evening), not a
file-grouping rule. A solo iteration produces one file. Either way the
scope is 2 files touched (one new `docs/ref/<source>.md` + this index
to flip status), well within the 3–5 soft limit (AGENTS §2.3).

## 2. Index of per-ref files

| ID | Source | File | License | Phase / Track | One-line verdict | Status |
|---|---|---|---|---|---|---|
| iter-0h-a | Neighborly | `docs/ref/neighborly.md` | MIT | phase 5 (cousin); iter-3 (P2a pattern source) | pair-keyed relationship map shape; P2a precedent | done |
| iter-0h-b | Mesa | `docs/ref/mesa.md` | Apache-2.0 | phase 0 (architectural pattern) | Python ABM reference; single-RNG discipline; amnesia anti-pattern | done |
| iter-0h-c | DF Legends XML | `docs/ref/df_legends_xml.md` | proprietary (export only) | bg-1..bg-4 (track B) | event-id + tick schema; `event_collections`; reputation-as-event | done |
| ref-1 | DF worldgen + history layer | `docs/ref/df_worldgen.md` | proprietary (read exported data only) | bg-1..bg-4 (track B); phase 5 LOD | history ticks abstractly; populations vs notables LOD ladder | done |
| ref-2 | C:DDA `data/json/` schema | `docs/ref/cdda_data_json.md` | CC-BY-SA 3.0 | phase 3 (content-pack reference) | content-as-JSON at scale; per-category file split; pair-keyed `relations` | done |
| ref-3 | Paradox event scripting | `docs/ref/paradox_scripting.md` | (closed wikis) | phase 3 (event grammar) | trigger / weight / mtth / effect / option / scope backbone | done |
| ref-4-a | RimWorld | `docs/ref/rimworld.md` | closed | phase 3 (director ref) | Defs taxonomy + IncidentDef field shape + storyteller trio (D-005 anti-pattern named) | done |
| ref-4-b | L4D Director | `docs/ref/l4d_director.md` | closed | phase 3 (director ref) | intensity ratchet + peak/rest clock + multi-channel family | done |
| ref-4-c | Alien: Isolation | `docs/ref/alien_isolation.md` | closed | phase 3 (director ref) | two-AI split (actor vs director) + pressure-scalar cap-and-floor + encounter-window floor + three-axis anxiety (perceived/actual/unknown) | done |
| ref-5-a | Wesnoth WML | `docs/ref/wesnoth_wml.md` | GPL-2.0+ | phase 3 (event grammar family) | `[event]`/`[filter]`/action triad + `first_time_only`/`id`/`delayed_variable_substitution` orthogonal fields + Lua escape-valve precedent (`cli/`/`brief/` split) | done |
| ref-5-b | Endless Sky mission DSL | `docs/ref/endless_sky_dsl.md` | GPL-3.0 code; mixed assets | phase 3 (event grammar family) | mission lifecycle (offer/accept/complete/fail/defer) + flat `effect` mini-language + `phrase` one-symbol grammar + `event` block as background-event precedent for `seeded_hooks` + `npc` `personality` flags | done |
| ref-5-c | ink | `docs/ref/ink.md` | MIT | phase 3 (event grammar family) | knot/stitch/divert/gather graph shape (`Brief` sketch inherits) + `LIST` multivalued flags (`entity.state` inherits) + `+`/`*` choice persistence (`Intent.accept_policy` inherits) + `#` tags (`Brief.metadata` inherits); explicitly negative on default non-determinism (INV-2 fix) + snapshot-only state (INV-1 fix) | done |
| ref-5-d | tracery | `docs/ref/tracery.md` | Apache-2.0 | phase 3 (event grammar family) | JSON grammar shape (`templates.json` inherits) + save/restore stack (`render/` `stack[pop]` inherits) + modifier pattern (`templates.json` modifiers inherit) + 200-line runtime scale (proves useful procedural text = small algorithm, not framework); explicitly negative on default unseeded RNG (INV-2 fix) | done |
| ref-6-a | Brogue | `docs/ref/brogue.md` | AGPL | phase 5 (roguelike emergence) | emergent depth from few rules; fog-of-war model | todo |
| ref-6-b | DCSS | `docs/ref/dcss.md` | GPL | phase 5 (roguelike emergence) | tile-based combat;god-themed systems | todo |
| ref-6-c | KeeperRL | `docs/ref/keeperrl.md` | GPL | phase 5 (roguelike emergence) | micro-sim — dwarf-fortress-style world in a roguelike shell | todo |
| ref-7-a | Stanford Generative Agents | `docs/ref/generative_agents.md` | (paper) | bg-4 (cost notes) | mostly negative precedent; cost notes overlap | todo |
| ref-7-b | ai-town | `docs/ref/ai_town.md` | MIT | bg-4 (cost notes) | multi-agent sandbox on generative agents | todo |
| ref-7-c | letta | `docs/ref/letta.md` | Apache-2.0 | bg-4 (cost notes) | memory architecture for LLM agents | todo |
| ref-8-a | Azgaar FMG | `docs/ref/azgaar_fmg.md` | MIT | phase 5 (worldgen donors) | fantasy map generator — biomes, rivers, names | todo |
| ref-8-b | Natural Earth | `docs/ref/natural_earth.md` | public domain | phase 5 (worldgen donors) | real-world vector + raster geo data | todo |
| ref-8-c | GeoNames | `docs/ref/geonames.md` | CC-BY | phase 5 (worldgen donors) | toponym database at scale | todo |
| ref-9-a | libtcod | `docs/ref/libtcod.md` | BSD | phase 5 (grid math, pattern only) | FOV + pathfinding reference (D-012 — pattern only) | todo |
| ref-9-b | rot.js | `docs/ref/rot_js.md` | BSD | phase 5 (grid math, pattern only) | browser-side roguelike toolkit | todo |
| ref-9-c | Red Blob Games | `docs/ref/red_blob_games.md` | CC-BY | phase 5 (grid math, pattern only) | algorithm write-ups — hex grids, A*, FOV | todo |
| ref-10-a | entt | `docs/ref/entt.md` | MIT | phase 5 (ECS patterns) | C++ ECS reference; sparse-set storage | todo |
| ref-10-b | Bevy | `docs/ref/bevy.md` | MIT / Apache-2.0 | phase 5 (ECS patterns) | Rust ECS + scheduler; event-sourced internals | todo |
| ref-10-c | EventStore | `docs/ref/eventstore.md` | MIT | phase 5 (event-sourcing) | stream/projection patterns — T2 reference | todo |
| ref-11-a | SQLite FTS5 | `docs/ref/sqlite_fts5.md` | public domain | phase 4 (retrieval candidates) | full-text search in stdlib SQLite | todo |
| ref-11-b | DuckDB | `docs/ref/duckdb.md` | MIT | phase 4 (retrieval candidates) | analytical SQL — read-only archive queries | todo |
| ref-11-c | sqlite-vec | `docs/ref/sqlite_vec.md` | MIT | phase 4 (retrieval candidates) | vector search in stdlib SQLite | todo |

Status flips to `done` when the per-ref file exists and passes
`pytest -q` + `ruff check .` clean (no test depends on the deep-dive
files; the gate is just that the iteration closes cleanly).

When a future ref-N iteration adds new files to `docs/ref/`, **append to
this table in the same iteration** — same-edit rule, AGENTS §3.
