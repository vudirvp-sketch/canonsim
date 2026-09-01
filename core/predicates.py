"""The JSON predicate grammar (drama-1, phase 3; phases.md §3 — the
Paradox trigger block adapted per L10: JSON structures over the
projection, no string expression languages in packs). The single owner
of the truth-valued half of the event grammar; `docs/DIRECTOR_SPEC.md`
§3 owns the contract, the donor mechanics live in
`docs/ref/paradox_scripting.md`.

What the donor gave, minus its footguns (phases.md §3): the implicit-AND
trigger root, AND/OR/NOT logic blocks, value comparisons — as JSON
pack data evaluated by a generic interpreter. The Paradox implicit-`this`
scope is replaced by an explicit `of`/`path` read against the folded
projection (D-023); "MTTH is anti-deterministic by construction" is
rejected by construction here — the evaluator is a PURE function of
(spec, projection, beat_tick): no RNG, no wall-clock, no iteration
order dependence (INV-2; TIME-1 — a predicate never schedules, it only
answers).

Leaf kinds (each a Mapping carrying `"kind"`):

- `time` — `{"kind": "time", "tick": N}`: `beat_tick >= tick`
- `place` — `{"kind": "place", "target_npc": S, "location": S}`:
  the target's projection position equals `location`
- `threshold` — `{"kind": "threshold", "target_npc": S, "axis": S,
  "comparator": "at_least"|"at_most", "value": N}`: the target's
  `relations.<axis>` meets the comparison (the v0.1 leaf, unchanged)
- `prop` — `{"kind": "prop", "of": S, "path": S, "comparator":
  "at_least"|"at_most"|"equals"|"not_equals", "value": ...}`: the
  generalized projection read — any entity, any prop path

Compound nodes (one discriminator key per node, the Paradox shape):

- `{"all": [spec, ...]}` — AND (an empty list is vacuously true)
- `{"any": [spec, ...]}` — OR (an empty list is false)
- `{"not": spec}` — negation, a single inner spec (the donor's
  own recommendation against multi-inner NOT)

A root spec is a bare leaf Mapping, a compound Mapping, or a LIST of
specs (the implicit-AND root — the Paradox `trigger = { ... }` body).
Unknown kinds and malformed shapes raise ValueError loudly — pack lint
catches them at load time, the evaluator never guesses (L10: validated
content, not parsed content).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Final

__all__ = [
    "COMPARATORS",
    "COMPOUND_KEYS",
    "LEAF_KINDS",
    "evaluate",
]

LEAF_KINDS: Final = ("time", "place", "threshold", "prop")
"""The closed leaf vocabulary (drama-1). `time`/`place`/`threshold` are
the v0.1 trigger kinds (DIRECTOR_SPEC §3, byte-identical semantics);
`prop` is the generalized projection read."""

COMPOUND_KEYS: Final = ("all", "any", "not")
"""The closed compound vocabulary: AND / OR / single-inner NOT."""

COMPARATORS: Final = ("at_least", "at_most", "equals", "not_equals")
"""The closed comparison vocabulary. `threshold` carries the v0.1 pair
(at_least | at_least's mirror); `prop` carries all four."""


def evaluate(
    spec: Any,
    projection: Mapping[str, Mapping[str, Any]],
    beat_tick: int,
) -> bool:
    """Evaluate one predicate spec against the folded projection and the
    current beat tick. Pure (INV-2): same spec + same projection + same
    tick = same answer, in any process. Raises ValueError on an unknown
    kind or a malformed shape — never guesses (the pack lint owns
    load-time validation; this is the runtime backstop)."""
    if isinstance(spec, Sequence) and not isinstance(spec, (str, bytes)):
        return all(evaluate(item, projection, beat_tick) for item in spec)
    if not isinstance(spec, Mapping):
        raise ValueError(f"predicate spec must be an object or a list, got {spec!r}")
    if not spec:
        raise ValueError("predicate spec must not be empty")
    compounds = [key for key in COMPOUND_KEYS if key in spec]
    if compounds:
        if len(spec) != 1:
            raise ValueError(
                f"compound predicate carries extra keys {sorted(spec)!r} "
                f"beside {compounds[0]!r}"
            )
        return _compound(compounds[0], spec[compounds[0]], projection, beat_tick)
    kind = spec.get("kind")
    if kind == "time":
        return beat_tick >= _int(spec, "tick")
    if kind == "place":
        npc = _text(spec, "target_npc")
        return projection.get(npc, {}).get("position") == _text(spec, "location")
    if kind == "threshold":
        npc = _text(spec, "target_npc")
        prop = f"relations.{_text(spec, 'axis')}"
        value = projection.get(npc, {}).get(prop)
        if not isinstance(value, int) or isinstance(value, bool):
            return False
        if spec["comparator"] == "at_least":
            return value >= _int(spec, "value")
        if spec["comparator"] == "at_most":
            return value <= _int(spec, "value")
        raise ValueError(f"unknown threshold comparator {spec['comparator']!r}")
    if kind == "prop":
        return _prop(spec, projection)
    raise ValueError(f"unknown predicate kind {kind!r}")


def _compound(
    key: str,
    inner: Any,
    projection: Mapping[str, Mapping[str, Any]],
    beat_tick: int,
) -> bool:
    """The all/any/not family. `all: []` is vacuously true and `any: []`
    false (the standard empty-AND/empty-OR semantics); the pack lint
    rejects empty lists as dead vocabulary (L1) — the evaluator stays
    mathematically honest either way."""
    if key == "not":
        return not evaluate(inner, projection, beat_tick)
    if not isinstance(inner, Sequence) or isinstance(inner, (str, bytes)):
        raise ValueError(f"{key!r} must carry a list, got {inner!r}")
    if key == "all":
        return all(evaluate(item, projection, beat_tick) for item in inner)
    return any(evaluate(item, projection, beat_tick) for item in inner)


def _prop(
    spec: Mapping[str, Any],
    projection: Mapping[str, Mapping[str, Any]],
) -> bool:
    """The generalized projection read: any entity, any prop path. A
    missing prop answers False under the ordering comparators and under
    `equals`, True under `not_equals` (the value genuinely is not that);
    a bool-vs-number comparison is never equal (Python's `True == 1`
    footgun, guarded explicitly)."""
    entity = _text(spec, "of")
    actual = projection.get(entity, {}).get(_text(spec, "path"))
    expected = spec["value"]
    comparator = spec["comparator"]
    if comparator == "equals":
        return _same_kind(actual, expected) and actual == expected
    if comparator == "not_equals":
        return not (_same_kind(actual, expected) and actual == expected)
    if not isinstance(actual, int) or isinstance(actual, bool):
        return False
    if comparator == "at_least":
        return actual >= _int(spec, "value")
    if comparator == "at_most":
        return actual <= _int(spec, "value")
    raise ValueError(f"unknown prop comparator {comparator!r}")


def _same_kind(left: Any, right: Any) -> bool:
    """True when the two values are comparable without the bool/int
    conflation (True == 1 in Python — a flag must not equal a count)."""
    return isinstance(left, bool) == isinstance(right, bool)


def _int(spec: Mapping[str, Any], key: str) -> int:
    value = spec.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"predicate field {key!r} must be an integer, got {value!r}")
    return value


def _text(spec: Mapping[str, Any], key: str) -> str:
    value = spec.get(key)
    if not isinstance(value, str):
        raise ValueError(f"predicate field {key!r} must be a string, got {value!r}")
    return value
