"""The immutable execution artifact + provenance (wb-3, the app spec
§10 + §7.6 — the family's third row).

The law: **before side effects, freeze all materially relevant run
inputs.** The `ExecutionArtifact` is that freeze — immutable by
construction (a frozen dataclass; there is no mutation API, and the
replay law below keeps even re-runs honest):

```text
execution_id/operation_id ; model identity + content identity ;
pack/schema identity where relevant ; prompt identity + frozen
material inputs ; resolved inference configuration ;
backend/runtime/build/protocol identity ; capability snapshot ;
serialized request identity/digest ; seed/deterministic inputs ;
tool-authority state where relevant ; terminal result/status +
relevant diagnostics
```

Existing engine/CanonSim provenance remains authoritative for its
fields (the CanonSim log header, the provenance manifest of the
engine adapter); this artifact EXTENDS/references those, it never
competes with them (CONTRACTS §5: no second semantic authority —
§7.6's rule: "an execution artifact closes the material inputs/
identity needed to explain a run; it is not a replacement for
CanonSim's canonical log").

The reproducibility scopes (§10) — `REPRODUCIBILITY_SCOPES`:

```text
EXACT_BITWISE | SEMANTIC | APPROXIMATE | EXPLANATORY_ONLY
```

The three reproducibility KINDS, separated (never conflated):
canonical (same canonical inputs → same canonical replay — the
engine's own byte-identical law, INV-2), request (same immutable
request inputs → same serialized request), inference (request +
declared model/backend/runtime conditions). The artifact's
`request_digest` serves the request kind: a deterministic digest of
the serialized request, so two runs of the same request inputs
carry the same digest while remaining distinct executions.

Prompt text alone is insufficient when templates, special tokens,
grammar, tokenizer/model metadata, seed or runtime configuration
can differ — hence the named frozen fields, not a blob.
**Replay creates a new execution identity**: a replay artifact
references the original via `replay_of` and still carries its own
`execution_id` — the vocabulary makes the distinction explicit, the
serialization keeps it (same frozen inputs, two executions, two
artifacts, one lineage link).

Determinism law (D4): the same constructor inputs produce the
byte-identical JSON — `json.dumps(..., sort_keys=True,
separators=(",", ":"))`, lists in sorted/construction order, and NO
CLOCK anywhere: the §10 field list carries no timestamp, and this
module never imports the clock (a wall/monotonic value may enter an
artifact only as an explicit, frozen input field — never as a hidden
read; §17: no wall clock in request identity).
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from workbench.application.identity import content_digest

#: The artifact's own schema identity — bumps on any breaking shape
#: change (the same discipline as the IR's SCHEMA_IDENTITY and the
#: event schema's `schema_version`).
ARTIFACT_SCHEMA_IDENTITY = "canon_execution_artifact@0.1"

#: The reproducibility scopes (§10 — the spec spells the first as
#: `EXACT/BITWISE`; the token here is EXACT_BITWISE, one scope).
REPRODUCIBILITY_SCOPES: frozenset[str] = frozenset(
    {"EXACT_BITWISE", "SEMANTIC", "APPROXIMATE", "EXPLANATORY_ONLY"}
)

#: The three reproducibility kinds, separated (§10 — documented
#: vocabulary; the artifact's fields serve each kind without
#: conflating them: canonical = the engine's own replay law; request
#: = the frozen inputs + request_digest; inference = request + the
#: declared model/backend/runtime identities).
REPRODUCIBILITY_KINDS: frozenset[str] = frozenset(
    {"CANONICAL", "REQUEST", "INFERENCE"}
)


class ArtifactError(ValueError):
    """A malformed execution artifact (construction-time, never
    silent)."""


def request_digest(frozen_inputs: Mapping[str, str]) -> str:
    """The serialized request identity (§10's "serialized request
    identity/digest", the REQUEST reproducibility kind): a
    deterministic sha256-hex digest over the named frozen inputs —
    sorted keys, fixed separators, no clock, no PYTHONHASHSEED
    dependence. The same immutable request inputs always yield the
    same digest; any material change to the inputs changes it."""
    payload = json.dumps(
        dict(sorted(frozen_inputs.items())),
        sort_keys=True,
        separators=(",", ":"),
    )
    return content_digest(payload)


@dataclass(frozen=True)
class ExecutionArtifact:
    """One Workbench operation/run's frozen record: the material
    inputs, the identities they rode on, and the terminal outcome.

    Identity fields are opaque identity strings (a §9 material
    identity, a CanonSim schema identity, an engine provenance
    field) — this artifact references them, it never re-derives
    them (the single-owner law: CanonSim provenance stays
    authoritative for its own fields).

    `frozen_inputs` — the prompt identity and the other named
    material inputs ("prompt identity + frozen material inputs"):
    a name → identity/digest mapping, frozen sorted at construction.
    `capability_snapshot` (§10.1) — the observed capability snapshot
    when capability data materially influenced the run; immutable
    run provenance once recorded here.
    `status` — the terminal result/status, free-form at step 1 (the
    Execution lifecycle vocabulary — §11 — owns its closure when
    that step lands; this field only requires it non-empty and
    terminal-sounding: it is written once, at freeze time).
    `diagnostics` — the relevant diagnostics, ordered as given.
    `replay_of` — the original execution_id when this artifact is a
    replay (§10: replay creates a NEW execution identity — the link
    is lineage, never identity reuse).
    """

    execution_id: str
    status: str
    frozen_inputs: tuple[tuple[str, str], ...] = field(default=())
    operation_id: str | None = None
    model_identity: str | None = None
    pack_schema_identity: str | None = None
    prompt_identity: str | None = None
    inference_config: str | None = None
    backend_identity: str | None = None
    runtime_identity: str | None = None
    protocol_identity: str | None = None
    capability_snapshot: str | None = None
    request_digest_field: str | None = None
    seed: str | None = None
    tool_authority_state: str | None = None
    diagnostics: tuple[str, ...] = field(default=())
    replay_of: str | None = None
    reproducibility_scope: str = "SEMANTIC"

    def __post_init__(self) -> None:
        if not self.execution_id:
            raise ArtifactError("artifact: empty execution_id")
        if not self.status:
            raise ArtifactError(
                f"artifact {self.execution_id!r}: empty terminal status"
            )
        if self.reproducibility_scope not in REPRODUCIBILITY_SCOPES:
            raise ArtifactError(
                f"artifact {self.execution_id!r}: unknown "
                f"reproducibility_scope {self.reproducibility_scope!r} "
                f"(closed enum: {sorted(REPRODUCIBILITY_SCOPES)})"
            )
        seen: set[str] = set()
        for name, value in self.frozen_inputs:
            if not name:
                raise ArtifactError(
                    f"artifact {self.execution_id!r}: empty frozen-input name"
                )
            if name in seen:
                raise ArtifactError(
                    f"artifact {self.execution_id!r}: duplicate "
                    f"frozen-input name {name!r}"
                )
            seen.add(name)
            if not isinstance(value, str) or not value:
                raise ArtifactError(
                    f"artifact {self.execution_id!r}: frozen-input "
                    f"{name!r} must be a non-empty str"
                )
        if self.replay_of is not None and not self.replay_of:
            raise ArtifactError(
                f"artifact {self.execution_id!r}: replay_of must be a "
                "non-empty execution_id or None"
            )
        for label, value in (
            ("operation_id", self.operation_id),
            ("model_identity", self.model_identity),
            ("pack_schema_identity", self.pack_schema_identity),
            ("prompt_identity", self.prompt_identity),
            ("inference_config", self.inference_config),
            ("backend_identity", self.backend_identity),
            ("runtime_identity", self.runtime_identity),
            ("protocol_identity", self.protocol_identity),
            ("capability_snapshot", self.capability_snapshot),
            ("seed", self.seed),
            ("tool_authority_state", self.tool_authority_state),
        ):
            if value is not None and not value:
                raise ArtifactError(
                    f"artifact {self.execution_id!r}: {label} must be a "
                    "non-empty identity string or None"
                )

    @classmethod
    def freeze(
        cls,
        execution_id: str,
        status: str,
        frozen_inputs: Mapping[str, str] | Sequence[tuple[str, str]] = (),
        **optional: str | None,
    ) -> ExecutionArtifact:
        """The freeze constructor: the frozen inputs land SORTED (the
        mapping form or the pair form — deterministic regardless of
        caller order, the D4 discipline), and the request digest is
        computed from them when not supplied explicitly."""
        if isinstance(frozen_inputs, Mapping):
            pairs = sorted(frozen_inputs.items())
        else:
            pairs = sorted(frozen_inputs)
        digest = optional.pop("request_digest_field", None)
        if digest is None and pairs:
            digest = request_digest(dict(pairs))
        return cls(
            execution_id=execution_id,
            status=status,
            frozen_inputs=tuple(pairs),
            request_digest_field=digest,
            **optional,
        )

    def to_mapping(self) -> dict[str, object]:
        return {
            "artifact_schema_identity": ARTIFACT_SCHEMA_IDENTITY,
            "backend_identity": self.backend_identity,
            "capability_snapshot": self.capability_snapshot,
            "diagnostics": list(self.diagnostics),
            "execution_id": self.execution_id,
            "frozen_inputs": [list(pair) for pair in self.frozen_inputs],
            "inference_config": self.inference_config,
            "model_identity": self.model_identity,
            "operation_id": self.operation_id,
            "pack_schema_identity": self.pack_schema_identity,
            "prompt_identity": self.prompt_identity,
            "protocol_identity": self.protocol_identity,
            "replay_of": self.replay_of,
            "request_digest": self.request_digest_field,
            "reproducibility_scope": self.reproducibility_scope,
            "runtime_identity": self.runtime_identity,
            "seed": self.seed,
            "status": self.status,
            "tool_authority_state": self.tool_authority_state,
        }

    def to_json(self) -> str:
        """The deterministic serialization (D4: sort_keys + fixed
        separators; byte-identical on rebuild — no hidden clock, no
        PYTHONHASHSEED dependence)."""
        return json.dumps(
            self.to_mapping(), sort_keys=True, separators=(",", ":")
        )

    def inputs_digest(self) -> str | None:
        """The request-kind digest over THIS artifact's frozen inputs
        (the same function the freeze constructor used — the request
        reproducibility check: a stored artifact's inputs re-digest
        to the same value, or something material changed)."""
        if not self.frozen_inputs:
            return None
        return request_digest(dict(self.frozen_inputs))


def artifact_from_mapping(
    data: Mapping[str, object],
) -> ExecutionArtifact:
    """Parse one artifact mapping (the persistence/diagnostic side's
    round-trip; strict — an unknown field is a schema drift, loud,
    the same law as the IR's parser)."""
    known = {
        "artifact_schema_identity",
        *(f for f in ExecutionArtifact.__dataclass_fields__),
    }
    known.add("request_digest")  # the serialized name of the digest field
    unknown = set(data) - known
    if unknown:
        raise ArtifactError(f"artifact: unknown fields {sorted(unknown)}")
    stored = data.get("artifact_schema_identity")
    if stored != ARTIFACT_SCHEMA_IDENTITY:
        raise ArtifactError(
            f"artifact: schema identity {stored!r} != "
            f"{ARTIFACT_SCHEMA_IDENTITY!r} (a version drift — loud, "
            "never a best-effort parse)"
        )
    inputs = data.get("frozen_inputs", [])
    pairs = tuple((str(pair[0]), str(pair[1])) for pair in inputs)
    return ExecutionArtifact(
        execution_id=str(data["execution_id"]),
        status=str(data["status"]),
        frozen_inputs=pairs,
        operation_id=data.get("operation_id"),
        model_identity=data.get("model_identity"),
        pack_schema_identity=data.get("pack_schema_identity"),
        prompt_identity=data.get("prompt_identity"),
        inference_config=data.get("inference_config"),
        backend_identity=data.get("backend_identity"),
        runtime_identity=data.get("runtime_identity"),
        protocol_identity=data.get("protocol_identity"),
        capability_snapshot=data.get("capability_snapshot"),
        request_digest_field=data.get("request_digest"),
        seed=data.get("seed"),
        tool_authority_state=data.get("tool_authority_state"),
        diagnostics=tuple(str(d) for d in data.get("diagnostics", [])),
        replay_of=data.get("replay_of"),
        reproducibility_scope=str(data.get("reproducibility_scope", "SEMANTIC")),
    )
