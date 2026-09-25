"""The inference-profile store (ssi-4 step 3, iter-249 — extracted
verbatim from the single-module era).

The profile owner: load (loud — a corrupt or schema-mismatched file
refuses, never a silently-reset profile) → current() → update()
(validate + apply + persist atomically, thread-safe — the gateway
dispatches on worker threads, the composition root reads current()
at each spawn). The persisted document carries TWO named sections
(one file, one authority, never a second store): `profile` (the
§19.1 BASE document) and `workspace` (the §14 pinned control ids).
The schema tag SCHEMA lives HERE — the persistence layer owns the
document's identity.
"""

from __future__ import annotations

import json
import os
import threading
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path

from workbench.application.inference.chain import DEFAULT_CHAIN, _upgrade_chain
from workbench.application.inference.library import (
    _FIELDS,
    SAMPLER_CHAIN_IDS,
    InferenceError,
)
from workbench.application.inference.profile import (
    InferenceProfile,
    _validate_field,
    _validate_pinned,
)

#: The persisted document's schema tag (§15.3's schema-evolution law —
#: the inf-2 extension ADDS fields/categories without renaming or
#: removing any inf-1 field: an old profile loads as-is, its absent
#: fields take the library baselines, its 5-member chain upgrades to
#: the 9-member set at load).
SCHEMA = "canonsim.workbench.inference/1"


# ---------------------------------------------------------------- the store


class InferenceStore:
    """The inference-profile owner: load (loud) → current() → update()
    (validate + apply + persist atomically). Thread-safe (the gateway
    dispatches on worker threads; the composition root reads
    `current()` at each spawn — settings.py's own policy-clock law).

    The persisted document carries TWO named sections (one file, one
    authority, never a second store): `profile` (the §19.1 BASE
    document: name + values + the chain) and `workspace` (the §14
    live state: the pinned control ids — an absent section is the
    honest empty, the file predates the section)."""

    def __init__(self, path: Path) -> None:
        if not isinstance(path, Path):
            raise InferenceError("the profile path must be a pathlib.Path")
        if not path.is_absolute():
            raise InferenceError(
                f"the profile path {str(path)!r} is relative — the "
                ".git/CWD-independence law (app §16) requires an "
                "absolute path from the composition root"
            )
        self._path = path
        self._lock = threading.Lock()
        self._profile, self._pinned = self._load()

    @property
    def path(self) -> Path:
        return self._path

    def current(self) -> InferenceProfile:
        with self._lock:
            return self._profile

    def pinned(self) -> tuple[str, ...]:
        """The workspace's pinned control ids (§14 — the ordering
        policy's own first rung: an explicit personal pin)."""
        with self._lock:
            return self._pinned

    def update(self, partial: Mapping[str, object]) -> InferenceProfile:
        """§19.1's REQUESTED→ACCEPTED→EFFECTIVE half: validate the
        CLOSED partial document (absent fields unchanged), apply, and
        persist atomically — the returned value is the new current.
        The `pinned` key routes to the WORKSPACE section (never the
        profile values); `name`/`sampler_chain`/value fields route to
        the profile."""
        if not isinstance(partial, Mapping):
            raise InferenceError("the update payload must be a mapping")
        allowed = {"name", "sampler_chain", "pinned", *_FIELDS}
        unknown = sorted(set(partial) - allowed)
        if unknown:
            raise InferenceError(
                f"unknown field(s) {unknown} (closed set: {list(allowed)})"
            )
        accepted = {
            name: _validate_field(name, value)
            for name, value in partial.items()
        }
        with self._lock:
            new_values = {
                **self._profile.values,
                **{
                    key: value
                    for key, value in accepted.items()
                    if key in _FIELDS
                },
            }
            updated = replace(
                self._profile,
                name=accepted.get("name", self._profile.name),
                values=new_values,
                sampler_chain=accepted.get(
                    "sampler_chain", self._profile.sampler_chain
                ),
            )
            self._profile = updated
            if "pinned" in accepted:
                self._pinned = accepted["pinned"]  # type: ignore[assignment]
            self._persist_locked(self._profile, self._pinned)
            return self._profile

    # ------------------------------------------------------------ private

    def _load(self) -> tuple[InferenceProfile, tuple[str, ...]]:
        """The §16 startup/recovery read (settings.py's own law): a
        MISSING file is the honest defaults (the file appears on the
        first save); a corrupt or schema-mismatched file refuses
        LOUD — never a silently-reset profile. The inf-1 → inf-2
        chain upgrade rides here (§_upgrade_chain: the 5-member chain
        grows to the 9-member set, the operator's order preserved)."""
        if not self._path.exists():
            return InferenceProfile(), ()
        try:
            raw = self._path.read_text(encoding="utf-8")
            document = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            raise InferenceError(
                f"the inference profile {str(self._path)!r} is unreadable "
                f"({exc}) — fix or delete it by hand; it is never reset "
                "silently"
            ) from exc
        if not isinstance(document, dict):
            raise InferenceError(
                f"the inference profile {str(self._path)!r} is not an object"
            )
        if document.get("schema") != SCHEMA:
            raise InferenceError(
                f"the inference profile {str(self._path)!r} carries schema "
                f"{document.get('schema')!r}, expected {SCHEMA!r} — "
                "migrate or delete it by hand"
            )
        unknown_top = sorted(set(document) - {"schema", "profile", "workspace"})
        if unknown_top:
            raise InferenceError(
                f"the inference profile carries unknown section(s) "
                f"{unknown_top} (closed set: ['profile', 'workspace'])"
            )
        body = document.get("profile")
        if not isinstance(body, dict):
            raise InferenceError(
                f"the inference profile {str(self._path)!r} has no profile "
                "object"
            )
        workspace = document.get("workspace", {})
        if not isinstance(workspace, dict):
            raise InferenceError(
                f"the inference profile {str(self._path)!r} has a "
                "malformed workspace section"
            )
        pinned_raw = workspace.get("pinned", [])
        pinned = _validate_pinned(pinned_raw)
        unknown = sorted(set(body) - {"name", "sampler_chain", *_FIELDS})
        if unknown:
            raise InferenceError(
                f"the inference profile carries unknown field(s) {unknown} "
                f"(closed set: {list(_FIELDS)})"
            )
        chain_raw = body.get("sampler_chain")
        if chain_raw is not None:
            if not isinstance(chain_raw, list) or not chain_raw:
                raise InferenceError(
                    "the persisted sampler_chain must be a non-empty list"
                )
            loaded: dict[str, bool] = {}
            for item in chain_raw:
                if (
                    not isinstance(item, dict)
                    or set(item) != {"id", "enabled"}
                    or item["id"] not in SAMPLER_CHAIN_IDS
                    or not isinstance(item["enabled"], bool)
                ):
                    raise InferenceError(
                        "the persisted sampler_chain carries a malformed "
                        f"member {item!r}"
                    )
                loaded[str(item["id"])] = bool(item["enabled"])
            chain = _upgrade_chain(loaded)
        else:
            chain = DEFAULT_CHAIN
        accepted = {
            name: _validate_field(name, value)
            for name, value in body.items()
            if name not in ("name", "sampler_chain")
        }
        name = (
            _validate_field("name", body["name"]) if "name" in body else "Baseline"
        )
        profile = replace(
            InferenceProfile(),
            name=name,
            values={**dict(InferenceProfile().values), **accepted},
            sampler_chain=chain,
        )
        return profile, pinned

    def _persist_locked(
        self, profile: InferenceProfile, pinned: tuple[str, ...]
    ) -> None:
        """The atomic write (§15's crash-safety half): a tmp file in
        the same directory + os.replace — a crash never leaves a
        half-written profile behind."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            document = {
                "schema": SCHEMA,
                "profile": profile.as_document(),
                "workspace": {"pinned": list(pinned)},
            }
            tmp_path = self._path.with_suffix(".json.tmp")
            tmp_path.write_text(
                json.dumps(document, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            os.replace(tmp_path, self._path)
        except OSError as exc:
            raise InferenceError(
                f"cannot persist the inference profile to "
                f"{str(self._path)!r}: {exc}"
            ) from exc
