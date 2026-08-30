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
from core.resolvers import movement_changes

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle with pack.py
    from core.pack import Pack
    from core.rng import RngBank

__all__ = [
    "arrest_resolution_draft",
    "briefing_draft",
    "iter_suspicion_reactions",
    "next_rotation_tick",
    "rotation_plan",
]

# projection prop conventions shared with core/fold.py
CRIME_STATUS_PROP = "crime_status"


def _clamp(value: int, scale: Sequence[int]) -> int:
    return max(int(scale[0]), min(int(scale[1]), value))


# -- the crime-status progression (status_values is ordered; T4) -------------


def _at_or_past(status: Any, target: str, values: Sequence[str]) -> bool:
    """True when `status` sits at or beyond `target` in the pack's ordered
    `crime_watch.status_values` progression (v0.1: unknown → suspect →
    caught). An absent or unknown status precedes everything (None → the
    flip stays legal). `caught` is terminal — a status at or past `suspect`
    never flips again (T4: the caught state is irreversible)."""
    try:
        return values.index(status) >= values.index(target)
    except ValueError:
        return False


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
        # flip lands only while the status is still BELOW the suspect value
        # in the pack's progression — a suspect (or caught) suspect never
        # re-flips (T4: caught is irreversible, KI#18)
        status = projection.get(suspect_id, {}).get(CRIME_STATUS_PROP)
        status_values = list(config.get("status_values", ()))
        if new >= suspect_at and not _at_or_past(
            status, config["status_suspect_value"], status_values
        ):
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
                    pack.rules, {knowledge.who, suspect_id}, irreversible=0, hooks=0,
                    event_type=config["reaction_event"],
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
                        pack.rules, {knowledge.who, suspect_id}, irreversible=0,
                        hooks=0, event_type=arrest["event"],
                    ),
                )
            )
        yield tuple(drafts)


# -- arrest resolution (iter-4 leftover: capture/escape on threshold crossing) ---


def arrest_resolution_draft(
    pack: "Pack",
    projection: Mapping[str, Mapping[str, Any]],
    bank: "RngBank",
    arrest_record: EventRecord,
) -> EventDraft | None:
    """The arrest resolution (iter-4 leftover): the watcher moved to
    arrest; now the suspect evades vs the watcher's pursuit. Success =
    the suspect escapes (no state change — the attempt is a fact, the
    escape is a fact); failure = the suspect is caught (`crime_status:
    suspect -> caught`, irreversible per the pack's `crime_watch.arrest`).

    The check draws from the substantive stream (canon rolls); the
    resolution is a single event cause-chained to the attempt — the
    arrest is never a maybe, only its outcome is. Returns None when
    the suspect is already caught (a re-arrest is silent — idempotent
    per the KI#13 discipline)."""
    config = pack.rules["crime_watch"]["arrest"]
    suspect = arrest_record.target
    watcher = arrest_record.actor
    if suspect is None or watcher is None:
        return None
    if projection.get(suspect, {}).get(CRIME_STATUS_PROP) == "caught":
        return None  # already resolved — no duplicate
    checks = pack.rules["checks"]
    kind = checks["kinds"][config["resolution_check"]]
    die = checks["die"]
    evasion = _skill_total(pack, projection, suspect, kind["attack"])
    evasion_total = evasion + bank.randint(1, die)
    pursuit = _skill_total(pack, projection, watcher, kind["defend"])
    pursuit_total = pursuit + bank.randint(1, die)
    caught = pursuit_total >= evasion_total  # tie -> pursuer (pack rule)
    margin = pursuit_total - evasion_total
    if caught:
        changes = (
            StateChange(
                entity=suspect,
                prop=CRIME_STATUS_PROP,
                from_=projection[suspect].get(CRIME_STATUS_PROP),
                to_=config["caught_value"],
                irreversible=bool(config.get("caught_irreversible", False)),
            ),
        )
    else:
        changes = ()
    return EventDraft(
        t=arrest_record.t,
        type=config["resolution_event"],
        actor=watcher,
        target=suspect,
        cause=arrest_record.id,
        outcome={
            "caught": caught, "evasion_total": evasion_total,
            "pursuit_total": pursuit_total, "margin": margin,
        },
        state_changes=changes,
        importance=pack_importance(
            pack.rules, {watcher, suspect},
            irreversible=1 if caught and config.get("caught_irreversible") else 0,
            hooks=0,
            event_type=config["resolution_event"],
        ),
    )


def _skill_total(
    pack: "Pack",
    projection: Mapping[str, Mapping[str, Any]],
    entity_id: str,
    skill: str,
) -> int:
    """A local copy of `core.intent.skill_total` to avoid a runtime cycle
    (knowledge <-> intent already chain; this isolates the crime-system
    face of the skill table). Same pack-data semantics: base + status
    modifiers, every number in `rules.checks`."""
    checks = pack.rules["checks"]
    config = checks["skills"][skill]
    total: int = config["base"]
    for axis, mod in sorted(config.get("status_modifiers", {}).items()):
        value = projection.get(entity_id, {}).get(f"status.{axis}")
        if value is None:
            continue
        if "per_10_points" in mod and isinstance(value, (int, float)):
            total += (int(value) // 10) * mod["per_10_points"]
        elif "flat_when" in mod:
            total += mod["flat"] if value == mod["flat_when"] else 0
        elif "flat_at_least" in mod and isinstance(value, (int, float)):
            total += mod["flat"] if value >= mod["flat_at_least"] else 0
        elif "flat" in mod and isinstance(value, (int, float)) and value != 0:
            total += mod["flat"]
    return total


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
    the pair only forms when both posts are manned. Each swap rides
    `movement_changes`, so carried items travel with the rotating
    participant (KI#46: a participant walking off duty with a carried
    item must not leave its position behind — the st-1 presence fold
    reads positions as world facts)."""
    config = pack.rules["crime_watch"]["rotation"]
    duty, rest = config["duty_post"], config["rest_post"]
    participants: Sequence[str] = config["participants"]
    outgoing = next(
        (p for p in participants if projection[p]["position"] == duty), None
    )
    incoming = next(
        (p for p in participants if projection[p]["position"] == rest), None
    )
    changes: list[StateChange] = []
    for participant in participants:  # pack order — deterministic
        position = projection[participant]["position"]
        if position == duty:
            changes.extend(movement_changes(pack, projection, participant, rest))
        elif position == rest:
            changes.extend(movement_changes(pack, projection, participant, duty))
    return tuple(changes), outgoing, incoming


def briefing_draft(
    pack: Pack,
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
            pack.rules, {outgoing, incoming}, irreversible=0, hooks=0,
            event_type=config["rotation"]["transfer_event"],
        ),
    )
