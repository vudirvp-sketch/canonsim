"""Groups & simulation LOD (depth-7, phases.md §5 — the iter-11b
resolutions in the D-112-ratified edition; TASKS depth-7): the WRITE
side of the LOD ladder at group scale — how off-screen life is
represented in the log, and how a group becomes canon when the reader
approaches. depth-6 landed the READ-side actor (the one-id law: the
group acts through the intent door); this module lands the tiers:

- **The population tier** (the COLD zone): a group anchored in the
  cold background emits ONE AGGREGATE EVENT per macro crossing —
  `macro_tick_drafts` — actor = the group id (one id, all tiers), the
  outcome carrying the POPULATION cardinality under `POPULATION_KEY`
  (the D-112 shape: counts for populations, events for notables; log
  growth O(groups x macrobeats), never O(members x ticks)). The count
  is derived from the live fold (L3): the static members whose
  `member_of` is still None — the unborn population. Pure arithmetic,
  zero draws (INV-2-clean by construction; the stream registry never
  sees a tier event).
- **The notable tier** (the WARM ring / the ACTIVE scene): the
  members act individually through the beat machinery (depth-3's zone
  scoping — the warm ring at the crossings, the active scene at the
  beats). The tier transition itself is the CONDENSATION —
  `condensation_drafts`: when a group's anchor crosses into the
  warm/active zones (the PC's approach; the zones follow the reader),
  ONE event per group carries each member's canon birth as a
  StateChange(member, `MEMBER_OF_PROP`, None -> group) — the D-054
  promotion shape at group scale (the detail materializer's twin: the
  slot is born, never re-birthed — a member already holding a value
  is SKIPPED) plus the group's tombstone marker
  (`MARKER_PROP`: None -> True).
- **The tombstone** (the derived store, INV-5 untouched): after the
  condensation the aggregate is realized — `is_condensed` reads the
  marker from the fold and the macro-tick walk stays silent. The
  marker is written once by the condensation event (INV-1 — state
  changes only through events) and never un-set by the engine; the
  aggregate events already in the log are never edited.
- **The `member_of` door** (D-020's pair-relation at group scale):
  membership is runtime state. The projection holds no seed for it
  (absence IS None — the D-054 slot shape, `core/fold.py`'s family);
  the condensation is the engine's writer, and any pack event may
  write it through the same state_changes surface — a join (None ->
  group), a leave (group -> None, the member fades back into the
  population), a transfer (group -> other). The fold's `apply_event`
  validates every from-value (INV-1 made executable). The depth-6
  faction walk reads the STATIC member list, never this door (the
  iter-92 law: "the runtime `member_of` state door is depth-7's row,
  never this walk's").

The id never changes between tiers (D-112): the aggregate's actor,
the condensation's actor, and the intent door's actor are the SAME
group entity id — `known_by`, entity texture, and old knowledge keys
survive without migration.

Pack vocabulary (both optional per group — the 68a pattern: the
committed pack declares neither; a group without them is depth-6's
intent-door actor alone, zero tier machinery, zero events):

- `entities.json::groups` — the record gains `macro_event` (the
  aggregate's event type) and `condense_event` (the condensation's
  event type), both in the template closure (EVENT_SCHEMA §11),
  both refused on a memberless group (dead data — the vacuity law:
  a population of nobody never carries a count and never births).
- The outcome keys `POPULATION_KEY` / `MEMBERS_KEY` are the engine's
  own mechanical vocabulary (the `cold_npcs` family — INV-3), the
  template binding surface for the pack's lines.

Determinism (INV-2): pack declaration order everywhere — the groups
walk in the pack's own order, the births in the group's own member
order; never a set iteration. The population tier's drafts are pure
functions of (pack, projection, t) — no entropy, no state mutation;
the condensation's TIER half (the member_of births, the marker, the
counts) stays draw-free with it. The NAME half (name-1, D-116 (12))
draws — on each member's own `name:<npc>` stream (the D-079 family
law's sixth member, `core/names.py::materialize_name`), so an added,
removed, or re-armed declaration shifts neither a canon check draw
nor another npc's name; the unborn population stays counts — the
lazy-depth law: unnamed until the reader's zone warms.
"""

from __future__ import annotations

from collections.abc import Collection
from typing import TYPE_CHECKING, Any, Final

from core.intent import pack_importance
from core.log import EventDraft, StateChange
from core.names import materialize_name
from core.rng import RngBank

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack

__all__ = [
    "MARKER_PROP",
    "MEMBER_OF_PROP",
    "MEMBERS_KEY",
    "NAMES_KEY",
    "POPULATION_KEY",
    "condensation_drafts",
    "is_condensed",
    "macro_tick_drafts",
]

#: The membership pair-relation's prop name on the member (D-020 at
#: group scale). Absence = None = the population tier (the D-054 slot
#: shape: the slot exists, unclaimed, until an event births it).
MEMBER_OF_PROP: Final = "member_of"

#: The group's tombstone marker prop — None until the condensation
#: writes True (the derived-store realization record, INV-5-clean:
#: the marker is fold state derived from the condensation event,
#: never a log edit). The macro-tick walk reads it as its gate.
MARKER_PROP: Final = "condensed"

#: The aggregate outcome's cardinality key — the unborn population's
#: count (the engine's mechanical vocabulary, the `cold_npcs` family;
#: INV-3 — a pack's template binds it, the engine never spells a
#: domain word).
POPULATION_KEY: Final = "population"

#: The condensation outcome's cardinality key — the canon membership's
#: size after the births (the notable tier's count).
MEMBERS_KEY: Final = "members"

#: The condensation outcome's generated-names key (name-1): the drawn
#: names of the members materialized by THIS event, member order — the
#: engine's mechanical vocabulary (the `population`/`members` family;
#: INV-3 — a pack's template binds the list, the tracery rendering
#: joins it). Present only when something materialized (the
#: drifted_from law — a never-empty key never rides an unarmed event).
NAMES_KEY: Final = "names"


def is_condensed(projection: "Projection", group_id: str) -> bool:
    """The tombstone read: True once the condensation event has
    written the group's marker (the aggregate is realized — the
    macro-tick walk stays silent from that event on). Derived from
    the fold (L3), never stored outside it."""
    return projection.get(group_id, {}).get(MARKER_PROP) is True


def _population(
    members: Collection[str], projection: "Projection", group_id: str
) -> int:
    """The unborn population's cardinality: the static members whose
    `member_of` is still None (absence included). A member who joined
    at runtime left the population (they are canon now); a member who
    left a runtime membership faded back into it; a member holding
    ANOTHER group's id belongs to neither (the transfer's honest
    read). Derived from the live fold (L3)."""
    return sum(
        1
        for member in members
        if projection.get(member, {}).get(MEMBER_OF_PROP) is None
    )


def macro_tick_drafts(
    pack: "Pack",
    projection: "Projection",
    t: int,
    locations: Collection[str],
) -> tuple[EventDraft, ...]:
    """One crossing's macro-tick aggregates (the population tier):
    for each group declaring `macro_event`, anchored in `locations`
    (the caller's COLD zone), not yet condensed — ONE event with
    cardinality: actor = the group id (one id, all tiers), the
    outcome carrying the population count under `POPULATION_KEY`.
    No knowledge (a world count), no state_changes (the count is
    derived, L3), no hooks (the director boundary is the consumers'
    own rows); importance rides the pack's own rule. The caller
    chains the cause to the macro turn (the consumer rides the
    clock's own event — the drift's precedent) and stamps the seed.

    `locations` is the LOD filter (the cold zone at the crossing);
    the walk itself follows pack declaration order (INV-2). A group
    without `macro_event`, a condensed group (the tombstone), and a
    group anchored outside the zone all stay silent — the 68a
    pattern per group."""
    drafts: list[EventDraft] = []
    for group in pack.entities.get("groups", ()):
        group_id = group["id"]
        event_type = group.get("macro_event")
        if event_type is None:
            continue  # this group's heartbeat is not declared (the 68a law)
        if is_condensed(projection, group_id):
            continue  # the tombstone: the aggregate is realized (D-112 (3))
        if projection.get(group_id, {}).get("position") not in locations:
            continue  # not this zone's population (the LOD filter)
        drafts.append(
            EventDraft(
                t=t,
                type=event_type,
                actor=group_id,
                cause=None,  # the loop chains it to the macro turn
                outcome={
                    POPULATION_KEY: _population(
                        group.get("members", ()), projection, group_id,
                    ),
                },
                knowledge=(),
                state_changes=(),
                hooks=(),
                importance=pack_importance(
                    pack.rules, set(), irreversible=0, hooks=0,
                    event_type=event_type,
                ),
            )
        )
    return tuple(drafts)


def condensation_drafts(
    bank: RngBank,
    pack: "Pack",
    projection: "Projection",
    t: int,
    locations: Collection[str],
) -> tuple[EventDraft, ...]:
    """One zone computation's tier transitions (the condensation on
    crossing the warm transition, D-112 (3) / D-116 (9)): for each
    group declaring `condense_event`, anchored in `locations` (the
    caller's warm ring + active scene), not yet condensed — ONE event
    carrying every un-born static member's canon birth
    (StateChange(member, `MEMBER_OF_PROP`, None -> group), the group's
    own member order — the D-054 promotion shape: a member already
    holding a value is SKIPPED, never re-birthed) plus the group's
    tombstone marker (`MARKER_PROP`: None -> True). The outcome
    carries the canon membership's size after the births under
    `MEMBERS_KEY`. No knowledge (the arrival snapshot is the move
    event's own templates, INTENT_SCHEMA §7 — a separate door, already
    landed), no hooks; importance rides the pack's own rule over the
    touched set (every entity whose state the event changed).

    name-1 (D-116 (12) — condensation's canon-birth events need
    names): a member declaring a generated name materializes it on
    THIS event — the birth (member, `NAME_PROP`, None -> drawn) paired
    with the member's own block (the membership birth first, the name
    beside it — one member, one block), drawn from the member's own
    `name:<npc>` stream (`core/names.py::materialize_name` — the
    unarmed/canon skips are its law; a runtime-joined member still
    gets the name it never had), and the outcome's `NAMES_KEY` lists
    the drawn names in member order (present only when something
    materialized — the drifted_from law). The tier half (the births,
    the marker, the counts) stays draw-free; an authored membership
    draws nothing at all.

    The condensation is the WRITE-side record alone: the members'
    per-beat activity was already depth-3's zone scoping (their
    positions put them in the warm ring or the active scene); what
    was missing — and what this event births — is their canon
    MEMBERSHIP. `locations` is the LOD filter (warm ∪ active); the
    walk follows pack declaration order (INV-2)."""
    drafts: list[EventDraft] = []
    for group in pack.entities.get("groups", ()):
        group_id = group["id"]
        event_type = group.get("condense_event")
        if event_type is None:
            continue  # this group's materialization is not declared
        if is_condensed(projection, group_id):
            continue  # already realized — the marker is write-once
        if projection.get(group_id, {}).get("position") not in locations:
            continue  # this zone does not condense here (the LOD filter)
        members = group.get("members", ())
        births: list[StateChange] = []
        named: list[str] = []
        canon = 0
        for member in members:
            current = projection.get(member, {}).get(MEMBER_OF_PROP)
            if current is None:
                births.append(
                    StateChange(
                        entity=member,
                        prop=MEMBER_OF_PROP,
                        from_=None,
                        to_=group_id,
                    )
                )
                canon += 1
            elif current == group_id:
                canon += 1  # a runtime join: already canon, not re-birthed
            name_birth = materialize_name(bank, pack, projection, member)
            if name_birth is not None:
                births.append(name_birth)
                named.append(str(name_birth.to_))
        changes = births + [
            StateChange(
                entity=group_id, prop=MARKER_PROP, from_=None, to_=True,
            )
        ]
        touched = {change.entity for change in changes}
        outcome: dict[str, Any] = {MEMBERS_KEY: canon}
        if named:
            outcome[NAMES_KEY] = named
        drafts.append(
            EventDraft(
                t=t,
                type=event_type,
                actor=group_id,
                cause=None,  # the loop chains it to the writer's last id
                outcome=outcome,
                knowledge=(),
                state_changes=tuple(changes),
                hooks=(),
                importance=pack_importance(
                    pack.rules, touched, irreversible=0, hooks=0,
                    event_type=event_type,
                ),
            )
        )
    return tuple(drafts)
