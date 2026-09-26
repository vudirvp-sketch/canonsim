"""The semantic diff layer over T1 (ssi-7/Phase 6, D-229 — the owner's
2026-09-26 «ssi7 и/или ssi8 ==> можешь начать» go-ahead).

Compares two canon logs at the SEMANTIC level — the additional
verification layer `docs/TEST_PLAN.md` §1.4 owns. T1's byte-identity is
environment-pinned BY DESIGN (the golden byte-compares only on the
generating interpreter, TEST_PLAN §1.1 — the documented decision this
layer never touches, never «fixes»): the semantic layer answers the
question the pin excludes — «are these two logs the same run produced
under a different interpreter, line ending, or commit?» — by comparing
the parsed event stream (the anchors id/t/type/actor/target/cause, every
deeper field by path) plus the optional run-side RngBank fingerprints
(the substantive draw count, RNG-1 — the latent-divergence axis neither
byte equality nor event equality can see: two streams can carry equal
events yet already sit at different entropy positions).

Independence law (TEST_PLAN §9's independent-re-derivation oracle +
§1.3's instrument law): this tool imports NOTHING from core/ — the log
reading is re-derived with the stdlib json module alone, so the checker
never shares the checked implementation's parser. Pure stdlib, read-only,
periphery (scripts/, D-046) — never a runtime dependency of anything.

Admission (D-198, the topology.py precedent): named consumer = the
cross-environment verification gap TEST_PLAN §1.1 documents (STATUS FAQ:
«env-pinned verification cuts both ways» — the standing pitfall); minimal
intervention = one stdlib-only script + one test file (the
instrument+pin pair); owner = the ssi phase ladder
(`docs/ssi/SSI_OVERLAY.md` §6); verification =
`tests/test_semantic_diff.py`'s claim packet (the independence arms
GREEN, every mutation arm RED — a checker that cannot fail is
decoration); scope safety = TEST_PLAN §1.4 the single law owner, this
script the instrument, never a second source of truth.

Exit codes: 0 = semantically equal; 1 = semantic delta (the report on
stdout); 2 = input error — loud, never a silent skip (SSI-N006).
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = [
    "ANCHOR_FIELDS",
    "ENVIRONMENTAL_HEADER_FIELDS",
    "SEMANTIC_HEADER_FIELDS",
    "DiffInputError",
    "EventDelta",
    "SemanticDiff",
    "compare",
    "format_report",
    "main",
    "parse_log",
]

#: The header fields that ARE the run's semantics (a difference is a
#: delta): the schema contract, the seed, the pack identity
#: (EVENT_SCHEMA.md §1 — core/log.py HEADER_KEYS is the shape owner;
#: this list only classifies the same keys).
SEMANTIC_HEADER_FIELDS: tuple[str, ...] = ("schema_version", "seed", "pack")
#: The header fields that are environment/provenance meta by design
#: (TEST_PLAN §1.1's pin; §1.4's ignore set): the generating interpreter
#: and the code commit. Reported, never failing — the layer's whole
#: point. The `header` flag itself is shape, not a field.
ENVIRONMENTAL_HEADER_FIELDS: tuple[str, ...] = ("python", "commit")
#: The per-event anchors the report names first (the phase's own
#: enumeration — event ids/types/causes/actors/targets — plus the tick,
#: the scheduler's semantic): their values headline every event delta.
ANCHOR_FIELDS: tuple[str, ...] = ("id", "t", "type", "actor", "target", "cause")
#: Report caps: the first events/field paths shown per run — the full
#: evidence stays computable, the report stays readable.
MAX_EVENT_DELTAS = 10
MAX_FIELD_PATHS = 8


class DiffInputError(RuntimeError):
    """A log that cannot be read as the canonical JSONL shape (exit 2)."""


@dataclass(frozen=True)
class EventDelta:
    """One event position where the streams disagree."""

    index: int
    #: the event's id from whichever side has it — the report's anchor
    context: str = ""
    #: differing anchors as (field, left, right) — the headline keys
    anchors: tuple[tuple[str, Any, Any], ...] = ()
    #: formatted deep paths, e.g. `outcome.duration: 4 != 7`
    fields: tuple[str, ...] = ()
    #: "left"/"right" when the event exists on one side only
    side: str | None = None


@dataclass(frozen=True)
class SemanticDiff:
    """The full comparison result; `equal` is the verdict."""

    left: Path
    right: Path
    header_semantic: tuple[tuple[str, Any, Any], ...] = ()
    header_environmental: tuple[tuple[str, Any, Any], ...] = ()
    header_unclassified: tuple[str, ...] = ()
    fingerprints_compared: bool = False
    fingerprint_left: int | None = None
    fingerprint_right: int | None = None
    event_count_left: int = 0
    event_count_right: int = 0
    event_deltas: tuple[EventDelta, ...] = ()
    prefix_relation: bool = False

    @property
    def fingerprint_delta(self) -> bool:
        return (
            self.fingerprints_compared
            and self.fingerprint_left is not None
            and self.fingerprint_right is not None
            and self.fingerprint_left != self.fingerprint_right
        )

    @property
    def equal(self) -> bool:
        """Semantically equal: no header-semantic delta, no fingerprint
        delta, no event delta. Environmental deltas never count."""
        return (
            not self.header_semantic
            and not self.fingerprint_delta
            and not self.event_deltas
        )


def parse_log(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Read one canon log independently of core/: the header mapping +
    the event mappings, each line parsed with the stdlib json module
    (line endings and key order are parse-level, never semantic —
    CRLF/LF/CR and BOM tolerated). Raises DiffInputError on anything
    that is not the canonical shape: missing file, unreadable bytes, a
    first line that is not the header, an interior blank line, a
    non-object line."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise DiffInputError(f"{path}: unreadable ({exc})") from exc
    lines = text.splitlines()
    if not lines or not lines[0].strip():
        raise DiffInputError(f"{path}: empty log (no header line)")
    try:
        header = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise DiffInputError(f"{path}:1: header is not JSON ({exc})") from exc
    if not isinstance(header, dict) or header.get("header") is not True:
        raise DiffInputError(f"{path}:1: first line is not the log header")
    events: list[dict[str, Any]] = []
    for lineno, line in enumerate(lines[1:], start=2):
        if not line.strip():
            # one trailing blank after the last event is the writer's
            # own newline; an interior blank is corruption
            if lineno == len(lines):
                break
            raise DiffInputError(f"{path}:{lineno}: blank line inside the log")
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise DiffInputError(f"{path}:{lineno}: not JSON ({exc})") from exc
        if not isinstance(event, dict):
            raise DiffInputError(f"{path}:{lineno}: event line is not an object")
        events.append(event)
    return header, events


def _json_equal(left: Any, right: Any) -> bool:
    """Semantic equality of two parsed JSON values: booleans never equal
    numbers (different kinds — `true != 1`), ints and floats compare
    numerically (`4 == 4.0` — the same value), containers recurse in
    key-order-independent form."""
    if isinstance(left, bool) or isinstance(right, bool):
        return isinstance(left, bool) and isinstance(right, bool) and left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(
            _json_equal(left[k], right[k]) for k in left
        )
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(
            _json_equal(a, b) for a, b in zip(left, right, strict=True)
        )
    return type(left) is type(right) and left == right


def _deep_diff(left: Any, right: Any, prefix: str, out: list[str]) -> None:
    """Collect the differing field paths between two parsed values onto
    `out` (bounded by the caller)."""
    if _json_equal(left, right):
        return
    if isinstance(left, dict) and isinstance(right, dict):
        for key in sorted(set(left) | set(right)):
            if key not in left:
                out.append(f"{prefix}.{key}: absent != {right[key]!r}")
            elif key not in right:
                out.append(f"{prefix}.{key}: {left[key]!r} != absent")
            else:
                _deep_diff(left[key], right[key], f"{prefix}.{key}", out)
        return
    if isinstance(left, list) and isinstance(right, list):
        for i, (a, b) in enumerate(zip(left, right, strict=True)):
            _deep_diff(a, b, f"{prefix}[{i}]", out)
        if len(left) != len(right):
            out.append(f"{prefix}: list lengths {len(left)} != {len(right)}")
        return
    out.append(f"{prefix}: {left!r} != {right!r}")


def compare(
    left: Path,
    right: Path,
    fingerprint_left: int | None = None,
    fingerprint_right: int | None = None,
) -> SemanticDiff:
    """The semantic comparison of two logs (parse errors raise
    DiffInputError — loud, never a silent skip). Fingerprints are
    both-or-neither: the run-side RngBank draw counts join the verdict
    only when the caller supplies the pair."""
    if (fingerprint_left is None) != (fingerprint_right is None):
        raise DiffInputError(
            "fingerprints are both-or-neither — supply --fingerprint-left and "
            "--fingerprint-right together (a half-pair is a silent skip)"
        )
    header_l, events_l = parse_log(left)
    header_r, events_r = parse_log(right)

    known = set(SEMANTIC_HEADER_FIELDS) | set(ENVIRONMENTAL_HEADER_FIELDS)
    semantic: list[tuple[str, Any, Any]] = []
    environmental: list[tuple[str, Any, Any]] = []
    for field in SEMANTIC_HEADER_FIELDS:
        if field not in header_l or field not in header_r:
            raise DiffInputError(
                f"header lacks the semantic field {field!r} "
                f"({left}: {sorted(header_l)} / {right}: {sorted(header_r)})"
            )
        if not _json_equal(header_l[field], header_r[field]):
            semantic.append((field, header_l[field], header_r[field]))
    for field in ENVIRONMENTAL_HEADER_FIELDS:
        if field not in header_l or field not in header_r:
            raise DiffInputError(
                f"header lacks the environmental field {field!r} "
                f"({left}: {sorted(header_l)} / {right}: {sorted(header_r)})"
            )
        if not _json_equal(header_l[field], header_r[field]):
            environmental.append((field, header_l[field], header_r[field]))
    unclassified = tuple(
        sorted(
            (set(header_l) | set(header_r))
            - known
            - {"header"}
        )
    )

    deltas: list[EventDelta] = []
    for index in range(max(len(events_l), len(events_r))):
        if index >= len(events_r):
            deltas.append(
                EventDelta(
                    index=index,
                    context=str(events_l[index].get("id", "?")),
                    side="left",
                )
            )
            continue
        if index >= len(events_l):
            deltas.append(
                EventDelta(
                    index=index,
                    context=str(events_r[index].get("id", "?")),
                    side="right",
                )
            )
            continue
        ev_l, ev_r = events_l[index], events_r[index]
        if _json_equal(ev_l, ev_r):
            continue
        anchors = tuple(
            (name, ev_l.get(name), ev_r.get(name))
            for name in ANCHOR_FIELDS
            if not _json_equal(ev_l.get(name), ev_r.get(name))
        )
        paths: list[str] = []
        _deep_diff(ev_l, ev_r, "event", paths)
        deltas.append(
            EventDelta(
                index=index,
                context=str(ev_l.get("id", "?")),
                anchors=anchors,
                fields=tuple(paths[:MAX_FIELD_PATHS]),
            )
        )
    prefix = bool(deltas) and all(d.side for d in deltas) and not any(
        d.anchors or d.fields for d in deltas
    )

    return SemanticDiff(
        left=left,
        right=right,
        header_semantic=tuple(semantic),
        header_environmental=tuple(environmental),
        header_unclassified=unclassified,
        fingerprints_compared=fingerprint_left is not None,
        fingerprint_left=fingerprint_left,
        fingerprint_right=fingerprint_right,
        event_count_left=len(events_l),
        event_count_right=len(events_r),
        event_deltas=tuple(deltas[:MAX_EVENT_DELTAS]),
        prefix_relation=prefix,
    )


def _fmt(value: Any) -> str:
    return repr(value) if isinstance(value, str) else str(value)


def format_report(diff: SemanticDiff) -> str:
    """The human-readable report (stdout; the verdict line is the last)."""
    lines: list[str] = [f"semantic diff: {diff.left} vs {diff.right}"]
    for field, left, right in diff.header_semantic:
        lines.append(f"header: {field} {_fmt(left)} != {_fmt(right)} — semantic")
    if not diff.header_semantic:
        lines.append("header: schema_version/seed/pack equal")
    for field, left, right in diff.header_environmental:
        lines.append(
            f"environment (ignored by design, TEST_PLAN §1.4): {field} "
            f"{_fmt(left)} != {_fmt(right)}"
        )
    if diff.header_unclassified:
        lines.append(
            "unclassified header keys (not compared): "
            + ", ".join(diff.header_unclassified)
        )
    if not diff.fingerprints_compared:
        lines.append(
            "fingerprints: not compared (run-side RngBank values not supplied)"
        )
    elif diff.fingerprint_delta:
        lines.append(
            f"fingerprints: {diff.fingerprint_left} != {diff.fingerprint_right} "
            "— the substantive draw count diverged (latent RNG drift, RNG-1)"
        )
    else:
        lines.append(f"fingerprints: {diff.fingerprint_left} == {diff.fingerprint_right}")
    counts = (
        f"events: {diff.event_count_left} == {diff.event_count_right}"
        if diff.event_count_left == diff.event_count_right
        else f"events: {diff.event_count_left} != {diff.event_count_right}"
    )
    lines.append(counts)
    for delta in diff.event_deltas:
        where = f"event[{delta.index}]"
        if delta.context:
            where += f" (id={delta.context})"
        if delta.side:
            note = "present only in the left log" if delta.side == "left" else (
                "present only in the right log"
            )
            lines.append(f"{where}: {note}")
            continue
        parts = [
            f"{name} {_fmt(left)} != {_fmt(right)}"
            for name, left, right in delta.anchors
        ]
        headline = " · ".join(parts) if parts else "deep fields differ"
        lines.append(f"{where}: {headline}")
        lines.extend(f"  {path}" for path in delta.fields)
    if diff.prefix_relation:
        lines.append(
            "the shorter stream is a strict prefix of the longer — the "
            "divergence is append-only (a longer run of the same prefix)"
        )
    if diff.equal:
        lines.append(
            f"VERDICT: SEMANTICALLY EQUAL "
            f"({len(diff.header_environmental)} environmental difference(s) ignored)"
        )
    else:
        header_n = len(diff.header_semantic)
        fp_n = 1 if diff.fingerprint_delta else 0
        lines.append(
            f"VERDICT: SEMANTIC DELTA — header: {header_n}, fingerprint: {fp_n}, "
            f"events: {len(diff.event_deltas)}"
            + ("+" if len(diff.event_deltas) == MAX_EVENT_DELTAS else "")
            + " (SSI-N010: no semantic drift without delta)"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Semantic diff of two canon logs (ssi-7, TEST_PLAN §1.4)"
    )
    parser.add_argument("left", type=Path, help="the left log (.jsonl)")
    parser.add_argument("right", type=Path, help="the right log (.jsonl)")
    parser.add_argument(
        "--fingerprint-left",
        type=int,
        default=None,
        help="the left run's RngBank substantive draw count (both-or-neither)",
    )
    parser.add_argument(
        "--fingerprint-right",
        type=int,
        default=None,
        help="the right run's RngBank substantive draw count (both-or-neither)",
    )
    args = parser.parse_args(argv)
    try:
        diff = compare(
            args.left,
            args.right,
            fingerprint_left=args.fingerprint_left,
            fingerprint_right=args.fingerprint_right,
        )
    except DiffInputError as exc:
        print(f"semantic diff: INPUT ERROR — {exc}")
        return 2
    print(format_report(diff))
    return 0 if diff.equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
