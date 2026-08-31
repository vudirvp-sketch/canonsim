"""The parser boundary's document layer (phase 2, mode C — blueprint §2;
format/contract owner `docs/PARSER_SPEC.md`, decision D-062).

The parser lives OUTSIDE the codebase at dev-time, exactly like the
narrator (D-055): an operator — or, later, a grammar-constrained runtime
model behind the owner-gated engine decision — reads a parse call document
and writes a parse reply document; the repo stays LLM-free and
network-free (INV-4 unchanged). This module is the boundary's PURE half,
document assembly and inspection as functions of (log, pack, ledger):

- the **grammar snapshot** — the closed target grammar as data: the pack's
  action intents (verbs, with the declared fields and their pack-derivable
  value constraints) plus the addressable nouns (canon entities + live
  texture entries). Ghost interactivity is structurally impossible: any
  noun the narrator established is parseable by construction; anything
  else in the player's words takes the disambiguation path (the question
  alternative — uncertainty is surfaced, never guessed, blueprint §2);
- the **call document** — the player's utterance verbatim + the snapshot
  + the parse protocol (the closed reply grammar);
- the **reply document gate** — one CLOSED document with exactly one
  alternative: an intent (checked against the snapshot: kind, target,
  field names and values, texture references), a disambiguation question,
  or a no-intent verdict. Off-grammar output is a loud ParseError AT the
  boundary; the session prints it and nothing feeds the door — the world
  never moves on a malformed parse (the runtime re-ask ladder is deferred
  with the runtime engine decision, PARSER_SPEC §7).

Field constraints are derived, never hardcoded per action: `ticks` is a
positive integer when the pack declares the drawn-`N` form, `method` is
the rules' modifier-table keys, `near` is the action's ignition layer's
spot list on the actor's current location (the same list the completion
resolver validates against, so snapshot and door agree by construction),
`texture` is a live-entry reference on texture-capable verbs
(INTENT_SCHEMA §9 owns the field grammar). One path per intent
(texture reference XOR target) is enforced at the door, not here — one
owner per law, `core/intent.py::validate_shape`.

No RNG, no wall-clock, no I/O, writes nothing (INV-1/2/4; same
(log, ledger, pack) → same call bytes — the D-049 quarantine family).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from brief.ledger import SceneLedger
from core.fold import fold, initial_projection
from core.log import EventRecord
from core.pack import Pack

__all__ = [
    "FieldConstraint",
    "GrammarSnapshot",
    "Noun",
    "ParseError",
    "ParseReply",
    "ParsedIntent",
    "Verb",
    "grammar_snapshot",
    "parse_call",
    "parse_reply_from_mapping",
]

#: The call document's section ids (PARSER_SPEC §3 block geometry).
PLAYER_INPUT_BLOCK: str = "player_input"
GRAMMAR_BLOCK: str = "grammar"
PROTOCOL_BLOCK: str = "parse_protocol"

#: The reply document's closed alternative set (PARSER_SPEC §4).
_ALTERNATIVES: tuple[str, ...] = ("intent", "question", "no_intent")


class ParseError(RuntimeError):
    """The reply document's grammar violation, or parse-cycle misuse: the
    emitter (the external parser) is outside the codebase, so the boundary
    treats this family as off-grammar output — loud, caught by the session
    BEFORE anything feeds the door; never a crash, never a silent drop."""


@dataclass(frozen=True, slots=True)
class FieldConstraint:
    """One verb field's grammar as the snapshot derives it from pack data:
    a closed value enum (`values`), a positive-integer drawn-duration
    field (`positive_int`), or a live texture-entry reference (`texture`).
    `values=None` with both flags false is an open string the door
    validates downstream (the boundary never duplicates door-owned
    checks — one owner per law)."""

    name: str
    values: tuple[str, ...] | None = None
    positive_int: bool = False
    texture: bool = False


@dataclass(frozen=True, slots=True)
class Verb:
    """One addressable action intent: the pack's intent name, its display
    label (for word matching against the player's utterance), whether the
    preconditions require a target, and the declared fields' constraints."""

    intent: str
    label: str
    target_required: bool
    fields: tuple[FieldConstraint, ...] = ()


@dataclass(frozen=True, slots=True)
class Noun:
    """One addressable noun: a canon entity (id, category, display name),
    or a live texture entry (the copy-verbatim reference a texture-capable
    verb's field must carry, with the entry's surface prose for word
    matching — the narrator's own words, parseable by construction)."""

    id: str
    kind: str
    name: str
    texture: Mapping[str, str] | None = None


@dataclass(frozen=True, slots=True)
class GrammarSnapshot:
    """The closed target grammar for one parse call (blueprint §2: the
    pack's verbs plus the addressable nouns). Construction order
    throughout — pack declaration order for verbs and entities, ledger
    append order for texture entries (INV-2)."""

    verbs: tuple[Verb, ...] = ()
    nouns: tuple[Noun, ...] = ()


@dataclass(frozen=True, slots=True)
class ParsedIntent:
    """The intent alternative of a reply: one classification with slots,
    never free-form generation — kind, optional target, optional declared
    fields. The door (INTENT_SCHEMA §2) owns everything downstream."""

    kind: str
    target: str | None = None
    fields: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ParseReply:
    """One parse reply, gated: exactly one alternative is set — a parsed
    intent, a disambiguation question (uncertainty surfaced, never
    guessed), or a no-intent verdict (the utterance carries no
    world-touching intent)."""

    intent: ParsedIntent | None = None
    question: str | None = None
    no_intent: str | None = None


# -- the grammar snapshot -------------------------------------------------------


def grammar_snapshot(
    events: Sequence[EventRecord], pack: Pack, ledger: SceneLedger
) -> GrammarSnapshot:
    """The closed target grammar as data (pure): the pack's action intents
    with their field constraints, plus the addressable nouns — every canon
    entity and every live texture entry. The `near` enum derives from the
    actor's current position, so the projection is folded here (a pure
    function of the log; the snapshot never stores it)."""
    state = fold(events, initial_projection(pack.entities))
    position = state[pack.player_id()]["position"]
    verbs = tuple(
        _verb(action, pack, position)
        for action in pack.data["actions.json"]["actions"]
    )
    nouns = [
        Noun(id=record["id"], kind=kind, name=str(record.get("name", record["id"])))
        for category, kind in (
            ("locations", "location"),
            ("npcs", "npc"),
            ("ambient_entities", "ambient"),
            ("items", "item"),
        )
        for record in pack.entities[category]
    ]
    nouns.extend(
        Noun(
            id=entry.id, kind="texture", name=entry.surface,
            texture={
                "entry": entry.id, "scope": entry.scope,
                "slot": entry.slot, "value": entry.value,
            },
        )
        for entry in ledger.live()
    )
    return GrammarSnapshot(verbs=verbs, nouns=tuple(nouns))


def _verb(action: Mapping[str, Any], pack: Pack, position: str) -> Verb:
    """One verb's grammar, derived from pack data only (INV-3): the
    declared fields with their derivable constraints, and the
    target-required flag read from the preconditions exactly as the door's
    own shape gate derives it (`core/intent.py::validate_shape`)."""
    target_required = any(
        value == "target"
        for cond in action.get("requires", ())
        for value in cond.values()
    )
    constraints = []
    for name in action.get("fields", ()):
        if name == "ticks" and action.get("ticks") == "N":
            constraints.append(FieldConstraint(name, positive_int=True))
        elif name == "method":
            methods = pack.rules.get("checks", {}).get("methods", {})
            constraints.append(FieldConstraint(name, values=tuple(methods)))
        elif name == "near":
            constraints.append(FieldConstraint(name, values=_spot_values(action, pack, position)))
        elif name == "texture" and action.get("texture") is not None:
            constraints.append(FieldConstraint(name, texture=True))
        else:
            constraints.append(FieldConstraint(name))
    return Verb(
        intent=str(action["intent"]),
        label=str(action.get("label", action["intent"])),
        target_required=target_required,
        fields=tuple(constraints),
    )


def _spot_values(
    action: Mapping[str, Any], pack: Pack, position: str
) -> tuple[str, ...] | None:
    """The `near` field's closed values: the action's ignition layer's
    spot list on the actor's current location — the same list the
    completion resolver validates against, so the grammar and the door
    agree by construction. No ignition config → no derivable enum
    (`None` = open; the door owns that value's validation)."""
    config = action.get("ignition")
    if config is None:
        return None
    layer = pack.rules["transitions"][config["layer"]]
    record = pack.entity(position) or {}
    return tuple(record.get(layer["spot_field"], ()))


# -- the call document (PARSER_SPEC §3) -----------------------------------------


def parse_call(
    text: str,
    events: Sequence[EventRecord],
    pack: Pack,
    ledger: SceneLedger,
) -> str:
    """Assemble the parse call document (pure): the player's utterance
    verbatim, the grammar snapshot, and the parse protocol — everything
    the external parser may draw on for one utterance. Same
    (log, ledger, pack, text) → same bytes."""
    snapshot = grammar_snapshot(events, pack, ledger)
    lines = [f"## {PLAYER_INPUT_BLOCK}", text, "", f"## {GRAMMAR_BLOCK}", "verbs:"]
    for verb in snapshot.verbs:
        parts = [f"  {verb.intent} \"{verb.label}\""]
        if verb.target_required:
            parts.append("[target required]")
        parts.extend(_render_field(constraint) for constraint in verb.fields)
        lines.append(" ".join(parts))
    lines.append("nouns:")
    lines.extend(
        f"  {noun.id} ({noun.kind}) \"{noun.name}\""
        for noun in snapshot.nouns
        if noun.texture is None
    )
    texture = [noun for noun in snapshot.nouns if noun.texture is not None]
    if texture:
        lines.append("texture entries:")
        lines.extend(
            f"  {noun.texture['entry']} {noun.texture['scope']} "
            f"{noun.texture['slot']}={noun.texture['value']} \"{noun.name}\""
            for noun in texture
        )
    lines.extend([
        "", f"## {PROTOCOL_BLOCK}",
        "reply: ONE JSON object with exactly one alternative —",
        "  {\"intent\": {\"kind\": \"<verb>\", \"target\": \"<noun id>\", \"fields\": {...}}}",
        "  {\"question\": \"<ask the player — never guess>\"}",
        "  {\"no_intent\": \"<the utterance carries no world-touching intent>\"}",
        "kind must be a listed verb; target (when given) a listed noun id; only",
        "the listed fields, with the listed values; the texture field copies one",
        "texture entry's {\"entry\", \"scope\", \"slot\", \"value\"} verbatim — and",
        "carries no \"target\" (one path per intent, INTENT_SCHEMA §3).",
    ])
    return "\n".join(lines) + "\n"


def _render_field(constraint: FieldConstraint) -> str:
    if constraint.texture:
        return f"{constraint.name}=<a live texture entry>"
    if constraint.positive_int:
        return f"{constraint.name}=<positive integer>"
    if constraint.values is None:
        return f"{constraint.name}=<string>"
    if not constraint.values:
        return f"{constraint.name}=<none available>"
    return f"{constraint.name}=one of: {', '.join(constraint.values)}"


# -- the reply document gate (PARSER_SPEC §4) -----------------------------------


def parse_reply_from_mapping(doc: Any, snapshot: GrammarSnapshot) -> ParseReply:
    """Gate one parse reply against the snapshot (loud ParseError on any
    off-grammar output — the document is closed). Exactly one alternative:
    an intent (deep-checked: kind, target, fields, values, texture
    references), a question, or a no-intent verdict. The door owns every
    check this gate does not derive from the snapshot (preconditions,
    target-required, the one-path law) — one owner per law."""
    if not isinstance(doc, Mapping):
        raise ParseError(f"reply must be an object, got {type(doc).__name__}")
    keys = set(doc)
    alternatives = keys & set(_ALTERNATIVES)
    if len(alternatives) != 1 or keys != alternatives:
        raise ParseError(
            f"reply must carry exactly one of {'|'.join(_ALTERNATIVES)}, "
            f"got {sorted(keys)} — the document is closed"
        )
    if "question" in doc:
        return ParseReply(question=_non_empty_str(doc["question"], "question"))
    if "no_intent" in doc:
        return ParseReply(no_intent=_non_empty_str(doc["no_intent"], "no_intent"))
    return ParseReply(intent=_parsed_intent(doc["intent"], snapshot))


def _parsed_intent(doc: Any, snapshot: GrammarSnapshot) -> ParsedIntent:
    if not isinstance(doc, Mapping):
        raise ParseError(f"intent must be an object, got {type(doc).__name__}")
    unknown = [key for key in doc if key not in ("kind", "target", "fields")]
    if unknown:
        raise ParseError(
            f"intent: unknown keys {sorted(unknown)} — the document is closed"
        )
    if "kind" not in doc:
        raise ParseError("intent: missing required key 'kind'")
    kind = _non_empty_str(doc["kind"], "intent kind")
    verb = next((verb for verb in snapshot.verbs if verb.intent == kind), None)
    if verb is None:
        raise ParseError(
            f"intent kind {kind!r} is not in the grammar "
            f"(verbs: {[verb.intent for verb in snapshot.verbs]})"
        )
    target = doc.get("target")
    if target is not None:
        target = _non_empty_str(target, "intent target")
        if not any(noun.id == target for noun in snapshot.nouns):
            raise ParseError(
                f"intent target {target!r} is not an addressable noun — "
                "take the disambiguation path instead of guessing"
            )
    fields = doc.get("fields", {})
    if not isinstance(fields, Mapping):
        raise ParseError("intent fields must be an object")
    by_name = {constraint.name: constraint for constraint in verb.fields}
    extras = set(fields) - set(by_name)
    if extras:
        raise ParseError(
            f"{kind} takes no fields {sorted(extras)}; "
            f"allowed: {sorted(by_name)}"
        )
    for name, constraint in by_name.items():
        if name not in fields:
            continue
        value = fields[name]
        if constraint.texture:
            _check_texture_reference(kind, value, snapshot)
        elif constraint.positive_int:
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ParseError(
                    f"{kind} field {name!r} must be a positive integer, got {value!r}"
                )
        elif constraint.values is not None:
            if value not in constraint.values:
                raise ParseError(
                    f"{kind} field {name!r} must be one of "
                    f"{list(constraint.values)}, got {value!r}"
                )
        elif not isinstance(value, str) or not value:
            raise ParseError(
                f"{kind} field {name!r} must be a non-empty string, got {value!r}"
            )
    return ParsedIntent(kind=kind, target=target, fields=dict(fields))


def _check_texture_reference(
    kind: str, value: Any, snapshot: GrammarSnapshot
) -> None:
    """The texture field is a copy-verbatim reference to a live entry
    listed in the snapshot's texture nouns — a fabricated or stale
    reference is off-grammar (the parser can only name what the narrator
    established; ghost interactivity is structurally impossible)."""
    if not isinstance(value, Mapping):
        raise ParseError(
            f"{kind} texture must be the entry reference object, "
            f"got {type(value).__name__}"
        )
    expected = {"entry", "scope", "slot", "value"}
    if set(value) != expected:
        raise ParseError(
            f"{kind} texture must carry exactly {sorted(expected)}, "
            f"got {sorted(value)}"
        )
    live = [
        noun.texture for noun in snapshot.nouns if noun.texture is not None
    ]
    if value not in live:
        raise ParseError(
            f"{kind} texture reference {value.get('entry')!r} is not a live "
            "texture entry — take the disambiguation path instead of guessing"
        )


def _non_empty_str(value: Any, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ParseError(f"{what} must be a non-empty string, got {value!r}")
    return value
