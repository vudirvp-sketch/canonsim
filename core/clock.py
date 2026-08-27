"""Integer tick clock: day-phase boundaries are pack rule data, never code
constants (INV-3, `docs/blueprint/phase0.md` §1). One tick = one in-world
minute; the numbers themselves (1440/day, phase ranges) are owned by the
pack's `rules.json` (`MVP_SCOPE.md` §8) and cross-checked at load.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["Clock", "Phase"]


@dataclass(frozen=True, slots=True)
class Phase:
    """One day phase as pack data (`rules.json` `time.phases`)."""

    id: str
    from_tick: int
    to_tick: int


class Clock:
    """Monotonic integer tick counter with pack-driven phase/day lookup."""

    def __init__(self, phases: tuple[Phase, ...], ticks_per_day: int) -> None:
        if ticks_per_day <= 0:
            raise ValueError(f"ticks_per_day must be positive, got {ticks_per_day}")
        self._phases = phases
        self._ticks_per_day = ticks_per_day
        self._tick = 0
        cursor = 0
        for phase in self._phases:
            if phase.from_tick != cursor or phase.to_tick <= phase.from_tick:
                raise ValueError(f"phases must be contiguous and non-empty: {phase}")
            cursor = phase.to_tick
        if cursor != ticks_per_day:
            raise ValueError(f"phases cover {cursor} ticks, day is {ticks_per_day}")

    @classmethod
    def from_rules(cls, time_rules: dict) -> Clock:
        """Build from the pack's `rules.json` `time` section."""
        phases = tuple(
            Phase(id=p["id"], from_tick=p["from"], to_tick=p["to"])
            for p in time_rules["phases"]
        )
        return cls(phases=phases, ticks_per_day=time_rules["ticks_per_day"])

    @property
    def tick(self) -> int:
        return self._tick

    @property
    def ticks_per_day(self) -> int:
        return self._ticks_per_day

    def advance_to(self, tick: int) -> None:
        """Move the clock forward; time never flows backwards."""
        if tick < self._tick:
            raise ValueError(f"clock regression: {self._tick} -> {tick}")
        self._tick = tick

    def day_of(self, tick: int) -> int:
        """Day number for a tick (day 0 is the first day)."""
        return tick // self._ticks_per_day

    def phase_of(self, tick: int) -> str:
        """Phase id for a tick; fails loudly on uncovered ticks (pack lint
        guarantees coverage, the Clock double-checks at lookup)."""
        day_tick = tick % self._ticks_per_day
        for phase in self._phases:
            if phase.from_tick <= day_tick < phase.to_tick:
                return phase.id
        raise ValueError(f"tick {tick} (day offset {day_tick}) is covered by no phase")
