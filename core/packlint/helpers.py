"""The packlint foundation: the error class, the shape tools, and the
regex vocabularies every domain lint shares (the D-175 split's rider —
`core/pack.py` owns the admission contract, `core/packlint/` the
implementation)."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any, Final

from core.predicates import COMPARATORS, COMPOUND_KEYS, LEAF_KINDS
from core.worldgen import WORLDGEN_BLOCK


class PackError(RuntimeError):
    """Load-time lint failure — the pack never reaches the simulation."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PackError(message)


def _ids(records: list[Mapping[str, Any]]) -> set[str]:
    return {record["id"] for record in records}


def _is_int(value: Any) -> bool:
    """A JSON integer (bool excluded — a flag is never a count)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: Any) -> bool:
    """A JSON number (int or float, bool excluded)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


_SNAKE_CASE: Final = re.compile(r"^[a-z][a-z0-9_]*$")
_SLOT: Final = re.compile(r"\{([a-z_]+)\}")
_EXCEPT_TOKENS: Final = ("actor", "target", "cause_actor")
_NOUNS: Final = ("actor", "target", "texture")

#: The template-binding forms the reachability lint scans for (depth-5b,
#: D-116 (2)): `{slot}` (the value substitution) and `{slot?…` (the
#: conditional key — the missing-key else arm is the designed branch for
#: outcome shapes that lack the slot). The `#ref#` grammar form is the
#: symbols' surface, not the event-data binding surface.
_BRACE_SLOT: Final = re.compile(r"\{([a-z][a-z0-9_]*)\}")
_BRACE_COND: Final = re.compile(r"\{([a-z][a-z0-9_]*)\?")

def _bound_template_slots(templates: Mapping[str, Any]) -> frozenset[str]:
    """Every slot name the pack's template lines bind (depth-5b): the
    `{slot}` / `{slot?…}` references across the events' lines, the
    symbols' alternatives, and the day_header / scene_card / fallback
    strings. The reachability law's template consumer — a claim whose
    slot never appears here can never render (L1: dead data)."""
    slots: set[str] = set()

    def scan(value: Any) -> None:
        if isinstance(value, str):
            slots.update(_BRACE_SLOT.findall(value))
            slots.update(_BRACE_COND.findall(value))
        elif isinstance(value, list):
            for item in value:
                scan(item)

    events = templates.get("events")
    if isinstance(events, Mapping):
        scan(list(events.values()))
    symbols = templates.get("symbols")
    if isinstance(symbols, Mapping):
        scan(list(symbols.values()))
    for key in ("day_header", "scene_card", "fallback"):
        scan(templates.get(key))
    return frozenset(slots)


def _armed_claim_slots(rules: Mapping[str, Any]) -> frozenset[str]:
    """The armed claims' slots (bridge-1, D-116 (1)): the scene-line
    legal set's worldgen half — a scene field may name an armed claim's
    slot (the claims' first brief-side consumer: the pipe reads the slot
    from the folded projection). A DEFENSIVE walk — the worldgen block's
    own shape lint runs LAST (the order law, the KI#77 family), so only
    well-formed entries contribute here; a malformed block contributes
    nothing and still gets its own clean refusal in `_worldgen`."""
    config = rules.get(WORLDGEN_BLOCK)
    if not isinstance(config, Mapping):
        return frozenset()
    claims = config.get("claims")
    if not isinstance(claims, list):
        return frozenset()
    return frozenset(
        entry["slot"]
        for entry in claims
        if isinstance(entry, Mapping)
        and isinstance(entry.get("slot"), str)
    )

def _director_prop_reads(rules: Mapping[str, Any]) -> frozenset[tuple[str, str]]:
    """Every `(entity, path)` pair a declared director hook reads
    through a `prop` predicate leaf (depth-5b, the reachability law's
    hook consumer): the hooks' triggers, their weight modifiers' `when`
    clauses, and their options' trigger lists. The leaves are walked
    wherever they sit in the compound tree — the shapes are linted
    elsewhere; this scan only collects."""
    reads: set[tuple[str, str]] = set()

    def walk(spec: Any) -> None:
        if isinstance(spec, list):
            for item in spec:
                walk(item)
            return
        if not isinstance(spec, Mapping):
            return
        if spec.get("kind") == "prop":
            reads.add((str(spec.get("of")), str(spec.get("path"))))
        for key in COMPOUND_KEYS:
            if key in spec:
                walk(spec[key])

    hooks = rules.get("director", {})
    if not isinstance(hooks, Mapping):
        return frozenset(reads)
    for spec in hooks.get("hooks", {}).values():
        if not isinstance(spec, Mapping):
            continue
        walk(spec.get("trigger"))
        weight = spec.get("weight")
        if isinstance(weight, Mapping):
            modifiers = weight.get("modifiers")
            if isinstance(modifiers, list):
                for modifier in modifiers:
                    if isinstance(modifier, Mapping):
                        walk(modifier.get("when"))
        options = spec.get("options")
        if isinstance(options, list):
            for option in options:
                if isinstance(option, Mapping):
                    walk(option.get("trigger"))
    return frozenset(reads)

def _lint_weight_spec(
    weight_spec: Any,
    where: str,
    npc_ids: set[str],
    location_ids: set[str],
    relation_axes: set[str],
    entity_ids: set[str],
) -> None:
    """The shared weight lint (drama-1's hook-weight block, extracted
    for drama-2's option weights): a flat non-negative int (the v0.1
    form) or the weight_multiplier object {base, modifiers} — base
    int >= 0, each modifier EXACTLY one of add (int >= 0) | factor
    (number >= 0) plus a `when` predicate (the evaluator applies them
    in declaration order; a factor of 0 legally zeroes). The message
    prefix is `{where}: weight...` so both call sites read cleanly."""
    if isinstance(weight_spec, Mapping):
        _require(
            _is_int(weight_spec.get("base")) and weight_spec["base"] >= 0,
            f"{where}: weight.base must be a non-negative integer",
        )
        modifiers = weight_spec.get("modifiers", ())
        _require(
            isinstance(modifiers, list),
            f"{where}: weight.modifiers must be a list",
        )
        for index, modifier in enumerate(modifiers):
            mwhere = f"{where}.weight.modifiers[{index}]"
            _require(
                isinstance(modifier, Mapping),
                f"{mwhere}: must be an object",
            )
            has_add = "add" in modifier
            has_factor = "factor" in modifier
            _require(
                has_add != has_factor,
                f"{mwhere}: exactly one of add|factor is required "
                "(the donor's shape — never both)",
            )
            if has_add:
                _require(
                    _is_int(modifier["add"]) and modifier["add"] >= 0,
                    f"{mwhere}: add must be a non-negative integer",
                )
            else:
                _require(
                    _is_number(modifier["factor"])
                    and modifier["factor"] >= 0,
                    f"{mwhere}: factor must be a non-negative number",
                )
            when = modifier.get("when")
            error = _predicate_error(
                when, f"{mwhere}.when", npc_ids, location_ids,
                relation_axes, entity_ids,
            )
            _require(
                error is None,
                error or "unreachable",
            )
    else:
        _require(
            _is_int(weight_spec) and weight_spec >= 0,
            f"{where}: weight must be a non-negative integer or a "
            "weight_multiplier object",
        )



def _predicate_error(
    spec: Any,
    where: str,
    npc_ids: set[str],
    location_ids: set[str],
    relation_axes: set[str],
    entity_ids: set[str],
) -> str | None:
    """Validate one drama-1 predicate spec (core/predicates.py owns the
    grammar; this is the load-time shape gate — the evaluator's loud
    ValueError is the runtime backstop, never the first line of defense).
    Returns the error message or None when the spec is valid. Recursive;
    `where` carries the pack path for the message (e.g.
    `director.hooks['x'].trigger.all[0]`)."""
    if isinstance(spec, list):
        if not spec:  # L1: an empty AND is dead vocabulary
            return f"{where}: an empty predicate list is dead vocabulary"
        for index, item in enumerate(spec):
            error = _predicate_error(
                item, f"{where}[{index}]", npc_ids, location_ids,
                relation_axes, entity_ids,
            )
            if error:
                return error
        return None
    if not isinstance(spec, Mapping) or not spec:
        return f"{where}: predicate must be a non-empty object or a list"
    compounds = [key for key in COMPOUND_KEYS if key in spec]
    if compounds:
        if len(spec) != 1:
            return (
                f"{where}: a compound carries extra keys {sorted(spec)} "
                f"beside {compounds[0]!r}"
            )
        inner = spec[compounds[0]]
        # pack-ci (iter-117, PACK_SPEC §6 AP-15): rule atomicity — a
        # compound's members must be LEAVES. Nested compounds are the
        # conditional chains ("if X and if Y before that, then Z") the
        # crosswalk refuses; split them into separate rules instead.
        # The evaluator (core/predicates.py) keeps its recursive grammar
        # — this is the authoring discipline gate, never a runtime law.
        if compounds[0] == "not":
            if isinstance(inner, Mapping) and any(
                key in inner for key in COMPOUND_KEYS
            ):
                return (
                    f"{where}.not: nested compound — one condition per "
                    f"rule, compound conditions split (AP-15)"
                )
            return _predicate_error(
                inner, f"{where}.not", npc_ids, location_ids,
                relation_axes, entity_ids,
            )
        if not isinstance(inner, list) or not inner:  # L1: dead vocabulary
            return f"{where}.{compounds[0]}: must be a non-empty list"
        for index, item in enumerate(inner):
            if isinstance(item, Mapping) and any(
                key in item for key in COMPOUND_KEYS
            ):
                return (
                    f"{where}.{compounds[0]}[{index}]: nested compound — "
                    f"one condition per rule, compound conditions split "
                    f"(AP-15)"
                )
            error = _predicate_error(
                item, f"{where}.{compounds[0]}[{index}]", npc_ids,
                location_ids, relation_axes, entity_ids,
            )
            if error:
                return error
        return None
    kind = spec.get("kind")
    if kind not in LEAF_KINDS:
        return f"{where}: kind must be one of {list(LEAF_KINDS)}, got {kind!r}"
    if kind == "time":
        if not _is_int(spec.get("tick")) or spec["tick"] < 0:
            return f"{where}: time predicate needs a non-negative integer tick"
    elif kind == "place":
        if spec.get("target_npc") not in npc_ids:
            return f"{where}: place predicate target_npc must name an npc"
        if spec.get("location") not in location_ids:
            return f"{where}: place predicate location must name a location"
    elif kind == "threshold":
        if spec.get("target_npc") not in npc_ids:
            return f"{where}: threshold predicate target_npc must name an npc"
        if spec.get("axis") not in relation_axes:
            return f"{where}: threshold predicate axis must be a relations axis"
        if spec.get("comparator") not in ("at_least", "at_most"):
            return f"{where}: threshold comparator must be at_least|at_most"
        if not _is_int(spec.get("value")):
            return f"{where}: threshold value must be an integer"
    else:  # prop — the generalized projection read (drama-1)
        if spec.get("of") not in entity_ids:
            return f"{where}: prop predicate 'of' must name an entity"
        if not isinstance(spec.get("path"), str) or not spec["path"]:
            return f"{where}: prop predicate 'path' must be a non-empty string"
        if spec.get("comparator") not in COMPARATORS:
            return (
                f"{where}: prop comparator must be one of {list(COMPARATORS)}"
            )
        if spec.get("comparator") in ("at_least", "at_most") and not _is_int(
            spec.get("value")
        ):
            return f"{where}: prop {spec['comparator']} needs an integer value"
        if "value" not in spec:
            return f"{where}: prop predicate needs a value"
        if spec.get("value") is None:
            return (
                f"{where}: prop predicate 'value' must not be null — "
                "absence is the world's answer (False, DIRECTOR_SPEC §3), "
                "never a pack value"
            )
    return None
