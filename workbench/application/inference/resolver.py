"""The effective-state resolver (ssi-4 step 2, iter-248 — extracted
verbatim from the single-module era).

The law's §6 pipeline's deterministic minimal form (LLAMA_CPP_
INFERENCE_CONTROL_LAW the owner): compose the BASE profile with the
call-local REQUEST layer, evaluate the RELATIONS (evidence-pinned
only), and return the per-control document — every resolved control
carries exactly one state from the closed STATES vocabulary plus a
REASON whenever it is not EFFECTIVE (§7: configured-but-ineffective
controls stay VISIBLE, never a hidden drop). Pure function of the
profile — no I/O, no store, no gateway.
"""

from __future__ import annotations

from collections.abc import Mapping

from workbench.application.inference.chain import ChainItem
from workbench.application.inference.library import (
    _CONTROL_INDEX,
    CATEGORIES,
    CHAIN_FAMILIES,
    CONTROL_LIBRARY,
    SemanticControl,
)
from workbench.application.inference.presets import PRESETS
from workbench.application.inference.profile import InferenceProfile
from workbench.application.inference.relations import RELATIONS, EffectiveNoop

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
