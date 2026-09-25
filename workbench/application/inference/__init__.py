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
package is its landed form — the full library over the reviewed
runtime surface.

The three layers (the law's §2, kept strictly separate; the ssi-4
package layout follows them):

```text
RAW CAPABILITY      the runtime's own surface (existence/syntax/
                    values/defaults) — the reviewed --help snapshot
                    is the EVIDENCE; the actual installed binary is
                    the AUTHORITY (never this module)
SEMANTIC CONTROL    THIS package — identity, human name, category,
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

The package layout (ssi-4/Phase 3, iter-247 — the split by the LAW's
own semantic owners, the strangler method the packlint decomposition
proved; the public import surface `workbench.application.inference`
UNCHANGED, every consumer and test importing exactly as before):
`library` (the control model + the 85-control data + the indexes),
`chain` (the membership/order semantics), `presets`, `relations` —
the semantic-control DATA half (iter-247); `profile` (the document
+ its acceptance laws) and `resolver` (the effective-state
resolver) — the RESOLUTION half (iter-248); `store` (the profile
owner + the schema tag), `migration` (the one-way settings
migration), `operations` (the gateway family + the chat BASE
provider), `compiled` (the platform seam's input vocabulary) — the
PERSISTENCE/OPERATIONS half (iter-249). THIS file is the pure
re-export shell: the byte-stable public import surface
`workbench.application.inference` — every consumer and test
importing exactly as before, each half at its semantic owner.
"""

from workbench.application.inference.chain import DEFAULT_CHAIN, ChainItem
from workbench.application.inference.compiled import compile_semantic
from workbench.application.inference.library import (
    CATEGORIES,
    CHAIN_FAMILIES,
    CHAT_TEMPLATE_FORMS,
    CONTROL_LIBRARY,
    FIT_FORMS,
    FLASH_ATTENTION_FORMS,
    GPU_LAYER_FORMS,
    KV_CACHE_TYPES,
    LOAD_MODE_FORMS,
    NUMA_FORMS,
    REASONING_EFFORT_FORMS,
    REASONING_FORMAT_FORMS,
    REASONING_FORMS,
    ROPE_SCALING_FORMS,
    SAMPLER_CHAIN_IDS,
    SPEC_TYPE_FORMS,
    SPLIT_MODE_FORMS,
    InferenceError,
    SemanticControl,
)
from workbench.application.inference.migration import migrate_launch_semantics
from workbench.application.inference.operations import (
    effective_temperature,
    register_inference_operations,
)
from workbench.application.inference.presets import PRESETS, InferencePreset
from workbench.application.inference.profile import InferenceProfile
from workbench.application.inference.relations import (
    RELATIONS,
    Condition,
    EffectiveNoop,
    Requires,
)
from workbench.application.inference.resolver import STATES, resolve
from workbench.application.inference.store import SCHEMA, InferenceStore

__all__ = [
    "SCHEMA",
    "CATEGORIES",
    "CHAIN_FAMILIES",
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
    "DEFAULT_CHAIN",
    "SPLIT_MODE_FORMS",
    "SPEC_TYPE_FORMS",
    "STATES",
    "RELATIONS",
    "InferenceError",
    "InferencePreset",
    "InferenceProfile",
    "InferenceStore",
    "CONTROL_LIBRARY",
    "PRESETS",
    "SemanticControl",
    "ChainItem",
    "Condition",
    "EffectiveNoop",
    "Requires",
    "compile_semantic",
    "effective_temperature",
    "migrate_launch_semantics",
    "register_inference_operations",
    "resolve",
]
