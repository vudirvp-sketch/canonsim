"""The identity closure (wb-3, the app spec §9 — the family's third
row).

The law: **path is location, not identity.**

```text
logical_name + revision/version + strong content identity
+ relevant schema/metadata identity = material identity
```

Multi-file, sharded, multimodal or adapter-based assets use a
deterministic composite identity over all material constituents
(`CompositeIdentity` — order-independent: the constituents enter the
digest sorted, so two construction orders of the same material yield
the same composite, the D4 read-side discipline).

The vocabulary distinguishes `logical_name`, `revision`, 
`content_digest`, `location`, `metadata` — five different axes a
`ContentIdentity` keeps apart. The mismatch laws (§9):

```text
same path + new bytes      → new content identity
same name + new revision   → new revision identity
same revision + new bytes  → identity mismatch; never silently reuse
```

`recheck()` makes the third law executable: a stored identity against
actual bytes returns VERIFIED, MISMATCH (loud — the caller refuses
reuse), or INTEGRITY_UNKNOWN (the stored digest itself was never
strongly established — failed/incomplete hashing is explicit, never
a quiet pass).

Size/mtime/platform file identity may be a cheap scan fingerprint;
it is not a correctness identity and does not appear here. Hashing
is sha256 in hex form — the same primitive as `core/rng.py`'s
`stable_hash` (the int form kept for stream seeding); the hex form
is the content-identity form (§9 "strong content identity").
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Iterable

#: The integrity vocabulary (§9 + the explicit failed-hash state).
INTEGRITY_STATUSES: frozenset[str] = frozenset(
    {"VERIFIED", "MISMATCH", "INTEGRITY_UNKNOWN"}
)

#: The digest form: sha256, 64 hex chars, lowercase.
DIGEST_HEX_LENGTH = 64

#: The identity axes a ContentIdentity keeps apart (§9's vocabulary:
#: logical_name / revision / content_digest / location / metadata).
IDENTITY_AXES: tuple[str, ...] = (
    "logical_name",
    "revision",
    "content_digest",
    "location",
    "metadata",
)


class IdentityError(ValueError):
    """A malformed identity document (construction-time, never
    silent — the same law as the Scene IR's error class)."""


def content_digest(data: bytes | str) -> str:
    """The strong content identity of one material's bytes.

    Deterministic (sha256 hexdigest; str is UTF-8 encoded) — the same
    bytes (or the same str) always yield the same digest, with zero
    dependence on PYTHONHASHSEED (INV-2's read-side discipline).
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _valid_digest(digest: str | None) -> bool:
    return (
        isinstance(digest, str)
        and len(digest) == DIGEST_HEX_LENGTH
        and all(c in "0123456789abcdef" for c in digest)
    )


@dataclass(frozen=True)
class ContentIdentity:
    """One material's identity: the five §9 axes apart.

    `content_digest` is the strong content identity (sha256 hex) or
    None — None means the digest was never strongly established and
    every integrity question about this material answers
    INTEGRITY_UNKNOWN, never a quiet pass (§9's explicit-failure law).
    """

    logical_name: str
    revision: str
    content_digest: str | None
    location: str | None = None
    metadata: tuple[tuple[str, str], ...] = field(default=())

    def __post_init__(self) -> None:
        if not self.logical_name:
            raise IdentityError("identity: empty logical_name")
        if not self.revision:
            raise IdentityError(
                f"identity {self.logical_name!r}: empty revision"
            )
        if self.content_digest is not None and not _valid_digest(
            self.content_digest
        ):
            raise IdentityError(
                f"identity {self.logical_name!r}: malformed "
                f"content_digest (want {DIGEST_HEX_LENGTH} lowercase "
                "hex chars, or None for INTEGRITY_UNKNOWN)"
            )
        seen: set[str] = set()
        for key, value in self.metadata:
            if not key:
                raise IdentityError(
                    f"identity {self.logical_name!r}: empty metadata key"
                )
            if key in seen:
                raise IdentityError(
                    f"identity {self.logical_name!r}: duplicate "
                    f"metadata key {key!r}"
                )
            seen.add(key)
            if not isinstance(value, str):
                raise IdentityError(
                    f"identity {self.logical_name!r}: metadata "
                    f"{key!r} must be a str (got {type(value).__name__})"
                )

    @classmethod
    def from_bytes(
        cls,
        logical_name: str,
        revision: str,
        data: bytes | str,
        location: str | None = None,
        metadata: Iterable[tuple[str, str]] = (),
    ) -> ContentIdentity:
        """Freeze a material's identity from its actual bytes — the
        digest is computed here, once, and never recomputed from a
        path afterwards (path is location, not identity)."""
        return cls(
            logical_name=logical_name,
            revision=revision,
            content_digest=content_digest(data),
            location=location,
            metadata=tuple(sorted(metadata)),
        )

    def material_identity(self) -> str:
        """The material identity string: the composite digest over
        the name, revision, content digest, location and metadata —
        the §9 equation, serialized deterministically (sorted keys,
        fixed separators — the D4 discipline)."""
        payload = {
            "content_digest": self.content_digest,
            "location": self.location,
            "logical_name": self.logical_name,
            "metadata": [list(pair) for pair in sorted(self.metadata)],
            "revision": self.revision,
        }
        return content_digest(
            json.dumps(payload, sort_keys=True, separators=(",", ":"))
        )

    def recheck(self, data: bytes | str) -> str:
        """The third mismatch law, executable: this identity against
        actual bytes.

        VERIFIED           — the stored digest matches the bytes;
        MISMATCH           — same identity, new bytes: the caller
                             MUST refuse reuse (never silent);
        INTEGRITY_UNKNOWN  — the stored digest itself was never
                             strongly established (None) — explicit
                             uncertainty, never a quiet pass.
        """
        if self.content_digest is None:
            return "INTEGRITY_UNKNOWN"
        actual = content_digest(data)
        return "VERIFIED" if actual == self.content_digest else "MISMATCH"

    def to_mapping(self) -> dict[str, object]:
        return {
            "content_digest": self.content_digest,
            "location": self.location,
            "logical_name": self.logical_name,
            "metadata": [list(pair) for pair in sorted(self.metadata)],
            "revision": self.revision,
        }


@dataclass(frozen=True)
class CompositeIdentity:
    """The deterministic composite identity over all material
    constituents of one logical asset (§9: multi-file, sharded,
    multimodal or adapter-based).

    Order-independent by construction: the constituents' material
    identities enter the composite digest SORTED, so the same set of
    material always yields the same composite regardless of the order
    it was assembled in (the INV-2 read-side rule: iteration only via
    sorted() or construction order — here sorted wins, because a
    shard set has no meaningful construction order).
    """

    logical_name: str
    revision: str
    constituents: tuple[ContentIdentity, ...]

    def __post_init__(self) -> None:
        if not self.logical_name:
            raise IdentityError("composite: empty logical_name")
        if not self.revision:
            raise IdentityError(
                f"composite {self.logical_name!r}: empty revision"
            )
        if not self.constituents:
            raise IdentityError(
                f"composite {self.logical_name!r}: no constituents "
                "(a composite identity needs its material)"
            )
        names = [c.logical_name for c in self.constituents]
        duplicated = sorted({n for n in names if names.count(n) > 1})
        if duplicated:
            raise IdentityError(
                f"composite {self.logical_name!r}: duplicate "
                f"constituent logical_name(s) {duplicated} — a shard "
                "set names each material once"
            )

    def composite_digest(self) -> str:
        """The composite material identity: sha256 over the sorted
        constituent material identities + the composite's own name
        and revision."""
        payload = {
            "constituents": sorted(
                c.material_identity() for c in self.constituents
            ),
            "logical_name": self.logical_name,
            "revision": self.revision,
        }
        return content_digest(
            json.dumps(payload, sort_keys=True, separators=(",", ":"))
        )

    def integrity(self) -> str:
        """The composite's integrity answer: VERIFIED only when every
        constituent is strongly digested; INTEGRITY_UNKNOWN the moment
        any constituent is (a partial-identity composite is never a
        verified composite — explicit, never a quiet pass)."""
        if any(c.content_digest is None for c in self.constituents):
            return "INTEGRITY_UNKNOWN"
        return "VERIFIED"
