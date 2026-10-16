"""The workbench composition root (wb-5, the app spec §6.1 — the
family's fifth row; the backend wiring wb-6, §32 step 7; the fetch
+ settings wiring wb-9; the local-import wiring wb-10).

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

The wb-9 wiring (the owner's «подтянуть модель откуда угодно» +
«настройки запуска llama.cpp» calls): a `fetch` seam (the platform's
HttpModelFetcher, injected like the port — never imported here)
wires the `model.fetch` work kind into the default work-kind map; the
INJECTED `settings_store` (constructed by the composition root over
the §16 USER_CONFIG path — one instance per process, so the launch
provider and the operations share one current state) wires its two
operations (backend.settings / backend.settings.update — only with a
backend port: their consumer); the `temperature_default` provider
hands chat.send the settings' temperature as its BASE layer (§19.1 —
the caller's explicit value still wins); the preview/liveness
callables stay the composition root's own (the store never imports
the platform — §6's direction law).

The wb-10 wiring (the owner's «просто открывающийся проводник и выбор
уже скаченных локальных моделей» call): the `model.import` work kind
— a LOCAL file copy into the models root, no network anywhere (INV-4
untouched — the fetch kind's sibling without a fetcher), so it wires
into the default map UNCONDITIONALLY.

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
from workbench.application.inference import (
    InferenceStore,
    effective_temperature,
    register_inference_operations,
)
from workbench.application.operations.backend import (
    BackendPortError,
    ModelLoadStates,
    chat_replay_adapter,
    register_backend_operations,
)
from workbench.application.operations.execution import (
    ExecutionRegistry,
    ExecutionRegistryConfig,
    RegistryError,
    WorkCallable,
    WorkContext,
    WorkKind,
)
from workbench.application.operations.models import (
    ModelRegistry,
    ModelRegistryError,
    digest_work,
    model_fetch_kind,
    model_import_kind,
)
from workbench.application.operations.observatory import (
    register_observatory_operations,
)
from workbench.application.settings import (
    SettingsStore,
    register_settings_operations,
)

# WorkKind is defined in execution.py (the run family's own module —
# wb-9's fetch factory constructs kinds without a circular import) and
# re-exported here: the composition is its historical home and the
# package's public surface (__all__ carries it).

__all__ = [
    "WorkKind",
    "WorkbenchOperations",
    "compose_workbench_operations",
    "model_digest_kind",
]


class CompositionError(ValueError):
    """A composition-root contract violation (construction-time —
    the §6.1 validate-dependencies step, LOUD)."""


def _temperature_from(store: InferenceStore) -> Callable[[], float]:
    """chat.send's BASE provider over the injected inference store
    (§19.1 + LLAMA_CPP_INFERENCE_CONTROL_LAW §6 — the BASE PROFILE
    layer; the closure reads CURRENT at each dispatch, so an
    inference update applies to the very next chat call; the explicit
    call-local value always wins, backend.py's own law — inf-1
    re-pointed the provider from the launch-settings store's flat
    field to the resolver's effective temperature)."""

    def current_temperature() -> float:
        return effective_temperature(store)

    return current_temperature


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
    fetch: object | None = None,
    settings_store: SettingsStore | None = None,
    inference_store: InferenceStore | None = None,
    command_preview: Callable[[Mapping[str, object]], str] | None = None,
    managed_live: Callable[[], bool] | None = None,
    observatory_runs_root: Path | None = None,
    observatory_schema: Mapping[str, object] | None = None,
) -> WorkbenchOperations:
    """Construct → validate → wire: build the registries, resolve the
    work kinds (the caller's mapping or the default composition — the
    digest kind always, the fetch kind when a fetcher is injected,
    wb-9), register the five operations on the gateway — the single
    wiring point (a duplicate name is the gateway's own loud
    one-name-one-owner error) — and, when a backend port is injected,
    the three backend operations (wb-6: chat.send + model.load/
    model.unload over the port) plus the settings family (wb-9: the
    INJECTED store — constructed by the composition root over the
    USER_CONFIG path, ONE instance per process so the provider and
    the operations read the same current state; its two operations;
    and chat.send's temperature BASE provider — only with a port:
    their consumer). A malformed port is the §6.1 validate step's own
    loud CompositionError."""
    models = ModelRegistry(models_root)
    executions = ExecutionRegistry(clock, registry_config)
    if work_kinds is not None:
        kinds = dict(work_kinds)
    else:
        digest_kind = model_digest_kind(models)
        kinds = {digest_kind.name: digest_kind}
        if fetch is not None:
            fetch_kind = model_fetch_kind(models, fetch)
            kinds[fetch_kind.name] = fetch_kind
        import_kind = model_import_kind(models)
        kinds[import_kind.name] = import_kind
    if not kinds:
        raise CompositionError(
            "the composition wires at least one work kind — an empty "
            "work-kind map has no run family"
        )
    # The execution family's replay adapters (iter-387): every
    # run.start kind is pairs-native-replayable by construction; the
    # chat.completion arm joins when a backend port is wired (the
    # backend block below); the live-gate kinds (model.load/unload)
    # stay OUT — their ladder walks live state the replay must not
    # bypass (their re-dispatch is the user's explicit call).
    replay_adapters: dict[str, ReplayAdapter] = {
        name: _kind_replay_adapter(kind) for name, kind in kinds.items()
    }

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
            temperature_default = (
                _temperature_from(inference_store)
                if inference_store is not None
                else None
            )
            model_loads = register_backend_operations(
                gateway,
                executions,
                models,
                backend,
                temperature_default=temperature_default,
            )
            replay_adapters["chat.completion"] = chat_replay_adapter(
                backend
            )
            if settings_store is not None:
                register_settings_operations(
                    gateway,
                    settings_store,
                    command_preview=command_preview,
                    managed_live=managed_live,
                )
            if inference_store is not None:
                register_inference_operations(
                    gateway,
                    inference_store,
                    compiled_preview=command_preview,
                    managed_live=managed_live,
                )
        except BackendPortError as exc:
            raise CompositionError(
                f"the injected backend does not satisfy the port: {exc}"
            ) from exc
    # The obs-2 wiring (FRONTEND_UIUX_LAW §25's P1 continuation): the
    # Observatory's two READ operations, over the INJECTED runs root
    # + event schema (the consumer-gated law — neither injected means
    # no Observatory surface served; one without the other is a
    # half-wired surface, refused loudly).
    if (
        observatory_runs_root is not None
        and observatory_schema is not None
    ):
        register_observatory_operations(
            gateway, observatory_runs_root, observatory_schema
        )
    elif (
        observatory_runs_root is not None or observatory_schema is not None
    ):
        raise CompositionError(
            "the observatory seam needs BOTH the runs root and the event "
            "schema — one without the other is a half-wired surface"
        )
    # The execution family (iter-387 — the app law §8's
    # execution.get/replay [CONTRACT] row, the replay-UI row's app
    # half): the provenance read + the replay admission, registered
    # AFTER the backend block so the adapter map is final.
    gateway.register(
        OperationSpec(
            name="execution.get",
            kind="READ",
            handler=_make_execution_get(executions),
            session_scoped=True,
            description=(
                "the execution's provenance read (§10): lineage "
                "(replay_of + the direct replays) + the frozen inputs "
                "+ the closed artifact"
            ),
        )
    )
    gateway.register(
        OperationSpec(
            name="execution.replay",
            kind="MUTATION",
            handler=_make_execution_replay(executions, replay_adapters),
            session_scoped=True,
            description=(
                "§10's replay admission: re-run a TERMINAL execution's "
                "frozen material as a NEW execution identity (lineage "
                "via replay_of — the run.start kinds + chat.completion; "
                "the live-gate kinds own their re-dispatch)"
            ),
        )
    )
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
        reserved = sorted(
            set(kind_pairs) & {"work", "deadline_seconds"}
        )
        if reserved:
            raise _rejected(
                f"run.start: the work kind's arguments freeze reserved "
                f"envelope key(s) {reserved} — the envelope vocabulary "
                "law (iter-387: the replay's envelope strip depends "
                "on it)"
            )
        deadline_argument = arguments.get("deadline_seconds")
        if deadline_argument is not None and (
            isinstance(deadline_argument, bool)
            or not isinstance(deadline_argument, (int, float))
            or deadline_argument <= 0
        ):
            raise _rejected(
                "run.start: deadline_seconds must be a positive number"
            )
        resolved_deadline = (
            deadline_argument
            if deadline_argument is not None
            else kind.default_deadline_seconds
        )
        try:
            seconds = executions.resolve_deadline_seconds(resolved_deadline)
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


# ------------------------------------------------- the execution family


#: One replayable work kind's reconstruction arm (iter-387): the
#: FROZEN pairs → the work callable the replay launches — hosted by
#: the kind's own admission site (the module that froze owns the
#: unfreeze, never a second truth over the format).
ReplayAdapter = Callable[[Mapping[str, str]], WorkCallable]


def _kind_replay_adapter(kind: WorkKind) -> ReplayAdapter:
    """The run.start kinds' replay adapter: the frozen envelope → the
    kind's own pairs → the SAME work the original launched
    (WorkKind.work is pairs-native by signature). The envelope's two
    reserved keys (work, deadline_seconds) strip; the integrity
    assertion catches a kind whose own pairs would shadow the
    envelope's work key — loud at replay, never a silently wrong
    re-run (run.start's own admission rejects the reserved keys, the
    same vocabulary law at the owner)."""

    def adapter(frozen_inputs: Mapping[str, str]) -> WorkCallable:
        if frozen_inputs.get("work") != kind.name:
            raise RegistryError(
                f"work kind {kind.name!r} replay: the frozen envelope's "
                f"work key is {frozen_inputs.get('work')!r} — the kind's "
                "own pairs shadow the envelope (the run.start freeze law)"
            )
        pairs = {
            key: value
            for key, value in frozen_inputs.items()
            if key not in ("work", "deadline_seconds")
        }

        def replay_work(context: WorkContext) -> Mapping[str, object]:
            return kind.work(context, pairs)

        return replay_work

    return adapter


def _make_execution_get(executions: ExecutionRegistry):
    """execution.get — the execution family's PROVENANCE read
    (iter-387, the app law §8/§10): the lineage + the frozen material
    + the closed artifact. Deliberately NOT run.get's document: the
    lifecycle read (state/progress/deadline) and the provenance read
    (lineage/frozen inputs/artifact) are separate families'
    concerns — the lineage is readable from ADMISSION (before any
    terminal artifact exists)."""

    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"execution_id"})
        if unknown:
            raise _rejected(
                f"execution.get: unknown argument(s) {unknown} "
                "(closed set: ['execution_id'])"
            )
        execution_id = arguments.get("execution_id")
        if not isinstance(execution_id, str) or not execution_id:
            raise _rejected(
                "execution.get: execution_id must be a non-empty str"
            )
        session_id = context.session.session_id if context.session else ""
        try:
            document = executions.document(execution_id, session_id)
            replay_of, replays = executions.lineage(execution_id, session_id)
        except RegistryError as exc:
            raise _rejected(f"execution.get: {exc}") from exc
        return {
            "execution_id": document["execution_id"],
            "operation_id": document["operation_id"],
            "work": document["work"],
            "state": document["state"],
            "terminal": document["terminal"],
            "replay_of": replay_of,
            "replays": list(replays),
            "request_digest": document["request_digest"],
            "frozen_inputs": document["frozen_inputs"],
            "artifact": document["artifact"],
        }

    return handler


def _make_execution_replay(
    executions: ExecutionRegistry,
    adapters: Mapping[str, ReplayAdapter],
):
    """execution.replay — §10's replay admission (iter-387): re-run
    a TERMINAL execution's frozen material as a NEW execution
    identity, the new record + artifact linked by replay_of (lineage,
    never identity reuse). The honest gates, in order: the closed
    argument set, the session's ownership (the registry's own law),
    the TERMINAL requirement (an in-flight original rejects — its
    outcome is not yet truth), the kind's replayability (the
    live-gate kinds — model.load/unload — own their re-dispatch; the
    ladder walks live state a replay must not bypass), and the
    frozen envelope's deadline re-resolution (the same §12 ceiling
    law path — the carried budget, never a new one). The frozen
    material is post-validation BY CONSTRUCTION (the §10 freeze at
    the original's admission) — the replay re-runs, it never
    re-validates."""

    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"execution_id"})
        if unknown:
            raise _rejected(
                f"execution.replay: unknown argument(s) {unknown} "
                "(closed set: ['execution_id'])"
            )
        original_id = arguments.get("execution_id")
        if not isinstance(original_id, str) or not original_id:
            raise _rejected(
                "execution.replay: execution_id must be a non-empty str"
            )
        session_id = context.session.session_id if context.session else ""
        try:
            source = executions.document(original_id, session_id)
        except RegistryError as exc:
            raise _rejected(f"execution.replay: {exc}") from exc
        if not source["terminal"]:
            raise _rejected(
                f"execution.replay: execution {original_id!r} is still "
                f"in flight ({source['state']}) — replay admits only "
                "terminal executions"
            )
        work_kind = str(source["work"])
        adapter = adapters.get(work_kind)
        if adapter is None:
            raise _rejected(
                f"execution.replay: work kind {work_kind!r} is not "
                "replayable (the live-gate kinds own their re-dispatch; "
                f"replayable: {sorted(adapters)})"
            )
        frozen = {
            str(key): str(value)
            for key, value in source["frozen_inputs"]
        }
        raw_seconds = frozen.get("deadline_seconds")
        if raw_seconds is None:
            raise _rejected(
                f"execution.replay: execution {original_id!r}: the "
                "frozen envelope carries no deadline_seconds (the "
                "admission freeze law) — the budget cannot re-resolve"
            )
        try:
            seconds = executions.resolve_deadline_seconds(
                float(raw_seconds)
            )
            work = adapter(frozen)
            new_id = executions.admit(
                operation_id="execution.replay",
                session_id=session_id,
                work_kind=work_kind,
                frozen_inputs=frozen,
                deadline_seconds=seconds,
                replay_of=original_id,
            )
        except (RegistryError, ValueError) as exc:
            raise _rejected(f"execution.replay: {exc}") from exc
        executions.launch(new_id, work)
        if context.effects is not None:
            context.effects.effect(
                {
                    "effect": "RUN_REPLAYED",
                    "execution_id": new_id,
                    "work": work_kind,
                    "replay_of": original_id,
                }
            )
        return {
            "replayed_from": original_id,
            "execution_id": new_id,
            "work": work_kind,
            "deadline_seconds": seconds,
            "state": "STARTING",
        }

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
