# REFERENCES.md — External Source Catalog

> Full catalog of external sources: games, libraries, data, engines, papers.
> Policy owner: `docs/ROADMAP.md` §4 (what we take, and when) — that table is
> the active shortlist; this file is the long list. Curated from the owner's
> source survey (3 blocks, 2026-08-25) and verified against live sources in
> two passes (web search, then GitHub search API by exact name + raw LICENSE
> probes after an owner correction; 2026-08-25). Updated from the owner's
> revised functional survey (rev v2, same date): layer/priority map in §14;
> rev-v2 additions carry license "verify" — the check is deferred to phase-4
> intake (D-017). Rot by design: licenses, URLs
> and project health age — re-verify at intake; review quarterly together with
> `docs/TECH_NOTES.md`.
>
> Tags: **[D]** data donor · **[P]** pattern / design reference ·
> **[C]** code donor. Our runtime is Python stdlib-only (D-012), so almost all
> code sources are [P]; [C] means a port is cheaper than reimplementation.
> License column: SPDX id where confirmed 2026-08-25; "verify" = not confirmed;
> "none" = repo carries no license file (all rights reserved — reference only).
> Nothing here changes phase-0 law: **phase 0 uses zero external code.**

## 0. Intake rules (run before copying anything)

1. One project can carry **several licenses**: code, data and assets differ
   (SS14: MIT code / CC-BY-SA assets; ToME: GPL engine / non-redistributable
   assets; Endless Sky: GPL code / mixed assets). Read the LICENSE files,
   not the README headline.
2. Copyleft (GPL / AGPL / CC-BY-SA): reading as a pattern is always fine;
   copying makes our file share the license. D-015 (no monetization) lifts
   the license *filter*, not the *obligation* to comply.
3. CC-BY (SRDs, game-icons, GeoNames): attribution required — keep a CREDITS
   sidecar in any pack that uses them.
4. CC0 / public domain / MIT / BSD / Apache-2.0 / Zlib: copy freely.
5. Proprietary (§10): design reference only — no code, no assets, no 1:1
   rewrites from decompilation or leaks, commercial or not.
6. Phase gate: a source is *consulted* when its phase arrives (`ROADMAP §4`).
   Reading design notes early is allowed; vendoring early is scope creep.
7. **Owner's standing policy (rev v2):** sources are inspiration and pattern
   references, never 1:1 copies — everything that ships in this repo is an
   own, improved interpretation. For open code this is rules 1–4 plus a
   rewrite; for proprietary §10 sources it means public docs and talks only:
   take the idea, never the expression.

## 1. Ready data donors [D]

| Source | License (2026-08-25) | Take | Phase |
|---|---|---|---|
| C:DDA `data/json/` | CC-BY-SA 3.0 (code + data) | content ontology: items, monsters, recipes, missions, factions | 3 |
| DCSS `dat/`, vaults | GPL-2.0+ | monster/item descriptions, vault grammar | pattern |
| Angband `lib/gamedata/` | GPL-2.0 or legacy Angband licence | ego / artifact / monster tables, depth structure | pattern |
| T-Engine / ToME `data/` | engine GPL-3.0; **assets not redistributable** | Lua zone / quest / talent layout | pattern |
| Endless Sky `data/` | code GPL-3.0; assets mixed (some CC-BY-2.0) | mission DSL, factions, world state | 3+ pattern |
| Wesnoth WML `data/` | GPL-2.0+ | event → condition → effect grammar | 3+ pattern |
| Open5e API | data: SRD 5.1 CC-BY-4.0 + third-party OGL; site license custom — verify | REST JSON: monsters, spells, items | 6 |
| D&D SRD 5.1 / 5.2 | CC-BY-4.0 | monsters, spells, conditions | 6 |
| Fate Core SRD | CC-BY 3.0 (Evil Hat) | aspects / consequences / stunts as narrative states | pattern |
| Dungeon World SRD | CC-BY 3.0 | moves, tags | pattern |
| DF Legends XML | proprietary game; export from own install (DF Classic + DFHack) | ready canonical event log | bg-1 |
| RimWorld modding wiki + mods | proprietary game; mod licenses vary | Defs taxonomy, IncidentDefs, storyteller anti-pattern | pattern only |
| Paradox wikis (CK3 / EU4 / Stellaris) | proprietary; wikis are documentation | event grammar: trigger / weight / mtth / effect / option / scope | pattern, 3 |
| Wikidata | CC0 | fact graph: names, professions, mythological figures | 5–6 |
| Project Gutenberg | public domain (US) | myths, sagas, chronicles, bestiaries — name / legend raw material | 6 |
| Natural Earth | public domain | regions, rivers, coastlines | 5 |
| GeoNames | CC-BY 4.0 (terms apply) | toponyms, settlement hierarchies | 5 |
| Kenney / game-icons.net / OpenGameArt | CC0 / CC-BY 3.0 / mixed | icons and tiles — only if a UI ever needs them | optional |

## 2. Open games & mechanic donors [P]

| Source | License | Study for |
|---|---|---|
| Cataclysm-DDA | CC-BY-SA 3.0 | needs, recipes, factions, missions; content-as-JSON (`ROADMAP §4`) |
| Cataclysm: Bright Nights | CC-BY-SA 3.0 (C:DDA heritage; repo carries several license files) | same corpus, alternative balance; JSON schema evolution |
| DCSS | GPL-2.0+ | dungeon generation, turn scheduling, deterministic RNG discipline |
| NetHack (+ Slash'EM / UnNetHack / SporkHack) | NGPL (variants vary — verify) | item × item interactions, special levels, artifact quirks |
| Brogue / BrogueCE | AGPL-3.0 (CE) | environmental sim: fire, gas, water, light — emergence from few rules |
| Angband / PosChengband | GPL-2.0 or Angband licence / variant licence | ego items, uniques, town + depth structure |
| Tales of Maj'Eyal (T-Engine 4) | engine GPL-3.0; assets ToME-only | Lua add-ons, talents, zone generation |
| KeeperRL | GPL-2.0 | creature micro-simulation + base + world map (`ROADMAP §4`) |
| Pixel Dungeon / Shattered PD | GPL-3.0 | compact readable core: levels, buffs, traps |
| OpenXcom | GPL-3.0 | data-driven tactical rules; UFOpaedia as structured codex |
| Endless Sky / Naev | GPL-3.0 (Naev with exceptions — verify) | missions, factions, economy, world state |
| Freeciv / FreeOrion | GPL-2.0+ (FreeOrion content CC-BY-SA 3.0) | macro layer: cities, tech, diplomacy; galaxy generation |
| Wesnoth | GPL-2.0+ | WML event system, campaigns, unit traits |
| Simutrans / OpenTTD | Artistic-1.0 / GPL-2.0 | economy chains, deterministic transport simulation |
| OpenRA | GPL-3.0 | actor / trait data-driven rules, modding |
| Space Station 14 | MIT (code) / CC-BY-SA 3.0 (most assets) | emergent chemistry, atmosphere, role systems |
| SS13 codebases: tgstation / Baystation12 / Paradise | AGPL-3.0 (family norm — verify per repo) | round structure, antagonists, event chaos |
| DFHack | Zlib (+ some MIT / BSD parts) | DF structures, `exportlegends` (bg-1) |
| LambdaHack | BSD-3-Clause | engine-as-library discipline, strict determinism (Haskell) |
| GearHead 1 / 2 | LGPL | Hewitt's story-fragment random generation — early dynamic-plot precedent |
| Neighborly (ShiJbey/neighborly) | MIT | agent-based settlement simulation for emergent-narrative research — closest cousin |
| Mesa | Apache-2.0 | Python ABM framework: model / scheduler patterns — same language as our core |
| Azgaar Fantasy-Map-Generator (Azgaar/Fantasy-Map-Generator) | MIT | states, cultures, religions, chronology generator (`ROADMAP §4`, phase 5) |

## 3. Algorithm & engine libraries [P/C]

> Reading and porting references only — the runtime is stdlib (D-012).

| Library | License | Notes |
|---|---|---|
| libtcod | BSD-3-Clause | the classic: FOV, pathfinding, RNG, noise |
| rot.js | BSD-3-Clause | JS toolkit: scheduler, FOV, map generators — well-documented algorithms |
| GoRogue | MIT | C#: maps, FOV, pathfinding |
| SadConsole | MIT | C# console engine |
| RogueSharp | MIT | C#: dungeons, paths, FOV |
| tcod-ecs (HexDecimal/python-tcod-ecs) | MIT | Python sparse-set ECS; basis of the official python-tcod tutorial. Starter: Rakaneth/python-tcod-template-2024 (no license — reference) |
| PathFinding.js | MIT | A* / BFS / Dijkstra reference implementations |
| delaunator | MIT | Delaunay triangulation for region / world graphs |
| FastNoiseLite | MIT | Perlin / Simplex / cellular for terrain and climate |
| pcg-cpp | Apache-2.0 / MIT | PCG RNG family |
| xoshiro generators (prng.di.unimi.it) | site code — verify | xoshiro / xoroshiro |
| WaveFunctionCollapse (mxgmn) | MIT | constraint-based generation |

## 4. Narrative engines & grammars [P]

> Design references for `INTENT_SCHEMA.md` (phase 2) and event skins.
> None becomes a runtime dependency.

| Engine | License | Use |
|---|---|---|
| YarnSpinner | MIT | node / condition / variable dialogue grammar |
| ink | MIT | branching narrative, choices, flags |
| Twine | GPL (tool; story formats vary) | prototyping scene graphs |
| Inform 7 | mixed (Artistic 2.0 core — verify) | world-model / action / rule formalism |
| tracery | Apache-2.0 | grammar-based text generation: names, rumors, chronicle skins |

## 5. LLM infrastructure (track B / phase 1+)

| Tool | License | Use |
|---|---|---|
| llama.cpp | MIT | local inference, GBNF grammars, quantization — mode C backbone (`TECH_NOTES §1`) |
| Outlines | Apache-2.0 | structured generation, guaranteed JSON |
| guidance | MIT | templated constrained generation |
| vLLM | Apache-2.0 | fast serving if the circuit outgrows llama.cpp |
| Ollama | MIT | convenience runtime; weaker grammars than llama.cpp / Outlines |
| letta (ex-MemGPT) | Apache-2.0 | long-term-memory patterns (phase 4 design notes) |
| generative_agents (joonspk-research) | Apache-2.0 | memory / reflection / planning patterns + cost benchmark (`ROADMAP §4`) |
| ai-town | MIT | negative reference: runtime LLM agents (`ROADMAP §4`) |
| JSON Schema spec | — | contract language for Intent / Event / Brief |
| pydantic / zod | MIT | validation patterns — port ideas, not deps (D-012) |
| nomic-embed-text (nomic-ai) | verify | light CPU embedder for static-lore vectors (phase 4; §14) |
| bge-m3 (BAAI) | verify | multilingual CPU-friendly embedder — alternative to nomic-embed-text (phase 4; §14) |
| cross-encoder rerankers (e.g. bge-reranker-v2-m3) | verify | re-rank top-k static-lore candidates (optional, phase 4+; §14) |

## 6. Storage & event sourcing [P]

| Source | License | Use |
|---|---|---|
| SQLite (+FTS5) | public domain | canon index (D-003); FTS5 keyword search over facts/lore — the zero-dependency search layer (rev v2) |
| DuckDB | MIT | analytics over the log, chronicle rebuilds (rev v2: offline "chronicler" compression) |
| EventStore (EventStoreDB) | BSD-3-Clause (≤23.x); ESLv2 from 24.10 — pattern only | event-sourcing patterns: streams, projections |
| AxonFramework | Apache-2.0 | CQRS / event-sourcing architecture patterns |
| qdrant | Apache-2.0 | static-lore RAG vectors (phase 4) — demoted by rev v2: only where server infra already exists; local-first default = lancedb / sqlite-vec |
| lancedb | Apache-2.0 | lightweight local vector store (phase 4) |
| sqlite-vec (asg017) | verify | vector search inside SQLite for static-lore RAG (phase 4; §14) |

## 7. ECS references [P]

| Source | License | Use |
|---|---|---|
| entt | MIT | C++ ECS — component / system design |
| Bevy | MIT / Apache-2.0 | Rust ECS scheduling model |
| donburi (yohamta0/donburi-ecs) | MIT | Go ECS |
| ecs-faq (SanderMertens) | none (reading) | ECS concepts: relations, tags |

## 8. Knowledge bases & course material

| Site | What |
|---|---|
| Red Blob Games (redblobgames.com) | hex / grid math, A*, FOV, polygon maps — the algorithms course |
| RogueBasin (roguebasin.com) | the roguelike knowledge base: FOV, dungeon gen, turn systems |
| PCG Wiki (pcg.wikidot.com) | procedural generation patterns: maps, quests, names |
| Game Programming Patterns (gameprogrammingpatterns.com) | Event Queue, Component, Command, State — core vocabulary |
| Gaffer on Games (gafferongames.com) | determinism, state replication, serialization |
| r/roguelikedev + roguelikedev.reddit FAQ | community architecture discussions |

## 9. LLM × game precedents (related work)

| Project | License | Note |
|---|---|---|
| AI Dungeon | proprietary | negative case: canonless drift (`VISION §9`) |
| SillyTavern | AGPL-3.0 | UX reference for cards / lorebooks; our frontend is a dumb terminal — take ideas, not code |
| dpasca/roguellm | none — reference only | experimental LLM-enhanced roguelike prototype |
| aceangel3k/rogue-isek-ai | none — reference only | LLM-generated-everything dungeon crawler experiment |
| tegridydev/dnd-llm-game | IDCDW (permissive) | local DM model + small rules/state-extraction model — mode C kin |
| ctavolazzi/AI-DnD | MIT | autonomous AI-driven D&D campaign simulator |
| kngwyu/rogue-gym | Apache-2.0 / MIT | roguelike with APIs for training AI agents |
| mcp-tool-shop-org/ai-rpg-engine | MIT | TS toolkit for deterministic RPG simulation (state, events, RNG) — architectural kin |
| RusianHu/Labyrinthia-AI | MIT | roguelike fully driven by an LLM (D&D-flavored, Chinese README) — the "LLM does everything" pole |
| MillennialJesus/ReputeX-Engine | none — reference only | modular AI-driven reputation + language engine for dynamic storytelling scenarios |
| CorruptTigga/Echo | custom — reference only | text-driven Viking-era open-world life simulation (JS) — LLM-narrated life-sim kin |
| vudirvp-sketch/universe-audit-protocol-webapp (owner's own) | README says MIT; **no LICENSE file** (checked 2026-08-27 — reference only until fixed) | LLM world-concept audit (5-block pipeline, countable-criteria rubric): take = criteria-as-thresholds discipline, 7-hole taxonomy, prompt shapes + free-tier resilience for phase-1 harness; negative = LLM-as-judge scoring, regex-over-markdown bridge. Deep dive: `docs/ref/uap_audit.md` (ref-12) |
| vudirvp-sketch/live-char-guide (owner's own) | MIT (LICENSE file verified 2026-08-27) | Character-card methodology for RP with 12B–32B+ models (SPINE causal chain → Trigger→Action→Price anchors → voice isolation → SP assembly → 15 anti-patterns → countable diagnostics): take = Price/observability discipline as pack-lint vocabulary + phase-1 brief injection grammar; negative = prompt-compensation machinery, false-memory/fatigue-emulation canon breaks. Deep dive: `docs/ref/live_char_guide.md` (ref-13) |

## 10. Proprietary design references [P] — never copy

| Source | Study |
|---|---|
| Dwarf Fortress | worldgen / Legends: procedural history, event collections, epistemology schema |
| RimWorld | XML-defs content-as-data; IncidentDefs; storyteller = named anti-pattern (D-005) |
| Kenshi | faction simulation without plot; region-based hostile world |
| Left 4 Dead AI Director (GDC talks) | pacing: tension curve, peaks and rests |
| Alien: Isolation (GDC talks) | dual-AI director: pressure, hunt, adaptation |
| Paradox event scripting (CK3 / EU4 / Stellaris wikis) | event grammar: trigger, weight, mean-time-to-happen, effect, option |

## 11. Unverified / misattributed (anti-hallucination log)

> Checked 2026-08-25 in two passes: (1) web search — misses small fresh repos;
> (2) after an owner correction, GitHub search API by exact name + raw
> LICENSE probes. Lesson baked into D-016: **query GitHub search by exact
> name first** — SEO search alone produced false negatives (Labyrinthia-AI,
> ReputeX-Engine and Echo were wrongly dropped in pass 1; restored in §9).

| Survey item | Verdict |
|---|---|
| StrobeServer (Kenshi AI backend) | not found — GitHub search returns 0 repos of this name; nearest kin: Kenshi agent-environment scaffolds |
| "Story-Engine" | no canonical repo — name collides with hundreds of projects; none matches the survey description |
| Astray as a "Lua maze library" | misattributed — wwwtyro/Astray is a JS/Three.js WebGL maze demo (Unlicense); not Lua, not a library |

Verified to exist but small / hobby-scale (kept out of the main tables):
Osnowa (azsdaja/Osnowa, MIT), indiv0/colonize (GPL-3.0), mcgillij/pyDF (no
license — reference only), Edgar-Unity (MIT core + paid PRO),
Rakaneth/python-tcod-template-2024 (no license — tcod + tcod-ecs starter),
nidomika/procedural-generation-algorithm (BSP-based, Python, no license),
tomasforsman/RACEngine (C#, no description or license — ECS claim
unconfirmed), GearHead story-fragment notes (§2). Value is precedent, not
donor code.

## 12. GitHub search topics

`roguelike` · `procedural-generation` · `dungeon-generation` ·
`world-generation` · `event-sourcing` · `ecs` · `interactive-fiction` ·
`story-generation`

## 13. Starter stack per phase (from the survey, mapped to our roadmap)

| Phase | Consult |
|---|---|
| 0 (now) | zero external code (law). Reading: Game Programming Patterns, Gaffer on Games, RogueBasin |
| bg track | DF Legends XML (own install + DFHack); llama.cpp + Outlines / guidance + JSON Schema |
| 3 (director / events) | C:DDA JSON + fire mechanics; Endless Sky / Wesnoth / Paradox event grammars; RimWorld + L4D + Alien as pacing references |
| 4 (knowledge / scene) | letta memory patterns; lancedb / sqlite-vec + light embedders (nomic-embed-text / bge-m3) for static-lore RAG (qdrant only with existing server infra) |
| 5 (depth / worldgen) | Azgaar FMG; Natural Earth + GeoNames; Freeciv / FreeOrion macro patterns; Mesa ABM patterns |
| 6 (packs) | SRD 5.1 + Open5e + Gutenberg + Wikidata; tracery for skins; Fate / Dungeon World for narrative mechanics vocabulary |

## 14. Functional map & owner priorities (survey rev v2, 2026-08-25)

> The owner's layer-by-layer view: which sources close which architectural
> layer, at what priority. **Priority ≠ intake time**: Must/Should/Could is
> importance to the final concept; the Phase column above (and `ROADMAP §4`)
> stays the operative filter — phase 0 remains zero-external-code (D-012,
> D-015). Under D-012 the "Must" runtime tools (Pydantic/Zod, rot.js, libtcod,
> FTS5, vector stores) enter as patterns, ports or stdlib features, not as
> dependencies, until a decision says otherwise. Phase mapping: rev v2's
> phases 0–5 = ROADMAP 0–4 + 6 (rev v2 has no depth phase; ROADMAP unchanged,
> D-017).

| Layer (rev v2) | Must | Should | Could | Catalog |
|---|---|---|---|---|
| Canon, events, storage, contracts | SQLite (+FTS5), JSON Schema, Pydantic/Zod patterns, event sourcing | Game Programming Patterns | DuckDB | §5, §6, §8 |
| Simulation donors | C:DDA | SS14, DCSS, KeeperRL | Shattered PD | §1, §2 |
| Worldgen & determinism | PCG; rot.js or libtcod (one) | FastNoiseLite, Red Blob, RogueBasin | WFC, Delaunator | §3, §8 |
| Event grammar, skins, pacing | RimWorld pacing (curves, buffers — through the D-005 lens) | L4D Director, Paradox scripting, Ink, Tracery | Wesnoth WML | §10, §1, §4 |
| Memory, epistemology, legends | DF Legends | Stanford Generative Agents, Paradox intrigue | — | §1, §10, §5 |
| Content & setting packs | C:DDA `data/json` | Open5e, FATE / DW SRDs | Wikidata, Gutenberg, Natural Earth + GeoNames | §1 |
| LLM circuit | llama.cpp, constrained decoding (GBNF / Outlines / guidance / JSON Schema), local 12–27B models | LanceDB / sqlite-vec, light embedders (nomic-embed-text / bge-m3) | cross-encoder reranker | §5, §6, `TECH_NOTES §1` |
| QA & regression | golden tests, blind-NPC suite, seed regression | pack CI, latency/repeat metrics | — | internal: `MVP_SCOPE.md` §14, `SPECS_BACKLOG.md` |

Notes:

- The QA row is internal practice, not external sources — T0–T8 already own
  it; latency/repeat metrics (p50/p95, repeats, stagnation, refusals) join the
  phase-1 mode-A harness (`TECH_NOTES.md` §6).
- Rev v2's exclusions (NetHack family, ToME, OpenXcom / Endless Sky / Naev /
  Freeciv / FreeOrion / OpenTTD / Simutrans, SS13 codebases, GoRogue /
  SadConsole / RogueSharp / PathFinding.js, extra RNG families, Twine / Yarn /
  Inform 7, EventStore / Axon as dependencies, Qdrant-as-default, art assets,
  MemGPT/Letta & ai-town as a canon layer) match the catalog's existing phase
  and [P] gating. Rationale: no unique function, or duplicates a
  better-fitted source (the D-015 filter). Nothing is deleted from the
  catalog; demotions are recorded, not removed.

## 15. Principle donors (absorbed, not intake)

Owner-provided architecture texts consulted as principle references — no
code, no data, no license question (the owner's own materials), so the §0
intake rules do not apply. The influence is recorded where the law lives;
these rows are the catalog anchor:

| Text | Absorbed into | Status |
|---|---|---|
| INVARIANT-CORE v3 (manifesto) | D-031; L13 (`docs/BLUEPRINT.md` §2); type-discipline + fitness-test clauses (`docs/blueprint/phase0.md` §1) | absorbed 2026-08-27 |
| Elegant Solutions (curated exemplars) | D-031; L14 (`docs/BLUEPRINT.md` §2); log-as-stream idioms (`docs/TECH_NOTES.md` §7) | absorbed 2026-08-27 |
