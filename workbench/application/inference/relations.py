"""The typed relation data (the law's §12 — ssi-4 step 1, extracted
verbatim): Condition/Requires/EffectiveNoop + the evidence-pinned
RELATIONS set. Semantic conditions over PROFILE VALUES, never bare
flag-name pairs; each relation sourced from the runtime evidence (the
--help's own words) or the chip specification's own law — never
invented. The evaluation lives in the resolver; this module is data.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

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
