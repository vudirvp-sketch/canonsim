"""The compiled semantic document (ssi-4 step 3, iter-249 — extracted
verbatim; the law's §13 — the platform boundary's INPUT vocabulary).

Every ACTIVE control's value keyed by the PROFILE FIELD (the
platform's own flag table maps field → flag syntax — app §2's seam
law: this side owns the MEANING, the platform owns the FLAG); the
chain compiles to the ordered enabled `--samplers` member list;
LEGACY/REMOVED controls are never emitted. The FLAG SYNTAX itself
stays the platform's single owner (workbench/platform/
llama_process.py) — never restated here.
"""

from __future__ import annotations

from workbench.application.inference.library import CONTROL_LIBRARY
from workbench.application.inference.profile import InferenceProfile


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
