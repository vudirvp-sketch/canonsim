"""The scene manager (scene-1, phase 4 — the chorus queue; architecture
owner `docs/blueprint/phases.md` §1/§4, contract owner `docs/BRIEF_SPEC.md`
§3.9/§6).

The chorus is a **queue, not a convention**: which NPCs may speak in a
beat is a deterministic fold over (log, pack), never a hardcoded rule
about who talks. `speaking_queue` is that fold:

- **presence-gated** — only NPCs structurally present at the current
  scene's location (`core.fold.present_in_order`, a projection read);
- **pack-gated** — an NPC carries a `brief.actors` entry or it is not
  chorus-eligible (the pack's own declaration is the gate, the DORMANT
  family precedent: a pack without the block has an empty chorus and
  runs byte-identically, INV-3);
- **kind-gated** — the player is never queued (mode A owns its call;
  this queue is mode B's), ambient groups are never queued (the knower
  gate: an ambient group holds records but does not speak, the
  leverage-knower law's sibling);
- **ordered** — pack declaration order (INV-2 construction order, never
  a set);
- **capped** — `brief.chorus.max_actor_calls` per beat: the mediator
  drains the queue head-first, one NPC per call, and the NPCs beyond
  the cap fall to the L12 template rung (their beats already render
  through the chronicle — the deterministic prose of phase 0; never a
  blocked beat, never a silent drop).

Pure: reads (events, pack), writes nothing (INV-1); no RNG, no
wall-clock (INV-2); no LLM, no network (INV-4). The session-loop
wiring — when the chorus fires inside the beat cycle and how actor
replies feed the door — is the next row (TASKS `scene-2`); this module
is the law the wiring will obey.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from brief.ledger import current_scene
from core.fold import fold, initial_projection, present_in_order
from core.log import EventRecord

if TYPE_CHECKING:  # pack is a duck-typed argument — no runtime cycle
    from core.pack import Pack

__all__ = ["speaking_queue"]


def speaking_queue(events: Sequence[EventRecord], pack: "Pack") -> tuple[str, ...]:
    """The beat's chorus queue: the present, pack-declared NPCs at the
    current scene's location, pack declaration order, capped by the
    per-beat actor-call budget (BRIEF_SPEC §3.9). Empty when the pack
    declares no `brief.chorus` block (the pack's own declaration is the
    gate — mode B off, byte-identical runs)."""
    config = pack.rules["brief"].get("chorus")
    if config is None:
        return ()
    cap = int(config["max_actor_calls"])
    if cap <= 0:
        return ()  # belt-and-braces: the lint already refuses this
    scene = current_scene(events, pack)
    state = fold(events, initial_projection(pack.entities))
    actors = pack.rules["brief"].get("actors", {})
    player = pack.player_id()
    return tuple(
        entity_id
        for entity_id in present_in_order(pack, state, scene.location_id)
        if entity_id != player
        and pack.kind_of(entity_id) == "npc"
        and entity_id in actors
    )[:cap]
