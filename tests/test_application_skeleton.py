"""wb-3's claim packet (CONTRACTS §5, TEST_PLAN §9's form).

Claim: the Workbench application-operations skeleton (app §32
step 1) is typed, closed-vocabulary, loud-on-violation, and
deterministic exactly where determinism is the law — the §9
identity closure (path is location, not identity; mismatch never
silent), the §10 immutable execution artifact (frozen before side
effects; byte-identical serialization; replay = new identity), the
§16 directory contract (explicit absolute paths, CWD-independent),
the §17 clock domains (separated, injectable), and the §27
dependency envelope (empty — stdlib only).

Lens: determinism + boundary purity (closed vocabularies, the
mismatch laws, no hidden clock anywhere in the artifact chain).
Prism: same-input byte-diff rebuilds; an identity perturbation
(the discriminant); a chdir pair (CWD independence); injected
clock doubles (no host-clock trust); frozen-instance mutation
attempts (immutability).
"""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

from workbench.application import (
    DEPENDENCY_ENVELOPE_VERSION,
    RUNTIME_DEPENDENCIES,
)
from workbench.application.artifact import (
    ARTIFACT_SCHEMA_IDENTITY,
    REPRODUCIBILITY_KINDS,
    REPRODUCIBILITY_SCOPES,
    ArtifactError,
    ExecutionArtifact,
    artifact_from_mapping,
    request_digest,
)
from workbench.application.clock import (
    CLOCK_DOMAINS,
    PROVIDED_DOMAINS,
    AppClock,
    ClockError,
)
from workbench.application.directories import (
    DIRECTORY_STATES,
    PATH_ROLES,
    DirectoryError,
    DirectoryLayout,
    probe_directory,
)
from workbench.application.identity import (
    IDENTITY_AXES,
    INTEGRITY_STATUSES,
    CompositeIdentity,
    ContentIdentity,
    IdentityError,
    content_digest,
)

REPO = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------- identity


def test_content_digest_is_strong_and_stable() -> None:
    first = content_digest(b"model bytes")
    second = content_digest(b"model bytes")
    other = content_digest(b"model bytes ")
    assert first == second
    assert first != other
    assert len(first) == 64
    assert first == first.lower()
    # str and its UTF-8 bytes are the same material
    assert content_digest("prompt") == content_digest("prompt".encode())


def test_identity_axes_are_five_and_closed() -> None:
    assert IDENTITY_AXES == (
        "logical_name",
        "revision",
        "content_digest",
        "location",
        "metadata",
    )
    assert INTEGRITY_STATUSES == frozenset(
        {"VERIFIED", "MISMATCH", "INTEGRITY_UNKNOWN"}
    )


def test_material_identity_binds_name_revision_and_content() -> None:
    base = ContentIdentity.from_bytes("llama", "r1", b"weights")
    renamed = ContentIdentity.from_bytes("other", "r1", b"weights")
    revised = ContentIdentity.from_bytes("llama", "r2", b"weights")
    rewritten = ContentIdentity.from_bytes("llama", "r1", b"weights2")
    ids = {
        base.material_identity(),
        renamed.material_identity(),
        revised.material_identity(),
        rewritten.material_identity(),
    }
    # the §9 equation: each axis change yields a distinct material
    # identity — same path + new bytes → new content identity; same
    # name + new revision → new revision identity
    assert len(ids) == 4


def test_recheck_laws_never_silent() -> None:
    frozen = ContentIdentity.from_bytes("pack", "r1", b"original")
    assert frozen.recheck(b"original") == "VERIFIED"
    # same revision + new bytes → identity mismatch, the caller
    # refuses reuse (never a quiet pass)
    assert frozen.recheck(b"tampered") == "MISMATCH"
    undigested = ContentIdentity(
        logical_name="pack", revision="r1", content_digest=None
    )
    # failed/incomplete strong hashing is explicit
    assert undigested.recheck(b"anything") == "INTEGRITY_UNKNOWN"


def test_identity_construction_is_loud() -> None:
    with pytest.raises(IdentityError):
        ContentIdentity(logical_name="", revision="r1", content_digest=None)
    with pytest.raises(IdentityError):
        ContentIdentity(
            logical_name="pack", revision="", content_digest=None
        )
    with pytest.raises(IdentityError):
        ContentIdentity(
            logical_name="pack", revision="r1", content_digest="not-hex"
        )
    with pytest.raises(IdentityError):
        ContentIdentity(
            logical_name="pack",
            revision="r1",
            content_digest=None,
            metadata=(("dup", "a"), ("dup", "b")),
        )


def test_composite_identity_is_order_independent() -> None:
    shards = [
        ContentIdentity.from_bytes("shard-a", "r1", b"AAAA"),
        ContentIdentity.from_bytes("shard-b", "r1", b"BBBB"),
        ContentIdentity.from_bytes("shard-c", "r1", b"CCCC"),
    ]
    forward = CompositeIdentity("model", "r1", tuple(shards))
    backward = CompositeIdentity("model", "r1", tuple(reversed(shards)))
    # the same material set yields the same composite regardless of
    # assembly order (a shard set has no meaningful construction
    # order — sorted wins, the INV-2 read-side rule)
    assert forward.composite_digest() == backward.composite_digest()
    # one shard's bytes change → the composite changes
    swapped = CompositeIdentity(
        "model",
        "r1",
        (
            ContentIdentity.from_bytes("shard-a", "r1", b"AAAX"),
            shards[1],
            shards[2],
        ),
    )
    assert swapped.composite_digest() != forward.composite_digest()


def test_composite_integrity_is_all_or_unknown() -> None:
    strong = [
        ContentIdentity.from_bytes("s1", "r1", b"1"),
        ContentIdentity.from_bytes("s2", "r1", b"2"),
    ]
    assert CompositeIdentity("m", "r1", tuple(strong)).integrity() == (
        "VERIFIED"
    )
    partial = [
        ContentIdentity.from_bytes("s1", "r1", b"1"),
        ContentIdentity("s2", "r1", None),
    ]
    assert CompositeIdentity("m", "r1", tuple(partial)).integrity() == (
        "INTEGRITY_UNKNOWN"
    )
    with pytest.raises(IdentityError):
        CompositeIdentity("m", "r1", ())
    with pytest.raises(IdentityError):
        CompositeIdentity(
            "m", "r1", (strong[0], ContentIdentity.from_bytes("s1", "r2", b"x"))
        )


# --------------------------------------------------------------- artifact


def _sample_artifact(execution_id: str = "exec-001") -> ExecutionArtifact:
    return ExecutionArtifact.freeze(
        execution_id=execution_id,
        status="COMPLETED",
        frozen_inputs={
            "prompt": content_digest("system text"),
            "grammar": content_digest("gbnf snapshot"),
            "seed": "125",
        },
        operation_id="op-77",
        model_identity="model-material-id",
        replay_of=None,
        reproducibility_scope="SEMANTIC",
    )


def test_artifact_freezes_the_ten_field_list() -> None:
    mapping = json.loads(_sample_artifact().to_json())
    for key in (
        "execution_id",
        "operation_id",
        "model_identity",
        "pack_schema_identity",
        "prompt_identity",
        "frozen_inputs",
        "inference_config",
        "backend_identity",
        "runtime_identity",
        "protocol_identity",
        "capability_snapshot",
        "request_digest",
        "seed",
        "tool_authority_state",
        "status",
        "diagnostics",
        "replay_of",
        "reproducibility_scope",
        "artifact_schema_identity",
    ):
        assert key in mapping, f"§10 field {key} missing from the artifact"


def test_artifact_is_immutable_and_loud() -> None:
    artifact = _sample_artifact()
    with pytest.raises(AttributeError):
        artifact.status = "FAILED"  # type: ignore[misc]
    with pytest.raises(ArtifactError):
        ExecutionArtifact(execution_id="", status="COMPLETED")
    with pytest.raises(ArtifactError):
        ExecutionArtifact.freeze("exec-x", "COMPLETED", {"name": ""})
    with pytest.raises(ArtifactError):
        ExecutionArtifact.freeze(
            "exec-x", "COMPLETED", [("n", "v"), ("n", "w")]
        )
    with pytest.raises(ArtifactError):
        ExecutionArtifact.freeze(
            "exec-x",
            "COMPLETED",
            {"name": "v"},
            reproducibility_scope="ROUGHLY",
        )


def test_artifact_rebuild_is_byte_identical_no_hidden_clock() -> None:
    first = _sample_artifact().to_json()
    second = _sample_artifact().to_json()
    assert first == second
    # the freeze constructor is order-insensitive over the inputs map
    shuffled = ExecutionArtifact.freeze(
        "exec-001",
        "COMPLETED",
        [
            ("seed", "125"),
            ("grammar", content_digest("gbnf snapshot")),
            ("prompt", content_digest("system text")),
        ],
        operation_id="op-77",
        model_identity="model-material-id",
        reproducibility_scope="SEMANTIC",
    ).to_json()
    assert first == shuffled


def test_request_reproducibility_same_inputs_same_digest() -> None:
    inputs = {"prompt": content_digest("p"), "seed": "125"}
    reordered = dict(reversed(list(inputs.items())))
    assert request_digest(inputs) == request_digest(reordered)
    other = {"prompt": content_digest("q"), "seed": "125"}
    assert request_digest(inputs) != request_digest(other)
    artifact = _sample_artifact()
    # the stored digest re-derives from the frozen inputs
    assert artifact.request_digest_field == artifact.inputs_digest()


def test_replay_is_a_new_execution_identity() -> None:
    original = _sample_artifact("exec-001")
    replay = _sample_artifact("exec-002")
    object.__setattr__(replay, "replay_of", "exec-001")
    assert replay.execution_id != original.execution_id
    assert replay.replay_of == original.execution_id
    # same frozen inputs → same request digest (the REQUEST kind is
    # reproducible), different executions (§10: replay creates a NEW
    # execution identity — the link is lineage, never reuse)
    assert replay.request_digest_field == original.request_digest_field
    assert json.loads(replay.to_json())["replay_of"] == "exec-001"


def test_artifact_roundtrip_is_strict() -> None:
    artifact = _sample_artifact()
    mapping = json.loads(artifact.to_json())
    rebuilt = artifact_from_mapping(mapping)
    assert rebuilt.to_json() == artifact.to_json()
    drifted = dict(mapping)
    drifted["surprise"] = "field"
    with pytest.raises(ArtifactError):
        artifact_from_mapping(drifted)
    with pytest.raises(ArtifactError):
        drifted = dict(mapping)
        drifted["artifact_schema_identity"] = "canon_execution_artifact@9.9"
        artifact_from_mapping(drifted)


def test_reproducibility_vocabularies_closed() -> None:
    assert REPRODUCIBILITY_SCOPES == frozenset(
        {"EXACT_BITWISE", "SEMANTIC", "APPROXIMATE", "EXPLANATORY_ONLY"}
    )
    assert REPRODUCIBILITY_KINDS == frozenset(
        {"CANONICAL", "REQUEST", "INFERENCE"}
    )
    assert ARTIFACT_SCHEMA_IDENTITY == "canon_execution_artifact@0.1"


def test_artifact_module_never_imports_the_clock() -> None:
    """§17's hard sentence made executable on the module graph: the
    artifact chain may hold no clock — a wall/monotonic value enters
    an artifact only as an explicit frozen input, never a hidden
    read (the byte-identical rebuild above is the runtime proof;
    this is the static one)."""
    source = (REPO / "workbench" / "application" / "artifact.py").read_text(
        encoding="utf-8"
    )
    assert "import time" not in source
    assert "from workbench.application.clock" not in source


# ------------------------------------------------------------ directories


def test_directory_roles_and_states_are_closed() -> None:
    assert PATH_ROLES == frozenset(
        {
            "RUNTIME",
            "USER_CONFIG",
            "USER_DATA",
            "MODELS_ASSETS",
            "CACHE",
            "BACKUPS",
            "LOGS",
        }
    )
    assert DIRECTORY_STATES == frozenset(
        {
            "OK",
            "MISSING",
            "READ_ONLY",
            "PERMISSION_DENIED",
            "CORRUPT",
            "PARTIALLY_MIGRATED",
            "EXTERNALLY_REMOVED",
        }
    )


def test_layout_requires_absolute_root_and_is_loud() -> None:
    with pytest.raises(DirectoryError):
        DirectoryLayout(root=Path("relative/root"))
    with pytest.raises(DirectoryError):
        DirectoryLayout(root="not-even-a-path")  # type: ignore[arg-type]
    layout = DirectoryLayout(root=Path("/opt/canonsim"))
    with pytest.raises(DirectoryError):
        layout.path_for("NOT_A_ROLE")


def test_layout_paths_are_cwd_independent(tmp_path: Path) -> None:
    layout = DirectoryLayout(root=Path("/opt/canonsim"))
    before = layout.all_paths()
    original = Path.cwd()
    try:
        os.chdir(tmp_path)
        after = layout.all_paths()
    finally:
        os.chdir(original)
    assert before == after
    assert before["CACHE"] == Path("/opt/canonsim/cache")
    assert set(before) == set(PATH_ROLES)


def test_probe_classifies_missing_ok_denied(tmp_path: Path) -> None:
    assert probe_directory(tmp_path / "absent") == "MISSING"
    assert probe_directory(tmp_path) == "OK"
    occupied = tmp_path / "occupied"
    occupied.write_text("a file in the directory slot", encoding="utf-8")
    assert probe_directory(occupied) == "CORRUPT"
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        pytest.skip("running as root — permission bits do not bind")
    locked = tmp_path / "locked"
    locked.mkdir()
    locked.chmod(stat.S_IRUSR | stat.S_IXUSR)
    try:
        assert probe_directory(locked) == "PERMISSION_DENIED"
    finally:
        locked.chmod(stat.S_IRWXU)
    assert probe_directory(locked) == "OK"


# ------------------------------------------------------------------ clock


def test_clock_domains_closed_and_two_provided() -> None:
    assert CLOCK_DOMAINS == frozenset(
        {"SEMANTIC", "MONOTONIC", "UTC_WALL", "UI_ANIMATION"}
    )
    # SEMANTIC (the engine's tick axis) and UI_ANIMATION (the
    # presentation side) are named-only — never sourced here
    assert PROVIDED_DOMAINS == frozenset({"MONOTONIC", "UTC_WALL"})


def test_app_clock_uses_injected_providers() -> None:
    calls = {"monotonic": 0, "utc": 0}

    def fake_monotonic() -> float:
        calls["monotonic"] += 1
        return 100.0

    def fake_utc() -> float:
        calls["utc"] += 1
        return 1_700_000_000.0

    clock = AppClock(monotonic=fake_monotonic, utc=fake_utc)
    assert clock.now_monotonic() == 100.0
    assert clock.now_utc() == 1_700_000_000.0
    assert calls == {"monotonic": 1, "utc": 1}
    with pytest.raises(ClockError):
        AppClock(monotonic="not-callable", utc=fake_utc)  # type: ignore[arg-type]
    wired = AppClock(monotonic=fake_monotonic, utc=fake_utc)
    with pytest.raises(AttributeError):
        wired.utc = fake_utc  # type: ignore[misc]


def test_app_clock_defaults_are_real_and_monotonic() -> None:
    clock = AppClock()
    first = clock.now_monotonic()
    second = clock.now_monotonic()
    assert second >= first


# ---------------------------------------------------- dependency envelope


def test_dependency_envelope_is_empty_and_declared() -> None:
    assert RUNTIME_DEPENDENCIES == frozenset()
    assert DEPENDENCY_ENVELOPE_VERSION == "envelope@0.1"


def test_envelope_agrees_with_pyproject() -> None:
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    assert 'dependencies = []' in pyproject
    assert '"workbench.application"' in pyproject


def test_skeleton_is_deterministic_across_hashseeds() -> None:
    """INV-2's read-side discipline, stronger than the suite's fixed
    seed: the identity/artifact chain must be byte-identical under a
    different PYTHONHASHSEED (sha256 + sorted — no reliance on
    dict/set iteration order anywhere in the skeleton)."""
    code = (
        "from workbench.application.artifact import ExecutionArtifact\n"
        "from workbench.application.identity import CompositeIdentity,"
        " ContentIdentity, content_digest\n"
        "shards = (ContentIdentity.from_bytes('s-a','r1',b'AAAA'),"
        " ContentIdentity.from_bytes('s-b','r1',b'BBBB'))\n"
        "comp = CompositeIdentity('m','r1',shards)\n"
        "a = ExecutionArtifact.freeze('e1','COMPLETED',"
        "{'p': content_digest('x'),'seed':'7'},"
        " model_identity=comp.composite_digest())\n"
        "print(comp.composite_digest())\n"
        "print(a.to_json())\n"
    )
    outputs = []
    for seed in ("0", "12345"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            env=env,
            cwd=str(REPO),
            check=True,
        )
        outputs.append(result.stdout)
    assert outputs[0] == outputs[1]
