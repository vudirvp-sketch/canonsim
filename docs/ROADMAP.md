# ROADMAP.md — Phases, Tracks, Gates

## 1. Two tracks

- **Track A (main):** the simulator, no LLM. All phase-0 iterations (`iter-N`).
  This is the critical path.
- **Track B (background):** LLM-circuit spikes on foreign canon (Dwarf Fortress
  Legends XML) — cheap evening work. Tasks `bg-N`. Never blocks track A.

Either track can be dropped without losing the other. The fork that resolves
the "LLM too early / too late" conflict: **early integration is dangerous** (a
narrator masks simulator holes with pretty prose), but **early development is
not** — the briefer, validator, and renderer are exercised on foreign canon in
parallel with building our own; they switch to our canon only after the
phase-0 gate.

## 2. Phase table

| Phase | Build | Exit criteria | Kill-criteria |
|---|---|---|---|
| **0. Sim without LLM** (TavernSim — this repo, now) | one dense slice: time, position, relations, knowledge, states, fire, watch, director; event log; template chronicle | chronicle reads as a story; full test suite `MVP_SCOPE.md` §16 | mechanisms not expressive, ontology has no combinatorial depth → rethink ontology, not "add LLM" |
| 1. Narrator | mode A over the log; validator; reverse prose validation | 0 canon violations per 100 beats (regression set) | ≥1 breach per 1000 beats in live play |
| 2. Parser | mode C; disambiguation questions / buttons on uncertainty | ≥90% valid intents | else redo the grammar |
| 3. Director | stagnation detector, complication buffer, arcs | a scene without an event < N beats | else redo the drama model |
| 4. Knowledge & scene | `known_by` filter, mode B, scene manager, retrieval + legends (F) | 0 leaks on the blind-NPC suite | else bug in retrieval/filter |
| 5. Depth | lazy worldgen, factions with goals, long history | an emergent chain of 3+ events without the player | else weak faction model |
| 6. Packs & worldbuilder | pack system, mode G, pack CI | a new T1 reskin without core edits, ≤1 day | else the module contract is wrong |

Phase-0 exit/kill details: `docs/MVP_SCOPE.md` §16. Each phase must be
playable at its exit — the roadmap never crosses a gate with a dead build.

## 3. Phase-0 protected non-goals

No big world / worldgen / lazy depth / faction goals; no LLM in the product; no
free-text input; no UI and no frontend integration; no pack system; no magic /
economy / combat; no external code donors before their phase. Full list:
`docs/MVP_SCOPE.md` §2.

## 4. Sources & donors (what we take, and when)

| Source | Access | What we take | When |
|---|---|---|---|
| DF Legends XML | data | a ready canonical event log: `historical_events`, `event_collections` (war → battle → episode), figures, entities, relations | background, week 1 |
| DF mechanics | closed | worldgen lesson: history ticks abstractly (populations + notables) — direct confirmation of the LOD principle | pattern |
| RimWorld / Kenshi | closed | XML-defs "content = data"; the storyteller anti-pattern; "world not player-centered" | pattern |
| Tabletop (GURPS / FATE) | — | "universal mechanics + setting books" = core/pack | pattern |
| C:DDA (CC-BY-SA) | code + data | the reference for content-as-JSON; field/fire/smoke mechanics | phase 3 |
| BrogueCE (AGPL) | code | level generation, if dungeons ever arrive | late phases |
| KeeperRL (GPL-2.0) | code | creature micro-simulation with needs | as needed |
| Azgaar FMG (MIT) | code | the most valuable code donor: states, cultures, religions, a chronology generator (JS → Python port is trivial); "a small DF worldgen", readable in an evening | phase 5 |
| AI Town (MIT) | code | negative reference for runtime LLM agents | pattern |
| Park et al. 2023 + "1000 People" 2024 | papers | the cost benchmark: why runtime LLM agents are not our path | reference |
| Endless Sky (GPL-3.0) | data + pattern | mission language: events, factions, world state | phase 3 |
| Paradox event scripting (CK3/EU4/Stellaris wikis) | closed | event grammar: trigger, weight, mean-time-to-happen, effect, option | phase 3 |
| Neighborly (MIT) | code | agent-based settlement sim for emergent narrative — closest existing cousin; architecture reading | phase 5 |

**License stance** (`docs/DECISIONS.md` D-015): no monetization planned; the
license filter is lifted — open bases are read and adapted freely, including
functional re-invention. The filter that remains is practical usefulness and
phase. The C++ roguelike frameworks (C:DDA, KeeperRL, Brogue) are content and
render machines, not the "seed → tick → event → log" cycle we need — their
value is specific algorithms in specific phases. **Phase 0 needs zero external
 code.** The only irreplaceable external resource is DF data.

**Full catalog:** `docs/REFERENCES.md` — every source from the owner's 2026-08
survey, curated and verified (licenses checked 2026-08-25), tagged
[D]/[P]/[C] and phase-gated; unverifiable survey items are logged there
(§11). This table stays the active shortlist: a source graduates into it
when its phase arrives, not before.

## 5. Gate review protocol

A gate is passed only on evidence:

1. Run the committed playscripts (identical seeds).
2. Compute log metrics M1/M2 (`docs/MVP_SCOPE.md` §15).
3. Director-off A/B run (T8).
4. Human chronicle read (T7).
5. Verdict recorded in `worklog.md` + `STATUS.md`. A kill-criteria hit stops
   feature work until the ontology is fixed.

## 6. Soul-of-Waifu horizon

End state: a simulation mode inside Soul-of-Waifu (`docs/VISION.md` §10).
Prerequisites: the mediator protocol specs (BRIEF_SPEC and friends —
`docs/SPECS_BACKLOG.md`) and the "dumb terminal" frontend contract (the
frontend renders; the mediator owns the context window). No SoW-specific work
before the phase-1 gate — any of it now is scope creep.
