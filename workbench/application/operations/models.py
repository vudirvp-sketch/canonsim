"""The model discovery family (wb-5, the app spec §§9/20 — the
family's fifth row).

The law: **file exists ≠ valid ≠ selected ≠ loading ≠ loaded ≠
active** (§20) — wb-5 lands the DISCOVERY half honestly: `discover`
+ `inspect` over the §16 MODELS_ASSETS role, the §9 identity closure
per file, and the strong content identity "computed when needed"
(§20). The select/loading/active half arrives with the backend row
(app §32 step 7 — the admission law: no loading machinery without
the backend that loads). Every discovered record therefore names
state DISCOVERED — the only state this half can truthfully hold.

Identity discipline (§9, over the wb-3 skeleton):

```text
logical_name + content identity (sha256) = the model's material
identity ; size/mtime = the cheap scan fingerprint (a routine-
refresh SCREEN, "not a correctness identity") ; location = a path,
never an identity
```

The §9 laws made executable: same path + new bytes → a NEW content
identity (inspect recomputes — the digest is a pure function of the
bytes, never cached across a fingerprint change); same bytes → the
same identity (stability); "same revision + new bytes → identity
mismatch; never silently reuse" — the artifact side owns that (an
artifact frozen with a model identity never re-derives it, wb-3's
immutable freeze).

The long-running arm (§20: "for large assets ... strong identity is
computed when needed"): `model_digest_work` — the chunked sha256
computation AS A RUN (the run registry's cancellation/deadline
checkpoints between chunks, the §10 artifact frozen before the first
byte is read, the result recorded back into the registry as the
run's effect). This is the run family's one real work kind in wb-5 —
the consumer that makes the execution substrate land as machinery in
use, not machinery awaiting a demo.
"""

from __future__ import annotations

import hashlib
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from workbench.application.operations.execution import WorkContext

#: The discovery state a wb-5 record can hold (§20's vocabulary —
#: the loading states belong to the backend row; DISCOVERED is the
#: only honest member here).
DISCOVERY_STATE = "DISCOVERED"

#: The §16 outcome names discovery can observe (the shallow subset —
#: MISSING and the slot-CORRUPT form; the write-probe states belong
#: to the startup/recovery path that owns writes).
_DIRECTORY_MISSING = "MISSING"
_DIRECTORY_CORRUPT = "CORRUPT"
_DIRECTORY_OK = "OK"

#: The digest work's chunk size — the checkpoint cadence (one
#: `WorkContext.check()` per chunk; small enough to bound the
#: cancellation latency, large enough to keep the syscall count
#: sane on real model files).
DEFAULT_CHUNK_BYTES = 1024 * 1024


class ModelRegistryError(ValueError):
    """A model-registry contract violation (LOUD — an unknown model,
    a corrupt slot; never a silent empty)."""


@dataclass(frozen=True)
class _ModelEntry:
    """The registry-private discovery record (the read view is the
    `document()` mapping)."""

    logical_name: str
    location: str
    size_bytes: int
    mtime_ns: int
    content_digest: str | None = None


class ModelRegistry:
    """The in-memory model discovery registry over ONE root (the
    §16 MODELS_ASSETS path, supplied by the composition root).

    The registry is read-through: `discover()` re-scans (the §20
    routine refresh — the cheap fingerprint per file), `inspect()`
    recomputes the strong identity FRESH (the §9 correctness identity
    is never served from a cache the mtime screen cannot validate),
    and the digest run's completion records the strong identity it
    computed (the run's own effect — `record_strong_identity`).
    """

    def __init__(self, models_root: Path) -> None:
        if not isinstance(models_root, Path):
            raise ModelRegistryError(
                "models_root must be a pathlib.Path "
                f"(got {type(models_root).__name__})"
            )
        if not models_root.is_absolute():
            raise ModelRegistryError(
                f"models_root {str(models_root)!r} is relative — the "
                ".git/CWD-independence law (app §16) requires an explicit "
                "absolute root from the composition root"
            )
        self._root = models_root
        self._entries: dict[str, _ModelEntry] = {}

    @property
    def root(self) -> Path:
        return self._root

    def discover(self) -> dict[str, object]:
        """The §20 scan (`model.list`'s body): classify the slot
        (MISSING truthfully empty, CORRUPT loudly rejected by the
        handler), then the direct-child files sorted by logical_name —
        each carrying the cheap fingerprint and the strong identity
        when one has been computed (by inspect or a digest run)."""
        if not self._root.exists():
            return {
                "directory_state": _DIRECTORY_MISSING,
                "models": [],
            }
        if not self._root.is_dir():
            raise ModelRegistryError(
                f"the MODELS_ASSETS slot {str(self._root)!r} exists but is "
                "not a directory (§16's shallow CORRUPT form)"
            )
        scanned: dict[str, _ModelEntry] = {}
        for child in sorted(self._root.iterdir(), key=lambda p: p.name):
            if not child.is_file():
                continue
            stat = child.stat()
            name = child.name
            previous = self._entries.get(name)
            if (
                previous is not None
                and previous.size_bytes == stat.st_size
                and previous.mtime_ns == stat.st_mtime_ns
            ):
                # the §20 screen: the cheap fingerprint is unchanged —
                # keep the previously computed strong identity (if
                # any); the screen is a refresh heuristic, never the
                # correctness identity (inspect recomputes).
                scanned[name] = previous
                continue
            scanned[name] = _ModelEntry(
                logical_name=name,
                location=str(child),
                size_bytes=stat.st_size,
                mtime_ns=stat.st_mtime_ns,
                content_digest=None,
            )
        self._entries = scanned
        return {
            "directory_state": _DIRECTORY_OK,
            "models": [self._document(entry) for entry in self._entries.values()],
        }

    def inspect(self, logical_name: str) -> dict[str, object]:
        """The strong identity computed fresh (§9's correctness
        identity — the sha256 of the bytes, never a cached value):
        the whole file, one pass, returned AND recorded."""
        path = self._resolve(logical_name)
        digest = _hash_file(path, chunk_bytes=DEFAULT_CHUNK_BYTES)
        stat = path.stat()
        entry = _ModelEntry(
            logical_name=logical_name,
            location=str(path),
            size_bytes=stat.st_size,
            mtime_ns=stat.st_mtime_ns,
            content_digest=digest,
        )
        self._entries[logical_name] = entry
        return self._document(entry)

    def record_strong_identity(
        self, logical_name: str, digest: str, size_bytes: int, mtime_ns: int
    ) -> None:
        """The digest run's effect surface: the strong identity a run
        computed, recorded under its observed fingerprint. The run's
        artifact was frozen BEFORE this write (§10 — the composition
        admits first, the work effects after)."""
        if not digest:
            raise ModelRegistryError("record_strong_identity: empty digest")
        path = self._resolve(logical_name)
        self._entries[logical_name] = _ModelEntry(
            logical_name=logical_name,
            location=str(path),
            size_bytes=size_bytes,
            mtime_ns=mtime_ns,
            content_digest=digest,
        )

    def resolve(self, logical_name: str) -> Path:
        """The model's location (§9: a path, never an identity) — the
        digest work's target."""
        return self._resolve(logical_name)

    def _resolve(self, logical_name: str) -> Path:
        """Resolve one logical name to its file, the honest way: the
        name must be a current discovery entry (a vanished file is a
        LOUD unknown-model error, never a stale path) and the file
        must still exist at that location."""
        if (
            not isinstance(logical_name, str)
            or not logical_name
            or os.sep in logical_name
            or (os.altsep and os.altsep in logical_name)
            or logical_name in (".", "..")
        ):
            raise ModelRegistryError(
                f"logical_name {logical_name!r}: a plain file name "
                "(no path separators, never '.'/'..')"
            )
        if logical_name not in self._entries:
            raise ModelRegistryError(
                f"model {logical_name!r}: not discovered — model.list "
                "first (discovery is the §20 entry gate)"
            )
        path = self._root / logical_name
        if not path.is_file():
            raise ModelRegistryError(
                f"model {logical_name!r}: vanished from "
                f"{str(self._root)!r} since discovery"
            )
        return path

    def _document(self, entry: _ModelEntry) -> dict[str, object]:
        return {
            "logical_name": entry.logical_name,
            "location": entry.location,
            "size_bytes": entry.size_bytes,
            "mtime_ns": entry.mtime_ns,
            "content_digest": entry.content_digest,
            "state": DISCOVERY_STATE,
        }


def _hash_file(path: Path, chunk_bytes: int) -> str:
    """The chunked sha256 (the shared strong-identity body: inspect's
    synchronous pass and the digest run's cancellable pass both end
    here — one hash law, two call shapes)."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_bytes)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def digest_work(
    context: WorkContext, registry: ModelRegistry, logical_name: str
) -> Mapping[str, object]:
    """The run family's one real work kind (§20's long-running arm):
    the chunked strong-identity computation with the §12 checkpoints
    between chunks — the §10 artifact was frozen before this function
    exists, the cancellation and the absolute deadline are observed
    cooperatively, and the computed identity is recorded into the
    registry as the run's effect."""
    path = registry.resolve(logical_name)
    stat = path.stat()
    hasher = hashlib.sha256()
    chunks = 0
    with path.open("rb") as handle:
        while True:
            context.check()  # §12: the cancellation + absolute-deadline checkpoint
            chunk = handle.read(DEFAULT_CHUNK_BYTES)
            if not chunk:
                break
            hasher.update(chunk)
            chunks += 1
    digest = hasher.hexdigest()
    registry.record_strong_identity(
        logical_name=logical_name,
        digest=digest,
        size_bytes=stat.st_size,
        mtime_ns=stat.st_mtime_ns,
    )
    return {
        "chunks": chunks,
        "content_digest": digest,
        "logical_name": logical_name,
        "size_bytes": stat.st_size,
    }
