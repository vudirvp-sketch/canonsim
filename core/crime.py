"""The crime-and-watch system (phase0 §3, MVP_SCOPE §5 system 7): NPC
memory driving behavior. Every threshold, axis, event type and delta here
is pack data (`rules.json` `crime_watch`) — the code is the mechanic.

- **Suspicion reactions:** acquiring a crime-mapped knowledge token moves
  the knower's suspicion axis by the pack delta (novel tokens only — a
  knower never re-reacts to what they already hold). The crime-status
  flip rides the first crossing event — the ev_0007 shape (suspicion
  0→25 together with status unknown→suspect), landed on the reacting
  system, not on the action (iter-3 task law). Crossing the arrest
  threshold while co-located with the suspect emits an arrest attempt —
  the reacting watcher acts on what *this* knower holds (EPIST-1); the
  attempt is a fact, its resolution is later work.
- **Watch rotation:** the pack-declared duty/rest posts swap their
  participants; the outgoing holder briefs the incoming one — a transfer
  event decaying fidelity one step (D-006: spread between watchers is
  transfer events, never group state; no group reputation exists).
- **Rotation ticks** are intraday offsets repeated every day — computed
  on demand from the clock, never pre-seeded into the queue: a run still
  ends when its script does.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Any

from core.intent import pack_importance
from core.knowledge import TOLD, KnowledgeView, decay_fidelity
from core.log import EventDraft, EventRecord, KnowledgeRecord, StateChange

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle with pack.py
    from core.pack import Pack

__all__ = [
    "briefing_draft",
    "iter_suspicion_reactions",
    "next_rotation_tick",
    "rotation_plan",
]

# projection prop conventions shared with core/fold.py
CRIME_STATUS_PROP = "crime_status"


def _clamp(value: int, scale: Sequence[int]) -> int:
    return max(int(scale[0]), min(int(scale[1]), value))


def iter_suspicion_reactions(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
    view: KnowledgeView,
    record: EventRecord,
) -> Iterator[tuple[EventDraft, ...]]:
    """Yield one draft group per reacting knower in the event's record
    order (deterministic). A group is the suspicion event (plus the status
    flip when it crosses) and, when the arrest threshold is crossed
    co-located with the suspect, the arrest attempt that follows it.
    Lazy on purpose: each group reads the projection as left by the
    previously committed groups — the status flip lands exactly once
    (the KI#13 lesson: never build all drafts against a stale world)."""
    config = pack.rules["crime_watch"]
    mapping: Mapping[str, str] = config.get("suspicion_from_knowledge", {})
    if not mapping:
        return
    axis = config["suspicion_axis"]
    scale = pack.rules["relations"]["scale"]
    thresholds = pack.rules["relations"]["suspicion_thresholds"]
    suspect_at = int(thresholds["status_suspect_at"])
    arrest = config["arrest"]
    arrest_at = int(arrest["requires_suspicion"])
    suspect_id = pack.player_id()
    sources: Mapping[str, int] = config["suspicion_sources"]

    for knowledge in record.knowledge:  # event order — deterministic
        source = mapping.get(knowledge.knows)
        if source is None:
            continue
        if view.holds(knowledge.who, knowledge.knows, before_source=record.id):
            continue  # not novel: the knower already reacted to this token
        props = projection.get(knowledge.who)
        if props is None or f"relations.{axis}" not in props:
            continue  # no suspicion home: the player, ambient groups
        delta = int(sources[source])
        current = int(props[f"relations.{axis}"])
        new = _clamp(current + delta, scale)
        if new == current:
            continue
        changes = [
            StateChange(
                entity=knowledge.who,
                prop=f"relations.{axis}",
                from_=current,
                to_=new,
            )
        ]
        # the status flip rides the first crossing (ev_0007 shape); the
        # v0.1 status field is two-valued — flip unless already flipped
        status = projection.get(suspect_id, {}).get(CRIME_STATUS_PROP)
        if new >= suspect_at and status != config["status_suspect_value"]:
            changes.append(
                StateChange(
                    entity=suspect_id,
                    prop=CRIME_STATUS_PROP,
                    from_=status,
                    to_=config["status_suspect_value"],
                )
            )
        drafts = [
            EventDraft(
                t=record.t,
                type=config["reaction_event"],
                actor=knowledge.who,
                target=suspect_id,
                cause=None,  # the loop chains the cause to the triggering event
                outcome={
                    "token": knowledge.knows,
                    "source": source,
                    "delta": delta,
                    "from": current,
                    "to": new,
                },
                state_changes=tuple(changes),
                importance=pack_importance(
                    pack.rules, {knowledge.who, suspect_id}, irreversible=0, hooks=0
                ),
            )
        ]
        if (
            current < arrest_at <= new
            and arrest.get("requires_same_location", False)
            and projection.get(suspect_id, {}).get("position")
            == projection[knowledge.who].get("position")
        ):
            drafts.append(
                EventDraft(
                    t=record.t,
                    type=arrest["event"],
                    actor=knowledge.who,
                    target=suspect_id,
                    cause=None,  # the loop chains it to this group's suspicion event
                    outcome={"suspicion": new, "threshold": arrest_at},
                    importance=pack_importance(
                        pack.rules, {knowledge.who, suspect_id}, irreversible=0, hooks=0
                    ),
                )
            )
        yield tuple(drafts)


# -- watch rotation (D-006: spread between watchers is transfer events) -------


def next_rotation_tick(
    rules: Mapping[str, Any], ticks_per_day: int, after: int
) -> int | None:
    """The smallest rotation tick strictly after `after` (intraday offsets
    repeated daily); None when the pack declares no rotations."""
    offsets = sorted(rules["crime_watch"].get("watch_rotation_ticks", ()))
    if not offsets:
        return None
    day = after // ticks_per_day
    candidates = sorted(
        d * ticks_per_day + offset
        for d in (day, day + 1)
        for offset in offsets
    )
    for candidate in candidates:
        if candidate > after:
            return candidate
    raise AssertionError("unreachable: next-day offsets always exceed `after`")


def rotation_plan(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
) -> tuple[tuple[StateChange, ...], str | None, str | None]:
    """The rotation's position swaps plus the briefing pair: outgoing = the
    participant leaving the duty post, incoming = the one leaving the rest
    post. Participants elsewhere (in pursuit, say) simply do not rotate —
    the pair only forms when both posts are manned."""
    config = pack.rules["crime_watch"]["rotation"]
    duty, rest = config["duty_post"], config["rest_post"]
    participants: Sequence[str] = config["participants"]
    outgoing = next(
        (p for p in participants if projection[p]["position"] == duty), None
    )
    incoming = next(
        (p for p in participants if projection[p]["position"] == rest), None
    )
    changes = []
    for participant in participants:  # pack order — deterministic
        position = projection[participant]["position"]
        if position == duty:
            changes.append(
                StateChange(entity=participant, prop="position", from_=duty, to_=rest)
            )
        elif position == rest:
            changes.append(
                StateChange(entity=participant, prop="position", from_=rest, to_=duty)
            )
    return tuple(changes), outgoing, incoming


def briefing_draft(
    pack: Pack,
    projection: Mapping[str, Mapping[str, Any]],
    view: KnowledgeView,
    tick: int,
    cause_id: str,
    outgoing: str | None,
    incoming: str | None,
) -> EventDraft | None:
    """The handover briefing: the outgoing holder re-emits every record the
    incoming one lacks, told, one fidelity step down (D-007); dedup by
    token — a listener never re-learns, and fidelity never upgrades.
    Official handovers are always accepted (the acceptance roll is the
    rumor path's mechanic, `core/knowledge.py`). None when the pair did
    not form or nothing new passes."""
    config = pack.rules["crime_watch"]
    if not config.get("transfer_on_rotation", False):
        return None
    if outgoing is None or incoming is None or outgoing == incoming:
        return None
    chain = pack.rules["knowledge"]["fidelity_chain"]
    records = []
    for record in view.records_of(outgoing):  # acquisition order — deterministic
        if view.holds(incoming, record.knows):
            continue
        records.append(
            KnowledgeRecord(
                who=incoming,
                channel=TOLD,  # type: ignore[arg-type]
                fidelity=decay_fidelity(record.fidelity, chain),
                knows=record.knows,
                at=tick,
            )
        )
    if not records:
        return None
    return EventDraft(
        t=tick,
        type=config["rotation"]["transfer_event"],
        actor=outgoing,
        target=incoming,
        cause=cause_id,
        outcome={"count": len(records)},
        knowledge=tuple(records),
        importance=pack_importance(
            pack.rules, {outgoing, incoming}, irreversible=0, hooks=0
        ),
    )
