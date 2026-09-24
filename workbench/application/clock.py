"""The clock contract (wb-3, the app spec §17 — the family's third
row).

The law: **clock domains are separated — the right clock for the
right question, never one time source everywhere.**

```text
CanonSim semantic time → simulation meaning/determinism ;
monotonic clock        → deadline/timeout/retry/duration ;
UTC/wall observation   → display/persistence timestamps where needed ;
UI animation time      → visual only
```

`CLOCK_DOMAINS` is the closed four-domain vocabulary. This module
provides providers for exactly TWO of them — the ones the
application's own mechanics need:

- MONOTONIC — `AppClock.now_monotonic()`: the deadline/timeout/
  retry/duration source (§12 later composes OperationContext's
  `started_monotonic`/`deadline_monotonic` from it — one absolute
  deadline per logical operation on THIS clock);
- UTC_WALL — `AppClock.now_utc()`: the display/persistence
  observation source.

The other two domains are named and NOT provided:

- SEMANTIC — CanonSim semantic time (ticks) is the ENGINE's own
  (the log's tick axis, INV-2's no-wall-clock law); this module
  must not fabricate a second semantic time source, and no value
  from any clock here may enter CanonSim deterministic state,
  canonical replay or request identity (§17's hard sentence — the
  artifact module imports nothing from here, and its byte-identical
  rebuild is the executable proof);
- UI_ANIMATION — visual-only time belongs to the presentation side
  (the Redot project's own clocks), never to application policy.

`AppClock` is injectable: the composition root (§6.1) wires the
stdlib providers (the defaults); tests wire deterministic doubles —
the same law as the engine's seeded streams, read-side edition:
time-dependent APPLICATION behavior must be testable without
waiting on or trusting the host clock. The providers must be
monotonic-nondecreasing and callable; the frozen holder keeps a
wired clock from being silently swapped under a running operation.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

#: The closed clock-domain vocabulary (§17's four lines).
CLOCK_DOMAINS: frozenset[str] = frozenset(
    {"SEMANTIC", "MONOTONIC", "UTC_WALL", "UI_ANIMATION"}
)

#: The domains THIS module provides providers for (the other two
#: are named-only: SEMANTIC is the engine's own tick axis, never
#: sourced here; UI_ANIMATION is the presentation side's own).
PROVIDED_DOMAINS: frozenset[str] = frozenset({"MONOTONIC", "UTC_WALL"})

#: Provider signature: a zero-argument callable returning a float.
ClockProvider = Callable[[], float]


class ClockError(ValueError):
    """A clock-contract violation (construction-time, never
    silent)."""


def _check_provider(domain: str, provider: object) -> None:
    if not callable(provider):
        raise ClockError(
            f"clock: {domain} provider must be callable "
            f"(got {type(provider).__name__})"
        )


@dataclass(frozen=True)
class AppClock:
    """The application's two wired clocks (monotonic + UTC wall),
    injectable for deterministic tests.

    Defaults are the stdlib providers (`time.monotonic`,
    `time.time`) — real time for the running application, swapped
    for doubles in tests. Frozen: a wired clock is not silently
    replaced mid-operation (a restart composes a new AppClock, it
    never mutates one).
    """

    monotonic: ClockProvider = field(default=time.monotonic)
    utc: ClockProvider = field(default=time.time)

    def __post_init__(self) -> None:
        _check_provider("MONOTONIC", self.monotonic)
        _check_provider("UTC_WALL", self.utc)

    def now_monotonic(self) -> float:
        """The deadline/timeout/retry/duration domain (§12's future
        OperationContext reads here — one absolute deadline per
        logical operation, retries never extend it)."""
        return self.monotonic()

    def now_utc(self) -> float:
        """The display/persistence observation domain — timestamps
        for humans and stores, NEVER for CanonSim deterministic
        state, canonical replay or request identity (§17)."""
        return self.utc()
