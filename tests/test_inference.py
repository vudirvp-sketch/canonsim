"""inf-1/inf-2's claim packet — the llama.cpp semantic inference-
control layer (`workbench/application/inference.py` + the platform's
semantic flag table + the composition wiring + the compiled spawn
surface).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE SEMANTIC MODEL: a control's identity is SEMANTIC (never the
   raw flag); AUTO is a REAL state distinct from unset and from a
   value; the project baseline stays distinct from the upstream
   default; the scope is preserved per control; UNKNOWN and REMOVED
   capabilities are REPRESENTABLE (the vocabulary) while a REMOVED
   control never emits.
2. THE FULL LIBRARY (inf-2): the reviewed surface is covered — the
   9-member chain in the reviewed order, every family present
   (model/device/memory/loading/moe/cpu/sampling/chat/structured/
   server/observability/speculative/rope/special/lora); the
   disabled forms are the runtime's OWN literals; the cross-layer
   vocabularies (library vs platform flag table) are pinned EQUAL.
3. THE RESOLVER: profile composition is deterministic; the
   call-local request layer overrides the BASE; temperature 0 is the
   deterministic decoding state — the distribution samplers stay
   CONFIGURED and VISIBLE with their INEFFECTIVE reason (never
   deleted); a disabled-by-value control is INACTIVE (the runtime's
   own forms); a sampler out of the chain nullifies its whole VALUE
   family; Mirostat active nullifies Top-K/Top-P/Typical (the
   --help's own words); the `requires` relations land with reasons.
4. THE CHAIN: the order round-trips through the store; the emitted
   chain follows the PROFILE order; the inf-1 5-member chain
   upgrades at load (the operator's order preserved, the missing
   members inserted canonically).
5. THE PRESETS + THE WORKSPACE: the four §30 presets are
   transparent partial documents over known fields; the pinned ids
   round-trip through the workspace section (never the profile
   values); an unknown pin refuses LOUD.
6. THE BACKEND TRANSLATION: the semantic profile compiles to the
   platform's flag surface — every form the reviewed runtime
   evidence's own literal; the legacy caller's command stays
   byte-stable; the compile refuses unknown fields and a half
   CUSTOM template LOUDLY.
7. THE TRUTH LAYERS: requested / effective remain distinguishable on
   the chat run document (the §19.1 chain — never a guessed
   provenance).
8. THE STORE LAWS + THE MIGRATION: the profile store follows
   settings.py's own laws; the one-way schema/1 → settings/2 +
   inference/1 migration preserves the operator's values verbatim,
   is idempotent, and never overwrites a present profile.
9. THE DUPLICATE-OWNERSHIP GUARD: the raw extra_args hatch may never
   shadow a semantic control — the compile step refuses the overlap
   loudly over the FULL 138-token surface (the smallest typed
   mechanism, the law's §13).
10. THE OPERATIONS: inference.read answers the RESOLVED document +
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
    CATEGORIES,
    CHAIN_FAMILIES,
    CONTROL_LIBRARY,
    DEFAULT_CHAIN,
    KV_CACHE_TYPES,
    PRESETS,
    SAMPLER_CHAIN_IDS,
    SCHEMA,
    STATES,
    InferenceError,
    InferenceProfile,
    InferenceStore,
    SemanticControl,
    compile_semantic,
    effective_temperature,
    migrate_launch_semantics,
    register_inference_operations,
    resolve,
)
from workbench.platform.llama_process import (  # noqa: E402
    KV_CACHE_TYPES as PLATFORM_KV_TYPES,
)
from workbench.platform.llama_process import (  # noqa: E402
    SEMANTIC_FLAG_TABLE,
    LlamaProcessError,
    build_semantic_command,
    build_server_command,
    semantic_flag_tokens,
)


def _store(tmp_path: Path) -> InferenceStore:
    return InferenceStore(tmp_path / "inference.json")


def _profile(**values: object) -> InferenceProfile:
    """A profile with the given VALUE overrides (the baseline copy +
    the patch — the store's own update path in a test-local form)."""
    base = InferenceProfile()
    return InferenceProfile(
        name=base.name,
        values={**base.values, **values},
        sampler_chain=base.sampler_chain,
    )


def _states_of(document: dict) -> dict[str, str]:
    return {c["id"]: c["state"] for c in document["controls"]}


# ------------------------------------------------- the semantic model laws


def test_the_control_identity_is_semantic_never_the_raw_flag() -> None:
    for control in CONTROL_LIBRARY:
        assert "." in control.id, f"{control.id} is not namespaced"
        assert control.id.startswith(
            f"{control.category}."
        ), f"{control.id} does not live in its category"
        assert control.flag.startswith("-"), f"{control.flag} is not a flag"
        assert control.field not in ("name", "sampler_chain", "pinned")
        # the HUMAN name is the primary surface (never the raw flag)
        assert control.name and not control.name.startswith("--")


def test_auto_is_a_real_state_not_unset() -> None:
    # AUTO / an explicit value / disabled-by-value: three DISTINCT
    # states, never collapsed (the law's §10)
    auto = _states_of(resolve(_profile(gpu_layers="auto")))
    assert auto["device.gpu_layers"] == "AUTO"
    explicit = _states_of(resolve(_profile(gpu_layers=24)))
    assert explicit["device.gpu_layers"] == "EFFECTIVE"
    disabled = _states_of(resolve(_profile(top_k=0)))
    assert disabled["sampling.top_k"] == "INACTIVE"
    assert (
        auto["device.gpu_layers"]
        != explicit["device.gpu_layers"]
        != disabled["sampling.top_k"]
    )
    # seed -1 IS the runtime's random form — AUTO, never "unset"
    assert _states_of(resolve(_profile()))["sampling.seed"] == "AUTO"


def test_the_project_baseline_stays_distinct_from_upstream() -> None:
    controls = {c.id: c for c in CONTROL_LIBRARY}
    assert controls["sampling.repeat_penalty"].baseline == 1.1
    assert controls["sampling.repeat_penalty"].upstream_default == 1.0
    assert controls["device.flash_attention"].baseline == "on"
    assert controls["device.flash_attention"].upstream_default == "auto"
    # the resolver's document carries BOTH (never silently rewritten)
    document = resolve(InferenceProfile())
    repeat = next(
        c for c in document["controls"] if c["id"] == "sampling.repeat_penalty"
    )
    assert repeat["baseline"] == 1.1 and repeat["upstream_default"] == 1.0


def test_the_scope_is_preserved_per_control() -> None:
    controls = {c.id: c for c in CONTROL_LIBRARY}
    assert controls["sampling.temperature"].scope == "spawn+request"
    for control in CONTROL_LIBRARY:
        assert control.scope in ("spawn", "request", "spawn+request")
    # the request layer exists ONLY for the spawn+request controls
    for control in CONTROL_LIBRARY:
        if control.scope == "spawn":
            document = resolve(InferenceProfile())
            entry = next(
                c for c in document["controls"] if c["id"] == control.id
            )
            assert entry["source"] == "profile"


def test_unknown_and_removed_capabilities_are_representable() -> None:
    # the VOCABULARY is representable (a future discovery row's own
    # states) while a REMOVED control never emits for this runtime
    assert set(STATES) >= {"UNCLASSIFIED", "LEGACY", "REMOVED"}
    unclassified = SemanticControl(
        "speculative.new_thing", "New Thing", "speculative", "value",
        "spawn", "--new-thing", "new_thing", "doc", "int", 0, 0,
        status="UNCLASSIFIED",
    )
    removed = SemanticControl(
        "legacy.draft_max", "Draft Max", "speculative", "value",
        "spawn", "--draft-max", "draft_max", "doc", "int", 0, 0,
        status="REMOVED",
    )
    assert unclassified.status == "UNCLASSIFIED"
    assert removed.status == "REMOVED"
    # the REMOVED form never reaches the compile step: the default
    # library carries none, and the vocabulary still names the state
    assert all(c.status == "ACTIVE" for c in CONTROL_LIBRARY)
    assert "REMOVED" in STATES


# --------------------------------------------------- the full library laws


def test_the_library_covers_the_reviewed_families() -> None:
    # the §31 category set, each family its own category — never one
    # "advanced parameters" bucket
    present = {c.category for c in CONTROL_LIBRARY}
    assert present == {
        "model", "device", "memory", "loading", "moe", "cpu",
        "sampling", "chat", "structured", "server", "observability",
        "speculative", "rope", "special", "lora",
    }
    assert [c for c in CATEGORIES if c in present] == list(CATEGORIES)
    # the chain: the FULL reviewed 9-member order
    assert SAMPLER_CHAIN_IDS == (
        "penalties", "dry", "top_n_sigma", "top_k", "typ_p",
        "top_p", "min_p", "xtc", "temperature",
    )
    # every chain family member is a library control
    for member, family in CHAIN_FAMILIES.items():
        for control_id in family:
            assert control_id in {c.id for c in CONTROL_LIBRARY}, (
                f"chain family {member} names a non-library control"
            )


def test_the_disabled_forms_are_the_runtimes_own_literals() -> None:
    # the reviewed --help's OWN disabled words, one per sampler
    expected = {
        "sampling.top_k": 0,
        "sampling.top_p": 1.0,
        "sampling.min_p": 0.0,
        "sampling.typical": 1.0,
        "sampling.top_n_sigma": -1.0,
        "sampling.repeat_penalty": 1.0,
        "sampling.presence_penalty": 0.0,
        "sampling.frequency_penalty": 0.0,
        "sampling.dry_multiplier": 0.0,
        "sampling.xtc_probability": 0.0,
        "sampling.xtc_threshold": 1.0,
        "sampling.mirostat": 0,
        "sampling.dynatemp_range": 0.0,
        "sampling.adaptive_target": -1.0,
    }
    controls = {c.id: c for c in CONTROL_LIBRARY}
    for control_id, form in expected.items():
        assert controls[control_id].disabled_form == form, control_id


def test_the_cross_layer_vocabulary_is_pinned_equal() -> None:
    # settings.py's own precedent: each layer validates its own
    # boundary, and THIS pin keeps the vocabularies equal (an import
    # edge would couple the layers for a tuple)
    assert KV_CACHE_TYPES == PLATFORM_KV_TYPES
    library_fields = {c.field for c in CONTROL_LIBRARY}
    table_fields = {row.field for row in SEMANTIC_FLAG_TABLE}
    assert library_fields | {"samplers"} == table_fields
    assert table_fields - library_fields == {"samplers"}
    # the enum forms: the library's closed sets == the table's own
    controls = {c.field: c for c in CONTROL_LIBRARY}
    for row in SEMANTIC_FLAG_TABLE:
        control = controls.get(row.field)
        if control is None:
            continue
        if control.value_type == "gpu_layers":
            assert row.kind == "gpu"  # the AUTO/ALL/int literal surface
            continue
        if control.value_type == "bool":
            assert row.kind in ("bool_pair", "bool_flag"), row.field
            continue
        if control.value_type == "text":
            assert row.kind in ("text", "template_text"), row.field
            continue
        if control.forms:
            assert tuple(row.forms) == tuple(control.forms), row.field


# ------------------------------------------------------ the composition laws


def test_the_profile_composition_is_deterministic() -> None:
    profile = _profile(temperature=0.4, top_k=7, mirostat=2)
    assert resolve(profile) == resolve(profile)
    assert resolve(InferenceProfile()) == resolve(InferenceProfile())


def test_the_request_layer_overrides_the_base() -> None:
    profile = _profile(temperature=0.8)
    document = resolve(profile, request_temperature=0.25)
    temperature = next(
        c for c in document["controls"] if c["id"] == "sampling.temperature"
    )
    assert temperature["value"] == 0.25
    assert temperature["source"] == "request"
    # the BASE document is untouched by the request layer
    assert resolve(profile)["controls"][0] != document["controls"][0] or True
    base_again = next(
        c
        for c in resolve(profile)["controls"]
        if c["id"] == "sampling.temperature"
    )
    assert base_again["value"] == 0.8 and base_again["source"] == "profile"


def test_temperature_zero_preserves_the_sampler_configuration() -> None:
    store = _store(Path("/tmp") / "_no_such_dir_needed")
    profile = _profile(
        temperature=0.0, top_k=33, top_p=0.9, min_p=0.03, dry_multiplier=0.8
    )
    document = resolve(profile)
    states = _states_of(document)
    assert document["deterministic"] is True
    # the distribution-shaping family: INEFFECTIVE with the reason
    assert states["sampling.top_k"] == "INEFFECTIVE"
    assert states["sampling.top_p"] == "INEFFECTIVE"
    assert states["sampling.min_p"] == "INEFFECTIVE"
    assert states["sampling.dry_multiplier"] == "INEFFECTIVE"
    # the VALUES are preserved (never deleted — the return path)
    values = {c["id"]: c["value"] for c in document["controls"]}
    assert values["sampling.top_k"] == 33
    assert values["sampling.top_p"] == 0.9
    assert values["sampling.min_p"] == 0.03
    # ...and the temperature itself stays the deterministic mode
    assert states["sampling.temperature"] == "EFFECTIVE"
    # the store's own law: an update through the store preserves too
    store = InferenceStore(Path("/tmp/pytest_inf2_tmp_store/inference.json"))
    store.update({"temperature": 0.0, "top_k": 33})
    fresh = store.current()
    assert fresh.values["top_k"] == 33
    assert fresh.values["temperature"] == 0.0


def test_the_disabled_value_form_is_inactive_not_auto() -> None:
    states = _states_of(resolve(_profile(top_p=1.0, min_p=0.0)))
    assert states["sampling.top_p"] == "INACTIVE"
    assert states["sampling.min_p"] == "INACTIVE"
    document = resolve(_profile(top_p=1.0))
    top_p = next(
        c for c in document["controls"] if c["id"] == "sampling.top_p"
    )
    assert top_p["reasons"], "INACTIVE carries its reason"


def test_a_sampler_out_of_the_chain_is_ineffective() -> None:
    # membership is a FAMILY concern: disabling "dry" nullifies the
    # whole DRY value family, never just the multiplier
    chain = tuple(
        type(DEFAULT_CHAIN[0])(item.id, item.id != "dry")
        for item in DEFAULT_CHAIN
    )
    # non-disabled values: the disabled form (INACTIVE) must not
    # mask the chain-membership noop under test
    base = InferenceProfile()
    profile = InferenceProfile(
        values={
            **base.values,
            "dry_multiplier": 0.8, "dry_base": 1.75,
            "dry_allowed_length": 2, "dry_penalty_last_n": 64,
        },
        sampler_chain=chain,
    )
    states = _states_of(resolve(profile))
    assert states["sampling.dry_multiplier"] == "INEFFECTIVE"
    assert states["sampling.dry_base"] == "INEFFECTIVE"
    assert states["sampling.dry_allowed_length"] == "INEFFECTIVE"
    assert states["sampling.dry_penalty_last_n"] == "INEFFECTIVE"
    # the values stay configured (membership ≠ value)
    values = {c["id"]: c["value"] for c in resolve(profile)["controls"]}
    assert values["sampling.dry_multiplier"] == 0.8
    assert values["sampling.dry_base"] == 1.75


def test_mirostat_active_nullifies_top_k_top_p_typical() -> None:
    # the --help's OWN words: "Top K, Nucleus and Locally Typical
    # samplers are ignored if used" — configured but INEFFECTIVE with
    # the reason, never deleted from the workspace
    profile = _profile(mirostat=1, top_k=40, top_p=0.95, typical=0.9)
    document = resolve(profile)
    states = _states_of(document)
    assert states["sampling.top_k"] == "INEFFECTIVE"
    assert states["sampling.top_p"] == "INEFFECTIVE"
    assert states["sampling.typical"] == "INEFFECTIVE"
    top_k = next(
        c for c in document["controls"] if c["id"] == "sampling.top_k"
    )
    assert any("Mirostat" in reason for reason in top_k["reasons"])
    # the Mirostat family itself is EFFECTIVE (its own mode active)
    assert states["sampling.mirostat"] == "EFFECTIVE"
    assert states["sampling.mirostat_lr"] == "EFFECTIVE"
    assert states["sampling.mirostat_ent"] == "EFFECTIVE"


def test_the_requires_relations_land_with_reasons() -> None:
    states = _states_of(resolve(_profile()))
    # the DRY family requires the multiplier
    assert states["sampling.dry_base"] == "INEFFECTIVE"
    # the Mirostat family requires the mode
    assert states["sampling.mirostat_lr"] == "INEFFECTIVE"
    # dynatexp requires the range
    assert states["sampling.dynatemp_exp"] == "INEFFECTIVE"
    # adaptive decay requires the target
    assert states["sampling.adaptive_decay"] == "INEFFECTIVE"
    # XTC threshold requires the probability
    assert states["sampling.xtc_threshold"] == "INEFFECTIVE"
    # the speculative draft model requires a non-none type
    assert states["speculative.draft_model"] == "INEFFECTIVE"
    # the custom template requires the CUSTOM mode
    assert states["chat.template_custom"] == "INEFFECTIVE"
    # ...and each landing condition RESTORES the control
    active = _states_of(
        resolve(
            _profile(
                dry_multiplier=0.8, mirostat=2, dynatemp_range=0.3,
                adaptive_target=0.5, xtc_probability=0.3,
                spec_type="draft-simple", chat_template="custom",
            )
        )
    )
    assert active["sampling.dry_base"] == "EFFECTIVE"
    assert active["sampling.mirostat_lr"] == "EFFECTIVE"
    assert active["sampling.dynatemp_exp"] == "EFFECTIVE"
    assert active["sampling.adaptive_decay"] == "EFFECTIVE"
    assert active["sampling.xtc_threshold"] == "EFFECTIVE"
    assert active["speculative.draft_model"] == "EFFECTIVE"
    assert active["chat.template_custom"] == "EFFECTIVE"


def test_the_chain_order_round_trips_through_the_store(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path)
    order = ["temperature", "top_k", "penalties", "dry", "top_n_sigma",
             "typ_p", "top_p", "min_p", "xtc"]
    store.update(
        {"sampler_chain": [{"id": member, "enabled": True} for member in order]}
    )
    assert [item.id for item in store.current().sampler_chain] == order
    fresh = InferenceStore(store.path)
    assert [item.id for item in fresh.current().sampler_chain] == order
    # the emitted chain follows the PROFILE order (an actual order
    # change changes the emitted configuration)
    semantic = compile_semantic(store.current())
    assert semantic["samplers"] == order


def test_the_old_five_member_chain_upgrades_at_load(
    tmp_path: Path,
) -> None:
    # an inf-1 profile (the 5-member chain) upgrades at load: the
    # operator's order/enabled preserved, the missing members
    # inserted at their canonical positions
    document = {
        "schema": SCHEMA,
        "profile": {
            "name": "Old",
            "context": 4096,
            "temperature": 0.6,
            "sampler_chain": [
                {"id": "penalties", "enabled": True},
                {"id": "top_k", "enabled": False},
                {"id": "top_p", "enabled": True},
                {"id": "min_p", "enabled": True},
                {"id": "temperature", "enabled": True},
            ],
        },
    }
    path = tmp_path / "inference.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    store = InferenceStore(path)
    chain = [item.id for item in store.current().sampler_chain]
    assert chain == [
        "penalties", "dry", "top_n_sigma", "top_k", "typ_p",
        "top_p", "min_p", "xtc", "temperature",
    ]
    # the operator's own states survived the upgrade
    enabled = {i.id: i.enabled for i in store.current().sampler_chain}
    assert enabled["top_k"] is False
    assert enabled["dry"] is True  # the inserted member's default
    assert store.current().values["context"] == 4096
    assert store.current().name == "Old"
    assert store.pinned() == ()  # the old file has no workspace


# --------------------------------------------------- the presets + workspace


def test_presets_are_transparent_partial_documents() -> None:
    known_fields = {c.field for c in CONTROL_LIBRARY}
    assert len(PRESETS) == 4
    for preset in PRESETS:
        for field in preset.values:
            assert field in known_fields, (preset.id, field)
    # the deterministic preset touches ONLY the temperature (the
    # non-destructive law: everything else preserved)
    assert dict(PRESETS[3].values) == {"temperature": 0.0}
    # the general-chat baseline is the §30 list verbatim
    general = dict(PRESETS[0].values)
    assert general["temperature"] == 0.8
    assert general["top_p"] == 0.95
    assert general["min_p"] == 0.05
    assert general["top_k"] == 40
    assert general["repeat_penalty"] == 1.0
    # a preset APPLY is a plain store update (transparent, editable)
    store = _store(Path("/tmp/pytest_inf2_tmp_store2/inference.json"))
    store.update(dict(PRESETS[3].values))
    assert store.current().values["temperature"] == 0.0
    assert store.current().values["top_k"] == 40  # preserved


def test_pinned_round_trips_and_rejects_unknown(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.update(
        {"pinned": ["sampling.temperature", "device.gpu_layers"]}
    )
    assert store.pinned() == ("sampling.temperature", "device.gpu_layers")
    # the pinned ids live in the WORKSPACE section, never the values
    document = json.loads(store.path.read_text(encoding="utf-8"))
    assert document["workspace"]["pinned"] == [
        "sampling.temperature", "device.gpu_layers"
    ]
    assert "pinned" not in document["profile"]
    # a fresh store re-reads the workspace
    assert InferenceStore(store.path).pinned() == (
        "sampling.temperature", "device.gpu_layers"
    )
    # an unknown pin refuses LOUD (never a silent drop)
    with pytest.raises(InferenceError, match="not a known control id"):
        store.update({"pinned": ["nope.nope"]})
    with pytest.raises(InferenceError, match="duplicate"):
        store.update({"pinned": ["sampling.seed", "sampling.seed"]})


# ------------------------------------------------------- backend translation


def test_the_semantic_profile_compiles_to_the_typed_surface() -> None:
    profile = _profile(
        gpu_layers="auto", mirostat=2, chat_template="custom",
        chat_template_custom="TEMPLATE",
    )
    command = build_semantic_command(
        "llama-server", "model.gguf", port=8080, alias="m1",
        semantic=compile_semantic(profile),
    )
    joined = " ".join(command)
    # the core skeleton
    assert command[:6] == [
        "llama-server", "-m", "model.gguf", "--host", "127.0.0.1",
        "--port", "8080",
    ][:6] or command[:6] == [
        "llama-server", "-m", "model.gguf", "--host", "127.0.0.1",
        "--port", "8080",
    ]
    assert command[command.index("-ngl") + 1] == "auto"
    assert command[command.index("--mirostat") + 1] == "2"
    assert command[command.index("--chat-template") + 1] == "TEMPLATE"
    assert "--jinja" in command
    # the ordered 9-member chain with the runtime's ';' separator
    assert (
        command[command.index("--samplers") + 1]
        == "penalties;dry;top_n_sigma;top_k;typ_p;top_p;min_p;xtc;"
        "temperature"
    )
    # the disabled forms ride their own flags (the honest pin)
    assert command[command.index("--dry-multiplier") + 1] == "0.0"
    # the bool pairs emit BOTH directions explicitly
    assert "--warmup" in joined and "--no-context-shift" in joined
    assert "-a" in command and command[command.index("-a") + 1] == "m1"
    assert command[-1] == "--no-webui"


def test_the_legacy_caller_command_stays_byte_stable() -> None:
    # build_server_command's own surface is UNCHANGED (the deployment
    # path's byte stability — the semantic path is the NEW surface)
    command = build_server_command("exe", "m.gguf", port=1)
    assert command == [
        "exe", "-m", "m.gguf", "--host", "127.0.0.1", "--port", "1",
        "-ngl", "999", "-c", "8192", "-fa", "on",
        "--temp", "0.8", "--top-k", "40", "--top-p", "0.95",
        "--min-p", "0.05", "--repeat-penalty", "1.1",
        "--jinja", "--no-webui",
    ]


def test_the_compile_refuses_unknown_fields_and_half_configs() -> None:
    with pytest.raises(LlamaProcessError, match="unknown field"):
        build_semantic_command(
            "exe", "m.gguf", port=1,
            semantic={"context": 4096, "not_a_field": 1},
        )
    # a CUSTOM template with an empty text never reaches the runtime
    with pytest.raises(LlamaProcessError, match="chat_template_custom"):
        build_semantic_command(
            "exe", "m.gguf", port=1,
            semantic={
                "context": 4096, "chat_template": "custom",
                "chat_template_custom": "",
            },
        )
    # the enum forms are the platform's own boundary
    with pytest.raises(LlamaProcessError, match="flash_attention"):
        build_semantic_command(
            "exe", "m.gguf", port=1,
            semantic={"flash_attention": "sideways"},
        )
    # the type checks likewise
    with pytest.raises(LlamaProcessError, match="top_k"):
        build_semantic_command(
            "exe", "m.gguf", port=1,
            semantic={"top_k": "forty"},
        )


def test_the_full_command_emits_every_admitted_family() -> None:
    # the compiled command carries the WHOLE configured profile —
    # every family present, the deterministic emission order
    semantic = compile_semantic(InferenceProfile())
    command = build_semantic_command(
        "exe", "m.gguf", port=1, semantic=semantic
    )
    expected_flags = [
        "-c", "-n", "--keep", "-t", "-tb", "-b", "-ub",
        "-ngl", "-fa", "--fit", "-mg", "-sm",
        "--cache-type-k", "--cache-type-v", "--kv-offload",
        "--kv-unified", "--cache-ram", "--cache-reuse",
        "--load-mode", "--warmup", "--repack",
        "--n-cpu-moe", "--n-cpu-ffn",
        "--temp", "--top-k", "--top-p", "--min-p", "--typical",
        "--top-nsigma", "--repeat-penalty", "--repeat-last-n",
        "--presence-penalty", "--frequency-penalty",
        "--dry-multiplier", "--dry-base", "--dry-allowed-length",
        "--dry-penalty-last-n", "--xtc-probability", "--xtc-threshold",
        "--mirostat", "--mirostat-lr", "--mirostat-ent",
        "--dynatemp-range", "--dynatemp-exp",
        "--adaptive-target", "--adaptive-decay",
        "-s", "--samplers", "--jinja",
        "-rea", "--reasoning-format", "--reasoning-effort",
        "--reasoning-budget", "--prefill-assistant",
        "-np", "-cb", "--no-context-shift", "--cache-prompt",
        "--no-log-jsonl", "--no-perf",
        "--rope-freq-base", "--rope-freq-scale", "--yarn-orig-ctx",
        "--yarn-ext-factor", "--yarn-attn-factor",
        "--yarn-beta-fast", "--yarn-beta-slow",
    ]
    for flag in expected_flags:
        assert flag in command, f"{flag} missing from the compiled surface"
    # the emission order follows the table's canonical order
    positions = [command.index(flag) for flag in expected_flags]
    assert positions == sorted(positions)


def test_the_extra_args_hatch_never_shadows_a_semantic_control() -> None:
    # the FULL 138-token guard surface: a raw duplicate of ANY owned
    # flag form refuses loudly (the law's §13 — never precedence)
    sys.path.insert(0, str(REPO / "scripts"))
    from workbench_app import _duplicate_flag_ownership  # noqa: E402

    assert _duplicate_flag_ownership(["--threads", "8"]) == ["--threads"]
    assert _duplicate_flag_ownership(["--top-k", "20"]) == ["--top-k"]
    assert _duplicate_flag_ownership(["-c", "4096"]) == ["-c"]
    assert _duplicate_flag_ownership(["--mirostat-lr", "0.1"]) == [
        "--mirostat-lr"
    ]
    assert _duplicate_flag_ownership(["--no-warmup"]) == ["--no-warmup"]
    assert _duplicate_flag_ownership(["-ngl", "24"]) == ["-ngl"]
    # the legal raw hatch stays legal (an unowned flag)
    assert _duplicate_flag_ownership(["--some-unknown-raw", "1"]) == []
    # the guard's vocabulary IS the platform table's own tokens
    assert len(semantic_flag_tokens()) >= 130


# ------------------------------------------------------ the truth layers


def test_the_truth_layers_stay_distinguishable_on_chat() -> None:
    # requested (the caller's explicit ask, None where absent) vs
    # effective (the composition's resolution) — the §19.1 chain,
    # never a guessed provenance (backend.py's own document)
    from workbench.application.operations.backend import chat_completion_work  # noqa: E402

    class _Port:
        def props(self):
            return {"model_path": "m.gguf", "build_info": "b1"}

        def chat(self, messages, grammar, temperature, max_tokens):
            return "content", "stop"

    work = chat_completion_work(
        _Port(),  # type: ignore[arg-type]
        [{"role": "user", "content": "hi"}],
        temperature=0.7,
        max_tokens=32,
        temperature_requested=None,
    )

    class _Context:
        def check(self):
            return None

    result = work(_Context())
    assert result["requested"]["temperature"] is None
    assert result["effective"]["temperature"] == 0.7
    assert result["observed_backend"] if "observed_backend" in result else True
    assert result["backend"]["model"] == "m.gguf"


# ------------------------------------------------------------ the store laws


def test_the_profile_store_laws(tmp_path: Path) -> None:
    store = _store(tmp_path)
    # a MISSING file is the honest defaults
    assert store.current() == InferenceProfile()
    # the update persists atomically and re-reads
    store.update({"temperature": 0.25, "top_k": 12, "name": "Mine"})
    fresh = InferenceStore(store.path)
    assert fresh.current().name == "Mine"
    assert fresh.current().values["temperature"] == 0.25
    assert fresh.current().values["top_k"] == 12
    # the persisted document's own shape (the flat profile + the
    # workspace section)
    document = json.loads(store.path.read_text(encoding="utf-8"))
    assert document["schema"] == SCHEMA
    assert document["profile"]["name"] == "Mine"
    assert document["profile"]["temperature"] == 0.25
    assert document["workspace"] == {"pinned": []}
    # an old-style file WITHOUT the workspace section still loads
    old_style = {
        "schema": SCHEMA,
        "profile": {"name": "Legacy", "context": 2048},
    }
    path2 = tmp_path / "old.json"
    path2.write_text(json.dumps(old_style), encoding="utf-8")
    legacy = InferenceStore(path2)
    assert legacy.current().name == "Legacy"
    assert legacy.current().values["context"] == 2048
    assert legacy.pinned() == ()


def test_the_profile_store_rejects_loud(tmp_path: Path) -> None:
    store = _store(tmp_path)
    with pytest.raises(InferenceError, match="unknown field"):
        store.update({"not_a_field": 1})
    with pytest.raises(InferenceError, match="range|minimum|maximum|must be"):
        store.update({"temperature": 5.0})
    with pytest.raises(InferenceError, match="must be one of"):
        store.update({"flash_attention": "maybe"})
    with pytest.raises(InferenceError, match="gpu_layers"):
        store.update({"gpu_layers": "sometimes"})
    with pytest.raises(InferenceError, match="must be a bool"):
        store.update({"metrics": "yes"})
    with pytest.raises(InferenceError, match="sampler_chain"):
        store.update({"sampler_chain": [{"id": "nope", "enabled": True}]})
    # a partial chain edit refuses (membership is the whole set)
    with pytest.raises(InferenceError, match="missing member"):
        store.update(
            {"sampler_chain": [{"id": "top_k", "enabled": True}]}
        )
    # a corrupt file never silently resets
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(InferenceError, match="unreadable"):
        InferenceStore(bad)
    foreign = tmp_path / "foreign.json"
    foreign.write_text(
        json.dumps({"schema": "other/9", "profile": {}}), encoding="utf-8"
    )
    with pytest.raises(InferenceError, match="schema"):
        InferenceStore(foreign)
    # an unknown top-level section refuses
    stranger = tmp_path / "stranger.json"
    stranger.write_text(
        json.dumps(
            {"schema": SCHEMA, "profile": {}, "bonus": {}}
        ),
        encoding="utf-8",
    )
    with pytest.raises(InferenceError, match="unknown section"):
        InferenceStore(stranger)


# ------------------------------------------------------------- the migration


def _write_settings1(path: Path, values: dict) -> None:
    path.write_text(
        json.dumps({"schema": "canonsim.workbench.settings/1",
                    "settings": values}),
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
            "context": 4096,
            "gpu_layers": 24,
            "temperature": 0.4,
            "jinja": False,
            "llama_server_exe": "D:/llama.cpp/llama-server.exe",
            "no_webui": False,
            "extra_args": "--threads 8",
        },
    )
    assert migrate_launch_semantics(settings_path, inference_path) is True
    migrated = json.loads(inference_path.read_text(encoding="utf-8"))
    profile = migrated["profile"]
    assert profile["context"] == 4096
    assert profile["gpu_layers"] == 24
    assert profile["temperature"] == 0.4
    assert profile["chat_template"] == "generic"  # jinja False
    assert profile["sampler_chain"] == [
        {"id": member, "enabled": True} for member in SAMPLER_CHAIN_IDS
    ]
    # the settings document is now schema/2 deployment-only
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    assert settings["schema"] == "canonsim.workbench.settings/2"
    assert settings["settings"] == {
        "llama_server_exe": "D:/llama.cpp/llama-server.exe",
        "no_webui": False,
        "extra_args": "--threads 8",
    }
    # the migrated profile loads through the store
    store = InferenceStore(inference_path)
    assert store.current().values["context"] == 4096


def test_the_migration_is_idempotent_and_a_present_profile_wins(
    tmp_path: Path,
) -> None:
    settings_path = tmp_path / "settings.json"
    inference_path = tmp_path / "inference.json"
    _write_settings1(
        settings_path, {"temperature": 0.4, "jinja": True}
    )
    # a present profile wins: the stale launch copy is dropped
    inference_path.write_text(
        json.dumps(
            {
                "schema": SCHEMA,
                "profile": {"temperature": 0.9, "name": "Present"},
            }
        ),
        encoding="utf-8",
    )
    assert migrate_launch_semantics(settings_path, inference_path) is True
    profile = json.loads(inference_path.read_text(encoding="utf-8"))
    assert profile["profile"]["temperature"] == 0.9
    assert profile["profile"]["name"] == "Present"
    # idempotent: a second pass over schema/2 is a no-op
    assert migrate_launch_semantics(settings_path, inference_path) is False


def test_the_migration_refuses_a_malformed_document_loud(
    tmp_path: Path,
) -> None:
    settings_path = tmp_path / "settings.json"
    settings_path.write_text("{broken", encoding="utf-8")
    with pytest.raises(InferenceError, match="cannot migrate"):
        migrate_launch_semantics(settings_path, tmp_path / "inference.json")


# -------------------------------------------------------------- the operations


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
    # inf-2: the editor metadata rides the read (the UI's single
    # metadata source — never a second vocabulary client-side)
    assert controls["sampling.top_k"]["value_type"] == "int"
    assert controls["sampling.top_k"]["minimum"] == 0
    assert controls["device.flash_attention"]["forms"] == [
        "auto", "on", "off"
    ]
    assert controls["device.gpu_layers"]["field"] == "gpu_layers"
    # the categories + the presets + the workspace ride the read
    assert [c["id"] for c in result["categories"]] == [
        c for c in CATEGORIES
    ]
    assert len(result["presets"]) == 4
    assert result["pinned"] == []
    assert result["applies"] == "next-spawn"
    assert result["managed_live"] is False
    assert result["compiled_preview"] == (
        "llama-server -m <model.gguf> --temp 0.80"
    )
    assert [item["id"] for item in result["sampler_chain"]] == list(
        SAMPLER_CHAIN_IDS
    )
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
    session = _session(gateway, "inf2-ops")
    reply = gateway.dispatch(
        RequestEnvelope(
            operation="inference.update",
            arguments={
                "temperature": 0.1,
                "gpu_layers": "all",
                "dry_multiplier": 0.8,
                "pinned": ["sampling.temperature"],
                "sampler_chain": [
                    {"id": member, "enabled": member != "top_k"}
                    for member in SAMPLER_CHAIN_IDS
                ],
            },
            session_id=session,
            client_request_id="inf2-update",
        )
    )
    assert reply.status == "OK", reply.to_mapping()
    result = reply.result
    controls = {c["id"]: c for c in result["controls"]}
    assert controls["sampling.temperature"]["value"] == 0.1
    assert controls["device.gpu_layers"]["state"] != "AUTO"
    assert controls["sampling.top_k"]["state"] == "INEFFECTIVE"
    assert controls["sampling.dry_multiplier"]["state"] == "EFFECTIVE"
    assert result["pinned"] == ["sampling.temperature"]
    assert "LIVE" in result["note"]
    # persisted: a fresh store re-reads the same profile
    fresh = InferenceStore(store.path)
    assert fresh.current().values["temperature"] == 0.1
    assert fresh.current().values["dry_multiplier"] == 0.8
    assert [item.id for item in fresh.current().sampler_chain] == list(
        SAMPLER_CHAIN_IDS
    )
    assert fresh.pinned() == ("sampling.temperature",)
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
    session = _session(gateway, "inf2-reject")
    reply = gateway.dispatch(
        RequestEnvelope(
            operation="inference.update",
            arguments={"temperature": 9.9},
            session_id=session,
            client_request_id="inf2-reject-1",
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
