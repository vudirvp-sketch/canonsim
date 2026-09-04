# LEGEND_SPEC.md — Reflection, Compaction & Legends Contract (phase 4)

> Written just-in-time at the leg-3 row (the D-022 law — never ahead of
> the consumer). Owner of the **compression half** of the LEGEND_SPEC
> sketch: reflection & memory compaction, reflection provenance, the
> `stale` flag. The **trait half** landed earlier as leg-1 (iter-55,
> `core/traits.py` + D-084) — linked, never restated here. The runtime
> owner is `core/reflection.py`; the pack contract is
> `rules.json::reflection` (lint `core/pack.py::_reflection`); the
> reaction-cascade position is `core/loop.py::_react` (after leverage,
> before the director seeding). Architecture row: `phases.md` §4.

## 1. Scope

| Surface | Owner | Status |
|---|---|---|
| The reflection mint (recurrence → event) | `core/reflection.py::reflection_drafts` | live (leg-3, iter-57) |
| The pack block + lint | `rules.json::reflection` + `core/pack.py::_reflection` | live; ARMED (leg-3b, iter-58) |
| Reflection provenance (`list[event_id]`) | the event's `outcome.provenance` | live (leg-3) |
| The `stale` flag (read side) | `core/reflection.py::stale_reflections` | live (leg-3); consumers: retr-1, leg-4 |
| The expansion law (demand side) | `core/reflection.py::expand_reflection` | live (leg-3) |
| Trait crystallization (P3f) | `core/traits.py` + D-084 + BRIEF_SPEC §3.5 | landed (leg-1/leg-2) |
| The retrieval ladder (ranking, `α·recency + …`) | `retr-1` (TASKS row) | not this spec's code |
| Offline scavenge (tombstones, DuckDB) | `leg-4` (TASKS row), D-012 | not this spec's code |
| Legends collections (DF structure) | `docs/TAXONOMY.md` (bg-2) | not this spec's code |

## 2. The compaction law

**Reflection-on-recurrence** (the Generative Agents donor): when a
knower's held records of a declared token family reach the block's
`threshold`, the memory compacts — the knower mints a **reflection
event**, a higher-level entry that is itself a log entry. The
originals are **never dropped and never edited** (INV-1/INV-5): the
append-only log stays the only truth, and letta's
`summarize_messages_in_place` is the named anti-pattern this design
refuses — compaction is always an append, never a rewrite.

Recurrence means **repeats**: the count of the knower's held records
whose `knows` is in the insight's `family` (acquisition order). This
is the echo's renewal made **known**, where the echo makes it felt;
breadth (DISTINCT tokens) stays the traits' business — one mechanism
per axis, never two (the echo/traits/reflection split: felt /
believed / concluded).

The mint fires at the Nth record's own event, inside the reaction
cascade (`loop._react`), committed through the canon door
(`_commit` — state-free by construction). ONE reflection per
(knower, insight) per **run**: the minted insight token is held
knowledge from its mint on, and records are never dropped, so the
`view.holds` gate blocks forever — the **never-re-reflect law**. A
third recurrence only grows the expansion's evidence.

Laws that follow from the shape:

- **No RNG anywhere** (INV-2): reflection is an inference, not a
  stochastic act — the telling rolls acceptance, the reflection does
  not. Deterministic in event order + declaration order.
- **No hooks, no state changes** (L6): the director buffer never
  seeds from a reflection, suspicion never moves — entropy reads
  observable state only (DIRECTOR_SPEC §4), and a knowledge-derived
  entry is not observable state. The cascade terminates by
  construction (the leverage one-hop law's sibling).
- **The knower gate**: kind `npc` only — an ambient group holds
  records but does not draw conclusions in v0.1 (the leverage knower
  law).
- **The told-conclusion law**: the minted insight record is ordinary
  knowledge — tellable onward (the telling reaction's own fidelity
  decay), salient in the fold like any record. A knower who HEARD a
  conclusion holds it as knowledge and never re-derives it (the
  never-re-learn law's own semantics; the hearsay knower's honest
  state).

## 3. The reflection event

The pack declares the event type (`reflection.event`) — pack data, no
schema bump (EVENT_SCHEMA §11: a new type or outcome payload is pack
vocabulary; the type must render in the chronicle, the secrets law).

| Field | Value | Law |
|---|---|---|
| `type` | `reflection.event` | renders (templates own the line) |
| `actor` | the reflector | the knower, an npc |
| `target` | `null` | a reflection has no direct object |
| `cause` | the triggering event | chained by the loop |
| `outcome.about` | the insight token | the pack's declared insight |
| `outcome.provenance` | `list[event_id]` | §4 below |
| `outcome.recurrence` | int | the evidence count at mint |
| `knowledge` | one record | `channel: inferred`, `fidelity: exact`, `knows: <insight>` |
| `hooks` / `state_changes` | empty | L6 + termination by construction |

The channel is `inferred` (P2d's channel — an inference from one's
own memory, not a perception). The fidelity is `exact`: the
reflection faithfully states what the knower **holds**; the
underlying evidence's quality rides the provenance, not this record.
The record's `source` is the reflection event's own id (stamped by
the writer, L3 derive-never-store). Importance comes from the pack
rule (`pack_importance`, the reflector as the touched entity); the
pack may list the type in `importance.story_critical_events` to raise
it — the rule, not this spec, owns the signal.

## 4. The provenance law

Every reflection carries `outcome.provenance: list[event_id]` — the
ids of the source events that minted the contributing records,
deduped first-seen in acquisition order. The list is the
**demand handle** for every consumer (the brief's belief lines carry
the same shape, BRIEF_SPEC §3.5):

- **The source is always queryable; the reflection is a derived
  view, never a replacement.** `expand_reflection` reads the family
  records back from the knowledge view — every record the reflector
  holds (the mint-time subset is `provenance`; the live fold is the
  expansion; evidence is evidence, the `expand_trait` twin).
- **On contradiction, the source outranks the reflection's
  recency** (phases.md §4). This is a retrieval-time ranking law:
  it lands with **retr-1** (the deterministic re-ranker), recorded
  here as the contract the ladder must honor — the runtime salience
  rank (`importance, then recency`) does not compare claims and must
  not be patched to.

## 5. The stale law

A reflection whose provenance no longer resolves is **stale** and is
excluded from retrieval. `stale_reflections(pack, events)` is the
read-side screening: the ids of reflection events whose
`outcome.provenance` ids do not all resolve within the given event
universe.

In the **runtime log** the fold is empty by construction: originals
are never dropped (INV-1), so every minted provenance id resolves.
The flag earns its keep only in **derived stores after offline
scavenge** (leg-4's tombstones — the log itself is never edited,
INV-5): a scavenged index that dropped a source record must screen
its reflections before serving them. **retr-1 must consult this fold**
— serving a stale reflection as fact is the derived-store lie this
law exists to prevent.

## 6. The pack contract (`rules.json::reflection`)

Closed key set (unknown key = load error): `event` · `threshold` ·
`reflections` · `notes`. Per-insight closed key set: `family` ·
`notes` (the traits' `family` vocabulary — the same concept, one
word).

Lint laws (all load-time, `core/pack.py::_reflection`):

1. `event` must be in the template vocabulary (EVENT_SCHEMA §11 —
   the reflection renders in the chronicle).
2. `threshold` an integer ≥ 2 — a first occurrence is an event, not
   a recurrence (the compaction floor, the traits threshold's twin).
3. Every `family` token must be **mintable** (a declared knowledge
   template mints it — a token nobody can ever learn is dead
   vocabulary).
4. **One-sided membership**: a family token feeds exactly one
   insight (a token in two families double-counts one recurrence).
5. No duplicate family entries (a duplicate double-counts).
6. **Vocabulary hygiene**: an insight token never collides with a
   mintable knowledge token (one string, two vocabularies — the
   template mint would hold it and the never-re-reflect gate would
   block the fold's own mint forever; the traits law). Corollary:
   the insight vocabulary is disjoint from every read-model
   vocabulary (echo/traits/secrets all require mintable tokens) —
   the only minting path for an insight token is the reflection
   event itself and onward transfer.

The block is **optional**: a pack without it mints no reflection
events and runs byte-identically (the pack's own declaration is the
gate, INV-3).

## 7. The arming (leg-3b, iter-58)

The committed pack carries the LIVE block: the measured recurrence
(day1_full seeds 123/128 — the PC retries the theft) mints the pack's
insight pair, one per axis of the theft's evidence —
`sneak_at_work_here` over `figure_reaching_for_purse` (the watcher's
conclusion: the targeted guard holds the sighting twice, t=9/12) and
`trouble_by_the_bar` over `noise_by_the_bar` (the room's conclusion:
the barkeep, the drunkard, and the serving maid each hold the noise
twice). `threshold` 2; the event `conclusion_drawn` renders
"{actor} had noticed it before, and named it: {knows}." and rides
`importance.story_critical_events` — a named conclusion is a tale
beat (the knowledge-flow precedent: knowledge_transfer and
rumor_told are story-critical too).

The zero-regen landing (the iter-52 precedent): 8/10 day1 seeds
byte-identical (exactly 123/128 mint — 4 events each, cause-chained
to the second `pickpocket_failed`); the narrator corpus (105 cases),
the parse corpus (10 cases), and the T1 golden fixture measured
untouched through the real mediator/parser cycles — zero re-distill.
The told-conclusion law rides LIVE through the watch-change
briefing: the briefing tells the relief guard the minted conclusion
(told/partial, one fidelity step down) with the evidence, and the
never-re-reflect gate blocks his own re-derivation — he holds
`figure_reaching_for_purse` twice from the one transfer, yet mints
nothing. The laws compose without special cases.

## 8. What this spec deliberately does not own

Legends **collections** (DF's event_collections many-to-many) stay
bg-2/TAXONOMY territory; offline **DuckDB analytics** is leg-4 (never
in the runtime import graph, D-012); the **retrieval ladder** is
retr-1 (this spec fixes only the two contract points the ladder must
honor: consult `stale_reflections`, source-outranks-reflection on
contradiction); **trait crystallization** is D-084's row and
BRIEF_SPEC §3.5's read. The brief's future reflection read (if the
phase needs one) is a BRIEF_SPEC amendment, same-commit law §8.
