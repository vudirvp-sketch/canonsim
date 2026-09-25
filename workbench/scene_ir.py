"""The Visual Scene IR — the renderer-neutral read-side contract
(wb-1, CONTRACTS §5 D2/D5; the v5.2 brief's §7/§23 vocabulary).

What this is: a typed, deterministic, engine-independent document that
describes ONE scene's visual composition from CanonSim semantic
products. Redot (or any future renderer) consumes it; nothing in it
may leak renderer types (no Node/Texture/UID as identity), and the
semantic statuses are never silently collapsed — UNKNOWN never becomes
ABSENT, HIDDEN never becomes ABSENT, VISUAL never becomes CANONICAL.

Determinism law (D4): the same inputs produce byte-identical JSON —
`json.dumps(..., sort_keys=True, separators=(",", ":"))`, floats
rounded to `COORD_DECIMALS`, lists in construction order. No wall
clock, no PYTHONHASHSEED dependence (the sha256 `stable_hash`, the
one hash implementation — reached through the canonical read seam
`workbench/canonical_read.py`, ssi-6/D-228; this module holds no
core/ import of its own).

Identity closure (the v5.2 brief's §23.1): a scene is reproducible
only when the semantic input AND the composition material are pinned —
`scene_identity = digest(semantic_input_identity + composition_seed +
asset_manifest_identity + composition_policy_version +
scene_ir_schema_identity + source_revision)`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from workbench.canonical_read import stable_hash

#: The IR's own schema identity — bumps on any breaking shape change
#: (the same discipline as the event schema's `schema_version`).
SCHEMA_IDENTITY = "canon_scene_ir@0.1"

#: The composition policy version — the placement/variant algorithm's
#: identity (a placement change bumps this, not the schema).
COMPOSITION_POLICY_VERSION = "composition@0.1"

#: The placeholder asset manifest identity (wb-1 has no real assets —
#: the vocabulary is code-drawn placeholders; a real manifest lands at
#: its own wb row).
ASSET_MANIFEST_IDENTITY = "manifest.placeholder@0.1"

#: The IR coordinate space (the compositor maps this to its viewport).
COORDINATE_SPACE: tuple[int, int] = (1280, 720)

#: Float rounding for stable serialization across platforms.
COORD_DECIMALS = 3

#: The semantic-status vocabulary (CONTRACTS §5 D5 — the closed enum).
STATUSES: frozenset[str] = frozenset(
    {"CANONICAL", "DERIVED", "OBSERVED", "UNKNOWN", "HIDDEN", "VISUAL"}
)

#: Draw order, coarsest first (the layer list is the compositor's law).
LAYERS: tuple[str, ...] = ("background", "stage", "props", "actors", "overlays")

#: The observation profile vocabulary (the brief's §29 — wb-1 ships the
#: canon view; the perception/assurance/debug views land at their rows).
OBSERVATION_PROFILES: frozenset[str] = frozenset(
    {"CANON_VIEW", "PERCEPTION_VIEW", "ASSURANCE_VIEW", "DEBUG_VIEW"}
)


class SceneIRError(ValueError):
    """A malformed IR document (construction-time, never silent)."""


def _round(value: float) -> float:
    return round(float(value), COORD_DECIMALS)


@dataclass(frozen=True)
class Instance:
    """One visual instance: what to draw, where, on which layer — and
    the semantic status + provenance that keep it honest."""

    asset_id: str
    position: tuple[float, float]
    layer: str
    semantic_status: str
    provenance: str | None = None
    variant_id: str = "v0"
    rotation: float = 0.0
    scale: float = 1.0
    visibility: bool = True
    animation_state: str = "idle"
    palette_variant: str = "p0"

    def __post_init__(self) -> None:
        if not self.asset_id:
            raise SceneIRError("instance: empty asset_id")
        if self.semantic_status not in STATUSES:
            raise SceneIRError(
                f"instance {self.asset_id}: unknown semantic_status "
                f"{self.semantic_status!r} (closed enum: {sorted(STATUSES)})"
            )
        if self.layer not in LAYERS:
            raise SceneIRError(
                f"instance {self.asset_id}: unknown layer {self.layer!r} "
                f"(closed enum: {list(LAYERS)})"
            )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "animation_state": self.animation_state,
            "asset_id": self.asset_id,
            "layer": self.layer,
            "palette_variant": self.palette_variant,
            "position": [_round(self.position[0]), _round(self.position[1])],
            "provenance": self.provenance,
            "rotation": _round(self.rotation),
            "scale": _round(self.scale),
            "semantic_status": self.semantic_status,
            "variant_id": self.variant_id,
            "visibility": self.visibility,
        }


@dataclass(frozen=True)
class Camera:
    """Presentation camera — explicitly NOT a canonical fact (the brief's
    §28: semantic focus ≠ presentation camera ≠ user camera state; wb-1
    pins the presentation camera only, the user layer comes later)."""

    mode: str = "LOCAL_SCENE"
    focus: tuple[float, float] = (
        COORDINATE_SPACE[0] / 2.0,
        COORDINATE_SPACE[1] / 2.0,
    )
    zoom: float = 1.0

    def to_mapping(self) -> dict[str, Any]:
        return {
            "focus": [_round(self.focus[0]), _round(self.focus[1])],
            "mode": self.mode,
            "zoom": _round(self.zoom),
        }


@dataclass(frozen=True)
class Overlay:
    """A text overlay (debug/assurance state — the brief's §29 assurance
    vocabulary; wb-1 ships the debug line)."""

    kind: str
    text: str
    position: tuple[float, float]
    semantic_status: str = "DERIVED"

    def __post_init__(self) -> None:
        if self.semantic_status not in STATUSES:
            raise SceneIRError(f"overlay: unknown status {self.semantic_status!r}")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "position": [_round(self.position[0]), _round(self.position[1])],
            "semantic_status": self.semantic_status,
            "text": self.text,
        }


@dataclass(frozen=True)
class Scene:
    """The whole scene document — identity closure + composition."""

    semantic_input_identity: str
    source_revision: str
    composition_seed: int
    background: Mapping[str, Any]
    actors: tuple[Instance, ...] = ()
    props: tuple[Instance, ...] = ()
    effects: tuple[Mapping[str, Any], ...] = ()
    overlays: tuple[Overlay, ...] = ()
    camera: Camera = field(default_factory=Camera)
    observation_profile: str = "CANON_VIEW"

    def __post_init__(self) -> None:
        if self.observation_profile not in OBSERVATION_PROFILES:
            raise SceneIRError(
                f"scene: unknown observation_profile {self.observation_profile!r}"
            )
        if self.background.get("semantic_status") not in STATUSES:
            raise SceneIRError("scene.background: missing/unknown semantic_status")

    @property
    def scene_identity(self) -> str:
        """The v5.2 composition identity — the digest over the full
        closure (semantic input + seed + manifest + policy + schema +
        source revision)."""
        material = (
            f"{self.semantic_input_identity}:{self.composition_seed}:"
            f"{ASSET_MANIFEST_IDENTITY}:{COMPOSITION_POLICY_VERSION}:"
            f"{SCHEMA_IDENTITY}:{self.source_revision}"
        )
        return f"sha256:{stable_hash(material):016x}"

    def to_mapping(self) -> dict[str, Any]:
        return {
            "actors": [i.to_mapping() for i in self.actors],
            "asset_manifest_identity": ASSET_MANIFEST_IDENTITY,
            "background": dict(self.background),
            "camera": self.camera.to_mapping(),
            "composition_policy_version": COMPOSITION_POLICY_VERSION,
            "composition_seed": self.composition_seed,
            "coordinate_space": [COORDINATE_SPACE[0], COORDINATE_SPACE[1]],
            "effects": [dict(e) for e in self.effects],
            "layers": list(LAYERS),
            "observation_profile": self.observation_profile,
            "overlays": [o.to_mapping() for o in self.overlays],
            "props": [i.to_mapping() for i in self.props],
            "scene_identity": self.scene_identity,
            "scene_ir_schema_identity": SCHEMA_IDENTITY,
            "semantic_input_identity": self.semantic_input_identity,
            "source_revision": self.source_revision,
        }

    def to_json(self) -> str:
        """The deterministic serialization (D4: sort_keys + fixed
        separators + rounded floats; byte-identical on rebuild)."""
        return json.dumps(
            self.to_mapping(), sort_keys=True, separators=(",", ":")
        )


def instance_from_mapping(data: Mapping[str, Any]) -> Instance:
    """Parse one instance mapping (the Redot side's JSON round-trip
    check; strict — an unknown field is a schema drift, loud)."""
    known = set(Instance.__dataclass_fields__)
    unknown = set(data) - known
    if unknown:
        raise SceneIRError(f"instance: unknown fields {sorted(unknown)}")
    pos = data["position"]
    return Instance(
        asset_id=str(data["asset_id"]),
        position=(float(pos[0]), float(pos[1])),
        layer=str(data["layer"]),
        semantic_status=str(data["semantic_status"]),
        provenance=data.get("provenance"),
        variant_id=str(data.get("variant_id", "v0")),
        rotation=float(data.get("rotation", 0.0)),
        scale=float(data.get("scale", 1.0)),
        visibility=bool(data.get("visibility", True)),
        animation_state=str(data.get("animation_state", "idle")),
        palette_variant=str(data.get("palette_variant", "p0")),
    )


def palette_pick(key: str, palette: Sequence[str]) -> str:
    """Deterministic palette variant: the stable hash picks, never a
    random draw (D4 — no RNG anywhere in the Python half)."""
    return palette[stable_hash(key) % len(palette)]
