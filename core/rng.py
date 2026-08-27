"""RngBank: the single point of randomness control (INV-2, RNG-1, D-028).

One master seed; named streams deterministically derived via
`stable_hash(f"{seed}:{stream}")` — sha256-based, environment-independent
(never relies on PYTHONHASHSEED). Phase-0 streams: `substantive` (canon) and
`cosmetic` (render-only). All draws flow through the bank, which counts them
per stream; the substantive counter is the replay fingerprint T1 compares.
Guards (donor discipline, `docs/blueprint/phase0.md` §1):

- `assure(name)` — run a scope with `name` as the active stream (Brogue
  `assureCosmeticRNG`); nesting a *different* stream inside an assured scope
  raises immediately: a wrong-stream draw is loud, never silent.
- `audit(name)` — assert zero draws on `name` inside the scope (DCSS
  `ASSERT_stable`); the test-side assertion.
- `peek(name)` — non-advancing read of the next float (tests only).

A draw outside any `assure` scope goes to the default active stream:
`substantive` (canon is the default; render paths must assure cosmetic).
"""

from __future__ import annotations

import hashlib
import random
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from typing import Final

__all__ = ["COSMETIC", "PHASE0_STREAMS", "SUBSTANTIVE", "RngBank", "RngError", "stable_hash"]

SUBSTANTIVE: Final = "substantive"
COSMETIC: Final = "cosmetic"
PHASE0_STREAMS: Final = (SUBSTANTIVE, COSMETIC)


class RngError(RuntimeError):
    """INV-2 violation: wrong-stream draw or an audit-scope draw leak."""


def stable_hash(text: str) -> int:
    """Environment-independent 64-bit hash: sha256, first 8 bytes, big-endian."""
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")


class RngBank:
    """Holds every named stream; the only door to entropy (L5)."""

    def __init__(self, seed: int, streams: Iterable[str] = PHASE0_STREAMS) -> None:
        self._seed = int(seed)
        self._streams: dict[str, random.Random] = {}
        self._counts: dict[str, int] = {}
        self._active: str = SUBSTANTIVE
        self._assured: str | None = None
        for name in streams:
            self._register(name)

    @property
    def seed(self) -> int:
        return self._seed

    @property
    def active(self) -> str:
        """The stream draws currently route to."""
        return self._active

    def _register(self, name: str) -> None:
        if name in self._streams:
            raise RngError(f"duplicate stream {name!r}")
        self._streams[name] = random.Random(stable_hash(f"{self._seed}:{name}"))
        self._counts[name] = 0

    def _rng(self, name: str) -> random.Random:
        if name not in self._streams:
            raise RngError(f"unknown stream {name!r} (known: {sorted(self._streams)})")
        return self._streams[name]

    def count(self, name: str = SUBSTANTIVE) -> int:
        """Draws taken from `name` so far."""
        return self._counts[name]

    @property
    def fingerprint(self) -> int:
        """Replay fingerprint: the substantive draw count (RNG-1)."""
        return self._counts[SUBSTANTIVE]

    @contextmanager
    def assure(self, name: str) -> Iterator[None]:
        """Scope with `name` active; a nested different stream is an error."""
        self._rng(name)
        if self._assured is not None and self._assured != name:
            raise RngError(
                f"cannot assure {name!r} inside an assured {self._assured!r} scope"
            )
        prev_active, prev_assured = self._active, self._assured
        self._active, self._assured = name, name
        try:
            yield
        finally:
            self._active, self._assured = prev_active, prev_assured

    @contextmanager
    def audit(self, name: str = SUBSTANTIVE) -> Iterator[None]:
        """Assert zero draws on `name` inside the scope (DCSS ASSERT_stable)."""
        self._rng(name)  # fail fast on unknown stream names
        before = self._counts[name]
        try:
            yield
        except BaseException:
            raise
        else:
            drawn = self._counts[name] - before
            if drawn:
                raise RngError(f"{drawn} draw(s) on stream {name!r} inside audit scope")

    def peek(self, name: str = SUBSTANTIVE) -> float:
        """Next float of `name` without advancing it (tests only)."""
        rng = self._rng(name)
        state = rng.getstate()
        try:
            return rng.random()
        finally:
            rng.setstate(state)

    # -- draw surface (the only advancing operations) -----------------------

    def randint(self, lo: int, hi: int) -> int:
        """Inclusive integer draw from the active stream."""
        self._counts[self._active] += 1
        return self._streams[self._active].randint(lo, hi)

    def random(self) -> float:
        """Float draw from the active stream."""
        self._counts[self._active] += 1
        return self._streams[self._active].random()
