"""The single event queue: one heapq keyed `(tick, sub_order, actor_id)` with
a monotonic `seq` as the never-compared-before last tiebreak, so payloads are
never ordered (SCHED-1, `docs/blueprint/phase0.md` §1). rot.js's bare `_time`
key is the named collision hazard the 3-tuple fixes; KeeperRL's
players-before-nonplayers discipline collapses into the sub_order bands.
"""

from __future__ import annotations

import heapq
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import count
from typing import Any, Final, Literal

__all__ = [
    "NPC_REACTION",
    "PLAYER_INTENT",
    "QueueEntry",
    "QueueKind",
    "EventQueue",
    "SCHEDULED",
    "SYSTEM_PASS",
]

# sub_order bands (SCHED-1): system passes (0-99) < player intents (100s)
# < NPC reactions (200s) < scheduled completions (300s). Within a band,
# actor_id orders.
SYSTEM_PASS: Final[int] = 0
PLAYER_INTENT: Final[int] = 100
NPC_REACTION: Final[int] = 200
SCHEDULED: Final[int] = 300

QueueKind = Literal["intent", "completion", "pass", "follow_up"]


@dataclass(frozen=True, slots=True)
class QueueEntry:
    """One queue item. Ordering key: (tick, sub_order, actor_id, seq)."""

    tick: int
    sub_order: int
    actor_id: str
    seq: int
    kind: QueueKind
    payload: Any  # IntentData | CompletionPayload (core/loop.py)


class EventQueue:
    """heapq-driven scheduler; push during pops is safe (deterministic)."""

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, str, int, QueueEntry]] = []
        self._seq = count()

    def __len__(self) -> int:
        return len(self._heap)

    def push(self, tick: int, sub_order: int, actor_id: str, kind: QueueKind,
             payload: Any) -> QueueEntry:
        """Enqueue one entry; `seq` makes the key a total order."""
        if tick < 0:
            raise ValueError(f"tick must be non-negative, got {tick}")
        entry = QueueEntry(
            tick=tick, sub_order=sub_order, actor_id=actor_id,
            seq=next(self._seq), kind=kind, payload=payload,
        )
        heapq.heappush(self._heap, (tick, sub_order, actor_id, entry.seq, entry))
        return entry

    def pop(self) -> QueueEntry:
        """Pop the next entry in (tick, sub_order, actor_id, seq) order."""
        if not self._heap:
            raise IndexError("pop from an empty queue")
        return heapq.heappop(self._heap)[4]

    def peek_tick(self) -> int | None:
        """Tick of the head entry (None when empty); non-advancing."""
        return self._heap[0][0] if self._heap else None

    def __iter__(self) -> Iterator[QueueEntry]:
        """Snapshot iteration in key order (tests/inspection; not the run path)."""
        ordered = sorted(self._heap, key=lambda item: item[:4])
        return iter(item[4] for item in ordered)
