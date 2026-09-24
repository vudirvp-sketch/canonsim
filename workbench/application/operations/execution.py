"""The operation deadline, cancellation and the run registry (wb-5,
the app spec §§10/12 — the family's fifth row).

The law: **one logical operation owns one absolute deadline on the
monotonic clock; lower layers receive remaining budget only** (§12).
`OperationDeadline` is that ownership — frozen at admission, never
extended (there is no API that could); the work sees
`WorkContext.remaining_budget()`, the checkpoint reading, never a
fresh deadline. "Per-attempt socket timeout is transport policy, not
a new logical deadline; `tries × timeout_s` is invalid" — the retry
that matters here is the gateway's idempotent replay (the recorded
outcome, wb-4's law): a retried `run.start` NEVER re-runs, so no
retry can stretch the deadline.

The run registry — the execution substrate §8 names ("long-running
work returns identity immediately"):

```text
admit  : freeze the §10 inputs BEFORE any side effect, derive the
         execution identity, enter ADMITTED
launch : walk STARTING, spawn the worker (a daemon thread — the
         in-memory registry dies with the process, G2's honest form;
         the persistence rows own the durable counterpart)
worker : walk RUNNING → the work callable (outside the registry
         lock) → the truthful terminal close
```

The terminal close (§11 + §12.3, every walk under the registry lock
and through `lifecycles.transition` — no direct state writes):

```text
work returned  + CANCEL_REQUESTED → FAILED_TO_CANCEL (the result
                recorded on the record — the late result, never a
                completion)
work returned  otherwise          → COMPLETING → COMPLETED
WorkCancelled  + CANCEL_REQUESTED → CANCELED (the observed abort)
WorkCancelled  otherwise          → FAILED (the contract violation)
DeadlineExceeded                  → FAILED (the diagnostics name it)
any other raise                   → FAILED (the failure type named)
```

The artifact closes ONCE at terminal (`ExecutionArtifact.freeze`,
status = the terminal state — the §11 closure the wb-3 field pointed
at) and stays clock-free: the deadline's monotonic readings are
runtime observations riding the run.get document's explicit
`deadline` field, never the artifact (D4's law — no hidden clock in
any byte-deterministic form).

The execution identity (§10: replay creates a NEW one — the replay
operation itself is a later row's; the derivation here): the digest
over the request identity + the frozen-input request digest. Under
the gateway's idempotency layer one logical request admits exactly
once, so the derivation is collision-free where it is reachable; a
duplicate admission is LOUD (`RegistryError`), never a silent reuse.

Cancellation truth (§12.3): `request_cancel` returns the REQUEST's
truth — CANCEL_REQUESTED (accepted; the outcome will be CANCELED or
FAILED_TO_CANCEL or UNKNOWN), CANCELED (idempotent re-request on an
already-canceled record), or FAILED_TO_CANCEL (the work is terminal
or past its last checkpoint — "do not claim completion merely
because a stop button was pressed", and never claim cancellation the
work did not observe). `mark_unknown` is the §25 process-loss surface
(the watchdog rows' producer; the vocabulary's UNKNOWN branch).
"""

from __future__ import annotations

import json
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

from workbench.application.artifact import (
    ExecutionArtifact,
    request_digest,
)
from workbench.application.clock import AppClock
from workbench.application.identity import content_digest
from workbench.application.operations.lifecycles import (
    TERMINAL_STATES,
    transition,
)


class RegistryError(ValueError):
    """A registry-contract violation (construction- or admission-
    time — LOUD, never a silent fallback)."""


class WorkCancelled(Exception):
    """The cooperative checkpoint abort (§12.3): the work observed
    the cancellation token at a checkpoint and stopped."""


class DeadlineExceeded(Exception):
    """The §12 deadline law's abort: the checkpoint observed the
    operation's absolute deadline passed — a terminal failure, never
    a hidden retry loop (§29's "startup timeout → terminal")."""


@dataclass(frozen=True)
class ExecutionRegistryConfig:
    """The registry's boundedness ceilings (§26: "bounded requires an
    explicit ceiling"): the default deadline when the caller supplies
    none, and the maximum any caller may request — a deadline beyond
    the ceiling is rejected at admission (DOMAIN_REJECTED upstream),
    never silently clamped."""

    default_deadline_seconds: float = 60.0
    max_deadline_seconds: float = 3600.0

    def __post_init__(self) -> None:
        for name in ("default_deadline_seconds", "max_deadline_seconds"):
            value = getattr(self, name)
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or value <= 0
            ):
                raise RegistryError(f"{name}: a positive number")
        if self.default_deadline_seconds > self.max_deadline_seconds:
            raise RegistryError(
                "default_deadline_seconds cannot exceed "
                "max_deadline_seconds"
            )


@dataclass(frozen=True)
class OperationDeadline:
    """§12's `OperationContext` deadline half: the operation's ONE
    absolute deadline on the monotonic clock, frozen at admission.
    `remaining(now)` is the lower layers' only view — the budget
    left; `exceeded(now)` its terminal question."""

    operation_id: str
    started_monotonic: float
    deadline_monotonic: float

    def __post_init__(self) -> None:
        if not self.operation_id:
            raise RegistryError("deadline: empty operation_id")
        if self.deadline_monotonic <= self.started_monotonic:
            raise RegistryError(
                "deadline: deadline_monotonic must exceed "
                "started_monotonic (a positive budget)"
            )

    def remaining(self, now_monotonic: float) -> float:
        """The remaining budget at a monotonic reading (negative once
        past — `exceeded` is the boolean form; no clamping hides the
        overrun)."""
        return self.deadline_monotonic - now_monotonic

    def exceeded(self, now_monotonic: float) -> bool:
        return now_monotonic >= self.deadline_monotonic


class CancellationToken:
    """§12's `cancellation` field: the cooperative token the work
    polls at its checkpoints — `request()` is the cancel path's write
    (the registry, under its lock), `requested()` the work's read."""

    def __init__(self) -> None:
        self._event = threading.Event()

    def request(self) -> None:
        self._event.set()

    def requested(self) -> bool:
        return self._event.is_set()


def _no_progress(_payload: Mapping[str, object]) -> None:
    """The progress reporter's default no-op (the older work kinds —
    digest, chat — never report; the field stays constructible)."""


@dataclass(frozen=True)
class WorkContext:
    """What a work callable receives (§12's OperationContext material
    for the run family): the execution identity, the frozen absolute
    deadline, the injectable clock, the cancellation token, and the
    progress reporter (wb-9 — the live-observation surface a long
    download reports through; a no-op default keeps the older work
    kinds' construction unchanged). `check()` is THE checkpoint — the
    cooperative contract every long-running work honours between its
    chunks; `progress(payload)` is the §13 operational-state half — a
    JSON-safe mapping the run.get document serves to the caller
    BETWEEN admission and the terminal (never identity, never
    artifact — D4's clock-adjacency law applies to it too)."""

    execution_id: str
    deadline: OperationDeadline
    clock: AppClock
    cancellation: CancellationToken
    progress: Callable[[Mapping[str, object]], None] = _no_progress

    def cancellation_requested(self) -> bool:
        return self.cancellation.requested()

    def remaining_budget(self) -> float:
        """The budget left, read through the wired clock — the only
        deadline view the work ever gets (§12: remaining budget
        only)."""
        return self.deadline.remaining(self.clock.now_monotonic())

    def check(self) -> None:
        """The checkpoint: raise `WorkCancelled` when the cancellation
        was requested, `DeadlineExceeded` when the absolute deadline
        passed. Never returns a verdict — a checkpoint is an abort or
        nothing."""
        if self.cancellation.requested():
            raise WorkCancelled(
                f"execution {self.execution_id}: the checkpoint observed "
                "the cancellation request"
            )
        if self.deadline.exceeded(self.clock.now_monotonic()):
            raise DeadlineExceeded(
                f"execution {self.execution_id}: the absolute deadline "
                f"passed with {self.remaining_budget():.3f}s remaining"
            )


#: The registered work signature: context → a JSON-safe result
#: document (validated at the terminal close — the closed-document
#: law).
WorkCallable = Callable[[WorkContext], Mapping[str, object]]


@dataclass(frozen=True)
class WorkKind:
    """One wired work kind (the composition's registration unit —
    defined here, the run family's own module, so the kind factories
    (models.py's digest + fetch) can construct theirs without a
    circular import): the name, the typed argument validator (the
    envelope's `arguments` → the frozen-input pairs — the §10 freeze
    material, DOMAIN_REJECTED on any violation), the work callable
    over the frozen inputs, and the kind's own default deadline
    (wb-9 — a minutes-class kind resolves its own §12 material input
    when the caller names none; None = the registry's generic
    default)."""

    name: str
    description: str
    validate_arguments: Callable[[Mapping[str, object]], dict[str, str]]
    work: Callable[[WorkContext, Mapping[str, str]], Mapping[str, object]]
    default_deadline_seconds: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise RegistryError(
                f"work kind {self.name!r}: a non-empty name"
            )
        if not callable(self.validate_arguments) or not callable(self.work):
            raise RegistryError(
                f"work kind {self.name!r}: validate_arguments and work "
                "must be callable"
            )
        if self.default_deadline_seconds is not None and (
            isinstance(self.default_deadline_seconds, bool)
            or not isinstance(self.default_deadline_seconds, (int, float))
            or self.default_deadline_seconds <= 0
        ):
            raise RegistryError(
                f"work kind {self.name!r}: default_deadline_seconds "
                "must be a positive number or None"
            )


def _validate_work_result(
    result: object,
) -> tuple[bool, dict[str, object] | None, str | None]:
    """The closed-document gate for a work result: a JSON-safe
    mapping passes (True, the mapping, None); anything else fails
    with the diagnostic that names the violation — the caller closes
    the record FAILED with it, never a best-effort record."""
    if not isinstance(result, Mapping):
        return (
            False,
            None,
            f"the work returned {type(result).__name__}, not a mapping "
            "(the closed-document law)",
        )
    try:
        json.dumps(dict(result), sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError):
        return False, None, "the work result is not JSON-safe"
    return True, dict(result), None


@dataclass
class _ExecutionRecord:
    """The registry-private execution record (the read view is the
    `document()` mapping — callers never touch this)."""

    execution_id: str
    operation_id: str
    session_id: str
    work_kind: str
    frozen_inputs: tuple[tuple[str, str], ...]
    request_digest_value: str
    state: str
    deadline: OperationDeadline
    cancellation: CancellationToken
    result: dict[str, object] | None = None
    failure_type: str | None = None
    diagnostics: list[str] = field(default_factory=list)
    artifact: ExecutionArtifact | None = None
    thread: threading.Thread | None = None
    progress: dict[str, object] | None = None


class ExecutionRegistry:
    """The in-memory execution registry (G2: in-memory by contract —
    the persistence rows own the durable counterpart).

    One coarse registry lock serializes every state walk, the
    cancellation request, and the terminal close; the WORK runs
    outside it (a long digest must not block `run.get`). The worker
    threads are daemons: the registry and its records die with the
    process — the honest wb-5 form, restorable state being a later
    row's own contract.
    """

    def __init__(
        self,
        clock: AppClock,
        config: ExecutionRegistryConfig | None = None,
    ) -> None:
        self._clock = clock
        self._config = config if config is not None else ExecutionRegistryConfig()
        self._lock = threading.Lock()
        self._executions: dict[str, _ExecutionRecord] = {}

    @property
    def config(self) -> ExecutionRegistryConfig:
        return self._config

    @property
    def execution_ids(self) -> tuple[str, ...]:
        """Every admitted execution's identity, sorted (the
        deterministic enumeration)."""
        with self._lock:
            return tuple(sorted(self._executions))

    def resolve_deadline_seconds(self, requested: float | None) -> float:
        """The resolved deadline (§12's material input): the caller's
        explicit value or the default — validated against the ceiling
        (a bounded run, §26), never silently clamped."""
        seconds = (
            self._config.default_deadline_seconds
            if requested is None
            else requested
        )
        if (
            isinstance(seconds, bool)
            or not isinstance(seconds, (int, float))
            or seconds <= 0
        ):
            raise RegistryError(
                f"deadline_seconds: a positive number (got {seconds!r})"
            )
        if seconds > self._config.max_deadline_seconds:
            raise RegistryError(
                f"deadline_seconds {seconds} exceeds the ceiling "
                f"{self._config.max_deadline_seconds} (§26 boundedness — "
                "rejected, never clamped)"
            )
        return float(seconds)

    def admit(
        self,
        operation_id: str,
        session_id: str,
        work_kind: str,
        frozen_inputs: Mapping[str, str],
        deadline_seconds: float | None,
    ) -> str:
        """Admit one execution (§10: the input freeze happens HERE —
        before any side effect, before the work exists): derive the
        execution identity from the request identity + the frozen
        material, enter ADMITTED, and return the execution_id. A
        duplicate derivation is LOUD (the idempotency layer upstream
        makes it unreachable in practice — the law holds anyway)."""
        seconds = self.resolve_deadline_seconds(deadline_seconds)
        pairs = tuple(sorted(frozen_inputs.items()))
        digest = request_digest(dict(pairs))
        execution_id = content_digest(
            json.dumps(
                {"operation_id": operation_id, "request_digest": digest},
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        started = self._clock.now_monotonic()
        deadline = OperationDeadline(
            operation_id=operation_id,
            started_monotonic=started,
            deadline_monotonic=started + seconds,
        )
        record = _ExecutionRecord(
            execution_id=execution_id,
            operation_id=operation_id,
            session_id=session_id,
            work_kind=work_kind,
            frozen_inputs=pairs,
            request_digest_value=digest,
            state="ADMITTED",
            deadline=deadline,
            cancellation=CancellationToken(),
        )
        with self._lock:
            if execution_id in self._executions:
                raise RegistryError(
                    f"execution {execution_id}: already admitted — one "
                    "request identity, one execution"
                )
            self._executions[execution_id] = record
        return execution_id

    def launch(self, execution_id: str, work: WorkCallable) -> None:
        """Launch the admitted execution: walk STARTING, construct +
        start the worker. The walk happens under the lock BEFORE the
        spawn, so the dispatch-time view is exactly STARTING; any
        spawn failure (construction or start) walks FAILED loudly
        (§29: no hidden loop) and re-raises — the handler's raise maps
        SENT_OUTCOME_UNKNOWN upstream, the registry's own record
        stays truthful at its layer."""
        with self._lock:
            record = self._require_locked(execution_id)
            self._walk_locked(record, "STARTING")
        try:
            thread = threading.Thread(
                target=self._worker,
                args=(record, work),
                daemon=True,
                name=f"canonsim-run-{execution_id[:12]}",
            )
            with self._lock:
                record.thread = thread
            thread.start()
        except BaseException as exc:
            with self._lock:
                self._close_locked(
                    record,
                    "FAILED",
                    diagnostics=[
                        "the worker thread failed to start: "
                        f"{type(exc).__name__}"
                    ],
                )
            raise

    def document(self, execution_id: str, session_id: str) -> dict[str, object]:
        """The run.get view: the live state, the frozen inputs (the
        §10 input freeze is observable from admission — the
        before-side-effects proof surface), the deadline readings (an
        explicit runtime observation, never identity), the live
        progress (wb-9 — the work's own last report, None when it
        never reported), and at terminal the result, the failure
        type, and the closed artifact."""
        with self._lock:
            record = self._require_owned_locked(execution_id, session_id)
            terminal = record.state in TERMINAL_STATES["EXECUTION"]
            return {
                "execution_id": record.execution_id,
                "operation_id": record.operation_id,
                "work": record.work_kind,
                "state": record.state,
                "terminal": terminal,
                "frozen_inputs": [list(pair) for pair in record.frozen_inputs],
                "request_digest": record.request_digest_value,
                "deadline": {
                    "started_monotonic": record.deadline.started_monotonic,
                    "deadline_monotonic": record.deadline.deadline_monotonic,
                },
                "progress": (
                    dict(record.progress)
                    if record.progress is not None
                    else None
                ),
                "result": dict(record.result) if record.result is not None else None,
                "failure_type": record.failure_type,
                "diagnostics": list(record.diagnostics),
                "artifact": (
                    record.artifact.to_mapping()
                    if record.artifact is not None
                    else None
                ),
            }

    def report_progress(
        self, execution_id: str, payload: Mapping[str, object]
    ) -> None:
        """The work's live-observation write (wb-9 — the reporter the
        WorkContext closes over): one JSON-safe mapping recorded on
        the run's record, served by `document()` until the terminal
        close leaves it in place (the last honest observation, never
        scrubbed). A non-JSON-safe payload is the work contract's own
        loud violation."""
        try:
            json.dumps(dict(payload), sort_keys=True, separators=(",", ":"))
        except (TypeError, ValueError) as exc:
            raise RegistryError(
                f"the progress payload is not JSON-safe: {exc}"
            ) from exc
        with self._lock:
            record = self._require_locked(execution_id)
            record.progress = dict(payload)

    def request_cancel(self, execution_id: str, session_id: str) -> str:
        """§12.3's cancellation request truth (see the module note).
        The state walk and the token write happen under one lock hold
        — the worker's next checkpoint observes them together."""
        with self._lock:
            record = self._require_owned_locked(execution_id, session_id)
            if record.state == "CANCEL_REQUESTED":
                return "CANCEL_REQUESTED"
            if record.state == "CANCELED":
                return "CANCELED"
            if record.state in ("ADMITTED", "STARTING", "RUNNING"):
                self._walk_locked(record, "CANCEL_REQUESTED")
                record.cancellation.request()
                return "CANCEL_REQUESTED"
            # COMPLETING / COMPLETED / FAILED / FAILED_TO_CANCEL /
            # UNKNOWN: the work is past its last checkpoint or
            # terminal — the request cannot take effect.
            return "FAILED_TO_CANCEL"

    def mark_unknown(self, execution_id: str, reason: str) -> None:
        """The §25 process-loss surface: an execution whose outcome
        cannot be determined (the worker vanished without a terminal
        close) is marked UNKNOWN — truthful, evidence preserved (the
        diagnostics carry the reason). The watchdog rows own the
        producers; the registry owns the honest terminal. Legal from
        STARTING/RUNNING/CANCEL_REQUESTED (§11's predecessors); from
        ADMITTED it raises — an unlaunched admission has no
        undeterminable outcome."""
        with self._lock:
            record = self._require_locked(execution_id)
            self._close_locked(record, "UNKNOWN", diagnostics=[reason])

    def wait(self, execution_id: str, timeout: float) -> bool:
        """Await the execution's terminal state (the observation
        helper — the production read path is `document()`/run.get):
        join the worker up to `timeout` seconds and report whether
        the record is terminal. A timeout is a FALSE return, never an
        error — polling stays the caller's choice."""
        with self._lock:
            record = self._require_locked(execution_id)
            thread = record.thread
        if thread is not None and thread.is_alive():
            thread.join(timeout)
        with self._lock:
            record = self._executions.get(execution_id)
            return (
                record is not None
                and record.state in TERMINAL_STATES["EXECUTION"]
            )

    # ------------------------------------------------------------ worker

    def _worker(self, record: _ExecutionRecord, work: WorkCallable) -> None:
        """The worker thread body: RUNNING, the work (OUTSIDE the
        registry lock), the truthful terminal close (§12.3 — the
        mapping in the module note)."""
        with self._lock:
            self._walk_locked(record, "RUNNING")
        context = WorkContext(
            execution_id=record.execution_id,
            deadline=record.deadline,
            clock=self._clock,
            cancellation=record.cancellation,
            progress=self._progress_reporter(record.execution_id),
        )
        try:
            result = work(context)
        except WorkCancelled:
            with self._lock:
                if record.state == "CANCEL_REQUESTED":
                    self._close_locked(
                        record,
                        "CANCELED",
                        diagnostics=[
                            "the checkpoint observed the cancellation "
                            "request"
                        ],
                    )
                else:
                    self._close_locked(
                        record,
                        "FAILED",
                        diagnostics=[
                            "the work raised WorkCancelled without a "
                            "cancellation request (the work contract "
                            "violation)"
                        ],
                    )
        except DeadlineExceeded:
            with self._lock:
                self._close_locked(
                    record,
                    "FAILED",
                    failure_type="DeadlineExceeded",
                    diagnostics=[
                        "deadline exceeded (the absolute §12 deadline)"
                    ],
                )
        except Exception as exc:
            with self._lock:
                self._close_locked(
                    record,
                    "FAILED",
                    failure_type=type(exc).__name__,
                    diagnostics=[
                        "the work raised "
                        f"{type(exc).__name__}: {str(exc)[:400]}"
                    ],
                )
        else:
            ok, mapping, bad = _validate_work_result(result)
            with self._lock:
                if not ok:
                    assert bad is not None
                    self._close_locked(record, "FAILED", diagnostics=[bad])
                elif record.state == "CANCEL_REQUESTED":
                    self._close_locked(
                        record,
                        "FAILED_TO_CANCEL",
                        result=mapping,
                        diagnostics=[
                            "the work returned despite the cancellation "
                            "request (the late result, recorded — never a "
                            "completion)"
                        ],
                    )
                else:
                    self._close_locked(record, "COMPLETED", result=mapping)

    # ------------------------------------------------------------- locked

    def _progress_reporter(
        self, execution_id: str
    ) -> Callable[[Mapping[str, object]], None]:
        def report(payload: Mapping[str, object]) -> None:
            self.report_progress(execution_id, payload)

        return report

    def _walk_locked(self, record: _ExecutionRecord, target: str) -> None:
        """One validated state move (§11's table, loud on illegal —
        including every attempted move OUT of a terminal state: a
        double close is a bug, never a quiet overwrite)."""
        record.state = transition("EXECUTION", record.state, target)

    def _close_locked(
        self,
        record: _ExecutionRecord,
        terminal: str,
        result: dict[str, object] | None = None,
        failure_type: str | None = None,
        diagnostics: list[str] | None = None,
    ) -> None:
        """The terminal close: the COMPLETED path walks COMPLETING
        first (§11's ladder), then the terminal state, the result, the
        diagnostics — and the §10 artifact closes ONCE with the
        terminal status (clock-free: the deadline readings never enter
        it)."""
        if terminal == "COMPLETED":
            self._walk_locked(record, "COMPLETING")
        self._walk_locked(record, terminal)
        record.result = result
        record.failure_type = failure_type
        if diagnostics:
            record.diagnostics.extend(diagnostics)
        record.artifact = ExecutionArtifact.freeze(
            execution_id=record.execution_id,
            status=terminal,
            frozen_inputs=record.frozen_inputs,
            operation_id=record.operation_id,
            diagnostics=tuple(record.diagnostics),
        )

    def _require_locked(self, execution_id: str) -> _ExecutionRecord:
        record = self._executions.get(execution_id)
        if record is None:
            raise RegistryError(f"execution {execution_id!r}: no such execution")
        return record

    def _require_owned_locked(
        self, execution_id: str, session_id: str
    ) -> _ExecutionRecord:
        """The session-ownership guard: an execution is visible only
        to the session that admitted it (the in-memory registry's own
        boundary; the cross-session read model is a later row's)."""
        record = self._require_locked(execution_id)
        if record.session_id != session_id:
            raise RegistryError(
                f"execution {execution_id!r}: belongs to another session "
                "(the session-ownership law)"
            )
        return record
