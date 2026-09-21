"""engine-1 acceptance — the GBNF mapping (iter-177, D-193; the mapping
`brief/gbnf.py`, its laws `docs/PARSER_SPEC.md` §2.1, the build contract
CONTRACTS §4.1 D6/I3: ONE INV-3-clean pure function over the grammar
snapshot).

The pins:

- **determinism + the golden grammar**: same snapshot → same bytes,
  byte-identical to the committed fixture `parse_gbnf_seed125.gbnf`
  (the tavern pack, seed 125, fresh open; the regen protocol:
  `scripts/regen_parse_gbnf.py` — any byte drift is a grammar-contract
  change, never silent);
- **the dialect laws** (measured at llama.cpp b11064, TECH_NOTES
  §13.1): rule names carry no underscores; the char classes and the
  optional groups are the documented forms;
- **the corpus correspondence** (the §4.3 zero-gate-edit evidence's
  grammar half): EVERY intent reply in the engine-1 deviation corpus —
  both models, verbatim — is in the grammar's language, and every
  pinned malformed probe is OUTSIDE it (the f1b degenerate empty
  no_intent structurally impossible). The oracle is an independent
  re-derivation (TEST_PLAN §9's law): a regex conversion of the emitted
  GBNF subset — literals, references, groups, alternation, classes map
  mechanically onto Python `re` — never a second grammar engine;
- **the door's shape laws at the source**: the one-path law (a texture
  verb's canon and texture paths are separate alternatives — the s2c1
  combo cannot be emitted), canon-nouns-only targets (texture ids never
  targets), the drawn-`N` ticks field required, empty-enum fields never
  offered;
- **the literal escapes**: quotes and backslashes round-trip through
  JSON; control characters refuse LOUD (the dialect has no literal
  escape for them);
- **the fingerprint**: the D3 manifest's grammar id — stable, and moved
  by any grammar change.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from brief.gbnf import gbnf_grammar, grammar_fingerprint
from brief.ledger import SceneLedger
from brief.parser import (
    FieldConstraint,
    GrammarSnapshot,
    Noun,
    Verb,
    grammar_snapshot,
)
from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
ENGINE1 = json.loads(
    (REPO / "tests" / "fixtures" / "engine1_deviation_corpus.json").read_text(
        encoding="utf-8")
)


def _snapshot_at_open() -> GrammarSnapshot:
    """The pinned golden state: the tavern pack, seed 125, fresh open,
    an empty ledger (the fixture's own anchor)."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "run.jsonl"
        sim = Simulator(PACK, 125, log, SCHEMA, commit="0000000")
        sim.open()
        _header, events = read_log(log, SCHEMA)
        return grammar_snapshot(events, PACK, SceneLedger())


# -- the regex oracle (an independent re-derivation, never a 2nd engine) -------


def _rules(grammar: str) -> dict[str, str]:
    return {
        line.split(" ::= ", 1)[0]: line.split(" ::= ", 1)[1]
        for line in grammar.splitlines()
    }


def _unescape(literal: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(literal):
        if literal[i] == "\\" and i + 1 < len(literal):
            out.append(literal[i + 1])
            i += 2
        else:
            out.append(literal[i])
            i += 1
    return "".join(out)


def _rule_regex(name: str, rules: dict[str, str], seen: tuple[str, ...]) -> str:
    """One rule body as a Python regex: GBNF literals, references,
    groups, alternation, repetition and char classes map mechanically
    onto `re` (the emitted subset only — the oracle's own fence)."""
    assert name not in seen, f"recursion at {name}"
    body = rules[name]
    out: list[str] = []
    i, n = 0, len(body)
    while i < n:
        char = body[i]
        if char == '"':  # a literal: unescape its body, regex-escape it
            j = i + 1
            content: list[str] = []
            while j < n:
                if body[j] == "\\":
                    content.append(body[j : j + 2])
                    j += 2
                elif body[j] == '"':
                    break
                else:
                    content.append(body[j])
                    j += 1
            out.append(re.escape(_unescape("".join(content))))
            i = j + 1
        elif char == "(":
            out.append("(?:")
            i += 1
        elif char in ")|*":
            out.append(char)
            i += 1
        elif char == "[":  # a char class: GBNF and re share the syntax
            close = body.index("]", i)
            out.append(body[i : close + 1])
            i = close + 1
        elif char.isspace():
            i += 1
        else:  # a rule reference
            j = i
            while j < n and (body[j].isalnum() or body[j] == "-"):
                j += 1
            out.append(_rule_regex(body[i:j], rules, seen + (name,)))
            i = j
    return "(?:" + "".join(out) + ")"


def _language_re(grammar: str) -> re.Pattern[str]:
    return re.compile(_rule_regex("root", _rules(grammar), ()))


def _corpus_replies(model: str) -> list[dict[str, Any]]:
    return [
        cycle["reply"]
        for case in ENGINE1["engines"][model]["cases"]
        for cycle in case["cycles"]
        if cycle.get("reply") is not None
    ]


# -- determinism + the golden fixture ------------------------------------------


def test_the_golden_grammar_bytes() -> None:
    """Byte-identity with the committed fixture; the regen protocol is
    `scripts/regen_parse_gbnf.py` over the pinned state (any drift is a
    grammar-contract change, never silent)."""
    grammar = gbnf_grammar(_snapshot_at_open())
    fixture = (REPO / "tests" / "fixtures" / "parse_gbnf_seed125.gbnf").read_text(
        encoding="utf-8"
    )
    assert grammar == fixture


def test_same_snapshot_same_bytes() -> None:
    snapshot = _snapshot_at_open()
    assert gbnf_grammar(snapshot) == gbnf_grammar(snapshot)


# -- the dialect laws (b11064, TECH_NOTES §13.1) -------------------------------


def test_rule_names_carry_no_underscores() -> None:
    grammar = gbnf_grammar(_snapshot_at_open())
    names = [
        line.split(" ::= ")[0] for line in grammar.splitlines()
    ]
    assert names and all("_" not in name for name in names)


def test_the_string_rule_demands_a_non_empty_body() -> None:
    """The f1b leak shape (`{"no_intent": ""}`) is structurally
    impossible: the string rule is one-or-more chars, never `*`."""
    grammar = gbnf_grammar(_snapshot_at_open())
    string_rule = _rules(grammar)["string"]
    assert "string-char ( string-char )*" in string_rule
    language = _language_re(grammar)
    assert language.match('{"no_intent": ""}') is None
    assert language.match('{"no_intent": "loitering"}') is not None


# -- the corpus correspondence (§4.3's grammar half) ----------------------------


@pytest.mark.parametrize("model", sorted(ENGINE1["engines"]))
def test_every_corpus_intent_reply_is_in_the_language(model: str) -> None:
    """Both models' station replies, verbatim (the fixture's canonical
    byte form), are describable by the grammar — the grammar's language
    covers everything the station's own v2 grammar let through on this
    corpus, zero gate edits."""
    grammar = gbnf_grammar(_snapshot_at_open())
    language = _language_re(grammar)
    checked = 0
    for reply in _corpus_replies(model):
        if "intent" not in reply:
            continue  # question/no_intent: the string rule's own pin
        text = json.dumps(reply, ensure_ascii=False)
        assert language.fullmatch(text), text
        checked += 1
    assert checked > 0


@pytest.mark.parametrize("model", sorted(ENGINE1["engines"]))
def test_the_pinned_malformed_probes_are_outside(model: str) -> None:
    """Every probe the corpus pins as gate-refusing is outside the
    grammar's language too (the grammar is narrower than the gate,
    never wider). The corpus carries the leak probe on the e4b side
    (the f1b degenerate empty no_intent); models without probes pin
    the negative arm only."""
    grammar = gbnf_grammar(_snapshot_at_open())
    language = _language_re(grammar)
    probes = [
        probe
        for case in ENGINE1["engines"][model]["cases"]
        for cycle in case["cycles"]
        for probe in cycle.get("probes", ())
    ]
    if model == "e4b":
        assert probes  # the f1b leak probe is pinned on this side
    for probe in probes:
        assert language.fullmatch(json.dumps(probe)) is None, probe


# -- the door's shape laws at the source ----------------------------------------


def _texture_snapshot() -> GrammarSnapshot:
    """The tavern verbs plus ONE live texture entry (the ledger's own
    shape, constructed directly — the snapshot dataclasses are public)."""
    base = _snapshot_at_open()
    entry = {
        "entry": "tex_0000",
        "scope": "scene:loc_tavern",
        "slot": "candles",
        "value": "lit",
    }
    return GrammarSnapshot(
        verbs=base.verbs,
        nouns=base.nouns
        + (Noun(id="tex_0000", kind="texture", name="A few candles", texture=entry),),
    )


def test_the_one_path_law_is_encoded() -> None:
    """The s2c1 crash form — `take` pairing a target WITH the texture
    reference — cannot be emitted: the canon path (target, no texture
    field) and the texture path (null target, the verbatim reference)
    are SEPARATE alternatives, never both."""
    grammar = gbnf_grammar(_texture_snapshot())
    language = _language_re(grammar)
    reference = {
        "entry": "tex_0000", "scope": "scene:loc_tavern",
        "slot": "candles", "value": "lit",
    }
    # the texture path: null target + the verbatim reference — IN
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "take", "target": None,
                   "fields": {"texture": reference}}
    })) is not None
    # the canon path: a canon target, no texture field — IN
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "take", "target": "rope_01", "fields": {}}
    })) is not None
    # the one-path combo: target AND texture — OUT (the s2c1 form)
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "take", "target": "tex_0000",
                   "fields": {"texture": reference}}
    })) is None
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "take", "target": "rope_01",
                   "fields": {"texture": reference}}
    })) is None


def test_canon_targets_exclude_texture_ids() -> None:
    grammar = gbnf_grammar(_texture_snapshot())
    canon_target = _rules(grammar)["canon-target"]
    # the entry is a listed noun (its id rides the texture-ref literal)
    # but never a target
    assert "tex_0000" in grammar
    assert "tex_0000" not in canon_target
    # and the texture reference itself rides verbatim, escapes and all
    assert '\\"entry\\": \\"tex_0000\\"' in grammar


def test_the_drawn_n_ticks_field_is_required() -> None:
    """`wait` has no empty-fields alternative: the door's accept-time
    law (a drawn-`N` verb demands its ticks step field) holds at the
    source."""
    grammar = gbnf_grammar(_snapshot_at_open())
    wait = _rules(grammar)["verb-wait"]
    assert "ticks" in wait and "positive-int" in wait
    assert "{}" not in wait  # no empty-fields alternative on this verb
    language = _language_re(grammar)
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "wait", "target": None, "fields": {"ticks": 5}}
    })) is not None
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "wait", "target": None, "fields": {}}
    })) is None
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "wait", "target": None, "fields": {"ticks": 0}}
    })) is None
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "wait", "target": None, "fields": {"ticks": "5"}}
    })) is None


def test_the_empty_enum_field_is_never_offered() -> None:
    """`drop_break` at the street: the `near` spot list is empty (`<none
    available>` in the call document) — the grammar offers no near field
    at all."""
    grammar = gbnf_grammar(_snapshot_at_open())
    drop = _rules(grammar)["verb-drop-break"]
    assert "near" not in drop
    language = _language_re(grammar)
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "drop_break", "target": "rope_01", "fields": {}}
    })) is not None
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "drop_break", "target": "rope_01",
                   "fields": {"near": "bar"}}
    })) is None


def test_the_closed_enums_ride_verbatim() -> None:
    grammar = gbnf_grammar(_snapshot_at_open())
    steal = _rules(grammar)["verb-steal"]
    assert '"{\\"method\\": \\"distraction\\"}"' in steal
    language = _language_re(grammar)
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "steal", "target": "purse_01",
                   "fields": {"method": "distraction"}}
    })) is not None
    assert language.fullmatch(json.dumps({
        "intent": {"kind": "steal", "target": "purse_01",
                   "fields": {"method": "violence"}}
    })) is None


# -- the escapes and the guards --------------------------------------------------


def test_literals_round_trip_through_json() -> None:
    """A texture value carrying quotes and backslashes survives the
    literal escape verbatim (json.gbnf's own forms): the emitted GBNF
    literal is itself a valid JSON string whose parsed body IS the
    verbatim reference object."""
    entry = {
        "entry": "tex_0001", "scope": "scene:loc_tavern",
        "slot": "note", "value": 'a "quoted" \\ value',
    }
    snapshot = GrammarSnapshot(
        verbs=(Verb(intent="take", label="take", target_required=True,
                    fields=(FieldConstraint("texture", texture=True),)),),
        nouns=(
            Noun(id="rope_01", kind="item", name="the rope"),
            Noun(id="tex_0001", kind="texture", name="note",
                 texture=entry),
        ),
    )
    grammar = gbnf_grammar(snapshot)
    literal = re.search(
        r'texture-ref-tex-0001 ::= ("(?:[^"\\]|\\.)*")', grammar
    )
    assert literal is not None
    reference_text = json.loads(literal.group(1))  # the JSON string body
    assert json.loads(reference_text) == entry  # the verbatim object
    # a control-character VALUE rides its JSON encoding verbatim (the
    # newline becomes the two-char \n escape inside the reply's bytes)
    entry_nl = dict(entry, entry="tex_0002", value="a\nnewline")
    snapshot_nl = GrammarSnapshot(
        verbs=snapshot.verbs,
        nouns=snapshot.nouns
        + (Noun(id="tex_0002", kind="texture", name="note",
                texture=entry_nl),),
    )
    grammar_nl = gbnf_grammar(snapshot_nl)
    literal_nl = re.search(
        r'texture-ref-tex-0002 ::= ("(?:[^"\\]|\\.)*")', grammar_nl
    )
    assert literal_nl is not None
    assert json.loads(json.loads(literal_nl.group(1))) == entry_nl


def test_control_characters_refuse_loud() -> None:
    """A canon identifier carrying a control character has no literal
    form in the measured dialect (json.gbnf's escapes only) — loud, never
    a silently-broken grammar. (A texture VALUE with a control character
    rides its JSON encoding — the round-trip test's own pin.)"""
    snapshot = GrammarSnapshot(
        verbs=(Verb(intent="take", label="take", target_required=True),),
        nouns=(
            Noun(id="rope\n01", kind="item", name="the rope"),
        ),
    )
    with pytest.raises(ValueError, match="control character"):
        gbnf_grammar(snapshot)


def test_no_canon_nouns_refuses_loud() -> None:
    snapshot = GrammarSnapshot(
        verbs=(Verb(intent="wait", label="wait", target_required=False),),
        nouns=(),
    )
    with pytest.raises(ValueError, match="no canon nouns"):
        gbnf_grammar(snapshot)


# -- the fingerprint (the D3 manifest's grammar id) ------------------------------


def test_the_fingerprint_is_stable_and_sensitive() -> None:
    base = gbnf_grammar(_snapshot_at_open())
    assert grammar_fingerprint(base) == grammar_fingerprint(base)
    assert len(grammar_fingerprint(base)) == 16
    other = gbnf_grammar(_texture_snapshot())
    assert grammar_fingerprint(base) != grammar_fingerprint(other)
