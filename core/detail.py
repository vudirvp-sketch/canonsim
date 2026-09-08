"""Lazy scene-detail materialization (depth-2, `phases.md` §5 — the
phase-5 build column's second row; TASKS depth-2). The D-054
texture-promotion law executed at scene scale, never a second mechanism
beside the ledger/promotion door:

- **The lazy draw** (`materialize_scene_detail`): a scene's unobserved
  detail is generated deterministically from the content-addressed
  stream `scene:<id>:detail` (`core/rng.py::scene_detail_stream_name`,
  the D-079 family law's third member) on the first meaningful
  observation — the scene-snapshot resolver family (`observe`: the
  action whose knowledge is the scene itself). One draw per pack-declared
  slot, pack declaration order (INV-2); the committed event's
  `state_changes` carry each birth as `StateChange(location, slot,
  None -> value)` — the canon-birth shape of the texture promotion,
  riding the observation event exactly as the take rides the promotion.
  Re-observation reproduces the same detail: a slot already in the
  folded projection is SKIPPED — no redraw, no second change (the
  fingerprint law: the stream advances only on an actual birth).
- **First-commit-wins** (the committed world outranks every later
  claim, whatever its value — a slot already described empty rejects
  the later gold): the draw path's canon-skip IS the law's draw-side
  half; the claim-side half is `detail_claim`, the ledger's
  texture-OCC mirror — an external claim (the depth-5 worldgen passes
  are the first legal caller; the loop's own draw never conflicts with
  itself) answers `commit` (slot unclaimed), `no_op` (canon holds the
  same value — the idempotent duplicate), or `slot_conflict` with the
  CAUSE CHAIN: the event that last wrote the slot, the current
  authority the claim conflicts with. The log is the only truth read
  (INV-1); pack-modeled slots are lint-refused against the block
  (`core/pack.py::_scene_detail`), so a claim verdict never needs the
  pack.
- **The unarmed law (the 68a pattern)**: a pack without the
  `rules.json::scene_detail` block materializes nothing — the draw
  returns before any assure scope or draw, so the fingerprint and the
  v0.1 bytes are untouched by construction. The pack's own declaration
  is the arming (depth-2b); the block's shape lint is the block's only
  reader at runtime-lint time.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from core.log import EventRecord, StateChange
from core.rng import RngBank, scene_detail_stream_name

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle with pack.py
    from core.pack import Pack

__all__ = [
    "COMMIT",
    "ClaimVerdict",
    "NO_OP",
    "SCENE_DETAIL_BLOCK",
    "SLOT_CONFLICT",
    "detail_claim",
    "materialize_scene_detail",
    "materialized_fields",
]

#: The rules.json block this module reads: `location_id -> slot list`.
#: The lint (`core/pack.py::_scene_detail`) owns the closed vocabulary.
SCENE_DETAIL_BLOCK: Final = "scene_detail"

COMMIT: Final = "commit"
NO_OP: Final = "no_op"
SLOT_CONFLICT: Final = "slot_conflict"


@dataclass(frozen=True, slots=True)
class ClaimVerdict:
    """The claim gate's answer for one `(location, slot, value)` claim
    against the committed log. `commit`: the slot is unclaimed — the
    claimer is the first committer, the law's winner. `no_op`: canon
    holds the same value (the idempotent duplicate — the ledger's
    duplicate rule, a recorded non-event, never a refusal).
    `slot_conflict`: canon holds a different value — the loser is
    rejected, `cause` chain-linking the winning event (the last write
    on the slot, the authority the claim conflicts with; a pack-modeled
    slot never reaches the verdict — the lint refuses the double
    claim)."""

    outcome: str
    cause: str | None = None

    @property
    def refused(self) -> bool:
        return self.outcome == SLOT_CONFLICT


def materialize_scene_detail(
    bank: RngBank, pack: "Pack", projection: Mapping[str, Mapping[str, Any]],
    location: str,
) -> tuple[StateChange, ...]:
    """Draw the scene's unmaterialized detail slots, in pack declaration
    order, from the scene's own `scene:<id>:detail` stream (nested inside
    the assured substantive run scope — the family law). A slot already
    present in the folded projection is skipped: first-commit-wins, the
    re-observation law (canon is the answer, never a redraw). An unarmed
    pack (no `scene_detail` block, or the location unlisted) answers an
    empty tuple BEFORE touching the bank — zero assures, zero draws, the
    v0.1 bytes untouched."""
    slots = pack.rules.get(SCENE_DETAIL_BLOCK, {}).get(location)
    if not slots:
        return ()
    site = projection.get(location, {})
    changes: list[StateChange] = []
    with bank.assure(scene_detail_stream_name(location)):
        for spec in slots:  # pack order — deterministic (INV-2)
            slot = spec["slot"]
            if slot in site:
                continue  # canon outranks the lazy draw — never a redraw
            values = spec["values"]
            value = values[bank.randint(0, len(values) - 1)]
            changes.append(
                StateChange(entity=location, prop=slot, from_=None, to_=value)
            )
    return tuple(changes)


def materialized_fields(changes: Sequence[StateChange]) -> list[dict[str, Any]]:
    """The observation event's outcome decoration: one `{slot, value}`
    per materialized birth, in commit order. Present on the event only
    when something materialized — the drifted_from law (a never-empty
    key never rides an unarmed event, so the committed v0.1 bytes do
    not move)."""
    return [{"slot": change.prop, "value": change.to_} for change in changes]


def detail_claim(
    events: Sequence[EventRecord], location: str, slot: str, value: Any,
) -> ClaimVerdict:
    """The slot_conflict mirror (the ledger's texture-OCC twin at scene
    scale): validate one declared detail claim against the committed
    world. Log order, the LAST write on `(location, slot)` owns the
    current canon value; a written slot refuses a different value with
    the winning event's id as the cause chain, and accepts the same
    value as the idempotent no-op. An unclaimed slot commits —
    first-commit-wins for the claimer. The loop's own draw never calls
    this (it skips canon slots before drawing); the gate is the law's
    single owner for the external claim paths — the depth-5 worldgen
    passes family — pinned here, live the day its first caller lands
    (the first-consumer law)."""
    written = False
    current: Any = None
    cause: str | None = None
    for event in events:  # log order: the last write is the authority
        for change in event.state_changes:
            if change.entity == location and change.prop == slot:
                written, current, cause = True, change.to_, event.id
    if not written:
        return ClaimVerdict(COMMIT)
    if current == value:
        return ClaimVerdict(NO_OP)
    return ClaimVerdict(SLOT_CONFLICT, cause)
