# Canonsim Worldbuilding — Active Knowledge Surface

> Cleaned and consolidated from the 15-document worldbuilding archive.
> Repository-facing text is in English, while the original source archive is
> preserved separately as legacy research material.

## Purpose

This directory is the **active worldbuilding context** for Canonsim.
It is not a runtime contract, pack schema, or substitute for repository
engineering law. The engine/runtime remains authoritative for what is already
implemented; this surface owns the setting's durable world-level design.
Repository law (`AGENTS.md`) and the navigation map
(`docs/AGENT_NAVIGATION.md` §3) govern how this surface is read, cited, and
updated.

## Read order

Normal worldbuilding work:

1. `WORLD_KERNEL.md` — current world identity, hard laws, scope, and open questions.
2. The relevant domain owner — `RESONANCE.md`, `LIFE_PERSONHOOD.md`, `PEOPLES.md`, or `CULTURES_CIVILIZATION.md`.
3. `ANCHOR_REGION.md` — current human-scale integration surface and causal map.
4. `WORLD_AUTHORING.md` — authoring doctrine and quality tests.
5. `WORLD_TESTS.md` — evidence, stress tests, and unresolved test obligations.
6. `WORLD_WORKPLAN.md` — current frontier and next work.

Do **not** load the legacy source archive by default. Open it only to recover
provenance, inspect a disputed passage, or deliberately re-run old research.

## Information ownership

| Surface | Owns | Does not own |
|---|---|---|
| `WORLD_KERNEL.md` | world identity, central contradiction, hard world laws, canonical terminology, scope | detailed domain mechanics, test history |
| `RESONANCE.md` | Resonance ontology, limits, capability boundaries | culture-specific spellbooks, runtime implementation |
| `LIFE_PERSONHOOD.md` | life, death, Echo, personhood, continuity | lineage ecology, cultural institutions |
| `PEOPLES.md` | lineages, biology, lifecycle, migration, inter-lineage contact | culture as learned solution sets |
| `CULTURES_CIVILIZATION.md` | culture + civilization formation, regimes, institutions, cultural fingerprints | individual biography, Resonance physics |
| `WORLD_AUTHORING.md` | authoring method, meaning/voice doctrine, anti-collection rules | canon facts |
| `ANCHOR_REGION.md` | Sarrow Vale integration, causal map, meso frontier | world-wide canon |
| `WORLD_TESTS.md` | test definitions and evidence | new canon decisions without a test/research disposition |
| `WORLD_WORKPLAN.md` | current frontier, routing, next deliverables | historical transcript |

## Status vocabulary

- **HARD** — load-bearing working canon; removing it requires an explicit reconsideration.
- **WORKING** — active hypothesis used for authoring, not final truth.
- **MYSTERY** — deliberately unresolved; the uncertainty itself is part of the world.
- **DEFERRED** — important but intentionally not solved yet.
- **REJECTED** — tested direction not used in the current world model.
- **PROPOSAL** — a possible future direction, not current canon.

## Canon hygiene

One fact has one owner. A downstream document should point to its owner rather
than restating the whole rule. Research conclusions belong in the owner only
when they alter a future authoring decision; otherwise they remain evidence in
`WORLD_TESTS.md` or the legacy source archive.

This is intentionally a **small context surface**. The objective is not to make
worldbuilding shorter; it is to make the same depth cheaper to recover and harder
to contradict.

## Consolidation map

| Legacy document | Disposition |
|---|---|
| `CANONSIM_NEW_WORLD_KERNEL_v0.1.md` | absorbed into `WORLD_KERNEL.md` |
| `CANONSIM_NEW_WORLD_RECONCILIATION_v0.1.md` | absorbed into all owner docs; its status taxonomy is retained here |
| `CANONSIM_NEW_WORLD_WORKPLAN_v0.1.md` | absorbed into `WORLD_WORKPLAN.md` |
| `WORLD FOUNDATION v0.1*` | durable world laws → `WORLD_KERNEL.md`; stress evidence → `WORLD_TESTS.md` |
| `WORLD FOUNDATION v0.2*` | historical backbone → `WORLD_KERNEL.md`; ancient-network open questions → `WORLD_WORKPLAN.md` |
| `World Constitution v0.1` | world laws → `WORLD_KERNEL.md`; method → `WORLD_AUTHORING.md` |
| `RESONANCE v0.2` + `RESONANCE v0.3` | merged into `RESONANCE.md` |
| `LIFE & PERSONHOOD v0.1` | absorbed into `LIFE_PERSONHOOD.md` |
| `PEOPLES & ANOMALOUS BIOLOGY v0.1` | absorbed into `PEOPLES.md` |
| `CULTURE FOUNDATION v0.1` | absorbed into `CULTURES_CIVILIZATION.md` |
| `CIVILIZATION FOUNDATION v0.1` | absorbed into `CULTURES_CIVILIZATION.md`; unused catalogue detail dropped |
| `WORLD FOUNDATION v0.1t` | absorbed into `WORLD_TESTS.md` |
| `Выступление Курвица.md` | source material; useful principles absorbed into `WORLD_AUTHORING.md` |
| `теория строительства миров canonsim.md` | absorbed into `WORLD_AUTHORING.md` |

## Current repository relationship

The repository is the source of truth for **implemented** behavior. The active
worldbuilding surface is the source of truth for the **authored setting model**.
A repository implementation that predates or differs from a worldbuilding
proposal is not silently "fixed" by this directory; the difference is recorded
as open work until an explicit worldbuilding or engineering decision resolves it.

The current repository already contains an original second setting,
`content/province_pack`, whose Sarrow Vale slice is used in `ANCHOR_REGION.md`
as an implementation witness and integration laboratory. That does not mean
that every future worldbuilding claim is already implemented there.

## Terminology boundary

Two words carry different senses on each side of this surface and must not
be conflated:

- **canon** here means authored-setting canon (the status vocabulary above).
  It never means the repository's event-log canon — INV-1 in `AGENTS.md`:
  the append-only JSONL log is the truth, `core/log.py` the only canon-write
  path. Nothing in this directory is a canon-write surface.
- **Echo** here is the world-level phenomenon (`RESONANCE.md` §2,
  `LIFE_PERSONHOOD.md` §3: the structural residue of a prior process). The
  repository's `core/echo.py` is an engine read model — a per-NPC
  psychological-residue fold over that NPC's own knowledge records. The two
  concepts share a word; any mapping between the engine fold and the world
  phenomenon is an open integration question, never an established identity.
  Neither side is silently changed to match the other.
