"""Append-only JSONL event log: the only canon-write path (INV-1, P1a).

Line 1 is the run header — no wall-clock anywhere (INV-2, D-004); its shape
is `docs/EVENT_SCHEMA.md` §1, enforced by `validate_header`. Every event
line is validated against `schemas/event.schema.json` via the stdlib
mini-validator *before* it is written (T0 by construction, KI#10/D-032).
Cause-chain integrity at write time: the first event of a run is the
run-start event and carries `cause: null`; every later event must chain to
an already-written event id. Ids are `ev_0000…` — monotonic, gap-free,
writer-assigned. `knowledge[].source` is derived (always the own event id;
L3 derive-never-store) and stamped by the writer, never hand-written.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, Literal

from core.ids import sequence_id
from core.schema import validate

__all__ = [
    "Channel",
    "EventDraft",
    "EventLogWriter",
    "EventRecord",
    "Fidelity",
    "IMPORTANCE_ORDER",
    "Importance",
    "KnowledgeRecord",
    "LoggedKnowledgeRecord",
    "LogError",
    "StateChange",
    "event_from_mapping",
    "next_log_path",
    "python_version",
    "read_log",
    "validate_header",
]

Channel = Literal["saw", "heard", "told", "inferred"]
Fidelity = Literal["exact", "partial", "vague"]
Importance = Literal["low", "medium", "high"]

# The single owner of the importance ordering (the `Importance` literal's
# order): the chronicle gate and the eventless-stretch metric both compare
# against it (D-024 — one owner, linked, never restated).
IMPORTANCE_ORDER: Final[tuple[str, ...]] = ("low", "medium", "high")

_EVENT_ID_PREFIX: Final = "ev"


class LogError(RuntimeError):
    """Log-format or cause-chain violation caught at write/read time."""


# -- DTOs ----------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class KnowledgeRecord:
    """Knowledge record as constructed by an emitter (EVENT_SCHEMA §3).

    `source` is not a field: it is always the owning event's id, stamped by
    the writer (L3 — derived, never hand-written).
    """

    who: str
    channel: Channel
    fidelity: Fidelity
    knows: str
    at: int


@dataclass(frozen=True, slots=True)
class LoggedKnowledgeRecord:
    """A knowledge record as it lives in the log line (with `source`)."""

    who: str
    channel: Channel
    fidelity: Fidelity
    knows: str
    at: int
    source: str


@dataclass(frozen=True, slots=True)
class StateChange:
    """One state delta; `irreversible` never reverts without a counter-event."""

    entity: str
    prop: str
    from_: Any
    to_: Any
    irreversible: bool = False


@dataclass(frozen=True, slots=True)
class EventDraft:
    """Event under construction: `id` and `knowledge[].source` are derived."""

    t: int
    type: str
    actor: str
    cause: str | None
    outcome: Mapping[str, Any]
    knowledge: tuple[KnowledgeRecord, ...] = ()
    state_changes: tuple[StateChange, ...] = ()
    hooks: tuple[str, ...] = ()
    importance: Importance = "low"
    provenance: Mapping[str, Any] = field(default_factory=dict)
    target: str | None = None


@dataclass(frozen=True, slots=True)
class EventRecord:
    """A logged event: exactly what one JSONL line parses back into."""

    id: str
    t: int
    type: str
    actor: str
    cause: str | None
    outcome: Mapping[str, Any]
    knowledge: tuple[LoggedKnowledgeRecord, ...]
    state_changes: tuple[StateChange, ...]
    hooks: tuple[str, ...]
    importance: Importance
    provenance: Mapping[str, Any]
    target: str | None


# -- serialization (field order per EVENT_SCHEMA.md §2-§4) ---------------


def _knowledge_to_mapping(record: LoggedKnowledgeRecord) -> dict[str, Any]:
    return {
        "who": record.who,
        "channel": record.channel,
        "fidelity": record.fidelity,
        "knows": record.knows,
        "at": record.at,
        "source": record.source,
    }


def _change_to_mapping(change: StateChange) -> dict[str, Any]:
    return {
        "entity": change.entity,
        "prop": change.prop,
        "from": change.from_,
        "to": change.to_,
        "irreversible": change.irreversible,
    }


def event_to_mapping(record: EventRecord) -> dict[str, Any]:
    """Serialize in the documented field order (deterministic bytes)."""
    data: dict[str, Any] = {
        "id": record.id,
        "t": record.t,
        "type": record.type,
        "actor": record.actor,
    }
    if record.target is not None:
        data["target"] = record.target
    data["cause"] = record.cause
    data["outcome"] = dict(record.outcome)
    data["knowledge"] = [_knowledge_to_mapping(k) for k in record.knowledge]
    data["state_changes"] = [_change_to_mapping(c) for c in record.state_changes]
    data["hooks"] = list(record.hooks)
    data["importance"] = record.importance
    data["provenance"] = dict(record.provenance)
    return data


def event_from_mapping(data: Mapping[str, Any]) -> EventRecord:
    """Build an EventRecord from a validated log-line mapping."""
    return EventRecord(
        id=data["id"],
        t=data["t"],
        type=data["type"],
        actor=data["actor"],
        cause=data["cause"],
        outcome=dict(data["outcome"]),
        knowledge=tuple(
            LoggedKnowledgeRecord(
                who=k["who"], channel=k["channel"], fidelity=k["fidelity"],
                knows=k["knows"], at=k["at"], source=k["source"],
            )
            for k in data["knowledge"]
        ),
        state_changes=tuple(
            StateChange(
                entity=c["entity"], prop=c["prop"], from_=c["from"],
                to_=c["to"], irreversible=c.get("irreversible", False),
            )
            for c in data["state_changes"]
        ),
        hooks=tuple(data["hooks"]),
        importance=data["importance"],
        provenance=dict(data["provenance"]),
        target=data.get("target"),
    )


# -- header (EVENT_SCHEMA.md §1: exact keys, no wall-clock) ---------------


HEADER_KEYS: Final = ("header", "schema_version", "seed", "python", "commit", "pack")


def validate_header(line: Mapping[str, Any]) -> None:
    """Header shape contract: exact key set (no timestamp can even appear)."""
    if tuple(sorted(line)) != tuple(sorted(HEADER_KEYS)):
        raise LogError(f"header keys must be exactly {list(HEADER_KEYS)}, got {sorted(line)}")
    if line["header"] is not True:
        raise LogError("header field 'header' must be true")
    for key in ("schema_version", "python", "commit", "pack"):
        if not isinstance(line[key], str):
            raise LogError(f"header field {key!r} must be a string")
    if not isinstance(line["seed"], int) or isinstance(line["seed"], bool):
        raise LogError("header field 'seed' must be an integer")


def python_version() -> str:
    """Runtime Python version for the header (same-environment determinism)."""
    info = sys.version_info
    return f"{info.major}.{info.minor}.{info.micro}"


def next_log_path(logs_dir: Path, seed: int) -> Path:
    """First free `run_<seed>_<n>.jsonl` path inside `logs_dir` (§1 pattern).

    Never returns an existing path (KI#14): counting files breaks after a
    middle delete — `len(existing)` would name a live log, and the writer's
    `"w"` mode would silently truncate it. The first free slot wins, so a
    deleted middle file is refilled instead.
    """
    taken: set[str] = set()
    if logs_dir.is_dir():
        taken = {path.name for path in logs_dir.glob(f"run_{seed}_*.jsonl")}
    n = 0
    while f"run_{seed}_{n}.jsonl" in taken:
        n += 1
    return logs_dir / f"run_{seed}_{n}.jsonl"


# -- the writer (the only canon-write path) -------------------------------


class EventLogWriter:
    """Append-only JSONL writer with write-time integrity checks.

    `schema` is the parsed `schemas/event.schema.json`; the header's
    `schema_version` is derived from its `$id` — the schema file is the
    single version owner (D-010).
    """

    def __init__(self, path: Path, schema: Mapping[str, Any]) -> None:
        self._schema = schema
        self._schema_version = self._extract_schema_version(schema)
        self._path = path
        self._fh = path.open("w", encoding="utf-8")
        self._header_written = False
        self._count = 0
        self._last_tick: int | None = None
        self._written_ids: set[str] = set()
        self._last_id: str | None = None

    @staticmethod
    def _extract_schema_version(schema: Mapping[str, Any]) -> str:
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or "/" not in schema_id:
            raise LogError(f"schema $id must look like 'canonsim/event/<ver>', got {schema_id!r}")
        return schema_id.rsplit("/", 1)[-1]

    @property
    def path(self) -> Path:
        return self._path

    @property
    def event_count(self) -> int:
        return self._count

    @property
    def last_id(self) -> str | None:
        return self._last_id

    def __enter__(self) -> EventLogWriter:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        if not self._fh.closed:
            self._fh.flush()
            self._fh.close()

    def write_header(self, seed: int, commit: str, pack: str) -> None:
        """Write line 1. Must happen before any event; flushed immediately."""
        if self._header_written:
            raise LogError("header already written")
        if self._count:
            raise LogError("header must precede all events")
        header = {
            "header": True,
            "schema_version": self._schema_version,
            "seed": seed,
            "python": python_version(),
            "commit": commit,
            "pack": pack,
        }
        validate_header(header)
        self._fh.write(json.dumps(header) + "\n")
        self._fh.flush()
        self._header_written = True

    def append(self, draft: EventDraft) -> EventRecord:
        """Validate, assign id + knowledge sources, append, return the record."""
        if not self._header_written:
            raise LogError("header must be written before events")
        event_id = sequence_id(_EVENT_ID_PREFIX, self._count)
        if self._count == 0:
            if draft.cause is not None:
                raise LogError("the first event of a run is the run-start: cause must be null")
        else:
            if draft.cause is None:
                raise LogError("only the run-start event may carry cause null")
            if draft.cause not in self._written_ids:
                raise LogError(f"cause {draft.cause!r} references no written event")
        if self._last_tick is not None and draft.t < self._last_tick:
            raise LogError(f"tick regression in log: {self._last_tick} -> {draft.t}")

        record = EventRecord(
            id=event_id,
            t=draft.t,
            type=draft.type,
            actor=draft.actor,
            cause=draft.cause,
            outcome=dict(draft.outcome),
            knowledge=tuple(
                LoggedKnowledgeRecord(
                    who=k.who, channel=k.channel, fidelity=k.fidelity,
                    knows=k.knows, at=k.at, source=event_id,
                )
                for k in draft.knowledge
            ),
            state_changes=draft.state_changes,
            hooks=draft.hooks,
            importance=draft.importance,
            provenance=dict(draft.provenance),
            target=draft.target,
        )
        line = event_to_mapping(record)
        validate(line, self._schema)

        self._fh.write(json.dumps(line) + "\n")
        self._fh.flush()
        self._count += 1
        self._last_tick = draft.t
        self._written_ids.add(event_id)
        self._last_id = event_id
        return record


# -- the reader ------------------------------------------------------------


def read_log(
    path: Path, schema: Mapping[str, Any]
) -> tuple[dict[str, Any], list[EventRecord]]:
    """Read a log: validate the header shape and every event line (T0/T2).

    The writer is the enforcement point for derived fields (ids, knowledge
    sources); the reader validates each line against the schema and hands
    back typed records.
    """
    header: dict[str, Any] | None = None
    events: list[EventRecord] = []
    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            if not line.strip():
                raise LogError(f"{path}:{lineno}: blank line in log")
            data = json.loads(line)
            if lineno == 1:
                validate_header(data)
                header = dict(data)
                continue
            try:
                validate(data, schema)
            except ValueError as exc:
                raise LogError(f"{path}:{lineno}: schema validation failed: {exc}") from exc
            events.append(event_from_mapping(data))
    if header is None:
        raise LogError(f"{path}: empty log (no header)")
    return header, events


def log_lines(events: Sequence[EventRecord]) -> list[str]:
    """Serialize records to log lines (test helper; same bytes as the writer)."""
    return [json.dumps(event_to_mapping(e)) for e in events]
