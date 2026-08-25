# Neighborly · `REFERENCES.md` §2 · MIT · phase 5 (cousin); iter-3 (P2a pattern source)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015).

**What it is.** C# agent-based settlement simulation (`ShiJbey/neighborly`,
MIT) — the closest existing cousin to canonsim's phase-5 settlement
vision: NPCs with relationships, jobs, personalities, and routines that
produce emergent narrative summaries.

**Concrete mechanics.**

- ECS-shaped core: an `Entity` is an integer id; components (`Position`,
  `Relationship`, `Occupation`, `Personality`, `Mood`, `Health`) are
  struct-bags keyed by entity id; systems (`TimeSystem`, `SocialSystem`,
  `RoutineSystem`, `NarrativeLogSystem`) tick on a daily cadence.
- `RelationshipTracker` is a **pair-keyed map**:
  `Dictionary<(int, int), Relationship>` where the key is a sorted tuple
  of entity ids and the value carries axes (trust, friendship, romance,
  familiarity) plus a per-axis weight used as a tiebreaker in social
  decisions.
- The social step: a `SocialSystem` iterates entities, asks
  `RelationshipTracker` for candidates (filter by proximity +
  relationship score above threshold), picks one, and emits a
  `SocialInteraction` record (enum: greet, argue, compliment,
  small-talk, …). The interaction updates the relationship axes per
  type-specific delta tables.
- Narrative is **post-hoc**: a `NarrativeLogSystem` runs at day's end,
  reads the day's `SocialInteraction` records, writes prose summaries.
  The narrative layer is a *reader* over state, not a participant.

**What we take.**

- The **pair-keyed relationship map** shape — `Dictionary<(int, int), …>`
  with a sorted tuple as canonical key. This is exactly P2a (D-020,
  `CORE_DESIGN_RESEARCH.md` §6): "sparse pair-keyed relation map" for
  NPC↔NPC relations in iter-3. Neighborly confirms the data structure.
- The "system-per-verb" decomposition — `SocialSystem`, `RoutineSystem`
  as separate ticked scopes. Our `sim/systems/` 8-system layout
  (`MVP_SCOPE.md` §5) is the same discipline; Neighborly proves "social"
  deserves its own system, not a method on `NPC`.

**What we adapt.**

- **State-mutating tick → event-emitting tick** (INV-1). Neighborly's
  `SocialSystem` mutates `RelationshipTracker` in place during the step;
  we emit a `rumor_heard` / `relation_changed` event into the queue, the
  writer flushes it to JSONL, and an incremental projection updates
  relations. The event is the truth; the projection is a cache
  (D-023, KI#5).
- **Post-hoc narrative → recorded log + template chronicle** (iter-5).
  Neighborly writes prose summaries at day's end and stores them as
  primary artifacts; we write events during the tick and let
  `render/` assemble the chronicle from the JSONL. Replay reconstructs
  what was *reported* vs what *happened* — Neighborly cannot.
- **Relationship matrix → relations-as-derived-state.** Neighborly
  stores `RelationshipTracker` as primary state; we derive relations
  from `relation_changed` events (fold over the log, `EVENT_SCHEMA.md`
  §1). INV-1 preserved; relations are a view, not a store.

**What inspires us.** The "settlement simulates itself without a player"
posture — confirms Kenshi's lesson (`CORE_DESIGN_RESEARCH.md` §3 row 4)
that the world must run for its own sake, not for the PC. Neighborly is
the proof-of-existence that agent goals + interactions produce emergent
narrative *at all* — we don't invent the genre, we harden its epistemology.

**Strengths.**

- Readable C# codebase, MIT-licensed — pattern transfer is direct.
- Solves the pair-keyed relations problem ahead of us; the data
  structure choice is validated.
- The system-per-verb decomposition matches our 8-system layout, so the
  architectural mapping is one-to-one.

**Weaknesses.**

- Weak epistemology (`CORE_DESIGN_RESEARCH.md` §2 row "Neighborly"):
  agents act but don't accumulate structured knowledge — no `known_by`,
  no fidelity, no rumor-distortion channel. This is the gap our
  `knowledge` records (MVP_SCOPE §10, EVENT_SCHEMA §3) are designed to
  fill; Neighborly confirms it is a real gap, not our invention.
- State-mutating tick — the Mesa anti-pattern (see `mesa.md`). Replay
  requires re-running; we cannot byte-compare a Neighborly run without
  recording every RNG draw externally.
- No causal chain — `SocialInteraction` records have no `cause`; the
  "why" lives in agent code, not the log. Our `cause` (EVENT_SCHEMA §2,
  P1a) is the missing ledger.
- Narrative is post-hoc summary, not a recorded log — summaries drift;
  replay cannot detect when the narrator lied.

**Verdict.** Phase-5 settlement cousin. Iter-3 P2a lifts its pair-keyed
map shape. Its epistemology gap is the spec for our knowledge records;
its amnesia is the spec for our event log. Read the repo at iter-3.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
