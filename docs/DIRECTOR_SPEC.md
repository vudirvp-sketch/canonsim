# DIRECTOR_SPEC.md — Director Contract

> Trigger fired at iter-4 start (`docs/SPECS_BACKLOG.md`). Single owner
> of the director's runtime contract; the blueprint `docs/blueprint/
> phase0.md` §4 owns the donor design, `core/director.py` owns the
> mechanics. Cited by ledger rows DIR-*; this file never restates them.
> ≤300 lines. The pacing clock (DIR-1) landed iter-36 (phase 3, D-065);
> the phase-3 refinements still recorded-not-built live in §11. The
> clock's measured impact (DIR-2, iter-37: both pacing arms
> byte-identical on day1_full — the stagnation path never fires there)
> is owned by `docs/TEST_PLAN.md` §6.

## 1. What the director is

A **consequence planner** (D-005) that releases already-seeded hooks
into the world through the intent door — never an improviser. The
buffer holds hooks seeded at event time; triggers (time / place /
threshold) fire causally; the stagnation detector releases the
lowest-threshold hook when narrative entropy (P2e) drops below the
pack's floor. Director-off (T8 A/B baseline) keeps the buffer seeding
but suppresses releases — the world's emergent chains come from
urgencies + reactions + rotations, not director injections.

## 2. The buffer

| Field | Owner | Type |
|---|---|---|
| `tag` | event (the `hooks[]` entry) | `str` |
| `seeded_by_event` | commit door | event id |
| `seeded_at_tick` | commit door | `int` |
| `weight` | pack (`director.hooks[tag].weight`) | `int ≥ 0` |
| `release_threshold` | pack | `int ≥ 0` |
| `target_npc` | pack | npc id |
| `intent_kind` | pack | action name |
| `intent_target` | pack (optional) | entity id or `null` |
| `intent_fields` | pack | mapping |
| `trigger` | pack (optional) | `{kind, ...}` (see §3) |

The buffer is **per-run** (folded from the log; reseeds from the
master seed every run because the events are deterministic per seed).
The pack data (`director.hooks`, policies, stagnation parameters) is
constant across runs. Director adaptation state never persists (INV-1:
`state = fold(log)`, the log is per-run).

## 3. Triggers (causal — fire regardless of entropy)

| Kind | Fields | Fires when |
|---|---|---|
| `time` | `tick` | `beat_tick ≥ tick` |
| `place` | `target_npc`, `location` | the target's projection position == location |
| `threshold` | `target_npc`, `axis`, `comparator` (`at_least` / `at_most`), `value` | the target's `relations.<axis>` meets the comparison |

A hook with `trigger: null` is **stagnation-only** — its trigger
never fires on its own; it relies on the stagnation detector.

## 4. Narrative entropy (P2e)

```
entropy = sum(weight of unreleased hooks)
        + sum(relations.suspicion across NPCs with the axis)
        + count of burning <layer>.<spot> props across all locations
```

Observable state only (L6) — never knowledge records, never PC
internals. The Influence Boundary (EPIST-1) extends from the
perceiver to the director itself. Replaces the v0.1 draft's flat
`release_after_ticks_without_visible_event: 90` timer — a tension
floor sensor, not a boredom timer.

## 5. Release policy (the minimal pair + the pacing clock)

```python
class DirectorPolicy(Protocol):
    def permit_release(
        self, explicit_trigger_fires: bool, current_entropy: int
    ) -> bool: ...
```

- `EnabledPolicy(entropy_floor=N)`: explicit triggers always release;
  stagnation releases when `entropy < N`.
- `DisabledPolicy`: never releases (T8 A/B baseline).

**The pacing clock (DIR-1, landed iter-36; the L4D peak/rest donor):**
a per-run four-state machine `RAMP / PEAK / REST / STAGNATION` over
narrative entropy, advanced once per beat (guarded against a double
advance inside one beat). Pack data `director.pacing`
`{peak_floor, min_peak_beats, min_rest_beats}` — `peak_floor` sits
strictly above the stagnation floor (lint); a pack WITHOUT the block
runs the v0.1 minimal pair, byte-identically (the pack's own
declaration is the gate, INV-3).

- **PEAK** — entropy ≥ `peak_floor`: the world is loud; the director
  does not add. Holds `min_peak_beats` even through an entropy dip
  (the L4D `PeakDuration` anti-flap floor).
- **REST** — entered when a PEAK ends: `min_rest_beats` of post-climax
  breathing room during which the stagnation path is suppressed (the
  L4D `RestMinDuration`; the flat v0.1 detector re-injected the beat
  after a climax, flattening the arc). Broken early only by the world
  re-spiking — the director never ends its own rest with a release.
- **STAGNATION** — entropy below the stagnation floor: the only quiet
  state that releases (the policy's floor stays the release authority
  — one owner per law; RAMP is the same band above the floor).
- Explicit triggers NEVER consult the clock (D-005: causality is not
  pacing — the world's own consequences fire mid-rest).

The clock is derived state — a deterministic fold of the per-beat
entropy sequence (INV-2: same log → same clock → same releases); it
writes nothing, and `TimeSincePeak` / `TimeSinceRest` (the donor's
two-clock fields) are the state machine itself. Measured impact at
landing (iter-36): the day1_full ON log is unchanged — all three of
its beats sit in PEAK (the double-steal suspicion), and its sole
release is the explicit document-check; the committed fixtures carry
no stagnation releases, so T1/T8/corpus stay byte-identical.

## 6. Release budget + cooldown

- **1 release per beat** (the director never spams). The budget is
  consumed by a release or a rejection at the front door (the world
  noticed the attempt).
- **Per-NPC cooldown** (`director.stagnation.per_npc_cooldown_beats`,
  pack data — the `MinGapBetweenEncounters` analogue applied to
  targeting). After a release targeting NPC X, that NPC is blocked
  for N beats.
- **Dead actors never targeted**: an NPC removed from the projection
  or with `crime_status == caught` is skipped — the entropy sensor
  stops chasing ghosts.

## 7. The beat cycle

Beats are intraday tick offsets (`urgencies.beat_ticks`) repeated
daily, like watch rotations. They are NEVER pre-seeded into the
queue — a run still ends when its script's queue drains. The beat
fires three pieces in order, each through the commit door (D-037):

1. **States decay** (`core/states.py`): fatigue/intoxication/fear
   deltas proportional to elapsed ticks since the NPC's last decay
   event (or run start). Injury has `auto_decay: 0` — never decays
   (T4 holds; only a counter-event can change it).
2. **Urgencies** (`core/urgencies.py`, P2b): per-NPC goal rolls
   (`probability_per_beat` against the substantive stream). A hit
   that passes the preconditions yields an IntentData enqueued as
   `kind="intent"` band `NPC_REACTION`. A roll that hits but
   preconditions fail stays silent — the NPC tried, the world said
   no (no rejection event; the world's noise floor absorbs it).
3. **Director releases**: explicit triggers first, then the
   stagnation detector. Each release produces an IntentData enqueued
   the same way as an urgency.

Crossings fire in **tick order**: a beat at T=720 between rotations
at T=360 and T=1080 fires between them, not after both — otherwise
the log writer's tick-monotonicity invariant would reject the
out-of-order commit (the same hazard the iter-3 clock-crossing
rotation faced).

## 8. Director releases ride the intent door

A released hook produces an `IntentData` (id `director_<N>`) the
loop enqueues with `sub_order=NPC_REACTION`. The front door
validates preconditions, runs OCC (`based_on_event_seq` stamped at
enqueue), rolls the opposed check, and emits the event through the
resolver. A rejected director intent emits an `intent_rejected`
no-op event with `cause_intent = "director_..."` — the world noticed
the attempt (D-037: the canon door dispatches all reactions, the
director included).

The director never moves actors, changes state, or bypasses the
Intent→Event front-door (phase0 §4 "Objective broadcast"). The
director's contribution to M5 (non-PC event share) is measured
against the director-off baseline at the T8 A/B run (iter-6).

## 9. Per-NPC vs global targeting

The director's release targets **the hook's `target_npc`** (pack
data, not chosen at runtime). The cooldown applies to that NPC.
Targeting is thus a pack-level decision; the director never picks
a random NPC — that would be Alien's "the director learns the
player" anti-pattern, named and excluded.

Future work: a per-NPC desirability score (the L4D escalation
factors, phase-3 refinement) may select among candidate hooks
targeting different NPCs. For phase 0, the lowest-threshold rule
suffices.

## 10. Acceptance criteria (the iter-4 task)

- Seeded hooks fire causally — no "from nothing" complications
  (D-005).
- The world acts without the PC — urgencies fire on the beat cycle
  regardless of director state (M5 non-trivially non-zero by
  construction).
- T4 irreversibility holds — fire, injury, and the caught state
  are all irreversible; the decay pass never reduces them.
- T8 director-off (deferred to iter-6's A/B run): ≥3 emergent
  chains without the director. The chains come from urgencies +
  crime reactions + watch rotations + telling reactions + the
  transition engine.

## 11. What this spec does NOT cover (phase-3+ refinements)

- Multi-channel policies (threat / social / ambient) — L4D family.
- Layered thresholds (L4D2 three-intensity rule) and `PEAK_CLIMAX`
  (a high-severity hook's release is a climax beat, placed at the end
  of a peak — donor: the L4D boss rule).
- The full document_check action (the v0.1 stub uses `wait`; a
  dedicated action arrives when the document-check hook deserves
  its own resolution).
- A per-NPC desirability score for hook selection (phase-3).

Recorded, not built — the trigger for each refinement is the
matching phase gate or a fresh owner request.
