# DIRECTOR_SPEC.md — Director Contract

> Trigger fired at iter-4 start (`docs/SPECS_BACKLOG.md`). Single owner
> of the director's runtime contract; the blueprint `docs/blueprint/
> phase0.md` §4 owns the donor design, `core/director.py` owns the
> mechanics. Cited by ledger rows DIR-*; this file never restates them.
> ≤300 lines. Phase-3 landings: the pacing clock DIR-1 (iter-36,
> D-065), the climax layer DIR-3 (iter-38, D-067), the multi-channel
> split DIR-4 (iter-39, D-068), the event grammar's predicate + weight
> layer drama-1 (iter-40, D-069); the phase-3 refinements still
> recorded-not-built live in §11. Measured impact (every landing
> byte-identical on day1_full — the D-066 all-PEAK window; the grammar
> layer's 10-seed A/B included, iter-40): `docs/TEST_PLAN.md` §6.

## 1. What the director is

A **consequence planner** (D-005) that releases already-seeded hooks
into the world through the intent door — never an improviser. The
buffer holds hooks seeded at event time; predicate triggers (§3) fire
causally; the stagnation detector releases the lowest-threshold hook
when narrative entropy (P2e) drops below the pack's floor. Director-off
(T8 A/B baseline) keeps the buffer seeding but suppresses releases —
the world's emergent chains come from urgencies + reactions +
rotations, not director injections.

## 2. The buffer

| Field | Owner | Type |
|---|---|---|
| `tag` | event (the `hooks[]` entry) | `str` |
| `seeded_by_event` | commit door | event id |
| `seeded_at_tick` | commit door | `int` |
| `weight` | pack (`director.hooks[tag].weight`) | `int ≥ 0` — the BASE tension (drama-1: a flat int, or the `weight_multiplier` object `{base, modifiers}` — see §3a) |
| `release_threshold` | pack | `int ≥ 0` |
| `target_npc` | pack | npc id |
| `intent_kind` | pack | action name |
| `intent_target` | pack (optional) | entity id or `null` |
| `intent_fields` | pack | mapping |
| `trigger` | pack (optional) | a predicate spec (see §3) |
| `climax` | pack (optional, `director.hooks[tag].climax`) | `bool` — the boss-beat flag (DIR-3; see §5) |
| `channel` | pack (optional, `director.hooks[tag].channel`) | `str` — the hook's pacing dimension (DIR-4; see §5) |
| `weight_modifiers` | pack (drama-1, from the multiplier object) | the modifier tail — see §3a |
| `first_time_only` | pack (optional, `director.hooks[tag].first_time_only`) | `bool` — the Wesnoth fire-only-once release policy (drama-1): once any instance of the tag releases, the tag burns for the run; burned instances stay facts in the buffer but never release and never count toward entropy (un-dischargeable tension is noise, not tension) |

The buffer is **per-run** (folded from the log; reseeds from the
master seed every run because the events are deterministic per seed).
The pack data (`director.hooks`, policies, stagnation parameters) is
constant across runs. Director adaptation state never persists (INV-1:
`state = fold(log)`, the log is per-run).

## 3. Triggers (drama-1 predicates — causal, fire regardless of entropy)

A hook's `trigger` is a **predicate spec** — a JSON structure over the
folded projection, evaluated by `core/predicates.py` (the grammar's
single owner; pack lint validates the shape at load, the evaluator is
the loud runtime backstop). Pure (INV-2): a predicate only answers,
never schedules (TIME-1 — MTTH is the named anti-pattern the grammar
exists to replace).

Leaves (a Mapping carrying `kind`):

| Kind | Fields | Fires when |
|---|---|---|
| `time` | `tick` | `beat_tick ≥ tick` |
| `place` | `target_npc`, `location` | the target's projection position == location |
| `threshold` | `target_npc`, `axis`, `comparator` (`at_least` / `at_most`), `value` | the target's `relations.<axis>` meets the comparison |
| `prop` | `of`, `path`, `comparator` (`at_least` / `at_most` / `equals` / `not_equals`), `value` | the generalized projection read: any entity, any prop path |

Compounds (one discriminator key per node): `{"all": [spec, ...]}`
(AND), `{"any": [spec, ...]}` (OR), `{"not": spec}` (single inner —
the donor's own recommendation). A bare LIST of specs is the
implicit-AND root (the Paradox trigger body). The v0.1 leaf kinds run
unchanged through the grammar — a pack's flat triggers are
byte-identical. A missing prop / missing entity answers False (a
world answer, not an error); a bool never equals a number (`True != 1`
guarded); empty `all`/`any` lists are dead vocabulary (L1 — pack lint
rejects them).

A hook with `trigger: null` is **stagnation-only** — its trigger
never fires on its own; it relies on the stagnation detector.

## 3a. The weight_multiplier (drama-1 — context-sensitive tension)

`director.hooks[tag].weight` is a flat int (the v0.1 form) or the
multiplier object:

```json
{"base": 2,
 "modifiers": [
   {"add": 2, "when": {"kind": "threshold", "...": "..."}},
   {"factor": 0.5, "when": {"kind": "prop", "...": "..."}}
 ]}
```

Each modifier carries EXACTLY one of `add` (int ≥ 0) or `factor`
(number ≥ 0 — 0 legally zeroes the tension) plus a `when` predicate
(any spec from §3). The entropy sensor reads the **effective weight**
per beat: base, then each modifier whose `when` passes, in declaration
order — `add` sums, `factor` multiplies and truncates. Pure per
INV-2: a stored effective weight would be a projection inside the
buffer (L3); the buffer keeps data, evaluation computes the number.
The channel entropies read the same effective values (DIR-4). A pack
with flat weights runs the v0.1 entropy, byte-identically.

## 4. Narrative entropy (P2e)

```
entropy = sum(EFFECTIVE weight of unreleased, un-burned hooks)
        + sum(relations.suspicion across NPCs with the axis)
        + count of burning <layer>.<spot> props across all locations
```

Observable state only (L6) — never knowledge records, never PC
internals. The Influence Boundary (EPIST-1) extends from the
perceiver to the director itself. Replaces the v0.1 draft's flat
`release_after_ticks_without_visible_event: 90` timer — a tension
floor sensor, not a boredom timer.

## 5. Release policy (the minimal pair + the pacing clock + the climax
layer + the multi-channel split)

```python
class DirectorPolicy(Protocol):
    def permit_release(
        self, explicit_trigger_fires: bool, current_entropy: int
    ) -> bool: ...

    def permit_quiet(
        self, channel: ChannelConfig, channel_entropy: int
    ) -> bool: ...

    def permit_climax(self) -> bool: ...
```

- `EnabledPolicy(entropy_floor=N)`: explicit triggers always release;
  stagnation releases when `entropy < N` (the v0.1 global-floor quiet
  question — channelless hooks keep it even in a channels pack);
  `permit_quiet` compares the channel's entropy against the channel's
  own floor; the climax path is permitted whenever the pacing gates
  pass.
- `DisabledPolicy`: never releases (T8 A/B baseline) — every channel
  and the boss included.

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
two-clock fields) are the state machine itself. Measured at landing:
day1_full byte-identical, no fixture regen (TEST_PLAN §6 owns the
numbers).

**The climax layer (DIR-3, landed iter-38; the L4D2 three-intensity
rule + the boss-beat rule):** layered thresholds — the optional third
entropy layer `director.pacing.climax_floor`, strictly above
`peak_floor` (pack lint; the donor's instantiation is 3× the peak
threshold — this pack's 75 = 3 × 25). A climax-flagged hook releases
only through the climax path: the clock in PEAK having held
`min_peak_beats` (the placement law — boss beats END peaks, never
start them) and entropy at the third layer. The release marks the
beat `PEAK_CLIMAX` — one beat, entered only by a climax release,
never by entropy alone (the state marks the placement of a
high-severity hook, not an intensity band) — and the next transition
is REST unconditionally (boss beat + reset; a still-loud world breaks
the rest per the re-spike law, the transition after). Climax hooks
never release through the stagnation path — a boss does not spawn
because the world is boring — and explicit triggers stay causal
(D-005): when both fire at one beat, the explicit path releases
first and the clock does not mark PEAK_CLIMAX. The policy question is
separate (`permit_climax()` on the protocol — the boss releases at
high entropy where the stagnation path releases at low; one boolean
cannot serve both honestly). A pack without `climax_floor` runs the
iter-36 two-layer clock byte-identically, and a flagged hook without
the layer is explicit-trigger-only (the nopacing harness variant is
exactly that pack — legal, not drift). The tavern pack declares the
layer but no hook carries the flag yet — the document-check's v0.1
stub intent would make a hollow boss; the flag lands with the
`document_check` action (§11), the owner's content call.

**The multi-channel split (DIR-4, landed iter-39; the L4D
three-director family — Horde / S.I. / Music → threat / social /
ambient, the names are the pack's own):** `director.channels`
declares the pacing dimensions — each an `entropy_floor` plus the
observable inputs it binds (`inputs`, the closed vocabulary
`suspicion | physical_threats`; the channel's own unreleased hook
weights always feed it). A hook opts in per hook
(`director.hooks[tag].channel` — the per-hook opt-in mirrors the
climax flag): the quiet gate asks the hook's OWN channel's floor
against that channel's entropy, so a quiet social channel can inject
while the threat channel burns — the multi-channel win the single
global floor cannot express. Channelless hooks keep the v0.1
`entropy_floor` question even in a channels pack (the mixed mode is
legal); a channel tag without the block is inert dormant vocabulary
(the climax-flag-without-layer law; pack lint rejects a tag naming no
declared channel when the block exists). The pack's declaration is
the gate (INV-3): a pack without `director.channels` runs the v0.1
global-floor quiet path, byte-identically. What stays global on
purpose: the pacing clock (one drama arc over TOTAL entropy —
PEAK/REST suppress every channel), the budget (1 release per beat
across ALL channels; the pick stays the global lowest-threshold
tiebreak), the climax path (the boss gate reads total entropy), the
explicit triggers (D-005: causality is not channeling), the per-NPC
cooldown and the dead-actor skip. This pack's instantiation: threat 3
(an escalation's weight meets its own floor — the quiet path
self-blocks; `possible_document_check` fires causally), social 5 (the
v0.1 floor carried, suspicion-bound; `guard_suspicious_of_pc`),
ambient 2 (inputless noise floor — declared-but-dormant, no hook
carries it yet, the owner's content call). Measured at landing: the
10-seed A/B byte-identical (TEST_PLAN §6; the unit tests exercise
the split directly).

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
3. **Director releases**: explicit triggers first, then the climax
   path (DIR-3 — the boss gate), then the quiet path (the stagnation
   family — per channel since DIR-4). Each
   release produces an IntentData enqueued the same way as an urgency.

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

- The full document_check action (the v0.1 stub uses `wait`; a
  dedicated action arrives when the document-check hook deserves
  its own resolution — and with it the climax flag on the hook, per
  §5's scope note).
- A per-NPC desirability score for hook selection (phase-3).
- Ambient-channel content (the tavern pack declares the dimension; no
  hook carries it — a content-scale decision, the owner's call).
- The event grammar's remainder (drama-2/3, phases.md §3): option
  blocks with per-option availability gates + the
  `immediate`/`option`/`after` lifecycle, and the on_action dispatch
  table with append-not-overwrite composition (the ctx scope helpers
  ride with them — the predicate layer landed iter-40 is their
  foundation, not their replacement).

Recorded, not built — the trigger for each refinement is the
matching phase gate or a fresh owner request.
