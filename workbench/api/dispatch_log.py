"""The dispatch log (diaglog-1, iter-402 — WORKBENCH_APP_LAW §21's
redaction floor, not its full envelope).

ONE JSON line per `POST /op`: WHAT was dispatched and WHAT the dispatch
answered — `operation`, `operation_id`, `status`, `rejection`,
`error_type`, `elapsed_ms`. Request bodies, headers, tokens and
credentials never enter the record: the envelope's identity fields are
the observability, the payload is not (§21's redaction status).

Ownership: the LAUNCHER (the composition root) owns destination and
rotation — the LOGS path role and a bounded `RotatingFileHandler`; the
transport only EMITS through `record_dispatch`. Unconfigured, the
logger sits at its default level with no handler, so INFO records are
dropped and library/test use stays silent (stdout noise is absence of
observation, §21).

Boundedness: `max_bytes` per file and `backups` kept files are explicit
ceilings (a byte cap that rotates, never an unbounded append).
"""

from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

#: The one logger name the dispatch records ride.
LOGGER_NAME = "canonsim.dispatch"

#: The rotation ceilings — a declared bound, never an unbounded append.
DEFAULT_MAX_BYTES = 1_048_576
DEFAULT_BACKUPS = 3
DEFAULT_FILENAME = "gateway.log"

_LOGGER = logging.getLogger(LOGGER_NAME)
#: The handlers THIS module installed (a re-configuration replaces its
#: own set, never a foreign handler the embedding process owns).
_INSTALLED: list[logging.Handler] = []


def configure_dispatch_log(
    path: Path,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backups: int = DEFAULT_BACKUPS,
) -> Path:
    """Point the dispatch logger at `path` with bounded rotation.

    Idempotent: a second call replaces the handlers THIS module
    installed (the caller's other handlers are untouched) — the
    launcher's one call and a test's throwaway path both work. The
    parent directory is created; a creation failure raises loudly (the
    launcher decides whether serving without the log is acceptable —
    never a silent no-op).
    """
    if max_bytes <= 0 or backups < 1:
        raise ValueError(
            f"dispatch log: max_bytes must be positive and backups >= 1 "
            f"(got max_bytes={max_bytes}, backups={backups})"
        )
    for handler in list(_INSTALLED):
        _LOGGER.removeHandler(handler)
        handler.close()
    _INSTALLED.clear()
    path.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        path,
        maxBytes=max_bytes,
        backupCount=backups,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter("%(message)s"))
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)
    # The root's levels/handlers stay untouched: the dispatch log is an
    # explicit instrument, never a global logging configuration.
    _LOGGER.propagate = False
    _INSTALLED.append(handler)
    return path


def disable_dispatch_log() -> None:
    """Remove the handlers THIS module installed and restore the
    silent default — the inverse of `configure_dispatch_log` (an
    embedding process and a test's cleanup both need it; the root
    configuration stays untouched)."""
    for handler in list(_INSTALLED):
        _LOGGER.removeHandler(handler)
        handler.close()
    _INSTALLED.clear()
    _LOGGER.setLevel(logging.NOTSET)


def record_dispatch(
    *,
    operation: str,
    operation_id: str,
    status: str,
    rejection: str | None,
    error_type: str | None,
    elapsed_ms: float,
) -> None:
    """One dispatch's record — the identity fields only, never a
    payload. A disabled logger (unconfigured) returns before any
    formatting work (the silent-by-default law)."""
    if not _LOGGER.isEnabledFor(logging.INFO):
        return
    _LOGGER.info(
        json.dumps(
            {
                "operation": operation,
                "operation_id": operation_id,
                "status": status,
                "rejection": rejection,
                "error_type": error_type,
                "elapsed_ms": round(elapsed_ms, 3),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
