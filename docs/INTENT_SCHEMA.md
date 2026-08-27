# INTENT_SCHEMA.md — Intent Contract v0 (Track A, iter-2)

> The trigger for this spec (`docs/SPECS_BACKLOG.md`: "iter-2 starts") has
> fired; it is written from the iter-2 build, not ahead of it. Owners: the
> intent record and lifecycle live here; the **event** contract lives in
> `docs/EVENT_SCHEMA.md` (an Intent is a proposal, an Event is a fact);
> the 12 actions and their parameters live in
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
| `fields` | per-action map | no | the action's declared `fields` only (`method`, `ticks`, `near` in tavern_pack) |
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

Nouns: `actor`, `target`. Runtime sources: the projection for position /
carrier / relations / status; the pack for static records. The same
evaluator runs at proposal time and at completion time (OCC, §4).

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
rule (MVP_SCOPE §9): entities touched + irreversibility + hooks.

## 7. Knowledge templates

Per action and branch (`success` / `failure` / `failure_total`), the pack
declares record templates: `who` ∈ {`actor`, `target`, `same_location`,
`adjacent_locations`, `destination_location`} + optional `except` tokens
(`actor`, `target`, `cause_actor`); `channel`/`fidelity` from the
EVENT_SCHEMA enums; `knows` is a slot template over `{actor}`, `{target}`,
`{location}`, `{cause_actor}` (closed set, lint-checked). Audiences resolve
to knowledge-holders only — npcs and ambient groups, never items; hearing
radii follow `rules.json` `position_visibility.hearing` (adjacent
locations hear vague only). Blind-NPC (T3) holds by construction: no
record, no knowledge.

Audience notes: `same_location` resolves against the actor's position at
**completion time, pre-change** — for a move that is the *origin* (the
departure sighting); `destination_location` (iter-3, movement sightings)
resolves against the action's target and requires a target-kind-location
precondition (lint-checked).

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
`wait.ticks` (positive integer, required). Malformed steps (unknown
fields, missing targets, bad spot names, unknown methods) are **author
errors**: loud `RunnerError`, never logged as rejections — the line
between "the character attempted the impossible" (a fact) and "the script
is wrong" (a bug).

## 10. Versioning

This contract is code+pack owned (`core/intent.py`, `actions.json`,
`rules.json`); a grammar change that renames or removes a field of §2–§8
is an owner-approval event per `AGENTS.md` §8. Additive tests, audiences,
slots, or check kinds = pack/code growth, no bump.
