"""The re-encounter fold (since-1, D-180; the contract boundary
`docs/CONTRACTS.md` §3, the reading surface `docs/BRIEF_SPEC.md` §3.4's
extension): what changed in an entity since the reader last met it.

**The baseline sense (D1 — the per-entity encounter epoch).** A
(reader, entity) ENCOUNTER EPOCH is a maximal interval over which the
two are physically co-present: co-presence per
`core/fold.py::present_entities` — both positioned at the shared
location, or the carried-item closure — and, for a location, the
reader positioned at it (the scene's own interval). An epoch opens
when either one arrives at the other's location, closes when the
co-presence breaks (either moves away; a dropped item at the reader's
feet stays co-present, a carried-off item breaks). Event-indexed, not
tick-indexed: co-presence is evaluated on the projection state after
each event, and flips ride the events that flip them (same-tick events
resolve in log order — INV-2 by construction; ticks are display-only).

**The window (D1):** the delta window is [end-of-previous-epoch,
start-of-current-epoch) — what changed while apart. Concretely the
comparison basis is the reader's perceived surface at the two epoch
boundaries: the previous epoch's END state (the projection immediately
BEFORE the break event — what the reader last saw while together) vs
the current epoch's START state (the projection immediately AFTER the
opening event — the first view of the reunion). Changes during
co-presence are baked into the boundary snapshots and never surface
(scene_delta's own territory); an intermediate position hop the reader
never saw stays silent (only the endpoint comparison renders); a prop
the reader never knew a before-value for stays silent (D3 — the
comparison basis is the reader's perceived surface, never raw state).

**The heard family (D3):** the reader's own knowledge records born on
events that happened entirely while apart (co-presence false on both
sides of the event — the break and reunion events' own records are the
boundary moments' sightings, the beat window's territory). A record
renders on the entity it names (the record's token contains the
entity id, delimited by non-alphanumerics — pack-authored tokens that
name nobody render nowhere, D4's authoring law). The knower boundary
follows `core/retrieval.py`'s own law: only the READER's records ever
render — a record held by another knower is not the reader's
perceived surface.

Read-side view state, never logged (I1 — zero canon writes, zero new
event types); zero streams (INV-2 — no RNG anywhere in the fold); the
same log assembles to the same deltas in any process (I4). The pack
owns the line vocabulary (D4): `rules.json::brief.present_entities.
since_lines` — a missing section is the unarmed landing (the fold is
never built, zero segments, the committed corpus bytes untouched).
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

from core.fold import Projection, apply_event, initial_projection, present_entities
from core.log import EventRecord
from core.pack import Pack

__all__ = [
    "HeardDelta",
    "PropDelta",
    "Reunion",
    "ReunionFold",
    "since_config",
]

_POSITION: Final = "position"


@dataclass(frozen=True, slots=True)
class PropDelta:
    """One apart-window change on a pack-listed observable prop — the
    reader's perceived endpoints (never the intermediate hops)."""

    prop: str
    from_: Any
    to_: Any


@dataclass(frozen=True, slots=True)
class HeardDelta:
    """One of the reader's records born while apart, naming the entity."""

    token: str
    channel: str
    fidelity: str
    at: int


@dataclass(frozen=True, slots=True)
class Reunion:
    """One entity's re-encounter delta at the current epoch's opening:
    the pack-listed prop deltas (pack declaration order), the position
    transfer (the reader's last-seen location vs the reunion location),
    and the reader's apart-born records naming the entity (newest
    first — the brief's recency law). None of this is a canon write;
    the assembler renders it through the pack's templates."""

    props: tuple[PropDelta, ...]
    position: tuple[Any, Any] | None  # (last-seen, now) — None when unmoved
    heard: tuple[HeardDelta, ...]


@dataclass(frozen=True, slots=True)
class _Epoch:
    """One closed (reader, entity) encounter interval, reduced to what
    the reunion needs: the snapshot of the entity's observed props at
    the epoch's END (the projection immediately before the break
    event — the reader's last view while together)."""

    end_props: Mapping[str, Any]


def _both_known(before: Any, after: Any) -> bool:
    """D3's never-raw-state law: a delta renders only when the reader
    knew BOTH endpoint values (a prop born while apart has no
    perceived before — silent, never a `None -> value` line)."""
    return before is not None and after is not None


def _names(token: str, entity_id: str) -> bool:
    """Does the record's token name the entity? The id must appear
    delimited by non-alphanumerics (`npc_x_01` in `npc_x_01_present`
    yes; in `npc_x_012` no) — pack-authored tokens that name nobody
    render nowhere (D4: the pack's authoring problem)."""
    return (
        re.search(
            rf"(?<![A-Za-z0-9]){re.escape(entity_id)}(?![A-Za-z0-9])",
            token,
        )
        is not None
    )


class ReunionFold:
    """The per-(reader, entity) encounter epochs over one log — one
    pass, all candidate entities at once (the card population — npcs,
    ambient entities, items — plus every location, the scene card's
    own surface; groups act and never appear, so they carry no
    epochs). Build once per assembly, query per card. Pure: writes
    nothing, draws nothing (INV-1/2); the same (events, pack, reader)
    re-derives the same epochs (I4).

    The snapshots carry only the props the pack's vocabulary lists
    (plus `position`) — the card-observable surface, never private
    state (knowledge, echo, traits are not the card surface; D3's
    never-raw-state law made structural).
    """

    def __init__(
        self,
        events: Sequence[EventRecord],
        pack: Pack,
        reader: str,
        props: Sequence[str] = (),
    ) -> None:
        self._reader = reader
        self._candidates: list[str] = [
            record["id"]
            for category in ("npcs", "ambient_entities", "items")
            for record in pack.entities.get(category, ())
        ]
        self._candidates.extend(
            record["id"] for record in pack.entities.get("locations", ())
        )
        self._watched: tuple[str, ...] = (*props, _POSITION)
        self._pack = pack

        state = initial_projection(pack.entities)
        # per candidate: the last closed epoch, the open epoch's start
        # snapshot and entry records, and the records collected during
        # the apart stretch in progress
        self._prev: dict[str, _Epoch | None] = {}
        self._start: dict[str, Mapping[str, Any] | None] = {}
        self._entry_heard: dict[str, tuple[HeardDelta, ...]] = {}
        self._apart_heard: dict[str, list[HeardDelta]] = {}
        self._open: dict[str, bool] = {}
        for entity_id, co_present in self._presence(state).items():
            self._open[entity_id] = co_present
            self._prev[entity_id] = None
            # the initial epoch (t=0, the scenes() law) never yields a
            # reunion: no previous epoch exists — its start snapshot
            # stays None, `reunion` answers None by construction
            self._start[entity_id] = None
            self._entry_heard[entity_id] = ()
            self._apart_heard[entity_id] = []

        for event in events:
            relevant = any(
                change.prop in (_POSITION, "carrier")
                for change in event.state_changes
            )
            pre_open: dict[str, bool] | None = None
            end_shots: dict[str, dict[str, Any]] | None = None
            if relevant:  # presence may flip: keep the pre-event views
                pre_open = dict(self._open)
                end_shots = {
                    entity_id: self._snapshot(state, entity_id)
                    for entity_id in self._candidates
                    if self._open[entity_id]
                }
            apply_event(state, event)
            if relevant:
                for entity_id, now_present in self._presence(state).items():
                    if now_present == self._open[entity_id]:
                        continue
                    if now_present:  # the epoch opens at this event
                        self._entry_heard[entity_id] = tuple(
                            self._apart_heard[entity_id]
                        )
                        self._apart_heard[entity_id] = []
                        self._start[entity_id] = self._snapshot(
                            state, entity_id
                        )
                    else:  # the epoch closes: the END view is pre-event
                        self._prev[entity_id] = _Epoch(
                            end_props=end_shots[entity_id]
                        )
                    self._open[entity_id] = now_present
            # the reader's records born on this event belong to an
            # entity's apart window only when the pair was apart on
            # BOTH sides of the event (the break and reunion events'
            # own records are the boundary sightings — the beat
            # window's territory, never since-segments)
            for record in event.knowledge:
                if record.who != self._reader:
                    continue  # the knower boundary: only the reader's
                for entity_id in self._candidates:
                    was_apart = (
                        not pre_open[entity_id]
                        if pre_open is not None
                        else not self._open[entity_id]
                    )
                    if not (was_apart and not self._open[entity_id]):
                        continue  # not born entirely while apart
                    if _names(record.knows, entity_id):
                        self._apart_heard[entity_id].append(
                            HeardDelta(
                                token=record.knows,
                                channel=record.channel,
                                fidelity=record.fidelity,
                                at=event.t,
                            )
                        )

    # -- the reunion query ------------------------------------------------

    def reunion(self, entity_id: str) -> Reunion | None:
        """The current epoch's entry delta, or None when the entity is
        not currently co-present (no open epoch) or has no previous
        epoch (a first meeting — no apart window exists)."""
        if not self._open.get(entity_id, False):
            return None
        prev = self._prev.get(entity_id)
        start = self._start.get(entity_id)
        if prev is None or start is None:
            return None
        deltas = tuple(
            PropDelta(prop, prev.end_props[prop], start[prop])
            for prop in self._watched[:-1]  # the pack's order; position last
            if _both_known(prev.end_props[prop], start[prop])
            and prev.end_props[prop] != start[prop]
        )
        position = None
        if (
            _both_known(prev.end_props[_POSITION], start[_POSITION])
            and prev.end_props[_POSITION] != start[_POSITION]
        ):
            position = (prev.end_props[_POSITION], start[_POSITION])
        return Reunion(
            props=deltas,
            position=position,
            heard=self._entry_heard.get(entity_id, ()),
        )

    # -- internals ---------------------------------------------------------

    def _presence(self, state: Projection) -> dict[str, bool]:
        """Co-presence per candidate on the current projection: the
        present set at the reader's location (the carried-item closure
        included), plus the location the reader is AT (the scene's own
        interval — the reader's perceived surface of a place)."""
        present: frozenset[str] = frozenset()
        reader_pos = state.get(self._reader, {}).get(_POSITION)
        if reader_pos is not None:
            present = present_entities(state, str(reader_pos), self._pack)
        return {
            entity_id: (
                entity_id in present
                or (
                    self._pack.kind_of(entity_id) == "location"
                    and reader_pos == entity_id
                )
            )
            for entity_id in self._candidates
        }

    def _snapshot(self, state: Projection, entity_id: str) -> dict[str, Any]:
        props = state.get(entity_id, {})
        return {prop: props.get(prop) for prop in self._watched}


def since_config(pack: Pack) -> Mapping[str, Any] | None:
    """The pack's since-lines vocabulary (D4) — None = unarmed (the
    fold is never built, zero segments render, the committed bytes
    stand)."""
    section = pack.rules.get("brief", {}).get("present_entities", {})
    config = section.get("since_lines")
    if config is None:
        return None
    return config if isinstance(config, Mapping) else None
