# Alien: Isolation · `REFERENCES.md` §10 + §14 · proprietary (GDC talks + interviews only) · phase 3 (director ref)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015). Source is proprietary — GDC 2015 talk by Gary Napper
  + Andy Bray, Eurogamer / PC Gamer interviews, Creative Assembly
  dev-blog posts only. No code, no assets, no 1:1 rewrites
  (`REFERENCES.md` §0.5).

**What it is.** A survival-horror game (Creative Assembly, 2014) built
around a single AI antagonist — the Xenomorph — that hunts the player
across a space station. The key design decision (per the GDC 2015 talk
"The Perfect Panic" + Eurogamer's "How the AI of Alien: Isolation was
made" interview) is that **the Xenomorph is two AI systems**: a
reactive **"Xenomorph AI"** (the actor that perceives, moves, and
attacks) and a proactive **"Director AI"** (the metronome that decides
when and where the Xenomorph should be). The split is the design
lesson — the actor is not pacing itself; the director paces it from
outside. Closed source; the talk, interviews, and the post-mortem
articles are the public surface — design-notes only.

**Concrete mechanics.**

- **Two-AI architecture.** Per the GDC talk, the Xenomorph is **not
  one agent**:
  - the **Xenomorph AI** — the actor with senses (hearing, sight,
    a "trace" or recent-activity sense), a behaviour tree for
    navigation, and an attack state machine. It **does not know
    the player's position**; it perceives through sensors. The
    talk calls this a "SenseBoard" — a per-tick update of `can_hear`,
    `can_see`, `last_known_position`, `last_known_time`.
  - the **Director AI** — a separate system that decides the
    Xenomorph's **objective** for the next beat: `Investigate_
    Sound`, `Search Area`, `Stalk Player`, `Patrol Route`, `Retreat
    to Vent`. The objective is broadcast to the Xenomorph AI,
    which switches its behaviour tree accordingly.
  The Director never moves the Xenomorph; it tells the Xenomorph
  what to want. The Xenomorph never decides pacing; it acts on the
  objective. **Strict separation of concerns** — this is the
  pattern we take.
- **Pressure scalar.** The Director maintains a `Pressure` number per
  player that:
  - **rises** when the Xenomorph is near, visible, or audible to
    the player (the Director **measures the player's perception**,
    not the Xenomorph's distance — same epistemic lesson as L4D's
    intensity ratchet, `l4d_director.md` §"intensity ratchet");
  - **decays** when the player is safe, idle, or moving between
    encounters;
  - **caps at a `PressureCeiling`** above which the Director must
    switch the Xenomorph's objective to `Retreat to Vent` for a
    `RecoveryFloor` (≈ 30–60s per the talk);
  - **floors at a `PressureFloor`** below which the Director may
    switch objective to `Stalk Player` and spawn the Xenomorph
    from a vent near the player's path.
  The shape is **L4D's intensity ratchet with explicit cap-and-
  floor-driven state transitions** — the same scalar, the same
  perceived-state inputs, but with **forced behaviour changes
  when the scalar saturates**. This is the layer the L4D post-mortem
  leaves implicit; Alien: Isolation names it explicitly.
- **Encounter windows.** The Director schedules **windows** of
  `EncounterDuration` (≈ 30–90s per the talk) during which the
  Xenomorph is permitted to be near the player; outside the
  window, the Xenomorph is forced into a vent and **offscreen**.
  The schedule is **not a fixed clock** — the next window is
  scheduled based on `Pressure` and on `TimeSinceLastEncounter`,
  with a `MinGapBetweenEncounters` floor (≈ 60–90s). The pattern:
  **a beat-based director with a forced offscreen state during
  the gap** — the Xenomorph doesn't pace against the player
  continuously, only in windows. Our `DIRECTOR_SPEC` sketch in
  `SPECS_BACKLOG.md` adopts the same shape: `RAMP` /
  `PEAK` / `REST` / `STAGNATION` — the `REST` state is the
  "offscreen vent" analogue, with `MinRestDuration` floor.
- **The "spider search" pattern.** When the Xenomorph has no
  objective from the Director, it executes a **random walk
  constrained by the player's perceived position** — weighted
  toward high-heat rooms (rooms where the player has been seen
  recently), avoiding low-heat rooms. The talk describes this as
  a **biased random walk** — not a pathfinder, not a learned
  policy. The implication for us: when our director is in `REST`
  state and the player-driven entropy is low, **the world should
  be quiet, not empty** — NPCs continue their schedule (the
  maid roams, the drunkard seeks ale, the guard patrols), but no
  new seeded hooks release. The "spider search" is the schedule
  continuing; the windows are the director's interventions on
  top. `MVP_SCOPE.md` §5 director-on vs director-off maps
  exactly: on = scheduled windows + schedule; off = schedule
  only.
- **The Director "learns" the player.** Per the Eurogamer
  interview with Andy Bray: the Director maintains a
  **per-player-pattern map** — recent preferred hiding spots
  (lockers, under-desk), recent preferred distraction items
  (flare, noisemaker), recent preferred routes. The Director
  biases the Xenomorph's patrol weights and the vent-spawn
  selection to **counter** the player's recent pattern: a
  player who always hides in lockers sees the Xenomorph check
  lockers more often; a player who flares-and-runs sees vents
  spawn along the run path. **This is the most controversial
  design choice in the talk** — and the one we explicitly refuse.
  Our `VISION.md` §6 forbids the simulation from adapting to the
  player's psychology; the LLM briefer may adapt its prose to
  perceived player psychology (the `psychological_echo` proposal
  P3e in `CORE_DESIGN_RESEARCH.md` §6), but the **canon**
  (the JSONL log, the seeded hooks, the director's releases) is
  player-blind. Alien: Isolation's "Director learns the player"
  is the **named anti-pattern** for our P3e scope.
- **Three-axis anxiety.** The talk names three scalar
  dimensions the Director balances:
  - **Perceived threat** — what the player perceives right now
    (the Xenomorph visible, audio cue);
  - **Actual threat** — what the simulation has spawned (the
    Xenomorph's actual position, the actual objective);
  - **Unknown** — the player's uncertainty (no Xenomorph visible,
    no audio cue; the player does not know where the Xenomorph
    is).
  The Director explicitly schedules beats to **all three axes**,
  not just the first. A `REST` beat lowers perceived threat but
  keeps **unknown** high (the Xenomorph is in a vent; the player
  knows it's there but not where). A `STALK` beat raises both
  perceived and unknown. The three-axis model is portable to
  our `narrative_entropy` (`P2e`) — `unknown` is the gap between
  actual state (what the sim knows) and perceived state (what
  the PC knows); our `knowledge records` (`EVENT_SCHEMA.md`)
  model this gap directly. **The Director paces against the gap,
  not just the inputs** — the most portable Alien lesson.
- **Threat map.** The Director maintains a **per-room heat map**
  updated each tick by recent player presence (last seen, last
  heard, last touched). The Xenomorph's `Investigate Sound`
  and `Search Area` objectives are weighted by this heat map
  — the actor is biased toward where the player **was**, not
  where it is now. The pattern: **perception lags** — the
  director paces against history, not against real-time. Our
  `M4` novelty / `M5` non-PC event share metrics (`D-019`)
  measure the world's continuing state during the player's
  absence; the threat-map precedent supports the design.
- **"Offscreen" presence.** When the Xenomorph is in a vent,
  the simulation **continues to model its position** — it
  moves through the vent network toward a new exit point. The
  player cannot see the Xenomorph; the Xenomorph is still
  simulated. This is the existence proof that **a director
  can place actors offscreen without removing them from the
  simulation** — the world is continuous, the player's view is
  not. Our `MVP_SCOPE.md` §3 already models every NPC every
  tick; the `T8 director-off A/B` test will measure the
  emergent chains when the player is not present.
- **The "Objective" broadcast.** The Director does not move
  the Xenomorph; it broadcasts an objective. The Xenomorph's
  behaviour tree switches on the objective. The lesson for us:
  **the director emits a directive, not an action**. Our
  `seeded_hook` release in `rules.json` is a directive — a
  trigger condition that, when fired, **adds an `Intent` to
  the queue** for an NPC; the NPC's behaviour (the executor)
  decides what the action is. The Intent / Event boundary in
  our `EVENT_SCHEMA.md` §1 inherits the same split.

**What we take.**

- **Two-AI architecture: actor vs director.** Our phase-0 sim
  already separates the two: the `core/` queue + `sim/systems/*`
  is the actor layer; the director (`MVP_SCOPE.md` §5) is the
  directive layer. The Xenomorph-vs-Director precedent is
  explicit: **the director emits directives, the actor
  executes**. We have the architecture already; Alien is the
  reference that names it.
- **Pressure scalar with cap-driven state transitions.** L4D's
  intensity ratchet is the scalar; Alien adds **forced state
  transitions when the scalar saturates**. Our `DIRECTOR_SPEC`
  sketch has the same shape — `entropy_threshold` → `RAMP` →
  `PEAK` → forced `REST` after `PeakDuration`; the cap-driven
  transition is the precedent.
- **Encounter windows with `MinGapBetweenEncounters` floor.**
  Our `P2e` director releases the lowest-threshold seeded hook
  when entropy drops below threshold; the **`MinGapBetweenEncounters`
  floor is the `MinRestDuration` in our spec** — same shape,
  same lesson.
- **Three-axis anxiety — perceived / actual / unknown.** The
  **`unknown` axis is portable**: our knowledge records model
  the gap between actual state (the JSONL log) and perceived
  state (what the PC knows); the director paces against the
  gap. The L4D precedent measures perceived state only; Alien
  adds the unknown as a separate axis — this is the design
  refinement we can adopt for phase-3 director metrics.
- **Threat map = per-room heat map of recent player presence.**
  Our `M4` / `M5` metrics measure the world's continuing state
  during the player's absence; the threat-map precedent
  supports the design. The pattern: **perception lags history,
  history lags actuality** — three timescales, three axes.
- **Offscreen presence.** Our sim already models every NPC every
  tick; the precedent confirms: **the director does not remove
  actors from the simulation, only from the player's perception
  window**. The T8 director-off A/B test will measure the
  emergent chains when the player is not present.
- **Objective broadcast → Intent/Event split.** Our `EVENT_
  SCHEMA.md` §1 already separates Intent (decision) from Event
  (state-change); the Director-vs-Xenomorph precedent is
  the existence proof at production scale.

**What we adapt.**

- **Pressure scalar → `narrative_entropy` (`P2e`).** Same shape,
  same inputs (perceived-state — `suspicion`, `fire_spread`,
  `watch_roster`), same cap-driven state transitions. The
  cap-and-floor behaviour is the layer L4D leaves implicit and
  Alien names — we adopt it.
- **Encounter windows → seeded-hook release with `MinGap` floor.**
  Our director releases the lowest-threshold seeded hook when
  entropy drops below `entropy_threshold`; the `MinGapBetween_
  Encounters` floor is the `MinRestDuration` in `DIRECTOR_SPEC`.
  Same shape; the magnitude is far smaller (one tavern, one
  scene).
- **Three-axis anxiety → `entropy` measures perceived state,
  knowledge records model the unknown.** Our phase-0 director
  uses **perceived state only** (per L4D); the three-axis
  model is a **phase-3 refinement** — measure `unknown` as a
  separate scalar (gap between actual and perceived) and pace
  against it as well. Not phase 0.
- **Threat map → `M4` novelty / `M5` non-PC event share metrics
  (`D-019`).** The threat map is a per-room heat map; our
  metrics are log-derived (per `MVP_SCOPE.md` §15) — same idea,
  different time scale (we measure the world's state across the
  whole run, not per-room per-tick).
- **The "Director learns the player" pattern → explicitly
  refused.** Our `VISION.md` §6 promises the canon is player-
  blind; the LLM briefer's `psychological_echo` (P3e) may adapt
  prose to perceived player psychology, but the canon (the
  JSONL log, the seeded hooks, the director's releases) is
  not player-adapted. Alien's "Director learns the player" is
  the **named negative reference** in `STATUS.md` FAQ if a
  future agent proposes "make the director adapt to the PC's
  recent actions." The Alien precedent supports the case against.

**What inspires us.** The **strict separation of actor vs director**
lesson — the actor perceives and executes, the director paces and
emits directives, and neither knows the other's internals. Our
architecture already follows this (the Intent/Event split, the
`core/` queue vs `sim/systems/*` separation); Alien: Isolation is
the existence proof that the split scales to a single-antagonist
narrative at production quality. The second lesson is the **three-axis
anxiety model** — pacing against perceived / actual / unknown — which
L4D measures only the first of; Alien adds the unknown as a separate
axis and paces against the gap. The gap is what our `knowledge
records` already model; the director paces against the same gap.

**Strengths.**

- The GDC 2015 talk is **the most cited single-antagonist director
  talk** in game AI history — the field of "asymmetric director
  design" is named after it. The pattern is the gold standard
  for any director that paces against a single threat.
- Public: the talk, the Eurogamer interview, the PC Gamer
  post-mortem all name the field-shape (`Pressure`, `PressureCeiling`,
  `PressureFloor`, `EncounterDuration`, `MinGapBetweenEncounters`,
  the three-axis anxiety model, the threat map) — patterns not
  content per §0.7 (D-015).
- The **objective-broadcast pattern** (Director emits a directive;
  actor switches behaviour tree) is the portable lesson for our
  Intent/Event boundary; the existence proof is at production
  quality.

**Weaknesses.**

- **Closed source.** The actual SenseBoard implementation, the
  behaviour tree internals, the heat-map algorithm are inferred
  from play, not from code. The field-shape from the talk is in
  bounds; the implementation is out.
- **The "Director learns the player" mechanic** (the most
  controversial design choice) — explicit D-005 violation if
  naively ported. We name it as a negative reference, not a
  strength.
- **Single-antagonist design.** Our phase-0 sim has no single
  antagonist; the threat is diffuse (a theft, a fire, a rumor).
  The "Xenomorph director" pattern paces against one threat;
  our director paces against a sum of seeded-hook weights + global
  suspicion + visible physical threats. The shape is portable;
  the magnitude is different.
- **Three-axis anxiety is a phase-3 refinement.** Phase-0 director
  uses perceived state only (per L4D); measuring the `unknown`
  axis requires the knowledge-record machinery that lands in
  iter-3. The Alien precedent inspires the phase-3 refinement,
  not the phase-0 implementation.

**Verdict.** Phase-3 director reference, mostly positive on the
two-AI split (actor vs director, objective broadcast), the
pressure-scalar with cap-driven transitions, and the encounter-
window + MinGap floor. Explicitly negative on the "Director learns
the player" mechanic (named anti-pattern for our `VISION.md` §6
player-blind canon law). The three-axis anxiety model is a phase-3
refinement inspiration, not a phase-0 implementation. The GDC 2015
talk is the single most cited single-antagonist director reference
in game AI; our `DIRECTOR_SPEC` sketch inherits the shape.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
