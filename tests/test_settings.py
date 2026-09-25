"""wb-9's claim packet — the launch-settings store + the
backend.settings operations (`workbench/application/settings.py`).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE STORE LAWS: the missing file is the honest defaults (the file
   appears only on the first save); the update validates the CLOSED
   field set (types, rejected loud — never clamped), applies the
   partial (absent fields unchanged), and persists ATOMICALLY
   (the schema-tagged document a fresh store re-reads identically).
   inf-1: the store is the DEPLOYMENT half (schema/2 — the semantic
   generation-control fields moved to the inference profile; the old
   schema/1 field names now reject LOUD, never a guessed mapping).
2. THE LOAD LAWS: a corrupt file, a foreign schema tag, an unknown
   field, a bad value — each refuses to load LOUD (the operator's
   saved values are data, never a silently-reset cache); a relative
   path is the .git/CWD-independence law's own rejection.
3. THE OPERATIONS: backend.settings answers the effective document
   (+ the injected command preview + the managed liveness + the
   next-spawn note); backend.settings.update walks the store's own
   validation (DOMAIN_REJECTED carrier), emits the SETTINGS_UPDATED
   effect, and persists; the READ takes no arguments; a corrupt store
   never reaches the gateway (the composition's loud refusal).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from workbench.api.contract import RequestEnvelope  # noqa: E402
from workbench.api.gateway import Gateway  # noqa: E402
from workbench.application.settings import (  # noqa: E402
    SCHEMA,
    LaunchSettings,
    SettingsError,
    SettingsStore,
    register_settings_operations,
)


def _store(tmp_path: Path) -> SettingsStore:
    return SettingsStore(tmp_path / "settings.json")


# ------------------------------------------------------- the store laws


def test_the_missing_file_is_the_honest_defaults(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    store = SettingsStore(path)
    assert not path.exists(), "the file appears only on the first save"
    current = store.current()
    assert current == LaunchSettings()
    assert current.llama_server_exe == ""
    assert current.no_webui is True
    assert current.extra_args == ""


def test_the_schema1_semantic_fields_reject_loud(tmp_path: Path) -> None:
    """inf-1's ownership split, executable: the SEMANTIC field names
    are no longer this store's vocabulary — every one rejects LOUD
    (the closed set is the whole law; the values live in the
    inference profile store now)."""
    store = _store(tmp_path)
    for gone in (
        "context",
        "gpu_layers",
        "flash_attention",
        "jinja",
        "temperature",
        "top_k",
        "top_p",
        "min_p",
        "repeat_penalty",
    ):
        with pytest.raises(SettingsError, match="unknown field"):
            store.update({gone: 1})


def test_the_update_validates_applies_and_persists(
    tmp_path: Path,
) -> None:
    path = tmp_path / "settings.json"
    store = SettingsStore(path)
    updated = store.update(
        {"llama_server_exe": "D:/llama.cpp/llama-server.exe",
         "no_webui": False,
         "extra_args": "--verbose"}
    )
    assert updated.llama_server_exe == "D:/llama.cpp/llama-server.exe"
    assert updated.no_webui is False
    assert updated.extra_args == "--verbose"
    # the atomic persistence: the schema-tagged document on disk
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["schema"] == SCHEMA
    assert document["settings"]["llama_server_exe"] == (
        "D:/llama.cpp/llama-server.exe"
    )
    # a FRESH store re-reads the same values (the roundtrip)
    assert SettingsStore(path).current() == updated


def test_the_update_rejections_are_loud(tmp_path: Path) -> None:
    store = _store(tmp_path)
    for bad in (
        {"llama_server_exe": None},
        {"llama_server_exe": 8},
        {"no_webui": "yes"},
        {"extra_args": 8},
        {"nope": 1},
    ):
        with pytest.raises(SettingsError, match=sorted(bad)[0].replace(".", "")):
            store.update(bad)
    assert store.current() == LaunchSettings(), "no partial application"


def test_the_update_rejects_non_mappings(tmp_path: Path) -> None:
    store = _store(tmp_path)
    with pytest.raises(SettingsError, match="mapping"):
        store.update([("context", 4096)])  # type: ignore[arg-type]


def test_the_load_refuses_loud(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    # corrupt JSON
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(SettingsError, match="unreadable"):
        SettingsStore(path)
    # a foreign schema tag
    path.write_text(
        json.dumps({"schema": "canonsim.workbench.settings/0",
                    "settings": {}}),
        encoding="utf-8",
    )
    with pytest.raises(SettingsError, match="schema"):
        SettingsStore(path)
    # no settings object
    path.write_text(json.dumps({"schema": SCHEMA}), encoding="utf-8")
    with pytest.raises(SettingsError, match="settings"):
        SettingsStore(path)
    # unknown fields in the file
    path.write_text(
        json.dumps({"schema": SCHEMA, "settings": {"nope": 1}}),
        encoding="utf-8",
    )
    with pytest.raises(SettingsError, match="unknown field"):
        SettingsStore(path)
    # a bad value in the file
    path.write_text(
        json.dumps({"schema": SCHEMA, "settings": {"no_webui": "yes"}}),
        encoding="utf-8",
    )
    with pytest.raises(SettingsError, match="no_webui"):
        SettingsStore(path)
    # a schema/1 document (the pre-split form): the loud refusal with
    # the migration's own name (the composition root migrates at boot;
    # a hand-rolled load never guesses a mapping)
    path.write_text(
        json.dumps(
            {"schema": "canonsim.workbench.settings/1", "settings": {}}
        ),
        encoding="utf-8",
    )
    with pytest.raises(SettingsError, match="schema"):
        SettingsStore(path)


def test_the_relative_path_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(SettingsError, match="relative"):
        SettingsStore(Path("settings.json"))
    with pytest.raises(SettingsError, match="Path"):
        SettingsStore("settings.json")  # type: ignore[arg-type]


# ------------------------------------------------------ the operations


def _gateway_with(
    store: SettingsStore,
    *,
    preview=None,
    managed_live=None,
):
    gateway = Gateway()
    register_settings_operations(
        gateway, store, command_preview=preview, managed_live=managed_live
    )
    return gateway


def _session(gateway: Gateway, key: str) -> str:
    response = gateway.dispatch(
        RequestEnvelope(
            operation="session.create",
            arguments={},
            client_request_id=key,
        )
    )
    assert response.status == "OK", response.to_mapping()
    return str(response.result["session_id"])


def test_backend_settings_answers_the_effective_document(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path)
    preview_calls: list[dict] = []

    def preview(current):
        preview_calls.append(dict(current))
        return "llama-server -m <model.gguf> --no-webui %s" % current["extra_args"]

    gateway = _gateway_with(
        store, preview=preview, managed_live=lambda: False
    )
    reply = gateway.dispatch(
        RequestEnvelope(operation="backend.settings", arguments={})
    )
    assert reply.status == "OK", reply.to_mapping()
    result = reply.result
    assert result["settings"] == LaunchSettings().as_document()
    assert result["managed_live"] is False
    assert result["applies"] == "next-spawn"
    assert result["command_preview"] == (
        "llama-server -m <model.gguf> --no-webui "
    )
    assert result.get("note") is None, "the LIVE note rides the live form"
    assert preview_calls, "the preview rode the injected callable"
    # the READ takes no arguments — the closed surface
    bad = gateway.dispatch(
        RequestEnvelope(
            operation="backend.settings", arguments={"no_webui": 1}
        )
    )
    assert bad.status != "OK"


def test_backend_settings_update_walks_the_store(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    store = SettingsStore(path)
    gateway = _gateway_with(
        store, preview=lambda c: "cmd", managed_live=lambda: True
    )
    session = _session(gateway, "wb9-settings-ops")
    reply = gateway.dispatch(
        RequestEnvelope(
            operation="backend.settings.update",
            arguments={"no_webui": False, "extra_args": "--verbose"},
            session_id=session,
            client_request_id="wb9-update",
        )
    )
    assert reply.status == "OK", reply.to_mapping()
    result = reply.result
    assert result["settings"]["no_webui"] is False
    assert result["settings"]["extra_args"] == "--verbose"
    assert result["settings"]["llama_server_exe"] == ""  # absent unchanged
    assert result["managed_live"] is True
    assert "note" in result and "LIVE" in result["note"]
    # persisted + served to a fresh read
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["settings"]["extra_args"] == "--verbose"
    read = gateway.dispatch(
        RequestEnvelope(operation="backend.settings", arguments={})
    )
    assert read.result["settings"]["no_webui"] is False
    # the ordered event stream carries the SETTINGS_UPDATED effect
    events = gateway.dispatch(
        RequestEnvelope(
            operation="session.events",
            arguments={},
            session_id=session,
        )
    )
    effects = [e for e in events.result["events"] if "SETTINGS" in str(e)]
    assert effects, "the update emitted its dispatch-time effect"


def test_backend_settings_update_rejects_loud(tmp_path: Path) -> None:
    store = _store(tmp_path)
    gateway = _gateway_with(store)
    session = _session(gateway, "wb9-reject")
    for index, bad in enumerate(
        ({"context": 0}, {"temperature": 9.9}, {"nope": 1})
    ):
        reply = gateway.dispatch(
            RequestEnvelope(
                operation="backend.settings.update",
                arguments=bad,
                session_id=session,
                client_request_id=f"wb9-bad-{index}",
            )
        )
        assert reply.status != "OK", bad
        assert reply.rejection == "DOMAIN_REJECTED"
    assert store.current() == LaunchSettings()


def test_the_update_requires_the_session_and_the_key(tmp_path: Path) -> None:
    store = _store(tmp_path)
    gateway = _gateway_with(store)
    # no session: the mutation refuses
    no_session = gateway.dispatch(
        RequestEnvelope(
            operation="backend.settings.update",
            arguments={"context": 2048},
            client_request_id="wb9-nosession",
        )
    )
    assert no_session.status != "OK"
    session = _session(gateway, "wb9-key")
    # no idempotency key: the mutation refuses (G4)
    no_key = gateway.dispatch(
        RequestEnvelope(
            operation="backend.settings.update",
            arguments={"context": 2048},
            session_id=session,
        )
    )
    assert no_key.status != "OK"
