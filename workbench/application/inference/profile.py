"""The typed profile document + its acceptance laws (ssi-4 step 2,
iter-248 — extracted verbatim from the single-module era).

The §19.1 BASE PROFILE layer's own home (WORKBENCH_APP_LAW owns the
composition chain, the LAW owns the control model): InferenceProfile —
ONE mapping keyed by the library's profile FIELDS plus the ordered
sampler chain; the validation family — the per-control acceptance
(§19.1's ACCEPTED step: rejected LOUD, never a silent clamp, the
value_type/forms/limits ARE the closed vocabulary, data-driven over
the library's own metadata). The persisted document's shape is
field-stable (§15.3: an old profile loads as-is, absent fields take
the library baselines).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from workbench.application.inference.chain import DEFAULT_CHAIN, ChainItem
from workbench.application.inference.library import (
    _CONTROL_INDEX,
    _FIELD_INDEX,
    _FIELDS,
    CONTROL_LIBRARY,
    GPU_LAYER_FORMS,
    SAMPLER_CHAIN_IDS,
    InferenceError,
    SemanticControl,
)

# ---------------------------------------------------------------- the profile


@dataclass(frozen=True)
class InferenceProfile:
    """The typed semantic configuration document — the §19.1 BASE
    PROFILE layer (reusable, persisted, the single semantic owner).
    The values ride ONE mapping keyed by the library's profile
    FIELDS (the inf-1 flat document, unchanged for the original 13
    fields — an old profile loads as-is); the CHAIN holds membership
    + order only (the two are edited together, one document, one
    authority)."""

    name: str = "Baseline"
    values: Mapping[str, object] = field(
        default_factory=lambda: {
            control.field: control.baseline
            for control in CONTROL_LIBRARY
        }
    )
    sampler_chain: tuple[ChainItem, ...] = DEFAULT_CHAIN

    def __post_init__(self) -> None:
        # The chain accepts the WIRE form too (a list of {id, enabled}
        # dicts — the JSON roundtrip's own shape); the normalization
        # keeps every consumer typed.
        raw_chain = self.sampler_chain
        if raw_chain and not isinstance(raw_chain[0], ChainItem):
            normalized = tuple(
                ChainItem(str(item["id"]), bool(item["enabled"]))
                for item in raw_chain  # type: ignore[index]
            )
            object.__setattr__(self, "sampler_chain", normalized)

    def as_document(self) -> dict[str, object]:
        """The JSON-safe read view (the wire shape — field order
        fixed, the values verbatim; the chain as the ordered list)."""
        document: dict[str, object] = {"name": self.name}
        document.update(self.values)
        document["sampler_chain"] = [
            {"id": item.id, "enabled": item.enabled}
            for item in self.sampler_chain
        ]
        return document


# ---------------------------------------------------------------- validation


def _validate_field(name: str, value: object) -> object:
    """One field's acceptance law (§19.1's ACCEPTED step — rejected
    LOUD, never a silent clamp). Data-driven over the library's own
    metadata (§3): the value_type/forms/limits ARE the closed
    vocabulary — the runtime's own form sets (the reviewed --help
    snapshot), never an invented enum."""
    if name == "name":
        if not isinstance(value, str) or not value.strip() or len(value) > 64:
            raise InferenceError(
                f"name {value!r} must be a non-empty str (<= 64 chars)"
            )
        return value.strip()
    if name == "sampler_chain":
        return _validate_chain(value)
    if name == "pinned":
        return _validate_pinned(value)
    control = _FIELD_INDEX.get(name)
    if control is None:
        raise InferenceError(
            f"unknown field {name!r} (closed set: {list(_FIELDS)})"
        )
    return _validate_control_value(control, value)


def _validate_control_value(control: SemanticControl, value: object) -> object:
    """The per-control acceptance: the value_type's own law. Every
    range/form below is the reviewed --help's own vocabulary (or a
    documented workbench bound where the snapshot pins none)."""
    kind = control.value_type
    if kind == "int":
        if isinstance(value, bool) or not isinstance(value, int):
            raise InferenceError(
                f"{control.field} {value!r} must be an int"
                + _range_doc(control)
            )
        _check_range(control, value)
        return value
    if kind == "float":
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
        ):
            raise InferenceError(
                f"{control.field} {value!r} must be a number"
                + _range_doc(control)
            )
        _check_range(control, float(value))
        return float(value)
    if kind == "bool":
        if not isinstance(value, bool):
            raise InferenceError(f"{control.field} {value!r} must be a bool")
        return value
    if kind == "enum":
        if value not in control.forms:
            raise InferenceError(
                f"{control.field} {value!r} must be one of "
                f"{list(control.forms)}"
            )
        return value
    if kind == "text":
        if not isinstance(value, str) or len(value) > 4096:
            raise InferenceError(
                f"{control.field} {value!r} must be a str (<= 4096 chars)"
            )
        return value
    if kind == "gpu_layers":
        if isinstance(value, str):
            if value not in GPU_LAYER_FORMS:
                raise InferenceError(
                    f"gpu_layers {value!r} must be 'auto' | 'all' or an "
                    "int in [0, 999]"
                )
            return value
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or not 0 <= value <= 999
        ):
            raise InferenceError(
                f"gpu_layers {value!r} must be 'auto' | 'all' or an "
                "int in [0, 999]"
            )
        return value
    raise InferenceError(  # pragma: no cover — the library is closed
        f"{control.field} carries an unknown value_type {kind!r}"
    )


def _range_doc(control: SemanticControl) -> str:
    if control.minimum is None or control.maximum is None:
        return ""
    low = int(control.minimum) if control.minimum == int(control.minimum) else control.minimum
    high = int(control.maximum) if control.maximum == int(control.maximum) else control.maximum
    return f" in [{low}, {high}]"


def _check_range(control: SemanticControl, value: float) -> None:
    if control.minimum is not None and value < control.minimum:
        raise InferenceError(
            f"{control.field} {value!r} is below the minimum "
            f"{control.minimum}"
        )
    if control.maximum is not None and value > control.maximum:
        raise InferenceError(
            f"{control.field} {value!r} is above the maximum "
            f"{control.maximum}"
        )


def _validate_chain(value: object) -> tuple[ChainItem, ...]:
    """The chain's acceptance law: a non-empty list over the library's
    own member ids, each {id, enabled} exactly, EVERY member present
    exactly once (membership is the whole set; order and enabled are
    the user's) — the chain stays one document, never a partial edit."""
    if not isinstance(value, (list, tuple)) or not value:
        raise InferenceError(
            "sampler_chain must be a non-empty ordered list of "
            "{id, enabled} objects"
        )
    items: list[ChainItem] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        if not isinstance(raw, Mapping) or set(raw) != {"id", "enabled"}:
            raise InferenceError(
                f"sampler_chain[{index}] must be exactly {{id, enabled}}"
            )
        item_id = raw["id"]
        if not isinstance(item_id, str) or item_id not in SAMPLER_CHAIN_IDS:
            raise InferenceError(
                f"sampler_chain[{index}].id {item_id!r} is not one of "
                f"{list(SAMPLER_CHAIN_IDS)} (the chain is never edited "
                "by omission — the whole set, one document)"
            )
        if item_id in seen:
            raise InferenceError(
                f"sampler_chain carries a duplicate member {item_id!r}"
            )
        seen.add(item_id)
        enabled = raw["enabled"]
        if not isinstance(enabled, bool):
            raise InferenceError(
                f"sampler_chain[{index}].enabled must be a bool"
            )
        items.append(ChainItem(item_id, enabled))
    missing = sorted(set(SAMPLER_CHAIN_IDS) - seen)
    if missing:
        raise InferenceError(
            f"sampler_chain is missing member(s) {missing} — membership "
            "is the whole set, never a partial document"
        )
    return tuple(items)


def _validate_pinned(value: object) -> tuple[str, ...]:
    """The workspace's pinned list (§14): known control ids only,
    order preserved (the user's own), duplicates rejected LOUD."""
    if not isinstance(value, (list, tuple)):
        raise InferenceError(
            "pinned must be a list of semantic control ids"
        )
    seen: set[str] = set()
    items: list[str] = []
    for index, raw in enumerate(value):
        if not isinstance(raw, str) or raw not in _CONTROL_INDEX:
            raise InferenceError(
                f"pinned[{index}] {raw!r} is not a known control id"
            )
        if raw in seen:
            raise InferenceError(f"pinned carries a duplicate {raw!r}")
        seen.add(raw)
        items.append(raw)
    return tuple(items)
