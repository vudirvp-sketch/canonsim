"""The states decay pass (MVP_SCOPE §5 system 5, deferred from iter-3):
fatigue/intoxication/fear decay per the pack's `rules.states` rates.
The pass fires at clock-crossing beats (the same discipline as watch
rotations — never pre-seeded, so a run still ends when its script's
queue drains). Injury has `auto_decay: 0` (the pack's signal it never
decays — only a counter-event can change it); attention decays via
the pack rate too, and resets on rotation when `reset_on_rotation`
holds (the distract action's "distracted" → neutral arc).

Every state delta is an event through the commit door (INV-1); the pass
returns drafts, the loop commits them. A delta that disagrees with
the projection fails loudly at the `_commit` gate (D-035 — the log
never holds a desynced event).

Per-axis rules (pack data, every number tunable):
- fatigue: `gain_per_360_ticks_awake` (+); `reset_on_rotation` (→ 0 at
  the watch rotation if true; the relief wakes fresh)
- intoxication: `decay_per_360_ticks` (−)
- fear: `decay_per_360_ticks` (−); `spike_on_alarm` (+, fires from
  the transition engine's alarm event, NOT here)
- injury: `auto_decay: 0` (no decay — counter-events only)
- attention: `decay_per_360_ticks` (−, often 0)
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from core.intent import pack_importance
from core.log import EventDraft, StateChange
from core.transitions import WORLD

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack

__all__ = ["decay_drafts"]

DECAY_EVENT: str = "status_decayed"  # templates vocabulary (lint-checked)


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


@dataclass(frozen=True, slots=True)
class _AxisDelta:
    """One axis's per-beat delta: signed (positive = gain, negative =
    decay). Computed at the beat from the pack's `per_360_ticks` rate
    and the actual beat gap (in ticks since the last decay event for
    the NPC, or since run start)."""

    axis: str
    delta: int


def _axis_deltas(
    pack: "Pack",
    axis: str,
    config: Mapping[str, Any],
    last_decay_tick: int | None,
    beat_tick: int,
) -> _AxisDelta | None:
    """Compute the signed per-axis delta for one beat. Returns None when
    the axis has no decay rule or the rate is zero. The rate is
    `gain_per_360_ticks_awake` (fatigue) or `decay_per_360_ticks`
    (others) — applied proportionally to the elapsed ticks since the
    last decay event (or since run start). Integer arithmetic only."""
    last = last_decay_tick if last_decay_tick is not None else 0
    elapsed = beat_tick - last
    if elapsed <= 0:
        return None
    rate_key = (
        "gain_per_360_ticks_awake" if axis == "fatigue"
        else "decay_per_360_ticks"
    )
    rate = config.get(rate_key)
    if rate is None:
        return None  # the axis has no decay rule (attention's optional)
    if rate == 0:
        return None  # explicitly zero: no decay (injury's sentinel)
    # Integer arithmetic: scaled to per-360 ticks, floored. A 60-tick
    # beat with rate 10/360 = floor(60*10/360) = floor(1.66) = 1.
    delta = (elapsed * int(rate)) // 360
    if delta == 0:
        return None
    # fatigue gains (+rate), the rest decay (-rate)
    sign = 1 if axis == "fatigue" else -1
    return _AxisDelta(axis=axis, delta=sign * delta)


def decay_drafts(
    pack: "Pack",
    projection: "Projection",
    events: Sequence[Any],
    beat_tick: int,
) -> tuple[EventDraft, ...]:
    """One decay beat: for each NPC with a `status.*` axis the pack
    declares a rate for, compute the delta since the last decay event
    (or run start) and produce a draft. The first NPC with a non-zero
    delta anchors the event; an empty tuple means no decay this beat.

    The drafts are per-NPC: one `status_decayed` event per NPC with a
    non-empty change set, so the chronicle reads each character's
    drift separately rather than as a single muddled line. The
    importance rule treats status deltas as low (the v0.1 call: only
    socially-meaningful changes climb to medium)."""
    states_config = pack.rules.get("states", {})
    if not states_config:
        return ()
    npcs = pack.entities["npcs"]
    drafts: list[EventDraft] = []
    for npc in npcs:
        npc_id = npc["id"]
        props = projection.get(npc_id)
        if props is None:
            continue
        if props.get("crime_status") == "caught":
            continue  # the caught do not tire
        last_decay = _last_decay_tick(events, npc_id)
        changes: list[StateChange] = []
        for axis, config in states_config.items():
            if not isinstance(config, Mapping):
                continue  # the section's notes field
            if axis == "notes":
                continue
            current = props.get(f"status.{axis}")
            if not isinstance(current, int) or isinstance(current, bool):
                continue  # NPC has no value on this axis (e.g. attention)
            delta = _axis_deltas(pack, axis, config, last_decay, beat_tick)
            if delta is None or delta.delta == 0:
                continue
            scale = pack.rules["relations"]["scale"]
            new_value = _clamp(current + delta.delta, scale[0], scale[1])
            if new_value == current:
                continue
            changes.append(
                StateChange(
                    entity=npc_id,
                    prop=f"status.{axis}",
                    from_=current,
                    to_=new_value,
                )
            )
        if not changes:
            continue
        drafts.append(
            EventDraft(
                t=beat_tick,
                type=DECAY_EVENT,
                actor=WORLD,
                target=npc_id,
                cause=None,  # the loop chains it to the last written event
                outcome={
                    "axes": [c.prop.split(".", 1)[1] for c in changes],
                },
                state_changes=tuple(changes),
                importance=pack_importance(
                    pack.rules, {WORLD, npc_id}, irreversible=0, hooks=0
                ),
            )
        )
    return tuple(drafts)


def _last_decay_tick(events: Sequence[Any], npc_id: str) -> int | None:
    """The tick of the NPC's latest `status_decayed` event — the
    baseline for proportional delta computation. None when the NPC
    has never decayed (run start)."""
    last: int | None = None
    for event in events:
        if event.type == DECAY_EVENT and event.target == npc_id:
            last = event.t
    return last
