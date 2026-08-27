"""Deterministic tracery engine (CHRON-1, `docs/blueprint/phase0.md` §5).

tracery's grammar — a JSON symbol table (symbol → alternatives, nested
`#symbol#` expansion, dot-notation hierarchies, modifiers, save/restore)
— with ink's `shuffle` semantics (pick without immediate repeat) on a
~200-line stdlib engine. Every pick comes from the **cosmetic stream**
(RNG-1) or `sorted()` order, never wall-clock, never `PYTHONHASHSEED`:
the same grammar + the same seed + the same call order = the same bytes
(T1 covers the chronicle too).

Syntax (two reference families over one context):

- `#path.mod1.mod2#` — a reference. Resolution order: a value saved in
  the current expansion scope (`[key:value]`), then a context slot
  (event data, filled by the chronicle renderer), then a grammar symbol
  (a `ShufflePool` pick). `path` may be dotted (dot-notation hierarchy);
  the LONGEST prefix that names a known symbol wins, the rest must be
  modifiers. Modifiers: `.a` (a/an article), `.capitalize`, `.upper`,
  `.lower`.
- `[key:value]` — save/restore: expands `value` NOW and binds it to
  `key` for the REST of the current expansion scope (pronoun/article
  agreement — the tracery memory stack, scoped).
- `{slot}` — verbatim context substitution (no modifiers, no
  re-expansion of the inserted value).
- `{cond?a|b}` — ink-style conditional text: the branch chosen by the
  RAW truthiness of the context value (bools stay bools, `""` is
  false); the chosen branch is expanded recursively.

The grammar is immutable and linted at construction (unknown symbols,
unknown modifiers, malformed references fail loudly — a pack author's
bug crashes at load, not mid-story). Expansion state (the per-symbol
`ShufflePool` last-pick memory) lives on the `Engine`, so one `Engine`
= one render pass: the render is a pure function of (grammar, seed,
call order) and never touches canon (INV-1: the renderer writes
nothing to the log; INV-2: cosmetic stream only).
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any, Callable, Final

from core.rng import COSMETIC, RngBank

__all__ = [
    "Engine",
    "Grammar",
    "GrammarError",
    "ShufflePool",
]

# -- modifiers (the single registry — tracery's "modifier list is the
# single point of extension", adapted: code owns the functions, packs own
# the words) ---------------------------------------------------------------


def _article(word: str) -> str:
    """`a`/`an` by vowel onset (the tracery `.a` modifier)."""
    return f"an {word}" if word[:1].lower() in "aeiou" else f"a {word}"


MODIFIERS: Final[dict[str, Callable[[str], str]]] = {
    "a": _article,
    "capitalize": str.capitalize,
    "upper": str.upper,
    "lower": str.lower,
}

_MAX_DEPTH: Final = 32  # cycle guard: grammar cycles fail loudly, not by stack
_NAME: Final = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$")
_SIMPLE_NAME: Final = re.compile(r"^[a-z][a-z0-9_]*$")
_IMPORTANCE_ORDER: Final = ("low", "medium", "high")


class GrammarError(RuntimeError):
    """Grammar lint failure or expansion error — a pack-author bug."""


def flatten_symbols(data: Any, prefix: str = "") -> dict[str, tuple[str, ...]]:
    """Flatten nested JSON into dotted symbol → alternatives.

    A list value is the alternatives; a plain string is a single
    alternative; a dict recurses with a dotted key prefix. A dotted key
    colliding with an existing symbol is a lint failure (ambiguity).
    """
    symbols: dict[str, tuple[str, ...]] = {}
    if isinstance(data, Mapping):
        for key, value in data.items():
            if not isinstance(key, str) or not _NAME.match(key):
                raise GrammarError(f"symbol name {key!r} is not dotted snake_case")
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, Mapping):
                for nested, alternatives in flatten_symbols(value, path).items():
                    if nested in symbols:
                        raise GrammarError(f"duplicate symbol {nested!r}")
                    symbols[nested] = alternatives
            else:
                alternatives = _as_alternatives(value, path)
                if path in symbols:
                    raise GrammarError(f"duplicate symbol {path!r}")
                symbols[path] = alternatives
    return symbols


def _as_alternatives(value: Any, path: str) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        alternatives = tuple(value)
        if not alternatives or not all(isinstance(a, str) for a in alternatives):
            raise GrammarError(
                f"symbol {path!r}: alternatives must be a non-empty list of strings"
            )
        return alternatives
    raise GrammarError(
        f"symbol {path!r}: expected a string, a list of strings, or a nested "
        f"object, got {type(value).__name__}"
    )


class Grammar:
    """The immutable, linted symbol table built from `templates.json`."""

    def __init__(self, templates: Mapping[str, Any]) -> None:
        data = dict(templates)
        symbols = flatten_symbols(data.get("symbols", {}))
        # the chronicle's own lines are pooled symbols too: a plain string
        # is a single alternative, a list gives ink-shuffle variety
        for name in ("day_header", "scene_card", "fallback"):
            if name not in data:
                raise GrammarError(f"templates: missing {name!r}")
            symbols[name] = _as_alternatives(data[name], name)
        for event_type, value in data.get("events", {}).items():
            symbols[f"event.{event_type}"] = _as_alternatives(value, f"event.{event_type}")
        self._symbols = symbols
        self._tale_gate = _tale_gate(data)
        self._lint()

    @property
    def tale_gate(self) -> str:
        """The minimum importance that earns a chronicle line (pack data)."""
        return self._tale_gate

    def alternatives(self, symbol: str) -> tuple[str, ...]:
        """The alternatives of a symbol (empty when undeclared)."""
        return self._symbols.get(symbol, ())

    def __contains__(self, symbol: str) -> bool:
        return symbol in self._symbols

    def _lint(self) -> None:
        for _symbol, alternatives in sorted(self._symbols.items()):
            for alternative in alternatives:
                for ref in _references(alternative):
                    self.decompose(ref)  # unknown symbol/modifier fails loudly

    def decompose(self, ref: str) -> tuple[str, tuple[str, ...], str | None]:
        """Split `a.b.c` into (symbol, modifiers, context-key fallback).

        The LONGEST prefix that names a known symbol wins; the remainder
        must be known modifiers. When no prefix is a grammar symbol, the
        first part is a context-slot lookup (event data — `#actor#`,
        `#phase.capitalize#`) and the REST are still modifiers.
        """
        parts = ref.split(".")
        for size in range(len(parts), 1, -1):
            candidate = ".".join(parts[:size])
            if candidate in self._symbols:
                return candidate, _check_modifiers(parts[size:], ref), None
        # no dotted prefix is a grammar symbol: a context slot + modifiers
        return parts[0], _check_modifiers(parts[1:], ref), parts[0]


def _check_modifiers(parts: list[str], ref: str) -> tuple[str, ...]:
    for part in parts:
        if part not in MODIFIERS:
            raise GrammarError(
                f"reference #{ref}#: unknown modifier {part!r} "
                f"(known: {sorted(MODIFIERS)})"
            )
    return tuple(parts)


def _references(text: str) -> list[str]:
    """Every `#...#` reference in a template string."""
    refs: list[str] = []
    index = 0
    while True:
        start = text.find("#", index)
        if start < 0:
            return refs
        end = text.find("#", start + 1)
        if end < 0:
            raise GrammarError(f"unterminated # in template: {text!r}")
        refs.append(text[start + 1 : end])
        index = end + 1


def _tale_gate(data: Mapping[str, Any]) -> str:
    gate = data.get("tale_gate", {}).get("min_importance", "low")
    if gate not in _IMPORTANCE_ORDER:
        raise GrammarError(
            f"tale_gate.min_importance must be one of {list(_IMPORTANCE_ORDER)}, "
            f"got {gate!r}"
        )
    return gate


class ShufflePool:
    """ink's `shuffle` (random pick without immediate repeat), made
    deterministic: candidates = `sorted(alternatives)` minus the last
    pick; more than one candidate → a seeded draw from the cosmetic
    stream; exactly one → taken as-is; zero (a single-alternative symbol)
    → the last pick repeats. `last_pick` advances after every pick."""

    def __init__(self, alternatives: Sequence[str], bank: RngBank) -> None:
        self._alternatives = tuple(alternatives)
        self._bank = bank
        self.last_pick: str | None = None

    def pick(self) -> str:
        candidates = [a for a in sorted(self._alternatives) if a != self.last_pick]
        if not candidates:
            chosen = self.last_pick  # single alternative: it must repeat
            assert chosen is not None
        elif len(candidates) == 1:
            chosen = candidates[0]
        else:
            chosen = candidates[self._bank.randint(0, len(candidates) - 1)]
        self.last_pick = chosen
        return chosen


class Engine:
    """One render pass: the grammar plus the per-symbol pool state.

    A fresh `Engine` per pass keeps the render a pure function of the
    log: pools never survive across passes (a second render of the same
    log starts from the same last_pick=None and the same fresh bank)."""

    def __init__(self, grammar: Grammar, bank: RngBank) -> None:
        self._grammar = grammar
        self._bank = bank
        self._pools: dict[str, ShufflePool] = {}

    def expand_symbol(self, symbol: str, context: Mapping[str, Any]) -> str:
        """Pick a symbol's alternative (pool applies) and expand it."""
        with self._bank.assure(COSMETIC):  # RNG-1: render paths draw cosmetic
            return self._expand_symbol(symbol, context, 0)

    def expand_text(self, text: str, context: Mapping[str, Any]) -> str:
        """Expand a raw template string (not from the symbol table)."""
        with self._bank.assure(COSMETIC):
            return self._expand(text, dict(context), 0)

    # -- internals -----------------------------------------------------------

    def _expand_symbol(self, symbol: str, context: Mapping[str, Any], depth: int) -> str:
        alternatives = self._grammar.alternatives(symbol)
        if not alternatives:
            raise GrammarError(f"unknown symbol {symbol!r}")
        pool = self._pools.get(symbol)
        if pool is None:
            pool = ShufflePool(alternatives, self._bank)
            self._pools[symbol] = pool
        return self._expand(pool.pick(), dict(context), depth + 1)

    def _expand(self, text: str, context: dict[str, Any], depth: int) -> str:
        if depth > _MAX_DEPTH:
            raise GrammarError(
                f"expansion exceeded {_MAX_DEPTH} levels — a symbol cycle?"
            )
        out: list[str] = []
        index = 0
        length = len(text)
        while index < length:
            char = text[index]
            if char == "#":
                end = text.find("#", index + 1)
                if end < 0:
                    raise GrammarError(f"unterminated # in {text!r}")
                out.append(self._expand_ref(text[index + 1 : end], context, depth))
                index = end + 1
            elif char == "[":
                end = text.find("]", index + 1)
                if end < 0:
                    raise GrammarError(f"unterminated [ in {text!r}")
                key, sep, value = text[index + 1 : end].partition(":")
                if not sep:
                    raise GrammarError(f"save needs '[key:value]', got {text!r}")
                key = key.strip()
                if not _SIMPLE_NAME.match(key):
                    raise GrammarError(f"save key {key!r} is not snake_case")
                # the save binds for the REST of this expansion scope only
                context = {**context, key: self._expand(value, context, depth + 1)}
                index = end + 1
            elif char == "{":
                end = _matching_brace(text, index)
                inner = text[index + 1 : end]
                out.append(self._expand_brace(inner, context, depth))
                index = end + 1
            else:
                out.append(char)
                index += 1
        return "".join(out)

    def _expand_brace(self, inner: str, context: Mapping[str, Any], depth: int) -> str:
        """`{slot}` verbatim substitution or `{cond?a|b}` conditional."""
        if "?" in inner:
            cond, sep, branches = inner.partition("?")
            if not sep:
                raise GrammarError(f"malformed conditional {inner!r}")
            true_branch, has_else, false_branch = branches.partition("|")
            value = context.get(cond.strip())
            chosen = true_branch if value else (
                false_branch if has_else else ""
            )
            return self._expand(chosen, dict(context), depth + 1)
        slot = inner.strip()
        if not _SIMPLE_NAME.match(slot):
            raise GrammarError(f"slot name {slot!r} is not snake_case")
        if slot not in context:
            raise GrammarError(f"unknown slot {{{slot}}} (context: {sorted(context)})")
        value = context[slot]
        return value if isinstance(value, str) else str(value)

    def _expand_ref(self, ref: str, context: Mapping[str, Any], depth: int) -> str:
        symbol, modifiers, context_key = self._grammar.decompose(ref)
        if context_key is not None and context_key in context:
            value = context[context_key]
            text = value if isinstance(value, str) else str(value)
        elif symbol in self._grammar:
            text = self._expand_symbol(symbol, context, depth)
        elif context_key is not None:
            raise GrammarError(
                f"reference #{ref}#: neither a symbol nor a context slot"
            )
        else:  # pragma: no cover — _decompose guarantees a context_key here
            raise GrammarError(f"reference #{ref}#: unresolvable")
        for modifier in modifiers:
            text = MODIFIERS[modifier](text)
        return text


def _matching_brace(text: str, start: int) -> int:
    """Index of the `}` matching the `{` at `start` (braces nest)."""
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    raise GrammarError(f"unterminated {{ in {text!r}")
