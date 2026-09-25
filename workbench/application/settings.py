"""The launch-settings store + the backend.settings operations (wb-9,
the app spec §§7.1/19/20 — the owner's 2026-09-25 «настройки запуска
llama.cpp, флаги как минимум основные + список остальных скрытый или
свёрнутый, сэмплеры всякие» call; the DEPLOYMENT half after inf-1's
Settings ≠ Inference Control split).

The law this module closes: the managed llama-server's LAUNCH
settings are CONFIGURATION (§7.1's user-configuration role), not
code — a typed, validated, persisted document the Workbench UI reads
and writes over the gateway, with the honest §18/§19.1 chain:

```text
REQUESTED  what the UI's Save sent (the closed field set)
ACCEPTED   what passed validation (closed vocabularies — rejected
           loud, never clamped)
EFFECTIVE  what the NEXT spawn will use (the composition root's
           provider merges the store with the CLI overrides)
OBSERVED   the actual command the spawn ran (the managed backend's
           evidence line — workbench_app.py's own surface)
PRESENTED  what the Settings surface shows (the READ document + the
           command preview)
```

inf-1's ownership split (LLAMA_CPP_INFERENCE_CONTROL_LAW §1 — the
chip specification's own law): THIS store owns DEPLOYMENT ONLY —
the executable preference, the web-UI surface, the raw extra_args
escape hatch. The SEMANTIC generation-control values (context,
GPU placement, flash attention, fit, KV types, the sampler family,
seed, the chat template, the sampler chain) moved to the inference
profile store (`workbench/application/inference.py`) — the §19.1
BASE PROFILE layer. The one-way schema/1 → schema/2 migration lives
there (`migrate_launch_semantics`, the composition root's own
boot step — the operator's saved values move verbatim, never a
silent reset).

`extra_args` stays the RAW COMPATIBILITY / DEBUG ESCAPE HATCH (the
law's §13): the operator's own flags verbatim, NEVER the semantic
storage system — the composition root's compile step rejects a
duplicate flag ownership loudly (a semantic Top-K plus a raw
`--top-k` is a conflict surfaced, never an ambiguous precedence).

The honest limits, named in the surface itself: a settings update
applies at the NEXT model.load spawn — a LIVE server keeps its flags
until unloaded (the §11.1 replacement path is a later row); the
endpoint host/port are NOT settings (loopback-fixed by the exposure
law, CLI-overridable, restart-scoped); llama-server's own per-request
surface may still override the sampler defaults per call (§19.1's
EFFECTIVE never silently wins OBSERVED).

Persistence (§16's USER_CONFIG role): one JSON file under the runtime
root (`workbench/runtime/settings.json`, gitignored), schema-tagged,
atomically written (tmp + os.replace), loaded loud — a corrupt or
schema-mismatched file refuses to start with the fix note, never a
silent reset (the operator's own saved values are data, not cache).

Zero network, zero engine imports, zero platform imports (the command
preview is INJECTED by the composition root — the one place platform
mechanics are wired); stdlib only (D-012, §27's envelope holds).
"""

from __future__ import annotations

import json
import os
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from pathlib import Path

from workbench.api.gateway import (
    Gateway,
    OperationRejected,
    OperationSpec,
)

__all__ = [
    "SCHEMA",
    "LaunchSettings",
    "SettingsError",
    "SettingsStore",
    "register_settings_operations",
]

#: The deployment owner's own defaults (§7.1 — this module IS the
#: launch-settings DEPLOYMENT owner after inf-1's split; the semantic
#: generation-control baseline lives in the inference profile's own
#: defaults, and the composition root passes EVERY field explicitly
#: at each spawn — the builder's fallbacks never shadow them).
DEFAULTS: dict[str, object] = {
    "llama_server_exe": "",
    "no_webui": True,
    "extra_args": "",
}

#: The persisted document's schema tag (§15.3's schema-evolution law:
#: inf-1's Settings ≠ Inference Control split moved the semantic
#: fields to the inference profile — a schema/1 document migrates
#: through `workbench/application/inference.py`'s
#: `migrate_launch_semantics` at composition boot; a file with a
#: foreign tag refuses to load, never a guessed mapping).
SCHEMA = "canonsim.workbench.settings/2"

#: The closed field set (the store's whole vocabulary — anything else
#: in an update or a persisted file is LOUD, never ignored).
_FIELDS = (
    "llama_server_exe",
    "no_webui",
    "extra_args",
)


class SettingsError(ValueError):
    """A settings contract violation (LOUD — a malformed persisted
    file, an out-of-range value; never a silent reset or clamp)."""


@dataclass(frozen=True)
class LaunchSettings:
    """The typed launch-settings document — the managed spawn's own
    DEPLOYMENT knobs (inf-1's split: the semantic generation controls
    live in `workbench/application/inference.py`'s profile store —
    Settings ≠ Inference Control, the law's §1).

    `llama_server_exe` is a PREFERENCE, not a resolved path: "" means
    auto-discovery (the runtime/llama.cpp folder, then PATH — the
    composition root owns the resolution and the preview shows the
    effective command). `extra_args` is the raw escape hatch (the
    law's §13 — duplicate flag ownership against the semantic layer
    rejects loudly at the compile step)."""

    llama_server_exe: str = ""
    no_webui: bool = True
    extra_args: str = ""

    def as_document(self) -> dict[str, object]:
        """The JSON-safe read view (the wire shape — the field order
        fixed, the values verbatim)."""
        return {
            "llama_server_exe": self.llama_server_exe,
            "no_webui": self.no_webui,
            "extra_args": self.extra_args,
        }


def _validate_field(name: str, value: object) -> object:
    """One field's acceptance law: the closed type per field, rejected
    LOUD (§19.1's VALIDATED step — never a silent clamp)."""
    if name == "llama_server_exe":
        if not isinstance(value, str):
            raise SettingsError(
                "llama_server_exe must be a str (empty = auto)"
            )
        return value
    if name == "no_webui":
        if not isinstance(value, bool):
            raise SettingsError(f"{name} {value!r} must be a bool")
        return value
    if name == "extra_args":
        if not isinstance(value, str):
            raise SettingsError(f"{name} {value!r} must be a str")
        return value
    raise SettingsError(f"unknown field {name!r} (closed set: {list(_FIELDS)})")


class SettingsStore:
    """The launch-settings owner: load (loud) → current() → update()
    (validate + apply + persist atomically). Thread-safe — the gateway
    dispatches on worker threads; the managed backend reads `current()`
    at each spawn (its own policy clock, never a shared cache)."""

    def __init__(self, path: Path) -> None:
        if not isinstance(path, Path):
            raise SettingsError("the settings path must be a pathlib.Path")
        if not path.is_absolute():
            raise SettingsError(
                f"the settings path {str(path)!r} is relative — the "
                ".git/CWD-independence law (app §16) requires an "
                "absolute path from the composition root"
            )
        self._path = path
        self._lock = threading.Lock()
        self._settings = self._load()

    @property
    def path(self) -> Path:
        return self._path

    def current(self) -> LaunchSettings:
        with self._lock:
            return self._settings

    def update(self, partial: Mapping[str, object]) -> LaunchSettings:
        """§19.1's REQUESTED→ACCEPTED→EFFECTIVE half: validate the
        CLOSED partial document (absent fields unchanged), apply, and
        persist atomically — the returned value is the new current
        (the caller's evidence, never a guess about the file)."""
        if not isinstance(partial, Mapping):
            raise SettingsError("the update payload must be a mapping")
        unknown = sorted(set(partial) - set(_FIELDS))
        if unknown:
            raise SettingsError(
                f"unknown field(s) {unknown} (closed set: {list(_FIELDS)})"
            )
        accepted = {
            name: _validate_field(name, value)
            for name, value in partial.items()
        }
        with self._lock:
            updated = replace(self._settings, **accepted)
            self._persist_locked(updated)
            self._settings = updated
            return updated

    # ------------------------------------------------------------ private

    def _load(self) -> LaunchSettings:
        """The §16 startup/recovery read: a MISSING file is the honest
        defaults (the file appears on the first save); a corrupt or
        schema-mismatched file refuses LOUD — the operator's saved
        values are data, never a silently-reset cache."""
        if not self._path.exists():
            return LaunchSettings()
        try:
            raw = self._path.read_text(encoding="utf-8")
            document = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            raise SettingsError(
                f"the settings file {str(self._path)!r} is unreadable "
                f"({exc}) — fix or delete it by hand; it is never reset "
                "silently"
            ) from exc
        if not isinstance(document, dict):
            raise SettingsError(
                f"the settings file {str(self._path)!r} is not an object"
            )
        if document.get("schema") != SCHEMA:
            raise SettingsError(
                f"the settings file {str(self._path)!r} carries schema "
                f"{document.get('schema')!r}, expected {SCHEMA!r} — "
                "migrate or delete it by hand"
            )
        body = document.get("settings")
        if not isinstance(body, dict):
            raise SettingsError(
                f"the settings file {str(self._path)!r} has no settings "
                "object"
            )
        unknown = sorted(set(body) - set(_FIELDS))
        if unknown:
            raise SettingsError(
                f"the settings file carries unknown field(s) {unknown} "
                f"(closed set: {list(_FIELDS)})"
            )
        accepted = {
            name: _validate_field(name, value) for name, value in body.items()
        }
        return replace(LaunchSettings(), **accepted)

    def _persist_locked(self, settings: LaunchSettings) -> None:
        """The atomic write (§15's crash-safety half): a tmp file in
        the same directory + os.replace — a crash never leaves a
        half-written settings file behind."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            document = {
                "schema": SCHEMA,
                "settings": settings.as_document(),
            }
            tmp_path = self._path.with_suffix(".json.tmp")
            tmp_path.write_text(
                json.dumps(document, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            os.replace(tmp_path, self._path)
        except OSError as exc:
            raise SettingsError(
                f"cannot persist the settings to {str(self._path)!r}: {exc}"
            ) from exc


# ------------------------------------------------------------- operations


def _rejected(reason: str) -> OperationRejected:
    return OperationRejected("DOMAIN_REJECTED", reason)


def register_settings_operations(
    gateway: Gateway,
    store: SettingsStore,
    *,
    command_preview: Callable[[Mapping[str, object]], str] | None = None,
    managed_live: Callable[[], bool] | None = None,
) -> None:
    """The settings family's wiring (the composition root calls it —
    §6.1's single-owner law): the READ (the effective document + the
    injected command preview + the managed liveness) and the UPDATE
    (the closed partial document, validated through the store, the
    honest next-spawn note). The preview and liveness callables are
    INJECTED — this module never imports the platform or the managed
    backend (the composition root owns that wiring)."""
    gateway.register(
        OperationSpec(
            name="backend.settings",
            kind="READ",
            handler=_make_settings_read(store, command_preview, managed_live),
            description=(
                "the launch-settings document (§7.1/§19) + the effective "
                "command preview — the Settings surface's own read"
            ),
        )
    )
    gateway.register(
        OperationSpec(
            name="backend.settings.update",
            kind="MUTATION",
            handler=_make_settings_update(store, command_preview, managed_live),
            session_scoped=True,
            description=(
                "the closed partial update (validated, persisted — "
                "effective at the NEXT managed spawn, §11.1's "
                "replacement path being a later row)"
            ),
        )
    )


def _settings_document(
    store: SettingsStore,
    command_preview: Callable[[Mapping[str, object]], str] | None,
    live: Callable[[], bool] | None,
) -> dict[str, object]:
    current = store.current().as_document()
    live_now = bool(live is not None and live())
    document: dict[str, object] = {
        "settings": current,
        "managed_live": live_now,
        "applies": "next-spawn",
    }
    if command_preview is not None:
        document["command_preview"] = command_preview(current)
    else:
        document["command_preview"] = None
    if live_now:
        document["note"] = (
            "a LIVE server keeps its launch flags until unloaded — the "
            "saved values apply at the next model.load"
        )
    return document


def _make_settings_read(
    store: SettingsStore,
    command_preview: Callable[[Mapping[str, object]], str] | None,
    live: Callable[[], bool] | None,
):
    def handler(context) -> Mapping[str, object]:
        if context.arguments:
            raise _rejected(
                f"backend.settings: takes no arguments "
                f"({sorted(context.arguments)})"
            )
        return _settings_document(store, command_preview, live)

    return handler


def _make_settings_update(
    store: SettingsStore,
    command_preview: Callable[[Mapping[str, object]], str] | None,
    live: Callable[[], bool] | None,
):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        try:
            store.update(arguments)
        except SettingsError as exc:
            raise _rejected(f"backend.settings.update: {exc}") from exc
        if context.effects is not None:
            context.effects.effect(
                {"effect": "SETTINGS_UPDATED", "fields": sorted(arguments)}
            )
        return _settings_document(store, command_preview, live)

    return handler
