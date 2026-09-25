"""The llama.cpp semantic inference-control layer (inf-1, the chip
specification's repo-side landing — the owner's 2026-09-25 chip
workspace hand-off over `llama_cpp_chip_workspace_spec_2026-09-25.md`
+ «флаги llama.cpp.txt`, the reviewed runtime snapshot).

The law this module closes: **a chip is a SEMANTIC RUNTIME CONTROL,
not a CLI flag and not a UI button** — the users manipulate semantic
controls, the application resolves them into an effective
configuration, and the compiled CLI form is a technical artifact
(never the authoring language). The single law owner for the
architecture is `docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md`; this
module is its first LANDED form — the vertical slice.

The three layers (the law's §2, kept strictly separate):

```text
RAW CAPABILITY      the runtime's own surface (existence/syntax/
                    values/defaults) — the reviewed --help snapshot
                    is the EVIDENCE; the actual installed binary is
                    the AUTHORITY (never this module)
SEMANTIC CONTROL    THIS module — identity, human name, category,
                    kind, scope, relations, effective state
UI REPRESENTATION   workbench/presentation/redot — a projection,
                    never the semantic authority
```

The vertical slice's first admitted control set (cross-category per
the law's §16 — deliberately NOT only samplers):

```text
MODEL    Context
DEVICE   GPU Layers (AUTO/all/explicit) · Flash Attention (auto/on/off)
         Fit (on/off)
MEMORY   KV Cache Type K · KV Cache Type V
SAMPLING Temperature · Top-K · Top-P · Min-P · Penalties (repeat) ·
         Seed · the ordered SAMPLER CHAIN
CHAT     Chat Template (MODEL DEFAULT / GENERIC)
```

Settings ≠ Inference Control (the law's §1): the launch-settings
store (`workbench/application/settings.py`) owns DEPLOYMENT
(executable, web UI, raw extra_args); THIS store owns the semantic
generation-control values — the §19.1 BASE PROFILE layer. The
one-way migration `migrate_launch_semantics` moves the semantic
fields out of a schema/1 settings document at composition boot
(values preserved — the operator's saved values are data).

The honest truth chain (§19.1 — REQUESTED / ACCEPTED / EFFECTIVE /
OBSERVED / PRESENTED) is carried by the resolver's document: every
resolved control names its profile value, its request override and
its effective value with a REASON whenever a relation nullifies it
(the law's §7: configured-but-ineffective controls stay VISIBLE).

Zero network, zero engine imports, zero platform imports (the
compiled preview is INJECTED by the composition root — settings.py's
own seam); stdlib only (D-012, §27's envelope holds).
"""

from __future__ import annotations

import json
import os
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path

from workbench.api.gateway import (
    Gateway,
    OperationRejected,
    OperationSpec,
)

__all__ = [
    "SCHEMA",
    "CHAT_TEMPLATE_FORMS",
    "FLASH_ATTENTION_FORMS",
    "FIT_FORMS",
    "GPU_LAYER_FORMS",
    "KV_CACHE_TYPES",
    "SAMPLER_CHAIN_IDS",
    "InferenceError",
    "InferenceProfile",
    "InferenceStore",
    "CONTROL_LIBRARY",
    "migrate_launch_semantics",
    "register_inference_operations",
    "resolve",
]

#: The persisted document's schema tag (§15.3's schema-evolution law).
SCHEMA = "canonsim.workbench.inference/1"

# ------------------------------------------------------------- vocabularies

#: The GPU layer placement forms — the reviewed runtime's own literal
#: values (`-ngl N | 'auto' | 'all'`): AUTO and ALL are REAL runtime
#: forms, never "unset"/"off" synonyms (the law's §10).
GPU_LAYER_FORMS = ("auto", "all")

#: Flash attention forms (the runtime's `[on|off|auto]`).
FLASH_ATTENTION_FORMS = ("auto", "on", "off")

#: The memory-fitting heuristic's forms (`--fit [on|off]`).
FIT_FORMS = ("on", "off")

#: The KV cache data types (the reviewed `-ctk/-ctv` allowed set).
KV_CACHE_TYPES = (
    "f32",
    "f16",
    "bf16",
    "q8_0",
    "q4_0",
    "q4_1",
    "iq4_nl",
    "q5_0",
    "q5_1",
)

#: The chat template semantic modes: MODEL DEFAULT = the model's own
#: jinja template (emits `--jinja`); GENERIC = the server's fallback
#: (omits it). An explicit custom template string is a LATER row (the
#: law's §12 — the override relation lands with its consumer).
CHAT_TEMPLATE_FORMS = ("model_default", "generic")

#: The sampler chain's member ids — the reviewed runtime's own
#: `--samplers` names, restricted to the slice's controllable five
#: (the disabled-by-value forms are the runtime's own semantics:
#: top_k 0 / top_p 1.0 / min_p 0.0 / penalties 1.0). DRY, XTC,
#: top_n_sigma, typ_p and the adaptive families are LATER groups
#: (the law's §17 ladder — never collapsed into "advanced flags").
SAMPLER_CHAIN_IDS = ("penalties", "top_k", "top_p", "min_p", "temperature")


class InferenceError(ValueError):
    """An inference-contract violation (LOUD — a malformed profile, an
    out-of-range value, a relation conflict; never a silent clamp)."""


# --------------------------------------------------------------- the model


@dataclass(frozen=True)
class SemanticControl:
    """One semantic control's definition — the overlay's atom (the
    law's §3). Identity is the SEMANTIC id (``sampling.top_k``), never
    the raw flag; the flag is the raw mapping (shown in tooltips and
    the compile step, never the primary identity)."""

    id: str
    name: str
    category: str
    kind: str  # value | mode | toggle | chain
    scope: str  # spawn | request | spawn+request
    flag: str
    value_doc: str
    baseline: object
    upstream_default: object
    notes: tuple[str, ...] = ()
    status: str = "ACTIVE"  # ACTIVE | UNCLASSIFIED | LEGACY | REMOVED


def _library() -> tuple[SemanticControl, ...]:
    """The first admitted control set (the vertical slice). The
    `upstream_default` fields are the reviewed snapshot's OWN values
    (runtime evidence, pinned 2026-09-25) — they are NOT the project
    baseline: `baseline` is CanonSim's own pin (§5's ladder: upstream
    default ≠ project baseline ≠ profile value)."""

    def c(*args, **kwargs) -> SemanticControl:
        return SemanticControl(*args, **kwargs)

    return (
        c(
            "model.context",
            "Context",
            "model",
            "value",
            "spawn",
            "--ctx-size",
            "int in [1, 2097152] tokens",
            8192,
            0,
            (
                "the upstream default 0 loads the context from model "
                "metadata — a later row (the model-metadata AUTO form)",
            ),
        ),
        c(
            "device.gpu_layers",
            "GPU Layers",
            "device",
            "mode",
            "spawn",
            "-ngl",
            "'auto' | 'all' | an exact layer count in [0, 999]",
            999,
            "auto",
            (
                "AUTO ('auto') and ALL ('all') are the runtime's own "
                "literal forms — never 'unset' synonyms",
            ),
        ),
        c(
            "device.flash_attention",
            "Flash Attention",
            "device",
            "mode",
            "spawn",
            "-fa",
            "'auto' | 'on' | 'off'",
            "on",
            "auto",
            (
                "the project baseline 'on' is an explicit pin, NOT the "
                "upstream default 'auto'",
            ),
        ),
        c(
            "device.fit",
            "Fit",
            "device",
            "toggle",
            "spawn",
            "--fit",
            "'on' | 'off' — the automatic device-memory fitting",
            "on",
            "on",
            (
                "a good starting point, NOT a guaranteed optimum — the "
                "chip specification's own risk note (an INFERENCE, not "
                "a fact: benchmark manual placement when it matters)",
            ),
        ),
        c(
            "memory.cache_type_k",
            "KV Cache Type K",
            "memory",
            "mode",
            "spawn",
            "--cache-type-k",
            "one of " + " | ".join(KV_CACHE_TYPES),
            "f16",
            "f16",
            (
                "quantized forms (q*_*) are build-sensitive — re-verify "
                "against the installed binary before relying on them",
            ),
        ),
        c(
            "memory.cache_type_v",
            "KV Cache Type V",
            "memory",
            "mode",
            "spawn",
            "--cache-type-v",
            "one of " + " | ".join(KV_CACHE_TYPES),
            "f16",
            "f16",
            (
                "quantized V forms are more restrictive than K on some "
                "builds — the runtime refuses loudly, never silently",
            ),
        ),
        c(
            "sampling.temperature",
            "Temperature",
            "sampling",
            "value",
            "spawn+request",
            "--temp",
            "a number in [0, 2]",
            0.8,
            0.8,
            (
                "0 = the deterministic (greedy) decoding state — the "
                "profile's other sampler values are PRESERVED, never "
                "deleted (the law's §11)",
            ),
        ),
        c(
            "sampling.top_k",
            "Top-K",
            "sampling",
            "value",
            "spawn",
            "--top-k",
            "an int in [0, 10000] (the runtime's own form: 0 = disabled)",
            40,
            40,
            ("0 = disabled — a REAL off value, distinct from AUTO",),
        ),
        c(
            "sampling.top_p",
            "Top-P",
            "sampling",
            "value",
            "spawn",
            "--top-p",
            "a number in [0, 1] (the runtime's own form: 1.0 = disabled)",
            0.95,
            0.95,
            ("1.0 = disabled — a REAL off value, distinct from AUTO",),
        ),
        c(
            "sampling.min_p",
            "Min-P",
            "sampling",
            "value",
            "spawn",
            "--min-p",
            "a number in [0, 1] (the runtime's own form: 0.0 = disabled)",
            0.05,
            0.05,
            ("0.0 = disabled — a REAL off value, distinct from AUTO",),
        ),
        c(
            "sampling.penalties",
            "Penalties",
            "sampling",
            "value",
            "spawn",
            "--repeat-penalty",
            "a number in [0, 4] (the runtime's own form: 1.0 = disabled)",
            1.1,
            1.0,
            (
                "the project baseline 1.1 is an explicit pin — the "
                "upstream default is 1.00 (disabled); §5's ladder in "
                "one control",
            ),
        ),
        c(
            "sampling.seed",
            "Seed",
            "sampling",
            "value",
            "spawn",
            "--seed",
            "an int in [-1, 2147483647] (-1 = the runtime's random form)",
            -1,
            -1,
            (
                "-1 IS the random form (the runtime's own sentinel) — "
                "a fixed seed is not a bit-identical guarantee across "
                "execution shapes (the reviewed --help's own caveat)",
            ),
        ),
        c(
            "chat.template",
            "Chat Template",
            "chat",
            "mode",
            "spawn",
            "--jinja",
            "MODEL DEFAULT (the model's own template) | GENERIC",
            "model_default",
            "model_default",
            (
                "an explicit custom template string (the override "
                "relation) is a later row with its own consumer",
            ),
        ),
    )


#: The control library — the semantic overlay's first admitted set.
CONTROL_LIBRARY: tuple[SemanticControl, ...] = _library()

_CONTROL_INDEX: dict[str, SemanticControl] = {
    control.id: control for control in CONTROL_LIBRARY
}


@dataclass(frozen=True)
class ChainItem:
    """One sampler chain member's profile state (the law's §11): a
    sampler chain is an ORDERED semantic object — membership +
    position are first-class, never a favorites grid. `enabled`
    decides whether the member is emitted into `--samplers`."""

    id: str
    enabled: bool


@dataclass(frozen=True)
class InferenceProfile:
    """The typed semantic configuration document — the §19.1 BASE
    PROFILE layer (reusable, persisted, the single semantic owner).
    The sampler VALUES live in their own fields; the CHAIN holds
    membership + order only (the two are edited together, one
    document, one authority)."""

    name: str = "Baseline"
    context: int = 8192
    gpu_layers: int | str = 999
    flash_attention: str = "on"
    fit: str = "on"
    cache_type_k: str = "f16"
    cache_type_v: str = "f16"
    temperature: float = 0.8
    top_k: int = 40
    top_p: float = 0.95
    min_p: float = 0.05
    repeat_penalty: float = 1.1
    seed: int = -1
    chat_template: str = "model_default"
    sampler_chain: tuple[ChainItem, ...] = field(
        default_factory=lambda: tuple(
            ChainItem(item, True) for item in SAMPLER_CHAIN_IDS
        )
    )

    def __post_init__(self) -> None:
        # The chain accepts both the typed and the WIRE form (a list
        # of {id, enabled} dicts — the JSON roundtrip's own shape);
        # the normalization keeps every consumer typed.
        raw_chain = self.sampler_chain
        if raw_chain and not isinstance(raw_chain[0], ChainItem):
            normalized = tuple(
                ChainItem(str(item["id"]), bool(item["enabled"]))
                for item in raw_chain
            )
            object.__setattr__(self, "sampler_chain", normalized)

    def as_document(self) -> dict[str, object]:
        """The JSON-safe read view (the wire shape — field order
        fixed, the values verbatim; the chain as the ordered list)."""
        return {
            "name": self.name,
            "context": self.context,
            "gpu_layers": self.gpu_layers,
            "flash_attention": self.flash_attention,
            "fit": self.fit,
            "cache_type_k": self.cache_type_k,
            "cache_type_v": self.cache_type_v,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "min_p": self.min_p,
            "repeat_penalty": self.repeat_penalty,
            "seed": self.seed,
            "chat_template": self.chat_template,
            "sampler_chain": [
                {"id": item.id, "enabled": item.enabled}
                for item in self.sampler_chain
            ],
        }


_FIELDS: tuple[str, ...] = (
    "name",
    "context",
    "gpu_layers",
    "flash_attention",
    "fit",
    "cache_type_k",
    "cache_type_v",
    "temperature",
    "top_k",
    "top_p",
    "min_p",
    "repeat_penalty",
    "seed",
    "chat_template",
    "sampler_chain",
)


# ------------------------------------------------------------- validation


def _validate_field(name: str, value: object) -> object:
    """One field's acceptance law (§19.1's ACCEPTED step — rejected
    LOUD, never a silent clamp). The closed per-field vocabulary is
    the RUNTIME's own form set (the reviewed --help snapshot), not an
    invented enum."""
    if name == "name":
        if not isinstance(value, str) or not value.strip() or len(value) > 64:
            raise InferenceError(
                f"name {value!r} must be a non-empty str (<= 64 chars)"
            )
        return value.strip()
    if name == "context":
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or not 1 <= value <= 2_097_152
        ):
            raise InferenceError(
                f"context {value!r} must be an int in [1, 2097152]"
            )
        return value
    if name == "gpu_layers":
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
    if name == "flash_attention":
        if value not in FLASH_ATTENTION_FORMS:
            raise InferenceError(
                f"flash_attention {value!r} must be one of "
                f"{list(FLASH_ATTENTION_FORMS)}"
            )
        return value
    if name == "fit":
        if value not in FIT_FORMS:
            raise InferenceError(
                f"fit {value!r} must be one of {list(FIT_FORMS)}"
            )
        return value
    if name in ("cache_type_k", "cache_type_v"):
        if value not in KV_CACHE_TYPES:
            raise InferenceError(
                f"{name} {value!r} must be one of {list(KV_CACHE_TYPES)}"
            )
        return value
    if name == "temperature":
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not 0.0 <= float(value) <= 2.0
        ):
            raise InferenceError(
                f"temperature {value!r} must be a number in [0, 2]"
            )
        return float(value)
    if name == "top_k":
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or not 0 <= value <= 10_000
        ):
            raise InferenceError(
                f"top_k {value!r} must be an int in [0, 10000]"
            )
        return value
    if name in ("top_p", "min_p"):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not 0.0 <= float(value) <= 1.0
        ):
            raise InferenceError(f"{name} {value!r} must be a number in [0, 1]")
        return float(value)
    if name == "repeat_penalty":
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not 0.0 <= float(value) <= 4.0
        ):
            raise InferenceError(
                f"repeat_penalty {value!r} must be a number in [0, 4]"
            )
        return float(value)
    if name == "seed":
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or not -1 <= value <= 2_147_483_647
        ):
            raise InferenceError(
                f"seed {value!r} must be an int in [-1, 2147483647]"
            )
        return value
    if name == "chat_template":
        if value not in CHAT_TEMPLATE_FORMS:
            raise InferenceError(
                f"chat_template {value!r} must be one of "
                f"{list(CHAT_TEMPLATE_FORMS)}"
            )
        return value
    if name == "sampler_chain":
        return _validate_chain(value)
    raise InferenceError(
        f"unknown field {name!r} (closed set: {list(_FIELDS)})"
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
        if item_id not in SAMPLER_CHAIN_IDS:
            raise InferenceError(
                f"sampler_chain[{index}].id {item_id!r} is not one of "
                f"{list(SAMPLER_CHAIN_IDS)} (the later rows extend this "
                "set — the chain is never edited by omission)"
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


# ------------------------------------------------------------ the resolver


#: The resolved-state vocabulary (the law's §8): CONFIGURED is a
#: document fact, not a state; every resolved control carries exactly
#: one state below plus a REASON whenever it is not EFFECTIVE.
STATES = (
    "EFFECTIVE",
    "AUTO",
    "INACTIVE",
    "INEFFECTIVE",
    "CONFLICT",
    "RISK",
    "EXPERIMENTAL",
    "UNCLASSIFIED",
    "LEGACY",
    "REMOVED",
)

#: The runtime's own disabled-value forms (the reviewed --help's own
#: words, pinned per sampler — the INACTIVE state's source of truth).
_DISABLED_FORMS: dict[str, object] = {
    "sampling.top_k": 0,
    "sampling.top_p": 1.0,
    "sampling.min_p": 0.0,
    "sampling.penalties": 1.0,
}


def resolve(
    profile: InferenceProfile,
    *,
    request_temperature: float | None = None,
) -> dict[str, object]:
    """The effective-state resolver (the law's §6 pipeline, the
    deterministic minimal form): compose the BASE profile with the
    call-local REQUEST layer where given, validate implicitly (the
    store already accepted the values), evaluate the RELATIONS
    (evidence-pinned only), and return the per-control document.

    The relations this slice pins (each sourced from the runtime
    evidence or the chip specification's own law — never invented):

    - ``effective_noop``: temperature 0 = the deterministic decoding
      state → the distribution samplers (top_k, top_p, min_p,
      penalties) stay CONFIGURED but INEFFECTIVE, with the reason —
      their values are PRESERVED (never deleted, the law's §11).
    - ``effective_noop``: a sampler NOT in the chain (enabled=false)
      → its value flag is accepted but INEFFECTIVE (reason: not in
      the sampler chain) — membership and value stay separate.
    - ``value-disable``: the runtime's own disabled forms
      (top_k 0 / top_p 1.0 / min_p 0.0 / penalties 1.0) → INACTIVE
      with the reason (distinct from AUTO and from a value).

    The request layer: an EXPLICIT request temperature overrides the
    BASE value (§19.1's call-local layer); seed's request scope waits
    for its adapter consumer (the honest DEFERRED note rides the
    document)."""
    # ---- composition (BASE -> call-local), the request layer
    temperature = (
        float(request_temperature)
        if request_temperature is not None
        else profile.temperature
    )
    deterministic = temperature == 0.0
    chain_ids = [item.id for item in profile.sampler_chain]
    chain_enabled = {
        item.id: item.enabled for item in profile.sampler_chain
    }

    def control_document(control: SemanticControl) -> dict[str, object]:
        value = _profile_value(profile, control).value
        if control.id == "sampling.temperature":
            value = temperature
            source = (
                "request" if request_temperature is not None else "profile"
            )
        else:
            source = "profile"
        state = "EFFECTIVE"
        reasons: list[str] = []
        if control.id == "device.gpu_layers" and isinstance(value, str):
            # 'auto'/'all' are REAL runtime forms — AUTO is a first-
            # class state, never 'unset' (the law's §10).
            state = "AUTO" if value == "auto" else "EFFECTIVE"
        if control.id == "device.flash_attention" and value == "auto":
            state = "AUTO"
        if control.id == "sampling.seed" and value == -1:
            state = "AUTO"
            reasons.append(
                "-1 is the runtime's random-seed form (the --help's own "
                "sentinel, not an application convention)"
            )
        if control.id in _DISABLED_FORMS and value == _DISABLED_FORMS[control.id]:
            state = "INACTIVE"
            reasons.append(
                f"{control.flag} {value} is the runtime's own disabled "
                "form (a real off value, distinct from AUTO)"
            )
        if control.id in _DISABLED_FORMS and control.id != "sampling.temperature":
            if deterministic and state != "INACTIVE":
                state = "INEFFECTIVE"
                reasons.append(
                    "temperature 0 is the deterministic decoding state — "
                    "the distribution samplers are ignored; the configured "
                    "value is preserved (return by restoring temperature)"
                )
            elif (
                not chain_enabled.get(control.id.rsplit(".", 1)[1], True)
                and state != "INEFFECTIVE"
            ):
                state = "INEFFECTIVE"
                reasons.append(
                    "the sampler is not in the emitted chain (enabled = "
                    "false) — membership and value are separate concerns"
                )
        if control.id == "sampling.temperature" and deterministic:
            state = "EFFECTIVE"
            reasons.append(
                "temperature 0 = the deterministic (greedy) decoding mode"
            )
        return {
            "id": control.id,
            "name": control.name,
            "category": control.category,
            "kind": control.kind,
            "scope": control.scope,
            "flag": control.flag,
            "value": value,
            "value_doc": control.value_doc,
            "source": source,
            "state": state,
            "reasons": reasons,
            "baseline": control.baseline,
            "upstream_default": control.upstream_default,
            "notes": list(control.notes),
        }

    controls = [control_document(c) for c in CONTROL_LIBRARY]
    chain_document = [
        {
            "id": item.id,
            "name": _CONTROL_INDEX[f"sampling.{item.id}"].name
            if f"sampling.{item.id}" in _CONTROL_INDEX
            else item.id,
            "enabled": item.enabled,
            "order": index,
            "value": _profile_value(
                profile, _CONTROL_INDEX[f"sampling.{item.id}"]
            ).value,
            "state": _chain_item_state(
                item, deterministic, profile
            ),
            "reasons": _chain_item_reasons(item, deterministic),
        }
        for index, item in enumerate(profile.sampler_chain)
    ]
    return {
        "profile_name": profile.name,
        "controls": controls,
        "sampler_chain": chain_document,
        "chain_order": chain_ids,
        "deterministic": deterministic,
        "request_layer": {
            "temperature": request_temperature,
            "seed": None,
            "note": (
                "the request layer carries the explicit call-local "
                "overrides; seed's request scope waits for the engine "
                "adapter's own consumer (a later row)"
            ),
        },
    }


@dataclass(frozen=True)
class _Value:
    """A resolved control value (the internal accessor's carrier)."""

    value: object


_FIELD_OF_CONTROL: dict[str, str] = {
    "model.context": "context",
    "device.gpu_layers": "gpu_layers",
    "device.flash_attention": "flash_attention",
    "device.fit": "fit",
    "memory.cache_type_k": "cache_type_k",
    "memory.cache_type_v": "cache_type_v",
    "sampling.temperature": "temperature",
    "sampling.top_k": "top_k",
    "sampling.top_p": "top_p",
    "sampling.min_p": "min_p",
    "sampling.penalties": "repeat_penalty",
    "sampling.seed": "seed",
    "chat.template": "chat_template",
}


def _profile_value(profile: InferenceProfile, control: SemanticControl) -> _Value:
    field_name = _FIELD_OF_CONTROL[control.id]
    return _Value(getattr(profile, field_name))


def _chain_item_state(
    item: ChainItem, deterministic: bool, profile: InferenceProfile
) -> str:
    if not item.enabled:
        return "INEFFECTIVE"
    if deterministic and item.id != "temperature":
        return "INEFFECTIVE"
    control_id = f"sampling.{item.id}"
    value = _profile_value(profile, _CONTROL_INDEX[control_id]).value
    if control_id in _DISABLED_FORMS and value == _DISABLED_FORMS[control_id]:
        return "INACTIVE"
    if item.id == "temperature":
        return "EFFECTIVE"
    return "EFFECTIVE"


def _chain_item_reasons(item: ChainItem, deterministic: bool) -> list[str]:
    if not item.enabled:
        return [
            "the sampler is not in the emitted chain (enabled = false)"
        ]
    if deterministic and item.id != "temperature":
        return [
            "temperature 0 is the deterministic decoding state — "
            "ignored; the configured value is preserved"
        ]
    return []


# --------------------------------------------------------------- the store


class InferenceStore:
    """The inference-profile owner: load (loud) → current() → update()
    (validate + apply + persist atomically). Thread-safe (the gateway
    dispatches on worker threads; the composition root reads
    `current()` at each spawn — settings.py's own policy-clock law)."""

    def __init__(self, path: Path) -> None:
        if not isinstance(path, Path):
            raise InferenceError("the profile path must be a pathlib.Path")
        if not path.is_absolute():
            raise InferenceError(
                f"the profile path {str(path)!r} is relative — the "
                ".git/CWD-independence law (app §16) requires an "
                "absolute path from the composition root"
            )
        self._path = path
        self._lock = threading.Lock()
        self._profile = self._load()

    @property
    def path(self) -> Path:
        return self._path

    def current(self) -> InferenceProfile:
        with self._lock:
            return self._profile

    def update(self, partial: Mapping[str, object]) -> InferenceProfile:
        """§19.1's REQUESTED→ACCEPTED→EFFECTIVE half: validate the
        CLOSED partial document (absent fields unchanged), apply, and
        persist atomically — the returned value is the new current."""
        if not isinstance(partial, Mapping):
            raise InferenceError("the update payload must be a mapping")
        unknown = sorted(set(partial) - set(_FIELDS))
        if unknown:
            raise InferenceError(
                f"unknown field(s) {unknown} (closed set: {list(_FIELDS)})"
            )
        accepted = {
            name: _validate_field(name, value)
            for name, value in partial.items()
        }
        with self._lock:
            updated = replace(self._profile, **accepted)
            self._persist_locked(updated)
            self._profile = updated
            return updated

    # ------------------------------------------------------------ private

    def _load(self) -> InferenceProfile:
        """The §16 startup/recovery read (settings.py's own law): a
        MISSING file is the honest defaults (the file appears on the
        first save); a corrupt or schema-mismatched file refuses
        LOUD — never a silently-reset profile."""
        if not self._path.exists():
            return InferenceProfile()
        try:
            raw = self._path.read_text(encoding="utf-8")
            document = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            raise InferenceError(
                f"the inference profile {str(self._path)!r} is unreadable "
                f"({exc}) — fix or delete it by hand; it is never reset "
                "silently"
            ) from exc
        if not isinstance(document, dict):
            raise InferenceError(
                f"the inference profile {str(self._path)!r} is not an object"
            )
        if document.get("schema") != SCHEMA:
            raise InferenceError(
                f"the inference profile {str(self._path)!r} carries schema "
                f"{document.get('schema')!r}, expected {SCHEMA!r} — "
                "migrate or delete it by hand"
            )
        body = document.get("profile")
        if not isinstance(body, dict):
            raise InferenceError(
                f"the inference profile {str(self._path)!r} has no profile "
                "object"
            )
        unknown = sorted(set(body) - set(_FIELDS))
        if unknown:
            raise InferenceError(
                f"the inference profile carries unknown field(s) {unknown} "
                f"(closed set: {list(_FIELDS)})"
            )
        accepted = {
            name: _validate_field(name, value) for name, value in body.items()
        }
        return replace(InferenceProfile(), **accepted)

    def _persist_locked(self, profile: InferenceProfile) -> None:
        """The atomic write (§15's crash-safety half): a tmp file in
        the same directory + os.replace — a crash never leaves a
        half-written profile behind."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            document = {
                "schema": SCHEMA,
                "profile": profile.as_document(),
            }
            tmp_path = self._path.with_suffix(".json.tmp")
            tmp_path.write_text(
                json.dumps(document, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            os.replace(tmp_path, self._path)
        except OSError as exc:
            raise InferenceError(
                f"cannot persist the inference profile to "
                f"{str(self._path)!r}: {exc}"
            ) from exc


# ------------------------------------------------------------- migration

#: The launch-settings semantic fields (the schema/1 vocabulary this
#: module ADOPTS — the migration's input contract; the deployment
#: fields stay the settings store's own).
_LAUNCH_SEMANTIC_FIELDS = (
    "context",
    "gpu_layers",
    "flash_attention",
    "temperature",
    "top_k",
    "top_p",
    "min_p",
    "repeat_penalty",
    "jinja",
)

_SETTINGS_SCHEMA_1 = "canonsim.workbench.settings/1"
_SETTINGS_SCHEMA_2 = "canonsim.workbench.settings/2"


def migrate_launch_semantics(
    settings_path: Path, inference_path: Path
) -> bool:
    """The one-way settings/1 → settings/2 + inference/1 migration
    (the composition root calls it BEFORE constructing the stores):

    - a settings/1 document's SEMANTIC fields (the sampler family +
      context/gpu-layers/flash-attention/jinja) move into the
      inference profile — written ONLY when no inference profile
      exists yet (the inference store is the newer truth; a present
      profile wins, the stale launch copy is simply dropped);
    - the settings document is rewritten as schema/2 carrying ONLY
      the deployment fields (llama_server_exe, no_webui,
      extra_args);
    - values are preserved verbatim (jinja: true → chat_template
      'model_default', false → 'generic') — never a silent reset.

    Idempotent: a schema/2 or missing settings file is a no-op. A
    malformed settings document raises LOUD (the operator's saved
    values are data). Returns True when a migration happened."""
    if not settings_path.exists():
        return False
    try:
        raw = settings_path.read_text(encoding="utf-8")
        document = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise InferenceError(
            f"cannot migrate the settings document "
            f"{str(settings_path)!r} ({exc}) — fix it by hand; the "
            "migration never resets the operator's values"
        ) from exc
    if not isinstance(document, dict):
        raise InferenceError(
            f"the settings document {str(settings_path)!r} is not an object"
        )
    schema = document.get("schema")
    if schema != _SETTINGS_SCHEMA_1:
        return False  # schema/2 (already migrated) or a foreign tag
    body = document.get("settings")
    if not isinstance(body, dict):
        raise InferenceError(
            f"the settings document {str(settings_path)!r} has no "
            "settings object"
        )
    semantic = {
        name: body[name] for name in _LAUNCH_SEMANTIC_FIELDS if name in body
    }
    if inference_path.exists():
        try:
            existing = json.loads(inference_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise InferenceError(
                f"the inference profile {str(inference_path)!r} is "
                f"unreadable ({exc}) — fix it by hand; the migration "
                "never overwrites it"
            ) from exc
        if not isinstance(existing, dict) or existing.get("schema") != SCHEMA:
            raise InferenceError(
                f"the inference profile {str(inference_path)!r} carries a "
                f"foreign schema — fix or delete it by hand"
            )
    else:
        jinja = semantic.pop("jinja", True)
        profile_body: dict[str, object] = {
            name: value
            for name, value in semantic.items()
            if name in _FIELDS
        }
        profile_body["chat_template"] = (
            "model_default" if jinja else "generic"
        )
        accepted = {
            name: _validate_field(name, value)
            for name, value in profile_body.items()
        }
        profile = replace(InferenceProfile(), **accepted)
        inference_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = inference_path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(
                {"schema": SCHEMA, "profile": profile.as_document()},
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        os.replace(tmp, inference_path)
    deployment = {
        name: body[name]
        for name in ("llama_server_exe", "no_webui", "extra_args")
        if name in body
    }
    rewritten = {
        "schema": _SETTINGS_SCHEMA_2,
        "settings": deployment,
    }
    tmp = settings_path.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(rewritten, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, settings_path)
    return True


# ------------------------------------------------------------ operations


def _rejected(reason: str) -> OperationRejected:
    return OperationRejected("DOMAIN_REJECTED", reason)


def register_inference_operations(
    gateway: Gateway,
    store: InferenceStore,
    *,
    compiled_preview: Callable[[Mapping[str, object]], str] | None = None,
    managed_live: Callable[[], bool] | None = None,
) -> None:
    """The inference family's wiring (the composition root calls it —
    §6.1's single-owner law): the READ (the resolved controls
    document + the injected compiled preview + the managed liveness)
    and the UPDATE (the closed partial document, validated through
    the store, the honest next-spawn note). The preview and liveness
    callables are INJECTED — this module never imports the platform
    or the managed backend (settings.py's own seam)."""
    gateway.register(
        OperationSpec(
            name="inference.read",
            kind="READ",
            handler=_make_inference_read(store, compiled_preview, managed_live),
            description=(
                "the resolved inference-control document (§19.1's "
                "effective state per control) + the compiled preview — "
                "the Inference surface's own read"
            ),
        )
    )
    gateway.register(
        OperationSpec(
            name="inference.update",
            kind="MUTATION",
            handler=_make_inference_update(store, compiled_preview, managed_live),
            session_scoped=True,
            description=(
                "the closed partial update over the semantic profile "
                "(validated, persisted — effective at the NEXT managed "
                "spawn, §11.1's replacement path being a later row)"
            ),
        )
    )


def _inference_document(
    store: InferenceStore,
    compiled_preview: Callable[[Mapping[str, object]], str] | None,
    live: Callable[[], bool] | None,
    *,
    request_temperature: float | None = None,
) -> dict[str, object]:
    """The read model: the RESOLVED document (the effective state per
    control — the law's §6/§8) + the compiled-preview evidence + the
    honest next-spawn note (a LIVE server keeps its spawn flags until
    unloaded — settings.py's own law, verbatim)."""
    resolved = resolve(
        store.current(), request_temperature=request_temperature
    )
    live_now = bool(live is not None and live())
    document: dict[str, object] = {
        **resolved,
        "profile": store.current().as_document(),
        "managed_live": live_now,
        "applies": "next-spawn",
    }
    if compiled_preview is not None:
        document["compiled_preview"] = compiled_preview(
            store.current().as_document()
        )
    else:
        document["compiled_preview"] = None
    if live_now:
        document["note"] = (
            "a LIVE server keeps its spawn flags until unloaded — the "
            "saved values apply at the next model.load"
        )
    return document


def _make_inference_read(
    store: InferenceStore,
    compiled_preview: Callable[[Mapping[str, object]], str] | None,
    live: Callable[[], bool] | None,
):
    def handler(context) -> Mapping[str, object]:
        if context.arguments:
            raise _rejected(
                f"inference.read: takes no arguments "
                f"({sorted(context.arguments)})"
            )
        return _inference_document(store, compiled_preview, live)

    return handler


def _make_inference_update(
    store: InferenceStore,
    compiled_preview: Callable[[Mapping[str, object]], str] | None,
    live: Callable[[], bool] | None,
):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        try:
            store.update(arguments)
        except InferenceError as exc:
            raise _rejected(f"inference.update: {exc}") from exc
        if context.effects is not None:
            context.effects.effect(
                {
                    "effect": "INFERENCE_UPDATED",
                    "fields": sorted(
                        key for key in arguments if key != "sampler_chain"
                    ),
                }
            )
        return _inference_document(store, compiled_preview, live)

    return handler


def effective_temperature(store: InferenceStore) -> float:
    """The chat row's BASE-temperature provider (§19.1's BASE layer —
    composition.py's injected callable): the resolved profile's
    effective temperature, the value a chat.send WITHOUT an explicit
    temperature resolves from (the explicit call-local value always
    wins, backend.py's own law)."""
    profile = store.current()
    resolved = resolve(profile)
    for control in resolved["controls"]:  # type: ignore[union-attr]
        if control["id"] == "sampling.temperature":  # type: ignore[index]
            value = control["value"]
            if isinstance(value, (int, float)) and not isinstance(
                value, bool
            ):
                return float(value)
    return float(profile.temperature)


def launch_kwargs(profile: InferenceProfile) -> dict[str, object]:
    """The compiled launch-argument document (the law's §13 — the
    platform's typed surface vocabulary): the semantic values mapped
    onto `build_server_command`'s own kwargs. The FLAG SYNTAX stays
    the platform's single owner (app §2's seam law); this function
    owns the MEANING→value mapping only. The chain compiles to the
    ordered enabled `--samplers` members; AUTO/ALL gpu forms pass
    through as the runtime's own literal forms."""
    chain = [item.id for item in profile.sampler_chain if item.enabled]
    kwargs: dict[str, object] = {
        "context": profile.context,
        "gpu_layers": profile.gpu_layers,
        "flash_attention": profile.flash_attention,
        "fit": profile.fit,
        "cache_type_k": profile.cache_type_k,
        "cache_type_v": profile.cache_type_v,
        "temperature": profile.temperature,
        "top_k": profile.top_k,
        "top_p": profile.top_p,
        "min_p": profile.min_p,
        "repeat_penalty": profile.repeat_penalty,
        "samplers": chain,
        "seed": profile.seed,
        "jinja": profile.chat_template == "model_default",
    }
    return kwargs
