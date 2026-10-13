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

iter-379 (the standing order's decay-landing row): `DecayIndex` —
the HEAP form of both walks' population scans. The walks stay the
semantic owners (D-024: `decay_drafts`/`next_decay_tick` own the
formulas); the index is their read-side accelerator, exact by the
twin laws (tests/test_decayidx.py). See the class docstring for the
staleness/veto discipline.
"""

from __future__ import annotations

import heapq
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from core.intent import pack_importance
from core.log import EventDraft, StateChange
from core.transitions import WORLD

if TYPE_CHECKING:  # pack + projection are duck-typed — no runtime cycle
    from core.fold import Projection
    from core.pack import Pack

__all__ = [
    "DecayIndex",
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


class DecayIndex:
    """The decay landing index (iter-379, the standing order's
    decay-landing row — the iter-362 index class applied to the two
    population-linear decay scans): one min-heap per LOCATION, each
    holding ``(next_fire, npc, prop)`` candidate cells for the LIVE
    (valued, unpinned, uncaught) status pairs positioned there — the
    walks' whole-population per-beat scans replaced by a heap peek
    (`next_decay_tick`) and a bounded firing enumeration
    (`decay_drafts`). The measured basis: decay_walk 3.31 profiled s
    + next_decay_tick 2.68 s on h32 10y (12.5% + the skip probe's
    decay share), the ×8.1 density exponent the strongest residual.

    THE STALENESS/VETO LAWS (the design's whole safety):

    - **INV-1 licenses staleness handling.** Every cause of
      staleness — the base moving (`last_change`), the value moving
      (pinning, type flips, births/clears), the position moving
      (scope hops), the caught flag flipping — rides a committed
      event's state changes, and `_commit` folds EVERY state change
      through `apply_change` AFTER the projection apply. So a cell
      dropped as stale always has a fresher successor in the pool:
      the re-derivation either pushed one (the pair still live) or
      the pair is legitimately absent (pinned/absent/caught never
      fire — the walks' own vetoes).
    - **Validation on sight, never eagerly.** A popped cell is valid
      iff it passes the walk's OWN filters against the live bound
      state: the entity present, positioned at this heap's key, not
      caught, the value int-not-bool, not pinned at the clamp bound
      in the axis's direction, and the cell's next_fire equal to
      `base + elapsed_first` for the CURRENT base. Invalid cells are
      dropped on sight — the pool is a candidate set, never a truth.
    - **The enumeration never consumes.** `firing` re-pushes every
      valid cell it popped, so a caller that drops the drafts (no
      commit) leaves the pool exactly as it was — the index is a
      pure read-side accelerator, never an assumption about the
      caller's commit discipline.

    KI#16's law is the birth constraint (the SensesIndex form): the
    pool is born from the pack-seeded INITIAL projection — the whole
    projection, seeds included, bases read from the caller's
    `last_change` (empty at construction: base 0, the walk's own
    default). The identity gate (the ScanGateMemo/SensesIndex law):
    `serves` answers True only for the exact projection, last-change
    dict, and axis table objects stamped at birth — every foreign
    caller keeps the walks. Deterministic throughout (INV-2): tuple
    heap cells, construction-order scans, zero draws, zero clock.
    Rebuildable from the log (the buffer's law) — never exported in
    the run state; a resume re-births it from the restored
    projection and the folded `last_change`."""

    __slots__ = (
        "_axes",
        "_axis_by_prop",
        "_scale",
        "_npc_ids",
        "_order",
        "_heaps",
        "_bound",
        "_last_change",
    )

    def __init__(self, pack: "Pack", axes: "Sequence[_DecayAxis]") -> None:
        # the CALLER's object kept by reference — `serves` gates on its
        # identity (the loop's init-time memo, never a re-wrapped copy)
        self._axes = axes
        self._axis_by_prop = {axis.prop: axis for axis in self._axes}
        self._scale = tuple(pack.rules["relations"]["scale"])
        self._npc_ids = frozenset(npc["id"] for npc in pack.entities["npcs"])
        # the pack's own declaration order (INV-2) — the firing
        # enumeration's answer order, the walk's own draft order
        self._order = {
            npc["id"]: index for index, npc in enumerate(pack.entities["npcs"])
        }
        self._heaps: dict[Any, list[tuple[int, str, str]]] = {}
        self._bound: "Projection | None" = None
        self._last_change: "Mapping[tuple[str, str], int] | None" = None

    @classmethod
    def from_projection(
        cls,
        pack: "Pack",
        projection: "Projection",
        axes: "Sequence[_DecayAxis]",
        last_change: "Mapping[tuple[str, str], int]",
    ) -> "DecayIndex":
        """The birth scan AND the identity stamp (the SensesIndex
        birth + bind collapsed: this index never folds a replay — a
        resume re-births from the restored state, so one constructor
        is exact). Scans the WHOLE projection (KI#16: every seeded
        value felt like an event record — the walk's own reading of
        the same projection), bases from `last_change` (the loop's
        own dict — at construction empty, so base 0, the walk's
        default for never-changed pairs)."""
        index = cls(pack, axes)
        for npc_id in index._order:
            props = projection.get(npc_id)
            if props is None:
                continue
            if props.get("crime_status") == "caught":
                continue
            heap = index._heaps.setdefault(props.get("position"), [])
            for axis in index._axes:
                current = props.get(axis.prop)
                if not isinstance(current, int) or isinstance(current, bool):
                    continue
                if _clamp(
                    current + axis.sign, index._scale[0], index._scale[1]
                ) == current:
                    continue  # pinned at the bound: never fires
                base = last_change.get((npc_id, axis.prop), 0)
                heapq.heappush(heap, (base + axis.elapsed_first, npc_id, axis.prop))
        index._bound = projection
        index._last_change = last_change
        return index

    def serves(
        self,
        projection: "Projection",
        last_change: "Mapping[tuple[str, str], int]",
        axes: "Sequence[_DecayAxis] | None",
    ) -> bool:
        """The identity gate: the walks' index branch serves ONLY the
        exact objects stamped at birth — the bound projection, the
        bound last-change dict, and the caller's axis table being the
        birth table itself (a None or a fresh resolution keeps the
        walk, the safe fallback for every existing caller)."""
        return (
            self._bound is not None
            and self._bound is projection
            and self._last_change is last_change
            and axes is self._axes
        )

    def apply_change(self, entity: str, prop: str) -> None:
        """Fold one committed state change (the `apply_event` twin for
        the pool): re-derive the pairs the change could move — the
        change's own axis when `prop` IS a decay axis (the base and
        the value move together: `last_change` was just updated, so
        the re-derivation reads the fresh base), ALL the entity's
        axes when `prop` moves the scope carriers (`position`,
        `crime_status`). Reads the live bound projection (the caller
        folds AFTER the apply) and the bound `last_change` — one
        source of truth per fact (D-024), never a private base copy.
        A re-derivation that fails a veto pushes nothing: the pair is
        legitimately absent until a later change re-derives it."""
        if entity not in self._npc_ids or self._bound is None:
            return
        if prop in self._axis_by_prop:
            self._repush(entity, self._axis_by_prop[prop])
        elif prop == "position" or prop == "crime_status":
            for axis in self._axes:
                self._repush(entity, axis)

    def _repush(self, entity: str, axis: _DecayAxis) -> None:
        """Push one fresh candidate cell for `(entity, axis)` iff the
        pair is live at the CURRENT bound state (the walks' own
        vetoes: present, uncaught, valued, unpinned)."""
        assert self._bound is not None and self._last_change is not None
        props = self._bound.get(entity)
        if props is None:
            return
        if props.get("crime_status") == "caught":
            return
        current = props.get(axis.prop)
        if not isinstance(current, int) or isinstance(current, bool):
            return
        if _clamp(current + axis.sign, self._scale[0], self._scale[1]) == current:
            return  # pinned at the bound: never fires
        base = self._last_change.get((entity, axis.prop), 0)
        heapq.heappush(
            self._heaps.setdefault(props.get("position"), []),
            (base + axis.elapsed_first, entity, axis.prop),
        )

    def _valid(self, cell: tuple[int, str, str], key: Any) -> bool:
        """One cell against the live bound state — the walks' OWN
        filters, never a second semantics: present, positioned at this
        heap's key (the scope's own read), not caught, valued
        int-not-bool, not pinned, and fresh (`next_fire` equal to the
        CURRENT base's landing — the cell was pushed by the latest
        re-derivation, never an older one)."""
        assert self._bound is not None and self._last_change is not None
        _, npc, prop = cell
        props = self._bound.get(npc)
        if props is None:
            return False
        if props.get("position") != key:
            return False  # the pair moved heaps: this cell is stale
        if props.get("crime_status") == "caught":
            return False
        axis = self._axis_by_prop[prop]
        current = props.get(prop)
        if not isinstance(current, int) or isinstance(current, bool):
            return False
        if _clamp(current + axis.sign, self._scale[0], self._scale[1]) == current:
            return False  # pinned at the bound: never fires
        return cell[0] == (
            self._last_change.get((npc, prop), 0) + axis.elapsed_first
        )

    def _scope_heaps(
        self, locations: Collection[str] | None
    ) -> list[tuple[Any, list[tuple[int, str, str]]]]:
        """The (key, heap) pairs under the call's scope, in the caller's
        own order (None — the one-scene law — is every heap; the dict's
        insertion order is deterministic, INV-2). The KEY rides along:
        validation compares the pair's live position to the heap the
        cell actually sits in — a pair that moved heaps fails its old
        heap's key, wherever it stands now."""
        if locations is None:
            return list(self._heaps.items())
        return [
            (loc, self._heaps[loc])
            for loc in locations
            if loc in self._heaps
        ]

    def next_fire(self, locations: Collection[str] | None) -> int | None:
        """The pool's minimum next-fire under the scope — the raw
        `min(base + elapsed_first)` the walk's `max(…, from_tick)`
        clamp composes with (the from_tick formula stays the walk's
        own, D-024). Stale cells at the tops are dropped on sight —
        the peek is also the pool's cleanup."""
        best: int | None = None
        for key, heap in self._scope_heaps(locations):
            while heap and not self._valid(heap[0], key):
                heapq.heappop(heap)
            if heap and (best is None or heap[0][0] < best):
                best = heap[0][0]
        return best

    def firing(
        self, beat_tick: int, locations: Collection[str] | None
    ) -> tuple[tuple[str, frozenset[str]], ...]:
        """The firing pairs at `beat_tick` under the scope: every
        VALID cell with `next_fire <= beat_tick`, grouped per NPC in
        the pack's own declaration order (the walk's draft order —
        INV-2). The enumeration NEVER consumes: valid cells popped
        during the scan are re-pushed before the answer, so a caller
        that drops the drafts leaves the pool exactly as it was (the
        no-commit law); the commit path's own re-derivations then
        supersede them naturally."""
        pairs: dict[str, set[str]] = {}
        for key, heap in self._scope_heaps(locations):
            held: list[tuple[int, str, str]] = []
            while heap and heap[0][0] <= beat_tick:
                cell = heapq.heappop(heap)
                if self._valid(cell, key):
                    held.append(cell)
                    pairs.setdefault(cell[1], set()).add(cell[2])
            for cell in held:
                heapq.heappush(heap, cell)
        return tuple(
            (npc, frozenset(props))
            for npc, props in sorted(pairs.items(), key=lambda item: self._order[item[0]])
        )


def _axis_change(
    npc_id: str,
    props: Mapping[str, Any],
    axis: _DecayAxis,
    last_change: Mapping[tuple[str, str], int],
    beat_tick: int,
    scale: Sequence[int],
) -> StateChange | None:
    """ONE axis's interval-proportional delta — the walk's own
    formula, extracted as its single owner (iter-379: the walk branch
    and the index branch call exactly this, so the two paths can
    never drift; the check order is the walk's historical order).
    None when the pair produces nothing this beat."""
    current = props.get(axis.prop)
    if not isinstance(current, int) or isinstance(current, bool):
        return None  # NPC has no value on this axis (e.g. attention)
    # the interval-proportional delta (integer arithmetic:
    # scaled to per-360 ticks, floored — a 60-tick beat with
    # rate 10/360 = floor(60*10/360) = floor(1.66) = 1)
    last_change_tick = last_change.get((npc_id, axis.prop))
    base = last_change_tick if last_change_tick is not None else 0
    elapsed = beat_tick - base
    if elapsed <= 0:
        return None
    delta = (elapsed * axis.rate) // 360
    if delta == 0:
        return None
    new_value = _clamp(current + axis.sign * delta, scale[0], scale[1])
    if new_value == current:
        return None
    return StateChange(
        entity=npc_id,
        prop=axis.prop,
        from_=current,
        to_=new_value,
    )


def _decay_draft(
    pack: "Pack", npc_id: str, changes: list[StateChange], beat_tick: int
) -> EventDraft:
    """One NPC's `status_decayed` draft from its change set — the
    walk's own construction, shared by both branches (the importance
    rule treats status deltas as low: only socially-meaningful
    changes climb to medium)."""
    return EventDraft(
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


def decay_drafts(
    pack: "Pack",
    projection: "Projection",
    last_change: Mapping[tuple[str, str], int],
    beat_tick: int,
    locations: Collection[str] | None = None,
    axes: "Sequence[_DecayAxis] | None" = None,
    *,
    index: DecayIndex | None = None,
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

    `index` (iter-379): the caller's `DecayIndex` — the heap form of
    this walk's population scan, served ONLY for the exact bound
    objects (`serves` — the identity gate; every other caller keeps
    this whole walk, the semantic owner). The candidates narrow the
    iteration; the per-pair computation is the SAME `_axis_change`
    both paths call, so the drafts are equal by construction — the
    twin law (tests/test_decayidx.py) the falsifier.

    The drafts are per-NPC: one `status_decayed` event per NPC with a
    non-empty change set, so the chronicle reads each character's
    drift separately rather than as a single muddled line. The
    importance rule treats status deltas as low (the v0.1 call: only
    socially-meaningful changes climb to medium)."""
    table = _decay_axes(pack) if axes is None else axes
    if not table:
        return ()
    scale = pack.rules["relations"]["scale"]
    drafts: list[EventDraft] = []
    if index is not None and index.serves(projection, last_change, axes):
        # the heap form: the firing candidates in the pack's own NPC
        # order (the walk's draft order), then the walk's own per-pair
        # computation over them alone — the population scan is the
        # pool's, the formula stays this walk's
        for npc_id, live_props in index.firing(beat_tick, locations):
            props = projection.get(npc_id)
            if props is None:
                continue  # defense: the enumeration validated presence
            if locations is not None and props.get("position") not in locations:
                continue  # defense: the enumeration validated scope
            if props.get("crime_status") == "caught":
                continue  # defense: the enumeration validated the veto
            changes: list[StateChange] = []
            for axis in table:
                if axis.prop not in live_props:
                    continue
                change = _axis_change(
                    npc_id, props, axis, last_change, beat_tick, scale
                )
                if change is not None:
                    changes.append(change)
            if changes:
                drafts.append(_decay_draft(pack, npc_id, changes, beat_tick))
        return tuple(drafts)
    for npc in pack.entities["npcs"]:
        npc_id = npc["id"]
        props = projection.get(npc_id)
        if props is None:
            continue
        if locations is not None and props.get("position") not in locations:
            continue  # the scene-LOD filter: this zone does not tick here
        if props.get("crime_status") == "caught":
            continue  # the caught do not tire
        changes = []
        for axis in table:
            change = _axis_change(
                npc_id, props, axis, last_change, beat_tick, scale
            )
            if change is not None:
                changes.append(change)
        if not changes:
            continue
        drafts.append(_decay_draft(pack, npc_id, changes, beat_tick))
    return tuple(drafts)


def next_decay_tick(
    pack: "Pack",
    projection: "Projection",
    last_change: Mapping[tuple[str, str], int],
    from_tick: int,
    locations: Collection[str] | None = None,
    axes: "Sequence[_DecayAxis] | None" = None,
    *,
    index: DecayIndex | None = None,
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
    never re-deciding them.

    `index` (iter-379): the caller's `DecayIndex` — the heap peek of
    this walk's population scan, served ONLY for the exact bound
    objects (the identity gate). The peek answers the raw
    `min(base + elapsed_first)` under the scope; the `max(…,
    from_tick)` clamp below stays THIS walk's own formula — the index
    never re-owns it (D-024). The twin law (tests/test_decayidx.py)
    pins the equality."""
    table = _decay_axes(pack) if axes is None else axes
    if not table:
        return None
    if index is not None and index.serves(projection, last_change, axes):
        landing = index.next_fire(locations)
        return None if landing is None else max(landing, from_tick)
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
