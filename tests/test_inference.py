"""inf-1's claim packet — the llama.cpp semantic inference-control
layer (`workbench/application/inference.py` + the composition wiring
+ the compiled spawn surface).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE SEMANTIC MODEL: a control's identity is SEMANTIC (never the
   raw flag); AUTO is a REAL state distinct from unset and from a
   value; the project baseline stays distinct from the upstream
   default; the scope is preserved per control; UNKNOWN and REMOVED
   capabilities are REPRESENTABLE (the vocabulary) while a REMOVED
   control never emits.
2. THE RESOLVER: profile composition is deterministic; the
   call-local request layer overrides the BASE; temperature 0 is the
   deterministic decoding state — the distribution samplers stay
   CONFIGURED and VISIBLE with their INEFFECTIVE reason (never
   deleted); a disabled-by-value control is INACTIVE (the runtime's
   own forms); a sampler out of the chain is INEFFECTIVE with its
   reason.
3. THE CHAIN: the order round-trips through the store; the emitted
   chain follows the PROFILE order (an actual order change changes
   the emitted configuration).
4. THE BACKEND TRANSLATION: the semantic profile compiles to the
   platform's typed surface — the AUTO/ALL forms, the ordered
   samplers, the seed, the fit, the KV pair — each flag form the
   reviewed runtime evidence's own literal; the legacy caller's
   command stays byte-stable.
5. THE TRUTH LAYERS: requested / effective remain distinguishable on
   the chat run document (the §19.1 chain — never a guessed
   provenance).
6. THE STORE LAWS + THE MIGRATION: the profile store follows
   settings.py's own laws; the one-way schema/1 → settings/2 +
   inference/1 migration preserves the operator's values verbatim,
   is idempotent, and never overwrites a present profile.
7. THE DUPLICATE-OWNERSHIP GUARD: the raw extra_args hatch may never
   shadow a semantic control — the compile step refuses the overlap
   loudly (the smallest typed mechanism, the law's §13).
8. THE OPERATIONS: inference.read answers the RESOLVED document +
   the injected compiled preview; inference.update walks the store's
   own validation (DOMAIN_REJECTED) and emits its effect.
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
from workbench.application.inference import (  # noqa: E402
    CHAT_TEMPLATE_FORMS,
    CONTROL_LIBRARY,
    FIT_FORMS,
    FLASH_ATTENTION_FORMS,
    KV_CACHE_TYPES,
    SAMPLER_CHAIN_IDS,
    SCHEMA,
    STATES,
    InferenceError,
    InferenceProfile,
    InferenceStore,
    SemanticControl,
    effective_temperature,
    launch_kwargs,
    migrate_launch_semantics,
    register_inference_operations,
    resolve,
)
from workbench.platform.llama_process import (  # noqa: E402
    KV_CACHE_TYPES as PLATFORM_KV_TYPES,
)
from workbench.platform.llama_process import (  # noqa: E402
    build_server_command,
)


def _store(tmp_path: Path) -> InferenceStore:
    return InferenceStore(tmp_path / "inference.json")


# ------------------------------------------------- the semantic model laws


def test_the_control_identity_is_semantic_never_the_raw_flag() -> None:
    """The law's §1/§14.1: the identity is the semantic id; the raw
    flag is metadata (the tooltip/compile mapping), never the primary
    key — and every id in the library is unique."""
    ids = [control.id for control in CONTROL_LIBRARY]
    assert len(ids) == len(set(ids)), "one identity per control"
    for control in CONTROL_LIBRARY:
        assert "." in control.id, f"namespaced id: {control.id}"
        assert control.id != control.flag, "identity is not the flag"
        assert control.name != control.flag, "the human name is not the flag"
        assert control.kind in ("value", "mode", "toggle", "chain")
        assert control.scope in ("spawn", "request", "spawn+request")
        assert control.status in (
            "ACTIVE", "UNCLASSIFIED", "LEGACY", "REMOVED"
        )


def test_auto_is_a_real_state_not_unset() -> None:
    """The law's §10: AUTO ('auto') is a first-class runtime form —
    resolving it yields the AUTO state (never 'unset', never a
    default guess); the explicit form yields EFFECTIVE; the two never
    collapse."""
    profile = InferenceProfile(gpu_layers="auto", flash_attention="auto")
    resolved = resolve(profile)
    states = {c["id"]: c for c in resolved["controls"]}
    assert states["device.gpu_layers"]["state"] == "AUTO"
    assert states["device.gpu_layers"]["value"] == "auto"
    assert states["device.flash_attention"]["state"] == "AUTO"
    explicit = resolve(InferenceProfile(gpu_layers=999, flash_attention="on"))
    states = {c["id"]: c for c in explicit["controls"]}
    assert states["device.gpu_layers"]["state"] == "EFFECTIVE"
    assert states["device.gpu_layers"]["value"] == 999
    # the seed's own AUTO form: -1 IS the runtime's random sentinel
    assert states["sampling.seed"]["state"] == "AUTO"
    assert states["sampling.seed"]["value"] == -1


def test_the_project_baseline_stays_distinct_from_upstream() -> None:
    """The law's §5: the upstream default (runtime evidence) is NOT
    the project baseline — the profile's baseline pins its own values
    and the resolver document carries BOTH (never a silent rewrite
    of the project pin to match upstream)."""
    index = {control.id: control for control in CONTROL_LIBRARY}
    assert index["sampling.penalties"].baseline == 1.1
    assert index["sampling.penalties"].upstream_default == 1.0
    assert index["device.flash_attention"].baseline == "on"
    assert index["device.flash_attention"].upstream_default == "auto"
    resolved = resolve(InferenceProfile())
    for control in resolved["controls"]:
        assert control["baseline"] is not None
        assert "upstream_default" in control


def test_the_scope_is_preserved_per_control() -> None:
    """The law's §7: every control carries its explicit scope — the
    spawn/request split never collapses (the temperature rides BOTH;
    the KV types are spawn-only; the request layer's seed deferral is
    named, never guessed)."""
    index = {control.id: control for control in CONTROL_LIBRARY}
    assert index["sampling.temperature"].scope == "spawn+request"
    assert index["memory.cache_type_k"].scope == "spawn"
    resolved = resolve(InferenceProfile())
    for control in resolved["controls"]:
        assert control["scope"] in ("spawn", "request", "spawn+request")
    assert "seed" in str(resolved["request_layer"]["note"])


def test_unknown_and_removed_capabilities_are_representable() -> None:
    """The law's §2/§9: the vocabulary holds UNCLASSIFIED (a NEW
    upstream control nobody classified yet) and REMOVED (a LEGACY
    form the current runtime dropped) — representable in the MODEL
    while a REMOVED control never reaches the emitted surface."""
    assert "UNCLASSIFIED" in STATES
    assert "REMOVED" in STATES
    assert "LEGACY" in STATES
    new_upstream = SemanticControl(
        id="sampling.some_new_sampler",
        name="Some New Sampler",
        category="sampling",
        kind="value",
        scope="spawn",
        flag="--some-new-sampler",
        value_doc="a float",
        baseline=0.5,
        upstream_default=0.5,
        status="UNCLASSIFIED",
    )
    assert new_upstream.status == "UNCLASSIFIED"
    removed = SemanticControl(
        id="sampling.draft_legacy",
        name="Draft (LEGACY)",
        category="sampling",
        kind="value",
        scope="spawn",
        flag="--draft",
        value_doc="a legacy form",
        baseline=0,
        upstream_default=0,
        notes=("the removed --draft* family — kept searchable, never emitted",),
        status="REMOVED",
    )
    assert removed.status == "REMOVED"
    # the emitted profile surface never carries a REMOVED/LEGACY id
    emitted = {control.id for control in CONTROL_LIBRARY}
    assert "sampling.draft_legacy" not in emitted


def test_the_cross_layer_vocabulary_is_pinned_equal() -> None:
    """The drift guard (the settings.py precedent: each layer
    validates its own boundary, the claim packet pins the two
    vocabularies EQUAL — an import edge would couple the layers)."""
    assert KV_CACHE_TYPES == PLATFORM_KV_TYPES
    assert set(FLASH_ATTENTION_FORMS) == {"auto", "on", "off"}
    assert set(FIT_FORMS) == {"on", "off"}
    assert set(CHAT_TEMPLATE_FORMS) == {"model_default", "generic"}
    assert set(SAMPLER_CHAIN_IDS) == {
        "penalties", "top_k", "top_p", "min_p", "temperature"
    }


# -------------------------------------------------------- the resolver laws


def test_the_profile_composition_is_deterministic() -> None:
    profile = InferenceProfile(temperature=0.4, top_k=77)
    first = resolve(profile)
    second = resolve(profile)
    assert first == second, "the resolver is a pure function of the profile"


def test_the_request_layer_overrides_the_base() -> None:
    """§19.1's call-local layer: an EXPLICIT request temperature wins
    over the BASE profile value; the document names the source."""
    profile = InferenceProfile(temperature=0.4)
    resolved = resolve(profile, request_temperature=1.5)
    states = {c["id"]: c for c in resolved["controls"]}
    assert states["sampling.temperature"]["value"] == 1.5
    assert states["sampling.temperature"]["source"] == "request"
    plain = resolve(profile)
    states = {c["id"]: c for c in plain["controls"]}
    assert states["sampling.temperature"]["value"] == 0.4
    assert states["sampling.temperature"]["source"] == "profile"


def test_temperature_zero_preserves_the_sampler_configuration() -> None:
    """The law's §11 (the chip specification's §3.4): temperature 0 is
    the DETERMINISTIC decoding state — the distribution samplers stay
    CONFIGURED and VISIBLE with the INEFFECTIVE reason and their
    values PRESERVED (never deleted; the user returns by restoring
    the temperature)."""
    profile = InferenceProfile(temperature=0.0, top_k=40, top_p=0.95)
    resolved = resolve(profile)
    states = {c["id"]: c for c in resolved["controls"]}
    assert resolved["deterministic"] is True
    assert states["sampling.temperature"]["value"] == 0.0
    assert states["sampling.temperature"]["state"] == "EFFECTIVE"
    for sampler in ("sampling.top_k", "sampling.top_p", "sampling.min_p"):
        control = states[sampler]
        assert control["state"] == "INEFFECTIVE"
        assert control["reasons"], "the reason is mandatory"
        assert "deterministic" in " ".join(control["reasons"])
        # the VALUE is preserved — never deleted
        assert control["value"] == InferenceProfile().as_document()[
            {"sampling.top_k": "top_k", "sampling.top_p": "top_p",
             "sampling.min_p": "min_p"}[sampler]
        ]
    # restoring the temperature returns the samplers to EFFECTIVE
    restored = resolve(InferenceProfile(temperature=0.4))
    states = {c["id"]: c for c in restored["controls"]}
    assert states["sampling.top_k"]["state"] == "EFFECTIVE"


def test_the_disabled_value_form_is_inactive_not_auto() -> None:
    """The runtime's own disabled forms (top_k 0 / top_p 1.0 /
    min_p 0.0 / penalties 1.0) — INACTIVE with the reason, distinct
    from AUTO and from a value."""
    profile = InferenceProfile(
        top_k=0, top_p=1.0, min_p=0.0, repeat_penalty=1.0
    )
    resolved = resolve(profile)
    states = {c["id"]: c for c in resolved["controls"]}
    assert states["sampling.top_k"]["state"] == "INACTIVE"
    assert states["sampling.top_p"]["state"] == "INACTIVE"
    assert states["sampling.min_p"]["state"] == "INACTIVE"
    assert states["sampling.penalties"]["state"] == "INACTIVE"
    for control in resolved["controls"]:
        if control["state"] == "INACTIVE":
            assert control["reasons"], "the reason is mandatory"


def test_a_sampler_out_of_the_chain_is_ineffective() -> None:
    """Membership and value are separate concerns (the law's §11): a
    sampler enabled=false stays CONFIGURED (its value flag remains)
    but is INEFFECTIVE with the reason — never a silent drop."""
    profile = InferenceProfile(
        sampler_chain=[
            {"id": "penalties", "enabled": True},
            {"id": "top_k", "enabled": False},
            {"id": "top_p", "enabled": True},
            {"id": "min_p", "enabled": True},
            {"id": "temperature", "enabled": True},
        ]
    )
    resolved = resolve(profile)
    states = {c["id"]: c for c in resolved["controls"]}
    assert states["sampling.top_k"]["state"] == "INEFFECTIVE"
    assert "chain" in " ".join(states["sampling.top_k"]["reasons"])
    # the value itself stays the profile's own (still emitted pinned)
    assert states["sampling.top_k"]["value"] == 40
    chain = {item["id"]: item for item in resolved["sampler_chain"]}
    assert chain["top_k"]["enabled"] is False
    assert chain["top_k"]["state"] == "INEFFECTIVE"


def test_the_chain_order_round_trips_through_the_store() -> None:
    """The sampler chain is an ORDERED first-class object: the order
    round-trips through the store's validation, and the EMITTED chain
    follows the PROFILE order — an actual order change changes the
    emitted configuration (never a cosmetic sort)."""
    reordered = [
        {"id": "temperature", "enabled": True},
        {"id": "min_p", "enabled": True},
        {"id": "top_p", "enabled": True},
        {"id": "penalties", "enabled": True},
        {"id": "top_k", "enabled": True},
    ]
    profile = InferenceProfile(sampler_chain=reordered)  # type: ignore[arg-type]
    assert [item.id for item in profile.sampler_chain] == [
        "temperature", "min_p", "top_p", "penalties", "top_k"
    ]
    kwargs = launch_kwargs(profile)
    assert kwargs["samplers"] == [
        "temperature", "min_p", "top_p", "penalties", "top_k"
    ]
    default_kwargs = launch_kwargs(InferenceProfile())
    assert default_kwargs["samplers"] == list(SAMPLER_CHAIN_IDS)
    # disabled members leave the emitted chain; enabled stay in order
    mixed = [
        {"id": "penalties", "enabled": True},
        {"id": "top_k", "enabled": False},
        {"id": "temperature", "enabled": True},
        {"id": "top_p", "enabled": True},
        {"id": "min_p", "enabled": True},
    ]
    kwargs = launch_kwargs(
        InferenceProfile(sampler_chain=mixed)  # type: ignore[arg-type]
    )
    assert kwargs["samplers"] == ["penalties", "temperature", "top_p", "min_p"]


# --------------------------------------------------- the backend translation


def test_the_semantic_profile_compiles_to_the_typed_surface() -> None:
    """The law's §13: the semantic values map onto the platform's
    typed surface — every emitted form the reviewed runtime
    evidence's own literal (the ';' separators, the -ngl forms, the
    KV enum, the seed sentinel)."""
    profile = InferenceProfile(
        gpu_layers="all",
        fit="off",
        cache_type_k="q8_0",
        cache_type_v="q4_0",
        seed=1234,
        chat_template="generic",
        temperature=0.25,
    )
    kwargs = launch_kwargs(profile)
    command = build_server_command(
        ["python", "stub.py"], "model.gguf", port=8765, **kwargs
    )
    text = " ".join(command)
    assert "-ngl all" in text
    assert "-fa on" in text
    assert "--fit off" in text
    assert "--samplers penalties;top_k;top_p;min_p;temperature" in text
    assert "--seed 1234" in text
    assert "--cache-type-k q8_0" in text
    assert "--cache-type-v q4_0" in text
    assert "--temp 0.25" in text
    assert "--jinja" not in text, "the GENERIC template omits --jinja"
    assert command.index("-ngl") < command.index("--temp"), "a stable order"
    # the AUTO gpu form passes through as the runtime's own literal
    auto = launch_kwargs(InferenceProfile(gpu_layers="auto"))
    assert auto["gpu_layers"] == "auto"
    command = build_server_command(
        ["python", "stub.py"], "model.gguf", port=8765, **auto
    )
    assert "-ngl auto" in " ".join(command)


def test_the_legacy_caller_command_stays_byte_stable() -> None:
    """The platform's typed surface is ADDITIVE: the legacy caller
    (no semantic kwargs) gets the exact pre-inf-1 command — no flag
    appears unless the semantic layer emitted it."""
    command = build_server_command(["python", "stub.py"], "m.gguf", port=8765)
    text = " ".join(command)
    assert text == (
        "python stub.py -m m.gguf --host 127.0.0.1 --port 8765 -ngl 999 "
        "-c 8192 -fa on --temp 0.8 --top-k 40 --top-p 0.95 --min-p 0.05 "
        "--repeat-penalty 1.1 --jinja --no-webui"
    )


def test_the_extra_args_hatch_never_shadows_a_semantic_control() -> None:
    """The law's §13: a semantic Top-K plus a raw `--top-k` (or any
    alias form) is a CONFLICT refused loudly — never an ambiguous
    precedence; a raw-only hatch stays legal."""
    sys.path.insert(0, str(REPO / "scripts"))
    from workbench_app import _duplicate_flag_ownership  # noqa: E402

    assert _duplicate_flag_ownership(["--verbose"]) == []
    assert _duplicate_flag_ownership(["--some-unknown-flag", "x"]) == []
    assert _duplicate_flag_ownership(["--top-k", "20"]) == ["--top-k"]
    assert _duplicate_flag_ownership(["-c", "1024"]) == ["-c"]
    assert sorted(_duplicate_flag_ownership(["-ngl", "0", "-s", "7"])) == [
        "-ngl", "-s"
    ]


def test_the_truth_layers_stay_distinguishable_on_chat() -> None:
    """The §19.1 chain made executable: the chat work document carries
    REQUESTED (what the caller explicitly asked, None where absent)
    and EFFECTIVE (what the composition resolved) as SEPARATE
    documents — never a guessed provenance."""
    from workbench.application.operations.backend import (  # noqa: E402
        chat_completion_work,
    )

    class _Port:
        def chat(self, messages, *, grammar=None, temperature=0.8,
                 max_tokens=512):
            return ("content", "stop")

    work = chat_completion_work(
        _Port(), [{"role": "user", "content": "hi"}], 0.7, 64,
        temperature_requested=0.7,
    )

    class _Ctx:
        def check(self) -> None:
            return None

    result = work(_Ctx())
    assert result["requested"]["temperature"] == 0.7
    assert result["effective"]["temperature"] == 0.7
    absent = chat_completion_work(
        _Port(), [{"role": "user", "content": "hi"}], 0.7, 64,
    )
    result = absent(_Ctx())
    assert result["requested"]["temperature"] is None, (
        "an absent ask is None — the honest REQUESTED layer"
    )
    assert result["effective"]["temperature"] == 0.7, (
        "the EFFECTIVE layer names what the composition resolved"
    )


# ------------------------------------------------------------ the store laws


def test_the_profile_store_laws(tmp_path: Path) -> None:
    path = tmp_path / "inference.json"
    store = InferenceStore(path)
    assert not path.exists(), "the file appears only on the first save"
    assert store.current() == InferenceProfile()
    updated = store.update(
        {"temperature": 0.3, "context": 4096, "gpu_layers": "auto"}
    )
    assert updated.temperature == 0.3
    assert updated.gpu_layers == "auto"
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["schema"] == SCHEMA
    assert document["profile"]["gpu_layers"] == "auto"
    assert InferenceStore(path).current() == updated, "the roundtrip"


def test_the_profile_store_rejects_loud(tmp_path: Path) -> None:
    store = _store(tmp_path)
    for bad in (
        {"context": 0},
        {"context": True},
        {"gpu_layers": -1},
        {"gpu_layers": 1000},
        {"gpu_layers": "maybe"},
        {"flash_attention": "sometimes"},
        {"fit": "maybe"},
        {"cache_type_k": "q3_0"},
        {"temperature": 2.5},
        {"top_k": -1},
        {"top_p": 1.5},
        {"min_p": -0.1},
        {"repeat_penalty": 5.0},
        {"seed": -2},
        {"chat_template": "custom"},
        {"name": ""},
        {"sampler_chain": []},
        {"sampler_chain": [{"id": "dry"}]},
        {"sampler_chain": [{"id": "top_k"}]},  # a partial chain refuses
        {"nope": 1},
    ):
        with pytest.raises(InferenceError):
            store.update(bad)
    assert store.current() == InferenceProfile(), "no partial application"
    # the load refusals: corrupt, foreign schema, unknown field
    path = tmp_path / "inference.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(InferenceError, match="unreadable"):
        InferenceStore(path)
    path.write_text(
        json.dumps({"schema": "canonsim.workbench.inference/0"}),
        encoding="utf-8",
    )
    with pytest.raises(InferenceError, match="schema"):
        InferenceStore(path)
    path.write_text(
        json.dumps({"schema": SCHEMA, "profile": {"nope": 1}}),
        encoding="utf-8",
    )
    with pytest.raises(InferenceError, match="unknown field"):
        InferenceStore(path)
    with pytest.raises(InferenceError, match="relative"):
        InferenceStore(Path("inference.json"))


# ------------------------------------------------------------- the migration


def _write_settings1(path: Path, values: dict) -> None:
    path.write_text(
        json.dumps(
            {
                "schema": "canonsim.workbench.settings/1",
                "settings": values,
            }
        ),
        encoding="utf-8",
    )


def test_the_migration_moves_the_semantics_verbatim(
    tmp_path: Path,
) -> None:
    settings_path = tmp_path / "settings.json"
    inference_path = tmp_path / "inference.json"
    _write_settings1(
        settings_path,
        {
            "llama_server_exe": "D:/llama.cpp/llama-server.exe",
            "context": 4096,
            "gpu_layers": 24,
            "flash_attention": "off",
            "jinja": False,
            "no_webui": True,
            "temperature": 0.6,
            "top_k": 50,
            "top_p": 0.9,
            "min_p": 0.03,
            "repeat_penalty": 1.15,
            "extra_args": "--verbose",
        },
    )
    assert migrate_launch_semantics(settings_path, inference_path) is True
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    assert settings["schema"] == "canonsim.workbench.settings/2"
    assert settings["settings"] == {
        "llama_server_exe": "D:/llama.cpp/llama-server.exe",
        "no_webui": True,
        "extra_args": "--verbose",
    }
    profile = json.loads(inference_path.read_text(encoding="utf-8"))
    body = profile["profile"]
    assert profile["schema"] == SCHEMA
    # the values moved VERBATIM — the operator's own, never a reset
    assert body["context"] == 4096
    assert body["gpu_layers"] == 24
    assert body["flash_attention"] == "off"
    assert body["temperature"] == 0.6
    assert body["top_k"] == 50
    assert body["top_p"] == 0.9
    assert body["min_p"] == 0.03
    assert body["repeat_penalty"] == 1.15
    assert body["chat_template"] == "generic", "jinja: false -> GENERIC"


def test_the_migration_is_idempotent_and_a_present_profile_wins(
    tmp_path: Path,
) -> None:
    settings_path = tmp_path / "settings.json"
    inference_path = tmp_path / "inference.json"
    _write_settings1(settings_path, {"temperature": 0.6})
    assert migrate_launch_semantics(settings_path, inference_path) is True
    # idempotent: a schema/2 document no-ops
    assert migrate_launch_semantics(settings_path, inference_path) is False
    # a present inference profile is NEVER overwritten (the newer
    # truth wins; a stale schema/1 copy that reappears — a restored
    # backup — has its semantic fields DROPPED, the file rewritten
    # schema/2, the profile untouched)
    _write_settings1(settings_path, {"temperature": 0.9})
    assert migrate_launch_semantics(settings_path, inference_path) is True
    profile = json.loads(inference_path.read_text(encoding="utf-8"))
    assert profile["profile"]["temperature"] == 0.6, (
        "the inference profile wins — never overwritten by the stale copy"
    )
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    assert settings["schema"] == "canonsim.workbench.settings/2"
    assert "temperature" not in settings["settings"]
    # a missing settings file is a no-op
    assert (
        migrate_launch_semantics(
            tmp_path / "absent.json", tmp_path / "absent2.json"
        )
        is False
    )


def test_the_migration_refuses_a_malformed_document_loud(
    tmp_path: Path,
) -> None:
    settings_path = tmp_path / "settings.json"
    settings_path.write_text("{not json", encoding="utf-8")
    with pytest.raises(InferenceError, match="never resets"):
        migrate_launch_semantics(
            settings_path, tmp_path / "inference.json"
        )


# ------------------------------------------------------------- the operations


def _gateway_with(
    store: InferenceStore,
    *,
    preview=None,
    managed_live=None,
):
    gateway = Gateway()
    register_inference_operations(
        gateway, store, compiled_preview=preview, managed_live=managed_live
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


def test_inference_read_answers_the_resolved_document(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path)

    def preview(current):
        assert "temperature" in current
        return "llama-server -m <model.gguf> --temp %.2f" % current[
            "temperature"
        ]

    gateway = _gateway_with(store, preview=preview, managed_live=lambda: False)
    reply = gateway.dispatch(
        RequestEnvelope(operation="inference.read", arguments={})
    )
    assert reply.status == "OK", reply.to_mapping()
    result = reply.result
    controls = {c["id"]: c for c in result["controls"]}
    assert controls["sampling.temperature"]["state"] == "EFFECTIVE"
    assert controls["sampling.seed"]["state"] == "AUTO"
    assert result["applies"] == "next-spawn"
    assert result["managed_live"] is False
    assert result["compiled_preview"] == "llama-server -m <model.gguf> --temp 0.80"
    assert [item["id"] for item in result["sampler_chain"]] == list(
        SAMPLER_CHAIN_IDS
    )
    assert result["profile"] == InferenceProfile().as_document()
    # the READ takes no arguments — the closed surface
    bad = gateway.dispatch(
        RequestEnvelope(
            operation="inference.read", arguments={"temperature": 1}
        )
    )
    assert bad.status != "OK"


def test_inference_update_walks_the_store(tmp_path: Path) -> None:
    store = _store(tmp_path)
    gateway = _gateway_with(
        store, preview=lambda c: "cmd", managed_live=lambda: True
    )
    session = _session(gateway, "inf1-ops")
    reply = gateway.dispatch(
        RequestEnvelope(
            operation="inference.update",
            arguments={
                "temperature": 0.1,
                "gpu_layers": "all",
                "sampler_chain": [
                    {"id": "temperature", "enabled": True},
                    {"id": "top_k", "enabled": False},
                    {"id": "penalties", "enabled": True},
                    {"id": "top_p", "enabled": True},
                    {"id": "min_p", "enabled": True},
                ],
            },
            session_id=session,
            client_request_id="inf1-update",
        )
    )
    assert reply.status == "OK", reply.to_mapping()
    result = reply.result
    controls = {c["id"]: c for c in result["controls"]}
    assert controls["sampling.temperature"]["value"] == 0.1
    assert controls["device.gpu_layers"]["state"] != "AUTO"
    assert controls["sampling.top_k"]["state"] == "INEFFECTIVE"
    assert "LIVE" in result["note"]
    # persisted: a fresh store re-reads the same profile
    fresh = InferenceStore(store.path)
    assert fresh.current().temperature == 0.1
    assert [item.id for item in fresh.current().sampler_chain] == [
        "temperature", "top_k", "penalties", "top_p", "min_p"
    ]
    # the ordered event stream carries the INFERENCE_UPDATED effect
    events = gateway.dispatch(
        RequestEnvelope(
            operation="session.events",
            arguments={},
            session_id=session,
        )
    )
    effects = [
        e for e in events.result["events"] if "INFERENCE" in str(e)
    ]
    assert effects, "the update emitted its dispatch-time effect"


def test_inference_update_rejects_loud(tmp_path: Path) -> None:
    store = _store(tmp_path)
    gateway = _gateway_with(store)
    session = _session(gateway, "inf1-reject")
    reply = gateway.dispatch(
        RequestEnvelope(
            operation="inference.update",
            arguments={"temperature": 9.9},
            session_id=session,
            client_request_id="inf1-reject-1",
        )
    )
    assert reply.status != "OK"
    assert reply.rejection == "DOMAIN_REJECTED"
    assert store.current() == InferenceProfile()


def test_the_chat_base_temperature_resolves_from_the_profile(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path)
    assert effective_temperature(store) == 0.8
    store.update({"temperature": 0.33})
    assert effective_temperature(store) == 0.33
    # deterministic-mode profile: the effective temperature is 0.0
    store.update({"temperature": 0.0})
    assert effective_temperature(store) == 0.0
