"""The scene LOD (depth-3, phases.md §5 — three zones): the simulation's
relevance discipline, the D-112 write-side law at scene scale. The zone
partition is a PURE function of (pack, projection) — the pack's location
graph (the `exits` adjacency, linted symmetric) and the PC's live
position:

- **ACTIVE** — the PC's location: its NPCs tick per-beat (the beat
  machinery as today);
- **WARM** — the adjacent locations (the active location's exits, the
  pack's own declaration order): their NPCs tick at the MACRO
  CROSSINGS only — the scheduler rule (INV-2-clean: the crossings are
  the positive multiples of the pack-declared `time.macro.cadence_ticks`,
  `core/macro.py`'s arithmetic — pure tick math, never entropy; the
  warm cadence is one clock with the calendar, never a second
  declaration);
- **COLD** — everything else: its NPCs never tick per-NPC; the zone
  rides the macro turn's AGGREGATE alone — the census count under
  `COLD_COUNT_KEY` (the D-112 shape: counts for populations, events
  for notables; log growth O(active + warm/cadence + aggregates), the
  long-history fear bounded by construction).

The ONE-GATE law: the LOD engages exactly when the macro clock is
ARMED (`time.macro` declared). The unarmed law is the one-scene world
— the whole simulation ticks per-beat, the v0.1 bytes untouched (the
68a pattern; the committed pack's arming rides with the macro clock's
first consumer). No new pack vocabulary: the zones derive from `exits`
+ the position fold, the cadence from `time.macro`, the census from
the projection (L3: derived, never stored).

Determinism (INV-2): construction order everywhere — the warm tuple
follows the exits list's own order, the cold tuple the pack's location
declaration order; never a set iteration.
"""

from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from core.fold import Projection

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle
    from core.pack import Pack

__all__ = [
    "COLD_COUNT_KEY",
    "LodError",
    "SceneZones",
    "npc_population",
    "scene_zones",
]

#: The cold census's outcome key on the macro turn (the flat-keys
#: family: the template binding surface). The engine's own mechanical
#: vocabulary — the `year` / `participants` / `places` family, never a
#: domain word (INV-3); a pack's template may bind it (the reachability
#: law is the template's own business, as for `year`).
COLD_COUNT_KEY: Final = "cold_npcs"


class LodError(ValueError):
    """A scene-LOD contract failure (the pred-contract family, D-111:
    a raw read that cannot be answered fails LOUD, never a KeyError)."""


@dataclass(frozen=True, slots=True)
class SceneZones:
    """The three zones at one tick: the active scene (the PC's
    location), the warm ring (its exits, pack declaration order), and
    the cold background (the remaining locations, pack declaration
    order). Read-side derived state — a pure fold view, never logged."""

    active: str
    warm: tuple[str, ...]
    cold: tuple[str, ...]


def scene_zones(pack: "Pack", projection: Projection) -> SceneZones:
    """The zone partition (a pure function of the pack's exits graph +
    the PC's live position). The warm ring is the ACTIVE location's
    exits — the pack's own order, self-exits and duplicates filtered
    (belt-and-braces: the lint guarantees declared, symmetric targets);
    the cold background is the remaining locations in declaration
    order (INV-2: construction order, never a set)."""
    player = pack.player_id()
    props = projection.get(player)
    if props is None:
        raise LodError(
            f"the player {player!r} is absent from the projection — "
            "the zone partition reads the live fold (the "
            "pred-contract family, D-111)"
        )
    active = props.get("position")
    record = pack.entity(active) if isinstance(active, str) else None
    if record is None:
        raise LodError(
            f"the player {player!r} stands at {active!r} — not a "
            "declared location; the zone partition reads the exits "
            "graph (the pred-contract family, D-111)"
        )
    warm: list[str] = []
    for exit_id in record.get("exits", ()):
        if exit_id == active or exit_id in warm:
            continue  # a self-exit or a duplicate: never ring members
        warm.append(exit_id)
    cold = tuple(
        loc["id"]
        for loc in pack.entities["locations"]
        if loc["id"] != active and loc["id"] not in warm
    )
    return SceneZones(active=active, warm=tuple(warm), cold=cold)


def npc_population(
    pack: "Pack", projection: Projection, locations: Collection[str]
) -> int:
    """The NPC population positioned in `locations` (the census read:
    kind-`npc` entities alone — ambient groups never tick, so the LOD
    silences nothing of theirs; items are not souls). Derived from the
    projection at the reading tick (L3), recorded on the turn (INV-1)
    — never stored."""
    return sum(
        1
        for npc in pack.entities["npcs"]
        if projection.get(npc["id"], {}).get("position") in locations
    )
