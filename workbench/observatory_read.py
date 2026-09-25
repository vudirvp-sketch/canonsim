"""The Observatory read model (obs-2 — the READ-side seam into the
canonical backend; FRONTEND_UIUX_LAW §25's P1 continuation, the law's
own implementation invariant: canonical/backend state → typed read
model → UI).

What this is: the bounded, deterministic projection of the canonical
JSONL log (INV-1 — the append-only truth) the Observatory surface
consumes. It sits beside ``workbench/scene_build.py`` — the same
read-side edge wb-1 established over ``core.log.read_log`` (the
workbench reads CanonSim's READ products; it never writes, never
re-interprets, never becomes a second authority — the LAW's
invariants 1/2).

The application-operations package stays CanonSim-free (its own
dependency envelope): this module is the seam's one home, and the
operations layer (``workbench/application/operations/observatory.py``)
reaches the canonical log ONLY through it.

Boundedness (LAW §39 — the frontend consumes bounded read models; it
must never materialise an entire analytical population):

```text
list_runs(runs_root)      — the discovery scan: per *.jsonl run the
                            parsed header or the honest degradation
                            (header=None + the observed error — a
                            corrupt first line never fails the whole
                            listing, LAW §16's distinct states), sorted
                            by name, content truths only (no mtime —
                            no wall-clock anywhere, INV-2's spirit).

read_window(runs_root, schema, run, after, limit)
                          — ONE run's bounded event window: the full
                            log validated line by line (T0), then cut
                            AFTER the cursor event id (the semantic
                            identity, LAW §6.2 — never a row index).
                            limit defaults to DEFAULT_WINDOW (50),
                            capped at MAX_WINDOW (200). next_after is
                            the window's last event id when more
                            remain, else None.
```

Authority axis (LAW §14): every event in the committed log is
CANONICAL — the log writer is the only canon-write path (INV-1), so
the row's authority is the truth, never a per-row guess. The
OBSERVED/DERIVED/UNKNOWN members become reachable when the
perception/knowledge views land (their own rows, never fabricated
here).

Every domain violation raises ``ObservatoryReadError`` (the reason
rides the message; the operations layer translates it to the
gateway's DOMAIN_REJECTED — NOT_SENT, never a §12.1 outcome):
unknown run (NO MATCH), stale cursor, corrupt log, duplicate event
ids, malformed run stem, bad limit. NO DATA (the runs root holds no
runs) stays the listing's own honest answer.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

from core.log import LogError, read_log, validate_header

#: The boundedness law's declared ceiling (LAW §39 — the window the
#: UI may request; the default keeps a page at 50 rows, the cap 200
#: is the hard ceiling any single read may return).
DEFAULT_WINDOW = 50
MAX_WINDOW = 200

#: The reading profile the canonical log carries (the observation
#: profile vocabulary's canon member — the only honest value for a
#: direct log read; the perception/assurance/debug profiles are
#: later rows over their own read models).
READ_PROFILE = "CANON_VIEW"

#: The authority every committed event carries (INV-1's truth — the
#: log is the canonical product; LAW §14 renders the axis, it does
#: not guess it).
EVENT_AUTHORITY = "CANONICAL"

#: The run stem's closed form (the ``run_<seed>_<n>`` family plus any
#: future well-formed stem): one leading alphanumeric, then
#: alphanumerics/underscores/hyphens — no dots, no separators, no
#: traversal; the name is JOINED onto the runs root, never resolved.
_RUN_STEM = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


class ObservatoryReadError(ValueError):
    """A read-model domain violation (the reason rides the message;
    the operations layer translates it to DOMAIN_REJECTED)."""


def _require_stem(run: object) -> str:
    """The closed stem form (path-safety by construction, never a
    resolve): anything else is a loud read-model error."""
    if not isinstance(run, str) or not run:
        raise ObservatoryReadError(
            "observatory: run must be a non-empty str"
        )
    if not _RUN_STEM.match(run):
        raise ObservatoryReadError(
            f"observatory: run {run!r} is not a run stem "
            "(the [A-Za-z0-9][A-Za-z0-9_-]* form)"
        )
    return run


def _read_header(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """One log's header alone (the listing's cheap arm): the first
    line parsed and shape-validated. A missing/blank/corrupt first
    line is the honest degradation pair (None, the observed error)
    — never a raised listing and never a silent skip."""
    try:
        with path.open(encoding="utf-8") as handle:
            first = handle.readline()
    except OSError as exc:
        return None, f"unreadable: {exc.__class__.__name__}"
    if not first.strip():
        return None, "empty first line"
    try:
        data = json.loads(first)
    except ValueError as exc:
        return None, f"first line is not JSON: {exc}"
    try:
        validate_header(data)
    except LogError as exc:
        return None, str(exc)
    return {
        "seed": data["seed"],
        "pack": data["pack"],
        "schema_version": data["schema_version"],
    }, None


def list_runs(runs_root: Path) -> dict[str, object]:
    """The discovery scan over the runs root (the Observatory context
    strip's own read). A missing root is the honest NO DATA — an
    empty listing, never an error."""
    if not runs_root.is_dir():
        return {"runs_root": runs_root.name, "runs": []}
    runs: list[dict[str, object]] = []
    for path in sorted(runs_root.glob("*.jsonl")):
        header, error = _read_header(path)
        entry: dict[str, object] = {
            "name": path.stem,
            "size_bytes": path.stat().st_size,
            "header": header,
            "error": error,
        }
        runs.append(entry)
    return {"runs_root": runs_root.name, "runs": runs}


def read_window(
    runs_root: Path,
    schema: Mapping[str, Any],
    run: str,
    after: str = "",
    limit: int | None = None,
) -> dict[str, object]:
    """One run's bounded event window (the event table + the
    selection model's read). The full log is validated line by line
    (T0 — ``read_log``'s own law) before the window is cut; the
    cursor is an event id (LAW §6.2)."""
    _require_stem(run)
    if not isinstance(after, str):
        raise ObservatoryReadError("observatory: after must be a str (event id)")
    if limit is None:
        limit = DEFAULT_WINDOW
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ObservatoryReadError("observatory: limit must be a positive int")
    limit = min(limit, MAX_WINDOW)
    path = runs_root / f"{run}.jsonl"
    if not path.is_file():
        raise ObservatoryReadError(
            f"observatory: no run {run!r} in the runs root "
            "(NO MATCH — the run does not exist)"
        )
    try:
        header, events = read_log(path, schema)
    except (LogError, OSError, ValueError) as exc:
        raise ObservatoryReadError(
            f"observatory: run {run!r} failed validation: {exc}"
        ) from exc
    start = 0
    ids: dict[str, int] = {}
    for index, record in enumerate(events):
        # The event id IS the semantic identity (LAW §6.2) — a
        # duplicate makes the log corrupt for cursoring (and for
        # selection); refused loudly, never a silently-skipped window.
        if record.id in ids:
            raise ObservatoryReadError(
                f"observatory: run {run!r} carries duplicate event id "
                f"{record.id!r} — the log is corrupt"
            )
        ids[record.id] = index
    if after:
        # A stale cursor (the id left the run) is a loud error: the
        # surface re-reads from the head, never a silent empty window.
        if after not in ids:
            raise ObservatoryReadError(
                f"observatory: after {after!r} is not an event of run "
                f"{run!r} (a stale cursor — re-read from the head)"
            )
        start = ids[after] + 1
    window_events = events[start : start + limit]
    rows = [_row(record) for record in window_events]
    next_after: str | None = None
    if start + limit < len(events) and window_events:
        next_after = window_events[-1].id
    return {
        "run": run,
        "header": {
            "schema_version": header["schema_version"],
            "seed": header["seed"],
            "python": header["python"],
            "commit": header["commit"],
            "pack": header["pack"],
        },
        "profile": READ_PROFILE,
        "authority": EVENT_AUTHORITY,
        "total_events": len(events),
        "window": {
            "after": after,
            "limit": limit,
            "events": rows,
            "next_after": next_after,
        },
    }


def _row(record: Any) -> dict[str, object]:
    """One event's bounded projection — the table row + the
    inspector's own data (LAW §5.1: the selection consumes the SAME
    document; no second per-event op in the slice). The declared
    cause and the state changes ride as DATA (LAW §12: a cause_id
    alone never implies a causal conclusion — the evidence ladder
    keeps its own honest statuses)."""
    return {
        "id": record.id,
        "t": record.t,
        "type": record.type,
        "actor": record.actor,
        "kind": record.outcome.get("kind", record.type),
        "importance": record.importance,
        "cause": record.cause,
        "authority": EVENT_AUTHORITY,
        "state_changes": [
            {
                "entity": change.entity,
                "prop": change.prop,
                "from": change.from_,
                "to": change.to_,
            }
            for change in record.state_changes
        ],
        "knowledge_count": len(record.knowledge),
        "provenance": dict(record.provenance),
    }
