"""The llama.cpp semantic inference-control layer (inf-1/inf-2, the
chip specification's repo-side landing — the owner's 2026-09-25 chip
workspace hand-off over `llama_cpp_chip_workspace_spec_2026-09-25.md`
+ «флаги llama.cpp.txt`, the reviewed runtime snapshot; inf-2 the
owner's 2026-09-26 «доделывай по-человечески» call — the FULL chip
library, the relations, the presets, the workspace pinning).

The law this module closes: **a chip is a SEMANTIC RUNTIME CONTROL,
not a CLI flag and not a UI button** — the users manipulate semantic
controls, the application resolves them into an effective
configuration, and the compiled CLI form is a technical artifact
(never the authoring language). The single law owner for the
architecture is `docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md`; this
module is its landed form — the full library over the reviewed
runtime surface.

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

The admitted control families (inf-2 — the whole reviewed surface,
each family its own category, never one "advanced parameters"
bucket):

```text
MODEL    Context · Predict · Keep · Threads · Batch Threads ·
         Batch Size · Ubatch Size
DEVICE   GPU Layers · Flash Attention · Fit · Main GPU · Tensor
         Split · Split Mode
MEMORY   KV K/V · KV Offload · Unified KV · Cache RAM · Cache
         Reuse · Full SWA Cache
LOADING  Load Mode · Warmup · Check Tensors · Weight Repack
MOE      MoE CPU · MoE CPU Layers · FFN CPU Layers · Tensor Override
CPU      NUMA
SAMPLING the FULL surface: Temperature · Top-K · Top-P · Min-P ·
         Typical-P · Top-N-Sigma · the penalties family (Repeat/
         Window/Presence/Frequency) · the DRY family · the XTC
         family · the Mirostat family · Dynatemp · Adaptive-P ·
         Ignore EOS · Logit Bias · Seed — + the 9-member ordered
         SAMPLER CHAIN (the reviewed default order)
CHAT     Chat Template (+ custom) · Reasoning (on/off/auto) ·
         Format · Effort · Budget · Prefill Assistant
STRUCT.  GBNF Grammar · JSON Schema
SERVER   Parallel · Continuous Batching · Context Shift · Prompt
         Caching
OBSERV.  Metrics · JSONL Logging · Internal Timings
SPEC.    Speculative Type · Draft Model
ROPE     RoPE Scaling · Freq Base/Scale · the YaRN family
SPECIAL  Embeddings · Multimodal Projector
LORA     LoRA Adapter
```

Settings ≠ Inference Control (the law's §1): the launch-settings
store (`workbench/application/settings.py`) owns DEPLOYMENT
(executable, web UI, raw extra_args); THIS store owns the semantic
generation-control values — the §19.1 BASE PROFILE layer (plus the
§14 WORKSPACE section: the pinned control ids, never a second store).
The one-way migration `migrate_launch_semantics` moves the semantic
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
    "CATEGORIES",
    "CHAT_TEMPLATE_FORMS",
    "FLASH_ATTENTION_FORMS",
    "FIT_FORMS",
    "GPU_LAYER_FORMS",
    "KV_CACHE_TYPES",
    "LOAD_MODE_FORMS",
    "NUMA_FORMS",
    "REASONING_FORMS",
    "REASONING_FORMAT_FORMS",
    "REASONING_EFFORT_FORMS",
    "ROPE_SCALING_FORMS",
    "SAMPLER_CHAIN_IDS",
    "SPLIT_MODE_FORMS",
    "SPEC_TYPE_FORMS",
    "InferenceError",
    "InferenceProfile",
    "InferenceStore",
    "CONTROL_LIBRARY",
    "PRESETS",
    "compile_semantic",
    "migrate_launch_semantics",
    "register_inference_operations",
    "resolve",
]

#: The persisted document's schema tag (§15.3's schema-evolution law —
#: the inf-2 extension ADDS fields/categories without renaming or
#: removing any inf-1 field: an old profile loads as-is, its absent
#: fields take the library baselines, its 5-member chain upgrades to
#: the 9-member set at load).
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

#: The model loading modes (the reviewed `-lm` allowed set).
LOAD_MODE_FORMS = ("auto", "none", "mmap", "mlock", "mmap+mlock", "dio")

#: The multi-GPU split modes (the reviewed `-sm` allowed set).
SPLIT_MODE_FORMS = ("none", "layer", "row", "tensor")

#: The NUMA strategies (the reviewed `--numa` allowed set; "off" is
#: the application's own not-emitted form — the runtime takes no
#: `--numa` argument by default).
NUMA_FORMS = ("off", "distribute", "isolate", "numactl")

#: The chat template semantic modes: MODEL DEFAULT = the model's own
#: jinja template (emits `--jinja`); GENERIC = the server's fallback
#: (emits `--no-jinja`); CUSTOM = an explicit jinja template string
#: (emits `--jinja --chat-template <text>` — the law's §12 override
#: relation, its custom text riding the companion field).
CHAT_TEMPLATE_FORMS = ("model_default", "generic", "custom")

#: The reasoning switch forms (the reviewed `-rea [on|off|auto]`).
REASONING_FORMS = ("auto", "on", "off")

#: The reasoning-format forms (the reviewed allowed set, auto = the
#: runtime's own detection).
REASONING_FORMAT_FORMS = ("auto", "none", "deepseek", "deepseek-legacy")

#: The reasoning-effort levels (the reviewed allowed set; "default"
#: keeps the template's own).
REASONING_EFFORT_FORMS = (
    "default",
    "minimal",
    "low",
    "medium",
    "high",
    "xhigh",
    "max",
)

#: The RoPE scaling strategies ("model" is the application's own
#: not-emitted form — the model's own metadata wins, the runtime's
#: documented default).
ROPE_SCALING_FORMS = ("model", "none", "linear", "yarn")

#: The speculative-decoding types (the reviewed `--spec-type` set).
SPEC_TYPE_FORMS = (
    "none",
    "draft-simple",
    "draft-eagle3",
    "draft-mtp",
    "draft-dflash",
    "draft-dspark",
    "ngram-simple",
    "ngram-map-k",
    "ngram-map-k4v",
    "ngram-mod",
    "ngram-cache",
)

#: The category order — the reviewed chip specification's §31 default
#: semantic order (the law's §16 ladder, one category per family,
#: never one "advanced parameters" bucket). "legacy" is NOT a user
#: category (a search-only compatibility layer, a later discovery row).
CATEGORIES = (
    "model",
    "device",
    "memory",
    "loading",
    "moe",
    "cpu",
    "sampling",
    "chat",
    "structured",
    "server",
    "observability",
    "speculative",
    "rope",
    "special",
    "lora",
)

#: The sampler chain's member ids — the reviewed runtime's own
#: `--samplers` names, the FULL 9-member default order (the inf-1
#: slice carried the controllable five; inf-2 completes the chain to
#: the reviewed evidence's own order — DRY, top_n_sigma, typ_p and
#: XTC join as first-class members).
SAMPLER_CHAIN_IDS = (
    "penalties",
    "dry",
    "top_n_sigma",
    "top_k",
    "typ_p",
    "top_p",
    "min_p",
    "xtc",
    "temperature",
)

#: The chain member → the value controls it governs (membership is a
#: FAMILY concern: the "dry" chain step nullifies the whole DRY
#: family when disabled, never just its multiplier). The ids are the
#: SEMANTIC ids (`sampling.*`), the chain ids the runtime's own
#: `--samplers` names — two vocabularies, one mapping.
CHAIN_FAMILIES: Mapping[str, tuple[str, ...]] = {
    "penalties": (
        "sampling.repeat_penalty",
        "sampling.repeat_last_n",
        "sampling.presence_penalty",
        "sampling.frequency_penalty",
    ),
    "dry": (
        "sampling.dry_multiplier",
        "sampling.dry_base",
        "sampling.dry_allowed_length",
        "sampling.dry_penalty_last_n",
    ),
    "top_n_sigma": ("sampling.top_n_sigma",),
    "top_k": ("sampling.top_k",),
    "typ_p": ("sampling.typical",),
    "top_p": ("sampling.top_p",),
    "min_p": ("sampling.min_p",),
    "xtc": ("sampling.xtc_probability", "sampling.xtc_threshold"),
    "temperature": ("sampling.temperature",),
}


class InferenceError(ValueError):
    """An inference-contract violation (LOUD — a malformed profile, an
    out-of-range value, a relation conflict; never a silent clamp)."""


# --------------------------------------------------------------- the model


@dataclass(frozen=True)
class SemanticControl:
    """One semantic control's definition — the overlay's atom (the
    law's §3). Identity is the SEMANTIC id (``sampling.top_k``), never
    the raw flag; the flag is the raw mapping (shown in tooltips and
    the compile step, never the primary identity). The ``field`` is
    the PROFILE vocabulary (the persisted document's own key —
    stable across library growth); ``value_type``/``forms``/limits
    drive BOTH the store validation and the UI editors (one metadata
    source — the UI never re-encodes the vocabulary)."""

    id: str
    name: str
    category: str
    kind: str  # value | mode | toggle | chain | display
    scope: str  # spawn | request | spawn+request
    flag: str
    field: str
    value_doc: str
    value_type: str  # int | float | bool | enum | text | gpu_layers
    baseline: object
    upstream_default: object
    forms: tuple[str, ...] = ()
    minimum: float | None = None
    maximum: float | None = None
    step: float = 1.0
    disabled_form: object = None
    auto_form: object = None
    notes: tuple[str, ...] = ()
    status: str = "ACTIVE"  # ACTIVE | UNCLASSIFIED | LEGACY | REMOVED
    advanced: bool = False


def _c(
    cid: str,
    name: str,
    category: str,
    kind: str,
    scope: str,
    flag: str,
    profile_field: str,
    value_doc: str,
    baseline: object,
    upstream: object,
    *,
    value_type: str = "enum",
    forms: tuple[str, ...] = (),
    minimum: float | None = None,
    maximum: float | None = None,
    step: float = 1.0,
    disabled_form: object = None,
    auto_form: object = None,
    notes: tuple[str, ...] = (),
    status: str = "ACTIVE",
    advanced: bool = False,
) -> SemanticControl:
    """The library's compact constructor (one control per call site —
    the explicit style over a positional mega-table: reviewable,
    greppable, and the closed vocabulary rides each entry)."""
    return SemanticControl(
        id=cid,
        name=name,
        category=category,
        kind=kind,
        scope=scope,
        flag=flag,
        field=profile_field,
        value_doc=value_doc,
        value_type=value_type,
        baseline=baseline,
        upstream_default=upstream,
        forms=forms,
        minimum=minimum,
        maximum=maximum,
        step=step,
        disabled_form=disabled_form,
        auto_form=auto_form,
        notes=notes,
        status=status,
        advanced=advanced,
    )


def _library() -> tuple[SemanticControl, ...]:
    """The admitted control library (inf-2 — the FULL reviewed
    surface). The ``upstream_default`` fields are the reviewed
    snapshot's OWN values (runtime evidence, pinned 2026-09-25) —
    they are NOT the project baseline: ``baseline`` is CanonSim's own
    pin (§5's ladder: upstream default ≠ project baseline ≠ profile
    value). Text controls use "" as the not-emitted form; every
    ``disabled_form``/``auto_form`` is the runtime's OWN literal
    (0 / 1.0 / -1 / "auto"), never an application convention."""

    return (
        # ------------------------------------------------ model / runtime
        _c(
            "model.context", "Context", "model", "value", "spawn",
            "-c", "context",
            "int in [1, 2097152] tokens",
            8192, 0,
            value_type="int", minimum=1, maximum=2_097_152, step=512,
            notes=(
                "the upstream default 0 loads the context from model "
                "metadata — the workbench pins an explicit value (the "
                "compiled command never relies on the build's choice)",
            ),
        ),
        _c(
            "model.n_predict", "Predict", "model", "value", "spawn",
            "-n", "n_predict",
            "int in [-1, 2147483647] tokens (-1 = infinity)",
            -1, -1,
            value_type="int", minimum=-1, maximum=2_147_483_647,
            notes=(
                "the server-side generation cap; -1 = the runtime's own "
                "infinity form (per-request max_tokens rides the API)",
            ),
        ),
        _c(
            "model.keep", "Keep", "model", "value", "spawn",
            "--keep", "keep",
            "int in [-1, 2097152] tokens (-1 = all, 0 = none)",
            0, 0,
            value_type="int", minimum=-1, maximum=2_097_152,
        ),
        _c(
            "model.threads", "CPU Threads", "model", "value", "spawn",
            "-t", "threads",
            "int in [-1, 1024] (-1 = the build's own choice)",
            -1, -1,
            value_type="int", minimum=-1, maximum=1024,
            auto_form=-1,
            notes=(
                "-1 is the runtime's own default form (the build picks "
                "the thread count) — a real AUTO form, not 'unset'",
            ),
        ),
        _c(
            "model.threads_batch", "Batch Threads", "model", "value",
            "spawn", "-tb", "threads_batch",
            "int in [-1, 1024] (-1 = same as CPU Threads)",
            -1, -1,
            value_type="int", minimum=-1, maximum=1024,
            auto_form=-1,
        ),
        _c(
            "model.batch_size", "Batch Size", "model", "value", "spawn",
            "-b", "batch_size",
            "int in [1, 2097152] tokens (the logical batch)",
            2048, 2048,
            value_type="int", minimum=1, maximum=2_097_152, step=128,
        ),
        _c(
            "model.ubatch_size", "Ubatch Size", "model", "value",
            "spawn", "-ub", "ubatch_size",
            "int in [1, 2097152] tokens (the physical batch)",
            512, 512,
            value_type="int", minimum=1, maximum=2_097_152, step=64,
        ),
        # ------------------------------------------------------ device / GPU
        _c(
            "device.gpu_layers", "GPU Layers", "device", "mode", "spawn",
            "-ngl", "gpu_layers",
            "'auto' | 'all' | an exact layer count in [0, 999]",
            999, "auto",
            value_type="gpu_layers", forms=GPU_LAYER_FORMS,
            maximum=999, auto_form="auto",
            notes=(
                "AUTO ('auto') and ALL ('all') are the runtime's own "
                "literal forms — never 'unset' synonyms",
            ),
        ),
        _c(
            "device.flash_attention", "Flash Attention", "device",
            "mode", "spawn", "-fa", "flash_attention",
            "'auto' | 'on' | 'off'",
            "on", "auto",
            forms=FLASH_ATTENTION_FORMS, auto_form="auto",
            notes=(
                "the project baseline 'on' is an explicit pin, NOT the "
                "upstream default 'auto'",
            ),
        ),
        _c(
            "device.fit", "Fit", "device", "toggle", "spawn",
            "--fit", "fit",
            "'on' | 'off' — the automatic device-memory fitting",
            "on", "on",
            forms=FIT_FORMS,
            notes=(
                "a good starting point, NOT a guaranteed optimum — the "
                "chip specification's own risk note (an INFERENCE, not "
                "a fact: benchmark manual placement when it matters)",
            ),
        ),
        _c(
            "device.main_gpu", "Main GPU", "device", "value", "spawn",
            "-mg", "main_gpu",
            "int in [0, 64] (the GPU index; meaningful with split "
            "modes none/row)",
            0, 0,
            value_type="int", minimum=0, maximum=64,
        ),
        _c(
            "device.tensor_split", "Tensor Split", "device", "value",
            "spawn", "-ts", "tensor_split",
            "comma-separated fractions per GPU (e.g. '3,1'); empty = "
            "the runtime's own split",
            "", "",
            value_type="text", advanced=True,
        ),
        _c(
            "device.split_mode", "Split Mode", "device", "mode", "spawn",
            "-sm", "split_mode",
            "one of " + " | ".join(SPLIT_MODE_FORMS),
            "layer", "layer",
            forms=SPLIT_MODE_FORMS, advanced=True,
            notes=(
                "the snapshot lists the forms without a default — "
                "'layer' pinned per the historical value; re-verify "
                "against the installed binary (the §19 protocol)",
            ),
        ),
        # ------------------------------------------------------ memory / KV
        _c(
            "memory.cache_type_k", "KV Cache Type K", "memory", "mode",
            "spawn", "--cache-type-k", "cache_type_k",
            "one of " + " | ".join(KV_CACHE_TYPES),
            "f16", "f16",
            forms=KV_CACHE_TYPES,
            notes=(
                "quantized forms (q*_*) are build-sensitive — re-verify "
                "against the installed binary before relying on them",
            ),
        ),
        _c(
            "memory.cache_type_v", "KV Cache Type V", "memory", "mode",
            "spawn", "--cache-type-v", "cache_type_v",
            "one of " + " | ".join(KV_CACHE_TYPES),
            "f16", "f16",
            forms=KV_CACHE_TYPES,
            notes=(
                "quantized V forms are more restrictive than K on some "
                "builds — the runtime refuses loudly, never silently",
            ),
        ),
        _c(
            "memory.kv_offload", "KV Offload", "memory", "toggle",
            "spawn", "--kv-offload", "kv_offload",
            "'on' | 'off' — the KV cache offloading",
            True, True,
            value_type="bool", forms=("on", "off"),
        ),
        _c(
            "memory.kv_unified", "Unified KV", "memory", "toggle",
            "spawn", "--kv-unified", "kv_unified",
            "'on' | 'off' — one shared KV buffer across sequences",
            True, True,
            value_type="bool", forms=("on", "off"),
            notes=(
                "the runtime's own default is conditional ('enabled if "
                "number of slots is auto') — the profile pins it "
                "explicitly (the compiled command never leans on the "
                "build's conditional)",
            ),
        ),
        _c(
            "memory.cache_ram", "Cache RAM", "memory", "value", "spawn",
            "--cache-ram", "cache_ram",
            "int in [-1, 1048576] MiB (-1 = no limit)",
            8192, 8192,
            value_type="int", minimum=-1, maximum=1_048_576, step=256,
            advanced=True,
        ),
        _c(
            "memory.cache_reuse", "Cache Reuse", "memory", "value",
            "spawn", "--cache-reuse", "cache_reuse",
            "int in [0, 2097152] tokens (the min chunk for KV-shift "
            "reuse; 0 = disabled)",
            0, 0,
            value_type="int", minimum=0, maximum=2_097_152,
            disabled_form=0,
            notes=("requires prompt caching enabled",),
        ),
        _c(
            "memory.swa_full", "Full SWA Cache", "memory", "toggle",
            "spawn", "--swa-full", "swa_full",
            "'on' | 'off' — full-size SWA cache for SWA models",
            False, False,
            value_type="bool", forms=("on", "off"), advanced=True,
        ),
        # ---------------------------------------------------------- loading
        _c(
            "loading.load_mode", "Load Mode", "loading", "mode",
            "spawn", "--load-mode", "load_mode",
            "one of " + " | ".join(LOAD_MODE_FORMS),
            "auto", "auto",
            forms=LOAD_MODE_FORMS, auto_form="auto", advanced=True,
            notes=(
                "the reviewed forms replace the legacy --mmap/--mlock "
                "pair (the snapshot's own consolidation)",
            ),
        ),
        _c(
            "loading.warmup", "Warmup", "loading", "toggle", "spawn",
            "--warmup", "warmup",
            "'on' | 'off' — the empty warmup run",
            True, True,
            value_type="bool", forms=("on", "off"),
        ),
        _c(
            "loading.check_tensors", "Check Tensors", "loading",
            "toggle", "spawn", "--check-tensors", "check_tensors",
            "'on' | 'off' — validate tensor data on load",
            False, False,
            value_type="bool", forms=("on", "off"), advanced=True,
        ),
        _c(
            "loading.repack", "Weight Repack", "loading", "toggle",
            "spawn", "--repack", "repack",
            "'on' | 'off' — the weight repacking",
            True, True,
            value_type="bool", forms=("on", "off"), advanced=True,
        ),
        # --------------------------------------------------------------- MoE
        _c(
            "moe.cpu_moe", "MoE CPU", "moe", "toggle", "spawn",
            "--cpu-moe", "cpu_moe",
            "'on' | 'off' — ALL MoE expert weights in the CPU",
            False, False,
            value_type="bool", forms=("on", "off"),
        ),
        _c(
            "moe.n_cpu_moe", "MoE CPU Layers", "moe", "value", "spawn",
            "--n-cpu-moe", "n_cpu_moe",
            "int in [0, 999] — the MoE experts of the first N layers "
            "stay in the CPU (0 = none)",
            0, 0,
            value_type="int", minimum=0, maximum=999,
            disabled_form=0,
            notes=(
                "the dense-models twin is n_cpu_ffn; for MoE expert "
                "weights use THIS control (the --help's own split)",
            ),
        ),
        _c(
            "moe.n_cpu_ffn", "FFN CPU Layers", "moe", "value", "spawn",
            "--n-cpu-ffn", "n_cpu_ffn",
            "int in [0, 999] — the dense FFN of the first N layers "
            "stays in the CPU (0 = none)",
            0, 0,
            value_type="int", minimum=0, maximum=999,
            disabled_form=0, advanced=True,
        ),
        _c(
            "moe.override_tensor", "Tensor Override", "moe", "value",
            "spawn", "--override-tensor", "override_tensor",
            "'<pattern>=<buffer>,...' — the raw tensor-level override; "
            "empty = none",
            "", "",
            value_type="text", advanced=True,
            notes=(
                "the low-level escape for per-tensor placement (the "
                "raw syntax rides the value_doc — an expert control)",
            ),
        ),
        # ---------------------------------------------------------- CPU / NUMA
        _c(
            "cpu.numa", "NUMA", "cpu", "mode", "spawn",
            "--numa", "numa",
            "one of " + " | ".join(NUMA_FORMS) + " (off = not emitted)",
            "off", "off",
            forms=NUMA_FORMS, advanced=True,
            notes=(
                "'off' is the application's own not-emitted form — the "
                "runtime takes no --numa argument by default",
            ),
        ),

        # ------------------------------------------------------------ sampling
        _c(
            "sampling.temperature", "Temperature", "sampling", "value",
            "spawn+request", "--temp", "temperature",
            "a number in [0, 2]",
            0.8, 0.8,
            value_type="float", minimum=0, maximum=2, step=0.05,
            notes=(
                "0 = the deterministic (greedy) decoding state — the "
                "profile's other sampler values are PRESERVED, never "
                "deleted (the law's §11)",
            ),
        ),
        _c(
            "sampling.top_k", "Top-K", "sampling", "value", "spawn",
            "--top-k", "top_k",
            "an int in [0, 10000] (the runtime's own form: 0 = disabled)",
            40, 40,
            value_type="int", minimum=0, maximum=10_000,
            disabled_form=0,
            notes=("0 = disabled — a REAL off value, distinct from AUTO",),
        ),
        _c(
            "sampling.top_p", "Top-P", "sampling", "value", "spawn",
            "--top-p", "top_p",
            "a number in [0, 1] (the runtime's own form: 1.0 = disabled)",
            0.95, 0.95,
            value_type="float", minimum=0, maximum=1, step=0.01,
            disabled_form=1.0,
            notes=("1.0 = disabled — a REAL off value, distinct from AUTO",),
        ),
        _c(
            "sampling.min_p", "Min-P", "sampling", "value", "spawn",
            "--min-p", "min_p",
            "a number in [0, 1] (the runtime's own form: 0.0 = disabled)",
            0.05, 0.05,
            value_type="float", minimum=0, maximum=1, step=0.01,
            disabled_form=0.0,
            notes=("0.0 = disabled — a REAL off value, distinct from AUTO",),
        ),
        _c(
            "sampling.typical", "Typical-P", "sampling", "value",
            "spawn", "--typical", "typical",
            "a number in [0, 1] (the runtime's own form: 1.0 = disabled)",
            1.0, 1.0,
            value_type="float", minimum=0, maximum=1, step=0.01,
            disabled_form=1.0,
            notes=(
                "locally typical sampling — an alternative/tuning "
                "control, generally disabled in the reviewed baseline "
                "(the chip spec §2.6's own classification)",
            ),
        ),
        _c(
            "sampling.top_n_sigma", "Top-N-Sigma", "sampling", "value",
            "spawn", "--top-nsigma", "top_n_sigma",
            "a number in [-1, 10] (the runtime's own form: -1.0 = "
            "disabled)",
            -1.0, -1.0,
            value_type="float", minimum=-1, maximum=10, step=0.05,
            disabled_form=-1.0,
            notes=(
                "specialized distribution truncation — default disabled "
                "(the reviewed --help's own words)",
            ),
        ),
        _c(
            "sampling.repeat_penalty", "Repeat Penalty", "sampling",
            "value", "spawn", "--repeat-penalty", "repeat_penalty",
            "a number in [0, 4] (the runtime's own form: 1.0 = disabled)",
            1.1, 1.0,
            value_type="float", minimum=0, maximum=4, step=0.05,
            disabled_form=1.0,
            notes=(
                "the project baseline 1.1 is an explicit pin — the "
                "upstream default is 1.00 (disabled); §5's ladder in "
                "one control. Token-level generic repetition pressure — "
                "NOT the DRY sequence-aware family",
            ),
        ),
        _c(
            "sampling.repeat_last_n", "Repeat Window", "sampling",
            "value", "spawn", "--repeat-last-n", "repeat_last_n",
            "an int in [0, 2097152] tokens (0 = the penalty sees "
            "nothing)",
            64, 64,
            value_type="int", minimum=0, maximum=2_097_152,
            disabled_form=0,
        ),
        _c(
            "sampling.presence_penalty", "Presence Penalty", "sampling",
            "value", "spawn", "--presence-penalty", "presence_penalty",
            "a number in [-2, 2] (0 = disabled)",
            0.0, 0.0,
            value_type="float", minimum=-2, maximum=2, step=0.05,
            disabled_form=0.0,
        ),
        _c(
            "sampling.frequency_penalty", "Frequency Penalty",
            "sampling", "value", "spawn", "--frequency-penalty",
            "frequency_penalty",
            "a number in [-2, 2] (0 = disabled)",
            0.0, 0.0,
            value_type="float", minimum=-2, maximum=2, step=0.05,
            disabled_form=0.0,
        ),
        _c(
            "sampling.dry_multiplier", "DRY Multiplier", "sampling",
            "value", "spawn", "--dry-multiplier", "dry_multiplier",
            "a number in [0, 10] (the runtime's own form: 0.0 = "
            "disabled)",
            0.0, 0.0,
            value_type="float", minimum=0, maximum=10, step=0.05,
            disabled_form=0.0,
            notes=(
                "DRY is the MODERN phrase/sequence-aware repetition "
                "control (multiplier * base^(match_length - "
                "allowed_length)) — never bucketed 'legacy'",
            ),
        ),
        _c(
            "sampling.dry_base", "DRY Base", "sampling", "value",
            "spawn", "--dry-base", "dry_base",
            "a number in [0, 10] (the exponential growth base)",
            1.75, 1.75,
            value_type="float", minimum=0, maximum=10, step=0.05,
        ),
        _c(
            "sampling.dry_allowed_length", "DRY Allowed Length",
            "sampling", "value", "spawn", "--dry-allowed-length",
            "dry_allowed_length",
            "an int in [0, 2097152] tokens (the unpenalized prefix "
            "length)",
            2, 2,
            value_type="int", minimum=0, maximum=2_097_152,
        ),
        _c(
            "sampling.dry_penalty_last_n", "DRY Window", "sampling",
            "value", "spawn", "--dry-penalty-last-n",
            "dry_penalty_last_n",
            "an int in [0, 2097152] tokens (0 = the DRY penalty sees "
            "nothing)",
            64, 64,
            value_type="int", minimum=0, maximum=2_097_152,
            disabled_form=0,
        ),
        _c(
            "sampling.dry_sequence_breaker", "DRY Sequence Breakers",
            "sampling", "value", "spawn", "--dry-sequence-breaker",
            "dry_sequence_breaker",
            "a comma-separated token list; empty = the runtime's own "
            "default breakers ('\\n', ':', '\"', '*'), 'none' = no "
            "breakers",
            "", "",
            value_type="text", advanced=True,
            notes=(
                "the flag ADDS breakers and clears the defaults in the "
                "process — an empty value leaves the runtime's own set",
            ),
        ),
        _c(
            "sampling.xtc_probability", "XTC Probability", "sampling",
            "value", "spawn", "--xtc-probability", "xtc_probability",
            "a number in [0, 1] (the runtime's own form: 0.0 = "
            "disabled)",
            0.0, 0.0,
            value_type="float", minimum=0, maximum=1, step=0.01,
            disabled_form=0.0,
            notes=(
                "XTC is a MODERN diversity/anti-collapse mechanism — "
                "the min-p -> XTC combination is the reviewed upstream "
                "recommendation for creative generation; default-off is "
                "conservatism, not irrelevance",
            ),
        ),
        _c(
            "sampling.xtc_threshold", "XTC Threshold", "sampling",
            "value", "spawn", "--xtc-threshold", "xtc_threshold",
            "a number in [0, 1] (the runtime's own form: 1.0 = "
            "disabled)",
            0.10, 0.10,
            value_type="float", minimum=0, maximum=1, step=0.01,
            disabled_form=1.0,
        ),
        _c(
            "sampling.mirostat", "Mirostat", "sampling", "mode",
            "spawn", "--mirostat", "mirostat",
            "0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0 (the "
            "runtime's own forms)",
            0, 0,
            value_type="int", minimum=0, maximum=2, disabled_form=0,
            notes=(
                "a SEPARATE sampling strategy: when active, Top-K, "
                "Nucleus and Locally Typical samplers are IGNORED (the "
                "--help's own words — the resolver pins that relation)",
            ),
        ),
        _c(
            "sampling.mirostat_lr", "Mirostat Learning Rate",
            "sampling", "value", "spawn", "--mirostat-lr", "mirostat_lr",
            "a number in [0, 1] (the eta parameter)",
            0.10, 0.10,
            value_type="float", minimum=0, maximum=1, step=0.01,
        ),
        _c(
            "sampling.mirostat_ent", "Mirostat Target Entropy",
            "sampling", "value", "spawn", "--mirostat-ent",
            "mirostat_ent",
            "a number in [0, 20] (the tau parameter)",
            5.0, 5.0,
            value_type="float", minimum=0, maximum=20, step=0.1,
        ),
        _c(
            "sampling.dynatemp_range", "Dynatemp Range", "sampling",
            "value", "spawn", "--dynatemp-range", "dynatemp_range",
            "a number in [0, 10] (0 = disabled)",
            0.0, 0.0,
            value_type="float", minimum=0, maximum=10, step=0.05,
            disabled_form=0.0,
            notes=(
                "dynamic temperature is its OWN capability, never "
                "synonymous with adaptive-p (the chip spec §2.5)",
            ),
        ),
        _c(
            "sampling.dynatemp_exp", "Dynatemp Exponent", "sampling",
            "value", "spawn", "--dynatemp-exp", "dynatemp_exp",
            "a number in [0, 10]",
            1.0, 1.0,
            value_type="float", minimum=0, maximum=10, step=0.05,
        ),
        _c(
            "sampling.adaptive_target", "Adaptive-P Target", "sampling",
            "value", "spawn", "--adaptive-target", "adaptive_target",
            "a number in [-1, 1] (the runtime's own form: negative = "
            "disabled)",
            -1.0, -1.0,
            value_type="float", minimum=-1, maximum=1, step=0.01,
            disabled_form=-1.0,
            notes=(
                "adaptive-p targets probability/selection behavior via "
                "adaptive state/EMA — NOT a hard truncation filter and "
                "NOT a dynatemp synonym",
            ),
        ),
        _c(
            "sampling.adaptive_decay", "Adaptive-P Decay", "sampling",
            "value", "spawn", "--adaptive-decay", "adaptive_decay",
            "a number in [0, 0.99] (lower = more reactive)",
            0.90, 0.90,
            value_type="float", minimum=0, maximum=0.99, step=0.01,
        ),
        _c(
            "sampling.ignore_eos", "Ignore EOS", "sampling", "toggle",
            "spawn", "--ignore-eos", "ignore_eos",
            "'on' | 'off' — ignore the end-of-stream token (implies "
            "EOS logit suppression)",
            False, False,
            value_type="bool", forms=("on", "off"), advanced=True,
        ),
        _c(
            "sampling.logit_bias", "Logit Bias", "sampling", "value",
            "spawn", "--logit-bias", "logit_bias",
            "'TOKEN_ID(+/-)BIAS,...' — the raw token-level bias; empty "
            "= none",
            "", "",
            value_type="text", advanced=True,
            notes=(
                "token-specific: classified advanced/diagnostic, not "
                "general-purpose sampling (the chip spec §2.2A's own "
                "rule)",
            ),
        ),
        _c(
            "sampling.seed", "Seed", "sampling", "value", "spawn",
            "-s", "seed",
            "an int in [-1, 2147483647] (-1 = the runtime's random "
            "form)",
            -1, -1,
            value_type="int", minimum=-1, maximum=2_147_483_647,
            auto_form=-1,
            notes=(
                "-1 IS the random form (the runtime's own sentinel) — "
                "a fixed seed is not a bit-identical guarantee across "
                "execution shapes (the reviewed --help's own caveat)",
            ),
        ),
        # --------------------------------------------- chat / template / reasoning
        _c(
            "chat.template", "Chat Template", "chat", "mode", "spawn",
            "--jinja", "chat_template",
            "MODEL DEFAULT (the model's own template) | GENERIC (the "
            "server's fallback) | CUSTOM (an explicit jinja template)",
            "model_default", "model_default",
            forms=CHAT_TEMPLATE_FORMS,
            notes=(
                "the template is a BEHAVIORAL PROTOCOL, not formatting — "
                "model metadata wins unless there is a concrete reason "
                "to override; CUSTOM overrides it (the §12 relation)",
            ),
        ),
        _c(
            "chat.template_custom", "Custom Template", "chat", "value",
            "spawn", "--chat-template", "chat_template_custom",
            "the explicit jinja template string (only meaningful with "
            "Chat Template = CUSTOM)",
            "", "",
            value_type="text", advanced=True,
        ),
        _c(
            "chat.reasoning", "Reasoning", "chat", "mode", "spawn",
            "-rea", "reasoning",
            "one of " + " | ".join(REASONING_FORMS) + " (auto = detect "
            "from the template)",
            "auto", "auto",
            forms=REASONING_FORMS, auto_form="auto",
        ),
        _c(
            "chat.reasoning_format", "Reasoning Format", "chat",
            "mode", "spawn", "--reasoning-format", "reasoning_format",
            "one of " + " | ".join(REASONING_FORMAT_FORMS),
            "auto", "auto",
            forms=REASONING_FORMAT_FORMS,
        ),
        _c(
            "chat.reasoning_effort", "Reasoning Effort", "chat",
            "mode", "spawn", "--reasoning-effort", "reasoning_effort",
            "one of " + " | ".join(REASONING_EFFORT_FORMS),
            "default", "default",
            forms=REASONING_EFFORT_FORMS,
            notes=(
                "reasoning controls are model/template-dependent (the "
                "chip spec §4.2's own caveat)",
            ),
        ),
        _c(
            "chat.reasoning_budget", "Reasoning Budget", "chat",
            "value", "spawn", "--reasoning-budget", "reasoning_budget",
            "an int in [-1, 2097152] tokens (-1 = unrestricted, 0 = "
            "immediate end)",
            -1, -1,
            value_type="int", minimum=-1, maximum=2_097_152,
        ),
        _c(
            "chat.prefill_assistant", "Prefill Assistant", "chat",
            "toggle", "spawn", "--prefill-assistant",
            "prefill_assistant",
            "'on' | 'off' — prefill the assistant's response when the "
            "last message is an assistant message",
            True, True,
            value_type="bool", forms=("on", "off"), advanced=True,
        ),
        # --------------------------------------------------- structured output
        _c(
            "structured.grammar", "GBNF Grammar", "structured", "value",
            "spawn", "--grammar", "grammar",
            "the BNF-like grammar text; empty = unconstrained",
            "", "",
            value_type="text", advanced=True,
            notes=(
                "a spawn-time DEFAULT constraint — the per-request "
                "grammar rides the chat request surface (a later row)",
            ),
        ),
        _c(
            "structured.json_schema", "JSON Schema", "structured",
            "value", "spawn", "-j", "json_schema",
            "the JSON schema text; empty = unconstrained",
            "", "",
            value_type="text", advanced=True,
        ),
        # ------------------------------------------------ server / concurrency
        _c(
            "server.parallel", "Parallel Slots", "server", "value",
            "spawn", "-np", "parallel",
            "an int in [-1, 512] (the runtime's own form: -1 = auto)",
            -1, -1,
            value_type="int", minimum=-1, maximum=512,
            auto_form=-1,
        ),
        _c(
            "server.cont_batching", "Continuous Batching", "server",
            "toggle", "spawn", "-cb", "cont_batching",
            "'on' | 'off' — the dynamic batching",
            True, True,
            value_type="bool", forms=("on", "off"),
        ),
        _c(
            "server.context_shift", "Context Shift", "server", "toggle",
            "spawn", "--context-shift", "context_shift",
            "'on' | 'off' — context shift on infinite text generation",
            False, False,
            value_type="bool", forms=("on", "off"),
            notes=(
                "the reviewed default is DISABLED — the snapshot's own "
                "word, pinned here verbatim",
            ),
        ),
        _c(
            "server.cache_prompt", "Prompt Caching", "server", "toggle",
            "spawn", "--cache-prompt", "cache_prompt",
            "'on' | 'off' — the prompt cache",
            True, True,
            value_type="bool", forms=("on", "off"),
        ),
        # ----------------------------------------------------- observability
        _c(
            "observability.metrics", "Prometheus Metrics",
            "observability", "toggle", "spawn", "--metrics", "metrics",
            "'on' | 'off' — the prometheus-compatible endpoint",
            False, False,
            value_type="bool", forms=("on", "off"),
        ),
        _c(
            "observability.log_jsonl", "JSONL Logging", "observability",
            "toggle", "spawn", "--log-jsonl", "log_jsonl",
            "'on' | 'off' — one JSON object per line to stdout",
            False, False,
            value_type="bool", forms=("on", "off"),
        ),
        _c(
            "observability.perf", "Internal Timings", "observability",
            "toggle", "spawn", "--perf", "perf",
            "'on' | 'off' — the libllama performance timings",
            False, False,
            value_type="bool", forms=("on", "off"),
        ),
        # -------------------------------------------------- speculative decoding
        _c(
            "speculative.type", "Speculative Decoding", "speculative",
            "mode", "spawn", "--spec-type", "spec_type",
            "one of " + " | ".join(SPEC_TYPE_FORMS),
            "none", "none",
            forms=SPEC_TYPE_FORMS, advanced=True,
            notes=(
                "the modern surface replaces the legacy --draft*/"
                "--spec-ngram-* flags (LEGACY/REMOVED — searchable "
                "later, never emitted)",
            ),
        ),
        _c(
            "speculative.draft_model", "Draft Model", "speculative",
            "value", "spawn", "--spec-draft-model", "spec_draft_model",
            "the draft GGUF path; empty = the type's own default",
            "", "",
            value_type="text", advanced=True,
        ),
        # ------------------------------------------------------ RoPE / YaRN
        _c(
            "rope.scaling", "RoPE Scaling", "rope", "mode", "spawn",
            "--rope-scaling", "rope_scaling",
            "one of " + " | ".join(ROPE_SCALING_FORMS) + " (model = the "
            "model's own metadata wins)",
            "model", "model",
            forms=ROPE_SCALING_FORMS, advanced=True,
            notes=(
                "the runtime's default is 'linear unless specified by "
                "model' — 'model' is the not-emitted form that leaves "
                "the resolution to the runtime",
            ),
        ),
        _c(
            "rope.freq_base", "RoPE Freq Base", "rope", "value",
            "spawn", "--rope-freq-base", "rope_freq_base",
            "a number in [0, 1000000000] (0 = loaded from model)",
            0.0, 0.0,
            value_type="float", minimum=0, maximum=1_000_000_000,
            step=1000, advanced=True,
        ),
        _c(
            "rope.freq_scale", "RoPE Freq Scale", "rope", "value",
            "spawn", "--rope-freq-scale", "rope_freq_scale",
            "a number in [0, 10] (0 = loaded from model)",
            0.0, 0.0,
            value_type="float", minimum=0, maximum=10, step=0.01,
            advanced=True,
        ),
        _c(
            "rope.yarn_orig_ctx", "YaRN Original Context", "rope",
            "value", "spawn", "--yarn-orig-ctx", "yarn_orig_ctx",
            "an int in [0, 2097152] (0 = the model's training context)",
            0, 0,
            value_type="int", minimum=0, maximum=2_097_152,
            advanced=True,
        ),
        _c(
            "rope.yarn_ext_factor", "YaRN Extrapolation Mix", "rope",
            "value", "spawn", "--yarn-ext-factor", "yarn_ext_factor",
            "a number in [-1, 10] (-1 = the runtime's auto form)",
            -1.0, -1.0,
            value_type="float", minimum=-1, maximum=10, step=0.01,
            auto_form=-1.0, advanced=True,
        ),
        _c(
            "rope.yarn_attn_factor", "YaRN Attention Magnitude", "rope",
            "value", "spawn", "--yarn-attn-factor", "yarn_attn_factor",
            "a number in [-1, 10] (-1 = the runtime's auto form)",
            -1.0, -1.0,
            value_type="float", minimum=-1, maximum=10, step=0.01,
            auto_form=-1.0, advanced=True,
        ),
        _c(
            "rope.yarn_beta_fast", "YaRN Beta Fast", "rope", "value",
            "spawn", "--yarn-beta-fast", "yarn_beta_fast",
            "a number in [-1, 10] (-1 = the runtime's auto form)",
            -1.0, -1.0,
            value_type="float", minimum=-1, maximum=10, step=0.01,
            auto_form=-1.0, advanced=True,
        ),
        _c(
            "rope.yarn_beta_slow", "YaRN Beta Slow", "rope", "value",
            "spawn", "--yarn-beta-slow", "yarn_beta_slow",
            "a number in [-1, 10] (-1 = the runtime's auto form)",
            -1.0, -1.0,
            value_type="float", minimum=-1, maximum=10, step=0.01,
            auto_form=-1.0, advanced=True,
        ),
        # ------------------------------------------------------ special modes
        _c(
            "special.embedding", "Embeddings Mode", "special",
            "toggle", "spawn", "--embedding", "embedding",
            "'on' | 'off' — restrict to the embedding use case (only "
            "with dedicated embedding models)",
            False, False,
            value_type="bool", forms=("on", "off"), advanced=True,
        ),
        _c(
            "special.mmproj", "Multimodal Projector", "special",
            "value", "spawn", "-mm", "mmproj",
            "the projector GGUF path; empty = the runtime's automatic "
            "resolution",
            "", "",
            value_type="text", advanced=True,
        ),
        # --------------------------------------------------------------- LoRA
        _c(
            "lora.adapter", "LoRA Adapter", "lora", "value", "spawn",
            "--lora", "lora",
            "the LoRA adapter path; empty = none (comma-separated for "
            "multiple)",
            "", "",
            value_type="text", advanced=True,
        ),
    )


#: The control library — the semantic overlay's admitted set.
CONTROL_LIBRARY: tuple[SemanticControl, ...] = _library()

_CONTROL_INDEX: dict[str, SemanticControl] = {
    control.id: control for control in CONTROL_LIBRARY
}

_FIELD_INDEX: dict[str, SemanticControl] = {
    control.field: control for control in CONTROL_LIBRARY
}

#: The profile's value fields (the persisted document's closed set —
#: name/sampler_chain/pinned are the document's own companions).
_FIELDS: tuple[str, ...] = tuple(
    control.field for control in CONTROL_LIBRARY
)


# ---------------------------------------------------------------- the chain


@dataclass(frozen=True)
class ChainItem:
    """One sampler chain member's profile state (the law's §11): a
    sampler chain is an ORDERED semantic object — membership +
    position are first-class, never a favorites grid. `enabled`
    decides whether the member is emitted into `--samplers`."""

    id: str
    enabled: bool


#: The chain's default document (the reviewed runtime's own order,
#: every member enabled).
DEFAULT_CHAIN: tuple[ChainItem, ...] = tuple(
    ChainItem(member, True) for member in SAMPLER_CHAIN_IDS
)


def _upgrade_chain(loaded: Mapping[str, bool]) -> tuple[ChainItem, ...]:
    """The inf-1 → inf-2 chain upgrade (the load-time normalization):
    a 5-member profile's chain grows to the library's 9-member set —
    the MISSING members insert at their canonical positions (each
    before the first present member that follows it canonically),
    the present members keep their loaded order and enabled state.
    Non-destructive: never reorders what the operator already set."""
    order: list[str] = [
        member for member in loaded if member in SAMPLER_CHAIN_IDS
    ]
    for member in SAMPLER_CHAIN_IDS:
        if member in loaded:
            continue
        canonical = SAMPLER_CHAIN_IDS.index(member)
        insert_at = len(order)
        for position, present in enumerate(order):
            if SAMPLER_CHAIN_IDS.index(present) > canonical:
                insert_at = position
                break
        order.insert(insert_at, member)
    return tuple(ChainItem(member, bool(loaded.get(member, True))) for member in order)


# --------------------------------------------------------------- the presets


@dataclass(frozen=True)
class InferencePreset:
    """A named configuration STARTING POINT (the law's §14 — the chip
    specification §30's own recommended set). A preset is NEVER an
    opaque mode: it applies as a TRANSPARENT diff (the UI previews
    every field it would change) and the chips stay editable after
    the apply. The values are the spec's own numbers where it pins
    them; where it pins only structure, the value is CanonSim's
    documented starting point — never an invented upstream truth."""

    id: str
    name: str
    description: str
    values: Mapping[str, object]


#: The four §30 presets (evidence-pinned).
PRESETS: tuple[InferencePreset, ...] = (
    InferencePreset(
        "general_chat",
        "General chat",
        "the §30 general-chat baseline: the stable core, every "
        "specialized sampler off",
        {
            "temperature": 0.8,
            "top_p": 0.95,
            "min_p": 0.05,
            "top_k": 40,
            "repeat_penalty": 1.0,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "dry_multiplier": 0.0,
            "xtc_probability": 0.0,
            "mirostat": 0,
            "typical": 1.0,
            "top_n_sigma": -1.0,
            "adaptive_target": -1.0,
            "dynatemp_range": 0.0,
        },
    ),
    InferencePreset(
        "long_form",
        "Long-form / anti-loop",
        "the §30 long-form arm: the general baseline + DRY on (the "
        "0.8 multiplier is CanonSim's documented starting point — the "
        "spec pins the structure, not the number); evaluate, never "
        "stack every anti-repetition mechanism blindly",
        {
            "temperature": 0.8,
            "top_p": 0.95,
            "min_p": 0.05,
            "top_k": 40,
            "repeat_penalty": 1.0,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "dry_multiplier": 0.8,
            "xtc_probability": 0.0,
            "mirostat": 0,
            "typical": 1.0,
            "top_n_sigma": -1.0,
            "adaptive_target": -1.0,
            "dynatemp_range": 0.0,
        },
    ),
    InferencePreset(
        "adaptive_sampling",
        "Adaptive sampling",
        "the §30 adaptive arm: min-p + adaptive-p as a coherent mode "
        "(min-p preceding, adaptive-p the terminal position) — the "
        "0.75 target is CanonSim's starting point, tune per model; "
        "never a sampler soup",
        {
            "temperature": 0.8,
            "min_p": 0.02,
            "top_p": 1.0,
            "top_k": 0,
            "repeat_penalty": 1.0,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "dry_multiplier": 0.0,
            "xtc_probability": 0.0,
            "mirostat": 0,
            "typical": 1.0,
            "top_n_sigma": -1.0,
            "adaptive_target": 0.75,
            "adaptive_decay": 0.90,
            "dynatemp_range": 0.0,
        },
    ),
    InferencePreset(
        "deterministic",
        "Deterministic / structured",
        "the §30 deterministic arm: temperature 0 (greedy decoding — "
        "the profile's other sampler values are PRESERVED and "
        "returnable; pair with grammar/JSON schema when structure "
        "must be enforced)",
        {"temperature": 0.0},
    ),
)


# --------------------------------------------------------------- the relations


@dataclass(frozen=True)
class Condition:
    """One typed relation predicate — a field/op/value triple over
    the PROFILE VALUES (semantic conditions, never bare flag-name
    pairs — the law's §12)."""

    field: str
    op: str  # "eq" | "ne" | "gt" | "ge" | "lt"
    value: object

    def holds(self, values: Mapping[str, object]) -> bool:
        current = values.get(self.field)
        if self.op == "eq":
            return current == self.value
        if self.op == "ne":
            return current != self.value
        if isinstance(current, bool) or current is None:
            return False
        if not isinstance(current, (int, float)):
            return False
        if self.op == "gt":
            return float(current) > float(self.value)  # type: ignore[arg-type]
        if self.op == "ge":
            return float(current) >= float(self.value)  # type: ignore[arg-type]
        return float(current) < float(self.value)  # lt


@dataclass(frozen=True)
class Requires:
    """``requires`` — the condition for meaningful use: the control's
    value is ACCEPTED and PRESERVED but carries no effect until the
    condition lands (rendered INEFFECTIVE with the reason — the law's
    §7 vocabulary, never a hidden drop)."""

    control: str  # the semantic id
    when: Condition
    reason: str


@dataclass(frozen=True)
class EffectiveNoop:
    """``effective_noop`` — accepted but NULLIFIED: when the condition
    holds, every target control stays CONFIGURED and VISIBLE with the
    reason (the chip spec §19's own example: Mirostat active + top-k
    configured -> top-k ineffective)."""

    when: Condition
    targets: tuple[str, ...]  # the semantic ids made ineffective
    reason: str


#: The relations this build pins (each sourced from the runtime
#: evidence or the chip specification's own law — never invented).
RELATIONS: tuple[Requires | EffectiveNoop, ...] = (
    # the --mirostat --help's OWN words: "Top K, Nucleus and Locally
    # Typical samplers are ignored if used"
    EffectiveNoop(
        Condition("mirostat", "ne", 0),
        ("sampling.top_k", "sampling.top_p", "sampling.typical"),
        "Mirostat is active — Top K, Nucleus and Locally Typical "
        "samplers are ignored (the --help's own words); the values "
        "are preserved",
    ),
    # the chip spec §3.4: temperature 0 = the deterministic decoding
    # state — the distribution-shaping controls are ignored
    EffectiveNoop(
        Condition("temperature", "eq", 0.0),
        (
            "sampling.top_n_sigma",
            "sampling.top_k",
            "sampling.typical",
            "sampling.top_p",
            "sampling.min_p",
            "sampling.xtc_probability",
            "sampling.xtc_threshold",
            "sampling.repeat_penalty",
            "sampling.repeat_last_n",
            "sampling.presence_penalty",
            "sampling.frequency_penalty",
            "sampling.dry_multiplier",
            "sampling.dry_base",
            "sampling.dry_allowed_length",
            "sampling.dry_penalty_last_n",
        ),
        "temperature 0 is the deterministic decoding state — the "
        "distribution-shaping controls are ignored; the configured "
        "values are preserved (return by restoring temperature)",
    ),
    # the DRY family requires the multiplier
    Requires(
        "sampling.dry_base",
        Condition("dry_multiplier", "eq", 0.0),
        "DRY is off (multiplier 0) — the base carries no effect until "
        "DRY is enabled; the value is preserved",
    ),
    Requires(
        "sampling.dry_allowed_length",
        Condition("dry_multiplier", "eq", 0.0),
        "DRY is off (multiplier 0) — the allowed length carries no "
        "effect until DRY is enabled; the value is preserved",
    ),
    Requires(
        "sampling.dry_penalty_last_n",
        Condition("dry_multiplier", "eq", 0.0),
        "DRY is off (multiplier 0) — the window carries no effect "
        "until DRY is enabled; the value is preserved",
    ),
    # the Mirostat family requires the mode
    Requires(
        "sampling.mirostat_lr",
        Condition("mirostat", "eq", 0),
        "Mirostat is off — the learning rate carries no effect until "
        "Mirostat is enabled; the value is preserved",
    ),
    Requires(
        "sampling.mirostat_ent",
        Condition("mirostat", "eq", 0),
        "Mirostat is off — the target entropy carries no effect until "
        "Mirostat is enabled; the value is preserved",
    ),
    # dynatemp-exp requires the range
    Requires(
        "sampling.dynatemp_exp",
        Condition("dynatemp_range", "eq", 0.0),
        "dynamic temperature is off (range 0) — the exponent carries "
        "no effect until the range is set; the value is preserved",
    ),
    # adaptive-decay requires the target
    Requires(
        "sampling.adaptive_decay",
        Condition("adaptive_target", "lt", 0.0),
        "adaptive-p is off (target negative) — the decay carries no "
        "effect until the target is set; the value is preserved",
    ),
    # XTC threshold requires the probability
    Requires(
        "sampling.xtc_threshold",
        Condition("xtc_probability", "eq", 0.0),
        "XTC is off (probability 0) — the threshold carries no effect "
        "until XTC is enabled; the value is preserved",
    ),
    # the speculative draft model requires a non-none type
    Requires(
        "speculative.draft_model",
        Condition("spec_type", "eq", "none"),
        "speculative decoding is off (type none) — the draft model "
        "carries no effect until a type is chosen; the value is "
        "preserved",
    ),
    # the custom template requires the CUSTOM mode
    Requires(
        "chat.template_custom",
        Condition("chat_template", "ne", "custom"),
        "the custom template text applies only with Chat Template = "
        "CUSTOM — with MODEL DEFAULT/GENERIC it carries no effect; the "
        "value is preserved",
    ),
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


# ------------------------------------------------------------- the resolver


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

    The relation set this build pins (each sourced from the runtime
    evidence or the chip specification's own law — never invented):
    the mirostat effective_noop (the --help's own ignored-samplers
    list), the temperature-0 deterministic noop (the whole
    distribution-shaping family, values PRESERVED), the family
    ``requires`` (DRY/Mirostat/dynatemp/adaptive/XTC/speculative/
    custom-template), and the chain-membership noop (a disabled
    member's whole VALUE family).

    The request layer: an EXPLICIT request temperature overrides the
    BASE value (§19.1's call-local layer); seed's request scope waits
    for its adapter consumer (the honest DEFERRED note rides the
    document)."""
    # ---- composition (BASE -> call-local), the request layer
    values: dict[str, object] = dict(profile.values)
    temperature = (
        float(request_temperature)
        if request_temperature is not None
        else values.get("temperature", 0.8)
    )
    values["temperature"] = temperature
    deterministic = temperature == 0.0
    chain_enabled: dict[str, bool] = {
        item.id: item.enabled for item in profile.sampler_chain
    }
    # the chain membership -> the value families it governs
    chain_disabled_controls: set[str] = set()
    for member, family in CHAIN_FAMILIES.items():
        if not chain_enabled.get(member, True):
            chain_disabled_controls.update(family)

    def control_document(control: SemanticControl) -> dict[str, object]:
        value = values.get(control.field, control.baseline)
        if control.id == "sampling.temperature":
            source = (
                "request" if request_temperature is not None else "profile"
            )
        else:
            source = "profile"
        state = "EFFECTIVE"
        reasons: list[str] = []
        # 1. the capability status first (a LEGACY/REMOVED control is
        # never silently rendered as healthy)
        if control.status in ("LEGACY", "REMOVED", "UNCLASSIFIED"):
            state = control.status
        # 2. the AUTO form (a REAL runtime form, never 'unset')
        if state == "EFFECTIVE" and control.auto_form is not None:
            if value == control.auto_form:
                state = "AUTO"
                if control.id == "sampling.seed":
                    reasons.append(
                        "-1 is the runtime's random-seed form (the "
                        "--help's own sentinel, not an application "
                        "convention)"
                    )
        # 3. the runtime's own disabled forms (INACTIVE: a REAL off
        # value, distinct from AUTO)
        if state in ("EFFECTIVE", "AUTO") and control.disabled_form is not None:
            if value == control.disabled_form:
                state = "INACTIVE"
                reasons.append(
                    f"{control.flag} {value} is the runtime's own "
                    "disabled form (a real off value, distinct from AUTO)"
                )
        # 4. the relations (INEFFECTIVE: accepted, preserved, with the
        # mandatory reason — never hidden)
        if state in ("EFFECTIVE", "AUTO"):
            for relation in RELATIONS:
                if isinstance(relation, EffectiveNoop):
                    if control.id in relation.targets and relation.when.holds(
                        values
                    ):
                        if state != "INEFFECTIVE":
                            state = "INEFFECTIVE"
                        reasons.append(relation.reason)
                elif relation.control == control.id and relation.when.holds(
                    values
                ):
                    if state != "INEFFECTIVE":
                        state = "INEFFECTIVE"
                    reasons.append(relation.reason)
        # 5. the chain-membership noop (the family concern)
        if (
            state in ("EFFECTIVE", "AUTO")
            and control.id in chain_disabled_controls
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
            "field": control.field,
            "value": value,
            "value_doc": control.value_doc,
            "value_type": control.value_type,
            "forms": list(control.forms),
            "minimum": control.minimum,
            "maximum": control.maximum,
            "step": control.step,
            "advanced": control.advanced,
            "source": source,
            "state": state,
            "reasons": reasons,
            "baseline": control.baseline,
            "upstream_default": control.upstream_default,
            "notes": list(control.notes),
        }

    controls = [control_document(c) for c in CONTROL_LIBRARY]
    chain_document = []
    for index, item in enumerate(profile.sampler_chain):
        control = _CONTROL_INDEX.get(f"sampling.{item.id}")
        value = (
            values.get(control.field, control.baseline)
            if control is not None
            else None
        )
        state, reasons = _chain_item_state(item, deterministic, values)
        chain_document.append(
            {
                "id": item.id,
                "name": control.name if control is not None else item.id,
                "enabled": item.enabled,
                "order": index,
                "value": value,
                "state": state,
                "reasons": reasons,
            }
        )
    categories = [
        {
            "id": category,
            "controls": sum(
                1 for control in CONTROL_LIBRARY
                if control.category == category
            ),
        }
        for category in CATEGORIES
        if any(control.category == category for control in CONTROL_LIBRARY)
    ]
    return {
        "profile_name": profile.name,
        "categories": categories,
        "controls": controls,
        "sampler_chain": chain_document,
        "chain_order": [item.id for item in profile.sampler_chain],
        "deterministic": deterministic,
        "presets": [
            {
                "id": preset.id,
                "name": preset.name,
                "description": preset.description,
                "values": dict(preset.values),
            }
            for preset in PRESETS
        ],
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


def _chain_item_state(
    item: ChainItem, deterministic: bool, values: Mapping[str, object]
) -> tuple[str, list[str]]:
    """One chain member's resolved state (the §11 document): the
    membership, the deterministic noop and the disabled-by-value form
    in precedence order — each with its mandatory reason."""
    if not item.enabled:
        return "INEFFECTIVE", [
            "the sampler is not in the emitted chain (enabled = false)"
        ]
    if deterministic and item.id != "temperature":
        return "INEFFECTIVE", [
            "temperature 0 is the deterministic decoding state — "
            "ignored; the configured value is preserved"
        ]
    control = _CONTROL_INDEX.get(f"sampling.{item.id}")
    if control is not None and control.disabled_form is not None:
        if values.get(control.field, control.baseline) == control.disabled_form:
            return "INACTIVE", [
                f"{control.flag} {values.get(control.field)} is the "
                "runtime's own disabled form (a real off value)"
            ]
    mirostat_on = values.get("mirostat", 0) != 0
    if mirostat_on and item.id in ("top_k", "top_p", "typ_p"):
        return "INEFFECTIVE", [
            "Mirostat is active — Top K, Nucleus and Locally Typical "
            "samplers are ignored (the --help's own words)"
        ]
    return "EFFECTIVE", []


# ---------------------------------------------------------------- the store


class InferenceStore:
    """The inference-profile owner: load (loud) → current() → update()
    (validate + apply + persist atomically). Thread-safe (the gateway
    dispatches on worker threads; the composition root reads
    `current()` at each spawn — settings.py's own policy-clock law).

    The persisted document carries TWO named sections (one file, one
    authority, never a second store): `profile` (the §19.1 BASE
    document: name + values + the chain) and `workspace` (the §14
    live state: the pinned control ids — an absent section is the
    honest empty, the file predates the section)."""

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
        self._profile, self._pinned = self._load()

    @property
    def path(self) -> Path:
        return self._path

    def current(self) -> InferenceProfile:
        with self._lock:
            return self._profile

    def pinned(self) -> tuple[str, ...]:
        """The workspace's pinned control ids (§14 — the ordering
        policy's own first rung: an explicit personal pin)."""
        with self._lock:
            return self._pinned

    def update(self, partial: Mapping[str, object]) -> InferenceProfile:
        """§19.1's REQUESTED→ACCEPTED→EFFECTIVE half: validate the
        CLOSED partial document (absent fields unchanged), apply, and
        persist atomically — the returned value is the new current.
        The `pinned` key routes to the WORKSPACE section (never the
        profile values); `name`/`sampler_chain`/value fields route to
        the profile."""
        if not isinstance(partial, Mapping):
            raise InferenceError("the update payload must be a mapping")
        allowed = {"name", "sampler_chain", "pinned", *_FIELDS}
        unknown = sorted(set(partial) - allowed)
        if unknown:
            raise InferenceError(
                f"unknown field(s) {unknown} (closed set: {list(allowed)})"
            )
        accepted = {
            name: _validate_field(name, value)
            for name, value in partial.items()
        }
        with self._lock:
            new_values = {
                **self._profile.values,
                **{
                    key: value
                    for key, value in accepted.items()
                    if key in _FIELDS
                },
            }
            updated = replace(
                self._profile,
                name=accepted.get("name", self._profile.name),
                values=new_values,
                sampler_chain=accepted.get(
                    "sampler_chain", self._profile.sampler_chain
                ),
            )
            self._profile = updated
            if "pinned" in accepted:
                self._pinned = accepted["pinned"]  # type: ignore[assignment]
            self._persist_locked(self._profile, self._pinned)
            return self._profile

    # ------------------------------------------------------------ private

    def _load(self) -> tuple[InferenceProfile, tuple[str, ...]]:
        """The §16 startup/recovery read (settings.py's own law): a
        MISSING file is the honest defaults (the file appears on the
        first save); a corrupt or schema-mismatched file refuses
        LOUD — never a silently-reset profile. The inf-1 → inf-2
        chain upgrade rides here (§_upgrade_chain: the 5-member chain
        grows to the 9-member set, the operator's order preserved)."""
        if not self._path.exists():
            return InferenceProfile(), ()
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
        unknown_top = sorted(set(document) - {"schema", "profile", "workspace"})
        if unknown_top:
            raise InferenceError(
                f"the inference profile carries unknown section(s) "
                f"{unknown_top} (closed set: ['profile', 'workspace'])"
            )
        body = document.get("profile")
        if not isinstance(body, dict):
            raise InferenceError(
                f"the inference profile {str(self._path)!r} has no profile "
                "object"
            )
        workspace = document.get("workspace", {})
        if not isinstance(workspace, dict):
            raise InferenceError(
                f"the inference profile {str(self._path)!r} has a "
                "malformed workspace section"
            )
        pinned_raw = workspace.get("pinned", [])
        pinned = _validate_pinned(pinned_raw)
        unknown = sorted(set(body) - {"name", "sampler_chain", *_FIELDS})
        if unknown:
            raise InferenceError(
                f"the inference profile carries unknown field(s) {unknown} "
                f"(closed set: {list(_FIELDS)})"
            )
        chain_raw = body.get("sampler_chain")
        if chain_raw is not None:
            if not isinstance(chain_raw, list) or not chain_raw:
                raise InferenceError(
                    "the persisted sampler_chain must be a non-empty list"
                )
            loaded: dict[str, bool] = {}
            for item in chain_raw:
                if (
                    not isinstance(item, dict)
                    or set(item) != {"id", "enabled"}
                    or item["id"] not in SAMPLER_CHAIN_IDS
                    or not isinstance(item["enabled"], bool)
                ):
                    raise InferenceError(
                        "the persisted sampler_chain carries a malformed "
                        f"member {item!r}"
                    )
                loaded[str(item["id"])] = bool(item["enabled"])
            chain = _upgrade_chain(loaded)
        else:
            chain = DEFAULT_CHAIN
        accepted = {
            name: _validate_field(name, value)
            for name, value in body.items()
            if name not in ("name", "sampler_chain")
        }
        name = (
            _validate_field("name", body["name"]) if "name" in body else "Baseline"
        )
        profile = replace(
            InferenceProfile(),
            name=name,
            values={**dict(InferenceProfile().values), **accepted},
            sampler_chain=chain,
        )
        return profile, pinned

    def _persist_locked(
        self, profile: InferenceProfile, pinned: tuple[str, ...]
    ) -> None:
        """The atomic write (§15's crash-safety half): a tmp file in
        the same directory + os.replace — a crash never leaves a
        half-written profile behind."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            document = {
                "schema": SCHEMA,
                "profile": profile.as_document(),
                "workspace": {"pinned": list(pinned)},
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
        profile = replace(
            InferenceProfile(),
            values={**dict(InferenceProfile().values), **accepted},
        )
        inference_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = inference_path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(
                {
                    "schema": SCHEMA,
                    "profile": profile.as_document(),
                    "workspace": {"pinned": []},
                },
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
    control — the law's §6/§8) + the workspace's pinned ids + the
    compiled-preview evidence + the honest next-spawn note (a LIVE
    server keeps its spawn flags until unloaded — settings.py's own
    law, verbatim)."""
    profile = store.current()
    resolved = resolve(profile, request_temperature=request_temperature)
    live_now = bool(live is not None and live())
    pinned = list(store.pinned())
    document: dict[str, object] = {
        **resolved,
        "profile": profile.as_document(),
        "pinned": pinned,
        "managed_live": live_now,
        "applies": "next-spawn",
    }
    if compiled_preview is not None:
        document["compiled_preview"] = compiled_preview(
            profile.as_document()
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
    return float(profile.values.get("temperature", 0.8))  # type: ignore[arg-type]


def compile_semantic(profile: InferenceProfile) -> dict[str, object]:
    """The compiled semantic document (the law's §13 — the platform
    boundary's INPUT vocabulary): every ACTIVE control's value keyed
    by the PROFILE FIELD (the platform's own flag table maps field →
    flag syntax — app §2's seam law: this side owns the MEANING, the
    platform owns the FLAG). The chain compiles to the ordered
    enabled `--samplers` member list; LEGACY/REMOVED controls are
    never emitted (the vocabulary is representable, the emission
    refuses). The FLAG SYNTAX itself stays the platform's single
    owner — never restated here."""
    values: dict[str, object] = {}
    for control in CONTROL_LIBRARY:
        if control.status in ("LEGACY", "REMOVED"):
            continue  # representable, never emitted for this runtime
        values[control.field] = profile.values.get(
            control.field, control.baseline
        )
    values["samplers"] = [
        item.id for item in profile.sampler_chain if item.enabled
    ]
    return values
