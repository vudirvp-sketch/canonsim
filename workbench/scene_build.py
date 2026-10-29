"""The scene read model (wb-1, CONTRACTS §5 D2/D3): a committed log
folded into the scene at one location — the Visual Scene IR's semantic
source.

The law here is reuse, not invention: `read_log` + `fold` +
`present_in_order` are the ONE presence/canon laws (the
render/chronicle.py read-side pattern); this module only projects what
they already answer — reached through the canonical read seam
(`workbench/canonical_read.py`, ssi-6/D-228 — this module holds no
core/ import of its own). Zero canon writes, zero network, zero RNG —
the deterministic placement rides `stable_hash` and construction order
(INV-2's read-side discipline).

Composition (wb-1's placeholder policy, `COMPOSITION_POLICY_VERSION`):
a flat two-tone background + a baseline row of actor placeholders + a
shelf row of prop placeholders — positions spread evenly across the
IR coordinate space, palette/variant picked by stable hash. No
per-instance hand placement anywhere (the brief's §33 agent-first
law); a real asset vocabulary is a later wb row's material.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from workbench.canonical_read import (
    EventRecord,
    PackError,
    fold,
    initial_projection,
    load_pack,
    present_in_order,
    read_log,
    stable_hash,
)
from workbench.scene_ir import (
    COORDINATE_SPACE,
    Camera,
    Instance,
    Overlay,
    Scene,
    palette_pick,
)

#: The repository's machine-readable event schema (the read_log
#: validation input — the same file every reader uses).
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "event.schema.json"

#: Actor/prop placeholder sizes (IR units — the compositor scales).
ACTOR_SIZE: tuple[float, float] = (64.0, 96.0)
PROP_SIZE: tuple[float, float] = (48.0, 48.0)

#: The placement bands (x margins + row centers, top-left coordinates).
ACTOR_MARGIN_X = 240.0
ACTOR_ROW_Y = 470.0
PROP_MARGIN_X = 320.0
PROP_ROW_Y = 280.0

#: The placeholder palettes (muted, high-silhouette — the brief's §32
#: visual language; presentation data, never semantic).
ACTOR_PALETTE: tuple[str, ...] = (
    "#d9a066", "#8fb3a9", "#c37b5d", "#a68db5", "#9db87d",
)
PROP_PALETTE: tuple[str, ...] = ("#7d95b5", "#b58f7d", "#8d9db5", "#b5a27d")
BG_PALETTE: tuple[str, ...] = ("#1c2128", "#232a33", "#2a2420")
FLOOR_PALETTE: tuple[str, ...] = ("#2d333b", "#343b44", "#3b352c")

#: The kinds drawn as actors / props; every other kind (locations,
#: groups) is not a scene instance at this tier — skipped honestly,
#: never silently relabeled.
ACTOR_KINDS = frozenset({"npc", "ambient"})
PROP_KINDS = frozenset({"item"})


def _spread(margin: float, size: float, count: int) -> list[float]:
    """Even, deterministic slot centers across the placement band."""
    width = float(COORDINATE_SPACE[0])
    if count <= 0:
        return []
    if count == 1:
        return [(width - size) / 2.0]
    step = (width - 2.0 * margin - size) / float(count - 1)
    return [margin + i * step for i in range(count)]


def _identity(events: Sequence[EventRecord], header: Mapping[str, Any]) -> str:
    """The semantic input identity: a stable digest over the pack+seed
    and every (event id, event type) pair — two logs that differ in
    ANY event differ here (the fixture's provenance, never a path)."""
    material = [f"{header.get('pack', '?')}@{header.get('seed', '?')}"]
    material.extend(f"{e.id}:{e.type}" for e in events)
    joined = "\n".join(material)
    return f"sha256:{stable_hash(joined):016x}"


def _default_location(pack: Any, state: Mapping[str, Mapping[str, Any]]) -> str:
    """The player's location when the caller pins none; a pack without
    a positioned player falls back to the densest location (ties →
    sorted first — pure function of the projection, no pack words)."""
    try:
        player = pack.player_id()
    except PackError:  # no is_player npc in this pack
        player = None
    if player is not None:
        position = state.get(player, {}).get("position")
        if isinstance(position, str):
            return position
    counts: dict[str, int] = {}
    for props in state.values():
        position = props.get("position")
        if isinstance(position, str):
            counts[position] = counts.get(position, 0) + 1
    if not counts:
        return ""
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def build_scene(
    log_path: Path, pack_dir: Path, location: str | None = None
) -> Scene:
    """Fold a committed log and compose the scene at one location.

    The scene is a pure function of (log, pack, location): same inputs
    → byte-identical `Scene.to_json()` (CONTRACTS §5 D4).
    """
    pack = load_pack(pack_dir)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    header, events = read_log(log_path, schema)
    state = fold(events, initial_projection(pack.entities))

    last_tick = events[-1].t if events else 0
    last_id = events[-1].id if events else "none"
    scene_location = location or _default_location(pack, state)
    present = present_in_order(pack, state, scene_location) if scene_location else ()

    actors: list[Instance] = []
    props: list[Instance] = []
    for entity_id in present:
        kind = pack.kind_of(entity_id)
        if kind in ACTOR_KINDS:
            actors.append(entity_id)
        elif kind in PROP_KINDS:
            props.append(entity_id)

    actor_instances: list[Instance] = []
    for slot, entity_id in enumerate(actors):
        jitter = stable_hash(f"{entity_id}:jitter") % 17 - 8
        actor_instances.append(
            Instance(
                asset_id="actor.silhouette",
                position=(
                    _spread(ACTOR_MARGIN_X, ACTOR_SIZE[0], len(actors))[slot],
                    ACTOR_ROW_Y + float(jitter),
                ),
                layer="actors",
                semantic_status="CANONICAL",
                provenance=entity_id,
                palette_variant=palette_pick(entity_id, ACTOR_PALETTE),
            )
        )

    prop_instances: list[Instance] = []
    for slot, entity_id in enumerate(props):
        jitter = stable_hash(f"{entity_id}:jitter") % 13 - 6
        prop_instances.append(
            Instance(
                asset_id="prop.block",
                position=(
                    _spread(PROP_MARGIN_X, PROP_SIZE[0], len(props))[slot],
                    PROP_ROW_Y + float(jitter),
                ),
                layer="props",
                semantic_status="CANONICAL",
                provenance=entity_id,
                palette_variant=palette_pick(entity_id, PROP_PALETTE),
            )
        )

    debug = (
        f"{pack.name_version} seed={header.get('seed')} t={last_tick} "
        f"loc={scene_location or 'none'} "
        f"actors={len(actor_instances)} props={len(prop_instances)} "
        f"events={len(events)}"
    )

    return Scene(
        semantic_input_identity=_identity(events, header),
        source_revision=(
            f"seed={header.get('seed')};events={len(events)};"
            f"last={last_id};tick={last_tick}"
        ),
        composition_seed=stable_hash(
            f"{header.get('seed')}:{last_tick}:{scene_location}"
        ),
        background={
            "kind": "flat",
            "color": palette_pick(f"{scene_location}:bg", BG_PALETTE),
            "floor_color": palette_pick(f"{scene_location}:floor", FLOOR_PALETTE),
            "floor_band": [0.0, 560.0, 1280.0, 160.0],
            "semantic_status": "VISUAL",
        },
        actors=tuple(actor_instances),
        props=tuple(prop_instances),
        overlays=(
            Overlay(kind="debug", text=debug, position=(24.0, 20.0)),
        ),
        camera=Camera(),
    )
