"""The one exits read (roads-1, `docs/CONTRACTS.md` §1 D3; iter-104's
read-path law, the owner's combined-variant call): every runtime consumer
of a location's adjacency reads through THIS function — never the pack
record's `exits` key directly, never the WorldModel's derived graph
directly.

THE OVERRIDE ORDER (the pack-wins law):

1. The AUTHORED record wins when declared: a location whose entities.json
   `exits` list is NON-EMPTY reads exactly that list (authored packs keep
   manual exits; the load-time entities lint — symmetric, orphan-free —
   stays the authored half's single owner, unchanged by roads-1). The
   entities lint requires an `exits` list on every location, so "an
   empty list" is the generated-world marker — a mode G pack cannot
   hand-author seed-dependent edges (the row's own premise), it declares
   the empty list and the pass fills the graph.
2. Else the PASS-DERIVED edges: the roads pass's location-to-location
   graph (`core/worldgen.py::_pass_roads`, the MST backbone + the
   pack-declared k-nearest overlay) read off the WorldModel — derived,
   rebuildable, never truth (L11: a pure function of the header seed +
   pack). Unclaimed locations and unarmed worlds read the empty tuple
   (the 68a pattern: nothing is invented where nothing was declared).

Read-side only (INV-1 untouched): the read answers a fold-time question
and writes nothing; the derived graph carries no canon births. The
runtime consumers (the LOD warm ring, the intent door's move validation,
the autonomy doors' precondition folds) all hold the WorldModel the
loop re-derives at open/resume; callers without a world (tests, unarmed
packs) pass None and read the authored half alone — correct because the
committed packs author non-empty exits everywhere.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # duck-typed arguments — no runtime cycle either way
    from core.pack import Pack
    from core.worldgen import WorldModel

__all__ = ["exits"]


def exits(pack: "Pack", world: "WorldModel | None", location: str) -> tuple[str, ...]:
    """The effective exits of `location` (the one shared read): the
    authored record when non-empty (the pack wins), else the pass-derived
    edges (the roads graph on the WorldModel), else the empty tuple (an
    unclaimed location, or an unarmed world). Deterministic by
    construction — both halves are ordered data (the authored list's own
    order, the derived list's I5 edge order; INV-2)."""
    record = pack.entity(location)
    authored = record.get("exits") if record is not None else None
    if authored:
        return tuple(authored)
    if world is None:
        return ()
    for claimed, derived in world.roads:
        if claimed == location:
            return derived
    return ()
