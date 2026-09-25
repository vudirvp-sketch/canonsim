"""The canonical read seam (Phase 5/ssi-6, D-228): the ONE workbench
module that imports core/ — the narrow read API every other workbench
module reaches CanonSim's read products through (INV-4's
sanctioned-module pattern, «exactly N modules», applied to the
core-read boundary instead of the network boundary).

What this is: a PURE re-export shell over the canonical read surface
the workbench read-side actually consumes — nothing more, nothing
re-implemented (D-024's one-owner law: the semantic homes stay
core/log.py, core/fold.py, core/pack.py, core/rng.py; this module
owns only the EDGE, never a second copy of anything). The pinned
surface, `__all__`:

- ``core.log``   — read_log, validate_header, EventRecord, LogError
- ``core.fold``  — fold, initial_projection, present_in_order
- ``core.pack``  — load_pack, PackError
- ``core.rng``   — stable_hash

The laws this seam carries:

1. Read-only. Zero canon writes ride here — the log writer stays the
   only canon-write path (INV-1's privilege separation); a workbench
   module never gains a write arm by importing through this seam.
2. One edge. ``workbench/`` imports core/ EXACTLY HERE — enforced by
   tests/test_architecture.py (a core import anywhere else in
   workbench/ goes RED) and drift-pinned by scripts/topology.py
   --check (this module rides the map's watchlist: its reads cell is
   hard-pinned, so the surface grows DELIBERATELY — a map update in
   the same iteration, never silently).
3. Bounded consumers. The map names them: scene_build.py (the scene
   read model — fold/log/pack/rng), observatory_read.py (the
   Observatory read model — log), scene_ir.py (the Scene IR — rng).
   A fourth consumer joins by importing this module, never core/.

Scope note: ``scripts/`` (the offline operator graph, D-046) and
``render/`` (the chronicle read-side) keep their direct core imports
by design — periphery, outside the workbench app layer this seam
bounds (the map's §0 scope law).
"""

from __future__ import annotations

from core.fold import fold, initial_projection, present_in_order
from core.log import EventRecord, LogError, read_log, validate_header
from core.pack import PackError, load_pack
from core.rng import stable_hash

__all__ = [
    "EventRecord",
    "LogError",
    "PackError",
    "fold",
    "initial_projection",
    "load_pack",
    "present_in_order",
    "read_log",
    "stable_hash",
    "validate_header",
]
