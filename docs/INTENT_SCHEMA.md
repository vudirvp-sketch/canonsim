# INTENT_SCHEMA.md — Intent Contract v0 (Track A, iter-2)

> The trigger for this spec (`docs/SPECS_BACKLOG.md`: "iter-2 starts") has
> fired; it is written from the iter-2 build, not ahead of it. Owners: the
> intent record and lifecycle live here; the **event** contract lives in
> `docs/EVENT_SCHEMA.md` (an Intent is a proposal, an Event is a fact);
> the pack's action vocabulary and its parameters live in
> `content/tavern_pack/actions.json` (`docs/MVP_SCOPE.md` §7 owns the
> table); the playscript file format lives in `docs/MVP_SCOPE.md` §13.
> This doc never restates those — it defines the grammar they share.

## 1. What an Intent is

An Intent is a **proposal** against the projection, never a state change
(phase0 §2). The front door (`core/loop.py`) owns the lifecycle; the
machinery (preconditions, checks, OCC, knowledge resolution) lives in
`core/intent.py`; resolvers live in `core/resolvers.py` as a name→callable
registry keyed by the pack's `resolver` field (INV-3: a string in data, a
generic mechanic in code).

```
PROPOSED ──validate shape──▶ ACCEPTED ──SCHEDULED completion──▶ resolved event
   │                            │                                  (success |
   │                            └─ precondition broken before     failure type)
   │                               completion (OCC) → REJECTED
   └─ precondition broken at proposal → REJECTED
REJECTED = an `intent_rejected` no-op event with a cause chain — never a
silent drop, never an exception.
```

## 2. The intent record

| Field | Type | Req | Meaning |
|---|---|---|---|
| `id` | string `intent_NNNN` | yes | monotonic per run, writer-side |
| `type` | string, snake_case | yes | one of the pack's action intents (`actions.json`) |
| `actor` | entity id | yes | the proposer (the player in phase 0; NPCs and the director enqueue through the same door from iter-4) |
| `target` | entity id | no | direct object; required when a precondition references the noun `target` |
| `fields` | per-action map | no | the action's declared `fields` only (`method`, `ticks`, `near` in tavern_pack; `take` also declares `texture` — iter-11) |
| `fields.texture` | resolved reference | no | the mediator's noun-resolution output `{entry, scope, slot, value}` — a live ledger entry the mediator resolved BEFORE the door (blueprint §1); core stays ledger-blind: the reference is data, shape-gated loud (`core/intent.py::texture_reference`), never checked for ledger liveness (the withdrawal mirror owns mid-flight retirement, VALIDATION_SPEC §8) |
| `based_on_event_seq` | integer | yes | the projection's event count at proposal — the OCC anchor (§4) |
| `risk` | number | reserved | phase 1+ (the mediator's risk dial; no consumer in phase 0 — a dead field would violate L1) |
| `uncertainty` | number | reserved | phase 1+ (validator confidence input) |

Reserved fields are documented with their phase and have **no** runtime
effect until then.

## 3. Preconditions (soft rejections)

`actions.json` `requires`: a list of structured conditions, all of which
must hold. **No string expression language** (L10) — a closed test set,
each with named parameters; the pack lint fails at load on an unknown
test. A failing condition rejects the intent with
`outcome.failed_test = "<noun>.<test>"`.

| Test | Parameters | Holds when |
|---|---|---|
| `kind` | `is` | the noun's entity category equals `is` (npc / item / location / ambient) |
| `same_location` | `with` | noun and `with` resolve to one location |
| `adjacent_to` | `with` | the noun (a location) is in `with`'s location's exits — teleport stays impossible (T5) |
| `location_of` | `with` | the noun **is** the location of `with` |
| `flag` | `flag` | the noun's pack record carries a truthy flag (`steal_target`, `is_fire_source`, …) |
| `field_in` | `field`, `values` | the pack field's value is in `values` (flammability classes) |
| `field_nonempty` | `field` | the pack field is a non-empty list (fire spots) |
| `carries_flagged` | `flag` | the npc carries an item whose pack record has `flag` |
| `flagged_accessible` | `flag` | an item with `flag` is carried by the noun or lies in its location |
| `relation_at_least` | `axis`, `value` | the npc's `relations.<axis>` (toward the actor, v0.1) is at least `value` — the talk trust floor |
| `carried_by` | `who` | the item's runtime `carrier` equals `who` |
| `uncarried` | — | the item's runtime `carrier` is None |
| `has_field` | `field` | the pack record has the field (`use_effect`) |
| `spot_available` | `layer` | the noun (a location) holds at least one spot of the pack-declared transition layer NOT in the layer's `spot_state` — the exact condition the ignite resolver keys on, so door and resolver agree by construction (pack-2/iter-29: igniting a destroyed or fully-burning location is a door rejection, never a no-ignition success; the layer param is lint-checked against the declared layers) |
| `texture_noun` | — | the intent carries a well-formed resolved texture reference whose scope target is a known entity (iter-11; ledger liveness deliberately NOT tested — core is ledger-blind) |

Nouns: `actor`, `target`, `texture` (iter-11 — resolves to the reference's
scope target, the canon entity a promotion lands on). Runtime sources: the
projection for position / carrier / relations / status; the pack for static
records. The same evaluator runs at proposal time and at completion time
(OCC, §4).

**The texture path (iter-11, blueprint §1 promotion).** When an intent
carries a `texture` field and the action ships a pack `texture` block, the
block's `requires` REPLACE the canon list (`core/intent.py::requires_for`)
and its `knowledge` templates render with the texture context — no canon
target on that path, so the `{target}` slot is lint-forbidden in the block
(use `{texture_slot}`). The pack owns which actions are texture-capable
(the grammar); the ledger owns which nouns are addressable (the
vocabulary) — the split is D-049. A success commits the promotion itself:
the scope target gains the slot as a canon prop (the object's canon birth);
a failure promotes nothing (the entry stays live+pinned). One intent is ONE
path: carrying both the reference and a canon `target` is a loud author
error at the shape gate (iter-11a) — the texture path replaces the target,
never combines with it.

## 4. Intent OCC (`based_on_event_seq`)

Every accepted intent carries the projection's event count at proposal.
At completion, if events were written since (`MAX(event_seq) >
based_on_event_seq`) **and** a precondition now fails, the intent is
rejected with `outcome.reason = "projection_moved"` and
`cause` = the id of the **event whose application first broke the
precondition** (found by folding forward from the initial projection —
attribution only; STATE-1 is untouched). A moved projection with intact
preconditions proceeds normally — one mechanism, the same semantics the
phase-1 validator uses (phase0 §2).

## 5. Checks (opposed rolls)

`rules.json` `checks` owns every number. A check runs at completion, from
the substantive stream, after the OCC re-check:

- **Attacker total** = skill base + status modifiers + `die` roll
  (`die: 20`). Status modifiers are per-skill tables with four modes:
  `per_10_points`, `flat` (non-zero numeric status), `flat_at_least` +
  `flat`, `flat_when` + `flat` (string statuses, e.g. attention).
- **Defender total**: `environment` — the action's flat `difficulty` +
  die; `target` — the target entity's defend skill + die;
  `best_in_location` — the strongest opposing npc/ambient at the actor's
  location (pack order breaks ties); **no** opponent present → the check
  is skipped (unopposed).
- Tie → defender. Defender wins by ≥ `failure_margin` → `total_failure`
  (the partial/total split of steal, when the action declares a
  `failure_total` knowledge branch).
- Intent `fields.method` names a modifier table (`distraction`: defender
  −10) — the in-attempt gambit, distinct from the `distract` action's
  lingering attention status.

The check result rides the event `outcome.check` (passed, margin, totals,
defender_id) — the balance-1 harness (iter-6) reads it from the log.

## 6. Outcomes and event emission

The resolver returns: the event **type** (the action's
`events.success` / `events.failure` — pack data, closed against the
template vocabulary at load), the `outcome` payload (always including the
check summary when a check ran), knowledge records, state changes, hooks,
and **ignitions** (world reactions executed after the primary event:
`drop_break`/`arson` → the fire layer). State changes compute `from` from
the projection at completion (items travel with their carrier; status
deltas clamp to the pack's relation scale). Importance follows the pack
rule (MVP_SCOPE §9): entities touched + irreversibility + far hooks +
the story-critical hook (tune-1/D-059).

**Actor status effects (tune-1, the `recuperate` resolver).** An action
may declare a `status_effects` list of `{status, delta}` entries — the
resolver applies each to the ACTOR, reading the current value from the
projection (never hardcoding `from`), clamping to the relation scale, and
skipping clamped-to-zero deltas (a quiet beat, not a desynced write).
The axes must be declared `rules.states` axes and the block is legal only
on the `recuperate` resolver (both lint-checked — dead pack data fails at
load). The tavern pack's `rest` is the canonical use: the fatigue
counter-play (KI#4).

## 7. Knowledge templates

Per action and branch (`success` / `failure` / `failure_total`), the pack
declares record templates: `who` ∈ {`actor`, `target`, `same_location`,
`adjacent_locations`, `destination_location`} + optional `except` tokens
(`actor`, `target`, `cause_actor`); `channel`/`fidelity` from the
EVENT_SCHEMA enums; `knows` is a slot template over `{actor}`, `{target}`,
`{location}`, `{cause_actor}`, `{texture_slot}` (closed set, lint-checked —
the texture slot names the promoted texture's slot, iter-11), `{present}`
(only on an expansion record, st-1 — below). Audiences resolve
to knowledge-holders only — npcs and ambient groups, never items; hearing
radii follow `rules.json` `position_visibility.hearing` (adjacent
locations hear vague only). Blind-NPC (T3) holds by construction: no
record, no knowledge.

Audience notes: `same_location` resolves against the actor's position at
**completion time, pre-change** — for a move that is the *origin* (the
departure sighting); `destination_location` (iter-3, movement sightings)
resolves against the action's target and requires a target-kind-location
precondition (lint-checked).

**The per-present-target expansion (st-1, the arrival snapshot's write
side; blueprint §5).** A template may declare `present_at` ∈ {`location`,
`destination_location`} — the audience stays `actor` (KI#43's law: this
is a `knows` expansion, NOT an audience kind), and the template expands
to ONE record per entity present at the site: pack declaration order
(npcs → ambient → items), the actor itself excluded, items included
(carried items are present via the carrier closure). `knows` must use
the `{present}` slot (one present target's id per record; the pairing is
lint-checked both ways — a site without the slot would emit N identical
records, a slot without a site has no semantics). `present_at:
destination_location` requires the target-kind-location precondition,
exactly like the audience; `except` is meaningless on an expansion (the
audience is the actor alone) and refused at load. The tavern pack's
`move` carries the canonical use: on arrival the mover learns one exact
`saw` record per present entity — the durable write-side twin of the
brief's entity cards (`BRIEF_SPEC.md` §3.4).

## 8. Rejection events

`intent_rejected` (mandatory template line, lint-checked): actor = the
proposer, `outcome` = `{action, reason: precondition|projection_moved,
failed_test}`, no state changes, no knowledge (the world did not
necessarily notice an impossible attempt — perception of attempts is
iter-3+), importance `low`, `provenance.cause_intent` present. A rejected
step consumes no ticks; the playscript continues at the same tick.

## 9. Button/command mapping (phase 0)

CLI commands and playscript steps map 1:1 to intents — no free text
(phase-2 parser gate). Current per-action `fields`:
`steal.method`, `drop_break.near` (a pack spot of the location),
`wait.ticks` (positive integer, required), `take.texture` (the
mediator-resolved reference, iter-11). Malformed steps (unknown
fields, missing targets, a target+texture mix, bad spot names, unknown
methods) are **author errors**: loud `RunnerError`, never logged as
rejections — the line between "the character attempted the impossible"
(a fact) and "the script is wrong" (a bug).

## 10. Versioning

This contract is code+pack owned (`core/intent.py`, `actions.json`,
`rules.json`); a grammar change that renames or removes a field of §2–§8
is an owner-approval event per `AGENTS.md` §8. Additive tests, audiences,
slots, or check kinds = pack/code growth, no bump.
