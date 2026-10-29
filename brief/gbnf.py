"""The GBNF serialization of the grammar snapshot (engine-1's landing,
iter-177, D-193; the snapshot's own law `docs/PARSER_SPEC.md` §2, the
serialization's laws its §2.1; CONTRACTS §4.1 D6/I3: ONE INV-3-clean pure
function over the snapshot — engine-generic data in, grammar text out).

The runtime engine (a llama-server behind the explicit adapter,
`cli/engine.py`) constrains its parse replies with this grammar: the
closed target grammar of `brief/parser.py::grammar_snapshot`, encoded as
GBNF so the door's own shape laws hold at the SOURCE (the v2 handoff's
measured lessons, TECH_NOTES §13.1: the v1 grammar's un-encoded shape
laws let the one-path crash form through at the owner's station). The
grammar is NARROWER than the reply gate, never wider — grammar-valid
output is gate-valid by construction; the honest guess-within-grammar
class (wrong kind, wrong canon target, wrong field value) stays
untouched (D-192's D5: the grammar fixes validity, never honesty — the
world answers those at the door).

The encoded door laws (`core/intent.py::validate_shape` +
`action_duration`, one owner per law — this module re-derives nothing
the snapshot does not carry):

- one reply alternative: `{"intent": ...}` | `{"question": ...}` |
  `{"no_intent": ...}` — exactly the gate's closed set, non-empty
  strings for the free-text alternatives (the f1b degenerate empty
  no_intent is structurally impossible here);
- `kind` enumerates the snapshot's verbs;
- the target enum is CANON NOUNS ONLY (texture entries are word-matching
  nouns, never targets) and is required exactly where the door demands
  one (`target_required`);
- the ONE-PATH law (texture XOR target, INTENT_SCHEMA §3): a
  texture-capable verb renders as SEPARATE path alternatives — the canon
  path (a canon target, the non-texture fields) and the texture path
  (`"target": null`, the live entry's verbatim `{entry, scope, slot,
  value}`) — the s2c1 one-path combo cannot be emitted;
- the drawn-`N` `ticks` field is REQUIRED (the door's accept-time law,
  mirrored on the snapshot's `FieldConstraint.required`);
- enum fields enumerate their closed values; an EMPTY enum (`<none
  available>`) never offers the field; open string fields ride the JSON
  string rule; positive integers ride `[1-9][0-9]*` (no leading zeros —
  invalid JSON anyway).

The dialect laws (measured at llama.cpp b11064, TECH_NOTES §13.1 — the
station compile check rides the owner's first live run; the repo pins
the laws structurally): rule names carry NO underscores (dashes fine —
identifiers are sanitized); `[...]` is a char class, the optional group
is `( ... )?`; `\"` escapes inside literals (json.gbnf's own form); the
string/number rules adopt json.gbnf's proven shapes (starred groups and
explicit repetition instead of `+`).

Pure: no RNG, no wall-clock, no I/O (INV-1/2/4; same snapshot → same
grammar bytes — the request identity's constraint half, D-192's D3).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence

from brief.parser import FieldConstraint, GrammarSnapshot, Noun, Verb

__all__ = ["gbnf_grammar", "grammar_fingerprint"]

_DQ = '"'  # the JSON quote character


def gbnf_grammar(snapshot: GrammarSnapshot) -> str:
    """The snapshot as GBNF text (pure, deterministic): the closed reply
    grammar the runtime engine's parse calls are constrained by. Same
    snapshot → same bytes, in any process, any `PYTHONHASHSEED`."""
    canon = [noun.id for noun in snapshot.nouns if noun.texture is None]
    if not canon:
        # A pack with verbs but no addressable canon nouns cannot offer a
        # target anywhere: loud, never a silently-broken grammar.
        raise ValueError(
            "the grammar snapshot carries no canon nouns — the GBNF "
            "serialization needs at least one addressable entity"
        )
    texture = [noun for noun in snapshot.nouns if noun.texture is not None]
    lines: list[str] = [
        "root ::= intent-doc | question-doc | no-intent-doc",
        'intent-doc ::= "{\\"intent\\": {" verb-body "}}"',
        "verb-body ::= " + " | ".join(_verb_rule_name(v) for v in snapshot.verbs),
        'question-doc ::= "{\\"question\\": " string "}"',
        'no-intent-doc ::= "{\\"no_intent\\": " string "}"',
        'string ::= "\\"" string-char ( string-char )* "\\""',
        'string-char ::= [^"\\\\\\x7F\\x00-\\x1F] | "\\\\" '
        '( ["\\\\bfnrt] | "u" hex hex hex hex )',
        "hex ::= [0-9a-fA-F]",
        "positive-int ::= [1-9] [0-9]*",
        "canon-target ::= "
        + " | ".join(_literal(_DQ + noun + _DQ) for noun in canon),
    ]
    for verb in snapshot.verbs:
        lines.append(_verb_rule(verb, live_texture=bool(texture)))
    if texture:
        lines.append(
            "texture-ref ::= "
            + " | ".join(_texture_rule_name(n) for n in texture)
        )
        for noun in texture:
            lines.append(_texture_rule(noun))
    return "\n".join(lines) + "\n"


def grammar_fingerprint(grammar: str) -> str:
    """The grammar id of the D3 inference manifest: the sha256 of the
    grammar text, truncated to 16 hex chars (the station manifest's own
    form, TECH_NOTES §13.1's round-4 record). Stable for the same
    snapshot; any grammar change moves it."""
    return hashlib.sha256(grammar.encode("utf-8")).hexdigest()[:16]


# -- the verb rules (the door's shape laws, encoded) ---------------------------


def _verb_rule(verb: Verb, live_texture: bool) -> str:
    """One verb's body alternatives. The canon path is always present
    (the field subsets of the non-texture fields, required ones forced
    in); a texture-capable verb gains the texture path as a SEPARATE
    alternative — one path, never both (the one-path law at the source,
    the s2c1 lesson). The texture path exists only when live entries can
    satisfy it (the texture-ref rule is emitted only then)."""
    target = (
        "canon-target" if verb.target_required
        else f"( {_literal('null')} | canon-target )"
    )
    paths = [
        _merge_literals(
            _literal(f"{_DQ}kind{_DQ}: {_DQ}{verb.intent}{_DQ}, "
                     f"{_DQ}target{_DQ}: ")
            + target
            + _literal(f", {_DQ}fields{_DQ}: ")
            + _fields_alternatives(verb.fields, texture=False)
        )
    ]
    if any(f.texture for f in verb.fields) and live_texture:
        paths.append(
            _merge_literals(
                _literal(f"{_DQ}kind{_DQ}: {_DQ}{verb.intent}{_DQ}, "
                         f"{_DQ}target{_DQ}: null, {_DQ}fields{_DQ}: ")
                + _fields_alternatives(verb.fields, texture=True)
            )
        )
    return f"{_verb_rule_name(verb)} ::= " + " | ".join(paths)


def _fields_alternatives(
    fields: Sequence[FieldConstraint], *, texture: bool
) -> str:
    """The `fields` object's alternatives as GBNF token sequences: every
    legal subset of the usable optional non-texture fields (required
    ones forced in, empty-enum fields never offered), each object
    rendered in DECLARATION order — the texture pair rides its declared
    position on the texture path and never appears on the canon path."""
    if any(f.required and f.values is not None and not f.values for f in fields):
        raise ValueError(
            "a required field with an empty value enum cannot be encoded — "
            "a pack-authoring contradiction (the door would refuse every reply)"
        )
    usable = [
        f for f in fields
        if not f.texture and not (f.values is not None and not f.values)
    ]
    optional = [f for f in usable if not f.required]
    alternatives = []
    for mask in range(1 << len(optional)):
        chosen = {
            optional[i].name for i in range(len(optional)) if mask >> i & 1
        }
        combo = {
            f.name for f in usable if f.required or f.name in chosen
        }
        alternatives.append(_fields_object(fields, combo, texture=texture))
    if len(alternatives) == 1:
        return alternatives[0]
    return "( " + " | ".join(alternatives) + " )"


def _fields_object(
    all_fields: Sequence[FieldConstraint],
    combo: set[str],
    *,
    texture: bool,
) -> str:
    """One fields-object alternative as a GBNF token sequence: `"name":
    value` pairs in declaration order (a merged literal when the value is
    a closed single value; a name literal + rule reference for enum /
    integer / string / texture values), with `{`/`}`/`, ` as literal
    fragments — a bare brace is a GBNF repetition operator and never
    appears unquoted (adjacent fragments merge in the rule assembly)."""
    pairs: list[str] = []
    for f in all_fields:
        if f.texture:
            if texture:
                pairs.append(_pair(f.name, ("ref", "texture-ref")))
            continue  # the canon path never carries the texture field
        if f.name in combo:
            pairs.append(_pair(f.name, _value_rule(f)))
    if not pairs:
        return _literal("{}")
    return _literal("{") + _literal(", ").join(pairs) + _literal("}")


def _pair(name: str, value: tuple[str, str]) -> str:
    """One `"name": value` pair as GBNF tokens: a merged literal when the
    value is a closed single value (kind "lit" — the raw JSON text,
    quotes and all), else the name literal followed by the rule
    reference or group (kind "ref")."""
    kind, text = value
    if kind == "lit":
        return _literal(f"{_DQ}{name}{_DQ}: {_DQ}{text}{_DQ}")
    return _literal(f"{_DQ}{name}{_DQ}: ") + text


def _value_rule(constraint: FieldConstraint) -> tuple[str, str]:
    """One field value's grammar as (kind, text): the closed single-value
    enum as a literal's raw JSON text, everything else — the enum group,
    the positive-integer form, the JSON string rule, the texture
    reference — as the rule-reference text that follows the name
    literal."""
    if constraint.positive_int:
        return "ref", "positive-int"
    if constraint.texture:
        return "ref", "texture-ref"
    if constraint.values is not None:
        if len(constraint.values) == 1:
            return "lit", constraint.values[0]
        return (
            "ref",
            "( "
            + " | ".join(_literal(_DQ + v + _DQ) for v in constraint.values)
            + " )",
        )
    return "ref", "string"


def _verb_rule_name(verb: Verb) -> str:
    return _sanitize(f"verb-{verb.intent}")


def _texture_rule_name(noun: Noun) -> str:
    return _sanitize(f"texture-ref-{noun.id}")


def _texture_rule(noun: Noun) -> str:
    """One live entry's verbatim reference as a literal alternative — the
    copy-verbatim law at the source: the engine can only name what the
    narrator established (ghost interactivity structurally impossible).
    Each value rides its JSON encoding (json.dumps, ensure_ascii=False —
    the byte form the reply must carry) BEFORE the GBNF literal escape,
    so a value with quotes/backslashes round-trips verbatim through the
    gate's json.loads."""
    assert noun.texture is not None  # the caller filters texture nouns
    body = ", ".join(
        f"{_DQ}{key}{_DQ}: {json.dumps(str(noun.texture[key]), ensure_ascii=False)}"
        for key in ("entry", "scope", "slot", "value")
    )
    return f"{_texture_rule_name(noun)} ::= " + _literal("{" + body + "}")


def _merge_literals(body: str) -> str:
    """Merge directly adjacent string literals into one (cosmetic,
    INV-2-neutral): the emitter assembles JSON fragments (`{`, `", "`,
    pair literals) and the merged form is the single readable literal a
    station operator reads. Escaped contents concatenate safely — both
    fragments are already valid escaped bodies."""
    parts: list[tuple[str, str]] = []  # (kind, text): "lit" | "other"
    i, n = 0, len(body)
    while i < n:
        if body[i] == _DQ:
            j = i + 1
            while j < n:
                if body[j] == "\\":
                    j += 2
                elif body[j] == _DQ:
                    break
                else:
                    j += 1
            if j >= n:
                raise ValueError(f"unterminated literal in rule body: {body!r}")
            content = body[i + 1 : j]
            if parts and parts[-1][0] == "lit":
                parts[-1] = ("lit", parts[-1][1] + content)
            else:
                parts.append(("lit", content))
            i = j + 1
        else:
            parts.append(("other", body[i]))
            i += 1
    return "".join(
        (_DQ + text + _DQ) if kind == "lit" else text for kind, text in parts
    )


def _sanitize(name: str) -> str:
    """Rule identifiers carry no underscores (the b11064 dialect: parse
    failure; dashes fine) — pack identifiers are sanitized, never
    assumed clean."""
    return name.replace("_", "-")


def _literal(text: str) -> str:
    """A GBNF string literal for a JSON fragment: the escaped body in
    double quotes. Only the measured-supported escapes are emitted
    (`\"`, `\\` — json.gbnf's own form); a control character has no
    literal form in this dialect and refuses LOUD (a pack-authoring bug
    on the value, never a silently-broken grammar)."""
    escaped: list[str] = []
    for char in text:
        if char == _DQ:
            escaped.append('\\"')
        elif char == "\\":
            escaped.append("\\\\")
        elif ord(char) < 0x20 or ord(char) == 0x7F:
            raise ValueError(
                f"a grammar literal cannot carry the control character "
                f"{char!r} (the b11064 dialect has no literal escape for "
                f"it) — the pack value is unparseable at the source: {text!r}"
            )
        else:
            escaped.append(char)
    return _DQ + "".join(escaped) + _DQ
