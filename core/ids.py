"""Gap-free event ids and generation-packed actor handles (entt entt_traits).

Event ids are `ev_0000…` — monotonic and gap-free per run (EVENT_SCHEMA §2
pattern `^ev_[0-9]{4,}$`); the log writer assigns them, nobody else.
Actor handles pack `(index, generation)` into one int so a recycled index is
distinguishable in the queue key when dynamic entities arrive (phase 3+);
phase-0 pack entities address each other by stable string ids instead.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["ActorHandle", "sequence_id"]

_GENERATION_BITS: int = 24
_INDEX_MASK: int = (1 << _GENERATION_BITS) - 1


def sequence_id(prefix: str, n: int) -> str:
    """Zero-padded sequence id: prefix + 4+ digits (ev_0007, intent_0006)."""
    if n < 0:
        raise ValueError(f"sequence numbers are non-negative, got {n}")
    return f"{prefix}_{n:04d}"


@dataclass(frozen=True, slots=True)
class ActorHandle:
    """(index, generation) packed actor handle.

    `index` reuses slots of destroyed actors; `generation` separates an old
    handle from the recycled occupant of the same slot. Named future change
    (L13): dynamic entity recycling in phase 3+ keeps queue keys unambiguous.
    """

    index: int
    generation: int

    def pack(self) -> int:
        """Pack into one int: generation in the high bits, index in the low."""
        if not 0 <= self.index <= _INDEX_MASK:
            raise ValueError(f"index out of range 0..{_INDEX_MASK}: {self.index}")
        if self.generation < 0:
            raise ValueError(f"generation must be non-negative: {self.generation}")
        return (self.generation << _GENERATION_BITS) | self.index

    @classmethod
    def unpack(cls, packed: int) -> ActorHandle:
        """Inverse of `pack`."""
        if packed < 0:
            raise ValueError(f"packed handles are non-negative, got {packed}")
        return cls(index=packed & _INDEX_MASK, generation=packed >> _GENERATION_BITS)
