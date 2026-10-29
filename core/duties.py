"""The duty memory (agenda-1 P3, iter-423): a pack-declared duty that goes
unkept at its clock becomes a RECORDED fact of the world — the same
writer the item expectations own (`core.knowledge.expectation_drafts`),
generalized from "the item is where it should be" to "the post is held by
one of the people who owe it".

Why a writer at all (the iter-415 §5.5 boundary): the projection is the
CURRENT state, so "the watch was not kept on the last rotation" is not
derivable from it — history needs a birth event. This module is that
birth site and nothing else: no scheduler (the clock already exists —
the watch rotation), no stored duty state, no priority.

Pack vocabulary (both halves optional — the unarmed law, the 68a
pattern: a pack declaring no `expectations.duties` keeps every byte and
every event of its corpus, INERT-FIRST measured, never assumed):

- `rules.json::expectations.duties[]` — one row per obligation:
  `{id, archetypes, post, knows, notes?}`. A row binds the obligation to
  a DECLARED `psyche` archetype (the identity layer owns who a person is;
  the row REFERENCES it, never copies a per-NPC roster — the design's
  generative form), names the LOCATION the obligation is owed at, and the
  knowledge token the lapse mints.
- `rules.json::expectations.duty_event` — the event type a lapse emits
  (a template-vocabulary member; the block's `check_at` clock is the one
  clock both halves run on).

The three states of a duty at the clock (pure projection reads):

    held     — at least one current holder stands at the post;
    dormant  — no current holder exists (a BORN holder is owed from its
               birth on; before it, nobody owes anything — the born law
               `core.psyche` P1, never an always-violated row);
    lapsed   — holders exist and none of them is at the post.

A lapse drafts ONE event per WITNESS: every entity present at the post
who is not a holder of that duty (the perception law the at-location
expectations already carry — an absence is knowable only on site). The
witness receives an `inferred`-channel record of the row's `knows` token;
once a witness holds it, the same lapse is not re-recorded (the
expectations dedup law — a memory, not a drumbeat).

The cause chain is the honest mover: the latest event that changed the
`position` of any lapsed holder (`core.knowledge.last_prop_mover`, the
expectations' own finder generalized). A holder the log never moved (a
freshly BORN holder, whose only event is the birth) has no mover to
blame — the draft then chains to the CLOCK event that opened the check
(`clock_event`: the rotation's own scheduled-beat convention), never to
an invented cause and never to a null one (the log writer allows a null
cause on the run-start event only).

No entropy: the check is a pure read of (pack, projection, log), so it
adds no stream, no draw count and no quiet-beat arithmetic (INV-2 — the
drive ticker's draw-count law has no twin here because nothing rolls).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.knowledge import (
    INFERRED,
    EventDraft,
    KnowledgeRecord,
    KnowledgeView,
    last_prop_mover,
    pack_importance,
)
from core.psyche import profile_of

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.log import EventRecord
    from core.pack import Pack

__all__ = [
    "DUTIES_KEY",
    "DUTY_EVENT_KEY",
    "DutySpec",
    "duty_specs",
    "duty_violation_drafts",
]

#: The expectations block's duty halves (the writer's one home).
DUTIES_KEY: Final = "duties"
DUTY_EVENT_KEY: Final = "duty_event"


@dataclass(frozen=True, slots=True)
class DutySpec:
    """One pack duty joined with its CURRENT holders (the parse's product:
    the row's immutable shape plus the projection's profiles).

    - `duty` / `post` / `knows`: the row's declared identities — the id is
      the citation key the event's outcome carries, the post is the one
      location the obligation is owed at, `knows` is the token the lapse
      mints;
    - `holders`: every npc whose profile archetype the row names, in npc
      declaration order (INV-2 — the pack's own order is the canon order);
      empty = dormant (nobody owes the duty yet).
    """

    duty: str
    post: str
    knows: str
    holders: tuple[str, ...]


def _config(pack: "Pack") -> Mapping[str, Any] | None:
    """The expectations block, or None (a pack with no block runs no
    duty check — the unarmed law)."""
    config = pack.rules.get("expectations")
    return config if isinstance(config, Mapping) else None


def duty_specs(
    pack: "Pack", projection: "Projection | None" = None,
) -> tuple[DutySpec, ...]:
    """Parse the pack's duty rows and join each with its current holders.

    The holders are read through `core.psyche.profile_of` (the authored
    key first, the born prop after), so a born profile arms its duty from
    the same accessor the drive ticker reads — one owner for "who is this
    person". Order: row declaration order, then npc declaration order;
    the same (pack, projection) always answers the same specs."""
    config = _config(pack)
    if config is None:
        return ()
    rows = config.get(DUTIES_KEY)
    if not isinstance(rows, (list, tuple)) or not rows:
        return ()
    state: Mapping[str, Mapping[str, Any]] = projection or {}
    profiles: list[tuple[str, str | None]] = []
    for npc in pack.entities.get("npcs", ()):
        profile = profile_of(pack, state, npc["id"])
        profiles.append(
            (
                str(npc["id"]),
                str(profile["archetype"]) if profile is not None else None,
            )
        )
    specs: list[DutySpec] = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue  # the lint owns the shape — this is the read-side check
        wanted = {str(name) for name in row.get("archetypes", ())}
        specs.append(
            DutySpec(
                duty=str(row["id"]),
                post=str(row["post"]),
                knows=str(row["knows"]),
                holders=tuple(
                    npc_id for npc_id, archetype in profiles
                    if archetype is not None and archetype in wanted
                ),
            )
        )
    return tuple(specs)


def duty_violation_drafts(
    pack: "Pack",
    projection: "Projection",
    view: KnowledgeView,
    events: Sequence["EventRecord"],
    tick: int,
    clock_event: str,
) -> tuple[EventDraft, ...]:
    """Draft the lapse records for one clock crossing: one event per
    witness of each lapsed duty, `inferred`-channel, cause-chained to the
    latest event that moved a lapsed holder's position — or to
    `clock_event` when the log moved nobody (the born-holder arm; see the
    module docstring).

    Every draft is an ordinary canon event: the caller commits it through
    the door, so its reactions cascade exactly like any other fact's."""
    config = _config(pack)
    if config is None:
        return ()
    event_type = config.get(DUTY_EVENT_KEY)
    if not isinstance(event_type, str) or not event_type:
        return ()  # no rows or no event type: the unarmed law
    posts = {
        post_id: tuple(
            str(npc["id"]) for npc in pack.entities.get("npcs", ())
            if str(npc["id"]) in projection
            and projection[str(npc["id"])].get("position") == post_id
        )
        for post_id in {
            spec.post for spec in duty_specs(pack, projection)
        }
    }
    drafts: list[EventDraft] = []
    for spec in duty_specs(pack, projection):
        if not spec.holders:
            continue  # dormant: nobody owes it yet
        present = tuple(h for h in spec.holders if h in projection)
        if any(projection[holder].get("position") == spec.post for holder in present):
            continue  # held
        away = tuple(
            holder for holder in present
            if projection[holder].get("position") != spec.post
        )
        cause = last_prop_mover(events, away, "position")
        witnesses = tuple(
            entity for entity in posts.get(spec.post, ())
            if entity not in spec.holders
        )
        for witness in witnesses:
            if view.holds(witness, spec.knows):
                continue  # already noticed — a memory, not a drumbeat
            drafts.append(
                EventDraft(
                    t=tick,
                    type=event_type,
                    actor=witness,
                    target=None,
                    cause=cause.id if cause is not None else clock_event,
                    outcome={
                        "duty": spec.duty,
                        "expected": {"held_at": spec.post},
                        "observed": {"held_by": []},
                    },
                    knowledge=(
                        KnowledgeRecord(
                            who=witness,
                            channel=INFERRED,
                            fidelity="exact",
                            knows=spec.knows,
                            at=tick,
                        ),
                    ),
                    importance=pack_importance(
                        pack.rules,
                        {witness, *away},
                        irreversible=0,
                        hooks=0,
                        event_type=event_type,
                    ),
                )
            )
    return tuple(drafts)
