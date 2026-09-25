"""The semantic-control MODEL + the admitted control library (ssi-4
step 1, iter-247 — the inf-1/inf-2 core's DATA half, extracted
verbatim from the single-module era).

Law owner: `docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md` — §3 the control
model (the SemanticControl atom: identity is the SEMANTIC id, never
the raw flag; the field is the PROFILE vocabulary), §2 the three-layer
split (THIS module is the SEMANTIC CONTROL layer's identity/data
half). The RAW CAPABILITY surface is never hardcoded as law here:
every form/default is the reviewed snapshot's own evidence, the
installed binary the authority (the §19 protocol). The UI projection
(inference.gd) reads the resolved document, never this module.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

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
