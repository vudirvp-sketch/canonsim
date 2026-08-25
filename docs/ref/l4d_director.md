# Left 4 Dead AI Director · `REFERENCES.md` §10 + §14 · proprietary (GDC talks + dev commentary only) · phase 3 (director ref)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015). Source is proprietary — public GDC talks, in-game
> developer commentary nodes, press interviews only. No code, no
> assets, no 1:1 rewrites (`REFERENCES.md` §0.5).

**What it is.** The pacing system for Valve's Left 4 Dead (2008,
directed by Mike Booth). The "AI Director" name is misleading: it is
**not a single AI**, but a **set of policies** over a procedural spawn
queue. The core insight (Booth's GDC 2009 talk "Left 4 Dead 2: A
Detailed Post-Mortem" + the 2008 Valve developer commentary nodes
embedded in-game) is that **player perception of pacing is a curve,
not a series of events**; the Director's job is to keep that curve in
the engagement band by ratcheting threats up during calm and forcing
rests during peaks. Closed source; the talk and the commentary nodes
are the public surface — design-notes only.

**Concrete mechanics.**

- **Three directors, not one.** Per Booth's post-mortem the AI
  Director is actually a small family of subsystems with separate
  responsibilities:
  - the **Horde Director** (the "spawn queue + intensity ratchet"
    people mean when they say "the AI Director") — runs continuously
    during an active map, decides zombie population per beat;
  - the **Special Infected Director** — picks one of the S.I.
    archetypes (`Hunter`, `Smoker`, `Boomer`, `Tank`, `Witch`) to
    deploy based on player geometry and on the recent-fire history;
  - the **Music / Cues Director** — the audio layer that telegraphs
    boss spawns and "calm" beats; the player hears the Director
    more than they see it.
  Our `P2e` narrative entropy (`SPECS_BACKLOG.md` DIRECTOR_SPEC)
  inherits this **multi-channel** lesson: a single "director" code
  path with multiple sub-policies, each responsible for one pacing
  dimension — not one god function. The phase-0 director in our
  `MVP_SCOPE.md` §5 is the Horde Director analogue; the other two
  channels wait for phase 3.
- **Intensity ratchet.** The scalar named in the GDC talk. A number
  per player that:
  - **increases** when zombies are visible or audible near the player
    (a haptic/audio perception check — Director is aware of what
    the **player** perceives, not what is in the world);
  - **decays** when the player is safe, idle, or moving between
    encounters;
  - **caps at a maximum** (`PeakThreshold`) above which the Director
    is forbidden from spawning new common zombies.
  Booth's exact phrasing in the post-mortem Q&A: "the Director is
  measuring a player's stress, not the world's population." The
  public field-shape: a per-player float, a per-tick delta, a
  cap, a floor. We rename — `narrative_entropy` (`P2e`) is the
  direct analogue; the visible-state inputs are the same idea
  (suspicion, fire, watch).
- **Peak / rest rhythm.** The Director forces a **peak** when
  intensity exceeds `PeakThreshold` for `PeakDuration` (≈ 10–30s);
  after a peak, it enforces a **rest** for `RestMinDuration`
  (≈ 20–45s) during which intensity is forcibly decayed by suppressing
  spawns. The pattern: a **two-state pacing clock** — `Peak` vs
  `Rest` — with min durations on both. Our `DIRECTOR_SPEC` sketch
  adopts the same shape (`DIRECTOR_SPEC` sketch in
  `SPECS_BACKLOG.md`): the director's state machine has `RAMP`,
  `PEAK`, `REST`, `STAGNATION`; the transitions are gated by
  `MinRampDuration` / `MinRestDuration` floors exactly like L4D's.
- **Spawn budget, not spawn count.** A scalar `MaxPopulation` per
  side per moment (≈ 30 common infected on a normal-difficulty map
  per the post-mortem; modulated by difficulty and player count).
  The Director spawns **up to** `MaxPopulation - current_alive`;
  it does **not** spawn at fixed times. The implication for us:
  our seeded-hook director (`P2e` release-the-lowest-threshold
  hook) operates on the **same budget** logic — when N hooks
  can fire, the queue is `sorted()` by `(threshold, tick, hook_id)`
  and only the lowest is released; the budget is 1 per beat. The
  L4D analogue is exact.
- **Boss placement on the peak.** `Tank` and `Witch` spawns are
  **boss beats** that the Director places at the end of a peak,
  not at the start. The pattern: **a beat has a shape** — a peak
  has a beginning (intensity threshold reached), middle (max
  population, S.I. cycle), end (boss beat + reset). Our `MVP_SCOPE.md`
  §5 director + `DIRECTOR_SPEC` sketch — currently `RAMP`/`PEAK`/
  `REST`/`STAGNATION` only — should add a `PEAK_CLIMAX` state
  when a `seeded_hook` of high severity fires; that's a phase-3
  refinement, not phase 0.
- **The `S.I.` cycle.** Special Infected spawn slots are limited
  (usually 1-2 at a time per team, depending on game mode). The
  S.I. Director picks the archetype based on player geometry —
  `Hunter` for line-of-sight gaps, `Smoker` for runners, `Boomer`
  for clustered survivors, `Tank` at peak climax. The decision
  is **rule-driven** (a `if`-`elif` over perception queries), not
  a learned policy. Per the post-mortem: "no neural network;
  just a series of weighted heuristics". For us: the seeded-hook
  selection in `rules.json` (`MVP_SCOPE.md` §8) is the same
  shape — `seeded_hook_weights: Dict[str, float]` and a
  weighted-random draw from visible state. **No learning,
  no LLM** — exactly the L4D precedent.
- **"Time since last peak" + "Time since last rest" timers.** The
  director holds two scalars: a `TimeSincePeak` and a `TimeSinceRest`,
  and the transitions in the pacing clock are gated by **both**
  (a peak can fire only if `TimeSinceRest > MinRestDuration`; a
  rest can fire only if `TimeSincePeak > MinPeakDuration`). The
  two-clock shape is the most portable L4D lesson for our
  `DIRECTOR_SPEC`: two cooldown timers, not one.
- **Player-cardinal survival bias.** A separate sub-system: if
  all four players are bleeding out, the spawn rate of health
  packs in the next safe-room is boosted — a **redistributive
  luck mechanic** that pulls a near-wipe back from the edge.
  Public on the developer commentary nodes; the rule is "keep
  one player alive across the wipe". This is **inverse of D-005**:
  rather than inventing a new threat, the Director **softens the
  existing threat** when the team is critical. Our `P2e` does
  not have this (we promise irreversibility per `VISION.md` §6);
  we name it as a **negative reference** — the limit case of a
  director that **changes canon to serve pacing**. Our director
  changes pacing to serve canon, the opposite direction.
- **L4D2 additions (post-mortem additions).** The sequel adds:
  - the **`Uncommon Common`** family — variant zombies that
    change spawn weights in campaign-specific maps;
  - the **`Fade to Black`** respawn mechanic — down-but-not-out
    players see only black until revived (changes the perception
    channel, not the simulation);
  - **three-intensity tank spawn rule** — `Tank` cannot spawn
    until `PeakThreshold` × 3 sustained for `MinPeakDuration × 3`,
    a stricter threshold on top of the regular peak rule.
  The pattern: **thresholds are layered**, not flat — a `Boss`
  threshold gates a `Peak` threshold gates a `Calm` threshold.
  Our `DIRECTOR_SPEC` sketch has one `entropy_threshold`; the L4D2
  precedent suggests layered thresholds as a phase-3 refinement.

**What we take.**

- **The intensity ratchet shape.** Per-player scalar, per-tick
  delta, cap, floor — exactly the `narrative_entropy` (`P2e`)
  proposal. The Director measures **perceived state** (zombies
  visible/audible), not **actual state** (zombies spawned); our
  entropy measures **visible state** (suspicion, fire spread,
  watch roster), not **hidden state** (knowledge records, NPC
  intents) — the alignment is direct.
- **Peak / rest two-state clock.** Our `DIRECTOR_SPEC` sketch
  in `SPECS_BACKLOG.md` uses the `RAMP` / `PEAK` / `REST` /
  `STAGNATION` shape; the L4D precedent is the explicit source.
  Both floors (`MinRampDuration`, `MinRestDuration`) come from
  L4D's `PeakDuration` / `RestMinDuration` fields.
- **Spawn budget = 1 per beat** (per seeded-hook release). The
  Director releases the **lowest-threshold** seeded hook from
  the queue when entropy drops — exactly the L4D Horde Director's
  "spawn up to budget" pattern with budget set to 1. The order
  is `sorted()` by `(threshold, tick, hook_id)` — INV-2's
  deterministic iteration law.
- **Two-clock cooldowns (`TimeSincePeak`, `TimeSinceRest`).**
  Our director's state machine in `DIRECTOR_SPEC` has a single
  `time_in_state` per state; the L4D precedent suggests a
  phase-3 refinement: separate cooldowns per state transition,
  not one universal timer.

**What we adapt.**

- **Three directors → multi-channel director with one core.**
  Our phase-0 director is the Horde Director analogue (threat
  queue + intensity ratchet). The S.I. Director and Music
  Director are phase-3 channels; the L4D precedent says **don't
  build a single god function** — separate `DirectorPolicy`
  subclasses per channel, each feeding the same entropy
  ratchet. We do this with `seeded_hook_weights` per channel
  in `rules.json`, not in code — INV-3 split, L4D pattern.
- **`MaxPopulation` budget → `MaxConcurrentSeededHooks`.** L4D
  caps at ~30 per side; we cap at **1 per beat** (phase 0),
  with a `MaxConcurrentSeededHooks` setting in `rules.json`
  reserved for phase-3 escalation. The shape is the same;
  the magnitude is far smaller (one tavern, not a four-player
  map).
- **Player-cardinal survival bias → explicitly forbidden.** Our
  `VISION.md` §6 promises irreversibility; the L4D soft-can-on-
  wipe mechanic is a **named negative reference** in `STATUS.md`
  FAQ if a future agent proposes "boost guard suspicion when
  player is about to lose." The L4D precedent supports the case
  against, not for.
- **`Boss` threshold layered on `Peak` threshold → phase-3
  layered thresholds in `DIRECTOR_SPEC`.** Phase-0 director has
  one threshold per state (`entropy_threshold`, `stagnation_
  threshold`); phase-3 may add a `Boss` threshold per
  high-severity seeded-hook family, gated on top of `Peak`.

**What inspires us.** The **measure the player's stress, not the
world's population** lesson. L4D's Director is the canonical proof
that **a pacing algorithm driven by perceived-state inputs beats
a spawn timer** — every zombie game since has copied the shape
because it works. Our `P2e` narrative entropy is the design heir:
the director releases a hook when **visible** entropy drops, not
when an invisible counter ticks. The Director is **epistemic** in
a precise sense: it paces against the player's perception, not the
sim's actuality. Our chronicle is the same shape — the LLM briefer
will write what NPCs perceive, not what the simulation did; the
Director paces against the same perceived state.

**Strengths.**

- The GDC 2009 post-mortem by Booth is **the most cited pacing
  algorithm talk in game AI history** — the field "AI Director"
  is named after it. The pattern is the gold standard; the
  field is named after this single talk.
- Public: the talk + the in-game commentary nodes are explicit
  about field names (`PeakThreshold`, `RestMinDuration`,
  `MaxPopulation`, `TimeSincePeak`) — patterns not content per
  §0.7 (D-015).
- The **multi-channel lesson** (Horde vs S.I. vs Music) is the
  portable pattern our `DirectorPolicy` interface inherits; the
  single-god-function anti-pattern is what we refuse.

**Weaknesses.**

- **Player-perception queries are L4D-specific.** L4D's intensity
  ratchet checks "can the player hear/see the zombie"; our
  phase-0 sim has no perception channel yet — we measure
  visible-state (`suspicion`, `fire`, `watch`) which is a proxy
  for "perceived threat", not a perception query itself. The
  adaptation is lossy; the L4D precedent is the inspiration, not
  a portable implementation.
- **Closed source.** The exact spawn-geometry heuristics (where
  in the map does the S.I. spawn?) are inferred from play, not
  documented. We don't need them — our tavern is one scene — but
  the precedent is **shallow**: the GDC talk covers the pacing
  shape, not the placement.
- **Player-cardinal survival bias** — D-005 violation if naively
  ported. We name it as a negative reference, not a strength.
- **The "AI Director" name is misleading.** It's a heuristic
  policy family, not a learning agent. The field is rife with
  myth-making; the actual algorithm is simple. Our adaptation
  must be explicit: **no ML, no learned policy**, just as
  `VISION.md` §6 promises.

**Verdict.** Phase-3 director reference, almost entirely positive
on the pacing shape (intensity ratchet, peak/rest clock, spawn
budget, multi-channel family), explicitly negative on the
soft-can-on-wipe mechanic (irreversibility). The GDC talk is the
single most important pacing-algorithm reference in game AI; our
`DIRECTOR_SPEC` sketch and `P2e` proposal are direct inheritors
of the L4D shape. Closed-source placement heuristics are out of
bounds; the field-shape from the post-mortem is in bounds.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
