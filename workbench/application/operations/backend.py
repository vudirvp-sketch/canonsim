"""The backend row (wb-6, the app spec §§4.1/11.1/19/20/29 — the
family's sixth row, app §32 step 7).

The law this row closes: **chat.send's consumer IS the backend** — the
admission law's wb-5 deferral («chat.send honestly NOT registered —
its consumer is the backend row»). The owner's «подключи llama.cpp»
call opens the row: the llama.cpp backend arrives as ONE typed port
injected at the composition root. The workbench application stays
engine-agnostic and network-free — INV-4's two-surface form untouched
(the physical transport is `cli/engine.py`'s `LlamaServerClient`,
which satisfies the port structurally; `workbench/` never imports it —
the application-entry rows own the physical wiring, and the §27
envelope holds: no `cli/`, no engine, no network here).

The port (§4.1: "`adapters/llama_cpp` may be a future typed boundary
but cannot create a second physical network surface"):

```text
BackendPort = props() + chat() + load_model() + unload_model()
```

every member carrying a registered consumer this row. The failure
contract is the adapter's own (D-192 D1): a raised exception with a
`cause` in {"unavailable", "http", "malformed"} — §12.1's vocabulary
at the model layer: "unavailable" = the outcome is UNKNOWN (the call
was sent, nothing came back), "http"/"malformed" = the backend's
observed terminal answer.

§11.1's ATTACHED form: the operator owns the llama-server process
(D-192 D1 — the backend process is not application state); the
workbench observes (props) and requests (chat/load/unload). The
MANAGED half (spawn/stop) landed at wb-8 OUTSIDE this module — the
process mechanics in `workbench/platform/llama_process.py`, the
lifecycle policy at the composition root (workbench_app.py --managed):
the operations still see ONLY this port's shape, so both ownership
forms ride the same handlers.

chat.send (§8 + §19.1 + §12, over the wb-5 run registry):

```text
REQUESTED = the caller's messages/temperature/max_tokens
ACCEPTED  = validated in range, the row's defaults resolved (the
            round-4 prose recipe: temperature 0.8, max_tokens 512)
EFFECTIVE = the frozen inputs (§10 — admitted BEFORE any side
            effect; the registry's request digest IS the request
            identity at the application layer — the wire bytes are
            the adapter's own business, §19)
OBSERVED  = content + finish_reason + the backend identity (props;
            a failed probe never kills the chat — the identity lands
            "unavailable", the honest note, never a fabricated one)
```

Long-running work returns identity immediately (§8): chat.send admits
+ launches a `chat.completion` execution and returns the execution_id;
run.get (wb-5, already registered) is the read path; the live-events
row (§32 step 6) delivers streaming later. The single blocking port
call is bounded by the transport's own timeout policy (§12: "per-
attempt socket timeout is transport policy"); the cooperative
checkpoints fire where the work CAN yield — entry and post-probe. A
reply landing past the deadline still closes COMPLETED: the deadline
readings ride the run document (nothing fabricated — §13's
preserve-the-complete-output law); a cancellation observed mid-call
closes through the registry's own truthful late-result path
(FAILED_TO_CANCEL, the result recorded).

model.load / model.unload (§20's loading half — "file exists ≠ valid
≠ selected ≠ loading ≠ loaded ≠ active") over the Model ladder
(§11, lifecycles.py's MODEL machine), walked on OBSERVED outcomes —
the application's observation surface folds the backend's replies
(INV-1's own law, applied to the application layer; the in-flight
LOADING/UNLOADING are transit states, never resting ones). wb-11:
BOTH dispatch as RUNS (the chat.send pattern — the owner's
2026-09-26 «молча висят + транспорт результ 13» call over the
freeze chain: a minutes-class managed spawn ran INSIDE the gateway's
coarse dispatch lock, so every concurrent request — model.list,
session.create, app.status — starved past the client's 10s budget
and the whole UI hung silent). The dispatch-side walk stays fast and
honest (validate + the ladder's admission-side SELECTED/ACTIVE gate,
milliseconds under the lock); the minutes-class port call (the
managed spawn + readiness walk, the graceful stop) runs on the
registry's worker thread — and the run's FAILED diagnostics carry
the observed cause (`str(exc)` — §21's diagnostics surface, the
reason ON the run.get wire, never an error_type-only blackout):

```text
load:   DISCOVERED → VALIDATED → SELECTED (admission-side, dispatch)
        then the run, on the reply: LOADING → LOADED → ACTIVE
        (success) or LOADING → FAILED (the backend's observed
        refusal); an "unavailable" outcome rests at SELECTED — the
        unknown-outcome truth, legal to re-load (§12.1's sibling)
unload: ACTIVE (the dispatch gate) then the run: UNLOADING → EVICTED
        on the success reply; any failure leaves ACTIVE — the
        observed still-loaded truth
```

The ladder's honest gap, recorded (D-203): FAILED is terminal with no
re-selection path (only EVICTED → SELECTED exists), so a FAILED model
rejects re-load loudly (DOMAIN_REJECTED) — the owner's ladder
amendment is the recorded open note, never a silent local fix
(AGENTS §11: no silent reconciliation). The replacement path
(§11.1's "prepare new → validate → ready → swap → retire old") is a
later row: loading an ACTIVE model rejects (unload first).

The load-state read surface (`ModelLoadStates.document`) is wired as
the `model.states` READ operation (wb-8 — the frontend Models
surface's registered consumer, frontend §46 Phase A's Models row);
its diagnostic use rides the same document, never a second owner.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Protocol, runtime_checkable

from workbench.api.gateway import (
    Gateway,
    OperationRejected,
    OperationSpec,
)
from workbench.application.operations.execution import (
    ExecutionRegistry,
    RegistryError,
    WorkContext,
)
from workbench.application.operations.lifecycles import (
    LifecycleError,
    transition,
)
from workbench.application.operations.models import (
    ModelRegistry,
    ModelRegistryError,
)

__all__ = [
    "CHAT_DEFAULT_DEADLINE_SECONDS",
    "CHAT_DEFAULT_MAX_TOKENS",
    "CHAT_DEFAULT_TEMPERATURE",
    "CHAT_MAX_MAX_TOKENS",
    "CHAT_ROLES",
    "MODEL_LOAD_DEFAULT_DEADLINE_SECONDS",
    "MODEL_UNLOAD_DEFAULT_DEADLINE_SECONDS",
    "BackendPort",
    "BackendPortError",
    "ModelLoadStates",
    "chat_completion_work",
    "model_load_work",
    "model_unload_work",
    "register_backend_operations",
    "require_backend_port",
]

#: The chat row's ACCEPTED-layer defaults (§19.1's REQUESTED→ACCEPTED
#: resolution — the round-4 prose recipe, the door's own temperatures):
#: the narrator's 0.8 and the prose completion budget 512.
CHAT_DEFAULT_TEMPERATURE = 0.8
CHAT_DEFAULT_MAX_TOKENS = 512

#: The per-request max_tokens ceiling (§26: "bounded requires an
#: explicit ceiling") — rejected, never clamped.
CHAT_MAX_MAX_TOKENS = 4096

#: The chat row's own default deadline (seconds): a local-LLM prose
#: completion at the recipe's budget can outrun the registry's generic
#: 60s default — the row resolves its own (§12's material input).
CHAT_DEFAULT_DEADLINE_SECONDS = 120.0

#: The load run's own default deadline (wb-11): the MANAGED arm's
#: spawn + readiness walk is minutes-class (the composition root's
#: 300s readiness budget + the margin) — the row resolves its own
#: (§12's material input; the caller may still name a tighter one).
MODEL_LOAD_DEFAULT_DEADLINE_SECONDS = 330.0

#: The unload run's own default deadline (wb-11): the managed stop is
#: the bounded graceful TERM → grace(10s) → kill walk — 30s covers it
#: with the margin; the attached arm's transport is 10s single-try.
MODEL_UNLOAD_DEFAULT_DEADLINE_SECONDS = 30.0

#: The chat roles the surface accepts (§18's prompt roles: system |
#: user/chat; assistant = the history form the Chat UI sends).
CHAT_ROLES = frozenset({"system", "user", "assistant"})


@runtime_checkable
class BackendPort(Protocol):
    """The typed llama.cpp seam (§4.1's future boundary, minimally
    closed over this row's four consumers): the effective-state
    evidence (`props`), one chat completion (`chat`), and the
    model-management pair (`load_model`/`unload_model`). The physical
    owner is `cli/engine.py`'s `LlamaServerClient` (INV-4) — satisfied
    structurally, never imported here. Failure contract: a raised
    exception carrying `cause` in {"unavailable", "http", "malformed"}
    (the adapter's D1 mapping; duck-typed, engine-agnostic)."""

    def props(self) -> dict[str, Any]:
        """`/props` — the backend identity evidence: model path,
        build_info (the manifest row's own half)."""
        ...

    def chat(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        grammar: str | None = None,
        temperature: float = CHAT_DEFAULT_TEMPERATURE,
        max_tokens: int = CHAT_DEFAULT_MAX_TOKENS,
    ) -> tuple[str, str]:
        """One chat completion -> (content, finish_reason)."""
        ...

    def load_model(
        self, model_path: str, alias: str | None = None
    ) -> dict[str, Any]:
        """POST /models/load — the model's path + optional alias."""
        ...

    def unload_model(self, model_ref: str) -> dict[str, Any]:
        """POST /models/unload — the load's alias (or path)."""
        ...


class BackendPortError(ValueError):
    """A port-contract violation (construction-time — the composition's
    §6.1 validate-dependencies step, LOUD)."""


def require_backend_port(backend: object) -> None:
    """The §6.1 validate step for the injected backend: every member
    present and callable — a loud CompositionError-side carrier at the
    composition, never a mid-dispatch AttributeError."""
    for name in ("props", "chat", "load_model", "unload_model"):
        member = getattr(backend, name, None)
        if not callable(member):
            raise BackendPortError(
                f"backend port: {name!r} is missing or not callable "
                f"(got {type(member).__name__} on {type(backend).__name__})"
            )


# ------------------------------------------------------------- the model
#                                                              load states


class ModelLoadStates:
    """The Model-lifecycle state owner for the backend family (§11's
    MODEL machine, walked on observed outcomes — the module note).

    One logical_name → one state; the discovery entry gate is the
    `ModelRegistry`'s (the handlers resolve there first); the tracker
    only ever names models the registry resolved. All walks go through
    `lifecycles.transition` — the invalid-transition loudness is the
    module's own law, never bypassed.
    """

    def __init__(self) -> None:
        self._states: dict[str, str] = {}
        self._active: str | None = None

    def state(self, logical_name: str) -> str | None:
        """The current Model-lifecycle state, or None when never
        touched (the read view — never a state mutation)."""
        return self._states.get(logical_name)

    @property
    def active(self) -> str | None:
        """The logical_name of the ACTIVE model (the §20 'expose
        active model' half — at most one this row: the slot is single,
        a second load of anything while one is ACTIVE rejects)."""
        return self._active

    def select(self, logical_name: str) -> None:
        """The admission-side walk: DISCOVERED → VALIDATED → SELECTED
        for a fresh entry; EVICTED → SELECTED the re-selection (the
        ladder's own return path); an already-SELECTED name is the
        legal retry after an unknown outcome (a no-op — the state
        already names the truth). Anything else raises — the handlers
        pre-check the reachable cases and map them to DOMAIN_REJECTED
        (ACTIVE: unload first; FAILED: the ladder's terminal gap)."""
        current = self._states.get(logical_name)
        if current is None:
            self._states[logical_name] = "DISCOVERED"
            current = "DISCOVERED"
        if current == "SELECTED":
            return
        if current == "DISCOVERED":
            current = _walk(current, "VALIDATED")
        self._states[logical_name] = _walk(current, "SELECTED")

    def settle_load_success(self, logical_name: str) -> None:
        """The observed success fold: SELECTED → LOADING → LOADED →
        ACTIVE (the §20 chain's landing half — LOADING/LOADED are
        transit states; the resting truth is ACTIVE) + the active-slot
        record."""
        current = self._require(logical_name, "SELECTED")
        current = _walk(current, "LOADING")
        current = _walk(current, "LOADED")
        self._states[logical_name] = _walk(current, "ACTIVE")
        self._active = logical_name

    def settle_load_failure(self, logical_name: str, observed: bool) -> None:
        """The observed-failure fold: the backend's terminal answer
        (http/malformed) walks SELECTED → LOADING → FAILED; an
        UNKNOWN outcome ("unavailable") rests at SELECTED — the
        honest §12.1 sibling, legal to re-load."""
        if not observed:
            return
        current = self._require(logical_name, "SELECTED")
        current = _walk(current, "LOADING")
        self._states[logical_name] = _walk(current, "FAILED")

    def settle_unload_success(self, logical_name: str) -> None:
        """The observed eviction fold: ACTIVE → UNLOADING → EVICTED +
        the active-slot clear (an unload failure performs NO walk —
        the model's observed truth is still ACTIVE)."""
        current = self._require(logical_name, "ACTIVE")
        current = _walk(current, "UNLOADING")
        self._states[logical_name] = _walk(current, "EVICTED")
        if self._active == logical_name:
            self._active = None

    def document(self) -> dict[str, object]:
        """The read view (the diagnostic/test surface — the registered
        consumer is a later row, the admission law): the per-model
        states sorted by name + the active slot."""
        return {
            "states": {
                name: self._states[name] for name in sorted(self._states)
            },
            "active": self._active,
        }

    def _require(self, logical_name: str, expected: str) -> str:
        current = self._states.get(logical_name)
        if current != expected:
            raise LifecycleError(
                f"MODEL: model {logical_name!r} is {current!r}, not "
                f"{expected!r} (the handler's pre-check was bypassed — "
                "a composition bug, loud by design)"
            )
        return current


def _walk(current: str, target: str) -> str:
    return transition("MODEL", current, target)


# ------------------------------------------------------------ the chat work


def chat_completion_work(
    port: BackendPort,
    messages: Sequence[Mapping[str, str]],
    temperature: float,
    max_tokens: int,
) -> Mapping[str, object]:
    """The chat work factory (the run family's backend consumer): the
    §19.1 EFFECTIVE→OBSERVED half over the frozen inputs — the §10
    freeze already happened at admission; the work probes the backend
    identity (props — a failed probe never kills the chat), yields at
    its checkpoints, and returns the observed completion. The §10
    provenance's backend half rides the result document (OBSERVED),
    never the artifact (the adapter's manifest stays the physical
    owner's; the application records what it saw)."""

    def work(context: WorkContext) -> Mapping[str, object]:
        context.check()  # the entry checkpoint (§12)
        identity = _backend_identity(port)
        context.check()  # the post-probe yield point
        content, finish_reason = port.chat(
            list(messages),
            grammar=None,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return {
            "content": content,
            "finish_reason": finish_reason,
            "backend": identity,
            "requested": {
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        }

    return work


def _backend_identity(port: BackendPort) -> dict[str, object]:
    """The OBSERVED backend identity (props): model path + build. A
    failed probe is the honest "unavailable" note — the chat itself
    may still succeed (readiness ≠ identity evidence); never a
    fabricated identity, never a silent skip."""
    try:
        props = port.props()
    except Exception as exc:  # noqa: BLE001 — the probe never kills the chat
        return {"probe": "unavailable", "detail": str(exc)}
    model = props.get("model_path") or props.get("model")
    return {
        "model": model if isinstance(model, str) else None,
        "build": props.get("build_info"),
    }


# ---------------------------------------------------------------- handlers


def _rejected(reason: str) -> OperationRejected:
    return OperationRejected("DOMAIN_REJECTED", reason)


def _validate_chat_arguments(
    arguments: Mapping[str, object],
    temperature_default: Callable[[], float] | None = None,
) -> tuple[list[dict[str, str]], float, int]:
    """chat.send's REQUESTED→ACCEPTED layer: the closed argument set,
    the messages shape (a non-empty list of {role, content} over the
    closed role set), the temperature range [0, 2], the max_tokens
    range [1, CHAT_MAX_MAX_TOKENS] — rejected loud, never clamped
    (§19.1's clamping machinery is a later row; the honest minimal is
    a closed validated surface). The deadline rides separately (§12's
    own resolution, the handler's).

    wb-9: an ABSENT temperature resolves through the injected BASE
    provider (the launch-settings store's temperature — §19.1's
    BASE PROFILE layer) when one is wired, else the row's own
    constant; the caller's EXPLICIT value always wins (the
    call-local override layer)."""
    unknown = sorted(
        set(arguments)
        - {"messages", "temperature", "max_tokens", "deadline_seconds"}
    )
    if unknown:
        raise _rejected(
            f"chat.send: unknown argument(s) {unknown} "
            "(closed set: ['deadline_seconds', 'messages', "
            "'max_tokens', 'temperature'])"
        )
    raw_messages = arguments.get("messages")
    if not isinstance(raw_messages, list) or not raw_messages:
        raise _rejected(
            "chat.send: messages must be a non-empty list of "
            "{role, content} objects"
        )
    messages: list[dict[str, str]] = []
    for index, item in enumerate(raw_messages):
        if not isinstance(item, Mapping) or set(item) != {"role", "content"}:
            raise _rejected(
                f"chat.send: messages[{index}] must be exactly "
                "{role, content}"
            )
        role = item["role"]
        content = item["content"]
        if role not in CHAT_ROLES:
            raise _rejected(
                f"chat.send: messages[{index}].role {role!r} is not "
                f"one of {sorted(CHAT_ROLES)}"
            )
        if not isinstance(content, str) or not content:
            raise _rejected(
                f"chat.send: messages[{index}].content must be a "
                "non-empty str"
            )
        messages.append({"role": str(role), "content": content})
    raw_temperature = arguments.get("temperature")
    if raw_temperature is None:
        temperature = (
            temperature_default()
            if temperature_default is not None
            else CHAT_DEFAULT_TEMPERATURE
        )
        if (
            isinstance(temperature, bool)
            or not isinstance(temperature, (int, float))
            or not 0.0 <= float(temperature) <= 2.0
        ):
            raise _rejected(
                "chat.send: the resolved default temperature is not a "
                f"number in [0, 2] (got {temperature!r}) — a settings "
                "store contract violation"
            )
        temperature = float(temperature)
    elif (
        isinstance(raw_temperature, bool)
        or not isinstance(raw_temperature, (int, float))
        or not 0.0 <= float(raw_temperature) <= 2.0
    ):
        raise _rejected(
            "chat.send: temperature must be a number in [0, 2] "
            f"(got {raw_temperature!r})"
        )
    else:
        temperature = float(raw_temperature)
    raw_max_tokens = arguments.get("max_tokens")
    if raw_max_tokens is None:
        max_tokens = CHAT_DEFAULT_MAX_TOKENS
    elif (
        isinstance(raw_max_tokens, bool)
        or not isinstance(raw_max_tokens, int)
        or not 1 <= raw_max_tokens <= CHAT_MAX_MAX_TOKENS
    ):
        raise _rejected(
            f"chat.send: max_tokens must be an int in "
            f"[1, {CHAT_MAX_MAX_TOKENS}] (got {raw_max_tokens!r})"
        )
    else:
        max_tokens = raw_max_tokens
    return messages, temperature, max_tokens


def _make_chat_send(
    executions: ExecutionRegistry,
    port: BackendPort,
    temperature_default: Callable[[], float] | None = None,
):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        messages, temperature, max_tokens = _validate_chat_arguments(
            arguments, temperature_default
        )
        # §12: one absolute deadline per logical operation — the
        # caller's explicit value or the row's own default (the
        # registry's ceiling law applies, never a silent clamp)
        try:
            seconds = executions.resolve_deadline_seconds(
                arguments.get("deadline_seconds")
                if arguments.get("deadline_seconds") is not None
                else CHAT_DEFAULT_DEADLINE_SECONDS
            )
        except RegistryError as exc:
            raise _rejected(f"chat.send: {exc}") from exc
        # §10: the freeze BEFORE any side effect — the frozen inputs
        # ARE the request identity at the application layer (§19:
        # the wire bytes stay the adapter's).
        frozen = {
            "deadline_seconds": str(seconds),
            "max_tokens": str(max_tokens),
            "messages": json.dumps(
                messages, sort_keys=True, separators=(",", ":")
            ),
            "temperature": repr(temperature),
        }
        session_id = context.session.session_id if context.session else ""
        execution_id = executions.admit(
            operation_id=context.operation_id,
            session_id=session_id,
            work_kind="chat.completion",
            frozen_inputs=frozen,
            deadline_seconds=seconds,
        )
        work = chat_completion_work(port, messages, temperature, max_tokens)
        executions.launch(execution_id, work)
        if context.effects is not None:
            context.effects.effect(
                {
                    "effect": "CHAT_DISPATCHED",
                    "execution_id": execution_id,
                    "work": "chat.completion",
                }
            )
        return {
            "deadline_seconds": seconds,
            "execution_id": execution_id,
            "state": "STARTING",
            "work": "chat.completion",
        }

    return handler


def _cause(exc: BaseException) -> str:
    """The port failure's cause (the adapter's D1 vocabulary,
    duck-typed): anything without a `cause` is "malformed"-class —
    the backend's observed terminal answer (an exception the port
    raised on its own is a contract answer, never an unknown)."""
    cause = getattr(exc, "cause", None)
    return cause if isinstance(cause, str) else "malformed"


def model_load_work(
    models: ModelRegistry,
    loads: ModelLoadStates,
    port: BackendPort,
    logical_name: str,
    in_flight: dict[str, str],
):
    """The load run's work factory (wb-11 — the minutes-class arm
    OFF the dispatch lock): re-resolve (a vanished file between
    dispatch and the work is the honest late failure — the ladder
    rests SELECTED, a deliberate re-load stays legal), then the port
    call (the managed spawn + readiness walk or the attached load),
    then the observed fold. The failure raise rides the registry's
    FAILED diagnostics — the reason ON the run.get wire (§21), never
    an error_type-only blackout. The `in_flight` map is the handler's
    own (one load run per name at a time); the finally-pop is this
    side's half of that contract."""

    def work(context: WorkContext) -> Mapping[str, object]:
        try:
            context.check()  # the entry checkpoint (§12)
            try:
                path = models.resolve(logical_name)
            except ModelRegistryError as exc:
                loads.settle_load_failure(
                    logical_name, observed=False
                )  # the pre-backend truth: SELECTED, the re-load legal
                raise RuntimeError(
                    f"model.load run: the model vanished since dispatch — {exc}"
                ) from exc
            try:
                reply = port.load_model(str(path), alias=logical_name)
            except Exception as exc:
                loads.settle_load_failure(
                    logical_name, observed=_cause(exc) != "unavailable"
                )
                raise  # the run closes FAILED — the observed cause rides
                # the diagnostics (§21), the ladder rests at its truth
            if reply.get("success") is False:
                # the backend answered success:false at HTTP 200 — the
                # observed refusal (the stub pins the shape; build-
                # sensitive, the module note)
                loads.settle_load_failure(logical_name, observed=True)
                raise RuntimeError(
                    "model.load run: the backend refused the load "
                    f"({json.dumps(reply, sort_keys=True)})"
                )
            loads.settle_load_success(logical_name)
            return {
                "logical_name": logical_name,
                "location": str(path),
                "reply": dict(reply),
                "state": "ACTIVE",
            }
        finally:
            in_flight.pop(logical_name, None)

    return work


def _make_model_load(
    models: ModelRegistry,
    loads: ModelLoadStates,
    port: BackendPort,
    executions: ExecutionRegistry,
):
    # One load run per name at a time (the handler's own admission
    # guard): a name resting SELECTED after an unknown outcome stays
    # RE-LOADABLE (§12.1's sibling) — only a genuinely in-flight run
    # rejects; the work's finally-pop is the clear half.
    in_flight: dict[str, str] = {}

    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"logical_name", "deadline_seconds"})
        if unknown:
            raise _rejected(
                f"model.load: unknown argument(s) {unknown} "
                "(closed set: ['deadline_seconds', 'logical_name'])"
            )
        logical_name = arguments.get("logical_name")
        if not isinstance(logical_name, str) or not logical_name:
            raise _rejected(
                "model.load: logical_name must be a non-empty str"
            )
        # §20's entry gate: discovery first (the registry's own law).
        # The path itself is the WORK's own re-resolve (a vanished
        # file between dispatch and the work is the honest late
        # failure) — the dispatch needs only the gate's verdict.
        try:
            models.resolve(logical_name)
        except ModelRegistryError as exc:
            raise _rejected(f"model.load: {exc}") from exc
        current = loads.state(logical_name)
        if current == "ACTIVE":
            raise _rejected(
                f"model.load: {logical_name!r} is already ACTIVE — "
                "unload first (the replacement path is a later row)"
            )
        if current == "FAILED":
            raise _rejected(
                f"model.load: {logical_name!r} is FAILED — the Model "
                "ladder's FAILED is terminal (no re-selection path; "
                "the recorded ladder gap, D-203)"
            )
        active = loads.active
        if active is not None and active != logical_name:
            # the single-slot law (ModelLoadStates.active's own doc):
            # at most one ACTIVE this row — a second load while the
            # slot holds rejects (the swap path is a later row).
            raise _rejected(
                f"model.load: {active!r} is ACTIVE — unload first "
                "(the slot is single this row; the replacement path "
                "is a later row)"
            )
        flight = in_flight.get(logical_name)
        if flight is not None:
            raise _rejected(
                f"model.load: {logical_name!r} is already loading "
                f"(run {flight[:12]}) — run.get names the walk; a "
                "re-load is legal once it lands"
            )
        loads.select(logical_name)  # the admission-side walk (fast)
        # §12: the row's own default deadline — the managed readiness
        # walk is minutes-class; the caller may name a tighter one.
        try:
            seconds = executions.resolve_deadline_seconds(
                arguments.get("deadline_seconds")
                if arguments.get("deadline_seconds") is not None
                else MODEL_LOAD_DEFAULT_DEADLINE_SECONDS
            )
        except RegistryError as exc:
            raise _rejected(f"model.load: {exc}") from exc
        frozen = {
            "deadline_seconds": str(seconds),
            "logical_name": logical_name,
        }
        session_id = context.session.session_id if context.session else ""
        execution_id = executions.admit(
            operation_id=context.operation_id,
            session_id=session_id,
            work_kind="model.load",
            frozen_inputs=frozen,
            deadline_seconds=seconds,
        )
        work = model_load_work(models, loads, port, logical_name, in_flight)
        in_flight[logical_name] = execution_id
        executions.launch(execution_id, work)
        if context.effects is not None:
            context.effects.effect(
                {
                    "effect": "MODEL_LOAD_DISPATCHED",
                    "execution_id": execution_id,
                    "logical_name": logical_name,
                    "work": "model.load",
                }
            )
        return {
            "deadline_seconds": seconds,
            "execution_id": execution_id,
            "logical_name": logical_name,
            "state": "STARTING",
            "work": "model.load",
        }

    return handler


def model_unload_work(
    loads: ModelLoadStates, port: BackendPort, logical_name: str
):
    """The unload run's work factory (wb-11): the graceful stop /
    attached unload on the worker thread — the observed eviction fold
    on success; a failure performs NO walk (the observed truth is
    still ACTIVE) and the cause rides the FAILED diagnostics (§21)."""

    def work(context: WorkContext) -> Mapping[str, object]:
        context.check()  # the entry checkpoint (§12)
        try:
            reply = port.unload_model(logical_name)
        except Exception:
            raise  # no ladder walk — the run's FAILED diagnostics
            # carry the cause; the model's truth is still ACTIVE
        loads.settle_unload_success(logical_name)
        return {
            "logical_name": logical_name,
            "reply": dict(reply),
            "state": "EVICTED",
        }

    return work


def _make_model_unload(
    loads: ModelLoadStates,
    port: BackendPort,
    executions: ExecutionRegistry,
):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"logical_name", "deadline_seconds"})
        if unknown:
            raise _rejected(
                f"model.unload: unknown argument(s) {unknown} "
                "(closed set: ['deadline_seconds', 'logical_name'])"
            )
        logical_name = arguments.get("logical_name")
        if not isinstance(logical_name, str) or not logical_name:
            raise _rejected(
                "model.unload: logical_name must be a non-empty str"
            )
        if loads.state(logical_name) != "ACTIVE":
            raise _rejected(
                f"model.unload: {logical_name!r} is not ACTIVE "
                f"(state: {loads.state(logical_name)!r}) — nothing "
                "active to unload"
            )
        try:
            seconds = executions.resolve_deadline_seconds(
                arguments.get("deadline_seconds")
                if arguments.get("deadline_seconds") is not None
                else MODEL_UNLOAD_DEFAULT_DEADLINE_SECONDS
            )
        except RegistryError as exc:
            raise _rejected(f"model.unload: {exc}") from exc
        frozen = {
            "deadline_seconds": str(seconds),
            "logical_name": logical_name,
        }
        session_id = context.session.session_id if context.session else ""
        execution_id = executions.admit(
            operation_id=context.operation_id,
            session_id=session_id,
            work_kind="model.unload",
            frozen_inputs=frozen,
            deadline_seconds=seconds,
        )
        work = model_unload_work(loads, port, logical_name)
        executions.launch(execution_id, work)
        if context.effects is not None:
            context.effects.effect(
                {
                    "effect": "MODEL_UNLOAD_DISPATCHED",
                    "execution_id": execution_id,
                    "logical_name": logical_name,
                    "work": "model.unload",
                }
            )
        return {
            "deadline_seconds": seconds,
            "execution_id": execution_id,
            "logical_name": logical_name,
            "state": "STARTING",
            "work": "model.unload",
        }

    return handler


def _make_model_states(loads: ModelLoadStates):
    def handler(context) -> Mapping[str, object]:
        if context.arguments:
            raise _rejected(
                f"model.states: takes no arguments "
                f"({sorted(context.arguments)})"
            )
        return loads.document()

    return handler


def register_backend_operations(
    gateway: Gateway,
    executions: ExecutionRegistry,
    models: ModelRegistry,
    backend: object,
    *,
    temperature_default: Callable[[], float] | None = None,
) -> ModelLoadStates:
    """The backend family's wiring (called by the composition root —
    §6.1's single-owner law: this function never constructs the
    registries, it only wires the three operations over them). The
    port validation happens HERE (the §6.1 validate step); the
    returned `ModelLoadStates` is the family's state owner (the
    composition hands it to the caller's handle). wb-9: the optional
    `temperature_default` provider (the launch-settings store's
    BASE layer) resolves chat.send's absent-temperature default —
    injected, never imported."""
    require_backend_port(backend)
    port: BackendPort = backend  # structural — validated above
    loads = ModelLoadStates()
    gateway.register(
        OperationSpec(
            name="chat.send",
            kind="MUTATION",
            handler=_make_chat_send(executions, port, temperature_default),
            session_scoped=True,
            description=(
                "one chat completion over the backend port (§8/§19.1 — "
                "admits a chat.completion run, returns the execution "
                "identity immediately)"
            ),
        )
    )
    gateway.register(
        OperationSpec(
            name="model.load",
            kind="MUTATION",
            handler=_make_model_load(models, loads, port, executions),
            session_scoped=True,
            description=(
                "§20's loading half as a RUN (wb-11): the fast "
                "dispatch walks the ladder to SELECTED and admits a "
                "model.load execution — the minutes-class port call "
                "runs off the dispatch lock; run.get is the poll path"
            ),
        )
    )
    gateway.register(
        OperationSpec(
            name="model.unload",
            kind="MUTATION",
            handler=_make_model_unload(loads, port, executions),
            session_scoped=True,
            description=(
                "§20's unload half as a RUN (wb-11): the graceful "
                "stop / attached unload rides the worker thread — "
                "ACTIVE → EVICTED observed on the run's terminal"
            ),
        )
    )
    gateway.register(
        OperationSpec(
            name="model.states",
            kind="READ",
            handler=_make_model_states(loads),
            description=(
                "the Model-lifecycle read view (§11's MODEL machine): "
                "the per-model states + the active slot — the frontend "
                "Models surface's registered consumer (frontend §46 "
                "Phase A's Models row, wb-8)"
            ),
        )
    )
    return loads
