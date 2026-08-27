"""Minimal JSON-Schema validator for the subset canonsim uses (KI#10, D-032).

Schema-driven, no contract duplication: `schemas/event.schema.json` is the
single machine contract and this module validates instances against it with
zero runtime dependencies (D-012). Supported keywords: `type` (string or list
form), `properties`, `required`, `enum`, `pattern` (JSON-Schema semantics:
unanchored search, strings only), `additionalProperties` (boolean form),
`items` (single-schema form), `minimum`, and `$defs` + local `$ref`
(`#/$defs/<name>` only). Annotation keywords (`title`, `description`,
`default`, `$schema`, `$id`, `$comment`) are ignored. Any other keyword fails
loudly at validation time — a schema that grew past the subset must never
pass silently (fail-fast, `docs/blueprint/phase0.md` §1).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

__all__ = ["SchemaError", "ValidationError", "validate"]


class SchemaError(ValueError):
    """The schema itself is malformed or uses an unsupported keyword."""


class ValidationError(ValueError):
    """The instance does not match the schema."""


# Keywords this validator understands or deliberately ignores (annotations).
_SUPPORTED: frozenset[str] = frozenset(
    {"$ref", "type", "enum", "pattern", "properties", "required",
     "additionalProperties", "items", "minimum"}
)
_ANNOTATIONS: frozenset[str] = frozenset(
    {"$schema", "$id", "title", "description", "default", "$comment", "$defs"}
)


def _is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


_TYPE_CHECKS: Mapping[str, Any] = {
    "object": lambda v: isinstance(v, Mapping),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": _is_integer,
    "number": lambda v: _is_integer(v) or isinstance(v, float),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def _check_type(instance: Any, expected: str, path: str) -> None:
    check = _TYPE_CHECKS.get(expected)
    if check is None:
        raise SchemaError(f"unsupported type {expected!r} at {path}")
    if not check(instance):
        raise ValidationError(f"{path}: expected type {expected!r}, got {type(instance).__name__}")


def _resolve_ref(ref: Any, root: Mapping[str, Any], path: str) -> Mapping[str, Any]:
    if not isinstance(ref, str) or not ref.startswith("#/$defs/"):
        raise SchemaError(f"{path}: only local '#/$defs/<name>' $ref is supported, got {ref!r}")
    name = ref[len("#/$defs/"):]
    defs = root.get("$defs")
    if not isinstance(defs, Mapping) or name not in defs:
        raise SchemaError(f"{path}: $ref target {ref!r} not found in $defs")
    target = defs[name]
    if not isinstance(target, Mapping):
        raise SchemaError(f"{path}: $ref target {ref!r} is not an object")
    return target


def validate(
    instance: Any,
    schema: Mapping[str, Any],
    *,
    _root: Mapping[str, Any] | None = None,
    _path: str = "$",
    _active_refs: frozenset[str] = frozenset(),
) -> None:
    """Validate `instance` against `schema`; raise ValidationError/SchemaError.

    `_root`, `_path` and `_active_refs` are internal recursion parameters.
    """
    if not isinstance(schema, Mapping):
        raise SchemaError(f"{_path}: schema must be an object")

    root = schema if _root is None else _root
    unknown = set(schema) - _SUPPORTED - _ANNOTATIONS
    if unknown:
        raise SchemaError(f"{_path}: unsupported schema keyword(s): {sorted(unknown)}")

    if "$ref" in schema:
        ref = schema["$ref"]
        if ref in _active_refs:
            raise SchemaError(f"{_path}: cyclic $ref {ref!r}")
        target = _resolve_ref(ref, root, _path)
        validate(
            instance,
            target,
            _root=root,
            _path=_path,
            _active_refs=_active_refs | {ref},
        )
        return

    if "type" in schema:
        expected = schema["type"]
        if isinstance(expected, str):
            _check_type(instance, expected, _path)
        elif isinstance(expected, list) and expected:
            if not any(_TYPE_CHECKS.get(t, lambda v: False)(instance) for t in expected):
                raise ValidationError(
                    f"{_path}: expected one of {expected!r}, got {type(instance).__name__}"
                )
            for entry in expected:
                if entry not in _TYPE_CHECKS:
                    raise SchemaError(f"{_path}: unsupported type {entry!r} in type list")
        else:
            raise SchemaError(f"{_path}: 'type' must be a string or non-empty list")

    if "enum" in schema:
        enum = schema["enum"]
        if not isinstance(enum, list):
            raise SchemaError(f"{_path}: 'enum' must be an array")
        if instance not in enum:
            raise ValidationError(f"{_path}: {instance!r} not in enum {enum!r}")

    if "pattern" in schema:
        pattern = schema["pattern"]
        if not isinstance(pattern, str):
            raise SchemaError(f"{_path}: 'pattern' must be a string")
        if isinstance(instance, str) and re.search(pattern, instance) is None:
            raise ValidationError(f"{_path}: {instance!r} does not match {pattern!r}")

    if "minimum" in schema:
        minimum = schema["minimum"]
        if not _is_integer(minimum) and not isinstance(minimum, float):
            raise SchemaError(f"{_path}: 'minimum' must be a number")
        if (_is_integer(instance) or isinstance(instance, float)) and instance < minimum:
            raise ValidationError(f"{_path}: {instance!r} < minimum {minimum!r}")

    if "properties" in schema:
        props = schema["properties"]
        if not isinstance(props, Mapping):
            raise SchemaError(f"{_path}: 'properties' must be an object")
        if isinstance(instance, Mapping):
            for key in sorted(props):
                if key in instance:
                    validate(instance[key], props[key], _root=root, _path=f"{_path}.{key}")

    if "required" in schema:
        required = schema["required"]
        if not isinstance(required, list):
            raise SchemaError(f"{_path}: 'required' must be an array")
        if isinstance(instance, Mapping):
            for key in required:
                if key not in instance:
                    raise ValidationError(f"{_path}: missing required property {key!r}")

    if "additionalProperties" in schema:
        extra = schema["additionalProperties"]
        if not isinstance(extra, bool):
            raise SchemaError(f"{_path}: only boolean 'additionalProperties' is supported")
        if extra is False and isinstance(instance, Mapping):
            props = schema.get("properties", {})
            for key in instance:
                if key not in props:
                    raise ValidationError(f"{_path}: unexpected property {key!r}")

    if "items" in schema:
        items = schema["items"]
        if not isinstance(items, Mapping):
            raise SchemaError(f"{_path}: only the single-schema 'items' form is supported")
        if isinstance(instance, list):
            for index, item in enumerate(instance):
                validate(item, items, _root=root, _path=f"{_path}[{index}]")
