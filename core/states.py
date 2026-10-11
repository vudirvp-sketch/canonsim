"""The states decay pass (MVP_SCOPE §5 system 5, deferred from iter-3):
fatigue/intoxication/fear decay per the pack's `rules.states` rates.
The pass fires at clock-crossing beats (the same discipline as watch
rotations — never pre-seeded, so a run still ends when its script's
queue drains). Injury has `auto_decay: 0` (the pack's signal it never
decays — only a counter-event can change it); attention decays via
the pack rate too, and resets on rotation when `reset_on_rotation`
holds (the distract action's "distracted" → neutral arc).

Every state delta is an event through the commit door (INV-1); the
pass returns drafts, the loop commits them. A delta that disagrees with
the projection fails loudly at the `_commit` gate (D-035 — the log
never holds a desynced event).

Per-axis rules (pack data, every number tunable):
- fatigue: `gain_per_360_ticks_awake` (+); `reset_on_rotation` (→ 0
  for the rotation participants at the watch change if true — "the
  relief wakes fresh")
- intoxication: `decay_per_360_ticks` (−)
- fear: `decay_per_360_ticks` (−); the alarm spike number lives with the
  transition layer (`transitions.<layer>.alarm.fear_spike`) — it fires
  from the transition engine's alarm event, NOT here
- injury: `auto_decay: 0` (no decay — counter-events only)
- attention: `decay_per_360_ticks` (−, often 0); `reset_on_rotation`

iter-370 (the beat-machinery static-resolution family): the axis
CONFIGURATION is resolved once per pack — `decay_axes` builds the
static table (prop name, rate, sign, the first-fire elapsed) the two
walks read, the `urgency_specs` parse-once class extended from the
parse to its products. The per-(NPC, axis) path previously re-derived
the prop f-string, the config Mapping checks, and the rate lookup on
every pair of every beat (the measured density cost: 931K pair visits
per h32 10y run in EACH walk); the table carries the resolved values,
so the per-pair work is the two dict reads and the arithmetic the
law already owned. Byte-identical by construction (the oracle law:
the table equals the per-pair resolution over every committed pack).
"""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from core.intent import pack_importance
from core.log import EventDraft, StateChange
from core.transitions import WORLD

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack

__all__ = [
    "decay_axes",
    "decay_drafts",
    "next_decay_tick",
    "rotation_resets",
]

DECAY_EVENT: str = "status_decayed"  # templates vocabulary (lint-checked)


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


@dataclass(frozen=True, slots=True)
class _DecayAxis:
    """One pack-declared decay axis, statically resolved (iter-370):
    the pre-built `status.<axis>` prop name, the non-zero per-360 rate
    (the magnitude — the sign rides separately: fatigue gains, the
    rest decay), and `elapsed_first` — the first elapsed-tick count at
    which the floored delta reaches 1 (``ceil(360 / rate)``), the
    landing formula's own constant (H9's twin)."""

    axis: str
    prop: str
    rate: int
    sign: int
    elapsed_first: int


@dataclass(frozen=True, slots=True)
class _AxisDelta:
    """One axis's per-beat delta: signed (positive = gain, negative =
    decay). Computed at the beat from the pack's `per_360_ticks` rate
    and the actual beat gap (in ticks since the last decay event for
    the NPC, or since run start)."""

    axis: str
    delta: int


def _decay_axes(pack: "Pack") -> tuple[_DecayAxis, ...]:
    """The static half of `rules.states` (iter-370): every axis with a
    Mapping config, a rate key, and a non-zero rate — in the pack's own
    declaration order (INV-2). The `notes` section and rate-less axes
    (attention without a rule, injury's zero sentinel) resolve to
    nothing, exactly as the per-pair checks they replace."""
    states_config = pack.rules.get("states", {})
    axes: list[_DecayAxis] = []
    for axis, config in states_config.items():
        if not isinstance(config, Mapping):
            continue  # the section's notes field
        if axis == "notes":
            continue
        rate_key = (
            "gain_per_360_ticks_awake" if axis == "fatigue"
            else "decay_per_360_ticks"
        )
        rate = config.get(rate_key)
        if rate is None:
            continue  # the axis has no decay rule (attention's optional)
        rate = int(rate)
        if rate == 0:
            continue  # explicitly zero: no decay (injury's sentinel)
        axes.append(
            _DecayAxis(
                axis=axis,
                prop=f"status.{axis}",
                rate=rate,
                sign=1 if axis == "fatigue" else -1,
                elapsed_first=-(-360 // rate),
            )
        )
    return tuple(axes)


def decay_axes(pack: "Pack") -> tuple[_DecayAxis, ...]:
    """The parse-once accessor (iter-370, the static-resolution family
    — the `urgency_specs` memo's own class): the pure `_decay_axes`
    resolution, named for the LOOP's init-time memo. Both decay walks
    take the pre-parsed table through their `axes` parameter; None
    (the default) keeps the standalone resolution, so every existing
    caller is untouched."""
    return _decay_axes(pack)


def decay_drafts(
    pack: "Pack",
    projection: "Projection",
    last_change: Mapping[tuple[str, str], int],
    beat_tick: int,
    locations: Collection[str] | None = None,
    axes: "Sequence[_DecayAxis] | None" = None,
) -> tuple[EventDraft, ...]:
    """One decay beat: for each NPC with a `status.*` axis the pack
    declares a rate for, compute the delta since the last event that
    changed that axis (decay beat, use effect, rotation reset — or run
    start) and produce a draft. The first NPC with a non-zero delta
    anchors the event; an empty tuple means no decay this beat.

    depth-3 (the scene LOD filter): `locations` scopes the walk to NPCs
    positioned there — the ACTIVE zone at a beat, the WARM ring at a
    macro crossing; None (the default) is the one-scene law, every NPC
    (the unarmed world's per-beat behavior, the v0.1 bytes). The decay
    law itself is interval-proportional (the delta covers the elapsed
    since the axis's last change), so the coarser warm sampling lands
    the same linear drift, floored per event — value-exact modulo the
    floor, never a second scoring path (L13).

    `last_change` is the Simulator's derived index `(entity, prop) ->
    tick of the latest committed event that changed it`, maintained in
    the `_commit` funnel (L3 — a strict function of the log, no per-beat
    event scan; the KI#19 "any committer" baseline for free).

    `axes` (iter-370): the caller's PRE-PARSED static table (the loop's
    init-time memo via `decay_axes`) — None keeps the standalone
    resolution; the memo is byte-identical (the resolution is pure).

    The drafts are per-NPC: one `status_decayed` event per NPC with a
    non-empty change set, so the chronicle reads each character's
    drift separately rather than as a single muddled line. The
    importance rule treats status deltas as low (the v0.1 call: only
    socially-meaningful changes climb to medium)."""
    table = _decay_axes(pack) if axes is None else axes
    if not table:
        return ()
    npcs = pack.entities["npcs"]
    scale = pack.rules["relations"]["scale"]
    drafts: list[EventDraft] = []
    for npc in npcs:
        npc_id = npc["id"]
        props = projection.get(npc_id)
        if props is None:
            continue
        if locations is not None and props.get("position") not in locations:
            continue  # the scene-LOD filter: this zone does not tick here
        if props.get("crime_status") == "caught":
            continue  # the caught do not tire
        changes: list[StateChange] = []
        for axis in table:
            current = props.get(axis.prop)
            if not isinstance(current, int) or isinstance(current, bool):
                continue  # NPC has no value on this axis (e.g. attention)
            # the interval-proportional delta (integer arithmetic:
            # scaled to per-360 ticks, floored — a 60-tick beat with
            # rate 10/360 = floor(60*10/360) = floor(1.66) = 1)
            last_change_tick = last_change.get((npc_id, axis.prop))
            base = last_change_tick if last_change_tick is not None else 0
            elapsed = beat_tick - base
            if elapsed <= 0:
                continue
            delta = (elapsed * axis.rate) // 360
            if delta == 0:
                continue
            new_value = _clamp(
                current + axis.sign * delta, scale[0], scale[1]
            )
            if new_value == current:
                continue
            changes.append(
                StateChange(
                    entity=npc_id,
                    prop=axis.prop,
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
                    pack.rules, {WORLD, npc_id}, irreversible=0, hooks=0,
                    event_type=DECAY_EVENT,
                ),
            )
        )
    return tuple(drafts)


def next_decay_tick(
    pack: "Pack",
    projection: "Projection",
    last_change: Mapping[tuple[str, str], int],
    from_tick: int,
    locations: Collection[str] | None = None,
    axes: "Sequence[_DecayAxis] | None" = None,
) -> int | None:
    """The first tick >= `from_tick` at which `decay_drafts` would be
    non-empty — H9's quiet-beat skip landing bound for the decay family
    (iter-337). The pure FORMULA TWIN of the per-beat walk: per (npc,
    axis) in the ticking scope, the interval-proportional delta crosses
    1 exactly at ``last + ceil(360 / rate)`` (integer arithmetic: the
    floored product first reaches 1 there, and every later tick covers
    the same elapsed plus more — the decay is interval-proportional, so
    a skipped beat changes NO value, the next computed delta covers the
    whole gap); an axis whose value is already PINNED at the clamp
    bound in the delta's direction never fires (the pinned law —
    ``_clamp(current + sign) == current`` holds for every delta >= 1,
    monotonically), so it never constrains a landing. None when no axis
    can fire at any tick (the run's quiet stretches on a clamped or
    fully-rested world).

    `axes` (iter-370): the caller's PRE-PARSED static table (the loop's
    init-time memo via `decay_axes`) — the `decay_drafts` form's own
    parameter; None keeps the standalone resolution.

    The answer is a TICK, not a beat: the caller maps it onto the beat
    grid (the first grid point >= this tick inside the stretch). The
    twin's exactness is pinned by a property law (tests/test_h9.py:
    the formula's tick vs the first beat where `decay_drafts` answers
    non-empty, over crafted states) — the twin mirrors the walk's own
    filters (absent NPCs skip, the LOD scope skips, the caught skip),
    never re-deciding them."""
    table = _decay_axes(pack) if axes is None else axes
    if not table:
        return None
    scale = pack.rules["relations"]["scale"]
    best: int | None = None
    for npc in pack.entities["npcs"]:
        npc_id = npc["id"]
        props = projection.get(npc_id)
        if props is None:
            continue
        if locations is not None and props.get("position") not in locations:
            continue
        if props.get("crime_status") == "caught":
            continue
        for axis in table:
            current = props.get(axis.prop)
            if not isinstance(current, int) or isinstance(current, bool):
                continue
            if _clamp(current + axis.sign, scale[0], scale[1]) == current:
                continue  # pinned at the bound: this axis never fires
            last = last_change.get((npc_id, axis.prop))
            base = last if last is not None else 0
            # delta = (elapsed * rate) // 360 >= 1  <=>  elapsed >= ceil(360/rate)
            candidate = max(base + axis.elapsed_first, from_tick)
            if best is None or candidate < best:
                best = candidate
    return best


def rotation_resets(
    pack: "Pack",
    projection: "Projection",
    participants: Sequence[str],
) -> tuple[StateChange, ...]:
    """The `reset_on_rotation` status resets for the watch participants
    (KI#19): every axis the pack flags resets to 0 for every participant
    at the watch change — the handover is a context switch for both
    posts ("the relief wakes fresh"; a distracted holder hands over
    neutral). Only non-zero values produce changes; the resets ride the
    `watch_change` event the loop commits (INV-1 — one committer, one
    cause chain)."""
    states_config = pack.rules.get("states", {})
    if not states_config:
        return ()
    changes: list[StateChange] = []
    for participant in participants:
        props = projection.get(participant)
        if props is None:
            continue
        for axis, config in states_config.items():
            if not isinstance(config, Mapping):
                continue
            if not config.get("reset_on_rotation", False):
                continue
            current = props.get(f"status.{axis}")
            if not isinstance(current, int) or isinstance(current, bool):
                continue
            if current == 0:
                continue
            changes.append(
                StateChange(
                    entity=participant,
                    prop=f"status.{axis}",
                    from_=current,
                    to_=0,
                )
            )
    return tuple(changes)
