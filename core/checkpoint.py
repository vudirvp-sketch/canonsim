"""Fold checkpoints (depth-4, phase 5; `docs/blueprint/phases.md` §5).

The projection fold is the replay cost: `fold(log)` pays O(N) on every
replay/branch, which is the phase-5 long-history price once pre-PC
worldgen history lands (depth-5). A fold-checkpoint bounds it: a
snapshot of the projection at an event-index offset, so replay restarts
at `snapshot + tail replay` instead of a full refold (rollback =
snapshot + tail replay, `phases.md` §5).

The artifact laws (the SQLite-index law, INV-1/INV-5, grown from the
chronicler family — iter-64's derived-artifact pattern):

- **Derived, never truth.** A checkpoint is a pure function of
  (log prefix, pack initial projection). It writes NOTHING to the log —
  the integrity anchor is never an event in the truth (intake-4: a
  snapshot-anchor event in the canon log was proposed and refused).
  Committed? Never: the artifacts live under `output/` (gitignored).
- **Byte-deterministic serialization.** One canonical form for the
  projection (`canonical_state_bytes` — compact JSON, sorted keys); the
  sha256 digest over the artifact bytes is the integrity anchor, the
  `stable_hash` family's hashlib (INV-2's spirit: same inputs, same
  bytes, any process).
- **Verified by re-fold.** `verify`/`verify_all` re-fold the prefix and
  byte-compare — a snapshot that drifted from its log fails loudly.
- **The anchor lives in the index, not in the artifact.** The derived
  index (`index.json` + `CheckpointRecord`) carries each snapshot's
  sha256 plus the folded prefix's own sha256 (`prefix_digest` — the
  first `1 + offset` log lines: the log only grows (INV-5), so the
  prefix digest is append-stable and the checkpoint stays bound to its
  log as the run continues).

The offset semantics: `events[:offset]` is folded INTO the snapshot,
`events[offset:]` is the tail. Ids are gap-free writer-assigned
(`core/ids.py`), so offset K names the prefix ending at `ev_{K-1:04d}`.

Not here (owner-gated, `phases.md` §7): the resume door — opening a
live session over an existing log. Checkpoints serve the read/replay
side only; the runtime keeps its incremental projection (STATE-1,
D-003/D-023 — `fold` is never the startup hot path).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.fold import Projection, apply_event, fold
from core.log import EventRecord

__all__ = [
    "INDEX_NAME",
    "CheckpointError",
    "CheckpointIndex",
    "CheckpointRecord",
    "FoldCheckpoint",
    "canonical_state_bytes",
    "checkpoint_path",
    "load_checkpoint",
    "prefix_digest",
    "read_index",
    "save_checkpoint",
    "sha256_hex",
    "verify",
    "verify_all",
    "write_index",
]

INDEX_NAME = "index.json"
_ENVELOPE_KEYS = frozenset({"offset", "state"})
_INDEX_KEYS = frozenset({"checkpoints", "log", "pack"})
_RECORD_KEYS = frozenset({"offset", "prefix_sha256", "snapshot_sha256"})


class CheckpointError(RuntimeError):
    """Checkpoint integrity failure (shape, anchor, re-fold, bounds)."""


def sha256_hex(data: bytes) -> str:
    """The digest form used everywhere here: sha256, lowercase hex."""
    return hashlib.sha256(data).hexdigest()


def canonical_state_bytes(state: Projection) -> bytes:
    """THE byte-deterministic serialization of a projection (single owner).

    Compact JSON, keys sorted (iteration order never leaks — INV-2), so
    the same state serializes to the same bytes in any process and any
    `PYTHONHASHSEED`. Values are the pack's JSON scalars; floats never
    enter the canonical path (the phase-5 geometry discipline,
    `phases.md` §5).
    """
    return json.dumps(state, sort_keys=True, separators=(",", ":")).encode("utf-8")


def checkpoint_path(out_dir: Path, offset: int) -> Path:
    """The artifact file for an offset: `checkpoint_<offset:06d>.json`."""
    return out_dir / f"checkpoint_{offset:06d}.json"


@dataclass(frozen=True, slots=True)
class FoldCheckpoint:
    """One derived snapshot: the projection after folding `events[:offset]`.

    `state` is the snapshot dict (copied at construction — the live
    projection keeps mutating; the checkpoint never does). The digest
    anchors the ARTIFACT bytes (offset + state envelope); the index
    carries it, `load_checkpoint` checks it.
    """

    offset: int
    state: Projection

    def to_bytes(self) -> bytes:
        """The artifact bytes: the envelope `{"offset", "state"}`, canonical
        form, file-shaped with one trailing newline."""
        envelope = {"offset": self.offset, "state": self.state}
        return json.dumps(envelope, sort_keys=True, separators=(",", ":")
                          ).encode("utf-8") + b"\n"

    @property
    def digest(self) -> str:
        """sha256 over the artifact bytes — the integrity anchor value."""
        return sha256_hex(self.to_bytes())

    def record(self, prefix_sha256: str) -> CheckpointRecord:
        """The derived-index row for this checkpoint (given the folded
        prefix's digest — `prefix_digest` owns its computation)."""
        return CheckpointRecord(
            offset=self.offset,
            prefix_sha256=prefix_sha256,
            snapshot_sha256=self.digest,
        )

    def restore(self, events: Sequence[EventRecord]) -> Projection:
        """Rollback = snapshot + tail replay (`phases.md` §5): apply
        `events[offset:]` onto a copy of the snapshot. A snapshot that
        disagrees with the log's true state at the offset goes loud on
        the first tail event that touches the diverged prop
        (`apply_event`'s from_-check, INV-1's own net); the STRONG check
        is `verify`'s re-fold. Never mutates the snapshot.
        """
        if self.offset > len(events):
            raise CheckpointError(
                f"checkpoint offset {self.offset} exceeds the log's "
                f"{len(events)} events — a truncated log cannot replay "
                f"the checkpointed tail"
            )
        state = {entity: dict(props) for entity, props in self.state.items()}
        for event in events[self.offset:]:
            apply_event(state, event)
        return state

    @classmethod
    def from_state(cls, state: Projection, offset: int) -> FoldCheckpoint:
        """Snapshot a LIVE state at event count `offset` (the incremental
        door — a deep copy, no fold: the runtime's own projection, or an
        offline builder's running fold, hands itself in)."""
        _require_offset(offset)
        return cls(
            offset=offset,
            state={entity: dict(props) for entity, props in state.items()},
        )

    @classmethod
    def from_events(
        cls, events: Sequence[EventRecord], initial: Projection, offset: int
    ) -> FoldCheckpoint:
        """The offline build path over a read log: fold `events[:offset]`
        over the pack-seeded initial projection (the T2 truth path —
        never the runtime hot path, D-003/D-023)."""
        _require_offset(offset)
        if offset > len(events):
            raise CheckpointError(
                f"offset {offset} exceeds the log's {len(events)} events"
            )
        return cls(offset=offset, state=fold(events[:offset], initial))

    @classmethod
    def from_bytes(cls, data: bytes) -> FoldCheckpoint:
        """Parse the artifact bytes back (loud on any shape drift)."""
        try:
            parsed = json.loads(data)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise CheckpointError(f"artifact bytes are not JSON: {exc}") from exc
        if not isinstance(parsed, dict) or set(parsed) != _ENVELOPE_KEYS:
            raise CheckpointError(
                f"artifact envelope keys must be {sorted(_ENVELOPE_KEYS)}, "
                f"got {sorted(parsed) if isinstance(parsed, dict) else type(parsed)}"
            )
        offset = parsed["offset"]
        state = parsed["state"]
        if not isinstance(offset, int) or isinstance(offset, bool):
            raise CheckpointError(f"artifact offset must be an int, got {offset!r}")
        _require_offset(offset)
        if not isinstance(state, dict) or not all(
            isinstance(props, dict) for props in state.values()
        ):
            raise CheckpointError(
                "artifact state must be a mapping of entity -> {prop: value}"
            )
        return cls(offset=offset, state=state)


@dataclass(frozen=True, slots=True)
class CheckpointRecord:
    """One derived-index record — the integrity anchor row (intake-4):
    the snapshot's sha256 (the artifact bytes) and the folded log
    prefix's sha256 (append-stable). The anchor lives HERE and in
    `index.json`, never in the log."""

    offset: int
    prefix_sha256: str
    snapshot_sha256: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> CheckpointRecord:
        if not isinstance(data, Mapping) or set(data) != _RECORD_KEYS:
            raise CheckpointError(
                f"index record keys must be {sorted(_RECORD_KEYS)}, got "
                f"{sorted(data) if isinstance(data, Mapping) else data!r}"
            )
        offset = data["offset"]
        if not isinstance(offset, int) or isinstance(offset, bool):
            raise CheckpointError(f"index record offset must be an int, got {offset!r}")
        _require_offset(offset)
        prefix_sha, snapshot_sha = data["prefix_sha256"], data["snapshot_sha256"]
        if not _is_sha256_hex(prefix_sha) or not _is_sha256_hex(snapshot_sha):
            raise CheckpointError(
                "index record digests must be sha256 hex (64 lowercase chars), "
                f"got prefix {prefix_sha!r}, snapshot {snapshot_sha!r}"
            )
        return cls(offset=offset, prefix_sha256=prefix_sha, snapshot_sha256=snapshot_sha)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "offset": self.offset,
            "prefix_sha256": self.prefix_sha256,
            "snapshot_sha256": self.snapshot_sha256,
        }


@dataclass(frozen=True, slots=True)
class CheckpointIndex:
    """The derived index document: which log, which pack seeded the fold,
    and the anchor records — sorted by offset (the writer's law; the
    reader rejects any other order — a hand-edited index is loud)."""

    log: str
    pack: str
    records: tuple[CheckpointRecord, ...]

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> CheckpointIndex:
        if not isinstance(data, Mapping) or set(data) != _INDEX_KEYS:
            raise CheckpointError(
                f"index keys must be {sorted(_INDEX_KEYS)}, got "
                f"{sorted(data) if isinstance(data, Mapping) else data!r}"
            )
        raw = data["checkpoints"]
        if not isinstance(raw, list):
            raise CheckpointError("index 'checkpoints' must be a list")
        records = tuple(CheckpointRecord.from_mapping(r) for r in raw)
        offsets = [r.offset for r in records]
        if offsets != sorted(set(offsets)):
            raise CheckpointError(
                "index records must be sorted by offset, strictly "
                f"increasing, no duplicates — got {offsets}"
            )
        if not isinstance(data["log"], str) or not isinstance(data["pack"], str):
            raise CheckpointError("index 'log' and 'pack' must be strings")
        return cls(log=data["log"], pack=data["pack"], records=records)


# -- the re-fold law ----------------------------------------------------------


def verify(
    checkpoint: FoldCheckpoint,
    events: Sequence[EventRecord],
    initial: Projection,
) -> None:
    """The re-fold law (phases.md §5 / intake-4): the snapshot must equal
    an independent re-fold of `events[:offset]` over `initial`,
    byte-for-byte. Raises CheckpointError on any drift — an edited
    snapshot, a wrong offset, or a log that is not the one folded."""
    if not 0 <= checkpoint.offset <= len(events):
        raise CheckpointError(
            f"checkpoint offset {checkpoint.offset} out of bounds for a "
            f"{len(events)}-event log"
        )
    refolded = fold(events[: checkpoint.offset], initial)
    if canonical_state_bytes(refolded) != canonical_state_bytes(checkpoint.state):
        raise CheckpointError(
            f"checkpoint at offset {checkpoint.offset} does not match a "
            f"re-fold of its prefix — the snapshot or the log drifted"
        )


def verify_all(
    checkpoints: Iterable[FoldCheckpoint],
    events: Sequence[EventRecord],
    initial: Projection,
) -> None:
    """The batch re-fold: ONE incremental pass over the events, comparing
    every checkpoint's canonical bytes at its offset — O(N + states),
    never O(N x checkpoints). Each checkpoint is verified exactly as
    `verify` would (the same law, the scalable shape)."""
    by_offset: dict[int, FoldCheckpoint] = {}
    for checkpoint in checkpoints:
        if checkpoint.offset in by_offset:
            raise CheckpointError(f"duplicate checkpoint offset {checkpoint.offset}")
        if not 0 <= checkpoint.offset <= len(events):
            raise CheckpointError(
                f"checkpoint offset {checkpoint.offset} out of bounds for a "
                f"{len(events)}-event log"
            )
        by_offset[checkpoint.offset] = checkpoint
    state = {entity: dict(props) for entity, props in initial.items()}
    if 0 in by_offset:
        _compare_or_raise(0, by_offset[0], state)
    for count, event in enumerate(events, start=1):
        apply_event(state, event)
        if count in by_offset:
            _compare_or_raise(count, by_offset[count], state)


def _compare_or_raise(offset: int, checkpoint: FoldCheckpoint, state: Projection) -> None:
    if canonical_state_bytes(state) != canonical_state_bytes(checkpoint.state):
        raise CheckpointError(
            f"checkpoint at offset {offset} does not match a re-fold of its "
            f"prefix — the snapshot or the log drifted"
        )


# -- the log-prefix identity ---------------------------------------------------


def prefix_digest(log: Path, offset: int) -> str:
    """sha256 over the log's first `1 + offset` lines (the run header + the
    folded events) — the append-stable identity of the checkpointed
    prefix. The log only grows (INV-5), so this digest never changes as
    the run continues; a different log, or a prefix that was never this
    log's, gives a different digest. Streams: never loads the log whole
    (token hygiene). Loud when the log holds fewer lines than the offset
    claims (a truncated log is a lie about its prefix, the count-gate
    spirit). The log must be read-validated first (`core.log.read_log`)."""
    _require_offset(offset)
    digest = hashlib.sha256()
    lines = 0
    with log.open("rb") as fh:
        for line in fh:
            lines += 1
            if lines > offset + 1:
                break
            digest.update(line)
    if lines < offset + 1:
        raise CheckpointError(
            f"{log}: holds {lines} lines but the prefix at offset {offset} "
            f"needs {offset + 1} (header + events) — a truncated log"
        )
    return digest.hexdigest()


# -- the artifact I/O (the chronicler family's file shapes) -------------------


def save_checkpoint(
    checkpoint: FoldCheckpoint, out_dir: Path, prefix_sha256: str
) -> CheckpointRecord:
    """Write the artifact file; return the anchor record (the index row).
    Callers verify BEFORE saving — an unverified checkpoint must never
    reach disk (the count-gate spirit: nothing written on integrity
    failure)."""
    if not _is_sha256_hex(prefix_sha256):
        raise CheckpointError(f"prefix_sha256 must be sha256 hex, got {prefix_sha256!r}")
    out_dir.mkdir(parents=True, exist_ok=True)
    data = checkpoint.to_bytes()
    checkpoint_path(out_dir, checkpoint.offset).write_bytes(data)
    return checkpoint.record(prefix_sha256)


def write_index(index: CheckpointIndex, out_dir: Path) -> Path:
    """Write `index.json` — byte-deterministic (the manifest law:
    content-derived only, sorted keys, no wall-clock, no absolute
    paths). Same inputs, same bytes, any process."""
    data = {
        "log": index.log,
        "pack": index.pack,
        "checkpoints": [r.to_mapping() for r in index.records],
    }
    path = out_dir / INDEX_NAME
    path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path


def read_index(out_dir: Path) -> CheckpointIndex:
    """Parse `index.json` (loud on any drift: wrong keys, unsorted
    offsets, malformed digests)."""
    path = out_dir / INDEX_NAME
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckpointError(f"{path}: cannot read the checkpoint index: {exc}") from exc
    return CheckpointIndex.from_mapping(data)


def load_checkpoint(record: CheckpointRecord, out_dir: Path) -> FoldCheckpoint:
    """Read an artifact back, anchor-checked: the file's sha256 must equal
    the record's `snapshot_sha256` (an edited or corrupted artifact is
    loud — the anchor's teeth), and the envelope's offset must agree
    with the record. The PREFIX digest is checked by the caller against
    the log (`prefix_digest`), not here — this door owns the artifact
    bytes only."""
    path = checkpoint_path(out_dir, record.offset)
    if not path.is_file():
        raise CheckpointError(f"{path}: checkpoint artifact missing")
    data = path.read_bytes()
    digest = sha256_hex(data)
    if digest != record.snapshot_sha256:
        raise CheckpointError(
            f"{path}: anchor mismatch — index records sha256 "
            f"{record.snapshot_sha256} but the file digests to {digest} "
            f"(the artifact was edited or corrupted)"
        )
    checkpoint = FoldCheckpoint.from_bytes(data)
    if checkpoint.offset != record.offset:
        raise CheckpointError(
            f"{path}: envelope offset {checkpoint.offset} disagrees with the "
            f"index record offset {record.offset}"
        )
    return checkpoint


# -- internals -----------------------------------------------------------------


def _require_offset(offset: int) -> None:
    if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
        raise CheckpointError(f"offsets are non-negative ints, got {offset!r}")


def _is_sha256_hex(text: object) -> bool:
    return (
        isinstance(text, str)
        and len(text) == 64
        and all(c in "0123456789abcdef" for c in text)
    )
