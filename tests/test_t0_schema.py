"""T0 — schema validation (MVP_SCOPE §14, from iter-1).

Every log line validates against `schemas/event.schema.json` via the stdlib
mini-validator (KI#10 resolved, D-032). The doc examples are fixtures: the
```json blocks of `docs/EVENT_SCHEMA.md` are extracted at test time and
validated — docs, schema and validator cannot drift silently (D-010). The
log header is validated as a separate shape (§1). Plus unit coverage of the
validator subset, including loud failures on unsupported keywords.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from core.log import validate_header
from core.schema import SchemaError, ValidationError, validate

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
DOC = (REPO / "docs" / "EVENT_SCHEMA.md").read_text(encoding="utf-8")


def doc_json_blocks() -> list[dict[str, Any]]:
    blocks = re.findall(r"```json\n(.*?)```", DOC, re.DOTALL)
    return [json.loads(block) for block in blocks]


def event_blocks() -> list[dict[str, Any]]:
    return [block for block in doc_json_blocks() if "header" not in block]


def header_block() -> dict[str, Any]:
    headers = [block for block in doc_json_blocks() if "header" in block]
    assert len(headers) == 1, "EVENT_SCHEMA.md must carry exactly one header example"
    return headers[0]


# -- the doc examples are fixtures (D-010) ---------------------------------


def test_doc_canonical_example_validates() -> None:
    events = event_blocks()
    assert len(events) == 2, "expected the §3 transfer example and the §10 canonical example"
    for example in events:
        validate(example, SCHEMA)


def test_doc_transfer_example_is_the_rumor_shape() -> None:
    transfer = next(e for e in event_blocks() if e["type"] == "rumor_told")
    record = transfer["knowledge"][0]
    assert record["channel"] == "told" and record["fidelity"] == "vague"  # D-007 decay


def test_doc_header_example_matches_header_contract() -> None:
    validate_header(header_block())


# -- validator subset units -------------------------------------------------


def test_type_forms() -> None:
    validate("x", {"type": "string"})
    validate(None, {"type": ["string", "null"]})
    with pytest.raises(ValidationError):
        validate(3, {"type": "string"})
    with pytest.raises(ValidationError):
        validate(True, {"type": "integer"})  # bool is not an integer here


def test_required_and_additional_properties() -> None:
    schema = {"type": "object", "required": ["a"], "additionalProperties": False,
              "properties": {"a": {"type": "integer"}}}
    validate({"a": 1}, schema)
    with pytest.raises(ValidationError, match="missing required"):
        validate({}, schema)
    with pytest.raises(ValidationError, match="unexpected property"):
        validate({"a": 1, "b": 2}, schema)


def test_enum_and_pattern() -> None:
    validate("low", {"enum": ["low", "medium", "high"]})
    with pytest.raises(ValidationError):
        validate("huge", {"enum": ["low", "medium", "high"]})
    validate("ev_0007", {"type": "string", "pattern": "^ev_[0-9]{4,}$"})
    with pytest.raises(ValidationError):
        validate("ev_7", {"type": "string", "pattern": "^ev_[0-9]{4,}$"})
    validate("abcXYZ", {"type": "string", "pattern": "abc"})  # unanchored search semantics


def test_minimum() -> None:
    validate(0, {"type": "integer", "minimum": 0})
    with pytest.raises(ValidationError):
        validate(-1, {"type": "integer", "minimum": 0})
    validate("not a number", {"type": "string", "minimum": 0})  # non-numbers pass


def test_ref_defs_and_items() -> None:
    schema = {
        "$defs": {"kv": {"type": "object", "required": ["who"],
                         "additionalProperties": False,
                         "properties": {"who": {"type": "string"}}}},
        "type": "object",
        "required": ["records"],
        "properties": {"records": {"type": "array",
                                   "items": {"$ref": "#/$defs/kv"}}},
    }
    validate({"records": [{"who": "a"}, {"who": "b"}]}, schema)
    with pytest.raises(ValidationError):
        validate({"records": [{"who": 1}]}, schema)


def test_unsupported_keyword_fails_loudly() -> None:
    with pytest.raises(SchemaError, match="unsupported schema keyword"):
        validate(1, {"maximum": 10})


def test_cyclic_ref_fails_loudly() -> None:
    schema = {"$defs": {"a": {"$ref": "#/$defs/b"}, "b": {"$ref": "#/$defs/a"}},
              "$ref": "#/$defs/a"}
    with pytest.raises(SchemaError, match="cyclic"):
        validate(1, schema)


def test_external_ref_rejected() -> None:
    with pytest.raises(SchemaError, match="only local"):
        validate(1, {"$ref": "https://example.com/schema.json"})


# -- T0 on real logs: every line validates ----------------------------------


def test_golden_fixture_log_validates_line_by_line() -> None:
    from core.log import read_log

    golden = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
    header, events = read_log(golden, SCHEMA)  # read_log validates every line (T0)
    assert header["seed"] == 42
    assert header["pack"] == "tavern_pack@0.1"
    assert len(events) == 6
    assert all(event.id.startswith("ev_") for event in events)


def test_writer_output_validates_against_schema(tmp_path: Path) -> None:
    from core.log import read_log
    from core.loop import Simulator, load_playscript
    from core.pack import load_pack

    pack = load_pack(REPO / "content" / "tavern_pack")
    script = load_playscript(REPO / "tests" / "playscripts" / "plumbing_smoke.json")
    sim = Simulator(pack, script["seed"], tmp_path / "run.jsonl", SCHEMA, commit="0000000")
    sim.run_playscript(script)
    header, events = read_log(tmp_path / "run.jsonl", SCHEMA)
    assert header["schema_version"] == SCHEMA["$id"].rsplit("/", 1)[-1]
    assert len(events) == 6
