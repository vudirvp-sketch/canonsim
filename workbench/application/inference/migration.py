"""The one-way settings/1 → settings/2 + inference/1 migration
(ssi-4 step 3, iter-249 — extracted verbatim).

The composition root calls it BEFORE constructing the stores: a
settings/1 document's SEMANTIC fields move into the inference profile
(written ONLY when no profile exists yet — the inference store is the
newer truth, a present profile wins); the settings document is
rewritten as schema/2 carrying ONLY the deployment fields; values
preserved verbatim (jinja: true → chat_template 'model_default').
Idempotent; a malformed document raises LOUD (the operator's saved
values are data).
"""

from __future__ import annotations

import json
import os
from dataclasses import replace
from pathlib import Path

from workbench.application.inference.library import _FIELDS, InferenceError
from workbench.application.inference.profile import (
    InferenceProfile,
    _validate_field,
)
from workbench.application.inference.store import SCHEMA

# ------------------------------------------------------------- migration

#: The launch-settings semantic fields (the schema/1 vocabulary this
#: module ADOPTS — the migration's input contract; the deployment
#: fields stay the settings store's own).
_LAUNCH_SEMANTIC_FIELDS = (
    "context",
    "gpu_layers",
    "flash_attention",
    "temperature",
    "top_k",
    "top_p",
    "min_p",
    "repeat_penalty",
    "jinja",
)

_SETTINGS_SCHEMA_1 = "canonsim.workbench.settings/1"
_SETTINGS_SCHEMA_2 = "canonsim.workbench.settings/2"


def migrate_launch_semantics(
    settings_path: Path, inference_path: Path
) -> bool:
    """The one-way settings/1 → settings/2 + inference/1 migration
    (the composition root calls it BEFORE constructing the stores):

    - a settings/1 document's SEMANTIC fields (the sampler family +
      context/gpu-layers/flash-attention/jinja) move into the
      inference profile — written ONLY when no inference profile
      exists yet (the inference store is the newer truth; a present
      profile wins, the stale launch copy is simply dropped);
    - the settings document is rewritten as schema/2 carrying ONLY
      the deployment fields (llama_server_exe, no_webui,
      extra_args);
    - values are preserved verbatim (jinja: true → chat_template
      'model_default', false → 'generic') — never a silent reset.

    Idempotent: a schema/2 or missing settings file is a no-op. A
    malformed settings document raises LOUD (the operator's saved
    values are data). Returns True when a migration happened."""
    if not settings_path.exists():
        return False
    try:
        raw = settings_path.read_text(encoding="utf-8")
        document = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise InferenceError(
            f"cannot migrate the settings document "
            f"{str(settings_path)!r} ({exc}) — fix it by hand; the "
            "migration never resets the operator's values"
        ) from exc
    if not isinstance(document, dict):
        raise InferenceError(
            f"the settings document {str(settings_path)!r} is not an object"
        )
    schema = document.get("schema")
    if schema != _SETTINGS_SCHEMA_1:
        return False  # schema/2 (already migrated) or a foreign tag
    body = document.get("settings")
    if not isinstance(body, dict):
        raise InferenceError(
            f"the settings document {str(settings_path)!r} has no "
            "settings object"
        )
    semantic = {
        name: body[name] for name in _LAUNCH_SEMANTIC_FIELDS if name in body
    }
    if inference_path.exists():
        try:
            existing = json.loads(inference_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise InferenceError(
                f"the inference profile {str(inference_path)!r} is "
                f"unreadable ({exc}) — fix it by hand; the migration "
                "never overwrites it"
            ) from exc
        if not isinstance(existing, dict) or existing.get("schema") != SCHEMA:
            raise InferenceError(
                f"the inference profile {str(inference_path)!r} carries a "
                f"foreign schema — fix or delete it by hand"
            )
    else:
        jinja = semantic.pop("jinja", True)
        profile_body: dict[str, object] = {
            name: value
            for name, value in semantic.items()
            if name in _FIELDS
        }
        profile_body["chat_template"] = (
            "model_default" if jinja else "generic"
        )
        accepted = {
            name: _validate_field(name, value)
            for name, value in profile_body.items()
        }
        profile = replace(
            InferenceProfile(),
            values={**dict(InferenceProfile().values), **accepted},
        )
        inference_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = inference_path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(
                {
                    "schema": SCHEMA,
                    "profile": profile.as_document(),
                    "workspace": {"pinned": []},
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        os.replace(tmp, inference_path)
    deployment = {
        name: body[name]
        for name in ("llama_server_exe", "no_webui", "extra_args")
        if name in body
    }
    rewritten = {
        "schema": _SETTINGS_SCHEMA_2,
        "settings": deployment,
    }
    tmp = settings_path.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(rewritten, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, settings_path)
    return True
