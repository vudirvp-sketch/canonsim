# DIRECTOR_SPEC.md — Director Contract

> Trigger fired at iter-4 start (`docs/SPECS_BACKLOG.md`). Single owner
> of the director's runtime contract; the blueprint `docs/blueprint/
> phase0.md` §4 owns the donor design, `core/director.py` owns the
> mechanics. Cited by ledger rows DIR-*; this file never restates them.
> ≤300 lines. Phase-3 landings: the pacing clock DIR-1 (iter-36,
> D-065), the climax layer DIR-3 (iter-38, D-067), the multi-channel
> split DIR-4 (iter-39, D-068), the event grammar's predicate + weight
> layer drama-1 (iter-40, D-069), the grammar's option layer drama-2
> (iter-41, D-070 — §3b), the grammar's on_action dispatch drama-3
> (iter-42, D-071 — §3c), the document_check content landing (iter-43,
> D-072 — §11's first pre-iter-43 row closed), the alarm panic echo
> (iter-48, content-2, D-077 — §3c's second live entry, the 7-case
> corpus re-distill); the phase-3 refinements
> still recorded-not-built live in §11. Measured impact (the grammar
> layers were byte-identical on day1_full at landing — the D-066
> all-PEAK window; the document_check landing is the first DELIBERATE
> divergence: the check fires on the runs that reach the confrontation,
> with the corpus regen it implied): `docs/TEST_PLAN.md` §6. arc-1
> (iter-47, D-076): the release-chain layer (§3d) — landed dormant, the
> 10-seed A/B byte-identical, zero corpus regen.

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
| `options` | pack (optional, `director.hooks[tag].options`; drama-2) | the release's branches — see §3b |

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

## 3b. The option layer (drama-2, iter-41 — the Paradox option mechanics adapted)

`director.hooks[tag].options` is an optional non-empty list of option
blocks — the release's branches. Each block carries EXACTLY the closed
key set `trigger | weight | intent | notes` (an unknown key is a lint
error, never a silent ignore — a typo'd `triger` would read as an
always-available option):

| Key | Shape | Meaning |
|---|---|---|
| `trigger` | a §3 predicate spec (optional) | the availability gate — closed = unavailable this beat |
| `weight` | a §3a flat int or multiplier (optional; default base 1) | the ai_chance weight — choice-local, never feeds entropy |
| `intent` | `{kind?, target?, fields?}` (optional) | the payload override — each declared key wholly replaces the base payload key; undeclared keys inherit |
| `notes` | prose (optional) | pack documentation |

The choose step (at release, before anything hits the door): every
option's availability gate evaluates against the projection; a zero
EFFECTIVE weight is never picked (the Stellaris factor-0 zero-out);
the heaviest effective weight wins, ties break by declaration order.
**No RNG** — the choice is a pure function of (pack data, projection,
beat_tick): every director decision stays RNG-free, and the cross-run
variety the donor's weighted DRAW provides comes from world state (the
modifiers read the projection — different runs, different winners).
The weighted draw itself is deliberately excluded, as MTTH is (the
TIME-1 family).

Laws composing with the existing machinery:

- **Deferred release**: a hook whose options are ALL gated off or
  zeroed out cannot release that beat — nothing hits the door, no
  budget is consumed; the hook waits for a world where an option
  opens (a closed hook is not a spent hook: the clock does not mark
  PEAK_CLIMAX for a closed boss). The threshold tiebreak orders
  releasable hooks only.
- **The base payload is the fallback**: a hook without `options` has
  exactly one implicit option — the base payload, always pickable; the
  v0.1 release path is byte-identical (the pack's own declaration is
  the gate, INV-3).
- **One owner per number**: the hook's own weight stays THE tension
  (§3a — the entropy sensor is unchanged); option weights steer the
  choice only.
- **The budget law holds**: 1 release per beat, 1 IntentData per
  release — the chosen option's payload rides the door (§8 unchanged).

The three-phase lifecycle maps onto the existing doors (phases.md §3):
immediate → **seed** (the consequence registers at commit time — the
projection facts the gates read are already canon); option → **choose**
(the gated weighted pick above); after → **apply** (the door's commit +
reaction dispatch — D-037's `_commit` runs reactions for every event).
No literal `immediate`/`after` effect blocks land — the adaptation IS
the mapping. The ctx scope helpers (`every`/`random`/`any`) did NOT
ride HERE: the option gates are single-entity predicates (the drama-1
grammar unchanged) and runtime target picking is §9's named
anti-pattern — the quantified-predicate question landed with drama-3's
on_action dispatch instead (§3c: the witnesses scope + the per-entity
gate, the entity-set iteration's first earner).

This pack's live instantiation: the vigil hook's glance/stare pair —
below the document-check band both weigh 1 and the glance (the v0.1
nudge) wins the tie by declaration order; in the band the stare's
escalated weight (1 + 2 when suspicion ≥ 50) wins, so the release
CHOICE hardens with the world exactly as the hook's tension does (two
layers, one band, one number each). Inert on the committed runs (the
vigil never releases there; TEST_PLAN §6 owns the A/B).

## 3c. The on_action dispatch (drama-3, iter-42 — the Paradox on_action
table adapted; `core/onaction.py` the mechanics)

`on_action` in rules.json: a table keyed by **committed event type**
— event X commits → content reacts, as pack data. The reaction runs
INSIDE `_react` (the canon door, D-037), APPENDED after the hardcoded
system reactions (suspicion → arrest → telling) and before the
director seeding — the donor's append-not-overwrite composition law:
vanilla logic runs, custom entries add, never replace; every entry of
the keyed LIST dispatches (the list is the append semantics — a
second declaration never replaces the first). The reaction is
immediate and cause-chained; nothing schedules (TIME-1 — MTTH stays
excluded with the weighted draw).

Each entry — the closed key set `scope | gate | event | state |
actor | target | notes` (an unknown key is a lint error, never a
silent ignore):

| Key | Shape | Meaning |
|---|---|---|
| `scope` | `"witnesses"` (the closed v0.1 vocabulary) | the entity-set selector: the triggering event's OWN knowledge records, deduped by first occurrence, in event order — "every NPC who witnessed X". The EXPLICIT ctx argument: no implicit `this`, no inherited scope |
| `gate` | a non-empty list of `{prop, comparator, value}` (optional) | the quantified predicate — per-entity conditions evaluated with the CANDIDATE as the argument (the spec carries NO entity field; `comparator` is the predicates.py vocabulary; a missing prop answers honestly, a bool never equals a number) |
| `event` | a templates event type (required) | the reaction event |
| `state` | `{prop, add}` — add a non-zero int (required) | the scoped state change: one clamped numeric delta per passing candidate (`relations.scale`, the one numeric scale — the alarm precedent); a candidate without a numeric home is dropped (the suspicion law); a clamped no-op is dropped (KI#13) |
| `actor` / `target` | `world` \| `source_actor` \| `source_target` (optional; defaults actor `world`, target `source_target`) | the closed one-hop resolution vocabulary — the donor's this/from chain collapsed to three names |
| `notes` | prose (optional) | pack documentation |

The reaction body is the **alarm shape**: ONE event per entry, t =
the source's tick, cause chained to the source, the outcome carrying
the source location (the event's own `location` outcome field, else
the source actor's position — the chronicle's fallback law) and the
reacting set; an empty gated scope emits NOTHING (a world answer, not
an event). The reaction event carries NO knowledge and NO hooks: the
system reactions skip a knowledge-less event, deferred consequences
ride the actions' own hooks (D-005), and pack lint enforces the
**one-hop law** — no table key may name a reaction event type the
table itself emits (a second-order declaration is a load-time error;
the cascade terminates by construction). The generator is lazy: each
entry's draft reads the projection as left by the previously
committed entries (KI#13). Pure per INV-2: a function of (pack data,
projection, record) — no RNG, no clock, no stored choice.

The grammar's ctx scope helpers: `every` rides as the scope+gate pair
above (the named use case — "every NPC who witnessed X"); `any` (the
exists-quantifier entry gate) and `random` (a one-pick iterator) stay
recorded-not-built — no content need has earned them (the ambient-
channel pattern; they land with their first consumer). Knowledge-
bearing reactions (a reaction that teaches) wait the same way.

This pack's declaration is LIVE since iter-43 (D-072 — the
owner's content call landed): the entry keys both branch types of
the check — `document_check` and `document_check_failed` →
`crowd_wary` (every witness of the public check grows warier —
the crowd-reaction layer the token-keyed crime system does not
cover; the scope reads the check's own witnesses, the room's
sighting token is deliberately un-mapped crowd memory). It fires on
every committed run and live session where the check lands
(cause-chained to the check; the reacting set = the witnesses with
a numeric home). The alarm panic echo is LIVE since iter-48
(content-2, D-077): `alarm_raised` → `panic_ripple` — every witness
of the shout gains fear (the through-the-walls law). The +10 delta
is the CONTAGION half, a quarter of the hardcoded +40 direct spike
(fear seen AND panic heard compound: the occupants 40 → 50, the
cause actor 0 → 10 — he hears his own shout); the scope is un-gated
(a shout unsettles everyone who heard it — the alarm's own
knowledge resolution decides who that is; the adjacent-hearer half
is structurally empty on the day-1 runs per the tune-3 static-
placement finding, dormant until NPC movement exists). The echo
commits at the alarm's own tick (the fear decay baseline stays
where the alarm set it); no knowledge, no hooks (the one-hop law);
`panic_ripple` is story-critical with its own chronicle line. The
landing paid the corpus regen it always implied (7 fire-family
cases re-distilled, the iter-43 precedent; the alarm case gained
the echo's own claims — the panic event by id + the cause actor's
fear). A pack without the `on_action` block runs
the v0.1 reaction behavior, byte-identically on runs that fire no
entry (TEST_PLAN §6 owns the A/B).

## 3d. The arc layer (arc-1, iter-47 — the release chains; P3c, the
DF event_collections / Paradox event-chain precedent)

`director.arcs` (pack data) declares named CHAINS of hook tags —
the arcs & tension shaping layer (P3c; the last engine row of the
phase-3 build column). Each arc block carries the closed key set
`members | min_gap_beats | notes` (an unknown key is a lint error,
never a silent ignore — the option-block precedent):

| Key | Shape | Meaning |
|---|---|---|
| `members` | a list of ≥ 2 unique declared hook tags | the chain's release ORDER; membership is declared HERE ONLY — one-sided, the members list is the single owner of the fact (D-024; a hook spec carries no arc key) |
| `min_gap_beats` | `int ≥ 2` | the chain's own pacing floor — the next member's beat waits at least this many beats after the previous one (1 is the 1-per-beat budget's own law — dead vocabulary, refused at load) |
| `notes` | prose (optional) | pack documentation |

Pack lint also refuses: a member naming no declared hook tag (a
typo'd member waits forever), a doubled member (a tag chained to
itself), and a tag in two arcs (ambiguous order — which cursor
governs its candidacy).

**The order law (causality, not pacing):** a member tag is a release
CANDIDATE only while it is its arc's current member — the first
member not yet released this run (a per-run cursor, folded state like
the burn set, INV-2). The chain gates candidacy on ALL release paths,
explicit triggers included: an arc is pack-declared causal structure
(a second beat that presupposes the first), not an intensity band —
D-005's ungated-explicit law is about the CLOCK, and the chain is not
the clock. A held explicit trigger re-evaluates per beat; when the
cursor reaches that member it fires if its trigger still holds (a
transient trigger that died while held is the pack author's liveness
question, honestly unanswered). A completed arc has no current member:
its leftover instances are spent facts. **The stall is honest** — if a
member's target dies or its trigger never fires, the chain stops
there and later members never release (the world's causality broke
the plan; the re-plan-on-violation refinement, §11, is the recorded
future escape hatch). Measured live (D-076, seed 125, day1_full, the
watcher pair chained as an e2e probe): the corpus-pinned relief-twin
release is HELD all run — its predecessor never releases on that run
("the post emptied the beat his band opened", iter-43) — the chain
semantics working, not a bug.

**The gap law (the tension-shaping half — pacing):** the current
member may not release through the quiet or climax path within
`min_gap_beats` beats of the arc's previous member's release — the
chain's beats march, they do not dump. Explicit triggers bypass the
gap (D-005: causality is not pacing — the world's own consequences
fire mid-gap exactly as they fire mid-rest). The first member has no
predecessor and is never gap-gated.

**The entropy mirror:** instances of PASSED members (a member whose
position precedes the cursor — one instance of it released, the arc
moved on) never release again and stop counting toward entropy — the
`first_time_only` burn law's twin (one play per arc beat;
un-dischargeable tension is noise). The CURRENT and FUTURE members
count normally — the seeded buffer's meaning is unchanged (a
fully-seeded chain reads its whole weight until it starts marching;
the channel entropies read the same view — the mirror is one law, not
a global-entropy special case). A stalled arc's future members keep
counting, exactly as any permanently-blocked hook does today (entropy
measures unresolved tension; a dead man's hook is noise the v0.1 law
already tolerates — no new hazard, unchanged).

The cursor advances at emit-time inside `_mark_released` — the same
law the budget and the per-NPC cooldown follow (a door rejection
still spends the member's beat: `intent_rejected` is a fact, the
world noticed the attempt; re-firing a spent member is the
re-plan-on-violation question, not this layer). Composes with every
standing layer: channels (a member may carry one — both gates
AND-compose), the climax flag (a boss member releases only through
the climax path AND only when current AND only gap-open), options
(the chosen option's payload rides the member's release),
`first_time_only` (orthogonal — a burned tag cannot advance the
cursor it already advanced).

A pack without `director.arcs` runs the v0.1 release path
byte-identically (the pack's own declaration is the gate, INV-3); an
EMPTY block is legal and inert. No chain is live in the committed
content set — the live driver is the content-6 row (the iter-38/42/
45/46 dormancy pattern; the machinery is unit-pinned on mutated packs
+ the 10-seed day1_full A/B 10/10 byte-identical vs HEAD, zero corpus
regen — D-076, TEST_PLAN §6 owns the protocol).

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
exactly that pack — legal, not drift). Since iter-43 (D-072) the
document-check pair carries the flag: the boss path consults the
option gate (a closed boss does not mark PEAK_CLIMAX, §3b's
deferred-release law), so the flag never burns on a world-impossible
release — measured live: a run whose watchers never reach the band
but whose tension sits at the third layer still releases the check
(the seed-2 shape, pinned in tests/test_doccheck.py).

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
   (`probability_per_beat`, each entry on its own `urgency:<npc>:<kind>`
   stream — engine-2, D-079: stream-isolated from the checks and from the
   other entries, so pack urgency growth shifts no draw positions). A
   hit that passes the preconditions yields an IntentData enqueued as
   `kind="intent"` band `NPC_REACTION`. A roll that hits but fails
   preconditions stays silent — the NPC tried, the world said
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

- The on_action grammar's `any`/`random` scope helpers and
  knowledge-bearing reactions (§3c — recorded-not-built, the
  first-consumer law).
- Ambient-channel content (the tavern pack declares the dimension; no
  hook carries it — a content-scale decision; lands with `social-1`'s
  fact-cluster work or its own row).
- A per-NPC desirability score for hook selection (phase-3).
- The arc layer's re-plan-on-violation (the Generative Agents
  planning shape, deterministic): a stalled chain today STAYS
  stalled (§3d — the stall is honest); a future refinement may let a
  pack declare a recovery (e.g. skip the stuck member, or re-seed the
  chain's remainder) — recorded-not-built, the first-consumer law
  (content-6's live driver decides whether any content needs it).
- The Alien three-axis `unknown` axis — pacing against the gap
  between actual state (log) and perceived state (knowledge records):
  the sketch (phases.md §3) says the director MAY pace against the
  gap; §4's entropy law says entropy reads observable state ONLY
  (L6/EPIST-1) and a knowledge-derived score is not observable state
  (the iter-46 FAQ pinned the same fence for the echo — an
  invariant-grade violation if wired). These two records CONFLICT and
  the conflict is the owner's to resolve: either the unknown axis
  never feeds entropy (a separate pacing input with its own declared
  fence), or the entropy law is amended by the owner with the L6
  boundary redrawn explicitly. Not built, not silently resolved.

The document_check action itself LANDED (iter-43, D-072 — the
§11 first row of the pre-iter-43 record, the owner's content call):
the full action over the `inspect` resolver, the climax flag on the
watcher pair, and the live crowd-witness reaction — the design
records live in `docs/DECISIONS.md` D-072 and the pack's own notes.
The alarm panic echo LANDED next (iter-48, content-2, D-077 — the
pre-iter-48 §11's first row): the through-the-walls law as one
on_action entry over the standing dispatch, with the 7-case corpus
re-distill (§3c the landing record).

Recorded, not built — the trigger for each refinement is the
matching phase gate or a fresh owner request.
