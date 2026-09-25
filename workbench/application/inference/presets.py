"""The four §30 presets (the law's §14 — ssi-4 step 1, extracted
verbatim): named configuration STARTING POINTS, applied as
TRANSPARENT diff-previewed documents — never opaque modes, the chips
stay editable after the apply. The values are the spec's own numbers
where it pins them; where it pins only structure, the value is
CanonSim's documented starting point — never an invented upstream
truth.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

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
