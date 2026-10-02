"""The gateway dispatch core (wb-4, the app spec §§4.1/8/12/13 — the
family's fourth row).

The law: **one inbound Workbench gateway over application
operations** (§33's checklist row) — this module is its semantic
owner, and it is SOCKET-FREE (G1): the delivery surface
(`transport.py`) calls the SAME `dispatch_document` a CLI/GUI caller
would call directly; the parity is the packet's byte-diff proof.

The dispatch pipeline (G2/G4 — one core, every delivery surface):

```text
identity -> authenticate -> resolve operation -> validate shape
-> idempotency -> session/revision/lease guard -> invoke
-> commit effects
```

- authenticate: AUTH_FAILED (missing/wrong credential when auth is
  required) / AUTHZ_DENIED (the credential's scope denies THIS
  operation) — constant-time comparison (`hmac.compare_digest`), the
  token never recorded (G6/§21).
- resolve + shape: DOMAIN_REJECTED — unknown operation, malformed
  arguments, a mutation without `client_request_id`, a session-scoped
  operation without a resolvable session.
- idempotency (mutations, §12.2): the recorded-outcome replay — the
  same `client_request_id` + the same material digest returns the
  ORIGINAL outcome (one effect, §30's row, `duplicate=True`); a
  conflicting reuse (same key, different material) is
  DUPLICATE_REQUEST.
- revision/lease: STALE_REVISION (§12.2's CAS — the mutation's
  `expected_revision` must equal the session's CURRENT revision; a
  stale writer cannot mutate newer state) / LEASE_EXPIRED (§8's
  exclusive-control token — a lease not currently valid-for-use).
- invoke + outcome (§12.1, G4): a READ raising -> RUNTIME_FAILED (a
  known terminal failure — nothing was sent that could take effect);
  a MUTATION raising after admission -> SENT_OUTCOME_UNKNOWN (the
  ambiguity honored, the UNKNOWN recorded so the blind retry is
  blocked — a retry replays the recorded UNKNOWN, never re-attempts).
- commit: the revision bump + the ordered event append (§13) happen
  under the dispatch lock, together with the idempotency record —
  one admission, one effect, one event.

Ordered events (G5): per-session sequence from 1, no clock in any
identity; `session.events` is the reconnect arm (§13): replay from
`since_sequence` while retained, else RESYNC_REQUIRED + the bounded
current snapshot. Retention is an explicit ceiling (G5/§26:
`retention_events`), FIFO beyond it.

Live delivery (§13's one-way event direction, iter-305): `subscribe`
is the push channel the SSE binding translates — the SAME ordered
stream `session.events` replays on demand. The core stays socket-
free (G1): a `Subscription` is a bounded per-subscriber delivery
queue fanned out under the dispatch lock at `_emit` time; a slow
consumer overflows OBSERVABLY (the channel closes with the terminal,
the retained stream is never touched — the canonical record never
drops, the derived delivery channel may). The replay/live boundary
is gapless by construction: `subscribe` runs under the same coarse
lock as `_emit`, so the replay window ends at `last_sequence` and
the live queue starts at `last_sequence + 1` — no gap, no duplicate.

Session translation (§4.1: the gateway owns it): the in-memory seed
(session.create/get/attach/detach/events + app.status) — IN-MEMORY
by contract (G2: restorable sessions wait for the persistence rows);
session_id derives from the creation request's material (G6 —
deterministic, retry-stable). Sessions and idempotency records live
with the process; the durable stores are later rows' own contracts.

Registered operations (`register`, §6.1's composition-root wiring
point): typed `OperationSpec`s — wb-5+ grows the real families on
this seam; a registered MUTATION's effect surface in wb-4 is its
recorded outcome (the admission law: the world-state effect API
arrives with its first real consumer). No God Object (§2.1): the
gateway owns translation and admission, never operation semantics.

Concurrency: one coarse dispatch lock (threading.Lock) — every
dispatch, effect, and sequence increment serializes; the resource-
admission/lifecycle rows (§32 step 2) own any finer policy.
"""

from __future__ import annotations

import hmac
import threading
from collections import deque
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace

from workbench.api.contract import (
    EXPOSURES,
    GATEWAY_SCHEMA_IDENTITY,
    OPERATION_KINDS,
    REJECTIONS,
    EventEnvelope,
    GatewayContractError,
    RequestEnvelope,
    ResponseDocument,
    canonical_json,
    require_operation_name,
)
from workbench.application.clock import AppClock
from workbench.application.identity import content_digest

#: The lease default (§8: "a short-lived lease token") — seconds on
#: the MONOTONIC clock (§12: the deadline domain for retry/lease).
DEFAULT_LEASE_SECONDS = 30.0

#: The per-session retained-event ceiling (G5/§26: bounded with an
#: explicit ceiling — beyond it, reconnect answers RESYNC_REQUIRED).
DEFAULT_RETENTION_EVENTS = 256

#: The default per-subscriber live-delivery buffer (§13's bounded
#: buffer, §26's explicit ceiling): the events a subscriber may lag
#: behind before the channel overflows and closes with the terminal.
DEFAULT_STREAM_BUFFER_EVENTS = 64

#: The subscription's open modes (§13's dual answer — the same two
#: lanes `session.events` answers): REPLAY (the retained window
#: after the cursor) or RESYNC (the cursor fell out of retention —
#: the bounded current snapshot, then the live tail).
SUBSCRIPTION_MODES: frozenset[str] = frozenset({"REPLAY", "RESYNC"})

#: The live channel's states: OPEN (receiving), OVERFLOW (the
#: bounded buffer filled — drain, then the terminal), CLOSED (no
#: further delivery, idempotent).
SUBSCRIPTION_STATES: frozenset[str] = frozenset(
    {"OPEN", "OVERFLOW", "CLOSED"}
)

#: The framed server-close reasons (§13/§25): the members that may
#: ride a `stream.close` frame. `CLIENT` closes a channel without a
#: frame (the consumer is gone — there is nobody to tell).
STREAM_CLOSE_REASONS: frozenset[str] = frozenset({"SHUTDOWN"})

#: The auth scope wildcard.
SCOPE_WILDCARD = "*"


class GatewayError(ValueError):
    """A gateway construction/config violation — LOUD, before any
    request is served (the exposure law's start-time half, G3)."""


@dataclass(frozen=True)
class GatewayCredential:
    """One gateway credential (§8/§21): the secret token (compared
    constant-time, never recorded), the principal it names, and the
    operation scope (`*` = every operation, else explicit names)."""

    token: str
    principal: str
    allowed_operations: frozenset[str] = frozenset({SCOPE_WILDCARD})

    def __post_init__(self) -> None:
        if not isinstance(self.token, str) or not self.token:
            raise GatewayError("credential: a non-empty token")
        if not isinstance(self.principal, str) or not self.principal:
            raise GatewayError("credential: a non-empty principal")
        for name in self.allowed_operations:
            if name != SCOPE_WILDCARD and "." not in name:
                raise GatewayError(
                    f"credential {self.principal!r}: scope entry "
                    f"{name!r} is not the family.member form or '*'"
                )


@dataclass(frozen=True)
class GatewayConfig:
    """The gateway's construction-time policy (G3): the exposure axis
    and its start law, the auth mode, the lease window, the retention
    ceiling.

    The §30/§33 law is executable HERE: non-loopback exposure cannot
    start without auth — `GatewayConfig(exposure="LAN")` without
    `auth_required` raises at construction, never at request time.
    The shipped transport binds loopback hosts only; the LAN/TUNNEL
    bindings are future rows with their own consumers (G3).
    """

    exposure: str = "LOOPBACK"
    auth_required: bool = False
    credentials: tuple[GatewayCredential, ...] = ()
    lease_seconds: float = DEFAULT_LEASE_SECONDS
    retention_events: int = DEFAULT_RETENTION_EVENTS
    stream_buffer_events: int = DEFAULT_STREAM_BUFFER_EVENTS

    def __post_init__(self) -> None:
        if self.exposure not in EXPOSURES:
            raise GatewayError(
                f"exposure {self.exposure!r}: the closed set "
                f"{sorted(EXPOSURES)}"
            )
        if self.exposure != "LOOPBACK" and not self.auth_required:
            raise GatewayError(
                f"exposure {self.exposure!r} cannot start without auth "
                "(§30/§33 — non-loopback exposure is authenticated/"
                "authorized or it does not start)"
            )
        if self.auth_required and not self.credentials:
            raise GatewayError(
                "auth_required with no credentials — nothing could "
                "ever authenticate"
            )
        if (
            not isinstance(self.lease_seconds, (int, float))
            or isinstance(self.lease_seconds, bool)
            or self.lease_seconds <= 0
        ):
            raise GatewayError("lease_seconds: a positive number")
        if (
            isinstance(self.retention_events, bool)
            or not isinstance(self.retention_events, int)
            or self.retention_events < 1
        ):
            raise GatewayError("retention_events: an int >= 1")
        if (
            isinstance(self.stream_buffer_events, bool)
            or not isinstance(self.stream_buffer_events, int)
            or self.stream_buffer_events < 1
        ):
            raise GatewayError("stream_buffer_events: an int >= 1")
        if self.stream_buffer_events > self.retention_events:
            # §13's overflow invariant: a consumer that overflowed
            # lags at most `stream_buffer_events` behind the live
            # edge, and retention holds at least that many events —
            # so a reconnect from its last received sequence ALWAYS
            # replays (never a second resync). The constraint is
            # construction law, never a runtime clamp.
            raise GatewayError(
                "stream_buffer_events cannot exceed retention_events "
                "(the overflow-reconnect-always-replays invariant)"
            )


@dataclass(frozen=True)
class SessionView:
    """The frozen session snapshot handed to operation handlers (the
    read view — handlers never touch the registry)."""

    session_id: str
    revision: int
    attached: bool


@dataclass(frozen=True)
class OperationContext:
    """What an operation handler receives: the operation name, the
    dispatch's logical operation identity, the idempotency key, the
    validated arguments, the resolved session view when
    session-scoped, the wired clock (§17 — handlers read the domains
    through it, never the host clock), and — for session-scoped
    operations — the event surface (`effects`, wb-5: the handler's
    OPERATION_EFFECT declaration path into §13's ordered stream)."""

    operation: str
    operation_id: str
    client_request_id: str | None
    arguments: Mapping[str, object]
    session: SessionView | None
    clock: AppClock
    effects: OperationEffects | None = None


#: The registered handler signature: context -> result document.
OperationHandler = Callable[[OperationContext], Mapping[str, object]]


class OperationEffects:
    """The REGISTERED operations' event surface (wb-5): one method,
    `effect(payload)`, appending an OPERATION_EFFECT event into the
    dispatching session's ordered stream (§13 — the gateway owns the
    stream and its sequence; the handler only declares the effect).

    Constructed by the gateway for session-scoped operations only;
    non-session-scoped operations get None (no session, no stream —
    there is nothing to append to, and using it is a loud None
    dereference, never a quiet drop)."""

    __slots__ = ("_emit_effect",)

    def __init__(
        self, emit_effect: Callable[[Mapping[str, object]], None]
    ) -> None:
        self._emit_effect = emit_effect

    def effect(self, payload: Mapping[str, object]) -> None:
        """Declare one operation effect: the payload must be JSON-safe
        (the EventEnvelope's own closed-document law — a violation is
        loud at the append, never a silent drop)."""
        self._emit_effect(dict(payload))


@dataclass(frozen=True)
class OperationSpec:
    """One registered operation (§6.1's composition-root wiring
    point, G2): the name (family.member), the kind (READ vs
    MUTATION — the dispatch-outcome mapping rides it), the handler,
    and the guard flags (session-scoped, revision-guarded,
    lease-guarded)."""

    name: str
    kind: str
    handler: OperationHandler
    session_scoped: bool = False
    requires_revision: bool = False
    requires_lease: bool = False
    description: str = ""

    def __post_init__(self) -> None:
        require_operation_name(self.name)
        if self.kind not in OPERATION_KINDS:
            raise GatewayError(
                f"operation {self.name!r}: kind {self.kind!r} is not "
                f"{sorted(OPERATION_KINDS)}"
            )
        if not callable(self.handler):
            raise GatewayError(
                f"operation {self.name!r}: the handler must be callable"
            )
        if self.kind == "READ" and (self.requires_revision or self.requires_lease):
            raise GatewayError(
                f"operation {self.name!r}: a READ takes no revision/"
                "lease guards"
            )


@dataclass
class _Session:
    """The in-memory session record (gateway-private; the read view
    is the frozen SessionView)."""

    session_id: str
    revision: int = 0
    attached: bool = False
    created_observed_at: float = 0.0
    last_sequence: int = 0
    lease_token: str | None = None
    lease_expires_monotonic: float | None = None


@dataclass(frozen=True)
class _RecordedOutcome:
    """The idempotency record (§12.2): the request's material digest
    + the terminal response — a retry replays it, a conflicting reuse
    collides with it."""

    material_digest: str
    response: ResponseDocument


class _Rejected(Exception):
    """The pipeline's internal rejection carrier — caught at the
    dispatch boundary and translated into the ResponseDocument (the
    rejection vocabulary is closed; the reason is a safe literal)."""

    def __init__(self, rejection: str, reason: str) -> None:
        super().__init__(reason)
        self.rejection = rejection
        self.reason = reason


class OperationRejected(_Rejected):
    """The REGISTERED operations' public rejection carrier (wb-5):
    raise this from a handler to reject with a member of the closed
    §8 vocabulary — the same pipeline path the builtins ride (the
    `except _Rejected` arm passes it through UNMAPPED: a rejection is
    NOT_SENT, never a §12.1 dispatch outcome), the membership
    enforced at raise time (an invented member is a construction
    bug, loud)."""

    def __init__(self, rejection: str, reason: str) -> None:
        if rejection not in REJECTIONS:
            raise GatewayError(
                f"OperationRejected: {rejection!r} is not a member of "
                f"the closed rejection set {sorted(REJECTIONS)}"
            )
        super().__init__(rejection, reason)


@dataclass(frozen=True)
class StreamEvent:
    """One live delivery item: an ordered session event (§13),
    pushed at `_emit` time under the dispatch lock."""

    envelope: EventEnvelope


@dataclass(frozen=True)
class StreamOverflow:
    """The bounded buffer's observable terminal (§13): the consumer
    fell further behind than `stream_buffer_events`; the queued
    events drained first, then this terminal closes the channel.
    `last_sequence` is the session's newest sequence at the overflow
    moment — the consumer reconnects from ITS last received id."""

    last_sequence: int


@dataclass(frozen=True)
class StreamClosed:
    """The channel's closed terminal: the gateway stopped (the
    framed `reason` is a STREAM_CLOSE_REASONS member) or the consumer
    side ended the channel (`CLIENT` — unframed: nobody to tell).
    Idempotent on repeated pulls."""

    reason: str


@dataclass(frozen=True)
class StreamRejection:
    """The subscribe answer's rejected lane: a member of the closed
    §8 rejection vocabulary plus its reason — the same lane a POST
    dispatch would answer with (the verdict rides the stream surface,
    never a fabricated delivery failure)."""

    rejection: str
    reason: str

    def __post_init__(self) -> None:
        if self.rejection not in REJECTIONS:
            raise GatewayError(
                f"StreamRejection: {self.rejection!r} is not a member "
                f"of the closed rejection set {sorted(REJECTIONS)}"
            )
        if not isinstance(self.reason, str) or not self.reason:
            raise GatewayError("StreamRejection: a non-empty reason")


#: The live channel's pull result: an event, a terminal, or None (the
#: heartbeat wake — nothing arrived within the timeout).
StreamItem = StreamEvent | StreamOverflow | StreamClosed


class Subscription:
    """One subscriber's bounded live-delivery channel over a
    session's ordered stream (§13 — the core half of the SSE row,
    socket-free by construction like everything else here).

    The gateway constructs it under the dispatch lock (the gapless
    replay/live boundary); the delivery surface (the loopback
    transport's writer thread, a future CLI parity consumer) then
    PULLS via `next_item(timeout)` and ends with `close()`.

    Boundedness (§26): the pending queue never exceeds the
    construction ceiling — a full queue at push time flips the
    channel to OVERFLOW observably (the terminal item), the queued
    events still drain in order, and the retained stream itself is
    never touched: canonical data is never silently dropped, a
    derived delivery channel may close loudly.

    Lock discipline: `_push`/`_close` run under the GATEWAY's lock
    and take only the condition (gateway -> cond, one-way nesting);
    `next_item`/`close` take the condition alone — nothing ever
    acquires the gateway lock while holding the condition.
    """

    def __init__(
        self,
        *,
        session_id: str,
        clock: AppClock,
        ceiling: int,
        mode: str,
        replay: tuple[EventEnvelope, ...],
        resync_document: Mapping[str, object] | None,
        last_sequence: int,
        unregister: Callable[["Subscription"], None],
    ) -> None:
        if mode not in SUBSCRIPTION_MODES:
            raise GatewayError(
                f"subscription mode {mode!r}: the closed set "
                f"{sorted(SUBSCRIPTION_MODES)}"
            )
        if (
            isinstance(ceiling, bool)
            or not isinstance(ceiling, int)
            or ceiling < 1
        ):
            raise GatewayError("subscription ceiling: an int >= 1")
        if mode == "RESYNC" and resync_document is None:
            raise GatewayError(
                "a RESYNC subscription carries its snapshot document"
            )
        if mode == "REPLAY" and resync_document is not None:
            raise GatewayError(
                "a REPLAY subscription carries no snapshot document"
            )
        self._session_id = session_id
        self._clock = clock
        self._ceiling = ceiling
        self._mode = mode
        self._replay = replay
        self._resync_document = (
            dict(resync_document) if resync_document is not None else None
        )
        self._open_last_sequence = last_sequence
        self._unregister = unregister
        self._cond = threading.Condition()
        self._pending: deque[EventEnvelope] = deque()
        self._state = "OPEN"
        self._terminal: StreamOverflow | StreamClosed | None = None
        self._known_sequence = last_sequence

    # ------------------------------------------------------------ answer

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def mode(self) -> str:
        """§13's dual answer: REPLAY (the retained window rides
        `replay`) or RESYNC (the snapshot rides
        `resync_document`)."""
        return self._mode

    @property
    def replay(self) -> tuple[EventEnvelope, ...]:
        """The retained events after the cursor, in sequence order —
        the SAME window `session.events(since_sequence)` replays."""
        return self._replay

    @property
    def resync_document(self) -> Mapping[str, object] | None:
        """The bounded current snapshot document (RESYNC mode only —
        the same shape `session.events` answers)."""
        return self._resync_document

    @property
    def last_sequence(self) -> int:
        """The session's sequence at subscription time — the replay
        window's end and the live tail's start (gapless)."""
        return self._open_last_sequence

    @property
    def known_sequence(self) -> int:
        """The newest sequence this channel has observed (at open or
        on the last push) — the honest bound a terminal frame may
        report; the consumer's own last received id stays its
        reconnect cursor."""
        with self._cond:
            return self._known_sequence

    # ------------------------------------------------------------ channel

    def next_item(self, timeout: float) -> StreamItem | None:
        """Pull the next delivery item, blocking up to `timeout`
        seconds. None is the heartbeat wake (nothing arrived); an
        event drains in sequence order; a terminal item arrives
        after the pending queue drains and repeats idempotently."""
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            raise GatewayError("next_item timeout: a positive number")
        with self._cond:
            deadline = self._clock.now_monotonic() + timeout
            while self._state == "OPEN" and not self._pending:
                remaining = deadline - self._clock.now_monotonic()
                if remaining <= 0:
                    return None
                self._cond.wait(remaining)
            if self._pending:
                envelope = self._pending.popleft()
                return StreamEvent(envelope)
            assert self._terminal is not None  # not OPEN, queue empty
            return self._terminal

    def close(self) -> None:
        """End the channel from the consumer side (idempotent): no
        frame rides this close (`CLIENT` — the consumer is the one
        ending it), the fan-out stops, the registration drops."""
        with self._cond:
            if self._state != "OPEN":
                return
            self._state = "CLOSED"
            self._terminal = StreamClosed("CLIENT")
            self._cond.notify_all()
        self._unregister(self)

    # ------------------------------------------------------- core-private

    def _push(self, envelope: EventEnvelope) -> None:
        """Fan out one event to this channel — called under the
        GATEWAY's lock (the condition is the only lock taken here:
        the safe one-way nesting)."""
        with self._cond:
            if self._state != "OPEN":
                return
            if len(self._pending) >= self._ceiling:
                self._state = "OVERFLOW"
                self._known_sequence = envelope.sequence
                self._terminal = StreamOverflow(envelope.sequence)
                self._cond.notify_all()
                return
            self._pending.append(envelope)
            self._known_sequence = envelope.sequence
            self._cond.notify_all()

    def _close(self, reason: str) -> None:
        """End the channel from the gateway side — called under the
        GATEWAY's lock (the framed terminal; the registration removal
        is the caller's, iterating a copied roster)."""
        if reason not in STREAM_CLOSE_REASONS:
            raise GatewayError(
                f"stream close reason {reason!r}: the closed set "
                f"{sorted(STREAM_CLOSE_REASONS)}"
            )
        with self._cond:
            if self._state != "OPEN":
                return
            self._state = "CLOSED"
            self._terminal = StreamClosed(reason)
            self._cond.notify_all()

    def state(self) -> str:
        """The channel's state (SUBSCRIPTION_STATES) — an observable
        for tests and diagnostics, never identity."""
        with self._cond:
            return self._state


#: `Gateway.subscribe`'s answer: the rejected lane or the live
#: channel (whose `mode` carries §13's dual answer).
StreamAnswer = StreamRejection | Subscription


class Gateway:
    """The one inbound Workbench gateway over application operations.

    Socket-free by construction (G1); the delivery surface — the
    loopback HTTP transport or a direct Python caller — dispatches
    through `dispatch`/`dispatch_document`, the same core (§30's
    "GUI/CLI/API share operation semantics").
    """

    def __init__(
        self,
        config: GatewayConfig | None = None,
        clock: AppClock | None = None,
    ) -> None:
        self._config = config if config is not None else GatewayConfig()
        self._clock = clock if clock is not None else AppClock()
        self._operations: dict[str, OperationSpec] = {}
        self._lock = threading.Lock()
        self._sessions: dict[str, _Session] = {}
        self._events: dict[str, deque[EventEnvelope]] = {}
        self._idempotency: dict[str, _RecordedOutcome] = {}
        self._subscriptions: dict[str, list[Subscription]] = {}
        self._dispatch_counter = 0
        for spec in self._builtin_specs():
            self._operations[spec.name] = spec

    # ------------------------------------------------------------ surface

    @property
    def config(self) -> GatewayConfig:
        return self._config

    @property
    def operation_names(self) -> tuple[str, ...]:
        return tuple(sorted(self._operations))

    def register(self, spec: OperationSpec) -> None:
        """The composition root's wiring point (§6.1): register an
        application operation. Loud on a duplicate name — one name,
        one owner, never a silent override."""
        with self._lock:
            if spec.name in self._operations:
                raise GatewayError(
                    f"operation {spec.name!r}: already registered — "
                    "one name, one owner"
                )
            self._operations[spec.name] = spec

    def dispatch_document(
        self, document: Mapping[str, object]
    ) -> ResponseDocument:
        """The wire-neutral entry point (the transport's and the CLI
        parity's path): parse the envelope (a malformed document is
        DOMAIN_REJECTED — never an exception across the boundary),
        then dispatch."""
        try:
            envelope = RequestEnvelope.from_mapping(document)
        except GatewayContractError as exc:
            return self._response(
                status="REJECTED",
                operation_id=self._malformed_operation_id(document),
                rejection="DOMAIN_REJECTED",
                result={"error_type": "GatewayContractError", "reason": str(exc)},
            )
        return self.dispatch(envelope)

    def dispatch(self, envelope: RequestEnvelope) -> ResponseDocument:
        """The typed entry point — the whole pipeline under one
        coarse lock (the admission rows own finer policy)."""
        with self._lock:
            return self._dispatch_locked(envelope)

    def subscribe(
        self, session_id: str, since_sequence: int
    ) -> StreamRejection | Subscription:
        """Open one live delivery channel over a session's ordered
        stream (§13 — the SSE binding's core surface, the same
        channel a CLI parity consumer would pull).

        The answer is §13's dual: REPLAY (the retained window after
        `since_sequence` rides `subscription.replay`, then the live
        tail) or RESYNC (the cursor fell out of retention — the
        bounded current snapshot rides `resync_document`, then the
        live tail). A cursor beyond `last_sequence` yields an empty
        replay — the open answer's own `last_sequence` is the
        observable the consumer needs to detect its inconsistency.

        The whole open runs under the coarse dispatch lock, so the
        replay/live boundary is exact: the replay ends at the
        session's current `last_sequence` and the live queue starts
        at `last_sequence + 1` — no gap, no duplicate, no missed
        event between the two halves. An unknown session answers the
        rejected lane (DOMAIN_REJECTED — the same verdict a POST
        `session.events` would answer; the stream surface carries
        it, never a fabricated transport failure).
        """
        if not isinstance(session_id, str) or not session_id:
            raise GatewayError("subscribe: session_id must be a non-empty str")
        if (
            isinstance(since_sequence, bool)
            or not isinstance(since_sequence, int)
            or since_sequence < 0
        ):
            raise GatewayError("subscribe: since_sequence must be an int >= 0")
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return StreamRejection(
                    rejection="DOMAIN_REJECTED",
                    reason=f"session {session_id!r}: no such session",
                )
            retained = self._events.get(session_id, deque())
            resync_document: dict[str, object] | None = None
            replay: tuple[EventEnvelope, ...] = ()
            if retained and since_sequence < retained[0].sequence - 1:
                # §13: the cursor fell out of the retained window —
                # the bounded current snapshot (the SAME document
                # `session.events` answers), then the live tail.
                resync_document = {
                    "last_sequence": session.last_sequence,
                    "resync": "RESYNC_REQUIRED",
                    "retained_from": retained[0].sequence,
                    "snapshot": self._session_document(session),
                }
                mode = "RESYNC"
            else:
                replay = tuple(
                    event for event in retained if event.sequence > since_sequence
                )
                mode = "REPLAY"
            subscription = Subscription(
                session_id=session_id,
                clock=self._clock,
                ceiling=self._config.stream_buffer_events,
                mode=mode,
                replay=replay,
                resync_document=resync_document,
                last_sequence=session.last_sequence,
                unregister=self._unregister_subscription,
            )
            self._subscriptions.setdefault(session_id, []).append(subscription)
            return subscription

    def close_subscriptions(self) -> int:
        """The bounded-shutdown surface (§25 + §13): close every live
        channel with the SHUTDOWN terminal so each delivery writer
        wakes immediately, frames its honest close, and exits — the
        stream is a READ surface, nothing else is touched (a client
        disconnect never implicitly cancels unrelated execution, and
        neither does the server's own stop). Idempotent; returns the
        number of channels closed by THIS call."""
        with self._lock:
            closed = 0
            for session_id in list(self._subscriptions):
                channels = self._subscriptions.get(session_id)
                if not channels:
                    del self._subscriptions[session_id]
                    continue
                for subscription in list(channels):
                    before = subscription.state()
                    subscription._close("SHUTDOWN")
                    if before == "OPEN":
                        closed += 1
                channels.clear()
            return closed

    def _unregister_subscription(self, subscription: Subscription) -> None:
        """Drop one consumer-side-closed channel from the fan-out
        (idempotent — the shutdown path clears whole rosters
        itself). Takes the gateway lock WITHOUT holding the channel
        condition: the one-way nesting law."""
        with self._lock:
            channels = self._subscriptions.get(subscription.session_id)
            if channels is None:
                return
            if subscription in channels:
                channels.remove(subscription)
            if not channels:
                del self._subscriptions[subscription.session_id]

    # ------------------------------------------------------------ pipeline

    def _dispatch_locked(self, envelope: RequestEnvelope) -> ResponseDocument:
        # The request's logical identity FIRST (pre-auth, safe: a
        # digest of the client's own key — no server state, no
        # secret) so every rejection carries it.
        operation_id = self._operation_id(envelope)
        try:
            self._authenticate(envelope)
            spec = self._resolve(envelope)
            if spec.kind == "MUTATION":
                return self._dispatch_mutation(envelope, spec, operation_id)
            return self._dispatch_read(envelope, spec, operation_id)
        except _Rejected as rejection:
            return self._response(
                status="REJECTED",
                operation_id=operation_id,
                rejection=rejection.rejection,
                result={"reason": rejection.reason},
            )

    def _operation_id(self, envelope: RequestEnvelope) -> str:
        """The request's logical identity (G6): keyed requests derive
        it from the idempotency key (stable across retries — the
        logical operation); unkeyed reads from the dispatch counter
        (per-dispatch). It is the REQUEST identity — §10's execution
        identity (replay = a NEW one) is the artifact rows' own."""
        if envelope.client_request_id is not None:
            return content_digest(
                canonical_json({"client_request_id": envelope.client_request_id})
            )
        self._dispatch_counter += 1
        return content_digest(
            canonical_json({"dispatch": self._dispatch_counter})
        )

    def _malformed_operation_id(self, document: Mapping[str, object]) -> str:
        """The malformed-document identity: canonicalize what came
        in; if even that fails, degrade to the type name — the
        boundary never raises."""
        try:
            material = canonical_json(dict(document))
        except Exception:
            material = type(document).__name__
        return content_digest(material)

    def _authenticate(self, envelope: RequestEnvelope) -> None:
        """AUTH_FAILED / AUTHZ_DENIED (§8): the credential check and
        the scope check — constant-time, the token never recorded."""
        if not self._config.auth_required:
            return
        token = envelope.auth_token
        if token is None:
            raise _Rejected("AUTH_FAILED", "auth required: no credential presented")
        for credential in self._config.credentials:
            if hmac.compare_digest(credential.token, token):
                if (
                    SCOPE_WILDCARD in credential.allowed_operations
                    or envelope.operation in credential.allowed_operations
                ):
                    return
                raise _Rejected(
                    "AUTHZ_DENIED",
                    f"principal {credential.principal!r} is not "
                    f"authorized for {envelope.operation!r}",
                )
        raise _Rejected("AUTH_FAILED", "auth failed: unknown credential")

    def _resolve(self, envelope: RequestEnvelope) -> OperationSpec:
        spec = self._operations.get(envelope.operation)
        if spec is None:
            raise _Rejected(
                "DOMAIN_REJECTED",
                f"unknown operation {envelope.operation!r} — registered: "
                f"{sorted(self._operations)}",
            )
        return spec

    def _session_guard(
        self, envelope: RequestEnvelope, spec: OperationSpec
    ) -> _Session | None:
        """The session resolution + the revision/lease guards
        (§12.2/§8): DOMAIN_REJECTED for the unresolvable,
        STALE_REVISION for the stale writer, LEASE_EXPIRED for a
        lease not currently valid-for-use. None when the operation is
        not session-scoped."""
        if not spec.session_scoped:
            return None
        session_id = envelope.session_id
        if session_id is None:
            raise _Rejected(
                "DOMAIN_REJECTED",
                f"{envelope.operation}: a session-scoped operation "
                "requires session_id",
            )
        session = self._sessions.get(session_id)
        if session is None:
            raise _Rejected(
                "DOMAIN_REJECTED",
                f"session {session_id!r}: no such session",
            )
        if spec.requires_revision:
            if envelope.expected_revision is None:
                raise _Rejected(
                    "DOMAIN_REJECTED",
                    f"{envelope.operation}: requires expected_revision",
                )
            if envelope.expected_revision != session.revision:
                raise _Rejected(
                    "STALE_REVISION",
                    f"expected revision {envelope.expected_revision} != "
                    f"current {session.revision} — a stale writer "
                    "cannot mutate newer state",
                )
        if spec.requires_lease:
            valid = (
                session.lease_token is not None
                and envelope.lease_token == session.lease_token
                and session.lease_expires_monotonic is not None
                and self._clock.now_monotonic() < session.lease_expires_monotonic
            )
            if not valid:
                raise _Rejected(
                    "LEASE_EXPIRED",
                    "the lease is not currently valid-for-use (absent, "
                    "mismatched, or expired)",
                )
        return session

    def _dispatch_mutation(
        self,
        envelope: RequestEnvelope,
        spec: OperationSpec,
        operation_id: str,
    ) -> ResponseDocument:
        """The mutation arm: idempotency first (a retry replays the
        recorded outcome even after the world moved on — the guard
        already passed once), then the guards, the invocation, the
        effect commit, and the record (UNKNOWN outcomes are recorded
        too — the blind retry is blocked, §12.1)."""
        key = envelope.client_request_id
        if key is None:
            raise _Rejected(
                "DOMAIN_REJECTED",
                f"{envelope.operation}: a mutation requires "
                "client_request_id (the idempotency key, §12.2)",
            )
        material = envelope.material_digest()
        recorded = self._idempotency.get(key)
        if recorded is not None:
            if recorded.material_digest != material:
                raise _Rejected(
                    "DUPLICATE_REQUEST",
                    "the idempotency key is already bound to a "
                    "different request (the conflicting reuse)",
                )
            return replace(recorded.response, duplicate=True)
        session = self._session_guard(envelope, spec)
        response = self._invoke(envelope, spec, operation_id, session)
        self._idempotency[key] = _RecordedOutcome(
            material_digest=material, response=response
        )
        return response

    def _dispatch_read(
        self,
        envelope: RequestEnvelope,
        spec: OperationSpec,
        operation_id: str,
    ) -> ResponseDocument:
        session = self._session_guard(envelope, spec)
        return self._invoke(envelope, spec, operation_id, session)

    def _invoke(
        self,
        envelope: RequestEnvelope,
        spec: OperationSpec,
        operation_id: str,
        session: _Session | None,
    ) -> ResponseDocument:
        """The invocation + the §12.1 outcome mapping: a MUTATION
        raising after admission is SENT_OUTCOME_UNKNOWN (recorded —
        the blind retry is blocked); a READ raising is RUNTIME_FAILED.
        The exception's TYPE rides the result; the message is §21's
        diagnostics surface, never the wire."""
        context = OperationContext(
            operation=envelope.operation,
            operation_id=operation_id,
            client_request_id=envelope.client_request_id,
            arguments=envelope.arguments,
            session=(
                SessionView(
                    session_id=session.session_id,
                    revision=session.revision,
                    attached=session.attached,
                )
                if session is not None
                else None
            ),
            clock=self._clock,
            effects=self._effects_for(session, operation_id),
        )
        try:
            result = spec.handler(context)
        except _Rejected:
            # the builtins' own validation rejections ride the
            # pipeline's carrier, never the failure mapper
            raise
        except Exception as exc:
            failure = {"error_type": type(exc).__name__}
            if spec.kind == "MUTATION":
                return self._response(
                    status="UNKNOWN",
                    operation_id=operation_id,
                    rejection="SENT_OUTCOME_UNKNOWN",
                    result=failure,
                    session_id=session.session_id if session else None,
                    revision=session.revision if session else None,
                    sequence=session.last_sequence if session else None,
                )
            return self._response(
                status="FAILED",
                operation_id=operation_id,
                rejection="RUNTIME_FAILED",
                result=failure,
            )
        return self._response(
            status="OK",
            operation_id=operation_id,
            result=dict(result) if result is not None else {},
            session_id=session.session_id if session else None,
            revision=session.revision if session else None,
            sequence=session.last_sequence if session else None,
        )

    def _effects_for(
        self, session: _Session | None, operation_id: str
    ) -> OperationEffects | None:
        """The session-scoped event surface for registered handlers
        (wb-5): the gateway keeps the stream and its sequence — the
        handler's `effect(payload)` appends an OPERATION_EFFECT into
        the dispatching session's ordered stream. None for
        non-session-scoped operations (no session, no stream)."""
        if session is None:
            return None

        def _emit_effect(payload: Mapping[str, object]) -> None:
            self._emit(
                session,
                "OPERATION_EFFECT",
                operation_id=operation_id,
                payload=payload,
            )

        return OperationEffects(_emit_effect)

    def _response(
        self,
        status: str,
        operation_id: str,
        rejection: str | None = None,
        result: Mapping[str, object] | None = None,
        session_id: str | None = None,
        revision: int | None = None,
        sequence: int | None = None,
    ) -> ResponseDocument:
        return ResponseDocument(
            status=status,
            operation_id=operation_id,
            rejection=rejection,
            result=dict(result) if result is not None else None,
            session_id=session_id or None,
            revision=revision,
            sequence=sequence,
        )

    # ------------------------------------------------------- session seed

    def _builtin_specs(self) -> tuple[OperationSpec, ...]:
        """The session-translation seed (§8's first family + the
        service status) — IN-MEMORY by contract (G2)."""
        return (
            OperationSpec(
                name="session.create",
                kind="MUTATION",
                handler=self._op_session_create,
                description="create a session (the §8 first family)",
            ),
            OperationSpec(
                name="session.get",
                kind="READ",
                handler=self._op_session_get,
                session_scoped=True,
            ),
            OperationSpec(
                name="session.attach",
                kind="MUTATION",
                handler=self._op_session_attach,
                session_scoped=True,
                requires_revision=True,
            ),
            OperationSpec(
                name="session.detach",
                kind="MUTATION",
                handler=self._op_session_detach,
                session_scoped=True,
                requires_revision=True,
                requires_lease=True,
            ),
            OperationSpec(
                name="session.events",
                kind="READ",
                handler=self._op_session_events,
                session_scoped=True,
            ),
            OperationSpec(
                name="app.status",
                kind="READ",
                handler=self._op_app_status,
            ),
        )

    def _label_argument(self, context: OperationContext) -> str:
        """The seed's shared argument validation: {} or {"label": str}
        — the closed-document law, DOMAIN_REJECTED on anything else."""
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"label"})
        if unknown:
            raise _Rejected(
                "DOMAIN_REJECTED",
                f"{context.operation}: unknown argument(s) {unknown}",
            )
        label = arguments.get("label", "")
        if not isinstance(label, str):
            raise _Rejected(
                "DOMAIN_REJECTED", f"{context.operation}: label must be str"
            )
        return label

    def _no_arguments(self, context: OperationContext) -> None:
        if context.arguments:
            raise _Rejected(
                "DOMAIN_REJECTED",
                f"{context.operation}: takes no arguments "
                f"({sorted(context.arguments)})",
            )

    def _op_session_create(
        self, context: OperationContext
    ) -> Mapping[str, object]:
        self._label_argument(context)
        # The session id derives from the creation request's material
        # (G6): the client's idempotency key + the arguments —
        # deterministic, retry-stable, key-distinct (the idempotency
        # layer guarantees the same key never reaches here twice).
        session_id = content_digest(
            canonical_json(
                {
                    "arguments": dict(context.arguments),
                    "client_request_id": context.client_request_id,
                    "operation": context.operation,
                }
            )
        )
        observed = self._clock.now_utc()
        session = _Session(
            session_id=session_id,
            revision=0,
            attached=False,
            created_observed_at=observed,
        )
        self._sessions[session_id] = session
        self._events[session_id] = deque(maxlen=self._config.retention_events)
        self._emit(
            session,
            "SESSION_CREATED",
            operation_id=context.operation_id,
            payload={"created_observed_at": observed},
        )
        return {
            "session_id": session_id,
            "revision": session.revision,
            "event_sequence": session.last_sequence,
        }

    def _op_session_get(self, context: OperationContext) -> Mapping[str, object]:
        self._no_arguments(context)
        session = self._require_session(context)
        return self._session_document(session)

    def _op_session_attach(
        self, context: OperationContext
    ) -> Mapping[str, object]:
        label = self._label_argument(context)
        session = self._require_session(context)
        observed = self._clock.now_utc()
        expires = self._clock.now_monotonic() + self._config.lease_seconds
        lease_token = content_digest(
            canonical_json(
                {
                    "expires_monotonic": expires,
                    "session_id": session.session_id,
                }
            )
        )
        session.attached = True
        session.revision += 1
        session.lease_token = lease_token
        session.lease_expires_monotonic = expires
        self._emit(
            session,
            "SESSION_ATTACHED",
            operation_id=context.operation_id,
            payload={"label": label, "observed_at": observed},
        )
        return {
            "attached": True,
            "lease_seconds": self._config.lease_seconds,
            "lease_token": lease_token,
        }

    def _op_session_detach(
        self, context: OperationContext
    ) -> Mapping[str, object]:
        self._no_arguments(context)
        session = self._require_session(context)
        observed = self._clock.now_utc()
        session.attached = False
        session.revision += 1
        session.lease_token = None
        session.lease_expires_monotonic = None
        self._emit(
            session,
            "SESSION_DETACHED",
            operation_id=context.operation_id,
            payload={"observed_at": observed},
        )
        return {"detached": True}

    def _op_session_events(
        self, context: OperationContext
    ) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        unknown = sorted(set(arguments) - {"since_sequence"})
        if unknown:
            raise _Rejected(
                "DOMAIN_REJECTED",
                f"{context.operation}: unknown argument(s) {unknown}",
            )
        since = arguments.get("since_sequence", 0)
        if isinstance(since, bool) or not isinstance(since, int) or since < 0:
            raise _Rejected(
                "DOMAIN_REJECTED",
                f"{context.operation}: since_sequence must be an int >= 0",
            )
        session = self._require_session(context)
        retained = self._events[session.session_id]
        if retained:
            first = retained[0].sequence
            if since < first - 1:
                # §13: cannot replay from `since` — resync with the
                # bounded current snapshot instead.
                return {
                    "last_sequence": session.last_sequence,
                    "resync": "RESYNC_REQUIRED",
                    "retained_from": first,
                    "snapshot": self._session_document(session),
                }
        replay = [
            event.to_mapping() for event in retained if event.sequence > since
        ]
        return {
            "events": replay,
            "last_sequence": session.last_sequence,
        }

    def _op_app_status(self, context: OperationContext) -> Mapping[str, object]:
        self._no_arguments(context)
        # Construction-stable only (the parity law): no volatile
        # counters, no clock (§21's observations own those).
        return {
            "service": "canonsim-workbench-gateway",
            "contract": GATEWAY_SCHEMA_IDENTITY,
            "exposure": self._config.exposure,
            "auth_required": self._config.auth_required,
            "operations": sorted(self._operations),
        }

    def _require_session(self, context: OperationContext) -> _Session:
        session_id = context.session.session_id if context.session else None
        session = self._sessions.get(session_id or "")
        if session is None:
            raise _Rejected(
                "DOMAIN_REJECTED", f"session {session_id!r}: no such session"
            )
        return session

    def _session_document(self, session: _Session) -> dict[str, object]:
        return {
            "attached": session.attached,
            "created_observed_at": session.created_observed_at,
            "event_sequence": session.last_sequence,
            "revision": session.revision,
            "session_id": session.session_id,
        }

    def _emit(
        self,
        session: _Session,
        event_type: str,
        operation_id: str,
        payload: Mapping[str, object],
    ) -> EventEnvelope:
        """The ordered append (§13): sequence = last + 1 — no clock
        in the identity; `observed_at` is the UTC_WALL reading. The
        same append fans out to the session's live channels (under
        this lock — the writer threads wake on their own condition,
        never here)."""
        session.last_sequence += 1
        event = EventEnvelope.build(
            session_id=session.session_id,
            operation_id=operation_id,
            sequence=session.last_sequence,
            event_type=event_type,
            observed_at=self._clock.now_utc(),
            payload=payload,
        )
        self._events[session.session_id].append(event)
        for subscription in self._subscriptions.get(session.session_id, ()):
            subscription._push(event)
        return event
