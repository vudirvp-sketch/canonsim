"""The gateway contract (wb-4, the app spec §§8/12/13 — the family's
fourth row).

The law: **HTTP is a delivery mechanism; the semantic API is
application operations** (§8). This module owns the wire-neutral
documents that make that split real — the closed vocabularies and the
typed envelopes every delivery surface (the loopback HTTP binding
today, CLI parity by the same core) serializes:

```text
RequestEnvelope  — operation | arguments | client_request_id |
                   session_id | expected_revision | lease_token |
                   auth_token
ResponseDocument — status | operation_id | rejection | result |
                   session_id | revision | sequence | duplicate
EventEnvelope    — event_id | session_id | operation_id | sequence |
                   event_type | observed_at | payload
```

Closed vocabularies (each a frozen set, each tested for its exact
membership — a silent vocabulary member is a bug):

- `REJECTIONS` — §8's minimum distinction set: AUTH_FAILED |
  AUTHZ_DENIED | DUPLICATE_REQUEST | STALE_REVISION | LEASE_EXPIRED
  | DOMAIN_REJECTED | RUNTIME_FAILED | SENT_OUTCOME_UNKNOWN. Every
  rejection is NOT_SENT (§12.1): nothing was dispatched.
- `EXPOSURES` — §4's independent axis: LOOPBACK | LAN | TUNNEL. The
  start law (G3): non-loopback exposure cannot start without auth.
- `DISPATCH_STATUSES` — the response status: OK | REJECTED | FAILED
  | UNKNOWN, mapped one-to-one onto §12.1's dispatch outcomes by
  `DISPATCH_OUTCOME_FOR_STATUS` (a READ failure is a KNOWN terminal
  failure; a MUTATION failure after admission is UNKNOWN — the
  ambiguity honored, never a fabricated result).
- `EVENT_TYPES` — the ordered-stream members the session-translation
  seed emits (§13): SESSION_CREATED | SESSION_ATTACHED |
  SESSION_DETACHED | OPERATION_EFFECT (wb-5+ effects).

Identity discipline (G6, the D4 read-side law): every digest here is
sha256 over canonical JSON (`sort_keys=True`, fixed separators) — no
PYTHONHASHSEED dependence, no RNG, NO CLOCK in any identity (§17:
`observed_at` is the injectable UTC_WALL observation, never identity
material). The auth token is never digest material: `material_digest`
freezes the request's material EXCLUDING the credential (§21's law —
credentials never enter digests, responses, events, or status).

Serialization is strict (the closed-document law): `from_mapping`
rejects unknown keys, wrong types, and non-JSON-safe values LOUDLY
(`GatewayContractError` — the same law as the Scene IR and the
execution artifact); `to_mapping` is the deterministic byte form.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from workbench.application.identity import content_digest

#: The contract's own schema identity — bumps on any breaking envelope
#: shape change (the same discipline as the artifact's and the IR's).
GATEWAY_SCHEMA_IDENTITY = "canon_workbench_gateway@0.1"

#: §8's minimum rejection/failure distinctions — the closed set.
REJECTIONS: frozenset[str] = frozenset(
    {
        "AUTH_FAILED",
        "AUTHZ_DENIED",
        "DUPLICATE_REQUEST",
        "STALE_REVISION",
        "LEASE_EXPIRED",
        "DOMAIN_REJECTED",
        "RUNTIME_FAILED",
        "SENT_OUTCOME_UNKNOWN",
    }
)

#: §4's exposure axis — the independent EXPOSURE modes.
EXPOSURES: frozenset[str] = frozenset({"LOOPBACK", "LAN", "TUNNEL"})

#: The response statuses over the dispatch pipeline.
DISPATCH_STATUSES: frozenset[str] = frozenset(
    {"OK", "REJECTED", "FAILED", "UNKNOWN"}
)

#: §12.1's dispatch-outcome vocabulary.
DISPATCH_OUTCOMES: frozenset[str] = frozenset(
    {"NOT_SENT", "SENT_AND_TERMINAL", "SENT_OUTCOME_UNKNOWN"}
)

#: The status -> dispatch-outcome law (§12.1): every rejection is
#: NOT_SENT; OK and FAILED are known terminal results; UNKNOWN is the
#: ambiguous dispatch — no blind retry (G4).
DISPATCH_OUTCOME_FOR_STATUS: dict[str, str] = {
    "OK": "SENT_AND_TERMINAL",
    "FAILED": "SENT_AND_TERMINAL",
    "REJECTED": "NOT_SENT",
    "UNKNOWN": "SENT_OUTCOME_UNKNOWN",
}

#: The ordered-stream event types the seed emits (§13).
EVENT_TYPES: frozenset[str] = frozenset(
    {
        "SESSION_CREATED",
        "SESSION_ATTACHED",
        "SESSION_DETACHED",
        "OPERATION_EFFECT",
    }
)

#: The operation kinds (the dispatch-outcome mapping depends on it).
OPERATION_KINDS: frozenset[str] = frozenset({"READ", "MUTATION"})


class GatewayContractError(ValueError):
    """A malformed gateway document (construction-time, never
    silent — the closed-document law)."""


def canonical_json(value: Any) -> str:
    """The deterministic serialization every digest and byte-form
    rides: sorted keys, fixed separators, UTF-8 — the D4 discipline.
    Only JSON-safe values are legal inputs (validated by
    `_require_json_safe` before material ever reaches here)."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _require_json_safe(value: Any, where: str) -> None:
    """The closed-document law, recursive arm: arguments and payloads
    must be JSON-safe (str/int/float/bool/None/list/dict with str
    keys, floats finite). Anything else — a set, a tuple, an object,
    NaN — is a loud construction error, never a silent drop."""
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return
    if isinstance(value, int):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise GatewayContractError(
                f"{where}: non-finite float (JSON-safe values only)"
            )
        return
    if isinstance(value, list):
        for item in value:
            _require_json_safe(item, where)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise GatewayContractError(
                    f"{where}: dict key must be str "
                    f"(got {type(key).__name__})"
                )
            _require_json_safe(item, where)
        return
    raise GatewayContractError(
        f"{where}: value of type {type(value).__name__} is not JSON-safe"
    )


def require_operation_name(name: Any) -> str:
    """The operation name is the family.member form (§8's families:
    session.*, run.*, chat.*, model.*): two or more dot-separated
    non-empty lowercase segments."""
    if not isinstance(name, str) or "." not in name:
        raise GatewayContractError(
            f"operation {name!r}: the family.member form (>=1 dot)"
        )
    segments = name.split(".")
    for segment in segments:
        if not segment or not segment.replace("_", "a").isalnum() or segment != segment.lower():
            raise GatewayContractError(
                f"operation {name!r}: lowercase [a-z0-9_] segments"
            )
    return name


def _require_optional_str(value: Any, key: str) -> None:
    if value is not None and (not isinstance(value, str) or not value):
        raise GatewayContractError(f"{key}: a non-empty str or absent")


def _unknown_keys(document: Mapping[str, Any], known: frozenset[str]) -> list[str]:
    return sorted(set(document) - known)


@dataclass(frozen=True)
class RequestEnvelope:
    """One client request, wire-neutral (§8).

    `client_request_id` is the idempotency key (§12.2 — the stable
    mutation identity; REQUIRED on mutations, G4). `expected_revision`
    is the CAS guard for session mutations (§12.2). `lease_token` is
    the exclusive-control token (§8). `auth_token` is the credential —
    consumed by the gateway, never digest/serialization material.
    """

    operation: str
    arguments: Mapping[str, Any] = field(default_factory=dict)
    client_request_id: str | None = None
    session_id: str | None = None
    expected_revision: int | None = None
    lease_token: str | None = None
    auth_token: str | None = None

    def __post_init__(self) -> None:
        require_operation_name(self.operation)
        if not isinstance(self.arguments, Mapping):
            raise GatewayContractError("arguments: a mapping")
        _require_json_safe(dict(self.arguments), "arguments")
        _require_optional_str(self.client_request_id, "client_request_id")
        _require_optional_str(self.session_id, "session_id")
        _require_optional_str(self.lease_token, "lease_token")
        _require_optional_str(self.auth_token, "auth_token")
        if self.expected_revision is not None and (
            isinstance(self.expected_revision, bool)
            or not isinstance(self.expected_revision, int)
            or self.expected_revision < 0
        ):
            raise GatewayContractError(
                "expected_revision: a non-negative int or absent"
            )

    def to_mapping(self) -> dict[str, Any]:
        document: dict[str, Any] = {"operation": self.operation}
        if self.arguments:
            document["arguments"] = dict(self.arguments)
        for key in (
            "client_request_id",
            "session_id",
            "expected_revision",
            "lease_token",
            "auth_token",
        ):
            value = getattr(self, key)
            if value is not None:
                document[key] = value
        return document

    @classmethod
    def from_mapping(cls, document: Mapping[str, Any]) -> RequestEnvelope:
        if not isinstance(document, Mapping):
            raise GatewayContractError(
                "request envelope: a JSON object (dict), got "
                f"{type(document).__name__}"
            )
        known = frozenset(
            {
                "operation",
                "arguments",
                "client_request_id",
                "session_id",
                "expected_revision",
                "lease_token",
                "auth_token",
            }
        )
        unknown = _unknown_keys(document, known)
        if unknown:
            raise GatewayContractError(
                f"request envelope: unknown key(s) {unknown} — the "
                "closed document law (contract.py owns the fields)"
            )
        arguments = document.get("arguments", {})
        if not isinstance(arguments, Mapping):
            raise GatewayContractError("arguments: a mapping")
        return cls(
            operation=document.get("operation"),
            arguments=dict(arguments),
            client_request_id=document.get("client_request_id"),
            session_id=document.get("session_id"),
            expected_revision=document.get("expected_revision"),
            lease_token=document.get("lease_token"),
            auth_token=document.get("auth_token"),
        )

    def material_digest(self) -> str:
        """The request's material identity (G6): the canonical-JSON
        digest over every material field — EXCLUDING `auth_token`
        (§21: the credential never enters a digest) and EXCLUDING the
        identity-free derived fields. The same logical retry carries
        the same digest; any material change changes it."""
        material: dict[str, Any] = {
            "arguments": dict(self.arguments),
            "client_request_id": self.client_request_id,
            "expected_revision": self.expected_revision,
            "lease_token": self.lease_token,
            "operation": self.operation,
            "session_id": self.session_id,
        }
        return content_digest(canonical_json(material))


@dataclass(frozen=True)
class ResponseDocument:
    """The dispatch's terminal answer, wire-neutral.

    `status` is DISPATCH_STATUSES; `rejection` is the REJECTIONS
    member when REJECTED/FAILED/UNKNOWN; `result` carries the
    operation's payload when OK (or the failure's error TYPE — never
    a raw message: §21's diagnostics surface owns the full envelope);
    `session_id`/`revision`/`sequence` are the post-dispatch session
    state; `duplicate` marks the idempotent replay (the recorded
    outcome, not a second effect).
    """

    status: str
    operation_id: str
    rejection: str | None = None
    result: Mapping[str, Any] | None = None
    session_id: str | None = None
    revision: int | None = None
    sequence: int | None = None
    duplicate: bool = False

    def __post_init__(self) -> None:
        if self.status not in DISPATCH_STATUSES:
            raise GatewayContractError(
                f"response status {self.status!r}: the closed set "
                f"{sorted(DISPATCH_STATUSES)}"
            )
        if self.status == "OK" and self.rejection is not None:
            raise GatewayContractError("an OK response carries no rejection")
        if self.status != "OK" and self.rejection not in REJECTIONS:
            raise GatewayContractError(
                f"response rejection {self.rejection!r}: the closed set "
                f"{sorted(REJECTIONS)}"
            )
        if not isinstance(self.operation_id, str) or not self.operation_id:
            raise GatewayContractError("operation_id: a non-empty str")
        if self.result is not None:
            if not isinstance(self.result, Mapping):
                raise GatewayContractError("result: a mapping or absent")
            _require_json_safe(dict(self.result), "result")

    def dispatch_outcome(self) -> str:
        """§12.1's outcome for this response — the closed mapping."""
        return DISPATCH_OUTCOME_FOR_STATUS[self.status]

    def to_mapping(self) -> dict[str, Any]:
        document: dict[str, Any] = {
            "operation_id": self.operation_id,
            "status": self.status,
        }
        if self.rejection is not None:
            document["rejection"] = self.rejection
        if self.result is not None:
            document["result"] = dict(self.result)
        if self.session_id is not None:
            document["session_id"] = self.session_id
        if self.revision is not None:
            document["revision"] = self.revision
        if self.sequence is not None:
            document["sequence"] = self.sequence
        if self.duplicate:
            document["duplicate"] = True
        return document

    @classmethod
    def from_mapping(cls, document: Mapping[str, Any]) -> ResponseDocument:
        if not isinstance(document, Mapping):
            raise GatewayContractError(
                "response document: a JSON object (dict), got "
                f"{type(document).__name__}"
            )
        known = frozenset(
            {
                "status",
                "operation_id",
                "rejection",
                "result",
                "session_id",
                "revision",
                "sequence",
                "duplicate",
            }
        )
        unknown = _unknown_keys(document, known)
        if unknown:
            raise GatewayContractError(
                f"response document: unknown key(s) {unknown} — the "
                "closed document law"
            )
        result = document.get("result")
        if result is not None and not isinstance(result, Mapping):
            raise GatewayContractError("result: a mapping or absent")
        return cls(
            status=document.get("status"),
            operation_id=document.get("operation_id"),
            rejection=document.get("rejection"),
            result=dict(result) if result is not None else None,
            session_id=document.get("session_id"),
            revision=document.get("revision"),
            sequence=document.get("sequence"),
            duplicate=bool(document.get("duplicate", False)),
        )


@dataclass(frozen=True)
class EventEnvelope:
    """One ordered session event (§8's envelope, §13's stream law).

    `sequence` is the per-session counter starting at 1 — NO clock in
    the identity; `event_id` is the deterministic digest over
    (session_id, operation_id, sequence); `observed_at` is the
    UTC_WALL observation (the injectable clock's reading — display/
    persistence class only, §17).
    """

    event_id: str
    session_id: str
    operation_id: str
    sequence: int
    event_type: str
    observed_at: float
    payload: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("event_id", "session_id", "operation_id"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name):
                raise GatewayContractError(f"event {name}: a non-empty str")
        if (
            isinstance(self.sequence, bool)
            or not isinstance(self.sequence, int)
            or self.sequence < 1
        ):
            raise GatewayContractError("event sequence: an int >= 1")
        if self.event_type not in EVENT_TYPES:
            raise GatewayContractError(
                f"event type {self.event_type!r}: the closed set "
                f"{sorted(EVENT_TYPES)}"
            )
        if not isinstance(self.observed_at, float) or not math.isfinite(
            self.observed_at
        ):
            raise GatewayContractError("event observed_at: a finite float")
        if not isinstance(self.payload, Mapping):
            raise GatewayContractError("event payload: a mapping")
        _require_json_safe(dict(self.payload), "event payload")

    @classmethod
    def build(
        cls,
        session_id: str,
        operation_id: str,
        sequence: int,
        event_type: str,
        observed_at: float,
        payload: Mapping[str, Any],
    ) -> EventEnvelope:
        """The deterministic constructor: `event_id` derives from the
        (session_id, operation_id, sequence) material — the same
        effect always yields the same event identity (no clock, no
        RNG; the D4 discipline)."""
        event_id = content_digest(
            canonical_json(
                {
                    "operation_id": operation_id,
                    "sequence": sequence,
                    "session_id": session_id,
                }
            )
        )
        return cls(
            event_id=event_id,
            session_id=session_id,
            operation_id=operation_id,
            sequence=sequence,
            event_type=event_type,
            observed_at=observed_at,
            payload=dict(payload),
        )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "observed_at": self.observed_at,
            "operation_id": self.operation_id,
            "payload": dict(self.payload),
            "sequence": self.sequence,
            "session_id": self.session_id,
        }

    @classmethod
    def from_mapping(cls, document: Mapping[str, Any]) -> EventEnvelope:
        if not isinstance(document, Mapping):
            raise GatewayContractError("event envelope: a JSON object")
        known = frozenset(
            {
                "event_id",
                "session_id",
                "operation_id",
                "sequence",
                "event_type",
                "observed_at",
                "payload",
            }
        )
        unknown = _unknown_keys(document, known)
        if unknown:
            raise GatewayContractError(
                f"event envelope: unknown key(s) {unknown} — the "
                "closed document law"
            )
        payload = document.get("payload", {})
        if not isinstance(payload, Mapping):
            raise GatewayContractError("event payload: a mapping")
        return cls(
            event_id=document.get("event_id"),
            session_id=document.get("session_id"),
            operation_id=document.get("operation_id"),
            sequence=document.get("sequence"),
            event_type=document.get("event_type"),
            observed_at=document.get("observed_at"),
            payload=dict(payload),
        )


#: The strict-roundtrip check's roster (the same law as the
#: artifact's): every envelope dataclass must survive
#: to_mapping -> from_mapping byte-identically.
ENVELOPE_TYPES: tuple[type, ...] = (
    RequestEnvelope,
    ResponseDocument,
    EventEnvelope,
)
