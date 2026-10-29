"""The Observatory operations surface (obs-2, FRONTEND_UIUX_LAW
§25's P1 continuation — the live run feeding the context strip +
the event table over READ operations; the selection model's first
consumer rides the same documents).

The law: the Observatory is a PROJECTION instrument, never a second
authority (LAW §0 + the invariants 1/2). This module owns ONLY the
operations surface — the closed argument sets, the DOMAIN_REJECTED
translations (NOT_SENT, never a §12.1 outcome), and the gateway
wiring. The read model itself lives at ``workbench/observatory_read.py``
(the seam's one home beside ``scene_build.py`` — the application-
operations package stays CanonSim-free, its own dependency
envelope's law).

```text
observatory.runs — READ, no arguments: the discovery scan (the
                    context strip's own read).
observatory.read — READ, {run, after?, limit?}: one run's bounded
                    event window (the event table + the selection
                    model's read).
```

Honest failures (LAW §16/§21.1): every read-model domain violation
— unknown run (NO MATCH), stale cursor, corrupt log, malformed
stem, bad limit, unknown argument — is DOMAIN_REJECTED with the
observed cause, never a fabricated empty result.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from workbench.api.gateway import (
    Gateway,
    OperationRejected,
    OperationSpec,
)
from workbench.observatory_read import (
    ObservatoryReadError,
    list_runs,
    read_window,
)


def _rejected(reason: str) -> OperationRejected:
    """The handlers' DOMAIN_REJECTED carrier (NOT_SENT — the same
    closed vocabulary as the sibling operations)."""
    return OperationRejected("DOMAIN_REJECTED", reason)


def register_observatory_operations(
    gateway: Gateway, runs_root: Path, schema: Mapping[str, Any]
) -> None:
    """The Observatory family's wiring (the composition root calls
    it — §6.1's single-owner law): the two READ operations over the
    injected runs root and event schema. The root and schema are
    INJECTED (the composition root owns the filesystem truth — this
    module never guesses a path)."""
    gateway.register(
        OperationSpec(
            name="observatory.runs",
            kind="READ",
            handler=_make_runs(runs_root),
            description=(
                "the runs discovery scan over the canonical logs root "
                "(obs-2: the Observatory context strip's own read)"
            ),
        )
    )
    gateway.register(
        OperationSpec(
            name="observatory.read",
            kind="READ",
            handler=_make_read(runs_root, schema),
            description=(
                "one run's bounded event window over the canonical log "
                "(obs-2: the event table + the selection model's read)"
            ),
        )
    )


def _make_runs(runs_root: Path):
    def handler(context) -> Mapping[str, object]:
        if context.arguments:
            raise _rejected(
                "observatory.runs: takes no arguments "
                f"({sorted(context.arguments)})"
            )
        return list_runs(runs_root)

    return handler


def _make_read(runs_root: Path, schema: Mapping[str, Any]):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"run", "after", "limit"})
        if unknown:
            raise _rejected(
                f"observatory.read: unknown argument(s) {unknown} "
                "(closed set: ['after', 'limit', 'run'])"
            )
        run = arguments.get("run")
        if not isinstance(run, str) or not run:
            raise _rejected("observatory.read: run must be a non-empty str")
        after = arguments.get("after", "")
        if not isinstance(after, str):
            raise _rejected(
                "observatory.read: after must be a str (event id)"
            )
        limit = arguments.get("limit")
        try:
            return read_window(runs_root, schema, run, after, limit)
        except ObservatoryReadError as exc:
            raise _rejected(f"observatory.read: {exc}") from exc

    return handler
