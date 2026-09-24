"""The workbench composition root (wb-5, the app spec §6.1 — the
family's fifth row; the backend wiring wb-6, §32 step 7).

The law: **the composition root is the single wiring owner** —
construct → validate dependencies → wire owners (register the
operations on the gateway) — "not = service locator | global
registry | god object | hidden dependency injector" (§6.1). This
module constructs the model registry and the execution registry,
wires the work kinds (the one real kind in wb-5: `model.digest`,
bound to the model registry), and registers the five application
operations on the wb-4 gateway's `OperationSpec` surface — the
composition point wb-4 named:

```text
run.start / run.get / run.cancel   — the run family (§8), over the
                                     execution registry (§10/§12)
model.list / model.inspect         — the model family's discovery
                                     half (§20), over the §16
                                     MODELS_ASSETS role
```

The backend row (wb-6, the owner's «подключи llama.cpp» call): when
a `backend` port is injected, `register_backend_operations` wires the
three backend operations — chat.send + model.load/model.unload
(§8/§19.1/§20) — and the admission law's wb-5 deferral closes:
chat.send's consumer IS the backend. With no port the three stay
unregistered (the same honest form — machinery without a consumer
is forbidden). The physical transport stays `cli/engine.py` (INV-4):
`workbench/` never imports it — the application-entry rows own the
physical wiring; the port is the typed seam (backend.py).

The registered handlers reject through the gateway's public
`OperationRejected` carrier (DOMAIN_REJECTED — NOT_SENT, never a
§12.1 outcome), emit their dispatch-time effects through the
context's `effects` surface (§13's ordered stream), and read the
clock only through the context (§17).

Tests compose smaller compositions explicitly (§6.1's own law):
`work_kinds` is injectable — the claim packet wires probe kinds
(blocking, failing, deadline-crossing) without touching the
production kind.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from workbench.api.gateway import (
    Gateway,
    OperationRejected,
    OperationSpec,
)
from workbench.application.clock import AppClock
from workbench.application.operations.backend import (
    BackendPortError,
    ModelLoadStates,
    register_backend_operations,
)
from workbench.application.operations.execution import (
    ExecutionRegistry,
    ExecutionRegistryConfig,
    RegistryError,
    WorkCallable,
    WorkContext,
)
from workbench.application.operations.models import (
    ModelRegistry,
    ModelRegistryError,
    digest_work,
)

__all__ = [
    "WorkKind",
    "WorkbenchOperations",
    "compose_workbench_operations",
    "model_digest_kind",
]


class CompositionError(ValueError):
    """A composition-root contract violation (construction-time —
    the §6.1 validate-dependencies step, LOUD)."""


@dataclass(frozen=True)
class WorkKind:
    """One wired work kind (the composition's registration unit):
    the name, the typed argument validator (the envelope's `arguments`
    → the frozen-input pairs — the §10 freeze material, DOMAIN_REJECTED
    on any violation), and the work callable over the frozen inputs."""

    name: str
    description: str
    validate_arguments: Callable[[Mapping[str, object]], dict[str, str]]
    work: Callable[[WorkContext, Mapping[str, str]], Mapping[str, object]]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise CompositionError(
                f"work kind {self.name!r}: a non-empty name"
            )
        if not callable(self.validate_arguments) or not callable(self.work):
            raise CompositionError(
                f"work kind {self.name!r}: validate_arguments and work "
                "must be callable"
            )


@dataclass(frozen=True)
class WorkbenchOperations:
    """The composed application's handle: the two registries (the
    state owners), the backend family's load-state owner (None when
    no port was injected — the three backend operations then stay
    unregistered, the admission law's honest form), and the wired
    work-kind names (the registration closure — what run.start may
    launch)."""

    models: ModelRegistry
    executions: ExecutionRegistry
    work_kinds: tuple[str, ...]
    model_loads: ModelLoadStates | None = None


def model_digest_kind(registry: ModelRegistry) -> WorkKind:
    """The one real work kind (§20's long-running arm): the chunked
    strong-identity computation over the model registry — the run
    family's first consumer, bound to the registry the composition
    constructed."""

    def validate_arguments(
        arguments: Mapping[str, object],
    ) -> dict[str, str]:
        unknown = sorted(set(arguments) - {"logical_name"})
        if unknown:
            raise _rejected(
                f"model.digest: unknown argument(s) {unknown} "
                "(closed set: ['logical_name'])"
            )
        logical_name = arguments.get("logical_name")
        if not isinstance(logical_name, str) or not logical_name:
            raise _rejected(
                "model.digest: logical_name must be a non-empty str"
            )
        # §20's entry gate, pre-admission: the target must be a
        # CURRENT discovery entry — a NOT_SENT domain rejection, never
        # a post-admission work failure (a vanish between admission
        # and the work stays the honest late FAILED).
        try:
            registry.resolve(logical_name)
        except ModelRegistryError as exc:
            raise _rejected(f"model.digest: {exc}") from exc
        return {"logical_name": logical_name}

    def work(
        context: WorkContext, inputs: Mapping[str, str]
    ) -> Mapping[str, object]:
        return digest_work(context, registry, inputs["logical_name"])

    return WorkKind(
        name="model.digest",
        description=(
            "the chunked strong-identity computation (§20's "
            "computed-when-needed arm, the §12 checkpoints between "
            "chunks)"
        ),
        validate_arguments=validate_arguments,
        work=work,
    )


def compose_workbench_operations(
    gateway: Gateway,
    models_root: Path,
    clock: AppClock,
    *,
    registry_config: ExecutionRegistryConfig | None = None,
    work_kinds: Mapping[str, WorkKind] | None = None,
    backend: object | None = None,
) -> WorkbenchOperations:
    """Construct → validate → wire: build the registries, resolve the
    work kinds (the caller's mapping or the default `model.digest`
    composition), register the five operations on the gateway — the
    single wiring point (a duplicate name is the gateway's own loud
    one-name-one-owner error) — and, when a backend port is injected,
    the three backend operations (wb-6: chat.send + model.load/
    model.unload over the port). A malformed port is the §6.1
    validate step's own loud CompositionError."""
    models = ModelRegistry(models_root)
    executions = ExecutionRegistry(clock, registry_config)
    if work_kinds is not None:
        kinds = dict(work_kinds)
    else:
        digest_kind = model_digest_kind(models)
        kinds = {digest_kind.name: digest_kind}
    if not kinds:
        raise CompositionError(
            "the composition wires at least one work kind — an empty "
            "work-kind map has no run family"
        )

    gateway.register(
        OperationSpec(
            name="run.start",
            kind="MUTATION",
            handler=_make_run_start(executions, kinds),
            session_scoped=True,
            description="admit + launch one long-running work kind (§8/§12)",
        )
    )
    gateway.register(
        OperationSpec(
            name="run.get",
            kind="READ",
            handler=_make_run_get(executions),
            session_scoped=True,
            description="the execution's live state + frozen inputs + artifact",
        )
    )
    gateway.register(
        OperationSpec(
            name="run.cancel",
            kind="MUTATION",
            handler=_make_run_cancel(executions),
            session_scoped=True,
            description="§12.3's truthful cancellation request",
        )
    )
    gateway.register(
        OperationSpec(
            name="model.list",
            kind="READ",
            handler=_make_model_list(models),
            description="the §20 discovery scan over the MODELS_ASSETS role",
        )
    )
    gateway.register(
        OperationSpec(
            name="model.inspect",
            kind="READ",
            handler=_make_model_inspect(models),
            description="the §9 strong identity computed fresh",
        )
    )
    model_loads: ModelLoadStates | None = None
    if backend is not None:
        try:
            model_loads = register_backend_operations(
                gateway, executions, models, backend
            )
        except BackendPortError as exc:
            raise CompositionError(
                f"the injected backend does not satisfy the port: {exc}"
            ) from exc
    return WorkbenchOperations(
        models=models,
        executions=executions,
        work_kinds=tuple(sorted(kinds)),
        model_loads=model_loads,
    )


# ------------------------------------------------------------- handlers


def _rejected(reason: str) -> OperationRejected:
    """The handlers' DOMAIN_REJECTED carrier — one line, the closed
    vocabulary's NOT_SENT member for every argument/domain
    violation (never a §12.1 dispatch outcome)."""
    return OperationRejected("DOMAIN_REJECTED", reason)


def _make_run_start(
    executions: ExecutionRegistry, kinds: Mapping[str, WorkKind]
):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"work", "arguments", "deadline_seconds"})
        if unknown:
            raise _rejected(
                f"run.start: unknown argument(s) {unknown} "
                "(closed set: ['arguments', 'deadline_seconds', 'work'])"
            )
        work_name = arguments.get("work")
        if not isinstance(work_name, str) or not work_name:
            raise _rejected("run.start: work must be a non-empty str")
        kind = kinds.get(work_name)
        if kind is None:
            raise _rejected(
                f"run.start: unknown work kind {work_name!r} "
                f"(registered: {sorted(kinds)})"
            )
        inner = arguments.get("arguments", {})
        if not isinstance(inner, Mapping):
            raise _rejected(
                "run.start: arguments must be an object (the work's own "
                "arguments)"
            )
        kind_pairs = kind.validate_arguments(inner)
        deadline_argument = arguments.get("deadline_seconds")
        if deadline_argument is not None and (
            isinstance(deadline_argument, bool)
            or not isinstance(deadline_argument, (int, float))
            or deadline_argument <= 0
        ):
            raise _rejected(
                "run.start: deadline_seconds must be a positive number"
            )
        try:
            seconds = executions.resolve_deadline_seconds(deadline_argument)
        except RegistryError as exc:
            raise _rejected(f"run.start: {exc}") from exc
        session_id = context.session.session_id if context.session else ""
        frozen = {
            "work": kind.name,
            **kind_pairs,
            "deadline_seconds": str(seconds),
        }
        execution_id = executions.admit(
            operation_id=context.operation_id,
            session_id=session_id,
            work_kind=kind.name,
            frozen_inputs=frozen,
            deadline_seconds=seconds,
        )
        bound: WorkCallable = lambda ctx: kind.work(ctx, kind_pairs)  # noqa: E731
        executions.launch(execution_id, bound)
        if context.effects is not None:
            context.effects.effect(
                {
                    "effect": "RUN_STARTED",
                    "execution_id": execution_id,
                    "work": kind.name,
                }
            )
        return {
            "execution_id": execution_id,
            "work": kind.name,
            "deadline_seconds": seconds,
        }

    return handler


def _make_run_get(executions: ExecutionRegistry):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"execution_id"})
        if unknown:
            raise _rejected(
                f"run.get: unknown argument(s) {unknown} "
                "(closed set: ['execution_id'])"
            )
        execution_id = arguments.get("execution_id")
        if not isinstance(execution_id, str) or not execution_id:
            raise _rejected("run.get: execution_id must be a non-empty str")
        session_id = context.session.session_id if context.session else ""
        try:
            return executions.document(execution_id, session_id)
        except RegistryError as exc:
            raise _rejected(f"run.get: {exc}") from exc

    return handler


def _make_run_cancel(executions: ExecutionRegistry):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"execution_id"})
        if unknown:
            raise _rejected(
                f"run.cancel: unknown argument(s) {unknown} "
                "(closed set: ['execution_id'])"
            )
        execution_id = arguments.get("execution_id")
        if not isinstance(execution_id, str) or not execution_id:
            raise _rejected("run.cancel: execution_id must be a non-empty str")
        session_id = context.session.session_id if context.session else ""
        try:
            outcome = executions.request_cancel(execution_id, session_id)
        except RegistryError as exc:
            raise _rejected(f"run.cancel: {exc}") from exc
        if context.effects is not None:
            context.effects.effect(
                {
                    "effect": "CANCEL_REQUESTED",
                    "execution_id": execution_id,
                    "cancellation": outcome,
                }
            )
        return {"execution_id": execution_id, "cancellation": outcome}

    return handler


def _make_model_list(models: ModelRegistry):
    def handler(context) -> Mapping[str, object]:
        if context.arguments:
            raise _rejected(
                f"model.list: takes no arguments ({sorted(context.arguments)})"
            )
        try:
            return models.discover()
        except ModelRegistryError as exc:
            raise _rejected(f"model.list: {exc}") from exc

    return handler


def _make_model_inspect(models: ModelRegistry):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"logical_name"})
        if unknown:
            raise _rejected(
                f"model.inspect: unknown argument(s) {unknown} "
                "(closed set: ['logical_name'])"
            )
        logical_name = arguments.get("logical_name")
        if not isinstance(logical_name, str) or not logical_name:
            raise _rejected(
                "model.inspect: logical_name must be a non-empty str"
            )
        try:
            return models.inspect(logical_name)
        except ModelRegistryError as exc:
            raise _rejected(f"model.inspect: {exc}") from exc

    return handler
