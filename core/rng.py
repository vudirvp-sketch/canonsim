"""RngBank: the single point of randomness control (INV-2, RNG-1, D-028).

One master seed; named streams deterministically derived via
`stable_hash(f"{seed}:{stream}")` — sha256-based, environment-independent
(never relies on PYTHONHASHSEED). Registered streams: `substantive` (canon
checks) and `cosmetic` (render-only); plus six CONTENT-ADDRESSED FAMILIES
of lazily registered streams, whose names are built by the owning module
and pack-linted before any draw — `urgency:<npc>:<kind>` (engine-2,
D-079, `urgency_stream_name`), `drift:<family>` (rumordrift, A2''/
D-099, `drift_stream_name`), `scene:<id>:detail` (lazy detail
materialization, depth-2, `scene_detail_stream_name`),
`worldgen:<pass>` (the ordered worldgen passes, depth-5,
`worldgen_stream_name`), `faction:<group>:<kind>` (the faction
goal rolls, depth-6, `faction_stream_name`), and `name:<npc>` (the
generated names, name-1, `name_stream_name`). All draws flow through the
bank, which counts them per stream; the substantive counter is the
replay fingerprint T1 compares. Guards (donor discipline,
`docs/blueprint/phase0.md` §1):

- `assure(name)` — run a scope with `name` as the active stream (Brogue
  `assureCosmeticRNG`). Nesting a *different* stream inside an assured
  scope raises immediately — EXCEPT the six content-addressed families:
  an urgency-, drift-, scene-, worldgen-, faction-, or name-family
  stream may shadow the assured `substantive` run scope
  (engine-2, rumordrift + lazy detail (depth-2), worldgen (depth-5),
  factions (depth-6), names (name-1)): all are
  canon-relevant but stream-isolated per declared entry, so an added,
  removed, or re-armed pack entry shifts neither a later canon check
  draw nor another entry's roll — the single shared stream was measured
  and refused for urgencies (the entries
  coupled by draw position; D-079); drift, scene detail, the worldgen
  passes, and the generated names inherit the same isolation law
  (D-095: "isolation is
  law"; at pass granularity a re-tuned map config shifts neither a
  canon check draw nor another pass's draws). A wrong-stream draw is
  loud, never silent.
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

__all__ = [
    "COSMETIC",
    "DRIFT_PREFIX",
    "FACTION_PREFIX",
    "FAMILY_PREFIXES",
    "NAME_PREFIX",
    "PHASE0_STREAMS",
    "SCENE_PREFIX",
    "SUBSTANTIVE",
    "URGENCY_PREFIX",
    "WORLDGEN_PREFIX",
    "RngBank",
    "RngError",
    "drift_stream_name",
    "faction_stream_name",
    "name_stream_name",
    "scene_detail_stream_name",
    "stable_hash",
    "urgency_stream_name",
    "worldgen_stream_name",
]

SUBSTANTIVE: Final = "substantive"
COSMETIC: Final = "cosmetic"
URGENCY_PREFIX: Final = "urgency:"
DRIFT_PREFIX: Final = "drift:"
SCENE_PREFIX: Final = "scene:"
WORLDGEN_PREFIX: Final = "worldgen:"
FACTION_PREFIX: Final = "faction:"
NAME_PREFIX: Final = "name:"
PHASE0_STREAMS: Final = (SUBSTANTIVE, COSMETIC)

# The six lazily registered content-addressed families (D-079's law,
# extended by drift, scene detail, the worldgen passes, the faction
# goal rolls, and the generated names): the name-building functions are
# the single owners of each grammar, and the pack lint validates the
# ids inside before any draw.
FAMILY_PREFIXES: Final = (
    URGENCY_PREFIX,
    DRIFT_PREFIX,
    SCENE_PREFIX,
    WORLDGEN_PREFIX,
    FACTION_PREFIX,
    NAME_PREFIX,
)


def urgency_stream_name(npc: str, intent_kind: str) -> str:
    """The per-entry urgency roll stream: content-addressed
    `urgency:<npc>:<kind>` (engine-2, D-079). One stream per pack urgency
    entry — the (npc, kind) pair is pack-linted unique, so the name is
    injective; adding an entry adds a NEW stream and never shifts another
    entry's draws (the add-safety law)."""
    return f"{URGENCY_PREFIX}{npc}:{intent_kind}"


def drift_stream_name(family: str) -> str:
    """The per-family rumor-drift stream: content-addressed
    `drift:<family>` (rumordrift, A2''/D-099). One stream per pack-declared
    `knowledge.drift` family — family ids are map keys, so the name is
    injective; arming, adding, or removing a family shifts neither a canon
    check draw nor another family's rolls (the isolation law, D-095)."""
    return f"{DRIFT_PREFIX}{family}"


def scene_detail_stream_name(location_id: str) -> str:
    """The per-scene lazy-detail stream: content-addressed
    `scene:<id>:detail` (depth-2, `phases.md` §5 — the D-079 family law's
    third member). One stream per pack-declared `scene_detail` location —
    location ids are entities.json map keys, so the name is injective;
    arming a scene's detail block draws from that scene's OWN stream, so
    it shifts neither a canon check draw nor another scene's details
    (the isolation law at stream-address granularity; the within-scene
    slot list is one pack unit — a slot-list edit is a content change,
    D-079's content-landing protocol, its corpus price paid at arming)."""
    return f"{SCENE_PREFIX}{location_id}:detail"


def worldgen_stream_name(pass_name: str) -> str:
    """The per-pass worldgen stream: content-addressed
    `worldgen:<pass>` (depth-5, `phases.md` §5 — the D-079 family law's
    fourth member; the pass names are the closed `PASS_ORDER` vocabulary
    of `core/worldgen.py`, ":"-free and unique, so the name is injective).
    One stream per ordered pass — re-tuning, adding, or removing a pass
    shifts neither a canon check draw nor another pass's draws (the
    isolation law at pass granularity; the corpus price of arming
    worldgen is the genesis events alone, never a moved canon check)."""
    return f"{WORLDGEN_PREFIX}{pass_name}"


def faction_stream_name(group_id: str, intent_kind: str) -> str:
    """The per-entry faction goal-roll stream: content-addressed
    `faction:<group>:<kind>` (depth-6, `phases.md` §5 P3b — the D-079
    family law's fifth member). One stream per pack-declared faction
    entry — the (group, kind) pair is pack-linted unique and group ids
    are entity-unique across categories, so the name is injective;
    adding, removing, or re-tuning a faction shifts neither a canon
    check draw nor another entry's rolls (the isolation law at faction
    granularity — the KeeperRL small formula's odds are the world's own
    derived number, never another stream's draw positions)."""
    return f"{FACTION_PREFIX}{group_id}:{intent_kind}"


def name_stream_name(npc: str) -> str:
    """The per-npc generated-name stream: content-addressed `name:<npc>`
    (name-1, `phases.md` §5 — the D-079 family law's sixth member; the
    scene-detail twin: a lazy per-entity materialization). One stream
    per npc declaring a generated name — npc ids are entity-unique
    across categories, so the name is injective; arming, adding, or
    removing a declaration shifts neither a canon check draw nor
    another npc's name (the isolation law at declaration granularity;
    the birth is first-commit-wins, so a re-tuned profile pays its
    corpus price only on the unborn — canon names are never redrawn)."""
    return f"{NAME_PREFIX}{npc}"


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
            if name.startswith(FAMILY_PREFIXES):
                # engine-2 + rumordrift + lazy detail (depth-2) + the
                # worldgen passes (depth-5) + the faction goal rolls
                # (depth-6) + the generated names (name-1): the six
                # content-addressed stream families register lazily —
                # names built by `urgency_stream_name`
                # / `drift_stream_name` / `scene_detail_stream_name` /
                # `worldgen_stream_name` / `faction_stream_name` /
                # `name_stream_name`, pack-linted before any draw; the
                # closed-set tripwire survives for every non-family
                # name (a typo stays loud).
                self._register(name)
            else:
                raise RngError(
                    f"unknown stream {name!r} (known: {sorted(self._streams)})"
                )
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
        """Scope with `name` active; nesting a foreign stream is an error
        unless the pairing is the content-addressed family law: an
        urgency-, drift-, scene-, worldgen-, faction-, or name-family
        stream may shadow the assured substantive run scope — and
        nothing else may nest anywhere."""
        self._rng(name)
        if (
            self._assured is not None
            and self._assured != name
            and not (
                name.startswith(FAMILY_PREFIXES)
                and self._assured == SUBSTANTIVE
            )
        ):
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
